# Mod structure and setup

## Exact storage locations

| OS | Local mod folder |
|---|---|
| Windows | `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\` |
| Linux | `~/.local/share/Paradox Interactive/Stellaris/mod/` |
| macOS | `~/Documents/Paradox Interactive/Stellaris/mod/` |

Source notes: Windows location and descriptor placement are from the official Stellaris modding tutorial. Linux is also shown by CWTools. Linux/macOS table is also present in the Stellaris Mods wiki snippet, although the full page was client-challenge blocked during retrieval. `[S007] [S013] [S019]`

## Descriptor pair

Required:

```text
%USERPROFILE%/Documents/Paradox Interactive/Stellaris/mod/my_mod.mod
%USERPROFILE%/Documents/Paradox Interactive/Stellaris/mod/my_mod/descriptor.mod
```

Outer `.mod`:

```pdx
version="0.1.0"
tags={
    "Gameplay"
}
name="My Mod"
supported_version="v4.4.*"
path="C:/Users/YOU/Documents/Paradox Interactive/Stellaris/mod/my_mod"
```

Inner `descriptor.mod`:

```pdx
version="0.1.0"
tags={
    "Gameplay"
}
name="My Mod"
supported_version="v4.4.*"
```

Rules:

- Outer file has `path`.
- Inner file does not have `path`.
- `supported_version` may use a wildcard such as `v4.4.*`.
- `supported_version` is visual/launcher-facing only. `[S007]`

## Recommended skeleton

```text
my_mod/
  descriptor.mod
  common/
    governments/
      civics/
        my_mod_civics.txt
    on_actions/
      my_mod_on_actions.txt
    scripted_effects/
      my_mod_scripted_effects.txt
    scripted_triggers/
      my_mod_scripted_triggers.txt
  events/
    my_mod_events.txt
  localisation/
    english/
      my_mod_l_english.yml
```

## Mirror structure rule

Stellaris reads most content from the install directory and from mod directories using the same folder structure. Do not edit the install directory. Use the mod folder to add or override content. `[S007]`

Common roots:

| Root | Purpose |
|---|---|
| `common/` | Game data/rules. |
| `events/` | Event scripts. |
| `localisation/` | Player-visible strings. |
| `localisation_synced/` | Synced localisation. |
| `gfx/` | Graphical components. |
| `interface/` | UI layout and asset rules. |

## Naming conventions

Use a unique prefix. For example, if the mod prefix is `my_mod`, use:

```text
my_mod_civics.txt
my_mod_events.txt
my_mod_l_english.yml
namespace = my_mod
my_mod.0001
my_mod_civic_example
my_mod_has_feature_enabled
my_mod_apply_feature_effect
my_mod_feature_enabled
my_mod_feature_counter
```

Avoid:

```text
00_civics.txt
civic_example
namespace = events
```

The official tutorial specifically notes that using `00_civics.txt` would override vanilla civics and recommends mod-specific naming. `[S007]`

## Localisation

Rules from the localisation page:

- Folder is `localisation`, not `localization`.
- UTF-8 with BOM is required.
- File name must end with `_l_<language>.yml`.
- First line must be `l_<language>:`.
- Every key after the header must begin with whitespace.
- There is no reliable fallback language.
- `localisation/replace` is for intentional key overrides and loads after other localisation files. `[S008]`

## Safe minimal event scaffolding

```pdx
namespace = my_mod

country_event = {
    id = my_mod.0001
    hide_window = yes
    is_triggered_only = yes

    trigger = {
        is_ai = no
    }

    immediate = {
        log = "[my_mod] event my_mod.0001 fired"
    }
}
```

The official tutorial recommends `is_triggered_only = yes` as a general rule unless there is a strong reason to run recurring event polling. `[S007]`
