# Stellar AI Director Full Replacement Plan

Date: 2026-07-06
Target when written: Stellaris 4.4.4 stable, for the user's fixed high-power modded playset. Current target as of 2026-07-08 is Stellaris 4.4.5 stable/current local install; revalidate this plan's implementation assumptions against 4.4.5 before further use.
Status: Planning document. This is the required roadmap before more AI-weight tuning.

## Purpose

Stellar AI Director must become a full mod-set-aware AI policy layer, not a pile of broad economic guesses. The AI cannot reason like a player. Every important modded object has to be inventoried, classified, connected to prerequisites, and given an explicit rule for when the AI should pursue it, ignore it, delay it, or exploit it.

The goal is to make AI empires understand the high-scale playset well enough to progress toward the same power curve a human player uses: Mega Engineering, economy megastructures, Mega Shipyards, Gigastructural planetcraft, war moons, systemcraft, NSC3 hulls, ESC components, tall/habitat scaling, and conquest when boxed in.

## Current Problem

The current Director has partial scaffolding:

- generated reference validation for some technologies/resources/scripted objects;
- a megastructure ROI matrix for many Gigas/NSC3 objects;
- a broad replacement economic plan;
- special-resource budget objects for a few Gigas resources;
- integration-surface audits that identify some parent objects and whether they have AI weights.

That is not enough. A larger alloy reserve does not help if the AI is not explicitly guided into the tech, AP, prerequisite structures, special resources, and build paths that actually spend those alloys. The Director needs complete object coverage and explicit decision logic.

## Non-Goals

- Do not launch Stellaris or run observer scenarios by default.
- Do not encode fast-moving strategy assertions as unit tests.
- Do not treat Stellar AI as the strategic baseline after the opening curve.
- Do not handwrite one-off weights without first recording the object and prerequisite path in the atlas.
- Do not overwrite parent mod AI support blindly. First identify whether it exists, what it expects, and whether it is sufficient.

## Source Mods

The initial full-replacement scope is the active high-scale AI playset:

| mod | workshop/source id | role in the plan |
| --- | --- | --- |
| Stellaris vanilla 4.4.5 | local Steam install | current baseline object model, valid script surfaces, vanilla AI patterns |
| Stellar AI | `3610149307` | early-game reference only, not late-game strategy baseline |
| Gigastructural Engineering & More (4.4) | `1121692237` | primary high-scale megastructure/planetcraft/systemcraft target |
| NSC3 | `683230077` | ship classes, Mega Shipyard support, military scaling |
| Extra Ship Components NEXT | `2648658105` | advanced component and reactor/shield/weapon chains |
| Starbase Extended 3.0 | `3250900527` | station defense and starbase scaling |
| Universal Resource Patch | active dependency | resource compatibility and shared resource definitions |

Compatibility patches and other enabled mods must be added to the atlas when they define or override objects in AI-relevant folders.

## Deliverables

The project needs these durable artifacts before serious behavior tuning continues:

| artifact | format | purpose |
| --- | --- | --- |
| Object atlas | CSV/JSONL/SQLite | every relevant vanilla and modded object with source file, type, ownership, replaces/overrides, and load-order winner |
| Dependency graph | JSON/SQLite edges | prerequisites, upgrade chains, event gates, flag gates, resource gates, build chains |
| AI support map | CSV/Markdown | source AI weights, scripted AI helpers, budgets, economic plans, ship design logic, event AI paths |
| Strategic role map | CSV/Markdown | each object classified as economy, research, fleet, defense, unlock, prerequisite, trap, flavor, crisis-only, etc. |
| Policy matrix | CSV/JSONL | exact AI action for each object: rush, build, delay, avoid, exploit, reserve, or leave parent AI in control |
| Generated AI patch | mod files | generated weights, budgets, economic plans, scripted triggers/effects, and overrides produced from the policy matrix |
| Static validator | Python | verifies generated files parse and all referenced Stellaris/mod objects exist |
| Coverage report | Markdown | counts covered vs uncovered objects by mod/type/strategic tier |

## Object Atlas Scope

The atlas must cover all AI-relevant object surfaces, not just megastructures.

Required folders and object types:

| surface | examples of needed data |
| --- | --- |
| `common/technologies` | prerequisites, tier, area, rare status, feature flags, weight modifiers, unlocks |
| `common/ascension_perks` | prerequisites, AI weights, unlock chains, crisis/mega paths |
| `common/traditions` | unlock dependencies, modifiers, AI weights |
| `common/megastructures` | cost, upkeep, produces, stages, upgrades, build limits, star/planet restrictions, AI weights |
| `common/buildings` | cost, upkeep, jobs, produces, planet restrictions, empire restrictions, AI weights |
| `common/districts` | cost, jobs, planet type restrictions, AI weights |
| `common/pop_jobs` | resources produced/consumed, strata, weights, specialist bottlenecks |
| `common/resources` | market status, strategic use, stockpile behavior, compatibility patch ownership |
| `common/deposits` | resource unlocks, planet/star/system requirements, megastructure hooks |
| `common/ship_sizes` | fleet role, buildability, naval cap, logistics/trade upkeep, AI role |
| `common/component_templates` | component tier, power, resources, prerequisites, AI tags |
| `common/section_templates` | hull compatibility, weapon slots, AI tags |
| `common/starbase_modules` | defense/economy/military role, prerequisites, AI weights |
| `common/starbase_buildings` | defense/economy/military role, prerequisites, AI weights |
| `common/edicts`, `common/policies`, `common/decisions` | AI weights, economy/military leverage, prerequisites |
| `common/scripted_triggers` | reusable condition gates, parent AI hooks |
| `common/scripted_effects` | hidden build/unlock/economy/event behavior |
| `common/script_values` | weight formulas and dynamic costs |
| `events` | event gates, flags, country state, special unlocks, crisis and fallen-empire paths |
| `common/ai_budget`, `common/economic_plans` | existing budget categories and economy target behavior |
| `common/personalities`, `common/country_types` | special AI behavior, Fallen Empire and crisis exceptions |

The atlas must distinguish objects that merely exist from objects that matter strategically. Low-impact flavor objects still need validity coverage, but they do not need the same policy depth as planetcraft/systemcraft.

## Atlas Schema

Each atlas row should include:

| field | meaning |
| --- | --- |
| `object_id` | script key, such as `giga_war_moon`, `planetcraft_printer_0`, or `esc_tech_dark_matter_power_core_2` |
| `object_type` | technology, megastructure, ship_size, component, building, etc. |
| `mod_id` / `mod_name` | owning source mod |
| `source_file` | file where object is defined |
| `load_winner` | which mod wins if object is overridden |
| `source_has_ai_weight` | whether the defining object has an AI block |
| `ai_weight_summary` | brief parsed summary of existing AI behavior |
| `cost` | full resource cost, preserving unpriced resources |
| `upkeep` | full upkeep/logistics cost |
| `produces` | resources, modifiers, jobs, shipyard capacity, naval cap, build speed, etc. |
| `prerequisites` | explicit tech/AP/tradition/object requirements |
| `potential_allow_gates` | potential/allow/custom trigger constraints |
| `event_flags` | flags or event chains required |
| `upgrade_from` / `upgrades_to` | stage graph |
| `unlocks` | objects unlocked by this object |
| `strategic_role` | economy, research, fleet, defense, unlock, prerequisite, trap, flavor |
| `strategic_tier` | opening, early, midgame, crisis-prep, planetcraft, systemcraft, fallback |
| `policy_status` | parent_ai_ok, needs_direct_weight, needs_route_policy, avoid, unknown |
| `director_action` | rush, build, reserve, delay, avoid, exploit, observe |
| `validation_status` | ok, missing_reference, unresolved_script, parser_gap, manual_review |

## Dependency Graph

The graph is the core of the work. It must answer questions like:

- What exactly unlocks planetcraft?
- What exactly unlocks war moons?
- What exactly unlocks systemcraft?
- Which techs/APs/traditions are mandatory?
- Which prerequisite structures must exist first?
- Which special resources must be produced before construction is realistic?
- Which event or country flags block the path?
- Which objects are traps or dead ends for normal AI empires?

Required edge types:

| edge | example |
| --- | --- |
| `requires_technology` | object requires `tech_mega_engineering` |
| `requires_ascension_perk` | object requires `ap_celestial_printing` |
| `requires_tradition` | object gated behind tradition adoption/completion |
| `requires_structure` | systemcraft requires prior planetcraft/war moon infrastructure |
| `requires_ship_count` | systemcraft requires owned `giga_planet_behemoth` or `giga_war_moon` counts where source confirms |
| `requires_resource_income` | object needs sentient metal, negative mass, megaconstruction, dark matter, etc. |
| `requires_resource_stockpile` | object has one-time special-resource cost |
| `requires_star_or_planet_class` | build target constraints |
| `requires_country_flag` | event-driven unlocks |
| `sets_country_flag` | event/object creates future gate |
| `unlocks_object` | tech unlocks component, ship, building, megastructure |
| `upgrades_to` | stage chain |
| `replaces_or_overrides` | load-order conflict relation |

