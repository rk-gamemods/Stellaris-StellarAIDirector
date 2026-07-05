# Implementation Slices And Handoff

## Objective

Break implementation into small, reviewable slices with clear gates. Do not merge broad event/economy behavior before the data model and validator can prove the contracts.

## Slice Order

### S0 - Tooling And Source Readiness

Outputs:

- Munch guide calls return content.
- Munch startup assertion passes or records only expected duplicate-stdio warnings.
- Relevant JDocMunch/JCodeMunch indexes are fresh.
- Open Brain memory lookup is performed.

Gate:

- Do not implement while required tool surfaces are stale or failing.

### S1 - Evidence And Classification Prep

Outputs:

- feasibility note under `research/stellar-ai/`;
- initial war-goal classification CSV;
- source evidence for verified primitives and allowlisted war goals.

Gate:

- Unknown war goals must be explicitly inert before event generation starts.

### S2 - Generator Data Model

Outputs:

- constants and table helpers in `tools/stellar_ai_director_lib.py`;
- data model tests;
- no generated runtime hook yet.

Gate:

- Fanatic `3x` tests, civic cap tests, and table-shape tests pass.

### S3 - Generated Values And Triggers

Outputs:

- threat-response script values;
- threat-response scripted triggers;
- static validator checks for names, ranges, and safety gates.

Gate:

- Generated files parse and validator catches seeded broken names/ranges/gates.

### S4 - Opinion Modifiers And Localization

Outputs:

- opinion modifier file;
- localization file;
- tests for caps, decay, exclusivity, and keys.

Gate:

- Repeated-application and mutual-exclusion tests pass.

### S5 - Event And On-Action Flow

Outputs:

- hidden `staid_tr` event chain;
- `on_war_beginning` hook;
- runtime-flow contract tests.

Gate:

- Forbidden-effect tests pass.
- Unknown-war-goal stop-path tests pass.
- Participant exclusion and awareness-gate tests pass.

### S6 - Economy Integration

Outputs:

- capped third-party threat economy pressure path;
- safety gate tests;
- tuning notes update.

Gate:

- Economy pressure is exactly zero under survival/recovery/deficit/at-war failures.
- Economy values stay within cap.

### S7 - Full Validator And Audit Integration

Outputs:

- `validate_generated_patch()` covers all new surfaces;
- file/reference/conflict audits include new generated folders;
- docs and plan status artifacts updated.

Gate:

- `python tools/validate_stellar_ai_director_patch.py` passes.
- Seeded contract breaks fail in tests.

### S8 - Launch And Observer Smoke

Outputs:

- main-menu proof;
- observer smoke notes;
- logs and generated reports under `research/stellar-ai/`.

Gate:

- Run only after S7 passes.
- Stop on new Director problem lines, forced-war behavior, missing localization, or repeated event spam.

## Stop Conditions

Stop and repair before continuing if:

- active Munch guide calls fail;
- the local source corpus is stale for a primitive or war-goal claim;
- deterministic tests fail;
- validation fails;
- generated files require hand edits to pass;
- forbidden effects appear;
- unknown war goals produce output;
- runtime logs show repeated event spam or missing generated objects.

## Handoff Package

At handoff, include:

- files changed;
- generated artifacts;
- source evidence inspected;
- validation commands and results;
- failed commands and reruns;
- runtime evidence if performed;
- remaining risks;
- next recommended action.

Handoff should be saved in Open Brain with who/what/where/when/why/how context and should also be reflected in repo docs or research artifacts when it changes project state.
