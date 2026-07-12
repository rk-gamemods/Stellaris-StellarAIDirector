# Stellar AI Director Comparative Recovery

- Date: 2026-07-11
- Branch: `codex/stellar-ai-director-comparative-recovery`
- Repository target policy: Stellaris PC 4.4.5 stable
- Observed local source/install baseline: Stellaris PC 4.4.4 rollback, inspected for this recovery
- Validation class: static and deterministic model evidence; no game launch or observer run was authorized

## Purpose

This recovery builds the corrected post-rollback version described in
`C:/Users/Admin/Downloads/stellar_ai_director_comparative_recovery_plan.md`
without restoring the failed c9 strategic-resource overreaction. The controlling
requirements are:

- preserve the useful AI, compatibility, fleet, research, and megastructure work
  that survived the rollback;
- remove scripted fleet mutation and keep production behavior on native AI
  surfaces;
- restore only a bounded ordinary strategic-resource nudge;
- never treat storage capacity, a small stockpile, or small income as a problem
  by itself;
- model simultaneous competition among economic, research, expansion, military,
  influence, queue, slot, job, and megastructure lanes;
- ask for the top five failure modes of every changed hook before accepting it;
- preserve rollback resolution with small, evidence-backed commits.

## Rollback Provenance

The recovery branch started from commit
`12325475bdbad06c83471ce2d9d580d7fd69bf25`. The command
`git diff --exit-code 12325475bdbad06c83471ce2d9d580d7fd69bf25
b1fd00b86555b9b6d2657f6f5f01411f7c2a7ccd` proved the two trees identical.
Commit `f4b55f8` was a behavioral comparison baseline in the report, not the
rollback target. The rollback therefore removed only the c9 delta rather than
reverting the mod to f4-era content wholesale.

The c9 delta had combined two materially different changes:

- a good deletion of a scripted fleet MIA recovery event; and
- unsafe ordinary strategic-resource objects plus phase/scaling subplans whose
  modeled priorities could rise from 562.5 before a deficit to 4,500 during a
  deficit.

The rollback restored the scripted fleet event while correctly removing the c9
economic pressure. Recovery work must therefore restore the fleet deletion and a
much smaller economic behavior independently.

## Preserved Good Work

The comparison and active-source audits found that the rollback retained the
substantial post-f4 work the user did not intend to lose, including:

- parent ownership of the science-cloak components;
- the Forgotten Empires system-route rule correction;
- the Gigas rogue handler and its paired fortress exception;
- the More Events Mod outpost correction;
- tradition, ascension, and research routing improvements;
- the prior removal of constructor `clear_orders` behavior from
  `staid_economy_safety.5`; and
- current native budget, economic-plan, and construction ownership outside the
  specific reverted c9 delta.

These surfaces were not reimplemented wholesale. Recovery changes are narrow and
must preserve their existing generated objects and source provenance.

## Implemented Recovery Slices

### Native fleet ownership

The Director no longer dispatches or defines `staid_economy_safety.3`, and the
generator/validator rejects production uses of `set_mia`, `set_fleet_order`,
`set_fleet_stance`, and `move_to`. Fleet recovery remains native AI behavior.

### Gigas habitat scoring

The active Gigas parent route remains authoritative. Its base factor, core/ideal
system multipliers, orbital-site check, recent-build cooldown, starport veto, AI
habitat cap, and queue hooks are preserved. The Director removed its 125,000 base
and generic-route hard veto. An existing colonizable habitat now applies a 0.1
penalty instead of a zero, and Director planetary-capacity readiness adds only a
factor of 2.

### Ordinary strategic-resource recovery

The broad ESC readiness subplan no longer targets volatile motes, exotic gases,
or rare crystals. It is optional and non-scaling while retaining its existing
advanced-resource and support-economy targets.

A separate additive plan defines exactly three unique subplans. Each is optional,
non-scaling, gated only by the resource's actual `has_deficit`, and targets income
of 1. The Director does not override ordinary strategic-resource objects, add
technology or market gates, script purchases, grant free resources, or force a
producer.

