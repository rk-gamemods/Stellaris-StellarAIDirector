# Stellar AI Director Research Capacity

This is a deterministic active-stack capacity inventory. It resolves winning active-stack job definitions, building job slots, direct building output/upkeep, and building upgrade chains. Job triggered resource blocks are included in the optimistic output columns and should be treated as maximum-potential math, not runtime proof.

Job-producing modifiers are normalized from Stellaris 4.x workforce units using 100 workforce = 1 full job equivalent. Raw workforce totals are retained in the building CSV.

- Jobs indexed: 501
- Buildings indexed: 826
- Districts/zones indexed: 547
- Buildings with resolved research output: 135
- Districts/zones with net consumer-goods output: 8
- Technologies with research-relevant modifiers indexed: 18
- Source roots include vanilla at `C:\Steam\steamapps\common\Stellaris` plus enabled launcher mods.
- Plan rows include base and building-modifier-adjusted research/upkeep. Technology rows are inventoried but not auto-applied to colony plans yet.

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
