# Stellar AI Director deficit, construction, fleet, influence, and boss regression fix

Date: 2026-07-09  
Target examined: Stellar AI Director on the active Stellaris PC 4.4 playset  
Installed vanilla baseline: Pegasus v4.4.4 (5505)  
Forward development target: Stellaris 4.4.5 with required 4.4.4 compatibility  
Validation type: static generation, parser, reference, and regression checks; no game launch or observer run

## Scope and naming

This pass concerns the local `Stellar AI Director` mod. It does not concern the
separate Workshop mod named `Stellar AI`, which is not installed in the active
playset. The active launcher descriptor points directly to this repository's
`mods/StellarAIDirector` directory.

The reported save state had an alloy deficit, a consumer-goods deficit, nearly
capped influence, excessive fleet strength, no current war, and naval-capacity
buildings competing for slots on research-designated worlds. The screenshot is
evidence for the resource state only; fleet dominance, diplomacy, and planetary
construction were reported observations and require a future runtime replay for
behavioral confirmation.

A later playtest screenshot supplied on 2026-07-09 adds a second exact regression
state: approximately 1.9K alloys at -31 per month, 414/1183 naval capacity, only
three colonies, and one of those colonies designated as a Fortress World with
multiple military-defense slots. The user also reported that this boxed-in empire
was much stronger than its neighbors but was neither acquiring claims/territory
nor using the fleet it continued to fund. This screenshot is retained as source
evidence at
`C:/Users/Admin/AppData/Local/Temp/codex-clipboard-03fec56f-4631-49f2-873f-6df3cddc4b91.png`.

## Root causes

1. `staid_militarist_conquest_strategy` and
   `staid_aggressive_fleet_pressure` treated almost every non-pacifist empire
   with unused naval capacity as a conquest/fleet-scaling candidate. That let an
   economic empire enter the 6,000-alloy and 6,000-naval-cap conquest plan
   without a military identity or immediate threat.
2. The economic valuation model summed 4.x job-workforce modifiers as if each
   unit were a complete job. Planetary Diversity's `building_navel_base` and
   `building_navel_command` were therefore modeled as creating 600 and 1,200
   jobs. The correct workforce conversion used by this project is 100 workforce
   units per job, producing modeled estimates of 6 and 12 before branch-aware
   interpretation.
3. Dataset-generated job pressure applied core-deficit and aggressive-fleet
   multipliers to every selected job building and district. Naval-capacity
   buildings consequently received emergency economic boosts even while their
   alloy support economy was collapsing.
4. Research construction could use high-scale escape clauses to bypass its
   consumer-goods and energy runway. Labs could be suppressed during the
   deficit while unrelated dataset-generated military buildings remained
   attractive.
5. The influence budget generator did not replace the vanilla `weight` block.
   Its intended Director weight existed only as unused generator metadata, so
   claims did not receive a boxed-in/high-influence pressure path.
6. Consumer-goods repair existed, but there was no matching explicit alloy
   runway repair subplan. Surplus and fleet routes also had insufficiently hard
   deficit exclusions.
7. The prior construction fix treated building `ai_weight` as authoritative.
   Local vanilla `common/buildings/00_example.txt` explicitly says building
   `ai_weight` is not used while economic plans are active. Research/pop/PD
   building-weight files therefore could not prove plan enforcement.
8. Boss targeting used vanilla's low generic boss-readiness thresholds for an
   active stack containing Gigas, More Events Mod, Guilli's, and Ancient
   Systems boss fleets. Rogue Eeloo and Legendary Guardian Forgos are explicitly
   spawned with `is_boss = yes`; Forgos also receives extreme health,
   regeneration, damage, and hostile-aura modifiers from the enabled Ancient
   Systems Difficulty MOD.
9. Vanilla `col_fortress` and `col_habitat_fortress` had no economic, colony-count,
   naval-use, or threat gate. Their own fortress-zone/building feedback increased
   designation weight, so a three-colony empire could sacrifice a third of its
   productive worlds while running an alloy deficit.
10. The vanilla `alloys_expenditure_ships` budget remained independently active
    even when Director economic-plan fleet pressure was disabled. No enabled mod
    other than the late-loading Director defines that object, so vanilla's always-on
    ship expenditure was the remaining live budget path capable of continued
    peacetime fleet funding.
