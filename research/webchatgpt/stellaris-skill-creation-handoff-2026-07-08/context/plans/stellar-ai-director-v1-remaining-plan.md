# Stellar AI Director V1 Remaining Work Plan

Last updated: 2026-07-04

Owner context: Stellaris modding workspace at `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods`.

Primary target: a late-loading local mod named `Stellar AI Director` that
centralizes deterministic AI decision-tree overrides for the active Irony
playset.

This is a living implementation plan. Update it as work is completed, deferred,
or replaced by better evidence.

## Source Of Truth And Current Evidence

This plan is based on:

- Current user request: create a maximum-effort plan for finishing the AI mod
  patch and save it in a dedicated plan directory.
- Existing project rules in `AGENTS.md`.
- Existing generated mod skeleton under `mods/StellarAIDirector/`.
- Existing tools under `tools/`.
- Current validation commands run on 2026-07-04:
  - `python tools\validate_stellar_ai_director_patch.py`
  - `python -m unittest discover -s tools\tests`
- Current Munch gate result:
  - `jcodemunch_guide` works.
  - `jdatamunch_guide` works.
  - `jdocmunch_guide` returns `Transport closed`.
  - `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1` fails because
    duplicate live Munch worker processes are present.

Important limitation: this plan does not claim a fresh JDocMunch-backed corpus
review. JDocMunch must be repaired or remounted before any source-corpus-heavy
implementation or final verification is treated as complete.

## Current Verified State

### Existing Mod Skeleton

`mods/StellarAIDirector/` exists and currently contains:

- `descriptor.mod`
- `README.md`
- `common/ai_budget/zzz_staid_alloys_budget.txt`
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt`
- `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- `common/script_values/zzz_staid_roi_values.txt`

### Existing Required Parents

`mods/StellarAIDirector/descriptor.mod` currently declares dependencies on:

- `Stellar AI`
- `Gigastructural Engineering & More (4.4)`
- `NSC3`
- `Extra Ship Components NEXT`
- `Starbase Extended 3.0`
- `!!!Universal Resource Patch [2.4+]`

These dependency names still need final launcher/Irony verification against the
actual local mod descriptors and loaded playset names.

### Existing Generated Policy Surface

The current generated patch appears to provide:

- State triggers for:
  - core deficit with short runway;
  - survival mode;
  - recovery mode;
  - megastructure prep readiness;
  - megastructure commit safety;
  - pausing new megastructure starts;
  - shipyard payoff readiness;
  - surplus sink pressure;
  - research sink priority readiness;
  - shipyard expansion readiness;
  - unity sink priority readiness.
- A full-object override of Stellar AI's `alloys_expenditure_megastructures`
  budget object.
- Additive subplans inside `basic_economy_plan` for:
  - mega alloy reserve;
  - Gigas special resource reserve;
  - payoff exploitation alloys.
- Numeric script values for generated ROI thresholds and documentation anchors.

### Existing Tools And Tests

Existing tools:

- `tools/build_active_playset_snapshot.py`
- `tools/build_ai_roi_matrix.py`
- `tools/build_mod_snapshot_inventory.py`
- `tools/generate_stellar_ai_director_patch.py`
- `tools/stellar_ai_director_lib.py`
- `tools/validate_stellar_ai_director_patch.py`

Existing tests:

- `tools/tests/test_stellar_ai_director.py`

Current validation result:

- `python tools\validate_stellar_ai_director_patch.py`: passed.
- `python -m unittest discover -s tools\tests`: 36 tests passed.

### What This Means

The project has a real prototype, not just notes. However, it is not yet a
campaign-ready V1 because it only touches a narrow set of AI surfaces. It still
needs a complete source-corpus-backed audit, broader generated policy surfaces,
load-order verification, conflict verification, Stellaris launch validation,
and later observer testing.

## Definition Of A Working V1

V1 is working when all of these are true:

- The mod loads after every required parent mod whose AI, economy,
  megastructure, tech, starbase, or shipyard logic it intentionally overrides.
- The descriptor and README clearly list hard dependencies and tested version
  assumptions.
- Every generated reference to resources, technologies, ascension perks,
  scripted triggers, scripted values, megastructures, starbase modules,
  buildings, ship sizes, components, events, and defines is verified against the
  active playset or vanilla sources.
- The generated PDXScript validates locally and does not reference disabled or
  missing mods.
- Irony shows only intentional conflicts, especially around AI policy surfaces.
- Stellaris reaches the main menu with the patch enabled.
- The first observer smoke test shows at least one AI empire can remain alive,
  pursue a high-ROI economy or shipyard path when eligible, and avoid obvious
  deficit spirals.
- The plan, README, generated artifacts, and validation outputs explain what
  V1 changes and what it intentionally leaves alone.

## V1 Non-Goals

V1 must not try to solve every possible AI weakness.

Out of scope for V1:

- Self-learning, adaptive, or LLM-style runtime behavior.
- Large UI changes.
- New player-facing content unrelated to AI decision weights.
- Full ship design rewrite unless evidence shows NSC3 or ESC AI design weights
  are unusable.
