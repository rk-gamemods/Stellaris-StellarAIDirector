# Stellar AI Director Route Reports

Generated from atlas route hints, dependency edges, and policy rows. This is a static planning report.

## mega_engineering_core

- Objects: 1269
- Dependency edges: 3907
- Policy rows: 1269
- Manual/external dependency targets: 847

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `alloys_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `alloys_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `alloys_expenditure_megastructures_arkships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `alloys_expenditure_megastructures_arkships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `alloys_expenditure_megastructures_waystations` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `alloys_expenditure_megastructures_waystations` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `alloys_expenditure_pre_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/giga_budgets.txt` |
| `dark_matter_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `energy_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_energy_budget.txt` |
| `food_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_food_budget.txt` |
| `food_expenditure_megastructures_arkships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_food_budget.txt` |
| `food_expenditure_megastructures_waystations` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_food_budget.txt` |
| `influence_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_influence_budget.txt` |
| `influence_expenditure_megastructures_arkships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_influence_budget.txt` |
| `influence_expenditure_megastructures_waystations` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_influence_budget.txt` |
| `negative_mass_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `sentient_metal_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `supertensiles_upkeep_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/giga_amb_budget.txt` |
| `unity_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_unity_budget.txt` |
| `ehof_megastructure.001` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.002` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.003` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.004` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.005` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0051` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0052` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0053` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.00531` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0054` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0055` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0056` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.006` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.007` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.008` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.009` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0091` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0092` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.010` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.0102` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |
| `ehof_megastructure.011` | event | parent_ai_unknown | manual_review | `events/giga_105_ehof.txt` |

## mega_shipyard_core

- Objects: 74
- Dependency edges: 232
- Policy rows: 74
- Manual/external dependency targets: 28

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_private_shipyards` | building | parent_ai_complete | observe | `common/buildings/14_branch_office_buildings.txt` |
| `holding_franchise_headquarters` | building | parent_ai_absent | observe | `common/buildings/15_overlord_holdings.txt` |
| `d_fallen_orbital_shipyard` | deposit | parent_ai_absent | observe | `common/deposits/10_paragon_deposits.txt` |
| `giga_equatorial_shipyard_origin.001` | event | parent_ai_unknown | manual_review | `events/giga_209_origins_equatorial_shipyard.txt` |
| `blokkat_shipyard_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_p_blokkat_shipyard.txt` |
| `blokkat_shipyard_build_custodians` | megastructure | parent_ai_absent | build | `common/megastructures/zz_p_blokkat_shipyard.txt` |
| `blokkat_shipyard_build_dismantler` | megastructure | parent_ai_absent | build | `common/megastructures/zz_p_blokkat_shipyard.txt` |
| `blokkat_shipyard_build_evictors` | megastructure | parent_ai_absent | build | `common/megastructures/zz_p_blokkat_shipyard.txt` |
| `blokkat_shipyard_build_terminator` | megastructure | parent_ai_absent | build | `common/megastructures/zz_p_blokkat_shipyard.txt` |
| `eq_shipyard_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_e_equatorial_shipyard_dummy.txt` |
| `eq_shipyard_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_equatorial_shipyard.txt` |
| `eq_shipyard_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_equatorial_shipyard.txt` |
| `eq_shipyard_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_equatorial_shipyard.txt` |
| `gpm_mega_shipyard_restored_precursor` | megastructure | parent_ai_absent | build | `common/megastructures/000_z_giga_compat_dummy_megas.txt` |
| `gpm_mega_shipyard_ruined_precursor` | megastructure | parent_ai_absent | build | `common/megastructures/000_z_giga_compat_dummy_megas.txt` |
| `mega_shipyard_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_e_mega_shipyard_dummy.txt` |
| `mega_shipyard_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_mega_shipyard.txt` |
| `mega_shipyard_0` | megastructure | parent_ai_partial | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_0` | megastructure | parent_ai_partial | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_mega_shipyard.txt` |
| `mega_shipyard_1` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_1` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_mega_shipyard.txt` |
| `mega_shipyard_2` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_2` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_3` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_mega_shipyard.txt` |
| `mega_shipyard_3` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_3` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_permanently_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_permanently_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_restored` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_mega_shipyard.txt` |
| `mega_shipyard_restored` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_restored` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_mega_shipyard.txt` |
| `mega_shipyard_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `mega_shipyard_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/11_mega_shipyard.txt` |
| `nsc_flagship_shipyard` | megastructure | parent_ai_partial | build | `common/megastructures/nsc_megas_flagship.txt` |
| `nsc_flagship_shipyard_complete` | megastructure | parent_ai_absent | build | `common/megastructures/nsc_megas_flagship.txt` |
| `nsc_headquarters_0` | megastructure | parent_ai_partial | build | `common/megastructures/nsc_megas_headquarters.txt` |
| `nsc_headquarters_1` | megastructure | parent_ai_absent | build | `common/megastructures/nsc_megas_headquarters.txt` |

## economy_megastructure_core

- Objects: 243
- Dependency edges: 771
- Policy rows: 243
- Manual/external dependency targets: 83

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_giga_matrioshka_brain_uplink` | building | parent_ai_complete | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_amalgamation` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_anti_deviancy` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_diplomacy` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_entertainment` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_factory` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_foundry` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_hell` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_livestock` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_refinery` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_research` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_robot` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_sanctuary` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_training` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_unity` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_virtual` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `dyson_gun_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_e_stellar_cannon_dummy.txt` |
| `dyson_gun_0` | megastructure | parent_ai_partial | build | `common/megastructures/31_dyson_gun.txt` |
| `dyson_gun_0_restored` | megastructure | parent_ai_absent | build | `common/megastructures/31_dyson_gun.txt` |
| `dyson_gun_1` | megastructure | parent_ai_absent | build | `common/megastructures/31_dyson_gun.txt` |
| `dyson_gun_2` | megastructure | parent_ai_absent | build | `common/megastructures/31_dyson_gun.txt` |
| `dyson_gun_3` | megastructure | parent_ai_absent | build | `common/megastructures/31_dyson_gun.txt` |
| `dyson_gun_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/31_dyson_gun.txt` |
| `dyson_sphere_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_e_dyson_sphere_dummy.txt` |
| `dyson_sphere_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_dyson_sphere.txt` |
| `dyson_sphere_0` | megastructure | parent_ai_partial | build | `common/megastructures/01_dyson_sphere.txt` |
| `dyson_sphere_0_a_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_0_b_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_0_f_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_0_g_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_0_k_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_0_m_giant_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_0_m_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_0_o_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_o_star.txt` |
| `dyson_sphere_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_dyson_sphere.txt` |
| `dyson_sphere_1` | megastructure | parent_ai_absent | build | `common/megastructures/01_dyson_sphere.txt` |
| `dyson_sphere_1_a_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_1_b_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_1_f_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |
| `dyson_sphere_1_g_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_scaling.txt` |

## early_kilo_economy_core

- Objects: 58
- Dependency edges: 154
- Policy rows: 58
- Manual/external dependency targets: 7

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `d_arc_furnace_1` | deposit | parent_ai_complete | observe | `common/deposits/13_machine_age_deposits.txt` |
| `d_arc_furnace_2` | deposit | parent_ai_complete | observe | `common/deposits/13_machine_age_deposits.txt` |
| `d_arc_furnace_3` | deposit | parent_ai_complete | observe | `common/deposits/13_machine_age_deposits.txt` |
| `d_arc_furnace_4` | deposit | parent_ai_complete | observe | `common/deposits/13_machine_age_deposits.txt` |
| `asteroid_manufactory_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_c_asteroid_manufactory_dummy.txt` |
| `asteroid_manufactory_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_2` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_ai_alloys` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_ai_consumer_goods` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_ai_energy` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_ai_food` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_ai_supertensiles` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_alloys` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_consumer_goods` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_energy` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_food` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_platform_alloys` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_platform_consumer_goods` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_platform_energy` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_platform_food` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_platform_supertensiles` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `asteroid_manufactory_supertensiles` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_asteroid_manufactory.txt` |
| `orbital_arc_furnace_1` | megastructure | parent_ai_absent | build | `common/megastructures/000_c_arc_orbital_arc_furnace_dummy.txt` |
| `orbital_arc_furnace_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_1` | megastructure | parent_ai_partial | build | `common/megastructures/17_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_2` | megastructure | parent_ai_absent | build | `common/megastructures/17_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_3` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_3` | megastructure | parent_ai_absent | build | `common/megastructures/17_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_4` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_4` | megastructure | parent_ai_absent | build | `common/megastructures/17_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_destroyed` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_destroyed` | megastructure | parent_ai_absent | build | `common/megastructures/17_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_restored` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_orbital_arc_furnace.txt` |
| `orbital_arc_furnace_restored` | megastructure | parent_ai_absent | build | `common/megastructures/17_orbital_arc_furnace.txt` |
| `dismantle_arc_furnace_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/federations_event_effects.txt` |
| `remove_flags_asteroid_manufactory` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_menu_effects.txt` |
| `remove_flags_storm_observatory` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_menu_effects.txt` |
| `giga_has_asteroid_manufactory` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `giga_has_completed_asteroid_manufactory` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |

