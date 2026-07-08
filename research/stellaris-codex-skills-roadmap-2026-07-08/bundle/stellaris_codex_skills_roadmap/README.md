# Stellaris Codex Skills Roadmap Bundle

Generated: 2026-07-08

This bundle is a **roadmap and planning artifact** for future Codex skills. It deliberately does **not** contain full skill files, `SKILL.md` bodies, executable mod code, or generated Stellaris script. The files are meant to be ingested by Codex as small planning references before individual skills are authored.

## Architecture summary

Recommended architecture: many small, opt-in skills under a future `skills/stellaris/` namespace. Each skill should cover one repeatable workflow or one narrow knowledge area. Agents should chain multiple skills when needed rather than loading a giant Stellaris modding reference.

The roadmap is split into layers:

1. Foundation/routing skills that decide task scope and evidence needs.
2. Schema/research skills that look up vanilla/CWTools/generated-doc facts without doing implementation.
3. Implementation skills organized by Stellaris file surface and gameplay domain.
4. Validation skills for CWTools, Irony, runtime logs, observer runs, UI smoke checks, and save safety.
5. Compatibility skills for major active-stack mods, kept separate from vanilla/schema skills.
6. Packaging/release skills for descriptor, Workshop, version-bump, and compatibility-patch workflows.

## Important ingestion note

The `proposed_skill_specs/` files are **skill cards**, not finished skills. They are intentionally short and only record:

- purpose;
- trigger;
- do-not-use boundary;
- likely evidence sources;
- related skills;
- priority;
- scope-control notes.

Do not rename these files to `SKILL.md` without writing a real focused skill and testing that it stays small.

## Main files

- `TREE.md` — proposed future directory hierarchy.
- `ROADMAP_TABLE.md` — full grouped roadmap table.
- `FIRST_BUILD_ORDER.md` — recommended first 15 skills and rationale.
- `COMMON_CHAINS.md` — common multi-skill chains for Codex task routing.
- `SOURCE_EVIDENCE_GUIDE.md` — evidence types each skill should prefer.
- `catalog/skills_catalog.json` — machine-readable catalog.
- `catalog/skills_catalog.jsonl` — one skill card per line for chunked ingestion.
- `proposed_skill_specs/<category>/<skill-id>.md` — one small card per proposed skill.

## Counts

- Categories: 11
- Proposed skills: 106
- Must-have skills: 57
- Should-have skills: 32
- Later skills: 17

## Cleanup changes from the chat draft

- Added `stl-ai-personalities`, which the draft referenced indirectly but did not define.
- Split source/evidence maintenance into `stl-source-inventory-maintenance` instead of hiding it under foundation.
- Added `stl-generated-script-docs`, `stl-object-id-inventory`, and `stl-vanilla-overrides-audit` so research tasks stay smaller.
- Added explicit unresolved-schema/runtime skills such as `stl-colony-automation-exception-research` and `stl-ai-catchup-construction-events`.
- Split 4.x-specific areas into `stl-pop-groups-workforce`, `stl-nomads-arkships-waylines`, and `stl-situations-scripted-actions`.
- Added validation-specific cards for ship graph validation, UI smoke checks, generator artifact validation, and custom audit-adapter design.
- Kept active-stack compatibility separate from vanilla implementation skills.
