# Stellar AI Director V2 AI Behavior Design

Generated: 2026-07-08
Packet: Stellar AI Director Strategic V2 Roadmap Packet
Target: Stellaris PC 4.4.5 stable/current, backwards compatible with 4.4.4 where source-backed


## Design Principle

The AI is not being made smarter by wishful roleplay. It is being given evidence-backed **computed strategic state** and safe, generated levers. Persistent state is reserved for proven hysteresis, cooldowns, doctrine locks, planet-role locks, or megastructure attempt memory.

## What Better AI Means

| Domain | Observable better behavior | Not acceptable as proof |
| --- | --- | --- |
| Economy | Useful construction, stable support resources, fewer capped stockpiles, fewer unstaffed priority jobs, no avoidable deficit spirals. | More weights without checking job staffing or support resources. |
| Research | Early labs/research districts when safe, research policies/edicts, Discovery/Diplomacy/AP routes, Mega Engineering/Mega Shipyard/Gigas/NSC/ESC tech progression. | Late-game megastructure weights alone. |
| Growth | Pop assembly/growth buildings where valid, high-pop research worlds, no invalid empire-type assembly paths. | Universal assembly spam. |
| Fleet | Fleet built for survival, crisis, conquest, raiding, subject formation, or secured economy. | Fleet power number rising while economy/research stagnate. |
| War | Militarists pursue payoff; non-militarists maintain defensive sufficiency; threat response remains bounded. | Forced wars, punitive CB spam, or diplomatic-action overrides without proof. |
| Defense | Starbase/static-defense investment tied to threat/economy/crisis posture. | Overbuilding defenses everywhere. |
| Megastructures | Prerequisites, APs, techs, special resources, reserves, and queue continuation are aligned. | Alloy hoarding without build/upgrade progress. |
| Compatibility | Major mods are first-class route inputs and conflict surfaces. | Assuming parent AI supports high-scale routes because an `ai_weight` exists. |

## Strategic Behavior Model

### Opening Route Classifier

Existing/planned Director strategy should continue to use route families such as:

- direct research opening;
- unity-to-research opening;
- military-to-pops opening;
- defensive tall research opening;
- trade-to-research opening;
- hive growth research opening;
- machine growth research opening.

Codex should refine these through verified scripted triggers and safe weights. The route classifier should influence economic plans, policies, edicts, technologies, traditions, APs, buildings, districts, fleet doctrine, and diplomacy. It should not pretend to be a mutable external AI brain.

### Economy

Desired behavior:

1. Early minerals and energy support construction and labs.
2. CG is kept sufficient for research jobs.
3. Food/minerals support growth/assembly as empire type requires.
4. Trade capacity is treated as logistics/capacity, not generic sellable income.
5. Special resources remain distinct bottlenecks for Gigas/ESC/NSC and rare-resource buildings.
6. Stockpile cap waste is converted into useful spending only when safety gates pass.
7. Deficit, survival, and recovery modes always override ambition.

Moddable levers:

- economic plans;
- AI budgets;
- building/district `ai_weight` / `ai_weight_coefficient` / verified `ai_resource_production` surfaces;
- policy/edict weights;
- scripted triggers and values;
- market/fleet safety events where already verified.

Aspirational/unproven:

- Direct job assignment rewrites unless a valid job/automation surface is proven.
- Broad colony automation overrides.
- Hidden economy bonuses.

### Research

Desired behavior:

- Research should be a first-75-year priority, not a midgame afterthought.
- AI should get enough support economy to staff research jobs.
- AI should seek Mega Engineering and downstream Gigas/NSC/ESC unlocks through prerequisite-aware technology weights.
- Research labs, institutes, supercomputers, archaeostudies, science habitats/districts, and modded research buildings should be weighted when safe.
- Research diplomacy should be attractive to friendly/non-genocidal research/economy-oriented empires.

Moddable levers:

- technology weights;
- building/district weights;
- policies/edicts;
- traditions/APs;
- research federation weight;
- economic-plan support-resource gates.

Aspirational/unproven:

- Direct research agreement formation through diplomatic actions/personality rewrites, pending evidence.
- Runtime milestones until observer runs are approved.

### Unity And Diplomacy

Desired behavior:

- Unity should turn into traditions/APs that improve research, economy, and modded progression tempo.
- Research Cooperative should be preferred by research/economy AI where ethics/civics make it plausible.
- Friendly/non-genocidal AI should satisfy research agreement prerequisites where safe, but direct action forcing remains gated.

Safe levers:

- federation type weights;
- tradition/AP weights;
- diplomacy-policy weights if verified;
- opinion or stance support only if additive and source-backed.

Gated levers:

- personalities;
- diplomatic actions;
- envoy behavior;
- event-driven proposal forcing.

### Fleets And War

Desired behavior:

