#!/usr/bin/env python3
"""Build research-capacity tables from the active Stellaris stack."""

from __future__ import annotations

import json
import math
import re
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
    _numeric_atom,
    _valuation_stack_roots,
    _winning_economic_definitions,
    atom_value,
    assignment_atoms,
    block_assignments,
    build_active_playset_snapshot,
    compact_list,
    collect_global_variables,
    iter_assignments,
    iter_text_files,
    parse_file,
    write_csv,
    write_text_file,
)


OUT_JOBS = RESEARCH_ROOT / "stellar-ai-director-research-capacity-jobs-2026-07-09.csv"
OUT_BUILDINGS = RESEARCH_ROOT / "stellar-ai-director-research-capacity-buildings-2026-07-09.csv"
OUT_DEVELOPMENT = RESEARCH_ROOT / "stellar-ai-director-research-capacity-development-2026-07-09.csv"
OUT_PLAN = RESEARCH_ROOT / "stellar-ai-director-research-capacity-plan-2026-07-09.csv"
OUT_ROLES = RESEARCH_ROOT / "stellar-ai-director-colony-role-targets-2026-07-09.csv"
OUT_TECH = RESEARCH_ROOT / "stellar-ai-director-research-capacity-tech-modifiers-2026-07-09.csv"
OUT_INFRA = RESEARCH_ROOT / "stellar-ai-director-strategic-infrastructure-targets-2026-07-09.csv"
OUT_RESOURCE_COVERAGE = RESEARCH_ROOT / "stellar-ai-director-modeling-resource-coverage-2026-07-09.csv"
OUT_READINESS = RESEARCH_ROOT / "stellar-ai-director-build-plan-readiness-2026-07-09.csv"
OUT_BENEFITS = RESEARCH_ROOT / "stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv"
OUT_BLOCKERS = RESEARCH_ROOT / "stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv"
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
    "food",
    "unity",
    "influence",
    "trade",
    "trade_value",
    "sr_zro",
    "sr_dark_matter",
    "sr_living_metal",
    "nanites",
    "giga_sr_negative_mass",
    "giga_sr_amb_megaconstruction",
    "giga_sr_iodizium",
    "giga_sr_sentient_metal",
)
UPKEEP_MULT_KEYS = ("planet_researchers_upkeep_mult",)
ROLE_TARGETS = {
    "research_world": ("physics_research", "society_research", "engineering_research"),
    "forge_world": ("alloys",),
    "factory_world": ("consumer_goods",),
    "generator_world": ("energy",),
    "mining_world": ("minerals",),
    "agri_world": ("food",),
    "unity_world": ("unity",),
    "refinery_world": ("volatile_motes", "exotic_gases", "rare_crystals"),
    "trade_world": ("trade",),
}
STRATEGIC_MODIFIER_TERMS = (
    "pop_growth",
    "pop_assembly",
    "resettlement",
    "migration",
    "shipyard",
    "naval_cap",
    "naval_capacity",
    "stability",
    "amenities",
    "housing",
    "habitability",
    "planet_capacity",
    "crime",
    "deviancy",
    "defense_army",
    "defense_armies",
    "army",
    "bombardment",
    "ship_build",
    "shipyard_build",
    "starbase",
    "megastructure",
    "build_speed",
    "district",
    "blocker",
    "envoy",
    "diplom",
    "trust",
    "federation",
    "opinion",
    "relations",
    "research_speed",
)
POP_GROWTH_TERMS = ("pop_growth", "pop_assembly", "organic_pop_assembly", "clone_soldiers")
RESETTLEMENT_SOURCE_TERMS = ("resettlement_unemployed_mult",)
RESETTLEMENT_DESTINATION_TERMS = ("resettlement_unemployed_destination_mult",)
CAPITAL_STRATEGIC_TERMS = ("envoy", "diplom", "trust", "federation", "opinion", "relations", "edict", "council")
STARBASE_PRIORITY_TERMS = ("resettlement", "migration", "shipyard", "naval_cap", "trade", "food", "stability")
BENEFIT_CLASS_TERMS = {
    "pop_growth_assembly": POP_GROWTH_TERMS,
    "migration_resettlement": ("resettlement", "migration"),
    "trade_policy_value": ("trade", "trade_value"),
    "amenities": ("amenities",),
    "stability": ("stability",),
    "housing": ("housing",),
    "habitability": ("habitability",),
    "planet_capacity": ("planet_capacity",),
    "crime_deviancy_control": ("crime", "deviancy"),
    "defense_armies": ("defense_army", "defense_armies", "army"),
    "bombardment_resistance": ("bombardment",),
    "naval_capacity": ("naval_cap", "naval_capacity"),
    "shipyard_throughput": ("shipyard", "ship_build", "shipyard_build"),
    "starbase_support": ("starbase", "shipyard", "naval_cap", "trade", "resettlement", "migration"),
    "diplomacy_envoys": CAPITAL_STRATEGIC_TERMS,
    "research_speed": ("research_speed",),
    "empire_country_modifier": ("country_modifier", "triggered_country_modifier", "empire_limit"),
    "megastructure_construction": ("megastructure", "build_speed"),
    "blocker_district_capacity": ("blocker", "district"),
    "direct_resource_support": SUPPORT_KEYS,
}
RESOURCE_AMOUNT_JSON_COLUMNS = {
    "jobs": (
        "base_output_json",
        "triggered_output_json",
        "optimistic_output_json",
        "base_upkeep_json",
        "triggered_upkeep_json",
        "optimistic_upkeep_json",
    ),
    "buildings": (
        "direct_output_json",
        "direct_triggered_output_json",
        "direct_optimistic_output_json",
        "direct_upkeep_json",
        "direct_triggered_upkeep_json",
        "direct_optimistic_upkeep_json",
        "job_base_output_json",
        "job_triggered_output_json",
        "job_output_json",
        "job_base_upkeep_json",
        "job_triggered_upkeep_json",
        "job_upkeep_json",
        "base_output_json",
        "triggered_output_json",
        "optimistic_output_json",
        "total_output_json",
        "base_upkeep_json",
        "triggered_upkeep_json",
        "optimistic_upkeep_json",
        "total_upkeep_json",
    ),
    "development": (
        "direct_output_json",
        "direct_triggered_output_json",
        "direct_optimistic_output_json",
        "direct_upkeep_json",
        "direct_triggered_upkeep_json",
        "direct_optimistic_upkeep_json",
        "job_base_output_json",
        "job_triggered_output_json",
        "job_output_json",
        "job_base_upkeep_json",
        "job_triggered_upkeep_json",
        "job_upkeep_json",
        "base_output_json",
        "triggered_output_json",
        "optimistic_output_json",
        "total_output_json",
        "base_upkeep_json",
        "triggered_upkeep_json",
        "optimistic_upkeep_json",
        "total_upkeep_json",
        "base_net_resources_json",
        "conservative_net_resources_json",
        "optimistic_net_resources_json",
        "net_resources_json",
    ),
    "strategic_infrastructure": (
        "direct_output_json",
        "direct_triggered_output_json",
        "direct_optimistic_output_json",
        "direct_upkeep_json",
        "direct_triggered_upkeep_json",
        "direct_optimistic_upkeep_json",
    ),
}


def add_amounts(left: dict[str, float], right: dict[str, float], factor: float = 1.0) -> None:
    for key, value in right.items():
        left[key] = left.get(key, 0.0) + value * factor


def research_total(amounts: dict[str, float]) -> float:
    return sum(amounts.get(key, 0.0) for key in RESEARCH_KEYS)


def resource_columns(prefix: str, amounts: dict[str, float]) -> dict[str, float]:
    keys = (*RESEARCH_KEYS, *SUPPORT_KEYS)
    return {f"{prefix}_{key}": round(amounts.get(key, 0.0), 6) for key in keys}


def role_total(amounts: dict[str, float], role: str) -> float:
    return sum(amounts.get(key, 0.0) for key in ROLE_TARGETS[role])


def net_amounts(output: dict[str, float], upkeep: dict[str, float]) -> dict[str, float]:
    net = dict(output)
    add_amounts(net, upkeep, -1.0)
    return net


def combined_amounts(*amounts: dict[str, float]) -> dict[str, float]:
    combined: dict[str, float] = {}
    for item in amounts:
        add_amounts(combined, item)
    return combined


def classify_colony_class(object_id: str) -> str:
    lower = object_id.lower()
    if "birch" in lower:
        return "birch_world"
    if "frameworld" in lower:
        return "frameworld"
    if "alderson" in lower:
        return "alderson_disk"
    if "ring_world" in lower or "ringworld" in lower or "_srw_" in lower:
        return "ring_world"
    if "habitat" in lower or lower.startswith("district_hab_") or "_hab_" in lower or "superhab" in lower:
        return "habitat"
    if "arcology" in lower or "ecumenopolis" in lower:
        return "arcology"
    if "resort" in lower:
        return "resort_world"
    return "generic_planet_or_special"


def assignment_value_text(value: Any) -> str:
    atom = atom_value(value)
    if atom is None:
        return ""
    return str(atom).strip('"')


def has_assignment(value: PDXBlock, key: str, expected: str | None = None) -> bool:
    for assignment in iter_assignments(value):
        if assignment.key.strip('"') != key:
            continue
        if expected is None:
            return True
        if assignment_value_text(assignment.value).lower() == expected.lower():
            return True
    return False


def collect_numeric_assignments_matching(
    value: PDXBlock, variables: dict[str, float], terms: tuple[str, ...]
) -> tuple[dict[str, float], set[str]]:
    modifiers: dict[str, float] = {}
    unresolved: set[str] = set()
    for assignment in iter_assignments(value):
        key = assignment.key.strip('"')
        if not any(term in key.lower() for term in terms):
            continue
        amount, unresolved_variable = _numeric_atom(assignment.value, variables)
        if unresolved_variable:
            unresolved.add(unresolved_variable)
            continue
        modifiers[key] = modifiers.get(key, 0.0) + amount
    return modifiers, unresolved


def sum_modifier_terms(modifiers: dict[str, float], terms: tuple[str, ...]) -> float:
    return sum(amount for key, amount in modifiers.items() if any(term in key.lower() for term in terms))


