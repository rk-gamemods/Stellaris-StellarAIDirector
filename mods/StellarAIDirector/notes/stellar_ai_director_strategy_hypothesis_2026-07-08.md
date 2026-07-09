# Stellar AI Director Strategy Hypothesis

**Document role:** centralized working theory / strategy hypothesis  
**Generated:** 2026-07-08  
**Target project:** `StellarAIDirector` in the StellarisMods repository  
**Primary target version:** Stellaris PC 4.4.5 stable/current local install  
**Compatibility posture:** preserve 4.4.4 compatibility where practical; treat 4.5+ as a separate porting branch  
**Target playset profile:** high-scale modded game with Gigastructural Engineering & More (4.4), NSC3, Extra Ship Components NEXT, Starbase Extended 3.0, Universal Resource Patch, Planetary Diversity, and related UI/compatibility support

---

## 1. Status And Warning Label

This document is a **strategy hypothesis**, not a proven source of truth.

It consolidates strategic assumptions, design ideas, route theories, implementation intentions, and benchmark expectations that are currently scattered across the Stellar AI Director README, high-scale replacement audit, full replacement plan, opening/research/fleet specialization plan, research-federation pass, research-scaling audit, snowball checkpoints, threat-response plans, observer-loop runbook, and generated-source summaries.

It should be maintained as a central discovery document for the **intended AI approach**. It should not be treated as proof that the AI already executes the strategy successfully in-game. Runtime success requires fresh observer-game evidence, save/log inspection, and repeated tuning.

This document deliberately uses words such as **hypothesis**, **theory**, **expected**, **should**, **candidate**, and **needs validation**. These are intentional. The project is still in an empirical tuning phase.

---

## 2. Why This Document Exists

The Stellar AI Director project has accumulated multiple good but fragmented planning documents. The strategic spine is visible, but it is split across documents with different dates, statuses, and scopes. Some older files remain useful as provenance but should not be read as current launch truth. This document centralizes the strategic theory so future Codex agents and human maintainers can find the intended direction without reconstructing it from many partial plans.

This document should answer:

1. What is the AI actually trying to accomplish?
2. Why is generic vanilla/Stellar AI-style scaling insufficient for the current playset?
3. What economic, technology, expansion, war, megastructure, and fleet behaviors are believed necessary for 25x crisis relevance?
4. Which ideas are strategic hypotheses that need observer validation?
5. Which project files currently support or implement parts of the strategy?
6. What should future implementation and testing preserve, revise, or falsify?

---

## 3. Source Anchor Map

The document consolidates the following project sources:

| Source path | Role in this hypothesis |
| --- | --- |
| `mods/StellarAIDirector/README.md` | Current high-level scope, parent dependencies, absorbed/reimplemented surfaces, current strategic feature list, validation commands. |
| `research/stellar-ai/stellar-ai-director-full-replacement-plan-2026-07-06.md` | Broad strategic doctrine: Director as mod-set-aware policy layer, not broad guesses; explicit rules for modded objects and prerequisite chains. Historical/provenance, but strategically important. |
| `research/stellar-ai/stellar-ai-director-high-scale-replacement-audit-2026-07-06.md` | Failure diagnosis and high-scale correction: 20k fleet power vs 2M Katzenartig; need Gigas/NSC3/ESC megastructure/tech/fleet readiness. Historical/provenance, but important. |
| `research/stellar-ai/stellar-ai-director-opening-research-policy-fleet-specialization-implementation-plan-2026-07-07.md` | First-75-year strategy: research snowball, growth, policies/edicts, Research Federation, fleet doctrine, productive military use. |
| `research/stellar-ai/stellar-ai-director-research-federation-and-tech-snowball-pass-2026-07-07.md` | Research target correction, tech-rush support chain, Research Cooperative/research agreement surfaces, unity-to-research and military-to-pops route. |
| `research/stellar-ai/stellar-ai-director-research-scaling-audit-2026-07-06.md` | Early compounding gap analysis: pop assembly, labs, Gigas science kilostructures, Planetary Computer, research agreements, ACOT inactive-surface warning. |
| `research/stellar-ai/stellar-ai-director-snowball-checkpoints-2026-07-06.md` | Deterministic snowball ladder: survival floor, early research/build surface, kilostructures, megastructures, fleet conversion. |
| `plans/stellar-ai-director-threat-response-plan.md` and focused threat-response plan set | Bounded observed-aggression response: opinion/readiness only, no forced wars, no survival-gate bypass. |
| `research/stellar-ai/stellar-ai-observer-loop-runbook.md` | Empirical target: one or two top AI empires plausibly crisis-competitive by 2350 against 25x crisis pressure without hidden bonuses. |
| `research/stellar-ai/archive/standalone-baseline-cleanup-2026-07-08/README.md` | Interpretation warning: some older replacement/audit documents are historical or superseded for current launch proof, but remain useful as route provenance. |

