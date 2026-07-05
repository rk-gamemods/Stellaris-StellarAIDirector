# RK Cheat Traits 4.4

Local 4.4-compatible replacement for `udk Cheat Traits (Updated for 4.0)`.

The Workshop mod is still marked for `v4.0.*`. Its species-archetype overwrite
also references the old `pop_resources/regular_upkeep` inline script, which is
not present in the local 4.4.4 install. This local version uses the current
4.4 vanilla species-archetype file and changes only the trait-pick caps.

What this does:

- Sets biological, lithoid, machine, robot, and presapient trait pick caps to
  `99`.
- Adds `RK Cheat: 500 Trait Points`, a player-only species trait with cost
  `-500`.
- Adds `RK Cheat: Immortality`, a player-only species trait that sets
  `immortal_leaders = yes`.
- Prevents random/AI selection of the cheat traits.

Do not stack this with any other mod that overwrites
`common/species_archetypes/00_species_archetypes.txt`.
