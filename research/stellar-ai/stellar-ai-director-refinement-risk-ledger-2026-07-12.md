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

Status: committed and pushed as `ff0d3d3a8ae42ab05250c449e4c59095adf20869`.

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

## H04 — Ship-upgrade budget eligibility

Status: committed and pushed as `93d1e0921b72a79b0e1a1649424287c8ada13e6d`.

Evidence:

- Vanilla permits the ship-upgrade category only at peace and when an owned
  fleet can actually be upgraded, with weight `0.2` and no desired minimum.
- The recovery baseline added `staid_fleet_buildup_economy_safe` as a hard
  potential requirement, so an unrelated runway judgment could suppress a
  legal upgrade even when the required resources existed.
- The verified 2270 save has higher serialized technology power than military
  power for every AI and no active ship queue, making legal upgrade reachability
  a required—but not sufficient—conversion path.

Decision:

Restore vanilla upgrade eligibility by removing only the broad runway veto.
Keep the peace requirement, owned-fleet controller check, `can_be_upgraded`,
vanilla weight, capacity modifier, and biological-ship modifier.

Top five risks and controls:

1. **Upgrades may consume alloys needed for new hulls.** Keep vanilla's lower
   `0.2` share and no desired minimum; compare upgrade and new-hull queues.
2. **Frequent design changes may create upgrade churn.** Track repeated upgrade
   orders and component/design errors before changing weight.
3. **Docked upgrading fleets may reduce readiness.** Preserve vanilla's
   peacetime-only condition and inspect war transitions.
4. **Modded components may require scarce strategic resources.** Let native
   affordability decide; do not grant or market-buy resources by script.
5. **Zero-fleet empires still cannot use this lane.** Treat template creation,
   new-hull demand, and shipyard execution as separate evidence paths.

Static acceptance:

- The upgrade object retains `is_at_war = no`, controller ownership, and
  `can_be_upgraded = yes`.
- It contains no `staid_fleet_buildup_economy_safe` potential veto.
- Generator output and checked-in artifact match; targeted tests and the
  static validator do not dirty the worktree.

Rollback boundary:

Revert only H04 if upgrade churn or economic damage appears. Do not re-close
new-hull spending from H03 as part of an upgrade-only rollback.

## H05 — Megastructure safety bypass from large stockpiles

Status: committed and pushed as `ee18d07a07c7e88008e121cbe85089c021f0e8e1`.

Evidence:

- `staid_high_scale_snowball_pressure` becomes true from any one of minerals
  above 25,000, energy above 50,000, or alloys above 15,000, plus later
  high-income/stockpile cases.
- That single signal bypassed recovery, basic runway, trade-capacity, war/naval,
  survival, and pause-new-project checks in megastructure prep, commit, and
  continuation state.
- The observed failure combined very large alloy holdings, six occupied
  constructors, several simultaneous megaprojects, and legal unclaimed systems.

Decision:

Large stockpiles no longer bypass megastructure safety state. Prep requires no
recovery state, basic runway, trade capacity, its explicit stockpile/income
floors, and peace or adequate naval use. Commit requires no short-runway core
deficit, basic runway, trade capacity, and peace or adequate naval use.
Continuation priority requires commit safety, no survival mode, and actual
surplus or resource-waste pressure. New-project pause conditions apply even to
large empires. Parent/base project weights remain; this changes only Director
bonuses and pauses.

Top five risks and controls:

1. **A rich late empire may start fewer valuable projects.** Preserve explicit
   prep income/stockpile floors and route weights; measure idle constructors and
   legal high-value candidates before relaxing safety.
2. **A useful unfinished stage may lose the Director continuation bonus.** Its
   parent/base weight remains. Require multi-checkpoint stall evidence before a
   bounded continuation-only exception.
3. **Trade-capacity safety may be irrelevant to a low-trade empire.** It is an
   upkeep/logistics headroom proxy, not a universal wealth target; review it
   separately if low trade but ample relevant runway blocks all projects.
4. **War gating may block a strategically necessary defense project.** Adequate
   naval use still permits prep/commit, while object-specific defensive weights
   remain. Do not create a generic wealth bypass.
5. **High-scale modifiers remain on non-safety routes.** Audit and remove those
   as separate H06 changes; H05 does not claim the broad trigger is gone.

Static acceptance:

- Prep, commit, continuation, and pause-new-project blocks contain no
  `staid_high_scale_snowball_pressure` bypass.
- Their explicit recovery/deficit/runway/trade/war/survival controls remain.
- PDX parsing, targeted tests, and the static validator pass without dirtying
  the worktree.

Rollback boundary:

Revert only H05 if safety-state reachability proves too restrictive. Do not
restore the generic budget or spam target from H01/H02.

## H06 — High-scale route multipliers on megaproject objects

Status: implemented on the research branch; static validation pending commit.

Evidence:

- Even after H05, route generation still added direct high-scale factors to
  early economy kilostructures, storage-cap projects, and every upgrade stage.
- Those factors operated on project `ai_weight` itself and could multiply a
  legal start or continuation from a single unrelated large stockpile.
- The same route table also supports technology objects, where restored
  high-scale unlock pressure is intentional and must not be removed wholesale.

Decision:

Filter `staid_high_scale_snowball_pressure` modifiers only when the generated
target is a megastructure. Remove the separate high-scale upgrade multiplier.
Keep technology-route high-scale modifiers, project technology factors,
time/lifetime value, safety gates, resource-waste pressure, and the bounded
continuation bonus.

Top five risks and controls:

1. **Valid rich-empires starts may receive less urgency.** Project technology,
   timing, lifetime-value, and route-ready factors remain; measure legal idle
   candidates before adding any bounded factor.
2. **Useful technology pressure might be removed accidentally.** Unit coverage
   explicitly proves that the early-kilo technology route still retains the
   high-scale modifier.
3. **Upgrade completion may slow.** Keep continuation factor `35` when H05's
   bounded continuation state is genuinely ready and resource-waste factor `8`.
4. **Copied megastructure objects may drift with parent updates.** Rebuild from
   current parent sources and compare object provenance before release.
5. **Resource-waste pressure can still prefer projects aggressively.** That
   trigger represents actual capped/unusable resources rather than mere scale;
   audit it separately if constructor saturation persists.

Static acceptance:

- No generated megastructure object contains a country-scoped high-scale
  modifier.
- Source route generation excludes it for both starts and upgrades.
- A technology route explicitly retains the high-scale modifier.
- PDX parsing, targeted tests, and the static validator pass without dirtying
  the worktree.

Rollback boundary:

Revert only H06 if route-level project selection becomes too weak. Do not
restore H05 safety bypasses or the H01/H02 generic reserve pressure.