- Fleet investment must have a purpose: survival, defended economy, conquest payoff, raiding pops, subject creation, hostile-fauna clearance, crisis readiness, or shipyard throughput payoff.
- Militarist/conqueror AI should be more willing to use fleet when safe and profitable.
- Pacifist/economy AI should avoid needless fleet overbuild and keep research/economy investment high.
- Threat response should change opinion/readiness without forced wars.

Safe levers:

- fleet-throughput economic subplans;
- technology route weights for hulls/components;
- bombardment stance AI weights where source-backed;
- threat-response opinion/readiness flags;
- war support reserves.

Gated levers:

- war declaration thresholds;
- claims/CB automation;
- join-war behavior;
- personalities;
- diplomatic-action overrides.

### Defense And Crisis Response

Desired behavior:

- Starbases and static defenses should be built where they protect strategic systems, shipyards, chokepoints, megastructure sites, or crisis fronts.
- Defense should not consume the entire growth/research budget.
- Crisis readiness should integrate technology, shipyard, fleet-throughput, starbase, alloy/energy reserves, and special resources.

Safe levers:

- starbase modules/buildings weights;
- starbase tech weights;
- fleet-throughput economic plans;
- static-defense economic subplans;
- threat-response readiness flags.

Research questions:

- Exact crisis detection surfaces in current 4.4.5 and major mods.
- Starbase Extended winning object behavior and scope safety.
- Whether advanced Gigas crises expose safe AI preparation signals.

### Megastructures And Gigastructures

Desired behavior:

- AI should not just reserve alloys; it should progress through prerequisites, APs, techs, build sites, special resources, construction caps, and upgrade chains.
- Economy megastructures should arrive early enough to matter.
- Planetcraft/war moon/systemcraft paths should be route-aware, not random late picks.

Safe levers:

- technology/AP/tradition route weights;
- megastructure route copies already proven;
- AI budgets for alloys and Gigas special resources;
- economic plan reserves and construction pressure.

Gated levers:

- broad Gigas object rewrites;
- queue continuation claims;
- settings-sensitive feature forcing;
- runtime optimization claims.

### Colonies, Planets, And Planetary Diversity

Desired behavior:

- AI should exploit high-value PD worlds/buildings/districts when support resources are safe.
- Outposts and special planets should be recognized as economic opportunities.
- Broad colony designation rewrites should not fight vanilla or parent automation.

Safe levers:

- targeted PD building/district weights;
- scripted value/trigger classifications;
- decisions where already generated and source-backed;
- economic valuation datasets.

Gated levers:

- broad colony-type rewrites;
- blanket designation overrides;
- assumptions about all PD submods without current object evidence.

## Major Mod Compatibility Expectations

| Mod | Expected V2 posture | Safe current lane | Gated lane |
| --- | --- | --- | --- |
| Gigastructural Engineering & More (4.4) | Treat as core high-scale progression pillar. | Tech/AP/tradition/megastructure route weights, Gigas resource budgets, alloy reserves, route graph. | Queue continuation proof, broad object rewrites, crisis-specific logic. |
| NSC3 | Treat as core fleet/hull expansion pillar. | Technology weights, Mega Shipyard/fleet-throughput, support economy. | Direct ship designs, ship sizes, sections, section templates. |
| Extra Ship Components NEXT | Treat as high-tier component/resource pillar. | Tech/resource readiness, special-resource support, no direct component-template overrides. | ESC component-template `key = ...` handling, direct component templates. |
| Starbase Extended 3.0 | Treat as defense pillar after scope verification. | Starbase module/building weights already generated where valid. | Broader defense strategy until active-stack scope/conflict proof. |
| UI Overhaul Dynamic | Treat as UI compatibility dependency, not a Director implementation surface. | Load-order docs only. | UI files unless future explicit UI task. |
| Universal Resource Patch | Treat as resource display/compat infrastructure. | Load order after parent, before Director; preserve special resources. | Any assumption that it normalizes all resource semantics. |
| Planetary Diversity | Treat as economy/planet variety pillar. | Targeted PD value triggers, decisions, buildings. | Broad designation/colony rewrites. |
| AI/performance mods | Treat as overlap risks, not free wins. | Research active conflict/winner behavior. | Stacking AI rewrites without conflict proof. |

## Runtime Metrics To Add If Observer Is Approved

- Monthly research split and total.
- Empty researcher jobs.
- CG, energy, minerals, food, alloys, trade-capacity income/stockpile/runway.
- Pop growth and assembly indicators.
- Empire size, colonies, systems, habitats.
- Traditions/AP timing.
- Mega Engineering, Mega Shipyard, Gigas unlock status.
- Megastructure started/upgraded/completed counts.
- Fleet power, naval cap used/available, shipyard capacity.
- Wars declared, territory/pops/subjects gained, raiding outcomes.
- Starbase and defense-platform investment.
- Deficit/survival/recovery triggers.
- Research agreements, federation type, subjects/scholaria.

Observer metrics are evidence, not fast unit tests.
