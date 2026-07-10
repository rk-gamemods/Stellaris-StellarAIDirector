from __future__ import annotations

import contextlib
import hashlib
import json
import mimetypes
import os
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from .db import (
    SEMANTIC_CHECKS,
    KnowledgeBaseError,
    connect_writer,
    exclusive_writer_lock,
    sha256_file,
    utc_now,
    writer_lock_path,
)
from .paths import REPO_ROOT, TARGET_VERSION, jdatamunch_manifest, stellaris_install_root
from .structured import DatasetProfile, SUPPORTED_SUFFIXES, profile_structured_file, semantic_role


VANILLA_TEXT_SUFFIXES = {
    ".txt",
    ".csv",
    ".json",
    ".jsonl",
    ".ndjson",
    ".yml",
    ".yaml",
    ".gui",
    ".gfx",
    ".asset",
    ".shader",
}
VANILLA_DIRECTORIES = (
    "common",
    "events",
    "interface",
    "localisation",
    "localisation_synced",
    "map",
    "prescripted_countries",
)


@dataclass(frozen=True)
class GitState:
    head: str
    branch: str
    status_text: str
    status_hash: str
    worktree_state: str


@dataclass(frozen=True)
class Baseline:
    display_version: str
    raw_version: str
    checksum_or_build: str | None
    steam_build_id: str | None


@dataclass
class InventoryFile:
    corpus_code: str
    root: Path
    path: Path
    relative_path: str
    source_system_key: str
    source_root_key: str
    artifact_kind: str
    file_role: str
    sha256: str
    size_bytes: int
    modified_at: str
    mtime_ns: int
    profile: DatasetProfile | None = None
    profile_error: str | None = None


@dataclass
class PreparedCatalog:
    git: GitState
    baseline: Baseline
    files: list[InventoryFile]
    manifest_rows: list[dict[str, object]]
    object_atlas_rows: list[dict[str, str]] = field(default_factory=list)
    dependency_rows: list[dict[str, str]] = field(default_factory=list)


def _run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def git_state() -> GitState:
    head = _run_git("rev-parse", "HEAD").strip()
    branch = _run_git("branch", "--show-current").strip() or "detached"
    status = _run_git("status", "--porcelain=v1", "--untracked-files=all")
    return GitState(
        head=head,
        branch=branch,
        status_text=status,
        status_hash=hashlib.sha256(status.encode("utf-8")).hexdigest(),
        worktree_state="dirty" if status else "clean",
    )


def _repo_paths() -> list[Path]:
    raw = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "-co", "--exclude-standard", "-z"],
        check=True,
        capture_output=True,
    ).stdout
    paths: list[Path] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        relative = item.decode("utf-8", errors="surrogateescape")
        path = REPO_ROOT / relative
        if path.is_file():
            paths.append(path)
    return sorted(set(paths), key=lambda value: value.as_posix().lower())


def _vanilla_paths(root: Path) -> list[Path]:
    paths: set[Path] = set()
    for name in ("launcher-settings.json", "checksum_manifest.txt"):
        candidate = root / name
        if candidate.is_file():
            paths.add(candidate)
    for directory in VANILLA_DIRECTORIES:
        base = root / directory
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in VANILLA_TEXT_SUFFIXES:
                paths.add(path)
    return sorted(paths, key=lambda value: value.as_posix().lower())