- Exotic Gigas superprojects as mainline choices unless they are explicitly
  proven safe by tests and source inspection.
- Performance-heavy scripted polling events unless no lighter Stellaris AI
  surface can express the needed decision.
- Blindly overriding large parent mod objects without an ownership note and a
  conflict reason.

## Load Order Target

The patch should be placed very late in the Irony mod list.

Required placement rule:

- `Stellar AI Director` loads after:
  - Stellar AI;
  - Gigastructural Engineering & More (4.4);
  - NSC3;
  - Extra Ship Components NEXT;
  - Starbase Extended 3.0;
  - Universal Resource Patch;
  - any compatibility patch that modifies those parents and is meant to be
    upstream of the Director.

Suggested Irony position:

- Near the bottom of the gameplay section.
- After AI, economy, megastructure, technology, ship/component, and starbase
  mods it coordinates.
- Before only those local or compatibility patches that are intentionally meant
  to override the Director.

Validation requirement:

- Use Irony conflict scan to confirm `Stellar AI Director` wins only the
  intended AI policy conflicts.
- Record every intentional winning conflict in the mod README or a dedicated
  conflict note.
- If another late patch must win over the Director, document the exception and
  why it is safe.

## Remaining Work Dashboard

Status values:

- `Done`: completed and verified.
- `Partial`: some implementation exists but is not enough for V1.
- `Needed`: not implemented yet.
- `Gate`: must pass before dependent work is trustworthy.
- `Deferred`: intentionally not part of V1.

| ID | Workstream | Status | V1 Required | Summary |
| --- | --- | --- | --- | --- |
| P0 | Munch/JDocMunch startup gate | Gate | Yes | Active JDocMunch MCP still fails; duplicate workers exist. |
| P1 | Source corpus freshness and indexes | Partial | Yes | Source snapshots exist, but JDocMunch-backed verification is not fresh. |
| P2 | Playset and dependency lock | Partial | Yes | Descriptor dependencies exist; names and load position need Irony verification. |
| P3 | ROI and market model | Partial | Yes | Strong tests exist; coverage must expand beyond current ROI targets. |
| P4 | Decision tree model | Partial | Yes | Offline tests exist; more scenarios and PDX mapping needed. |
| P5 | Generated PDXScript policy surfaces | Partial | Yes | Current patch touches budgets/plans/triggers only. |
| P6 | Tech, AP, tradition, and unlock prioritization | Needed | Yes | Must prioritize unlock chains for required mods. |
| P7 | Megastructure and gigastructure build priorities | Partial | Yes | ROI matrix exists; per-object AI weights still need generated overrides. |
| P8 | Shipyard, fleet throughput, and ship production sinks | Partial | Yes | Strategic shipyard math exists; policy needs in-game surface mapping. |
| P9 | Starbase and defensive economy logic | Needed | Yes | Required by user preference; no generated starbase policy yet. |
| P10 | Planetary/building capacity use | Needed | Should | Required if active mods expand planet capacity. |
| P11 | NSC3/ESC integration | Partial | Yes | V1 currently leaves design weights untouched; tech/use audit needed. |
| P12 | Validator hardening | Partial | Yes | Current validator passes; must cover more PDX surfaces and load-order checks. |
| P13 | Irony conflict and load-order validation | Needed | Yes | No recorded Irony conflict pass yet. |
| P14 | Stellaris launch validation | Needed | Yes | Main-menu launch not recorded. |
| P15 | Observer smoke test | Needed | Yes | Needed before calling campaign-ready. |
| P16 | Documentation and tuning loop | Partial | Yes | README exists; needs conflict notes, tuning knobs, and test log. |

## Phase P0 - Tooling Gate And Shared Munch Direction

Objective: restore reliable tooling before corpus-heavy implementation.

Current defect:

- The active Codex thread still cannot call `jdocmunch_guide`.
- The startup checker reports duplicate `jcodemunch-mcp` and `jdatamunch-mcp`
  processes.
- Current Munch config uses per-client stdio commands, which cannot guarantee a
  single universal tool instance across Codex threads.

Keep unchanged:

- Do not enable JDocMunch embeddings unless explicitly requested.
- Do not treat CLI fallbacks as equivalent to active-thread MCP health.
- Do not launch nested Codex sessions as a normal preflight.

Tasks:

- [ ] Decide the immediate operational path:
  - close/restart Codex to clear duplicate worker processes; or
  - manually terminate orphaned Munch workers only after confirming they are not
    attached to active work; or
  - move directly to a shared service transport if available.
- [ ] Re-run:
  - `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1`
- [ ] Confirm active-thread guide calls:
  - `jdocmunch_guide`
  - `jcodemunch_guide`
  - `jdatamunch_guide`
- [ ] Research whether current Munch MCP packages expose streamable HTTP or SSE
  transport.
- [ ] If they do not, create a separate plan to add a local singleton service
  wrapper or upstream transport support.
- [ ] Record final tooling state in Open Brain.

Acceptance criteria:

- The startup checker passes.
- Active-thread guide calls all return content.
- Future work can use JDocMunch for source/document navigation instead of raw
  full-file reads.
