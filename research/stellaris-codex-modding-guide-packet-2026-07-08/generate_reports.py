#!/usr/bin/env python3
"""Generate the 2026-07-08 Stellaris packet supplement evidence tables."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


REPO = Path(r"C:\Users\Admin\Documents\GIT\GameMods\StellarisMods")
OUT = REPO / "research" / "stellaris-codex-modding-guide-packet-2026-07-08"
TABLES = OUT / "tables"
PACKET = OUT / "packet" / "stellaris_coding_agent_packet"
FOLLOWUP = OUT / "webchatgpt-followup-2026-07-08"
STELLARIS = Path(r"C:\Steam\steamapps\common\Stellaris")
USER = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris")

sys.path.insert(0, str(REPO / "tools"))

from stellar_ai_director_lib import (  # type: ignore  # noqa: E402
    PDXAtom,
    PDXBlock,
    PDXParseError,
    block_assignments,
    iter_assignments,
    parse_file,
    read_text,
)


DATE = "2026-07-08"

SURFACES: dict[str, dict[str, str]] = {
    "economic_plans": {
        "folder": "economic_plans",
        "object_type": "economic_plan",
        "merge_model": "additive_object_merge",
    },
    "ai_budget": {
        "folder": "ai_budget",
        "object_type": "ai_budget_entry",
        "merge_model": "top_level_duplicate_unproven; category/resource duplicates allowed",
    },
    "ai_planet_specialization": {
        "folder": "ai_planet_specialization",
        "object_type": "ai_planet_specialization",
        "merge_model": "folder_absent_in_local_4.4.5",
    },
    "colony_types": {
        "folder": "colony_types",
        "object_type": "colony_type",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "colony_automation": {
        "folder": "colony_automation",
        "object_type": "colony_automation",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "colony_automation_categories": {
        "folder": "colony_automation_categories",
        "object_type": "colony_automation_category",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "on_actions": {
        "folder": "on_actions",
        "object_type": "on_action",
        "merge_model": "additive_object_merge",
    },
    "megastructures": {
        "folder": "megastructures",
        "object_type": "megastructure",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "starbase_modules": {
        "folder": "starbase_modules",
        "object_type": "starbase_module",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "starbase_buildings": {
        "folder": "starbase_buildings",
        "object_type": "starbase_building",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "ship_sizes": {
        "folder": "ship_sizes",
        "object_type": "ship_size",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "section_templates": {
        "folder": "section_templates",
        "object_type": "section_template",
        "merge_model": "last_definition_wins_by_section_key",
    },
    "component_templates": {
        "folder": "component_templates",
        "object_type": "component_template",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "component_sets": {
        "folder": "component_sets",
        "object_type": "component_set",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "global_ship_designs": {
        "folder": "global_ship_designs",
        "object_type": "global_ship_design",
        "merge_model": "last_definition_wins_by_design_name",
    },
    "districts": {
        "folder": "districts",
        "object_type": "district",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "zones": {
        "folder": "zones",
        "object_type": "zone",
        "merge_model": "last_definition_wins_by_object_id",
    },
    "zone_slots": {
        "folder": "zone_slots",
        "object_type": "zone_slot",
        "merge_model": "last_definition_wins_by_object_id",
    },
}

FOCUS_IDS = {
    "1121692237",
    "3250900527",
    "683230077",
    "2648658105",
    "819148835",
    "3173239930",
    "1732447147",
    "2284514368",
    "3610149307",
    "1595876588",
    "3696204283",
}

PD_ZONE_REF_KEYS = {"zone", "zone_slot", "zone_slots", "district_set"}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def install_version() -> dict[str, str]:
    path = STELLARIS / "launcher-settings.json"
    if not path.exists():
        return {}
    data = load_json(path)
    return {
        "version": data.get("version", ""),
        "rawVersion": data.get("rawVersion", ""),
        "modsCompatibilityVersion": data.get("modsCompatibilityVersion", ""),
    }


def launcher_active() -> dict[str, Any]:
    con = sqlite3.connect(USER / "launcher-v2.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    active = cur.execute("select * from playsets where isActive=1").fetchone()
    if active is None:
        return {"active": None, "mods": []}
    mods = cur.execute(
        """
        select pm.position, pm.enabled, m.gameRegistryId, m.steamId, m.displayName,
               m.version, m.requiredVersion, m.source, m.dirPath, m.archivePath
        from playsets_mods pm
        join mods m on m.id = pm.modId
        where pm.playsetId = ? and pm.enabled = 1
        order by pm.position
        """,
        (active["id"],),
    ).fetchall()
    return {"active": dict(active), "mods": [dict(row) for row in mods]}


def active_roots() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    version = install_version()
    dlc = load_json(USER / "dlc_load.json")
    registry = load_json(USER / "mods_registry.json")
    by_registry = {entry.get("gameRegistryId"): entry for entry in registry.values()}
    launcher = launcher_active()
    launcher_ids = [row["gameRegistryId"] for row in launcher["mods"]]
    dlc_ids = list(dlc.get("enabled_mods", []))

    roots: list[dict[str, Any]] = [
        {
            "load_position": 0,
            "game_registry_id": "vanilla",
            "steam_id": "vanilla",
            "display_name": "Stellaris vanilla",
            "version": version.get("version", ""),
            "required_version": version.get("rawVersion", ""),
            "source": "vanilla",
            "root": str(STELLARIS),
            "common_exists": (STELLARIS / "common").exists(),
            "descriptor_exists": False,
            "is_focus_source": True,
        }
    ]

    missing = []
    for index, registry_id in enumerate(dlc_ids, start=1):
        entry = by_registry.get(registry_id)
        if not entry:
            missing.append(registry_id)
            continue
        root = Path(str(entry.get("dirPath") or "__missing__"))
        steam_id = str(entry.get("steamId") or "")
        roots.append(
            {
                "load_position": index,
                "game_registry_id": registry_id,
                "steam_id": steam_id,
                "display_name": entry.get("displayName") or "",
                "version": entry.get("version") or "",
                "required_version": entry.get("requiredVersion") or "",
                "source": entry.get("source") or "",
                "root": str(root),
                "common_exists": (root / "common").exists(),
                "descriptor_exists": (root / "descriptor.mod").exists(),
                "is_focus_source": steam_id in FOCUS_IDS or "StellarAIDirector" in str(root),
            }
        )

    meta = {
        "dlc_enabled_count": len(dlc_ids),
        "launcher_enabled_count": len(launcher_ids),
        "launcher_active_playset": launcher.get("active"),
        "dlc_minus_launcher": [item for item in dlc_ids if item not in launcher_ids],
        "launcher_minus_dlc": [item for item in launcher_ids if item not in dlc_ids],
        "registry_missing": missing,
        "dlc_load_path": str(USER / "dlc_load.json"),
        "mods_registry_path": str(USER / "mods_registry.json"),
        "launcher_sqlite_path": str(USER / "launcher-v2.sqlite"),
    }
    return roots, meta


def iter_text_files(folder: Path) -> Iterable[Path]:
    if not folder.exists():
        return []
    suffixes = {".txt", ".mod", ".asset", ".gfx", ".gui"}
    return sorted(path for path in folder.rglob("*") if path.is_file() and path.suffix.lower() in suffixes)


def block_has_key(value: Any, key: str) -> bool:
    return isinstance(value, PDXBlock) and any(assign.key == key for assign in iter_assignments(value))


def block_count_key(value: Any, key: str) -> int:
    if not isinstance(value, PDXBlock):
        return 0
    return sum(1 for assign in iter_assignments(value) if assign.key == key)


def child_atom(value: Any, key: str) -> str:
    if not isinstance(value, PDXBlock):
        return ""
    for assign in block_assignments(value):
        if assign.key == key and isinstance(assign.value, PDXAtom):
            return assign.value.value.strip('"')
    return ""


def block_key_values(value: Any, keys: set[str]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    if not isinstance(value, PDXBlock):
        return values
    for assign in iter_assignments(value):
        if assign.key not in keys:
            continue
        if isinstance(assign.value, PDXAtom):
            values.append((assign.key, assign.value.value.strip('"')))
        elif isinstance(assign.value, PDXBlock):
            for item in assign.value.items:
                if isinstance(item, PDXAtom):
                    values.append((assign.key, item.value.strip('"')))
                elif isinstance(item, type(assign)) and isinstance(item.value, PDXAtom):
                    values.append((item.key, item.value.value.strip('"')))
    return values


def object_id_for(surface: str, assignment: Any) -> str:
    if surface in {"section_templates", "component_templates", "component_sets"}:
        return child_atom(assignment.value, "key") or child_atom(assignment.value, "name") or assignment.key
    if surface == "global_ship_designs":
        return child_atom(assignment.value, "name") or assignment.key
    return assignment.key


def global_design_refs(value: Any) -> list[tuple[str, str, str]]:
    refs: list[tuple[str, str, str]] = []
    if not isinstance(value, PDXBlock):
        return refs
    for assign in block_assignments(value):
        if assign.key == "ship_size" and isinstance(assign.value, PDXAtom):
            refs.append(("ship_size", assign.value.value.strip('"'), "ship_sizes"))
        elif assign.key == "required_component" and isinstance(assign.value, PDXAtom):
            refs.append(("required_component", assign.value.value.strip('"'), "component_templates"))
        elif assign.key == "section" and isinstance(assign.value, PDXBlock):
            for section_child in block_assignments(assign.value):
                if section_child.key == "template" and isinstance(section_child.value, PDXAtom):
                    refs.append(("section.template", section_child.value.value.strip('"'), "section_templates"))
                elif section_child.key == "component" and isinstance(section_child.value, PDXBlock):
                    for component_child in block_assignments(section_child.value):
                        if component_child.key == "template" and isinstance(component_child.value, PDXAtom):
                            refs.append(("component.template", component_child.value.value.strip('"'), "component_templates"))
    return refs


def source_kind(source: dict[str, Any]) -> str:
    steam_id = str(source.get("steam_id") or "")
    name = str(source.get("display_name") or "")
    root = str(source.get("root") or "")
    if source.get("source") == "vanilla":
        return "vanilla"
    if "StellarAIDirector" in root:
        return "local_patch"
    if steam_id in FOCUS_IDS:
        return "focus_mod"
    if "Planetary Diversity" in name:
        return "planetary_diversity_family"
    if "NSC3" in name or "Extra Ship Components" in name or "ESC" in name:
        return "ship_component_family"
    return "enabled_mod"


def collect_definitions(roots: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    definitions: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    provenance: list[dict[str, Any]] = []
    order = 0

    for source in roots:
        root = Path(str(source["root"]))
        common = root / "common"
        for surface, spec in SURFACES.items():
            folder = common / spec["folder"]
            files = list(iter_text_files(folder)) if folder.exists() else []
            object_count = 0
            ai_weight_objects = 0
            parse_error_count = 0

            for file_path in files:
                relative_file = file_path.relative_to(root).as_posix()
                try:
                    parsed = parse_file(file_path)
                except PDXParseError as exc:
                    parse_error_count += 1
                    errors.append(
                        {
                            "surface": surface,
                            "load_position": source["load_position"],
                            "game_registry_id": source["game_registry_id"],
                            "steam_id": source["steam_id"],
                            "display_name": source["display_name"],
                            "relative_file": relative_file,
                            "source_file": str(file_path),
                            "diagnostic": str(exc),
                        }
                    )
                    continue

                assignment_index = 0
                for assignment in block_assignments(parsed):
                    if assignment.key.startswith("@") or not isinstance(assignment.value, PDXBlock):
                        continue
                    object_id = object_id_for(surface, assignment)
                    if not object_id or object_id.startswith("@"):
                        continue
                    assignment_index += 1
                    object_count += 1
                    has_ai_weight = block_has_key(assignment.value, "ai_weight")
                    if has_ai_weight:
                        ai_weight_objects += 1
                    order += 1
                    definitions.append(
                        {
                            "order_index": order,
                            "surface": surface,
                            "object_type": spec["object_type"],
                            "object_id": object_id,
                            "raw_assignment_key": assignment.key,
                            "merge_model": spec["merge_model"],
                            "load_position": source["load_position"],
                            "game_registry_id": source["game_registry_id"],
                            "steam_id": source["steam_id"],
                            "display_name": source["display_name"],
                            "source_kind": source_kind(source),
                            "source": source["source"],
                            "root": source["root"],
                            "relative_file": relative_file,
                            "source_file": str(file_path),
                            "file_order_key": relative_file.lower(),
                            "assignment_index_in_file": assignment_index,
                            "has_ai_weight": "yes" if has_ai_weight else "no",
                            "ai_weight_count": block_count_key(assignment.value, "ai_weight"),
                            "has_potential": "yes" if block_has_key(assignment.value, "potential") else "no",
                            "has_possible": "yes" if block_has_key(assignment.value, "possible") else "no",
                            "has_allow": "yes" if block_has_key(assignment.value, "allow") else "no",
                            "has_resources": "yes" if block_has_key(assignment.value, "resources") else "no",
                            "has_ai_resource_production": "yes"
                            if block_has_key(assignment.value, "ai_resource_production")
                            else "no",
                            "has_ai_ship_data": "yes" if block_has_key(assignment.value, "ai_ship_data") else "no",
                            "nested_from_count": block_count_key(assignment.value, "from"),
                            "nested_owner_count": block_count_key(assignment.value, "owner"),
                            "nested_root_count": block_count_key(assignment.value, "root"),
                        }
                    )

            provenance.append(
                {
                    "surface": surface,
                    "folder": spec["folder"],
                    "merge_model": spec["merge_model"],
                    "load_position": source["load_position"],
                    "game_registry_id": source["game_registry_id"],
                    "steam_id": source["steam_id"],
                    "display_name": source["display_name"],
                    "source_kind": source_kind(source),
                    "root": source["root"],
                    "folder_exists": "yes" if folder.exists() else "no",
                    "file_count": len(files),
                    "object_count": object_count,
                    "ai_weight_object_count": ai_weight_objects,
                    "parse_error_count": parse_error_count,
                }
            )

    return definitions, errors, provenance


def build_winners(definitions: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in definitions:
        grouped[(row["surface"], row["object_id"])].append(row)

    winners: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    for (_surface, _object_id), rows in sorted(grouped.items()):
        rows_sorted = sorted(
            rows,
            key=lambda row: (
                int(row["load_position"]),
                str(row["file_order_key"]),
                int(row["assignment_index_in_file"]),
                int(row["order_index"]),
            ),
        )
        winner = rows_sorted[-1]
        source_summary = " | ".join(
            f"{row['load_position']}:{row['display_name']}:{row['relative_file']}" for row in rows_sorted
        )
        definitions_count = len(rows_sorted)
        source_mod_count = len({(row["load_position"], row["display_name"]) for row in rows_sorted})
        risk = "none"
        if definitions_count > 1:
            risk = "merge_expected" if "additive" in str(winner["merge_model"]) else "override_conflict"
        result = {
            **winner,
            "definitions_count": definitions_count,
            "source_mod_count": source_mod_count,
            "all_sources_load_order": source_summary,
            "conflict_or_merge_risk": risk,
        }
        winners.append(result)
        if definitions_count > 1:
            conflicts.append(result)
    return winners, conflicts


def collect_ship_reference_checks(definitions: list[dict[str, Any]], winners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    winner_ids: dict[str, set[str]] = defaultdict(set)
    for row in winners:
        winner_ids[row["surface"]].add(row["object_id"])

    winner_keys = {(row["surface"], row["object_id"], row["load_position"], row["relative_file"]) for row in winners}
    rows: list[dict[str, Any]] = []
    for row in definitions:
        if row["surface"] not in {"section_templates", "global_ship_designs"}:
            continue
        if (row["surface"], row["object_id"], row["load_position"], row["relative_file"]) not in winner_keys:
            continue
        try:
            parsed = parse_file(Path(row["source_file"]))
        except PDXParseError:
            continue
        for assignment in block_assignments(parsed):
            if not isinstance(assignment.value, PDXBlock) or object_id_for(row["surface"], assignment) != row["object_id"]:
                continue
            if row["surface"] == "section_templates":
                ship_size = child_atom(assignment.value, "ship_size")
                if ship_size:
                    rows.append(
                        {
                            **row,
                            "reference_key": "ship_size",
                            "reference_value": ship_size,
                            "target_surface": "ship_sizes",
                            "reference_status": "ok" if ship_size in winner_ids["ship_sizes"] else "missing",
                        }
                    )
            if row["surface"] == "global_ship_designs":
                for ref_key, ref_val, target in global_design_refs(assignment.value):
                    if ref_val and not ref_val.isdigit() and not ref_val.startswith("@"):
                        rows.append(
                            {
                                **row,
                                "reference_key": ref_key,
                                "reference_value": ref_val,
                                "target_surface": target,
                                "reference_status": "ok" if ref_val in winner_ids[target] else "missing",
                            }
                        )
            break
    return rows


def collect_planetary_diversity_checks(definitions: list[dict[str, Any]], winners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    winner_ids: dict[str, set[str]] = defaultdict(set)
    for row in winners:
        winner_ids[row["surface"]].add(row["object_id"])

    rows: list[dict[str, Any]] = []
    for row in definitions:
        if row["surface"] not in {"districts", "zones", "zone_slots"}:
            continue
        if "Planetary Diversity" not in str(row["display_name"]) and row["source_kind"] != "vanilla":
            continue
        try:
            parsed = parse_file(Path(row["source_file"]))
        except PDXParseError:
            continue
        for assignment in block_assignments(parsed):
            if not isinstance(assignment.value, PDXBlock) or object_id_for(row["surface"], assignment) != row["object_id"]:
                continue
            refs = block_key_values(assignment.value, PD_ZONE_REF_KEYS)
            if not refs:
                rows.append(
                    {
                        **row,
                        "reference_key": "",
                        "reference_value": "",
                        "target_surface": "",
                        "reference_status": "no_explicit_zone_reference_detected",
                    }
                )
            for ref_key, ref_val in refs:
                target = "zone_slots" if "slot" in ref_key else "zones"
                status = "ok" if ref_val in winner_ids[target] or ref_val in winner_ids["districts"] else "not_checked_or_missing"
                rows.append(
                    {
                        **row,
                        "reference_key": ref_key,
                        "reference_value": ref_val,
                        "target_surface": target,
                        "reference_status": status,
                    }
                )
            break
    return rows


def summarize_surfaces(
    definitions: list[dict[str, Any]],
    conflicts: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    errors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for surface, spec in SURFACES.items():
        surface_defs = [row for row in definitions if row["surface"] == surface]
        surface_conflicts = [row for row in conflicts if row["surface"] == surface]
        surface_prov = [row for row in provenance if row["surface"] == surface]
        rows.append(
            {
                "surface": surface,
                "folder": spec["folder"],
                "merge_model": spec["merge_model"],
                "definition_count": len(surface_defs),
                "unique_object_count": len({row["object_id"] for row in surface_defs}),
                "conflict_or_merge_count": len(surface_conflicts),
                "source_root_count_with_folder": sum(1 for row in surface_prov if row["folder_exists"] == "yes"),
                "source_root_count_with_objects": sum(1 for row in surface_prov if int(row["object_count"]) > 0),
                "ai_weight_definition_count": sum(1 for row in surface_defs if row["has_ai_weight"] == "yes"),
                "parse_error_count": sum(1 for row in errors if row["surface"] == surface),
                "focus_source_object_count": sum(
                    1
                    for row in surface_defs
                    if row["source_kind"] in {"focus_mod", "local_patch", "planetary_diversity_family", "ship_component_family"}
                ),
            }
        )
    return rows


def run_cmd(args: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(args, cwd=str(REPO), text=True, capture_output=True, timeout=60)
        return {
            "command": " ".join(args),
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except Exception as exc:  # pragma: no cover - diagnostic fallback.
        return {"command": " ".join(args), "exit_code": "error", "stdout": "", "stderr": str(exc)}


def cwtools_diagnostics(parse_errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for args in (["where.exe", "cwtools"], ["where.exe", "cwtools-cli"], ["dotnet", "tool", "list", "-g"]):
        result = run_cmd(args)
        rows.append(
            {
                "check": result["command"],
                "status": "pass" if result["exit_code"] == 0 else "not_found_or_failed",
                "exit_code": result["exit_code"],
                "detail": (result["stdout"] or result["stderr"])[:1000],
            }
        )

    extension_dirs = [
        Path.home() / ".vscode" / "extensions",
        Path.home() / ".vscode-insiders" / "extensions",
        Path.home() / ".cursor" / "extensions",
    ]
    found_ext = []
    for base in extension_dirs:
        if base.exists():
            found_ext.extend(str(path) for path in base.iterdir() if path.is_dir() and re.search(r"cwtools|tboby", path.name, re.I))
    rows.append(
        {
            "check": "VS Code/Cursor CWTools extension directories",
            "status": "found" if found_ext else "not_found",
            "exit_code": "",
            "detail": " | ".join(found_ext),
        }
    )
    rows.append(
        {
            "check": "PDX parser diagnostics for requested active-stack surfaces",
            "status": "pass" if not parse_errors else "warnings",
            "exit_code": "",
            "detail": f"parse_error_count={len(parse_errors)}; see pdx-parse-diagnostics-2026-07-08.csv",
        }
    )
    return rows


def make_markdown(
    summary_rows: list[dict[str, Any]],
    roots: list[dict[str, Any]],
    meta: dict[str, Any],
    conflicts: list[dict[str, Any]],
    ship_checks: list[dict[str, Any]],
    pd_checks: list[dict[str, Any]],
    parse_errors: list[dict[str, Any]],
    cw_rows: list[dict[str, Any]],
) -> str:
    version = install_version()
    focus_roots = [row for row in roots if row.get("is_focus_source")]
    top_conflicts = sorted(conflicts, key=lambda row: (row["surface"], -int(row["definitions_count"]), row["object_id"]))[:25]
    missing_ship = [row for row in ship_checks if row["reference_status"] == "missing"]
    pd_missing = [row for row in pd_checks if row["reference_status"] == "not_checked_or_missing"]
    cw_status = "; ".join(f"{row['check']}={row['status']}" for row in cw_rows)

    def surface_line(name: str) -> str:
        row = next(item for item in summary_rows if item["surface"] == name)
        return (
            f"| {name} | {row['definition_count']} | {row['unique_object_count']} | "
            f"{row['conflict_or_merge_count']} | {row['source_root_count_with_folder']} | "
            f"{row['ai_weight_definition_count']} | {row['merge_model']} |"
        )

    lines = [
        f"# Stellaris Codex Modding Guide Packet Supplement ({DATE})",
        "",
        "## Scope And Authority",
        "",
        f"This supplement verifies the attached `stellaris_coding_agent_packet.zip` against the local game and active playset on {DATE}. It is source-provenance documentation only; it did not edit live game, Workshop, or mod source files.",
        "",
        f"Important correction: the local install is `{version.get('version', 'unknown')}` with `rawVersion={version.get('rawVersion', 'unknown')}` and `modsCompatibilityVersion={version.get('modsCompatibilityVersion', 'unknown')}` from `{STELLARIS / 'launcher-settings.json'}`. The request and packet refer to 4.4.4, but the current inspected source files are 4.4.5. Treat these findings as stable 4.4.x evidence and re-check against a true 4.4.4 rollback before making 4.4.4-only claims.",
        "",
        "Live playset evidence:",
        f"- `dlc_load.json` enabled mods: {meta['dlc_enabled_count']}.",
        f"- Active launcher playset: `{(meta.get('launcher_active_playset') or {}).get('name', 'unknown')}` from `{meta['launcher_sqlite_path']}`.",
        f"- Launcher enabled mods: {meta['launcher_enabled_count']}.",
        f"- `dlc_load.json` and launcher active playset differ by: dlc-minus-launcher={len(meta['dlc_minus_launcher'])}, launcher-minus-dlc={len(meta['launcher_minus_dlc'])}.",
        "",
        "## Requested Open Questions",
        "",
        "| Topic | Verified Finding | Evidence | Residual Risk |",
        "|---|---|---|---|",
        "| `common/economic_plans` | Correct the packet: economic plans are not simple full-object last-winner objects. Vanilla `00_example.txt` says economic plans are additive and multiple instances of a plan are mashed together; duplicate subplan names overwrite the existing subplan. | `C:/Steam/steamapps/common/Stellaris/common/economic_plans/00_example.txt`; see `surface-summary-2026-07-08.csv` and conflict matrix. | Static report does not resolve nested subplan wins; inspect subplan names before patching. |",
        "| `common/ai_budget` | Folder exists in 4.4.5 with 20 vanilla files plus modded definitions. Vanilla docs show `potential` gates entries; budget categories must have `use_for_ai_budget = yes`; multiple entries with the same category and resource are allowed. | `C:/Steam/steamapps/common/Stellaris/common/ai_budget/documentation.txt` and `00_alloys_budget.txt`; Gigas active source has additional special-resource budgets. | No local source proves top-level same-ID budget entries merge like economic plans; treat duplicate top-level budget IDs as conflict risk. |",
        "| `common/ai_planet_specialization` | Correct the packet: this folder is absent in the current local 4.4.5 install. Related current surfaces are `common/colony_types`, `common/colony_automation*`, `common/districts`, `common/zones`, and `common/zone_slots`. | Filesystem check against `C:/Steam/steamapps/common/Stellaris/common`; surface summary has zero folder roots for `ai_planet_specialization`. | The term still appears as district flags such as `exempt_from_ai_planet_specialization`; do not create a same-named folder without schema proof. |",
        "| `common/on_actions` merge behavior | Treat as additive/merge-like, not simple last-winner. Vanilla economic-plan docs explicitly compare economic-plan additive overwriting to on_actions; the on_actions README defines `events` and `random_events` blocks and custom on_actions. | `C:/Steam/steamapps/common/Stellaris/common/economic_plans/00_example.txt`; `C:/Steam/steamapps/common/Stellaris/common/on_actions/99_README_ON_ACTIONS.txt`. | Nested duplicate event entries still need object-level review; static matrix labels duplicate on_actions as `merge_expected`. |",
        "| Gigas megastructure AI hooks | Gigas active source contributes megastructure definitions, AI-weighted megastructures, and multiple AI budget files for special resources such as negative mass, sentient metal, and supertensiles. | `surface-source-provenance-2026-07-08.csv`, `winning-objects-2026-07-08.csv`, Gigas JDoc index, and active source root at load position 62. | Static source proves hooks exist, not that AI reaches the tech/economy state to use them. Runtime observer proof is still required. |",
        "| Starbase Extended starbase scopes | Starbase Extended active source defines starbase modules/buildings with `ai_weight`; static report records nested `from`/`owner` usage counts for scope-sensitive review. | Load position 72 source root; `starbase-extended-scope-report-2026-07-08.csv`. | CWTools schema was not available locally, so scope diagnostics are parser/provenance only. |",
        "| NSC3/ESC ship/component/section validity | NSC3 and ESC parse across requested ship/component surfaces. The generated ship reference check reports missing references separately for global designs/section templates. | `ship-design-reference-checks-2026-07-08.csv`; active load positions 70-71 plus NSC3 shipset patches at 42-48 and 77-80. | Static parser is not a full game schema engine; CWTools or launch logs should confirm unresolved missing rows. |",
        "| Planetary Diversity zones/districts | Planetary Diversity family is active at positions 64-67 plus UI patch at 107. Current 4.4.5 uses `zones` and `zone_slots`; generated report checks PD district/zone references against active winners. | `planetary-diversity-zone-district-report-2026-07-08.csv`. | Some references are not simple object IDs; rows marked `not_checked_or_missing` need CWTools/runtime log confirmation before treating them as broken. |",
        "",
        "## Surface Summary",
        "",
        "| Surface | Definitions | Unique Objects | Conflicts/Merges | Source Roots With Folder | AI Weight Definitions | Merge Model |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    for name in [
        "economic_plans",
        "ai_budget",
        "ai_planet_specialization",
        "colony_types",
        "on_actions",
        "megastructures",
        "starbase_modules",
        "starbase_buildings",
        "ship_sizes",
        "section_templates",
        "component_templates",
        "component_sets",
        "global_ship_designs",
        "districts",
        "zones",
        "zone_slots",
    ]:
        lines.append(surface_line(name))

    lines.extend(
        [
            "",
            "## Focus Source Roots",
            "",
            "| Load | Steam ID | Name | Required Version | Root |",
            "|---:|---|---|---|---|",
        ]
    )
    for row in focus_roots:
        lines.append(f"| {row['load_position']} | {row['steam_id']} | {row['display_name']} | {row['required_version']} | `{row['root']}` |")

    lines.extend(
        [
            "",
            "## Conflict And Winner Notes",
            "",
            "The complete active-load-order matrix is in `tables/active-load-order-conflict-matrix-2026-07-08.csv`; the complete winner table is in `tables/winning-objects-2026-07-08.csv`. The rows below are the first high-signal duplicate objects after sorting by surface and duplicate count.",
            "",
            "| Surface | Object | Definitions | Winner | Risk |",
            "|---|---|---:|---|---|",
        ]
    )
    for row in top_conflicts:
        lines.append(
            f"| {row['surface']} | `{row['object_id']}` | {row['definitions_count']} | "
            f"{row['load_position']}:{row['display_name']} `{row['relative_file']}` | {row['conflict_or_merge_risk']} |"
        )

    lines.extend(
        [
            "",
            "## Static Diagnostics",
            "",
            f"CWTools availability checks: {cw_status}.",
            "",
            f"PDX parser diagnostics for requested surfaces: {len(parse_errors)} parse errors. See `tables/pdx-parse-diagnostics-2026-07-08.csv`.",
            "",
            f"Ship/section/component reference checks: {len(ship_checks)} rows, {len(missing_ship)} missing-reference rows. See `tables/ship-design-reference-checks-2026-07-08.csv`.",
            "",
            f"Planetary Diversity zone/district checks: {len(pd_checks)} rows, {len(pd_missing)} not-checked-or-missing rows. See `tables/planetary-diversity-zone-district-report-2026-07-08.csv`.",
            "",
            "## Safe Runtime Validation Plan",
            "",
            "Do not run this automatically. Use it only after explicit user approval for runtime testing.",
            "",
            "1. Before launch, run `python tools\\manage_stellaris_commands_at_date.py status`; the live `commands_at_date.txt` must be absent unless the user approves an observer run.",
            "2. Snapshot `dlc_load.json`, `mods_registry.json`, active `launcher-v2.sqlite` playset rows, and the generated conflict/winner tables from this supplement.",
            "3. If the test is only load-safety, launch to main menu with the active playset and capture `error.log`, `game.log`, and `setup.log`; do not arm dated commands.",
            "4. If the test is AI behavior, create a supervised observer-run folder, then enable the managed command schedule only through `python tools\\manage_stellaris_commands_at_date.py enable`; use `game_speed 5` for approved observer schedules.",
            "5. Capture checkpoints at 2250, 2300, 2325, and 2350 or stop early if research/economy slope makes the 2350 benchmark impossible.",
            "6. Disable the live command schedule before handoff with `python tools\\manage_stellaris_commands_at_date.py disable`, then verify `status` reports absent.",
            "7. Treat runtime logs as the source of truth for CWTools-unchecked missing references, GUI layout, AI megastructure adoption, upkeep spirals, and starbase spending crowd-out.",
            "",
            "## Generated Artifacts",
            "",
        ]
    )
    for filename in [
        "active-source-roots-2026-07-08.csv",
        "surface-source-provenance-2026-07-08.csv",
        "surface-summary-2026-07-08.csv",
        "object-definitions-2026-07-08.csv",
        "active-load-order-conflict-matrix-2026-07-08.csv",
        "winning-objects-2026-07-08.csv",
        "gigas-megastructure-ai-hooks-2026-07-08.csv",
        "starbase-extended-scope-report-2026-07-08.csv",
        "ship-design-reference-checks-2026-07-08.csv",
        "planetary-diversity-zone-district-report-2026-07-08.csv",
        "pdx-parse-diagnostics-2026-07-08.csv",
        "cwtools-diagnostics-2026-07-08.csv",
    ]:
        lines.append(f"- `tables/{filename}`")
    if FOLLOWUP.exists():
        for filename in [
            "stellaris_44x_ai_surface_followup_report.md",
            "cwtools_schema_surface_matrix.csv",
            "mod_maintainer_guidance_matrix.csv",
            "remaining_open_questions.csv",
        ]:
            if (FOLLOWUP / filename).exists():
                lines.append(f"- `webchatgpt-followup-2026-07-08/{filename}`")
        lines.extend(
            [
                "",
                "## Web ChatGPT Follow-up Reconciliation",
                "",
                "Returned follow-up files are preserved under `webchatgpt-followup-2026-07-08/`.",
                "They refine the supplement but do not overturn the local-source findings.",
                "",
                "| Topic | Follow-up result | Effect on this supplement |",
                "|---|---|---|",
                "| CWTools schema authority | Public CWTools is the current schema source found, but no public 4.4.4- or 4.4.5-labelled schema ref was found. | Keep local 4.4.5 files as the inspected source of truth; treat public CWTools as current schema guidance, not a proven 4.4.4/4.4.5 diff. |",
                "| `economic_plans` and `ai_budget` | Public CWT exposes object paths and fields; local economic-plan docs still provide the strongest merge semantics found. | No change: economic plans are additive/merge-like locally; top-level `ai_budget` duplicate behavior still needs active-stack/runtime validation. |",
                "| `on_actions` | Public CWT validates shape only; nested duplicate event-ID behavior is not specified. | No change: duplicate nested `events` and `random_events` semantics remain runtime-test questions. |",
                "| 4.4.4 versus 4.4.5 | No public exact version split was found for the requested surfaces. | A verified 4.4.4 depot/snapshot is still required for exact rollback claims. |",
                "| NSC3/ESC/SFT | Public guidance supports ESC before NSC3, Spacefleet Tactica ordering/add-ons, and ship-designer/runtime smoke tests. | Prioritize final graph validation for ship sizes, sections, component templates/sets, combat computers, and global ship designs. |",
                "| Planetary Diversity/UIOD | Public guidance confirms 4.4 support and UIOD/planet-view compatibility concerns, but not exact zone/slot definitions. | Keep local PD zone/district table as source evidence; verify visible zones/planet UI in runtime only with approval. |",
                "| Gigas/URP/UMP/starbases | Public guidance supports Gigas AI megastructure use and resource/UI patching concerns; Starbase Extended identity still needs exact local workshop-source confirmation. | Keep Gigas hooks as source-proven, and treat resource-group/topbar/starbase UI conflicts as active-stack validation items. |",
                "| CWTools diagnostics | Strongest public machine-readable path found is `cwtools/cwtools-action` with `output.json`; no maintained standalone Windows CLI was verified. | Local CWTools diagnostics remain unavailable; CI/action-based diagnostics are the recommended next schema-validation route. |",
            ]
        )
    lines.extend(
        [
            "",
            "## Remaining Open Questions",
            "",
            "The current remaining questions are captured in `webchatgpt-followup-2026-07-08/remaining_open_questions.csv`. Highest-priority follow-up remains: exact 4.4.4 depot diff, duplicate nested `on_actions` runtime behavior, active-stack economic-plan merged subplan winners, NSC3/ESC/SFT ship graph validity, PD/UIOD runtime visibility, Starbase Extended identity, and machine-readable CWTools action diagnostics.",
            "",
        ]
    )
    return "\n".join(lines)


def make_readme() -> str:
    files = sorted(path.relative_to(PACKET).as_posix() for path in PACKET.rglob("*") if path.is_file()) if PACKET.exists() else []
    lines = [
        f"# Stellaris Codex Modding Guide Packet Intake ({DATE})",
        "",
        "This folder preserves the attached packet and adds a source-provenance supplement generated from the current local Stellaris install and active playset.",
        "",
        "Important: the local inspected install is Stellaris 4.4.5, not 4.4.4. The packet remains useful for 4.4.x guidance, but exact 4.4.4 rollback claims need a separate rollback validation pass.",
        "",
        "## Files",
        "",
        "- `packet/stellaris_coding_agent_packet/`: extracted attached packet contents.",
        "- `supplement-2026-07-08.md`: verified/corrected supplement.",
        "- `tables/`: generated CSV evidence tables.",
        "- `webchatgpt-followup-2026-07-08/`: returned Web ChatGPT research report and CSV matrices.",
        "",
        "## Packet Inventory",
        "",
    ]
    for item in files:
        lines.append(f"- `packet/stellaris_coding_agent_packet/{item}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    roots, meta = active_roots()
    definitions, parse_errors, provenance = collect_definitions(roots)
    winners, conflicts = build_winners(definitions)
    ship_checks = collect_ship_reference_checks(definitions, winners)
    pd_checks = collect_planetary_diversity_checks(definitions, winners)
    summary_rows = summarize_surfaces(definitions, conflicts, provenance, parse_errors)
    cw_rows = cwtools_diagnostics(parse_errors)

    write_csv(
        TABLES / "active-source-roots-2026-07-08.csv",
        roots,
        [
            "load_position",
            "game_registry_id",
            "steam_id",
            "display_name",
            "version",
            "required_version",
            "source",
            "root",
            "common_exists",
            "descriptor_exists",
            "is_focus_source",
        ],
    )
    write_json(TABLES / "active-playset-metadata-2026-07-08.json", meta)
    write_csv(
        TABLES / "surface-source-provenance-2026-07-08.csv",
        provenance,
        [
            "surface",
            "folder",
            "merge_model",
            "load_position",
            "game_registry_id",
            "steam_id",
            "display_name",
            "source_kind",
            "root",
            "folder_exists",
            "file_count",
            "object_count",
            "ai_weight_object_count",
            "parse_error_count",
        ],
    )
    definition_fields = [
        "order_index",
        "surface",
        "object_type",
        "object_id",
        "raw_assignment_key",
        "merge_model",
        "load_position",
        "game_registry_id",
        "steam_id",
        "display_name",
        "source_kind",
        "source",
        "root",
        "relative_file",
        "source_file",
        "has_ai_weight",
        "ai_weight_count",
        "has_potential",
        "has_possible",
        "has_allow",
        "has_resources",
        "has_ai_resource_production",
        "has_ai_ship_data",
        "nested_from_count",
        "nested_owner_count",
        "nested_root_count",
    ]
    write_csv(TABLES / "object-definitions-2026-07-08.csv", definitions, definition_fields)
    write_csv(
        TABLES / "winning-objects-2026-07-08.csv",
        winners,
        [
            *definition_fields[1:],
            "definitions_count",
            "source_mod_count",
            "all_sources_load_order",
            "conflict_or_merge_risk",
        ],
    )
    write_csv(
        TABLES / "active-load-order-conflict-matrix-2026-07-08.csv",
        conflicts,
        [
            "surface",
            "object_type",
            "object_id",
            "merge_model",
            "definitions_count",
            "source_mod_count",
            "load_position",
            "game_registry_id",
            "steam_id",
            "display_name",
            "source_kind",
            "relative_file",
            "source_file",
            "has_ai_weight",
            "ai_weight_count",
            "all_sources_load_order",
            "conflict_or_merge_risk",
        ],
    )
    write_csv(
        TABLES / "surface-summary-2026-07-08.csv",
        summary_rows,
        [
            "surface",
            "folder",
            "merge_model",
            "definition_count",
            "unique_object_count",
            "conflict_or_merge_count",
            "source_root_count_with_folder",
            "source_root_count_with_objects",
            "ai_weight_definition_count",
            "parse_error_count",
            "focus_source_object_count",
        ],
    )
    write_csv(
        TABLES / "pdx-parse-diagnostics-2026-07-08.csv",
        parse_errors,
        ["surface", "load_position", "game_registry_id", "steam_id", "display_name", "relative_file", "source_file", "diagnostic"],
    )
    write_csv(TABLES / "cwtools-diagnostics-2026-07-08.csv", cw_rows, ["check", "status", "exit_code", "detail"])
    write_csv(
        TABLES / "ship-design-reference-checks-2026-07-08.csv",
        ship_checks,
        ["surface", "object_id", "load_position", "steam_id", "display_name", "relative_file", "reference_key", "reference_value", "target_surface", "reference_status", "source_file"],
    )
    write_csv(
        TABLES / "planetary-diversity-zone-district-report-2026-07-08.csv",
        pd_checks,
        ["surface", "object_id", "load_position", "steam_id", "display_name", "relative_file", "reference_key", "reference_value", "target_surface", "reference_status", "source_file"],
    )

    giga = [row for row in winners if row["steam_id"] == "1121692237" and row["surface"] == "megastructures"]
    write_csv(
        TABLES / "gigas-megastructure-ai-hooks-2026-07-08.csv",
        giga,
        [
            "surface",
            "object_id",
            "load_position",
            "steam_id",
            "display_name",
            "relative_file",
            "has_ai_weight",
            "ai_weight_count",
            "has_resources",
            "has_potential",
            "has_possible",
            "nested_from_count",
            "nested_owner_count",
            "definitions_count",
            "source_file",
        ],
    )
    sbx = [row for row in winners if row["steam_id"] == "3250900527" and row["surface"] in {"starbase_modules", "starbase_buildings"}]
    write_csv(
        TABLES / "starbase-extended-scope-report-2026-07-08.csv",
        sbx,
        [
            "surface",
            "object_id",
            "load_position",
            "steam_id",
            "display_name",
            "relative_file",
            "has_ai_weight",
            "ai_weight_count",
            "has_potential",
            "has_possible",
            "nested_from_count",
            "nested_owner_count",
            "nested_root_count",
            "definitions_count",
            "source_file",
        ],
    )

    (OUT / "README.md").write_text(make_readme(), encoding="utf-8")
    (OUT / "supplement-2026-07-08.md").write_text(
        make_markdown(summary_rows, roots, meta, conflicts, ship_checks, pd_checks, parse_errors, cw_rows),
        encoding="utf-8",
    )

    manifest_rows = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.name != "artifact-manifest-2026-07-08.csv" and "__pycache__" not in path.parts:
            manifest_rows.append(
                {
                    "relative_path": path.relative_to(OUT).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    write_csv(TABLES / "artifact-manifest-2026-07-08.csv", manifest_rows, ["relative_path", "bytes", "sha256"])

    print(
        json.dumps(
            {
                "roots": len(roots),
                "definitions": len(definitions),
                "winners": len(winners),
                "conflicts": len(conflicts),
                "parse_errors": len(parse_errors),
                "ship_reference_rows": len(ship_checks),
                "planetary_diversity_rows": len(pd_checks),
                "out": str(OUT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
