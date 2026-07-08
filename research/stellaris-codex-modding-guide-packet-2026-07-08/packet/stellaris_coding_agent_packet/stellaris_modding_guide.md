# Stellaris 4.4.x Modding Guide for Codex Implementation Agents

**Target baseline:** Stellaris PC 4.4.4 stable. Treat 4.4.x as the implementation target. Mention 4.5 only when separately verified and clearly labeled.

**Primary use case:** building and validating local Stellaris mods, especially AI/economy/compatibility submods for heavy playsets with Gigastructural Engineering, NSC3, Extra Ship Components NEXT, Starbase Extended, Stellar AI or similar AI mods, Planetary Diversity, UI mods, and other large Workshop mods.

**Codex operating assumption:** the agent cannot safely launch observer games by default. It should rely on static validation, vanilla/mod source inspection, generated audit files, active load-order evidence, CWTools diagnostics, and bounded runtime proof only when the user explicitly provides or permits it.

**Public-source access date:** 2026-07-08. See `sources.csv` for URLs, publishers, version notes, reliability, and supported claims.

## Reliability labels

- **[CONFIRMED: public source]** Supported by a public source listed in `sources.csv`.
- **[CONFIRMED: CWTools schema]** Supported by public CWTools Stellaris config. Strong schema evidence; still verify against local 4.4.4 and active mods.
- **[INFERRED: vanilla/mod pattern]** Practical implementation rule inferred from typical Stellaris/Clausewitz patterns. Verify before risky changes.
- **[COMMUNITY-REPORTED]** Useful lead only. Never treat as 4.4.4 proof.
- **[UNCERTAIN / VERSION-SENSITIVE]** Needs local vanilla, active mod, CWTools, or runtime verification.

## Table of contents

