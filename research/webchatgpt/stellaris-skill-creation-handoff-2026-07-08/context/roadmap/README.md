# Stellaris Codex Skills Roadmap Source

This directory preserves the consolidated Stellaris Codex skills roadmap bundle
and prepares it as source material for future Codex skill creation work.

## Contents

| Path | Use |
| --- | --- |
| `raw/stellaris_codex_skills_roadmap_bundle.zip` | Original attached bundle, preserved unchanged. |
| `bundle/stellaris_codex_skills_roadmap/README.md` | Bundle entrypoint and usage notes. |
| `bundle/stellaris_codex_skills_roadmap/TREE.md` | Proposed skill directory/topic hierarchy. |
| `bundle/stellaris_codex_skills_roadmap/ROADMAP_TABLE.md` | Full roadmap table for all proposed skills. |
| `bundle/stellaris_codex_skills_roadmap/FIRST_BUILD_ORDER.md` | Recommended initial build order. |
| `bundle/stellaris_codex_skills_roadmap/COMMON_CHAINS.md` | Suggested multi-skill routing chains. |
| `bundle/stellaris_codex_skills_roadmap/SOURCE_EVIDENCE_GUIDE.md` | Evidence expectations for skill creation. |
| `bundle/stellaris_codex_skills_roadmap/proposed_skill_specs/` | Per-topic roadmap cards. These are not finished `SKILL.md` files. |
| `bundle/stellaris_codex_skills_roadmap/catalog/skills_catalog.jsonl` | Machine-readable catalog of 106 roadmap specs. |

## Indexed Surfaces

Use these indexed handles before broad file reads:

| Tool | Handle | Notes |
| --- | --- | --- |
| JDocMunch | `local/stellaris-codex-skills-roadmap-2026-07-08` | 131 docs, 1,767 sections, embeddings disabled. |
| JDataMunch | `stellaris_codex_skills_roadmap_catalog_2026_07_08` | 106 rows, 11 columns, valid index. |

Priority split from the catalog:

| Priority | Count |
| --- | ---: |
| must-have | 57 |
| should-have | 32 |
| later | 17 |

## Use Boundary

Treat this bundle as a roadmap and planning source, not as completed skill
content. Future skill creation should research each topic against current local
Stellaris files, CWTools/schema data, active playset evidence, Irony conflicts,
runtime logs when explicitly approved, and the existing project research before
writing any `SKILL.md`.

Keep skills small, topic-based, and composable. Do not turn this into one large
Stellaris modding skill.
