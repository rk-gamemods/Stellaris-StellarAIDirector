# Stellaris 30-Day Modding Scene Report

**Research date:** 2026-07-04  
**Primary research window:** 2026-06-04 to 2026-07-04  
**Platform assumption:** Steam PC build, Steam Workshop as default mod ecosystem.  
**Citation convention:** Bracketed IDs such as `[S01]` or `[M14]` resolve to full source URL, publication/update date, retrieval date, and reliability notes in `source_inventory.csv`. Rows in the CSV matrices include raw source URLs.  


## Executive readout

The Steam Workshop scene is active but patch-sensitive. Several pillar mods were updated inside the 30-day window and either explicitly support 4.4 or are very close to the 4.4.4 live branch: UI Overhaul Dynamic, Guilli’s Planet Modifiers and Features, More Events Mod, Planetary Diversity, Gigastructural Engineering, NSC3, Stellar AI, AI Game Performance Optimisation, Amazing Space Battles, and Star Trek: New Civilisations. [M01, M06, M08, M10, M14, M17, M19, M20, M23, M33]

The scene is also riskier than usual because 4.4/Nomads changed Arkship, Waystation, colony/planet, logistics, UI, scripted modifier, and AI behavior. Official 4.4.4 notes explicitly call out modder-facing changes and the need to update scripted modifiers to work on colonies rather than planets; community collection notes warned that the 4.4 Arkship-economy split would create major compatibility work. [S01, S12]

Best safe default for a returning Steam player: start with **UIOD + UIOD Tiny Outliner**, then add **Guilli’s Planet Modifiers**, **More Events Mod**, and **Planetary Diversity** only after a short vanilla reacclimation. Add **AI Game Performance Optimisation** or **Stellar AI** in a second test campaign, not in the first launch. [M01, M04, M06, M08, M10, M19, M20]

## Reliability tiers used in the CSV matrix

- **5 - safe default:** active, current 4.4 support, long adoption history, limited or well-understood conflict surface.
- **4 - good but test:** active/current and useful, but changes AI/performance/combat/graphics enough to deserve a test save.
- **3 - usable with caveats:** active or close to current but large, invasive, or version-lagged by a minor patch.
- **2 - watchlist:** popular or promising, but beta-only, stale by one major version, or with current crash/compatibility warnings.
- **1 - avoid current live:** stale/obsolete or not suited to 4.4.4 live.

## UI and QoL

**UI Overhaul Dynamic** is the core UI recommendation. It showed a July 3 update, claims “For 4.4,” has a very large subscriber base, supports multiplayer even when others do not use it, adapts UI to resolution, expands major windows, and says to load it at the bottom/last except compatches/specific overrides. [M01]

Use **UI Overhaul Dynamic - Tiny Outliner** if using UIOD. It requires UIOD, is labeled for 4.4, and says not to run it with other outliner mods. [M04]

Use **Full Tiny Outliner** only if you do **not** use UIOD. It claims 4.4.x compatibility and save/achievement/multiplayer friendliness but explicitly says it is not compatible with UI Overhaul Dynamic. [M03]

Avoid mixing live and beta UI tracks: **UI Overhaul Dynamic Beta** is for the **4.4.5 Pegasus Open Beta**, requires UIOD, and should load after the main mod. That is a beta-branch tool, not a stable 4.4.4 recommendation. [M02, S02]

## Events, story, exploration, and planets

**Guilli’s Planet Modifiers and Features** is one of the strongest vanilla+ content picks. It was updated on June 28, says 4.4+, adds hundreds of planetary modifiers/features, notes compatibility support for Planetary Diversity, Gigastructures, and Real Space, and a modder update says the 4.4/Nomads pass added Arkship visit/expedition content while reducing base-game event overwrites. [M06, M07]

**More Events Mod** remains a high-confidence story/event expansion. It was updated June 24, claims 4.4.* compatibility, and adds anomalies, archaeology, astral rift, primitive/colony/country/special-system events, origins, questlines, and crises. [M08]

**Planetary Diversity** is a high-confidence planet-variety mod. It was updated June 20, claims 4.4.* support, and uses startup events/art to add planet variety rather than simply increasing planet count. [M10]

**Archaeology Story Pack 4.4** is a watchlist item. It was updated June 18 and is labeled 4.4, but the page text also references 4.3 and comments report a Nomad/Arkship homeworld issue. Use only after a separate settled-empire test and never alongside the old Archaeology Story Pack version. [M09]

## Performance and AI

