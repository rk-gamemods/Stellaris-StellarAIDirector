# Stellar AI Director Megastructure Reserve And Continuation Contract

Date: 2026-07-09

Task card: T14 - Megastructure reserve and continuation contract

## Scope

This note validates the current static reserve and queue-continuation surfaces for
Stellar AI Director strategic v2. It does not claim runtime efficacy. Runtime
proof remains deferred until the observer phase is eligible under the packet
contract.

## Static Reserve Findings

- Alloy megastructure reserve is a full-object override at
  `mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt:7`.
  It applies only to default countries that can build megastructures and are not
  in `staid_pause_new_megastructure`.
- The alloy budget starts at `weight = 8`, increases for prep-ready, commit-safe
  upgrade opportunities, Mega Engineering, and year 80+, and reduces during
  survival mode. Evidence:
  `mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt:18`.
- The alloy reserve target is intentionally high scale: desired minimum starts
  at 25,000 alloys, adds 100,000 for prep-ready, adds 250,000 for commit-safe
  owned upgradeable megastructures, and adds 500,000 after year 120. Desired
  maximum reaches substantially higher late-game reserve caps. Evidence:
  `mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt:39`.
- Gigas special-resource budgets reserve `giga_sr_sentient_metal`,
  `giga_sr_negative_mass`, and `giga_sr_amb_megaconstruction` for
  megastructure categories/upkeep. They reduce or pause during survival and
  recovery states, then increase under `staid_megastructure_commit_safe`.
  Evidence:
  `mods/StellarAIDirector/common/ai_budget/zzz_staid_gigas_resource_budgets.txt:6`.
- The additive economic plan supplies reserve income pressure at multiple
  scales: midgame megastructure rush after year 45, crisis-scale giga rush after
  year 80, planetcraft survival curve after year 120, pathological snowball
  reserve, construction spenddown reserve, megastructure spam reserve, mega
  alloy reserve, and Gigas special-resource reserve. Evidence:
  `mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt:132`
  and
  `mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt:325`.

## Continuation Findings

- `staid_megastructure_prep_ready` requires non-nomadic country state,
  megastructure construction ability, recovery/runway/trade-capacity safety or
  high-scale snowball pressure, 8,000+ alloy stockpile, positive energy/mineral
  income, 80+ monthly alloy income, and adequate war posture. Evidence:
  `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt:164`.
- `staid_megastructure_commit_safe` is a softer continuation gate than prep:
  it requires megastructure construction ability, no short-runway core deficit
  unless high-scale snowballing, basic economy safety, trade/capacity safety,
  and adequate war posture. Evidence:
  `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt:190`.
- `staid_megastructure_continuation_priority_ready` requires commit safety and
  a reason to continue: surplus sink, resource waste, or high-scale snowball
  pressure, while avoiding survival-mode continuation unless snowballing.
  Evidence:
  `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt:212`.
- `staid_pause_new_megastructure` blocks new megastructure starts during
  survival mode, low-naval-cap wars, or high threat with weak naval posture,
  unless high-scale snowball pressure is active. Evidence:
  `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt:225`.
- Generated megastructure starter objects use route-specific build-priority
  gates, while generated upgrade/continuation stages repeatedly apply
  `factor = 35` under `staid_megastructure_continuation_priority_ready`.
  Evidence examples:
  `mods/StellarAIDirector/common/megastructures/zzzz_staid_03_megastructures_megastructures.txt:222`,
  `mods/StellarAIDirector/common/megastructures/zzzz_staid_03_megastructures_megastructures.txt:1077`,
  `mods/StellarAIDirector/common/megastructures/zzzz_staid_03_megastructures_megastructures.txt:4345`,
  `mods/StellarAIDirector/common/megastructures/zzzz_staid_03_megastructures_megastructures.txt:4901`,
  `mods/StellarAIDirector/common/megastructures/zzzz_staid_03_megastructures_megastructures.txt:5045`,
  and
  `mods/StellarAIDirector/common/megastructures/zzzz_staid_03_megastructures_megastructures.txt:5154`.

## Reference And Parse Validation

- `python tools/validate_stellar_ai_director_patch.py` passed.
- JData `stellar_ai_director_generated_reference_audit_20260704` validates with
  3,779 rows and zero rows where `status != ok`.
- JData reference rows confirm the reserve/continuation files resolve the
  relevant resources and scripted triggers:
  `alloys`, `giga_sr_sentient_metal`, `giga_sr_negative_mass`,
  `giga_sr_amb_megaconstruction`, `staid_megastructure_prep_ready`,
  `staid_megastructure_commit_safe`, and
  `staid_megastructure_continuation_priority_ready`.
- JData `stellar_ai_director_generated_file_audit_20260704` validates with 42
  generated files.

## Queue-Continuation Runtime Proof Method

When live observer testing becomes eligible, each checkpoint packet under
`research/stellar-ai/observer-runs/` should preserve enough evidence to decide
whether reserve and continuation logic is actually producing queue momentum.
The observer run should record:

- year/date, empire, authority/civics/ethics, war state, subject/federation
  state, and whether hidden economic bonuses are disabled;
- total research per month plus physics/society/engineering breakdown;
- alloy income, alloy stockpile, energy/mineral/consumer-goods/food deficits,
  and special-resource income/stockpiles for Gigas resources;
- fleet count, total fleet power, naval cap usage, active wars, losses, and
  whether naval pressure is starving megastructure reserves;
- owned megastructures by type/stage, upgradeable megastructures, active build
  queues, recently completed stages, stalled stages, and whether continuation
  resumes after temporary survival/recovery states;
- relevant route unlocks: Mega Engineering, Mega Shipyard, Science Nexus or
  Think Tank path, Gigas kilostructures, planetcraft, war moon, systemcraft, and
  special-resource techs;
- colony count, pop count, research worlds/planetary computers, open jobs,
  unemployment, and construction backlog;
- evidence artifacts: logs, saves, screenshots, checkpoint JSON/CSV, summary
  Markdown, and any extracted data from
  `tools/stellar_ai_observer_loop.py` or
  `tools/extract_stellar_ai_checkpoint.py`.

Static success for this task means the reserve and continuation gates are
parseable, referenced, route-connected, and documented. Runtime success is not
proven until an eligible observer run shows at least one AI maintaining safe
economy/fleet posture while continuing megastructure stages and reaching the
packet's 3,000+ monthly research target before 2350.

## Decision

No gameplay patch is warranted from T14 static evidence. The current reserve
and continuation surfaces are coherent and reference-clean. The remaining work
is runtime proof during the final observer phase, not speculative static
rewriting.
