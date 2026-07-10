# Stellar AI Director New-Galaxy Crash Scope Fix — 2026-07-09

## Incident

- Target runtime: Stellaris 4.4.4 with `supported_version="v4.4.*"` and 4.4.5-forward compatibility.
- Symptom: Stellaris crashed immediately after the new-galaxy generation button was pressed.
- Fresh crash folder: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\crashes\stellaris_20260709_214255`.
- The game log reached `Generating World! Specified Seed: 447184826` and then terminated with a native `C0000005` access violation.
- The crash-folder `error.log` and live `game.log` were inspected through `tools/summarize_stellaris_log.py`; the full 38 MB live log was not loaded directly.

## Evidence and regression boundary

The fresh log reported a new Stellar AI Director error:

```text
Wrong scope for trigger 'has_planet_flag' at common/colony_types/zzzzz_staid_16_research_buildout_plan.txt | Current Scope: colony | Supported Scopes: planet
```

The same semantic mistake also existed in the generated Gigas habitat district compatibility file:

```text
Wrong scope for trigger 'has_planet_flag' at common/districts/zzzz_staid_09_gigas_habitat_zone_slot_compat_districts.txt | Current Scope: colony | Supported Scopes: planet
```

The fresh crash summary was compared with the previous `stellaris_20260709_195643` crash summary. Both contained 127 fatal entries and the same 68 fatal signatures. The new research-colony wrong-scope error was new; the large pre-existing Gigas missing-zone-slot fatal set was unchanged. This makes the new colony-type scope regression the directly attributable change, while leaving third-party fatal background risk explicitly unresolved.

## Root cause

In Stellaris 4.4 colony-type and district object gates execute from `colony` scope. The generated research plan and copied habitat district blocks used bare planet-only flag operations. They needed an explicit scope transition:

```text
planet = { has_planet_flag = some_flag }
```

The generator now emits the explicit `planet` wrapper for the research-plan designation gates and rewrites copied Gigas habitat `has_planet_flag` checks into planet scope.

## Generic recurrence prevention

`generated_colony_root_scope_errors()` now recursively parses every generated `.txt` file under both:

- `common/colony_types`
- `common/districts`

It tracks common scope transitions and rejects `has_planet_flag`, `set_planet_flag`, or `remove_planet_flag` when reached from colony rather than planet scope. `validate_generated_patch()` always invokes this scanner.

The regression test `test_all_generated_colony_root_surfaces_scope_planet_flag_operations` verifies the real generated mod has no violations and uses synthetic bad colony-type and district fixtures to prove that all three operations and both generated surfaces are detected. This implements the project rule that every newly discovered runtime error pattern must become a generic whole-surface test, not a one-file assertion.

## Validation

- `python -m py_compile tools/stellar_ai_director_lib.py tools/tests/test_stellar_ai_director.py` — passed.
- `python tools/generate_stellar_ai_director_patch.py` — passed.
- Focused scope, research-plan, and Gigas habitat tests — 3 passed.
- `python -m unittest tools.tests.test_stellar_ai_director` — 89 passed.
- `python tools/validate_stellar_ai_director_patch.py` — passed.
- `git diff --check` — passed; only existing line-ending conversion warnings were emitted.
- `python tools/manage_stellaris_commands_at_date.py status` — harness absent, as required outside an approved observer run.

Runtime confirmation remains pending a user-launched 4.4.4 new-galaxy attempt. Stellaris was not launched automatically.