def strategic_tags_for_object(
    object_type: str,
    object_id: str,
    value: PDXBlock,
    modifiers: dict[str, float],
    direct_output: dict[str, float],
) -> list[str]:
    tags: list[str] = []
    object_lower = object_id.lower()
    if object_type == "building" and classify_colony_class(object_id) == "habitat":
        tags.append("habitat_support_candidate")
    if object_type == "building" and sum_modifier_terms(modifiers, POP_GROWTH_TERMS) > 0:
        tags.append("habitat_growth_center")
    if sum_modifier_terms(modifiers, RESETTLEMENT_SOURCE_TERMS) > 0:
        tags.append("migration_source")
    if sum_modifier_terms(modifiers, RESETTLEMENT_DESTINATION_TERMS) > 0:
        tags.append("migration_destination")
    if object_type == "building" and (
        has_assignment(value, "country_modifier")
        or has_assignment(value, "triggered_country_modifier")
        or has_assignment(value, "empire_limit")
        or has_assignment(value, "is_capital", "yes")
        or "capital" in object_lower
    ):
        tags.append("capital_or_empire_unique_candidate")
    if object_type.startswith("starbase") and any(term in object_lower for term in STARBASE_PRIORITY_TERMS):
        tags.append("starbase_support_candidate")
    if object_type.startswith("starbase") and sum_modifier_terms(modifiers, ("resettlement", "migration")) > 0:
        tags.append("starbase_migration_support")
    if object_type.startswith("starbase") and (
        sum_modifier_terms(modifiers, ("shipyard", "naval_cap")) or any(term in object_lower for term in ("shipyard", "anchorage"))
    ):
        tags.append("starbase_fleet_scaling")
    if object_type.startswith("starbase") and (
        direct_output.get("food", 0.0) > 0
        or direct_output.get("energy", 0.0) > 0
        or direct_output.get("minerals", 0.0) > 0
        or direct_output.get("trade", 0.0) > 0
    ):
        tags.append("starbase_resource_support")
    if has_assignment(value, "can_demolish", "no"):
        tags.append("cannot_demolish")
    if has_assignment(value, "destroy_trigger"):
        tags.append("has_destroy_trigger")
    return sorted(set(tags))


def normalize_job_workforce(amount: float) -> float:
    return amount / JOB_WORKFORCE_UNITS


def job_subject(job_id: str) -> str:
    base = job_id.removeprefix("job_")
    if base.endswith("y"):
        return f"{base[:-1]}ies"
    return f"{base}s"


def resolve_job(jobs: dict[str, dict[str, Any]], job_id: str) -> dict[str, Any] | None:
    return jobs.get(job_id) or jobs.get(job_id.removeprefix("job_"))


def is_research_modifier_key(key: str) -> bool:
    return (
        "research" in key
        and (
            key.endswith("_produces_add")
            or key.endswith("_produces_mult")
            or key.endswith("_upkeep_add")
            or key.endswith("_upkeep_mult")
            or key.endswith("_research_speed_mult")
        )
    )


def collect_numeric_modifier_assignments(
    value: PDXBlock, variables: dict[str, float]
) -> tuple[dict[str, float], set[str]]:
    modifiers: dict[str, float] = {}
    unresolved: set[str] = set()
    for assignment in iter_assignments(value):
        key = assignment.key.strip('"')
        if not is_research_modifier_key(key):
            continue
        amount, unresolved_variable = _numeric_atom(assignment.value, variables)
        if unresolved_variable:
            unresolved.add(unresolved_variable)
            continue
        modifiers[key] = modifiers.get(key, 0.0) + amount
    return modifiers, unresolved


def collect_building_research_modifier_effects(
    value: PDXBlock, variables: dict[str, float]
) -> tuple[dict[str, Any], set[str]]:
    modifiers, unresolved = collect_numeric_modifier_assignments(value, variables)
    job_research_add: dict[str, dict[str, float]] = {}
    job_upkeep_add: dict[str, dict[str, float]] = {}
    job_research_mult: dict[str, float] = {}
    resource_job_mult: dict[str, float] = {}
    upkeep_mult = 0.0
    for key, amount in modifiers.items():
        add_match = re.fullmatch(r"planet_([A-Za-z0-9_]+)_(physics_research|society_research|engineering_research)_produces_add", key)
        if add_match:
            subject, resource = add_match.groups()
            job_research_add.setdefault(subject, {})[resource] = job_research_add.setdefault(subject, {}).get(resource, 0.0) + amount
            continue
        res_mult_match = re.fullmatch(r"planet_jobs_(physics_research|society_research|engineering_research)_produces_mult", key)
        if res_mult_match:
            resource = res_mult_match.group(1)
            resource_job_mult[resource] = resource_job_mult.get(resource, 0.0) + amount
            continue
        upkeep_add_match = re.fullmatch(r"planet_([A-Za-z0-9_]+)_([A-Za-z0-9_]+)_upkeep_add", key)
        if upkeep_add_match:
            subject, resource = upkeep_add_match.groups()
            if resource in SUPPORT_KEYS:
                job_upkeep_add.setdefault(subject, {})[resource] = job_upkeep_add.setdefault(subject, {}).get(resource, 0.0) + amount
            continue
        if key in UPKEEP_MULT_KEYS:
            upkeep_mult += amount
            continue
        mult_match = re.fullmatch(r"planet_([A-Za-z0-9_]+)_produces_mult", key)
        if mult_match:
            job_research_mult[mult_match.group(1)] = job_research_mult.get(mult_match.group(1), 0.0) + amount
            continue
        job_res_mult_match = re.fullmatch(r"planet_([A-Za-z0-9_]+)_(physics_research|society_research|engineering_research)_produces_mult", key)
        if job_res_mult_match:
            subject, resource = job_res_mult_match.groups()
            job_research_mult[f"{subject}:{resource}"] = job_research_mult.get(f"{subject}:{resource}", 0.0) + amount
    return (
        {
            "research_modifier_keys": modifiers,
            "job_research_add": job_research_add,
            "job_upkeep_add": job_upkeep_add,
            "job_research_mult": job_research_mult,
            "resource_job_mult": resource_job_mult,
            "researcher_upkeep_mult": upkeep_mult,
        },
        unresolved,
    )


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
                "category": atom_value(block_assignments(value, "category")[0].value) if block_assignments(value, "category") else "",
                "subject": job_subject(str(row["job_id"])),
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
                **resource_columns("triggered_output", triggered_output),
                **resource_columns("optimistic_output", optimistic_output),
                **resource_columns("base_upkeep", base_upkeep),
                **resource_columns("triggered_upkeep", triggered_upkeep),
                **resource_columns("optimistic_upkeep", optimistic_upkeep),
            }
        )
    return winners


def direct_resource_blocks(
    value: PDXBlock, variables: dict[str, float]
) -> tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, float], set[str]]:
    output: dict[str, float] = {}
    triggered_output: dict[str, float] = {}
    upkeep: dict[str, float] = {}
    triggered_upkeep: dict[str, float] = {}
    unresolved: set[str] = set()
    for resources in block_assignments(value, "resources"):
        if not isinstance(resources.value, PDXBlock):
            continue
        for assignment in block_assignments(resources.value):
            if assignment.key in {"produces", "produced_resources"}:
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(output, amounts)
                unresolved.update(missing)
            elif assignment.key in {"triggered_produces", "triggered_produced_resources"}:
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(triggered_output, amounts)
                unresolved.update(missing)
            elif assignment.key == "upkeep":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(upkeep, amounts)
                unresolved.update(missing)
            elif assignment.key == "triggered_upkeep":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                add_amounts(triggered_upkeep, amounts)
                unresolved.update(missing)
    for ai_production in block_assignments(value, "ai_resource_production"):
        amounts, missing = _collect_resource_amounts(ai_production.value, variables)
        add_amounts(output, amounts)
        unresolved.update(missing)
    return output, triggered_output, upkeep, triggered_upkeep, unresolved


