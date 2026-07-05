# Stellar AI Modded Progression Theorycraft - 2026-07-04

## Scope

This is a whiteboard analysis, not a playtest result.

The goal is to map how `Stellar AI` currently improves the default game AI, then
identify a small and coherent way to make it scale better with the current
late-game mod environment:

- `Stellar AI` as the economy and research AI baseline.
- `Gigastructural Engineering & More (4.4)` as the main megastructure and
  superproject layer.
- `NSC3` as the expanded hull and fleet progression layer.
- `Extra Ship Components NEXT` as the advanced component and late research
  layer.
- `Starbase Extended` as the static defense layer.

The target is not to make every AI empire pursue every powerful toy. The target
is to give the AI a sane progression spine so it can keep scaling into modded
midgame and endgame instead of stopping at vanilla endgame behavior.

## Source Set

Local source snapshot:

`research/mod-source-snapshots/2026-07-04`

Relevant copied mod roots:

| Mod | Snapshot Folder | Notes |
| --- | --- | --- |
| Stellar AI | `3610149307-stellar-ai` | Version `0.10`, supported Stellaris `v4.4.4`. |
| Gigastructural Engineering | `1121692237-gigastructural-engineering-more-44` | Adds megastructures, special resources, ascension perks, events, and crises. |
| NSC3 | `683230077-nsc3` | Adds ship sizes, sections, components, technologies, starbase content. |
| Extra Ship Components NEXT | `2648658105-extra-ship-components-next` | Adds large late-game component and tech trees. |
| Starbase Extended | `3250900527-starbase-extended-30` | Adds starbase modules, buildings, levels, and defense-related ship sizes. |

The supporting inventory dataset for this pass was generated from the copied
source snapshot. It is useful for finding AI surfaces, but the analysis below
is grounded in the copied files rather than playtest behavior.

## Current Stellar AI Logic Map

Stellar AI is mostly an economic planning, planet specialization, and research
acceleration mod. It is not primarily a direct Gigas/NSC/ESC compatibility mod.

### 1. Economy Plan Ladder

Stellar AI defines a clear economy-plan ladder:

| Layer | File | Purpose |
| --- | --- | --- |
| Basic economy | `common/economic_plans/111_stellarai_basic.txt` | Early economy, early research targets, fleet rebuild, vanilla strategic resource recovery. |
| Advanced economy | `common/economic_plans/111_stellarai.txt` | Midgame research scaling, higher fleet rebuild, stronger foundation requirements. |
| Endgame economy | `common/economic_plans/03_endgame.txt` | Huge vanilla endgame research targets and alloy targets. |
| Beyond endgame economy | `common/economic_plans/04_beyond_endgame.txt` | Very high research targets, very high fleet rebuild alloy target, naval cap push. |

Important current behavior:

- Basic economy starts with very high plan weight and pushes physics, society,
  and engineering research from the beginning.
- Advanced economy continues the same research-first posture once the empire is
  stable enough.
- Endgame sets each research type to `10000`.
- Beyond endgame sets each research type to `50000`.
- Fleet rebuild subplans increase alloy pressure sharply when the AI should
  rebuild its navy.
- Vanilla strategic resource recovery exists for motes, gases, and crystals.

Interpretation:

Stellar AI already tries to keep the AI from stagnating at normal vanilla
research levels. That is good for a modded playset. The gap is that these
targets are broad. They do not by themselves say "finish the Gigas megastructure
unlock spine", "feed ESC dark matter/nanite/zro components", or "modernize into
NSC3 heavy hulls".

### 2. Readiness And Recovery State Machine

The main reusable readiness logic is in:

`common/scripted_triggers/stellarai_reactive_triggers.txt`

Current trigger roles:

| Trigger | Role |
| --- | --- |
| `stellarai_military_emergency` | Detects dangerous military pressure and war state. |
| `stellarai_economic_crisis` | Detects deficit or low stockpile states. |
| `stellarai_foundation_ready` | Requires no major crisis, stable energy/minerals, and minimum stockpiles. |
| `stellarai_research_ready` | Requires later date, no crisis, stronger income, and stronger stockpiles. |
| `stellarai_should_rebuild_fleet` | Decides when alloy pressure should move toward ships. |
| `stellarai_country_unity_push` | Pushes unity early enough to reach ascension perks. |
| `stellarai_good_research_candidate` | Finds good research planets. |
| `stellarai_research_claim_candidate` | Controls which planets can be claimed for research specialization. |

