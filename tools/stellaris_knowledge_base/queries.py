from __future__ import annotations

import contextlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from .db import (
    KnowledgeBaseError,
    connect_read_only,
    lock_status,
    maintenance_status,
    writer_lock_path,
)
from .paths import TARGET_VERSION


def _rows(cursor: sqlite3.Cursor) -> list[dict[str, Any]]:
    return [dict(row) for row in cursor.fetchall()]


def status(database: Path) -> dict[str, Any]:
    with contextlib.closing(connect_read_only(database)) as connection:
        latest = connection.execute(
            """
            SELECT run_key,run_kind,state,started_at,completed_at,files_seen,files_changed,
                   structured_files_profiled,object_rows_loaded,relation_rows_loaded,issue_count
            FROM kb_ingest_run ORDER BY ingest_run_id DESC LIMIT 1
            """
        ).fetchone()
        baseline = connection.execute(
            """
            SELECT b.display_version,b.raw_version,b.checksum_or_build,b.steam_build_id,
                   b.captured_at,sr.canonical_path
            FROM kb_environment_baseline b
            JOIN source_root sr ON sr.source_root_id=b.source_root_id
            WHERE b.is_current=1
            """
        ).fetchone()
        counts = {}
        for label, sql in {
            "knowledge_items": "SELECT COUNT(*) FROM knowledge_item",
            "game_objects": "SELECT COUNT(*) FROM game_object",
            "object_definitions": "SELECT COUNT(*) FROM object_definition",
            "claims": "SELECT COUNT(*) FROM claim",
            "open_questions": "SELECT COUNT(*) FROM open_question WHERE status_code NOT IN ('resolved','wont_fix')",
            "current_relations": "SELECT COUNT(*) FROM item_relation WHERE is_current=1",
            "source_artifacts": "SELECT COUNT(*) FROM source_artifact",
            "current_catalog_files": "SELECT COUNT(*) FROM kb_catalog_entry WHERE availability_status='available'",
            "dataset_schemas": "SELECT COUNT(*) FROM dataset_schema",
            "dataset_columns": "SELECT COUNT(*) FROM dataset_column",
            "jdatamunch_handles": "SELECT COUNT(*) FROM kb_external_dataset_handle WHERE provider_code='jdatamunch' AND is_current=1",
            "atlas_rows": "SELECT COUNT(*) FROM kb_object_atlas_entry",
            "dependency_rows": "SELECT COUNT(*) FROM kb_dependency_edge_entry",
        }.items():
            counts[label] = int(connection.execute(sql).fetchone()[0])
        payload = {
            "database": str(database.resolve()),
            "application_id": int(connection.execute("PRAGMA application_id").fetchone()[0]),
            "user_version": int(connection.execute("PRAGMA user_version").fetchone()[0]),
            "journal_mode": str(connection.execute("PRAGMA journal_mode").fetchone()[0]),
            "primary_target": connection.execute(
                "SELECT version_label FROM game_version WHERE is_primary_target=1"
            ).fetchone()[0],
            "baseline": dict(baseline) if baseline else None,
            "latest_ingest": dict(latest) if latest else None,
            "counts": counts,
        }
    payload["writer_lock"] = lock_status(writer_lock_path(database))
    payload["maintenance_access"] = maintenance_status(database)
    return payload


def _fts_query(text: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9_.:-]+", text)
    if not tokens:
        raise KnowledgeBaseError("Search text did not contain any FTS-safe tokens.")
    return " OR ".join(f'"{token.replace(chr(34), "")}"' for token in tokens[:20])


def search(database: Path, text: str, limit: int = 25) -> list[dict[str, Any]]:
    query = _fts_query(text)
    with contextlib.closing(connect_read_only(database)) as connection:
        return _rows(
            connection.execute(
                """
                SELECT 'item' AS result_kind,ki.canonical_key AS result_key,
                       ki.display_name AS title,ki.summary AS detail,bm25(item_fts) AS rank
                FROM item_fts JOIN knowledge_item ki ON ki.item_id=item_fts.rowid
                WHERE item_fts MATCH ?
                UNION ALL
                SELECT 'claim','claim:'||c.claim_id,c.statement,COALESCE(c.epistemic_note,''),bm25(claim_fts)
                FROM claim_fts JOIN claim c ON c.claim_id=claim_fts.rowid
                WHERE claim_fts MATCH ?
                UNION ALL
                SELECT 'question',q.question_key,q.question_text,q.uncertainty_reason,bm25(question_fts)
                FROM question_fts JOIN open_question q ON q.question_id=question_fts.rowid
                WHERE question_fts MATCH ?
                ORDER BY rank LIMIT ?
                """,
                (query, query, query, limit),
            )
        )


