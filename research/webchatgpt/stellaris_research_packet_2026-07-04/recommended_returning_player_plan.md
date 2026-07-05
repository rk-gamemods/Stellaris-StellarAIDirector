# Recommended Returning Player Plan

**Research date:** 2026-07-04  
**Primary research window:** 2026-06-04 to 2026-07-04  
**Platform assumption:** Steam PC build, Steam Workshop as default mod ecosystem.  
**Citation convention:** Bracketed IDs such as `[S01]` or `[M14]` resolve to full source URL, publication/update date, retrieval date, and reliability notes in `source_inventory.csv`. Rows in the CSV matrices include raw source URLs.  


## Goal

Build confidence in modern Stellaris before committing to a long modded campaign. The plan assumes Steam, live 4.4.4 stable, and a preference for Steam Workshop mods. [S01, S05]

## Stage 0 — setup and vanilla reacclimation checklist

1. **Select the stable branch.** In Steam, avoid `stellaris_test` unless deliberately testing 4.4.5/4.5 beta content. The live baseline is 4.4.4; 4.4.5 and 4.5 are beta/testing tracks. [S01, S02, S03]
2. **Create a clean launcher playset called `00_Vanilla_4.4.4`.** Disable every mod and launch once. The Steam store confirms Workshop support; the official launcher remains the final game-launch surface. [S05, S13]
3. **Start a new vanilla save.** Do not load an old multi-year save first; 4.4.4 fixed old-save startup crashes, but official patch notes still advise backing up saves when changing versions. [S01]
4. **Play a settled empire for 2–4 hours.** Learn the post-4.3 economy/fleet scale and 4.4 UI/job/Situation Log changes before adding large mods. [S07, S04, S01]
5. **Do one short Nomad test separately.** The Nomads DLC is current and interesting, but its Operational Reserves, Wayline logistics and Arkship/Waystation systems are still the active balance/bug area. [S04, S02, S09]

## Stage 1 — light QoL mod list

Use this after the vanilla launch works.

Recommended list:

1. UI Overhaul Dynamic — `https://steamcommunity.com/sharedfiles/filedetails/?id=1623423360` [M01]
2. UI Overhaul Dynamic - Tiny Outliner — `https://steamcommunity.com/sharedfiles/filedetails/?id=1628912584` [M04]
3. Optional UIOD submods from the official collection, especially Improved Text or Planet View Performance Mode — `https://steamcommunity.com/workshop/filedetails/?id=2094085974` [M05]

Do not add Full Tiny Outliner if using UIOD. Full Tiny Outliner is for non-UIOD lists and explicitly says it is not compatible with UIOD. [M03, M04]

Smoke test:

- Launch a new game.
- Open diplomacy, situation log, planet view, fleet manager, species screen, ship designer, and outliner.
- Save, reload, and open the same UI panels again.
- If UIOD causes a crash on diplomacy, check whether you are on the latest July 3 main mod and whether you accidentally installed the beta plugin on stable. [M01, M02, S11]

## Stage 2 — medium vanilla+ content setup

Add content only after Stage 1 succeeds.

Recommended list:

1. UI Overhaul Dynamic. [M01]
2. UI Overhaul Dynamic - Tiny Outliner. [M04]
3. Guilli’s Planet Modifiers and Features. [M06, M07]
4. More Events Mod. [M08]
5. Planetary Diversity. [M10]
6. AI Game Performance Optimisation 4.4, configured conservatively. [M20]

Optional after one successful 50-year test:

- Stellar AI, but only if you want stronger research/economy AI and will not use any other AI overhaul. [M19]
- Dynamic Political Events, if you want internal-political flavor and are not focused on Nomad-specific play. [M21]
- Amazing Space Battles, if you want battle visuals and can tolerate battle pacing/performance changes. [M23]

Testing process:

- Start a new save.
- Run observer or hands-off speed 3–5 to year 2230.
- Check `Documents/Paradox Interactive/Stellaris/logs/error.log` after exit.
- Add one optional mod at a time and repeat.
- Never add NSC3/Gigas/ESC into an ongoing Stage 2 save.

## Stage 3 — ambitious overhaul setup

Use this only after a stable medium campaign or when you are comfortable abandoning a test save.

Core candidates:

