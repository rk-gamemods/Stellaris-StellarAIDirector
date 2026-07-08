# Stellaris Scope Atlas for 4.4.x Modding

**Target baseline:** Stellaris PC 4.4.4 stable.
**Public-source access date:** 2026-07-08.
**Use case:** AI/economy/compatibility implementation in heavy playsets.

Folder-specific scopes below are based on public sources and CWTools schema where stated. They are strong implementation clues, not substitutes for inspecting local 4.4.4 vanilla files and the active parent mods.

## Reliability labels

- **[CONFIRMED: public source]** documented by Stellaris Wiki or public tool docs.
- **[CONFIRMED: CWTools schema]** supported by public CWTools Stellaris config; verify against local 4.4.4 and active mods.
- **[INFERRED: vanilla/mod pattern]** common PDXScript practice; verify locally.
- **[UNCERTAIN / VERSION-SENSITIVE]** do not implement without local file proof.

## Core scope model

A scope is the object currently being evaluated by a trigger, effect, modifier rule, or resource block. The public Scopes wiki documents `THIS`, `PREV`, `FROM`, `ROOT`, dot scopes, and scope-changing triggers/effects, and notes that wrong-scope errors are logged in `error.log`. **[CONFIRMED: public source]**

| Token / bridge | Usual meaning | Guardrail |
|---|---|---|
| `this` / `THIS` | Current object at this point in evaluation | Changes inside every scope-changing block |
| `root` / `ROOT` | Root object for the current evaluation chain | Event roots and object roots differ |
| `from` / `FROM` | Caller or external object supplied by the engine/caller | Meaning is object-specific; never assume |
| `fromfrom` | One level farther up the caller chain | Useful in some megastructure contexts; fragile elsewhere |
| `prev` / `PREV` | Previous scope before the latest scope change | Avoid in deep AI weights; comments required |
| `owner` | Owning country where supported | Best planet/pop/starbase-to-country bridge when supported |
| `controller` | Controlling country where supported | Can differ from owner during occupation/war |
| `solar_system` | Current object to star/system | System is not country; bridge again if needed |
| `capital_scope` | Country to capital planet | Check existence in unusual countries |
| `planet` | Pop/job/orbit to planet bridge | Exact support varies by block |
| `species` | Pop/leader/country to species bridge | Species triggers differ from country triggers |

## Scope-transition patterns

### Direct trigger in current scope

```txt
# Current scope: country.
is_ai = yes
has_technology = tech_starbase_3
```

### Planet to country

```txt
# Current scope: planet.
owner = {
    is_ai = yes
    has_technology = tech_mega_engineering
}
```

### Starbase definition to country

```txt
# Current scope: starbase for starbase module/building/level AI weights per CWTools.
from = {
    is_ai = yes
}
```

### Megastructure AI weight to country

```txt
# Current scope: system; country is `from` per CWTools megastructure schema.
from = {
    is_ai = yes
    has_technology = tech_mega_engineering
}
```

### Pop/job to planet and owner

```txt
# Current scope: pop or pop-job evaluation, depending child block.
planet = {
    owner = {
        is_ai = yes
    }
}
```

## Object-type atlas

### Country

Common in technology weights, edicts, policy options, ascension perks, traditions, AI personalities, many country events, diplomacy actor contexts, economic plans, and AI budgets.

Typical country-scope checks:

```txt
is_ai = yes
is_at_war = yes
has_technology = tech_starbase_3
has_country_flag = my_mod_flag
```

Wrong-scope risk: country triggers copied directly into planet, system, starbase, pop, or event-recipient contexts.

### Planet

Common in buildings, districts, zones, decisions, planet events, deposits, triggered planet modifiers, and planet-specialization logic.

```txt
owner = {
    is_ai = yes
}
solar_system = {
    # system triggers here
}
```

High-frequency mistake: putting `has_technology`, `is_ai`, or country flags directly in a building/district/zone block.

### Pop / pop group / job

Common in `common/pop_jobs`, pop categories, species interactions, and job weights. CWTools comments for jobs indicate multiple child-block scopes: pop/pop group, planet, country, and system can all appear depending on the specific child block.

Implementation rules:

- Do not move a trigger from `country_modifier` to `resources` or `triggered_planet_modifier` without checking the child scope.
- For country checks, prefer a clearly supported bridge such as `owner = { ... }` or `planet = { owner = { ... } }`.
- For species checks, use species bridges or current species scope only where local examples confirm it.
- Resource blocks can use special scopes; verify against local job examples.

### Fleet and ship

Fleet/ship surfaces include ship sizes, sections, components, ship behaviors, combat computers, global ship designs, and event-driven design logic. In heavy NSC3/ESC playsets, these are high-risk.