---

## 4. Core Strategic Hypothesis

The working hypothesis is:

> A high-scale modded Stellaris AI cannot become crisis-relevant by passively improving vanilla priorities. It needs a deterministic, mod-set-aware strategy spine that converts early economic stability into aggressive research velocity, then converts research into megastructure unlocks, special-resource support, Mega Shipyard throughput, advanced hull/component access, and finally millions-scale fleet power. When boxed in, it must create breathing room through productive aggression, subjects, pops, or tall/habitat expansion rather than sitting in a small territory with idle fleets and weak research.

The project does not assume the AI can reason like a player. Instead, the Director should approximate a strong player’s route through explicit weighted surfaces:

```text
survival floor
  -> early economy compression
  -> pop and research snowball
  -> unity / tradition / ascension acceleration
  -> tech-card and unlock pressure
  -> kilostructure and early megastructure stepping stones
  -> Mega Engineering / Mega Shipyard / Gigas / NSC3 / ESC unlock chains
  -> special-resource and alloy reserve support
  -> planetcraft, war moon, systemcraft, and late economy megastructure routes
  -> fleet-throughput conversion into crisis-scale military power
```

The hypothesis is falsifiable. If observer testing shows the AI still fails to hit research, megastructure, and fleet benchmarks, the strategy document should be updated rather than defended.

---

## 5. Baseline Failure Case

The motivating failure was a crowded observer game where the strongest AI empire reached only about **20,000 fleet power by the mid-2300s** while the Katzenartig crisis reached roughly **2,000,000 fleet power**. The user also observed little or no meaningful AI megastructure construction.

The strategic interpretation is that the AI was not merely underbuilding ships. It was failing the entire high-scale route:

- insufficient early research velocity;
- insufficient economy to support research jobs;
- insufficient transition from economy into Mega Engineering and modded unlocks;
- insufficient megastructure construction and upgrade pacing;
- insufficient Mega Shipyard / naval-cap / alloy conversion;
- insufficient exploitation of Gigas/NSC3/ESC endgame routes;
- insufficient productive aggression or tall fallback when spatially constrained.

The response is not to simply increase fleet desire. More fleet power without tech and economy becomes an alloy sink. The response is to improve the whole ladder.

---

## 6. Benchmark Hypothesis

The observer-loop runbook defines a very high standard. This document adopts those targets as **benchmark hypotheses**, not proven reachable targets:

| Date / phase | Strategy target |
| --- | --- |
| 2270-2280 | roughly 1,000+ monthly research for competitive snowball candidates. |
| 2350 | roughly 5,000-6,000+ monthly research as a minimum crisis-relevance target. |
| 2350+ | one or two top AI empires plausibly able to continue scaling toward 25x crisis pressure without hidden AI/player economic bonuses. |
| 2350-2400+ | eventual fleet power on the order of millions to tens of millions, depending on crisis type, timing, and mod settings. |

A 2350 AI with only hundreds of monthly research is a failed benchmark even if it has improved economy or naval usage. Fleet power is diagnostic only when it is supported by tech, economy, shipyard throughput, and survival value.

Observer testing should therefore capture more than fleet power:

- monthly research;
- researched technology count and high-tier unlocks;
- Mega Engineering timing;
- Mega Shipyard timing;
- Gigas kilostructure/megastructure starts and completions;
- planetcraft/war moon/systemcraft route progress;
- NSC3 hull unlocks;
- ESC high-tier components/reactors/shields/weapons;
- alloys income and stockpile;
- trade/logistics capacity;
- naval capacity used/available;
- shipyard count and build throughput;
- empire size and research efficiency;
- pops, colonies, habitats, subjects, and conquered/vassalized income;
- crisis-fleet survivability.

