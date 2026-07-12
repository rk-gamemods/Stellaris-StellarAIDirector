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

Status: the original availability correction was committed at `75bca24e`.
The follow-up robustness correction removes its residual factor-0.25
colonization-plan dampener; focused static validation passed, with copied-save
runtime continuation still pending.

Evidence:

- The integrity-verified `2270.04.15` save copy has SHA-256
  `7E49527196CAA35DCCD5FB22FF24E77C08A1EEA84C9263A52E87DF95492784B7`.
- Paunaby (system 10/star 221), Aerea (70/1186), and Zosma (96/329)
  remain unowned, surveyed, unrestricted type-19 native expansion candidates.
- Country 0 has thirteen constructors, eleven of them idle, and no outpost
  order. Executor saturation explains 2255-2257 but is no longer the immediate
  2270 gate between recognized candidate and assigned construction order.
- In 2268.01 through 2269.07 the same three type-19 candidates persisted with
  twelve of thirteen constructors idle, zero type-1 colonization plans, no
  outpost order, 895-1000 influence, and more than 63,000 alloys. Therefore the
  colonization-plan condition cannot explain the entire observed stall.
- The one type-1 record is for planet 2, already owned by country 0 with
  `colonize_date="2270.01.26"`; the save date is `2270.04.15`.
- The vanilla alloy outpost potential puts both country-type exclusions and
  `ai_colonize_plans > 0` inside one multi-statement `NOT`. Its exact runtime
  semantics were not proven by generated docs or CWTools. The biological food
  analogue uses an explicit `NOR`, proving that colonization-plan ineligibility
  is at least the source's intended paired behavior.
- The save series predates H01-H07 and the live descriptor switch, so it cannot
  prove any current correction at runtime.

Preserve native expansion-plan recognition, system scores, target selection,
pathing, threat limit, influence reserve, biological-ship rule, wilderness
terraforming exclusion, base weights, and desired minima. For the alloy lane,
normalize the ambiguous multi-statement `NOT` to an explicit country-type
`NOR`. For both alloy and biological-food lanes, remove only the
colonization-plan condition. Do not retain a numeric dampener tied to a count
that can remain stale. In the ordinary alloy lane, the native colony allocation
weight remains `0.5` while the outpost allocation weight remains `0.2` (a 2.5:1
budget-weight ratio). Biological-food colonies use `2.0` versus food outposts at
`0.2`, and infernal alloy colonies use `0.8`. These are allocation weights, not
proven scheduler odds. This does not promise an outpost.

Top five risks:

1. **A valid colony ship may compete with an outpost in a constrained economy.**
   Retain the native `0.5` colony and `0.2` outpost weights plus all native
   resource reserves; compare colony and outpost completion in low-resource
   runtime cases before promotion.
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
  explicit alloy `NOR`, removal of the colonization eligibility clause, and
  generator block ordering. The original weight blocks remain byte-identical to
  their pinned sources, and the other source subblocks retain their contents.
- Pinned source hashes and an active-playset scan fail generation if vanilla
  drifts or any enabled parent mod begins overriding either budget object.
- Threat, influence, country-type, biological, wilderness-terraform, weight,
  and desired-min markers remain under regression coverage.
- No constructor cap, scripted target/order, `clear_orders`, free resource, or
  forced claim is added.
- PDX parsing, focused recovery tests, known-object validation, JData provenance
  validation, static validator, and clean-worktree checks pass before commit.

Rollback boundary:

Revert only the H07 follow-up if colony completion regresses; revert original
H07 separately if the availability override itself proves harmful. Do not
restore H01-H06 megastructure pressure or the removed order watchdog.

## H07c — Defer accelerated claim spending while expansion is active

Status: implemented as a separate, save-safe trigger correction; focused
static validation passed, with copied-save runtime continuation still pending.

Evidence:

- Country 0 is a non-militarist `ruthless_capitalists` personality with
  authoritarian and fanatic-materialist ethics. At `2270.04.15` it is at peace,
  holds `980` influence with `+10.75` monthly income, and has three serialized
  type-19 expansion candidates.
- The save does not serialize the evaluated results of
  `has_ai_expansion_plan` or `has_potential_claims`. Claim-budget competition is
  therefore a strong Director-specific hypothesis, not proven causation.
- Before this correction, influence above `900` bypassed the shared trigger's
  no-expansion-plan condition. For this non-militarist empire, the generic claim
  lane could therefore reach `0.20 * 3 * 2 = 1.20` while the vanilla station lane
  remained `0.50`.
- The independent high-influence factor remains on each claim budget object.
  While an expansion plan exists, this empire's generic claim weight is now
  bounded at `0.20 * 2 = 0.40`; when no expansion plan exists, the factor-3
  acceleration can still raise it to `1.20` at capped influence.

Change only `staid_influence_claim_pressure`: retain its peace, non-pacifist,
potential-claim, and influence-above-500 gates, but require a direct
`NOT = { has_ai_expansion_plan = yes }`. Preserve all three claim objects,
their independent high-influence factor `2`, boxed-in urgency factor `12`, base
weights, and potentials. This reorders discretionary influence pressure without
creating claims, targets, resources, orders, or persistent state.

Top five risks:

