# Stellar AI Director Opening Research, Policy, and Fleet Specialization Implementation Plan

Date: 2026-07-07
Target game version: Stellaris PC 4.4.5 live by default, with a 4.4.4 inventory/compatibility mode for pinned installations
Target mod: `mods/StellarAIDirector`

Planning addendum: `research/stellar-ai/stellar-ai-director-webchatgpt-computed-kernel-addendum-2026-07-07.md`

## Scope Lock

This is an implementation plan for changing AI behavior through script weights, generated mod artifacts, and static validation only.

Out of scope for this plan:

- running observer games;
- running benchmark scenarios;
- collecting checkpoint screenshots or save snapshots;
- measuring runtime empire outcomes;
- launching Stellaris as part of validation;
- proving that a generated AI beats a crisis in a simulated run.

The user will do scenario and runtime testing manually. The only tests in this plan are code and artifact validity checks: generator execution, static validation, parser/load-safety checks where available, unit tests for deterministic helper behavior, and Git whitespace/diff hygiene.

The implementation model is computed strategic state, not an imagined mutable AI brain. The generator should emit scripted triggers, scripted values where verified, `ai_weight` gates, economic-plan weights, and local inventory validation. Persistent flags, variables, or events are reserved for hysteresis, cooldowns, planet role locks, doctrine lock-in, and megastructure attempt memory after the relevant on-action/state surfaces are verified.

## Objective

Revise Stellar AI Director so AI empires build a stronger first-75-year foundation for late-game 25x crisis relevance. The next implementation pass should make AI openings less generic by explicitly weighting:

- early research snowballing;
- early growth and pop throughput;
- early policy and edict choices;
- research pacts and Research Federation preference;
- coherent fleet doctrine lanes tied to technology choices;
- military investment only when it buys territory, pops, economy, subject leverage, or survival.

The immediate goal is not to make a final perfect AI. The goal is to produce the next testable weight set: a concrete, internally coherent version that the user can run manually.

## Current Diagnosis

The current generated AI has some useful late-game and fleet pressure, but it is still underpowered for the user's target. A year-2350 empire with roughly 800 monthly research is not a partial success for this objective; it is a failed economic trajectory. For the intended modded setup, the AI should be aiming for roughly 1,000 monthly research by the 2270-2280 window and 5,000-6,000 or more by 2350, with enough economy behind it to keep scaling.

The main defects to address in the next weight pass are:

- early research weight is too broad and not aggressive enough;
- early growth policies and edicts are not being controlled as a first-class opening system;
- unity, consumer goods, minerals, and energy are not being treated as support systems for research acceleration;
- diplomacy does not sufficiently favor research pacts and Research Federation formation;
- fleet investment is not clearly connected to a strategic return;
- military technology is not lane-specialized, so an empire can waste research across armor, shields, lasers, kinetics, missiles, and strike craft without enough doctrine coherence;
- the AI lacks a first-75-year "opening book" that maps empire type to growth, research, diplomacy, and military posture.

## Source Surfaces To Edit

Primary generator:

- `tools/stellar_ai_director_lib.py`
- `tools/generate_stellar_ai_director_patch.py`
- `tools/validate_stellar_ai_director_patch.py`

Primary generated mod surfaces:

