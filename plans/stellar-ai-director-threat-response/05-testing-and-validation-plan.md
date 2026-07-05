# Testing And Validation Plan

## Objective

Prove every non-game-launch threat-response behavior with deterministic tests and validator checks before any Stellaris launch or observer smoke test.

## Required Commands

Run these after implementation changes:

```powershell
python -m unittest tools.tests.test_stellar_ai_director
python tools/generate_stellar_ai_director_patch.py
python tools/validate_stellar_ai_director_patch.py
```

Run these for documentation and repo hygiene after plan/docs changes:

```powershell
git diff --check -- plans
```

Refresh and verify the local docs index when generated docs or plans change:

```powershell
jdocmunch-mcp index-local C:\Users\Admin\Documents\GIT\GameMods\StellarisMods --name local/StellarisMods-docs --no-ai-summaries
jdocmunch-mcp verify-index --repo local/StellarisMods-docs
```

Use the active MCP tools when mounted; the CLI commands above are fallback/readback examples, not a replacement for the repo's Munch tool requirement.

## Unit Test Groups

### Data Model Tests

Test that:

- `THREAT_RESPONSE_AXES` contains only expected axis names;
- every normal ethic vector has every axis;
- every fanatic vector equals exactly `3x` the normal vector before caps;
- civic additions cannot exceed per-civic and total caps;
- gestalt and homicidal paths do not use normal moral outrage by default;
- score limits and tier cutoffs are stable and monotonic.

### War-Goal Classification Tests

Test that:

- `wg_conquest`, `wg_subjugation`, and `wg_humiliation` classify with expected severity;
- unknown war goals return severity `0`;
- unknown war goals produce no punitive, readiness, CB, or forced-war output;
- the classification CSV contains all allowlisted rows;
- allowlisted rows include source/evidence/status fields;
- every allowlisted goal is present in vanilla or indexed source snapshots.

### Generation Tests

Test that generated files:

- exist at the expected paths;
- parse with the local PDX parser where applicable;
- contain at least one top-level object where expected;
- use only `staid_tr_` object prefixes for threat response;
- use event namespace `staid_tr`;
- include localization for visible opinion modifiers;
- include no placeholder tokens or empty generated files.

### Reference Tests

Test that:

- every `value:...` reference resolves;
- every scripted trigger reference resolves;
- every opinion modifier used by events exists;
- every event referenced by on-actions exists;
- every localization key referenced by visible content exists;
- file/reference audit rows include the new generated folders.

### Range And Ratio Tests

Test that:

- anti-aggressor score range is `0..100`;
- alignment score range is `0..60`;
- defensive-readiness score range is `0..50`;
- anti-aggressor opinion is never below `-200`;
- shared-threat opinion is never above `+60`;
- alignment opinion is never above `+40`;
- relation/country flag duration equals the generator constant;
- third-party economy values are at most `alloys <= 7`, `energy <= 6`, and `naval_cap <= 40`;
- third-party economy pressure is never above `20%` of the existing fleet-throughput reserve.

### Safety-Gate Tests

Validator must fail if third-party threat economy output omits:

- `NOT = { staid_core_deficit_short_runway = yes }`;
- `NOT = { staid_survival_mode = yes }`;
- `NOT = { staid_recovery_mode = yes }`;
- `is_at_war = no`;
- required income and stockpile checks.

Validator must also fail if:

- `staid_survival_mode` references any `staid_tr_` trigger;
- `staid_recovery_mode` references any `staid_tr_` trigger;
- threat response modifies core survival/recovery/deficit triggers;
- threat response can produce economy pressure for a struggling third-party empire.

### Forbidden-Effect Tests

Fail validation if any generated V1 file contains:

- `declare_war`;
- `join_war`;
- `add_casus_belli`;
- `attacker_war_goal`;
- forced punitive `wg_*`;
- generated `common/diplomatic_actions`.

For V1, any future war/CB effect path should not exist at all.

### Runtime-Flow Contract Tests

Use static generated-text and parsed-object tests to prove:

- `on_war_beginning` hooks only the threat-response dispatcher;
- first event verifies attacker-side war leader;
- participants cannot become third-party observers;
- unknown war goals stop before opinion/economy application;
- awareness gate appears before output application;
- opinion removal happens before opinion application;
- anti-aggressor high/severe and alignment cannot coexist for the same pair;
- defensive-readiness flag can be set only after foreign-affairs safety passes.

## Scenario Matrix

Use generator-level expected-output tests for:

- pacifist egalitarian observer strongly condemns conquest;
- fanatic pacifist contribution is exactly triple normal pacifist before caps;
- militarist authoritarian observer can respect distant conquest;
- militarist authoritarian adjacent to repeated aggression shifts toward defensive concern;
- xenophobe reacts strongly to nearby aggression and weakly to distant unrelated wars;
- materialist reacts through risk/strategic stability rather than moral outrage;
- gestalt uses fear/survival logic, not moral outrage;
- purifier/devouring/exterminator does not join normal moral containment logic;
- struggling third-party empire gets opinion state only and no economy response;
- directly attacked empire is not routed through third-party foreign-affairs safety;
- unknown modded war goal produces no punitive state.

## Manual Runtime Validation

Manual/runtime validation happens only after deterministic checks pass.

Minimum runtime sequence:

1. Generate and validate the patch.
2. Confirm main-menu load proof with the parent playset and Director-enabled playset.
3. Run observer smoke with at least one classified aggressive war.
4. Inspect logs for new Director problem lines, missing localization, invalid references, or repeated event spam.
5. Confirm no forced wars, join-war behavior, or punitive CBs appeared.
6. Record evidence in `mods/StellarAIDirector/notes/observer-test-log.md` and `research/stellar-ai/`.

Runtime smoke is not a substitute for deterministic tests. It only proves that generated files load and basic event behavior does not immediately break in-game.
