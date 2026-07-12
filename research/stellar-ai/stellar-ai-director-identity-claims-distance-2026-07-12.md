# Identity claims and war-distance preference

Target: Stellaris Pegasus 4.4.4 active stack. This slice changes only the three already-owned vanilla influence claim budgets. It does not create claims, casus belli, war goals, targets, declarations, or fleet orders.

## Behavior and evidence boundary

Resolved Conquest multiplies legal claim-budget weight by 1.15, its lead-secondary vector by 1.05, and Barbaric Despoiler by 1.10. The largest reviewed blended overlap is 1.265. Every modifier requires a conflict-free eligible identity, potential claims, safe basic-economy runway, peace, and no survival, recovery, catastrophic-collapse, or core-deficit short-runway state. Extermination receives no factor because total-war identities do not need claims. Defensive and diplomatic identities receive no negative factor, preserving defensive reconquest and mixed cases.

`WAR_DECLARATION_MAX_DISTANCE = 300` remains the outer candidate-consideration ceiling. `WAR_DECLARATION_MALUS_DISTANCE = 25` is where the engine begins preferring nearer targets; it is not a 25-hop expansion limit measured from an empire's home system. The verified script surface exposes no per-identity or per-target distance weight, so the global `300 / 25 / 0.05 / 0.5` policy is unchanged. Native claim scoring separately favors nearby border targets and retains its vanilla maximum claim distance.

## Top five risks and controls

1. **Influence crowd-out:** the existing boxed-in and capped-influence factors can already stack strongly. Control: identity factors are limited to 1.15/1.05/1.10, require safe runway, and add no new expenditure lane.
2. **Claims mistaken for execution:** more budget weight may still yield no valid target or declaration. Control: preserve `has_potential_claims`, native executor, legality, CB, war-goal, and declaration ownership; runtime acceptance measures claims and subsequent planner state separately.
3. **Total-war waste:** exterminators or swarms could spend influence on unnecessary claims. Control: no extermination or genocidal identity factor is added.
4. **Mixed-identity suppression:** negative diplomatic or defensive factors could prevent reconquest. Control: this slice uses positive conquest/despoiler preferences only and leaves all other identities at the parent weight.
5. **Distance overcorrection:** lowering the hard ceiling can stall large empires, while raising the near-distance malus globally can create remote wars. Control: retain the proven 300-hop ceiling and 25-hop preference threshold unchanged; no arbitrary empire-size cap is introduced.

## Proof and rollback

Static proof covers fixed-object ownership, additive bounded modifiers, safety gates, exclusion of extermination, unchanged global distance defines, generated-file currency, parser/reference validation, and absence of state mutation. It cannot prove which target the executable ranks or whether a funded claim becomes a declaration. Runtime acceptance records target distance, claim creation, influence reserve, preparation state, war goal, and declaration outcome.

Rollback is one fine-grained commit removing the three identity modifiers and the claim-budget file from the focused archetype overlay allowlist while retaining all prior economic, diplomatic, territorial, and strategy identity consumers.
