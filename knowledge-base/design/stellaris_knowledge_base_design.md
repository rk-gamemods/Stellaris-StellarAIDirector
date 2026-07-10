# Stellaris AI Mod Knowledge Base — Project-Aware Relational Design

**Artifact:** `stellaris_knowledge_base_design.md`  
**Schema revision:** 2  
**Database engine:** SQLite only  
**Minimum SQLite:** 3.37.0 with FTS5 enabled  
**Validated runtime:** Python `sqlite3` linked to SQLite 3.46.1  
**Project snapshot reviewed:** `b605aa0e85b5ac68c40a07fdb7c41ece02c365cd` on `codex/stellar-ai-director-strategic-v2`, dirty worktree, captured 2026-07-10  
**Design date:** 2026-07-10

## 1. Executive decision

Use a **stable knowledge-item supertype with typed sidecars**, surrounded by six normalized context layers:

1. exact Stellaris versions, repository snapshots, mod releases, source roots, playset snapshots, and execution contexts;
2. retrievable evidence artifacts and fine-grained locators, including external dataset schemas and cells;
3. immutable claims with version/context-specific assessments, contradictions, questions, and revalidation policy;
4. definition occurrences, resolved references, playset-specific winners, and explicit conflict sets;
5. a typed relationship graph plus authored checklists and tool-routing rules; and
6. registered analysis models with scenarios, subjects, metrics, typed values, hard gates, consumer policies, validation findings, and issue queues.

The core contains **96 ordinary STRICT tables, 4 FTS5 virtual tables, 12 views, 23 triggers, and 83 explicit indexes**. FTS5 shadow tables are SQLite implementation details and are not counted as logical tables. The examples add one independent `ext_war_planning_mechanic_detail` sidecar, yielding **101 logical tables in the demonstration database** without changing any unrelated core table.

This is still a small local knowledge organizer. It does **not** replace the game installation, Workshop/source snapshots, saves, logs, Git, Irony, CWTools, Munch indexes, or the generated CSV/JSON/JSONL products. Those systems remain authoritative for their own contents. The database stores stable identities, conclusions, applicability, exact retrieval instructions, schemas, selected normalized facts, and relationships needed for impact analysis.

### Why the project-aware revision is necessary

The first-pass design correctly separated claims, evidence, versions, and graph edges, but the actual Stellaris project exposes additional facts that must be first-class:

- a definition is only a **winner relative to a captured playset and load order**;
- the same mod has stable identity, multiple releases, multiple roots, and distinct repository/live-launch surfaces;
- generated CSVs are authoritative datasets with evolving schemas, stable keys, and thousands of repeated dimensional columns;
- model facts need scenario, resource, subject, gate, policy, and issue coordinates;
- conflict scans and validators produce findings, not claims by themselves;
- observer/save facts need exact run mode and save identity, and user observations must remain distinct from parsed state; and
- historical generator checkpoints must coexist with current zero-blocker or expanded-schema outputs instead of being overwritten.

## 2. Project corpus reviewed and accommodation result

The context bundle reports **751 packed source candidates**: 93 CSV, 39 JSON, 5 JSONL, 383 Markdown, 42 Python, 184 text, and 5 YAML files. The active work includes seven local mod source folders including Stellar AI Director, a large active 4.4 playset, deterministic tools, object-atlas outputs, economic/modeling datasets, conflict and validation reports, observer checkpoints, selected save evidence, plans, ledgers, and external research packets.

The representative seed registers complete layouts for 15 important dataset schemas and **1,361 external columns**, including the actual current shapes below. This is a schema-fit demonstration, not a proposal to bulk-copy all rows.

| Existing artifact | Current shape | Relational accommodation |
|---|---:|---|
| Object atlas | 31,211 × 24 | `dataset_schema`/`dataset_column`; object identities and selected occurrences in `object_definition`; references in `definition_reference`; winners in `playset_object_resolution`. |
| Dependency edges | 34,789 × 8 | External dataset remains authoritative; selected durable edges become `definition_reference` or `item_relation` with evidence. |
| Parent-AI support map | 31,211 × 10 | External schema plus selected classifications as `analysis_subject`/`analysis_value`/`analysis_policy`. |
| Policy matrix | 8,135 × 13 | Route/policy subjects and typed policy decisions; selected durable dependencies in the graph. |
| Research-capacity jobs | 501 × 155 | Complete column catalog; repeated scenario × flow × resource columns normalize to `analysis_metric` + resource-dimensioned `analysis_value`. |
| Research-capacity buildings | 826 × 282 | Definition/winner provenance, gates, job references, scenarios, resource flows, and selected benefits. |
| Development districts/zones | 547 × 370 | Same dimensional fact model, with `object_kind`/`game_object` identities for districts and zones. |
| Research colony plans | 24 × 315 | Plan subject composed through `analysis_subject_member`; scenario/resource facts remain typed. |
| Colony role targets | 247 × 78 | Role/policy subjects, selected target members, scores, and source locators. |
| Technology modifiers | 18 × 9 | Technology items, definition references, and selected analysis metrics. |
| Build-plan readiness | 826 × 24 | `analysis_gate` for prerequisites/potential/allow/flags; `analysis_policy` for readiness/fallback/replacement. |
| Strategic benefit taxonomy | 1,924 × 22 current; 1,887 × 19 historical checkpoint | Versioned `dataset_schema`; benefit-class items; `analysis_metric`, `analysis_value`, `analysis_policy`; `v_dataset_schema_drift`. |
| Modeling blocker accounting | current extracted schema 0 × 9; earlier ledger checkpoint 396 rows | Each run keeps its own dataset schema/artifact; current issues are `analysis_issue`; historical queues are not deleted. |
| Consumer policy | 1,093 × 23 | `analysis_policy` and `analysis_gate`; exact external rows remain addressable through dataset locators. |
| Selected saves | four hashed `.sav` files, raw archives external | Save artifacts by hash/size; run/context; runtime subjects and typed facts; user observation in a separate locator/fact with lower evidentiary directness. |

### Corpus-to-table mapping

| Project information | Primary tables | Why this fits without uncontrolled EAV or copying tools |
|---|---|---|
| Repository branches, commits, dirty state, source files | `repository_snapshot`, `source_root`, `source_artifact`, `file_asset` | Stable snapshot identity plus retrievable path/hash. |
| Mods, Workshop IDs, descriptors, supported versions | `mod_package`, `mod_release`, `source_root`, `source_artifact` | Stable mod identity is separated from each captured release/root. |
| Active Irony/launcher playset and load order | `playset`, `playset_snapshot`, `playset_member`, `execution_context` | Membership/order are historical snapshots; live-load status remains separate. |
| Vanilla/mod object definitions and fields | `game_object`, `object_definition`, `object_field_occurrence`, `definition_reference` | Named typed columns preserve occurrence structure and exact locators. |
| Active winners and conflicts | `playset_object_resolution`, `object_conflict`, `object_conflict_member` | Winning is contextual, explainable, and versioned by snapshot. |
| CSV/JSON/JSONL schemas | `dataset_schema`, `dataset_column`, `dataset_key_column`, `evidence_locator` | Complete layout and stable keys are known while full records stay external. |
| Wide resource/scenario models | `analysis_model`, `analysis_run`, `analysis_scenario`, `analysis_subject`, `analysis_metric`, `analysis_value` | Controlled dimensions replace hundreds of bespoke nullable columns in the core. |
| Readiness, fallback, benefit formulas, zero-effect classifications | `analysis_gate`, `analysis_policy`, `analysis_issue` | Hard eligibility, policy, and unresolved work are not conflated with numeric facts. |
| CWTools/parser/reference/conflict/log/save findings | `verification_run`, `validation_finding`, `evidence_locator` | Findings are run-specific evidence products and may support later claims. |
| Research conclusions and contradictions | `claim`, `claim_assessment`, `claim_evidence`, `claim_conflict` | Proposition, judgment, and evidence remain independent and historical. |
| Open questions and missing proof | `open_question`, `question_item`, `question_evidence`, `analysis_issue` | Exact missing evidence and follow-up remain queryable. |
| Change impact and maintenance process | `item_relation`, `v_impact_arc`, recursive CTEs, `impact_rule`, checklist tables | Direct and transitive paths include why, risk, review, validation, and tools. |
| Tool authority and routing | `source_system`, `tool`, `tool_capability`, `tool_route` | The KB points to JDataMunch/JCodeMunch/JDocMunch, Irony, CWTools, scripts, logs, and saves rather than replacing them. |

## 3. Requirements, recommendations, assumptions, and unresolved choices

### 3.1 Requirements implemented

- One local SQLite database; no server, daemon, watcher, GUI, parser framework, or background service.
- Exact game versions and reusable spans, plus execution contexts for playset, repository, run mode, settings, DLC, and exclusions.
- Stable identities for mechanics, families, subsystems, mods, objects, fields, triggers, effects, scopes, modifiers, defines, resources, technologies, files, tools, datasets, benefit classes, routes, and settings.
- Version/context-specific claims and assessments with direct supporting, contradicting, or qualifying evidence and complete retrieval provenance.
- Definition occurrences separated from playset-specific winners and conflict sets.
- Typed, versioned relationship graph with recursive direct/transitive impact paths and actionable review/validation text.
- Authored subsystem checklists and structured tool routes.
- Explicit stale/reverification queues, contradictions, unresolved questions, validation findings, and analysis issues.
- Complete external dataset schema catalogs and selected normalized model facts, without copying full authoritative datasets.
- Typed extension sidecars for future mechanics without unrelated core migrations.
- Traceable writes through actors and change sets, plus append/supersede history.

### 3.2 Recommendations

- Set `PRAGMA foreign_keys=ON` on **every** connection; do not depend on a build default.
- Use one short writer transaction at a time, a nonzero busy timeout, and read-only/query-only connections for AI agents that are not updating knowledge.
- Use WAL for the expected same-host pattern of several readers and infrequent writes; checkpoint/close before copying the database file.
- Keep large datasets external. Register complete schemas and keys; normalize only facts needed for durable cross-dataset queries, impact analysis, or conclusions.
- Regenerate playset winners and model outputs whenever the repository, source roots, game version, or playset fingerprint changes.
- Run `PRAGMA optimize` after schema/index changes and periodically on evolving long-lived databases.
- Before handoff, run all semantic checks, `foreign_key_check`, `quick_check`, and `integrity_check`.

### 3.3 Assumptions

- The project can assign exact versions a linear `version_order` within the current PC release line. A future parallel branch can add a version-line sidecar without replacing existing version IDs.
- The database is normally used on one machine. Source roots may contain local paths, while stable root/artifact keys provide portability.
- Claims are atomic enough for one assessment state. Compound statements should be split.
- Recursive reachability means “review or validate this,” not automatic proof of runtime causality.
- The current functional database begins with representative data; gradual population is intentional.

### 3.4 Unresolved implementation choices

- **WAL versus literal one-directory-entry operation.** WAL is recommended for concurrency, but active WAL mode creates `-wal` and `-shm` companion files. Use rollback journal mode only if “one file at every instant” outweighs concurrent-read behavior.
- **Dataset registration scope.** Revision 2 demonstrates 15 central schemas. Register the remaining CSV/JSON/JSONL layouts incrementally when an agent needs them; do not block day-one implementation on all 137 structured artifacts.
- **Normalized-fact scope.** Do not materialize all millions of object-atlas/dependency/model cells. Promote facts only when they are reused across claims, impact paths, checklists, or model comparisons.
- **Exact current launcher state.** Captured playset membership is evidence; live next-launch state remains a separately checked status and should not be inferred from repository source.
- **Current 4.4.5 country-type war gates.** The Director full-object override cites Pegasus 4.4.4 provenance. The exact 4.4.5 vanilla object remains an explicit open revalidation question in the seed.

## 4. Relational methodology and boundaries

### 4.1 Stable supertype plus typed sidecars

`knowledge_item` is the graph-addressable identity. Domain structure lives in one-to-one or one-to-many typed tables. This is class-table inheritance, not EAV: a mod has `mod_package` fields; a field has `field_definition`; a model has `analysis_model`; a resource is a typed item; a future mechanic can add an `ext_*` sidecar with named columns and constraints.

### 4.2 Immutable propositions, contextual judgments

`claim` stores the wording. `claim_assessment` stores the version span, execution context, state, confidence, verification run, and freshness. New evidence creates a new assessment that supersedes the previous current row. A materially reworded proposition creates a new claim.

### 4.3 Definition occurrence, resolution, and conflict are separate

`object_definition` means “this source occurrence exists.” It never means “this is globally winning.” `playset_object_resolution` answers which occurrence wins for one captured stack. `object_conflict` and members explain the candidate set, load positions, differing fields, risk, and required review. This directly fixes the ambiguity exposed by Director overrides of Gigas, NSC3, ESC, Planetary Diversity, Starbase Extended, vanilla country types, buildings, technologies, and other full objects.

### 4.4 External datasets remain external

`dataset_schema` and `dataset_column` preserve the complete layout. `dataset_key_column` defines stable record identity. `evidence_locator` can point to a dataset row/cell. Reusable facts are normalized through the analysis tables. This is not uncontrolled EAV because metrics and dimensions are registered and typed; the generic coordinate exists only for analysis outputs whose dimensions genuinely vary by model/scenario/resource.

### 4.5 Provenance chain

The normal retrieval path is:

`repository_snapshot/mod_release/source_root` → `source_system` → `source_artifact` → optional `dataset_schema` → `evidence_locator` → claim/relation/finding/policy/value/question.

Generated artifacts additionally use `artifact_derivation` and `analysis_run_artifact`. A locator can carry path and lines, section, symbol/object key, record set/key, row/column, JSON path, archive member, byte range, query, timestamp, game date, excerpt, and explicit retrieval instructions.

## 5. Impact-analysis approach

### 5.1 Typed stored edges

`item_relation` stores the semantic relation, version span, confidence, risk, basis claim, rationale, impact explanation, review action, and validation action. `relation_type.impact_propagation_mode` says whether a proposed change propagates forward, reverse, both, or not at all.

`v_impact_arc` expands every current semantic edge into normalized **changed item → potentially affected item** arcs. The view preserves the stored direction so every result can explain why it was traversed.

### 5.2 Recursive direct and transitive analysis

Q4 uses a version-filtered recursive CTE with:

- depth 1 for direct consequences and depth 2+ for transitive consequences;
- a delimiter-wrapped visited-ID path to prevent cycles;
- an explicit maximum depth;
- readable item and relation paths;
- maximum path risk;
- accumulated edge-specific review and validation actions; and
- shortest-preferred-path ranking per affected item.

Q5 performs undirected discovery when the question is “why are these two concepts connected?” Q6 combines authored checklist steps with graph-derived actions, retaining the path that caused each generated review item.

### 5.3 Project-aware propagation

A change to `building_navel_base`, for example, can traverse to its Director source file, the PD parent occurrence, `tech_planetary_defenses`, `staid_naval_capacity_expansion_ready`, naval-capacity benefit policy, the active playset winner/conflict, source datasets, and required validation. A change to a model field can traverse through dataset schema, generator tool, model run, policy, affected object, subsystem, and compatibility parents.

Impact output is conservative. It answers what must be inspected and why; it does not assert that every reachable node changes at runtime.

## 6. Versioning, freshness, contradictions, and revalidation

- `game_version` stores exact builds and one primary target; `version_span` stores reusable intervals.
- `item_version_status`, field/symbol revisions, definitions, relationships, checklists, routes, and mechanic sidecars all use version spans.
- `version_change` records explicit pairwise deltas with affected items and evidence.
- `claim_assessment` adds execution context when version alone is insufficient.
- `revalidation_policy`, `claim_revalidation_policy`, and `item_revalidation_policy` generate a systematic stale/reverify queue.
- `v_reverification_queue` combines assessment state, confidence, target-version coverage, deadlines, and explicit policies.
- `claim_conflict` preserves logical contradictions; `object_conflict` preserves load/source conflicts; `analysis_issue` preserves model/runtime work queues. These are distinct domains and should not be collapsed.

## 7. Modeling the existing wide CSVs

The 155–370-column economic artifacts are not 155–370 unrelated properties. Most columns are combinations such as:

`base_output_physics_research`, `triggered_upkeep_consumer_goods`, `optimistic_net_alloys`, `conservative_output_energy`, or prerequisite-qualified variants.

The relational representation is:

- model: `analysis_model`;
- generator execution: `analysis_run`;
- variant: `analysis_scenario`;
- object/row/planet plan/country/save: `analysis_subject`;
- reusable fact definition: `analysis_metric` (`resource_output`, `resource_upkeep`, `resource_net`, readiness status, planner target, etc.);
- resource or other typed dimension: `dimension_item_id`;
- one typed coordinate value: `analysis_value`;
- prerequisites/eligibility: `analysis_gate`;
- formula/non-scoring/fallback/replacement decision: `analysis_policy`; and
- unresolved/missing evidence: `analysis_issue`.

This controlled dimensional fact table is appropriate because metric and dimension definitions are constrained. It is not a generic property bag: values cannot introduce arbitrary field names; every metric belongs to a registered model, every optional dimension has a declared item type, and semantic mismatch views/triggers must remain empty.

## 8. Safe, traceable AI-agent updates

1. Open the database; verify `application_id=1397441074`, `user_version=2`, schema metadata, FTS5, and `PRAGMA foreign_keys=ON`.
2. Use `PRAGMA query_only=ON` for a read-only agent. A writer opens one short explicit transaction and creates an `open` change set.
3. Resolve or create stable items, repository/mod/root/playset/context records, then source artifacts and exact locators before conclusions.
4. Add definition occurrences or model facts; never mark a definition as winner outside `playset_object_resolution`.
5. Add evidence links before a new assessment, relation, policy, finding, or issue resolution.
6. Supersede current assessments/policies/status rows in the same transaction; do not hard-delete contradicted or stale evidence.
7. Commit the change set with actor, time, purpose, and repository commit when applicable.
8. Run Q13, Q22, foreign-key checks, and integrity checks. Refresh FTS only through normal triggers or an explicit FTS rebuild after exceptional bulk operations.

## 9. SQLite-specific decisions

### 9.1 STRICT tables

All 96 ordinary core tables are `STRICT`. SQLite introduced STRICT tables in 3.37.0; each column has an allowed type and type violations participate in `integrity_check`/`quick_check`. This reduces accidental AI-agent insertion of numeric-looking text or malformed booleans.[^sqlite-strict]

### 9.2 Foreign keys

Foreign keys use restrictive deletion for durable provenance and cascades only for true dependent rows. SQLite requires foreign-key enforcement to be enabled per connection; clients must set it explicitly.[^sqlite-fk]

### 9.3 WAL and the one-file constraint

WAL matches occasional parallel readers and infrequent writes, but active WAL mode creates `-wal` and `-shm` companion files. The authoritative persistent database remains the main SQLite file; checkpoint and close before transport. Use rollback journal mode instead only if the literal transient companion-file constraint is stronger.[^sqlite-wal]

### 9.4 Recursive CTEs

SQLite recursive CTEs support graph/tree walks. The examples use bounded recursive traversal rather than a materialized transitive-closure table, which is simpler and adequate for the expected local scale.[^sqlite-cte]

### 9.5 Partial indexes

Partial unique indexes enforce one current assessment/status, one primary target version, and other subset uniqueness without blocking historical rows.[^sqlite-partial]

### 9.6 FTS5

Four external-content FTS5 tables accelerate discovery over items, claims, questions, and evidence. Triggers keep them synchronized; structured relational tables remain authoritative.[^sqlite-fts]

### 9.7 Optimization and validation

Current SQLite guidance recommends `PRAGMA optimize` as the normal way to invoke targeted ANALYZE work. `integrity_check` does not replace `foreign_key_check`; both are part of the handoff gate.[^sqlite-optimize] [^sqlite-pragma]

## 10. One-working-day implementation boundary

### Included

1. Create a fresh database from the schema and verify SQLite/FTS5 support.
2. Load the representative seed: versions, core vocabularies, source systems, project snapshot, central mods/releases/roots/playset, 15 dataset schemas with 1,361 column definitions, representative object winners/conflicts, model facts, selected save facts, claims, relations, checklist/tool routes, and extension sidecar.
3. Run Q1–Q22 and all integrity/semantic checks.
4. Document connection discipline and the append/supersede write lifecycle.

### Explicitly excluded

- importing all 751 files or all rows from large datasets;
- writing parsers, import frameworks, watchers, observer harnesses, conflict solvers, GUIs, APIs, or services;
- replacing JDataMunch/JCodeMunch/JDocMunch, Irony, CWTools, Git, logs, or saves;
- materializing every transitive relationship;
- inventing formulas/confidence scores or claiming runtime causation without evidence; and
- launching Stellaris or running observer simulations.

## 11. Table inventory

- **1. Governance, authorship, versions, and controlled vocabularies: 20 tables.** `schema_metadata`, `actor`, `change_set`, `lifecycle_state`, `confidence_level`, `assessment_state`, `game_version`, `version_span`, `item_type`, `object_kind`, `script_symbol_kind`, `claim_type`, `evidence_source_type`, `locator_type`, `evidence_stance`, `risk_level`, `relation_type`, `change_kind`, `change_type`, `investigation_task_type`.
- **2. Stable identities and typed Stellaris surfaces: 16 tables.** `knowledge_item`, `item_alias`, `item_version_status`, `mechanic_family`, `mechanic`, `subsystem`, `game_object`, `file_asset`, `script_symbol`, `field_definition`, `field_revision`, `script_scope`, `script_symbol_revision`, `symbol_scope_rule`, `symbol_parameter`, `ai_budget_mechanic_detail`.
- **3. Repository, mod-release, playset, and execution context: 10 tables.** `repository_snapshot`, `mod_package`, `mod_release`, `source_root`, `playset`, `playset_snapshot`, `playset_member`, `execution_context`, `execution_context_item`, `playset_object_resolution`.
- **4. Evidence, external datasets, definitions, conflicts, and validation: 14 tables.** `source_system`, `source_artifact`, `artifact_derivation`, `evidence_locator`, `dataset_schema`, `dataset_column`, `dataset_key_column`, `object_definition`, `object_field_occurrence`, `definition_reference`, `object_conflict`, `object_conflict_member`, `verification_run`, `validation_finding`.
- **5. Claims, assessments, contradictions, questions, and revalidation: 11 tables.** `claim`, `claim_item`, `claim_assessment`, `claim_evidence`, `claim_conflict`, `open_question`, `question_item`, `question_evidence`, `revalidation_policy`, `claim_revalidation_policy`, `item_revalidation_policy`.
- **6. Relationship graph, version changes, checklists, implementation, and tools: 14 tables.** `item_relation`, `relation_evidence`, `impact_rule`, `implementation_reference`, `version_change`, `version_change_item`, `version_change_evidence`, `checklist`, `checklist_target`, `checklist_step`, `checklist_step_item`, `tool`, `tool_capability`, `tool_route`.
- **7. Analysis models, scenarios, facts, gates, policies, and issues: 11 tables.** `analysis_model`, `analysis_run`, `analysis_run_artifact`, `analysis_scenario`, `analysis_subject`, `analysis_subject_member`, `analysis_metric`, `analysis_value`, `analysis_gate`, `analysis_policy`, `analysis_issue`.
- **8. Full-text discovery: 4 virtual tables.** `item_fts`, `claim_fts`, `question_fts`, `evidence_fts`.

Core total: **96 ordinary STRICT tables + 4 FTS5 virtual tables = 100 logical tables**.

## 12. Detailed table and field catalog

Every ordinary table is `STRICT`. The executable SQL is authoritative for exact syntax. The catalog below explains the purpose, keys, constraints, relationships, indexes, triggers, and every field.

### 1. Governance, authorship, versions, and controlled vocabularies

This group establishes safe governance, exact version applicability, ordered confidence/risk, and extensible vocabularies.

#### `schema_metadata`

**Purpose and expected use.** Stores database-level identity, schema revision, feature requirements, and operational conventions. These values let a client reject the wrong file or unsupported schema without inferring meaning from table contents.

**Primary key.** `metadata_key`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `metadata_key` | `metadata_key TEXT PRIMARY KEY` | Stable machine key used by clients to read a specific schema fact. |
| `metadata_value` | `metadata_value TEXT NOT NULL` | Serialized scalar value for the schema fact; values remain intentionally simple and non-JSON. |
| `description` | `description TEXT` | Explains how a client should interpret the metadata value. |

