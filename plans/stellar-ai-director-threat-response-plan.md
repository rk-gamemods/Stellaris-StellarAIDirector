# Stellar AI Director Threat Response Full Implementation Plan

Status: planning document only. No implementation has been performed from this plan yet.
Target game version: Stellaris PC 4.4.4 stable.
Captured: 2026-07-05.

Review annotation, 2026-07-05: this file is now the source brief for the focused plan set in `plans/stellar-ai-director-threat-response/`. Use that folder for implementation handoff, testing, risk mitigation, runtime interaction clarifications, and expanded acceptance gates. Preserve this document as the original integrated plan unless a later design decision intentionally replaces it.

## Summary

Implement a bounded, personality-weighted galactic threat-response layer for Stellar AI Director. This layer reacts to aggressive wars that other empires can observe, but it does not replace vanilla survival logic, Stellar AI economic logic, or Director recovery/deficit gates.

The concepts `moral_outrage`, `regional_fear`, `shared_threat_cooperation`, `conquest_respect`, `punitive_pressure`, `defensive_readiness`, and `opportunism` are not native Stellaris concepts. They are Director-owned design axes stored in the Python generator, compiled into concrete PDXScript artifacts that Stellaris can execute.

V1 outputs only:

- tiered opinion toward the aggressor;
- tiered shared-threat opinion toward victims/other threatened observers;
- timed country/relation flags;
- one small defensive-readiness economy pressure path;
- validation/reporting for unclassified war goals.

V1 explicitly does not force wars, join wars, add punitive CBs, overwrite diplomatic actions, or bypass survival/recovery/deficit gates.

## Verified Stellaris Primitives

Use only primitives verified in the local Stellaris 4.4.4 install:

- `on_war_beginning`
- `is_war_participant`
- `any_attacker`
- `any_defender`
- `random_attacker`
- `random_defender`
- `is_war_leader`
- `using_war_goal`
- event `scopes = { from = ... fromfrom = ... }`
- `script_values` with arithmetic, `min`, `max`, and `value:...`
- `check_variable_arithmetic`
- `set_timed_country_flag`
- `set_timed_relation_flag`
- `has_relation_flag`
- `add_opinion_modifier`
- `remove_opinion_modifier`
- opinion `modifier = { ... }`
- opinion `decay`
- opinion `accumulative`
- existing Director gates:
  - `staid_core_deficit_short_runway`
  - `staid_survival_mode`
  - `staid_recovery_mode`
  - `staid_fleet_buildup_economy_safe`
  - `staid_starbase_defense_economy_safe`

## Generated Files And Isolation

Extend the existing generator-driven Director system rather than hand-writing scattered logic.

Add/extend Python surfaces:

- `tools/stellar_ai_director_lib.py`
  - threat vector tables
  - war-goal classification table
  - score/tier generation helpers
  - threat-response validation helpers
- `tools/generate_stellar_ai_director_patch.py`
  - emits the new threat-response files
- `tools/validate_stellar_ai_director_patch.py`
  - fails on threat-response contract violations
- `tools/tests/test_stellar_ai_director.py`
  - owns deterministic tests for all non-game-launch behavior

Generate new PDXScript files:

- `mods/StellarAIDirector/common/script_values/zzz_staid_threat_response_values.txt`
- `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
- `mods/StellarAIDirector/common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`
- `mods/StellarAIDirector/common/on_actions/zzz_staid_threat_response_on_actions.txt`
- `mods/StellarAIDirector/events/zzz_staid_threat_response_events.txt`
- `mods/StellarAIDirector/localisation/english/staid_threat_response_l_english.yml`

Update durable docs/artifacts:

- `plans/stellar-ai-director-threat-response-plan.md`
- `research/stellar-ai/stellar-ai-director-threat-response-feasibility-2026-07-05.md`
- `research/stellar-ai/stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv`
- `mods/StellarAIDirector/notes/tuning-notes.md`

The threat-response layer remains isolated. It must not modify:

- `staid_survival_mode`
- `staid_recovery_mode`
- `staid_core_deficit_short_runway`
- vanilla or generated `common/diplomatic_actions`
- v1 war declaration / join-war / CB behavior

## Generator-Owned Data Model

Add generator constants:

```python
THREAT_RESPONSE_AXES = (
    "moral_outrage",
    "regional_fear",
    "shared_threat_cooperation",
    "conquest_respect",
    "punitive_pressure",
    "defensive_readiness",
    "opportunism",
)

THREAT_SCORE_LIMITS = {
    "anti_aggressor_score": (0, 100),
    "alignment_with_aggressor_score": (0, 60),
    "defensive_readiness_score": (0, 50),
}

