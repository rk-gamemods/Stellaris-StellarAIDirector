-- Stellaris AI Mod Knowledge Base
-- Foundational schema, revision 2: project-corpus, playset, dataset, and analysis sidecars.
-- Minimum SQLite version: 3.37.0 (STRICT tables). FTS5 must be enabled.
-- Connection rule: every writer and reader should execute PRAGMA foreign_keys=ON;
-- Writers should also set a nonzero busy_timeout and use short explicit transactions.

PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;
PRAGMA journal_mode = WAL;
PRAGMA recursive_triggers = ON;
PRAGMA application_id = 1397441074; -- 0x534B4232, project-local "SKB2" marker.
PRAGMA user_version = 2;

BEGIN IMMEDIATE;

-- ---------------------------------------------------------------------------
-- 1. Database metadata, authorship, and version axes
-- ---------------------------------------------------------------------------

CREATE TABLE schema_metadata (
    metadata_key TEXT PRIMARY KEY,
    metadata_value TEXT NOT NULL,
    description TEXT
) STRICT;

CREATE TABLE actor (
    actor_id INTEGER PRIMARY KEY,
    actor_key TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    actor_type TEXT NOT NULL CHECK (actor_type IN ('human','ai_agent','tool','system')),
    external_identifier TEXT,
    notes TEXT
) STRICT;

CREATE TABLE change_set (
    change_set_id INTEGER PRIMARY KEY,
    change_set_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    purpose TEXT NOT NULL,
    actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT,
    state TEXT NOT NULL CHECK (state IN ('open','committed','aborted')),
    opened_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    committed_at TEXT,
    repository_commit TEXT,
    transaction_note TEXT,
    CHECK ((state = 'committed' AND committed_at IS NOT NULL) OR state <> 'committed')
) STRICT;

CREATE INDEX idx_change_set_actor_state ON change_set(actor_id, state, opened_at);

CREATE TABLE lifecycle_state (
    lifecycle_state_id INTEGER PRIMARY KEY,
    state_code TEXT NOT NULL UNIQUE,
    state_name TEXT NOT NULL,
    is_active INTEGER NOT NULL CHECK (is_active IN (0,1)),
    description TEXT NOT NULL
) STRICT;

CREATE TABLE confidence_level (
    confidence_level_id INTEGER PRIMARY KEY,
    confidence_code TEXT NOT NULL UNIQUE,
    confidence_name TEXT NOT NULL,
    rank_value INTEGER NOT NULL UNIQUE CHECK (rank_value BETWEEN 0 AND 100),
    description TEXT NOT NULL
) STRICT;

CREATE TABLE assessment_state (
    assessment_state_id INTEGER PRIMARY KEY,
    state_code TEXT NOT NULL UNIQUE,
    state_name TEXT NOT NULL,
    rank_value INTEGER NOT NULL CHECK (rank_value BETWEEN 0 AND 100),
    is_usable_as_fact INTEGER NOT NULL CHECK (is_usable_as_fact IN (0,1)),
    description TEXT NOT NULL
) STRICT;

