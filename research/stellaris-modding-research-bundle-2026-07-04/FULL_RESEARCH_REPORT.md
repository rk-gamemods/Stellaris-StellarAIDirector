# Stellaris modding research report for mod developers and Codex

Generated: 2026-07-04  
Scope: Stellaris PC mod development for 4.4.x, with 4.4.5 beta and 4.5 beta forward-compatibility notes.  
Source notation: `[S###]` entries resolve in `source_index.json` / `source_index.csv`.

## 1. Executive findings

The correct stable target at the time of this research is **Stellaris 4.4.4 “Pegasus”, checksum 5505**. The official Steam news page reports that 4.4.4 was released on June 24, 2026 and was ready for Steam, GOG, and MS Store. `[S002]`

There is also a **4.4.5 “Pegasus” open beta** on the `stellaris_test` branch. The early beta was posted June 25, 2026 and described as still in development with minimal QA; Dev Diary #427 says the beta was updated again on July 1/2, 2026. `[S003] [S004]`

The current 4.4 series is not merely a small patch line for modders. It combines the already-large 4.0 Phoenix rework with a Nomads/Arkship/Wayline layer. Mods touching population, jobs, planet economy, districts, buildings, planet UI, trade/logistics, empire ownership assumptions, starbases, situations, automation, contracts, or AI economy logic need active testing rather than descriptor-only version bumps. `[S001] [S002] [S004] [S005] [S006]`

The upcoming **4.5 “Cygnus” beta is a separate porting concern**. The Dev Diary #427 notes say pop groups are no longer divided by ethics or factions; instead each pop group has percentages for each ethic/faction, and the notes explicitly state that this is a breaking change that will not preserve save compatibility. Mods using old pop-ethics/faction assumptions, triggers, effects, or UI displays should be branched and ported intentionally. `[S004]`

