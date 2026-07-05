# Codex brief: Stellaris 4.4.x mod development

## Operating assumptions

- Target stable release: Stellaris PC 4.4.4 “Pegasus” unless the user says they are developing against the 4.4.5 open beta. `[S002]`
- Use `supported_version="v4.4.*"` for stable 4.4-compatible local/workshop descriptors. This field is launcher-facing only; it does not determine whether script code loads. `[S007]`
- Treat 4.5 as a separate porting branch because the 4.5 beta changes pop group ethics/faction representation and says it is a breaking, save-incompatible change. `[S004]`

## File placement rule

Local mod source belongs under the Stellaris user mod directory, not the game install directory.

| OS | Local mod directory |
|---|---|
| Windows | `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\` |
| Linux | `~/.local/share/Paradox Interactive/Stellaris/mod/` |
| macOS | `~/Documents/Paradox Interactive/Stellaris/mod/` |

Windows descriptor placement is confirmed in the official modding tutorial; Linux/macOS paths are from the Stellaris Mods wiki snippet and CWTools Linux example. `[S007] [S013] [S019]`

## Minimal required files

A local mod needs two descriptor files:

```text
<user Stellaris mod dir>/my_mod.mod
<user Stellaris mod dir>/my_mod/descriptor.mod
```

The outer `.mod` file contains metadata plus `path="..."`. The inner `descriptor.mod` contains the same metadata but does **not** contain `path`. `[S007]`

## Starter descriptor

Outer file, `my_mod.mod`:

```pdx
version="0.1.0"
tags={
    "Gameplay"
}
name="My Mod"
supported_version="v4.4.*"
path="C:/Users/YOU/Documents/Paradox Interactive/Stellaris/mod/my_mod"
```

Inner file, `my_mod/descriptor.mod`:

```pdx
version="0.1.0"
tags={
    "Gameplay"
}
name="My Mod"
supported_version="v4.4.*"
```

## Folder mirroring rule

A mod mirrors the game install folder structure. Common modded folders are:

```text
common/          game data and rules
events/          event scripts
localisation/    player-facing strings; spelling uses s, not z
localisation_synced/
gfx/             graphical components
interface/       GUI definitions and layout
```

Do not edit the game installation folder directly. Add or overwrite through the mod folder. `[S007]`

## Naming rule for Codex

Always prefix created object IDs, event namespaces, localisation keys, files, flags, variables, and scripted effects/triggers with the mod prefix, for example `my_mod_`.

Bad:

```text
common/governments/civics/00_civics.txt
civic_new_order
```

Better:

```text
common/governments/civics/my_mod_civics.txt
my_mod_civic_new_order
```

The official tutorial specifically warns against using vanilla-like `00_civics.txt` because it can override vanilla civics. `[S007]`

## Localisation rules

- Folder is `localisation`, not `localization`.
- File name must end in `_l_<language>.yml`, e.g. `my_mod_l_english.yml`.
- First line must be `l_english:` for English.
- Save as UTF-8 with BOM.
- There is no reliable fallback language; missing keys show as raw keys.
- Use `localisation/replace` for intentional key overrides. `[S008]`

## Load order rule

The practical rule is: the playset is loaded in order, and later/lower mods often override earlier/top mods when the content type is LIOS-style. However, Stellaris/Clausewitz content includes FIOS/LIOS exceptions, so **do not implement a universal “last mod wins” assumption**. Use Irony Mod Manager or current vanilla + CWTools/full-cache validation to detect actual element-level conflicts. `[S011] [S012]`

## Conflict-safe behavior

When adding content:

1. Add new files with unique names.
2. Add new object keys with a unique prefix.
3. Do not copy whole vanilla files unless the folder requires a full replacement.
4. If overriding a vanilla object, isolate and document the key.
5. If patching another mod, make a separate compatibility patch that loads after the affected mods.
6. Test with only the mod, then with target playset, then inspect `error.log`.

## 4.4-specific hazards to test

- Arkship colonies are ship-carried colonies, not normal planets.
- Nomadic Empires may not own conventional claimed systems or settled worlds.
- Waystations/Waylines add new trade/logistics geography and UI surfaces.
- Contracts affect diplomacy/economy/event logic.
- 4.4.4 fixes included Arkship colony planet-class modifiers, Waystation UI crash with modded UI, arkships moving between owners in Nomad Total Wars, and double Wayline modifier application. Treat these as regression targets. `[S001] [S002]`

## 4.5 hazard

Do not casually version-bump pop/faction/ethics/job mods from 4.4 to 4.5. The 4.5 beta changes pop group ethics/faction representation from per-group splits to percentages and removes/deprecates several old pop-ethic triggers. `[S004]`

## Debug loop

1. Run clean playset with only the mod.
2. Check descriptor and path.
3. Launch with `-script_debug -debug_mode -debugtooltip` while testing.
4. Read `error.log` first, then `game.log`.
5. Add temporary `log = "..."` effects.
6. Use console `help` to confirm command names, then test selected-scope scripts and events.
7. Use `debugtooltip` for object IDs and hidden state.
8. Use `script_profiler` for performance regressions. `[S007] [S010]`

## AI/LLM findings

There is no supported native “LLM API inside Stellaris” found. Public LLM projects are external companions:

- Galactic Conclave: reads saves, generates empire diplomacy through an LLM, applies optional actions through a command file and the Stellaris `run` console command. `[S015]`
- Stellaris Overmind: watches autosaves, uses an LLM to choose macro strategy, and nudges AI empires through personality/stat modifiers while native Stellaris AI handles execution. `[S016]`
- Stellaris LLM Companion: save analyzer/advisor with MCP relay into Claude/Codex-style clients. `[S017]`

Architecture recommendation for LLM empire control: external service + save parser + whitelisted action schema + mod/console bridge + audit logs + no free-form command execution.
