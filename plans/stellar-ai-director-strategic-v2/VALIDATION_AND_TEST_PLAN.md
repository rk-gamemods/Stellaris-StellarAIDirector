# Stellar AI Director V2 Validation And Test Plan

Generated: 2026-07-08
Packet: Stellar AI Director Strategic V2 Roadmap Packet
Target: Stellaris PC 4.4.5 stable/current, backwards compatible with 4.4.4 where source-backed


## Validation Philosophy

Default validation is static. Runtime observer validation is optional and requires explicit user approval.

Static validation should prove:

- generated files are syntactically and structurally safe;
- references resolve to vanilla, parent-mod, or generated objects;
- unsafe surfaces are gated;
- generated objects have source/provenance comments;
- compatibility assumptions are documented;
- live launcher readiness is separate from source readiness.

Static validation should not pretend to prove:

- AI will beat a 25x crisis;
- observer outcomes;
- war behavior quality;
- megastructure queue continuation;
- save/load runtime behavior.

## Existing Validation Commands

Run these before any commit-ready claim after generator changes:

```powershell
python tools\generate_stellar_ai_director_patch.py
python tools\validate_stellar_ai_director_patch.py
python -m py_compile tools\stellar_ai_director_lib.py tools\generate_stellar_ai_director_patch.py tools\validate_stellar_ai_director_patch.py
python -m unittest discover -s tools\tests
git diff --check
```

When route/source coverage changes:

```powershell
python tools\build_stellar_ai_director_object_atlas.py
```

When live-launch readiness is being reported without launching:

```powershell
python tools\manage_stellaris_commands_at_date.py status
```

Also inspect:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\StellarAIDirector.mod`
- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\dlc_load.json`

## Existing Scripts And Evidence Surfaces

| Script/artifact | Use |
| --- | --- |
| `tools/generate_stellar_ai_director_patch.py` | Regenerate Director mod files and research artifacts. |
| `tools/validate_stellar_ai_director_patch.py` | Run deterministic Director validation. |
| `tools/build_stellar_ai_director_object_atlas.py` | Regenerate object atlas, dependency edges, parent AI support map, policy matrix, coverage report, and route report. |
| `tools/build_stellar_ai_director_file_audit.py` | Refresh generated file surface audit. |
| `tools/build_stellar_ai_director_reference_audit.py` | Refresh generated reference audit. |
| `tools/build_stellar_ai_director_integration_policy_audit.py` | Refresh integration policy readiness audit. |
| `tools/build_stellar_ai_director_roi_quality_audit.py` | Refresh ROI quality audit. |
| `tools/build_stellar_ai_economic_valuation_dataset.py` | Refresh active-stack building/zone/district valuation dataset. |
| `tools/manage_stellaris_commands_at_date.py` | Manage observer command schedule; must report absent outside approved observer runs. |
| `tools/extract_stellar_ai_checkpoint.py` | Extract checkpoint rows from saves during approved observer validation. |
| `tools/tests/test_stellar_ai_director.py` | Deterministic generator and generated-surface test suite. |
| `tools/tests/test_stellar_ai_observer_loop.py` | Observer harness helper tests, not runtime proof. |
| Irony Mod Manager | Playset dependency, conflict, and load-order investigation. |
| CWTools | PDXScript syntax/schema feedback where available. |

## Static Validation Layers

### Layer 1 - File Shape And Generated Ownership

- Every generated `.txt` file parses with the local parser used by validator.
- Every generated common file has expected top-level object type.
- Generated files include generator comments and route/provenance comments for full-object overrides.
- No generated file is hand-edited to pass validation.
- No stale generated folders return after cleanup, especially removed `common/zones` outputs if unsupported.

### Layer 2 - Reference Integrity

- Every referenced technology, resource, scripted trigger, scripted value, opinion modifier, event, localization key, starbase module/building, AP, tradition, megastructure, building, district, decision, and policy option resolves to vanilla, parent mod, or generated inventory.
- Optional-mod references are omitted or guarded unless the generator proves presence.
- Route reports identify unresolved event/script gates as manual-review blockers, not guesses.

### Layer 3 - Compatibility And Conflict Validation

- Irony conflicts are classified as intentional Director wins, required parent wins, harmless additive duplicates, unexpected gameplay conflicts, or false positives.
- Required parent load positions remain documented.
- Director remains after Gigas, NSC3, ESC NEXT, Starbase Extended, Universal Resource Patch, and relevant compatibility patches.
- Stellar AI remains private parity evidence, not descriptor dependency.

### Layer 4 - Safety Gates

Validator should fail on:

- generated `common/diplomatic_actions` unless a future gate explicitly allows it;
- generated `common/personalities` unless a future gate explicitly allows it;
- direct ship-design/component-template/section-template/ship-size overrides unless a future gate explicitly allows them;
- forced war effects in V2 core: `declare_war`, `join_war`, `add_casus_belli`, forced punitive `wg_*` dispatch;
- threat-response economy pressure without survival/recovery/deficit/at-war safety gates;
- stale docs implying Stellar AI is required;
- unsupported economic-plan targets;
- duplicate malformed top-level blocks in copied overrides;
- invalid folder names or localization path/header errors.

### Layer 5 - Strategy Consistency

Tests should check contracts, not tune numbers:

