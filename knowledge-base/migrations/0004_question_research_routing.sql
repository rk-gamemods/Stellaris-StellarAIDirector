-- Separate question workflow state from the evidence route needed to answer it.
-- Applied transactionally by tools/stellaris_knowledge_base/migrations.py.

ALTER TABLE open_question ADD COLUMN evidence_mode_code TEXT NOT NULL DEFAULT 'static'
    CHECK (evidence_mode_code IN ('static','runtime','tooling','mixed'));

ALTER TABLE open_question ADD COLUMN runtime_approval_required INTEGER NOT NULL DEFAULT 0
    CHECK (runtime_approval_required IN (0,1));

ALTER TABLE open_question ADD COLUMN next_action TEXT;

CREATE INDEX IF NOT EXISTS idx_open_question_evidence_route
    ON open_question(evidence_mode_code, status_code, priority DESC, target_version_id);

INSERT OR REPLACE INTO schema_metadata(metadata_key, metadata_value, description) VALUES
('production_extension_revision', '4', 'Adds explicit static/runtime/tooling research routing to open questions.'),
('question_routing_contract', 'workflow_status+evidence_mode+runtime_approval', 'Keeps question state distinct from the evidence route required to resolve it.');

PRAGMA user_version = 4;

INSERT INTO kb_migration(migration_version, migration_name, script_sha256)
VALUES (4, 'question_research_routing', '{{MIGRATION_SHA256}}');
