# Stellar AI Director Hostile Fauna Clearance Inventory

Date: 2026-07-09

Task card: T18 - Hostile fauna clearance inventory

## Scope

This pass inventories the `hostile_space_fauna_clearance_route` before any
increase to clearance aggression. It does not change generated gameplay files.

## Evidence Surfaces

- JDataMunch `stellar_ai_director_object_atlas_20260706`, filtered with
  `route_ids contains hostile_space_fauna_clearance_route`.
- Current vanilla Stellaris 4.4.5 source files under
  `C:\Steam\steamapps\common\Stellaris`.
- Scoped `rg` fallback for selected `.txt` PDXScript files after JCodeMunch
  rejected those files as unsupported source extensions.

The route is broad: 455 rows / 449 distinct objects across 19 object types.
The largest groups are events (205), scripted triggers (50), scripted effects
(40), ship sizes (38), technologies (31), deposits (20), and AI budgets (13).

That shape means this route is not a clean target list for early military
clearance. It includes cheap blockers, reward hooks, special projects,
leviathan event chains, advanced crystal/ESC/Gigas support objects, and unsafe
guardian-class ship sizes.

## Cheap Or Plausible Targets

These are plausible inputs for a future narrowly gated reserve policy:

- `space_amoeba`: max hitpoints 300, fleet slot size 1.
- `ancient_mining_drone`: max hitpoints 200, fleet slot size 1.
- Small crystal entities: `@corvette_hp = 300`, fleet slot size 1.
- Medium crystal entities: `@destroyer_hp = 650`, fleet slot size 2.
- Large crystal entities: `@cruiser_hp = 1400`, fleet slot size 4.

These are blockers an expanding AI might reasonably clear once alloy, naval
capacity, and war safety gates are healthy.

## Medium Caution Targets

These are not first-push targets, but may be safe later:

- `space_amoeba_mother`: max hitpoints 2000, fleet slot size 4.
- `space_amoeba_centenarian`: max hitpoints 2000, fleet slot size 4.
- Reanimated ordinary amoeba variants, when they appear as reward assets rather
  than hostile map blockers.

These should require a stronger reserve and should not be used to justify
blanket aggression against all route members.

## Unsafe Targets

These must be excluded from generic early clearance pressure:

- `crystal_station_large`: max hitpoints 40000.
- `leviathan_01_scavenger_bot`: max hitpoints 100000.
- `leviathan_01_elder_tiyanki`: max hitpoints 125000, fleet slot size 32.
- `leviathan_01_voidspawn`: max hitpoints 100000.
- Reanimated leviathan and dragon entries, including 100000-150000 hitpoint
  reward ships.

The route also touches leviathan event rewards such as tiered material/research
rewards, artifact rewards, relic hooks, special projects, standard unity
rewards, and `tech_leviathan_techgenesis`. Those are valuable, but they are not
evidence that early fleets should chase every hostile-fauna route object.

## Decision

Do not add a generated reserve or aggression change in T18.

For T19, the safe recommendation is:

- only consider a narrow reserve-pressure policy for ordinary fauna/mining
  drone/crystal ship blockers;
- require healthy economy and fleet reserve gates;
- explicitly exclude crystal stations, Distant Stars guardians, reanimated
  leviathans, and broad leviathan event-chain objects;
- document runtime proof separately if this becomes part of the live observer
  target.

## Validation

- JDataMunch atlas index integrity: `ok`.
- Atlas route aggregate: 455 rows / 449 distinct objects.
- Source inspection used scoped current vanilla files only.
- JCodeMunch fallback note: selected Stellaris `.txt` PDXScript files were
  attempted through `index_folder`, but the tool returned unsupported extension
  warnings for the exact files, so scoped `rg` was used for line-level source
  evidence.

## Remaining Runtime Proof

This is a static inventory. It does not prove in-game clearance behavior,
fleet targeting, or reward timing. Runtime claims remain deferred until the
packet reaches the approved observer-test phase.