1. [Hard implementation rules](#hard-implementation-rules)
2. [How Stellaris loads mod files](#how-stellaris-loads-mod-files)
3. [Descriptors, dependencies, launcher files, and DLC](#descriptors-dependencies-launcher-files-and-dlc)
4. [PDXScript syntax and parse traps](#pdxscript-syntax-and-parse-traps)
5. [Scope rules](#scope-rules)
6. [AI modding model](#ai-modding-model)
7. [Folder-specific surfaces](#folder-specific-surfaces)
8. [Compatibility workflow for large playsets](#compatibility-workflow-for-large-playsets)
9. [Validation and debugging](#validation-and-debugging)
10. [Codex failure-mode guardrails](#codex-failure-mode-guardrails)
11. [Worked examples](#worked-examples)
12. [Implementation handoff checklist](#implementation-handoff-checklist)

---

## Hard implementation rules

1. **Never mark work implemented from a roadmap row or note.** Require current generated-file evidence, active source evidence, and validation output.
2. **Treat same-ID objects as full-object overrides unless proven otherwise.** A same-ID object containing only `ai_weight` is usually not a field patch; it is an incomplete replacement.
3. **`ai_weight` is only one AI layer.** It helps choose among valid candidates. It does not create prerequisites, budgets, build slots, resource goals, or runtime proof.
4. **Scope is more important than syntax.** Syntactically valid country triggers in planet/system/starbase/megastructure scope are still wrong.
5. **Patch after parents, but do not blindly overwrite parent files.** Compatibility submods should normally load after Gigas/NSC3/ESC/Starbase Extended/PD/AI mods and touch the smallest safe object.
6. **Every full override needs provenance comments.** Record parent mod, file, object ID, source hash, changed fields, reason, and validation status.
7. **Static validation is not runtime proof.** It can prove files and references are plausible; it cannot prove AI behavior over decades.
8. **Prevent catastrophic AI collapse, not ordinary risk.** Excessive `factor = 0` gates make the AI safe but inert.

---

## How Stellaris loads mod files

### Folder model

Stellaris mods mirror the game folder. Public modding documentation identifies major modding directories including `common/`, `events/`, `localisation/`, `localisation_synced/`, `gfx/`, and `interface/`. **[CONFIRMED: public source]**

The practical rule is: place a file in the same relative folder the game expects, and define objects using IDs and fields supported by that folder's schema.

### Two layers of conflict

1. **File path conflicts.** Assets, GUI files, some map files, and path-loaded resources can be hidden by later files with the same path.
2. **Object ID conflicts.** Many `common/` folders load top-level objects keyed by ID. New IDs are usually additive; duplicate IDs are usually full-object override/last-winner risks. **[INFERRED: vanilla/mod pattern]**

### Additive versus full override

Examples:

```txt
# Additive if building_my_mod_anchor is new.
building_my_mod_anchor = { ... }
```

```txt
# Full-object override risk if building_research_lab_1 already exists.
building_research_lab_1 = {
    ai_weight = { weight = 10 } # likely incomplete and unsafe
}
```

Safer full override workflow:

```txt
# MYMOD OVERRIDE PROVENANCE
# Parent source: <active winning mod>/<file>
# Parent object: building_research_lab_1
# Parent hash: <sha256>
# Change: one ai_weight modifier only
building_research_lab_1 = {
    # complete active winning object preserved
}
```

### What "last mod wins" means

It means the later active source often supplies the winning file/object/key. It does **not** mean fields from two same-ID objects merge. It also does not mean launcher dependencies prove the final active order. Generate a conflict matrix instead.

### Duplicate object IDs

Duplicate IDs are how overrides happen, but they must be intentional. For every generated duplicate ID, record:

```csv
surface,object_id,winning_parent_mod,winning_parent_file,parent_hash,generated_file,changed_fields,reason,validation_status
```

If Codex cannot name the winning parent source, it is not ready to override.

---

## Descriptors, dependencies, launcher files, and DLC

The public modding tutorial describes `descriptor.mod` inside the mod folder and a launcher `.mod` file in the user Stellaris mod directory. The external `.mod` file points to the mod path. `supported_version` is a launcher compatibility indicator and does not itself control script loading. **[CONFIRMED: public source]**

Example local descriptor:

```txt
version="0.1"
name="My Stellaris 4.4.4 Compatibility Patch"
supported_version="4.4.*"
tags={
    "Balance"
    "Fixes"
}
```

Example external `.mod` file:

```txt
name="My Stellaris 4.4.4 Compatibility Patch"
path="mod/my_stellaris_444_patch"
supported_version="4.4.*"
```

### Dependencies

Descriptor dependencies document intent. They are not sufficient proof of final active order. The active playset may be represented by launcher files, `dlc_load.json`, Workshop descriptors, exported playset data, launcher databases, or user-provided evidence. The exact launcher format is version-sensitive; inspect the user's local files.

### `remote_file_id`

`remote_file_id` is Workshop metadata. Do not fabricate it for local-only mods. If publishing to Steam, let the launcher/Workshop workflow manage it.

### DLC gates

Use vanilla-verified DLC gates such as `host_has_dlc = "DLC Name"` when using DLC-only mechanics/assets. Do not invent DLC names. Preserve DLC gates in full overrides.

```txt
potential = {
    host_has_dlc = "Utopia"
    owner = { is_ai = yes } # if current scope is planet
}
```

---

## PDXScript syntax and parse traps

### Core syntax

```txt
# comment
key = value
key = {
    child = value
    child_block = {
        nested_key = yes
    }
}
```

Values include `yes`, `no`, integers, decimals, identifiers, `@variables`, and quoted strings. Comments start with `#`.

Inline and multiline blocks are equivalent if braces are correct:

```txt
OR = { is_ai = yes has_country_flag = my_flag }
```

Prefer multiline blocks for implementation review.

### Numeric comparisons

The public technology modding page shows numeric comparison syntax such as `has_level > 2` and `years_passed < 20`. **[CONFIRMED: public source]**

Only use comparisons where the trigger/field supports them:

```txt
num_pops >= 50
years_passed < 20
```

### Lists

```txt
category = { voidcraft particles }
prerequisites = { "tech_starbase_3" "tech_battleships" }
```

Follow local vanilla style for quoting.

### Weight blocks

Typical modifier-rule pattern:

```txt
ai_weight = {
    weight = 1
    modifier = {
        factor = 2
        owner = { has_technology = tech_starbase_4 }
    }
    modifier = {
        add = 5
        owner = { has_country_flag = my_mod_needs_defense }
    }
}
```

- `factor` multiplies.
- `add` adds.
- `factor = 0` is a hard veto in many contexts; use sparingly.
- Gameplay modifier blocks such as `planet_modifier = { planet_jobs_alloys_produces_mult = 0.10 }` are not weight-rule blocks.

### `always = no`

Safe only inside trigger-compatible blocks and only when disabling does not leave dangling references:

```txt
potential = { always = no }
allow = { always = no }
trigger = { always = no }
```

Unsafe in non-trigger blocks:

```txt
resources = { always = no }        # wrong
planet_modifier = { always = no }  # wrong
events = { always = no }           # wrong
```

### Localisation syntax

Localisation is YAML-like, not normal PDXScript. Public localisation docs describe `.yml`, UTF-8 BOM, language headers such as `l_english:`, key lines, and `localisation/replace` override behavior. **[CONFIRMED: public source]**

```yml
l_english:
 my_key:0 "Visible Text"
 my_key_desc:0 "Description."
```

---

## Scope rules

The public Scopes wiki explains `THIS`, `PREV`, `FROM`, `ROOT`, dot scopes, and scope-changing triggers/effects, and says wrong-scope errors appear in `error.log`. **[CONFIRMED: public source]**

### Common scope bridges

| Current scope | Country/empire checks usually require |
|---|---|
| country | direct trigger |
| planet | `owner = { ... }` |
| starbase definition AI weight | `from = { ... }` per CWTools starbase comments |
| megastructure `ai_weight` | `from = { ... }` per CWTools; current scope is system |
| pop/job | `owner`, `planet`, or block-specific scope; verify exact child block |
| fleet/ship | usually `owner = { ... }`, but verify |
| federation/diplomacy | action/event-specific actor/recipient scopes; use vanilla examples only |

### Confirmed CWTools scope anchors

- Technology `weight_modifier` and `ai_weight`: country scope.
- Buildings: planet scope for body/AI weight.
- Districts: planet scope for potential/allow/AI weight/AI production.
- Zones: planet scope for potential/unlock/AI production.
- Starbase buildings/modules/levels: starbase scope with `from = country` in definition comments.
- Megastructure `ai_weight`: `this/root = system`, `from = country`, `fromfrom = megastructure`.
- Pop jobs: scope varies by child block.

Wrong in planet scope:

```txt
has_technology = tech_mega_engineering
```

Correct:

```txt
owner = { has_technology = tech_mega_engineering }
```

Wrong in megastructure `ai_weight`:

```txt
is_ai = yes
has_technology = tech_mega_engineering
```

Correct:

```txt
from = {
    is_ai = yes
    has_technology = tech_mega_engineering
}
```

Read `scope_atlas.md` for the full scope atlas.

---

## AI modding model

### What `ai_weight` can do

It can adjust preference among valid candidates: technologies, buildings, districts, starbase modules/buildings, megastructures, perks, traditions, and other objects where the folder supports AI weights.

### What `ai_weight` cannot do

It cannot create build slots, resources, prerequisites, economic goals, budget, ship-design validity, or runtime proof. If an AI does not build a high-weight object, inspect economic plans, AI budgets, planet specialization, jobs/upkeep, prerequisites, and parent AI mod logic.

### AI layers

1. Availability: `potential`, `allow`, `possible`, prerequisites, DLC, country type.
2. Object scoring: `ai_weight`, `weight_modifier`, `ai_resource_production`.
3. Planet planning: `ai_planet_specialization`, designations, zones, jobs.
4. Economy: `common/economic_categories`, `common/ai_budget`, `common/economic_plans`.
5. Strategy: `ai_personalities`, scripted values/triggers, defines, war/claims/fleet logic.
6. Parent mods: Stellar AI/StarNet/Gigas/NSC3/ESC/Starbase Extended may replace the relevant layer.

### Construction pressure without hacks

Prefer this order:

1. Make the object valid only when sensible.
2. Add/correct `ai_resource_production`.
3. Add moderate `ai_weight` in correct scope.
4. Align planet specializations/designations/zones.
5. Adjust budgets/plans only with source proof.
6. Avoid event-forced construction unless exact source proof supports it.

Read `ai_modding_reference.md` for details.

---

## Folder-specific surfaces

The canonical machine-readable table is `folder_surface_matrix.csv`. It has one row per major modding surface with current scope, merge behavior, AI fields, common blocks, conflict risk, validation strategy, mistakes, and example anchor.

Preview:

| folder_path | object_type | current_scope | merge_behavior | ai_fields | conflict_risk |
| --- | --- | --- | --- | --- | --- |
| common/scripted_triggers/*.txt | scripted trigger | Caller-defined; executes in caller scope unless it changes scope internally | Top-level trigger IDs additive; duplicate ID last-winner/full replacement risk | Indirect: used by ai_weight/plans/events | Medium |
| common/scripted_effects/*.txt | scripted effect | Caller-defined; effect context from caller | Top-level effect IDs additive; duplicate ID last-winner/full replacement risk | Indirect; avoid direct AI construction hacks | High |
| common/scripted_values/*.txt | scripted value | Caller-defined; often country/planet/system depending use site | Top-level IDs additive; duplicate full override | Frequently used by AI weights, budgets, triggers | Medium-high |
| common/technology/*.txt | technology | weight_modifier and ai_weight: country (`this/root` country per CWTools) | New IDs additive; same ID full-object override/last winner | weight_modifier; ai_weight; ai_update_type if present locally | High |
| common/technology/tier/*.txt | technology tier/category support | Weight modifiers are country scope per CWTools | Top-level IDs additive; duplicate full override | weight_modifier | Medium-high |
| common/buildings/*.txt | planet building | Planet scope for body/ai_weight per CWTools; country via owner | New IDs additive; duplicate full-object override/last winner | ai_weight; ai_resource_production; ai_estimate_without_unemployment; resources category | High |
| common/districts/*.txt | planet district | Planet scope for potential/allow/ai_weight/ai_resource_production per CWTools | New IDs additive; duplicate full override | ai_weight; ai_resource_production; additional_ai_weight; ai_weight_coefficient | High |
| common/zones/*.txt | planet zone / zone slot | Planet scope for potential/unlock and ai_resource_production per CWTools | New IDs additive; duplicate full override | ai_resource_production; indirect construction pressure | High |
| common/pop_jobs/*.txt | pop job | Varies by child block: pop/pop_group, planet, country, system per CWTools comments | New job IDs additive; duplicate full override | Indirect: job weights/resources/economic categories | High |
| common/pop_categories/*.txt | pop category | Pop/pop_group-oriented; exact fields local-schema dependent | IDs additive; duplicate full override | Indirect via strata/job/economy | Medium-high |
| common/economic_categories/*.txt | economic category | Definition context; triggered subset scope depends on assigned resource block per wiki | IDs additive; duplicate full override | use_for_ai_budget; ai_use_parent_for_resources_upkeep; generated modifiers | Very high |
| common/ai_budget/*.txt | AI budget entry | Country/economic AI context; exact keys/scopes local 4.4.4 required | Top-level entries additive/override; global AI economy impact | resource; type; category; potential; fraction; static_min/static_max in historic examples only | Very high |
| common/economic_plans/*.txt | AI economic plan | Country AI planning context; exact syntax local 4.4.4 required | Plan IDs/objects additive/override; interlocked by stage/country type | goals; weights; scripted triggers/values; resource priorities | Very high |
| common/ai_resource_production/*.txt | AI resource production mapping | AI economy context; verify local scope | IDs additive/override | Resource valuation; interacts with object ai_resource_production | High |
| common/ai_planet_specialization/*.txt | AI planet specialization | Planet/country planning context; exact field scopes local | IDs additive; duplicate full override | Specialization weights/goals/allowed build preferences | High |
| common/personalities/*.txt | AI personality | Country/personality selection context; verify local fields | New IDs additive; duplicate full override | aggressiveness; bravery; trade; military/colony spending; ship preferences | High |
| common/defines/*.txt | defines/constants | No script scope; key-value constants | Namespace/key last-winner; file/load-order sensitive | Many AI constants for war/claims/economy/fleet depending current defines | Very high |
| common/starbase_buildings/*.txt | starbase building | Starbase scope with `from = country` per CWTools top-level comments | New IDs additive; duplicate full override | ai_weight; ai_build_at_chokepoint; ai_build_outside_chokepoint | High |
| common/starbase_modules/*.txt | starbase module | Starbase scope with `from = country` per CWTools top-level comments | New IDs additive; duplicate full override | ai_weight; ai_build_at_chokepoint; ai_build_outside_chokepoint | High |
| common/starbase_levels/*.txt | starbase level | Starbase scope with `from = country` for ai_weight per CWTools | IDs additive; duplicate full override | ai_weight; potential_home_base; level_weight indirect | High |
| common/megastructures/*.txt | megastructure/orbital structure | ai_weight: `this/root = system`, `from = country`, `fromfrom = megastructure` per CWTools | New IDs additive; duplicate full-object override/last winner | ai_weight; availability gates indirectly | Very high |
| common/ship_sizes/*.txt | ship size | Ship design/combat context; exact child scopes vary | New sizes additive; duplicate full override | AI design/fleet role fields if supported locally | Very high |
| common/component_templates/*.txt | component template | Component object; modifier scopes vary by child block | New components additive; duplicate full override | ai_weight/ai_tags if supported; auto-design scoring indirect | Very high |
| common/section_templates/*.txt | section template | Ship design context; slots/reference scopes schema-dependent | New sections additive; duplicate full override | Auto-design eligibility indirect | Very high |

High-risk surfaces requiring exact active source proof:

- `common/ai_budget/`
- `common/economic_plans/`
- `common/defines/`
- `common/diplo_actions/`
- species rights and related policy files
- `common/ship_sizes/`
- `common/component_templates/`
- `common/section_templates/`
- `common/global_ship_designs/`
- `common/on_actions/`
- `interface/`

---

## Compatibility workflow for large playsets

### Inspect active stack

1. Resolve active load order.
2. Resolve each enabled mod to an absolute folder.
3. Record descriptor metadata, dependencies, supported version, and Workshop ID if present.
4. Hash relevant files.
5. Parse top-level object IDs by folder.
6. Sort duplicate IDs by active load order.
7. Identify winning parent for every override.

Conceptual search:

```bash
rg -n "^\s*mega_shipyard_3\s*=" "<vanilla>/common" "<mods>/*/common"
rg -n "^\s*tech_mega_engineering\s*=" "<vanilla>/common" "<mods>/*/common"
```

### Gigastructural Engineering

Patch megastructure AI by inspecting Gigas' own AI triggers/weights/budget hooks first. Avoid copying giant files. For megastructure `ai_weight`, put country checks under `from`.

### NSC3

Avoid ship sizes, sections, and components without exact active source proof. Fleet AI tuning should usually go through budgets, personalities, technologies, and supported parent surfaces instead of direct component forcing.

### ESC NEXT

Check component sets, prerequisites, strategic resources, icons, and auto-design validity before AI technology/component weighting.

### Starbase Extended

Starbase definitions are starbase scope with `from = country` according to CWTools comments. Prefer moderate weights and chokepoint flags over direct build forcing. Verify level chains and module slots.

### Planetary Diversity

Verify planet classes, district sets, zones, zone slots, designations, and buildings. Do not assume vanilla district availability.

### Stellar AI / StarNet-style AI mods

Treat the AI mod as parent for AI layers. If object-level weights do nothing, inspect `economic_plans`, `ai_budget`, `ai_planet_specialization`, personalities, scripted triggers/values, and defines.

---

## Validation and debugging

Public modding docs describe logs under the Stellaris user data folder and mention `error.log`, `game.log`, `setup.log`, crash folders, and launch parameters including `-script_debug`, `-debug_mode`, `-debugtooltip`, `-logprefix`, `-logpostfix`, and `-logall`. **[CONFIRMED: public source]**

Static validation can prove:

- paths and descriptors are plausible;
- braces and quoting are plausible;
- object IDs exist;
- duplicate IDs and likely winners are known;
- references/localisation/icons exist;
- CWTools accepts supported triggers/effects/modifiers and scopes;
- generated files match current intent.

Static validation cannot prove:

- AI builds the object;
- economy survives;
- UI looks correct;
- diplomacy/war behavior is sane;
- a megastructure chain completes.

Read `validation_checklists.md` for detailed checklists and log triage.

---

## Codex failure-mode guardrails

Guard explicitly against:

- treating roadmap rows as proof;
- reporting implementation without current generated-file evidence;
- assuming `ai_weight` is the right AI layer;
- using country triggers directly in object scopes;
- adding unsupported `ai_weight` blocks;
- assuming all files merge additively;
- forgetting DLC gates;
- forgetting localisation;
- ignoring active load order and parent winning files;
- confusing static validation with runtime proof;
- over-gating AI into uselessness;
- editing diplomacy, species rights, ship designs/components/sections, personalities, or event-driven forcing without exact source proof;
- reverting newer user intent because older roadmaps looked authoritative.

---

## Worked examples

The `examples/` folder contains snippet patterns:

- `scripted_trigger.txt`
- `technology_weight.txt`
- `full_object_override_with_provenance.txt`
- `starbase_module_building_weight.txt`
- `megastructure_weight_country_scope.txt`
- `district_building_construction_pressure.txt`
- `economic_plan.txt`
- `ai_budget.txt`
- `localisation.yml.txt`
- `descriptor_files.txt`
- `bad_patch_and_corrected_version.txt`

Examples are patterns, not guaranteed drop-ins. Every trigger/effect/key must be verified against local 4.4.4 and the active playset.

---

## Implementation handoff checklist

- [ ] Target baseline says Stellaris 4.4.4.
- [ ] Active load order captured or explicitly unavailable.
- [ ] Parent winning source identified for every same-ID override.
- [ ] Full overrides have provenance comments.
- [ ] New visible objects have localisation and icons.
- [ ] DLC gates preserved or added where needed.
- [ ] Every AI weight has documented current scope.
- [ ] Country checks are wrapped correctly from non-country scopes.
- [ ] No unsupported AI fields were added.
- [ ] Conflict matrix generated.
- [ ] Static parse/CWTools validation run or unavailability documented.
- [ ] Runtime claims are only made from runtime evidence.
- [ ] Current user intent is not overwritten by stale notes.



---

## Loader behavior by folder family

This section summarizes practical load behavior for implementation decisions. Treat it as an audit guide, not a replacement for local parser proof.

| Folder family | Practical behavior | Override risk | Agent action |
|---|---|---|---|
| `common/*` object databases | Many folders load top-level keyed objects. New IDs are usually additive. Same ID is usually a full-object override or last-winner object replacement. | High for same-ID edits; medium for new IDs with references. | Parse top-level IDs by folder, find duplicates, identify winning parent, full-copy for overrides. |
| `common/scripted_triggers`, `common/scripted_effects`, `common/scripted_values` | Top-level helper IDs are callable from many places. New helpers are additive; duplicate helper names affect every caller that resolves to the winner. | High because broad helpers can change many systems. | Use mod-prefixed names, document expected caller scope, do not override vanilla/parent helpers unless proven. |
| `events` | Event namespaces and IDs are loaded globally. New IDs are additive; duplicate IDs or namespaces can conflict. Event effects/triggers are only proven when called. | High for on_action/event forcing and duplicate IDs. | Use unique namespace, document event scope contract, audit on_action hooks, runtime-test invoked events. |
| `localisation` | YAML-like key/value files. Keys are global per language. Later duplicate keys or `localisation/replace` can override visible text. | Medium; usually display breakage rather than crash, but bad encoding can break parsing. | Use UTF-8 BOM, language header, unique keys, audit missing `$KEY$` text. |
| `interface` | GUI and sprite definition files are often path/key sensitive. Duplicate widget/sprite names or same file paths are last-winner prone. | Very high with UI mods. | Avoid unless necessary; compare active UI mod winners; runtime visual proof required. |
| `gfx/interface`, `gfx/models`, portraits | Asset files and definitions are path/reference sensitive. Missing assets produce logs/placeholders/crashes depending use. | Medium-high. | Verify file paths, sprite names, entity references, icon sizes, DDS format if applicable. |
| `map` and galaxy generation | Parser behavior is specialized and load-order sensitive. | Very high. | Avoid in AI/economy compatibility patches unless exact source proof. |
| `sound`, `music`, `flags`, `prescripted_countries` | Mixed additive/path-key behavior. | Medium. | Follow local vanilla style; verify references and localisation. |
| `replace_path` in descriptor | Can hide entire vanilla/mod directories. | Extremely high. | Do not use unless intentionally replacing a complete directory and documenting every consequence. |

### Duplicate-ID audit algorithm

1. Build an ordered list of source roots: vanilla first, then enabled mods in active load order, then generated patch mod.
2. For each relevant folder, scan top-level IDs at brace depth 0.
3. Record `source_root, relative_file, object_id, line, file_hash`.
4. Sort by active order.
5. Mark the last source for each `folder_path/object_id` as the candidate winner.
6. For every generated duplicate, require:
   - parent winner path;
   - parent hash;
   - changed field list;
   - reason;
   - validation status.

Minimal output:

```csv
folder,object_id,source_order,source_mod,file,line,hash,is_winner,generated_override_reason
common/buildings,building_foundry_1,17,Stellar AI,path/file.txt,123,abc...,no,
common/buildings,building_foundry_1,99,My Patch,path/file.txt,8,def...,yes,AI weight compatibility
```

### What "last mod wins" does not prove

- It does not prove field-level merge.
- It does not prove dependencies are satisfied.
- It does not prove DLC availability.
- It does not prove an unsupported block is accepted.
- It does not prove AI will use the object.
- It does not prove a same-ID object was intentionally copied from the active parent.
- It does not prove a local patch survived a newer user change.

### `dlc_load.json` and DLC gates

`dlc_load.json` controls enabled DLC state at the user profile/launcher level. Script gates such as `host_has_dlc`, `has_dlc`, or local vanilla equivalents still matter in content files. A mod descriptor dependency is not a DLC gate. Preserve parent DLC gates unless deliberately changing compatibility and documenting the reason.

Agent checklist:

- Search parent object for DLC triggers.
- Search referenced objects for DLC-only technologies, components, origins, civics, traits, or assets.
- Preserve `host_has_dlc`/`has_dlc`/equivalent gates where found.
- In validation reports, distinguish "DLC disabled" from "object missing."

---

## Source evidence index

The full machine-readable source list is in `sources.csv`. Key public anchors used in this packet:

| Claim area | Primary source URL | Evidence type | Version note |
|---|---|---|---|
| Folder structure, descriptors, supported_version, logs | https://stellaris.paradoxwikis.com/Modding_tutorial | Public wiki | Current as accessed; verify edge cases in local 4.4.4 |
| Scope model, `root`/`from`/`prev`/wrong-scope logs | https://stellaris.paradoxwikis.com/Scopes | Public wiki | Core model stable; folder defaults version-sensitive |
| Localisation `.yml`, BOM, headers, replace behavior | https://stellaris.paradoxwikis.com/Localisation_modding | Public wiki | Page may have older-version markers; verify local behavior |
| Modifiers, economic categories, `use_for_ai_budget` | https://stellaris.paradoxwikis.com/Modifier_modding | Public wiki | Economic details require local 4.4.4 verification |
| Technology weight and `weight_modifier` | https://stellaris.paradoxwikis.com/Technology_modding | Public wiki + CWTools | Verify exact fields locally |
| AI personalities and aggression/bravery concepts | https://stellaris.paradoxwikis.com/AI_personalities | Public wiki | Page may be older than 4.4.4 |
| CWTools static validation capabilities | https://marketplace.visualstudio.com/items?itemName=tboby.cwtools-vscode | Tool documentation | Tool/config version-sensitive |
| CWTools Stellaris schema/config | https://github.com/cwtools/cwtools-stellaris-config | Public schema | Master branch; not guaranteed identical to 4.4.4 stable |
| Technologies schema hints | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/technologies_consolidated.cwt | CWTools schema | Strong public clue; local verification required |
| Megastructure AI scope hint | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/megastructures.cwt | CWTools schema | Critical wrong-scope prevention; local verification required |
| Starbase AI scope hints | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/starbases_consolidated.cwt | CWTools schema | Verify against vanilla and Starbase Extended |
| Building/district/zone/job AI hints | CWTools `buildings.cwt`, `districts.cwt`, `zones.cwt`, `jobs_and_social_strata.cwt` | CWTools schema | Verify against local 4.4.4 and active mods |
| Edict/policy/decision scope hints | CWTools `edicts.cwt`, `policies.cwt`, `decisions.cwt` | CWTools schema | Master branch; verify local 4.4.4 |