def dossier(database: Path, item_key: str, version: str) -> dict[str, Any]:
    if version != TARGET_VERSION:
        raise KnowledgeBaseError(f"Production dossier queries require --version {TARGET_VERSION}.")
    with contextlib.closing(connect_read_only(database)) as connection:
        item = connection.execute(
            """
            SELECT ki.item_id,ki.canonical_key,ki.display_name,ki.summary,it.type_code
            FROM knowledge_item ki JOIN item_type it ON it.item_type_id=ki.item_type_id
            WHERE ki.canonical_key=?
            """,
            (item_key,),
        ).fetchone()
        if item is None:
            raise KnowledgeBaseError(f"Unknown knowledge item: {item_key}")
        claims = _rows(
            connection.execute(
                """
                SELECT c.claim_id,kci.claim_key,c.statement,c.context,c.epistemic_note,
                       vca.assessment_state,vca.confidence_code,vca.assessed_at,
                       vca.basis_summary,vca.reverify_after
                FROM claim c
                LEFT JOIN kb_claim_identity kci ON kci.claim_id=c.claim_id
                JOIN v_current_claim_assessment vca ON vca.claim_id=c.claim_id
                JOIN version_span vs ON vs.version_span_id=vca.version_span_id
                JOIN game_version target ON target.version_label=?
                LEFT JOIN game_version minv ON minv.game_version_id=vs.min_version_id
                LEFT JOIN game_version maxv ON maxv.game_version_id=vs.max_version_id
                WHERE c.primary_item_id=?
                  AND target.version_order BETWEEN COALESCE(minv.version_order,target.version_order)
                                               AND COALESCE(maxv.version_order,target.version_order)
                ORDER BY c.claim_id
                """,
                (version, item["item_id"]),
            )
        )
        evidence = _rows(
            connection.execute(
                """
                SELECT ce.claim_id,es.stance_code,ce.directness_rank,ce.strength_rank,
                       ce.interpretation,el.label,sa.source_artifact_id,
                       ss.system_key AS source_system,est.type_code AS evidence_source_type,
                       (SELECT group_concat(DISTINCT kce.corpus_code)
                        FROM kb_catalog_entry kce
                        WHERE kce.current_source_artifact_id=sa.source_artifact_id) AS artifact_corpora,
                       sa.uri_or_path,sa.repository_relative_path,el.relative_path,
                       sa.content_hash_algorithm,sa.content_hash_value,sa.file_size_bytes,
                       gv.version_label AS artifact_game_version,sa.repository_commit,
                       sa.modified_at,sa.captured_at,sa.observed_at,
                        el.line_start,el.line_end,el.section_title,el.record_set,
                        el.record_key,el.row_number,el.column_name,el.retrieval_instructions
                FROM claim c
                JOIN claim_evidence ce ON ce.claim_id=c.claim_id
                JOIN evidence_stance es ON es.evidence_stance_id=ce.evidence_stance_id
                JOIN evidence_locator el ON el.evidence_locator_id=ce.evidence_locator_id
                JOIN source_artifact sa ON sa.source_artifact_id=el.source_artifact_id
                JOIN source_system ss ON ss.source_system_id=sa.source_system_id
                JOIN evidence_source_type est ON est.evidence_source_type_id=ss.evidence_source_type_id
                LEFT JOIN game_version gv ON gv.game_version_id=sa.game_version_id
                WHERE c.primary_item_id=?
                ORDER BY ce.claim_id,ce.strength_rank DESC,ce.directness_rank DESC
                """,
                (item["item_id"],),
            )
        )
        questions = _rows(
            connection.execute(
                """
                SELECT question_key,question_text,uncertainty_reason,status_code,
                       evidence_mode_code,runtime_approval_required,next_action,priority
                FROM open_question WHERE primary_item_id=? AND target_version_id=(
                    SELECT game_version_id FROM game_version WHERE version_label=?
                ) ORDER BY priority DESC,question_key
                """,
                (item["item_id"], version),
            )
        )
        return {
            "target_version": version,
            "item": dict(item),
            "claims": claims,
            "evidence": evidence,
            "questions": questions,
        }


