# Stellar AI Director Threat Response Feasibility

Target game version: Stellaris PC 4.4.5 stable/current local install.
Local install inspected: `C:/Steam/steamapps/common/Stellaris`.

## Verified Primitives

- `on_war_beginning` from vanilla on-actions.
- `any_attacker`, `any_defender`, `random_defender`, `is_war_leader`, and `using_war_goal` for war context.
- `has_communications` for observer awareness.
- `set_timed_country_flag`, `set_timed_relation_flag`, `add_opinion_modifier`, `remove_opinion_modifier`, `decay`, and `accumulative`.
- Existing Director gates: `staid_core_deficit_short_runway`, `staid_survival_mode`, `staid_recovery_mode`, `staid_fleet_buildup_economy_safe`, and `staid_starbase_defense_economy_safe`.

## Intentional Non-Use

- No forced wars, join-war behavior, punitive casus belli, diplomatic-action overrides, or forced `wg_*` dispatch.
- No raw generator axes are consumed as Stellaris runtime concepts.
- No uncertain visibility model beyond verified communications.

## Compatibility Position

V1 reacts only from eligible third-party default countries with communications. Direct victims, participants, uncertain country types, and unknown war goals remain outside the third-party economy path. Modded war goals are inert until explicitly classified with evidence and tests.

## Test Steps

Run unit tests, regenerate the patch, validate generated output, run `git diff --check`, refresh the docs index, and verify the generated CSV evidence. Runtime/main-menu/observer launch validation is intentionally out of scope for this deterministic implementation goal unless a separate user-approved runtime task is opened.

## Recommendation

Proceed with the bounded V1 implementation as opinion, relation/country flag, and capped economy pressure only.
