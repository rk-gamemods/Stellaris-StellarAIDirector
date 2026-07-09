# Stellar AI Director Research Capacity

This is a deterministic active-stack capacity inventory. It resolves winning active-stack job definitions, building job slots, direct building output/upkeep, and building upgrade chains. Job triggered resource blocks are included in the optimistic output columns and should be treated as maximum-potential math, not runtime proof.

Job-producing modifiers are normalized from Stellaris 4.x workforce units using 100 workforce = 1 full job equivalent. Raw workforce totals are retained in the building CSV.

- Jobs indexed: 501
- Buildings indexed: 826
- Districts/zones indexed: 547
- Buildings with resolved research output: 135
- Districts/zones with net consumer-goods output: 8
- Colony role target rows: 247
- Technologies with research-relevant modifiers indexed: 18
- Strategic infrastructure target rows: 1333
- Resource coverage rows: 21
- Build-plan readiness rows: 826
- Strategic benefit taxonomy rows: 1887
- Modeling blocker accounting rows: 1042
- Build-plan consumer policy rows: 1093
- Source roots include vanilla at `C:\Steam\steamapps\common\Stellaris` plus enabled launcher mods.
- Plan rows include base and building-modifier-adjusted research/upkeep. Technology rows are inventoried but not auto-applied to colony plans yet.
- Jobs, buildings, development rows, and plan rows preserve base, triggered, conservative, and optimistic resource scenarios where applicable.
- Strategic infrastructure rows classify habitat growth centers, capital/empire-unique candidates, starbase migration support, and refactor constraints such as `can_demolish = no`.
- Resource coverage rows classify every resource key detected in amount JSON as promoted or unsupported.
- Build-plan readiness rows classify building gate phases and same-role fallback candidates before unlocks.
- Strategic benefit taxonomy rows classify detected non-resource benefits and record no-evidence classes for active-stack gaps.
- Modeling blocker accounting rows normalize unknown jobs, unresolved variables, quality flags, unsupported resources, and unvalued benefit formulas.
- Build-plan consumer policy rows join readiness, blocker accounting, role targets, and benefit taxonomy into scorable/not-scorable consumer decisions.

## Top Research Buildings

| rank | building | research/month | jobs | mod |
| --- | --- | ---: | ---: | --- |
| 1 | `building_mem_lost_emperor_ancient_palace` | 1506.9 | 8.8 | More Events Mod |
| 2 | `building_master_archive` | 450.0 | 10.0 | Stellaris vanilla |
| 3 | `building_pinniped_sanctuary` | 105.0 | 16.0 | Stellaris vanilla |
| 4 | `building_giga_institute_2` | 81.0 | 0 | Gigastructural Engineering & More (4.4) |
| 5 | `building_giga_supercomputer_2` | 81.0 | 0 | Gigastructural Engineering & More (4.4) |
| 6 | `building_wet_td_bio_lab` | 68.25 | 9.0 | Stellar AI Director |
| 7 | `building_superhab_lab` | 64.5 | 9.0 | Stellar AI Director |
| 8 | `building_fe_lab_2` | 60.0 | 0 | Stellaris vanilla |
| 9 | `building_giga_iodizium_research` | 60.0 | 0 | Gigastructural Engineering & More (4.4) |
| 10 | `building_giga_institute_1` | 54.0 | 0 | Gigastructural Engineering & More (4.4) |
| 11 | `building_giga_supercomputer_1` | 54.0 | 0 | Gigastructural Engineering & More (4.4) |
| 12 | `building_cryo_lab` | 49.125 | 4.5 | Stellar AI Director |
| 13 | `building_order_keep` | 48.0 | 16.0 | Stellaris vanilla |
| 14 | `building_augmentation_center` | 40.0 | 8.0 | Stellaris vanilla |
| 15 | `building_karst_lab` | 36.0 | 9.0 | Stellar AI Director |
| 16 | `building_navel_command` | 36.0 | 12.0 | Planetary Diversity - More Arcologies |
| 17 | `building_supercon_lab` | 34.125 | 4.5 | Stellar AI Director |
| 18 | `building_aquifer_lab` | 32.25 | 4.5 | Stellar AI Director |
| 19 | `building_biolumen_lab` | 32.25 | 4.5 | Stellar AI Director |
| 20 | `building_lichen_lab` | 32.25 | 4.5 | Stellar AI Director |

