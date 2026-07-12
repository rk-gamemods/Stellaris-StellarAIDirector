# Stellar AI Director — Pegasus 4.4.4 Native War-Planning Replacement

Date: 2026-07-10  
Target: Stellaris PC 4.4.4 “Pegasus”  
Working behavioral reference: Stellar AI 0.10, Workshop `3610149307`

## Replacement Contract

This layer replaces the Director’s contradictory war-planning configuration as one native system. It does not declare wars, create claims or casus belli, create armies, grant resources, force diplomacy, or issue fleet attack/movement orders. Stellaris still owns target selection, legal CB and war-goal selection, preparation, declaration, transport/invasion execution, and fleet missions.

The implementation retains Director’s high-scale economic, research, crisis, megastructure, Gigastructures, NSC3, ESC NEXT, Starbase Extended, Planetary Diversity, Nomad/Arkship, and Universal Resource Patch lanes. Only the war-planning envelope and its immediate budget/posture dependencies are replaced.

## Native Chain

1. **Country-type readiness:** `default` has no `min_navy_for_wars` field and has `min_assault_armies_for_wars = 0`. Armies are useful logistics, never a declaration prerequisite.
2. **Complete personalities:** 20 Pegasus 4.4.4 personality objects are copied wholesale. Only `aggressiveness`, `bravery`, and `military_spending` are substituted from Stellar AI 0.10; behavior flags, diplomatic acceptance, design preferences, and personality selection remain 4.4.4 vanilla.
3. **Temporary opening:** the Director’s economic opening remains long-lived, but the diplomatic opening is bounded to the first 40 years and exits immediately for war or physical containment.
4. **Boxed-in breakout:** `has_ai_expansion_plan = no` activates a native boxed-in pressure proxy before the old five-colony cutoff. It raises Belligerent/Supremacist posture, claim expenditure, army reserve, and war logistics. The engine’s boxed-in declaration multiplier and legal claim/CB scoring still choose the target.
5. **Army recruitment:** native mineral army budgets receive a small uncapped reserve: 200 base, +300 boxed in, +300 conquest/raiding, and +500 at war or under existential threat. No `desired_max` is used.
6. **Budget competition:** vanilla planet-budget base weights remain `1.0`, `0.8`, and `0.6`, but receive a `0.65` factor while war logistics are active so construction does not consume the entire mineral budget.
7. **High naval capacity:** normal peacetime new-ship budget share falls to 25% at 80% used naval capacity but remains eligible, so the workaround no longer freezes weak absolute fleets. `AI_NAVAL_CAP_SCORE_MULT` remains at vanilla `15`.
8. **Declaration envelope:** global war defines return to the working native range: 12–30 months preparation, base aggression 25, enemy-fleet multiplier 1.2, maximum distance 50, declaration minimum 0.5, and offense/defense allotment 1.0. Only boxed-in multipliers remain modestly above vanilla at 8 and 12.

## Cevantia / Pobbma Behavior

United Cevantian Nation is handled as an AI actor even though it is country 0 in an observer run. Its lack of an expansion plan activates boxed-in pressure regardless of empire size. Its existing Pobbma claim, legal CBs, Belligerent/Unrestricted posture, strong fleet, and Ruthless Capitalist conqueror/subjugator/opportunist flags then feed the native planner. No special case names country 0, Cevantia, Nosakoa, or Pobbma.

## Provenance

Every copied full-object override in this package is enumerated in:

`research/stellar-ai/stellar-ai-director-war-planning-444-provenance-2026-07-10.csv`

That inventory covers all 20 personalities, `default`, the three copied policy objects, the army/planet/ship/megastructure budget objects, and the global `NAI` define group.

## Hardcoded Limits

- Pegasus 4.4.4 does not expose the later executable repair for “AI not declaring war if naval capacity is too high.” The 80% peacetime construction guard is a fresh-game native workaround, not a backport of the executable fix.
- No verified 4.4.4 script surface assigns extra target score specifically to “the empire whose closed border blocks my only route.” The implementation raises the native boxed-in state, posture, claims, and logistics; the executable still chooses the exact target and decides whether closed-border reachability is acceptable.
- Native army demand, transport assembly, invasion confidence, and war-goal selection remain executable-owned. Budgets make useful armies affordable but do not force a number or type.
- The observed science-ship/MIA loop at Pobbma is an automation/pathfinding defect and is not solved by war-planner data.

## Acceptance Gate

Run one fresh 4.4.4 observer game with the normal playset for roughly 20–30 years. Confirm multiple ordinary wars, at least one strong boxed-in empire selecting and attacking its blocking neighbor, useful but non-excessive offensive armies, and a functioning economy.