Interpretation:

This is the right place to add a modded progression state layer later. The
existing logic already thinks in terms of "stable enough", "research ready", and
"rebuild fleet now". A compatibility patch should extend that vocabulary rather
than invent a separate hidden AI.

### 3. Planet Commitment Layer

The commitment system is event-driven:

`events/111_stellarai_commitment_events.txt`

It periodically tags planets with flags such as:

- `stellarai_invalid_for_research`
- `stellarai_research_plan_claimed`
- `stellarai_research_commitment_soft`
- `stellarai_research_commitment_hard`
- `stellarai_industry_commitment_soft`
- `stellarai_industry_commitment_hard`
- `stellarai_rural_commitment_soft`
- `stellarai_trade_commitment_soft`

Research world selection is capped by colony count and date. For example, after
year 45, more planets can be claimed as research worlds as the empire grows.

Interpretation:

This is useful for modded AI because it means Stellar AI already creates
specialized research capacity instead of relying only on generic building
weights. We should avoid breaking this. If a future patch needs special Gigas or
ESC worlds, it should cooperate with these flags instead of fighting them.

### 4. Budget Layer

The key budget files are:

- `common/ai_budget/00_alloys_budget.txt`
- `common/ai_budget/00_minerals_budget.txt`

Important current alloy behavior:

- `alloys_expenditure_ships` gets much stronger when
  `stellarai_should_rebuild_fleet = yes`.
- The ship budget reduces pressure when over naval cap or in some recovery
  states.
- `alloys_expenditure_megastructures` exists and is gated by
  `can_build_megastructures`.
- The generic megastructure alloy budget has a base desired max of `20000`.
- The megastructure budget increases if naval capacity is healthy and an owned
  megastructure can be upgraded.

Interpretation:

Stellar AI is not blind to megastructure spending. But `20000` is probably a
vanilla-scale cap, not a robust Gigas superproject reserve. If a Gigas stage or
chain needs higher staged reserves, the AI may keep spending itself down before
it can complete the highest-impact projects.

### 5. Personality Layer

Stellar AI also touches personalities:

`common/personalities/00_personalities.txt`

The visible role is broad AI behavior tuning such as expansion, aggression,
bravery, and military spending. Personality can be used later as a decision
filter, but it should not be the first patch surface.

Interpretation:

Personality is a good late tuning layer. The first progression patch should
start with economy, readiness, research, and budget logic.

## AI Surface Separation

The short answer is: yes, Stellaris mod AI is split across different surfaces,
and we can tune many of them separately. But they are not fully isolated.

Useful separate levers:

| Surface | What It Can Influence |
| --- | --- |
| `common/personalities` | Broad diplomatic, military, aggression, bravery, expansion, and behavior style. |
| `common/economic_plans` | Desired income targets and economic growth direction. |
| `common/ai_budget` | How resources get divided between ships, starbases, colonies, megastructures, decisions, upkeep, and other buckets. |
| Object-local `ai_weight` blocks | Whether the AI prefers specific techs, buildings, modules, components, ships, megastructures, or perks. |
| `common/scripted_triggers` and `common/script_values` | Shared state checks and scoring logic that other files can reuse. |
| `events` and `on_actions` | Periodic state tracking, flags, claims, recovery behavior, and complex multi-step logic. |
| `common/colony_types`, buildings, zones, and jobs | Planet specialization and build behavior. |

The important caution:

```text
Separate files do not mean separate consequences.

Economy plan changes can starve war.
War budget changes can delay megastructures.
Megastructure saving can delay fleet upgrades.
Starbase spending can protect the empire or waste alloys.
Tech weights do nothing if the economy cannot exploit the unlock.
Personality changes can make the same budget rules behave differently.
Full-object overwrites from multiple mods can replace each other by load order.
```

So the correct architecture is a single compatibility layer that owns the
integration policy, while keeping the actual patch files separated by game AI
surface. One mod can contain separate files for economy, budget, tech, perks,
starbases, and scripted triggers. That gives us one place to reason about the
strategy without forcing every rule into one giant file.

## Current Mod AI Surfaces

