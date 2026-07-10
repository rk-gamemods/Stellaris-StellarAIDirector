from __future__ import annotations

import contextlib
import errno
import hashlib
import json
import os
import sqlite3
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterator

from .paths import BACKUP_ROOT, LIVE_DATABASE, WRITE_LOCK


APPLICATION_ID = 1_397_441_074
USER_VERSION = 4
BUSY_TIMEOUT_MS = 30_000


class KnowledgeBaseError(RuntimeError):
    """Raised when a database safety or identity contract fails."""


class KnowledgeBaseConnection(sqlite3.Connection):
    """SQLite connection that retains cooperative maintenance access until close."""

    _maintenance_descriptor: int | None = None

    def close(self) -> None:
        descriptor = self._maintenance_descriptor
        self._maintenance_descriptor = None
        try:
            super().close()
        finally:
            if descriptor is not None:
                _unlock_descriptor(descriptor)
                os.close(descriptor)


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def publish_no_replace(temporary: Path, destination: Path) -> None:
    """Atomically publish a same-volume file without replacing an existing path."""
    try:
        os.link(temporary, destination)
    except FileExistsError as exc:
        raise KnowledgeBaseError(f"Refusing to overwrite existing file: {destination}") from exc
    except OSError as exc:
        raise KnowledgeBaseError(
            f"Could not atomically publish {destination} without replacement: {exc}"
        ) from exc
    temporary.unlink()


def _configure_connection(connection: sqlite3.Connection, *, read_only: bool) -> None:
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
    connection.execute("PRAGMA recursive_triggers=ON")
    if read_only:
        connection.execute("PRAGMA query_only=ON")


def connect_read_only(
    path: Path,
    *,
    expected_user_version: int = USER_VERSION,
    maintenance_held: bool = False,
) -> sqlite3.Connection:
    if not path.is_file():
        raise KnowledgeBaseError(f"Knowledge-base file does not exist: {path}")
    uri = f"file:{path.resolve().as_posix()}?mode=ro"
    descriptor = None if maintenance_held else _acquire_maintenance_descriptor(path, shared=True)
    try:
        connection = sqlite3.connect(
            uri,
            uri=True,
            timeout=BUSY_TIMEOUT_MS / 1000,
            factory=KnowledgeBaseConnection,
        )
        connection._maintenance_descriptor = descriptor
    except Exception:
        if descriptor is not None:
            _unlock_descriptor(descriptor)
            os.close(descriptor)
        raise
    try:
        connection.row_factory = sqlite3.Row
        _configure_connection(connection, read_only=True)
        verify_identity(connection, expected_user_version=expected_user_version)
        return connection
    except Exception:
        connection.close()
        raise


