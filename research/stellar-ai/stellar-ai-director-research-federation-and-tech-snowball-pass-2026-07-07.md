# Stellar AI Director Research Federation And Tech Snowball Pass

Date: 2026-07-07
Target game when written: Stellaris PC 4.4.4 stable, active modded observer stack. Current target as of 2026-07-08 is Stellaris PC 4.4.5 stable/current local install.

## User Correction

The current benchmark is not "one empire is getting somewhere" at 800 monthly research in 2350. For this 25x crisis-oriented modded stack, that is a failed run. The working target is roughly:

- 1000+ monthly research by about 2270-2280.
- 5000-6000+ monthly research by 2350 at minimum.
- Fleet output matters only when it buys survival, territory, pops, subjects, diplomatic leverage, or crisis readiness. Fleet that sits idle is an economic drag.

## External Research Findings

Human tech-rush advice repeatedly converges on the same pattern: maximize the number and quality of pops doing research, support them with consumer goods and energy, avoid letting empire-size penalties erase the gain, and use unity/ascension/federation/subject tools to compound faster than raw labs alone.

Key online sources inspected:

- Stellaris Wiki, Technology: https://stellaris.paradoxwikis.com/Technology
- Stellaris Wiki search snippets for Federation and Diplomacy: https://stellaris.paradoxwikis.com/Federation and https://stellaris.paradoxwikis.com/Diplomacy
- Reddit, "Absolute best tech rush?" 2025 thread: https://www.reddit.com/r/Stellaris/comments/1ig9i4f/absolute_best_tech_rush/
- Reddit, "Struggling with tech rush, advice?" 2025 thread: https://www.reddit.com/r/Stellaris/comments/1ivh5l0/struggling_with_tech_rush_advice/
- Steam multiplayer guide: https://steamcommunity.com/sharedfiles/filedetails/?id=2309611439
- Steam economy discussion, 2025: https://steamcommunity.com/app/281990/discussions/0/596284732212418039/
- Stellaris Build, "Generic Tech Rush Guide (1000 Tech by Year 30)": https://stellaris-build.com/build/4

Actionable patterns:

- Early research is a production chain, not a single building priority: research labs require consumer goods, minerals to build, energy/market support, and enough pops to staff the jobs.
- The capital or best early high-pop world should become the first research concentration because it has early building slots and pops; weaker colonies should carry basic production and consumer-good support.
- Do not overbuild empty jobs. Building labs before pop throughput and CG support exist creates stalled construction and deficits instead of research.
- Unity acceleration matters because modern tech-rush routes often rush ascension/virtuality/modularity/synthetic/psionic or tradition bonuses first, then convert the larger bonus base into research.
- Research alternatives and tech card manipulation matter. The wiki confirms tier gates, card weights, and extra alternatives from Technocracy, Science Division, Scientific Revolution, Self-Evolving Logic, Research Cooperative president, and Scholarium relationships.
- Keep empire-size pressure visible. The wiki states research cost rises with empire size above 100, and player advice treats sub-100 or high-output-per-size development as a major tech-rush constraint.
- Military tech-rush can be valid only when it takes pops or converts neighbors into subjects, especially scholarium-style research subjects. Passive fleet buildup is not a tech rush.
- Friendly diplomacy should push research agreements and Research Cooperative federation behavior. Ordinary non-research federations do not serve the 2350 crisis-research benchmark.

## Local Game File Findings

Vanilla Research Cooperative / `research_federation`:

- `C:\Steam\steamapps\common\Stellaris\common\federation_types\00_federation_types.txt`
- Object: `research_federation`
- Allow condition: Federations DLC, plus materialist, machine empire, or completed Discovery federation finisher.
- Vanilla `ai_weight` has `base = 0` and only small personality modifiers such as `erudite_explorers +10`, `peaceful_traders +10`, `honorbound_warriors -20`, `hegemonic_imperialists -20`, and `decadent_hierarchy -30`.

Vanilla Research Cooperative research sharing:

- `C:\Steam\steamapps\common\Stellaris\common\federation_perks\00_perks.txt`
- `research_federation_passive` sets `federation_research_sharing_mult = 0.25` and enables `research_sharing = yes`.
- `research_share_1` through `research_share_4` each add another `federation_research_sharing_mult = 0.05`.
- `research_boost_1` adds `all_technology_research_speed = 0.05` for members.