### Cross-priority economic model

The pure model separates facts, policy activation, feasibility, selection,
scheduling, gate transitions, and counterfactual starvation. It models all 12
explicit lanes and treats market income as a temporary bridge rather than earned
recovery.

Important safety contracts include:

- missing trigger facts are indeterminate and fail closed;
- small balanced use is safe regardless of small storage capacity;
- +1/+2 recovery pressure is bounded at the resource level, not multiplied once
  per candidate;
- actual burn caps each increment; `requested_income` records the full bounded
  desired increment, while `remaining_pressure` records only the uncommitted
  portion after durable queued net output;
- partial pending output reduces `remaining_pressure` without shrinking the full
  `requested_income`; a genuinely faster candidate may still pursue that full
  increment, while the same or a slower duplicate is suppressed;
- a slow queued producer caps duplicate slow producers, while only a genuinely
  faster candidate may improve recovery timing;
- exact target fit beats high-priority extreme overshoot;
- long construction is evaluated through completion plus an explicit 12/24-month
  operating-support window;
- a project cannot create an earlier or deeper earned-income runway failure;
- queue, slot, job, budget, influence, resource, and gate state are independent;
- synchronous conflicting gate changes fail instead of depending on rule names;
- starvation comparisons require identical scenarios and a genuine policy-off
  baseline;
- runway collisions remain attributable after a policy choice makes another lane
  individually infeasible;
- Decimal arithmetic uses a private fixed context and is independent of caller
  precision.

### Portable cross-priority evidence pipeline

Commit `ef8860fb` publishes the model evidence independently from gameplay. The
pipeline strictly parses the committed three-resource, optional, non-scaling,
actual-deficit-only +1 plan and publishes seven deterministic outputs with
provenance ID
`a80b2f8a27e481979834963b7f2e831f78cfadc587ff67a5fc81e7543a5ac7e8`.

The published evidence contains 15,021 rows:

- 1,320 legacy timeline rows;
- 10 summary rows;
- 175 active-priority rows;
- 12,486 concurrent-feasibility rows;
- 840 starvation rows;
- 120 activation-matrix rows; and
- 70 counterfactual rows.

Its input fixtures contain 14 checkpoints, 35 candidates, five policy variants,
and 24 activation cases. Internal text provenance is normalized to LF and the
tracked Git attributes preserve the publication byte contract. The external
comparative report is represented by a tracked attestation with raw SHA-256
`e41cc8d6a5a933a8b2507d496057ec6cb7045c0f5611d42208fc4e305d495039`.
An absent local Downloads copy yields the same provenance through the attestation;
a present copy with different bytes is rejected. This ledger is deliberately not
a pipeline input, which avoids circular provenance.

## Top-Five Risk Register

Every production hook, trigger, and model decision surface changed by this
recovery maps to a five-risk cluster below. No other production behavior hook was
added in these slices.

| Changed surface | Five-risk cluster |
|---|---|
| Removal of `staid_economy_safety.3` and its dispatcher | Scripted fleet recovery removal |
| Gigas parent shape plus `ai_colonize_plans > 0` factor 0.1 | Gigas habitat weight |
| `staid_planetary_capacity_growth_ready` factor 2 | Planetary-capacity readiness factor |
| Residual ESC optional/non-scaling exact target map | Residual ESC readiness subplan |
| `has_deficit = volatile_motes` | `has_deficit = volatile_motes` |
| `has_deficit = exotic_gases` | `has_deficit = exotic_gases` |
| `has_deficit = rare_crystals` | `has_deficit = rare_crystals` |
| Policy activation, target fit, and candidate selection | Model activation and candidate selection |
| `requested_income` and `remaining_pressure` | Desired demand versus remaining pressure |
| Pending output and faster-candidate suppression | Pending producer and expedition logic |
| Counterfactual starvation classification | Model starvation attribution |
| Synchronous gate changes and feedback | Gate-cascade transition handling |
| Artifact publication, source hashing, and report attestation | Pipeline provenance and freshness |

