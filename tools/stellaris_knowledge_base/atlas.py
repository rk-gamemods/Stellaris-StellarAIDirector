from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .db import KnowledgeBaseError
from .paths import REPO_ROOT, TARGET_VERSION


MOD_SNAPSHOT_PATHS = {
    "1121692237": "1121692237-gigastructural-engineering-more-44",
    "3610149307": "3610149307-stellar-ai",
    "683230077": "683230077-nsc3",
    "2648658105": "2648658105-extra-ship-components-next",
    "3250900527": "3250900527-starbase-extended-30",
}

OBJECT_KIND_ALIASES = {
    "pop_job": "job",
    "scripted_value": "script_value",
    "scripted_variable": "scripted_variable",
}

EDGE_RELATION_TYPES = {
    "belongs_to_route": "part_of",
    "flag_gate_or_effect": "interacts_with",
    "requires_technology": "gated_by",
    "upgrades_from": "depends_on",
    "upgrades_to": "unlocks",
    "unlocks_object": "unlocks",
    "requires_resource_stockpile": "gated_by",
}


def _id(connection, table: str, key_column: str, value: str, id_column: str | None = None) -> int:
    id_column = id_column or f"{table}_id"
    row = connection.execute(
        f"SELECT {id_column} FROM {table} WHERE {key_column}=?", (value,)
    ).fetchone()
    if row is None:
        raise KnowledgeBaseError(f"Missing {table}.{key_column}={value}")
    return int(row[0])


def _ensure_item_type(connection, type_code: str, type_name: str, description: str) -> int:
    row = connection.execute(
        "SELECT item_type_id FROM item_type WHERE type_code=?", (type_code,)
    ).fetchone()
    if row:
        return int(row[0])
    next_id = int(connection.execute("SELECT COALESCE(MAX(item_type_id),0)+1 FROM item_type").fetchone()[0])
    connection.execute(
        "INSERT INTO item_type(item_type_id,type_code,type_name,description) VALUES (?,?,?,?)",
        (next_id, type_code, type_name, description),
    )
    return next_id


def _ensure_object_kind(connection, kind_code: str) -> int:
    kind_code = OBJECT_KIND_ALIASES.get(kind_code, kind_code)
    row = connection.execute(
        "SELECT object_kind_id FROM object_kind WHERE kind_code=?", (kind_code,)
    ).fetchone()
    if row:
        return int(row[0])
    next_id = int(connection.execute("SELECT COALESCE(MAX(object_kind_id),0)+1 FROM object_kind").fetchone()[0])
    connection.execute(
        """
        INSERT INTO object_kind(object_kind_id,kind_code,kind_name,definition_folder,description)
        VALUES (?,?,?,?,?)
        """,
        (
            next_id,
            kind_code,
            kind_code.replace("_", " ").title(),
            "unknown",
            "Object kind registered from the 4.4.4 object atlas; exact loader folder remains source-routed.",
        ),
    )
    return next_id


def _ensure_knowledge_item(
    connection,
    *,
    canonical_key: str,
    display_name: str,
    summary: str,
    item_type_code: str,
    change_set_id: int,
    actor_id: int,
) -> int:
    item_type_id = _id(connection, "item_type", "type_code", item_type_code)
    lifecycle_state_id = _id(connection, "lifecycle_state", "state_code", "active")
    connection.execute(
        """
        INSERT INTO knowledge_item(
            item_type_id,canonical_key,display_name,summary,lifecycle_state_id,
            created_by_actor_id,created_in_change_set_id
        ) VALUES (?,?,?,?,?,?,?)
        ON CONFLICT(canonical_key) DO UPDATE SET
            display_name=excluded.display_name,
            summary=excluded.summary,
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now'),
            updated_in_change_set_id=excluded.created_in_change_set_id
        """,
        (
            item_type_id,
            canonical_key,
            display_name,
            summary,
            lifecycle_state_id,
            actor_id,
            change_set_id,
        ),
    )
    return _id(connection, "knowledge_item", "canonical_key", canonical_key, "item_id")


