-- Production operations and ingestion sidecars for the project-aware SKB2 schema.
-- Applied transactionally by tools/stellaris_knowledge_base/migrations.py.

CREATE TABLE IF NOT EXISTS kb_migration (
    migration_version INTEGER PRIMARY KEY,
    migration_name TEXT NOT NULL UNIQUE,
    script_sha256 TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
) STRICT;

CREATE TABLE IF NOT EXISTS kb_ingest_run (
    ingest_run_id INTEGER PRIMARY KEY,
    run_key TEXT NOT NULL UNIQUE,
    run_kind TEXT NOT NULL CHECK (run_kind IN ('install','refresh','catalog','dataset_manifest','knowledge_packet')),
    target_version_id INTEGER NOT NULL REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT,
    change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    state TEXT NOT NULL CHECK (state IN ('running','committed','aborted')),
    started_at TEXT NOT NULL,
    completed_at TEXT,
    input_summary TEXT NOT NULL,
    files_seen INTEGER NOT NULL DEFAULT 0 CHECK (files_seen >= 0),
    files_changed INTEGER NOT NULL DEFAULT 0 CHECK (files_changed >= 0),
    structured_files_profiled INTEGER NOT NULL DEFAULT 0 CHECK (structured_files_profiled >= 0),
    object_rows_loaded INTEGER NOT NULL DEFAULT 0 CHECK (object_rows_loaded >= 0),
    relation_rows_loaded INTEGER NOT NULL DEFAULT 0 CHECK (relation_rows_loaded >= 0),
    issue_count INTEGER NOT NULL DEFAULT 0 CHECK (issue_count >= 0),
    notes TEXT,
    CHECK ((state = 'committed' AND completed_at IS NOT NULL) OR state <> 'committed')
) STRICT;

CREATE INDEX IF NOT EXISTS idx_kb_ingest_run_state
    ON kb_ingest_run(state, started_at DESC);