Implementation rules:

- Do not infer a country scope just because the object belongs to an empire.
- Use `owner = { ... }` only if local schema/examples support it.
- Component templates, section templates, and global ship designs can be parser-data surfaces more than gameplay trigger surfaces.
- Runtime proof is usually needed for auto-design and fleet composition claims.

### Starbase

CWTools starbase schema provides strong clues that starbase buildings/modules/levels evaluate AI weights in starbase scope, with `from = country` available.

```txt
ai_weight = {
    weight = 10
    modifier = {
        factor = 2
        from = {
            is_ai = yes
            has_technology = tech_starbase_4
        }
    }
}
```

Wrong:

```txt
ai_weight = {
    modifier = {
        factor = 2
        has_technology = tech_starbase_4
    }
}
```

Use Starbase Extended source as parent when active; preserve module slots, prerequisites, component sets, and AI placement booleans.

### System and megastructure

CWTools megastructure schema states that megastructure `ai_weight` has `this/root = system`, `from = country`, and `fromfrom = megastructure`.

```txt
ai_weight = {
    weight = 1
    modifier = {
        factor = 2
        from = {
            my_mod_country_is_ai_and_safe_to_spend = yes
        }
    }
}
```

Wrong:

```txt
ai_weight = {
    modifier = {
        factor = 2
        is_ai = yes
    }
}
```

For Gigastructural Engineering, do not copy giant megastructure objects until the active winner, internal scripted triggers/effects, and build-chain stages are known.

### Archaeological site

Archaeological sites usually mix site, stage, planet/system, country, and event scopes. Stage events often supply `from` chains. Use exact vanilla or parent-mod examples for each stage. Do not add country triggers directly to a site/stage block without proving the current scope.

### Federation

Federation types/laws/perks mix federation and member country scopes. Actor, federation, president, member, and target country may all appear in adjacent blocks. Treat federation modding like diplomacy: use exact local source proof before editing AI decisions or law weights.

### Species and leader

Species traits, species rights, leader traits, agendas, council positions, and leader events can evaluate species, pop, leader, country, or owner scopes. Species rights and traits are compatibility-risk surfaces with many DLC and policy interactions.

Rules:

- Preserve DLC gates and trait categories.
- Avoid country triggers unless the block is country scope or has a verified owner bridge.
- Runtime proof is required for species-template, leader-pool, and council behavior claims.

### War, diplomacy, claims, and bombardment

Diplomatic actions, war goals, claims, bombardment stances, and raiding behavior have actor/recipient/target/fleet/planet mixed scopes. `root`, `from`, and `fromfrom` meanings are action-specific. Do not patch these from memory.

Safer alternatives:

- tune economic readiness first;
- tune personalities or scripted values only with exact source proof;
- preserve vanilla gates for genocidal, crisis, subject, fallen empire, and total-war cases.

### Events

Event scope depends on event type and caller.

```txt
namespace = my_mod

country_event = {
    id = my_mod.1
    trigger = { is_ai = yes } # ROOT/THIS usually country
}

planet_event = {
    id = my_mod.2
    trigger = {
        owner = { is_ai = yes } # ROOT/THIS usually planet
    }
}
```

When firing or hooking events, document:

```txt
# EVENT SCOPE CONTRACT:
# event id: my_mod.100
# fired from: <on_action or effect>
# root/this: <object>
# from: <object>
# fromfrom: <object or none>
```

## Folder-specific current-scope matrix

