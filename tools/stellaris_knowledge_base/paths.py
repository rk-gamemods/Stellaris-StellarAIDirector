from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_ROOT = REPO_ROOT / "knowledge-base"
DESIGN_ROOT = KNOWLEDGE_BASE_ROOT / "design"
MIGRATIONS_ROOT = KNOWLEDGE_BASE_ROOT / "migrations"
MANIFESTS_ROOT = KNOWLEDGE_BASE_ROOT / "manifests"
RUNTIME_ROOT = KNOWLEDGE_BASE_ROOT / "runtime"
BACKUP_ROOT = KNOWLEDGE_BASE_ROOT / "backups"
LIVE_DATABASE = RUNTIME_ROOT / "stellaris_knowledge_base.sqlite3"
WRITE_LOCK = RUNTIME_ROOT / "stellaris_knowledge_base.write.lock"
TARGET_VERSION = "4.4.4"


def stellaris_install_root() -> Path:
    configured = os.environ.get("STELLARIS_INSTALL_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(r"C:\Steam\steamapps\common\Stellaris")


def jdatamunch_manifest() -> Path:
    return MANIFESTS_ROOT / "jdatamunch_datasets.json"
