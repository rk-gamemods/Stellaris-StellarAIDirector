# Godly Traits Redux 4.4 Local Update

Target game version: Stellaris PC 4.4.5 stable/current local install.

Source: local Steam Workshop mod `Godly Traits Redux 4.0`, ID `2945430513`, from `C:\Steam\steamapps\workshop\content\281990\2945430513`. The Workshop page is still branded for 4.0, is Steam-flagged incompatible, and has recent comments discussing current-version issues, so this repo keeps a local 4.4 compatibility copy instead of relying on the Workshop item.

Local mod: `mods/RKGodlyTraitsRedux44`, installed through launcher descriptor `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\rk_godly_traits_redux_44.mod`.

Preserved content:

- powerful species traits such as Godly Species, Demigods, Neffalim, Divine Ancestors, Deus Machina, Borg, Ancient, Everlasting, Hyper Fertile, Super Fertile, and Nano Assemblers;
- point traits granting `-4`, `-8`, `-16`, and `-32` trait-point costs;
- civics granting `+4`, `+8`, `+16`, and `+32` species trait picks across biological, lithoid, machine, and robot archetypes;
- leader traits and on_action events that assign godly/demigod leader traits from qualifying species traits.

Compatibility changes:

- removed stale `PLANTOID` archetype references because vanilla 4.4 species archetypes are `BIOLOGICAL`, `ROBOT`, `MACHINE`, `PRESAPIENT`, `LITHOID`, and `OTHER`;
- changed missing demigod leader icon references from `trait_demigod_race.dds` to the source mod's actual `trait_demigod.dds`;
- removed the obsolete `leader_class = general` event branch and undefined `leader_trait_general_godly` reference;
- fixed malformed `NOR` syntax in the ruler event;
- normalized an uppercase `FROM` scope to `from`;
- fixed duplicated `GTR_trait_nephalem` localization by restoring `GTR_trait_nephalem_desc`.

Load-order note: this was registered for Irony visibility only. No Irony collection or load order was changed. Slot it near the other trait/empire-creation mods when testing; do not move the rest of the list around for this.
