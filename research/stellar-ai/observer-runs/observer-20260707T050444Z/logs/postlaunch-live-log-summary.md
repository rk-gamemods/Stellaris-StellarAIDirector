# Stellaris Log Summary

Files: 2
Entries: 221122
Raw entry lines: 225698
Families: 115188
Groups: 121446

## Severity Counts

| severity | entries |
| --- | ---: |
| error | 18507 |
| fatal | 127 |
| info | 202488 |

## Top Families

### 1. 1547x `trigger.cpp:<line>` [error]

Family: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218138` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223820` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218138`-`218140` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:2758(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218143`-`218145` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:1206(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 164x `namelist.cpp:<line>` [error]

Family: `namelist.cpp:<line>: Error: Failed Reading Ship Names!`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:14938` at `01:19:40`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15709` at `01:19:43`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:14938`-`14940` at `01:19:40`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:wormhole_station
	common/name_lists/AS01.txt(41)
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:14941`-`14943` at `01:19:40`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:terraform_station
	common/name_lists/AS01.txt(42)
```

### 3. 152x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference fe_escort from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213905` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218010` at `01:20:55`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213905`-`213905` at `01:20:53`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/esc_components_thrusters.txt:107(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214203`-`214203` at `01:20:53`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/nsc_thrusters.txt:306(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters_sr.txt:30(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 4. 133x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225269` at `01:21:19`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225488` at `01:21:20`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225269`-`225269` at `01:21:19`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4584 @ scripted effect destroy_star_system at file: events/machine_age_crisis_events.txt line: 3203
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225270`-`225270` at `01:21:19`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4584 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4219 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7529
```

### 5. 124x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference starbase_battlefortress from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213860` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:216847` at `01:20:55`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213860`-`213860` at `01:20:53`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:219 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_archaeo.txt line: 3522
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213863`-`213863` at `01:20:53`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:219 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_kinetics.txt:3335(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 6. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference att from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213895` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:217976` at `01:20:55`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213895`-`213895` at `01:20:53`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 362
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214061`-`214061` at `01:20:53`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:47(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 7. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference conquistador from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213896` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:217977` at `01:20:55`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213896`-`213896` at `01:20:53`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 362
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214062`-`214062` at `01:20:53`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:47(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 8. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_hive_farmers]! file`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218320` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223810` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218320`-`218320` at `01:20:56`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_03_hair.txt line: 118
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218363`-`218363` at `01:20:56`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_male_02_hair.txt line: 555
```

### 9. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_mutualistic_behavior]! file`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218152` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223770` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218152`-`218152` at `01:20:56`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_female_05_hair.txt line: 34
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218250`-`218250` at `01:20:56`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_female_04_hair.txt line: 1491
```

### 10. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_parasitic_alien]! file`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218142` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223716` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218142`-`218142` at `01:20:56`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_male_04_hair.txt line: 1695
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218268`-`218268` at `01:20:56`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_female_02_hair.txt line: 619
```

### 11. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [vbp_hive_mind]! file`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218365` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223727` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218365`-`218365` at `01:20:56`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_female_04_hair.txt line: 825
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218371`-`218371` at `01:20:56`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_female_04_hair.txt line: 919
```

### 12. 99x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference juggernaut_nosh from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213861` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:216848` at `01:20:55`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213861`-`213861` at `01:20:53`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_archaeo.txt line: 3522
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213864`-`213864` at `01:20:53`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_kinetics.txt:3335(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 13. 92x `dlc.cpp:<line>` [error]

Family: `dlc.cpp:<line>: Invalid supported_version`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:2` at `01:17:52`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:93` at `01:17:53`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:2`-`2` at `01:17:52`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3`-`3` at `01:17:52`

```text
Invalid supported_version in  file: mod/ugc_1199002146.mod line: 9
```

### 14. 92x `job_type.cpp:<line>` [error]

Family: `job_type.cpp:<line>: Missing job Localization Key`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15760` at `01:19:48`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15889` at `01:19:49`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15760`-`15760` at `01:19:48`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_desc
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15761`-`15761` at `01:19:48`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_minerals_desc
```

### 15. 92x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference major_orbital from database common/scripted_effects/zzz_staid_gigas_habitat_compat_effects.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223906` at `01:21:04`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:224088` at `01:21:04`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223906`-`223906` at `01:21:04`

```text
Failed to deferred read key reference major_orbital from database  common/scripted_effects/zzz_staid_gigas_habitat_compat_effects.txt:12 @ scripted effect science_kilo_update_orbital_effect at file: common/megastructures/zz_c_atmospheric_storm_observatory.txt line: 250
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223908`-`223908` at `01:21:04`

```text
Failed to deferred read key reference major_orbital from database  common/scripted_effects/zzz_staid_gigas_habitat_compat_effects.txt:21 @ scripted effect science_kilo_update_orbital_effect at file: common/megastructures/zz_c_atmospheric_storm_observatory.txt line: 250
```

### 16. 92x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference minor_orbital from database common/scripted_effects/zzz_staid_gigas_habitat_compat_effects.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223907` at `01:21:04`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:224089` at `01:21:04`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223907`-`223907` at `01:21:04`

```text
Failed to deferred read key reference minor_orbital from database  common/scripted_effects/zzz_staid_gigas_habitat_compat_effects.txt:13 @ scripted effect science_kilo_update_orbital_effect at file: common/megastructures/zz_c_atmospheric_storm_observatory.txt line: 250
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223909`-`223909` at `01:21:04`

```text
Failed to deferred read key reference minor_orbital from database  common/scripted_effects/zzz_staid_gigas_habitat_compat_effects.txt:22 @ scripted effect science_kilo_update_orbital_effect at file: common/megastructures/zz_c_atmospheric_storm_observatory.txt line: 250
```

### 17. 90x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference escortcarrier from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213832` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218011` at `01:20:55`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213832`-`213832` at `01:20:53`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 1000
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213996`-`213996` at `01:20:53`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:553(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 18. 89x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference artemis from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213828` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:216810` at `01:20:55`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213828`-`213828` at `01:20:53`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:88 @ in scripted trigger ESC_ship_uses_destroyer_components at file: common/component_templates/00_utilities_thrusters.txt line: 928
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213870`-`213870` at `01:20:53`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:98 @ in scripted trigger ESC_ship_uses_destroyer_reactors at file: common/component_templates/00_utilities_reactors.txt line: 377
```

### 19. 84x `ship_size.cpp:<line>` [error]

Family: `ship_size.cpp:<line>: Missing ship size Localization Key`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3971` at `01:19:32`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:4101` at `01:19:33`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3971`-`3971` at `01:19:32`

```text
Missing ship size Localization Key: precursor_colossus
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3972`-`3972` at `01:19:32`

```text
Missing ship size Localization Key: precursor_colossus_plural
```

### 20. 78x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213793` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:215067` at `01:20:54`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213793`-`213793` at `01:20:53`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 408
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213794`-`213794` at `01:20:53`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 378
```


## Top Exact Groups

### 1. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218314` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223680` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218314`-`218316` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:1832(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218343`-`218345` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:1664(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218199` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223814` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218199`-`218201` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:2334(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218227`-`218229` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:2802(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 3. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218180` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223807` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218180`-`218182` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:36(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218193`-`218195` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:2467(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 4. 102x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218138` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223800` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218138`-`218140` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:2758(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218157`-`218159` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:2851(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 5. 92x `dlc.cpp:<line>` [error]

Signature: `dlc.cpp:<line>: Invalid supported_version in file: mod/ugc_<id>.mod line: <n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:2` at `01:17:52`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:93` at `01:17:53`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:2`-`2` at `01:17:52`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3`-`3` at `01:17:52`

```text
Invalid supported_version in  file: mod/ugc_1199002146.mod line: 9
```

### 6. 92x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218146` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223764` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218146`-`218148` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:370(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218265`-`218267` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:850(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 7. 88x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218149` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223783` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218149`-`218151` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1576(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218166`-`218168` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1237(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 8. 80x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218163` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223751` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218163`-`218165` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:756(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218213`-`218215` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:756(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 9. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213793` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:215067` at `01:20:54`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213793`-`213793` at `01:20:53`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 408
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213794`-`213794` at `01:20:53`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 378
```

### 10. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213880` at `01:20:53`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:215075` at `01:20:54`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213880`-`213880` at `01:20:53`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 412
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213938`-`213938` at `01:20:53`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 563
```

### 11. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218156` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223787` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218156`-`218156` at `01:20:56`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 378]: Error in scripted trigger, cannot find: has_job
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218169`-`218169` at `01:20:56`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 600]: Error in scripted trigger, cannot find: has_job
```

### 12. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218246` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223645` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218246`-`218246` at `01:20:56`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 412]: Error in scripted trigger, cannot find: has_job
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218352`-`218352` at `01:20:56`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 563]: Error in scripted trigger, cannot find: has_job
```

### 13. 72x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218153` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223488` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218153`-`218155` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:553(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218400`-`218402` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:186(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 14. 68x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:<n>(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218230` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223705` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218230`-`218232` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:186(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218340`-`218342` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:47(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 15. 60x `parser_deferred_database_objects.cpp:<line>` [error]

Signature: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt:<n> @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:<n> @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:<n> @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:<n> @ scripted effect giga_cosmogenesis_effect at file: events/giga_02`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225270` at `01:21:19`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225485` at `01:21:20`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225270`-`225270` at `01:21:19`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4584 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4219 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7529
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225272`-`225272` at `01:21:19`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4584 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4238 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7700
```

### 16. 60x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218143` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223788` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218143`-`218145` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:1206(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218255`-`218257` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:1115(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 17. 60x `section.cpp:<line>` [info]

Signature: `section.cpp:<line>: section has no entity. file common/section_templates/explorationship.txt Line <n>-<n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:64933` at `01:20:08`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:76412` at `01:20:08`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:64933`-`64933` at `01:20:08`

```text
section has no entity. file common/section_templates/explorationship.txt Line 18-37
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:65131`-`65131` at `01:20:08`

```text
section has no entity. file common/section_templates/explorationship.txt Line 39-68
```

### 18. 52x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218296` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223817` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218296`-`218298` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:1221(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218321`-`218323` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:1137(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 19. 47x `economic_unit_template.cpp:<line>` [error]

Signature: `economic_unit_template.cpp:<line>: Failed to read key reference starbase_stations from database file: common/ship_sizes/!_giga_placeholder_ships.txt:<n>(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: <n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3975` at `01:19:32`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:4099` at `01:19:33`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3975`-`3975` at `01:19:32`

```text
Failed to read key reference starbase_stations from database  file: common/ship_sizes/!_giga_placeholder_ships.txt:110(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: 3
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3976`-`3976` at `01:19:32`

```text
Failed to read key reference starbase_stations from database  file: common/ship_sizes/!_giga_placeholder_ships.txt:111(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: 3
```

### 20. 44x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218353` at `01:20:56`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223811` at `01:20:56`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218353`-`218355` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:281(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218464`-`218466` at `01:20:56`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:1111(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```