The other major mods are not empty from an AI perspective. They contain many
local AI weights and support files. The problem is coordination.

### Gigastructural Engineering

Observed AI-relevant surfaces:

- `common/ai_budget`
- `common/economic_plans`
- `common/megastructures`
- `common/technology`
- `common/ascension_perks`
- `common/strategic_resources`
- events and scripted logic

Important findings:

- Gigas defines budgets for special resources such as negative mass and sentient
  metal.
- Gigas defines an additive economic plan that targets special resources after
  relevant techs are unlocked.
- Gigas adds strong ascension-perk AI weight for vanilla megastructure-related
  perks such as Galactic Wonders and Master Builders.
- `ap_gigastructural_constructs` has a very high AI weight.
- Some very large or exotic Gigas branches are deliberately disabled for AI by
  `ai_weight = 0`, including examples like QSO, Vast Expanses, Celestial
  Printing, and Supermassive EHOF.
- Gigas contains many megastructure-local `ai_weight` definitions.

Interpretation:

Gigas already does a lot of local AI work. The missing piece is probably not
"list every Gigas object as available". The missing piece is a central
progression policy that defines when it is safe and desirable to move from
vanilla megastructures into Gigas-scale projects, and how much economy reserve
it should maintain while doing so.

### NSC3

Observed AI-relevant surfaces:

- ship sizes
- section templates
- component templates
- technologies
- starbase content
- some events and local weights

Important findings:

- NSC3 includes AI weights on ship sizes, sections, components, and technology.
- It extends the vanilla hull ladder with larger and more specialized ships.
- It overwrites or extends important hull tech chains such as battleship and
  titan progression.

Interpretation:

The main coordination issue is probably not local ship component selection. The
main issue is making sure the AI researches the hull unlock chain, has the alloy
economy to build larger hulls, and does not spend every alloy on megastructures
when it is militarily exposed.

### Extra Ship Components NEXT

Observed AI-relevant surfaces:

- many component templates with `ai_weight`
- many late-game technologies
- special-resource usage and production hooks
- advanced reactors, drives, sensors, weapons, combat computers, and auras

Important findings:

- ESC has a large late-game tech tree with many local AI weights.
- ESC creates demand for resources such as rare crystals, zro, dark matter, and
  nanites depending on which component branches are unlocked.
- The tech set continues beyond vanilla-tier expectations.

Interpretation:

Stellar AI's huge generic research targets help here, but the AI can still drift
if critical ESC unlock chains are not weighted strongly enough or if the economy
does not produce the resources required by the components it unlocks.

### Starbase Extended

Observed AI-relevant surfaces:

- starbase buildings
- starbase modules
- starbase levels
- defense-related ship sizes
- local AI weights

Interpretation:

This should be handled as a defensive specialization layer, not as a global
economy priority. The AI should invest harder into expanded starbases when it is
defensive, threatened, guarding chokepoints, or protecting critical
megastructure systems.

## Current Gap

The current setup looks fragmented:

```text
Current separate AI islands:

Stellar AI
  -> research economy
  -> planet specialization
  -> alloy and mineral budgets

Gigastructural Engineering
  -> megastructure weights
  -> special resource budgets
  -> Gigas ascension perks

NSC3
  -> hull, section, and component weights

Extra Ship Components NEXT
  -> late component tech weights

Starbase Extended
  -> starbase module and building weights
```

What appears to be missing:

```text
Missing shared progression spine:

stable economy
  -> sustained modded research
  -> ascension perk strategy
  -> megastructure unlock spine
  -> special resource production
  -> NSC3/ESC fleet modernization
  -> protected critical systems
  -> optional superprojects
```

The mods have many local weights, but there is no obvious shared late-game
decision tree that asks:

- Is the empire stable enough to start a megastructure push?
- Is it under military pressure and therefore should delay a superproject?
- Does it have the research output to keep climbing modded tech chains?
- Does it need Gigas resources before it can build or upgrade the next project?
- Does it need ESC resources before its ship designs become affordable?
- Should this personality pursue defensive starbase scaling, giant ships,
  megastructure economy, or exotic Gigas superprojects?

## Lumpy Investment Problem

Stellar AI currently looks optimized for smooth, fast growth. That makes sense
for vanilla. It is not enough for a modded Gigas environment.

The strategic problem is that many high-end megastructures and gigastructures
are not smooth upgrades. They are lumpy investments:

```text
Before project:
  normal income
  normal ship production
  normal starbase defense
  normal research scaling

During project:
  large alloy and special-resource drain
  possibly weaker fleet spending for several years
  delayed gratification
  real survival risk if neighbors attack

After project completes:
  economy/research/shipyard capacity can jump by an order of magnitude
  the empire can afford fleets or projects that were impossible before
  the bottleneck changes from "can I afford this?" to "can I spend this fast
  enough?"
```

That means the AI needs a return-on-investment model, not only a deficit
avoidance model. A temporary deficit or low stockpile can be correct if it buys
a project that multiplies the empire's economy, research, naval production, or
defensive leverage.

This should not mean reckless spending. It should mean the AI can identify a
high-payoff project, reserve resources for it, stay alive while building it, and
then immediately shift into a post-completion spending plan.

### Investment Curve To Model

For each major project, the compatibility layer should estimate:

| Field | Meaning |
| --- | --- |
| Up-front cost | Alloys, influence, unity, special resources, build time, required construction asset. |
| Opportunity cost | Ships, starbases, colonies, and other megastructures delayed while saving/building. |
| Survival risk | Whether the empire can afford to be weaker during the build window. |
| Payoff type | Economy, research, ship production, fleet power, defense, special resources, or crisis response. |
| Payoff magnitude | Rough projected change to income, research, naval output, or defensive leverage. |
| Time to payoff | Years until the completed stage starts paying back. |
| Follow-through need | What the AI must do after completion to exploit the payoff. |

The last field matters a lot. A mega shipyard is only part of the answer. If it
multiplies ship production capacity, the AI also needs the alloy income,
strategic resources, naval cap, ship design tech, and upgrade budget to use that
capacity. Otherwise it built a powerful machine and left it idle.

### New Strategic Modes

The AI should be able to leave smooth-growth mode when a high-payoff branch is
available:

| Mode | Purpose |
| --- | --- |
| Smooth growth | Default Stellar AI behavior: stabilize economy, research hard, build normally. |
| Investment preparation | Push prerequisites, stockpiles, and defenses for a selected project. |
| Investment commitment | Reserve resources and tolerate temporary weakness while building the project. |
| Survival hold | Stop or delay the project if war/crisis risk is too high. |
| Payoff exploitation | Spend the new economic/shipyard/research capacity aggressively after completion. |
| Next bottleneck search | Identify whether the new limit is alloys, naval cap, shipyards, special resources, or tech. |

This is the core reason a player can fall behind early and still become
untouchable later. The player is not merely growing faster; the player is
choosing a project that changes the slope of the entire empire.

## Desired Core Progression Spine

The simplest useful improvement is a small compatibility mod that loads after
Stellar AI and the major content mods. It should not physically merge all AI
logic into one giant replacement file. It should add a progression layer that
coordinates the existing local AI systems.

Suggested future mod:

`mods/StellarAIModdedProgression/`

Working principle:

- Leave Stellar AI as the broad economy/research baseline.
- Leave Gigas, NSC3, ESC, and Starbase Extended local weights in place unless
  they are proven wrong.
- Add small shared triggers and additive economy/budget nudges.
- Only overwrite high-risk objects when a specific conflict or missing AI path
  is proven.

### Proposed State Triggers

Add a small set of scripted triggers or script values:

| Proposed Trigger | Meaning |
| --- | --- |
| `sai_modded_economy_stable` | Foundation is ready, no crisis, positive energy/minerals/alloys, stockpiles safe. |
| `sai_modded_research_spine_ready` | Research economy is strong enough to pursue modded tech chains. |
| `sai_modded_mega_spine_ready` | Mega-Engineering or equivalent prereqs are unlocked and the empire can reserve alloys. |
| `sai_modded_special_resource_ready` | Required Gigas or ESC special-resource production exists or can be started. |
| `sai_modded_navy_modernization_ready` | Large hull or advanced component techs are available and economy can support upgrades. |
| `sai_modded_superproject_ready` | Economy, naval safety, ascension state, and resource reserves justify a major Gigas project. |
| `sai_modded_rival_pressure` | Nearby rivals, federation enemies, crisis actors, or war state should override peaceful build plans. |
| `sai_modded_investment_window_open` | The empire is safe enough to commit to a temporary economic dip for a high-payoff project. |
| `sai_modded_payoff_exploitation_ready` | A major project has completed and the empire should spend into its new bottleneck. |