def impact(
    database: Path,
    item_key: str,
    version: str,
    max_depth: int = 3,
    limit: int = 100,
    relation_types: list[str] | None = None,
) -> list[dict[str, Any]]:
    if version != TARGET_VERSION:
        raise KnowledgeBaseError(f"Production impact queries require --version {TARGET_VERSION}.")
    if max_depth < 1 or max_depth > 12:
        raise KnowledgeBaseError("Impact depth must be between 1 and 12.")
    if limit < 1 or limit > 500:
        raise KnowledgeBaseError("Impact limit must be between 1 and 500.")
    relation_types_json = json.dumps(relation_types) if relation_types else None
    with contextlib.closing(connect_read_only(database)) as connection:
        return _rows(
            connection.execute(
                """
                WITH RECURSIVE
                target(version_order) AS (
                    SELECT version_order FROM game_version WHERE version_label=:version
                ),
                start(item_id) AS (
                    SELECT item_id FROM knowledge_item WHERE canonical_key=:item_key
                ),
                arcs AS (
                    SELECT a.*,
                           COALESCE((
                               SELECT group_concat(el.stable_locator_key,';')
                               FROM relation_evidence re
                               JOIN evidence_locator el
                                 ON el.evidence_locator_id=re.evidence_locator_id
                               WHERE re.item_relation_id=a.item_relation_id
                           ),'') AS edge_evidence
                    FROM v_impact_arc a
                    JOIN version_span vs ON vs.version_span_id=a.version_span_id
                    JOIN target t
                    LEFT JOIN game_version minv ON minv.game_version_id=vs.min_version_id
                    LEFT JOIN game_version maxv ON maxv.game_version_id=vs.max_version_id
                    WHERE t.version_order BETWEEN COALESCE(minv.version_order,t.version_order)
                                              AND COALESCE(maxv.version_order,t.version_order)
                      AND (:relation_types_json IS NULL OR a.relation_type_code IN (
                          SELECT value FROM json_each(:relation_types_json)
                      ))
                ),
                walk(item_id,depth,item_path,canonical_path,relation_path,relation_id_path,
                     relation_evidence_path,max_risk,review_actions,validation_actions) AS (
                    SELECT s.item_id,0,'|'||s.item_id||'|',ki.canonical_key,'','','',0,'',''
                    FROM start s JOIN knowledge_item ki ON ki.item_id=s.item_id
                    UNION ALL
                    SELECT a.affected_item_id,w.depth+1,
                           w.item_path||a.affected_item_id||'|',
                           w.canonical_path||' > '||affected.canonical_key,
                           CASE WHEN w.relation_path='' THEN a.relation_type_code
                                ELSE w.relation_path||' > '||a.relation_type_code END,
                           CASE WHEN w.relation_id_path='' THEN CAST(a.item_relation_id AS TEXT)
                                ELSE w.relation_id_path||' > '||a.item_relation_id END,
                           trim(w.relation_evidence_path||
                                CASE WHEN a.edge_evidence='' THEN '' ELSE ' | '||a.edge_evidence END,' |'),
                           MAX(w.max_risk,rl.rank_value),
                           trim(w.review_actions||CASE WHEN a.review_action IS NULL THEN '' ELSE ' | '||a.review_action END,' |'),
                           trim(w.validation_actions||CASE WHEN a.validation_action IS NULL THEN '' ELSE ' | '||a.validation_action END,' |')
                    FROM walk w JOIN arcs a ON a.changed_item_id=w.item_id
                    JOIN risk_level rl ON rl.risk_level_id=a.risk_level_id
                    JOIN knowledge_item affected ON affected.item_id=a.affected_item_id
                    WHERE w.depth<:max_depth
                      AND instr(w.item_path,'|'||a.affected_item_id||'|')=0
                ),
                ranked AS (
                    SELECT w.*,ROW_NUMBER() OVER (PARTITION BY item_id ORDER BY depth,max_risk DESC) AS rn
                    FROM walk w WHERE depth>0
                )
                SELECT r.depth,ki.canonical_key AS affected_item,ki.display_name,
                       r.canonical_path,r.relation_path,r.relation_id_path,
                       r.relation_evidence_path,r.max_risk,r.review_actions,r.validation_actions
                FROM ranked r JOIN knowledge_item ki ON ki.item_id=r.item_id
                WHERE r.rn=1 ORDER BY r.depth,r.max_risk DESC,ki.canonical_key LIMIT :limit
                """,
                {
                    "version": version,
                    "item_key": item_key,
                    "max_depth": max_depth,
                    "limit": limit,
                    "relation_types_json": relation_types_json,
                },
            )
        )