## Top Consumer-Goods Districts/Zones

| rank | type | object | net consumer goods/month | jobs | mod |
| --- | --- | --- | ---: | ---: | --- |
| 1 | district | `district_giga_birch_void_ktisma` | 5000.0 | 2.4 | Gigastructural Engineering & More (4.4) |
| 2 | district | `district_giga_frameworld_sanctuary_advanced` | 40.0 | 0.4 | Gigastructural Engineering & More (4.4) |
| 3 | district | `district_giga_frameworld_sanctuary` | 20.0 | 0.2 | Gigastructural Engineering & More (4.4) |
| 4 | district | `district_giga_frameworld_factory_advanced` | 10.0 | 0.01 | Gigastructural Engineering & More (4.4) |
| 5 | district | `district_srw_commercial` | 8.5 | 4.0 | Planetary Diversity - More Arcologies |
| 6 | zone | `zone_resort_grand_museum` | 6.0 | 2.0 | Stellaris vanilla |
| 7 | zone | `zone_resort_spiritual_retreat` | 6.0 | 2.0 | Stellaris vanilla |
| 8 | district | `district_giga_frameworld_factory` | 5.0 | 0.01 | Gigastructural Engineering & More (4.4) |

## Colony Role Targets

| role | source | class | net role output | selected |
| --- | --- | --- | ---: | --- |
| agri_world | build_plan_candidate_terminal_buildings_12_in_12_slots | building_slots_any_colony | 511.0 | `building_nourishment_center|building_giga_gas_giant_habitation_module|building_giga_interstellar_hydroponic_farm|building_low_tech_farm|building_contained_ecosphere|building_giga_pcc_scrap_pile|building_bio_reprocessing_facilities|building_food_processing_center|building_junkheap|building_giga_corrona_homes|building_foundry_upkeep_1|building_food_conglomerate` |
| agri_world | development_top_1 | all_colony_classes | 10000.0 | `district:district_giga_birch_void_ktisma` |
| factory_world | build_plan_candidate_terminal_buildings_12_in_12_slots | building_slots_any_colony | 99.625 | `building_affluence_center|building_junkheap|building_factory_efficiency_1|building_low_tech_scrap_refinery|building_underground_chemists|building_virtual_entertainment_studios|building_temple_of_prosperity|building_subversive_shrine|building_low_tech_admin_hub|building_research_upkeep_1|esc_building_reprocessing_plant|building_industrial_subsidiary` |
| factory_world | development_top_1 | all_colony_classes | 5000.0 | `district:district_giga_birch_void_ktisma` |
| forge_world | build_plan_candidate_terminal_buildings_12_in_12_slots | building_slots_any_colony | 153.675 | `building_giga_gas_giant_habitation_module|building_nano_forge|building_giga_pcc_scrap_pile|building_giga_interstellar_hydroponic_farm|building_nanotech_cauldron|building_foundry_efficiency_1|esc_building_reprocessing_plant|building_wet_td_bio_lab|building_materiality_engine|building_low_tech_scrap_refinery|building_supercon_lab|building_storm_lab` |
| forge_world | development_top_1 | all_colony_classes | 5000.0 | `district:district_giga_birch_void_ktisma` |
| generator_world | build_plan_candidate_terminal_buildings_12_in_12_slots | building_slots_any_colony | 1023.0 | `building_giga_gas_giant_habitation_module|building_giga_blokkat_blokkwork_node|building_class_4_singularity|building_giga_research_lab_2|building_giga_flusion_fusion_power_plant|building_giga_iodizium_plant|esc_building_stellar_energy_tower|building_waste_reprocessing_center|building_giga_energy_nexus_3|building_cyberdome|building_private_security|building_underground_clubs` |
| generator_world | development_top_1 | all_colony_classes | 10000.0 | `district:district_giga_birch_void_ktisma` |
| mining_world | build_plan_candidate_terminal_buildings_12_in_12_slots | building_slots_any_colony | 434.5 | `building_giga_gas_giant_habitation_module|building_giga_pcc_scrap_pile|building_giga_matter_synthesizer|esc_building_magmaminer_2|building_mineral_purification_hub|building_wildcat_miners|building_low_tech_scrap_refinery|building_materiality_engine|building_junkheap|building_waste_reprocessing_center|gpm_building_mining_nanite_nexus|building_research_upkeep_1` |
| mining_world | development_top_1 | all_colony_classes | 10000.0 | `district:district_giga_birch_void_ktisma` |
| refinery_world | build_plan_candidate_terminal_buildings_9_in_12_slots | building_slots_any_colony | 135.5 | `building_dimensional_fabricator|building_nanite_transmuter|building_mote_aggravator|building_crystal_growth|building_churning_stomach|esc_building_crystal_farm_2|building_giga_elysium_dust_sifter|building_living_metal_clinic|building_offworld_expedition_hub` |
| refinery_world | development_top_1 | all_colony_classes | 9.0 | `district:district_giga_frameworld_refinery` |
| research_world | build_plan_candidate_terminal_buildings_12_in_12_slots | building_slots_any_colony | 1154.4025 | `building_master_archive|building_pinniped_sanctuary|building_giga_supercomputer_2|building_giga_institute_2|building_wet_td_bio_lab|building_superhab_lab|building_giga_iodizium_research|esc_building_dragon_hatchery|building_cryo_lab|building_order_keep|building_augmentation_center|building_navel_command` |
| research_world | development_top_1 | all_colony_classes | 7500.0 | `district:district_giga_birch_void_physma` |
| trade_world | build_plan_candidate_terminal_buildings_12_in_12_slots | building_slots_any_colony | 381.0 | `building_giga_research_lab_2|building_giga_interstellar_hydroponic_farm|building_giga_gas_giant_habitation_module|building_tendril_cradle_4|building_cyberdome|building_temple_of_prosperity|building_subversive_shrine|building_low_tech_admin_hub|building_giga_matrioshka_brain_uplink_entertainment|building_clear_thought_clinic|building_imperial_concession_port|building_gaia_unity_temple` |
| trade_world | development_top_1 | all_colony_classes | 103.0 | `district:district_maginot_ringworld_barracks` |
| unity_world | build_plan_candidate_terminal_buildings_12_in_12_slots | building_slots_any_colony | 369.0 | `gpm_building_ascension_tower|building_giga_matrioshka_brain_uplink_sanctuary|building_giga_matrioshka_brain_uplink_entertainment|building_solarpunk_gaiaseeder|building_gaia_unity_servitor|building_simulation_3|building_sensorium_3|building_hypercomms_forum|building_galactic_memorial_3|building_corporate_forum|xeno_geology_holomuseum|galactic_history_holomuseum` |
| unity_world | development_top_1 | all_colony_classes | 346.5 | `district:district_mindlink` |

