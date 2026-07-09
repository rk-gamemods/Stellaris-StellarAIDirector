# Stellar AI Director Defense/Crisis Economic Gate Pass

Date: 2026-07-09
Task: T23 - Defense/crisis economic gate pass
Target game version: Stellaris 4.4.5 stable
Scope: generated defense/economy gate refinement

## Goal

Refine static defense pressure so Starbase Extended and related defensive
starbase investments stay aggressive when risk is real, but do not activate from
broad fleet/conquest/high-scale pressure alone.

## Inputs

- T22 Starbase Extended surface study:
  `research/stellar-ai/stellar-ai-director-starbase-defense-v2-surface-study-2026-07-09.md`
- Current generated trigger file:
  `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- Current generated economic plan:
  `mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt`
- Current generated starbase modules/buildings:
  - `mods/StellarAIDirector/common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt`
  - `mods/StellarAIDirector/common/starbase_modules/zzzz_staid_05_starbase_defense_starbase_modules.txt`

## Implementation

The generator now emits a separate `staid_static_defense_threat_window` trigger.
`staid_static_defense_investment_ready` requires both:

- `staid_starbase_defense_economy_safe = yes`
- `staid_static_defense_threat_window = yes`

The economy gate now blocks catastrophic collapse and short-runway deficit
states. It also blocks recovery-mode spending unless there is a real emergency:
security existential pressure, crisis starbase pressure, or homeland attack.

The threat window allows:

- crisis starbase pressure;
- existential security pressure;
- homeland attack;
- defensive starbase strategy;
- aggressive/conquest pressure only when paired with an additional timing or
  risk signal: `highest_threat > 25`, year 80+, or high-scale snowball pressure.

The crisis starbase economic-plan reserve now also requires
`staid_starbase_defense_economy_safe = yes`, so crisis pressure cannot bypass the
deficit/recovery brakes.

## Compatibility Position

No new Starbase Extended objects were added. The pass stays on existing
Director-owned starbase module/building overrides and the additive economic
plan. It does not touch `common/ship_sizes`, `common/section_templates`,
`common/component_sets`, `common/component_templates`, GUI, or GFX.

## Validation

- `python tools\generate_stellar_ai_director_patch.py` passed.
- Focused test passed:
  `python -m unittest tools.tests.test_stellar_ai_director.GeneratedModValidityTests.test_starbase_route_weights_use_owner_country_scope`
- `python -m py_compile tools\stellar_ai_director_lib.py tools\tests\test_stellar_ai_director.py` passed.
- `python tools\validate_stellar_ai_director_patch.py` passed.
- `python -m unittest discover -s tools\tests` passed: 70 tests.
- `git diff --check` passed with only Git CRLF warnings.

## Remaining Risk

This is static validation only. It proves the generated gates parse and are
covered by tests, but it does not prove live AI starbase construction behavior,
Starbase Extended UI slots, or save/reload behavior. Those remain final
runtime/observer evidence work after all non-runtime packet slices are complete.

