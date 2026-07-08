# Stellaris 30-Day Research Brief - July 4, 2026

## Summary

2026-07-08 update: this brief is now historical for the July 4 research
window. Stellaris 4.4.5 "Pegasus" is live on the stable 4.4 branch and is the
current local target for new work; use `research/stellar-ai/stellar-ai-director-4-4-5-compatibility-triage-2026-07-08.md`
for the current 4.4.5 compatibility posture.

Stellaris is currently in the 4.4 "Pegasus" / Nomads cycle. The stable version identified during this research window is 4.4.4, checksum 5505, released June 24, 2026. A 4.4.5 Pegasus open beta is also active, so the game is still in a hotfix-and-beta tail after the June 15 Nomads launch.

For a returning Steam player, the safest path is: reacclimate on current vanilla first, add UI-only/QoL mods next, then add medium content mods one at a time. Treat large ship/megastructure/ethics overhauls as new-save projects that need Irony Mod Manager and compatibility patch review.

Raw last30days artifacts:

- `research/last30days/stellaris-current-state-patch-dlc-bugs-performance-player-sentiment-raw-v3.md`
- `research/last30days/stellaris-steam-workshop-mods-popular-reliable-compatibility-collections-raw-v3.md`
- `research/last30days/stellaris-modding-tools-mod-manager-conflict-analyzer-cli-steam-workshop-raw-v3.md`

Coverage note: the engine returned Reddit, YouTube-adjacent/social, X, GitHub, Hacker News, Digg, and web/grounding evidence across the runs. TikTok and Instagram were not available because no ScrapeCreators key was configured.

## Current Game State

- Current stable anchor: Stellaris 4.4.4 "Pegasus", checksum 5505, released June 24, 2026. The patch notes focus on Nomads/Arkships, balance, AI, UI, QoL, bug fixes, and performance.
- Current expansion anchor: Nomads launched June 15, 2026 alongside free update 4.4 "Pegasus". Paradox describes Nomads as Arkship-centered, non-territorial play with waylines, contracts, and nomadic empires.
- Returning-player delta: since pre-2024/2025 play, the game has had major systemic churn, including 4.0 "Phoenix" performance/pop/economy changes, 4.3 base-game DLC integration, and 4.4 UI/job/war/situation changes.
- DLC assumptions changed: Utopia, Synthetic Dawn, Humanoids, and most Galaxy Edition elements were rolled into the base game in the 4.3.x window. Mod pages and old compatibility notes may still assume older DLC ownership boundaries.
- Current issue posture: 4.4.5 open beta notes and social posts show active follow-up fixes after 4.4.4, including Nomads UI/UX and a science-ship automation daily-stutter fix. Do not freeze a large mod list until the stable branch settles further.

## Steam Workshop Mod Matrix

| Mod or Family | Current Signal | Reliability | Risk | Recommendation |
|---|---:|---|---|---|
| UI Overhaul Dynamic | Steam page says 4.4, updated July 3, huge subscriber base | High | Low-medium | Best first mod. Add its submods/patches carefully. |
| UIOD Extended Topbar / Improved Font / Tiny Outliner / Planet View Performance | 4.4-tagged submods exist | High | Low-medium | Good light QoL layer. Verify achievement/checksum goals. |
| Planetary Diversity | Steam page says Stellaris 4.4.* and active changelog | High | Medium | Good medium content pick; use UIOD + PD patch if using UIOD. |
| Guilli's Planet Modifiers and Features | Steam page says 4.4+ | High-medium | Medium | Strong Vanilla+ content, but broad gameplay surface. |
| Real Space 4.0 | Page says v4.0.9 compatible with 4.4.3; comments report some 4.4.4 success | Medium | Medium | Use after a vanilla/QoL baseline. Watch exact 4.4.4 updates. |
| More Events Mod | Page says compatible with 4.4.* | Medium-high | Medium | Good event layer; not achievement compatible. |
| Dynamic Political Events | Says low overlap with known event mods including More Events | Medium | Medium | Add after More Events only if you want political flavor. |
| Gigastructural Engineering & More (4.4) | 4.4 page, June 30 update, huge overhaul | Medium-high | High | Ambitious-run mod, not a returning-player default. |
| NSC3 | June 27 update says updated for 4.4 and new save recommended | Medium | High | Powerful but volatile; use only in a dedicated new-save list. |
| Ethics & Civics branches | Bug Branch says updated to 4.4; Classic comments report crashes/lagging workshop fixes | Mixed | High | Prefer maintained forks; avoid Classic until verified. |
| Universal Modifier Patch | 4.4.* utility, broad dependency usage | Medium | Situational | Use only when mod docs or Irony conflicts indicate it is needed. |

## Bundles And Compatibility