1. **A stale native expansion plan may defer otherwise useful claims.** Keep the
   independent high-influence factor and boxed-in urgency path; check whether
   claims resume after the expansion plan clears in runtime continuation.
2. **Claim competition may not be the planner-to-order blocker.** The save does
   not expose evaluated budget choice or scheduler internals; keep this as a
   separate rollback commit and require A/B runtime evidence.
3. **Militarist claim lanes may still aggregate above the station lane.** This
   exact save is non-militarist. Do not generalize its `0.40` versus `0.50`
   comparison; test regular and fanatic militarist expansion separately before
   broadening the correction.
4. **Long-distance aggression may start later.** The no-expansion condition
   delays only the shared factor-3 acceleration, not normal claims, capped
   influence spend-down, or boxed-in urgency. Check claim creation and war
   preparation after nearby expansion opportunities are exhausted.
5. **Boxed-in urgency may still dominate normal expansion.** Its factor `12`
   is intentionally preserved and could raise this empire's capped-influence
   generic claim weight to `4.80` even with an expansion plan. The screenshot
   topology suggests `staid_boxed_in_war_pressure` should be false, but the save
   does not serialize the evaluated trigger. Verify that path in runtime before
   altering it.

Static acceptance:

- The generated decision-state trigger artifact equals `triggers_text()` and
  parses without cycles or unresolved scripted-trigger references.
- `staid_influence_claim_pressure` contains exactly one direct no-expansion-plan
  gate and no influence-above-900 bypass.
- All three claim objects retain their original base, factor-3 shared trigger,
  factor-12 boxed-in urgency, and independent factor-2 high-influence signal.
- No claim-budget artifact, order surface, event, effect, persistent state, or
  constructor target changes in this slice.
- Generated trigger equality is checked directly and the claim-budget artifact
  remains byte-identical; the broad all-artifact generator is not used.

Rollback boundary:

Revert only H07c if valid claims remain deferred after expansion ends or if
aggression regresses. Do not revert H07/H07b outpost availability or H01-H06
constructor-pressure corrections with it.

## H07d — Deconflict claims from both visible borders and boxed urgency

Status: implemented as a separate, save-safe refinement of H07c; focused static
validation passed, with copied-save runtime continuation still pending.

Evidence:

- Vanilla Pegasus 4.4.4 defines `has_bordering_system` as an owned border
  system having an intel-visible, unowned hyperlane neighbor. It excludes
  precursor/enclave systems, hostile fleets, fleets above `1000`, and systems
  where another constructor is already building a starbase.
- The Director already uses that trigger as its topology-backed boxed-in signal
  and records prior runtime evidence (`TEST_2231`) that internal
  `has_ai_expansion_plan` state can remain active after every peaceful
  territorial exit is gone.
- Conversely, this save does not serialize the evaluated expansion-plan result;
  raw type-19 candidates do not prove that the planner promoted the visible
  holes into a formal plan. H07c alone could therefore leave factor-3 claim
  pressure active before plan creation.
- Aerea is enclosed by four country-0 systems, while Paunaby and Zosma border
  country-0 territory. The preserved save series records them as unowned and
  intel-visible, so `has_bordering_system = yes` directly describes at least
  one reported route even if the internal plan result is false.
- A naïve replacement of the plan gate with `has_bordering_system = no` was
  independently rejected before commit: it could stack factor `3` with boxed-
  in factor `12` and capped-influence factor `2`, producing a `14.4` generic
  claim weight. H07d keeps the plan guard and makes those pressure paths
  mutually exclusive.

Retain H07c's `NOT = { has_ai_expansion_plan = yes }`, and add both
`has_bordering_system = no` and
`NOT = { staid_boxed_in_war_pressure = yes }` to
`staid_influence_claim_pressure`. The shared factor-3 acceleration now requires
no internal expansion plan, no immediately adjacent visible/unowned safe
system, and no boxed-in factor-12 pressure. Normal claim weights, the independent
capped-influence factor `2`, all claim potentials, and vanilla station rules
remain unchanged. This deconflicts spending pressure; it does not create a
plan, target, constructor order, claim, or outpost.

Top five risks:

1. **A false-negative plan can still expose distance-two expansion to claims.**
   Retaining the plan gate protects recognized distance-two routes; runtime
   evidence must test a viable distance-two target when the serialized save
   cannot prove the evaluated plan result.
2. **A stale positive plan can suppress factor-3 claims.** Boxed-in factor `12`
   remains available for true containment, while normal and capped-influence
   claim weights remain available elsewhere. Verify claims resume after local
   expansion ends without assuming a trigger refresh cadence.
3. **The topology latch can toggle with intel or fleet movement.** Vanilla
   intentionally ignores unknown, hostile, heavily defended, and already-being-
   claimed systems. Record those raw conditions before attributing a transition
   to Director logic.
4. **Militarist lanes can still accumulate pressure.** Regular and fanatic
   militarists retain their extra claim objects, and the independent factor `2`
   remains. Compare maximum individual and summed eligible category weights;
   do not present them as scheduler probabilities.
5. **Pressure deconfliction may not produce a construction order.** Native plan
   creation, target scoring, influence reservation, and constructor assignment
   remain engine-owned. Keep H07d independently reversible and require gameplay
   continuation evidence.

Static acceptance:

- The generated decision-state artifact equals `triggers_text()` and parses
  without trigger cycles or unresolved references.
- `staid_influence_claim_pressure` contains exactly one no-plan gate, one
  `has_bordering_system = no`, one boxed-pressure exclusion, and no internal
  influence-above-900 bypass.
- The boxed-pressure trigger excluded from factor `3` is required by
  `staid_boxed_in_claim_urgency`, and that wrapper is the sole input of every
  preserved factor-12 claim modifier, preventing a `3 * 12` overlap.
- All three claim objects remain byte-identical and retain their base weights,
  factor-3 shared trigger, factor-12 boxed urgency, and independent factor-2
  capped-influence signal.
- No outpost/station potential, target, order, event, effect, resource grant,
  persistent state, or constructor rule changes in this slice.

Rollback boundary:

Revert only H07d to restore H07c's plan-only deconfliction if claims are
materially delayed by safe adjacent systems or the boxed-exclusion interaction.
Do not revert H07/H07b availability or H01-H06 constructor-pressure corrections.

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

## H08b — Generated mutually exclusive nation-archetype triggers

Status: implemented as a generated, identity-only production trigger surface.
The live mod contains the classifiers, but this slice adds no consumer, weight,
factor, resource rule, flag, event, effect, order, war rule, or economic target.

- `tools/stellar_ai_archetype_triggers.py` owns the focused renderer;
  `tools/generate_stellar_ai_archetype_triggers.py` exposes one fixed-output,
  no-flag command; and the broad Director generator owns the same artifact.
- Generation fails closed unless the installed Pegasus 4.4.4 personality source
  matches SHA-256
  `1F89C8D6C9444F575526A8635DB59DF78140AD43401538214E6B62F685298BAA`
  and every reviewed vanilla personality ID still exists.
- Seven primary triggers use the H08a precedence order: extermination,
  gestalt-growth, defensive, research, diplomatic, conquest, and balanced.
  Candidate helpers keep the primaries mutually exclusive without a deep chain.
- Every pair of the six non-balanced hard signals is covered by the identity
  conflict trigger. Conflicting hard evidence fails closed to balanced rather
  than allowing two archetype consumers to stack.
- Eligibility is limited to default, non-nomadic countries. Unknown or modded
  identities without a reviewed signal use balanced; genocidal gestalt signals
  remain extermination, while non-genocidal gestalt anchors remain
  gestalt-growth.
- The mixed `dominator + liberator` case preserves the model's diplomatic
  tie/precedence. A first-pass diplomatic veto incorrectly routed it to conquest;
  independent review caught the divergence before commit and a regression test
  now fixes the intended translation.

Top five risks:

1. **A modded or newly added personality can inherit the wrong broad fallback.**
   Exact reviewed personality anchors dominate broad behaviors and ethics;
   unknown identities fall back to balanced, while source hash/ID drift blocks
   regeneration for the pinned 4.4.4 build.
2. **Two identity signals can stack downstream multipliers.** The seven primary
   triggers are candidate-precedence routes, all 15 hard-signal pairs route to
   conflict, and balanced is the exclusive eligible fallback. Tests assert every
   boolean reference value and reject duplicate `staid_` trigger IDs across the
   mod.
3. **A broad `conqueror`-family behavior can erase a more specific identity.**
   Exact anchors win first; broad conquest is last among non-balanced routes.
   Diplomatic mixed evidence retains H08a precedence unless `conqueror` is
   explicitly present, and no gameplay weight consumes the result in H08b.
4. **Version or load-order drift can make copied identity assumptions stale.**
   The renderer verifies the exact source hash and all 30 reviewed IDs before it
   writes. A dedicated drift test proves generation fails before artifact output.
5. **A future consumer can turn a stable label into an economic overreaction.**
   H08b contains only positive identity predicates and bounded boolean routing.
   Future H08c consumers must remain separate commits, apply small bounded deltas
   after recovery/legality/runway gates, and prove zero-overlay equivalence.

- The generated artifact parses as PDXScript, is byte-equivalent to its renderer,
  has an acyclic reference graph with maximum depth four, and uses an exact
  allowlist of identity predicates and reviewed marker values.
- The local 4.4.4 `triggers.log` (SHA-256
  `59D227268A61158475F50C895A833553305E3EC29FC1B1269A7AA4A018C2B316`)
  verifies the engine predicates used here as country-scope forms. Current
  vanilla scripted-trigger definitions and AI-weight call sites separately
  verify the hive, machine, wilderness, pacifist, and federator helpers.
- JDocMunch rejected the generated `.log` files as an unsupported extension, so
  exact log excerpts were read only after that direct index attempt failed.
  CWTools was also not installed (`cwtools` and `cwtools-cli` were both missing;
  no extension or global tool was found), so the clean custom validator result
  is supporting parser evidence and is not described as a CWTools pass.
- Focused H08a/H08b validation currently passes 36 tests plus 42 parameterized
  subtests. Compilation, scoped Ruff checks, the static Director validator, and
  `git diff --check` also pass.
- No Stellaris process or observer simulation was launched. Runtime semantics
  remain a user gameplay check after this static trigger slice is committed.

