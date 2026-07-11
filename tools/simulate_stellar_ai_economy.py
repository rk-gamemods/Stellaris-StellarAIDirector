"""Deterministic economic-band simulator for Stellar AI Director.

This is an offline design tool. It does not generate or modify Stellaris mod
files. Run without arguments from the repository root.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research" / "stellar-ai"
SCENARIOS = RESEARCH / "stellar-ai-economic-model-scenarios-2026-07-11.csv"
TIMELINE = RESEARCH / "stellar-ai-economic-model-timeline-2026-07-11.csv"
SUMMARY = RESEARCH / "stellar-ai-economic-model-summary-2026-07-11.csv"

ORDINARY = ("energy", "minerals", "food", "consumer_goods", "alloys", "unity")
RESOURCES = ORDINARY + ("research",)

PHASE_FLOORS = {
    "early": {"energy": 40, "minerals": 120, "food": 10, "consumer_goods": 30, "alloys": 60, "unity": 30, "research": 300},
    "mid": {"energy": 100, "minerals": 150, "food": 10, "consumer_goods": 60, "alloys": 250, "unity": 80, "research": 1200},
    "late": {"energy": 250, "minerals": 200, "food": 10, "consumer_goods": 120, "alloys": 600, "unity": 150, "research": 4000},
}

# Approximate marginal support burden derived from the project's research
# capacity model. These are model parameters, not claimed engine constants.
RESEARCH_ENERGY_SUPPORT = 0.15
RESEARCH_CG_SUPPORT = 0.03
RESEARCH_RATIO = 2.0


@dataclass(frozen=True)
class Scenario:
    name: str
    phase: str
    months: int
    investments_per_month: int
    aggressive_expansion: bool
    at_war: bool
    bio_ships: bool
    income: dict[str, float]
    stockpile: dict[str, float]
    increments: dict[str, float]


def _bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}


def load_scenarios(path: Path = SCENARIOS) -> list[Scenario]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    scenarios: list[Scenario] = []
    for row in rows:
        scenarios.append(
            Scenario(
                name=row["scenario"],
                phase=row["phase"],
                months=int(row["months"]),
                investments_per_month=int(row["investments_per_month"]),
                aggressive_expansion=_bool(row["aggressive_expansion"]),
                at_war=_bool(row["at_war"]),
                bio_ships=_bool(row["bio_ships"]),
                income={resource: float(row[f"income_{resource}"]) for resource in RESOURCES},
                stockpile={resource: float(row[f"stockpile_{resource}"]) for resource in ORDINARY},
                increments={resource: float(row[f"increment_{resource}"]) for resource in RESOURCES},
            )
        )
    return scenarios


def targets(scenario: Scenario, income: dict[str, float]) -> dict[str, float]:
    result = dict(PHASE_FLOORS[scenario.phase])
    result["food"] = 50 if scenario.bio_ships else 10
    if scenario.aggressive_expansion:
        result["minerals"] *= 1.75 if scenario.phase == "early" else 1.25
    if scenario.at_war:
        result["alloys"] *= 1.5
    result["energy"] = max(result["energy"], income["research"] * RESEARCH_ENERGY_SUPPORT)
    result["consumer_goods"] = max(result["consumer_goods"], income["research"] * RESEARCH_CG_SUPPORT)
    ordinary_positive = sum(max(income[resource], 0.0) for resource in ORDINARY)
    result["research"] = max(result["research"], RESEARCH_RATIO * ordinary_positive)
    return result


def choose_investment(scenario: Scenario, income: dict[str, float], stockpile: dict[str, float]) -> tuple[str | None, dict[str, float]]:
    current_targets = targets(scenario, income)
    projected_research = income["research"] + scenario.increments["research"]
    # Give support resources a one-step look-ahead target. Without this, the
    # controller can correctly block the next research increment while also
    # seeing no current energy/CG shortfall, leaving all three lanes idle.
    current_targets["energy"] = max(
        current_targets["energy"], projected_research * RESEARCH_ENERGY_SUPPORT
    )
    current_targets["consumer_goods"] = max(
        current_targets["consumer_goods"], projected_research * RESEARCH_CG_SUPPORT
    )
    scores: dict[str, float] = {}
    for resource in RESOURCES:
        target = current_targets[resource]
        shortfall = max(target - income[resource], 0.0)
        scores[resource] = shortfall / max(target, 1.0)

    # Survival inputs interrupt research only when actually unsafe.
    for resource in ("energy", "consumer_goods", "food"):
        if income[resource] < 0:
            scores[resource] += 100
        elif stockpile[resource] < max(-income[resource] * 6, 0):
            scores[resource] += 50

    # Research wins ordinary competition; phase-specific construction inputs
    # remain meaningful without becoming unlimited surplus sinks.
    scores["research"] *= 8.0
    scores["energy"] *= 4.0
    scores["consumer_goods"] *= 4.0
    scores["minerals"] *= 2.5 if scenario.phase == "early" else 1.5
    scores["alloys"] *= 2.0 if scenario.phase == "early" else 3.0
    scores["unity"] *= 1.0
    scores["food"] *= 1.0

    # Research may push aggressively only when the next marginal increment is
    # already supportable. This prevents alternating bands from letting science
    # outrun the energy/consumer-goods economy by one planning cycle.
    if (
        income["energy"] < max(PHASE_FLOORS[scenario.phase]["energy"], projected_research * RESEARCH_ENERGY_SUPPORT)
        or income["consumer_goods"]
        < max(PHASE_FLOORS[scenario.phase]["consumer_goods"], projected_research * RESEARCH_CG_SUPPORT)
    ):
        scores["research"] = 0.0

    viable = [resource for resource in RESOURCES if scenario.increments[resource] > 0]
    choice = max(viable, key=lambda resource: (scores[resource], resource == "research"))
    return (choice if scores[choice] > 0 else None), current_targets


def simulate(scenario: Scenario) -> tuple[list[dict[str, object]], dict[str, object]]:
    income = dict(scenario.income)
    stockpile = dict(scenario.stockpile)
    investments: Counter[str] = Counter()
    timeline: list[dict[str, object]] = []
    minimum_stockpile = dict(stockpile)

    for month in range(1, scenario.months + 1):
        for _ in range(scenario.investments_per_month):
            resource, _ = choose_investment(scenario, income, stockpile)
            if resource is None:
                break
            income[resource] += scenario.increments[resource]
            investments[resource] += 1
        for resource in ORDINARY:
            stockpile[resource] = max(0.0, stockpile[resource] + income[resource])
            minimum_stockpile[resource] = min(minimum_stockpile[resource], stockpile[resource])
        current_targets = targets(scenario, income)
        ordinary_positive = sum(max(income[resource], 0.0) for resource in ORDINARY)
        timeline.append(
            {
                "scenario": scenario.name,
                "month": month,
                **{f"income_{resource}": round(income[resource], 3) for resource in RESOURCES},
                **{f"target_{resource}": round(current_targets[resource], 3) for resource in RESOURCES},
                "research_to_ordinary_ratio": round(income["research"] / max(ordinary_positive, 1.0), 4),
            }
        )

    ordinary_positive = sum(max(income[resource], 0.0) for resource in ORDINARY)
    final_targets = targets(scenario, income)
    summary: dict[str, object] = {
        "scenario": scenario.name,
        "phase": scenario.phase,
        "months": scenario.months,
        "research_to_ordinary_ratio": round(income["research"] / max(ordinary_positive, 1.0), 4),
        "ratio_target_met": income["research"] >= RESEARCH_RATIO * ordinary_positive,
        "food_overproduction": income["food"] > (100 if scenario.bio_ships else 50),
        "support_safe": income["energy"] >= final_targets["energy"] and income["consumer_goods"] >= final_targets["consumer_goods"],
        **{f"final_income_{resource}": round(income[resource], 3) for resource in RESOURCES},
        **{f"investment_{resource}": investments[resource] for resource in RESOURCES},
        **{f"minimum_stockpile_{resource}": round(minimum_stockpile[resource], 3) for resource in ORDINARY},
    }
    return timeline, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    all_timeline: list[dict[str, object]] = []
    all_summary: list[dict[str, object]] = []
    for scenario in load_scenarios():
        timeline, summary = simulate(scenario)
        all_timeline.extend(timeline)
        all_summary.append(summary)
    write_csv(TIMELINE, all_timeline)
    write_csv(SUMMARY, all_summary)
    print(f"Simulated {len(all_summary)} scenarios; wrote {TIMELINE.name} and {SUMMARY.name}")


if __name__ == "__main__":
    main()
