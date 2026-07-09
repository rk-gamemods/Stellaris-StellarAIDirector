# Research

Use this folder for Stellaris modding references, vanilla file notes, compatibility findings, and game-version research.

Keep notes source-backed when possible. Include file paths, game version, DLC assumptions, and date checked.

## Primary Guides

| Path | Use |
| --- | --- |
| `stellaris-modding-guide-2026-07-04.md` | Fast-start operational guide for Stellaris 4.4.x mod work. |
| `stellaris-modding-research-bundle-2026-07-04/` | Full attached research bundle with source IDs, reports, matrices, templates, and validation notes. |
| `stellaris-codex-modding-guide-packet-2026-07-08/` | Versioned supplement for the attached Codex modding guide packet, verified against local Stellaris 4.4.5 vanilla files and the active 120-mod playset. |
| `stellaris-codex-skills-roadmap-2026-07-08/` | Preserved consolidated roadmap bundle and indexed source package for creating small, topic-based Stellaris Codex skills. |
| `stellaris-external-gap-research-integration-2026-07-09.md` | Integration note for the 2026-07-09 external Web ChatGPT gap-research packet; preserves all packet files, promotes actionable findings, and records local verification gates. |
| `webchatgpt/external-stellaris-gap-research-2026-07-09/` | Full preserved external packet with main report, 13 Markdown findings docs, source inventory, ranked/actionable gaps, and runtime verification queue. |
| `stellar-ai/war-mechanics-reference-2026-07-08/` | Focused external AI war-mechanics packet for claims, CBs, war goals, declaration gates, personality war fields, war defines, fleet-use separation, and passive-galaxy diagnosis. Use as a research reference, then verify against local vanilla and active-stack files before code changes. |
| `local-stellaris-environment-2026-07-04.md` | Local install, Workshop, launcher, and Irony paths verified on this machine. |
| `stellaris-30-day-research-2026-07-04.md` | Recent modding and game-state research rollup. |
| `stellaris-preferred-collections-2026-07-04.md` | User-preferred collection and compatibility research notes. |
| `stellaris-traits-collection-research-2026-07-04.md` | Updated collection research after adding trait, empire-creation, and immortal-leader preferences. |
| `stellaris-collection-2473560875-instructions-2026-07-04.md` | Deep dive on the recommended collection's author instructions, intended use, optional modules, and modification risks. |
| `stellar-ai/` | Focused research project for Stellar AI as the baseline AI mod and likely center for compatibility adjustments. |
| `steam-collection-2473560875-irony-mod-list-2026-07-04.txt` | Raw Irony clipboard list copied from the collection author's Steam discussion, updated there on 2026-07-02. |
| `steam-collection-2473560875-irony-remoteid-filters-2026-07-04.txt` | Generated remote-ID filter chunks for bulk-selecting collection mods in Irony's Installed Mods panel. |
| `irony-import-workflow-collection-2473560875-2026-07-04.md` | Corrected workflow for using Irony with already-subscribed Steam collection mods; explains ZIP import versus clipboard order import. |
| `stellaris-webchatgpt-reconciliation-2026-07-04.md` | Reconciliation notes for external research packets. |

## Source Bundle Use

The source bundle's Markdown reports cite sources with IDs such as `[S007]`. Resolve those IDs through:

- `stellaris-modding-research-bundle-2026-07-04/source_index.csv`
- `stellaris-modding-research-bundle-2026-07-04/source_index.json`
- `stellaris-modding-research-bundle-2026-07-04/RESEARCH_EVIDENCE_NOTES.md`

For implementation, start with the synthesized guide and then open the specific bundle file for the surface being changed:

- version and porting: `CURRENT_VERSION_AND_STRUCTURAL_CHANGES.md`
- structure and descriptors: `MOD_STRUCTURE_AND_SETUP.md`
- conflicts and load order: `LOAD_ORDER_OVERRIDES_AND_CONFLICTS.md`
- validation: `MOD_SCHEMA_VALIDATION_WORKFLOW.md`
- debugging: `TROUBLESHOOTING_DEBUGGING_AI.md`
- playset maintenance: `PLAYSET_INSTALLATION_MAINTENANCE.md`
- LLM/external bridge design: `AI_LLM_ARCHITECTURE_SPEC.md`
