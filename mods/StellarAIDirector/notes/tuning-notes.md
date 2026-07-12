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
| 4.4.4 peacetime new-ship guard | 0.80 used naval capacity | avoid entering the executable high-capacity war-declaration defect; war/emergency bypasses |
| native army reserve | 200 minerals base; +300 boxed; +300 conquest/raiding; +500 war/existential | fund useful assault-army recruitment without forcing units or capping demand |
| war preparation window | 12–30 months | restore working native preparation rather than one-month declaration churn |
| strategic value horizon year | 2350 | long-lived economic, military, and modifier payoffs are weighted by remaining months before this goal date |
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
- Generated starbase pressure is guarded by `staid_static_defense_threat_window` and `staid_starbase_defense_economy_safe`.
- Copied safe Starbase Extended/ESC starbase module and building objects can receive Director defense pressure; Waystation sections, ship sizes, component templates, and other loader-sensitive defense surfaces remain outside Director ownership.

## Trade-Capacity Policy

- Trade is modeled as Stellaris 4.4 logistics/capacity headroom, not as a normal priced ROI resource.
- The generated `basic_economy_plan` includes trade reserve and trade recovery subplans so the Director's full-object replacement keeps trade logistics visible while pushing beyond vanilla/Stellar AI scale.
- Fleet, planetary, megastructure, static-defense, and surplus gates require trade income floors before adding more ship, colony, or resource-imbalance upkeep pressure.
- Advanced component and modded fleet conversion routes require core support runway, fleet-level trade capacity, and strategic-resource income before their strategic-resource pressure can fire.

## Market Cap-Breaker Policy

- Capped stockpile waste is treated as an economic emergency, not harmless savings.
- The monthly cap breaker sells only large positive-income overflow for marketable resources with verified market pricing or parent market-value support.
- Alloys, energy, unity, Gigas negative mass, and Gigas megaconstruction are excluded from forced sale because they are strategic reserves or not safely market-priced in source files.

## Fleet-Throughput Policy

- Mega Shipyard readiness becomes an economic-plan subplan only when alloy income, energy income, trade income, alloy stockpile, and energy stockpile are all safe.
- Fleet payoff exploitation is blocked while over-naval-cap upkeep spirals are likely (`used_naval_capacity_percent >= 1.05`).
- Research sink remains first when the Mega Shipyard unlock is missing because `staid_shipyard_expansion_ready` requires `tech_mega_shipyard`.
- Militarist conquest, raiding-pop acquisition, and early hostile-fauna clearance now have separate fleet reserve lanes; military empires are not forced to wait for peaceful surplus-only fleet spending.
- War declaration globals return to the working native 4.4.4 envelope: 12–30 months preparation, base aggression 25, enemy-fleet multiplier 1.2, maximum distance 50, minimum score 0.5, and offense/defense allotment 1.0. Boxed-in multipliers remain bounded above vanilla at 8/12.
- Normal peacetime new-ship spending pauses at 80% used naval capacity, while upgrades, war, crisis, and defensive-emergency spending bypass the guard. This is the native-data workaround for the executable high-cap declaration defect later fixed in 4.4.5.
- Native army budgets reserve 200 minerals at baseline, with bounded additions for boxed-in, conquest/raiding, war, and existential-defense states. No desired_max caps recruitment and no army is created by script.
- Raiding empires prioritize `ap_nihilistic_acquisition`, raiding bombardment, and no-surrender bombardment posture when their setup supports abducting pops as a growth strategy.
- Hostile space fauna continues to use the engine's separate boss readiness lane at 100000/500000 military power. Ordinary empire confidence uses the native `ENEMY_FLEET_POWER_MULT = 1.2`; boss readiness is not made easier by the war-planner repair.

## Unlock-Research Policy

- The unlock-research policy is mandatory survival pressure after the opening curve, not a surplus-only luxury; it keeps physics, society, engineering, and unity pressure on until core Mega Engineering, Mega Shipyard, Gigas, NSC3, and ESC unlock paths are reachable.
- Direct technology/AP/tradition category/node route overrides are emitted from copied source objects and trace back to the policy matrix and route override report.

## Mega/Giga Build Priority Policy

