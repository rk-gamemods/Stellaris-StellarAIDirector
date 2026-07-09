# Modding Tools And Free Online Resources

## Direct answer

The best free current workflow is: Paradox Wiki for concept/folder surfaces, current vanilla and mod source for exact syntax, CWTools for static PDXScript validation, Irony Mod Manager for load order/conflicts, OldEnt generated lists for trigger/effect/modifier discovery, Steam/GitHub changelogs for mod-specific current claims, and save/log tools for runtime evidence.

## Reliability matrix

| Resource | Best use | Reliability for exact syntax | Staleness risk | Source |
|---|---|---:|---:|---|
| Paradox Wiki Modding Tutorial | Folder structure, general mod creation, common folders | medium-high | medium | [S065] |
| Paradox Wiki Localisation | Localisation spelling, BOM, language files | high | low-medium | [S066] |
| Paradox Wiki Event Modding | Event types/scopes/concepts | medium-high | medium | [S067] |
| Paradox Wiki Console Commands | Public command list and access method | medium-high | medium | [S060] |
| Current vanilla files | Exact triggers/effects/object syntax | highest | low if target install is current | local required |
| Current Workshop/source files | Exact modded IDs and parent AI support | highest | low if source is current | local required / [S003] |
| CWTools | Parser/schema/static diagnostics | high | low if config current | [S069][S070][S071][S072][S073] |
| Irony Mod Manager | Load order, dependency, element-level conflicts, patch mods | high | low-medium | [S074][S075][S076] |
| OldEnt generated lists | Trigger/effect/modifier discovery and version diffs | medium-high | version-specific | [S077] |
| Steam Workshop pages/changelogs | Maintainer claims, current version signals, load order | high for page claims | medium | mod sources |
| Reddit/Steam discussions | Player strategy and bug symptoms | medium-low | high | community sources |
| Pdx-Unlimiter | Save management/editor workflows | medium | medium | [S078] |
| Save-game editing wiki | Save-format cautions and backup rule | medium-high | medium | [S079] |
| Stellaris Dashboard | Save/statistics visualization example | medium | medium | [S080] |

## CWTools workflow

CWTools is a library for parsing, editing, and validating Paradox script files [S070]. The VS Code extension supports Paradox script and Stellaris, and its usage flow is to open the mod folder, select the vanilla folder, and wait for diagnostics [S071]. The Stellaris config repository provides `.cwt` config files that are used automatically for stable/latest or can be manually copied into `.cwtools` [S072]. Recent changelog entries mention Stellaris script-value parameter support, modifier fixes, and scope/completion improvements [S073].

Recommended use:

1. Open the generated mod folder directly.
2. Select current vanilla Stellaris folder.
3. Add active parent mod folders as multi-root workspace if supported.
4. Fix unknown triggers/effects/modifiers, wrong scopes, bad localization references, and missing sprites before runtime tests.
5. Do not treat CWTools pass as proof of AI behavior.

## Irony workflow

Irony is the conflict/load-order tool because its docs say it understands game structures, FIOS/LIOS rules, and deterministic load order [S074]. The author utility discussion explains that Irony loads game elements rather than only comparing filenames and can tell whether a definition wins through load order or FIOS/LIOS [S076].

Recommended use:

1. Import/construct the active collection.
2. Do not trust generic “last mod wins.”
3. Run conflict scans for exact surfaces: ship sizes, components, sections, starbase levels, UI files, topbar resources, common resources, AI budgets, economic plans, megastructures, technologies, and global ship designs.
4. Patch only conflicts that affect the intended stack.
5. Export conflict reports and patch provenance.

## Public schemas and exact syntax

- Use CWTools Stellaris config for schema hints [S072].
- Use current vanilla and current parent mod source for exact syntax.
- Use OldEnt for discovery and version diffs, not as final proof when a 4.4.5 local file is available [S077].
- Use generated docs from the current install if available.

## Public mod source examples

- Gigas GitHub live branch for exact Gigas source lookup when the Workshop folder is not mounted [S003].
- NSC3 GitHub releases for change history and release-note provenance [S026].
- Workshop pages/changelogs for current user-facing instructions and load order [S025][S029][S041][S047][S048][S049][S051][S054][S057].

## Tooling decisions for this project

- Exact script syntax: vanilla/source + CWTools.
- Exact load order/conflicts: Irony.
- Exact modded IDs: active Workshop source + debugtooltip/help.
- Runtime behavior: error.log/game.log + disposable test save + observer metrics.
- Player strategy: use Reddit/Steam discussions as advice, not schema.