- `mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt`
- `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- `mods/StellarAIDirector/common/technology/zzzz_staid_01_unlock_technology_technology.txt`
- `mods/StellarAIDirector/common/buildings/zzzz_staid_06_research_infrastructure_buildings.txt`
- `mods/StellarAIDirector/common/districts/zzzz_staid_06_research_infrastructure_districts.txt`
- `mods/StellarAIDirector/common/traditions/zzzz_staid_02_perks_traditions_traditions.txt`
- `mods/StellarAIDirector/common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt`

New generated mod surfaces expected from this plan:

- `mods/StellarAIDirector/common/policies/zzzz_staid_10_opening_growth_policies.txt`
- `mods/StellarAIDirector/common/edicts/zzzz_staid_10_opening_growth_edicts.txt`
- `mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_10_opening_strategy_triggers.txt`
- `mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_11_fleet_doctrine_triggers.txt`

Possible later surfaces, only after direct vanilla/mod-surface verification:

- `mods/StellarAIDirector/common/personalities/zzzz_staid_12_personality_overrides.txt`
- `mods/StellarAIDirector/common/federation_types/zzzz_staid_13_research_federation_weights.txt`
- `mods/StellarAIDirector/common/diplomatic_actions/zzzz_staid_13_research_pact_weights.txt`

Personality, federation, and diplomatic action overrides are higher compatibility risk than additive generated triggers and economic plan weights. They should be implemented only after confirming object names, override behavior, and conflict risk against vanilla and the active mod set.

## Implementation Contract

All changes should be owned by the generator, not hand-edited into generated files. The generator should produce deterministic artifacts with clear comments and stable route names.

The implementation should:

- use verified vanilla IDs before generating policy, edict, federation, diplomatic, personality, building, district, or technology overrides;
- avoid invented triggers, effects, or policy option names;
- prefer `ai_weight` changes on existing options and objects when that is sufficient;
- avoid event-driven policy setting unless direct `ai_weight` control cannot express the desired behavior;
- avoid hidden bonuses or player-specific behavior;
- keep military investment subordinate to strategic return unless an empire is explicitly on an aggressive route;
- preserve forced-filler behavior for technology choices when the desired lane tech is not offered;
- document every generated pass in the mod notes.

## Opening Strategy Classifier

Add a first-75-year classifier that maps each AI empire into one dominant opening route. This classifier should be represented as generated scripted triggers and reused by economic plans, policy weights, edict weights, technology weights, diplomacy weights, and fleet doctrine selection.

Recommended route triggers:

- `staid_opening_direct_research`
- `staid_opening_unity_to_research`
- `staid_opening_military_to_pops`
- `staid_opening_defensive_tall_research`
- `staid_opening_trade_to_research`
- `staid_opening_hive_growth_research`
- `staid_opening_machine_growth_research`

### Direct Research Route

Purpose: push labs, researchers, research stations, research edicts, research pacts, and Mega Engineering prerequisites as early as possible.

Likely inputs:

- materialist, technocracy-like, machine intelligence, synthetic-leaning, or research civic/personality signals;
- no severe monthly energy, mineral, food, or consumer goods deficit;
- not in an existential defensive war;
- enough pop base to support researcher jobs;
- year less than 75 for opening-specific weights, then transition into midgame megastructure route.

Expected behavior:

- prefer research-supporting policies;
- turn on research subsidies when affordable;
- prefer labs and researcher-enabling buildings;
- favor research pact diplomacy;
- strongly prefer Research Federation over other federation types when federation formation is available;
- keep fleet at defensive minimum unless threat or opportunity route is active.

### Unity To Research Route

Purpose: use unity and tradition acceleration to unlock research scaling, ascension strength, and empire-wide economic modifiers faster.

Likely inputs:

- spiritualist, unity civic, ascension-heavy, virtual, modularity, synthetic, psionic, or tradition-synergy signals;
- stable basic economy;
- not boxed into a mandatory conquest route.

Expected behavior:

- use unity edicts and campaigns when affordable;
- avoid converting the entire economy into unity at the expense of research;
- weight traditions and ascension perks that accelerate research, pop growth, production, or megastructure access;
- transition into direct research or megastructure route once core unity unlocks are reached.

### Military To Pops Route

Purpose: fleet spending is justified only if it can buy territory, subjects, pops, chokepoints, vassal income, or survival.

Likely inputs:

- militarist, authoritarian, purifier-like, conqueror, hegemon, subjugator, or aggressive personality signals;
- nearby weaker neighbors or boxed-in growth ceiling;
- sufficient alloy and naval capacity runway;
- clear war-philosophy compatibility.

Expected behavior:

- increase alloy and naval weights early;
- pick a coherent fleet doctrine lane;
- use policies that support war readiness;
- lower acceptance thresholds for favorable wars only when the AI can plausibly win or gain;
- avoid fleet overbuilding if no expansion, conquest, subject, or defensive purpose exists.

### Defensive Tall Research Route

Purpose: when conquest is bad or unsafe, build chokepoints, starbases, internal growth, research habitats, and megastructure prerequisites.

Likely inputs:

- boxed in;
- weaker than neighbor;
- pacifist or defensive personality;
- strong tall modifiers;
- habitat, megastructure, or station-defense synergy.

Expected behavior:

- invest in fortification only at real chokepoints and threatened borders;
- avoid wasteful fleet escalation beyond defense;
- push research, starbase economy, and defensive technology;
- favor diplomacy, research pacts, and Research Federation.

### Trade To Research Route

Purpose: use trade, commercial value, consumer goods conversion, and diplomacy to support research growth.

Likely inputs:

- megacorp, trade civic, commercial pact weighting, high trade value, or trade federation pressure;
- enough protection against piracy and early aggression;
- strong consumer goods or unity conversion options.

Expected behavior:

- avoid clerk spam unless trade value is actually productive;
- use trade policy to support consumer goods or unity needs;
- invest in research once consumer goods are stable;
- prefer research pacts even when commercial diplomacy is also weighted.

### Hive And Machine Growth Research Routes

Purpose: account for non-standard economies that cannot use the same consumer goods, trade, or policy assumptions as normal empires.

Hive expected behavior:

- prioritize pop growth, spawning pools, food/mineral stability, and research drones;
- use hive-compatible nutritional or growth edicts;
- avoid irrelevant consumer goods and trade assumptions.

Machine expected behavior:

- prioritize assembly, energy, minerals/alloys, research drones, and maintenance stability;
- weight robotics/machine production technologies;
- avoid organic-only edict or policy assumptions.

## Opening Economic Plan Changes

Add explicit first-75-year economic plan targets and subplans inside the generator. These should not be runtime benchmarks; they are weight targets for what the AI should try to build toward.

Recommended generated subplans:

- `Stellar AI Director competitive opening mineral tempo`
- `Stellar AI Director competitive opening consumer goods bridge`
- `Stellar AI Director competitive opening research capital`
- `Stellar AI Director competitive opening colony specialization`
- `Stellar AI Director competitive opening pop assembly`
- `Stellar AI Director competitive opening defensive tall research`
- `Stellar AI Director competitive opening military-to-pops`
- `Stellar AI Director competitive opening research recovery`

### Years 0-25 Weight Intent

Primary purpose: create the resource and pop foundation that lets the AI add researchers without collapsing.

Weight priorities:

- minerals for construction tempo;
- energy safety;
- food safety for organic empires;
- consumer goods bridge for normal research empires;
- pop assembly and growth infrastructure;
- exploration and survey acceleration where legal;
- first labs only when the economy can support researcher jobs;
- avoid early prestige fleet spending unless military-to-pops or survival route is active.

Suggested target pressure:

- minerals: high priority until construction bottleneck is relieved;
- energy: high priority when monthly balance is unsafe;
- consumer goods: high priority for normal empires before adding more labs;
- research: moderate-to-high, gated by CG/energy stability;
- alloys: defensive baseline, higher only for military-to-pops or active threat;
- unity: enough to unlock key early traditions, not enough to starve research.

### Years 25-50 Weight Intent

Primary purpose: convert a stable economy into a research engine.

Weight priorities:

- labs and research jobs;
- building slots and capital upgrades that unlock more research jobs;
- research station value;
- research edicts where affordable;
- education or leader-development campaigns where legal;
- consumer goods production to support researchers;
- traditions and perks that improve research, economy, pops, or megastructure access;
- military only to defend, conquer with purpose, or maintain diplomatic leverage.

Suggested target pressure:

- research should become the dominant non-survival weight;
- engineering should receive extra pressure because Mega Engineering, starbases, habitats, ships, armor, and industrial scaling compete there;
- society should be used for pop growth, administrative, biological, and unity-relevant support;
- physics should support research speed, energy, shields, sensors, and computing.

### Years 50-75 Weight Intent

Primary purpose: move from opening economy into midgame snowball.

Weight priorities:

- research institutes and higher-tier labs where legal;
- orbital/habitat/research district scaling if the empire has the tech and economy;
- Mega Engineering prerequisites;
- Gigastructural and NSC3 prerequisite routes where active;
- subject, federation, or research pact acceleration;
- doctrine-specialized military tech only if the fleet has a strategic role.

Suggested target pressure:

- direct research and unity-to-research routes should aggressively prioritize research throughput;
- defensive tall route should prioritize research, chokepoint survival, and internal scaling;
- military-to-pops route should push fleet only while it is converting into external gains.

## Building, District, And Job Weight Changes

The plan should add or strengthen generated weights for early research infrastructure and the support economy that keeps it fed.

High-priority research and support targets:

- research labs and upgraded labs;
- research institute or equivalent empire research amplifier;
- research district and habitat research options where legal;
- archaeology, astral, or special research buildings when available and relevant;
- pop assembly and growth buildings;
- consumer goods production buildings for normal empires;
- mineral and energy stabilization buildings;
- unity buildings only where they accelerate the chosen research route;
- starbase economy modules that reduce early planet pressure, after verifying IDs.

Implementation notes:

- Do not assume a job-weighting surface exists until verified in vanilla or generated docs.
- If direct job weights are not available, express behavior through building, district, economic plan, and resource weights.
- Do not claim clerk suppression, researcher prioritization, or soldier suppression unless the implementation touches a verified script surface that actually controls those outcomes.
- Add comments in generator data structures explaining which opening route owns each weight.

## Policy Weight Changes

Create a generated policy override pass only after verifying exact vanilla policy and option IDs. Prefer option-level `ai_weight` blocks. Use event-driven `set_policy` only as a fallback if static policy weights cannot control the behavior cleanly.

Expected new generator function:

- `opening_growth_policy_artifact_passes()`

Expected generated file:

- `common/policies/zzzz_staid_10_opening_growth_policies.txt`

### Policy Weight Map

Economic policy:

- Direct research: prefer civilian or research-supportive economic posture when consumer goods are the research bottleneck.
- Unity to research: prefer the policy that best supports early unity without starving labs.
- Military to pops: prefer military/alloy posture only when conquest or survival route is active.
- Defensive tall research: prefer balanced or civilian support unless threat level requires alloys.

Trade policy:

- Trade-to-research: prefer consumer-goods or unity conversion if it supports labs and traditions.
- Direct research: prefer consumer-goods support when CG bottleneck blocks labs.
- Non-trade empires: avoid over-weighting trade policy if trade value is low or irrelevant.

Diplomatic stance:

- Direct research and defensive tall: prefer cooperative, scientific, or diplomacy-positive stances that support research pacts.
- Military to pops: prefer supremacy or aggressive stance only when conquest route is active.
- Genocidal or incompatible authorities: do not force diplomacy-positive options that cannot work.

War philosophy:

- Military to pops: weight unrestricted or liberation/subjugation-compatible war policy when legal and useful.
- Direct research, unity-to-research, defensive tall: avoid war policies that encourage wasteful wars.

Robotic workers and artificial intelligence policy:

- Research/growth routes: allow robots and AI where legal and not ethics-blocked, because pop growth and specialist capacity support research.
- Spiritualist or AI-restricted empires: do not create illegal or roleplay-breaking forced choices.

Migration and refugee policy:

- Research/growth routes: prefer policies that increase pop acquisition when empire ethics and stability allow it.
- Xenophobe or security-sensitive empires: respect compatibility and avoid blindly forcing openness.

Living standards and species-rights surfaces:

- Only include if verified safe to override and compatible with empire ethics.
- Weight living standards that improve specialist output, stability, or research where the economy can afford them.
- Avoid broad rights overrides in the first pass unless the surface is well understood.

### Policy Weight Formula Pattern

Use high but bounded static weights with gates:

- add strong positive weight for the matching opening route;
- add negative or low weight for off-route policies;
- require basic resource safety before choosing policies that increase upkeep;
- add threat gates before military policy escalation;
- add legality and authority gates before diplomacy, AI, robot, migration, or living-standard changes.

Example intent, not final syntax:

- matching opening route: `+5000` to `+10000`;
- active deficit safety veto: `0` or severe reduction;
- active existential threat: military/defensive policy boost;
- off-route military escalation: strong reduction unless conquest route is active.

## Edict Weight Changes

Create a generated edict weighting pass after verifying exact edict IDs, resources, costs, and legal conditions.

Expected new generator function:

- `opening_growth_edict_artifact_passes()`

Expected generated file:

- `common/edicts/zzzz_staid_10_opening_growth_edicts.txt`

### Edict Weight Map

`map_the_stars`:

- high weight in the first exploration phase;
- strongest for direct research, trade-to-research, and defensive tall openings;
- reduce after expansion value falls or resource pressure is too high.

`research_subsidies`:

- highest priority for direct research and unity-to-research once energy and unity upkeep are safe;
- lower or disabled during severe energy deficit;
- should remain a core research-snowball lever.

`capacity_subsidies`:

- high weight when energy is the bottleneck blocking labs, edicts, or fleet upkeep;
- lower when energy is already safe.

`mining_subsidies`:

- high weight in mineral-tempo opening;
- high weight when construction or alloy/research support is mineral-bound;
- lower when mineral stockpile and income are safe.

`farming_subsidies`:

- use only for organic empires when food is a real growth or upkeep constraint;
- avoid over-weighting if food is already safe.

`nutritional_plenitude` and hive-compatible growth edicts:

- high weight for biological and hive growth routes when food economy can support it;
- lower during food deficit.

`education_campaign`:

- weight for research routes when leader/scientist bonuses and unity cost are affordable.

`healthcare_campaign`:

- weight for organic growth routes when consumer goods and energy can support it.

`recycling_campaign`:

- weight when consumer goods or minerals are constraining lab expansion.

`fortify_the_border`:

- high weight only for defensive tall, chokepoint, active-threat, or border-survival states;
- low weight for direct research route with no relevant threat;
- avoid spending unity on defense theater when it does not buy survival.

## Technology Weight Changes

Add a more explicit first-75-year research map. The goal is not to pick one universal tech path. The goal is to pick a lane, stay in it, and avoid wasting research on off-lane military tech unless forced.

Expected new data structures:

- `OPENING_RESEARCH_TECH_TARGETS`
- `OPENING_GROWTH_TECH_TARGETS`
- `OPENING_ECONOMY_TECH_TARGETS`
- `FLEET_DOCTRINE_TECH_TARGETS`
- `FLEET_DOCTRINE_AVOIDANCE_HINTS`

### Research And Economy Tech Priority

High-priority categories:

- research speed and researcher output;
- research alternatives;
- lab upgrades and research building unlocks;
- engineering prerequisites for starbases, habitats, megastructures, and Mega Engineering;
- pop growth and pop assembly;
- energy and mineral production multipliers;
- consumer goods and industrial efficiency;
- unity or tradition acceleration where it directly supports the selected route;
- exploration and anomaly payoff where early enough to matter.

Engineering needs special handling because it carries too many critical lanes:

- Mega Engineering prerequisites;
- ship hulls and starbases;
- armor and materials;
- robots and assembly;
- industry and minerals;
- Gigastructural/NSC3 paths.

The implementation should prevent military engineering tech from crowding out Mega Engineering and economy prerequisites unless the empire is in the military-to-pops or survival route.

### Forced Filler Rule

When desired route tech is not available, the AI should pick useful filler in the same area instead of boosting random off-lane tech.

Preferred filler:

- cheapest tier-progressing tech that unlocks more rolls;
- economy or research support tech;
- prerequisites for known future target tech;
- survival tech only when threatened.

Avoid:

- splitting between armor and shields without doctrine reason;
- taking every weapon family just because it appears;
- over-investing in fleet upgrades for pacifist or diplomacy-first research routes;
- delaying Mega Engineering prerequisites for low-impact military sidegrades.

## Fleet Doctrine System

Add a unified fleet doctrine classifier that maps AI personalities and strategic route to coherent technology priorities. This does not mean every empire gets more fleet. It means every empire that invests in fleet should invest coherently.

Expected new generator function:

- `fleet_doctrine_artifact_passes()`

Expected generated file:

- `common/scripted_triggers/zzzz_staid_11_fleet_doctrine_triggers.txt`

Recommended doctrine triggers:

- `staid_doctrine_energy_shield`
- `staid_doctrine_kinetic_armor`
- `staid_doctrine_missile_evasion`
- `staid_doctrine_carrier_strikecraft`
- `staid_doctrine_balanced_filler`

### Energy And Shield Doctrine

Inputs:

- personality prefers energy weapons;
- empire has shield, physics, or energy synergies;
- direct research route has enough physics throughput;
- no strong reason to hard-counter a known threat differently.

Prioritize:

- lasers and other energy weapons;
- shields;
- reactors and power;
- sensors, combat computers, tracking, and accuracy;
- physics research speed.

De-prioritize:

- armor as a main lane unless forced by available choices or threat;
- kinetic and explosive weapon lines except for minimum viable filler.

### Kinetic And Armor Doctrine

Inputs:

- personality prefers kinetic weapons;
- empire has armor, materials, alloy, or engineering synergies;
- militarist or defensive tall empire with engineering depth.

Prioritize:

- kinetic weapons;
- armor and hull durability;
- alloy production and ship build efficiency;
- engineering research speed;
- starbase and defensive platforms when defensive tall is active.

De-prioritize:

- lasers and shields as mainline picks unless forced;
- missile and strike craft sidegrades unless the doctrine changes.

### Missile And Evasion Doctrine

Inputs:

- personality prefers explosive weapons;
- early aggression or skirmish route;
- corvette/frigate timing matters;
- empire needs low-cost military pressure.

Prioritize:

- missiles, torpedoes, and explosive weapons;
- afterburners, speed, disengagement, and evasion support;
- relevant hull unlocks;
- alloy and naval capacity only when fleet is being used for gains.

De-prioritize:

- slow battleship-style side paths too early;
- armor-heavy or shield-heavy detours unless survival requires them.

### Carrier And Strike Craft Doctrine

Inputs:

- personality prefers strike craft;
- empire has hangar, carrier, starbase defense, or NSC3 capital-hull synergy;
- defensive tall or midgame fleet scaling route.

Prioritize:

- strike craft and hangar technologies;
- carrier-capable hulls;
- point defense and flak support;
- reactors and command systems;
- starbase hangars for defensive tall.

De-prioritize:

- unrelated weapon families unless no useful carrier-support option appears.

### Balanced Filler Doctrine

Purpose: prevent incoherent over-specialization when the empire has no strong doctrine signal.

Behavior:

- pick one temporary lane based on the first useful weapon or defense family offered;
- avoid equal boosts to every family;
- prefer economy, research, and hull prerequisites over random military sidegrades;
- reclassify into a stronger doctrine once personality, technology, or route evidence appears.

## Fleet Investment Theory

Fleet is not an independent success metric. Fleet spending is useful only when it buys something.

The implementation should use three fleet modes:

- defensive minimum;
- strategic aggression;
- survival emergency.

### Defensive Minimum

Default for direct research, unity-to-research, trade-to-research, and many defensive tall empires.

Behavior:

- maintain enough fleet and starbase defense to avoid easy conquest;
- avoid excessive alloy sink;
- keep technology picks focused on economy and research unless threatened;
- use diplomacy, research pacts, and federations to reduce security burden.

### Strategic Aggression

Used by military-to-pops route and aggressive personalities when conquest or subjugation has a plausible return.

Behavior:

- alloy and naval weights rise sharply;
- war policy and diplomatic stance shift aggressive when legal;
- doctrine-specific weapon and defense techs get higher weights;
- expansion, claims, subjects, and captured pops justify the fleet investment.

### Survival Emergency

Used when the empire is threatened, boxed in, or vulnerable.

Behavior:

- immediate defensive tech and alloy weights rise;
- fortification edicts and starbase defense receive priority;
- research route temporarily shifts toward survival tech;
- once threat falls, return to research or growth route.

## Research Pact And Federation Changes

The AI should be much more willing to use diplomacy as a research multiplier.

Research pact goals:

- increase acceptance or proposal weights for friendly, non-hostile, non-genocidal empires;
- favor research pacts especially for direct research, unity-to-research, defensive tall, trade-to-research, and machine research routes;
- avoid wasting diplomatic effort on incompatible enemies.

Federation goals:

- strongly prefer Research Federation when the empire's purpose is research snowballing;
- avoid forming lower-value federations when Research Federation is legal and plausible;
- allow military or hegemony federation pressure only for empires whose strategy actually benefits from it;
- preserve legal, DLC, ethic, and tradition requirements.

Implementation sequence:

1. Verify exact vanilla federation and diplomatic-action files.
2. Identify whether federation type choice and research pact acceptance are controlled by object `ai_weight`, personality fields, diplomatic actions, or other script.
3. Add generated overrides only where the control surface is verified.
4. Add static validation to ensure every referenced federation type, diplomatic action, policy, edict, and trigger exists.

## Generator Implementation Steps

1. Add verified ID inventories for relevant policies, policy options, edicts, diplomacy actions, federation types, military technology groups, research buildings, and growth buildings.
2. Add opening route trigger generation.
3. Add opening economic plan subplans and route-specific resource priorities.
4. Add policy weighting artifact generation.
5. Add edict weighting artifact generation.
6. Add early research and economy technology target maps.
7. Add fleet doctrine classifier and doctrine-specific tech target maps.
8. Add research pact and Research Federation weighting only after source-surface verification.
9. Regenerate the mod artifacts.
10. Update mod notes with the new route model, generated files, and validation status.

## Static Validation Plan

These are the only tests that belong to this implementation plan.

Run after code changes:

```powershell
python -m py_compile tools\stellar_ai_director_lib.py tools\generate_stellar_ai_director_patch.py tools\validate_stellar_ai_director_patch.py
```

Run generator:

```powershell
python tools\generate_stellar_ai_director_patch.py
```

Run static mod validation:

```powershell
python tools\validate_stellar_ai_director_patch.py
```

Run deterministic Python tests that cover generator and validation behavior:

```powershell
python -m unittest discover -s tools\tests
```

Run Git whitespace check:

```powershell
git diff --check
```

If CWTools or an equivalent parser is already configured locally for this repo, run it only as a static syntax/schema check. Do not turn parser validation into a runtime game test.

Do not run:

- observer simulations;
- manual scenario benchmarks;
- save-game checkpoint collection;
- crisis outcome tests;
- automated game launches.

## Acceptance Criteria

This implementation pass is acceptable when:

- generator changes produce deterministic artifacts;
- generated policy, edict, opening-route, and fleet-doctrine files exist where planned;
- every referenced policy, edict, technology, federation type, diplomatic action, building, district, trigger, and scripted value is verified against vanilla, parent mods, or generated inventories;
- direct research, unity-to-research, military-to-pops, defensive tall, trade-to-research, hive, and machine openings have distinct weight behavior;
- early policy and edict choices are explicitly weighted for growth and research acceleration;
- Research Federation and research pact preference are weighted where verified script surfaces allow it;
- fleet technology weights are doctrine-specialized instead of boosting all weapon and defense families equally;
- fleet spending is tied to defensive minimum, strategic aggression, or survival emergency;
- static validation commands pass;
- the notes explain what changed and what manual runtime questions remain for the user to test.

## Manual Runtime Questions For The User

These are not Codex validation steps for this plan. They are the questions the user can answer later during manual testing:

- Does the AI hit roughly 1,000 monthly research by the 2270-2280 window?
- Does the AI approach 5,000-6,000 or more monthly research by 2350 in successful runs?
- Do research empires choose research pacts and Research Federations more reliably?
- Do military empires use fleet to gain territory, subjects, pops, or defensive survival rather than merely stockpiling fleet power?
- Do doctrine-specialized empires avoid wasting research across unrelated weapon and defense lanes?
- Do policy and edict choices visibly improve the opening economy?

## Risks And Mitigations

Risk: policy and edict overrides may conflict with other mods.

Mitigation: verify exact object IDs, keep generated files clearly named, and document overwritten vanilla objects.

Risk: route specialization may overfit and starve a missing prerequisite.

Mitigation: keep forced-filler logic for cheap tier progress, economy support, and known prerequisites.

Risk: military-to-pops route may overbuild fleet without conquest payoff.

Mitigation: gate high fleet spending behind aggressive personality, strategic opportunity, active threat, or boxed-in state.

Risk: research routes may underbuild alloys and die.

Mitigation: keep defensive minimum and survival emergency paths separate from strategic aggression.

Risk: diplomacy changes may cause wrong federation type selection or low-value diplomacy spam.

Mitigation: weight Research Federation and research pacts strongly only for compatible, friendly, research-oriented empires.

Risk: unsupported assumptions about jobs, policies, or diplomacy controls.

Mitigation: do not generate a claim-bearing change until the specific vanilla or mod control surface has been verified.

## First Implementation Slice

The first coding slice should be:

1. Verified ID inventory for policies, edicts, and key opening tech/building targets.
2. Opening route scripted triggers.
3. Opening economic plan subplans.
4. Policy and edict AI weights for research/growth openings.
5. Static validation updates.

The second coding slice should be:

1. Fleet doctrine triggers.
2. Doctrine-specific technology target maps.
3. Military-to-pops and defensive minimum fleet weight refinements.
4. Research pact and Research Federation weighting after source-surface verification.

The first slice should be preferred because early policy, edict, growth, and research acceleration are the highest-priority defects for the user's target.