## science_kilo_snowball_core

- Objects: 21
- Dependency edges: 77
- Policy rows: 21
- Manual/external dependency targets: 21

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `atmosphere_shredder_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_c_atmospheric_storm_observatory_dummy.txt` |
| `atmosphere_shredder_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_atmospheric_storm_observatory.txt` |
| `atmosphere_shredder_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_atmospheric_storm_observatory.txt` |
| `atmosphere_shredder_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_atmospheric_storm_observatory.txt` |
| `atmosphere_shredder_3` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_atmospheric_storm_observatory.txt` |
| `atmosphere_shredder_restored` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_atmospheric_storm_observatory.txt` |
| `atmosphere_shredder_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_atmospheric_storm_observatory.txt` |
| `macro_test_site_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_c_macroengineering_test_site_dummy.txt` |
| `macro_test_site_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_macroengineering_test_site.txt` |
| `macro_test_site_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_macroengineering_test_site.txt` |
| `macro_test_site_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_macroengineering_test_site.txt` |
| `macro_test_site_3` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_macroengineering_test_site.txt` |
| `macro_test_site_restored` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_macroengineering_test_site.txt` |
| `macro_test_site_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_macroengineering_test_site.txt` |
| `ehof_giga_new_create_atmosphere_shredder_system` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/z_giga_new_ehof_effects_1.txt` |
| `giga_dismantle_science_kilo_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_dismantle_effects.txt` |
| `science_kilo_update_orbital_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_habitat_effects.txt` |
| `ehof_giga_new_is_atmosphere_shredder` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_new_ehof_triggers.txt` |
| `giga_has_macroengineering_test_site` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `giga_system_has_atmosphere_shredder` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `giga_tech_engineering_test_site` | technology | parent_ai_partial | research | `common/technology/giga_03_engineering.txt` |

## research_megastructure_core

