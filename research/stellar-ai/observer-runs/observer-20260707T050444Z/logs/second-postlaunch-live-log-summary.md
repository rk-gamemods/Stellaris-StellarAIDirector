# Stellaris Log Summary

Files: 2
Entries: 220932
Raw entry lines: 225508
Families: 115183
Groups: 121424

## Severity Counts

| severity | entries |
| --- | ---: |
| error | 18317 |
| fatal | 127 |
| info | 202488 |

## Top Families

### 1. 1547x `trigger.cpp:<line>` [error]

Family: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218139` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223814` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218139`-`218141` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:1366(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218142`-`218144` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1352(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 164x `namelist.cpp:<line>` [error]

Family: `namelist.cpp:<line>: Error: Failed Reading Ship Names!`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:14938` at `01:29:28`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15709` at `01:29:29`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:14938`-`14940` at `01:29:28`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:wormhole_station
	common/name_lists/AS01.txt(41)
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:14941`-`14943` at `01:29:28`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:terraform_station
	common/name_lists/AS01.txt(42)
```

### 3. 152x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference fe_escort from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213983` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218008` at `01:30:24`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213983`-`213983` at `01:30:22`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/nsc_thrusters.txt:234(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214332`-`214332` at `01:30:22`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/esc_components_thrusters.txt:437(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 4. 133x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225081` at `01:30:47`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225298` at `01:30:47`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225081`-`225081` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4257 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7529
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225082`-`225082` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/zzz_giga_overwrites.txt:191 @ scripted effect activate_behemoth_superweapon at file: events/biogenesis_crisis_events.txt line: 3378
```

### 5. 124x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference starbase_battlefortress from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213803` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:216850` at `01:30:24`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213803`-`213803` at `01:30:22`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:412 @ in scripted trigger ESC_ship_uses_starbase_computers at file: common/component_templates/esc_components_computers.txt:995(inline_script) common/inline_scripts/ship_components_general/esc_inlines_combat_computers.txt:13(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213942`-`213942` at `01:30:22`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:219 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_leviathans.txt:623(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 6. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference att from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214246` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218009` at `01:30:24`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214246`-`214246` at `01:30:22`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 758
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214303`-`214303` at `01:30:22`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 964
```

### 7. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference conquistador from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214247` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218010` at `01:30:24`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214247`-`214247` at `01:30:22`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 758
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214304`-`214304` at `01:30:22`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 964
```

### 8. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_hive_farmers]! file`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218182` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223802` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218182`-`218182` at `01:30:24`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_05_hair.txt line: 301
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218215`-`218215` at `01:30:24`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_01_hair.txt line: 1489
```

### 9. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_mutualistic_behavior]! file`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218151` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223812` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218151`-`218151` at `01:30:24`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_female_02_hair.txt line: 800
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218178`-`218178` at `01:30:24`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_male_03_hair.txt line: 2639
```

### 10. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_parasitic_alien]! file`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218410` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223791` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218410`-`218410` at `01:30:24`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_male_05_hair.txt line: 467
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218476`-`218476` at `01:30:24`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_female_05_hair.txt line: 341
```

### 11. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [vbp_hive_mind]! file`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218138` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223739` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218138`-`218138` at `01:30:24`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_male_05_hair.txt line: 385
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218192`-`218192` at `01:30:24`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_female_03_hair.txt line: 1307
```

### 12. 99x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference juggernaut_nosh from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213943` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:216851` at `01:30:24`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213943`-`213943` at `01:30:22`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_leviathans.txt:623(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213993`-`213993` at `01:30:22`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_kinetics.txt:3208(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 13. 92x `dlc.cpp:<line>` [error]

Family: `dlc.cpp:<line>: Invalid supported_version`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:2` at `01:28:21`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:93` at `01:28:22`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:2`-`2` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3`-`3` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1199002146.mod line: 9
```

### 14. 92x `job_type.cpp:<line>` [error]

Family: `job_type.cpp:<line>: Missing job Localization Key`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15760` at `01:29:33`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15889` at `01:29:34`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15760`-`15760` at `01:29:33`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_desc
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:15761`-`15761` at `01:29:33`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_minerals_desc
```

### 15. 90x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference escortcarrier from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213891` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218011` at `01:30:24`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213891`-`213891` at `01:30:22`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213952`-`213952` at `01:30:22`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 395
```

### 16. 89x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference artemis from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213994` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:216758` at `01:30:24`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213994`-`213994` at `01:30:22`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:98 @ in scripted trigger ESC_ship_uses_destroyer_reactors at file: common/component_templates/esc_components_reactors_bio.txt:979(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:214132`-`214132` at `01:30:22`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:98 @ in scripted trigger ESC_ship_uses_destroyer_reactors at file: common/component_templates/esc_components_reactors.txt:350(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```


## Top Exact Groups

### 1. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218208` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223768` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218208`-`218210` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:270(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218227`-`218229` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:4145(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218219` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223809` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218219`-`218221` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:4516(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218288`-`218290` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:2334(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 3. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218189` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223799` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218189`-`218191` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:649(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218242`-`218244` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:1449(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 4. 102x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218145` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223795` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218145`-`218147` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:1862(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218148`-`218150` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:1260(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 5. 92x `dlc.cpp:<line>` [error]

Signature: `dlc.cpp:<line>: Invalid supported_version in file: mod/ugc_<id>.mod line: <n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:2` at `01:28:21`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:93` at `01:28:22`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:2`-`2` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:3`-`3` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1199002146.mod line: 9
```

### 6. 92x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218172` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223751` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218172`-`218174` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:410(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218280`-`218282` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:186(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 7. 88x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218142` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223780` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218142`-`218144` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1352(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218196`-`218198` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:957(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 8. 80x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218179` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223803` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218179`-`218181` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:869(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218442`-`218444` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:756(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 9. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213775` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:215057` at `01:30:23`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213775`-`213775` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213776`-`213776` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 291
```

### 10. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213795` at `01:30:22`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:215066` at `01:30:23`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213795`-`213795` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 419
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:213813`-`213813` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 598
```

### 11. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218158` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223720` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218158`-`218158` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195]: Error in scripted trigger, cannot find: has_job
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218159`-`218159` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 291]: Error in scripted trigger, cannot find: has_job
```

### 12. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218206` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223772` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218206`-`218206` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 419]: Error in scripted trigger, cannot find: has_job
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218397`-`218397` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 414]: Error in scripted trigger, cannot find: has_job
```

### 13. 72x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218338` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223764` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218338`-`218340` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:496(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218366`-`218368` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:595(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 14. 68x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:<n>(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218203` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223748` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218203`-`218205` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:107(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218322`-`218324` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:216(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 15. 60x `parser_deferred_database_objects.cpp:<line>` [error]

Signature: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt:<n> @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:<n> @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:<n> @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:<n> @ scripted effect giga_cosmogenesis_effect at file: events/giga_02`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225081` at `01:30:47`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225298` at `01:30:47`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225081`-`225081` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4257 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7529
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:225084`-`225084` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4200 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7680
```

### 16. 60x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218313` at `01:30:24`
Last: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:223814` at `01:30:25`

Samples:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218313`-`218315` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:1316(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log:218384`-`218386` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:744(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```
