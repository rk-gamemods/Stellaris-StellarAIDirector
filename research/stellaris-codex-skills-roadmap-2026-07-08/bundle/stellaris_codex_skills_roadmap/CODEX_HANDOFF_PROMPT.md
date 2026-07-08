# Codex handoff prompt

Use this when asking Codex to ingest the roadmap bundle.

```text
You are ingesting a Stellaris Codex skills roadmap bundle. Treat all files as planning artifacts, not finished skill files. Do not create monolithic Stellaris skills. Load `README.md`, `TREE.md`, `ROADMAP_TABLE.md`, `FIRST_BUILD_ORDER.md`, `COMMON_CHAINS.md`, and `catalog/skills_catalog.json` first. Then load only the per-skill roadmap cards relevant to the current implementation task.

When authoring real skills later:
- create one narrow skill at a time;
- keep implementation skills separate from validation/research skills;
- keep vanilla/CWTools/schema knowledge separate from active-stack mod compatibility knowledge;
- require evidence refresh for live Workshop/mod-page claims;
- do not write full SKILL.md bodies from the roadmap text without narrowing and testing.
```