- Objects: 212
- Dependency edges: 610
- Policy rows: 212
- Manual/external dependency targets: 59

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_forever_cruise_passenger_research` | building | parent_ai_absent | observe | `common/buildings/24_nomads_buildings.txt` |
| `building_giga_aeternum_megacity_research` | building | parent_ai_absent | observe | `common/buildings/giga_aeternum_buildings.txt` |
| `building_giga_blokkat_hyperdimensional_research` | building | parent_ai_absent | observe | `common/buildings/giga_blokkat_buildings.txt` |
| `building_giga_iodizium_research` | building | parent_ai_complete | observe | `common/buildings/giga_buildings.txt` |
| `building_giga_matrioshka_brain_uplink_research` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_research_lab_1` | building | parent_ai_absent | observe | `common/buildings/giga_buildings.txt` |
| `building_giga_research_lab_2` | building | parent_ai_absent | observe | `common/buildings/giga_buildings.txt` |
| `building_illicit_research_labs` | building | parent_ai_complete | observe | `common/buildings/14_branch_office_buildings.txt` |
| `building_low_tech_research_lab` | building | parent_ai_absent | observe | `common/buildings/16_first_contact_buildings.txt` |
| `building_primitive_research` | building | parent_ai_absent | observe | `common/buildings/11_primitive_buildings.txt` |
| `building_private_research_initiative` | building | parent_ai_complete | observe | `common/buildings/14_branch_office_buildings.txt` |
| `building_research_efficiency_1` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_research_lab_1` | building | parent_ai_absent | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_research_lab_1` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_research_lab_2` | building | parent_ai_absent | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_research_lab_2` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_research_lab_3` | building | parent_ai_absent | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_research_lab_3` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_research_upkeep_1` | building | parent_ai_complete | observe | `common/buildings/05_research_buildings.txt` |
| `esc_building_central_research_bureau` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `d_artifacts_research_1` | deposit | parent_ai_complete | observe | `common/deposits/06_ancient_relics_deposits.txt` |
| `d_artifacts_research_2` | deposit | parent_ai_complete | observe | `common/deposits/06_ancient_relics_deposits.txt` |
| `d_artifacts_research_3` | deposit | parent_ai_complete | observe | `common/deposits/06_ancient_relics_deposits.txt` |
| `d_giga_job_upkeep_researchers_neg` | deposit | parent_ai_complete | observe | `common/deposits/giga_job_size_deposits.txt` |
| `d_giga_job_upkeep_researchers_pos` | deposit | parent_ai_complete | observe | `common/deposits/giga_job_size_deposits.txt` |
| `d_payback_habitat_research` | deposit | parent_ai_absent | observe | `common/deposits/09_first_contact_deposits.txt` |
| `d_portal_research_zone` | deposit | parent_ai_complete | observe | `common/deposits/02_event_planetary_deposits.txt` |
| `district_arcology_research` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_arcology_research_engineering` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_arcology_research_physics` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_arcology_research_society` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_hive_research` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_hive_research_engineering` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_hive_research_physics` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_hive_research_society` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_nexus_research` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_nexus_research_engineering` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_nexus_research_physics` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_nexus_research_society` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_research` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |

## planetary_computer_research_core

- Objects: 24
- Dependency edges: 53
- Policy rows: 24
- Manual/external dependency targets: 8

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `giga_pcc_origin_alloys` | ai_budget | parent_ai_partial | observe | `common/ai_budget/giga_special_purpose_budgets.txt` |
| `building_giga_pcc_scrap_pile` | building | parent_ai_absent | observe | `common/buildings/giga_buildings.txt` |
| `decision_giga_pcc_science_district` | decision | parent_ai_partial | manual_review | `common/decisions/giga_ai_helpers.txt` |
| `giga_frameworld_computing_complex` | decision | parent_ai_partial | manual_review | `common/decisions/giga_frameworld_upgrades.txt` |
| `d_frameworld_computing_complex` | deposit | parent_ai_complete | observe | `common/deposits/giga_frameworld_deposits.txt` |
| `district_giga_pcc_admin` | district | parent_ai_absent | observe | `common/districts/giga_planetary_computer.txt` |
| `district_giga_pcc_science` | district | parent_ai_absent | observe | `common/districts/giga_planetary_computer.txt` |
| `giga_planetary_computer_origin.001` | event | parent_ai_unknown | manual_review | `events/giga_205_origins_planetary_computer.txt` |
| `planetary_computer_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_e_planetary_computer_dummy.txt` |
| `planetary_computer_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_planetary_computer.txt` |
| `planetary_computer_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_planetary_computer.txt` |
| `planetary_computer_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_planetary_computer.txt` |
| `frameworld_audit_upgrade_computing_complex_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_frameworld_general_effects.txt` |
| `remove_flags_planetary_computer` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_menu_effects.txt` |
| `frameworld_audit_upgrade_computing_complex` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_frameworld_triggers.txt` |
| `giga_has_completed_planetary_computer` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_achievement_triggers.txt` |
| `giga_has_planetary_computer_mega` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `giga_is_pc_giga_planetary_computer` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_planet_class_triggers.txt` |
| `giga_frameworld_outpost_planet_jobs_pc_giga_planetary_computer` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_frameworld_outpost_special_planets.txt` |
| `giga_planetary_computer_limit` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_megastructure_limits.txt` |
| `computing` | technology | parent_ai_absent | research | `common/technology/category/00_category.txt` |
| `giga_tech_planetary_computer` | technology | parent_ai_partial | research | `common/technology/giga_02_society.txt` |
| `giga_tech_repeatable_planetary_computer_cap` | technology | parent_ai_absent | research | `common/technology/giga_07_repeatables_megastructures.txt` |
| `tech_trinary_computing` | technology | parent_ai_partial | research | `common/technology/00_first_contact_tech.txt` |

## pop_assembly_snowball_core

- Objects: 70
- Dependency edges: 126
- Policy rows: 70
- Manual/external dependency targets: 21

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_clone_vats` | building | parent_ai_absent | observe | `common/buildings/01_pop_assembly_buildings.txt` |
| `building_crystal_growth` | building | parent_ai_absent | build | `common/buildings/21_wilderness_buildings.txt` |
| `building_massive_growth_1` | building | parent_ai_absent | build | `common/buildings/21_wilderness_buildings.txt` |
| `building_massive_growth_2` | building | parent_ai_absent | build | `common/buildings/21_wilderness_buildings.txt` |
| `building_massive_growth_3` | building | parent_ai_absent | build | `common/buildings/21_wilderness_buildings.txt` |
| `building_massive_growth_4` | building | parent_ai_absent | build | `common/buildings/21_wilderness_buildings.txt` |
| `building_robot_assembly_complex` | building | parent_ai_absent | build | `common/buildings/01_pop_assembly_buildings.txt` |
| `building_robot_assembly_plant` | building | parent_ai_absent | build | `common/buildings/01_pop_assembly_buildings.txt` |
| `building_spawning_pool` | building | parent_ai_absent | observe | `common/buildings/01_pop_assembly_buildings.txt` |
| `decision_discourage_growth` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `decision_enact_robot_assembly_control` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `decision_end_discourage_growth` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `decision_end_robot_assembly_control` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `decision_tissue_growth_stimulants` | decision | parent_ai_partial | manual_review | `common/decisions/05_ancient_relics_decisions.txt` |
| `d_baol_growth` | deposit | parent_ai_absent | observe | `common/deposits/06_ancient_relics_deposits.txt` |
| `d_crystaline_growths` | deposit | parent_ai_absent | observe | `common/deposits/15_strange_worlds_deposits.txt` |
| `modular_growth_compounds` | edict | parent_ai_partial | manual_review | `common/edicts/00_edicts.txt` |
| `giga_extra_growth.001` | event | parent_ai_unknown | manual_review | `events/giga_032_extra_growth.txt` |
| `awakened_fallen_empire_hive_mind_growth` | personality | parent_ai_partial | manual_review | `common/personalities/01_fallen_empire_personalities.txt` |
| `space_fauna_growth` | policy | parent_ai_partial | manual_review | `common/policies/02_policies_grand_archive.txt` |
| `break_cycle_of_growth` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/shroud_shadows_scripted_effects.txt` |
| `create_hive_fe_fragment_growth` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/fallen_empire_scripted_effects.txt` |
| `giga_extra_growth_find_species` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_extra_growth_effects.txt` |
| `giga_extra_growth_recalculate_variables` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_extra_growth_effects.txt` |
| `giga_extra_growth_setup` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_extra_growth_effects.txt` |
| `giga_extra_growth_tick` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_extra_growth_effects.txt` |
| `launch_cycle_of_growth` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/shroud_shadows_scripted_effects.txt` |
| `can_remove_pop_growth_genetic_traits` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/05_scripted_triggers_traits.txt` |
| `giga_exclude_planet_from_virtual_growth` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_scripted_triggers.txt` |
| `giga_planet_has_robot_assembly_facilities` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_assembly_triggers.txt` |
| `has_cloning_genomic_growth_tradition` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/05_scripted_triggers_biogenesis.txt` |
| `has_cycle_of_growth` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/08_scripted_triggers_shroud.txt` |
| `robot_assembly_plant_upkeep_affordable` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/00_scripted_triggers.txt` |
| `spawning_pool_upkeep_affordable` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/00_scripted_triggers.txt` |
| `entropy_drinkers_edicts_pop_growth` | scripted_value | parent_ai_absent | observe | `common/script_values/07_script_values_shroud.txt` |
| `giga_calculate_extra_growth_base` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_extra_growth_values.txt` |
| `giga_calculate_extra_growth_eta` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_extra_growth_values.txt` |
| `giga_calculate_extra_growth_internal` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_extra_growth_values.txt` |
| `giga_calculate_extra_growth_modifiers` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_extra_growth_values.txt` |
| `giga_calculate_extra_growth_required` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_extra_growth_values.txt` |

## ring_world_growth_core

- Objects: 65
- Dependency edges: 173
- Policy rows: 65
- Manual/external dependency targets: 25

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `decision_enact_population_control` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `decision_enact_population_control_gestalt` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `decision_end_population_control` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `decision_end_population_control_gestalt` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `decision_expel_population` | decision | parent_ai_partial | manual_review | `common/decisions/01_political_decisions.txt` |
| `d_segment_rubble_1` | deposit | parent_ai_complete | observe | `common/deposits/07_federations_deposits.txt` |
| `d_segment_rubble_1_small` | deposit | parent_ai_complete | observe | `common/deposits/07_federations_deposits.txt` |
| `d_segment_rubble_2` | deposit | parent_ai_complete | observe | `common/deposits/07_federations_deposits.txt` |
| `d_segment_rubble_3` | deposit | parent_ai_complete | observe | `common/deposits/07_federations_deposits.txt` |
| `d_segment_rubble_4` | deposit | parent_ai_complete | observe | `common/deposits/07_federations_deposits.txt` |
| `district_ring_world_administrative` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_energy` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_factory` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_food` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_fortress` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_foundry` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_industrial` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_organic_housing` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_research` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_research_engineering` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_research_physics` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_research_society` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_spiritualist` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `district_ring_world_trade` | district | parent_ai_absent | observe | `common/districts/06_swap_districts.txt` |
| `blokkat_population_willingness_propaganda` | edict | parent_ai_partial | manual_review | `common/edicts/blokkat_edicts.txt` |
| `ring_world_1` | megastructure | parent_ai_absent | build | `common/megastructures/000_e_ring_world_dummy.txt` |
| `ring_world_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_ring_world.txt` |
| `ring_world_1` | megastructure | parent_ai_partial | build | `common/megastructures/00_ring_world.txt` |
| `ring_world_2` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_ring_world.txt` |
| `ring_world_2` | megastructure | parent_ai_absent | build | `common/megastructures/00_ring_world.txt` |
| `ring_world_2_intermediate` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_ring_world.txt` |
| `ring_world_2_intermediate` | megastructure | parent_ai_absent | build | `common/megastructures/00_ring_world.txt` |
| `ring_world_3_intermediate` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_ring_world.txt` |
| `ring_world_3_intermediate` | megastructure | parent_ai_absent | build | `common/megastructures/00_ring_world.txt` |
| `ring_world_behemoth_restored` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_behemoth_ringworld.txt` |
| `ring_world_behemoth_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_behemoth_ringworld.txt` |
| `ring_world_gargantuan_restored` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_gargantuan_ringworld.txt` |
| `ring_world_gargantuan_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_gargantuan_ringworld.txt` |
| `ring_world_restored` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_ring_world.txt` |
| `ring_world_restored` | megastructure | parent_ai_partial | build | `common/megastructures/00_ring_world.txt` |

## storage_cap_core

- Objects: 26
- Dependency edges: 69
- Policy rows: 26
- Manual/external dependency targets: 17

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_drone_megastorage` | building | parent_ai_absent | observe | `common/buildings/07_amenity_buildings.txt` |
| `building_drone_storage` | building | parent_ai_absent | observe | `common/buildings/07_amenity_buildings.txt` |
| `building_giga_mega_storage` | building | parent_ai_absent | observe | `common/buildings/giga_ring_world_buildings.txt` |
| `kugelblitz_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_c_emp_kugelblitz_dummy.txt` |
| `kugelblitz_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_kugelblitz.txt` |
| `kugelblitz_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_kugelblitz.txt` |
| `kugelblitz_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_kugelblitz.txt` |
| `kugelblitz_3` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_kugelblitz.txt` |
| `kugelblitz_restored` | megastructure | parent_ai_partial | build | `common/megastructures/zz_c_kugelblitz.txt` |
| `kugelblitz_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/zz_c_kugelblitz.txt` |
| `ehof_giga_new_create_kugelblitz_system` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/z_giga_new_ehof_effects_1.txt` |
| `expel_nomads_destroy_waystation_and_take_stockpile_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/nomads_effects.txt` |
| `random_stockpile_negative` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/00_scripted_effects.txt` |
| `random_stockpile_positive` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/00_scripted_effects.txt` |
| `remove_bm_cost_from_stockpile` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_scripted_effects.txt` |
| `drone_storage_upkeep_affordable` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/00_scripted_triggers.txt` |
| `ehof_giga_new_is_kugelblitz` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_new_ehof_triggers.txt` |
| `giga_has_completed_kugelblitz` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_achievement_triggers.txt` |
| `giga_has_kugelblitz` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `has_negative_income_with_stockpile` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/00_scripted_triggers.txt` |
| `giga_ai_savings_stockpile_fraction` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_ai_savings_values.txt` |
| `giga_ai_savings_stockpile_threshold` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_ai_savings_values.txt` |
| `giga_amb_stockpile_calc` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_amb_script_values.txt` |
| `storage_room` | starbase_module | parent_ai_complete | supplement_prerequisites | `common/starbase_modules/nsc_starbase_modules.txt` |
| `giga_tech_kugelblitz` | technology | parent_ai_partial | research | `common/technology/giga_01_physics.txt` |
| `giga_tech_repeatable_dimensional_storage` | technology | parent_ai_partial | research | `common/technology/giga_04_repeatables.txt` |

