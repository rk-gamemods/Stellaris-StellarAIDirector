# Stellar AI Director NSC3 Hull Readiness Pass

Date: 2026-07-09

Task card: T17 - NSC3 hull readiness support pass

## Scope

This pass improves NSC3 hull-route readiness through safe technology and
economic-plan pressure. It does not add direct ship-design, ship-size,
section-template, component-template, component-set, ship-behavior, or
component-slot output.

## Change

Added a generated economic-plan subplan:

`Stellar AI Director NSC3 hull readiness reserve`

The subplan activates when:

- `staid_research_input_runway_safe = yes`
- catastrophic collapse is not active
- one NSC3/fleet-throughput condition is present:
  `staid_nsc3_capital_hull_unlock_ready`, vanilla battleships, NSC3 carrier
  tech, NSC3 dreadnought tech, or year 80+ pressure

It adds supporting pressure for:

- `alloys = 900`
- `energy = 650`
- `minerals = 450`
- `engineering_research = 900`
- `physics_research = 450`
- `trade = 250`
- `naval_cap = 1200`

## Why This Is Safe

T15 showed that direct ship graph output remains blocked. This pass only
strengthens the supporting economy behind the existing NSC3 technology route.
It helps the AI afford and research capital hull paths while leaving final
ship-size, section, component, behavior, and design semantics to parent mods and
future dedicated validation.

## Validation

- `python tools/generate_stellar_ai_director_patch.py` passed.
- `python -m py_compile tools\stellar_ai_director_lib.py tools\generate_stellar_ai_director_patch.py tools\validate_stellar_ai_director_patch.py tools\tests\test_stellar_ai_director.py` passed.
- `python tools\validate_stellar_ai_director_patch.py` passed.
- Focused regression passed:
  `python -m unittest tools.tests.test_stellar_ai_director.GeneratedModValidityTests.test_phase_machine_and_modded_conversion_gates_are_generated`
- Full regression passed:
  `python -m unittest discover -s tools\tests` with 68 tests.
- Generated reference audit updated with the new economic-plan references and
  all new rows are `ok`.

## Remaining Runtime Proof

This static pass does not prove that the AI selects valid NSC3 designs,
sections, or ship designer templates in game. That remains runtime/smoke-test
work after non-runtime packet tasks are complete.
