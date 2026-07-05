# Main Implementation Plan

## Objective

Add the threat-response feature through the existing deterministic generator and validator pipeline. The durable behavior belongs in `tools/stellar_ai_director_lib.py`; wrappers remain thin command surfaces.

## Keep Unchanged

- Keep `tools/generate_stellar_ai_director_patch.py` as the simple `run_all()` wrapper.
- Keep `tools/validate_stellar_ai_director_patch.py` as the simple `validate_generated_patch()` wrapper.
- Preserve existing generated Director files unless a threat-response slice explicitly extends audit coverage or economy plans.
- Preserve existing survival/recovery/deficit trigger semantics.
- Preserve existing V1 main-menu, observer, Irony, and plan-status evidence flows.

## Owner Surfaces

Primary owner:

- `tools/stellar_ai_director_lib.py`

Required implementation consumers:

- `tools/tests/test_stellar_ai_director.py`
- `tools/generate_stellar_ai_director_patch.py`
- `tools/validate_stellar_ai_director_patch.py`

Generated outputs:

- `mods/StellarAIDirector/common/script_values/zzz_staid_threat_response_values.txt`
- `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
- `mods/StellarAIDirector/common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`
- `mods/StellarAIDirector/common/on_actions/zzz_staid_threat_response_on_actions.txt`
- `mods/StellarAIDirector/events/zzz_staid_threat_response_events.txt`
- `mods/StellarAIDirector/localisation/english/staid_threat_response_l_english.yml`

Durable evidence outputs:

- `research/stellar-ai/stellar-ai-director-threat-response-feasibility-2026-07-05.md`
- `research/stellar-ai/stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv`
- `mods/StellarAIDirector/notes/tuning-notes.md`

## Implementation Steps

### I1 - Data Model

Add generator constants for:

- `THREAT_RESPONSE_AXES`
- normal ethic vector table;
- fanatic multiplier constant set to exactly `3`;
- gestalt/homicidal vector table;
- civic/personality additive cap table;
- score limits;
- tier cutoffs;
- opinion values and caps;
- relation/country flag durations;
- economy ratio cap;
- forbidden V1 effect strings.

Add helper functions that return plain serializable rows. Prefer deterministic rows over scattered literals so tests and CSVs can consume the same source.

### I2 - War-Goal Classification

Add `WAR_GOAL_THREAT_CLASSES` with initial entries:

- `wg_conquest`, severity `2`;
- `wg_subjugation`, severity `3`;
- `wg_humiliation`, severity `1`.

Each row must include:

- war goal key;
- severity;
- classification status;
- source evidence path or source label;
- notes;
- whether punitive outputs are allowed.

Unknown lookup must return severity `0`, punitive outputs disabled, readiness disabled, forced-war disabled, and audit status `unknown_inert`.

### I3 - Threat Score Generation

Generate script values or equivalent tier triggers for:

- anti-aggressor score range `0..100`;
- alignment score range `0..60`;
- defensive-readiness score range `0..50`.

If direct formula output is brittle in PDXScript, emit tier triggers that are equivalent to generator-owned score expectations. Do not let runtime PDXScript become the only source of the math.

### I4 - Runtime Trigger Generation

Generate `staid_tr_` scripted triggers for:

- classified war-goal checks;
- observer eligibility;
- awareness/communications gate;
- attacker war leader gate;
- observer not aggressor;
- observer not attacker-side participant;
- observer not defender-side participant;
- third-party foreign-affairs safety;
- anti-aggressor tier checks;
- alignment tier checks;
- defensive-readiness tier checks;
- modifier exclusivity checks.

The third-party economy trigger must include all existing Director safety gates and `is_at_war = no`.

### I5 - Opinion And Localization Generation

Generate opinion modifiers for:

- anti-aggressor low, medium, high, severe;
- shared-threat low, medium, high;
- conquest alignment low, medium, high.

Each visible modifier needs a localization key. Opinion generation must encode decay and stacking behavior consistently with the source plan. Event code must remove incompatible lower or opposite modifiers before applying a higher tier.

### I6 - Event And On-Action Generation

Generate an `on_war_beginning` hook that dispatches to a hidden `staid_tr` event chain.

The chain must:

1. run only for the attacker-side war leader;
2. classify the war goal;
3. stop immediately for unknown or inert war goals;
4. choose a representative defender only for V1 victim/shared-threat output;
5. evaluate only eligible observers;
6. apply only allowed opinion/flag/economy outputs;
7. never call forbidden war effects.

### I7 - Economy Integration

Add a narrow third-party threat readiness economy pressure path. It must:

- be capped at `20%` of existing fleet-throughput reserve values;
- produce at most `alloys <= 7`, `energy <= 6`, and `naval_cap <= 40`;
- be exactly zero when survival, recovery, deficit, or at-war gates fail;
- not route direct self-defense through third-party economy safety;
- remain subordinate to existing Director fleet/starbase economy gates.

### I8 - Validation And Audit Integration

Extend existing generated-file and reference audit coverage so the new folders are not invisible:

- `opinion_modifiers`;
- `on_actions`;
- `events`;
- `localisation/english`.

Add threat-response-specific validation that fails on:

- invalid names;
- missing references;
- missing localization;
- missing safety gates;
- out-of-range scores/opinions/economy values;
- broken fanatic ratios;
- unclassified allowlist entries;
- forbidden forced-war effects;
- missing classification CSV;
- generated output not matching generator tables.

## Contracts And Precedence

- Generator tables precede emitted PDXScript.
- Emitted PDXScript precedes manual notes.
- Validator failures block launch/observer testing.
- Runtime unknown-war-goal behavior must be inert even if research artifacts list unknown candidates for later review.
- Safety gates precede personality-driven outputs.
- Anti-aggressor high/severe opinion beats conquest alignment for the same observer/aggressor pair.

## Out Of Scope

- New diplomatic actions.
- New casus belli.
- War declaration automation.
- Multi-victim galaxy-wide opinion propagation beyond the bounded V1 representative defender behavior.
- Runtime UI or Situation Log integration.
