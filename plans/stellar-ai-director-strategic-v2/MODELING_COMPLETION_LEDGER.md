# Stellar AI Director Modeling Completion Ledger

Last updated: 2026-07-09

This ledger tracks the full economic/building modeling layer required before
AI build-plan implementation should consume generated active-stack data. It is
the durable control surface for the modeling goal; update it whenever a gap is
closed, split, blocked, or newly discovered.

## Current Baseline

Target version: Stellaris PC 4.4.5 stable/current local install.

Branch: `codex/stellar-ai-director-strategic-v2`.

Primary generator: `tools/build_stellar_ai_research_capacity_dataset.py`.

Primary generated artifacts:

| Artifact | Current evidence | Status |
| --- | --- | --- |
| `research/stellar-ai/stellar-ai-director-research-capacity-jobs-2026-07-09.csv` | 501 active-stack winning jobs; 86 columns after resource promotion. | Generated baseline exists. |
| `research/stellar-ai/stellar-ai-director-research-capacity-buildings-2026-07-09.csv` | 826 building rows; 76 columns; JData join shows all 648 active-stack winning building IDs from `stellar_ai_director_object_atlas_20260706` are present. | Basic active winning building coverage met; enrichment incomplete. |
| `research/stellar-ai/stellar-ai-director-research-capacity-development-2026-07-09.csv` | 547 district/zone rows; 92 columns. | Generated baseline exists; enrichment incomplete. |
| `research/stellar-ai/stellar-ai-director-research-capacity-plan-2026-07-09.csv` | 24 research colony scenario rows; 104 columns. | Baseline exists; scenario model incomplete. |
| `research/stellar-ai/stellar-ai-director-colony-role-targets-2026-07-09.csv` | 220 colony role rows; 78 columns. | Baseline exists; missing several required role families. |
| `research/stellar-ai/stellar-ai-director-research-capacity-tech-modifiers-2026-07-09.csv` | 18 research-relevant technology rows. | Inventoried only; not applied as phased scenarios. |
| `research/stellar-ai/stellar-ai-director-strategic-infrastructure-targets-2026-07-09.csv` | 801 strategic infrastructure rows; 69 columns. | Baseline exists; benefit taxonomy incomplete. |
| `research/stellar-ai/stellar-ai-director-modeling-resource-coverage-2026-07-09.csv` | 20 resource coverage rows; all detected amount-resource keys are promoted. | Resource coverage requirement met for current generated model. |
| `research/stellar-ai/stellar-ai-director-research-capacity-2026-07-09.md` | Summary generated from the same script. | Baseline exists; should expand with every closed gap. |

Observed startup/tool state:

- Munch active-thread guide calls returned content for JDocMunch, JCodeMunch,
  and JDataMunch.
- `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1` passed with the
  expected transitional stdio duplicate-process warnings.
- JCodeMunch index refreshed for `local/StellarisMods-223b92bc` at current
  checkout.
- JDocMunch plan index refreshed and SHA-certified at
  `a787f66af3bd00cfcaaf3d28f6ba22fb8c43ace7`.
- JDocMunch research index refreshed; source is dirty because pre-existing
  observer-run files are modified.

## Gap Ledger

Statuses:

- `done`: current generated artifact satisfies the stated requirement and has
  validation evidence in this ledger.
- `in_progress`: actively being implemented in the current modeling pass.
- `partial`: a source-backed subset is implemented and validated, but the full
  requirement still has open work.
- `open`: required work remains and is locally actionable.
- `blocked`: source-backed blocker remains after repair attempts and requires
  user decision, external source, or runtime proof.
- `deferred_runtime`: static model can record the question, but proof requires
  explicitly approved runtime validation.