- ROI-ready megastructure and gigastructure rows are mapped through generated alloy, special-resource, and economy-plan gates.
- Generated full-object route overrides now cover Dyson Sphere, Mega Shipyard, neutronium gigaforge, Nidavellir forge, Matrioshka brain, planetcraft printer, war moon, and systemcraft starts; generated files preserve parent `@variable` parse context and remove absent optional `pc_magnetar` compatibility references.
- The Gigas habitat start preserves parent base/site scoring, the 30-year queued-build cooldown, the starport veto, and the AI habitat cap. An active native colonization plan applies a nonzero `0.1` backlog penalty instead of any empty habitat hard-zeroing all future starts; crowded-tall readiness adds only a bounded factor `2`.
- Exotic projects outside those route starts remain inventoried until the core loop is observer-tested against the high-scale crisis benchmark.

## Planetary-Capacity Policy

- Expanded planet/building capacity is covered through a country-level economic-plan subplan once mineral, energy, and trade logistics runway are safe.
- The generated subplan uses supported `pops` and income targets only; do not emit `empire_size`, which the current Stellaris 4.4.4 economic-plan surface rejects.
- Safe research economic-plan demand is gated by `staid_research_construction_priority_ready`; vanilla research-zone eligibility remains the hard building boundary. The Director no longer emits research or pop-assembly building `ai_weight` files as if they were an authoritative planner.
- Planetary Diversity outpost decisions are copied into generated decision overrides with Director-owned weights for moon, mining, food, energy, and research outposts; the research family strongly favors the capital because the opening strategy treats the capital as the first research hub.
- Planetary Diversity decision availability owns tech, site, and button prerequisites. Director weights do not duplicate those checks; if the button is available and the mineral/energy runway is safe, the AI is pushed to use the matching outpost.
- Permanent and long-lived scaling investments use a 2350 horizon: the same outpost, building, tech, megastructure, or buff is worth far more in 2220 than in 2320 because every remaining year multiplies its payoff.
- Unity-to-research pressure targets source-backed Discovery, Diplomacy, Technological Ascendancy, Master Builders, Galactic Wonders, and Gigastructural Constructs paths instead of hoarding unity generically.
- Research diplomacy pressure stays on the safe lane: copied Research Cooperative federation weighting and Discovery/Diplomacy/AP support remain, while the cooperative stance is restricted to the temporary diplomatic opening and exits for native war pressure. Direct research-agreement actions remain gated.
- Planetary Diversity outpost decisions retain source-owned availability and Director decision weights; obsolete generated PD building-weight and role-trigger files are removed.
- More Arcologies support is intentionally narrow: `building_navel_base` and `building_navel_command` use hard AI strategic-readiness and research-world exclusion gates, while `building_pd_rogue_council`, More Arcologies zones, and broad colony/designation rewrites remain blocked.
- Arkship carrier planets are excluded from copied Planetary Diversity outpost decisions, and later high-scale planetary pressure remains normal-empire-only where the Nomad/Arkship audit found no safe shared surface.

## Nomad/Arkship Compatibility Policy

- Nomadic empires get only the targeted opening research route `staid_opening_nomad_arkship_research` until a dedicated Nomad strategy is proven.
- Most megastructure, colony, starbase, war, fleet, fauna, and planetary-capacity pressure is guarded for normal empires with `is_nomadic = no`.
- The Director does not override Nomad colony types, Arkship ship sizes, Arkship component templates, Waystation sections, Waylines, Contracts, or Operational Reserve objects; those remain owned by vanilla and parent mods.

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

- The Director does not issue movement, stance, MIA, or pathfinding orders from script.
- The removed two-pulse handler was intended for post-war access pockets, but its foreign-space predicate also selected current enemy territory.
- Native pathfinding, border access, and MIA behavior now own both active-war travel and post-war recovery.

## Safe Tuning Rules

- Do not lower prep or commit reserves below survival/recovery safety gates.
- Keep research sink before fleet sink until core modded unlocks are available.
- Treat unpriced resources and trade logistics as bottlenecks, not fake scalar value.
- Re-run generator, validator, unit tests, and coverage after every tuning change.
