#!/usr/bin/env python3
"""Build research-capacity tables from the active Stellaris stack."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from stellar_ai_director_lib import (
    PDXBlock,
    PDXParseError,
    RESEARCH_ROOT,
    STELLARIS_INSTALL_ROOT,
    _collect_economic_definitions,
    _collect_job_adds,
    _collect_resource_amounts,
    _collect_upgrade_ids,
    _json_dump,
    _valuation_stack_roots,
    _winning_economic_definitions,
    atom_value,
    block_assignments,
    build_active_playset_snapshot,
    collect_global_variables,
    iter_assignments,
    iter_text_files,
    parse_file,
    write_csv,
    write_text_file,
)


OUT_JOBS = RESEARCH_ROOT / "stellar-ai-director-research-capacity-jobs-2026-07-09.csv"
OUT_BUILDINGS = RESEARCH_ROOT / "stellar-ai-director-research-capacity-buildings-2026-07-09.csv"
OUT_PLAN = RESEARCH_ROOT / "stellar-ai-director-research-capacity-plan-2026-07-09.csv"
OUT_MD = RESEARCH_ROOT / "stellar-ai-director-research-capacity-2026-07-09.md"
RESEARCH_KEYS = ("physics_research", "society_research", "engineering_research")
JOB_WORKFORCE_UNITS = 100.0
SUPPORT_KEYS = (
    "energy",
    "minerals",
    "consumer_goods",
    "alloys",
    "volatile_motes",
    "exotic_gases",
    "rare_crystals",
)


def add_amounts(left: dict[str, float], right: dict[str, float], factor: float = 1.0) -> None:
    for key, value in right.items():
        left[key] = left.get(key, 0.0) + value * factor


def research_total(amounts: dict[str, float]) -> float:
    return sum(amounts.get(key, 0.0) for key in RESEARCH_KEYS)


def resource_columns(prefix: str, amounts: dict[str, float]) -> dict[str, float]:
    keys = (*RESEARCH_KEYS, *SUPPORT_KEYS)
    return {f"{prefix}_{key}": round(amounts.get(key, 0.0), 6) for key in keys}


def normalize_job_workforce(amount: float) -> float:
    return amount / JOB_WORKFORCE_UNITS


def collect_job_resources(value: PDXBlock, variables: dict[str, float]) -> tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, float], set[str]]:
    base_output: dict[str, float] = {}
    triggered_output: dict[str, float] = {}
    base_upkeep: dict[str, float] = {}
    triggered_upkeep: dict[str, float] = {}
    unresolved: set[str] = set()
    for resources in block_assignments(value, "resources"):
        if not isinstance(resources.value, PDXBlock):
            continue
        for assignment in block_assignments(resources.value):
            if assignment.key == "produces":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(base_output, amounts)
                unresolved.update(missing)
            elif assignment.key == "upkeep":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(base_upkeep, amounts)
                unresolved.update(missing)
            elif assignment.key == "triggered_produces":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(triggered_output, amounts)
                unresolved.update(missing)
            elif assignment.key == "triggered_upkeep":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(triggered_upkeep, amounts)
                unresolved.update(missing)
    return base_output, triggered_output, base_upkeep, triggered_upkeep, unresolved


def collect_winning_jobs(playset: dict[str, Any]) -> dict[str, dict[str, Any]]:
    roots = _valuation_stack_roots(playset)
    variables = collect_global_variables([Path(root["root"]) for root in roots])
    winners: dict[str, dict[str, Any]] = {}
    for root_info in roots:
        root = Path(root_info["root"])
        folder = root / "common" / "pop_jobs"
        if not folder.exists():
            continue
        for path in iter_text_files(folder):
            try:
                parsed = parse_file(path)
            except PDXParseError:
                continue
            for assignment in block_assignments(parsed):
                if assignment.key.startswith("@") or not isinstance(assignment.value, PDXBlock):
                    continue
                current = winners.get(assignment.key)
                if current is None or int(root_info["load_position"]) >= int(current["load_position"]):
                    winners[assignment.key] = {
                        **root_info,
                        "job_id": assignment.key,
                        "relative_file": str(path.relative_to(root)),
                        "value": assignment.value,
                    }
    for row in winners.values():
        value = row["value"]
        base_output, triggered_output, base_upkeep, triggered_upkeep, unresolved = collect_job_resources(value, variables)
        optimistic_output = dict(base_output)
        optimistic_upkeep = dict(base_upkeep)
        add_amounts(optimistic_output, triggered_output)
        add_amounts(optimistic_upkeep, triggered_upkeep)
        row.update(
            {
                "base_output_json": _json_dump(base_output),
                "triggered_output_json": _json_dump(triggered_output),
                "optimistic_output_json": _json_dump(optimistic_output),
                "base_upkeep_json": _json_dump(base_upkeep),
                "triggered_upkeep_json": _json_dump(triggered_upkeep),
                "optimistic_upkeep_json": _json_dump(optimistic_upkeep),
                "base_research_total": round(research_total(base_output), 6),
                "optimistic_research_total": round(research_total(optimistic_output), 6),
                "unresolved_variables": "|".join(sorted(unresolved)) or "none",
                **resource_columns("base_output", base_output),
                **resource_columns("optimistic_output", optimistic_output),
                **resource_columns("optimistic_upkeep", optimistic_upkeep),
            }
        )
    return winners


def direct_resource_blocks(value: PDXBlock, variables: dict[str, float]) -> tuple[dict[str, float], dict[str, float], set[str]]:
    output: dict[str, float] = {}
    upkeep: dict[str, float] = {}
    unresolved: set[str] = set()
    for resources in block_assignments(value, "resources"):
        if not isinstance(resources.value, PDXBlock):
            continue
        for assignment in block_assignments(resources.value):
            if assignment.key in {"produces", "produced_resources"}:
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(output, amounts)
                unresolved.update(missing)
            elif assignment.key == "upkeep":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(upkeep, amounts)
                unresolved.update(missing)
    for ai_production in block_assignments(value, "ai_resource_production"):
        amounts, missing = _collect_resource_amounts(ai_production.value, variables)
        add_amounts(output, amounts)
        unresolved.update(missing)
    return output, upkeep, unresolved


def chain_for(building_id: str, upgrades: dict[str, list[str]]) -> list[str]:
    chain = [building_id]
    seen = {building_id}
    current = building_id
    while upgrades.get(current):
        nxt = sorted(upgrades[current])[0]
        if nxt in seen:
            break
        chain.append(nxt)
        seen.add(nxt)
        current = nxt
    return chain


def collect_buildings(playset: dict[str, Any], jobs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    roots = _valuation_stack_roots(playset)
    variables = collect_global_variables([Path(root["root"]) for root in roots])
    definitions = _collect_economic_definitions(playset)
    winners = _winning_economic_definitions(definitions)
    upgrades = {
        object_id: _collect_upgrade_ids(row["value"])
        for (object_type, object_id), row in winners.items()
        if object_type == "building" and isinstance(row.get("value"), PDXBlock)
    }
    rows: list[dict[str, Any]] = []
    for (object_type, object_id), row in sorted(winners.items()):
        if object_type != "building" or not isinstance(row.get("value"), PDXBlock):
            continue
        value = row["value"]
        jobs_created, missing_jobs = _collect_job_adds(value, variables)
        direct_output, direct_upkeep, missing_direct = direct_resource_blocks(value, variables)
        job_output: dict[str, float] = {}
        job_upkeep: dict[str, float] = {}
        unknown_jobs: list[str] = []
        for job_id, count in jobs_created.items():
            job = jobs.get(job_id)
            if not job:
                unknown_jobs.append(job_id)
                continue
            job_equivalents = normalize_job_workforce(count)
            add_amounts(job_output, json.loads(str(job["optimistic_output_json"])), job_equivalents)
            add_amounts(job_upkeep, json.loads(str(job["optimistic_upkeep_json"])), job_equivalents)
        total_output = dict(direct_output)
        total_upkeep = dict(direct_upkeep)
        add_amounts(total_output, job_output)
        add_amounts(total_upkeep, job_upkeep)
        chain = chain_for(object_id, upgrades)
        rows.append(
            {
                "building_id": object_id,
                "winning_mod_name": row["name"],
                "winning_file": row["relative_file"],
                "category": atom_value(block_assignments(value, "category")[0].value) if block_assignments(value, "category") else "",
                "is_upgrade_terminal": "yes" if not upgrades.get(object_id) else "no",
                "upgrade_chain_to_terminal": "|".join(chain),
                "upgrade_terminal": chain[-1],
                "jobs_created_json": _json_dump(jobs_created),
                "raw_job_workforce_total": round(sum(max(0.0, amount) for amount in jobs_created.values()), 6),
                "job_slots_total": round(
                    sum(max(0.0, normalize_job_workforce(amount)) for amount in jobs_created.values()), 6
                ),
                "unknown_jobs": "|".join(sorted(unknown_jobs)) or "none",
                "direct_output_json": _json_dump(direct_output),
                "direct_upkeep_json": _json_dump(direct_upkeep),
                "job_output_json": _json_dump(job_output),
                "job_upkeep_json": _json_dump(job_upkeep),
                "total_output_json": _json_dump(total_output),
                "total_upkeep_json": _json_dump(total_upkeep),
                "total_research": round(research_total(total_output), 6),
                "data_quality_flags": "|".join(
                    flag
                    for flag in [
                        "research_output" if research_total(total_output) > 0 else "",
                        "has_unknown_jobs" if unknown_jobs else "",
                        "unresolved_variables" if missing_jobs or missing_direct else "",
                    ]
                    if flag
                )
                or "none",
                "unresolved_variables": "|".join(sorted(missing_jobs | missing_direct)) or "none",
                **resource_columns("total_output", total_output),
                **resource_columns("total_upkeep", total_upkeep),
            }
        )
    return rows


def plan_rows(buildings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def repeatable_candidate(row: dict[str, Any]) -> bool:
        mod_name = str(row["winning_mod_name"]).lower()
        building_id = str(row["building_id"])
        if "more events" in mod_name or "more primitives" in mod_name:
            return False
        special_prefixes = ("holding_", "building_fe_", "building_organic_", "building_passenger_")
        return not building_id.startswith(special_prefixes)

    scopes = {
        "raw_top_terminal": [
            row for row in buildings if row["is_upgrade_terminal"] == "yes" and float(row["total_research"]) > 0
        ],
        "repeatable_candidate_terminal": [
            row
            for row in buildings
            if row["is_upgrade_terminal"] == "yes" and float(row["total_research"]) > 0 and repeatable_candidate(row)
        ],
    }
    rows: list[dict[str, Any]] = []
    for scope, candidates in scopes.items():
        best = sorted(candidates, key=lambda row: float(row["total_research"]), reverse=True)
        for slots in (6, 8, 10, 12):
            for take in (1, min(3, len(best)), min(slots, len(best))):
                selected = best[:take]
                research = sum(float(row["total_research"]) for row in selected)
                rows.append(
                    {
                        "scenario": f"{scope}_top_{take}_in_{slots}_slots",
                        "building_slots": slots,
                        "selected_buildings": "|".join(row["building_id"] for row in selected),
                        "research_per_full_colony": round(research, 6),
                        "colonies_for_3000_research": math.ceil(3000 / research) if research > 0 else 0,
                        "unused_slots": slots - take,
                    }
                )
    return rows


def write_summary(jobs: dict[str, dict[str, Any]], buildings: list[dict[str, Any]], plans: list[dict[str, Any]]) -> None:
    research_buildings = [row for row in buildings if float(row["total_research"]) > 0]
    best = sorted(research_buildings, key=lambda row: float(row["total_research"]), reverse=True)[:20]
    lines = [
        "# Stellar AI Director Research Capacity",
        "",
        "This is a deterministic active-stack capacity inventory. It resolves winning active-stack job definitions, building job slots, direct building output/upkeep, and building upgrade chains. Job triggered resource blocks are included in the optimistic output columns and should be treated as maximum-potential math, not runtime proof.",
        "",
        f"Job-producing modifiers are normalized from Stellaris 4.x workforce units using {JOB_WORKFORCE_UNITS:g} workforce = 1 full job equivalent. Raw workforce totals are retained in the building CSV.",
        "",
        f"- Jobs indexed: {len(jobs)}",
        f"- Buildings indexed: {len(buildings)}",
        f"- Buildings with resolved research output: {len(research_buildings)}",
        f"- Source roots include vanilla at `{STELLARIS_INSTALL_ROOT}` plus enabled launcher mods.",
        "",
        "## Top Research Buildings",
        "",
        "| rank | building | research/month | jobs | mod |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for index, row in enumerate(best, 1):
        lines.append(
            f"| {index} | `{row['building_id']}` | {row['total_research']} | {row['job_slots_total']} | {row['winning_mod_name']} |"
        )
    lines.extend(["", "## Colony Scenarios", "", "| scenario | research/month | colonies for 3000 |", "| --- | ---: | ---: |"])
    for row in plans:
        lines.append(f"| {row['scenario']} | {row['research_per_full_colony']} | {row['colonies_for_3000_research']} |")
    write_text_file(OUT_MD, "\n".join(lines) + "\n")


def main() -> None:
    playset = build_active_playset_snapshot()
    jobs = collect_winning_jobs(playset)
    job_rows = [
        {key: value for key, value in row.items() if key != "value"}
        for row in sorted(jobs.values(), key=lambda item: item["job_id"])
    ]
    buildings = collect_buildings(playset, jobs)
    plans = plan_rows(buildings)
    write_csv(OUT_JOBS, job_rows)
    write_csv(OUT_BUILDINGS, buildings)
    write_csv(OUT_PLAN, plans)
    write_summary(jobs, buildings, plans)
    print(f"generated {len(job_rows)} jobs, {len(buildings)} buildings, {len(plans)} plan rows")


if __name__ == "__main__":
    main()
