# Stellar AI Director Standalone Baseline Cleanup

Date: 2026-07-08
Target: Stellaris PC 4.4.5 stable/current local install
Scope: post-standalone-baseline project cleanup, static validation, and next-work gap inventory.

## Current Source Of Truth

- `mods/StellarAIDirector/README.md` and `mods/StellarAIDirector/descriptor.mod` are the user-facing launch surface.
- `mods/StellarAIDirector/notes/load-order.md` records current load-order expectations.
- `research/stellar-ai/stellar-ai-director-standalone-parity-inventory-2026-07-08.md` records which Stellar AI-style surfaces are implemented, partially implemented, or deferred.
- `research/stellar-ai/stellar-ai-director-open-roadmap-2026-07-07.md` remains the detailed implementation roadmap.
- `research/stellar-ai/archive/standalone-baseline-cleanup-2026-07-08/README.md` classifies superseded or historical evidence that should not be read as current launch status.

## Dirty-State Classification

| Class | Count | Action | Rationale |
| --- | ---: | --- | --- |
| Tracked Director mod files | 15 | keep/update | Generated or user-facing Stellar AI Director baseline outputs. Refresh through `tools/generate_stellar_ai_director_patch.py`. |
| Untracked Director mod files | 19 | keep/update | New generated standalone surfaces for budgets, policies, edicts, decisions, fleet doctrine, Planetary Diversity, and high-scale construction pressure. |
| Tracked Director research files | 30 | keep/update or archive-by-index | Current generated audits and historical notes. Generator-owned outputs stay in place; stale interpretation is handled by current README/gap/archive docs. |
| Untracked Director research files | 69 | keep/update, with observer artifacts treated as historical evidence | Includes current parity inventory, roadmap, static validation notes, generated data artifacts, observer run summaries, and war-mechanics reference material. Runtime observer artifacts are not current standalone proof unless explicitly revalidated. |
| Director tools/tests | 11 | keep/update | Generator, validator, observer-harness helper, log summarizers, and associated tests needed for static validation and safe observer-command status checks. |
| Repo docs/config | 5 | keep/update if staged with baseline | `.gitignore`, `AGENTS.md`, `README.md`, `mods/README.md`, and `research/README.md` contain project-level 4.4.5, Munch, and observer-harness rules. Stage only if the commit intentionally includes project policy cleanup. |
| Non-Director research/mod docs | 16 tracked | leave unstaged unless separately requested | RK trait docs and broad Stellaris/WebChatGPT research are outside the standalone Director baseline cleanup. |
| Codex skill/guide packets | 221 untracked | ignore/leave unstaged for this baseline | Large support packets are unrelated to the Director standalone launch baseline. |
| `chatgpt_context_bundle/` | 2 untracked | ignore/leave unstaged | Temporary context-bundle helper output, not part of the mod baseline. |

## Quantified Remaining Gaps

| Gap | Status | Evidence | Owner surface | Risk | Next action |
| --- | --- | --- | --- | --- | --- |
| Runtime observer proof | not complete | Static validation and previous observer artifacts exist, but this cleanup goal explicitly does not launch Stellaris or run observer games. Current parity inventory marks runtime proof as deferred. | `research/stellar-ai/observer-runs/`; `tools/manage_stellaris_commands_at_date.py`; future user-approved Irony observer run | High: static proof cannot demonstrate actual AI timing, queue behavior, or crisis-readiness slope. | Run a user-approved Irony observer pass after baseline commit; record live `commands_at_date.txt` status before and after. |
| Broad personality rewrites | not implemented | Current generated mod has no `common/personalities` output. Roadmap gates personalities as high-risk full-object behavior. | Future generator route plus active-stack conflict review | High: personality rewrites can alter diplomacy/war behavior globally and conflict with other AI mods. | Inventory winning personality files, identify minimal safe fields, and require conflict proof before generation. |
| Diplomatic action overrides | not implemented | Current generated mod has no `common/diplomatic_actions` output. Research-agreement behavior remains gated by exact vanilla/active-stack semantics. | Future diplomacy compatibility slice | High: action acceptance/proposal rules can break diplomacy or federation behavior. | Build a focused diplomatic-action audit before any override. Prefer stance/federation weights unless direct action edits are proven safe. |
| Advanced war chain behavior | partial baseline only | Director has threat response, conquest/raiding reserves, bombardment stance support, and war-support economy pressure, but no direct declaration/CB/war-goal chain override. | `common/scripted_triggers`, `events`, `common/bombardment_stances`, future war-mechanics slice | Medium-high: static reserves may not produce desired offensive wars or crisis posture. | Use `war-mechanics-reference-2026-07-08/` plus local vanilla/active-stack files to design a separate war-chain pass. |
| Direct NSC3/ESC ship design/component/section handling | not implemented | Parity inventory and roadmap note direct ship-design/component/section handling is deferred. Current support is technology/resource readiness only. | Future ship-stack compatibility slice | High: ship size, section, component, and design overrides are conflict-heavy and load-order sensitive. | Build a source-verified NSC3/ESC lane report, then generate only minimal safe technology/component support. |
| Advanced Gigas route optimization and continuation proof | partial static support | Director has Gigas route weights, megastructure/economic-plan reserves, and generated audits, but no runtime proof that queues continue, upgrade, and sequence optimally. | `common/megastructures`, `common/economic_plans`, route reports, future observer proof | Medium-high: AI can still stall on cost, prerequisites, site limits, or continuation chains. | Add queue/continuation evidence from save inspection or observer runs before claiming optimization. |
| Colony type/designation breadth beyond targeted planet logic | partial baseline | Baseline covers Planetary Diversity/outpost value and building/district pressure; broad colony type/designation rewrites remain deferred. | Future colony automation/designation slice | Medium: broad designation rewrites can fight vanilla automation and modded planet types. | Inventory current winning colony/designation objects and add targeted rules only where evidence shows gaps. |
| Remaining stale Stellar AI dependency wording | mostly cleaned, monitor | Public Director README and load-order notes say Stellar AI is a private parity source, not dependency. Research README was updated in this cleanup. Archive index marks old launch/observer notes historical. | `mods/StellarAIDirector/README.md`, `mods/StellarAIDirector/notes/load-order.md`, `research/stellar-ai/README.md`, archive index | Medium: old reports can still be misread as launch requirements. | Re-run exact stale-wording search after regeneration; update current docs or archive index for any remaining current-surface conflicts. |
| Commit/push/live-launch readiness | pending validation in this cleanup | Previous memory says static validation passed and live descriptor was installed, but this run must re-check after generator/doc cleanup. | Git, live descriptor, `dlc_load.json`, validation commands | Medium: untracked unrelated files can pollute commit; launcher files can drift. | Regenerate, validate, verify live descriptor/dlc_load/observer command status, then stage only the coherent baseline and push. |

## Cleanup Rationale

- Generated mod outputs remain in their generator-owned paths and are refreshed by `tools/generate_stellar_ai_director_patch.py`.
- Private Stellar AI provenance is preserved because it explains replacement decisions, but current user-facing docs must not imply Stellar AI is required.
- Historical launch, observer, and failed-or-partial roadmap artifacts are indexed through the archive note instead of deleted, so future work can inspect them without mistaking them for current readiness.
- Unrelated broad research packets and temporary context bundles are left unstaged unless the user requests a separate cleanup commit.
