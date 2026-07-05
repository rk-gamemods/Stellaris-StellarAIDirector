# LLM architecture spec for Stellaris empire steering

## Goal

Design an LLM-assisted system that can inspect a Stellaris game state and either advise the player or steer AI empires without pretending that Stellaris PDXScript can host a native LLM.

## Non-goals

- Do not replace the entire native Stellaris AI micro layer in a first version.
- Do not generate raw console commands from the LLM.
- Do not bypass Ironman restrictions.
- Do not leak API keys or save data.

## Reference projects

- Galactic Conclave uses save parsing and a command-file `run` bridge for diplomacy actions. `[S015]`
- Stellaris Overmind uses autosave watching, LLM macro-strategy, and native AI nudges through personality/stat modifiers. `[S016]`
- Stellaris LLM Companion parses saves and exposes strategic advice/MCP context to tools like Codex. `[S017]`

## Recommended component diagram

```text
Stellaris
  | autosave / manual save
  v
Save watcher
  v
Save extractor / parser
  v
Normalized game-state JSON
  v
Visibility + permission filter
  v
Empire profile builder
  v
LLM planner
  v
Strict action schema JSON
  v
Validator
  v
Human approval / policy gate
  v
Action bridge
  |-- mod event flag/variable interface
  |-- console command file + run, for non-Ironman test/control modes
  v
Audit log + training data
```

## State model

Minimum normalized state fields:

```json
{
  "game_version": "4.4.4",
  "date": "2250.01.01",
  "empires": [
    {
      "id": 0,
      "name": "Example Union",
      "ethics": ["ethic_egalitarian"],
      "civics": ["civic_beacon_of_liberty"],
      "is_nomadic": false,
      "economy": {
        "energy": 1200,
        "minerals": 800,
        "alloys": 220,
        "research_total": 450
      },
      "military": {
        "fleet_power": 3100,
        "naval_cap_used": 42,
        "naval_cap_max": 60
      },
      "colonies": [
        {"id": 100, "name": "Capital", "carrier_type": "planet"}
      ],
      "known_neighbors": [1, 2]
    }
  ]
}
```

For 4.4.x, include carrier/colony type so Arkships are not mistaken for normal planets.

## Action schema

Only allow fixed actions:

```json
{
  "type": "object",
  "required": ["empire_id", "strategy", "actions"],
  "properties": {
    "empire_id": {"type": "integer"},
    "strategy": {
      "type": "string",
      "enum": ["FOCUS_TECH", "FOCUS_ALLOYS", "PREPARE_WAR", "DEFEND", "EXPAND", "RECOVER_ECONOMY", "DIPLOMACY"]
    },
    "actions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type"],
        "properties": {
          "type": {
            "type": "string",
            "enum": ["set_strategy_flag", "apply_country_modifier", "set_ai_personality_profile", "recommend_to_player"]
          },
          "flag": {"type": "string"},
          "modifier": {"type": "string"},
          "duration_days": {"type": "integer", "minimum": 30, "maximum": 3600},
          "message": {"type": "string"}
        }
      }
    }
  }
}
```

## Validator requirements

- Reject unknown action type.
- Reject unknown modifier/flag not declared in mod whitelist.
- Reject actions for non-existent empires.
- Reject actions outside allowed game mode.
- Reject hidden-information use if fog-of-war mode enabled.
- Reject destructive actions unless human-approved.
- Log every accepted/rejected action.

## Bridge options

### Option A: Advisory-only

- No game writes.
- Safest.
- Works with Ironman if reading save/logs only, but respect user privacy.

### Option B: Non-Ironman console bridge

- External app writes a command file.
- User/app invokes `run <file>`.
- Galactic Conclave uses this pattern. `[S015]`
- High risk if command file is not fully generated from validated actions.

### Option C: Mod-mediated flag bridge

- External app writes state into a file or commands that set predefined flags/variables.
- In-game mod events react to those flags.
- Less arbitrary than raw console commands.
- Still requires careful validation and non-Ironman testing.

## Security controls

Use Overmind-style controls:

- Do not commit `.env`, `config.toml`, or logs.
- Use environment variables for keys.
- Treat saves as untrusted input.
- Identify prompt-injection vectors.
- Restrict network access for local-only mode.
- Include explicit action whitelist. `[S016]`
