# Stellaris 4.4.4 Modding Quick Reference for Codex Agents

Target: Stellaris PC 4.4.4 stable. Public-source access date: 2026-07-08.

## First checks

1. Capture active playset load order.
2. Resolve enabled mods to folders.
3. Search target object ID in vanilla + active mods.
4. Determine winning parent source.
5. Decide additive new ID versus full override.
6. Verify folder supports fields you plan to add.
7. Verify exact current scope.
8. Add provenance comments for full overrides.
9. Add localisation, icons, DLC gates.
10. Generate duplicate-ID/conflict matrix and validation report.

## PDXScript essentials

```txt
# comment
key = value
key = { child = value }
key = {
    child = value
    nested = { value = yes }
}
```

Values: `yes`, `no`, numbers, identifiers, `@variables`, and quoted strings.

Comparisons: use only in supported trigger fields.

```txt
has_level > 2
years_passed < 20
num_pops >= 50
```

Lists:

```txt
category = { voidcraft particles }
prerequisites = { "tech_starbase_3" "tech_battleships" }
```

Weight rule:

```txt
ai_weight = {
    weight = 1
    modifier = {
        factor = 2
        <trigger in current scope> = yes
    }
    modifier = {
        add = 5
        <trigger in current scope> = yes
    }
}
```

`factor` multiplies. `add` adds. `factor = 0` usually vetoes; use only for true invalid/catastrophic cases.

## Localisation

```yml
l_english:
 my_key:0 "Visible Text"
 my_key_desc:0 "Description."
```

Use `.yml`, language header, UTF-8 BOM if following wiki expectation, no PDX braces, and quote text. Duplicate localisation keys are last-loaded/replace-sensitive.

## Merge assumptions

| Situation | Safe assumption |
|---|---|
| New object ID in supported `common/` folder | Additive |
| Same object ID in `common/` | Full-object override/last-winner risk |
| New scripted trigger/effect/value ID | Additive |
| Duplicate scripted helper ID | Last-winner/full replacement risk |
| New event ID/namespace | Additive |
| Duplicate event ID | Unsafe |
| New localisation key | Additive |
| Duplicate localisation key | Last-loaded, or `localisation/replace` override |
| Same asset path | Later/winning file hides earlier |
| GUI/interface file | High-conflict full/path override risk |
| defines key | Last-winner global override |

## Current-scope cheat sheet

| Surface | Current scope | Country checks |
|---|---|---|
| Technology `weight_modifier` / `ai_weight` | country per CWTools | direct |
| Building `ai_weight` | planet per CWTools | `owner = { ... }` |
| District `ai_weight` | planet per CWTools | `owner = { ... }` |
| Zone potential/unlock | planet per CWTools | `owner = { ... }` |
| Starbase building/module/level `ai_weight` | starbase with `from = country` per CWTools comments | `from = { ... }` |
| Megastructure `ai_weight` | system with `from = country`, `fromfrom = megastructure` per CWTools | `from = { ... }` |
| Pop jobs | varies by child block | verify exact block |
| Decisions | usually planet | `owner = { ... }` |
| Edicts/policies/perks/traditions | usually country | direct; verify |
| Events | event type/caller dependent | inspect ROOT/FROM chain |

## Wrong-scope corrections

Planet-scoped bad:

```txt
has_technology = tech_mega_engineering
```

Planet-scoped correct:

```txt
owner = { has_technology = tech_mega_engineering }
```

Megastructure `ai_weight` bad:

```txt
is_ai = yes
has_technology = tech_mega_engineering
```

Megastructure `ai_weight` correct:

```txt
from = {
    is_ai = yes
    has_technology = tech_mega_engineering
}
```

Starbase definition AI weight correct shape:

```txt
from = {
    is_ai = yes
    has_technology = tech_starbase_4
}
```

## AI layer decision tree

```text
Need AI to build/use X?
  ├─ Is X available? Check potential/allow/possible/prereq/DLC.
  ├─ Does folder support ai_weight or ai_resource_production?
  ├─ Is current scope correct?
  ├─ Is X same-ID parent object? If yes, full override with provenance.
  ├─ Does planet/system/starbase selection logic ever consider X?
  ├─ Do economic plans and ai_budget support the cost/resource category?
  ├─ Does active AI mod replace this layer?
  └─ Add minimal weight/production/budget change and validate.
```

## Static validation commands

Adapt paths:

```bash
rg -n "^\s*<object_id>\s*=" <vanilla>/common <mods>/*/common <generated>/common
rg -n "ai_weight\s*=\s*\{" <generated>/common
rg -n "host_has_dlc|has_dlc" <generated>
rg -n "OVERRIDE PROVENANCE|Parent source|source hash" <generated>
rg -n "^\s*<loc_key>:" <vanilla>/localisation <mods>/*/localisation <generated>/localisation
```

## Error triage

- Unknown trigger/effect/modifier: fix.
- Wrong scope: fix wrapper.
- Missing object reference: add reference/gate or remove dependency.
- Missing tech tier/category: high risk; fix.
- GUI parse errors: high risk.
- Missing localisation/icon: fix before handoff.
- Duplicate object ID: intentional only with provenance.
- `supported_version` warning: not proof of script failure.

## Never do

- Do not mark implemented from roadmap rows.
- Do not ship partial same-ID objects.
- Do not add `ai_weight` to unsupported folders.
- Do not put country triggers directly in planet/system/starbase/megastructure scopes.
- Do not edit `ai_budget`, `economic_plans`, `defines`, ship sizes, sections, components, diplomacy, species rights, or personalities without exact active source proof.
- Do not claim runtime behavior from static validation.
- Do not over-gate AI until it becomes harmless and useless.
