# Stellar AI Director Research Capacity

This is a deterministic active-stack capacity inventory. It resolves winning active-stack job definitions, building job slots, direct building output/upkeep, and building upgrade chains. Job triggered resource blocks are included in the optimistic output columns and should be treated as maximum-potential math, not runtime proof.

Job-producing modifiers are normalized from Stellaris 4.x workforce units using 100 workforce = 1 full job equivalent. Raw workforce totals are retained in the building CSV.

- Jobs indexed: 501
- Buildings indexed: 826
- Buildings with resolved research output: 55
- Source roots include vanilla at `C:\Steam\steamapps\common\Stellaris` plus enabled launcher mods.

## Top Research Buildings

| rank | building | research/month | jobs | mod |
| --- | --- | ---: | ---: | --- |
| 1 | `building_mem_lost_emperor_ancient_palace` | 1500.0 | 8.8 | More Events Mod |
| 2 | `building_master_archive` | 300.0 | 10.0 | Stellaris vanilla |
| 3 | `building_giga_institute_2` | 81.0 | 0 | Gigastructural Engineering & More (4.4) |
| 4 | `building_giga_supercomputer_2` | 81.0 | 0 | Gigastructural Engineering & More (4.4) |
| 5 | `building_fe_lab_2` | 60.0 | 0 | Stellaris vanilla |
| 6 | `building_giga_iodizium_research` | 60.0 | 0 | Gigastructural Engineering & More (4.4) |
| 7 | `building_giga_institute_1` | 54.0 | 0 | Gigastructural Engineering & More (4.4) |
| 8 | `building_giga_supercomputer_1` | 54.0 | 0 | Gigastructural Engineering & More (4.4) |
| 9 | `building_mp_primitive_particle_accelerator` | 25.0 | 0 | More Primitives |
| 10 | `building_mem_asp_spire` | 24.0 | 0 | More Events Mod |
| 11 | `holding_mem_asp_spire` | 24.0 | 0 | More Events Mod |
| 12 | `building_defense_nexus_capacity` | 20.0 | 0 | Gigastructural Engineering & More (4.4) |
| 13 | `building_mp_primitive_holographic_domes` | 20.0 | 0 | More Primitives |
| 14 | `building_mp_primitive_satellite_dish` | 20.0 | 0 | More Primitives |
| 15 | `building_mp_primitive_test_site` | 20.0 | 1.0 | More Primitives |
| 16 | `building_organic_paradise` | 20.0 | 30.0 | Stellaris vanilla |
| 17 | `building_organic_sanctuary` | 20.0 | 15.0 | Stellaris vanilla |
| 18 | `building_passenger_dorms` | 20.0 | 5.0 | Stellaris vanilla |
| 19 | `building_passenger_paradise` | 20.0 | 15.0 | Stellaris vanilla |
| 20 | `esc_building_dragon_hatchery` | 20.0 | 0 | Extra Ship Components NEXT |

## Colony Scenarios

| scenario | research/month | colonies for 3000 |
| --- | ---: | ---: |
| raw_top_terminal_top_1_in_6_slots | 1500.0 | 2 |
| raw_top_terminal_top_3_in_6_slots | 1881.0 | 2 |
| raw_top_terminal_top_6_in_6_slots | 2082.0 | 2 |
| raw_top_terminal_top_1_in_8_slots | 1500.0 | 2 |
| raw_top_terminal_top_3_in_8_slots | 1881.0 | 2 |
| raw_top_terminal_top_8_in_8_slots | 2131.0 | 2 |
| raw_top_terminal_top_1_in_10_slots | 1500.0 | 2 |
| raw_top_terminal_top_3_in_10_slots | 1881.0 | 2 |
| raw_top_terminal_top_10_in_10_slots | 2175.0 | 2 |
| raw_top_terminal_top_1_in_12_slots | 1500.0 | 2 |
| raw_top_terminal_top_3_in_12_slots | 1881.0 | 2 |
| raw_top_terminal_top_12_in_12_slots | 2215.0 | 2 |
| repeatable_candidate_terminal_top_1_in_6_slots | 300.0 | 10 |
| repeatable_candidate_terminal_top_3_in_6_slots | 462.0 | 7 |
| repeatable_candidate_terminal_top_6_in_6_slots | 562.0 | 6 |
| repeatable_candidate_terminal_top_1_in_8_slots | 300.0 | 10 |
| repeatable_candidate_terminal_top_3_in_8_slots | 462.0 | 7 |
| repeatable_candidate_terminal_top_8_in_8_slots | 596.0 | 6 |
| repeatable_candidate_terminal_top_1_in_10_slots | 300.0 | 10 |
| repeatable_candidate_terminal_top_3_in_10_slots | 462.0 | 7 |
| repeatable_candidate_terminal_top_10_in_10_slots | 626.0 | 5 |
| repeatable_candidate_terminal_top_1_in_12_slots | 300.0 | 10 |
| repeatable_candidate_terminal_top_3_in_12_slots | 462.0 | 7 |
| repeatable_candidate_terminal_top_12_in_12_slots | 656.0 | 5 |