These should mostly wrap existing Stellar AI readiness triggers. That keeps the
patch aligned with the mod's current design.

### Proposed Economy Extensions

Add one or more additive economic plan sections rather than replacing Stellar
AI's whole plan ladder.

Potential subplans:

| Subplan | Gate | Target |
| --- | --- | --- |
| Modded research continuation | Stable economy plus late-game mod techs available | Keep pushing physics/society/engineering beyond vanilla repeatables. |
| Mega-Engineering preparation | Before/after `tech_mega_engineering` | More engineering research, alloys, unity, and influence reserve. |
| Gigas special resource bootstrap | Relevant Gigas tech unlocked | Produce sentient metal, negative mass, supertensiles, iodizium, or other required resources. |
| ESC component resource bootstrap | ESC tech/resource need exists | Produce rare crystals, zro, dark matter, nanites, and other component resources only when useful. |
| NSC3 heavy hull buildout | Larger hull tech unlocked and not in economic crisis | Raise alloys and naval cap target. |
| Superproject reserve | Mega spine ready and not under military emergency | Reserve enough alloys/special resources for high-value megastructure stages. |
| Payoff exploitation | Major project completed | Spend the new surplus into ships, starbases, upgrades, research, or the next bottleneck. |

The important design point is conditionality. The AI should not produce every
modded resource forever just because the mod is installed.

### Proposed Research Strategy

Do not solve research by blindly multiplying every modded tech weight. That
often creates nonsense behavior.

Prefer critical-chain support:

| Chain | Reason |
| --- | --- |
| Mega-Engineering and vanilla megastructure prereqs | Opens the transition from normal empire scaling to large-scale infrastructure. |
| Galactic Wonders and Master Builders support | Gigas already pushes these; verify the chain remains coherent. |
| Gigastructural Constructs | Core Gigas ascension route already has high AI weight and should remain central. |
| Gigas resource unlocks | The AI needs the resources before it can exploit advanced structures and components. |
| Gigas core megastructure unlocks | Focus on economy, research, alloy, and strategic power structures before exotic branches. |
| NSC3 hull unlocks | Larger ships only matter if the AI researches and can afford them. |
| ESC reactor, sensor, drive, computer, and weapon tiers | These make advanced hulls actually scale in combat power. |

Patch style:

- Add research options where the mod itself already does this for AI and we can
  mirror the pattern safely.
- Increase weights only for bottleneck techs that unlock whole progression
  branches.
- Tie tech pressure to empire state and personality rather than making every AI
  identical.

### Proposed Ascension Strategy

Current Gigas behavior appears to strongly support:

- `ap_galactic_wonders`
- `ap_master_builders`
- `ap_gigastructural_constructs`

Those should likely remain the mainline path.

Potential controlled additions:

| Gigas AP Branch | Current Concern | Possible Patch Direction |
| --- | --- | --- |
| QSO | AI weight appears disabled. | Only enable for very strong, safe, late empires with required economy and no severe threat. |
| Vast Expanses / Birch-style branch | AI weight appears disabled. | Enable only for high-research, high-alloy, expansionist or megastructure-focused personalities. |
| Celestial Printing | AI weight appears disabled. | Enable only if the empire has the required economy and strategic reason. |
| Supermassive EHOF | AI weight appears disabled. | Treat as a specialized path, not a default AI goal. |

The safest first pass is not to enable all exotic branches. It is to make sure
the mainline Gigas path works, then selectively allow one or two advanced paths
with strong gates.

### Proposed Megastructure Strategy

The AI should probably use a tiered megastructure preference model that ranks
projects by strategic payoff, not only by immediate affordability:

| Priority | Megastructure Type | AI Logic |
| --- | --- | --- |
| 1 | Economy stabilizers | Build if economy is stable and project gives broad resource/research scaling. |
| 2 | Research scaling | Build if research spine is ready and fleet safety is acceptable. |
| 3 | Alloy and strategic resource scaling | Build if future ship/megastructure needs are blocked by production. |
| 4 | Defensive or chokepoint structures | Build if threatened or protecting critical systems. |
| 5 | Crisis-response structures | Build when crisis flags, enemy pressure, or survival triggers apply. |
| 6 | Exotic superprojects | Build only when economy, navy, and prerequisites are already strong. |