- There is a written next step for singleton service transport if the current
  packages remain stdio-only.

## Phase P1 - Source Corpus Freshness And Index Recovery

Objective: ensure the patch is based on current, indexed sources.

Current defect:

- Source snapshots exist under `research/mod-source-snapshots/2026-07-04/`.
- JDocMunch is not currently available in the active thread for documentation
  and section navigation.
- It is not yet proven that every gameplay-heavy source folder is indexed and
  queryable.

Tasks:

- [ ] Verify snapshot manifest freshness:
  - `research/mod-source-snapshots/2026-07-04/snapshot-manifest.csv`
  - `research/mod-source-snapshots/2026-07-04/descriptor-inventory.csv`
  - `research/mod-source-snapshots/2026-07-04/pdx-object-inventory.csv`
  - `research/mod-source-snapshots/2026-07-04/ai-surface-inventory.csv`
- [ ] Rebuild snapshot inventory from the active Irony playset.
- [ ] Use JDocMunch after P0 to index or verify documentation and text-heavy
  research surfaces.
- [ ] Use JCodeMunch for tools and generated Python code when code navigation is
  needed.
- [ ] Use JDataMunch for CSV matrices instead of manual CSV inspection once the
  relevant datasets are indexed.
- [ ] Create a short corpus status note with:
  - snapshot date;
  - active playset name;
  - required parent mods present;
  - optional gameplay mods detected;
  - files/folders omitted from indexing and why.

Acceptance criteria:

- Every required parent mod source root is present.
- Every required parent descriptor is mapped to a stable local snapshot path.
- Object inventory includes resources, technologies, APs, megastructures,
  starbase modules/buildings, ship sizes, components, scripted triggers,
  scripted values, events, and economic plans.
- Any missing or unparseable source surface is listed with exact examples and a
  follow-up task.

## Phase P2 - Playset And Dependency Lock

Objective: lock the exact playset and dependency contract for V1.

Current defect:

- Descriptor dependencies exist, but the exact launcher/Irony names and load
  ordering still need verification.

Tasks:

- [ ] Read the active Irony selected collection.
- [ ] Confirm all required parent mods are installed and enabled.
- [ ] Verify local descriptor names exactly match `descriptor.mod`
  dependency names.
- [ ] Add missing dependency aliases or correct names if Paradox launcher names
  differ from workshop names.
- [ ] Generate a load-order note under either:
  - `mods/StellarAIDirector/notes/load-order.md`; or
  - `research/stellar-ai/stellar-ai-director-load-order-2026-07-04.md`.
- [ ] Document the intended Irony placement:
  - after required parents;
  - after parent compatibility patches the Director must supersede;
  - before any local patch intentionally overriding the Director.
- [ ] Add a final mod-list entry or import helper only after Irony workflow is
  clear.

Acceptance criteria:

- The mod descriptor has verified dependency names.
- The README names the required load-order position.
- There is an explicit list of upstream mods whose AI behavior the Director
  intentionally coordinates.
- Irony can place the patch where it wins intended conflicts.

## Phase P3 - ROI And Market Model Hardening

Objective: make the ROI model good enough to drive generated priorities.

Current state:

- ROI extraction exists.
- Inline script and variable expansion tests exist.
- Dyson wrapper costs are no longer zero in tests.
- Market-aware conversion tests exist, including alloy base and ceiling price
  behavior and the mineral-to-alloy stress conversion concern.
- Current tests report at least 140 eligible ROI rows.

Remaining defects:

- The ROI model still needs broader coverage beyond current target names.
- Some resources are intentionally unpriced and must be handled as bottleneck
  gates rather than forced into a fake scalar value.
- Strategic utility values need explicit caps and scenario multipliers so a
  shipyard or defense structure is not judged only by income production.

Tasks:

- [ ] Expand ROI extraction coverage for all required parent mods:
  - vanilla megastructures;
  - Gigastructural Engineering megastructures/gigastructures;
  - NSC3 megastructures and shipyard structures;
  - Starbase Extended modules/buildings;
  - relevant ESC resource consumers/unlocks.
- [ ] Separate ROI categories:
  - direct economy producer;
  - bottleneck resource producer;
  - shipyard throughput multiplier;
  - naval cap multiplier;
  - defensive leverage structure;
  - research acceleration;
  - unity/tradition acceleration;
  - prerequisite unlock;
  - exotic/superproject.
- [ ] Preserve unpriced resources as named bottlenecks:
  - do not hide them inside a fake all-purpose value;
  - expose them as required-resource gates;
  - add scarcity and surplus columns.
- [ ] Add scenario-specific valuation columns:
  - base-market cost;
  - deficit-market cost;
  - surplus-liquidation payoff;
  - market-fee-aware cost;
  - resource-bottleneck relief;
  - shipyard throughput value;
  - defensive leverage value;
  - unlock-chain value.
- [ ] Add diminishing return handling:
  - research value before and after very high research income;
  - alloy value when alloy income is negative, adequate, high, or stockpile-capped;
  - energy/mineral/CG value under deficit and surplus;
  - rare resource value when needed by queued construction or ship components.
