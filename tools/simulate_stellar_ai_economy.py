"""Deterministic economic-band simulator for Stellar AI Director.

This is an offline design tool. It does not generate or modify Stellaris mod
files. Run without arguments from the repository root.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research" / "stellar-ai"
SCENARIOS = RESEARCH / "stellar-ai-economic-model-scenarios-2026-07-11.csv"
TIMELINE = RESEARCH / "stellar-ai-economic-model-timeline-2026-07-11.csv"
SUMMARY = RESEARCH / "stellar-ai-economic-model-summary-2026-07-11.csv"
PDX_PLAN = ROOT / "mods" / "StellarAIDirector" / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"

ORDINARY = ("energy", "minerals", "food", "consumer_goods", "alloys", "unity", "trade")
RESOURCES = ORDINARY + ("research",)
RESEARCH_RATIO = 2.0

PHASE_SUBPLANS = {
    "early": ("Stellar AI Director safe research baseline", "Stellar AI Director early modded research rush"),
    "mid": ("Stellar AI Director safe research baseline", "Stellar AI Director midgame megastructure rush"),
    "late": ("Stellar AI Director safe research baseline", "Stellar AI Director crisis-scale giga rush"),
}
WAR_SUBPLAN = "Stellar AI Director militarist conquest fleet reserve"


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


@dataclass(frozen=True)
class PdxPolicy:
    source: Path
    base_income: dict[str, float]
    subplan_income: dict[str, dict[str, float]]


def _braced_block(text: str, open_brace: int) -> tuple[str, int]:
    depth = 0
    for index in range(open_brace, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[open_brace + 1 : index], index + 1
    raise ValueError(f"Unclosed PDX block beginning at byte {open_brace}")


def _named_blocks(text: str, key: str) -> list[str]:
    blocks: list[str] = []
    pattern = re.compile(rf"(?m)^\s*{re.escape(key)}\s*=\s*\{{")
    for match in pattern.finditer(text):
        block, _ = _braced_block(text, match.end() - 1)
        blocks.append(block)
    return blocks


def _income(block: str) -> dict[str, float]:
    matches = _named_blocks(block, "income")
    if not matches:
        return {resource: 0.0 for resource in RESOURCES}
    values = {resource: 0.0 for resource in RESOURCES}
    for key, raw_value in re.findall(r"(?m)^\s*([a-zA-Z0-9_]+)\s*=\s*(-?\d+(?:\.\d+)?)\s*$", matches[0]):
        if key in values:
            values[key] += float(raw_value)
        elif key in {"physics_research", "society_research", "engineering_research"}:
            values["research"] += float(raw_value)
    return values


def load_pdx_policy(path: Path = PDX_PLAN) -> PdxPolicy:
    text = re.sub(r"(?m)#.*$", "", path.read_text(encoding="utf-8-sig"))
    plan_match = re.search(r"(?m)^basic_economy_plan\s*=\s*\{", text)
    if not plan_match:
        raise ValueError(f"basic_economy_plan not found in {path}")
    plan, _ = _braced_block(text, plan_match.end() - 1)
    first_subplan = re.search(r"(?m)^\s*subplan\s*=\s*\{", plan)
    base_region = plan[: first_subplan.start()] if first_subplan else plan
    subplans: dict[str, dict[str, float]] = {}
    for block in _named_blocks(plan, "subplan"):
        name_match = re.search(r'(?m)^\s*set_name\s*=\s*"([^"]+)"', block)
        if name_match:
            subplans[name_match.group(1)] = _income(block)
    return PdxPolicy(path, _income(base_region), subplans)


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
                income={resource: float(row.get(f"income_{resource}", 0) or 0) for resource in RESOURCES},
                stockpile={resource: float(row.get(f"stockpile_{resource}", 0) or 0) for resource in ORDINARY},
                increments={resource: float(row.get(f"increment_{resource}", 0) or 0) for resource in RESOURCES},
            )
        )
    return scenarios


def targets(scenario: Scenario, policy: PdxPolicy) -> dict[str, float]:
    result = dict(policy.base_income)
    selected = list(PHASE_SUBPLANS[scenario.phase])
    if scenario.at_war:
        selected.append(WAR_SUBPLAN)
    for name in selected:
        if name not in policy.subplan_income:
            raise ValueError(f"Required PDX subplan not found: {name}")
        for resource, value in policy.subplan_income[name].items():
            result[resource] += value
    return result


def choose_investment(scenario: Scenario, policy: PdxPolicy, income: dict[str, float], stockpile: dict[str, float]) -> tuple[str | None, dict[str, float]]:
    current_targets = targets(scenario, policy)
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

    viable = [resource for resource in RESOURCES if scenario.increments[resource] > 0]
    choice = max(viable, key=lambda resource: (scores[resource], resource == "research"))
    return (choice if scores[choice] > 0 else None), current_targets


def simulate(scenario: Scenario, policy: PdxPolicy | None = None) -> tuple[list[dict[str, object]], dict[str, object]]:
    policy = policy or load_pdx_policy()
    income = dict(scenario.income)
    stockpile = dict(scenario.stockpile)
    investments: Counter[str] = Counter()
    timeline: list[dict[str, object]] = []
    minimum_stockpile = dict(stockpile)

    for month in range(1, scenario.months + 1):
        for _ in range(scenario.investments_per_month):
            resource, _ = choose_investment(scenario, policy, income, stockpile)
            if resource is None:
                break
            income[resource] += scenario.increments[resource]
            investments[resource] += 1
        for resource in ORDINARY:
            stockpile[resource] = max(0.0, stockpile[resource] + income[resource])
            minimum_stockpile[resource] = min(minimum_stockpile[resource], stockpile[resource])
        current_targets = targets(scenario, policy)
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
    final_targets = targets(scenario, policy)
    summary: dict[str, object] = {
        "scenario": scenario.name,
        "phase": scenario.phase,
        "months": scenario.months,
        "research_to_ordinary_ratio": round(income["research"] / max(ordinary_positive, 1.0), 4),
        "ratio_target_met": income["research"] >= RESEARCH_RATIO * ordinary_positive,
        "food_overproduction": income["food"] > (100 if scenario.bio_ships else 50),
        "support_safe": income["energy"] >= final_targets["energy"] and income["consumer_goods"] >= final_targets["consumer_goods"],
        "pdx_source": str(policy.source.relative_to(ROOT)).replace("\\", "/"),
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
    policy = load_pdx_policy()
    all_timeline: list[dict[str, object]] = []
    all_summary: list[dict[str, object]] = []
    for scenario in load_scenarios():
        timeline, summary = simulate(scenario, policy)
        all_timeline.extend(timeline)
        all_summary.append(summary)
    write_csv(TIMELINE, all_timeline)
    write_csv(SUMMARY, all_summary)
    print(f"Simulated {len(all_summary)} scenarios from {policy.source.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
