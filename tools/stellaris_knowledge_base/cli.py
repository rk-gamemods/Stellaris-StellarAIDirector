from __future__ import annotations

import argparse
import contextlib
import json
import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path
from typing import Any

from .catalog import catalog_is_current, populate_database, prepare_catalog
from .db import (
    APPLICATION_ID,
    USER_VERSION,
    KnowledgeBaseError,
    checkpoint_database,
    exclusive_maintenance_barrier,
    exclusive_writer_lock,
    lock_status,
    maintenance_lock_path,
    maintenance_status,
    online_backup,
    validate_database,
    writer_lock_path,
)
from .migrations import build_atomic_database, migrate_database
from .packets import apply_packet, dry_run_packet, prepare_packet
from .paths import LIVE_DATABASE, TARGET_VERSION
from .queries import (
    catalog_sources,
    dossier,
    gaps,
    impact,
    read_only_sql,
    search,
    status,
)


def _print(payload: Any) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False, default=str))


def _database(value: str | None) -> Path:
    return Path(value).expanduser().resolve() if value else LIVE_DATABASE.resolve()


def _raw_database_identity(database: Path) -> tuple[int, int]:
    if not database.is_file():
        raise KnowledgeBaseError(f"Knowledge-base file does not exist: {database}")
    uri = f"file:{database.resolve().as_posix()}?mode=ro"
    with contextlib.closing(sqlite3.connect(uri, uri=True)) as connection:
        return (
            int(connection.execute("PRAGMA application_id").fetchone()[0]),
            int(connection.execute("PRAGMA user_version").fetchone()[0]),
        )


def _require_valid(validation: dict[str, Any], operation: str) -> dict[str, Any]:
    if not validation["ok"]:
        raise KnowledgeBaseError(
            f"{operation} failed post-operation validation: {validation['problems']}"
        )
    return validation