def _ensure_game_object(
    connection,
    *,
    object_type: str,
    object_id: str,
    origin_class: str,
    change_set_id: int,
    actor_id: int,
) -> int:
    normalized_type = OBJECT_KIND_ALIASES.get(object_type, object_type)
    canonical_key = f"object:{normalized_type}:{object_id}"
    item_id = _ensure_knowledge_item(
        connection,
        canonical_key=canonical_key,
        display_name=object_id,
        summary=f"Stellaris {normalized_type} registered from the version-attested 4.4.4 object atlas.",
        item_type_code="game_object",
        change_set_id=change_set_id,
        actor_id=actor_id,
    )
    kind_id = _ensure_object_kind(connection, normalized_type)
    existing = connection.execute("SELECT item_id FROM game_object WHERE item_id=?", (item_id,)).fetchone()
    if not existing:
        connection.execute(
            """
            INSERT INTO game_object(item_id,object_kind_id,script_key,namespace,origin_class,notes)
            VALUES (?,?,?,'',?,?)
            """,
            (
                item_id,
                kind_id,
                object_id,
                origin_class,
                "Stable object identity; definition occurrences retain their individual source origins.",
            ),
        )
    return item_id


def _ensure_mod_release_and_root(
    connection,
    *,
    mod_id: str,
    mod_name: str,
    version_span_id: int,
    target_version_id: int,
    change_set_id: int,
    actor_id: int,
    repository_snapshot_id: int,
    observed_at: str,
) -> tuple[int | None, int]:
    if mod_id == "vanilla":
        root = connection.execute(
            """
            SELECT source_root_id FROM source_root
            WHERE root_key LIKE 'vanilla:4.4.4:%' AND availability_status='available'
            ORDER BY source_root_id DESC LIMIT 1
            """
        ).fetchone()
        if not root:
            raise KnowledgeBaseError("The current 4.4.4 vanilla root was not registered.")
        return None, int(root[0])
    _ensure_item_type(connection, "mod", "Mod", "Stellaris mod package identity.")
    mod_item_id = _ensure_knowledge_item(
        connection,
        canonical_key=f"mod:{mod_id}",
        display_name=mod_name,
        summary=f"Captured mod source represented in the 4.4.4 object atlas ({mod_id}).",
        item_type_code="mod",
        change_set_id=change_set_id,
        actor_id=actor_id,
    )
    connection.execute(
        """
        INSERT INTO mod_package(item_id,mod_key,steam_workshop_id,mod_scope,author_or_owner,homepage_uri,notes)
        VALUES (?,?,?,'workshop_mod',NULL,NULL,?)
        ON CONFLICT(item_id) DO UPDATE SET notes=excluded.notes
        """,
        (mod_item_id, f"workshop:{mod_id}", mod_id, "Registered from the version-attested object atlas."),
    )
    release_key = f"atlas:{mod_id}:{TARGET_VERSION}"
    existing = connection.execute(
        "SELECT mod_release_id FROM mod_release WHERE release_key=?", (release_key,)
    ).fetchone()
    if existing:
        mod_release_id = int(existing[0])
    else:
        cursor = connection.execute(
            """
            INSERT INTO mod_release(
                mod_item_id,release_key,version_text,version_span_id,supported_game_pattern,
                remote_file_id,descriptor_artifact_id,captured_at,release_status,notes,
                created_in_change_set_id
            ) VALUES (?,?,NULL,?,'v4.4.*',?,NULL,?,'active',?,?)
            """,
            (
                mod_item_id,
                release_key,
                version_span_id,
                mod_id,
                observed_at,
                "Occurrence source for the 4.4.4 object atlas; exact Workshop version text was not asserted.",
                change_set_id,
            ),
        )
        mod_release_id = int(cursor.lastrowid)
    snapshot_name = MOD_SNAPSHOT_PATHS.get(mod_id)
    canonical = (
        REPO_ROOT / "research" / "mod-source-snapshots" / "2026-07-04" / snapshot_name
        if snapshot_name
        else REPO_ROOT / "research" / "mod-source-snapshots" / "2026-07-04" / mod_id
    )
    root_key = f"atlas-mod:{mod_id}:{TARGET_VERSION}"
    connection.execute(
        """
        INSERT INTO source_root(
            root_key,root_kind,canonical_path,repository_snapshot_id,mod_release_id,
            game_version_id,captured_at,availability_status,authoritative_for,notes,
            created_in_change_set_id
        ) VALUES (?,'mod_snapshot',?,?,?,?,?,'available',?,?,?)
        ON CONFLICT(root_key) DO UPDATE SET
            captured_at=excluded.captured_at,availability_status='available'
        """,
        (
            root_key,
            str(canonical),
            repository_snapshot_id,
            mod_release_id,
            target_version_id,
            observed_at,
            "Captured source occurrence represented by the 4.4.4 object atlas.",
            "Path availability is cataloged separately; the atlas remains the row-level authority.",
            change_set_id,
        ),
    )
    source_root_id = _id(connection, "source_root", "root_key", root_key)
    return mod_release_id, source_root_id


