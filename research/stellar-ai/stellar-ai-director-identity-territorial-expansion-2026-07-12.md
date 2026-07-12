# Identity-specific territorial expansion budgets

Target: Stellaris Pegasus 4.4.4 active stack. This slice modifies only the Director's existing native outpost budget pair: `alloys_expenditure_starbases_expand` and `food_expenditure_starbases_expand`.

## Behavior

Resolved primary Gestalt Growth receives a 1.25 allocation preference; Defensive and Conquest receive 1.15; Extermination receives 1.10. If the single resolved lead-secondary vector is one of those four lanes, it contributes 1.05. Primary and same-vector secondary cannot overlap by classifier contract. The maximum primary-secondary product is 1.3125.

The alloy and biological-food variants receive exactly the same identity clauses. Native expansion-plan presence, influence above 75, fallen/awakened-empire exclusions, bioship routing, wilderness terraforming exclusion, desired minima, and resource affordability remain unchanged. At `highest_threat >= 50`, the existing 0.5 modifier still dominates directionally: even maximum identity overlap yields only 0.65625 of the calm base allocation.

## Top five risks and controls

1. **Runaway expansion starving other lanes:** identity could turn a preference into a permanent reserve. Control: weight-only factors; no desired-min increase, hard empire-size target, free influence, or forced construction.
2. **Primary-secondary overcount:** the same identity could multiply twice. Control: resolved primary triggers plus the single lead-secondary classifier; structural tests verify lead-secondary excludes the same primary and bound the maximum product.
3. **Expansion under threat:** identity could erase the defensive threat reduction. Control: the existing 0.5 high-threat multiplier remains; worst overlap is still below calm allocation.
4. **Bioship/alloy asymmetry:** biological empires could receive different strategic behavior because their outposts use food. Control: exact shared modifier text and weight parity tests across both expenditure objects.
5. **Planner/executor mismatch:** more allocation may not create an outpost order when candidates or constructors are unavailable. Control: native `has_ai_expansion_plan`, candidate selection, pathing, influence, and executor remain authoritative; runtime proof tracks orders rather than inferring success from budget.

## Proof and rollback

Static validation proves source hashes, fixed output ownership, unchanged potential and desired-min fields, exact alloy/food symmetry, bounded composition, and absence of events/orders/free resources. It cannot prove which system is selected or whether the construction executor acts. Runtime acceptance uses the existing copied-save expansion evidence tool to compare legal candidates, constructor orders, budget state, and completed outposts.

Rollback is one fine-grained commit restoring the prior threat-softened native outpost budget without affecting diplomatic or economic identity consumers.
