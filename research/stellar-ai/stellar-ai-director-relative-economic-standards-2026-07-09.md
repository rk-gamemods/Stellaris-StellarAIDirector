# Stellar AI Director Relative Economic Standards

Generated 2026-07-09 for the 4.4.5-forward / 4.4.4-compatible Director build.

These are country-scope, piecewise relative standards. Colony bands scale civilian-resource headroom. Alloy safety must pass both the colony band and the current-fleet-power income band, so a large empire or fleet cannot qualify on an early-game flat floor. Stockpile targets are capped operating floats, not full replacement-cost warehouses. Ordinary food economies require positive monthly balance and a colony-scaled reserve; biological-ship empires additionally scale food income and operating reserves with fleet power.

| basis | resource | measure | lower inclusive | upper exclusive | target | consumer trigger | rationale |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| owned_colonies | energy | income |  | 6 | 25 | `staid_scaled_energy_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | income | 6 | 15 | 75 | `staid_scaled_energy_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | income | 15 | 30 | 150 | `staid_scaled_energy_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | income | 30 | 50 | 300 | `staid_scaled_energy_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | income | 50 |  | 600 | `staid_scaled_energy_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | stockpile |  | 6 | 1500 | `staid_scaled_energy_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | stockpile | 6 | 15 | 3000 | `staid_scaled_energy_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | stockpile | 15 | 30 | 6000 | `staid_scaled_energy_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | stockpile | 30 | 50 | 10000 | `staid_scaled_energy_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | energy | stockpile | 50 |  | 15000 | `staid_scaled_energy_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | income |  | 6 | 25 | `staid_scaled_minerals_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | income | 6 | 15 | 75 | `staid_scaled_minerals_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | income | 15 | 30 | 150 | `staid_scaled_minerals_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | income | 30 | 50 | 300 | `staid_scaled_minerals_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | income | 50 |  | 600 | `staid_scaled_minerals_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | stockpile |  | 6 | 1500 | `staid_scaled_minerals_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | stockpile | 6 | 15 | 3000 | `staid_scaled_minerals_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | stockpile | 15 | 30 | 6000 | `staid_scaled_minerals_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | stockpile | 30 | 50 | 10000 | `staid_scaled_minerals_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | minerals | stockpile | 50 |  | 15000 | `staid_scaled_minerals_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | income |  | 6 | 75 | `staid_scaled_alloys_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | income | 6 | 15 | 150 | `staid_scaled_alloys_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | income | 15 | 30 | 300 | `staid_scaled_alloys_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | income | 30 | 50 | 600 | `staid_scaled_alloys_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | income | 50 |  | 1200 | `staid_scaled_alloys_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | stockpile |  | 6 | 1500 | `staid_scaled_alloys_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | stockpile | 6 | 15 | 3000 | `staid_scaled_alloys_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | stockpile | 15 | 30 | 6000 | `staid_scaled_alloys_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | stockpile | 30 | 50 | 10000 | `staid_scaled_alloys_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | alloys | stockpile | 50 |  | 15000 | `staid_scaled_alloys_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | income |  | 6 | 10 | `staid_scaled_consumer_goods_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | income | 6 | 15 | 25 | `staid_scaled_consumer_goods_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | income | 15 | 30 | 60 | `staid_scaled_consumer_goods_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | income | 30 | 50 | 120 | `staid_scaled_consumer_goods_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | income | 50 |  | 250 | `staid_scaled_consumer_goods_income_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | stockpile |  | 6 | 1000 | `staid_scaled_consumer_goods_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | stockpile | 6 | 15 | 2000 | `staid_scaled_consumer_goods_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | stockpile | 15 | 30 | 4000 | `staid_scaled_consumer_goods_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | stockpile | 30 | 50 | 8000 | `staid_scaled_consumer_goods_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | consumer_goods | stockpile | 50 |  | 12000 | `staid_scaled_consumer_goods_stockpile_safe` | civilian economy scale and construction/upkeep headroom |
| owned_colonies | food | stockpile |  | 6 | 750 | `staid_scaled_food_stockpile_safe` | maintenance balance plus scaled reserve |
| owned_colonies | food | stockpile | 6 | 15 | 1500 | `staid_scaled_food_stockpile_safe` | maintenance balance plus scaled reserve |
| owned_colonies | food | stockpile | 15 | 30 | 3000 | `staid_scaled_food_stockpile_safe` | maintenance balance plus scaled reserve |
| owned_colonies | food | stockpile | 30 | 50 | 6000 | `staid_scaled_food_stockpile_safe` | maintenance balance plus scaled reserve |
| owned_colonies | food | stockpile | 50 |  | 12000 | `staid_scaled_food_stockpile_safe` | maintenance balance plus scaled reserve |
| current_fleet_power | alloys | income |  | 10000 | 75 | `staid_scaled_alloy_fleet_income_safe` | fleet replacement throughput |
| current_fleet_power | alloys | income | 10000 | 50000 | 150 | `staid_scaled_alloy_fleet_income_safe` | fleet replacement throughput |
| current_fleet_power | alloys | income | 50000 | 200000 | 300 | `staid_scaled_alloy_fleet_income_safe` | fleet replacement throughput |
| current_fleet_power | alloys | income | 200000 | 500000 | 600 | `staid_scaled_alloy_fleet_income_safe` | fleet replacement throughput |
| current_fleet_power | alloys | income | 500000 | 1000000 | 1200 | `staid_scaled_alloy_fleet_income_safe` | fleet replacement throughput |
| current_fleet_power | alloys | income | 1000000 |  | 2000 | `staid_scaled_alloy_fleet_income_safe` | fleet replacement throughput |
| current_fleet_power | alloys | stockpile |  | 10000 | 1500 | `staid_scaled_alloy_fleet_stockpile_safe` | capped military operating float; surplus remains investable |
| current_fleet_power | alloys | stockpile | 10000 | 50000 | 3000 | `staid_scaled_alloy_fleet_stockpile_safe` | capped military operating float; surplus remains investable |
| current_fleet_power | alloys | stockpile | 50000 | 200000 | 6000 | `staid_scaled_alloy_fleet_stockpile_safe` | capped military operating float; surplus remains investable |
| current_fleet_power | alloys | stockpile | 200000 | 500000 | 10000 | `staid_scaled_alloy_fleet_stockpile_safe` | capped military operating float; surplus remains investable |
| current_fleet_power | alloys | stockpile | 500000 | 1000000 | 15000 | `staid_scaled_alloy_fleet_stockpile_safe` | capped military operating float; surplus remains investable |
| current_fleet_power | alloys | stockpile | 1000000 |  | 20000 | `staid_scaled_alloy_fleet_stockpile_safe` | capped military operating float; surplus remains investable |
| bio_ship_fleet_power | food | income |  | 10000 | 25 | `staid_scaled_bioship_food_fleet_income_safe` | biological-ship replacement throughput |
| bio_ship_fleet_power | food | income | 10000 | 50000 | 75 | `staid_scaled_bioship_food_fleet_income_safe` | biological-ship replacement throughput |
| bio_ship_fleet_power | food | income | 50000 | 200000 | 150 | `staid_scaled_bioship_food_fleet_income_safe` | biological-ship replacement throughput |
| bio_ship_fleet_power | food | income | 200000 | 500000 | 300 | `staid_scaled_bioship_food_fleet_income_safe` | biological-ship replacement throughput |
| bio_ship_fleet_power | food | income | 500000 | 1000000 | 600 | `staid_scaled_bioship_food_fleet_income_safe` | biological-ship replacement throughput |
| bio_ship_fleet_power | food | income | 1000000 |  | 1000 | `staid_scaled_bioship_food_fleet_income_safe` | biological-ship replacement throughput |
| bio_ship_fleet_power | food | stockpile |  | 10000 | 1500 | `staid_scaled_bioship_food_fleet_stockpile_safe` | capped biological-fleet operating float; surplus remains investable |
| bio_ship_fleet_power | food | stockpile | 10000 | 50000 | 3000 | `staid_scaled_bioship_food_fleet_stockpile_safe` | capped biological-fleet operating float; surplus remains investable |
| bio_ship_fleet_power | food | stockpile | 50000 | 200000 | 6000 | `staid_scaled_bioship_food_fleet_stockpile_safe` | capped biological-fleet operating float; surplus remains investable |
| bio_ship_fleet_power | food | stockpile | 200000 | 500000 | 10000 | `staid_scaled_bioship_food_fleet_stockpile_safe` | capped biological-fleet operating float; surplus remains investable |
| bio_ship_fleet_power | food | stockpile | 500000 | 1000000 | 15000 | `staid_scaled_bioship_food_fleet_stockpile_safe` | capped biological-fleet operating float; surplus remains investable |
| bio_ship_fleet_power | food | stockpile | 1000000 |  | 20000 | `staid_scaled_bioship_food_fleet_stockpile_safe` | capped biological-fleet operating float; surplus remains investable |

## Interpretation

- The thresholds are net monthly income after upkeep, not gross production.
- Current fleet power deliberately lowers the military replacement-income band after catastrophic losses, while the colony band still requires a large empire to retain strong baseline throughput.
- Biological-ship empires use the colony alloy band for non-ship infrastructure but replace the alloy fleet burden with a food fleet burden.
- The largest alloy/biological-food military float is 20,000. Surplus above the operating float remains available to megastructures, fleet construction, and other high-return sinks; no normal state attempts to pre-fund an entire fleet replacement.
- A much larger reserve should only be introduced later behind explicit strategic evidence such as imminent total-war exposure or a known catastrophic battle, not as a default scale rule.
- These are safety gates for discretionary expansion, research scaling, fleet growth, and fortress investment; deficit-repair plans remain active below them.
- The economic plan generates 37 mutually exclusive colony/fleet repair bands. Each unsafe gate requires both earned monthly income and an operating float, so a market purchase can delay depletion but cannot make the economy count as repaired.
- Hard-shortage detection approximates two months of runway with deficit-magnitude bands because Stellaris exposes income and stockpile comparisons but not stockpile/income division.
- Core repair subplans request domestic resource income directly and contain no trade-income target. Director-owned market code has no buy path; its only market action is a positive-income, no-deficit overflow sale above the fixed reserve and 90% of the mods-included storage cap.
- Near-cap pressure also opens the source-proven Kugelblitz storage route when megastructure commitment is otherwise safe; storage expansion buys investment time but does not replace income repair.
- Runtime observation is still required to tune band boundaries against the active mod stack.
