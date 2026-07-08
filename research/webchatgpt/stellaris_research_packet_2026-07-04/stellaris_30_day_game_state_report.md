# Stellaris 30-Day Game State Report

**Research date:** 2026-07-04  
**Primary research window:** 2026-06-04 to 2026-07-04  
**Platform assumption:** Steam PC build, Steam Workshop as default mod ecosystem.  
**Citation convention:** Bracketed IDs such as `[S01]` or `[M14]` resolve to full source URL, publication/update date, retrieval date, and reliability notes in `source_inventory.csv`. Rows in the CSV matrices include raw source URLs.  


## Executive readout

The live public build to plan around is **Stellaris 4.4.4 “Pegasus”**, released on **2026-06-24** and stated by Paradox as ready on Steam, GOG, and MS Store. The stable branch should be treated as the return-to-play baseline; **4.4.5 “Pegasus”** and **4.5 “Cygnus”** are opt-in beta/testing tracks, with 4.4.5 explicitly described as still in development with minimal QA review and 4.5 described as a very early beta whose changes are tentative. [S01, S02, S03]

The major new live-context DLC is **Stellaris: Nomads**, released with the free **4.4 “Pegasus”** update on **2026-06-15**. Nomads adds Arkship-based mobile empires, Wayline Networks, contracts, Nomad origins, Stellar Cannon, and Champion’s Forge Live; the free update also brought war-joining/leaving changes, job-system and job-selection improvements, a reworked Situation Log UI, performance improvements, and bug fixes. [S04]

Steam sentiment is currently positive but not euphoric: the Steam page snapshot retrieved on 2026-07-04 shows **Recent Reviews: Mostly Positive**, with **72% of 982 recent reviews** positive, while long-run English reviews remain **Very Positive** at **86% of 76,159**. The same Steam store page confirms Steam Workshop support and shows the current expansion-subscription/DLC store context. [S05]

## Confirmed stable/beta branch context

| Branch | Status on 2026-07-04 | Practical implication |
|---|---:|---|
| 4.4.4 “Pegasus” | Current public/stable patch released 2026-06-24. [S01] | Use this for a serious returning-player campaign and for most Workshop mod plans. |
| 4.4.5 “Pegasus” | Opt-in `stellaris_test` beta released 2026-06-25; Paradox warned it had minimal QA review. [S02] | Use only for testing balance/resource changes and beta-specific UI/mod updates. Do not mix with a stable-branch mod list. |
| 4.5 “Cygnus” | Early Open Beta / experimental track discussed 2026-07-02; Paradox says changes are tentative and further July updates are expected. [S03] | Treat as future-facing modder/watchlist context, not a compatibility target for current campaigns. |

## Major gameplay and systems changes relevant to a returning player

### Nomads and Arkship economies

Nomads are a major mechanical departure from settled empire play: the expansion centers on Arkships, Waylines, Waystations, contract work, and mobile logistics instead of normal territorial expansion. Official launch materials describe Nomadic Empires, Arkships, Wayline Networks, the contract system, four Nomad origins, Defender of the Galaxy, Stellar Cannon, and Champion’s Forge Live. [S04]

Returning-player implication: a vanilla settled empire is still the best first reacclimation campaign. A Nomad run should be a second campaign or a short test because Arkship UI, Operational Reserves, Waystation logistics, and contract pacing are exactly where the patch cycle has been most active. [S01, S02, S09]

### Free 4.4 changes beyond the DLC

The free 4.4 update added the ability to join and leave wars in progress, improved job systems and job selection, reworked the Situation Log UI, and included performance improvements and bug fixes. [S04] Patch 4.4.4 added or refined Nomad logistics such as a Logistics Hub indicator, improved whole-system Arkship/logistic ship targeting, and science-ship automation behavior that stays automated when no reachable tasks temporarily exist. [S01]

### 4.3 background: lower fleet/economy scale and performance work

For context older than the 30-day window, the 4.3 “Cetus” update focused on performance/stability and deliberately cut back the “supercharged” 4.0 economies and navies. Paradox described smaller economies and navies, naval capacity changes to reduce ship counts, economy reductions, and a Custodian focus on performance and stability. [S07]

Returning-player implication: very old mental models about fleet sizes, economy snowballing, ascension strength, and late-game performance may be wrong. Modded play should avoid immediately stacking ship-count, pop-growth, megastructure, and economy overhauls before learning the 4.3/4.4 baseline. [S07, S01]

### 4.0/BioGenesis background

For a multi-year return, 4.0/BioGenesis is important background: Paradox’s 2025 release materials described overhauled genetic ascension, biological ships, a player-crisis path, new origins, a megastructure, and performance/gameplay improvements. [S08] This matters because 2026 ship, species, ascension, and biological content mods may assume post-4.0 file structures and balance.

## Technical, UI, performance, and modding changes

Patch 4.4.4 includes explicit performance and stability changes: improved empire creation UI performance, fixed recurring daily stutter from science-ship Excavate/Astral Rift automation when no reachable target existed, fixed a crash when starting from an old save, fixed hotjoin OOS, and changed resync behavior so the host reloads the save during resync to reduce OOS. [S01]