def _ensure_atlas_source_system(connection, change_set_id: int) -> int:
    evidence_type_id = _id(connection, "evidence_source_type", "type_code", "repository")
    connection.execute(
        """
        INSERT INTO source_system(
            system_key,system_name,evidence_source_type_id,canonical_root,access_mode,
            authoritative_for,default_tool_item_id,retrieval_instructions,is_local_only,
            notes,created_in_change_set_id
        ) VALUES ('captured-mod-source-roots','Captured 4.4.4 mod source roots',?,?,'filesystem/index',
                  'Object definition occurrences represented by the generated object atlas',NULL,?,1,?,?)
        ON CONFLICT(system_key) DO NOTHING
        """,
        (
            evidence_type_id,
            str(REPO_ROOT / "research" / "mod-source-snapshots"),
            "Use the object-atlas record locator, then retrieve the exact source root/path and verify the captured version context.",
            "The generated atlas is the occurrence locator; raw source remains external authority.",
            change_set_id,
        ),
    )
    return _id(connection, "source_system", "system_key", "captured-mod-source-roots")


def ingest_object_atlas(
    connection,
    *,
    rows: list[dict[str, str]],
    source_artifact_id: int,
    dataset_schema_id: int,
    version_span_code: str,
    change_set_id: int,
    actor_id: int,
    repository_snapshot_id: int,
    observed_at: str,
) -> int:
    existing = connection.execute(
        "SELECT COUNT(*) FROM kb_object_atlas_entry WHERE dataset_schema_id=?",
        (dataset_schema_id,),
    ).fetchone()[0]
    if existing:
        return 0
    version_span_id = _id(connection, "version_span", "span_code", version_span_code)
    target_version_id = _id(connection, "game_version", "version_label", TARGET_VERSION)
    locator_type_id = _id(connection, "locator_type", "type_code", "dataset_record")
    source_system_id = _ensure_atlas_source_system(connection, change_set_id)
    mod_cache: dict[tuple[str, str], tuple[int | None, int]] = {}
    loaded = 0
    for row_number, row in enumerate(rows, start=1):
        object_id = (row.get("object_id") or "").strip()
        object_type = (row.get("object_type") or "unknown").strip()
        mod_id = (row.get("mod_id") or "unknown").strip()
        mod_name = (row.get("mod_name") or mod_id).strip()
        if not object_id:
            continue
        origin_class = "vanilla" if mod_id == "vanilla" else "external_mod"
        object_item_id = _ensure_game_object(
            connection,
            object_type=object_type,
            object_id=object_id,
            origin_class=origin_class,
            change_set_id=change_set_id,
            actor_id=actor_id,
        )
        cache_key = (mod_id, mod_name)
        if cache_key not in mod_cache:
            mod_cache[cache_key] = _ensure_mod_release_and_root(
                connection,
                mod_id=mod_id,
                mod_name=mod_name,
                version_span_id=version_span_id,
                target_version_id=target_version_id,
                change_set_id=change_set_id,
                actor_id=actor_id,
                repository_snapshot_id=repository_snapshot_id,
                observed_at=observed_at,
            )
        mod_release_id, source_root_id = mod_cache[cache_key]
        locator_key = f"object-atlas-row:{row_number}"
        cursor = connection.execute(
            """
            INSERT INTO evidence_locator(
                source_artifact_id,dataset_schema_id,locator_type_id,stable_locator_key,
                label,relative_path,record_set,record_key,row_number,evidence_summary,
                retrieval_instructions,created_by_actor_id,created_in_change_set_id
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                source_artifact_id,
                dataset_schema_id,
                locator_type_id,
                locator_key,
                f"Object atlas row {row_number}: {object_type}:{object_id}",
                row.get("source_file"),
                "object-atlas-2026-07-06",
                f"{object_type}:{object_id}:{mod_id}:{row.get('source_file','')}",
                row_number,
                "Generated 4.4.4 object occurrence and classification row.",
                "Use JDataMunch on stellaris_ai_director_object_atlas_2026_07_06 and verify the underlying source file before promoting behavior claims.",
                actor_id,
                change_set_id,
            ),
        )
        evidence_locator_id = int(cursor.lastrowid)
        cursor = connection.execute(
            """
            INSERT INTO object_definition(
                object_item_id,version_span_id,source_system_id,source_root_id,
                mod_release_id,evidence_locator_id,definition_status,object_path,
                line_start,line_end,content_hash_algorithm,content_hash,notes,
                created_in_change_set_id
            ) VALUES (?,?,?,?,?,?,'candidate',?,NULL,NULL,NULL,NULL,?,?)
            """,
            (
                object_item_id,
                version_span_id,
                source_system_id,
                source_root_id,
                mod_release_id,
                evidence_locator_id,
                row.get("source_file"),
                "Occurrence registered from the object atlas. The load_winner signal is retained in kb_object_atlas_entry, not promoted to playset resolution.",
                change_set_id,
            ),
        )
        object_definition_id = int(cursor.lastrowid)
        connection.execute(
            """
            INSERT INTO kb_object_atlas_entry(
                dataset_schema_id,row_number,object_definition_id,evidence_locator_id,
                mod_id,mod_name,source_file,load_winner_signal,source_has_ai_weight,
                strategic_role,strategic_tier,parent_ai_support,policy_status,
                director_action,validation_status
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                dataset_schema_id,
                row_number,
                object_definition_id,
                evidence_locator_id,
                mod_id,
                mod_name,
                row.get("source_file") or "",
                row.get("load_winner") or "unknown",
                row.get("source_has_ai_weight") or "unknown",
                row.get("strategic_role") or None,
                row.get("strategic_tier") or None,
                row.get("parent_ai_support") or None,
                row.get("policy_status") or None,
                row.get("director_action") or None,
                row.get("validation_status") or "unknown",
            ),
        )
        loaded += 1
    return loaded


