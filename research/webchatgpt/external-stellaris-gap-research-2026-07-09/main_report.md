# Main Report: Filled External Findings For The High-Powered Stellaris 4.4.x Stack

## Executive answer

The stack should be treated as a separate high-powered balance environment rather than a vanilla-plus game. Gigastructural Engineering raises the endgame ceiling with dozens of megastructures, weaponized planets, stellar-scale structures, and optional crises intended to match those power spikes [S001]. NSC3 changes naval scale and ship-class behavior; its 4.4 update recommends a new save and materially changes fleet capacity/command limits [S025][S026]. ESC NEXT adds a component progression layer and requires a fresh game rather than conversion from old ESC 3.0 saves [S028]. The maintained 4.4 collection guidance says NSC3 + ESC NEXT users must adjust ESC reactor settings because ESC reactors are weaker than NSC3 reactors [S029]. Spacefleet Tactica is not optional decoration in that interaction; NSC3 removed its old Advanced Ship Behaviors due bugs and recommends SFT as the behavior replacement [S027].

The strategic answer is route discipline. Experienced-player advice splits into two viable lines: **early aggression/alloy conversion** or **hard tech rush into alloy/naval conversion**. The failure mode is a balanced-looking empire that is simultaneously under-teched, under-alloyed, and late to Mega Engineering. A normal lower-bound benchmark from community advice is around 500-800 science and 100 alloys by year 50 [S018], while an elite tech-rush benchmark is 2k+ science by 2240 and 3k+ by 2250 [S017]. For 25x crisis and Gigas crises, the latter should be the AI target curve, not the human-casual baseline.

The AI answer is explicit route support, not trust. Gigas publicly claims AI megastructure use through its feature scope [S001], and Stellar AI claims a research-first no-hidden-bonus posture [S033], but public player discussion still doubts whether AI can keep up with Gigas scaling [S038], and Gigas crisis discussions report AI ineffectiveness against Blokkats [S039]. Therefore, Stellar AI Director should keep explicit route overrides for research, Mega Engineering, Gigas special resources, megastructure construction throughput, NSC/ESC tech, shipyard/fleet throughput, and crisis-counter milestones.

## Direct answers to the ten research questions

### 1. High-powered gameplay strategy

**Answered finding.** Experienced players recommend either a hard tech rush or early conquest/alloy rush. Both paths are about focus, not balance. The tech-rush path uses early diplomacy/economy to fund labs, hits 2k+ science around 2240 and 3k+ by 2250 in a strong run [S017], then pivots to alloys and fleet when threats appear. The conquest path avoids normal expansion, forces early contact, converts influence/alloys into claims/vassals/pop acquisition, and scales through conquered population and industrial worlds [S016]. A non-cheese lower line is about 500-800 science and 100 alloys by year 50 [S018], but that is not enough for a heavily modded 25x/Gigas endgame unless the crisis date is late and the conversion phase is strong.

**Implementation decision.** The AI should choose a lane by 2210-2220: tech-federation/tall, alloy-conquest, or emergency survival. It should not slowly average between them. By 2240-2250, it should have a computed trigger that asks: “Do I have Mega Engineering progress and lab throughput?” If not, it must increase research pressure before building marginal fleets. By 2275-2300, it should ask: “Can I convert research into alloy/naval throughput?” If not, it must prioritize shipyards, starbase defenses, alloy districts/buildings, and Mega Shipyard/Gigas shipyard routes.

### 2. Gigastructural progression and crisis knowledge

**Answered finding.** The high-value progression path is: regular economy stabilization -> Mega Engineering/Gigas unlock pressure -> economy megastructures and special-resource routes -> construction-throughput resources -> celestial military structures -> crisis-specific counters. Gigas crisis counterplay is not “more vanilla battleships.” Katzenartig should be handled through resistance/contact/sabotage and only then open war [S006][S007][S008]. Blokkats require research/knowledge/scrap/destabilizer-style progression and systemcraft-scale force at the right windows [S004][S005][S012]. Aeternum expects planetcraft/systemcraft/attack-moon-scale power and a large alloy/shipyard economy [S009][S010][S011]. Compound-style threats are event/research-gated before they become conventionally vulnerable [S015].

**Mandatory systems.** Mega Engineering pressure, Gigas selection/UI setup, UIOD+Gigas patch, resource visibility via URP, EHOF/cohesive-resource acquisition if those resources are enabled, economy megas, construction throughput, and celestial ships when Gigas crises are enabled [S001][S013][S014][S048][S051].