- [ ] Add per-resource runway columns:
  - `resource_deficit_runway_months`;
  - `stockpile_required_for_safe_commit`;
  - `required_surplus_income_before_start`;
  - `emergency_abort_threshold`.
- [ ] Add tests for specific named structures:
  - Gigas Dyson variants;
  - Matrioshka-style research structures;
  - Neutronium Gigaforge;
  - Nidavellir;
  - HRAE;
  - NSC3 mega shipyard stages;
  - vanilla Mega Shipyard;
  - Starbase Extended high-defense modules;
  - at least one special-resource bottleneck path.

Acceptance criteria:

- No decision-eligible row has zero cost unless the source truly defines no
  cost and the row explains why.
- No decision-eligible row has unresolved cost/upkeep/production without a
  visible `data_quality` reason.
- Every unpriced resource is preserved as a named bottleneck.
- Strategic objects that do not produce income still receive strategy roles.
- ROI rows are stable enough that generated thresholds do not swing wildly from
  parsing noise.

## Phase P4 - Decision Tree Model Hardening

Objective: finish the deterministic logic model before emitting broader script.

Current state:

- Offline `EmpireState` tests exist for survival, recovery, prep, commit,
  payoff exploitation, surplus research/fleet/unity sinks, war interruption,
  lost economy, and shipyard support.

Remaining defects:

- Offline model needs more scenarios.
- Offline model needs clearer mapping to actual Stellaris triggers.
- Emergency exits need deeper coverage for resource-specific collapse.

Tasks:

- [ ] Expand offline state model inputs:
  - at war;
  - war exhaustion;
  - lost war;
  - lost territory/economy fraction;
  - fleet power ratio if available;
  - used naval capacity;
  - fleet upkeep pressure;
  - starbase choke coverage;
  - alloy/energy/mineral/CG/food/special-resource income;
  - stockpile runway by resource;
  - active megastructure progress;
  - construction capacity;
  - research sink availability;
  - fleet sink availability;
  - unity sink availability;
  - personality posture.
- [ ] Define deterministic states:
  - `survival_mode`;
  - `recovery_mode`;
  - `normal_growth_mode`;
  - `investment_prep_mode`;
  - `investment_commit_mode`;
  - `payoff_exploitation_mode`;
  - `research_expansion_mode`;
  - `shipyard_expansion_mode`;
  - `unity_expansion_mode`;
  - `defensive_fortification_mode`;
  - `superproject_mode` gated or disabled for V1.
- [ ] Add escape hatch tests:
  - war starts during prep with weak fleet;
  - war starts near completion with safe runway;
  - half economy lost during commit;
  - energy deficit from fleet upkeep;
  - rare resource deficit from advanced components;
  - alloy stockpile capped with insufficient shipyard capacity;
  - massive energy surplus but alloy bottleneck;
  - defensive personality at chokepoint;
  - aggressive personality with sustainable fleet budget;
  - crisis or rival pressure forcing defense before long-payoff projects.
- [ ] Define exact state precedence:
  - survival always wins;
  - recovery beats new investment;
  - near-complete commit can continue only with safe runway;
  - payoff exploitation only after the relevant completed project exists;
  - surplus sinks only after economy safety gates pass.
- [ ] Document personality modifiers:
  - defensive empires prefer chokepoint starbases and lower idle fleet upkeep;
  - aggressive empires tolerate higher fleet spending if income supports it;
  - research-focused empires prioritize research sinks earlier;
  - isolationist/tall empires bias toward defensive and megastructure paths.

Acceptance criteria:

- Offline tests cover all state transitions and negative paths.
- Every PDXScript trigger has a corresponding offline model concept or a
  documented engine-only reason.
- The decision tree cannot choose new long-payoff investment during short
  resource runway survival cases.
- The decision tree can choose high-ROI investment when a stable empire is
  strong enough to survive the upfront cost.

## Phase P5 - Generated PDXScript Policy Surfaces

Objective: expand from prototype triggers/budget/plans to a coherent generated
patch.

Current state:

- Current generated PDX surfaces are narrow and mostly additive, except one
  intentional budget override.

Remaining defects:

- The patch does not yet centralize all relevant AI modifications.
- It does not yet emit tech/AP/tradition/starbase/megastructure priority
  overrides.
- It does not yet provide enough in-game weight surfaces to force the desired
  strategic behavior.

Tasks:

- [ ] Inventory all relevant AI-bearing PDX object types in required parents:
  - `common/ai_budget`;
  - `common/economic_plans`;
  - `common/megastructures`;
  - `common/technology`;
  - `common/ascension_perks`;
  - `common/traditions`;
  - `common/starbase_modules`;
  - `common/starbase_buildings`;
  - `common/buildings`;
  - `common/ship_sizes`;
  - `common/component_templates`;
  - scripted triggers/effects/values used by those objects.
- [ ] Categorize each target as:
  - additive new object;
  - full-object override;
  - no safe direct override;
  - defer to parent mod;
  - needs compatibility patch.