Local mods should be created in the user Stellaris mod directory, not the game install directory. On Windows, the official modding tutorial places the outer descriptor at `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\`. On Linux, CWTools gives `~/.local/share/Paradox Interactive/Stellaris/mod/`; the Stellaris Mods wiki snippet also lists Linux and macOS mod paths. `[S007] [S013] [S019]`

A local mod needs **two descriptors**: an outer `<mod>.mod` file in the user `mod` directory, and an inner `descriptor.mod` file at the root of the mod folder. The outer file has `path`; the inner file does not. `supported_version` can use a wildcard such as `v4.4.*`, but it is only a visual compatibility indicator in the launcher and does not decide whether code loads. `[S007]`

Load order is not safely summarized as “last mod wins.” Later/lower mods often override earlier/top mods for LIOS-style content, but Stellaris/Clausewitz games have FIOS/LIOS behavior and folder-specific rules. Irony Mod Manager is specifically useful because it understands FIOS/LIOS and reports element-level conflicts rather than relying only on filename collisions. `[S011] [S012]`

There are public LLM-adjacent Stellaris projects, but they are external tools, not native in-engine LLM mods. Galactic Conclave reads saves and uses LLMs for diplomacy, with optional command execution through a generated command file and `run`. Stellaris Overmind is closest to “LLM controlling AI empires,” but its README says the LLM chooses macro strategy and applies personality/stat overrides while Stellaris’ native AI still executes build queues, research, fleets, and other micro decisions. `[S015] [S016]`

## 2. Version and structural-change analysis

### 2.1 Stable and beta target matrix

| Branch | Status at research time | Modder posture |
|---|---:|---|
| 4.4.4 Pegasus | Stable release; checksum 5505; available on Steam/GOG/MS Store | Main public release target. Use `supported_version="v4.4.*"`. |
| 4.4.5 Pegasus beta | Open beta on `stellaris_test`; early beta and updated beta notes exist | Separate beta test branch. Do not publish as stable unless explicitly supporting beta. |
| 4.5 Cygnus beta | Early/open beta path with experimental changes | Separate porting branch, especially for pop/faction/ethics/jobs/UI mods. |

The 4.4.4 patch notes include multiple bugfixes that reveal areas where mods can fail: planet-class modifiers on Arkship colonies, Waystation UI crashes in modded UI cases, Total Wars moving Arkships between owners, and Arkships double-benefiting from Wayline modifiers. Those are not just bugs; they identify compatibility surfaces to regression-test. `[S002]`

### 2.2 4.0 Phoenix: why 4.x mods are not 3.x mods

4.0 Phoenix changed fundamental gameplay data structures. Paradox describes grouping singular pops by species, strata, and ethic; pop groups produce Workforce; Workforce is assigned to jobs; species traits that previously created extra resources now generate bonus workforce when working those jobs; growth is simultaneous across species on a planet; and species modification gained default template/integration behavior. `[S005]`

4.0 also removed the old trade-route model and turned trade into a normal resource/logistical system. It added trade costs for planetary deficits and military fleet logistics, and made trade collection available to Gestalts through Logistics Drones. `[S005]`

The planet economy/UI changed as well: districts provide base jobs, district specializations provide additional jobs per district, buildings provide jobs, and the player assigns/restricts Workforce rather than directly assigning individual pops. `[S005] [S006]`

Practical modding consequences:

- Pre-4.0 job-output assumptions may be wrong because output now depends on Workforce and job efficiency.
- Pop-count scripts and UI displays must respect the x100/pop-group model.
- Mods that modified Clerks, Maintenance Drones, trade routes, starbase trade collection, branch offices, or local deficits require schema review.
- Planet UI mods need full re-evaluation because 4.0 changed planet management surfaces.
- Species modification mods need review for default templates and gradual integration behavior.

### 2.3 4.4 Pegasus/Nomads: the new compatibility surface

Nomads adds empires not bound by normal claimed systems or settled worlds, using Arkships as main habitats. The expansion also adds Wayline Networks, Waystations, Contracts, new Nomad origins, Hero Ships, Stellar Cannon, and new civics/traditions. The free 4.4 Pegasus update adds join/leave-war-in-progress behavior, improved job systems and selection, a reworked Situation Log UI, performance improvements, bug fixes, and related changes. `[S001]`

Practical modding consequences:

- Do not assume `capital_scope` is a normal settled planet.
- Do not assume every empire owns normal colonized worlds or claimed systems.
- Test country/planet scopes against ship-carried Arkship colonies.
- Test planet modifiers and colony modifiers against Arkship colonies.
- Test starbase and orbital-ring logic against Waystations and Arkship equivalents.
- Test UI mods around Situation Log, Waystation UI, Arkship planet view, fleet automation windows, and contract panels.
- Test diplomacy/war mods around join/leave war in progress and Nomad total-war handling.
- Test economy mods around Operational Reserves, Wayline stockpiles, harvesting/strip-mining, passenger satisfaction, and Nomadic resource abundance.

### 2.4 4.4.5 beta modding changes

The updated 4.4.5 beta notes include direct modding-facing changes:

- Situations can define `total_progress` with per-stage `section_weight` and auto-generated progress modifiers/triggers.
- Situations, stages, and approaches support `custom_tooltip` and `custom_tooltip_with_modifiers`; this replaces approach-only `active_tooltip` behavior.
- New scripted trigger: `orbital_ring_and_arkship_equivalent_absent`.
- Starbase modules support `scripted_effect_cooldown`, `scripted_effect_cooldown_flag`, and `scripted_effect_cooldown_flag_desc`.
- `<id>` and `<event_chain>` become optional for `is_point_of_interest`.
- Scripted actions support an `automation = {}` block with options, and fleet-scoped `has_automation_flag` can gate automation weights.
- Scripted action automation blocks support `parent` to nest rows under another action in the settings menu.
- Added `home_colony` and `background_colony` scopes, analogous to planet scopes but generalized to colonies on any carrier type. `[S004]`

Codex implication: if generating situation or automation code for 4.4.5, include a branch check or clear target-version note. Do not use these beta-only fields in a 4.4.4-stable mod unless tested to ensure unknown keys are ignored or harmless.

### 2.5 4.5 beta pop/faction/ethics breaking changes

The 4.5 notes say pop groups are no longer divided by ethics or factions; each group instead has percentage membership. They explicitly say this is breaking and will not preserve save compatibility. `[S004]`

The 4.5 modding notes also include:

- Remove obsolete faction parameters.
- Add `pop_ethic_amount` and `pop_ethic_percentage` triggers.
- Add `pop_force_add_ethic`, `pop_force_remove_ethic`, and `pop_force_transfer_ethic` effects.
- Fix `pop_force_add_ethic` and `pop_change_ethic` triggers.
- Remove deprecated `pop_has_ethic` and `pop_group_has_ethic`.
- Add random anomaly/archaeology/deposit spawn-capability triggers and surveyor parameter for `spawn_random_anomaly`.
- Expose AI naval-cap penalty defines. `[S004]`

Codex implication: for 4.5, never generate old pop-ethic triggers unless the user explicitly targets 4.4 or earlier. For 4.4, avoid prematurely using 4.5 triggers/effects unless the mod branch is beta-only.

## 3. Exact mod structure and storage

### 3.1 Local mod locations

| OS | Directory | Source confidence |
|---|---|---|
| Windows | `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\` | High, official tutorial `[S007]` |
| Linux | `~/.local/share/Paradox Interactive/Stellaris/mod/` | Medium-high, CWTools and Stellaris Mods snippet `[S013] [S019]` |
| macOS | `~/Documents/Paradox Interactive/Stellaris/mod/` | Medium, Stellaris Mods snippet `[S019]` |

The user data folder may be redirected by launch configuration or OS-level Documents redirection. If the launcher does not detect a mod, inspect `launcher-settings.json`, `userdir.txt`, or the launcher UI paths before assuming the mod is malformed.

### 3.2 Required descriptor pair

A local mod needs this minimum structure:

```text
<user Stellaris mod dir>/my_mod.mod
<user Stellaris mod dir>/my_mod/descriptor.mod
```

Outer descriptor:

```pdx
version="0.1.0"
tags={
    "Gameplay"
}
name="My Mod"
supported_version="v4.4.*"
path="C:/Users/YOU/Documents/Paradox Interactive/Stellaris/mod/my_mod"
```

Inner descriptor:

```pdx
version="0.1.0"
tags={
    "Gameplay"
}
name="My Mod"
supported_version="v4.4.*"
```

The official tutorial states that the only difference is the `path` line. It also states that `supported_version` is merely a visual indicator and has no effect on mod loading/code. `[S007]`

### 3.3 Project tree for a gameplay mod

```text
my_mod/
  descriptor.mod
  common/
    governments/
      civics/
        my_mod_civics.txt
    on_actions/
      my_mod_on_actions.txt
    scripted_effects/
      my_mod_scripted_effects.txt
    scripted_triggers/
      my_mod_scripted_triggers.txt
  events/
    my_mod_events.txt
  localisation/
    english/
      my_mod_l_english.yml
  gfx/
    interface/
      icons/
        my_mod_icon.dds
  interface/
    my_mod.gui
