# Stellar AI Director

Late-loading deterministic AI policy patch for the active Irony playset.

This mod is a deterministic standalone AI replacement baseline for the current
4.4 high-scale playset. It no longer declares or requires Stellar AI at launch.
Stellar AI remains a private parity reference for local development provenance:
the Director absorbs or reimplements the high-value AI budget, economic-plan,
research/economy/fleet conversion, construction-pressure, and war-support
surfaces needed for a viable single-AI baseline before deeper enhancements.

## Required Parents

- Gigastructural Engineering & More (4.4)
- NSC3
- Extra Ship Components NEXT
- Starbase Extended 3.0
- !!!Universal Resource Patch [2.4+]

Detected selected collection: `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`.

Missing required Steam parents during generation: none.

## Stellar AI Parity Reference

- Stellar AI source was used as private local parity evidence, not as a launch
  dependency.
- Reference present during generation: False.
- Reference load position during generation: None.
- Absorbed/reimplemented baseline surfaces: `common/ai_budget`,
  `common/economic_plans`, construction-pressure defines and budgets,
  research/economy/fleet conversion, market/runway safety, claim/war-support
  reserves, and high-scale modded progression hooks.
- Remaining standalone limits: direct diplomatic-action overrides, direct
  NSC3/ESC ship-design handling, executable-only target/reachability details,
  and runtime observer proof.

## Scope

- Adds scripted decision-state triggers for survival, recovery, megastructure
  prep, safe commit, surplus-sink pressure, and shipyard payoff exploitation.
- Overrides the regular `default` country type to remove Pegasus 4.4.4's
  pre-planner readiness deadlock: the 50% desired-navy requirement is omitted
  and the six-assault-army requirement is set to zero. Every other field is
  copied from the current vanilla object, and native target selection, casus
  belli, war goals, relative-strength checks, preparation, declarations, and
  fleet execution remain engine-owned. Regenerate and revalidate this
  full-object override after changing Stellaris versions.
- Copies the 20 ordinary/crisis personality objects from Pegasus 4.4.4 and
  substitutes only the working Stellar AI 0.10 `aggressiveness`, `bravery`, and
  `military_spending` values. Native behavior flags, diplomacy fields, design
  preferences, and selection rules remain intact.
- Gives diplomacy a bounded sub-40-year peaceful opening that exits immediately
  for war pressure or physical containment. Boxed-in empires strongly prefer
  Belligerent or Supremacist posture and retain claim pressure after five colonies.
- Replaces the native mineral army budgets with a modest uncapped reserve. The
  engine still chooses legal army types and counts; armies are not a declaration
  prerequisite and no unit is created by script.
- Applies a bounded Pegasus 4.4.4 high-naval-capacity workaround: the peacetime
  ship-budget share is reduced to 25% at 80% used capacity, but the category
  remains eligible so weak absolute fleets can still recover.
- Leaves the generic megastructure alloy budget upstream/parent-owned while
  retaining targeted Director route weights and Gigas special-resource support.
- Replaces the base economic plan with a mod-set-specific high-scale survival
  plan that forces research, alloy, trade, naval-cap, tall-scaling, and
  megastructure pressure on a mid-2300s crisis curve.
- Adds economic-plan targets for alloy reserves, Gigas special resources,
  and static-defense/starbase pressure when empires need to climb toward
  Gigas/NSC3/ESC-scale economy and fleet power.
- Adds trade-capacity recovery and reserve subplans so the Director preserves
  Stellaris 4.4 logistics/upkeep headroom instead of treating trade as a
  normal buy/sell commodity.
- Adds a monthly market cap-breaker for AI empires that are wasting large
  positive-income stockpiles, converting marketable overflow into trade
  currency instead of letting storage caps void the income.
- Removes the legacy two-pulse stranded-fleet event. Its intended post-war
  rescue gate also matched idle fleets in active enemy territory and could
  recall an offensive fleet during homeland pressure; movement and MIA recovery
  now remain native engine responsibilities.
