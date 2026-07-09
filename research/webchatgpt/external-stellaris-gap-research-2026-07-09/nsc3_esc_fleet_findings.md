# NSC3 + ESC NEXT + Spacefleet Tactica Fleet Findings

## Direct answer

NSC3, ESC NEXT, and Spacefleet Tactica should be treated as three different layers:

1. **NSC3** changes ship classes, fleet scale, command limits, capacity, and ship-role surface [S025][S026].
2. **ESC NEXT** adds an advanced component progression layer and requires a new game rather than conversion from old ESC 3.0 saves [S028].
3. **Spacefleet Tactica** is the ship-behavior/combat-computer behavior layer that NSC3 recommends after removing its own Advanced Ship Behaviors due ongoing bugs [S027].

The first hard compatibility rule is to configure ESC NEXT reactors when NSC3 is active. The maintained 4.4 collection says ESC reactors are significantly weaker than NSC3 reactors and must be adjusted when NSC3 + ESC NEXT are used together [S029].

## Interaction map

| Layer | What it owns | What can break | Source |
|---|---|---|---|
| NSC3 | New ship classes, sections, fleet/naval scale, command limits | Missing classes, broken shipsets, outdated saves, designer invalidity | [S025][S026] |
| ESC NEXT | Advanced components, weapons, reactors, component progression | Research clutter, weak reactors, missing components, old-save incompatibility | [S028][S029] |
| ESC overwrite add-ons | Component progression, global designs, special weapon type display/behavior | AI global design overwrite conflicts, turret/entity issues, components out of intended sequence | [S028][S029] |
| SFT | Combat behavior/computers/ship behavior | Empty behavior slots, no valid computer choice, bad pursuit/kiting behavior | [S027][S030][S032] |
| UIOD | Larger ship designer and UI room for new classes/sections | Cannot see/save sections or starbase modules correctly | [S047] |

## Recommended fleet-design logic

### Strategic roles

- **Screens/pickets:** protect high-value hulls; soak fire; run PD/flak when missiles/strike craft matter.
- **Torpedo/frigate wings:** high-health single-target threats such as Cetana-style targets, leviathans, large stations, or Gigas capital objects [S021].
- **Missile/carrier kiting:** strong against shield-heavy or low-PD threats; community anti-crisis discussions recommend missile/strike craft approaches for Unbidden-style enemies [S020].
- **Artillery capitals:** long-range alpha and repeatable scaling; pair with artillery/carrier computers where SFT/NSC/ESC compatibility proves valid.
- **Dreadnought/titan/flagship/NSC capitals:** fleet anchors, aura platforms, and high-end damage sinks.
- **Celestial ships:** not normal fleets; use Gigas route logic for attack moons, planetcraft, and systemcraft [S009][S012].

### Component priorities

1. **Reactors/power:** NSC reactor path should dominate if ESC reactor branch is weaker in the stack [S029].
2. **Sensors/combat computers/behaviors:** design is invalid if no behavior/computer is selectable [S030].
3. **Weapons:** choose by crisis or opponent defenses, not a universal “best” weapon [S019][S020][S021].
4. **Defenses:** refit against known threat. Shields/armor/hull ratio should be counter-specific; older Katzen advice prefers armor over shields when fighting Katzen directly [S008].
5. **Auras/support:** capital hulls should carry aura/support roles when the component graph allows it.

## Compatibility and load-order mistakes

### Mistake 1: leaving ESC reactors cluttering NSC reactor progression

**Symptom:** repeated research offers for lower-powered ESC reactors, invalid power budgets, or AI designs using weaker reactors.
**Fix:** follow collection guidance: adjust ESC NEXT settings before the first month passes [S029].

### Mistake 2: no SFT/behavior layer after NSC3 removed ASB

**Symptom:** ships close incorrectly, fail to pursue, or lack valid behavior/computer choices.
**Fix:** include SFT or a vetted behavior layer; validate ship designs after all techs [S027][S030][S032].

### Mistake 3: stale AI/NSC patches

**Symptom:** AI or player cannot build new ship classes, tech progression stays vanilla, shipyards fail, or global designs reference missing sections.
**Evidence:** Starnet for NSC3 explicitly says it is for 3.12 [S036], and comments document tech/buildability problems in old AI/NSC/ESC patch contexts [S037].
**Fix:** do not use stale 3.12 patches in 4.4.x; build a current local compatibility patch only after source inspection.

### Mistake 4: UI designer too small or overwritten

**Symptom:** ship designer/section UI cannot show new NSC slots/classes, or starbase UI slots vanish.
**Fix:** UIOD plus relevant compatibility patches; UIOD explicitly expands the ship designer for new sections/classes [S047].

## AI ship-design implications

Do not generate AI global designs until the active component/section/computer graph is validated. Required checks:

1. Every ship size has valid sections.
2. Every section has valid slots.
3. Every slot has at least one valid component after tech unlocks.
4. Every design has enough reactor power.
5. Every combat computer/behavior slot has a valid choice.
6. Global AI designs do not reference stale ESC/NSC components.
7. Crisis-specific retrofit branches exist.

## Test pass to run later

- New disposable game, all relevant mods active.
- Before month one: configure ESC NEXT reactors.
- `research_all_technologies` or staged tech unlocks.
- Open ship designer for corvette/frigate/destroyer/cruiser/battleship/titan/juggernaut plus NSC hulls.
- Save at least one design per class.
- Validate auto-design and AI global designs.
- Inspect error.log for missing section/component/computer keys.