The graph should be queryable by goal. Example:

```text
goal: systemcraft
required path:
  tech -> AP -> planetcraft -> war moon count -> systemcraft tech chain -> special resource economy -> build site
missing current policy:
  direct tech weights
  direct AP weights
  construction weights
  ship count build pressure
  special resource reserve policy
```

## Existing AI Support Map

For every object with AI impact, determine whether parent mods already provide support.

Classify existing support as:

| status | meaning |
| --- | --- |
| `parent_ai_complete` | source appears to define useful AI weights and gates |
| `parent_ai_partial` | has AI weights but misses high-scale strategy, prerequisites, or crisis pacing |
| `parent_ai_present_but_wrong_goal` | AI support exists but optimizes for vanilla-scale or non-user playset assumptions |
| `parent_ai_absent` | no AI support found |
| `parent_ai_unknown` | parser could not resolve support yet |

For `parent_ai_complete`, the Director should usually push prerequisites and resources rather than overwrite the object.

For `parent_ai_partial`, the Director should add pressure around the missing prerequisite, economy, or priority gate.

For `parent_ai_absent`, the Director needs direct policy.

## Strategic Progression Routes

The Director needs explicit routes, not generic economic pressure.

Initial route set:

| route | outcome |
| --- | --- |
| `mega_engineering_core` | reach Mega Engineering and base megastructure construction |
| `mega_shipyard_core` | unlock and exploit Mega Shipyard / NSC3 shipyard infrastructure |
| `economy_megastructure_core` | Dyson, gigaforge, Nidavellir, Matrioshka, and other economy multipliers |
| `gigas_special_resource_core` | sentient metal, negative mass, megaconstruction/supertensiles, dark matter dependencies |
| `planetcraft_route` | tech/AP/structure chain to planetcraft |
| `war_moon_route` | tech/build chain to war moons or equivalent lunar combat hulls |
| `systemcraft_route` | full chain to systemcraft, including prerequisite ship counts and APs |
| `nsc3_capital_hull_route` | NSC3 dreadnought/carrier/flagship/supercapital hull unlocks and shipyard support |
| `esc_component_route` | high-tier reactors, shields, weapons, strike craft, sensors, and aux components |
| `crowded_tall_route` | habitats, planetary capacity, buildings, districts, jobs, and pop growth when boxed in |
| `conquest_escape_route` | fleet economy, war declarations/claims/subjugation pressure when boxed in |
| `fallen_empire_benchmark_route` | target curve for matching fallen empire planetcraft/war moon/fleet scale |

Each route must have:

- required objects;
- desired timing windows;
- blocking conditions;
- economy/resource prerequisites;
- fallback choices;
- generated AI weights or parent-AI nudges;
- validation queries.

## Policy Matrix

The policy matrix is the source of truth for generated AI behavior. No direct weight should be written without a policy row.

Required policy fields:

| field | examples |
| --- | --- |
| `object_id` | `planetcraft_printer_0` |
| `route_id` | `planetcraft_route` |
| `priority_band` | mandatory, high, medium, low, avoid |
| `timing` | before 2250, 2250-2300, 2300-2350, 2350+ |
| `empire_context` | boxed-in, wide, tall, militarist, crisis-threatened, fallen-empire-neighbor |
| `prereq_state` | missing tech, missing AP, missing resource, build-ready, upgrade-ready |
| `desired_action` | research, build, upgrade, reserve, design_ship, increase_income, avoid |
| `weight_formula` | named formula generated into mod files |
| `safety_gates` | no core deficit, war state, minimum resource income, trade/logistics floor |
| `parent_ai_strategy` | reuse, supplement, override |
| `notes` | source-specific reasoning |

## Implementation Phases

### Phase 0: Freeze Scope And Tool Contract

Create the object-atlas pipeline and stop ad hoc tuning.

Tasks:

- Create an `object_atlas` generator in `tools/`.
- Define the atlas CSV/JSONL schema.
- Define a graph edge schema.
- Define static validation rules.
- Keep tests limited to generated file validity and object reference validity.
- Do not launch the game.

Outputs:

- `research/stellar-ai/object-atlas/schema.md`
- `research/stellar-ai/object-atlas/object-atlas-2026-07-06.csv`
- `research/stellar-ai/object-atlas/dependency-edges-2026-07-06.csv`
- static validator updates.

Acceptance:

- atlas generator runs over vanilla plus required parent mods;
- every row records source file and object type;
- generated references validate against the atlas.

### Phase 1: Exhaustive Object Inventory

Inventory all relevant objects from vanilla, Stellar AI, Gigas, NSC3, ESC, Starbase Extended, Universal Resource Patch, and compatibility patches.

