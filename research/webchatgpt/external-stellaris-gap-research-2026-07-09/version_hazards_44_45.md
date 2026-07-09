# Stellaris 4.4.x And 4.5 Modding Hazards

## Direct answer

4.4.5 is the current 4.4 stable target. Its patch notes add a Resource Abundance slider and Nomad/Waystation/Arkship fixes that affect economy baselines, automation, and new-game setup [S081]. 4.4 as a branch introduced Nomads/Arkships/Waylines/Contracts and broad gameplay/UI/fleet changes [S082]. 4.5 Cygnus is a separate beta/porting branch: pop groups are no longer divided by ethics/factions, faction/ethic percentages are carried on pop groups, ethics/factions are displayed in planetary management UI, pop ethics/faction conversion changes, and the notes explicitly warn that this is breaking and will not preserve save compatibility [S083][S084].

## 4.4.x hazards

### Resource Abundance slider

4.4.5 adds a Resource Abundance slider [S081]. This changes economic baselines and makes player/AI benchmark comparisons sensitive to galaxy setup. A 4.4.5 game at high resource abundance is not directly comparable to a 4.3/4.4 “scarce” or x1 resource game.

**Modding impact:** AI benchmarks must record galaxy resource setting.

### Nomads, Arkships, Waystations, Waylines, Contracts

4.4 introduced or expanded Nomad-specific mechanics, Arkships, Waystations, Waylines, and Contracts [S082]. 4.4.5 continues fixing these systems [S081].

**Modding impact:** any AI economy, colony, starbase, ship, UI, or event logic touching colonies/capitals/automation must test nomadic and non-nomadic empires separately.

### Launcher/playset behavior

4.4 dev-diary notes say launcher mod lists auto-disable on major update and the launcher bails to main menu when resuming incompatible saves [S085].

**Modding impact:** do not infer active playset state from source files. Check launcher/Irony state before live tests.

### UI hazards

UIOD and UI patches can lag game updates. A 4.4.4 transition report described UIOD diplomacy-screen crashes and beta-plugin mitigation [S053].

**Modding impact:** UI mods require current Workshop status and runtime UI click-through after each game patch.

### Ship design hazards

4.4 NSC3 updates changed fleet caps and ship costs and recommend new saves [S025][S026]. NSC3 also removed Advanced Ship Behaviors and recommends SFT [S027].

**Modding impact:** ship sizes, sections, components, combat computers, global designs, and auto-design behavior must be revalidated after updates.

## 4.5 hazards

| Surface | Why risky in 4.5 | Source |
|---|---|---|
| Pops/pop groups | Pop groups no longer divided by ethics/factions; percentage memberships replace old structure | [S083][S084] |
| Factions/ethics | More frequent shifting/conversion; ethic attraction impacts faction growth | [S083][S084] |
| UI | Planetary management UI now displays faction/ethic data and verbose tooltips | [S083] |
| Species/cyberization | Cyberization policies adjusted and Limited Cybernetic species trait removed in beta notes | [S083] |
| Save compatibility | Explicitly breaking; saves not preserved | [S083][S084] |
| AI economy/jobs | Any pop/job/faction/ethic rewrite changes AI assumptions | [S083][S084] |

## Porting policy

- Keep 4.4.5 as the stable branch for the current stack.
- Do not change descriptors to 4.5 until a separate porting branch exists.
- Diff vanilla 4.4.5 vs 4.5 beta for every touched folder.
- Rebuild CWTools config/generated docs for 4.5.
- Run Irony conflicts on a 4.5-specific playset.
- Test only disposable saves; do not load a live campaign.

## Highest-risk file families

- `common/pop_jobs`, jobs/zones/districts/buildings.
- Species traits, species rights, cybernetic/synthetic/biological ascension surfaces.
- Factions and ethics.
- Leaders/council traits if pop/faction effects are referenced.
- UI planet view, topbar, species/faction/planet-management windows.
- Ship sizes/sections/components/combat computers/global designs.
- AI economy: economic plans, AI budgets, AI weights, colony automation.
- Events/on_actions that assume old pop/faction/species scopes.

## Test checklist before any 4.5 port claim

1. Static source diff against 4.4.5.
2. CWTools diagnostics on every generated and hand-authored file.
3. Irony conflict scan against active 4.5 parent mods.
4. New disposable galaxy with normal empire.
5. New disposable galaxy with Nomad/Arkship empire.
6. Ship designer click-through.
7. Planet management/faction/species UI click-through.
8. Error.log/game.log scan.
9. Observer benchmark only after all static and smoke checks pass.
