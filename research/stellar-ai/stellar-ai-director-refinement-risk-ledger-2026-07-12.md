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

Status: committed as `f2ff08848d3156f53ff982ee0acde15e6bd9fc9f`.

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

## H07 — Native outpost budget availability beside colonization

Status: implemented and committed on the research branch at `75bca24e`;
focused static validation passed, with copied-save runtime continuation still
pending.

Evidence:

- The integrity-verified `2270.04.15` save copy has SHA-256
  `7E49527196CAA35DCCD5FB22FF24E77C08A1EEA84C9263A52E87DF95492784B7`.
- Paunaby (system 10/star 221), Aerea (70/1186), and Zosma (96/329)
  remain unowned, surveyed, unrestricted type-19 native expansion candidates.
- Country 0 has thirteen constructors, eleven of them idle, and no outpost
  order. Executor saturation explains 2255-2257 but is no longer the immediate
  2270 gate between recognized candidate and assigned construction order.
- The one type-1 record is for planet 2, already owned by country 0 with
  `colonize_date="2270.01.26"`; the save date is `2270.04.15`.
- The vanilla alloy outpost potential puts both country-type exclusions and
  `ai_colonize_plans > 0` inside one multi-statement `NOT`. Its exact runtime
  semantics were not proven by generated docs or CWTools. The biological food
  analogue uses an explicit `NOR`, proving that colonization-plan ineligibility
  is at least the source's intended paired behavior.
- This save predates H01-H06 and the live descriptor switch, so it cannot prove
  the corrected megastructure pressure or this new availability hook at runtime.

Preserve native expansion-plan recognition, system scores, target selection,
pathing, threat limit, influence reserve, biological-ship rule, wilderness
terraforming exclusion, base weights, and desired minima. For the alloy lane,
normalize the ambiguous multi-statement `NOT` to an explicit country-type
`NOR`. For both alloy and biological-food lanes, move only the colonization-plan
condition from eligibility to a factor `0.25` weight modifier. This creates a
bounded allocation signal; it does not promise a scheduler ratio or an outpost.

Top five risks:

1. **A valid colony ship may compete with an outpost in a constrained economy.**
   Keep the outpost weight at one quarter while a colonization plan exists and
   retain all native resource reserves; compare colony and outpost completion
   in low-resource runtime cases before promotion.
2. **The ambiguous alloy `NOT` may not be the actual engine blocker.** The save
   isolates the planner-to-order gap but not executable internals; keep H07 as a
   separate rollback commit and require continuation evidence.
3. **Biological or wilderness empires may lose a parent safeguard.** Generate
   from the version-identified food object and prove the bio requirement plus
   wilderness/terraform exclusion survive byte-for-byte apart from one clause.
4. **A stale expansion plan may fund a low-value outpost.** Native scoring,
   legality, pathing, influence cost, and target ownership remain unchanged;
   this hook creates no target and issues no order.
5. **Eligibility may still fail to produce execution.** Static validation proves
   only that both resource lanes can fund a legal outpost. Runtime proof needs a
   serialized outpost order or completed claim with an idle constructor.

Static acceptance:

- Generated alloy and food objects match their 4.4.4 sources except for the
  explicit alloy `NOR`, removal of the colonization eligibility clause, and the
  paired factor-0.25 weight modifiers.
- Pinned source hashes and an active-playset scan fail generation if vanilla
  drifts or any enabled parent mod begins overriding either budget object.
- Threat, influence, country-type, biological, wilderness-terraform, weight,
  and desired-min markers remain under regression coverage.
- No constructor cap, scripted target/order, `clear_orders`, free resource, or
  forced claim is added.
- PDX parsing, focused recovery tests, known-object validation, JData provenance
  validation, static validator, and clean-worktree checks pass before commit.

Rollback boundary:

Revert only H07 if colony completion regresses or no outpost opportunity appears.
Do not restore H01-H06 megastructure pressure or the removed order watchdog.

## H08a — Deterministic nation identity and bounded policy model

Status: implemented as an offline model and fixture surface; no production mod
consumer or gameplay weight is connected in this slice.

Evidence:

- Pegasus 4.4.4 `common/personalities/00_personalities.txt` has SHA-256
  `1F89C8D6C9444F575526A8635DB59DF78140AD43401538214E6B62F685298BAA`.
  All 30 normal/global personality IDs are either assigned a reviewed anchor or
  explicitly recorded as outside the seven primary anchors.
- The integrity-verified `2270.04.15` save has SHA-256
  `7E49527196CAA35DCCD5FB22FF24E77C08A1EEA84C9263A52E87DF95492784B7`.
  Its ten AI candidates classify from identity fields alone as three
  extermination, four conquest, one defensive, one research, and one
  diplomatic. It supplies no ordinary gestalt-growth or balanced primary, so
  those remain synthetic adversarial fixtures.
- The model keeps the engine-selected personality anchor separate from ethics,
  civics, government, authority, origin, perks, and source-resolved behavior
  evidence. Primary identity is mutually exclusive for presentation, while the
  full evidence vector and ordered secondaries remain available to consumers.
- Dynamic observations use explicit unknown states. Fleet absence, missing
  templates, filled templates, naval headroom, shipyard use, tracked resource
  capacity, and tracked resource use are separate facts. Static identity never
  depends on military power, technology power, stockpiles, income, queues, or
  observed outcomes.
- Policy output is a bounded five-level category over the existing twelve model
  lanes. It is not mapped to a Stellaris multiplier or mutable priority number.
  Recovery, legality, and post-completion runway dominate identity preference.

Top five risks:

1. **A primary label can erase hybrid identity.** Preserve every non-primary
   evidence component and its reason codes; use the primary only for mutually
   exclusive routing. Fanatic ethics record three secondary-pressure units to a
   normal ethic's one, without turning classification into an opaque sum.
2. **Outcome feedback can rewrite identity and create an overreaction loop.**
   Keep all economy, fleet, capacity, threat, and queue observations out of
   `NationIdentity`; they may alter bounded policy output only.
3. **Missing templates or zero denominators can be mistaken for zero demand.**
   Distinguish serialized reinforcement demand from template-creation and
   template-expansion gaps, and keep unknown naval capacity distinct from zero.
4. **Unknown or modded identities can receive an unsafe confident label.** Use
   an explicit `insufficient_evidence` status with a neutral balanced primary;
   exclude non-default and nomadic countries rather than guessing.
5. **A model-only preference can bypass economic feasibility when integrated.**
   Do not connect this slice to the selector or mod. A later integration must
   apply bounded deltas only after existing activation, recovery, legality,
   affordability, queue, and runway gates, and must prove zero-overlay parity.

Static acceptance:

- Every dataclass is immutable and canonicalizes unordered identity inputs.
- The fixture tables cover all seven primaries, excluded/conflict/insufficient
  states, crisis, assimilator, wilderness, nomadic, hard-conflict, low-use and
  low-capacity, no-template, filled-template, threat, recovery, unsafe-runway,
  unknown/zero naval-capacity, permutation, and enormous-value cases.
- The exact ten-save primary distribution is asserted without golden fleet,
  income, stockpile, or technology thresholds.
- Pressure outputs remain categorical and bounded under zero, unknown, and
  enormous inputs. No cost, order, resource, claim, war, flag, or game state is
  mutated.
- Focused tests, compilation, lint, formatting, both JData fixture indexes, and
  `git diff --check` must pass before commit.

Rollback boundary:

Revert only H08a if the offline schema or fixtures prove misleading. This slice
does not alter the live mod; H08b must be a separate trigger-only commit, and any
later behavior consumer must remain separately reversible.
