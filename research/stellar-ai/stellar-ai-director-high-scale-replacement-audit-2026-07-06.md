# Stellar AI Director High-Scale Replacement Audit

Date: 2026-07-06
Target game/mod context when written: Stellaris 4.4.4 stable with Gigastructural Engineering & More (4.4), NSC3, Extra Ship Components NEXT, Starbase Extended 3.0, Universal Resource Patch, and Stellar AI loaded before the local Director patch. Current target as of 2026-07-08 is Stellaris 4.4.5 stable/current local install; revalidate this audit's implementation assumptions against 4.4.5 before further use.

## User-Observed Failure

In a crowded observer game, the largest AI empire reached only about 20,000 fleet power by the mid-2300s while the Katzenartig crisis arrived around 2,000,000 fleet power. The user observed no meaningful AI megastructure construction and described the current behavior as unable to exploit the high-scale mod set.

The design correction is explicit: Stellar AI Director is not a fallback compatibility shim and should not preserve Stellar AI as the strategic baseline after the opening curve. Stellar AI can be treated as an early-game reference, but the Director must replace the economic and strategic assumptions so AI empires push toward Gigastructural Engineering, NSC3, ESC NEXT, megastructures, habitats/tall scaling, conquest scaling, planetcraft/systemcraft, and millions-scale fleet readiness.

## Local Source Evidence

- Vanilla 4.4 economic plans and ship-size files model `trade` as a real resource and logistics/upkeep bottleneck, not as a market-priced resource that can be bought or sold away.
- Gigastructural Engineering indexed evidence shows `planetcraft_printer_0` requiring `giga_tech_planet_assembly`; systemcraft construction requires `giga_tech_war_system_1`, `giga_tech_war_system_2`, `giga_tech_war_system_3`, `ap_celestial_printing`, and large behemoth ship counts.
- NSC3 indexed evidence shows Mega Shipyard and Headquarters megastructure surfaces tied to `tech_mega_shipyard`, `tech_mega_engineering`, and `tech_starbase_6`.
- ESC NEXT indexed evidence shows high-tier component chains such as `esc_tech_dark_matter_power_core_2` and `esc_tech_strikecraft_5`, with rare high-tier prerequisites.

## Replacement Slice Implemented

This slice converts the generated `basic_economy_plan` override from conservative late-game support into high-scale survival pressure:

- base economic plan weight increased to make the Director-owned replacement dominant;
- research income targets escalate through early rush, midgame megastructure rush, crisis-scale giga rush, and planetcraft survival curve stages;
- Mega Engineering and modded unlock research pressure becomes mandatory after the opening curve, not only a surplus behavior;
- fleet-throughput targets now push `alloys = 500`, `trade = 150`, and `naval_cap = 800` when shipyard payoff gates are safe;
- planetary/tall scaling targets now push `pops = 400000`, stronger mineral/energy runway, and late planetcraft-scale research and trade pressure;
- megastructure alloy reserve budgets now hold much larger stockpiles and continue scaling after year 119 instead of stopping near vanilla/Stellar AI reserve sizes.

## Remaining Required Replacement Surfaces

This is not yet the full high-scale AI. The next slices should copy parent objects with source context and add direct policy for:

- Gigastructure build weights and construction priorities, especially Dyson/Nidavellir/Matrioshka/economy multipliers, planetcraft, and systemcraft chains;
- ascension perk, tradition, and technology weights for `tech_mega_engineering`, `tech_mega_shipyard`, Gigas planetcraft/systemcraft unlocks, NSC3 capital hull/infrastructure unlocks, and ESC high-tier component chains;
- habitat/tall-development policy for crowded galaxies where expansion is blocked;
- conquest escalation policy for empires that cannot scale tall fast enough;
- ship design, starbase, and component selection once NSC3/ESC parent AI usage is proven insufficient;
- observer-run benchmarks against the Katzenartig crisis curve, with target milestones before 2300, 2350, and 2400.

## Validation Expectation

Do not treat this slice as final proof that the AI can defeat the crisis. It is the first hard replacement of the economy and reserve posture. A fresh observer game must verify that AI empires actually unlock and build modded megastructures, advance through Gigas/NSC3/ESC tech chains, and reach fleet/economy scale near the crisis benchmark.