- [ ] For every full-object override:
  - add an ownership comment;
  - list parent source path;
  - list exact reason for override;
  - verify no unrelated behavior was dropped.
- [ ] Generate focused files by responsibility:
  - `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`;
  - `common/script_values/zzz_staid_roi_values.txt`;
  - `common/ai_budget/zzz_staid_alloys_budget.txt`;
  - `common/economic_plans/zzzz_staid_additive_economic_plan.txt`;
  - new tech weight file if safe;
  - new megastructure override file if required;
  - new starbase policy file if required;
  - new AP/tradition weight file if required.
- [ ] Avoid dumping every override into one giant file.
- [ ] Keep generated comments concise but enough for conflict review.

Acceptance criteria:

- Generated files are small enough to review by surface.
- Every generated reference is validated.
- Every broad override has an ownership note.
- No generated file references optional mods unless the generator proves they
  exist or guards them safely.

## Phase P6 - Technology, Ascension Perk, Tradition, And Unlock Priorities

Objective: make the AI actually unlock the paths needed for late-game power.

Current defect:

- Current prototype does not emit direct technology/AP/tradition prioritization.
- The AI may build a stronger economy but still fail to research or select the
  unlocks that make Gigas/NSC3/ESC scaling possible.

Tasks:

- [ ] Inventory all required unlock tech chains:
  - vanilla megastructure chain;
  - Gigas megastructure/gigastructure unlocks;
  - Gigas special resource unlocks;
  - NSC3 ship size and shipyard unlocks;
  - ESC advanced weapons/reactors/shields/armor/resource unlocks;
  - Starbase Extended defense unlocks.
- [ ] Identify AI weight surfaces for technologies.
- [ ] Add priority bands:
  - survival economy tech;
  - research economy tech;
  - mega-engineering prerequisites;
  - first high-ROI economy multiplier;
  - shipyard/fleet throughput;
  - advanced military component unlocks;
  - defensive starbase unlocks;
  - repeatables after core modded unlocks.
- [ ] Inventory ascension perks that unlock mega/giga progression.
- [ ] Add AP strategy:
  - prioritize required mega/giga APs when economy and tech prerequisites are
    ready;
  - avoid taking dead-end APs that block key build paths;
  - allow personality-specific variation only after core unlock path remains
    viable.
- [ ] Inventory tradition mods if active playset expands tradition count/options.
- [ ] Add tradition strategy only if active mods require it for the core loop.
- [ ] Add validation that every referenced tech/AP/tradition exists.

Acceptance criteria:

- AI can reach modded construction prerequisites, not only vanilla endgame.
- Research-heavy Stellar AI behavior is preserved but extended into modded
  unlocks.
- No tech/AP/tradition reference is emitted without validation.

## Phase P7 - Megastructure And Gigastructure Build Priority Overrides

Objective: convert ROI analysis into actual AI build priorities.

Current defect:

- ROI analysis identifies candidates, but generated PDX does not yet clearly
  alter individual megastructure/gigastructure build weights.

Tasks:

- [ ] For each decision-eligible structure, classify:
  - buildable by normal empire;
  - requires special origin/civic/path;
  - requires unique resource;
  - requires site/star/body type;
  - one-per-empire or limited count;
  - dangerous or exotic.
- [ ] Build priority tiers:
  - first economy multiplier;
  - first research multiplier;
  - special resource bottleneck;
  - shipyard throughput;
  - defensive leverage;
  - second bottleneck project;
  - optional/superproject.
- [ ] Add site-selection logic where the same structure has variants:
  - Dyson star variants;
  - Matrioshka star variants;
  - other Gigas wrapper variants.
- [ ] Generate AI weights with gates:
  - do not start if survival/recovery;
  - prefer high ROI when prep-ready;
  - continue near-complete projects when runway is safe;
  - pause new projects under war/fleet emergency;
  - bias to bottleneck relief based on resource deficits.
- [ ] Keep superprojects disabled or heavily gated:
  - require overwhelming economy;
  - require safe fleet/defense;
  - require completed core loop;
  - require no critical deficits.

Acceptance criteria:

- The AI can select a first high-ROI economy megastructure.
- The AI can prefer better star/body variants when multiple options exist.
- Shipyard megastructures are valued as throughput sinks, not income producers.
- Exotic projects do not derail normal AI survival.

## Phase P8 - Shipyard, Fleet Throughput, And Surplus Sink Logic

Objective: let AI convert huge economy into military power without collapse.

Current state:

- ROI tests include strategic shipyard throughput for NSC3 mega shipyard stages.
- Decision tests include surplus fleet sink behavior.

Remaining defects:

- In-game PDX mapping for shipyard/fleet expansion is not complete.
- The AI must avoid building a massive shipyard before it has economy to use it.

Tasks:

- [ ] Define shipyard expansion prerequisites:
  - alloy income high enough;
  - energy income high enough;
  - stockpile near cap or unable to spend alloys;
  - fleet buildup desired;
  - current shipyard capacity inadequate or strategic war plan requires burst
    production.