**Trap systems.** Enabling high Gigas crises without committing to celestial ships; stacking megastructure build cap without alloy/special-resource throughput; fighting Katzen conventionally before resistance progress; allowing UI/resource patches to hide special resources; letting AI build low-ROI prestige structures while still below research/alloy/naval curve [S006][S014][S039][S052].

### 3. NSC3 + ESC NEXT + Spacefleet Tactica fleet design

**Answered finding.** NSC3 owns ship scale/classes; ESC NEXT owns advanced components; SFT owns combat behavior after NSC3 removed Advanced Ship Behaviors [S025][S027][S028]. The first compatibility decision is the ESC reactor setting: disable or de-prioritize ESC reactors before the first month when using NSC3 because the collection maintainer warns that ESC reactors are weaker than NSC3 reactors and clutter the research/design path [S029]. The second decision is to verify ship behavior/computer slots, because empty behavior slots can prevent saving NSC designs [S030].

**Fleet doctrine.** Use ship classes by role instead of mono-hull spam: screens/pickets to absorb and screen; carrier/missile artillery for kiting; artillery capitals for long-range decisive damage; dreadnought/titan/flagship-style hulls as anchors; crisis-specific retrofit branches for Unbidden/Scourge/Contingency/Cetana-style targets [S019][S020][S021]. Do not judge readiness solely by UI fleet power; crisis counterfit can outperform much higher listed enemy fleet power [S019].

### 4. AI use of high-powered mods

**Answered finding.** Public evidence supports AI hooks and AI-mod claims, not reliable full-stack mastery. Gigas feature scope includes AI megastructure use claims [S001]. Stellar AI claims a research-first strategy and no hidden AI-only bonuses [S033]. StarNet claims economy/research/military/fleet-use improvements [S035]. Yagisan’s Better Stellaris claims mod-added job handling [S040]. But player discussion still doubts AI performance in Gigas [S038], and Blokkat discussion reports AI ineffectiveness [S039]. Starnet for NSC3 is stale for 4.4 because its page says it is for 3.12 [S036].

**Implementation decision.** Use parent AI support as evidence, not proof. The Director should classify parent support as complete/partial/absent/wrong-goal and then override only route-critical missing pieces: Mega Engineering, Gigas perk/tech gates, special resources, economy megas, celestial ships, NSC/ESC tech paths, shipyard throughput, starbase defense, and crisis counters.

### 5. Console commands and test cheat sheets

**Answered finding.** The public command reference is the Paradox Wiki console-command page, plus in-game `help` for exact current syntax [S060]. Third-party command databases are useful for discovery but should not outrank Paradox Wiki or in-game `help` [S063]. Deposits and planet features can be tested with selected-scope `effect` commands [S061]. `debugtooltip` is the core ID-discovery command for leaders/objects [S062]. `create_megastructure` tests can fail when the wrong object/scope/player context is selected, so megastructure-spawn tests must include selected star/system context and `help create_megastructure` verification [S064].

**Implementation decision.** The cheat sheet in this packet gives templates for tech, resources, planets, deposits, modifiers, fleets, megastructures, events, AI observation, and crisis triggers. Anything with a modded object ID is marked “replace with active-stack ID from local source/debugtooltip/help,” not left as a research question.

### 6. Modding tools and free online resources

**Answered finding.** The reliable public stack is Paradox Wiki for concepts and folder surfaces, CWTools for PDXScript/static validation, CWTools Stellaris config for schema rules, Irony for load order/conflict analysis, OldEnt’s generated trigger/effect/modifier lists for version-diff discovery, Steam/GitHub source/changelogs for mod-specific claims, and save/log tools for post-run evidence [S065][S066][S067][S068][S069][S070][S071][S072][S073][S074][S075][S076][S077][S078][S079][S080].

**Reliability hierarchy.** Exact syntax: current vanilla/mod source + CWTools + generated docs. Exact conflicts: Irony, not a generic “last mod wins” rule [S074][S076]. Conceptual docs: Paradox Wiki. Fast discovery: OldEnt and Steam/GitHub. Runtime behavior: logs/saves/observer runs only.

### 7. Starbase, orbital ring, and planetary defense strategy

