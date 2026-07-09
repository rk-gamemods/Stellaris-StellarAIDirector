# Generator Change Plan

## Scope

This plan is for Codex implementation after reviewing the two generated decision CSVs in this packet. It does not implement code here.

Current blocker queue coverage from `stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv`:

- `unresolved_variable` rows: 131
- `benefit_formula_status` rows: 265
- total current rows covered by this packet: 396

Packet decisions:

- unresolved-variable decisions: {'resolved_source_local_variable': 130, 'still_blocked_missing_evidence': 1}
- benefit-formula decisions: {'detected_only_non_scoring_policy': 260, 'numeric_formula_defined': 4, 'source_backed_zero_effect': 1}

## Exact recommended changes for `tools/build_stellar_ai_research_capacity_dataset.py`

1. Replace the current source-local variable lookup with a source-aware resolver keyed by the parsed winning source file, not only `Path(source_file)`. The generated rows carry relative source paths such as `common\buildings\14_branch_office_buildings.txt`; resolving `Path(source_file)` from the repo root misses the actual active-stack source file. Build a cache keyed by `(winning_mod_name, winning_file)` or by the absolute source path stored during `_winning_economic_definitions`, then merge those variables over `collect_global_variables` before calling `_collect_resource_amounts`, `_collect_job_adds`, `collect_numeric_modifier_assignments`, and `collect_numeric_assignments_matching`.

2. Add bracket-expression numeric evaluation for PDX arithmetic atoms such as `@[ advanced_cost * 2 ]`, `@[ advanced_upkeep * 2 ]`, `@[ upkeep_mult * 0.5 ]`, and `@[ research_upkeep * 0.5 ]`. The evaluator must support variables written inside bracket expressions without the leading `@` by trying both `name` and `@name` in the merged variable table. It should return an exact unresolved internal identifier, not the generic token `@[`, when an expression variable is missing.

3. Apply the source-local variable resolutions from `unresolved_variable_resolutions.csv`:
   - resolve vanilla branch-office `@crime_floor_from_legal_crime = 5`;
   - resolve vanilla and wilderness capital defense-army variables `@tier_2_capital_defense_armies = 4`, `@tier_3_capital_defense_armies = 8`, and `@tier_4_capital_defense_armies = 16`;
   - resolve vanilla habitat/ringworld/cosmogenesis upkeep variables in their owning files;
   - resolve Gigas frameworld variables such as `@base_upkeep = 1`, `@city_upkeep = 2`, `@advanced_upkeep = 5`, `@advanced_rare_upkeep = 1`, `@advanced_double_upkeep = 10`, `@advanced_double_rare_upkeep = 2`, `@mega_upkeep = 20`, and `@mega_alloy_upkeep = 5`;
   - resolve Gigas ringworld mega-housing variables including `@mega_housing_upkeep = 0.4`, `@ring_building_housing = 1500`, `@ring_building_housing_communal = 2000`, `@ring_building_amenities = 1500`, and `@ring_building_amenities_communal = 2500`;
   - resolve Gigas Elysium and Void Birch upkeep variables `@elysium_maintenance = 5` and `@void_birch_maintenance = 1000`.

4. Keep `district_giga_birch_physma_administration` blocked unless a readable active-stack assignment for `giga_birch_sector_jobs` is supplied. The uploaded `giga_birch_world.txt` has `job_bio_trophy_add = @[ giga_birch_sector_jobs * 5 ]` but no defining assignment. Do not infer this value from nearby districts.

5. Add a deterministic benefit-formula policy layer before `modeling_blocker_accounting_rows()` emits `benefit_formula_status` rows. Implement either a generated policy table matching `benefit_formula_policy_matrix.csv` or an equivalent in-code mapping:
   - `housing` for the four Gigas mega-housing buildings becomes `numeric_formula_defined` by parsing `planet_housing_add` with source-local variables and preserving `multiplier = value:giga_ring_world_building_size` as conditional scaling;
   - `planet_capacity` with `not_observed` becomes `source_backed_zero_effect` and remains an audit row only;
   - `amenities`, `blocker_district_capacity`, `bombardment_resistance`, `defense_armies`, `diplomacy_envoys`, `direct_resource_support`, `empire_country_modifier`, `shipyard_throughput`, `starbase_support`, and `trade_policy_value` become `detected_only_non_scoring_policy` when taxonomy evidence is `text_or_structural_signal` or `strategic_tag` and `benefit_amount` is zero.

6. Do not delete detected-only benefit evidence. Keep the taxonomy row, source terms, tags, and matched evidence, but prevent those rows from blocking unrelated numeric scoring and prevent them from receiving invented positive weights.