| ID | Requirement | Owner artifact/script | Current evidence | Status | Validation command or check | Blocker / next action |
| --- | --- | --- | --- | --- | --- | --- |
| M01 | Inventory and reconcile every active-stack winning building against object atlas/source roots. | `tools/build_stellar_ai_research_capacity_dataset.py`; buildings CSV; `stellar_ai_director_object_atlas_20260706` | JData join: 648 atlas winning buildings, 648 modeled, 0 missing. Buildings CSV has 826 rows including chain/context rows. | done | `JDataMunch run_sql` join between atlas and buildings datasets. Re-run after every generator refresh. | Keep as regression test or generated completion report row. |
| M02 | Record source mod/file, category, jobs, direct output/upkeep, job output/upkeep, upgrade chain, terminal status, unresolved variables, and quality flags for modeled buildings. | Buildings CSV | Current columns include `winning_mod_name`, `winning_file`, `category`, `jobs_created_json`, `direct_output_json`, `direct_upkeep_json`, `job_output_json`, `job_upkeep_json`, `upgrade_chain_to_terminal`, `upgrade_terminal`, `is_upgrade_terminal`, `unresolved_variables`, `data_quality_flags`. | done | `JDataMunch describe_dataset` for buildings CSV; generator run; schema test to add. | Add explicit schema test so this cannot regress. |
| M03 | Promote all resource outputs/upkeeps used by active buildings/districts/zones into normal numeric columns or classify unsupported with source-backed reason. | Generator `SUPPORT_KEYS`; `stellar-ai-director-modeling-resource-coverage-2026-07-09.csv`; buildings/development/infra CSVs | `giga_sr_negative_mass`, `giga_sr_amb_megaconstruction`, `giga_sr_iodizium`, `giga_sr_sentient_metal`, and `influence` are now in the modeled resource column set. The generated coverage CSV reports 20 amount-resource keys and all have `normal_column_status=promoted`. | done | Focused unit tests pass; generator output includes 20 resource coverage rows; JData `aggregate` on resource coverage returns only `promoted`; JData index/validate ok for all eight modeling CSVs. | Re-run coverage after later parser/scenario expansion. |
| M04 | Separate base, triggered, optimistic, conservative, and prerequisite-qualified benefits instead of silently mixing conditional benefits. | Jobs/buildings/development CSVs; new scenario columns/report | Job rows keep base/triggered/optimistic job resources, but building/development totals consume optimistic job resources and direct triggered resources are not separated into scenario columns. | open | Add tests for scenario column presence and known triggered rows. | Refactor resource aggregation to retain scenario-specific columns for buildings/districts/zones and plan rows. |
| M05 | Detect and value or classify pop growth/assembly benefits. | Strategic infrastructure CSV | Current strategic rows detect `pop_growth` and `pop_assembly` terms and score habitat growth centers. | partial | `JDataMunch validate_index`; targeted rows for clone vats/genomic facilities. | Add explicit benefit-class columns/status and formulas instead of tag-only scoring. |
| M06 | Detect and value or classify migration/resettlement source/destination. | Strategic infrastructure CSV | `transit_hub` is detected as `starbase_migration_support` with `resettlement_source_mult`; migration destination tags exist. | partial | JData known-row test for `transit_hub`; unit test to add. | Add conservative/optimistic/prerequisite-qualified valuation columns and build-plan readiness implication. |
| M07 | Detect and value or classify trade policy conversion. | New benefit taxonomy artifact | Current model tracks `trade` as a resource column but does not model trade-policy conversion. | open | Add static source inspection of trade policies and generated classification rows. | Parse trade conversion policies or classify as detected-only pending formula. |
| M08 | Detect and value or classify amenities, stability, housing, habitability, planet capacity, crime/deviancy, defense armies, bombardment resistance, naval cap, shipyard throughput, starbase support, envoys/diplomacy, research speed, empire/country modifiers, megastructure/construction benefits, blocker/district-capacity effects. | Strategic infrastructure CSV plus new benefit taxonomy artifact | Current term list covers a subset: growth, assembly, resettlement, migration, shipyard, naval cap, stability, amenities, envoys/diplomacy, research speed. It does not yet cover the full required taxonomy or produce explicit status/formula columns per class. | open | Add JData schema/aggregate checks by benefit class; add known-row tests. | Implement comprehensive benefit taxonomy detection and status columns. |
| M09 | Drive unknown jobs, unresolved variables, unparsed modifiers, and unsupported benefit classes to zero where feasible; source-backed blocker for any remainder. | Jobs/buildings/development/infra CSVs; completion report | Current buildings: 29 rows with unknown jobs, 36 with unresolved variables, 213 with quality flags. | open | JData aggregate on `unknown_jobs`, `unresolved_variables`, `data_quality_flags`; add threshold test for tracked blocker rows. | Resolve global variables/job aliases where possible; create blocker rows for remaining source-backed cases. |
| M10 | Cover colony role models: capital, research, forge, factory, generator, mining, agri, unity, refinery, trade, habitat growth/support, ring-world, arcology/ecumenopolis, frameworld, birch, and special Gigas world cases. | Role targets CSV; strategic infrastructure CSV | Current role target rows cover research/forge/factory/generator/mining/agri/unity/refinery/trade. Strategic infrastructure covers capital, habitat growth/support. Development rows classify habitat/ring_world/arcology/frameworld/birch/alderson/resort/generic. | open | JData aggregate by role and `colony_class`; generated report. | Add explicit role-family rows for capital, habitat_growth, habitat_support, ring_world, arcology, frameworld, birch, and special Gigas cases instead of only class-filtered development candidates. |
| M11 | Apply technology/prerequisite/capital-tier gates to building availability and build-plan readiness. | Atlas prerequisites columns; buildings/development CSVs; new readiness CSV | Buildings and development rows now carry `prerequisites`, `potential_allow_gates`, `event_flags`, and `unlock_flags` extracted with the same lightweight helper pattern as the object atlas. Tech modifiers are still inventoried but not applied to scenario readiness. | partial | Focused gate-column unit test passes; JData index/validate ok for buildings 826x76 and development 547x92. | Create readiness scenarios that consume prerequisites, capital tiers, and fallback-before-unlock candidates. |
| M12 | Answer whether colony automation/build plans can replace, demolish, or refactor buildings. | Strategic infrastructure CSV; vanilla/active source docs; new readiness note | Strategic infrastructure captures `can_demolish`, `can_build`, `can_be_disabled`, `destroy_trigger` for detected strategic objects only. | open | JDocMunch/JData source review; generated readiness note. | Inspect 4.4.5 colony automation/build-plan surfaces and add source-backed answer. |
| M13 | Model fallback buildings before unlocks. | New readiness CSV/report | Not currently modeled. | open | Generated fallback rows and tests for known lab/capital tier examples. | Use prerequisite/capital-tier data to pair pre-unlock fallback candidates with terminal targets. |
| M14 | Model blocker clearing and district-capacity effects. | New readiness CSV/report | Not currently modeled. | open | Source inspection and generated rows for blocker/district-capacity effects. | Parse blocker/decision/deposit effects or classify detected-only pending formula. |
| M15 | Identify which build-plan surfaces should consume the model. | Completion report; implementation note | Current model produces research/role/infra rows but no consumer contract for AI build-plan generation. | open | JDoc/JCode source review of economic plans, ai_resource_production, colony automation, build plans. | Write source-backed consumer contract for build-plan generator. |
| M16 | Add deterministic completion validation: schema, row counts, unresolved flags, required columns, and known rows. | `tools/tests/test_stellar_ai_director.py`; optional dedicated test file | Added focused tests for active-winning-building reconciliation, promoted Gigas resource columns/resource coverage, and source gate columns. | partial | Focused tests and full `python -m unittest discover -s tools\tests` pass. | Add tests for known `transit_hub`, role families, unresolved blocker accounting, and full schema/row-count contracts. |
| M17 | Regenerate from a clean command and index/validate every refreshed CSV with JDataMunch. | Generator outputs; JData datasets | Regenerated all research-capacity CSVs after custom resource, coverage-table, and source-gate changes; row counts stable, column growth expected, new coverage artifact added. | partial | `python tools\build_stellar_ai_research_capacity_dataset.py`; JData `index_local` and `validate_index` ok for jobs/buildings/development/plan/roles/tech/infra/resource-coverage datasets. | Repeat after each later artifact change; final pass must cover every new/refreshed CSV. |
| M18 | Keep generated modeling artifacts idempotent and avoid hand-maintained tables. | Generator and generated outputs | Current modeling artifacts are generated by script, including the new resource coverage CSV. Ledger is hand-maintained by design as the control plan, not model data. | in_progress | Generator and patch generator both run cleanly in this pass; run twice or compare clean diff after future generator changes when needed. | Any new CSV/report must be generated by script where possible. |
| M19 | Preserve static-only boundary unless runtime becomes the only remaining blocker. | Goal contract; validation plan | No runtime/observer testing approved for this modeling goal. | done | `python tools\manage_stellaris_commands_at_date.py status` before handoff/if observer harness touched. | Do not launch Stellaris or enable `commands_at_date.txt` without explicit approval. |
| M20 | Commit coherent modeling milestones as rollback points. | Git history | Current branch at `a787f66a`; pre-existing dirty observer-run files are unrelated and must not be staged with modeling commits. | in_progress | `git status --short --branch`; `git diff --check`; staged diff review before commit. | Stage only modeling/generator/test/ledger artifacts and commit this validated milestone. |

