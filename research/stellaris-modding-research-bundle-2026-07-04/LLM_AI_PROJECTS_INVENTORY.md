# LLM / AI projects inventory and feasibility assessment

## Summary answer

Yes, people have built LLM-adjacent Stellaris tools. The public examples found are external companion applications, not pure in-game mods. The closest to an LLM steering AI empires is **Stellaris Overmind**, which uses an LLM for macro-strategy and then nudges Stellaris native AI through personality/stat changes. It does not replace the native AI’s micro-decision layer. `[S016]`

## Inventory

| Project | Type | What it does | Runtime game control? | Notes |
|---|---|---|---|---|
| Galactic Conclave | External LLM diplomacy app | Parses save, lets player talk to empires, tunes responses to ethos/government, optional APPLY actions through command file + `run`. `[S015]` | Partial, user-approved console bridge | Windows-focused; Ironman injection disabled. |
| Stellaris Overmind | External LLM strategy/AI-steering engine + mod | Watches autosaves; player advisor mode; AI mode chooses macro strategies and applies personality/stat modifiers while native AI handles micro. `[S016]` | Macro steering, not full AI replacement | Closest found to LLM-controlled empires. |
| Stellaris LLM Companion | External save analyzer/advisor | Reads saves, tracks changes, generates strategic advice, MCP relay into Claude/Codex. `[S017]` | Advisory only | Useful for Codex/AI analysis, not empire control. |
| Beachboys Fair AI 2 | Workshop mod claiming ChatGPT-assisted AI rework | Claims AI systems rework designed with ChatGPT; community comments allege unrecognized folders/code. `[S018]` | No evidence of runtime LLM | Treat as cautionary AI-assisted-dev example. |

## Galactic Conclave details

README claims:

- Talk to AIs in a Stellaris save.
- Empires can change minds, declare war, or offer trade deals based on conversation.
- Supports local Ollama or cloud OpenAI/DeepSeek/Anthropic-style providers.
- Reads newest save and lists empires.
- `save_parser.py` parses save files.
- `game_io.py` writes commands to `conclave_cmd.txt` and executes with `run`.
- Each empire response is tuned to government and ethos.
- Ironman mode disables console injection. `[S015]`

Assessment: real LLM-in-the-loop roleplay/diplomacy companion, but not native game AI.

## Stellaris Overmind details

README claims:

- Player Mode watches autosaves, runs the LLM, and produces strategic suggestions.
- AI Mode reads save file, identifies AI empires, generates a ruleset from ethics/civics/origin, and asks the LLM for macro strategy.
- Mod applies personality overrides and stat modifiers.
- Native Stellaris AI handles build queues, research, fleets, and other micro-decisions. `[S016]`

Assessment: best public architecture found for LLM empire steering. It should be treated as a macro-strategy overlay rather than a replacement AI.

## Stellaris LLM Companion details

README claims:

- Reads saves and tracks changes over time.
- Gives actionable strategy in the empire’s voice.
- Covers military, economy, diplomacy, leaders, planets, tech, and more.
- Uses a Rust parser.
- Supports MCP relay into Claude Desktop, Codex, and other MCP-compatible clients.
- Keeps saves local; user brings API key. `[S017]`

Assessment: good source of patterns for Codex consumption and structured save-state analysis.

## Feasible architecture for new LLM empire controller

Recommended components:

```text
1. Save/log watcher
2. Save parser -> normalized JSON
3. Visibility/fog-of-war filter
4. Empire personality/ruleset builder
5. LLM planner with strict JSON schema
6. Validator and safety policy
7. Action-to-Stellaris bridge:
   a. mod event that reads flags/variables, or
   b. console command file executed with `run`, or
   c. human-approved command queue
8. Audit log and replay data
```

Do not attempt:

- Raw LLM API calls from PDXScript.
- Free-form LLM-generated console commands.
- Full replacement of native AI without a robust action API.
- Hidden-information access unless the design intentionally gives the AI omniscience.

## Minimum action schema

Example:

```json
{
  "empire_id": 3,
  "turn_date": "2250.01.01",
  "strategy": "FOCUS_TECH",
  "confidence": 0.72,
  "actions": [
    {
      "type": "set_personality_flag",
      "flag": "my_mod_focus_research",
      "duration_months": 120
    },
    {
      "type": "apply_country_modifier",
      "modifier": "my_mod_llm_research_push",
      "duration_months": 60
    }
  ],
  "rationale": "Weak fleet but strong defensive position and surplus consumer goods."
}
```

Validator rules:

- `type` must be from a fixed enum.
- `modifier` must be in a whitelist generated from mod files.
- `empire_id` must exist in save and be eligible.
- Durations must be bounded.
- No arbitrary script or console command strings.

## Security risks

Overmind’s security notes are directly relevant: prompt injection, code execution through crafted save files/directives/LLM responses, and credential leaks are named concerns; hardening notes advise against committing configs/logs, using environment variables, restricting network access for local mode, and treating saves as untrusted input. `[S016]`