## gigas_special_resource_core

- Objects: 174
- Dependency edges: 317
- Policy rows: 174
- Manual/external dependency targets: 52

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `dark_matter_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_expenditure_planets` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_expenditure_ships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_expenditure_starbases` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_expenditure_trade` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_expenditure_upgrade` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_upkeep_edicts` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_upkeep_planets` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_upkeep_ships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `dark_matter_upkeep_starbases` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_dark_matter_budget.txt` |
| `negative_mass_expenditure_buffer` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_colonies_expand` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_colonies_expand_machine` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_decisions` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_planets` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_ship_upgrades` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_ships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_starbases` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_starbases_expand` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_expenditure_starbases_fallen_empires` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_upkeep_buffer` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_upkeep_planets` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `negative_mass_upkeep_ships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `sentient_metal_expenditure_buffer` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_colonies_expand` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_colonies_expand_machine` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_decisions` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_planets` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_ship_upgrades` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_ships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_starbases` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_starbases_expand` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_expenditure_starbases_fallen_empires` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_upkeep_buffer` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_upkeep_planets` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `sentient_metal_upkeep_ships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `supertensiles_upkeep_buffer` | ai_budget | parent_ai_partial | observe | `common/ai_budget/giga_amb_budget.txt` |
| `supertensiles_upkeep_megastructures` | ai_budget | parent_ai_partial | observe | `common/ai_budget/giga_amb_budget.txt` |

## research_throughput_infrastructure

- Objects: 270
- Dependency edges: 688
- Policy rows: 270
- Manual/external dependency targets: 56

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_adakkaria_patriotic_institute` | building | parent_ai_absent | observe | `common/buildings/19_cosmic_storm_buildings.txt` |
| `building_archaeostudies_faculty` | building | parent_ai_absent | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_archaeostudies_faculty` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_forever_cruise_passenger_research` | building | parent_ai_absent | observe | `common/buildings/24_nomads_buildings.txt` |
| `building_giga_aeternum_megacity_research` | building | parent_ai_absent | observe | `common/buildings/giga_aeternum_buildings.txt` |
| `building_giga_blokkat_hyperdimensional_research` | building | parent_ai_absent | observe | `common/buildings/giga_blokkat_buildings.txt` |
| `building_giga_institute_1` | building | parent_ai_complete | observe | `common/buildings/giga_buildings.txt` |
| `building_giga_institute_2` | building | parent_ai_complete | observe | `common/buildings/giga_buildings.txt` |
| `building_giga_iodizium_research` | building | parent_ai_complete | observe | `common/buildings/giga_buildings.txt` |
| `building_giga_matrioshka_brain_uplink_research` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_research_lab_1` | building | parent_ai_absent | observe | `common/buildings/giga_buildings.txt` |
| `building_giga_research_lab_2` | building | parent_ai_absent | observe | `common/buildings/giga_buildings.txt` |
| `building_giga_supercomputer_1` | building | parent_ai_complete | observe | `common/buildings/giga_buildings.txt` |
| `building_giga_supercomputer_2` | building | parent_ai_complete | observe | `common/buildings/giga_buildings.txt` |
| `building_illicit_research_labs` | building | parent_ai_complete | observe | `common/buildings/14_branch_office_buildings.txt` |
| `building_institute` | building | parent_ai_complete | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_institute` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_katzen_science` | building | parent_ai_absent | observe | `common/buildings/giga_flusion_buildings.txt` |
| `building_low_tech_research_lab` | building | parent_ai_absent | observe | `common/buildings/16_first_contact_buildings.txt` |
| `building_primitive_research` | building | parent_ai_absent | observe | `common/buildings/11_primitive_buildings.txt` |
| `building_private_research_initiative` | building | parent_ai_complete | observe | `common/buildings/14_branch_office_buildings.txt` |
| `building_research_efficiency_1` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_research_lab_1` | building | parent_ai_absent | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_research_lab_1` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_research_lab_2` | building | parent_ai_absent | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_research_lab_2` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_research_lab_3` | building | parent_ai_absent | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_research_lab_3` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_research_upkeep_1` | building | parent_ai_complete | observe | `common/buildings/05_research_buildings.txt` |
| `building_supercomputer` | building | parent_ai_complete | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_supercomputer` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `esc_building_central_research_bureau` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_technology_institute` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `decision_giga_pcc_science_district` | decision | parent_ai_partial | manual_review | `common/decisions/giga_ai_helpers.txt` |
| `d_artifacts_research_1` | deposit | parent_ai_complete | observe | `common/deposits/06_ancient_relics_deposits.txt` |
| `d_artifacts_research_2` | deposit | parent_ai_complete | observe | `common/deposits/06_ancient_relics_deposits.txt` |
| `d_artifacts_research_3` | deposit | parent_ai_complete | observe | `common/deposits/06_ancient_relics_deposits.txt` |
| `d_giga_job_upkeep_researchers_neg` | deposit | parent_ai_complete | observe | `common/deposits/giga_job_size_deposits.txt` |
| `d_giga_job_upkeep_researchers_pos` | deposit | parent_ai_complete | observe | `common/deposits/giga_job_size_deposits.txt` |
| `d_payback_habitat_research` | deposit | parent_ai_absent | observe | `common/deposits/09_first_contact_deposits.txt` |

## research_diplomacy_core

- Objects: 14
- Dependency edges: 23
- Policy rows: 14
- Manual/external dependency targets: 2

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_giga_matrioshka_brain_uplink_diplomacy` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `masters_writings_diplomacy` | edict | parent_ai_partial | manual_review | `common/edicts/01_campaigns.txt` |
| `research_federation` | federation_type | parent_ai_partial | manual_review | `common/federation_types/00_federation_types.txt` |
| `close_mindwarden_diplomacy` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/shroud_shadows_scripted_effects.txt` |
| `destroy_espionage_asset_diplomacy` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/espionage_event_effects.txt` |
| `has_espionage_asset_diplomacy` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/02_scripted_triggers_espionage.txt` |
| `tech_xeno_diplomacy` | technology | parent_ai_partial | research | `common/technology/00_soc_tech.txt` |
| `tr_diplomacy_adopt` | tradition | parent_ai_absent | research | `common/traditions/00_diplomacy.txt` |
| `tr_diplomacy_diplomatic_networking` | tradition | parent_ai_partial | research | `common/traditions/00_diplomacy.txt` |
| `tr_diplomacy_direct_diplomacy` | tradition | parent_ai_partial | research | `common/traditions/00_diplomacy.txt` |
| `tr_diplomacy_eminent_diplomats` | tradition | parent_ai_partial | research | `common/traditions/00_diplomacy.txt` |
| `tr_diplomacy_entente_coordination` | tradition | parent_ai_partial | research | `common/traditions/00_diplomacy.txt` |
| `tr_diplomacy_finish` | tradition | parent_ai_absent | research | `common/traditions/00_diplomacy.txt` |
| `tr_diplomacy_the_federation` | tradition | parent_ai_partial | research | `common/traditions/00_diplomacy.txt` |

## planetcraft_route

- Objects: 24
- Dependency edges: 111
- Policy rows: 24
- Manual/external dependency targets: 18

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `ap_celestial_printing` | ascension_perk | parent_ai_partial | research | `common/ascension_perks/giga_ascension_perks.txt` |
| `aeternum_planetcraft_restored` | megastructure | parent_ai_absent | build | `common/megastructures/zzz_unlisted_megas.txt` |
| `aeternum_planetcraft_ruined` | megastructure | parent_ai_absent | build | `common/megastructures/zzz_unlisted_megas.txt` |
| `planetcraft_printer_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_i_behemoth_assembly_plant_dummy.txt` |
| `planetcraft_printer_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_0_real` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_1_fake` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_2_fake` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_3` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_3_fake` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_make_planet` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_make_planet_fake` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `planetcraft_printer_ready` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| `remove_flags_fe_planetcrafts` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_menu_effects.txt` |
| `giga_has_planetcraft_printer` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `giga_aeternum_planetcraft` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/giga_aeternum_ships.txt` |
| `giga_corrona_planetcraft` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/giga_corrona_ships.txt` |
| `giga_planet_behemoth` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/giga_ships.txt` |
| `giga_tech_aeternite_planetcraft` | technology | parent_ai_partial | research | `common/technology/giga_11_aeternum.txt` |
| `giga_tech_asteroid_artillery_planetcraft_upgrade` | technology | parent_ai_partial | research | `common/technology/giga_12_asteroid_artillery.txt` |
| `giga_tech_maginot_planetcraft_upgrade` | technology | parent_ai_partial | research | `common/technology/giga_15_maginot.txt` |
| `giga_tech_planet_assembly` | technology | parent_ai_partial | research | `common/technology/giga_01_physics.txt` |

## war_moon_route

- Objects: 50
- Dependency edges: 226
- Policy rows: 50
- Manual/external dependency targets: 61

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `giga_survey_attack_moon` | edict | parent_ai_partial | manual_review | `common/edicts/giga_edicts.txt` |
| `flusion_attack_moon_0` | megastructure | parent_ai_absent | build | `common/megastructures/zzz_unlisted_megas.txt` |
| `flusion_attack_moon_1` | megastructure | parent_ai_absent | build | `common/megastructures/zzz_unlisted_megas.txt` |
| `lunar_disco_ball_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_e_lunar_speculorefractor_disco_dummy.txt` |
| `lunar_disco_ball_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_lunar_speculorefractor_disco.txt` |
| `lunar_disco_ball_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_lunar_speculorefractor_disco.txt` |
| `lunar_disco_ball_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_lunar_speculorefractor_disco.txt` |
| `lunar_macroreplicator_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_i_lunar_macroreplicator_dummy.txt` |
| `lunar_macroreplicator_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `lunar_macroreplicator_0_real` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `lunar_macroreplicator_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `lunar_macroreplicator_1_fake` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `lunar_macroreplicator_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `lunar_macroreplicator_2_fake` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `lunar_macroreplicator_make_moon` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `lunar_macroreplicator_make_moon_fake` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `lunar_macroreplicator_ready` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_lunar_macroreplicator.txt` |
| `war_moon_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_e_attack_moon_dummy.txt` |
| `war_moon_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_1` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_2` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_debris_barren` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_debris_cold_barren` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_debris_disco` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_debris_frozen` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_debris_luna` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_debris_molten` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_restored_barren` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_restored_cold_barren` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_restored_disco` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_restored_frozen` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_restored_luna` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `war_moon_restored_molten` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_attack_moon.txt` |
| `giga_war_moon` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_scripted_effects.txt` |
| `giga_war_moon_debris_mega` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_scripted_effects.txt` |
| `giga_can_be_war_moon` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_scripted_triggers.txt` |
| `giga_has_completed_war_moon` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_achievement_triggers.txt` |
| `giga_has_lunar_disco_ball` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `giga_has_lunar_macroreplicator` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `giga_has_war_moon_mega` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |

