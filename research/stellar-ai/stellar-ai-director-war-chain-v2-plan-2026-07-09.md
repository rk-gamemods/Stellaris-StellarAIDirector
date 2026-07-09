# Stellar AI Director War-Chain V2 Plan

Date: 2026-07-09

Task card: T21 - War-chain research plan

## Scope

This is a design-only pass. It does not implement new gameplay output. The
purpose is to define an advanced war-chain v2 direction that can improve AI war
coherence without unsafe direct war control.

## Sources

- T20 fleet payoff review:
  `research/stellar-ai/stellar-ai-director-fleet-payoff-route-review-2026-07-09.md`
- Threat-response feasibility note:
  `research/stellar-ai/stellar-ai-director-threat-response-feasibility-2026-07-05.md`
- JDataMunch `stellar_ai_war_mechanics_lever_catalog_20260708`
- JDataMunch `stellar_ai_war_mechanics_defines_catalog_20260708`
- Current generated threat-response files:
  - `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
  - `mods/StellarAIDirector/events/zzz_staid_threat_response_events.txt`
  - `mods/StellarAIDirector/common/on_actions/zzz_staid_threat_response_on_actions.txt`
  - `mods/StellarAIDirector/common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`

## Verified Baseline

Current threat response is a reactive observer path:

- `on_war_beginning` fires the Director observer.
- War-goal checks use block syntax:
  `using_war_goal = { type = wg_conquest owner = root }`, plus subjugation and
  humiliation variants.
- The observer stores timed country flags such as
  `staid_tr_war_goal_conquest`.
- Eligible observers require communications and non-participation.
- Observer effects remove and apply opinion modifiers, set timed relation
  flags, and set defensive-readiness flags when foreign affairs are safe.

Scoped search over the current threat-response triggers, events, on-actions,
and opinion modifiers found no `declare_war`, `join_war`, `add_casus_belli`,
`set_war_goal`, `create_war`, `add_claim`, or `create_claim` output.

## Safe V2 Levers

War-goal memory:

- Extend the current timed war-goal flags into richer route memory for
  conquest, subjugation, humiliation, crisis, and total-war categories.
- Keep it observational: use `on_war_beginning`, `using_war_goal`, attacker,
  defender, leader, and communications context only.

Opinion pressure:

- Scale existing opinion and relation flags by repeated aggression and shared
  threat context.
- Keep modifiers timed/decaying and visibility-gated.

Defensive readiness:

- Convert observed hostile war-chain state into readiness flags consumed by
  starbase defense, fleet reserve, shipyard, and economic support weights.
- Keep economy gates such as `staid_tr_foreign_affairs_safe`,
  `staid_fleet_buildup_economy_safe`, and `staid_starbase_defense_economy_safe`.

Policy bias:

- Bias already-legal policy, bombardment, and diplomatic-stance options when
  the AI has the economy and route readiness to use them.
- This is the same safe class as T20: AI weights only, no direct war dispatch.

Claim and CB support research:

- Future work may research indirect support for claims, subject wars, or
  conquest access.
- Any such pass must first prove the current 4.4.5 vanilla and active-stack
  surfaces. The default should remain indirect support through economy,
  policies, military readiness, threat, and opinion pressure.

## Forbidden Paths

Do not implement the following in war-chain v2:

- `declare_war`
- `join_war`
- `set_war_goal`
- `create_war`
- `add_casus_belli`
- `add_claim`
- `create_claim`
- broad `00_personalities` rewrites
- broad `common/casus_belli` or `common/war_goals` overrides
- forced federation/join-war behavior
- direct fleet spawning, teleporting, or forced attack orders

These are forbidden because the war-mechanics catalog shows legal war access is
guarded by claims, CBs, war goals, relative power, target independence, subject
status, total-war rules, and policy validity. Forcing around those gates would
be high-risk and likely incompatible.

## Future Implementation Shape

If a future implementation card is approved, build it in this order:

1. Add new `staid_tr_*` observer flags or values for richer war-goal memory.
2. Add tests that prove all new `using_war_goal` checks use block syntax.
3. Add tests that forbid direct war/CB/claim hooks.
4. Add conservative AI-weight consumers in existing Director-owned policy,
   starbase, fleet reserve, and economy surfaces.
5. Refresh generated audits and reference indexes.
6. Defer efficacy claims until observer telemetry shows actual useful wars,
   raiding, claims, defensive coalitions, and survival outcomes.

## Validation

- JDataMunch validated both war-mechanics datasets.
- JDocMunch retrieved and hash-verified the threat-response feasibility
  sections used for this plan.
- JCodeMunch located current threat-response generator/test surfaces.
- Scoped `rg` over current generated threat-response files found no forbidden
  direct war/CB/claim outputs.

## Runtime Boundary

No runtime claim is made here. War-chain v2 remains a future design plan until
the packet reaches the approved observer-test phase or a later implementation
card explicitly asks for this work.
