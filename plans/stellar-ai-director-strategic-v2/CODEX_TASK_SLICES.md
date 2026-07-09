# Stellar AI Director V2 Codex Task Slices

Generated: 2026-07-08
Packet: Stellar AI Director Strategic V2 Roadmap Packet
Target: Stellaris PC 4.4.5 stable/current, backwards compatible with 4.4.4 where source-backed


## How Codex Should Use These Cards

Pick one card, complete it, validate it, and report its status. Do not implement the entire roadmap in one commit. Cards are designed to be independently reviewable unless dependencies say otherwise.

Minimum checks for most implementation cards:

```powershell
python tools\generate_stellar_ai_director_patch.py
python tools\validate_stellar_ai_director_patch.py
python -m py_compile tools\stellar_ai_director_lib.py tools\generate_stellar_ai_director_patch.py tools\validate_stellar_ai_director_patch.py
python -m unittest discover -s tools\tests
git diff --check
```

Runtime/observer cards are approval-gated and must not be run by default.


## T00 - Re-read current baseline and source hierarchy

| Field | Contract |
| --- | --- |
| Objective | Establish the current implementation frame before editing. |
| Inputs | 02_PROJECT_CONTROL_AND_GUIDANCE.md; 04_STELLAR_AI_DIRECTOR_CONTEXT.md; current README/descriptor/load-order notes; standalone parity inventory. |
| Likely files | No code files unless docs are stale. |
| Exact checks | Stale wording search for 4.4.4-as-current, 4.4.5-beta, required Stellar AI dependency, runtime proof claims. |
| Acceptance criteria | A short research/status note or updated existing note states current 4.4.5 target, standalone status, required parents, and deferred gaps. |
| Dependencies | None |
| Expected artifacts | Updated source-readiness note or no-change report. |

## T01 - Refresh generator/static baseline

| Field | Contract |
| --- | --- |
| Objective | Regenerate and validate before strategic edits so later diffs are meaningful. |
| Inputs | Current generator and validator; generated mod files. |
| Likely files | tools/stellar_ai_director_lib.py; generated outputs under mods/StellarAIDirector; research/stellar-ai generated audits. |
| Exact checks | python tools/generate_stellar_ai_director_patch.py; python tools/validate_stellar_ai_director_patch.py; python -m unittest discover -s tools/tests; git diff --check. |
| Acceptance criteria | Commands pass or failures are classified before new behavior work. |
| Dependencies | T00 |
| Expected artifacts | Validation transcript and regenerated artifacts if changed. |

## T02 - Add stale-dependency validator

| Field | Contract |
| --- | --- |
| Objective | Prevent reintroducing Stellar AI as launch dependency or current doc requirement. |
| Inputs | README, descriptor, load-order notes, research README, archive index. |
| Likely files | tools/validate_stellar_ai_director_patch.py; tools/tests/test_stellar_ai_director.py. |
| Exact checks | Unit test seeded bad descriptor/doc wording; normal validation. |
| Acceptance criteria | Validator fails if current surfaces imply Stellar AI is required; archive/historical references allowed only in archive context. |
| Dependencies | T01 |
| Expected artifacts | Test and validator extension. |

## T03 - Add forbidden-surface gate

| Field | Contract |
| --- | --- |
| Objective | Make unsafe folders fail unless explicitly allowed by a researched task flag. |
| Inputs | Current roadmap gaps; technical contracts. |
| Likely files | validator; tests. |
| Exact checks | Create fixtures or checks for common/diplomatic_actions, common/personalities, direct ship-design/component-template/section-template/ship-size outputs. |
| Acceptance criteria | Default generated patch contains none of these folders unless a future whitelisted task changes contract. |
| Dependencies | T01 |
| Expected artifacts | Forbidden surface validation test. |

## T04 - 4.4.5 log-risk classifier

