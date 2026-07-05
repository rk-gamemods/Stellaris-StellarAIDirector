# Current version and structural changes

## Version status snapshot

Generated: 2026-07-04

| Version/branch | Source finding | Modder action |
|---|---|---|
| 4.4.4 “Pegasus” stable | Steam news reports “Stellaris 4.4.4 patch released (5505)” and availability through Steam, GOG, MS Store. `[S002]` | Primary public target. |
| 4.4.5 “Pegasus” open beta | Steam news says early 4.4.5 was made available on `stellaris_test`; Dev Diary #427 says 4.4.5 beta was updated again. `[S003] [S004]` | Maintain beta branch. |
| 4.5 “Cygnus” open beta | Dev Diary #427 describes experimental beta and a breaking pop/faction/ethics change. `[S004]` | Separate porting branch. |

## 4.0 Phoenix structural changes

The 4.0 Phoenix update is the main reason older Stellaris modding knowledge can fail. Relevant changes:

- Pops grouped by species, strata, and ethic; groups produce Workforce. `[S005]`
- Workforce is assigned to jobs, and pop groups can supply multiple jobs. `[S005]`
- Species traits that formerly created extra resources now generate bonus workforce in relevant jobs. `[S005]`
- Pop growth became simultaneous across species on a planet. `[S005]`
- Old Trade Routes were removed; Trade became a regular resource/logistics system. `[S005] [S006]`
- Planetary deficits and military fleets interact with logistics/trade costs. `[S005] [S006]`
- Districts/jobs/buildings/planet UI were reworked. `[S005] [S006]`

## 4.4 Pegasus/Nomads structural changes

Relevant added systems:

- Nomadic Empires not bound to normal claimed systems/colonized worlds. `[S001]`
- Arkships replace traditional worlds for Nomad empires and are upgradable carrier colonies. `[S001]`
- Waystations and Waylines create lasting interstellar trade/resource routes. `[S001]`
- Contract System creates task-driven empire interactions. `[S001]`
- Free 4.4 update includes join/leave wars in progress, improved job systems/selection, reworked Situation Log UI, performance fixes. `[S001]`

## 4.4.4 regression targets

4.4.4 fixes reveal the following modding hazards:

| Patch note surface | Why it matters to mods |
|---|---|
| Planet-class modifiers now apply to Arkship colonies | Planet/colony modifiers must handle carrier colonies. |
| Waystation UI crash in some modded UI cases | UI mods must test Waystation screens. |
| Total Wars between Nomads move Arkships between owners | War/ownership scripts must handle Arkship ownership transfer. |
| Arkships no longer double-benefit from Wayline modifiers | Modifier stacking around Waylines needs regression tests. |
| Doomsday planet modifier applied to embarked Arkship | Origin/event migration to Arkship state can break. |

Source: `[S002]`

## 4.4.5 beta modding-facing changes

Use only if targeting beta or if confirmed compatible with stable:

- `total_progress` with per-stage `section_weight` for situations.
- Situation/stage/approach `custom_tooltip` and `custom_tooltip_with_modifiers`.
- `orbital_ring_and_arkship_equivalent_absent` scripted trigger.
- Starbase module `scripted_effect_cooldown`, `scripted_effect_cooldown_flag`, `scripted_effect_cooldown_flag_desc`.
- Optional `<id>` and `<event_chain>` for `is_point_of_interest`.
- Scripted action `automation = {}` with options and parent nesting.
- Fleet-scoped `has_automation_flag`.
- `home_colony` and `background_colony` scopes.

Source: `[S004]`

## 4.5 beta breaking changes

Do not version-bump blindly from 4.4 to 4.5 if the mod touches pops, factions, ethics, jobs, species, workforce, UI, or AI economy.

Critical changes:

- Pop groups no longer divided by ethics/factions.
- Pop groups have percentage belonging to each ethic/faction.
- Change is explicitly breaking and save-incompatible.
- Deprecated pop ethic triggers are removed/replaced.

Source: `[S004]`