Revert H08b independently by removing the generated trigger artifact, focused
renderer/generator/tests, broad-generator hook, and this ledger section. H08a's
offline model and every earlier live gameplay recovery slice remain intact.

## H08c — Hard-anchored fleet and technology identity tie-breakers

Status: implemented as two bounded native-AI consumer surfaces. This slice
changes only the alloy ship budget and the existing technology route override;
it adds no economic-plan target, personality scalar, event, on_action, flag,
resource, free grant, order, claim, war goal, or declaration.

- The ship budget adds ordinary-peacetime underfill factors of `1.12` for an
  unambiguous extermination anchor and `1.08` for an unambiguous conquest
  anchor. Every other identity remains at the native/Director baseline.
- Ship factors require used naval capacity below `0.80`, peace, no recent loss,
  no catastrophic collapse, no core-deficit short runway, and the exact inverse
  of the native crisis `x5` predicate. They therefore cannot compound the
  native war/recent-loss `x3`, crisis `x5`, or Director high-capacity `x0.25`
  paths.
- Technology factors are positive route-specific tie-breakers between `1.05`
  and `1.15`. They require the matching route gate, peace, no recent loss, no
  survival/recovery/collapse/short-runway state, one hard identity anchor,
  default non-nomadic eligibility, and no hard-identity conflict. A route's
  existing factor-zero veto remains earlier in the block and algebraically
  decisive.
- Research/diplomatic anchors affect only the three reviewed research route
  families; gestalt-growth affects selectable pop-assembly targets; defensive
  affects the selectable fallen-empire benchmark; and conquest/extermination
  affect selectable Mega Shipyard, war-moon, systemcraft, NSC3 hull, and ESC
  component targets.
- Four source-inert or event-granted technology objects are explicitly neutral:
  `giga_tech_lunar_assembly`, `giga_tech_war_system_1`, `tech_ring_world`, and
  `esc_tech_dreadnought_computer`. Their source draw weight or
  `weight_modifier` is zero, so changing downstream `ai_weight` cannot put them
  into the draw pool.
- `tools/generate_stellar_ai_archetype_overlays.py` owns an exact two-path
  `check|diff|write` allowlist. Its zero-overlay render is logically
  byte-equivalent to pre-H08c HEAD for both production artifacts.

The consumer intentionally uses `staid_archetype_hard_*`, not the broader H08b
primary triggers. Adversarial review found that mixed soft evidence can diverge
between the H08a strength-count model and H08b's fixed candidate precedence.
For example, fanatic militarist plus materialist is conquest in H08a but can
route to research in H08b. Until a dedicated parity slice fixes and tests every
mixed-evidence permutation, soft-only, unknown, balanced, and conflicted
identities receive no H08c factor.

Top five risks:

1. **Identity pressure can multiply native emergency spending into an extreme
   response.** Ship tie-breakers are disjoint from war, recent loss, crisis,
   collapse, and short-runway states. Technology tie-breakers are disjoint from
   war, recent loss, survival, recovery, collapse, and short runway and alter
   research selection only, not the research or ship budget. The largest factor
   is `1.15`.
2. **Soft or modded identity evidence can be mistranslated.** Consumers require
   one reviewed hard anchor, `staid_archetype_eligible_country = yes`, and
   `staid_archetype_identity_conflict = no`. Non-default, nomadic, balanced,
   unknown, soft-only, and conflicted countries are neutral.
3. **Large existing technology weights can turn a small factor into route
   saturation.** Factors apply only to named routes, never globally, never
   exceed `1.15`, and cannot bypass route factor-zero gates or source
   prerequisites. Source-inert targets are excluded rather than falsely
   claiming efficacy.
4. **A new consumer can double-count the 72 existing economic subplans or
   elevated personality military scalars.** H08c changes neither surface and
   does not add research, alloy, or naval-capacity targets.
5. **Full-object regeneration can overwrite unrelated behavior.** The focused
   renderer owns exactly two paths, proves zero-overlay parity, validates
   PDXScript before writing, updates only stale outputs, and verifies every
   post-write result.

Static acceptance:

- All production identity factors are in `(1.0, 1.15]`, use hard anchors, and
  fail neutral on conflict. At most one hard anchor can fire after the conflict
  gate, even where a technology object contains multiple alternative lines.
- The native ship base, `x3`, `x5`, over-cap, bioship, desired-minimum, and
  potential rules are unchanged outside the additive H08c blocks.
- Exactly 42 reviewed technology override objects remain generated. Only
  selectable objects in the explicit route matrix receive H08c lines; the four
  proven inert/event targets receive none.
- Focused tests cover the two-file allowlist, zero-overlay hashes, route matrix,
  factor bounds, emergency disjointness, conflict neutrality, inert-target
  exclusions, factor-zero precedence, read-only check/diff modes, and stale-only
  writes. Runtime behavior remains a user gameplay test; no observer run is
  authorized by this slice.
- The exact native crisis inverse includes a global country query. Independent
  QA rejected copying it onto all 45 technology modifiers: production now adds
  zero `any_country` scans to the technology artifact and exactly two guarded
  scans to the ship budget. These are never called from a Director pulse, but
  their actual late-game runtime cost remains a playtest/profile observation.

Rollback boundary:

Revert H08c independently by removing the two additive modifier families, the
focused renderer/generator/tests, and this ledger section. H08a's offline model,
H08b's identity-only triggers, and all earlier expansion/economic recovery
slices remain intact.

## H08d — Generated classifier parity for mixed-strength identity evidence

Status: implemented as an identity-only correction to the H08b trigger graph.
This slice changes no consumer factor, personality, budget, economic plan,
event, state, resource, order, claim, war rule, or declaration.

- The production classifier now mirrors H08a's lexicographic evidence model:
  hard anchors dominate; otherwise strong-marker count dominates supporting
  count; the original archetype precedence breaks exact ties.
- Thirty-six native `calc_true_if` helpers count only the finite, source-mapped
  H08a identity vocabulary. One additional counter detects two-or-more hard
  archetypes directly. Pairwise greater-than-or-equal helpers then select one
  deterministic candidate without numeric variables or persistent state.
- Reviewed Pegasus 4.4.4 personality IDs remain hard anchors. Ethics, civics,
  ascension perks, authorities, governments, origins, wilderness status, and
  personality behaviors are projected from the same model tables used by H08a.
- Every non-balanced public primary has exactly three conditions: eligible
  default/non-nomadic country, no hard-identity conflict, and its unique
  candidate. Older preceding-candidate `NOR` chains were removed after the
  pairwise total order made them redundant, reducing the worst balanced path
  from 42 candidate evaluations to 12.
- H08c continues to consume only the unchanged hard-anchor, eligibility, and
  conflict helpers. The conflict helper is now one six-input `calc_true_if`
  instead of 15 pairwise branches, reducing its live expansion from 31 checks
  to seven. No live mod consumer currently calls the expanded public primary
  graph.

Top five risks:

1. **The generated marker vocabulary can drift from the offline model.** The
   renderer imports the H08a marker tables directly, rejects duplicate
   projections, verifies all reviewed personality IDs, and pins the exact
   Pegasus 4.4.4 personality source hash.
2. **Count comparisons can select the wrong hybrid archetype.** Tests evaluate
   all 30 H08a identity fixtures plus 13 adversarial mixed-strength cases,
   including fanatic-militarist/materialist and multi-signal pacifist research
   combinations, through both model and generated-trigger semantics.
3. **A correct classifier can still be too expensive.** `calc_true_if` replaces
   combinatorial threshold expansion; the graph is acyclic with maximum depth
   five, contains no country/planet/fleet iterators or pulse hooks, and public
   primaries avoid redundant candidate chains. The generated artifact remains
   51,273 bytes and requires runtime profiling before widespread use.
4. **Hard conflicts or excluded countries can receive a confident strategy.**
   Public non-balanced primaries require eligibility and `identity_conflict =
   no`; balanced is a neutral fallback, while every behavior consumer must
   retain its own conflict/eligibility gate where a factor is non-neutral.
5. **Runtime behavior predicates lose offline provenance.** Stellaris exposes
   the effective personality behavior but cannot distinguish H08a's
   `save_time_winner_verified` from `current_source_resolved`. Runtime behavior
   evidence is therefore conservatively supporting; reviewed personality IDs
   remain the hard source of truth.

Static acceptance:

- The artifact has 118 unique top-level triggers, 37 exact `calc_true_if`
  counters, no combinatorial threshold branches, no cycles, and maximum
  reference depth five.
- Public trigger IDs and all H08c hard/eligibility/conflict helper IDs remain
  stable. The focused and broad generators share one renderer; focused output
  is idempotent at SHA-256
  `DB2CFAF3205063DA9D5CF5FB4ECD1BCBC0774F39C50912E202949F83B96B36BB`.
- Focused H08a/H08d/H08c tests, parser validation, the static Director
  validator, compilation, scoped Ruff/format checks, and `git diff --check`
  must pass. CWTools remains not installed, so local parser/validator evidence
  is not represented as a CWTools result.
- Runtime classification behavior and performance remain gameplay/profile
  questions; no observer run is authorized by this slice.

Rollback boundary:

Revert H08d independently by restoring the prior H08b renderer, focused tests,
and generated trigger artifact and removing this ledger section. H08a's offline
model, H08c's hard-anchor consumers, and every earlier gameplay fix remain
intact.

## H08e — Bounded public lead-secondary archetype

Status: implemented as an inert identity-classification extension. This slice
adds no weight, budget, economic plan, event, state, resource, order, claim,
war rule, or declaration by itself. Any economy or behavior consumer remains a
separate generator, validation, and rollback boundary.

- Six public `staid_archetype_lead_secondary_<archetype>` triggers expose at
  most the first item in H08a's ordered `classification.secondary` tuple.
- A lead secondary must be eligible, conflict-free, supported by positive
  identity evidence, and explicitly different from the selected primary.
- Each trigger reuses the H08d strong/supporting greater-than-or-equal circuit.
  For every competitor, it either ignores the one selected primary or proves
  that the proposed lead secondary outranks that non-primary competitor.
- Balanced has no secondary trigger because balanced owns no positive identity
  evidence in H08a. Excluded, conflicted, insufficient-evidence, and
  single-archetype identities therefore expose no lead secondary.

Top five risks:

1. **Two secondary triggers can be true at once.** The pairwise total order is
   reused without a secondary-to-secondary chain, and tests evaluate all six
   triggers together and reject more than one result.