def _dependency_item(
    connection,
    *,
    item_type: str,
    item_id: str,
    change_set_id: int,
    actor_id: int,
) -> int:
    normalized = OBJECT_KIND_ALIASES.get(item_type, item_type)
    if normalized == "route":
        _ensure_item_type(connection, "strategic_route", "Strategic route", "AI strategic planning route.")
        return _ensure_knowledge_item(
            connection,
            canonical_key=f"route:{item_id}",
            display_name=item_id,
            summary="Strategic route registered from the generated 4.4.4 dependency graph.",
            item_type_code="strategic_route",
            change_set_id=change_set_id,
            actor_id=actor_id,
        )
    if normalized == "flag":
        _ensure_item_type(connection, "setting", "State flag or setting", "Persistent script flag or setting.")
        return _ensure_knowledge_item(
            connection,
            canonical_key=f"flag:{item_id}",
            display_name=item_id,
            summary="Script flag referenced by the generated 4.4.4 dependency graph.",
            item_type_code="setting",
            change_set_id=change_set_id,
            actor_id=actor_id,
        )
    if normalized == "object":
        normalized = "unknown"
    return _ensure_game_object(
        connection,
        object_type=normalized,
        object_id=item_id,
        origin_class="unknown",
        change_set_id=change_set_id,
        actor_id=actor_id,
    )


