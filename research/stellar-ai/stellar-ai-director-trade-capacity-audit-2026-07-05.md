# Stellar AI Director Trade Capacity Audit

Date: 2026-07-05
Target game version: Stellaris PC 4.4.4 stable
Mod scope: `mods/StellarAIDirector`

## Finding

Stellaris 4.4 trade is not safe to model as a normal buy/sell commodity. It is
defined as the market resource and as an advanced resource, but vanilla economy
and ship scripts also use it as logistics capacity. The AI Director therefore
needs explicit trade-capacity gates and trade income targets before it pushes
fleet, planet, defense, or megastructure expansion that can add logistics
pressure.

## Vanilla Files Inspected

- `common/strategic_resources/00_strategic_resources.txt`: `trade` is an
  advanced resource with a 50000 cap.
- `common/defines/00_defines.txt`: `MARKET_RESOURCE = "trade"` and AI trade
  stockpile thresholds are defined.
- `common/economic_categories/00_common_categories.txt`: the `trade` category
  participates in AI budgeting.
- `common/economic_plans/02_intermediate.txt`, `04_mature.txt`,
  `05_endgame.txt`: vanilla economic plans include trade income targets.
- `common/ship_sizes/21_overlord.txt` and
  `common/ship_sizes/29_nomads_dlc_ships.txt`: ship resources include
  `logistics = { trade = ... }`.
- `common/scripted_triggers/00_scripted_triggers.txt`: vanilla
  `should_ai_focus_on_trade` exists for trade-specialized AI personalities and
  species traits, which is narrower than the logistics-safe floor the Director
  needs.

## Director Model

- Keep `trade` out of market ROI scalar valuation unless a specific script
  surface supplies a verified market conversion. Treat it as bottleneck/capacity
  evidence in the decision tree.
- Treat negative trade with short stockpile runway as a core deficit.
- Treat low known trade income as expansion pressure when the empire is near
  naval cap, wants fleet buildup, has completed a shipyard multiplier, or is
  preparing large projects.
- Require explicit trade income floors before fleet-throughput, payoff,
  planetary-capacity, starbase-defense, surplus-sink, and megastructure-prep
  gates can activate.
- Preserve vanilla-style trade income pressure in the Director's full
  `basic_economy_plan` override by adding trade reserve and recovery subplans.

## Compatibility Notes

- This is country-level AI policy only; it does not change ship sizes, jobs,
  resources, market rules, colony upkeep, or trade policies.
- The model should remain compatible with Gigastructural Engineering, NSC3, ESC
  NEXT, Starbase Extended, and Universal Resource Patch because it only adds
  namespaced triggers and generated economy-plan targets.
- Nomads, Arkships, and Waystations remain important runtime cases because
  local vanilla files show trade logistics on Arkship-related ship resources.

## Validation Plan

- Regenerate `mods/StellarAIDirector` from
  `tools/generate_stellar_ai_director_patch.py`.
- Run focused unit tests for resource valuation, decision-state classification,
  and generated PDX text.
- Run the generated patch validator.
- Re-index the Stellar AI Director code/docs after generation.

## Open Questions

- Runtime observer testing should confirm that the income thresholds are neither
  too conservative for early fleet movement nor too permissive for late-game
  naval-cap expansion.
- Direct planet automation and ship-design overrides remain deferred until
  observer evidence shows parent AI cannot handle the new logistics pressure.
