# Stellar AI Director 4.4.5 Compatibility Triage

Date: 2026-07-08

Current target: Stellaris PC 4.4.5 "Pegasus" stable/current local install.

## Version Evidence

- Local runtime log: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\game.log` reports `Game Version: Pegasus v4.4.5` for the latest load attempt.
- Official Steam news reports that the Stellaris 4.4.5 "Pegasus" update is ready for Steam, GOG, and MS Store.
- Launcher descriptors should continue to use `supported_version="v4.4.*"` for 4.4-line mods; this is launcher metadata, not script-load proof.

## 4.4.5 Patch Surfaces To Treat As Risky

- Resource Abundance slider changes alter the strategic economy baseline for new games.
- Waystation Voidlure and Arkship Voidlure modules expand Nomads/Waystation surfaces.
- Fleet automation and construction automation gained per-action/default controls.
- Operational Reserves changed for Nomadic empires, including capacity scaling and critical-stage penalties.
- Species rights are recalculated when loading a save, so species-rights or living-standard assumptions need exact 4.4.5 proof before changes.

## Latest Load-Freeze Log Neighborhood

No Stellaris launch or observer run was performed for this note. This is a static/log triage of the latest user-reported freeze at 100 percent loading.

Counts from the latest `error.log`:

| pattern | count |
| --- | ---: |
| `zzzz_staid` | 4403 |
| `Unexpected token` | 325 |
| `Failed to deferred read key reference` | 4830 |
| `uses_ship_category` | 1547 |
| `has_job` | 443 |
| `major_orbital` | 66 |
| `minor_orbital` | 34 |
| `frameworld_planetary_outpost` | 142 |
| `starbase_modules` | 62 |

Director-owned issues already patched after this log:

- Removed generated copied zone overrides from `common/zones` and made regeneration delete the stale generated zones file.
- Removed unsupported `empire_size` targets from generated economic-plan subplans.
- Merged duplicate top-level `potential` blocks in copied starbase-module overrides before replacing `ai_weight`.

Remaining likely active-stack 4.4.5 risks if loading still freezes:

- Gigastructural Engineering references `major_orbital`, `major_orbital_knights`, and `minor_orbital` through `common/scripted_triggers/giga_mega_categories.txt` and alternate mega-build effects.
- Gigas frameworld paths reference `frameworld_planetary_outpost`, missing frameworld defensive station ship sizes, and missing `giga_frameworld_origin.1002`.
- ESC/ship-size trigger surfaces repeatedly fail deferred key reads for missing or changed ship sizes.
- `uses_ship_category` is being evaluated in a `ship_growth_stage` scope where the log says it is invalid.
- Portrait asset selectors emit invalid `has_job` use.
- Gigas GUI and asset files emit parser/entity warnings that may be independent of Director.

## Working Position

The project baseline is now 4.4.5. Do not continue to treat 4.4.5 as beta in current docs, prompts, or generated notes. Keep old 4.4.4 observer runs, audits, and raw research as historical evidence only; revalidate any 4.4.4-derived implementation assumption against current local vanilla files, active-stack inventories, generated audits, and current logs before changing generated behavior.