**AI Game Performance Optimisation 4.4** is the best performance utility currently found. It was updated June 28 and exposes configurable options to limit lag drivers such as AI gateway/habitat/subspecies/fleet/market behaviors. It is not neutral: it changes AI behavior and galaxy systems, so enable options deliberately. [M20]

**Stellar AI** is the current AI-overhaul recommendation. It was updated June 24, says it was rebuilt on 4.4/Nomads definitions, preserves Arkship/Nomad logic, and warns that AI overhauls touching the same definitions are incompatible. Use only one AI overhaul at a time. [M19]

**StarNet AI** and **StarTech AI** should not be used for a 4.4.4 return list. Both are stale relative to the current patch, and StarTech comments indicate current-functionality concerns. Their old compatibility/load-order notes remain background only. [M30, M31]

## Megastructures, ships, components, and combat

**Gigastructural Engineering & More (4.4)** is actively maintained and popular, but it is not a safe-default returning-player mod. It was updated June 30 and adds megastructures, optional crises, a mod menu, achievements, origins, exploration content, and improved AI use of megastructures. It also overwrites/affects core megastructure and habitable-structure behavior and documents known issues such as custom resources not displaying correctly in the topbar and Real Space System Scale causing clipping/exploded ringworlds. [M14, M15]

**NSC3** is current and major. It requires UI Overhaul Dynamic, was updated June 28, and GitHub releases show Update 27 on June 29 after a June 27 4.4 update. Update 26 recommended a new save, and NSC still interacts with ship-size definitions and vanilla ship classes. Use only in an ambitious new campaign after testing UIOD and any ship/component mods. [M17, M18]

**Extra Ship Components NEXT** is a strong ship-tech mod but needs a new-game mindset. It was updated June 20, warns against use with old ESC 3.0 saves, and says ESC should load before NSC3 when combined. [M16]

**Amazing Space Battles** is current and attractive but not purely cosmetic: it changes visual effects, battle spacing/movement, targeting, explosions and battle duration. Use if you want battle spectacle and have tested performance. [M23]

## Graphics and map/skybox mods

**Immersive Galaxy and Skybox** is the better current skybox pick than Beautiful Universe if you want a large graphics package. It was updated June 19, advertises 117 skyboxes and built-in compatibility with Gigas, Real Space and Hypothetical Stars. Recent comments mention crash/bloom issues, so test it before adding gameplay mods. [M24]

**Beautiful Universe v2.0** is on watchlist/avoid for now. Its concept is fine, but recent comments and author notes point to possible 4.4/UIOD crash issues and newer alternatives. [M25]

**Light Borders + Swapped Colors + Star Pins [4.0+]** is a lightweight optional fork. It claims 4.0+/4.3 compatibility and achievement friendliness but had no explicit 4.4 claim observed. The original **Light Borders + Star Pins** is stale and should be avoided. [M26, M27]

## Diplomacy, politics, traditions, and roleplay

**Dynamic Political Events** is still useful for internal-politics flavor, but it was not updated inside the 30-day window. It claims compatibility with event mods including More Events and says it is maintained for bugs/vanilla compatibility, but it should be treated as a medium-confidence addition, especially for Nomad games. [M21]

**Expanded Stellaris Traditions** claims 4.4.* and was updated June 15, but tradition mods are balance/system mods, not light QoL. Test it standalone before combining with ascension-slot, perk, UI, or tradition-layout mods. [M28]

**More Traditions** is a watchlist/do-not-use-yet item for returning-player plans. Its own page says it was updated for 4.4 but not fully refined, that some traditions are not updated for Nomads, and comments report breakage/crashes. [M29]

**DarkSpace (Stellaris 4.4)** is a current, broad Vanilla+ roleplay mod. It is interesting for a second or third campaign, not the first reacclimation list, because it adds many origins, civics, species/ship/FE/Nomad-related systems and therefore has a wide interaction surface. [M22]

## Total conversions

**Star Trek: New Civilisations** is the standout current-live total conversion: it was updated July 3 and explicitly says STNC-2607 is Stellaris 4.4.4 compatible. Treat it as a separate game/playset, not a mod to combine with vanilla UI/AI/megastructure/ship overhauls. [M33]

**Star Trek: New Horizons** is still active but currently lists **4.3.7 Compatible WIP**. Its page recommends deactivating other mods, using only STNH main + optional TNG/UI/music submods, using no more than one STNH UI submod, and having 16 GB RAM minimum. Do not use on live 4.4.4 unless it updates; roll back to 4.3.7 for an STNH campaign. [M34, M35]