THREAT_ECONOMY_RATIO_CAP = 0.20
THREAT_RELATION_FLAG_DAYS = 7200
```

The generator emits PDXScript values/triggers/objects. Stellaris runtime does not need to know what a design axis means; it only consumes emitted script values, tier triggers, flags, and opinion modifiers.

Runtime state is named and bounded:

- `staid_tr_anti_aggressor_low`
- `staid_tr_anti_aggressor_medium`
- `staid_tr_anti_aggressor_high`
- `staid_tr_anti_aggressor_severe`
- `staid_tr_alignment_low`
- `staid_tr_alignment_medium`
- `staid_tr_alignment_high`
- `staid_tr_defensive_readiness_low`
- `staid_tr_defensive_readiness_high`

Pairwise observer-to-aggressor state uses timed relation flags. Economy readiness uses timed country flags.

## Personality Vectors

Normal ethic contribution is `W`. Fanatic contribution is exactly `3W`.

Normal ethic table:

| Ethic | Outrage | Fear | Cooperation | Respect | Punitive | Defense | Opportunism |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pacifist | +3 | +1 | +2 | -2 | +1 | +2 | 0 |
| Egalitarian | +2 | +1 | +2 | -1 | +1 | +1 | 0 |
| Xenophile | +1 | +1 | +3 | -1 | +1 | +1 | 0 |
| Militarist | -1 | +2 | 0 | +2 | +1 | +2 | +1 |
| Authoritarian | -1 | +1 | -1 | +2 | 0 | +1 | +2 |
| Xenophobe | 0 | +3 | -2 | +1 | +2 | +2 | +1 |
| Materialist | 0 | +2 | +1 | 0 | +1 | +1 | +1 |
| Spiritualist | +1 | +1 | +1 | 0 | +1 | +1 | 0 |

Fanatic examples:

- pacifist outrage `+3` becomes fanatic pacifist outrage `+9`
- authoritarian respect `+2` becomes fanatic authoritarian respect `+6`
- xenophile cooperation `+3` becomes fanatic xenophile cooperation `+9`

Gestalt vectors are separate and do not use moral ethics by default:

| Type | Outrage | Fear | Cooperation | Respect | Punitive | Defense | Opportunism |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hive/machine | 0 | +2 | 0 | 0 | +1 | +2 | 0 |
| Empath/servitor-like | +2 | +2 | +2 | 0 | +1 | +2 | 0 |
| Purifier/devouring/exterminator | 0 | +2 | -3 | +3 | 0 | +2 | +2 |

Civic/personality additions are bounded:

- normal civic contribution max `+1` per axis;
- total civic contribution max `+2` normal-equivalent per axis;
- no civic can bypass caps;
- homicidal/genocidal civics use the special gestalt/homicidal path, not normal moral outrage.

## Score Math

Emit script values equivalent to:

```text
anti_aggressor_score =
  clamp(0, 100,
    severity * 10
    + moral_outrage * 5
    + regional_fear * 5
    + shared_threat_cooperation * 4
    + punitive_pressure * 6
    - conquest_respect * 5
    - opportunism * 3
  )

alignment_with_aggressor_score =
  clamp(0, 60,
    conquest_respect * 6
    + opportunism * 5
    - moral_outrage * 7
    - regional_fear * 3
  )

defensive_readiness_score =
  clamp(0, 50,
    severity * 5
    + regional_fear * 5
    + defensive_readiness * 5
  )