---

## 7. Strategic Principles

### 7.1 The Director Must Be Mod-Set-Aware

The AI cannot be expected to infer a coherent route through Gigastructural Engineering, NSC3, ESC NEXT, Starbase Extended, Planetary Diversity, and the rest of the active stack from generic vanilla weights.

Every important modded object should be inventoried, classified, connected to prerequisites, and given explicit pursue/delay/ignore/exploit rules. Larger alloy reserves are not enough if the AI is not guided into the technologies, ascension perks, prerequisite structures, special resources, and build paths that spend those alloys.

### 7.2 Stellar AI Is Reference, Not Late-Game Baseline

Stellar AI remains useful as an early-game/economy reference and parity source, but the Director’s late-game strategy must supersede it for this high-power playset. The Director should absorb useful surfaces while replacing assumptions that do not scale into Gigas/NSC3/ESC late-game threats.

### 7.3 Research Is The Central Snowball Resource

For the current target, research is not just one economy category. It is the gate to:

- Mega Engineering;
- Mega Shipyard;
- Gigas science/economy kilostructures;
- planetcraft/systemcraft chains;
- NSC3 advanced hulls;
- ESC high-tier components;
- repeatables and late-game ship quality;
- endgame fleet power measured in millions rather than thousands.

The AI should treat under-curve research as an emergency strategic condition after survival needs are met.

### 7.4 Economy Exists To Feed Research, Unlocks, And Fleet Conversion

Energy, minerals, consumer goods, alloys, trade, special resources, naval capacity, unity, and pops should be understood as support systems for the route. The AI should avoid generic hoarding and instead spend surplus into the next bottleneck.

The current README already encodes a v1 surplus-sink order after survival and recovery gates:

```text
1. research sink
2. fleet-production sink
3. unity sink
```

This document adopts that ordering as the default hypothesis. It should be revised only if observer evidence shows the order produces deficits, stalled fleets, delayed ascension, or poor crisis readiness.

### 7.5 Fleet Investment Must Be Productive

Fleet investment is valuable when it buys survival, territory, pops, subjects, chokepoints, diplomatic leverage, or crisis readiness. Fleet that sits idle while the empire remains boxed in and under-researched is an economic drag.

The Director should support two different military functions:

1. **Survival/security floor:** enough fleet/starbase defense to avoid dying.
2. **Productive aggression:** fleet investment only when it can plausibly produce territory, pops, subjects, vassal income, chokepoints, or strategic breathing room.

### 7.6 Boxed-In Empires Need Escape Routes

A crowded galaxy is a core use case. If the AI has one to three planets and no cheap expansion path, it must not simply stagnate. It needs a deterministic branch:

1. If there is a weak nearby neighbor or vassalization target, pursue productive conquest/subject escape when safe.
2. If conquest is unsafe, blocked, or personality-incompatible, pivot to tall/habitat scaling.
3. Habitat and tall-scaling routes should be treated as expansion infrastructure, not flavor.

### 7.7 Megastructures Need A Prerequisite Ladder

The AI should not treat all megastructures as equal late-game luxuries. It needs a ladder:

1. early kilostructures and economy accelerators;
2. research acceleration structures;
3. Mega Engineering and Mega Shipyard;
4. economy megastructures and major research megastructures;
5. planetcraft / war moon / systemcraft routes;
6. crisis-scale shipyard/fleet conversion.

Superprojects should be gated by affordability, survival safety, special resources, and project availability. Attempt memory/cooldowns may be needed later to avoid repeated impossible reservations.

### 7.8 Safety Gates Beat Ambition

Survival, recovery, core deficits, short runway, and war pressure must override expansionary or speculative spending. The Director should be aggressive, but not self-destructive.

Strong AI behavior does not mean spending all resources immediately. It means spending into the highest leverage bottleneck while preserving enough runway to keep the economy alive.

---

## 8. Strategy Ladder By Game Phase

The year ranges below are working labels, not hardcoded truth. They should be tuned against observer data and difficulty/mod settings.

### Phase 0: Load/Validation/Eligibility

Before strategy matters, the mod must load and remain parse-safe. Current work should distinguish:

