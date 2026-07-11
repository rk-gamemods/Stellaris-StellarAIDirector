"""Deterministic PDX-driven economy model for the Stellar AI Director.

The legacy lane deliberately preserves the original ordinary-resource model.
The strategic lane adds delayed construction, upkeep growth, capacity, costs,
stockpile depletion, and the bridge that must be supplied by native market
demand while new production is still under construction.
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
STRATEGIC_SCENARIOS = RESEARCH / "stellar-ai-strategic-resource-model-scenarios-2026-07-11.csv"
TIMELINE = RESEARCH / "stellar-ai-economic-model-timeline-2026-07-11.csv"
SUMMARY = RESEARCH / "stellar-ai-economic-model-summary-2026-07-11.csv"
PDX_PLAN = ROOT / "mods" / "StellarAIDirector" / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"

ORDINARY = ("energy", "minerals", "food", "consumer_goods", "alloys", "unity", "trade")
STRATEGIC = ("volatile_motes", "exotic_gases", "rare_crystals")
LEGACY_RESOURCES = ORDINARY + ("research",)
FLOW_RESOURCES = ORDINARY + STRATEGIC
RESOURCES = LEGACY_RESOURCES + STRATEGIC
RESEARCH_RATIO = 2.0
EPSILON = 1e-9

PHASE_SUBPLANS = {
    "early": ("Stellar AI Director safe research baseline", "Stellar AI Director early modded research rush"),
    "mid": ("Stellar AI Director safe research baseline", "Stellar AI Director midgame megastructure rush"),
    "late": ("Stellar AI Director safe research baseline", "Stellar AI Director crisis-scale giga rush"),
    "beyond": ("Stellar AI Director safe research baseline", "Stellar AI Director planetcraft survival curve"),
}
PHASE_YEARS = {"early": 20, "mid": 60, "late": 90, "beyond": 130}
WAR_SUBPLAN = "Stellar AI Director militarist conquest fleet reserve"


@dataclass(frozen=True)
class Scenario:
    name: str
    phase: str
    years_passed: int
    months: int
    investments_per_month: int
    strategic_project_starts_per_month: int
    aggressive_expansion: bool
    at_war: bool
    bio_ships: bool
    control: bool
    income: dict[str, float]
    stockpile: dict[str, float]
    increments: dict[str, float]
    production: dict[str, float]
    upkeep: dict[str, float]
    upkeep_growth: dict[str, float]
    strategic_available: dict[str, bool]
    strategic_deficit: dict[str, bool]
    strategic_max_projects: dict[str, int]
    strategic_completion_delay_months: int
    strategic_project_mineral_cost: float
    strategic_project_energy_upkeep: float
    market_currency_reserve: float
    market_cost_per_resource_unit: float


@dataclass(frozen=True)
class StrategicRecoveryBand:
    name: str
    phase: str
    resource: str
    min_years: int
    max_years: int | None
    income_floor: float
    stockpile_floor: float
    target: float


@dataclass(frozen=True)
class PdxPolicy:
    source: Path
    base_income: dict[str, float]
    subplan_income: dict[str, dict[str, float]]
    strategic_recovery: dict[tuple[str, str], StrategicRecoveryBand]


def _braced_block(text: str, opening_brace: int) -> tuple[str, int]:
    depth = 0
    for index in range(opening_brace, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[opening_brace + 1 : index], index + 1
    raise ValueError("Unclosed PDX block")


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


def _year_window(block: str) -> tuple[int, int | None]:
    lower_bounds = [int(value) + 1 for value in re.findall(r"years_passed\s*>\s*(\d+)", block)]
    upper_bounds = [int(value) - 1 for value in re.findall(r"years_passed\s*<\s*(\d+)", block)]
    return (max(lower_bounds, default=0), min(upper_bounds) if upper_bounds else None)


def load_pdx_policy(path: Path = PDX_PLAN) -> PdxPolicy:
    text = re.sub(r"(?m)#.*$", "", path.read_text(encoding="utf-8-sig"))
    plan_match = re.search(r"(?m)^basic_economy_plan\s*=\s*\{", text)
    if not plan_match:
        raise ValueError(f"basic_economy_plan not found in {path}")
    plan, _ = _braced_block(text, plan_match.end() - 1)
    first_subplan = re.search(r"(?m)^\s*subplan\s*=\s*\{", plan)
    base_region = plan[: first_subplan.start()] if first_subplan else plan
    subplans: dict[str, dict[str, float]] = {}
    strategic_recovery: dict[tuple[str, str], StrategicRecoveryBand] = {}
    for block in _named_blocks(plan, "subplan"):
        name_match = re.search(r'(?m)^\s*set_name\s*=\s*"([^"]+)"', block)
        if not name_match:
            continue
        name = name_match.group(1)
        income = _income(block)
        subplans[name] = income
        recovery_match = re.fullmatch(
            r"Stellar AI Director (opening|advanced|endgame|beyond endgame) "
            r"strategic resource recovery - (volatile_motes|exotic_gases|rare_crystals)",
            name,
        )
        if not recovery_match:
            continue
        phase, resource = recovery_match.groups()
        income_floor_match = re.search(
            rf"NOT\s*=\s*\{{\s*has_monthly_income\s*=\s*\{{\s*resource\s*=\s*{resource}"
            rf"\s+value\s*>\s*(-?\d+(?:\.\d+)?)\s*\}}\s*\}}",
            block,
            flags=re.DOTALL,
        )
        stockpile_floor_match = re.search(
            rf"resource_stockpile_compare\s*=\s*\{{\s*resource\s*=\s*{resource}"
            rf"\s+value\s*<\s*(-?\d+(?:\.\d+)?)\s*\}}",
            block,
            flags=re.DOTALL,
        )
        if not income_floor_match or not stockpile_floor_match or income[resource] <= 0:
            raise ValueError(f"Incomplete strategic recovery subplan: {name}")
        min_years, max_years = _year_window(block)
        key = (phase, resource)
        if key in strategic_recovery:
            raise ValueError(f"Duplicate strategic recovery subplan: {name}")
        strategic_recovery[key] = StrategicRecoveryBand(
            name=name,
            phase=phase,
            resource=resource,
            min_years=min_years,
            max_years=max_years,
            income_floor=float(income_floor_match.group(1)),
            stockpile_floor=float(stockpile_floor_match.group(1)),
            target=income[resource],
        )
    return PdxPolicy(path, _income(base_region), subplans, strategic_recovery)


def _bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}


def _float(row: dict[str, str], key: str, default: float = 0.0) -> float:
    return float(row.get(key, "") or default)


def _int(row: dict[str, str], key: str, default: int = 0) -> int:
    return int(row.get(key, "") or default)


def _legacy_scenario(row: dict[str, str]) -> Scenario:
    income = {resource: _float(row, f"income_{resource}") for resource in LEGACY_RESOURCES}
    income.update({resource: 0.0 for resource in STRATEGIC})
    stockpile = {resource: _float(row, f"stockpile_{resource}") for resource in ORDINARY}
    stockpile.update({resource: 0.0 for resource in STRATEGIC})
    increments = {resource: _float(row, f"increment_{resource}") for resource in LEGACY_RESOURCES}
    increments.update({resource: 0.0 for resource in STRATEGIC})
    phase = row["phase"]
    return Scenario(
        name=row["scenario"],
        phase=phase,
        years_passed=PHASE_YEARS[phase],
        months=int(row["months"]),
        investments_per_month=int(row["investments_per_month"]),
        strategic_project_starts_per_month=0,
        aggressive_expansion=_bool(row["aggressive_expansion"]),
        at_war=_bool(row["at_war"]),
        bio_ships=_bool(row["bio_ships"]),
        control=True,
        income=income,
        stockpile=stockpile,
        increments=increments,
        production={resource: 0.0 for resource in STRATEGIC},
        upkeep={resource: 0.0 for resource in STRATEGIC},
        upkeep_growth={resource: 0.0 for resource in STRATEGIC},
        strategic_available={resource: False for resource in STRATEGIC},
        strategic_deficit={resource: False for resource in STRATEGIC},
        strategic_max_projects={resource: 0 for resource in STRATEGIC},
        strategic_completion_delay_months=16,
        strategic_project_mineral_cost=500.0,
        strategic_project_energy_upkeep=3.0,
        market_currency_reserve=0.0,
        market_cost_per_resource_unit=65.0,
    )


def _strategic_scenario(row: dict[str, str], base: Scenario) -> Scenario:
    production = {resource: _float(row, f"production_{resource}") for resource in STRATEGIC}
    upkeep = {resource: _float(row, f"upkeep_{resource}") for resource in STRATEGIC}
    upkeep_growth = {resource: _float(row, f"upkeep_growth_{resource}") for resource in STRATEGIC}
    income = dict(base.income)
    stockpile = dict(base.stockpile)
    increments = dict(base.increments)
    for resource in STRATEGIC:
        income[resource] = production[resource] - upkeep[resource]
        stockpile[resource] = _float(row, f"stockpile_{resource}")
        increments[resource] = _float(row, f"increment_{resource}")
    delay = _int(row, "strategic_completion_delay_months", 16)
    if delay < 1:
        raise ValueError(f"{row['scenario']}: construction delay must be at least one month")
    return Scenario(
        name=row["scenario"],
        phase=base.phase,
        years_passed=_int(row, "years_passed", PHASE_YEARS[base.phase]),
        months=_int(row, "months", base.months),
        investments_per_month=base.investments_per_month,
        strategic_project_starts_per_month=_int(row, "strategic_project_starts_per_month", 1),
        aggressive_expansion=base.aggressive_expansion,
        at_war=base.at_war,
        bio_ships=base.bio_ships,
        control=False,
        income=income,
        stockpile=stockpile,
        increments=increments,
        production=production,
        upkeep=upkeep,
        upkeep_growth=upkeep_growth,
        strategic_available={resource: _bool(row[f"available_{resource}"]) for resource in STRATEGIC},
        strategic_deficit={resource: _bool(row[f"deficit_{resource}"]) for resource in STRATEGIC},
        strategic_max_projects={resource: _int(row, f"max_projects_{resource}") for resource in STRATEGIC},
        strategic_completion_delay_months=delay,
        strategic_project_mineral_cost=_float(row, "strategic_project_mineral_cost", 500.0),
        strategic_project_energy_upkeep=_float(row, "strategic_project_energy_upkeep", 3.0),
        market_currency_reserve=_float(row, "market_currency_reserve"),
        market_cost_per_resource_unit=_float(row, "market_cost_per_resource_unit", 65.0),
    )


def load_scenarios(path: Path = SCENARIOS, strategic_path: Path = STRATEGIC_SCENARIOS) -> list[Scenario]:
    with path.open(encoding="utf-8", newline="") as handle:
        controls = [_legacy_scenario(row) for row in csv.DictReader(handle)]
    if not strategic_path.exists():
        return controls
    by_name = {scenario.name: scenario for scenario in controls}
    with strategic_path.open(encoding="utf-8", newline="") as handle:
        strategic_rows = list(csv.DictReader(handle))
    strategic: list[Scenario] = []
    for row in strategic_rows:
        base_name = row["base_scenario"]
        if base_name not in by_name:
            raise ValueError(f"Unknown base scenario {base_name!r} for {row['scenario']}")
        strategic.append(_strategic_scenario(row, by_name[base_name]))
    return controls + strategic


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


def choose_investment(
    scenario: Scenario,
    policy: PdxPolicy,
    income: dict[str, float],
    stockpile: dict[str, float],
) -> tuple[str | None, dict[str, float]]:
    current_targets = targets(scenario, policy)
    scores: dict[str, float] = {}
    for resource in LEGACY_RESOURCES:
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

    viable = [resource for resource in LEGACY_RESOURCES if scenario.increments[resource] > 0]
    choice = max(viable, key=lambda resource: (scores[resource], resource == "research"))
    return (choice if scores[choice] > 0 else None), current_targets


def strategic_band_for_year(policy: PdxPolicy, years_passed: int, resource: str) -> StrategicRecoveryBand | None:
    matches = [
        band
        for band in policy.strategic_recovery.values()
        if band.resource == resource
        and years_passed >= band.min_years
        and (band.max_years is None or years_passed <= band.max_years)
    ]
    if len(matches) > 1:
        raise ValueError(f"Overlapping strategic recovery bands for {resource} at year {years_passed}")
    return matches[0] if matches else None


def strategic_recovery_triggered(
    scenario: Scenario,
    band: StrategicRecoveryBand | None,
    resource: str,
    income: float,
    stockpile: float,
) -> bool:
    return bool(
        band
        and scenario.strategic_available[resource]
        and (
            scenario.strategic_deficit[resource]
            or income <= band.income_floor
            or stockpile < band.stockpile_floor
        )
    )


def _queue_strategic_projects(
    *,
    scenario: Scenario,
    month: int,
    bands: dict[str, StrategicRecoveryBand | None],
    income: dict[str, float],
    stockpile: dict[str, float],
    pending: dict[str, list[int]],
    investments: Counter[str],
) -> tuple[Counter[str], float]:
    starts = Counter()
    mineral_cost = 0.0
    remaining_starts = scenario.strategic_project_starts_per_month
    while remaining_starts > 0:
        candidates: list[tuple[float, int, str]] = []
        for order, resource in enumerate(STRATEGIC):
            band = bands[resource]
            if not strategic_recovery_triggered(
                scenario, band, resource, income[resource], stockpile[resource]
            ):
                continue
            increment = scenario.increments[resource]
            effective_income = income[resource] + len(pending[resource]) * increment
            if (
                not band
                or increment <= 0
                or effective_income + EPSILON >= band.target
                or investments[resource] >= scenario.strategic_max_projects[resource]
            ):
                continue
            candidates.append(((band.target - effective_income) / max(band.target, 1.0), -order, resource))
        if not candidates:
            break
        if stockpile["minerals"] + EPSILON < scenario.strategic_project_mineral_cost:
            break
        _, _, resource = max(candidates)
        pending[resource].append(month + scenario.strategic_completion_delay_months)
        investments[resource] += 1
        starts[resource] += 1
        remaining_starts -= 1
        stockpile["minerals"] -= scenario.strategic_project_mineral_cost
        mineral_cost += scenario.strategic_project_mineral_cost
    return starts, mineral_cost


def simulate(scenario: Scenario, policy: PdxPolicy | None = None) -> tuple[list[dict[str, object]], dict[str, object]]:
    policy = policy or load_pdx_policy()
    income = dict(scenario.income)
    production = dict(scenario.production)
    upkeep = dict(scenario.upkeep)
    stockpile = {resource: max(0.0, scenario.stockpile[resource]) for resource in FLOW_RESOURCES}
    raw_stockpile = dict(scenario.stockpile)
    minimum_stockpile = dict(stockpile)
    minimum_raw_stockpile = {resource: raw_stockpile[resource] for resource in STRATEGIC}
    bridge_required = {resource: 0.0 for resource in STRATEGIC}
    depletion_month: dict[str, int | None] = {resource: None for resource in STRATEGIC}
    months_to_nonnegative: dict[str, int | None] = {
        resource: (0 if income[resource] >= 0 else None) for resource in STRATEGIC
    }
    recovery_required = {
        resource: bool(scenario.strategic_deficit[resource] or income[resource] < 0) for resource in STRATEGIC
    }
    pending = {resource: [] for resource in STRATEGIC}
    investments: Counter[str] = Counter()
    completions: Counter[str] = Counter()
    total_construction_minerals = 0.0
    total_completion_energy_upkeep = 0.0
    timeline: list[dict[str, object]] = []

    for month in range(1, scenario.months + 1):
        completed_now: Counter[str] = Counter()
        for resource in STRATEGIC:
            due = sum(1 for due_month in pending[resource] if due_month <= month)
            if due:
                pending[resource] = [due_month for due_month in pending[resource] if due_month > month]
                production[resource] += due * scenario.increments[resource]
                completions[resource] += due
                completed_now[resource] += due
                added_energy_upkeep = due * scenario.strategic_project_energy_upkeep
                income["energy"] -= added_energy_upkeep
                total_completion_energy_upkeep += added_energy_upkeep

        for resource in STRATEGIC:
            upkeep[resource] += scenario.upkeep_growth[resource]
            income[resource] = production[resource] - upkeep[resource]
            if months_to_nonnegative[resource] is None and income[resource] >= 0:
                months_to_nonnegative[resource] = month

        bands = {
            resource: strategic_band_for_year(policy, scenario.years_passed, resource)
            for resource in STRATEGIC
        }
        active = {
            resource: strategic_recovery_triggered(
                scenario, bands[resource], resource, income[resource], stockpile[resource]
            )
            for resource in STRATEGIC
        }
        for resource in STRATEGIC:
            recovery_required[resource] = recovery_required[resource] or active[resource]

        started_now, construction_minerals = _queue_strategic_projects(
            scenario=scenario,
            month=month,
            bands=bands,
            income=income,
            stockpile=stockpile,
            pending=pending,
            investments=investments,
        )
        total_construction_minerals += construction_minerals
        raw_stockpile["minerals"] = stockpile["minerals"]

        for _ in range(scenario.investments_per_month):
            resource, _ = choose_investment(scenario, policy, income, stockpile)
            if resource is None:
                break
            income[resource] += scenario.increments[resource]
            investments[resource] += 1

        for resource in ORDINARY:
            stockpile[resource] = max(0.0, stockpile[resource] + income[resource])
            raw_stockpile[resource] = stockpile[resource]
            minimum_stockpile[resource] = min(minimum_stockpile[resource], stockpile[resource])
        for resource in STRATEGIC:
            raw_stockpile[resource] += income[resource]
            stockpile[resource] = max(0.0, raw_stockpile[resource])
            minimum_stockpile[resource] = min(minimum_stockpile[resource], stockpile[resource])
            minimum_raw_stockpile[resource] = min(minimum_raw_stockpile[resource], raw_stockpile[resource])
            bridge_required[resource] = max(bridge_required[resource], -raw_stockpile[resource], 0.0)
            if depletion_month[resource] is None and raw_stockpile[resource] < 0:
                depletion_month[resource] = month

        current_targets = targets(scenario, policy)
        ordinary_positive = sum(max(income[resource], 0.0) for resource in ORDINARY)
        row: dict[str, object] = {
            "scenario": scenario.name,
            "month": month,
            **{f"income_{resource}": round(income[resource], 3) for resource in LEGACY_RESOURCES},
            **{f"target_{resource}": round(current_targets[resource], 3) for resource in LEGACY_RESOURCES},
            "research_to_ordinary_ratio": round(income["research"] / max(ordinary_positive, 1.0), 4),
        }
        for resource in STRATEGIC:
            band = bands[resource]
            row.update(
                {
                    f"recovery_band_{resource}": band.phase if band else "",
                    f"recovery_active_{resource}": active[resource],
                    f"production_{resource}": round(production[resource], 3),
                    f"upkeep_{resource}": round(upkeep[resource], 3),
                    f"income_{resource}": round(income[resource], 3),
                    f"target_{resource}": round(band.target, 3) if band else 0.0,
                    f"pending_output_{resource}": round(len(pending[resource]) * scenario.increments[resource], 3),
                    f"stockpile_{resource}": round(stockpile[resource], 3),
                    f"raw_stockpile_{resource}": round(raw_stockpile[resource], 3),
                    f"projects_started_{resource}": started_now[resource],
                    f"projects_completed_{resource}": completed_now[resource],
                    f"bridge_required_{resource}": round(bridge_required[resource], 3),
                }
            )
        row["construction_minerals"] = round(construction_minerals, 3)
        row["completion_energy_upkeep"] = round(
            sum(completed_now.values()) * scenario.strategic_project_energy_upkeep, 3
        )
        timeline.append(row)

    ordinary_positive = sum(max(income[resource], 0.0) for resource in ORDINARY)
    final_targets = targets(scenario, policy)
    support_safe = (
        income["energy"] >= final_targets["energy"]
        and income["consumer_goods"] >= final_targets["consumer_goods"]
    )
    summary: dict[str, object] = {
        "scenario": scenario.name,
        "phase": scenario.phase,
        "months": scenario.months,
        "research_to_ordinary_ratio": round(income["research"] / max(ordinary_positive, 1.0), 4),
        "ratio_target_met": income["research"] >= RESEARCH_RATIO * ordinary_positive,
        "food_overproduction": income["food"] > (100 if scenario.bio_ships else 50),
        "support_safe": support_safe,
        "pdx_source": str(policy.source.relative_to(ROOT)).replace("\\", "/"),
        **{f"final_income_{resource}": round(income[resource], 3) for resource in LEGACY_RESOURCES},
        **{f"investment_{resource}": investments[resource] for resource in LEGACY_RESOURCES},
        **{f"minimum_stockpile_{resource}": round(minimum_stockpile[resource], 3) for resource in ORDINARY},
    }
    eventual_results: list[bool] = []
    construction_survival: list[bool] = []
    bridge_market_costs: list[float] = []
    for resource in STRATEGIC:
        band = strategic_band_for_year(policy, scenario.years_passed, resource)
        effective_income = income[resource] + len(pending[resource]) * scenario.increments[resource]
        final_triggered = strategic_recovery_triggered(
            scenario, band, resource, income[resource], stockpile[resource]
        )
        target_reached = bool(
            not recovery_required[resource]
            or (band is not None and effective_income + EPSILON >= band.target)
        )
        eventual_recovery = bool(
            not recovery_required[resource]
            or (
                band is not None
                and scenario.strategic_available[resource]
                and (
                    (final_triggered and effective_income + EPSILON >= band.target)
                    or (not final_triggered and income[resource] > 0)
                )
            )
        )
        survives = bridge_required[resource] <= EPSILON
        bridge_market_cost = bridge_required[resource] * scenario.market_cost_per_resource_unit
        bridge_affordable = survives or scenario.market_currency_reserve + EPSILON >= bridge_market_cost
        capacity_exhausted = bool(
            recovery_required[resource]
            and band is not None
            and effective_income + EPSILON < band.target
            and investments[resource] >= scenario.strategic_max_projects[resource]
        )
        eventual_results.append(eventual_recovery)
        construction_survival.append(survives)
        bridge_market_costs.append(bridge_market_cost)
        summary.update(
            {
                f"final_production_{resource}": round(production[resource], 3),
                f"final_upkeep_{resource}": round(upkeep[resource], 3),
                f"final_income_{resource}": round(income[resource], 3),
                f"strategic_target_{resource}": round(band.target, 3) if band else 0.0,
                f"investment_{resource}": investments[resource],
                f"completed_projects_{resource}": completions[resource],
                f"pending_projects_{resource}": len(pending[resource]),
                f"months_to_nonnegative_{resource}": months_to_nonnegative[resource],
                f"minimum_stockpile_{resource}": round(minimum_stockpile[resource], 3),
                f"minimum_raw_stockpile_{resource}": round(minimum_raw_stockpile[resource], 3),
                f"bridge_required_{resource}": round(bridge_required[resource], 3),
                f"bridge_market_cost_{resource}": round(bridge_market_cost, 3),
                f"bridge_affordable_{resource}": bridge_affordable,
                f"depletion_month_{resource}": depletion_month[resource],
                f"recovery_required_{resource}": recovery_required[resource],
                f"target_reached_{resource}": target_reached,
                f"eventual_recovery_{resource}": eventual_recovery,
                f"construction_only_survives_{resource}": survives,
                f"capacity_exhausted_{resource}": capacity_exhausted,
            }
        )
    total_bridge_market_cost = sum(bridge_market_costs)
    total_bridge_affordable = (
        total_bridge_market_cost <= EPSILON
        or scenario.market_currency_reserve + EPSILON >= total_bridge_market_cost
    )
    summary.update(
        {
            "strategic_eventual_recovery": all(eventual_results),
            "strategic_construction_only_survives": all(construction_survival),
            "strategic_market_bridge_affordable": total_bridge_affordable,
            "strategic_recovery_financed": all(eventual_results) and total_bridge_affordable,
            "strategic_safe": all(eventual_results) and total_bridge_affordable,
            "ordinary_model_safe": summary["ratio_target_met"] and support_safe,
            "total_strategic_construction_minerals": round(total_construction_minerals, 3),
            "total_strategic_completion_energy_upkeep": round(total_completion_energy_upkeep, 3),
            "market_currency_reserve": round(scenario.market_currency_reserve, 3),
            "market_cost_per_resource_unit": round(scenario.market_cost_per_resource_unit, 3),
            "total_bridge_market_cost": round(total_bridge_market_cost, 3),
        }
    )
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
