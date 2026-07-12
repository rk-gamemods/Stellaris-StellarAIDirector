"""Deterministic economic-band simulator for Stellar AI Director.

This is an offline design tool. It does not generate or modify Stellaris mod
files. Run without arguments from the repository root.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import tempfile
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

try:
    from .stellar_ai_economic_model import (
        DEFICIT_ONLY_PLUS_ONE,
        DEFICIT_ONLY_PLUS_TWO,
        FAILED_C9,
        PARENT_ONLY,
        PREZERO_RUNWAY_PLUS_ONE,
        EconomicState,
        FactSet,
        FeasibilityCode,
        Lane,
        PendingProject,
        PolicyMode,
        PolicyRun,
        PolicyVariant,
        Project,
        QuantityVector,
        Truth,
        build_active_priority_set,
        compare_policy_variants,
        evaluate_bundle_feasibility,
        evaluate_policy_activation,
        find_feasible_bundles,
        select_bundle,
    )
except ImportError:  # Direct ``python tools/simulate_stellar_ai_economy.py``.
    from stellar_ai_economic_model import (  # type: ignore[no-redef]
        DEFICIT_ONLY_PLUS_ONE,
        DEFICIT_ONLY_PLUS_TWO,
        FAILED_C9,
        PARENT_ONLY,
        PREZERO_RUNWAY_PLUS_ONE,
        EconomicState,
        FactSet,
        FeasibilityCode,
        Lane,
        PendingProject,
        PolicyMode,
        PolicyRun,
        PolicyVariant,
        Project,
        QuantityVector,
        Truth,
        build_active_priority_set,
        compare_policy_variants,
        evaluate_bundle_feasibility,
        evaluate_policy_activation,
        find_feasible_bundles,
        select_bundle,
    )


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research" / "stellar-ai"
SCENARIOS = RESEARCH / "stellar-ai-economic-model-scenarios-2026-07-11.csv"
TIMELINE = RESEARCH / "stellar-ai-economic-model-timeline-2026-07-11.csv"
SUMMARY = RESEARCH / "stellar-ai-economic-model-summary-2026-07-11.csv"
PDX_PLAN = ROOT / "mods" / "StellarAIDirector" / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
STRATEGIC_RECOVERY_PLAN = (
    ROOT
    / "mods"
    / "StellarAIDirector"
    / "common"
    / "economic_plans"
    / "zzzz_staid_21_strategic_resource_deficit_recovery.txt"
)
MODEL_CORE = ROOT / "tools" / "stellar_ai_economic_model.py"
MODEL_CHECKPOINTS = RESEARCH / "stellar-ai-director-economic-checkpoints.csv"
MODEL_CANDIDATES = RESEARCH / "stellar-ai-director-economic-lane-candidates.csv"
MODEL_POLICIES = RESEARCH / "stellar-ai-director-economic-policy-variants.csv"
MODEL_ACTIVATION_CASES = RESEARCH / "stellar-ai-director-economic-policy-activation-cases.csv"
ACTIVE_PRIORITY = RESEARCH / "stellar-ai-director-active-priority-snapshot.csv"
CONCURRENT_FEASIBILITY = RESEARCH / "stellar-ai-director-concurrent-spending-feasibility.csv"
LANE_STARVATION = RESEARCH / "stellar-ai-director-lane-starvation.csv"
ACTIVATION_MATRIX = RESEARCH / "stellar-ai-director-policy-activation-matrix.csv"
POLICY_COUNTERFACTUAL = RESEARCH / "stellar-ai-director-policy-counterfactual.csv"
MODEL_PROVENANCE = RESEARCH / "stellar-ai-director-economic-model-provenance.json"
COMPARATIVE_REPORT_ATTESTATION = (
    RESEARCH / "stellar-ai-director-comparative-report-attestation.json"
)
COMPARATIVE_REPORT = Path.home() / "Downloads" / "stellar_ai_director_comparative_recovery_plan.md"
COMPARATIVE_REPORT_EXPECTED_SHA256 = (
    "e41cc8d6a5a933a8b2507d496057ec6cb7045c0f5611d42208fc4e305d495039"
)

MODEL_SCHEMA_VERSION = 1
MODEL_EVIDENCE_CLASS = "deterministic_model_not_runtime_proof"
PROVENANCE_HASH_NORMALIZED_TEXT_LF = "normalized_lf_text_sha256_v1"
PROVENANCE_HASH_RAW_BYTES = "raw_bytes_sha256_v1"
COMPARATIVE_REPORT_AVAILABLE = "available_verified"
COMPARATIVE_REPORT_ATTESTED_ONLY = "absent_attestation_only"
STRATEGIC_RESOURCES = ("volatile_motes", "exotic_gases", "rare_crystals")
MODEL_POLICIES_ORDERED = (
    PARENT_ONLY,
    DEFICIT_ONLY_PLUS_ONE,
    DEFICIT_ONLY_PLUS_TWO,
    PREZERO_RUNWAY_PLUS_ONE,
    FAILED_C9,
)
MODEL_OUTPUTS = (
    TIMELINE,
    SUMMARY,
    ACTIVE_PRIORITY,
    CONCURRENT_FEASIBILITY,
    LANE_STARVATION,
    ACTIVATION_MATRIX,
    POLICY_COUNTERFACTUAL,
)

ORDINARY = ("energy", "minerals", "food", "consumer_goods", "alloys", "unity", "trade")
RESOURCES = ORDINARY + ("research",)
RESEARCH_RATIO = 2.0

PHASE_SUBPLANS = {
    "early": ("Stellar AI Director safe research baseline", "Stellar AI Director opening direct research route"),
    "mid": ("Stellar AI Director safe research baseline", "Stellar AI Director primary research economy"),
    "late": ("Stellar AI Director safe research baseline", "Stellar AI Director primary research economy"),
}
CONQUEST_SUBPLAN = "Stellar AI Director militarist conquest fleet reserve"


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
    if scenario.aggressive_expansion:
        selected.append(CONQUEST_SUBPLAN)
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


def serialize_csv_rows(
    rows: list[dict[str, object]],
    fields: tuple[str, ...] | None = None,
) -> bytes:
    if not rows:
        raise ValueError("CSV rows must not be empty")
    fieldnames = fields or tuple(rows[0])
    expected = set(fieldnames)
    for index, row in enumerate(rows):
        if set(row) != expected:
            raise ValueError(
                f"CSV row {index} schema mismatch: expected {fieldnames!r}, "
                f"got {tuple(row)!r}"
            )
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(
        handle,
        fieldnames=fieldnames,
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(serialize_csv_rows(rows))


@dataclass(frozen=True)
class ModelCheckpoint:
    scenario_id: str
    description: str
    horizon_months: int
    state: EconomicState
    parent_winner_verified: bool
    evidence_ref: str


@dataclass(frozen=True)
class ModelCandidate:
    scenario_id: str
    project: Project
    legal: bool
    consumer_surface: str
    emergency_class: str
    parent_provenance: str
    parent_winner_verified: bool


@dataclass(frozen=True)
class StrategicRecoveryRule:
    resource: str
    set_name: str
    income: Decimal


def _split_values(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split("|") if item.strip())


def _strict_bool(value: str, *, label: str) -> bool:
    if value not in {"true", "false"}:
        raise ValueError(f"{label}: expected strict true/false, got {value!r}")
    return value == "true"


def _validate_fixture_id(value: str, *, label: str) -> str:
    if not re.fullmatch(r"[a-z0-9_]+", value):
        raise ValueError(f"{label}: expected [a-z0-9_]+, got {value!r}")
    return value


def _json_mapping(value: str, *, label: str) -> dict[str, object]:
    try:
        result = json.loads(value or "{}")
    except json.JSONDecodeError as error:
        raise ValueError(f"{label}: invalid JSON: {error}") from error
    if not isinstance(result, dict):
        raise ValueError(f"{label}: expected a JSON object")
    return result


def _json_list(value: str, *, label: str) -> list[object]:
    try:
        result = json.loads(value or "[]")
    except json.JSONDecodeError as error:
        raise ValueError(f"{label}: invalid JSON: {error}") from error
    if not isinstance(result, list):
        raise ValueError(f"{label}: expected a JSON list")
    return result


def _quantities(value: str, *, label: str) -> QuantityVector:
    return QuantityVector.from_mapping(_json_mapping(value, label=label))


def _fact_set(value: str, *, label: str) -> FactSet:
    raw = _json_mapping(value, label=label)
    try:
        return FactSet.from_mapping({key: Truth(str(item).lower()) for key, item in raw.items()})
    except ValueError as error:
        raise ValueError(f"{label}: invalid tri-state fact: {error}") from error


def _read_fixture(path: Path, expected_fields: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        actual = tuple(reader.fieldnames or ())
        if actual != expected_fields:
            raise ValueError(f"{path}: expected header {expected_fields!r}, got {actual!r}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path}: fixture must contain at least one row")
    return rows


CHECKPOINT_FIELDS = (
    "scenario_id", "description", "horizon_months", "stockpile_json",
    "capacity_json", "earned_income_json", "market_income_json",
    "active_upkeep_json", "budgets_json", "queue_capacity_json",
    "queue_used_json", "slot_capacity_json", "slot_used_json",
    "job_capacity_json", "job_used_json", "influence", "deficit_status_json",
    "unlocked_resources", "gates", "pending_projects_json",
    "parent_winner_verified", "evidence_ref",
)
CANDIDATE_FIELDS = (
    "scenario_id", "project_id", "lane", "base_priority", "one_time_cost_json",
    "budget_cost_json", "influence_cost", "queue", "queue_slots",
    "slot_cost_json", "job_cost_json", "duration_months",
    "completion_income_json", "completion_upkeep_json", "required_gates",
    "forbidden_gates", "add_gates", "remove_gates", "strategic_resource",
    "repeatable", "legal", "consumer_surface", "emergency_class",
    "parent_provenance", "parent_winner_verified",
)
POLICY_FIELDS = (
    "policy_id", "source_class", "mode", "income_pressure", "priority_bonus",
    "runway_threshold_months", "failed_income_target", "gameplay_plan",
    "evidence_ref",
)
ACTIVATION_CASE_FIELDS = (
    "case_id", "case_family", "resource", "stockpile", "capacity",
    "earned_income",
    "market_income", "active_upkeep", "deficit_status", "unlocked",
    "expected_active_policies", "risk_label", "evidence_ref",
)

LEGACY_TIMELINE_FIELDS = (
    "scenario",
    "month",
    *(f"income_{resource}" for resource in RESOURCES),
    *(f"target_{resource}" for resource in RESOURCES),
    "research_to_ordinary_ratio",
)
LEGACY_SUMMARY_FIELDS = (
    "scenario",
    "phase",
    "months",
    "research_to_ordinary_ratio",
    "ratio_target_met",
    "food_overproduction",
    "support_safe",
    "pdx_source",
    *(f"final_income_{resource}" for resource in RESOURCES),
    *(f"investment_{resource}" for resource in RESOURCES),
    *(f"minimum_stockpile_{resource}" for resource in ORDINARY),
)
ACTIVE_PRIORITY_OUTPUT_FIELDS = (
    "schema_version", "source_provenance_id", "evidence_class", "scenario_id",
    "policy_id", "horizon_months", "project_id", "lane", "consumer_surface",
    "emergency_class", "activation_state", "activation_reasons",
    "requested_income", "remaining_pressure", "priority", "legal",
    "parent_winner_verified",
    "affordable_now", "feasibility_reasons", "one_time_cost_json",
    "monthly_upkeep_json", "completion_income_json", "queue", "required_gates",
    "parent_provenance", "evidence_ref",
)
CONCURRENT_FEASIBILITY_OUTPUT_FIELDS = (
    "schema_version", "source_provenance_id", "evidence_class", "scenario_id",
    "policy_id", "horizon_months", "bundle_id", "project_ids", "lanes",
    "candidate_count", "resource_affordable", "budget_feasible",
    "queue_feasible", "slot_feasible", "job_feasible", "influence_feasible",
    "runway_preserved", "gate_feasible", "affordable", "feasible",
    "selected_by_policy", "major_lane_count", "reasons_json",
)
LANE_STARVATION_OUTPUT_FIELDS = (
    "schema_version", "source_provenance_id", "evidence_class", "scenario_id",
    "policy_id", "horizon_months", "lane", "starved",
    "months_affordable_unselected", "starvation_months", "threshold_months",
    "shared_bottlenecks", "counterfactual_selected_months", "classification",
)
ACTIVATION_MATRIX_OUTPUT_FIELDS = (
    "schema_version", "source_provenance_id", "evidence_class", "case_id",
    "case_family", "policy_id", "resource", "stockpile", "capacity",
    "earned_income", "market_income", "active_upkeep", "net_earned_income",
    "actual_deficit", "unlocked", "activation_result", "activation_reasons",
    "requested_income", "remaining_pressure", "runway_months",
    "expected_active", "expectation_met",
    "unsafe_predeficit_activation", "earned_income_recovered",
    "market_stock_only", "risk_label", "evidence_ref",
)
POLICY_COUNTERFACTUAL_OUTPUT_FIELDS = (
    "schema_version", "source_provenance_id", "evidence_class", "scenario_id",
    "policy_id", "baseline_policy_id", "horizon_months",
    "unsafe_predeficit_activation_count", "foregone_affordable_action_count",
    "major_lanes_progressed",
    *(
        field
        for resource in STRATEGIC_RESOURCES
        for field in (
            f"deficit_exit_month_{resource}",
            f"durable_strict_positive_month_{resource}",
            f"durable_earned_recovery_month_{resource}",
            f"earned_income_recovered_{resource}",
            f"market_stock_only_{resource}",
            f"minimum_stockpile_{resource}",
            f"producer_starts_{resource}",
            f"producer_completions_{resource}",
        )
    ),
    *(field for lane in Lane for field in (f"actions_{lane.value}", f"starvation_months_{lane.value}")),
    "unsafe", "unsafe_reason_codes",
)
MODEL_OUTPUT_SCHEMAS = {
    TIMELINE: LEGACY_TIMELINE_FIELDS,
    SUMMARY: LEGACY_SUMMARY_FIELDS,
    ACTIVE_PRIORITY: ACTIVE_PRIORITY_OUTPUT_FIELDS,
    CONCURRENT_FEASIBILITY: CONCURRENT_FEASIBILITY_OUTPUT_FIELDS,
    LANE_STARVATION: LANE_STARVATION_OUTPUT_FIELDS,
    ACTIVATION_MATRIX: ACTIVATION_MATRIX_OUTPUT_FIELDS,
    POLICY_COUNTERFACTUAL: POLICY_COUNTERFACTUAL_OUTPUT_FIELDS,
}


PENDING_PROJECT_FIELDS = {
    "project_id",
    "lane",
    "completes_at_month",
    "completion_income",
    "completion_upkeep",
    "strategic_resource",
}


def _pending_projects(value: str, *, scenario_id: str) -> tuple[PendingProject, ...]:
    pending: list[PendingProject] = []
    seen: set[str] = set()
    for index, raw in enumerate(
        _json_list(value, label=f"{scenario_id}.pending_projects")
    ):
        label = f"{scenario_id}.pending_projects[{index}]"
        if not isinstance(raw, dict) or set(raw) != PENDING_PROJECT_FIELDS:
            actual = sorted(raw) if isinstance(raw, dict) else type(raw).__name__
            raise ValueError(
                f"{label}: expected exact keys {sorted(PENDING_PROJECT_FIELDS)!r}, "
                f"got {actual!r}"
            )
        project_id = _validate_fixture_id(str(raw["project_id"]), label=f"{label}.project_id")
        if project_id in seen:
            raise ValueError(f"{label}: duplicate pending project ID {project_id!r}")
        seen.add(project_id)
        try:
            lane = Lane(str(raw["lane"]))
        except ValueError as error:
            raise ValueError(f"{label}: unknown lane {raw['lane']!r}") from error
        income = raw["completion_income"]
        upkeep = raw["completion_upkeep"]
        if not isinstance(income, dict) or not isinstance(upkeep, dict):
            raise ValueError(f"{label}: completion vectors must be JSON objects")
        strategic_resource = str(raw["strategic_resource"]) or None
        project = Project(
            project_id=project_id,
            lane=lane,
            base_priority=0,
            completion_income=QuantityVector.from_mapping(income),
            completion_upkeep=QuantityVector.from_mapping(upkeep),
            strategic_resource=strategic_resource,
        )
        pending.append(
            PendingProject(
                project=project,
                completes_at_month=int(raw["completes_at_month"]),
            )
        )
    return tuple(sorted(pending, key=lambda item: item.project.project_id))


def load_model_checkpoints(path: Path = MODEL_CHECKPOINTS) -> tuple[ModelCheckpoint, ...]:
    checkpoints: list[ModelCheckpoint] = []
    seen: set[str] = set()
    for row in _read_fixture(path, CHECKPOINT_FIELDS):
        scenario_id = _validate_fixture_id(
            row["scenario_id"], label=f"{path}.scenario_id"
        )
        if scenario_id in seen:
            raise ValueError(f"{path}: duplicate scenario_id {scenario_id!r}")
        seen.add(scenario_id)
        horizon = int(row["horizon_months"])
        if horizon not in {12, 24}:
            raise ValueError(f"{scenario_id}: horizon_months must be 12 or 24")
        checkpoints.append(
            ModelCheckpoint(
                scenario_id=scenario_id,
                description=row["description"],
                horizon_months=horizon,
                state=EconomicState(
                    stockpile=_quantities(row["stockpile_json"], label=f"{scenario_id}.stockpile"),
                    capacity=_quantities(row["capacity_json"], label=f"{scenario_id}.capacity"),
                    earned_income=_quantities(row["earned_income_json"], label=f"{scenario_id}.earned_income"),
                    market_income=_quantities(row["market_income_json"], label=f"{scenario_id}.market_income"),
                    active_upkeep=_quantities(row["active_upkeep_json"], label=f"{scenario_id}.active_upkeep"),
                    budgets=_quantities(row["budgets_json"], label=f"{scenario_id}.budgets"),
                    queue_capacity=_quantities(row["queue_capacity_json"], label=f"{scenario_id}.queue_capacity"),
                    queue_used=_quantities(row["queue_used_json"], label=f"{scenario_id}.queue_used"),
                    slot_capacity=_quantities(row["slot_capacity_json"], label=f"{scenario_id}.slot_capacity"),
                    slot_used=_quantities(row["slot_used_json"], label=f"{scenario_id}.slot_used"),
                    job_capacity=_quantities(row["job_capacity_json"], label=f"{scenario_id}.job_capacity"),
                    job_used=_quantities(row["job_used_json"], label=f"{scenario_id}.job_used"),
                    influence=Decimal(row["influence"]),
                    deficit_status=_fact_set(row["deficit_status_json"], label=f"{scenario_id}.deficit_status"),
                    unlocked_resources=frozenset(_split_values(row["unlocked_resources"])),
                    gates=frozenset(_split_values(row["gates"])),
                    pending=_pending_projects(
                        row["pending_projects_json"], scenario_id=scenario_id
                    ),
                ),
                parent_winner_verified=_strict_bool(
                    row["parent_winner_verified"],
                    label=f"{scenario_id}.parent_winner_verified",
                ),
                evidence_ref=row["evidence_ref"],
            )
        )
    return tuple(checkpoints)


def load_model_candidates(path: Path = MODEL_CANDIDATES) -> tuple[ModelCandidate, ...]:
    candidates: list[ModelCandidate] = []
    seen: set[tuple[str, str]] = set()
    for row in _read_fixture(path, CANDIDATE_FIELDS):
        key = (
            _validate_fixture_id(row["scenario_id"], label=f"{path}.scenario_id"),
            _validate_fixture_id(row["project_id"], label=f"{path}.project_id"),
        )
        if key in seen:
            raise ValueError(f"{path}: duplicate candidate key {key!r}")
        seen.add(key)
        try:
            lane = Lane(row["lane"])
        except ValueError as error:
            raise ValueError(f"{key}: unknown lane {row['lane']!r}") from error
        candidates.append(
            ModelCandidate(
                scenario_id=row["scenario_id"],
                project=Project(
                    project_id=row["project_id"],
                    lane=lane,
                    base_priority=Decimal(row["base_priority"]),
                    one_time_cost=_quantities(row["one_time_cost_json"], label=f"{key}.one_time_cost"),
                    budget_cost=_quantities(row["budget_cost_json"], label=f"{key}.budget_cost"),
                    influence_cost=Decimal(row["influence_cost"] or "0"),
                    queue=row["queue"] or None,
                    queue_slots=Decimal(row["queue_slots"] or "1"),
                    slot_cost=_quantities(row["slot_cost_json"], label=f"{key}.slot_cost"),
                    job_cost=_quantities(row["job_cost_json"], label=f"{key}.job_cost"),
                    duration_months=int(row["duration_months"]),
                    completion_income=_quantities(row["completion_income_json"], label=f"{key}.completion_income"),
                    completion_upkeep=_quantities(row["completion_upkeep_json"], label=f"{key}.completion_upkeep"),
                    required_gates=frozenset(_split_values(row["required_gates"])),
                    forbidden_gates=frozenset(_split_values(row["forbidden_gates"])),
                    add_gates=frozenset(_split_values(row["add_gates"])),
                    remove_gates=frozenset(_split_values(row["remove_gates"])),
                    strategic_resource=row["strategic_resource"] or None,
                    repeatable=_strict_bool(
                        row["repeatable"], label=f"{key}.repeatable"
                    ),
                ),
                legal=_strict_bool(row["legal"], label=f"{key}.legal"),
                consumer_surface=row["consumer_surface"],
                emergency_class=row["emergency_class"],
                parent_provenance=row["parent_provenance"],
                parent_winner_verified=_strict_bool(
                    row["parent_winner_verified"],
                    label=f"{key}.parent_winner_verified",
                ),
            )
        )
    return tuple(candidates)


def _decimal_text(value: Decimal | None) -> str:
    if value is None:
        return ""
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _vector_json(vector: QuantityVector) -> str:
    return json.dumps(
        {key: _decimal_text(value) for key, value in vector.values},
        sort_keys=True,
        separators=(",", ":"),
    )


def _remove_named_blocks(text: str, key: str) -> tuple[list[str], str]:
    pattern = re.compile(rf"(?m)^\s*{re.escape(key)}\s*=\s*\{{")
    spans: list[tuple[int, int]] = []
    blocks: list[str] = []
    for match in pattern.finditer(text):
        block, end = _braced_block(text, match.end() - 1)
        spans.append((match.start(), end))
        blocks.append(block)
    remainder = text
    for start, end in reversed(spans):
        remainder = remainder[:start] + remainder[end:]
    return blocks, remainder


def parse_strategic_recovery_plan(
    path: Path = STRATEGIC_RECOVERY_PLAN,
) -> tuple[StrategicRecoveryRule, ...]:
    text = re.sub(r"(?m)#.*$", "", path.read_text(encoding="utf-8-sig"))
    plan_matches = list(
        re.finditer(r"(?m)^\s*basic_economy_plan\s*=\s*\{", text)
    )
    if len(plan_matches) != 1:
        raise ValueError(f"{path}: expected exactly one basic_economy_plan")
    plan_match = plan_matches[0]
    plan, plan_end = _braced_block(text, plan_match.end() - 1)
    outside = text[: plan_match.start()] + text[plan_end:]
    if outside.strip():
        raise ValueError(f"{path}: unexpected content outside basic_economy_plan")
    subplans, plan_remainder = _remove_named_blocks(plan, "subplan")
    if len(subplans) != 3 or plan_remainder.strip():
        raise ValueError(
            f"{path}: expected exactly three subplans and no other plan keys"
        )

    expected_names = {
        "volatile_motes": "Stellar AI Director actual-deficit recovery - volatile motes",
        "exotic_gases": "Stellar AI Director actual-deficit recovery - exotic gases",
        "rare_crystals": "Stellar AI Director actual-deficit recovery - rare crystals",
    }
    rules: dict[str, StrategicRecoveryRule] = {}
    for index, block in enumerate(subplans):
        label = f"{path}: subplan[{index}]"
        if re.search(r"(?m)^\s*scaling\s*=", block):
            raise ValueError(f"{label}: recovery subplans must be non-scaling")
        optional = re.findall(r"(?m)^\s*optional\s*=\s*(\w+)\s*$", block)
        names = re.findall(r'(?m)^\s*set_name\s*=\s*"([^"]+)"\s*$', block)
        potential_blocks, remainder = _remove_named_blocks(block, "potential")
        income_blocks, remainder = _remove_named_blocks(remainder, "income")
        remainder = re.sub(r"(?m)^\s*optional\s*=\s*yes\s*$", "", remainder)
        remainder = re.sub(
            r'(?m)^\s*set_name\s*=\s*"[^"]+"\s*$', "", remainder
        )
        if (
            optional != ["yes"]
            or len(names) != 1
            or len(potential_blocks) != 1
            or len(income_blocks) != 1
            or remainder.strip()
        ):
            raise ValueError(
                f"{label}: expected only optional=yes, set_name, potential, and income"
            )
        potential_match = re.fullmatch(
            r"\s*has_deficit\s*=\s*([a-z0-9_]+)\s*", potential_blocks[0]
        )
        income_match = re.fullmatch(
            r"\s*([a-z0-9_]+)\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*",
            income_blocks[0],
        )
        if not potential_match or not income_match:
            raise ValueError(
                f"{label}: potential must be has_deficit only and income one resource"
            )
        resource = potential_match.group(1)
        if income_match.group(1) != resource:
            raise ValueError(f"{label}: deficit and income resources must match")
        if resource not in expected_names or names[0] != expected_names[resource]:
            raise ValueError(f"{label}: unexpected resource or set_name")
        income = Decimal(income_match.group(2))
        if income != Decimal("1"):
            raise ValueError(f"{label}: gameplay recovery income must be exactly +1")
        if resource in rules:
            raise ValueError(f"{label}: duplicate resource {resource}")
        rules[resource] = StrategicRecoveryRule(resource, names[0], income)
    if set(rules) != set(STRATEGIC_RESOURCES):
        raise ValueError(f"{path}: recovery resources must be exactly {STRATEGIC_RESOURCES}")
    return tuple(rules[resource] for resource in STRATEGIC_RESOURCES)


def load_and_validate_model_policies(path: Path = MODEL_POLICIES) -> tuple[PolicyVariant, ...]:
    rows = _read_fixture(path, POLICY_FIELDS)
    gameplay_rules = parse_strategic_recovery_plan()
    by_name = {variant.name: variant for variant in MODEL_POLICIES_ORDERED}
    if {row["policy_id"] for row in rows} != set(by_name):
        raise ValueError(f"{path}: policy IDs must exactly match the five core variants")
    for row in rows:
        _validate_fixture_id(row["policy_id"].replace("-", "_"), label=f"{path}.policy_id")
        variant = by_name[row["policy_id"]]
        expected = {
            "mode": variant.mode.value,
            "income_pressure": _decimal_text(variant.income_pressure),
            "priority_bonus": _decimal_text(variant.priority_bonus),
            "runway_threshold_months": _decimal_text(variant.runway_threshold_months),
            "failed_income_target": _decimal_text(variant.failed_income_target),
        }
        for field, value in expected.items():
            if row[field] != value:
                raise ValueError(f"{path}: {variant.name}.{field} expected {value!r}, got {row[field]!r}")
        if variant is DEFICIT_ONLY_PLUS_ONE:
            expected_plan = str(STRATEGIC_RECOVERY_PLAN.relative_to(ROOT)).replace("\\", "/")
            if row["gameplay_plan"] != expected_plan:
                raise ValueError(
                    f"{path}: deficit-only-plus-one must bind to {expected_plan}"
                )
            if {rule.income for rule in gameplay_rules} != {variant.income_pressure}:
                raise ValueError(
                    f"{path}: fixture +1 pressure differs from parsed gameplay plan"
                )
        elif row["gameplay_plan"]:
            raise ValueError(
                f"{path}: only deficit-only-plus-one may bind the current gameplay plan"
            )
    return MODEL_POLICIES_ORDERED


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_normalized_text_lf(path: Path) -> str:
    """Hash text after normalizing CRLF and lone CR line endings to LF."""

    payload = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(payload).hexdigest()


def _provenance_sha256(path: Path, hash_mode: str) -> str:
    if hash_mode == PROVENANCE_HASH_NORMALIZED_TEXT_LF:
        return _sha256_normalized_text_lf(path)
    if hash_mode == PROVENANCE_HASH_RAW_BYTES:
        return _sha256(path)
    raise ValueError(f"Unknown provenance hash mode: {hash_mode}")


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def load_comparative_report_attestation(
    path: Path = COMPARATIVE_REPORT_ATTESTATION,
) -> dict[str, object]:
    try:
        attestation = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path}: invalid comparative-report attestation JSON") from error
    expected_fields = {
        "schema_version",
        "filename",
        "origin",
        "sha256",
        "hash_mode",
        "attested_date",
        "purpose",
    }
    if not isinstance(attestation, dict) or set(attestation) != expected_fields:
        raise ValueError(f"{path}: comparative-report attestation schema mismatch")
    expected_values = {
        "schema_version": 1,
        "filename": "stellar_ai_director_comparative_recovery_plan.md",
        "sha256": COMPARATIVE_REPORT_EXPECTED_SHA256,
        "hash_mode": PROVENANCE_HASH_RAW_BYTES,
        "attested_date": "2026-07-11",
    }
    for field, expected in expected_values.items():
        if attestation[field] != expected:
            raise ValueError(
                f"{path}: attestation {field} expected {expected!r}, "
                f"got {attestation[field]!r}"
            )
    for field in ("origin", "purpose"):
        if not isinstance(attestation[field], str) or not attestation[field].strip():
            raise ValueError(f"{path}: attestation {field} must be non-empty text")
    return attestation


def verify_optional_comparative_report(
    report_path: Path | None = None,
) -> str:
    attestation = load_comparative_report_attestation()
    path = COMPARATIVE_REPORT if report_path is None else report_path
    if not path.exists():
        return COMPARATIVE_REPORT_ATTESTED_ONLY
    if not path.is_file():
        raise OSError(f"External comparative report is not a file: {path}")
    actual_hash = _sha256(path)
    expected_hash = str(attestation["sha256"])
    if actual_hash != expected_hash:
        raise ValueError(
            "External comparative report hash mismatch: expected "
            f"{expected_hash}, got {actual_hash}; "
            "review the changed report before accepting new model provenance"
        )
    return COMPARATIVE_REPORT_AVAILABLE


def model_source_provenance() -> tuple[str, list[dict[str, str]]]:
    verify_optional_comparative_report()
    sources = (
        (
            "tools/stellar_ai_economic_model.py",
            MODEL_CORE,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "tools/simulate_stellar_ai_economy.py",
            Path(__file__).resolve(),
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "research/stellar-ai/stellar-ai-economic-model-scenarios-2026-07-11.csv",
            SCENARIOS,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt",
            PDX_PLAN,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "mods/StellarAIDirector/common/economic_plans/"
            "zzzz_staid_21_strategic_resource_deficit_recovery.txt",
            STRATEGIC_RECOVERY_PLAN,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "research/stellar-ai/stellar-ai-director-economic-checkpoints.csv",
            MODEL_CHECKPOINTS,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "research/stellar-ai/stellar-ai-director-economic-lane-candidates.csv",
            MODEL_CANDIDATES,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "research/stellar-ai/stellar-ai-director-economic-policy-variants.csv",
            MODEL_POLICIES,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "research/stellar-ai/stellar-ai-director-economic-policy-activation-cases.csv",
            MODEL_ACTIVATION_CASES,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
        (
            "research/stellar-ai/stellar-ai-director-comparative-report-attestation.json",
            COMPARATIVE_REPORT_ATTESTATION,
            PROVENANCE_HASH_NORMALIZED_TEXT_LF,
        ),
    )
    missing = [str(path) for _, path, _ in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Model provenance sources missing: {missing}")
    records = [
        {
            "logical_path": logical,
            "sha256": _provenance_sha256(path, hash_mode),
            "hash_mode": hash_mode,
        }
        for logical, path, hash_mode in sorted(sources)
    ]
    identity = {
        "schema_version": MODEL_SCHEMA_VERSION,
        "evidence_class": MODEL_EVIDENCE_CLASS,
        "sources": records,
    }
    return hashlib.sha256(_canonical_json(identity)).hexdigest(), records


def _feasibility_reason_json(reasons: tuple[object, ...]) -> str:
    return json.dumps(
        [
            {
                "code": reason.code.value,
                "key": reason.key,
                "required": _decimal_text(reason.required),
                "available": _decimal_text(reason.available),
                "projects": list(reason.project_ids),
            }
            for reason in reasons
        ],
        sort_keys=True,
        separators=(",", ":"),
    )


def _load_activation_case_rows() -> list[dict[str, str]]:
    rows = _read_fixture(MODEL_ACTIVATION_CASES, ACTIVATION_CASE_FIELDS)
    seen: set[str] = set()
    coverage: dict[str, set[str]] = {resource: set() for resource in STRATEGIC_RESOURCES}
    for row in rows:
        case_id = _validate_fixture_id(
            row["case_id"], label=f"{MODEL_ACTIVATION_CASES}.case_id"
        )
        family = _validate_fixture_id(
            row["case_family"], label=f"{MODEL_ACTIVATION_CASES}.case_family"
        )
        if case_id in seen:
            raise ValueError(f"{MODEL_ACTIVATION_CASES}: duplicate case_id {case_id}")
        seen.add(case_id)
        resource = row["resource"]
        if resource not in coverage:
            raise ValueError(f"{MODEL_ACTIVATION_CASES}: unknown resource {resource}")
        coverage[resource].add(family)
        _strict_bool(row["unlocked"], label=f"{case_id}.unlocked")
        if row["deficit_status"] not in {truth.value for truth in Truth}:
            raise ValueError(f"{case_id}: invalid deficit_status")
    family_sets = list(coverage.values())
    if len(rows) != 24 or not family_sets[0] or any(
        families != family_sets[0] for families in family_sets[1:]
    ):
        raise ValueError(
            f"{MODEL_ACTIVATION_CASES}: expected identical eight-case coverage "
            "for all three resources"
        )
    if len(family_sets[0]) != 8:
        raise ValueError(f"{MODEL_ACTIVATION_CASES}: expected exactly eight case families")
    return rows


def _activation_matrix_rows(provenance_id: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in _load_activation_case_rows():
        resource = case["resource"]
        unlocked = _strict_bool(case["unlocked"], label=f"{case['case_id']}.unlocked")
        deficit = Truth(case["deficit_status"])
        state = EconomicState(
            stockpile=QuantityVector.from_mapping({resource: case["stockpile"]}),
            capacity=QuantityVector.from_mapping({resource: case["capacity"]}),
            earned_income=QuantityVector.from_mapping({resource: case["earned_income"]}),
            market_income=QuantityVector.from_mapping({resource: case["market_income"]}),
            active_upkeep=QuantityVector.from_mapping({resource: case["active_upkeep"]}),
            deficit_status=FactSet.from_mapping({resource: deficit}),
            unlocked_resources=frozenset({resource} if unlocked else ()),
        )
        expected = set(_split_values(case["expected_active_policies"]))
        for variant in MODEL_POLICIES_ORDERED:
            result = evaluate_policy_activation(state, variant, resource)
            active = result.truth is Truth.TRUE
            net = Decimal(case["earned_income"]) - Decimal(case["active_upkeep"])
            rows.append(
                {
                    "schema_version": MODEL_SCHEMA_VERSION,
                    "source_provenance_id": provenance_id,
                    "evidence_class": MODEL_EVIDENCE_CLASS,
                    "case_id": case["case_id"],
                    "case_family": case["case_family"],
                    "policy_id": variant.name,
                    "resource": resource,
                    "stockpile": case["stockpile"],
                    "capacity": case["capacity"],
                    "earned_income": case["earned_income"],
                    "market_income": case["market_income"],
                    "active_upkeep": case["active_upkeep"],
                    "net_earned_income": _decimal_text(net),
                    "actual_deficit": deficit is Truth.TRUE,
                    "unlocked": unlocked,
                    "activation_result": result.truth.value,
                    "activation_reasons": "|".join(reason.value for reason in result.reasons),
                    "requested_income": _decimal_text(result.requested_income),
                    "remaining_pressure": _decimal_text(result.remaining_pressure),
                    "runway_months": _decimal_text(result.runway_months),
                    "expected_active": variant.name in expected,
                    "expectation_met": active == (variant.name in expected),
                    "unsafe_predeficit_activation": (
                        active
                        and deficit is Truth.FALSE
                        and variant.mode is not PolicyMode.ACTUAL_DEFICIT_OR_RUNWAY
                    ),
                    "earned_income_recovered": net >= 0,
                    "market_stock_only": Decimal(case["market_income"]) > 0 and net < 0,
                    "risk_label": case["risk_label"],
                    "evidence_ref": case["evidence_ref"],
                }
            )
    return rows


def _first_deficit_exit(run: PolicyRun, resource: str) -> str:
    if run.initial_state.deficit_status.get(resource) is Truth.FALSE:
        return "0"
    for snapshot in run.snapshots:
        if snapshot.state_after.deficit_status.get(resource) is Truth.FALSE:
            return str(snapshot.state_after.month)
    return ""


def _durable_income_month(
    run: PolicyRun,
    resource: str,
    *,
    include_zero: bool,
    window: int = 6,
) -> str:
    states = [snapshot.state_after for snapshot in run.snapshots]
    for index in range(0, len(states) - window + 1):
        sample = states[index : index + window]
        nets = [
            state.earned_income.get(resource) - state.active_upkeep.get(resource)
            for state in sample
            if state.earned_income.contains(resource)
            and state.active_upkeep.contains(resource)
        ]
        if len(nets) == window and all(
            net >= 0 if include_zero else net > 0 for net in nets
        ):
            return str(sample[0].month)
    return ""


def build_cross_priority_artifacts(
) -> tuple[dict[Path, list[dict[str, object]]], str, list[dict[str, str]]]:
    provenance_id, source_records = model_source_provenance()
    policies = load_and_validate_model_policies()
    checkpoints = load_model_checkpoints()
    candidates = load_model_candidates()
    checkpoint_ids = {checkpoint.scenario_id for checkpoint in checkpoints}
    orphaned = sorted({candidate.scenario_id for candidate in candidates} - checkpoint_ids)
    if orphaned:
        raise ValueError(f"Candidate fixtures reference unknown checkpoints: {orphaned}")
    grouped = {
        scenario_id: tuple(candidate for candidate in candidates if candidate.scenario_id == scenario_id)
        for scenario_id in checkpoint_ids
    }
    if {candidate.project.lane for candidate in candidates} != set(Lane):
        raise ValueError("Candidate fixtures must cover all twelve Lane values")
    for scenario_id, scenario_candidates in grouped.items():
        legal_count = sum(candidate.legal for candidate in scenario_candidates)
        if legal_count > 12:
            raise ValueError(f"{scenario_id}: exact model supports at most 12 legal candidates")

    active_rows: list[dict[str, object]] = []
    feasibility_rows: list[dict[str, object]] = []
    starvation_rows: list[dict[str, object]] = []
    counterfactual_rows: list[dict[str, object]] = []

    for checkpoint in checkpoints:
        specs = grouped[checkpoint.scenario_id]
        legal_projects = tuple(spec.project for spec in specs if spec.legal)
        comparison = compare_policy_variants(
            checkpoint.state,
            legal_projects,
            baseline=PARENT_ONLY,
            variants=policies[1:],
            months=checkpoint.horizon_months,
            operating_horizon_months=checkpoint.horizon_months,
            starvation_months=3,
            max_candidates=12,
        )
        runs = {comparison.baseline.variant.name: comparison.baseline}
        starvation_by_policy: dict[str, tuple[object, ...]] = {PARENT_ONLY.name: ()}
        for alternative in comparison.variants:
            runs[alternative.variant.name] = alternative.run
            starvation_by_policy[alternative.variant.name] = alternative.starvation

        for variant in policies:
            priorities = build_active_priority_set(checkpoint.state, legal_projects, variant)
            decisions = {decision.project.project_id: decision for decision in priorities.decisions}
            active_projects = tuple(priority.project for priority in priorities.active)
            search = find_feasible_bundles(
                checkpoint.state,
                active_projects,
                max_candidates=12,
                horizon_months=checkpoint.horizon_months,
            )
            selected = select_bundle(search, priorities)

            for spec in specs:
                singleton = (
                    evaluate_bundle_feasibility(
                        checkpoint.state,
                        (spec.project,),
                        horizon_months=checkpoint.horizon_months,
                    )
                    if spec.legal
                    else None
                )
                decision = decisions.get(spec.project.project_id)
                activation = decision.activation if decision else None
                state_text = (
                    "blocked_legality"
                    if not spec.legal
                    else decision.truth.value if decision else "inactive"
                )
                active_rows.append(
                    {
                        "schema_version": MODEL_SCHEMA_VERSION,
                        "source_provenance_id": provenance_id,
                        "evidence_class": MODEL_EVIDENCE_CLASS,
                        "scenario_id": checkpoint.scenario_id,
                        "policy_id": variant.name,
                        "horizon_months": checkpoint.horizon_months,
                        "project_id": spec.project.project_id,
                        "lane": spec.project.lane.value,
                        "consumer_surface": spec.consumer_surface,
                        "emergency_class": spec.emergency_class,
                        "activation_state": state_text,
                        "activation_reasons": "|".join(reason.value for reason in activation.reasons) if activation else "",
                        "requested_income": _decimal_text(activation.requested_income) if activation else "0",
                        "remaining_pressure": _decimal_text(activation.remaining_pressure) if activation else "0",
                        "priority": _decimal_text(decision.priority) if decision else _decimal_text(spec.project.base_priority),
                        "legal": spec.legal,
                        "parent_winner_verified": checkpoint.parent_winner_verified and spec.parent_winner_verified,
                        "affordable_now": bool(singleton and singleton.feasible),
                        "feasibility_reasons": _feasibility_reason_json(singleton.reasons) if singleton else "legality",
                        "one_time_cost_json": _vector_json(spec.project.one_time_cost),
                        "monthly_upkeep_json": _vector_json(spec.project.completion_upkeep),
                        "completion_income_json": _vector_json(spec.project.completion_income),
                        "queue": spec.project.queue or "",
                        "required_gates": "|".join(sorted(spec.project.required_gates)),
                        "parent_provenance": spec.parent_provenance,
                        "evidence_ref": checkpoint.evidence_ref,
                    }
                )

            all_bundles = sorted(
                search.feasible + search.rejected,
                key=lambda result: (len(result.projects), result.project_ids),
            )
            for bundle in all_bundles:
                codes = {reason.code for reason in bundle.reasons}
                code_values = {code.value for code in codes}
                affordable = not code_values & {"resource", "budget", "influence", "runway"}
                feasibility_rows.append(
                    {
                        "schema_version": MODEL_SCHEMA_VERSION,
                        "source_provenance_id": provenance_id,
                        "evidence_class": MODEL_EVIDENCE_CLASS,
                        "scenario_id": checkpoint.scenario_id,
                        "policy_id": variant.name,
                        "horizon_months": checkpoint.horizon_months,
                        "bundle_id": "|".join(bundle.project_ids) or "empty",
                        "project_ids": "|".join(bundle.project_ids),
                        "lanes": "|".join(sorted({project.lane.value for project in bundle.projects})),
                        "candidate_count": len(bundle.projects),
                        "resource_affordable": FeasibilityCode.RESOURCE not in codes,
                        "budget_feasible": FeasibilityCode.BUDGET not in codes,
                        "queue_feasible": FeasibilityCode.QUEUE not in codes,
                        "slot_feasible": FeasibilityCode.SLOT not in codes,
                        "job_feasible": FeasibilityCode.JOB not in codes,
                        "influence_feasible": FeasibilityCode.INFLUENCE not in codes,
                        "runway_preserved": "runway" not in code_values,
                        "gate_feasible": not codes & {FeasibilityCode.MISSING_GATE, FeasibilityCode.FORBIDDEN_GATE},
                        "affordable": affordable,
                        "feasible": bundle.feasible,
                        "selected_by_policy": bundle.project_ids == selected.project_ids,
                        "major_lane_count": len({project.lane for project in bundle.projects}),
                        "reasons_json": _feasibility_reason_json(bundle.reasons),
                    }
                )

            starvations = starvation_by_policy[variant.name]
            by_lane = {item.lane: item for item in starvations}
            for lane in Lane:
                item = by_lane.get(lane)
                starvation_rows.append(
                    {
                        "schema_version": MODEL_SCHEMA_VERSION,
                        "source_provenance_id": provenance_id,
                        "evidence_class": MODEL_EVIDENCE_CLASS,
                        "scenario_id": checkpoint.scenario_id,
                        "policy_id": variant.name,
                        "horizon_months": checkpoint.horizon_months,
                        "lane": lane.value,
                        "starved": item is not None,
                        "months_affordable_unselected": len(item.months) if item else 0,
                        "starvation_months": "|".join(map(str, item.months)) if item else "",
                        "threshold_months": 3,
                        "shared_bottlenecks": "|".join(f"{code.value}:{key}" for code, key in item.shared_bottlenecks) if item else "",
                        "counterfactual_selected_months": "|".join(map(str, item.counterfactual_selected_months)) if item else "",
                        "classification": "cross_priority_starvation" if item else "none",
                    }
                )

            run = runs[variant.name]
            action_counts = Counter(
                project.lane.value
                for snapshot in run.snapshots
                for project in snapshot.selected.projects
            )
            starvation_months = {lane.value: 0 for lane in Lane}
            for item in starvations:
                starvation_months[item.lane.value] += len(item.months)
            unsafe_predeficit = sum(
                1
                for snapshot in run.snapshots
                for decision in snapshot.priorities.decisions
                if decision.active
                and decision.project.strategic_resource is not None
                and snapshot.state_before.deficit_status.get(decision.project.strategic_resource) is Truth.FALSE
                and variant.mode is not PolicyMode.ACTUAL_DEFICIT_OR_RUNWAY
            )
            starts_by_resource = Counter(
                project.strategic_resource
                for snapshot in run.snapshots
                for project in snapshot.selected.projects
                if project.strategic_resource
            )
            completions_by_resource = Counter()
            for snapshot in run.snapshots:
                for project in snapshot.selected.projects:
                    if project.strategic_resource and snapshot.month + project.duration_months <= run.final_state.month:
                        completions_by_resource[project.strategic_resource] += 1
            minimum_stockpile = {
                resource: min(
                    [run.initial_state.stockpile.get(resource)]
                    + [snapshot.state_after.stockpile.get(resource) for snapshot in run.snapshots]
                )
                for resource in ("volatile_motes", "exotic_gases", "rare_crystals")
            }
            unsafe_reasons: list[str] = []
            if unsafe_predeficit:
                unsafe_reasons.append("predeficit_activation")
            if starvations:
                unsafe_reasons.append("cross_priority_starvation")
            row: dict[str, object] = {
                "schema_version": MODEL_SCHEMA_VERSION,
                "source_provenance_id": provenance_id,
                "evidence_class": MODEL_EVIDENCE_CLASS,
                "scenario_id": checkpoint.scenario_id,
                "policy_id": variant.name,
                "baseline_policy_id": PARENT_ONLY.name,
                "horizon_months": checkpoint.horizon_months,
                "unsafe_predeficit_activation_count": unsafe_predeficit,
                "foregone_affordable_action_count": sum(len(snapshot.blocked_opportunities) for snapshot in run.snapshots),
                "major_lanes_progressed": sum(action_counts[lane.value] > 0 for lane in Lane),
            }
            for resource in ("volatile_motes", "exotic_gases", "rare_crystals"):
                durable_positive = _durable_income_month(
                    run, resource, include_zero=False
                )
                durable_recovery = _durable_income_month(
                    run, resource, include_zero=True
                )
                row.update(
                    {
                        f"deficit_exit_month_{resource}": _first_deficit_exit(run, resource),
                        f"durable_strict_positive_month_{resource}": durable_positive,
                        f"durable_earned_recovery_month_{resource}": durable_recovery,
                        f"earned_income_recovered_{resource}": bool(durable_recovery),
                        f"market_stock_only_{resource}": (
                            run.final_state.market_income.get(resource) > 0
                            and not durable_recovery
                        ),
                        f"minimum_stockpile_{resource}": _decimal_text(minimum_stockpile[resource]),
                        f"producer_starts_{resource}": starts_by_resource[resource],
                        f"producer_completions_{resource}": completions_by_resource[resource],
                    }
                )
            for lane in Lane:
                row[f"actions_{lane.value}"] = action_counts[lane.value]
                row[f"starvation_months_{lane.value}"] = starvation_months[lane.value]
            row.update(
                {
                    "unsafe": bool(unsafe_reasons),
                    "unsafe_reason_codes": "|".join(unsafe_reasons),
                }
            )
            counterfactual_rows.append(row)

    artifacts = {
        ACTIVE_PRIORITY: active_rows,
        CONCURRENT_FEASIBILITY: feasibility_rows,
        LANE_STARVATION: starvation_rows,
        ACTIVATION_MATRIX: _activation_matrix_rows(provenance_id),
        POLICY_COUNTERFACTUAL: counterfactual_rows,
    }
    return artifacts, provenance_id, source_records


@dataclass(frozen=True)
class ModelPublication:
    csv_bytes: dict[Path, bytes]
    manifest_bytes: bytes
    provenance_id: str
    row_counts: dict[str, int]


def build_legacy_artifact_rows(
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    policy = load_pdx_policy()
    timeline: list[dict[str, object]] = []
    summary: list[dict[str, object]] = []
    for scenario in load_scenarios():
        scenario_timeline, scenario_summary = simulate(scenario, policy)
        timeline.extend(scenario_timeline)
        summary.append(scenario_summary)
    return timeline, summary


def build_model_publication(
    legacy_timeline: list[dict[str, object]] | None = None,
    legacy_summary: list[dict[str, object]] | None = None,
    cross_artifacts: dict[Path, list[dict[str, object]]] | None = None,
) -> ModelPublication:
    if legacy_timeline is None or legacy_summary is None:
        if legacy_timeline is not None or legacy_summary is not None:
            raise ValueError("legacy timeline and summary must be supplied together")
        legacy_timeline, legacy_summary = build_legacy_artifact_rows()
    if cross_artifacts is None:
        cross_artifacts, provenance_id, sources = build_cross_priority_artifacts()
    else:
        provenance_id, sources = model_source_provenance()
    all_rows = {
        TIMELINE: legacy_timeline,
        SUMMARY: legacy_summary,
        **cross_artifacts,
    }
    if set(all_rows) != set(MODEL_OUTPUTS):
        raise ValueError("Model output allowlist mismatch")
    if any(path.resolve().parent != RESEARCH.resolve() for path in all_rows):
        raise ValueError("Model outputs must remain under research/stellar-ai")
    row_counts = {path.name: len(rows) for path, rows in all_rows.items()}
    csv_bytes = {
        path: serialize_csv_rows(rows, MODEL_OUTPUT_SCHEMAS[path])
        for path, rows in all_rows.items()
    }
    outputs = [
        {
            "logical_path": f"research/stellar-ai/{target.name}",
            "sha256": hashlib.sha256(payload).hexdigest(),
            "row_count": row_counts[target.name],
        }
        for target, payload in sorted(csv_bytes.items(), key=lambda item: item[0].name)
    ]
    manifest = {
        "schema_version": MODEL_SCHEMA_VERSION,
        "source_provenance_id": provenance_id,
        "evidence_class": MODEL_EVIDENCE_CLASS,
        "sources": sources,
        "outputs": outputs,
    }
    return ModelPublication(
        csv_bytes=csv_bytes,
        manifest_bytes=_canonical_json(manifest) + b"\n",
        provenance_id=provenance_id,
        row_counts=row_counts,
    )


def verify_model_artifact_freshness(
    legacy_timeline: list[dict[str, object]] | None = None,
    legacy_summary: list[dict[str, object]] | None = None,
    cross_artifacts: dict[Path, list[dict[str, object]]] | None = None,
) -> tuple[str, dict[str, int]]:
    publication = build_model_publication(
        legacy_timeline,
        legacy_summary,
        cross_artifacts,
    )
    mismatches: list[str] = []
    for target, expected in publication.csv_bytes.items():
        if not target.is_file():
            mismatches.append(f"missing:{target.name}")
        elif target.read_bytes() != expected:
            mismatches.append(f"stale:{target.name}")
    if not MODEL_PROVENANCE.is_file():
        mismatches.append(f"missing:{MODEL_PROVENANCE.name}")
    elif MODEL_PROVENANCE.read_bytes() != publication.manifest_bytes:
        mismatches.append(f"stale:{MODEL_PROVENANCE.name}")
    if mismatches:
        raise ValueError(
            "Economic model artifacts are not byte-exact/current: "
            + ", ".join(mismatches)
            + "; run python tools/simulate_stellar_ai_economy.py"
        )
    return publication.provenance_id, publication.row_counts


def publish_model_artifacts(
    legacy_timeline: list[dict[str, object]],
    legacy_summary: list[dict[str, object]],
) -> tuple[str, dict[str, int]]:
    publication = build_model_publication(legacy_timeline, legacy_summary)
    with tempfile.TemporaryDirectory(prefix=".staid-economic-model-", dir=RESEARCH) as temp_dir:
        staging = Path(temp_dir)
        staged: dict[Path, Path] = {}
        for target, payload in publication.csv_bytes.items():
            staged_path = staging / target.name
            staged_path.write_bytes(payload)
            staged[target] = staged_path
        staged_manifest = staging / MODEL_PROVENANCE.name
        staged_manifest.write_bytes(publication.manifest_bytes)
        for target in MODEL_OUTPUTS:
            os.replace(staged[target], target)
        os.replace(staged_manifest, MODEL_PROVENANCE)
    return publication.provenance_id, publication.row_counts


def main() -> None:
    external_report_status = verify_optional_comparative_report()
    policy = load_pdx_policy()
    all_timeline: list[dict[str, object]] = []
    all_summary: list[dict[str, object]] = []
    for scenario in load_scenarios():
        timeline, summary = simulate(scenario, policy)
        all_timeline.extend(timeline)
        all_summary.append(summary)
    provenance_id, row_counts = publish_model_artifacts(all_timeline, all_summary)
    print(
        f"Simulated {len(all_summary)} legacy scenarios and five cross-priority artifacts "
        f"from {policy.source.relative_to(ROOT)}; provenance={provenance_id}; "
        f"rows={sum(row_counts.values())}; external_report={external_report_status}"
    )


if __name__ == "__main__":
    main()