- source mod files;
- launcher/live installed mod surface;
- active playset order;
- static validation;
- runtime proof;
- observer proof.

Static validation can prove generated files exist, parse, and reference known objects. It cannot prove the AI is strategically successful.

### Phase 1: Opening Compression, 2200-2225

Hypothesis: the AI must build the foundation for a research economy without dying or overbuying idle fleets.

Priority surfaces:

- core deficit prevention;
- early minerals, energy, consumer goods, and alloy stability;
- early research lab/district availability;
- early pop-growth and pop-assembly decisions;
- initial starbase choke defense;
- early survey/expansion support;
- avoid overbuilding unstaffed jobs;
- avoid passive fleet overbuilding unless there is a real war/conquest/survival payoff.

Expected behavior:

- capital or best early high-pop world should become an early research concentration when support economy exists;
- support colonies should carry basic production and consumer-goods support;
- early policies and edicts should favor growth/research/economy without causing deficits;
- trade/logistics should be preserved as a real support surface, not bought/sold away as if it were a normal market commodity.

### Phase 2: Research And Pop Snowball, 2225-2250

Hypothesis: the AI needs compounding pop and research growth before midgame. Late megastructures cannot fix an empire that reaches 2300 with poor research velocity.

Priority surfaces:

- research lab upgrades;
- research districts and research-specialized planet designations where safe;
- pop assembly buildings for eligible empire types;
- clone/spawning/robot/machine assembly paths;
- consumer-goods support for researchers;
- energy support for upkeep and market smoothing;
- unity/tradition routes that accelerate research later;
- empire-size efficiency.

Candidate problem from research-scaling audit: pop assembly and research buildings may have had weak or passive Director treatment. The next strategy pass should verify whether generated weights actually cause AI construction, not merely observation.

### Phase 3: Mid-Early Strategic Commitment, 2250-2275

Hypothesis: by this point the AI should be specializing toward one or more coherent routes:

- direct research rush;
- unity-to-research;
- trade/logistics-to-research;
- boxed-in tall/habitat route;
- military-to-pops/subjects route;
- research-diplomacy route;
- Mega Engineering prerequisite rush.

Expected behavior:

- stronger preference for research pacts and Research Cooperative when legal, compatible, and useful;
- avoidance of lower-value federation types when the empire’s strategic role is research/economy snowball;
- coherent fleet doctrine lanes tied to tech choices;
- productive aggression only when there is likely gain;
- early tall/habitat pressure for boxed-in empires.

### Phase 4: Megastructure Prerequisite Rush, 2275-2300

Hypothesis: the AI must stop treating Mega Engineering and modded unlocks as optional surplus behavior. They are the bridge between ordinary AI scaling and high-scale modded crisis relevance.

Priority unlocks include:

- Mega Engineering;
- Mega Shipyard;
- Gigas science and economy kilostructures;
- NSC3 hull progression;
- ESC high-tier components and strategic resources;
- Gigas planetcraft/systemcraft prerequisites;
- ascension perks and traditions that unlock or accelerate megastructures.

The AI should be biased toward technologies and perks that lead to route unlocks, not merely locally efficient economy choices.

### Phase 5: Midgame Payoff Acceleration, 2300-2325

Hypothesis: completed early kilostructures and megastructures should fund the next tier. The AI needs direct build/upgrade pressure, reserve budgets, and special-resource support.

Priority surfaces:

- affordable economy kilostructures;
- science kilostructures;
- Science Nexus / Think Tank equivalents;
- Planetary Computer and its science districts where available;
- Mega Shipyard and shipyard infrastructure;
- alloy reserve and release logic;
- rare/special-resource runway;
- habitat/tall expansion if territory is limited;
- strategic chokepoint/starbase defense around critical build systems.

### Phase 6: Crisis-Scale Fleet Conversion, 2325-2350

Hypothesis: once the economy/research ladder is online, the AI must convert surplus into actual military output. This is where Mega Shipyard, naval capacity, alloy income, ship component tech, hull tech, and fleet doctrine must come together.

Priority surfaces:

- fleet-throughput economic subplans;
- Mega Shipyard payoff gates;
- naval-cap pressure;
- advanced hull unlocks;
- ESC component progression;
- fleet reinforcement and upgrade readiness;
- starbase defense support for critical systems;
- war-readiness for active crises and high-scale enemies.

