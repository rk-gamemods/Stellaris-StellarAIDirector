# Stellar AI Director Irony Conflict Scan

Date reviewed: 2026-07-04
Tool: Irony Mod Manager v1.27.192, Irony Conflict Solver Analyze Only
Collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity

## Load Order Boundary

- Existing collection order was preserved by the order proof artifact.
- `!!!Universal Resource Patch [2.4+]` remains at position 116.
- `Stellar AI Director` is the only added local mod and is at position 117.
- No other mod was moved during this review.

## Analyzer Result

- Reviewed surface: `common\ai_budget`
- Conflict Count: 3000
- Reviewed Director conflict classification: intentional Director win
- No unexplained Director gameplay conflicts were observed in the reviewed Director conflict set.

## Reviewed Objects

| object | observed left side | observed right side | classification |
| --- | --- | --- | --- |
| `alloys_expenditure_megastructures` | Stellar AI object | Stellar AI Director - `alloys_expenditure_megastructures` (LIOS) | intentional Director win |
| `negative_mass_expenditure_megastructures` | Gigastructural Engineering & More (4.4) object | Stellar AI Director - `negative_mass_expenditure_megastructures` (LIOS) | intentional Director win |
| `sentient_metal_expenditure_megastructures` | Gigastructural Engineering & More (4.4) object | Stellar AI Director - `sentient_metal_expenditure_megastructures` (LIOS) | intentional Director win |
| `supertensiles_upkeep_megastructures` | Gigastructural Engineering & More (4.4) object | Stellar AI Director - `supertensiles_upkeep_megastructures` (LIOS) | intentional Director win |

## Review Notes

- The resolved output pane used the generated Irony collection object name for each reviewed entry.
- The Director right-side output contains the expected `staid_` gates, including survival/recovery and megastructure pause/prep/commit safety logic.
- The analyzer view was reviewed without applying a conflict solver mutation and without changing the existing collection order.
