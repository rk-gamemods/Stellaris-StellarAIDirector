# Research evidence notes

This file is meant for Codex or another agent that needs to reason from source-backed observations without re-reading the full report. Source IDs resolve in `source_index.json`.

## S001 — Paradox Nomads + 4.4 Pegasus launch

Observed facts:

- Publication date: June 15, 2026.
- Nomads and the free 4.4 Pegasus update were available on PC.
- Nomads centers on Arkships, interstellar trade routes, contracts, favor/resources/influence, and not claiming/colonizing in the usual way.
- Free 4.4 update adds join/leave wars in progress, improved job systems and selection, reworked Situation Log UI, performance improvements, bug fixes, and more.
- Feature list includes Nomadic Empires, Arkships, Wayline Networks, Contract System, new origins, Defender of the Galaxy, Stellar Cannon, Champions Forge Live, paragons, civics, traditions.

Modding implications:

- Do not assume all empires have a normal settled capital planet.
- Do not assume all colony scopes are standard planet colonies.
- Treat Arkship UI, Waystations, contracts, and Situation Log as new UI compatibility surfaces.
- War/diplomacy mods need tests for join/leave-war behavior and Nomad empire cases.

## S002 — 4.4.4 patch

Observed facts:

- Title says “Stellaris 4.4.4 patch released (5505)”.
- Date shown: Jun 24.
- Notes say 4.4.4 should be ready for download via Steam, GOG, and MS Store.
- Fixes/improvements include AI contract abandonment, Arkship/logistic ship notifications, Logistics Hub indicator, Arkship random names using ship namelists, and many Nomad fixes.
- Particularly relevant bugfixes: planet class modifiers apply to Arkship ship-carried colonies; Waystation UI crash with some modded UI; Total Wars between Nomads move Arkships between owners; Arkships no longer double-benefit from waystation/wayline modifiers; doomsday embarking modifier fixes.

Modding implications:

- Stable target is 4.4.4 unless 4.4.5 beta is explicitly requested.
- The patch notes expose regression targets for mods touching planets, Arkships, UI, wars, modifiers, or Waylines.

## S003 — 4.4.5 early beta

Observed facts:

- Steam news says 4.4.5 early beta went up on `stellaris_test`.
- Notes say it was expedited and had minimal QA review.
- Features include Resource Abundance slider, Waystation Voidlure modules, Arkship Voidlure Array, and fleet automation settings/behavior changes.

Modding implications:

- Treat 4.4.5 as beta branch, not stable branch.
- Automation and resource generation changes can alter AI/economy scripts and testing baselines.

## S004 — Dev Diary #427 / 4.4.5 updated beta / 4.5 beta

Observed facts:

4.4.5 modding additions:

- Situation `total_progress` and per-stage `section_weight`.
- Situation/stage/approach `custom_tooltip` and `custom_tooltip_with_modifiers`.
- New scripted trigger `orbital_ring_and_arkship_equivalent_absent`.
- Starbase modules support scripted-effect cooldown fields.
- `is_point_of_interest` optional `<id>` and `<event_chain>`.
- Scripted action automation block with options and parent nesting.
- Fleet-scoped `has_automation_flag`.
- `home_colony` and `background_colony` scopes.

4.5 beta changes:

- Pop groups no longer divided by ethics/factions; instead each pop group has percentages.
- Notes explicitly say this is breaking and will not preserve save compatibility.
- Modding notes remove obsolete faction parameters, add `pop_ethic_amount`/`pop_ethic_percentage`, add `pop_force_add_ethic`/`pop_force_remove_ethic`/`pop_force_transfer_ethic`, remove deprecated `pop_has_ethic` and `pop_group_has_ethic`.

Modding implications:

- Use `home_colony`/`background_colony` thinking for any colony-on-carrier logic in 4.4.5+.
- Plan a 4.5 port for pop/faction/ethic mods.

## S005/S006 — 4.0 Phoenix structural break

Observed facts:

- Pops grouped by species, strata, and ethic.
- Pop groups produce Workforce assigned to jobs.
- Pop groups can supply Workforce to multiple jobs.
- Species traits that created resource output now generate bonus workforce in relevant jobs.
- Pop growth simultaneous across species on a planet.
- Trade routes removed; Trade is now a normal resource/logistics system.
- Planet economy reworked around jobs/districts/buildings/district specializations.