7. Update `consumer_policy_rows()` so objects blocked only by detected-only non-scoring benefit rows may return to their readiness-derived status (`scorable_now`, `gated_scorable_with_conditions`, `not_build_plan_candidate`, or role-target status). Objects with the remaining `giga_birch_sector_jobs` unresolved-variable row must remain `blocked_unresolved_modeling`.

## Exact recommended changes for `tools/stellar_ai_director_lib.py`

1. Extend `_numeric_atom()` or add a helper used by it to evaluate PDX bracket arithmetic expressions. Use a small whitelist parser rather than unrestricted `eval`: numeric literals, `+`, `-`, `*`, `/`, parentheses, and variable names are sufficient for the current rows.

2. Normalize expression-variable lookup so `advanced_upkeep`, `@advanced_upkeep`, `upkeep_mult`, and `@upkeep_mult` can all resolve to the same source-local variable table entry when used inside `@[ ... ]` expressions.

3. Return precise unresolved identifiers. For `@[ giga_birch_sector_jobs * 5 ]`, the unresolved token should be `giga_birch_sector_jobs` or `@giga_birch_sector_jobs`, not `@[`.

4. Keep `collect_variables()` comment-tolerant and numeric-sign tolerant. It already strips comments in the uploaded code path; preserve that behavior and support negative and exponent numeric forms so later source-local variables do not regress.

## Exact recommended test changes for `tools/tests/test_stellar_ai_director.py`

1. Add a test that generated blocker accounting has no generic `@[` unresolved-variable rows. The expected remaining expression blocker, if the missing Gigas value is still unavailable, must name `giga_birch_sector_jobs` and object `district_giga_birch_physma_administration`.

2. Add fixtures/assertions for specific resolved source-local variables:
   - `building_ai_emporium` or another branch-office row resolves `@crime_floor_from_legal_crime = 5`;
   - capital rows resolve defense-army variables 4/8/16;
   - habitat/ringworld rows resolve `@hab_maintenance`, `@low_hab_maintenance`, `@rw_maintenance`, and `@rw_maintenance_sr`;
   - Gigas frameworld rows resolve `@advanced_upkeep`, `@advanced_rare_upkeep`, `@advanced_double_upkeep`, and `@advanced_double_rare_upkeep`;
   - Gigas ringworld housing rows resolve the housing/amenities variables.

3. Add bracket-expression tests for:
   - `building_giga_matrioshka_brain_uplink_refinery`: `@[ upkeep_mult * 0.5 ] -> 0.125` and `@[ research_upkeep * 0.5 ] -> 0.5`;
   - `district_giga_frameworld_amenities_dystopian`: `@[ advanced_cost * 2 ] -> 2000` and `@[ advanced_upkeep * 2 ] -> 10`.

4. Add benefit-policy tests that verify:
   - `benefit_formula_status` rows are not emitted for detected-only non-scoring policy rows;
   - the four Gigas mega-housing rows receive a formula-preserved housing status, not a generic score;
   - the `planet_capacity` no-evidence row is zero-effect/audit-only;
   - detected-only rows do not alter numeric resource totals.

5. Add stable count tests with two branches:
   - without the missing Gigas `giga_birch_sector_jobs` source value, blocker accounting should fall from 396 to 1;
   - after that source value is supplied and parsed, blocker accounting should fall to 0.

## Expected blocker-count changes after implementation

- `benefit_formula_status`: 265 -> 0 using this policy matrix.
- `unresolved_variable`: 131 -> 1 from the uploaded context alone.
- Total blockers: 396 -> 1 from the uploaded context alone.
- Total blockers can become 0 only after Codex/user supplies the active-stack definition for `giga_birch_sector_jobs` or confirms it from a readable Gigas source file.

## Expected row-count or schema changes in generated CSV artifacts

- `stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv`: row count should become 1 from the uploaded context alone, or 0 after the missing Gigas variable is supplied.
- `stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv`: row count can remain 1887. Recommended additive columns are `modeling_decision`, `formula_or_policy`, and `policy_confidence`, or a generated companion policy table can be used instead.
- `stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv`: row count can remain 1093, but `blocked_unresolved_modeling` should drop substantially because detected-only non-scoring benefit rows no longer block consumption.
- `stellar-ai-director-research-capacity-buildings-2026-07-09.csv` and `stellar-ai-director-research-capacity-development-2026-07-09.csv`: row counts should remain 826 and 547; numeric values and `unresolved_variables` cells should change where variables and bracket expressions resolve.
- Readiness, role-target, jobs, resource-coverage, plan, and tech-modifier row counts are not expected to change from this correction alone.
