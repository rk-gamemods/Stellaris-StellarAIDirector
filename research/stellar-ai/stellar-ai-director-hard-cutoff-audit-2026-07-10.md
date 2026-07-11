# Stellar AI Director hard-cutoff audit — 2026-07-10

## Scope

- Target: Stellaris PC Pegasus 4.4.4 (5505).
- Runtime evidence: Empire Zero in autosaves 2239.07.01 through 2241.07.01.
- Source surfaces: vanilla `common/ai_budget`, Director generated AI budgets and scripted triggers.
- Boundary: native AI weights, budgets, and plans only. No forced construction or event-driven orders.

## Adopted decision rule

Peace uses the native colony-expansion path. War raises the admission threshold:

`colonize during war = native colonization plan AND native species/affordability gates AND relative economy safe AND no short-runway deficit AND no existential emergency`

`staid_basic_economy_runway_safe` supplies the relative component. Its mineral,
alloy, consumer-goods, food, and energy requirements scale through the existing
colony-count and fleet-power standards rather than one flat stockpile number.
`staid_security_existential` prevents surplus-looking empires from colonizing
while the Director's immediate defensive-emergency state is active.

## Confirmed harmful cutoff

Vanilla `alloys_expenditure_colonies_expand` requires peace or the midgame year.
In the observed 4.4.4 saves, Empire Zero remained at four colonies throughout a
two-year continuous war despite `colonize=yes`, several valid controlled colony
targets, no colony ship, and stockpiles around 9–10k energy, 30–37k minerals,
22–24k food, 39–42k consumer goods, and 32–37k alloys. This is the proven gate
replaced by the relative wartime rule above.

## Other hard gates reviewed

| Surface | Vanilla cutoff | Assessment | Action |
|---|---|---|---|
| Alloy/food ship upgrades | `is_at_war = no` | Plausibly intentional because upgrading can withdraw fleets from active fronts. Continuous war can cause technological stagnation, but the save provides no fleet-upgrade failure evidence. | Do not change yet. Seek a save with obsolete designs, affordable upgrades, and prolonged war. |
| Gateway construction energy budget | `is_at_war = no` | Could suppress strategic mobility during long wars, but construction timing and gateway location matter. | Candidate for a future economy-safe plus security-safe exception; no current change. |
| Unity/influence megastructure budgets | `is_at_war = no` | Long wars can indefinitely block productive megastructures, but diversion may be correct during existential defense. | Candidate for the same relative pattern after runtime evidence. |
| Alloy/food megastructure budgets | peace OR naval capacity above 90% | Already has an offset path rather than a unilateral shutdown. | Preserve. |
| Director peacetime naval-capacity guard | peace-only by design | This is a 4.4.4 war-declaration workaround and explicitly releases during war/emergency. | Preserve. |
| Director diplomatic-opening and boxed-in prewar states | peace-only by definition | These are state classifiers, not economic spending shutoffs; activating them during an existing war would be semantically wrong. | Preserve. |
| Disabled/obsolete objects using `always = no` | Explicit compatibility or obsolete-content sentinels | Not adaptive AI decisions. | Exclude from economy balancing. |

## General review heuristic

A binary gate deserves review when all are true:

1. the blocking state can persist for years (war, capped capacity, deficit flag);
2. the prohibited action remains strategically useful in some blocked states;
3. the engine exposes enough native economic/threat evidence to define a safe exception;
4. the exception still leaves target selection and execution to the native planner.

Prefer `normal path OR (persistent blocked state AND relative economy safe AND
threat safe)` over deleting the safety rule. Do not relax gates solely because
an empire has a large absolute stockpile; income, runway, empire scale, fleet
burden, and immediate survival state must agree.

## Knowledge-base feedback

The version-scoped database correctly located the launcher-selected colony
budget override and nearby Director budget files. It did not contain a curated
claim for the colonization-plan → desired-colonizer → multi-resource funding
pipeline, and the attempted `--mechanic-family ai_economy` filter failed because
that mechanic family is not registered. A future evidence packet should add
that pipeline and a discoverable AI-economy/budget classification.

## Validation boundary

Static validation can prove parsing, object replacement, preserved native
gates, and presence of the relative exception. Only a subsequent game save can
prove that a wartime AI with a valid plan actually builds and uses a colony
ship, and that a threatened or resource-tight wartime AI remains restrained.
