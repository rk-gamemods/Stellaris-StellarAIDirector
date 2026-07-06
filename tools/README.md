# Tools

Use this folder for repeatable helper scripts, validators, packaging commands, or analysis utilities for Stellaris modding.

Prefer small, documented tools with clear inputs and outputs.

## Local Validation Surfaces

- Irony Mod Manager is the project-local tool for playset dependency, conflict, and load-order investigation.
- CWTools diagnostics should be used for PDXScript syntax/schema feedback when editing gameplay scripts.
- `python tools/build_stellar_ai_director_object_atlas.py` regenerates the Stellar AI Director object atlas, dependency edges, parent-AI support map, policy matrix, coverage report, and route report.
- Runtime validation should inspect `error.log` first, then `game.log`.
- Use generated script docs, current vanilla files, and source references before trusting an unfamiliar trigger, effect, modifier, scope, or folder path.

Reusable templates and matrices from the attached research bundle are under `research/stellaris-modding-research-bundle-2026-07-04/`.
