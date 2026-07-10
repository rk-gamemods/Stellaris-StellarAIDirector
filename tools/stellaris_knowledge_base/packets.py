from __future__ import annotations

import contextlib
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .db import (
    SEMANTIC_CHECKS,
    KnowledgeBaseError,
    connect_read_only,
    connect_writer,
    exclusive_writer_lock,
    utc_now,
    writer_lock_path,
)
from .paths import TARGET_VERSION


PACKET_VERSION = 1
QUESTION_STATUSES = {"open", "investigating", "blocked", "resolved", "wont_fix"}
EVIDENCE_MODES = {"static", "runtime", "tooling", "mixed"}


@dataclass(frozen=True)
class PreparedPacket:
    source_path: Path
    packet: dict[str, Any]
    packet_sha256: str


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KnowledgeBaseError(f"{label} must be a non-empty string.")
    return value


def _validate_packet_structure(packet: dict[str, Any]) -> None:
    for field in ("packet_key", "target_version", "purpose"):
        _nonempty(packet.get(field), field)
    for section in ("items", "evidence", "claims", "questions", "relations"):
        if not isinstance(packet.get(section, []), list):
            raise KnowledgeBaseError(f"{section} must be a JSON array.")
    actor = packet.get("actor", {})
    if not isinstance(actor, dict):
        raise KnowledgeBaseError("actor must be a JSON object.")
    if actor.get("type", "ai_agent") not in {"human", "ai_agent", "tool", "system"}:
        raise KnowledgeBaseError("actor.type must be human, ai_agent, tool, or system.")

    required_fields = {
        "items": {"key", "type"},
        "evidence": {"key", "summary", "retrieval_instructions"},
        "claims": {
            "key",
            "type",
            "primary_item",
            "statement",
            "state",
            "confidence",
            "basis_summary",
        },
        "questions": {"key", "primary_item", "question", "uncertainty_reason"},
        "relations": {
            "key",
            "source",
            "type",
            "target",
            "rationale",
            "impact_explanation",
        },
    }
    keys: dict[str, set[str]] = {}
    for section, required in required_fields.items():
        seen: set[str] = set()
        for index, entry in enumerate(packet.get(section, [])):
            if not isinstance(entry, dict):
                raise KnowledgeBaseError(f"{section}[{index}] must be a JSON object.")
            missing = sorted(required - entry.keys())
            if missing:
                raise KnowledgeBaseError(
                    f"{section}[{index}] is missing keys: {', '.join(missing)}"
                )
            key = _nonempty(entry.get("key"), f"{section}[{index}].key")
            if key in seen:
                raise KnowledgeBaseError(f"Duplicate {section} key: {key}")
            seen.add(key)
            for field in required - {"key"}:
                _nonempty(entry.get(field), f"{section}[{index}].{field}")
        keys[section] = seen

    for evidence in packet.get("evidence", []):
        if not evidence.get("relative_path") and not evidence.get("dataset_handle"):
            raise KnowledgeBaseError(
                f"Evidence {evidence['key']} requires relative_path or dataset_handle."
            )
    for claim in packet.get("claims", []):
        links = claim.get("evidence", [])
        if not isinstance(links, list):
            raise KnowledgeBaseError(f"Claim {claim['key']} evidence must be an array.")
        for link in links:
            if not isinstance(link, dict) or link.get("key") not in keys["evidence"]:
                raise KnowledgeBaseError(
                    f"Claim {claim['key']} references evidence not defined in this packet."
                )
            _nonempty(link.get("interpretation"), f"claim {claim['key']} evidence interpretation")
            for rank_name in ("directness", "strength"):
                rank = link.get(rank_name, 4)
                if not isinstance(rank, int) or not 1 <= rank <= 5:
                    raise KnowledgeBaseError(
                        f"Claim {claim['key']} {rank_name} must be an integer from 1 to 5."
                    )
    for question in packet.get("questions", []):
        status = question.get("status", "open")
        mode = question.get("evidence_mode", "static")
        if status not in QUESTION_STATUSES:
            raise KnowledgeBaseError(
                f"Question {question['key']} has unsupported workflow status {status}."
            )
        if mode not in EVIDENCE_MODES:
            raise KnowledgeBaseError(
                f"Question {question['key']} has unsupported evidence_mode {mode}."
            )
        runtime_approval = question.get(
            "runtime_approval_required", mode in {"runtime", "mixed"}
        )
        if runtime_approval not in {True, False, 0, 1}:
            raise KnowledgeBaseError(
                f"Question {question['key']} runtime_approval_required must be boolean."
            )
        if mode in {"runtime", "mixed"} and not bool(runtime_approval):
            raise KnowledgeBaseError(
                f"Question {question['key']} requires runtime_approval_required=true."
            )
        priority = question.get("priority", 50)
        if not isinstance(priority, int) or not 1 <= priority <= 100:
            raise KnowledgeBaseError(
                f"Question {question['key']} priority must be an integer from 1 to 100."
            )
        if status in {"open", "investigating", "blocked"}:
            _nonempty(question.get("next_action"), f"question {question['key']}.next_action")
        evidence_keys = question.get("evidence", [])
        if not isinstance(evidence_keys, list) or any(
            key not in keys["evidence"] for key in evidence_keys
        ):
            raise KnowledgeBaseError(
                f"Question {question['key']} references evidence not defined in this packet."
            )
        resolution_claim = question.get("resolution_claim")
        if resolution_claim is not None and resolution_claim not in keys["claims"]:
            raise KnowledgeBaseError(
                f"Question {question['key']} resolution_claim must be defined in this packet."
            )
    for relation in packet.get("relations", []):
        evidence_keys = relation.get("evidence", [])
        if not isinstance(evidence_keys, list) or any(
            key not in keys["evidence"] for key in evidence_keys
        ):
            raise KnowledgeBaseError(
                f"Relation {relation['key']} references evidence not defined in this packet."
            )
        source_claim = relation.get("source_claim")
        if source_claim is not None and source_claim not in keys["claims"]:
            raise KnowledgeBaseError(
                f"Relation {relation['key']} source_claim must be defined in this packet."
            )