### Scripted fleet recovery removal

1. Native fleet recovery may still be weak in an engine edge case; static checks
   cannot prove runtime recovery quality.
2. A stale dispatcher or on-action reference could call the removed event.
3. A queued event in an old save could reference an event no longer defined.
4. A compatibility mod could independently mutate fleet orders and be mistaken for
   Director behavior.
5. A future generator change could reintroduce a forbidden fleet effect unless the
   mod-wide validator remains active.

Controls: dispatcher and definition removed together; forbidden-effect scan is
mod-wide; no runtime claim is made.

### Gigas habitat weight

1. `ai_colonize_plans` scope or meaning could drift in a future Gigas/game version.
2. A 0.1 penalty could still be too permissive in an empire with many idle
   colonizable habitats.
3. A hard zero would recreate deadlock; an excessive multiplier would recreate
   habitat spam.
4. Parent cooldown, starport, cap, or queue veto drift could silently remove a
   safety boundary.
5. Planetary-capacity readiness could be true during a different bottleneck and
   add pressure at the wrong time.

Controls: exact parent-shape fail-fast test; all parent vetoes retained; Director
adds only factor 2; no generic hard zero.

### Planetary-capacity readiness factor

1. The readiness trigger may be true while minerals, alloys, influence, queues,
   or construction capacity are the real bottleneck.
2. A stale or over-broad readiness fact could add habitat pressure for too many
   consecutive checkpoints.
3. Factor 2 compounds with the parent's core and ideal-system multipliers and
   could be larger in practice than it appears in isolation.
4. A future trigger rename or scope change could turn a known false state into an
   indeterminate or wrongly true state.
5. A load-order winner change could move the readiness factor onto a different
   parent object shape.

Controls: the factor is bounded at 2; parent cooldown, cap, starport, queue, and
site vetoes remain authoritative; exact parent-shape tests fail closed; runtime
frequency and magnitude remain an explicit A/B question.

### Residual ESC readiness subplan

1. Its existing OR-based support-ready semantics may exit when only one support
   resource is healthy.
2. Optional/non-scaling behavior may underreact for a genuinely scarce advanced
   resource.
3. Its year-80 activation remains broad.
4. Some advanced resources may have no legal producer for the current empire.
5. Retained energy, mineral, trade, and research targets still compete with other
   active lanes.

Controls: ordinary resources removed; remaining targets unchanged in this slice;
exact-shape generator test; unresolved OR semantics left for separate evidence.

### `has_deficit = volatile_motes`

1. Nomadic construction can consume motes and create a circular recovery route.
2. Mining technology does not prove a current deposit or productive extraction.
3. A chemical plant without sufficient industrial jobs may not yield modeled
   output.
4. Market stock can hide negative earned income without durable recovery.
5. Simultaneous deficits can contend for minerals, jobs, slots, queues, research,
   fleet construction, and megastructures.

Controls: actual-deficit-only +1 target; optional/non-scaling; producer legality
left to parent/vanilla; earned recovery kept separate from market bridging;
cross-lane feasibility artifacts.

### `has_deficit = exotic_gases`

1. Deficit-state cadence can oscillate or reactivate while construction is slow.
2. A refinery route may be legal but not productive because industrial jobs are
   unavailable.
3. Research-building gas use can grow faster than the +1 nudge.
4. Market purchases can clear visible stock pressure without fixing earned income.
5. Gas recovery can consume the same mineral, job, slot, queue, and operating
   headroom needed by research and defense.

Controls: queued net output caps duplicates; slow and timely recovery are modeled
separately; +1 is resource-level; runway starvation is counterfactually reported.

### `has_deficit = rare_crystals`

1. Active ESC independently adds crystal pressure, so merged pressure can exceed
   the Director's +1.
