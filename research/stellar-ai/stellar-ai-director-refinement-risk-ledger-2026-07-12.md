# Stellar AI Director Refinement Risk Ledger

Date: 2026-07-12  
Runtime evidence baseline: Stellaris Pegasus 4.4.4 (`5505`)  
Source baseline: `78627926b7e99bdfba8c14f6c047061a5e24db8e`  
Research branch: `codex/stellar-ai-director-research-refinements`

This is the durable risk and rollback record for the post-recovery refinement
series. Current source, current active-stack winners, verified saves, and
targeted tests outrank historical reports. Runtime outcomes remain hypotheses
until the user tests a deliberately installed research build.

Each hook must record five concrete failure modes before promotion. Acceptance
is opportunity-based: a legal, affordable native lane should act without a
universal quota or a scripted order.

## H01 — Generic megastructure alloy-budget ownership

Status: committed and pushed as `d3c61a3a525826fda2976cb35dec897a6a83105c`.

Evidence:

- Installed vanilla 4.4.4 gives `alloys_expenditure_megastructures` weight
  `0.4`, an unfinished-project factor of `3`, no `desired_min`, and a
  `desired_max` of `20000`.
- The recovery baseline replaced it with weight `8`, multiplicative prep,
  commit, technology, and time factors, a base `desired_min` of `25000`, and
  reserve maxima that can reach millions of alloys.
- The observed empire had legal unclaimed systems while construction ships
  traversed or worked elsewhere. Earlier save inspection found all six
  constructors occupied by habitats, a Dyson Swarm, and four Deep Space
  Citadels.
- The verified 2270 save contains 103,754 alloys across ten AI empires and 97
  idle simultaneous shipyard slots. This proves that global alloy reservation
  did not convert wealth into a balanced set of native actions.

Decision:

The Director no longer defines `alloys_expenditure_megastructures`. Vanilla or
the active parent mod owns the generic reserve. Director route weights may rank
specific legal projects, and Gigas special-resource budgets remain separate.
No constructor orders are cleared and no outpost is forced.

Top five risks and controls:

1. **Expensive Gigas stages may be underfunded.** Preserve parent budget
   ownership, Gigas special-resource lanes, and object-specific continuation
   weights; test unfinished-stage progress separately from new starts.
2. **An unfinished project may stall after the reserve falls.** Vanilla already
   raises the generic weight for upgradeable projects. Acceptance requires
   observing legal continuation over multiple checkpoints before adding any
   bounded continuation-only reserve.
3. **Another late-loading mod may become an unsafe winner.** Reconstruct the
   active `common/ai_budget` winner with Irony before public release; do not
   assume that removing Director ownership always means vanilla wins.
4. **Freed alloys may feed fleets but not territorial expansion.** Track
   constructor availability, starbase budget share, influence, route legality,
   candidate score, shipyard utilization, and fleet queues independently. Do
   not treat one improved lane as proof that the others are fixed.
5. **Existing save orders may mask the change for years.** Do not cancel or
   rewrite queued construction. Evaluate only newly selected orders after
   current projects finish, and compare a continued save with a fresh campaign
   before changing weights again.

Static acceptance:

- The generated Director alloy-budget file contains ship and upgrade objects
  but no top-level `alloys_expenditure_megastructures` object.
- Generator output and the checked-in artifact are identical.
- PDX parsing and the repository static validator pass without changing the
  worktree.

Rollback boundary:

Revert only the H01 commit. Do not restore the former weight-8/multi-million
reserve wholesale; if runtime evidence proves underfunded continuations, add a
new continuation-only slice with its own five-risk review.

## H02 — Global scaling megastructure income target

Status: committed and pushed as `d8899d5e16af12ac80c6332d7086447baa5b0039`.

Evidence:

- `basic_economy_plan` contained a scaling subplan named `Stellar AI Director
  megastructure spam reserve`.
- It activated when either `staid_megastructure_commit_safe` or the broad
  `staid_high_scale_snowball_pressure` trigger was true.
- It requested alloy income `8000`, energy `8000`, minerals `5000`, trade
  `1000`, and three Gigas strategic-resource incomes of `10`, irrespective of
  actual project cost, consumption, or constructor availability.
- The verified 2270 save showed homogeneous resolved resource targets across
  every personality and a fleet-conversion failure despite large stockpiles.

Decision:

Remove only the global scaling spam subplan. Keep the small prep-gated `mega
alloy reserve`, the separate Gigas special-resource reserve, active-parent
budget ownership, and route-specific project/continuation weights. This slice
does not claim that the remaining economic plan is personality-aware.

Top five risks and controls:

1. **A genuinely expensive project may not induce enough production.** Keep
   project-specific gates and special-resource support; add a bounded
   cost-backed target only after observed continuation starvation.
2. **An active stage may lose support mid-build.** Construction costs are paid
   at start, while upkeep and later stages remain visible to parent and route
   logic. Test continuation at checkpoints instead of restoring a global goal.
3. **Broad high-scale bypasses still affect other hooks.** Treat their removal
   from prep, commit, and new-start weights as a separate rollback slice; H02
   alone is not proof that megaproject saturation is fully solved.
4. **Homogeneous base targets may still erase personality differences.** The
   archetype/economic-mode redesign must measure final merged targets and
   enforce mutually exclusive modes rather than stacking more subplans.
5. **A loaded save may retain cached economic-plan state temporarily.** Compare
   resolved targets after the engine's normal recalculation window and include
   a fresh-campaign checkpoint before drawing a causal conclusion.

Static acceptance:

- Neither generator output nor the checked-in plan contains the spam subplan.
- The small prep reserve and Gigas special-resource reserve remain present.
- Generator output and the checked-in plan are identical.
- Targeted parsing/tests and the repository static validator pass without
  changing the worktree.

Rollback boundary:

Revert only the H02 commit. Never restore the fixed `8000/8000/5000` scaling
vector without evidence that those simultaneous incomes match real demand.

## H03 — Ship-budget eligibility and high-capacity damping

Status: implemented on the research branch; static validation pending commit.

Evidence:

- The recovery baseline changed vanilla `alloys_expenditure_ships` from
  `potential = { always = yes }` to a hard eligibility gate requiring either
  the first ten years, a narrow emergency, or full economic runway below the
  80% peacetime naval-capacity guard.
- In the verified 2270 save, nine of ten AIs have less than 2,000 military
  power, five have less than 1,000, and two have no combat fleet.
- The ten AIs hold 103,754 alloys with positive aggregate income, but all 97
  simultaneous shipyard slots are idle and no military ship is queued.
- Several aggressive empires are at only 21–43% estimated naval capacity, so
  their failure cannot be explained by the 80% guard alone. A hard economy
  potential can close the ship lane despite abundant relevant resources.

Decision:

Restore the native always-available ship category. Preserve vanilla base,
war/crisis, over-capacity, and biological-ship weights. At 80% used naval
capacity, apply a factor of `0.25` through the existing cautious 4.4.4 guard
instead of making the category ineligible. This slice does not add personality
bonuses or force fleet templates, reinforcement, or construction orders.

Top five risks and controls:

1. **Weak economies may overbuild and incur unsustainable upkeep.** Retain the
   vanilla base weight and affordability system; add no new low-cap multiplier
   in this slice, and measure upkeep/runway alongside fleet growth.
2. **The 4.4.4 high-capacity declaration defect may reappear.** Keep a strong
   0.25 peacetime share factor at 80% and preserve a separate 4.4.4 rollback.
   Do not remove it based only on unverified 4.4.5 notes.
3. **The shared category may prioritize civilian science ships.** That is
   native behavior and prevents opening exploration deadlock; telemetry must
   separate civilian and military queue utilization.
4. **Biological fleets may not be alloy-limited.** Preserve vanilla's
   biological alloy factor and evaluate food income/upkeep before adding any
   archetype pressure.
5. **Budget eligibility may not create fleet-template demand.** Record template
   targets, reinforcement queue, shipyard utilization, and actual military
   power. If queues remain empty, fix the strongest verified native demand
   surface rather than multiplying the budget blindly.

Static acceptance:

- The ship object contains `always = yes` and no runway or `NOT guard`
  potential veto.
- The 0.25 high-capacity factor and guard are present in the weight block.
- Vanilla war/crisis and biological modifiers remain.
- Generator output and checked-in artifact match; targeted tests and the
  static validator do not dirty the worktree.

Rollback boundary:

Revert only the H03 commit to restore the hard 80% shutdown. If runtime upkeep
fails, adjust the bounded weight factor in a new slice instead of restoring all
economic runway vetoes.
