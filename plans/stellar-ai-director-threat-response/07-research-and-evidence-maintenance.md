# Research And Evidence Maintenance

## Objective

Keep threat-response implementation grounded in current local Stellaris 4.4.4 evidence, source snapshots, and generated audit artifacts.

## Required Research Artifacts

### Feasibility Note

Path:

- `research/stellar-ai/stellar-ai-director-threat-response-feasibility-2026-07-05.md`

Must include:

- target game version;
- local Stellaris install path inspected;
- vanilla files inspected;
- mod source snapshots inspected;
- verified primitives used by the plan;
- primitives intentionally not used;
- compatibility cases reviewed;
- test steps;
- open questions;
- final implementation recommendation.

### War-Goal Classification CSV

Path:

- `research/stellar-ai/stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv`

Required columns:

- `war_goal`;
- `source`;
- `source_path`;
- `mod_or_vanilla`;
- `classification`;
- `severity`;
- `punitive_outputs_allowed`;
- `readiness_outputs_allowed`;
- `forced_war_allowed`;
- `status`;
- `notes`.

Initial rows:

- `wg_conquest`;
- `wg_subjugation`;
- `wg_humiliation`.

Unknown rows discovered from vanilla or mod snapshots must use:

- `severity = 0`;
- `punitive_outputs_allowed = no`;
- `readiness_outputs_allowed = no`;
- `forced_war_allowed = no`;
- `status = unknown_inert` or `needs_review`.

## Source Freshness

Before relying on source claims:

- verify the local docs index for `local/StellarisMods-docs`;
- refresh it if changed docs or source snapshots are missing;
- verify the code index for `local/StellarisMods-223b92bc` before code navigation;
- refresh source snapshots if the active playset or target game version changes.

Do not use stale Munch results to justify primitives, war-goal support, or generated-file contracts.

## Evidence Rules

- Preserve original vanilla or mod excerpts when they justify a behavior.
- Distinguish vanilla war goals from modded war goals.
- Distinguish confirmed runtime primitives from generator-only design concepts.
- Record source path and date for every primitive or war-goal claim.
- If a primitive is unverified, do not emit it in generated files.
- If a compatibility case is uncertain, prefer explicit exclusion over speculative behavior.

## Review Loop

The classification CSV is a maintenance surface, not a runtime permission slip. A war goal becomes active only when:

1. source evidence is recorded;
2. severity is intentionally assigned;
3. expected outputs are defined;
4. unit tests cover the classification;
5. validator checks include the generated behavior;
6. runtime unknown-inert behavior remains covered.

## Compatibility Review Targets

Review when touched by implementation:

- Gigastructural Engineering war goals, crisis actors, special resources, and country types;
- NSC3 scripted country, fleet, starbase, and ship behavior;
- Extra Ship Components and other ship/component expansion mods;
- Starbase Extended and other starbase-defense mods;
- smarter AI mods;
- performance optimizer mods;
- Nomads;
- Arkships;
- Waystations;
- Waylines;
- Contracts;
- Stellaris 4.4 Situation Log behavior.

For each target, classify as:

- safe interaction;
- explicit exclusion;
- unknown inert;
- needs separate plan.
