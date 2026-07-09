# Gigastructural Engineering Findings

## Direct answer

Gigastructural Engineering should be handled as an escalation ladder: economy megastructures and special-resource acquisition first, construction throughput second, celestial military structures third, crisis-specific counters fourth. It is a mistake to treat Gigas as “more vanilla megastructures.” Its Workshop page says it adds a wide range of megastructures, weaponized planets, microwormholes, stellar lasers, system-spanning computers, and optional crises built to match the power of those megastructures [S001]. Recent changelogs mention attack moon upkeep, Planetary Computers, Systemcraft construction, and Hyperlane Formation Study behavior [S002], confirming that 4.4-era Gigas mechanics continue to touch economy, celestial fleets, and special events.

## Progression path that matters

### Phase 1: unlock and survival economy

- Keep research strong enough to reach Mega Engineering and Gigas prerequisites.
- Preserve energy, consumer goods, minerals, and strategic resources to sustain labs.
- Do not overbuild early fleets unless threatened.
- Do not spend rare Gigas resources on low-ROI structures while behind curve.

**Evidence:** high-end 25x strategy emphasizes early tech benchmarks [S017], and Gigas itself adds late systems whose counters require Gigas-scale power [S001].

### Phase 2: economy megastructures and special resources

Players identify Gigas special-resource routes such as quasi-negative mass and sentient metal with EHOF/cohesive-star exploration, and psionic sublimate with Shroud-oriented systems [S013]. The exact current object IDs must come from local Workshop source, but the strategy is filled: the AI must reserve these resources and pursue their acquisition routes before trying to execute late Gigas projects.

**AI rule:** every Gigas route should have explicit stockpile and monthly-income gates for special resources. Treat them like alloys, not like flavor.

### Phase 3: construction throughput

Players distinguish megastructure build capacity and build speed from actual resource throughput; too much build cap can become a trap when alloys and special resources cannot support it [S014].

**AI rule:** add build-cap/build-speed only when alloy/special-resource income and stockpiles can feed the cap. Otherwise, the AI creates many stalled projects and no fleet.

### Phase 4: celestial military escalation

Player discussions repeatedly describe attack moons, planetcraft, and systemcraft as the expected power class for Aeternum/Blokkat-tier fights [S009][S010][S011][S012]. These are not optional if Gigas crises are enabled at serious difficulty.

**AI rule:** when Gigas crises are enabled, route weights must eventually favor war moons/planetcraft/systemcraft or equivalent current Gigas celestial ships.

## Major Gigas threats and counters

### Katzenartig Imperium

**Filled answer:** do not try to match the Katzen head-on in early-midgame. Contact and support the resistance as early as possible [S006]. Use both resistance channels where available, trigger revolts to distract the Imperium, and sabotage the Kaisermoon to weaken/freeze the crisis before capital invasion [S007]. Older advice also recommends investing heavily in the resistance, using an attache to delay declaration, and preferring armor over shields in unavoidable open combat [S008].

**AI implication:** if Katzen appears, the AI needs an event-route flag that values resistance/support mechanics and defensive survival. Vanilla fleet-power comparison alone is not enough.

**Trap:** open conventional war before resistance/sabotage progress.

### Blokkats

**Filled answer:** Blokkats require a research/counter-mechanic route, not only fleets. The dev-diary-style source describes Blokkat Knowledge, Hyperdimensional Destabilizer progression, dismantlers/scrap, and shield-window mechanics [S004]. Player discussions recommend reading the event messages, using scrap for recurring research, building megastructures outside the Blokkat path, reaching knowledge thresholds, and jumping systemcraft during shield-down windows [S005]. Other player advice emphasizes science, Matrioshka Brain-style research scaling, continued attack moon/planetcraft construction, and multiple systemcraft [S012].

**AI implication:** create explicit Blokkat route stages: preserve science -> collect/convert scrap -> complete counter-research -> build/activate counterstructure -> attack during vulnerability -> maintain distant economy.

**Trap:** feeding fleets into the Vester before the research/counter window is open.

### Aeternum

**Filled answer:** Aeternum is meant for a full Gigas-run economy. Players describe needing planetcraft/systemcraft/attack moons and screening fleets [S009], plus enormous alloy throughput for shipyards, attack moons, planetcraft, systemcraft, and megastructures [S010]. Another discussion states the intended tools are planetcraft and systemcraft [S011].

**AI implication:** Aeternum-enabled games must weight celestial ships and shipyard capacity earlier. If the AI reaches Aeternum with only vanilla fleets, the failure is strategic, not tactical.

**Trap:** enabling Aeternum in a run where Gigas progression was disabled, delayed, or underfunded.

### Compound

**Filled answer:** public sources are less current and mostly conceptual, but community references describe Compound-style threats as event/research-gated before normal military solutions work [S015].

**AI implication:** classify Compound as “research/event gate first, fleet second” until local source identifies exact current event chain and trigger IDs.

## Mandatory choices versus traps

| Category | Mandatory / high-value | Trap / avoid |
|---|---|---|
| Game setup | Read Gigas startup selection; tune crises to intended curve | Enable every optional crisis at high settings without route support |
| UI | UIOD + Gigas patch when UIOD and Gigas are both active [S048] | Missing bottom interface / hidden Gigas UI |
| Resources | URP/resource visibility for Gigas resources [S051] | Debugging economy while special resources are hidden |
| Economy | Research + economy megas + special-resource acquisition [S001][S013] | Build-cap spam without alloy/special-resource throughput [S014] |
| Military | Attack moons, planetcraft, systemcraft when crises enabled [S009][S012] | Vanilla battleship-only plan against Gigas crises |
| Katzen | Resistance, revolt, sabotage, then capital invasion [S006][S007] | Head-on early war |
| Blokkats | Knowledge/research/scrap/counterstructure/systemcraft [S004][S005] | Attack before vulnerability/counter research |
| Aeternum | Full Gigas economy and celestial ships [S009][S010][S011] | Late activation in a non-Gigas-scaled run |

## AI Director route checklist

- `gigas_unlock_route`: Mega Engineering, Gigas AP/tech prerequisites, research speed.
- `gigas_economy_route`: economy megas, lab megas, alloy megas, energy/mineral megas.
- `gigas_special_resource_route`: sentient metal, quasi-negative mass, psionic sublimate, megaconstruction/supertensile-style throughput.
- `gigas_shipyard_route`: Mega Shipyard/Gigas shipyards/shipyard capacity.
- `gigas_celestial_route`: attack moons -> planetcraft -> systemcraft.
- `gigas_crisis_counter_route`: Katzen resistance, Blokkat knowledge, Aeternum celestial readiness, Compound event research.