2. A legal crystal plant may lack productive industrial jobs.
3. Market stock can hide negative earned income.
4. A parent-plan or load-order change could introduce a second recovery signal.
5. Simultaneous resource deficits can starve protected non-resource lanes.

Controls: unique Director set names; no ordinary resource object override; merged
source inventory retained; cross-priority and triple-deficit fixtures required.

### Model activation and candidate selection

1. Treating eventual recovery as timely can strand an active deficit.
2. Ignoring eventual queued output can schedule the same slow producer repeatedly.
3. Candidate base priority can overwhelm a +1 target and choose +100 output.
4. Fixed-from-start horizons can miss upkeep that starts after long construction.
5. Global arithmetic context or input order can make an otherwise identical run
   non-deterministic.

Controls: month-by-month queued outlook; candidate-specific faster-than-committed
filter; target fit before producer preference; construction-plus-operation
horizon; fixed Decimal context and canonical ordering.

### Desired demand versus remaining pressure

1. Treating partial pending output as the full desired target can under-request
   recovery and leave a deficit active indefinitely.
2. Treating remaining pressure as a fresh full target can duplicate demand and
   recreate extreme overshoot across several candidates.
3. Zero, fractional, or changing burn can produce unstable increments if bounds
   are rounded or applied in the wrong order.
4. Candidate-local copies of the target can multiply a resource-level +1 policy.
5. If output schemas collapse the two metrics, a safe run can be misread as an
   underreaction or an unsafe run as resolved.

Controls: `requested_income` is the full bounded desired increment and
`remaining_pressure` is the uncommitted remainder; resource-level bounding,
Decimal arithmetic, exact schema tests, fractional cases, and checked-in artifact
freshness enforce the distinction.

### Pending producer and expedition logic

1. A very slow queued producer can suppress a timely legal candidate and strand
   the deficit.
2. Fractional pending output can either suppress too much or schedule repeated
   producers if its net contribution is misclassified.
3. Incorrect completion dates can make the model call a same-speed candidate
   faster and admit a duplicate.
4. Pending consumers can create a pre-zero runway failure that current-income-only
   logic would miss.
5. Weak project identity can compare different projects as if they were the same
   recovery path and create false suppression or false expedition.

Controls: canonical project identity, completion-ordered month-by-month outlook,
full/fractional/slow producer fixtures, pending-consumer fixtures, and a strict
genuinely-faster-than-committed comparison.

### Model starvation attribution

1. Individually affordable lanes can become jointly infeasible through shared
   resources or capacity.
2. Future upkeep can consume runway even when start costs are affordable.
3. A one-time policy choice can permanently remove another lane's feasibility.
4. Comparing different candidates, facts, horizons, or rules can create false
   causal attribution.
5. A policy-on failure without policy-off progress is correlation, not proven
   starvation.

Controls: shared bottleneck reasons include runway; path-dependent infeasibility is
carried forward; scenario fingerprints are required; policy-off progress is
required; minimum consecutive duration remains explicit.

### Gate-cascade transition handling

1. Sequential gate updates can make results depend on rule or input order.
2. Two simultaneous rules can request incompatible values and silently hide a
   genuine conflict.
3. Missing trigger facts can be mistaken for false or safe and admit unsupported
   actions.
4. One policy choice can close a gate permanently and remove another lane from
   later feasibility checks.
5. A horizon ending at construction completion can miss the operating upkeep that
   causes the actual downstream gate collapse.

Controls: tri-state facts fail closed; gate changes are applied synchronously;
conflicting writes are rejected; path-dependent infeasibility is retained; and
construction is evaluated through completion plus 12/24 months of operation.

### Pipeline provenance and freshness

1. Git line-ending conversion can change raw hashes for semantically identical
   internal text.
2. Requiring a machine-local Downloads report can make clean-clone verification
   impossible.
