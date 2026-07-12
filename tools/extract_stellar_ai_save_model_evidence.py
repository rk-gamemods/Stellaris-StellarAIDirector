#!/usr/bin/env python3
"""Extract deterministic, read-only AI model evidence from a Stellaris save."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from stellar_ai_director_lib import (
    iter_numbered_child_blocks,
    load_stellaris_save_gamestate,
    sum_resource_assignments,
)
from stellar_ai_observer_loop import (
    country_type,
    localized_key_text,
    top_level_numeric_assignment,
    top_level_scalar_assignment,
)


PARSER_CONTRACT = "stellar-ai-save-model-evidence/v1"
PARSER_VERSION = "1.0.0"
NEVER_HUMAN_SENTINEL = "0.01.01"
MILITARY_SHIP_CLASS = "shipclass_military"
SYSTEM_STARBASE_SHIP_CLASS = "shipclass_starbase"

CSV_FIELDS = [
    "country_id",
    "empire_name",
    "country_type",
    "control_classification",
    "control_classification_certainty",
    "last_date_was_human",
    "personality",
    "government_type",
    "authority",
    "origin",
    "ethics",
    "civics",
    "military_power",
    "fleet_size_not_power",
    "economy_power",
    "tech_power",
    "naval_capacity_used",
    "naval_capacity_available",
    "naval_capacity_estimate_from_coverage",
    "naval_capacity_source",
    "alloy_stockpile",
    "alloy_net_income",
    "systems",
    "colonies",
    "pops",
    "mobile_military_fleet_count",
    "military_ship_count",
    "fleet_template_count",
    "fleet_template_target_ship_count",
    "fleet_template_current_ship_count",
    "fleet_template_queued_ship_count",
    "fleet_template_reinforcement_demand_ship_count",
    "shipyard_queue_count",
    "shipyard_parallel_capacity",
    "ship_construction_items_queued",
    "shipyard_active_slots",
    "shipyard_active_utilization",
    "warnings",
]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _balanced_block_at(text: str, brace_index: int) -> str:
    if brace_index >= len(text) or text[brace_index] != "{":
        raise ValueError("balanced block extraction requires an opening brace")
    depth = 0
    in_quote = False
    escaped = False
    in_comment = False
    for index in range(brace_index, len(text)):
        char = text[index]
        if in_comment:
            if char in "\r\n":
                in_comment = False
            continue
        if char == "\\" and in_quote and not escaped:
            escaped = True
            continue
        if char == '"' and not escaped:
            in_quote = not in_quote
        elif not in_quote and char == "#":
            in_comment = True
        elif not in_quote and char == "{":
            depth += 1
        elif not in_quote and char == "}":
            depth -= 1
            if depth == 0:
                return text[brace_index : index + 1]
            if depth < 0:
                break
        escaped = False
    raise ValueError("unterminated PDX block")


def _block_body(block_text: str) -> str:
    text = block_text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text[1:-1]
    return text


def _top_level_assignment_block(block_text: str, key: str) -> str:
    """Return a direct child block while ignoring same-named nested blocks."""

    text = _block_body(block_text)
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*=\s*")
    depth = 0
    in_quote = False
    escaped = False
    offset = 0
    for line in text.splitlines(keepends=True):
        if depth == 0 and not in_quote:
            match = pattern.match(line)
            if match:
                brace_index = offset + match.end()
                while brace_index < len(text) and text[brace_index].isspace():
                    brace_index += 1
                if brace_index < len(text) and text[brace_index] == "{":
                    return _balanced_block_at(text, brace_index)
        for char in line:
            if char == "\\" and in_quote and not escaped:
                escaped = True
                continue
            if char == '"' and not escaped:
                in_quote = not in_quote
            elif not in_quote and char == "#":
                break
            elif not in_quote and char == "{":
                depth += 1
            elif not in_quote and char == "}":
                depth -= 1
            escaped = False
        offset += len(line)
    return ""


def _direct_anonymous_blocks(block_text: str) -> list[str]:
    text = _block_body(block_text)
    blocks: list[str] = []
    index = 0
    in_quote = False
    escaped = False
    in_comment = False
    while index < len(text):
        char = text[index]
        if in_comment:
            if char in "\r\n":
                in_comment = False
            index += 1
            continue
        if char == "\\" and in_quote and not escaped:
            escaped = True
            index += 1
            continue
        if char == '"' and not escaped:
            in_quote = not in_quote
            index += 1
            escaped = False
            continue
        if not in_quote and char == "#":
            in_comment = True
            index += 1
            continue
        if not in_quote and char == "{":
            block = _balanced_block_at(text, index)
            blocks.append(block)
            index += len(block)
            continue
        escaped = False
        index += 1
    return blocks


def _numeric_list(block_text: str) -> list[str]:
    return re.findall(r"(?<![A-Za-z0-9_])\d+(?![A-Za-z0-9_])", _block_body(block_text))


def _quoted_atoms(block_text: str) -> list[str]:
    return re.findall(r'"((?:\\.|[^"])*)"', _block_body(block_text))


def _rounded(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value, 5)


def _integer_scalar(block_text: str, key: str) -> int | None:
    value = top_level_numeric_assignment(block_text, key)
    if value is None or not value.is_integer():
        return None
    return int(value)


def _current_owned_fleet_ids(country_block: str) -> list[str]:
    manager = _top_level_assignment_block(country_block, "fleets_manager")
    owned = _top_level_assignment_block(manager, "owned_fleets")
    result: list[str] = []
    for reference in _direct_anonymous_blocks(owned):
        lost_control = top_level_scalar_assignment(reference, "ownership_status") == "lost_control"
        if not lost_control:
            lost_control = bool(
                re.search(r"\bownership_status\s*=\s*lost_control\b", _block_body(reference))
            )
        if lost_control:
            continue
        fleet_id = top_level_scalar_assignment(reference, "fleet")
        if fleet_id:
            result.append(fleet_id)
    return result


def _control_classification(country_block: str) -> tuple[str, str, str]:
    last_human = top_level_scalar_assignment(country_block, "last_date_was_human")
    if last_human and last_human != NEVER_HUMAN_SENTINEL:
        return (
            "player_or_previously_human",
            "proven_human_history",
            f"last_date_was_human={last_human}",
        )
    if last_human == NEVER_HUMAN_SENTINEL:
        return (
            "ai_candidate_no_human_history_recorded",
            "current_controller_uncertain",
            f"last_date_was_human={NEVER_HUMAN_SENTINEL}; no definitive current-controller field was found",
        )
    return (
        "unknown",
        "current_controller_uncertain",
        "last_date_was_human is absent",
    )


def _shipyard_queues(gamestate: str) -> tuple[dict[str, list[dict[str, int | str]]], list[str]]:
    warnings: list[str] = []
    construction = _top_level_assignment_block(gamestate, "construction")
    queue_manager = _top_level_assignment_block(construction, "queue_mgr")
    queues = _top_level_assignment_block(queue_manager, "queues")
    if not queues:
        return {}, ["construction.queue_mgr.queues is unavailable"]

    by_owner: dict[str, list[dict[str, int | str]]] = defaultdict(list)
    for queue_id, block in iter_numbered_child_blocks(queues):
        if top_level_scalar_assignment(block, "type") != "ships":
            continue
        owner = top_level_scalar_assignment(block, "owner")
        capacity = _integer_scalar(block, "simultaneous")
        if not owner or capacity is None:
            warnings.append(f"ship queue {queue_id} has incomplete owner/capacity data")
            continue
        queued_items = len(_numeric_list(_top_level_assignment_block(block, "items")))
        by_owner[owner].append(
            {
                "queue_id": queue_id,
                "parallel_capacity": capacity,
                "queued_items": queued_items,
                "active_slots": min(capacity, queued_items),
            }
        )
    return dict(by_owner), sorted(set(warnings))


def _fleet_template_details(
    country_block: str,
    fleets: dict[str, str],
    templates: dict[str, str],
    warnings: list[str],
) -> list[dict[str, Any]]:
    manager = _top_level_assignment_block(country_block, "fleet_template_manager")
    template_ids = _numeric_list(_top_level_assignment_block(manager, "fleet_template"))
    details: list[dict[str, Any]] = []
    for template_id in sorted(template_ids, key=int):
        block = templates.get(template_id)
        if not block:
            warnings.append(f"fleet template {template_id} is referenced but missing")
            details.append(
                {
                    "template_id": template_id,
                    "linked_fleet_id": None,
                    "target_ship_count": None,
                    "current_ship_count": None,
                    "queued_ship_count": None,
                    "reinforcement_demand_ship_count": None,
                    "fleet_size_points_not_ship_count": None,
                }
            )
            continue

        design = _top_level_assignment_block(block, "fleet_template_design")
        target_ship_count = 0
        for entry in _direct_anonymous_blocks(design):
            implementation = _top_level_assignment_block(entry, "ship_design_implementation")
            if not implementation:
                warnings.append(f"fleet template {template_id} contains an unrecognized design entry")
                continue
            count = _integer_scalar(entry, "count")
            target_ship_count += 1 if count is None else count

        linked_fleet_id = top_level_scalar_assignment(block, "fleet") or None
        linked_fleet = fleets.get(linked_fleet_id or "")
        current_ship_count: int | None = None
        if linked_fleet:
            current_ship_count = len(_numeric_list(_top_level_assignment_block(linked_fleet, "ships")))
        elif linked_fleet_id:
            warnings.append(f"fleet template {template_id} links to missing fleet {linked_fleet_id}")

        queued_ship_count = len(_numeric_list(_top_level_assignment_block(block, "all_queued")))
        reinforcement_demand = None
        if current_ship_count is not None:
            reinforcement_demand = max(target_ship_count - current_ship_count - queued_ship_count, 0)
        details.append(
            {
                "template_id": template_id,
                "linked_fleet_id": linked_fleet_id,
                "target_ship_count": target_ship_count,
                "current_ship_count": current_ship_count,
                "queued_ship_count": queued_ship_count,
                "reinforcement_demand_ship_count": reinforcement_demand,
                "fleet_size_points_not_ship_count": _integer_scalar(block, "fleet_size"),
            }
        )
    return details


def _sum_optional(details: list[dict[str, Any]], key: str) -> int | None:
    values = [detail[key] for detail in details]
    if any(value is None for value in values):
        return None
    return sum(values)


def _empire_row(
    country_id: str,
    country_block: str,
    fleets: dict[str, str],
    templates: dict[str, str],
    queues_by_owner: dict[str, list[dict[str, int | str]]],
) -> dict[str, Any]:
    warnings: list[str] = []
    fleet_ids = _current_owned_fleet_ids(country_block)
    military_fleet_count = 0
    military_ship_count = 0
    systems = 0
    indexed_military_power = 0.0
    for fleet_id in fleet_ids:
        fleet = fleets.get(fleet_id)
        if not fleet:
            warnings.append(f"owned fleet {fleet_id} is missing from the global fleet table")
            continue
        ship_class = top_level_scalar_assignment(fleet, "ship_class")
        ship_count = len(_numeric_list(_top_level_assignment_block(fleet, "ships")))
        if ship_class == MILITARY_SHIP_CLASS:
            military_fleet_count += 1
            military_ship_count += ship_count
            indexed_military_power += top_level_numeric_assignment(fleet, "military_power") or 0.0
        elif ship_class == SYSTEM_STARBASE_SHIP_CLASS:
            systems += 1

    military_power = top_level_numeric_assignment(country_block, "military_power")
    if military_power is not None and abs(military_power - indexed_military_power) > 0.02:
        warnings.append(
            "country military_power does not match the sum of current owned shipclass_military fleets"
        )

    budget = _top_level_assignment_block(country_block, "budget")
    current_month = _top_level_assignment_block(budget, "current_month")
    balance = sum_resource_assignments(_top_level_assignment_block(current_month, "balance"))
    alloy_net_income = balance.get("alloys")
    if alloy_net_income is None:
        warnings.append("current-month net alloy income is unavailable")

    modules = _top_level_assignment_block(country_block, "modules")
    economy_module = _top_level_assignment_block(modules, "standard_economy_module")
    stockpile = sum_resource_assignments(_top_level_assignment_block(economy_module, "resources"))
    alloy_stockpile = stockpile.get("alloys")
    if alloy_stockpile is None:
        warnings.append("alloy stockpile is unavailable")

    government = _top_level_assignment_block(country_block, "government")
    ethos = _top_level_assignment_block(country_block, "ethos")
    civics = _quoted_atoms(_top_level_assignment_block(government, "civics"))
    ethics = re.findall(r'\bethic\s*=\s*"([^"]+)"', ethos)

    colonies_block = _top_level_assignment_block(country_block, "controlled_colonies")
    colonies = len(_numeric_list(colonies_block)) if colonies_block else None
    if colonies is None:
        warnings.append("controlled colony count is unavailable")

    naval_used = top_level_numeric_assignment(country_block, "used_naval_capacity")
    naval_available = top_level_numeric_assignment(country_block, "naval_capacity")
    navy_coverage = top_level_numeric_assignment(country_block, "navy_coverage")
    naval_estimate = None
    naval_source = "unavailable"
    if naval_available is not None:
        naval_source = "direct_naval_capacity"
    elif naval_used is not None and navy_coverage is not None and navy_coverage > 0:
        naval_estimate = naval_used / navy_coverage
        naval_source = "derived_used_naval_capacity_divided_by_navy_coverage"

    classification, certainty, evidence = _control_classification(country_block)
    template_details = _fleet_template_details(country_block, fleets, templates, warnings)
    ship_queues = sorted(queues_by_owner.get(country_id, []), key=lambda row: int(row["queue_id"]))
    shipyard_capacity = sum(int(queue["parallel_capacity"]) for queue in ship_queues)
    ship_items = sum(int(queue["queued_items"]) for queue in ship_queues)
    active_slots = sum(int(queue["active_slots"]) for queue in ship_queues)

    row = {
        "country_id": country_id,
        "empire_name": localized_key_text(country_block, "name") or f"country_{country_id}",
        "country_type": country_type(country_block),
        "control_classification": classification,
        "control_classification_certainty": certainty,
        "control_classification_evidence": evidence,
        "last_date_was_human": top_level_scalar_assignment(country_block, "last_date_was_human") or None,
        "personality": top_level_scalar_assignment(country_block, "personality") or None,
        "government_type": top_level_scalar_assignment(government, "type") or None,
        "authority": top_level_scalar_assignment(government, "authority") or None,
        "origin": top_level_scalar_assignment(government, "origin") or None,
        "ethics": sorted(ethics),
        "civics": sorted(civics),
        "military_power": _rounded(military_power),
        "fleet_size_not_power": _rounded(top_level_numeric_assignment(country_block, "fleet_size")),
        "economy_power": _rounded(top_level_numeric_assignment(country_block, "economy_power")),
        "tech_power": _rounded(top_level_numeric_assignment(country_block, "tech_power")),
        "naval_capacity_used": _rounded(naval_used),
        "naval_capacity_available": _rounded(naval_available),
        "naval_capacity_estimate_from_coverage": _rounded(naval_estimate),
        "naval_capacity_source": naval_source,
        "navy_coverage": _rounded(navy_coverage),
        "alloy_stockpile": _rounded(alloy_stockpile),
        "alloy_net_income": _rounded(alloy_net_income),
        "systems": systems,
        "systems_count_method": "current owned shipclass_starbase fleets",
        "colonies": colonies,
        "pops": _rounded(top_level_numeric_assignment(country_block, "num_sapient_pops")),
        "mobile_military_fleet_count": military_fleet_count,
        "military_ship_count": military_ship_count,
        "fleet_template_count": len(template_details),
        "fleet_template_target_ship_count": _sum_optional(template_details, "target_ship_count"),
        "fleet_template_current_ship_count": _sum_optional(template_details, "current_ship_count"),
        "fleet_template_queued_ship_count": _sum_optional(template_details, "queued_ship_count"),
        "fleet_template_reinforcement_demand_ship_count": _sum_optional(
            template_details, "reinforcement_demand_ship_count"
        ),
        "fleet_templates": template_details,
        "shipyard_queue_count": len(ship_queues),
        "shipyard_parallel_capacity": shipyard_capacity,
        "ship_construction_items_queued": ship_items,
        "shipyard_active_slots": active_slots,
        "shipyard_active_utilization": _rounded(active_slots / shipyard_capacity)
        if shipyard_capacity
        else None,
        "shipyard_queues": ship_queues,
        "warnings": sorted(set(warnings)),
    }
    return row


def build_snapshot(save_path: Path) -> dict[str, Any]:
    save_path = save_path.resolve()
    if not save_path.is_file():
        raise FileNotFoundError(f"Save does not exist: {save_path}")

    input_hash = _sha256(save_path)
    gamestate = load_stellaris_save_gamestate(save_path)
    with zipfile.ZipFile(save_path) as archive:
        if "meta" not in archive.namelist():
            raise ValueError(f"Stellaris save is missing meta entry: {save_path}")
        meta = archive.read("meta").decode("utf-8", "replace")

    countries_block = _top_level_assignment_block(gamestate, "country")
    fleets_block = _top_level_assignment_block(gamestate, "fleet")
    templates_block = _top_level_assignment_block(gamestate, "fleet_template")
    if not countries_block:
        raise ValueError("Stellaris gamestate has no top-level country block")

    countries = dict(iter_numbered_child_blocks(countries_block))
    fleets = dict(iter_numbered_child_blocks(fleets_block))
    templates = dict(iter_numbered_child_blocks(templates_block))
    queues_by_owner, global_warnings = _shipyard_queues(gamestate)

    type_counts: Counter[str] = Counter()
    empires: list[dict[str, Any]] = []
    for country_id, block in countries.items():
        current_type = country_type(block) or "missing"
        type_counts[current_type] += 1
        if current_type != "default":
            continue
        empires.append(_empire_row(country_id, block, fleets, templates, queues_by_owner))
    empires.sort(key=lambda row: int(row["country_id"]))

    meta_date = top_level_scalar_assignment(meta, "date")
    gamestate_date = top_level_scalar_assignment(gamestate, "date")
    if meta_date and gamestate_date and meta_date != gamestate_date:
        global_warnings.append(f"meta date {meta_date} differs from gamestate date {gamestate_date}")
    if any(
        empire["control_classification_certainty"] == "current_controller_uncertain"
        for empire in empires
    ):
        global_warnings.append(
            "countries without recorded human history are AI candidates, not proven current AI controllers"
        )

    snapshot = {
        "schema": PARSER_CONTRACT,
        "parser": {
            "version": PARSER_VERSION,
            "country_scalar_parser": "stellar_ai_observer_loop.top_level_scalar_assignment",
            "country_type_parser": "stellar_ai_observer_loop.country_type",
            "military_power_source": "country.military_power",
            "fleet_size_contract": "reported separately and never used as military power",
        },
        "input": {
            "file_name": save_path.name,
            "byte_size": save_path.stat().st_size,
            "sha256": input_hash,
        },
        "save": {
            "name": top_level_scalar_assignment(meta, "name") or None,
            "version": top_level_scalar_assignment(meta, "version")
            or top_level_scalar_assignment(gamestate, "version")
            or None,
            "version_control_revision": top_level_scalar_assignment(meta, "version_control_revision")
            or top_level_scalar_assignment(gamestate, "version_control_revision")
            or None,
            "date": meta_date or gamestate_date or None,
            "gamestate_date": gamestate_date or None,
        },
        "methodology": {
            "included_country_contract": "top-level country.type=default; zero-power and collapsed empires remain included",
            "control_classification_contract": (
                "non-sentinel last_date_was_human proves human history; the sentinel does not prove current AI control"
            ),
            "systems_contract": "count current owned fleets whose top-level ship_class is shipclass_starbase",
            "shipyard_contract": (
                "capacity is construction queue simultaneous for type=ships; active slots are min(items, simultaneous)"
            ),
            "reinforcement_contract": (
                "target template design ships minus linked current fleet ships minus all_queued entries, floored at zero"
            ),
        },
        "summary": {
            "country_count": len(countries),
            "country_type_counts": dict(sorted(type_counts.items())),
            "normal_default_empire_count": len(empires),
            "player_or_previously_human_count": sum(
                empire["control_classification"] == "player_or_previously_human" for empire in empires
            ),
            "ai_candidate_no_human_history_recorded_count": sum(
                empire["control_classification"] == "ai_candidate_no_human_history_recorded"
                for empire in empires
            ),
        },
        "empires": empires,
        "warnings": sorted(set(global_warnings)),
    }
    return snapshot


def render_json(snapshot: dict[str, Any]) -> str:
    return json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def render_csv(snapshot: dict[str, Any]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    for empire in snapshot["empires"]:
        row = {field: empire.get(field) for field in CSV_FIELDS}
        row["ethics"] = "|".join(empire["ethics"])
        row["civics"] = "|".join(empire["civics"])
        row["warnings"] = "|".join(empire["warnings"])
        writer.writerow({key: "" if value is None else value for key, value in row.items()})
    return output.getvalue()


def _write_output(path: Path, content: str, input_path: Path) -> None:
    resolved = path.resolve()
    if resolved == input_path.resolve():
        raise ValueError("Output path must not overwrite the input save")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(content, encoding="utf-8", newline="\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save", type=Path, help="Read-only Stellaris .sav input")
    parser.add_argument("--json-out", type=Path, help="Write stable JSON evidence")
    parser.add_argument("--csv-out", type=Path, help="Write stable empire-level CSV evidence")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    snapshot = build_snapshot(args.save)
    json_text = render_json(snapshot)
    if args.json_out:
        _write_output(args.json_out, json_text, args.save)
    if args.csv_out:
        _write_output(args.csv_out, render_csv(snapshot), args.save)
    if not args.json_out and not args.csv_out:
        sys.stdout.write(json_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
