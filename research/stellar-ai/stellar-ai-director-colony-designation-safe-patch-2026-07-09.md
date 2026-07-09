# Stellar AI Director Colony/Designation Safe Patch

Date: 2026-07-09

Task: T25 - Colony/designation safe patch

## Scope

This slice applies only the source-proven Planetary Diversity - More Arcologies building support identified by the T24 review. It does not add a broad `common/colony_types` rewrite, does not patch zones or zone slots, and does not change vanilla colony automation designations.

## Implemented Patch

The dataset job-pressure generator now includes the active More Arcologies Workshop root when building its known object inventory. This lets the safety gate verify More Arcologies `common/pop_jobs` objects before copying high-ROI building definitions.

Generated building support added:

| Object | Source | Reason |
| --- | --- | --- |
| `building_navel_base` | `Planetary Diversity - More Arcologies::common/buildings/pd_arc_buildings.txt` | Adds 300 `pd_naval_admin` or `pd_naval_admin_gestalt` jobs, has tech and colony blockers, and had no parent `ai_weight`. |
| `building_navel_command` | `Planetary Diversity - More Arcologies::common/buildings/pd_arc_buildings.txt` | Upgrades the base to 600 naval-admin jobs, has upgraded-capital and `tech_global_defense_grid` gates, and had no parent `ai_weight`. |

The source spelling is `navel`, and the generated object IDs preserve it exactly.

## Deferred Targets

- `building_pd_rogue_council` remains excluded through an explicit dataset job-pressure forbidden-object guard. Its source `potential` includes a player-only construction path for AI unless the building already exists, so copying it into the generic ROI construction route would fight parent automation.
- More Arcologies zones such as `zone_pd_command_nexus`, `zone_pd_preserve`, and `zone_pd_trade_market` remain deferred because T24 found high zone conflict risk and no dedicated zone/zone-slot runtime proof.
- No `common/colony_types` or broad designation rewrite is emitted in this slice.

## Evidence

- `pd_arcology_jobs.txt` defines `pd_naval_admin` and `pd_naval_admin_gestalt`, resolving the job-reference blocker that had kept the buildings out of the generated job-pressure path.
- Refreshed `stellar_ai_director_dataset_job_pressure_overrides_20260707` contains 249 rows and includes only `building_navel_base` and `building_navel_command` from the T24 building candidate set.
- Refreshed `stellar_ai_director_generated_reference_audit_20260704` contains 3,818 rows, all with `status = ok`.
- Focused regression `GeneratedModValidityTests.test_dataset_job_pressure_overrides_use_live_valuation_rows` asserts the two naval buildings are selected, `building_pd_rogue_council` is excluded, and no zone objects enter the dataset job-pressure override set.

## Validation

- `python tools\generate_stellar_ai_director_patch.py` passed.
- `python -m unittest tools.tests.test_stellar_ai_director.GeneratedModValidityTests.test_dataset_job_pressure_overrides_use_live_valuation_rows` passed.
- `python -m py_compile tools\stellar_ai_director_lib.py tools\tests\test_stellar_ai_director.py` passed.
- `python tools\validate_stellar_ai_director_patch.py` passed.
- `python -m unittest discover -s tools\tests` passed 70 tests.
- `git diff --check` passed with line-ending warnings only.

## Remaining Risk

This is static construction-pressure proof. It proves parse/reference/load-order safety for the generated objects, but not that live AI planets will choose these buildings at the intended cadence. Runtime AI behavior remains deferred to the final observer proof phase.
