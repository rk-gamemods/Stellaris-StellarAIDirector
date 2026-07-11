# Science-Ship Route Retry / MIA Loop: Evidence and Fix Boundary

Date: 2026-07-11

Target: Stellaris Pegasus 4.4.4 (checksum 5505), Stellar AI Director

Branch inspected: `codex/science-route-and-research-reassignment` at `8826d53e`

Runtime launch performed: no

## Decision

The reported loop is real, repeatable in the newest save sequence, and is not
fixed by preventing AI science ships from fitting cloaking components.

Pegasus 4.4.4 does not expose a native AI data surface for destination-specific
route failure memory. The exposed native auto-explore controls are three scalar
scores. They cannot remember that one fleet failed in one system, suppress only
that route, or re-enable it when access or detection materially changes.

The only source-backed route to destination-specific memory uses the
`on_crossing_border` and `on_fleet_went_mia` hooks plus a fleet event and a
namespaced flag. That would cross this repository's native-AI-only production
boundary, which explicitly prohibits events, on_actions, and scripted fleet
orders as AI competence substitutes. Therefore no production implementation was
made in this investigation.

## Save evidence

Source folder:

`C:\Users\Admin\Documents\Paradox Interactive\Stellaris\save games\unitedcevantiannation24_1055935931`

All five saves are Pegasus 4.4.4 saves. Country 0 owns science fleets `689`,
`804`, and `33555064`. Each retains `mia_type=mia_forced_to_decloak` across the
entire two-year sequence while its serialized `order_id` keeps increasing.
That is evidence of repeated reassignment/retry rather than one stale MIA
record.

| Save | Fleet 689 order | Fleet 804 order | Fleet 33555064 order |
|---|---:|---:|---:|
| `autosave_2237.01.01.sav` | 581 | 736 | 298 |
| `autosave_2237.07.01.sav` | 585 | 758 | 335 |
| `autosave_2238.01.01.sav` | 589 | 770 | 373 |
| `autosave_2238.07.01.sav` | 621 | 782 | 394 |
| `autosave_2239.01.01.sav` | 642 | 804 | 415 |

The serialized `mia_from` origin is system `123` (`Chi_Volantis`) for fleet
`689` in `2238.01.01` and fleet `804` in `2238.07.01`, matching the highlighted
Fallen Empire route in the screenshot. The affected fleets continue to carry
`is_cloaked=yes` state when forced to decloak.

Save hashes:

| Save | SHA-256 |
|---|---|
| `autosave_2237.01.01.sav` | `15C96EE19743F6632CA3655643B918BC384B3DFB4FE90A995D0FB63A4907C0E0` |
| `autosave_2237.07.01.sav` | `88D748945D1BA6B93ACA1FB46B5BF4B1C5571F9AADD42BF3417873C5270E6ED1` |
| `autosave_2238.01.01.sav` | `9AE845AB0D9F86C389080ACDA2495C918EB2A4422B557F0995785A260DB042E5` |
| `autosave_2238.07.01.sav` | `2D7C6FA3D5DC7E55FEFC1B9B02DAEF5B21DC1034BBD11A701D5F59220D7C5E26` |
| `autosave_2239.01.01.sav` | `53510194D3A43756C170BEC3A23EA715363D956E8A759215596C2C7D028DF430` |

## Current Director behavior relevant to the loop

`tools/stellar_ai_director_lib.py` currently generates two relevant changes:

1. `high_scale_ai_defines_text()` changes the native values to:
   - `AUTO_EXPLORE_ATTRACTION_SCORE = 1000` (vanilla: 200)
   - `AUTO_EXPLORE_COLLABORATION_PENALTY = 2000` (vanilla: 750)
   - `AUTO_EXPLORE_SYSTEM_OWNED = 100` (vanilla: 1000)
2. `science_cloaking_ai_safety_components_text()` copies all five vanilla
   science cloaking components and replaces their AI design weight with zero.

The first change makes foreign-owned systems ten times less costly to the
auto-explore scorer than vanilla. It can increase pressure toward the Fallen
Empire route. The second change is the rejected workaround: it weakens AI ship
capability and does not implement failure memory. The newest save also proves
that forced-decloak loops remain observable despite that generated override.

Restoring the vanilla foreign-system penalty and removing the cloak suppression
would be native-compliant cleanup, but neither is an evidence-backed complete
fix for retry memory. The former changes only a global score; it cannot blacklist
one failed route or distinguish open access from closed borders. It must not be
reported as solving the loop.

## Exact native 4.4.4 surface inventory

### Auto-explore controls

`C:\Steam\steamapps\common\Stellaris\common\defines\00_defines.txt` exposes
only these route-scoring values:

```text
AUTO_EXPLORE_ATTRACTION_SCORE = 200
AUTO_EXPLORE_COLLABORATION_PENALTY = 750
AUTO_EXPLORE_SYSTEM_OWNED = 1000
```

An exact search across current vanilla `common/` and `events/` found no other
PDXScript auto-explore selection, failure-memory, destination blacklist, or
retry-backoff object. Other occurrences are message types and Nomad ship UI.

### MIA hook

`C:\Steam\steamapps\common\Stellaris\common\on_actions\00_on_actions.txt`
defines:

