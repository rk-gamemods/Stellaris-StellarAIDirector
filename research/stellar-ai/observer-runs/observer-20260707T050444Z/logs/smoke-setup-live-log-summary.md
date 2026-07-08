# Stellaris Log Summary

Files: 2
Entries: 221153
Raw entry lines: 227012
Families: 115245
Groups: 121521

## Severity Counts

| severity | entries |
| --- | ---: |
| error | 18494 |
| fatal | 127 |
| info | 202532 |

## Top Families

### 1. 1547x `trigger.cpp:<line>` [error]

Family: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218139` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223814` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218139`-`218141` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:1366(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218142`-`218144` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1352(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218145`-`218147` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:1862(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 164x `namelist.cpp:<line>` [error]

Family: `namelist.cpp:<line>: Error: Failed Reading Ship Names!`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:14938` at `01:29:28`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:15709` at `01:29:29`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:14938`-`14940` at `01:29:28`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:wormhole_station
	common/name_lists/AS01.txt(41)
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:14941`-`14943` at `01:29:28`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:terraform_station
	common/name_lists/AS01.txt(42)
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:14944`-`14946` at `01:29:28`

```text
Error: Failed Reading Ship Names!
	Reason: Invalid Ship Size:outpost_station
	common/name_lists/AS01.txt(44)
```

### 3. 152x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference fe_escort from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213983` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218008` at `01:30:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213983`-`213983` at `01:30:22`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/nsc_thrusters.txt:234(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214332`-`214332` at `01:30:22`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/esc_components_thrusters.txt:437(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214349`-`214349` at `01:30:22`

```text
Failed to deferred read key reference fe_escort from database  common/scripted_triggers/esc_ship_size_triggers.txt:302 @ in scripted trigger ESC_ship_uses_strikecruiser_components at file: common/component_templates/nsc_thrusters.txt:90(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 4. 133x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225081` at `01:30:47`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225298` at `01:30:47`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225081`-`225081` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4257 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7529
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225082`-`225082` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/zzz_giga_overwrites.txt:191 @ scripted effect activate_behemoth_superweapon at file: events/biogenesis_crisis_events.txt line: 3378
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225083`-`225083` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/02_machine_age_effects.txt:1417 @ scripted effect synth_queen_wipe_system at file: events/machine_age_crisis_events.txt line: 4706
```

### 5. 128x `trigger.cpp:<line>` [error]

Family: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' | Current Scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225607` at `01:34:15`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:226797` at `01:34:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225607`-`225609` at `01:34:15`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:3435(inline_script) common/inline_scripts/ship_components_general/esc_inlines_titanic_standard_bio.txt line: 7
Current Scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225610`-`225612` at `01:34:15`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:3503(inline_script) common/inline_scripts/ship_components_general/esc_inlines_titanic_standard_bio.txt line: 7
Current Scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225613`-`225615` at `01:34:15`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:4074(inline_script) common/inline_scripts/ship_components_general/esc_inlines_titanic_standard_bio.txt line: 7
Current Scope: ship_growth_stage
Supported Scopes: country
```

### 6. 124x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference starbase_battlefortress from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213803` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:216850` at `01:30:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213803`-`213803` at `01:30:22`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:412 @ in scripted trigger ESC_ship_uses_starbase_computers at file: common/component_templates/esc_components_computers.txt:995(inline_script) common/inline_scripts/ship_components_general/esc_inlines_combat_computers.txt:13(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213942`-`213942` at `01:30:22`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:219 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_leviathans.txt:623(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213992`-`213992` at `01:30:22`

```text
Failed to deferred read key reference starbase_battlefortress from database  common/scripted_triggers/esc_ship_size_triggers.txt:219 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_kinetics.txt:3208(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 7. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference att from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214246` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218009` at `01:30:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214246`-`214246` at `01:30:22`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 758
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214303`-`214303` at `01:30:22`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 964
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214352`-`214352` at `01:30:22`

```text
Failed to deferred read key reference att from database  common/scripted_triggers/esc_ship_size_triggers.txt:110 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:216(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 8. 120x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference conquistador from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214247` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218010` at `01:30:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214247`-`214247` at `01:30:22`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 758
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214304`-`214304` at `01:30:22`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/00_utilities_thrusters.txt line: 964
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214353`-`214353` at `01:30:22`

```text
Failed to deferred read key reference conquistador from database  common/scripted_triggers/esc_ship_size_triggers.txt:111 @ in scripted trigger ESC_ship_uses_cruiser_components at file: common/component_templates/esc_components_thrusters.txt:216(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

### 9. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_hive_farmers]! file`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218182` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223802` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218182`-`218182` at `01:30:24`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_05_hair.txt line: 301
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218215`-`218215` at `01:30:24`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_01_hair.txt line: 1489
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218222`-`218222` at `01:30:24`

```text
Invalid government type [gov_hive_farmers]!  file: gfx/portraits/asset_selectors/human_female_03_hair.txt line: 1572
```

### 10. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_mutualistic_behavior]! file`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218151` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223812` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218151`-`218151` at `01:30:24`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_female_02_hair.txt line: 800
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218178`-`218178` at `01:30:24`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_male_03_hair.txt line: 2639
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218277`-`218277` at `01:30:24`

```text
Invalid government type [gov_mutualistic_behavior]!  file: gfx/portraits/asset_selectors/human_male_01_hair.txt line: 1050
```

### 11. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [gov_parasitic_alien]! file`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218410` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223791` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218410`-`218410` at `01:30:24`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_male_05_hair.txt line: 467
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218476`-`218476` at `01:30:24`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_female_05_hair.txt line: 341
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218484`-`218484` at `01:30:24`

```text
Invalid government type [gov_parasitic_alien]!  file: gfx/portraits/asset_selectors/human_male_01_hair.txt line: 34
```

### 12. 105x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Invalid government type [vbp_hive_mind]! file`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218138` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223739` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218138`-`218138` at `01:30:24`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_male_05_hair.txt line: 385
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218192`-`218192` at `01:30:24`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_female_03_hair.txt line: 1307
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218207`-`218207` at `01:30:24`

```text
Invalid government type [vbp_hive_mind]!  file: gfx/portraits/asset_selectors/human_male_02_hair.txt line: 958
```

### 13. 99x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference juggernaut_nosh from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213943` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:216851` at `01:30:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213943`-`213943` at `01:30:22`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_leviathans.txt:623(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213993`-`213993` at `01:30:22`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_kinetics.txt:3208(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214004`-`214004` at `01:30:22`

```text
Failed to deferred read key reference juggernaut_nosh from database  common/scripted_triggers/esc_ship_size_triggers.txt:220 @ in scripted trigger ESC_ship_uses_juggernaut_components at file: common/component_templates/esc_components_psionic.txt line: 1286
```

### 14. 92x `dlc.cpp:<line>` [error]

Family: `dlc.cpp:<line>: Invalid supported_version`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:2` at `01:28:21`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:93` at `01:28:22`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:2`-`2` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3`-`3` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1199002146.mod line: 9
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:4`-`4` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1333526620.mod line: 12
```

### 15. 92x `job_type.cpp:<line>` [error]

Family: `job_type.cpp:<line>: Missing job Localization Key`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:15760` at `01:29:33`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:15889` at `01:29:34`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:15760`-`15760` at `01:29:33`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_desc
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:15761`-`15761` at `01:29:33`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_minerals_desc
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:15762`-`15762` at `01:29:33`

```text
Missing job Localization Key: giga_birch_orykta_manager_energy_refinery_desc
```

### 16. 90x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference escortcarrier from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213891` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218011` at `01:30:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213891`-`213891` at `01:30:22`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/esc_components_thrusters.txt:231(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213952`-`213952` at `01:30:22`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 395
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214026`-`214026` at `01:30:22`

```text
Failed to deferred read key reference escortcarrier from database  common/scripted_triggers/esc_ship_size_triggers.txt:136 @ in scripted trigger ESC_ship_uses_battleship_components at file: common/component_templates/00_utilities_thrusters.txt line: 594
```

### 17. 89x `parser_deferred_database_objects.cpp:<line>` [error]

Family: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference artemis from database common/scripted_triggers/esc_ship_size_triggers.txt`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213994` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:216758` at `01:30:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213994`-`213994` at `01:30:22`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:98 @ in scripted trigger ESC_ship_uses_destroyer_reactors at file: common/component_templates/esc_components_reactors_bio.txt:979(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214132`-`214132` at `01:30:22`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:98 @ in scripted trigger ESC_ship_uses_destroyer_reactors at file: common/component_templates/esc_components_reactors.txt:350(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 7
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:214133`-`214133` at `01:30:22`

```text
Failed to deferred read key reference artemis from database  common/scripted_triggers/esc_ship_size_triggers.txt:98 @ in scripted trigger ESC_ship_uses_destroyer_reactors at file: common/component_templates/00_utilities_reactors.txt line: 69
```

### 18. 84x `ship_size.cpp:<line>` [error]

Family: `ship_size.cpp:<line>: Missing ship size Localization Key`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3971` at `01:29:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:4101` at `01:29:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3971`-`3971` at `01:29:24`

```text
Missing ship size Localization Key: precursor_colossus
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3972`-`3972` at `01:29:24`

```text
Missing ship size Localization Key: precursor_colossus_plural
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3973`-`3973` at `01:29:24`

```text
Missing ship size Localization Key: sofe_ancient_weapon
```

### 19. 78x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213775` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:215057` at `01:30:23`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213775`-`213775` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213776`-`213776` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 291
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213786`-`213786` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 325
```

### 20. 78x `trigger_impl.cpp:<line>` [error]

Family: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213795` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:215066` at `01:30:23`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213795`-`213795` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 419
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213813`-`213813` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 598
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213860`-`213860` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 290
```


## Top Exact Groups

### 1. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218208` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223768` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218208`-`218210` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:270(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218227`-`218229` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:4145(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218355`-`218357` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_archaeo.txt:4259(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 2. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218219` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223809` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218219`-`218221` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:4516(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218288`-`218290` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:2334(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218316`-`218318` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_energy.txt:4658(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 3. 120x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218189` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223799` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218189`-`218191` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:649(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218242`-`218244` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:1449(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218245`-`218247` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_shields.txt:198(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 4. 102x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218145` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223795` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218145`-`218147` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:1862(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218148`-`218150` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:1260(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218169`-`218171` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_armor.txt:1908(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 5. 92x `dlc.cpp:<line>` [error]

Signature: `dlc.cpp:<line>: Invalid supported_version in file: mod/ugc_<id>.mod line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:2` at `01:28:21`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:93` at `01:28:22`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:2`-`2` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3`-`3` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1199002146.mod line: 9
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:4`-`4` at `01:28:21`

```text
Invalid supported_version in  file: mod/ugc_1333526620.mod line: 12
```

### 6. 92x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218172` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223751` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218172`-`218174` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:410(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218280`-`218282` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:186(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218294`-`218296` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:22(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 7. 88x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218142` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223780` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218142`-`218144` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1352(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218196`-`218198` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:957(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218223`-`218225` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors.txt:1026(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 8. 80x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218179` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223803` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218179`-`218181` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:869(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218442`-`218444` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:756(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218489`-`218491` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_kinetics.txt:67(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 9. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213775` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:215057` at `01:30:23`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213775`-`213775` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213776`-`213776` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 291
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213786`-`213786` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 325
```

### 10. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: Scripted Trigger has_job is invalid at file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213795` at `01:30:22`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:215066` at `01:30:23`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213795`-`213795` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 419
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213813`-`213813` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 598
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:213860`-`213860` at `01:30:22`

```text
Scripted Trigger has_job is invalid at  file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 290
```

### 11. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218158` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223720` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218158`-`218158` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 195]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218159`-`218159` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 291]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218287`-`218287` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_female_clothes_01.txt line: 156]: Error in scripted trigger, cannot find: has_job
```

### 12. 78x `trigger_impl.cpp:<line>` [error]

Signature: `trigger_impl.cpp:<line>: [ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: <n>]: Error in scripted trigger, cannot find: has_job`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218206` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223772` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218206`-`218206` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 419]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218397`-`218397` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 414]: Error in scripted trigger, cannot find: has_job
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218449`-`218449` at `01:30:24`

```text
[ file: gfx/portraits/asset_selectors/new_human_male_clothes_01.txt line: 352]: Error in scripted trigger, cannot find: has_job
```

### 13. 72x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218338` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223764` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218338`-`218340` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:496(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218366`-`218368` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:595(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218407`-`218409` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:146(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general.txt:31(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 14. 68x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:<n>(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218203` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223748` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218203`-`218205` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:107(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218322`-`218324` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:216(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218403`-`218405` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_thrusters.txt:525(inline_script) common/inline_scripts/thrusters/esc_inlines_thrusters.txt:29(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 12
Current scope: ship_growth_stage
Supported Scopes: country
```

### 15. 60x `parser_deferred_database_objects.cpp:<line>` [error]

Signature: `parser_deferred_database_objects.cpp:<line>: Failed to deferred read key reference frameworld_planetary_outpost from database common/scripted_triggers/giga_habitat_triggers.txt:<n> @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:<n> @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:<n> @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:<n> @ scripted effect giga_cosmogenesis_effect at file: events/giga_02`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225081` at `01:30:47`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225298` at `01:30:47`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225081`-`225081` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4257 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7529
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225084`-`225084` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4563 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4200 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7680
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:225088`-`225088` at `01:30:47`

```text
Failed to deferred read key reference frameworld_planetary_outpost from database  common/scripted_triggers/giga_habitat_triggers.txt:35 @ in scripted trigger giga_is_habitat_orbital at common/scripted_effects/zzz_giga_overwrites.txt:106 @ scripted effect spawn_habitat_cracker_effect at common/scripted_effects/00_scripted_effects.txt:4584 @ scripted effect destroy_star_system at common/scripted_effects/giga_scripted_effects.txt:4257 @ scripted effect giga_cosmogenesis_effect at file: events/giga_021_blokkat.txt line: 7780
```

### 16. 60x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:<n>(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218313` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223814` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218313`-`218315` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:1316(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218384`-`218386` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:744(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218439`-`218441` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_reactors_bio.txt:721(inline_script) common/inline_scripts/reactors/esc_inlines_reactors_general_sr.txt:35(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships_conditional.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

### 17. 60x `section.cpp:<line>` [info]

Signature: `section.cpp:<line>: section has no entity. file common/section_templates/explorationship.txt Line <n>-<n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:64933` at `01:29:46`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:76412` at `01:29:46`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:64933`-`64933` at `01:29:46`

```text
section has no entity. file common/section_templates/explorationship.txt Line 18-37
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:65131`-`65131` at `01:29:46`

```text
section has no entity. file common/section_templates/explorationship.txt Line 39-68
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:65328`-`65328` at `01:29:46`

```text
section has no entity. file common/section_templates/explorationship.txt Line 70-94
```

### 18. 52x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218139` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223658` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218139`-`218141` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:1366(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218378`-`218380` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:1599(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218430`-`218432` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_nanites.txt:737(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

### 19. 47x `economic_unit_template.cpp:<line>` [error]

Signature: `economic_unit_template.cpp:<line>: Failed to read key reference starbase_stations from database file: common/ship_sizes/!_giga_placeholder_ships.txt:<n>(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: <n>`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3975` at `01:29:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:4099` at `01:29:24`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3975`-`3975` at `01:29:24`

```text
Failed to read key reference starbase_stations from database  file: common/ship_sizes/!_giga_placeholder_ships.txt:110(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: 3
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3976`-`3976` at `01:29:24`

```text
Failed to read key reference starbase_stations from database  file: common/ship_sizes/!_giga_placeholder_ships.txt:111(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: 3
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:3977`-`3977` at `01:29:24`

```text
Failed to read key reference starbase_stations from database  file: common/ship_sizes/!_giga_placeholder_ships.txt:112(inline_script) common/inline_scripts/giga_placeholders/ship_sizes.txt line: 3
```

### 20. 44x `trigger.cpp:<line>` [error]

Signature: `trigger.cpp:<line>: Wrong scope for trigger 'uses_ship_category' at common/scripted_triggers/07_scripted_triggers_ships.txt:<n> @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:<n>(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: <n> | Current scope: ship_growth_stage | Supported Scopes: country`

First: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218291` at `01:30:24`
Last: `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:223699` at `01:30:25`

Samples:

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218291`-`218293` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:220(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218454`-`218456` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:65(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 10
Current scope: ship_growth_stage
Supported Scopes: country
```

- `research\stellar-ai\observer-runs\observer-20260707T050444Z\logs\smoke-setup-error.log:218496`-`218498` at `01:30:24`

```text
Wrong scope for trigger 'uses_ship_category' at  common/scripted_triggers/07_scripted_triggers_ships.txt:35 @ in scripted trigger country_uses_bio_ships at file: common/component_templates/esc_components_auxiliary.txt:250(inline_script) common/inline_scripts/ship_components_general/esc_inlines_uses_bio_ships.txt line: 11
Current scope: ship_growth_stage
Supported Scopes: country
```