3. Treating any present report as trusted can silently model a different source.
4. Per-file atomic replacement does not make the eight-file publication
   transactionally atomic as a set, so interruption can leave a mixed generation.
5. Including this downstream ledger in model provenance would create a circular
   dependency and unstable rebuilds.

Controls: normalized-LF internal hashes, targeted `eol=lf` Git attributes, a
tracked raw-hash report attestation, rejection of a changed present report,
standalone byte-freshness verification, deterministic reruns, and deliberate
exclusion of this ledger from pipeline inputs. Multi-file transactional
publication remains a documented non-blocking limitation; the verifier detects a
torn set before it is accepted.

## Source and Compatibility Boundaries

Source-of-truth order used for this recovery:

1. current user instruction;
2. repository contracts, schemas, documentation, and the user-supplied
   comparative recovery report;
3. current branch gameplay source, generator, tests, validators, and committed
   pipeline;
4. connected local install, launcher, Irony/load-order, and active parent-winner
   evidence;
5. deterministic model fixtures and generated outputs;
6. Open Brain web-chat summary and later memories as advisory historical context;
7. inference only where no stronger source was available.

The repository policy target is 4.4.5 stable. The inspected machine and active
rollback evidence were 4.4.4, so 4.4.4 vanilla and generated evidence is used
here only as the explicit rollback baseline. Promotion to a 4.4.5 live target
requires a fresh vanilla, active-winner, conflict, and static-validation pass; it
is not implied by the 4.4.4 evidence.

The changed production surfaces are limited to the removed fleet-recovery
dispatcher/event, the copied Gigas habitat weight object, the residual ESC
additive economic subplan, and the new three-resource deficit-only additive plan.
No new event, scripted effect, free-resource path, market purchase, technology
gate, full ordinary-resource object, or forced producer was added.

Active economic-plan contributors inspected for this slice included vanilla,
Gigas, ESC, and the Director. Stellar AI Workshop was installed but disabled.
Producer legality remains complicated by ordinary, Wilderness, Nomad, Arkship,
deposit extraction, and market-only paths, so no small technology predicate was
invented. Separate ownership audits covered the preserved Forgotten Empires,
More Events Mod, NSC3/ship, Gigas, tradition, and science-cloak surfaces; that
does not substitute for the required 4.4.5 revalidation. The recovery assumes
the same DLC entitlements and 116-mod playset used by the audit, preserves parent
DLC/mod toggles, and makes no claim for a different DLC or load-order set.

The recovery branch is intentionally not the live launcher target. At the
recorded audit, the authoritative newer descriptor
`C:/Users/Admin/Documents/Paradox Interactive/Stellaris/mod/StellarAIDirector.mod`
(modified `2026-07-11T23:43:38.915Z`) pointed to
`C:/wt/staid-live-rollback/mods/StellarAIDirector`, a clean tree at
`12325475bdbad06c83471ce2d9d580d7fd69bf25` on
`codex/live-rollback-c9da`. `dlc_load.json` enabled that descriptor last at
zero-based position 115 of 116. Older launcher database/registry cache rows
still reported `C:/wt/staid444-topology/mods/StellarAIDirector`; those older
cache surfaces are stale and inconsistent with the direct descriptor. Stellaris
will not load this comparative-recovery branch until an explicit later promotion.

## Validation Ledger

Completed static checks include:

- mod-wide forbidden scripted fleet-effect checks;
- exact Gigas parent transformation and habitat-route tests;
- strategic recovery exact-shape, negative-contract, parser, and artifact tests;
- local PDX parser checks;
- generated patch validator;
- 41 pure-model unit and adversarial tests;
- 17 pipeline tests covering strict PDX parsing, schemas, activation families,
  concurrency, pending producers/consumers, starvation, provenance, and
  portability;
- manual doctrine checker and standalone byte-freshness verifier;
- legacy model byte preservation and deterministic full rerun;
- absent-report reproduction with unchanged provenance and changed-present-report
  rejection;
