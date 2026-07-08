# Stellaris Log Summary

Files: 2
Entries: 221388
Raw entry lines: 226621
Families: 115337
Groups: 121605

## Severity Counts

| severity | entries |
| --- | ---: |
| error | 18549 |
| fatal | 127 |
| info | 202712 |

## Top Families

### 1. 1547x `trigger.cpp:<line>` [error]

Family: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218138` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223813` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218138`-`218140` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/nsc_thrusters.txt:290(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218141`-`218143` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:2808(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218144`-`218146` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:567(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 164x `namelist.cpp:<line>` [error]

Family: `namelist.cpp:<line>: Error: Failed Reading Ship Names!`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:14938` at `02:10:04`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:15709` at `02:10:06`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:14938`-`14940` at `02:10:04`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:wormhole_station
	common/name_lists/AS01.txt(41)
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:14941`-`14943` at `02:10:04`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:terraform_station
	common/name_lists/AS01.txt(42)
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:14944`-`14946` at `02:10:04`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:outpost_station
	common/name_lists/AS01.txt(44)
```

### 3. 152x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference fe_escort from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213941` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218037` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213941`-`213941` at `02:10:56`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/nsc_thrusters.txt:90(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214000`-`214000` at `02:10:56`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/esc_components_thrusters.txt:107(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214017`-`214017` at `02:10:56`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:322 @ in scripted trigger ESC_ship_uses_battlecruiser_components at file: common/component_templates/nsc_thrusters.txt:320(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters_sr.txt:30(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 4. 133x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225079` at `02:11:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225296` at `02:11:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225079`-`225079` at `02:11:24`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4257 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7529
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225080`-`225080` at `02:11:24`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/02_machine_age_effects.txt:1417 @ scripted effect synth_queen_wipe_system at file: events/machine_age_crisis_events.txt line: 5303
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225081`-`225081` at `02:11:24`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at file: events/!_giga_overwritten_events.txt line: 1134
```

### 5. 132x `trigger.cpp:<line>` [error]

Family: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' | Current Scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225608` at `02:13:09`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:226001` at `02:13:10`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225608`-`225610` at `02:13:09`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:3435(inline_script) common/inline_scripts/ship_components_general/esc_inlines_titanic_standard_bio.txt line: 7
Current Scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225611`-`225613` at `02:13:09`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:3503(inline_script) common/inline_scripts/ship_components_general/esc_inlines_titanic_standard_bio.txt line: 7
Current Scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225614`-`225616` at `02:13:09`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:4074(inline_script) common/inline_scripts/ship_components_general/esc_inlines_titanic_standard_bio.txt line: 7
Current Scope: ship_growth_stage
Supported Scopes: country
```

### 6. 124x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference starbase_battlefortress from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213780` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:216785` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213780`-`213780` at `02:10:56`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:219 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_energy.txt:4299(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213790`-`213790` at `02:10:56`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:48 @ in scripted trigger ESC_ship_uses_big_starbase_components at file: common/component_templates/esc_overwrites_computers_fe_starbase.txt line: 222
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213868`-`213868` at `02:10:56`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:219 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_gravitic.txt:1565(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 7. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference att from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213784` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:217973` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213784`-`213784` at `02:10:56`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 758
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214523`-`214523` at `02:10:56`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:381(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214576`-`214576` at `02:10:56`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:47(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 8. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference conquistador from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213785` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:217974` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213785`-`213785` at `02:10:56`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 758
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214524`-`214524` at `02:10:56`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:381(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214577`-`214577` at `02:10:56`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:47(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 9. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_hive_farmers]! file`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218165` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223735` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218165`-`218165` at `02:10:58`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_03_hair.txt line: 991
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218363`-`218363` at `02:10:58`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_03_hair.txt line: 821
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218376`-`218376` at `02:10:58`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_05_hair.txt line: 516
```

### 10. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_mutualistic_behavior]! file`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218159` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223808` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218159`-`218159` at `02:10:58`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_female_01_hair.txt line: 1923
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218228`-`218228` at `02:10:58`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_female_02_hair.txt line: 615
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218277`-`218277` at `02:10:58`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_female_04_hair.txt line: 1491
```

### 11. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_parasitic_alien]! file`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218244` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223799` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218244`-`218244` at `02:10:58`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_female_02_hair.txt line: 724
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218316`-`218316` at `02:10:58`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_male_01_hair.txt line: 1915
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218329`-`218329` at `02:10:58`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_male_05_hair.txt line: 467
```

### 12. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [vbp_hive_mind]! file`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218170` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223800` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218170`-`218170` at `02:10:58`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_female_02_hair.txt line: 396
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218171`-`218171` at `02:10:58`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_female_03_hair.txt line: 1925
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218284`-`218284` at `02:10:58`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_female_04_hair.txt line: 995
```

### 13. 99x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference juggernaut_nosh from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213781` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:216786` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213781`-`213781` at `02:10:56`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_energy.txt:4299(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213869`-`213869` at `02:10:56`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_gravitic.txt:1565(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213933`-`213933` at `02:10:56`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_energy.txt:3064(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 14. 92x `dlc.cpp:<line>` [error]

Family: `dlc.cpp:<line>: Invalid supported_version`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:2` at `02:08:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:93` at `02:08:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:2`-`2` at `02:08:58`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3`-`3` at `02:08:58`

```text
Invalid supported_version in  file: mod/ugc_1199002146.mod line: 9
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:4`-`4` at `02:08:58`

```text
Invalid supported_version in  file: mod/ugc_1333526620.mod line: 12
```

### 15. 92x `job_type.cpp:<line>` [error]

Family: `job_type.cpp:<line>: Missing job Localization Key`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:15760` at `02:10:09`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:15889` at `02:10:10`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:15760`-`15760` at `02:10:09`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_desc
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:15761`-`15761` at `02:10:09`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_minerals_desc
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:15762`-`15762` at `02:10:09`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_refinery_desc
```

### 16. 90x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference escortcarrier from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213883` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218009` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213883`-`213883` at `02:10:56`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213958`-`213958` at `02:10:56`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 197
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214166`-`214166` at `02:10:56`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:553(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 17. 89x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference artemis from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213792` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:216847` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213792`-`213792` at `02:10:56`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:98 @ in scripted trigger ESC_ship_uses_destroyer_reactors at file: common/component_templates/00_utilities_reactors.txt line: 69
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213991`-`213991` at `02:10:56`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:88 @ in scripted trigger ESC_ship_uses_destroyer_components at file: common/component_templates/esc_components_thrusters.txt:525(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214115`-`214115` at `02:10:56`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:88 @ in scripted trigger ESC_ship_uses_destroyer_components at file: common/component_templates/00_utilities_thrusters.txt line: 726
```

### 18. 84x `ship_size.cpp:<line>` [error]

Family: `ship_size.cpp:<line>: Missing ship size Localization Key`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3971` at `02:10:00`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:4101` at `02:10:00`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3971`-`3971` at `02:10:00`

```text
Missing ship size Localization Key: precursor_colossus
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3972`-`3972` at `02:10:00`

```text
Missing ship size Localization Key: precursor_colossus_plural
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3973`-`3973` at `02:10:00`

```text
Missing ship size Localization Key: sofe_ancient_weapon
```

### 19. 78x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213793` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:215020` at `02:10:57`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213793`-`213793` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 83
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213931`-`213931` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 367
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213950`-`213950` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195
```

### 20. 78x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213788` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:215061` at `02:10:57`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213788`-`213788` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 251
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213870`-`213870` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 234
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213873`-`213873` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 412
```

### 21. 78x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218218` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223759` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218218`-`218218` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 367]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218229`-`218229` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218266`-`218266` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 599]: Error in scripted trigger, cannot find: has_job
```

### 22. 78x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218154` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223739` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218154`-`218154` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 251]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218164`-`218164` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 234]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218179`-`218179` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 290]: Error in scripted trigger, cannot find: has_job
```

### 23. 77x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference ultrajuggernaut from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213957` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218003` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213957`-`213957` at `02:10:56`

```text
Failed to deferred read key reference ultrajuggernaut from database  common/scripted_triggers/esc_ship_size_triggers.txt:366 @ in scripted trigger ESC_ship_uses_flagship_components at file: common/component_templates/nsc_thrusters.txt:362(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters_sr.txt:30(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214347`-`214347` at `02:10:56`

```text
Failed to deferred read key reference ultrajuggernaut from database  common/scripted_triggers/esc_ship_size_triggers.txt:366 @ in scripted trigger ESC_ship_uses_flagship_components at file: common/component_templates/esc_components_thrusters.txt:493(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214562`-`214562` at `02:10:56`

```text
Failed to deferred read key reference ultrajuggernaut from database  common/scripted_triggers/esc_ship_size_triggers.txt:366 @ in scripted trigger ESC_ship_uses_flagship_components at file: common/component_templates/nsc_thrusters.txt:290(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 24. 74x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference SCX_Carrier from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213884` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218010` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213884`-`213884` at `02:10:56`

```text
Failed to deferred read key reference SCX_Carrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:138 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213959`-`213959` at `02:10:56`

```text
Failed to deferred read key reference SCX_Carrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:138 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 197
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214167`-`214167` at `02:10:56`

```text
Failed to deferred read key reference SCX_Carrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:138 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:553(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 25. 74x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference fe_battlecruiser from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213909` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218035` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213909`-`213909` at `02:10:56`

```text
Failed to deferred read key reference fe_battlecruiser from database  common/scripted_triggers/esc_ship_size_triggers.txt:167 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213984`-`213984` at `02:10:56`

```text
Failed to deferred read key reference fe_battlecruiser from database  common/scripted_triggers/esc_ship_size_triggers.txt:167 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 197
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214192`-`214192` at `02:10:56`

```text
Failed to deferred read key reference fe_battlecruiser from database  common/scripted_triggers/esc_ship_size_triggers.txt:167 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:553(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 26. 74x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference ironclad from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214118` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218006` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214118`-`214118` at `02:10:56`

```text
Failed to deferred read key reference ironclad from database  common/scripted_triggers/esc_ship_size_triggers.txt:193 @ in scripted trigger ESC_ship_uses_titan_components at file: common/component_templates/esc_components_thrusters.txt:409(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214199`-`214199` at `02:10:56`

```text
Failed to deferred read key reference ironclad from database  common/scripted_triggers/esc_ship_size_triggers.txt:193 @ in scripted trigger ESC_ship_uses_titan_components at file: common/component_templates/00_utilities_thrusters.txt line: 428
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214210`-`214210` at `02:10:56`

```text
Failed to deferred read key reference ironclad from database  common/scripted_triggers/esc_ship_size_triggers.txt:193 @ in scripted trigger ESC_ship_uses_titan_components at file: common/component_templates/00_utilities_thrusters.txt line: 822
```

### 27. 74x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference rs_heavy_dreadnought_type_a from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213885` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218011` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213885`-`213885` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_a from database  common/scripted_triggers/esc_ship_size_triggers.txt:142 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213960`-`213960` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_a from database  common/scripted_triggers/esc_ship_size_triggers.txt:142 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 197
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214168`-`214168` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_a from database  common/scripted_triggers/esc_ship_size_triggers.txt:142 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:553(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 28. 74x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference rs_heavy_dreadnought_type_b from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213886` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218012` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213886`-`213886` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_b from database  common/scripted_triggers/esc_ship_size_triggers.txt:143 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213961`-`213961` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_b from database  common/scripted_triggers/esc_ship_size_triggers.txt:143 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 197
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214169`-`214169` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_b from database  common/scripted_triggers/esc_ship_size_triggers.txt:143 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:553(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 29. 74x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference rs_heavy_dreadnought_type_c from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213887` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218013` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213887`-`213887` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_c from database  common/scripted_triggers/esc_ship_size_triggers.txt:144 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213962`-`213962` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_c from database  common/scripted_triggers/esc_ship_size_triggers.txt:144 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 197
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214170`-`214170` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_c from database  common/scripted_triggers/esc_ship_size_triggers.txt:144 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:553(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 30. 74x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference rs_heavy_dreadnought_type_d from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213888` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218014` at `02:10:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213888`-`213888` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_d from database  common/scripted_triggers/esc_ship_size_triggers.txt:145 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213963`-`213963` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_d from database  common/scripted_triggers/esc_ship_size_triggers.txt:145 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 197
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214171`-`214171` at `02:10:56`

```text
Failed to deferred read key reference rs_heavy_dreadnought_type_d from database  common/scripted_triggers/esc_ship_size_triggers.txt:145 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:553(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```


## Top Exact Groups

### 1. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218202` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223796` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218202`-`218204` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:4895(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218208`-`218210` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:203(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218238`-`218240` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:1523(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218173` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223813` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218173`-`218175` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:396(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218260`-`218262` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:238(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218323`-`218325` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:2703(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 3. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218156` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223718` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218156`-`218158` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:1170(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218186`-`218188` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:733(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218251`-`218253` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:1170(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 4. 102x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218166` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223809` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218166`-`218168` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:2851(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218219`-`218221` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:1862(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218222`-`218224` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:2191(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 5. 92x `dlc.cpp:<line>` [error]

Signature: `dlc.cpp:<line>: Invalid supported_version in file: mod/ugc_<id>.mod line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:2` at `02:08:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:93` at `02:08:58`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:2`-`2` at `02:08:58`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3`-`3` at `02:08:58`

```text
Invalid supported_version in  file: mod/ugc_1199002146.mod line: 9
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:4`-`4` at `02:08:58`

```text
Invalid supported_version in  file: mod/ugc_1333526620.mod line: 12
```

### 6. 92x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218161` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223750` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218161`-`218163` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:266(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218225`-`218227` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:514(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218271`-`218273` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:206(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 7. 88x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218310` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223771` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218310`-`218312` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1759(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218481`-`218483` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1598(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218499`-`218501` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1678(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 8. 80x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218141` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223805` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218141`-`218143` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:2808(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218334`-`218336` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:1098(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218402`-`218404` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:290(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 9. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213793` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:215020` at `02:10:57`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213793`-`213793` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 83
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213931`-`213931` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 367
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213950`-`213950` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195
```

### 10. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213788` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:215061` at `02:10:57`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213788`-`213788` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 251
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213870`-`213870` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 234
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213873`-`213873` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 412
```

### 11. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218218` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223759` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218218`-`218218` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 367]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218229`-`218229` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218266`-`218266` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 599]: Error in scripted trigger, cannot find: has_job
```

### 12. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218154` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223739` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218154`-`218154` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 251]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218164`-`218164` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 234]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218179`-`218179` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 290]: Error in scripted trigger, cannot find: has_job
```

### 13. 72x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218176` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223616` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218176`-`218178` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:931(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218211`-`218213` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:22(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218241`-`218243` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:553(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 14. 68x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:<n>(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218144` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223756` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218144`-`218146` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:567(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218214`-`218216` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:47(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218245`-`218247` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:479(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 15. 61x `eventcommands.cpp:<line>` [info]

Signature: `eventcommands.cpp:<line>: Event first_contact.1 added info about event selection. selectedOption 0, human -1, playerEventId <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:19` at `02:20:40`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:183` at `02:23:00`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:19`-`19` at `02:20:40`

```text
Event first_contact.1 added info about event selection. selectedOption 0, human -1, playerEventId 10
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:20`-`20` at `02:20:48`

```text
Event first_contact.1 added info about event selection. selectedOption 0, human -1, playerEventId 13
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:23`-`23` at `02:20:49`

```text
Event first_contact.1 added info about event selection. selectedOption 0, human -1, playerEventId 15
```

### 16. 60x `parser_deferred_database_objects.cpp:<line>` [error]

Signature: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt:<n> @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:<n> @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:<n> @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:<n> @ scripted effect giga_cosmogenesis_effect at file: events/giga_02`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225079` at `02:11:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225296` at `02:11:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225079`-`225079` at `02:11:24`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4257 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7529
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225097`-`225097` at `02:11:24`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4584 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4238 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7700
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:225101`-`225101` at `02:11:24`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4219 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7635
```

### 17. 60x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218254` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223801` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218254`-`218256` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:1364(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218353`-`218355` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:863(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218408`-`218410` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:1137(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 18. 60x `section.cpp:<line>` [info]

Signature: `section.cpp:<line>: section has no entity. file common/section_templates/explorationship.txt Line <n>-<n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:64933` at `02:10:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:76412` at `02:10:22`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:64933`-`64933` at `02:10:22`

```text
section has no entity. file common/section_templates/explorationship.txt Line 18-37
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:65131`-`65131` at `02:10:22`

```text
section has no entity. file common/section_templates/explorationship.txt Line 39-68
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:65328`-`65328` at `02:10:22`

```text
section has no entity. file common/section_templates/explorationship.txt Line 70-94
```

### 19. 52x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218196` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223650` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218196`-`218198` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:2228(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218359`-`218361` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:2299(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218391`-`218393` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:2299(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 20. 47x `economic_unit_template.cpp:<line>` [error]

Signature: `economic_unit_template.cpp:<line>: Failed to read key reference starbase_stations from database file: common/ship_sizes/!_giga_placeholder_ships.txt:<n>(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3975` at `02:10:00`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:4099` at `02:10:00`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3975`-`3975` at `02:10:00`

```text
Failed to read key reference starbase_stations from database  file: common/ship_sizes/!_giga_placeholder_ships.txt:110(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: 3
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3976`-`3976` at `02:10:00`

```text
Failed to read key reference starbase_stations from database  file: common/ship_sizes/!_giga_placeholder_ships.txt:111(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: 3
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:3977`-`3977` at `02:10:00`

```text
Failed to read key reference starbase_stations from database  file: common/ship_sizes/!_giga_placeholder_ships.txt:112(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: 3
```

### 21. 44x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218189` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223763` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218189`-`218191` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:1217(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218313`-`218315` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:448(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218317`-`218319` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:1111(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 22. 43x `section.cpp:<line>` [info]

Signature: `section.cpp:<line>: section has no entity. file common/section_templates/Flagship.txt Line <n>-<n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:38019` at `02:10:21`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:46233` at `02:10:21`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:38019`-`38019` at `02:10:21`

```text
section has no entity. file common/section_templates/Flagship.txt Line 7-83
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:38213`-`38213` at `02:10:21`

```text
section has no entity. file common/section_templates/Flagship.txt Line 87-183
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:38407`-`38407` at `02:10:21`

```text
section has no entity. file common/section_templates/Flagship.txt Line 187-291
```

### 23. 42x `effect.cpp:<line>` [error]

Signature: `effect.cpp:<line>: Error: "Unexpected token: none, near line: <n> | " in file: "common/button_effects/giga_megastructure_view.txt:<n>(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_normal_part.txt:<n>(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_grow_ship.txt" near line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:16172` at `02:10:16`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:16254` at `02:10:16`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:16172`-`16173` at `02:10:16`

```text
Error: "Unexpected token: none, near line: 65
" in file: "common/button_effects/giga_megastructure_view.txt:67(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_normal_part.txt:21(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_grow_ship.txt" near line: 65
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:16174`-`16175` at `02:10:16`

```text
Error: "Unexpected token: none, near line: 65
" in file: "common/button_effects/giga_megastructure_view.txt:67(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_normal_part.txt:43(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_grow_ship.txt" near line: 65
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:16176`-`16177` at `02:10:16`

```text
Error: "Unexpected token: none, near line: 60
" in file: "common/button_effects/giga_megastructure_view.txt:67(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_normal_part.txt:99(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_grow_ship.txt" near line: 60
```

### 24. 42x `parser_deferred_database_objects.cpp:<line>` [error]

Signature: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference none from database file: common/button_effects/giga_megastructure_view.txt:<n>(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_normal_part.txt:<n>(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_grow_ship.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:212406` at `02:10:29`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:212447` at `02:10:29`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:212406`-`212406` at `02:10:29`

```text
Failed to deferred read key reference none from database  file: common/button_effects/giga_megastructure_view.txt:67(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_normal_part.txt:21(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_grow_ship.txt line: 22
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:212407`-`212407` at `02:10:29`

```text
Failed to deferred read key reference none from database  file: common/button_effects/giga_megastructure_view.txt:67(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_normal_part.txt:43(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_grow_ship.txt line: 22
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:212408`-`212408` at `02:10:29`

```text
Failed to deferred read key reference none from database  file: common/button_effects/giga_megastructure_view.txt:67(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_normal_part.txt:99(inline_script) common/inline_scripts/megastructures/big_vat/big_vat_grow_ship.txt line: 22
```

### 25. 42x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/vamp_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213786` at `02:10:56`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214997` at `02:10:57`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213786`-`213786` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/vamp_clothes_01.txt line: 174
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:213955`-`213955` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/vamp_clothes_01.txt line: 44
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:214013`-`214013` at `02:10:56`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/vamp_clothes_01.txt line: 22
```

### 26. 42x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/vamp_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218153` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223516` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218153`-`218153` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/vamp_clothes_01.txt line: 174]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218234`-`218234` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/vamp_clothes_01.txt line: 44]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218371`-`218371` at `02:10:58`

```text
[ file: gfx/portraits/asset_selectors/vamp_clothes_01.txt line: 161]: Error in scripted trigger, cannot find: has_job
```

### 27. 40x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_gravitic.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218293` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223682` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218293`-`218295` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_gravitic.txt:1168(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218417`-`218419` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_gravitic.txt:960(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218514`-`218516` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_gravitic.txt:1168(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 28. 40x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_tesla.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218149` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223477` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218149`-`218151` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_tesla.txt:1777(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218192`-`218194` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_tesla.txt:1245(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218231`-`218233` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_tesla.txt:187(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 29. 40x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/nsc_thrusters.txt:<n>(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218138` at `02:10:58`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:223664` at `02:10:59`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218138`-`218140` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/nsc_thrusters.txt:290(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218489`-`218491` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/nsc_thrusters.txt:90(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-error.log:218893`-`218895` at `02:10:58`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/nsc_thrusters.txt:204(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 30. 38x `eventcommands.cpp:<line>` [info]

Signature: `eventcommands.cpp:<line>: Event first_contact.<n> added info about event selection. selectedOption 0, human -1, playerEventId <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:21` at `02:20:48`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:176` at `02:22:57`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:21`-`21` at `02:20:48`

```text
Event first_contact.5000 added info about event selection. selectedOption 0, human -1, playerEventId 18
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:22`-`22` at `02:20:49`

```text
Event first_contact.5000 added info about event selection. selectedOption 0, human -1, playerEventId 11
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\observer-control-game.log:25`-`25` at `02:20:50`

```text
Event first_contact.5000 added info about event selection. selectedOption 0, human -1, playerEventId 19
```