def _classify(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv", ".jsonl", ".ndjson"}:
        return "dataset", "structured_data"
    if suffix == ".json":
        return "structured_document", "structured_data"
    if suffix in {".py", ".ps1", ".sql"}:
        return "source_code", "automation_or_schema"
    if suffix in {".md", ".rst"}:
        return "documentation", "documentation"
    if suffix in {".txt", ".yml", ".yaml", ".gui", ".gfx", ".asset", ".shader"}:
        return "script_or_config", "stellaris_or_configuration"
    if suffix in {".png", ".jpg", ".jpeg", ".dds", ".tga", ".gif", ".svg"}:
        return "image", "asset"
    return "file", "other"


def _inventory_file(
    *,
    corpus_code: str,
    root: Path,
    path: Path,
    source_system_key: str,
    source_root_key: str,
) -> InventoryFile:
    stat = path.stat()
    artifact_kind, file_role = _classify(path)
    relative = path.relative_to(root).as_posix()
    modified_at = datetime.fromtimestamp(stat.st_mtime, UTC).isoformat().replace("+00:00", "Z")
    record = InventoryFile(
        corpus_code=corpus_code,
        root=root,
        path=path,
        relative_path=relative,
        source_system_key=source_system_key,
        source_root_key=source_root_key,
        artifact_kind=artifact_kind,
        file_role=file_role,
        sha256=sha256_file(path),
        size_bytes=stat.st_size,
        modified_at=modified_at,
        mtime_ns=stat.st_mtime_ns,
    )
    if path.suffix.lower() in SUPPORTED_SUFFIXES:
        try:
            record.profile = profile_structured_file(path)
        except Exception as exc:  # every failure is preserved as an ingest issue
            record.profile_error = f"{type(exc).__name__}: {exc}"
    return record


def _read_baseline(root: Path) -> Baseline:
    launcher = root / "launcher-settings.json"
    if not launcher.is_file():
        raise KnowledgeBaseError(f"Missing Stellaris launcher settings: {launcher}")
    payload = json.loads(launcher.read_text(encoding="utf-8-sig"))
    raw_version = str(payload.get("rawVersion", ""))
    display_version = str(payload.get("version", ""))
    if raw_version.lstrip("v") != TARGET_VERSION:
        raise KnowledgeBaseError(
            f"Local Stellaris install is {raw_version or '<unknown>'}; expected v{TARGET_VERSION}."
        )
    checksum = None
    if "(" in display_version and display_version.endswith(")"):
        checksum = display_version.rsplit("(", 1)[1][:-1]
    manifest = root.parent.parent / "appmanifest_281990.acf"
    steam_build_id = None
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8", errors="replace").splitlines():
            if '"buildid"' in line:
                parts = line.replace('"', " ").split()
                if parts:
                    steam_build_id = parts[-1]
                    break
    return Baseline(
        display_version=display_version,
        raw_version=raw_version,
        checksum_or_build=checksum,
        steam_build_id=steam_build_id,
    )


def _read_csv_dicts(path: Path) -> list[dict[str, str]]:
    import csv

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def prepare_catalog() -> PreparedCatalog:
    install_root = stellaris_install_root()
    current_git = git_state()
    baseline = _read_baseline(install_root)
    repo_root_key = f"repo:{current_git.head[:12]}:{current_git.status_hash[:12]}"
    vanilla_root_key = f"vanilla:{TARGET_VERSION}:{baseline.checksum_or_build or 'unknown'}"
    files = [
        _inventory_file(
            corpus_code="repo",
            root=REPO_ROOT,
            path=path,
            source_system_key="stellar-ai-repository",
            source_root_key=repo_root_key,
        )
        for path in _repo_paths()
    ]
    files.extend(
        _inventory_file(
            corpus_code=f"vanilla-{TARGET_VERSION}",
            root=install_root,
            path=path,
            source_system_key=f"vanilla-{TARGET_VERSION}",
            source_root_key=vanilla_root_key,
        )
        for path in _vanilla_paths(install_root)
    )
    manifest_rows: list[dict[str, object]] = []
    manifest_path = jdatamunch_manifest()
    if manifest_path.is_file():
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_rows = list(payload.get("datasets", []))
    by_repo_path = {record.relative_path: record.path for record in files if record.corpus_code == "repo"}
    object_path = by_repo_path.get("research/stellar-ai/object-atlas/object-atlas-2026-07-06.csv")
    dependency_path = by_repo_path.get("research/stellar-ai/object-atlas/dependency-edges-2026-07-06.csv")
    object_rows = _read_csv_dicts(object_path) if object_path else []
    dependency_rows = _read_csv_dicts(dependency_path) if dependency_path else []
    return PreparedCatalog(
        git=current_git,
        baseline=baseline,
        files=files,
        manifest_rows=manifest_rows,
        object_atlas_rows=object_rows,
        dependency_rows=dependency_rows,
    )


def _assert_inputs_stable(prepared: PreparedCatalog) -> None:
    current_git = git_state()
    if current_git != prepared.git:
        raise KnowledgeBaseError("Repository state changed during catalog preparation; rerun refresh.")
    for record in prepared.files:
        stat = record.path.stat()
        if stat.st_size != record.size_bytes or stat.st_mtime_ns != record.mtime_ns:
            raise KnowledgeBaseError(f"Input changed during catalog preparation: {record.path}")
        if sha256_file(record.path) != record.sha256:
            raise KnowledgeBaseError(f"Input fingerprint changed during catalog preparation: {record.path}")


def prepared_input_fingerprint(prepared: PreparedCatalog) -> str:
    payload = {
        "adapter": "stellaris-kb-catalog-v1",
        "target_version": TARGET_VERSION,
        "git": {
            "head": prepared.git.head,
            "branch": prepared.git.branch,
            "status_sha256": prepared.git.status_hash,
        },
        "baseline": {
            "display_version": prepared.baseline.display_version,
            "raw_version": prepared.baseline.raw_version,
            "checksum_or_build": prepared.baseline.checksum_or_build,
            "steam_build_id": prepared.baseline.steam_build_id,
        },
        "files": [
            (record.corpus_code, record.relative_path, record.sha256, record.size_bytes)
            for record in sorted(
                prepared.files, key=lambda row: (row.corpus_code, row.relative_path)
            )
        ],
        "manifest": sorted(
            (
                str(row.get("dataset", "")),
                str(row.get("fingerprint", "")),
                int(row.get("rows", 0) or 0),
                int(row.get("columns", 0) or 0),
            )
            for row in prepared.manifest_rows
        ),
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def catalog_is_current(path: Path, prepared: PreparedCatalog) -> bool:
    from .db import connect_read_only

    _assert_inputs_stable(prepared)
    run_key = f"catalog:v1:{prepared_input_fingerprint(prepared)}"
    with contextlib.closing(connect_read_only(path)) as connection:
        return (
            connection.execute(
                "SELECT 1 FROM kb_ingest_run WHERE run_key=? AND state='committed'",
                (run_key,),
            ).fetchone()
            is not None
        )


def _id(connection, table: str, key_column: str, value: str, id_column: str | None = None) -> int:
    id_column = id_column or f"{table}_id"
    row = connection.execute(
        f"SELECT {id_column} FROM {table} WHERE {key_column}=?", (value,)
    ).fetchone()
    if row is None:
        raise KnowledgeBaseError(f"Missing {table}.{key_column}={value}")
    return int(row[0])


def _ensure_source_system(
    connection,
    *,
    key: str,
    name: str,
    evidence_type: str,
    root: Path,
    authority: str,
    change_set_id: int,
) -> int:
    evidence_type_id = _id(connection, "evidence_source_type", "type_code", evidence_type)
    connection.execute(
        """
        INSERT INTO source_system(
            system_key,system_name,evidence_source_type_id,canonical_root,access_mode,
            authoritative_for,default_tool_item_id,retrieval_instructions,is_local_only,notes,
            created_in_change_set_id
        ) VALUES (?,?,?,?,?,?,NULL,?,1,NULL,?)
        ON CONFLICT(system_key) DO UPDATE SET
            system_name=excluded.system_name,
            canonical_root=excluded.canonical_root,
            authoritative_for=excluded.authoritative_for,
            retrieval_instructions=excluded.retrieval_instructions
        """,
        (
            key,
            name,
            evidence_type_id,
            str(root),
            "filesystem/index",
            authority,
            "Use the catalog hash and exact relative path; route content reads through JDocMunch, JCodeMunch, or JDataMunch by artifact type.",
            change_set_id,
        ),
    )
    return _id(connection, "source_system", "system_key", key)


def _ensure_file_item(connection, record: InventoryFile, change_set_id: int, actor_id: int) -> int:
    item_type_id = _id(connection, "item_type", "type_code", "file")
    lifecycle_state_id = _id(connection, "lifecycle_state", "state_code", "active")
    canonical_key = f"file:{record.corpus_code}:{record.relative_path}"
    connection.execute(
        """
        INSERT INTO knowledge_item(
            item_type_id,canonical_key,display_name,summary,lifecycle_state_id,
            created_by_actor_id,created_in_change_set_id
        ) VALUES (?,?,?,?,?,?,?)
        ON CONFLICT(canonical_key) DO UPDATE SET
            display_name=excluded.display_name,
            summary=excluded.summary,
            lifecycle_state_id=excluded.lifecycle_state_id,
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now'),
            updated_in_change_set_id=excluded.created_in_change_set_id
        """,
        (
            item_type_id,
            canonical_key,
            record.path.name,
            f"{record.file_role} file in {record.corpus_code}: {record.relative_path}",
            lifecycle_state_id,
            actor_id,
            change_set_id,
        ),
    )
    item_id = _id(connection, "knowledge_item", "canonical_key", canonical_key, "item_id")
    connection.execute(
        """
        INSERT INTO file_asset(item_id,corpus_code,relative_path,file_role,load_order_note)
        VALUES (?,?,?,?,NULL)
        ON CONFLICT(corpus_code,relative_path) DO UPDATE SET file_role=excluded.file_role
        """,
        (item_id, record.corpus_code, record.relative_path, record.file_role),
    )
    return item_id


def _register_dataset_schema(
    connection,
    *,
    record: InventoryFile,
    source_artifact_id: int,
    change_set_id: int,
) -> int | None:
    profile = record.profile
    if profile is None:
        return None
    schema_key = f"catalog:{record.corpus_code}:{record.relative_path}"
    schema_version = record.sha256[:16]
    existing = connection.execute(
        """
        SELECT dataset_schema_id FROM dataset_schema
        WHERE source_artifact_id=? AND schema_key=? AND schema_version=?
        """,
        (source_artifact_id, schema_key, schema_version),
    ).fetchone()
    if existing:
        return int(existing[0])
    stable_description = (
        ", ".join(profile.stable_key_columns)
        if profile.stable_key_columns
        else "No inferred unique key; use row-number locators."
    )
    cursor = connection.execute(
        """
        INSERT INTO dataset_schema(
            source_artifact_id,schema_key,schema_version,format_code,delimiter,has_header,
            row_count,column_count,schema_hash_algorithm,schema_hash_value,
            generated_by_tool_item_id,is_authoritative_external,storage_policy,
            stable_key_description,notes,created_in_change_set_id
        ) VALUES (?,?,?,?,?,?,?,?,?,?,NULL,1,'locator_only',?,?,?)
        """,
        (
            source_artifact_id,
            schema_key,
            schema_version,
            profile.format_code,
            profile.delimiter,
            int(profile.has_header),
            profile.row_count,
            len(profile.columns),
            "sha256",
            profile.schema_hash,
            stable_description,
            " ".join(profile.notes),
            change_set_id,
        ),
    )
    dataset_schema_id = int(cursor.lastrowid)
    column_ids: dict[str, int] = {}
    for ordinal, column in enumerate(profile.columns, start=1):
        cursor = connection.execute(
            """
            INSERT INTO dataset_column(
                dataset_schema_id,ordinal,column_name,logical_type,semantic_role,
                dimension_group,metric_key,unit,is_nullable,mapped_item_type_id,
                mapped_field_item_id,description
            ) VALUES (?,?,?,?,?,NULL,NULL,NULL,?,NULL,NULL,?)
            """,
            (
                dataset_schema_id,
                ordinal,
                column.name,
                column.logical_type,
                semantic_role(column.name, column.logical_type),
                int(column.nullable),
                f"Observed column {column.name} from {record.relative_path}.",
            ),
        )
        column_ids[column.name] = int(cursor.lastrowid)
    for key_ordinal, name in enumerate(profile.stable_key_columns, start=1):
        connection.execute(
            """
            INSERT INTO dataset_key_column(
                dataset_schema_id,dataset_column_id,key_ordinal,normalization_rule,
                is_stable_across_versions
            ) VALUES (?,?,?,'trimmed exact text',0)
            """,
            (dataset_schema_id, column_ids[name], key_ordinal),
        )
    return dataset_schema_id


def _register_file(
    connection,
    *,
    record: InventoryFile,
    source_system_id: int,
    source_root_id: int,
    repository_snapshot_id: int | None,
    ingest_run_id: int,
    change_set_id: int,
    actor_id: int,
    observed_at: str,
) -> tuple[int, int | None, bool]:
    item_id = _ensure_file_item(connection, record, change_set_id, actor_id)
    stable_key = f"catalog:{record.corpus_code}:{record.relative_path}:sha256:{record.sha256}"
    existing = connection.execute(
        "SELECT source_artifact_id FROM source_artifact WHERE source_system_id=? AND stable_key=?",
        (source_system_id, stable_key),
    ).fetchone()
    changed = existing is None
    if existing:
        source_artifact_id = int(existing[0])
    else:
        cursor = connection.execute(
            """
            INSERT INTO source_artifact(
                source_system_id,source_root_id,repository_snapshot_id,mod_release_id,
                stable_key,artifact_kind,title,uri_or_path,repository_relative_path,
                game_version_id,repository_commit,tool_version,content_hash_algorithm,
                content_hash_value,file_size_bytes,mime_type,modified_at,captured_at,
                observed_at,availability_status,notes,created_in_change_set_id
            ) VALUES (?,?,?,NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                source_system_id,
                source_root_id,
                repository_snapshot_id,
                stable_key,
                record.artifact_kind,
                record.path.name,
                str(record.path),
                record.relative_path,
                _id(connection, "game_version", "version_label", TARGET_VERSION)
                if record.corpus_code.startswith("vanilla-")
                else None,
                repository_snapshot_id and connection.execute(
                    "SELECT commit_sha FROM repository_snapshot WHERE repository_snapshot_id=?",
                    (repository_snapshot_id,),
                ).fetchone()[0],
                None,
                "sha256",
                record.sha256,
                record.size_bytes,
                mimetypes.guess_type(record.path.name)[0],
                record.modified_at,
                observed_at,
                observed_at,
                "available",
                "Immutable content-addressed catalog revision.",
                change_set_id,
            ),
        )
        source_artifact_id = int(cursor.lastrowid)
    entry = connection.execute(
        """
        SELECT catalog_entry_id,current_hash_value FROM kb_catalog_entry
        WHERE source_system_id=? AND corpus_code=? AND relative_path=?
        """,
        (source_system_id, record.corpus_code, record.relative_path),
    ).fetchone()
    if entry:
        catalog_entry_id = int(entry[0])
        changed = changed or entry[1] != record.sha256
        connection.execute(
            """
            UPDATE kb_catalog_entry SET
                artifact_kind=?,file_role=?,current_source_artifact_id=?,item_id=?,
                current_hash_algorithm='sha256',current_hash_value=?,current_size_bytes=?,
                current_modified_at=?,availability_status='available',last_seen_at=?,
                updated_in_change_set_id=?
            WHERE catalog_entry_id=?
            """,
            (
                record.artifact_kind,
                record.file_role,
                source_artifact_id,
                item_id,
                record.sha256,
                record.size_bytes,
                record.modified_at,
                observed_at,
                change_set_id,
                catalog_entry_id,
            ),
        )
    else:
        cursor = connection.execute(
            """
            INSERT INTO kb_catalog_entry(
                source_system_id,corpus_code,relative_path,artifact_kind,file_role,
                current_source_artifact_id,item_id,current_hash_algorithm,current_hash_value,
                current_size_bytes,current_modified_at,availability_status,first_seen_at,
                last_seen_at,created_in_change_set_id,updated_in_change_set_id
            ) VALUES (?,?,?,?,?,?,?,'sha256',?,?,?,'available',?,?,?,NULL)
            """,
            (
                source_system_id,
                record.corpus_code,
                record.relative_path,
                record.artifact_kind,
                record.file_role,
                source_artifact_id,
                item_id,
                record.sha256,
                record.size_bytes,
                record.modified_at,
                observed_at,
                observed_at,
                change_set_id,
            ),
        )
        catalog_entry_id = int(cursor.lastrowid)
        changed = True
    connection.execute(
        """
        INSERT INTO kb_catalog_observation(
            ingest_run_id,catalog_entry_id,source_artifact_id,repository_snapshot_id,
            is_present,content_hash_algorithm,content_hash_value,file_size_bytes,
            modified_at,observed_at
        ) VALUES (?,?,?,?,1,'sha256',?,?,?,?)
        """,
        (
            ingest_run_id,
            catalog_entry_id,
            source_artifact_id,
            repository_snapshot_id,
            record.sha256,
            record.size_bytes,
            record.modified_at,
            observed_at,
        ),
    )
    locator_type_id = _id(connection, "locator_type", "type_code", "file_hash")
    connection.execute(
        """
        INSERT INTO evidence_locator(
            source_artifact_id,dataset_schema_id,locator_type_id,stable_locator_key,label,
            relative_path,evidence_summary,retrieval_instructions,created_by_actor_id,
            created_in_change_set_id
        ) VALUES (?,NULL,?,'whole-file',?,?,?,?,?,?)
        ON CONFLICT(source_artifact_id,stable_locator_key) DO NOTHING
        """,
        (
            source_artifact_id,
            locator_type_id,
            f"{record.corpus_code}:{record.relative_path}",
            record.relative_path,
            f"SHA-256 {record.sha256}; {record.size_bytes} bytes.",
            "Retrieve the exact content-addressed file revision through its registered source system and verify SHA-256 before use.",
            actor_id,
            change_set_id,
        ),
    )
    dataset_schema_id = _register_dataset_schema(
        connection,
        record=record,
        source_artifact_id=source_artifact_id,
        change_set_id=change_set_id,
    )
    return source_artifact_id, dataset_schema_id, changed


def _mark_missing(
    connection,
    *,
    corpus_code: str,
    source_system_id: int,
    ingest_run_id: int,
    change_set_id: int,
    observed_at: str,
) -> None:
    rows = connection.execute(
        """
        SELECT ce.catalog_entry_id,ce.current_source_artifact_id
        FROM kb_catalog_entry ce
        WHERE ce.source_system_id=? AND ce.corpus_code=? AND ce.availability_status='available'
          AND NOT EXISTS (
              SELECT 1 FROM kb_catalog_observation o
              WHERE o.ingest_run_id=? AND o.catalog_entry_id=ce.catalog_entry_id
          )
        """,
        (source_system_id, corpus_code, ingest_run_id),
    ).fetchall()
    for row in rows:
        connection.execute(
            """
            UPDATE kb_catalog_entry SET availability_status='missing',last_seen_at=?,
                updated_in_change_set_id=? WHERE catalog_entry_id=?
            """,
            (observed_at, change_set_id, row[0]),
        )
        connection.execute(
            """
            INSERT INTO kb_catalog_observation(
                ingest_run_id,catalog_entry_id,source_artifact_id,repository_snapshot_id,
                is_present,observed_at
            ) VALUES (?,?,?,NULL,0,?)
            """,
            (ingest_run_id, row[0], row[1], observed_at),
        )


def _register_manifest(
    connection,
    *,
    rows: Iterable[dict[str, object]],
    change_set_id: int,
    observed_at: str,
) -> None:
    seen: set[str] = set()
    for row in rows:
        handle = str(row.get("dataset", "")).strip()
        if not handle:
            continue
        seen.add(handle)
        file_name = str(row.get("file", "") or "")
        fingerprint = str(row.get("fingerprint", "") or "")
        match = None
        if fingerprint.startswith("sha256:"):
            match = connection.execute(
                """
                SELECT ce.current_source_artifact_id,ds.dataset_schema_id
                FROM kb_catalog_entry ce
                LEFT JOIN dataset_schema ds ON ds.source_artifact_id=ce.current_source_artifact_id
                WHERE ce.current_hash_value=? AND ce.availability_status='available'
                ORDER BY CASE WHEN substr(ce.relative_path, -length(?))=? THEN 0 ELSE 1 END,
                         ds.dataset_schema_id DESC LIMIT 1
                """,
                (fingerprint.split(":", 1)[1], file_name, file_name),
            ).fetchone()
        artifact_id = int(match[0]) if match and match[0] is not None else None
        schema_id = int(match[1]) if match and match[1] is not None else None
        existing = connection.execute(
            """
            SELECT external_dataset_handle_id FROM kb_external_dataset_handle
            WHERE provider_code='jdatamunch' AND dataset_handle=?
            """,
            (handle,),
        ).fetchone()
        values = (
            schema_id,
            artifact_id,
            file_name or None,
            fingerprint or None,
            row.get("rows"),
            row.get("columns"),
            row.get("indexed_at"),
            observed_at,
            change_set_id,
        )
        if existing:
            connection.execute(
                """
                UPDATE kb_external_dataset_handle SET
                    dataset_schema_id=?,source_artifact_id=?,source_file_name=?,fingerprint=?,
                    row_count=?,column_count=?,indexed_at=?,last_seen_at=?,is_current=1,
                    updated_in_change_set_id=?
                WHERE external_dataset_handle_id=?
                """,
                (*values, existing[0]),
            )
        else:
            connection.execute(
                """
                INSERT INTO kb_external_dataset_handle(
                    provider_code,dataset_handle,dataset_schema_id,source_artifact_id,
                    source_file_name,fingerprint,row_count,column_count,indexed_at,
                    first_seen_at,last_seen_at,is_current,created_in_change_set_id,
                    updated_in_change_set_id
                ) VALUES ('jdatamunch',?,?,?,?,?,?,?,?,?,?,1,?,NULL)
                """,
                (
                    handle,
                    schema_id,
                    artifact_id,
                    file_name or None,
                    fingerprint or None,
                    row.get("rows"),
                    row.get("columns"),
                    row.get("indexed_at"),
                    observed_at,
                    observed_at,
                    change_set_id,
                ),
            )
    if seen:
        placeholders = ",".join("?" for _ in seen)
        connection.execute(
            f"""
            UPDATE kb_external_dataset_handle SET is_current=0,updated_in_change_set_id=?
            WHERE provider_code='jdatamunch' AND dataset_handle NOT IN ({placeholders})
            """,
            (change_set_id, *sorted(seen)),
        )


def populate_database(
    path: Path,
    *,
    run_kind: str = "refresh",
    prepared: PreparedCatalog | None = None,
    lock_held: bool = False,
) -> dict[str, int]:
    prepared = prepared or prepare_catalog()
    _assert_inputs_stable(prepared)
    observed_at = utc_now()
    input_fingerprint = prepared_input_fingerprint(prepared)
    run_key = f"catalog:v1:{input_fingerprint}"
    counts = {
        "files_seen": len(prepared.files),
        "files_changed": 0,
        "structured_files_profiled": sum(record.profile is not None for record in prepared.files),
        "object_rows_loaded": 0,
        "relation_rows_loaded": 0,
        "issue_count": sum(record.profile_error is not None for record in prepared.files),
        "already_current": 0,
    }
    lock = (
        contextlib.nullcontext()
        if lock_held
        else exclusive_writer_lock(
            f"{run_kind} catalog and knowledge ingestion", writer_lock_path(path)
        )
    )
    with lock:
        _assert_inputs_stable(prepared)
        connection = connect_writer(path)
        try:
            connection.execute("BEGIN IMMEDIATE")
            if connection.execute(
                "SELECT 1 FROM kb_ingest_run WHERE run_key=? AND state='committed'",
                (run_key,),
            ).fetchone():
                connection.rollback()
                counts["already_current"] = 1
                return counts
            actor_id = _id(connection, "actor", "actor_key", "tool:stellaris-kb", "actor_id")
            target_version_id = _id(connection, "game_version", "version_label", TARGET_VERSION)
            change_set_key = f"change:{run_key}"
            cursor = connection.execute(
                """
                INSERT INTO change_set(
                    change_set_key,title,purpose,actor_id,state,opened_at,repository_commit,
                    transaction_note
                ) VALUES (?,?,?,?,'open',?,?,?)
                """,
                (
                    change_set_key,
                    f"{run_kind.title()} project and 4.4.4 catalog",
                    "Register exact file revisions, external dataset schemas, and selected durable graph facts.",
                    actor_id,
                    observed_at,
                    prepared.git.head,
                    "All source discovery and profiling completed before the serialized writer transaction.",
                ),
            )
            change_set_id = int(cursor.lastrowid)
            snapshot_key = f"repo:{prepared.git.head}:{prepared.git.status_hash}:{observed_at}"
            cursor = connection.execute(
                """
                INSERT INTO repository_snapshot(
                    snapshot_key,repository_name,repository_root,branch_name,commit_sha,
                    worktree_state,captured_at,notes,created_in_change_set_id
                ) VALUES (?,?,?,?,?,?,?,?,?)
                """,
                (
                    snapshot_key,
                    "StellarisMods",
                    str(REPO_ROOT),
                    prepared.git.branch,
                    prepared.git.head,
                    prepared.git.worktree_state,
                    observed_at,
                    f"Porcelain status SHA-256 {prepared.git.status_hash}.",
                    change_set_id,
                ),
            )
            repository_snapshot_id = int(cursor.lastrowid)
            cursor = connection.execute(
                """
                INSERT INTO kb_ingest_run(
                    run_key,run_kind,target_version_id,repository_snapshot_id,change_set_id,
                    state,started_at,input_summary
                ) VALUES (?,?,?,?,?,'running',?,?)
                """,
                (
                    run_key,
                    run_kind,
                    target_version_id,
                    repository_snapshot_id,
                    change_set_id,
                    observed_at,
                    f"repo_files={sum(r.corpus_code=='repo' for r in prepared.files)}; "
                    f"vanilla_files={sum(r.corpus_code.startswith('vanilla-') for r in prepared.files)}; "
                    f"git_status_sha256={prepared.git.status_hash}; "
                    f"input_fingerprint={input_fingerprint}",
                ),
            )
            ingest_run_id = int(cursor.lastrowid)
            repo_system_id = _ensure_source_system(
                connection,
                key="stellar-ai-repository",
                name="StellarisMods repository",
                evidence_type="repository",
                root=REPO_ROOT,
                authority="Current repository files and deterministic tools for the captured snapshot.",
                change_set_id=change_set_id,
            )
            vanilla_root = stellaris_install_root()
            vanilla_system_id = _ensure_source_system(
                connection,
                key=f"vanilla-{TARGET_VERSION}",
                name=f"Local vanilla Stellaris {TARGET_VERSION}",
                evidence_type="vanilla_files",
                root=vanilla_root,
                authority=f"Exact local {TARGET_VERSION} scripted definitions.",
                change_set_id=change_set_id,
            )
            root_ids: dict[str, int] = {}
            for key, kind, canonical, system_id, repo_snapshot in (
                (
                    next(r.source_root_key for r in prepared.files if r.corpus_code == "repo"),
                    "repository",
                    REPO_ROOT,
                    repo_system_id,
                    repository_snapshot_id,
                ),
                (
                    next(r.source_root_key for r in prepared.files if r.corpus_code.startswith("vanilla-")),
                    "vanilla_install",
                    vanilla_root,
                    vanilla_system_id,
                    None,
                ),
            ):
                connection.execute(
                    """
                    INSERT INTO source_root(
                        root_key,root_kind,canonical_path,repository_snapshot_id,mod_release_id,
                        game_version_id,captured_at,availability_status,authoritative_for,notes,
                        created_in_change_set_id
                    ) VALUES (?,?,?,?,NULL,?,?,'available',?,?,?)
                    ON CONFLICT(root_key) DO UPDATE SET
                        availability_status='available',captured_at=excluded.captured_at
                    """,
                    (
                        key,
                        kind,
                        str(canonical),
                        repo_snapshot,
                        target_version_id if kind == "vanilla_install" else None,
                        observed_at,
                        "Captured repository source." if kind == "repository" else f"Exact local {TARGET_VERSION} vanilla files.",
                        f"Source system id {system_id}.",
                        change_set_id,
                    ),
                )
                root_ids[key] = _id(connection, "source_root", "root_key", key)
            artifact_maps: dict[str, tuple[int, int | None]] = {}
            systems = {
                "stellar-ai-repository": repo_system_id,
                f"vanilla-{TARGET_VERSION}": vanilla_system_id,
            }
            for record in prepared.files:
                artifact_id, schema_id, changed = _register_file(
                    connection,
                    record=record,
                    source_system_id=systems[record.source_system_key],
                    source_root_id=root_ids[record.source_root_key],
                    repository_snapshot_id=repository_snapshot_id if record.corpus_code == "repo" else None,
                    ingest_run_id=ingest_run_id,
                    change_set_id=change_set_id,
                    actor_id=actor_id,
                    observed_at=observed_at,
                )
                artifact_maps[f"{record.corpus_code}:{record.relative_path}"] = (artifact_id, schema_id)
                counts["files_changed"] += int(changed)
                if record.profile_error:
                    connection.execute(
                        """
                        INSERT INTO kb_ingest_issue(
                            ingest_run_id,corpus_code,relative_path,stage_code,severity_code,
                            issue_code,message,status_code,created_at
                        ) VALUES (?,?,?,'schema_profile','warning','profile_failed',?,'open',?)
                        """,
                        (
                            ingest_run_id,
                            record.corpus_code,
                            record.relative_path,
                            record.profile_error,
                            observed_at,
                        ),
                    )
            _mark_missing(
                connection,
                corpus_code="repo",
                source_system_id=repo_system_id,
                ingest_run_id=ingest_run_id,
                change_set_id=change_set_id,
                observed_at=observed_at,
            )
            _mark_missing(
                connection,
                corpus_code=f"vanilla-{TARGET_VERSION}",
                source_system_id=vanilla_system_id,
                ingest_run_id=ingest_run_id,
                change_set_id=change_set_id,
                observed_at=observed_at,
            )
            _register_manifest(
                connection,
                rows=prepared.manifest_rows,
                change_set_id=change_set_id,
                observed_at=observed_at,
            )
            launcher_artifact_id = artifact_maps[f"vanilla-{TARGET_VERSION}:launcher-settings.json"][0]
            connection.execute("UPDATE kb_environment_baseline SET is_current=0,retired_in_change_set_id=? WHERE is_current=1", (change_set_id,))
            connection.execute(
                """
                INSERT INTO kb_environment_baseline(
                    baseline_key,game_version_id,source_root_id,launcher_artifact_id,
                    display_version,raw_version,checksum_or_build,steam_build_id,captured_at,
                    is_current,created_in_change_set_id
                ) VALUES (?,?,?,?,?,?,?,?,?,1,?)
                """,
                (
                    f"baseline:{TARGET_VERSION}:{prepared.baseline.checksum_or_build}:{observed_at}",
                    target_version_id,
                    root_ids[next(r.source_root_key for r in prepared.files if r.corpus_code.startswith('vanilla-'))],
                    launcher_artifact_id,
                    prepared.baseline.display_version,
                    prepared.baseline.raw_version,
                    prepared.baseline.checksum_or_build,
                    prepared.baseline.steam_build_id,
                    observed_at,
                    change_set_id,
                ),
            )
            from .atlas import ingest_dependency_edges, ingest_object_atlas

            atlas_key = "repo:research/stellar-ai/object-atlas/object-atlas-2026-07-06.csv"
            edges_key = "repo:research/stellar-ai/object-atlas/dependency-edges-2026-07-06.csv"
            if atlas_key in artifact_maps and artifact_maps[atlas_key][1] is not None:
                counts["object_rows_loaded"] = ingest_object_atlas(
                    connection,
                    rows=prepared.object_atlas_rows,
                    source_artifact_id=artifact_maps[atlas_key][0],
                    dataset_schema_id=int(artifact_maps[atlas_key][1]),
                    version_span_code="v4.4.4",
                    change_set_id=change_set_id,
                    actor_id=actor_id,
                    repository_snapshot_id=repository_snapshot_id,
                    observed_at=observed_at,
                )
            if edges_key in artifact_maps and artifact_maps[edges_key][1] is not None:
                counts["relation_rows_loaded"] = ingest_dependency_edges(
                    connection,
                    rows=prepared.dependency_rows,
                    source_artifact_id=artifact_maps[edges_key][0],
                    dataset_schema_id=int(artifact_maps[edges_key][1]),
                    version_span_code="v4.4.4",
                    change_set_id=change_set_id,
                    actor_id=actor_id,
                )
            completed_at = utc_now()
            connection.execute(
                """
                UPDATE kb_ingest_run SET state='committed',completed_at=?,files_seen=?,
                    files_changed=?,structured_files_profiled=?,object_rows_loaded=?,
                    relation_rows_loaded=?,issue_count=? WHERE ingest_run_id=?
                """,
                (
                    completed_at,
                    counts["files_seen"],
                    counts["files_changed"],
                    counts["structured_files_profiled"],
                    counts["object_rows_loaded"],
                    counts["relation_rows_loaded"],
                    counts["issue_count"],
                    ingest_run_id,
                ),
            )
            connection.execute(
                """
                UPDATE change_set SET state='committed',committed_at=? WHERE change_set_id=?
                """,
                (completed_at, change_set_id),
            )
            if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
                raise KnowledgeBaseError("Foreign-key validation failed inside the ingestion transaction.")
            semantic_failures = [
                name
                for name, sql in SEMANTIC_CHECKS
                if int(connection.execute(sql).fetchone()[0]) != 0
            ]
            if semantic_failures:
                raise KnowledgeBaseError(
                    "Semantic validation failed inside the ingestion transaction: "
                    + ", ".join(semantic_failures)
                )
            connection.commit()
            connection.execute("PRAGMA optimize")
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
    return counts