| Field | Contract |
| --- | --- |
| Objective | Turn latest load-freeze/error patterns into a static triage report so Codex can separate Director vs parent issues. |
| Inputs | 4.4.5 triage note; error summaries; tools/log summarizers. |
| Likely files | tools/stellar_ai_director_lib.py or new helper; research/stellar-ai/*4-4-5-log-risk*.md/csv. |
| Exact checks | Run classifier on latest summary artifacts; unit test pattern categories. |
| Acceptance criteria | Report classifies Gigas orbital/frameworld, ESC deferred refs, uses_ship_category scope, has_job, starbase modules, and Director-owned issues separately. |
| Dependencies | T01 |
| Expected artifacts | 4.4.5 log-risk report and tests. |

## T05 - Object atlas freshness gate

| Field | Contract |
| --- | --- |
| Objective | Ensure route and object evidence is current before route changes. |
| Inputs | object atlas, dependency edges, parent AI support map, policy matrix. |
| Likely files | tools/build_stellar_ai_director_object_atlas.py; research/stellar-ai/object-atlas/*.csv/md. |
| Exact checks | python tools/build_stellar_ai_director_object_atlas.py; validate object atlas artifacts. |
| Acceptance criteria | Atlas outputs refresh cleanly or Codex records exact blocker. |
| Dependencies | T01 |
| Expected artifacts | Refreshed atlas artifacts or freshness note. |

## T06 - First-75-year route trigger review

| Field | Contract |
| --- | --- |
| Objective | Review existing opening route triggers and identify missing support gates. |
| Inputs | opening research/policy/fleet implementation plan; generated triggers; economic plan. |
| Likely files | tools/stellar_ai_director_lib.py; common/scripted_triggers/zzzz_staid_10_opening_strategy_triggers.txt. |
| Exact checks | Generator; validator; tests for trigger names and no missing references. |
| Acceptance criteria | Route triggers are documented, generated, and reusable across economy/policy/tech without persistent-state guesses. |
| Dependencies | T01 |
| Expected artifacts | Route trigger review note and tests. |

## T07 - Research-world construction pressure pass

| Field | Contract |
| --- | --- |
| Objective | Strengthen safe early labs/research districts while preserving support economy. |
| Inputs | research-scaling audit; building/district generated files; economic valuation datasets. |
| Likely files | generator; common/buildings; common/districts; economic plan; tests. |
| Exact checks | Validate references; test support-resource gates; inspect generated weights. |
| Acceptance criteria | AI gets stronger research construction pressure only when CG/energy/mineral runway is safe; no unconditional lab spam. |
| Dependencies | T06 |
| Expected artifacts | Generated research construction pass and tuning note. |

## T08 - Pop assembly active-pressure pass

| Field | Contract |
| --- | --- |
| Objective | Promote assembly/growth objects where source supports safe build pressure. |
| Inputs | Research-scaling audit pop assembly table; vanilla/current mod object definitions. |
| Likely files | generator; common/buildings/zzzz_staid_07_pop_assembly_buildings.txt; tests. |
| Exact checks | Tests for empire-type gates; reference audit; validator. |
| Acceptance criteria | Robot/machine/clone/hive assembly objects have source-backed pressure and invalid empire paths are excluded. |
| Dependencies | T06 |
| Expected artifacts | Generated pop assembly pass and evidence note. |

## T09 - Support economy bridge audit

| Field | Contract |
| --- | --- |
| Objective | Make sure CG, energy, minerals, food, trade capacity, and strategic resources support research/fleet routes without flattening. |
| Inputs | trade-capacity audit; economic plans; resource datasets. |
| Likely files | economic plan; script triggers; tests. |
| Exact checks | Validator checks trade/special-resource gates; no generic trade sell/buy flattening. |
| Acceptance criteria | Support resources remain first-class bottlenecks with safe gates. |
| Dependencies | T07,T08 |
| Expected artifacts | Support economy gate report and generated updates. |

## T10 - Unity-to-research route pass

| Field | Contract |
| --- | --- |
| Objective | Weight traditions/APs that convert into research tempo and modded progression. |
| Inputs | opening plan; AP/tradition files; route overrides; object atlas. |
| Likely files | generator; common/traditions; common/ascension_perks; tests. |
| Exact checks | Generated AP/tradition files parse; route rationale comments present; references resolve. |
| Acceptance criteria | Discovery/Diplomacy/ascension/research payoff paths are source-backed and not generic unity hoarding. |
| Dependencies | T06 |
| Expected artifacts | Generated unity-to-research pass. |

## T11 - Research diplomacy safe lane

| Field | Contract |
| --- | --- |
| Objective | Preserve Research Cooperative and research-friendly diplomacy without unsafe action/personality overrides. |
| Inputs | open roadmap; research federation file; research agreement evidence. |
| Likely files | common/federation_types; policies; traditions; research note. |
| Exact checks | Tests confirm no diplomatic_actions/personalities output; federation file parses. |
| Acceptance criteria | Research Cooperative preference is maintained; research agreement formation remains gated unless proven. |
| Dependencies | T03,T10 |
| Expected artifacts | Research diplomacy note and static updates. |

## T12 - Research agreement surface study

| Field | Contract |
| --- | --- |
| Objective | Determine whether a safe implementation path exists for research agreements. |
| Inputs | Vanilla action_form_research_agreement; active-stack winners; diplomacy/personalities. |
| Likely files | research/stellar-ai/*research-agreement-surface*.md/csv. |
| Exact checks | JDoc/JCode/JData inspection; no generated gameplay output. |
| Acceptance criteria | Report explains prerequisites, winning objects, conflict risk, and recommends implement/defer. |
| Dependencies | T11 |
| Expected artifacts | Research agreement surface report. |

## T13 - Gigas route blocker refresh

| Field | Contract |
| --- | --- |
| Objective | Find missing route edges or special-resource blockers for Gigas/Mega Engineering/Mega Shipyard. |
| Inputs | object atlas; dependency edges; Gigas route reports; generated megastructures. |
| Likely files | research report; generator only if safe missing route found. |
| Exact checks | Atlas and route report refresh; reference audit. |
| Acceptance criteria | Each high-priority Gigas route has prerequisites/resource blockers recorded; no broad rewrite without proof. |
| Dependencies | T05 |
| Expected artifacts | Gigas blocker report and optional small route patch. |

## T14 - Megastructure reserve and continuation contract

| Field | Contract |
| --- | --- |
| Objective | Validate current reserve budgets and define queue-continuation proof method. |
| Inputs | ai_budget files; economic plan; megastructure files; observer-test-log. |
| Likely files | research report; tests if static blockers identified. |
| Exact checks | Budget parse; reference audit; no runtime claims. |
| Acceptance criteria | Codex can tell what static reserves do and what runtime evidence is still needed. |
| Dependencies | T13 |
| Expected artifacts | Queue continuation research contract. |

## T15 - NSC3/ESC lane evidence graph

| Field | Contract |
| --- | --- |
| Objective | Map ship tech/component/section/ship-size graph before direct handling. |
| Inputs | ship-design-reference checks; ESC/NSC source snapshots; route overrides. |
| Likely files | research/stellar-ai/*nsc3-esc-ship-stack-lane*.md/csv. |
| Exact checks | JData/JCode graph inspection; no generated direct ship overrides. |
| Acceptance criteria | Report identifies safe tech/resource support and blocks direct templates until loader semantics are proven. |
| Dependencies | T05 |
| Expected artifacts | NSC3/ESC lane report. |

## T16 - ESC resource readiness support pass

| Field | Contract |
| --- | --- |
| Objective | Improve ESC special resource/component tech support only through safe technology/economy levers. |
| Inputs | ESC lane report; current esc_component_route rows. |
| Likely files | generator; common/technology; economic plan; tests. |
| Exact checks | No component-template output; references resolve; resource gates exist. |
| Acceptance criteria | AI is better prepared for ESC high-tier components without direct component-template overrides. |
| Dependencies | T15 |
| Expected artifacts | Generated ESC readiness pass. |

## T17 - NSC3 hull readiness support pass

| Field | Contract |
| --- | --- |
| Objective | Improve NSC3 hull and fleet-throughput readiness via safe tech/economy levers. |
| Inputs | NSC3 lane report; current tech route rows; fleet-throughput plan. |
| Likely files | generator; common/technology; economic plans; tests. |
| Exact checks | No direct ship-design output; Mega Shipyard/fleet-throughput gates parse. |
| Acceptance criteria | AI reaches NSC3 hull routes with supporting economy, not guessed designs. |
| Dependencies | T15 |
| Expected artifacts | Generated NSC3 readiness pass. |

## T18 - Hostile fauna clearance inventory

| Field | Contract |
| --- | --- |
| Objective | Inventory cheap early blockers and rewards before increasing clearance aggression. |
| Inputs | Planetary Diversity profile follow-up; vanilla/mod fauna/events. |
| Likely files | research/stellar-ai/*hostile-fauna-clearance*.md/csv. |
| Exact checks | Source inspection; no generated reserve change unless target power/reward categories exist. |
| Acceptance criteria | Targets are classified cheap blocker vs leviathan/unsafe; implementation recommendation clear. |
| Dependencies | T06 |
| Expected artifacts | Hostile fauna inventory. |

## T19 - Hostile fauna reserve tuning

| Field | Contract |
| --- | --- |
| Objective | Add or refine early fleet reserve pressure for safe clearance targets only. |
| Inputs | Hostile fauna inventory; existing fleet/economic plan. |
| Likely files | generator; economic plan; tests. |
| Exact checks | Forbidden suicide targets test; references resolve. |
| Acceptance criteria | AI reserves small fleet for proven cheap blockers without attacking oversized guardians. |
| Dependencies | T18 |
| Expected artifacts | Generated hostile fauna reserve pass. |

## T20 - Fleet payoff route review

| Field | Contract |
| --- | --- |
| Objective | Audit militarist/conquest/raiding/fleet routes against economic payoff. |
| Inputs | opening plan; bombardment stance; economic plan; war mechanics reference. |
| Likely files | research note; generator if small safe tuning. |
| Exact checks | No forced war effects; tests for raiding/conquest routes; validator. |
| Acceptance criteria | Fleet pressure has documented payoff route and safety gates. |
| Dependencies | T06 |
| Expected artifacts | Fleet payoff review and optional generated tuning. |

## T21 - War-chain research plan

| Field | Contract |
| --- | --- |
| Objective | Design advanced war-chain pass without implementation. |
| Inputs | war-mechanics-reference; claims/CB/wargoals; threat-response plan. |
| Likely files | research/stellar-ai/*war-chain-v2-plan*.md/csv. |
| Exact checks | Source verification; no declare_war/join_war/add_casus_belli output. |
| Acceptance criteria | Report identifies safe future levers and forbidden paths. |
| Dependencies | T20 |
| Expected artifacts | War-chain research plan. |

## T22 - Starbase Extended defense surface study

| Field | Contract |
| --- | --- |
| Objective | Verify starbase modules/buildings/scopes before expanding defense behavior. |
| Inputs | Starbase Extended scope report; active conflict matrix; generated starbase files. |
| Likely files | research/stellar-ai/*starbase-defense-v2*.md/csv. |
| Exact checks | Irony Analyze Only; scope validation; reference audit. |
| Acceptance criteria | Source-backed list of safe starbase/defense AI levers exists. |
| Dependencies | T05 |
| Expected artifacts | Starbase defense surface report. |

## T23 - Defense/crisis economic gate pass

| Field | Contract |
| --- | --- |
| Objective | Refine static defense pressure tied to threat/crisis/economy state. |
| Inputs | Starbase study; threat-response triggers; economic plan. |
| Likely files | generator; starbase modules/buildings; economic plan; tests. |
| Exact checks | Generated files parse; survival/recovery/deficit gates; no over-defense unconditional weights. |
| Acceptance criteria | Defense investment is risk/economy-gated and compatible with Starbase Extended. |
| Dependencies | T22 |
| Expected artifacts | Generated defense pass. |

## T24 - Planetary Diversity targeted expansion review

| Field | Contract |
| --- | --- |
| Objective | Find high-value PD worlds/buildings/districts beyond current targeted support. |
| Inputs | PD profile; economic valuation datasets; current PD generated files. |
| Likely files | research/stellar-ai/*pd-targeted-expansion*.md/csv. |
| Exact checks | JData inspection; no broad designation rewrite. |
| Acceptance criteria | High-value PD targets and blockers documented. |
| Dependencies | T05 |
| Expected artifacts | PD targeted expansion report. |

## T25 - Colony/designation safe patch

| Field | Contract |
| --- | --- |
| Objective | Add targeted planet/colony support only where report shows safe gap. |
| Inputs | PD targeted report; colony/designation winners. |
| Likely files | generator; decisions/buildings/districts/triggers; tests. |
| Exact checks | Reference audit; no broad colony_type rewrite unless source-proven. |
| Acceptance criteria | Targeted planet logic improves ROI without fighting vanilla automation. |
| Dependencies | T24 |
| Expected artifacts | Generated PD/colony patch. |

## T26 - 4.4.5 Nomad/Arkship compatibility audit

| Field | Contract |
| --- | --- |
| Objective | Ensure touched economy/planet/war/starbase surfaces account for Nomads, Arkships, Waystations, Waylines, Contracts, Operational Reserves. |
| Inputs | 4.4.5 triage; vanilla files; generated changes from T07-T25. |
| Likely files | research/stellar-ai/*nomad-arkship-compat*.md; tests if needed. |
| Exact checks | Source inspection; generated references check; no invented Nomad assumptions. |
| Acceptance criteria | Every touched surface has normal/Nomad compatibility classification. |
| Dependencies | T07,T09,T23,T25 |
| Expected artifacts | Nomad/Arkship compatibility report. |

## T27 - Docs refresh after implementation slice

| Field | Contract |
| --- | --- |
| Objective | Update README/load-order/conflicts/tuning/observer notes for actual changes. |
| Inputs | Changed files and validation results. |
| Likely files | mods/StellarAIDirector/README.md; notes/*.md; research status notes. |
| Exact checks | Docs link exact generated surfaces; stale wording search. |
| Acceptance criteria | Docs accurately distinguish static proof, launch proof, observer proof, and deferred gaps. |
| Dependencies | Any implementation slice |
| Expected artifacts | Updated docs. |

## T28 - Live launcher readiness check

| Field | Contract |
| --- | --- |
| Objective | Verify source changes are reflected in live launcher surfaces without launching Stellaris. |
| Inputs | Local launcher mod folder and dlc_load.json. |
| Likely files | No repo source unless helper docs stale. |
| Exact checks | Check `StellarAIDirector.mod` path and `dlc_load.json`; manage commands status. |
| Acceptance criteria | Live status reported as checked or not checked; no runtime launched. |
| Dependencies | T27 |
| Expected artifacts | Readiness note/status block. |

## T29 - Commit-ready packaging gate

| Field | Contract |
| --- | --- |
| Objective | Stage only coherent Director changes and avoid unrelated packets/noise. |
| Inputs | Git status; dirty-state classification. |
| Likely files | All changed files. |
| Exact checks | git status; git diff --check; validation commands repeated as needed. |
| Acceptance criteria | Commit candidate contains only coherent slice changes, not raw observer artifacts or unrelated research. |
| Dependencies | T27,T28 |
| Expected artifacts | Commit checklist. |

## T30 - Optional observer run preparation

| Field | Contract |
| --- | --- |
| Objective | Prepare but do not run an observer benchmark unless user approves. |
| Inputs | Observer loop runbook; manage_stellaris_commands_at_date.py; validation results. |
| Likely files | observer-run folder only if approved; otherwise plan note. |
| Exact checks | Pre-run status check; settings note; checkpoint plan. |
| Acceptance criteria | Approval recorded before runtime; commands_at_date absent outside active run. |
| Dependencies | T29 |
| Expected artifacts | Observer plan or approved run packet. |

## Dependency Map

```text
T00 -> T01 -> T02/T03/T04/T05
T05/T06 -> T07/T08/T09/T10/T11
T11 -> T12
T05 -> T13/T15/T22/T24
T13 -> T14
T15 -> T16/T17
T18 -> T19
T06 -> T20 -> T21
T22 -> T23
T24 -> T25
T07/T09/T23/T25 -> T26
Any implementation slice -> T27 -> T28 -> T29 -> T30 optional
```

## Commit Granularity Rule

A good commit contains one of:

- one validator/test improvement;
- one source/evidence report;
- one generated behavior slice plus its generator/tests/docs;
- one documentation/readiness cleanup;
- one approved observer evidence packet.

Do not combine direct ship design, personalities, diplomatic actions, and economy tuning in the same commit.