2. **The primary can leak back as its own secondary.** Every secondary trigger
   requires its corresponding public primary to be false, and parity tests
   assert that non-empty primary and secondary results differ.
3. **The wrong hybrid identity can become the lead secondary.** All 30 H08a
   fixtures and the adversarial mixed-strength set compare the generated result
   directly with `classification.secondary[0]`, including hard-primary,
   strong-count, supporting-count, and exact-precedence ties.
4. **Neutral or invalid identities can receive a confident secondary.** The
   layer retains the H08d eligibility and hard-conflict gates, requires positive
   evidence for the proposed secondary, and has no balanced secondary object.
5. **A correct secondary classifier can still be expensive when consumed.**
   The six triggers add no iterator, pulse, event, or persistent state and keep
   the graph acyclic at maximum depth five, but the generated artifact grows to
   70,538 bytes. Each separate consumer must remain bounded and requires
   runtime profiling before widespread use in frequently evaluated AI weights.

Static acceptance:

- The generated artifact has 124 unique top-level triggers, including exactly
  six lead-secondary triggers, and remains acyclic at maximum reference depth
  five.
- The focused single-output generator owns the artifact and is idempotent at
  SHA-256 `85334F5114FAEA4011A8A925E2E1F7ED9CE3CF35744D5BD8FD018B4350FF7042`.
  The broad generator was not run.
- Focused classifier tests, combined H08a/H08d/H08e/H08c tests, parser/static
  validation, compilation, scoped Ruff/format checks, and `git diff --check`
  must pass before commit. Runtime behavior and performance remain unproven.
- H08d's personality-behavior provenance limitation remains: live behavior
  predicates are conservatively supporting because the engine cannot expose
  the offline `save_time_winner_verified` distinction.

Rollback boundary: remove the six lead-secondary render blocks, their focused
tests, this ledger section, and regenerate the one trigger artifact. H08a's
offline secondary tuple, H08c's hard-anchor consumers, H08d's primary parity,
and H09 remain intact.

## H08f0 — Orthogonal defining-identity and role labels

Status: implemented as ten exact, stateless public country triggers for
megacorp, subject, overlord, rogue servitor, assimilator, machine exterminator,
devouring swarm, inward perfection, barbaric despoiler, and nomadic/Arkship
identity. They are labels for dedicated consumers, not competing archetypes.

Top five risks:

1. **New labels can create false archetype conflicts.** None participates in
   the H08 hard-conflict counter; each may overlap the primary and runner-up.
2. **Personality aliases can misclassify reformed empires.** Defining identities
   use current civic/authority state, never personality-name approximations.
3. **Subject and overlord status can change.** Both are live role predicates
   with no flags or cached state and are intentionally separate overlays.
4. **Arkship scope can be confused with ship scope.** The country label uses
   `is_nomadic = yes`; ship/starbase Arkship predicates are not used.
5. **Labels can become expensive if placed in hot consumers.** This slice adds
   no weights, plans, iterators, effects, or orders; each later consumer requires
   its own overlap, performance, and rollback review.

Rollback boundary: remove only the ten wrapper triggers and focused tests, then
regenerate the one archetype artifact. Primary/secondary classification remains.

## H08f — Bounded identity economic consumers

Status: implemented as dedicated primary archetype economic subplans plus one
bounded lead-secondary subplan. Balanced identities retain the shared safe
baseline. The conquest primary reuses the existing conquest reserve without
its former `naval_cap = 6000` target. Five universal clock-driven research and
snowball ramps are retired; modded-unlock, ESC, and NSC3 support now require
real readiness or technology evidence rather than elapsed years.

Top five risks:

1. **Mixed identities can stack into an extreme target.** H08e proves exactly
   one primary and at most one distinct lead secondary; secondary targets are
   independently capped and ordinary plans are non-scaling.
2. **Identity spending can delay recovery.** Every identity plan requires safe
   basic runway, no short-runway core deficit, and no collapse; research-bearing
   plans also require construction-ready research inputs. War alone is not a
   veto because safe capped resources must remain available to civilian growth.
3. **A target can request an unused resource.** Identity plans omit food and
   consumer goods; resource-specific repair remains guarded by `country_uses_*`
   predicates. Runtime proof must still check trade handling for unusual
   machine or gestalt combinations.
4. **Removing time ramps can weaken genuine late-game scaling.** Trigger-driven
   unlock, stockpile-conversion, fleet-throughput, megastructure, crisis, and
   relative repair plans remain. Runtime telemetry must decide whether a future
   evidence-driven high-scale overlay is needed.
5. **Economic-plan target composition is engine-owned.** Static tests prove
   gates, cardinality, targets, syntax, and absence of clocks/state/orders; they
   cannot prove final merged target selection or construction execution.

Rollback boundary: revert the economic renderer, its focused generator/tests,
and the one economic-plan artifact. Do not revert H08e classification or H09.

### H08f1 — Defining-civic economic branches

Status: defining machine exterminator, rogue servitor, assimilator, devouring
swarm, inward-perfection, megacorp, barbaric-despoiler, and nomadic identities
now use dedicated bounded subplans. Broad archetype plans explicitly exclude
these identities, preventing duplicate primary-plus-civic stacking. Subject and
overlord remain dynamic labels without fixed resource targets because contracts
can invert net obligations.

