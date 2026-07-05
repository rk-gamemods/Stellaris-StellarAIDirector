# Stellaris Web ChatGPT Packet Reconciliation

Date checked: 2026-07-04

Local baseline report: `research/stellaris-30-day-research-2026-07-04.md`

Web ChatGPT packet: `C:\Users\Admin\Downloads\stellaris_research_packet_2026-07-04.zip`

Packet SHA-256: `C5147EA8017FF187311E75298F67EDD24DDDF9789CE79CE113D311C47ACE4D50`

Extracted packet folder: `research/webchatgpt/stellaris_research_packet_2026-07-04/`

## Method

Treat the Web ChatGPT packet as source-discovery and synthesis context, not as a canonical source by itself. Promote claims only when they align with stronger sources such as official Paradox notes, Steam Workshop pages, GitHub releases, tool documentation, or the previously saved `last30days` artifacts.

The packet source inventory is heavily Steam-centered: 31 Steam Workshop mod pages, 5 Steam Workshop collections, 3 GitHub repositories, 2 GitHub releases, 2 press reviews, official Paradox/Steam news, Valve SteamCMD docs, CWTools pages, and a Reddit/community bug report.

## Overall Reconciliation

The packet mostly confirms the local `last30days` report:

- Live baseline remains Stellaris 4.4.4 "Pegasus" checksum 5505, released 2026-06-24.
- 4.4.5 "Pegasus" is an opt-in beta/testing branch, not the default modding target.
- Nomads and 4.4 are the key current compatibility disruptors because Arkships, Waystations, colony-vs-planet logic, logistics, UI, and scripted modifiers changed.
- UI Overhaul Dynamic is still the safest UI foundation, with current-version caveats.
- Big content and system mods should be staged into new saves rather than added casually to an ongoing campaign.
- Irony Mod Manager remains the leading current conflict-aware mod manager.

The packet adds useful resolution in four areas: AI/performance mods, total conversions, UI/outliner compatibility, and AI-friendly tooling.

## New Or Sharper Findings

### AI and performance mods

The packet adds a clearer AI path than the local baseline:

- `Stellar AI` is the current AI overhaul candidate for 4.4.4 because it was rebuilt around 4.4/Nomads logic and explicitly warns against combining AI overhauls.
- `AI Game Performance Optimisation 4.4` is a plausible performance-focused second-stage add, but it changes AI behavior and galaxy systems, so it is not "pure QoL."
- `StarNet AI` and `StarTech AI` should be avoided on live 4.4.4 for now because their Workshop pages are stale relative to Pegasus.

Decision impact: add either `Stellar AI` or `AI Game Performance Optimisation 4.4` only after the vanilla/QoL setup is stable. Do not stack AI overhauls.

### UI and outliner choice

The packet clarifies the Tiny Outliner fork split:

- Use `UI Overhaul Dynamic` plus `UI Overhaul Dynamic - Tiny Outliner` if using UIOD.
- Use `Full Tiny Outliner` only if not using UIOD.
- Do not mix UIOD with Full Tiny Outliner.
- Do not use `UI Overhaul Dynamic Beta` on live 4.4.4; it targets the 4.4.5 beta branch.

Decision impact: the default UI set should be UIOD plus its own Tiny Outliner submod, not a generic Tiny Outliner stack.

### Total conversions

The packet adds a useful live-version split:

- `Star Trek: New Civilisations` appears to be the current live-compatible total conversion candidate, with a 4.4.4-compatible STNC-2607 update.
- `Star Trek: New Horizons`, `Star Wars: Legacy of the Old Republic`, and `Star Wars: New Dawn` are currently 4.3.7-targeted or otherwise not live-4.4.4 ready.

Decision impact: treat total conversions as isolated playsets. If trying one soon, pick STNC, not STNH or the Star Wars conversions, unless rolling back Stellaris.

### Visual and battle mods

The packet improves the optional visual tier:

- `Immersive Galaxy and Skybox` looks like a better current skybox candidate than `Beautiful Universe v2.0`.
- `Beautiful Universe v2.0` should be watchlisted because the packet found possible crash/UIOD concern signals.
- `Amazing Space Battles` is current and interesting, but it changes battle spacing, targeting, explosions, duration, and possibly performance, so it is not merely cosmetic.

Decision impact: keep visual mods optional and test after core UI/content mods.

### Tooling

The packet adds the most value in tooling:

- `SteamCMD` is useful for AI-assisted Workshop downloading by app/workshop ID, but it does not understand Stellaris conflicts.
- `CWTools` and `CWTools.CLI`/`cwtools-action` are important for PDXScript validation and are much more AI-friendly than GUI-only tools.
- `Irony Mod Manager` remains best for conflict/load-order analysis, but its CLI/structured-output surface is limited.
- A small custom Codex/Python audit adapter would fill the gap between Steam subscriptions, launcher playsets, Irony conflict state, Workshop freshness, descriptor metadata, file-overwrite inventory, and CWTools validation.

Decision impact: use Irony for human conflict review, SteamCMD for deterministic acquisition if needed, CWTools for validation, and consider a custom adapter only after we know the exact playset workflow.

## Conflicts Or Corrections

### Irony Mod Manager latest release

The packet's tool matrix says Irony latest is `v1.27.189` released 2026-06-19. This is stale. GitHub Releases show `v1.27.191` released 2026-06-30, and the repository page lists `v1.27.191 Latest Jun 30, 2026`.

Resolution: use GitHub Releases as source of truth. The packet is still correct that Irony is active and current.

### UIOD crash risk

The local baseline treated UIOD as safe default. The packet adds a July 3 Reddit crash report involving diplomacy-screen crashes on 4.4.4, with comments suggesting beta UIOD until the main mod updated.

Resolution: this is a transient watch item, not a reversal. UIOD still belongs in the safe default, but test it immediately after subscribing and make sure the live UIOD page has the latest July 3 update. Do not use the beta UIOD plugin on stable unless deliberately testing 4.4.5.

### Real Space exact version confidence

The local baseline treated Real Space as medium-confidence/current-ish. The packet sharpens this: Real Space 4.0 appeared to claim 4.4.3 rather than explicit 4.4.4, and Real Space System Scale has known interaction risks with Gigastructural Engineering.

Resolution: Real Space stays in the medium/ambitious tier, not the safe default. Avoid scale-sensitive Gigas combinations unless a current compatibility patch is verified.

### Dynamic Political Events freshness

The local baseline included Dynamic Political Events as a medium Vanilla+ option. The packet notes it was not updated in the last 30 days.

Resolution: keep DPE as a later medium-confidence mod, not part of the first "current and safest" list.

### Light Borders

The local baseline had Light Borders as optional from community discussion. The packet distinguishes the stale original from a newer fork.

Resolution: avoid the original Light Borders + Star Pins. Only test the newer `Light Borders + Swapped Colors + Star Pins [4.0+]` fork, and treat it as optional because explicit 4.4.4 support was not established.

### Collections

The packet lists helpful collections, including `Stellaris - Essentials for Pegasus 4.4.1`, UIOD submod and compatibility collections, Planetary Diversity collections, Real Space full pack, Gigas submods, NSC companion mods, Amazing Space Battles Collection, STNH collection, and Renegades Modding Group.

Resolution: use collections for source discovery and load-order clues, not as executable truth. The 4.4.1 collection is behind current 4.4.4, and total-conversion collections must match their target game version.

## Updated Practical Recommendation

First launch:

- Stable 4.4.4 vanilla, no mods.
- One short settled-empire reacclimation save.
- One separate Nomad test if using the DLC.

Light QoL:

- UI Overhaul Dynamic.
- UI Overhaul Dynamic - Tiny Outliner.
- UIOD compatibility patches only where explicitly required.

First content tier:

- Guilli's Planet Modifiers and Features.
- More Events Mod.
- Planetary Diversity.

Second test tier:

- AI Game Performance Optimisation 4.4, conservatively configured, or Stellar AI, but not both as AI overhauls.
- Amazing Space Battles if battle pacing changes are acceptable.
- Immersive Galaxy and Skybox if visual-only tests pass.
- Dynamic Political Events as a later medium-confidence addition.

Ambitious/new-save tier:

- Gigastructural Engineering.
- NSC3.
- Extra Ship Components NEXT, loaded before NSC3 if combined.
- Real Space, with caution around scale modules and Gigas.
- DarkSpace.

Total conversion tier:

- Star Trek: New Civilisations on live 4.4.4 as an isolated playset.
- STNH and Star Wars conversions only after their pages update for live 4.4.4 or if intentionally rolling back.

## Evidence Limits

The packet is valuable but should not be treated as final install truth. Before subscribing or building a playset, re-open the exact Workshop pages because Workshop update timestamps, comments, dependencies, and required patches can change quickly after a major Stellaris release.

The prior local `last30days` run did not have TikTok/Instagram coverage. It did return X-like items despite diagnosis not listing X as active, so social coverage remains mixed. The Web ChatGPT packet is stronger for Steam Workshop and tooling source discovery than for broad social sentiment.