11. Existing boxed-in claim pressure multiplied the general claim budget only to
    0.6 before the high-influence modifier. That helped but did not express the
    urgency of a non-pacifist empire with fewer than five colonies and no peaceful
    expansion route.
12. The generated conflict audit used a narrow historical object inventory and
    treated wrapper names such as `utility_component_template` as object IDs. It
    therefore misclassified the new fortress overrides as additive and produced
    hundreds of false component/behavior collisions when broader coverage was
    enabled.

## Implemented policy

- Normalize 4.x job-workforce quantities by 100 before calculating job counts,
  gross value, and return-on-investment scores. Raw modifier JSON remains in the
  evidence CSV for provenance.
- Classify naval, soldier, fortress, command, army, and related objects as the
  `military_capacity` family before any output-based research classification.
- Stop treating building `ai_weight` as the primary construction planner.
  Superseded research, pop-assembly, and broad Planetary Diversity building
  weight files are deleted by the generator before valuation/index rebuilds.
- Exclude every `military_capacity` object from dataset job-pressure output.
  Nonmilitary selected objects preserve parent construction scoring and expose
  verified economic output through `ai_resource_production`, which feeds the
  active economic-plan scoring path.
- Override only More Arcologies `building_navel_base` and
  `building_navel_command` with hard AI eligibility: strategic naval expansion
  must be ready, research-designated worlds are excluded, and existing AI naval
  buildings on research worlds receive a destroy trigger. Human and carrier
  behavior remains available through explicit bypasses.
- Require research construction to satisfy input-runway safety without a
  high-scale bypass.
- Add `staid_alloy_runway_safe` and a dedicated alloy-runway repair subplan.
  Basic-economy, fleet-buildup, fleet-payoff, conquest, and surplus routes now
  depend on deficit-safe runway conditions.
- Restrict conquest/aggressive fleet identities to actual militarist,
  xenophobe, despoiler, war, loss, or threat evidence instead of generic
  non-pacifism.
- Replace the actual claims `weight` in all three vanilla claim budgets. Add
  `staid_influence_claim_pressure` for a non-pacifist empire at peace with
  potential claims, more than 500 influence, and either no remaining expansion
  plan or more than 900 influence.
- Add a stronger `staid_boxed_in_claim_urgency` factor for non-pacifist empires
  below five colonies with potential claims, no active peaceful expansion plan,
  and more than 250 influence. This still funds the legal claim/CB prerequisite;
  it does not bypass vanilla target, war-goal, truce, or declaration checks.
- Override current-vanilla `alloys_expenditure_ships` and
  `alloys_expenditure_ship_upgrades` in the existing Director alloy-budget file.
  Normal new-fleet and upgrade spending now requires positive alloy income plus
  the civilian-economy runway gate. A separate defensive-emergency trigger keeps
  ship construction available during an actual war, recent lost war, or severe
  under-capacity threat.
- Override only `col_fortress`, `col_habitat_fortress`, the shared fortress-zone
  inline script, `building_stronghold`, and `building_fortress`. AI eligibility
  now requires no alloy deficit, positive alloy income, at least six colonies,
  at least 70% naval-capacity use, and a real war/loss/threat reason. Human access
  and the source carrier bypass are preserved.
- Require the AI fortress planet itself to sit in a system where vanilla's
  `is_bottleneck_system` trigger is true. The check uses the source-proven
  planet-to-system scope form `solar_system = { is_bottleneck_system = yes }`
  and applies to the designation, fortress zone, stronghold construction, and
  fortress upgrade. The unique Knights habitat designation may retain its role
  when an Order Keep or Order Castle exists, but ordinary fortress infrastructure
  still requires a bottleneck.
- Replace the shared flat resource-runway standards with country-scope relative
  bands recorded in
  `stellar-ai-director-relative-economic-standards-2026-07-09.csv`. Energy,
  minerals, consumer goods, alloys, and all major reserves scale with owned
  colony count. Alloy income and reserves must additionally pass a current-fleet-
  power band. At one million fleet power the income standard reaches +2,000
  monthly alloys, but the normal liquid operating float is capped at 20,000.
  This avoids warehousing full replacement cost and leaves surplus alloys free
  for megastructures, ships, and other investments. A larger reserve is deferred
  to a future explicit imminent-loss strategy rather than assumed by default.
  Food is treated differently: it needs positive net income, while
  only its reserve scales with empire size for ordinary empires. Biological-ship
  empires instead add fleet-power-scaled food income and reserve requirements,
  while retaining only the colony-scaled alloy requirement needed for non-ship
  infrastructure.
