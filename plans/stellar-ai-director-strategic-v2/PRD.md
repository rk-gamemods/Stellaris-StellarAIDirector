# Stellar AI Director V2 PRD

Generated: 2026-07-08
Packet: Stellar AI Director Strategic V2 Roadmap Packet
Target: Stellaris PC 4.4.5 stable/current, backwards compatible with 4.4.4 where source-backed


## Source Frame

This packet is built from the uploaded project context bundle and is intended for Codex to use inside the local repository. It does not implement mod code. It turns the current evidence into a strategic execution contract.

Primary local sources used:

- `02_PROJECT_CONTROL_AND_GUIDANCE.md` for source order, 4.4.5 default target, validation posture, runtime approval gates, user preferences, and final status reporting rules.
- `03_MOD_SOURCE_AND_DESCRIPTORS.md` for the current `mods/StellarAIDirector` source shape, README, descriptor, load-order notes, and generated script surfaces.
- `04_STELLAR_AI_DIRECTOR_CONTEXT.md` for current Stellar AI Director behavior, standalone parity status, open roadmap, 4.4.5 compatibility triage, research-scaling diagnosis, and deferred gaps.
- `05_RESEARCH_AND_EVIDENCE_GUIDES.md` for modding-source order, playset/collection context, and current 4.4.x research guidance.
- `06_DATASETS_AND_VALIDATION_REPORTS.md` for dataset/report inventory, generated audits, observer summaries, and compatibility evidence catalogs.
- `07_TOOLS_AND_VALIDATORS.md` for generator, atlas, validation, observer, launcher, and test command surfaces.
- `08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md` for manifest coverage, large-artifact omissions, and dataset catalog boundaries.

External source used only for current-version framing:

- Official Steam Community Stellaris announcement for the 4.4.5 Pegasus patch being live on Steam/GOG/MS Store. Codex should still prefer the local installed vanilla files and local runtime logs when implementing.

Assumption labels used here:

- **Proven local evidence**: directly stated in the uploaded bundle or current generated artifacts.
- **Static inference**: a reasoned conclusion from local evidence, but not runtime proof.
- **Research question**: requires Codex inspection of local vanilla/mod files, Munch datasets, CWTools, Irony, logs, or approved runtime evidence.
- **User decision**: requires the user's preference or approval.

## Product Thesis

Stellar AI Director V2 should become a **standalone, mod-set-aware AI execution layer**, not another broad bundle of AI-weight boosts.

The next phase must make AI empires more competitive in the user's high-scale 4.4.x playset by turning local evidence into safe, generated policy: stronger early compounding economy, research scaling, fleet-to-payoff behavior, crisis/defense readiness, and explicit compatibility with Gigastructural Engineering, NSC3, Extra Ship Components NEXT, Starbase Extended, UI Overhaul Dynamic, Universal Resource Patch, Planetary Diversity, and selected AI/performance mods.

The strategic shift is:

```text
V1 posture: static-safe standalone parity and broad route pressure.
V2 posture: evidence-gated compounding behavior with measurable outcomes and risk-ranked override lanes.
```

## Current Situation

### Proven local evidence

- Stellar AI Director is now described as a deterministic standalone AI replacement baseline and no longer declares or requires Stellar AI at launch. Stellar AI remains a private parity reference only.
- Required compatibility parents currently include Gigastructural Engineering & More (4.4), NSC3, Extra Ship Components NEXT, Starbase Extended 3.0, and Universal Resource Patch.
- Existing Director surfaces already cover AI budgets, economic plans, research/economy/fleet conversion, construction pressure, market/runway safety, Gigas resource reserves, high-scale progression hooks, fleet-throughput, starbase/static-defense pressure, Planetary Diversity targeted support, and a bounded V1 threat-response layer.
- Explicit deferred gaps remain: broad personality rewrites, diplomatic action overrides, direct NSC3/ESC ship-design/component/section handling, advanced war-chain behavior, advanced Gigas continuation proof, broad colony/designation rewrites, and current post-standalone runtime observer proof.
- The project target is now Stellaris PC 4.4.5 stable/current. Local 4.4.4 notes and observer evidence are historical unless revalidated.

### Static inference

The next major value is not adding isolated weights. The next value is forcing a clean execution sequence:

1. Prove the current 4.4.5 standalone baseline is generator-clean and launcher-clean.
2. Build richer static evidence and validators so Codex cannot drift into invented or unsafe surfaces.
3. Improve first-75-year economic compounding, because late megastructure weights do not matter if the AI misses research, pop growth, CG/energy support, and early route selection.
4. Make fleet investment conditional on payoff: survival, defended economy, territory, pops, subjects, or crisis preparation.
5. Research risky surfaces before implementation: diplomatic actions, personalities, direct ship designs, component templates, section templates, ship sizes, and broad Gigas rewrites.
6. Only after static gates pass, optionally run observer tests with explicit user approval.

## User-Facing Gameplay Goals

| Goal | Desired player-visible outcome | Confidence |
| --- | --- | --- |
| Stronger AI economy | AI empires should fill useful jobs, avoid resource cap waste, keep CG/energy/research inputs stable, and spend minerals/alloys into compounding infrastructure rather than idling. | High for static plan; runtime impact requires observer proof. |
| Better research scaling | Competitive AI empires should pursue labs, research districts, research policies/edicts, Mega Engineering, Mega Shipyard, NSC hulls, ESC component techs, Gigas unlocks, and research diplomacy more coherently. | High for static levers; runtime magnitude uncertain. |
| Better high-scale progression | AI should not stall before Gigas/NSC3/ESC payoff chains because of missing prerequisite, reserve, or special-resource planning. | Medium-high; queue continuation needs runtime/save evidence. |
| Better fleet payoff | Militarist/conquest AI should convert fleet into territory, pops, subjects, raiding, or survival rather than sitting on fleet power without economic return. Non-militarists should not overbuild fleets at the expense of research. | Medium; war-chain surfaces are risky. |
| Better defense and crisis readiness | AI should invest in starbases, defenses, shipyards, reserves, and fleet production when threat/crisis posture justifies it. | Medium; crisis-response triggers need evidence. |
| Major-mod compatibility | Director should coordinate with Gigastructural Engineering, NSC3, ESC NEXT, Starbase Extended, UIOD, Universal Resource Patch, Planetary Diversity, and major AI/performance mods without guessing loader behavior. | High for research contracts; implementation varies by surface. |
| Standalone independence | Director should remain usable without Stellar AI as a launcher dependency, while preserving source provenance for parity decisions. | High. |

## Runtime Outcome Targets If Observer Runs Are Later Approved

These are **tuning targets**, not unit-test gates. Do not encode them as brittle automated tests.

| Checkpoint | Target signal | Why it matters |
| --- | --- | --- |
| 2250 | No broad deficit spiral; useful early labs/assembly/construction visible; no mass unstaffed researcher jobs. | Proves the opening did not overbuild or starve support resources. |
| 2270-2280 | Leading regular AI approaches roughly 1,000 monthly research in the high-scale playset, subject to settings and no hidden bonuses. | Existing planning identifies lower trajectories as failed for 25x crisis goals. |
| 2300 | Leading AI has clear tech/economy/fleet specialization and is not blocked from Mega Engineering/Mega Shipyard/Gigas/NSC/ESC routes. | Shows compounding route selection is happening early enough. |
| 2325 | AI has either scalable economy megastructure progress, strong conquest payoff, or a documented blocker. | Identifies whether V2 is moving beyond V1 route pressure. |
| 2350 | Leading AI aims for 5,000-6,000+ monthly research and crisis-relevant fleet/economy slope without hidden bonuses. | Target posture for 25x crisis relevance. |

## Non-Goals

- Do not implement code in this planning packet.
- Do not launch Stellaris or run observer games without explicit approval.
- Do not treat old 4.4.4 observer evidence as current 4.4.5 standalone proof.
- Do not add direct `common/diplomatic_actions`, `common/personalities`, ship designs, component templates, section templates, or ship-size overrides without source-backed gate completion.
- Do not invent Stellaris triggers, effects, modifiers, scopes, folder names, or loader behavior.
- Do not solve bad AI by hidden economic bonuses unless the user explicitly approves a separate balance mode.
- Do not recommend Real Space or Star Wars total conversions by default.
- Do not treat generated CSVs as fully inspected row-by-row unless Codex actually uses JDataMunch/JDocMunch/JCodeMunch to inspect them.

## Priority Requirements

### P0 - Baseline Integrity And Evidence Hardening