## Immediate Next Work Queue

1. Add explicit M02 schema tests for the existing source/category/job/output/
   upkeep/upgrade/quality columns so the broader building enrichment contract is
   guarded.
2. Add explicit benefit-class taxonomy/status columns, starting with the
   benefit classes already partially detected in strategic infrastructure rows.
3. Expand role-family rows for capital, habitat, ring-world, arcology,
   frameworld, birch, and special Gigas cases.
4. Create build-plan readiness scenarios that consume source gates, capital
   tiers, fallback-before-unlock candidates, and automation replacement limits.
5. Refresh all generated CSVs, JDataMunch indexes, validation, tests, and this
   ledger after each coherent pass.

## Validation Log

| Time/commit | Command or tool | Result | Notes |
| --- | --- | --- | --- |
| 2026-07-09 / `a787f66a` | Munch startup gate: exact guide discovery, guide calls, `assert-munch-mcp-startup.ps1` | pass | Duplicate stdio process warnings only; active guide calls returned content. |
| 2026-07-09 / `a787f66a` | JCodeMunch `index_folder` on repo | pass | `symbol_count=58432`, `file_count=747`; one expected skipped secret `.dds`. |
| 2026-07-09 / `a787f66a` | JDocMunch `index_local` and `verify_index` for plan docs | pass | Plan docs SHA-certified at current commit. |
| 2026-07-09 / `a787f66a` | JDocMunch `index_local` and sampled `verify_index` for `research/stellar-ai` | pass | Research index refreshed; source dirty due pre-existing observer-run file modifications. |
| 2026-07-09 / `a787f66a` | JDataMunch join: atlas winning buildings to buildings CSV | pass | 648 atlas winning buildings, 648 modeled, 0 missing. |
| 2026-07-09 / `a787f66a` | JDataMunch `search_data` for Gigas custom resources | gap found | Resources appear in JSON but not normal numeric columns. |
| 2026-07-09 / `a787f66a` | Focused unit tests for Gigas resource columns and building reconciliation before regeneration | expected fail then pass | Gigas column test failed before regeneration and passed after regenerating artifacts. |
| 2026-07-09 / `a787f66a` | `python tools\build_stellar_ai_research_capacity_dataset.py` | pass | Generated 501 jobs, 826 buildings, 547 districts/zones, 24 plan rows, 220 role rows, 18 tech modifier rows, 801 strategic infrastructure rows. |
| 2026-07-09 / `a787f66a` | JDataMunch `index_local` and `validate_index` for seven research-capacity CSV datasets | pass | Jobs 501x83, buildings 826x70, development 547x85, plan 24x100, roles 220x75, tech 18x9, infra 801x67. |
| 2026-07-09 / `a787f66a` | `python tools\build_stellar_ai_research_capacity_dataset.py` after resource-coverage addition | pass | Generated 501 jobs, 826 buildings, 547 districts/zones, 24 plan rows, 220 role rows, 18 tech modifier rows, 801 strategic infrastructure rows, 20 resource coverage rows. |
| 2026-07-09 / `a787f66a` | JDataMunch `index_local`, `validate_index`, and aggregate for eight modeling CSV datasets | pass | Jobs 501x86, buildings 826x72, development 547x88, plan 24x104, roles 220x78, tech 18x9, infra 801x69, resource coverage 20x8. Coverage aggregate: 20 promoted, 0 unsupported. |
| 2026-07-09 / `a787f66a` | Focused unit test for source gate columns; JDataMunch refresh/validate | expected fail then pass | Gate test failed before regeneration, passed after. Buildings now 826x76 and development 547x92 with prerequisites/gate columns; all eight dataset indexes validate. |
| 2026-07-09 / `a787f66a` | `python -m py_compile tools\build_stellar_ai_research_capacity_dataset.py tools\tests\test_stellar_ai_director.py` | pass | Syntax check passed after the resource coverage and source-gate edits. |
| 2026-07-09 / `a787f66a` | `python -m unittest discover -s tools\tests` | pass | Full tools test suite: 79 tests passed. |
| 2026-07-09 / `a787f66a` | `python tools\generate_stellar_ai_director_patch.py`; `python tools\validate_stellar_ai_director_patch.py` | pass | Generated patch surface remained clean in `git status`; validator reported `Stellar AI Director validation passed.` |
| 2026-07-09 / `a787f66a` | `python tools\manage_stellaris_commands_at_date.py status` | pass | Live dated observer command file absent; no observer harness active. |
| 2026-07-09 / `a787f66a` | `git diff --check` | pass | Exit 0. Git emitted existing LF/CRLF warnings for generated mod/research files, but no whitespace errors. |
| 2026-07-09 / `a787f66a` | JCodeMunch `index_folder` on repo after edits | pass | Existing local-identity index refreshed; `changed=2`, `symbol_count=58444`; one expected skipped secret `.dds`. |
| 2026-07-09 / `a787f66a` | JDocMunch `index_local` and sampled `verify_index` after edits | pass | Plan index added the modeling ledger; research index refreshed the generated summary. Sample verifies had no drift/missing/error sections. |
