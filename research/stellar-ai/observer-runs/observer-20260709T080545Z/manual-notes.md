# Manual Notes For observer-20260709T080545Z

## Setup

- Launch surface: direct Stellaris launch through local install after Irony/launcher-readiness gates.
- Irony collection/playset: active Stellaris playset with Stellar AI Director and strategic v2 compatibility stack.
- Stellar AI Director included: yes; baseline commit `ce54d33 Loosen research construction recovery gate`.
- Game version: target Stellaris 4.4.5; previous runtime screen displayed Pegasus v4.4.4 and must be rechecked here.
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

### 2300

### 2325

### 2350

## Qualitative Behavior

- Strong AI behavior:
- Bad economy behavior:
- Bad fleet/war behavior:
- Missing modded asset usage:
- Deficit or collapse cases:

## Patch Hypotheses

Each hypothesis must cite evidence from this run, source files, logs, saves, screenshots, or current research.

| hypothesis | evidence | expected effect | patch status | result |
| --- | --- | --- | --- | --- |
| Research construction recovery was over-gated by `staid_research_input_runway_safe` | `observer-20260709T052514Z` showed only ~645 top regular-AI research by 2325; generated research labs had zero AI weight until high energy income/stockpile thresholds were met | Under-curve empires should build labs earlier, raising research trajectory by 2250/2300/2325 and making 3,000+ monthly research before 2350 plausible | Implemented in `ce54d33` via `staid_research_construction_priority_ready` | Pending this run |
