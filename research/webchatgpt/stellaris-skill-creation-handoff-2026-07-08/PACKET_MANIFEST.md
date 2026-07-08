# Stellaris Skill Creation WebChatGPT Context Packet

Created: 2026-07-08

Purpose: provide WebChatGPT with enough context to author baseline/core Stellaris Codex skills without drifting into third-party compatibility work.

Packet rule: at most 40 files total.

## Included File Groups

- Prompt and manifest for WebChatGPT.
- Repository and project rules.
- Roadmap catalog, build order, category indexes, and completion ledger.
- Skill creator instructions for valid Codex skill structure.
- Stellaris baseline modding research and validation docs.
- Stellar AI Director local mod files and tools as project context, not as a request to prioritize Stellar AI compatibility.

## Priority Instruction

The external model should focus on baseline/core roadmap skills first:

- foundation;
- schema and research;
- script surfaces;
- AI economy and planets;
- gameplay domains;
- ships, war, and starbases;
- megastructures;
- UI, localization, and assets;
- validation and diagnostics;
- packaging and release.

The external model should defer mod-specific `09_compatibility` rows until after the core categories are done.