## systemcraft_route

- Objects: 33
- Dependency edges: 118
- Policy rows: 33
- Manual/external dependency targets: 23

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `ap_celestial_printing` | ascension_perk | parent_ai_partial | research | `common/ascension_perks/giga_ascension_perks.txt` |
| `decision_systemcraft_crew` | decision | parent_ai_partial | manual_review | `common/decisions/giga_decisions.txt` |
| `war_system_0` | megastructure | parent_ai_absent | build | `common/megastructures/000_i_stellar_systemcraft_dummy.txt` |
| `war_system_0` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_stellar_systemcraft.txt` |
| `war_system_1` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_stellar_systemcraft.txt` |
| `war_system_2` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_stellar_systemcraft.txt` |
| `war_system_3` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_stellar_systemcraft.txt` |
| `war_system_4` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_stellar_systemcraft.txt` |
| `war_system_5` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_stellar_systemcraft.txt` |
| `remove_flags_systemcraft` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_menu_effects.txt` |
| `can_destroy_planet_with_PLANET_KILLER_CRACKER_SYSTEMCRAFT` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/zzz_overwrites.txt` |
| `can_destroy_planet_with_PLANET_KILLER_DELUGE_SYSTEMCRAFT` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/zzz_overwrites.txt` |
| `can_destroy_planet_with_PLANET_KILLER_DEVOLUTION_SYSTEMCRAFT` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/zzz_overwrites.txt` |
| `can_destroy_planet_with_PLANET_KILLER_GODRAY_SYSTEMCRAFT` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/zzz_overwrites.txt` |
| `can_destroy_planet_with_PLANET_KILLER_NANOBOTS_SYSTEMCRAFT` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/zzz_overwrites.txt` |
| `can_destroy_planet_with_PLANET_KILLER_NEUTRON_SYSTEMCRAFT` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/zzz_overwrites.txt` |
| `can_destroy_planet_with_PLANET_KILLER_SHIELDER_SYSTEMCRAFT` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/zzz_overwrites.txt` |
| `can_destroy_planet_with_PLANET_KILLER_SMELTER_SYSTEMCRAFT` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/zzz_overwrites.txt` |
| `giga_has_completed_war_system` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_achievement_triggers.txt` |
| `giga_has_war_system` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_megastructure_type_triggers.txt` |
| `giga_ship_uses_war_system_components` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_scripted_triggers.txt` |
| `giga_systemcraft_limit` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_megastructure_limits.txt` |
| `giga_o_systemcraft` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/!_giga_placeholder_ships.txt` |
| `giga_planet_behemoth` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/giga_ships.txt` |
| `giga_systemcraft` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/giga_ships.txt` |
| `giga_tech_maginot_systemcraft_upgrade` | technology | parent_ai_partial | research | `common/technology/giga_15_maginot.txt` |
| `giga_tech_repeatable_systemcraft_cap` | technology | parent_ai_absent | research | `common/technology/giga_07_repeatables_megastructures.txt` |
| `giga_tech_war_system_1` | technology | parent_ai_partial | research | `common/technology/giga_05_weightless.txt` |
| `giga_tech_war_system_2` | technology | parent_ai_partial | research | `common/technology/giga_01_physics.txt` |
| `giga_tech_war_system_3` | technology | parent_ai_partial | research | `common/technology/giga_01_physics.txt` |
| `giga_tech_war_system_4` | technology | parent_ai_partial | research | `common/technology/giga_01_physics.txt` |
| `giga_tech_war_system_5` | technology | parent_ai_partial | research | `common/technology/giga_01_physics.txt` |
| `giga_tech_war_system_6` | technology | parent_ai_partial | research | `common/technology/giga_03_engineering.txt` |

## nsc3_capital_hull_route