- Collections are useful as discovery sources, not as truth. The 4.4 collection search results surfaced NSC3, Planetary Diversity, Real Space, More Events, Gigastructural, and patch utilities, but collection pages/comments can lag individual mod pages.
- UIOD has an explicit compatibility patch ecosystem. Follow each patch page's load order rather than using one generic order.
- Heavy overhauls often require new saves. NSC3 explicitly recommends a new save for its June 27 update.
- Compatibility patches matter more than raw load order once you combine UI, planet, ship, economy, and event mods.
- Watch for old "compatible" labels on workshop pages. Some Steam pages show Steam's generic incompatibility banner while the body says 4.4 support; treat the body, changelog, and comments together.

## Tooling Matrix

| Tool | Status | AI Friendliness | Use |
|---|---|---|---|
| Irony Mod Manager | Active GitHub repo, latest release v1.27.191 on June 30, 2026, 502 stars | Medium | Best available conflict-aware manager for Stellaris. GUI-oriented, but open source with logs, releases, issues, and deterministic concepts. |
| Paradox Launcher | Built-in | Low-medium | Good for basic playsets, weak for conflict analysis. 4.4 launcher behavior auto-disables mod lists on major update to reduce broken saves. |
| ParadoxosModManager | Historical/older | Medium | Background option only. Do not choose over Irony for current work. |
| Wiki/modding docs | Current enough for structure | High for parsing paths | Use for local mod descriptor layout, folder conventions, and manual validation. |
| Custom Codex helpers | Not needed first | High | Useful later for parsing playsets, checking Steam IDs, validating descriptors, and preparing Irony-friendly reports. |

Irony is the clear tool winner. Its docs say it understands game structures and FIOS/LIOS rules, supports deterministic load order management, and has conflict awareness. The Steam discussion explains its conflict solver as element-aware rather than filename-only and says it can generate patch mods, filter conflicts by mod, provide database search, and merge collections. The tradeoff is that it is still an advanced GUI tool, not a clean CLI-first automation surface.

## Recommended Returning-Player Plan

1. Vanilla reacclimation:
   - For an explicitly approved runtime check, play one small/medium 4.4.5 game without mods.
   - Learn Nomads, Arkships, waylines/contracts, new job/UI/situation behavior, and base-game DLC changes.

2. Light QoL setup:
   - UI Overhaul Dynamic.
   - UIOD Extended Topbar, Improved Font or text submod, Tiny Outliner-style submods, Planet View Performance Mode if needed.
   - Optional: Light Borders, Tech Tiers Revealed, music packs.
   - Goal: mostly UI comfort, low gameplay disruption.

3. Medium Vanilla+ setup:
   - Add Planetary Diversity, Guilli's Planet Modifiers, Real Space, More Events Mod, Dynamic Political Events.
   - Add required UIOD compatibility patches.
   - Start a fresh save, test 20-30 in-game years, then save the playset.

4. Ambitious overhaul setup:
   - Add Gigastructural Engineering, NSC3, Ethics/Civics maintained fork, total conversions, or major shipsets only after the medium setup is stable.
   - Use Irony before launch.
   - Start a new save and expect breakage after game updates.

5. Validation workflow:
   - Subscribe in small batches.
   - Read each mod page's version line, required items, and load order.
   - Use Irony to inspect conflicts rather than blindly resolving every conflict.
   - Disable half the list to isolate crashes if needed.
   - Keep a stable exported/merged playset before major game updates.

## Key Sources

- Steam News: Stellaris 4.4.4 patch released - https://store.steampowered.com/news/app/281990/view/689761349249532145
- Paradox Interactive: Nomads and 4.4 Pegasus launch - https://www.paradoxinteractive.com/media/press-releases/press-release/paradox-interactive-launches-major-expansion-and-free-update-for-stellaris
- Stellaris Wiki patches - https://stellaris.paradoxwikis.com/Patches
- UI Overhaul Dynamic - https://steamcommunity.com/sharedfiles/filedetails/?id=1623423360
- Planetary Diversity - https://steamcommunity.com/sharedfiles/filedetails/?id=819148835
- Gigastructural Engineering & More - https://steamcommunity.com/sharedfiles/filedetails/?id=1121692237
- Guilli's Planet Modifiers and Features - https://steamcommunity.com/sharedfiles/filedetails/?id=865040033
- Real Space 4.0 - https://steamcommunity.com/sharedfiles/filedetails/?id=937289339
- NSC3 - https://steamcommunity.com/sharedfiles/filedetails/?id=683230077
- Irony Mod Manager docs - https://bcssov.github.io/IronyModManager/
- Irony Mod Manager GitHub - https://github.com/bcssov/IronyModManager
- Stellaris Modding Tutorial - https://stellaris.paradoxwikis.com/Modding_tutorial
