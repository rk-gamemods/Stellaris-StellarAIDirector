# Stellar AI Initial Audit - 2026-07-04

## Scope

This note starts a focused research track for `Stellar AI`, installed locally
from Steam Workshop item `3610149307`.

The question for this pass is not whether Stellar AI is "good" in the abstract.
The question is whether it is the right baseline AI layer for a playset with
major late-game power systems such as Gigastructural Engineering, NSC3, ESC
NEXT, starbase/defense mods, and other advanced content.

## Source Facts

Descriptor facts from
`C:\Steam\steamapps\workshop\content\281990\3610149307\descriptor.mod`:

- name: `Stellar AI`
- version: `0.10`
- supported version: `v4.4.4`
- tags: `Gameplay`, `Economy`, `Buildings`, `Fixes`, `Balance`
- remote file id: `3610149307`

Attached/pasted mod description says the mod shifts AI toward a research-focused
playstyle, with early expansion, stable raw resources and consumer goods, at
least one reserved non-capital research world, stronger research acceleration
around year 45, researcher output changed from vanilla 3 to 5 for core
researcher families, and later conversion of research/industry into fleet
power.

Local inventory:

| Area | Count |
| --- | ---: |
| `.vscode` | 1 |
| `common` | 79 |
| `events` | 1 |
| `localisation` | 1 |
| `descriptor.mod` | 1 |
| `thumbnail.png` | 1 |

`common` inventory:

| Area | Count |
| --- | ---: |
| `ai_budget` | 2 |
| `buildings` | 5 |
| `colony_types` | 1 |
| `defines` | 1 |
| `economic_plans` | 4 |
| `inline_scripts` | 57 |
| `on_actions` | 1 |
| `personalities` | 1 |
| `pop_jobs` | 2 |
| `script_values` | 1 |
| `scripted_triggers` | 1 |
| `scripted_variables` | 1 |
| `static_modifiers` | 1 |
| `strategic_resources` | 1 |
| `zones` | 1 |

## Design Reading

Stellar AI is primarily an economy and planet-development AI mod. Its center of
gravity is not combat tactics or direct modded-megastructure selection. The
installed files show these major surfaces:

- economy plans in `common/economic_plans`;
- alloy and mineral spending budgets in `common/ai_budget`;
- building definitions and AI weights in `common/buildings`;
- colony designation logic in `common/colony_types`;
- zone priorities in `common/zones`;
- researcher job output changes in `common/pop_jobs`;
- reusable AI logic in `common/inline_scripts/stellarai`;
- economic readiness and recovery predicates in
  `common/scripted_triggers/stellarai_reactive_triggers.txt`;
- event-driven planet commitment and market stabilization in
  `events/111_stellarai_commitment_events.txt`;
- event hooks in `common/on_actions/stellarai_commitment_on_actions.txt`;
- early expansion personality behavior in `common/personalities/00_personalities.txt`.

This is consistent with the pasted description: the mod is trying to make AI
empires build a coherent research economy instead of receiving hidden bonuses.

## Confirmed Mechanics

### Research Economy

`111_stellarai_basic.txt` defines `basic_economy_plan` with `ai_weight = 900`
and research focus targets for physics, society, and engineering research.

`111_stellarai.txt` defines `advanced_economy_plan` with `ai_weight = 250`,
midgame research income targets, and scaling subplans gated by
`stellarai_foundation_ready`.

`03_endgame.txt` defines `endgame_economy_plan` with `ai_weight = 50`,
baseline endgame income targets of 200 energy, 300 minerals, 300 alloys, 10000
for each research type, 500 unity, and an alloy subplan that pushes 1000 alloys
or 2200 alloys while `stellarai_should_rebuild_fleet = yes`.

`04_beyond_endgame.txt` defines `beyond_endgame_economy_plan` with very high
research targets, 500 alloy baseline, and a fleet rebuild subplan targeting
15000 alloys.

### Researcher Output

The specialist and gestalt job files set the core researcher families to 5
research output:

- `physicist` produces `physics_research = 5`;
- `biologist` produces `society_research = 5`;
- `engineer` produces `engineering_research = 5`;
- gestalt calculator/brain-drone variants also show 5-output research jobs.

This is a player-and-AI balance change, not a hidden AI-only modifier.

### Planet Specialization

`common/colony_types/~stellarai_colony_types.txt` overrides or redefines many
vanilla colony designations, including research, habitat research, ring
research, forge, factory, rural, unity, fortress, and machine/hive variants.

The research designation entries use `stellarai/research_colony_type_potential`.
Other designations use guard scripts such as
`stellarai/invalid_colony_type_potential`, `stellarai/forge_colony_building_modifiers`,
and `stellarai/factory_colony_building_modifiers`.

`common/on_actions/stellarai_commitment_on_actions.txt` hooks building,
district, zone, game-start, yearly, and monthly events into the
`stellarai_commitment` event namespace.

The event file applies flags such as:

- `stellarai_research_plan_claimed`;
- `stellarai_research_commitment_soft`;
- `stellarai_research_commitment_hard`;
- `stellarai_invalid_for_research`;
- `stellarai_invalid_for_research_to_build`.

