# Stellar AI Director: Research-First Economic Controller Model

Date: 2026-07-11  
Target behavior: Stellaris 4.4.x Stellar AI Director  
Status: offline design model only; this work does not alter the live mod

## Purpose

This model tests whether a banded Stellaris economic plan can approximate a
ratio-based strategy without creating a sprawling set of disconnected static
targets. The governing doctrine supplied by the user is:

- research is the primary snowball mechanism and should be pushed continuously;
- total research income should be at least twice the sum of positive ordinary
  net incomes;
- energy and consumer goods must support research growth;
- food normally needs only a small positive margin;
- minerals receive extra emphasis during early aggressive expansion;
- alloys gain relative emphasis from the midgame onward and during war;
- survival deficits may interrupt research, but resource surpluses must not
  become unlimited sinks.

The simulator is deliberately independent of Stellaris. It tests the controller
math before that math is translated into the discrete economic-plan bands that
the game supports.

## Model contract

For each simulated month, the controller may allocate a scenario-defined number
of abstract investment units. Each unit increases one income lane by that
scenario's marginal increment. The controller recalculates all targets after
every unit, so one lane cannot consume the entire monthly allocation while a
more urgent lane deteriorates.

The ordinary-resource sum is:

```text
O = max(energy, 0) + max(minerals, 0) + max(food, 0)
  + max(consumer_goods, 0) + max(alloys, 0) + max(unity, 0)
```

The research target is:

```text
research_target = max(phase_research_floor, 2 × O)
```

Research support targets are:

```text
energy_target = max(phase_energy_floor, 0.15 × research)
consumer_goods_target = max(phase_consumer_goods_floor, 0.03 × research)
```

The 0.15 and 0.03 coefficients are explicit model parameters based on the
project's current abstract research-capacity assumptions. They are not claimed
to be Stellaris engine constants and must be calibrated against observer saves
before implementation.

Normal food targets 10 net income. Bio-ship scenarios target 50 because food is
also a military production input for those empires. Early aggressive expansion
multiplies the mineral floor by 1.75; later expansion uses 1.25. War multiplies
the alloy floor by 1.5.

## Phase floors

| Phase | Energy | Minerals | Food | Consumer goods | Alloys | Unity | Research |
|---|---:|---:|---:|---:|---:|---:|---:|
| Early | 40 | 120 | 10 | 30 | 60 | 30 | 300 |
| Mid | 100 | 150 | 10 | 60 | 250 | 80 | 1,200 |
| Late | 250 | 200 | 10 | 120 | 600 | 150 | 4,000 |

These floors are guardrails, not desired surplus ratios. Once a non-research
lane is safe and above its applicable floor, its ordinary score falls to zero.
Research remains active until it reaches the 2:1 target.

## Allocation and cross-band safeguards

Each lane's base urgency is its proportional shortfall from its current target.
Research receives the strongest ordinary priority. Energy and consumer goods
receive the next-highest priority because they support research. Minerals and
alloys receive phase-dependent multipliers; food and unity do not receive a
surplus-seeking multiplier.

Three rules prevent the principal failure modes:

1. Negative energy, consumer goods, or food receives an emergency score that
   interrupts ordinary research competition.
2. The controller checks whether the *next* research increment is supportable.
   If not, research pauses and energy or consumer goods receives a one-step
   look-ahead target. This avoids a deadlock where science is blocked but its
   support lanes see no present shortfall.
3. If every lane has a zero score, the controller leaves capacity idle. It does
   not invest merely because an allocation slot exists.

## Scenario results

The source inputs are in
`stellar-ai-economic-model-scenarios-2026-07-11.csv`. The full monthly record is
in `stellar-ai-economic-model-timeline-2026-07-11.csv`; the compact results are
in `stellar-ai-economic-model-summary-2026-07-11.csv`.

| Scenario | Final research / ordinary | 2:1 met | Support safe | Key behavior |
|---|---:|:---:|:---:|---|
| Early balanced | 2.0218 | Yes | Yes | Research resumed after support growth |
| Early expansion | 2.0312 | Yes | Yes | 12 mineral vs. 4 alloy investments |
| CG constrained | 2.0170 | Yes | Yes | 7 CG investments repaired the constraint |
| Energy constrained | 2.0101 | Yes | Yes | 22 energy investments repaired the constraint |
| Food surplus trap | 2.0041 | Yes | Yes | Zero additional food investment |
| Food deficit recovery | 2.0152 | Yes | Yes | Four food investments ended the deficit at +13 |
| Midgame fleet pivot | 2.0000 | Yes | Yes | 25 alloy investments, then research |
| Rich wartime research | 2.0000 | Yes | Yes | Existing safety allowed pure research investment |
| Late research scale | 2.0102 | Yes | Yes | Support and research scaled without basic surplus chasing |
| Bio-ship burden | 2.0090 | Yes | Yes | Food floor and wartime alloy demand both remained active |

The pre-fix run also supplied useful negative evidence. The support check could
block the next research increment while current energy and consumer-goods
targets were already satisfied, producing permanent idle capacity. Adding the
one-step support look-ahead resolved that failure. This regression is retained
in the automated tests.

The food-surplus scenario begins at +775 food. The controller cannot erase
existing surplus income in this simplified model, so `food_overproduction`
remains true, but it directs **zero** new investment to food and raises research
until the 2:1 ratio is restored. A future live implementation needs separate
reassignment/demolition restraint logic if it is expected to unwind existing
production rather than merely stop adding to it.

## Translation strategy for Stellaris economic plans

The eventual mod should use a small number of coordinated bands rather than a
large Cartesian product of resource conditions:

1. Phase floors provide early, mid, and late safety baselines.
2. Emergency support bands activate only for actual negative or unsafe
   energy/CG/food conditions.
3. Research bands step upward whenever support is safe.
4. Mineral and alloy bands change with phase, expansion pressure, and war.
5. Every higher research band must carry matching forward energy/CG support
   requirements so the engine cannot enter the deadlock found by this model.
6. Food bands stop at a low normal ceiling, with a distinct bio-ship exception.

This is more manageable than independently targeting every possible income
combination: the bands implement a state machine with explicit priority and
support invariants, while this simulator checks the intended ratio across
representative starting states.

## Validation and limitations

Automated tests require:

- all modeled support-deficit scenarios recover and finish at or above 2:1;
- a pre-existing food surplus receives no new food investment;
- a food deficit is repaired without creating a large normal surplus;
- early expansion favors minerals over alloys;
- midgame war favors alloys over minerals;
- ordinary non-bio scenarios that begin at or below +50 food remain at or below
  +50.

This is not a game-engine simulation and does not prove runtime AI behavior. It
does not model pops, jobs, planet slots, build times, market trades, stockpile
spending, technology unlocks, designation selection, conquered-world
reassignment, or mod conflicts. Investment increments are scenario parameters,
not literal buildings. Runtime saves must calibrate the coefficients and prove
that Stellaris's native planner follows the translated bands.

No production mod change should be made from this model alone. The next step is
to review the policy, agree on the phase floors and support coefficients, then
map the accepted controller to the smallest set of native economic-plan bands
and validate their merged winners before a fresh observer test.

