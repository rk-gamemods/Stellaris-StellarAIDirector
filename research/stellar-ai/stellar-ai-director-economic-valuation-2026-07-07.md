# Stellar AI Director Economic Valuation Dataset

Generated: 2026-07-09T19:30:15.339751+00:00

This dataset is the required evidence gate before generating new late-game unemployment or construction-pressure weights. It mines the active Irony stack plus vanilla for planet `buildings`, `zones`, and `districts`, records the top-level load winner, and computes rough long-horizon ROI against the 2350 target end date.

Important limitations:

- ROI is a rough planning number, not a game simulation.
- Explicit `ai_resource_production` and direct production are valued directly.
- Job-only objects use `6.0` value per job per month because final job output depends on empire, species, designation, buildings, and modifiers.
- Modifier-only objects use a conservative key-count proxy and are flagged for review.
- Inline scripts and unresolved variables are flagged so later weight generation can prefer high-confidence rows or require manual review.

Active collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity
Active mod count: 116

## Row Counts

- building: 826
- district: 286
- zone: 261

## Data Quality Flags

- ai_weight_absent: 1163
- ai_weight_zero_or_gated_zero: 34
- has_ai_or_direct_output: 214
- has_build_cost: 616
- has_jobs: 348
- has_upkeep: 758
- none: 1
- overridden_in_stack: 201
- uses_inline_script: 1037

## Highest Rough ROI At 2250 Horizon

- district `district_maginot_ringworld_barracks` from Gigastructural Engineering & More (4.4): ROI@2250=110169680.0, jobs=15300.0, flags=ai_weight_zero_or_gated_zero|has_build_cost|has_jobs|has_upkeep
- building `building_fe_dome` from Stellaris vanilla: ROI@2250=89970900.0, jobs=12500.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- district `district_rw_science` from Stellaris vanilla: ROI@2250=86413550.0, jobs=12000.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- building `building_giga_gas_giant_habitation_module` from Gigastructural Engineering & More (4.4): ROI@2250=45387900.0, jobs=6300.0, flags=ai_weight_zero_or_gated_zero|has_jobs|has_upkeep|uses_inline_script
- building `building_fe_sky_dome` from Stellaris vanilla: ROI@2250=44994000.0, jobs=6250.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- building `building_giga_aeternum_synthetizer` from Gigastructural Engineering & More (4.4): ROI@2250=44229600.0, jobs=6000.0, flags=ai_weight_zero_or_gated_zero|has_ai_or_direct_output|has_jobs|uses_inline_script
- building `gpm_building_ascension_tower` from Guilli's Planet Modifiers and Features: ROI@2250=43213980.0, jobs=6000.0, flags=ai_weight_zero_or_gated_zero|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep
- building `building_giga_matrioshka_brain_uplink_sanctuary` from Gigastructural Engineering & More (4.4): ROI@2250=36007200.0, jobs=5000.0, flags=ai_weight_absent|has_jobs|uses_inline_script
- district `district_rw_farming` from Stellaris vanilla: ROI@2250=32402750.0, jobs=4500.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- district `district_rw_generator` from Stellaris vanilla: ROI@2250=32402750.0, jobs=4500.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- building `building_giga_matrioshka_brain_uplink_entertainment` from Gigastructural Engineering & More (4.4): ROI@2250=26676000.0, jobs=3700.0, flags=ai_weight_absent|has_jobs|uses_inline_script
- district `district_mindlink` from Stellaris vanilla: ROI@2250=22062075.0, jobs=3000.0, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
- building `building_organic_paradise` from Stellaris vanilla: ROI@2250=21693100.0, jobs=3000.0, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
- district `district_maginot_ringworld_bunkers` from Gigastructural Engineering & More (4.4): ROI@2250=21604700.0, jobs=3000.0, flags=has_build_cost|has_jobs|has_upkeep|uses_inline_script
- district `district_rw_commercial` from Stellaris vanilla: ROI@2250=18722750.0, jobs=2600.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- building `building_gaia_unity_servitor` from Stellar AI Director: ROI@2250=18004520.0, jobs=2500.0, flags=has_build_cost|has_jobs|has_upkeep|overridden_in_stack
- building `building_imperial_machine_capital` from Stellaris vanilla: ROI@2250=15865800.0, jobs=2200.0, flags=ai_weight_absent|has_jobs|has_upkeep|uses_inline_script
- building `building_giga_matrioshka_brain_uplink_hell` from Gigastructural Engineering & More (4.4): ROI@2250=14403600.0, jobs=2000.0, flags=ai_weight_absent|has_jobs|uses_inline_script
- district `district_rw_city` from Stellaris vanilla: ROI@2250=13688950.0, jobs=1900.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep|uses_inline_script
- building `building_primitive_capital` from Stellaris vanilla: ROI@2250=12992400.0, jobs=1800.0, flags=ai_weight_absent|has_jobs
- district `district_maginot_world_barracks` from Gigastructural Engineering & More (4.4): ROI@2250=12983440.0, jobs=1800.0, flags=ai_weight_zero_or_gated_zero|has_build_cost|has_jobs|has_upkeep
- building `building_machine_system_capital` from Stellaris vanilla: ROI@2250=12265800.0, jobs=1700.0, flags=ai_weight_absent|has_jobs|has_upkeep|uses_inline_script
- building `building_mp_primitive_bnw_hatchery` from More Primitives: ROI@2250=12254400.0, jobs=1700.0, flags=ai_weight_absent|has_jobs
- building `building_giga_corrona_capital` from Gigastructural Engineering & More (4.4): ROI@2250=11556000.0, jobs=1600.0, flags=ai_weight_zero_or_gated_zero|has_jobs
- building `building_imperial_hive_capital` from Stellaris vanilla: ROI@2250=11542200.0, jobs=1600.0, flags=ai_weight_absent|has_jobs|has_upkeep|uses_inline_script