- Adds a fleet-throughput economic subplan so Mega Shipyard unlocks and strong
  surplus can become fleet power without ignoring energy/alloy/trade runway checks.
- Adds planetary-capacity and safe research economic-plan demand while leaving
  vanilla designation/zone eligibility to select legal research infrastructure.
- Adds hard AI eligibility for More Arcologies `building_navel_base` and
  `building_navel_command`: naval expansion must be strategically ready and
  research-designated worlds are excluded. Inactive building `ai_weight`
  modifiers are not used as plan enforcement.
- Adds mandatory unlock-research pressure so AI empires keep pushing
  engineering/research/unity toward Mega Engineering, Mega Shipyard,
  planetcraft/systemcraft chains, NSC hulls, and ESC component tiers.
- Adds a bounded V1 threat-response layer for observed classified aggression:
  opinion modifiers, timed relation/country flags, and a third-party defensive
  readiness economy subplan capped at alloys 7, energy 6, and naval cap 40.
- Keeps unknown or unclassified war goals inert and does not declare wars,
  join wars, add punitive casus belli, or override diplomatic actions.
- Adds full-object route overrides for Mega Engineering, Mega Shipyard, Gigas
  planetcraft/systemcraft unlocks, NSC3 hull unlocks, ESC high-tier component
  unlocks, AP/tradition category/node pressure, economy megastructures, planetcraft, war moon,
  systemcraft, and ESC starbase reactor support.
- Adds threat/economy-gated starbase defense pressure for copied safe parent
  starbase modules and buildings while keeping Starbase Extended Waystation
  section and ship/component surfaces outside Director ownership.
- Records 4.4.4 Nomad/Arkship compatibility as a targeted opening-research
  lane plus normal-empire-only high-scale pressure; the Director does not own
  Nomad colony types, Arkship ship sizes, Arkship component templates,
  Waystation sections, Waylines, Contracts, or Operational Reserve objects.
- Leaves ESC internal component-template `key = ...` overrides and direct NSC3
  ship-design templates as manual-review blockers until the atlas models those
  loader surfaces safely.

## Load Order

Place Stellar AI Director after all required content parents and after parent
compatibility patches that the Director must supersede. Stellar AI is not a
required parent and should not be needed for the standalone baseline. In the
current selected collection, the latest required parent is at load position
72.
The Director may still be compared against Stellar AI for private parity review,
but the descriptor intentionally omits a Stellar AI dependency.

## Runtime Proof

The normal mod must not fire startup proof popups or auto-confirm third-party
setup menus. Live-launch proof is checked through the launcher descriptor,
`dlc_load.json`, static validation, and explicit user-approved smoke testing
outside normal gameplay flow.

## Surplus Sink Ordering

After survival and recovery gates, the Director treats strong alloy/energy
surplus, capped marketable resources, or under-curve research as signals that
the empire needs useful spending outlets. The v1 order is:

1. research sink;
2. fleet-production sink;
3. unity sink.

`source_has_ai_weight` in the ROI matrix only reports whether the parent mod
defined an upstream AI weight. The Director's own policy is expressed in the
separate `director_*` columns.

## Validation

Run:

```powershell
python tools/generate_stellar_ai_director_patch.py
python tools/validate_staid_444_war_solution.py
python tools/validate_stellar_ai_director_patch.py
python -m unittest discover -s tools/tests
```

Static validation proves generated file safety, known-reference coverage, and
deterministic policy contracts.
War-planning runtime proof remains one final fresh-game observer gate: run the
normal 4.4.4 playset for roughly 20–30 years with every regular empire under AI
control, then confirm multiple ordinary wars, a boxed-in breakout attempt, useful
but non-excessive offensive armies, and a functioning economy. Longer economic
and research benchmarking remains a separate Director quality goal.