Important distinction: fleet conversion should happen **after** enough research/economy structure exists to make the ships matter. Early fleet spam is not the same as crisis readiness.

### Phase 7: 2350-2400+ Endgame And Crisis Response

Hypothesis: endgame success requires one or two top AI empires to keep compounding. They should not stop at vanilla-style late-game ceilings.

Priority surfaces:

- repeatable tech and advanced component quality;
- Gigas planetcraft, war moon, systemcraft, and other high-scale routes if safe;
- continuous megastructure upgrades;
- special-resource stockpiles and production;
- sustained fleet replacement throughput;
- defensive critical-system protection;
- threat-response and crisis prioritization;
- avoiding self-destruction through impossible superprojects.

---

## 9. Strategic Route Families

### 9.1 Survival Floor Route

Goal: prevent collapse while preserving snowball potential.

Signals:

- war or imminent threat;
- core deficits;
- short stockpile runway;
- exposed chokepoints;
- low naval capacity or low fleet relative to neighbors;
- crisis proximity.

Outputs:

- pause speculative megastructure commitments;
- protect alloy/energy runway;
- build defensive chokepoints and starbases;
- maintain minimum fleet;
- recover trade/logistics if needed;
- avoid third-party foreign-affairs spending.

### 9.2 Direct Research Route

Goal: maximize research throughput early enough to unlock late-game routes.

Signals:

- research below curve;
- safe basic economy;
- available building slots or research districts;
- sufficient consumer goods/energy/minerals;
- high-pop capital or research-suitable colony;
- access to research buildings/kilostructures.

Outputs:

- stronger research lab/building/district weights;
- capital/research-world specialization;
- support colony basic production;
- research edicts/policies where valid;
- tech alternatives and research speed bonuses;
- research federation and research agreement support where valid.

### 9.3 Pop Assembly / Growth Route

Goal: increase the number of productive pops that can staff research, alloy, CG, and special-resource jobs.

Signals:

- eligible empire type;
- safe upkeep runway;
- building slot availability;
- strong long-term growth payoff;
- no severe deficit or housing/job trap.

Outputs:

- robot assembly, machine assembly, clone vats, spawning pools, and equivalent buildings for valid empires;
- avoid invalid empire-type paths;
- avoid overbuilding unsupported jobs;
- couple growth with housing/jobs/research-plan support.

### 9.4 Unity-To-Research Route

Goal: use traditions, ascension perks, and unity-driven bonuses to compound research before 2300.

Signals:

- unity production can accelerate key tradition/perk completion;
- Discovery/Diplomacy/research-relevant traditions available;
- ascension routes provide major research/economy payoff;
- empire has enough economy to avoid unity starving research.

Outputs:

- favor traditions/perks that convert into research speed, tech alternatives, megastructure access, or economy multipliers;
- avoid generic unity hoarding;
- avoid unity routes that do not feed the high-scale plan.

### 9.5 Research Diplomacy Route

Goal: use diplomacy to amplify research when compatible.

Signals:

- non-genocidal, compatible diplomacy profile;
- materialist/machine/discovery/research-oriented empire;
- friendly neighbors;
- embassy/trust/opinion gates achievable;
- Research Cooperative legal and plausible.

Outputs:

- prefer Research Cooperative over generic federation types when research snowballing is the strategic role;
- prefer research agreements when prerequisites are met;
- improve trust/opinion/embassy setup where valid surfaces exist;
- avoid forcing diplomacy for empires whose ethics/civics make it implausible.

### 9.6 Productive Aggression / Military-To-Pops Route

Goal: use military investment to create economic/research breathing room.

Signals:

- boxed-in empire;
- weak neighbor or subject target;
- claim/vassalization/conquest opportunity;
- sufficient alloy/energy/naval runway;
- compatible personality/ethics/war philosophy;
- strategic chokepoint or pop gain available.

Outputs:

- early alloy/naval weight only when a real payoff exists;
- conquest/subjugation/raiding pressure where legal and safe;
- avoid fleet overbuilding if there is no expansion, subject, pop, survival, or defensive purpose;
- prefer wars that buy colonies, pops, subjects, territory, or crisis-relevant economy.

