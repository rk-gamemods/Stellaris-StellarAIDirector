# Stellaris AI Modding Reference for 4.4.x Heavy Playsets

Target: Stellaris PC 4.4.4 stable. Public-source access date: 2026-07-08.

## Core principle

Stellaris AI behavior is layered. `ai_weight` is useful, but often not decisive. In a heavy playset, an AI mod may override budgets, economic plans, planet specializations, personalities, scripted triggers, scripted values, and defines.

## AI layers

| Layer | Files/surfaces | Controls | Static checks |
|---|---|---|---|
| Availability | potential/allow/possible/prereq/DLC | Whether object can be considered | CWTools; rg refs; preserve gates |
| Object scoring | ai_weight, weight_modifier, ai_resource_production | Candidate preference | folder support and scope audit |
| Economic categories | economic_categories/resources | modifier hierarchy and budget categories | category exists; use_for_ai_budget |
| Planet planning | ai_planet_specialization, designations, zones, jobs | what planets want | compare active specializations |
| Budgets | common/ai_budget | spending caps/reserves | active parent source; runtime economy proof |
| Economic plans | common/economic_plans | strategic resource goals | active AI mod plan inspection |
| Strategy | personalities, scripted triggers/values, defines | aggression/fleet/diplomacy | source proof; runtime proof |
| Scripted forcing | events/on_actions/scripted effects | direct actions | high risk; runtime proof required |

## `ai_weight`

Good for:

- moderate preferences among valid choices;
- AI-only vetoes for catastrophic cases;
- aligning modded objects with verified prerequisites;
- technology draw/selection, buildings/districts, starbases, megastructures where supported.

Bad for:

- missing budgets;
- missing resources;
- missing prerequisites;
- invalid planet/zone slots;
- auto-design/component-set failures;
- economy plans that never ask for the resource;
- runtime proof.

Start moderate:

```txt
modifier = { factor = 1.25 <condition> = yes }
modifier = { factor = 1.5  <condition> = yes }
modifier = { factor = 2    <strong_condition> = yes }
```

Use `factor = 0` only for invalid/catastrophic states.

## Technology AI

`weight_modifier` affects technology draw chance per public tech docs. CWTools supports technology `ai_weight` with country scope.

Workflow:

1. Find active winning tech object.
2. Verify prerequisites, tier, category, icons, localisation.
3. For same-ID edits, full-copy object with provenance.
4. Use direct country triggers.
5. Avoid huge multipliers that destroy tech diversity.

```txt
ai_weight = {
    weight = 1
    modifier = {
        factor = 1.5
        is_ai = yes
        has_technology = tech_starbase_3
    }
}
```

## Buildings, districts, zones, jobs

Construction pressure requires:

1. Valid `potential`/`allow` and prerequisites.
2. Slots/zone slots.
3. Planet specialization/designation desire.
4. `ai_resource_production` or comparable production signal.
5. Budget/resource support.
6. Jobs that are fillable and not economically destructive.

Planet-scoped pattern:

```txt
ai_weight = {
    weight = 5
    modifier = {
        factor = 2
        owner = { is_ai = yes }
    }
}
```

If it fails, inspect `common/ai_planet_specialization`, `common/economic_plans`, `common/ai_budget`, jobs, upkeep, districts, and zones.

## Starbase AI

CWTools confirms starbase modules/buildings/levels have `ai_weight`; starbase definition comments use starbase scope with `from = country`.

```txt
ai_weight = {
    weight = 10
    modifier = {
        factor = 0
        from = { is_ai = no }
    }
    modifier = {
        factor = 1.5
        from = { is_at_war = yes }
    }
}
```

Use placement booleans if supported:

```txt
ai_build_at_chokepoint = yes
ai_build_outside_chokepoint = no
```

Do not starve ship budgets by making every starbase module enormous.

## Megastructure AI

CWTools states megastructure `ai_weight` is system scope, `from = country`, `fromfrom = megastructure`.

```txt
ai_weight = {
    weight = 1
    modifier = {
        factor = 0
        from = { is_ai = no }
    }
    modifier = {
        factor = 2
        from = {
            has_technology = tech_mega_engineering
        }
    }
}
```

Megastructure construction often depends more on budgets/plans/resources/placement caps than object weight. For Gigas, inspect Gigas AI helpers before patching.

## Economic categories

Public modifier docs describe economic categories, generated modifiers, and `use_for_ai_budget`. Resource blocks assigned to economic categories determine applicable modifiers and AI budget categories.

Do not add categories casually. If adding one:

- define generated modifiers intentionally;
- add localisation for generated modifiers when visible/logged;
- decide whether `use_for_ai_budget` is required;
- audit all `resources = { category = ... }` users;
- verify against local 4.4.4.

## `ai_budget`

High risk. Exact 4.4.4 syntax must come from local vanilla or active AI mod. Public docs confirm relation to `common/ai_budget`, but not enough current syntax to invent objects.

Rules:

1. Treat active AI mod as parent.
2. Search for resource/category entries.
3. Copy exact active winning entry.
4. Change the smallest leaf.
5. Keep reserves/caps conservative.
6. Runtime proof required for AI economy claims.

Historic/community search terms only: `resource`, `type`, `category`, `potential`, `fraction`, `static_min`, `static_max`.

## `economic_plans`

High risk. These files change across patches and AI mods often use them for integrations.

Use for:

- stage/country-type resource goals;
- crisis-scale economies;
- machine/hive/special country plans;
- resource and construction priorities.

Do not edit without local source proof. Do not remove fallback goals. Avoid hard blockers that stop all normal risk.

## Personalities, aggression, claims, war readiness

Public AI personality docs say personalities affect foreign policy, domestic policy, and fleet budgeting, but the page observed was marked PC 4.2. Verify local 4.4.4.

For the detailed war-start chain, use
`research/stellar-ai/war-mechanics-reference-2026-07-08/`. That packet covers
claims, casus belli, war goals, declare-war gates, personality war fields,
war defines, fleet-use separation, and passive-galaxy failure modes. Treat it
as a research packet until the specific values are verified against local
vanilla files and active-stack winning files.

Tuning order:

1. Inspect personalities.
2. Inspect fleet/naval budgets and economic plans.
3. Inspect ship design availability under NSC3/ESC.
4. Tune verified scripted triggers/values.
5. Use defines only as last resort.

Risks from defines:

- far-away claims waste influence;
- more wars without logistics;
- fleet overbuilding starves economy;
- starbase spending crowds out ships;
- crisis economies collapse due to upkeep.

## High-risk/high-reward AI behavior

Goal: prevent catastrophic collapse, not ordinary economic risk.

Good gates:

- avoid megastructure construction during severe alloy deficit;
- reduce starbase spam during active existential war;
- reserve rare resources for component upkeep.

Bad gates:

- require huge stockpiles before every build;
- never declare war unless overwhelmingly stronger;
- never invest in economy during war.

## AI patch decision tree

```text
Need AI to build/use X?
  ├─ availability passes?
  ├─ folder supports AI field?
  ├─ scope correct?
  ├─ active parent object identified?
  ├─ budget/resource goal exists?
  ├─ planet/system/starbase logic considers X?
  ├─ active AI mod overrides this layer?
  └─ minimal patch + validation
```
---

## Practical AI tuning matrix

| Goal | First surface to inspect | Secondary surfaces | Good patch shape | Bad patch shape |
|---|---|---|---|---|
| More AI alloy economy | buildings, districts, jobs, planet specialization | economic_plans, ai_budget, resource production hints | moderate planet-scope `ai_weight`, `ai_resource_production`, specialization alignment | event-forcing foundries everywhere |
| More research prioritization | technology `weight_modifier` and `ai_weight` | economic plans for researcher upkeep, labs, jobs | country-scope tech weights + lab construction pressure | massive factor on one tech while prerequisites/budgets fail |
| More starbase defense | starbase modules/buildings, levels | budgets, chokepoint logic, personalities | starbase-scope AI weights with `from` country checks | every starbase maxed, bankrupting ship budget |
| More megastructures | megastructure weights, tech prereqs | ai_budget/economic_plans, scripted values, Gigas AI helpers | system-scope weight with `from` country readiness guard | direct event construction or country triggers in system scope |
| Higher naval cap use | jobs/buildings/starbases/techs giving naval cap | ship designs, budgets, personalities, defines | resource and ship-design validity first; conservative budget tuning | defines forcing overbuilding without economy |
| More aggression/claims | personalities, claims logic, war readiness triggers | fleet/economy budgets, relations, distance defines | small targeted changes for specific personality/country type | global aggression/claim-distance defines |
| Crisis-scale economy | economic_plans, ai_budget, country types | scripted triggers/values, jobs, megastructures | staged plan that preserves minerals/energy/CG/alloys | all-in alloy economy that collapses amenities/CG/energy |
| Modded component adoption | technology/component prerequisites, auto-design validity | ship sizes/sections, component sets, resources | prove design validity before weight changes | weight components that cannot fit or lack resources |

## `ai_weight` versus `weight_modifier`

Use `weight_modifier` when the vanilla object already uses it as part of selection/draw chance, such as technology draw weighting. Use `ai_weight` when the object schema supports AI selection weighting. Some surfaces support both, some support one, and some support neither. Adding an unsupported block is at best ignored and at worst a parser/schema error.

Implementation rule:

```txt
# Do not add this unless the exact folder schema supports it.
ai_weight = { weight = 1 }
```

Verification rule:

```bash
rg -n "ai_weight|AI_weight|weight_modifier" "<vanilla>/common/<same_folder>" "<enabled_mods>"
```

Then check CWTools diagnostics and local examples.

## Economic plans and budgets: practical local audit

Because public sources do not provide enough 4.4.4-stable syntax to invent safe `economic_plans` or `ai_budget` entries, agents should audit locally:

```bash
rg -n "alloys|consumer_goods|energy|minerals|strategic|megastructure|starbase|naval" "<vanilla>/common/economic_plans" "<enabled_mods>"
rg -n "alloys|consumer_goods|energy|minerals|strategic|megastructure|starbase|naval" "<vanilla>/common/ai_budget" "<enabled_mods>"
rg -n "use_for_ai_budget|economic_category" "<vanilla>/common" "<enabled_mods>"
```

Create `ai_layer_audit.csv`:

```csv
layer,file,object_id,parent_mod,winning,scope_or_schema,resource_or_budget,changed,no_change_reason
economic_plan,path,id,Stellar AI,yes,local schema,alloys,proposed,
ai_budget,path,id,vanilla,no,local schema,starbase,,parent mod wins
```

Only after that decide whether the problem is object preference, resource demand, budget allocation, or construction availability.

## Construction pressure without direct forcing

Preferred sequence for a new/modded building, district, or zone:

1. Verify object is available to the AI country and planet.
2. Verify slots/zone slots/district caps.
3. Verify jobs are fillable and outputs/upkeep are not catastrophic.
4. Verify resource categories and `ai_resource_production` hints.
5. Verify planet specialization/designation values.
6. Add moderate `ai_weight` in planet scope.
7. If still unused, inspect economic plans/budgets.
8. Only consider scripted construction effects with exact vanilla/mod proof and runtime tests.

Direct construction events are fragile because they can ignore build queues, resources, prerequisites, planet suitability, unemployment, district caps, and parent AI mod planning.

## Fleet, naval-cap, war, claims, and raiding

Do not solve fleet weakness by only increasing aggression. A more aggressive AI with invalid ship designs or a weak economy loses faster.

Safer tuning order:

1. Confirm ship designs are valid under NSC3/ESC.
2. Confirm component prerequisites and strategic resources are available.
3. Confirm naval-cap sources are buildable and not too expensive.
4. Confirm fleet budget and economic plan can afford alloys/upkeep.
5. Confirm personalities/war readiness allow reasonable aggression.
6. Tune claims/distance/war defines only after the above.

Define risks:

- `declaration distance` or claim-distance style changes can waste influence and fleet travel time.
- aggression base increases can produce wars without logistics.
- bravery increases can suicide fleets.
- naval-cap pressure can bankrupt energy/alloy economies.
- starbase overinvestment can crowd out mobile fleets.

## Research prioritization

Technology AI has two distinct problems:

1. The tech must appear in the draw pool.
2. The AI must choose it when drawn.

Therefore inspect:

- prerequisites;
- `area`, `tier`, and `category`;
- feature flags or unlocks expected by parent mods;
- `weight` and `weight_modifier`;
- `ai_weight` if supported locally;
- alternatives with much higher weight;
- research economy and scientist/agenda modifiers.

Use moderate factors. Huge factors on one path can prevent the AI from picking economy, naval cap, strategic resource, or prerequisite technologies.

## Megastructure spending under Gigastructural Engineering

For Gigas-style megastructures, assume object-level `ai_weight` is only one layer.

Audit:

```bash
rg -n "<mega_id>|ai_weight|economic_plan|ai_budget|scripted_value|scripted_trigger" "<gigas_mod>/common" "<gigas_mod>/events"
```

Check:

- buildable stage chain;
- country flags/limits;
- system placement rules;
- required technologies/ascension perks/traditions;
- resource and influence costs;
- parent-mod scripted triggers;
- crisis/katzen/aeternum/special-country logic if present;
- AI budget hooks.

Patch principle: prevent catastrophic collapse, but still allow some expensive strategic investment. Do not require enormous stockpiles before every build unless runtime evidence shows collapse.

## Starbase investment under Starbase Extended

Starbase investment competes with ships and alloys. Patch only after identifying the active parent object.

Good patterns:

```txt
modifier = {
    factor = 1.5
    from = { is_at_war = yes }
}

modifier = {
    factor = 0
    from = { has_country_flag = my_mod_ai_starbase_spending_pause }
}
```

Bad patterns:

```txt
modifier = { factor = 100 from = { is_ai = yes } }
```

Starbase Extended and NSC3 may alter module slots, sections, or defensive role. Preserve all parent fields.

## Compatibility with Stellar AI / StarNet-style mods

If an AI overhaul is active, treat it as the parent for AI logic even when vanilla has a similarly named object. The mod may replace:

- `economic_plans`;
- `ai_budget`;
- `ai_planet_specialization`;
- building/district weights;
- personalities;
- scripted values/triggers;
- defines.

Do not override those layers blindly. Prefer adding mod-prefixed scripted triggers/values and small compatibility patches that preserve the parent mod's strategy.

## Runtime evidence boundaries

Static validation can say: "This AI weight is syntactically valid, in the right scope, and wins load order."

It cannot say: "The AI will build this in a real game."

Runtime evidence for AI claims should include:

- game version and checksum/modlist;
- active load order;
- start settings;
- observer duration;
- relevant logs;
- save/audit extraction showing AI built/researched/used the target;
- comparison against control or prior behavior when feasible.

If runtime is not allowed, report the patch as statically validated only.