```

Tier cutoffs:

- `anti_aggressor_low`: `25+`
- `anti_aggressor_medium`: `45+`
- `anti_aggressor_high`: `65+`
- `anti_aggressor_severe`: `85+`
- `alignment_low`: `20+`
- `alignment_medium`: `35+`
- `alignment_high`: `50+`
- `defensive_readiness_low`: `25+`
- `defensive_readiness_high`: `40+`

If the emitted PDXScript cannot represent one formula cleanly in one object, the generator emits equivalent tier triggers. The generator remains the source of truth for the math.

## War-Goal Classification

Only explicitly classified war goals can create punitive threat response.

Initial allowlist:

| War Goal | Severity |
| --- | ---: |
| `wg_conquest` | 2 |
| `wg_subjugation` | 3 |
| `wg_humiliation` | 1 |

Context severity modifiers:

- repeated aggressive war within 20 years: `+2`
- observer adjacent to aggressor or victim: `+2`
- victim is federation ally / defensive pact / guaranteed: `+3`
- observer has claims or direct border with aggressor: `+1`
- aggressor is homicidal/genocidal: severe path, still bounded by caps

Unknown or modded war goals:

- severity `0`
- no punitive opinion
- no containment flag
- no defensive-readiness flag
- no CB
- no forced war
- recorded in the classification CSV for later manual review

## Runtime Event Flow

`on_war_beginning` calls one hidden event, `staid_tr.1`.

`staid_tr.1` processes only once per war, when `root` is the attacker-side war leader:

```text
from = {
  any_attacker = {
    is_same_value = root
    is_war_leader = yes
  }
}
```

This prevents duplicate galaxy-wide applications from every participant.

Event flow:

1. Verify attacker war leader.
2. Verify war goal is allowlisted.
3. Save attacker as aggressor.
4. Save representative defender with `random_defender`.
5. Dispatch observer evaluation to aware default countries.
6. Observer event receives:
   - `root` = observer
   - `from` = aggressor
   - `fromfrom` = defender/victim representative
7. Observer computes tier using generated triggers/script values.
8. Observer applies only allowed outputs:
   - timed relation flag toward aggressor;
   - timed country flag for defensive readiness if foreign-affairs safe;
   - opinion modifier toward aggressor;
   - shared-threat opinion toward victim/observers when applicable.

Awareness rule for v1:

- observer must be a default country;
- observer must not be the aggressor;
- observer must have communications or another verified relation/visibility path;
- no omniscient galaxy-wide reaction.

## Opinion Effects And Caps

Anti-aggressor opinion toward aggressor:

| Tier | Opinion |
| --- | ---: |
| Low | -30 |
| Medium | -60 |
| High | -120 |
| Severe | -200 |

Shared-threat cooperation:

| Tier | Opinion |
| --- | ---: |
| Low | +15 |
| Medium | +30 |
| High/Severe | +60 |

Conquest alignment / respect:

| Tier | Opinion |
| --- | ---: |
| Low | +10 |
| Medium | +25 |
| High | +40 |

Stacking rules:

- applying a higher tier removes lower tiers first;
- anti-aggressor high/severe cannot coexist with alignment for the same observer/aggressor pair;
- opinion modifiers decay;
- no opinion path exceeds its cap.

## Economy And Survival Guardrails

Add `staid_tr_foreign_affairs_safe`.

Required for any third-party threat economy response:

```text
NOT = { staid_core_deficit_short_runway = yes }
NOT = { staid_survival_mode = yes }
NOT = { staid_recovery_mode = yes }
is_at_war = no
```

Also require enough resources:

```text
has_monthly_income = { resource = alloys value > 120 }
has_monthly_income = { resource = energy value > 100 }
resource_stockpile_compare = { resource = alloys value > 8000 }
resource_stockpile_compare = { resource = energy value > 5000 }
```

Threat readiness is not used for direct self-defense. If the AI is the defender/victim, vanilla/Stellar AI/Director war and survival logic owns the existential response.

Third-party economy cap:

- existing Director fleet-throughput reserve is `alloys = 35`, `energy = 30`, `naval_cap = 200`;
- third-party threat economy ratio cap is `20%`;
- maximum v1 threat subplan:
  - `alloys <= 7`
  - `energy <= 6`
  - `naval_cap <= 40`

If survival/recovery/deficit/war gate is active, third-party threat economy contribution is exactly `0`.

## Forced-War Restrictions

V1 generated files must not contain:

- `declare_war`
- `join_war`
- `add_casus_belli`
- forced `wg_*` dispatch
- forced punitive event chain
- diplomatic-action override that effectively forces escalation

This is intentional. Event-style forced wars bypass AI intelligence too easily.

Future punitive-war/CB work, if added later, must be a separate phase with:

- direct-threat requirement;
- safe economy gate;
- military capability gate;
- distance/proximity gate;
- cooldown;
- no survival/recovery/deficit state;
- separate tests proving it cannot fire for weak, distant, struggling, unknown-war-goal, or already-at-war empires.

## Automated Test Matrix

Everything that does not require opening Stellaris must be tested.

### Generated Object Validity

- every generated `.txt` file parses with the local PDX parser;
- every generated common file has at least one top-level object;
- every generated object appears in the correct folder;
- no malformed braces;
- no placeholder tokens;
- no empty generated files.

### Name Validity

- every generated object name matches `^[a-z][a-z0-9_]*$`;
- every threat-response object starts with `staid_tr_`;
- event namespace is only `staid_tr`;
- event IDs are unique;
- localization keys exist for visible opinion modifiers;
- no duplicate generated top-level objects unless explicitly classified as an intentional override.

### Reference Validity

- every generated `value:...` script value reference exists;
- every generated scripted trigger reference exists;
- every generated opinion modifier used by events exists;
- every event referenced by on-actions exists;
- every generated localization key referenced by visible content exists;
- every allowlisted war goal exists in vanilla or indexed mod snapshots;
- every unknown/modded war goal remains inert until added to the allowlist;
- no generated reference is missing from `collect_generated_reference_rows`.

### Value Range Tests

- vector values remain within declared axis ranges;
- score values include explicit `min/max` or equivalent clamp;
- anti-aggressor score range is `0..100`;
- alignment score range is `0..60`;
- defensive readiness score range is `0..50`;
- opinion values stay within caps:
  - anti-aggressor `>= -200`
  - shared-threat `<= +60`
  - alignment `<= +40`
- relation/country flag duration equals `7200` days unless changed in one generator constant;
- economy subplan values stay within:
  - `alloys <= 7`
  - `energy <= 6`
  - `naval_cap <= 40`

### Ratio Tests

- every fanatic vector equals exactly `3x` the normal vector;
- every civic addition is within civic cap;
- total civic contribution per axis is within cap;
- third-party threat economy pressure is never above `20%` of the existing fleet-throughput reserve;
- third-party threat economy pressure is exactly `0` when foreign-affairs safety gates fail;
- alignment and anti-aggressor severe cannot both be active for the same pair.

### Survival And Deficit Gate Tests

Fail validation if any third-party threat economy trigger omits:

- `NOT = { staid_core_deficit_short_runway = yes }`
- `NOT = { staid_survival_mode = yes }`
- `NOT = { staid_recovery_mode = yes }`
- `is_at_war = no`

Fail validation if:

- `staid_survival_mode` references any `staid_tr_` trigger;
- `staid_recovery_mode` references any `staid_tr_` trigger;
- threat response modifies core survival/recovery/deficit triggers;
- threat response can produce economy pressure for a struggling third-party empire.

### Unknown War-Goal Tests

- war goal not in `WAR_GOAL_THREAT_CLASSES` has severity `0`;
- unknown war goal emits no punitive opinion;
- unknown war goal emits no readiness flag;
- unknown war goal emits no CB;
- unknown war goal emits no forced war effect;
- unknown war goal appears in the classification audit artifact.

### Forced-War Safety Tests

Fail validation if any generated v1 file contains:

- `declare_war`
- `join_war`
- `add_casus_belli`
- `attacker_war_goal`
- forced punitive `wg_*`
- generated `common/diplomatic_actions`

Also fail if an event path can call a future war/CB effect without:

- direct-threat classification;
- not survival;
- not recovery;
- not deficit;
- not already at war;
- capability gate;
- proximity gate;
- cooldown.

For v1, this path should not exist at all.

### Scenario Matrix Tests

Use generator-level expected-output tests for these profiles:

- pacifist egalitarian observer condemns conquest strongly;
- fanatic pacifist contribution is exactly triple normal pacifist before caps;
- militarist authoritarian observer can respect distant conquest;
- militarist authoritarian adjacent to repeated aggression shifts toward defensive concern;
- xenophobe reacts strongly to nearby aggression but weakly to distant unrelated wars;
- materialist reacts through risk/strategic stability rather than moral outrage;
- gestalt uses fear/survival logic, not moral outrage;
- purifier/devouring/exterminator does not join moral containment logic;
- struggling third-party empire gets opinion state only, no economy response;
- directly attacked empire is not routed through third-party foreign-affairs safety;
- unknown modded war goal produces no punitive state.

## Validation Commands

Required before any launch/observer-game test:

```powershell
python -m unittest tools.tests.test_stellar_ai_director
python tools/generate_stellar_ai_director_patch.py
python tools/validate_stellar_ai_director_patch.py
```

`validate_generated_patch` must include the threat-response checks, so a normal Director validation run catches broken names, objects, references, ranges, ratios, safety gates, and forbidden forced-war effects.

## Acceptance Criteria

- Threat response creates visible diplomatic consequences for aggression.
- Different ethics/civics/gestalts produce materially different reactions.
- Fanatic ethics preserve exact `3x` normal-weight ratios.
- Unknown modded war goals are inert until classified.
- Third-party struggling empires do not spend themselves into collapse.
- Threat economy pressure cannot exceed the declared ratio cap.
- Survival/recovery/deficit gates cannot be bypassed by personality logic.
- V1 cannot force wars, join wars, or add punitive CBs.
- All non-game-launch behavior is covered by deterministic tests and validator failures.
- Observer-game testing is only the final runtime smoke after automated validation passes.

## Assumptions

- Target game version is Stellaris PC 4.4.4 stable.
- V1 is diplomacy/readiness pressure only, not punitive-war automation.
- Direct self-defense remains owned by vanilla/Stellar AI/Director war and survival behavior.
- Major future escalation features require a separate plan and stricter tests.
