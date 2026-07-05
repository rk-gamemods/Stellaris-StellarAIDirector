# Preferred Stellaris Collection Research

Date checked: 2026-07-04

Target profile:

- Prefer Gigastructural Engineering, NSC3, Extra Ship Components NEXT or similar ship/component expansions, UI Overhaul Dynamic dependencies, smarter AI, performance optimization, and stronger station/planetary defense options.
- Exclude Real Space by default.
- Exclude Star Wars themed mods and shipsets by default.
- Steam Workshop is preferred.

## Best Starting Point

### 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity

Steam URL: `https://steamcommunity.com/sharedfiles/filedetails/?id=2473560875`

Steam ID: `2473560875`

Collection state observed:

- 116 child items from Steam collection API.
- Workshop page says updated July 2, 2026, with revision `07/02/2026`.
- Page explicitly says to use its discussion-tab load-order instructions and Irony Mod Manager text list.
- Page says NSC3 is optional, but if using NSC3 plus ESC NEXT, ESC NEXT settings must be adjusted because ESC reactors are significantly lower powered than NSC3 reactors.
- Page describes Gigastructural Engineering as adding 45 megastructures, 4 optional crises, origins, unique systems, and AI use of megastructures.

Observed target-match items in the collection:

| Desired area | Included item |
| --- | --- |
| Gigas | `Gigastructural Engineering & More (4.4)` |
| NSC | `NSC3` |
| Components | `Extra Ship Components NEXT` |
| ESC add-ons | `ESC NEXT: Overwrites: Component Progression`, `ESC NEXT: Overwrites: Global Ship Designs`, `ESC NEXT: Overwrites: Special Weapon Types Patch` |
| UI | `UI Overhaul Dynamic`, `UI Overhaul Dynamic - Tiny Outliner`, `UI Overhaul Dynamic - Tiny Options`, `UI Overhaul Dynamic - Extended Topbar for DLCs` |
| UI patches | `UI Overhaul Dynamic + Gigastructural Engineering`, `UI Overhaul Dynamic + Planetary Diversity`, `UI Overhaul Dynamic + Improved Leaders View` |
| AI | `Stellar AI`, `Smarter Hyper Relays: Improved AI (shrimpAI)` |
| Stations | `Starbase Extended 3.0` |
| Planet/content | `Planetary Diversity`, `Guilli's Planet Modifiers and Features`, PD submods |

Observed conflicts with user preferences:

- Includes several Star Wars shipsets and NSC3 shipset patches. These should be excluded.
- Very large collection. Do not subscribe all unless deliberately testing the maintainer's exact playset.
- Contains many portrait, shipset, visual, and optional flavor mods that are not required for the preferred core.

Recommendation:

Use this as the main discovery and load-order source, not as a one-click install. Start from its core NSC/Gigas/ESC/UI/AI/station choices, then strip Star Wars, Real Space, extra shipsets, portraits, and low-value visual extras.

## Strong Supporting Collections

### NSC Highly Recommended Companion Mods

Steam URL: `https://steamcommunity.com/workshop/filedetails/?id=3753239451`

Steam ID: `3753239451`

Observed children from Steam collection API:

- `NSC3`
- `Extra Ship Components NEXT`
- `Spacefleet Tactica`
- `NSC3 Shipsets - Fran's work for you`
- `NSC3 Module: Extra Shipsets`
- `NSC3 Mass Effect Shipsets`

Recommendation:

Use this as the authoritative NSC-side companion list. It is much smaller than the 116-item collection and directly confirms NSC3 plus ESC NEXT as the preferred ship/component pairing. The shipset add-ons are optional. `Spacefleet Tactica` deserves follow-up because NSC3's page recommends it as the replacement for removed NSC Advanced Ship Behaviors.

### UI Overhaul Dynamic - Compatibility Patches

Steam URL: `https://steamcommunity.com/workshop/filedetails/?id=1680652232`

Steam ID: `1680652232`

Collection state observed:

- 16 child items from Steam collection API.
- Page includes `UI Overhaul Dynamic + Gigastructural Engineering` for 4.4.
- Page includes `UI Overhaul Dynamic + Planetary Diversity` for 4.4.
- Page includes several older or warning-marked patches. Use exact needed patches only.

Recommendation:

Use as the UI patch menu. For the preferred profile, the likely required patch is `UI Overhaul Dynamic + Gigastructural Engineering`; `UI Overhaul Dynamic + Planetary Diversity` is likely useful if Planetary Diversity stays in the list.

### UI Overhaul Dynamic - Submods

Steam URL: `https://steamcommunity.com/workshop/filedetails/?id=2094085974`

Steam ID: `2094085974`

Observed:

- 24 child items from Steam collection API.
- Prior packet found it current around the 4.4 window.

Recommendation:

Use selectively. Good candidates are Tiny Outliner, Tiny Options, Extended Topbar for DLCs, and maybe Planet View Performance Mode if the user wants less visual clutter. Avoid overlapping outliner/speed dial choices.

### Gigastructural Engineering - Compatibility Patches

Steam URL: `https://steamcommunity.com/workshop/filedetails/?id=2678436516`

Steam ID: `2678436516`

Observed:

- 13 child items from Steam collection API.
- Page says it is a collection of patches for compatibility between Gigastructural Engineering and other mods.
- Includes `Gigastructural Engineering & More (4.4)` and `UI Overhaul Dynamic`.
- Also includes stale or unwanted Real Space/System Scale related material. Do not blindly subscribe all.

