# Runtime Interaction Contract

## Objective

Define the exact logical interactions the generated PDXScript must implement so the feature behaves predictably in-game and remains bounded.

## Actors

- Aggressor: attacker-side war leader that began a classified aggressive war.
- Victim representative: one defender-side country selected for V1 shared-threat context.
- Observer: a default country that is neither the aggressor nor any war participant and can plausibly know about the war.
- Direct victim: any defender-side participant. Direct victims are owned by vanilla/Stellar AI/Director war and survival behavior, not the third-party observer economy path.

## Event Trigger

`on_war_beginning` dispatches to one hidden `staid_tr` event chain.

The first event must verify that `root` is the attacker-side war leader before any galaxy or observer iteration occurs. If that check fails, the chain stops with no output.

## Observer Eligibility

An observer must:

- be a default country;
- not be the aggressor;
- not be an attacker-side participant;
- not be a defender-side participant;
- not be a country type that should avoid normal diplomatic logic;
- pass the selected and verified awareness/communications predicate;
- pass any Nomad/Arkship/Waystation/Wayline/Contract compatibility exclusion required by inspected sources.

The awareness predicate must be selected from verified Stellaris 4.4.4 primitives. If only communications is confidently verified, V1 must use communications rather than an invented visibility model.

## War-Goal Classification

Classification precedes all outputs.

Allowed V1 classes:

| War goal | Severity | Runtime behavior |
| --- | ---: | --- |
| `wg_conquest` | 2 | May create opinion/flag/readiness outputs if observer gates pass. |
| `wg_subjugation` | 3 | May create stronger opinion/flag/readiness outputs if observer gates pass. |
| `wg_humiliation` | 1 | May create lower opinion outputs if observer gates pass. |

Unknown or unclassified goals:

- severity `0`;
- no punitive opinion;
- no shared-threat opinion;
- no alignment opinion;
- no readiness flag;
- no economy pressure;
- no CB;
- no forced war;
- audit row only.

## Severity Modifiers

Severity modifiers are allowed only after the base war goal is classified.

Allowed V1 modifiers:

- repeated aggressive war within 20 years: `+2`;
- observer adjacent to aggressor or victim: `+2`;
- victim is federation ally, defensive pact partner, or guaranteed country: `+3`;
- observer has claims or a direct border with aggressor: `+1`;
- aggressor is homicidal/genocidal: severe path, still capped.

Any modifier that cannot be expressed with verified primitives must stay generator-side as an unimplemented row with tests proving it does not appear in generated runtime script.

## State And Direction

Use separate state for separate meanings:

- observer-to-aggressor relation flags for anti-aggressor or alignment state;
- observer-to-victim relation flags for shared-threat state;
- observer country flags for defensive-readiness state;
- aggressor or observer cooldown flags only if needed for repeated-aggression detection or duplicate suppression.

Do not reuse one flag for both "this pair already reacted" and "this aggressor has repeated aggression." Those are different meanings and require different tests.

## Output Precedence

The generated event chain must apply outputs in this order:

1. Stop if root is not attacker war leader.
2. Stop if war goal is not classified.
3. Stop for non-observer countries and participants.
4. Stop if awareness gate fails.
5. Compute generator-owned score/tier outputs.
6. Remove incompatible lower-tier or opposite-polarity opinions.
7. Apply the highest valid anti-aggressor or alignment opinion.
8. Apply shared-threat opinion only to the victim representative unless a bounded multi-victim path is explicitly implemented.
9. Apply defensive-readiness country flag only if `staid_tr_foreign_affairs_safe` passes.
10. Apply economy pressure only from the generated economic-plan path and only while the readiness flag and all safety gates pass.

## Opinion Interactions

Anti-aggressor high/severe and conquest alignment must be mutually exclusive for the same observer/aggressor pair.

Higher anti-aggressor tiers remove lower anti-aggressor tiers before applying. Higher alignment tiers remove lower alignment tiers before applying. Anti-aggressor high/severe removes alignment for the same pair.

Opinion modifiers must decay. If accumulative behavior is used, generated values and removal order must prove the configured cap cannot be exceeded by repeated event applications.

## Economy Interactions

Threat-readiness economy pressure is third-party-only.

It is exactly zero when any of these are true:

- `staid_core_deficit_short_runway = yes`;
- `staid_survival_mode = yes`;
- `staid_recovery_mode = yes`;
- `is_at_war = yes`;
- required monthly income or stockpile checks fail.

If the country is directly attacked, this feature does not decide its direct war economy behavior. Existing vanilla/Stellar AI/Director self-defense and survival behavior owns that response.

## Shared-Threat Interactions

V1 should prefer a bounded observer-to-victim shared-threat opinion over observer-to-observer mesh behavior. A galaxy-wide observer mesh can become expensive and hard to reason about.

If observer-to-observer shared-threat cooperation is implemented later, it must have:

- an explicit cap on affected countries;
- duplicate suppression;
- performance tests or a bounded-loop proof;
- separate interaction tests for federations, defensive pacts, guarantees, vassals, and crisis actors.

## Compatibility Clarifications

Required compatibility cases when implementation touches relevant diplomacy, economy, colony, planet, war, UI, starbase, automation, AI, or modifier behavior:

- Nomads;
- Arkships;
- Waystations;
- Waylines;
- Contracts;
- Stellaris 4.4 Situation Log behavior;
- Gigastructural Engineering war goals, crises, and special country types;
- NSC3 and ship/component expansion scripted country or fleet behavior;
- smarter AI mods and performance optimizers in the active playset.

Compatibility checks do not mean V1 must implement special behavior for each case. They mean the plan must prove the feature either interacts safely or explicitly excludes the case.
