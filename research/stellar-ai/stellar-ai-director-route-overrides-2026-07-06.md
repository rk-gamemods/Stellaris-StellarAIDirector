# Stellar AI Director Route Override Report

Generated full-object override surfaces. These are actual mod behavior changes, not atlas-only evidence.

Load-safety guard: generated override files copy required source-local `@variables` from parent/vanilla scripted variables and strip optional absent `pc_magnetar` placement references from copied Gigas megastructure starts when that Real Space planet class is not present in the supported source inventory.

| route | object | type | parent strategy | source AI | generated file | source |
| --- | --- | --- | --- | --- | --- | --- |
| mega_engineering_core | `tech_mega_engineering` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/00_megastructures.txt` |
| mega_shipyard_core | `tech_mega_shipyard` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/00_megastructures.txt` |
| planetcraft_route | `giga_tech_planet_assembly` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_01_physics.txt` |
| war_moon_route | `giga_tech_lunar_assembly` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_01_physics.txt` |
| war_moon_route | `giga_tech_war_moon_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_03_engineering.txt` |
| war_moon_route | `giga_tech_war_moon_2` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_03_engineering.txt` |
| war_moon_route | `giga_tech_war_moon_sections` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_03_engineering.txt` |
| systemcraft_route | `giga_tech_war_system_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_05_weightless.txt` |
| systemcraft_route | `giga_tech_war_system_2` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_01_physics.txt` |
| systemcraft_route | `giga_tech_war_system_3` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_01_physics.txt` |
| systemcraft_route | `giga_tech_war_system_4` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_01_physics.txt` |
| systemcraft_route | `giga_tech_war_system_5` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_01_physics.txt` |
| systemcraft_route | `giga_tech_war_system_6` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_03_engineering.txt` |
| gigas_special_resource_core | `tech_ehof_sentient_tier_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_06_special_project_tech.txt` |
| gigas_special_resource_core | `tech_nm_utilization_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_09_ehof_other.txt` |
| gigas_special_resource_core | `giga_tech_amb_supertensiles` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/giga_17_alternative_mega_build.txt` |
| nsc3_capital_hull_route | `tech_Carrier_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/nsc_technologies.txt` |
| nsc3_capital_hull_route | `tech_Dreadnought_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/nsc_technologies.txt` |
| nsc3_capital_hull_route | `tech_Flagship_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/nsc_technologies.txt` |
| nsc3_capital_hull_route | `tech_heavycarrier_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/nsc_technologies.txt` |
| nsc3_capital_hull_route | `tech_supercarrier_1` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/nsc_technologies.txt` |
| esc_component_route | `esc_tech_dark_matter_power_core_2` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/esc_technology_req_components.txt` |
| esc_component_route | `esc_tech_strikecraft_5` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/esc_technology_strikecraft.txt` |
| esc_component_route | `esc_tech_dreadnought_computer` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/esc_technology_req_components.txt` |
| fallen_empire_benchmark_route | `tech_starbase_6` | technology | parent_ai_partial | yes | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | `common/technology/sbx_3_0_technologies.txt` |
| economy_megastructure_core | `ap_gigastructural_constructs` | ascension_perk | parent_ai_partial | yes | `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt` | `common/ascension_perks/giga_ascension_perks.txt` |
| planetcraft_route | `ap_celestial_printing` | ascension_perk | parent_ai_partial | yes | `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt` | `common/ascension_perks/giga_ascension_perks.txt` |
| conquest_escape_route | `ap_lord_of_war` | ascension_perk | parent_ai_partial | yes | `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt` | `common/ascension_perks/00_ascension_perks.txt` |
| conquest_escape_route | `tr_supremacy_adopt` | tradition | parent_ai_absent | no | `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` | `common/traditions/00_supremacy.txt` |
| economy_megastructure_core | `tr_prosperity_adopt` | tradition | parent_ai_partial | yes | `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` | `common/traditions/00_prosperity.txt` |
| crowded_tall_route | `tr_adaptability_adopt` | tradition | parent_ai_absent | no | `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` | `common/traditions/00_adaptability.txt` |
| crowded_tall_route | `tr_mercantile_adopt` | tradition | parent_ai_partial | yes | `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` | `common/traditions/00_mercantile.txt` |
| economy_megastructure_core | `dyson_sphere_0` | megastructure | parent_ai_partial | yes | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | `common/megastructures/zz_e_dyson_sphere.txt` |
| mega_shipyard_core | `mega_shipyard_0` | megastructure | parent_ai_partial | yes | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | `common/megastructures/zz_e_mega_shipyard.txt` |
| economy_megastructure_core | `neutronium_gigaforge_0` | megastructure | parent_ai_partial | yes | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | `common/megastructures/zz_e_neutronium_gigaforge.txt` |
| economy_megastructure_core | `nidavellir_forge_0` | megastructure | parent_ai_partial | yes | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | `common/megastructures/zz_i_nidavellir_forge.txt` |
| economy_megastructure_core | `matrioshka_brain_0_g_star` | megastructure | parent_ai_partial | yes | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | `common/megastructures/zz_i_matrioshka_brain_revised.txt` |
| planetcraft_route | `planetcraft_printer_0` | megastructure | parent_ai_partial | yes | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | `common/megastructures/zz_i_behemoth_assembly_plant.txt` |
| war_moon_route | `war_moon_0` | megastructure | parent_ai_partial | yes | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | `common/megastructures/zz_e_attack_moon.txt` |
| systemcraft_route | `war_system_0` | megastructure | parent_ai_partial | yes | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | `common/megastructures/zz_i_stellar_systemcraft.txt` |
| fallen_empire_benchmark_route | `esc_starbase_reactor` | starbase_building | parent_ai_complete | yes | `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt` | `common/starbase_buildings/esc_starbase_buildings.txt` |

## Manual Review Blockers

- ESC component templates use internal `key = ...` entries in `common/component_templates`; the current atlas does not model those as top-level loader objects, so this generator does not emit guessed component-template overrides.
- NSC3 hull usage is implemented through technology weights, Mega Shipyard/fleet-throughput economy, and reserve pressure until a source-verified ship-design override surface is added.
- Runtime proof still requires an explicit observer run; static validation proves load-safety and reference integrity only.
