# Stellar AI Director Tuning Notes

Generated thresholds are derived from decision-eligible, resolved ROI rows.

| knob | current value | intent |
| --- | ---: | --- |
| prep stockpile alloys | 15000 | minimum reserve before new megastructure prep |
| prep income alloys | 130 | minimum monthly alloy income for prep |
| commit stockpile alloys | 27000 | reserve for continuing safe projects |
| shipyard stockpile alloys | 12000 | reserve before shipyard payoff exploitation |
| shipyard income alloys | 150 | monthly alloy floor for fleet-production sink |
| fleet buildup stockpile energy | 8000 | energy runway before shipyard/fleet sink can add naval-cap pressure |
| trade capacity income floor | 25 | minimum monthly trade before generic expansion gates are considered safe |
| fleet trade capacity income floor | 75 | minimum monthly trade before fleet-throughput and payoff gates add logistics pressure |
| planetary trade capacity income floor | 50 | minimum monthly trade before planetary-capacity and megastructure-prep gates add logistics pressure |
| surplus trade capacity income floor | 100 | minimum monthly trade before surplus sink pressure can activate |
| fleet buildup naval cap ceiling | 1.05 | stop pushing fleet payoff when naval usage is already above target |
| static-defense stockpile alloys | 3000 | minimum reserve before country-level starbase defense economy target |
| static-defense income alloys | 60 | monthly alloy floor for defensive starbase reserve |
| crisis starbase threat | 50 | threat floor that can activate crisis starbase reserve |
| planetary-capacity stockpile minerals | 5000 | mineral runway before expanded planet/building capacity target activates |
| planetary-capacity stockpile energy | 5000 | energy runway before expanded planet/building capacity target activates |
| planetary-capacity pops target | 400000 | high-scale pop target used by the country-level tall-growth capacity subplan |
| market cap-breaker minerals reserve | 50000 | sell large positive-income mineral overflow before caps void income |
| market cap-breaker food/consumer goods reserve | 30000 | sell large positive-income food/CG overflow while preserving large buffers |
| market cap-breaker strategic reserve | 800-2500 | sell marketable strategic overflow only above high reserves |
| stranded fleet warning duration | 70 days | require a second monthly proof before forcing vanilla MIA return-home |
| threat response relation flag days | 7200 | duration for observer/aggressor and observer/victim threat state |
| threat response economy ratio cap | 20 | maximum share of fleet-throughput reserve available to third-party threat readiness |
| threat readiness alloys cap | 7 | maximum added alloys target from third-party threat readiness |
| threat readiness energy cap | 6 | maximum added energy target from third-party threat readiness |
| threat readiness naval cap | 40 | maximum added naval-cap target from third-party threat readiness |
| eligible ROI rows | 140 | source sample used for threshold generation |

## Static-Defense Policy

- Defensive or high-threat empires get additive starbase reserve subplans only after recovery and short-runway deficit gates are clear.
- Aggressive under-cap empires keep fleet expansion priority unless crisis pressure is high.
- The generated ESC starbase reactor override adds direct crisis-starbase AI weight support; other starbase modules/buildings remain manual-review candidates.

## Trade-Capacity Policy

- Trade is modeled as Stellaris 4.4 logistics/capacity headroom, not as a normal priced ROI resource.
- The generated `basic_economy_plan` includes trade reserve and trade recovery subplans so the Director's full-object replacement keeps trade logistics visible while pushing beyond vanilla/Stellar AI scale.
- Fleet, planetary, megastructure, static-defense, and surplus gates require trade income floors before adding more ship, colony, or resource-imbalance upkeep pressure.

## Market Cap-Breaker Policy

- Capped stockpile waste is treated as an economic emergency, not harmless savings.
- The monthly cap breaker sells only large positive-income overflow for marketable resources with verified market pricing or parent market-value support.
- Alloys, energy, unity, Gigas negative mass, and Gigas megaconstruction are excluded from forced sale because they are strategic reserves or not safely market-priced in source files.

## Fleet-Throughput Policy

- Mega Shipyard readiness becomes an economic-plan subplan only when alloy income, energy income, trade income, alloy stockpile, and energy stockpile are all safe.
- Fleet payoff exploitation is blocked while over-naval-cap upkeep spirals are likely (`used_naval_capacity_percent >= 1.05`).
- Research sink remains first when the Mega Shipyard unlock is missing because `staid_shipyard_expansion_ready` requires `tech_mega_shipyard`.

## Unlock-Research Policy

- The unlock-research policy is mandatory survival pressure after the opening curve, not a surplus-only luxury; it keeps physics, society, engineering, and unity pressure on until core Mega Engineering, Mega Shipyard, Gigas, NSC3, and ESC unlock paths are reachable.
- Direct technology/AP/tradition route overrides are emitted from copied source objects and trace back to the policy matrix and route override report.

## Mega/Giga Build Priority Policy

- ROI-ready megastructure and gigastructure rows are mapped through generated alloy, special-resource, and economy-plan gates.
- Generated full-object route overrides now cover Dyson Sphere, Mega Shipyard, neutronium gigaforge, Nidavellir forge, Matrioshka brain, planetcraft printer, war moon, and systemcraft starts; generated files preserve parent `@variable` parse context and remove absent optional `pc_magnetar` compatibility references.
- Exotic projects outside those route starts remain inventoried until the core loop is observer-tested against the high-scale crisis benchmark.

## Planetary-Capacity Policy

- Expanded planet/building capacity is covered through a country-level economic-plan subplan once mineral, energy, and trade logistics runway are safe.
- The generated subplan uses supported `pops` and income targets only; do not emit `empire_size`, which Stellaris 4.4.4 rejects in active economic-plan files.
- No generated building/job references are emitted in this slice; direct planet automation rewrites remain a required follow-up when a specific missing parent surface is proven.

## NSC3/ESC Design Policy

- NSC3 and ESC unlock technologies now have copied source-object route AI weights and are paired with fleet-throughput economy gates.
- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.

## Threat-Response Policy

- V1 reacts only to explicitly classified war goals: `wg_conquest`, `wg_subjugation`, and `wg_humiliation`.
- Unknown or unclassified war goals are inert: no punitive opinion, no shared-threat opinion, no alignment opinion, no readiness flag, no economy pressure, no CB, and no forced war.
- Design axes such as moral outrage and regional fear remain generator-owned; runtime files consume only generated values, triggers, flags, events, and opinion modifiers.
- Third-party defensive-readiness economy pressure is gated by `staid_tr_foreign_affairs_safe`, requires no survival/recovery/deficit/war state, and is capped at 20% of the existing fleet-throughput reserve.
- Directly attacked empires remain owned by vanilla/Stellar AI/Director war and survival behavior, not the third-party threat economy path.

## Stranded-Fleet Recovery Policy

- The Director does not attempt normal movement/pathfinding orders from script.
- Idle, out-of-combat, MIA-eligible AI fleets outside their owner's space are marked only while `staid_homeland_under_attack` is true.
- A marked fleet must still satisfy the same stranded gate on a later monthly pulse before `set_mia = mia_return_home` fires.
- The gate is intended for post-war access/pocket failures where a strong fleet is trapped away from a collapsing homeland, not for active offensive fleets.

## Safe Tuning Rules

- Do not lower prep or commit reserves below survival/recovery safety gates.
- Keep research sink before fleet sink until core modded unlocks are available.
- Treat unpriced resources and trade logistics as bottlenecks, not fake scalar value.
- Re-run generator, validator, unit tests, and coverage after every tuning change.