```

This mirrors the game installation structure, which is required because Stellaris loads mod content by folder path and file-type-specific rules. `[S007]`

### 3.4 Localisation details

The localisation folder is spelled `localisation`. Each `.yml` file must be UTF-8 with BOM, end in `_l_<language>.yml`, and start with the matching language header such as `l_english:`. `[S008]`

Example:

```yaml
l_english:
 my_mod_civic_example: "Example Civic"
 my_mod_civic_example_desc: "This description appears in game."
```

Do not rely on English fallback for other game languages. The localisation page says missing localisations show as keys; it is common to duplicate English localisation into other language folders if no translation is available. `[S008]`

Use `localisation/replace` only for intentional key overrides. The localisation page describes this folder as loading after other localisation files and using LIOS behavior for duplicate keys. `[S008]`

## 4. Load order, priority, overrides, and patching

### 4.1 Practical model

Use this model while coding:

1. Unique new content generally coexists with other unique new content.
2. Duplicate object keys, duplicate localisation keys, duplicate UI files, duplicate asset paths, and copied vanilla definitions create conflicts.
3. Many conflicts resolve according to load order, but not all. Folder/content rules may be FIOS or LIOS.
4. Compatibility patches should load after the mods they patch unless the relevant rule is FIOS or a folder-specific exception.
5. Use Irony Mod Manager to inspect actual element-level conflicts.

Irony’s documentation says it understands game structures, FIOS/LIOS rules, and deterministic load-order management. A community/author discussion explains why filename-only conflict checking is insufficient and why a mod higher in the list can still win for certain FIOS cases. `[S011] [S012]`

### 4.2 Common conflict cases

| Case | Likely behavior | Risk | Recommended handling |
|---|---|---:|---|
| Two mods add different civics with unique keys | Both load | Low | Unique prefix and filenames. |
| Two mods define same civic key | One definition wins or errors, depending folder/rule | High | Patch merged definition; avoid duplicate keys. |
| Mod file named like vanilla `00_civics.txt` | Can override or shadow broad vanilla data | High | Use `my_mod_civics.txt`; official tutorial warns against `00_civics.txt`. `[S007]` |
| Duplicate localisation key | Later/replace key normally wins | Medium | For intentional text override, use `localisation/replace`; otherwise unique keys. `[S008]` |
| UI file copied from vanilla | Later file may replace entire UI file; changes are hard to merge | Very high | Patch manually; keep diffs minimal; test UI screens. |
| Two mods edit same on_action block | One may override or both may append depending file/schema behavior | High | Inspect vanilla and Irony; merge into compatibility patch. |
| Asset path collision | One image/model/asset can replace another | Medium-high | Unique paths and asset names. |
| `replace_path` use | Whole vanilla/mod path can be replaced | Very high | Use only for total conversions or deliberate destructive overrides; test thoroughly. |

### 4.3 Patch mods

A compatibility patch mod should:

- Contain only merged/bridging definitions.
- Be placed below/after the source mods in the launcher or Irony collection unless a known FIOS exception dictates otherwise.
- Use clear dependencies in its Workshop description even if descriptor-level dependencies are not enforced.
- Include a README listing which object keys are patched.
- Be versioned separately from the parent mods.

## 5. Scripted versus nonscripted mods

### 5.1 Scripted mods

“Scripted” in Stellaris means Paradox/Clausewitz script, not Python/Lua/JavaScript. These are mostly `.txt` files under `common/`, `events/`, `decisions/`, `situations/`, `on_actions/`, `scripted_effects/`, `scripted_triggers/`, and related folders.

Common scripted content:

- Civics, authorities, origins, governments.
- Buildings, districts, jobs, planet designations, deposits.
- Technologies, traditions, ascension perks, edicts, policies.
- Ship sizes, components, starbase buildings/modules, scripted actions.
- Events, anomalies, archaeological sites, special projects, situations.
- AI weights, economic plans, personalities, defines.
- Scripted triggers/effects/loc and on-actions.

Scripted mods are most likely to change checksum, break saves, conflict with overhauls, or require porting after 4.x structural changes.

### 5.2 Scopes and script correctness

Most objects expose scopes: planet, pop, country, fleet, ship, etc. Special system scopes include `THIS`, `PREV`, `FROM`, and `ROOT`. The Scopes page emphasizes that `ROOT` and `THIS` can be unintuitive in scripted effects/triggers and on-actions. `[S009]`

Always check potentially missing scopes before switching into them:

```pdx
if = {
    limit = { exists = owner }
    owner = {
        # safe owner-scoped effects here
    }
}
```

The Scopes page states that wrong-scope triggers produce `error.log` entries and may cause the rest of the code to fail or produce unintended results. Effects on non-existent scopes may silently do nothing. `[S009]`

### 5.3 Nonscripted/content mods

Nonscripted/content-only mods usually change presentation rather than core gameplay:

- Localisation-only text edits.
- Portraits, flags, city sets, icons, event pictures.
- Music and advisor/audio assets.
- UI layout and GUI assets.
- Namelists and cosmetic entity/asset definitions.

These can still conflict. UI mods are especially fragile because they often copy large vanilla `.gui` files. Asset path collisions and localisation key collisions are common. A “cosmetic” UI mod can still break game screens after a major update.

### 5.4 External companion tools

External tools are not pure Stellaris mods. They parse saves, watch logs, inspect playsets, call LLMs, or emit console commands. They are the most plausible architecture for LLM-assisted gameplay because Stellaris script does not expose a native HTTP/client runtime in public modding surfaces found in this research.

Examples: Galactic Conclave, Stellaris Overmind, Stellaris LLM Companion. `[S015] [S016] [S017]`

## 6. Best practices and maintenance workflow

### 6.1 Toolchain

Recommended baseline:

- VS Code + CWTools extension.
- Paradox Syntax Highlighting.
- Git from the first commit.
- WinMerge/Meld/Beyond Compare or equivalent directory diff tool.
- Irony Mod Manager for playset and conflict inspection.
- CWTools CLI / cwtools-action for CI validation.
- GIMP/Paint.net or equivalent for assets.
- 7-Zip for packaging and save-file inspection.

The official tutorial recommends VS Code/CWTools and notes CWTools can highlight errors, autocomplete, generate missing localisation lists, comment/uncomment blocks, and format documents. `[S007]`

CWTools’ own docs recommend backups, Git, opening the mod folder as a project, selecting the vanilla folder, and waiting for scans/errors. `[S013]`

cwtools-action uses the CWTools CLI for automated PDXScript analysis and requires validation rules plus a vanilla cache; the full cache is needed for more accurate validation involving load order and file overrides. `[S014]`

### 6.2 Repository layout

Recommended repository:

```text
stellaris-my-mod/
  README.md
  CHANGELOG.md
  LICENSE
  docs/
    compatibility.md
    porting-notes-4.4.md
    porting-notes-4.5.md
  mod/
    my_mod.mod.template
    my_mod/
      descriptor.mod
      common/
      events/
      localisation/
  tools/
    validate.py
    package.py
  test-notes/
    4.4.4-clean-playset.md
    4.4.5-beta.md
    4.5-beta.md