## Strategic Infrastructure Targets

| role | object | score | tags | source |
| --- | --- | ---: | --- | --- |
| starbase_migration_support | `starbase_building:transit_hub` | 350.0 | migration_source|starbase_migration_support | Stellaris vanilla |
| habitat_growth_center | `building:building_clone_army_clone_vat` | 1110.0 | capital_or_empire_unique_candidate|habitat_growth_center|has_destroy_trigger | Stellaris vanilla |
| habitat_growth_center | `building:building_clone_vats` | 450.0 | habitat_growth_center|has_destroy_trigger | Stellar AI Director |
| habitat_growth_center | `building:building_mem_lost_emperor_ancient_palace` | 285.0 | capital_or_empire_unique_candidate|habitat_growth_center|has_destroy_trigger | More Events Mod |
| habitat_growth_center | `building:building_mem_ancestors_grudge_robot_factory` | 135.0 | capital_or_empire_unique_candidate|habitat_growth_center | More Events Mod |
| habitat_growth_center | `building:building_genomic_facility` | 100.0 | habitat_growth_center|has_destroy_trigger | Stellaris vanilla |
| habitat_growth_center | `building:building_woorskyr_biofuel_refinery` | 13.75 | capital_or_empire_unique_candidate|habitat_growth_center|has_destroy_trigger | Forgotten Empires 4.4.1 |
| habitat_growth_center | `building:building_woorskyr_barkfarm` | 12.5 | capital_or_empire_unique_candidate|habitat_growth_center|has_destroy_trigger | Forgotten Empires 4.4.1 |
| habitat_growth_center | `building:building_woorskyr_growth_monitoring_center` | 12.5 | capital_or_empire_unique_candidate|habitat_growth_center|has_destroy_trigger | Forgotten Empires 4.4.1 |
| habitat_support_center | `building:building_hab_capital` | 15.0 | cannot_demolish|capital_or_empire_unique_candidate|habitat_support_candidate | Stellaris vanilla |
| habitat_support_center | `building:building_hab_fe_capital` | 15.0 | capital_or_empire_unique_candidate|habitat_support_candidate | Stellaris vanilla |
| habitat_support_center | `building:building_hab_major_capital` | 15.0 | cannot_demolish|capital_or_empire_unique_candidate|habitat_support_candidate | Stellaris vanilla |
| habitat_support_center | `building:building_hab_system_capital` | 15.0 | cannot_demolish|capital_or_empire_unique_candidate|habitat_support_candidate | Stellaris vanilla |
| habitat_support_center | `building:building_giga_gas_giant_habitation_module` | 5.0 | habitat_support_candidate|has_destroy_trigger | Gigastructural Engineering & More (4.4) |
| habitat_support_center | `building:building_giga_habitat_zro_harvester` | 5.0 | habitat_support_candidate | Gigastructural Engineering & More (4.4) |
| habitat_support_center | `building:building_superhab_farm` | 5.0 | habitat_support_candidate|has_destroy_trigger | Stellar AI Director |
| habitat_support_center | `building:building_superhab_foundry` | 5.0 | habitat_support_candidate|has_destroy_trigger | Stellar AI Director |
| capital_world | `building:building_grand_embassy` | 60.0 | capital_or_empire_unique_candidate|has_destroy_trigger | Stellaris vanilla |
| capital_world | `building:building_order_keep` | 60.0 | cannot_demolish|capital_or_empire_unique_candidate|has_destroy_trigger|migration_destination | Stellaris vanilla |
| capital_world | `building:building_embassy` | 35.0 | capital_or_empire_unique_candidate|has_destroy_trigger | Stellaris vanilla |
| capital_world | `building:building_whisperers_sanctum` | 35.0 | capital_or_empire_unique_candidate|has_destroy_trigger | Stellaris vanilla |
| capital_world | `building:mem_building_ancient_palace` | 35.0 | capital_or_empire_unique_candidate | More Events Mod |
| capital_world | `building:building_cyberdome` | 22.5 | capital_or_empire_unique_candidate|has_destroy_trigger|migration_destination | Stellaris vanilla |
| capital_world | `building:building_xeno_tourism_agency` | 22.5 | capital_or_empire_unique_candidate|migration_destination | Stellaris vanilla |
| capital_world | `building:building_cradle_sanctum` | 15.0 | capital_or_empire_unique_candidate|has_destroy_trigger | Stellaris vanilla |
| starbase_fleet_scaling | `starbase_module:arkship_capital_shipyard` | 60.0 | starbase_fleet_scaling|starbase_support_candidate | Stellaris vanilla |
| starbase_fleet_scaling | `starbase_building:equatorial_shipyard_uplink` | 60.0 | starbase_fleet_scaling|starbase_support_candidate | Gigastructural Engineering & More (4.4) |
| starbase_fleet_scaling | `starbase_building:gpm_precursor_shipyards_uplink` | 60.0 | starbase_fleet_scaling|starbase_support_candidate | Guilli's Planet Modifiers and Features |
| starbase_fleet_scaling | `starbase_building:hyperstructural_shipyard_uplink` | 60.0 | starbase_fleet_scaling|starbase_support_candidate | Gigastructural Engineering & More (4.4) |
| starbase_fleet_scaling | `starbase_module:orbital_ring_shipyard` | 60.0 | starbase_fleet_scaling|starbase_support_candidate | Stellaris vanilla |
| starbase_fleet_scaling | `starbase_module:shipyard` | 60.0 | starbase_fleet_scaling|starbase_support_candidate | Stellaris vanilla |
| starbase_fleet_scaling | `starbase_building:virtual_shipyard_uplink_building` | 60.0 | starbase_fleet_scaling|starbase_support_candidate | Gigastructural Engineering & More (4.4) |
| starbase_fleet_scaling | `starbase_building:adv_assembly_yard` | 50.0 | starbase_fleet_scaling | Starbase Extended 3.0 |
| starbase_resource_support | `starbase_building:financial_space_center` | 30.0 | starbase_resource_support | Starbase Extended 3.0 |
| starbase_resource_support | `starbase_building:pyroclastic_resonator` | 30.0 | starbase_resource_support | Stellaris vanilla |
| starbase_resource_support | `starbase_module:solar_panel_network` | 30.0 | starbase_resource_support | NSC3 |
| starbase_resource_support | `starbase_building:trader_proxy_office` | 30.0 | starbase_resource_support|starbase_support_candidate | Stellaris vanilla |
| starbase_resource_support | `starbase_module:trading_hub` | 29.5 | starbase_resource_support | Stellaris vanilla |
| starbase_resource_support | `starbase_building:esc_starbase_reactor` | 27.0 | starbase_resource_support | Stellar AI Director |
| starbase_resource_support | `starbase_module:astromining_bay` | 26.0 | starbase_resource_support | Stellaris vanilla |
| starbase_resource_support | `starbase_building:nebula_refinery` | 26.0 | starbase_resource_support | Stellaris vanilla |

