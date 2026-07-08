# Stellaris Log Summary

Files: 1
Entries: 217017
Raw entry lines: 221578
Families: 113680
Groups: 119933

## Severity Counts

| severity | entries |
| --- | ---: |
| error | 18415 |
| fatal | 127 |
| info | 198475 |

## Top Families

### 1. 1547x `trigger.cpp:<line>` [error]

Family: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214098` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219770` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214098`-`214100` at `20:32:19`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/00_utilities_aux.txt:172(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 164x `namelist.cpp:<line>` [error]

Family: `namelist.cpp:<line>: Error: Failed Reading Ship Names!`

First: `research\stellar-ai\with-director-error-2026-07-04.log:14849` at `20:31:29`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:15620` at `20:31:30`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:14849`-`14851` at `20:31:29`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:wormhole_station
	common/name_lists/AS01.txt(41)
```

### 3. 152x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference fe_escort from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\with-director-error-2026-07-04.log:209866` at `20:32:17`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:213968` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:209866`-`209866` at `20:32:17`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:322 @ in scripted trigger ESC_ship_uses_battlecruiser_components at file: common/component_templates/nsc_thrusters.txt:176(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 4. 133x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt`

First: `research\stellar-ai\with-director-error-2026-07-04.log:221152` at `20:32:37`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:221371` at `20:32:37`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:221152`-`221152` at `20:32:37`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at file: events/astral_planes_events.txt line: 2326
```

### 5. 124x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference starbase_battlefortress from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\with-director-error-2026-07-04.log:209857` at `20:32:17`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:212749` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:209857`-`209857` at `20:32:17`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:219 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_thrusters.txt:92(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 6. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference att from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\with-director-error-2026-07-04.log:210056` at `20:32:17`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:213937` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:210056`-`210056` at `20:32:17`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:47(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 7. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference conquistador from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\with-director-error-2026-07-04.log:210057` at `20:32:17`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:213938` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:210057`-`210057` at `20:32:17`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:47(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 8. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_hive_farmers]! file`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214331` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219568` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214331`-`214331` at `20:32:19`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_02_hair.txt line: 616
```


## Top Exact Groups

### 1. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214122` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219770` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214122`-`214124` at `20:32:19`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:4319(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214152` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219639` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214152`-`214154` at `20:32:19`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:2703(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 3. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214155` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219743` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214155`-`214157` at `20:32:19`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:1893(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 4. 102x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214101` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219728` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214101`-`214103` at `20:32:19`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:2191(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 5. 92x `dlc.cpp:<line>` [error]

Signature: `dlc.cpp:<line>: Invalid supported_version in file: mod/ugc_<id>.mod line: <n>`

First: `research\stellar-ai\with-director-error-2026-07-04.log:1` at `20:30:36`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:92` at `20:30:36`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:1`-`1` at `20:30:36`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

### 6. 92x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214303` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219746` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214303`-`214305` at `20:32:19`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:656(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 7. 88x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214244` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219720` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214244`-`214246` at `20:32:19`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:980(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 8. 80x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\with-director-error-2026-07-04.log:214184` at `20:32:19`
Last: `research\stellar-ai\with-director-error-2026-07-04.log:219667` at `20:32:19`

Samples:

- `research\stellar-ai\with-director-error-2026-07-04.log:214184`-`214186` at `20:32:19`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:691(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```