def _canonical_payload(packet: dict[str, Any]) -> bytes:
    return json.dumps(packet, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _id(connection, table: str, key_column: str, value: str, id_column: str | None = None) -> int:
    id_column = id_column or f"{table}_id"
    row = connection.execute(
        f"SELECT {id_column} FROM {table} WHERE {key_column}=?", (value,)
    ).fetchone()
    if row is None:
        raise KnowledgeBaseError(f"Missing {table}.{key_column}={value}")
    return int(row[0])


def prepare_packet(path: Path) -> PreparedPacket:
    source_path = path.expanduser().resolve()
    packet = json.loads(source_path.read_bytes().decode("utf-8"))
    if not isinstance(packet, dict):
        raise KnowledgeBaseError("Knowledge packet must be a JSON object.")
    required = {"packet_version", "packet_key", "target_version", "purpose"}
    missing = sorted(required - packet.keys())
    if missing:
        raise KnowledgeBaseError(f"Knowledge packet is missing keys: {', '.join(missing)}")
    if packet["packet_version"] != PACKET_VERSION:
        raise KnowledgeBaseError(
            f"Unsupported packet_version={packet['packet_version']}; expected {PACKET_VERSION}."
        )
    if packet["target_version"] != TARGET_VERSION:
        raise KnowledgeBaseError(
            f"Packet target {packet['target_version']} cannot be promoted into the {TARGET_VERSION} baseline."
        )
    _validate_packet_structure(packet)
    return PreparedPacket(
        source_path=source_path,
        packet=packet,
        packet_sha256=hashlib.sha256(_canonical_payload(packet)).hexdigest(),
    )


def load_packet(path: Path) -> dict[str, Any]:
    return prepare_packet(path).packet


def _resolve_artifact(connection, evidence: dict[str, Any]) -> tuple[int, int | None]:
    corpus = str(evidence.get("corpus", "repo"))
    relative_path = str(evidence.get("relative_path", ""))
    if relative_path:
        row = connection.execute(
            """
            SELECT ce.current_source_artifact_id,ds.dataset_schema_id
            FROM kb_catalog_entry ce
            LEFT JOIN dataset_schema ds ON ds.source_artifact_id=ce.current_source_artifact_id
            WHERE ce.corpus_code=? AND ce.relative_path=? AND ce.availability_status='available'
            ORDER BY ds.dataset_schema_id DESC LIMIT 1
            """,
            (corpus, relative_path),
        ).fetchone()
        if row:
            return int(row[0]), int(row[1]) if row[1] is not None else None
    dataset_handle = evidence.get("dataset_handle")
    if dataset_handle:
        row = connection.execute(
            """
            SELECT source_artifact_id,dataset_schema_id FROM kb_external_dataset_handle
            WHERE provider_code='jdatamunch' AND dataset_handle=? AND is_current=1
            """,
            (dataset_handle,),
        ).fetchone()
        if row and row[0] is not None:
            return int(row[0]), int(row[1]) if row[1] is not None else None
    raise KnowledgeBaseError(
        f"Evidence {evidence.get('key','<unnamed>')} does not resolve to a current catalog artifact."
    )


def dry_run_packet(
    database: Path,
    packet_path: Path,
    *,
    prepared: PreparedPacket | None = None,
) -> dict[str, Any]:
    prepared = prepared or prepare_packet(packet_path)
    if prepared.source_path != packet_path.expanduser().resolve():
        raise KnowledgeBaseError("Prepared packet path does not match the requested source path.")
    packet = prepared.packet
    digest = prepared.packet_sha256
    with contextlib.closing(connect_read_only(database)) as connection:
        already = connection.execute(
            "SELECT packet_key FROM kb_packet_application WHERE packet_sha256=?", (digest,)
        ).fetchone()
        collision = connection.execute(
            "SELECT packet_sha256 FROM kb_packet_application WHERE packet_key=?",
            (packet["packet_key"],),
        ).fetchone()
        resolved = []
        for evidence in packet.get("evidence", []):
            artifact_id, schema_id = _resolve_artifact(connection, evidence)
            if evidence.get("use_dataset_schema", False) and schema_id is None:
                raise KnowledgeBaseError(
                    f"Evidence {evidence['key']} requires a dataset schema, but none is registered."
                )
            _id(
                connection,
                "locator_type",
                "type_code",
                evidence.get("locator_type", "note_section"),
            )
            resolved.append(
                {
                    "key": evidence["key"],
                    "source_artifact_id": artifact_id,
                    "dataset_schema_id": schema_id,
                }
            )
        for item in packet.get("items", []):
            expected_type_id = _id(connection, "item_type", "type_code", item["type"])
            existing_item = connection.execute(
                "SELECT item_type_id FROM knowledge_item WHERE canonical_key=?",
                (item["key"],),
            ).fetchone()
            if existing_item and int(existing_item[0]) != expected_type_id:
                raise KnowledgeBaseError(
                    f"Item {item['key']} already exists with a different item type."
                )
        for claim in packet.get("claims", []):
            _id(connection, "claim_type", "type_code", claim["type"])
            _id(connection, "assessment_state", "state_code", claim["state"])
            _id(connection, "confidence_level", "confidence_code", claim["confidence"])
            if claim["primary_item"] not in {item["key"] for item in packet.get("items", [])}:
                _id(
                    connection,
                    "knowledge_item",
                    "canonical_key",
                    claim["primary_item"],
                    "item_id",
                )
            for link in claim.get("evidence", []):
                _id(
                    connection,
                    "evidence_stance",
                    "stance_code",
                    link.get("stance", "supports"),
                )
        packet_item_keys = {item["key"] for item in packet.get("items", [])}
        for question in packet.get("questions", []):
            if question["primary_item"] not in packet_item_keys:
                _id(
                    connection,
                    "knowledge_item",
                    "canonical_key",
                    question["primary_item"],
                    "item_id",
                )
        for relation in packet.get("relations", []):
            for item_key in (relation["source"], relation["target"]):
                if item_key not in packet_item_keys:
                    _id(
                        connection,
                        "knowledge_item",
                        "canonical_key",
                        item_key,
                        "item_id",
                    )
            _id(connection, "relation_type", "type_code", relation["type"])
            _id(
                connection,
                "confidence_level",
                "confidence_code",
                relation.get("confidence", "medium"),
            )
            _id(
                connection,
                "risk_level",
                "risk_code",
                relation.get("risk", "medium"),
            )
        if collision and collision[0] != digest:
            raise KnowledgeBaseError(
                f"packet_key {packet['packet_key']} was already used with a different payload."
            )
        return {
            "packet_key": packet["packet_key"],
            "packet_sha256": digest,
            "already_applied": bool(already),
            "target_version": packet["target_version"],
            "counts": {
                key: len(packet.get(key, []))
                for key in ("items", "evidence", "claims", "questions", "relations")
            },
            "resolved_evidence": resolved,
        }


def _ensure_actor(connection, actor: dict[str, Any]) -> int:
    key = str(actor.get("key", "ai:codex"))
    display_name = str(actor.get("display_name", "Codex"))
    actor_type = str(actor.get("type", "ai_agent"))
    if actor_type not in {"human", "ai_agent", "tool", "system"}:
        raise KnowledgeBaseError(f"Unsupported actor type: {actor_type}")
    connection.execute(
        """
        INSERT INTO actor(actor_key,display_name,actor_type,external_identifier,notes)
        VALUES (?,?,?,NULL,'Registered by a knowledge packet.')
        ON CONFLICT(actor_key) DO UPDATE SET display_name=excluded.display_name
        """,
        (key, display_name, actor_type),
    )
    return _id(connection, "actor", "actor_key", key, "actor_id")


def _ensure_item(connection, item: dict[str, Any], change_set_id: int, actor_id: int) -> int:
    item_type_id = _id(connection, "item_type", "type_code", item["type"])
    lifecycle_id = _id(connection, "lifecycle_state", "state_code", "active")
    connection.execute(
        """
        INSERT INTO knowledge_item(
            item_type_id,canonical_key,display_name,summary,lifecycle_state_id,
            created_by_actor_id,created_in_change_set_id
        ) VALUES (?,?,?,?,?,?,?)
        ON CONFLICT(canonical_key) DO UPDATE SET
            display_name=excluded.display_name,summary=excluded.summary,
            updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now'),
            updated_in_change_set_id=excluded.created_in_change_set_id
        """,
        (
            item_type_id,
            item["key"],
            item.get("display_name", item["key"]),
            item.get("summary", "Knowledge-packet item."),
            lifecycle_id,
            actor_id,
            change_set_id,
        ),
    )
    return _id(connection, "knowledge_item", "canonical_key", item["key"], "item_id")


def apply_packet(
    database: Path,
    packet_path: Path,
    *,
    lock_held: bool = False,
    prepared: PreparedPacket | None = None,
) -> dict[str, Any]:
    prepared = prepared or prepare_packet(packet_path)
    packet = prepared.packet
    lock = (
        contextlib.nullcontext()
        if lock_held
        else exclusive_writer_lock(
            f"apply knowledge packet {packet['packet_key']}", writer_lock_path(database)
        )
    )
    with lock:
        preview = dry_run_packet(database, packet_path, prepared=prepared)
        if preview["already_applied"]:
            return {**preview, "result": "no_op"}
        applied_at = utc_now()
        connection = connect_writer(database)
        try:
            connection.execute("BEGIN IMMEDIATE")
            collision = connection.execute(
                "SELECT packet_sha256 FROM kb_packet_application WHERE packet_key=?",
                (packet["packet_key"],),
            ).fetchone()
            if collision:
                if collision[0] == preview["packet_sha256"]:
                    connection.rollback()
                    return {**preview, "result": "no_op"}
                raise KnowledgeBaseError("Packet key collision after acquiring the writer lock.")
            actor_id = _ensure_actor(connection, packet.get("actor", {}))
            target_version_id = _id(
                connection, "game_version", "version_label", packet["target_version"]
            )
            version_span_id = _id(
                connection, "version_span", "span_code", f"v{packet['target_version']}"
            )
            cursor = connection.execute(
                """
                INSERT INTO change_set(
                    change_set_key,title,purpose,actor_id,state,opened_at,repository_commit,
                    transaction_note
                ) VALUES (?,?,?,?,'open',?,?,?)
                """,
                (
                    f"packet:{packet['packet_key']}:{preview['packet_sha256'][:12]}",
                    packet.get("title", packet["packet_key"]),
                    packet["purpose"],
                    actor_id,
                    applied_at,
                    packet.get("repository_commit"),
                    f"Canonical packet SHA-256 {preview['packet_sha256']}.",
                ),
            )
            change_set_id = int(cursor.lastrowid)
            item_ids: dict[str, int] = {}
            for item in packet.get("items", []):
                item_ids[item["key"]] = _ensure_item(connection, item, change_set_id, actor_id)
            evidence_ids: dict[str, int] = {}
            for evidence in packet.get("evidence", []):
                source_artifact_id, dataset_schema_id = _resolve_artifact(connection, evidence)
                locator_type_id = _id(
                    connection,
                    "locator_type",
                    "type_code",
                    evidence.get("locator_type", "note_section"),
                )
                stable_key = f"packet:{packet['packet_key']}:{evidence['key']}"
                cursor = connection.execute(
                    """
                    INSERT INTO evidence_locator(
                        source_artifact_id,dataset_schema_id,locator_type_id,stable_locator_key,
                        label,relative_path,line_start,line_end,section_title,
                        symbol_or_object_key,record_set,record_key,row_number,column_name,
                        json_path,query_text,excerpt,evidence_summary,retrieval_instructions,
                        created_by_actor_id,created_in_change_set_id
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        source_artifact_id,
                        dataset_schema_id if evidence.get("use_dataset_schema", False) else None,
                        locator_type_id,
                        stable_key,
                        evidence.get("label", evidence["key"]),
                        evidence.get("relative_path"),
                        evidence.get("line_start"),
                        evidence.get("line_end"),
                        evidence.get("section_title"),
                        evidence.get("symbol_or_object_key"),
                        evidence.get("record_set"),
                        evidence.get("record_key"),
                        evidence.get("row_number"),
                        evidence.get("column_name"),
                        evidence.get("json_path"),
                        evidence.get("query_text"),
                        evidence.get("excerpt"),
                        evidence["summary"],
                        evidence["retrieval_instructions"],
                        actor_id,
                        change_set_id,
                    ),
                )
                evidence_ids[evidence["key"]] = int(cursor.lastrowid)
            claim_ids: dict[str, int] = {}
            for claim in packet.get("claims", []):
                primary_item_id = item_ids.get(claim["primary_item"]) or _id(
                    connection,
                    "knowledge_item",
                    "canonical_key",
                    claim["primary_item"],
                    "item_id",
                )
                identity = connection.execute(
                    """
                    SELECT c.claim_id,c.statement,c.primary_item_id
                    FROM kb_claim_identity k JOIN claim c ON c.claim_id=k.claim_id
                    WHERE k.claim_key=?
                    """,
                    (claim["key"],),
                ).fetchone()
                if identity:
                    if identity[1] != claim["statement"] or int(identity[2]) != primary_item_id:
                        raise KnowledgeBaseError(
                            f"Claim key {claim['key']} changed its immutable statement or primary item."
                        )
                    claim_id = int(identity[0])
                else:
                    cursor = connection.execute(
                        """
                        INSERT INTO claim(
                            claim_type_id,primary_item_id,statement,context,epistemic_note,
                            supersedes_claim_id,lifecycle_state_id,created_by_actor_id,
                            created_in_change_set_id
                        ) VALUES (?,?,?,?,?,NULL,?,?,?)
                        """,
                        (
                            _id(connection, "claim_type", "type_code", claim["type"]),
                            primary_item_id,
                            claim["statement"],
                            claim.get("context"),
                            claim.get("epistemic_note"),
                            _id(connection, "lifecycle_state", "state_code", "active"),
                            actor_id,
                            change_set_id,
                        ),
                    )
                    claim_id = int(cursor.lastrowid)
                    connection.execute(
                        "INSERT INTO kb_claim_identity(claim_id,claim_key) VALUES (?,?)",
                        (claim_id, claim["key"]),
                    )
                claim_ids[claim["key"]] = claim_id
                previous = connection.execute(
                    """
                    SELECT claim_assessment_id FROM claim_assessment
                    WHERE claim_id=? AND version_span_id=? AND is_current=1
                    ORDER BY claim_assessment_id DESC LIMIT 1
                    """,
                    (claim_id, version_span_id),
                ).fetchone()
                if previous:
                    connection.execute(
                        "UPDATE claim_assessment SET is_current=0 WHERE claim_assessment_id=?",
                        (previous[0],),
                    )
                connection.execute(
                    """
                    INSERT INTO claim_assessment(
                        claim_id,version_span_id,assessment_state_id,confidence_level_id,
                        verification_run_id,execution_context_id,assessed_by_actor_id,
                        assessed_at,basis_summary,reverify_after,is_current,
                        supersedes_assessment_id,created_in_change_set_id
                    ) VALUES (?,?,?,?,NULL,NULL,?,?,?,NULL,1,?,?)
                    """,
                    (
                        claim_id,
                        version_span_id,
                        _id(connection, "assessment_state", "state_code", claim["state"]),
                        _id(connection, "confidence_level", "confidence_code", claim["confidence"]),
                        actor_id,
                        applied_at,
                        claim["basis_summary"],
                        int(previous[0]) if previous else None,
                        change_set_id,
                    ),
                )
                for link in claim.get("evidence", []):
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO claim_evidence(
                            claim_id,evidence_locator_id,evidence_stance_id,directness_rank,
                            strength_rank,verification_run_id,interpretation,created_in_change_set_id
                        ) VALUES (?,?,?,?,?,NULL,?,?)
                        """,
                        (
                            claim_id,
                            evidence_ids[link["key"]],
                            _id(connection, "evidence_stance", "stance_code", link.get("stance", "supports")),
                            int(link.get("directness", 4)),
                            int(link.get("strength", 4)),
                            link["interpretation"],
                            change_set_id,
                        ),
                    )
            for question in packet.get("questions", []):
                primary_item_id = item_ids.get(question["primary_item"]) or _id(
                    connection,
                    "knowledge_item",
                    "canonical_key",
                    question["primary_item"],
                    "item_id",
                )
                resolution_claim_id = claim_ids.get(question.get("resolution_claim"))
                existing = connection.execute(
                    "SELECT question_id,primary_item_id,question_text FROM open_question WHERE question_key=?",
                    (question["key"],),
                ).fetchone()
                status = question.get("status", "open")
                evidence_mode = question.get("evidence_mode", "static")
                runtime_approval_required = int(
                    bool(
                        question.get(
                            "runtime_approval_required",
                            evidence_mode in {"runtime", "mixed"},
                        )
                    )
                )
                closed = status in {"resolved", "wont_fix"}
                if existing:
                    question_id = int(existing[0])
                    if int(existing[1]) != primary_item_id or str(existing[2]) != question["question"]:
                        raise KnowledgeBaseError(
                            f"Question key {question['key']} changed its immutable primary item or question text."
                        )
                    connection.execute(
                        """
                        UPDATE open_question SET question_text=?,uncertainty_reason=?,
                            target_version_id=?,status_code=?,evidence_mode_code=?,
                            runtime_approval_required=?,next_action=?,priority=?,owner_actor_id=?,
                            resolution_claim_id=?,closed_in_change_set_id=? WHERE question_id=?
                        """,
                        (
                            question["question"],
                            question["uncertainty_reason"],
                            target_version_id,
                            status,
                            evidence_mode,
                            runtime_approval_required,
                            question.get("next_action"),
                            int(question.get("priority", 50)),
                            actor_id,
                            resolution_claim_id,
                            change_set_id if closed else None,
                            question_id,
                        ),
                    )
                else:
                    cursor = connection.execute(
                        """
                        INSERT INTO open_question(
                            question_key,primary_item_id,question_text,uncertainty_reason,
                            target_version_id,status_code,evidence_mode_code,
                            runtime_approval_required,next_action,priority,owner_actor_id,
                            resolution_claim_id,next_review_at,created_in_change_set_id,
                            closed_in_change_set_id
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,NULL,?,?)
                        """,
                        (
                            question["key"],
                            primary_item_id,
                            question["question"],
                            question["uncertainty_reason"],
                            target_version_id,
                            status,
                            evidence_mode,
                            runtime_approval_required,
                            question.get("next_action"),
                            int(question.get("priority", 50)),
                            actor_id,
                            resolution_claim_id,
                            change_set_id,
                            change_set_id if closed else None,
                        ),
                    )
                    question_id = int(cursor.lastrowid)
                for key in question.get("evidence", []):
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO question_evidence(
                            question_id,evidence_locator_id,relevance_code,notes
                        ) VALUES (?,?,'context','Knowledge packet evidence.')
                        """,
                        (question_id, evidence_ids[key]),
                    )
            for relation in packet.get("relations", []):
                source_item_id = item_ids.get(relation["source"]) or _id(
                    connection, "knowledge_item", "canonical_key", relation["source"], "item_id"
                )
                target_item_id = item_ids.get(relation["target"]) or _id(
                    connection, "knowledge_item", "canonical_key", relation["target"], "item_id"
                )
                relation_type_id = _id(
                    connection, "relation_type", "type_code", relation["type"]
                )
                identity = connection.execute(
                    """
                    SELECT k.item_relation_id,r.source_item_id,r.relation_type_id,
                           r.target_item_id,r.version_span_id
                    FROM kb_relation_identity k
                    JOIN item_relation r ON r.item_relation_id=k.item_relation_id
                    WHERE k.relation_key=?
                    """,
                    (relation["key"],),
                ).fetchone()
                if identity:
                    item_relation_id = int(identity[0])
                    expected_identity = (
                        source_item_id,
                        relation_type_id,
                        target_item_id,
                        version_span_id,
                    )
                    if tuple(map(int, identity[1:])) != expected_identity:
                        raise KnowledgeBaseError(
                            f"Relation key {relation['key']} changed its immutable endpoints, type, or version."
                        )
                else:
                    collision = connection.execute(
                        """
                        SELECT item_relation_id FROM item_relation
                        WHERE source_item_id=? AND relation_type_id=? AND target_item_id=?
                          AND version_span_id=? AND is_current=1
                        """,
                        (source_item_id, relation_type_id, target_item_id, version_span_id),
                    ).fetchone()
                    if collision:
                        raise KnowledgeBaseError(
                            f"Relation {relation['key']} collides with an existing current relation."
                        )
                    cursor = connection.execute(
                        """
                        INSERT INTO item_relation(
                            source_item_id,relation_type_id,target_item_id,version_span_id,
                            confidence_level_id,risk_level_id,source_claim_id,rationale,
                            impact_explanation,review_action,validation_action,is_current,
                            created_in_change_set_id,retired_in_change_set_id
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,1,?,NULL)
                        """,
                        (
                            source_item_id,
                            relation_type_id,
                            target_item_id,
                            version_span_id,
                            _id(connection, "confidence_level", "confidence_code", relation.get("confidence", "medium")),
                            _id(connection, "risk_level", "risk_code", relation.get("risk", "medium")),
                            claim_ids.get(relation.get("source_claim")),
                            relation["rationale"],
                            relation["impact_explanation"],
                            relation.get("review_action"),
                            relation.get("validation_action"),
                            change_set_id,
                        ),
                    )
                    item_relation_id = int(cursor.lastrowid)
                    connection.execute(
                        "INSERT INTO kb_relation_identity(item_relation_id,relation_key) VALUES (?,?)",
                        (item_relation_id, relation["key"]),
                    )
                for key in relation.get("evidence", []):
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO relation_evidence(
                            item_relation_id,evidence_locator_id,evidence_stance_id,
                            strength_rank,interpretation
                        ) VALUES (?,?,?,4,'Knowledge packet evidence.')
                        """,
                        (
                            item_relation_id,
                            evidence_ids[key],
                            _id(connection, "evidence_stance", "stance_code", "supports"),
                        ),
                    )
            summary = json.dumps(preview["counts"], sort_keys=True)
            connection.execute(
                """
                INSERT INTO kb_packet_application(
                    packet_sha256,packet_version,packet_key,change_set_id,applied_at,
                    target_version_id,source_path,result_summary
                ) VALUES (?,?,?,?,?,?,?,?)
                """,
                (
                    preview["packet_sha256"],
                    packet["packet_version"],
                    packet["packet_key"],
                    change_set_id,
                    applied_at,
                    target_version_id,
                    str(prepared.source_path),
                    summary,
                ),
            )
            connection.execute(
                "UPDATE change_set SET state='committed',committed_at=? WHERE change_set_id=?",
                (utc_now(), change_set_id),
            )
            if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
                raise KnowledgeBaseError("Knowledge packet introduced a foreign-key violation.")
            semantic_failures = [
                name
                for name, sql in SEMANTIC_CHECKS
                if int(connection.execute(sql).fetchone()[0]) != 0
            ]
            if semantic_failures:
                raise KnowledgeBaseError(
                    "Knowledge packet failed semantic validation: "
                    + ", ".join(semantic_failures)
                )
            connection.commit()
            return {**preview, "result": "committed", "change_set_id": change_set_id}
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
