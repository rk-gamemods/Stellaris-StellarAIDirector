# Codex implementation rulebook for Stellaris mods

This is a rule file that can be pasted into Codex as system/developer context for generating Stellaris 4.4.x mod files.

## Global constraints

1. Target `Stellaris 4.4.4` unless the task explicitly says `4.4.5 beta`, `4.5 beta`, or another version.
2. Do not invent folders. Use recognized Stellaris mod paths mirrored from vanilla.
3. Do not invent triggers/effects/modifiers. Prefer names found in provided vanilla files, generated docs, or source references.
4. Additive unique-key content is preferred over overriding vanilla.
5. Prefix every new key with the mod prefix.
6. Use `is_triggered_only = yes` for events unless there is a specific reason to poll.
7. Guard optional scope switches with `exists`.
8. Treat Nomad/Arkship colonies as a first-class compatibility case in 4.4.x.
9. Do not assume load order is always last-wins; flag conflicts for Irony/CWTools validation.
10. Never emit arbitrary console commands as an LLM bridge. Use a whitelisted action schema.

## Required descriptor behavior

- Outer `.mod` in user mod dir includes `path`.
- Inner `descriptor.mod` in mod root excludes `path`.
- `supported_version` is visual only but should be accurate for users.

## Required localisation behavior

- Path: `localisation/english/<mod>_l_english.yml`.
- Encoding: UTF-8 with BOM.
- First line: `l_english:`.
- Prefix all keys.
- Add whitespace before every key.

## Event generation template

```pdx
namespace = MOD_PREFIX

country_event = {
    id = MOD_PREFIX.0001
    hide_window = yes
    is_triggered_only = yes

    trigger = {
        exists = this
    }

    immediate = {
        log = "[MOD_PREFIX] MOD_PREFIX.0001 fired"
    }
}
```

## Scripted trigger style

```pdx
MOD_PREFIX_can_do_thing = {
    exists = this
    is_country_type = default
    NOT = { has_country_flag = MOD_PREFIX_thing_disabled }
}
```

## Scripted effect style

```pdx
MOD_PREFIX_apply_thing = {
    if = {
        limit = { exists = this }
        set_timed_country_flag = {
            flag = MOD_PREFIX_thing_active
            days = 3600
        }
    }
}
```

## Do not generate without vanilla validation

- Full UI `.gui` replacements.
- AI economic plans.
- Pop/job/faction/ethics logic for 4.5.
- `replace_path` descriptors.
- New folder names.
- Direct edits to vanilla install folder.
- Assumptions that all countries have planets/capitals/claims.

## Patch note interpretation rules

- 4.0 changes invalidate old pop/job/trade assumptions.
- 4.4 changes add Arkship/Wayline/Contract/Situation Log compatibility cases.
- 4.4.5 beta fields should not be used in stable code without checking that stable ignores them.
- 4.5 pop/faction/ethics changes require a branch and explicit migration.

## Required output when modifying a mod

Every Codex change should include:

1. Files changed.
2. Object keys added/overridden.
3. Localisation keys added/overridden.
4. Scope assumptions.
5. Load-order/conflict assumptions.
6. Test plan.
7. Items requiring runtime validation.
