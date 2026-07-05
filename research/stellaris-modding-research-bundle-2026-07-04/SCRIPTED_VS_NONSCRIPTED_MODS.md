# Scripted vs nonscripted mods

## Scripted mods

In Stellaris modding, “scripted” means Paradox/Clausewitz PDXScript. It usually lives in `.txt` files under recognized folders.

Common scripted areas:

```text
common/governments/civics/
common/origins/
common/buildings/
common/districts/
common/pop_jobs/
common/deposits/
common/technology/
common/traditions/
common/ascension_perks/
common/edicts/
common/policies/
common/component_templates/
common/ship_sizes/
common/starbase_buildings/
common/starbase_modules/
common/ship_behaviors/
common/on_actions/
common/scripted_effects/
common/scripted_triggers/
common/scripted_loc/
events/
```

Scripted mods can add or override gameplay state. They are most likely to be checksum-changing, save-affecting, and patch-sensitive.

## Script execution model essentials

- Script runs in a scope.
- Wrong-scope triggers produce `error.log` entries and may cause failures. `[S009]`
- Effects on a nonexistent scope can silently do nothing. `[S009]`
- `any_` triggers switch scope and return true if any matching object passes. `[S009]`
- `every_` and `random_` effects switch scope and apply to all/random matching objects. `[S009]`
- Use `limit = {}` inside `every_`/`random_` effects.
- Use `exists = scope` checks before optional scope switches. `[S009]`

## Event scripts

Always declare a namespace:

```pdx
namespace = my_mod
```

Use namespaced event IDs:

```pdx
country_event = {
    id = my_mod.0001
    hide_window = yes
    is_triggered_only = yes
}
```

The official tutorial recommends making events triggered-only unless there is a clear reason for recurring checks. `[S007]`

## Nonscripted/content mods

Nonscripted mods change presentation/content rather than rules:

- Localisation text.
- Portraits.
- Flags/emblems.
- Icons and event images.
- Music and advisor audio.
- UI layout.
- Namelists.

These still conflict if keys, paths, or UI files overlap. UI mods are frequently high-risk because a small visual change may require copying a large vanilla `.gui` file.

## External companion tools

External tools are neither normal scripted nor nonscripted mods. They can:

- Parse saves.
- Watch autosaves.
- Parse logs.
- Generate strategy advice.
- Emit console commands.
- Use LLMs.

The public LLM-related projects found in this research are external companions using save parsing and/or command bridges. `[S015] [S016] [S017]`
