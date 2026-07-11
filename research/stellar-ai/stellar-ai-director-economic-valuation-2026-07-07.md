# Stellar AI Director Economic Valuation Dataset

Generated: 2026-07-11T20:51:07.414173+00:00

This dataset is the required evidence gate before generating new late-game unemployment or construction-pressure weights. It mines the active Irony stack plus vanilla for planet `buildings`, `zones`, and `districts`, records the top-level load winner, and computes rough long-horizon ROI against the 2350 target end date.

Important limitations:

- ROI is a rough planning number, not a game simulation.
- Explicit `ai_resource_production` and direct production are valued directly.
- Stellaris 4.x job modifiers use workforce units, normalized here as `100` workforce per full job equivalent before valuation.
- Job-only objects use `6.0` value per normalized job per month because final job output depends on empire, species, designation, buildings, and modifiers.
- Modifier-only objects use a conservative key-count proxy and are flagged for review.
- Inline scripts and unresolved variables are flagged so later weight generation can prefer high-confidence rows or require manual review.

Active collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity
Active mod count: 116

## Row Counts

- building: 826
- district: 286
- zone: 261

## Data Quality Flags

- ai_weight_absent: 1256
- ai_weight_zero_or_gated_zero: 34
- has_ai_or_direct_output: 214
- has_build_cost: 616
- has_jobs: 348
- has_upkeep: 758
- none: 1
- overridden_in_stack: 123
- uses_inline_script: 1037

## Highest Rough ROI At 2250 Horizon

- district `district_giga_birch_void_ktisma` from Gigastructural Engineering & More (4.4): ROI@2250=9392880.0, jobs=2.4, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep
- district `district_giga_birch_void_orykta` from Gigastructural Engineering & More (4.4): ROI@2250=7856880.0, jobs=2.4, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs
- building `building_mem_lost_emperor_ancient_palace` from More Events Mod: ROI@2250=3886560.0, jobs=8.8, flags=has_ai_or_direct_output|has_jobs
- building `building_giga_aeternum_synthetizer` from Gigastructural Engineering & More (4.4): ROI@2250=1461600.0, jobs=60.0, flags=ai_weight_zero_or_gated_zero|has_ai_or_direct_output|has_jobs|uses_inline_script
- district `district_maginot_ringworld_barracks` from Gigastructural Engineering & More (4.4): ROI@2250=1111280.0, jobs=153.0, flags=ai_weight_zero_or_gated_zero|has_build_cost|has_jobs|has_upkeep
- district `district_rw_science` from Stellaris vanilla: ROI@2250=877550.0, jobs=120.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- building `building_fe_dome` from Stellaris vanilla: ROI@2250=870900.0, jobs=125.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- district `district_mindlink` from Stellaris vanilla: ROI@2250=678075.0, jobs=30.0, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
- building `building_giga_gas_giant_habitation_module` from Gigastructural Engineering & More (4.4): ROI@2250=481500.0, jobs=63.0, flags=ai_weight_zero_or_gated_zero|has_jobs|has_upkeep|uses_inline_script
- building `building_dimensional_fabricator` from Stellaris vanilla: ROI@2250=463100.0, jobs=0.0, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_upkeep
- building `gpm_building_ascension_tower` from Guilli's Planet Modifiers and Features: ROI@2250=445980.0, jobs=60.0, flags=ai_weight_zero_or_gated_zero|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep
- building `building_fe_sky_dome` from Stellaris vanilla: ROI@2250=444000.0, jobs=62.5, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- building `building_giga_matrioshka_brain_uplink_sanctuary` from Gigastructural Engineering & More (4.4): ROI@2250=367200.0, jobs=50.0, flags=ai_weight_absent|has_jobs|uses_inline_script
- building `building_master_archive` from Stellaris vanilla: ROI@2250=329100.0, jobs=10.0, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
- district `district_rw_farming` from Stellaris vanilla: ROI@2250=326750.0, jobs=45.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- district `district_rw_generator` from Stellaris vanilla: ROI@2250=326750.0, jobs=45.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- building `building_organic_paradise` from Stellaris vanilla: ROI@2250=309100.0, jobs=30.0, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
- building `building_giga_matrioshka_brain_uplink_entertainment` from Gigastructural Engineering & More (4.4): ROI@2250=302400.0, jobs=37.0, flags=ai_weight_absent|has_jobs|uses_inline_script
- building `building_giga_aeternum_quantum_reactor` from Gigastructural Engineering & More (4.4): ROI@2250=300000.0, jobs=0.0, flags=ai_weight_zero_or_gated_zero|has_ai_or_direct_output|uses_inline_script
- building `building_giga_aeternum_leisure_center` from Gigastructural Engineering & More (4.4): ROI@2250=225000.0, jobs=0.0, flags=ai_weight_zero_or_gated_zero|has_ai_or_direct_output|uses_inline_script
- district `district_maginot_ringworld_bunkers` from Gigastructural Engineering & More (4.4): ROI@2250=220700.0, jobs=30.0, flags=has_build_cost|has_jobs|has_upkeep|uses_inline_script
- building `building_passenger_paradise` from Stellaris vanilla: ROI@2250=204700.0, jobs=15.0, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
- district `district_giga_frameworld_sanctuary_advanced` from Gigastructural Engineering & More (4.4): ROI@2250=190780.0, jobs=0.4, flags=ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep
- district `district_rw_commercial` from Stellaris vanilla: ROI@2250=189950.0, jobs=26.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
- building `building_gaia_unity_servitor` from Planetary Diversity: ROI@2250=184520.0, jobs=25.0, flags=ai_weight_absent|has_build_cost|has_jobs|has_upkeep