**Answered finding.** Starbase Extended 3.0 is the best match for the requested stack because its page says it supports 4.**.*, Vanilla, NSC, and ACOT, and it adds starbase levels with many module/building slots [S041]. Expanded Starbases should not be used in the same NSC3 stack because its page says it is not compatible with NSC or other mods that modify the starbase ship-size file [S042]. Planetary-cannon mods are appealing conceptually, but the At War chain is old/3.9-labeled and should not be treated as current 4.4.x-ready without local source/launch proof [S043][S044]. Eternal Vigilance Redux is a promising add-on if automated defense-platform spending is desired, but its upkeep/economy behavior must be tested because it intentionally affects platform automation and AI spending policies [S045].

**Strategy.** Use Starbase Extended for chokepoints, shipyard throughput, and orbital defense infrastructure; do not rely on starbases alone for Gigas/25x crisis. Static defense should buy time, protect shipyards/megas, and force favorable engagements, not replace mobile crisis-counter fleets.

### 8. Planetary Diversity and Guilli strategy

**Answered finding.** Planetary Diversity changes planet variety and, through submods, can add gameplay-affecting worlds, archetypes, districts, jobs, buildings, deposits, and terraforming paths [S054][S055][S056]. Guilli’s Planet Modifiers and Features adds hundreds of planet modifiers and content that interacts with them, with special compatibility claimed for PD and Gigas [S057][S058]. Planet modifiers can be positive, negative, or mixed and affect colonies [S059].

**Strategy.** Prioritize planets by modifiers/deposits/jobs and strategic role, not by class name alone. In a crowded high-threat galaxy: research worlds with direct research modifiers and lab capacity first; alloy/industrial worlds with mineral/industrial support second; energy/mineral worlds that support megastructure inputs third; rare-resource worlds when they unlock bottleneck upkeep; unity/trade worlds only when they support ascension/market goals without delaying crisis readiness.

### 9. Modded resources and UI/resource visibility

**Answered finding.** URP solves a real problem: added strategic resources from different mods may be hidden or poorly displayed without a resource patch [S051]. UIOD and topbar submods expand UI capacity and resource display [S047][S050]. UIOD+Gigas and UIOD+PD patches fix parent-specific UI surfaces [S048][S049]. Users still report missing resources and load-order sensitivity, including cases fixed by moving URP lower/bottom [S052].

**Implementation decision.** Treat resource visibility as infrastructure, not QoL. If an AI route consumes sentient metal, quasi-negative mass, megaconstruction/supertensiles, ESC resources, or PD/Guilli special deposits, the UI and AI budget must expose those as first-class constraints. Hidden resources lead to false “AI is dumb” diagnoses because the player/tester cannot see the bottleneck.

### 10. 4.4.x and 4.5 modding hazards

**Answered finding.** 4.4.5 is the stable target and adds a Resource Abundance slider plus Nomad/Waystation/Arkship fixes that affect economy baselines and modded automation assumptions [S081]. 4.4 as a whole introduced Nomads/Arkships/Waylines/Contracts and broad UI/fleet/gameplay changes [S082]. The 4.5 Cygnus beta is a separate porting branch because pop groups are no longer divided by ethics/factions and save compatibility is explicitly broken [S083][S084]. 4.4 launcher behavior also disables mod lists on major update to reduce broken saves/crash-on-load issues [S085].

**Risk surfaces.** Pops, jobs, species, leaders, UI, ship designs, resources, AI economy, colony automation, factions, ethics, events, and launcher/playset state should not be casually version-bumped from 4.4.x to 4.5. Treat 4.5 as a new branch with static source diffs first, then CWTools/Irony, then disposable runtime tests.

## Final project decisions from the filled research

1. Make Stellar AI Director route-based: tech -> Mega Engineering -> Gigas special resources -> economy megas -> shipyard/naval conversion -> celestial/crisis counters.
2. Use the elite 2250 science curve as the high-threat AI target and the 500-800 science/year-50 line only as a lower-bound warning.
3. Keep NSC3 + ESC NEXT + SFT, but enforce ESC reactor configuration and validate ship behavior/computer slots before trusting designs.
4. Keep Starbase Extended as the static-defense pillar; reject Expanded Starbases for this NSC3 stack unless a custom compatibility patch is intentionally built.
5. Keep UIOD, UIOD+Gigas, UIOD+PD, Extended Topbar, and URP as infrastructure.
6. Do not treat current public AI mods as enough proof that AI can use Gigas/NSC3/ESC. Use observer benchmarks.
7. Treat 4.5 as a separate porting effort.
