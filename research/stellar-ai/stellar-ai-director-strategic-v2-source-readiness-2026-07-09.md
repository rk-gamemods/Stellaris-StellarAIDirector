# Stellar AI Director Strategic V2 Source Readiness

Date: 2026-07-09

## Scope

This note closes task card T00 for the strategic v2 packet. It records the
current source hierarchy, launch-dependency posture, version target, and known
deferred gaps before implementation or validator changes.

## Current Target

- Target game version: Stellaris PC 4.4.5 stable/current local install.
- Launcher descriptor compatibility: `supported_version="v4.4.*"`.
- Historical 4.4.4 notes and observer artifacts remain useful background, but
  they are not current proof unless revalidated against 4.4.5 local sources,
  generated audits, active playset state, or new observer evidence.

## Standalone Dependency Posture

`mods/StellarAIDirector/descriptor.mod` defines Stellar AI Director as a
standalone mod with these required parents:

- Gigastructural Engineering & More (4.4)
- NSC3
- Extra Ship Components NEXT
- Starbase Extended 3.0
- !!!Universal Resource Patch [2.4+]

The descriptor does not require Stellar AI. Current mod documentation also says
Stellar AI is private parity/reference evidence only and is not a launch
dependency for the standalone baseline.

## Packet Source Hierarchy

The strategic v2 packet now governs new work in this order:

1. `PACKET_MANIFEST.md`
2. `PRD.md`
3. `TECHNICAL_CONTRACTS.md`
4. `VALIDATION_AND_TEST_PLAN.md`
5. `IMPLEMENTATION_ROADMAP.md`
6. `CODEX_TASK_SLICES.md`
7. `AI_BEHAVIOR_DESIGN.md`
8. `EVIDENCE_MAP.csv`
9. `DECISION_MATRIX.csv`
10. `RESEARCH_QUESTIONS.md`
11. `OPEN_QUESTIONS_FOR_USER.md`

Implementation must proceed through `CODEX_TASK_SLICES.md` one validated task
card at a time. The roadmap is planning context, not a direct implementation
order.

## Current Evidence

- Munch startup gate passed for the active thread: JDocMunch, JCodeMunch, and
  JDataMunch guide calls returned content, and
  `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1` reported
  `MUNCH_PREFLIGHT_PASS`.
- JDocMunch index `local/StellarisMods-strategic-v2-active-20260709` covers the
  packet, mod documentation, and observer runbook with embeddings disabled.
- JDataMunch indexed and validated the packet evidence map and decision matrix.
- JCodeMunch indexed the current repository state after commit
  `ca2d9d75238ffa08a60f78fd0d191d025d7ad542`.
- `tools\manage_stellaris_commands_at_date.py status` reported no live
  `commands_at_date.txt` file.
- A narrowed stale-wording scan over `mods/StellarAIDirector/**` and
  `research/stellar-ai/**` found no current launch dependency on Stellar AI and
  no current claim that 4.4.4 is the active target. It found expected historical
  notes, deferred observer-proof references, and one live localization load
  proof string that still says "v1"; that wording is a documentation cleanup
  item, not a dependency blocker.

## Deferred Gaps Carried Into V2

- Runtime observer proof is not current and remains required before runtime
  efficacy claims.
- Advanced Gigas queue continuation and sequencing need static and runtime
  evidence.
- NSC3 and ESC direct ship-design/component/section handling remains research
  gated.
- Personality, diplomatic-action, forced-war, broad ship-stack, and hidden-bonus
  surfaces remain forbidden unless separately authorized and source-backed.
- Colony/designation rewrites remain high-risk and require narrow evidence.
- Nomad, Arkship, Waystation, and Wayline compatibility must be checked before
  readiness claims that touch relevant economy, colony, war, diplomacy, UI,
  starbase, automation, AI, or modifier behavior.

## T00 Conclusion

Strategic v2 can proceed to T01 static baseline validation. The active target is
4.4.5, the Director remains standalone, the required parents are explicit, and
current docs preserve the distinction between static proof and future runtime
observer proof.