**Star Wars: Legacy of the Old Republic** and **Star Wars: New Dawn** are currently 4.3.7-targeted, not 4.4.4-targeted. LoToR’s page also warns it is a total overhaul incompatible with the vast majority of mods, and UI mods can hide custom resources/buttons. [M36, M37]

## Current compatibility-risk map

- **UIOD vs Full Tiny Outliner:** choose one UI/outliner ecosystem. Use UIOD + UIOD Tiny Outliner, or Full Tiny Outliner without UIOD. [M01, M03, M04]
- **UIOD load order:** UIOD says to load at the bottom/last except compatches or specific overrides. [M01]
- **ESC + NSC3:** ESC says it should load before NSC3 when combined. [M16]
- **One AI overhaul only:** Stellar AI warns against AI overhauls replacing the same definitions; StarNet/StarTech are stale. [M19, M30, M31]
- **Gigas + Real Space System Scale:** Gigas known issues flag Real Space System Scale as causing clipping/exploded ringworlds. [M15]
- **Total conversions:** STNC, STNH, LoToR, and New Dawn should be separate playsets, not mixed with standard vanilla+ stacks unless their docs explicitly say so. [M33, M34, M36, M37]
- **UI track mixing:** UIOD Beta targeted the 4.4.5 beta when this packet was written. As of 2026-07-08, 4.4.5 is the live target; re-check UIOD main/beta page guidance before using a beta UI track in the current playset. [M02, S02]

## Safe-default shortlist

1. UI Overhaul Dynamic. [M01]
2. UI Overhaul Dynamic - Tiny Outliner. [M04]
3. Guilli’s Planet Modifiers and Features. [M06, M07]
4. More Events Mod. [M08]
5. Planetary Diversity. [M10]

## Medium setup additions after testing

1. AI Game Performance Optimisation 4.4. [M20]
2. Stellar AI, but only if you want a more demanding AI and will not run another AI overhaul. [M19]
3. Dynamic Political Events. [M21]
4. Amazing Space Battles. [M23]
5. Immersive Galaxy and Skybox if you want graphics and can tolerate a large asset mod. [M24]

## Ambitious overhaul stack candidates

1. Gigastructural Engineering & More. [M14, M15]
2. NSC3. [M17, M18]
3. Extra Ship Components NEXT. [M16]
4. Real Space 4.0, but only if you are not also using scale-sensitive megastructure combinations without patches. [M12, M15]
5. Star Trek: New Civilisations as a separate total-conversion playset. [M33]

## Do-not-use-yet / watchlist

- UI Overhaul Dynamic Beta on stable 4.4.4: beta-only. [M02]
- Archaeology Story Pack 4.4 for Nomads: inconsistent version text and Nomad issue report. [M09]
- More Traditions: own-page warning plus crash/breakage comments. [M29]
- Beautiful Universe v2.0: possible 4.4/UIOD crash watch; use Immersive Galaxy/Skybox instead if desired. [M25]
- StarNet AI and StarTech AI: stale relative to 4.4. [M30, M31]
- STNH, LoToR, New Dawn on live 4.4.4: currently 4.3.7-targeted. [M34, M36, M37]

## Source ID appendix