def source_gate_summary(value: PDXBlock) -> dict[str, str]:
    prereqs: list[str] = []
    event_flags: list[str] = []
    unlock_flags: list[str] = []
    gates: list[str] = []
    gate_atoms: list[str] = []
    for assignment in iter_assignments(value):
        key = assignment.key.strip('"')
        if key == "prerequisites":
            prereqs.extend(assignment_atoms(assignment.value))
        elif key in {"feature_flags", "feature_flag", "show_tech_unlock_if"}:
            unlock_flags.extend(assignment_atoms(assignment.value))
        elif key in {"has_country_flag", "set_country_flag", "has_global_flag", "set_global_flag"}:
            event_flags.extend(assignment_atoms(assignment.value))
        elif key in {"potential", "allow", "possible", "trigger"}:
            gates.append(key)
            gate_atoms.extend(assignment_atoms(assignment.value))
    return {
        "prerequisites": compact_list(prereqs),
        "potential_allow_gates": compact_list(gates),
        "potential_allow_gate_atoms": compact_list(gate_atoms),
        "event_flags": compact_list(event_flags),
        "unlock_flags": compact_list(unlock_flags),
    }


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
        direct_output, direct_triggered_output, direct_upkeep, direct_triggered_upkeep, missing_direct = direct_resource_blocks(value, variables)
        direct_optimistic_output = combined_amounts(direct_output, direct_triggered_output)
        direct_optimistic_upkeep = combined_amounts(direct_upkeep, direct_triggered_upkeep)
        modifier_effects, missing_modifiers = collect_building_research_modifier_effects(value, variables)
        gates = source_gate_summary(value)
        job_base_output: dict[str, float] = {}
        job_triggered_output: dict[str, float] = {}
        job_output: dict[str, float] = {}
        job_base_upkeep: dict[str, float] = {}
        job_triggered_upkeep: dict[str, float] = {}
        job_upkeep: dict[str, float] = {}
        job_subject_counts: dict[str, float] = {}
        unknown_jobs: list[str] = []
        for job_id, count in jobs_created.items():
            job = resolve_job(jobs, job_id)
            if not job:
                unknown_jobs.append(job_id)
                continue
            job_equivalents = normalize_job_workforce(count)
            add_amounts(job_base_output, json.loads(str(job["base_output_json"])), job_equivalents)
            add_amounts(job_triggered_output, json.loads(str(job["triggered_output_json"])), job_equivalents)
            add_amounts(job_output, json.loads(str(job["optimistic_output_json"])), job_equivalents)
            add_amounts(job_base_upkeep, json.loads(str(job["base_upkeep_json"])), job_equivalents)
            add_amounts(job_triggered_upkeep, json.loads(str(job["triggered_upkeep_json"])), job_equivalents)
            add_amounts(job_upkeep, json.loads(str(job["optimistic_upkeep_json"])), job_equivalents)
            subject = str(job["subject"])
            category = str(job.get("category", ""))
            job_subject_counts[subject] = job_subject_counts.get(subject, 0.0) + job_equivalents
            if category:
                job_subject_counts[category.removeprefix("planet_")] = (
                    job_subject_counts.get(category.removeprefix("planet_"), 0.0) + job_equivalents
                )
        base_output = combined_amounts(direct_output, job_base_output)
        triggered_output = combined_amounts(direct_triggered_output, job_triggered_output)
        total_output = combined_amounts(base_output, triggered_output)
        base_upkeep = combined_amounts(direct_upkeep, job_base_upkeep)
        triggered_upkeep = combined_amounts(direct_triggered_upkeep, job_triggered_upkeep)
        total_upkeep = combined_amounts(base_upkeep, triggered_upkeep)
        conservative_output = dict(base_output)
        conservative_upkeep = dict(total_upkeep)
        chain = chain_for(object_id, upgrades)
        rows.append(
            {
                "building_id": object_id,
                "colony_class": classify_colony_class(object_id),
                "winning_mod_name": row["name"],
                "winning_file": row["relative_file"],
                "category": atom_value(block_assignments(value, "category")[0].value) if block_assignments(value, "category") else "",
                **gates,
                "is_upgrade_terminal": "yes" if not upgrades.get(object_id) else "no",
                "upgrade_chain_to_terminal": "|".join(chain),
                "upgrade_terminal": chain[-1],
                "jobs_created_json": _json_dump(jobs_created),
                "raw_job_workforce_total": round(sum(max(0.0, amount) for amount in jobs_created.values()), 6),
                "job_slots_total": round(
                    sum(max(0.0, normalize_job_workforce(amount)) for amount in jobs_created.values()), 6
                ),
                "unknown_jobs": "|".join(sorted(unknown_jobs)) or "none",
                "job_subject_counts_json": _json_dump(job_subject_counts),
                "direct_output_json": _json_dump(direct_output),
                "direct_triggered_output_json": _json_dump(direct_triggered_output),
                "direct_optimistic_output_json": _json_dump(direct_optimistic_output),
                "direct_upkeep_json": _json_dump(direct_upkeep),
                "direct_triggered_upkeep_json": _json_dump(direct_triggered_upkeep),
                "direct_optimistic_upkeep_json": _json_dump(direct_optimistic_upkeep),
                "job_base_output_json": _json_dump(job_base_output),
                "job_triggered_output_json": _json_dump(job_triggered_output),
                "job_output_json": _json_dump(job_output),
                "job_base_upkeep_json": _json_dump(job_base_upkeep),
                "job_triggered_upkeep_json": _json_dump(job_triggered_upkeep),
                "job_upkeep_json": _json_dump(job_upkeep),
                "research_modifier_effects_json": _json_dump(modifier_effects),
                "base_output_json": _json_dump(base_output),
                "triggered_output_json": _json_dump(triggered_output),
                "conservative_output_json": _json_dump(conservative_output),
                "optimistic_output_json": _json_dump(total_output),
                "total_output_json": _json_dump(total_output),
                "base_upkeep_json": _json_dump(base_upkeep),
                "triggered_upkeep_json": _json_dump(triggered_upkeep),
                "conservative_upkeep_json": _json_dump(conservative_upkeep),
                "optimistic_upkeep_json": _json_dump(total_upkeep),
                "total_upkeep_json": _json_dump(total_upkeep),
                "base_research": round(research_total(base_output), 6),
                "triggered_research": round(research_total(triggered_output), 6),
                "conservative_research": round(research_total(conservative_output), 6),
                "optimistic_research": round(research_total(total_output), 6),
                "total_research": round(research_total(total_output), 6),
                "direct_research": round(research_total(direct_output), 6),
                "job_research": round(research_total(job_output), 6),
                "modeled_researcher_upkeep_mult": round(float(modifier_effects["researcher_upkeep_mult"]), 6),
                "data_quality_flags": "|".join(
                    flag
                    for flag in [
                        "research_output" if research_total(total_output) > 0 else "",
                        "has_research_modifiers" if modifier_effects["research_modifier_keys"] else "",
                        "has_unknown_jobs" if unknown_jobs else "",
                        "unresolved_variables" if missing_jobs or missing_direct or missing_modifiers else "",
                    ]
                    if flag
                )
                or "none",
                "unresolved_variables": "|".join(sorted(missing_jobs | missing_direct | missing_modifiers)) or "none",
                **resource_columns("base_output", base_output),
                **resource_columns("triggered_output", triggered_output),
                **resource_columns("conservative_output", conservative_output),
                **resource_columns("optimistic_output", total_output),
                **resource_columns("total_output", total_output),
                **resource_columns("base_upkeep", base_upkeep),
                **resource_columns("triggered_upkeep", triggered_upkeep),
                **resource_columns("conservative_upkeep", conservative_upkeep),
                **resource_columns("optimistic_upkeep", total_upkeep),
                **resource_columns("total_upkeep", total_upkeep),
            }
        )
    return rows


