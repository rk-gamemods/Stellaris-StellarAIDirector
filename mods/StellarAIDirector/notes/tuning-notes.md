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
| planetary-capacity pops target | 250000 | pop target used by safe country-level capacity subplan |
| threat response relation flag days | 7200 | duration for observer/aggressor and observer/victim threat state |
| threat response economy ratio cap | 20 | maximum share of fleet-throughput reserve available to third-party threat readiness |
| threat readiness alloys cap | 7 | maximum added alloys target from third-party threat readiness |
| threat readiness energy cap | 6 | maximum added energy target from third-party threat readiness |
| threat readiness naval cap | 40 | maximum added naval-cap target from third-party threat readiness |
| eligible ROI rows | 140 | source sample used for threshold generation |

## Static-Defense Policy

- Defensive or high-threat empires get additive starbase reserve subplans only after recovery and short-runway deficit gates are clear.
- Aggressive under-cap empires keep fleet expansion priority unless crisis pressure is high.
- Direct starbase module/building weights remain deferred until each parent surface can be proven safe to override.

## Trade-Capacity Policy

- Trade is modeled as Stellaris 4.4 logistics/capacity headroom, not as a normal priced ROI resource.
- The generated `basic_economy_plan` includes trade reserve and trade recovery subplans so the Director's full-object override preserves vanilla trade-income pressure.
- Fleet, planetary, megastructure, static-defense, and surplus gates require trade income floors before adding more ship, colony, or resource-imbalance upkeep pressure.

## Fleet-Throughput Policy

- Mega Shipyard readiness becomes an economic-plan subplan only when alloy income, energy income, trade income, alloy stockpile, and energy stockpile are all safe.
- Fleet payoff exploitation is blocked while over-naval-cap upkeep spirals are likely (`used_naval_capacity_percent >= 1.05`).
- Research sink remains first when the Mega Shipyard unlock is missing because `staid_shipyard_expansion_ready` requires `tech_mega_shipyard`.

## Unlock-Research Policy

- Surplus empires use the unlock-research policy to keep pressure on physics, society, engineering, and unity until core Mega Engineering and Mega Shipyard gates are present.
- Direct technology/AP/tradition object overrides are deferred in v1; generated references are limited to validator-checked technology gates.

## Mega/Giga Build Priority Policy

- ROI-ready megastructure and gigastructure rows are mapped through generated alloy, special-resource, and economy-plan gates.
- Direct individual megastructure/gigastructure build-weight overrides are deferred unless a parent object surface is proven safe for the specific candidate.
- Exotic or path-specific projects remain deferred until the core loop is observer-tested.

## Planetary-Capacity Policy

- Expanded planet/building capacity is covered through a country-level economic-plan subplan once mineral, energy, and trade logistics runway are safe.
- The generated subplan uses supported `pops` and income targets only; do not emit `empire_size`, which Stellaris 4.4.4 rejects in active economic-plan files.
- No generated building/job references are emitted in v1; direct planet automation rewrites remain deferred until a specific missing parent surface is proven.

## NSC3/ESC Design Policy

- Direct NSC3/ESC ship and component design overrides are deferred until observer evidence proves parent AI cannot use the new hulls or components.
- Warning rows in the P11 integration audit are treated as parent-design gaps to observe, not automatic v1 override targets.

## Threat-Response Policy

- V1 reacts only to explicitly classified war goals: `wg_conquest`, `wg_subjugation`, and `wg_humiliation`.
- Unknown or unclassified war goals are inert: no punitive opinion, no shared-threat opinion, no alignment opinion, no readiness flag, no economy pressure, no CB, and no forced war.
- Design axes such as moral outrage and regional fear remain generator-owned; runtime files consume only generated values, triggers, flags, events, and opinion modifiers.
- Third-party defensive-readiness economy pressure is gated by `staid_tr_foreign_affairs_safe`, requires no survival/recovery/deficit/war state, and is capped at 20% of the existing fleet-throughput reserve.
- Directly attacked empires remain owned by vanilla/Stellar AI/Director war and survival behavior, not the third-party threat economy path.

## Safe Tuning Rules

- Do not lower prep or commit reserves below survival/recovery safety gates.
- Keep research sink before fleet sink until core modded unlocks are available.
- Treat unpriced resources and trade logistics as bottlenecks, not fake scalar value.
- Re-run generator, validator, unit tests, and coverage after every tuning change.