def connect_writer(
    path: Path,
    *,
    expected_user_version: int = USER_VERSION,
    maintenance_held: bool = False,
) -> sqlite3.Connection:
    if not path.is_file():
        raise KnowledgeBaseError(f"Knowledge-base file does not exist: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = None if maintenance_held else _acquire_maintenance_descriptor(path, shared=True)
    try:
        connection = sqlite3.connect(
            path,
            timeout=BUSY_TIMEOUT_MS / 1000,
            factory=KnowledgeBaseConnection,
        )
        connection._maintenance_descriptor = descriptor
    except Exception:
        if descriptor is not None:
            _unlock_descriptor(descriptor)
            os.close(descriptor)
        raise
    try:
        connection.row_factory = sqlite3.Row
        _configure_connection(connection, read_only=False)
        verify_identity(connection, expected_user_version=expected_user_version)
        return connection
    except Exception:
        connection.close()
        raise


def verify_identity(
    connection: sqlite3.Connection,
    *,
    expected_user_version: int = USER_VERSION,
) -> None:
    application_id = int(connection.execute("PRAGMA application_id").fetchone()[0])
    user_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
    if application_id != APPLICATION_ID:
        raise KnowledgeBaseError(
            f"Refusing database with application_id={application_id}; expected {APPLICATION_ID}."
        )
    if user_version != expected_user_version:
        raise KnowledgeBaseError(
            f"Refusing database with user_version={user_version}; expected {expected_user_version}."
        )
    if int(connection.execute("PRAGMA foreign_keys").fetchone()[0]) != 1:
        raise KnowledgeBaseError("SQLite foreign-key enforcement is not active on this connection.")


@dataclass(frozen=True)
class LockOwner:
    pid: int
    acquired_at: str
    purpose: str


def _prepare_lock_file(descriptor: int) -> None:
    if os.fstat(descriptor).st_size == 0:
        os.write(descriptor, b"\0")
        os.fsync(descriptor)
    os.lseek(descriptor, 0, os.SEEK_SET)


def _try_lock_descriptor(descriptor: int, *, shared: bool = False) -> bool:
    _prepare_lock_file(descriptor)
    try:
        if os.name == "nt":
            import ctypes
            import msvcrt
            from ctypes import wintypes

            class Overlapped(ctypes.Structure):
                _fields_ = (
                    ("Internal", ctypes.c_size_t),
                    ("InternalHigh", ctypes.c_size_t),
                    ("Offset", wintypes.DWORD),
                    ("OffsetHigh", wintypes.DWORD),
                    ("hEvent", wintypes.HANDLE),
                )

            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.LockFileEx.argtypes = (
                wintypes.HANDLE,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.DWORD,
                ctypes.POINTER(Overlapped),
            )
            kernel32.LockFileEx.restype = wintypes.BOOL
            handle = wintypes.HANDLE(msvcrt.get_osfhandle(descriptor))
            flags = 0x00000001 | (0 if shared else 0x00000002)
            overlapped = Overlapped()
            if not kernel32.LockFileEx(handle, flags, 0, 1, 0, ctypes.byref(overlapped)):
                error = ctypes.get_last_error()
                if error in {32, 33, 158}:
                    return False
                raise ctypes.WinError(error)
        else:
            import fcntl

            mode = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
            fcntl.flock(descriptor, mode | fcntl.LOCK_NB)
        return True
    except OSError as exc:
        if exc.errno in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
            return False
        raise


def _unlock_descriptor(descriptor: int) -> None:
    os.lseek(descriptor, 0, os.SEEK_SET)
    if os.name == "nt":
        import ctypes
        import msvcrt
        from ctypes import wintypes

        class Overlapped(ctypes.Structure):
            _fields_ = (
                ("Internal", ctypes.c_size_t),
                ("InternalHigh", ctypes.c_size_t),
                ("Offset", wintypes.DWORD),
                ("OffsetHigh", wintypes.DWORD),
                ("hEvent", wintypes.HANDLE),
            )

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.UnlockFileEx.argtypes = (
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.POINTER(Overlapped),
        )
        kernel32.UnlockFileEx.restype = wintypes.BOOL
        handle = wintypes.HANDLE(msvcrt.get_osfhandle(descriptor))
        overlapped = Overlapped()
        if not kernel32.UnlockFileEx(handle, 0, 1, 0, ctypes.byref(overlapped)):
            raise ctypes.WinError(ctypes.get_last_error())
    else:
        import fcntl

        fcntl.flock(descriptor, fcntl.LOCK_UN)


def _read_lock_metadata(descriptor: int) -> str:
    os.lseek(descriptor, 1, os.SEEK_SET)
    return os.read(descriptor, 1024 * 1024).decode("utf-8", errors="replace").rstrip("\0")


def writer_lock_path(database: Path) -> Path:
    return Path(str(database.resolve()) + ".write.lock")


def maintenance_lock_path(database: Path) -> Path:
    return Path(str(database.resolve()) + ".maintenance.lock")


def maintenance_status(database: Path) -> dict[str, object]:
    lock_path = maintenance_lock_path(database)
    if not lock_path.exists():
        return {
            "active": False,
            "metadata_file_exists": False,
            "path": str(lock_path),
        }
    descriptor = os.open(lock_path, os.O_RDWR)
    try:
        active = not _try_lock_descriptor(descriptor, shared=False)
        if not active:
            _unlock_descriptor(descriptor)
        return {
            "active": active,
            "metadata_file_exists": True,
            "path": str(lock_path),
            "meaning": "active means one or more shared database users or exclusive maintenance",
        }
    finally:
        os.close(descriptor)


def _acquire_maintenance_descriptor(database: Path, *, shared: bool) -> int:
    lock_path = maintenance_lock_path(database)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        if not _try_lock_descriptor(descriptor, shared=shared):
            mode = "shared access" if shared else "exclusive maintenance"
            raise KnowledgeBaseError(
                f"Cannot acquire {mode} for {database}; another database user is active."
            )
        return descriptor
    except Exception:
        os.close(descriptor)
        raise


@contextlib.contextmanager
def exclusive_maintenance_barrier(database: Path) -> Iterator[None]:
    descriptor = _acquire_maintenance_descriptor(database, shared=False)
    try:
        yield
    finally:
        _unlock_descriptor(descriptor)
        os.close(descriptor)


@contextlib.contextmanager
def exclusive_writer_lock(purpose: str, lock_path: Path = WRITE_LOCK) -> Iterator[LockOwner]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    owner = LockOwner(pid=os.getpid(), acquired_at=utc_now(), purpose=purpose)
    flags = os.O_CREAT | os.O_RDWR
    descriptor = os.open(lock_path, flags, 0o600)
    try:
        existing = _read_lock_metadata(descriptor) or "<metadata not yet written>"
        if not _try_lock_descriptor(descriptor):
            raise KnowledgeBaseError(
                f"The serialized writer lock is active at {lock_path}: {existing}. "
                "Use the doctor command to inspect it; do not delete the lock file."
            )
        payload = b"\0" + (
            json.dumps(owner.__dict__, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        os.lseek(descriptor, 0, os.SEEK_SET)
        os.ftruncate(descriptor, 0)
        os.write(descriptor, payload)
        os.fsync(descriptor)
        try:
            yield owner
        finally:
            _unlock_descriptor(descriptor)
    finally:
        os.close(descriptor)


def lock_status(lock_path: Path = WRITE_LOCK) -> dict[str, object]:
    if not lock_path.exists():
        return {
            "exists": False,
            "active": False,
            "metadata_file_exists": False,
            "path": str(lock_path),
        }
    descriptor = os.open(lock_path, os.O_RDWR)
    try:
        metadata = _read_lock_metadata(descriptor)
        active = not _try_lock_descriptor(descriptor)
        if not active:
            _unlock_descriptor(descriptor)
        result: dict[str, object] = {
            "exists": active,
            "active": active,
            "metadata_file_exists": True,
            "path": str(lock_path),
        }
        try:
            result["owner" if active else "last_owner"] = json.loads(
                metadata
            )
        except (OSError, json.JSONDecodeError) as exc:
            result["error"] = str(exc)
        return result
    finally:
        os.close(descriptor)


SEMANTIC_CHECKS: tuple[tuple[str, str], ...] = (
    (
        "runtime_question_without_approval_guard",
        """
        SELECT COUNT(*) FROM open_question
        WHERE evidence_mode_code IN ('runtime','mixed')
          AND runtime_approval_required <> 1
        """,
    ),
    ("sidecar_type_mismatch", "SELECT COUNT(*) FROM v_sidecar_type_mismatch"),
    (
        "current_assessment_overlap_for_same_claim",
        """
        SELECT COUNT(*) FROM (
            SELECT a.claim_id
            FROM claim_assessment a
            JOIN claim_assessment b
              ON a.claim_assessment_id < b.claim_assessment_id
             AND a.claim_id = b.claim_id
             AND a.is_current = 1
             AND b.is_current = 1
            JOIN version_span avs ON avs.version_span_id = a.version_span_id
            JOIN version_span bvs ON bvs.version_span_id = b.version_span_id
            LEFT JOIN game_version amin ON amin.game_version_id = avs.min_version_id
            LEFT JOIN game_version amax ON amax.game_version_id = avs.max_version_id
            LEFT JOIN game_version bmin ON bmin.game_version_id = bvs.min_version_id
            LEFT JOIN game_version bmax ON bmax.game_version_id = bvs.max_version_id
            WHERE COALESCE(amin.version_order, -9223372036854775808)
                  <= COALESCE(bmax.version_order, 9223372036854775807)
              AND COALESCE(bmin.version_order, -9223372036854775808)
                  <= COALESCE(amax.version_order, 9223372036854775807)
        )
        """,
    ),
    (
        "analysis_dimension_type_mismatch",
        "SELECT COUNT(*) FROM v_analysis_dimension_type_mismatch",
    ),
    (
        "dataset_key_column_orphan",
        """
        SELECT COUNT(*)
        FROM dataset_key_column dkc
        LEFT JOIN dataset_column dc
          ON dc.dataset_schema_id=dkc.dataset_schema_id
         AND dc.dataset_column_id=dkc.dataset_column_id
        WHERE dc.dataset_column_id IS NULL
        """,
    ),
    (
        "playset_resolution_without_winner",
        """
        SELECT COUNT(*) FROM playset_object_resolution
        WHERE resolution_status IN ('single','resolved') AND winning_definition_id IS NULL
        """,
    ),
    (
        "current_playset_duplicate_position",
        """
        SELECT COUNT(*) FROM (
          SELECT playset_snapshot_id, load_position
          FROM playset_member
          GROUP BY playset_snapshot_id, load_position
          HAVING COUNT(*) > 1
        )
        """,
    ),
    (
        "open_change_sets",
        "SELECT COUNT(*) FROM change_set WHERE state='open'",
    ),
    (
        "primary_target_not_4_4_4",
        "SELECT CASE WHEN COUNT(*)=1 THEN 0 ELSE 1 END FROM game_version "
        "WHERE is_primary_target=1 AND version_label='4.4.4'",
    ),
)


def validate_database(
    path: Path,
    *,
    full: bool = True,
    expected_user_version: int = USER_VERSION,
    fts_integrity: bool = True,
    maintenance_held: bool = False,
) -> dict[str, object]:
    with contextlib.closing(
        connect_read_only(
            path,
            expected_user_version=expected_user_version,
            maintenance_held=maintenance_held,
        )
    ) as connection:
        result: dict[str, object] = {
            "database": str(path.resolve()),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
            "sqlite_version": sqlite3.sqlite_version,
            "application_id": int(connection.execute("PRAGMA application_id").fetchone()[0]),
            "user_version": int(connection.execute("PRAGMA user_version").fetchone()[0]),
            "foreign_keys": int(connection.execute("PRAGMA foreign_keys").fetchone()[0]),
            "journal_mode": str(connection.execute("PRAGMA journal_mode").fetchone()[0]),
            "primary_target": connection.execute(
                "SELECT version_label FROM game_version WHERE is_primary_target=1"
            ).fetchone()[0],
        }
        checks = SEMANTIC_CHECKS
        if expected_user_version < 4:
            checks = tuple(
                check for check in checks if check[0] != "runtime_question_without_approval_guard"
            )
        result["semantic_checks"] = {
            name: int(connection.execute(sql).fetchone()[0]) for name, sql in checks
        }
        result["foreign_key_violations"] = len(
            connection.execute("PRAGMA foreign_key_check").fetchall()
        )
        if full:
            result["integrity_check"] = connection.execute("PRAGMA integrity_check").fetchone()[0]
            result["quick_check"] = connection.execute("PRAGMA quick_check").fetchone()[0]
            fts_pairs = (
                ("item_fts", "knowledge_item"),
                ("claim_fts", "claim"),
                ("question_fts", "open_question"),
                ("evidence_fts", "evidence_locator"),
            )
            result["fts_shadow_mismatches"] = {
                fts: int(
                    connection.execute(
                        f"""
                        SELECT
                          (SELECT COUNT(*) FROM {content}
                           WHERE rowid NOT IN (SELECT id FROM {fts}_docsize))
                          +
                          (SELECT COUNT(*) FROM {fts}_docsize
                           WHERE id NOT IN (SELECT rowid FROM {content}))
                        """
                    ).fetchone()[0]
                )
                for fts, content in fts_pairs
            }
        problems = [
            name
            for name, count in result["semantic_checks"].items()
            if int(count) != 0
        ]
        if result["foreign_key_violations"]:
            problems.append("foreign_key_violations")
        if full and result.get("integrity_check") != "ok":
            problems.append("integrity_check")
        if full and any(result.get("fts_shadow_mismatches", {}).values()):
            problems.append("fts_shadow_mismatch")
        result["fts5"] = "shadow-check-ok" if full else "not_checked"
        result["ok"] = not problems
        result["problems"] = problems
    if full and fts_integrity:
        try:
            with contextlib.closing(
                connect_writer(
                    path,
                    expected_user_version=expected_user_version,
                    maintenance_held=maintenance_held,
                )
            ) as writer:
                writer.execute("BEGIN IMMEDIATE")
                for table in ("item_fts", "claim_fts", "question_fts", "evidence_fts"):
                    writer.execute(
                        f"INSERT INTO {table}({table},rank) VALUES ('integrity-check',1)"
                    )
                writer.rollback()
            result["fts5"] = "integrity-check-ok"
        except sqlite3.DatabaseError as exc:
            result["fts5"] = f"integrity-check-failed: {exc}"
            result["problems"].append("fts5_integrity_check")
            result["ok"] = False
    return result


def checkpoint_database(
    path: Path, *, truncate: bool = True, maintenance_held: bool = False
) -> dict[str, int]:
    with contextlib.closing(
        connect_writer(path, maintenance_held=maintenance_held)
    ) as connection:
        mode = "TRUNCATE" if truncate else "PASSIVE"
        busy, log_frames, checkpointed = connection.execute(
            f"PRAGMA wal_checkpoint({mode})"
        ).fetchone()
        if busy:
            raise KnowledgeBaseError(
                f"WAL checkpoint remained busy: busy={busy}, log={log_frames}, checkpointed={checkpointed}"
            )
        return {
            "busy": int(busy),
            "log_frames": int(log_frames),
            "checkpointed_frames": int(checkpointed),
        }


def online_backup(
    source: Path,
    output: Path | None = None,
    *,
    expected_user_version: int = USER_VERSION,
    maintenance_held: bool = False,
) -> dict[str, object]:
    if output is None:
        backup_root = (
            BACKUP_ROOT
            if source.resolve() == LIVE_DATABASE.resolve()
            else source.resolve().parent / "backups"
        )
        backup_root.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
        output = backup_root / f"stellaris_knowledge_base-{stamp}.sqlite3"
    output = output.resolve()
    if output.exists():
        raise KnowledgeBaseError(f"Refusing to overwrite backup: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(name)
    temporary.unlink(missing_ok=True)
    try:
        with contextlib.closing(
            connect_read_only(
                source,
                expected_user_version=expected_user_version,
                maintenance_held=maintenance_held,
            )
        ) as src, contextlib.closing(
            sqlite3.connect(temporary)
        ) as dst:
            src.backup(dst)
        validation = validate_database(
            temporary,
            full=True,
            expected_user_version=expected_user_version,
        )
        if not validation["ok"]:
            raise KnowledgeBaseError(f"Backup validation failed: {validation['problems']}")
        publish_no_replace(temporary, output)
        validation["database"] = str(output)
        validation["size_bytes"] = output.stat().st_size
        validation["sha256"] = sha256_file(output)
        return {
            "path": str(output),
            "size_bytes": validation["size_bytes"],
            "sha256": validation["sha256"],
            "validation": validation,
        }
    finally:
        temporary.unlink(missing_ok=True)
        maintenance_lock_path(temporary).unlink(missing_ok=True)
