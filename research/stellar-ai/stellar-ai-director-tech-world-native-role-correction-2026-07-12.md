# Tech-World native role correction

Target: Stellaris PC 4.4.4 active local baseline, Stellar AI Director live-linked test branch.

## Evidence and correction

The 2263.01.01 save had 13 colonies, six persistent research-plan claim flags, but only four actual Tech-World designations. Several claimed or designated worlds had mature generator, mining, farming, factory, or foundry infrastructure and no reachable research producer chain. The event quota therefore measured stored intent rather than realized specialization.

The correction removes the monthly research-claim event, carrier-flag quota, and `+100000` designation/zone directives. Native designation weights now count actual `col_research` worlds against a soft one-third ceiling. Positive pressure requires safe research input runway and either existing research infrastructure or a low-conversion-cost urban candidate. Mature rural or industrial worlds without research infrastructure are not treated as candidates. A selected Tech-World receives a bounded `+5` research-zone weight so native construction can follow through without a forced queue or scripted conversion.

At 13 colonies the soft ceiling is four actual Tech-Worlds. The staged trigger covers one role per three colonies through 60 colonies; empires larger than 60 remain conservatively capped at 20 until runtime evidence justifies another tier.

## Top five risks and follow-up tests

1. Zone occupancy: native weights cannot guarantee conversion when every compatible zone slot is occupied. Runtime-check whether unsuitable existing Tech-Worlds reclassify and whether suitable worlds create research zones.
2. Modded district IDs: the greenfield guard explicitly measures vanilla city, generator, mining, and farming districts. Audit high-volume active-stack district aliases before broadening eligibility.
3. Research-world scarcity: strict conversion-cost guards may leave an empire below one-third when no suitable world exists. This is intentional; verify the capital and special-world research paths remain sufficient.
4. Input shocks: the runway gate pauses new roles but does not dismantle productive existing research worlds. Verify a consumer-goods or energy shock does not cause designation churn.
5. Very large empires: the 60-colony terminal tier is deliberately conservative. Add tiers only with save-backed evidence that candidate quality and support income scale safely.

## Static and runtime boundary

Static validation must prove syntax, zero live research-plan flag/event references, exact staged count thresholds, current-vanilla object parity outside the additive weight blocks, and bounded zone pressure. It cannot prove designation selection, zone conversion, or construction execution. Those require a new save after the updated mod is loaded.