Tasks:

- Parse all required `common/` folders and event files.
- Record every top-level object in supported folders.
- Record whether each object has `ai_weight`, `ai_weight_modifier`, `ai_will_do`, `weight`, or scripted AI helper usage.
- Record object overrides and load-order winners.
- Preserve unknown/unparsed objects for manual review instead of dropping them.

Acceptance:

- coverage report shows object counts by mod and type;
- no supported folder silently skipped;
- unknown parser cases are listed with file and line context.

### Phase 2: Cost, Output, And Resource Model

Turn object data into real resource knowledge.

Tasks:

- Extract `cost`, `upkeep`, `produces`, `modifier`, jobs, deposits, shipyard capacity, naval cap, build speed, build cost, and build time effects.
- Preserve every resource, including unpriced/special resources.
- Record resource market status separately from strategic status.
- Identify resources that cannot be bought/sold but are still required.
- Track trade as logistics/upkeep headroom, not market value.

Acceptance:

- every cost/upkeep/produces resource either resolves to a known resource or appears in a missing-resource report;
- special resources are not flattened into alloy/energy guesses;
- each strategic resource has producers and consumers linked where source files expose them.

### Phase 3: Dependency Graph

Build the prerequisite graph.

Tasks:

- Extract prerequisites from techs, APs, traditions, scripted triggers, potential blocks, allow blocks, events, and upgrade chains.
- Extract hidden gates from scripted effects and event flags when possible.
- Add manual edge annotations where script logic is too complex for the parser.
- Build goal queries for planetcraft, war moons, systemcraft, Mega Shipyard, ESC high-tier components, and NSC3 capital ships.

Acceptance:

- every high-scale route has a queryable dependency path;
- unresolved gates are listed as blockers with source file references;
- graph can answer "what does AI need next?" for each route.

### Phase 4: Existing AI Support Reverse Engineering

Find and classify parent AI infrastructure.

Tasks:

- Parse AI weights inside Gigas, NSC3, ESC, Starbase Extended, Stellar AI, and vanilla.
- Identify scripted AI helper triggers/effects.
- Identify budget and economic-plan categories parent mods expect.
- Identify event-driven AI behavior.
- Classify support as complete, partial, wrong-goal, absent, or unknown.

Acceptance:

- support map has one row per strategic object;
- parent AI support is reused where it is good;
- missing or insufficient support has explicit gap rows.

### Phase 5: Strategic Role And Priority Classification

Classify every object into strategic meaning.

Tasks:

- Define role taxonomy.
- Assign every object a role and confidence.
- Use source evidence first, heuristic classification second, manual review for high-impact unknowns.
- Separate critical routes from flavor/noise.

Required role classes:

- mandatory unlock;
- economy multiplier;
- research multiplier;
- fleet production;
- direct combat power;
- defensive infrastructure;
- tall scaling;
- conquest enabler;
- special resource producer;
- special resource consumer;
- prerequisite-only;
- trap/avoid;
- flavor/low impact;
- unknown/manual review.

Acceptance:

- all objects have a role, even if `unknown/manual_review`;
- all high-impact unknowns are listed before policy generation.

### Phase 6: Route Policy Design

Design the actual AI roadmap.

Tasks:

- Build route policies for Mega Engineering, economy megastructures, planetcraft, war moons, systemcraft, NSC3 hulls, ESC components, tall scaling, and conquest escape.
- Define timing windows and fallback choices.
- Define when to reuse parent AI support and when to override.
- Define resource and tech gates for each route.

Acceptance:

- each route has explicit "next best action" rules;
- policy rows map to existing objects in the atlas;
- no generated weight refers to an object outside the atlas.

### Phase 7: Generated AI Surfaces

Generate AI patch files from the policy matrix.

Candidate generated surfaces:

- technology weights;
- ascension perk weights;
- megastructure build weights;
- ship size and ship design support;
- component selection weights;
- starbase module/building weights;
- building and district weights;
- economic plans;
- AI budgets;
- scripted triggers and script values.

Rule:

Do not generate an override unless the atlas row says the Director owns that surface and the conflict report records the reason.

Acceptance:

- every generated reference resolves against the atlas;
- every generated override has an ownership note;
- parent AI support is not overwritten unless policy says override.

### Phase 8: Static Validation

Keep tests universal and non-strategic.

Tests should only verify:

- generated files are in supported mod folders;
- generated PDXScript parses;
- localization files are structurally valid;
- no unresolved template placeholders exist;
- every referenced technology/resource/scripted trigger/scripted value/object exists in vanilla, parent mods, or generated files;
- override targets exist;
- dependency graph references valid nodes.