Modding implications:

- Do not port 3.x pop/job/trade/planet-economy mods by descriptor bump.
- Use vanilla 4.x files as schema references.

## S007 — Modding tutorial

Observed facts:

- Every manual mod needs two descriptors.
- First descriptor is in `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\` and contains metadata + path.
- Second descriptor is named `descriptor.mod` in the root mod folder and contains metadata without path.
- `supported_version` supports wildcards and is only a visual launcher indicator; it has no effect on loading/code.
- Do not edit game install folder; mod folder mirrors game folder structure.
- Common content folders: `common`, `events`, `localisation`, `localisation_synced`, `gfx`, `interface`.
- Recommended tools include VS Code, CWTools, syntax highlighting, WinMerge, 7-Zip, GIMP/Paint.net, GitHub, Discord, Irony.
- CWTools helps with error highlighting, autocomplete, missing localisation lists, commenting, formatting.
- Logs and launch parameters are documented; `log` effect can write custom lines; `script_profiler` is referenced.
- The tutorial recommends Git and warns against local + Workshop duplicate loading.

Modding implications:

- This is the canonical mod-structure source for this bundle.

## S008 — Localisation

Observed facts:

- `localisation` folder uses British spelling.
- `.yml` files must be UTF-8 with BOM.
- File names must end `_l_<language>.yml`.
- First line must be `l_<language>:`.
- No mod-friendly fallback language; missing keys display raw keys.
- `localisation/replace` loads after all other localisation and can override duplicate keys via LIOS.

Modding implications:

- Codex must create localisation files with BOM.
- Text overrides should be deliberate and isolated.

## S009 — Scopes

Observed facts:

- Objects provide scopes such as planet/pop/country.
- Special scopes: THIS, PREV, FROM, ROOT.
- `exists` checks are recommended when a scope might not exist.
- Wrong-scope triggers produce errors and can fail code; nonexistent-scope effects can silently do nothing.
- `any_`, `every_`, and `random_` constructs switch scope.
- Current docs can be generated with `trigger_docs` and logs/script documentation.

Modding implications:

- Wrong scope is a primary failure mode for generated code.
- Codex should add `exists` guards around optional relationships, especially in Nomad/Arkship code.

## S010 — Console commands

Observed facts:

- Page verified for PC 4.2, so confirm on current version.
- Console is for non-Ironman games; commands disable achievements.
- `help` lists commands; `help <command>` gives command details.
- `debugtooltip` reveals generated species/leader/empire/ship/pop IDs.

Modding implications:

- Use `help` in 4.4.x to verify commands.
- Do not promise achievement-safe debugging with console commands.

## S011/S012 — Irony and FIOS/LIOS

Observed facts:

- Irony supports Stellaris and understands game structures, FIOS/LIOS, and deterministic load-order management.
- Filename-only conflict checks can be misleading.
- Irony conflict solver detects loaded game elements and explains whether a definition is used because of load order or FIOS/LIOS.
- Not every conflict requires patching.

Modding implications:

- For serious playsets, use Irony rather than manual load-order folklore.

## S013/S014 — CWTools and CI

Observed facts:

- CWTools is a VS Code extension for Paradox script files.
- Docs recommend Git and frequent commits.
- It scans mod/vanilla folders and reports syntax errors.
- cwtools-action runs automated validation with rules and vanilla cache; full cache improves validation around load order and file overrides.

Modding implications:

- Codex-generated code should be followed by CWTools validation.

## S015/S016/S017/S018 — LLM and AI-adjacent sources

Observed facts:

- Galactic Conclave: external diplomacy app, save parser, LLM provider, command-file `run` bridge, Ironman injection disabled.
- Stellaris Overmind: player advisor and AI-mode macro strategy; native Stellaris AI still executes micro decisions.
- Stellaris LLM Companion: save analyzer, strategic advisor, MCP relay to Claude/Codex.
- Beachboys Fair AI 2: claims ChatGPT-assisted AI overhaul; comments allege nonworking/invalid generated content.

Modding implications:

- Public runtime LLM work is external-tool based.
- AI assistance must be schema/log validated.