- Rebuild conflict ownership from the current active 116-mod playset, excluding
  the Director itself as a parent. Flat objects use their assignment IDs; wrapped
  component templates/sets use `key`, and ship behaviors use `name`. Generated
  SFT equivalence copies now carry explicit full-object ownership headers. The
  settled audit contains 497 intentional overrides, 369 additive Director
  objects, and zero unexpected parent collisions.
- Preserve `ENEMY_FLEET_POWER_MULT = 0.55` for aggressive ordinary wars.
  Separately raise `BOSS_MILITARY_POWER` to 100,000 and
  `ULTRA_BOSS_MILITARY_POWER` to 500,000.
- Register `staid_boss_safety.1` on `on_space_battle_lost`. If an AI loses to
  the confirmed Gigas `eeloofleet` or Ancient Systems
  `legendary_guardian_fleet`, the exact surviving target fleet is persistently
  reclassified as `is_ultra_boss = yes`, so subsequent attempts use the higher
  engine readiness tier rather than repeating the original plan.

The influence fix improves the vanilla prerequisite chain by funding claims;
it does not directly declare wars. Vanilla war planning, diplomatic legality,
casus belli, claims, truces, and target evaluation still decide whether a war
starts. This is intentional to avoid unsafe event-forced wars.

## Source and generated surfaces

Authoritative implementation source:

- `tools/stellar_ai_director_lib.py`
- `tools/tests/test_stellar_ai_director.py`

Regenerated mod surfaces:

- `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt`
- `common/ai_budget/zzzz_staid_08_site_limited_expansion_ai_budget.txt`
- `common/buildings/zzzz_staid_13_dataset_job_pressure_buildings.txt`
- `common/districts/zzzz_staid_13_dataset_job_pressure_districts.txt`
- `common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt`
- `common/colony_types/zzzzz_staid_15_fortress_economic_hard_gates.txt`
- `common/buildings/zzzzz_staid_15_fortress_economic_hard_gates.txt`
- `common/inline_scripts/zones/shared_fortress_zone.txt`
- `common/ai_budget/zzz_staid_alloys_budget.txt`
- `common/defines/zzzz_staid_14_high_scale_ai_defines.txt`
- `common/on_actions/zzzz_staid_boss_defeat_escalation_on_actions.txt`
- `events/zzzz_staid_boss_defeat_escalation_events.txt`

Regenerated evidence includes the economic-valuation, job-pressure override,
generated-reference, generated-file, and generated-conflict CSV/Markdown pairs
under `research/stellar-ai/`. This note is support/process evidence and has no
standalone rendered counterpart.

Relevant local vanilla source checked against the installed 4.4.4 build:

- `common/ai_budget/00_alloys_budget.txt`
- `common/ai_budget/00_influence_budget.txt`
- `common/colony_types/00_colony_types.txt`
- `common/buildings/09_army_buildings.txt`
- `common/zones/00_zones.txt`
- `common/inline_scripts/zones/shared_fortress_zone.txt`
- generated trigger/effect documentation for `has_potential_claims`,
  `has_ai_expansion_plan`, and resource comparisons

## Income-led repair and market boundary

The relative standards now drive 37 mutually exclusive repair subplans:

- five colony bands each for energy, minerals, consumer goods, alloys, and
  ordinary food operating-float recovery;
- six current-fleet-power bands for alloy replacement throughput;
- six current-fleet-power bands for biological-ship food replacement
  throughput.

Every runway combines earned monthly income with an operating float. A market
purchase may delay a shortage, but it cannot satisfy the income condition and
therefore cannot turn off production repair. Core repair subplans request the
deficient resource directly and contain no trade-income target.

The survival policy is state-based:

1. Healthy overflow goes first to high-value and then speculative investments.
   Diplomatic exchange is preferred when the engine can arrange an acceptable
   resource-for-resource offer.
2. A mild negative balance above two months of runway activates income repair
   and suppresses new upkeep in the short resource.
3. A hard shortage below approximately two months of runway may use vanilla
   market buying as a temporary bridge while income repair remains active.