| Folder/surface | Object type | Current scope clue | Common wrong-scope mistake |
|---|---|---|---|
| `common/scripted_triggers/*.txt` | scripted trigger | Caller-defined; executes in caller scope unless it changes scope internally | Undocumented expected scope; generic helper names; unsupported triggers |
| `common/scripted_effects/*.txt` | scripted effect | Caller-defined; effect context from caller | Destructive effects in wrong scope; trigger syntax in effect context |
| `common/scripted_values/*.txt` | scripted value | Caller-defined; often country/planet/system depending use site | Changing global value instead of adding mod-prefixed value |
| `common/technology/*.txt` | technology | weight_modifier and ai_weight: country (`this/root` country per CWTools) | Partial same-ID tech; wrong scope; missing loc/icons |
| `common/technology/tier/*.txt` | technology tier/category support | Weight modifiers are country scope per CWTools | Unreachable tech tiers; tier gaps; crashy tech tree |
| `common/buildings/*.txt` | planet building | Planet scope for body/ai_weight per CWTools; country via owner | Country triggers directly in planet scope; no production signal |
| `common/districts/*.txt` | planet district | Planet scope for potential/allow/ai_weight/ai_resource_production per CWTools | Missing zone slots; owner-scope mistakes; obsolete 3.x assumptions |
| `common/zones/*.txt` | planet zone / zone slot | Planet scope for potential/unlock and ai_resource_production per CWTools | Zone-slot IDs not defined; country triggers without owner |
| `common/pop_jobs/*.txt` | pop job | Varies by child block: pop/pop_group, planet, country, system per CWTools comments | Country logic in pop scope; bad resource categories; unlocalized generated modifiers |
| `common/pop_categories/*.txt` | pop category | Pop/pop_group-oriented; exact fields local-schema dependent | Outdated full overrides; loc/icon assumptions |
| `common/economic_categories/*.txt` | economic category | Definition context; triggered subset scope depends on assigned resource block per wiki | Category without budget support; duplicate category; missing generated loc |
| `common/ai_budget/*.txt` | AI budget entry | Country/economic AI context; exact keys/scopes local 4.4.4 required | Spending boosts without income goals; outdated AI budget copies |
| `common/economic_plans/*.txt` | AI economic plan | Country AI planning context; exact syntax local 4.4.4 required | ai_weight patch when plan is blocker; over-gating AI plans |
| `common/ai_resource_production/*.txt` | AI resource production mapping | AI economy context; verify local scope | Object weights without production signal; mismatched resource category |
| `common/ai_planet_specialization/*.txt` | AI planet specialization | Planet/country planning context; exact field scopes local | Weighting building that specialization never wants |
| `common/personalities/*.txt` | AI personality | Country/personality selection context; verify local fields | Global aggression without economy readiness; wrong country triggers |
| `common/defines/*.txt` | defines/constants | No script scope; key-value constants | Overusing declaration distance/aggression; stale full define files |
| `common/starbase_buildings/*.txt` | starbase building | Starbase scope with `from = country` per CWTools top-level comments | Country triggers directly in starbase scope; full file overwrite |
| `common/starbase_modules/*.txt` | starbase module | Starbase scope with `from = country` per CWTools top-level comments | Wrong component_set/section; unsupported ai_weight nesting |
| `common/starbase_levels/*.txt` | starbase level | Starbase scope with `from = country` for ai_weight per CWTools | Breaking level chain; direct country triggers |
| `common/megastructures/*.txt` | megastructure/orbital structure | ai_weight: `this/root = system`, `from = country`, `fromfrom = megastructure` per CWTools | Country triggers in system scope; copying giant parent files |
| `common/ship_sizes/*.txt` | ship size | Ship design/combat context; exact child scopes vary | Breaking NSC3 classes; missing sections; outdated full overrides |
| `common/component_templates/*.txt` | component template | Component object; modifier scopes vary by child block | Invalid size/type; ESC/NSC set conflicts; missing icons |
| `common/section_templates/*.txt` | section template | Ship design context; slots/reference scopes schema-dependent | Invalid slots; NSC3 breakage; missing locators/entities |
| `common/ship_behaviors/*.txt` | ship behavior | Combat behavior data, not country/planet scope | Treating combat constants as strategic AI |
| `common/global_ship_designs/*.txt` | global ship design | Design template context; schema-dependent | Unavailable components; missing DLC/tech prerequisites |
| `common/strategic_resources/*.txt` | resource | Resource definition; no normal scope except triggers in fields | Resource without economy/budget support; market/localisation gaps |
| `common/decisions/*.txt` | planet decision | Planet scope with `from = country` per CWTools decision replace_scope; show_tech_unlock_if may be country | Country triggers directly in planet scope; missing icon/loc; queued decision effects wrong scope |
| `common/edicts/*.txt` | edict/campaign | Country scope for modifier/AI fields per CWTools country replace_scope; verify potential/allow/effects locally | Wrong cost category; adding ai_weight with bad capitalization/style; missing edict loc |
| `common/policies/*.txt` | policy/options | Country scope for policy/options per CWTools modifier replace_scope; actor semantics local | Using ai_weight instead of supported field; breaking policy flags; diplomacy/species-right side effects |
| `common/ascension_perks/*.txt` | ascension perk | Usually country scope for potential/possible/ai_weight | Wrong scope in possible; missing DLC; old full override |
| `common/traditions/*.txt` | tradition/tree | Usually country scope; verify tree schema | Breaking tree layout; assuming option-level merge |
| `common/federation_types/*.txt` | federation type/perks/laws | Federation/country mixed; verify each block | Country triggers in federation scope; missing DLC gates |
| `common/bombardment_stances/*.txt` | bombardment stance | Country/fleet/planet mixed; verify local schema | Available to wrong empires; bad policy gates |
| `common/species_traits/*.txt` | species trait | Species/pop/country mixed by block; verify local schema | Country checks in species scope; broken generated species |
| `common/leader_traits/*.txt` | leader trait | Leader scope; country via owner if supported | Country triggers in leader scope; outdated councilor fields |
| `common/diplo_actions/*.txt` | diplomatic action | Actor/recipient/country pair scopes; from/root action-specific | Breaking diplomacy; wrong actor/recipient scope |
| `common/on_actions/*.txt` | on-action hook | Event/effect scope depends on on_action and caller | Assuming additive merge; duplicate event IDs; wrong event scope |
| `events/*.txt` | event namespace/events | Event type defines ROOT/THIS; FROM depends on caller/on_action | Missing namespace; wrong ROOT/FROM; unsaved event target |
| `localisation/**/*.yml` | localisation key/value | No PDXScript scope; YAML-like parser | No BOM/header; colon unquoted; duplicate keys; missing _desc |
| `localisation_synced/**/*.yml` | network-synced localisation | No PDXScript scope | Putting normal loc here without proof; missing BOM/header |
| `interface/*.gui, interface/*.gfx` | GUI layout/sprite definitions | No normal script scope; GUI parser/sprite names | Blindly copying UI files; widget ID collisions; missing sprites |
| `gfx/interface/**` | icons/textures | Asset path; no script scope | Missing icon; wrong extension/case; no spriteType |
| `gfx/models, gfx/portraits, common/portraits` | models/portraits | Asset/portrait-definition context; exact schemas local | Missing meshes/textures; wrong paths; unsupported animation refs |
| `map/**` | galaxy/map data | Map parser; no ordinary scope except script fields | Editing map files without compatibility pass |
| `common/solar_system_initializers/*.txt` | system initializer | System/initializer context; planets/stars nested scopes | Wrong nested scopes; invalid planet/deposit refs |
| `common/archaeological_site_types/*.txt` | archaeological site | Site/stage context; events often planet/country/from chains | Wrong event scope; missing pictures/loc |
| `common/sector_focuses/*.txt` | sector/automation focus | Sector/country/planet automation context; verify 4.4.4 schema | Old automation assumptions; conflating player automation with empire AI |