def collect_development_rows(playset: dict[str, Any], jobs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    roots = _valuation_stack_roots(playset)
    variables = collect_global_variables([Path(root["root"]) for root in roots])
    definitions = _collect_economic_definitions(playset)
    winners = _winning_economic_definitions(definitions)
    rows: list[dict[str, Any]] = []
    for (object_type, object_id), row in sorted(winners.items()):
        if object_type not in {"district", "zone"} or not isinstance(row.get("value"), PDXBlock):
            continue
        value = row["value"]
        jobs_created, missing_jobs = _collect_job_adds(value, variables)
        direct_output, direct_triggered_output, direct_upkeep, direct_triggered_upkeep, missing_direct = direct_resource_blocks(value, variables)
        direct_optimistic_output = combined_amounts(direct_output, direct_triggered_output)
        direct_optimistic_upkeep = combined_amounts(direct_upkeep, direct_triggered_upkeep)
        gates = source_gate_summary(value)
        job_base_output: dict[str, float] = {}
        job_triggered_output: dict[str, float] = {}
        job_output: dict[str, float] = {}
        job_base_upkeep: dict[str, float] = {}
        job_triggered_upkeep: dict[str, float] = {}
        job_upkeep: dict[str, float] = {}
        unknown_jobs: list[str] = []
        for job_id, count in jobs_created.items():
            job = resolve_job(jobs, job_id)
            if not job:
                unknown_jobs.append(job_id)
                continue
            job_equivalents = normalize_job_workforce(count)
            add_amounts(job_base_output, json.loads(str(job["base_output_json"])), job_equivalents)
            add_amounts(job_triggered_output, json.loads(str(job["triggered_output_json"])), job_equivalents)
            add_amounts(job_output, json.loads(str(job["optimistic_output_json"])), job_equivalents)
            add_amounts(job_base_upkeep, json.loads(str(job["base_upkeep_json"])), job_equivalents)
            add_amounts(job_triggered_upkeep, json.loads(str(job["triggered_upkeep_json"])), job_equivalents)
            add_amounts(job_upkeep, json.loads(str(job["optimistic_upkeep_json"])), job_equivalents)
        base_output = combined_amounts(direct_output, job_base_output)
        triggered_output = combined_amounts(direct_triggered_output, job_triggered_output)
        total_output = combined_amounts(base_output, triggered_output)
        base_upkeep = combined_amounts(direct_upkeep, job_base_upkeep)
        triggered_upkeep = combined_amounts(direct_triggered_upkeep, job_triggered_upkeep)
        total_upkeep = combined_amounts(base_upkeep, triggered_upkeep)
        conservative_output = dict(base_output)
        conservative_upkeep = dict(total_upkeep)
        base_net_resources = net_amounts(base_output, base_upkeep)
        conservative_net_resources = net_amounts(conservative_output, conservative_upkeep)
        net_resources = net_amounts(total_output, total_upkeep)
        rows.append(
            {
                "object_type": object_type,
                "object_id": object_id,
                "colony_class": classify_colony_class(object_id),
                "winning_mod_name": row["name"],
                "winning_file": row["relative_file"],
                **gates,
                "jobs_created_json": _json_dump(jobs_created),
                "raw_job_workforce_total": round(sum(max(0.0, amount) for amount in jobs_created.values()), 6),
                "job_slots_total": round(
                    sum(max(0.0, normalize_job_workforce(amount)) for amount in jobs_created.values()), 6
                ),
                "unknown_jobs": "|".join(sorted(unknown_jobs)) or "none",
                "direct_output_json": _json_dump(direct_output),
                "direct_triggered_output_json": _json_dump(direct_triggered_output),
                "direct_optimistic_output_json": _json_dump(direct_optimistic_output),
                "direct_upkeep_json": _json_dump(direct_upkeep),
                "direct_triggered_upkeep_json": _json_dump(direct_triggered_upkeep),
                "direct_optimistic_upkeep_json": _json_dump(direct_optimistic_upkeep),
                "job_base_output_json": _json_dump(job_base_output),
                "job_triggered_output_json": _json_dump(job_triggered_output),
                "job_output_json": _json_dump(job_output),
                "job_base_upkeep_json": _json_dump(job_base_upkeep),
                "job_triggered_upkeep_json": _json_dump(job_triggered_upkeep),
                "job_upkeep_json": _json_dump(job_upkeep),
                "base_output_json": _json_dump(base_output),
                "triggered_output_json": _json_dump(triggered_output),
                "conservative_output_json": _json_dump(conservative_output),
                "optimistic_output_json": _json_dump(total_output),
                "total_output_json": _json_dump(total_output),
                "base_upkeep_json": _json_dump(base_upkeep),
                "triggered_upkeep_json": _json_dump(triggered_upkeep),
                "conservative_upkeep_json": _json_dump(conservative_upkeep),
                "optimistic_upkeep_json": _json_dump(total_upkeep),
                "total_upkeep_json": _json_dump(total_upkeep),
                "base_net_resources_json": _json_dump(base_net_resources),
                "conservative_net_resources_json": _json_dump(conservative_net_resources),
                "optimistic_net_resources_json": _json_dump(net_resources),
                "net_resources_json": _json_dump(net_resources),
                "base_research": round(research_total(base_output), 6),
                "triggered_research": round(research_total(triggered_output), 6),
                "conservative_research": round(research_total(conservative_output), 6),
                "optimistic_research": round(research_total(total_output), 6),
                "total_research": round(research_total(total_output), 6),
                "net_consumer_goods": round(net_resources.get("consumer_goods", 0.0), 6),
                "net_energy": round(net_resources.get("energy", 0.0), 6),
                "net_minerals": round(net_resources.get("minerals", 0.0), 6),
                "data_quality_flags": "|".join(
                    flag
                    for flag in [
                        "research_output" if research_total(total_output) > 0 else "",
                        "consumer_goods_positive" if net_resources.get("consumer_goods", 0.0) > 0 else "",
                        "consumer_goods_negative" if net_resources.get("consumer_goods", 0.0) < 0 else "",
                        "energy_positive" if net_resources.get("energy", 0.0) > 0 else "",
                        "minerals_positive" if net_resources.get("minerals", 0.0) > 0 else "",
                        "has_unknown_jobs" if unknown_jobs else "",
                        "unresolved_variables" if missing_jobs or missing_direct else "",
                    ]
                    if flag
                )
                or "none",
                "unresolved_variables": "|".join(sorted(missing_jobs | missing_direct)) or "none",
                **resource_columns("base_output", base_output),
                **resource_columns("triggered_output", triggered_output),
                **resource_columns("conservative_output", conservative_output),
                **resource_columns("optimistic_output", total_output),
                **resource_columns("total_output", total_output),
                **resource_columns("base_upkeep", base_upkeep),
                **resource_columns("triggered_upkeep", triggered_upkeep),
                **resource_columns("conservative_upkeep", conservative_upkeep),
                **resource_columns("optimistic_upkeep", total_upkeep),
                **resource_columns("total_upkeep", total_upkeep),
                **resource_columns("base_net", base_net_resources),
                **resource_columns("conservative_net", conservative_net_resources),
                **resource_columns("optimistic_net", net_resources),
                **resource_columns("net", net_resources),
            }
        )
    return rows


def add_nested_amounts(left: dict[str, dict[str, float]], right: dict[str, dict[str, float]]) -> None:
    for outer, inner in right.items():
        bucket = left.setdefault(outer, {})
        for key, value in inner.items():
            bucket[key] = bucket.get(key, 0.0) + float(value)


def aggregate_selected_buildings(selected: list[dict[str, Any]]) -> dict[str, Any]:
    direct_output: dict[str, float] = {}
    job_output: dict[str, float] = {}
    direct_upkeep: dict[str, float] = {}
    job_upkeep: dict[str, float] = {}
    base_output: dict[str, float] = {}
    triggered_output: dict[str, float] = {}
    optimistic_output: dict[str, float] = {}
    base_upkeep: dict[str, float] = {}
    triggered_upkeep: dict[str, float] = {}
    optimistic_upkeep: dict[str, float] = {}
    subject_counts: dict[str, float] = {}
    job_research_add: dict[str, dict[str, float]] = {}
    job_upkeep_add: dict[str, dict[str, float]] = {}
    job_research_mult: dict[str, float] = {}
    resource_job_mult: dict[str, float] = {}
    researcher_upkeep_mult = 0.0
    modifier_keys: dict[str, float] = {}
    for row in selected:
        add_amounts(direct_output, json.loads(str(row["direct_optimistic_output_json"])))
        add_amounts(job_output, json.loads(str(row["job_output_json"])))
        add_amounts(direct_upkeep, json.loads(str(row["direct_optimistic_upkeep_json"])))
        add_amounts(job_upkeep, json.loads(str(row["job_upkeep_json"])))
        add_amounts(base_output, json.loads(str(row["base_output_json"])))
        add_amounts(triggered_output, json.loads(str(row["triggered_output_json"])))
        add_amounts(optimistic_output, json.loads(str(row["optimistic_output_json"])))
        add_amounts(base_upkeep, json.loads(str(row["base_upkeep_json"])))
        add_amounts(triggered_upkeep, json.loads(str(row["triggered_upkeep_json"])))
        add_amounts(optimistic_upkeep, json.loads(str(row["optimistic_upkeep_json"])))
        add_amounts(subject_counts, json.loads(str(row["job_subject_counts_json"])))
        effects = json.loads(str(row["research_modifier_effects_json"]))
        add_nested_amounts(job_research_add, effects.get("job_research_add", {}))
        add_nested_amounts(job_upkeep_add, effects.get("job_upkeep_add", {}))
        add_amounts(job_research_mult, effects.get("job_research_mult", {}))
        add_amounts(resource_job_mult, effects.get("resource_job_mult", {}))
        add_amounts(modifier_keys, effects.get("research_modifier_keys", {}))
        researcher_upkeep_mult += float(effects.get("researcher_upkeep_mult", 0.0))
    conservative_output = dict(base_output)
    conservative_upkeep = dict(optimistic_upkeep)
    adjusted_output = dict(optimistic_output)
    adjusted_upkeep = dict(direct_upkeep)
    adjusted_job_upkeep = dict(job_upkeep)

    for resource in RESEARCH_KEYS:
        additive = sum(subject_counts.get(subject, 0.0) * values.get(resource, 0.0) for subject, values in job_research_add.items())
        mult = resource_job_mult.get(resource, 0.0)
        mult += job_research_mult.get("researchers", 0.0)
        mult += job_research_mult.get(f"researchers:{resource}", 0.0)
        adjusted_output[resource] = direct_output.get(resource, 0.0) + (job_output.get(resource, 0.0) + additive) * (1.0 + mult)

    for subject, values in job_upkeep_add.items():
        subject_count = subject_counts.get(subject, 0.0)
        for resource, amount in values.items():
            adjusted_job_upkeep[resource] = adjusted_job_upkeep.get(resource, 0.0) + subject_count * amount
    for resource, amount in list(adjusted_job_upkeep.items()):
        adjusted_job_upkeep[resource] = amount * (1.0 + researcher_upkeep_mult)
    add_amounts(adjusted_upkeep, adjusted_job_upkeep)

    return {
        "direct_output": direct_output,
        "job_output": job_output,
        "base_output": base_output,
        "triggered_output": triggered_output,
        "conservative_output": conservative_output,
        "optimistic_output": optimistic_output,
        "adjusted_output": adjusted_output,
        "direct_upkeep": direct_upkeep,
        "job_upkeep": job_upkeep,
        "base_upkeep": base_upkeep,
        "triggered_upkeep": triggered_upkeep,
        "conservative_upkeep": conservative_upkeep,
        "optimistic_upkeep": optimistic_upkeep,
        "base_net": net_amounts(base_output, base_upkeep),
        "conservative_net": net_amounts(conservative_output, conservative_upkeep),
        "optimistic_net": net_amounts(optimistic_output, optimistic_upkeep),
        "adjusted_upkeep": adjusted_upkeep,
        "subject_counts": subject_counts,
        "modifier_keys": modifier_keys,
        "job_research_add": job_research_add,
        "job_upkeep_add": job_upkeep_add,
        "job_research_mult": job_research_mult,
        "resource_job_mult": resource_job_mult,
        "researcher_upkeep_mult": researcher_upkeep_mult,
    }


def quota_count(target: float, amount: float) -> int:
    return math.ceil(target / amount) if amount > 0 else 0


def plan_rows(buildings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def research_candidate(row: dict[str, Any]) -> bool:
        if row["is_upgrade_terminal"] != "yes":
            return False
        if float(row["total_research"]) > 0:
            return True
        return "has_research_modifiers" in str(row["data_quality_flags"]).split("|")

    def repeatable_candidate(row: dict[str, Any]) -> bool:
        mod_name = str(row["winning_mod_name"]).lower()
        building_id = str(row["building_id"])
        if "more events" in mod_name or "more primitives" in mod_name:
            return False
        special_prefixes = ("holding_", "building_fe_", "building_organic_", "building_passenger_")
        return not building_id.startswith(special_prefixes)

    def greedy_best(candidates: list[dict[str, Any]], take: int) -> list[dict[str, Any]]:
        selected: list[dict[str, Any]] = []
        remaining = list(candidates)
        def marginal_score(row: dict[str, Any]) -> tuple[float, float, float, str]:
            bundle = aggregate_selected_buildings([*selected, row])
            return (
                research_total(bundle["adjusted_output"]),
                research_total(bundle["base_output"]),
                float(row["total_research"]),
                str(row["building_id"]),
            )

        while remaining and len(selected) < take:
            best_row = max(remaining, key=marginal_score)
            selected.append(best_row)
            remaining.remove(best_row)
        return selected

    scopes = {
        "raw_top_terminal": [row for row in buildings if research_candidate(row)],
        "repeatable_candidate_terminal": [
            row for row in buildings if research_candidate(row) and repeatable_candidate(row)
        ],
    }
    rows: list[dict[str, Any]] = []
    for scope, candidates in scopes.items():
        for slots in (6, 8, 10, 12):
            for take in sorted({1, min(3, len(candidates)), min(slots, len(candidates))}):
                selected = greedy_best(candidates, take)
                bundle = aggregate_selected_buildings(selected)
                base_research = research_total(bundle["base_output"])
                conservative_research = research_total(bundle["conservative_output"])
                optimistic_research = research_total(bundle["optimistic_output"])
                adjusted_research = research_total(bundle["adjusted_output"])
                rows.append(
                    {
                        "scenario": f"{scope}_top_{take}_in_{slots}_slots",
                        "building_slots": slots,
                        "selected_buildings": "|".join(row["building_id"] for row in selected),
                        "research_per_full_colony": round(adjusted_research, 6),
                        "base_research_per_full_colony": round(base_research, 6),
                        "conservative_research_per_full_colony": round(conservative_research, 6),
                        "optimistic_research_per_full_colony": round(optimistic_research, 6),
                        "adjusted_research_per_full_colony": round(adjusted_research, 6),
                        "colonies_for_3000_research": quota_count(3000, adjusted_research),
                        "colonies_for_3000_base_research": quota_count(3000, base_research),
                        "colonies_for_3000_conservative_research": quota_count(3000, conservative_research),
                        "colonies_for_3000_optimistic_research": quota_count(3000, optimistic_research),
                        "colonies_for_3000_adjusted_research": quota_count(3000, adjusted_research),
                        "modeled_researcher_upkeep_mult": round(bundle["researcher_upkeep_mult"], 6),
                        "modifier_keys_json": _json_dump(bundle["modifier_keys"]),
                        "unused_slots": slots - take,
                        **resource_columns("base_output", bundle["base_output"]),
                        **resource_columns("triggered_output", bundle["triggered_output"]),
                        **resource_columns("conservative_output", bundle["conservative_output"]),
                        **resource_columns("optimistic_output", bundle["optimistic_output"]),
                        **resource_columns("adjusted_output", bundle["adjusted_output"]),
                        **resource_columns("base_upkeep", bundle["base_upkeep"]),
                        **resource_columns("triggered_upkeep", bundle["triggered_upkeep"]),
                        **resource_columns("conservative_upkeep", bundle["conservative_upkeep"]),
                        **resource_columns("optimistic_upkeep", bundle["optimistic_upkeep"]),
                        **resource_columns("adjusted_upkeep", bundle["adjusted_upkeep"]),
                        **resource_columns("base_net", bundle["base_net"]),
                        **resource_columns("conservative_net", bundle["conservative_net"]),
                        **resource_columns("optimistic_net", bundle["optimistic_net"]),
                    }
                )
    return rows


def repeatable_building_candidate(row: dict[str, Any]) -> bool:
    mod_name = str(row["winning_mod_name"]).lower()
    building_id = str(row["building_id"])
    if "more events" in mod_name or "more primitives" in mod_name:
        return False
    special_prefixes = ("holding_", "building_fe_", "building_organic_", "building_passenger_")
    return not building_id.startswith(special_prefixes)


def build_plan_building_candidate(row: dict[str, Any]) -> bool:
    if not repeatable_building_candidate(row):
        return False
    building_id = str(row["building_id"]).lower()
    mod_name = str(row["winning_mod_name"]).lower()
    blocked_terms = (
        "capital",
        "primitive",
        "branch_office",
        "aeternum",
        "katzen",
        "ancient_palace",
        "fallen_empire",
        "lost_emperor",
    )
    if any(term in building_id or term in mod_name for term in blocked_terms):
        return False
    return True


def cell_items(value: Any) -> list[str]:
    text = str(value or "").strip()
    if not text or text == "none":
        return []
    return [item for item in text.split("|") if item]


def readiness_phase(row: dict[str, Any]) -> str:
    if cell_items(row.get("prerequisites")):
        return "after_prerequisite"
    if cell_items(row.get("unlock_flags")):
        return "after_feature_unlock"
    if cell_items(row.get("event_flags")):
        return "after_event_flag"
    if cell_items(row.get("potential_allow_gates")):
        return "conditional_scripted"
    return "base_available"


def primary_building_role(row: dict[str, Any]) -> tuple[str, float]:
    output = json.loads(str(row["optimistic_output_json"]))
    upkeep = json.loads(str(row["optimistic_upkeep_json"]))
    net = net_amounts(output, upkeep)
    if "has_research_modifiers" in str(row.get("data_quality_flags", "")).split("|"):
        return "research_world", max(0.0, research_total(output))
    best_role = "support"
    best_score = 0.0
    for role in ROLE_TARGETS:
        score = max(role_total(output, role), role_total(net, role))
        if score > best_score:
            best_role = role
            best_score = score
    return best_role, best_score


def has_capital_tier_gate(row: dict[str, Any]) -> str:
    text = "|".join(
        [
            str(row.get("prerequisites", "")),
            str(row.get("potential_allow_gate_atoms", "")),
            str(row.get("event_flags", "")),
            str(row.get("unlock_flags", "")),
        ]
    ).lower()
    terms = ("capital", "building_capital", "planetary_administration", "planetary_capital", "system_capital")
    return "yes" if any(term in text for term in terms) else "no"


def build_plan_readiness_rows(buildings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for row in buildings:
        role, role_score = primary_building_role(row)
        phase = readiness_phase(row)
        build_plan_candidate = build_plan_building_candidate(row)
        gate_reasons = []
        if cell_items(row.get("prerequisites")):
            gate_reasons.append("technology_prerequisite")
        if cell_items(row.get("unlock_flags")):
            gate_reasons.append("feature_unlock")
        if cell_items(row.get("event_flags")):
            gate_reasons.append("event_flag")
        if cell_items(row.get("potential_allow_gates")):
            gate_reasons.append("scripted_potential_allow")
        if not build_plan_candidate:
            gate_reasons.append("not_build_plan_candidate")
        enriched.append(
            {
                **row,
                "_primary_role": role,
                "_primary_role_score": role_score,
                "_readiness_phase": phase,
                "_build_plan_candidate": build_plan_candidate,
                "_gate_reasons": gate_reasons,
                "_capital_tier_gate": has_capital_tier_gate(row),
            }
        )

    fallback_pool = [
        row
        for row in enriched
        if row["_build_plan_candidate"]
        and row["_readiness_phase"] in {"base_available", "conditional_scripted"}
        and row["is_upgrade_terminal"] == "yes"
    ]
    rows: list[dict[str, Any]] = []
    for row in enriched:
        fallback = None
        if row["_readiness_phase"] != "base_available":
            candidates = [
                candidate
                for candidate in fallback_pool
                if candidate["_primary_role"] == row["_primary_role"] and candidate["building_id"] != row["building_id"]
            ]
            if candidates:
                fallback = max(
                    candidates,
                    key=lambda item: (
                        float(item["_primary_role_score"]),
                        float(item.get("job_slots_total", 0.0)),
                        str(item["building_id"]),
                    ),
                )
        rows.append(
            {
                "building_id": row["building_id"],
                "primary_role": row["_primary_role"],
                "primary_role_score": round(float(row["_primary_role_score"]), 6),
                "readiness_phase": row["_readiness_phase"],
                "gate_reasons": compact_list(row["_gate_reasons"]),
                "build_plan_candidate": "yes" if row["_build_plan_candidate"] else "no",
                "repeatable_candidate": "yes" if repeatable_building_candidate(row) else "no",
                "capital_tier_gate": row["_capital_tier_gate"],
                "fallback_building_id": str(fallback["building_id"]) if fallback else "",
                "fallback_primary_role_score": round(float(fallback["_primary_role_score"]), 6) if fallback else 0.0,
                "fallback_reason": "same_role_available_before_target_unlock" if fallback else "",
                "readiness_status": "fallback_available" if fallback else row["_readiness_phase"],
                "prerequisites": row.get("prerequisites", ""),
                "potential_allow_gates": row.get("potential_allow_gates", ""),
                "potential_allow_gate_atoms": row.get("potential_allow_gate_atoms", ""),
                "event_flags": row.get("event_flags", ""),
                "unlock_flags": row.get("unlock_flags", ""),
                "is_upgrade_terminal": row["is_upgrade_terminal"],
                "upgrade_terminal": row["upgrade_terminal"],
                "upgrade_chain_to_terminal": row["upgrade_chain_to_terminal"],
                "colony_class": row["colony_class"],
                "category": row["category"],
                "winning_mod_name": row["winning_mod_name"],
                "winning_file": row["winning_file"],
            }
        )
    return sorted(rows, key=lambda item: (str(item["primary_role"]), str(item["readiness_phase"]), str(item["building_id"])))


def building_bundle_for_role(selected: list[dict[str, Any]], role: str) -> dict[str, dict[str, float]]:
    if role == "research_world":
        bundle = aggregate_selected_buildings(selected)
        output = dict(bundle["adjusted_output"])
        upkeep = dict(bundle["adjusted_upkeep"])
        return {"output": output, "upkeep": upkeep, "net": net_amounts(output, upkeep)}
    output: dict[str, float] = {}
    upkeep: dict[str, float] = {}
    for row in selected:
        total_output = json.loads(str(row["total_output_json"]))
        total_upkeep = json.loads(str(row["total_upkeep_json"]))
        add_amounts(output, total_output)
        add_amounts(upkeep, total_upkeep)
    return {"output": output, "upkeep": upkeep, "net": net_amounts(output, upkeep)}


def role_building_candidates(buildings: list[dict[str, Any]], role: str, candidate_scope: str) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for row in buildings:
        if row["is_upgrade_terminal"] != "yes":
            continue
        if candidate_scope == "repeatable" and not repeatable_building_candidate(row):
            continue
        if candidate_scope == "build_plan" and not build_plan_building_candidate(row):
            continue
        bundle = building_bundle_for_role([row], role)
        if role_total(bundle["output"], role) > 0 or role_total(bundle["net"], role) > 0:
            candidates.append(row)
            continue
        if role == "research_world" and "has_research_modifiers" in str(row["data_quality_flags"]).split("|"):
            candidates.append(row)
    return candidates


def greedy_role_buildings(candidates: list[dict[str, Any]], role: str, take: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    remaining = list(candidates)

    def marginal_score(row: dict[str, Any]) -> tuple[float, float, float, str]:
        bundle = building_bundle_for_role([*selected, row], role)
        return (
            role_total(bundle["net"], role),
            role_total(bundle["output"], role),
            float(row.get("job_slots_total", 0.0)),
            str(row["building_id"]),
        )

    while remaining and len(selected) < take:
        best_row = max(remaining, key=marginal_score)
        selected.append(best_row)
        remaining.remove(best_row)
    return selected


def role_bundle_row(
    role: str,
    build_plan_family: str,
    source_scope: str,
    colony_class: str,
    slots: int,
    selected_objects: list[str],
    bundle: dict[str, dict[str, float]],
) -> dict[str, Any]:
    return {
        "role": role,
        "build_plan_family": build_plan_family,
        "source_scope": source_scope,
        "colony_class": colony_class,
        "slots": slots,
        "selected_count": len(selected_objects),
        "selected_objects": "|".join(selected_objects),
        "gross_role_output": round(role_total(bundle["output"], role), 6),
        "net_role_output": round(role_total(bundle["net"], role), 6),
        **resource_columns("output", bundle["output"]),
        **resource_columns("upkeep", bundle["upkeep"]),
        **resource_columns("net", bundle["net"]),
    }


def modeled_resource_total(amounts: dict[str, float]) -> float:
    return sum(max(0.0, float(amounts.get(key, 0.0))) for key in (*RESEARCH_KEYS, *SUPPORT_KEYS))


def role_family_bundle_row(
    role: str,
    source_scope: str,
    colony_class: str,
    selected_objects: list[str],
    output: dict[str, float],
    upkeep: dict[str, float],
    extra_score: float = 0.0,
) -> dict[str, Any]:
    net = net_amounts(output, upkeep)
    return {
        "role": role,
        "build_plan_family": role,
        "source_scope": source_scope,
        "colony_class": colony_class,
        "slots": 0,
        "selected_count": len(selected_objects),
        "selected_objects": "|".join(selected_objects),
        "gross_role_output": round(modeled_resource_total(output) + extra_score, 6),
        "net_role_output": round(modeled_resource_total(net) + extra_score, 6),
        **resource_columns("output", output),
        **resource_columns("upkeep", upkeep),
        **resource_columns("net", net),
    }


def add_development_family_rows(rows: list[dict[str, Any]], development_rows: list[dict[str, Any]]) -> None:
    family_classes = {
        "habitat_support_center": {"habitat"},
        "ring_world": {"ring_world"},
        "arcology_world": {"arcology"},
        "frameworld": {"frameworld"},
        "birch_world": {"birch_world"},
        "gigas_special_world": {"alderson_disk", "frameworld", "birch_world"},
    }
    for family, classes in family_classes.items():
        candidates = []
        for row in development_rows:
            if str(row["colony_class"]) not in classes:
                continue
            output = json.loads(str(row["optimistic_output_json"]))
            upkeep = json.loads(str(row["optimistic_upkeep_json"]))
            net = net_amounts(output, upkeep)
            score = modeled_resource_total(output) + modeled_resource_total(net)
            candidates.append((score, row, output, upkeep))
        if not candidates:
            continue
        ordered = sorted(candidates, key=lambda item: (item[0], str(item[1]["object_id"])), reverse=True)
        for take in sorted({1, min(3, len(ordered)), min(6, len(ordered))}):
            output: dict[str, float] = {}
            upkeep: dict[str, float] = {}
            selected_objects: list[str] = []
            for _score, row, row_output, row_upkeep in ordered[:take]:
                add_amounts(output, row_output)
                add_amounts(upkeep, row_upkeep)
                selected_objects.append(f"{row['object_type']}:{row['object_id']}")
            rows.append(
                role_family_bundle_row(
                    role=family,
                    source_scope=f"development_family_top_{take}",
                    colony_class="|".join(sorted(classes)),
                    selected_objects=selected_objects,
                    output=output,
                    upkeep=upkeep,
                )
            )


def add_strategic_family_rows(rows: list[dict[str, Any]], strategic_rows: list[dict[str, Any]]) -> None:
    strategic_roles = {"capital_world", "habitat_growth_center", "habitat_support_center"}
    for role in sorted(strategic_roles):
        candidates = [row for row in strategic_rows if str(row["role"]) == role]
        if not candidates:
            continue
        ordered = sorted(
            candidates,
            key=lambda item: (float(item["priority_score"]), str(item["object_id"])),
            reverse=True,
        )
        for take in sorted({1, min(3, len(ordered)), min(6, len(ordered))}):
            output: dict[str, float] = {}
            upkeep: dict[str, float] = {}
            selected_objects: list[str] = []
            extra_score = 0.0
            for row in ordered[:take]:
                add_amounts(output, json.loads(str(row["direct_optimistic_output_json"])))
                add_amounts(upkeep, json.loads(str(row["direct_optimistic_upkeep_json"])))
                selected_objects.append(f"{row['object_type']}:{row['object_id']}")
                extra_score += float(row["priority_score"])
            rows.append(
                role_family_bundle_row(
                    role=role,
                    source_scope=f"strategic_family_top_{take}",
                    colony_class="strategic_infrastructure",
                    selected_objects=selected_objects,
                    output=output,
                    upkeep=upkeep,
                    extra_score=extra_score,
                )
            )


def role_target_rows(
    buildings: list[dict[str, Any]], development_rows: list[dict[str, Any]], strategic_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for role in ROLE_TARGETS:
        for candidate_scope, source_scope in (
            ("raw", "raw_terminal_buildings"),
            ("repeatable", "repeatable_terminal_buildings"),
            ("build_plan", "build_plan_candidate_terminal_buildings"),
        ):
            candidates = role_building_candidates(buildings, role, candidate_scope)
            for slots in (6, 8, 10, 12):
                take = min(slots, len(candidates))
                if take <= 0:
                    continue
                selected = greedy_role_buildings(candidates, role, take)
                bundle = building_bundle_for_role(selected, role)
                rows.append(
                    role_bundle_row(
                        role=role,
                        build_plan_family=role,
                        source_scope=f"{source_scope}_{take}_in_{slots}_slots",
                        colony_class="building_slots_any_colony",
                        slots=slots,
                        selected_objects=[str(row["building_id"]) for row in selected],
                        bundle=bundle,
                    )
                )

        development_candidates = []
        for row in development_rows:
            output = json.loads(str(row["total_output_json"]))
            upkeep = json.loads(str(row["total_upkeep_json"]))
            bundle = {"output": output, "upkeep": upkeep, "net": net_amounts(output, upkeep)}
            if role_total(bundle["output"], role) > 0 or role_total(bundle["net"], role) > 0:
                development_candidates.append((row, bundle))

        classes = sorted({str(row["colony_class"]) for row, _bundle in development_candidates})
        for colony_class in ["all_colony_classes", *classes]:
            class_candidates = [
                (row, bundle)
                for row, bundle in development_candidates
                if colony_class == "all_colony_classes" or row["colony_class"] == colony_class
            ]
            if not class_candidates:
                continue
            ordered = sorted(
                class_candidates,
                key=lambda item: (role_total(item[1]["net"], role), role_total(item[1]["output"], role), str(item[0]["object_id"])),
                reverse=True,
            )
            for take in sorted({1, min(3, len(ordered)), min(6, len(ordered))}):
                selected_pairs = ordered[:take]
                output: dict[str, float] = {}
                upkeep: dict[str, float] = {}
                selected_objects: list[str] = []
                for row, bundle in selected_pairs:
                    add_amounts(output, bundle["output"])
                    add_amounts(upkeep, bundle["upkeep"])
                    selected_objects.append(f"{row['object_type']}:{row['object_id']}")
                rows.append(
                    role_bundle_row(
                        role=role,
                        build_plan_family=role,
                        source_scope=f"development_top_{take}",
                        colony_class=colony_class,
                        slots=0,
                        selected_objects=selected_objects,
                        bundle={"output": output, "upkeep": upkeep, "net": net_amounts(output, upkeep)},
                    )
                )
    add_development_family_rows(rows, development_rows)
    add_strategic_family_rows(rows, strategic_rows)
    return sorted(rows, key=lambda item: (str(item["role"]), str(item["source_scope"]), str(item["colony_class"])))


def collect_technology_modifier_rows(playset: dict[str, Any]) -> list[dict[str, Any]]:
    roots = _valuation_stack_roots(playset)
    variables = collect_global_variables([Path(root["root"]) for root in roots])
    winners: dict[str, dict[str, Any]] = {}
    for root_info in roots:
        root = Path(root_info["root"])
        folder = root / "common" / "technology"
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
                        "technology_id": assignment.key,
                        "relative_file": str(path.relative_to(root)),
                        "value": assignment.value,
                    }
    rows: list[dict[str, Any]] = []
    for tech_id, row in sorted(winners.items()):
        modifiers, unresolved = collect_numeric_modifier_assignments(row["value"], variables)
        if not modifiers:
            continue
        rows.append(
            {
                "technology_id": tech_id,
                "winning_mod_name": row["name"],
                "winning_file": row["relative_file"],
                "modifier_keys_json": _json_dump(modifiers),
                "planet_researcher_or_job_output_mult": round(
                    sum(
                        amount
                        for key, amount in modifiers.items()
                        if (
                            key.startswith("planet_researchers_") and key.endswith("_produces_mult")
                        ) or (
                            key.startswith("planet_jobs_") and key.endswith("_research_produces_mult")
                        )
                    ),
                    6,
                ),
                "station_research_output_mult": round(
                    sum(amount for key, amount in modifiers.items() if key.startswith("station_researchers_")),
                    6,
                ),
                "research_speed_mult": round(
                    sum(amount for key, amount in modifiers.items() if key.endswith("_research_speed_mult")),
                    6,
                ),
                "researcher_upkeep_mult": round(
                    sum(amount for key, amount in modifiers.items() if key in UPKEEP_MULT_KEYS),
                    6,
                ),
                "unresolved_variables": "|".join(sorted(unresolved)) or "none",
            }
        )
    return rows


def collect_winning_folder_definitions(playset: dict[str, Any], folders: dict[str, str]) -> dict[tuple[str, str], dict[str, Any]]:
    winners: dict[tuple[str, str], dict[str, Any]] = {}
    for root_info in _valuation_stack_roots(playset):
        root = Path(root_info["root"])
        common = root / "common"
        if not common.exists():
            continue
        for folder, object_type in folders.items():
            folder_path = common / folder
            if not folder_path.exists():
                continue
            for path in iter_text_files(folder_path):
                try:
                    parsed = parse_file(path)
                except PDXParseError:
                    continue
                for assignment in block_assignments(parsed):
                    if assignment.key.startswith("@") or not isinstance(assignment.value, PDXBlock):
                        continue
                    key = (object_type, assignment.key)
                    current = winners.get(key)
                    if current is None or int(root_info["load_position"]) >= int(current["load_position"]):
                        winners[key] = {
                            **root_info,
                            "object_type": object_type,
                            "object_id": assignment.key,
                            "relative_file": str(path.relative_to(root)),
                            "value": assignment.value,
                        }
    return winners


def strategic_priority_score(object_type: str, tags: list[str], modifiers: dict[str, float], output: dict[str, float]) -> float:
    score = 0.0
    score += max(0.0, sum_modifier_terms(modifiers, POP_GROWTH_TERMS)) * 25.0
    score += max(0.0, sum_modifier_terms(modifiers, RESETTLEMENT_SOURCE_TERMS)) * 100.0
    score += max(0.0, sum_modifier_terms(modifiers, RESETTLEMENT_DESTINATION_TERMS)) * 50.0
    score += max(0.0, sum_modifier_terms(modifiers, CAPITAL_STRATEGIC_TERMS)) * 25.0
    score += len([tag for tag in tags if tag in {"capital_or_empire_unique_candidate", "starbase_support_candidate"}]) * 10.0
    if "starbase_migration_support" in tags:
        score += 150.0
    if "starbase_fleet_scaling" in tags:
        score += 50.0
    if "starbase_resource_support" in tags:
        score += 15.0 + sum(max(0.0, output.get(key, 0.0)) for key in SUPPORT_KEYS)
    if "habitat_support_candidate" in tags:
        score += 5.0
    if object_type in {"district", "zone"} and "habitat_growth_center" in tags:
        score += 25.0
    return round(score, 6)


def strategic_infrastructure_rows(playset: dict[str, Any]) -> list[dict[str, Any]]:
    roots = _valuation_stack_roots(playset)
    variables = collect_global_variables([Path(root["root"]) for root in roots])
    definitions = _collect_economic_definitions(playset)
    winners = _winning_economic_definitions(definitions)
    winners.update(
        collect_winning_folder_definitions(
            playset,
            {
                "starbase_buildings": "starbase_building",
                "starbase_modules": "starbase_module",
            },
        )
    )
    rows: list[dict[str, Any]] = []
    for (object_type, object_id), row in sorted(winners.items()):
        value = row.get("value")
        if not isinstance(value, PDXBlock):
            continue
        modifiers, missing_modifiers = collect_numeric_assignments_matching(value, variables, STRATEGIC_MODIFIER_TERMS)
        output, triggered_output, upkeep, triggered_upkeep, missing_resources = direct_resource_blocks(value, variables)
        optimistic_output = combined_amounts(output, triggered_output)
        optimistic_upkeep = combined_amounts(upkeep, triggered_upkeep)
        tags = strategic_tags_for_object(object_type, object_id, value, modifiers, output)
        if not tags and not modifiers:
            continue
        role = "strategic_support"
        if "capital_or_empire_unique_candidate" in tags:
            role = "capital_world"
        if "habitat_growth_center" in tags:
            role = "habitat_growth_center"
        elif "habitat_support_candidate" in tags:
            role = "habitat_support_center"
        if "starbase_migration_support" in tags:
            role = "starbase_migration_support"
        elif "starbase_fleet_scaling" in tags:
            role = "starbase_fleet_scaling"
        elif "starbase_resource_support" in tags:
            role = "starbase_resource_support"
        rows.append(
            {
                "role": role,
                "object_type": object_type,
                "object_id": object_id,
                "colony_class": classify_colony_class(object_id),
                "strategic_tags": "|".join(tags) or "none",
                "priority_score": strategic_priority_score(object_type, tags, modifiers, output),
                "pop_growth_or_assembly": round(sum_modifier_terms(modifiers, POP_GROWTH_TERMS), 6),
                "resettlement_source_mult": round(sum_modifier_terms(modifiers, RESETTLEMENT_SOURCE_TERMS), 6),
                "resettlement_destination_mult": round(sum_modifier_terms(modifiers, RESETTLEMENT_DESTINATION_TERMS), 6),
                "capital_or_diplomacy_modifier": round(sum_modifier_terms(modifiers, CAPITAL_STRATEGIC_TERMS), 6),
                "can_demolish": assignment_value_text(block_assignments(value, "can_demolish")[0].value)
                if block_assignments(value, "can_demolish")
                else "default",
                "can_build": assignment_value_text(block_assignments(value, "can_build")[0].value)
                if block_assignments(value, "can_build")
                else "default",
                "can_be_disabled": assignment_value_text(block_assignments(value, "can_be_disabled")[0].value)
                if block_assignments(value, "can_be_disabled")
                else "default",
                "has_destroy_trigger": "yes" if has_assignment(value, "destroy_trigger") else "no",
                "has_country_modifier": "yes"
                if has_assignment(value, "country_modifier") or has_assignment(value, "triggered_country_modifier")
                else "no",
                "has_empire_limit": "yes" if has_assignment(value, "empire_limit") else "no",
                "requires_capital": "yes" if has_assignment(value, "is_capital", "yes") else "no",
                "winning_mod_name": row["name"],
                "winning_file": row["relative_file"],
                "modifier_keys_json": _json_dump(modifiers),
                "direct_output_json": _json_dump(output),
                "direct_triggered_output_json": _json_dump(triggered_output),
                "direct_optimistic_output_json": _json_dump(optimistic_output),
                "direct_upkeep_json": _json_dump(upkeep),
                "direct_triggered_upkeep_json": _json_dump(triggered_upkeep),
                "direct_optimistic_upkeep_json": _json_dump(optimistic_upkeep),
                "unresolved_variables": "|".join(sorted(missing_modifiers | missing_resources)) or "none",
                **resource_columns("direct_output", output),
                **resource_columns("direct_triggered_output", triggered_output),
                **resource_columns("direct_optimistic_output", optimistic_output),
                **resource_columns("direct_upkeep", upkeep),
                **resource_columns("direct_triggered_upkeep", triggered_upkeep),
                **resource_columns("direct_optimistic_upkeep", optimistic_upkeep),
            }
        )
    return sorted(rows, key=lambda item: (str(item["role"]), -float(item["priority_score"]), str(item["object_id"])))


def matching_modifier_keys(modifiers: dict[str, float], terms: tuple[str, ...]) -> list[str]:
    return sorted(key for key in modifiers if any(term in key.lower() for term in terms))


def direct_resource_benefit_amount(row: dict[str, Any]) -> float:
    output = json.loads(str(row.get("direct_optimistic_output_json", "{}") or "{}"))
    return sum(max(0.0, float(output.get(key, 0.0))) for key in SUPPORT_KEYS)


def strategic_benefit_taxonomy_rows(strategic_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen_classes: set[str] = set()
    for row in strategic_rows:
        modifiers = json.loads(str(row.get("modifier_keys_json", "{}") or "{}"))
        tags = cell_items(row.get("strategic_tags"))
        object_type = str(row["object_type"])
        object_id = str(row["object_id"])
        object_text = f"{object_type}|{object_id}|{'|'.join(tags)}".lower()
        for benefit_class, terms in BENEFIT_CLASS_TERMS.items():
            modifier_keys = matching_modifier_keys(modifiers, terms)
            tag_hits = [tag for tag in tags if any(term in tag.lower() for term in terms)]
            text_hit = any(term in object_text for term in terms)
            amount = sum(float(modifiers[key]) for key in modifier_keys)
            if benefit_class == "direct_resource_support":
                amount = direct_resource_benefit_amount(row)
            if benefit_class == "empire_country_modifier":
                text_hit = text_hit or str(row.get("has_country_modifier", "")) == "yes" or str(row.get("has_empire_limit", "")) == "yes"
            if benefit_class == "starbase_support":
                text_hit = text_hit or object_type.startswith("starbase")
            if not modifier_keys and not tag_hits and not text_hit and amount == 0:
                continue
            seen_classes.add(benefit_class)
            if amount != 0:
                evidence_kind = "numeric_modifier" if modifier_keys else "direct_resource"
                valuation_status = "numeric_value_preserved"
            elif modifier_keys:
                evidence_kind = "numeric_modifier_zero_sum"
                valuation_status = "numeric_value_preserved"
            elif tag_hits:
                evidence_kind = "strategic_tag"
                valuation_status = "detected_unvalued"
            else:
                evidence_kind = "text_or_structural_signal"
                valuation_status = "detected_unvalued"
            rows.append(
                {
                    "benefit_class": benefit_class,
                    "object_type": object_type,
                    "object_id": object_id,
                    "role": row["role"],
                    "strategic_tags": row["strategic_tags"],
                    "evidence_kind": evidence_kind,
                    "valuation_status": valuation_status,
                    "formula_status": "resource_or_modifier_amount" if amount != 0 or modifier_keys else "detected_no_formula",
                    "benefit_amount": round(amount, 6),
                    "source_terms": "|".join(terms),
                    "matched_modifier_keys": "|".join(modifier_keys),
                    "matched_tags": "|".join(tag_hits),
                    "priority_score": row["priority_score"],
                    "can_demolish": row["can_demolish"],
                    "can_build": row["can_build"],
                    "can_be_disabled": row["can_be_disabled"],
                    "has_destroy_trigger": row["has_destroy_trigger"],
                    "winning_mod_name": row["winning_mod_name"],
                    "winning_file": row["winning_file"],
                }
            )
    for benefit_class, terms in sorted(BENEFIT_CLASS_TERMS.items()):
        if benefit_class in seen_classes:
            continue
        rows.append(
            {
                "benefit_class": benefit_class,
                "object_type": "",
                "object_id": "",
                "role": "",
                "strategic_tags": "",
                "evidence_kind": "no_active_stack_evidence",
                "valuation_status": "not_observed",
                "formula_status": "not_observed",
                "benefit_amount": 0.0,
                "source_terms": "|".join(terms),
                "matched_modifier_keys": "",
                "matched_tags": "",
                "priority_score": 0.0,
                "can_demolish": "",
                "can_build": "",
                "can_be_disabled": "",
                "has_destroy_trigger": "",
                "winning_mod_name": "",
                "winning_file": "",
            }
        )
    return sorted(rows, key=lambda item: (str(item["benefit_class"]), str(item["object_type"]), str(item["object_id"])))


def add_blocker_row(
    rows: list[dict[str, Any]],
    source_artifact: str,
    object_type: str,
    object_id: str,
    issue_type: str,
    issue_key: str,
    accounting_status: str,
    next_action: str,
    source_mod: str = "",
    source_file: str = "",
) -> None:
    rows.append(
        {
            "source_artifact": source_artifact,
            "object_type": object_type,
            "object_id": object_id,
            "issue_type": issue_type,
            "issue_key": issue_key,
            "accounting_status": accounting_status,
            "next_action": next_action,
            "source_mod": source_mod,
            "source_file": source_file,
        }
    )


def modeling_blocker_accounting_rows(
    buildings: list[dict[str, Any]],
    development_rows: list[dict[str, Any]],
    strategic_rows: list[dict[str, Any]],
    resource_coverage_rows: list[dict[str, Any]],
    benefit_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in buildings:
        for job_id in cell_items(row.get("unknown_jobs")):
            add_blocker_row(
                rows,
                "buildings",
                "building",
                str(row["building_id"]),
                "unknown_job",
                job_id,
                "source_reference_unresolved",
                "Resolve job alias/source or record a source-backed exclusion before build-plan consumption.",
                str(row["winning_mod_name"]),
                str(row["winning_file"]),
            )
        for variable in cell_items(row.get("unresolved_variables")):
            add_blocker_row(
                rows,
                "buildings",
                "building",
                str(row["building_id"]),
                "unresolved_variable",
                variable,
                "variable_value_unresolved",
                "Resolve global/local variable value or preserve as conservative blocker.",
                str(row["winning_mod_name"]),
                str(row["winning_file"]),
            )
        for flag in cell_items(row.get("data_quality_flags")):
            add_blocker_row(
                rows,
                "buildings",
                "building",
                str(row["building_id"]),
                "data_quality_flag",
                flag,
                "tracked_quality_flag",
                "Review before using this row for final build-plan scoring.",
                str(row["winning_mod_name"]),
                str(row["winning_file"]),
            )
    for row in development_rows:
        for job_id in cell_items(row.get("unknown_jobs")):
            add_blocker_row(
                rows,
                "development",
                str(row["object_type"]),
                str(row["object_id"]),
                "unknown_job",
                job_id,
                "source_reference_unresolved",
                "Resolve job alias/source or record a source-backed exclusion before build-plan consumption.",
                str(row["winning_mod_name"]),
                str(row["winning_file"]),
            )
        for variable in cell_items(row.get("unresolved_variables")):
            add_blocker_row(
                rows,
                "development",
                str(row["object_type"]),
                str(row["object_id"]),
                "unresolved_variable",
                variable,
                "variable_value_unresolved",
                "Resolve global/local variable value or preserve as conservative blocker.",
                str(row["winning_mod_name"]),
                str(row["winning_file"]),
            )
        for flag in cell_items(row.get("data_quality_flags")):
            add_blocker_row(
                rows,
                "development",
                str(row["object_type"]),
                str(row["object_id"]),
                "data_quality_flag",
                flag,
                "tracked_quality_flag",
                "Review before using this row for final build-plan scoring.",
                str(row["winning_mod_name"]),
                str(row["winning_file"]),
            )
    for row in strategic_rows:
        for variable in cell_items(row.get("unresolved_variables")):
            add_blocker_row(
                rows,
                "strategic_infrastructure",
                str(row["object_type"]),
                str(row["object_id"]),
                "unresolved_variable",
                variable,
                "variable_value_unresolved",
                "Resolve global/local variable value or preserve as conservative blocker.",
                str(row["winning_mod_name"]),
                str(row["winning_file"]),
            )
    for row in resource_coverage_rows:
        if row.get("normal_column_status") == "unsupported":
            add_blocker_row(
                rows,
                "resource_coverage",
                "resource",
                str(row["resource_key"]),
                "unsupported_resource",
                str(row["resource_key"]),
                "unsupported_resource_detected",
                str(row.get("unsupported_reason", "")),
            )
    for row in benefit_rows:
        if row.get("valuation_status") in {"detected_unvalued", "not_observed"}:
            add_blocker_row(
                rows,
                "benefit_taxonomy",
                str(row.get("object_type", "")),
                str(row.get("object_id", "")),
                "benefit_formula_status",
                str(row["benefit_class"]),
                str(row["valuation_status"]),
                "Define formula/consumer policy or keep source-backed detected-only status.",
                str(row.get("winning_mod_name", "")),
                str(row.get("winning_file", "")),
            )
    return sorted(rows, key=lambda item: (str(item["issue_type"]), str(item["source_artifact"]), str(item["object_id"]), str(item["issue_key"])))


def modeling_resource_coverage_rows(
    job_rows: list[dict[str, Any]],
    buildings: list[dict[str, Any]],
    development_rows: list[dict[str, Any]],
    strategic_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    artifacts = {
        "jobs": job_rows,
        "buildings": buildings,
        "development": development_rows,
        "strategic_infrastructure": strategic_rows,
    }
    usage: dict[str, dict[str, Any]] = {}
    for artifact, rows in artifacts.items():
        for row in rows:
            row_id = str(row.get("job_id") or row.get("building_id") or row.get("object_id") or "")
            for column in RESOURCE_AMOUNT_JSON_COLUMNS[artifact]:
                data = json.loads(str(row.get(column, "{}") or "{}"))
                if not isinstance(data, dict):
                    continue
                for resource, amount in data.items():
                    if not isinstance(amount, (int, float)) or amount == 0:
                        continue
                    bucket = usage.setdefault(
                        resource,
                        {
                            "resource_key": resource,
                            "artifacts_seen": set(),
                            "output_rows": set(),
                            "upkeep_rows": set(),
                            "net_rows": set(),
                        },
                    )
                    bucket["artifacts_seen"].add(artifact)
                    if "upkeep" in column:
                        bucket["upkeep_rows"].add((artifact, row_id))
                    elif column.startswith("net_"):
                        bucket["net_rows"].add((artifact, row_id))
                    else:
                        bucket["output_rows"].add((artifact, row_id))

    modeled_resources = {*RESEARCH_KEYS, *SUPPORT_KEYS}
    rows: list[dict[str, Any]] = []
    for resource, data in sorted(usage.items()):
        modeled = resource in modeled_resources
        if resource in RESEARCH_KEYS:
            category = "research"
        elif resource.startswith("giga_sr_"):
            category = "gigas_custom_resource"
        else:
            category = "resource"
        rows.append(
            {
                "resource_key": resource,
                "category": category,
                "normal_column_status": "promoted" if modeled else "unsupported",
                "artifacts_seen": "|".join(sorted(data["artifacts_seen"])),
                "output_row_count": len(data["output_rows"]),
                "upkeep_row_count": len(data["upkeep_rows"]),
                "net_row_count": len(data["net_rows"]),
                "unsupported_reason": "" if modeled else "resource key detected in amount JSON but absent from modeled resource columns",
            }
        )
    return rows


def write_summary(
    jobs: dict[str, dict[str, Any]],
    buildings: list[dict[str, Any]],
    development_rows: list[dict[str, Any]],
    plans: list[dict[str, Any]],
    role_rows: list[dict[str, Any]],
    tech_rows: list[dict[str, Any]],
    strategic_rows: list[dict[str, Any]],
    resource_coverage_rows: list[dict[str, Any]],
    readiness_rows: list[dict[str, Any]],
    benefit_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
) -> None:
    research_buildings = [row for row in buildings if float(row["total_research"]) > 0]
    best = sorted(research_buildings, key=lambda row: float(row["total_research"]), reverse=True)[:20]
    consumer_goods_development = [
        row for row in development_rows if float(row["net_consumer_goods"]) > 0
    ]
    best_consumer_goods = sorted(
        consumer_goods_development, key=lambda row: float(row["net_consumer_goods"]), reverse=True
    )[:10]
    lines = [
        "# Stellar AI Director Research Capacity",
        "",
        "This is a deterministic active-stack capacity inventory. It resolves winning active-stack job definitions, building job slots, direct building output/upkeep, and building upgrade chains. Job triggered resource blocks are included in the optimistic output columns and should be treated as maximum-potential math, not runtime proof.",
        "",
        f"Job-producing modifiers are normalized from Stellaris 4.x workforce units using {JOB_WORKFORCE_UNITS:g} workforce = 1 full job equivalent. Raw workforce totals are retained in the building CSV.",
        "",
        f"- Jobs indexed: {len(jobs)}",
        f"- Buildings indexed: {len(buildings)}",
        f"- Districts/zones indexed: {len(development_rows)}",
        f"- Buildings with resolved research output: {len(research_buildings)}",
        f"- Districts/zones with net consumer-goods output: {len(consumer_goods_development)}",
        f"- Colony role target rows: {len(role_rows)}",
        f"- Technologies with research-relevant modifiers indexed: {len(tech_rows)}",
        f"- Strategic infrastructure target rows: {len(strategic_rows)}",
        f"- Resource coverage rows: {len(resource_coverage_rows)}",
        f"- Build-plan readiness rows: {len(readiness_rows)}",
        f"- Strategic benefit taxonomy rows: {len(benefit_rows)}",
        f"- Modeling blocker accounting rows: {len(blocker_rows)}",
        f"- Source roots include vanilla at `{STELLARIS_INSTALL_ROOT}` plus enabled launcher mods.",
        "- Plan rows include base and building-modifier-adjusted research/upkeep. Technology rows are inventoried but not auto-applied to colony plans yet.",
        "- Jobs, buildings, development rows, and plan rows preserve base, triggered, conservative, and optimistic resource scenarios where applicable.",
        "- Strategic infrastructure rows classify habitat growth centers, capital/empire-unique candidates, starbase migration support, and refactor constraints such as `can_demolish = no`.",
        "- Resource coverage rows classify every resource key detected in amount JSON as promoted or unsupported.",
        "- Build-plan readiness rows classify building gate phases and same-role fallback candidates before unlocks.",
        "- Strategic benefit taxonomy rows classify detected non-resource benefits and record no-evidence classes for active-stack gaps.",
        "- Modeling blocker accounting rows normalize unknown jobs, unresolved variables, quality flags, unsupported resources, and unvalued benefit formulas.",
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
    lines.extend(
        [
            "",
            "## Top Consumer-Goods Districts/Zones",
            "",
            "| rank | type | object | net consumer goods/month | jobs | mod |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for index, row in enumerate(best_consumer_goods, 1):
        lines.append(
            f"| {index} | {row['object_type']} | `{row['object_id']}` | {row['net_consumer_goods']} | {row['job_slots_total']} | {row['winning_mod_name']} |"
        )
    best_role_rows = [
        row
        for row in role_rows
        if (
            row["source_scope"].startswith("build_plan_candidate_terminal_buildings_")
            and row["source_scope"].endswith("_in_12_slots")
        )
        or (row["source_scope"] == "development_top_1" and row["colony_class"] == "all_colony_classes")
    ]
    lines.extend(
        [
            "",
            "## Colony Role Targets",
            "",
            "| role | source | class | net role output | selected |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    for row in sorted(best_role_rows, key=lambda item: (item["role"], item["source_scope"], item["colony_class"])):
        lines.append(
            f"| {row['role']} | {row['source_scope']} | {row['colony_class']} | {row['net_role_output']} | `{row['selected_objects']}` |"
        )
    lines.extend(
        [
            "",
            "## Strategic Infrastructure Targets",
            "",
            "| role | object | score | tags | source |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for role in (
        "starbase_migration_support",
        "habitat_growth_center",
        "habitat_support_center",
        "capital_world",
        "starbase_fleet_scaling",
        "starbase_resource_support",
    ):
        role_rows_for_summary = [row for row in strategic_rows if row["role"] == role]
        for row in sorted(role_rows_for_summary, key=lambda item: (-float(item["priority_score"]), str(item["object_id"])))[:8]:
            lines.append(
                f"| {row['role']} | `{row['object_type']}:{row['object_id']}` | {row['priority_score']} | {row['strategic_tags']} | {row['winning_mod_name']} |"
            )
    lines.extend(["", "## Colony Scenarios", "", "| scenario | base research/month | adjusted research/month | adjusted CG upkeep | colonies for 3000 |", "| --- | ---: | ---: | ---: | ---: |"])
    for row in plans:
        lines.append(
            f"| {row['scenario']} | {row['base_research_per_full_colony']} | {row['adjusted_research_per_full_colony']} | {row['adjusted_upkeep_consumer_goods']} | {row['colonies_for_3000_research']} |"
        )
    write_text_file(OUT_MD, "\n".join(lines) + "\n")


def main() -> None:
    playset = build_active_playset_snapshot()
    jobs = collect_winning_jobs(playset)
    job_rows = [
        {key: value for key, value in row.items() if key != "value"}
        for row in sorted(jobs.values(), key=lambda item: item["job_id"])
    ]
    buildings = collect_buildings(playset, jobs)
    development_rows = collect_development_rows(playset, jobs)
    plans = plan_rows(buildings)
    tech_rows = collect_technology_modifier_rows(playset)
    strategic_rows = strategic_infrastructure_rows(playset)
    role_rows = role_target_rows(buildings, development_rows, strategic_rows)
    resource_coverage_rows = modeling_resource_coverage_rows(job_rows, buildings, development_rows, strategic_rows)
    readiness_rows = build_plan_readiness_rows(buildings)
    benefit_rows = strategic_benefit_taxonomy_rows(strategic_rows)
    blocker_rows = modeling_blocker_accounting_rows(buildings, development_rows, strategic_rows, resource_coverage_rows, benefit_rows)
    write_csv(OUT_JOBS, job_rows)
    write_csv(OUT_BUILDINGS, buildings)
    write_csv(OUT_DEVELOPMENT, development_rows)
    write_csv(OUT_PLAN, plans)
    write_csv(OUT_ROLES, role_rows)
    write_csv(OUT_TECH, tech_rows)
    write_csv(OUT_INFRA, strategic_rows)
    write_csv(OUT_RESOURCE_COVERAGE, resource_coverage_rows)
    write_csv(OUT_READINESS, readiness_rows)
    write_csv(OUT_BENEFITS, benefit_rows)
    write_csv(OUT_BLOCKERS, blocker_rows)
    write_summary(
        jobs,
        buildings,
        development_rows,
        plans,
        role_rows,
        tech_rows,
        strategic_rows,
        resource_coverage_rows,
        readiness_rows,
        benefit_rows,
        blocker_rows,
    )
    print(
        f"generated {len(job_rows)} jobs, {len(buildings)} buildings, "
        f"{len(development_rows)} districts/zones, {len(plans)} plan rows, "
        f"{len(role_rows)} role rows, {len(tech_rows)} tech modifier rows, "
        f"{len(strategic_rows)} strategic infrastructure rows, "
        f"{len(resource_coverage_rows)} resource coverage rows, "
        f"{len(readiness_rows)} readiness rows, "
        f"{len(benefit_rows)} benefit taxonomy rows, "
        f"{len(blocker_rows)} blocker rows"
    )


if __name__ == "__main__":
    main()
