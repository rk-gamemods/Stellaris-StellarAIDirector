# Troubleshooting, debugging, and AI-assisted inspection

## Install/debug first pass

1. Confirm the outer `.mod` descriptor exists in the user mod directory.
2. Confirm `path` points to the actual mod root.
3. Confirm inner `descriptor.mod` exists.
4. Confirm launcher playset enables the local mod.
5. Remove duplicate local + Workshop copy if both exist.
6. Confirm folder names match recognized game structure.
7. Confirm localisation files are UTF-8 BOM and correctly named.
8. Launch a new game with only this mod.
9. Inspect `error.log`.

Source: descriptor and local/Workshop warning from `[S007]`; localisation rules from `[S008]`.

## Logs

Primary logs:

- `logs/error.log` — syntax/scope/missing key issues.
- `logs/game.log` — custom `log =` effect output and runtime information.
- `crashes/` — crash metadata.

Useful launch parameters listed in the official tutorial:

```text
-script_debug
-debug_mode
-debugtooltip
-logprefix
-logpostfix
-logall
```

Source: `[S007]`

## Temporary logging pattern

```pdx
log = "[my_mod] entering my_mod.0001 root=[This.GetName] day=[GetDate]"
```

Make repeated messages unique if needed because duplicate logs may be suppressed unless using `-logall`. `[S007]`

## Console inspection

The console is available in non-Ironman games; using console commands disables achievements. Use `help` and `help <command>` to confirm commands in the current game version. `[S010]`

High-value commands/categories:

| Command/category | Purpose | Caveat |
|---|---|---|
| `debugtooltip` | Show generated species, leader, empire, ship, pop IDs and hidden state. `[S010]` | Verify output in current version. |
| `event <id>` | Fire/test event. | Scope matters. |
| `effect = { ... }` | Execute ad hoc effects. | Dangerous; use test saves. |
| `observe` | Watch AI empires. | Player relinquishes control. |
| `play <id>` | Switch empire for inspection. | Can alter game state. |
| `ai` | Toggle AI. | Verify command name in 4.4.x. |
| `reload text` | Reload localisation. `[S008]` | Useful for text changes. |
| `switchlanguage l_english` | Language/localisation tests. `[S008]` | May reload localisation. |
| `toggle_string_id` | Show string IDs. `[S008]` | Useful for missing loc. |
| `script_profiler` | Profile scripts. `[S007]` | Use for performance bugs. |
| `trigger_docs` | Generate current trigger docs. `[S009]` | Prefer over stale wiki tables. |
| `run <file>` | Run a command file; used by external bridges such as Galactic Conclave. `[S015]` | Do not expose arbitrary LLM output. |

The current console wiki page was verified for PC 4.2; confirm exact availability in 4.4.x with `help`. `[S010]`

## Common error classes

| Symptom | Likely cause | Fix |
|---|---|---|
| Mod not listed | Bad descriptor path, wrong folder, launcher cache | Recreate descriptors; check user dir; reload launcher. |
| Raw localisation keys shown | Bad filename/header/BOM or missing key | Fix UTF-8 BOM, `_l_english`, `l_english:`. |
| Game loads but feature absent | Wrong folder, duplicate key lost conflict, trigger never true | Check folder path, Irony conflicts, add `log` effects. |
| `error.log` wrong scope | Trigger/effect called from wrong scope | Add scope switch or `exists` check. |
| UI crash | Copied stale `.gui` or conflict | Diff with current vanilla; patch/merge. |
| Performance stutter | Daily/monthly event polling too broad | Use `is_triggered_only`, on_actions, narrower triggers, `script_profiler`. |

## AI-assisted debugging process

Prepare a debug packet:

```text
/game_version.txt
/load_order.txt
/error.log
/game.log
/mod_tree.txt
/files_changed_since_last_working_commit.diff
/vanilla_reference_files/
/reproduction_steps.md
```

AI task prompt:

```text
Debug this Stellaris 4.4.4 PDXScript mod. Do not invent script commands.
Classify each error.log entry. Identify wrong scopes, missing localisations,
duplicate keys, invalid folder paths, stale vanilla overrides, and likely load-order conflicts.
Return a minimal patch and a test plan. Flag any assumption requiring runtime verification.
```

## Direct AI inspection of game state

No supported in-game LLM API was found. Available state channels are:

- Save files.
- Logs.
- Console/debugtooltip.
- Screenshots.
- External command files invoked by `run`.

Public LLM-adjacent projects use external save parsing and optional console bridges, not native LLM-in-engine execution. `[S015] [S016] [S017]`

## Security for AI bridges

For any LLM bridge:

- Do not commit API keys, `.env`, config files, or logs.
- Use environment variables for keys.
- Treat save files as untrusted input.
- Filter fog-of-war information.
- Whitelist actions.
- Validate every LLM action before applying it.
- Never run arbitrary generated console commands.

Overmind’s security notes explicitly identify credential leaks, prompt-injection vectors, code-execution paths via crafted save files/directives/LLM responses, and treating save files as untrusted input. `[S016]`