- Objects: 63
- Dependency edges: 129
- Policy rows: 63
- Manual/external dependency targets: 9

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `holding_franchise_headquarters` | building | parent_ai_absent | observe | `common/buildings/15_overlord_holdings.txt` |
| `guardian_dreadnought` | country_type | parent_ai_unknown | manual_review | `common/country_types/01_leviathans_country_types.txt` |
| `nsc_events_flagship.1` | event | parent_ai_unknown | manual_review | `events/nsc_events_flagship.txt` |
| `nsc_events_flagship.10` | event | parent_ai_unknown | manual_review | `events/nsc_events_flagship.txt` |
| `nsc_events_flagship.3` | event | parent_ai_unknown | manual_review | `events/nsc_events_flagship.txt` |
| `nsc_events_flagship.4` | event | parent_ai_unknown | manual_review | `events/nsc_events_flagship.txt` |
| `nsc_events_flagship.6` | event | parent_ai_unknown | manual_review | `events/nsc_events_flagship.txt` |
| `nsc_events_flagship.7` | event | parent_ai_unknown | manual_review | `events/nsc_events_flagship.txt` |
| `nsc_events_flagship.8` | event | parent_ai_unknown | manual_review | `events/nsc_events_flagship.txt` |
| `nsc_events_flagship.9` | event | parent_ai_unknown | manual_review | `events/nsc_events_flagship.txt` |
| `nsc_flagship_shipyard` | megastructure | parent_ai_partial | build | `common/megastructures/nsc_megas_flagship.txt` |
| `nsc_flagship_shipyard_complete` | megastructure | parent_ai_absent | build | `common/megastructures/nsc_megas_flagship.txt` |
| `nsc_headquarters_0` | megastructure | parent_ai_partial | build | `common/megastructures/nsc_megas_headquarters.txt` |
| `nsc_headquarters_1` | megastructure | parent_ai_absent | build | `common/megastructures/nsc_megas_headquarters.txt` |
| `ehof_giga_new_spawn_ancient_dreadnought` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/z_giga_new_ehof_guardian.txt` |
| `esc_mod_menu_component_dreadnought_disabled_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/esc_modmenu_effects.txt` |
| `esc_mod_menu_component_dreadnought_enabled_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/esc_modmenu_effects.txt` |
| `nsc_flagship_creation_for_ai_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/nsc_scripted_effects.txt` |
| `ESC_ship_uses_NSC_headquarters_computers` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_carrier_components` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_carrier_computers` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_carrier_reactors` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_dreadnought_carrier_components` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_dreadnought_carrier_reactors` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_dreadnought_components` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_dreadnought_reactors` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_flagship_components` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ESC_ship_uses_flagship_reactors` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/esc_ship_size_triggers.txt` |
| `ehof_giga_new_can_spawn_dreadnought` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/giga_new_ehof_triggers.txt` |
| `is_pd_headquarters_arcology` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/00_giga_compat_overwrite_me.txt` |
| `ship_uses_carrier_role` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/nsc_scripted_triggers.txt` |
| `ship_uses_carrier_role` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/07_scripted_triggers_ships.txt` |
| `ship_uses_dreadnought_reactors` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/nsc_scripted_triggers.txt` |
| `ship_uses_dreadnought_thrusters` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/nsc_scripted_triggers.txt` |
| `ship_uses_flagship_components` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/nsc_scripted_triggers.txt` |
| `Carrier` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/!_giga_placeholder_ships.txt` |
| `Carrier` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/nsc_ship_sizes.txt` |
| `Dreadnought` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/!_giga_placeholder_ships.txt` |
| `Dreadnought` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/nsc_ship_sizes.txt` |
| `Flagship` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/!_giga_placeholder_ships.txt` |

## esc_component_route

- Objects: 888
- Dependency edges: 2345
- Policy rows: 888
- Manual/external dependency targets: 747

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_bio_reactor` | building | parent_ai_absent | observe | `common/buildings/~stellarai_resource_buildings.txt` |
| `building_bio_reactor` | building | parent_ai_absent | observe | `common/buildings/03_resource_buildings.txt` |
| `building_bio_reactor_2` | building | parent_ai_absent | observe | `common/buildings/~stellarai_resource_buildings.txt` |
| `building_bio_reactor_2` | building | parent_ai_absent | observe | `common/buildings/03_resource_buildings.txt` |
| `building_giga_aeternum_quantum_reactor` | building | parent_ai_complete | observe | `common/buildings/giga_aeternum_buildings.txt` |
| `building_giga_eawaf_psifusion_reactor` | building | parent_ai_complete | observe | `common/buildings/giga_eawaf_buildings.txt` |
| `building_giga_planetary_shield_generator_2` | building | parent_ai_absent | observe | `common/buildings/giga_buildings.txt` |
| `building_lathe_reactor` | building | parent_ai_absent | observe | `common/buildings/20_machine_age_buildings.txt` |
| `building_planetary_shield_generator` | building | parent_ai_complete | observe | `common/buildings/09_army_buildings.txt` |
| `esc_building_central_research_bureau` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_cerebral_node` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_crystal_farm_1` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `esc_building_crystal_farm_2` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `esc_building_culture_nexus` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_dark_matter_facility` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `esc_building_dragon_hatchery` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_magmaminer_1` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `esc_building_magmaminer_2` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `esc_building_materials_laboratory` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_nanite_foundry` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `esc_building_network_regulator` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_quantum_node` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_reprocessing_plant` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `esc_building_stellar_energy_tower` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_technology_institute` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_watcher` | building | parent_ai_absent | observe | `common/buildings/esc_buildings_general.txt` |
| `esc_building_zro_distillery` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `decision_esc_clone_dragon` | decision | parent_ai_unknown | manual_review | `common/decisions/esc_decisions.txt` |
| `decision_esc_clone_sky_dragon` | decision | parent_ai_unknown | manual_review | `common/decisions/esc_decisions.txt` |
| `decision_esc_mod_cheat_menu` | decision | parent_ai_unknown | manual_review | `common/decisions/esc_decisions.txt` |
| `decision_esc_mod_menu` | decision | parent_ai_unknown | manual_review | `common/decisions/esc_decisions.txt` |
| `decision_grandbunny_shield_system` | decision | parent_ai_partial | manual_review | `common/decisions/blokkat_decisions.txt` |
| `decision_turn_aet_shield_off` | decision | parent_ai_partial | manual_review | `common/decisions/giga_aeternum_decisions.txt` |
| `decision_turn_aet_shield_on` | decision | parent_ai_partial | manual_review | `common/decisions/giga_aeternum_decisions.txt` |
| `decision_unaligned_shields` | decision | parent_ai_partial | manual_review | `common/decisions/15_nomads_dlc_decisions.txt` |
| `d_aeternum_gigantic_fission_reactor` | deposit | parent_ai_complete | observe | `common/deposits/aeternum_planetary_deposits.txt` |
| `d_alderson_ruined_shield` | deposit | parent_ai_complete | observe | `common/deposits/giga_planetary_deposits.txt` |
| `d_ancient_reactor_pits` | deposit | parent_ai_absent | observe | `common/deposits/06_ancient_relics_deposits.txt` |
| `d_esc_large_borehole_1` | deposit | parent_ai_complete | observe | `common/deposits/nhsc_deposits.txt` |
| `d_esc_mantle_alloy_plume` | deposit | parent_ai_absent | observe | `common/deposits/nhsc_deposits.txt` |

## crowded_tall_route

- Objects: 1697
- Dependency edges: 3166
- Policy rows: 1697
- Manual/external dependency targets: 528

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `alloys_expenditude_frameworld_advanced_districts` | ai_budget | parent_ai_partial | observe | `common/ai_budget/giga_frameworld_budgets.txt` |
| `alloys_expenditure_habitats` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `alloys_expenditure_habitats` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `food_expenditure_buildings` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_food_budget.txt` |
| `influence_expenditure_habitats` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_influence_budget.txt` |
| `nanites_expenditure_buildings` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_nanites_budget.txt` |
| `aesthetic_wonders_holomuseum` | building | parent_ai_absent | observe | `common/buildings/21_grand_archive_buildings.txt` |
| `building_abandoned_gene_clinic` | building | parent_ai_absent | observe | `common/buildings/20_machine_age_buildings.txt` |
| `building_adakkaria_patriotic_institute` | building | parent_ai_absent | observe | `common/buildings/19_cosmic_storm_buildings.txt` |
| `building_advanced_storm_attraction_center` | building | parent_ai_complete | observe | `common/buildings/19_cosmic_storm_buildings.txt` |
| `building_advanced_storm_repellent_center` | building | parent_ai_absent | observe | `common/buildings/19_cosmic_storm_buildings.txt` |
| `building_advanced_storm_resistant_production` | building | parent_ai_complete | observe | `common/buildings/19_cosmic_storm_buildings.txt` |
| `building_affluence_center` | building | parent_ai_absent | observe | `common/buildings/13_fallen_empire_buildings.txt` |
| `building_affluence_emporium` | building | parent_ai_absent | observe | `common/buildings/13_fallen_empire_buildings.txt` |
| `building_ai_emporium` | building | parent_ai_complete | observe | `common/buildings/14_branch_office_buildings.txt` |
| `building_akx_worm_3` | building | parent_ai_absent | observe | `common/buildings/12_event_buildings.txt` |
| `building_alpha_hub` | building | parent_ai_absent | observe | `common/buildings/08_unity_buildings.txt` |
| `building_amphitheater_of_the_mind` | building | parent_ai_complete | observe | `common/buildings/20_machine_age_buildings.txt` |
| `building_amusement_megaplex` | building | parent_ai_complete | observe | `common/buildings/14_branch_office_buildings.txt` |
| `building_ancient_control_center` | building | parent_ai_absent | observe | `common/buildings/13_fallen_empire_buildings.txt` |
| `building_ancient_cryo_chamber` | building | parent_ai_absent | observe | `common/buildings/13_fallen_empire_buildings.txt` |
| `building_ancient_hive_capital` | building | parent_ai_absent | observe | `common/buildings/13_fallen_empire_buildings.txt` |
| `building_ancient_palace` | building | parent_ai_absent | observe | `common/buildings/13_fallen_empire_buildings.txt` |
| `building_ancient_ward_1` | building | parent_ai_absent | observe | `common/buildings/23_shroud_buildings.txt` |
| `building_ancient_ward_2` | building | parent_ai_absent | observe | `common/buildings/23_shroud_buildings.txt` |
| `building_archaeo_refinery` | building | parent_ai_absent | observe | `common/buildings/04_manufacturing_buildings.txt` |
| `building_archaeostudies_faculty` | building | parent_ai_absent | observe | `common/buildings/~stellarai_research_buildings.txt` |
| `building_archaeostudies_faculty` | building | parent_ai_absent | observe | `common/buildings/05_research_buildings.txt` |
| `building_artist_patron` | building | parent_ai_absent | observe | `common/buildings/12_event_buildings.txt` |
| `building_astral_siphon_1` | building | parent_ai_absent | observe | `common/buildings/18_astral_planes_buildings.txt` |
| `building_astral_siphon_2` | building | parent_ai_absent | observe | `common/buildings/18_astral_planes_buildings.txt` |
| `building_astral_siphon_3` | building | parent_ai_absent | observe | `common/buildings/18_astral_planes_buildings.txt` |
| `building_astrometeorology_observation_center` | building | parent_ai_complete | observe | `common/buildings/19_cosmic_storm_buildings.txt` |
| `building_augmentation_bazaars` | building | parent_ai_complete | observe | `common/buildings/20_machine_age_buildings.txt` |
| `building_augmentation_bazaars_branch` | building | parent_ai_complete | observe | `common/buildings/14_branch_office_buildings.txt` |
| `building_augmentation_center` | building | parent_ai_absent | observe | `common/buildings/20_machine_age_buildings.txt` |
| `building_autochthon_monument` | building | parent_ai_complete | observe | `common/buildings/08_unity_buildings.txt` |
| `building_autocurating_vault` | building | parent_ai_absent | observe | `common/buildings/08_unity_buildings.txt` |
| `building_automation_1` | building | parent_ai_absent | observe | `common/buildings/01_pop_assembly_buildings.txt` |
| `building_automation_2` | building | parent_ai_absent | observe | `common/buildings/01_pop_assembly_buildings.txt` |