- **S01** — Stellaris 4.4.4 patch released (5505) - official Steam news — 2026-06-24 — retrieved 2026-07-04 — https://store.steampowered.com/oldnews/?appgroupname=Stellaris+-+Galaxy+Edition&appids=281990&feed=steam_community_announcements
- **S02** — Stellaris 4.4.5 "Pegasus" Early Open Beta notes - official Steam news — 2026-06-25 — retrieved 2026-07-04 — https://store.steampowered.com/oldnews/?appgroupname=Stellaris+-+Galaxy+Edition&appids=281990&feed=steam_community_announcements
- **S03** — Stellaris Dev Diary #427 - 4.5 Cygnus Open Beta context — 2026-07-02 — retrieved 2026-07-04 — https://store.steampowered.com/oldnews/?appgroupname=Stellaris+-+Galaxy+Edition&appids=281990&feed=steam_community_announcements
- **S04** — Paradox launches Nomads and 4.4 Pegasus — 2026-06-15 — retrieved 2026-07-04 — https://www.paradoxinteractive.com/media/press-releases/press-release/paradox-interactive-launches-major-expansion-and-free-update-for-stellaris
- **S05** — Stellaris Steam Store page — Live page retrieved 2026-07-04 — retrieved 2026-07-04 — https://store.steampowered.com/app/281990/Stellaris/
- **S06** — SteamDB Stellaris app info — Last record update 2026-07-02 UTC — retrieved 2026-07-04 — https://steamdb.info/app/281990/info/
- **S07** — Stellaris 4.3 Cetus update available - official Paradox forum/news — 2026-03-18 — retrieved 2026-07-04 — https://forum.paradoxplaza.com/forum/threads/stellaris-4-3-cetus-update-available-now.1710591/
- **S08** — Stellaris BioGenesis and 4.0 Phoenix release - official Paradox press release — 2025-05-05 — retrieved 2026-07-04 — https://www.paradoxinteractive.com/media/press-releases/press-release/paradox-interactive-releases-biogenesis-expansion-for-stellaris
- **S09** — PC Gamer: Stellaris Nomads impressions/review feature — 2026-06-17 — retrieved 2026-07-04 — https://www.pcgamer.com/games/strategy/stellaris-nomads-expansion-finally-lets-me-live-out-my-battlestar-galactica-fantasies-though-its-wayline-system-could-definitely-use-some-work/
- **S10** — Output Lag: Stellaris Nomads Review — 2026-07-01 — retrieved 2026-07-04 — https://outputlag.com/game-reviews/stellaris-nomads-review/
- **S11** — Reddit thread: UI Overhaul Dynamic 4.4.4 crash report — 2026-07-03 approx. / Reddit relative timestamp — retrieved 2026-07-04 — https://www.reddit.com/r/Stellaris/comments/1ueduft/for_anyone_wonder_ui_overhaul_dynamic_isnt/
- **S12** — Chinese Steam Workshop collection note on 4.4 compatibility disruption — 2026-06-15 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2812398535
- **S13** — Stellaris Wiki: Modding tutorial — Live page retrieved 2026-07-04 — retrieved 2026-07-04 — https://stellaris.paradoxwikis.com/Modding_tutorial
- **M01** — Steam Workshop: UI Overhaul Dynamic — Updated 2026-07-03 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1623423360
- **M02** — Steam Workshop: UI Overhaul Dynamic Beta — Updated 2026-07-01 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=1665106451
- **M03** — Steam Workshop: Full Tiny Outliner — Updated 2026-06-16 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2948301103
- **M04** — Steam Workshop: UI Overhaul Dynamic - Tiny Outliner — Updated 2026-06-23 approx. / page retrieved 2026-07-04 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1628912584
- **M05** — Steam Workshop collection: UI Overhaul Dynamic - Submods — Updated 2026-06-23 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=2094085974
- **M06** — Steam Workshop: Guilli’s Planet Modifiers and Features — Updated 2026-06-28 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=865040033
- **M07** — Reddit: Guilli’s Planet Modifiers 4.4 update post — 2026-06-18 approx. — retrieved 2026-07-04 — https://www.reddit.com/r/Stellaris/comments/1u8dl57/guillis_planet_modifiers_updated_to_stellaris_44/
- **M08** — Steam Workshop: More Events Mod — Updated 2026-06-24 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=727000451
- **M09** — Steam Workshop: Archaeology Story Pack 4.4 — Updated 2026-06-18 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=3723865830
- **M10** — Steam Workshop: Planetary Diversity — Updated 2026-06-20 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=819148835
- **M11** — Steam Workshop collection: Planetary Diversity - All of Them — Collection metadata older; item snippets current to 4.4.* — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=2347023229
- **M12** — Steam Workshop: Real Space 4.0 — Updated 2026-06-19 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=937289339
- **M13** — Steam Workshop collection: Real Space Full Pack — Collection metadata 2025; component snippets current to 4.4/4.4.3 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=1323937078
- **M14** — Steam Workshop: Gigastructural Engineering & More (4.4) — Updated 2026-06-30 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1121692237
- **M15** — Steam Workshop: Gigastructural Engineering known issues / page discussion — Updated 2026-06-30 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1121692237
- **M16** — Steam Workshop: Extra Ship Components NEXT — Updated 2026-06-20 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=2648658105
- **M17** — Steam Workshop: NSC3 — Updated 2026-06-28 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/683230077
- **M18** — GitHub: NSC3 releases — Updated 2026-06-29 — retrieved 2026-07-04 — https://github.com/mrfreake/NSC3/releases
- **M19** — Steam Workshop: Stellar AI — Updated 2026-06-24 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=3610149307
- **M20** — Steam Workshop: AI Game Performance Optimisation 4.4 — Updated 2026-06-28 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2184737698
- **M21** — Steam Workshop: Dynamic Political Events — Updated 2026-04-19 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1227620643
- **M22** — Steam Workshop: DarkSpace (Stellaris 4.4) — Updated 2026-06-15 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2719075597
- **M23** — Steam Workshop: Amazing Space Battles — Updated 2026-06-26 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1878473679
- **M24** — Steam Workshop: Immersive Galaxy and Skybox — Updated 2026-06-19 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2407436476
- **M25** — Steam Workshop: Beautiful Universe v2.0 — Updated 2026-06-26 comments; mod older — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=697938908
- **M26** — Steam Workshop: Light Borders + Swapped Colors + Star Pins [4.0+] — Updated 2026-05-15 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=3477695569
- **M27** — Steam Workshop: Light Borders + Star Pins original — Updated 2021-04-15 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2098862918
- **M28** — Steam Workshop: Expanded Stellaris Traditions — Updated 2026-06-15 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=946222466
- **M29** — Steam Workshop: More Traditions — Updated 2026-06-18 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=3067902147
- **M30** — Steam Workshop: StarNet AI — Updated 2024-05-12 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=1712760331
- **M31** — Steam Workshop: StarTech AI — Updated 2024-05-12 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2494712590
- **M32** — Steam Workshop: Starnet AI + AI Game Performance Optimisation Fix — Updated 2022 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2858696190
- **M33** — Steam Workshop: Star Trek New Civilisations — Updated 2026-07-03 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1886496498
- **M34** — Steam Workshop: Star Trek New Horizons — Updated 2026-06-14 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=688086068
- **M35** — Steam Workshop collection: ST New Horizons - A Star Trek Collection — Updated 2026-ish / page retrieved 2026-07-04 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=687674478
- **M36** — Steam Workshop: Star Wars Legacy of the Old Republic — Updated 2026-05-11 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=2791119024
- **M37** — Steam Workshop: Star Wars New Dawn — Updated 2026-05-13 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=3575236236
- **C01** — Steam Workshop collection: Stellaris - Essentials for Pegasus 4.4.1 — Updated 2026-06-15 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/?id=1678742403
- **C02** — Steam Workshop collection: Gigastructural Engineering submods / compatibility links — Updated 2026-06-30 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1121692237
- **C03** — Steam Workshop collection: Amazing Space Battles collection — Updated 2026-06-26 — retrieved 2026-07-04 — https://steamcommunity.com/sharedfiles/filedetails/?id=1878473679
- **C04** — Steam Workshop collection: NSC Highly Recommended Companion Mods — Updated 2026-06-28 — retrieved 2026-07-04 — https://steamcommunity.com/workshop/filedetails/683230077
- **T01** — Irony Mod Manager website — Live page retrieved 2026-07-04 — retrieved 2026-07-04 — https://bcssov.github.io/IronyModManager/
- **T02** — GitHub: IronyModManager releases — Released 2026-06-19 (v1.27.189 shown) — retrieved 2026-07-04 — https://github.com/bcssov/IronyModManager/releases
- **T03** — GitHub: IronyModManager repository — Live page retrieved 2026-07-04 — retrieved 2026-07-04 — https://github.com/bcssov/IronyModManager
- **T04** — Steam Workshop discussion: Irony Mod Manager utility — 2020-06-26 background — retrieved 2026-07-04 — https://steamcommunity.com/workshop/discussions/18446744073709551615/2574319296481107914/?appid=281990
- **T05** — GitHub organization: CWTools — Updated 2026-06-30 / 2026-07-02 repos visible — retrieved 2026-07-04 — https://github.com/cwtools
- **T06** — Visual Studio Marketplace: CWTools - Paradox Language Services — Live page retrieved 2026-07-04 — retrieved 2026-07-04 — https://marketplace.visualstudio.com/items?itemName=tboby.cwtools-vscode
- **T07** — CWTools get started page — Live page retrieved 2026-07-04 — retrieved 2026-07-04 — https://cwtools.github.io/get-started.html
- **T08** — GitHub: cwtools-action — Live page retrieved 2026-07-04 — retrieved 2026-07-04 — https://github.com/cwtools/cwtools-action
- **T09** — Valve Developer Community: SteamCMD — Updated 2026-04-28 — retrieved 2026-07-04 — https://developer.valvesoftware.com/wiki/SteamCMD
- **T10** — GitHub: Paradoxos Mod Manager — Legacy / retrieved 2026-07-04 — retrieved 2026-07-04 — https://github.com/ThibautSF/ParadoxosModManager
- **T11** — GitHub: Paradoxos Mod Manager Rework — Legacy / retrieved 2026-07-04 — retrieved 2026-07-04 — https://github.com/ThibautSF/ParadoxosModManagerRework
- **T12** — Steam Community: Stellaris Mod Manager thread — 2017 / legacy — retrieved 2026-07-04 — https://steamcommunity.com/app/281990/discussions/0/142261352649027925
