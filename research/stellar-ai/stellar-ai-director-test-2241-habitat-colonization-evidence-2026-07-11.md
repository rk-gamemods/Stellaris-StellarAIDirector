# Stellar AI Director TEST_2241 Habitat Colonization Evidence

## Scope

- Target: Stellaris PC Pegasus 4.4.4 (5505), Stellar AI Director.
- Save: `test_2241.02.27.sav` from the United Cevantian Nation campaign.
- Symptom: three completed habitats in Procyon, Sirius, and Tahlin remained
  unoccupied for years.
- Runtime boundary: existing save and logs were inspected read-only; Stellaris
  was not launched and no observer commands were enabled.

## Save evidence

Country 0 is AI-controlled and has three native type-1 colonization strategies:

| Planet | Planet ID | Class | Strategy target | Habitability value |
| --- | ---: | --- | ---: | ---: |
| Procyon Habitat | 2206 | `pc_habitat` | 87 | 80 |
| Sirius Habitat | 2207 | `pc_habitat` | 87 | 80 |
| Tahlin Habitat | 2208 | `pc_habitat` | 87 | 80 |

All three habitats are unowned, lie in systems controlled by country 0, and
have persisted since well before the 2241.02.27 checkpoint. Country 0 owns a
valid auto-generated `colonizer` design but has no colony ship. It has one
shipyard starbase and ample liquid resources: about 29.4k alloys, 30.8k food,
31.1k consumer goods, 39.7k energy, and 13.0k minerals. Monthly income is
positive in every core resource.

This proves that habitat candidate discovery is working. The stall occurs after
native plan creation, in the funding/build path.

## Root cause and narrow correction

Commit `66fac553` replaced vanilla's pre-midgame wartime exclusion in
`alloys_expenditure_colonies_expand` while preserving the native
`ai_colonize_plans`, species, income, resource, weight, and desired-min/max
gates. Commit `96bdd713` later added a Director-only composite wartime safety
gate. That extra gate can veto already-valid native plans and is not required to
protect candidate selection or affordability.

The correction removes only the Director-specific war-state gate and its now
unused scripted trigger. It does not create plans, force colonization, grant
resources, alter habitat objects, or change food/consumer-goods/mineral/energy
colony budgets.

## Runtime and source evidence

- Matching `error.log` and `game.log` timestamps precede the save by less than
  one minute.
- Runtime duplicate-object output confirms
  `common/ai_budget/zzzzz_staid_19_wartime_colony_alloy_budget.txt` is the loaded
  winner for `alloys_expenditure_colonies_expand`.
- No runtime error names that budget file, its object, or the removed scripted
  trigger.
- Current vanilla `common/ai_budget` was indexed and verified against Pegasus
  4.4.4 before comparison.

## Knowledge-base evaluation

The local knowledge base was useful for confirming the 4.4.4 build identity and
locating the exact colony alloy budget object. It was not sufficient for this
diagnosis: `ai_colonize_plans` returned no results, the budget dossier had no
claims or relations, and broad habitat searches were noisy. A future evidence
packet should connect native colonization strategies, `ai_colonize_plans`, the
multi-resource colony budget pipeline, colonizer designs, and shipyard
construction.

## Validation plan

1. Regenerate the mod and verify no unexpected generated churn.
2. Parse the generated budget and scripted-trigger files.
3. Run the focused colony-budget regression test and the full Director suite.
4. Run the static Director validator and Git diff checks.
5. In a future user-approved runtime continuation, load the corrected mod and
   observe whether a colony ship is built for planet 2206, 2207, or 2208.