```text
# This = fleet
on_fleet_went_mia = { ... }
```

It supplies only Fleet scope. It does not supply a failed destination, origin,
or MIA reason scope. Current CWTools trigger definitions expose `can_go_mia`,
but no trigger for `mia_forced_to_decloak` or another `mia_type` value. The
`mia_type` value is serialized in saves but is not a documented script trigger.

### Border-crossing hook

The same vanilla on-actions file defines:

```text
# Scope = Fleet
# From = Origin System
# FromFrom = Destination System
on_crossing_border = { ... }
```

Vanilla `events/nomads_arkship_events.txt` events `arkship.880`, `arkship.890`,
and `arkship.910` prove the following operations in exactly those scopes:

- `root.owner`
- `fromfrom.space_owner`
- `has_closed_borders = root.owner`
- `is_fallen_empire = yes`
- `is_cloaked = yes`
- comparison of `has_cloaking_detection` with
  `root.trigger:has_cloaking_strength`
- dynamic flags suffixed with an event target

CWTools also documents `clear_orders = yes` on Fleet scope and
`set_timed_fleet_flag`. These hooks and effects can implement route memory, but
they are event-driven control, not native AI weighting.

## Why a compliant native fix cannot meet the requested behavior

The required behavior needs all four capabilities below:

| Capability | Native auto-explore data | Script hook/event |
|---|---|---|
| Observe that an attempt went MIA | no | `on_fleet_went_mia` |
| Know the attempted destination | no | `on_crossing_border` (`FromFrom`) |
| Remember failure per fleet and destination | no | namespaced dynamic fleet flag |
| Cancel only a repeated failed order | no | Fleet-scope `clear_orders` |

No personality, economic plan, AI budget, component weight, or NAI define joins
these capabilities. A scalar foreign-system penalty can only reduce all foreign
travel. Disabling cloaking can only remove a capability. Neither learns from a
failed route.

## Narrow exception design (not implemented)

If the native-AI-only boundary is explicitly amended for this defect, the
narrowest design is event-driven and contains no scripted movement orders:

1. Register one hidden fleet event on `on_crossing_border` and one on
   `on_fleet_went_mia`.
2. For AI science fleets only, record a short-lived probe marker keyed to the
   exact `FromFrom` destination system when crossing a foreign border.
3. If that same fleet goes MIA while the probe is active, convert the probe into
   a persistent fleet/destination failure marker and clear the stale order.
4. On a later attempt to cross into that exact marked system, clear only that
   order while the material conditions are unchanged.
5. Remove/ignore the marker when one of these material changes is proven at the
   crossing hook:
   - system ownership changes;
   - borders/access become permissive;
   - hostile/war state changes appropriately;
   - the fleet's cloaking strength now exceeds destination detection.
6. Do not issue `move_to`, `set_fleet_order`, scripted survey, or any replacement
   destination. Native AI remains responsible for choosing another legal job.
7. Do not add recurring logging or a monthly galaxy-wide pulse. Both hooks are
   event-driven; any destination lookup must run only for an affected AI science
   fleet.

Even this design needs a focused runtime test. Static sources prove hook scopes,
flag syntax, and order cancellation; they cannot prove that the native planner
will choose a different target immediately after its stale order is cleared.

## Knowledge-base query result

The production knowledge base was healthy (`application_id=1397441074`,
`user_version=5`, primary target `4.4.4`). It correctly located and hash-attested
the two source files:

- `common/on_actions/00_on_actions.txt`, SHA-256
  `b629ef48cf822a5577611107a1bd4925dc73258aa6ee50ae8ad49c149488eeb2`
- `common/defines/00_defines.txt`, SHA-256
  `dfb4aa7c3fee50ef3dfe95b97c50ac2affbdd99135a065cd0cf06e5315fbf8fb`

However, exact version-scoped searches returned no results for:

- `on_fleet_went_mia`
- `AUTO_EXPLORE_SYSTEM_OWNED`
- `has_auto_move_target`
- `clear_orders`

A broad query for `forced decloak MIA science ship auto explore` returned the
generic `science` ship-size object and unrelated partial-token matches. It did
not rank the decisive on-action, define, trigger, effect, or vanilla Arkship
scope examples. The database was useful for source identity and provenance, but
not for answering the mechanic relationship.

Useful KB improvements for this question would be:

- index named on-action declarations with their documented scope chain;
- index NAI define keys and their comments as first-class symbols;
- ingest CWTools trigger/effect aliases with valid scope and parameter form;
- connect vanilla event occurrences to the hook that invokes them;
- rank exact multi-token mechanic chains above broad object-name token matches;
- support a query bundle such as `hook -> scopes -> available predicates/effects
  -> vanilla usages -> unresolved runtime boundary`;
- create an explicit gap when a save-serialized field such as `mia_type` has no
  documented script predicate, instead of silently returning unrelated matches.

## Validation boundary

- Save sequence and hashes: verified read-only.
- Vanilla 4.4.4 definitions and event examples: verified read-only.
- Director generator/test state: verified against the refreshed JCodeMunch index.
- Knowledge-base identity and query behavior: verified read-only; no KB write.
- Production mod: unchanged.
- Runtime behavior of the proposed exception: not tested and not claimed.