- Route triggers exist and are referenced consistently.
- Research/assembly/construction pressure has support-resource safety gates.
- Pop assembly pressure excludes invalid empire types.
- Trade capacity and special resources are not treated as generic commodities.
- Fleet pressure has payoff route comments/gates.
- Research Federation remains implemented without unsafe diplomacy/personality folders.
- NSC3/ESC support remains technology/resource readiness unless direct graph proof exists.

Do not encode exact observer targets like 5,000 monthly research into unit tests. Keep them in tuning notes and observer plans.

## New Validators And Tests To Add

| Validator/test | Purpose | Acceptance |
| --- | --- | --- |
| `test_stellar_ai_dependency_not_required_current_docs` | Prevent stale launch dependency wording. | Fails on current docs/descriptor implying Stellar AI is required. |
| `test_forbidden_surface_default_absent` | Block unsafe folders by default. | Fails if diplomatic_actions/personalities/direct ship folders are emitted. |
| `test_generated_full_overrides_have_provenance` | Keep conflict decisions auditable. | Every new full-object override has source object, parent path/mod, route, and reason comments. |
| `test_support_resource_gates_for_research_pressure` | Avoid lab spam. | Research construction weights include CG/energy/mineral or equivalent safe runway gates. |
| `test_pop_assembly_empire_type_gates` | Avoid invalid assembly logic. | Assembly objects are gated to valid empires and invalid routes excluded. |
| `test_trade_capacity_not_generic_commodity` | Preserve 4.4 logistics. | Trade-capacity support remains a distinct route/gate. |
| `test_no_direct_ship_stack_overrides_without_gate` | Preserve NSC3/ESC safety. | Direct ship-design/component-template/section-template/ship-size outputs fail by default. |
| `test_threat_response_no_forced_war_effects` | Preserve V1 safety. | Forced war/CB/join-war terms absent. |
| `test_observer_commands_use_game_speed_5` | Preserve approved observer harness speed. | `commands_at_date` helper emits `game_speed 5`, not 4. |
| `test_44_5_log_risk_classifier_patterns` | Classify recurring 4.4.5 log risks. | Known patterns are categorized as Director/parent/compat/manual-review. |

## Acceptance Gates

### Ready To Commit

All are required:

- Generator runs cleanly.
- Validator passes.
- `py_compile` passes.
- Full unit suite passes.
- `git diff --check` passes.
- Relevant generated audits refreshed or explicitly unchanged.
- Docs updated for user-facing behavior.
- No runtime/observer claims unless evidence exists.
- Git staging excludes unrelated raw observer artifacts, temporary context bundle output, and unrelated research packets.

### Ready To Push

All Ready To Commit gates plus:

- Commit created with coherent scope.
- Remote relationship checked.
- Push requested or explicitly allowed by user.
- Push result reported with branch and SHA.

### Ready For Live Launcher

All Ready To Commit gates plus:

- Live descriptor path checked.
- `dlc_load.json` checked.
- `commands_at_date.txt` status checked absent unless approved observer run is active.
- Irony load-order expectation verified or explicitly not checked.
- No claim that runtime behavior works unless launch/runtime evidence exists.

### Ready For Observer Run

All Ready For Live Launcher gates plus explicit user approval and:

- Observer run folder created with metadata/manual-notes template.
- Galaxy/settings/checkpoints agreed or defaulted from prior runbook.
- `commands_at_date.txt` status checked before enable.
- Stop conditions listed.
- Plan to disable/archive `commands_at_date.txt` after run.

## Optional Runtime Observer Plan

Only run after explicit user approval.

### Setup

- Launch via Irony collection/playset containing Stellar AI Director after required parents.
- Record game version, checksum if available, playset, required parents, load position, settings, DLC assumptions, Gigas/Guilli/Forgotten Empires configuration choices, and hidden-bonus posture.
- Use Tiny/Small benchmark first unless user chooses otherwise.
- Use no hidden AI economic bonuses by default unless user approves a separate balance mode.

### Checkpoints

- 2250, 2300, 2325, 2350.
- Optional 2270/2280 if measuring early research target.

### Metrics

- Monthly research by category and total.
- Economy power, tech power, fleet power.
- Incomes and stockpiles for energy, minerals, food, CG, alloys, trade/trade capacity, unity, influence, special resources.
- Pops, colonies, systems, habitats.
- Empty researcher jobs and unstaffed specialist jobs where save parser supports it.
- Traditions/APs/technologies unlocked.
- Mega Engineering, Mega Shipyard, Gigas routes, megastructures started/upgraded/completed.
- NSC3/ESC tech/hull/component readiness.
- Wars, conquests, subjects, raiding outcomes.
- Starbase/defense investment.
- Deficits, survival/recovery states.
- Research agreements/federation type/subjects/scholaria.

### Stop Conditions

- Freeze/crash at load or game start.
- New repeated Director-owned error lines.
- Event spam.
- Missing localization or missing generated object errors.
- Major economy collapse caused by new weights.
- Observer commands left installed outside active run.
- Parent-mod issue prevents interpreting Director behavior.

## Reporting Format For Codex

```text
Validation:
- generate: pass/fail, command, notable output
- validator: pass/fail, command, notable output
- unit tests: pass/fail, count
- py_compile: pass/fail
- git diff --check: pass/fail
- Irony/CWTools: checked/not checked, result
- live descriptor: checked/not checked, result
- observer command status: checked/not checked, result
- runtime: not run unless approved

Status:
- Live mod: ...
- Commit: ...
- Push: ...
```