| Requirement | Contract | Acceptance |
| --- | --- | --- |
| 4.4.5 current frame | Treat 4.4.5 stable/current as the implementation target, preserve 4.4.4 compatibility where feasible, and isolate 4.5 as a future porting branch. | Docs, descriptor, generated reports, and validation notes no longer call 4.4.5 beta or current work 4.4.4-only. |
| Standalone baseline | Preserve no Stellar AI launch dependency. | Descriptor omits Stellar AI; current docs state private parity reference only; stale wording search is clean or archived. |
| Static validation first | All implementation slices pass generator, validator, unit, py_compile, git diff, file/reference/conflict audit gates before runtime. | Codex reports exact commands and results. |
| Evidence hierarchy | Codex must use current user instruction, repo guidance, local vanilla, current mod source, bundle evidence, Irony/CWTools/logs, then inference. | Every task card includes required input artifacts and stop conditions. |
| Risk gate for unsafe surfaces | Diplomatic actions, personalities, ship templates, component templates, section templates, ship sizes, broad Gigas rewrites, and runtime observer proof require research gates. | No generated unsafe folders unless a task explicitly completes source-backed proof. |

### P1 - Compounding Economy And Research V2

| Requirement | Contract | Acceptance |
| --- | --- | --- |
| Opening route classifier refinement | Preserve/refine computed strategic-state route triggers for research, unity-to-research, military-to-pops, defensive tall, trade-to-research, hive growth, and machine growth. | Generated triggers parse; reused consistently in economic plans, policies, edicts, tech, AP/traditions, and construction pressure. |
| Capital/research-world pressure | Push at least one early high-pop world toward research when support economy is safe; avoid unsupported lab spam. | Generated building/district weights have CG/energy/mineral gates; validators check no unsafe support-resource omission. |
| Pop growth/assembly | Promote pop assembly/growth buildings from passive/under-prioritized evidence into safe active pressure by empire type where local surfaces allow. | Source-backed object list; invalid empire-type combinations rejected in tests. |
| Support economy bridge | Keep CG, energy, minerals, food, trade capacity, and strategic resources distinct bottlenecks. | No generic commodity flattening for trade/special resources; economic-plan subplans include safety gates. |
| Unity-to-research | Weight traditions/APs that convert into research tempo, not generic unity hoarding. | Discovery/Diplomacy/Mercantile/ascension choices documented with route rationale and source IDs. |

### P2 - Modded Progression, Fleet Payoff, Defense, War

| Requirement | Contract | Acceptance |
| --- | --- | --- |
| Gigas route mastery | Preserve route weights/reserves while adding queue-continuation research and blocker reporting before broad rewrites. | Static route report plus optional save/observer queue report before claiming optimization. |
| NSC3/ESC readiness | Continue current safe path through tech/resource/fleet-throughput until direct design/component handling is source-proven. | No direct ship-design/component-template/section-template output until source-verified lane report passes. |
| Starbase/defense | Expand AI use of starbases and static defenses only where Starbase Extended and vanilla scopes are verified. | Starbase modules/buildings parse; Irony conflicts classified; no guessed folders/scopes. |
| Fleet payoff | Tie fleet investment to survival, crisis readiness, conquest, raiding, subject formation, or secured economy. | Militarist/conquest routes include payoff gates and observer metrics, not only fleet-power growth. |
| War behavior | Keep V1 threat-response safe; design advanced war-chain as a separate evidence-gated phase. | No forced wars/CBs/diplomatic overrides in V2 core. |

### P3 - Optional Observer And Release Packaging

| Requirement | Contract | Acceptance |
| --- | --- | --- |
| Observer approval gate | Runtime observer runs require explicit user approval and pre/post observer-command status checks. | `commands_at_date.txt` absent before/after outside active run; setup documented. |
| Release readiness | Live launcher readiness, commit readiness, and push readiness are separate surfaces. | Codex reports live mod, commit, and push status explicitly. |
| User-facing docs | README/load-order/tuning/conflicts reflect current state and known risks. | No stale claims, no hidden runtime proof claims, no dependency confusion. |

## Definition Of V2 Strategic Success

V2 is strategically ready when Codex can show all of the following without runtime claims:

1. Current 4.4.5 standalone baseline is clean by static validation.
2. Evidence map and route contracts explain every major generated surface.
3. Early economy/research compounding has a source-backed implementation path.
4. High-risk surfaces are gated, not hand-waved.
5. Compatibility slices are prioritized by expected impact and risk.
6. Optional observer testing has a clear approval-gated runbook and metrics.
7. Codex can implement each task card independently and know exactly when to stop.