#### `actor`

**Purpose and expected use.** Normalizes the humans, AI agents, tools, and system identities that create or assess records. It supports traceable authorship without embedding names repeatedly in every knowledge row.

**Primary key.** `actor_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `actor_id` | `actor_id INTEGER PRIMARY KEY` | Stable primary key for the `actor` row. |
| `actor_key` | `actor_key TEXT NOT NULL UNIQUE` | Stable, namespaced identifier such as human:mod-owner or ai:agent-name. |
| `display_name` | `display_name TEXT NOT NULL` | Readable actor name shown in audit output. |
| `actor_type` | `actor_type TEXT NOT NULL CHECK (actor_type IN ('human','ai_agent','tool','system'))` | Distinguishes human, AI agent, tool, and system authorship. |
| `external_identifier` | `external_identifier TEXT` | Optional external account, agent, process, or tool identifier. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `change_set`

**Purpose and expected use.** Provides a logical audit envelope for a coherent write transaction. Every durable knowledge addition or retirement points to the change set that introduced it, so an AI agent can explain who changed what, why, and against which repository commit.

**Primary key.** `change_set_id`

**Table-level integrity rules.** `CHECK ((state = 'committed' AND committed_at IS NOT NULL) OR state <> 'committed')`.

**Relationships.** `(actor_id)` → `actor(actor_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_change_set_actor_state` — CREATE INDEX idx_change_set_actor_state ON change_set(actor_id, state, opened_at).

| Field | Declaration | Why it exists |
|---|---|---|
| `change_set_id` | `change_set_id INTEGER PRIMARY KEY` | Stable primary key for the `change_set` row. |
| `change_set_key` | `change_set_key TEXT NOT NULL UNIQUE` | Stable identifier for the logical write batch. |
| `title` | `title TEXT NOT NULL` | Human-readable name for the change batch. |
| `purpose` | `purpose TEXT NOT NULL` | States why the database change was made. |
| `actor_id` | `actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT` | Identifies the actor responsible for the change set. |
| `state` | `state TEXT NOT NULL CHECK (state IN ('open','committed','aborted'))` | Tracks whether the batch is open, committed, or aborted. |
| `opened_at` | `opened_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))` | ISO-8601 date/time associated with `opened_at`. |
| `committed_at` | `committed_at TEXT` | ISO-8601 date/time associated with `committed_at`. |
| `repository_commit` | `repository_commit TEXT` | Optional repository commit associated with the knowledge update. |
| `transaction_note` | `transaction_note TEXT` | Records transaction-level caveats, review notes, or handoff context. |

#### `lifecycle_state`

**Purpose and expected use.** Defines catalog lifecycle states such as draft, active, and retired. It separates “is this record current project material?” from epistemic states such as verified or uncertain.

**Primary key.** `lifecycle_state_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `lifecycle_state_id` | `lifecycle_state_id INTEGER PRIMARY KEY` | Stable primary key for the `lifecycle_state` row. |
| `state_code` | `state_code TEXT NOT NULL UNIQUE` | Stable code used to classify or filter `lifecycle_state` rows. |
| `state_name` | `state_name TEXT NOT NULL` | Human-readable name for this `lifecycle_state` value. |
| `is_active` | `is_active INTEGER NOT NULL CHECK (is_active IN (0,1))` | Indicates whether records in this lifecycle state should appear in normal current-use queries. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `confidence_level`

**Purpose and expected use.** Defines an ordered confidence vocabulary. Numeric ranks support sorting and thresholds while codes and descriptions preserve the project meaning of each level.

**Primary key.** `confidence_level_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `confidence_level_id` | `confidence_level_id INTEGER PRIMARY KEY` | Stable primary key for the `confidence_level` row. |
| `confidence_code` | `confidence_code TEXT NOT NULL UNIQUE` | Stable code used to classify or filter `confidence_level` rows. |
| `confidence_name` | `confidence_name TEXT NOT NULL` | Human-readable name for this `confidence_level` value. |
| `rank_value` | `rank_value INTEGER NOT NULL UNIQUE CHECK (rank_value BETWEEN 0 AND 100)` | Comparable 0–100 ordering used for sorting and thresholds; it is not a probability. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `assessment_state`

**Purpose and expected use.** Defines epistemic states such as verified, inferred, uncertain, contradicted, stale, and unknown. The explicit usability flag prevents agents from treating every assessment as an accepted fact.

**Primary key.** `assessment_state_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `assessment_state_id` | `assessment_state_id INTEGER PRIMARY KEY` | Stable primary key for the `assessment_state` row. |
| `state_code` | `state_code TEXT NOT NULL UNIQUE` | Stable code used to classify or filter `assessment_state` rows. |
| `state_name` | `state_name TEXT NOT NULL` | Human-readable name for this `assessment_state` value. |
| `rank_value` | `rank_value INTEGER NOT NULL CHECK (rank_value BETWEEN 0 AND 100)` | Ordering aid for epistemic states; it does not replace the state code. |
| `is_usable_as_fact` | `is_usable_as_fact INTEGER NOT NULL CHECK (is_usable_as_fact IN (0,1))` | Explicit gate for whether agents may normally cite this state as accepted fact. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `game_version`

**Purpose and expected use.** Catalogs exact Stellaris versions/builds in a deterministic order, including channel, codename, build identifier, and the single current target. It is the atomic version axis used by evidence, runs, and comparisons.

**Primary key.** `game_version_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `uq_game_version_primary_target` — CREATE UNIQUE INDEX uq_game_version_primary_target ON game_version(is_primary_target) WHERE is_primary_target = 1.

| Field | Declaration | Why it exists |
|---|---|---|
| `game_version_id` | `game_version_id INTEGER PRIMARY KEY` | Stable primary key for the `game_version` row. |
| `version_label` | `version_label TEXT NOT NULL UNIQUE` | Canonical user-facing version label, for example 4.4.5. |
| `version_order` | `version_order INTEGER NOT NULL UNIQUE` | Total ordering used to expand and compare version spans. |
| `major` | `major INTEGER CHECK (major IS NULL OR major >= 0)` | Parsed major component when known. |
| `minor` | `minor INTEGER CHECK (minor IS NULL OR minor >= 0)` | Parsed minor component when known. |
| `patch` | `patch INTEGER CHECK (patch IS NULL OR patch >= 0)` | Parsed patch component when known. |
| `codename` | `codename TEXT` | Optional Stellaris release codename. |
| `build_id` | `build_id TEXT` | Optional exact build/hash identifier, stronger than the marketing version alone. |
| `release_channel` | `release_channel TEXT NOT NULL DEFAULT 'unknown'` | Channel such as stable, beta, rollback, or unknown. |
| `released_on` | `released_on TEXT` | Release date when known. |
| `is_primary_target` | `is_primary_target INTEGER NOT NULL DEFAULT 0 CHECK (is_primary_target IN (0,1))` | Marks the one version against which current revalidation queues are evaluated. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `version_span`

**Purpose and expected use.** Represents an exact version, bounded interval, or open-ended applicability range without repeating version lists. Triggers reject reversed bounds; the expansion view maps spans to concrete versions.

**Primary key.** `version_span_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(max_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT); `(min_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_version_span_bounds` — CREATE INDEX idx_version_span_bounds ON version_span(min_version_id, max_version_id).

**Triggers.** `trg_version_span_order_insert`, `trg_version_span_order_update`.

| Field | Declaration | Why it exists |
|---|---|---|
| `version_span_id` | `version_span_id INTEGER PRIMARY KEY` | Stable primary key for the `version_span` row. |
| `span_code` | `span_code TEXT NOT NULL UNIQUE` | Stable code used by data and queries for the applicability interval. |
| `span_name` | `span_name TEXT NOT NULL` | Readable interval name. |
| `min_version_id` | `min_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | Optional inclusive lower version bound. |
| `max_version_id` | `max_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | Optional inclusive upper version bound. |
| `boundary_note` | `boundary_note TEXT` | Explains open bounds, beta assumptions, or why the interval was chosen. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `item_type`

**Purpose and expected use.** Defines the allowed categories in the stable knowledge-item supertype. New broad categories can be added as rows while important mechanics continue to use typed sidecar tables.

**Primary key.** `item_type_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_type_id` | `item_type_id INTEGER PRIMARY KEY` | Stable primary key for the `item_type` row. |
| `type_code` | `type_code TEXT NOT NULL UNIQUE` | Stable category code used by sidecar checks, routing, and query filters. |
| `type_name` | `type_name TEXT NOT NULL` | Readable category label. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `object_kind`

**Purpose and expected use.** Classifies Stellaris scripted objects such as economic plans, AI budgets, country types, buildings, jobs, resources, and technologies, including their usual definition folder.

**Primary key.** `object_kind_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `object_kind_id` | `object_kind_id INTEGER PRIMARY KEY` | Stable primary key for the `object_kind` row. |
| `kind_code` | `kind_code TEXT NOT NULL UNIQUE` | Stable code for a class of Stellaris definition. |
| `kind_name` | `kind_name TEXT NOT NULL` | Readable object-class label. |
| `definition_folder` | `definition_folder TEXT` | Usual vanilla/mod folder used to route source lookup. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `script_symbol_kind`

**Purpose and expected use.** Classifies triggers, effects, scripted triggers/effects, modifiers, and defines. It allows one symbol catalog to support kind-specific lookup without flattening symbols into free text.

**Primary key.** `script_symbol_kind_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `script_symbol_kind_id` | `script_symbol_kind_id INTEGER PRIMARY KEY` | Stable primary key for the `script_symbol_kind` row. |
| `kind_code` | `kind_code TEXT NOT NULL UNIQUE` | Stable code for the script-surface category. |
| `kind_name` | `kind_name TEXT NOT NULL` | Readable script-surface category. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `claim_type`

**Purpose and expected use.** Classifies claim intent—behavior, structure, compatibility, process, hypothesis, or negative finding—so agents can filter and apply appropriate proof standards.

**Primary key.** `claim_type_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `claim_type_id` | `claim_type_id INTEGER PRIMARY KEY` | Stable primary key for the `claim_type` row. |
| `type_code` | `type_code TEXT NOT NULL UNIQUE` | Stable claim-intent code. |
| `type_name` | `type_name TEXT NOT NULL` | Readable claim-intent label. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `evidence_source_type`

**Purpose and expected use.** Defines evidence classes and their normal authority boundary, default reliability, and primary/secondary character. It records what a source may establish without claiming that one rank automatically proves a conclusion.

**Primary key.** `evidence_source_type_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `evidence_source_type_id` | `evidence_source_type_id INTEGER PRIMARY KEY` | Stable primary key for the `evidence_source_type` row. |
| `type_code` | `type_code TEXT NOT NULL UNIQUE` | Stable code used to classify or filter `evidence_source_type` rows. |
| `type_name` | `type_name TEXT NOT NULL` | Human-readable name for this `evidence_source_type` value. |
| `default_reliability_rank` | `default_reliability_rank INTEGER NOT NULL CHECK (default_reliability_rank BETWEEN 0 AND 100)` | Default comparative rank for triage; claim-level interpretation may override its practical weight. |
| `authoritative_scope` | `authoritative_scope TEXT` | Defines exactly what this source class can authoritatively establish. |
| `is_primary_evidence` | `is_primary_evidence INTEGER NOT NULL CHECK (is_primary_evidence IN (0,1))` | Marks whether this source class normally constitutes direct/primary evidence. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `locator_type`

**Purpose and expected use.** Defines the finite locator modalities supported by the evidence locator union: file lines, object keys, symbols, dataset records, logs, save fields, commits, URLs, and note sections.

**Primary key.** `locator_type_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `locator_type_id` | `locator_type_id INTEGER PRIMARY KEY` | Stable primary key for the `locator_type` row. |
| `type_code` | `type_code TEXT NOT NULL UNIQUE` | Stable code selecting a locator modality. |
| `type_name` | `type_name TEXT NOT NULL` | Readable locator-modality label. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `evidence_stance`

**Purpose and expected use.** Defines whether an evidence item supports, contradicts, qualifies, or merely contextualizes a claim, relation, or version change. This preserves disagreement instead of overwriting it.

**Primary key.** `evidence_stance_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `evidence_stance_id` | `evidence_stance_id INTEGER PRIMARY KEY` | Stable primary key for the `evidence_stance` row. |
| `stance_code` | `stance_code TEXT NOT NULL UNIQUE` | Stable directional code used by evidence joins and summaries. |
| `stance_name` | `stance_name TEXT NOT NULL` | Readable stance label. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `risk_level`

**Purpose and expected use.** Defines ordered impact/compatibility risk used by relationships, impact rules, and version changes. Risk is kept separate from confidence: a poorly understood edge can still be high risk.

**Primary key.** `risk_level_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `risk_level_id` | `risk_level_id INTEGER PRIMARY KEY` | Stable primary key for the `risk_level` row. |
| `risk_code` | `risk_code TEXT NOT NULL UNIQUE` | Stable risk code. |
| `risk_name` | `risk_name TEXT NOT NULL` | Readable risk label. |
| `rank_value` | `rank_value INTEGER NOT NULL UNIQUE CHECK (rank_value BETWEEN 0 AND 100)` | Comparable risk severity used to aggregate paths and order reviews. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `relation_type`

**Purpose and expected use.** Defines the semantics, inverse label, and impact-propagation direction of each graph edge type. This is the key control that turns semantic relationships into conservative change-impact arcs.

**Primary key.** `relation_type_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `relation_type_id` | `relation_type_id INTEGER PRIMARY KEY` | Stable primary key for the `relation_type` row. |
| `type_code` | `type_code TEXT NOT NULL UNIQUE` | Stable semantic edge code used in traversal and action rules. |
| `type_name` | `type_name TEXT NOT NULL` | Forward-readable relationship label. |
| `inverse_name` | `inverse_name TEXT` | Readable label when displaying the same stored edge in reverse. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |
| `impact_propagation_mode` | `impact_propagation_mode TEXT NOT NULL CHECK (impact_propagation_mode IN ('forward','reverse','both','none'))` | Controls whether a change traverses the stored edge forward, reverse, both ways, or not at all. |
| `is_transitive_hint` | `is_transitive_hint INTEGER NOT NULL DEFAULT 0 CHECK (is_transitive_hint IN (0,1))` | Signals that repeated traversal is normally meaningful; query depth and cycle guards still control expansion. |

#### `change_kind`

**Purpose and expected use.** Classifies observed game-version deltas as added, removed, modified, renamed, behavioral, or unknown.

**Primary key.** `change_kind_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `change_kind_id` | `change_kind_id INTEGER PRIMARY KEY` | Stable primary key for the `change_kind` row. |
| `kind_code` | `kind_code TEXT NOT NULL UNIQUE` | Stable version-delta classification code. |
| `kind_name` | `kind_name TEXT NOT NULL` | Readable delta classification. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `change_type`

**Purpose and expected use.** Classifies maintenance work—field, object, mechanic, subsystem, or version-port changes—for checklist selection.

**Primary key.** `change_type_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `change_type_id` | `change_type_id INTEGER PRIMARY KEY` | Stable primary key for the `change_type` row. |
| `type_code` | `type_code TEXT NOT NULL UNIQUE` | Stable maintenance-change category used to select checklists. |
| `type_name` | `type_name TEXT NOT NULL` | Readable maintenance-change category. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

#### `investigation_task_type`

**Purpose and expected use.** Defines normalized investigation tasks such as source lookup, schema validation, conflict inspection, version diffing, static validation, and runtime observation.

**Primary key.** `investigation_task_type_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** No outbound foreign keys; the table is a root or controlled vocabulary.

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `investigation_task_type_id` | `investigation_task_type_id INTEGER PRIMARY KEY` | Stable primary key for the `investigation_task_type` row. |
| `task_code` | `task_code TEXT NOT NULL UNIQUE` | Stable task code used by capabilities, impact rules, and checklist steps. |
| `task_name` | `task_name TEXT NOT NULL` | Readable investigation task. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |

### 2. Stable identities and typed Stellaris surfaces

This group gives every mechanic, subsystem, object, field, script surface, file, and typed mechanic detail a stable relational identity.

#### `knowledge_item`

**Purpose and expected use.** Provides the stable identity shared by mechanics, subsystems, objects, fields, symbols, scopes, files, tools, checklists, resources, technologies, and systems. Graph edges and claims target this supertype, while typed sidecars enforce domain-specific structure.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(retired_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(updated_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_by_actor_id)` → `actor(actor_id)` (ON DELETE RESTRICT); `(lifecycle_state_id)` → `lifecycle_state(lifecycle_state_id)` (ON DELETE RESTRICT); `(item_type_id)` → `item_type(item_type_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_knowledge_item_lifecycle` — CREATE INDEX idx_knowledge_item_lifecycle ON knowledge_item(lifecycle_state_id, item_type_id); `idx_knowledge_item_type_name` — CREATE INDEX idx_knowledge_item_type_name ON knowledge_item(item_type_id, display_name).