Top five risks:

1. **Dedicated and broad plans can stack.** Broad settled plans contain an
   explicit NOR over every defining identity; the despoiler plan replaces the
   former oversized raiding reserve.
2. **Special economies can request unusable resources.** Machine/hive branches
   omit ambiguous food/consumer-goods targets; servitor, inward, and corporate
   branches use exact resource-usage gates.
3. **War can freeze rich civilian growth.** No defining branch uses war or
   recent-loss as a veto; runway, deficit, collapse, and research-input safety
   remain authoritative.
4. **Nomads can inherit settled planet assumptions.** Their isolated branch
   uses the country-level nomadic label and contains no archetype-eligibility or
   owned-planet condition.
5. **Fixed subject/overlord targets can reverse real contracts.** No economic
   consumer is added until native net-contract evidence exists.

Rollback boundary: remove the defining branches and broad-plan exclusions,
restore the previous bounded raiding reserve, and regenerate only the economic
artifact. Identity labels and primary classification remain.

### H08f2 — Nomad Waystation threat-softened budgets

Status: implemented as one focused artifact overriding the native influence,
alloy, and biological-food Waystation expenditure objects. The Pegasus hard
`highest_threat < 50` potential cutoff becomes a `0.5` weight modifier at
threat 50 or higher. Nomads remain excluded from settled outpost logic.

Top five risks:

1. **Wartime Waystations can crowd fleets or reserves.** Threat halves all three
   resource-lane weights rather than leaving full priority.
2. **Three budget lanes can diverge.** All three objects receive the same threat
   rule; biological food/alloy conversion gates remain source-identical.
3. **Waystations can exceed starbase capacity.** Native 0.5/0.1/0 capacity
   factors at 100%/125%/200% use remain untouched.
4. **Country, Arkship, and station scopes can be confused.** The consumers use
   native `is_nomadic` country budgets only; no ship/starbase predicate is added.
5. **Budget eligibility does not prove Wayline execution.** Static validation
   proves source fidelity and gates; Arkship carrier, Contract, Wayline, and
   ownership-transfer behavior still require runtime proof.

Rollback boundary: delete the focused artifact. Vanilla hard cutoffs resume;
the nomadic economic branch and identity label remain independent.

### H08f3 — Total-war invasion mineral staging

Status: machine exterminator, devouring-swarm, and assimilator labels add one
nonstacking 300-mineral desired-min modifier to the native army expenditure
budget when basic runway is safe and no core short-runway deficit or collapse
exists. Army definitions, recruitment eligibility, costs, damage, health,
bombardment, transports, landing targets, and invasion execution are unchanged.

Top five risks:

1. **Army reserves can crowd colony construction.** The addition is 300 minerals
   and is disabled by deficit/collapse gates; it reserves currency, not units.
2. **War identities can double-stack other army routes.** The three exact labels
   share one OR modifier, so multiple labels still add only once.
3. **Available budget can create excessive armies.** Native recruitment demand,
   legal army types, costs, and transport planning remain authoritative.
4. **Assimilators may prefer conquest without immediate invasion capacity.** The
   modifier only stages minerals; it does not force a target, landing, or war.
5. **Static validation can overclaim competence.** It proves budget gates and no
   scripted actions, not recruitment, escort, bombardment, landing, or victory.

Rollback boundary: remove the single desired-min modifier and regenerate only
the army-budget artifact. Identity and economic consumers remain independent.

## H09a — Retire stateful threat-response runtime

Status: implemented as a cleanup-only slice. The generator deletes the legacy
`on_war_beginning` hook, threat events, scripted triggers, and script values.
The threat-readiness economic subplan and strategy-kernel flag consumer are
removed. No migration event, replacement behavior, H09b budget factor, or
distance change is included.

The ten legacy `staid_tr_*` opinion modifier IDs and their localization remain
defined with `opinion = 0`. They are compatibility identifiers only: no
production event, on-action, trigger, plan, or effect applies or consumes them.

Top five risks:

1. **Deleting serialized opinion IDs can break copied-save references.** Keep
   the same IDs and localization as zero-effect definitions while old timed
   references age out.
2. **A cleanup event can recreate the prohibited stateful control plane.** No
   migration event or gameplay-state mutation is added; existing timed flags
   are inert because every consumer is removed.
3. **A generator rerun can silently restore the retired files.** The generator
   unlinks all four retired paths, and focused tests require their absence.
4. **A hidden consumer can preserve readiness pressure.** Negative validation
   rejects the readiness flag, foreign-affairs trigger, reserve name, war hook,
   event namespace, and timed threat-state writes across production scripts.
5. **Removing one emergency input can weaken unrelated defense behavior.**
   `staid_security_threatened` retains the native crisis-starbase signal; H09a
   adds no compensating factor until a separately reviewed bounded slice.

Save classification:

`cleanup-required; copied-save-only runtime proof pending`. Static validation
proves no new state writes and no live consumers. It cannot prove how Pegasus
4.4.4 resolves pre-existing serialized modifier/flag references, so the retained
zero-effect IDs require a copied-save load check before later deletion.

Rollback boundary:

Revert H09a independently by restoring the four legacy generated runtime files,
the readiness subplan, and the strategy-kernel flag branch. Do not combine that
rollback with any later stateless H09 factor or distance adjustment.

## H09b/H09c — Bounded arms-race nudge and war-distance cutoff

Status: implemented as two native, stateless scalar adjustments. A threatened
AI at peace with less than 80% naval-capacity use receives a `1.10` ship-budget
factor only when it has not recently lost a war and is outside collapse,
short-runway, and crisis states. `WAR_DECLARATION_MAX_DISTANCE` returns from the
Director's restrictive `50` to the Pegasus vanilla ceiling of `300`; the
existing Director distance malus, score floor, aggression base, and
offense/defense allotment remain unchanged.

Top five risks:

1. **Fleet spending can crowd out recovery.** The factor is capped at `1.10`,
   excludes collapse/short-runway/recent-loss states, and has a worst-case
   overlap of `1.10 * 1.12 = 1.232` with the strongest identity bias.
2. **`highest_threat` does not identify a useful target.** It only nudges the
   native ship budget; it does not select enemies, create claims, or order wars.
3. **Budget availability does not guarantee ships.** Templates, shipyards,
   affordability, queues, and the engine planner remain required; runtime proof
   must distinguish allocation from construction.
4. **A wider declaration radius can expose pathing or homeland-defense faults.**
   Only the hard cutoff changes to `300`; the malus still begins after 25 jumps,
   applies `0.05` per additional jump, and bottoms out at a `0.5` multiplier,
   preserving a nearby-target preference without excluding distant empires.
5. **Crisis exclusion adds another global crisis predicate evaluation.** No
   event, pulse, persistent state, or scripted order is added, but observer
   telemetry should confirm the native budget check is not a measurable cost.

Rollback boundary: remove the H09b modifier independently or return the one H09c
define to `50`. Neither rollback should restore the retired H09a event system.

## H09d — Threat-softened native outpost funding

Status: implemented after the save-backed unclaimed-system report exposed a
boundary mismatch. Both native outpost expenditure objects previously became
categorically unavailable at `highest_threat >= 50`, while the bounded ship
nudge begins only above 50. The hard potential cutoff is now a `0.5` weight
modifier at threat 50 or higher. Expansion-plan, influence, fallen-empire,
biological-ship, wilderness, native target scoring, and pathing rules remain.

Top five risks:

1. **An endangered empire can spend on unsafe expansion.** Threat halves the
   weight, and native expansion planning, target scoring, influence, and system
   pathing still decide whether an outpost is funded and selected.
2. **Threat exactly 50 can fall through both policies.** The outpost modifier
   uses `>= 50`; there is no uncovered equality boundary.
3. **Internal holes and dangerous frontier targets need different treatment.**
   The budget surface cannot identify a chosen target; native system scoring
   remains responsible. Runtime save inspection must distinguish the two.
4. **Alloy and biological-food budgets can diverge.** The same modifier is
   generated and tested in both objects, preserving their resource-specific
   native legality.
5. **More eligible candidates can add planner work.** No iterator, event,
   persistent state, or forced order is added, but observer telemetry must
   verify performance and outpost execution.

Rollback boundary: restore `highest_threat < 50` to each potential and remove
only the two `0.5` modifiers. H07 colonization-latch repair and H09b/H09c remain.

## H09e — Fillable unemployment and underdeveloped-planet candidate pressure

Status: implemented from `autosave_2230.01.01.sav` evidence. Empire 0 had four
colonies with 7.35-22.52 unemployed pops, empty queues, positive income, capped
core banks, and raw district headroom. Nominal open enforcer jobs made the old
`num_unemployed > 0 AND free_jobs < 1` signal false on three colonies; the
fourth satisfied it and still failed downstream candidate selection.

The new country trigger treats actual unemployment as actionable without
assuming nominal jobs are fillable. Economic demand and all three native
mineral planet-budget bands consume that shared trigger. Separately, the one
controlled construction-define experiment raises only
`AI_UNBUILT_DISTRICT_BOOST_MULTIPLIER` from `8.0` to `20.0`; its existing
2.5-pop threshold, free-job caps, opportunity costs, and build thresholds remain.

Top five risks:

1. **Transient unemployment can cause premature construction.** The budget
   effect is additive and candidate selection remains native; existing free-job
   caps and the unbuilt-district population threshold bound actual construction.
2. **Incompatible nominal jobs can mask demand.** The reusable trigger uses
   actual unemployment only and deliberately ignores nominal `free_jobs`.
3. **A global candidate multiplier can overbuild every empire.** Only the
   engine's existing underdeveloped-planet signal changes, from 8 to 20; no
   other construction define is altered in this experiment.
4. **Economic targets can exist without legal candidates.** Save forensics
   confirmed urban district headroom and empty zones, but runtime proof on the
   new build is still required to prove queue creation.
5. **War logistics can crowd civilian construction.** The mineral budget retains
   its 0.65 wartime share factor, but actual unemployment and capped-resource
   pressure remain active during war instead of being vetoed.

Rollback boundary: restore the multiplier to `8.0`, replace the reusable
unemployment trigger with the old free-job conjunction, and regenerate only
the defines, decision-trigger, mineral-budget, and economic-plan artifacts.