- normalized-LF provenance, LF publication, and targeted Git-attribute checks;
- post-commit clean-clone verification under both `core.autocrlf=true` and
  `core.autocrlf=false`, with clean status, identical provenance, all 14
  attributed paths at LF, and the Downloads report absent through a fake home;
- JCodeMunch/JDocMunch freshness checks, including final recovery-ledger index
  verification;
- JDataMunch indexing and integrity validation for all seven outputs and four
  fixture datasets (11 of 11); and
- Python compilation and scoped Ruff checks.

`commands_at_date.txt` was checked and is absent/unarmed.

CWTools was not installed locally (`cwtools` and `cwtools-cli` were not found), so
no check is labeled as CWTools validation. The report's section 11.4 save-analyzer
extensions were not implemented or tested in this recovery. No fresh-game A/B,
observer run, runtime producer start, market timing, deficit-recurrence window,
concurrent-lane threshold, colonization attempt, war/planner threshold, save
migration, or old-save event-queue behavior is claimed. The deterministic model
is evidence about bounded policy behavior, not proof of the engine's choices.
The 4.4.5 promotion pass is also still pending. Pipeline publication replaces
each file atomically but does not transactionally replace all eight publication
files as one set; freshness verification is required after any interrupted run.

## Commit Ledger

Fine-grained recovery commits created before this note:

- `0f19983f` — restore native fleet recovery ownership;
- `a114c8c4` — keep native fleet tests side-effect free;
- `c3c87b76` — enforce economy support safety in model checks;
- `7e7eb5e6` — bound Gigas habitat expansion without deadlock;
- `6f78bd9b` — add bounded strategic-resource recovery;
- `6a07b3ac` — add the bounded cross-priority economy model;
- `37ebd594` — separate full demand from remaining recovery pressure; and
- `ef8860fb` — publish portable cross-priority economy evidence.

The model core, strategic gameplay plan, model pipeline/artifacts, and this
recovery ledger are separate committed slices after their own focused checks.
The ledger does not embed its own self-referential commit SHA. Future work should
preserve this granularity and never combine unrelated rollback or recovery
behavior into one commit.

## Remaining Runtime Questions

- How does the engine combine parent `ai_wants` values with several optional
  additive subplans at the downstream construction score?
- How quickly does vanilla/parent AI select and operate a legal producer after a
  +1 target becomes active, and is +1 sufficient in the tested playset?
- Does engine deficit-state cadence produce visible oscillation or reactivation
  with these non-scaling subplans?
- When does native market bridging occur, how large is it, and can it hide a
  still-negative earned balance?
- Which real bottleneck—minerals, energy, budget, slots, queues, jobs, influence,
  or construction score—dominates under simultaneous pressure?
- How does the merged active stack arbitrate simultaneous motes, gases, and
  crystals deficits while preserving research, expansion, fleet, defense, and
  megastructure opportunities?
- Does the habitat 0.1 penalty produce an acceptable balance between colonizing
  existing habitats and creating new Gigas sites, and how often is the factor-2
  readiness hook active?
- Why can navy coverage reach 1.0 at low absolute power, and do the war planner,
  target selection, reinforcement, and fleet missions remain healthy?
- Which active producer objects win for ordinary, Wilderness, Nomad, Arkship,
  deposit, and refinery paths in the final 4.4.5 playset?
- Do all preserved copied objects and hard vetoes still match the active 4.4.5
  winners after promotion?
- Are old saves with queued removed fleet events clean, noisy, or incompatible,
  and which required state is actually serialized for a future save analyzer?
- Do the report's runtime acceptance windows for producer starts, durable
  recovery, non-recurrence, concurrent lanes, colonization, military growth, and
  wars pass in matched fresh-game A/B cells?

These questions retain the report's sections 13 and 16 as pending acceptance
work. Answering them requires an explicitly approved runtime A/B or observer run
after the 4.4.5 source and active-playset revalidation. The live
`commands_at_date.txt` harness must remain absent until such approval.
