# Stellaris Collection 2473560875 Instructions Deep Dive

Date checked: 2026-07-04  
Collection: [4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity](https://steamcommunity.com/sharedfiles/filedetails/?id=2473560875)  
Target assumed by collection author: latest Stellaris 4.4.x, with all DLC recommended  
Project target: Stellaris PC 4.4.4 stable unless explicitly changed

## Bottom Line

This collection is promising because it is current, maintained, documented, and intentionally modular. The author presents it as an "action packed" exploration-focused playset with major pillars such as NSC3, Gigastructural Engineering, Planetary Diversity, Guilli's Planet Modifiers, ESC NEXT, UI Overhaul Dynamic, event/archeology packs, starbase content, AI adjustments, and a large layer of optional visual variety.

The safest way to customize it is not to start by stripping all theme mods. The author explicitly treats shipsets, portraits, and similar visual additions as optional flavor that can usually be kept, removed, or ignored at player discretion. The risky decisions are the heavy scripted or gameplay systems: megastructures, ship-class overhauls, component expansions, event packs, archeology/rift packs, AI changes, performance-sensitive battle visuals, and anything with patches or startup configuration requirements.

## Source Of Truth Order For This Collection

Use the collection author's Steam discussions before changing the playset:

1. [4.4* Mod Load Order and Instructions](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/596274133248051325/)
2. [Irony Mod Manager Text List](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/4368003413703559586/)
3. [DLC: Do I Need Them All?](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/596285421871220191/)
4. [Game Details for this Collection](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/3825286048543186818/)
5. [Removing NSC3](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/3820788154612481641/)
6. [Configure ESC NEXT when using NSC3](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/4036976577926685988/)
7. [Ship Sets and Portrait Mods are Optional](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/3396302157195638920/)
8. [Checking Ship Sets for Compatibility](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/5545618081308567906/)
9. [Using the Fleet Formation Mods](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/4695657045623462347/)
10. [Gigastructural Engineering & More (4.4)](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/3372656531452244706/)
11. [Fixing problems with fresh reload of a Mod or Mods](https://steamcommunity.com/workshop/filedetails/discussion/2473560875/3371531264822661548/)

The collection page and discussions say the current load order is maintained in the discussion tab. The author avoids posting file downloads in comments because those links can become stale. The Irony thread is a clipboard-friendly helper, but the author says they do not personally use Irony and cannot provide Irony support.

## Collection Health Signals

As of 2026-07-04, the collection page showed:

- 116 items.
- 497 ratings.
- 27,406 unique visitors.
- 2,027 current favorites and 2,211 total favorites.
- Posted 2021-05-01 and updated 2026-07-02.
- Revision note dated 2026-07-02, including removal of Hypothetical Stars because it caused galaxy generation issues.

This matches the user's quality filter better than most low-signal Workshop collections: it has meaningful ratings, usage, active maintenance, explicit load order guidance, active troubleshooting guidance, and recent removals when a mod breaks the collection.

## Intended Use

The author intends this as a full playset for a richer exploration/action game, not a minimal vanilla-plus list. The design assumes:

- latest Stellaris 4.4.x;
- all DLC recommended, especially because several gameplay mods use DLC-dependent features;
- manual attention to load order;
- optional removal of undesired modules after understanding dependencies;
- UI Overhaul Dynamic and Universal Resource Patch as infrastructure pieces;
- Irony or another mod manager for practical playset maintenance, even though the author does not support Irony directly.

The collection is not intended to be a one-click black box. The repeated warnings to read discussion threads are real operating instructions.

## Low-Risk Or Mostly Visual Layer

The author explicitly marks custom shipsets and portrait mods as optional. This supports the user's preference: simple visual/theme items should not be treated as the same risk class as scripted gameplay systems.

Generally low-risk to keep, remove, or ignore:

- shipsets;
- portraits;
- flags and emblems;
- namelists;
- rooms, clothes, hair, and species presentation assets;
- camera or city graphics;
- simple UI graphics;
- fleet formation visuals when exactly one compatible formation mod is used.

Caveats:

- Some portrait mods include traits, civics, ships, or technology. Those are not purely visual and should be reviewed separately.
- Shipsets can break with current Stellaris graphical culture requirements even if the Steam page looks updated.
- NSC3 adds ship classes, so non-collection shipsets or unsupported shipset patches need compatibility checks.
- The author specifically warns against scale-changing fleet formation or ship-scale mods in this collection.

Recommended validation for custom shipsets:

1. Start with a small test game.
2. Use a Void Dwellers test empire to check habitats.
3. Preview ship models, but do not rely only on the empire designer.
4. Use `research_all_technologies`, let the game tick, and inspect the ship designer for corvettes, frigates, battlecruisers, carriers, dreadnoughts, flagships, explorers, stations, and habitats.

## High-Caution Gameplay And Scripted Layer

These are the parts to evaluate before keeping, removing, or extending the collection.

### Gigastructural Engineering

Gigas is optional, but it is a central pillar if retained. The collection page highlights many megastructures, optional crises, origins, unique systems, AI megastructure usage, and a custom UI for selecting which megastructures to use. If Gigas is kept with UI Overhaul Dynamic, the UIOD + Gigas patch is required.

Project posture: likely desired, but treat as a major gameplay pillar with performance and compatibility implications.

### NSC3

NSC3 is optional but deeply shapes ships, ship classes, components, and shipset compatibility. The author gives a separate removal thread. If NSC3 is removed, remove NSC3 and the listed NSC3 shipset patches too.

Project posture: likely desired because the user prioritizes ship and component expansion, but decide deliberately before adding more shipset or component mods.

### ESC NEXT

ESC NEXT is optional. When used with NSC3, the author says to disable ESC NEXT reactors through the ESC NEXT control panel before the first month advances, because ESC reactors can clutter research and ship design when NSC3 reactors are stronger.

Project posture: likely useful, but only if the startup configuration step is documented in the local playset notes.

### Planetary Diversity And Guilli's Planet Modifiers

Planetary Diversity and Guilli's Planet Modifiers are optional but major exploration/planetary variety pillars. They probably fit the user's preference for richer empire and planet options, but they are gameplay-affecting rather than harmless visuals. Keep their patches aligned with UIOD and any other parent dependencies.

Project posture: likely desired; verify patch coverage and load order in Irony.

### Starbase Extended

Starbase Extended is optional. It may fit the user's interest in stronger starbases and defenses, but it touches gameplay and should be evaluated with NSC3, ESC NEXT, Gigas, and AI behavior in mind.

Project posture: promising, but review for balance, AI use, and conflicts before treating it as baseline.

### Event, Archeology, Rift, And Crisis Content

The load order marks multiple event/story systems optional, including More Events Mod, Archaeology Story Pack, Forgotten Empires, Extra Events, AI-Player Exclusive Archaeology & Astral Rifts, Unique Systems Guaranteed, More Primitives, Planet Raider, and similar additions.

The collection page specifically calls out More Events Mod's Vazuran crisis timing and how to disable it in precursor options. Planet Raider adds a raid planet policy after invasion. Chris' Covert Operations adds covert operations and allows AI use based on its internal logic.

Project posture: review one by one. These are the easiest category to accidentally keep despite not wanting the content, and they can affect pacing, event load, crisis pressure, saves, and AI behavior.

### AI And Performance Systems

Stellar AI is optional and should be reviewed on its own page before being treated as safe. The user specifically cares whether AI can use advanced systems from major mods; this needs direct mod-page or in-game evidence, not assumption.

Visual mods can still have performance costs. The collection page warns that Battle Debris may lag when debris fields get large, and the ASB particle addon increases observable weapon particles. These are "visual" in theme but performance-sensitive in practice.

Project posture: keep performance-sensitive visuals separate from harmless static visuals.

## DLC Assumptions

The author's DLC thread says many mods are visual only and do not require DLC, but gameplay-changing mods may require or strongly recommend specific DLC. Examples called out include Leviathans for some ESC NEXT/Guilli content, and Ancient Relics, Utopia, Synthetic Dawn, Nemesis, First Contact, Machine Age, or other DLC for various event, empire, and machine-related mods.

Project posture: document local owned DLC before finalizing a playset. If all DLC is available, the collection's default assumption is simpler.

## Recommended Customization Strategy

1. Preserve the original collection link, load-order discussion, and Irony text-list discussion in local notes.
2. Import or reproduce the author's load order exactly before making preference changes.
3. Decide the big gameplay pillars first: Gigas, NSC3, ESC NEXT, Planetary Diversity, Guilli, Starbase Extended, Stellar AI, and event/archeology/rift packs.
4. Keep required infrastructure and patches for retained parent mods: UIOD, UIOD compatibility patches, Universal Resource Patch, and parent-specific patches.
5. Treat shipsets, portraits, flags, rooms, namelists, and simple graphic flavor as low priority for removal unless they clutter UI/readability or introduce compatibility warnings.
6. Review performance-sensitive visuals separately from static visuals.
7. Add trait/empire-creation mods only after the base collection is stable in Irony and a small test game.
8. Run an Irony conflict pass after every meaningful gameplay-system change.
9. Launch-test with a tiny galaxy before starting the intended campaign settings.

## Initial Keep / Review / Optional Buckets

### Strong Keep Candidates

- UI Overhaul Dynamic and required UIOD patches for retained parent mods.
- Universal Resource Patch.
- Gigastructural Engineering if the campaign wants megastructures and optional crises.
- NSC3 if the campaign wants ship-class and naval expansion.
- ESC NEXT if the NSC3 reactor-disable step is followed.
- Planetary Diversity and Guilli's Planet Modifiers if the campaign wants exploration and planet variety.
- Starbase Extended if review confirms it supports the user's defense-focused goals.

### Review Before Keeping

- More Events Mod.
- Archaeology Story Pack.
- Forgotten Empires.
- Extra Events.
- AI-Player Exclusive Archaeology & Astral Rifts.
- Unique Systems Guaranteed.
- More Primitives.
- Planet Raider.
- Chris' Covert Operations.
- Stellar AI.
- Battle Debris and high-particle ASB addons.
- Any portrait mod that adds traits, civics, tech, or ships.
- Any non-collection shipset or NSC3 shipset patch.

### Low-Risk Optional Flavor

- Shipsets already covered by the collection's instructions.
- Portrait-only packs.
- Flags and emblems.
- Namelists.
- Rooms, clothing, hair, and species presentation graphics.
- Simple city, camera, and interface visuals.

## Suggested Game Settings From The Author

The author's settings thread is a recommendation, not a requirement. It suggests:

- Ironman disabled.
- 200-800 star galaxies.
- Lower habitable worlds, often 0.25x.
- AI empire count scaled to galaxy size.
- Fallen Empires around 1-2.
- Random crisis, with crisis strength scaled by galaxy size.
- Hyperlane density around 0.5x to 1x.
- Gateways and wormholes above default.
- Clustered empire placement required when using No Clustered Starts.

Project posture: these settings imply the collection is tuned for exploration density and modded content discovery while trying to control colony/pop explosion. Keep this in mind before increasing habitable worlds or AI counts.

## Troubleshooting Boundary

The author's fresh-reload troubleshooting thread includes deleting or preserving specific files under the Paradox Stellaris user folder. Treat that as manual troubleshooting guidance only. Do not delete launcher, user, save, or mod-manager state from Codex without explicit user approval and a verified backup/restore plan.

## Open Questions For The Next Pass

- Which DLC are installed locally and should be assumed for this playset?
- Do we want Gigas optional crises enabled, disabled, or tuned down?
- Do we want NSC3 as a firm pillar, or should we consider the collection's documented NSC3-removal path?
- Which event/archeology/rift packs are actually desired versus merely included?
- Does Stellar AI understand the retained major systems well enough for this playset?
- Which trait/empire-creation mods should be added after the collection baseline is stable?
- Should we create a local Irony playset snapshot and conflict report for the unmodified collection first?