1. UI Overhaul Dynamic, required by NSC3. [M01, M17]
2. NSC3. [M17, M18]
3. Extra Ship Components NEXT, loaded before NSC3 if used. [M16]
4. Gigastructural Engineering & More. [M14, M15]
5. AI Game Performance Optimisation 4.4, configured for late-game survivability. [M20]
6. Optional Planetary Diversity and Guilli’s Planet Modifiers, because both have current compatibility signals and GPM specifically mentions compatibility work with Planetary Diversity/Gigas/Real Space. [M06, M10]

Major caveats:

- NSC3 requires UIOD and can affect ship-size definitions; use a new save. [M17, M18]
- ESC NEXT warns against old ESC 3.0 saves and documents ESC-before-NSC3 load order. [M16]
- Gigas has known issues involving `habitable_structure`, custom topbar resources, and Real Space System Scale geometry. [M15]
- Real Space 4.0 says 4.4.3 rather than 4.4.4, so add it only after the rest of the ambitious stack passes a test. [M12]

## Stage 4 — total conversion setup

Treat each total conversion as a separate game.

Current-live candidate:

- Star Trek: New Civilisations — `https://steamcommunity.com/sharedfiles/filedetails/?id=1886496498`; currently says STNC-2607 and Stellaris 4.4.4 compatible. [M33]

Rollback/watchlist candidates:

- Star Trek: New Horizons — currently says 4.3.7 Compatible WIP; use only with rollback or after a 4.4 update. [M34]
- Star Wars: Legacy of the Old Republic — currently says Cetus 4.3.7 compatible and warns most mods are incompatible. [M36]
- Star Wars: New Dawn — currently says Phoenix 4.3.7 compatible. [M37]

For STNH, use only the main mod, optional TNG submod, one official UI submod, and optional music mod; the page says multiple UI submods can crash and recommends 16 GB RAM minimum. [M34, M35]

## Suggested load-order strategy

Use the launcher for final playset activation and **Irony Mod Manager** for conflict/load-order diagnostics if the list gets beyond a handful of mods. Irony is current, cross-platform, conflict-aware, and deterministic, but it does not replace actual in-game smoke testing. [T01, T02, T03]

General order strategy for the recommended list:

1. Framework/core content and gameplay mods.
2. Planet/event/story mods.
3. AI/performance mods.
4. Ship/component/mega overhauls, respecting mod-specific notes.
5. UI mods near the bottom.
6. UIOD compatibility patches and specific UI overrides below UIOD when instructed.

Specific rules:

- UIOD says bottom/last except compatches/specific overrides. [M01]
- UIOD Tiny Outliner loads after UIOD and replaces outliner behavior within the UIOD ecosystem. [M04]
- ESC should load before NSC3. [M16]
- Real Space modules should load very low/bottom in their own ecosystem, but Real Space System Scale conflicts with Gigas known issues. [M12, M15]
- Use one AI overhaul only. [M19]

## What to avoid for now

- Any beta branch or beta-only mod in a serious stable campaign. [S02, S03, M02]
- Full Tiny Outliner with UIOD. [M03, M04]
- StarNet AI / StarTech AI for current live 4.4.4. [M30, M31]
- More Traditions until the author’s Nomads caveats and crash comments settle. [M29]
- Archaeology Story Pack 4.4 in a Nomad campaign until the Arkship/homeworld issue is clarified. [M09]
- Beautiful Universe v2.0 until the 4.4/UIOD crash watch signal clears. [M25]
- STNH, LoToR, and New Dawn on live 4.4.4 unless their pages update. [M34, M36, M37]

## Tooling workflow for Codex follow-up

Use the included CSV files as Codex inputs. The next planning step should be to build a local helper script that:

1. Reads Steam Workshop IDs and `descriptor.mod` metadata from subscribed mods. [S13, T09]
2. Emits `mods.json`, `overwritten_paths.csv`, and `load_order.md`.
3. Runs CWTools.CLI or cwtools-action-compatible validation on unpacked/local mod files. [T05, T08]
4. Optionally reads Irony profile/export/config files if available and compares them with the launcher playset. [T01, T03]
5. Flags version mismatches, beta-only mods, duplicate UI/outliner mods, multiple AI overhauls, and known risky pairs from `steam_workshop_mod_matrix.csv`.

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
