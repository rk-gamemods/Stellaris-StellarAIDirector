# External Stellaris Gap Research Packet - Filled Answers

Generated: 2026-07-09
Target: Stellaris PC 4.4.x, with 4.4.5 stable as the operating baseline and 4.5 treated as a separate beta/porting branch.

This packet preserves and answers the research questions instead of deleting them. `ranked_research_questions.md` and `answered_research_questions.csv` carry the direct answers. `actionable_research_gaps.csv` is retained because it was requested in the original packet shape, but each row is filled with a researched answer and an implementation action; it is not an unanswered-question list.

Claim labels used throughout:

- **confirmed fact**: primary mod page, official wiki/news, or tool documentation.
- **maintainer claim**: Workshop/mod author/page claim that still needs local source/runtime proof before code depends on it.
- **common player advice**: repeated strategy advice from community sources.
- **anecdotal claim**: one or a few player reports, useful for symptoms/counterplay but not final proof.
- **outdated/version-uncertain claim**: old or version-uncertain advice retained only when it explains a durable concept.
- **local/runtime verification item**: exact active-stack IDs, in-game command syntax, or AI behavior that cannot be externally proven and must be checked against the installed Workshop source or a disposable game.

## Files

- `README.md` - packet map and interpretation rules.
- `main_report.md` - integrated executive report answering all ten research questions.
- `ranked_research_questions.md` - ranked questions with direct answer, decision, confidence, and evidence.
- `answered_research_questions.csv` - machine-readable answered-question table.
- `source_inventory.csv` - all external sources with source type, version relevance, supported claim, confidence, and notes.
- `strategy_findings.md` - 25x/high-powered strategy benchmarks and year-by-year operating targets.
- `gigas_findings.md` - Gigas progression, crises, counters, mandatory routes, and traps.
- `nsc3_esc_fleet_findings.md` - NSC3 + ESC NEXT + Spacefleet Tactica interactions and fleet-design implications.
- `ai_modded_systems_findings.md` - evidence on AI use of high-powered modded systems.
- `console_testing_cheatsheet.md` - command/test examples and verification rules.
- `modding_tools_resources.md` - public tools, schemas, validators, and source references.
- `starbase_defense_findings.md` - Starbase Extended and defense-mod strategy/compatibility findings.
- `planetary_diversity_guilli_findings.md` - PD/Guilli strategy and AI valuation guidance.
- `modded_resources_ui_findings.md` - Gigas/ESC/PD/Guilli resource and UI visibility findings.
- `version_hazards_44_45.md` - 4.4.x and 4.5 hazards for modding and AI systems.
- `actionable_research_gaps.csv` - answered former gap questions with source-backed actions.
- `runtime_verification_queue.csv` - only exact local/in-game checks, not missing external research.
- `packet_manifest.csv` - file manifest.

## How to use this packet

1. Treat source IDs such as `[S029]` as citations into `source_inventory.csv`.
2. Use `confirmed fact` and `maintainer claim` rows to set project defaults.
3. Use `common player advice` rows to set AI route priorities and benchmark targets.
4. Use `anecdotal` rows for bug symptoms and crisis-counter hypotheses, then verify locally before scripting hard dependencies.
5. Use `runtime_verification_queue.csv` only for exact active-stack IDs, `help` output, or observer-run proof.
