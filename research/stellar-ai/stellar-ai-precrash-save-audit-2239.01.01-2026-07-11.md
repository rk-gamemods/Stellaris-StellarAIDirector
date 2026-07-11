# Stellar AI Director Pre-Crash Save Audit: 2239.01.01

Audit date: 2026-07-11  
Save: `autosave_2239.01.01.sav`  
Crash: `stellaris_20260711_094142`  
Observed empire: country 0, United Cevantian Nation

## Evidence boundary

This is a read-only audit of the last autosave written approximately 36 seconds
before the crash folder was created. It does not prove the crash cause. Saved
country/colony/fleet state is authoritative for the listed values; strategic
judgments are labeled below. No observer run or game launch was performed.

## Executive result

| Goal | Result | Evidence |
|---|---|---|
| Aggressive colonization | Improving / strong | 15 colonies by 2239; 14 at 2237.01 and 15 at 2239.01 |
| Approximately 50% research colonies | Partial / below target | 6 of 15 colonies are `col_research` or `col_habitat_research` (40%); 7 carry research-plan claims |
| Actual research scaling | Fail | Saved research rose only 1266.133 to 1292.790 over two years |
| Avoid continued food overproduction | Pass / acceptable | Food income stayed nearly flat, 454.220 to 455.654; the AI did not continue scaling it |
| Early exploration fleet | Pass on quantity | 8 science fleets exist |
| Useful exploration behavior | Fail | 3 of 8 science fleets are `mia_forced_to_decloak` while retaining active orders |
| War/conquest activity | Pass historically | Country flags record declared and won war; country 0 owns a subject |
| Current fleet utilization | Weak / underused | Saved fleet size is 190 and remained flat through all five autosaves |
| Research-oriented policy | Mixed / fail | Technological Ascendancy and Discovery are active, but `economic_policy_military` remains selected |

## Economic trend

| Save | Research | Energy | Minerals | Food | Consumer goods | Alloys | Colonies | Fleet size |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2237.01.01 | 1266.133 | 2106.281 | 2010.789 | 454.220 | 674.152 | 616.798 | 14 | 190 |
| 2237.07.01 | 1268.602 | 2078.237 | 2015.135 | 446.017 | 699.946 | 643.431 | 14 | 190 |
| 2238.01.01 | 1266.773 | 2095.408 | 2058.402 | 449.366 | 697.475 | 662.866 | 14 | 190 |
| 2238.07.01 | 1290.150 | 2112.922 | 2095.952 | 451.891 | 715.252 | 739.144 | 14 | 190 |
| 2239.01.01 | 1292.790 | 2107.706 | 2095.338 | 455.654 | 907.286 | 765.437 | 15 | 190 |

Research grew by only 2.1% while alloys grew 24.1% and consumer goods grew
34.6%. The positive ordinary-income sum at 2239 is far larger than research, so
the user's research-at-least-twice-positive-net-income doctrine is not being
achieved in actual saved behavior. The PDX model's prior green result therefore
does not prove live planner adherence; it does not activate/evaluate every
subplan or reproduce construction decisions.

Food remained essentially flat. That is acceptable: one existing production
source can create more surplus than the empire strictly needs, and the evidence
shows no continuing food-investment trend. No corrective action is recommended
for food from this save.

## Colony designations and output

Research-designated colonies:

- Lastargavin's Shelter — `col_research`, 34.4 research.
- Guison — `col_research`, 115.3 research.
- Color Precursor colony — `col_research`, 7.4 research.
- Al-Madain planetary computer — `col_research`, 0 research at 35 saved pops/workforce units.
- Olympia — `col_habitat_research`, 28.4 research.
- Agartha — `col_research`, 12.3 research.
- One additional research-plan claim is attached to a factory-designated colony,
  showing assignment/reassignment state is not perfectly aligned.

The capital produces approximately 792.2 of the empire's 1292.8 research.
Research designation assignment has improved but remains below the requested ratio, and
research buildout on the designated colonies is still far too weak and
capital-concentrated.

The building cache reinforces that conclusion. Several research-designated
colonies contain only research upkeep/efficiency support buildings and no
obvious laboratory/technology production building. The planetary computer has
one cached building and zero saved research output; Agartha has three cached
buildings and only 12.3 research output. Guison is the strongest non-capital
research world at 115.3 and contains an ESC materials laboratory. Research
designation alone is therefore not causing a reliable research-building
sequence.

## Fleet and exploration state

Country 0 owns 8 science fleets. At the checkpoint:

- fleets 689, 804, and 33555064 are `mia_forced_to_decloak`;
- all three retain an `order_id`;
- all eight science fleets retain active orders;
- country 0 has closed-border relations with at least one contacted empire;
- the Director changes `AUTO_EXPLORE_SYSTEM_OWNED` from vanilla 1000 to 100,
  making foreign-owned targets substantially more attractive.

This proves the repeated-route symptom is not a lack of science ships. It is a
planner/order-state failure that disables 37.5% of the available exploration
fleet at once.

The save contains one military fleet with approximately 6185.5 saved military
power, two transport fleets, and 18 starbases. Fleet size is 190 and did not
increase during the two-year autosave window. Country flags show an earlier war
declaration, war victory, and a subject, so conquest logic has operated, but the
current fleet-growth slope is stalled.

## Policy adherence

Helpful selections:

- belligerent diplomatic stance;
- unrestricted wars;
- indiscriminate bombardment;
- open borders;
- trade converted toward consumer goods;
- Map the Stars;
- Technological Ascendancy;
- Discovery traditions.

Conflicting or wasteful selections:

- `economic_policy_military` conflicts with research-first snowballing when the
  empire already has +765 alloys and only 1293 research;
- Mining Subsidies remains active at approximately +2095 minerals;
- Nutritional Plenitude was activated while food income was already about +449;
- all three research-field policies remain `research_policy_no_focus`.

## Recommended next checks

1. Treat the MIA/order-retention loop as an independent blocking defect.
2. Extend the economic model to evaluate the complete active PDX subplan set and
   compare predictions to these five autosaves.
3. Trace why research-designated colonies are not filling research buildings or
   jobs despite the designation ratio being correct.
4. Add surplus-aware policy gates for military economy, Mining Subsidies, and
   Nutritional Plenitude rather than leaving them as unconditional long-running
   choices.
5. Use the crash forensic lane to correlate the 2239 save state with only the
   bounded pre-crash log window; do not infer causation from startup errors.