**Triggers.** `trg_knowledge_item_fts_ad`, `trg_knowledge_item_fts_ai`, `trg_knowledge_item_fts_au`.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY` | Stable primary key for the `knowledge_item` row. |
| `item_type_id` | `item_type_id INTEGER NOT NULL REFERENCES item_type(item_type_id) ON DELETE RESTRICT` | Classifies the stable item and drives typed lookup/routing. |
| `canonical_key` | `canonical_key TEXT NOT NULL UNIQUE` | Globally unique, namespaced identity that remains stable if display text or paths change. |
| `display_name` | `display_name TEXT NOT NULL` | Readable name for UI-less SQL results and reports. |
| `summary` | `summary TEXT NOT NULL` | Concise durable explanation of what the item represents. |
| `lifecycle_state_id` | `lifecycle_state_id INTEGER NOT NULL REFERENCES lifecycle_state(lifecycle_state_id) ON DELETE RESTRICT` | Selects the catalog lifecycle state. |
| `created_by_actor_id` | `created_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT` | Foreign key to the actor that created the record. |
| `created_at` | `created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))` | UTC timestamp when the stable item identity was introduced. |
| `updated_at` | `updated_at TEXT` | UTC timestamp of the latest in-place metadata correction; substantive knowledge changes use versioned child rows. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |
| `updated_in_change_set_id` | `updated_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that last corrected mutable catalog metadata. |
| `retired_in_change_set_id` | `retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that retired this row without deleting history. |

#### `item_alias`

**Purpose and expected use.** Stores version-aware alternate names, folder names, abbreviations, and informal terms for exact lookup without changing a stable canonical key.

**Primary key.** `item_alias_id`

**Table-level integrity rules.** `UNIQUE(item_id, alias_text, alias_kind, version_span_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_item_alias_lookup` — CREATE INDEX idx_item_alias_lookup ON item_alias(alias_text, alias_kind).

| Field | Declaration | Why it exists |
|---|---|---|
| `item_alias_id` | `item_alias_id INTEGER PRIMARY KEY` | Stable primary key for the `item_alias` row. |
| `item_id` | `item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `alias_text` | `alias_text TEXT NOT NULL` | Alternate term accepted for lookup. |
| `alias_kind` | `alias_kind TEXT NOT NULL` | Describes whether the alias is an abbreviation, folder name, informal term, old key, or another controlled project convention. |
| `version_span_id` | `version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `item_version_status`

**Purpose and expected use.** Records whether an item is present, absent, renamed, deprecated, changed, or unknown for a version span, together with evidence, confidence, and an append/supersede history.

**Primary key.** `item_version_status_id`

**Table-level integrity rules.** `CHECK (supersedes_item_version_status_id IS NULL OR supersedes_item_version_status_id <> item_version_status_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(supersedes_item_version_status_id)` → `item_version_status(item_version_status_id)` (ON DELETE RESTRICT); `(assessed_by_actor_id)` → `actor(actor_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(confidence_level_id)` → `confidence_level(confidence_level_id)` (ON DELETE RESTRICT); `(assessment_state_id)` → `assessment_state(assessment_state_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_item_version_status_evidence` — CREATE INDEX idx_item_version_status_evidence ON item_version_status(evidence_locator_id) WHERE evidence_locator_id IS NOT NULL; `idx_item_version_status_lookup` — CREATE INDEX idx_item_version_status_lookup ON item_version_status(item_id, version_span_id, is_current, status_code); `idx_item_version_status_state` — CREATE INDEX idx_item_version_status_state ON item_version_status(assessment_state_id, confidence_level_id, assessed_at); `uq_item_version_status_current_exact_span` — CREATE UNIQUE INDEX uq_item_version_status_current_exact_span ON item_version_status(item_id, version_span_id) WHERE is_current = 1.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_version_status_id` | `item_version_status_id INTEGER PRIMARY KEY` | Stable primary key for the `item_version_status` row. |
| `item_id` | `item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity represented or linked by this row. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `status_code` | `status_code TEXT NOT NULL CHECK (status_code IN ('present','absent','renamed','deprecated','changed','unknown'))` | Version-specific existence/change status: present, absent, renamed, deprecated, changed, or unknown. |
| `assessment_state_id` | `assessment_state_id INTEGER NOT NULL REFERENCES assessment_state(assessment_state_id) ON DELETE RESTRICT` | Selects the normalized epistemic state. |
| `confidence_level_id` | `confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT` | Selects the normalized confidence level. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `assessed_by_actor_id` | `assessed_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT` | Foreign key to the actor responsible for the assessment. |
| `assessed_at` | `assessed_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))` | UTC time at which this status conclusion was made. |
| `basis_summary` | `basis_summary TEXT NOT NULL` | Short reasoning that justifies the status and points readers toward evidence. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |
| `is_current` | `is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1))` | Marks the non-retired status row for an exact item/span. |
| `supersedes_item_version_status_id` | `supersedes_item_version_status_id INTEGER REFERENCES item_version_status(item_version_status_id) ON DELETE RESTRICT` | References the previous item-status row in the append-only chain. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `mechanic_family`

**Purpose and expected use.** Adds typed fields for broad mechanic families, keeping taxonomy separate from individual mechanics and their evidence.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `family_code` | `family_code TEXT NOT NULL UNIQUE` | Stable short code for the family. |
| `domain_summary` | `domain_summary TEXT NOT NULL` | Defines the family boundary and included mechanics. |

#### `mechanic`

**Purpose and expected use.** Adds mechanic-specific purpose, visibility boundary, family, and owner scope to a knowledge item. It distinguishes script-visible, partly visible, hidden, and unknown engine behavior.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(owner_scope_item_id)` → `script_scope(item_id)` (ON DELETE RESTRICT); `(mechanic_family_item_id)` → `mechanic_family(item_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_mechanic_family` — CREATE INDEX idx_mechanic_family ON mechanic(mechanic_family_item_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `mechanic_family_item_id` | `mechanic_family_item_id INTEGER NOT NULL REFERENCES mechanic_family(item_id) ON DELETE RESTRICT` | Places the mechanic in a typed mechanic family. |
| `purpose` | `purpose TEXT NOT NULL` | Explains the mechanic’s role in Stellaris or the mod. |
| `engine_visibility` | `engine_visibility TEXT NOT NULL CHECK (engine_visibility IN ('script_visible','partially_script_visible','hardcoded_or_hidden','unknown'))` | States whether behavior is directly scripted, partly exposed, hidden/hardcoded, or not yet known. |
| `owner_scope_item_id` | `owner_scope_item_id INTEGER REFERENCES script_scope(item_id) ON DELETE RESTRICT` | References the normal owner/current scope of the mechanic. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `subsystem`

**Purpose and expected use.** Represents a maintainable subsystem of the target mod, including its repository focus and acceptance criteria. Checklists and impact paths can target the subsystem as a planning unit.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `subsystem_code` | `subsystem_code TEXT NOT NULL UNIQUE` | Stable code for planning and checklist selection. |
| `purpose` | `purpose TEXT NOT NULL` | Defines the subsystem’s responsibility. |
| `primary_repository_path` | `primary_repository_path TEXT` | Main repository location to inspect; it is a route hint, not copied file data. |
| `acceptance_summary` | `acceptance_summary TEXT` | States the subsystem-level definition of done. |

#### `game_object`

**Purpose and expected use.** Represents a concrete vanilla, mod, generated, or external-mod scripted definition by object kind, script key, namespace, and origin class.

**Primary key.** `item_id`

**Table-level integrity rules.** `UNIQUE(object_kind_id, script_key, namespace, origin_class)`.

**Relationships.** `(object_kind_id)` → `object_kind(object_kind_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_game_object_script_key` — CREATE INDEX idx_game_object_script_key ON game_object(script_key, object_kind_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `object_kind_id` | `object_kind_id INTEGER NOT NULL REFERENCES object_kind(object_kind_id) ON DELETE RESTRICT` | Classifies the Stellaris object definition. |
| `script_key` | `script_key TEXT NOT NULL` | Exact Stellaris object key used in source definitions. |
| `namespace` | `namespace TEXT NOT NULL DEFAULT ''` | Optional namespace needed to distinguish otherwise identical keys. |
| `origin_class` | `origin_class TEXT NOT NULL CHECK (origin_class IN ('vanilla','mod','generated','external_mod','unknown'))` | Distinguishes vanilla, target-mod, generated, external-mod, and unknown objects. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `file_asset`

**Purpose and expected use.** Represents a precise file or corpus-relative path as a graph-addressable item. It stores only identity and role, not the file contents, preserving existing tools as authoritative.

**Primary key.** `item_id`

**Table-level integrity rules.** `UNIQUE(corpus_code, relative_path)`.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_file_asset_path` — CREATE INDEX idx_file_asset_path ON file_asset(relative_path).

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `corpus_code` | `corpus_code TEXT NOT NULL` | Identifies the owning corpus, such as vanilla-4.4.5 or repository. |
| `relative_path` | `relative_path TEXT NOT NULL` | Portable path within the corpus; absolute roots remain in source_system. |
| `file_role` | `file_role TEXT NOT NULL` | Describes whether the file defines, validates, documents, or reports the item. |
| `load_order_note` | `load_order_note TEXT` | Captures overwrite/ordering caveats without pretending to replace Irony evidence. |

#### `script_symbol`

**Purpose and expected use.** Represents a trigger, effect, modifier, define, or scripted symbol by stable key, kind, namespace, and exposure class.

**Primary key.** `item_id`

**Table-level integrity rules.** `UNIQUE(script_symbol_kind_id, symbol_key, namespace)`.

**Relationships.** `(script_symbol_kind_id)` → `script_symbol_kind(script_symbol_kind_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_script_symbol_key` — CREATE INDEX idx_script_symbol_key ON script_symbol(symbol_key, script_symbol_kind_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `script_symbol_kind_id` | `script_symbol_kind_id INTEGER NOT NULL REFERENCES script_symbol_kind(script_symbol_kind_id) ON DELETE RESTRICT` | Classifies the symbol as trigger, effect, scripted surface, modifier, or define. |
| `symbol_key` | `symbol_key TEXT NOT NULL` | Exact trigger/effect/modifier/define key. |
| `namespace` | `namespace TEXT NOT NULL DEFAULT ''` | Optional namespace for scripted symbols. |
| `exposure_class` | `exposure_class TEXT NOT NULL CHECK (exposure_class IN ('built_in','scripted','define','generated','unknown'))` | Distinguishes built-in, scripted, define, generated, and unknown exposure. |
| `description` | `description TEXT` | Readable definition of the row’s controlled meaning. |

#### `field_definition`

**Purpose and expected use.** Defines a reusable field concept for an object kind, including its baseline type, cardinality, and semantics. Version-specific changes belong in field_revision rather than overwriting the catalog row.

**Primary key.** `item_id`

**Table-level integrity rules.** `UNIQUE(owner_object_kind_id, field_name)`.

**Relationships.** `(owner_object_kind_id)` → `object_kind(object_kind_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `owner_object_kind_id` | `owner_object_kind_id INTEGER NOT NULL REFERENCES object_kind(object_kind_id) ON DELETE RESTRICT` | Defines which object class owns this field. |
| `field_name` | `field_name TEXT NOT NULL` | Exact field name within the owner object kind. |
| `value_type` | `value_type TEXT NOT NULL` | Baseline expected value type for static lookup and validation. |
| `cardinality` | `cardinality TEXT NOT NULL` | Baseline multiplicity, such as scalar, optional, or repeated. |
| `semantic_summary` | `semantic_summary TEXT NOT NULL` | Baseline meaning independent of a specific source revision. |

#### `field_revision`

**Purpose and expected use.** Captures evidence-backed, version-specific field semantics, type, cardinality, and status. Multiple source systems can independently describe the same field and be reconciled through claims.

**Primary key.** `field_revision_id`

**Table-level integrity rules.** `UNIQUE(field_item_id, version_span_id, source_system_id, evidence_locator_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(source_system_id)` → `source_system(source_system_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(field_item_id)` → `field_definition(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_field_revision_lookup` — CREATE INDEX idx_field_revision_lookup ON field_revision(field_item_id, version_span_id, status_code).

| Field | Declaration | Why it exists |
|---|---|---|
| `field_revision_id` | `field_revision_id INTEGER PRIMARY KEY` | Stable primary key for the `field_revision` row. |
| `field_item_id` | `field_item_id INTEGER NOT NULL REFERENCES field_definition(item_id) ON DELETE RESTRICT` | References the typed field definition. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `source_system_id` | `source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT` | References the evidence system from which the row was retrieved. |
| `evidence_locator_id` | `evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `value_type` | `value_type TEXT NOT NULL` | Source- and version-specific field type. |
| `cardinality` | `cardinality TEXT NOT NULL` | Source- and version-specific multiplicity. |
| `semantic_summary` | `semantic_summary TEXT NOT NULL` | Evidence-backed semantics for the stated version/source. |
| `status_code` | `status_code TEXT NOT NULL CHECK (status_code IN ('present','absent','deprecated','changed','unknown'))` | Whether this revision says the field is present, absent, deprecated, changed, or unknown. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `script_scope`

**Purpose and expected use.** Represents a Stellaris script scope as a typed item so mechanics, symbols, and validation rules can refer to it relationally.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `scope_key` | `scope_key TEXT NOT NULL UNIQUE` | Stable project key for the scope. |
| `engine_scope_name` | `engine_scope_name TEXT` | Exact engine/documentation name when it differs from the project key. |
| `scope_summary` | `scope_summary TEXT NOT NULL` | Explains what object is in scope and how it is used. |

#### `script_symbol_revision`

**Purpose and expected use.** Records versioned signatures, values, behavior summaries, and presence status for triggers, effects, modifiers, and defines.

**Primary key.** `script_symbol_revision_id`

**Table-level integrity rules.** `UNIQUE(script_symbol_item_id, version_span_id, source_system_id, revision_kind, evidence_locator_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(source_system_id)` → `source_system(source_system_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(script_symbol_item_id)` → `script_symbol(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_symbol_revision_lookup` — CREATE INDEX idx_symbol_revision_lookup ON script_symbol_revision(script_symbol_item_id, version_span_id, status_code).

| Field | Declaration | Why it exists |
|---|---|---|
| `script_symbol_revision_id` | `script_symbol_revision_id INTEGER PRIMARY KEY` | Stable primary key for the `script_symbol_revision` row. |
| `script_symbol_item_id` | `script_symbol_item_id INTEGER NOT NULL REFERENCES script_symbol(item_id) ON DELETE RESTRICT` | References the typed script symbol. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `source_system_id` | `source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT` | References the evidence system from which the row was retrieved. |
| `evidence_locator_id` | `evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `revision_kind` | `revision_kind TEXT NOT NULL` | Names the revision facet, such as signature, define value, or behavior contract. |
| `signature_text` | `signature_text TEXT` | Versioned invocation signature when applicable. |
| `value_text` | `value_text TEXT` | Versioned scalar/text value, especially for defines or documented defaults. |
| `behavior_summary` | `behavior_summary TEXT` | Versioned behavior explanation supported by the locator. |
| `status_code` | `status_code TEXT NOT NULL CHECK (status_code IN ('present','absent','deprecated','changed','unknown'))` | Presence/deprecation/change status for the symbol revision. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `symbol_scope_rule`

**Purpose and expected use.** Records evidence-backed scope roles for a symbol—such as required current scope, target scope, or output scope—for a version span.

**Primary key.** `symbol_scope_rule_id`

**Table-level integrity rules.** `UNIQUE(script_symbol_item_id, scope_item_id, role_code, version_span_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(scope_item_id)` → `script_scope(item_id)` (ON DELETE RESTRICT); `(script_symbol_item_id)` → `script_symbol(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_symbol_scope_by_scope` — CREATE INDEX idx_symbol_scope_by_scope ON symbol_scope_rule(scope_item_id, version_span_id, role_code).

| Field | Declaration | Why it exists |
|---|---|---|
| `symbol_scope_rule_id` | `symbol_scope_rule_id INTEGER PRIMARY KEY` | Stable primary key for the `symbol_scope_rule` row. |
| `script_symbol_item_id` | `script_symbol_item_id INTEGER NOT NULL REFERENCES script_symbol(item_id) ON DELETE RESTRICT` | References the typed script symbol. |
| `scope_item_id` | `scope_item_id INTEGER NOT NULL REFERENCES script_scope(item_id) ON DELETE RESTRICT` | References the typed Stellaris scope. |
| `role_code` | `role_code TEXT NOT NULL` | Identifies how the scope participates, such as current, target, parameter, or output scope. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `rule_summary` | `rule_summary TEXT NOT NULL` | Explains the scope rule and any conditions. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `symbol_parameter`

**Purpose and expected use.** Records versioned, typed parameters for script symbols, including required/default behavior. It supports structured invocation and validation assistance.

**Primary key.** `symbol_parameter_id`

**Table-level integrity rules.** `UNIQUE(script_symbol_item_id, parameter_name, version_span_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(script_symbol_item_id)` → `script_symbol(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `symbol_parameter_id` | `symbol_parameter_id INTEGER PRIMARY KEY` | Stable primary key for the `symbol_parameter` row. |
| `script_symbol_item_id` | `script_symbol_item_id INTEGER NOT NULL REFERENCES script_symbol(item_id) ON DELETE RESTRICT` | References the typed script symbol. |
| `parameter_name` | `parameter_name TEXT NOT NULL` | Exact parameter name. |
| `value_type` | `value_type TEXT NOT NULL` | Expected parameter type. |
| `is_required` | `is_required INTEGER NOT NULL CHECK (is_required IN (0,1))` | States whether the parameter must be supplied. |
| `default_value_text` | `default_value_text TEXT` | Documented/default value when one exists. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `description` | `description TEXT NOT NULL` | Readable definition of the row’s controlled meaning. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `ai_budget_mechanic_detail`

**Purpose and expected use.** Demonstrates a normalized, versioned mechanic-specific sidecar for AI budgets. It stores allocation stages and behaviors that do not belong in the generic mechanic table.

**Primary key.** `ai_budget_mechanic_detail_id`

**Table-level integrity rules.** `UNIQUE(mechanic_item_id, version_span_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(basis_claim_id)` → `claim(claim_id)` (ON DELETE RESTRICT); `(budget_owner_scope_item_id)` → `script_scope(item_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(mechanic_item_id)` → `mechanic(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `ai_budget_mechanic_detail_id` | `ai_budget_mechanic_detail_id INTEGER PRIMARY KEY` | Stable primary key for the `ai_budget_mechanic_detail` row. |
| `mechanic_item_id` | `mechanic_item_id INTEGER NOT NULL REFERENCES mechanic(item_id) ON DELETE RESTRICT` | References the typed mechanic described by this sidecar. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `budget_owner_scope_item_id` | `budget_owner_scope_item_id INTEGER REFERENCES script_scope(item_id) ON DELETE RESTRICT` | References the scope that owns or evaluates the budget. |
| `allocation_unit` | `allocation_unit TEXT NOT NULL` | Describes the unit or basis allocated by the budget mechanic. |
| `allocation_stage` | `allocation_stage TEXT NOT NULL` | Names the planning/allocation stage in which the budget applies. |
| `reserve_behavior` | `reserve_behavior TEXT` | Versioned description of reserve handling. |
| `exhaustion_behavior` | `exhaustion_behavior TEXT` | Versioned description of behavior when the budget or reserve is exhausted. |
| `basis_claim_id` | `basis_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT` | References the claim supporting the typed detail row. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

### 3. Repository, mod-release, playset, and execution context

This group captures the actual repository, mod releases, active playset order, and execution conditions under which conclusions apply.

#### `repository_snapshot`

**Purpose and expected use.** Captures the exact repository branch, commit, worktree state, and capture time that bound a body of knowledge. It prevents a later dirty checkout from being mistaken for the source state that produced an artifact or conclusion.

**Primary key.** `repository_snapshot_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_repository_snapshot_commit` — CREATE INDEX idx_repository_snapshot_commit ON repository_snapshot(commit_sha, branch_name, captured_at).

| Field | Declaration | Why it exists |
|---|---|---|
| `repository_snapshot_id` | `repository_snapshot_id INTEGER PRIMARY KEY` | Stable primary key for the `repository_snapshot` row. |
| `snapshot_key` | `snapshot_key TEXT NOT NULL UNIQUE` | Stable machine key for the captured checkout state. |
| `repository_name` | `repository_name TEXT NOT NULL` | Human-readable name used in query results and review output while the machine key remains stable. |
| `repository_root` | `repository_root TEXT` | Optional local root used to retrieve files; portable queries should prefer snapshot_key plus repository-relative paths. |
| `branch_name` | `branch_name TEXT` | Branch captured with the snapshot so branch-specific work is not conflated. |
| `commit_sha` | `commit_sha TEXT` | Exact Git commit used to bind source evidence and generated outputs. |
| `worktree_state` | `worktree_state TEXT NOT NULL CHECK (worktree_state IN ('clean','dirty','unknown'))` | Records clean, dirty, or unknown because uncommitted files may differ from the commit. |
| `captured_at` | `captured_at TEXT NOT NULL` | Timestamp at which branch, commit, and worktree state were observed. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `mod_package`

**Purpose and expected use.** Adds stable mod identity and Workshop/project scope to a knowledge item. It lets playsets, releases, dependencies, compatibility claims, and source roots refer to one mod without repeating names or Steam IDs.

**Primary key.** `item_id`

**Table-level integrity rules.** `UNIQUE(steam_workshop_id)`.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | Stable primary key for the `mod_package` row. |
| `mod_key` | `mod_key TEXT NOT NULL UNIQUE` | Stable project key for the mod independent of display name or release. |
| `steam_workshop_id` | `steam_workshop_id TEXT` | Workshop remote ID when applicable; unique to prevent duplicate mod identities. |
| `mod_scope` | `mod_scope TEXT NOT NULL CHECK (mod_scope IN ('vanilla','project_mod','workshop_mod','compatibility_patch','reference_mod','utility','unknown'))` | Distinguishes vanilla, project mod, Workshop mod, compatibility patch, reference mod, utility, or unknown. |
| `author_or_owner` | `author_or_owner TEXT` | Stores the structured `author_or_owner` attribute required to interpret, route, retrieve, or validate the row. |
| `homepage_uri` | `homepage_uri TEXT` | Stores the structured `homepage_uri` attribute required to interpret, route, retrieve, or validate the row. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `mod_release`

**Purpose and expected use.** Represents one captured release or revision of a mod, including supported-game metadata and descriptor provenance. Object definitions and source roots attach to this release rather than to an ahistorical mod identity.

**Primary key.** `mod_release_id`

**Table-level integrity rules.** `UNIQUE(mod_item_id, version_text, captured_at)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(descriptor_artifact_id)` → `source_artifact(source_artifact_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(mod_item_id)` → `mod_package(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_mod_release_mod_version` — CREATE INDEX idx_mod_release_mod_version ON mod_release(mod_item_id, version_span_id, release_status).

| Field | Declaration | Why it exists |
|---|---|---|
| `mod_release_id` | `mod_release_id INTEGER PRIMARY KEY` | Stable primary key for the `mod_release` row. |
| `mod_item_id` | `mod_item_id INTEGER NOT NULL REFERENCES mod_package(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `mod_release` role (`mod_package.item_id`). |
| `release_key` | `release_key TEXT NOT NULL UNIQUE` | Stable identity for one captured release/revision. |
| `version_text` | `version_text TEXT` | Preserves the exact text/expression needed for review without substituting it for typed relational facts. |
| `version_span_id` | `version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Foreign key to `version_span.version_span_id`, preserving normalized identity and referential integrity. |
| `supported_game_pattern` | `supported_game_pattern TEXT` | Descriptor-facing version pattern such as v4.4.*; it is metadata, not proof that scripts load. |
| `remote_file_id` | `remote_file_id TEXT` | Normalized identifier linking this row to the named parent, target, or controlled entity. |
| `descriptor_artifact_id` | `descriptor_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT` | Points to the exact descriptor artifact supporting release metadata. |
| `captured_at` | `captured_at TEXT` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `release_status` | `release_status TEXT NOT NULL CHECK (release_status IN ('active','historical','missing','superseded','unknown'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `source_root`

**Purpose and expected use.** Names a retrievable root such as the repository, exact vanilla install, Workshop snapshot, project mod, log folder, save staging folder, or generated-output folder. It is the context anchor for paths that are otherwise ambiguous.

**Primary key.** `source_root_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(game_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT); `(mod_release_id)` → `mod_release(mod_release_id)` (ON DELETE RESTRICT); `(repository_snapshot_id)` → `repository_snapshot(repository_snapshot_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_source_root_context` — CREATE INDEX idx_source_root_context ON source_root(root_kind, game_version_id, mod_release_id, repository_snapshot_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `source_root_id` | `source_root_id INTEGER PRIMARY KEY` | Stable primary key for the `source_root` row. |
| `root_key` | `root_key TEXT NOT NULL UNIQUE` | Portable identity for the root even when the local absolute path changes. |
| `root_kind` | `root_kind TEXT NOT NULL CHECK (root_kind IN ('repository','vanilla_install','workshop_live','mod_snapshot','project_mod','launcher','logs','saves','generated','research','web_cache','other'))` | Classifies repository, vanilla, Workshop, snapshot, launcher, logs, saves, generated, research, or other roots. |
| `canonical_path` | `canonical_path TEXT NOT NULL` | Exact local or mounted root used for retrieval at capture time. |
| `repository_snapshot_id` | `repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT` | Foreign key to `repository_snapshot.repository_snapshot_id`, preserving normalized identity and referential integrity. |
| `mod_release_id` | `mod_release_id INTEGER REFERENCES mod_release(mod_release_id) ON DELETE RESTRICT` | Foreign key to `mod_release.mod_release_id`, preserving normalized identity and referential integrity. |
| `game_version_id` | `game_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | Foreign key to `game_version.game_version_id`, preserving normalized identity and referential integrity. |
| `captured_at` | `captured_at TEXT` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `availability_status` | `availability_status TEXT NOT NULL CHECK (availability_status IN ('available','missing','moved','archived','unknown'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `content_hash_algorithm` | `content_hash_algorithm TEXT` | Hash/fingerprint metadata used to validate identity and detect source or schema drift. |
| `content_hash_value` | `content_hash_value TEXT` | Hash/fingerprint metadata used to validate identity and detect source or schema drift. |
| `authoritative_for` | `authoritative_for TEXT` | Concise durable explanation needed to interpret the normalized row and its evidence boundary. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `playset`

**Purpose and expected use.** Provides the stable identity of a logical playset. Mutable membership and order are deliberately stored in snapshots so historical evidence is not rewritten when the active list changes.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | Stable primary key for the `playset` row. |
| `playset_key` | `playset_key TEXT NOT NULL UNIQUE` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `manager_name` | `manager_name TEXT` | Human-readable name used in query results and review output while the machine key remains stable. |
| `purpose` | `purpose TEXT NOT NULL` | Concise durable explanation needed to interpret the normalized row and its evidence boundary. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `playset_snapshot`

**Purpose and expected use.** Captures one versioned playset membership/order state together with game version, repository snapshot, source artifact, and resolution status. This is the unit against which active winners and conflicts are meaningful.

**Primary key.** `playset_snapshot_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(source_artifact_id)` → `source_artifact(source_artifact_id)` (ON DELETE RESTRICT); `(repository_snapshot_id)` → `repository_snapshot(repository_snapshot_id)` (ON DELETE RESTRICT); `(game_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT); `(playset_item_id)` → `playset(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_playset_snapshot_version` — CREATE INDEX idx_playset_snapshot_version ON playset_snapshot(game_version_id, captured_at); `uq_playset_snapshot_current` — CREATE UNIQUE INDEX uq_playset_snapshot_current ON playset_snapshot(playset_item_id) WHERE is_current = 1.

| Field | Declaration | Why it exists |
|---|---|---|
| `playset_snapshot_id` | `playset_snapshot_id INTEGER PRIMARY KEY` | Stable primary key for the `playset_snapshot` row. |
| `playset_item_id` | `playset_item_id INTEGER NOT NULL REFERENCES playset(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `playset_snapshot` role (`playset.item_id`). |
| `snapshot_key` | `snapshot_key TEXT NOT NULL UNIQUE` | Stable key for a captured membership/order state. |
| `game_version_id` | `game_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | Foreign key to `game_version.game_version_id`, preserving normalized identity and referential integrity. |
| `repository_snapshot_id` | `repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT` | Foreign key to `repository_snapshot.repository_snapshot_id`, preserving normalized identity and referential integrity. |
| `source_artifact_id` | `source_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT` | Foreign key to `source_artifact.source_artifact_id`, preserving normalized identity and referential integrity. |
| `captured_at` | `captured_at TEXT NOT NULL` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `declared_mod_count` | `declared_mod_count INTEGER CHECK (declared_mod_count IS NULL OR declared_mod_count >= 0)` | Expected member count for coverage and truncation checks. |
| `is_current` | `is_current INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1))` | Strict 0/1 flag for the named state so agents do not infer it from prose. |
| `resolution_status` | `resolution_status TEXT NOT NULL CHECK (resolution_status IN ('captured','validated','partial','stale','unknown'))` | Reports whether order/membership/winner resolution was validated, partial, failed, or unknown. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `playset_member`

**Purpose and expected use.** Stores one mod release/source root at one load position in a playset snapshot, including project-required status and separately reported live-launch state. It supports exact load-order queries without copying Irony data wholesale.

**Primary key.** `playset_member_id`

**Table-level integrity rules.** `UNIQUE(playset_snapshot_id, mod_release_id)`; `UNIQUE(playset_snapshot_id, load_position)`.

**Relationships.** `(source_root_id)` → `source_root(source_root_id)` (ON DELETE RESTRICT); `(mod_release_id)` → `mod_release(mod_release_id)` (ON DELETE RESTRICT); `(playset_snapshot_id)` → `playset_snapshot(playset_snapshot_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_playset_member_order` — CREATE INDEX idx_playset_member_order ON playset_member(playset_snapshot_id, enabled, load_position).

| Field | Declaration | Why it exists |
|---|---|---|
| `playset_member_id` | `playset_member_id INTEGER PRIMARY KEY` | Stable primary key for the `playset_member` row. |
| `playset_snapshot_id` | `playset_snapshot_id INTEGER NOT NULL REFERENCES playset_snapshot(playset_snapshot_id) ON DELETE CASCADE` | Foreign key to `playset_snapshot.playset_snapshot_id`, preserving normalized identity and referential integrity. |
| `mod_release_id` | `mod_release_id INTEGER NOT NULL REFERENCES mod_release(mod_release_id) ON DELETE RESTRICT` | Foreign key to `mod_release.mod_release_id`, preserving normalized identity and referential integrity. |
| `source_root_id` | `source_root_id INTEGER REFERENCES source_root(source_root_id) ON DELETE RESTRICT` | Foreign key to `source_root.source_root_id`, preserving normalized identity and referential integrity. |
| `load_position` | `load_position INTEGER NOT NULL CHECK (load_position >= 1)` | One-based captured order used to resolve overwrite and conflict precedence. |
| `enabled` | `enabled INTEGER NOT NULL DEFAULT 1 CHECK (enabled IN (0,1))` | Strict 0/1 flag for the named state so agents do not infer it from prose. |
| `required_by_project` | `required_by_project INTEGER NOT NULL DEFAULT 0 CHECK (required_by_project IN (0,1))` | Marks required parents/utilities separately from merely enabled optional integrations. |
| `descriptor_path` | `descriptor_path TEXT` | Retrieval or execution path kept separate from stable logical identity. |
| `live_load_state` | `live_load_state TEXT NOT NULL DEFAULT 'unknown' CHECK (live_load_state IN ('loaded','disabled','missing','unknown'))` | Separates source/captured membership from proof that the launcher will load it next launch. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `execution_context`

**Purpose and expected use.** Binds claims, assessments, verification runs, and analysis to the combination of game version, repository snapshot, playset snapshot, run mode, platform, checksum, and settings. It prevents observer evidence from silently applying to normal play or another stack.

**Primary key.** `execution_context_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(playset_snapshot_id)` → `playset_snapshot(playset_snapshot_id)` (ON DELETE RESTRICT); `(repository_snapshot_id)` → `repository_snapshot(repository_snapshot_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(game_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_execution_context_lookup` — CREATE INDEX idx_execution_context_lookup ON execution_context(game_version_id, playset_snapshot_id, repository_snapshot_id, run_mode).

| Field | Declaration | Why it exists |
|---|---|---|
| `execution_context_id` | `execution_context_id INTEGER PRIMARY KEY` | Stable primary key for the `execution_context` row. |
| `context_key` | `context_key TEXT NOT NULL UNIQUE` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `title` | `title TEXT NOT NULL` | Human-readable name used in query results and review output while the machine key remains stable. |
| `game_version_id` | `game_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | Foreign key to `game_version.game_version_id`, preserving normalized identity and referential integrity. |
| `version_span_id` | `version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Foreign key to `version_span.version_span_id`, preserving normalized identity and referential integrity. |
| `repository_snapshot_id` | `repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT` | Foreign key to `repository_snapshot.repository_snapshot_id`, preserving normalized identity and referential integrity. |
| `playset_snapshot_id` | `playset_snapshot_id INTEGER REFERENCES playset_snapshot(playset_snapshot_id) ON DELETE RESTRICT` | Foreign key to `playset_snapshot.playset_snapshot_id`, preserving normalized identity and referential integrity. |
| `run_mode` | `run_mode TEXT NOT NULL CHECK (run_mode IN ('static','normal_game','observer','save_analysis','log_analysis','research','database_validation','unknown'))` | Separates static, normal game, observer, save analysis, log analysis, research, and database-validation evidence. |
| `platform` | `platform TEXT` | Stores the normalized `platform` attribute needed to query and maintain `execution_context` records without an EAV or JSON fallback. |
| `game_checksum` | `game_checksum TEXT` | Optional exact game checksum when a runtime or build supplied it. |
| `settings_summary` | `settings_summary TEXT` | Concise durable explanation needed to interpret the normalized row and its evidence boundary. |
| `created_at` | `created_at TEXT NOT NULL` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `is_current` | `is_current INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1))` | Strict 0/1 flag for the named state so agents do not infer it from prose. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `execution_context_item`

**Purpose and expected use.** Adds normalized DLC, settings, assumptions, target subsystems, comparison baselines, and explicit exclusions to an execution context. It avoids an uncontrolled context JSON blob while remaining extensible through stable items.

**Primary key.** `execution_context_id`, `item_id`, `role_code`

**Table-level integrity rules.** `PRIMARY KEY(execution_context_id, item_id, role_code)`.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(execution_context_id)` → `execution_context(execution_context_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_execution_context_item_item` — CREATE INDEX idx_execution_context_item_item ON execution_context_item(item_id, role_code, execution_context_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `execution_context_id` | `execution_context_id INTEGER NOT NULL REFERENCES execution_context(execution_context_id) ON DELETE CASCADE` | Stable primary key for the `execution_context_item` row. |
| `item_id` | `item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | Stable primary key for the `execution_context_item` row. |
| `role_code` | `role_code TEXT NOT NULL CHECK (role_code IN ('enabled_dlc','required_dlc','assumption','setting','target_subsystem','comparison_baseline','excluded_item','other'))` | Controlled role for DLC, setting, assumption, target, baseline, or exclusion. |
| `state_code` | `state_code TEXT` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `playset_object_resolution`

**Purpose and expected use.** Stores the winning definition, ambiguity, or missing status for one object in one playset snapshot. Winning is therefore contextual and never an intrinsic property of an object-definition occurrence.

**Primary key.** `playset_object_resolution_id`

**Table-level integrity rules.** `UNIQUE(playset_snapshot_id, object_item_id)`.

**Relationships.** `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(resolver_tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(winning_definition_id)` → `object_definition(object_definition_id)` (ON DELETE RESTRICT); `(object_item_id)` → `game_object(item_id)` (ON DELETE RESTRICT); `(playset_snapshot_id)` → `playset_snapshot(playset_snapshot_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_playset_resolution_winner` — CREATE INDEX idx_playset_resolution_winner ON playset_object_resolution(playset_snapshot_id, winning_definition_id, resolution_status).

**Triggers.** `trg_playset_resolution_winner_object_insert`, `trg_playset_resolution_winner_object_update`.

| Field | Declaration | Why it exists |
|---|---|---|
| `playset_object_resolution_id` | `playset_object_resolution_id INTEGER PRIMARY KEY` | Stable primary key for the `playset_object_resolution` row. |
| `playset_snapshot_id` | `playset_snapshot_id INTEGER NOT NULL REFERENCES playset_snapshot(playset_snapshot_id) ON DELETE CASCADE` | Foreign key to `playset_snapshot.playset_snapshot_id`, preserving normalized identity and referential integrity. |
| `object_item_id` | `object_item_id INTEGER NOT NULL REFERENCES game_object(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `playset_object_resolution` role (`game_object.item_id`). |
| `winning_definition_id` | `winning_definition_id INTEGER REFERENCES object_definition(object_definition_id) ON DELETE RESTRICT` | Definition occurrence that wins in this exact playset snapshot; nullable for ambiguous/missing cases. |
| `resolution_status` | `resolution_status TEXT NOT NULL CHECK (resolution_status IN ('single','resolved','ambiguous','missing','not_applicable','unknown'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `resolver_tool_item_id` | `resolver_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `playset_object_resolution` role (`tool.item_id`). |
| `resolution_method` | `resolution_method TEXT NOT NULL` | Explains whether the result came from Irony, generated winner logic, manual review, or another method. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Foreign key to `evidence_locator.evidence_locator_id`, preserving normalized identity and referential integrity. |
| `review_required` | `review_required INTEGER NOT NULL CHECK (review_required IN (0,1))` | Flags winner results that remain unsafe to consume without human/source review. |
| `resolved_at` | `resolved_at TEXT` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

### 4. Evidence, external datasets, definitions, conflicts, and validation

This group preserves retrievable provenance, complete external schemas, object occurrences/references, winner conflicts, and validation results.

#### `source_system`

**Purpose and expected use.** Defines an authoritative or investigative evidence system—vanilla files, generated docs, CWTools, Irony, repository, logs, saves, Munch tools, or web sources—and how to retrieve evidence from it.

**Primary key.** `source_system_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(default_tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(evidence_source_type_id)` → `evidence_source_type(evidence_source_type_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_source_system_type` — CREATE INDEX idx_source_system_type ON source_system(evidence_source_type_id, system_name).

| Field | Declaration | Why it exists |
|---|---|---|
| `source_system_id` | `source_system_id INTEGER PRIMARY KEY` | Stable primary key for the `source_system` row. |
| `system_key` | `system_key TEXT NOT NULL UNIQUE` | Stable identifier for the evidence system. |
| `system_name` | `system_name TEXT NOT NULL` | Readable evidence-system name. |
| `evidence_source_type_id` | `evidence_source_type_id INTEGER NOT NULL REFERENCES evidence_source_type(evidence_source_type_id) ON DELETE RESTRICT` | Classifies the source system’s evidence type and authority boundary. |
| `canonical_root` | `canonical_root TEXT` | Root path, URI, index name, or repository base needed to resolve artifact locations. |
| `access_mode` | `access_mode TEXT NOT NULL` | How the source is accessed, such as filesystem, tool, index, Git, or web. |
| `authoritative_for` | `authoritative_for TEXT` | Concrete authority boundary for this exact source system. |
| `default_tool_item_id` | `default_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the default tool for retrieving evidence from this system. |
| `retrieval_instructions` | `retrieval_instructions TEXT NOT NULL` | Default procedure for recovering and validating evidence from the system. |
| `is_local_only` | `is_local_only INTEGER NOT NULL CHECK (is_local_only IN (0,1))` | Distinguishes sources that cannot be resolved outside the local workstation. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `source_artifact`

**Purpose and expected use.** Identifies one concrete retrievable file, report, save, log, web capture, generated dataset, or descriptor inside a source system and optional root/repository/mod-release context. It stores identity metadata and availability, not the corpus contents.

**Primary key.** `source_artifact_id`

**Table-level integrity rules.** `UNIQUE(source_system_id, stable_key)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(game_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT); `(mod_release_id)` → `mod_release(mod_release_id)` (ON DELETE RESTRICT); `(repository_snapshot_id)` → `repository_snapshot(repository_snapshot_id)` (ON DELETE RESTRICT); `(source_root_id)` → `source_root(source_root_id)` (ON DELETE RESTRICT); `(source_system_id)` → `source_system(source_system_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_source_artifact_context` — CREATE INDEX idx_source_artifact_context ON source_artifact(source_root_id, repository_snapshot_id, mod_release_id); `idx_source_artifact_path` — CREATE INDEX idx_source_artifact_path ON source_artifact(uri_or_path); `idx_source_artifact_version` — CREATE INDEX idx_source_artifact_version ON source_artifact(game_version_id, source_system_id, artifact_kind).

| Field | Declaration | Why it exists |
|---|---|---|
| `source_artifact_id` | `source_artifact_id INTEGER PRIMARY KEY` | Stable primary key for the `source_artifact` row. |
| `source_system_id` | `source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT` | References the evidence system from which the row was retrieved. |
| `source_root_id` | `source_root_id INTEGER REFERENCES source_root(source_root_id) ON DELETE RESTRICT` | Places the artifact inside an exact captured root, avoiding ambiguous relative paths. |
| `repository_snapshot_id` | `repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT` | Binds repository artifacts to branch/commit/worktree state. |
| `mod_release_id` | `mod_release_id INTEGER REFERENCES mod_release(mod_release_id) ON DELETE RESTRICT` | Binds a mod artifact to one captured release/revision. |
| `stable_key` | `stable_key TEXT NOT NULL` | Stable artifact identifier within its source system. |
| `artifact_kind` | `artifact_kind TEXT NOT NULL` | Classifies the artifact, such as source file, schema, report, log, save, note, or patch notes. |
| `title` | `title TEXT NOT NULL` | Readable artifact name. |
| `uri_or_path` | `uri_or_path TEXT NOT NULL` | Resolvable source-system path or URI. |
| `repository_relative_path` | `repository_relative_path TEXT` | Portable repository path when the artifact belongs to Git. |
| `game_version_id` | `game_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | Associates the row with an exact catalogued Stellaris version. |
| `repository_commit` | `repository_commit TEXT` | Commit that fixes the artifact’s repository content. |
| `tool_version` | `tool_version TEXT` | Version of the tool that produced or exposed the artifact. |
| `content_hash_algorithm` | `content_hash_algorithm TEXT` | Algorithm used for exact-content identity. |
| `content_hash_value` | `content_hash_value TEXT` | Hash value for drift detection and reproducibility. |
| `file_size_bytes` | `file_size_bytes INTEGER CHECK (file_size_bytes IS NULL OR file_size_bytes >= 0)` | Supports identity checks and retrieval validation without copying the file. |
| `mime_type` | `mime_type TEXT` | Allows tools and agents to select the correct inspection path. |
| `modified_at` | `modified_at TEXT` | Preserves source filesystem timestamp separately from capture/observation times. |
| `captured_at` | `captured_at TEXT` | Time the artifact snapshot was captured. |
| `observed_at` | `observed_at TEXT` | Time the evidence was actually observed or used. |
| `availability_status` | `availability_status TEXT NOT NULL CHECK (availability_status IN ('available','missing','moved','archived','unknown'))` | Current retrievability: available, missing, moved, archived, or unknown. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `artifact_derivation`

**Purpose and expected use.** Records that one artifact was produced from another by a named tool/run/method. It preserves generated-evidence lineage without importing tool-internal datasets.

**Primary key.** `artifact_derivation_id`

**Table-level integrity rules.** `CHECK (output_artifact_id <> input_artifact_id)`; `UNIQUE(output_artifact_id, input_artifact_id, process_run_key)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(verification_run_id)` → `verification_run(verification_run_id)` (ON DELETE RESTRICT); `(process_tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(input_artifact_id)` → `source_artifact(source_artifact_id)` (ON DELETE RESTRICT); `(output_artifact_id)` → `source_artifact(source_artifact_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_artifact_derivation_input` — CREATE INDEX idx_artifact_derivation_input ON artifact_derivation(input_artifact_id, output_artifact_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `artifact_derivation_id` | `artifact_derivation_id INTEGER PRIMARY KEY` | Stable primary key for the `artifact_derivation` row. |
| `output_artifact_id` | `output_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT` | References the derived output artifact. |
| `input_artifact_id` | `input_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT` | References an input artifact used to derive the output. |
| `process_tool_item_id` | `process_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the tool that performed the derivation. |
| `verification_run_id` | `verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT` | Connects lineage to the exact reproducible run that produced the output. |
| `process_run_key` | `process_run_key TEXT` | Identifier of the producing run, audit, or job. |
| `command_or_method` | `command_or_method TEXT` | Exact command or method used to create the output artifact. |
| `derived_at` | `derived_at TEXT` | Time the derivative was produced. |
| `rationale` | `rationale TEXT NOT NULL` | Explains what transformation occurred and why the lineage matters. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `evidence_locator`

**Purpose and expected use.** Provides a precise reusable anchor inside an artifact: path and lines/pages, section/symbol, dataset schema and record/cell, JSON path, archive member, byte range, query, timestamp, game date, and a bounded excerpt. It is the retrieval contract for reassessment.

**Primary key.** `evidence_locator_id`

**Table-level integrity rules.** `CHECK (line_end IS NULL OR line_start IS NOT NULL)`; `CHECK (line_end IS NULL OR line_end >= line_start)`; `CHECK (page_end IS NULL OR page_start IS NOT NULL)`; `CHECK (page_end IS NULL OR page_end >= page_start)`; `CHECK (byte_end IS NULL OR byte_start IS NOT NULL)`; `CHECK (byte_end IS NULL OR byte_end >= byte_start)`; `UNIQUE(source_artifact_id, stable_locator_key)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_by_actor_id)` → `actor(actor_id)` (ON DELETE RESTRICT); `(locator_type_id)` → `locator_type(locator_type_id)` (ON DELETE RESTRICT); `(dataset_schema_id)` → `dataset_schema(dataset_schema_id)` (ON DELETE RESTRICT); `(source_artifact_id)` → `source_artifact(source_artifact_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_evidence_locator_artifact` — CREATE INDEX idx_evidence_locator_artifact ON evidence_locator(source_artifact_id, locator_type_id); `idx_evidence_locator_record` — CREATE INDEX idx_evidence_locator_record ON evidence_locator(record_set, record_key, row_number, column_name); `idx_evidence_locator_symbol` — CREATE INDEX idx_evidence_locator_symbol ON evidence_locator(symbol_or_object_key, source_artifact_id).

**Triggers.** `trg_evidence_fts_ad`, `trg_evidence_fts_ai`, `trg_evidence_fts_au`.

| Field | Declaration | Why it exists |
|---|---|---|
| `evidence_locator_id` | `evidence_locator_id INTEGER PRIMARY KEY` | Stable primary key for the `evidence_locator` row. |
| `source_artifact_id` | `source_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT` | References the concrete artifact containing the located evidence. |
| `dataset_schema_id` | `dataset_schema_id INTEGER REFERENCES dataset_schema(dataset_schema_id) ON DELETE RESTRICT` | Connects a row/cell locator to the exact registered external schema version. |
| `locator_type_id` | `locator_type_id INTEGER NOT NULL REFERENCES locator_type(locator_type_id) ON DELETE RESTRICT` | Selects the structured locator modality. |
| `stable_locator_key` | `stable_locator_key TEXT NOT NULL` | Stable identifier for this exact location within the artifact. |
| `label` | `label TEXT NOT NULL` | Readable evidence label used in query results. |
| `relative_path` | `relative_path TEXT` | Nested path when the artifact is a bundle, repository, archive, or dataset family. |
| `line_start` | `line_start INTEGER CHECK (line_start IS NULL OR line_start >= 1)` | First one-based source line when line-based evidence is available. |
| `line_end` | `line_end INTEGER CHECK (line_end IS NULL OR line_end >= 1)` | Last one-based source line; paired checks prevent reversed ranges. |
| `page_start` | `page_start INTEGER CHECK (page_start IS NULL OR page_start >= 1)` | First one-based page for document/PDF evidence. |
| `page_end` | `page_end INTEGER CHECK (page_end IS NULL OR page_end >= 1)` | Last one-based page; paired checks prevent reversed ranges. |
| `section_title` | `section_title TEXT` | Heading or section anchor for prose/document sources. |
| `symbol_or_object_key` | `symbol_or_object_key TEXT` | Exact object or symbol used to retrieve the relevant definition. |
| `record_set` | `record_set TEXT` | Dataset/table/report section name. |
| `record_key` | `record_key TEXT` | Stable record identifier inside the record set. |
| `row_number` | `row_number INTEGER CHECK (row_number IS NULL OR row_number >= 1)` | Optional human/tool row coordinate; stable record_key remains primary when rows can reorder. |
| `column_name` | `column_name TEXT` | Optional exact external field/cell used as evidence. |
| `json_path` | `json_path TEXT` | JSONPath-like structured locator inside JSON artifacts. |
| `archive_member_path` | `archive_member_path TEXT` | Member path inside a save/ZIP/archive without copying archive contents. |
| `byte_start` | `byte_start INTEGER CHECK (byte_start IS NULL OR byte_start >= 0)` | Optional byte-range start for binary/large-text evidence. |
| `byte_end` | `byte_end INTEGER CHECK (byte_end IS NULL OR byte_end >= 0)` | Optional byte-range end paired with byte_start. |
| `query_text` | `query_text TEXT` | Search, SQL, command, or tool query needed to reproduce the locator. |
| `timestamp_start` | `timestamp_start TEXT` | Beginning of a runtime/log/recording time interval. |
| `timestamp_end` | `timestamp_end TEXT` | End of a runtime/log/recording time interval. |
| `game_date` | `game_date TEXT` | In-game date for save or runtime evidence. |
| `excerpt` | `excerpt TEXT` | Optional short orientation excerpt; it must not substitute for the source artifact. |
| `evidence_summary` | `evidence_summary TEXT NOT NULL` | Concise statement of what the located evidence shows. |
| `retrieval_instructions` | `retrieval_instructions TEXT` | Locator-specific recovery steps that override or refine source-system defaults. |
| `created_by_actor_id` | `created_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT` | Foreign key to the actor that created the record. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `dataset_schema`

**Purpose and expected use.** Registers an authoritative external CSV/TSV/JSON/JSONL/Parquet/XLSX/SQLite layout, row/column counts, schema hash, generator, stable-key contract, and storage policy. The dataset remains external; the database knows how to validate and address it.

**Primary key.** `dataset_schema_id`

**Table-level integrity rules.** `UNIQUE(source_artifact_id, schema_key, schema_version)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(generated_by_tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(source_artifact_id)` → `source_artifact(source_artifact_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_dataset_schema_key` — CREATE INDEX idx_dataset_schema_key ON dataset_schema(schema_key, schema_version, source_artifact_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `dataset_schema_id` | `dataset_schema_id INTEGER PRIMARY KEY` | Stable primary key for the `dataset_schema` row. |
| `source_artifact_id` | `source_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE CASCADE` | Foreign key to `source_artifact.source_artifact_id`, preserving normalized identity and referential integrity. |
| `schema_key` | `schema_key TEXT NOT NULL` | Logical dataset family used to compare versions and locate current/archived schemas. |
| `schema_version` | `schema_version TEXT NOT NULL` | Generator/date/commit schema version; multiple versions may coexist. |
| `format_code` | `format_code TEXT NOT NULL CHECK (format_code IN ('csv','tsv','json','jsonl','parquet','xlsx','sqlite','other'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `delimiter` | `delimiter TEXT` | Stores the structured `delimiter` attribute required to interpret, route, retrieve, or validate the row. |
| `has_header` | `has_header INTEGER NOT NULL CHECK (has_header IN (0,1))` | Strict 0/1 flag for the named state so agents do not infer it from prose. |
| `row_count` | `row_count INTEGER CHECK (row_count IS NULL OR row_count >= 0)` | Explicit count used for coverage, drift, truncation, or validation checks. |
| `column_count` | `column_count INTEGER CHECK (column_count IS NULL OR column_count >= 0)` | Explicit count used for coverage, drift, truncation, or validation checks. |
| `schema_hash_algorithm` | `schema_hash_algorithm TEXT` | Hash/fingerprint metadata used to validate identity and detect source or schema drift. |
| `schema_hash_value` | `schema_hash_value TEXT` | Hash/fingerprint metadata used to validate identity and detect source or schema drift. |
| `generated_by_tool_item_id` | `generated_by_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `dataset_schema` role (`tool.item_id`). |
| `is_authoritative_external` | `is_authoritative_external INTEGER NOT NULL CHECK (is_authoritative_external IN (0,1))` | Declares that the external artifact, not copied database values, is authoritative for the complete dataset. |
| `storage_policy` | `storage_policy TEXT NOT NULL CHECK (storage_policy IN ('locator_only','selected_rows','normalized_facts','full_import_allowed'))` | Controls whether the KB stores locators, selected rows, normalized facts, or permits a full import. |
| `stable_key_description` | `stable_key_description TEXT` | Stores the structured `stable_key_description` attribute required to interpret, route, retrieve, or validate the row. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `dataset_column`

**Purpose and expected use.** Catalogs every external dataset column with order, logical type, semantic role, dimensional grouping, metric mapping, unit, and optional item/field mapping. This is how hundreds of wide generated columns become understandable without EAV or a bulk copy.

**Primary key.** `dataset_column_id`

**Table-level integrity rules.** `UNIQUE(dataset_schema_id, ordinal)`; `UNIQUE(dataset_schema_id, column_name)`; `UNIQUE(dataset_schema_id, dataset_column_id)`.

**Relationships.** `(mapped_field_item_id)` → `field_definition(item_id)` (ON DELETE RESTRICT); `(mapped_item_type_id)` → `item_type(item_type_id)` (ON DELETE RESTRICT); `(dataset_schema_id)` → `dataset_schema(dataset_schema_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_dataset_column_semantics` — CREATE INDEX idx_dataset_column_semantics ON dataset_column(dataset_schema_id, semantic_role, dimension_group, metric_key).

| Field | Declaration | Why it exists |
|---|---|---|
| `dataset_column_id` | `dataset_column_id INTEGER PRIMARY KEY` | Stable primary key for the `dataset_column` row. |
| `dataset_schema_id` | `dataset_schema_id INTEGER NOT NULL REFERENCES dataset_schema(dataset_schema_id) ON DELETE CASCADE` | Foreign key to `dataset_schema.dataset_schema_id`, preserving normalized identity and referential integrity. |
| `ordinal` | `ordinal INTEGER NOT NULL CHECK (ordinal >= 1)` | Ordered numeric coordinate or rank used for deterministic traversal, display, or validation. |
| `column_name` | `column_name TEXT NOT NULL` | Human-readable name used in query results and review output while the machine key remains stable. |
| `logical_type` | `logical_type TEXT NOT NULL CHECK (logical_type IN ('integer','real','text','boolean','json','date','timestamp','path','identifier','expression','unknown'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `semantic_role` | `semantic_role TEXT NOT NULL CHECK (semantic_role IN ('identifier','dimension','metric','status','provenance','locator','expression','count','text','other'))` | Classifies identifier, dimension, metric, status, provenance, locator, expression, count, text, or other. |
| `dimension_group` | `dimension_group TEXT` | Names repeated dimensions such as scenario × output/upkeep/net × resource. |
| `metric_key` | `metric_key TEXT` | Maps a wide external column to a registered normalized metric when applicable. |
| `unit` | `unit TEXT` | Stores the structured `unit` attribute required to interpret, route, retrieve, or validate the row. |
| `is_nullable` | `is_nullable INTEGER NOT NULL CHECK (is_nullable IN (0,1))` | Strict 0/1 flag for the named state so agents do not infer it from prose. |
| `mapped_item_type_id` | `mapped_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE RESTRICT` | Constrains the type of knowledge item used as the metric dimension, for example resource. |
| `mapped_field_item_id` | `mapped_field_item_id INTEGER REFERENCES field_definition(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `dataset_column` role (`field_definition.item_id`). |
| `description` | `description TEXT NOT NULL` | Defines the durable project meaning of this row or controlled value. |

#### `dataset_key_column`

**Purpose and expected use.** Defines the ordered composite key of an external dataset and its normalization/stability rules. Exact keys allow evidence locators and schema comparisons to survive row reordering.

**Primary key.** `dataset_schema_id`, `dataset_column_id`

**Table-level integrity rules.** `PRIMARY KEY(dataset_schema_id, dataset_column_id)`; `UNIQUE(dataset_schema_id, key_ordinal)`; `FOREIGN KEY(dataset_schema_id, dataset_column_id) REFERENCES dataset_column(dataset_schema_id, dataset_column_id) ON DELETE CASCADE`.

**Relationships.** `(dataset_schema_id, dataset_column_id)` → `dataset_column(dataset_schema_id, dataset_column_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `dataset_schema_id` | `dataset_schema_id INTEGER NOT NULL` | Stable primary key for the `dataset_key_column` row. |
| `dataset_column_id` | `dataset_column_id INTEGER NOT NULL` | Stable primary key for the `dataset_key_column` row. |
| `key_ordinal` | `key_ordinal INTEGER NOT NULL CHECK (key_ordinal >= 1)` | Defines deterministic ordering of a composite external record key. |
| `normalization_rule` | `normalization_rule TEXT` | Documents trimming, case, path, or other normalization needed for stable joins. |
| `is_stable_across_versions` | `is_stable_across_versions INTEGER NOT NULL CHECK (is_stable_across_versions IN (0,1))` | Strict 0/1 flag for the named state so agents do not infer it from prose. |

#### `object_definition`

**Purpose and expected use.** Represents one definition occurrence of a game object in one source root/mod release/version span. It is a candidate, reference, removed, or unknown occurrence; playset-specific winning status lives in playset_object_resolution.

**Primary key.** `object_definition_id`

**Table-level integrity rules.** `CHECK (line_end IS NULL OR line_start IS NOT NULL)`; `CHECK (line_end IS NULL OR line_end >= line_start)`; `UNIQUE(object_item_id, version_span_id, source_system_id, evidence_locator_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(mod_release_id)` → `mod_release(mod_release_id)` (ON DELETE RESTRICT); `(source_root_id)` → `source_root(source_root_id)` (ON DELETE RESTRICT); `(source_system_id)` → `source_system(source_system_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(object_item_id)` → `game_object(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_object_definition_lookup` — CREATE INDEX idx_object_definition_lookup ON object_definition(object_item_id, version_span_id, definition_status); `idx_object_definition_origin` — CREATE INDEX idx_object_definition_origin ON object_definition(source_root_id, mod_release_id, object_item_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `object_definition_id` | `object_definition_id INTEGER PRIMARY KEY` | Stable primary key for the `object_definition` row. |
| `object_item_id` | `object_item_id INTEGER NOT NULL REFERENCES game_object(item_id) ON DELETE RESTRICT` | References the typed Stellaris object whose definition or occurrence is recorded. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `source_system_id` | `source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT` | References the evidence system from which the row was retrieved. |
| `source_root_id` | `source_root_id INTEGER REFERENCES source_root(source_root_id) ON DELETE RESTRICT` | Identifies the exact root in which this definition occurrence exists. |
| `mod_release_id` | `mod_release_id INTEGER REFERENCES mod_release(mod_release_id) ON DELETE RESTRICT` | Identifies the captured mod release that owns this occurrence. |
| `evidence_locator_id` | `evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `definition_status` | `definition_status TEXT NOT NULL CHECK (definition_status IN ('candidate','reference','removed','unknown'))` | Classifies an occurrence as candidate/reference/removed/unknown, never as a global winner. |
| `object_path` | `object_path TEXT` | Retrieval or execution path kept separate from stable logical identity. |
| `line_start` | `line_start INTEGER CHECK (line_start IS NULL OR line_start >= 1)` | Ordered numeric coordinate or rank used for deterministic traversal, display, or validation. |
| `line_end` | `line_end INTEGER CHECK (line_end IS NULL OR line_end >= 1)` | Ordered numeric coordinate or rank used for deterministic traversal, display, or validation. |
| `content_hash_algorithm` | `content_hash_algorithm TEXT` | Hash/fingerprint metadata used to validate identity and detect source or schema drift. |
| `content_hash` | `content_hash TEXT` | Optional hash of the definition block or source file used for drift detection. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `object_field_occurrence`

**Purpose and expected use.** Captures a typed, optionally nested occurrence of a known field inside an object definition, including ordinal, field path, value type, typed scalar, referenced item, expression, and exact evidence locator.

**Primary key.** `object_field_occurrence_id`

**Table-level integrity rules.** `CHECK ((integer_value IS NOT NULL) + (real_value IS NOT NULL) + (boolean_value IS NOT NULL) <= 1)`; `UNIQUE(object_item_id, field_item_id, version_span_id, evidence_locator_id, ordinal_in_object)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(referenced_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(source_system_id)` → `source_system(source_system_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(parent_occurrence_id)` → `object_field_occurrence(object_field_occurrence_id)` (ON DELETE CASCADE); `(field_item_id)` → `field_definition(item_id)` (ON DELETE RESTRICT); `(object_item_id)` → `game_object(item_id)` (ON DELETE RESTRICT); `(object_definition_id)` → `object_definition(object_definition_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_object_field_by_definition` — CREATE INDEX idx_object_field_by_definition ON object_field_occurrence(object_definition_id, field_path, ordinal_in_object); `idx_object_field_by_field` — CREATE INDEX idx_object_field_by_field ON object_field_occurrence(field_item_id, version_span_id, object_item_id); `idx_object_field_by_object` — CREATE INDEX idx_object_field_by_object ON object_field_occurrence(object_item_id, version_span_id, field_item_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `object_field_occurrence_id` | `object_field_occurrence_id INTEGER PRIMARY KEY` | Stable primary key for the `object_field_occurrence` row. |
| `object_definition_id` | `object_definition_id INTEGER REFERENCES object_definition(object_definition_id) ON DELETE CASCADE` | Links the field occurrence to a concrete definition occurrence when available. |
| `object_item_id` | `object_item_id INTEGER NOT NULL REFERENCES game_object(item_id) ON DELETE RESTRICT` | References the typed Stellaris object whose definition or occurrence is recorded. |
| `field_item_id` | `field_item_id INTEGER NOT NULL REFERENCES field_definition(item_id) ON DELETE RESTRICT` | References the typed field definition. |
| `parent_occurrence_id` | `parent_occurrence_id INTEGER REFERENCES object_field_occurrence(object_field_occurrence_id) ON DELETE CASCADE` | Represents nested PDX blocks/lists without flattening away structure. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `source_system_id` | `source_system_id INTEGER NOT NULL REFERENCES source_system(source_system_id) ON DELETE RESTRICT` | References the evidence system from which the row was retrieved. |
| `evidence_locator_id` | `evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `ordinal_in_object` | `ordinal_in_object INTEGER` | Disambiguates repeated occurrences of the same field within one object. |
| `field_path` | `field_path TEXT` | Stable dotted/path expression for the nested location within the object. |
| `occurrence_kind` | `occurrence_kind TEXT NOT NULL DEFAULT 'unknown' CHECK (occurrence_kind IN ('scalar','block','list','invocation','expression','unknown'))` | Distinguishes scalar, block, list, invocation, expression, or unknown source form. |
| `value_type` | `value_type TEXT CHECK (value_type IS NULL OR value_type IN ('integer','real','text','boolean','identifier','expression','block','list','unknown'))` | Declares how the captured source value should be interpreted. |
| `value_text` | `value_text TEXT` | Preserves the exact text/expression needed for review without substituting it for typed relational facts. |
| `integer_value` | `integer_value INTEGER` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `real_value` | `real_value REAL` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `boolean_value` | `boolean_value INTEGER CHECK (boolean_value IS NULL OR boolean_value IN (0,1))` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `referenced_item_id` | `referenced_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | Links identifier-valued fields directly to a stable item when resolution succeeds. |
| `expression_text` | `expression_text TEXT` | Optional short field expression for orientation; the underlying file remains authoritative. |
| `normalized_summary` | `normalized_summary TEXT` | Normalized explanation of the occurrence for comparison and search. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `definition_reference`

**Purpose and expected use.** Normalizes a reference emitted by one object definition—technology, resource, job, trigger, script, object key, or unresolved text—together with resolution status and source occurrence. It supplies dependency edges without pretending unresolved strings are known items.

**Primary key.** `definition_reference_id`

**Table-level integrity rules.** `CHECK (target_item_id IS NOT NULL OR target_key_text IS NOT NULL)`; `UNIQUE(object_definition_id, stable_reference_key)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(target_object_kind_id)` → `object_kind(object_kind_id)` (ON DELETE RESTRICT); `(target_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(source_occurrence_id)` → `object_field_occurrence(object_field_occurrence_id)` (ON DELETE SET NULL); `(object_definition_id)` → `object_definition(object_definition_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_definition_reference_target` — CREATE INDEX idx_definition_reference_target ON definition_reference(target_item_id, reference_kind, resolution_status); `idx_definition_reference_unresolved` — CREATE INDEX idx_definition_reference_unresolved ON definition_reference(target_key_text, target_object_kind_id, resolution_status) WHERE target_item_id IS NULL.

| Field | Declaration | Why it exists |
|---|---|---|
| `definition_reference_id` | `definition_reference_id INTEGER PRIMARY KEY` | Stable primary key for the `definition_reference` row. |
| `object_definition_id` | `object_definition_id INTEGER NOT NULL REFERENCES object_definition(object_definition_id) ON DELETE CASCADE` | Foreign key to `object_definition.object_definition_id`, preserving normalized identity and referential integrity. |
| `source_occurrence_id` | `source_occurrence_id INTEGER REFERENCES object_field_occurrence(object_field_occurrence_id) ON DELETE SET NULL` | Foreign key to `object_field_occurrence.object_field_occurrence_id`, preserving normalized identity and referential integrity. |
| `stable_reference_key` | `stable_reference_key TEXT NOT NULL` | Stable occurrence key within the definition, allowing repeated target text to be distinguished. |
| `reference_kind` | `reference_kind TEXT NOT NULL` | States whether the source refers to a technology, resource, object, trigger, job, script, variable, or another surface. |
| `target_item_id` | `target_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `definition_reference` role (`knowledge_item.item_id`). |
| `target_key_text` | `target_key_text TEXT` | Preserves the exact unresolved/external key when no stable item can yet be linked. |
| `target_object_kind_id` | `target_object_kind_id INTEGER REFERENCES object_kind(object_kind_id) ON DELETE RESTRICT` | Foreign key to `object_kind.object_kind_id`, preserving normalized identity and referential integrity. |
| `resolution_status` | `resolution_status TEXT NOT NULL CHECK (resolution_status IN ('resolved','external','missing','ambiguous','ignored','unknown'))` | Distinguishes resolved, external, missing, ambiguous, ignored, and unknown references. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Foreign key to `evidence_locator.evidence_locator_id`, preserving normalized identity and referential integrity. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `object_conflict`

**Purpose and expected use.** Represents a playset-specific duplicate, field overlap, collision, replace_path, dependency, load-order, or reference conflict with risk, disposition, evidence, and required action.

**Primary key.** `object_conflict_id`

**Table-level integrity rules.** `UNIQUE(playset_snapshot_id, conflict_key)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(detected_by_tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(winning_definition_id)` → `object_definition(object_definition_id)` (ON DELETE RESTRICT); `(risk_level_id)` → `risk_level(risk_level_id)` (ON DELETE RESTRICT); `(object_item_id)` → `game_object(item_id)` (ON DELETE RESTRICT); `(playset_snapshot_id)` → `playset_snapshot(playset_snapshot_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_object_conflict_queue` — CREATE INDEX idx_object_conflict_queue ON object_conflict(playset_snapshot_id, status_code, risk_level_id, object_item_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `object_conflict_id` | `object_conflict_id INTEGER PRIMARY KEY` | Stable primary key for the `object_conflict` row. |
| `playset_snapshot_id` | `playset_snapshot_id INTEGER NOT NULL REFERENCES playset_snapshot(playset_snapshot_id) ON DELETE CASCADE` | Foreign key to `playset_snapshot.playset_snapshot_id`, preserving normalized identity and referential integrity. |
| `conflict_key` | `conflict_key TEXT NOT NULL` | Stable identity for the conflict inside one snapshot. |
| `object_item_id` | `object_item_id INTEGER REFERENCES game_object(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `object_conflict` role (`game_object.item_id`). |
| `conflict_kind` | `conflict_kind TEXT NOT NULL CHECK (conflict_kind IN ('duplicate_definition','field_overlap','file_collision','replace_path','dependency','load_order','reference','unknown'))` | Classifies duplicate, overlap, collision, replace_path, dependency, load-order, or reference risk. |
| `risk_level_id` | `risk_level_id INTEGER NOT NULL REFERENCES risk_level(risk_level_id) ON DELETE RESTRICT` | Foreign key to `risk_level.risk_level_id`, preserving normalized identity and referential integrity. |
| `status_code` | `status_code TEXT NOT NULL CHECK (status_code IN ('open','reviewed','accepted','resolved','false_positive','stale'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `winning_definition_id` | `winning_definition_id INTEGER REFERENCES object_definition(object_definition_id) ON DELETE RESTRICT` | Foreign key to `object_definition.object_definition_id`, preserving normalized identity and referential integrity. |
| `detected_by_tool_item_id` | `detected_by_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `object_conflict` role (`tool.item_id`). |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Foreign key to `evidence_locator.evidence_locator_id`, preserving normalized identity and referential integrity. |
| `detected_at` | `detected_at TEXT` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `rationale` | `rationale TEXT NOT NULL` | Concise durable explanation needed to interpret the normalized row and its evidence boundary. |
| `required_action` | `required_action TEXT` | Stores the normalized `required_action` attribute needed to query and maintain `object_conflict` records without an EAV or JSON fallback. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `object_conflict_member`

**Purpose and expected use.** Lists the candidate/winner/loser/reference definitions participating in a conflict, with load position and differing-field summary. It explains how the conflict set produced the winner.

**Primary key.** `object_conflict_id`, `object_definition_id`

**Table-level integrity rules.** `PRIMARY KEY(object_conflict_id, object_definition_id)`.

**Relationships.** `(object_definition_id)` → `object_definition(object_definition_id)` (ON DELETE RESTRICT); `(object_conflict_id)` → `object_conflict(object_conflict_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

**Triggers.** `trg_object_conflict_member_object_insert`.

| Field | Declaration | Why it exists |
|---|---|---|
| `object_conflict_id` | `object_conflict_id INTEGER NOT NULL REFERENCES object_conflict(object_conflict_id) ON DELETE CASCADE` | Stable primary key for the `object_conflict_member` row. |
| `object_definition_id` | `object_definition_id INTEGER NOT NULL REFERENCES object_definition(object_definition_id) ON DELETE RESTRICT` | Stable primary key for the `object_conflict_member` row. |
| `member_role` | `member_role TEXT NOT NULL CHECK (member_role IN ('candidate','winner','loser','reference','unknown'))` | Explains whether this occurrence is candidate, winner, loser, reference, or unknown. |
| `load_position` | `load_position INTEGER CHECK (load_position IS NULL OR load_position >= 1)` | Ordered numeric coordinate or rank used for deterministic traversal, display, or validation. |
| `differing_fields` | `differing_fields TEXT` | Preserves the exact text/expression needed for review without substituting it for typed relational facts. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `verification_run`

**Purpose and expected use.** Describes a reproducible static check, source diff, generation, conflict scan, log/save analysis, observer run, controlled experiment, or database validation. It carries explicit approval and reproducibility status plus the execution context.

**Primary key.** `verification_run_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(performed_by_actor_id)` → `actor(actor_id)` (ON DELETE RESTRICT); `(tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(execution_context_id)` → `execution_context(execution_context_id)` (ON DELETE RESTRICT); `(target_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_verification_run_target` — CREATE INDEX idx_verification_run_target ON verification_run(target_version_id, outcome_code, completed_at).

| Field | Declaration | Why it exists |
|---|---|---|
| `verification_run_id` | `verification_run_id INTEGER PRIMARY KEY` | Stable primary key for the `verification_run` row. |
| `run_key` | `run_key TEXT NOT NULL UNIQUE` | Stable name for a reproducible verification activity. |
| `title` | `title TEXT NOT NULL` | Readable run name. |
| `run_kind` | `run_kind TEXT NOT NULL DEFAULT 'static_analysis' CHECK (run_kind IN ('static_analysis','schema_validation','conflict_scan','source_diff','model_generation','log_analysis','save_analysis','observer_run','controlled_experiment','database_validation','other'))` | Classifies the verification method so static, generation, log/save, observer, experiment, and database checks are not conflated. |
| `target_version_id` | `target_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | Selects the exact version the run, question, or query targets. |
| `execution_context_id` | `execution_context_id INTEGER REFERENCES execution_context(execution_context_id) ON DELETE RESTRICT` | Binds the run to its version/playset/repository/mode/settings context. |
| `tool_item_id` | `tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the typed tool used or recommended. |
| `performed_by_actor_id` | `performed_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT` | Foreign key to the actor that performed the verification run. |
| `method_summary` | `method_summary TEXT NOT NULL` | Describes the procedure and proof boundary. |
| `command_or_query` | `command_or_query TEXT` | Exact command/query when applicable. |
| `environment_summary` | `environment_summary TEXT` | Human-readable build, playset, DLC, save, or runtime context; exact artifacts/hashes remain normalized separately. |
| `started_at` | `started_at TEXT` | Run start time. |
| `completed_at` | `completed_at TEXT` | Run completion time. |
| `approval_status` | `approval_status TEXT NOT NULL DEFAULT 'not_required' CHECK (approval_status IN ('not_required','approved','not_approved','unknown'))` | Records whether runtime/observer work was approved, not required, not approved, or unknown. |
| `reproducibility_status` | `reproducibility_status TEXT NOT NULL DEFAULT 'partially_reproducible' CHECK (reproducibility_status IN ('reproducible','partially_reproducible','not_reproducible','unknown'))` | States whether exact inputs/methods are sufficient to rerun the check. |
| `outcome_code` | `outcome_code TEXT NOT NULL CHECK (outcome_code IN ('passed','failed','partial','inconclusive','not_run'))` | Passed, failed, partial, inconclusive, or not-run result. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `validation_finding`

**Purpose and expected use.** Stores a structured result from CWTools, parsers, reference audits, conflict scans, logs, saves, modeling checks, coverage checks, or database integrity checks. Findings remain tied to the exact verification run and evidence locator.

**Primary key.** `validation_finding_id`

**Table-level integrity rules.** `UNIQUE(verification_run_id, finding_key)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(primary_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(verification_run_id)` → `verification_run(verification_run_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_validation_finding_queue` — CREATE INDEX idx_validation_finding_queue ON validation_finding(status_code, severity_code, category_code, primary_item_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `validation_finding_id` | `validation_finding_id INTEGER PRIMARY KEY` | Stable primary key for the `validation_finding` row. |
| `verification_run_id` | `verification_run_id INTEGER NOT NULL REFERENCES verification_run(verification_run_id) ON DELETE CASCADE` | Foreign key to `verification_run.verification_run_id`, preserving normalized identity and referential integrity. |
| `finding_key` | `finding_key TEXT NOT NULL` | Stable run-local key used for regression comparison and deduplication. |
| `category_code` | `category_code TEXT NOT NULL CHECK (category_code IN ('syntax','schema','reference','conflict','load_order','runtime_log','save_state','modeling','coverage','integrity','performance','other'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `severity_code` | `severity_code TEXT NOT NULL CHECK (severity_code IN ('info','warning','error','critical'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `status_code` | `status_code TEXT NOT NULL CHECK (status_code IN ('open','accepted','resolved','false_positive','superseded'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `primary_item_id` | `primary_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `validation_finding` role (`knowledge_item.item_id`). |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Foreign key to `evidence_locator.evidence_locator_id`, preserving normalized identity and referential integrity. |
| `finding_summary` | `finding_summary TEXT NOT NULL` | Concise durable explanation needed to interpret the normalized row and its evidence boundary. |
| `expected_text` | `expected_text TEXT` | Preserves the exact text/expression needed for review without substituting it for typed relational facts. |
| `actual_text` | `actual_text TEXT` | Preserves the exact text/expression needed for review without substituting it for typed relational facts. |
| `remediation` | `remediation TEXT` | Stores the normalized `remediation` attribute needed to query and maintain `validation_finding` records without an EAV or JSON fallback. |
| `regression_key` | `regression_key TEXT` | Cross-run key used to recognize the same check/failure after regeneration. |
| `first_observed_at` | `first_observed_at TEXT` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `resolved_at` | `resolved_at TEXT` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

### 5. Claims, assessments, contradictions, questions, and revalidation

This group answers what is known, contradicted, uncertain, stale, or unresolved and why.

#### `claim`

**Purpose and expected use.** Stores a durable, atomic statement about one primary knowledge item. Statements are not overwritten when meaning changes; a new claim may supersede the old one.

**Primary key.** `claim_id`

**Table-level integrity rules.** `CHECK (supersedes_claim_id IS NULL OR supersedes_claim_id <> claim_id)`.

**Relationships.** `(retired_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_by_actor_id)` → `actor(actor_id)` (ON DELETE RESTRICT); `(lifecycle_state_id)` → `lifecycle_state(lifecycle_state_id)` (ON DELETE RESTRICT); `(supersedes_claim_id)` → `claim(claim_id)` (ON DELETE RESTRICT); `(primary_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(claim_type_id)` → `claim_type(claim_type_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_claim_primary_item` — CREATE INDEX idx_claim_primary_item ON claim(primary_item_id, lifecycle_state_id, claim_type_id); `idx_claim_supersedes` — CREATE INDEX idx_claim_supersedes ON claim(supersedes_claim_id) WHERE supersedes_claim_id IS NOT NULL.

**Triggers.** `trg_claim_fts_ad`, `trg_claim_fts_ai`, `trg_claim_fts_au`.

| Field | Declaration | Why it exists |
|---|---|---|
| `claim_id` | `claim_id INTEGER PRIMARY KEY` | Stable primary key for the `claim` row. |
| `claim_type_id` | `claim_type_id INTEGER NOT NULL REFERENCES claim_type(claim_type_id) ON DELETE RESTRICT` | Classifies the proposition’s intent and proof standard. |
| `primary_item_id` | `primary_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the main knowledge item about which the claim or question is written. |
| `statement` | `statement TEXT NOT NULL` | Atomic proposition whose wording is preserved for historical assessment. |
| `context` | `context TEXT` | Conditions, playset assumptions, or scope that limit the statement. |
| `epistemic_note` | `epistemic_note TEXT` | Explains expected proof standard or known reasoning boundary. |
| `supersedes_claim_id` | `supersedes_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT` | References the earlier claim replaced by this proposition. |
| `lifecycle_state_id` | `lifecycle_state_id INTEGER NOT NULL REFERENCES lifecycle_state(lifecycle_state_id) ON DELETE RESTRICT` | Selects the catalog lifecycle state. |
| `created_by_actor_id` | `created_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT` | Foreign key to the actor that created the record. |
| `created_at` | `created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))` | Time the proposition was first recorded. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |
| `retired_in_change_set_id` | `retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that retired this row without deleting history. |

#### `claim_item`

**Purpose and expected use.** Associates a claim with additional subjects, dependencies, contexts, outputs, or comparison items using explicit roles, enabling mechanics-centric retrieval beyond the primary item.

**Primary key.** `claim_id`, `item_id`, `role_code`

**Table-level integrity rules.** `PRIMARY KEY (claim_id, item_id, role_code)`.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(claim_id)` → `claim(claim_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_claim_item_item` — CREATE INDEX idx_claim_item_item ON claim_item(item_id, role_code, claim_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `claim_id` | `claim_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE CASCADE` | References the claim being linked, assessed, or evidenced. |
| `item_id` | `item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity represented or linked by this row. |
| `role_code` | `role_code TEXT NOT NULL` | Explains how the linked item participates in the claim. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `claim_assessment`

**Purpose and expected use.** Judges one immutable claim for a version span and optional execution context, with state, confidence, run, basis, revalidation deadline, and append/supersede history.

**Primary key.** `claim_assessment_id`

**Table-level integrity rules.** `CHECK (supersedes_assessment_id IS NULL OR supersedes_assessment_id <> claim_assessment_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(supersedes_assessment_id)` → `claim_assessment(claim_assessment_id)` (ON DELETE RESTRICT); `(assessed_by_actor_id)` → `actor(actor_id)` (ON DELETE RESTRICT); `(execution_context_id)` → `execution_context(execution_context_id)` (ON DELETE RESTRICT); `(verification_run_id)` → `verification_run(verification_run_id)` (ON DELETE RESTRICT); `(confidence_level_id)` → `confidence_level(confidence_level_id)` (ON DELETE RESTRICT); `(assessment_state_id)` → `assessment_state(assessment_state_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(claim_id)` → `claim(claim_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_claim_assessment_claim` — CREATE INDEX idx_claim_assessment_claim ON claim_assessment(claim_id, is_current, version_span_id); `idx_claim_assessment_state` — CREATE INDEX idx_claim_assessment_state ON claim_assessment(assessment_state_id, confidence_level_id, reverify_after); `uq_claim_assessment_current_exact_span` — CREATE UNIQUE INDEX uq_claim_assessment_current_exact_span ON claim_assessment(claim_id, version_span_id) WHERE is_current = 1.

| Field | Declaration | Why it exists |
|---|---|---|
| `claim_assessment_id` | `claim_assessment_id INTEGER PRIMARY KEY` | Stable primary key for the `claim_assessment` row. |
| `claim_id` | `claim_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE RESTRICT` | References the claim being linked, assessed, or evidenced. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `assessment_state_id` | `assessment_state_id INTEGER NOT NULL REFERENCES assessment_state(assessment_state_id) ON DELETE RESTRICT` | Selects the normalized epistemic state. |
| `confidence_level_id` | `confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT` | Selects the normalized confidence level. |
| `verification_run_id` | `verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT` | References the run that produced or tested this assessment/evidence. |
| `execution_context_id` | `execution_context_id INTEGER REFERENCES execution_context(execution_context_id) ON DELETE RESTRICT` | Limits an assessment to the playset/run mode/settings context when version alone is insufficient. |
| `assessed_by_actor_id` | `assessed_by_actor_id INTEGER NOT NULL REFERENCES actor(actor_id) ON DELETE RESTRICT` | Foreign key to the actor responsible for the assessment. |
| `assessed_at` | `assessed_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))` | Time the version-specific assessment was made. |
| `basis_summary` | `basis_summary TEXT NOT NULL` | Reasoned conclusion drawn from the linked evidence and run. |
| `reverify_after` | `reverify_after TEXT` | Optional due date for scheduled reassessment. |
| `is_current` | `is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1))` | Marks the current assessment for an exact claim/span. |
| `supersedes_assessment_id` | `supersedes_assessment_id INTEGER REFERENCES claim_assessment(claim_assessment_id) ON DELETE RESTRICT` | References the previous assessment in the append-only chain. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `claim_evidence`

**Purpose and expected use.** Connects claims to evidence locators with stance, directness, strength, optional verification run, and an explicit interpretation. Evidence aggregation never silently determines the final assessment.

**Primary key.** `claim_evidence_id`

**Table-level integrity rules.** `UNIQUE(claim_id, evidence_locator_id, evidence_stance_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(verification_run_id)` → `verification_run(verification_run_id)` (ON DELETE RESTRICT); `(evidence_stance_id)` → `evidence_stance(evidence_stance_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(claim_id)` → `claim(claim_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_claim_evidence_claim_stance` — CREATE INDEX idx_claim_evidence_claim_stance ON claim_evidence(claim_id, evidence_stance_id, strength_rank DESC); `idx_claim_evidence_locator` — CREATE INDEX idx_claim_evidence_locator ON claim_evidence(evidence_locator_id, claim_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `claim_evidence_id` | `claim_evidence_id INTEGER PRIMARY KEY` | Stable primary key for the `claim_evidence` row. |
| `claim_id` | `claim_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE CASCADE` | References the claim being linked, assessed, or evidenced. |
| `evidence_locator_id` | `evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `evidence_stance_id` | `evidence_stance_id INTEGER NOT NULL REFERENCES evidence_stance(evidence_stance_id) ON DELETE RESTRICT` | Selects whether evidence supports, contradicts, qualifies, or contextualizes. |
| `directness_rank` | `directness_rank INTEGER NOT NULL CHECK (directness_rank BETWEEN 1 AND 5)` | 1–5 measure of how directly the locator bears on the proposition. |
| `strength_rank` | `strength_rank INTEGER NOT NULL CHECK (strength_rank BETWEEN 1 AND 5)` | 1–5 qualitative evidentiary strength, separate from source-class reliability. |
| `verification_run_id` | `verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT` | References the run that produced or tested this assessment/evidence. |
| `interpretation` | `interpretation TEXT NOT NULL` | Explains why this locator has the stated stance for this claim. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `claim_conflict`

**Purpose and expected use.** Explicitly records a contradiction or incompatibility between two claims, its version applicability, analysis, status, and any resolving claim.

**Primary key.** `claim_conflict_id`

**Table-level integrity rules.** `CHECK (claim_a_id < claim_b_id)`; `UNIQUE(claim_a_id, claim_b_id, version_span_id)`.

**Relationships.** `(resolved_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(resolution_claim_id)` → `claim(claim_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(claim_b_id)` → `claim(claim_id)` (ON DELETE RESTRICT); `(claim_a_id)` → `claim(claim_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_claim_conflict_status` — CREATE INDEX idx_claim_conflict_status ON claim_conflict(status_code, version_span_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `claim_conflict_id` | `claim_conflict_id INTEGER PRIMARY KEY` | Stable primary key for the `claim_conflict` row. |
| `claim_a_id` | `claim_a_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE RESTRICT` | References the lower-ID member of the canonical conflict pair. |
| `claim_b_id` | `claim_b_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE RESTRICT` | References the higher-ID member of the canonical conflict pair. |
| `version_span_id` | `version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `conflict_kind` | `conflict_kind TEXT NOT NULL` | Project-defined classification of the contradiction. |
| `status_code` | `status_code TEXT NOT NULL CHECK (status_code IN ('open','resolved','dismissed'))` | Tracks open, resolved, or dismissed conflict state. |
| `analysis` | `analysis TEXT NOT NULL` | Explains why the claims conflict and what evidence would resolve them. |
| `resolution_claim_id` | `resolution_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT` | References the claim that resolves or closes the conflict/question. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |
| `resolved_in_change_set_id` | `resolved_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that recorded resolution. |

#### `open_question`

**Purpose and expected use.** Represents a prioritized, assignable uncertainty with target version, next review date, and eventual resolution claim. Unknowns become work items rather than disappearing into prose notes.

**Primary key.** `question_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(closed_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(resolution_claim_id)` → `claim(claim_id)` (ON DELETE RESTRICT); `(owner_actor_id)` → `actor(actor_id)` (ON DELETE RESTRICT); `(target_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT); `(primary_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_open_question_queue` — CREATE INDEX idx_open_question_queue ON open_question(status_code, priority DESC, target_version_id).

**Triggers.** `trg_question_fts_ad`, `trg_question_fts_ai`, `trg_question_fts_au`.

| Field | Declaration | Why it exists |
|---|---|---|
| `question_id` | `question_id INTEGER PRIMARY KEY` | Stable primary key for the `open_question` row. |
| `question_key` | `question_key TEXT NOT NULL UNIQUE` | Stable identifier for the uncertainty/work item. |
| `primary_item_id` | `primary_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the main knowledge item about which the claim or question is written. |
| `question_text` | `question_text TEXT NOT NULL` | The exact question that evidence must answer. |
| `uncertainty_reason` | `uncertainty_reason TEXT NOT NULL` | Explains why existing evidence is insufficient. |
| `target_version_id` | `target_version_id INTEGER REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | Selects the exact version the run, question, or query targets. |
| `status_code` | `status_code TEXT NOT NULL CHECK (status_code IN ('open','investigating','blocked','resolved','wont_fix'))` | Open, investigating, blocked, resolved, or wont-fix workflow state. |
| `priority` | `priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100)` | 1–100 urgency/importance used for queues. |
| `owner_actor_id` | `owner_actor_id INTEGER REFERENCES actor(actor_id) ON DELETE RESTRICT` | Optional foreign key to the actor responsible for follow-up. |
| `resolution_claim_id` | `resolution_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT` | References the claim that resolves or closes the conflict/question. |
| `next_review_at` | `next_review_at TEXT` | Optional scheduled next investigation date. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |
| `closed_in_change_set_id` | `closed_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that closed the work item. |

#### `question_item`

**Purpose and expected use.** Links an open question to every relevant mechanic, object, field, file, tool, or compatibility surface using role codes.

**Primary key.** `question_id`, `item_id`, `role_code`

**Table-level integrity rules.** `PRIMARY KEY(question_id, item_id, role_code)`.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(question_id)` → `open_question(question_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_question_item_item` — CREATE INDEX idx_question_item_item ON question_item(item_id, role_code, question_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `question_id` | `question_id INTEGER NOT NULL REFERENCES open_question(question_id) ON DELETE CASCADE` | References `open_question.question_id` to normalize this association instead of duplicating parent data. |
| `item_id` | `item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity represented or linked by this row. |
| `role_code` | `role_code TEXT NOT NULL` | Explains how the linked item participates in the question. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `question_evidence`

**Purpose and expected use.** Connects evidence to an open question with a relevance classification, allowing partial findings to be retained before the question is resolved.

**Primary key.** `question_id`, `evidence_locator_id`, `relevance_code`

**Table-level integrity rules.** `PRIMARY KEY(question_id, evidence_locator_id, relevance_code)`.

**Relationships.** `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(question_id)` → `open_question(question_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `question_id` | `question_id INTEGER NOT NULL REFERENCES open_question(question_id) ON DELETE CASCADE` | References `open_question.question_id` to normalize this association instead of duplicating parent data. |
| `evidence_locator_id` | `evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `relevance_code` | `relevance_code TEXT NOT NULL` | Classifies whether evidence narrows, blocks, motivates, or partly answers the question. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `revalidation_policy`

**Purpose and expected use.** Defines reusable rules for when knowledge must be revisited: any update, minimum patch/minor/major change, source changes, or age thresholds, plus preferred tools and instructions.

**Primary key.** `revalidation_policy_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(preferred_tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `revalidation_policy_id` | `revalidation_policy_id INTEGER PRIMARY KEY` | Stable primary key for the `revalidation_policy` row. |
| `policy_code` | `policy_code TEXT NOT NULL UNIQUE` | Stable reusable policy identifier. |
| `policy_name` | `policy_name TEXT NOT NULL` | Readable policy name. |
| `trigger_on_any_game_update` | `trigger_on_any_game_update INTEGER NOT NULL CHECK (trigger_on_any_game_update IN (0,1))` | Queues knowledge on every catalogued game update. |
| `minimum_version_change` | `minimum_version_change TEXT CHECK (minimum_version_change IN ('patch','minor','major','any') OR minimum_version_change IS NULL)` | Smallest patch/minor/major change that should trigger review. |
| `trigger_on_source_change` | `trigger_on_source_change INTEGER NOT NULL CHECK (trigger_on_source_change IN (0,1))` | Queues knowledge when its authoritative source artifact changes. |
| `max_age_days` | `max_age_days INTEGER CHECK (max_age_days IS NULL OR max_age_days >= 1)` | Maximum acceptable age before evidence is considered due for review. |
| `preferred_tool_item_id` | `preferred_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the preferred tool for this policy or impact action. |
| `instructions` | `instructions TEXT NOT NULL` | Concrete revalidation procedure. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `claim_revalidation_policy`

**Purpose and expected use.** Assigns one or more revalidation policies to a claim with priority and notes.

**Primary key.** `claim_id`, `revalidation_policy_id`

**Table-level integrity rules.** `PRIMARY KEY(claim_id, revalidation_policy_id)`.

**Relationships.** `(revalidation_policy_id)` → `revalidation_policy(revalidation_policy_id)` (ON DELETE RESTRICT); `(claim_id)` → `claim(claim_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `claim_id` | `claim_id INTEGER NOT NULL REFERENCES claim(claim_id) ON DELETE CASCADE` | References the claim being linked, assessed, or evidenced. |
| `revalidation_policy_id` | `revalidation_policy_id INTEGER NOT NULL REFERENCES revalidation_policy(revalidation_policy_id) ON DELETE RESTRICT` | References the reusable revalidation rule. |
| `priority` | `priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100)` | Relative order when a claim has several policies. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `item_revalidation_policy`

**Purpose and expected use.** Assigns revalidation policies to a knowledge item so all related claims can be queued when the item or game version changes.

**Primary key.** `item_id`, `revalidation_policy_id`

**Table-level integrity rules.** `PRIMARY KEY(item_id, revalidation_policy_id)`.

**Relationships.** `(revalidation_policy_id)` → `revalidation_policy(revalidation_policy_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `revalidation_policy_id` | `revalidation_policy_id INTEGER NOT NULL REFERENCES revalidation_policy(revalidation_policy_id) ON DELETE RESTRICT` | References the reusable revalidation rule. |
| `priority` | `priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100)` | Relative order when an item has several policies. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

### 6. Relationship graph, version changes, checklists, implementation, and tools

This group drives direct/transitive impact analysis, change planning, version deltas, implementation references, and tool selection.

#### `item_relation`

**Purpose and expected use.** Stores evidence-aware, versioned, typed edges between knowledge items, including why the edge exists and what review/validation action it implies. This is the durable semantic graph used for impact analysis.

**Primary key.** `item_relation_id`

**Table-level integrity rules.** `CHECK (source_item_id <> target_item_id)`.

**Relationships.** `(retired_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(source_claim_id)` → `claim(claim_id)` (ON DELETE RESTRICT); `(risk_level_id)` → `risk_level(risk_level_id)` (ON DELETE RESTRICT); `(confidence_level_id)` → `confidence_level(confidence_level_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(target_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(relation_type_id)` → `relation_type(relation_type_id)` (ON DELETE RESTRICT); `(source_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_item_relation_source` — CREATE INDEX idx_item_relation_source ON item_relation(source_item_id, version_span_id, relation_type_id, is_current); `idx_item_relation_target` — CREATE INDEX idx_item_relation_target ON item_relation(target_item_id, version_span_id, relation_type_id, is_current); `uq_item_relation_current` — CREATE UNIQUE INDEX uq_item_relation_current ON item_relation(source_item_id, relation_type_id, target_item_id, version_span_id) WHERE is_current = 1.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_relation_id` | `item_relation_id INTEGER PRIMARY KEY` | Stable primary key for the `item_relation` row. |
| `source_item_id` | `source_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the semantic source of the stored relationship. |
| `relation_type_id` | `relation_type_id INTEGER NOT NULL REFERENCES relation_type(relation_type_id) ON DELETE RESTRICT` | Selects the semantic edge type and its impact-propagation mode. |
| `target_item_id` | `target_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the semantic target of the relationship or route selector. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `confidence_level_id` | `confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT` | Selects the normalized confidence level. |
| `risk_level_id` | `risk_level_id INTEGER NOT NULL REFERENCES risk_level(risk_level_id) ON DELETE RESTRICT` | Selects the normalized risk severity. |
| `source_claim_id` | `source_claim_id INTEGER REFERENCES claim(claim_id) ON DELETE RESTRICT` | References the claim that justifies the relationship. |
| `rationale` | `rationale TEXT NOT NULL` | Explains the semantic reason for the edge. |
| `impact_explanation` | `impact_explanation TEXT NOT NULL` | Explains why a change may propagate across this edge. |
| `review_action` | `review_action TEXT` | Edge-specific inspection action returned by impact queries. |
| `validation_action` | `validation_action TEXT` | Edge-specific validation action returned by impact queries. |
| `is_current` | `is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1))` | Marks the current edge while retaining retired history. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |
| `retired_in_change_set_id` | `retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that retired this row without deleting history. |

#### `relation_evidence`

**Purpose and expected use.** Attaches supporting, contradicting, qualifying, or contextual evidence to a specific graph edge, preventing relationships from becoming unexplained assertions.

**Primary key.** `item_relation_id`, `evidence_locator_id`, `evidence_stance_id`

**Table-level integrity rules.** `PRIMARY KEY(item_relation_id, evidence_locator_id, evidence_stance_id)`.

**Relationships.** `(evidence_stance_id)` → `evidence_stance(evidence_stance_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(item_relation_id)` → `item_relation(item_relation_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_relation_id` | `item_relation_id INTEGER NOT NULL REFERENCES item_relation(item_relation_id) ON DELETE CASCADE` | References `item_relation.item_relation_id` to normalize this association instead of duplicating parent data. |
| `evidence_locator_id` | `evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `evidence_stance_id` | `evidence_stance_id INTEGER NOT NULL REFERENCES evidence_stance(evidence_stance_id) ON DELETE RESTRICT` | Selects whether evidence supports, contradicts, qualifies, or contextualizes. |
| `strength_rank` | `strength_rank INTEGER NOT NULL CHECK (strength_rank BETWEEN 1 AND 5)` | 1–5 strength of the evidence for or against the edge. |
| `interpretation` | `interpretation TEXT NOT NULL` | Explains the evidence stance for this relationship. |

#### `impact_rule`

**Purpose and expected use.** Maps relation types and optional changed/affected item types to reusable risk, investigation task, tool, review, and validation templates. It turns graph traversal into actionable work.

**Primary key.** `impact_rule_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(preferred_tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(investigation_task_type_id)` → `investigation_task_type(investigation_task_type_id)` (ON DELETE RESTRICT); `(risk_level_id)` → `risk_level(risk_level_id)` (ON DELETE RESTRICT); `(affected_item_type_id)` → `item_type(item_type_id)` (ON DELETE RESTRICT); `(changed_item_type_id)` → `item_type(item_type_id)` (ON DELETE RESTRICT); `(relation_type_id)` → `relation_type(relation_type_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_impact_rule_match` — CREATE INDEX idx_impact_rule_match ON impact_rule(relation_type_id, changed_item_type_id, affected_item_type_id, is_active, priority DESC).

| Field | Declaration | Why it exists |
|---|---|---|
| `impact_rule_id` | `impact_rule_id INTEGER PRIMARY KEY` | Stable primary key for the `impact_rule` row. |
| `relation_type_id` | `relation_type_id INTEGER NOT NULL REFERENCES relation_type(relation_type_id) ON DELETE RESTRICT` | Selects the semantic edge type and its impact-propagation mode. |
| `changed_item_type_id` | `changed_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE RESTRICT` | Optionally restricts an impact rule to a changed-item category. |
| `affected_item_type_id` | `affected_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE RESTRICT` | Optionally restricts an impact rule to an affected-item category. |
| `risk_level_id` | `risk_level_id INTEGER NOT NULL REFERENCES risk_level(risk_level_id) ON DELETE RESTRICT` | Selects the normalized risk severity. |
| `investigation_task_type_id` | `investigation_task_type_id INTEGER REFERENCES investigation_task_type(investigation_task_type_id) ON DELETE RESTRICT` | Selects the normalized investigation task. |
| `preferred_tool_item_id` | `preferred_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the preferred tool for this policy or impact action. |
| `priority` | `priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100)` | Rule selection/order when several templates match an arc. |
| `action_template` | `action_template TEXT NOT NULL` | Reusable review instruction emitted for matching impacts. |
| `validation_template` | `validation_template TEXT` | Reusable validation instruction emitted for matching impacts. |
| `is_active` | `is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))` | Allows a rule to be retired without deletion. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `implementation_reference`

**Purpose and expected use.** Links a mechanic or topic to preferred vanilla examples, mod examples, anti-examples, or compatibility examples with version and evidence locators.

**Primary key.** `implementation_reference_id`

**Table-level integrity rules.** `UNIQUE(topic_item_id, example_item_id, reference_kind, version_span_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(example_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(topic_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_implementation_reference_topic` — CREATE INDEX idx_implementation_reference_topic ON implementation_reference(topic_item_id, version_span_id, reference_kind).

| Field | Declaration | Why it exists |
|---|---|---|
| `implementation_reference_id` | `implementation_reference_id INTEGER PRIMARY KEY` | Stable primary key for the `implementation_reference` row. |
| `topic_item_id` | `topic_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the mechanic or topic for which an implementation example is relevant. |
| `example_item_id` | `example_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the vanilla/mod/compatibility example item. |
| `reference_kind` | `reference_kind TEXT NOT NULL CHECK (reference_kind IN ('vanilla_example','mod_example','anti_example','compatibility_example'))` | Vanilla example, mod example, anti-example, or compatibility example. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `rationale` | `rationale TEXT NOT NULL` | Explains what the example teaches and why it is relevant. |
| `is_preferred` | `is_preferred INTEGER NOT NULL DEFAULT 0 CHECK (is_preferred IN (0,1))` | Marks the first example agents should inspect. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `version_change`

**Purpose and expected use.** Records an explicit delta between two exact Stellaris versions with change kind, evidence state, confidence, risk, migration note, and review requirement.

**Primary key.** `version_change_id`

**Table-level integrity rules.** `CHECK (from_version_id <> to_version_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(detected_by_verification_run_id)` → `verification_run(verification_run_id)` (ON DELETE RESTRICT); `(risk_level_id)` → `risk_level(risk_level_id)` (ON DELETE RESTRICT); `(confidence_level_id)` → `confidence_level(confidence_level_id)` (ON DELETE RESTRICT); `(assessment_state_id)` → `assessment_state(assessment_state_id)` (ON DELETE RESTRICT); `(change_kind_id)` → `change_kind(change_kind_id)` (ON DELETE RESTRICT); `(to_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT); `(from_version_id)` → `game_version(game_version_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_version_change_pair` — CREATE INDEX idx_version_change_pair ON version_change(from_version_id, to_version_id, risk_level_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `version_change_id` | `version_change_id INTEGER PRIMARY KEY` | Stable primary key for the `version_change` row. |
| `change_key` | `change_key TEXT NOT NULL UNIQUE` | Stable identifier for the explicit delta. |
| `from_version_id` | `from_version_id INTEGER NOT NULL REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | References the exact earlier/comparison-source Stellaris version. |
| `to_version_id` | `to_version_id INTEGER NOT NULL REFERENCES game_version(game_version_id) ON DELETE RESTRICT` | References the exact later/comparison-target Stellaris version. |
| `change_kind_id` | `change_kind_id INTEGER NOT NULL REFERENCES change_kind(change_kind_id) ON DELETE RESTRICT` | Classifies the explicit version delta. |
| `summary` | `summary TEXT NOT NULL` | Concise statement of what changed. |
| `assessment_state_id` | `assessment_state_id INTEGER NOT NULL REFERENCES assessment_state(assessment_state_id) ON DELETE RESTRICT` | Selects the normalized epistemic state. |
| `confidence_level_id` | `confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT` | Selects the normalized confidence level. |
| `risk_level_id` | `risk_level_id INTEGER NOT NULL REFERENCES risk_level(risk_level_id) ON DELETE RESTRICT` | Selects the normalized risk severity. |
| `review_required` | `review_required INTEGER NOT NULL CHECK (review_required IN (0,1))` | Explicitly states whether downstream review is mandatory. |
| `migration_note` | `migration_note TEXT` | Actionable porting/revalidation guidance. |
| `detected_by_verification_run_id` | `detected_by_verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT` | References the run that detected or confirmed the delta. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `version_change_item`

**Purpose and expected use.** Links a version delta to all subject, old, new, affected, or review items, enabling impact and comparison queries by mechanic or surface.

**Primary key.** `version_change_id`, `item_id`, `role_code`

**Table-level integrity rules.** `PRIMARY KEY(version_change_id, item_id, role_code)`.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(version_change_id)` → `version_change(version_change_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_version_change_item_item` — CREATE INDEX idx_version_change_item_item ON version_change_item(item_id, version_change_id, role_code).

| Field | Declaration | Why it exists |
|---|---|---|
| `version_change_id` | `version_change_id INTEGER NOT NULL REFERENCES version_change(version_change_id) ON DELETE CASCADE` | References the explicit version-to-version delta. |
| `item_id` | `item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity represented or linked by this row. |
| `role_code` | `role_code TEXT NOT NULL CHECK (role_code IN ('subject','old','new','affected','review'))` | Subject/old/new/affected/review role in the version delta. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `version_change_evidence`

**Purpose and expected use.** Attaches evidence locators and stance to a version delta, preserving both confirmation and qualification.

**Primary key.** `version_change_id`, `evidence_locator_id`, `evidence_stance_id`

**Table-level integrity rules.** `PRIMARY KEY(version_change_id, evidence_locator_id, evidence_stance_id)`.

**Relationships.** `(evidence_stance_id)` → `evidence_stance(evidence_stance_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(version_change_id)` → `version_change(version_change_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `version_change_id` | `version_change_id INTEGER NOT NULL REFERENCES version_change(version_change_id) ON DELETE CASCADE` | References the explicit version-to-version delta. |
| `evidence_locator_id` | `evidence_locator_id INTEGER NOT NULL REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | References the precise reusable evidence location. |
| `evidence_stance_id` | `evidence_stance_id INTEGER NOT NULL REFERENCES evidence_stance(evidence_stance_id) ON DELETE RESTRICT` | Selects whether evidence supports, contradicts, qualifies, or contextualizes. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `checklist`

**Purpose and expected use.** Defines a reusable, graph-addressable maintenance checklist with change type, purpose, and completion criteria.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(retired_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(change_type_id)` → `change_type(change_type_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `change_type_id` | `change_type_id INTEGER NOT NULL REFERENCES change_type(change_type_id) ON DELETE RESTRICT` | Classifies the maintenance change covered by the checklist. |
| `purpose` | `purpose TEXT NOT NULL` | Defines what maintenance decision the checklist supports. |
| `completion_criteria` | `completion_criteria TEXT NOT NULL` | Auditable definition of done. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |
| `retired_in_change_set_id` | `retired_in_change_set_id INTEGER REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that retired this row without deleting history. |

#### `checklist_target`

**Purpose and expected use.** Declares the items and version spans to which a checklist applies, allowing one checklist to cover a subsystem, mechanic, or porting target without copying its steps.

**Primary key.** `checklist_item_id`, `target_item_id`, `version_span_id`

**Table-level integrity rules.** `PRIMARY KEY(checklist_item_id, target_item_id, version_span_id)`.

**Relationships.** `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(target_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(checklist_item_id)` → `checklist(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_checklist_target_target` — CREATE INDEX idx_checklist_target_target ON checklist_target(target_item_id, version_span_id, checklist_item_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `checklist_item_id` | `checklist_item_id INTEGER NOT NULL REFERENCES checklist(item_id) ON DELETE CASCADE` | References the typed checklist containing the target or step. |
| `target_item_id` | `target_item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the semantic target of the relationship or route selector. |
| `version_span_id` | `version_span_id INTEGER NOT NULL REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `applicability_note` | `applicability_note TEXT NOT NULL` | Explains target-specific use or exclusions. |

#### `checklist_step`

**Purpose and expected use.** Stores ordered, phase-aware, required/blocking work instructions with rationale, tool/task routing, expected result, and failure action.

**Primary key.** `checklist_step_id`

**Table-level integrity rules.** `UNIQUE(checklist_item_id, step_number)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(investigation_task_type_id)` → `investigation_task_type(investigation_task_type_id)` (ON DELETE RESTRICT); `(tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(checklist_item_id)` → `checklist(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_checklist_step_order` — CREATE INDEX idx_checklist_step_order ON checklist_step(checklist_item_id, step_number).

| Field | Declaration | Why it exists |
|---|---|---|
| `checklist_step_id` | `checklist_step_id INTEGER PRIMARY KEY` | Stable primary key for the `checklist_step` row. |
| `checklist_item_id` | `checklist_item_id INTEGER NOT NULL REFERENCES checklist(item_id) ON DELETE CASCADE` | References the typed checklist containing the target or step. |
| `step_number` | `step_number INTEGER NOT NULL CHECK (step_number >= 1)` | Stable execution order within the checklist. |
| `phase_code` | `phase_code TEXT NOT NULL` | Groups steps into discovery, design, edit, static validation, compatibility, or runtime phases. |
| `title` | `title TEXT NOT NULL` | Short action name. |
| `instruction` | `instruction TEXT NOT NULL` | Exact work to perform. |
| `rationale` | `rationale TEXT NOT NULL` | Why the step exists and what risk it controls. |
| `is_required` | `is_required INTEGER NOT NULL CHECK (is_required IN (0,1))` | Whether omission requires an explicit waiver. |
| `is_blocking` | `is_blocking INTEGER NOT NULL CHECK (is_blocking IN (0,1))` | Whether failure must stop the change. |
| `tool_item_id` | `tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the typed tool used or recommended. |
| `investigation_task_type_id` | `investigation_task_type_id INTEGER REFERENCES investigation_task_type(investigation_task_type_id) ON DELETE RESTRICT` | Selects the normalized investigation task. |
| `expected_result` | `expected_result TEXT` | Observable success criterion. |
| `failure_action` | `failure_action TEXT` | Required response when the expected result is not obtained. |
| `version_span_id` | `version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to the change set that introduced this row, providing write provenance. |

#### `checklist_step_item`

**Purpose and expected use.** Links a checklist step to every item it must inspect, modify, validate, compare, require, or produce.

**Primary key.** `checklist_step_id`, `item_id`, `role_code`

**Table-level integrity rules.** `PRIMARY KEY(checklist_step_id, item_id, role_code)`.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(checklist_step_id)` → `checklist_step(checklist_step_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_checklist_step_item_item` — CREATE INDEX idx_checklist_step_item_item ON checklist_step_item(item_id, role_code, checklist_step_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `checklist_step_id` | `checklist_step_id INTEGER NOT NULL REFERENCES checklist_step(checklist_step_id) ON DELETE CASCADE` | References the ordered checklist step. |
| `item_id` | `item_id INTEGER NOT NULL REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity represented or linked by this row. |
| `role_code` | `role_code TEXT NOT NULL CHECK (role_code IN ('inspect','modify','validate','compare','prerequisite','output'))` | Inspect, modify, validate, compare, prerequisite, or output role. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `tool`

**Purpose and expected use.** Represents an existing local or external tool as a typed knowledge item, including its authority boundary and invocation/output locator conventions.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity represented or linked by this row. |
| `tool_kind` | `tool_kind TEXT NOT NULL` | Tool category such as schema checker, conflict manager, source index, validator, log viewer, or save extractor. |
| `executable_or_entrypoint` | `executable_or_entrypoint TEXT` | Local executable, script, command, or index entrypoint. |
| `authority_scope` | `authority_scope TEXT NOT NULL` | What conclusions the tool may authoritatively support. |
| `default_invocation` | `default_invocation TEXT` | Normal command or interaction pattern. |
| `output_locator_pattern` | `output_locator_pattern TEXT` | How to identify a reusable locator in the tool’s output. |
| `is_local_only` | `is_local_only INTEGER NOT NULL CHECK (is_local_only IN (0,1))` | Whether the tool is available only in the local environment. |
| `notes` | `notes TEXT` | Optional caveats or local context that do not warrant a separate normalized relation. |

#### `tool_capability`

**Purpose and expected use.** Describes what a tool can do for a normalized investigation task, how to invoke it, what output to expect, limitations, and preference priority.

**Primary key.** `tool_capability_id`

**Table-level integrity rules.** `UNIQUE(tool_item_id, investigation_task_type_id, capability_summary)`.

**Relationships.** `(investigation_task_type_id)` → `investigation_task_type(investigation_task_type_id)` (ON DELETE RESTRICT); `(tool_item_id)` → `tool(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_tool_capability_task` — CREATE INDEX idx_tool_capability_task ON tool_capability(investigation_task_type_id, priority DESC, tool_item_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `tool_capability_id` | `tool_capability_id INTEGER PRIMARY KEY` | Stable primary key for the `tool_capability` row. |
| `tool_item_id` | `tool_item_id INTEGER NOT NULL REFERENCES tool(item_id) ON DELETE CASCADE` | References the typed tool used or recommended. |
| `investigation_task_type_id` | `investigation_task_type_id INTEGER NOT NULL REFERENCES investigation_task_type(investigation_task_type_id) ON DELETE RESTRICT` | Selects the normalized investigation task. |
| `capability_summary` | `capability_summary TEXT NOT NULL` | Specific supported investigation capability. |
| `invocation_template` | `invocation_template TEXT` | Parameterized invocation for the task. |
| `expected_output` | `expected_output TEXT NOT NULL` | Evidence or report shape that should result. |
| `limitations` | `limitations TEXT` | Known proof boundaries or missing visibility. |
| `priority` | `priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 100)` | Preference among tools capable of the same task. |

#### `tool_route`

**Purpose and expected use.** Routes a specific item, item type, or evidence source type to a tool capability for an optional version span, with priority, instructions, and fallback. A check constraint requires exactly one selector.

**Primary key.** `tool_route_id`

**Table-level integrity rules.** `CHECK ( (target_item_id IS NOT NULL) + (target_item_type_id IS NOT NULL) + (evidence_source_type_id IS NOT NULL) = 1 )`.

**Relationships.** `(fallback_tool_capability_id)` → `tool_capability(tool_capability_id)` (ON DELETE RESTRICT); `(version_span_id)` → `version_span(version_span_id)` (ON DELETE RESTRICT); `(evidence_source_type_id)` → `evidence_source_type(evidence_source_type_id)` (ON DELETE CASCADE); `(target_item_type_id)` → `item_type(item_type_id)` (ON DELETE CASCADE); `(target_item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE); `(tool_capability_id)` → `tool_capability(tool_capability_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_tool_route_item` — CREATE INDEX idx_tool_route_item ON tool_route(target_item_id, version_span_id, route_priority DESC) WHERE target_item_id IS NOT NULL; `idx_tool_route_source_type` — CREATE INDEX idx_tool_route_source_type ON tool_route(evidence_source_type_id, version_span_id, route_priority DESC) WHERE evidence_source_type_id IS NOT NULL; `idx_tool_route_type` — CREATE INDEX idx_tool_route_type ON tool_route(target_item_type_id, version_span_id, route_priority DESC) WHERE target_item_type_id IS NOT NULL.

| Field | Declaration | Why it exists |
|---|---|---|
| `tool_route_id` | `tool_route_id INTEGER PRIMARY KEY` | Stable primary key for the `tool_route` row. |
| `tool_capability_id` | `tool_capability_id INTEGER NOT NULL REFERENCES tool_capability(tool_capability_id) ON DELETE CASCADE` | References the tool/task capability selected by the route. |
| `target_item_id` | `target_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | References the semantic target of the relationship or route selector. |
| `target_item_type_id` | `target_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE CASCADE` | Optionally selects all knowledge items of a type for routing. |
| `evidence_source_type_id` | `evidence_source_type_id INTEGER REFERENCES evidence_source_type(evidence_source_type_id) ON DELETE CASCADE` | Classifies the source system’s evidence type and authority boundary. |
| `version_span_id` | `version_span_id INTEGER REFERENCES version_span(version_span_id) ON DELETE RESTRICT` | Selects the normalized Stellaris-version applicability interval. |
| `route_priority` | `route_priority INTEGER NOT NULL CHECK (route_priority BETWEEN 1 AND 100)` | Preference among applicable routes. |
| `instructions` | `instructions TEXT NOT NULL` | Target-specific retrieval or validation instructions. |
| `fallback_tool_capability_id` | `fallback_tool_capability_id INTEGER REFERENCES tool_capability(tool_capability_id) ON DELETE RESTRICT` | References the capability to use when the preferred route is unavailable or insufficient. |
| `is_active` | `is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))` | Allows a route to be retired without deleting its history. |

### 7. Analysis models, scenarios, facts, gates, policies, and issues

This group fits the existing wide modeling CSVs and runtime diagnostics into typed scenarios, dimensions, facts, gates, policies, and issue queues.

#### `analysis_model`

**Purpose and expected use.** Registers a durable inventory, valuation, policy, diagnostic, comparison, coverage, or observer model as a typed knowledge item. It records the authoritative tool boundary and whether results should remain locators or selected normalized facts.

**Primary key.** `item_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(authoritative_tool_item_id)` → `tool(item_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `item_id` | `item_id INTEGER PRIMARY KEY REFERENCES knowledge_item(item_id) ON DELETE CASCADE` | Stable primary key for the `analysis_model` row. |
| `model_key` | `model_key TEXT NOT NULL UNIQUE` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `model_kind` | `model_kind TEXT NOT NULL CHECK (model_kind IN ('inventory','valuation','policy','diagnostic','comparison','coverage','observer','other'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `purpose` | `purpose TEXT NOT NULL` | Concise durable explanation needed to interpret the normalized row and its evidence boundary. |
| `authoritative_tool_item_id` | `authoritative_tool_item_id INTEGER REFERENCES tool(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `analysis_model` role (`tool.item_id`). |
| `authority_boundary` | `authority_boundary TEXT NOT NULL` | States exactly what the model/tool output proves and what still requires source or runtime evidence. |
| `default_storage_policy` | `default_storage_policy TEXT NOT NULL CHECK (default_storage_policy IN ('locator_only','selected_facts','normalized_facts'))` | Controls whether outputs remain locators or selected normalized facts. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `analysis_run`

**Purpose and expected use.** Captures one execution of an analysis model with target version, execution context, tool, input fingerprint, timestamps, outcome, reported dimensions, and change-set provenance.

**Primary key.** `analysis_run_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(generator_artifact_id)` → `source_artifact(source_artifact_id)` (ON DELETE RESTRICT); `(repository_snapshot_id)` → `repository_snapshot(repository_snapshot_id)` (ON DELETE RESTRICT); `(verification_run_id)` → `verification_run(verification_run_id)` (ON DELETE RESTRICT); `(execution_context_id)` → `execution_context(execution_context_id)` (ON DELETE RESTRICT); `(model_item_id)` → `analysis_model(item_id)` (ON DELETE RESTRICT).

**Important explicit indexes.** `idx_analysis_run_model_context` — CREATE INDEX idx_analysis_run_model_context ON analysis_run(model_item_id, execution_context_id, completed_at, outcome_code).

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_run_id` | `analysis_run_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_run` row. |
| `run_key` | `run_key TEXT NOT NULL UNIQUE` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `model_item_id` | `model_item_id INTEGER NOT NULL REFERENCES analysis_model(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `analysis_run` role (`analysis_model.item_id`). |
| `execution_context_id` | `execution_context_id INTEGER REFERENCES execution_context(execution_context_id) ON DELETE RESTRICT` | Foreign key to `execution_context.execution_context_id`, preserving normalized identity and referential integrity. |
| `verification_run_id` | `verification_run_id INTEGER REFERENCES verification_run(verification_run_id) ON DELETE RESTRICT` | Foreign key to `verification_run.verification_run_id`, preserving normalized identity and referential integrity. |
| `repository_snapshot_id` | `repository_snapshot_id INTEGER REFERENCES repository_snapshot(repository_snapshot_id) ON DELETE RESTRICT` | Foreign key to `repository_snapshot.repository_snapshot_id`, preserving normalized identity and referential integrity. |
| `model_version` | `model_version TEXT NOT NULL` | Stores the normalized `model_version` attribute needed to query and maintain `analysis_run` records without an EAV or JSON fallback. |
| `generator_artifact_id` | `generator_artifact_id INTEGER REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT` | Foreign key to `source_artifact.source_artifact_id`, preserving normalized identity and referential integrity. |
| `schema_version` | `schema_version TEXT` | Stores the normalized `schema_version` attribute needed to query and maintain `analysis_run` records without an EAV or JSON fallback. |
| `command_or_method` | `command_or_method TEXT` | Stores the normalized `command_or_method` attribute needed to query and maintain `analysis_run` records without an EAV or JSON fallback. |
| `input_fingerprint` | `input_fingerprint TEXT` | Hash or deterministic summary of the source roots/playset/artifacts used by the run. |
| `started_at` | `started_at TEXT` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `completed_at` | `completed_at TEXT` | ISO-8601 date/time or date used to order history, determine freshness, and schedule revalidation. |
| `outcome_code` | `outcome_code TEXT NOT NULL CHECK (outcome_code IN ('passed','failed','partial','inconclusive','not_run'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `reported_row_count` | `reported_row_count INTEGER CHECK (reported_row_count IS NULL OR reported_row_count >= 0)` | Generator-reported principal row count used for drift and completeness checks. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `analysis_run_artifact`

**Purpose and expected use.** Links an analysis run to each input, output, report, log, save, schema, or policy artifact and marks which roles are required for reproducibility.

**Primary key.** `analysis_run_id`, `source_artifact_id`, `artifact_role`

**Table-level integrity rules.** `PRIMARY KEY(analysis_run_id, source_artifact_id, artifact_role)`.

**Relationships.** `(dataset_schema_id)` → `dataset_schema(dataset_schema_id)` (ON DELETE RESTRICT); `(source_artifact_id)` → `source_artifact(source_artifact_id)` (ON DELETE RESTRICT); `(analysis_run_id)` → `analysis_run(analysis_run_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_run_id` | `analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE` | Stable primary key for the `analysis_run_artifact` row. |
| `source_artifact_id` | `source_artifact_id INTEGER NOT NULL REFERENCES source_artifact(source_artifact_id) ON DELETE RESTRICT` | Stable primary key for the `analysis_run_artifact` row. |
| `artifact_role` | `artifact_role TEXT NOT NULL CHECK (artifact_role IN ('input','output','report','manifest','log','source_code','comparison_baseline'))` | Stable primary key for the `analysis_run_artifact` row. |
| `dataset_schema_id` | `dataset_schema_id INTEGER REFERENCES dataset_schema(dataset_schema_id) ON DELETE RESTRICT` | Foreign key to `dataset_schema.dataset_schema_id`, preserving normalized identity and referential integrity. |
| `is_required` | `is_required INTEGER NOT NULL CHECK (is_required IN (0,1))` | Strict 0/1 flag for the named state so agents do not infer it from prose. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `analysis_scenario`

**Purpose and expected use.** Defines ordered baseline, optimistic, conservative, triggered, prerequisite-qualified, game-date, comparison, or project-specific scenarios within one run. Parent scenarios support controlled inheritance without encoding assumptions in column names alone.

**Primary key.** `analysis_scenario_id`

**Table-level integrity rules.** `UNIQUE(analysis_run_id, scenario_key)`; `UNIQUE(analysis_run_id, ordinal)`.

**Relationships.** `(parent_scenario_id)` → `analysis_scenario(analysis_scenario_id)` (ON DELETE RESTRICT); `(analysis_run_id)` → `analysis_run(analysis_run_id)` (ON DELETE CASCADE).

**Important explicit indexes.** None beyond primary-key/UNIQUE indexes generated by SQLite; expected volume and access path do not justify another day-one index.

**Triggers.** `trg_analysis_scenario_parent_run_insert`.

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_scenario_id` | `analysis_scenario_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_scenario` row. |
| `analysis_run_id` | `analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE` | Foreign key to `analysis_run.analysis_run_id`, preserving normalized identity and referential integrity. |
| `scenario_key` | `scenario_key TEXT NOT NULL` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `scenario_name` | `scenario_name TEXT NOT NULL` | Human-readable name used in query results and review output while the machine key remains stable. |
| `scenario_family` | `scenario_family TEXT NOT NULL` | Groups base, triggered, conservative, optimistic, prerequisite-qualified, date, or comparison scenarios. |
| `parent_scenario_id` | `parent_scenario_id INTEGER REFERENCES analysis_scenario(analysis_scenario_id) ON DELETE RESTRICT` | Optional inheritance/provenance link between scenario variants. |
| `ordinal` | `ordinal INTEGER NOT NULL CHECK (ordinal >= 1)` | Ordered numeric coordinate or rank used for deterministic traversal, display, or validation. |
| `assumptions_summary` | `assumptions_summary TEXT NOT NULL` | Concise durable explanation needed to interpret the normalized row and its evidence boundary. |
| `is_baseline` | `is_baseline INTEGER NOT NULL CHECK (is_baseline IN (0,1))` | Strict 0/1 flag for the named state so agents do not infer it from prose. |

#### `analysis_subject`

**Purpose and expected use.** Provides a stable run-local coordinate for a knowledge item, external dataset record, runtime entity, aggregate, policy class, or version pair. It is the subject to which metrics, gates, policies, and issues attach.

**Primary key.** `analysis_subject_id`

**Table-level integrity rules.** `CHECK (item_id IS NOT NULL OR source_locator_id IS NOT NULL OR external_key IS NOT NULL OR subject_kind IN ('aggregate','policy_class','version_pair','other'))`; `UNIQUE(analysis_run_id, subject_key)`.

**Relationships.** `(parent_subject_id)` → `analysis_subject(analysis_subject_id)` (ON DELETE CASCADE); `(source_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(analysis_run_id)` → `analysis_run(analysis_run_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_analysis_subject_external` — CREATE INDEX idx_analysis_subject_external ON analysis_subject(external_type, external_key, analysis_run_id); `idx_analysis_subject_item` — CREATE INDEX idx_analysis_subject_item ON analysis_subject(item_id, analysis_run_id, subject_kind).

**Triggers.** `trg_analysis_subject_parent_run_insert`.

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_subject_id` | `analysis_subject_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_subject` row. |
| `analysis_run_id` | `analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE` | Foreign key to `analysis_run.analysis_run_id`, preserving normalized identity and referential integrity. |
| `subject_key` | `subject_key TEXT NOT NULL` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `subject_kind` | `subject_kind TEXT NOT NULL CHECK (subject_kind IN ('knowledge_item','external_record','runtime_entity','aggregate','policy_class','version_pair','other'))` | Distinguishes a stable item, external record, runtime entity, aggregate, policy class, version pair, or other subject. |
| `item_id` | `item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `analysis_subject` role (`knowledge_item.item_id`). |
| `source_locator_id` | `source_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Directly anchors an external-record/runtime subject to the exact evidence row or section. |
| `parent_subject_id` | `parent_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE` | Foreign key to `analysis_subject.analysis_subject_id`, preserving normalized identity and referential integrity. |
| `external_type` | `external_type TEXT` | Stores the structured `external_type` attribute required to interpret, route, retrieve, or validate the row. |
| `external_key` | `external_key TEXT` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `label` | `label TEXT NOT NULL` | Human-readable name used in query results and review output while the machine key remains stable. |
| `status_code` | `status_code TEXT` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `analysis_subject_member`

**Purpose and expected use.** Normalizes the members of an aggregate or composite subject, with role, order, quantity, and weight. It supports colony plans, fleets, conflict sets, and grouped runtime populations without storing an opaque list.

**Primary key.** `analysis_subject_member_id`

**Table-level integrity rules.** `CHECK ((member_subject_id IS NOT NULL) + (member_item_id IS NOT NULL) = 1)`; `CHECK (member_subject_id IS NULL OR member_subject_id <> parent_subject_id)`.

**Relationships.** `(member_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(member_subject_id)` → `analysis_subject(analysis_subject_id)` (ON DELETE RESTRICT); `(parent_subject_id)` → `analysis_subject(analysis_subject_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_analysis_subject_member_reverse` — CREATE INDEX idx_analysis_subject_member_reverse ON analysis_subject_member(member_subject_id, member_item_id, role_code); `uq_analysis_subject_member` — CREATE UNIQUE INDEX uq_analysis_subject_member ON analysis_subject_member(parent_subject_id, role_code, ifnull(member_subject_id,-1), ifnull(member_item_id,-1), ifnull(ordinal,-1)).

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_subject_member_id` | `analysis_subject_member_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_subject_member` row. |
| `parent_subject_id` | `parent_subject_id INTEGER NOT NULL REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE` | Foreign key to `analysis_subject.analysis_subject_id`, preserving normalized identity and referential integrity. |
| `member_subject_id` | `member_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE RESTRICT` | References another run-local subject when the member itself has metrics or identity in the run. |
| `member_item_id` | `member_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References a stable knowledge item when no separate run-local subject is needed. |
| `role_code` | `role_code TEXT NOT NULL` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `ordinal` | `ordinal INTEGER CHECK (ordinal IS NULL OR ordinal >= 1)` | Ordered numeric coordinate or rank used for deterministic traversal, display, or validation. |
| `quantity` | `quantity REAL` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `weight` | `weight REAL` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `analysis_metric`

**Purpose and expected use.** Declares each model metric once with value type, unit, aggregation semantics, optional dimension item type, subject restriction, and stability contract. Metrics remain typed and queryable across runs.

**Primary key.** `analysis_metric_id`

**Table-level integrity rules.** `UNIQUE(model_item_id, metric_key)`.

**Relationships.** `(dimension_item_type_id)` → `item_type(item_type_id)` (ON DELETE RESTRICT); `(model_item_id)` → `analysis_model(item_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_analysis_metric_lookup` — CREATE INDEX idx_analysis_metric_lookup ON analysis_metric(model_item_id, aggregation_semantics, dimension_item_type_id).

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_metric_id` | `analysis_metric_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_metric` row. |
| `model_item_id` | `model_item_id INTEGER NOT NULL REFERENCES analysis_model(item_id) ON DELETE CASCADE` | References the stable knowledge-item identity required by this `analysis_metric` role (`analysis_model.item_id`). |
| `metric_key` | `metric_key TEXT NOT NULL` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `metric_name` | `metric_name TEXT NOT NULL` | Human-readable name used in query results and review output while the machine key remains stable. |
| `value_type` | `value_type TEXT NOT NULL CHECK (value_type IN ('integer','real','text','boolean'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `unit` | `unit TEXT` | Stores the structured `unit` attribute required to interpret, route, retrieve, or validate the row. |
| `aggregation_semantics` | `aggregation_semantics TEXT NOT NULL CHECK (aggregation_semantics IN ('additive','ratio','score','categorical','set_count','identifier','boolean','other'))` | Tells consumers whether values add, form ratios/scores/counts/identifiers/booleans, or require another rule. |
| `dimension_item_type_id` | `dimension_item_type_id INTEGER REFERENCES item_type(item_type_id) ON DELETE RESTRICT` | Optional required item type for dimension_item_id, enforced by semantic checks/triggers. |
| `allowed_subject_kind` | `allowed_subject_kind TEXT` | Stores the normalized `allowed_subject_kind` attribute needed to query and maintain `analysis_metric` records without an EAV or JSON fallback. |
| `description` | `description TEXT NOT NULL` | Defines the durable project meaning of this row or controlled value. |
| `stable_across_runs` | `stable_across_runs INTEGER NOT NULL CHECK (stable_across_runs IN (0,1))` | Stores the normalized `stable_across_runs` attribute needed to query and maintain `analysis_metric` records without an EAV or JSON fallback. |

#### `analysis_value`

**Purpose and expected use.** Stores one typed fact at the coordinate subject × scenario × metric × optional dimension item × ordinal. Exactly one integer, real, text, or boolean value is present, with evidence and confidence where appropriate.

**Primary key.** `analysis_value_id`

**Table-level integrity rules.** `CHECK ((integer_value IS NOT NULL) + (real_value IS NOT NULL) + (text_value IS NOT NULL) + (boolean_value IS NOT NULL) = 1)`.

**Relationships.** `(confidence_level_id)` → `confidence_level(confidence_level_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(dimension_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(analysis_metric_id)` → `analysis_metric(analysis_metric_id)` (ON DELETE RESTRICT); `(analysis_scenario_id)` → `analysis_scenario(analysis_scenario_id)` (ON DELETE CASCADE); `(analysis_subject_id)` → `analysis_subject(analysis_subject_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_analysis_value_metric` — CREATE INDEX idx_analysis_value_metric ON analysis_value(analysis_metric_id, dimension_item_id, analysis_scenario_id); `uq_analysis_value_coordinate` — CREATE UNIQUE INDEX uq_analysis_value_coordinate ON analysis_value(analysis_subject_id, ifnull(analysis_scenario_id,-1), analysis_metric_id, ifnull(dimension_item_id,-1), ordinal).

**Triggers.** `trg_analysis_value_consistency_insert`.

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_value_id` | `analysis_value_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_value` row. |
| `analysis_subject_id` | `analysis_subject_id INTEGER NOT NULL REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE` | Foreign key to `analysis_subject.analysis_subject_id`, preserving normalized identity and referential integrity. |
| `analysis_scenario_id` | `analysis_scenario_id INTEGER REFERENCES analysis_scenario(analysis_scenario_id) ON DELETE CASCADE` | Foreign key to `analysis_scenario.analysis_scenario_id`, preserving normalized identity and referential integrity. |
| `analysis_metric_id` | `analysis_metric_id INTEGER NOT NULL REFERENCES analysis_metric(analysis_metric_id) ON DELETE RESTRICT` | Foreign key to `analysis_metric.analysis_metric_id`, preserving normalized identity and referential integrity. |
| `dimension_item_id` | `dimension_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | Optional typed dimension such as resource, technology, mod, or benefit class. |
| `ordinal` | `ordinal INTEGER NOT NULL DEFAULT 1 CHECK (ordinal >= 1)` | Allows repeated values at the same logical coordinate while preserving deterministic order. |
| `integer_value` | `integer_value INTEGER` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `real_value` | `real_value REAL` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `text_value` | `text_value TEXT` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `boolean_value` | `boolean_value INTEGER CHECK (boolean_value IS NULL OR boolean_value IN (0,1))` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Foreign key to `evidence_locator.evidence_locator_id`, preserving normalized identity and referential integrity. |
| `confidence_level_id` | `confidence_level_id INTEGER REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT` | Foreign key to `confidence_level.confidence_level_id`, preserving normalized identity and referential integrity. |
| `source_terms` | `source_terms TEXT` | Preserves the exact source terms or generator terms that produced the normalized fact. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `analysis_gate`

**Purpose and expected use.** Stores hard or soft prerequisites, potential/allow conditions, event/unlock flags, capital tiers, safety gates, and consumer gates separately from scores. Agents can therefore explain why an object is unavailable or conditional.

**Primary key.** `analysis_gate_id`

**Table-level integrity rules.** Inline column constraints, primary/foreign keys, and indexes shown below; no additional table-level expression.

**Relationships.** `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(target_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(analysis_scenario_id)` → `analysis_scenario(analysis_scenario_id)` (ON DELETE CASCADE); `(analysis_subject_id)` → `analysis_subject(analysis_subject_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_analysis_gate_queue` — CREATE INDEX idx_analysis_gate_queue ON analysis_gate(state_code, is_hard, gate_kind, target_item_id); `uq_analysis_gate` — CREATE UNIQUE INDEX uq_analysis_gate ON analysis_gate(analysis_subject_id, ifnull(analysis_scenario_id,-1), gate_kind, gate_key, ifnull(target_item_id,-1)).

**Triggers.** `trg_analysis_gate_consistency_insert`.

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_gate_id` | `analysis_gate_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_gate` row. |
| `analysis_subject_id` | `analysis_subject_id INTEGER NOT NULL REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE` | Foreign key to `analysis_subject.analysis_subject_id`, preserving normalized identity and referential integrity. |
| `analysis_scenario_id` | `analysis_scenario_id INTEGER REFERENCES analysis_scenario(analysis_scenario_id) ON DELETE CASCADE` | Foreign key to `analysis_scenario.analysis_scenario_id`, preserving normalized identity and referential integrity. |
| `gate_kind` | `gate_kind TEXT NOT NULL CHECK (gate_kind IN ('prerequisite','potential','allow','event_flag','unlock_flag','capital_tier','availability','safety','consumer','other'))` | Separates prerequisite, potential, allow, flag, tier, availability, safety, and consumer gates. |
| `gate_key` | `gate_key TEXT NOT NULL` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `target_item_id` | `target_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `analysis_gate` role (`knowledge_item.item_id`). |
| `phase_code` | `phase_code TEXT` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `state_code` | `state_code TEXT NOT NULL CHECK (state_code IN ('satisfied','unsatisfied','conditional','unknown','not_applicable'))` | Reports satisfied, unsatisfied, conditional, unknown, or not applicable. |
| `is_hard` | `is_hard INTEGER NOT NULL CHECK (is_hard IN (0,1))` | Distinguishes eligibility blockers from scoring preferences. |
| `expression_text` | `expression_text TEXT` | Preserves the exact text/expression needed for review without substituting it for typed relational facts. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Foreign key to `evidence_locator.evidence_locator_id`, preserving normalized identity and referential integrity. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

#### `analysis_policy`

**Purpose and expected use.** Stores source-backed formula, consumer, readiness, fallback, replacement, classification, zero-effect, or detected-only decisions. It prevents unsupported model rows from receiving invented numeric scores.

**Primary key.** `analysis_policy_id`

**Table-level integrity rules.** `CHECK (supersedes_policy_id IS NULL OR supersedes_policy_id <> analysis_policy_id)`.

**Relationships.** `(created_in_change_set_id)` → `change_set(change_set_id)` (ON DELETE RESTRICT); `(supersedes_policy_id)` → `analysis_policy(analysis_policy_id)` (ON DELETE RESTRICT); `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(confidence_level_id)` → `confidence_level(confidence_level_id)` (ON DELETE RESTRICT); `(fallback_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(fallback_subject_id)` → `analysis_subject(analysis_subject_id)` (ON DELETE RESTRICT); `(dimension_item_id)` → `knowledge_item(item_id)` (ON DELETE RESTRICT); `(analysis_metric_id)` → `analysis_metric(analysis_metric_id)` (ON DELETE RESTRICT); `(analysis_subject_id)` → `analysis_subject(analysis_subject_id)` (ON DELETE CASCADE); `(analysis_run_id)` → `analysis_run(analysis_run_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_analysis_policy_lookup` — CREATE INDEX idx_analysis_policy_lookup ON analysis_policy(analysis_run_id, policy_kind, policy_status, analysis_subject_id, analysis_metric_id).

**Triggers.** `trg_analysis_policy_consistency_insert`.

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_policy_id` | `analysis_policy_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_policy` row. |
| `analysis_run_id` | `analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE` | Foreign key to `analysis_run.analysis_run_id`, preserving normalized identity and referential integrity. |
| `analysis_subject_id` | `analysis_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE` | Foreign key to `analysis_subject.analysis_subject_id`, preserving normalized identity and referential integrity. |
| `analysis_metric_id` | `analysis_metric_id INTEGER REFERENCES analysis_metric(analysis_metric_id) ON DELETE RESTRICT` | Foreign key to `analysis_metric.analysis_metric_id`, preserving normalized identity and referential integrity. |
| `dimension_item_id` | `dimension_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `analysis_policy` role (`knowledge_item.item_id`). |
| `policy_kind` | `policy_kind TEXT NOT NULL CHECK (policy_kind IN ('formula','consumer','readiness','fallback','replacement','classification','zero_effect','detected_only','other'))` | Classifies formula, consumer, readiness, fallback, replacement, classification, zero-effect, detected-only, or other policy. |
| `decision_code` | `decision_code TEXT NOT NULL` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `policy_status` | `policy_status TEXT NOT NULL CHECK (policy_status IN ('active','draft','blocked','superseded'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `formula_or_policy_text` | `formula_or_policy_text TEXT NOT NULL` | Stores the explicit deterministic rule or non-scoring policy instead of an opaque status. |
| `numeric_parameter` | `numeric_parameter REAL` | Typed value or parameter used by the named fact/policy coordinate; surrounding constraints prevent ambiguous storage. |
| `can_consume_code` | `can_consume_code TEXT NOT NULL DEFAULT 'not_applicable' CHECK (can_consume_code IN ('yes','no','conditional','not_applicable'))` | States whether a downstream consumer may use the row now, conditionally, not at all, or not applicable. |
| `fallback_subject_id` | `fallback_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE RESTRICT` | Foreign key to `analysis_subject.analysis_subject_id`, preserving normalized identity and referential integrity. |
| `fallback_item_id` | `fallback_item_id INTEGER REFERENCES knowledge_item(item_id) ON DELETE RESTRICT` | References the stable knowledge-item identity required by this `analysis_policy` role (`knowledge_item.item_id`). |
| `confidence_level_id` | `confidence_level_id INTEGER NOT NULL REFERENCES confidence_level(confidence_level_id) ON DELETE RESTRICT` | Foreign key to `confidence_level.confidence_level_id`, preserving normalized identity and referential integrity. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Foreign key to `evidence_locator.evidence_locator_id`, preserving normalized identity and referential integrity. |
| `next_action` | `next_action TEXT` | Stores the normalized `next_action` attribute needed to query and maintain `analysis_policy` records without an EAV or JSON fallback. |
| `supersedes_policy_id` | `supersedes_policy_id INTEGER REFERENCES analysis_policy(analysis_policy_id) ON DELETE RESTRICT` | Foreign key to `analysis_policy.analysis_policy_id`, preserving normalized identity and referential integrity. |
| `created_in_change_set_id` | `created_in_change_set_id INTEGER NOT NULL REFERENCES change_set(change_set_id) ON DELETE RESTRICT` | Foreign key to `change_set.change_set_id`, preserving normalized identity and referential integrity. |

#### `analysis_issue`

**Purpose and expected use.** Maintains the exact unresolved, resolved, accepted, excluded, or zero-effect issue queue for a model/run/subject, including missing evidence, resolution policy, linked question, priority, and evidence.

**Primary key.** `analysis_issue_id`

**Table-level integrity rules.** `UNIQUE(analysis_run_id, analysis_subject_id, issue_type, issue_key)`.

**Relationships.** `(evidence_locator_id)` → `evidence_locator(evidence_locator_id)` (ON DELETE RESTRICT); `(question_id)` → `open_question(question_id)` (ON DELETE RESTRICT); `(resolution_policy_id)` → `analysis_policy(analysis_policy_id)` (ON DELETE RESTRICT); `(analysis_subject_id)` → `analysis_subject(analysis_subject_id)` (ON DELETE CASCADE); `(analysis_run_id)` → `analysis_run(analysis_run_id)` (ON DELETE CASCADE).

**Important explicit indexes.** `idx_analysis_issue_queue` — CREATE INDEX idx_analysis_issue_queue ON analysis_issue(status_code, severity_code, priority DESC, issue_type).

**Triggers.** `trg_analysis_issue_consistency_insert`.

| Field | Declaration | Why it exists |
|---|---|---|
| `analysis_issue_id` | `analysis_issue_id INTEGER PRIMARY KEY` | Stable primary key for the `analysis_issue` row. |
| `analysis_run_id` | `analysis_run_id INTEGER NOT NULL REFERENCES analysis_run(analysis_run_id) ON DELETE CASCADE` | Foreign key to `analysis_run.analysis_run_id`, preserving normalized identity and referential integrity. |
| `analysis_subject_id` | `analysis_subject_id INTEGER REFERENCES analysis_subject(analysis_subject_id) ON DELETE CASCADE` | Foreign key to `analysis_subject.analysis_subject_id`, preserving normalized identity and referential integrity. |
| `issue_type` | `issue_type TEXT NOT NULL` | Stores the normalized `issue_type` attribute needed to query and maintain `analysis_issue` records without an EAV or JSON fallback. |
| `issue_key` | `issue_key TEXT NOT NULL` | Stable machine key used for deterministic lookup, deduplication, comparison, and external references. |
| `status_code` | `status_code TEXT NOT NULL CHECK (status_code IN ('open','resolved','classified_zero_effect','excluded','accepted','superseded'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `severity_code` | `severity_code TEXT NOT NULL CHECK (severity_code IN ('info','warning','error','critical'))` | Controlled code used for filtering and workflow decisions without relying on display text. |
| `priority` | `priority INTEGER NOT NULL CHECK (priority BETWEEN 0 AND 100)` | Ordered numeric coordinate or rank used for deterministic traversal, display, or validation. |
| `exact_missing_evidence` | `exact_missing_evidence TEXT` | Names the exact file, row, policy, runtime trace, or human decision still required. |
| `resolution_summary` | `resolution_summary TEXT` | Concise durable explanation needed to interpret the normalized row and its evidence boundary. |
| `resolution_policy_id` | `resolution_policy_id INTEGER REFERENCES analysis_policy(analysis_policy_id) ON DELETE RESTRICT` | Links an issue to the policy that classified or resolved it. |
| `question_id` | `question_id INTEGER REFERENCES open_question(question_id) ON DELETE RESTRICT` | Foreign key to `open_question.question_id`, preserving normalized identity and referential integrity. |
| `evidence_locator_id` | `evidence_locator_id INTEGER REFERENCES evidence_locator(evidence_locator_id) ON DELETE RESTRICT` | Foreign key to `evidence_locator.evidence_locator_id`, preserving normalized identity and referential integrity. |
| `notes` | `notes TEXT` | Optional caveats or context that do not justify another normalized relation. |

### 8. Full-text virtual tables

The FTS tables are derived search accelerators. Their rowid maps to the authoritative content table primary key. SQLite-created shadow tables are intentionally omitted from the logical inventory.

| Virtual table | External content | Indexed fields | Use |
|---|---|---|---|
| `item_fts` | `knowledge_item` | `canonical_key`, `display_name`, `summary` | Find mechanics, objects, files, tools, mods, routes, and models when an exact key is unknown. |
| `claim_fts` | `claim` | `statement`, `context`, `epistemic_note` | Discover propositions before applying version/context/evidence filters. |
| `question_fts` | `open_question` | `question_text`, `uncertainty_reason` | Find unresolved research and validation questions. |
| `evidence_fts` | `evidence_locator` | `label`, `excerpt`, `evidence_summary`, `retrieval_instructions` | Discover retrievable evidence anchors, never evidence truth by itself. |

## 13. Derived views

| View | Purpose |
|---|---|
| `v_version_span_version` | Expands each reusable span to exact versions for consistent applicability joins. |
| `v_current_claim_assessment` | Returns current assessments with readable claim/item/version/state/confidence/context fields. |
| `v_claim_evidence_summary` | Aggregates supporting, contradicting, qualifying, and contextual evidence counts/strengths. |
| `v_impact_arc` | Expands stored relation direction into changed-item → affected-item arcs according to propagation mode. |
| `v_reverification_queue` | Combines target-version coverage, epistemic state, confidence, deadlines, and explicit policies. |
| `v_sidecar_type_mismatch` | Semantic integrity check that typed item sidecars match the expected item type. |
| `v_current_playset_member` | Readable current playset membership/order with mod/release/root fields. |
| `v_playset_object_winner` | Readable playset-specific winning definition and origin. |
| `v_analysis_value_typed` | Typed analysis facts with model/run/subject/scenario/metric/dimension metadata. |
| `v_open_analysis_issue` | Prioritized unresolved analysis/model/runtime issues and exact missing evidence. |
| `v_dataset_schema_drift` | Compares consecutive registered schemas in one dataset family. |
| `v_analysis_dimension_type_mismatch` | Semantic integrity check for metric-declared dimension item types. |

## 14. Representative query catalog and validated behavior

The executable examples contain the full SQL. The same bytes were loaded and each query was executed in order.

| Query | Use case | Validated rows |
|---:|---|---:|
| Q1 | Everything known about a mechanic for target version 4.4.5 | 21 |
| Q2 | Supporting, contradicting, and qualifying evidence with provenance | 3 |
| Q3 | Knowledge requiring re-verification | 5 |
| Q4 | Direct and transitive consequences with paths/actions | 33 |
| Q5 | Shortest explanatory relationship path | 1 |
| Q6 | Complete authored + impact-generated subsystem checklist | 43 |
| Q7 | Related triggers, effects, fields, scopes, defines, technologies, resources, and examples | 16 |
| Q8 | Weakly supported, stale, contradicted, uncertain, unknown, or unresolved knowledge | 9 |
| Q9 | Explicit comparison between two Stellaris versions | 1 |
| Q10 | Query a newly added typed war-planning sidecar | 1 |
| Q11 | Structured tool routing | 1 |
| Q12 | FTS5 discovery plus structured types | 20 |
| Q13 | Core semantic integrity checks | 2 checks, both zero |
| Q14 | Captured active playset members/load positions | 9 representative members |
| Q15 | Playset-specific winners and conflict context | 3 |
| Q16 | Scenario/metric/resource normalized model facts | 7 |
| Q17 | Open model/runtime issues and exact missing evidence | 2 |
| Q18 | Dataset schema drift across generator checkpoints | 2 |
| Q19 | Complete current building-model column catalog | 282 |
| Q20 | Selected-save progression and country-0 diagnostic facts | 35 |
| Q21 | Project artifacts, schemas, models, and tools covering a topic | 35 |
| Q22 | Project-aware semantic integrity checks | 4 checks, all zero |

## 15. Extension pattern for a newly introduced mechanic

A new mechanic always fits immediately as `knowledge_item` + `mechanic`, with claims, evidence, versions, relations, questions, checklists, tools, model subjects, and issues. Add a sidecar only when recurring structured attributes deserve named typed columns.

The examples create `ext_war_planning_mechanic_detail` after the core schema. It references the mechanic item, version span, declaration-gate summary, script-visible inputs, hidden-engine boundary, required runtime proof, optional basis claim, and change set. No core table changes are required. The same pattern supports future sidecars for Arkships, Waylines, Contracts, megastructure queues, ship-design doctrine, colony-role state, or another newly added system.

Rules for extensions:

- use a project/`ext_` prefix;
- use named typed columns rather than property/value rows or JSON blobs;
- reference stable items, version spans, claims/evidence, and change sets;
- add uniqueness/range/enumeration constraints;
- extend semantic sidecar-type checks; and
- leave unrelated core tables untouched.

## 16. Validation performed

The delivered schema and examples were executed in a fresh local SQLite database using Python `sqlite3` linked to SQLite 3.46.1.

- `PRAGMA foreign_keys` returned `1`.
- Journal mode returned `wal`.
- `PRAGMA application_id` returned `1397441074` (`0x534B4232`, SKB2).
- `PRAGMA user_version` returned `2`.
- Schema inventory: 96 STRICT core tables, 4 FTS5 tables, 12 views, 23 triggers, 83 explicit indexes.
- Demonstration inventory: 97 STRICT tables because the extension sidecar is added, plus the same 4 FTS5 tables.
- `PRAGMA foreign_key_check` returned zero rows.
- `PRAGMA integrity_check` returned `ok`.
- `PRAGMA quick_check` returned `ok`.
- Q13 returned two semantic checks with zero problems.
- Q22 returned four project-aware semantic checks with zero problems.
- All Q1–Q22 executed successfully; row counts are reported above.

The representative Stellaris facts are clearly scoped to the captured project snapshot, generated artifacts, and selected saves. They demonstrate data fit and query behavior; they are not a claim that every current Stellaris 4.4.5 engine behavior has been independently proved.

## 17. Day-one acceptance checklist

1. Confirm SQLite ≥3.37 and FTS5.
2. Execute the schema in a new file and verify application/user version.
3. Execute the examples and run Q1–Q22.
4. Confirm Q13/Q22 all zero, `foreign_key_check` empty, and integrity checks `ok`.
5. Replace representative local roots only with exact machine paths; keep stable root/artifact keys.
6. Refresh the current repository/playset/source-root snapshots before treating the seed as live truth.
7. Keep writes serialized and append/supersede accepted knowledge rather than editing history in place.

## References

[^sqlite-strict]: SQLite, “STRICT Tables,” https://www.sqlite.org/stricttables.html
[^sqlite-fk]: SQLite, “SQLite Foreign Key Support,” https://www.sqlite.org/foreignkeys.html
[^sqlite-wal]: SQLite, “Write-Ahead Logging,” https://www.sqlite.org/wal.html; “Temporary Files Used By SQLite,” https://www.sqlite.org/tempfiles.html
[^sqlite-cte]: SQLite, “The WITH Clause — Recursive Common Table Expressions,” https://www.sqlite.org/lang_with.html
[^sqlite-partial]: SQLite, “Partial Indexes,” https://www.sqlite.org/partialindex.html
[^sqlite-fts]: SQLite, “SQLite FTS5 Extension,” https://www.sqlite.org/fts5.html
[^sqlite-optimize]: SQLite, “ANALYZE — Recommended usage patterns,” https://www.sqlite.org/lang_analyze.html
[^sqlite-pragma]: SQLite, “PRAGMA Statements,” https://www.sqlite.org/pragma.html