Patch 4.4.4 also added modding hooks: `category_limit_fail_text` for scripted actions, `context_menu_ordering` for scripted action target ordering, per-ship-class shield multipliers, `collected_colony_resources`, and `AI_HOSTILE_FLEET_DISTANCE`. [S01] A key modding implication is that many 4.3-era or older mods touching colonies, planets, scripted modifiers, starbase/colony resource logic, ship classes, and UI windows may need actual adaptation rather than a simple supported-version string bump.

Paradox specifically noted in the 4.4.4 patch notes that numerous scripted modifiers needed to be updated to work on **colonies rather than planets** for Arkships. [S01] A Chinese collection maintainer independently warned on 2026-06-15 that 4.4’s colony/planet split for Arkship economy would create major mod adaptation problems and make adaptation take longer. That community warning is not official, but it matches the official patch-note direction. [S12, S01]

## Known current bugs, stability issues, and pain points

### Fixed or partially fixed in the public patch cycle

Early after 4.4.1/Nomads, Paradox reported many crash reports, especially from low-resolution Waystation UI truncation, and said the 4.4.2 stability fixes addressed over 90% of crashes reported in the first 24 hours. [S01] The 4.4.4 public patch then included fixes for AI contract-evaluation crashes, crashes involving modded Waystation UI cases, old-save startup crashes, and multiplayer OOS issues. [S01]

### Still-current or watchlist pain points

Historical July 4 posture: the then-active beta cycle was a signal that some Nomads economy and balance rough edges remained. As of 2026-07-08, 4.4.5 is live; its notes add a Resource Abundance slider, rework Operational Reserves, adjust Forever Cruise starting conditions/upkeep, add fallback logic for Champion's Forge Live, adjust fauna/Waystation behavior, and include multiple Nomad economy/ship-order fixes. [S02]

Player and press sentiment converges around **Nomads being fresh but not fully frictionless**. PC Gamer praised the Battlestar/Arkship fantasy and new galaxy feel but criticized Wayline logistics and Operational Reserves as confusing or rough. Output Lag rated Nomads 7.8/10 and praised it as a conceptually daring expansion that rewards mobility/adaptation. [S09, S10]

### Modded-UI stability watch

A Reddit report around July 3 said UI Overhaul Dynamic caused a crash when opening the diplomacy screen on 4.4.4, while comments suggested using the UIOD beta plugin until the main mod merged fixes. [S11] The main UIOD Workshop page later showed a July 3 update and a 4.4 support claim, so this should be treated as a transient risk to retest rather than a reason to avoid UIOD entirely. [M01, S11]

## DLC assumptions for modded play

Steam currently lists Steam Workshop support, an expansion subscription, and a large DLC catalog. The Steam page also shows store/bundle context that includes modern DLC such as Nomads, BioGenesis, Shadows of the Shroud, The Machine Age, Cosmic Storms, Grand Archive, and older expansion/story/species packs. [S05]

For a returning player, the safest mod assumption is: **do not assume every Workshop mod is DLC-free even when it technically runs without DLC**. Many large mods gate content behind DLC, refer to DLC systems, or are balanced around players owning most expansions. Guilli’s page says DLC is not required but DLC-locked features stay DLC-locked; More Events disables achievements and adds many systems; Gigas/NSC/ESC interact with ship, megastructure, crisis, and component systems where DLC ownership can alter content exposure. [M06, M08, M14, M16, M17]

Practical recommendation: either use the subscription for a month during reacclimation, or declare a fixed DLC set before building a mod list and keep that DLC set unchanged for the save.

## Current player sentiment synthesis

Confirmed metrics: Steam recent reviews are 72% positive across 982 recent reviews as of retrieval, while long-run English reviews are 86% positive across 76,159 reviews. [S05]

Community/press sentiment is mixed-positive. The positive side centers on Arkship fantasy, mobility, new exploration texture, and the novelty of living outside borders. The negative side centers on balance clarity, Operational Reserves, Wayline/logistics friction, early crashes, and the turbulence of major-patch mod compatibility. [S09, S10, S11, S12]

## Returning-player implications

1. **Start on stable 4.4.4, not beta.** Use betas only for test saves and beta-specific mod branches. [S01, S02, S03]
2. **Play 2–4 hours vanilla before subscribing to heavy mods.** The 4.3/4.4 economy, fleet, UI, job, and Nomad systems changed enough that an old 2.x/3.x intuition will mislead you. [S07, S04, S01]
3. **Use a new save for major mods.** Official patch notes warn save compatibility is not guaranteed between versions, and NSC3/Gigas/ship/AI/tradition mods each affect core systems. [S01, M14, M17, M19, M28]
4. **Do not mix UI tracks blindly.** UIOD Beta targeted 4.4.5 beta when this packet was written; because 4.4.5 is now live, re-check UIOD main/beta page guidance before using a beta UI track. [M01, M02, S02]
5. **Treat total conversions as separate games.** STNC is current for 4.4.4; STNH, LoToR, and New Dawn are currently 4.3.7-targeted and require rollback or waiting. [M33, M34, M36, M37]

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
