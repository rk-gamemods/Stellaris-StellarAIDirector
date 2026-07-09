# Modded Resources And UI Visibility Findings

## Direct answer

Universal Resource Patch and UI Overhaul Dynamic topbar/UI patches are infrastructure for this stack, not cosmetic preferences. URP’s page says it displays added strategic resources from different mods and advises moving it to the bottom if it does not work [S051]. Users report resource visibility problems and bottom-load-order fixes in comments [S052]. UI Overhaul Dynamic expands UI space, including the ship designer for new ship sections/classes [S047]. UIOD+Gigas and UIOD+PD patches provide parent-specific interface fixes and load order [S048][S049]. Extended Topbar for DLCs displays additional crisis/DLC resources on the top toolbar [S050].

## Important modded resources and bottlenecks

### Gigastructural Engineering

External discussion identifies resources such as quasi-negative mass and sentient metal as tied to EHOF/cohesive-star routes and psionic sublimate to Shroud-oriented systems [S013]. Local project context also treats Gigas special-resource chains as first-class constraints. The practical point is not the exact name list; it is that Gigas projects can bottleneck on non-vanilla resources that the AI and tester must see.

**AI rule:** track Gigas special resources separately from alloys and energy. Do not let megastructure budgets consume them during survival/recovery states.

### ESC NEXT

ESC NEXT adds component tiers and likely additional rare-resource pressure through high-tier components [S028]. Exact current resources and component upkeeps must be parsed from active source. The known strategy answer: ESC resource/upkeep needs must be visible before ship-design generation.

### Planetary Diversity / Guilli

PD submods can add districts, jobs, buildings, deposits, and terraforming paths [S056]. Guilli adds hundreds of planetary modifiers and content interacting with them [S057]. These do not always mean new stockpile resources, but they do create hidden valuation inputs: deposits, modifiers, district unlocks, and job output changes.

## What URP solves

URP solves the “added strategic resource display” problem [S051]. Without it, a resource can exist in scripts and economy but be missing or poorly visible in the topbar. That breaks testing because the player cannot see why a megastructure, component, or building is blocked.

## What UIOD and topbar patches solve

- UIOD gives room for expanded ship designer and larger UI [S047].
- UIOD+Gigas fixes Gigas bottom-interface issues and has explicit load order [S048].
- UIOD+PD fixes PD empire creation UI style and has explicit load order [S049].
- Extended Topbar for DLCs displays extra crisis/DLC resources [S050].

## Common resource/UI problems reported

| Symptom | Likely cause | Evidence | Fix |
|---|---|---|---|
| Strategic resource missing from topbar | URP not loaded late enough or resource unsupported | [S051][S052] | Move URP lower/bottom, verify supported-resource list, patch resource icon/UI. |
| Gigas UI bottom/menu broken | Missing UIOD+Gigas patch | [S048] | Load Gigas -> UIOD -> UIOD+Gigas. |
| PD empire creation UI misaligned | Missing UIOD+PD patch | [S049] | Load PD -> UIOD -> UIOD+PD. |
| New NSC ship sections cramped/invisible | Vanilla ship designer too small or UI conflict | [S047] | Use UIOD, then verify designer after all patches. |
| UI crashes after game patch | Transient UIOD update lag | [S053] | Check current Workshop comments/changelog; use beta plugin only if current page says so. |

## Load-order decision for this stack

Follow explicit page instructions first. Based on public sources:

1. Parent gameplay mods: Gigas, PD, NSC3, ESC NEXT, Starbase Extended.
2. UIOD after parent UI-affecting mods when instructed.
3. UIOD compatibility patches after both parents.
4. URP low/bottom enough that custom resource display works, while avoiding overwriting final UIOD layout if a specific UI patch says otherwise.
5. Use Irony to resolve exact element conflicts rather than a generic rule [S074][S076].

## AI Director resource policy

- Every route consuming a modded resource must expose stockpile, income, and deficit/runway checks.
- Every special resource should have a “do not spend while survival/recovery” guard.
- Resource visibility must be tested before observer runs; otherwise metrics will miss bottlenecks.
- Missing-resource comments are data: add unsupported active-stack resources to a local topbar/resource patch only after source proof.