4. A persistent deep deficit requires liability reduction. Fleet docking,
   fleet disbanding, building deactivation, megastructure disposal, territory
   release, enclave relief, subject/federation transfers, and irregular event
   income remain separate capability-audit items; none is assumed available
   until a real script or AI consumer is verified.

Because Stellaris does not expose stockpile divided by negative monthly income
as one trigger, the two-month boundary uses deficit-magnitude bands. A
-500/month balance crosses into short-runway state below 1,000 stockpile; a
-100/month balance crosses below 200.

The Director has no market-buy effect or scripted buy routine. Its monthly
market event only sells high-stockpile overflow when the resource has positive
monthly income, no deficit, its fixed minimum reserve, and at least 90% of its
actual mods-included storage cap. This cap-relative gate prevents production
from being discarded at 100% storage. Vanilla exposes NAI.AI_ALLOWED_TO_BUY as a
resource allow-list, but the actual buy decision is engine-side and has no
verified script trigger for a Director catastrophe-only condition. The
allow-list remains intact so vanilla emergency relief is not disabled; the
income gates prevent that relief from becoming the Director's definition of a
healthy economy.

The overflow-sale event previously referenced a scripted value owned by the
separate Stellar AI mod. That undeclared dependency was removed. The Director
now defines and calls its own staid_market_sell_value, using the vanilla
market_resource_price complex trigger.

The same 90%-of-cap pressure now makes the existing Kugelblitz storage route
eligible when the technology and safe megastructure-commit gates pass. The
active Gigas source gives 50,000 storage at stage 1, 150,000 at stage 2, and
500,000 at stage 3. Storage expansion buys time; it does not replace investment
or income repair.

## Static validation

The following checks passed after regeneration:

- `python -m unittest tools.tests.test_stellar_ai_director` — 85 tests passed.
- `python tools/validate_stellar_ai_director_patch.py` — passed.
- `python -m py_compile tools/stellar_ai_director_lib.py tools/generate_stellar_ai_director_patch.py tools/validate_stellar_ai_director_patch.py tools/tests/test_stellar_ai_director.py` — passed.
- Live observer-command harness status — absent and disabled.

CWTools could not be run because neither `cwtools` nor `cwtools-cli` is on
`PATH`, and `dotnet tool list -g` contains only `ilspycmd`. The project validator
and tests cover generated-file shape, trigger dependencies, references, and the
new strategic contracts, but are not a substitute for runtime AI observation.

## Remaining runtime questions

A user-approved observer or save replay should verify these outcomes in the
same strategic state:

1. Consumer-goods and alloy repair construction displaces naval-capacity
   construction during deficits.
2. Research-designated planets reject or remove More Arcologies naval-capacity
   buildings through the hard eligibility override.
3. Fleet scaling remains suppressed while the empire is already dominant and
   its basic economy is unsafe.
4. Boxed-in, non-pacifist empires with valid targets spend influence on claims
   and then pass through vanilla war planning instead of idling at the cap.
5. Research resumes and expands after the consumer-goods runway becomes safe.
6. Ordinary empire wars remain aggressive with the 0.55 multiplier while boss
   fleets wait for the dedicated readiness threshold.
7. An AI defeat by Rogue Eeloo or Forgos promotes that surviving fleet to the
   ultra-boss tier and prevents same-scale repeat attempts.
8. An AI with only three colonies, negative alloy income, and 35% naval-capacity
   use cannot select a fortress designation, fortress zone, new stronghold, or
   fortress upgrade, and its normal ship/upgrade alloy budgets are inactive.
9. A boxed-in non-pacifist empire below five colonies with potential claims and
   no peaceful expansion plan buys claims promptly; a later-gate failure should
   then be diagnosed at CB, war-goal, target, preparation, or declaration scope.
10. An otherwise eligible AI cannot select a normal fortress designation, build
    a fortress zone/stronghold, or upgrade a fortress outside a vanilla-computed
    bottleneck system.
11. A market purchase that restores stockpile but leaves monthly income below
    the relative standard does not clear the corresponding repair subplan.
12. Overflow sales occur only above their reserve with positive monthly income
    and no active deficit, and no Director market-buy action appears in logs.

The project builds toward 4.4.5, but the current active playset is intentionally
pinned to 4.4.4 because 4.4.5 breaks other enabled mods. Every current change
must therefore retain 4.4.4 load/runtime compatibility while avoiding design
choices that block the later 4.4.5 transition.
