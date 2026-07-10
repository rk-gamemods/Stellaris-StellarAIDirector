from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from stellaris_knowledge_base.db import (  # noqa: E402
    APPLICATION_ID,
    USER_VERSION,
    KnowledgeBaseError,
    connect_read_only,
    connect_writer,
    exclusive_maintenance_barrier,
    exclusive_writer_lock,
    lock_status,
    online_backup,
    validate_database,
)
from stellaris_knowledge_base.catalog import _register_manifest  # noqa: E402
from stellaris_knowledge_base.migrations import (  # noqa: E402
    BOOTSTRAP_PATH,
    PRODUCTION_MIGRATION_PATH,
    SCHEMA_PATH,
    _migration_sql,
    create_seeded_database,
    migrate_database,
)
from stellaris_knowledge_base.packets import apply_packet, dry_run_packet, load_packet  # noqa: E402
from stellaris_knowledge_base.queries import dossier, gaps, impact  # noqa: E402
from stellaris_knowledge_base.structured import profile_structured_file  # noqa: E402


class KnowledgeBaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.database = self.root / "kb.sqlite3"
        create_seeded_database(self.database)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA recursive_triggers=ON")
        return connection

    def add_catalog_fixture(self) -> None:
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            cursor = connection.execute(
                """
                INSERT INTO change_set(
                    change_set_key,title,purpose,actor_id,state,opened_at,transaction_note
                ) VALUES ('fixture:catalog','Fixture catalog','Test packet evidence.',5,'open',
                          '2026-07-10T00:00:01Z','test')
                """
            )
            change_set_id = int(cursor.lastrowid)
            evidence_type_id = connection.execute(
                "SELECT evidence_source_type_id FROM evidence_source_type WHERE type_code='repository'"
            ).fetchone()[0]
            cursor = connection.execute(
                """
                INSERT INTO source_system(
                    system_key,system_name,evidence_source_type_id,canonical_root,access_mode,
                    authoritative_for,retrieval_instructions,is_local_only,created_in_change_set_id
                ) VALUES ('fixture-system','Fixture',?,'fixture','filesystem','tests','exact path',1,?)
                """,
                (evidence_type_id, change_set_id),
            )
            source_system_id = int(cursor.lastrowid)
            cursor = connection.execute(
                """
                INSERT INTO source_root(
                    root_key,root_kind,canonical_path,availability_status,authoritative_for,
                    created_in_change_set_id
                ) VALUES ('fixture-root','research','fixture','available','tests',?)
                """,
                (change_set_id,),
            )
            source_root_id = int(cursor.lastrowid)
            cursor = connection.execute(
                """
                INSERT INTO source_artifact(
                    source_system_id,source_root_id,stable_key,artifact_kind,title,uri_or_path,
                    repository_relative_path,content_hash_algorithm,content_hash_value,
                    file_size_bytes,availability_status,created_in_change_set_id
                ) VALUES (?,?,'fixture-artifact','documentation','Fixture','fixture.md','fixture.md',
                          'sha256','abc',3,'available',?)
                """,
                (source_system_id, source_root_id, change_set_id),
            )
            artifact_id = int(cursor.lastrowid)
            connection.execute(
                """
                INSERT INTO kb_catalog_entry(
                    source_system_id,corpus_code,relative_path,artifact_kind,file_role,
                    current_source_artifact_id,current_hash_algorithm,current_hash_value,
                    current_size_bytes,availability_status,first_seen_at,last_seen_at,
                    created_in_change_set_id
                ) VALUES (?,'repo','fixture.md','documentation','documentation',?,'sha256','abc',3,
                          'available','2026-07-10T00:00:01Z','2026-07-10T00:00:01Z',?)
                """,
                (source_system_id, artifact_id, change_set_id),
            )
            connection.execute(
                "UPDATE change_set SET state='committed',committed_at='2026-07-10T00:00:02Z' WHERE change_set_id=?",
                (change_set_id,),
            )
            connection.commit()
        finally:
            connection.close()

    def test_production_bootstrap_has_no_demo_claims(self) -> None:
        connection = self.connect()
        try:
            self.assertEqual(APPLICATION_ID, connection.execute("PRAGMA application_id").fetchone()[0])
            self.assertEqual(USER_VERSION, connection.execute("PRAGMA user_version").fetchone()[0])
            self.assertEqual(0, connection.execute("SELECT COUNT(*) FROM claim").fetchone()[0])
            self.assertEqual(0, connection.execute("SELECT COUNT(*) FROM source_artifact").fetchone()[0])
            self.assertEqual(
                [("4.4.4",)],
                connection.execute(
                    "SELECT version_label FROM game_version WHERE is_primary_target=1"
                ).fetchall(),
            )
        finally:
            connection.close()

    def test_full_validation_passes(self) -> None:
        result = validate_database(self.database, full=True)
        self.assertTrue(result["ok"], result)

    def test_read_only_connection_refuses_writes(self) -> None:
        connection = connect_read_only(self.database)
        try:
            with self.assertRaises(sqlite3.OperationalError):
                connection.execute("INSERT INTO actor(actor_key,display_name,actor_type) VALUES ('x','x','tool')")
        finally:
            connection.close()

    def test_closed_change_set_cannot_create_item(self) -> None:
        connection = self.connect()
        try:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO knowledge_item(
                        item_type_id,canonical_key,display_name,summary,lifecycle_state_id,
                        created_by_actor_id,created_in_change_set_id
                    ) VALUES (17,'test:closed','Closed','Should fail',1,5,1)
                    """
                )
        finally:
            connection.close()

    def test_change_set_state_timestamp_guard(self) -> None:
        connection = self.connect()
        try:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO change_set(
                        change_set_key,title,purpose,actor_id,state,opened_at,committed_at
                    ) VALUES ('bad-state','Bad','Bad',5,'open','2026-07-10T00:00:00Z',
                              '2026-07-10T00:00:00Z')
                    """
                )
        finally:
            connection.close()

    def test_dataset_locator_must_match_artifact(self) -> None:
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            cursor = connection.execute(
                """
                INSERT INTO change_set(change_set_key,title,purpose,actor_id,state,opened_at)
                VALUES ('fixture:mismatch','Fixture','Test mismatch',5,'open','2026-07-10T00:00:00Z')
                """
            )
            change_set_id = int(cursor.lastrowid)
            evidence_type_id = connection.execute(
                "SELECT evidence_source_type_id FROM evidence_source_type WHERE type_code='repository'"
            ).fetchone()[0]
            system_id = connection.execute(
                """
                INSERT INTO source_system(system_key,system_name,evidence_source_type_id,
                    canonical_root,access_mode,authoritative_for,retrieval_instructions,
                    is_local_only,created_in_change_set_id)
                VALUES ('mismatch-system','Mismatch',?,'x','filesystem','test','test',1,?)
                """,
                (evidence_type_id, change_set_id),
            ).lastrowid
            artifacts = []
            for key in ("a", "b"):
                artifacts.append(
                    connection.execute(
                        """
                        INSERT INTO source_artifact(
                            source_system_id,stable_key,artifact_kind,title,uri_or_path,
                            availability_status,created_in_change_set_id
                        ) VALUES (?,?, 'dataset', ?, ?, 'available', ?)
                        """,
                        (system_id, key, key, key, change_set_id),
                    ).lastrowid
                )
            schema_id = connection.execute(
                """
                INSERT INTO dataset_schema(
                    source_artifact_id,schema_key,schema_version,format_code,has_header,
                    is_authoritative_external,storage_policy,created_in_change_set_id
                ) VALUES (?,'fixture','1','csv',1,1,'locator_only',?)
                """,
                (artifacts[0], change_set_id),
            ).lastrowid
            locator_type_id = connection.execute(
                "SELECT locator_type_id FROM locator_type WHERE type_code='dataset_record'"
            ).fetchone()[0]
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO evidence_locator(
                        source_artifact_id,dataset_schema_id,locator_type_id,stable_locator_key,
                        label,evidence_summary,created_by_actor_id,created_in_change_set_id
                    ) VALUES (?,?,?,'bad','bad','bad',5,?)
                    """,
                    (artifacts[1], schema_id, locator_type_id, change_set_id),
                )
            connection.rollback()
        finally:
            connection.close()

    def test_exclusive_writer_lock(self) -> None:
        lock = self.root / "writer.lock"
        with exclusive_writer_lock("outer", lock):
            with self.assertRaises(KnowledgeBaseError):
                with exclusive_writer_lock("inner", lock):
                    pass
        self.assertTrue(lock.exists())
        self.assertFalse(lock_status(lock)["active"])

    def test_os_writer_lock_recovers_after_process_exit(self) -> None:
        lock = self.root / "crash-recovery.lock"
        code = (
            "import os,sys; from pathlib import Path; "
            f"sys.path.insert(0,{str(TOOLS_ROOT)!r}); "
            "from stellaris_knowledge_base.db import exclusive_writer_lock; "
            f"ctx=exclusive_writer_lock('crash',Path({str(lock)!r})); "
            "ctx.__enter__(); os._exit(0)"
        )
        completed = subprocess.run([sys.executable, "-c", code], check=False)
        self.assertEqual(0, completed.returncode)
        with exclusive_writer_lock("recovered", lock):
            self.assertTrue(lock_status(lock)["active"])
        self.assertFalse(lock_status(lock)["active"])

    def test_online_backup_round_trip(self) -> None:
        output = self.root / "backup.sqlite3"
        result = online_backup(self.database, output)
        self.assertEqual(str(output.resolve()), result["path"])
        self.assertTrue(validate_database(output, full=True)["ok"])
        self.assertEqual(str(output.resolve()), result["validation"]["database"])

    def test_custom_database_default_backup_stays_disposable(self) -> None:
        result = online_backup(self.database)
        output = Path(result["path"])
        self.assertEqual((self.database.parent / "backups").resolve(), output.parent)
        self.assertTrue(output.is_file())

    def test_connect_writer_refuses_missing_database(self) -> None:
        with self.assertRaises(KnowledgeBaseError):
            connect_writer(self.root / "missing.sqlite3")

    def test_full_validation_detects_deleted_fts_index(self) -> None:
        connection = self.connect()
        try:
            change_set_id = connection.execute(
                """
                INSERT INTO change_set(change_set_key,title,purpose,actor_id,state,opened_at)
                VALUES ('fixture:fts-corruption','FTS fixture','Test FTS validation',5,'open',
                        '2026-07-10T00:00:00Z')
                """
            ).lastrowid
            connection.execute(
                """
                INSERT INTO knowledge_item(
                    item_type_id,canonical_key,display_name,summary,lifecycle_state_id,
                    created_by_actor_id,created_in_change_set_id
                ) VALUES (3,'subsystem:fts-fixture','FTS fixture','Searchable fixture',1,5,?)
                """,
                (change_set_id,),
            )
            connection.execute(
                "UPDATE change_set SET state='committed',committed_at='2026-07-10T00:00:01Z' "
                "WHERE change_set_id=?",
                (change_set_id,),
            )
            connection.commit()
            row = connection.execute(
                "SELECT item_id,canonical_key,display_name,summary FROM knowledge_item LIMIT 1"
            ).fetchone()
            connection.execute(
                """
                INSERT INTO item_fts(item_fts,rowid,canonical_key,display_name,summary)
                VALUES ('delete',?,?,?,?)
                """,
                row,
            )
            connection.commit()
        finally:
            connection.close()
        validation = validate_database(self.database, full=True)
        self.assertFalse(validation["ok"])
        self.assertTrue(
            "fts_shadow_mismatch" in validation["problems"]
            or "fts5_integrity_check" in validation["problems"]
        )

    def test_v3_backup_and_migration_path(self) -> None:
        old_database = self.root / "v3.sqlite3"
        connection = sqlite3.connect(old_database)
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
            connection.executescript(BOOTSTRAP_PATH.read_text(encoding="utf-8"))
            connection.executescript(_migration_sql(PRODUCTION_MIGRATION_PATH))
        finally:
            connection.close()
        old_backup = self.root / "v3-backup.sqlite3"
        backup = online_backup(
            old_database,
            old_backup,
            expected_user_version=3,
        )
        self.assertEqual(3, backup["validation"]["user_version"])
        self.assertEqual("migrated", migrate_database(old_database)["result"])
        self.assertTrue(validate_database(old_database, full=True)["ok"])

    def test_maintenance_barrier_allows_readers_and_excludes_restore(self) -> None:
        first = connect_read_only(self.database)
        second = connect_read_only(self.database)
        try:
            with self.assertRaises(KnowledgeBaseError):
                with exclusive_maintenance_barrier(self.database):
                    pass
        finally:
            first.close()
            second.close()
        with exclusive_maintenance_barrier(self.database):
            with self.assertRaises(KnowledgeBaseError):
                connect_read_only(self.database)

    def test_dataset_manifest_registration_is_bound_and_idempotent(self) -> None:
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            change_set_id = connection.execute(
                """
                INSERT INTO change_set(change_set_key,title,purpose,actor_id,state,opened_at)
                VALUES ('fixture:manifest','Manifest','Manifest binding test',5,'open',
                        '2026-07-10T00:00:00Z')
                """
            ).lastrowid
            rows = [
                {
                    "dataset": "fixture_dataset",
                    "file": "fixture.csv",
                    "fingerprint": "sha256:deadbeef",
                    "rows": 2,
                    "columns": 3,
                    "indexed_at": "2026-07-10T00:00:00Z",
                }
            ]
            _register_manifest(
                connection,
                rows=rows,
                change_set_id=change_set_id,
                observed_at="2026-07-10T00:00:01Z",
            )
            _register_manifest(
                connection,
                rows=rows,
                change_set_id=change_set_id,
                observed_at="2026-07-10T00:00:02Z",
            )
            self.assertEqual(
                1,
                connection.execute(
                    "SELECT COUNT(*) FROM kb_external_dataset_handle WHERE dataset_handle='fixture_dataset'"
                ).fetchone()[0],
            )
            connection.rollback()
        finally:
            connection.close()

    def test_structured_profile_detects_schema_and_key(self) -> None:
        path = self.root / "data.csv"
        path.write_text("record_key,count,enabled\na,1,true\nb,2,false\n", encoding="utf-8")
        profile = profile_structured_file(path)
        self.assertEqual(2, profile.row_count)
        self.assertEqual(["record_key"], profile.stable_key_columns)
        self.assertEqual(["identifier", "integer", "boolean"], [c.logical_type for c in profile.columns])

    def test_packet_is_version_guarded_and_idempotent(self) -> None:
        self.add_catalog_fixture()
        packet_path = self.root / "packet.json"
        packet = {
            "packet_version": 1,
            "packet_key": "test-packet",
            "target_version": "4.4.4",
            "purpose": "Exercise the packet transaction.",
            "items": [
                {
                    "key": "subsystem:test-kb",
                    "type": "subsystem",
                    "display_name": "Test KB subsystem",
                    "summary": "Test item.",
                },
                {
                    "key": "field:test-kb",
                    "type": "field",
                    "display_name": "Test KB field",
                    "summary": "Test field item.",
                }
            ],
            "evidence": [
                {
                    "key": "fixture-note",
                    "corpus": "repo",
                    "relative_path": "fixture.md",
                    "locator_type": "note_section",
                    "section_title": "Fixture",
                    "summary": "Fixture evidence.",
                    "retrieval_instructions": "Open the fixture.",
                }
            ],
            "claims": [
                {
                    "key": "claim:test-kb",
                    "type": "structure",
                    "primary_item": "subsystem:test-kb",
                    "statement": "The test packet creates one traceable claim.",
                    "state": "verified",
                    "confidence": "high",
                    "basis_summary": "Fixture evidence.",
                    "evidence": [
                        {
                            "key": "fixture-note",
                            "stance": "supports",
                            "directness": 5,
                            "strength": 5,
                            "interpretation": "Direct fixture.",
                        }
                    ],
                }
            ],
            "questions": [
                {
                    "key": "question:test-kb-static",
                    "primary_item": "subsystem:test-kb",
                    "question": "What additional static evidence should be cataloged?",
                    "uncertainty_reason": "The fixture intentionally contains one evidence item.",
                    "status": "open",
                    "evidence_mode": "static",
                    "runtime_approval_required": False,
                    "priority": 50,
                    "next_action": "Inspect another exact fixture without launching the game.",
                    "evidence": ["fixture-note"],
                }
            ],
            "relations": [
                {
                    "key": "relation:test-field-of-subsystem",
                    "source": "field:test-kb",
                    "type": "field_of",
                    "target": "subsystem:test-kb",
                    "confidence": "high",
                    "risk": "medium",
                    "source_claim": "claim:test-kb",
                    "rationale": "Fixture relation.",
                    "impact_explanation": "Fixture impact.",
                    "review_action": "Review fixture.",
                    "validation_action": "Validate fixture.",
                    "evidence": ["fixture-note"],
                }
            ],
        }
        packet_path.write_text(json.dumps(packet), encoding="utf-8")
        preview = dry_run_packet(self.database, packet_path)
        self.assertFalse(preview["already_applied"])
        with exclusive_writer_lock("serialized packet test"):
            first = apply_packet(self.database, packet_path, lock_held=True)
        self.assertEqual("committed", first["result"])
        second = apply_packet(self.database, packet_path)
        self.assertEqual("no_op", second["result"])
        connection = self.connect()
        try:
            route = connection.execute(
                "SELECT status_code,evidence_mode_code,runtime_approval_required "
                "FROM open_question WHERE question_key='question:test-kb-static'"
            ).fetchone()
            self.assertEqual(("open", "static", 0), route)
        finally:
            connection.close()
        item_dossier = dossier(self.database, "subsystem:test-kb", "4.4.4")
        self.assertEqual("sha256", item_dossier["evidence"][0]["content_hash_algorithm"])
        paths = impact(
            self.database,
            "field:test-kb",
            "4.4.4",
            max_depth=1,
            relation_types=["field_of"],
        )
        self.assertEqual("field:test-kb > subsystem:test-kb", paths[0]["canonical_path"])
        self.assertIn("fixture-note", paths[0]["relation_evidence_path"])
        queue = gaps(self.database, "4.4.4")
        self.assertEqual("static", queue["open_questions"][0]["evidence_mode_code"])
        packet["target_version"] = "4.4.5"
        packet_path.write_text(json.dumps(packet), encoding="utf-8")
        with self.assertRaises(KnowledgeBaseError):
            load_packet(packet_path)

    def test_packet_rejects_conflated_question_status_and_runtime_without_guard(self) -> None:
        packet_path = self.root / "bad-question-packet.json"
        packet = {
            "packet_version": 1,
            "packet_key": "bad-question-packet",
            "target_version": "4.4.4",
            "purpose": "Exercise question routing validation.",
            "questions": [
                {
                    "key": "question:bad",
                    "primary_item": "subsystem:bad",
                    "question": "Does this require runtime proof?",
                    "uncertainty_reason": "Deliberately malformed fixture.",
                    "status": "open_runtime",
                    "evidence_mode": "runtime",
                    "runtime_approval_required": False,
                    "next_action": "Wait for explicit approval.",
                }
            ],
        }
        packet_path.write_text(json.dumps(packet), encoding="utf-8")
        with self.assertRaisesRegex(KnowledgeBaseError, "unsupported workflow status"):
            load_packet(packet_path)


if __name__ == "__main__":
    unittest.main()
