# Risk Prevention And Mitigation

## Risk Doctrine

Threat response is high-risk because it touches diplomacy, opinion modifiers, event dispatch, war context, and economy pressure. Prevent risk through generator-owned contracts and validator failures before relying on launch or observer-game smoke tests.

## Risk Register

| ID | Risk | Prevention | Mitigation | Proof |
| --- | --- | --- | --- | --- |
| R1 | Abstract design axes leak into runtime as unsupported Stellaris concepts. | Keep axes only in generator constants and emitted comments/docs. Runtime files consume script values, triggers, flags, and opinion modifiers only. | Remove leaked axis references from generated files and add validator checks for raw axis names in runtime-sensitive contexts. | Unit tests and validator scan generated files. |
| R2 | `on_war_beginning` fires multiple galaxy-wide reactions for one war. | First event verifies attacker-side war leader before observer iteration. | Add duplicate-suppression relation/country flag only if launch testing shows repeated application. | Event contract tests inspect attacker leader gate and event IDs. |
| R3 | Unknown modded war goals accidentally create punitive effects. | Classification lookup defaults to severity `0` and inert outputs. | Add unknown war goal to CSV for manual review; do not hot-classify without tests. | Unknown-war-goal tests and CSV audit. |
| R4 | Generated files accidentally add forced war behavior. | Validator forbids `declare_war`, `join_war`, `add_casus_belli`, forced punitive `wg_*`, and generated diplomatic-action overrides. | Revert the offending generated event path and split punitive-war work into a separate plan. | Forbidden-effect tests fail before launch. |
| R5 | Third-party observers spend into collapse. | `staid_tr_foreign_affairs_safe` requires no deficit, no survival, no recovery, not at war, high income, and high stockpiles. | Set threat economy output to zero and leave only opinion effects for struggling empires. | Safety-gate and economy-ratio tests. |
| R6 | Opinion modifiers stack beyond intended caps. | Remove lower and opposite modifiers before applying higher tiers; use decay and bounded values. | Add cleanup event path or stricter non-accumulative modifiers if runtime shows stacking drift. | Repeated-application tests and validator checks. |
| R7 | Event scopes point at the wrong country. | Document root/from/fromfrom contract and inspect generated event blocks. | Disable output application until scope is corrected; preserve classification tests. | Event-flow tests and launch log checks. |
| R8 | Observer loop creates performance problems. | Exclude participants, require awareness, prefer representative defender, and avoid observer-to-observer mesh in V1. | Reduce outputs to relation with aggressor only if observer-game smoke shows overhead. | Static loop inspection and observer smoke notes. |
| R9 | Compatibility cases behave strangely. | Check Nomads, Arkships, Waystations, Waylines, Contracts, 4.4 Situation Log, Gigas, NSC3, and active playset AI/economy mods where touched. | Add explicit exclusions for country types or situations that cannot safely participate. | Research note and runtime smoke checklist. |
| R10 | Generated output conflicts with existing override audits. | Extend file/reference/conflict audit coverage for opinion modifiers, on-actions, events, and localization. | Classify intentional overrides or rename files/objects to avoid collisions. | Generated conflict and reference audit artifacts. |
| R11 | Localization encoding or keys break load. | Generate only explicit localization keys and keep file under `localisation/english`. | Remove visible strings until localization passes. | Unit tests and validator localization checks. |
| R12 | Source corpus becomes stale before implementation. | Refresh JDocMunch/JCodeMunch indexes and local source snapshots when current sources are needed. | Pause classification expansion until fresh evidence exists. | Verify-index output and research note timestamp. |
| R13 | Score math becomes hard to represent in PDXScript. | Generator remains source of truth and may emit equivalent tier triggers. | Replace direct formula script values with generated tier triggers and keep expected-output tests. | Formula/tier equivalence tests. |
| R14 | Homicidal or crisis actors receive normal moral diplomacy. | Route homicidal/genocidal paths through special vectors and exclusions. | Make those actors inert or severe-only depending on verified country type behavior. | Scenario tests and source-evidence note. |

## Prevention Gates

Implementation must stop before runtime testing if any gate fails:

- Munch startup and relevant indexes are not healthy.
- Generated files do not parse.
- Validator reports missing references, missing localization, out-of-range values, or forbidden effects.
- Unit tests fail.
- Unknown war goals produce anything other than inert output.
- Economy pressure can be emitted while survival/recovery/deficit/at-war gates fail.

## Mitigation Boundaries

Allowed mitigations:

- Narrow outputs to opinion-only while preserving the classification model.
- Keep generated event files present but unhooked from `on_war_beginning` until tests pass.
- Exclude uncertain country types or compatibility cases from observer eligibility.
- Treat unknown or unverified war goals as inert.
- Reduce shared-threat behavior to observer-to-victim only.

Disallowed mitigations:

- Bypassing validator failures for launch testing.
- Hand-editing generated files as the durable fix.
- Adding a runtime forced-war path to compensate for weak opinion impact.
- Weakening survival/recovery/deficit gates.
- Treating a passing launch as proof that deterministic tests are unnecessary.

## Rollback Boundary

Rollback is source-driven:

- remove or revert the generator constants/functions;
- remove generated threat-response files through the generator;
- remove on-action hook before launch testing if event behavior is suspect;
- keep research/audit notes that explain why rollback happened.

Do not delete unrelated Stellar AI Director files or existing evidence artifacts when rolling back this feature.
