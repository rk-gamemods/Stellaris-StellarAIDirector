#!/usr/bin/env python3
"""Extract bounded, read-only expansion evidence from Stellaris save series.

The extractor reports serialized observations.  It does not claim to reproduce
engine planning state, prove trigger truth, or infer continuous state between
the supplied snapshots.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable

from extract_stellar_ai_save_model_evidence import (
    _balanced_block_at,
    _block_body,
    _current_owned_fleet_ids,
    _direct_anonymous_blocks,
    _numeric_list,
    _top_level_assignment_block,
)
from stellar_ai_director_lib import sum_resource_assignments
from stellar_ai_observer_loop import (
    country_type,
    localized_key_text,
    top_level_scalar_assignment,
)


SCHEMA = "stellar-ai-expansion-evidence/v1"
PARSER_VERSION = "1.0.0"
MAX_SAVES = 32
MAX_SAVE_BYTES = 512 * 1024 * 1024
MAX_GAMESTATE_BYTES = 768 * 1024 * 1024
MAX_META_BYTES = 2 * 1024 * 1024
MAX_NUMBERED_ROWS = 250_000
MAX_SYSTEM_ROWS_PER_SAVE = 5_000
MAX_RELATION_ROWS_PER_SAVE = 10_000
CONSTRUCTOR_SHIP_CLASS = "shipclass_constructor"
NULL_REFERENCE = "4294967295"
STRATEGY_TYPES_OF_INTEREST = frozenset({"1", "19"})
STRATEGY_SEMANTIC_NOTES = {
    "1": "empirically calibrated type-1 row; not an official engine enum declaration",
    "19": "empirically calibrated type-19 row; not proof of has_ai_expansion_plan",
}
# Deliberately empty until a raw order key is independently calibrated.  Never
# infer an outpost order from a display name, target, or resource amount.
OUTPOST_ORDER_KIND_REGISTRY: dict[str, str] = {}
ORDER_SCALAR_KEYS = (
    "target",
    "planet",
    "system",
    "starbase",
    "fleet",
    "type",
    "can_reach",
    "in_progress",
    "progress",
    "order_id",
)

CSV_FIELDS = {
    "snapshots": (
        "snapshot_id",
        "date",
        "file_name",
        "sha256",
        "byte_size",
        "save_name",
        "version",
        "version_control_revision",
        "country_id",
        "country_name",
        "country_type",
        "stockpile_json",
        "income_json",
        "expenses_json",
        "balance_json",
        "strategy_interest_row_count",
        "constructor_count",
        "constructor_busy_current_order_count",
        "relation_count",
    ),
    "candidates": (
        "snapshot_id",
        "date",
        "country_id",
        "serialized_index",
        "raw_type",
        "raw_id",
        "raw_target",
        "raw_value",
        "mapped_planet_id",
        "mapped_system_id",
        "id_join_status",
        "semantic_boundary",
    ),
    "constructors": (
        "snapshot_id",
        "date",
        "country_id",
        "fleet_id",
        "fleet_name",
        "ship_count",
        "current_system_id",
        "current_system_source",
        "busy_from_current_order",
        "fleet_order_id_not_busy_signal",
        "current_order_present",
        "raw_order_kind_keys_json",
        "order_evidence_json",
    ),
    "systems": (
        "snapshot_id",
        "date",
        "system_id",
        "system_name",
        "interest_reasons_json",
        "planet_ids_json",
        "hyperlane_target_system_ids_json",
        "starbase_ids_json",
        "non_null_starbase_ids_json",
        "discovery_country_ids_json",
    ),
    "relations": (
        "snapshot_id",
        "date",
        "country_id",
        "relation_index",
        "other_country_id",
        "raw_fields_json",
    ),
    "episodes": (
        "episode_id",
        "country_id",
        "raw_type",
        "raw_id",
        "raw_target",
        "mapped_planet_id",
        "mapped_system_id",
        "episode_number",
        "first_observed_date",
        "last_observed_date",
        "observation_count",
        "observed_snapshot_ids_json",
        "observed_raw_values_json",
        "missing_supplied_snapshot_count_before",
        "present_in_final_snapshot",
        "continuous_engine_presence_proven",
        "evidence_classification",
        "semantic_boundary",
    ),
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _date_key(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value)
    if not match:
        raise ValueError(f"unsupported or missing Stellaris date: {value!r}")
    return tuple(int(part) for part in match.groups())


def _atom_key(value: str | None) -> tuple[int, Decimal | str]:
    if value is None:
        return (2, "")
    try:
        return (0, Decimal(value))
    except InvalidOperation:
        return (1, value)


def _json_cell(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _read_save_entries(save_path: Path) -> tuple[str, str, dict[str, Any]]:
    resolved = save_path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"save does not exist: {resolved}")
    before = resolved.stat()
    if before.st_size > MAX_SAVE_BYTES:
        raise ValueError(
            f"save exceeds the {MAX_SAVE_BYTES}-byte compressed input cap: {resolved}"
        )
    before_hash = _sha256(resolved)
    with zipfile.ZipFile(resolved) as archive:
        infos = {info.filename: info for info in archive.infolist()}
        for entry, cap in (
            ("gamestate", MAX_GAMESTATE_BYTES),
            ("meta", MAX_META_BYTES),
        ):
            info = infos.get(entry)
            if info is None:
                raise ValueError(f"Stellaris save is missing {entry} entry: {resolved}")
            if info.flag_bits & 0x1:
                raise ValueError(f"encrypted save entry is unsupported: {entry}")
            if info.file_size > cap:
                raise ValueError(
                    f"{entry} exceeds the {cap}-byte uncompressed cap: {resolved}"
                )
        gamestate_bytes = archive.read("gamestate")
        meta_bytes = archive.read("meta")
    after = resolved.stat()
    after_hash = _sha256(resolved)
    if (
        before.st_size != after.st_size
        or before.st_mtime_ns != after.st_mtime_ns
        or before_hash != after_hash
    ):
        raise ValueError(f"save changed while it was being read: {resolved}")
    try:
        gamestate = gamestate_bytes.decode("utf-8-sig", "strict")
        meta = meta_bytes.decode("utf-8-sig", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError(f"save entries are not strict UTF-8: {resolved}") from exc
    return (
        gamestate,
        meta,
        {
            "file_name": resolved.name,
            "byte_size": before.st_size,
            "sha256": before_hash,
        },
    )


def _direct_numbered_blocks(block_text: str) -> list[tuple[str, str]]:
    """Return direct numeric child blocks with quote/comment-aware balancing."""

    text = _block_body(block_text)
    pattern = re.compile(r"^\s*(\d+)\s*=\s*")
    rows: list[tuple[str, str]] = []
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
                    rows.append((match.group(1), _balanced_block_at(text, brace_index)))
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
    return rows


def _limited_numbered(block: str, label: str) -> dict[str, str]:
    rows = _direct_numbered_blocks(block)
    if len(rows) > MAX_NUMBERED_ROWS:
        raise ValueError(f"{label} exceeds the {MAX_NUMBERED_ROWS}-row parser cap")
    if len({row_id for row_id, _ in rows}) != len(rows):
        raise ValueError(f"{label} contains duplicate numeric IDs")
    return dict(rows)


def _direct_named_blocks(block_text: str, key: str) -> list[str]:
    """Return repeated direct child assignment blocks with the requested key."""

    text = _block_body(block_text)
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*=\s*")
    result: list[str] = []
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
                    result.append(_balanced_block_at(text, brace_index))
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
    return result


def _direct_scalar_values(block_text: str, key: str) -> list[str]:
    text = _block_body(block_text)
    pattern = re.compile(
        rf'^\s*{re.escape(key)}\s*=\s*(?:"((?:\\.|[^"])*)"|([^\s#{{}}]+))'
    )
    values: list[str] = []
    depth = 0
    in_quote = False
    escaped = False
    for line in text.splitlines():
        if depth == 0 and not in_quote:
            match = pattern.match(line)
            if match:
                values.append(
                    match.group(1) if match.group(1) is not None else match.group(2)
                )
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
    return values


def _direct_assignment_keys(block_text: str) -> list[str]:
    text = _block_body(block_text)
    pattern = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_.:-]*)\s*=")
    keys: list[str] = []
    depth = 0
    in_quote = False
    escaped = False
    for line in text.splitlines():
        if depth == 0 and not in_quote:
            match = pattern.match(line)
            if match:
                keys.append(match.group(1))
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
    return keys


def _resource_surface(country_block: str, path: tuple[str, ...]) -> dict[str, Any]:
    block = country_block
    for key in path:
        block = _top_level_assignment_block(block, key)
        if not block:
            break
    return {
        "source_path": "country." + ".".join(path),
        "serialized_block_present": bool(block),
        "values": sum_resource_assignments(block) if block else {},
    }


def _planet_system_id(planet_block: str) -> str | None:
    coordinate = _top_level_assignment_block(planet_block, "coordinate")
    origin = top_level_scalar_assignment(coordinate, "origin") or None
    return None if origin == NULL_REFERENCE else origin


def _strategy_rows(
    country_id: str, country_block: str, planets: dict[str, str]
) -> list[dict[str, Any]]:
    ai_block = _top_level_assignment_block(country_block, "ai")
    strategy_blocks: list[str] = []
    for block in _direct_named_blocks(ai_block, "strategy"):
        if top_level_scalar_assignment(block, "type"):
            strategy_blocks.append(block)
        else:
            strategy_blocks.extend(_direct_anonymous_blocks(block))
    result: list[dict[str, Any]] = []
    for index, raw_block in enumerate(strategy_blocks):
        raw_type = top_level_scalar_assignment(raw_block, "type") or None
        if raw_type not in STRATEGY_TYPES_OF_INTEREST:
            continue
        raw_id = top_level_scalar_assignment(raw_block, "id") or None
        raw_target = top_level_scalar_assignment(raw_block, "target") or None
        raw_value = top_level_scalar_assignment(raw_block, "value") or None
        if None in {raw_id, raw_target, raw_value}:
            raise ValueError(
                f"country {country_id} type-{raw_type} strategy row is missing id, target, or value"
            )
        planet = planets.get(raw_id)
        mapped_system = _planet_system_id(planet) if planet else None
        result.append(
            {
                "country_id": country_id,
                "serialized_index": index,
                "raw_type": raw_type,
                "raw_id": raw_id,
                "raw_target": raw_target,
                "raw_value": raw_value,
                "mapped_planet_id": raw_id if planet else None,
                "mapped_system_id": mapped_system,
                "id_join_status": (
                    "raw_id_matched_planet_table; namespace meaning remains empirical"
                    if planet
                    else "no raw_id match in planet table"
                ),
                "semantic_boundary": STRATEGY_SEMANTIC_NOTES[raw_type],
            }
        )
    return sorted(
        result,
        key=lambda row: (
            _atom_key(row["raw_type"]),
            _atom_key(row["raw_id"]),
            _atom_key(row["raw_target"]),
            _atom_key(row["raw_value"]),
            row["serialized_index"],
        ),
    )


def _fleet_current_system(fleet_block: str) -> tuple[str | None, str | None]:
    for owner, path in (
        ("movement_manager.coordinate.origin", ("movement_manager", "coordinate")),
        ("combat.coordinate.origin", ("combat", "coordinate")),
    ):
        block = fleet_block
        for key in path:
            block = _top_level_assignment_block(block, key)
            if not block:
                break
        origin = top_level_scalar_assignment(block, "origin") or None
        if origin and origin != NULL_REFERENCE:
            return origin, owner
    return None, None


def _order_evidence(current_order: str) -> tuple[list[str], list[dict[str, Any]]]:
    keys = _direct_assignment_keys(current_order)
    rows: list[dict[str, Any]] = []
    for key in keys:
        order_block = _top_level_assignment_block(current_order, key)
        raw_scalars = {
            scalar: value
            for scalar in ORDER_SCALAR_KEYS
            if (value := top_level_scalar_assignment(order_block, scalar))
        }
        coordinate = _top_level_assignment_block(order_block, "coordinate")
        coordinate_origin = top_level_scalar_assignment(coordinate, "origin") or None
        resources = _top_level_assignment_block(order_block, "resources")
        rows.append(
            {
                "raw_order_kind_key": key,
                "outpost_order_classification": OUTPOST_ORDER_KIND_REGISTRY.get(key),
                "outpost_order_classification_basis": (
                    "evidence-backed raw-order-key registry"
                    if key in OUTPOST_ORDER_KIND_REGISTRY
                    else "unclassified; no evidence-backed raw-order-key registry entry"
                ),
                "raw_scalars": raw_scalars,
                "raw_coordinate_origin": coordinate_origin,
                "serialized_order_resources": (
                    sum_resource_assignments(resources) if resources else {}
                ),
                "resource_semantic_boundary": (
                    "serialized order resource amounts; not inferred total or remaining cost"
                ),
            }
        )
    return keys, rows


def _constructor_rows(
    country_id: str, country_block: str, fleets: dict[str, str]
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for fleet_id in sorted(_current_owned_fleet_ids(country_block), key=_atom_key):
        fleet = fleets.get(fleet_id)
        if fleet is None:
            raise ValueError(
                f"country {country_id} references missing owned fleet {fleet_id}"
            )
        if top_level_scalar_assignment(fleet, "ship_class") != CONSTRUCTOR_SHIP_CLASS:
            continue
        current_order = _top_level_assignment_block(fleet, "current_order")
        order_keys, order_rows = (
            _order_evidence(current_order) if current_order else ([], [])
        )
        current_system, current_system_source = _fleet_current_system(fleet)
        result.append(
            {
                "country_id": country_id,
                "fleet_id": fleet_id,
                "fleet_name": localized_key_text(fleet, "name") or f"fleet_{fleet_id}",
                "ship_count": len(
                    _numeric_list(_top_level_assignment_block(fleet, "ships"))
                ),
                "current_system_id": current_system,
                "current_system_source": current_system_source,
                "busy_from_current_order": bool(current_order),
                "fleet_order_id_not_busy_signal": (
                    top_level_scalar_assignment(fleet, "order_id") or None
                ),
                "current_order_present": bool(current_order),
                "raw_order_kind_keys": order_keys,
                "order_evidence": order_rows,
            }
        )
    return result


def _relation_rows(country_id: str, country_block: str) -> list[dict[str, Any]]:
    manager = _top_level_assignment_block(country_block, "relations_manager")
    blocks = _direct_named_blocks(manager, "relation")
    if len(blocks) > MAX_RELATION_ROWS_PER_SAVE:
        raise ValueError(
            f"country {country_id} exceeds the {MAX_RELATION_ROWS_PER_SAVE}-relation cap"
        )
    fields = (
        "owner",
        "country",
        "contact",
        "threat",
        "trust",
        "border_range",
        "communications",
        "closed_borders",
        "relation_current",
        "relation_last_month",
    )
    result: list[dict[str, Any]] = []
    for index, block in enumerate(blocks):
        raw = {
            field: value
            for field in fields
            if (value := top_level_scalar_assignment(block, field))
        }
        result.append(
            {
                "country_id": country_id,
                "relation_index": index,
                "other_country_id": raw.get("country"),
                "raw_fields": raw,
            }
        )
    return sorted(
        result,
        key=lambda row: (_atom_key(row["other_country_id"]), row["relation_index"]),
    )


def _system_rows(
    systems: dict[str, str],
    strategy_rows: list[dict[str, Any]],
    constructors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    reasons: dict[str, set[str]] = defaultdict(set)
    for row in strategy_rows:
        if row["mapped_system_id"]:
            reasons[row["mapped_system_id"]].add(f"strategy_type_{row['raw_type']}")
    for row in constructors:
        if row["current_system_id"]:
            reasons[row["current_system_id"]].add("constructor_current_system")
        for order in row["order_evidence"]:
            origin = order["raw_coordinate_origin"]
            if origin and origin != NULL_REFERENCE:
                reasons[origin].add("constructor_order_coordinate_origin")
    if len(reasons) > MAX_SYSTEM_ROWS_PER_SAVE:
        raise ValueError(
            f"system evidence exceeds the {MAX_SYSTEM_ROWS_PER_SAVE}-row cap"
        )
    result: list[dict[str, Any]] = []
    for system_id in sorted(reasons, key=_atom_key):
        block = systems.get(system_id)
        if block is None:
            result.append(
                {
                    "system_id": system_id,
                    "system_name": None,
                    "interest_reasons": sorted(reasons[system_id]),
                    "planet_ids": [],
                    "hyperlane_target_system_ids": [],
                    "starbase_ids": [],
                    "non_null_starbase_ids": [],
                    "discovery_country_ids": [],
                    "warning": "referenced system is missing from galactic_object table",
                }
            )
            continue
        hyperlanes = _direct_anonymous_blocks(
            _top_level_assignment_block(block, "hyperlane")
        )
        hyperlane_targets = [
            target
            for lane in hyperlanes
            if (target := top_level_scalar_assignment(lane, "to"))
        ]
        starbases = _numeric_list(_top_level_assignment_block(block, "starbases"))
        result.append(
            {
                "system_id": system_id,
                "system_name": localized_key_text(block, "name")
                or f"system_{system_id}",
                "interest_reasons": sorted(reasons[system_id]),
                "planet_ids": sorted(
                    _direct_scalar_values(block, "planet"), key=_atom_key
                ),
                "hyperlane_target_system_ids": sorted(hyperlane_targets, key=_atom_key),
                "starbase_ids": sorted(starbases, key=_atom_key),
                "non_null_starbase_ids": sorted(
                    (starbase for starbase in starbases if starbase != NULL_REFERENCE),
                    key=_atom_key,
                ),
                "discovery_country_ids": sorted(
                    _numeric_list(_top_level_assignment_block(block, "discovery")),
                    key=_atom_key,
                ),
                "warning": None,
            }
        )
    return result


def _build_snapshot(save_path: Path, country_id: str) -> dict[str, Any]:
    gamestate, meta, input_row = _read_save_entries(save_path)
    meta_date = top_level_scalar_assignment(meta, "date") or None
    gamestate_date = top_level_scalar_assignment(gamestate, "date") or None
    if meta_date and gamestate_date and meta_date != gamestate_date:
        raise ValueError(
            f"meta date {meta_date} differs from gamestate date {gamestate_date}: {save_path}"
        )
    date = meta_date or gamestate_date
    if date is None:
        raise ValueError(f"save date is unavailable: {save_path}")
    _date_key(date)

    countries = _limited_numbered(
        _top_level_assignment_block(gamestate, "country"), "country table"
    )
    fleets = _limited_numbered(
        _top_level_assignment_block(gamestate, "fleet"), "fleet table"
    )
    planets_root = _top_level_assignment_block(gamestate, "planets")
    planets = _limited_numbered(
        _top_level_assignment_block(planets_root, "planet") or planets_root,
        "planet table",
    )
    systems = _limited_numbered(
        _top_level_assignment_block(gamestate, "galactic_object"),
        "galactic_object table",
    )
    country = countries.get(country_id)
    if country is None:
        raise ValueError(f"country {country_id} is absent from save {save_path.name}")

    resources = {
        "stockpile": _resource_surface(
            country, ("modules", "standard_economy_module", "resources")
        ),
        "income": _resource_surface(country, ("budget", "current_month", "income")),
        "expenses": _resource_surface(country, ("budget", "current_month", "expenses")),
        "balance": _resource_surface(country, ("budget", "current_month", "balance")),
    }
    strategy_rows = _strategy_rows(country_id, country, planets)
    constructors = _constructor_rows(country_id, country, fleets)
    relations = _relation_rows(country_id, country)
    system_rows = _system_rows(systems, strategy_rows, constructors)

    save_name = top_level_scalar_assignment(meta, "name") or None
    version = (
        top_level_scalar_assignment(meta, "version")
        or top_level_scalar_assignment(gamestate, "version")
        or None
    )
    revision = (
        top_level_scalar_assignment(meta, "version_control_revision")
        or top_level_scalar_assignment(gamestate, "version_control_revision")
        or None
    )
    snapshot_id = f"{date}-{input_row['sha256'][:12]}"
    return {
        "snapshot_id": snapshot_id,
        "input": input_row,
        "save": {
            "name": save_name,
            "version": version,
            "version_control_revision": revision,
            "date": date,
        },
        "country": {
            "country_id": country_id,
            "country_name": localized_key_text(country, "name")
            or f"country_{country_id}",
            "country_type": country_type(country) or None,
        },
        "resources": resources,
        "strategy_interest_rows": strategy_rows,
        "constructors": constructors,
        "systems": system_rows,
        "relations": relations,
    }


def _build_episodes(snapshots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    observations: dict[tuple[str, str, str, str], list[tuple[int, dict[str, Any]]]] = (
        defaultdict(list)
    )
    for snapshot_index, snapshot in enumerate(snapshots):
        for row in snapshot["strategy_interest_rows"]:
            key = (row["country_id"], row["raw_type"], row["raw_id"], row["raw_target"])
            observations[key].append((snapshot_index, row))

    episodes: list[dict[str, Any]] = []
    for key in sorted(
        observations, key=lambda item: tuple(_atom_key(value) for value in item)
    ):
        runs: list[list[tuple[int, dict[str, Any]]]] = []
        for observation in observations[key]:
            if not runs or observation[0] != runs[-1][-1][0] + 1:
                runs.append([])
            runs[-1].append(observation)
        previous_last = -1
        for episode_number, run in enumerate(runs, start=1):
            country_id, raw_type, raw_id, raw_target = key
            first_index = run[0][0]
            last_index = run[-1][0]
            snapshot_ids = [snapshots[index]["snapshot_id"] for index, _ in run]
            dates = [snapshots[index]["save"]["date"] for index, _ in run]
            episodes.append(
                {
                    "episode_id": (
                        f"country-{country_id}-type-{raw_type}-id-{raw_id}-"
                        f"target-{raw_target}-episode-{episode_number:03d}"
                    ),
                    "country_id": country_id,
                    "raw_type": raw_type,
                    "raw_id": raw_id,
                    "raw_target": raw_target,
                    "mapped_planet_id": run[0][1]["mapped_planet_id"],
                    "mapped_system_id": run[0][1]["mapped_system_id"],
                    "episode_number": episode_number,
                    "first_observed_date": dates[0],
                    "last_observed_date": dates[-1],
                    "observation_count": len(run),
                    "observed_snapshot_ids": snapshot_ids,
                    "observed_raw_values": [row["raw_value"] for _, row in run],
                    "missing_supplied_snapshot_count_before": (
                        0 if previous_last < 0 else first_index - previous_last - 1
                    ),
                    "present_in_final_snapshot": last_index == len(snapshots) - 1,
                    "continuous_engine_presence_proven": False,
                    "evidence_classification": "snapshot_observed_persistence",
                    "semantic_boundary": (
                        "episode spans consecutive supplied snapshots only; it is not continuous engine age"
                    ),
                    "supplied_snapshot_index_span": [first_index, last_index],
                }
            )
            previous_last = last_index
    return episodes


def build_series(save_paths: Iterable[Path], country_id: str) -> dict[str, Any]:
    paths = [Path(path) for path in save_paths]
    if not re.fullmatch(r"\d+", country_id):
        raise ValueError("country ID must be a non-negative integer atom")
    if not paths:
        raise ValueError("at least one save is required")
    if len(paths) > MAX_SAVES:
        raise ValueError(f"save series exceeds the fixed {MAX_SAVES}-save cap")
    resolved = [path.resolve() for path in paths]
    if len(set(resolved)) != len(resolved):
        raise ValueError("save series contains duplicate input paths")

    snapshots = [_build_snapshot(path, country_id) for path in paths]
    content_hashes = [row["input"]["sha256"] for row in snapshots]
    if len(set(content_hashes)) != len(content_hashes):
        raise ValueError("save series contains duplicate save content SHA-256")
    snapshots.sort(
        key=lambda row: (
            _date_key(row["save"]["date"]),
            row["input"]["sha256"],
            row["input"]["file_name"],
        )
    )
    dates = [row["save"]["date"] for row in snapshots]
    if len(set(dates)) != len(dates):
        raise ValueError(
            "save series contains duplicate dates; episode order would be ambiguous"
        )
    signatures = {
        (
            row["save"]["name"],
            row["save"]["version"],
            row["save"]["version_control_revision"],
            row["country"]["country_name"],
        )
        for row in snapshots
    }
    if len(signatures) != 1:
        raise ValueError(
            "save series failed campaign comparability: save name, version, revision, or country name differs"
        )
    signature = next(iter(signatures))
    candidate_mappings: dict[tuple[str, str, str, str], set[tuple[Any, Any]]] = (
        defaultdict(set)
    )
    for snapshot in snapshots:
        for row in snapshot["strategy_interest_rows"]:
            key = (
                row["country_id"],
                row["raw_type"],
                row["raw_id"],
                row["raw_target"],
            )
            candidate_mappings[key].add(
                (row["mapped_planet_id"], row["mapped_system_id"])
            )
    unstable_mappings = [
        {
            "country_id": key[0],
            "raw_type": key[1],
            "raw_id": key[2],
            "raw_target": key[3],
            "mappings": sorted(
                mappings, key=lambda value: tuple(_atom_key(item) for item in value)
            ),
        }
        for key, mappings in candidate_mappings.items()
        if len(mappings) > 1
    ]
    if unstable_mappings:
        raise ValueError(
            "save series candidate mapping drift: "
            + json.dumps(unstable_mappings, sort_keys=True)
        )
    return {
        "schema": SCHEMA,
        "parser": {
            "version": PARSER_VERSION,
            "fixed_caps": {
                "save_count": MAX_SAVES,
                "compressed_save_bytes": MAX_SAVE_BYTES,
                "gamestate_uncompressed_bytes": MAX_GAMESTATE_BYTES,
                "meta_uncompressed_bytes": MAX_META_BYTES,
            },
        },
        "methodology": {
            "read_only": True,
            "country_selection": "one explicit numeric country ID; no controller inference",
            "strategy_rows": (
                "raw direct country.ai.strategy rows whose serialized type atom is 1 or 19"
            ),
            "strategy_semantics": (
                "type labels are empirical research calibrations, not official engine enum proof"
            ),
            "constructor_busy": (
                "true only when a direct fleet.current_order block is serialized; fleet.order_id is reported separately"
            ),
            "order_resources": (
                "serialized amounts only; never labeled total cost or remaining cost"
            ),
            "outpost_order_classification": (
                "null unless the raw order kind exists in an evidence-backed registry"
            ),
            "resources": (
                "stockpile, current-month income, expenses, and balance remain separate source-path maps"
            ),
            "episodes": (
                "consecutive supplied-snapshot observations; never inferred continuous engine age"
            ),
            "systems": (
                "only systems referenced by selected strategy rows or constructor location/order evidence"
            ),
        },
        "campaign_comparability": {
            "status": "caller_asserted_series_with_consistency_checks",
            "common_campaign_lineage_proven": False,
            "save_name": signature[0],
            "version": signature[1],
            "version_control_revision": signature[2],
            "country_name": signature[3],
            "checks": [
                "unique supplied dates",
                "matching save name",
                "matching game version",
                "matching version-control revision",
                "matching country name for the explicit country ID",
            ],
        },
        "country_id": country_id,
        "snapshots": snapshots,
        "episodes": _build_episodes(snapshots),
        "warnings": [
            "matching metadata and candidate mappings cannot prove common campaign lineage or playset identity",
            "serialized observations cannot prove native trigger truth or why the engine did not issue an order",
            "system and planet ID joins are mechanical and retain an explicit empirical semantic boundary",
        ],
    }


def render_json(series: dict[str, Any]) -> str:
    return json.dumps(series, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def normalized_rows(series: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    tables: dict[str, list[dict[str, Any]]] = {name: [] for name in CSV_FIELDS}
    for snapshot in series["snapshots"]:
        snapshot_id = snapshot["snapshot_id"]
        date = snapshot["save"]["date"]
        tables["snapshots"].append(
            {
                "snapshot_id": snapshot_id,
                "date": date,
                **snapshot["input"],
                "save_name": snapshot["save"]["name"],
                "version": snapshot["save"]["version"],
                "version_control_revision": snapshot["save"][
                    "version_control_revision"
                ],
                **snapshot["country"],
                "stockpile_json": _json_cell(snapshot["resources"]["stockpile"]),
                "income_json": _json_cell(snapshot["resources"]["income"]),
                "expenses_json": _json_cell(snapshot["resources"]["expenses"]),
                "balance_json": _json_cell(snapshot["resources"]["balance"]),
                "strategy_interest_row_count": len(snapshot["strategy_interest_rows"]),
                "constructor_count": len(snapshot["constructors"]),
                "constructor_busy_current_order_count": sum(
                    row["busy_from_current_order"] for row in snapshot["constructors"]
                ),
                "relation_count": len(snapshot["relations"]),
            }
        )
        for row in snapshot["strategy_interest_rows"]:
            tables["candidates"].append(
                {"snapshot_id": snapshot_id, "date": date, **row}
            )
        for row in snapshot["constructors"]:
            tables["constructors"].append(
                {
                    "snapshot_id": snapshot_id,
                    "date": date,
                    **row,
                    "raw_order_kind_keys_json": _json_cell(row["raw_order_kind_keys"]),
                    "order_evidence_json": _json_cell(row["order_evidence"]),
                }
            )
        for row in snapshot["systems"]:
            tables["systems"].append(
                {
                    "snapshot_id": snapshot_id,
                    "date": date,
                    **row,
                    "interest_reasons_json": _json_cell(row["interest_reasons"]),
                    "planet_ids_json": _json_cell(row["planet_ids"]),
                    "hyperlane_target_system_ids_json": _json_cell(
                        row["hyperlane_target_system_ids"]
                    ),
                    "starbase_ids_json": _json_cell(row["starbase_ids"]),
                    "non_null_starbase_ids_json": _json_cell(
                        row["non_null_starbase_ids"]
                    ),
                    "discovery_country_ids_json": _json_cell(
                        row["discovery_country_ids"]
                    ),
                }
            )
        for row in snapshot["relations"]:
            tables["relations"].append(
                {
                    "snapshot_id": snapshot_id,
                    "date": date,
                    **row,
                    "raw_fields_json": _json_cell(row["raw_fields"]),
                }
            )
    for row in series["episodes"]:
        tables["episodes"].append(
            {
                **row,
                "observed_snapshot_ids_json": _json_cell(row["observed_snapshot_ids"]),
                "observed_raw_values_json": _json_cell(row["observed_raw_values"]),
            }
        )
    return tables


def render_csv_tables(series: dict[str, Any]) -> dict[str, str]:
    rendered: dict[str, str] = {}
    tables = normalized_rows(series)
    for name, fields in CSV_FIELDS.items():
        output = io.StringIO(newline="")
        writer = csv.DictWriter(
            output, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        for row in tables[name]:
            writer.writerow({field: row.get(field) for field in fields})
        rendered[name] = output.getvalue()
    return rendered


def _write_text(path: Path, content: str, inputs: set[Path]) -> None:
    resolved = path.resolve()
    if resolved in inputs:
        raise ValueError("output path must not overwrite an input save")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(content, encoding="utf-8", newline="\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "saves", nargs="+", type=Path, help="read-only Stellaris .sav inputs"
    )
    parser.add_argument(
        "--country-id", required=True, help="explicit serialized country ID"
    )
    parser.add_argument(
        "--json-out", type=Path, help="write deterministic JSON evidence"
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        help="write normalized snapshots/candidates/constructors/systems/relations/episodes CSVs",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        series = build_series(args.saves, args.country_id)
        inputs = {path.resolve() for path in args.saves}
        if args.json_out:
            _write_text(args.json_out, render_json(series), inputs)
        if args.csv_dir:
            csv_dir = args.csv_dir.resolve()
            if csv_dir in inputs:
                raise ValueError("CSV output directory must not be an input save")
            for name, content in render_csv_tables(series).items():
                _write_text(csv_dir / f"{name}.csv", content, inputs)
        if not args.json_out and not args.csv_dir:
            sys.stdout.write(render_json(series))
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