- [ ] Define when shipyard expansion is bad:
  - low alloy income;
  - negative energy runway;
  - fleet upkeep already causing collapse;
  - no strategic need and better research sink exists.
- [ ] Map shipyard strategy to actual AI surfaces:
  - megastructure AI weight;
  - starbase shipyard modules if relevant;
  - naval cap budget;
  - fleet build budget;
  - economy plans for alloys/energy/special resources.
- [ ] Add tests:
  - alloy stockpile capped -> shipyard/fleet sink;
  - high economy but no tech -> prioritize unlock;
  - shipyard completed but alloy income too low -> recovery/economy first;
  - shipyard completed and economy strong -> fleet payoff exploitation.
- [ ] Decide whether NSC3/ESC ship design weights need V1 overrides:
  - audit first;
  - leave untouched if parent AI weights are adequate;
  - override only if evidence shows AI cannot use bigger ships/components.

Acceptance criteria:

- Mega Shipyard and NSC3 shipyard structures get strategic weight when the AI
  has excess economy.
- The AI does not overbuild ships into an energy/alloy upkeep death spiral.
- Research remains the first surplus sink when relevant unlocks are still
  available.

## Phase P9 - Starbase And Defensive Economy Logic

Objective: make defensive empires use static defenses and chokepoints better.

Current defect:

- No generated starbase policy exists yet.

Tasks:

- [ ] Inventory Starbase Extended modules/buildings and defensive modifiers.
- [ ] Inventory vanilla starbase defensive AI weights.
- [ ] Identify choke/defense triggers Stellaris exposes to AI weights.
- [ ] Define defensive strategy:
  - chokepoint starbases reduce required idle fleet spending;
  - defensive personalities bias toward starbases before oversized idle fleets;
  - aggressive empires still prefer fleet if they can use it offensively;
  - crisis/rival pressure increases defense priority.
- [ ] Add starbase ROI categories:
  - defensive leverage;
  - naval cap support;
  - shipyard support;
  - trade/economy support;
  - special module support.
- [ ] Generate starbase weights only where source supports safe overrides.
- [ ] Add tests:
  - defensive empire with choke and safe economy chooses starbase investment;
  - defensive empire with deficit does not overbuild;
  - aggressive empire with strong economy still prioritizes fleet expansion;
  - crisis pressure increases defensive priority.

Acceptance criteria:

- Defensive empires get a clearer static-defense path.
- Starbase investment does not replace survival/recovery gates.
- The plan records which starbase surfaces could not be safely controlled.

## Phase P10 - Planetary And Building Capacity Logic

Objective: ensure AI uses expanded planet capacity if active mods add it.

Current defect:

- No generated planet/building policy exists yet.
- It is not yet proven whether the active playset expands building slots,
  districts, planet classes, or special planet infrastructure in a way the AI
  ignores.

Tasks:

- [ ] Inventory active mods that change:
  - building slots;
  - districts;
  - planet classes;
  - special deposits;
  - jobs;
  - automation plans;
  - economic plans.
- [ ] Determine whether Stellar AI already covers those surfaces.
- [ ] Add economy-plan targets only for high-impact missing resource paths.
- [ ] Avoid broad planet automation rewrites in V1 unless evidence shows a major
  gap.
- [ ] Add tests or validation rows for any generated building/job references.

Acceptance criteria:

- V1 either covers expanded planet capacity or explicitly documents why the
  active playset does not need extra planet logic.
- No generated building/job reference is unverified.

## Phase P11 - NSC3 And ESC Integration

Objective: ensure AI can use bigger ships and stronger components without a
large risky ship-design rewrite.

Current state:

- V1 README says NSC3 and ESC ship/component design weights are left untouched.

Remaining defect:

- It is not yet proven that leaving them untouched is enough.

Tasks:

- [ ] Inventory NSC3 AI surfaces:
  - ship sizes;
  - section templates;
  - shipyards;
  - naval cap effects;
  - technologies;
  - AI weights.
- [ ] Inventory ESC AI surfaces:
  - component templates;
  - strategic resource requirements;
  - technologies;
  - AI weights.
- [ ] Determine the minimum V1 intervention:
  - tech unlock prioritization only;
  - resource economy support;
  - shipyard throughput support;
  - direct ship/component weights if required.
- [ ] Add special-resource gates so AI does not research/build components it
  cannot sustain.
- [ ] Add tests for referenced NSC3/ESC IDs.
- [ ] Document any parent AI weights deliberately preserved.

Acceptance criteria:

- AI is more likely to unlock NSC3/ESC power paths.
- AI has economy support for components that consume advanced resources.
- Direct ship/component overrides are either implemented with evidence or
  explicitly deferred with reasons.

## Phase P12 - Validator Hardening

Objective: make invalid generated patches fail before Stellaris launch.

Current state:

- `validate_generated_patch()` exists and passes.

Remaining defects:

- Validator must cover every new surface added after the prototype.
- It must detect broad override risk and missing load-order assumptions.

Tasks:

- [ ] Add validation categories:
  - required parent mod present;
  - descriptor dependency name matches local descriptor;
  - generated file path is valid for Stellaris;
  - generated object references exist;
  - scripted trigger references exist;
  - scripted value references exist;
  - resource references exist;
  - technology references exist;
  - AP/tradition references exist;
  - megastructure references exist;
  - starbase module/building references exist;
  - ship size/component references exist;
  - event references exist if used;
  - optional references are guarded or omitted;
  - no broad override without ownership note.
- [ ] Add syntax-level checks:
  - parser can parse generated PDX;
  - braces are balanced;
  - no accidental unresolved template placeholders;
  - no disabled-mod references.
- [ ] Add data-quality checks:
  - no decision-eligible zero-cost rows unless explained;
  - no unresolved decision-eligible rows;
  - all generated thresholds come from eligible rows;
  - market price inputs are present.
- [ ] Add load-order checks:
  - Director dependencies present;
  - Director should be after required parents;
  - conflict owner list generated.

Acceptance criteria:

- A missing tech/resource/megastructure ID fails validation.
- An unguarded optional mod reference fails validation.
- A full-object override without ownership note fails validation.
- The validator is the main pre-launch gate before Irony/Stellaris.

## Phase P13 - Irony Conflict And Load-Order Validation

Objective: prove the patch wins only intended conflicts.

Tasks:

- [ ] Install or expose `mods/StellarAIDirector` to the Paradox launcher local
  mod folder if not already visible.
- [ ] Add the mod to the active Irony playset.
- [ ] Move it near the bottom after required parent mods.
- [ ] Run Irony conflict scan.
- [ ] Export or record conflict results.
- [ ] Classify conflicts:
  - intentional Director wins;
  - parent wins required;
  - harmless duplicate/additive;
  - unexpected conflict requiring code change;
  - false positive or cosmetic only.
- [ ] Update README/conflict notes with intentional conflicts.
- [ ] Re-run generated validation after any conflict-driven change.

Acceptance criteria:

- Irony conflict scan has no unexplained AI/gameplay conflicts.
- Load-order position is documented.
- The patch descriptor and README match the actual playset.

## Phase P14 - Stellaris Launch Validation

Objective: prove the generated patch loads into the game.

Tasks:

- [ ] Launch Stellaris with only required parent mods plus Director if practical.
- [ ] Launch with the full active playset plus Director.
- [ ] Reach main menu.
- [ ] Inspect:
  - `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log`
  - `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\game.log`
- [ ] Record:
  - game version;
  - DLC state if known;
  - playset name;
  - mod order date;
  - errors/warnings relevant to Director files.
- [ ] Fix any missing reference, syntax, or load-order errors.

Acceptance criteria:

- Main menu loads.
- No Director-caused fatal errors.
- No missing generated object references in logs.
- Known unrelated warnings are documented separately.

## Phase P15 - Observer Smoke Test

Objective: verify the decision tree does something useful in a running game.

Tasks:

- [ ] Create a repeatable observer test setup:
  - galaxy size;
  - AI count;
  - difficulty;
  - crisis settings;
  - mod list hash or exported order;
  - test duration checkpoints.
- [ ] Add logging or manual tracking for:
  - AI economy growth;
  - first mega-engineering unlocks;
  - first high-ROI megastructure starts;
  - completion of first economy multiplier;
  - shipyard/fleet payoff behavior;
  - deficit spirals;
  - war interruptions;
  - starbase defense investment.
- [ ] Run first short observer test:
  - early to midgame checkpoint;
  - verify no immediate AI self-sabotage.
- [ ] Run first long observer test:
  - into late game;
  - verify at least one AI starts/completes/exploits a high-ROI path.
- [ ] Record outcomes in `mods/StellarAIDirector/notes/observer-test-log.md`.

Acceptance criteria:

- At least one AI empire reaches a modded high-ROI path.
- AI does not broadly collapse from Director-induced overspending.
- If behavior is wrong, tuning changes are recorded against exact observed
  symptoms.

## Phase P16 - Documentation, Tuning, And Maintenance Loop

Objective: make the mod easy to update after real gameplay feedback.

Tasks:

- [ ] Update `mods/StellarAIDirector/README.md` with:
  - exact hard dependencies;
  - load-order position;
  - validation commands;
  - intentional override list;
  - known limitations;
  - tuning workflow.
- [ ] Add `mods/StellarAIDirector/notes/` if it does not exist.
- [ ] Add notes:
  - `load-order.md`;
  - `conflicts.md`;
  - `observer-test-log.md`;
  - `tuning-notes.md`.
- [ ] Add a generated tuning report from ROI/decision outputs.
- [ ] Keep CSVs as analysis inputs, not runtime files:
  - document which CSV columns feed generation;
  - document which values are hand-tunable;
  - document how to regenerate after changing weights.
- [ ] Add tuning knobs to the generator:
  - prep stockpile multiplier;
  - commit reserve multiplier;
  - deficit runway months;
  - shipyard surplus threshold;
  - research/fleet/unity sink ordering;
  - defensive starbase personality multiplier;
  - superproject gate.
- [ ] Add tests that fail when tuning knobs produce unsafe thresholds.

