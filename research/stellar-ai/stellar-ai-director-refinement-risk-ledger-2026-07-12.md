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

Status: implemented on the research branch; static validation pending commit.

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
