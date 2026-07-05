# Stellar AI Director Threat Response Plan Set

Status: expanded planning package.
Source plan: [../stellar-ai-director-threat-response-plan.md](../stellar-ai-director-threat-response-plan.md).
Target game version: Stellaris PC 4.4.4 stable.
Created: 2026-07-05.

This folder splits the original threat-response plan into focused, implementation-ready documents. Treat the source plan as the design brief and this folder as the controlling handoff package for implementation, validation, and review.

## Documents

- [00 Annotated Review](00-annotated-review.md): section-by-section review of the source plan, including gaps that this plan set closes.
- [01 Goals, Deliverables, And Acceptance](01-goals-deliverables-and-acceptance.md): concrete outputs, non-goals, source-of-truth rules, and pass/fail completion criteria.
- [02 Main Implementation Plan](02-main-implementation-plan.md): generator, emitted file, validator, and documentation work to perform.
- [03 Runtime Interaction Contract](03-runtime-interaction-contract.md): event flow, scopes, observer rules, war-goal classification, output precedence, and logical interaction clarifications.
- [04 Risk Prevention And Mitigation](04-risk-prevention-and-mitigation.md): risk register, prevention gates, mitigation paths, rollback boundaries, and stop conditions.
- [05 Testing And Validation Plan](05-testing-and-validation-plan.md): deterministic tests, validator checks, scenario matrix, commands, and manual runtime validation.
- [06 Implementation Slices And Handoff](06-implementation-slices-and-handoff.md): execution order, slice gates, handoff evidence, and completion packaging.
- [07 Research And Evidence Maintenance](07-research-and-evidence-maintenance.md): feasibility note, war-goal classification CSV, source corpus refresh, and audit artifact rules.

## Controlling Rules

- The Python generator in `tools/stellar_ai_director_lib.py` is the source of truth for threat-response constants, tables, generated PDXScript, validation, and research artifacts.
- The generated mod files under `mods/StellarAIDirector/` are outputs. Do not hand-edit them as the durable source of behavior.
- V1 is diplomacy and defensive-readiness pressure only. It must not declare wars, join wars, add punitive CBs, overwrite diplomatic actions, or bypass existing Director survival/recovery/deficit gates.
- Design axes such as `moral_outrage` and `regional_fear` must stay generator-owned. Stellaris runtime artifacts must consume only emitted script values, triggers, flags, events, and opinion modifiers.
- Unknown or unclassified war goals are inert until intentionally classified.

## Done Definition

This plan set is complete enough for implementation only when:

- every deliverable in [01 Goals, Deliverables, And Acceptance](01-goals-deliverables-and-acceptance.md) has a named output and acceptance check;
- every runtime interaction in [03 Runtime Interaction Contract](03-runtime-interaction-contract.md) has a deterministic validation path or is explicitly marked manual/runtime-only;
- every high-risk failure mode in [04 Risk Prevention And Mitigation](04-risk-prevention-and-mitigation.md) has a prevention check and a mitigation path;
- the automated checks in [05 Testing And Validation Plan](05-testing-and-validation-plan.md) pass before any launch or observer-game smoke test;
- completion evidence is captured in the implementation handoff described in [06 Implementation Slices And Handoff](06-implementation-slices-and-handoff.md).
