# Open Questions For User

Generated: 2026-07-08
Packet: Stellar AI Director Strategic V2 Roadmap Packet
Target: Stellaris PC 4.4.5 stable/current, backwards compatible with 4.4.4 where source-backed


These questions require user preference, approval, or release-direction choices. Technical unknowns are in `RESEARCH_QUESTIONS.md`.

## Approval-Gated Work

| ID | Question | Default if unanswered | Why user decision is required |
| --- | --- | --- | --- |
| UQ01 | Do you approve a new runtime observer benchmark after static V2 validation passes? | No runtime observer run. | Runtime launch/observer work is explicitly approval-gated and can alter live observer command files. |
| UQ02 | Should observer benchmarks use the previous tiny 12-AI 25x-crisis style setup, a larger realistic campaign setup, or both? | Tiny static-comparison setup first, if approved. | Settings heavily affect interpretation and runtime cost. |
| UQ03 | Are hidden AI economic bonuses acceptable as a separate optional balance mode? | No hidden bonuses. | This changes philosophy from smarter AI behavior to compensation. |
| UQ04 | What AI power level is acceptable: competitive but beatable, near-human optimized, or deliberately brutal for high-scale crises? | Competitive but not hidden-bonus brutal. | Determines whether tuning should preserve normal-feeling galaxy balance or chase crisis parity aggressively. |
| UQ05 | Should the top AI be tuned for 25x crisis relevance by 2350 as the main benchmark? | Treat as aspirational observer target, not static gate. | The benchmark shapes early research/fleet/aggression tradeoffs. |

## Compatibility Preferences

| ID | Question | Default if unanswered | Why user decision is required |
| --- | --- | --- | --- |
| UQ06 | Are Gigastructural Engineering, NSC3, ESC NEXT, Starbase Extended, Planetary Diversity, UIOD, and Universal Resource Patch all mandatory targets for V2? | Yes for core V2 compatibility. | Required parents and scope determine route graph and validation effort. |
| UQ07 | Should Director preserve compatibility with Stellar AI as an optional same-playset mod, or only use it as private parity reference? | Private parity reference only. | Optional coexistence creates extra load-order/conflict burdens. |
| UQ08 | Are other AI/performance mods in the preferred playset mandatory compatibility targets? | Research overlap first; do not guarantee. | AI/performance mods can suppress behavior or conflict with Director. |
| UQ09 | Should Starbase Extended remain the defense baseline, or should lighter defense mods be considered later? | Keep Starbase Extended baseline for this phase. | Defense strategy depends on parent module/building objects. |

## Behavior Philosophy

| ID | Question | Default if unanswered | Why user decision is required |
| --- | --- | --- | --- |
| UQ10 | Should militarist AIs be pushed toward more wars if safe, or should V2 avoid changing aggression until runtime proof exists? | Avoid direct aggression changes; improve payoff support first. | War behavior can change campaign feel and stability. |
| UQ11 | Should non-genocidal diplomacy be made more cooperative for research pacts/federations, even if it reduces conflict density? | Make research cooperation more attractive through safe levers only. | Diplomacy tuning changes galaxy politics. |
| UQ12 | Should crisis defense prioritize fleet production, starbase chokepoints, megastructure economy, or balanced readiness? | Balanced readiness with research/economy preserved. | Determines resource allocation under threat. |
| UQ13 | Should AI be allowed to exploit strong trait/empire-creation mods if they are in the playset? | Do not add trait-specific AI exploitation in V2 unless later requested. | Trait mods can make AI power uneven and require separate compatibility study. |

## Release And Workflow

| ID | Question | Default if unanswered | Why user decision is required |
| --- | --- | --- | --- |
| UQ14 | Should Codex commit each validated slice, or only produce a working tree for review? | Commit only when explicitly asked. | Repo policy requires explicit reporting; user may want review before commit. |
| UQ15 | Should Codex push after a successful commit? | Do not push unless explicitly asked. | Remote state is separate from local commit readiness. |
| UQ16 | Should the live launcher descriptor be updated automatically after source changes? | Check and report live state; update only if asked by implementation prompt. | Source mod and live launcher state are separate. |
| UQ17 | Should the V2 packet itself be committed into the repo under `plans/` or `research/`, or used only as external Codex handoff input? | Use as external handoff unless user asks to commit it. | Planning artifacts can clutter repo if not intentionally placed. |

## Recommended Defaults For Codex

Unless the user answers otherwise, Codex should implement with these defaults:

```text
Runtime observer: no
Hidden AI bonuses: no
Target version: 4.4.5, compatible with 4.4.4 where source-backed
Core compatibility: Gigas, NSC3, ESC NEXT, Starbase Extended, UIOD, URP, Planetary Diversity
Stellar AI: private parity reference only, not dependency
Unsafe surfaces: research-gated, not generated by default
War aggression: support payoff and readiness, no forced wars
Commit/push/live install: report separately; do not assume approval
```
