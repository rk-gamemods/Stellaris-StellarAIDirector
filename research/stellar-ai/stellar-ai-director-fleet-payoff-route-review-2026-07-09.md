# Stellar AI Director Fleet Payoff Route Review

Date: 2026-07-09

Task card: T20 - Fleet payoff route review

## Scope

This pass audits militarist conquest, raiding-pop acquisition, and fleet
pressure routes against economic payoff. It does not change gameplay generator
output. The implementation change is a regression test that locks the current
payoff surfaces away from forced war effects.

## War Mechanics Evidence

JDataMunch validation passed for:

- `stellar_ai_war_mechanics_lever_catalog_20260708`
- `stellar_ai_war_mechanics_defines_catalog_20260708`

Relevant lever rows show:

- `aggressiveness` increases declaration attempts and offensive fleet
  commitment, but still requires a legal CB, war goal, and target.
- `military_spending` only helps if alloy, energy, naval-cap, and shipyard
  economy exist.
- `war_philosophy/unrestricted_wars` unlocks normal claim/subjugation access,
  but broad policy overwrites are high risk.
- `wg_conquest`, `cb_subjugation`, and `wg_subjugation` remain guarded by
  claims, relative power, independence, subject, and total-war/galactic-role
  constraints.

This means the Director should bias prerequisite economy, policy preference,
and route payoff surfaces, not force declarations or claims.

## Current Payoff Chain

Conquest payoff route:

- `staid_militarist_conquest_strategy` gates militarist/xenophobe/despoiler
  pressure and naval-cap use.
- `Stellar AI Director militarist conquest fleet reserve` reserves:
  `alloys = 6000`, `energy = 3500`, `minerals = 2500`, `unity = 1000`,
  `trade = 800`, `naval_cap = 6000`.
- Conquest route weights support `ap_lord_of_war`, Supremacy, aggressive fleet
  pressure, site-limited expansion, and fleet-buildup economy readiness.
- Policy weighting biases supremacist diplomacy and indiscriminate
  bombardment, but does not add claims, CBs, war goals, or declarations.

Raiding payoff route:

- `staid_raiding_pop_growth_strategy` requires a raiding-enabling perk, civic,
  or origin and avoids catastrophic collapse.
- `staid_raiding_pop_acquisition_priority` also catches the opening
  military-to-pops route before year 75.
- `Stellar AI Director raiding pop acquisition reserve` reserves:
  `alloys = 4500`, `energy = 3000`, `minerals = 1800`, `unity = 800`,
  `trade = 700`, `naval_cap = 4500`.
- `ap_nihilistic_acquisition` receives route weight when the raiding payoff is
  active.
- The raiding bombardment stance preserves `abduct_pops = yes` and adds owner
  AI weight for raiding, conquest, and opening military-to-pops routes.

Hostile-fauna route:

- Covered by T18/T19. It remains a small reserve/economy signal and is not a
  forced-war route.

## Test Added

Added:

`GeneratedModValidityTests.test_fleet_payoff_routes_bias_economy_without_forcing_wars`

The test checks that conquest and raiding payoff blocks include the expected
economy, naval-cap, policy, bombardment, and ascension-perk payoff markers. It
also bans forced-war hooks from the scoped route blocks:

- `declare_war`
- `set_war_goal`
- `create_war`
- `add_claim`
- `create_claim`
- `add_casus_belli`
- `country_event =`
- `fleet_event =`
- `create_fleet`

The first draft of the test intentionally used a wider generated-file scope and
failed because unrelated parent ascension perks contain inherited
`country_event` hooks. The final test scopes the assertion to conquest/raiding
route blocks only.

## Validation

- `python -m py_compile tools\tests\test_stellar_ai_director.py` passed.
- Focused regression passed:
  `python -m unittest tools.tests.test_stellar_ai_director.GeneratedModValidityTests.test_fleet_payoff_routes_bias_economy_without_forcing_wars`
- `python tools\validate_stellar_ai_director_patch.py` passed.
- Full regression passed:
  `python -m unittest discover -s tools\tests` with 70 tests.

## Decision

No gameplay generator tuning is needed in T20. The existing payoff chain is
coherent enough for static validation: it builds economy/naval capacity, raises
relevant perk/policy/bombardment weights, and avoids direct war/claim effects.

Runtime still needs to prove whether AI empires actually convert the pressure
into useful wars, raiding, and fleet payoff during the final observer phase.
