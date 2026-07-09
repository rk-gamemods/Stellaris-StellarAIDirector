# External Stellaris Gap Research Integration

Date checked: 2026-07-09

External packet: `C:\Users\Admin\Downloads\external-stellaris-gap-research-2026-07-09.zip`

Packet SHA-256: `EB44203DDD37C7962133CF1DD339139531986E8D815C15DD299B96618285FBA2`

Preserved packet folder: `research/webchatgpt/external-stellaris-gap-research-2026-07-09/`

Primary local context: `research/README.md`, `research/stellaris-webchatgpt-reconciliation-2026-07-04.md`, `research/stellaris-codex-modding-guide-packet-2026-07-08/`, `research/stellar-ai/`

## Integration Decision

Keep the full packet as a preserved external research artifact and add this note as the local integration layer. Do not scatter the packet under a mod-owned directory. The packet is broad stack research for a high-powered Stellaris 4.4.x environment, not source material owned by one mod.

No packet files were excluded. The packet manifest lists 18 files, and all 18 are preserved under `research/webchatgpt/external-stellaris-gap-research-2026-07-09/`.

## Method

Treat the packet as source discovery, synthesis, and backlog input. Promote its findings into local work only when they align with stronger project sources: local vanilla files, active Workshop source, mod source snapshots, Irony conflict/load-order evidence, CWTools/schema checks, runtime logs, save inspection, or approved observer runs.

The packet's own use guidance says to resolve source IDs through `source_inventory.csv`, use confirmed facts and maintainer claims for defaults, use common player advice for route priorities, treat anecdotal rows as hypotheses, and rely on `runtime_verification_queue.csv` for exact active-stack IDs, command help, or observer proof.

## Packet Inventory

| File | Integration status | Reason |
| --- | --- | --- |
| `README.md` | Kept as packet entrypoint | Explains packet use and citation conventions. |
| `main_report.md` | Kept and summarized here | Main synthesis for the high-powered stack. |
| `ranked_research_questions.md` | Kept | Human-readable priority framing for the CSV gap rows. |
| `answered_research_questions.csv` | Kept and indexed | 10 answered topics that mirror `actionable_research_gaps.csv`. |
| `actionable_research_gaps.csv` | Kept and indexed | 10 ranked actionable gaps for future AI Director/playset work. |
| `runtime_verification_queue.csv` | Kept and indexed | 10 local verification tasks where public research is insufficient. |
| `source_inventory.csv` | Kept and indexed | 85 source rows, all accessed 2026-07-09. |
| `packet_manifest.csv` | Kept and indexed | Confirms the 18-file packet inventory. |
| `strategy_findings.md` | Kept | High-powered strategy and benchmark synthesis. |
| `gigas_findings.md` | Kept | Gigastructural progression, threats, and route checklist. |
| `nsc3_esc_fleet_findings.md` | Kept | NSC3, ESC NEXT, and Spacefleet Tactica interaction notes. |
| `ai_modded_systems_findings.md` | Kept | AI-support claims and proof gaps for high-powered mod systems. |
| `console_testing_cheatsheet.md` | Kept | Useful only after local `help` verification in the current game build. |
| `modding_tools_resources.md` | Kept | Tooling/source-order context consistent with repo rules. |
| `starbase_defense_findings.md` | Kept | Defense-mod triage and starbase route implications. |
| `planetary_diversity_guilli_findings.md` | Kept | Planet role scoring inputs for PD and Guilli-style modifiers. |
| `modded_resources_ui_findings.md` | Kept | Resource visibility and UI patch implications. |
| `version_hazards_44_45.md` | Kept | 4.4.x versus 4.5 separation guidance. |

## Source Inventory Shape

The source inventory has 85 rows. Confidence distribution:

| Confidence | Rows |
| --- | ---: |
| high | 38 |
| medium | 30 |
| medium-high | 10 |
| low-medium | 7 |

Largest source-type groups:

| Source type | Rows | Local treatment |
| --- | ---: | --- |
| Reddit community discussion | 19 | Use for common strategy, bug symptoms, and hypotheses only. Verify before hard dependencies. |
| Steam Workshop mod page | 19 | Useful for maintainer claims and current public scope. Verify active local files before implementation. |
| Paradox Wiki | 11 | Good baseline reference, still subordinate to local installed game files. |
| GitHub repository | 8 | Useful for exact source lookup when it matches the active/local mod version. |

## Promoted Findings

These findings are useful enough to make visible in the main research index and future planning:

1. Treat the active high-powered stack as its own balance environment, not vanilla-plus. Gigastructural Engineering, NSC3, ESC NEXT, Spacefleet Tactica, UI/resource patches, and Gigas crises shift benchmarks and dependencies enough that route discipline matters more than generic economic balance. Packet citations: Q1-Q4, sources S001, S025-S029, S033, S038-S039.
2. Preserve aggressive research and alloy conversion as the default AI Director strategic pressure: tech rush or early alloy/conquest, then convert into shipyards, megastructures, and crisis counters by roughly 2275-2300. Packet citations: Q1, sources S016-S024.
3. Keep explicit Director routes for research, Mega Engineering, Gigas special resources, megastructure construction throughput, NSC/ESC technology, shipyard/fleet throughput, and crisis-counter milestones. Packet citations: Q2-Q4, sources S001-S015, S033-S040.
4. Treat NSC3 plus ESC NEXT plus Spacefleet Tactica as a graph-validation problem before AI ship-design generation. Packet citations: Q3, sources S025-S032.
5. Treat Starbase Extended 3.0 as the preferred static-defense candidate over incompatible or stale starbase-level alternatives until local active-stack evidence says otherwise. Packet citations: Q7, sources S041-S046.
6. Treat UI/resource patches as required infrastructure for interpreting high-powered mod behavior, not cosmetic polish. Missing topbar/resource visibility can create false diagnoses for AI bottlenecks and ship-design failures. Packet citations: Q9, sources S047-S053.
7. Use Planetary Diversity and Guilli-style modifier/deposit information as input to role scoring, not as a reason to key AI decisions off planet class names alone. Packet citations: Q8, sources S054-S059.
8. Keep 4.4.5 as the stable local branch target and treat 4.5 as a separate porting branch until parent mods are current and local diff/validation evidence exists. Packet citations: Q10, sources S081-S085.

## Advisory Findings

These findings are kept but should not be treated as implementation proof:

- Community benchmark claims such as 2k+ science by 2240 and 3k+ by 2250 are useful target pressure, but local observer evidence remains the proof surface for AI behavior.
- Gigas, Stellar AI, StarNet, Yagisan, and related AI-support claims are useful source discovery. They do not prove that the active AI can use high-powered systems well.
- Gigas crisis counterplay from player discussions is useful strategic framing. Exact event, project, flag, resource, and megastructure IDs must come from local active source or runtime checks.
- Console command examples are useful prompts for testing, but exact command availability and arguments must be checked in the current local build using in-game `help`.

## Local Verification Queue

The packet identifies these P0 checks where public research is explicitly insufficient:

| ID | Surface | Local check |
| --- | --- | --- |
| RV001 | Console command help | Run `help create_megastructure`, `help effect`, `help research_technology`, `help resource`, `help human_ai`, and `help observe` in the current 4.4.x build before relying on command syntax. |
| RV002 | Gigas object IDs | Parse the active Gigas Workshop source for current tech, megastructure, event, resource, flag, and crisis IDs. |
| RV003 | ESC reactor setting | Confirm the ESC NEXT reactor setting in a disposable game with NSC3 active. |
| RV004 | NSC3/ESC/SFT ship designer | In an all-tech disposable save, test design saving for vanilla and NSC hulls and inspect computer/behavior slots. |

The P1/P2 rows are also retained in `runtime_verification_queue.csv`: Starbase Extended slots/upgrades, URP resource visibility, PD/Guilli active modifiers, Gigas crisis counter flow, AI observer proof, and 4.5 port-branch validation.

## Relationship To Existing Research

This packet complements, rather than replaces, existing local research.

- `research/stellaris-webchatgpt-reconciliation-2026-07-04.md` remains the earlier general Web ChatGPT packet reconciliation for broad 4.4-era playset and tooling choices.
- `research/stellaris-codex-modding-guide-packet-2026-07-08/` remains the local-verified Codex modding guide supplement.
- `research/stellar-ai/` remains the detailed local research and implementation history for Stellar AI Director. The new packet can feed future Stellar AI Director route-planning, but it does not overwrite existing observer results or local generated datasets.
- The packet's public source inventory is subordinate to local source snapshots, active Workshop files, CWTools/Irony validation, and runtime evidence whenever implementation depends on exact object IDs or active-stack behavior.

## Exclusion Ledger

No exclusions. Nothing from the packet was dropped, superseded, or discarded.

The only narrowing decision is promotion level: all artifacts are preserved, while implementation-significant claims remain advisory until verified against local sources or runtime evidence. This is because the packet itself distinguishes confirmed/maintainer/community/anecdotal sources and includes a runtime verification queue for exact active-stack facts.

## Indexed Surfaces

JDocMunch:

- `local/stellaris-external-gap-research-20260709`: indexed 13 Markdown docs, 151 sections, embeddings disabled.

JDataMunch:

- `stellaris_external_gap_packet_manifest_20260709`: 18 rows, 3 columns, validation OK.
- `stellaris_external_gap_source_inventory_20260709`: 85 rows, 9 columns, validation OK.
- `stellaris_external_gap_actionable_research_gaps_20260709`: 10 rows, 8 columns, validation OK.
- `stellaris_external_gap_answered_research_questions_20260709`: 10 rows, 8 columns, validation OK.
- `stellaris_external_gap_runtime_verification_queue_20260709`: 10 rows, 7 columns, validation OK.
