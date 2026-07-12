"""Opt-in diagnostic check of the generated Director PDX economy plan.

Run this file directly only during economic troubleshooting or an explicitly
verbose validation pass. It is intentionally outside tools/tests so routine
automatic test discovery does not execute the simulation.
"""

from __future__ import annotations

import sys
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from simulate_stellar_ai_economy import (  # noqa: E402
    ACTIVATION_MATRIX,
    ACTIVE_PRIORITY,
    CONCURRENT_FEASIBILITY,
    DEFICIT_ONLY_PLUS_ONE,
    FAILED_C9,
    LANE_STARVATION,
    POLICY_COUNTERFACTUAL,
    PARENT_ONLY,
    STRATEGIC_RESOURCES,
    build_cross_priority_artifacts,
    load_pdx_policy,
    load_scenarios,
    simulate,
    verify_model_artifact_freshness,
    verify_optional_comparative_report,
)


def main() -> int:
    external_report_status = verify_optional_comparative_report()
    policy = load_pdx_policy()
    failures: list[str] = []
    legacy_timeline: list[dict[str, object]] = []
    legacy_summary: list[dict[str, object]] = []
    print(f"PDX source: {policy.source}")
    print(f"External report: {external_report_status}")
    for scenario in load_scenarios():
        timeline, result = simulate(scenario, policy)
        legacy_timeline.extend(timeline)
        legacy_summary.append(result)
        print(
            f"{scenario.name}: ratio={result['research_to_ordinary_ratio']:.4f} "
            f"support_safe={result['support_safe']} food={result['final_income_food']}"
        )
        if not result["ratio_target_met"]:
            failures.append(f"{scenario.name}: research ratio below 2:1")
        if not result["support_safe"]:
            failures.append(f"{scenario.name}: energy or consumer-goods support below target")
        if not scenario.bio_ships and scenario.income["food"] <= 50 and result["final_income_food"] > 50:
            failures.append(f"{scenario.name}: normal food income exceeds +50")

    artifacts, provenance_id, _ = build_cross_priority_artifacts()
    activation = artifacts[ACTIVATION_MATRIX]
    if any(not row["expectation_met"] for row in activation):
        failures.append("cross-priority activation matrix differs from its fixture oracle")
    if len(activation) != 120 or {
        row["resource"] for row in activation
    } != set(STRATEGIC_RESOURCES):
        failures.append("activation matrix lacks exact 8-case coverage for all strategic resources")
    if any(
        row["unsafe_predeficit_activation"] and row["policy_id"] != FAILED_C9.name
        for row in activation
    ):
        failures.append("a bounded policy is classified as an unsafe pre-deficit activation")
    selected = {
        (row["scenario_id"], row["policy_id"]): set(str(row["project_ids"]).split("|"))
        for row in artifacts[CONCURRENT_FEASIBILITY]
        if row["selected_by_policy"]
    }
    expected_bundles = {
        ("research_gas_deficit", DEFICIT_ONLY_PLUS_ONE.name): {"research_lane", "gas_recovery_lane"},
        ("research_motes_deficit", DEFICIT_ONLY_PLUS_ONE.name): {"motes_research_lane", "motes_recovery_lane"},
        ("defense_crystals_deficit", DEFICIT_ONLY_PLUS_ONE.name): {"crystals_defense_lane", "crystals_recovery_lane"},
        ("threat_strategic_deficit", DEFICIT_ONLY_PLUS_ONE.name): {"threat_defense", "threat_hulls", "threat_gas"},
        ("influence_sharing", PARENT_ONLY.name): {"share_claim", "share_outpost"},
        ("habitat_non_veto", PARENT_ONLY.name): {"colonize_existing_habitat", "start_new_habitat"},
    }
    for key, expected in expected_bundles.items():
        if selected.get(key) != expected:
            failures.append(f"{key}: expected concurrent bundle {sorted(expected)}, got {sorted(selected.get(key, set()))}")
    c9_starvation = [
        row
        for row in artifacts[LANE_STARVATION]
        if row["scenario_id"] == "failed_c9_collateral"
        and row["policy_id"] == FAILED_C9.name
        and row["lane"] == "research"
        and row["starved"]
    ]
    if not c9_starvation:
        failures.append("failed c9 policy did not reproduce collateral research starvation")
    c9_counterfactual = [
        row
        for row in artifacts[POLICY_COUNTERFACTUAL]
        if row["scenario_id"] == "failed_c9_collateral"
        and row["policy_id"] == FAILED_C9.name
        and row["unsafe"]
    ]
    if not c9_counterfactual:
        failures.append("failed c9 counterfactual was not classified unsafe")
    pending = {
        row["scenario_id"]: row
        for row in artifacts[ACTIVE_PRIORITY]
        if row["policy_id"] == DEFICIT_ONLY_PLUS_ONE.name
        and row["scenario_id"].startswith("pending_")
    }
    expected_pending = {
        "pending_gas_full_commitment": ("false", "committed_recovery"),
        "pending_gas_fractional_commitment": ("true", "actual_deficit"),
        "pending_gas_slow_commitment": ("true", "actual_deficit"),
    }
    for scenario_id, (state, reason) in expected_pending.items():
        row = pending.get(scenario_id)
        if not row or (row["activation_state"], row["activation_reasons"]) != (
            state,
            reason,
        ):
            failures.append(
                f"{scenario_id}: expected activation {(state, reason)}, got "
                f"{None if not row else (row['activation_state'], row['activation_reasons'])}"
            )
    consumer = pending.get("pending_consumer_runway")
    if not consumer or consumer["affordable_now"] or '"code":"runway"' not in consumer["feasibility_reasons"]:
        failures.append("pending consumer upkeep did not block unsafe research runway")
    print(
        f"Cross-priority model: provenance={provenance_id} "
        f"activation={len(activation)} feasibility={len(artifacts[CONCURRENT_FEASIBILITY])}"
    )
    try:
        verified_id, _ = verify_model_artifact_freshness(
            legacy_timeline,
            legacy_summary,
            artifacts,
        )
        if verified_id != provenance_id:
            failures.append("artifact verifier returned a different provenance ID")
    except (OSError, ValueError) as error:
        failures.append(str(error))
    if failures:
        print("\nPDX policy failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("\nPDX policy satisfies the modeled doctrine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
