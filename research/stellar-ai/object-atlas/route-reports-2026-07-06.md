# Stellar AI Director Route Reports

Generated from atlas route hints, dependency edges, and policy rows. This is a static planning report.

## mega_engineering_core

- Objects: 1269
- Dependency edges: 3731
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
- Dependency edges: 664
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

## gigas_special_resource_core

- Objects: 174
- Dependency edges: 314
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

- Objects: 59
- Dependency edges: 121
- Policy rows: 59
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
| `Dreadnought` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/!_giga_placeholder_ships.txt` |
| `Flagship` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/!_giga_placeholder_ships.txt` |
| `large_ship_carrier_swarm` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/03_swarm_ships.txt` |
| `rs_carrier` | ship_size | parent_ai_absent | design_ship | `common/ship_sizes/!_giga_placeholder_ships.txt` |

## esc_component_route

- Objects: 888
- Dependency edges: 2244
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

- Objects: 1691
- Dependency edges: 2884
- Policy rows: 1691
- Manual/external dependency targets: 464

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

- Objects: 637
- Dependency edges: 1231
- Policy rows: 637
- Manual/external dependency targets: 332

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

## fallen_empire_benchmark_route

- Objects: 854
- Dependency edges: 2049
- Policy rows: 854
- Manual/external dependency targets: 1043

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
