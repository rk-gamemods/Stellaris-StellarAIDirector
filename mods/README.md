# Mods

Create one folder per Stellaris mod here.

Default to Stellaris PC 4.4.5 stable/current local install unless the mod README says otherwise. Use `supported_version="v4.4.*"` for stable 4.4 descriptors, including 4.4.5.

Each mod should include its own `README.md` with:

- mod purpose;
- target Stellaris version;
- required or assumed DLC;
- touched vanilla systems;
- mod prefix;
- object keys added or overridden;
- localisation keys added or overridden;
- compatibility notes;
- test checklist.

## Mod Folder Rules

- Use unique, prefixed filenames instead of vanilla-like names such as `00_civics.txt`.
- Add only folders the mod actually needs.
- Keep source project files here, not in the live Stellaris launcher mod directory.
- When preparing a playable local copy, use the descriptor pair described in `research/stellaris-modding-guide-2026-07-04.md`.
- Treat overwrites, copied vanilla files, UI files, and `replace_path` as high-risk until validated against current vanilla files and Irony conflict results.

The attached research bundle includes a starter skeleton at `research/stellaris-modding-research-bundle-2026-07-04/templates/stellaris_mod_skeleton/`.

## Local 4.4 Replacements

- `StellarAIDirector/` - AI budget/priority patch for the Irony playset.
- `RKImmortalLeadersTrait/` - local 4.4 replacement for the old Immortal Leaders Trait mod.
- `RKCheatTraits44/` - local 4.4 replacement for udk Cheat Traits; use this for effectively unlimited custom empire trait points/picks.
- `RKGodlyTraitsRedux44/` - local 4.4 compatibility copy of Godly Traits Redux 4.0 with powerful species and leader traits.
- `RKMoreTraitPoints/` - local 4.4 replacement for More Trait Points; do not stack with other species-archetype trait-point mods.
- `RKMilitusExtraTraitPicks/` - local 4.4 replacement for Militus' Extra Trait Points; do not stack with other species-archetype trait-point mods.
- `RKThreeCivicMoreTraitPointsPicks/` - local 4.4 replacement for 3 Civic Points + More Trait Points/Picks; do not stack with other species-archetype trait-point mods.