```

Use branches like:

- `main` or `stable-4.4`
- `beta-4.4.5`
- `port-4.5`
- `compat/<other-mod-name>`

### 6.3 Version discipline

- Do not release a version bump without running a clean 4.4.4 game.
- Tag releases with both mod version and tested game version, e.g. `v0.4.2-stellaris-4.4.4`.
- Keep a migration note for every vanilla object override.
- Keep a list of “known full-file copies” because those are highest risk after patches.
- Maintain a regression save/playthrough that exercises every feature.

### 6.4 AI-assisted coding discipline

AI can help generate scaffolds, refactor repetitive PDXScript, summarize patch notes, generate test matrices, and analyze logs. It should not invent folder names, triggers, effects, modifiers, or scopes without validation against current vanilla files, generated `trigger_docs`, CWTools, or the wiki. The Beachboys Fair AI Workshop listing is a cautionary example: it claimed ChatGPT-assisted AI-system work, while comments alleged unrecognized folders and nonworking/syntax-invalid code. `[S018]`

Codex should be instructed to:

1. Read the current vanilla file for the target folder before generating changes.
2. Use only existing folders unless intentionally creating recognised new files under a recognized path.
3. Prefer additive unique-key files.
4. Run/expect CWTools validation.
5. Scan `error.log` after loading.
6. Treat unknown effect/trigger/modifier names as suspicious until validated.

## 7. Troubleshooting and debugging

### 7.1 Install/path checklist

- Is `<mod>.mod` in the user `mod` directory?
- Does `<mod>.mod` have the correct absolute or relative `path`?
- Is `descriptor.mod` inside the mod root?
- Does the launcher playset enable the mod?
- Is there both a local copy and Workshop subscription of the same mod? The tutorial warns Stellaris may refuse to load a mod subscribed from the Workshop and present as a local mod simultaneously. `[S007]`
- Are paths case-correct on Linux/macOS?
- Is the user data folder redirected?

### 7.2 Logs and launch parameters

Use `error.log` and `game.log` first. The official tutorial identifies these logs and crash folder behavior. It also lists useful launch parameters including `-script_debug`, `-debug_mode`, `-debugtooltip`, `-logprefix`, `-logpostfix`, and `-logall`. `[S007]`

Temporary logging pattern:

```pdx
log = "[my_mod] reached my_mod.0001 immediate for root=[This.GetName]"
```

The tutorial notes duplicate log messages can be suppressed unless made unique or run with `-logall`. `[S007]`

### 7.3 Console and runtime inspection

The Console Commands page says the console is available in non-Ironman games, can be opened through keyboard shortcuts depending on layout, and using console commands disables achievements. It also says `help` prints commands and `help <command-name>` gives command descriptions/parameters. `[S010]`

Useful command categories:

- `debugtooltip`: show generated IDs and hidden state; wiki specifically cites species, leader, empire, ship, and pop IDs as debugtooltip-derived. `[S010]`
- `observe`: watch the galaxy while AI plays.
- `play <empire id>`: switch country for inspection.
- `ai`: toggle AI.
- `event <event_id>` or selected-scope event execution: test events manually.
- `reload text`: reload localisation.
- `switchlanguage l_english`: language-switch test.
- `trigger_docs`: generate trigger docs for current version.
- `script_profiler`: measure script performance.

Because the console page was verified for PC 4.2, verify exact command names in 4.4.x with in-console `help`. `[S010]`

### 7.4 AI-assisted debugging workflow

Provide the AI/Codex with:

- Target Stellaris version and checksum.
- Full mod folder tree.
- Files changed since last working version.
- Current `error.log` and relevant `game.log` excerpts.
- Active playset/load order.
- Vanilla reference file(s) for any overridden folder/object.
- The exact reproduction steps and save if applicable.

Prompt pattern:

```text
You are debugging a Stellaris 4.4.4 mod. Do not invent triggers/effects/folders.
Use only PDXScript patterns shown in the provided vanilla files or official docs.
First classify each error.log line by file/key/scope.
Then produce a minimal patch. Prefer additive unique-key files.
Flag anything requiring runtime verification.
```

Good AI tasks:

- Map `error.log` lines to exact files.
- Detect duplicate object IDs/localisation keys.
- Compare a copied vanilla file against current vanilla.
- Generate event-log instrumentation.
- Convert repeated trigger conditions into `scripted_triggers`.
- Produce a 4.5 porting TODO list from deprecated triggers/effects.
- Draft an Irony compatibility patch map from conflicts.

Bad AI tasks:

- Inventing folder names or triggers not found in vanilla/current docs.
- Writing full AI economy systems without schema validation.
- Making broad file replacements from memory.
- Generating console command execution from untrusted LLM output.

### 7.5 Direct AI inspection of game state

No supported native in-game LLM inspection API was found. Direct options are indirect:

- In-game console and debug tooltips.
- Logs (`error.log`, `game.log`, script `log` effect).
- Save-file parsing by external tools.
- Screenshots/vision if a human or automation captures UI.
- Console command files invoked by `run`, as demonstrated by Galactic Conclave. `[S015]`

The best current architecture for AI game-state inspection is an external process that watches autosaves and logs, parses the save into structured JSON, feeds that to the LLM, constrains output to a whitelist of actions, and applies only approved effects through a mod event or console bridge.

## 8. LLM/AI projects

### 8.1 Galactic Conclave

Galactic Conclave is a Windows-focused LLM diplomacy companion. Its README says it lets the user talk to AIs in a Stellaris save; it reads the newest save, lists empires, tunes responses to government/ethos, supports local Ollama or cloud LLM APIs, and writes commands to `conclave_cmd.txt` executed through Stellaris’ `run` command. It detects Ironman and disables console injection to avoid modifying the save. `[S015]`

Interpretation: this is real LLM-in-the-loop diplomacy tooling, but not a native in-engine LLM and not a full empire AI controller.

### 8.2 Stellaris Overmind

Stellaris Overmind is the closest found project to “LLM in charge of AI empires.” Its README describes a Player Mode that watches autosaves and produces strategic suggestions. Its AI Mode reads the save, identifies AI empires, generates a ruleset from ethics/civics/origin, has an LLM choose macro strategy, then applies personality overrides/stat modifiers. The README explicitly says Stellaris’ native AI handles micro-decisions such as build queues, research, and fleets. `[S016]`

Interpretation: this is macro-strategy steering, not replacement of the native AI. It is a plausible architecture to extend.

### 8.3 Stellaris LLM Companion

Stellaris LLM Companion reads saves, tracks changes over time, and gives actionable strategic advice in the empire’s voice. It uses a Rust parser and includes MCP relay support for Claude/Codex-style clients. `[S017]`

Interpretation: useful for AI-assisted analysis and strategy advice, not direct empire control.

### 8.4 AI-assisted Workshop mods

Beachboys Fair AI 2 claims to be an AI-system rework designed with ChatGPT. Community comments on the listing allege the mod contains folders/code not recognized by the game and syntax that does not work. `[S018]`

Interpretation: treat as a cautionary example. AI can accelerate PDXScript work only when constrained by vanilla schemas, CWTools validation, log inspection, and runtime testing.

## 9. Architecture recommendation for an LLM empire controller

A serious LLM-controlled empire system should not try to put raw LLM code inside Stellaris script. Use a hybrid architecture:

```text
Stellaris save/logs
    -> external parser
    -> normalized game-state JSON
    -> rules / fog-of-war / permission filter
    -> LLM planner
    -> strict action schema
    -> validator
    -> human approval or policy gate
    -> mod event / console command bridge
    -> audit log
```

Design constraints:

- Never let the LLM output arbitrary console commands.
- Use action IDs and parameter schemas, not free-form script.
- Keep hidden information filtered if the AI is supposed to obey fog of war.
- Treat save files as untrusted local input.
- Do not commit API keys, configs, or logs.
- Prefer local LLM mode if privacy or network isolation matters.

Overmind’s security notes identify prompt-injection vectors, code-execution paths via crafted save files/directives/LLM responses, and credential leaks as relevant risks, and advise not committing configs/logs and treating saves as untrusted input. `[S016]`

## 10. Validation caveats

This report intentionally distinguishes stable facts from required validation:

- Stable: descriptor pair, folder mirroring, localisation BOM/naming, logs, and basic debug tooling.
- High confidence: 4.4.4/4.4.5/4.5 version status from official Steam/Paradox sources.
- Medium confidence: full folder-by-folder override semantics, because the accessible current Modding page was client-challenge blocked and Irony/actual game files should be used for exact FIOS/LIOS behavior.
- Must validate in target environment: exact console command availability on 4.4.x, because the console wiki page was verified for PC 4.2.
- Must validate in actual code: any public LLM project claims; repo READMEs prove architecture claims, not runtime quality.