### 9.7 Boxed-In Tall / Habitat Route

Goal: give small-territory empires a non-stagnation path.

Signals:

- one to three colonies;
- no cheap expansion path;
- conquest unsafe or blocked;
- habitat tech/build surfaces available;
- enough economy for tall investment.

Outputs:

- habitat tech pressure;
- habitat construction starts;
- tall-scaling buildings and districts;
- research-focused habitats where economy supports them;
- avoid treating habitats as flavor.

### 9.8 Kilostructure And Megastructure Ladder Route

Goal: move from ordinary economy to high-scale Gigas/NSC/ESC economy.

Signals:

- Mega Engineering path emerging;
- early Gigas tech available;
- affordability gates satisfied;
- safe alloy/special-resource reserves;
- expected payoff before crisis horizon.

Outputs:

- early economy kilostructures;
- science kilostructures;
- Mega Engineering pressure;
- Mega Shipyard pressure;
- economy megastructure starts/upgrades;
- late planetcraft/war moon/systemcraft paths with safety gates.

### 9.9 Special Resource And Logistics Route

Goal: prevent advanced projects and components from stalling on hidden support resources.

Signals:

- ESC/Gigas advanced tech unlocked or near unlock;
- special-resource upkeep/cost gates;
- strategic-resource deficits;
- trade/logistics bottlenecks;
- stockpile cap waste.

Outputs:

- special-resource budgets;
- energy/trade/logistics reserves;
- cap-breaker conversion for wasted marketable stockpiles;
- avoid treating trade as a disposable market commodity.

### 9.10 Fleet Throughput Route

Goal: convert economy into real military power once unlocks and shipyard capacity exist.

Signals:

- Mega Shipyard unlocked or available;
- strong alloy/energy/trade surplus;
- naval-cap headroom or ability to expand it;
- advanced hull/component tech;
- crisis or serious military threat.

Outputs:

- fleet-throughput economic subplans;
- naval cap targets;
- Mega Shipyard payoff exploitation;
- shipyard and reinforcement throughput;
- component/hull tech priorities;
- critical-system defense.

---

## 10. Threat Response Theory

The current threat-response strategy is intentionally bounded.

The Director may react to observed classified aggression through:

- opinion modifiers;
- timed relation/country flags;
- tightly capped third-party defensive-readiness economy pressure.

It must not:

- declare wars;
- join wars;
- add punitive casus belli;
- override diplomatic actions;
- bypass survival/recovery/deficit gates;
- punish unknown or unclassified war goals.

Threat response is not the main crisis-scaling engine. It is a diplomacy/readiness layer that can make aggression matter without turning the AI into a reckless forced-war machine.

Future punitive-war or containment behavior, if ever implemented, should be treated as a separate plan with direct-threat gates, capability gates, cooldowns, proximity checks, and runtime proof.

---

## 11. Current Implementation Interpretation

The current `mods/StellarAIDirector/README.md` says the mod now includes or attempts to include:

- decision-state triggers for survival, recovery, megastructure prep, safe commit, surplus-sink pressure, and shipyard payoff;
- high-scale megastructure alloy budgeting;
- a base economic-plan replacement that forces research, alloy, trade, naval cap, tall scaling, and megastructure pressure;
- targets for alloy reserves, Gigas special resources, static defense, and starbases;
- trade-capacity recovery and reserve subplans;
- market cap-breaker behavior for wasted stockpiles;
- stranded-fleet recovery guard;
- fleet-throughput economic subplan;
- planetary-capacity and research/habitat science construction weights;
- mandatory unlock-research pressure toward Mega Engineering, Mega Shipyard, planetcraft/systemcraft, NSC hulls, and ESC component tiers;
- bounded threat response;
- full-object route overrides for major Gigas/NSC3/ESC/AP/tradition/economy routes;
- manual-review blockers for ESC component-template `key = ...` overrides and direct NSC3 ship-design templates.

Interpretation: the source indicates the project has moved beyond pure planning, but runtime behavior remains unproven until new observer evidence is collected for the current standalone state.

---

## 12. Guardrails And Non-Goals

### 12.1 Non-Goals

The strategy does not require:

- hidden AI economic bonuses;
- launching runtime observer games as part of every Codex task;
- forcing wars through event effects;
- treating old Stellar AI behavior as the late-game baseline;
- hardcoding unverified Stellaris triggers/effects/scopes;
- replacing every parent mod object blindly;
- relying on ACOT or inactive mods unless they are active in the launcher surface;
- treating a single static validation pass as proof of success.

### 12.2 Safety Rules

The Director should fail closed when unsure:

- unknown war goals are inert;
- unsupported project branches are delayed or ignored;
- unverified hooks are researched before implementation;
- survival/recovery/deficit gates override speculative spending;
- runtime testing is not claimed unless actual observer artifacts exist;
- parent-mod AI support is inspected before being overwritten.

### 12.3 Validation Boundary

Static validation should prove:

- generated files exist;
- PDXScript is structurally parseable where validators support it;
- references resolve to known vanilla/mod/generated objects;
- generated objects are named and placed correctly;
- forbidden effects are absent;
- strategy surfaces do not bypass safety gates.

Static validation should not claim:

- the AI hit 2350 research targets;
- the AI built the right megastructures;
- the AI used fleets productively;
- the AI can beat or survive a 25x crisis.

---

## 13. Observer Testing Theory

The observer loop is the empirical engine for this document.

Recommended checkpoint years:

- 2250;
- 2275 or 2280;
- 2300;
- 2325;
- 2350;
- 2375 if needed;
- 2400 if testing late crisis conversion.

Recommended outputs:

| Metric | Why it matters |
| --- | --- |
| Monthly research | Primary curve health. |
| Tech count and key unlocks | Confirms the AI reaches the route gates. |
| Mega Engineering year | Critical transition point. |
| Mega Shipyard year | Fleet-throughput conversion point. |
| Gigas kilostructures/megastructures | Confirms AI uses modded assets. |
| NSC3 hull unlocks | Confirms ship-class scaling. |
| ESC component tiers | Confirms quality scaling. |
| Alloy income/stockpile | Confirms fleet/megastructure affordability. |
| Energy/trade/logistics | Confirms upkeep runway. |
| Naval capacity used/available | Confirms fleet conversion, not just build desire. |
| Pops/colonies/habitats/subjects | Confirms expansion or tall/subject escape. |
| Fleet power | Final diagnostic, not sufficient alone. |
| Crisis engagement outcome | Ultimate but noisy runtime signal. |

A future benchmark report should classify outcomes as:

- **invalid run**: mod not loaded, broken playset, wrong settings, bad observer setup;
- **failed trajectory**: research/economy far below curve;
- **partial improvement**: some metrics improved but no crisis-relevant route;
- **route success / fleet failure**: tech/megastructures unlocked, but fleet conversion failed;
- **fleet success / route concern**: fleet rose, but without sustainable tech/economy path;
- **candidate success**: one or two top AI empires plausibly scale toward 25x crisis relevance.

---

## 14. Open Questions

These questions should be maintained as first-class strategy risks.

### 14.1 Research And Economy

1. Are research labs and research districts being actively built by the generated Director layer, or merely observed through inherited Stellar AI behavior?
2. Are pop assembly buildings being built early enough for eligible empire types?
3. Do early CG/energy/mineral supports prevent lab staffing collapse?
4. Does unity-to-research produce faster pre-2300 research, or does it starve direct research?
5. Are empire-size penalties being offset by enough output-per-size improvement?

### 14.2 Diplomacy

1. Do research-oriented AI empires form Research Cooperatives more often?
2. Do they satisfy research agreement prerequisites often enough?
3. Are personality overrides needed, or can safer federation/tradition/diplomacy weights do enough?
4. Do diplomacy weights conflict with militarist/productive-aggression routes?

### 14.3 Expansion And War

1. Do boxed-in empires choose conquest/subject escape when it is profitable?
2. Do they avoid idle fleet buildup when there is no useful target?
3. Do they pivot to habitats/tall scaling when conquest is unsafe?
4. Can productive aggression be improved without forced-war event behavior?

### 14.4 Megastructures And Gigas Routes

1. Which Gigas exotic branches should most AI empires be allowed to pursue?
2. Which should be restricted to certain personalities or high-performing empires?
3. Are early science/economy kilostructures weighted strongly enough?
4. Does the AI both build Planetary Computer and fill science districts?
5. What reserve targets are correct for each superproject stage?
6. Are project cooldowns or memory flags needed to prevent impossible reservation loops?

