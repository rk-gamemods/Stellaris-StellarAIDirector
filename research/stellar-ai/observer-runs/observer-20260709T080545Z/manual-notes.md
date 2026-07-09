# Manual Notes For observer-20260709T080545Z

## Setup

- Launch surface: direct Stellaris launch through local install after Irony/launcher-readiness gates.
- Irony collection/playset: active Stellaris playset with Stellar AI Director and strategic v2 compatibility stack.
- Stellar AI Director included: yes; baseline commit `ce54d33 Loosen research construction recovery gate`.
- Game version: runtime displayed Pegasus v4.4.4 (26b7), while the repository default target is 4.4.5. Treat this as a runtime-version mismatch risk.
- Galaxy size: Tiny / 200 stars.
- AI empire count: 6 regular AI empires.
- Difficulty: Ensign.
- Scaling: off.
- Advanced AI starts: off.
- Player/AI hidden bonuses: off; difficulty-adjusted AI modifiers disabled.
- Crisis settings: not the primary benchmark; stop at or before 2350.
- Seed save: capture after new-game setup before long observer advance.
- Predecessor run: `observer-20260709T052514Z`, stopped at 2325 because the top eligible regular AI reached only ~645 research/month.
- Rerun hypothesis: commit `ce54d33` should let under-curve empires build research labs once minimum consumer-goods and energy runway is safe instead of waiting for the old 3,000-energy full runway gate.
- Gigas/Guilli setup caveat: startup UI reported job-based megastructure build cap/supertensiles disabled due a 4.4 bug and mega build cap set to Unlimited. This may affect how "megastructures" counts should be interpreted.
- Commands-at-date lifecycle: enabled through `tools\manage_stellaris_commands_at_date.py enable` for this run only, then disabled after the 2350 endpoint. Final status was absent/managed=false.
- Benchmark result: failed. No eligible regular AI reached 3,000 total monthly research before or at 2350.

## Console Verification

Record exact `help <command>` results before relying on commands.

| command | help verified | result or alternative |
| --- | --- | --- |
| `human_ai` | no | |
| `observe` | no | |
| `game_speed 5` | no | |
| `fast_forward <days> 1` | no | |

## Checkpoint Notes

### 2250

- Top research: `NAME_The_Chosen` at 207.429/month, 35.46 alloys/month, fleet 160, 3 colonies, 1 megastructure.
- Best large-structure count: `United %ADJECTIVE% Teaf'alan Polity` at 5 megastructures but only 157.646 research/month.
- Overall read: research trajectory was far below the benchmark curve by the first checkpoint.

### 2300

- Top research: `NAME_The_Chosen` at 562.025/month, 121.329 alloys/month, fleet 362, 6 colonies, 6 megastructures.
- `SPEC_Alari Kernel` reached 8 megastructures and 211.248 alloys/month but only 357.581 research/month and fleet 5.
- Overall read: the research-gate patch did not create the needed early snowball. Some empires were building structures, but research conversion remained weak.

### 2325

- Top research: `NAME_The_Chosen` at 723.871/month, 188.192 alloys/month, fleet 486, 6 colonies, 11 megastructures.
- `EMPIRE_DESIGN_humans1` reached 16 megastructures and 453.775 research/month, still far below the needed trajectory.
- Overall read: under-curve empires improved compared with the predecessor run, but none were close to 3,000 research/month or advanced-ship readiness.

### 2350

- Top research: `Laurnaise Empire` at 1018.93/month, 335.996 alloys/month, fleet 1130, 3 colonies, 5 megastructures.
- `EMPIRE_DESIGN_humans1` had 28 megastructures but only 598.307 research/month and fleet 23.
- `NAME_The_Chosen` regressed from 723.871 research/month in 2325 to 546.841 in 2350, with fleet 92.
- Overall read: benchmark failed decisively. The strongest empire reached only about one third of the required 3,000 research/month target by 2350.

## Qualitative Behavior

- Strong AI behavior: multiple empires built or owned many structures counted as megastructures, and several maintained positive basic-resource income.
- Bad economy behavior: research income stayed far below target despite relaxed lab construction gates; high megastructure counts did not reliably correlate with research output.
- Bad fleet/war behavior: some high-structure empires had negligible fleets by 2350, especially `EMPIRE_DESIGN_humans1` with fleet 23 despite 28 megastructures.
- Missing modded asset usage: checkpoint data does not prove meaningful research megastructure or advanced-ship progression; save/log inspection is required to distinguish useful megas from low-value or non-research structures.
- Deficit or collapse cases: no broad monthly resource deficit was visible in the top checkpoint rows, so the failure is more likely priority/conversion/activation than a simple visible deficit spiral.

## Patch Hypotheses

Each hypothesis must cite evidence from this run, source files, logs, saves, screenshots, or current research.

| hypothesis | evidence | expected effect | patch status | result |
| --- | --- | --- | --- | --- |
| Research construction recovery was over-gated by `staid_research_input_runway_safe` | `observer-20260709T052514Z` showed only ~645 top regular-AI research by 2325; generated research labs had zero AI weight until high energy income/stockpile thresholds were met | Under-curve empires should build labs earlier, raising research trajectory by 2250/2300/2325 and making 3,000+ monthly research before 2350 plausible | Implemented in `ce54d33` via `staid_research_construction_priority_ready` | Failed as a sufficient fix. Top research reached 723.871 by 2325 and 1018.93 by 2350, below the 3,000/month benchmark. |
| Megastructure ownership is not translating into research or fleet power | `EMPIRE_DESIGN_humans1` reached 28 megastructures at 2350 but only 598.307 research/month and fleet 23 | Next patch should bias useful research/technology/ship-enabling megastructure paths and verify the owned structure types in saves, not only structure counts | Not implemented | New hypothesis from this failed run |
| Economic-plan or job conversion may be limiting labs and specialist output | Top empires had positive resource income but low research relative to colonies, pops, and structures; no top-row deficit explains the miss | Inspect save internals for building/job mix and confirm relevant economic plans and AI weights activate through 2250/2300/2325 | Not implemented | New hypothesis from this failed run |