def ingest_dependency_edges(
    connection,
    *,
    rows: list[dict[str, str]],
    source_artifact_id: int,
    dataset_schema_id: int,
    version_span_code: str,
    change_set_id: int,
    actor_id: int,
) -> int:
    existing = connection.execute(
        "SELECT COUNT(*) FROM kb_dependency_edge_entry WHERE dataset_schema_id=?",
        (dataset_schema_id,),
    ).fetchone()[0]
    if existing:
        return 0
    version_span_id = _id(connection, "version_span", "span_code", version_span_code)
    confidence_id = _id(connection, "confidence_level", "confidence_code", "medium")
    risk_id = _id(connection, "risk_level", "risk_code", "medium")
    stance_id = _id(connection, "evidence_stance", "stance_code", "supports")
    locator_type_id = _id(connection, "locator_type", "type_code", "dataset_record")
    loaded = 0
    for row_number, row in enumerate(rows, start=1):
        source_id = (row.get("source_id") or "").strip()
        target_id = (row.get("target_id") or "").strip()
        source_type = (row.get("source_type") or "unknown").strip()
        target_type = (row.get("target_type") or "unknown").strip()
        edge_type = (row.get("edge_type") or "interacts_with").strip()
        if not source_id or not target_id:
            continue
        source_item_id = _dependency_item(
            connection,
            item_type=source_type,
            item_id=source_id,
            change_set_id=change_set_id,
            actor_id=actor_id,
        )
        target_item_id = _dependency_item(
            connection,
            item_type=target_type,
            item_id=target_id,
            change_set_id=change_set_id,
            actor_id=actor_id,
        )
        if source_item_id == target_item_id:
            continue
        relation_code = EDGE_RELATION_TYPES.get(edge_type, "interacts_with")
        relation_type_id = _id(connection, "relation_type", "type_code", relation_code)
        locator_key = f"dependency-edge-row:{row_number}"
        cursor = connection.execute(
            """
            INSERT INTO evidence_locator(
                source_artifact_id,dataset_schema_id,locator_type_id,stable_locator_key,
                label,relative_path,record_set,record_key,row_number,evidence_summary,
                retrieval_instructions,created_by_actor_id,created_in_change_set_id
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                source_artifact_id,
                dataset_schema_id,
                locator_type_id,
                locator_key,
                f"Dependency row {row_number}: {source_type}:{source_id} {edge_type} {target_type}:{target_id}",
                row.get("source_file"),
                "dependency-edges-2026-07-06",
                f"{source_type}:{source_id}:{edge_type}:{target_type}:{target_id}",
                row_number,
                "Generated dependency edge derived from the version-attested 4.4.4 object atlas.",
                "Use JDataMunch on stellaris_ai_director_dependency_edges_2026_07_06 and inspect the underlying source before promoting exact behavior claims.",
                actor_id,
                change_set_id,
            ),
        )
        evidence_locator_id = int(cursor.lastrowid)
        connection.execute(
            """
            INSERT INTO item_relation(
                source_item_id,relation_type_id,target_item_id,version_span_id,
                confidence_level_id,risk_level_id,source_claim_id,rationale,
                impact_explanation,review_action,validation_action,is_current,
                created_in_change_set_id,retired_in_change_set_id
            ) VALUES (?,?,?,?,?,?,NULL,?,?,?,?,1,?,NULL)
            ON CONFLICT(source_item_id,relation_type_id,target_item_id,version_span_id)
            WHERE is_current=1 DO NOTHING
            """,
            (
                source_item_id,
                relation_type_id,
                target_item_id,
                version_span_id,
                confidence_id,
                risk_id,
                f"Generated edge type {edge_type}; target status {row.get('target_status','unknown')}; evidence {row.get('evidence','unknown')}.",
                "Changes should review the connected item, but the generated edge does not by itself prove runtime causation.",
                f"Inspect {row.get('source_file') or 'the registered source'} and the target definition.",
                "Re-run the dependency generator and applicable static/runtime checks for the exact 4.4.4 context.",
                change_set_id,
            ),
        )
        relation = connection.execute(
            """
            SELECT item_relation_id FROM item_relation
            WHERE source_item_id=? AND relation_type_id=? AND target_item_id=?
              AND version_span_id=? AND is_current=1
            """,
            (source_item_id, relation_type_id, target_item_id, version_span_id),
        ).fetchone()
        if not relation:
            raise KnowledgeBaseError("Dependency relation insert did not resolve to a current relation.")
        item_relation_id = int(relation[0])
        relation_key = f"generated:{version_span_code}:{relation_code}:{source_type}:{source_id}:{target_type}:{target_id}"
        connection.execute(
            "INSERT OR IGNORE INTO kb_relation_identity(item_relation_id,relation_key) VALUES (?,?)",
            (item_relation_id, relation_key),
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO relation_evidence(
                item_relation_id,evidence_locator_id,evidence_stance_id,strength_rank,interpretation
            ) VALUES (?,?,?,3,?)
            """,
            (
                item_relation_id,
                evidence_locator_id,
                stance_id,
                "Generated static edge supports review relevance; exact behavior and direction remain evidence-scoped.",
            ),
        )
        connection.execute(
            """
            INSERT INTO kb_dependency_edge_entry(
                dataset_schema_id,row_number,item_relation_id,evidence_locator_id,
                source_type,edge_type,target_type,target_status,source_file,evidence_code
            ) VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                dataset_schema_id,
                row_number,
                item_relation_id,
                evidence_locator_id,
                source_type,
                edge_type,
                target_type,
                row.get("target_status") or "unknown",
                row.get("source_file") or "",
                row.get("evidence") or "unknown",
            ),
        )
        loaded += 1
    return loaded