## conquest_escape_route

- Objects: 657
- Dependency edges: 1273
- Policy rows: 657
- Manual/external dependency targets: 342

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `influence_expenditure_claims` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_influence_budget.txt` |
| `influence_expenditure_claims_fanatic_militarist` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_influence_budget.txt` |
| `influence_expenditure_claims_militarist` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_influence_budget.txt` |
| `ap_lord_of_war` | ascension_perk | parent_ai_partial | research | `common/ascension_perks/00_ascension_perks.txt` |
| `building_ancient_ward_1` | building | parent_ai_absent | observe | `common/buildings/23_shroud_buildings.txt` |
| `building_ancient_ward_2` | building | parent_ai_absent | observe | `common/buildings/23_shroud_buildings.txt` |
| `building_expanded_warren` | building | parent_ai_absent | observe | `common/buildings/07_amenity_buildings.txt` |
| `building_hive_warren` | building | parent_ai_absent | observe | `common/buildings/07_amenity_buildings.txt` |
| `caravaneer_fleet` | country_type | parent_ai_unknown | manual_review | `common/country_types/03_country_types_megacorp.txt` |
| `mindwarden_enclave` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `swarm` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `swarm_fleeing_blokkats` | country_type | parent_ai_unknown | manual_review | `common/country_types/giga_blokkat_country_types.txt` |
| `decision_caravaneer_tupperware` | decision | parent_ai_partial | manual_review | `common/decisions/04_caravaneer_decisions.txt` |
| `decision_claim_system_megas` | decision | parent_ai_partial | manual_review | `common/decisions/giga_decisions.txt` |
| `decision_lithoid_swarm_consume_world` | decision | parent_ai_partial | manual_review | `common/decisions/02_special_decisions.txt` |
| `decision_manager_awards` | decision | parent_ai_partial | manual_review | `common/decisions/05_ancient_relics_decisions.txt` |
| `decision_nanotech_swarm_consume_world` | decision | parent_ai_partial | manual_review | `common/decisions/12_machine_age_decisions.txt` |
| `d_toxic_god_deitys_swarms` | deposit | parent_ai_absent | observe | `common/deposits/02_event_planetary_deposits.txt` |
| `d_toxic_god_deitys_swarms_upgraded` | deposit | parent_ai_absent | observe | `common/deposits/02_event_planetary_deposits.txt` |
| `d_wetware_computer` | deposit | parent_ai_complete | observe | `common/deposits/02_event_planetary_deposits.txt` |
| `cybernetic_creed_war_edict` | edict | parent_ai_partial | manual_review | `common/edicts/04_machine_age_edicts.txt` |
| `fleet_supremacy` | edict | parent_ai_partial | manual_review | `common/edicts/00_edicts.txt` |
| `giga_eawaf_sirens_secret_mindwardens` | edict | parent_ai_unknown | manual_review | `common/edicts/giga_edicts.txt` |
| `grand_fleet` | edict | parent_ai_partial | manual_review | `common/edicts/02_ambitions.txt` |
| `masters_writings_war` | edict | parent_ai_partial | manual_review | `common/edicts/01_campaigns.txt` |
| `stately_acclaim` | edict | parent_ai_partial | manual_review | `common/edicts/04_machine_age_edicts.txt` |
| `war_drone_campaign` | edict | parent_ai_partial | manual_review | `common/edicts/01_campaigns.txt` |
| `war_drone_campaign_wilderness` | edict | parent_ai_partial | manual_review | `common/edicts/01_campaigns.txt` |
| `awareness.100` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.105` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.115` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.120` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.125` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.130` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.135` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.140` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.145` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.150` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.155` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |
| `awareness.160` | event | parent_ai_unknown | manual_review | `events/pre_ftl_awareness_events.txt` |

## raiding_pop_acquisition_route

- Objects: 44
- Dependency edges: 59
- Policy rows: 44
- Manual/external dependency targets: 6

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `ap_nihilistic_acquisition` | ascension_perk | parent_ai_partial | research | `common/ascension_perks/00_ascension_perks.txt` |
| `decision_cease_psi_inoculate_pops` | decision | parent_ai_partial | manual_review | `common/decisions/08_paragon_decisions.txt` |
| `decision_psi_inoculate_pops` | decision | parent_ai_partial | manual_review | `common/decisions/08_paragon_decisions.txt` |
| `d_ancient_bombardment_craters` | deposit | parent_ai_complete | observe | `common/deposits/02_event_planetary_deposits.txt` |
| `orbital_bombardment` | policy | parent_ai_unknown | manual_review | `common/policies/nsc_policies.txt` |
| `orbital_bombardment` | policy | parent_ai_partial | manual_review | `common/policies/00_policies.txt` |
| `orbital_bombardment_accept_surrender` | policy | parent_ai_partial | manual_review | `common/policies/00_policies.txt` |
| `add_advanced_empire_capital_pops_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/01_start_of_game_effects.txt` |
| `add_advanced_empire_colony_pops_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/01_start_of_game_effects.txt` |
| `create_hibernators_pops` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/strange_worlds_effects.txt` |
| `cyberize_creed_pops_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/02_machine_age_effects.txt` |
| `cyberize_limited_hive_pops_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/02_machine_age_effects.txt` |
| `cyberize_pops_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/02_machine_age_effects.txt` |
| `generate_civic_secondary_pops` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/01_start_of_game_effects.txt` |
| `generate_start_pops` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/01_start_of_game_effects.txt` |
| `giga_frameworld_outpost_pops_and_message` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_frameworld_general_effects.txt` |
| `increase_pre_ftl_pops_by_age_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/pre_ftl_scripted_effects.txt` |
| `make_nascent_starting_pops` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/biogenesis_effects.txt` |
| `make_pops_storm_fused_with_chance` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/cosmic_storms_scripted_effects.txt` |
| `setup_paluush_primitive_planet_no_buildings_no_pops` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/giga_primitives.txt` |
| `synthesize_pops_effect` | scripted_effect | parent_ai_absent | observe | `common/scripted_effects/02_machine_age_effects.txt` |
| `has_organic_pops` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/00_scripted_triggers.txt` |
| `is_under_crisis_bombardment` | scripted_trigger | parent_ai_absent | observe | `common/scripted_triggers/00_scripted_triggers.txt` |
| `available_pops_for_bodysnatcher` | scripted_value | parent_ai_absent | observe | `common/script_values/06_script_values_biogenesis.txt` |
| `calc_intensity_from_pops_in_system` | scripted_value | parent_ai_absent | observe | `common/script_values/07_script_values_shroud.txt` |
| `clone_pops_value` | scripted_value | parent_ai_absent | observe | `common/script_values/06_script_values_biogenesis.txt` |
| `giga_birch_insula_from_pops_next` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_birch_values.txt` |
| `giga_birch_insulae_from_pops` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_birch_values.txt` |
| `giga_elysium_pen_pops` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_elysium_values.txt` |
| `giga_frameworld_outpost_pops` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_frameworld_script_values.txt` |
| `giga_grab_percent_pops` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_script_values.txt` |
| `giga_planet_density_by_pops` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_job_scaling_values.txt` |
| `giga_planet_density_by_pops_inner_1` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_job_scaling_values.txt` |
| `giga_planet_density_by_pops_inner_2` | scripted_value | parent_ai_partial | observe | `common/script_values/giga_job_scaling_values.txt` |
| `giga_psychic_hypersiphon_psionic_pops` | scripted_value | parent_ai_absent | observe | `common/script_values/giga_script_values.txt` |
| `num_pops_in_strata` | scripted_value | parent_ai_absent | observe | `common/script_values/00_script_values.txt` |
| `pre_ftl_pops_shifting_ethic` | scripted_value | parent_ai_absent | observe | `common/script_values/00_script_values.txt` |
| `situation_machine_uprising_pops_monthly_progress` | scripted_value | parent_ai_absent | observe | `common/script_values/00_script_values.txt` |
| `situation_shroud_forged_machine_pops_modifier` | scripted_value | parent_ai_absent | observe | `common/script_values/00_script_values.txt` |
| `situation_shroud_forged_mechanical_pops_modifier` | scripted_value | parent_ai_absent | observe | `common/script_values/00_script_values.txt` |