CREATE TABLE IF NOT EXISTS kb_catalog_entry (
    catalog_entry_id INTEGER PRIMARY KEY,
    source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT,
    corpus_code TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    artifact_kind TEXT NOT NULL,
    file_role TEXT NOT NULL,
    current_source_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    current_hash_algorithm TEXT,
    current_hash_value TEXT,
    current_size_bytes INTEGER CHECK (current_size_bytes IS NULL OR current_size_bytes >= 0),
    current_modified_at TEXT,
    availability_status TEXT NOT NULL CHECK (availability_status IN ('available','missing','moved','archived','unknown')),
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    updated_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(source_system_id, corpus_code, relative_path)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_kb_catalog_entry_current_artifact
    ON kb_catalog_entry(current_source_artifact_id);
CREATE INDEX IF NOT EXISTS idx_kb_catalog_entry_lookup
    ON kb_catalog_entry(corpus_code, availability_status, relative_path);

CREATE TABLE IF NOT EXISTS kb_catalog_observation (
    ingest_run_id INTEGER NOT NULL REFERENCES kb_ingest_run(ingest_run_id) ON DELETE CASCADE,
    catalog_entry_id INTEGER NOT NULL REFERENCES kb_catalog_entry(catalog_entry_id) ON DELETE RESTRICT,
    source_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT,
    is_present INTEGER NOT NULL CHECK (is_present IN (0,1)),
    content_hash_algorithm TEXT,
    content_hash_value TEXT,
    file_size_bytes INTEGER CHECK (file_size_bytes IS NULL OR file_size_bytes >= 0),
    modified_at TEXT,
    observed_at TEXT NOT NULL,
    PRIMARY KEY(ingest_run_id, catalog_entry_id)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_kb_catalog_observation_artifact
    ON kb_catalog_observation(source_artifact_id, observed_at DESC);

CREATE TABLE IF NOT EXISTS kb_external_dataset_handle (
    external_dataset_handle_id INTEGER PRIMARY KEY,
    provider_code TEXT NOT NULL,
    dataset_handle TEXT NOT NULL,
    dataset_schema_id INTEGER REFERENCES dataset_schema(dataset_schema_id) ON DELETE SET NULL,
    source_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE SET NULL,
    source_file_name TEXT,
    fingerprint TEXT,
    row_count INTEGER CHECK (row_count IS NULL OR row_count >= 0),
    column_count INTEGER CHECK (column_count IS NULL OR column_count >= 0),
    indexed_at TEXT,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    updated_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(provider_code, dataset_handle)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_kb_external_dataset_current
    ON kb_external_dataset_handle(provider_code, is_current, dataset_handle);

CREATE TABLE IF NOT EXISTS kb_claim_identity (
    claim_id INTEGER PRIMARY KEY REFERENCES claim(claim_id) ON DELETE CASCADE,
    claim_key TEXT NOT NULL UNIQUE
) STRICT;

CREATE TABLE IF NOT EXISTS kb_relation_identity (
    item_relation_id INTEGER PRIMARY KEY REFERENCES item_relation(item_relation_id) ON DELETE CASCADE,
    relation_key TEXT NOT NULL UNIQUE
) STRICT;

CREATE TABLE IF NOT EXISTS kb_packet_application (
    packet_sha256 TEXT PRIMARY KEY,
    packet_version INTEGER NOT NULL CHECK (packet_version >= 1),
    packet_key TEXT NOT NULL UNIQUE,
    change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    applied_at TEXT NOT NULL,
    target_version_id INTEGER NOT NULL REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    source_path TEXT,
    result_summary TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS kb_environment_baseline (
    baseline_id INTEGER PRIMARY KEY,
    baseline_key TEXT NOT NULL UNIQUE,
    game_version_id INTEGER NOT NULL REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    source_root_id INTEGER NOT NULL REFERENCES source_root(source_root_id) ON DELETE RESTRICT,
    launcher_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    display_version TEXT NOT NULL,
    raw_version TEXT NOT NULL,
    checksum_or_build TEXT,
    steam_build_id TEXT,
    captured_at TEXT NOT NULL,
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE UNIQUE INDEX IF NOT EXISTS uq_kb_environment_baseline_current
    ON kb_environment_baseline(is_current) WHERE is_current = 1;

CREATE TABLE IF NOT EXISTS kb_ingest_issue (
    ingest_issue_id INTEGER PRIMARY KEY,
    ingest_run_id INTEGER NOT NULL REFERENCES kb_ingest_run(ingest_run_id) ON DELETE CASCADE,
    corpus_code TEXT,
    relative_path TEXT,
    stage_code TEXT NOT NULL,
    severity_code TEXT NOT NULL CHECK (severity_code IN ('info','warning','error')),
    issue_code TEXT NOT NULL,
    message TEXT NOT NULL,
    status_code TEXT NOT NULL CHECK (status_code IN ('open','accepted','resolved')),
    created_at TEXT NOT NULL,
    UNIQUE(ingest_run_id, corpus_code, relative_path, stage_code, issue_code)
) STRICT;

CREATE TABLE IF NOT EXISTS kb_object_atlas_entry (
    dataset_schema_id INTEGER NOT NULL REFERENCES dataset_schema(dataset_schema_id) ON DELETE CASCADE,
    row_number INTEGER NOT NULL CHECK (row_number >= 1),
    object_definition_id INTEGER NOT NULL REFERENCES object_definition(object_definition_id) ON DELETE CASCADE,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    mod_id TEXT NOT NULL,
    mod_name TEXT NOT NULL,
    source_file TEXT NOT NULL,
    load_winner_signal TEXT NOT NULL CHECK (load_winner_signal IN ('yes','no','unknown')),
    source_has_ai_weight TEXT NOT NULL CHECK (source_has_ai_weight IN ('yes','no','unknown')),
    strategic_role TEXT,
    strategic_tier TEXT,
    parent_ai_support TEXT,
    policy_status TEXT,
    director_action TEXT,
    validation_status TEXT NOT NULL,
    PRIMARY KEY(dataset_schema_id, row_number),
    UNIQUE(object_definition_id, dataset_schema_id, row_number)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_kb_object_atlas_definition
    ON kb_object_atlas_entry(object_definition_id);
CREATE INDEX IF NOT EXISTS idx_kb_object_atlas_policy
    ON kb_object_atlas_entry(policy_status, parent_ai_support, director_action);

CREATE TABLE IF NOT EXISTS kb_dependency_edge_entry (
    dataset_schema_id INTEGER NOT NULL REFERENCES dataset_schema(dataset_schema_id) ON DELETE CASCADE,
    row_number INTEGER NOT NULL CHECK (row_number >= 1),
    item_relation_id INTEGER NOT NULL REFERENCES item_relation(item_relation_id) ON DELETE CASCADE,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    source_type TEXT NOT NULL,
    edge_type TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_status TEXT NOT NULL,
    source_file TEXT NOT NULL,
    evidence_code TEXT NOT NULL,
    PRIMARY KEY(dataset_schema_id, row_number)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_kb_dependency_edge_relation
    ON kb_dependency_edge_entry(item_relation_id);

-- Close provenance holes in the revision-2 foundation.
CREATE TRIGGER IF NOT EXISTS trg_kb_evidence_locator_dataset_insert
BEFORE INSERT ON evidence_locator
WHEN NEW.dataset_schema_id IS NOT NULL
 AND NOT EXISTS (
     SELECT 1 FROM dataset_schema ds
     WHERE ds.dataset_schema_id=NEW.dataset_schema_id
       AND ds.source_artifact_id=NEW.source_artifact_id
 )
BEGIN
    SELECT RAISE(ABORT, 'evidence locator dataset schema belongs to another artifact');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_evidence_locator_dataset_update
BEFORE UPDATE OF source_artifact_id, dataset_schema_id ON evidence_locator
WHEN NEW.dataset_schema_id IS NOT NULL
 AND NOT EXISTS (
     SELECT 1 FROM dataset_schema ds
     WHERE ds.dataset_schema_id=NEW.dataset_schema_id
       AND ds.source_artifact_id=NEW.source_artifact_id
 )
BEGIN
    SELECT RAISE(ABORT, 'evidence locator dataset schema belongs to another artifact');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_analysis_run_artifact_dataset_insert
BEFORE INSERT ON analysis_run_artifact
WHEN NEW.dataset_schema_id IS NOT NULL
 AND NOT EXISTS (
     SELECT 1 FROM dataset_schema ds
     WHERE ds.dataset_schema_id=NEW.dataset_schema_id
       AND ds.source_artifact_id=NEW.source_artifact_id
 )
BEGIN
    SELECT RAISE(ABORT, 'analysis run dataset schema belongs to another artifact');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_analysis_run_artifact_dataset_update
BEFORE UPDATE OF source_artifact_id, dataset_schema_id ON analysis_run_artifact
WHEN NEW.dataset_schema_id IS NOT NULL
 AND NOT EXISTS (
     SELECT 1 FROM dataset_schema ds
     WHERE ds.dataset_schema_id=NEW.dataset_schema_id
       AND ds.source_artifact_id=NEW.source_artifact_id
 )
BEGIN
    SELECT RAISE(ABORT, 'analysis run dataset schema belongs to another artifact');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_object_conflict_winner_insert
BEFORE INSERT ON object_conflict
WHEN NEW.winning_definition_id IS NOT NULL
 AND NOT EXISTS (
     SELECT 1 FROM object_definition od
     WHERE od.object_definition_id=NEW.winning_definition_id
       AND od.object_item_id=NEW.object_item_id
 )
BEGIN
    SELECT RAISE(ABORT, 'object conflict winner belongs to another object');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_object_conflict_winner_update
BEFORE UPDATE OF object_item_id, winning_definition_id ON object_conflict
WHEN NEW.winning_definition_id IS NOT NULL
 AND NOT EXISTS (
     SELECT 1 FROM object_definition od
     WHERE od.object_definition_id=NEW.winning_definition_id
       AND od.object_item_id=NEW.object_item_id
 )
BEGIN
    SELECT RAISE(ABORT, 'object conflict winner belongs to another object');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_analysis_scenario_parent_insert
BEFORE INSERT ON analysis_scenario
WHEN NEW.parent_scenario_id IS NOT NULL
 AND (
     NEW.parent_scenario_id=NEW.analysis_scenario_id
     OR NOT EXISTS (
         SELECT 1 FROM analysis_scenario parent
         WHERE parent.analysis_scenario_id=NEW.parent_scenario_id
           AND parent.analysis_run_id=NEW.analysis_run_id
     )
 )
BEGIN
    SELECT RAISE(ABORT, 'analysis scenario parent is self or belongs to another run');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_analysis_scenario_parent_update
BEFORE UPDATE OF parent_scenario_id, analysis_run_id ON analysis_scenario
WHEN NEW.parent_scenario_id IS NOT NULL
 AND (
     NEW.parent_scenario_id=NEW.analysis_scenario_id
     OR NOT EXISTS (
         SELECT 1 FROM analysis_scenario parent
         WHERE parent.analysis_scenario_id=NEW.parent_scenario_id
           AND parent.analysis_run_id=NEW.analysis_run_id
     )
     OR EXISTS (
         WITH RECURSIVE descendants(id) AS (
             SELECT analysis_scenario_id FROM analysis_scenario
             WHERE parent_scenario_id=NEW.analysis_scenario_id
             UNION ALL
             SELECT child.analysis_scenario_id
             FROM analysis_scenario child JOIN descendants d ON child.parent_scenario_id=d.id
         )
         SELECT 1 FROM descendants WHERE id=NEW.parent_scenario_id
     )
 )
BEGIN
    SELECT RAISE(ABORT, 'analysis scenario parent would create an invalid hierarchy');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_change_set_shape_insert
BEFORE INSERT ON change_set
WHEN (NEW.state='committed' AND NEW.committed_at IS NULL)
  OR (NEW.state<>'committed' AND NEW.committed_at IS NOT NULL)
BEGIN
    SELECT RAISE(ABORT, 'change-set state/timestamp mismatch');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_change_set_transition_update
BEFORE UPDATE OF state, committed_at, opened_at ON change_set
WHEN OLD.state IN ('committed','aborted')
  OR NEW.state='open'
  OR (NEW.state='committed' AND NEW.committed_at IS NULL)
  OR (NEW.state='aborted' AND NEW.committed_at IS NOT NULL)
BEGIN
    SELECT RAISE(ABORT, 'invalid or nonterminal change-set transition');
END;

CREATE UNIQUE INDEX IF NOT EXISTS uq_item_alias_global
    ON item_alias(item_id, alias_text, alias_kind)
    WHERE version_span_id IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_artifact_derivation_without_run
    ON artifact_derivation(output_artifact_id, input_artifact_id)
    WHERE process_run_key IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_claim_conflict_global
    ON claim_conflict(claim_a_id, claim_b_id)
    WHERE version_span_id IS NULL;

CREATE TRIGGER IF NOT EXISTS trg_kb_repository_snapshot_open_changeset_insert
BEFORE INSERT ON repository_snapshot
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_source_root_open_changeset_insert
BEFORE INSERT ON source_root
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_source_artifact_open_changeset_insert
BEFORE INSERT ON source_artifact
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_knowledge_item_open_changeset_insert
BEFORE INSERT ON knowledge_item
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_evidence_locator_open_changeset_insert
BEFORE INSERT ON evidence_locator
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_dataset_schema_open_changeset_insert
BEFORE INSERT ON dataset_schema
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_claim_open_changeset_insert
BEFORE INSERT ON claim
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_claim_assessment_open_changeset_insert
BEFORE INSERT ON claim_assessment
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_item_relation_open_changeset_insert
BEFORE INSERT ON item_relation
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_open_question_open_changeset_insert
BEFORE INSERT ON open_question
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_verification_run_open_changeset_insert
BEFORE INSERT ON verification_run
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_validation_finding_open_changeset_insert
BEFORE INSERT ON validation_finding
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_object_definition_open_changeset_insert
BEFORE INSERT ON object_definition
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_object_conflict_open_changeset_insert
BEFORE INSERT ON object_conflict
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_analysis_model_open_changeset_insert
BEFORE INSERT ON analysis_model
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_analysis_run_open_changeset_insert
BEFORE INSERT ON analysis_run
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_analysis_metric_open_changeset_insert
BEFORE INSERT ON analysis_metric
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_analysis_issue_open_changeset_insert
BEFORE INSERT ON analysis_issue
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_kb_catalog_entry_open_changeset_insert
BEFORE INSERT ON kb_catalog_entry
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_kb_external_dataset_handle_open_changeset_insert
BEFORE INSERT ON kb_external_dataset_handle
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

CREATE TRIGGER IF NOT EXISTS trg_kb_kb_environment_baseline_open_changeset_insert
BEFORE INSERT ON kb_environment_baseline
WHEN NOT EXISTS (
    SELECT 1 FROM change_set cs
    WHERE cs.change_set_id=NEW.created_in_change_set_id AND cs.state='open'
)
BEGIN
    SELECT RAISE(ABORT, 'created_in_change_set_id must reference an open change set');
END;

INSERT OR REPLACE INTO schema_metadata(metadata_key, metadata_value, description) VALUES
('production_extension_revision', '3', 'Production ingestion, packet, catalog, and environment sidecars.'),
('production_target_version', '4.4.4', 'Explicit user-selected operating Stellaris version.'),
('design_bundle_sha256', 'c279db03b51c1f557ae3bd8d1f84c186f7c01acdbf9f7a17fa82b7a15a3b570f', 'Source project-aware design bundle.'),
('writer_contract', 'exclusive_lock+begin_immediate+append_supersede', 'Serialized writer and provenance lifecycle contract.');

UPDATE game_version SET is_primary_target = 0 WHERE is_primary_target = 1;
UPDATE game_version
SET is_primary_target = 1,
    build_id = '5505',
    notes = 'Primary operating target verified from local launcher-settings.json; Pegasus v4.4.4 (5505).'
WHERE version_label = '4.4.4';

UPDATE version_span
SET span_name = 'Current Stellaris 4.4.4 target',
    boundary_note = 'Exact current operating version verified locally.'
WHERE span_code = 'v4.4.4';

PRAGMA user_version = 3;

INSERT INTO kb_migration(migration_version, migration_name, script_sha256)
VALUES (3, 'production_ingestion', '{{MIGRATION_SHA256}}');