Acceptance criteria:

- A future agent can change weights without reading the whole chat history.
- A player feedback note can be translated into a small generator/config change.
- Generated files remain reproducible from tools and source snapshots.

## Implementation Slice Order

Use this order unless a later discovery proves it wrong:

1. P0: Repair Munch gate enough for source-corpus work.
2. P1: Refresh source snapshots and indexes.
3. P2: Verify playset dependencies and load-order names.
4. P12: Harden validator before adding more generated surfaces.
5. P3: Expand ROI/data model coverage.
6. P4: Expand offline decision-tree scenarios.
7. P6: Add tech/AP/tradition unlock strategy.
8. P7: Add megastructure/gigastructure priority generation.
9. P8: Add shipyard/fleet throughput policy.
10. P9: Add starbase defensive policy.
11. P11: Audit NSC3/ESC and add only required minimal overrides.
12. P10: Add planet/building capacity policy only if active mods require it.
13. P13: Irony conflict validation.
14. P14: Stellaris main-menu validation.
15. P15: Observer smoke tests.
16. P16: Documentation and tuning loop.

## Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| JDocMunch remains unavailable in active threads | Source review becomes slow and error-prone | Treat P0 as first gate; do not claim corpus-complete verification without it. |
| Duplicate Munch workers hide stale handles | Agents believe tools work when active thread is broken | Startup checker fails on duplicates; move toward singleton service. |
| Wrong descriptor dependency names | Launcher does not enforce parent order | Verify names against local descriptors and Irony. |
| Full-object override drops parent behavior | Breaks parent mod AI or compatibility | Ownership notes, source diff review, validator rule. |
| Stellaris trigger/effect assumptions are wrong | Script loads with errors or silently fails | Verify against vanilla/current mod sources, CWTools, and logs. |
| ROI scalar hides resource scarcity | AI chooses bad projects during bottlenecks | Preserve per-resource columns and bottleneck gates. |
| Shipyard treated as income producer | AI undervalues throughput sink | Keep strategic shipyard valuation separate from income ROI. |
| AI overbuilds fleet after payoff | Energy/alloy upkeep death spiral | Add fleet upkeep and runway escape hatches. |
| Research sink over-prioritized forever | AI delays fleet/defense despite danger | State precedence and threat gates. |
| Starbase defense over-prioritized | Passive empires waste resources on static defense | Personality/threat/choke gates and negative tests. |
| Exotic Gigas projects destabilize AI | AI burns economy on unsafe superprojects | Disable or heavily gate superproject mode in V1. |
| Irony conflict scan reveals broad conflicts | Patch cannot safely load late as planned | Split overrides or defer unsafe surfaces. |
| Main-menu logs show missing IDs | Patch not ready for play | Validator expansion and log-driven fixes. |

## Exact Validation Commands

Run from `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods`.

Tooling gate:

```powershell
& 'C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1'
```

Generator:

```powershell
python tools\generate_stellar_ai_director_patch.py
```

Patch validator:

```powershell
python tools\validate_stellar_ai_director_patch.py
```

Unit tests:

```powershell
python -m unittest discover -s tools\tests
```

Optional syntax and hygiene:

```powershell
git diff --check
```

Manual validation:

- Irony conflict scan.
- Stellaris main-menu launch.
- `error.log` and `game.log` review.
- Observer smoke test.

## Completion Checklist For V1

- [ ] P0 Munch gate passes.
- [ ] P1 source corpus/index status is current.
- [ ] P2 dependency names and load order are verified.
- [ ] P3 ROI matrix covers required parent surfaces.
- [ ] P4 decision tree tests cover emergency exits and surplus sinks.
- [ ] P5 generated PDX surfaces are expanded and documented.
- [ ] P6 tech/AP/tradition unlocks are prioritized or explicitly deferred.
- [ ] P7 megastructure/gigastructure weights are generated and validated.
- [ ] P8 shipyard/fleet throughput logic is generated and validated.
- [ ] P9 starbase defense logic is generated or explicitly deferred with reason.
- [ ] P10 planet/building expansion logic is covered or ruled out.
- [ ] P11 NSC3/ESC integration is audited and minimally patched if needed.
- [ ] P12 validator catches missing references and unsafe overrides.
- [ ] P13 Irony conflict scan is reviewed and documented.
- [ ] P14 Stellaris reaches main menu with the patch enabled.
- [ ] P15 observer smoke test confirms at least one useful high-ROI AI path.
- [ ] P16 README/notes/tuning docs are current.

## Current Best Estimate

Assuming P0 tooling is restored first:

- Minimal V1 that loads and has broader generated priorities: 4 to 8 focused
  hours.
- V1 with Irony conflict validation and main-menu launch: about 1 focused day.
- V1 that is trustworthy for a real campaign: 1 to 2 focused days plus observer
  test time.
- Tuned behavior that consistently challenges the player in late game: iterative
  work over multiple observer/play sessions.

The largest unknown is not writing files. The largest unknown is mapping the
right Stellaris AI surfaces without accidentally overriding too much parent mod
behavior.