### 14.5 Fleet And Components

1. Does Mega Shipyard unlock actually convert into built fleet power?
2. Does NSC3 hull progression happen on time?
3. Does ESC component progression happen on time?
4. Are direct NSC3 ship-design templates required, or can tech/component pressure suffice?
5. Does fleet upgrade behavior require additional support, or is tech/component readiness enough?

### 14.6 Runtime Proof

1. Is the current standalone baseline loaded in the actual live playset?
2. Are old observer runs invalid for current state after cleanup?
3. What are the first new observer-run results after this consolidation?
4. Which hypothesis sections are falsified by the next run?

---

## 15. Maintenance Protocol

This document should be updated when:

- observer results contradict a hypothesis;
- a route is implemented or removed;
- a source plan is superseded;
- a new major mod is added or removed;
- Stellaris version changes from 4.4.5;
- Gigas/NSC3/ESC changes major object IDs or prerequisites;
- the live playset changes;
- validation discovers an unsafe or invalid hook;
- a user decision changes strategy priority.

Recommended update format:

```text
YYYY-MM-DD update:
- What changed:
- Evidence source:
- Affected hypothesis section:
- Strategic impact:
- Required implementation/test follow-up:
```

Do not silently delete failed hypotheses. Move them to a rejected/deprecated subsection with evidence, so future agents do not rediscover and reimplement them.

2026-07-09 update:
- What changed: Added a targeted follow-up hypothesis after observer run `observer-20260709T080545Z` failed the 2350 research benchmark. The run's top eligible AI reached only 1018.93 monthly research by 2350, and save inspection showed research-designated planets with almost no staffed research jobs.
- Evidence source: `research/stellar-ai/observer-runs/observer-20260709T080545Z/checkpoints.csv`, `summary.md`, `manual-notes.md`, and save inspection of `checkpoint-2350-autosave_2350.01.01.sav`. Example: `EMPIRE_DESIGN_humans1` had research-designated colonies such as `HUMAN1_PLANET_Spring` and `HUMAN1_PLANET_NewCoventry` but zero decoded research jobs on those worlds; the same save showed high parsed megastructure counts were mostly Dyson swarms, asteroid/orbital industry assets, and other non-research structures rather than a research snowball.
- Affected hypothesis section: 9.2 Direct Research Route, 13 Observer Testing Theory, 14.1 Research And Economy, and 14.4 Megastructures And Gigas Routes.
- Strategic impact: Megastructure count alone is not a success proxy. The next patch should make existing research designations materially increase lab/science-district construction pressure while preserving support-economy gates, and should continue distinguishing research-producing megastructures from generic economy/industry megastructures.
- Required implementation/test follow-up: Apply only source-backed designation-aware pressure to generated research infrastructure weights; do not broad-rewrite `common/colony_types` unless later evidence proves the colony selection layer itself is the bottleneck. The next observer run must verify research jobs, labs, science districts, and research megastructure composition, not just total parsed megastructure count.

---

## 16. Recommended Repository Placement

Recommended destination path inside the repo:

```text
research/stellar-ai/stellar-ai-director-strategy-hypothesis-2026-07-08.md
```

Optionally, after the strategy stabilizes, create a shorter pointer from:

```text
mods/StellarAIDirector/notes/strategy-hypothesis.md
```

That pointer should link to the maintained research document rather than duplicating it.

---

## 17. Compact Strategy Statement For Future Agents

Use this as the short version when orienting a coding agent:

> Stellar AI Director is trying to make AI empires in a high-power Gigas/NSC3/ESC playset scale like competent late-game contenders, not like vanilla AI with slightly better budgets. The working theory is that 25x crisis relevance requires early economic compression, aggressive research snowballing, productive military expansion when boxed in, strong unity/diplomacy/federation support where useful, explicit Mega Engineering / Mega Shipyard / Gigas / NSC3 / ESC unlock ladders, special-resource and alloy reserve support, and conversion of completed economy/research assets into millions-scale fleet throughput. This is a hypothesis, not proven doctrine; static validation proves files are safe, while observer runs prove or falsify the strategy.