def _restore(database: Path, backup: Path, confirm: bool) -> dict[str, Any]:
    if not confirm:
        raise KnowledgeBaseError("Restore requires --confirm-replace.")
    backup = backup.expanduser().resolve()
    validation = validate_database(backup, full=True)
    if not validation["ok"]:
        raise KnowledgeBaseError(f"Backup is not valid: {validation['problems']}")
    if validation["application_id"] != APPLICATION_ID or validation["user_version"] != USER_VERSION:
        raise KnowledgeBaseError("Backup identity/version does not match this installation.")
    checkpoint = None
    before_identity = None
    with exclusive_writer_lock(f"restore from {backup}", writer_lock_path(database)):
        with exclusive_maintenance_barrier(database):
            safety = (
                online_backup(database, maintenance_held=True) if database.exists() else None
            )
            if safety:
                before = safety["validation"]
                before_identity = {
                    "application_id": before["application_id"],
                    "user_version": before["user_version"],
                    "primary_target": before["primary_target"],
                }
            if database.exists():
                checkpoint = checkpoint_database(
                    database,
                    truncate=True,
                    maintenance_held=True,
                )
            database.parent.mkdir(parents=True, exist_ok=True)
            descriptor, name = tempfile.mkstemp(
                prefix=".restore.", suffix=".sqlite3", dir=database.parent
            )
            os.close(descriptor)
            temporary = Path(name)
            temporary.unlink(missing_ok=True)
            try:
                source_uri = f"file:{backup.as_posix()}?mode=ro"
                with contextlib.closing(
                    sqlite3.connect(source_uri, uri=True)
                ) as source, contextlib.closing(sqlite3.connect(temporary)) as target:
                    source.backup(target)
                restored = validate_database(temporary, full=True)
                if not restored["ok"]:
                    raise KnowledgeBaseError(
                        f"Restored copy failed validation: {restored['problems']}"
                    )
                os.replace(temporary, database)
            finally:
                temporary.unlink(missing_ok=True)
                maintenance_lock_path(temporary).unlink(missing_ok=True)
            final_validation = _require_valid(
                validate_database(
                    database,
                    full=True,
                    maintenance_held=True,
                ),
                "restore",
            )
    return {
        "result": "restored",
        "database": str(database),
        "input": str(backup),
        "before_identity": before_identity,
        "after_identity": {
            "application_id": final_validation["application_id"],
            "user_version": final_validation["user_version"],
            "primary_target": final_validation["primary_target"],
        },
        "safety_backup": safety,
        "checkpoint": checkpoint,
        "coordination": {
            "writer": lock_status(writer_lock_path(database)),
            "maintenance": maintenance_status(database),
        },
        "validation": final_validation,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install, populate, query, and safely maintain the local Stellaris knowledge base."
    )
    parser.add_argument("--database", help=f"Override live database path (default: {LIVE_DATABASE}).")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("install", help="Create and fully populate a new production database atomically.")
    sub.add_parser("refresh", help="Rescan current project/vanilla inputs and ingest changed revisions.")
    sub.add_parser("status", help="Show identity, target, catalog, knowledge, and last-ingest state.")

    validate = sub.add_parser("validate", help="Run identity, semantic, FK, FTS, and integrity gates.")
    validate.add_argument("--fast", action="store_true", help="Skip full integrity/FTS checks.")

    sub.add_parser("doctor", help="Inspect validation, lock, WAL companions, and runtime support.")
    sub.add_parser("migrate", help="Apply the reviewed production migration to an eligible v2 database.")

    backup = sub.add_parser("backup", help="Create and validate an online SQLite backup.")
    backup.add_argument("--output", type=Path)

    checkpoint = sub.add_parser("checkpoint", help="Checkpoint WAL for safe single-file transport.")
    checkpoint.add_argument("--passive", action="store_true")

    restore = sub.add_parser("restore", help="Restore a validated backup under exclusive coordination.")
    restore.add_argument("--input", type=Path, required=True)
    restore.add_argument("--confirm-replace", action="store_true")

    packet = sub.add_parser("packet", help="Dry-run or apply a versioned knowledge packet.")
    packet.add_argument("action", choices=("dry-run", "apply"))
    packet.add_argument("path", type=Path)

    search_parser = sub.add_parser("search", help="FTS discovery across items, claims, and questions.")
    search_parser.add_argument("text")
    search_parser.add_argument("--limit", type=int, default=25)

    dossier_parser = sub.add_parser("dossier", help="Return version-scoped claims/evidence for one item.")
    dossier_parser.add_argument("item_key")
    dossier_parser.add_argument("--version", required=True)

    impact_parser = sub.add_parser("impact", help="Return bounded direct/transitive impact paths.")
    impact_parser.add_argument("item_key")
    impact_parser.add_argument("--version", required=True)
    impact_parser.add_argument("--max-depth", type=int, default=3)
    impact_parser.add_argument("--limit", type=int, default=100)
    impact_parser.add_argument(
        "--relation-type",
        action="append",
        dest="relation_types",
        help="Restrict traversal to one relation type; repeat for multiple types.",
    )

    gaps_parser = sub.add_parser("gaps", help="Return open questions, revalidation, and analysis issues.")
    gaps_parser.add_argument("--version", required=True)
    gaps_parser.add_argument("--limit", type=int, default=100)

    sources = sub.add_parser("sources", help="Search the registered project/vanilla artifact catalog.")
    sources.add_argument("text", nargs="?", default="")
    sources.add_argument("--limit", type=int, default=100)

    sql = sub.add_parser("sql", help="Run one bounded read-only SELECT/WITH query.")
    sql.add_argument("statement")
    sql.add_argument("--limit", type=int, default=1000)
    return parser