Recommendation:

Use as a patch-discovery menu for Gigas, not an install set.

## Alternative Broad Collections

### Current

Steam URL: `https://steamcommunity.com/sharedfiles/filedetails/?id=3611360080`

Steam ID: `3611360080`

Observed:

- 27 child items.
- Includes `Gigastructural Engineering & More (4.4)`, `NSC3`, `Extra Ship Components NEXT`, ESC overwrite add-ons, `AI Game Performance Optimisation 4.4`, `UI Overhaul Dynamic`, and `UI Overhaul Dynamic + Gigastructural Engineering`.
- Also includes multiple Star Wars shipsets and a Halo total-conversion/mod set component, which conflict with the user's default preferences.
- Low collection adoption signal observed: 1 favorite.

Recommendation:

Potentially useful as a compact source list, but weaker than the 116-item NSC/PD collection because it is less documented and includes unwanted theme mods.

### Perfect Stellaris 4.0.21

Steam URL: `https://steamcommunity.com/sharedfiles/filedetails/?id=2089433274`

Observed:

- Updated 2026-05-30 by Steam API.
- Search snippets show Gigas and Starbase Extended.
- Includes Real Space, which conflicts with the user's preference.

Recommendation:

Do not use as a starting point.

## Defensive Mods To Investigate

These are not all collection anchors, but they match the user's strong-station or planetary-weapon preference.

| Mod | Steam URL | Observed status | Initial take |
| --- | --- | --- | --- |
| `Starbase Extended 3.0` | included in collection `2473560875` as item `3250900527` | Updated 2026-06-29 by Steam API | Most promising station candidate because it already appears in the best broad collection. Needs compatibility check with NSC3/Gigas/UIOD. |
| `Starbase Expansion` | `https://steamcommunity.com/sharedfiles/filedetails/?id=3707774430` | Updated 2026-06-30 by Steam API; page says working with 4.4.* | Balanced station expansion; requires UIOD-style starbase UI order. Potentially a cleaner alternative to Starbase Extended. |
| `Slightly Larger Starbases [4.4]` | `https://steamcommunity.com/sharedfiles/filedetails/?id=3168007310` | Updated 2026-06-15; page says 4.4 | Interesting but comments mention Gigas compatibility concerns, so lower priority for this profile. |
| `Expanded Starbases` | `https://steamcommunity.com/sharedfiles/filedetails/?id=1359700418` | Updated 2026-06-30 by Steam API | Avoid for NSC3 profile: page says it is not compatible with NSC or other mods that modify the starbase ship size file. |
| `Eternal Vigilance Redux` | `https://steamcommunity.com/sharedfiles/filedetails/?id=3692979098` | Updated 2026-06-15; says 4.2 to 4.4+ | Good lightweight defense candidate; restores automated defense-platform building and has AI spending controls. |
| `Armored Starbases` | `https://steamcommunity.com/sharedfiles/filedetails/?id=3748725141` | Posted 2026-06-20; page says 4.3.7 to 4.4 | Promising low-overwrite candidate: doubles armor for starbases/platforms/ion cannons and says it edits no vanilla files. |
| `At War: Planetary Cannons` | `https://steamcommunity.com/sharedfiles/filedetails/?id=1609801017` | Old original page; points to takeover ID `2506911097` | Conceptually exact match for planetary weapons, but not current-safe without finding a maintained 4.4 fork. |

## Preliminary Build Strategy

Use these collection sources as menus:

1. Base UI/dependency set:
   - UI Overhaul Dynamic
   - UI Overhaul Dynamic - Tiny Outliner
   - UI Overhaul Dynamic + Gigastructural Engineering
   - UI Overhaul Dynamic + Planetary Diversity if PD is included

2. Core ambitious content:
   - Gigastructural Engineering & More (4.4)
   - NSC3
   - Extra Ship Components NEXT
   - ESC NEXT overwrite add-ons only after confirming current ESC/NSC notes

3. AI/performance:
   - Stellar AI for smarter AI, or AI Game Performance Optimisation 4.4 for performance and behavior throttles.
   - Test combining them only after checking overlap and load order; prefer one first.

4. Defenses:
   - First test `Starbase Extended 3.0` because it appears in the best collection.
   - If compatibility is rough, try `Starbase Expansion` or `Armored Starbases` as lighter alternatives.
   - Treat `At War: Planetary Cannons` as a watchlist item until a 4.4-maintained page is verified.

5. Exclusions:
   - Remove Real Space.
   - Remove Star Wars shipsets and Star Wars themed mods.
   - Remove total conversions and unrelated shipsets unless deliberately testing them.

## Next Verification Tasks

- Use Steam pages and local downloaded descriptors to identify exact dependencies for NSC3, ESC NEXT, Gigas, UIOD patches, and station mods.
- Use Irony to compare conflicts between:
  - NSC3 + ESC NEXT
  - NSC3 + Gigas
  - NSC3/Gigas + Starbase Extended 3.0
  - UIOD + UIOD Gigas patch + UIOD PD patch
  - Stellar AI + Gigas/NSC3
  - AI Game Performance Optimisation + Gigas/NSC3
- Search specifically for a current 4.4 planetary-cannon or planetary-defense fork.