This is important because later patches should avoid fighting these flags. If
we want AI empires to pursue modded late-game planets or resource chains, we
need to account for this commitment system.

### Building, Zone, And Budget Behavior

The mod replaces or adjusts core vanilla buildings and zones with stronger AI
weights and reusable guard scripts.

Important examples:

- research buildings use `ai_weight_coefficient` variables such as
  `@research_lab_tier1_coefficient`, `@research_lab_tier2_coefficient`, and
  `@research_building_tier*_coefficient`;
- resource and manufacturing buildings use recovery and rare-resource guard
  scripts;
- zones define priority and coefficient values for research, industry, urban,
  rural, strategic resource, and trade uses;
- alloy budgets include vanilla megastructure, waystation, arkship, habitat,
  decision, ship, starbase, colony, army, and upkeep categories;
- mineral budgets cover planets, stations, armies, colonies, ships, deposit
  blockers, and upkeep.

### Vanilla Megastructure Awareness

`common/ai_budget/00_alloys_budget.txt` includes an
`alloys_expenditure_megastructures` category with desired maximum 20000 alloys.
It also has dedicated categories for Nomad waystations, arkships, habitats, and
decision spending. The decision spending checks `tech_mega_engineering` for
ring restoration style behavior.

This means Stellar AI is not blind to vanilla megastructure-scale alloy
spending. It does not by itself prove that the AI will pursue modded
megastructure chains well.

## Modded Late-Game Gap

An exact local search for these terms returned no matches in Stellar AI:

- `giga_`
- `giga`
- `NSC`
- `ESC`
- `ACOT`
- `sentient_metal`
- `negative_mass`
- `iodizium`
- `ehof`
- `katzen`
- `quasi`

Inference: Stellar AI is probably not directly aware of Gigastructural
Engineering, NSC3, ESC NEXT, or ACOT-specific resources and mechanics. It may
still indirectly help those systems by producing stronger research, alloys,
minerals, and strategic resources, but it does not appear to contain dedicated
decision logic for those modded late-game systems.

This matches the suspected failure mode: the AI can be economically better
without being strategically competent at the strongest modded options.

## Patch Risk Map

| Surface | Risk | Why It Matters |
| --- | --- | --- |
| `economic_plans` | Medium | Good place to add late-game resource/income targets, but overlapping plans can distort the entire economy. |
| `ai_budget` | Medium | Essential for megastructure spending, but bad weights can starve fleets, colonies, or recovery. |
| `buildings` | High | Stellar AI rewrites many vanilla building definitions; patching here can conflict with other building/content mods. |
| `colony_types` | High | Central to its specialization system; patches need to preserve commitment flags and invalidation guards. |
| `zones` | High | Core 4.4 planet-development surface; conflicts could affect every planet. |
| `pop_jobs` | Medium-high | Researcher output balance is core to Stellar AI; avoid casual edits unless intentionally changing balance. |
| `events`/`on_actions` | Medium-high | Powerful extension point for state tracking, but bad monthly/yearly logic can hurt performance or create hidden behavior loops. |
| `scripted_triggers`/`inline_scripts` | Medium | Best place for reusable compatibility predicates if kept small and source-backed. |
| `personalities` | Medium | Useful for early expansion and aggression behavior, but likely secondary to the Gigas/late-game gap. |

## Compatibility Hypotheses

These are hypotheses, not conclusions:

1. Stellar AI should remain the baseline broad AI mod for this playset unless a
   direct conflict or poor observer-game result proves otherwise.
2. The first compatibility patch should not rewrite Stellar AI wholesale. It
   should add a separate late-loading patch mod that targets Gigas/NSC/ESC
   integration points.
3. Gigas integration likely needs three kinds of support:
   - resource economy support for Gigas resources such as sentient metal,
     negative mass, and related special resources;
   - technology and prerequisite weighting for critical unlock chains;
   - megastructure `ai_weight` and alloy-budget alignment for high-impact
     structures.
4. NSC3/ESC integration likely needs a separate pass focused on ship classes,
   components, ship design behavior, alloy spending, and technology weights.
5. The observer-game test should measure whether AI empires actually reach and
   use late-game systems, not merely whether files contain plausible weights.

## Next Research Tasks

1. Compare Stellar AI's modified object names against vanilla 4.4.4 to identify
   full-object replacement surfaces and conflict sensitivity.
2. Inventory Gigas resources, techs, megastructures, AI budgets, and economic
   plans, then map them against Stellar AI's available extension points.
3. Identify whether Gigas already contains sufficient `ai_weight` logic for
   high-impact structures and whether Stellar AI's budgets help or interfere.
4. Build a small "AI capability matrix" for each retained major mod:
   - can the AI unlock it?
   - can the AI afford it?
   - does the AI prioritize it?
   - does the AI have economy support for required custom resources?
   - does another mod override the same object?
5. Only after that, draft a separate compatibility patch plan.

## Current Working Conclusion

Stellar AI looks like a serious and coherent economy/research AI mod. It is
probably a good center of gravity for this playset. The visible gap is not
basic competence; it is direct late-game awareness of modded power systems.

The safest path is to keep Stellar AI as the baseline, then build a targeted
compatibility layer around Gigastructural Engineering and other retained
late-game mods.

