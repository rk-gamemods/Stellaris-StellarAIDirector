# Source and evidence guide

Generated: 2026-07-08

Use this as a reminder of which evidence source should decide which kind of question.

## Evidence hierarchy by question type

| Question type | Prefer | Use cautiously | Do not overtrust |
|---|---|---|---|
| Allowed keys/path shape | CWTools current schema, vanilla examples, generated docs | Wiki examples | Old forum snippets without version labels |
| Runtime behavior | Runtime logs, copied-save tests, minimal test mods, observer runs | CWTools pass/fail as a precheck | Schema alone |
| Active-stack winners | Irony merged/conflict output, enabled mod order, descriptors | Maintainer load-order notes | Source files from one mod in isolation |
| Public compatibility guidance | Current mod pages, maintainer notes, local descriptors | Collections and comments | Old compatibility patches without update dates |
| Version porting | Verified vanilla snapshots, patch notes, depot diffs | CWTools latest rules | supported_version string alone |
| UI visibility | Runtime screenshots, interface/resource_groups winners, UIOD patch files | Static grep | Resource definition alone |
| Save safety | Patch notes, copied-save smoke tests, new-game smoke tests | Maintainer comments | Assumptions from similar object types |

## Project evidence files worth keeping near this roadmap

- `source_inventory.csv` / `source_index.json` — source provenance and freshness.
- `modding_tools_matrix.csv` — tool capability and limitation inventory.
- `cwtools_schema_surface_matrix.csv` — current public CWTools schema surfaces and gaps.
- `mod_maintainer_guidance_matrix.csv` — active-stack mod guidance.
- `remaining_open_questions.csv` — unresolved semantics and required validation steps.
- Irony merged/conflict exports — final active-stack winners.
- `error.log`, `game.log`, `script.log`, localization logs — runtime truth after launch.

## Freshness rule

Public Workshop pages, GitHub releases, patch notes, and beta guidance are dynamic. A skill that depends on live compatibility should instruct Codex to refresh source evidence before making a release or compatibility decision.
