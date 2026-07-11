# Tech-World zone-selection failure — 2026-07-10

## Runtime evidence

- Save: `unitedcevantiannation22_-528599974/autosave_2231.07.01.sav`
- SHA-256: `BB0DF96384A7F2D8241BFB57DB9E1EBEF8AEAD32B0E82BC71025E0708355F774`
- Target: Pegasus 4.4.4.
- Indig's Refuge: planet 977, colony 59, designated `col_research` since 2214.08,
  3,537 population units, only 2.7 society research. Its city zones were
  `zone_default`, `zone_trade`, and `zone_foundry`; buildings were the capital,
  robot assembly, medical center, resource silo, and refinery.
- Kojogg's Keep: planet 2037, colony 55, designated `col_research` since 2210.09,
  3,857 population units, zero research. Its seven-level city district used
  `zone_default`, `zone_foundry`, and `zone_factory`; buildings were the capital,
  robot assembly, medical center, and refinery.
- Both planets had open capacity and were queuing another city district.

## Root cause

The Director successfully committed both planets to the Tech-World designation,
but did not connect that designation to zone selection. Commit `b605aa0e` removed
the former direct research-building weight output and relied on vanilla zone
eligibility. Vanilla `building_research_lab_1` explicitly requires
`has_any_research_zone = yes` for AI empires. Because neither planet selected a
research zone, research labs were not candidates at all. Economic-plan research
demand and designation weight cannot cross that eligibility boundary.

## Narrow fix

Copy the four ordinary urban research-zone objects from current vanilla and add
`additional_ai_weight` of 100,000 only when the planet is AI-controlled and has
`col_research`. This changes the missing designation-to-zone edge without
altering building costs, jobs, resource production, research-lab eligibility,
non-research worlds, or human behavior. Once a research zone exists, vanilla
adds researcher jobs and permits the AI to build one research-lab chain.

## Compatibility and validation

- Touched surface: `common/zones`; full-object override risk is limited to
  `zone_research`, `zone_research_physics`, `zone_research_society`, and
  `zone_research_engineering` from Pegasus 4.4.4.
- Active playset was checked through `dlc_load.json`; none of the cataloged
  Workshop research-building override mods found by source search were enabled.
- Static parser, focused regression test, Python compilation, and Director
  validator are required. Runtime proof remains a subsequent save showing a
  research zone and research production on these or equivalent Tech-Worlds.