Vanilla research agreement action:

- `C:\Steam\steamapps\common\Stellaris\common\diplomatic_actions\00_actions.txt`
- Object: `action_form_research_agreement`
- `AI_acceptance_base_value = -50`.
- It requires good opinion or 20 trust, and also an embassy or `tr_diplomacy_diplomatic_networking`.
- The action itself does not expose a normal `ai_acceptance` block in vanilla, so the practical knobs are personality acceptance, opinion/trust/embassy setup, and diplomatic-tradition behavior.
- Inside a Research Cooperative with the passive perk, member research sharing is automatic and separate research agreement formation is blocked by the `federation_automatic_research` tooltip.

Vanilla personality knob:

- `C:\Steam\steamapps\common\Stellaris\common\personalities\00_personalities.txt`
- `research_agreement_acceptance` is documented as added directly to the chance of accepting a research agreement.
- Current Stellar AI Director does not own `common/personalities`, so changing this is likely a full-object personality override with high compatibility risk unless a safer parent-mod extension surface is found.

## Patch Backlog

P0: Research Federation selection

- Add or generate a `research_federation` override only after reviewing conflict behavior with parent mods.
- Raise Research Cooperative weight for materialist, machine, technologist, erudite, discovery, high-research, friendly, and non-militarist/economy-oriented AI.
- Penalize trade, martial, hegemony, and spiritualist federation drift for empires whose observed role is research/economy snowball, unless their ethics/civics make Research Cooperative impossible.
- Consider allowing militarist empires to prefer military/hegemony only when they also have aggressive war thresholds and a conquest/subject payoff path.

P0: Research agreement formation

- Do not rely only on `research_agreement_acceptance`; also make AI more likely to satisfy the prerequisites: embassies, trust, good opinion, and Diplomatic Networking.
- Candidate surfaces: personalities, diplomacy tradition weights, envoy/diplomacy behavior, opinion modifiers, and event/scripted nudges that are legal for AI only.
- Friendly/non-genocidal empires should treat research agreements as default-positive when opinion/trust gates are met.

P0: Early economy micromanagement for research

- Push one early high-pop capital/research world to labs and research districts/buildings first.
- Move alloy/CG/basic production pressure to support colonies so the capital can stay on research.
- Keep CG and energy market support active enough to prevent lab staffing collapse.
- Avoid overbuilding unstaffed jobs and avoid too much fleet infrastructure unless the empire will use it.
- Add observer metrics for empty researcher jobs, CG deficits, empire size, unity/month, traditions/ascension timing, research agreements, federation type, and subject/scholarium count.

P1: Unity-to-research route

- Review AI weights for Discovery, Diplomacy, Mercantile/Trade where relevant, Cybernetics/Synthetics/Virtuality/Modularity/Psionics, Technological Ascendancy, and Science Division-style bonuses.
- Target result is not generic unity hoarding; it is early ascension/tradition completion that turns into higher research output before 2300.

P1: Military payoff split

- Militarist and conqueror personalities that build fleet should lower acceptable-war thresholds and aim for pops/subjects/territory.
- Non-militarists should keep defensive sufficiency and redirect surplus into research/economy/diplomacy.
- A fleet-focused empire must be evaluated by gained pops, colonies, subjects, and economy/research after wars, not fleet number alone.

## Git Noise Fix

The Codex UI reported over one million pending additions because untracked observer-run artifacts included raw copied Stellaris logs, saves, screenshots, and extracted dumps. Git's tracked diff was only about 10.9k insertions and 1.5k deletions before the ignore fix.

Added `.gitignore` rules for:

- `research/stellar-ai/observer-runs/**/logs/*.log`
- `research/stellar-ai/observer-runs/**/saves/*.sav`
- `research/stellar-ai/observer-runs/**/screenshots/*.png`
- `research/stellar-ai/observer-runs/**/screenshots/*.jpg`
- `research/stellar-ai/observer-runs/**/screenshots/*.jpeg`
- `research/stellar-ai/observer-runs/**/exports/`

This preserves small evidence files such as run README files, metadata, summaries, checkpoint CSVs, and manual notes, while keeping giant local artifacts out of Git status.
