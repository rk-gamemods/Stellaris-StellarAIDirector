# Stellar AI Director Hostile Fauna Reserve Pass

Date: 2026-07-09

Task card: T19 - Hostile fauna reserve tuning

## Scope

This pass refines the existing generated hostile fauna reserve so it follows
the T18 inventory boundary: small ordinary fauna, mining drones, and crystal
ship blockers are plausible reserve motivations; crystal stations, Distant
Stars guardians, reanimated leviathans, and broad leviathan event chains are
not safe generic targets.

## Change

Added a generated trigger:

`staid_hostile_fauna_safe_clearance_window`

The trigger requires:

- non-nomadic empire;
- no catastrophic collapse;
- no existential security state;
- safe basic stockpiles;
- `staid_fleet_buildup_economy_safe = yes`;
- `used_naval_capacity_percent < 1.20`;
- either the opening hostile-fauna route or an early alloy income floor of
  more than 60 alloys/month before year 60.

The existing `staid_hostile_fauna_clearance_strategy` now delegates to that
safe-clearance window. The existing generated economic subplan remains:

`Stellar AI Director hostile fauna clearance reserve`

It still reserves only modest support:

- `alloys = 220`
- `energy = 160`
- `minerals = 90`
- `naval_cap = 250`

## Why This Is Safe

The generated pass does not name map targets, fire events, create fleets,
declare wars, or force attacks. It is a conservative reserve/economy signal.
The new safe window tightens the old route from `used_naval_capacity_percent <
1.50` and 45 alloy/month fallback to `used_naval_capacity_percent < 1.20`, safe
stockpile and fleet-buildup gates, no existential security mode, and 60
alloy/month fallback.

The regression test explicitly bans the T18 unsafe identifiers and direct
event/fleet hooks from the safe-window, strategy, and reserve blocks.

## Validation

- `python tools/generate_stellar_ai_director_patch.py` passed.
- `python -m py_compile tools\stellar_ai_director_lib.py tools\generate_stellar_ai_director_patch.py tools\validate_stellar_ai_director_patch.py tools\tests\test_stellar_ai_director.py` passed.
- Focused regression passed:
  `python -m unittest tools.tests.test_stellar_ai_director.GeneratedModValidityTests.test_hostile_fauna_reserve_stays_on_safe_clearance_window`
- `python tools\validate_stellar_ai_director_patch.py` passed.
- Full regression passed:
  `python -m unittest discover -s tools\tests` with 69 tests.
- JDataMunch refreshed and validated the generated conflict, file-audit, and
  reference-audit CSV indexes. The generated reference audit now has 3,795 rows,
  all validated as indexed cleanly.
- JDocMunch indexed this note and the changed generated audit Markdown with
  `use_embeddings=false`.
- JCodeMunch indexed the changed generator and test files.

## Remaining Runtime Proof

This static pass does not prove that AI fleets choose the right map target or
avoid every possible guardian in live play. It only proves that Stellar AI
Director's generated surface remains a conservative reserve signal without
forbidden suicide-target identifiers or direct attack hooks. Runtime behavior
remains deferred to the approved observer phase after non-runtime work is
complete.