def run(args: argparse.Namespace) -> Any:
    database = _database(args.database)
    command = args.command
    if command == "install":
        prepared = prepare_catalog()
        return build_atomic_database(
            database,
            lambda path, run_kind: populate_database(path, run_kind=run_kind, prepared=prepared),
        )
    if command == "refresh":
        prepared = prepare_catalog()
        with exclusive_writer_lock(
            "refresh catalog and knowledge ingestion", writer_lock_path(database)
        ):
            if catalog_is_current(database, prepared):
                validation = _require_valid(
                    validate_database(database, full=True), "refresh no-op"
                )
                return {
                    "result": "no_op",
                    "target_version": TARGET_VERSION,
                    "backup": None,
                    "counts": {"already_current": 1},
                    "validation": validation,
                }
            backup = online_backup(database)
            counts = populate_database(
                database,
                run_kind="refresh",
                prepared=prepared,
                lock_held=True,
            )
            validation = _require_valid(
                validate_database(database, full=True), "refresh"
            )
        return {
            "result": "refreshed",
            "target_version": TARGET_VERSION,
            "backup": backup,
            "counts": counts,
            "validation": validation,
        }
    if command == "status":
        return status(database)
    if command == "validate":
        if args.fast:
            return validate_database(database, full=False)
        with exclusive_writer_lock("full database validation", writer_lock_path(database)):
            return validate_database(database, full=True)
    if command == "doctor":
        writer_state = lock_status(writer_lock_path(database))
        validation = (
            validate_database(
                database,
                full=True,
                fts_integrity=not bool(writer_state.get("active")),
            )
            if database.exists()
            else None
        )
        with contextlib.closing(sqlite3.connect(":memory:")) as memory:
            fts5_enabled = bool(
                memory.execute("SELECT sqlite_compileoption_used('ENABLE_FTS5')").fetchone()[0]
            )
        return {
            "sqlite_version": sqlite3.sqlite_version,
            "sqlite_minimum_met": tuple(map(int, sqlite3.sqlite_version.split("."))) >= (3, 37, 0),
            "fts5_enabled": fts5_enabled,
            "database": str(database),
            "database_exists": database.exists(),
            "writer_lock": writer_state,
            "maintenance_access": maintenance_status(database),
            "wal_exists": Path(str(database) + "-wal").exists(),
            "shm_exists": Path(str(database) + "-shm").exists(),
            "validation": validation,
        }
    if command == "migrate":
        with exclusive_writer_lock("schema migration", writer_lock_path(database)):
            application_id, source_version = _raw_database_identity(database)
            if application_id != APPLICATION_ID:
                raise KnowledgeBaseError(
                    f"Wrong application_id={application_id}; expected {APPLICATION_ID}."
                )
            if source_version == USER_VERSION:
                return {
                    "migration": {"result": "no_op", "user_version": source_version},
                    "validation": _require_valid(
                        validate_database(database, full=True), "migration no-op"
                    ),
                }
            backup = online_backup(
                database,
                expected_user_version=source_version,
            )
            result = migrate_database(database)
            validation = _require_valid(
                validate_database(database, full=True), "migration"
            )
        return {"backup": backup, "migration": result, "validation": validation}
    if command == "backup":
        return online_backup(database, args.output)
    if command == "checkpoint":
        with exclusive_writer_lock("WAL checkpoint", writer_lock_path(database)):
            result = checkpoint_database(database, truncate=not args.passive)
        return {"database": str(database), "checkpoint": result}
    if command == "restore":
        return _restore(database, args.input, args.confirm_replace)
    if command == "packet":
        if args.action == "dry-run":
            return dry_run_packet(database, args.path)
        preview = dry_run_packet(database, args.path)
        if preview["already_applied"]:
            return {**preview, "result": "no_op"}
        with exclusive_writer_lock(
            f"apply knowledge packet {preview['packet_key']}",
            writer_lock_path(database),
        ):
            prepared_packet = prepare_packet(args.path)
            locked_preview = dry_run_packet(
                database,
                args.path,
                prepared=prepared_packet,
            )
            if locked_preview["already_applied"]:
                return {**locked_preview, "result": "no_op"}
            backup = online_backup(database)
            application = apply_packet(
                database,
                args.path,
                lock_held=True,
                prepared=prepared_packet,
            )
            validation = _require_valid(
                validate_database(database, full=True), "knowledge packet"
            )
        return {"backup": backup, "application": application, "validation": validation}
    if command == "search":
        return {"query": args.text, "results": search(database, args.text, args.limit)}
    if command == "dossier":
        return dossier(database, args.item_key, args.version)
    if command == "impact":
        return {
            "target_version": args.version,
            "source_item": args.item_key,
            "max_depth": args.max_depth,
            "limit": args.limit,
            "relation_types": args.relation_types,
            "results": impact(
                database,
                args.item_key,
                args.version,
                args.max_depth,
                args.limit,
                args.relation_types,
            ),
        }
    if command == "gaps":
        return gaps(database, args.version, args.limit)
    if command == "sources":
        return {"query": args.text, "results": catalog_sources(database, args.text, args.limit)}
    if command == "sql":
        return {"results": read_only_sql(database, args.statement, args.limit)}
    raise KnowledgeBaseError(f"Unknown command: {command}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        _print(run(args))
        return 0
    except (KnowledgeBaseError, OSError, sqlite3.Error, ValueError, json.JSONDecodeError) as exc:
        _print({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
        return 2


if __name__ == "__main__":
    sys.exit(main())