Budget issue to investigate before patching:

- Stellar AI's generic alloy megastructure desired max is `20000`.
- Gigas special-resource megastructure budgets also appear to use vanilla-like
  reserve assumptions.
- Exact stage costs need to be parsed before changing these caps.

Probable patch direction:

- Keep vanilla megastructure spending intact.
- Add higher reserve caps only under `sai_modded_superproject_ready` or
  `sai_modded_investment_window_open`.
- Add a military override so the AI does not save for a superproject while it
  is losing a war or far below naval cap.
- Add a post-completion mode so the AI uses the new capacity instead of simply
  returning to smooth growth.

### Proposed Fleet Strategy

NSC3 and ESC likely already contain many local design weights, so the first
patch should support the economy around them:

| Need | Patch Direction |
| --- | --- |
| Larger hulls | Ensure battleship, titan, dreadnought, and related NSC3 chains keep research priority. |
| Advanced components | Ensure ESC critical component chains are not treated as optional filler forever. |
| Expensive refits | Reserve alloys and special resources for ship upgrades after major unlocks. |
| Naval cap | Use Stellar AI's beyond-endgame naval cap push earlier when heavy hulls are unlocked and economy is stable. |
| War pressure | Let military emergency override peaceful megastructure saving. |

The AI should not always build the biggest possible ship. It should build bigger
ships when it has the economy, tech, naval cap, and threat environment to use
them.

### Proposed Starbase Strategy

Starbase Extended should be integrated as a defensive pressure layer:

The important distinction is that a defensive fleet and a defensive starbase do
not have the same economic meaning:

- A defensive fleet is flexible, but it has ongoing upkeep and produces no
  return unless it deters war, wins a war, or supports conquest.
- A chokepoint starbase is static, but once placed correctly it can reduce the
  fleet size needed for survival across the whole empire.
- An aggressive empire can justify a larger fleet because the fleet can acquire
  territory, subjects, claims, and resources.
- A defensive empire should lean harder on static defenses, chokepoints, and
  protected economic systems so it is not paying for an oversized idle fleet.

Suggested gates:

| Gate | Behavior |
| --- | --- |
| Defensive personality | More starbase investment at borders and chokepoints. |
| Rival or crisis pressure | Upgrade defensive starbases earlier. |
| Critical megastructure system | Prioritize defenses around major economic or superproject systems. |
| Chokepoint value | Prefer systems that block access to multiple colonies, megastructures, or core sectors. |
| Aggressive personality | Prefer fleet spending unless the starbase protects offensive staging or a core bottleneck. |
| Peaceful wide economy | Do not overspend on starbases everywhere. |

This keeps static defense useful without letting it consume the entire alloy
economy.

### Proposed Tradition And Planet-Capacity Strategy

The current pass did not prove whether the active playset expands tradition
slots, tradition trees, planet construction capacity, district capacity, or
building slots. Those need to be included in the next inventory pass.

If the playset adds more traditions or lets empires complete more trees, then
the AI needs a tradition strategy that continues beyond vanilla assumptions:

- early survival and expansion traditions;
- research and unity acceleration;
- megastructure and construction-speed support;
- defensive or military specialization;
- late-game economic scaling.

If the playset expands planet construction capacity, the AI also needs to know
that planets can keep scaling instead of assuming the old saturation point:

- more building slots means more labs, unity, refineries, fortresses, or
  special-resource infrastructure;
- more districts or zones means old colony commitment rules may stop too early;
- more orbital or planetary construction means the AI needs stronger build
  priorities after the first normal planet plan is complete.

This should be handled as an optional capability scan. The compatibility patch
should detect whether those mods are present before changing tradition or planet
growth behavior.

## Minimal Patch Roadmap

### Phase 0 - Completed Baseline Map

Current result:

- Stellar AI is a research/economy spine.
- Gigas has extensive local AI support but not necessarily a global strategy
  bridge into Stellar AI.
- NSC3 and ESC have local component/hull/tech weights, but still need economy
  and research-chain support.
- Starbase Extended should be threat/personality gated.

### Phase 1 - Critical Unlock Chain Matrix

Build a source-backed matrix:

| Object Type | Needed Fields |
| --- | --- |
| Technology | key, prerequisites, tier, area, mod, unlocks, existing AI weight, bottleneck score, unlock-chain role. |
| Ascension perk | key, requirements, current AI weight, unlocks, branch role, strategy role. |
| Megastructure | key, build/upgrade costs, prerequisites, AI weight, role, stage count, payoff type, payoff magnitude, time to payoff. |
| Strategic resource | key, production sources, consumers, AI production hooks. |
| Ship size/component | key, tech prerequisite, resource cost, AI weight, combat role, post-megastructure spend role. |
| Starbase item | key, cost, defense value, chokepoint role, critical-system defense role. |
| Tradition/perk tree | key, slot assumptions, AI weight, strategy role, mod dependency. |
| Planet capacity expansion | source mod, added slots/districts/zones, AI build implications. |

This should be generated with a deterministic local script, not manually
maintained.

### Phase 2 - Additive Progression Patch

Create a small compatibility patch with:

- scripted triggers for modded readiness states;
- additive economic plan sections;
- conservative alloy and special-resource reserve logic;
- investment-window and payoff-exploitation states;
- no broad replacement of Stellar AI planet or building logic.

### Phase 3 - Research And Ascension Tuning

Patch only critical bottlenecks:

- mainline megastructure unlocks;
- Gigas resource chains;
- NSC3 heavy hull chains;
- ESC core component chains;
- selected gated Gigas AP branches if desired.

### Phase 4 - Megastructure Reserve Tuning

After parsing exact costs:

- adjust desired maximums for Gigas-scale projects;
- add project-tier-specific gates;
- preserve emergency shipbuilding and recovery behavior.

### Phase 5 - Personality Variants

Once the mainline works, add personality flavor:

- research megastructure builder;
- militarist heavy-hull modernizer;
- defensive bastion builder;
- economic superproject builder;
- crisis-response survivalist.

## Recommended First Implementation Shape

Do not bundle every AI adjustment by copying all source files into one master AI
mod. That would be fragile and hard to maintain.

Do bundle the logic conceptually in one small compatibility patch that loads
after the major mods:

```text
mods/StellarAIModdedProgression/
  README.md
  descriptor.mod
  common/
    scripted_triggers/
      sai_modded_progression_triggers.txt
    economic_plans/
      sai_modded_progression_economic_plan.txt
    ai_budget/
      sai_modded_progression_alloy_budget.txt
      sai_modded_progression_special_resource_budget.txt
    ascension_perks/
      sai_modded_progression_gigas_ap_weights.txt
    technology/
      sai_modded_progression_critical_tech_weights.txt
  notes/
    source-map.md
    critical-unlock-chain-matrix.md
```

Keep the first patch narrow:

1. Add readiness triggers.
2. Add economy subplans for Gigas/ESC resources.
3. Add conservative megastructure reserve scaling.
4. Add research pressure for a short list of bottleneck tech chains.
5. Leave ship design/component selection to NSC3 and ESC unless testing proves
   that their local AI weights fail.

## Open Questions

1. Which Gigas exotic branches should AI empires be allowed to pursue?
2. Should only certain personalities pursue QSO/Birch/EHOF-style projects?
3. What is the correct alloy and special-resource reserve target for each Gigas
   superproject stage?
4. Does Gigas already add enough research options for AI after each ascension
   perk, or do we need a compatibility helper?
5. Does ESC already maintain enough strategic-resource production in the active
   playset, or are its resource hooks only present in inactive/reference Gigas
   plans?
6. Should the compatibility patch favor stronger AI at the cost of more late
   game performance, or should it avoid enabling the heaviest projects for most
   AI empires?

## Working Conclusion

Stellar AI is a good center of gravity because it already configures empires to
build a research economy and later convert that economy into fleet power. The
modern modded gap is not basic intelligence. The gap is late-game coordination.

The best next step is a small `Stellar AI + Gigas/NSC3/ESC progression` patch
that adds a shared modded progression spine:

```text
stable economy
  -> sustained research
  -> critical ascension perks
  -> megastructure unlocks
  -> special resource support
  -> bigger fleets and better components
  -> defended critical systems
  -> carefully gated superprojects
```

That gives the AI a path to compete with a player using advanced modded assets
without requiring a giant rewrite of every mod's local AI logic.
