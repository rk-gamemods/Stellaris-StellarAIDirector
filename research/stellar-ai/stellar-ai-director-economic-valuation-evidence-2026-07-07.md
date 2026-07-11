# Stellar AI Director Economic Valuation Evidence

Generated: 2026-07-11T20:51:23.137368+00:00

This is the merged evidence index for economic AI decisions. The construction dataset owns planet-local construction surfaces. The companion nonconstruction dataset owns the rest of the economy-facing AI surfaces and intentionally does not duplicate buildings, zones, districts, or megastructures.

Validation contract:

- Construction dataset: `research/stellar-ai/stellar-ai-director-economic-valuation-2026-07-07.csv`
- Nonconstruction dataset: `research/stellar-ai/stellar-ai-director-nonconstruction-economic-valuation-2026-07-07.csv`
- Both datasets must expose the shared source, cost/upkeep/output, AI-state, data-quality, and 2350-horizon ROI columns.
- The nonconstruction dataset must not include `building`, `zone`, `district`, or `megastructure` rows.
- Future economic weight generation should query both datasets together, then choose eligible objects by `object_type`, ROI horizon, affordability, AI-state gap, and data-quality flags.

## Construction Dataset Counts

- building: 826
- district: 286
- zone: 261

## Nonconstruction Dataset Counts

- ascension_perk: 59
- colony_type: 124
- decision: 352
- deposit: 1174
- edict: 229
- policy: 65
- pop_job: 501
- resource: 36
- starbase_building: 207
- starbase_module: 185
- technology: 1534
- tradition: 269

Configured nonconstruction object types not present in the current file: none

## Combined Counts

- ascension_perk: 59
- building: 826
- colony_type: 124
- decision: 352
- deposit: 1174
- district: 286
- edict: 229
- policy: 65
- pop_job: 501
- resource: 36
- starbase_building: 207
- starbase_module: 185
- technology: 1534
- tradition: 269
- zone: 261