Tests should not verify:

- exact desired target numbers;
- exact behavior choices;
- launch proof;
- observer outcomes;
- whether a strategy is "good."

### Phase 9: Human Review Packets

Create review packets for manual decisions.

Required packets:

- high-impact objects with no AI support;
- high-impact objects with existing but suspicious AI support;
- route blockers with unresolved scripted gates;
- objects with special resources and no producer path;
- tech/AP/tradition gates needed for planetcraft, war moons, and systemcraft;
- likely traps or expensive low-payoff objects.

Acceptance:

- each packet is small enough to review;
- each row has source file evidence;
- decisions flow back into the policy matrix.

### Phase 10: Runtime Scenario Validation

Runtime validation is not default. It happens only when the user explicitly asks.

When requested, scenario validation should use controlled observer runs and compare against benchmark milestones:

| milestone | expected evidence |
| --- | --- |
| by 2250 | AI has route progress toward Mega Engineering and economy scaling |
| by 2300 | top AI is building or has built meaningful megastructure infrastructure |
| by 2350 | top AI has high-tier economy, shipyard throughput, and advanced hull/component usage |
| by 2400 | top AI can contest modded crises/Fallen Empire scale with planetcraft/war moons/systemcraft path progress |

No runtime result should be treated as proof unless it records:

- active mod list and load order;
- galaxy settings;
- difficulty/scaling settings;
- top AI tech/economy/fleet metrics;
- built megastructures and ship classes;
- route progress blockers.

## Immediate Next Work Items

These are the next concrete tasks. They should be done in order.

1. Create object atlas generator.
   - Input: vanilla install plus required Workshop folders.
   - Output: one atlas row per object.
   - Validation: row count by mod/type, parse errors listed.

2. Create dependency edge extractor.
   - Input: atlas objects and parsed PDX blocks.
   - Output: graph edges for requirements, upgrades, unlocks, flags, resources.
   - Validation: no edge references unknown nodes unless marked external/manual.

3. Create existing AI support extractor.
   - Input: object blocks and scripted AI helper files.
   - Output: support map with `parent_ai_complete`, `parent_ai_partial`, `parent_ai_absent`, etc.
   - Validation: high-impact objects all classified.

4. Build route queries for planetcraft, war moons, and systemcraft.
   - Input: graph.
   - Output: dependency path reports and missing policy gaps.
   - Validation: every required node resolves to source files.

5. Build first policy matrix for Gigas megastructure routes.
   - Scope: economy megastructures, planetcraft, war moons, systemcraft, and their prerequisites.
   - Output: policy rows only, not generated gameplay changes yet.
   - Validation: all policy object IDs exist in atlas.

6. Generate weights only after policy rows exist.
   - Scope: one route at a time.
   - Output: generated patch files plus conflict notes.
   - Validation: static object/reference tests only.

## First Atlas Priority Order

Because the full set may be around ten thousand objects, process in strategic order:

1. Gigas technologies, APs, megastructures, planetcraft, war moons, systemcraft, special resources.
2. NSC3 technologies, ship sizes, sections, shipyards, flagship/headquarters structures.
3. ESC technologies and component chains.
4. Starbase Extended modules/buildings and defensive economy.
5. Tall-scaling buildings, districts, jobs, habitats, and planet-capacity systems.
6. Remaining buildings/jobs/deposits/resources.
7. Flavor/low-impact objects.

## Required Review Standard

Every proposed AI rule must answer:

```text
What object is this?
Where is it defined?
What does it unlock or enable?
What unlocks it?
What does it cost?
What does it consume?
What does it produce?
Does parent AI already handle it?
If parent AI handles it, what state must the Director create so parent AI uses it?
If parent AI does not handle it, what direct weight or decision rule is required?
When should the AI rush it?
When should the AI avoid or delay it?
What validation proves the generated references are valid?
```

If those questions cannot be answered, the object stays in `manual_review` and does not get guessed weights.

## Success Criteria

The project is not meaningfully complete until:

- the atlas covers all AI-relevant objects in the target playset;
- the dependency graph can explain the route to planetcraft, war moons, and systemcraft;
- every high-impact object has parent AI support classified;
- every high-impact support gap has a policy row;
- generated AI files come from the policy matrix;
- static validation proves all generated references are valid;
- optional user-requested observer runs show AI empires actually progressing through high-scale routes.

## Current Truth

The Director is not yet this system. The current state is an early generator with partial ROI data and a broad replacement economy. The next correct move is to build the atlas and graph. More economic tuning before that is likely to create noise rather than intelligence.
