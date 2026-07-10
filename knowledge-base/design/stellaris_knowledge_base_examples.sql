-- Stellaris AI Mod Knowledge Base
-- Project-aware representative seed data and executable query examples, revision 2.
--
-- Run after stellaris_knowledge_base_schema.sql against a new database.
-- The records combine a small illustrative core with project-specific schema catalogs and selected normalized facts. They demonstrate the model and
-- query patterns; they do not claim to be a complete catalogue of Stellaris 4.4.5.
-- Replace representative vanilla paths, line ranges, hashes, and excerpts with locally
-- verified locators as the knowledge base is populated.

PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;

BEGIN IMMEDIATE;

INSERT INTO schema_metadata(metadata_key, metadata_value, description) VALUES
('seed_profile', 'representative_examples_2026-07-10', 'Identifies the illustrative seed data loaded by this file.');

-- ---------------------------------------------------------------------------
-- A. Actors, one traceable seed change set, and controlled vocabularies
-- ---------------------------------------------------------------------------

INSERT INTO actor(actor_id, actor_key, display_name, actor_type, external_identifier, notes) VALUES
(1, 'human:mod-owner', 'Mod owner', 'human', NULL, 'Primary local maintainer.'),
(2, 'ai:seed-designer', 'Seed-design AI agent', 'ai_agent', 'example-agent-1', 'Created representative seed records.'),
(3, 'tool:repo-validator', 'Repository validator', 'tool', 'tools/validate_stellar_ai_director_patch.py', 'Deterministic project validator.'),
(4, 'system:knowledge-base', 'Knowledge-base system', 'system', NULL, 'Reserved for database-maintained records.');

INSERT INTO change_set(
    change_set_id, change_set_key, title, purpose, actor_id, state,
    opened_at, committed_at, repository_commit, transaction_note
) VALUES (
    1, 'seed:2026-07-10', 'Representative Stellaris AI knowledge seed',
    'Demonstrate versioned claims, provenance, impact paths, checklists, and tool routing.',
    2, 'committed', '2026-07-10T16:00:00Z', '2026-07-10T16:30:00Z',
    'example-only', 'All example records in this script belong to this change set.'
);

INSERT INTO lifecycle_state(lifecycle_state_id, state_code, state_name, is_active, description) VALUES
(1, 'active', 'Active', 1, 'Current and available for normal use.'),
(2, 'draft', 'Draft', 1, 'Not yet accepted as current project knowledge.'),
(3, 'retired', 'Retired', 0, 'Preserved for history but no longer current.');

INSERT INTO confidence_level(confidence_level_id, confidence_code, confidence_name, rank_value, description) VALUES
(1, 'unknown', 'Unknown', 0, 'No defensible confidence assigned.'),
(2, 'low', 'Low', 25, 'Tentative; material gaps remain.'),
(3, 'medium', 'Medium', 50, 'Plausible and partly supported.'),
(4, 'high', 'High', 75, 'Strongly supported with limited residual uncertainty.'),
(5, 'very_high', 'Very high', 95, 'Multiple direct, reproducible sources or an authoritative direct source.');

INSERT INTO assessment_state(
    assessment_state_id, state_code, state_name, rank_value, is_usable_as_fact, description
) VALUES
(1, 'verified', 'Verified', 100, 1, 'Directly supported for the stated version span.'),
(2, 'inferred', 'Inferred', 70, 1, 'Reasoned from evidence but not directly demonstrated.'),
(3, 'uncertain', 'Uncertain', 40, 0, 'Material uncertainty remains.'),
(4, 'contradicted', 'Contradicted', 20, 0, 'Material evidence contradicts the statement.'),
(5, 'stale', 'Stale', 30, 0, 'Previously useful but overdue or version-invalidated.'),
(6, 'unknown', 'Unknown', 0, 0, 'No adequate evidence yet.'),
(7, 'not_applicable', 'Not applicable', 100, 0, 'Does not apply to the stated version or context.');

INSERT INTO item_type(item_type_id, type_code, type_name, description) VALUES
(1, 'mechanic_family', 'Mechanic family', 'Broad family used to organize mechanics.'),
(2, 'mechanic', 'Mechanic', 'A coherent Stellaris behavior or modding concept.'),
(3, 'subsystem', 'Mod subsystem', 'A maintainable subsystem of the target mod.'),
(4, 'game_object', 'Game object', 'A vanilla, mod, generated, or external-mod definition.'),
(5, 'field', 'Object field', 'A named field on a class of scripted object.'),
(6, 'trigger', 'Trigger', 'Built-in or scripted condition surface.'),
(7, 'effect', 'Effect', 'Built-in or scripted action surface.'),
(8, 'scope', 'Scope', 'Script execution or object scope.'),
(9, 'modifier', 'Modifier', 'Named modifier surface.'),
(10, 'define', 'Define', 'Engine define exposed through data files.'),
(11, 'resource', 'Resource', 'Stellaris resource represented as a typed game object.'),
(12, 'technology', 'Technology', 'Stellaris technology represented as a typed game object.'),
(13, 'file', 'File or corpus path', 'A precise implementation or evidence path.'),
(14, 'tool', 'Tool', 'An existing authoritative or investigative tool.'),
(15, 'checklist', 'Checklist', 'A reusable change and validation plan.'),
(16, 'system', 'System or environment', 'A corpus, playset, runtime, or other environment.'),
(17, 'other', 'Other', 'A stable item not yet assigned a more specific type.');

INSERT INTO object_kind(object_kind_id, kind_code, kind_name, definition_folder, description) VALUES
(1, 'economic_plan', 'Economic plan', 'common/economic_plans', 'AI economic-plan definition.'),
(2, 'ai_budget', 'AI budget', 'common/ai_budget', 'AI resource-budget definition.'),
(3, 'country_type', 'Country type', 'common/country_types', 'Country-type definition and AI eligibility surface.'),
(4, 'personality', 'AI personality', 'common/personalities', 'Diplomacy and strategic personality definition.'),
(5, 'building', 'Building', 'common/buildings', 'Planet building definition.'),
(6, 'job', 'Job', 'common/pop_jobs', 'Pop job definition.'),
(7, 'resource', 'Resource', 'common/resources', 'Resource definition or stable resource key.'),
(8, 'technology', 'Technology', 'common/technology', 'Technology definition.'),
(9, 'policy', 'Policy', 'common/policies', 'Policy definition.'),
(10, 'war_goal', 'War goal', 'common/war_goals', 'War-goal definition.'),
(11, 'casus_belli', 'Casus belli', 'common/casus_belli', 'Casus-belli definition.');

INSERT INTO script_symbol_kind(script_symbol_kind_id, kind_code, kind_name, description) VALUES
(1, 'trigger', 'Built-in trigger', 'Engine-exposed condition.'),
(2, 'effect', 'Built-in effect', 'Engine-exposed action.'),
(3, 'scripted_trigger', 'Scripted trigger', 'Reusable trigger implemented in script.'),
(4, 'scripted_effect', 'Scripted effect', 'Reusable effect implemented in script.'),
(5, 'modifier', 'Modifier', 'Named modifier identifier.'),
(6, 'define', 'Define', 'Named value in a defines surface.');

INSERT INTO claim_type(claim_type_id, type_code, type_name, description) VALUES
(1, 'behavior', 'Behavior', 'How a mechanic behaves.'),
(2, 'structure', 'Structure', 'What an object, field, or script surface contains.'),
(3, 'compatibility', 'Compatibility', 'Version, DLC, or mod-stack compatibility claim.'),
(4, 'process', 'Process', 'Required investigative or maintenance procedure.'),
(5, 'hypothesis', 'Hypothesis', 'Testable explanation not yet verified.'),
(6, 'negative', 'Negative finding', 'A verified absence, limitation, or lack of proof.');

INSERT INTO evidence_source_type(
    evidence_source_type_id, type_code, type_name, default_reliability_rank,
    authoritative_scope, is_primary_evidence, description
) VALUES
(1, 'vanilla_files', 'Vanilla files', 95, 'Scripted definitions in the captured game version', 1, 'Exact local vanilla files.'),
(2, 'generated_docs', 'Generated Stellaris documentation', 85, 'Exposed triggers, effects, modifiers, and scopes', 1, 'Version-matched generated documentation.'),
(3, 'cwtools', 'CWTools', 85, 'Schema and static diagnostics', 1, 'CWTools schema and diagnostics.'),
(4, 'irony', 'Irony Mod Manager', 90, 'Active-playset conflicts, ordering, and merged winners', 1, 'Conflict and load-order evidence.'),
(5, 'repository', 'Project repository', 90, 'Current mod source and deterministic scripts', 1, 'Version-controlled project files.'),
(6, 'research_note', 'Research note', 65, 'Documented conclusions and investigation history', 0, 'Source-backed local notes.'),
(7, 'runtime_log', 'Runtime log', 80, 'Observed parser/runtime messages for a specific run', 1, 'Game and error logs.'),
(8, 'save', 'Save evidence', 80, 'Persisted state for a specific game date and playset', 1, 'Save-field evidence.'),
(9, 'experiment', 'Controlled experiment', 90, 'Specified setup and observed result', 1, 'Reproducible experiment result.'),
(10, 'git_history', 'Git history', 85, 'Repository change provenance', 1, 'Commit and diff evidence.'),
(11, 'web', 'Web source', 55, 'Externally published information', 0, 'Web evidence; local revalidation may still be required.'),
(12, 'tool_output', 'Repository tool output', 85, 'Deterministic output for the captured inputs', 1, 'Validator, audit, or report output.'),
(13, 'patch_notes', 'Patch notes', 80, 'Declared version changes', 1, 'Official or preserved patch-note source.');

INSERT INTO locator_type(locator_type_id, type_code, type_name, description) VALUES
(1, 'file_lines', 'File line range', 'Path and line range.'),
(2, 'object_key', 'Object key', 'Object identifier within a source file or corpus.'),
(3, 'symbol', 'Symbol', 'Trigger, effect, modifier, define, or code symbol.'),
(4, 'dataset_record', 'Dataset record', 'Dataset name plus stable record key.'),
(5, 'command_output', 'Command output', 'Command and output region.'),
(6, 'log_range', 'Log range', 'Timestamped or line-bounded runtime log evidence.'),
(7, 'save_field', 'Save field', 'Save path and field/key locator.'),
(8, 'commit', 'Git commit', 'Commit SHA, path, and optional diff anchor.'),
(9, 'url_section', 'URL section', 'URL plus heading or section.'),
(10, 'note_section', 'Note section', 'Named section in a research or design note.');

INSERT INTO evidence_stance(evidence_stance_id, stance_code, stance_name, description) VALUES
(1, 'supports', 'Supports', 'Evidence tends to support the claim or relation.'),
(2, 'contradicts', 'Contradicts', 'Evidence tends to contradict it.'),
(3, 'qualifies', 'Qualifies', 'Evidence narrows, conditions, or limits it.'),
(4, 'context', 'Context only', 'Relevant context without directional support.');

INSERT INTO risk_level(risk_level_id, risk_code, risk_name, rank_value, description) VALUES
(1, 'low', 'Low', 20, 'Localized review is normally sufficient.'),
(2, 'medium', 'Medium', 50, 'Several connected surfaces should be reviewed.'),
(3, 'high', 'High', 75, 'Cross-system or compatibility consequences are likely.'),
(4, 'critical', 'Critical', 95, 'Failure can invalidate broad behavior or prevent loading.');

INSERT INTO relation_type(
    relation_type_id, type_code, type_name, inverse_name, description,
    impact_propagation_mode, is_transitive_hint
) VALUES
(1, 'part_of', 'is part of', 'contains', 'Child belongs to a broader mechanic, family, or subsystem.', 'both', 1),
(2, 'field_of', 'is a field of', 'has field', 'Field belongs to an object or object class.', 'both', 1),
(3, 'implements', 'implements', 'is implemented by', 'Definition or object implements a mechanic.', 'both', 1),
(4, 'implemented_in', 'is implemented in', 'implements item', 'Mechanic or object is implemented in a file.', 'both', 1),
(5, 'depends_on', 'depends on', 'is dependency of', 'Source requires target; target changes propagate back to source.', 'reverse', 1),
(6, 'references', 'references', 'is referenced by', 'Source names or calls target; target changes propagate back to source.', 'reverse', 1),
(7, 'controls', 'controls or influences', 'is controlled by', 'Source directly influences target behavior or demand.', 'forward', 1),
(8, 'interacts_with', 'interacts with', 'interacts with', 'Bidirectional operational or compatibility interaction.', 'both', 1),
(9, 'uses_scope', 'uses scope', 'scope used by', 'Symbol or mechanic is valid in or evaluates a scope.', 'reverse', 0),
(10, 'validated_by', 'is validated by', 'validates', 'Investigation route; not an impact dependency.', 'none', 0),
(11, 'supersedes', 'supersedes', 'is superseded by', 'Historical replacement relation.', 'none', 0),
(12, 'compatible_with', 'has compatibility concern with', 'has compatibility concern with', 'Mutual compatibility relationship.', 'both', 1),
(13, 'produced_by', 'is produced by', 'produces', 'Source output is produced by target; producer changes affect output.', 'reverse', 1);

INSERT INTO change_kind(change_kind_id, kind_code, kind_name, description) VALUES
(1, 'added', 'Added', 'New surface appeared.'),
(2, 'removed', 'Removed', 'Surface was removed.'),
(3, 'modified', 'Modified', 'Meaning, fields, or behavior changed.'),
(4, 'renamed', 'Renamed', 'Identifier changed.'),
(5, 'behavioral', 'Behavioral', 'Runtime behavior changed without a simple structural classification.'),
(6, 'unknown', 'Unknown', 'Change is observed but not yet classified.');

INSERT INTO change_type(change_type_id, type_code, type_name, description) VALUES
(1, 'field_change', 'Field change', 'Change a field value or expression.'),
(2, 'object_change', 'Object change', 'Add, remove, or modify a scripted object.'),
(3, 'mechanic_change', 'Mechanic change', 'Change a mechanic across multiple surfaces.'),
(4, 'subsystem_change', 'Subsystem change', 'Change a complete mod subsystem.'),
(5, 'version_port', 'Version port', 'Port or revalidate against a new Stellaris version.');

INSERT INTO investigation_task_type(
    investigation_task_type_id, task_code, task_name, description
) VALUES
(1, 'locate_definition', 'Locate definition', 'Retrieve exact object or field definitions.'),
(2, 'schema_validate', 'Schema validation', 'Check syntax, type, scope, and allowed fields.'),
(3, 'conflict_analysis', 'Conflict analysis', 'Determine active winner and load-order interactions.'),
(4, 'source_diff', 'Source diff', 'Compare files or symbols between versions.'),
(5, 'static_validate', 'Static validation', 'Run deterministic repository validation.'),
(6, 'runtime_log_check', 'Runtime log check', 'Inspect game/error logs for the target behavior.'),
(7, 'save_inspection', 'Save inspection', 'Inspect persisted state for a specified run.'),
(8, 'controlled_experiment', 'Controlled experiment', 'Run a bounded comparison to resolve a hypothesis.'),
(9, 'impact_review', 'Impact review', 'Traverse dependencies and review affected items.'),
(10, 'documentation_lookup', 'Documentation lookup', 'Retrieve generated or narrative documentation.'),
(11, 'history_review', 'History review', 'Inspect Git changes and prior decisions.');

-- ---------------------------------------------------------------------------
-- B. Versions and reusable applicability spans
-- ---------------------------------------------------------------------------

INSERT INTO game_version(
    game_version_id, version_label, version_order, major, minor, patch,
    codename, build_id, release_channel, released_on, is_primary_target, notes,
    created_in_change_set_id
) VALUES
(1, '4.4.4', 40404, 4, 4, 4, 'Pegasus', '7d82', 'stable', NULL, 0, 'Historical/rollback reference.', 1),
(2, '4.4.5', 40405, 4, 4, 5, 'Pegasus', NULL, 'stable', NULL, 1, 'Representative project primary target.', 1),
(3, '4.5-beta', 40500, 4, 5, NULL, NULL, NULL, 'beta', NULL, 0, 'Separate compatibility and porting branch.', 1);

INSERT INTO version_span(
    version_span_id, span_code, span_name, min_version_id, max_version_id,
    boundary_note, created_in_change_set_id
) VALUES
(1, 'all', 'All catalogued versions', NULL, NULL, 'Open-ended catalog span.', 1),
(2, 'v4.4.4', 'Stellaris 4.4.4 only', 1, 1, 'Exact historical version.', 1),
(3, 'v4.4.5', 'Stellaris 4.4.5 only', 2, 2, 'Exact primary target.', 1),
(4, 'v4.4.x', 'Stellaris 4.4.4 through 4.4.5', 1, 2, 'Known 4.4 project versions.', 1),
(5, 'v4.5-beta', 'Stellaris 4.5 beta only', 3, 3, 'Separate porting target.', 1),
(6, 'v4.4.5-plus', 'Stellaris 4.4.5 and later catalogued versions', 2, NULL, 'Open-ended until contradicted.', 1),
(7, 'v4.4.4-through-v4.5-beta', 'All three representative versions', 1, 3, 'Comparison span.', 1);

-- ---------------------------------------------------------------------------
-- C. Stable item catalogue and typed sidecars
-- ---------------------------------------------------------------------------

-- Mechanic families, subsystems, mechanics.
INSERT INTO knowledge_item(
    item_id, item_type_id, canonical_key, display_name, summary,
    lifecycle_state_id, created_by_actor_id, created_in_change_set_id
) VALUES
(100, 1, 'mechanic-family:ai-economy', 'AI economy', 'AI resource acquisition, allocation, jobs, buildings, and growth.', 1, 2, 1),
(101, 1, 'mechanic-family:ai-strategy', 'AI strategy', 'Country eligibility, personality, diplomacy, and war-planning behavior.', 1, 2, 1),
(110, 3, 'subsystem:economic-planning', 'Economic planning subsystem', 'Stellar AI Director budgets, plans, research growth, and construction demand.', 1, 2, 1),
(111, 3, 'subsystem:war-planning', 'War-planning subsystem', 'Stellar AI Director country, personality, claim, war-goal, and readiness surfaces.', 1, 2, 1),
(120, 2, 'mechanic:ai-budgets', 'AI budgets', 'Resource allocation and reserve behavior exposed through AI budget objects.', 1, 2, 1),
(121, 2, 'mechanic:economic-plans', 'Economic plans', 'AI economic priorities and phase-dependent strategic demand.', 1, 2, 1),
(122, 2, 'mechanic:country-types', 'Country types', 'Country classification and ordinary-AI eligibility assumptions.', 1, 2, 1),
(123, 2, 'mechanic:personalities', 'AI personalities', 'Diplomatic and strategic personality weights.', 1, 2, 1),
(124, 2, 'mechanic:war-planning', 'War planning', 'Claims, casus belli, war goals, personality, readiness, and engine-hidden decisions.', 1, 2, 1),
(125, 2, 'mechanic:building-job-economy', 'Building and job economy', 'Construction, employment, inputs, outputs, and AI demand.', 1, 2, 1),
(126, 2, 'mechanic:version-compatibility', 'Version compatibility', 'Version applicability and revalidation after Stellaris updates.', 1, 2, 1),
(127, 2, 'mechanic:resource-abundance-baseline', 'Resource Abundance baseline', 'Galaxy-setting effect on strategic economy assumptions.', 1, 2, 1),
(128, 2, 'mechanic:pop-workforce', 'Pop groups and workforce', 'Pop, job, faction, ethic, and workforce assumptions that affect AI economy.', 1, 2, 1);

INSERT INTO mechanic_family(item_id, family_code, domain_summary) VALUES
(100, 'ai-economy', 'Economic AI and its scripted surfaces.'),
(101, 'ai-strategy', 'Strategic AI and its scripted and partly hidden surfaces.');

INSERT INTO subsystem(item_id, subsystem_code, purpose, primary_repository_path, acceptance_summary) VALUES
(110, 'economic-planning', 'Coordinate budgets, plans, research demand, buildings, and jobs.', 'mods/StellarAIDirector/common', 'Static references resolve; active winners are known; affected claims are version-current.'),
(111, 'war-planning', 'Improve native AI strategic readiness without scripted forced wars.', 'mods/StellarAIDirector/common', 'Static surfaces validate and runtime claims remain explicitly evidence-bounded.');

INSERT INTO mechanic(item_id, mechanic_family_item_id, purpose, engine_visibility, owner_scope_item_id, notes) VALUES
(120, 100, 'Represent and tune AI resource allocation.', 'script_visible', NULL, 'Typed detail is stored in ai_budget_mechanic_detail.'),
(121, 100, 'Represent and tune strategic economic priorities.', 'partially_script_visible', NULL, 'Selection details may require runtime evidence.'),
(122, 101, 'Represent country classifications and AI participation.', 'partially_script_visible', NULL, NULL),
(123, 101, 'Represent diplomacy and strategic tendency weights.', 'partially_script_visible', NULL, NULL),
(124, 101, 'Represent script-visible war inputs while preserving hidden-engine uncertainty.', 'hardcoded_or_hidden', NULL, 'Do not infer declarations solely from weights.'),
(125, 100, 'Connect AI demand to buildings, jobs, technologies, and resources.', 'partially_script_visible', NULL, NULL),
(126, 101, 'Track version validity and compatibility review obligations.', 'script_visible', NULL, NULL),
(127, 100, 'Track changes to the strategic economic baseline.', 'partially_script_visible', NULL, NULL),
(128, 100, 'Track pop/workforce assumptions used by AI economy logic.', 'partially_script_visible', NULL, NULL);

-- Game objects, resources, and technologies.
INSERT INTO knowledge_item(
    item_id, item_type_id, canonical_key, display_name, summary,
    lifecycle_state_id, created_by_actor_id, created_in_change_set_id
) VALUES
(130, 4, 'object:economic_plan:staid_research_growth_plan', 'staid_research_growth_plan', 'Representative mod economic-plan object used to demonstrate field and impact queries.', 1, 2, 1),
(131, 4, 'object:ai_budget:alloys', 'alloys AI budget', 'Representative AI budget object for alloy allocation.', 1, 2, 1),
(132, 4, 'object:country_type:default', 'default country type', 'Representative ordinary country-type object.', 1, 2, 1),
(133, 4, 'object:personality:staid_aggressive_researcher', 'staid_aggressive_researcher', 'Representative mod AI personality.', 1, 2, 1),
(134, 4, 'object:building:building_research_lab_1', 'building_research_lab_1', 'Representative vanilla research building key; confirm exact target-version definition locally.', 1, 2, 1),
(135, 4, 'object:job:researcher', 'researcher job', 'Representative vanilla researcher job key; confirm exact target-version definition locally.', 1, 2, 1),
(136, 4, 'object:policy:economic_policy', 'economic_policy', 'Representative policy object related to economic behavior.', 1, 2, 1),
(137, 4, 'object:war_goal:wg_conquest', 'wg_conquest', 'Representative conquest war-goal key; local verification required.', 1, 2, 1),
(138, 4, 'object:casus_belli:cb_claim', 'cb_claim', 'Representative claim casus-belli key; local verification required.', 1, 2, 1),
(140, 11, 'resource:energy', 'energy', 'Energy resource.', 1, 2, 1),
(141, 11, 'resource:minerals', 'minerals', 'Minerals resource.', 1, 2, 1),
(142, 11, 'resource:alloys', 'alloys', 'Alloys resource.', 1, 2, 1),
(143, 11, 'resource:physics_research', 'physics_research', 'Physics research output.', 1, 2, 1),
(144, 11, 'resource:society_research', 'society_research', 'Society research output.', 1, 2, 1),
(145, 11, 'resource:engineering_research', 'engineering_research', 'Engineering research output.', 1, 2, 1),
(146, 12, 'technology:tech_basic_science_lab_1', 'tech_basic_science_lab_1', 'Representative technology gate for an early research building; verify locally.', 1, 2, 1);

INSERT INTO game_object(item_id, object_kind_id, script_key, namespace, origin_class, notes) VALUES
(130, 1, 'staid_research_growth_plan', 'staid', 'mod', 'Illustrative object key.'),
(131, 2, 'alloys', '', 'vanilla', 'Representative budget key.'),
(132, 3, 'default', '', 'vanilla', 'Representative country-type key.'),
(133, 4, 'staid_aggressive_researcher', 'staid', 'mod', 'Illustrative personality key.'),
(134, 5, 'building_research_lab_1', '', 'vanilla', 'Confirm definition path and fields for the target version.'),
(135, 6, 'researcher', '', 'vanilla', 'Confirm definition path and fields for the target version.'),
(136, 9, 'economic_policy', '', 'vanilla', 'Representative policy key.'),
(137, 10, 'wg_conquest', '', 'vanilla', 'Representative key, not asserted as current without evidence.'),
(138, 11, 'cb_claim', '', 'vanilla', 'Representative key, not asserted as current without evidence.'),
(140, 7, 'energy', '', 'vanilla', NULL),
(141, 7, 'minerals', '', 'vanilla', NULL),
(142, 7, 'alloys', '', 'vanilla', NULL),
(143, 7, 'physics_research', '', 'vanilla', NULL),
(144, 7, 'society_research', '', 'vanilla', NULL),
(145, 7, 'engineering_research', '', 'vanilla', NULL),
(146, 8, 'tech_basic_science_lab_1', '', 'vanilla', 'Representative key, confirm locally.');

-- Fields.
INSERT INTO knowledge_item(
    item_id, item_type_id, canonical_key, display_name, summary,
    lifecycle_state_id, created_by_actor_id, created_in_change_set_id
) VALUES
(150, 5, 'field:economic_plan.weight', 'economic_plan.weight', 'Weight expression on an economic-plan definition.', 1, 2, 1),
(151, 5, 'field:economic_plan.focus', 'economic_plan.focus', 'Representative focus/priorities field on an economic plan.', 1, 2, 1),
(152, 5, 'field:ai_budget.resource', 'ai_budget.resource', 'Resource targeted by an AI budget definition.', 1, 2, 1),
(153, 5, 'field:ai_budget.target', 'ai_budget.target', 'Representative budget target or allocation expression.', 1, 2, 1),
(154, 5, 'field:country_type.ai', 'country_type.ai', 'Representative country-type AI eligibility field.', 1, 2, 1),
(155, 5, 'field:personality.aggressiveness', 'personality.aggressiveness', 'Representative strategic personality weight.', 1, 2, 1),
(156, 5, 'field:building.ai_weight', 'building.ai_weight', 'AI construction weight on a building.', 1, 2, 1),
(157, 5, 'field:job.resources', 'job.resources', 'Job input/output resource block.', 1, 2, 1),
(158, 5, 'field:war_goal.ai_weight', 'war_goal.ai_weight', 'Representative AI weighting field for a war goal.', 1, 2, 1);

INSERT INTO field_definition(item_id, owner_object_kind_id, field_name, value_type, cardinality, semantic_summary) VALUES
(150, 1, 'weight', 'scripted weight block', 'zero_or_one', 'Contributes to economic-plan selection or priority; exact semantics are version-evidence dependent.'),
(151, 1, 'focus', 'block', 'zero_or_many', 'Representative economic priorities; verify exact field name against target schema.'),
(152, 2, 'resource', 'resource key', 'one', 'Identifies the resource budgeted by the object.'),
(153, 2, 'target', 'numeric or scripted expression', 'zero_or_one', 'Represents desired allocation behavior; verify exact schema.'),
(154, 3, 'ai', 'boolean', 'zero_or_one', 'Represents whether the country type participates in ordinary AI processing; verify exact schema.'),
(155, 4, 'aggressiveness', 'numeric weight', 'zero_or_one', 'Represents a personality tendency used by strategic AI; exact engine use may be hidden.'),
(156, 5, 'ai_weight', 'scripted weight block', 'zero_or_one', 'Weights AI construction eligibility or desirability.'),
(157, 6, 'resources', 'resource block', 'zero_or_many', 'Declares job inputs and outputs.'),
(158, 10, 'ai_weight', 'scripted weight block', 'zero_or_one', 'Weights AI use of a war goal; does not alone prove declaration behavior.');

-- Script symbols and scopes.
INSERT INTO knowledge_item(
    item_id, item_type_id, canonical_key, display_name, summary,
    lifecycle_state_id, created_by_actor_id, created_in_change_set_id
) VALUES
(160, 6, 'trigger:has_technology', 'has_technology', 'Built-in technology possession trigger.', 1, 2, 1),
(161, 6, 'scripted-trigger:staid_should_prioritize_research', 'staid_should_prioritize_research', 'Representative mod scripted trigger for research demand.', 1, 2, 1),
(162, 7, 'effect:add_resource', 'add_resource', 'Representative built-in resource-changing effect.', 1, 2, 1),
(163, 7, 'scripted-effect:staid_apply_budget_phase', 'staid_apply_budget_phase', 'Representative mod scripted effect used in planning logic.', 1, 2, 1),
(164, 9, 'modifier:planet_researchers_produces_mult', 'planet_researchers_produces_mult', 'Representative research-production modifier.', 1, 2, 1),
(165, 10, 'define:illustrative.ai_construction_budget_fraction', 'Illustrative AI construction define', 'Placeholder define item demonstrating define lookup; replace with an exact locally verified identifier.', 2, 2, 1),
(170, 8, 'scope:country', 'country scope', 'Country script scope.', 1, 2, 1),
(171, 8, 'scope:planet', 'planet scope', 'Planet script scope.', 1, 2, 1),
(172, 8, 'scope:pop', 'pop scope', 'Pop script scope.', 1, 2, 1);

INSERT INTO script_symbol(item_id, script_symbol_kind_id, symbol_key, namespace, exposure_class, description) VALUES
(160, 1, 'has_technology', '', 'built_in', 'Signature and scopes must be version-matched.'),
(161, 3, 'staid_should_prioritize_research', 'staid', 'scripted', 'Illustrative project trigger.'),
(162, 2, 'add_resource', '', 'built_in', 'Representative built-in effect; validate exact syntax.'),
(163, 4, 'staid_apply_budget_phase', 'staid', 'scripted', 'Illustrative project effect.'),
(164, 5, 'planet_researchers_produces_mult', '', 'built_in', 'Representative modifier key.'),
(165, 6, 'NAI.AI_CONSTRUCTION_BUDGET_FRACTION', '', 'unknown', 'Illustrative only; not asserted as a real current define.');

INSERT INTO script_scope(item_id, scope_key, engine_scope_name, scope_summary) VALUES
(170, 'country', 'country', 'Empire/country execution context.'),
(171, 'planet', 'planet', 'Planet execution context.'),
(172, 'pop', 'pop', 'Individual pop execution context.');

-- Implementation file items.
INSERT INTO knowledge_item(
    item_id, item_type_id, canonical_key, display_name, summary,
    lifecycle_state_id, created_by_actor_id, created_in_change_set_id
) VALUES
(180, 13, 'file:mod/ai_budget/alloys', 'zzz_staid_alloys_budget.txt', 'Stellar AI Director alloy-budget implementation file.', 1, 2, 1),
(181, 13, 'file:mod/economic_plans/additive', 'zzzz_staid_additive_economic_plan.txt', 'Stellar AI Director economic-plan implementation file.', 1, 2, 1),
(182, 13, 'file:mod/scripted_triggers/decision_state', 'zzz_staid_decision_state_triggers.txt', 'Stellar AI Director scripted decision-state triggers.', 1, 2, 1),
(183, 13, 'file:mod/script_values/roi', 'zzz_staid_roi_values.txt', 'Stellar AI Director ROI values.', 1, 2, 1),
(184, 13, 'file:mod/notes/tuning', 'tuning-notes.md', 'Project tuning and evidence notes.', 1, 2, 1),
(185, 13, 'file:vanilla/economic_plans/reference', 'Vanilla economic-plans reference', 'Version-specific vanilla economic-plan file or folder locator.', 1, 2, 1),
(186, 13, 'file:vanilla/ai_budget/reference', 'Vanilla AI-budget reference', 'Version-specific vanilla AI-budget file or folder locator.', 1, 2, 1),
(187, 13, 'file:generated/trigger-effect-docs', 'Generated trigger/effect documentation', 'Version-matched generated script documentation.', 1, 2, 1);

INSERT INTO file_asset(item_id, corpus_code, relative_path, file_role, load_order_note) VALUES
(180, 'repository', 'mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt', 'mod implementation', 'Inspect active winner separately with Irony.'),
(181, 'repository', 'mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt', 'mod implementation', 'Inspect active winner separately with Irony.'),
(182, 'repository', 'mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt', 'mod implementation', NULL),
(183, 'repository', 'mods/StellarAIDirector/common/script_values/zzz_staid_roi_values.txt', 'mod implementation', NULL),
(184, 'repository', 'mods/StellarAIDirector/notes/tuning-notes.md', 'research note', NULL),
(185, 'vanilla-4.4.5', 'common/economic_plans/', 'vanilla reference corpus', 'Resolve exact current file and object key locally.'),
(186, 'vanilla-4.4.5', 'common/ai_budget/', 'vanilla reference corpus', 'Resolve exact current file and object key locally.'),
(187, 'generated-docs-4.4.5', 'triggers-effects-modifiers-scopes/', 'generated documentation corpus', NULL);

-- Existing investigative tools as stable items.
INSERT INTO knowledge_item(
    item_id, item_type_id, canonical_key, display_name, summary,
    lifecycle_state_id, created_by_actor_id, created_in_change_set_id
) VALUES
(190, 14, 'tool:cwtools', 'CWTools', 'Schema and static diagnostic authority.', 1, 2, 1),
(191, 14, 'tool:irony', 'Irony Mod Manager', 'Conflict, load-order, and merged-winner authority.', 1, 2, 1),
(192, 14, 'tool:jdocmunch', 'JDocMunch', 'Documentation and prose retrieval tool.', 1, 2, 1),
(193, 14, 'tool:jcodemunch', 'JCodeMunch', 'Code and script retrieval tool.', 1, 2, 1),
(194, 14, 'tool:jdatamunch', 'JDataMunch', 'Structured dataset retrieval tool.', 1, 2, 1),
(195, 14, 'tool:repository-validator', 'Stellar AI Director validator', 'Deterministic project validation script.', 1, 2, 1),
(196, 14, 'tool:git', 'Git', 'Repository history and diff tool.', 1, 2, 1),
(197, 14, 'tool:runtime-log-review', 'Runtime log review', 'Retrieve and inspect Stellaris game/error logs.', 1, 2, 1),
(198, 14, 'tool:save-inspection', 'Save inspection', 'Retrieve specific persisted game state.', 1, 2, 1);

INSERT INTO tool(item_id, tool_kind, executable_or_entrypoint, authority_scope, default_invocation, output_locator_pattern, is_local_only, notes) VALUES
(190, 'editor/schema validator', 'CWTools language server or CLI', 'PDXScript schema, syntax, scopes, and diagnostics', NULL, 'diagnostic file/line/code', 1, NULL),
(191, 'mod manager', 'IronyModManager.exe', 'Active-playset conflicts and effective winners', NULL, 'conflict report/object key', 1, NULL),
(192, 'document index', 'JDocMunch', 'Indexed local documentation and notes', NULL, 'document/path/section', 1, 'Does not replace source authority.'),
(193, 'code index', 'JCodeMunch', 'Indexed local code and script', NULL, 'file/symbol/line', 1, 'Use exact source artifact for final evidence.'),
(194, 'dataset index', 'JDataMunch', 'CSV and structured dataset lookup', NULL, 'dataset/record key', 1, 'Store locator, not copied dataset.'),
(195, 'repository script', 'python tools/validate_stellar_ai_director_patch.py', 'Project-specific deterministic validation', 'python tools/validate_stellar_ai_director_patch.py', 'command output and generated report', 1, NULL),
(196, 'version control', 'git', 'Repository commit and diff history', 'git log -- <path>', 'commit/path/hunk', 1, NULL),
(197, 'manual/tool-assisted inspection', 'logs/game.log; logs/error.log', 'Run-specific runtime diagnostics', NULL, 'file/timestamp/line', 1, NULL),
(198, 'manual/tool-assisted inspection', 'selected .sav plus existing extraction scripts', 'Run-specific persisted state', NULL, 'save hash/game date/field', 1, 'Do not copy the full save into this database.');

-- Checklist item (steps are seeded later).
INSERT INTO knowledge_item(
    item_id, item_type_id, canonical_key, display_name, summary,
    lifecycle_state_id, created_by_actor_id, created_in_change_set_id
) VALUES
(200, 15, 'checklist:change-ai-economic-planning', 'Change AI economic planning', 'Reusable planning, implementation, compatibility, and validation checklist.', 1, 2, 1),
(210, 16, 'system:vanilla-4.4.5', 'Vanilla Stellaris 4.4.5 corpus', 'Exact local vanilla files for the target version.', 1, 2, 1),
(211, 16, 'system:active-playset', 'Active mod playset', 'Launcher order and merged winners for the actual playset.', 1, 2, 1),
(212, 16, 'system:runtime-evidence', 'Runtime evidence environment', 'Specific logs, saves, and controlled runs.', 1, 2, 1);

INSERT INTO checklist(item_id, change_type_id, purpose, completion_criteria, created_in_change_set_id) VALUES
(200, 4, 'Plan and validate a change to the AI economic-planning subsystem.',
 'Target version is explicit; direct and transitive impacts are reviewed; source and active winner are checked; static gates pass; behavioral claims are reassessed with appropriate evidence.', 1);

-- Aliases improve exact and full-text lookup without changing canonical keys.
INSERT INTO item_alias(item_alias_id, item_id, alias_text, alias_kind, version_span_id, notes, created_in_change_set_id) VALUES
(1, 120, 'ai_budget', 'folder/name', 4, NULL, 1),
(2, 121, 'economic_plans', 'folder/name', 4, NULL, 1),
(3, 111, 'war AI', 'informal', 4, NULL, 1),
(4, 128, 'workforce', 'informal', 5, NULL, 1),
(5, 190, 'CWT', 'abbreviation', 1, NULL, 1);

-- ---------------------------------------------------------------------------
-- D. Tools, routing, source systems, artifacts, derivations, and locators
-- ---------------------------------------------------------------------------

INSERT INTO tool_capability(
    tool_capability_id, tool_item_id, investigation_task_type_id,
    capability_summary, invocation_template, expected_output, limitations, priority
) VALUES
(1, 193, 1, 'Locate exact vanilla or mod definitions and references.', 'Search <corpus> for <object-or-field>.', 'File, symbol, and line locator.', 'Index freshness must be checked.', 90),
(2, 190, 2, 'Validate PDXScript fields, scopes, and diagnostics.', 'Open target files with version-matched CWTools configuration.', 'Schema diagnostics with file and line.', 'Cannot prove hidden runtime decisions.', 95),
(3, 191, 3, 'Find conflicts and effective active-playset winners.', 'Inspect conflicts and merged definition for <object-key>.', 'Winning source and conflict set.', 'Authority is limited to the selected playset and configuration.', 95),
(4, 196, 4, 'Diff source paths or versions.', 'git diff <from>..<to> -- <path>', 'Versioned file diff.', 'Does not compare external vanilla builds unless captured.', 80),
(5, 195, 5, 'Run deterministic project validation.', 'python tools/validate_stellar_ai_director_patch.py', 'Pass/fail output and targeted diagnostics.', 'Does not prove long-run AI efficacy.', 100),
(6, 197, 6, 'Inspect runtime logs for parse, scope, or behavior evidence.', 'Inspect logs for <run-key>/<object-key>.', 'Timestamped log range.', 'Absence of a log message is not automatically proof of absence.', 85),
(7, 198, 7, 'Inspect save fields for a controlled run.', 'Extract <fields> from save <hash>.', 'Game-date and field-value locator.', 'Save state may prove outcome but not hidden causation.', 85),
(8, 192, 10, 'Retrieve research notes and generated prose.', 'Search documents for <topic> and <version>.', 'Document and section locator.', 'Secondary unless backed by primary evidence.', 75),
(9, 194, 1, 'Locate records in object-atlas and audit datasets.', 'Search dataset <name> for <record-key>.', 'Dataset and stable record key.', 'Dataset generation inputs must be recorded.', 85),
(10, 196, 11, 'Trace why and when a project change was made.', 'git log -p -- <path>', 'Commit, path, and hunk.', 'Commit intent may need corroborating notes.', 85);

INSERT INTO tool_route(
    tool_route_id, tool_capability_id, target_item_id, target_item_type_id,
    evidence_source_type_id, version_span_id, route_priority, instructions,
    fallback_tool_capability_id, is_active
) VALUES
(1, 2, NULL, 5, NULL, 3, 100, 'Validate the field against the 4.4.5 CWTools schema before editing.', 1, 1),
(2, 3, 110, NULL, NULL, 3, 100, 'For active-playset claims, retrieve merged winners for every overridden budget and plan object.', 1, 1),
(3, 5, 110, NULL, NULL, 3, 95, 'Run the repository validator after edits and before accepting updated claims.', NULL, 1),
(4, 6, 111, NULL, NULL, 3, 90, 'Use a named runtime run and exact timestamp ranges for war-behavior claims.', 7, 1),
(5, 8, NULL, NULL, 6, NULL, 80, 'Use notes to locate prior conclusions, then follow their primary locators.', 1, 1),
(6, 9, NULL, NULL, 12, NULL, 85, 'Retrieve the exact dataset record and its generation context; do not copy the dataset wholesale.', 1, 1),
(7, 4, 126, NULL, NULL, 5, 95, 'Diff every touched vanilla folder and schema between 4.4.5 and 4.5 beta.', 2, 1);

INSERT INTO source_system(
    source_system_id, system_key, system_name, evidence_source_type_id,
    canonical_root, access_mode, authoritative_for, default_tool_item_id,
    retrieval_instructions, is_local_only, notes, created_in_change_set_id
) VALUES
(1, 'vanilla-4.4.5', 'Local vanilla Stellaris 4.4.5', 1, 'C:/Steam/steamapps/common/Stellaris', 'filesystem', 'Captured 4.4.5 scripted definitions', 193, 'Use exact path/object key; hash or otherwise identify the captured build.', 1, NULL, 1),
(2, 'generated-docs-4.4.5', 'Generated Stellaris 4.4.5 docs', 2, 'local/generated-docs/4.4.5', 'filesystem/index', '4.4.5 trigger/effect/modifier/scope documentation', 192, 'Retrieve exact symbol entry and generation/version metadata.', 1, NULL, 1),
(3, 'cwtools-4.4.5', 'CWTools Stellaris 4.4.5 configuration', 3, 'local/cwtools/stellaris', 'filesystem/editor', 'Schema and diagnostics', 190, 'Record schema file, rule, diagnostic code, and version configuration.', 1, NULL, 1),
(4, 'active-irony-playset', 'Irony active-playset evidence', 4, 'local/irony', 'application/export', 'Conflict sets, order, and merged winners', 191, 'Record playset identity, object key, winning source, and export/report locator.', 1, NULL, 1),
(5, 'stellar-ai-repository', 'Stellar AI Director repository', 5, 'repository-root', 'git/filesystem', 'Current mod source and project scripts', 193, 'Record repository commit plus relative path, symbol, and line range.', 1, NULL, 1),
(6, 'project-research', 'Project research notes', 6, 'research/', 'filesystem/index', 'Prior conclusions and investigation plans', 192, 'Retrieve section and follow embedded primary evidence.', 1, NULL, 1),
(7, 'stellaris-runtime-logs', 'Stellaris runtime logs', 7, 'user/Stellaris/logs', 'filesystem', 'Run-specific parser and runtime messages', 197, 'Record run key, file, timestamp/line range, game version, and playset.', 1, NULL, 1),
(8, 'selected-save-evidence', 'Selected save evidence', 8, 'staged-save-location', 'filesystem/extractor', 'Persisted game state for a controlled run', 198, 'Record save hash, game date, extraction method, and exact field key.', 1, NULL, 1),
(9, 'repository-tool-output', 'Repository validator and audit output', 12, 'research/stellar-ai', 'filesystem', 'Deterministic project checks for captured inputs', 195, 'Record command, tool version or commit, input commit, and output locator.', 1, NULL, 1),
(10, 'git-history', 'Git history', 10, 'repository-root/.git', 'git', 'Commit provenance and diffs', 196, 'Record commit SHA, path, and hunk or command.', 1, NULL, 1),
(11, 'stellaris-patch-notes', 'Stellaris patch notes', 13, 'preserved patch-note sources', 'document/web', 'Declared version changes', 192, 'Record publication/version and section; confirm scripted surfaces locally.', 0, NULL, 1);

INSERT INTO source_artifact(
    source_artifact_id, source_system_id, stable_key, artifact_kind, title,
    uri_or_path, repository_relative_path, game_version_id, repository_commit,
    tool_version, content_hash_algorithm, content_hash_value, captured_at,
    observed_at, availability_status, notes, created_in_change_set_id
) VALUES
(1, 6, 'context-bundle-2026-07-10', 'research bundle', 'ChatGPT project context bundle', 'chatgpt_context_bundle/', NULL, 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, '2026-07-10T14:15:43Z', NULL, 'available', 'Used only for project use cases and tool context.', 1),
(2, 1, 'economic-plans-corpus-4.4.5', 'vanilla corpus', 'Vanilla 4.4.5 economic-plan definitions', 'C:/Steam/steamapps/common/Stellaris/common/economic_plans/', NULL, 2, NULL, NULL, NULL, NULL, NULL, '2026-07-08T00:00:00Z', 'available', 'Representative folder locator; add exact file hashes in production.', 1),
(3, 3, 'economic-plan-schema-4.4.5', 'schema', 'CWTools economic-plan schema', 'local/cwtools/stellaris/economic_plans.cwt', NULL, 2, NULL, 'version-matched example', NULL, NULL, NULL, '2026-07-08T00:00:00Z', 'available', NULL, 1),
(4, 4, 'active-winner-report-2026-07-10', 'conflict report', 'Irony active-playset merged-winner report', 'local/irony/exports/active-winners-2026-07-10', NULL, 2, NULL, 'local installation', NULL, NULL, '2026-07-10T14:00:00Z', '2026-07-10T14:00:00Z', 'available', 'Representative report locator.', 1),
(5, 5, 'repo-alloys-budget-example', 'source file', 'Stellar AI Director alloys budget', 'repository-root/mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt', 'mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, '2026-07-10T14:15:43Z', NULL, 'available', NULL, 1),
(6, 5, 'repo-economic-plan-example', 'source file', 'Stellar AI Director additive economic plan', 'repository-root/mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt', 'mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, '2026-07-10T14:15:43Z', NULL, 'available', NULL, 1),
(7, 5, 'repo-scripted-trigger-example', 'source file', 'Stellar AI Director decision-state triggers', 'repository-root/mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt', 'mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, '2026-07-10T14:15:43Z', NULL, 'available', NULL, 1),
(8, 9, 'validator-output-example', 'command output', 'Stellar AI Director static validator output', 'research/stellar-ai/validator-output-example.txt', 'research/stellar-ai/validator-output-example.txt', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'repository script at commit', NULL, NULL, '2026-07-10T14:15:43Z', '2026-07-10T14:15:43Z', 'available', 'Representative output locator.', 1),
(9, 7, 'observer-run-example-game-log', 'runtime log', 'Observer run game.log excerpt', 'user/Stellaris/logs/game.log', NULL, 2, NULL, NULL, 'SHA-256', 'example-log-hash', '2026-07-09T13:25:40Z', '2026-07-09T13:25:40Z', 'available', 'Run-specific evidence, not a general truth.', 1),
(10, 8, 'observer-run-example-save', 'save', 'Observer run selected save', 'staged/STAID_EXAMPLE_2250.sav', NULL, 2, NULL, 'existing extractor', 'SHA-256', 'example-save-hash', '2026-07-09T13:25:40Z', '2026-07-09T13:25:40Z', 'available', 'Full save remains external.', 1),
(11, 11, 'patch-notes-4.4.5', 'patch notes', 'Stellaris 4.4.5 patch notes', 'preserved/stellaris-4.4.5-patch-notes', NULL, 2, NULL, NULL, NULL, NULL, NULL, '2026-07-08T00:00:00Z', 'available', 'Use exact preserved source in production.', 1),
(12, 11, 'patch-notes-4.5-beta', 'patch notes', 'Stellaris 4.5 beta patch notes', 'preserved/stellaris-4.5-beta-patch-notes', NULL, 3, NULL, NULL, NULL, NULL, NULL, '2026-07-08T00:00:00Z', 'available', 'Use exact preserved source in production.', 1),
(13, 10, 'commit-b605aa0e', 'git commit', 'Strategic-v2 repository commit', 'git:b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'git', NULL, NULL, '2026-07-10T00:00:00Z', NULL, 'available', NULL, 1),
(14, 2, 'generated-script-docs-4.4.5', 'generated documentation', 'Generated trigger/effect/modifier/scope docs', 'local/generated-docs/4.4.5/', NULL, 2, NULL, 'generator-version-example', NULL, NULL, NULL, '2026-07-08T00:00:00Z', 'available', NULL, 1);

INSERT INTO artifact_derivation(
    artifact_derivation_id, output_artifact_id, input_artifact_id,
    process_tool_item_id, process_run_key, command_or_method, derived_at,
    rationale, created_in_change_set_id
) VALUES
(1, 8, 5, 195, 'validator-example-2026-07-10', 'python tools/validate_stellar_ai_director_patch.py', '2026-07-10T14:15:43Z', 'Validator output derives from the captured repository source.', 1),
(2, 8, 6, 195, 'validator-example-2026-07-10', 'python tools/validate_stellar_ai_director_patch.py', '2026-07-10T14:15:43Z', 'Validator output derives from the captured repository source.', 1),
(3, 14, 2, 192, 'docs-example-4.4.5', 'Generate version-matched script documentation from local game metadata.', '2026-07-08T00:00:00Z', 'Generated docs must remain linked to their source version.', 1);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, section_title, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    1, 1, 10, 'baseline-version-policy', 'Project version and porting policy', '02_PROJECT_CONTROL_AND_GUIDANCE.md', 'Stellaris Modding Defaults', 'Target 4.4.5; treat 4.4.4 as historical unless revalidated; treat 4.5 as a separate porting branch.', 'Establishes the representative project version posture.', 'Open the named bundle file and section, then follow its underlying sources.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, section_title, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    2, 1, 10, 'tool-routing-policy', 'Project tool-routing policy', '05_RESEARCH_AND_EVIDENCE_GUIDES.md', 'Local Stellaris Tooling', 'Use vanilla files, generated docs, CWTools, Irony, Munch tools, repository scripts, logs, and saves for their respective evidence scopes.', 'Defines the external authority split used by this database.', 'Retrieve the section and the exact tool-specific source it directs the investigator to use.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, symbol_or_object_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    3, 2, 2, 'object:representative-plan', 'Representative vanilla economic-plan object', 'common/economic_plans/', 'representative_plan_key', 'Representative only: replace with exact target-version object key and file range.', 'Shows how an object-level vanilla locator is stored without copying the file.', 'Use JCodeMunch or filesystem search, then record exact file, key, and lines.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, symbol_or_object_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    4, 3, 3, 'schema:economic_plan.weight', 'CWTools rule for economic_plan.weight', 'economic_plans.cwt', 'weight', 'Representative schema locator for the weight field.', 'Supports structural validation of the field, not hidden runtime selection behavior.', 'Open the version-matched CWT rule and record exact diagnostic/rule lines.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, symbol_or_object_key, record_set, record_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    5, 4, 4, 'winner:staid_research_growth_plan', 'Active winner for staid_research_growth_plan', 'staid_research_growth_plan', 'merged_winners', 'economic_plan:staid_research_growth_plan', 'Representative Irony record: the mod definition is the selected winner in the captured playset.', 'Supports active-playset provenance for the example plan.', 'Open the named Irony export/report and confirm playset identity and winning source.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, symbol_or_object_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    6, 5, 2, 'object:alloys-budget', 'Alloys budget object in mod source', 'mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt', 'alloys', 'Mod-source locator for the alloy AI budget object.', 'Connects the budget mechanic to its implementation without copying the whole file.', 'Open the repository path at the recorded commit and locate the object key.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, symbol_or_object_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    7, 6, 2, 'object:staid-research-growth-plan', 'Research growth economic plan in mod source', 'mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt', 'staid_research_growth_plan', 'Representative mod-source locator for the economic plan.', 'Supports implementation relationships and field occurrences.', 'Open the repository path at the recorded commit and record exact lines before accepting production data.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, symbol_or_object_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    8, 7, 3, 'symbol:staid_should_prioritize_research', 'Research-priority scripted trigger', 'mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt', 'staid_should_prioritize_research', 'Representative scripted-trigger locator.', 'Shows precise symbol provenance.', 'Open the repository path at the recorded commit and record exact definition and call-site lines.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, query_text, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    9, 8, 5, 'validator:passed', 'Static validator passed', 'research/stellar-ai/validator-output-example.txt', 'python tools/validate_stellar_ai_director_patch.py', 'Stellar AI Director validation passed.', 'Supports static safety claims only.', 'Re-run the command against the target commit and preserve exact output.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, timestamp_start, timestamp_end, game_date, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    10, 9, 6, 'observer:no-war-proof', 'Observer log lacks sufficient causal war proof', 'user/Stellaris/logs/game.log', '2026-07-09T12:38:02Z', '2026-07-09T13:25:40Z', '2250.01.01', 'The run did not establish a complete causal path from script-visible weights to a war declaration.', 'Qualifies or contradicts claims that static weights alone prove war behavior.', 'Retrieve the exact run log by hash and inspect the recorded interval.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, record_set, record_key, game_date, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    11, 10, 7, 'save:war-state', 'Observer save war-state fields', 'countries', 'war_state_summary', '2250.01.01', 'Representative extracted fields show outcomes for one save but not the hidden engine decision process.', 'Provides run-specific outcome evidence and an explicit causation limitation.', 'Use the recorded save hash and extraction method; preserve field names and game date.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, section_title, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    12, 12, 10, 'section:pop-workforce-changes', '4.5 beta pop/workforce changes', 'Pops, factions, jobs, and workforce', 'The 4.5 beta changes pop-group, faction, ethic, job, and workforce assumptions.', 'Supports mandatory AI-economy revalidation for the separate 4.5 port.', 'Retrieve the preserved patch-note section, then diff exact vanilla/script schema surfaces.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, section_title, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    13, 11, 10, 'section:resource-abundance', '4.4.5 Resource Abundance change', 'Resource Abundance', 'The 4.4.5 update changed the Resource Abundance strategic-economy baseline.', 'Supports a version-specific compatibility claim.', 'Retrieve the exact preserved 4.4.5 patch-note section and compare relevant settings/defines locally.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, query_text, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    14, 13, 8, 'commit:strategic-v2', 'Strategic-v2 repository commit', 'git show b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'Git provenance for the representative repository snapshot.', 'Use the commit to retrieve exact source state.', 'Run git show and path-specific history commands.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, relative_path, section_title, symbol_or_object_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    15, 1, 10, 'descriptor-metadata-caveat', 'supported_version metadata caveat', '02_PROJECT_CONTROL_AND_GUIDANCE.md', 'Stellaris Modding Defaults', 'supported_version', 'supported_version is launcher-facing metadata and does not determine whether script code loads.', 'Directly contradicts treating descriptor metadata as proof of compatibility.', 'Retrieve the project guidance and then validate actual source and active playset separately.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, symbol_or_object_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    16, 14, 3, 'symbol:has_technology', 'Generated docs entry for has_technology', 'has_technology', 'Representative generated-documentation locator for trigger signature and scopes.', 'Supports version-matched symbol metadata.', 'Retrieve exact symbol entry and generator/version metadata.', 2, 1
);

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, locator_type_id, stable_locator_key, label, symbol_or_object_key, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES (
    17, 14, 3, 'symbol:add_resource', 'Generated docs entry for add_resource', 'add_resource', 'Representative generated-documentation locator for effect signature and scopes.', 'Supports version-matched symbol metadata.', 'Retrieve exact symbol entry and generator/version metadata.', 2, 1
);

-- ---------------------------------------------------------------------------
-- E. Versioned object/symbol detail and field occurrences
-- ---------------------------------------------------------------------------

INSERT INTO object_definition(
    object_definition_id, object_item_id, version_span_id, source_system_id,
    evidence_locator_id, definition_status, content_hash, notes,
    created_in_change_set_id
) VALUES
(1, 130, 3, 5, 7, 'candidate', NULL, 'Repository definition occurrence; playset-specific winning status is stored separately.', 1),
(2, 131, 3, 5, 6, 'candidate', NULL, 'Mod implementation occurrence of a representative budget object.', 1),
(3, 130, 3, 4, 5, 'reference', NULL, 'Historical merged-winner report represented as evidence; current resolution is stored in playset_object_resolution.', 1),
(4, 134, 3, 1, 3, 'reference', NULL, 'Representative vanilla example; replace locator with exact building definition.', 1);

INSERT INTO object_field_occurrence(
    object_field_occurrence_id, object_item_id, field_item_id, version_span_id,
    source_system_id, evidence_locator_id, ordinal_in_object, expression_text,
    normalized_summary, created_in_change_set_id
) VALUES
(1, 130, 150, 3, 5, 7, 1, 'weight = { ... }', 'The example plan contains a scripted weight block.', 1),
(2, 130, 151, 3, 5, 7, 1, 'focus = { research = ... }', 'Representative research-priority block; exact field must be schema-verified.', 1),
(3, 131, 152, 3, 5, 6, 1, 'resource = alloys', 'The example budget targets alloys.', 1),
(4, 131, 153, 3, 5, 6, 1, 'target = <expression>', 'Representative allocation target expression.', 1);

INSERT INTO script_symbol_revision(
    script_symbol_revision_id, script_symbol_item_id, version_span_id,
    source_system_id, evidence_locator_id, revision_kind, signature_text,
    value_text, behavior_summary, status_code, created_in_change_set_id
) VALUES
(1, 160, 3, 2, 16, 'generated-doc-entry', 'has_technology = <technology>', NULL, 'Tests whether the current scope has the named technology; exact allowed scopes come from the version-matched docs.', 'present', 1),
(2, 161, 3, 5, 8, 'scripted-definition', 'staid_should_prioritize_research = { ... }', NULL, 'Representative project decision-state trigger.', 'present', 1),
(3, 162, 3, 2, 17, 'generated-doc-entry', 'add_resource = { <resource> = <amount> }', NULL, 'Representative effect metadata; validate exact syntax and scope before use.', 'present', 1),
(4, 165, 3, 6, 1, 'placeholder', NULL, NULL, 'Illustrative define has not been verified.', 'unknown', 1);

INSERT INTO symbol_scope_rule(
    symbol_scope_rule_id, script_symbol_item_id, scope_item_id, role_code,
    version_span_id, evidence_locator_id, rule_summary, created_in_change_set_id
) VALUES
(1, 160, 170, 'supported_current_scope', 3, 16, 'Representative country-scope use; exact generated docs remain authoritative.', 1),
(2, 161, 170, 'scripted_current_scope', 3, 8, 'The representative project trigger is intended for country scope.', 1),
(3, 162, 170, 'supported_current_scope', 3, 17, 'Representative country-scope use; validate exact generated docs.', 1);

INSERT INTO symbol_parameter(
    symbol_parameter_id, script_symbol_item_id, parameter_name, value_type,
    is_required, default_value_text, version_span_id, description,
    created_in_change_set_id
) VALUES
(1, 160, 'technology', 'technology key', 1, NULL, 3, 'Technology to test.', 1),
(2, 162, 'resource_and_amount', 'resource/amount block', 1, NULL, 3, 'Resource and amount to add; exact syntax is documentation-controlled.', 1);

INSERT INTO field_revision(
    field_revision_id, field_item_id, version_span_id, source_system_id,
    evidence_locator_id, value_type, cardinality, semantic_summary,
    status_code, created_in_change_set_id
) VALUES
(1, 150, 3, 3, 4, 'scripted weight block', 'zero_or_one', 'Version-matched CWTools evidence recognizes the economic-plan weight surface; hidden selection magnitude remains claim-level knowledge.', 'present', 1),
(2, 151, 3, 3, 4, 'unknown pending exact rule lookup', 'unknown', 'The representative focus field remains intentionally unverified and must not be treated as schema fact.', 'unknown', 1);

INSERT INTO item_version_status(
    item_version_status_id, item_id, version_span_id, status_code,
    assessment_state_id, confidence_level_id, evidence_locator_id,
    assessed_by_actor_id, assessed_at, basis_summary, notes, is_current,
    supersedes_item_version_status_id, created_in_change_set_id
) VALUES
(1, 120, 3, 'present', 1, 4, 6, 2, '2026-07-10T16:02:00Z', 'The target repository snapshot contains the linked AI-budget implementation.', 'AI budget implementation present in target repository snapshot.', 1, NULL, 1),
(2, 121, 3, 'present', 1, 4, 7, 2, '2026-07-10T16:02:00Z', 'The target repository snapshot contains the linked economic-plan implementation.', 'Economic-plan implementation present in target repository snapshot.', 1, NULL, 1),
(3, 128, 5, 'changed', 2, 4, 12, 2, '2026-07-10T16:03:00Z', 'Patch-note evidence identifies material pop/workforce changes; exact field diffs remain pending.', '4.5 beta requires separate review of pop/workforce assumptions.', 1, NULL, 1),
(4, 165, 3, 'unknown', 6, 1, NULL, 2, '2026-07-10T16:03:00Z', 'No exact target-version source locator has been established for the illustrative define.', 'Illustrative define intentionally remains unverified.', 1, NULL, 1),
(5, 124, 3, 'present', 3, 3, 10, 2, '2026-07-10T16:04:00Z', 'Script-visible surfaces are catalogued, but the behavior boundary remains partly hidden and unproven.', 'Script-visible surfaces are present, but behavior remains partly hidden/unproven.', 1, NULL, 1);

-- ---------------------------------------------------------------------------
-- F. Verification runs, claims, assessments, evidence, conflicts, and questions
-- ---------------------------------------------------------------------------

INSERT INTO verification_run(
    verification_run_id, run_key, title, target_version_id, tool_item_id,
    performed_by_actor_id, method_summary, command_or_query, environment_summary,
    started_at, completed_at, outcome_code, notes, created_in_change_set_id
) VALUES
(1, 'static-schema-example-4.4.5', 'Economic-plan field/schema review', 2, 190, 2,
 'Inspect representative plan field against version-matched CWTools and source locators.', NULL, 'Local 4.4.5 schema context.',
 '2026-07-10T12:00:00Z', '2026-07-10T12:10:00Z', 'passed', 'Demonstration record.', 1),
(2, 'irony-winner-example-4.4.5', 'Active winner review', 2, 191, 2,
 'Inspect representative plan object in active-playset merged-winner report.', NULL, 'Representative active playset.',
 '2026-07-10T12:10:00Z', '2026-07-10T12:20:00Z', 'passed', 'Demonstration record.', 1),
(3, 'repo-validator-example-4.4.5', 'Repository static validation', 2, 195, 3,
 'Run deterministic project validator.', 'python tools/validate_stellar_ai_director_patch.py', 'Repository commit b605aa0e...',
 '2026-07-10T12:20:00Z', '2026-07-10T12:25:00Z', 'passed', 'Static safety only.', 1),
(4, 'observer-war-example-4.4.5', 'Bounded war-planning observer review', 2, 197, 1,
 'Inspect one observer run log and selected save for war-state evidence.', 'Inspect run log and extracted save fields.', 'One example run; no causal instrumentation.',
 '2026-07-09T12:38:02Z', '2026-07-09T13:25:40Z', 'inconclusive', 'Outcome evidence does not expose hidden engine causation.', 1),
(5, 'version-diff-example-4.5', '4.4.5 to 4.5 beta compatibility review', 3, 196, 2,
 'Review preserved patch notes and require exact source/schema diffs for touched surfaces.', 'Compare 4.4.5 and 4.5 beta touched folders.', 'Separate beta branch.',
 '2026-07-10T13:00:00Z', '2026-07-10T13:20:00Z', 'partial', 'Patch-note level evidence captured; exact full local diff remains work.', 1);

INSERT INTO claim(
    claim_id, claim_type_id, primary_item_id, statement, context,
    epistemic_note, supersedes_claim_id, lifecycle_state_id,
    created_by_actor_id, created_at, created_in_change_set_id,
    retired_in_change_set_id
) VALUES
(1, 4, 126, 'Launcher supported_version metadata does not prove that Stellaris script loaded correctly or that the mod is behaviorally compatible.', '4.4-line mod maintenance.', 'A process claim about evidence sufficiency.', NULL, 1, 2, '2026-07-10T16:05:00Z', 1, NULL),
(2, 3, 126, 'Setting supported_version to v4.4.* is sufficient proof that a mod is compatible with Stellaris 4.4.5.', 'Descriptor-only compatibility assertion.', 'Deliberately false/contradicted example.', NULL, 1, 2, '2026-07-10T16:05:00Z', 1, NULL),
(3, 5, 121, 'AI budget and economic-plan changes should be assessed together because plan priorities and resource allocation can interact.', 'Economic planning design hypothesis.', 'Supported structurally; runtime magnitude remains context-dependent.', NULL, 1, 2, '2026-07-10T16:06:00Z', 1, NULL),
(4, 1, 124, 'The current strategic-v2 war-planning configuration has been proven at runtime to cause appropriate war declarations.', 'One bounded observer run.', 'Deliberately over-strong statement for contradiction and uncertainty queries.', NULL, 1, 2, '2026-07-10T16:06:00Z', 1, NULL),
(5, 3, 128, 'The 4.5 beta pop/workforce changes require revalidation of 4.4 AI-economy assumptions before porting the subsystem.', 'Separate 4.5 porting branch.', 'Compatibility requirement derived from declared version changes.', NULL, 1, 2, '2026-07-10T16:07:00Z', 1, NULL),
(6, 3, 127, 'Stellaris 4.4.5 changes to Resource Abundance alter the strategic economy baseline that AI tuning assumes.', '4.4.5 compatibility review.', 'Version-specific patch-note claim; exact affected values still require local comparison.', NULL, 1, 2, '2026-07-10T16:07:00Z', 1, NULL),
(7, 1, 150, 'economic_plan.weight participates in plan selection or priority for the target version.', 'Representative field semantics.', 'Field existence can be schema-verified; exact engine weighting behavior may remain partly inferred.', NULL, 1, 2, '2026-07-10T16:08:00Z', 1, NULL),
(8, 5, 154, 'country_type.ai alone determines whether every country receives ordinary AI economic and war planning.', 'Country-type eligibility hypothesis.', 'Likely over-broad; requires object, engine, and runtime evidence.', NULL, 1, 2, '2026-07-10T16:08:00Z', 1, NULL),
(9, 2, 161, 'staid_should_prioritize_research is defined for country scope in the captured 4.4.5 repository snapshot.', 'Representative scripted trigger.', 'Source-backed structural claim.', NULL, 1, 2, '2026-07-10T16:09:00Z', 1, NULL),
(10, 5, 150, 'Changing economic_plan.weight can indirectly affect research-building demand through plan, budget, resource, job, and building relationships.', 'Impact-analysis hypothesis.', 'Path is explicit in the knowledge graph; actual magnitude needs validation.', NULL, 1, 2, '2026-07-10T16:09:00Z', 1, NULL),
(11, 6, 124, 'Long-run war-planning efficacy remains unproven for the current representative strategic branch.', 'Current project evidence status.', 'Negative status claim; static validation does not prove runtime efficacy.', NULL, 1, 2, '2026-07-10T16:10:00Z', 1, NULL),
(12, 3, 126, 'Findings verified only on 4.4.4 remain automatically current for 4.4.5 without revalidation.', 'Version carry-forward assertion.', 'Deliberately contradicted example.', NULL, 1, 2, '2026-07-10T16:10:00Z', 1, NULL);

INSERT INTO claim_item(claim_id, item_id, role_code, notes) VALUES
(1, 126, 'subject', NULL),
(2, 126, 'subject', NULL),
(3, 120, 'related', 'Budget side of the interaction.'),
(3, 121, 'subject', 'Plan side of the interaction.'),
(3, 110, 'subsystem', NULL),
(4, 111, 'subsystem', NULL),
(4, 123, 'input', NULL),
(4, 137, 'input', NULL),
(4, 138, 'input', NULL),
(5, 110, 'affected_subsystem', NULL),
(5, 125, 'affected_mechanic', NULL),
(6, 110, 'affected_subsystem', NULL),
(7, 121, 'owner_mechanic', NULL),
(8, 122, 'owner_mechanic', NULL),
(8, 132, 'example_object', NULL),
(9, 170, 'scope', NULL),
(10, 121, 'owner_mechanic', NULL),
(10, 134, 'possible_downstream', NULL),
(11, 111, 'subsystem', NULL),
(12, 126, 'subject', NULL);

INSERT INTO claim_assessment(
    claim_assessment_id, claim_id, version_span_id, assessment_state_id,
    confidence_level_id, verification_run_id, assessed_by_actor_id,
    assessed_at, basis_summary, reverify_after, is_current,
    supersedes_assessment_id, created_in_change_set_id
) VALUES
(1, 1, 4, 1, 5, NULL, 2, '2026-07-10T16:12:00Z', 'Project guidance explicitly separates descriptor metadata from load and behavior proof.', NULL, 1, NULL, 1),
(2, 2, 3, 4, 5, NULL, 2, '2026-07-10T16:12:00Z', 'Directly contradicted by the descriptor metadata caveat.', NULL, 1, NULL, 1),
(3, 3, 3, 2, 3, 1, 2, '2026-07-10T16:13:00Z', 'Related files, fields, and graph edges exist; runtime magnitude is not directly demonstrated.', '2026-09-01T00:00:00Z', 1, NULL, 1),
(4, 4, 3, 4, 4, 4, 2, '2026-07-10T16:13:00Z', 'The bounded run is inconclusive and the statement overclaims causation.', '2026-07-20T00:00:00Z', 1, NULL, 1),
(5, 5, 5, 2, 4, 5, 2, '2026-07-10T16:14:00Z', 'Patch-note changes touch core AI-economy assumptions; exact source diff remains required.', '2026-07-15T00:00:00Z', 1, NULL, 1),
(6, 6, 3, 1, 4, 5, 2, '2026-07-10T16:14:00Z', 'Preserved 4.4.5 patch-note evidence directly identifies the changed baseline.', NULL, 1, NULL, 1),
(7, 7, 3, 2, 3, 1, 2, '2026-07-10T16:15:00Z', 'Schema/source evidence supports the field; hidden selection semantics are not fully proved.', '2026-08-01T00:00:00Z', 1, NULL, 1),
(8, 8, 3, 3, 2, NULL, 2, '2026-07-10T16:15:00Z', 'No adequate evidence that one field universally controls all ordinary AI behavior.', '2026-07-01T00:00:00Z', 1, NULL, 1),
(9, 9, 3, 1, 4, 1, 2, '2026-07-10T16:16:00Z', 'Repository symbol and intended scope are directly locatable.', NULL, 1, NULL, 1),
(10, 10, 3, 2, 3, NULL, 2, '2026-07-10T16:16:00Z', 'The graph demonstrates a plausible dependency path; runtime magnitude is unresolved.', '2026-08-01T00:00:00Z', 1, NULL, 1),
(11, 11, 3, 1, 5, 4, 2, '2026-07-10T16:17:00Z', 'Project status and the inconclusive run directly support the negative finding.', '2026-07-20T00:00:00Z', 1, NULL, 1),
(12, 12, 3, 4, 5, NULL, 2, '2026-07-10T16:17:00Z', 'Project version policy requires 4.4.5 revalidation.', NULL, 1, NULL, 1);

INSERT INTO claim_evidence(
    claim_evidence_id, claim_id, evidence_locator_id, evidence_stance_id,
    directness_rank, strength_rank, verification_run_id, interpretation,
    created_in_change_set_id
) VALUES
(1, 1, 15, 1, 5, 5, NULL, 'Direct process guidance.', 1),
(2, 2, 15, 2, 5, 5, NULL, 'Direct contradiction.', 1),
(3, 3, 6, 1, 4, 3, 1, 'Budget implementation exists in the same subsystem.', 1),
(4, 3, 7, 1, 4, 3, 1, 'Economic-plan implementation exists in the same subsystem.', 1),
(5, 3, 10, 3, 2, 2, 4, 'Runtime evidence does not quantify the interaction.', 1),
(6, 4, 10, 2, 5, 4, 4, 'The run does not establish the claimed causal proof.', 1),
(7, 4, 11, 3, 4, 3, 4, 'Save evidence records outcomes but not hidden causation.', 1),
(8, 5, 12, 1, 4, 4, 5, 'Patch-note changes directly touch the assumptions.', 1),
(9, 5, 1, 1, 4, 4, NULL, 'Project policy independently requires a separate porting branch.', 1),
(10, 6, 13, 1, 5, 4, 5, 'Direct version-specific patch-note evidence.', 1),
(11, 7, 4, 1, 4, 3, 1, 'Schema supports the field structure.', 1),
(12, 7, 3, 1, 3, 3, 1, 'Vanilla object locator supplies an implementation reference.', 1),
(13, 7, 10, 3, 2, 2, 4, 'The runtime run does not isolate the field effect.', 1),
(14, 8, 1, 3, 2, 2, NULL, 'Project guidance requires broader verification and warns against invention.', 1),
(15, 9, 8, 1, 5, 4, 1, 'Direct project symbol locator.', 1),
(16, 10, 6, 1, 3, 3, NULL, 'Budget implementation supports part of the path.', 1),
(17, 10, 7, 1, 3, 3, NULL, 'Plan implementation supports part of the path.', 1),
(18, 10, 10, 2, 2, 2, 4, 'The observed run does not demonstrate the proposed downstream magnitude.', 1),
(19, 11, 10, 1, 5, 4, 4, 'Inconclusive runtime evidence supports the negative status claim.', 1),
(20, 11, 9, 3, 4, 3, 3, 'Static pass qualifies but cannot replace runtime proof.', 1),
(21, 12, 1, 2, 5, 5, NULL, 'Directly contradicts automatic carry-forward.', 1);

INSERT INTO claim_conflict(
    claim_conflict_id, claim_a_id, claim_b_id, version_span_id,
    conflict_kind, status_code, analysis, resolution_claim_id,
    created_in_change_set_id, resolved_in_change_set_id
) VALUES
(1, 1, 2, 3, 'mutually_exclusive_compatibility_rule', 'resolved', 'Descriptor metadata cannot both be insufficient and sufficient proof.', 1, 1, 1),
(2, 4, 11, 3, 'runtime_status_conflict', 'resolved', 'The positive proof claim conflicts with the verified negative status claim.', 11, 1, 1);

INSERT INTO open_question(
    question_id, question_key, primary_item_id, question_text,
    uncertainty_reason, target_version_id, status_code, priority,
    owner_actor_id, resolution_claim_id, next_review_at,
    created_in_change_set_id, closed_in_change_set_id
) VALUES
(1, 'question:plan-weight-construction-effect', 150, 'How much does changing economic_plan.weight alter research-building demand in a controlled 4.4.5 game?', 'The graph supplies a plausible path but no isolated runtime magnitude.', 2, 'open', 90, 1, NULL, '2026-07-20T00:00:00Z', 1, NULL),
(2, 'question:hidden-war-declaration-gates', 124, 'Which hidden engine gates remain between script-visible war weights and an actual declaration?', 'Static files and one save cannot reveal the full engine decision path.', 2, 'blocked', 100, 1, NULL, '2026-07-20T00:00:00Z', 1, NULL),
(3, 'question:4.5-pop-workforce-port', 128, 'Which exact 4.5 beta field, scope, and object changes invalidate the current AI-economy implementation?', 'Patch-note evidence identifies the risk family, but exact local file/schema diffs are incomplete.', 3, 'investigating', 95, 2, NULL, '2026-07-15T00:00:00Z', 1, NULL),
(4, 'question:illustrative-define', 165, 'What exact version-matched define, if any, corresponds to AI construction budget fraction?', 'The seed item is intentionally a placeholder and must not be used as a fact.', 2, 'open', 60, 2, NULL, '2026-07-15T00:00:00Z', 1, NULL);

INSERT INTO question_item(question_id, item_id, role_code, notes) VALUES
(1, 121, 'mechanic', NULL),
(1, 120, 'possible_mediator', NULL),
(1, 134, 'outcome', NULL),
(2, 123, 'input', NULL),
(2, 137, 'input', NULL),
(2, 138, 'input', NULL),
(3, 110, 'affected_subsystem', NULL),
(3, 125, 'affected_mechanic', NULL),
(4, 110, 'affected_subsystem', NULL);

INSERT INTO question_evidence(question_id, evidence_locator_id, relevance_code, notes) VALUES
(1, 10, 'missing_isolated_effect', 'Existing runtime evidence is not an isolated experiment.'),
(2, 10, 'hidden_causation_gap', NULL),
(2, 11, 'outcome_not_cause', NULL),
(3, 12, 'change_family', 'Patch notes define the high-risk surfaces.'),
(4, 1, 'verification_required', 'Project rules prohibit invented defines.');

-- Typed core sidecar example.
INSERT INTO ai_budget_mechanic_detail(
    ai_budget_mechanic_detail_id, mechanic_item_id, version_span_id,
    budget_owner_scope_item_id, allocation_unit, allocation_stage,
    reserve_behavior, exhaustion_behavior, basis_claim_id, notes,
    created_in_change_set_id
) VALUES
(1, 120, 3, 170, 'resource-specific budget object', 'economic planning/allocation',
 'Reserve behavior must be read from exact objects and validated against the active winner.',
 'Exhaustion behavior is not asserted by this representative seed.', 3,
 'Demonstrates mechanic-specific typed detail without adding generic EAV columns.', 1);

-- ---------------------------------------------------------------------------
-- G. Revalidation policies
-- ---------------------------------------------------------------------------

INSERT INTO revalidation_policy(
    revalidation_policy_id, policy_code, policy_name,
    trigger_on_any_game_update, minimum_version_change,
    trigger_on_source_change, max_age_days, preferred_tool_item_id,
    instructions, created_in_change_set_id
) VALUES
(1, 'every-game-patch', 'Revalidate after every Stellaris patch', 1, 'patch', 0, NULL, 193,
 'Retrieve the target-version source object and schema; compare fields, references, and related version changes.', 1),
(2, 'repository-source-change', 'Revalidate after source change', 0, NULL, 1, NULL, 195,
 'Run project validation and reassess claims and relations attached to changed source paths.', 1),
(3, 'runtime-evidence-30-days', 'Refresh runtime-sensitive knowledge', 0, NULL, 0, 30, 197,
 'Use a named run, exact game version/playset, and precise log/save locators.', 1),
(4, 'major-ai-economy-port', 'Full AI-economy port review', 1, 'minor', 1, NULL, 196,
 'Diff touched vanilla folders and schema, inspect active winners, and rerun static and bounded runtime checks.', 1);

INSERT INTO claim_revalidation_policy(claim_id, revalidation_policy_id, priority, notes) VALUES
(3, 2, 80, 'Reassess when plan or budget sources change.'),
(4, 3, 100, 'Runtime-sensitive overclaim.'),
(5, 4, 100, 'Required for 4.5 port.'),
(6, 1, 90, 'Galaxy-setting assumptions may change by patch.'),
(7, 1, 90, 'Field semantics are version-sensitive.'),
(8, 1, 100, 'Country-type behavior is version-sensitive and weakly supported.'),
(10, 2, 80, 'Impact path changes when source or graph changes.'),
(11, 3, 100, 'Negative status should be refreshed after a valid observer run.');

INSERT INTO item_revalidation_policy(item_id, revalidation_policy_id, priority, notes) VALUES
(110, 4, 100, 'Full subsystem port policy.'),
(111, 3, 90, 'Runtime-sensitive subsystem.'),
(120, 1, 90, 'Budget schema and behavior are version-sensitive.'),
(121, 1, 90, 'Plan schema and behavior are version-sensitive.'),
(128, 4, 100, '4.5 port risk.'),
(165, 1, 100, 'Placeholder must be replaced with exact source evidence.');

-- ---------------------------------------------------------------------------
-- H. Relationship graph, relation evidence, impact rules, and examples
-- ---------------------------------------------------------------------------

INSERT INTO item_relation(
    item_relation_id, source_item_id, relation_type_id, target_item_id,
    version_span_id, confidence_level_id, risk_level_id, source_claim_id,
    rationale, impact_explanation, review_action, validation_action,
    is_current, created_in_change_set_id, retired_in_change_set_id
) VALUES
(1, 120, 1, 110, 3, 5, 3, 3, 'AI budgets are a core part of economic planning.', 'Budget edits can alter subsystem resource allocation and downstream demand.', 'Review all budget objects, plan interactions, resources, and tests.', 'Run schema validation, active-winner inspection, and repository validation.', 1, 1, NULL),
(2, 121, 1, 110, 3, 5, 3, 3, 'Economic plans are a core part of economic planning.', 'Plan edits can alter priorities across budgets, construction, jobs, and research.', 'Review connected plan fields, budget relationships, and downstream objects.', 'Validate schema and run targeted behavioral checks if the claim is behavioral.', 1, 1, NULL),
(3, 122, 1, 111, 3, 4, 3, 8, 'Country types influence which countries are eligible for ordinary strategic processing.', 'Eligibility assumption changes can affect every strategic behavior.', 'Review country-type objects, exceptional countries, and runtime classification.', 'Check schema, active winners, and representative runtime countries.', 1, 1, NULL),
(4, 123, 1, 111, 3, 4, 3, 4, 'Personalities are a script-visible war-planning input.', 'Personality changes can alter diplomatic and strategic preferences but do not prove declarations.', 'Review personality fields, claims, CBs, war goals, and defines.', 'Static validation plus bounded runtime evidence.', 1, 1, NULL),
(5, 124, 1, 111, 3, 5, 4, 11, 'War planning is the defining mechanic of the subsystem.', 'Changes can cross claims, diplomacy, fleet readiness, and hidden engine gates.', 'Use the complete war-planning checklist and preserve uncertainty.', 'Static and runtime checks must be reported separately.', 1, 1, NULL),
(6, 125, 1, 110, 3, 5, 3, 10, 'Buildings and jobs realize economic-plan demand.', 'Changes can alter resource production, technology gates, and construction weights.', 'Review connected buildings, jobs, resources, technologies, and plan demand.', 'Run static validation and inspect a controlled planet state if behavior is claimed.', 1, 1, NULL),
(7, 150, 2, 130, 3, 5, 3, 7, 'weight is a field of the representative plan object.', 'A field edit changes the object definition and may propagate through its mechanic.', 'Inspect all occurrences and version-specific schema.', 'CWTools plus exact source comparison.', 1, 1, NULL),
(8, 151, 2, 130, 3, 3, 3, NULL, 'Representative focus field belongs to the example plan.', 'A field edit can change priority composition.', 'Verify that the field actually exists before editing.', 'CWTools and vanilla/mod source lookup.', 1, 1, NULL),
(9, 152, 2, 131, 3, 5, 3, NULL, 'resource is a field of the representative budget object.', 'Changing the budgeted resource redirects allocation consequences.', 'Review all references to old and new resources.', 'Schema validation and active-winner inspection.', 1, 1, NULL),
(10, 153, 2, 131, 3, 3, 3, NULL, 'Representative target field belongs to the budget object.', 'Changing the target expression can alter reserve or spending behavior.', 'Verify exact schema and all derived assumptions.', 'Schema and bounded runtime check.', 1, 1, NULL),
(11, 154, 2, 132, 3, 3, 4, 8, 'Representative AI field belongs to country type.', 'Eligibility edits can include or exclude whole country classes.', 'Review all country types and nonstandard countries.', 'Schema, active stack, save classification.', 1, 1, NULL),
(12, 155, 2, 133, 3, 3, 3, 4, 'Aggressiveness is represented as a personality field.', 'Changing it may alter preference but not guarantee an engine decision.', 'Review all related personality and war surfaces.', 'Static validation and runtime evidence.', 1, 1, NULL),
(13, 156, 2, 134, 3, 4, 3, NULL, 'AI construction weight is associated with a building.', 'Changing it can alter construction demand and resource balance.', 'Review technology, jobs, planet roles, and economic plan demand.', 'CWTools, active winner, and controlled planet inspection.', 1, 1, NULL),
(14, 157, 2, 135, 3, 4, 3, NULL, 'resources belongs to a job definition.', 'Changing outputs affects economy and plan satisfaction.', 'Review outputs, modifiers, buildings, and resource targets.', 'Schema plus controlled save/runtime check.', 1, 1, NULL),
(15, 158, 2, 137, 3, 3, 4, 4, 'AI weight is associated with a war goal.', 'Changing it may alter selection but cannot alone prove war declarations.', 'Review CB eligibility, claims, personalities, and hidden gates.', 'Static validation plus named runtime experiment.', 1, 1, NULL),
(16, 130, 3, 121, 3, 5, 3, 7, 'The plan object implements the economic-plans mechanic.', 'Object changes affect mechanic-level behavior.', 'Review mechanic claims and all connected budget/resource paths.', 'Static validation and reassessment of behavior claims.', 1, 1, NULL),
(17, 131, 3, 120, 3, 5, 3, 3, 'The budget object implements AI budgets.', 'Object changes affect allocation behavior.', 'Review budget detail and related resources.', 'Repository validator and active-winner inspection.', 1, 1, NULL),
(18, 132, 3, 122, 3, 3, 4, 8, 'The country-type object implements the country-type mechanic.', 'Eligibility changes propagate to strategic subsystems.', 'Review ordinary and exceptional country types.', 'Static and save-based classification checks.', 1, 1, NULL),
(19, 133, 3, 123, 3, 4, 3, 4, 'The personality object implements the personalities mechanic.', 'Preference changes can affect strategy.', 'Review war and diplomacy connections.', 'Static plus bounded runtime checks.', 1, 1, NULL),
(20, 134, 3, 125, 3, 4, 3, 10, 'The building is a concrete economic implementation example.', 'Building changes affect jobs, technology gates, and plan demand.', 'Review connected job, tech, modifiers, and plans.', 'Schema and controlled planet validation.', 1, 1, NULL),
(21, 135, 3, 125, 3, 4, 3, 10, 'The researcher job is a concrete economic implementation example.', 'Job changes affect resources and building demand.', 'Review resource outputs and providers.', 'Schema and controlled employment validation.', 1, 1, NULL),
(22, 121, 4, 181, 3, 5, 3, 7, 'The mechanic is implemented in the mod economic-plan file.', 'A mechanic change requires editing or reviewing this file.', 'Inspect file and all object keys within it.', 'Repository validator and source diff.', 1, 1, NULL),
(23, 120, 4, 180, 3, 5, 3, 3, 'The mechanic is implemented in the mod budget file.', 'A mechanic change requires editing or reviewing this file.', 'Inspect file and all budget object keys.', 'Repository validator and source diff.', 1, 1, NULL),
(24, 121, 4, 182, 3, 4, 2, 9, 'Decision-state triggers support plan selection.', 'Trigger changes can invalidate plan eligibility assumptions.', 'Review trigger definition, scope, and call sites.', 'CWTools and source-reference validation.', 1, 1, NULL),
(25, 121, 4, 183, 3, 3, 2, 10, 'ROI values may feed plan priorities.', 'Value changes can alter ranking and downstream demand.', 'Review value definitions and all references.', 'Repository validator and targeted comparison.', 1, 1, NULL),
(26, 121, 8, 120, 3, 4, 3, 3, 'Plan priorities and budgets interact in the economic subsystem.', 'A change on either side can invalidate assumptions on the other.', 'Review plan-to-budget resource mappings.', 'Static validation and targeted behavioral comparison.', 1, 1, NULL),
(27, 120, 7, 142, 3, 5, 3, 3, 'The representative budget controls alloy allocation.', 'Budget changes alter alloy reserves or spending demand.', 'Review alloy consumers, producers, and fleet/construction dependencies.', 'Inspect active budget winner and runtime resource state if behavior is claimed.', 1, 1, NULL),
(28, 120, 7, 143, 3, 3, 2, 10, 'Research budgeting may influence physics-research demand.', 'Budget changes can alter researcher/building demand.', 'Review plan resource mapping and researcher outputs.', 'Targeted source and runtime comparison.', 1, 1, NULL),
(29, 120, 7, 144, 3, 3, 2, 10, 'Research budgeting may influence society-research demand.', 'Budget changes can alter researcher/building demand.', 'Review plan resource mapping and researcher outputs.', 'Targeted source and runtime comparison.', 1, 1, NULL),
(30, 120, 7, 145, 3, 3, 2, 10, 'Research budgeting may influence engineering-research demand.', 'Budget changes can alter researcher/building demand.', 'Review plan resource mapping and researcher outputs.', 'Targeted source and runtime comparison.', 1, 1, NULL),
(31, 143, 7, 135, 3, 3, 2, 10, 'Physics research demand influences the researcher job path.', 'Changed demand should trigger job and building review.', 'Inspect researcher output and provider buildings.', 'Controlled employment and output check.', 1, 1, NULL),
(32, 144, 7, 135, 3, 3, 2, 10, 'Society research demand influences the researcher job path.', 'Changed demand should trigger job and building review.', 'Inspect researcher output and provider buildings.', 'Controlled employment and output check.', 1, 1, NULL),
(33, 145, 7, 135, 3, 3, 2, 10, 'Engineering research demand influences the researcher job path.', 'Changed demand should trigger job and building review.', 'Inspect researcher output and provider buildings.', 'Controlled employment and output check.', 1, 1, NULL),
(34, 135, 1, 134, 3, 4, 2, 10, 'The researcher job is provided by or associated with research buildings.', 'Job changes require reviewing provider buildings.', 'Inspect all providers and job counts.', 'Source lookup and controlled planet validation.', 1, 1, NULL),
(35, 134, 5, 146, 3, 4, 2, NULL, 'The representative research building is technology-gated.', 'Technology changes can invalidate building availability assumptions.', 'Review technology prerequisites and building potential.', 'Vanilla source/schema check.', 1, 1, NULL),
(36, 121, 6, 160, 3, 4, 2, 7, 'Economic planning may reference technology eligibility triggers.', 'Trigger signature or scope changes can break plan conditions.', 'Review all call sites and scope transitions.', 'Generated docs plus CWTools.', 1, 1, NULL),
(37, 121, 6, 161, 3, 5, 3, 9, 'The mechanic references the project research-priority trigger.', 'Trigger changes can alter plan eligibility.', 'Review trigger definition, scope, and callers.', 'CWTools and repository validator.', 1, 1, NULL),
(38, 121, 6, 163, 3, 3, 3, NULL, 'The mechanic may use the representative budget-phase effect.', 'Effect changes can alter allocation phase behavior.', 'Verify the effect exists and inspect call sites.', 'Generated docs/source lookup and static validation.', 1, 1, NULL),
(39, 121, 9, 170, 3, 4, 2, 9, 'Economic plans evaluate country-level state.', 'Scope rule changes can invalidate triggers and weights.', 'Review current/root/from transitions and country exceptions.', 'Generated docs and CWTools scope diagnostics.', 1, 1, NULL),
(40, 121, 8, 164, 3, 3, 2, 10, 'Plan demand interacts with research-production modifiers.', 'Modifier changes can alter how much demand is needed.', 'Review modifier sources and output calculations.', 'Vanilla/generated docs plus controlled comparison.', 1, 1, NULL),
(41, 121, 8, 165, 3, 1, 3, NULL, 'An AI construction define may interact with plan demand, but this seed identifier is unverified.', 'An invented or renamed define would invalidate any dependent implementation.', 'Resolve the exact define before use; keep the open question blocking.', 'Search local defines and version-matched documentation.', 1, 1, NULL),
(42, 121, 5, 146, 3, 4, 2, 7, 'Research plan paths depend on relevant technologies.', 'Technology changes can affect plan eligibility and construction paths.', 'Review prerequisites and gated objects.', 'Vanilla source and schema validation.', 1, 1, NULL),
(43, 110, 8, 111, 3, 3, 3, 10, 'Economic readiness and war planning interact through resource and fleet readiness.', 'Economic changes can alter strategic readiness; war changes can alter economic demand.', 'Review alloy, fleet, personality, and war-readiness assumptions.', 'Static graph review plus bounded runtime evidence.', 1, 1, NULL),
(44, 124, 8, 123, 3, 4, 3, 4, 'War planning interacts with personality weights.', 'Changes to either require reviewing the other.', 'Review personality and war input fields together.', 'Static validation plus runtime comparison.', 1, 1, NULL),
(45, 124, 8, 122, 3, 3, 4, 8, 'War planning interacts with country eligibility.', 'Country classification changes can include/exclude strategic actors.', 'Review country types and exceptional countries.', 'Schema, active winner, save classification.', 1, 1, NULL),
(46, 124, 5, 137, 3, 4, 4, 4, 'War planning depends on available war goals.', 'War-goal changes can block or redirect declarations.', 'Review goals, eligibility, and AI weights.', 'Vanilla/CWTools/Irony plus runtime evidence.', 1, 1, NULL),
(47, 124, 5, 138, 3, 4, 4, 4, 'War planning depends on available casus belli.', 'CB changes can block or redirect declarations.', 'Review CB generation, eligibility, and claims.', 'Vanilla/CWTools/Irony plus runtime evidence.', 1, 1, NULL),
(48, 124, 8, 142, 3, 3, 3, 10, 'War readiness interacts with alloy economy.', 'Alloy allocation changes can affect fleet readiness and strategic timing.', 'Review budget, ship construction, and readiness metrics.', 'Source review and bounded runtime comparison.', 1, 1, NULL),
(49, 126, 12, 128, 5, 5, 4, 5, '4.5 compatibility has a first-class concern with pop/workforce changes.', 'Porting without review can invalidate economy assumptions.', 'Run full version-port checklist.', 'Version diff, schema validation, and new-game tests.', 1, 1, NULL),
(50, 127, 8, 110, 3, 4, 3, 6, 'Resource Abundance changes the baseline for economic planning.', 'Tuning thresholds may no longer be calibrated.', 'Review economic targets and scenario assumptions.', 'Compare setting effects and rerun representative benchmarks.', 1, 1, NULL),
(51, 128, 8, 125, 5, 4, 4, 5, 'Pop/workforce changes interact directly with jobs and buildings.', '4.5 changes can invalidate job-output and construction assumptions.', 'Review jobs, buildings, districts, zones, and scopes.', 'Version diff and new-game compatibility tests.', 1, 1, NULL),
(52, 190, 10, 150, 3, 5, 1, NULL, 'CWTools validates field structure.', 'No impact propagation; this is a tool route.', NULL, NULL, 1, 1, NULL),
(53, 191, 10, 130, 3, 5, 1, NULL, 'Irony validates active winner/conflicts.', 'No impact propagation; this is a tool route.', NULL, NULL, 1, 1, NULL),
(54, 195, 10, 110, 3, 5, 1, NULL, 'Repository validator validates generated and referenced surfaces.', 'No impact propagation; this is a tool route.', NULL, NULL, 1, 1, NULL);

INSERT INTO relation_evidence(
    item_relation_id, evidence_locator_id, evidence_stance_id,
    strength_rank, interpretation
) VALUES
(7, 7, 1, 4, 'Source object contains the representative field occurrence.'),
(16, 7, 1, 4, 'Source locator ties the object to the plan mechanic.'),
(17, 6, 1, 4, 'Source locator ties the object to the budget mechanic.'),
(22, 7, 1, 5, 'Direct implementation file locator.'),
(23, 6, 1, 5, 'Direct implementation file locator.'),
(37, 8, 1, 5, 'Direct scripted-trigger locator.'),
(43, 10, 3, 2, 'Runtime evidence does not quantify this interaction.'),
(46, 10, 3, 2, 'Runtime evidence leaves hidden gates unresolved.'),
(47, 10, 3, 2, 'Runtime evidence leaves hidden gates unresolved.'),
(49, 12, 1, 4, 'Patch-note change family supports the compatibility edge.'),
(50, 13, 1, 4, 'Version-specific patch-note support.'),
(52, 4, 1, 5, 'Direct schema locator.'),
(53, 5, 1, 5, 'Direct active-winner locator.'),
(54, 9, 1, 5, 'Direct validator output locator.');

INSERT INTO impact_rule(
    impact_rule_id, relation_type_id, changed_item_type_id,
    affected_item_type_id, risk_level_id, investigation_task_type_id,
    preferred_tool_item_id, priority, action_template, validation_template,
    is_active, created_in_change_set_id
) VALUES
(1, 2, 5, 4, 3, 1, 193, 100, 'Inspect every occurrence of the changed field and its owning object.', 'Validate the field with CWTools and compare exact source definitions.', 1, 1),
(2, 3, 4, 2, 3, 9, 193, 95, 'Reassess mechanic claims and downstream relations for the changed object.', 'Run project validation and targeted source checks.', 1, 1),
(3, 1, 2, 3, 3, 9, 195, 95, 'Review the complete affected subsystem, not only the edited mechanic.', 'Run the subsystem checklist and static validation.', 1, 1),
(4, 4, 2, 13, 3, 1, 193, 90, 'Inspect and update the implementation file linked to the mechanic.', 'Diff the file and run repository validation.', 1, 1),
(5, 8, NULL, NULL, 3, 9, 192, 80, 'Review the interacting item and explain whether the interaction is material.', 'Use the relation-specific validation action and preserve uncertainty.', 1, 1),
(6, 5, NULL, NULL, 4, 9, 193, 100, 'Inspect the dependency because changing it can invalidate all dependants.', 'Verify exact definitions, active winners, and behavior-sensitive claims.', 1, 1),
(7, 6, NULL, NULL, 3, 1, 193, 95, 'Find every reference and call site affected by the changed symbol.', 'Validate scopes/signatures with generated docs and CWTools.', 1, 1),
(8, 7, NULL, NULL, 3, 9, 192, 85, 'Review the controlled downstream item and its validation requirements.', 'Run targeted source and behavioral checks appropriate to the affected type.', 1, 1),
(9, 12, NULL, NULL, 4, 3, 191, 100, 'Perform explicit compatibility review for both sides of the relation.', 'Inspect active winners and run the version/playset-specific checklist.', 1, 1);

INSERT INTO implementation_reference(
    implementation_reference_id, topic_item_id, example_item_id, reference_kind,
    version_span_id, evidence_locator_id, rationale, is_preferred,
    created_in_change_set_id
) VALUES
(1, 121, 185, 'vanilla_example', 3, 3, 'Use exact target-version vanilla economic plans as structural examples.', 1, 1),
(2, 121, 130, 'mod_example', 3, 7, 'Representative project economic-plan object.', 1, 1),
(3, 120, 186, 'vanilla_example', 3, 6, 'Use exact target-version vanilla budget objects as comparison points.', 1, 1),
(4, 120, 131, 'mod_example', 3, 6, 'Representative project budget object.', 1, 1),
(5, 125, 134, 'vanilla_example', 3, 3, 'Representative building example for research demand.', 0, 1),
(6, 124, 137, 'vanilla_example', 3, NULL, 'Representative war-goal example; exact target-version evidence is still required.', 0, 1),
(7, 126, 184, 'compatibility_example', 3, 1, 'Project tuning/compatibility notes provide context and route to primary sources.', 0, 1);

-- ---------------------------------------------------------------------------
-- I. Explicit version deltas
-- ---------------------------------------------------------------------------

INSERT INTO version_change(
    version_change_id, change_key, from_version_id, to_version_id,
    change_kind_id, summary, assessment_state_id, confidence_level_id,
    risk_level_id, review_required, migration_note,
    detected_by_verification_run_id, created_in_change_set_id
) VALUES
(1, 'change:4.4.4-to-4.4.5-resource-abundance', 1, 2, 5,
 'Resource Abundance changed the strategic economy baseline used by AI tuning.', 1, 4, 3, 1,
 'Review scenario baselines, thresholds, and benchmarks; do not assume 4.4.4 tuning transfers unchanged.', 5, 1),
(2, 'change:4.4.5-to-4.5-beta-pop-workforce', 2, 3, 3,
 'Pop groups, factions/ethics, jobs, and workforce assumptions changed in the 4.5 beta line.', 2, 4, 4, 1,
 'Use a separate porting branch; diff touched folders and schemas; validate with new disposable games.', 5, 1);

INSERT INTO version_change_item(version_change_id, item_id, role_code, notes) VALUES
(1, 127, 'subject', NULL),
(1, 110, 'affected', 'Economic planning thresholds and scenario baselines.'),
(1, 120, 'review', 'Budget assumptions.'),
(1, 121, 'review', 'Plan assumptions.'),
(2, 128, 'subject', NULL),
(2, 110, 'affected', 'AI economic planning.'),
(2, 125, 'affected', 'Building/job economy.'),
(2, 170, 'review', 'Country-scope assumptions.'),
(2, 171, 'review', 'Planet-scope assumptions.'),
(2, 172, 'review', 'Pop-scope assumptions.');

INSERT INTO version_change_evidence(version_change_id, evidence_locator_id, evidence_stance_id, notes) VALUES
(1, 13, 1, 'Version-specific patch-note evidence.'),
(2, 12, 1, 'Beta patch-note evidence; exact local source diff is still required.'),
(2, 1, 3, 'Project policy qualifies this as a separate port rather than an automatic upgrade.');

-- ---------------------------------------------------------------------------
-- J. Checklist and step-to-item links
-- ---------------------------------------------------------------------------

INSERT INTO checklist_target(checklist_item_id, target_item_id, version_span_id, applicability_note) VALUES
(200, 110, 3, 'Use for 4.4.5 economic-planning changes.'),
(200, 110, 5, 'Use as the base checklist plus the full version-port review for 4.5 beta.');

INSERT INTO checklist_step(
    checklist_step_id, checklist_item_id, step_number, phase_code, title,
    instruction, rationale, is_required, is_blocking, tool_item_id,
    investigation_task_type_id, expected_result, failure_action,
    version_span_id, created_in_change_set_id
) VALUES
(1, 200, 1, 'scope', 'Declare target and transaction',
 'Create a change_set; name the target version, item, intended behavior, non-goals, and rollback boundary.',
 'Prevents untraceable edits and accidental cross-version assumptions.', 1, 1, NULL, 9,
 'Open change_set and explicit target version.', 'Stop until the target and boundary are explicit.', NULL, 1),
(2, 200, 2, 'evidence', 'Retrieve current definitions and schema',
 'Retrieve exact vanilla/mod object definitions, field rules, generated symbol docs, and current claims for every edited item.',
 'Source and schema are authoritative for their own surfaces.', 1, 1, 193, 1,
 'Precise artifacts and locators for all edited surfaces.', 'Mark knowledge unknown/stale rather than guessing.', NULL, 1),
(3, 200, 3, 'impact', 'Run direct and transitive impact analysis',
 'Traverse v_impact_arc from each proposed changed item for the target version; preserve path, risk, review action, and validation action.',
 'Indirect dependencies are the primary reason for the knowledge graph.', 1, 1, 192, 9,
 'Deduplicated affected-item list with explanatory paths.', 'Add missing typed relations or open questions before editing.', NULL, 1),
(4, 200, 4, 'implementation', 'Inspect implementation and all call sites',
 'Inspect linked files, objects, fields, triggers, effects, scopes, defines, technologies, resources, and vanilla examples.',
 'A local edit may cross several script surfaces.', 1, 1, 193, 1,
 'Complete implementation-reference and call-site set.', 'Record unresolved references and do not proceed with invented identifiers.', NULL, 1),
(5, 200, 5, 'compatibility', 'Check active-playset winners and conflicts',
 'Use Irony for every overridden or contested object and record the actual winning definition and relevant load order.',
 'Repository source alone does not prove what the playset loads.', 1, 1, 191, 3,
 'Current conflict set and merged winner for every touched object.', 'Revise the patch boundary or add explicit compatibility work.', NULL, 1),
(6, 200, 6, 'edit', 'Apply the smallest coherent change',
 'Modify only the required files and update linked claims, assessments, relations, questions, and version status in the same change_set.',
 'Keeps implementation and durable knowledge synchronized.', 1, 1, NULL, 9,
 'Minimal diff with traceable knowledge updates.', 'Revert or split the change if unrelated surfaces are mixed.', NULL, 1),
(7, 200, 7, 'static', 'Run schema and scope diagnostics',
 'Run CWTools on every changed PDXScript file and resolve diagnostics, including scope and reference errors.',
 'Static schema errors should not reach runtime testing.', 1, 1, 190, 2,
 'No unresolved diagnostics within the accepted scope.', 'Fix or explicitly block the change.', NULL, 1),
(8, 200, 8, 'static', 'Run repository validation and tests',
 'Run the deterministic generator/validator/test commands relevant to the changed subsystem and record a verification_run.',
 'Project-specific invariants complement generic schema checks.', 1, 1, 195, 5,
 'Passing deterministic validation tied to the target commit.', 'Do not accept the change while required gates fail.', NULL, 1),
(9, 200, 9, 'runtime', 'Collect bounded runtime evidence when needed',
 'For behavioral claims, use an approved named run and record exact logs, save fields, setup, version, playset, and limitations.',
 'Static validation cannot prove hidden engine decisions or long-run efficacy.', 1, 0, 197, 6,
 'Run-specific evidence that supports, contradicts, or qualifies the claim.', 'Leave the claim inferred/uncertain if runtime proof is unavailable.', NULL, 1),
(10, 200, 10, 'close', 'Reassess and close the change set',
 'Supersede old assessments rather than overwriting history; resolve or retain contradictions; update revalidation dates; run database checks; commit the change_set.',
 'Preserves an auditable history and a reliable future queue.', 1, 1, NULL, 9,
 'Committed change_set, current assessments, open questions, and clean checks.', 'Keep the change_set open or abort it with a reason.', NULL, 1);

INSERT INTO checklist_step_item(checklist_step_id, item_id, role_code, notes) VALUES
(2, 150, 'inspect', 'Representative field.'),
(2, 130, 'inspect', 'Owning object.'),
(2, 185, 'compare', 'Vanilla example corpus.'),
(3, 110, 'validate', 'Target subsystem.'),
(4, 160, 'inspect', 'Related trigger.'),
(4, 161, 'inspect', 'Related scripted trigger.'),
(4, 163, 'inspect', 'Related scripted effect.'),
(4, 170, 'inspect', 'Related scope.'),
(4, 165, 'inspect', 'Unverified define placeholder must be resolved.'),
(4, 146, 'inspect', 'Related technology.'),
(4, 143, 'inspect', 'Related resource.'),
(4, 134, 'inspect', 'Representative building.'),
(5, 211, 'validate', 'Active playset.'),
(7, 181, 'validate', 'Economic-plan implementation.'),
(8, 180, 'validate', 'Budget implementation.'),
(8, 181, 'validate', 'Plan implementation.'),
(9, 212, 'validate', 'Runtime environment.'),
(10, 126, 'validate', 'Version and revalidation knowledge.');

-- ---------------------------------------------------------------------------
-- K. Project-aware corpus, playset, dataset, model, and observer examples
-- ---------------------------------------------------------------------------
-- These rows are grounded in the 2026-07-10 context-bundle snapshot at commit
-- b605aa0e85b5ac68c40a07fdb7c41ece02c365cd. Large generated datasets remain
-- authoritative external artifacts; this seed catalogs their complete column layouts
-- and stores only selected normalized facts with exact row/column locators.

-- Additional item types required by the actual Stellaris project corpus.
INSERT INTO item_type(
    item_type_id, type_code, type_name, description
) VALUES
(18, 'mod', 'Mod package', 'Vanilla, project, Workshop, compatibility, utility, or reference mod identity.'),
(19, 'playset', 'Playset', 'Stable logical playset whose captured membership changes over time.'),
(20, 'analysis_model', 'Analysis model', 'Registered inventory, valuation, policy, diagnostic, comparison, coverage, or observer model.'),
(21, 'benefit_class', 'Benefit class', 'Controlled strategic-benefit taxonomy class used by modeling policy.'),
(22, 'dlc', 'DLC or expansion', 'Versioned DLC/content assumption attached to an execution context.'),
(23, 'strategic_route', 'Strategic route', 'Named AI strategy or progression route used across policy surfaces.'),
(24, 'setting', 'Game or test setting', 'Galaxy, launcher, observer, or experimental setting relevant to evidence applicability.');

-- Object kinds observed in the current mod source tree and generated inventories.
INSERT INTO object_kind(
    object_kind_id, kind_code, kind_name, definition_folder, description
) VALUES
(12, 'district', 'District', 'common/districts', 'Planet, habitat, ring-world, or modded district definition.'),
(13, 'colony_type', 'Colony type', 'common/colony_types', 'Planet designation and AI specialization definition.'),
(14, 'ascension_perk', 'Ascension perk', 'common/ascension_perks', 'Ascension-perk definition and AI weighting.'),
(15, 'tradition', 'Tradition', 'common/traditions', 'Tradition-tree or tradition definition.'),
(16, 'megastructure', 'Megastructure', 'common/megastructures', 'Megastructure construction and upgrade definition.'),
(17, 'starbase_building', 'Starbase building', 'common/starbase_buildings', 'Starbase building definition.'),
(18, 'starbase_module', 'Starbase module', 'common/starbase_modules', 'Starbase module definition.'),
(19, 'component_template', 'Component template', 'common/component_templates', 'Ship or station component template.'),
(20, 'component_set', 'Component set', 'common/component_sets', 'Component-set metadata definition.'),
(21, 'component_tag', 'Component tag', 'common/component_tags', 'Component tag identifier.'),
(22, 'ship_behavior', 'Ship behavior', 'common/ship_behaviors', 'Combat or movement behavior definition.'),
(23, 'ship_size', 'Ship size', 'common/ship_sizes', 'Ship-size or section-bearing hull definition.'),
(24, 'scripted_modifier', 'Scripted modifier', 'common/scripted_modifiers', 'Reusable scripted modifier.'),
(25, 'edict', 'Edict', 'common/edicts', 'Edict definition.'),
(26, 'decision', 'Decision', 'common/decisions', 'Planet or country decision definition.'),
(27, 'federation_type', 'Federation type', 'common/federation_types', 'Federation type definition.'),
(28, 'bombardment_stance', 'Bombardment stance', 'common/bombardment_stances', 'Fleet bombardment stance definition.'),
(29, 'trait', 'Trait', 'common/traits', 'Species or leader trait definition.'),
(30, 'civic', 'Civic', 'common/governments/civics', 'Government civic definition.'),
(31, 'on_action', 'On action', 'common/on_actions', 'Engine hook registration.'),
(32, 'event', 'Event', 'events', 'Country, planet, ship, or other event definition.'),
(33, 'zone', 'Zone', 'common/zones', 'Planetary zone or build-out surface.'),
(34, 'inline_script', 'Inline script', 'common/inline_scripts', 'Reusable inline-script template.'),
(35, 'script_value', 'Script value', 'common/script_values', 'Reusable numeric expression.'),
(36, 'scripted_variable', 'Scripted variable', 'common/scripted_variables', 'Script-level variable constant.');

INSERT INTO evidence_source_type(
    evidence_source_type_id, type_code, type_name, default_reliability_rank, authoritative_scope, is_primary_evidence, description
) VALUES
(14, 'generated_dataset', 'Generated structured dataset', 88, 'Deterministic generated records for captured inputs', 1, 'CSV/JSON/JSONL outputs remain authoritative for their own rows and schemas.'),
(15, 'playset_snapshot', 'Captured playset snapshot', 90, 'Membership, order, and captured integration state for one playset snapshot', 1, 'Structured active-playset or Irony export.'),
(16, 'source_snapshot', 'Captured mod/source root', 90, 'Exact files present in a captured vanilla, Workshop, or project source root', 1, 'Path-preserving source snapshot or live root identity.'),
(17, 'runtime_observation', 'User/runtime observation', 65, 'Human-observed behavior correlated to a named run or save', 0, 'Observation must remain distinct from fields directly serialized or logged.');

INSERT INTO locator_type(
    locator_type_id, type_code, type_name, description
) VALUES
(11, 'dataset_cell', 'Dataset row/column', 'Dataset schema plus stable record key, optional row number, and column.'),
(12, 'json_path', 'JSON path', 'Artifact plus JSONPath-like path into a structured document.'),
(13, 'archive_member', 'Archive member', 'Archive artifact plus member path and optional byte range.'),
(14, 'file_hash', 'File hash identity', 'Cryptographic identity, size, and external retrieval path.'),
(15, 'playset_position', 'Playset load position', 'Captured playset member and load-order position.'),
(16, 'validation_finding', 'Validation finding', 'Run-specific finding key and result location.');

INSERT INTO investigation_task_type(
    investigation_task_type_id, task_code, task_name, description
) VALUES
(12, 'dataset_inspection', 'Dataset inspection', 'Retrieve rows, columns, aggregates, and schema from an authoritative external dataset.'),
(13, 'model_revalidation', 'Model revalidation', 'Regenerate a registered model and compare counts, schemas, policies, and issues.'),
(14, 'playset_resolution', 'Playset object resolution', 'Resolve the winning definition and conflict set for a captured playset.'),
(15, 'observer_analysis', 'Observer/save analysis', 'Analyze a named observer run, save set, or log set without conflating state with causation.'),
(16, 'schema_drift_review', 'Dataset schema-drift review', 'Compare registered versions of an external dataset schema and update mappings.');

INSERT INTO relation_type(
    relation_type_id, type_code, type_name, inverse_name, description, impact_propagation_mode, is_transitive_hint
) VALUES
(14, 'overrides', 'overrides', 'is overridden by', 'One definition intentionally supersedes another for the same loadable object.', 'both', 1),
(15, 'gated_by', 'is gated by', 'gates', 'Availability or use of the source depends on the target prerequisite or condition.', 'reverse', 1),
(16, 'unlocks', 'unlocks', 'is unlocked by', 'Source unlocks access to target.', 'forward', 1),
(17, 'consumes', 'consumes', 'is consumed by', 'Source consumes target resources or capacity; changes can affect both supply and demand review.', 'both', 1),
(18, 'generated_from', 'is generated from', 'generates', 'Generated model or artifact derives from target inputs.', 'reverse', 1),
(19, 'evaluated_by', 'is evaluated by', 'evaluates', 'Investigation or validation route without implying gameplay impact.', 'none', 0),
(20, 'feeds_model', 'feeds model', 'is fed by', 'Source evidence or dataset contributes inputs to the target model.', 'forward', 1),
(21, 'resolves_to', 'resolves to', 'is resolution of', 'Context-specific resolution relationship; not a gameplay impact edge.', 'none', 0);

INSERT INTO knowledge_item(
    item_id, item_type_id, canonical_key, display_name, summary, lifecycle_state_id, created_by_actor_id, created_in_change_set_id
) VALUES
(300, 18, 'mod:vanilla', 'Stellaris vanilla', 'Base-game scripted source and engine-owned behavior.', 1, 2, 1),
(301, 18, 'mod:stellar-ai-director', 'Stellar AI Director', 'Late-loading deterministic standalone AI replacement for the current high-scale playset.', 1, 2, 1),
(302, 18, 'mod:gigastructures', 'Gigastructural Engineering & More (4.4)', 'Required high-scale megastructure parent mod.', 1, 2, 1),
(303, 18, 'mod:nsc3', 'NSC3', 'Required ship-class and naval parent mod.', 1, 2, 1),
(304, 18, 'mod:esc-next', 'Extra Ship Components NEXT', 'Required component progression parent mod.', 1, 2, 1),
(305, 18, 'mod:starbase-extended', 'Starbase Extended 3.0', 'Required starbase parent mod.', 1, 2, 1),
(306, 18, 'mod:universal-resource-patch', 'Universal Resource Patch', 'Required/active resource-display and compatibility utility.', 1, 2, 1),
(307, 18, 'mod:planetary-diversity', 'Planetary Diversity', 'Active planet-system integration target.', 1, 2, 1),
(308, 18, 'mod:pd-more-arcologies', 'Planetary Diversity - More Arcologies', 'Active parent of naval-administration building overrides.', 1, 2, 1),
(309, 18, 'mod:ui-overhaul-dynamic', 'UI Overhaul Dynamic', 'Active UI dependency and compatibility surface.', 1, 2, 1),
(310, 18, 'mod:spacefleet-tactica', 'Spacefleet Tactica', 'Private equivalence/provenance reference; absent from the captured active playset.', 1, 2, 1),
(311, 18, 'mod:stellar-ai-reference', 'Stellar AI', 'Private parity reference; absent from the captured active playset.', 1, 2, 1),
(320, 19, 'playset:active-4.4-nsc3-pd', '4.4 NSC3/Planetary Diversity active playset', 'Captured 116-mod load order used by Director generation and compatibility analysis.', 1, 2, 1),
(330, 20, 'analysis-model:object-atlas', 'Object atlas and dependency graph', 'Inventories active-stack object definitions, references, parent AI support, and policy routes.', 1, 2, 1),
(331, 20, 'analysis-model:economic-capacity', 'Economic and research capacity model', 'Normalizes jobs, buildings, districts, zones, resources, scenarios, and strategic benefits.', 1, 2, 1),
(332, 20, 'analysis-model:build-plan-consumer', 'Build-plan readiness and consumer policy', 'Classifies hard gates, candidate status, fallback lifetime, formula policy, and consumer readiness.', 1, 2, 1),
(333, 20, 'analysis-model:observer-war-state', 'Observer war-state diagnostic', 'Measures serialized war readiness and outcomes without claiming hidden engine causation.', 1, 2, 1),
(340, 21, 'benefit-class:amenities', 'Amenities', 'Controlled strategic-benefit class: Amenities.', 1, 2, 1),
(341, 21, 'benefit-class:blocker_district_capacity', 'Blocker/district capacity', 'Controlled strategic-benefit class: Blocker/district capacity.', 1, 2, 1),
(342, 21, 'benefit-class:bombardment_resistance', 'Bombardment resistance', 'Controlled strategic-benefit class: Bombardment resistance.', 1, 2, 1),
(343, 21, 'benefit-class:crime_deviancy_control', 'Crime/deviancy control', 'Controlled strategic-benefit class: Crime/deviancy control.', 1, 2, 1),
(344, 21, 'benefit-class:defense_armies', 'Defense armies', 'Controlled strategic-benefit class: Defense armies.', 1, 2, 1),
(345, 21, 'benefit-class:diplomacy_envoys', 'Diplomacy/envoys', 'Controlled strategic-benefit class: Diplomacy/envoys.', 1, 2, 1),
(346, 21, 'benefit-class:direct_resource_support', 'Direct resource support', 'Controlled strategic-benefit class: Direct resource support.', 1, 2, 1),
(347, 21, 'benefit-class:empire_country_modifier', 'Empire/country modifiers', 'Controlled strategic-benefit class: Empire/country modifiers.', 1, 2, 1),
(348, 21, 'benefit-class:habitability', 'Habitability', 'Controlled strategic-benefit class: Habitability.', 1, 2, 1),
(349, 21, 'benefit-class:housing', 'Housing', 'Controlled strategic-benefit class: Housing.', 1, 2, 1),
(350, 21, 'benefit-class:megastructure_construction', 'Megastructure/construction', 'Controlled strategic-benefit class: Megastructure/construction.', 1, 2, 1),
(351, 21, 'benefit-class:migration_resettlement', 'Migration/resettlement', 'Controlled strategic-benefit class: Migration/resettlement.', 1, 2, 1),
(352, 21, 'benefit-class:naval_capacity', 'Naval capacity', 'Controlled strategic-benefit class: Naval capacity.', 1, 2, 1),
(353, 21, 'benefit-class:planet_capacity', 'Planet capacity', 'Controlled strategic-benefit class: Planet capacity.', 1, 2, 1),
(354, 21, 'benefit-class:pop_growth_assembly', 'Pop growth/assembly', 'Controlled strategic-benefit class: Pop growth/assembly.', 1, 2, 1),
(355, 21, 'benefit-class:research_speed', 'Research speed', 'Controlled strategic-benefit class: Research speed.', 1, 2, 1),
(356, 21, 'benefit-class:shipyard_throughput', 'Shipyard throughput', 'Controlled strategic-benefit class: Shipyard throughput.', 1, 2, 1),
(357, 21, 'benefit-class:stability', 'Stability', 'Controlled strategic-benefit class: Stability.', 1, 2, 1),
(358, 21, 'benefit-class:starbase_support', 'Starbase support', 'Controlled strategic-benefit class: Starbase support.', 1, 2, 1),
(359, 21, 'benefit-class:trade_policy_value', 'Trade/policy value', 'Controlled strategic-benefit class: Trade/policy value.', 1, 2, 1),
(360, 22, 'dlc:nomads', 'Nomads', '4.4-era content and compatibility assumption covering Arkships, Waystations, Waylines, and Contracts.', 1, 2, 1),
(361, 24, 'setting:resource-abundance', 'Resource Abundance', 'Galaxy setting whose 4.4.5 changes affect economy baselines.', 1, 2, 1),
(362, 24, 'setting:observer-all-ai', 'Observer all-AI mode', 'human_ai plus observe; country 0 is analyzed as an AI actor.', 1, 2, 1),
(363, 24, 'setting:game-speed-5', 'Observer game_speed 5', 'Dev-only observer speed shown by the UI as GAME_SPEED_6.', 1, 2, 1),
(370, 23, 'strategic-route:research_diplomacy_core', 'Research Diplomacy Core', 'Director policy route research_diplomacy_core.', 1, 2, 1),
(371, 23, 'strategic-route:economy_megastructure_core', 'Economy Megastructure Core', 'Director policy route economy_megastructure_core.', 1, 2, 1),
(372, 23, 'strategic-route:planetcraft_route', 'Planetcraft Route', 'Director policy route planetcraft_route.', 1, 2, 1),
(373, 23, 'strategic-route:conquest_escape_route', 'Conquest Escape Route', 'Director policy route conquest_escape_route.', 1, 2, 1),
(374, 23, 'strategic-route:raiding_pop_acquisition_route', 'Raiding Pop Acquisition Route', 'Director policy route raiding_pop_acquisition_route.', 1, 2, 1),
(400, 4, 'object:ai_budget:alloys_expenditure_megastructures', 'alloys_expenditure_megastructures', 'Director megastructure alloy budget override.', 1, 2, 1),
(401, 4, 'object:ai_budget:influence_expenditure_claims', 'influence_expenditure_claims', 'Claim influence budget route.', 1, 2, 1),
(402, 4, 'object:economic_plan:basic_economy_plan', 'basic_economy_plan', 'Full high-scale economic-plan replacement.', 1, 2, 1),
(403, 4, 'object:building:building_navel_base', 'building_navel_base', 'Planetary Diversity naval-administration building with Director hard AI gates.', 1, 2, 1),
(404, 4, 'object:building:building_navel_command', 'building_navel_command', 'Upgrade of building_navel_base.', 1, 2, 1),
(405, 4, 'object:colony_type:col_fortress', 'col_fortress', 'Vanilla fortress designation override with Director readiness gates.', 1, 2, 1),
(406, 4, 'object:colony_type:col_habitat_fortress', 'col_habitat_fortress', 'Habitat fortress designation override.', 1, 2, 1),
(407, 4, 'object:colony_type:col_research', 'col_research', 'Research-world designation plan commitment.', 1, 2, 1),
(408, 4, 'object:ascension_perk:ap_gigastructural_constructs', 'ap_gigastructural_constructs', 'Gigas progression ascension perk with Director route weighting.', 1, 2, 1),
(409, 4, 'object:ascension_perk:ap_celestial_printing', 'ap_celestial_printing', 'Planetcraft progression ascension perk.', 1, 2, 1),
(410, 4, 'object:ascension_perk:ap_technological_ascendancy', 'ap_technological_ascendancy', 'Research progression ascension perk.', 1, 2, 1),
(411, 12, 'technology:tech_mega_engineering', 'tech_mega_engineering', 'Core megastructure technology prerequisite.', 1, 2, 1),
(412, 4, 'object:job:low_tech_researcher', 'low_tech_researcher', 'Vanilla job record with explicit research output and consumer-goods upkeep.', 1, 2, 1),
(413, 11, 'resource:consumer_goods', 'consumer_goods', 'Consumer-goods resource.', 1, 2, 1),
(414, 11, 'resource:giga_sr_sentient_metal', 'giga_sr_sentient_metal', 'Gigastructures sentient-metal resource.', 1, 2, 1),
(415, 11, 'resource:giga_sr_negative_mass', 'giga_sr_negative_mass', 'Gigastructures negative-mass resource.', 1, 2, 1),
(416, 11, 'resource:giga_sr_amb_megaconstruction', 'giga_sr_amb_megaconstruction', 'Gigastructures supertensile/megaconstruction resource.', 1, 2, 1),
(417, 12, 'technology:tech_planetary_defenses', 'tech_planetary_defenses', 'Prerequisite for strongholds and naval-administration building.', 1, 2, 1),
(418, 4, 'object:building:building_stronghold', 'building_stronghold', 'Fortress-chain base building.', 1, 2, 1),
(419, 4, 'object:building:building_fortress', 'building_fortress', 'Fortress-chain upgrade.', 1, 2, 1),
(420, 4, 'object:bombardment_stance:raiding', 'raiding', 'Raiding bombardment stance with Director-owned AI weighting.', 1, 2, 1),
(421, 4, 'object:component_set:SFT_COMP_W_DRP_P_1', 'SFT_COMP_W_DRP_P_1', 'Spacefleet Tactica equivalence component set.', 1, 2, 1),
(422, 4, 'object:component_template:BIO_COMBAT_COMPUTER_SWARM_DEFAULT', 'BIO_COMBAT_COMPUTER_SWARM_DEFAULT', 'Biological-ship swarm computer template.', 1, 2, 1),
(423, 4, 'object:building:building_giga_matrioshka_brain_uplink_hell', 'building_giga_matrioshka_brain_uplink_hell', 'Generated model fallback example from Gigastructures.', 1, 2, 1),
(424, 5, 'field:country_type.ai.enabled', 'country_type.ai.enabled', 'Enables native AI for a country type.', 1, 2, 1),
(425, 5, 'field:country_type.ai.declare_war', 'country_type.ai.declare_war', 'Enables native war declaration processing.', 1, 2, 1),
(426, 5, 'field:country_type.ai.min_assault_armies_for_wars', 'country_type.ai.min_assault_armies_for_wars', 'Pre-planner assault-army threshold.', 1, 2, 1),
(427, 5, 'field:country_type.ai.min_navy_for_wars', 'country_type.ai.min_navy_for_wars', 'Pre-planner desired-navy threshold present in the 4.4.4 reference.', 1, 2, 1),
(428, 6, 'scripted-trigger:staid_naval_capacity_expansion_ready', 'staid_naval_capacity_expansion_ready', 'Director readiness trigger for naval-capacity construction.', 1, 2, 1),
(429, 12, 'technology:tech_global_defense_grid', 'tech_global_defense_grid', 'Upgrade prerequisite for fortress/naval command objects.', 1, 2, 1),
(431, 10, 'define:NAI.ENEMY_FLEET_POWER_MULT', 'NAI.ENEMY_FLEET_POWER_MULT', 'Loaded Director enemy-fleet multiplier used by diagnostic strength screening.', 1, 2, 1),
(432, 4, 'object:job:job_pd_naval_admin', 'job_pd_naval_admin', 'Planetary Diversity naval-administration job.', 1, 2, 1),
(433, 4, 'object:job:job_pd_naval_admin_gestalt', 'job_pd_naval_admin_gestalt', 'Gestalt naval-administration job.', 1, 2, 1),
(434, 11, 'resource:volatile_motes', 'volatile_motes', 'Volatile-motes strategic resource.', 1, 2, 1),
(500, 13, 'file:research/active-playset-json', 'stellar-ai-director-active-playset-2026-07-04.json', 'Captured 116-mod playset and required/optional integration state.', 1, 2, 1),
(501, 13, 'file:research/object-atlas', 'object-atlas-2026-07-06.csv', 'Generated active-stack object atlas.', 1, 2, 1),
(502, 13, 'file:research/dependency-edges', 'dependency-edges-2026-07-06.csv', 'Generated definition-reference and dependency edges.', 1, 2, 1),
(503, 13, 'file:research/parent-ai-support', 'parent-ai-support-map-2026-07-06.csv', 'Generated parent-AI support classification.', 1, 2, 1),
(504, 13, 'file:research/policy-matrix', 'policy-matrix-2026-07-06.csv', 'Generated route and Director action policy matrix.', 1, 2, 1),
(505, 13, 'file:research/capacity-jobs', 'stellar-ai-director-research-capacity-jobs-2026-07-09.csv', '501-row, 155-column active-stack job model.', 1, 2, 1),
(506, 13, 'file:research/capacity-buildings', 'stellar-ai-director-research-capacity-buildings-2026-07-09.csv', '826-row, 282-column building model.', 1, 2, 1),
(507, 13, 'file:research/capacity-development', 'stellar-ai-director-research-capacity-development-2026-07-09.csv', '547-row, 370-column district/zone model.', 1, 2, 1),
(508, 13, 'file:research/capacity-plan', 'stellar-ai-director-research-capacity-plan-2026-07-09.csv', '24-row research-colony scenario model.', 1, 2, 1),
(509, 13, 'file:research/colony-role-targets', 'stellar-ai-director-colony-role-targets-2026-07-09.csv', '247-row colony-role target model.', 1, 2, 1),
(510, 13, 'file:research/tech-modifiers', 'stellar-ai-director-research-capacity-tech-modifiers-2026-07-09.csv', '18-row research technology modifier inventory.', 1, 2, 1),
(511, 13, 'file:research/build-plan-readiness', 'stellar-ai-director-build-plan-readiness-2026-07-09.csv', '826-row hard-gate and fallback-readiness dataset.', 1, 2, 1),
(512, 13, 'file:research/benefit-taxonomy', 'stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv', '1,924-row strategic benefit taxonomy and policy classifications.', 1, 2, 1),
(513, 13, 'file:research/modeling-blockers', 'stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv', 'Current zero-row blocker accounting surface with stable schema.', 1, 2, 1),
(514, 13, 'file:research/consumer-policy', 'stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv', '1,093-row consumer policy surface.', 1, 2, 1),
(515, 13, 'file:bundle/selected-save-evidence', '11_SELECTED_SAVE_EVIDENCE.md', 'Hashed save manifest, derived war state, and interpretation limits.', 1, 2, 1),
(516, 13, 'file:bundle/source-manifest', '08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md', 'Repository and dataset catalog used to verify corpus coverage.', 1, 2, 1),
(517, 13, 'file:tool/research-capacity-generator', 'build_stellar_ai_research_capacity_dataset.py', 'Deterministic generator for capacity, readiness, taxonomy, blocker, and policy artifacts.', 1, 2, 1),
(518, 13, 'file:tool/director-library', 'stellar_ai_director_lib.py', 'Shared parsing, inventory, generator, and validation library.', 1, 2, 1),
(519, 13, 'file:mod/country-type-war-readiness', 'zzzzz_staid_18_native_war_readiness.txt', 'Director full-object default country-type override.', 1, 2, 1),
(520, 13, 'file:vanilla/country-types', '00_country_types.txt', 'Version-specific vanilla country-type source.', 1, 2, 1),
(521, 13, 'file:mod/pd-naval-hard-gates', 'zzzzz_staid_14_pd_naval_capacity_hard_gates.txt', 'Director overrides for PD naval-administration buildings.', 1, 2, 1),
(522, 13, 'file:research/benefit-taxonomy-archived', 'benefit-taxonomy schema at de022d94', 'Archived 1,887-row/19-column benefit-taxonomy schema checkpoint.', 1, 2, 1),
(523, 13, 'file:bundle/modeling-handoff', '10_STELLAR_AI_MODELING_HANDOFF.md', 'High-context modeling completion handoff.', 1, 2, 1),
(524, 13, 'file:bundle/project-guidance', '02_PROJECT_CONTROL_AND_GUIDANCE.md', 'Project rules, source order, tools, validation, and status reporting.', 1, 2, 1),
(525, 13, 'file:tool/object-atlas-generator', 'build_stellar_ai_director_object_atlas.py', 'Deterministic object-atlas generator entrypoint.', 1, 2, 1),
(526, 13, 'file:tool/war-state-analyzer', 'analyze_stellaris_war_state.py', 'Selected-save war-state diagnostic.', 1, 2, 1),
(550, 14, 'tool:object-atlas-generator', 'Object-atlas generator', 'Regenerates object atlas, dependency edges, parent AI support, and policy matrix.', 1, 2, 1),
(551, 14, 'tool:research-capacity-generator', 'Research-capacity generator', 'Regenerates capacity, readiness, benefit, blocker, and consumer-policy datasets.', 1, 2, 1),
(552, 14, 'tool:war-state-analyzer', 'War-state analyzer', 'Parses selected saves into serialized war-readiness evidence.', 1, 2, 1),
(553, 14, 'tool:context-bundle-generator', 'Context-bundle generator', 'Builds the point-in-time ChatGPT source bundle.', 1, 2, 1),
(554, 14, 'tool:sqlite-runtime', 'SQLite runtime validation', 'Executes schema/examples and database integrity checks.', 1, 2, 1);

INSERT INTO mod_package(
    item_id, mod_key, steam_workshop_id, mod_scope, author_or_owner, homepage_uri, notes
) VALUES
(300, 'vanilla', NULL, 'vanilla', 'Paradox Development Studio', NULL, 'Version captured through a local install root.'),
(301, 'stellar-ai-director', NULL, 'project_mod', 'Project maintainer', NULL, 'Repository source and generated local launcher copy are distinct surfaces.'),
(302, 'gigastructures', '1121692237', 'workshop_mod', NULL, NULL, 'Required parent.'),
(303, 'nsc3', '683230077', 'workshop_mod', NULL, NULL, 'Required parent.'),
(304, 'esc-next', '2648658105', 'workshop_mod', NULL, NULL, 'Required parent.'),
(305, 'starbase-extended', '3250900527', 'workshop_mod', NULL, NULL, 'Required parent.'),
(306, 'universal-resource-patch', '1595876588', 'utility', NULL, NULL, 'Active utility/integration.'),
(307, 'planetary-diversity', '819148835', 'workshop_mod', NULL, NULL, 'Active integration.'),
(308, 'pd-more-arcologies', '1732447147', 'workshop_mod', NULL, NULL, 'Active source of naval administration objects.'),
(309, 'ui-overhaul-dynamic', '1623423360', 'workshop_mod', NULL, NULL, 'Active UI dependency surface.'),
(310, 'spacefleet-tactica', '3696204283', 'reference_mod', NULL, NULL, 'Absent parity/equivalence source in captured playset.'),
(311, 'stellar-ai-reference', '3610149307', 'reference_mod', NULL, NULL, 'Absent private parity reference in captured playset.');

INSERT INTO playset(
    item_id, playset_key, manager_name, purpose, notes
) VALUES
(320, 'active-4.4-nsc3-pd', 'Irony Mod Manager / launcher snapshot', 'Represent the exact captured order and compatibility context used by current Director generation.', 'Live launcher state must be checked separately before a launch claim.');

INSERT INTO analysis_model(
    item_id, model_key, model_kind, purpose, authoritative_tool_item_id, authority_boundary, default_storage_policy, notes
) VALUES
(330, 'object-atlas', 'inventory', 'Inventory definitions, references, winners, parent AI support, and routes.', NULL, 'Authoritative only for captured generator inputs and generated rows.', 'locator_only', 'Selected definition/reference facts may be normalized.'),
(331, 'economic-capacity', 'valuation', 'Model resource flows, jobs, buildings, development objects, and scenario totals.', NULL, 'Generated arithmetic and classifications are authoritative for captured inputs; they do not prove runtime construction behavior.', 'normalized_facts', 'Wide columns are normalized as scenario + metric + resource dimensions.'),
(332, 'build-plan-consumer', 'policy', 'Model hard eligibility, readiness, fallback, benefit policy, and consumer status.', NULL, 'Policy classifications are project decisions tied to the generator version and source evidence.', 'normalized_facts', 'No generic score is invented for unsupported benefits.'),
(333, 'observer-war-state', 'observer', 'Measure serialized war state and selected runtime observations.', NULL, 'Save fields prove captured state; diagnostic screens and observations do not prove hidden engine causation.', 'selected_facts', 'Raw saves remain external and are addressed by hash.');

INSERT INTO game_object(
    item_id, object_kind_id, script_key, namespace, origin_class, notes
) VALUES
(400, 2, 'alloys_expenditure_megastructures', 'staid', 'mod', 'Full-object budget override.'),
(401, 2, 'influence_expenditure_claims', 'staid', 'mod', 'Claim budget route override.'),
(402, 1, 'basic_economy_plan', 'staid', 'mod', 'Full-object economic plan replacement.'),
(403, 5, 'building_navel_base', '', 'external_mod', 'Winning definition supplied by Director override.'),
(404, 5, 'building_navel_command', '', 'external_mod', 'Winning definition supplied by Director override.'),
(405, 13, 'col_fortress', '', 'vanilla', 'Director full-object override.'),
(406, 13, 'col_habitat_fortress', '', 'vanilla', 'Director full-object override.'),
(407, 13, 'col_research', '', 'vanilla', 'Director full-object override.'),
(408, 14, 'ap_gigastructural_constructs', '', 'external_mod', 'Gigas object overridden by Director.'),
(409, 14, 'ap_celestial_printing', '', 'external_mod', 'Gigas object overridden by Director.'),
(410, 14, 'ap_technological_ascendancy', '', 'vanilla', 'Vanilla object overridden by Director.'),
(411, 8, 'tech_mega_engineering', '', 'vanilla', NULL),
(412, 6, 'low_tech_researcher', '', 'vanilla', NULL),
(413, 7, 'consumer_goods', '', 'vanilla', NULL),
(414, 7, 'giga_sr_sentient_metal', '', 'external_mod', NULL),
(415, 7, 'giga_sr_negative_mass', '', 'external_mod', NULL),
(416, 7, 'giga_sr_amb_megaconstruction', '', 'external_mod', NULL),
(417, 8, 'tech_planetary_defenses', '', 'vanilla', NULL),
(418, 5, 'building_stronghold', '', 'vanilla', 'Director override exists.'),
(419, 5, 'building_fortress', '', 'vanilla', 'Director override exists.'),
(420, 28, 'raiding', '', 'vanilla', 'Director override exists.'),
(421, 20, 'SFT_COMP_W_DRP_P_1', 'SFT', 'external_mod', 'Copied equivalence source.'),
(422, 19, 'BIO_COMBAT_COMPUTER_SWARM_DEFAULT', '', 'vanilla', 'Director/SFT equivalence surface.'),
(423, 5, 'building_giga_matrioshka_brain_uplink_hell', '', 'external_mod', 'Generated fallback reference.'),
(429, 8, 'tech_global_defense_grid', '', 'vanilla', NULL),
(432, 6, 'job_pd_naval_admin', '', 'external_mod', NULL),
(433, 6, 'job_pd_naval_admin_gestalt', '', 'external_mod', NULL),
(434, 7, 'volatile_motes', '', 'vanilla', NULL);

INSERT INTO field_definition(
    item_id, owner_object_kind_id, field_name, value_type, cardinality, semantic_summary
) VALUES
(424, 3, 'ai.enabled', 'boolean', 'zero_or_one', 'Enables country-type native AI.'),
(425, 3, 'ai.declare_war', 'boolean', 'zero_or_one', 'Enables native war declaration processing.'),
(426, 3, 'ai.min_assault_armies_for_wars', 'integer', 'zero_or_one', 'Minimum assault-army gate before native war planning.'),
(427, 3, 'ai.min_navy_for_wars', 'real', 'zero_or_one', 'Minimum desired-navy coverage gate before native war planning.');

INSERT INTO script_symbol(
    item_id, script_symbol_kind_id, symbol_key, namespace, exposure_class, description
) VALUES
(428, 3, 'staid_naval_capacity_expansion_ready', 'staid', 'scripted', 'Country-scope readiness gate for naval-capacity infrastructure.'),
(431, 6, 'NAI.ENEMY_FLEET_POWER_MULT', '', 'built_in', 'Define used by the diagnostic 0.55 enemy-strength screen.');

INSERT INTO file_asset(
    item_id, corpus_code, relative_path, file_role, load_order_note
) VALUES
(500, 'repository', 'research/stellar-ai/stellar-ai-director-active-playset-2026-07-04.json', 'evidence/context', NULL),
(501, 'repository', 'research/stellar-ai/object-atlas/object-atlas-2026-07-06.csv', 'generated dataset', NULL),
(502, 'repository', 'research/stellar-ai/object-atlas/dependency-edges-2026-07-06.csv', 'generated dataset', NULL),
(503, 'repository', 'research/stellar-ai/object-atlas/parent-ai-support-map-2026-07-06.csv', 'generated dataset', NULL),
(504, 'repository', 'research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv', 'generated dataset', NULL),
(505, 'repository', 'research/stellar-ai/stellar-ai-director-research-capacity-jobs-2026-07-09.csv', 'generated dataset', NULL),
(506, 'repository', 'research/stellar-ai/stellar-ai-director-research-capacity-buildings-2026-07-09.csv', 'generated dataset', NULL),
(507, 'repository', 'research/stellar-ai/stellar-ai-director-research-capacity-development-2026-07-09.csv', 'generated dataset', NULL),
(508, 'repository', 'research/stellar-ai/stellar-ai-director-research-capacity-plan-2026-07-09.csv', 'generated dataset', NULL),
(509, 'repository', 'research/stellar-ai/stellar-ai-director-colony-role-targets-2026-07-09.csv', 'generated dataset', NULL),
(510, 'repository', 'research/stellar-ai/stellar-ai-director-research-capacity-tech-modifiers-2026-07-09.csv', 'generated dataset', NULL),
(511, 'repository', 'research/stellar-ai/stellar-ai-director-build-plan-readiness-2026-07-09.csv', 'generated dataset', NULL),
(512, 'repository', 'research/stellar-ai/stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv', 'generated dataset', NULL),
(513, 'repository', 'research/stellar-ai/stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv', 'generated dataset', NULL),
(514, 'repository', 'research/stellar-ai/stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv', 'generated dataset', NULL),
(515, 'repository', 'chatgpt_context_bundle/11_SELECTED_SAVE_EVIDENCE.md', 'evidence/context', NULL),
(516, 'repository', 'chatgpt_context_bundle/08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md', 'evidence/context', NULL),
(517, 'repository', 'tools/build_stellar_ai_research_capacity_dataset.py', 'source code', NULL),
(518, 'repository', 'tools/stellar_ai_director_lib.py', 'source code', NULL),
(519, 'repository', 'mods/StellarAIDirector/common/country_types/zzzzz_staid_18_native_war_readiness.txt', 'source code', 'Resolve active winner separately when the path is loadable game data.'),
(520, 'vanilla-4.4.5', 'vanilla-4.4.5/common/country_types/00_country_types.txt', 'evidence/context', NULL),
(521, 'repository', 'mods/StellarAIDirector/common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt', 'source code', 'Resolve active winner separately when the path is loadable game data.'),
(522, 'repository', 'research/stellar-ai/archive/benefit-taxonomy-at-de022d94', 'generated dataset', NULL),
(523, 'repository', 'chatgpt_context_bundle/10_STELLAR_AI_MODELING_HANDOFF.md', 'evidence/context', NULL),
(524, 'repository', 'chatgpt_context_bundle/02_PROJECT_CONTROL_AND_GUIDANCE.md', 'evidence/context', NULL),
(525, 'repository', 'tools/build_stellar_ai_director_object_atlas.py', 'source code', NULL),
(526, 'repository', 'tools/analyze_stellaris_war_state.py', 'source code', NULL);

INSERT INTO tool(
    item_id, tool_kind, executable_or_entrypoint, authority_scope, default_invocation, output_locator_pattern, is_local_only, notes
) VALUES
(550, 'repository script', 'python tools/build_stellar_ai_director_object_atlas.py', 'Generated object inventory and dependency surfaces', 'python tools/build_stellar_ai_director_object_atlas.py', 'CSV row and generation report', 1, 'Use JDataMunch for row/column inspection.'),
(551, 'repository script', 'python tools/build_stellar_ai_research_capacity_dataset.py', 'Generated capacity/readiness/policy model', 'python tools/build_stellar_ai_research_capacity_dataset.py', 'CSV row, schema, and generated summary', 1, 'Generated datasets remain authoritative for their own rows.'),
(552, 'repository script', 'python tools/analyze_stellaris_war_state.py', 'Selected-save serialized war-state analysis', 'python tools/analyze_stellaris_war_state.py <save> --observer-all-ai', 'JSON report and save hash', 1, 'Diagnostic screen, not hidden-engine proof.'),
(553, 'repository script', 'python chatgpt_context_bundle/tools/generate_bundle.py', 'Point-in-time source-bundle generation', 'python chatgpt_context_bundle/tools/generate_bundle.py', 'Bundle manifest and Markdown context files', 1, 'Bundle is a snapshot, not live truth.'),
(554, 'runtime/library', 'Python sqlite3 / sqlite3 CLI', 'SQLite schema execution, foreign-key checks, integrity checks, and query validation', NULL, 'Database file and check output', 1, 'Use the same schema/examples bytes delivered to the implementer.');

UPDATE analysis_model
SET authoritative_tool_item_id = CASE item_id
    WHEN 330 THEN 550
    WHEN 331 THEN 551
    WHEN 332 THEN 551
    WHEN 333 THEN 552
END
WHERE item_id IN (330,331,332,333);

INSERT INTO tool_capability(
    tool_capability_id, tool_item_id, investigation_task_type_id, capability_summary, invocation_template, expected_output, limitations, priority
) VALUES
(20, 550, 12, 'Regenerate and inspect object-atlas, dependency, parent-AI, and policy records.', 'Run generator, then inspect with JDataMunch.', 'Versioned CSV schemas and records.', 'Depends on captured source roots and active playset inputs.', 100),
(21, 551, 13, 'Regenerate economic/modeling artifacts and compare counts, schemas, policies, and blockers.', 'Run generator and validate every output dataset.', 'Deterministic CSV suite.', 'Does not prove runtime AI behavior.', 100),
(22, 552, 15, 'Analyze selected save state in observer/all-AI mode.', 'analyze_stellaris_war_state.py <save> --observer-all-ai', 'Serialized state summary and country rows.', 'Landed assault armies may be undercounted; hidden gates remain unexposed.', 95),
(23, 553, 10, 'Refresh the project context snapshot.', 'generate_bundle.py', 'Manifest plus context Markdown.', 'Must not be treated as live state after later repo/launcher changes.', 90),
(24, 554, 16, 'Execute schema/examples and report foreign-key, integrity, and semantic checks.', 'Load schema then examples into a fresh SQLite database.', 'Check results and query row counts.', 'Does not validate Stellaris game behavior.', 100);

INSERT INTO tool_route(
    tool_route_id, tool_capability_id, target_item_id, target_item_type_id, evidence_source_type_id, version_span_id, route_priority, instructions, fallback_tool_capability_id, is_active
) VALUES
(20, 20, 330, NULL, NULL, 3, 100, 'Regenerate before trusting object-atlas winners or dependency edges after source/playset change.', 9, 1),
(21, 21, 331, NULL, NULL, 3, 100, 'Regenerate and schema-compare all model CSVs; normalize only selected facts.', 9, 1),
(22, 21, 332, NULL, NULL, 3, 100, 'Treat unresolved issue rows and blocked policies as stop signs for final consumers.', 9, 1),
(23, 22, 333, NULL, NULL, 3, 100, 'Use only manually selected, hashed saves and preserve observer/all-AI semantics.', 7, 1),
(24, 24, NULL, 20, NULL, NULL, 100, 'Validate every delivered schema/examples pair in a new database.', NULL, 1);

INSERT INTO repository_snapshot(
    repository_snapshot_id, snapshot_key, repository_name, repository_root, branch_name, commit_sha, worktree_state, captured_at, notes, created_in_change_set_id
) VALUES
(1, 'stellaris-mods-b605aa0e-2026-07-10', 'StellarisMods', 'C:/Users/Admin/Documents/GIT/GameMods/StellarisMods', 'codex/stellar-ai-director-strategic-v2', 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'dirty', '2026-07-10T10:06:43-04:00', 'Point-in-time context-bundle snapshot; repository remains live source of truth.', 1);

INSERT INTO mod_release(
    mod_release_id, mod_item_id, release_key, version_text, version_span_id, supported_game_pattern, remote_file_id, descriptor_artifact_id, captured_at, release_status, notes, created_in_change_set_id
) VALUES
(1, 300, 'vanilla-4.4.5', '4.4.5', 3, '4.4.5', NULL, NULL, '2026-07-10T10:06:43-04:00', 'active', 'Local vanilla install target.', 1),
(2, 301, 'director-b605aa0e', 'b605aa0e', 3, 'v4.4.*', NULL, NULL, '2026-07-10T10:06:43-04:00', 'active', 'Repository snapshot; live launcher copy is separate.', 1),
(3, 302, 'gigas-1121692237-2026-07-04', NULL, 3, NULL, '1121692237', NULL, '2026-07-04T00:00:00Z', 'active', 'Captured Workshop source root.', 1),
(4, 303, 'nsc3-683230077-2026-07-04', NULL, 3, NULL, '683230077', NULL, '2026-07-04T00:00:00Z', 'active', 'Captured Workshop source root.', 1),
(5, 304, 'esc-next-2648658105-2026-07-04', NULL, 3, NULL, '2648658105', NULL, '2026-07-04T00:00:00Z', 'active', 'Captured Workshop source root.', 1),
(6, 305, 'starbase-extended-3250900527-2026-07-04', NULL, 3, NULL, '3250900527', NULL, '2026-07-04T00:00:00Z', 'active', 'Captured Workshop source root.', 1),
(7, 306, 'urp-1595876588-2026-07-04', NULL, 3, NULL, '1595876588', NULL, '2026-07-04T00:00:00Z', 'active', 'Captured Workshop source root.', 1),
(8, 307, 'pd-819148835-2026-07-04', NULL, 3, NULL, '819148835', NULL, '2026-07-04T00:00:00Z', 'active', 'Captured Workshop source root.', 1),
(9, 308, 'pd-more-arcologies-1732447147-2026-07-04', NULL, 3, NULL, '1732447147', NULL, '2026-07-04T00:00:00Z', 'active', 'Captured Workshop source root.', 1),
(10, 309, 'uiod-1623423360-2026-07-04', NULL, 3, NULL, '1623423360', NULL, '2026-07-04T00:00:00Z', 'active', 'Captured Workshop source root.', 1),
(11, 310, 'sft-reference-missing', NULL, 3, NULL, '3696204283', NULL, '2026-07-04T00:00:00Z', 'missing', 'Parity/equivalence reference absent from captured active playset.', 1),
(12, 311, 'stellar-ai-reference-missing', NULL, 3, NULL, '3610149307', NULL, '2026-07-04T00:00:00Z', 'missing', 'Parity reference absent from captured active playset.', 1);

INSERT INTO source_root(
    source_root_id, root_key, root_kind, canonical_path, repository_snapshot_id, mod_release_id, game_version_id, captured_at, availability_status, content_hash_algorithm, content_hash_value, authoritative_for, notes, created_in_change_set_id
) VALUES
(1, 'repo:stellaris-mods-b605aa0e', 'repository', 'C:/Users/Admin/Documents/GIT/GameMods/StellarisMods', 1, NULL, NULL, '2026-07-10T10:06:43-04:00', 'available', NULL, NULL, 'Repository source and project tools.', 'Dirty point-in-time snapshot.', 1),
(2, 'vanilla:4.4.5', 'vanilla_install', 'C:/Steam/steamapps/common/Stellaris', NULL, 1, 2, '2026-07-10T10:06:43-04:00', 'available', NULL, NULL, 'Exact local vanilla scripted definitions.', 'Live install path recorded by project guidance.', 1),
(3, 'project-mod:stellar-ai-director-b605aa0e', 'project_mod', 'C:/Users/Admin/Documents/GIT/GameMods/StellarisMods/mods/StellarAIDirector', 1, 2, 2, '2026-07-10T10:06:43-04:00', 'available', NULL, NULL, 'Director source files at repository snapshot.', 'Not proof of live launcher copy.', 1),
(4, 'workshop:gigas-1121692237', 'workshop_live', 'C:/Steam/steamapps/workshop/content/281990/1121692237', NULL, 3, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'Gigas source at captured playset time.', NULL, 1),
(5, 'workshop:nsc3-683230077', 'workshop_live', 'C:/Steam/steamapps/workshop/content/281990/683230077', NULL, 4, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'NSC3 source at captured playset time.', NULL, 1),
(6, 'workshop:esc-next-2648658105', 'workshop_live', 'C:/Steam/steamapps/workshop/content/281990/2648658105', NULL, 5, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'ESC NEXT source at captured playset time.', NULL, 1),
(7, 'workshop:starbase-extended-3250900527', 'workshop_live', 'C:/Steam/steamapps/workshop/content/281990/3250900527', NULL, 6, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'Starbase Extended source at captured playset time.', NULL, 1),
(8, 'workshop:urp-1595876588', 'workshop_live', 'C:/Steam/steamapps/workshop/content/281990/1595876588', NULL, 7, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'URP source at captured playset time.', NULL, 1),
(9, 'workshop:pd-819148835', 'workshop_live', 'C:/Steam/steamapps/workshop/content/281990/819148835', NULL, 8, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'Planetary Diversity source.', NULL, 1),
(10, 'workshop:pd-more-arcologies-1732447147', 'workshop_live', 'C:/Steam/steamapps/workshop/content/281990/1732447147', NULL, 9, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'PD More Arcologies source.', NULL, 1),
(11, 'workshop:uiod-1623423360', 'workshop_live', 'C:/Steam/steamapps/workshop/content/281990/1623423360', NULL, 10, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'UI Overhaul Dynamic source.', NULL, 1),
(12, 'generated:research-stellar-ai', 'generated', 'research/stellar-ai', 1, NULL, 2, '2026-07-10T10:06:43-04:00', 'available', NULL, NULL, 'Generated model and validation artifacts.', 'Datasets remain external authority.', 1),
(13, 'saves:selected-20260710', 'saves', 'C:/Users/Admin/AppData/Local/Temp/staid_bundle_save_stage_20260710_1008', NULL, NULL, 2, '2026-07-10T10:08:00-04:00', 'available', NULL, NULL, 'Only manually staged saves.', 'General save directory was not scanned.', 1),
(14, 'playset:captured-20260704', 'launcher', 'C:/Users/Admin/AppData/Roaming/Mario', NULL, NULL, 2, '2026-07-04T00:00:00Z', 'available', NULL, NULL, 'Captured active playset membership and order.', 'Not a claim about later live launcher state.', 1);

UPDATE source_artifact SET repository_snapshot_id=1 WHERE source_artifact_id IN (1,5,6,7,8,13);
UPDATE source_artifact SET source_root_id=1 WHERE source_artifact_id IN (1,13);
UPDATE source_artifact SET source_root_id=2, mod_release_id=1 WHERE source_artifact_id=2;
UPDATE source_artifact SET source_root_id=3, repository_snapshot_id=1, mod_release_id=2 WHERE source_artifact_id IN (5,6,7);
UPDATE object_definition SET source_root_id=3, mod_release_id=2, object_path='mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt' WHERE object_definition_id=1;
UPDATE object_definition SET source_root_id=3, mod_release_id=2, object_path='mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt' WHERE object_definition_id=2;
UPDATE object_definition SET source_root_id=2, mod_release_id=1, object_path='common/buildings/05_research_buildings.txt' WHERE object_definition_id=4;
UPDATE object_field_occurrence SET object_definition_id=1 WHERE object_field_occurrence_id IN (1,2);
UPDATE object_field_occurrence SET object_definition_id=2 WHERE object_field_occurrence_id IN (3,4);

INSERT INTO source_system(
    source_system_id, system_key, system_name, evidence_source_type_id, canonical_root, access_mode, authoritative_for, default_tool_item_id, retrieval_instructions, is_local_only, notes, created_in_change_set_id
) VALUES
(12, 'generated-research-datasets', 'Generated Stellar AI research datasets', 14, 'research/stellar-ai', 'filesystem/JDataMunch', 'Generated row values, schemas, counts, and classifications for captured inputs', 194, 'Use JDataMunch; record dataset schema, stable key, row, and column.', 1, 'Do not copy whole datasets into the knowledge base.', 1),
(13, 'captured-active-playset', 'Captured active playset JSON', 15, 'research/stellar-ai/stellar-ai-director-active-playset-2026-07-04.json', 'filesystem/JSON', 'Captured membership, order, required mods, optional integrations, and absent references', 191, 'Record snapshot key, JSON path, mod identity, and position.', 1, 'Refresh before current launcher claims.', 1),
(14, 'captured-mod-source-roots', 'Captured vanilla/Workshop/project source roots', 16, 'C:/Steam and repository roots', 'filesystem/index', 'Exact source occurrences available at the captured time', 193, 'Use the source_root identity plus exact path/object key.', 1, NULL, 1),
(15, 'selected-runtime-observations', 'Selected save report and user observation', 17, 'chatgpt_context_bundle/11_SELECTED_SAVE_EVIDENCE.md', 'document/save extractor', 'Run-correlated human observations and interpretation boundaries', 192, 'Separate user-observed behavior from parsed save fields.', 1, NULL, 1);

INSERT INTO source_artifact(
    source_artifact_id, source_system_id, source_root_id, repository_snapshot_id, mod_release_id, stable_key, artifact_kind, title, uri_or_path, repository_relative_path, game_version_id, repository_commit, tool_version, content_hash_algorithm, content_hash_value, file_size_bytes, mime_type, modified_at, captured_at, observed_at, availability_status, notes, created_in_change_set_id
) VALUES
(20, 13, 14, 1, NULL, 'active-playset-2026-07-04', 'json', 'Stellar AI Director active playset snapshot', 'research/stellar-ai/stellar-ai-director-active-playset-2026-07-04.json', 'research/stellar-ai/stellar-ai-director-active-playset-2026-07-04.json', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, 'SHA-256', '0574493084e12a50488ac6f5f9a7a7d0b698b0fed5466f6827e7cced84535fa7', 23264, 'application/json', NULL, '2026-07-10T10:06:43-04:00', '2026-07-04T00:00:00Z', 'available', '116 captured members.', 1),
(21, 12, 12, 1, NULL, 'object-atlas-2026-07-06', 'csv', 'Stellar AI Director object atlas', 'research/stellar-ai/object-atlas/object-atlas-2026-07-06.csv', 'research/stellar-ai/object-atlas/object-atlas-2026-07-06.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, 7367711, 'text/csv', NULL, '2026-07-06T00:00:00Z', NULL, 'available', 'Large external dataset; locator-only by default.', 1),
(22, 12, 12, 1, NULL, 'dependency-edges-2026-07-06', 'csv', 'Object-atlas dependency edges', 'research/stellar-ai/object-atlas/dependency-edges-2026-07-06.csv', 'research/stellar-ai/object-atlas/dependency-edges-2026-07-06.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, 5406610, 'text/csv', NULL, '2026-07-06T00:00:00Z', NULL, 'available', 'Large external edge dataset.', 1),
(23, 12, 12, 1, NULL, 'parent-ai-support-map-2026-07-06', 'csv', 'Parent AI support map', 'research/stellar-ai/object-atlas/parent-ai-support-map-2026-07-06.csv', 'research/stellar-ai/object-atlas/parent-ai-support-map-2026-07-06.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, 5242573, 'text/csv', NULL, '2026-07-06T00:00:00Z', NULL, 'available', 'Large external support dataset.', 1),
(24, 12, 12, 1, NULL, 'policy-matrix-2026-07-06', 'csv', 'Object-atlas policy matrix', 'research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv', 'research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, 2329976, 'text/csv', NULL, '2026-07-06T00:00:00Z', NULL, 'available', 'Large external route/policy dataset.', 1),
(25, 12, 12, 1, NULL, 'stellar-ai-director-research-capacity-jobs-2026-07-09', 'csv', 'Research-capacity jobs', 'research/stellar-ai/stellar-ai-director-research-capacity-jobs-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-research-capacity-jobs-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '5afc7a49f6c7d8910e81fa08380259aeb8cee68ac25b6cb687eebefe76e07313', 415398, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(26, 12, 12, 1, NULL, 'stellar-ai-director-research-capacity-buildings-2026-07-09', 'csv', 'Research-capacity buildings', 'research/stellar-ai/stellar-ai-director-research-capacity-buildings-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-research-capacity-buildings-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '003f5b666f7074eb25858b82b6c24de5fd61157c50bdc0fcd27c6d808c9b278c', 1484009, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(27, 12, 12, 1, NULL, 'stellar-ai-director-research-capacity-development-2026-07-09', 'csv', 'Research-capacity development', 'research/stellar-ai/stellar-ai-director-research-capacity-development-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-research-capacity-development-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '9fae683cc2449ad0e185e85201aff950b1c7cfd20a4247fb75171c2d3a472f18', 976590, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(28, 12, 12, 1, NULL, 'stellar-ai-director-research-capacity-plan-2026-07-09', 'csv', 'Research-capacity plan', 'research/stellar-ai/stellar-ai-director-research-capacity-plan-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-research-capacity-plan-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '155b0e58f79e5b6968915b7e30e7bccea93d2be2113328473081a8b666e0f783', 50539, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(29, 12, 12, 1, NULL, 'stellar-ai-director-colony-role-targets-2026-07-09', 'csv', 'Colony role targets', 'research/stellar-ai/stellar-ai-director-colony-role-targets-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-colony-role-targets-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '52e7fb929591131468b27d91bb139b76078a0792a0b1b5392ec9035c810e77a1', 145460, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(30, 12, 12, 1, NULL, 'stellar-ai-director-research-capacity-tech-modifiers-2026-07-09', 'csv', 'Research-capacity tech modifiers', 'research/stellar-ai/stellar-ai-director-research-capacity-tech-modifiers-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-research-capacity-tech-modifiers-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', 'dcb27d76e8226f4374c48ec1d3abe410f54538e9494a3dd4d673612f597bcedf', 3024, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(31, 12, 12, 1, NULL, 'stellar-ai-director-build-plan-readiness-2026-07-09', 'csv', 'Build-plan readiness', 'research/stellar-ai/stellar-ai-director-build-plan-readiness-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-build-plan-readiness-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '3c13215c82572aea69517f27eba5bf98ef90de340828c1b58827061386c138d6', 352041, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(32, 12, 12, 1, NULL, 'stellar-ai-director-strategic-benefit-taxonomy-2026-07-09', 'csv', 'Strategic benefit taxonomy', 'research/stellar-ai/stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '2594f6156c6b1460a258af6ca4900f3d0549b7d73112dc25cd2cd26dfa18b660', 764026, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(33, 12, 12, 1, NULL, 'stellar-ai-director-modeling-blocker-accounting-2026-07-09', 'csv', 'Modeling blocker accounting', 'research/stellar-ai/stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '071742b751439384a2d94a0aa64a3c2ecde836a2102b3f794b0cc92945f316ee', 111, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(34, 12, 12, 1, NULL, 'stellar-ai-director-build-plan-consumer-policy-2026-07-09', 'csv', 'Build-plan consumer policy', 'research/stellar-ai/stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv', 'research/stellar-ai/stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', 'generator at snapshot', 'SHA-256', '4f6fe3f3927e491c1ebf06ae522373575f497d140ce893a1f8a0557d913b07f9', 575012, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'available', 'Authoritative external generated dataset.', 1),
(35, 15, 13, 1, NULL, '11-selected-save-evidence', 'markdown', 'Selected observer save evidence', '/mnt/data/11_SELECTED_SAVE_EVIDENCE.md', 'chatgpt_context_bundle/11_SELECTED_SAVE_EVIDENCE.md', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, 'SHA-256', 'fb6d12069c5801ac27fc5782c3401b8b894fb29b9dff7ac05f59895abe81f06a', 4334, 'text/markdown', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', 'Point-in-time bundle artifact.', 1),
(42, 6, 12, 1, NULL, '08-source-file-manifest-and-upload-review', 'markdown', 'Source file manifest and dataset catalog', '/mnt/data/08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW(1).md', 'chatgpt_context_bundle/08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, 'SHA-256', '7be8ac596adb637079ea5b1f2bd864ae15377cc2d7df7a69dfaf85860a307e31', 121619, 'text/markdown', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', 'Point-in-time bundle artifact.', 1),
(47, 6, 12, 1, NULL, '10-stellar-ai-modeling-handoff', 'markdown', 'Stellar AI modeling handoff', '/mnt/data/10_STELLAR_AI_MODELING_HANDOFF(1).md', 'chatgpt_context_bundle/10_STELLAR_AI_MODELING_HANDOFF.md', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, 'SHA-256', 'ba0d3f1f321369054362838bb8f2821c1e966628fce64a9a2558f21f2fd96b36', 5805387, 'text/markdown', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', 'Point-in-time bundle artifact.', 1),
(36, 8, 13, NULL, NULL, 'save:122ac606adf5af27', 'save', 'STAID_WAR_GATE_TEST_Stuck_Ranulia_2239_08_13.sav', 'C:/Users/Admin/AppData/Local/Temp/staid_bundle_save_stage_20260710_1008/STAID_WAR_GATE_TEST_Stuck_Ranulia_2239_08_13.sav', NULL, 2, NULL, 'tools/analyze_stellaris_war_state.py', 'SHA-256', '122ac606adf5af27fea60ece60694a79f9d0593704eb586be35aab270287bb7f', 4282265, 'application/octet-stream', '2026-07-10T12:42:04+00:00', '2026-07-10T10:08:00-04:00', '2026-07-10T12:42:04+00:00', 'available', 'Raw save remains external; identity and selected facts are stored.', 1),
(37, 8, 13, NULL, NULL, 'save:12f9459277ffa4d5', 'save', 'autosave_2239.07.01.sav', 'C:/Users/Admin/AppData/Local/Temp/staid_bundle_save_stage_20260710_1008/autosave_2239.07.01.sav', NULL, 2, NULL, 'tools/analyze_stellaris_war_state.py', 'SHA-256', '12f9459277ffa4d51153ab32c5b8d66004d525c1ec2b312f3f05a027916e1556', 4293306, 'application/octet-stream', '2026-07-10T12:38:02+00:00', '2026-07-10T10:08:00-04:00', '2026-07-10T12:38:02+00:00', 'available', 'Raw save remains external; identity and selected facts are stored.', 1),
(38, 8, 13, NULL, NULL, 'save:884b7f753802ab68', 'save', 'STAID_WAR_GATE_TEST_END_2232_01_01.sav', 'C:/Users/Admin/AppData/Local/Temp/staid_bundle_save_stage_20260710_1008/STAID_WAR_GATE_TEST_END_2232_01_01.sav', NULL, 2, NULL, 'tools/analyze_stellaris_war_state.py', 'SHA-256', '884b7f753802ab68765b9abb269d98565367a8ebc5c841618ae6f7f5ab144c4d', 4131974, 'application/octet-stream', '2026-07-10T12:10:09+00:00', '2026-07-10T10:08:00-04:00', '2026-07-10T12:10:09+00:00', 'available', 'Raw save remains external; identity and selected facts are stored.', 1),
(39, 8, 13, NULL, NULL, 'save:70c29fab43be693e', 'save', 'STAID_WAR_GATE_TEST_START_2232_01_01.sav', 'C:/Users/Admin/AppData/Local/Temp/staid_bundle_save_stage_20260710_1008/STAID_WAR_GATE_TEST_START_2232_01_01.sav', NULL, 2, NULL, 'tools/analyze_stellaris_war_state.py', 'SHA-256', '70c29fab43be693ef7162252fc75890ea2ad76fdf73f1fcffd433ed7fdf55f0a', 4120957, 'application/octet-stream', '2026-07-10T12:08:41+00:00', '2026-07-10T10:08:00-04:00', '2026-07-10T12:08:41+00:00', 'available', 'Raw save remains external; identity and selected facts are stored.', 1),
(40, 5, 1, 1, NULL, 'build_stellar_ai_research_capacity_dataset.py', 'source file', 'Research-capacity generator', 'repository-root/tools/build_stellar_ai_research_capacity_dataset.py', 'tools/build_stellar_ai_research_capacity_dataset.py', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, 'SHA-256', '13ae6b8df79c25ece3fdc71d443931cdf0d58776ff01e1605535edd788fe6a5a', 119970, 'text/x-python', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', NULL, 1),
(41, 5, 1, 1, NULL, 'stellar_ai_director_lib.py', 'source file', 'Stellar AI Director library', 'repository-root/tools/stellar_ai_director_lib.py', 'tools/stellar_ai_director_lib.py', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, 'SHA-256', 'c5a148ac378dd5ab4d2b2b8b418288ed3854d2f6bcbf7d6be0a02108a3a9367b', 597152, 'text/x-python', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', NULL, 1),
(43, 12, 12, 1, NULL, 'benefit-taxonomy-de022d94', 'csv schema snapshot', 'Archived strategic-benefit taxonomy schema', 'research/stellar-ai/archive/de022d94/stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv', NULL, 2, 'de022d94', NULL, NULL, NULL, NULL, 'text/csv', NULL, '2026-07-09T00:00:00Z', NULL, 'archived', 'Ledger records 1,887 rows and 19 columns at this checkpoint.', 1),
(44, 5, 3, 1, 2, 'director-country-type-war-readiness', 'source file', 'Director native war-readiness country type', 'repository-root/mods/StellarAIDirector/common/country_types/zzzzz_staid_18_native_war_readiness.txt', 'mods/StellarAIDirector/common/country_types/zzzzz_staid_18_native_war_readiness.txt', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, NULL, 'text/plain', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', 'Full-object override.', 1),
(45, 1, 2, NULL, 1, 'vanilla-country-types-4.4.5', 'source file', 'Vanilla country types', 'C:/Steam/steamapps/common/Stellaris/common/country_types/00_country_types.txt', NULL, 2, NULL, NULL, NULL, NULL, NULL, 'text/plain', NULL, '2026-07-10T00:00:00Z', NULL, 'available', 'Exact current local file should be rehashed on revalidation.', 1),
(46, 5, 3, 1, 2, 'director-pd-naval-hard-gates', 'source file', 'Director PD naval capacity hard gates', 'repository-root/mods/StellarAIDirector/common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt', 'mods/StellarAIDirector/common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, NULL, 'text/plain', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', 'Full-object override of PD More Arcologies buildings.', 1),
(48, 5, 1, 1, NULL, 'object-atlas-generator-source', 'source file', 'Object-atlas generator', 'repository-root/tools/build_stellar_ai_director_object_atlas.py', 'tools/build_stellar_ai_director_object_atlas.py', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, NULL, 'text/x-python', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', NULL, 1),
(49, 5, 1, 1, NULL, 'war-state-analyzer-source', 'source file', 'War-state analyzer', 'repository-root/tools/analyze_stellaris_war_state.py', 'tools/analyze_stellaris_war_state.py', 2, 'b605aa0e85b5ac68c40a07fdb7c41ece02c365cd', NULL, NULL, NULL, NULL, 'text/x-python', NULL, '2026-07-10T10:06:43-04:00', NULL, 'available', NULL, 1);

INSERT INTO dataset_schema(
    dataset_schema_id, source_artifact_id, schema_key, schema_version, format_code, delimiter, has_header, row_count, column_count, schema_hash_algorithm, schema_hash_value, generated_by_tool_item_id, is_authoritative_external, storage_policy, stable_key_description, notes, created_in_change_set_id
) VALUES
(1, 21, 'object-atlas', '2026-07-06', 'csv', ',', 1, 31211, 24, 'SHA-256', '018e5c29919cfcf9679b312811a6d91ca754f8bae188ae1280c177e1baac6308', 550, 1, 'locator_only', 'Composite keys documented in dataset_key_column.', 'Full external dataset remains authoritative.', 1),
(2, 22, 'dependency-edges', '2026-07-06', 'csv', ',', 1, 34789, 8, 'SHA-256', 'c9b2da047d0d6e2e0812c0f4ef8141079d3e5d012f2b4bbc052181f46de9f465', 550, 1, 'locator_only', 'Composite keys documented in dataset_key_column.', 'Full external dataset remains authoritative.', 1),
(3, 23, 'parent-ai-support', '2026-07-06', 'csv', ',', 1, 31211, 10, 'SHA-256', '1faa1c45634c13e3e9797ee78281a48f7870aa84b7113f219ff40eaf1eaa4d11', 550, 1, 'locator_only', 'Composite keys documented in dataset_key_column.', 'Full external dataset remains authoritative.', 1),
(4, 24, 'policy-matrix', '2026-07-06', 'csv', ',', 1, 8135, 13, 'SHA-256', '719fb9cb5ac72c31c982dd9571d5a46eff78e72f17236660cccd46d04d134379', 550, 1, 'locator_only', 'Composite keys documented in dataset_key_column.', 'Full external dataset remains authoritative.', 1),
(5, 25, 'jobs-v2', '2026-07-09', 'csv', ',', 1, 501, 155, 'SHA-256', 'a3785f9f31bb6181989f60156ba11e53a6c6c1de96ec79468544173df7bd2f8d', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(6, 26, 'buildings-v2', '2026-07-09', 'csv', ',', 1, 826, 282, 'SHA-256', '720e36b2bfe029454fd7a3dace269e190ca8e358ebfe1735fb63ecf2a0ef1ee2', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(7, 27, 'development-v2', '2026-07-09', 'csv', ',', 1, 547, 370, 'SHA-256', '136289ef81867cac1932fb9430a7a7a75a476b1fb870d3f1f669c731d160e1de', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(8, 28, 'research-plan-v2', '2026-07-09', 'csv', ',', 1, 24, 315, 'SHA-256', 'ee47672fa820146cf2aa4e5401afe0f59fd897403753f084cf1ddab48040140b', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(9, 29, 'colony-role-targets-v2', '2026-07-09', 'csv', ',', 1, 247, 78, 'SHA-256', 'ae3cb9fa34126fe26273b7b9fd707800c9e160e4ea07241cf00c9c87d1734671', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(10, 30, 'tech-modifiers-v2', '2026-07-09', 'csv', ',', 1, 18, 9, 'SHA-256', '0fef745d2835e6d31c601b38abd5af720d179e15330ae38bb10b490da8b28659', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(11, 31, 'readiness-v2', '2026-07-09', 'csv', ',', 1, 826, 24, 'SHA-256', 'eb2c8206b998f227f58c1dfe3758889fb2ca05410905c4b68fe6fc8c200345ab', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(12, 32, 'benefit-taxonomy-v2', '2026-07-09', 'csv', ',', 1, 1924, 22, 'SHA-256', 'be24208d91e861e6d64d9a8aa724ff5c2b94c9b04ac746b4c40d5bd3fa9defb3', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(13, 33, 'blocker-accounting-v2', '2026-07-09', 'csv', ',', 1, 0, 9, 'SHA-256', 'd4ef35b6aa82751dc9c548ae82300289ded783ee43ea18e23db5636de9d8b24f', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(14, 34, 'consumer-policy-v2', '2026-07-09', 'csv', ',', 1, 1093, 23, 'SHA-256', 'd9d9e342df5eb5a7c51cd2839dad8999cee66cd4239b1b07598f417a489831ad', 551, 1, 'normalized_facts', 'Stable record key documented below.', 'Complete column layout registered; selected facts normalized.', 1),
(15, 43, 'benefit-taxonomy-v2', 'de022d94', 'csv', ',', 1, 1887, 19, 'SHA-256', '378da8e088b9accb4f062d743b82d1f74cc7d41e2726d52939d656eee9066678', 551, 1, 'locator_only', 'benefit_class + object_type + object_id', 'Archived schema checkpoint for drift demonstration.', 1);

-- Complete column catalogs for the principal current modeling CSVs, plus the core object-atlas datasets.
INSERT INTO dataset_column(
    dataset_column_id, dataset_schema_id, ordinal, column_name, logical_type, semantic_role, dimension_group, metric_key, unit, is_nullable, mapped_item_type_id, mapped_field_item_id, description
) VALUES
(1001, 1, 1, 'object_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1002, 1, 2, 'object_type', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_type''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1003, 1, 3, 'mod_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''mod_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1004, 1, 4, 'mod_name', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''mod_name''. Descriptive or dimensional source value used to interpret the external record.'),
(1005, 1, 5, 'source_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(1006, 1, 6, 'load_winner', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''load_winner''. Descriptive or dimensional source value used to interpret the external record.'),
(1007, 1, 7, 'source_has_ai_weight', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_has_ai_weight''. Descriptive or dimensional source value used to interpret the external record.'),
(1008, 1, 8, 'ai_weight_summary', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''ai_weight_summary''. Descriptive or dimensional source value used to interpret the external record.'),
(1009, 1, 9, 'cost', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''cost''. Descriptive or dimensional source value used to interpret the external record.'),
(1010, 1, 10, 'upkeep', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''upkeep''. Descriptive or dimensional source value used to interpret the external record.'),
(1011, 1, 11, 'produces', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''produces''. Descriptive or dimensional source value used to interpret the external record.'),
(1012, 1, 12, 'prerequisites', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''prerequisites''. Descriptive or dimensional source value used to interpret the external record.'),
(1013, 1, 13, 'potential_allow_gates', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''potential_allow_gates''. Descriptive or dimensional source value used to interpret the external record.'),
(1014, 1, 14, 'event_flags', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''event_flags''. Descriptive or dimensional source value used to interpret the external record.'),
(1015, 1, 15, 'upgrade_from', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''upgrade_from''. Descriptive or dimensional source value used to interpret the external record.'),
(1016, 1, 16, 'upgrades_to', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''upgrades_to''. Descriptive or dimensional source value used to interpret the external record.'),
(1017, 1, 17, 'unlocks', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unlocks''. Descriptive or dimensional source value used to interpret the external record.'),
(1018, 1, 18, 'strategic_role', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''strategic_role''. Descriptive or dimensional source value used to interpret the external record.'),
(1019, 1, 19, 'strategic_tier', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''strategic_tier''. Descriptive or dimensional source value used to interpret the external record.'),
(1020, 1, 20, 'route_ids', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''route_ids''. Descriptive or dimensional source value used to interpret the external record.'),
(1021, 1, 21, 'parent_ai_support', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''parent_ai_support''. Descriptive or dimensional source value used to interpret the external record.'),
(1022, 1, 22, 'policy_status', 'unknown', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''policy_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(1023, 1, 23, 'director_action', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''director_action''. Descriptive or dimensional source value used to interpret the external record.'),
(1024, 1, 24, 'validation_status', 'unknown', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''validation_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(1025, 2, 1, 'source_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1026, 2, 2, 'source_type', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_type''. Descriptive or dimensional source value used to interpret the external record.'),
(1027, 2, 3, 'edge_type', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''edge_type''. Descriptive or dimensional source value used to interpret the external record.'),
(1028, 2, 4, 'target_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''target_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1029, 2, 5, 'target_type', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''target_type''. Descriptive or dimensional source value used to interpret the external record.'),
(1030, 2, 6, 'target_status', 'unknown', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''target_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(1031, 2, 7, 'source_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(1032, 2, 8, 'evidence', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''evidence''. Descriptive or dimensional source value used to interpret the external record.'),
(1033, 3, 1, 'object_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1034, 3, 2, 'object_type', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_type''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1035, 3, 3, 'mod_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''mod_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1036, 3, 4, 'mod_name', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''mod_name''. Descriptive or dimensional source value used to interpret the external record.'),
(1037, 3, 5, 'source_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(1038, 3, 6, 'source_has_ai_weight', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_has_ai_weight''. Descriptive or dimensional source value used to interpret the external record.'),
(1039, 3, 7, 'parent_ai_support', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''parent_ai_support''. Descriptive or dimensional source value used to interpret the external record.'),
(1040, 3, 8, 'strategic_role', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''strategic_role''. Descriptive or dimensional source value used to interpret the external record.'),
(1041, 3, 9, 'route_ids', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''route_ids''. Descriptive or dimensional source value used to interpret the external record.'),
(1042, 3, 10, 'director_requirement', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''director_requirement''. Descriptive or dimensional source value used to interpret the external record.'),
(1043, 4, 1, 'object_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1044, 4, 2, 'object_type', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_type''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1045, 4, 3, 'route_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''route_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1046, 4, 4, 'priority_band', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''priority_band''. Descriptive or dimensional source value used to interpret the external record.'),
(1047, 4, 5, 'timing', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''timing''. Descriptive or dimensional source value used to interpret the external record.'),
(1048, 4, 6, 'empire_context', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''empire_context''. Descriptive or dimensional source value used to interpret the external record.'),
(1049, 4, 7, 'prereq_state', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''prereq_state''. Descriptive or dimensional source value used to interpret the external record.'),
(1050, 4, 8, 'desired_action', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''desired_action''. Descriptive or dimensional source value used to interpret the external record.'),
(1051, 4, 9, 'weight_formula', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''weight_formula''. Descriptive or dimensional source value used to interpret the external record.'),
(1052, 4, 10, 'safety_gates', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''safety_gates''. Descriptive or dimensional source value used to interpret the external record.'),
(1053, 4, 11, 'parent_ai_strategy', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''parent_ai_strategy''. Descriptive or dimensional source value used to interpret the external record.'),
(1054, 4, 12, 'source_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(1055, 4, 13, 'notes', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''notes''. Descriptive or dimensional source value used to interpret the external record.'),
(1056, 5, 1, 'load_position', 'integer', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''load_position''. Descriptive or dimensional source value used to interpret the external record.'),
(1057, 5, 2, 'steam_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''steam_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1058, 5, 3, 'name', 'text', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''name''. Identifies the source mod, file, root, or load position that produced the record.'),
(1059, 5, 4, 'root', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''root''. Identifies the source mod, file, root, or load position that produced the record.'),
(1060, 5, 5, 'job_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1061, 5, 6, 'relative_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''relative_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(1062, 5, 7, 'category', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''category''. Descriptive or dimensional source value used to interpret the external record.'),
(1063, 5, 8, 'subject', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''subject''. Descriptive or dimensional source value used to interpret the external record.'),
(1064, 5, 9, 'base_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1065, 5, 10, 'triggered_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''triggered_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1066, 5, 11, 'optimistic_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1067, 5, 12, 'base_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1068, 5, 13, 'triggered_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''triggered_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1069, 5, 14, 'optimistic_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1070, 5, 15, 'base_research_total', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_research_total''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1071, 5, 16, 'optimistic_research_total', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_research_total''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1072, 5, 17, 'unresolved_variables', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unresolved_variables''. Descriptive or dimensional source value used to interpret the external record.'),
(1073, 5, 18, 'base_output_physics_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_physics_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1074, 5, 19, 'base_output_society_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_society_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1075, 5, 20, 'base_output_engineering_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_engineering_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1076, 5, 21, 'base_output_energy', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_energy''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1077, 5, 22, 'base_output_minerals', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_minerals''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1078, 5, 23, 'base_output_consumer_goods', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_consumer_goods''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1079, 5, 24, 'base_output_alloys', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_alloys''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1080, 5, 25, 'base_output_volatile_motes', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_volatile_motes''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1081, 5, 26, 'base_output_exotic_gases', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_exotic_gases''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1082, 5, 27, 'base_output_rare_crystals', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_rare_crystals''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1083, 5, 28, 'base_output_food', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_food''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1084, 5, 29, 'base_output_unity', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_unity''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1085, 5, 30, 'base_output_influence', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_influence''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1086, 5, 31, 'base_output_trade', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_trade''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1087, 5, 32, 'base_output_trade_value', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_trade_value''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1088, 5, 33, 'base_output_sr_zro', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_zro''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1089, 5, 34, 'base_output_sr_dark_matter', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1090, 5, 35, 'base_output_sr_living_metal', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_living_metal''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1091, 5, 36, 'base_output_nanites', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_nanites''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1092, 5, 37, 'base_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1093, 5, 38, 'base_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1094, 5, 39, 'base_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1095, 5, 40, 'base_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1096, 5, 41, 'triggered_output_physics_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_physics_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1097, 5, 42, 'triggered_output_society_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_society_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1098, 5, 43, 'triggered_output_engineering_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_engineering_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1099, 5, 44, 'triggered_output_energy', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_energy''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1100, 5, 45, 'triggered_output_minerals', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_minerals''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1101, 5, 46, 'triggered_output_consumer_goods', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_consumer_goods''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1102, 5, 47, 'triggered_output_alloys', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_alloys''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1103, 5, 48, 'triggered_output_volatile_motes', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_volatile_motes''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1104, 5, 49, 'triggered_output_exotic_gases', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_exotic_gases''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1105, 5, 50, 'triggered_output_rare_crystals', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_rare_crystals''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1106, 5, 51, 'triggered_output_food', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_food''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1107, 5, 52, 'triggered_output_unity', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_unity''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1108, 5, 53, 'triggered_output_influence', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_influence''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1109, 5, 54, 'triggered_output_trade', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_trade''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1110, 5, 55, 'triggered_output_trade_value', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_trade_value''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1111, 5, 56, 'triggered_output_sr_zro', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_zro''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1112, 5, 57, 'triggered_output_sr_dark_matter', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1113, 5, 58, 'triggered_output_sr_living_metal', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_living_metal''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1114, 5, 59, 'triggered_output_nanites', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_nanites''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1115, 5, 60, 'triggered_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1116, 5, 61, 'triggered_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1117, 5, 62, 'triggered_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1118, 5, 63, 'triggered_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1119, 5, 64, 'optimistic_output_physics_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_physics_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1120, 5, 65, 'optimistic_output_society_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_society_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1121, 5, 66, 'optimistic_output_engineering_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_engineering_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1122, 5, 67, 'optimistic_output_energy', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_energy''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1123, 5, 68, 'optimistic_output_minerals', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_minerals''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1124, 5, 69, 'optimistic_output_consumer_goods', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_consumer_goods''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1125, 5, 70, 'optimistic_output_alloys', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_alloys''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1126, 5, 71, 'optimistic_output_volatile_motes', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_volatile_motes''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1127, 5, 72, 'optimistic_output_exotic_gases', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_exotic_gases''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1128, 5, 73, 'optimistic_output_rare_crystals', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_rare_crystals''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1129, 5, 74, 'optimistic_output_food', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_food''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1130, 5, 75, 'optimistic_output_unity', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_unity''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1131, 5, 76, 'optimistic_output_influence', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_influence''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1132, 5, 77, 'optimistic_output_trade', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_trade''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1133, 5, 78, 'optimistic_output_trade_value', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_trade_value''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1134, 5, 79, 'optimistic_output_sr_zro', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_zro''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1135, 5, 80, 'optimistic_output_sr_dark_matter', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1136, 5, 81, 'optimistic_output_sr_living_metal', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_living_metal''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1137, 5, 82, 'optimistic_output_nanites', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_nanites''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1138, 5, 83, 'optimistic_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1139, 5, 84, 'optimistic_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1140, 5, 85, 'optimistic_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1141, 5, 86, 'optimistic_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1142, 5, 87, 'base_upkeep_physics_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_physics_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1143, 5, 88, 'base_upkeep_society_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_society_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1144, 5, 89, 'base_upkeep_engineering_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1145, 5, 90, 'base_upkeep_energy', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_energy''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1146, 5, 91, 'base_upkeep_minerals', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_minerals''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1147, 5, 92, 'base_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1148, 5, 93, 'base_upkeep_alloys', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_alloys''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1149, 5, 94, 'base_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1150, 5, 95, 'base_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1151, 5, 96, 'base_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1152, 5, 97, 'base_upkeep_food', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_food''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1153, 5, 98, 'base_upkeep_unity', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_unity''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1154, 5, 99, 'base_upkeep_influence', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_influence''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1155, 5, 100, 'base_upkeep_trade', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_trade''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1156, 5, 101, 'base_upkeep_trade_value', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_trade_value''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1157, 5, 102, 'base_upkeep_sr_zro', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1158, 5, 103, 'base_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1159, 5, 104, 'base_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1160, 5, 105, 'base_upkeep_nanites', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_nanites''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1161, 5, 106, 'base_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1162, 5, 107, 'base_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1163, 5, 108, 'base_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1164, 5, 109, 'base_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1165, 5, 110, 'triggered_upkeep_physics_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_physics_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1166, 5, 111, 'triggered_upkeep_society_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_society_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1167, 5, 112, 'triggered_upkeep_engineering_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1168, 5, 113, 'triggered_upkeep_energy', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_energy''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1169, 5, 114, 'triggered_upkeep_minerals', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_minerals''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1170, 5, 115, 'triggered_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1171, 5, 116, 'triggered_upkeep_alloys', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_alloys''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1172, 5, 117, 'triggered_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1173, 5, 118, 'triggered_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1174, 5, 119, 'triggered_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1175, 5, 120, 'triggered_upkeep_food', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_food''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1176, 5, 121, 'triggered_upkeep_unity', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_unity''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1177, 5, 122, 'triggered_upkeep_influence', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_influence''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1178, 5, 123, 'triggered_upkeep_trade', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_trade''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1179, 5, 124, 'triggered_upkeep_trade_value', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_trade_value''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1180, 5, 125, 'triggered_upkeep_sr_zro', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1181, 5, 126, 'triggered_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1182, 5, 127, 'triggered_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1183, 5, 128, 'triggered_upkeep_nanites', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_nanites''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1184, 5, 129, 'triggered_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1185, 5, 130, 'triggered_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1186, 5, 131, 'triggered_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1187, 5, 132, 'triggered_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1188, 5, 133, 'optimistic_upkeep_physics_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_physics_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1189, 5, 134, 'optimistic_upkeep_society_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_society_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1190, 5, 135, 'optimistic_upkeep_engineering_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1191, 5, 136, 'optimistic_upkeep_energy', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_energy''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1192, 5, 137, 'optimistic_upkeep_minerals', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_minerals''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1193, 5, 138, 'optimistic_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1194, 5, 139, 'optimistic_upkeep_alloys', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_alloys''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1195, 5, 140, 'optimistic_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1196, 5, 141, 'optimistic_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1197, 5, 142, 'optimistic_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1198, 5, 143, 'optimistic_upkeep_food', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_food''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1199, 5, 144, 'optimistic_upkeep_unity', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_unity''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1200, 5, 145, 'optimistic_upkeep_influence', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_influence''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1201, 5, 146, 'optimistic_upkeep_trade', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_trade''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1202, 5, 147, 'optimistic_upkeep_trade_value', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_trade_value''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1203, 5, 148, 'optimistic_upkeep_sr_zro', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1204, 5, 149, 'optimistic_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1205, 5, 150, 'optimistic_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1206, 5, 151, 'optimistic_upkeep_nanites', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_nanites''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1207, 5, 152, 'optimistic_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1208, 5, 153, 'optimistic_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1209, 5, 154, 'optimistic_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1210, 5, 155, 'optimistic_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1211, 6, 1, 'building_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''building_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1212, 6, 2, 'colony_class', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''colony_class''. Descriptive or dimensional source value used to interpret the external record.'),
(1213, 6, 3, 'winning_mod_name', 'text', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_mod_name''. Identifies the source mod, file, root, or load position that produced the record.'),
(1214, 6, 4, 'winning_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(1215, 6, 5, 'category', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''category''. Descriptive or dimensional source value used to interpret the external record.'),
(1216, 6, 6, 'prerequisites', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''prerequisites''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1217, 6, 7, 'potential_allow_gates', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''potential_allow_gates''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1218, 6, 8, 'potential_allow_gate_atoms', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''potential_allow_gate_atoms''. Descriptive or dimensional source value used to interpret the external record.'),
(1219, 6, 9, 'event_flags', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''event_flags''. Descriptive or dimensional source value used to interpret the external record.'),
(1220, 6, 10, 'unlock_flags', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unlock_flags''. Descriptive or dimensional source value used to interpret the external record.'),
(1221, 6, 11, 'is_upgrade_terminal', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''is_upgrade_terminal''. Descriptive or dimensional source value used to interpret the external record.'),
(1222, 6, 12, 'upgrade_chain_to_terminal', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''upgrade_chain_to_terminal''. Descriptive or dimensional source value used to interpret the external record.'),
(1223, 6, 13, 'upgrade_terminal', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''upgrade_terminal''. Descriptive or dimensional source value used to interpret the external record.'),
(1224, 6, 14, 'jobs_created_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''jobs_created_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1225, 6, 15, 'raw_job_workforce_total', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''raw_job_workforce_total''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1226, 6, 16, 'job_slots_total', 'real', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_slots_total''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1227, 6, 17, 'unknown_jobs', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unknown_jobs''. Descriptive or dimensional source value used to interpret the external record.'),
(1228, 6, 18, 'source_excluded_jobs', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_excluded_jobs''. Descriptive or dimensional source value used to interpret the external record.'),
(1229, 6, 19, 'job_subject_counts_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_subject_counts_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1230, 6, 20, 'direct_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1231, 6, 21, 'direct_triggered_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_triggered_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1232, 6, 22, 'direct_optimistic_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_optimistic_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1233, 6, 23, 'direct_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1234, 6, 24, 'direct_triggered_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_triggered_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1235, 6, 25, 'direct_optimistic_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_optimistic_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1236, 6, 26, 'job_base_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_base_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1237, 6, 27, 'job_triggered_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_triggered_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1238, 6, 28, 'job_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1239, 6, 29, 'job_base_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_base_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1240, 6, 30, 'job_triggered_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_triggered_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1241, 6, 31, 'job_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1242, 6, 32, 'research_modifier_effects_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''research_modifier_effects_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1243, 6, 33, 'base_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1244, 6, 34, 'triggered_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''triggered_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1245, 6, 35, 'conservative_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1246, 6, 36, 'optimistic_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1247, 6, 37, 'total_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''total_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1248, 6, 38, 'base_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1249, 6, 39, 'triggered_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''triggered_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1250, 6, 40, 'conservative_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1251, 6, 41, 'optimistic_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1252, 6, 42, 'total_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''total_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1253, 6, 43, 'base_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1254, 6, 44, 'triggered_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''triggered_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1255, 6, 45, 'conservative_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1256, 6, 46, 'optimistic_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1257, 6, 47, 'total_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''total_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1258, 6, 48, 'direct_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''direct_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1259, 6, 49, 'job_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''job_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1260, 6, 50, 'modeled_researcher_upkeep_mult', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''modeled_researcher_upkeep_mult''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1261, 6, 51, 'data_quality_flags', 'text', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''data_quality_flags''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(1262, 6, 52, 'unresolved_variables', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unresolved_variables''. Descriptive or dimensional source value used to interpret the external record.'),
(1263, 6, 53, 'base_output_physics_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_physics_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1264, 6, 54, 'base_output_society_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_society_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1265, 6, 55, 'base_output_engineering_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_engineering_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1266, 6, 56, 'base_output_energy', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_energy''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1267, 6, 57, 'base_output_minerals', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_minerals''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1268, 6, 58, 'base_output_consumer_goods', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_consumer_goods''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1269, 6, 59, 'base_output_alloys', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_alloys''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1270, 6, 60, 'base_output_volatile_motes', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_volatile_motes''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1271, 6, 61, 'base_output_exotic_gases', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_exotic_gases''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1272, 6, 62, 'base_output_rare_crystals', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_rare_crystals''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1273, 6, 63, 'base_output_food', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_food''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1274, 6, 64, 'base_output_unity', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_unity''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1275, 6, 65, 'base_output_influence', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_influence''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1276, 6, 66, 'base_output_trade', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_trade''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1277, 6, 67, 'base_output_trade_value', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_trade_value''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1278, 6, 68, 'base_output_sr_zro', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_zro''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1279, 6, 69, 'base_output_sr_dark_matter', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1280, 6, 70, 'base_output_sr_living_metal', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_living_metal''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1281, 6, 71, 'base_output_nanites', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_nanites''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1282, 6, 72, 'base_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1283, 6, 73, 'base_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1284, 6, 74, 'base_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1285, 6, 75, 'base_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1286, 6, 76, 'triggered_output_physics_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_physics_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1287, 6, 77, 'triggered_output_society_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_society_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1288, 6, 78, 'triggered_output_engineering_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_engineering_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1289, 6, 79, 'triggered_output_energy', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_energy''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1290, 6, 80, 'triggered_output_minerals', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_minerals''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1291, 6, 81, 'triggered_output_consumer_goods', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_consumer_goods''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1292, 6, 82, 'triggered_output_alloys', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_alloys''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1293, 6, 83, 'triggered_output_volatile_motes', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_volatile_motes''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1294, 6, 84, 'triggered_output_exotic_gases', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_exotic_gases''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1295, 6, 85, 'triggered_output_rare_crystals', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_rare_crystals''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1296, 6, 86, 'triggered_output_food', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_food''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1297, 6, 87, 'triggered_output_unity', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_unity''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1298, 6, 88, 'triggered_output_influence', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_influence''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1299, 6, 89, 'triggered_output_trade', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_trade''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1300, 6, 90, 'triggered_output_trade_value', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_trade_value''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1301, 6, 91, 'triggered_output_sr_zro', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_zro''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1302, 6, 92, 'triggered_output_sr_dark_matter', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1303, 6, 93, 'triggered_output_sr_living_metal', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_living_metal''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1304, 6, 94, 'triggered_output_nanites', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_nanites''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1305, 6, 95, 'triggered_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1306, 6, 96, 'triggered_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1307, 6, 97, 'triggered_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1308, 6, 98, 'triggered_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1309, 6, 99, 'conservative_output_physics_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_physics_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1310, 6, 100, 'conservative_output_society_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_society_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1311, 6, 101, 'conservative_output_engineering_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_engineering_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1312, 6, 102, 'conservative_output_energy', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_energy''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1313, 6, 103, 'conservative_output_minerals', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_minerals''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1314, 6, 104, 'conservative_output_consumer_goods', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_consumer_goods''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1315, 6, 105, 'conservative_output_alloys', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_alloys''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1316, 6, 106, 'conservative_output_volatile_motes', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_volatile_motes''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1317, 6, 107, 'conservative_output_exotic_gases', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_exotic_gases''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1318, 6, 108, 'conservative_output_rare_crystals', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_rare_crystals''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1319, 6, 109, 'conservative_output_food', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_food''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1320, 6, 110, 'conservative_output_unity', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_unity''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1321, 6, 111, 'conservative_output_influence', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_influence''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1322, 6, 112, 'conservative_output_trade', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_trade''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1323, 6, 113, 'conservative_output_trade_value', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_trade_value''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1324, 6, 114, 'conservative_output_sr_zro', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_zro''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1325, 6, 115, 'conservative_output_sr_dark_matter', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1326, 6, 116, 'conservative_output_sr_living_metal', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_living_metal''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1327, 6, 117, 'conservative_output_nanites', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_nanites''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1328, 6, 118, 'conservative_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1329, 6, 119, 'conservative_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1330, 6, 120, 'conservative_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1331, 6, 121, 'conservative_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1332, 6, 122, 'optimistic_output_physics_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_physics_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1333, 6, 123, 'optimistic_output_society_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_society_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1334, 6, 124, 'optimistic_output_engineering_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_engineering_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1335, 6, 125, 'optimistic_output_energy', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_energy''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1336, 6, 126, 'optimistic_output_minerals', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_minerals''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1337, 6, 127, 'optimistic_output_consumer_goods', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_consumer_goods''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1338, 6, 128, 'optimistic_output_alloys', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_alloys''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1339, 6, 129, 'optimistic_output_volatile_motes', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_volatile_motes''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1340, 6, 130, 'optimistic_output_exotic_gases', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_exotic_gases''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1341, 6, 131, 'optimistic_output_rare_crystals', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_rare_crystals''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1342, 6, 132, 'optimistic_output_food', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_food''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1343, 6, 133, 'optimistic_output_unity', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_unity''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1344, 6, 134, 'optimistic_output_influence', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_influence''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1345, 6, 135, 'optimistic_output_trade', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_trade''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1346, 6, 136, 'optimistic_output_trade_value', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_trade_value''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1347, 6, 137, 'optimistic_output_sr_zro', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_zro''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1348, 6, 138, 'optimistic_output_sr_dark_matter', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1349, 6, 139, 'optimistic_output_sr_living_metal', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_living_metal''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1350, 6, 140, 'optimistic_output_nanites', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_nanites''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1351, 6, 141, 'optimistic_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1352, 6, 142, 'optimistic_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1353, 6, 143, 'optimistic_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1354, 6, 144, 'optimistic_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1355, 6, 145, 'total_output_physics_research', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_physics_research''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1356, 6, 146, 'total_output_society_research', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_society_research''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1357, 6, 147, 'total_output_engineering_research', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_engineering_research''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1358, 6, 148, 'total_output_energy', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_energy''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1359, 6, 149, 'total_output_minerals', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_minerals''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1360, 6, 150, 'total_output_consumer_goods', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_consumer_goods''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1361, 6, 151, 'total_output_alloys', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_alloys''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1362, 6, 152, 'total_output_volatile_motes', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_volatile_motes''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1363, 6, 153, 'total_output_exotic_gases', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_exotic_gases''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1364, 6, 154, 'total_output_rare_crystals', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_rare_crystals''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1365, 6, 155, 'total_output_food', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_food''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1366, 6, 156, 'total_output_unity', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_unity''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1367, 6, 157, 'total_output_influence', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_influence''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1368, 6, 158, 'total_output_trade', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_trade''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1369, 6, 159, 'total_output_trade_value', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_trade_value''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1370, 6, 160, 'total_output_sr_zro', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_sr_zro''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1371, 6, 161, 'total_output_sr_dark_matter', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1372, 6, 162, 'total_output_sr_living_metal', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_sr_living_metal''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1373, 6, 163, 'total_output_nanites', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_nanites''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1374, 6, 164, 'total_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1375, 6, 165, 'total_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1376, 6, 166, 'total_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1377, 6, 167, 'total_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1378, 6, 168, 'base_upkeep_physics_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_physics_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1379, 6, 169, 'base_upkeep_society_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_society_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1380, 6, 170, 'base_upkeep_engineering_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1381, 6, 171, 'base_upkeep_energy', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_energy''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1382, 6, 172, 'base_upkeep_minerals', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_minerals''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1383, 6, 173, 'base_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1384, 6, 174, 'base_upkeep_alloys', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_alloys''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1385, 6, 175, 'base_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1386, 6, 176, 'base_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1387, 6, 177, 'base_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1388, 6, 178, 'base_upkeep_food', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_food''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1389, 6, 179, 'base_upkeep_unity', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_unity''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1390, 6, 180, 'base_upkeep_influence', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_influence''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1391, 6, 181, 'base_upkeep_trade', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_trade''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1392, 6, 182, 'base_upkeep_trade_value', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_trade_value''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1393, 6, 183, 'base_upkeep_sr_zro', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1394, 6, 184, 'base_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1395, 6, 185, 'base_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1396, 6, 186, 'base_upkeep_nanites', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_nanites''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1397, 6, 187, 'base_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1398, 6, 188, 'base_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1399, 6, 189, 'base_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1400, 6, 190, 'base_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1401, 6, 191, 'triggered_upkeep_physics_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_physics_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1402, 6, 192, 'triggered_upkeep_society_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_society_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1403, 6, 193, 'triggered_upkeep_engineering_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1404, 6, 194, 'triggered_upkeep_energy', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_energy''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1405, 6, 195, 'triggered_upkeep_minerals', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_minerals''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1406, 6, 196, 'triggered_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1407, 6, 197, 'triggered_upkeep_alloys', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_alloys''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1408, 6, 198, 'triggered_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1409, 6, 199, 'triggered_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1410, 6, 200, 'triggered_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1411, 6, 201, 'triggered_upkeep_food', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_food''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1412, 6, 202, 'triggered_upkeep_unity', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_unity''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1413, 6, 203, 'triggered_upkeep_influence', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_influence''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1414, 6, 204, 'triggered_upkeep_trade', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_trade''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1415, 6, 205, 'triggered_upkeep_trade_value', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_trade_value''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1416, 6, 206, 'triggered_upkeep_sr_zro', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1417, 6, 207, 'triggered_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1418, 6, 208, 'triggered_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1419, 6, 209, 'triggered_upkeep_nanites', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_nanites''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1420, 6, 210, 'triggered_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1421, 6, 211, 'triggered_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1422, 6, 212, 'triggered_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1423, 6, 213, 'triggered_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1424, 6, 214, 'conservative_upkeep_physics_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_physics_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1425, 6, 215, 'conservative_upkeep_society_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_society_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1426, 6, 216, 'conservative_upkeep_engineering_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1427, 6, 217, 'conservative_upkeep_energy', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_energy''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1428, 6, 218, 'conservative_upkeep_minerals', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_minerals''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1429, 6, 219, 'conservative_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1430, 6, 220, 'conservative_upkeep_alloys', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_alloys''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1431, 6, 221, 'conservative_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1432, 6, 222, 'conservative_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1433, 6, 223, 'conservative_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1434, 6, 224, 'conservative_upkeep_food', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_food''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1435, 6, 225, 'conservative_upkeep_unity', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_unity''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1436, 6, 226, 'conservative_upkeep_influence', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_influence''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1437, 6, 227, 'conservative_upkeep_trade', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_trade''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1438, 6, 228, 'conservative_upkeep_trade_value', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_trade_value''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1439, 6, 229, 'conservative_upkeep_sr_zro', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1440, 6, 230, 'conservative_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1441, 6, 231, 'conservative_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1442, 6, 232, 'conservative_upkeep_nanites', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_nanites''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1443, 6, 233, 'conservative_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1444, 6, 234, 'conservative_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1445, 6, 235, 'conservative_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1446, 6, 236, 'conservative_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1447, 6, 237, 'optimistic_upkeep_physics_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_physics_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1448, 6, 238, 'optimistic_upkeep_society_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_society_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1449, 6, 239, 'optimistic_upkeep_engineering_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1450, 6, 240, 'optimistic_upkeep_energy', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_energy''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1451, 6, 241, 'optimistic_upkeep_minerals', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_minerals''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1452, 6, 242, 'optimistic_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1453, 6, 243, 'optimistic_upkeep_alloys', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_alloys''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1454, 6, 244, 'optimistic_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1455, 6, 245, 'optimistic_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1456, 6, 246, 'optimistic_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1457, 6, 247, 'optimistic_upkeep_food', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_food''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1458, 6, 248, 'optimistic_upkeep_unity', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_unity''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1459, 6, 249, 'optimistic_upkeep_influence', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_influence''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1460, 6, 250, 'optimistic_upkeep_trade', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_trade''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1461, 6, 251, 'optimistic_upkeep_trade_value', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_trade_value''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1462, 6, 252, 'optimistic_upkeep_sr_zro', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1463, 6, 253, 'optimistic_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1464, 6, 254, 'optimistic_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1465, 6, 255, 'optimistic_upkeep_nanites', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_nanites''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1466, 6, 256, 'optimistic_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1467, 6, 257, 'optimistic_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1468, 6, 258, 'optimistic_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1469, 6, 259, 'optimistic_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1470, 6, 260, 'total_upkeep_physics_research', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_physics_research''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1471, 6, 261, 'total_upkeep_society_research', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_society_research''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1472, 6, 262, 'total_upkeep_engineering_research', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1473, 6, 263, 'total_upkeep_energy', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_energy''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1474, 6, 264, 'total_upkeep_minerals', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_minerals''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1475, 6, 265, 'total_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1476, 6, 266, 'total_upkeep_alloys', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_alloys''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1477, 6, 267, 'total_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1478, 6, 268, 'total_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1479, 6, 269, 'total_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1480, 6, 270, 'total_upkeep_food', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_food''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1481, 6, 271, 'total_upkeep_unity', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_unity''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1482, 6, 272, 'total_upkeep_influence', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_influence''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1483, 6, 273, 'total_upkeep_trade', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_trade''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1484, 6, 274, 'total_upkeep_trade_value', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_trade_value''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1485, 6, 275, 'total_upkeep_sr_zro', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1486, 6, 276, 'total_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1487, 6, 277, 'total_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1488, 6, 278, 'total_upkeep_nanites', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_nanites''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1489, 6, 279, 'total_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1490, 6, 280, 'total_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1491, 6, 281, 'total_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1492, 6, 282, 'total_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1493, 7, 1, 'object_type', 'text', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_type''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1494, 7, 2, 'object_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1495, 7, 3, 'colony_class', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''colony_class''. Descriptive or dimensional source value used to interpret the external record.'),
(1496, 7, 4, 'winning_mod_name', 'text', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_mod_name''. Identifies the source mod, file, root, or load position that produced the record.'),
(1497, 7, 5, 'winning_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(1498, 7, 6, 'prerequisites', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''prerequisites''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1499, 7, 7, 'potential_allow_gates', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''potential_allow_gates''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1500, 7, 8, 'potential_allow_gate_atoms', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''potential_allow_gate_atoms''. Descriptive or dimensional source value used to interpret the external record.'),
(1501, 7, 9, 'event_flags', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''event_flags''. Descriptive or dimensional source value used to interpret the external record.'),
(1502, 7, 10, 'unlock_flags', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unlock_flags''. Descriptive or dimensional source value used to interpret the external record.'),
(1503, 7, 11, 'jobs_created_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''jobs_created_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1504, 7, 12, 'raw_job_workforce_total', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''raw_job_workforce_total''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1505, 7, 13, 'job_slots_total', 'real', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_slots_total''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1506, 7, 14, 'unknown_jobs', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unknown_jobs''. Descriptive or dimensional source value used to interpret the external record.'),
(1507, 7, 15, 'source_excluded_jobs', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_excluded_jobs''. Descriptive or dimensional source value used to interpret the external record.'),
(1508, 7, 16, 'direct_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1509, 7, 17, 'direct_triggered_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_triggered_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1510, 7, 18, 'direct_optimistic_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_optimistic_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1511, 7, 19, 'direct_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1512, 7, 20, 'direct_triggered_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_triggered_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1513, 7, 21, 'direct_optimistic_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''direct_optimistic_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1514, 7, 22, 'job_base_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_base_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1515, 7, 23, 'job_triggered_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_triggered_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1516, 7, 24, 'job_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1517, 7, 25, 'job_base_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_base_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1518, 7, 26, 'job_triggered_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_triggered_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1519, 7, 27, 'job_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''job_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1520, 7, 28, 'base_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1521, 7, 29, 'triggered_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''triggered_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1522, 7, 30, 'conservative_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1523, 7, 31, 'optimistic_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1524, 7, 32, 'total_output_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''total_output_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1525, 7, 33, 'base_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1526, 7, 34, 'triggered_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''triggered_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1527, 7, 35, 'conservative_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1528, 7, 36, 'optimistic_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1529, 7, 37, 'total_upkeep_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''total_upkeep_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1530, 7, 38, 'base_net_resources_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_resources_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1531, 7, 39, 'conservative_net_resources_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_resources_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1532, 7, 40, 'optimistic_net_resources_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_resources_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1533, 7, 41, 'net_resources_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''net_resources_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1534, 7, 42, 'base_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1535, 7, 43, 'triggered_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''triggered_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1536, 7, 44, 'conservative_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1537, 7, 45, 'optimistic_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1538, 7, 46, 'total_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''total_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1539, 7, 47, 'net_consumer_goods', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_consumer_goods''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1540, 7, 48, 'net_energy', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_energy''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1541, 7, 49, 'net_minerals', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_minerals''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1542, 7, 50, 'data_quality_flags', 'text', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''data_quality_flags''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(1543, 7, 51, 'unresolved_variables', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unresolved_variables''. Descriptive or dimensional source value used to interpret the external record.'),
(1544, 7, 52, 'base_output_physics_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_physics_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1545, 7, 53, 'base_output_society_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_society_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1546, 7, 54, 'base_output_engineering_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_engineering_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1547, 7, 55, 'base_output_energy', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_energy''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1548, 7, 56, 'base_output_minerals', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_minerals''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1549, 7, 57, 'base_output_consumer_goods', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_consumer_goods''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1550, 7, 58, 'base_output_alloys', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_alloys''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1551, 7, 59, 'base_output_volatile_motes', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_volatile_motes''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1552, 7, 60, 'base_output_exotic_gases', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_exotic_gases''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1553, 7, 61, 'base_output_rare_crystals', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_rare_crystals''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1554, 7, 62, 'base_output_food', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_food''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1555, 7, 63, 'base_output_unity', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_unity''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1556, 7, 64, 'base_output_influence', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_influence''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1557, 7, 65, 'base_output_trade', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_trade''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1558, 7, 66, 'base_output_trade_value', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_trade_value''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1559, 7, 67, 'base_output_sr_zro', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_zro''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1560, 7, 68, 'base_output_sr_dark_matter', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1561, 7, 69, 'base_output_sr_living_metal', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_living_metal''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1562, 7, 70, 'base_output_nanites', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_nanites''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1563, 7, 71, 'base_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1564, 7, 72, 'base_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1565, 7, 73, 'base_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1566, 7, 74, 'base_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1567, 7, 75, 'triggered_output_physics_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_physics_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1568, 7, 76, 'triggered_output_society_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_society_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1569, 7, 77, 'triggered_output_engineering_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_engineering_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1570, 7, 78, 'triggered_output_energy', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_energy''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1571, 7, 79, 'triggered_output_minerals', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_minerals''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1572, 7, 80, 'triggered_output_consumer_goods', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_consumer_goods''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1573, 7, 81, 'triggered_output_alloys', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_alloys''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1574, 7, 82, 'triggered_output_volatile_motes', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_volatile_motes''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1575, 7, 83, 'triggered_output_exotic_gases', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_exotic_gases''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1576, 7, 84, 'triggered_output_rare_crystals', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_rare_crystals''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1577, 7, 85, 'triggered_output_food', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_food''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1578, 7, 86, 'triggered_output_unity', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_unity''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1579, 7, 87, 'triggered_output_influence', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_influence''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1580, 7, 88, 'triggered_output_trade', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_trade''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1581, 7, 89, 'triggered_output_trade_value', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_trade_value''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1582, 7, 90, 'triggered_output_sr_zro', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_zro''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1583, 7, 91, 'triggered_output_sr_dark_matter', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1584, 7, 92, 'triggered_output_sr_living_metal', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_living_metal''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1585, 7, 93, 'triggered_output_nanites', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_nanites''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1586, 7, 94, 'triggered_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1587, 7, 95, 'triggered_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1588, 7, 96, 'triggered_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1589, 7, 97, 'triggered_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1590, 7, 98, 'conservative_output_physics_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_physics_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1591, 7, 99, 'conservative_output_society_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_society_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1592, 7, 100, 'conservative_output_engineering_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_engineering_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1593, 7, 101, 'conservative_output_energy', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_energy''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1594, 7, 102, 'conservative_output_minerals', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_minerals''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1595, 7, 103, 'conservative_output_consumer_goods', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_consumer_goods''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1596, 7, 104, 'conservative_output_alloys', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_alloys''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1597, 7, 105, 'conservative_output_volatile_motes', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_volatile_motes''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1598, 7, 106, 'conservative_output_exotic_gases', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_exotic_gases''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1599, 7, 107, 'conservative_output_rare_crystals', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_rare_crystals''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1600, 7, 108, 'conservative_output_food', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_food''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1601, 7, 109, 'conservative_output_unity', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_unity''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1602, 7, 110, 'conservative_output_influence', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_influence''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1603, 7, 111, 'conservative_output_trade', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_trade''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1604, 7, 112, 'conservative_output_trade_value', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_trade_value''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1605, 7, 113, 'conservative_output_sr_zro', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_zro''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1606, 7, 114, 'conservative_output_sr_dark_matter', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1607, 7, 115, 'conservative_output_sr_living_metal', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_living_metal''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1608, 7, 116, 'conservative_output_nanites', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_nanites''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1609, 7, 117, 'conservative_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1610, 7, 118, 'conservative_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1611, 7, 119, 'conservative_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1612, 7, 120, 'conservative_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1613, 7, 121, 'optimistic_output_physics_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_physics_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1614, 7, 122, 'optimistic_output_society_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_society_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1615, 7, 123, 'optimistic_output_engineering_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_engineering_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1616, 7, 124, 'optimistic_output_energy', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_energy''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1617, 7, 125, 'optimistic_output_minerals', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_minerals''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1618, 7, 126, 'optimistic_output_consumer_goods', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_consumer_goods''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1619, 7, 127, 'optimistic_output_alloys', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_alloys''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1620, 7, 128, 'optimistic_output_volatile_motes', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_volatile_motes''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1621, 7, 129, 'optimistic_output_exotic_gases', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_exotic_gases''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1622, 7, 130, 'optimistic_output_rare_crystals', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_rare_crystals''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1623, 7, 131, 'optimistic_output_food', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_food''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1624, 7, 132, 'optimistic_output_unity', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_unity''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1625, 7, 133, 'optimistic_output_influence', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_influence''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1626, 7, 134, 'optimistic_output_trade', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_trade''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1627, 7, 135, 'optimistic_output_trade_value', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_trade_value''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1628, 7, 136, 'optimistic_output_sr_zro', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_zro''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1629, 7, 137, 'optimistic_output_sr_dark_matter', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1630, 7, 138, 'optimistic_output_sr_living_metal', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_living_metal''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1631, 7, 139, 'optimistic_output_nanites', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_nanites''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1632, 7, 140, 'optimistic_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1633, 7, 141, 'optimistic_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1634, 7, 142, 'optimistic_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1635, 7, 143, 'optimistic_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1636, 7, 144, 'total_output_physics_research', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_physics_research''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1637, 7, 145, 'total_output_society_research', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_society_research''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1638, 7, 146, 'total_output_engineering_research', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_engineering_research''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1639, 7, 147, 'total_output_energy', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_energy''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1640, 7, 148, 'total_output_minerals', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_minerals''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1641, 7, 149, 'total_output_consumer_goods', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_consumer_goods''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1642, 7, 150, 'total_output_alloys', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_alloys''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1643, 7, 151, 'total_output_volatile_motes', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_volatile_motes''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1644, 7, 152, 'total_output_exotic_gases', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_exotic_gases''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1645, 7, 153, 'total_output_rare_crystals', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_rare_crystals''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1646, 7, 154, 'total_output_food', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_food''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1647, 7, 155, 'total_output_unity', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_unity''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1648, 7, 156, 'total_output_influence', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_influence''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1649, 7, 157, 'total_output_trade', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_trade''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1650, 7, 158, 'total_output_trade_value', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_trade_value''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1651, 7, 159, 'total_output_sr_zro', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_sr_zro''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1652, 7, 160, 'total_output_sr_dark_matter', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1653, 7, 161, 'total_output_sr_living_metal', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_sr_living_metal''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1654, 7, 162, 'total_output_nanites', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_nanites''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1655, 7, 163, 'total_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1656, 7, 164, 'total_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1657, 7, 165, 'total_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1658, 7, 166, 'total_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:total:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:total:output; normalize selected facts through analysis_metric/analysis_value.'),
(1659, 7, 167, 'base_upkeep_physics_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_physics_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1660, 7, 168, 'base_upkeep_society_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_society_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1661, 7, 169, 'base_upkeep_engineering_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1662, 7, 170, 'base_upkeep_energy', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_energy''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1663, 7, 171, 'base_upkeep_minerals', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_minerals''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1664, 7, 172, 'base_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1665, 7, 173, 'base_upkeep_alloys', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_alloys''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1666, 7, 174, 'base_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1667, 7, 175, 'base_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1668, 7, 176, 'base_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1669, 7, 177, 'base_upkeep_food', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_food''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1670, 7, 178, 'base_upkeep_unity', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_unity''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1671, 7, 179, 'base_upkeep_influence', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_influence''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1672, 7, 180, 'base_upkeep_trade', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_trade''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1673, 7, 181, 'base_upkeep_trade_value', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_trade_value''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1674, 7, 182, 'base_upkeep_sr_zro', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1675, 7, 183, 'base_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1676, 7, 184, 'base_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1677, 7, 185, 'base_upkeep_nanites', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_nanites''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1678, 7, 186, 'base_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1679, 7, 187, 'base_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1680, 7, 188, 'base_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1681, 7, 189, 'base_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1682, 7, 190, 'triggered_upkeep_physics_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_physics_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1683, 7, 191, 'triggered_upkeep_society_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_society_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1684, 7, 192, 'triggered_upkeep_engineering_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1685, 7, 193, 'triggered_upkeep_energy', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_energy''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1686, 7, 194, 'triggered_upkeep_minerals', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_minerals''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1687, 7, 195, 'triggered_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1688, 7, 196, 'triggered_upkeep_alloys', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_alloys''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1689, 7, 197, 'triggered_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1690, 7, 198, 'triggered_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1691, 7, 199, 'triggered_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1692, 7, 200, 'triggered_upkeep_food', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_food''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1693, 7, 201, 'triggered_upkeep_unity', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_unity''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1694, 7, 202, 'triggered_upkeep_influence', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_influence''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1695, 7, 203, 'triggered_upkeep_trade', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_trade''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1696, 7, 204, 'triggered_upkeep_trade_value', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_trade_value''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1697, 7, 205, 'triggered_upkeep_sr_zro', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1698, 7, 206, 'triggered_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1699, 7, 207, 'triggered_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1700, 7, 208, 'triggered_upkeep_nanites', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_nanites''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1701, 7, 209, 'triggered_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1702, 7, 210, 'triggered_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1703, 7, 211, 'triggered_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1704, 7, 212, 'triggered_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1705, 7, 213, 'conservative_upkeep_physics_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_physics_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1706, 7, 214, 'conservative_upkeep_society_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_society_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1707, 7, 215, 'conservative_upkeep_engineering_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1708, 7, 216, 'conservative_upkeep_energy', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_energy''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1709, 7, 217, 'conservative_upkeep_minerals', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_minerals''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1710, 7, 218, 'conservative_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1711, 7, 219, 'conservative_upkeep_alloys', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_alloys''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1712, 7, 220, 'conservative_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1713, 7, 221, 'conservative_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1714, 7, 222, 'conservative_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1715, 7, 223, 'conservative_upkeep_food', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_food''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1716, 7, 224, 'conservative_upkeep_unity', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_unity''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1717, 7, 225, 'conservative_upkeep_influence', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_influence''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1718, 7, 226, 'conservative_upkeep_trade', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_trade''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1719, 7, 227, 'conservative_upkeep_trade_value', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_trade_value''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1720, 7, 228, 'conservative_upkeep_sr_zro', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1721, 7, 229, 'conservative_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1722, 7, 230, 'conservative_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1723, 7, 231, 'conservative_upkeep_nanites', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_nanites''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1724, 7, 232, 'conservative_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1725, 7, 233, 'conservative_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1726, 7, 234, 'conservative_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1727, 7, 235, 'conservative_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1728, 7, 236, 'optimistic_upkeep_physics_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_physics_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1729, 7, 237, 'optimistic_upkeep_society_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_society_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1730, 7, 238, 'optimistic_upkeep_engineering_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1731, 7, 239, 'optimistic_upkeep_energy', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_energy''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1732, 7, 240, 'optimistic_upkeep_minerals', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_minerals''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1733, 7, 241, 'optimistic_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1734, 7, 242, 'optimistic_upkeep_alloys', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_alloys''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1735, 7, 243, 'optimistic_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1736, 7, 244, 'optimistic_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1737, 7, 245, 'optimistic_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1738, 7, 246, 'optimistic_upkeep_food', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_food''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1739, 7, 247, 'optimistic_upkeep_unity', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_unity''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1740, 7, 248, 'optimistic_upkeep_influence', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_influence''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1741, 7, 249, 'optimistic_upkeep_trade', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_trade''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1742, 7, 250, 'optimistic_upkeep_trade_value', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_trade_value''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1743, 7, 251, 'optimistic_upkeep_sr_zro', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1744, 7, 252, 'optimistic_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1745, 7, 253, 'optimistic_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1746, 7, 254, 'optimistic_upkeep_nanites', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_nanites''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1747, 7, 255, 'optimistic_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1748, 7, 256, 'optimistic_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1749, 7, 257, 'optimistic_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1750, 7, 258, 'optimistic_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1751, 7, 259, 'total_upkeep_physics_research', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_physics_research''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1752, 7, 260, 'total_upkeep_society_research', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_society_research''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1753, 7, 261, 'total_upkeep_engineering_research', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1754, 7, 262, 'total_upkeep_energy', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_energy''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1755, 7, 263, 'total_upkeep_minerals', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_minerals''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1756, 7, 264, 'total_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1757, 7, 265, 'total_upkeep_alloys', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_alloys''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1758, 7, 266, 'total_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1759, 7, 267, 'total_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1760, 7, 268, 'total_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1761, 7, 269, 'total_upkeep_food', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_food''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1762, 7, 270, 'total_upkeep_unity', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_unity''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1763, 7, 271, 'total_upkeep_influence', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_influence''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1764, 7, 272, 'total_upkeep_trade', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_trade''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1765, 7, 273, 'total_upkeep_trade_value', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_trade_value''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1766, 7, 274, 'total_upkeep_sr_zro', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1767, 7, 275, 'total_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1768, 7, 276, 'total_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1769, 7, 277, 'total_upkeep_nanites', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_nanites''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1770, 7, 278, 'total_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1771, 7, 279, 'total_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1772, 7, 280, 'total_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1773, 7, 281, 'total_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:total:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''total_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:total:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1774, 7, 282, 'base_net_physics_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_net_physics_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1775, 7, 283, 'base_net_society_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_net_society_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1776, 7, 284, 'base_net_engineering_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_net_engineering_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1777, 7, 285, 'base_net_energy', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_energy''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1778, 7, 286, 'base_net_minerals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_minerals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1779, 7, 287, 'base_net_consumer_goods', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_consumer_goods''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1780, 7, 288, 'base_net_alloys', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_alloys''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1781, 7, 289, 'base_net_volatile_motes', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_volatile_motes''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1782, 7, 290, 'base_net_exotic_gases', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_exotic_gases''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1783, 7, 291, 'base_net_rare_crystals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_rare_crystals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1784, 7, 292, 'base_net_food', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_food''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1785, 7, 293, 'base_net_unity', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_unity''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1786, 7, 294, 'base_net_influence', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_influence''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1787, 7, 295, 'base_net_trade', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_trade''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1788, 7, 296, 'base_net_trade_value', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_trade_value''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1789, 7, 297, 'base_net_sr_zro', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_sr_zro''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1790, 7, 298, 'base_net_sr_dark_matter', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_sr_dark_matter''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1791, 7, 299, 'base_net_sr_living_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_sr_living_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1792, 7, 300, 'base_net_nanites', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_nanites''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1793, 7, 301, 'base_net_giga_sr_negative_mass', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_giga_sr_negative_mass''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1794, 7, 302, 'base_net_giga_sr_amb_megaconstruction', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_giga_sr_amb_megaconstruction''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1795, 7, 303, 'base_net_giga_sr_iodizium', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_giga_sr_iodizium''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1796, 7, 304, 'base_net_giga_sr_sentient_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_giga_sr_sentient_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1797, 7, 305, 'conservative_net_physics_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_net_physics_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1798, 7, 306, 'conservative_net_society_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_net_society_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1799, 7, 307, 'conservative_net_engineering_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_net_engineering_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1800, 7, 308, 'conservative_net_energy', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_energy''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1801, 7, 309, 'conservative_net_minerals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_minerals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1802, 7, 310, 'conservative_net_consumer_goods', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_consumer_goods''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1803, 7, 311, 'conservative_net_alloys', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_alloys''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1804, 7, 312, 'conservative_net_volatile_motes', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_volatile_motes''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1805, 7, 313, 'conservative_net_exotic_gases', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_exotic_gases''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1806, 7, 314, 'conservative_net_rare_crystals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_rare_crystals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1807, 7, 315, 'conservative_net_food', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_food''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1808, 7, 316, 'conservative_net_unity', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_unity''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1809, 7, 317, 'conservative_net_influence', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_influence''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1810, 7, 318, 'conservative_net_trade', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_trade''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1811, 7, 319, 'conservative_net_trade_value', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_trade_value''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1812, 7, 320, 'conservative_net_sr_zro', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_sr_zro''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1813, 7, 321, 'conservative_net_sr_dark_matter', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_sr_dark_matter''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1814, 7, 322, 'conservative_net_sr_living_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_sr_living_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1815, 7, 323, 'conservative_net_nanites', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_nanites''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1816, 7, 324, 'conservative_net_giga_sr_negative_mass', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_giga_sr_negative_mass''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1817, 7, 325, 'conservative_net_giga_sr_amb_megaconstruction', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_giga_sr_amb_megaconstruction''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1818, 7, 326, 'conservative_net_giga_sr_iodizium', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_giga_sr_iodizium''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1819, 7, 327, 'conservative_net_giga_sr_sentient_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_giga_sr_sentient_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1820, 7, 328, 'optimistic_net_physics_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_net_physics_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1821, 7, 329, 'optimistic_net_society_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_net_society_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1822, 7, 330, 'optimistic_net_engineering_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_net_engineering_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1823, 7, 331, 'optimistic_net_energy', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_energy''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1824, 7, 332, 'optimistic_net_minerals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_minerals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1825, 7, 333, 'optimistic_net_consumer_goods', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_consumer_goods''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1826, 7, 334, 'optimistic_net_alloys', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_alloys''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1827, 7, 335, 'optimistic_net_volatile_motes', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_volatile_motes''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1828, 7, 336, 'optimistic_net_exotic_gases', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_exotic_gases''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1829, 7, 337, 'optimistic_net_rare_crystals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_rare_crystals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1830, 7, 338, 'optimistic_net_food', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_food''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1831, 7, 339, 'optimistic_net_unity', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_unity''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1832, 7, 340, 'optimistic_net_influence', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_influence''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1833, 7, 341, 'optimistic_net_trade', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_trade''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1834, 7, 342, 'optimistic_net_trade_value', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_trade_value''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1835, 7, 343, 'optimistic_net_sr_zro', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_sr_zro''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1836, 7, 344, 'optimistic_net_sr_dark_matter', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_sr_dark_matter''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1837, 7, 345, 'optimistic_net_sr_living_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_sr_living_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1838, 7, 346, 'optimistic_net_nanites', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_nanites''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1839, 7, 347, 'optimistic_net_giga_sr_negative_mass', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_giga_sr_negative_mass''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1840, 7, 348, 'optimistic_net_giga_sr_amb_megaconstruction', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_giga_sr_amb_megaconstruction''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1841, 7, 349, 'optimistic_net_giga_sr_iodizium', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_giga_sr_iodizium''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1842, 7, 350, 'optimistic_net_giga_sr_sentient_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_giga_sr_sentient_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1843, 7, 351, 'net_physics_research', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_physics_research''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1844, 7, 352, 'net_society_research', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_society_research''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1845, 7, 353, 'net_engineering_research', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_engineering_research''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1846, 7, 354, 'net_alloys', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_alloys''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1847, 7, 355, 'net_volatile_motes', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_volatile_motes''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1848, 7, 356, 'net_exotic_gases', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_exotic_gases''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1849, 7, 357, 'net_rare_crystals', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_rare_crystals''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1850, 7, 358, 'net_food', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_food''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1851, 7, 359, 'net_unity', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_unity''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1852, 7, 360, 'net_influence', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_influence''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1853, 7, 361, 'net_trade', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_trade''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1854, 7, 362, 'net_trade_value', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_trade_value''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1855, 7, 363, 'net_sr_zro', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_sr_zro''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1856, 7, 364, 'net_sr_dark_matter', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_sr_dark_matter''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1857, 7, 365, 'net_sr_living_metal', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_sr_living_metal''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1858, 7, 366, 'net_nanites', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_nanites''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1859, 7, 367, 'net_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1860, 7, 368, 'net_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1861, 7, 369, 'net_giga_sr_iodizium', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1862, 7, 370, 'net_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(1863, 8, 1, 'scenario', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''scenario''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(1864, 8, 2, 'building_slots', 'integer', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''building_slots''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1865, 8, 3, 'selected_buildings', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''selected_buildings''. Descriptive or dimensional source value used to interpret the external record.'),
(1866, 8, 4, 'research_per_full_colony', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''research_per_full_colony''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1867, 8, 5, 'base_research_per_full_colony', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_research_per_full_colony''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1868, 8, 6, 'conservative_research_per_full_colony', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_research_per_full_colony''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1869, 8, 7, 'optimistic_research_per_full_colony', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_research_per_full_colony''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1870, 8, 8, 'adjusted_research_per_full_colony', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''adjusted_research_per_full_colony''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1871, 8, 9, 'colonies_for_3000_research', 'integer', 'count', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''colonies_for_3000_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1872, 8, 10, 'colonies_for_3000_base_research', 'integer', 'count', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''colonies_for_3000_base_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1873, 8, 11, 'colonies_for_3000_conservative_research', 'integer', 'count', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''colonies_for_3000_conservative_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1874, 8, 12, 'colonies_for_3000_optimistic_research', 'integer', 'count', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''colonies_for_3000_optimistic_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1875, 8, 13, 'colonies_for_3000_adjusted_research', 'integer', 'count', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''colonies_for_3000_adjusted_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1876, 8, 14, 'modeled_researcher_upkeep_mult', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''modeled_researcher_upkeep_mult''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1877, 8, 15, 'modifier_keys_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''modifier_keys_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(1878, 8, 16, 'unused_slots', 'integer', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unused_slots''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(1879, 8, 17, 'base_output_physics_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_physics_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1880, 8, 18, 'base_output_society_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_society_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1881, 8, 19, 'base_output_engineering_research', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_engineering_research''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1882, 8, 20, 'base_output_energy', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_energy''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1883, 8, 21, 'base_output_minerals', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_minerals''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1884, 8, 22, 'base_output_consumer_goods', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_consumer_goods''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1885, 8, 23, 'base_output_alloys', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_alloys''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1886, 8, 24, 'base_output_volatile_motes', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_volatile_motes''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1887, 8, 25, 'base_output_exotic_gases', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_exotic_gases''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1888, 8, 26, 'base_output_rare_crystals', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_rare_crystals''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1889, 8, 27, 'base_output_food', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_food''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1890, 8, 28, 'base_output_unity', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_unity''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1891, 8, 29, 'base_output_influence', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_influence''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1892, 8, 30, 'base_output_trade', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_trade''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1893, 8, 31, 'base_output_trade_value', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_trade_value''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1894, 8, 32, 'base_output_sr_zro', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_zro''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1895, 8, 33, 'base_output_sr_dark_matter', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1896, 8, 34, 'base_output_sr_living_metal', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_sr_living_metal''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1897, 8, 35, 'base_output_nanites', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_nanites''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1898, 8, 36, 'base_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1899, 8, 37, 'base_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1900, 8, 38, 'base_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1901, 8, 39, 'base_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:base:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:base:output; normalize selected facts through analysis_metric/analysis_value.'),
(1902, 8, 40, 'triggered_output_physics_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_physics_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1903, 8, 41, 'triggered_output_society_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_society_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1904, 8, 42, 'triggered_output_engineering_research', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_engineering_research''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1905, 8, 43, 'triggered_output_energy', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_energy''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1906, 8, 44, 'triggered_output_minerals', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_minerals''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1907, 8, 45, 'triggered_output_consumer_goods', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_consumer_goods''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1908, 8, 46, 'triggered_output_alloys', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_alloys''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1909, 8, 47, 'triggered_output_volatile_motes', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_volatile_motes''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1910, 8, 48, 'triggered_output_exotic_gases', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_exotic_gases''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1911, 8, 49, 'triggered_output_rare_crystals', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_rare_crystals''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1912, 8, 50, 'triggered_output_food', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_food''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1913, 8, 51, 'triggered_output_unity', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_unity''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1914, 8, 52, 'triggered_output_influence', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_influence''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1915, 8, 53, 'triggered_output_trade', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_trade''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1916, 8, 54, 'triggered_output_trade_value', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_trade_value''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1917, 8, 55, 'triggered_output_sr_zro', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_zro''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1918, 8, 56, 'triggered_output_sr_dark_matter', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1919, 8, 57, 'triggered_output_sr_living_metal', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_sr_living_metal''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1920, 8, 58, 'triggered_output_nanites', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_nanites''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1921, 8, 59, 'triggered_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1922, 8, 60, 'triggered_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1923, 8, 61, 'triggered_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1924, 8, 62, 'triggered_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:triggered:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:triggered:output; normalize selected facts through analysis_metric/analysis_value.'),
(1925, 8, 63, 'conservative_output_physics_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_physics_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1926, 8, 64, 'conservative_output_society_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_society_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1927, 8, 65, 'conservative_output_engineering_research', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_engineering_research''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1928, 8, 66, 'conservative_output_energy', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_energy''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1929, 8, 67, 'conservative_output_minerals', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_minerals''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1930, 8, 68, 'conservative_output_consumer_goods', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_consumer_goods''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1931, 8, 69, 'conservative_output_alloys', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_alloys''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1932, 8, 70, 'conservative_output_volatile_motes', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_volatile_motes''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1933, 8, 71, 'conservative_output_exotic_gases', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_exotic_gases''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1934, 8, 72, 'conservative_output_rare_crystals', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_rare_crystals''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1935, 8, 73, 'conservative_output_food', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_food''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1936, 8, 74, 'conservative_output_unity', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_unity''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1937, 8, 75, 'conservative_output_influence', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_influence''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1938, 8, 76, 'conservative_output_trade', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_trade''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1939, 8, 77, 'conservative_output_trade_value', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_trade_value''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1940, 8, 78, 'conservative_output_sr_zro', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_zro''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1941, 8, 79, 'conservative_output_sr_dark_matter', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1942, 8, 80, 'conservative_output_sr_living_metal', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_sr_living_metal''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1943, 8, 81, 'conservative_output_nanites', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_nanites''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1944, 8, 82, 'conservative_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1945, 8, 83, 'conservative_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1946, 8, 84, 'conservative_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1947, 8, 85, 'conservative_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:conservative:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:conservative:output; normalize selected facts through analysis_metric/analysis_value.'),
(1948, 8, 86, 'optimistic_output_physics_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_physics_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1949, 8, 87, 'optimistic_output_society_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_society_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1950, 8, 88, 'optimistic_output_engineering_research', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_engineering_research''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1951, 8, 89, 'optimistic_output_energy', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_energy''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1952, 8, 90, 'optimistic_output_minerals', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_minerals''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1953, 8, 91, 'optimistic_output_consumer_goods', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_consumer_goods''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1954, 8, 92, 'optimistic_output_alloys', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_alloys''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1955, 8, 93, 'optimistic_output_volatile_motes', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_volatile_motes''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1956, 8, 94, 'optimistic_output_exotic_gases', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_exotic_gases''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1957, 8, 95, 'optimistic_output_rare_crystals', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_rare_crystals''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1958, 8, 96, 'optimistic_output_food', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_food''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1959, 8, 97, 'optimistic_output_unity', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_unity''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1960, 8, 98, 'optimistic_output_influence', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_influence''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1961, 8, 99, 'optimistic_output_trade', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_trade''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1962, 8, 100, 'optimistic_output_trade_value', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_trade_value''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1963, 8, 101, 'optimistic_output_sr_zro', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_zro''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1964, 8, 102, 'optimistic_output_sr_dark_matter', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1965, 8, 103, 'optimistic_output_sr_living_metal', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_sr_living_metal''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1966, 8, 104, 'optimistic_output_nanites', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_nanites''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1967, 8, 105, 'optimistic_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1968, 8, 106, 'optimistic_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1969, 8, 107, 'optimistic_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1970, 8, 108, 'optimistic_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:optimistic:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:optimistic:output; normalize selected facts through analysis_metric/analysis_value.'),
(1971, 8, 109, 'adjusted_output_physics_research', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_physics_research''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1972, 8, 110, 'adjusted_output_society_research', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_society_research''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1973, 8, 111, 'adjusted_output_engineering_research', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_engineering_research''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1974, 8, 112, 'adjusted_output_energy', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_energy''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1975, 8, 113, 'adjusted_output_minerals', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_minerals''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1976, 8, 114, 'adjusted_output_consumer_goods', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_consumer_goods''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1977, 8, 115, 'adjusted_output_alloys', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_alloys''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1978, 8, 116, 'adjusted_output_volatile_motes', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_volatile_motes''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1979, 8, 117, 'adjusted_output_exotic_gases', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_exotic_gases''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1980, 8, 118, 'adjusted_output_rare_crystals', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_rare_crystals''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1981, 8, 119, 'adjusted_output_food', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_food''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1982, 8, 120, 'adjusted_output_unity', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_unity''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1983, 8, 121, 'adjusted_output_influence', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_influence''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1984, 8, 122, 'adjusted_output_trade', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_trade''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1985, 8, 123, 'adjusted_output_trade_value', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_trade_value''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1986, 8, 124, 'adjusted_output_sr_zro', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_sr_zro''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1987, 8, 125, 'adjusted_output_sr_dark_matter', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_sr_dark_matter''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1988, 8, 126, 'adjusted_output_sr_living_metal', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_sr_living_metal''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1989, 8, 127, 'adjusted_output_nanites', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_nanites''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1990, 8, 128, 'adjusted_output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1991, 8, 129, 'adjusted_output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1992, 8, 130, 'adjusted_output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1993, 8, 131, 'adjusted_output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:adjusted:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:adjusted:output; normalize selected facts through analysis_metric/analysis_value.'),
(1994, 8, 132, 'base_upkeep_physics_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_physics_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1995, 8, 133, 'base_upkeep_society_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_society_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1996, 8, 134, 'base_upkeep_engineering_research', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1997, 8, 135, 'base_upkeep_energy', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_energy''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1998, 8, 136, 'base_upkeep_minerals', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_minerals''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(1999, 8, 137, 'base_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2000, 8, 138, 'base_upkeep_alloys', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_alloys''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2001, 8, 139, 'base_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2002, 8, 140, 'base_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2003, 8, 141, 'base_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2004, 8, 142, 'base_upkeep_food', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_food''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2005, 8, 143, 'base_upkeep_unity', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_unity''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2006, 8, 144, 'base_upkeep_influence', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_influence''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2007, 8, 145, 'base_upkeep_trade', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_trade''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2008, 8, 146, 'base_upkeep_trade_value', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_trade_value''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2009, 8, 147, 'base_upkeep_sr_zro', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2010, 8, 148, 'base_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2011, 8, 149, 'base_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2012, 8, 150, 'base_upkeep_nanites', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_nanites''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2013, 8, 151, 'base_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2014, 8, 152, 'base_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2015, 8, 153, 'base_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2016, 8, 154, 'base_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:base:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''base_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:base:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2017, 8, 155, 'triggered_upkeep_physics_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_physics_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2018, 8, 156, 'triggered_upkeep_society_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_society_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2019, 8, 157, 'triggered_upkeep_engineering_research', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2020, 8, 158, 'triggered_upkeep_energy', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_energy''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2021, 8, 159, 'triggered_upkeep_minerals', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_minerals''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2022, 8, 160, 'triggered_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2023, 8, 161, 'triggered_upkeep_alloys', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_alloys''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2024, 8, 162, 'triggered_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2025, 8, 163, 'triggered_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2026, 8, 164, 'triggered_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2027, 8, 165, 'triggered_upkeep_food', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_food''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2028, 8, 166, 'triggered_upkeep_unity', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_unity''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2029, 8, 167, 'triggered_upkeep_influence', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_influence''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2030, 8, 168, 'triggered_upkeep_trade', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_trade''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2031, 8, 169, 'triggered_upkeep_trade_value', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_trade_value''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2032, 8, 170, 'triggered_upkeep_sr_zro', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2033, 8, 171, 'triggered_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2034, 8, 172, 'triggered_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2035, 8, 173, 'triggered_upkeep_nanites', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_nanites''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2036, 8, 174, 'triggered_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2037, 8, 175, 'triggered_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2038, 8, 176, 'triggered_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2039, 8, 177, 'triggered_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:triggered:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''triggered_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:triggered:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2040, 8, 178, 'conservative_upkeep_physics_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_physics_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2041, 8, 179, 'conservative_upkeep_society_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_society_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2042, 8, 180, 'conservative_upkeep_engineering_research', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2043, 8, 181, 'conservative_upkeep_energy', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_energy''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2044, 8, 182, 'conservative_upkeep_minerals', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_minerals''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2045, 8, 183, 'conservative_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2046, 8, 184, 'conservative_upkeep_alloys', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_alloys''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2047, 8, 185, 'conservative_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2048, 8, 186, 'conservative_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2049, 8, 187, 'conservative_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2050, 8, 188, 'conservative_upkeep_food', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_food''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2051, 8, 189, 'conservative_upkeep_unity', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_unity''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2052, 8, 190, 'conservative_upkeep_influence', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_influence''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2053, 8, 191, 'conservative_upkeep_trade', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_trade''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2054, 8, 192, 'conservative_upkeep_trade_value', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_trade_value''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2055, 8, 193, 'conservative_upkeep_sr_zro', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2056, 8, 194, 'conservative_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2057, 8, 195, 'conservative_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2058, 8, 196, 'conservative_upkeep_nanites', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_nanites''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2059, 8, 197, 'conservative_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2060, 8, 198, 'conservative_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2061, 8, 199, 'conservative_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2062, 8, 200, 'conservative_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:conservative:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''conservative_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:conservative:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2063, 8, 201, 'optimistic_upkeep_physics_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_physics_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2064, 8, 202, 'optimistic_upkeep_society_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_society_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2065, 8, 203, 'optimistic_upkeep_engineering_research', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2066, 8, 204, 'optimistic_upkeep_energy', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_energy''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2067, 8, 205, 'optimistic_upkeep_minerals', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_minerals''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2068, 8, 206, 'optimistic_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2069, 8, 207, 'optimistic_upkeep_alloys', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_alloys''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2070, 8, 208, 'optimistic_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2071, 8, 209, 'optimistic_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2072, 8, 210, 'optimistic_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2073, 8, 211, 'optimistic_upkeep_food', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_food''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2074, 8, 212, 'optimistic_upkeep_unity', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_unity''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2075, 8, 213, 'optimistic_upkeep_influence', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_influence''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2076, 8, 214, 'optimistic_upkeep_trade', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_trade''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2077, 8, 215, 'optimistic_upkeep_trade_value', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_trade_value''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2078, 8, 216, 'optimistic_upkeep_sr_zro', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2079, 8, 217, 'optimistic_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2080, 8, 218, 'optimistic_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2081, 8, 219, 'optimistic_upkeep_nanites', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_nanites''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2082, 8, 220, 'optimistic_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2083, 8, 221, 'optimistic_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2084, 8, 222, 'optimistic_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2085, 8, 223, 'optimistic_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:optimistic:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''optimistic_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:optimistic:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2086, 8, 224, 'adjusted_upkeep_physics_research', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_physics_research''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2087, 8, 225, 'adjusted_upkeep_society_research', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_society_research''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2088, 8, 226, 'adjusted_upkeep_engineering_research', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_engineering_research''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2089, 8, 227, 'adjusted_upkeep_energy', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_energy''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2090, 8, 228, 'adjusted_upkeep_minerals', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_minerals''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2091, 8, 229, 'adjusted_upkeep_consumer_goods', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2092, 8, 230, 'adjusted_upkeep_alloys', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_alloys''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2093, 8, 231, 'adjusted_upkeep_volatile_motes', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2094, 8, 232, 'adjusted_upkeep_exotic_gases', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2095, 8, 233, 'adjusted_upkeep_rare_crystals', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2096, 8, 234, 'adjusted_upkeep_food', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_food''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2097, 8, 235, 'adjusted_upkeep_unity', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_unity''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2098, 8, 236, 'adjusted_upkeep_influence', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_influence''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2099, 8, 237, 'adjusted_upkeep_trade', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_trade''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2100, 8, 238, 'adjusted_upkeep_trade_value', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_trade_value''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2101, 8, 239, 'adjusted_upkeep_sr_zro', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_sr_zro''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2102, 8, 240, 'adjusted_upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2103, 8, 241, 'adjusted_upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2104, 8, 242, 'adjusted_upkeep_nanites', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_nanites''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2105, 8, 243, 'adjusted_upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2106, 8, 244, 'adjusted_upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2107, 8, 245, 'adjusted_upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2108, 8, 246, 'adjusted_upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:adjusted:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''adjusted_upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:adjusted:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2109, 8, 247, 'base_net_physics_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_net_physics_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2110, 8, 248, 'base_net_society_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_net_society_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2111, 8, 249, 'base_net_engineering_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''base_net_engineering_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2112, 8, 250, 'base_net_energy', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_energy''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2113, 8, 251, 'base_net_minerals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_minerals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2114, 8, 252, 'base_net_consumer_goods', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_consumer_goods''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2115, 8, 253, 'base_net_alloys', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_alloys''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2116, 8, 254, 'base_net_volatile_motes', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_volatile_motes''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2117, 8, 255, 'base_net_exotic_gases', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_exotic_gases''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2118, 8, 256, 'base_net_rare_crystals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_rare_crystals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2119, 8, 257, 'base_net_food', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_food''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2120, 8, 258, 'base_net_unity', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_unity''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2121, 8, 259, 'base_net_influence', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_influence''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2122, 8, 260, 'base_net_trade', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_trade''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2123, 8, 261, 'base_net_trade_value', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_trade_value''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2124, 8, 262, 'base_net_sr_zro', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_sr_zro''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2125, 8, 263, 'base_net_sr_dark_matter', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_sr_dark_matter''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2126, 8, 264, 'base_net_sr_living_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_sr_living_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2127, 8, 265, 'base_net_nanites', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_nanites''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2128, 8, 266, 'base_net_giga_sr_negative_mass', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_giga_sr_negative_mass''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2129, 8, 267, 'base_net_giga_sr_amb_megaconstruction', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_giga_sr_amb_megaconstruction''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2130, 8, 268, 'base_net_giga_sr_iodizium', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_giga_sr_iodizium''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2131, 8, 269, 'base_net_giga_sr_sentient_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''base_net_giga_sr_sentient_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2132, 8, 270, 'conservative_net_physics_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_net_physics_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2133, 8, 271, 'conservative_net_society_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_net_society_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2134, 8, 272, 'conservative_net_engineering_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''conservative_net_engineering_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2135, 8, 273, 'conservative_net_energy', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_energy''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2136, 8, 274, 'conservative_net_minerals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_minerals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2137, 8, 275, 'conservative_net_consumer_goods', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_consumer_goods''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2138, 8, 276, 'conservative_net_alloys', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_alloys''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2139, 8, 277, 'conservative_net_volatile_motes', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_volatile_motes''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2140, 8, 278, 'conservative_net_exotic_gases', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_exotic_gases''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2141, 8, 279, 'conservative_net_rare_crystals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_rare_crystals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2142, 8, 280, 'conservative_net_food', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_food''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2143, 8, 281, 'conservative_net_unity', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_unity''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2144, 8, 282, 'conservative_net_influence', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_influence''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2145, 8, 283, 'conservative_net_trade', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_trade''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2146, 8, 284, 'conservative_net_trade_value', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_trade_value''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2147, 8, 285, 'conservative_net_sr_zro', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_sr_zro''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2148, 8, 286, 'conservative_net_sr_dark_matter', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_sr_dark_matter''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2149, 8, 287, 'conservative_net_sr_living_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_sr_living_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2150, 8, 288, 'conservative_net_nanites', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_nanites''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2151, 8, 289, 'conservative_net_giga_sr_negative_mass', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_giga_sr_negative_mass''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2152, 8, 290, 'conservative_net_giga_sr_amb_megaconstruction', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_giga_sr_amb_megaconstruction''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2153, 8, 291, 'conservative_net_giga_sr_iodizium', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_giga_sr_iodizium''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2154, 8, 292, 'conservative_net_giga_sr_sentient_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''conservative_net_giga_sr_sentient_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2155, 8, 293, 'optimistic_net_physics_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_net_physics_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2156, 8, 294, 'optimistic_net_society_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_net_society_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2157, 8, 295, 'optimistic_net_engineering_research', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''optimistic_net_engineering_research''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2158, 8, 296, 'optimistic_net_energy', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_energy''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2159, 8, 297, 'optimistic_net_minerals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_minerals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2160, 8, 298, 'optimistic_net_consumer_goods', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_consumer_goods''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2161, 8, 299, 'optimistic_net_alloys', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_alloys''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2162, 8, 300, 'optimistic_net_volatile_motes', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_volatile_motes''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2163, 8, 301, 'optimistic_net_exotic_gases', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_exotic_gases''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2164, 8, 302, 'optimistic_net_rare_crystals', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_rare_crystals''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2165, 8, 303, 'optimistic_net_food', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_food''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2166, 8, 304, 'optimistic_net_unity', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_unity''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2167, 8, 305, 'optimistic_net_influence', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_influence''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2168, 8, 306, 'optimistic_net_trade', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_trade''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2169, 8, 307, 'optimistic_net_trade_value', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_trade_value''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2170, 8, 308, 'optimistic_net_sr_zro', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_sr_zro''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2171, 8, 309, 'optimistic_net_sr_dark_matter', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_sr_dark_matter''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2172, 8, 310, 'optimistic_net_sr_living_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_sr_living_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2173, 8, 311, 'optimistic_net_nanites', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_nanites''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2174, 8, 312, 'optimistic_net_giga_sr_negative_mass', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_giga_sr_negative_mass''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2175, 8, 313, 'optimistic_net_giga_sr_amb_megaconstruction', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_giga_sr_amb_megaconstruction''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2176, 8, 314, 'optimistic_net_giga_sr_iodizium', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_giga_sr_iodizium''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2177, 8, 315, 'optimistic_net_giga_sr_sentient_metal', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''optimistic_net_giga_sr_sentient_metal''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2178, 9, 1, 'role', 'identifier', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''role''. Descriptive or dimensional source value used to interpret the external record.'),
(2179, 9, 2, 'build_plan_family', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''build_plan_family''. Descriptive or dimensional source value used to interpret the external record.'),
(2180, 9, 3, 'source_scope', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_scope''. Descriptive or dimensional source value used to interpret the external record.'),
(2181, 9, 4, 'colony_class', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''colony_class''. Descriptive or dimensional source value used to interpret the external record.'),
(2182, 9, 5, 'slots', 'integer', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''slots''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2183, 9, 6, 'selected_count', 'integer', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''selected_count''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2184, 9, 7, 'selected_objects', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''selected_objects''. Descriptive or dimensional source value used to interpret the external record.'),
(2185, 9, 8, 'gross_role_output', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''gross_role_output''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2186, 9, 9, 'net_role_output', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''net_role_output''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2187, 9, 10, 'output_physics_research', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_physics_research''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2188, 9, 11, 'output_society_research', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_society_research''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2189, 9, 12, 'output_engineering_research', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_engineering_research''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2190, 9, 13, 'output_energy', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_energy''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2191, 9, 14, 'output_minerals', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_minerals''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2192, 9, 15, 'output_consumer_goods', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_consumer_goods''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2193, 9, 16, 'output_alloys', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_alloys''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2194, 9, 17, 'output_volatile_motes', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_volatile_motes''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2195, 9, 18, 'output_exotic_gases', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_exotic_gases''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2196, 9, 19, 'output_rare_crystals', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_rare_crystals''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2197, 9, 20, 'output_food', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_food''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2198, 9, 21, 'output_unity', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_unity''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2199, 9, 22, 'output_influence', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_influence''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2200, 9, 23, 'output_trade', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_trade''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2201, 9, 24, 'output_trade_value', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_trade_value''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2202, 9, 25, 'output_sr_zro', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_sr_zro''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2203, 9, 26, 'output_sr_dark_matter', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_sr_dark_matter''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2204, 9, 27, 'output_sr_living_metal', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_sr_living_metal''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2205, 9, 28, 'output_nanites', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_nanites''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2206, 9, 29, 'output_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2207, 9, 30, 'output_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2208, 9, 31, 'output_giga_sr_iodizium', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2209, 9, 32, 'output_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:aggregate:output', 'resource_output', 'modeled_amount', 1, 11, NULL, 'Exact external column ''output_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:aggregate:output; normalize selected facts through analysis_metric/analysis_value.'),
(2210, 9, 33, 'upkeep_physics_research', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_physics_research''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2211, 9, 34, 'upkeep_society_research', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_society_research''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2212, 9, 35, 'upkeep_engineering_research', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_engineering_research''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2213, 9, 36, 'upkeep_energy', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_energy''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2214, 9, 37, 'upkeep_minerals', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_minerals''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2215, 9, 38, 'upkeep_consumer_goods', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_consumer_goods''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2216, 9, 39, 'upkeep_alloys', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_alloys''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2217, 9, 40, 'upkeep_volatile_motes', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_volatile_motes''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2218, 9, 41, 'upkeep_exotic_gases', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_exotic_gases''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2219, 9, 42, 'upkeep_rare_crystals', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_rare_crystals''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2220, 9, 43, 'upkeep_food', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_food''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2221, 9, 44, 'upkeep_unity', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_unity''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2222, 9, 45, 'upkeep_influence', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_influence''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2223, 9, 46, 'upkeep_trade', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_trade''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2224, 9, 47, 'upkeep_trade_value', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_trade_value''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2225, 9, 48, 'upkeep_sr_zro', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_sr_zro''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2226, 9, 49, 'upkeep_sr_dark_matter', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_sr_dark_matter''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2227, 9, 50, 'upkeep_sr_living_metal', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_sr_living_metal''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2228, 9, 51, 'upkeep_nanites', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_nanites''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2229, 9, 52, 'upkeep_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2230, 9, 53, 'upkeep_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2231, 9, 54, 'upkeep_giga_sr_iodizium', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2232, 9, 55, 'upkeep_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:aggregate:upkeep', 'resource_upkeep', 'modeled_amount', 1, 11, NULL, 'Exact external column ''upkeep_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:aggregate:upkeep; normalize selected facts through analysis_metric/analysis_value.'),
(2233, 9, 56, 'net_physics_research', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_physics_research''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2234, 9, 57, 'net_society_research', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_society_research''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2235, 9, 58, 'net_engineering_research', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_engineering_research''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2236, 9, 59, 'net_energy', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_energy''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2237, 9, 60, 'net_minerals', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_minerals''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2238, 9, 61, 'net_consumer_goods', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_consumer_goods''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2239, 9, 62, 'net_alloys', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_alloys''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2240, 9, 63, 'net_volatile_motes', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_volatile_motes''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2241, 9, 64, 'net_exotic_gases', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_exotic_gases''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2242, 9, 65, 'net_rare_crystals', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_rare_crystals''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2243, 9, 66, 'net_food', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_food''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2244, 9, 67, 'net_unity', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_unity''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2245, 9, 68, 'net_influence', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_influence''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2246, 9, 69, 'net_trade', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_trade''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2247, 9, 70, 'net_trade_value', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_trade_value''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2248, 9, 71, 'net_sr_zro', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_sr_zro''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2249, 9, 72, 'net_sr_dark_matter', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_sr_dark_matter''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2250, 9, 73, 'net_sr_living_metal', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_sr_living_metal''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2251, 9, 74, 'net_nanites', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_nanites''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2252, 9, 75, 'net_giga_sr_negative_mass', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_giga_sr_negative_mass''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2253, 9, 76, 'net_giga_sr_amb_megaconstruction', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_giga_sr_amb_megaconstruction''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2254, 9, 77, 'net_giga_sr_iodizium', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_giga_sr_iodizium''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2255, 9, 78, 'net_giga_sr_sentient_metal', 'real', 'metric', 'resource_flow:net:net', 'resource_net', 'modeled_amount', 1, 11, NULL, 'Exact external column ''net_giga_sr_sentient_metal''. Controlled dimensional metric in resource_flow:net:net; normalize selected facts through analysis_metric/analysis_value.'),
(2256, 10, 1, 'technology_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''technology_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2257, 10, 2, 'winning_mod_name', 'text', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_mod_name''. Identifies the source mod, file, root, or load position that produced the record.'),
(2258, 10, 3, 'winning_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(2259, 10, 4, 'modifier_keys_json', 'json', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''modifier_keys_json''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(2260, 10, 5, 'planet_researcher_or_job_output_mult', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''planet_researcher_or_job_output_mult''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2261, 10, 6, 'station_research_output_mult', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''station_research_output_mult''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2262, 10, 7, 'research_speed_mult', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''research_speed_mult''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2263, 10, 8, 'researcher_upkeep_mult', 'real', 'metric', NULL, NULL, 'modeled_research', 1, NULL, NULL, 'Exact external column ''researcher_upkeep_mult''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2264, 10, 9, 'unresolved_variables', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unresolved_variables''. Descriptive or dimensional source value used to interpret the external record.'),
(2265, 11, 1, 'building_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''building_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2266, 11, 2, 'primary_role', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''primary_role''. Descriptive or dimensional source value used to interpret the external record.'),
(2267, 11, 3, 'primary_role_score', 'real', 'metric', NULL, NULL, 'score', 1, NULL, NULL, 'Exact external column ''primary_role_score''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2268, 11, 4, 'readiness_phase', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''readiness_phase''. Descriptive or dimensional source value used to interpret the external record.'),
(2269, 11, 5, 'gate_reasons', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''gate_reasons''. Descriptive or dimensional source value used to interpret the external record.'),
(2270, 11, 6, 'build_plan_candidate', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''build_plan_candidate''. Descriptive or dimensional source value used to interpret the external record.'),
(2271, 11, 7, 'repeatable_candidate', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''repeatable_candidate''. Descriptive or dimensional source value used to interpret the external record.'),
(2272, 11, 8, 'capital_tier_gate', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''capital_tier_gate''. Descriptive or dimensional source value used to interpret the external record.'),
(2273, 11, 9, 'fallback_building_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''fallback_building_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2274, 11, 10, 'fallback_primary_role_score', 'real', 'metric', NULL, NULL, 'score', 1, NULL, NULL, 'Exact external column ''fallback_primary_role_score''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2275, 11, 11, 'fallback_reason', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''fallback_reason''. Descriptive or dimensional source value used to interpret the external record.'),
(2276, 11, 12, 'readiness_status', 'text', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''readiness_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(2277, 11, 13, 'prerequisites', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''prerequisites''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(2278, 11, 14, 'potential_allow_gates', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''potential_allow_gates''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(2279, 11, 15, 'potential_allow_gate_atoms', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''potential_allow_gate_atoms''. Descriptive or dimensional source value used to interpret the external record.'),
(2280, 11, 16, 'event_flags', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''event_flags''. Descriptive or dimensional source value used to interpret the external record.'),
(2281, 11, 17, 'unlock_flags', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''unlock_flags''. Descriptive or dimensional source value used to interpret the external record.'),
(2282, 11, 18, 'is_upgrade_terminal', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''is_upgrade_terminal''. Descriptive or dimensional source value used to interpret the external record.'),
(2283, 11, 19, 'upgrade_terminal', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''upgrade_terminal''. Descriptive or dimensional source value used to interpret the external record.'),
(2284, 11, 20, 'upgrade_chain_to_terminal', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''upgrade_chain_to_terminal''. Descriptive or dimensional source value used to interpret the external record.'),
(2285, 11, 21, 'colony_class', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''colony_class''. Descriptive or dimensional source value used to interpret the external record.'),
(2286, 11, 22, 'category', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''category''. Descriptive or dimensional source value used to interpret the external record.'),
(2287, 11, 23, 'winning_mod_name', 'text', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_mod_name''. Identifies the source mod, file, root, or load position that produced the record.'),
(2288, 11, 24, 'winning_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(2289, 12, 1, 'benefit_class', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''benefit_class''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2290, 12, 2, 'object_type', 'text', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_type''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2291, 12, 3, 'object_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2292, 12, 4, 'role', 'identifier', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''role''. Descriptive or dimensional source value used to interpret the external record.'),
(2293, 12, 5, 'strategic_tags', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''strategic_tags''. Descriptive or dimensional source value used to interpret the external record.'),
(2294, 12, 6, 'evidence_kind', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''evidence_kind''. Descriptive or dimensional source value used to interpret the external record.'),
(2295, 12, 7, 'valuation_status', 'text', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''valuation_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(2296, 12, 8, 'formula_status', 'expression', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''formula_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(2297, 12, 9, 'benefit_amount', 'real', 'metric', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''benefit_amount''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2298, 12, 10, 'source_terms', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_terms''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(2299, 12, 11, 'matched_modifier_keys', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''matched_modifier_keys''. Descriptive or dimensional source value used to interpret the external record.'),
(2300, 12, 12, 'matched_tags', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''matched_tags''. Descriptive or dimensional source value used to interpret the external record.'),
(2301, 12, 13, 'priority_score', 'real', 'metric', NULL, NULL, 'score', 1, NULL, NULL, 'Exact external column ''priority_score''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2302, 12, 14, 'can_demolish', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''can_demolish''. Descriptive or dimensional source value used to interpret the external record.'),
(2303, 12, 15, 'can_build', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''can_build''. Descriptive or dimensional source value used to interpret the external record.'),
(2304, 12, 16, 'can_be_disabled', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''can_be_disabled''. Descriptive or dimensional source value used to interpret the external record.'),
(2305, 12, 17, 'has_destroy_trigger', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''has_destroy_trigger''. Descriptive or dimensional source value used to interpret the external record.'),
(2306, 12, 18, 'winning_mod_name', 'text', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_mod_name''. Identifies the source mod, file, root, or load position that produced the record.'),
(2307, 12, 19, 'winning_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(2308, 12, 20, 'modeling_decision', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''modeling_decision''. Descriptive or dimensional source value used to interpret the external record.'),
(2309, 12, 21, 'formula_or_policy', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''formula_or_policy''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(2310, 12, 22, 'policy_confidence', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''policy_confidence''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(2311, 13, 1, 'source_artifact', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_artifact''. Descriptive or dimensional source value used to interpret the external record.'),
(2312, 13, 2, 'object_type', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_type''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2313, 13, 3, 'object_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2314, 13, 4, 'issue_type', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''issue_type''. Descriptive or dimensional source value used to interpret the external record.'),
(2315, 13, 5, 'issue_key', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''issue_key''. Descriptive or dimensional source value used to interpret the external record.'),
(2316, 13, 6, 'accounting_status', 'unknown', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''accounting_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(2317, 13, 7, 'next_action', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''next_action''. Descriptive or dimensional source value used to interpret the external record.'),
(2318, 13, 8, 'source_mod', 'unknown', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_mod''. Identifies the source mod, file, root, or load position that produced the record.'),
(2319, 13, 9, 'source_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(2320, 14, 1, 'row_family', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''row_family''. Descriptive or dimensional source value used to interpret the external record.'),
(2321, 14, 2, 'consumer_surface', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''consumer_surface''. Descriptive or dimensional source value used to interpret the external record.'),
(2322, 14, 3, 'consumer_proof_status', 'text', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''consumer_proof_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(2323, 14, 4, 'object_type', 'text', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_type''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2324, 14, 5, 'object_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2325, 14, 6, 'role', 'identifier', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''role''. Descriptive or dimensional source value used to interpret the external record.'),
(2326, 14, 7, 'source_scope', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_scope''. Descriptive or dimensional source value used to interpret the external record.'),
(2327, 14, 8, 'consumer_modeling_status', 'text', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''consumer_modeling_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(2328, 14, 9, 'can_consume_now', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''can_consume_now''. Descriptive or dimensional source value used to interpret the external record.'),
(2329, 14, 10, 'readiness_phase', 'text', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''readiness_phase''. Descriptive or dimensional source value used to interpret the external record.'),
(2330, 14, 11, 'build_plan_candidate', 'boolean', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''build_plan_candidate''. Descriptive or dimensional source value used to interpret the external record.'),
(2331, 14, 12, 'gate_reasons', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''gate_reasons''. Descriptive or dimensional source value used to interpret the external record.'),
(2332, 14, 13, 'blocker_count', 'integer', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''blocker_count''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2333, 14, 14, 'blocker_issue_types', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''blocker_issue_types''. Descriptive or dimensional source value used to interpret the external record.'),
(2334, 14, 15, 'benefit_numeric_rows', 'integer', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''benefit_numeric_rows''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2335, 14, 16, 'benefit_policy_required_rows', 'integer', 'count', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''benefit_policy_required_rows''. Numeric generated measurement retained externally; store only selected normalized facts in the knowledge base.'),
(2336, 14, 17, 'fallback_building_id', 'identifier', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''fallback_building_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2337, 14, 18, 'fallback_lifetime', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''fallback_lifetime''. Descriptive or dimensional source value used to interpret the external record.'),
(2338, 14, 19, 'replacement_policy', 'expression', 'expression', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''replacement_policy''. Structured or expression-bearing source value; do not treat opaque text as a substitute for normalized facts.'),
(2339, 14, 20, 'selected_objects', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''selected_objects''. Descriptive or dimensional source value used to interpret the external record.'),
(2340, 14, 21, 'source_mod', 'text', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_mod''. Identifies the source mod, file, root, or load position that produced the record.'),
(2341, 14, 22, 'source_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_file''. Identifies the source mod, file, root, or load position that produced the record.'),
(2342, 14, 23, 'next_action', 'text', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''next_action''. Descriptive or dimensional source value used to interpret the external record.'),
(2343, 15, 1, 'benefit_class', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''benefit_class''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2344, 15, 2, 'object_type', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_type''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2345, 15, 3, 'object_id', 'unknown', 'identifier', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''object_id''. Stable or contextual record identifier used for exact evidence retrieval and joins.'),
(2346, 15, 4, 'role', 'unknown', 'dimension', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''role''. Descriptive or dimensional source value used to interpret the external record.'),
(2347, 15, 5, 'strategic_tags', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''strategic_tags''. Descriptive or dimensional source value used to interpret the external record.'),
(2348, 15, 6, 'evidence_kind', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''evidence_kind''. Descriptive or dimensional source value used to interpret the external record.'),
(2349, 15, 7, 'valuation_status', 'unknown', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''valuation_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(2350, 15, 8, 'formula_status', 'unknown', 'status', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''formula_status''. Generator-assigned status or quality classification; preserve the generator vocabulary.'),
(2351, 15, 9, 'benefit_amount', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''benefit_amount''. Descriptive or dimensional source value used to interpret the external record.'),
(2352, 15, 10, 'source_terms', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''source_terms''. Descriptive or dimensional source value used to interpret the external record.'),
(2353, 15, 11, 'matched_modifier_keys', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''matched_modifier_keys''. Descriptive or dimensional source value used to interpret the external record.'),
(2354, 15, 12, 'matched_tags', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''matched_tags''. Descriptive or dimensional source value used to interpret the external record.'),
(2355, 15, 13, 'priority_score', 'unknown', 'text', NULL, NULL, 'score', 1, NULL, NULL, 'Exact external column ''priority_score''. Descriptive or dimensional source value used to interpret the external record.'),
(2356, 15, 14, 'can_demolish', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''can_demolish''. Descriptive or dimensional source value used to interpret the external record.'),
(2357, 15, 15, 'can_build', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''can_build''. Descriptive or dimensional source value used to interpret the external record.'),
(2358, 15, 16, 'can_be_disabled', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''can_be_disabled''. Descriptive or dimensional source value used to interpret the external record.'),
(2359, 15, 17, 'has_destroy_trigger', 'unknown', 'text', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''has_destroy_trigger''. Descriptive or dimensional source value used to interpret the external record.'),
(2360, 15, 18, 'winning_mod_name', 'unknown', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_mod_name''. Identifies the source mod, file, root, or load position that produced the record.'),
(2361, 15, 19, 'winning_file', 'path', 'provenance', NULL, NULL, NULL, 1, NULL, NULL, 'Exact external column ''winning_file''. Identifies the source mod, file, root, or load position that produced the record.');

INSERT INTO dataset_key_column(
    dataset_schema_id, dataset_column_id, key_ordinal, normalization_rule, is_stable_across_versions
) VALUES
(1, 1002, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(1, 1001, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(1, 1003, 3, 'trim; preserve case unless generator contract says otherwise', 1),
(2, 1026, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(2, 1025, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(2, 1027, 3, 'trim; preserve case unless generator contract says otherwise', 1),
(2, 1029, 4, 'trim; preserve case unless generator contract says otherwise', 1),
(2, 1028, 5, 'trim; preserve case unless generator contract says otherwise', 1),
(3, 1034, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(3, 1033, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(3, 1035, 3, 'trim; preserve case unless generator contract says otherwise', 1),
(4, 1044, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(4, 1043, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(4, 1045, 3, 'trim; preserve case unless generator contract says otherwise', 1),
(5, 1057, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(5, 1060, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(6, 1211, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(7, 1493, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(7, 1494, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(8, 1863, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(9, 2178, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(9, 2179, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(9, 2180, 3, 'trim; preserve case unless generator contract says otherwise', 1),
(10, 2256, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(11, 2265, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(12, 2289, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(12, 2290, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(12, 2291, 3, 'trim; preserve case unless generator contract says otherwise', 1),
(13, 2311, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(13, 2312, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(13, 2313, 3, 'trim; preserve case unless generator contract says otherwise', 1),
(13, 2314, 4, 'trim; preserve case unless generator contract says otherwise', 1),
(13, 2315, 5, 'trim; preserve case unless generator contract says otherwise', 1),
(14, 2320, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(14, 2323, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(14, 2324, 3, 'trim; preserve case unless generator contract says otherwise', 1),
(14, 2326, 4, 'trim; preserve case unless generator contract says otherwise', 1),
(15, 2343, 1, 'trim; preserve case unless generator contract says otherwise', 1),
(15, 2344, 2, 'trim; preserve case unless generator contract says otherwise', 1),
(15, 2345, 3, 'trim; preserve case unless generator contract says otherwise', 1);

INSERT INTO playset_snapshot(
    playset_snapshot_id, playset_item_id, snapshot_key, game_version_id, repository_snapshot_id, source_artifact_id, captured_at, declared_mod_count, is_current, resolution_status, notes, created_in_change_set_id
) VALUES
(1, 320, 'active-playset-2026-07-04-plus-director', 2, 1, 20, '2026-07-10T10:06:43-04:00', 116, 1, 'validated', 'Captured source snapshot; refresh before claims about later launcher state.', 1);

INSERT INTO playset_member(
    playset_member_id, playset_snapshot_id, mod_release_id, source_root_id, load_position, enabled, required_by_project, descriptor_path, live_load_state, notes
) VALUES
(1, 1, 3, 4, 62, 1, 1, NULL, 'unknown', 'Required parent present in captured snapshot.'),
(2, 1, 8, 9, 64, 1, 0, NULL, 'unknown', 'Optional/active integration.'),
(3, 1, 9, 10, 66, 1, 0, NULL, 'unknown', 'Parent of Director naval administration overrides.'),
(4, 1, 5, 6, 70, 1, 1, NULL, 'unknown', 'Required parent.'),
(5, 1, 4, 5, 71, 1, 1, NULL, 'unknown', 'Required parent.'),
(6, 1, 6, 7, 72, 1, 1, NULL, 'unknown', 'Required parent.'),
(7, 1, 10, 11, 103, 1, 0, NULL, 'unknown', 'Active UI surface.'),
(8, 1, 7, 8, 115, 1, 1, NULL, 'unknown', 'Required/active utility.'),
(9, 1, 2, 3, 116, 1, 1, 'mods/StellarAIDirector/descriptor.mod', 'unknown', 'Project source member; live launcher descriptor not checked here.');

INSERT INTO execution_context(
    execution_context_id, context_key, title, game_version_id, version_span_id, repository_snapshot_id, playset_snapshot_id, run_mode, platform, game_checksum, settings_summary, created_at, is_current, notes, created_in_change_set_id
) VALUES
(1, 'context:static-b605aa0e-4.4.5', 'Static project/modeling context', 2, 3, 1, 1, 'static', 'Windows/Steam', NULL, 'Captured 116-mod playset; no game launch required.', '2026-07-10T10:06:43-04:00', 1, 'Default context for source/model artifacts.', 1),
(2, 'context:observer-war-gate-20260710', 'Observer/all-AI selected-save context', 2, 3, 1, 1, 'observer', 'Windows/Steam', NULL, 'human_ai; observe; game_speed 5; country 0 included as AI.', '2026-07-10T10:08:00-04:00', 0, 'Applies only to the manually selected saves.', 1),
(3, 'context:database-validation-revision2', 'SQLite design validation context', NULL, NULL, 1, NULL, 'database_validation', 'Python sqlite3', NULL, 'Fresh local SQLite file; foreign keys on; WAL requested.', '2026-07-10T17:00:00Z', 0, 'Used to validate the deliverable, not Stellaris behavior.', 1);

INSERT INTO execution_context_item(
    execution_context_id, item_id, role_code, state_code, notes
) VALUES
(1, 110, 'target_subsystem', 'active', 'Economic planning model.'),
(1, 111, 'target_subsystem', 'active', 'War-planning context.'),
(1, 360, 'enabled_dlc', 'assumed', 'Nomads compatibility case.'),
(1, 361, 'setting', 'version_sensitive', 'Economy baseline setting.'),
(1, 310, 'excluded_item', 'absent', 'Spacefleet Tactica absent from captured playset.'),
(1, 311, 'excluded_item', 'absent', 'Stellar AI parity reference absent.'),
(2, 111, 'target_subsystem', 'active', 'War-gate diagnosis.'),
(2, 362, 'setting', 'enabled', 'Country 0 treated as AI.'),
(2, 363, 'setting', 'enabled', 'Observer speed protocol.');

INSERT INTO evidence_locator(
    evidence_locator_id, source_artifact_id, dataset_schema_id, locator_type_id, stable_locator_key, label, relative_path, line_start, line_end, page_start, page_end, section_title, symbol_or_object_key, record_set, record_key, row_number, column_name, json_path, archive_member_path, byte_start, byte_end, query_text, timestamp_start, timestamp_end, game_date, excerpt, evidence_summary, retrieval_instructions, created_by_actor_id, created_in_change_set_id
) VALUES
(30, 20, NULL, 12, 'json:director-member', 'Director member in active playset', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '$.mods[115]', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Captured position 116 and project path.', 'Retrieves the Director playset member.', 'Open JSON and inspect $.mods[115].', 2, 1),
(31, 20, NULL, 12, 'json:required-mods', 'Required parent map', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '$.required_mods', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Required Gigas/ESC/NSC3/Starbase parents and positions.', 'Captures generator-required parents.', 'Open JSON and inspect $.required_mods.', 2, 1),
(32, 21, 1, 4, 'dataset:object-atlas-header', 'Object-atlas schema', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'object_atlas', 'header', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '24-column schema documented in dataset_column.', 'Exact generated schema.', 'Use JDataMunch describe_dataset.', 2, 1),
(33, 21, 1, 4, 'dataset:default-country-type', 'Object-atlas default country type', 'research/stellar-ai/object-atlas/object-atlas-2026-07-06.csv', NULL, NULL, NULL, NULL, NULL, 'default', 'object_atlas', 'country_type:default', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Locate every active-stack definition occurrence for country_type:default.', 'Definition inventory locator.', 'Query object_type=country_type and object_id=default.', 2, 1),
(34, 25, 5, 11, 'dataset:job-low-tech-researcher', 'low_tech_researcher model row', NULL, NULL, NULL, NULL, NULL, NULL, 'low_tech_researcher', 'jobs', 'vanilla:low_tech_researcher', 247, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Base output is one of each research type; base consumer-goods upkeep is one.', 'Exact selected model row.', 'Use JDataMunch row 247 or key vanilla+low_tech_researcher.', 2, 1),
(35, 26, 6, 11, 'dataset:building-research-lab-1', 'building_research_lab_1 model row', NULL, NULL, NULL, NULL, NULL, NULL, 'building_research_lab_1', 'buildings', 'building_research_lab_1', 652, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Vanilla winning file, tech prerequisite, upgrade chain, and energy upkeep.', 'Exact selected building row.', 'Use JDataMunch row 652 or building_id key.', 2, 1),
(36, 26, 6, 11, 'dataset:building-navel-base', 'building_navel_base model row', NULL, NULL, NULL, NULL, NULL, NULL, 'building_navel_base', 'buildings', 'building_navel_base', 578, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Director winner with PD jobs, modeled society output, and upkeep.', 'Exact selected building row.', 'Use JDataMunch row 578 or building_id key.', 2, 1),
(37, 31, 11, 11, 'dataset:readiness-research-lab-1', 'Research lab readiness row', NULL, NULL, NULL, NULL, NULL, NULL, 'building_research_lab_1', 'readiness', 'building_research_lab_1', 477, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'After-prerequisite candidate with conservative fallback policy.', 'Exact readiness row.', 'Use JDataMunch row 477.', 2, 1),
(38, 31, 11, 11, 'dataset:readiness-navel-base', 'Naval base readiness row', NULL, NULL, NULL, NULL, NULL, NULL, 'building_navel_base', 'readiness', 'building_navel_base', 192, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'After-prerequisite candidate with scripted gates and fallback.', 'Exact readiness row.', 'Use JDataMunch row 192.', 2, 1),
(39, 32, 12, 11, 'dataset:benefit-navel-capacity', 'Naval-capacity benefit row', NULL, NULL, NULL, NULL, NULL, NULL, 'building_navel_base', 'benefit_taxonomy', 'naval_capacity:building:building_navel_base', 1392, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Numeric modifier evidence preserved for naval capacity.', 'Exact benefit row.', 'Use JDataMunch row 1392.', 2, 1),
(40, 34, 14, 11, 'dataset:consumer-research-lab-1', 'Research lab consumer-policy row', NULL, NULL, NULL, NULL, NULL, NULL, 'building_research_lab_1', 'consumer_policy', 'building:building_research_lab_1', 672, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Conditional consumption with no proactive replacement proof.', 'Exact consumer-policy row.', 'Use JDataMunch row 672.', 2, 1),
(41, 34, 14, 11, 'dataset:consumer-navel-base', 'Naval base consumer-policy row', NULL, NULL, NULL, NULL, NULL, NULL, 'building_navel_base', 'consumer_policy', 'building:building_navel_base', 598, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Conditional consumption, two numeric benefit rows, permanent/no-regret fallback.', 'Exact consumer-policy row.', 'Use JDataMunch row 598.', 2, 1),
(42, 33, 13, 4, 'dataset:blocker-current-empty', 'Current blocker-accounting dataset', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'blocker_accounting', 'header_only', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Current extracted artifact has the 9-column header and zero blocker rows.', 'Exact current blocker surface.', 'Describe the dataset and verify row_count=0.', 2, 1),
(43, 35, NULL, 10, 'save-report:latest-summary', 'Latest selected save summary', '11_SELECTED_SAVE_EVIDENCE.md', NULL, NULL, NULL, NULL, 'Derived War-State Evidence', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2239.08.13 summary: 26 regular AI, 3 wars, 4 AI at war, 17 never at war, 16 modeled candidates.', 'Report-level evidence with explicit interpretation boundary.', 'Open the named report section and raw save by hash.', 2, 1),
(44, 36, NULL, 14, 'hash:stuck-ranulia-save', 'Latest selected save hash', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'SHA-256 122ac606...; 4,282,265 bytes.', 'Cryptographic save identity.', 'Retrieve the staged save path and verify SHA-256 before analysis.', 2, 1),
(45, 44, NULL, 2, 'object:director-default-country-type', 'Director default country type', 'mods/StellarAIDirector/common/country_types/zzzzz_staid_18_native_war_readiness.txt', NULL, NULL, NULL, NULL, NULL, 'default', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Full-object override: ai.enabled yes, declare_war yes, min_assault_armies_for_wars 0; min_navy gate omitted.', 'Exact project source occurrence.', 'Open file at repository snapshot and revalidate against current vanilla after updates.', 2, 1),
(46, 45, NULL, 2, 'object:vanilla-default-country-type', 'Vanilla default country type', 'common/country_types/00_country_types.txt', NULL, NULL, NULL, NULL, NULL, 'default', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Target-version vanilla occurrence; exact hash/fields must be refreshed for version changes.', 'Exact local vanilla source path.', 'Open current local 4.4.5 file and record lines/hash.', 2, 1),
(47, 20, NULL, 15, 'playset:director-position-116', 'Director captured load position', NULL, NULL, NULL, NULL, NULL, NULL, 'Stellar AI Director', 'mods', 'position:116', 116, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Director follows all required parents in the captured order.', 'Captured ordering evidence.', 'Open active playset JSON and verify member position 116.', 2, 1),
(48, 47, NULL, 10, 'ledger:benefit-schema-history', 'Benefit-taxonomy schema history', '10_STELLAR_AI_MODELING_HANDOFF.md', NULL, NULL, NULL, NULL, 'MODELING_COMPLETION_LEDGER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Ledger records an earlier 1,887-row/19-column checkpoint and later expanded schema.', 'Supports schema-drift demonstration.', 'Open the ledger validation log entries around commit de022d94.', 2, 1),
(49, 32, 12, 4, 'dataset:benefit-current-header', 'Current benefit-taxonomy header', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'benefit_taxonomy', 'header', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Current extracted schema has 22 columns and 1,924 rows.', 'Current schema locator.', 'Describe current dataset.', 2, 1),
(50, 47, NULL, 10, 'ledger:building-coverage', 'Active winning building coverage', '10_STELLAR_AI_MODELING_HANDOFF.md', NULL, NULL, NULL, NULL, 'MODELING_COMPLETION_LEDGER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'JData join reported 648 active winning building IDs and 648 modeled, with zero missing.', 'Coverage finding evidence.', 'Open M01 and validation log.', 2, 1),
(51, 47, NULL, 10, 'ledger:model-generation-counts', 'Model generation counts', '10_STELLAR_AI_MODELING_HANDOFF.md', NULL, NULL, NULL, NULL, 'MODELING_COMPLETION_LEDGER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Generator counts include 501 jobs, 826 buildings, 547 development rows, 247 roles, 826 readiness rows, and 1,093 consumer-policy rows.', 'Run-output summary.', 'Open validation log and current files.', 2, 1),
(52, 35, NULL, 10, 'observation:science-ship-mia-loop', 'Science-ship closed-border MIA loop observation', '11_SELECTED_SAVE_EVIDENCE.md', NULL, NULL, NULL, NULL, 'Runtime Observation Attached To The Latest Manual Save', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'User observed a science ship repeatedly enter a closed-border route, go MIA, and retry.', 'User observation correlated to the hashed save, not a parsed save field.', 'Retrieve report section and reproduce separately if causal proof is needed.', 2, 1),
(53, 37, NULL, 14, 'hash:autosave-2239-07-01', 'Autosave hash', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'SHA-256 12f9459...; 4,293,306 bytes.', 'Cryptographic save identity.', 'Verify SHA-256.', 2, 1),
(54, 38, NULL, 14, 'hash:end-save-2234-01-01', 'End save hash', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'SHA-256 884b7f7...; 4,131,974 bytes.', 'Cryptographic save identity.', 'Verify SHA-256.', 2, 1),
(55, 39, NULL, 14, 'hash:start-save-2232-01-01', 'Start save hash', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'SHA-256 70c29fa...; 4,120,957 bytes.', 'Cryptographic save identity.', 'Verify SHA-256.', 2, 1),
(56, 46, NULL, 2, 'object:director-building-navel-base', 'Director building_navel_base', 'mods/StellarAIDirector/common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt', NULL, NULL, NULL, NULL, NULL, 'building_navel_base', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Full-object override with hard AI readiness and research-designation exclusions.', 'Exact project source occurrence.', 'Open file at snapshot.', 2, 1),
(57, 21, 1, 4, 'object-atlas:pd-parent-navel-base', 'PD parent building_navel_base occurrence', NULL, NULL, NULL, NULL, NULL, NULL, 'building_navel_base', 'object_atlas', 'building:building_navel_base:PD More Arcologies', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Use object atlas/source root to retrieve the parent occurrence; exact parent path is intentionally not duplicated here.', 'Parent source occurrence locator.', 'Query object atlas then open source_root 10.', 2, 1);

INSERT INTO object_definition(
    object_definition_id, object_item_id, version_span_id, source_system_id, source_root_id, mod_release_id, evidence_locator_id, definition_status, object_path, line_start, line_end, content_hash_algorithm, content_hash, notes, created_in_change_set_id
) VALUES
(10, 132, 2, 1, 2, 1, 46, 'reference', 'common/country_types/00_country_types.txt', NULL, NULL, NULL, NULL, '4.4.4/vanilla reference values require target-version revalidation.', 1),
(11, 132, 3, 5, 3, 2, 45, 'candidate', 'mods/StellarAIDirector/common/country_types/zzzzz_staid_18_native_war_readiness.txt', NULL, NULL, NULL, NULL, 'Captured Director full-object override.', 1),
(12, 403, 3, 14, 10, 9, 57, 'reference', NULL, NULL, NULL, NULL, NULL, 'Parent PD More Arcologies occurrence; exact path retrieved through object atlas/source root.', 1),
(13, 403, 3, 5, 3, 2, 56, 'candidate', 'mods/StellarAIDirector/common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt', NULL, NULL, NULL, NULL, 'Captured Director winning override.', 1);

INSERT INTO object_field_occurrence(
    object_field_occurrence_id, object_definition_id, object_item_id, field_item_id, parent_occurrence_id, version_span_id, source_system_id, evidence_locator_id, ordinal_in_object, field_path, occurrence_kind, value_type, value_text, integer_value, real_value, boolean_value, referenced_item_id, expression_text, normalized_summary, created_in_change_set_id
) VALUES
(10, 10, 132, 427, NULL, 2, 1, 46, 1, 'ai.min_navy_for_wars', 'scalar', 'real', NULL, NULL, 0.5, NULL, NULL, 'min_navy_for_wars = 0.5', 'Pegasus 4.4.4 reference threshold.', 1),
(11, 10, 132, 426, NULL, 2, 1, 46, 1, 'ai.min_assault_armies_for_wars', 'scalar', 'integer', NULL, 6, NULL, NULL, NULL, 'min_assault_armies_for_wars = 6', 'Pegasus 4.4.4 reference threshold.', 1),
(12, 11, 132, 424, NULL, 3, 5, 45, 1, 'ai.enabled', 'scalar', 'boolean', NULL, NULL, NULL, 1, NULL, 'enabled = yes', 'Native AI remains enabled.', 1),
(13, 11, 132, 425, NULL, 3, 5, 45, 1, 'ai.declare_war', 'scalar', 'boolean', NULL, NULL, NULL, 1, NULL, 'declare_war = yes', 'Native declarations remain enabled.', 1),
(14, 11, 132, 426, NULL, 3, 5, 45, 1, 'ai.min_assault_armies_for_wars', 'scalar', 'integer', NULL, 0, NULL, NULL, NULL, 'min_assault_armies_for_wars = 0', 'Director removes the assault-army pre-planner threshold.', 1),
(15, 13, 403, 156, NULL, 3, 5, 56, 1, 'ai_weight', 'block', 'block', NULL, NULL, NULL, NULL, NULL, 'not used as plan enforcement', 'Source explicitly relies on potential/allow hard gates while economic plans are enabled.', 1);

INSERT INTO definition_reference(
    definition_reference_id, object_definition_id, source_occurrence_id, stable_reference_key, reference_kind, target_item_id, target_key_text, target_object_kind_id, resolution_status, evidence_locator_id, notes, created_in_change_set_id
) VALUES
(1, 13, NULL, 'prerequisite:tech_planetary_defenses', 'prerequisite', 417, NULL, 8, 'resolved', 56, NULL, 1),
(2, 13, NULL, 'job:job_pd_naval_admin', 'creates_job', 432, NULL, 6, 'resolved', 36, NULL, 1),
(3, 13, NULL, 'job:job_pd_naval_admin_gestalt', 'creates_job', 433, NULL, 6, 'resolved', 36, NULL, 1),
(4, 13, NULL, 'trigger:staid_naval_capacity_expansion_ready', 'eligibility_gate', 428, NULL, NULL, 'resolved', 56, NULL, 1),
(5, 11, NULL, 'field-omission:min_navy_for_wars', 'intentional_omission', 427, 'min_navy_for_wars', NULL, 'resolved', 45, 'Omission is the mechanism for removing the navy pre-planner gate.', 1);

INSERT INTO playset_object_resolution(
    playset_object_resolution_id, playset_snapshot_id, object_item_id, winning_definition_id, resolution_status, resolver_tool_item_id, resolution_method, evidence_locator_id, review_required, resolved_at, notes
) VALUES
(1, 1, 132, 11, 'resolved', 191, 'Captured load order plus full-object override source', 47, 1, '2026-07-10T10:06:43-04:00', 'Full-object copy must be regenerated/revalidated after game updates.'),
(2, 1, 403, 13, 'resolved', 191, 'Captured load order plus generated object-atlas winner', 36, 1, '2026-07-10T10:06:43-04:00', 'Parent object remains a compatibility dependency.'),
(3, 1, 134, 4, 'single', 191, 'Vanilla definition in captured object atlas', 35, 0, '2026-07-10T10:06:43-04:00', NULL);

INSERT INTO object_conflict(
    object_conflict_id, playset_snapshot_id, conflict_key, object_item_id, conflict_kind, risk_level_id, status_code, winning_definition_id, detected_by_tool_item_id, evidence_locator_id, detected_at, rationale, required_action, created_in_change_set_id
) VALUES
(1, 1, 'country_type:default:director-full-override', 132, 'duplicate_definition', 4, 'accepted', 11, 191, 45, '2026-07-10T10:06:43-04:00', 'Director intentionally replaces the complete regular default country type to remove two pre-planner gates.', 'Diff every vanilla field and regenerate after each game version change.', 1),
(2, 1, 'building:building_navel_base:pd-director', 403, 'duplicate_definition', 3, 'accepted', 13, 191, 56, '2026-07-10T10:06:43-04:00', 'Director intentionally supersedes the PD More Arcologies object with hard AI eligibility.', 'Review parent updates, job identities, prerequisites, and designation interactions.', 1);

INSERT INTO object_conflict_member(
    object_conflict_id, object_definition_id, member_role, load_position, differing_fields, notes
) VALUES
(1, 10, 'loser', NULL, 'ai.min_navy_for_wars; ai.min_assault_armies_for_wars', 'Vanilla/reference baseline.'),
(1, 11, 'winner', 116, 'ai.min_navy_for_wars omitted; ai.min_assault_armies_for_wars=0', 'Director winner.'),
(2, 12, 'loser', 66, 'potential; allow; destroy_trigger; job counts', 'PD More Arcologies parent occurrence.'),
(2, 13, 'winner', 116, 'potential; allow; destroy_trigger', 'Director winner.');

INSERT INTO verification_run(
    verification_run_id, run_key, title, run_kind, target_version_id, execution_context_id, tool_item_id, performed_by_actor_id, method_summary, command_or_query, environment_summary, started_at, completed_at, approval_status, reproducibility_status, outcome_code, notes, created_in_change_set_id
) VALUES
(10, 'object-atlas-generation-b605aa0e', 'Object-atlas generation', 'model_generation', 2, 1, 550, 3, 'Regenerate atlas, dependency edges, parent-AI support, and policy matrix.', 'python tools/build_stellar_ai_director_object_atlas.py', 'Captured repository, vanilla, Workshop roots, and playset.', '2026-07-06T00:00:00Z', '2026-07-06T00:10:00Z', 'not_required', 'reproducible', 'passed', 'Counts are bound to captured inputs.', 1),
(11, 'research-capacity-generation-b605aa0e', 'Economic/modeling dataset generation', 'model_generation', 2, 1, 551, 3, 'Regenerate capacity, readiness, benefit, blocker, and consumer-policy datasets.', 'python tools/build_stellar_ai_research_capacity_dataset.py', 'Captured source roots and generated atlas.', '2026-07-09T00:00:00Z', '2026-07-09T00:20:00Z', 'not_required', 'reproducible', 'passed', 'Current extracted blocker artifact has zero data rows.', 1),
(12, 'selected-save-war-analysis-20260710', 'Selected-save observer war-state analysis', 'save_analysis', 2, 2, 552, 3, 'Hash and analyze only manually staged saves with country 0 included as AI.', 'python tools/analyze_stellaris_war_state.py <save> --observer-all-ai', 'human_ai + observe + game_speed 5.', '2026-07-10T10:08:00-04:00', '2026-07-10T10:45:00-04:00', 'approved', 'reproducible', 'passed', 'Diagnostic screens do not expose every engine gate.', 1);

INSERT INTO analysis_run(
    analysis_run_id, run_key, model_item_id, execution_context_id, verification_run_id, repository_snapshot_id, model_version, generator_artifact_id, schema_version, command_or_method, input_fingerprint, started_at, completed_at, outcome_code, reported_row_count, notes, created_in_change_set_id
) VALUES
(1, 'analysis:object-atlas-b605aa0e', 330, 1, 10, 1, '2026-07-06', 48, 'object-atlas-v1', 'build_stellar_ai_director_object_atlas.py', 'repo b605aa0e + playset snapshot 1', '2026-07-06T00:00:00Z', '2026-07-06T00:10:00Z', 'passed', 31211, 'Companion outputs include dependency, parent support, and policy matrices.', 1),
(2, 'analysis:economic-capacity-b605aa0e', 331, 1, 11, 1, '2026-07-09', 40, 'capacity-v2', 'build_stellar_ai_research_capacity_dataset.py', 'atlas + active source roots', '2026-07-09T00:00:00Z', '2026-07-09T00:20:00Z', 'passed', 1333, 'Outputs include 501 jobs, 826 buildings, 547 development rows, 24 plans, 247 roles, and 18 technologies.', 1),
(3, 'analysis:build-plan-consumer-b605aa0e', 332, 1, 11, 1, '2026-07-09', 40, 'consumer-v2', 'build_stellar_ai_research_capacity_dataset.py', 'capacity model + source contracts', '2026-07-09T00:00:00Z', '2026-07-09T00:20:00Z', 'passed', 1093, 'Outputs include 826 readiness rows, 1,924 benefit rows, zero current blocker rows, and 1,093 policy rows.', 1),
(4, 'analysis:observer-war-state-20260710', 333, 2, 12, 1, '2026-07-10', 49, 'war-state-v1', 'analyze_stellaris_war_state.py --observer-all-ai', 'four selected SHA-256 save identities', '2026-07-10T10:08:00-04:00', '2026-07-10T10:45:00-04:00', 'passed', 26, 'Latest save contains 26 regular AI country rows.', 1);

INSERT INTO analysis_run_artifact(
    analysis_run_id, source_artifact_id, artifact_role, dataset_schema_id, is_required, notes
) VALUES
(1, 20, 'input', NULL, 1, NULL),
(1, 21, 'output', 1, 1, NULL),
(1, 22, 'output', 2, 1, NULL),
(1, 23, 'output', 3, 1, NULL),
(1, 24, 'output', 4, 1, NULL),
(1, 48, 'source_code', NULL, 1, NULL),
(2, 21, 'input', 1, 1, NULL),
(2, 25, 'output', 5, 1, NULL),
(2, 26, 'output', 6, 1, NULL),
(2, 27, 'output', 7, 1, NULL),
(2, 28, 'output', 8, 1, NULL),
(2, 29, 'output', 9, 1, NULL),
(2, 30, 'output', 10, 1, NULL),
(2, 40, 'source_code', NULL, 1, NULL),
(3, 26, 'input', 6, 1, NULL),
(3, 31, 'output', 11, 1, NULL),
(3, 32, 'output', 12, 1, NULL),
(3, 33, 'output', 13, 1, NULL),
(3, 34, 'output', 14, 1, NULL),
(3, 40, 'source_code', NULL, 1, NULL),
(3, 47, 'report', NULL, 1, NULL),
(4, 36, 'input', NULL, 1, NULL),
(4, 37, 'input', NULL, 1, NULL),
(4, 38, 'input', NULL, 1, NULL),
(4, 39, 'input', NULL, 1, NULL),
(4, 35, 'report', NULL, 1, NULL),
(4, 49, 'source_code', NULL, 1, NULL);

INSERT INTO artifact_derivation(
    artifact_derivation_id, output_artifact_id, input_artifact_id, process_tool_item_id, verification_run_id, process_run_key, command_or_method, derived_at, rationale, created_in_change_set_id
) VALUES
(20, 21, 20, 550, 10, 'object-atlas-generation-b605aa0e', 'build_stellar_ai_director_object_atlas.py', '2026-07-06T00:10:00Z', 'Playset order is an input to winning-definition classification.', 1),
(21, 22, 21, 550, 10, 'object-atlas-generation-b605aa0e', 'derive reference edges', '2026-07-06T00:10:00Z', 'Dependency edges derive from inventoried definitions.', 1),
(22, 23, 21, 550, 10, 'object-atlas-generation-b605aa0e', 'classify parent AI support', '2026-07-06T00:10:00Z', 'Parent support classifications derive from atlas records.', 1),
(23, 24, 21, 550, 10, 'object-atlas-generation-b605aa0e', 'derive policy matrix', '2026-07-06T00:10:00Z', 'Route policy rows derive from atlas and Director strategy inputs.', 1),
(24, 25, 21, 551, 11, 'research-capacity-generation-b605aa0e', 'build research capacity datasets', '2026-07-09T00:20:00Z', 'Job model derives from active definitions and parser/model policy.', 1),
(25, 26, 21, 551, 11, 'research-capacity-generation-b605aa0e', 'build research capacity datasets', '2026-07-09T00:20:00Z', 'Building model derives from active definitions and job model.', 1),
(26, 31, 26, 551, 11, 'research-capacity-generation-b605aa0e', 'derive readiness', '2026-07-09T00:20:00Z', 'Readiness derives from building gates and source contracts.', 1),
(27, 32, 26, 551, 11, 'research-capacity-generation-b605aa0e', 'derive benefit taxonomy', '2026-07-09T00:20:00Z', 'Benefit rows derive from strategic infrastructure and modifier evidence.', 1),
(28, 34, 31, 551, 11, 'research-capacity-generation-b605aa0e', 'derive consumer policy', '2026-07-09T00:20:00Z', 'Consumer policy derives from readiness, blockers, roles, and benefits.', 1),
(29, 35, 36, 552, 12, 'selected-save-war-analysis-20260710', 'analyze save --observer-all-ai', '2026-07-10T10:45:00-04:00', 'Report summarizes selected fields and interpretation boundaries.', 1);

INSERT INTO analysis_scenario(
    analysis_scenario_id, analysis_run_id, scenario_key, scenario_name, scenario_family, parent_scenario_id, ordinal, assumptions_summary, is_baseline
) VALUES
(1, 2, 'base', 'Base', 'resource_flow', NULL, 1, 'Unconditional/base modeled terms only.', 1),
(2, 2, 'conservative', 'Conservative', 'resource_flow', 1, 2, 'Base plus only conservative conditional terms.', 0),
(3, 2, 'optimistic', 'Optimistic', 'resource_flow', 1, 3, 'Base plus optimistic triggered terms.', 0),
(4, 3, 'current-playset', 'Current captured playset', 'consumer_policy', NULL, 1, 'Use captured winners, readiness gates, and current model policies.', 1);

INSERT INTO analysis_subject(
    analysis_subject_id, analysis_run_id, subject_key, subject_kind, item_id, source_locator_id, parent_subject_id, external_type, external_key, label, status_code, notes
) VALUES
(1, 1, 'object:country_type:default', 'knowledge_item', 132, 33, NULL, NULL, NULL, 'default country type', 'resolved', 'Playset winner stored separately.'),
(2, 2, 'job:low_tech_researcher', 'knowledge_item', 412, 34, NULL, NULL, NULL, 'low_tech_researcher', 'modeled', NULL),
(3, 2, 'building:building_research_lab_1', 'knowledge_item', 134, 35, NULL, NULL, NULL, 'building_research_lab_1', 'modeled', NULL),
(4, 2, 'building:building_navel_base', 'knowledge_item', 403, 36, NULL, NULL, NULL, 'building_navel_base', 'modeled', NULL),
(5, 3, 'consumer:building_research_lab_1', 'knowledge_item', 134, 40, NULL, NULL, NULL, 'Research lab consumer policy', 'conditional', NULL),
(6, 3, 'consumer:building_navel_base', 'knowledge_item', 403, 41, NULL, NULL, NULL, 'Naval base consumer policy', 'conditional', NULL),
(7, 3, 'benefit-class:naval_capacity', 'policy_class', 352, 39, NULL, NULL, NULL, 'Naval capacity benefit class', 'classified', NULL),
(10, 4, 'save:122ac606', 'external_record', NULL, 44, NULL, 'save', '122ac606adf5af27fea60ece60694a79f9d0593704eb586be35aab270287bb7f', 'Stuck Ranulia 2239.08.13', 'analyzed', NULL),
(11, 4, 'save:122ac606:country:0', 'runtime_entity', NULL, 43, 10, 'country', '0', 'United Cevantian Nation / country 0', 'analyzed', 'Observer/all-AI mode includes country 0 as an AI actor.'),
(12, 4, 'save:12f94592', 'external_record', NULL, 53, NULL, 'save', '12f9459277ffa4d51153ab32c5b8d66004d525c1ec2b312f3f05a027916e1556', 'Autosave 2239.07.01', 'analyzed', NULL),
(13, 4, 'save:884b7f75', 'external_record', NULL, 54, NULL, 'save', '884b7f753802ab68765b9abb269d98565367a8ebc5c841618ae6f7f5ab144c4d', 'End save 2234.01.01', 'analyzed', NULL),
(14, 4, 'save:70c29fab', 'external_record', NULL, 55, NULL, 'save', '70c29fab43be693ef7162252fc75890ea2ad76fdf73f1fcffd433ed7fdf55f0a', 'Start save 2232.01.01', 'analyzed', NULL);

INSERT INTO analysis_metric(
    analysis_metric_id, model_item_id, metric_key, metric_name, value_type, unit, aggregation_semantics, dimension_item_type_id, allowed_subject_kind, description, stable_across_runs
) VALUES
(1, 330, 'load_winner', 'Load winner', 'boolean', NULL, 'boolean', NULL, 'knowledge_item', 'Whether this definition is the captured playset winner.', 1),
(2, 330, 'resolution_status', 'Resolution status', 'text', NULL, 'categorical', NULL, 'knowledge_item', 'Playset-specific object resolution status.', 1),
(10, 331, 'resource_output', 'Resource output', 'real', 'modeled_amount', 'additive', 11, NULL, 'Output amount for a resource in a scenario.', 1),
(11, 331, 'resource_upkeep', 'Resource upkeep', 'real', 'modeled_amount', 'additive', 11, NULL, 'Upkeep amount for a resource in a scenario.', 1),
(12, 331, 'research_total', 'Research total', 'real', 'modeled_research', 'additive', NULL, NULL, 'Total research output under a scenario.', 1),
(13, 331, 'job_slots_total', 'Job slots total', 'real', 'jobs', 'set_count', NULL, NULL, 'Modeled jobs supplied by the object.', 1),
(14, 331, 'unresolved_variables', 'Unresolved variables', 'text', NULL, 'categorical', NULL, NULL, 'Generator-reported unresolved variable set or none.', 1),
(20, 332, 'primary_role', 'Primary role', 'text', NULL, 'categorical', NULL, NULL, 'Generated primary role for consumer policy.', 1),
(21, 332, 'primary_role_score', 'Primary role score', 'real', 'score', 'score', NULL, NULL, 'Generated role score.', 1),
(22, 332, 'build_plan_candidate', 'Build-plan candidate', 'boolean', NULL, 'boolean', NULL, NULL, 'Whether the source-backed candidate rules permit consumption.', 1),
(23, 332, 'can_consume_now', 'Can consume now', 'text', NULL, 'categorical', NULL, NULL, 'yes, no, conditional, or not_applicable.', 1),
(24, 332, 'benefit_numeric_rows', 'Numeric benefit rows', 'integer', 'rows', 'set_count', NULL, NULL, 'Number of numeric benefit rows attached to the consumer.', 1),
(30, 333, 'game_date', 'Game date', 'text', NULL, 'identifier', NULL, NULL, 'Serialized game date.', 1),
(31, 333, 'regular_ai_count', 'Regular AI empires', 'integer', 'countries', 'set_count', NULL, NULL, 'Regular AI empire count.', 1),
(32, 333, 'current_war_count', 'Current wars', 'integer', 'wars', 'set_count', NULL, NULL, 'Current serialized war count.', 1),
(33, 333, 'ai_at_war_count', 'AI empires at war', 'integer', 'countries', 'set_count', NULL, NULL, 'Regular AI empires participating in wars.', 1),
(34, 333, 'never_at_war_count', 'Never at war', 'integer', 'countries', 'set_count', NULL, NULL, 'Regular AI empires with no recorded prior war.', 1),
(35, 333, 'native_candidates_after_patch', 'Native candidates after patch', 'integer', 'countries', 'set_count', NULL, NULL, 'Diagnostic modeled candidates after removing two country-type gates.', 1),
(36, 333, 'military_power', 'Military power', 'real', 'power', 'score', NULL, 'runtime_entity', 'Serialized military power.', 1),
(37, 333, 'economy_power', 'Economy power', 'real', 'power', 'score', NULL, 'runtime_entity', 'Serialized economy power.', 1),
(38, 333, 'navy_coverage', 'Navy coverage', 'real', 'ratio', 'ratio', NULL, 'runtime_entity', 'Serialized navy coverage.', 1),
(39, 333, 'embarked_assault_armies_minimum', 'Embarked assault armies minimum', 'integer', 'armies', 'set_count', NULL, 'runtime_entity', 'Conservative embarked assault-army minimum.', 1),
(40, 333, 'casus_belli_count', 'Casus belli count', 'integer', 'casus_belli', 'set_count', NULL, 'runtime_entity', 'Serialized CB count.', 1),
(41, 333, 'legal_hostile_targets', 'Legal hostile targets', 'integer', 'countries', 'set_count', NULL, 'runtime_entity', 'Reachable hostile targets with a CB in the diagnostic model.', 1),
(42, 333, 'strength_viable_targets', 'Strength-viable targets', 'integer', 'countries', 'set_count', NULL, 'runtime_entity', 'Targets passing the 0.55 diagnostic strength screen.', 1),
(43, 333, 'planner_target', 'Planner target', 'text', NULL, 'identifier', NULL, 'runtime_entity', 'Serialized AI planner target.', 1),
(44, 333, 'preparing_war', 'Preparing war', 'boolean', NULL, 'boolean', NULL, 'runtime_entity', 'Whether serialized preparation date indicates active preparation.', 1),
(45, 333, 'at_war', 'At war', 'boolean', NULL, 'boolean', NULL, 'runtime_entity', 'Current war participation.', 1),
(46, 333, 'runtime_observation', 'Runtime observation', 'text', NULL, 'other', NULL, 'runtime_entity', 'User-observed behavior correlated to the save.', 0);

INSERT INTO analysis_value(
    analysis_value_id, analysis_subject_id, analysis_scenario_id, analysis_metric_id, dimension_item_id, ordinal, integer_value, real_value, text_value, boolean_value, evidence_locator_id, confidence_level_id, source_terms, notes
) VALUES
(1, 1, NULL, 1, NULL, 1, NULL, NULL, NULL, 1, 47, 5, 'playset_object_resolution:1', NULL),
(2, 1, NULL, 2, NULL, 1, NULL, NULL, 'resolved', NULL, 47, 5, NULL, NULL),
(10, 2, 1, 10, 143, 1, NULL, 1.0, NULL, NULL, 34, 4, 'base_output_physics_research', NULL),
(11, 2, 1, 10, 144, 1, NULL, 1.0, NULL, NULL, 34, 4, 'base_output_society_research', NULL),
(12, 2, 1, 10, 145, 1, NULL, 1.0, NULL, NULL, 34, 4, 'base_output_engineering_research', NULL),
(13, 2, 1, 11, 413, 1, NULL, 1.0, NULL, NULL, 34, 4, 'base_upkeep_consumer_goods', NULL),
(14, 2, 1, 12, NULL, 1, NULL, 3.0, NULL, NULL, 34, 4, 'base_research_total', NULL),
(15, 2, 1, 14, NULL, 1, NULL, NULL, 'none', NULL, 34, 4, 'unresolved_variables', NULL),
(20, 3, 1, 11, 140, 1, NULL, 2.0, NULL, NULL, 35, 4, 'base_upkeep_energy', NULL),
(21, 3, 1, 14, NULL, 1, NULL, NULL, 'none', NULL, 35, 4, 'unresolved_variables', NULL),
(22, 4, 1, 10, 144, 1, NULL, 18.0, NULL, NULL, 36, 4, 'base_output_society_research', NULL),
(23, 4, 1, 11, 140, 1, NULL, 7.0, NULL, NULL, 36, 4, 'base_upkeep_energy', NULL),
(24, 4, 1, 11, 141, 1, NULL, 6.0, NULL, NULL, 36, 4, 'base_upkeep_minerals', NULL),
(25, 4, 1, 11, 413, 1, NULL, 6.0, NULL, NULL, 36, 4, 'base_upkeep_consumer_goods', NULL),
(26, 4, 1, 12, NULL, 1, NULL, 18.0, NULL, NULL, 36, 4, 'base_research', NULL),
(27, 4, 1, 13, NULL, 1, NULL, 6.0, NULL, NULL, 36, 4, 'job_slots_total', NULL),
(28, 4, 1, 14, NULL, 1, NULL, NULL, 'none', NULL, 36, 4, 'unresolved_variables', NULL),
(30, 5, 4, 20, NULL, 1, NULL, NULL, 'support', NULL, 40, 5, NULL, NULL),
(31, 5, 4, 22, NULL, 1, NULL, NULL, NULL, 1, 40, 5, NULL, NULL),
(32, 5, 4, 23, NULL, 1, NULL, NULL, 'conditional', NULL, 40, 5, NULL, NULL),
(33, 6, 4, 20, NULL, 1, NULL, NULL, 'research_world', NULL, 41, 5, NULL, NULL),
(34, 6, 4, 21, NULL, 1, NULL, 18.0, NULL, NULL, 38, 5, NULL, NULL),
(35, 6, 4, 22, NULL, 1, NULL, NULL, NULL, 1, 41, 5, NULL, NULL),
(36, 6, 4, 23, NULL, 1, NULL, NULL, 'conditional', NULL, 41, 5, NULL, NULL),
(37, 6, 4, 24, NULL, 1, 2, NULL, NULL, NULL, 41, 5, NULL, NULL),
(100, 10, NULL, 30, NULL, 1, NULL, NULL, '2239.08.13', NULL, 43, 5, NULL, NULL),
(101, 10, NULL, 31, NULL, 1, 26, NULL, NULL, NULL, 43, 5, NULL, NULL),
(102, 10, NULL, 32, NULL, 1, 3, NULL, NULL, NULL, 43, 5, NULL, NULL),
(103, 10, NULL, 33, NULL, 1, 4, NULL, NULL, NULL, 43, 5, NULL, NULL),
(104, 10, NULL, 34, NULL, 1, 17, NULL, NULL, NULL, 43, 5, NULL, NULL),
(105, 10, NULL, 35, NULL, 1, 16, NULL, NULL, NULL, 43, 4, NULL, 'Diagnostic modeled candidate count, not declaration proof.'),
(120, 12, NULL, 30, NULL, 1, NULL, NULL, '2239.07.01', NULL, 53, 5, NULL, NULL),
(121, 12, NULL, 31, NULL, 1, 26, NULL, NULL, NULL, 53, 5, NULL, NULL),
(122, 12, NULL, 32, NULL, 1, 3, NULL, NULL, NULL, 53, 5, NULL, NULL),
(123, 12, NULL, 33, NULL, 1, 3, NULL, NULL, NULL, 53, 5, NULL, NULL),
(124, 12, NULL, 34, NULL, 1, 18, NULL, NULL, NULL, 53, 5, NULL, NULL),
(125, 12, NULL, 35, NULL, 1, 17, NULL, NULL, NULL, 53, 4, NULL, 'Diagnostic modeled candidate count, not declaration proof.'),
(140, 13, NULL, 30, NULL, 1, NULL, NULL, '2234.01.01', NULL, 54, 5, NULL, NULL),
(141, 13, NULL, 31, NULL, 1, 27, NULL, NULL, NULL, 54, 5, NULL, NULL),
(142, 13, NULL, 32, NULL, 1, 2, NULL, NULL, NULL, 54, 5, NULL, NULL),
(143, 13, NULL, 33, NULL, 1, 3, NULL, NULL, NULL, 54, 5, NULL, NULL),
(144, 13, NULL, 34, NULL, 1, 21, NULL, NULL, NULL, 54, 5, NULL, NULL),
(145, 13, NULL, 35, NULL, 1, 17, NULL, NULL, NULL, 54, 4, NULL, 'Diagnostic modeled candidate count, not declaration proof.'),
(160, 14, NULL, 30, NULL, 1, NULL, NULL, '2232.01.01', NULL, 55, 5, NULL, NULL),
(161, 14, NULL, 31, NULL, 1, 27, NULL, NULL, NULL, 55, 5, NULL, NULL),
(162, 14, NULL, 32, NULL, 1, 1, NULL, NULL, NULL, 55, 5, NULL, NULL),
(163, 14, NULL, 33, NULL, 1, 3, NULL, NULL, NULL, 55, 5, NULL, NULL),
(164, 14, NULL, 34, NULL, 1, 23, NULL, NULL, NULL, 55, 5, NULL, NULL),
(165, 14, NULL, 35, NULL, 1, 18, NULL, NULL, NULL, 55, 4, NULL, 'Diagnostic modeled candidate count, not declaration proof.'),
(180, 11, NULL, 36, NULL, 1, NULL, 15615.25781, NULL, NULL, 43, 5, NULL, NULL),
(181, 11, NULL, 37, NULL, 1, NULL, 9543.76367, NULL, NULL, 43, 5, NULL, NULL),
(182, 11, NULL, 38, NULL, 1, NULL, 1.0, NULL, NULL, 43, 5, NULL, NULL),
(183, 11, NULL, 39, NULL, 1, 0, NULL, NULL, NULL, 43, 5, NULL, 'Embarked minimum; landed assault armies may be omitted.'),
(184, 11, NULL, 40, NULL, 1, 14, NULL, NULL, NULL, 43, 5, NULL, NULL),
(185, 11, NULL, 41, NULL, 1, 2, NULL, NULL, NULL, 43, 4, NULL, NULL),
(186, 11, NULL, 42, NULL, 1, 2, NULL, NULL, NULL, 43, 4, NULL, 'Uses Director 0.55 multiplier as a diagnostic screen.'),
(187, 11, NULL, 43, NULL, 1, NULL, NULL, '4294967295', NULL, 43, 5, NULL, NULL),
(188, 11, NULL, 44, NULL, 1, NULL, NULL, NULL, 0, 43, 5, NULL, NULL),
(189, 11, NULL, 45, NULL, 1, NULL, NULL, NULL, 0, 43, 5, NULL, NULL),
(190, 11, NULL, 46, NULL, 1, NULL, NULL, 'Science ship repeatedly entered a closed-border Pobbma route, went MIA/emergency-recalled, and retried.', NULL, 52, 3, NULL, 'User observation; not a directly serialized parser field.');

INSERT INTO analysis_gate(
    analysis_gate_id, analysis_subject_id, analysis_scenario_id, gate_kind, gate_key, target_item_id, phase_code, state_code, is_hard, expression_text, evidence_locator_id, notes
) VALUES
(1, 5, 4, 'prerequisite', 'tech_basic_science_lab_1', 146, 'after_prerequisite', 'conditional', 1, 'has_technology = tech_basic_science_lab_1', 37, NULL),
(2, 5, 4, 'potential', 'building_research_lab_1.potential', NULL, 'conditional_scripted', 'conditional', 1, 'source potential block', 37, NULL),
(3, 5, 4, 'allow', 'building_research_lab_1.allow', NULL, 'conditional_scripted', 'conditional', 1, 'source allow block', 37, NULL),
(4, 6, 4, 'prerequisite', 'tech_planetary_defenses', 417, 'after_prerequisite', 'conditional', 1, 'has_technology = tech_planetary_defenses', 38, NULL),
(5, 6, 4, 'safety', 'staid_naval_capacity_expansion_ready', 428, 'conditional_scripted', 'conditional', 1, 'owner = { staid_naval_capacity_expansion_ready = yes }', 56, 'Research-designated worlds are excluded.'),
(6, 6, 4, 'consumer', 'build_plan_candidate', NULL, 'after_prerequisite', 'satisfied', 1, 'build_plan_candidate = yes', 41, NULL);

INSERT INTO analysis_policy(
    analysis_policy_id, analysis_run_id, analysis_subject_id, analysis_metric_id, dimension_item_id, policy_kind, decision_code, policy_status, formula_or_policy_text, numeric_parameter, can_consume_code, fallback_subject_id, fallback_item_id, confidence_level_id, evidence_locator_id, next_action, supersedes_policy_id, created_in_change_set_id
) VALUES
(1, 3, 5, NULL, NULL, 'readiness', 'gated_scorable_with_conditions', 'active', 'Emit only after prerequisite and scripted potential/allow gates pass.', NULL, 'conditional', NULL, 423, 5, 40, 'Revalidate fallback quality and source winner after source/playset changes.', NULL, 1),
(2, 3, 5, NULL, NULL, 'replacement', 'no_proactive_replacement_static_evidence', 'active', 'Treat fallback as permanent or no-regret; do not assume proactive demolition/refactoring.', NULL, 'not_applicable', NULL, 423, 5, 40, 'Require a separate source-backed replacement mechanism or runtime proof before temporary fallback policy.', NULL, 1),
(3, 3, 6, NULL, NULL, 'readiness', 'gated_scorable_with_conditions', 'active', 'Require tech_planetary_defenses, Director readiness trigger, and non-research designation before AI construction.', NULL, 'conditional', NULL, NULL, 5, 41, 'Review parent PD object and job identities after updates.', NULL, 1),
(4, 3, 7, NULL, NULL, 'classification', 'numeric_modifier_preserved_not_direct_consumer_score', 'active', 'Preserve numeric naval-capacity terms and map them only through an explicit source-backed consumer rule; do not invent a generic score.', NULL, 'no', NULL, NULL, 4, 39, 'Keep benefit evidence queryable while consumer mapping remains explicit.', NULL, 1);

INSERT INTO analysis_issue(
    analysis_issue_id, analysis_run_id, analysis_subject_id, issue_type, issue_key, status_code, severity_code, priority, exact_missing_evidence, resolution_summary, resolution_policy_id, question_id, evidence_locator_id, notes
) VALUES
(1, 3, 7, 'benefit_formula_status', 'naval_capacity', 'accepted', 'info', 30, NULL, 'Numeric evidence is retained; direct construction scoring is intentionally disallowed without explicit policy.', 4, NULL, 39, NULL),
(2, 4, 11, 'hidden_engine_causation', 'war_planner_target_absent', 'open', 'warning', 90, 'A controlled comparison or engine-exposed trace connecting script-visible gates to target selection and declaration.', 'Serialized state is known, but causal ordering among hidden gates is not.', NULL, NULL, 43, NULL),
(3, 4, 11, 'runtime_pathing', 'science_ship_closed_border_mia_loop', 'open', 'warning', 70, 'A reproducible pathing test with exact borders, orders, logs, and comparison build.', 'User observation is recorded but not yet causally diagnosed.', NULL, NULL, 52, 'May be separate from the war-planning defect.');

INSERT INTO validation_finding(
    validation_finding_id, verification_run_id, finding_key, category_code, severity_code, status_code, primary_item_id, evidence_locator_id, finding_summary, expected_text, actual_text, remediation, regression_key, first_observed_at, resolved_at, created_in_change_set_id
) VALUES
(1, 10, 'active-winning-building-coverage', 'coverage', 'info', 'resolved', 330, 50, 'All 648 active-stack winning building IDs were present in the generated building model.', '648 modeled', '648 modeled; 0 missing', 'Retain as a regeneration regression check.', 'object-atlas-building-coverage', '2026-07-09T00:00:00Z', '2026-07-09T00:00:00Z', 1),
(2, 11, 'current-blocker-accounting-zero', 'modeling', 'info', 'resolved', 332, 42, 'Current extracted blocker-accounting dataset has zero data rows.', '0 open blocker rows', '0 rows; 9-column schema retained', 'Regenerate and re-open issues when source/model changes introduce new blockers.', 'modeling-blocker-count', '2026-07-09T00:00:00Z', '2026-07-09T00:00:00Z', 1),
(3, 11, 'wide-resource-scenario-columns', 'modeling', 'info', 'resolved', 331, 51, 'Wide CSV columns form controlled scenario × direction × resource dimensions that map to typed analysis facts.', 'Typed normalized representation available', 'analysis_metric + analysis_value with resource dimension', 'Keep complete external schemas and normalize only selected facts.', 'resource-scenario-normalization', '2026-07-10T00:00:00Z', '2026-07-10T00:00:00Z', 1),
(4, 12, 'hidden-war-causation-unproven', 'save_state', 'warning', 'open', 111, 43, 'Selected saves show viable targets and no planner target for country 0, but do not expose every engine declaration gate.', 'Causal proof only when instrumented/controlled', 'Serialized state and diagnostic screens only', 'Keep claims uncertain and run a bounded comparison if approved.', 'war-hidden-causation', '2026-07-10T00:00:00Z', NULL, 1),
(5, 12, 'science-ship-mia-loop', 'runtime_log', 'warning', 'open', 124, 52, 'User observed a repeated closed-border MIA/retry loop correlated to the latest save.', 'No repeated invalid route', 'Observed repeated invalid route/retry', 'Investigate pathing separately with exact logs and reproducible setup.', 'science-ship-closed-border-loop', '2026-07-10T00:00:00Z', NULL, 1);

INSERT INTO claim(
    claim_id, claim_type_id, primary_item_id, statement, context, epistemic_note, supersedes_claim_id, lifecycle_state_id, created_by_actor_id, created_at, created_in_change_set_id, retired_in_change_set_id
) VALUES
(20, 2, 320, 'A definition is a winning definition only relative to a captured playset snapshot and its load order.', 'Active-stack conflict analysis.', 'Repository or vanilla occurrence alone is not a winner claim.', NULL, 1, 2, '2026-07-10T17:00:00Z', 1, NULL),
(21, 2, 331, 'The current wide modeling CSVs primarily encode controlled scenario, flow-direction, and resource dimensions rather than hundreds of unrelated attributes.', 'Capacity/modeling schema review.', 'The database catalogs every external column and normalizes selected facts through registered metrics.', NULL, 1, 2, '2026-07-10T17:00:00Z', 1, NULL),
(22, 6, 333, 'Selected save analysis can prove serialized state in a hashed save but cannot by itself prove hidden engine causation.', 'Observer war-state diagnosis.', 'Diagnostic thresholds and user observations remain explicitly bounded.', NULL, 1, 2, '2026-07-10T17:00:00Z', 1, NULL),
(23, 3, 301, 'The captured playset places Gigas at 62, ESC NEXT at 70, NSC3 at 71, Starbase Extended at 72, Universal Resource Patch at 115, and Stellar AI Director at 116.', 'Captured active playset snapshot.', 'This is a snapshot fact, not proof of later live launcher state.', NULL, 1, 2, '2026-07-10T17:00:00Z', 1, NULL),
(24, 3, 301, 'Spacefleet Tactica and Stellar AI are reference/parity sources but are absent from the captured active playset.', 'Captured active playset snapshot.', 'Absence is snapshot-specific.', NULL, 1, 2, '2026-07-10T17:00:00Z', 1, NULL);

INSERT INTO claim_item(
    claim_id, item_id, role_code, notes
) VALUES
(20, 320, 'context', NULL),
(20, 132, 'example_object', NULL),
(20, 403, 'example_object', NULL),
(21, 331, 'subject', NULL),
(21, 505, 'source_schema', NULL),
(21, 506, 'source_schema', NULL),
(21, 507, 'source_schema', NULL),
(22, 333, 'subject', NULL),
(22, 111, 'affected_subsystem', NULL),
(23, 302, 'member', NULL),
(23, 304, 'member', NULL),
(23, 303, 'member', NULL),
(23, 305, 'member', NULL),
(23, 306, 'member', NULL),
(23, 301, 'member', NULL),
(24, 310, 'absent_reference', NULL),
(24, 311, 'absent_reference', NULL);

INSERT INTO claim_assessment(
    claim_assessment_id, claim_id, version_span_id, assessment_state_id, confidence_level_id, verification_run_id, execution_context_id, assessed_by_actor_id, assessed_at, basis_summary, reverify_after, is_current, supersedes_assessment_id, created_in_change_set_id
) VALUES
(20, 20, 3, 1, 5, 10, 1, 2, '2026-07-10T17:05:00Z', 'Playset resolution tables and captured load order distinguish definition occurrence from winner.', NULL, 1, NULL, 1),
(21, 21, 3, 1, 5, 11, 1, 2, '2026-07-10T17:05:00Z', 'Complete external headers show repeated scenario/output/upkeep/resource naming patterns.', NULL, 1, NULL, 1),
(22, 22, 3, 1, 5, 12, 2, 2, '2026-07-10T17:05:00Z', 'Save report explicitly states the interpretation boundary.', NULL, 1, NULL, 1),
(23, 23, 3, 1, 5, 10, 1, 2, '2026-07-10T17:05:00Z', 'Captured JSON contains exact member positions.', NULL, 1, NULL, 1),
(24, 24, 3, 1, 5, 10, 1, 2, '2026-07-10T17:05:00Z', 'Captured parity_reference_mods map records both as absent.', NULL, 1, NULL, 1);

INSERT INTO claim_evidence(
    claim_evidence_id, claim_id, evidence_locator_id, evidence_stance_id, directness_rank, strength_rank, verification_run_id, interpretation, created_in_change_set_id
) VALUES
(22, 20, 47, 1, 5, 5, 10, 'Captured load position context.', 1),
(23, 20, 33, 1, 4, 5, 10, 'Object occurrence inventory supports the playset-specific resolution distinction.', 1),
(24, 21, 34, 1, 5, 5, 11, 'Job schema and selected row exhibit normalized resource dimensions.', 1),
(25, 21, 35, 1, 5, 5, 11, 'Building schema and selected row exhibit normalized resource dimensions.', 1),
(26, 21, 51, 1, 4, 5, 11, 'Generator schema and count history support the dimensional interpretation.', 1),
(27, 22, 43, 1, 5, 5, 12, 'Save-derived evidence states the interpretation boundary directly.', 1),
(28, 22, 52, 3, 4, 3, 12, 'The runtime observation is correlated evidence, not a parsed save field.', 1),
(29, 23, 31, 1, 5, 5, 10, 'Captured JSON gives required-parent positions.', 1),
(30, 23, 47, 1, 5, 5, 10, 'Captured JSON gives the Director position.', 1),
(31, 24, 30, 1, 5, 5, 10, 'Captured parity-reference map records both references as absent.', 1);

INSERT INTO open_question(
    question_id, question_key, primary_item_id, question_text, uncertainty_reason, target_version_id, status_code, priority, owner_actor_id, resolution_claim_id, next_review_at, created_in_change_set_id, closed_in_change_set_id
) VALUES
(10, 'question:current-4.4.5-native-war-gates', 132, 'Does the exact current 4.4.5 vanilla default country type still contain the same 0.5 navy and six-assault-army pre-planner gates as the 4.4.4 provenance reference?', 'The Director source comment cites Pegasus 4.4.4 while the project target is 4.4.5; the full-object override must be diffed against the exact local current file.', 2, 'open', 95, 2, NULL, '2026-07-15T00:00:00Z', 1, NULL);

INSERT INTO question_item(
    question_id, item_id, role_code, notes
) VALUES
(10, 132, 'subject', NULL),
(10, 426, 'field', NULL),
(10, 427, 'field', NULL),
(10, 519, 'implementation', NULL),
(10, 520, 'authoritative_source', NULL);

INSERT INTO question_evidence(
    question_id, evidence_locator_id, relevance_code, notes
) VALUES
(10, 45, 'current_override', 'Director source and provenance comment.'),
(10, 46, 'required_comparison', 'Exact 4.4.5 vanilla file must be diffed.');

INSERT INTO item_relation(
    item_relation_id, source_item_id, relation_type_id, target_item_id, version_span_id, confidence_level_id, risk_level_id, source_claim_id, rationale, impact_explanation, review_action, validation_action, is_current, created_in_change_set_id, retired_in_change_set_id
) VALUES
(60, 301, 5, 302, 1, 4, 3, NULL, 'Director depends on Gigas objects, resources, and progression surfaces.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review Gigas source/atlas winners and every Director override.', 'Regenerate atlas/model and validate Gigas references.', 1, 1, NULL),
(61, 301, 5, 303, 1, 4, 3, NULL, 'Director depends on NSC3 hull and fleet progression surfaces.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review NSC3 source and ship-design blockers.', 'Regenerate atlas and validate references.', 1, 1, NULL),
(62, 301, 5, 304, 1, 4, 3, NULL, 'Director depends on ESC component and resource surfaces.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review component template keys and resource readiness.', 'Validate ESC references and conflicts.', 1, 1, NULL),
(63, 301, 5, 305, 1, 4, 3, NULL, 'Director depends on Starbase Extended source surfaces.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review starbase modules/buildings and excluded Waystation surfaces.', 'Run conflict and scope review.', 1, 1, NULL),
(64, 301, 5, 306, 1, 4, 3, NULL, 'Director assumes the active Universal Resource Patch integration.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review resource keys and load order.', 'Validate current resource coverage.', 1, 1, NULL),
(65, 301, 12, 307, 1, 4, 3, NULL, 'Director contains targeted Planetary Diversity compatibility.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review PD objects, zones, districts, and decisions.', 'Run active winner/conflict review.', 1, 1, NULL),
(66, 301, 12, 308, 1, 4, 4, NULL, 'Director fully overrides selected PD More Arcologies buildings.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Diff parent objects and jobs.', 'Validate conflict winner and prerequisites.', 1, 1, NULL),
(67, 301, 1, 320, 1, 4, 2, 23, 'Director is a member of the captured active playset.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review snapshot membership and position.', 'Refresh playset before current launch claims.', 1, 1, NULL),
(68, 330, 18, 320, 1, 4, 3, 20, 'Object-atlas winner classification is generated from the captured playset.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Refresh playset input before regeneration.', 'Compare winner counts and conflicts.', 1, 1, NULL),
(69, 331, 5, 330, 1, 4, 3, 21, 'Economic model consumes object-atlas winners and references.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Regenerate atlas first.', 'Validate all generated datasets.', 1, 1, NULL),
(70, 332, 5, 331, 1, 4, 3, 21, 'Consumer policy depends on capacity and benefit modeling.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review model changes and issue queues.', 'Regenerate readiness/policy outputs.', 1, 1, NULL),
(71, 333, 5, 320, 1, 4, 3, 22, 'Observer interpretation depends on the captured playset context.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Record exact playset and version for every save.', 'Reject context-free runtime claims.', 1, 1, NULL),
(72, 403, 15, 417, 1, 4, 3, NULL, 'building_navel_base requires tech_planetary_defenses.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review prerequisite and availability.', 'Check readiness gate and source definition.', 1, 1, NULL),
(73, 403, 15, 428, 1, 4, 3, NULL, 'AI construction is gated by staid_naval_capacity_expansion_ready.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review trigger definition and callers.', 'Validate scope and hard gate.', 1, 1, NULL),
(74, 403, 7, 352, 1, 4, 3, NULL, 'Naval administration contributes naval-capacity strategic benefit.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review benefit terms and consumer policy.', 'Do not invent a direct score.', 1, 1, NULL),
(75, 132, 4, 519, 1, 4, 4, NULL, 'The active override is implemented in the Director country-type file.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Diff full object against current vanilla.', 'Run source and active-winner validation.', 1, 1, NULL),
(76, 403, 4, 521, 1, 4, 3, NULL, 'The winning override is implemented in the Director PD hard-gate file.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review parent changes and hard gates.', 'Run conflict/static validation.', 1, 1, NULL),
(77, 501, 13, 550, 1, 4, 2, NULL, 'Object-atlas CSV is produced by the object-atlas generator.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review generator/source inputs.', 'Regenerate and compare schema/counts.', 1, 1, NULL),
(78, 506, 13, 551, 1, 4, 2, NULL, 'Building model CSV is produced by the research-capacity generator.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Review generator policy and atlas inputs.', 'Regenerate and validate row/schema counts.', 1, 1, NULL),
(79, 515, 13, 552, 1, 4, 2, NULL, 'Selected-save report is produced by the war-state analyzer plus explicit user observation.', 'A change can propagate through this typed dependency, so the connected source, winner, model, or runtime context must be revalidated.', 'Separate parsed fields from observation.', 'Verify save hashes and extraction mode.', 1, 1, NULL);

INSERT INTO relation_evidence(
    item_relation_id, evidence_locator_id, evidence_stance_id, strength_rank, interpretation
) VALUES
(60, 31, 1, 5, 'Required parent map.'),
(66, 56, 1, 5, 'Director override source.'),
(67, 47, 1, 5, 'Captured position.'),
(68, 32, 1, 5, 'Object-atlas schema.'),
(69, 51, 1, 4, 'Generator chain.'),
(70, 41, 1, 4, 'Consumer-policy row.'),
(71, 43, 1, 5, 'Save context.'),
(72, 36, 1, 5, 'Building model prerequisite.'),
(73, 56, 1, 5, 'Source hard gate.'),
(74, 39, 1, 4, 'Benefit row.'),
(75, 45, 1, 5, 'Director country-type source.'),
(76, 56, 1, 5, 'Director building source.'),
(77, 50, 1, 5, 'Atlas generation and coverage.'),
(78, 51, 1, 5, 'Model output counts.'),
(79, 43, 1, 5, 'Selected-save report.');


-- ---------------------------------------------------------------------------
-- L. Future extension demonstration: a new typed war-planning sidecar
-- ---------------------------------------------------------------------------
-- This table is deliberately created outside the foundational schema to show that a
-- newly modeled mechanic can add typed, constrained detail without changing unrelated
-- core tables. In production, ship this as a numbered migration.

CREATE TABLE ext_war_planning_mechanic_detail (
    mechanic_item_id INTEGER NOT NULL REFERENCES mechanic(item_id) ON DELETE CASCADE,
    version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT,
    declaration_gate_summary TEXT NOT NULL,
    script_visible_inputs TEXT NOT NULL,
    hidden_engine_boundary TEXT NOT NULL,
    required_runtime_proof TEXT NOT NULL,
    basis_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT,
    created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT,
    PRIMARY KEY(mechanic_item_id, version_span_id)
) STRICT;

INSERT INTO ext_war_planning_mechanic_detail(
    mechanic_item_id, version_span_id, declaration_gate_summary,
    script_visible_inputs, hidden_engine_boundary, required_runtime_proof,
    basis_claim_id, created_in_change_set_id
) VALUES
(124, 3,
 'Claims, casus belli, war goals, personality, relative strength, and readiness are review surfaces; the complete declaration gate is not asserted.',
 'Country types; personalities; claim/CB/war-goal eligibility and weights; relevant defines; fleet/economic readiness.',
 'The final engine decision and ordering among hidden gates remain unresolved.',
 'A named controlled run with exact version/playset, source winners, logs, save state, and comparison against a stated hypothesis.',
 11, 1);

COMMIT;

-- ---------------------------------------------------------------------------
-- EXECUTABLE QUERY EXAMPLES
-- ---------------------------------------------------------------------------
-- Each query starts with a params CTE so it can be pasted into sqlite3, Python, or
-- another ordinary SQLite client with only the canonical key/version changed.

-- Q1. Everything known about a mechanic for a target version.
-- The result is intentionally row-oriented: callers can group by record_kind while
-- preserving ordinary relational output instead of receiving an opaque JSON document.
WITH params(mechanic_key, version_label) AS (
    VALUES ('mechanic:economic-plans', '4.4.5')
), target AS (
    SELECT
        ki.item_id, ki.item_type_id, ki.canonical_key, ki.display_name, ki.summary,
        gv.game_version_id, gv.version_label
    FROM params p
    JOIN knowledge_item ki ON ki.canonical_key = p.mechanic_key
    JOIN game_version gv ON gv.version_label = p.version_label
), related_claims AS (
    SELECT c.claim_id
    FROM target t
    JOIN claim c ON c.primary_item_id = t.item_id
    UNION
    SELECT ci.claim_id
    FROM target t
    JOIN claim_item ci ON ci.item_id = t.item_id
), related_questions AS (
    SELECT q.question_id
    FROM target t
    JOIN open_question q ON q.primary_item_id = t.item_id
    UNION
    SELECT qi.question_id
    FROM target t
    JOIN question_item qi ON qi.item_id = t.item_id
), knowledge_rows AS (
    SELECT
        'mechanic' AS record_kind,
        t.canonical_key AS record_key,
        t.display_name AS title,
        'catalogued' AS state,
        NULL AS confidence,
        'identity' AS relationship_or_role,
        t.summary AS detail,
        'target_version=' || t.version_label AS evidence_or_action
    FROM target t

    UNION ALL

    SELECT
        'item_version_status',
        printf('item_version_status:%d', ivs.item_version_status_id),
        t.display_name,
        ivs.status_code,
        cl.confidence_code,
        ast.state_code,
        ivs.basis_summary,
        COALESCE(el.label || ' — ' || el.evidence_summary, 'No locator attached')
    FROM target t
    JOIN item_version_status ivs ON ivs.item_id = t.item_id AND ivs.is_current = 1
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = ivs.version_span_id
     AND vsv.game_version_id = t.game_version_id
    JOIN assessment_state ast ON ast.assessment_state_id = ivs.assessment_state_id
    JOIN confidence_level cl ON cl.confidence_level_id = ivs.confidence_level_id
    LEFT JOIN evidence_locator el ON el.evidence_locator_id = ivs.evidence_locator_id

    UNION ALL

    SELECT
        'claim',
        printf('claim:%d', c.claim_id),
        c.statement,
        ast.state_code,
        cl.confidence_code,
        COALESCE(GROUP_CONCAT(DISTINCT ci.role_code), 'primary_item'),
        ca.basis_summary,
        printf('support=%d; contradict=%d; reverify_after=%s',
               COALESCE(ces.supporting_count, 0),
               COALESCE(ces.contradicting_count, 0),
               COALESCE(ca.reverify_after, 'not scheduled'))
    FROM target t
    JOIN related_claims rc
    JOIN claim c ON c.claim_id = rc.claim_id
    JOIN claim_assessment ca ON ca.claim_id = c.claim_id AND ca.is_current = 1
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = ca.version_span_id
     AND vsv.game_version_id = t.game_version_id
    JOIN assessment_state ast ON ast.assessment_state_id = ca.assessment_state_id
    JOIN confidence_level cl ON cl.confidence_level_id = ca.confidence_level_id
    LEFT JOIN claim_item ci ON ci.claim_id = c.claim_id AND ci.item_id = t.item_id
    LEFT JOIN v_claim_evidence_summary ces ON ces.claim_id = c.claim_id
    GROUP BY c.claim_id, c.statement, ast.state_code, cl.confidence_code,
             ca.basis_summary, ces.supporting_count, ces.contradicting_count,
             ca.reverify_after

    UNION ALL

    SELECT
        'relationship',
        printf('item_relation:%d', ir.item_relation_id),
        other.display_name,
        'current',
        cl.confidence_code,
        CASE
          WHEN ir.source_item_id = t.item_id THEN rt.type_code || ' ->'
          ELSE '<- ' || COALESCE(rt.inverse_name, rt.type_name)
        END,
        ir.rationale || ' ' || ir.impact_explanation,
        trim(COALESCE(ir.review_action, '') || CASE WHEN ir.validation_action IS NULL THEN '' ELSE ' | ' || ir.validation_action END, ' |')
    FROM target t
    JOIN item_relation ir ON (ir.source_item_id = t.item_id OR ir.target_item_id = t.item_id) AND ir.is_current = 1
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = ir.version_span_id
     AND vsv.game_version_id = t.game_version_id
    JOIN relation_type rt ON rt.relation_type_id = ir.relation_type_id
    JOIN confidence_level cl ON cl.confidence_level_id = ir.confidence_level_id
    JOIN knowledge_item other
      ON other.item_id = CASE WHEN ir.source_item_id = t.item_id THEN ir.target_item_id ELSE ir.source_item_id END

    UNION ALL

    SELECT
        'implementation_reference',
        printf('implementation_reference:%d', ref.implementation_reference_id),
        ex.display_name,
        ref.reference_kind,
        NULL,
        CASE WHEN ref.is_preferred = 1 THEN 'preferred' ELSE 'reference' END,
        ref.rationale,
        COALESCE(el.label || ' — ' || el.evidence_summary, ex.canonical_key)
    FROM target t
    JOIN implementation_reference ref ON ref.topic_item_id = t.item_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = ref.version_span_id
     AND vsv.game_version_id = t.game_version_id
    JOIN knowledge_item ex ON ex.item_id = ref.example_item_id
    LEFT JOIN evidence_locator el ON el.evidence_locator_id = ref.evidence_locator_id

    UNION ALL

    SELECT
        'open_question',
        'question:' || q.question_key,
        q.question_text,
        q.status_code,
        NULL,
        'priority=' || q.priority,
        q.uncertainty_reason,
        COALESCE('next_review_at=' || q.next_review_at, 'No review date')
    FROM target t
    JOIN related_questions rq
    JOIN open_question q ON q.question_id = rq.question_id

    UNION ALL

    SELECT
        'tool_route',
        printf('tool_route:%d', tr.tool_route_id),
        tool_item.display_name,
        CASE WHEN tr.is_active = 1 THEN 'active' ELSE 'inactive' END,
        NULL,
        itt.task_code,
        tr.instructions,
        COALESCE(tc.invocation_template, tool.default_invocation, 'Invocation depends on the target locator')
    FROM target t
    JOIN tool_route tr
      ON tr.is_active = 1
     AND (tr.target_item_id = t.item_id OR tr.target_item_type_id = t.item_type_id)
    LEFT JOIN v_version_span_version vsv
      ON vsv.version_span_id = tr.version_span_id
     AND vsv.game_version_id = t.game_version_id
    JOIN tool_capability tc ON tc.tool_capability_id = tr.tool_capability_id
    JOIN tool ON tool.item_id = tc.tool_item_id
    JOIN knowledge_item tool_item ON tool_item.item_id = tool.item_id
    JOIN investigation_task_type itt ON itt.investigation_task_type_id = tc.investigation_task_type_id
    WHERE tr.version_span_id IS NULL OR vsv.game_version_id IS NOT NULL
)
SELECT record_kind, record_key, title, state, confidence,
       relationship_or_role, detail, evidence_or_action
FROM knowledge_rows
ORDER BY
    CASE record_kind
      WHEN 'mechanic' THEN 1
      WHEN 'item_version_status' THEN 2
      WHEN 'claim' THEN 3
      WHEN 'relationship' THEN 4
      WHEN 'implementation_reference' THEN 5
      WHEN 'open_question' THEN 6
      WHEN 'tool_route' THEN 7
      ELSE 8
    END,
    record_key;

-- Q2. Evidence supporting and contradicting one claim, with full provenance/retrieval data.
WITH params(claim_id) AS (VALUES (10))
SELECT
    c.claim_id,
    c.statement,
    es.stance_code,
    ce.directness_rank,
    ce.strength_rank,
    el.label AS evidence_label,
    ss.system_name AS source_system,
    est.type_code AS source_type,
    sa.title AS artifact_title,
    sa.uri_or_path,
    sa.game_version_id,
    el.relative_path,
    el.line_start,
    el.line_end,
    el.symbol_or_object_key,
    el.record_set,
    el.record_key,
    el.timestamp_start,
    el.timestamp_end,
    el.game_date,
    el.evidence_summary,
    el.retrieval_instructions,
    ce.interpretation
FROM params p
JOIN claim c ON c.claim_id = p.claim_id
JOIN claim_evidence ce ON ce.claim_id = c.claim_id
JOIN evidence_stance es ON es.evidence_stance_id = ce.evidence_stance_id
JOIN evidence_locator el ON el.evidence_locator_id = ce.evidence_locator_id
JOIN source_artifact sa ON sa.source_artifact_id = el.source_artifact_id
JOIN source_system ss ON ss.source_system_id = sa.source_system_id
JOIN evidence_source_type est ON est.evidence_source_type_id = ss.evidence_source_type_id
ORDER BY CASE es.stance_code WHEN 'supports' THEN 1 WHEN 'contradicts' THEN 2 WHEN 'qualifies' THEN 3 ELSE 4 END,
         ce.strength_rank DESC;

-- Q3. Knowledge requiring re-verification for the current primary target.
SELECT
    claim_id, primary_item_key, current_state, confidence_code,
    target_version, reason_code, reverify_after, statement
FROM v_reverification_queue
WHERE requires_reverification = 1
ORDER BY
    CASE current_state
      WHEN 'contradicted' THEN 1 WHEN 'stale' THEN 2 WHEN 'unknown' THEN 3 WHEN 'uncertain' THEN 4 ELSE 5
    END,
    claim_id;

-- Q4. Direct and transitive consequences of changing a field, including the path.
WITH RECURSIVE
params(start_key, version_label, max_depth) AS (
    VALUES ('field:economic_plan.weight', '4.4.5', 8)
), start_item AS (
    SELECT ki.item_id, ki.canonical_key, gv.game_version_id
    FROM params p
    JOIN knowledge_item ki ON ki.canonical_key = p.start_key
    JOIN game_version gv ON gv.version_label = p.version_label
), impact(
    start_item_id, affected_item_id, depth, path_item_ids, path_text,
    relation_path, max_risk_rank, review_actions, validation_actions
) AS (
    SELECT
        s.item_id,
        arc.affected_item_id,
        1,
        printf('/%d/%d/', s.item_id, arc.affected_item_id),
        s.canonical_key || ' -> ' || affected.canonical_key,
        arc.relation_type_code,
        rl.rank_value,
        COALESCE(arc.review_action, ''),
        COALESCE(arc.validation_action, '')
    FROM start_item s
    JOIN v_impact_arc arc ON arc.changed_item_id = s.item_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = arc.version_span_id
     AND vsv.game_version_id = s.game_version_id
    JOIN knowledge_item affected ON affected.item_id = arc.affected_item_id
    JOIN risk_level rl ON rl.risk_level_id = arc.risk_level_id

    UNION ALL

    SELECT
        i.start_item_id,
        arc.affected_item_id,
        i.depth + 1,
        i.path_item_ids || printf('%d/', arc.affected_item_id),
        i.path_text || ' -> ' || affected.canonical_key,
        i.relation_path || ' / ' || arc.relation_type_code,
        MAX(i.max_risk_rank, rl.rank_value),
        trim(i.review_actions || CASE WHEN arc.review_action IS NULL OR arc.review_action = '' THEN '' ELSE ' | ' || arc.review_action END, ' |'),
        trim(i.validation_actions || CASE WHEN arc.validation_action IS NULL OR arc.validation_action = '' THEN '' ELSE ' | ' || arc.validation_action END, ' |')
    FROM impact i
    JOIN params p
    JOIN start_item s ON s.item_id = i.start_item_id
    JOIN v_impact_arc arc ON arc.changed_item_id = i.affected_item_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = arc.version_span_id
     AND vsv.game_version_id = s.game_version_id
    JOIN knowledge_item affected ON affected.item_id = arc.affected_item_id
    JOIN risk_level rl ON rl.risk_level_id = arc.risk_level_id
    WHERE i.depth < p.max_depth
      AND instr(i.path_item_ids, printf('/%d/', arc.affected_item_id)) = 0
), ranked AS (
    SELECT
        i.*,
        ROW_NUMBER() OVER (
            PARTITION BY affected_item_id
            ORDER BY depth ASC, max_risk_rank DESC, path_text ASC
        ) AS preferred_path
    FROM impact i
)
SELECT
    r.depth,
    affected.canonical_key AS affected_item,
    it.type_code AS affected_type,
    r.max_risk_rank,
    r.path_text,
    r.relation_path,
    r.review_actions,
    r.validation_actions
FROM ranked r
JOIN knowledge_item affected ON affected.item_id = r.affected_item_id
JOIN item_type it ON it.item_type_id = affected.item_type_id
WHERE r.preferred_path = 1
ORDER BY r.depth, r.max_risk_rank DESC, affected.canonical_key;

-- Q5. Explain the shortest relationship path between two items (undirected discovery).
WITH RECURSIVE
params(from_key, to_key, version_label, max_depth) AS (
    VALUES ('field:economic_plan.weight', 'subsystem:war-planning', '4.4.5', 8)
), endpoints AS (
    SELECT
        f.item_id AS from_item_id,
        t.item_id AS to_item_id,
        gv.game_version_id,
        p.max_depth
    FROM params p
    JOIN knowledge_item f ON f.canonical_key = p.from_key
    JOIN knowledge_item t ON t.canonical_key = p.to_key
    JOIN game_version gv ON gv.version_label = p.version_label
), undirected_edges AS (
    SELECT ir.source_item_id AS from_id, ir.target_item_id AS to_id,
           rt.type_code, rt.type_name, ir.rationale, ir.impact_explanation,
           ir.version_span_id
    FROM item_relation ir
    JOIN relation_type rt ON rt.relation_type_id = ir.relation_type_id
    WHERE ir.is_current = 1
    UNION ALL
    SELECT ir.target_item_id, ir.source_item_id,
           rt.type_code || ':inverse', COALESCE(rt.inverse_name, rt.type_name),
           ir.rationale, ir.impact_explanation, ir.version_span_id
    FROM item_relation ir
    JOIN relation_type rt ON rt.relation_type_id = ir.relation_type_id
    WHERE ir.is_current = 1
), paths(current_id, depth, visited, item_path, relation_path, explanation_path) AS (
    SELECT e.from_item_id, 0, printf('/%d/', e.from_item_id),
           k.canonical_key, '', ''
    FROM endpoints e
    JOIN knowledge_item k ON k.item_id = e.from_item_id
    UNION ALL
    SELECT edge.to_id, p.depth + 1,
           p.visited || printf('%d/', edge.to_id),
           p.item_path || ' -> ' || next_item.canonical_key,
           trim(p.relation_path || CASE WHEN p.relation_path = '' THEN '' ELSE ' / ' END || edge.type_code),
           trim(p.explanation_path || CASE WHEN p.explanation_path = '' THEN '' ELSE ' | ' END || edge.impact_explanation)
    FROM paths p
    JOIN endpoints ep
    JOIN undirected_edges edge ON edge.from_id = p.current_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = edge.version_span_id
     AND vsv.game_version_id = ep.game_version_id
    JOIN knowledge_item next_item ON next_item.item_id = edge.to_id
    WHERE p.depth < ep.max_depth
      AND instr(p.visited, printf('/%d/', edge.to_id)) = 0
)
SELECT depth, item_path, relation_path, explanation_path
FROM paths, endpoints
WHERE current_id = endpoints.to_item_id
ORDER BY depth, item_path
LIMIT 1;

-- Q6. Complete planning checklist for changing an AI subsystem.
-- Static authored steps are combined with impact-generated review actions.
WITH RECURSIVE
params(target_key, version_label, max_depth) AS (
    VALUES ('subsystem:economic-planning', '4.4.5', 4)
), target AS (
    SELECT ki.item_id, gv.game_version_id
    FROM params p
    JOIN knowledge_item ki ON ki.canonical_key = p.target_key
    JOIN game_version gv ON gv.version_label = p.version_label
), applicable_checklists AS (
    SELECT DISTINCT ct.checklist_item_id
    FROM target t
    JOIN checklist_target ct ON ct.target_item_id = t.item_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = ct.version_span_id
     AND vsv.game_version_id = t.game_version_id
), graph(current_id, depth, visited, path_text, review_action, validation_action) AS (
    SELECT arc.affected_item_id, 1,
           printf('/%d/%d/', t.item_id, arc.affected_item_id),
           start_ki.canonical_key || ' -> ' || affected.canonical_key,
           arc.review_action, arc.validation_action
    FROM target t
    JOIN knowledge_item start_ki ON start_ki.item_id = t.item_id
    JOIN v_impact_arc arc ON arc.changed_item_id = t.item_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = arc.version_span_id
     AND vsv.game_version_id = t.game_version_id
    JOIN knowledge_item affected ON affected.item_id = arc.affected_item_id
    UNION ALL
    SELECT arc.affected_item_id, g.depth + 1,
           g.visited || printf('%d/', arc.affected_item_id),
           g.path_text || ' -> ' || affected.canonical_key,
           arc.review_action, arc.validation_action
    FROM graph g
    JOIN params p
    JOIN target t
    JOIN v_impact_arc arc ON arc.changed_item_id = g.current_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = arc.version_span_id
     AND vsv.game_version_id = t.game_version_id
    JOIN knowledge_item affected ON affected.item_id = arc.affected_item_id
    WHERE g.depth < p.max_depth
      AND instr(g.visited, printf('/%d/', arc.affected_item_id)) = 0
), ranked_graph AS (
    SELECT
        graph.*,
        ROW_NUMBER() OVER (
            PARTITION BY current_id
            ORDER BY depth ASC, path_text ASC
        ) AS preferred_path
    FROM graph
), generated_actions AS (
    SELECT
        1000 + ROW_NUMBER() OVER (ORDER BY path_text, review_action) AS sort_key,
        'impact-generated' AS phase_code,
        'Review impact path' AS title,
        path_text || CASE WHEN review_action IS NULL THEN '' ELSE ': ' || review_action END AS instruction,
        COALESCE(validation_action, 'Use relation-specific validation.') AS expected_result,
        1 AS is_required,
        NULL AS tool_name
    FROM ranked_graph
    WHERE preferred_path = 1
      AND review_action IS NOT NULL
      AND review_action <> ''
), authored_steps AS (
    SELECT
        cs.step_number AS sort_key,
        cs.phase_code,
        cs.title,
        cs.instruction,
        cs.expected_result,
        cs.is_required,
        tool_ki.display_name AS tool_name
    FROM applicable_checklists ac
    JOIN checklist_step cs ON cs.checklist_item_id = ac.checklist_item_id
    LEFT JOIN knowledge_item tool_ki ON tool_ki.item_id = cs.tool_item_id
    LEFT JOIN v_version_span_version vsv
      ON vsv.version_span_id = cs.version_span_id
    JOIN target t
    WHERE cs.version_span_id IS NULL OR vsv.game_version_id = t.game_version_id
)
SELECT sort_key, phase_code, title, instruction, expected_result, is_required, tool_name
FROM authored_steps
UNION ALL
SELECT sort_key, phase_code, title, instruction, expected_result, is_required, tool_name
FROM generated_actions
ORDER BY sort_key, title;

-- Q7. Related triggers, effects, fields, scopes, defines, technologies, resources,
-- and vanilla examples for a mechanic.
WITH RECURSIVE
params(mechanic_key, version_label, max_depth) AS (
    VALUES ('mechanic:economic-plans', '4.4.5', 3)
), target AS (
    SELECT ki.item_id, gv.game_version_id
    FROM params p
    JOIN knowledge_item ki ON ki.canonical_key = p.mechanic_key
    JOIN game_version gv ON gv.version_label = p.version_label
), edges AS (
    SELECT source_item_id AS from_id, target_item_id AS to_id, version_span_id
    FROM item_relation WHERE is_current = 1
    UNION ALL
    SELECT target_item_id, source_item_id, version_span_id
    FROM item_relation WHERE is_current = 1
), related(item_id, depth, visited) AS (
    SELECT e.to_id, 1, printf('/%d/%d/', t.item_id, e.to_id)
    FROM target t
    JOIN edges e ON e.from_id = t.item_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = e.version_span_id
     AND vsv.game_version_id = t.game_version_id
    UNION ALL
    SELECT e.to_id, r.depth + 1, r.visited || printf('%d/', e.to_id)
    FROM related r
    JOIN params p
    JOIN target t
    JOIN edges e ON e.from_id = r.item_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = e.version_span_id
     AND vsv.game_version_id = t.game_version_id
    WHERE r.depth < p.max_depth
      AND instr(r.visited, printf('/%d/', e.to_id)) = 0
), typed_related AS (
    SELECT ki.item_id, ki.canonical_key, ki.display_name, it.type_code, MIN(r.depth) AS min_depth
    FROM related r
    JOIN knowledge_item ki ON ki.item_id = r.item_id
    JOIN item_type it ON it.item_type_id = ki.item_type_id
    WHERE it.type_code IN ('trigger','effect','field','scope','define','technology','resource')
    GROUP BY ki.item_id, ki.canonical_key, ki.display_name, it.type_code
), examples AS (
    SELECT
        ex.item_id, ex.canonical_key, ex.display_name,
        'vanilla_example' AS type_code, 0 AS min_depth
    FROM target t
    JOIN implementation_reference ir ON ir.topic_item_id = t.item_id
    JOIN v_version_span_version vsv
      ON vsv.version_span_id = ir.version_span_id
     AND vsv.game_version_id = t.game_version_id
    JOIN knowledge_item ex ON ex.item_id = ir.example_item_id
    WHERE ir.reference_kind = 'vanilla_example'
)
SELECT type_code, canonical_key, display_name, min_depth
FROM typed_related
UNION
SELECT type_code, canonical_key, display_name, min_depth
FROM examples
ORDER BY type_code, min_depth, canonical_key;

-- Q8. Weakly supported, contradicted, stale, uncertain, unknown, or unresolved knowledge.
SELECT
    'claim' AS record_type,
    c.claim_id AS record_id,
    ki.canonical_key AS primary_item,
    ast.state_code AS status,
    cl.confidence_code AS confidence,
    ca.assessed_at AS observed_at,
    c.statement AS text
FROM claim c
JOIN knowledge_item ki ON ki.item_id = c.primary_item_id
JOIN claim_assessment ca ON ca.claim_id = c.claim_id AND ca.is_current = 1
JOIN assessment_state ast ON ast.assessment_state_id = ca.assessment_state_id
JOIN confidence_level cl ON cl.confidence_level_id = ca.confidence_level_id
WHERE ast.state_code IN ('contradicted','stale','uncertain','unknown')
   OR cl.rank_value < 50
UNION ALL
SELECT
    'question', q.question_id, ki.canonical_key, q.status_code,
    NULL, q.next_review_at, q.question_text
FROM open_question q
JOIN knowledge_item ki ON ki.item_id = q.primary_item_id
WHERE q.status_code IN ('open','investigating','blocked')
ORDER BY record_type, record_id;

-- Q9. Compare two Stellaris versions: explicit deltas plus item status and claim assessments.
WITH params(from_label, to_label) AS (VALUES ('4.4.5', '4.5-beta')),
versions AS (
    SELECT f.game_version_id AS from_id, t.game_version_id AS to_id,
           f.version_label AS from_label, t.version_label AS to_label
    FROM params p
    JOIN game_version f ON f.version_label = p.from_label
    JOIN game_version t ON t.version_label = p.to_label
)
SELECT
    vc.change_key,
    v.from_label,
    v.to_label,
    ck.kind_code AS change_kind,
    vc.summary,
    rl.risk_code,
    ast.state_code AS assessment_state,
    cl.confidence_code,
    vc.review_required,
    group_concat(DISTINCT ki.canonical_key) AS related_items,
    vc.migration_note
FROM versions v
JOIN version_change vc ON vc.from_version_id = v.from_id AND vc.to_version_id = v.to_id
JOIN change_kind ck ON ck.change_kind_id = vc.change_kind_id
JOIN risk_level rl ON rl.risk_level_id = vc.risk_level_id
JOIN assessment_state ast ON ast.assessment_state_id = vc.assessment_state_id
JOIN confidence_level cl ON cl.confidence_level_id = vc.confidence_level_id
LEFT JOIN version_change_item vci ON vci.version_change_id = vc.version_change_id
LEFT JOIN knowledge_item ki ON ki.item_id = vci.item_id
GROUP BY vc.version_change_id
ORDER BY rl.rank_value DESC, vc.change_key;

-- Q10. Query the new war-planning sidecar without changing any unrelated core table.
SELECT
    ki.canonical_key,
    vs.span_code,
    ext.declaration_gate_summary,
    ext.script_visible_inputs,
    ext.hidden_engine_boundary,
    ext.required_runtime_proof,
    c.statement AS basis_claim
FROM ext_war_planning_mechanic_detail ext
JOIN knowledge_item ki ON ki.item_id = ext.mechanic_item_id
JOIN version_span vs ON vs.version_span_id = ext.version_span_id
LEFT JOIN claim c ON c.claim_id = ext.basis_claim_id;

-- Q11. Structured tool routing for an item or item type.
WITH params(target_key, version_label) AS (
    VALUES ('field:economic_plan.weight', '4.4.5')
), target AS (
    SELECT ki.item_id, ki.item_type_id, gv.game_version_id
    FROM params p
    JOIN knowledge_item ki ON ki.canonical_key = p.target_key
    JOIN game_version gv ON gv.version_label = p.version_label
)
SELECT
    tool_ki.display_name AS tool_name,
    itt.task_code,
    tc.capability_summary,
    tr.route_priority,
    tr.instructions,
    tc.invocation_template,
    tc.expected_output,
    fallback_ki.display_name AS fallback_tool
FROM target t
JOIN tool_route tr
  ON tr.is_active = 1
 AND (
      tr.target_item_id = t.item_id
      OR tr.target_item_type_id = t.item_type_id
 )
LEFT JOIN v_version_span_version vsv
  ON vsv.version_span_id = tr.version_span_id
JOIN tool_capability tc ON tc.tool_capability_id = tr.tool_capability_id
JOIN tool tool_sidecar ON tool_sidecar.item_id = tc.tool_item_id
JOIN knowledge_item tool_ki ON tool_ki.item_id = tool_sidecar.item_id
JOIN investigation_task_type itt ON itt.investigation_task_type_id = tc.investigation_task_type_id
LEFT JOIN tool_capability fallback_tc ON fallback_tc.tool_capability_id = tr.fallback_tool_capability_id
LEFT JOIN knowledge_item fallback_ki ON fallback_ki.item_id = fallback_tc.tool_item_id
WHERE tr.version_span_id IS NULL OR vsv.game_version_id = t.game_version_id
ORDER BY tr.route_priority DESC, tc.priority DESC;

-- Q12. Full-text lookup combined with structured item types.
SELECT
    ki.canonical_key,
    it.type_code,
    ki.display_name,
    snippet(item_fts, 2, '[', ']', ' … ', 12) AS match_snippet,
    bm25(item_fts) AS rank
FROM item_fts
JOIN knowledge_item ki ON ki.item_id = item_fts.rowid
JOIN item_type it ON it.item_type_id = ki.item_type_id
WHERE item_fts MATCH 'economic OR budget OR war'
ORDER BY rank, ki.canonical_key
LIMIT 20;

-- Q13. Integrity-oriented semantic checks beyond PRAGMA checks.
SELECT 'sidecar_type_mismatch' AS check_name, COUNT(*) AS problem_count
FROM v_sidecar_type_mismatch
UNION ALL
SELECT 'current_assessment_overlap_for_same_claim', COUNT(*)
FROM (
    SELECT a.claim_id
    FROM claim_assessment a
    JOIN claim_assessment b
      ON a.claim_assessment_id < b.claim_assessment_id
     AND a.claim_id = b.claim_id
     AND a.is_current = 1
     AND b.is_current = 1
    JOIN version_span avs ON avs.version_span_id = a.version_span_id
    JOIN version_span bvs ON bvs.version_span_id = b.version_span_id
    LEFT JOIN game_version amin ON amin.game_version_id = avs.min_version_id
    LEFT JOIN game_version amax ON amax.game_version_id = avs.max_version_id
    LEFT JOIN game_version bmin ON bmin.game_version_id = bvs.min_version_id
    LEFT JOIN game_version bmax ON bmax.game_version_id = bvs.max_version_id
    WHERE COALESCE(amin.version_order, -9223372036854775808) <= COALESCE(bmax.version_order, 9223372036854775807)
      AND COALESCE(bmin.version_order, -9223372036854775808) <= COALESCE(amax.version_order, 9223372036854775807)
);



-- Q14. Active captured playset members, required-parent status, and load positions.
SELECT
    playset_key, snapshot_key, version_label, load_position, mod_name,
    steam_workshop_id, required_by_project, live_load_state, canonical_path
FROM v_current_playset_member
ORDER BY load_position;

-- Q15. Playset-specific winning definitions and accepted/open conflict context.
SELECT
    w.object_key,
    w.resolution_status,
    w.release_key AS winning_release,
    w.relative_path AS winning_path,
    w.review_required,
    oc.conflict_kind,
    oc.status_code AS conflict_status,
    rl.risk_code,
    oc.rationale,
    oc.required_action
FROM v_playset_object_winner w
LEFT JOIN object_conflict oc
  ON oc.playset_snapshot_id=w.playset_snapshot_id
 AND oc.object_item_id=w.object_item_id
LEFT JOIN risk_level rl ON rl.risk_level_id=oc.risk_level_id
ORDER BY w.object_key;

-- Q16. Selected normalized model facts across scenario, metric, and resource dimensions.
WITH params(subject_key) AS (VALUES ('building:building_navel_base'))
SELECT
    v.run_key,
    v.subject_key,
    v.scenario_key,
    v.metric_key,
    v.dimension_item_key,
    COALESCE(v.real_value, v.integer_value, v.text_value, v.boolean_value) AS value,
    v.unit,
    el.record_set,
    el.record_key,
    el.row_number
FROM v_analysis_value_typed v
JOIN params p ON p.subject_key=v.subject_key
LEFT JOIN evidence_locator el ON el.evidence_locator_id=v.evidence_locator_id
ORDER BY v.scenario_key, v.metric_key, v.dimension_item_key;

-- Q17. Open model/runtime issues, exact missing evidence, and linked policies/questions.
SELECT
    model_key, run_key, subject_key, issue_type, issue_key,
    severity_code, priority, exact_missing_evidence, resolution_summary, question_id
FROM v_open_analysis_issue
ORDER BY priority DESC, model_key, subject_key;

-- Q18. Dataset schema drift between registered generator checkpoints.
SELECT
    schema_key, previous_schema_version, current_schema_version,
    previous_column_count, current_column_count, drift_status
FROM v_dataset_schema_drift
WHERE schema_key='benefit-taxonomy-v2'
ORDER BY current_schema_id;

-- Q19. Complete external dataset layouts and their normalization mapping.
WITH params(schema_key) AS (VALUES ('buildings-v2'))
SELECT
    ds.schema_key, ds.schema_version, ds.row_count, ds.column_count,
    dc.ordinal, dc.column_name, dc.logical_type, dc.semantic_role,
    dc.dimension_group, dc.metric_key, dc.unit,
    it.type_code AS mapped_item_type,
    dc.description
FROM params p
JOIN dataset_schema ds ON ds.schema_key=p.schema_key
JOIN dataset_column dc ON dc.dataset_schema_id=ds.dataset_schema_id
LEFT JOIN item_type it ON it.item_type_id=dc.mapped_item_type_id
WHERE ds.schema_version='2026-07-09'
ORDER BY dc.ordinal;

-- Q20. Observer-save progression and country-0 diagnostic facts, preserving evidence boundaries.
SELECT
    s.subject_key,
    s.label,
    m.metric_key,
    COALESCE(CAST(av.integer_value AS TEXT), CAST(av.real_value AS TEXT), av.text_value,
             CASE av.boolean_value WHEN 1 THEN 'true' WHEN 0 THEN 'false' END) AS value,
    cl.confidence_code,
    el.label AS evidence_locator,
    av.notes
FROM analysis_subject s
JOIN analysis_value av ON av.analysis_subject_id=s.analysis_subject_id
JOIN analysis_metric m ON m.analysis_metric_id=av.analysis_metric_id
LEFT JOIN confidence_level cl ON cl.confidence_level_id=av.confidence_level_id
LEFT JOIN evidence_locator el ON el.evidence_locator_id=av.evidence_locator_id
WHERE s.analysis_run_id=4
ORDER BY s.analysis_subject_id, m.metric_key;

-- Q21. Project-corpus accommodation: which external artifacts, schemas, models, and tools cover a topic.
WITH params(term) AS (VALUES ('research'))
SELECT DISTINCT
    ki.canonical_key,
    it.type_code,
    ki.display_name,
    fa.relative_path,
    am.model_key,
    t.executable_or_entrypoint
FROM params p
JOIN knowledge_item ki ON lower(ki.canonical_key || ' ' || ki.display_name || ' ' || ki.summary) LIKE '%' || lower(p.term) || '%'
JOIN item_type it ON it.item_type_id=ki.item_type_id
LEFT JOIN file_asset fa ON fa.item_id=ki.item_id
LEFT JOIN analysis_model am ON am.item_id=ki.item_id
LEFT JOIN tool t ON t.item_id=ki.item_id
ORDER BY it.type_code, ki.canonical_key;

-- Q22. Extended semantic checks for the project-aware schema.
SELECT 'analysis_dimension_type_mismatch' AS check_name, COUNT(*) AS problem_count
FROM v_analysis_dimension_type_mismatch
UNION ALL
SELECT 'dataset_key_column_orphan', COUNT(*)
FROM dataset_key_column dkc
LEFT JOIN dataset_column dc
  ON dc.dataset_schema_id=dkc.dataset_schema_id AND dc.dataset_column_id=dkc.dataset_column_id
WHERE dc.dataset_column_id IS NULL
UNION ALL
SELECT 'playset_resolution_without_winner', COUNT(*)
FROM playset_object_resolution
WHERE resolution_status IN ('single','resolved') AND winning_definition_id IS NULL
UNION ALL
SELECT 'current_playset_duplicate_position', COUNT(*)
FROM (
  SELECT playset_snapshot_id, load_position
  FROM playset_member
  GROUP BY playset_snapshot_id, load_position
  HAVING COUNT(*) > 1
);

-- Operational checks to run explicitly after loading:
PRAGMA foreign_key_check;
PRAGMA integrity_check;
