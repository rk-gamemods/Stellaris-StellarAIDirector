# Stellar AI Director Research Diplomacy Safe Lane

Date: 2026-07-09

Task card: `plans/stellar-ai-director-strategic-v2/CODEX_TASK_SLICES.md` T11.

Target version: Stellaris PC 4.4.5 stable/current local install.

## Objective

Preserve Research Cooperative and research-friendly diplomacy without unsafe direct diplomatic action or personality rewrites.

## Sources Checked

- Vanilla federation type: `C:\Steam\steamapps\common\Stellaris\common\federation_types\00_federation_types.txt`
- Vanilla research-agreement action: `C:\Steam\steamapps\common\Stellaris\common\diplomatic_actions\00_actions.txt`
- Generated federation override: `mods/StellarAIDirector/common/federation_types/zzzz_staid_15_research_diplomacy_federation_types.txt`
- Generated policy/tradition/AP support: `mods/StellarAIDirector/common/policies/zzzz_staid_10_opening_growth_policies.txt`, `mods/StellarAIDirector/common/traditions/zzzz_staid_02_perks_traditions_traditions.txt`, `mods/StellarAIDirector/common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt`
- Generated route trigger: `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt`

## Findings

The generated Research Cooperative surface is the safe implementation lane for T11. The Director copies the vanilla `research_federation` object into `common/federation_types`, preserves the vanilla `host_has_dlc = Federations`, `research_federation_passive`, level perks, and existing personality/cohesion acceptance structure, then adds Director-owned top-level `ai_weight` modifiers for `staid_research_diplomacy_priority_ready`, science-snowball readiness, research runway, materialist/machine preference, and Discovery federation completion.

The generated support lane also includes source-backed Discovery, Diplomacy, and Technological Ascendancy pressure plus cooperative diplomatic stance support. This satisfies the "research-friendly diplomacy" target without writing broad personality behavior or direct diplomatic action files.

The vanilla research agreement action remains a gated surface. `action_form_research_agreement` has a negative `AI_acceptance_base_value = -50`, many genocidal/isolationist/federation/separate-treaty exclusions, and explicit prerequisites for good opinion or trust plus embassy or Diplomatic Networking. Those prerequisites are plausible future levers, but direct action formation is still unsafe without a focused active-stack winner map, acceptance mechanics proof, and negative tests. No generated `common/diplomatic_actions` or `common/personalities` output is allowed for T11.

## Decision

T11 keeps research agreement formation deferred and source-gated. The current packet implementation should prefer Research Cooperative through `common/federation_types`, maintain cooperative diplomatic stance and Discovery/Diplomacy/AP support, and leave `action_form_research_agreement` untouched until T12 proves a safe implementation path.

## Validation

- `test_research_federation_weight_is_generated_without_unsafe_diplomacy_overrides` now checks that the generated federation file parses, Research Cooperative preference markers remain present, cooperative stance and Discovery/Diplomacy/AP support remain present, `action_form_research_agreement` is absent from generated common files, and `common/diplomatic_actions` plus `common/personalities` are not emitted.
- Static validation must continue to parse the generated federation file and reject forbidden diplomacy/personality surfaces.

## Remaining Risk

Static validation proves the generated files preserve the safe lane. It does not prove that AI empires will form enough Research Cooperatives or satisfy research-agreement prerequisites in live play; that remains runtime observer evidence after all non-runtime packet work is complete.