def gaps(database: Path, version: str, limit: int = 100) -> dict[str, Any]:
    if version != TARGET_VERSION:
        raise KnowledgeBaseError(f"Production gap queries require --version {TARGET_VERSION}.")
    with contextlib.closing(connect_read_only(database)) as connection:
        questions = _rows(
            connection.execute(
                """
                SELECT q.question_key,ki.canonical_key AS primary_item,q.question_text,
                       q.uncertainty_reason,q.status_code,q.evidence_mode_code,
                       q.runtime_approval_required,q.next_action,q.priority,
                       cs.opened_at AS question_created_at,q.next_review_at,
                       COUNT(DISTINCT ir.item_relation_id) AS connected_relation_count,
                       COALESCE(MAX(rl.rank_value),0) AS max_connected_risk
                FROM open_question q
                JOIN knowledge_item ki ON ki.item_id=q.primary_item_id
                JOIN game_version gv ON gv.game_version_id=q.target_version_id
                JOIN change_set cs ON cs.change_set_id=q.created_in_change_set_id
                LEFT JOIN item_relation ir ON ir.is_current=1 AND
                    (ir.source_item_id=q.primary_item_id OR ir.target_item_id=q.primary_item_id)
                LEFT JOIN risk_level rl ON rl.risk_level_id=ir.risk_level_id
                WHERE gv.version_label=? AND q.status_code NOT IN ('resolved','wont_fix')
                GROUP BY q.question_id
                ORDER BY q.priority DESC,max_connected_risk DESC,q.question_key LIMIT ?
                """,
                (version, limit),
            )
        )
        reverification = _rows(
            connection.execute(
                """
                SELECT * FROM v_reverification_queue
                WHERE target_version=? AND requires_reverification=1
                ORDER BY reason_code,claim_id LIMIT ?
                """,
                (version, limit),
            )
        )
        issues = _rows(
            connection.execute(
                """
                SELECT * FROM v_open_analysis_issue ORDER BY priority DESC LIMIT ?
                """,
                (limit,),
            )
        )
        return {
            "target_version": version,
            "open_questions": questions,
            "reverification_queue": reverification,
            "analysis_issues": issues,
        }


def catalog_sources(database: Path, text: str = "", limit: int = 100) -> list[dict[str, Any]]:
    pattern = f"%{text.lower()}%"
    with contextlib.closing(connect_read_only(database)) as connection:
        return _rows(
            connection.execute(
                """
                SELECT ce.corpus_code,ce.relative_path,ce.artifact_kind,ce.file_role,
                       ce.current_hash_value,ce.current_size_bytes,ce.current_modified_at,
                       ce.availability_status,ds.schema_key,ds.row_count,ds.column_count
                FROM kb_catalog_entry ce
                LEFT JOIN dataset_schema ds ON ds.source_artifact_id=ce.current_source_artifact_id
                WHERE lower(ce.relative_path) LIKE ?
                ORDER BY ce.corpus_code,ce.relative_path LIMIT ?
                """,
                (pattern, limit),
            )
        )


def read_only_sql(database: Path, statement: str, limit: int = 1000) -> list[dict[str, Any]]:
    stripped = statement.strip().rstrip(";")
    if not re.match(r"^(SELECT|WITH|PRAGMA\s+(?:table_info|index_list|foreign_key_list))\b", stripped, re.I):
        raise KnowledgeBaseError("Only read-only SELECT/WITH and schema-inspection PRAGMA statements are allowed.")
    if ";" in stripped:
        raise KnowledgeBaseError("Multiple SQL statements are not allowed.")
    with contextlib.closing(connect_read_only(database)) as connection:
        cursor = connection.execute(stripped)
        rows = cursor.fetchmany(limit + 1)
        if len(rows) > limit:
            raise KnowledgeBaseError(f"Query exceeded the row limit of {limit}; add a narrower predicate.")
        return [dict(row) for row in rows]