CREATE TABLE game_version (
    game_version_id INTEGER PRIMARY KEY,
    version_label TEXT NOT NULL UNIQUE,
    version_order INTEGER NOT NULL UNIQUE,
    major INTEGER CHECK (major IS NULL OR major >= 0),
    minor INTEGER CHECK (minor IS NULL OR minor >= 0),
    patch INTEGER CHECK (patch IS NULL OR patch >= 0),
    codename TEXT,
    build_id TEXT,
    release_channel TEXT NOT NULL DEFAULT 'unknown',
    released_on TEXT,
    is_primary_target INTEGER NOT NULL DEFAULT 0 CHECK (is_primary_target IN (0,1)),
    notes TEXT,
    created_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE UNIQUE INDEX uq_game_version_primary_target
    ON game_version(is_primary_target)
    WHERE is_primary_target = 1;

CREATE TABLE version_span (
    version_span_id INTEGER PRIMARY KEY,
    span_code TEXT NOT NULL UNIQUE,
    span_name TEXT NOT NULL,
    min_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    max_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    boundary_note TEXT,
    created_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_version_span_bounds ON version_span(min_version_id, max_version_id);

CREATE TRIGGER trg_version_span_order_insert
BEFORE INSERT ON version_span
WHEN NEW.min_version_id IS NOT NULL AND NEW.max_version_id IS NOT NULL
BEGIN
    SELECT CASE WHEN
        (SELECT version_order FROM game_version WHERE game_version_id = NEW.min_version_id) >
        (SELECT version_order FROM game_version WHERE game_version_id = NEW.max_version_id)
    THEN RAISE(ABORT, 'version_span minimum is after maximum') END;
END;

CREATE TRIGGER trg_version_span_order_update
BEFORE UPDATE OF min_version_id, max_version_id ON version_span
WHEN NEW.min_version_id IS NOT NULL AND NEW.max_version_id IS NOT NULL
BEGIN
    SELECT CASE WHEN
        (SELECT version_order FROM game_version WHERE game_version_id = NEW.min_version_id) >
        (SELECT version_order FROM game_version WHERE game_version_id = NEW.max_version_id)
    THEN RAISE(ABORT, 'version_span minimum is after maximum') END;
END;

-- ---------------------------------------------------------------------------
-- 2. Extensible controlled vocabularies
-- ---------------------------------------------------------------------------

CREATE TABLE item_type (
    item_type_id INTEGER PRIMARY KEY,
    type_code TEXT NOT NULL UNIQUE,
    type_name TEXT NOT NULL,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE object_kind (
    object_kind_id INTEGER PRIMARY KEY,
    kind_code TEXT NOT NULL UNIQUE,
    kind_name TEXT NOT NULL,
    definition_folder TEXT,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE script_symbol_kind (
    script_symbol_kind_id INTEGER PRIMARY KEY,
    kind_code TEXT NOT NULL UNIQUE,
    kind_name TEXT NOT NULL,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE claim_type (
    claim_type_id INTEGER PRIMARY KEY,
    type_code TEXT NOT NULL UNIQUE,
    type_name TEXT NOT NULL,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE evidence_source_type (
    evidence_source_type_id INTEGER PRIMARY KEY,
    type_code TEXT NOT NULL UNIQUE,
    type_name TEXT NOT NULL,
    default_reliability_rank INTEGER NOT NULL CHECK (default_reliability_rank BETWEEN 0 AND 100),
    authoritative_scope TEXT,
    is_primary_evidence INTEGER NOT NULL CHECK (is_primary_evidence IN (0,1)),
    description TEXT NOT NULL
) STRICT;

CREATE TABLE locator_type (
    locator_type_id INTEGER PRIMARY KEY,
    type_code TEXT NOT NULL UNIQUE,
    type_name TEXT NOT NULL,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE evidence_stance (
    evidence_stance_id INTEGER PRIMARY KEY,
    stance_code TEXT NOT NULL UNIQUE,
    stance_name TEXT NOT NULL,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE risk_level (
    risk_level_id INTEGER PRIMARY KEY,
    risk_code TEXT NOT NULL UNIQUE,
    risk_name TEXT NOT NULL,
    rank_value INTEGER NOT NULL UNIQUE CHECK (rank_value BETWEEN 0 AND 100),
    description TEXT NOT NULL
) STRICT;

CREATE TABLE relation_type (
    relation_type_id INTEGER PRIMARY KEY,
    type_code TEXT NOT NULL UNIQUE,
    type_name TEXT NOT NULL,
    inverse_name TEXT,
    description TEXT NOT NULL,
    impact_propagation_mode TEXT NOT NULL CHECK (impact_propagation_mode IN ('forward','reverse','both','none')),
    is_transitive_hint INTEGER NOT NULL DEFAULT 0 CHECK (is_transitive_hint IN (0,1))
) STRICT;

CREATE TABLE change_kind (
    change_kind_id INTEGER PRIMARY KEY,
    kind_code TEXT NOT NULL UNIQUE,
    kind_name TEXT NOT NULL,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE change_type (
    change_type_id INTEGER PRIMARY KEY,
    type_code TEXT NOT NULL UNIQUE,
    type_name TEXT NOT NULL,
    description TEXT NOT NULL
) STRICT;

CREATE TABLE investigation_task_type (
    investigation_task_type_id INTEGER PRIMARY KEY,
    task_code TEXT NOT NULL UNIQUE,
    task_name TEXT NOT NULL,
    description TEXT NOT NULL
) STRICT;

-- ---------------------------------------------------------------------------
-- 3. Stable knowledge-item supertype and typed sidecars
-- ---------------------------------------------------------------------------

CREATE TABLE knowledge_item (
    item_id INTEGER PRIMARY KEY,
    item_type_id INTEGER NOT NULL REFERENCES item_type(item_type_id) ON DELETE RESTRICT,
    canonical_key TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    summary TEXT NOT NULL,
    lifecycle_state_id INTEGER NOT NULL REFERENCES lifecycle_state(lifecycle_state_id) ON DELETE RESTRICT,
    created_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    updated_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_knowledge_item_type_name ON knowledge_item(item_type_id, display_name);
CREATE INDEX idx_knowledge_item_lifecycle ON knowledge_item(lifecycle_state_id, item_type_id);

CREATE TABLE item_alias (
    item_alias_id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    alias_text TEXT NOT NULL,
    alias_kind TEXT NOT NULL,
    version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(item_id, alias_text, alias_kind, version_span_id)
) STRICT;

CREATE INDEX idx_item_alias_lookup ON item_alias(alias_text, alias_kind);

CREATE TABLE item_version_status (
    item_version_status_id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    status_code TEXT NOT NULL CHECK (status_code IN ('present','absent','renamed','deprecated','changed','unknown')),
    assessment_state_id INTEGER NOT NULL REFERENCES assessment_state(assessment_state_id) ON DELETE RESTRICT,
    confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    assessed_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT,
    assessed_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    basis_summary TEXT NOT NULL,
    notes TEXT,
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
    supersedes_item_version_status_id INTEGER REFERENCES item_version_status(item_version_status_id) ON DELETE RESTRICT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (supersedes_item_version_status_id IS NULL OR supersedes_item_version_status_id <> item_version_status_id)
) STRICT;

CREATE UNIQUE INDEX uq_item_version_status_current_exact_span
    ON item_version_status(item_id, version_span_id)
    WHERE is_current = 1;
CREATE INDEX idx_item_version_status_lookup ON item_version_status(item_id, version_span_id, is_current, status_code);
CREATE INDEX idx_item_version_status_state ON item_version_status(assessment_state_id, confidence_level_id, assessed_at);

CREATE TABLE mechanic_family (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    family_code TEXT NOT NULL UNIQUE,
    domain_summary TEXT NOT NULL
) STRICT;

CREATE TABLE mechanic (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    mechanic_family_item_id INTEGER NOT NULL REFERENCES mechanic_family(item_id) ON DELETE RESTRICT,
    purpose TEXT NOT NULL,
    engine_visibility TEXT NOT NULL CHECK (engine_visibility IN ('script_visible','partially_script_visible','hardcoded_or_hidden','unknown')),
    owner_scope_item_id INTEGER REFERENCES script_scope(item_id) ON DELETE RESTRICT,
    notes TEXT
) STRICT;

CREATE INDEX idx_mechanic_family ON mechanic(mechanic_family_item_id);

CREATE TABLE subsystem (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    subsystem_code TEXT NOT NULL UNIQUE,
    purpose TEXT NOT NULL,
    primary_repository_path TEXT,
    acceptance_summary TEXT
) STRICT;

CREATE TABLE game_object (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    object_kind_id INTEGER NOT NULL REFERENCES object_kind(object_kind_id) ON DELETE RESTRICT,
    script_key TEXT NOT NULL,
    namespace TEXT NOT NULL DEFAULT '',
    origin_class TEXT NOT NULL CHECK (origin_class IN ('vanilla','mod','generated','external_mod','unknown')),
    notes TEXT,
    UNIQUE(object_kind_id, script_key, namespace, origin_class)
) STRICT;

CREATE INDEX idx_game_object_script_key ON game_object(script_key, object_kind_id);

CREATE TABLE file_asset (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    corpus_code TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    file_role TEXT NOT NULL,
    load_order_note TEXT,
    UNIQUE(corpus_code, relative_path)
) STRICT;

CREATE INDEX idx_file_asset_path ON file_asset(relative_path);

CREATE TABLE script_symbol (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    script_symbol_kind_id INTEGER NOT NULL REFERENCES script_symbol_kind(script_symbol_kind_id) ON DELETE RESTRICT,
    symbol_key TEXT NOT NULL,
    namespace TEXT NOT NULL DEFAULT '',
    exposure_class TEXT NOT NULL CHECK (exposure_class IN ('built_in','scripted','define','generated','unknown')),
    description TEXT,
    UNIQUE(script_symbol_kind_id, symbol_key, namespace)
) STRICT;

CREATE INDEX idx_script_symbol_key ON script_symbol(symbol_key, script_symbol_kind_id);

CREATE TABLE field_definition (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    owner_object_kind_id INTEGER NOT NULL REFERENCES object_kind(object_kind_id) ON DELETE RESTRICT,
    field_name TEXT NOT NULL,
    value_type TEXT NOT NULL,
    cardinality TEXT NOT NULL,
    semantic_summary TEXT NOT NULL,
    UNIQUE(owner_object_kind_id, field_name)
) STRICT;

CREATE TABLE field_revision (
    field_revision_id INTEGER PRIMARY KEY,
    field_item_id INTEGER NOT NULL REFERENCES field_definition(item_id) ON DELETE RESTRICT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    value_type TEXT NOT NULL,
    cardinality TEXT NOT NULL,
    semantic_summary TEXT NOT NULL,
    status_code TEXT NOT NULL CHECK (status_code IN ('present','absent','deprecated','changed','unknown')),
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(field_item_id, version_span_id, source_system_id, evidence_locator_id)
) STRICT;

CREATE INDEX idx_field_revision_lookup
    ON field_revision(field_item_id, version_span_id, status_code);

CREATE TABLE script_scope (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    scope_key TEXT NOT NULL UNIQUE,
    engine_scope_name TEXT,
    scope_summary TEXT NOT NULL
) STRICT;

CREATE TABLE object_definition (
    object_definition_id INTEGER PRIMARY KEY,
    object_item_id INTEGER NOT NULL REFERENCES game_object(item_id) ON DELETE RESTRICT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT,
    source_root_id INTEGER REFERENCES source_root(source_root_id) ON DELETE RESTRICT,
    mod_release_id INTEGER REFERENCES mod_release(mod_release_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    definition_status TEXT NOT NULL CHECK (definition_status IN ('candidate','reference','removed','unknown')),
    object_path TEXT,
    line_start INTEGER CHECK (line_start IS NULL OR line_start >= 1),
    line_end INTEGER CHECK (line_end IS NULL OR line_end >= 1),
    content_hash_algorithm TEXT,
    content_hash TEXT,
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (line_end IS NULL OR line_start IS NOT NULL),
    CHECK (line_end IS NULL OR line_end >= line_start),
    UNIQUE(object_item_id, version_span_id, source_system_id, evidence_locator_id)
) STRICT;

CREATE INDEX idx_object_definition_lookup ON object_definition(object_item_id, version_span_id, definition_status);
CREATE INDEX idx_object_definition_origin ON object_definition(source_root_id, mod_release_id, object_item_id);

CREATE TABLE object_field_occurrence (
    object_field_occurrence_id INTEGER PRIMARY KEY,
    object_definition_id INTEGER REFERENCES object_definition(object_definition_id) ON DELETE CASCADE,
    object_item_id INTEGER NOT NULL REFERENCES game_object(item_id) ON DELETE RESTRICT,
    field_item_id INTEGER NOT NULL REFERENCES field_definition(item_id) ON DELETE RESTRICT,
    parent_occurrence_id INTEGER REFERENCES object_field_occurrence(object_field_occurrence_id) ON DELETE CASCADE,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    ordinal_in_object INTEGER,
    field_path TEXT,
    occurrence_kind TEXT NOT NULL DEFAULT 'unknown' CHECK (occurrence_kind IN ('scalar','block','list','invocation','expression','unknown')),
    value_type TEXT CHECK (value_type IS NULL OR value_type IN ('integer','real','text','boolean','identifier','expression','block','list','unknown')),
    value_text TEXT,
    integer_value INTEGER,
    real_value REAL,
    boolean_value INTEGER CHECK (boolean_value IS NULL OR boolean_value IN (0,1)),
    referenced_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    expression_text TEXT,
    normalized_summary TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK ((integer_value IS NOT NULL) + (real_value IS NOT NULL) + (boolean_value IS NOT NULL) <= 1),
    UNIQUE(object_item_id, field_item_id, version_span_id, evidence_locator_id, ordinal_in_object)
) STRICT;

CREATE INDEX idx_object_field_by_field ON object_field_occurrence(field_item_id, version_span_id, object_item_id);
CREATE INDEX idx_object_field_by_object ON object_field_occurrence(object_item_id, version_span_id, field_item_id);
CREATE INDEX idx_object_field_by_definition ON object_field_occurrence(object_definition_id, field_path, ordinal_in_object);

CREATE TABLE script_symbol_revision (
    script_symbol_revision_id INTEGER PRIMARY KEY,
    script_symbol_item_id INTEGER NOT NULL REFERENCES script_symbol(item_id) ON DELETE RESTRICT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    revision_kind TEXT NOT NULL,
    signature_text TEXT,
    value_text TEXT,
    behavior_summary TEXT,
    status_code TEXT NOT NULL CHECK (status_code IN ('present','absent','deprecated','changed','unknown')),
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(script_symbol_item_id, version_span_id, source_system_id, revision_kind, evidence_locator_id)
) STRICT;

CREATE INDEX idx_symbol_revision_lookup ON script_symbol_revision(script_symbol_item_id, version_span_id, status_code);

CREATE TABLE symbol_scope_rule (
    symbol_scope_rule_id INTEGER PRIMARY KEY,
    script_symbol_item_id INTEGER NOT NULL REFERENCES script_symbol(item_id) ON DELETE RESTRICT,
    scope_item_id INTEGER NOT NULL REFERENCES script_scope(item_id) ON DELETE RESTRICT,
    role_code TEXT NOT NULL,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    rule_summary TEXT NOT NULL,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(script_symbol_item_id, scope_item_id, role_code, version_span_id)
) STRICT;

CREATE INDEX idx_symbol_scope_by_scope ON symbol_scope_rule(scope_item_id, version_span_id, role_code);

CREATE TABLE symbol_parameter (
    symbol_parameter_id INTEGER PRIMARY KEY,
    script_symbol_item_id INTEGER NOT NULL REFERENCES script_symbol(item_id) ON DELETE RESTRICT,
    parameter_name TEXT NOT NULL,
    value_type TEXT NOT NULL,
    is_required INTEGER NOT NULL CHECK (is_required IN (0,1)),
    default_value_text TEXT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    description TEXT NOT NULL,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(script_symbol_item_id, parameter_name, version_span_id)
) STRICT;

-- ---------------------------------------------------------------------------
-- 4. Evidence systems, artifacts, and precise locators
-- ---------------------------------------------------------------------------

CREATE TABLE source_system (
    source_system_id INTEGER PRIMARY KEY,
    system_key TEXT NOT NULL UNIQUE,
    system_name TEXT NOT NULL,
    evidence_source_type_id INTEGER NOT NULL REFERENCES evidence_source_type(evidence_source_type_id) ON DELETE RESTRICT,
    canonical_root TEXT,
    access_mode TEXT NOT NULL,
    authoritative_for TEXT,
    default_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    retrieval_instructions TEXT NOT NULL,
    is_local_only INTEGER NOT NULL CHECK (is_local_only IN (0,1)),
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_source_system_type ON source_system(evidence_source_type_id, system_name);

CREATE TABLE source_artifact (
    source_artifact_id INTEGER PRIMARY KEY,
    source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT,
    source_root_id INTEGER REFERENCES source_root(source_root_id) ON DELETE RESTRICT,
    repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT,
    mod_release_id INTEGER REFERENCES mod_release(mod_release_id) ON DELETE RESTRICT,
    stable_key TEXT NOT NULL,
    artifact_kind TEXT NOT NULL,
    title TEXT NOT NULL,
    uri_or_path TEXT NOT NULL,
    repository_relative_path TEXT,
    game_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    repository_commit TEXT,
    tool_version TEXT,
    content_hash_algorithm TEXT,
    content_hash_value TEXT,
    file_size_bytes INTEGER CHECK (file_size_bytes IS NULL OR file_size_bytes >= 0),
    mime_type TEXT,
    modified_at TEXT,
    captured_at TEXT,
    observed_at TEXT,
    availability_status TEXT NOT NULL CHECK (availability_status IN ('available','missing','moved','archived','unknown')),
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(source_system_id, stable_key)
) STRICT;

CREATE INDEX idx_source_artifact_version ON source_artifact(game_version_id, source_system_id, artifact_kind);
CREATE INDEX idx_source_artifact_path ON source_artifact(uri_or_path);
CREATE INDEX idx_source_artifact_context ON source_artifact(source_root_id, repository_snapshot_id, mod_release_id);

CREATE TABLE artifact_derivation (
    artifact_derivation_id INTEGER PRIMARY KEY,
    output_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    input_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    process_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT,
    process_run_key TEXT,
    command_or_method TEXT,
    derived_at TEXT,
    rationale TEXT NOT NULL,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (output_artifact_id <> input_artifact_id),
    UNIQUE(output_artifact_id, input_artifact_id, process_run_key)
) STRICT;

CREATE INDEX idx_artifact_derivation_input ON artifact_derivation(input_artifact_id, output_artifact_id);

CREATE TABLE evidence_locator (
    evidence_locator_id INTEGER PRIMARY KEY,
    source_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    dataset_schema_id INTEGER REFERENCES dataset_schema(dataset_schema_id) ON DELETE RESTRICT,
    locator_type_id INTEGER NOT NULL REFERENCES locator_type(locator_type_id) ON DELETE RESTRICT,
    stable_locator_key TEXT NOT NULL,
    label TEXT NOT NULL,
    relative_path TEXT,
    line_start INTEGER CHECK (line_start IS NULL OR line_start >= 1),
    line_end INTEGER CHECK (line_end IS NULL OR line_end >= 1),
    page_start INTEGER CHECK (page_start IS NULL OR page_start >= 1),
    page_end INTEGER CHECK (page_end IS NULL OR page_end >= 1),
    section_title TEXT,
    symbol_or_object_key TEXT,
    record_set TEXT,
    record_key TEXT,
    row_number INTEGER CHECK (row_number IS NULL OR row_number >= 1),
    column_name TEXT,
    json_path TEXT,
    archive_member_path TEXT,
    byte_start INTEGER CHECK (byte_start IS NULL OR byte_start >= 0),
    byte_end INTEGER CHECK (byte_end IS NULL OR byte_end >= 0),
    query_text TEXT,
    timestamp_start TEXT,
    timestamp_end TEXT,
    game_date TEXT,
    excerpt TEXT,
    evidence_summary TEXT NOT NULL,
    retrieval_instructions TEXT,
    created_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (line_end IS NULL OR line_start IS NOT NULL),
    CHECK (line_end IS NULL OR line_end >= line_start),
    CHECK (page_end IS NULL OR page_start IS NOT NULL),
    CHECK (page_end IS NULL OR page_end >= page_start),
    CHECK (byte_end IS NULL OR byte_start IS NOT NULL),
    CHECK (byte_end IS NULL OR byte_end >= byte_start),
    UNIQUE(source_artifact_id, stable_locator_key)
) STRICT;

CREATE INDEX idx_evidence_locator_symbol ON evidence_locator(symbol_or_object_key, source_artifact_id);
CREATE INDEX idx_evidence_locator_record ON evidence_locator(record_set, record_key, row_number, column_name);
CREATE INDEX idx_evidence_locator_artifact ON evidence_locator(source_artifact_id, locator_type_id);

-- Resolve forward references now that evidence tables exist.
CREATE INDEX idx_item_version_status_evidence ON item_version_status(evidence_locator_id) WHERE evidence_locator_id IS NOT NULL;

-- ---------------------------------------------------------------------------
-- 5. Claims, assessments, contradictions, questions, and revalidation
-- ---------------------------------------------------------------------------

CREATE TABLE verification_run (
    verification_run_id INTEGER PRIMARY KEY,
    run_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    run_kind TEXT NOT NULL DEFAULT 'static_analysis' CHECK (run_kind IN ('static_analysis','schema_validation','conflict_scan','source_diff','model_generation','log_analysis','save_analysis','observer_run','controlled_experiment','database_validation','other')),
    target_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    execution_context_id INTEGER REFERENCES execution_context(execution_context_id) ON DELETE RESTRICT,
    tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    performed_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT,
    method_summary TEXT NOT NULL,
    command_or_query TEXT,
    environment_summary TEXT,
    started_at TEXT,
    completed_at TEXT,
    approval_status TEXT NOT NULL DEFAULT 'not_required' CHECK (approval_status IN ('not_required','approved','not_approved','unknown')),
    reproducibility_status TEXT NOT NULL DEFAULT 'partially_reproducible' CHECK (reproducibility_status IN ('reproducible','partially_reproducible','not_reproducible','unknown')),
    outcome_code TEXT NOT NULL CHECK (outcome_code IN ('passed','failed','partial','inconclusive','not_run')),
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_verification_run_target ON verification_run(target_version_id, outcome_code, completed_at);

CREATE TABLE claim (
    claim_id INTEGER PRIMARY KEY,
    claim_type_id INTEGER NOT NULL REFERENCES claim_type(claim_type_id) ON DELETE RESTRICT,
    primary_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    statement TEXT NOT NULL,
    context TEXT,
    epistemic_note TEXT,
    supersedes_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT,
    lifecycle_state_id INTEGER NOT NULL REFERENCES lifecycle_state(lifecycle_state_id) ON DELETE RESTRICT,
    created_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (supersedes_claim_id IS NULL OR supersedes_claim_id <> claim_id)
) STRICT;

CREATE INDEX idx_claim_primary_item ON claim(primary_item_id, lifecycle_state_id, claim_type_id);
CREATE INDEX idx_claim_supersedes ON claim(supersedes_claim_id) WHERE supersedes_claim_id IS NOT NULL;

CREATE TABLE claim_item (
    claim_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    role_code TEXT NOT NULL,
    notes TEXT,
    PRIMARY KEY (claim_id, item_id, role_code)
) STRICT;

CREATE INDEX idx_claim_item_item ON claim_item(item_id, role_code, claim_id);

CREATE TABLE claim_assessment (
    claim_assessment_id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE RESTRICT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    assessment_state_id INTEGER NOT NULL REFERENCES assessment_state(assessment_state_id) ON DELETE RESTRICT,
    confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT,
    verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT,
    execution_context_id INTEGER REFERENCES execution_context(execution_context_id) ON DELETE RESTRICT,
    assessed_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT,
    assessed_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    basis_summary TEXT NOT NULL,
    reverify_after TEXT,
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
    supersedes_assessment_id INTEGER REFERENCES claim_assessment(claim_assessment_id) ON DELETE RESTRICT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (supersedes_assessment_id IS NULL OR supersedes_assessment_id <> claim_assessment_id)
) STRICT;

CREATE UNIQUE INDEX uq_claim_assessment_current_exact_span
    ON claim_assessment(claim_id, version_span_id)
    WHERE is_current = 1;
CREATE INDEX idx_claim_assessment_state ON claim_assessment(assessment_state_id, confidence_level_id, reverify_after);
CREATE INDEX idx_claim_assessment_claim ON claim_assessment(claim_id, is_current, version_span_id);

CREATE TABLE claim_conflict (
    claim_conflict_id INTEGER PRIMARY KEY,
    claim_a_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE RESTRICT,
    claim_b_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE RESTRICT,
    version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    conflict_kind TEXT NOT NULL,
    status_code TEXT NOT NULL CHECK (status_code IN ('open','resolved','dismissed')),
    analysis TEXT NOT NULL,
    resolution_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    resolved_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (claim_a_id < claim_b_id),
    UNIQUE(claim_a_id, claim_b_id, version_span_id)
) STRICT;

CREATE INDEX idx_claim_conflict_status ON claim_conflict(status_code, version_span_id);

CREATE TABLE open_question (
    question_id INTEGER PRIMARY KEY,
    question_key TEXT NOT NULL UNIQUE,
    primary_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    question_text TEXT NOT NULL,
    uncertainty_reason TEXT NOT NULL,
    target_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    status_code TEXT NOT NULL CHECK (status_code IN ('open','investigating','blocked','resolved','wont_fix')),
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100),
    owner_actor_id INTEGER REFERENCES actor(actor_id) ON DELETE RESTRICT,
    resolution_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT,
    next_review_at TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    closed_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_open_question_queue ON open_question(status_code, priority DESC, target_version_id);

CREATE TABLE question_item (
    question_id INTEGER NOT NULL REFERENCES open_question(question_id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    role_code TEXT NOT NULL,
    notes TEXT,
    PRIMARY KEY(question_id, item_id, role_code)
) STRICT;

CREATE INDEX idx_question_item_item ON question_item(item_id, role_code, question_id);

CREATE TABLE revalidation_policy (
    revalidation_policy_id INTEGER PRIMARY KEY,
    policy_code TEXT NOT NULL UNIQUE,
    policy_name TEXT NOT NULL,
    trigger_on_any_game_update INTEGER NOT NULL CHECK (trigger_on_any_game_update IN (0,1)),
    minimum_version_change TEXT CHECK (minimum_version_change IN ('patch','minor','major','any') OR minimum_version_change IS NULL),
    trigger_on_source_change INTEGER NOT NULL CHECK (trigger_on_source_change IN (0,1)),
    max_age_days INTEGER CHECK (max_age_days IS NULL OR max_age_days >= 1),
    preferred_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    instructions TEXT NOT NULL,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE TABLE claim_revalidation_policy (
    claim_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE CASCADE,
    revalidation_policy_id INTEGER NOT NULL REFERENCES revalidation_policy(revalidation_policy_id) ON DELETE RESTRICT,
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100),
    notes TEXT,
    PRIMARY KEY(claim_id, revalidation_policy_id)
) STRICT;

CREATE TABLE item_revalidation_policy (
    item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    revalidation_policy_id INTEGER NOT NULL REFERENCES revalidation_policy(revalidation_policy_id) ON DELETE RESTRICT,
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100),
    notes TEXT,
    PRIMARY KEY(item_id, revalidation_policy_id)
) STRICT;

CREATE TABLE claim_evidence (
    claim_evidence_id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE CASCADE,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    evidence_stance_id INTEGER NOT NULL REFERENCES evidence_stance(evidence_stance_id) ON DELETE RESTRICT,
    directness_rank INTEGER NOT NULL CHECK (directness_rank BETWEEN 1 AND 5),
    strength_rank INTEGER NOT NULL CHECK (strength_rank BETWEEN 1 AND 5),
    verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT,
    interpretation TEXT NOT NULL,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(claim_id, evidence_locator_id, evidence_stance_id)
) STRICT;

CREATE INDEX idx_claim_evidence_claim_stance ON claim_evidence(claim_id, evidence_stance_id, strength_rank DESC);
CREATE INDEX idx_claim_evidence_locator ON claim_evidence(evidence_locator_id, claim_id);

CREATE TABLE question_evidence (
    question_id INTEGER NOT NULL REFERENCES open_question(question_id) ON DELETE CASCADE,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    relevance_code TEXT NOT NULL,
    notes TEXT,
    PRIMARY KEY(question_id, evidence_locator_id, relevance_code)
) STRICT;

-- One deliberately typed, versioned mechanic-specific sidecar in the core.
CREATE TABLE ai_budget_mechanic_detail (
    ai_budget_mechanic_detail_id INTEGER PRIMARY KEY,
    mechanic_item_id INTEGER NOT NULL REFERENCES mechanic(item_id) ON DELETE RESTRICT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    budget_owner_scope_item_id INTEGER REFERENCES script_scope(item_id) ON DELETE RESTRICT,
    allocation_unit TEXT NOT NULL,
    allocation_stage TEXT NOT NULL,
    reserve_behavior TEXT,
    exhaustion_behavior TEXT,
    basis_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT,
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(mechanic_item_id, version_span_id)
) STRICT;

-- ---------------------------------------------------------------------------
-- 6. Typed graph relationships and impact-analysis rules
-- ---------------------------------------------------------------------------

CREATE TABLE item_relation (
    item_relation_id INTEGER PRIMARY KEY,
    source_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    relation_type_id INTEGER NOT NULL REFERENCES relation_type(relation_type_id) ON DELETE RESTRICT,
    target_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT,
    risk_level_id INTEGER NOT NULL REFERENCES risk_level(risk_level_id) ON DELETE RESTRICT,
    source_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT,
    rationale TEXT NOT NULL,
    impact_explanation TEXT NOT NULL,
    review_action TEXT,
    validation_action TEXT,
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (source_item_id <> target_item_id)
) STRICT;

CREATE UNIQUE INDEX uq_item_relation_current
    ON item_relation(source_item_id, relation_type_id, target_item_id, version_span_id)
    WHERE is_current = 1;
CREATE INDEX idx_item_relation_source ON item_relation(source_item_id, version_span_id, relation_type_id, is_current);
CREATE INDEX idx_item_relation_target ON item_relation(target_item_id, version_span_id, relation_type_id, is_current);

CREATE TABLE relation_evidence (
    item_relation_id INTEGER NOT NULL REFERENCES item_relation(item_relation_id) ON DELETE CASCADE,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    evidence_stance_id INTEGER NOT NULL REFERENCES evidence_stance(evidence_stance_id) ON DELETE RESTRICT,
    strength_rank INTEGER NOT NULL CHECK (strength_rank BETWEEN 1 AND 5),
    interpretation TEXT NOT NULL,
    PRIMARY KEY(item_relation_id, evidence_locator_id, evidence_stance_id)
) STRICT;

CREATE TABLE impact_rule (
    impact_rule_id INTEGER PRIMARY KEY,
    relation_type_id INTEGER NOT NULL REFERENCES relation_type(relation_type_id) ON DELETE RESTRICT,
    changed_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE RESTRICT,
    affected_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE RESTRICT,
    risk_level_id INTEGER NOT NULL REFERENCES risk_level(risk_level_id) ON DELETE RESTRICT,
    investigation_task_type_id INTEGER REFERENCES investigation_task_type(investigation_task_type_id) ON DELETE RESTRICT,
    preferred_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100),
    action_template TEXT NOT NULL,
    validation_template TEXT,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_impact_rule_match ON impact_rule(relation_type_id, changed_item_type_id, affected_item_type_id, is_active, priority DESC);

CREATE TABLE implementation_reference (
    implementation_reference_id INTEGER PRIMARY KEY,
    topic_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    example_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    reference_kind TEXT NOT NULL CHECK (reference_kind IN ('vanilla_example','mod_example','anti_example','compatibility_example')),
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    rationale TEXT NOT NULL,
    is_preferred INTEGER NOT NULL DEFAULT 0 CHECK (is_preferred IN (0,1)),
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(topic_item_id, example_item_id, reference_kind, version_span_id)
) STRICT;

CREATE INDEX idx_implementation_reference_topic ON implementation_reference(topic_item_id, version_span_id, reference_kind);

-- ---------------------------------------------------------------------------
-- 7. Explicit version-to-version change records
-- ---------------------------------------------------------------------------

CREATE TABLE version_change (
    version_change_id INTEGER PRIMARY KEY,
    change_key TEXT NOT NULL UNIQUE,
    from_version_id INTEGER NOT NULL REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    to_version_id INTEGER NOT NULL REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    change_kind_id INTEGER NOT NULL REFERENCES change_kind(change_kind_id) ON DELETE RESTRICT,
    summary TEXT NOT NULL,
    assessment_state_id INTEGER NOT NULL REFERENCES assessment_state(assessment_state_id) ON DELETE RESTRICT,
    confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT,
    risk_level_id INTEGER NOT NULL REFERENCES risk_level(risk_level_id) ON DELETE RESTRICT,
    review_required INTEGER NOT NULL CHECK (review_required IN (0,1)),
    migration_note TEXT,
    detected_by_verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (from_version_id <> to_version_id)
) STRICT;

CREATE INDEX idx_version_change_pair ON version_change(from_version_id, to_version_id, risk_level_id);

CREATE TABLE version_change_item (
    version_change_id INTEGER NOT NULL REFERENCES version_change(version_change_id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    role_code TEXT NOT NULL CHECK (role_code IN ('subject','old','new','affected','review')),
    notes TEXT,
    PRIMARY KEY(version_change_id, item_id, role_code)
) STRICT;

CREATE INDEX idx_version_change_item_item ON version_change_item(item_id, version_change_id, role_code);

CREATE TABLE version_change_evidence (
    version_change_id INTEGER NOT NULL REFERENCES version_change(version_change_id) ON DELETE CASCADE,
    evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    evidence_stance_id INTEGER NOT NULL REFERENCES evidence_stance(evidence_stance_id) ON DELETE RESTRICT,
    notes TEXT,
    PRIMARY KEY(version_change_id, evidence_locator_id, evidence_stance_id)
) STRICT;

-- ---------------------------------------------------------------------------
-- 8. Checklists and tool-routing
-- ---------------------------------------------------------------------------

CREATE TABLE checklist (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    change_type_id INTEGER NOT NULL REFERENCES change_type(change_type_id) ON DELETE RESTRICT,
    purpose TEXT NOT NULL,
    completion_criteria TEXT NOT NULL,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE TABLE checklist_target (
    checklist_item_id INTEGER NOT NULL REFERENCES checklist(item_id) ON DELETE CASCADE,
    target_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    applicability_note TEXT NOT NULL,
    PRIMARY KEY(checklist_item_id, target_item_id, version_span_id)
) STRICT;

CREATE INDEX idx_checklist_target_target ON checklist_target(target_item_id, version_span_id, checklist_item_id);

CREATE TABLE checklist_step (
    checklist_step_id INTEGER PRIMARY KEY,
    checklist_item_id INTEGER NOT NULL REFERENCES checklist(item_id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL CHECK (step_number >= 1),
    phase_code TEXT NOT NULL,
    title TEXT NOT NULL,
    instruction TEXT NOT NULL,
    rationale TEXT NOT NULL,
    is_required INTEGER NOT NULL CHECK (is_required IN (0,1)),
    is_blocking INTEGER NOT NULL CHECK (is_blocking IN (0,1)),
    tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    investigation_task_type_id INTEGER REFERENCES investigation_task_type(investigation_task_type_id) ON DELETE RESTRICT,
    expected_result TEXT,
    failure_action TEXT,
    version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(checklist_item_id, step_number)
) STRICT;

CREATE INDEX idx_checklist_step_order ON checklist_step(checklist_item_id, step_number);

CREATE TABLE checklist_step_item (
    checklist_step_id INTEGER NOT NULL REFERENCES checklist_step(checklist_step_id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    role_code TEXT NOT NULL CHECK (role_code IN ('inspect','modify','validate','compare','prerequisite','output')),
    notes TEXT,
    PRIMARY KEY(checklist_step_id, item_id, role_code)
) STRICT;

CREATE INDEX idx_checklist_step_item_item ON checklist_step_item(item_id, role_code, checklist_step_id);

CREATE TABLE tool (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    tool_kind TEXT NOT NULL,
    executable_or_entrypoint TEXT,
    authority_scope TEXT NOT NULL,
    default_invocation TEXT,
    output_locator_pattern TEXT,
    is_local_only INTEGER NOT NULL CHECK (is_local_only IN (0,1)),
    notes TEXT
) STRICT;

CREATE TABLE tool_capability (
    tool_capability_id INTEGER PRIMARY KEY,
    tool_item_id INTEGER NOT NULL REFERENCES tool(item_id) ON DELETE CASCADE,
    investigation_task_type_id INTEGER NOT NULL REFERENCES investigation_task_type(investigation_task_type_id) ON DELETE RESTRICT,
    capability_summary TEXT NOT NULL,
    invocation_template TEXT,
    expected_output TEXT NOT NULL,
    limitations TEXT,
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100),
    UNIQUE(tool_item_id, investigation_task_type_id, capability_summary)
) STRICT;

CREATE INDEX idx_tool_capability_task ON tool_capability(investigation_task_type_id, priority DESC, tool_item_id);

CREATE TABLE tool_route (
    tool_route_id INTEGER PRIMARY KEY,
    tool_capability_id INTEGER NOT NULL REFERENCES tool_capability(tool_capability_id) ON DELETE CASCADE,
    target_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    target_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE CASCADE,
    evidence_source_type_id INTEGER REFERENCES evidence_source_type(evidence_source_type_id) ON DELETE CASCADE,
    version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    route_priority INTEGER NOT NULL CHECK (route_priority BETWEEN 1 AND 100),
    instructions TEXT NOT NULL,
    fallback_tool_capability_id INTEGER REFERENCES tool_capability(tool_capability_id) ON DELETE RESTRICT,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    CHECK (
        (target_item_id IS NOT NULL) +
        (target_item_type_id IS NOT NULL) +
        (evidence_source_type_id IS NOT NULL) = 1
    )
) STRICT;

CREATE INDEX idx_tool_route_item ON tool_route(target_item_id, version_span_id, route_priority DESC) WHERE target_item_id IS NOT NULL;
CREATE INDEX idx_tool_route_type ON tool_route(target_item_type_id, version_span_id, route_priority DESC) WHERE target_item_type_id IS NOT NULL;
CREATE INDEX idx_tool_route_source_type ON tool_route(evidence_source_type_id, version_span_id, route_priority DESC) WHERE evidence_source_type_id IS NOT NULL;


-- ---------------------------------------------------------------------------
-- 9. Project snapshots, mods, playsets, datasets, and analysis sidecars
-- ---------------------------------------------------------------------------

CREATE TABLE repository_snapshot (
    repository_snapshot_id INTEGER PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    repository_name TEXT NOT NULL,
    repository_root TEXT,
    branch_name TEXT,
    commit_sha TEXT,
    worktree_state TEXT NOT NULL CHECK (worktree_state IN ('clean','dirty','unknown')),
    captured_at TEXT NOT NULL,
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_repository_snapshot_commit ON repository_snapshot(commit_sha, branch_name, captured_at);

CREATE TABLE mod_package (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    mod_key TEXT NOT NULL UNIQUE,
    steam_workshop_id TEXT,
    mod_scope TEXT NOT NULL CHECK (mod_scope IN ('vanilla','project_mod','workshop_mod','compatibility_patch','reference_mod','utility','unknown')),
    author_or_owner TEXT,
    homepage_uri TEXT,
    notes TEXT,
    UNIQUE(steam_workshop_id)
) STRICT;

CREATE TABLE mod_release (
    mod_release_id INTEGER PRIMARY KEY,
    mod_item_id INTEGER NOT NULL REFERENCES mod_package(item_id) ON DELETE RESTRICT,
    release_key TEXT NOT NULL UNIQUE,
    version_text TEXT,
    version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    supported_game_pattern TEXT,
    remote_file_id TEXT,
    descriptor_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    captured_at TEXT,
    release_status TEXT NOT NULL CHECK (release_status IN ('active','historical','missing','superseded','unknown')),
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(mod_item_id, version_text, captured_at)
) STRICT;

CREATE INDEX idx_mod_release_mod_version ON mod_release(mod_item_id, version_span_id, release_status);

CREATE TABLE source_root (
    source_root_id INTEGER PRIMARY KEY,
    root_key TEXT NOT NULL UNIQUE,
    root_kind TEXT NOT NULL CHECK (root_kind IN ('repository','vanilla_install','workshop_live','mod_snapshot','project_mod','launcher','logs','saves','generated','research','web_cache','other')),
    canonical_path TEXT NOT NULL,
    repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT,
    mod_release_id INTEGER REFERENCES mod_release(mod_release_id) ON DELETE RESTRICT,
    game_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    captured_at TEXT,
    availability_status TEXT NOT NULL CHECK (availability_status IN ('available','missing','moved','archived','unknown')),
    content_hash_algorithm TEXT,
    content_hash_value TEXT,
    authoritative_for TEXT,
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_source_root_context ON source_root(root_kind, game_version_id, mod_release_id, repository_snapshot_id);

CREATE TABLE playset (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    playset_key TEXT NOT NULL UNIQUE,
    manager_name TEXT,
    purpose TEXT NOT NULL,
    notes TEXT
) STRICT;

CREATE TABLE playset_snapshot (
    playset_snapshot_id INTEGER PRIMARY KEY,
    playset_item_id INTEGER NOT NULL REFERENCES playset(item_id) ON DELETE RESTRICT,
    snapshot_key TEXT NOT NULL UNIQUE,
    game_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT,
    source_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    captured_at TEXT NOT NULL,
    declared_mod_count INTEGER CHECK (declared_mod_count IS NULL OR declared_mod_count >= 0),
    is_current INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1)),
    resolution_status TEXT NOT NULL CHECK (resolution_status IN ('captured','validated','partial','stale','unknown')),
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE UNIQUE INDEX uq_playset_snapshot_current ON playset_snapshot(playset_item_id) WHERE is_current = 1;
CREATE INDEX idx_playset_snapshot_version ON playset_snapshot(game_version_id, captured_at);

CREATE TABLE playset_member (
    playset_member_id INTEGER PRIMARY KEY,
    playset_snapshot_id INTEGER NOT NULL REFERENCES playset_snapshot(playset_snapshot_id) ON DELETE CASCADE,
    mod_release_id INTEGER NOT NULL REFERENCES mod_release(mod_release_id) ON DELETE RESTRICT,
    source_root_id INTEGER REFERENCES source_root(source_root_id) ON DELETE RESTRICT,
    load_position INTEGER NOT NULL CHECK (load_position >= 1),
    enabled INTEGER NOT NULL DEFAULT 1 CHECK (enabled IN (0,1)),
    required_by_project INTEGER NOT NULL DEFAULT 0 CHECK (required_by_project IN (0,1)),
    descriptor_path TEXT,
    live_load_state TEXT NOT NULL DEFAULT 'unknown' CHECK (live_load_state IN ('loaded','disabled','missing','unknown')),
    notes TEXT,
    UNIQUE(playset_snapshot_id, mod_release_id),
    UNIQUE(playset_snapshot_id, load_position)
) STRICT;

CREATE INDEX idx_playset_member_order ON playset_member(playset_snapshot_id, enabled, load_position);

CREATE TABLE execution_context (
    execution_context_id INTEGER PRIMARY KEY,
    context_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    game_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT,
    version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT,
    playset_snapshot_id INTEGER REFERENCES playset_snapshot(playset_snapshot_id) ON DELETE RESTRICT,
    run_mode TEXT NOT NULL CHECK (run_mode IN ('static','normal_game','observer','save_analysis','log_analysis','research','database_validation','unknown')),
    platform TEXT,
    game_checksum TEXT,
    settings_summary TEXT,
    created_at TEXT NOT NULL,
    is_current INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1)),
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_execution_context_lookup ON execution_context(game_version_id, playset_snapshot_id, repository_snapshot_id, run_mode);

CREATE TABLE execution_context_item (
    execution_context_id INTEGER NOT NULL REFERENCES execution_context(execution_context_id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    role_code TEXT NOT NULL CHECK (role_code IN ('enabled_dlc','required_dlc','assumption','setting','target_subsystem','comparison_baseline','excluded_item','other')),
    state_code TEXT,
    notes TEXT,
    PRIMARY KEY(execution_context_id, item_id, role_code)
) STRICT;

CREATE INDEX idx_execution_context_item_item ON execution_context_item(item_id, role_code, execution_context_id);

CREATE TABLE dataset_schema (
    dataset_schema_id INTEGER PRIMARY KEY,
    source_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE CASCADE,
    schema_key TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    format_code TEXT NOT NULL CHECK (format_code IN ('csv','tsv','json','jsonl','parquet','xlsx','sqlite','other')),
    delimiter TEXT,
    has_header INTEGER NOT NULL CHECK (has_header IN (0,1)),
    row_count INTEGER CHECK (row_count IS NULL OR row_count >= 0),
    column_count INTEGER CHECK (column_count IS NULL OR column_count >= 0),
    schema_hash_algorithm TEXT,
    schema_hash_value TEXT,
    generated_by_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    is_authoritative_external INTEGER NOT NULL CHECK (is_authoritative_external IN (0,1)),
    storage_policy TEXT NOT NULL CHECK (storage_policy IN ('locator_only','selected_rows','normalized_facts','full_import_allowed')),
    stable_key_description TEXT,
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(source_artifact_id, schema_key, schema_version)
) STRICT;

CREATE INDEX idx_dataset_schema_key ON dataset_schema(schema_key, schema_version, source_artifact_id);

CREATE TABLE dataset_column (
    dataset_column_id INTEGER PRIMARY KEY,
    dataset_schema_id INTEGER NOT NULL REFERENCES dataset_schema(dataset_schema_id) ON DELETE CASCADE,
    ordinal INTEGER NOT NULL CHECK (ordinal >= 1),
    column_name TEXT NOT NULL,
    logical_type TEXT NOT NULL CHECK (logical_type IN ('integer','real','text','boolean','json','date','timestamp','path','identifier','expression','unknown')),
    semantic_role TEXT NOT NULL CHECK (semantic_role IN ('identifier','dimension','metric','status','provenance','locator','expression','count','text','other')),
    dimension_group TEXT,
    metric_key TEXT,
    unit TEXT,
    is_nullable INTEGER NOT NULL CHECK (is_nullable IN (0,1)),
    mapped_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE RESTRICT,
    mapped_field_item_id INTEGER REFERENCES field_definition(item_id) ON DELETE RESTRICT,
    description TEXT NOT NULL,
    UNIQUE(dataset_schema_id, ordinal),
    UNIQUE(dataset_schema_id, column_name),
    UNIQUE(dataset_schema_id, dataset_column_id)
) STRICT;

CREATE INDEX idx_dataset_column_semantics ON dataset_column(dataset_schema_id, semantic_role, dimension_group, metric_key);

CREATE TABLE dataset_key_column (
    dataset_schema_id INTEGER NOT NULL,
    dataset_column_id INTEGER NOT NULL,
    key_ordinal INTEGER NOT NULL CHECK (key_ordinal >= 1),
    normalization_rule TEXT,
    is_stable_across_versions INTEGER NOT NULL CHECK (is_stable_across_versions IN (0,1)),
    PRIMARY KEY(dataset_schema_id, dataset_column_id),
    UNIQUE(dataset_schema_id, key_ordinal),
    FOREIGN KEY(dataset_schema_id, dataset_column_id)
        REFERENCES dataset_column(dataset_schema_id, dataset_column_id) ON DELETE CASCADE
) STRICT;

CREATE TABLE definition_reference (
    definition_reference_id INTEGER PRIMARY KEY,
    object_definition_id INTEGER NOT NULL REFERENCES object_definition(object_definition_id) ON DELETE CASCADE,
    source_occurrence_id INTEGER REFERENCES object_field_occurrence(object_field_occurrence_id) ON DELETE SET NULL,
    stable_reference_key TEXT NOT NULL,
    reference_kind TEXT NOT NULL,
    target_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    target_key_text TEXT,
    target_object_kind_id INTEGER REFERENCES object_kind(object_kind_id) ON DELETE RESTRICT,
    resolution_status TEXT NOT NULL CHECK (resolution_status IN ('resolved','external','missing','ambiguous','ignored','unknown')),
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (target_item_id IS NOT NULL OR target_key_text IS NOT NULL),
    UNIQUE(object_definition_id, stable_reference_key)
) STRICT;

CREATE INDEX idx_definition_reference_target ON definition_reference(target_item_id, reference_kind, resolution_status);
CREATE INDEX idx_definition_reference_unresolved ON definition_reference(target_key_text, target_object_kind_id, resolution_status) WHERE target_item_id IS NULL;

CREATE TABLE playset_object_resolution (
    playset_object_resolution_id INTEGER PRIMARY KEY,
    playset_snapshot_id INTEGER NOT NULL REFERENCES playset_snapshot(playset_snapshot_id) ON DELETE CASCADE,
    object_item_id INTEGER NOT NULL REFERENCES game_object(item_id) ON DELETE RESTRICT,
    winning_definition_id INTEGER REFERENCES object_definition(object_definition_id) ON DELETE RESTRICT,
    resolution_status TEXT NOT NULL CHECK (resolution_status IN ('single','resolved','ambiguous','missing','not_applicable','unknown')),
    resolver_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    resolution_method TEXT NOT NULL,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    review_required INTEGER NOT NULL CHECK (review_required IN (0,1)),
    resolved_at TEXT,
    notes TEXT,
    UNIQUE(playset_snapshot_id, object_item_id)
) STRICT;

CREATE INDEX idx_playset_resolution_winner ON playset_object_resolution(playset_snapshot_id, winning_definition_id, resolution_status);

CREATE TABLE object_conflict (
    object_conflict_id INTEGER PRIMARY KEY,
    playset_snapshot_id INTEGER NOT NULL REFERENCES playset_snapshot(playset_snapshot_id) ON DELETE CASCADE,
    conflict_key TEXT NOT NULL,
    object_item_id INTEGER REFERENCES game_object(item_id) ON DELETE RESTRICT,
    conflict_kind TEXT NOT NULL CHECK (conflict_kind IN ('duplicate_definition','field_overlap','file_collision','replace_path','dependency','load_order','reference','unknown')),
    risk_level_id INTEGER NOT NULL REFERENCES risk_level(risk_level_id) ON DELETE RESTRICT,
    status_code TEXT NOT NULL CHECK (status_code IN ('open','reviewed','accepted','resolved','false_positive','stale')),
    winning_definition_id INTEGER REFERENCES object_definition(object_definition_id) ON DELETE RESTRICT,
    detected_by_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    detected_at TEXT,
    rationale TEXT NOT NULL,
    required_action TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(playset_snapshot_id, conflict_key)
) STRICT;

CREATE INDEX idx_object_conflict_queue ON object_conflict(playset_snapshot_id, status_code, risk_level_id, object_item_id);

CREATE TABLE object_conflict_member (
    object_conflict_id INTEGER NOT NULL REFERENCES object_conflict(object_conflict_id) ON DELETE CASCADE,
    object_definition_id INTEGER NOT NULL REFERENCES object_definition(object_definition_id) ON DELETE RESTRICT,
    member_role TEXT NOT NULL CHECK (member_role IN ('candidate','winner','loser','reference','unknown')),
    load_position INTEGER CHECK (load_position IS NULL OR load_position >= 1),
    differing_fields TEXT,
    notes TEXT,
    PRIMARY KEY(object_conflict_id, object_definition_id)
) STRICT;

CREATE TABLE validation_finding (
    validation_finding_id INTEGER PRIMARY KEY,
    verification_run_id INTEGER NOT NULL REFERENCES verification_run(verification_run_id) ON DELETE CASCADE,
    finding_key TEXT NOT NULL,
    category_code TEXT NOT NULL CHECK (category_code IN ('syntax','schema','reference','conflict','load_order','runtime_log','save_state','modeling','coverage','integrity','performance','other')),
    severity_code TEXT NOT NULL CHECK (severity_code IN ('info','warning','error','critical')),
    status_code TEXT NOT NULL CHECK (status_code IN ('open','accepted','resolved','false_positive','superseded')),
    primary_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    finding_summary TEXT NOT NULL,
    expected_text TEXT,
    actual_text TEXT,
    remediation TEXT,
    regression_key TEXT,
    first_observed_at TEXT,
    resolved_at TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    UNIQUE(verification_run_id, finding_key)
) STRICT;

CREATE INDEX idx_validation_finding_queue ON validation_finding(status_code, severity_code, category_code, primary_item_id);

CREATE TABLE analysis_model (
    item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE,
    model_key TEXT NOT NULL UNIQUE,
    model_kind TEXT NOT NULL CHECK (model_kind IN ('inventory','valuation','policy','diagnostic','comparison','coverage','observer','other')),
    purpose TEXT NOT NULL,
    authoritative_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT,
    authority_boundary TEXT NOT NULL,
    default_storage_policy TEXT NOT NULL CHECK (default_storage_policy IN ('locator_only','selected_facts','normalized_facts')),
    notes TEXT
) STRICT;

CREATE TABLE analysis_run (
    analysis_run_id INTEGER PRIMARY KEY,
    run_key TEXT NOT NULL UNIQUE,
    model_item_id INTEGER NOT NULL REFERENCES analysis_model(item_id) ON DELETE RESTRICT,
    execution_context_id INTEGER REFERENCES execution_context(execution_context_id) ON DELETE RESTRICT,
    verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT,
    repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT,
    model_version TEXT NOT NULL,
    generator_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    schema_version TEXT,
    command_or_method TEXT,
    input_fingerprint TEXT,
    started_at TEXT,
    completed_at TEXT,
    outcome_code TEXT NOT NULL CHECK (outcome_code IN ('passed','failed','partial','inconclusive','not_run')),
    reported_row_count INTEGER CHECK (reported_row_count IS NULL OR reported_row_count >= 0),
    notes TEXT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_analysis_run_model_context ON analysis_run(model_item_id, execution_context_id, completed_at, outcome_code);

CREATE TABLE analysis_run_artifact (
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE,
    source_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT,
    artifact_role TEXT NOT NULL CHECK (artifact_role IN ('input','output','report','manifest','log','source_code','comparison_baseline')),
    dataset_schema_id INTEGER REFERENCES dataset_schema(dataset_schema_id) ON DELETE RESTRICT,
    is_required INTEGER NOT NULL CHECK (is_required IN (0,1)),
    notes TEXT,
    PRIMARY KEY(analysis_run_id, source_artifact_id, artifact_role)
) STRICT;

CREATE TABLE analysis_scenario (
    analysis_scenario_id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE,
    scenario_key TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT NOT NULL,
    parent_scenario_id INTEGER REFERENCES analysis_scenario(analysis_scenario_id) ON DELETE RESTRICT,
    ordinal INTEGER NOT NULL CHECK (ordinal >= 1),
    assumptions_summary TEXT NOT NULL,
    is_baseline INTEGER NOT NULL CHECK (is_baseline IN (0,1)),
    UNIQUE(analysis_run_id, scenario_key),
    UNIQUE(analysis_run_id, ordinal)
) STRICT;

CREATE TABLE analysis_subject (
    analysis_subject_id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE,
    subject_key TEXT NOT NULL,
    subject_kind TEXT NOT NULL CHECK (subject_kind IN ('knowledge_item','external_record','runtime_entity','aggregate','policy_class','version_pair','other')),
    item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    source_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    parent_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE,
    external_type TEXT,
    external_key TEXT,
    label TEXT NOT NULL,
    status_code TEXT,
    notes TEXT,
    CHECK (item_id IS NOT NULL OR source_locator_id IS NOT NULL OR external_key IS NOT NULL OR subject_kind IN ('aggregate','policy_class','version_pair','other')),
    UNIQUE(analysis_run_id, subject_key)
) STRICT;

CREATE INDEX idx_analysis_subject_item ON analysis_subject(item_id, analysis_run_id, subject_kind);
CREATE INDEX idx_analysis_subject_external ON analysis_subject(external_type, external_key, analysis_run_id);

CREATE TABLE analysis_subject_member (
    analysis_subject_member_id INTEGER PRIMARY KEY,
    parent_subject_id INTEGER NOT NULL REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE,
    member_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE RESTRICT,
    member_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    role_code TEXT NOT NULL,
    ordinal INTEGER CHECK (ordinal IS NULL OR ordinal >= 1),
    quantity REAL,
    weight REAL,
    notes TEXT,
    CHECK ((member_subject_id IS NOT NULL) + (member_item_id IS NOT NULL) = 1),
    CHECK (member_subject_id IS NULL OR member_subject_id <> parent_subject_id)
) STRICT;

CREATE UNIQUE INDEX uq_analysis_subject_member
    ON analysis_subject_member(parent_subject_id, role_code, ifnull(member_subject_id,-1), ifnull(member_item_id,-1), ifnull(ordinal,-1));
CREATE INDEX idx_analysis_subject_member_reverse ON analysis_subject_member(member_subject_id, member_item_id, role_code);

CREATE TABLE analysis_metric (
    analysis_metric_id INTEGER PRIMARY KEY,
    model_item_id INTEGER NOT NULL REFERENCES analysis_model(item_id) ON DELETE CASCADE,
    metric_key TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value_type TEXT NOT NULL CHECK (value_type IN ('integer','real','text','boolean')),
    unit TEXT,
    aggregation_semantics TEXT NOT NULL CHECK (aggregation_semantics IN ('additive','ratio','score','categorical','set_count','identifier','boolean','other')),
    dimension_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE RESTRICT,
    allowed_subject_kind TEXT,
    description TEXT NOT NULL,
    stable_across_runs INTEGER NOT NULL CHECK (stable_across_runs IN (0,1)),
    UNIQUE(model_item_id, metric_key)
) STRICT;

CREATE INDEX idx_analysis_metric_lookup ON analysis_metric(model_item_id, aggregation_semantics, dimension_item_type_id);

CREATE TABLE analysis_value (
    analysis_value_id INTEGER PRIMARY KEY,
    analysis_subject_id INTEGER NOT NULL REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE,
    analysis_scenario_id INTEGER REFERENCES analysis_scenario(analysis_scenario_id) ON DELETE CASCADE,
    analysis_metric_id INTEGER NOT NULL REFERENCES analysis_metric(analysis_metric_id) ON DELETE RESTRICT,
    dimension_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    ordinal INTEGER NOT NULL DEFAULT 1 CHECK (ordinal >= 1),
    integer_value INTEGER,
    real_value REAL,
    text_value TEXT,
    boolean_value INTEGER CHECK (boolean_value IS NULL OR boolean_value IN (0,1)),
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    confidence_level_id INTEGER REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT,
    source_terms TEXT,
    notes TEXT,
    CHECK ((integer_value IS NOT NULL) + (real_value IS NOT NULL) + (text_value IS NOT NULL) + (boolean_value IS NOT NULL) = 1)
) STRICT;

CREATE UNIQUE INDEX uq_analysis_value_coordinate
    ON analysis_value(analysis_subject_id, ifnull(analysis_scenario_id,-1), analysis_metric_id, ifnull(dimension_item_id,-1), ordinal);
CREATE INDEX idx_analysis_value_metric ON analysis_value(analysis_metric_id, dimension_item_id, analysis_scenario_id);

CREATE TABLE analysis_gate (
    analysis_gate_id INTEGER PRIMARY KEY,
    analysis_subject_id INTEGER NOT NULL REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE,
    analysis_scenario_id INTEGER REFERENCES analysis_scenario(analysis_scenario_id) ON DELETE CASCADE,
    gate_kind TEXT NOT NULL CHECK (gate_kind IN ('prerequisite','potential','allow','event_flag','unlock_flag','capital_tier','availability','safety','consumer','other')),
    gate_key TEXT NOT NULL,
    target_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    phase_code TEXT,
    state_code TEXT NOT NULL CHECK (state_code IN ('satisfied','unsatisfied','conditional','unknown','not_applicable')),
    is_hard INTEGER NOT NULL CHECK (is_hard IN (0,1)),
    expression_text TEXT,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    notes TEXT
) STRICT;

CREATE UNIQUE INDEX uq_analysis_gate
    ON analysis_gate(analysis_subject_id, ifnull(analysis_scenario_id,-1), gate_kind, gate_key, ifnull(target_item_id,-1));
CREATE INDEX idx_analysis_gate_queue ON analysis_gate(state_code, is_hard, gate_kind, target_item_id);

CREATE TABLE analysis_policy (
    analysis_policy_id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE,
    analysis_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE,
    analysis_metric_id INTEGER REFERENCES analysis_metric(analysis_metric_id) ON DELETE RESTRICT,
    dimension_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    policy_kind TEXT NOT NULL CHECK (policy_kind IN ('formula','consumer','readiness','fallback','replacement','classification','zero_effect','detected_only','other')),
    decision_code TEXT NOT NULL,
    policy_status TEXT NOT NULL CHECK (policy_status IN ('active','draft','blocked','superseded')),
    formula_or_policy_text TEXT NOT NULL,
    numeric_parameter REAL,
    can_consume_code TEXT NOT NULL DEFAULT 'not_applicable' CHECK (can_consume_code IN ('yes','no','conditional','not_applicable')),
    fallback_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE RESTRICT,
    fallback_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT,
    confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    next_action TEXT,
    supersedes_policy_id INTEGER REFERENCES analysis_policy(analysis_policy_id) ON DELETE RESTRICT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    CHECK (supersedes_policy_id IS NULL OR supersedes_policy_id <> analysis_policy_id)
) STRICT;

CREATE INDEX idx_analysis_policy_lookup ON analysis_policy(analysis_run_id, policy_kind, policy_status, analysis_subject_id, analysis_metric_id);

CREATE TABLE analysis_issue (
    analysis_issue_id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE,
    analysis_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE,
    issue_type TEXT NOT NULL,
    issue_key TEXT NOT NULL,
    status_code TEXT NOT NULL CHECK (status_code IN ('open','resolved','classified_zero_effect','excluded','accepted','superseded')),
    severity_code TEXT NOT NULL CHECK (severity_code IN ('info','warning','error','critical')),
    priority INTEGER NOT NULL CHECK (priority BETWEEN 0 AND 100),
    exact_missing_evidence TEXT,
    resolution_summary TEXT,
    resolution_policy_id INTEGER REFERENCES analysis_policy(analysis_policy_id) ON DELETE RESTRICT,
    question_id INTEGER REFERENCES open_question(question_id) ON DELETE RESTRICT,
    evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT,
    notes TEXT,
    UNIQUE(analysis_run_id, analysis_subject_id, issue_type, issue_key)
) STRICT;

CREATE INDEX idx_analysis_issue_queue ON analysis_issue(status_code, severity_code, priority DESC, issue_type);

-- Cross-table consistency triggers for contextual and analysis sidecars.
CREATE TRIGGER trg_playset_resolution_winner_object_insert
BEFORE INSERT ON playset_object_resolution
WHEN NEW.winning_definition_id IS NOT NULL
BEGIN
    SELECT CASE WHEN (SELECT object_item_id FROM object_definition WHERE object_definition_id = NEW.winning_definition_id) <> NEW.object_item_id
        THEN RAISE(ABORT, 'playset winner definition belongs to a different object') END;
END;

CREATE TRIGGER trg_playset_resolution_winner_object_update
BEFORE UPDATE OF winning_definition_id, object_item_id ON playset_object_resolution
WHEN NEW.winning_definition_id IS NOT NULL
BEGIN
    SELECT CASE WHEN (SELECT object_item_id FROM object_definition WHERE object_definition_id = NEW.winning_definition_id) <> NEW.object_item_id
        THEN RAISE(ABORT, 'playset winner definition belongs to a different object') END;
END;

CREATE TRIGGER trg_object_conflict_member_object_insert
BEFORE INSERT ON object_conflict_member
WHEN (SELECT object_item_id FROM object_conflict WHERE object_conflict_id = NEW.object_conflict_id) IS NOT NULL
BEGIN
    SELECT CASE WHEN
        (SELECT od.object_item_id FROM object_definition od WHERE od.object_definition_id = NEW.object_definition_id) <>
        (SELECT oc.object_item_id FROM object_conflict oc WHERE oc.object_conflict_id = NEW.object_conflict_id)
        THEN RAISE(ABORT, 'conflict member definition belongs to a different object') END;
END;

CREATE TRIGGER trg_analysis_scenario_parent_run_insert
BEFORE INSERT ON analysis_scenario
WHEN NEW.parent_scenario_id IS NOT NULL
BEGIN
    SELECT CASE WHEN (SELECT analysis_run_id FROM analysis_scenario WHERE analysis_scenario_id = NEW.parent_scenario_id) <> NEW.analysis_run_id
        THEN RAISE(ABORT, 'analysis scenario parent belongs to a different run') END;
END;

CREATE TRIGGER trg_analysis_subject_parent_run_insert
BEFORE INSERT ON analysis_subject
WHEN NEW.parent_subject_id IS NOT NULL
BEGIN
    SELECT CASE WHEN (SELECT analysis_run_id FROM analysis_subject WHERE analysis_subject_id = NEW.parent_subject_id) <> NEW.analysis_run_id
        THEN RAISE(ABORT, 'analysis subject parent belongs to a different run') END;
END;

CREATE TRIGGER trg_analysis_value_consistency_insert
BEFORE INSERT ON analysis_value
BEGIN
    SELECT CASE WHEN
        (SELECT ar.model_item_id FROM analysis_subject s JOIN analysis_run ar ON ar.analysis_run_id=s.analysis_run_id WHERE s.analysis_subject_id=NEW.analysis_subject_id) <>
        (SELECT model_item_id FROM analysis_metric WHERE analysis_metric_id=NEW.analysis_metric_id)
        THEN RAISE(ABORT, 'analysis metric belongs to a different model') END;
    SELECT CASE WHEN NEW.analysis_scenario_id IS NOT NULL AND
        (SELECT analysis_run_id FROM analysis_scenario WHERE analysis_scenario_id=NEW.analysis_scenario_id) <>
        (SELECT analysis_run_id FROM analysis_subject WHERE analysis_subject_id=NEW.analysis_subject_id)
        THEN RAISE(ABORT, 'analysis value scenario belongs to a different run') END;
END;

CREATE TRIGGER trg_analysis_gate_consistency_insert
BEFORE INSERT ON analysis_gate
WHEN NEW.analysis_scenario_id IS NOT NULL
BEGIN
    SELECT CASE WHEN
        (SELECT analysis_run_id FROM analysis_scenario WHERE analysis_scenario_id=NEW.analysis_scenario_id) <>
        (SELECT analysis_run_id FROM analysis_subject WHERE analysis_subject_id=NEW.analysis_subject_id)
        THEN RAISE(ABORT, 'analysis gate scenario belongs to a different run') END;
END;

CREATE TRIGGER trg_analysis_policy_consistency_insert
BEFORE INSERT ON analysis_policy
BEGIN
    SELECT CASE WHEN NEW.analysis_subject_id IS NOT NULL AND
        (SELECT analysis_run_id FROM analysis_subject WHERE analysis_subject_id=NEW.analysis_subject_id) <> NEW.analysis_run_id
        THEN RAISE(ABORT, 'analysis policy subject belongs to a different run') END;
    SELECT CASE WHEN NEW.analysis_metric_id IS NOT NULL AND
        (SELECT model_item_id FROM analysis_metric WHERE analysis_metric_id=NEW.analysis_metric_id) <>
        (SELECT model_item_id FROM analysis_run WHERE analysis_run_id=NEW.analysis_run_id)
        THEN RAISE(ABORT, 'analysis policy metric belongs to a different model') END;
    SELECT CASE WHEN NEW.fallback_subject_id IS NOT NULL AND
        (SELECT analysis_run_id FROM analysis_subject WHERE analysis_subject_id=NEW.fallback_subject_id) <> NEW.analysis_run_id
        THEN RAISE(ABORT, 'analysis fallback subject belongs to a different run') END;
END;

CREATE TRIGGER trg_analysis_issue_consistency_insert
BEFORE INSERT ON analysis_issue
WHEN NEW.analysis_subject_id IS NOT NULL
BEGIN
    SELECT CASE WHEN
        (SELECT analysis_run_id FROM analysis_subject WHERE analysis_subject_id=NEW.analysis_subject_id) <> NEW.analysis_run_id
        THEN RAISE(ABORT, 'analysis issue subject belongs to a different run') END;
END;


-- ---------------------------------------------------------------------------
-- 10. Derived views for version applicability, impact paths, project context, and quality queues
-- ---------------------------------------------------------------------------

CREATE VIEW v_version_span_version AS
SELECT
    vs.version_span_id,
    vs.span_code,
    gv.game_version_id,
    gv.version_label,
    gv.version_order
FROM version_span AS vs
JOIN game_version AS gv
LEFT JOIN game_version AS minv ON minv.game_version_id = vs.min_version_id
LEFT JOIN game_version AS maxv ON maxv.game_version_id = vs.max_version_id
WHERE (vs.min_version_id IS NULL OR gv.version_order >= minv.version_order)
  AND (vs.max_version_id IS NULL OR gv.version_order <= maxv.version_order);

CREATE VIEW v_current_claim_assessment AS
SELECT
    ca.claim_assessment_id,
    ca.claim_id,
    ca.version_span_id,
    ast.state_code AS assessment_state,
    cl.confidence_code,
    cl.rank_value AS confidence_rank,
    ca.verification_run_id,
    ca.execution_context_id,
    ca.assessed_by_actor_id,
    ca.assessed_at,
    ca.basis_summary,
    ca.reverify_after
FROM claim_assessment AS ca
JOIN assessment_state AS ast ON ast.assessment_state_id = ca.assessment_state_id
JOIN confidence_level AS cl ON cl.confidence_level_id = ca.confidence_level_id
WHERE ca.is_current = 1;

CREATE VIEW v_claim_evidence_summary AS
SELECT
    c.claim_id,
    c.primary_item_id,
    SUM(CASE WHEN es.stance_code = 'supports' THEN 1 ELSE 0 END) AS supporting_count,
    SUM(CASE WHEN es.stance_code = 'contradicts' THEN 1 ELSE 0 END) AS contradicting_count,
    SUM(CASE WHEN es.stance_code = 'qualifies' THEN 1 ELSE 0 END) AS qualifying_count,
    MAX(CASE WHEN es.stance_code = 'supports' THEN ce.strength_rank END) AS strongest_support,
    MAX(CASE WHEN es.stance_code = 'contradicts' THEN ce.strength_rank END) AS strongest_contradiction
FROM claim AS c
LEFT JOIN claim_evidence AS ce ON ce.claim_id = c.claim_id
LEFT JOIN evidence_stance AS es ON es.evidence_stance_id = ce.evidence_stance_id
GROUP BY c.claim_id, c.primary_item_id;

CREATE VIEW v_impact_arc AS
SELECT
    ir.item_relation_id,
    ir.relation_type_id,
    ir.source_item_id AS changed_item_id,
    ir.target_item_id AS affected_item_id,
    rt.type_code AS relation_type_code,
    rt.type_name AS relation_type_name,
    'forward' AS traversal_direction,
    ir.version_span_id,
    ir.risk_level_id,
    ir.confidence_level_id,
    ir.rationale,
    ir.impact_explanation,
    ir.review_action,
    ir.validation_action
FROM item_relation AS ir
JOIN relation_type AS rt ON rt.relation_type_id = ir.relation_type_id
WHERE ir.is_current = 1
  AND rt.impact_propagation_mode IN ('forward','both')
UNION ALL
SELECT
    ir.item_relation_id,
    ir.relation_type_id,
    ir.target_item_id AS changed_item_id,
    ir.source_item_id AS affected_item_id,
    rt.type_code AS relation_type_code,
    rt.type_name AS relation_type_name,
    'reverse' AS traversal_direction,
    ir.version_span_id,
    ir.risk_level_id,
    ir.confidence_level_id,
    ir.rationale,
    ir.impact_explanation,
    ir.review_action,
    ir.validation_action
FROM item_relation AS ir
JOIN relation_type AS rt ON rt.relation_type_id = ir.relation_type_id
WHERE ir.is_current = 1
  AND rt.impact_propagation_mode IN ('reverse','both');

CREATE VIEW v_reverification_queue AS
SELECT
    c.claim_id,
    c.statement,
    ki.canonical_key AS primary_item_key,
    ast.state_code AS current_state,
    cl.confidence_code,
    ca.assessed_at,
    ca.reverify_after,
    gv.game_version_id AS target_version_id,
    gv.version_label AS target_version,
    CASE
        WHEN ast.state_code IN ('stale','unknown','uncertain','contradicted') THEN 'assessment_state_' || ast.state_code
        WHEN ca.reverify_after IS NOT NULL AND ca.reverify_after <= strftime('%Y-%m-%dT%H:%M:%fZ','now') THEN 'scheduled_reverification_due'
        WHEN vsv.game_version_id IS NULL THEN 'target_version_not_covered'
        ELSE 'not_due'
    END AS reason_code,
    CASE
        WHEN ast.state_code IN ('stale','unknown','uncertain','contradicted') THEN 1
        WHEN ca.reverify_after IS NOT NULL AND ca.reverify_after <= strftime('%Y-%m-%dT%H:%M:%fZ','now') THEN 1
        WHEN vsv.game_version_id IS NULL AND (
            EXISTS (SELECT 1 FROM claim_revalidation_policy crp WHERE crp.claim_id = c.claim_id)
            OR EXISTS (SELECT 1 FROM item_revalidation_policy irp WHERE irp.item_id = c.primary_item_id)
        ) THEN 1
        ELSE 0
    END AS requires_reverification
FROM claim AS c
JOIN knowledge_item AS ki ON ki.item_id = c.primary_item_id
JOIN claim_assessment AS ca ON ca.claim_id = c.claim_id AND ca.is_current = 1
JOIN assessment_state AS ast ON ast.assessment_state_id = ca.assessment_state_id
JOIN confidence_level AS cl ON cl.confidence_level_id = ca.confidence_level_id
JOIN game_version AS gv ON gv.is_primary_target = 1
LEFT JOIN v_version_span_version AS vsv
  ON vsv.version_span_id = ca.version_span_id
 AND vsv.game_version_id = gv.game_version_id;

CREATE VIEW v_sidecar_type_mismatch AS
SELECT ki.item_id, ki.canonical_key, it.type_code AS actual_type, 'mechanic_family' AS expected_type
FROM mechanic_family x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'mechanic_family'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'mechanic'
FROM mechanic x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'mechanic'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'subsystem'
FROM subsystem x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'subsystem'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'game_object|resource|technology'
FROM game_object x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code NOT IN ('game_object','resource','technology')
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'file'
FROM file_asset x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'file'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'trigger|effect|modifier|define'
FROM script_symbol x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code NOT IN ('trigger','effect','modifier','define')
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'field'
FROM field_definition x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'field'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'scope'
FROM script_scope x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'scope'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'checklist'
FROM checklist x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'checklist'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'tool'
FROM tool x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'tool'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'mod'
FROM mod_package x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'mod'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'playset'
FROM playset x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'playset'
UNION ALL
SELECT ki.item_id, ki.canonical_key, it.type_code, 'analysis_model'
FROM analysis_model x JOIN knowledge_item ki ON ki.item_id=x.item_id JOIN item_type it ON it.item_type_id=ki.item_type_id
WHERE it.type_code <> 'analysis_model';



CREATE VIEW v_current_playset_member AS
SELECT
    ps.playset_snapshot_id,
    p.playset_key,
    ps.snapshot_key,
    gv.version_label,
    pm.load_position,
    mp.item_id AS mod_item_id,
    ki.display_name AS mod_name,
    mp.steam_workshop_id,
    mr.release_key,
    sr.root_key,
    sr.canonical_path,
    pm.enabled,
    pm.required_by_project,
    pm.live_load_state
FROM playset_snapshot ps
JOIN playset p ON p.item_id=ps.playset_item_id
LEFT JOIN game_version gv ON gv.game_version_id=ps.game_version_id
JOIN playset_member pm ON pm.playset_snapshot_id=ps.playset_snapshot_id
JOIN mod_release mr ON mr.mod_release_id=pm.mod_release_id
JOIN mod_package mp ON mp.item_id=mr.mod_item_id
JOIN knowledge_item ki ON ki.item_id=mp.item_id
LEFT JOIN source_root sr ON sr.source_root_id=pm.source_root_id
WHERE ps.is_current=1;

CREATE VIEW v_playset_object_winner AS
SELECT
    por.playset_snapshot_id,
    ps.snapshot_key,
    por.object_item_id,
    ki.canonical_key AS object_key,
    por.resolution_status,
    por.winning_definition_id,
    od.mod_release_id,
    mr.release_key,
    od.source_root_id,
    el.relative_path,
    el.symbol_or_object_key,
    por.review_required,
    por.resolution_method
FROM playset_object_resolution por
JOIN playset_snapshot ps ON ps.playset_snapshot_id=por.playset_snapshot_id
JOIN knowledge_item ki ON ki.item_id=por.object_item_id
LEFT JOIN object_definition od ON od.object_definition_id=por.winning_definition_id
LEFT JOIN mod_release mr ON mr.mod_release_id=od.mod_release_id
LEFT JOIN evidence_locator el ON el.evidence_locator_id=od.evidence_locator_id;

CREATE VIEW v_analysis_value_typed AS
SELECT
    av.analysis_value_id,
    ar.run_key,
    am.model_key,
    s.subject_key,
    s.subject_kind,
    sc.scenario_key,
    m.metric_key,
    dki.canonical_key AS dimension_item_key,
    m.value_type,
    m.unit,
    av.integer_value,
    av.real_value,
    av.text_value,
    av.boolean_value,
    av.confidence_level_id,
    av.evidence_locator_id,
    av.source_terms
FROM analysis_value av
JOIN analysis_subject s ON s.analysis_subject_id=av.analysis_subject_id
JOIN analysis_run ar ON ar.analysis_run_id=s.analysis_run_id
JOIN analysis_model am ON am.item_id=ar.model_item_id
JOIN analysis_metric m ON m.analysis_metric_id=av.analysis_metric_id
LEFT JOIN analysis_scenario sc ON sc.analysis_scenario_id=av.analysis_scenario_id
LEFT JOIN knowledge_item dki ON dki.item_id=av.dimension_item_id;

CREATE VIEW v_open_analysis_issue AS
SELECT
    ai.analysis_issue_id,
    ar.run_key,
    am.model_key,
    s.subject_key,
    ai.issue_type,
    ai.issue_key,
    ai.severity_code,
    ai.priority,
    ai.exact_missing_evidence,
    ai.resolution_summary,
    ai.question_id
FROM analysis_issue ai
JOIN analysis_run ar ON ar.analysis_run_id=ai.analysis_run_id
JOIN analysis_model am ON am.item_id=ar.model_item_id
LEFT JOIN analysis_subject s ON s.analysis_subject_id=ai.analysis_subject_id
WHERE ai.status_code='open';

CREATE VIEW v_dataset_schema_drift AS
WITH ranked AS (
    SELECT
        ds.*,
        lag(ds.dataset_schema_id) OVER (PARTITION BY ds.schema_key ORDER BY ds.dataset_schema_id) AS previous_schema_id
    FROM dataset_schema ds
)
SELECT
    r.schema_key,
    r.previous_schema_id,
    r.dataset_schema_id AS current_schema_id,
    p.schema_version AS previous_schema_version,
    r.schema_version AS current_schema_version,
    p.column_count AS previous_column_count,
    r.column_count AS current_column_count,
    CASE
        WHEN r.previous_schema_id IS NULL THEN 'initial'
        WHEN p.schema_hash_value = r.schema_hash_value THEN 'unchanged'
        WHEN p.column_count <> r.column_count THEN 'column_count_changed'
        ELSE 'schema_changed'
    END AS drift_status
FROM ranked r
LEFT JOIN dataset_schema p ON p.dataset_schema_id=r.previous_schema_id;

CREATE VIEW v_analysis_dimension_type_mismatch AS
SELECT
    av.analysis_value_id,
    m.metric_key,
    m.dimension_item_type_id AS expected_item_type_id,
    ki.item_type_id AS actual_item_type_id,
    ki.canonical_key AS dimension_item_key
FROM analysis_value av
JOIN analysis_metric m ON m.analysis_metric_id=av.analysis_metric_id
JOIN knowledge_item ki ON ki.item_id=av.dimension_item_id
WHERE av.dimension_item_id IS NOT NULL
  AND m.dimension_item_type_id IS NOT NULL
  AND m.dimension_item_type_id <> ki.item_type_id;


-- ---------------------------------------------------------------------------
-- 11. Full-text indexes. They are derived search accelerators, not authority.
-- ---------------------------------------------------------------------------

CREATE VIRTUAL TABLE item_fts USING fts5(
    canonical_key,
    display_name,
    summary,
    content='knowledge_item',
    content_rowid='item_id',
    tokenize='unicode61 remove_diacritics 2'
);

CREATE VIRTUAL TABLE claim_fts USING fts5(
    statement,
    context,
    epistemic_note,
    content='claim',
    content_rowid='claim_id',
    tokenize='unicode61 remove_diacritics 2'
);

CREATE VIRTUAL TABLE question_fts USING fts5(
    question_text,
    uncertainty_reason,
    content='open_question',
    content_rowid='question_id',
    tokenize='unicode61 remove_diacritics 2'
);

CREATE VIRTUAL TABLE evidence_fts USING fts5(
    label,
    excerpt,
    evidence_summary,
    retrieval_instructions,
    content='evidence_locator',
    content_rowid='evidence_locator_id',
    tokenize='unicode61 remove_diacritics 2'
);

CREATE TRIGGER trg_knowledge_item_fts_ai AFTER INSERT ON knowledge_item BEGIN
    INSERT INTO item_fts(rowid, canonical_key, display_name, summary)
    VALUES (new.item_id, new.canonical_key, new.display_name, new.summary);
END;
CREATE TRIGGER trg_knowledge_item_fts_ad AFTER DELETE ON knowledge_item BEGIN
    INSERT INTO item_fts(item_fts, rowid, canonical_key, display_name, summary)
    VALUES ('delete', old.item_id, old.canonical_key, old.display_name, old.summary);
END;
CREATE TRIGGER trg_knowledge_item_fts_au AFTER UPDATE ON knowledge_item BEGIN
    INSERT INTO item_fts(item_fts, rowid, canonical_key, display_name, summary)
    VALUES ('delete', old.item_id, old.canonical_key, old.display_name, old.summary);
    INSERT INTO item_fts(rowid, canonical_key, display_name, summary)
    VALUES (new.item_id, new.canonical_key, new.display_name, new.summary);
END;

CREATE TRIGGER trg_claim_fts_ai AFTER INSERT ON claim BEGIN
    INSERT INTO claim_fts(rowid, statement, context, epistemic_note)
    VALUES (new.claim_id, new.statement, new.context, new.epistemic_note);
END;
CREATE TRIGGER trg_claim_fts_ad AFTER DELETE ON claim BEGIN
    INSERT INTO claim_fts(claim_fts, rowid, statement, context, epistemic_note)
    VALUES ('delete', old.claim_id, old.statement, old.context, old.epistemic_note);
END;
CREATE TRIGGER trg_claim_fts_au AFTER UPDATE ON claim BEGIN
    INSERT INTO claim_fts(claim_fts, rowid, statement, context, epistemic_note)
    VALUES ('delete', old.claim_id, old.statement, old.context, old.epistemic_note);
    INSERT INTO claim_fts(rowid, statement, context, epistemic_note)
    VALUES (new.claim_id, new.statement, new.context, new.epistemic_note);
END;

CREATE TRIGGER trg_question_fts_ai AFTER INSERT ON open_question BEGIN
    INSERT INTO question_fts(rowid, question_text, uncertainty_reason)
    VALUES (new.question_id, new.question_text, new.uncertainty_reason);
END;
CREATE TRIGGER trg_question_fts_ad AFTER DELETE ON open_question BEGIN
    INSERT INTO question_fts(question_fts, rowid, question_text, uncertainty_reason)
    VALUES ('delete', old.question_id, old.question_text, old.uncertainty_reason);
END;
CREATE TRIGGER trg_question_fts_au AFTER UPDATE ON open_question BEGIN
    INSERT INTO question_fts(question_fts, rowid, question_text, uncertainty_reason)
    VALUES ('delete', old.question_id, old.question_text, old.uncertainty_reason);
    INSERT INTO question_fts(rowid, question_text, uncertainty_reason)
    VALUES (new.question_id, new.question_text, new.uncertainty_reason);
END;

CREATE TRIGGER trg_evidence_fts_ai AFTER INSERT ON evidence_locator BEGIN
    INSERT INTO evidence_fts(rowid, label, excerpt, evidence_summary, retrieval_instructions)
    VALUES (new.evidence_locator_id, new.label, new.excerpt, new.evidence_summary, new.retrieval_instructions);
END;
CREATE TRIGGER trg_evidence_fts_ad AFTER DELETE ON evidence_locator BEGIN
    INSERT INTO evidence_fts(evidence_fts, rowid, label, excerpt, evidence_summary, retrieval_instructions)
    VALUES ('delete', old.evidence_locator_id, old.label, old.excerpt, old.evidence_summary, old.retrieval_instructions);
END;
CREATE TRIGGER trg_evidence_fts_au AFTER UPDATE ON evidence_locator BEGIN
    INSERT INTO evidence_fts(evidence_fts, rowid, label, excerpt, evidence_summary, retrieval_instructions)
    VALUES ('delete', old.evidence_locator_id, old.label, old.excerpt, old.evidence_summary, old.retrieval_instructions);
    INSERT INTO evidence_fts(rowid, label, excerpt, evidence_summary, retrieval_instructions)
    VALUES (new.evidence_locator_id, new.label, new.excerpt, new.evidence_summary, new.retrieval_instructions);
END;

INSERT INTO schema_metadata(metadata_key, metadata_value, description) VALUES
('schema_name', 'stellaris_ai_mod_knowledge_base', 'Stable logical schema identifier.'),
('schema_revision', '2', 'Project-aware revision with playset, dataset, and analysis sidecars.'),
('minimum_sqlite_version', '3.37.0', 'STRICT table support is required.'),
('fts_requirement', 'FTS5', 'Full-text virtual tables require an SQLite build with FTS5.'),
('impact_direction_convention', 'relation_type.impact_propagation_mode', 'v_impact_arc expands stored relations into changed-item to affected-item arcs.'),
('write_policy', 'short explicit transactions; append/supersede claims and assessments', 'Recommended AI-agent update discipline.');

COMMIT;
