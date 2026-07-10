from __future__ import annotations

import hashlib
import os
import sqlite3
import tempfile
from pathlib import Path

from .db import (
    APPLICATION_ID,
    USER_VERSION,
    KnowledgeBaseError,
    checkpoint_database,
    exclusive_writer_lock,
    maintenance_lock_path,
    publish_no_replace,
    validate_database,
    writer_lock_path,
)
from .paths import DESIGN_ROOT, MIGRATIONS_ROOT


SCHEMA_PATH = DESIGN_ROOT / "stellaris_knowledge_base_schema.sql"
BOOTSTRAP_PATH = MIGRATIONS_ROOT / "0002_production_bootstrap.sql"
PRODUCTION_MIGRATION_PATH = MIGRATIONS_ROOT / "0003_production_ingestion.sql"
QUESTION_ROUTING_MIGRATION_PATH = MIGRATIONS_ROOT / "0004_question_research_routing.sql"


def _migration_sql(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    marker = "{{MIGRATION_SHA256}}"
    if marker not in text:
        raise KnowledgeBaseError(f"Migration hash marker is missing from {path}")
    return "BEGIN IMMEDIATE;\n" + text.replace(marker, digest) + "\nCOMMIT;\n"


def create_seeded_database(path: Path) -> None:
    if path.exists():
        raise KnowledgeBaseError(f"Refusing to overwrite database: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    try:
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=30000")
        connection.execute("PRAGMA recursive_triggers=ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        if int(connection.execute("PRAGMA application_id").fetchone()[0]) != APPLICATION_ID:
            raise KnowledgeBaseError("The staged schema produced the wrong application_id.")
        connection.executescript(BOOTSTRAP_PATH.read_text(encoding="utf-8"))
        connection.executescript(_migration_sql(PRODUCTION_MIGRATION_PATH))
        connection.executescript(_migration_sql(QUESTION_ROUTING_MIGRATION_PATH))
        if int(connection.execute("PRAGMA user_version").fetchone()[0]) != USER_VERSION:
            raise KnowledgeBaseError("The production migration did not advance user_version.")
    finally:
        connection.close()


def migrate_database(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise KnowledgeBaseError(f"Knowledge-base file does not exist: {path}")
    connection = sqlite3.connect(path)
    try:
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=30000")
        connection.execute("PRAGMA recursive_triggers=ON")
        application_id = int(connection.execute("PRAGMA application_id").fetchone()[0])
        user_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
        if application_id != APPLICATION_ID:
            raise KnowledgeBaseError(f"Wrong application_id={application_id}; expected {APPLICATION_ID}.")
        if user_version == USER_VERSION:
            return {"result": "no_op", "user_version": user_version}
        if user_version not in {2, 3}:
            raise KnowledgeBaseError(f"No reviewed migration path from user_version={user_version}.")
        if user_version == 2:
            profile = connection.execute(
                "SELECT metadata_value FROM schema_metadata WHERE metadata_key='seed_profile'"
            ).fetchone()
            if profile and str(profile[0]).startswith("representative_examples"):
                raise KnowledgeBaseError(
                    "Refusing to migrate a demonstration-fixture database into production; install a fresh production database."
                )
            connection.executescript(_migration_sql(PRODUCTION_MIGRATION_PATH))
        connection.executescript(_migration_sql(QUESTION_ROUTING_MIGRATION_PATH))
    finally:
        connection.close()
    return {"result": "migrated", "user_version": USER_VERSION}


def build_atomic_database(destination: Path, populate) -> dict[str, object]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with exclusive_writer_lock("atomic database installation", writer_lock_path(destination)):
        if destination.exists():
            raise KnowledgeBaseError(
                f"A live database already exists at {destination}; use refresh instead of reinstalling."
            )
        descriptor, name = tempfile.mkstemp(
            prefix=".stellaris_knowledge_base.", suffix=".sqlite3", dir=destination.parent
        )
        os.close(descriptor)
        temporary = Path(name)
        temporary.unlink(missing_ok=True)
        try:
            create_seeded_database(temporary)
            populate(temporary, run_kind="install")
            checkpoint_database(temporary, truncate=True)
            validation = validate_database(temporary, full=True)
            if not validation["ok"]:
                raise KnowledgeBaseError(
                    f"New database failed validation: {validation['problems']}"
                )
            publish_no_replace(temporary, destination)
            return validate_database(destination, full=True)
        finally:
            temporary.unlink(missing_ok=True)
            writer_lock_path(temporary).unlink(missing_ok=True)
            maintenance_lock_path(temporary).unlink(missing_ok=True)