## Wrong-scope error-prevention recipes

### Recipe 1: Country trigger inside planet object

Bad:

```txt
ai_weight = {
    modifier = {
        factor = 2
        is_ai = yes
    }
}
```

Correct:

```txt
ai_weight = {
    modifier = {
        factor = 2
        owner = { is_ai = yes }
    }
}
```

### Recipe 2: Country trigger inside starbase object

Bad:

```txt
ai_weight = {
    modifier = {
        factor = 2
        has_technology = tech_starbase_5
    }
}
```

Correct:

```txt
ai_weight = {
    modifier = {
        factor = 2
        from = { has_technology = tech_starbase_5 }
    }
}
```

### Recipe 3: Country trigger inside megastructure AI weight

Bad:

```txt
ai_weight = {
    modifier = {
        factor = 2
        has_country_flag = wants_megastructure
    }
}
```

Correct:

```txt
ai_weight = {
    modifier = {
        factor = 2
        from = { has_country_flag = wants_megastructure }
    }
}
```

### Recipe 4: Event `from` chain ambiguity

Bad:

```txt
# From undocumented. Future agents cannot safely patch.
country_event = {
    id = my_mod.50
    immediate = {
        from = { set_country_flag = patched }
    }
}
```

Correct:

```txt
# SCOPE CONTRACT:
# Called only from planet scope via `owner = { country_event = { id = my_mod.50 } }`
# ROOT/THIS: country receiving event.
# FROM: planet that triggered the event.
country_event = {
    id = my_mod.50
    immediate = {
        from = {
            # planet effects only
        }
    }
}
```

## Scope-audit checklist

- [ ] Name the current scope before writing each trigger/effect block.
- [ ] Name the required scope for each trigger/effect used.
- [ ] Use the smallest explicit bridge: `owner`, `from`, `planet`, `solar_system`, `species`, or event target.
- [ ] Avoid `prev` unless the chain is shallow and commented.
- [ ] Put wrapper scripted triggers in the expected caller scope and name that scope in comments.
- [ ] Run CWTools scope diagnostics.
- [ ] Inspect `error.log` after any runtime launch.
- [ ] If logs show wrong-scope errors, fix scope before tuning weights.
- [ ] Do not claim AI behavior changed based only on static scope validity.

## Verification methods

1. Search local vanilla object examples in the same folder.
2. Search active parent mod examples in the same folder.
3. Check CWTools schema and scope tooltip.
4. Generate a scope audit file with one line per AI block:
   `file,object_id,block_path,current_scope,bridges_used,country_checks,verification_source`
5. Runtime: run only permitted bounded observer tests, then inspect `error.log` and save-state outcomes.