## hostile_space_fauna_clearance_route

- Objects: 455
- Dependency edges: 858
- Policy rows: 455
- Manual/external dependency targets: 260

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `rare_crystals_expenditure_hyper_relays` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_expenditure_planets` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_expenditure_ships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_expenditure_starbases` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_expenditure_starbases_standard` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_expenditure_trade` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_expenditure_upgrade` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_upkeep_edicts` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_upkeep_hyper_relays` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_upkeep_planets` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_upkeep_ships` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_upkeep_starbases` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `rare_crystals_upkeep_starbases_standard` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_rare_crystals_budget.txt` |
| `building_crystal_growth` | building | parent_ai_absent | build | `common/buildings/21_wilderness_buildings.txt` |
| `building_crystal_mines` | building | parent_ai_complete | observe | `common/buildings/~stellarai_deposit_buildings.txt` |
| `building_crystal_mines` | building | parent_ai_absent | observe | `common/buildings/10_deposit_buildings.txt` |
| `building_crystal_plant` | building | parent_ai_complete | observe | `common/buildings/~stellarai_manufacturing_buildings.txt` |
| `building_crystal_plant` | building | parent_ai_absent | observe | `common/buildings/04_manufacturing_buildings.txt` |
| `building_crystal_plant_2` | building | parent_ai_absent | observe | `common/buildings/12_event_buildings.txt` |
| `esc_building_crystal_farm_1` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `esc_building_crystal_farm_2` | building | parent_ai_complete | observe | `common/buildings/esc_buildings_resources.txt` |
| `amoeba` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `amoeba_borderless` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `amoeba_faction` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `amoeba_garrison` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `crystal` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `crystal_faction` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `decision_crystalline_architecture` | decision | parent_ai_partial | manual_review | `common/decisions/02_special_decisions.txt` |
| `decision_crystalline_refugees` | decision | parent_ai_partial | manual_review | `common/decisions/02_special_decisions.txt` |
| `decision_reorganize_leviathan_parade` | decision | parent_ai_unknown | manual_review | `common/decisions/02_special_decisions.txt` |
| `d_celestial_storm_3_crystal` | deposit | parent_ai_absent | observe | `common/deposits/12_cosmic_storms_deposits.txt` |
| `d_crystal_forest` | deposit | parent_ai_complete | observe | `common/deposits/01_planetary_deposits.txt` |
| `d_crystal_kraken_body` | deposit | parent_ai_complete | observe | `common/deposits/02_event_planetary_deposits.txt` |
| `d_crystal_kraken_body_bombed` | deposit | parent_ai_complete | observe | `common/deposits/02_event_planetary_deposits.txt` |
| `d_crystal_reef` | deposit | parent_ai_complete | observe | `common/deposits/01_planetary_deposits.txt` |
| `d_crystal_rift` | deposit | parent_ai_complete | observe | `common/deposits/11_astral_planes_deposits.txt` |
| `d_crystaline_growths` | deposit | parent_ai_absent | observe | `common/deposits/15_strange_worlds_deposits.txt` |
| `d_crystalline_caverns` | deposit | parent_ai_complete | observe | `common/deposits/01_planetary_deposits.txt` |
| `d_crystalline_glacier` | deposit | parent_ai_complete | observe | `common/deposits/02_event_planetary_deposits.txt` |
| `d_esc_mantle_rare_crystal_cluster` | deposit | parent_ai_absent | observe | `common/deposits/nhsc_deposits.txt` |

## apex_site_preservation_core

- Objects: 119
- Dependency edges: 401
- Policy rows: 119
- Manual/external dependency targets: 40

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `building_giga_matrioshka_brain_uplink` | building | parent_ai_complete | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_amalgamation` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_anti_deviancy` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_diplomacy` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_entertainment` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_factory` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_foundry` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_hell` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_livestock` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_refinery` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_research` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_robot` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_sanctuary` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_training` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_unity` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `building_giga_matrioshka_brain_uplink_virtual` | building | parent_ai_absent | observe | `common/buildings/giga_matrioshka_brain_uplinks.txt` |
| `giga_o_star.1000` | event | parent_ai_unknown | manual_review | `events/giga_019_o_stars.txt` |
| `giga_o_star.2000` | event | parent_ai_unknown | manual_review | `events/giga_019_o_stars.txt` |
| `giga_o_star.2001` | event | parent_ai_unknown | manual_review | `events/giga_019_o_stars.txt` |
| `dyson_sphere_0_o_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_e_dyson_sphere_o_star.txt` |
| `dyson_sphere_1_o_star` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_dyson_sphere_o_star.txt` |
| `dyson_sphere_2_o_star` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_dyson_sphere_o_star.txt` |
| `dyson_sphere_3_o_star` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_dyson_sphere_o_star.txt` |
| `dyson_sphere_4_o_star` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_dyson_sphere_o_star.txt` |
| `dyson_sphere_5_o_star` | megastructure | parent_ai_partial | build | `common/megastructures/zz_e_dyson_sphere_o_star.txt` |
| `matrioshka_brain_0_a_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_0_b_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_0_f_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_0_g_star` | megastructure | parent_ai_absent | build | `common/megastructures/000_i_matrioshka_brain_dummy.txt` |
| `matrioshka_brain_0_g_star` | megastructure | parent_ai_partial | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_0_k_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_0_m_giant_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_0_m_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_0_o_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_1_a_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_1_b_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_1_f_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_1_g_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_1_k_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| `matrioshka_brain_1_m_giant_star` | megastructure | parent_ai_absent | build | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |

## fallen_empire_benchmark_route

- Objects: 892
- Dependency edges: 2124
- Policy rows: 892
- Manual/external dependency targets: 1066

| object | type | support | action | source |
| --- | --- | --- | --- | --- |
| `alloys_expenditure_starbases_fallen_empires` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `alloys_expenditure_starbases_fallen_empires` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_alloys_budget.txt` |
| `food_expenditure_starbases_fallen_empires` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_food_budget.txt` |
| `negative_mass_expenditure_starbases_fallen_empires` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_negative_mass_budget.txt` |
| `sentient_metal_expenditure_starbases_fallen_empires` | ai_budget | parent_ai_partial | observe | `common/ai_budget/00_sentient_metal_budget.txt` |
| `ap_become_the_crisis` | ascension_perk | parent_ai_partial | research | `common/ascension_perks/00_ascension_perks.txt` |
| `awakened_corrona` | country_type | parent_ai_unknown | manual_review | `common/country_types/giga_corrona_country_types.txt` |
| `awakened_fallen_empire` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `awakened_marauders` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `awakened_synth_queen` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `fallen_empire` | country_type | parent_ai_unknown | manual_review | `common/country_types/00_country_types.txt` |
| `voidworms_crisis` | country_type | parent_ai_unknown | manual_review | `common/country_types/06_country_types_grand_archive.txt` |
| `decision_systemcraft_crew` | decision | parent_ai_partial | manual_review | `common/decisions/giga_decisions.txt` |
| `d_fallen_orbital_shipyard` | deposit | parent_ai_absent | observe | `common/deposits/10_paragon_deposits.txt` |
| `biocrisis.1` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.100` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.101` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.105` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.115` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.125` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.130` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.15` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.150` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.151` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.155` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.160` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.162` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.165` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.170` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.175` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.180` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.185` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.187` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.190` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.191` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.192` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.193` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.194` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.195` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
| `biocrisis.196` | event | parent_ai_unknown | manual_review | `events/biogenesis_crisis_events.txt` |