## Colony Scenarios

| scenario | base research/month | adjusted research/month | adjusted CG upkeep | colonies for 3000 |
| --- | ---: | ---: | ---: | ---: |
| raw_top_terminal_top_1_in_6_slots | 1506.9 | 1506.9 | 4.15 | 2 |
| raw_top_terminal_top_3_in_6_slots | 2061.9 | 2061.9 | 18.15 | 2 |
| raw_top_terminal_top_6_in_6_slots | 2194.65 | 2391.975 | 31.65 | 2 |
| raw_top_terminal_top_1_in_8_slots | 1506.9 | 1506.9 | 4.15 | 2 |
| raw_top_terminal_top_3_in_8_slots | 2061.9 | 2061.9 | 18.15 | 2 |
| raw_top_terminal_top_8_in_8_slots | 2356.65 | 2553.975 | 31.65 | 2 |
| raw_top_terminal_top_1_in_10_slots | 1506.9 | 1506.9 | 4.15 | 2 |
| raw_top_terminal_top_3_in_10_slots | 2061.9 | 2061.9 | 18.15 | 2 |
| raw_top_terminal_top_10_in_10_slots | 2453.775 | 2692.1625 | 35.4 | 2 |
| raw_top_terminal_top_1_in_12_slots | 1506.9 | 1506.9 | 4.15 | 2 |
| raw_top_terminal_top_3_in_12_slots | 2061.9 | 2061.9 | 18.15 | 2 |
| raw_top_terminal_top_12_in_12_slots | 2573.775 | 2815.0875 | 35.4 | 2 |
| repeatable_candidate_terminal_top_1_in_6_slots | 450.0 | 450.0 | 0.0 | 7 |
| repeatable_candidate_terminal_top_3_in_6_slots | 555.0 | 682.5 | 14.0 | 5 |
| repeatable_candidate_terminal_top_6_in_6_slots | 768.75 | 962.625 | 27.5 | 4 |
| repeatable_candidate_terminal_top_1_in_8_slots | 450.0 | 450.0 | 0.0 | 7 |
| repeatable_candidate_terminal_top_3_in_8_slots | 555.0 | 682.5 | 14.0 | 5 |
| repeatable_candidate_terminal_top_8_in_8_slots | 897.75 | 1115.625 | 27.5 | 3 |
| repeatable_candidate_terminal_top_1_in_10_slots | 450.0 | 450.0 | 0.0 | 7 |
| repeatable_candidate_terminal_top_3_in_10_slots | 555.0 | 682.5 | 14.0 | 5 |
| repeatable_candidate_terminal_top_10_in_10_slots | 1006.875 | 1244.4 | 31.25 | 3 |
| repeatable_candidate_terminal_top_1_in_12_slots | 450.0 | 450.0 | 0.0 | 7 |
| repeatable_candidate_terminal_top_3_in_12_slots | 555.0 | 682.5 | 14.0 | 5 |
| repeatable_candidate_terminal_top_12_in_12_slots | 1066.875 | 1367.0025 | 31.25 | 3 |
