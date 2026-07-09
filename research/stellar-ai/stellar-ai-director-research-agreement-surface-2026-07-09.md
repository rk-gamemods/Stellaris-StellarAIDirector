# Stellar AI Director Research Agreement Surface Study

Date: 2026-07-09

Task card: `plans/stellar-ai-director-strategic-v2/CODEX_TASK_SLICES.md` T12.

Target version: Stellaris PC 4.4.5 stable/current local install.

Output boundary: research only. No generated gameplay output was added for this task.

## Objective

Determine whether a safe implementation path exists for making AI research agreements more likely.

## Source Order Used

1. T12 packet contract and T11 safe-lane decision.
2. Current local vanilla files under `C:\Steam\steamapps\common\Stellaris`.
3. Active-stack source-root and winner/conflict datasets:
   - `stellaris_packet_active_source_roots_20260708`
   - `stellaris_packet_winning_objects_20260708`
   - `stellaris_packet_active_load_order_conflicts_20260708`
4. Exact active-root searches for `action_form_research_agreement`, acceptance gates, and personality research-agreement fields.
5. Current generated Stellar AI Director output.

## Findings

The active stack leaves `action_form_research_agreement` on the vanilla source object. JData validation passed for `stellaris_packet_active_source_roots_20260708`, `stellaris_packet_winning_objects_20260708`, and `stellaris_packet_active_load_order_conflicts_20260708`. Active source-root filtering confirmed relevant active candidates among the broad Workshop hits were only vanilla, More Primitives at load position 61, and Gigastructural Engineering at load position 62. Exact active-root search found `action_form_research_agreement` only in vanilla `common/diplomatic_actions/00_actions.txt`; More Primitives and Gigas define other diplomatic actions but not this object.

The vanilla action has a negative `AI_acceptance_base_value = -50`. Its visible prerequisite chain includes default/exiled country type gating, genocidal and isolationist exclusions, machine exterminator compatibility cases, infernal and khan exclusions, federation separate-treaty exclusions, automatic research-sharing exclusion for Research Cooperative federation members, pompous purist intel gates, a good-opinion or trust requirement, an embassy or `tr_diplomacy_diplomatic_networking` requirement, and protectorate exclusion.

Personality is a real acceptance lever, but it is not a safe T12 implementation surface. Vanilla `common/personalities/00_personalities.txt` documents `research_agreement_acceptance` as directly added to research-agreement acceptance. Examples include `erudite_explorers = 50`, `peaceful_traders = 10`, and `federation_builders = 15`, while hostile or isolated personalities can be negative or blocked. Changing personalities would affect far more than research agreements and requires a separate active-stack winning personality map plus field-by-field merge plan.

The current packet JData winner/conflict matrices do not include `action_form_research_agreement`. `get_rows` for that object returned zero rows in both `stellaris_packet_winning_objects_20260708` and `stellaris_packet_active_load_order_conflicts_20260708`. That means the current evidence surfaces cannot prove a winning diplomatic-action object or conflict-safe full-object override. This is a blocker for implementation, not for research.

## Implementation Decision

Defer direct implementation for research agreement formation.

Safe work already exists through T10/T11: cooperative diplomatic stance support, Discovery/Diplomacy/AP pressure, and copied Research Cooperative federation weighting. Directly patching `common/diplomatic_actions/action_form_research_agreement` or broad `common/personalities` would cross the packet's unsafe-surface gate without enough proof.

## Future Safe Path

A future implementation can become eligible only after all of the following are true:

1. A dedicated active-stack `diplomatic_actions` winner/conflict extractor proves the winning `action_form_research_agreement` object and all later active contenders.
2. A personality winner map proves which active `common/personalities` objects win and how `research_agreement_acceptance` interacts with other behavior fields.
3. Negative tests cover genocidal, inward perfection, pompous purist, federation separate-treaty, Research Cooperative automatic-sharing, subject/protectorate, and low-opinion/no-embassy cases.
4. A proposed change uses the smallest safe lever, preferably prerequisite support through traditions/stance/trust/opinion paths before any full action or personality override.
5. Static validation rejects generated `common/diplomatic_actions` and `common/personalities` unless this gate is explicitly flipped with source-backed tests.

## Artifacts

- Evidence matrix: `research/stellar-ai/stellar-ai-director-research-agreement-surface-2026-07-09.csv`
- Prior safe-lane report: `research/stellar-ai/stellar-ai-director-research-diplomacy-safe-lane-2026-07-09.md`

## Validation

- JData `validate_index` returned `ok` for `stellaris_packet_active_source_roots_20260708`.
- JData `validate_index` returned `ok` for `stellaris_packet_winning_objects_20260708`.
- JData `validate_index` returned `ok` for `stellaris_packet_active_load_order_conflicts_20260708`.
- JData `get_rows` for `object_id = action_form_research_agreement` returned zero rows in both winner/conflict matrices, proving this object is not currently modeled there.
- Exact active-root `rg` found `action_form_research_agreement` only in vanilla active diplomatic actions.
- No mod gameplay, generator, or validator files changed for T12.

## Remaining Risk

The conclusion is static. It does not prove whether AI empires will form enough research agreements during observer play; it only proves that the current packet lacks the source-backed gate needed to alter direct research-agreement formation safely.
