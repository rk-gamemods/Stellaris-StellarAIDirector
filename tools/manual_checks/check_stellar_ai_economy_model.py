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

from simulate_stellar_ai_economy import load_pdx_policy, load_scenarios, simulate  # noqa: E402


def main() -> int:
    policy = load_pdx_policy()
    failures: list[str] = []
    print(f"PDX source: {policy.source}")
    for scenario in load_scenarios():
        _, result = simulate(scenario, policy)
        if scenario.control:
            print(
                f"{scenario.name}: ratio={result['research_to_ordinary_ratio']:.4f} "
                f"support_safe={result['support_safe']} food={result['final_income_food']}"
            )
        else:
            print(
                f"{scenario.name}: eventual={result['strategic_eventual_recovery']} "
                f"unbridged={result['strategic_construction_only_survives']} "
                f"market_bridge={result['strategic_market_bridge_affordable']} "
                f"bridge_cost={result['total_bridge_market_cost']:.3f}"
            )
        if not result["ratio_target_met"]:
            failures.append(f"{scenario.name}: research ratio below 2:1")
        if not scenario.bio_ships and scenario.income["food"] <= 50 and result["final_income_food"] > 50:
            failures.append(f"{scenario.name}: normal food income exceeds +50")
        if not result["ordinary_model_safe"]:
            failures.append(f"{scenario.name}: strategic construction destabilizes ordinary support")
        if not scenario.control and not result["strategic_eventual_recovery"]:
            failures.append(f"{scenario.name}: strategic production does not recover")
        if not scenario.control and not result["strategic_recovery_financed"]:
            failures.append(f"{scenario.name}: recovery bridge is not financed")
        if scenario.name == "strategic_gas_prevention_growth":
            if not result["strategic_construction_only_survives"] or result["total_bridge_market_cost"] != 0:
                failures.append(f"{scenario.name}: proactive handler failed to prevent depletion")
    if failures:
        print("\nPDX policy failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("\nPDX policy satisfies the modeled doctrine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
