# Trait Option Mod Update - 2026-07-05

Target game install: `Pegasus v4.4.4 (5505)` with launcher compatibility
version `4.4`.

## Installed Mods Reviewed

| Workshop ID | Installed name | Installed supported version | Decision |
| --- | --- | ---: | --- |
| `686912554` | `Immortal Leaders Trait` | `3.0.2` | Replaced locally. The source file uses outdated 3.0-era syntax and includes an invalid `Using is_ai = no` line. |
| `3400802410` | `Immortal Leaders` | `v4.0.13` | Used as the safer syntax reference for the local immortal-trait replacement. |
| `2433663177` | `More Trait Points` | `3.14.*` | Replaced locally. The Workshop page is removed/incompatible and the local file overwrites stale pre-4.4 species archetypes. |
| `3007809395` | `Militus' Extra Trait Points` | `3.8.4` | Replaced locally. The local file overwrites stale pre-4.4 species archetypes. |
| `2980333846` | `3 Civic Points + More Trait Points/Picks` | `3.8.2` | Replaced locally. The local file overwrites stale pre-4.4 species archetypes. |

## Local Replacements

| Local mod | Replaces | Notes |
| --- | --- | --- |
| `mods/RKImmortalLeadersTrait` | `Immortal Leaders Trait` | Keeps the old `trait_Immortality` key for custom-empire compatibility and uses 4.4-supported `immortal_leaders = yes`. |
| `mods/RKMoreTraitPoints` | `More Trait Points` | Preserves the old 3/7 biological, 2/7 machine, 0/4 robot values on top of the current 4.4 vanilla archetype file. |
| `mods/RKMilitusExtraTraitPicks` | `Militus' Extra Trait Points` | Preserves the old 2/15 biological, 1/13 machine, 0/11 robot values on top of the current 4.4 vanilla archetype file. |
| `mods/RKThreeCivicMoreTraitPointsPicks` | `3 Civic Points + More Trait Points/Picks` | Preserves the old 3 civic, 3/7 biological, 2/6 machine, 0/5 robot values on top of the current 4.4 vanilla archetype file. |

The three trait-point/pick local mods all overwrite
`common/species_archetypes/00_species_archetypes.txt`. Enable only one of them
at a time. The old Workshop versions should be disabled when using these local
copies.

Launcher descriptor files were installed under:

- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\rk_immortal_leaders_trait.mod`
- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\rk_more_trait_points.mod`
- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\rk_militus_extra_trait_picks.mod`
- `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\rk_three_civic_more_trait_points_picks.mod`
