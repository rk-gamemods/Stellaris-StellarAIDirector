#!/usr/bin/env python3
"""Helpers for Stellar AI Director observer-run artifact folders."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from stellar_ai_director_lib import (
    extract_assignment_block,
    iter_numbered_child_blocks,
    load_stellaris_save_gamestate,
    numeric_assignment,
    save_scalar,
    sum_resource_assignments,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
OBSERVER_RUNS_ROOT = REPO_ROOT / "research" / "stellar-ai" / "observer-runs"

CHECKPOINT_FIELDS = [
    "run_id",
    "checkpoint_year",
    "date",
    "empire_rank",
    "empire_name",
    "country_id",
    "economy_power",
    "tech_power",
    "fleet_power",
    "naval_capacity_used",
    "naval_capacity_available",
    "research",
    "alloys_income",
    "consumer_goods_income",
    "energy_income",
    "minerals_income",
    "food_income",
    "pops",
    "colonies",
    "systems",
    "habitats",
    "megastructures",
    "deficits",
    "notes",
    "evidence_file",
]

REGULAR_AI_COUNTRY_TYPES = {"1", "2", "colony", "country"}
FALLEN_OR_SPECIAL_ECONOMY_POWER_FLOOR = 10_000
CHECKPOINT_RESOURCE_FIELDS = {
    "alloys_income": "alloys",
    "consumer_goods_income": "consumer_goods",
    "energy_income": "energy",
    "minerals_income": "minerals",
    "food_income": "food",
}
RESEARCH_RESOURCES = ("physics_research", "society_research", "engineering_research")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def default_run_id(now: datetime | None = None) -> str:
    timestamp = (now or utc_now()).strftime("%Y%m%dT%H%M%SZ")
    return f"observer-{timestamp}"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_readme_text(run_id: str) -> str:
    return f"""# Stellar AI Observer Run {run_id}

Use this folder as the complete evidence packet for one Irony-launched observer experiment.

## Required Files

- `metadata.json`: setup, settings, and run ownership.
- `manual-notes.md`: console verification, qualitative observations, and patch hypotheses.
- `checkpoints.csv`: structured rows for 2250, 2300, 2325, and 2350 benchmark captures.
- `metrics.json`: parsed or modeled metrics derived from saves/logs/checkpoints.
- `summary.json` and `summary.md`: generated run summary.

## Evidence Folders

- `logs/`: copied `game.log`, `error.log`, crash summaries, Irony output, or launcher proof.
- `saves/`: seed save and checkpoint saves used for parsing.
- `screenshots/`: visible proof for settings, commands, empire screens, or anomalies.
- `exports/`: playset exports, mod-list snapshots, or generated comparison reports.
"""


def manual_notes_text(run_id: str) -> str:
    return f"""# Manual Notes For {run_id}

## Setup

- Launch surface:
- Irony collection/playset:
- Stellar AI Director included:
- Game version:
- Galaxy size:
- AI empire count:
- Difficulty:
- Scaling:
- Advanced AI starts:
- Player/AI hidden bonuses:
- Crisis settings:
- Seed save:

## Console Verification

Record exact `help <command>` results before relying on commands.

| command | help verified | result or alternative |
| --- | --- | --- |
| `human_ai` | no | |
| `observe` | no | |
| `game_speed 5` | no | |
| `fast_forward <days> 1` | no | |

## Checkpoint Notes

### 2250

### 2300

### 2325

### 2350

## Qualitative Behavior

- Strong AI behavior:
- Bad economy behavior:
- Bad fleet/war behavior:
- Missing modded asset usage:
- Deficit or collapse cases:

## Patch Hypotheses

Each hypothesis must cite evidence from this run, source files, logs, saves, screenshots, or current research.

| hypothesis | evidence | expected effect | patch status | result |
| --- | --- | --- | --- | --- |
"""


def initial_metadata(run_id: str, created_at_utc: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "created_at_utc": created_at_utc,
        "status": "created",
        "target_game_version": "Stellaris 4.4.5 stable/current local install",
        "target_mod": "Stellar AI Director",
        "launcher": "Irony Mod Manager",
        "hidden_economic_bonuses": False,
        "standard_checkpoints": [2250, 2300, 2325, 2350],
        "benchmark_intent": "Top one or two AI empires plausibly crisis-ready by 2350 without hidden bonuses.",
        "settings": {
            "galaxy_size": "small baseline unless recorded otherwise",
            "difficulty": "Ensign",
            "scaling": "off",
            "advanced_ai_starts": "off",
            "player_bonuses": "off",
        },
        "artifacts": {
            "manual_notes": "manual-notes.md",
            "checkpoints": "checkpoints.csv",
            "metrics": "metrics.json",
            "summary_json": "summary.json",
            "summary_md": "summary.md",
        },
    }


def create_observer_run(root: Path = OBSERVER_RUNS_ROOT, run_id: str | None = None) -> Path:
    run_id = run_id or default_run_id()
    run_dir = root / run_id
    if run_dir.exists():
        raise FileExistsError(f"Observer run already exists: {run_dir}")

    for child in ("logs", "saves", "screenshots", "exports"):
        (run_dir / child).mkdir(parents=True, exist_ok=False)

    created_at = utc_now().isoformat()
    write_text(run_dir / "README.md", run_readme_text(run_id))
    write_json(run_dir / "metadata.json", initial_metadata(run_id, created_at))
    write_text(run_dir / "manual-notes.md", manual_notes_text(run_id))

    with (run_dir / "checkpoints.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHECKPOINT_FIELDS)
        writer.writeheader()

    write_json(run_dir / "metrics.json", {"run_id": run_id, "metrics": []})
    summary = summarize_observer_run(run_dir, write_files=False)
    write_json(run_dir / "summary.json", summary)
    write_text(run_dir / "summary.md", summary_markdown(summary))
    return run_dir


def latest_observer_run(root: Path = OBSERVER_RUNS_ROOT) -> Path:
    if not root.exists():
        raise FileNotFoundError(f"Observer runs root does not exist: {root}")
    candidates = [path for path in root.iterdir() if path.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"No observer run folders found under: {root}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def checkpoint_rows(run_dir: Path) -> list[dict[str, str]]:
    path = run_dir / "checkpoints.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def country_type(country_block: str) -> str:
    match = re.search(r'(^|\n)\s*type\s*=\s*"?([A-Za-z0-9_]+)"?', country_block)
    return match.group(2) if match else ""


def localized_key_text(block_text: str, key: str) -> str:
    named_block = extract_assignment_block(block_text, key)
    if not named_block:
        return ""
    direct = re.search(r'\bkey\s*=\s*"([^"]+)"', named_block)
    if direct and not direct.group(1).startswith("%"):
        return direct.group(1)
    variable_values = re.findall(r'value\s*=\s*\{\s*key\s*=\s*"([^"]+)"', named_block)
    return " ".join(variable_values)


def count_numeric_list_assignment(block_text: str, key: str) -> int | None:
    list_block = extract_assignment_block(block_text, key)
    if not list_block:
        return None
    return len(re.findall(r"\b\d+\b", list_block))


def checkpoint_country_row(
    *,
    run_id: str,
    checkpoint_year: int,
    date: str,
    rank: int,
    country_id: str,
    country_block: str,
    evidence_file: str,
) -> dict[str, str]:
    budget_block = extract_assignment_block(country_block, "budget")
    current_month_block = extract_assignment_block(budget_block, "current_month")
    income = sum_resource_assignments(extract_assignment_block(current_month_block, "income"))
    deficits = ",".join(f"{name}:{value:g}" for name, value in income.items() if value < 0)
    research = sum(income.get(resource, 0.0) for resource in RESEARCH_RESOURCES)
    row = {field: "" for field in CHECKPOINT_FIELDS}
    row.update(
        {
            "run_id": run_id,
            "checkpoint_year": str(checkpoint_year),
            "date": date,
            "empire_rank": str(rank),
            "empire_name": localized_key_text(country_block, "name") or f"country_{country_id}",
            "country_id": country_id,
            "economy_power": metric_text(numeric_assignment(country_block, "economy_power")),
            "tech_power": metric_text(numeric_assignment(country_block, "tech_power")),
            "fleet_power": metric_text(numeric_assignment(country_block, "fleet_size")),
            "naval_capacity_used": metric_text(numeric_assignment(country_block, "used_naval_capacity")),
            "naval_capacity_available": metric_text(numeric_assignment(country_block, "naval_capacity")),
            "research": metric_text(research),
            "pops": metric_text(numeric_assignment(country_block, "num_sapient_pops")),
            "colonies": metric_text(
                count_numeric_list_assignment(country_block, "controlled_colonies")
                or count_numeric_list_assignment(country_block, "owned_planets")
            ),
            "megastructures": metric_text(count_numeric_list_assignment(country_block, "owned_megastructures")),
            "deficits": deficits,
            "notes": f"save country type {country_type(country_block)}; regular AI benchmark excludes fallen/special countries",
            "evidence_file": evidence_file,
        }
    )
    for field, resource in CHECKPOINT_RESOURCE_FIELDS.items():
        row[field] = metric_text(income.get(resource))
    return row


def metric_text(value: float | None) -> str:
    if value is None:
        return ""
    rounded = round(value, 3)
    if rounded == int(rounded):
        return str(int(rounded))
    return f"{rounded:.3f}".rstrip("0").rstrip(".")


def extract_checkpoint_rows_from_save(
    save_path: Path,
    *,
    run_id: str,
    checkpoint_year: int,
    max_rows: int = 12,
    evidence_file: str = "",
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    gamestate = load_stellaris_save_gamestate(save_path)
    date = save_scalar(gamestate, "date")
    countries = dict(iter_numbered_child_blocks(extract_assignment_block(gamestate, "country")))
    eligible: list[tuple[float, str, str]] = []
    special: list[dict[str, Any]] = []
    type_counts: Counter[str] = Counter()
    for country_id, block in countries.items():
        current_type = country_type(block)
        type_counts[current_type or "missing"] += 1
        economy_power = numeric_assignment(block, "economy_power") or 0.0
        pops = numeric_assignment(block, "num_sapient_pops") or 0.0
        fleet_power = numeric_assignment(block, "fleet_size") or 0.0
        type_ten_regularized = current_type == "10" and 0 < economy_power < FALLEN_OR_SPECIAL_ECONOMY_POWER_FLOOR
        if (current_type in REGULAR_AI_COUNTRY_TYPES or type_ten_regularized) and pops > 0 and economy_power > 0:
            eligible.append((economy_power, country_id, block))
        elif economy_power > 100 or fleet_power > 1000:
            special.append(
                {
                    "country_id": country_id,
                    "type": current_type,
                    "name": localized_key_text(block, "name"),
                    "economy_power": metric_text(economy_power),
                    "fleet_power": metric_text(fleet_power),
                    "pops": metric_text(pops),
                }
            )
    eligible.sort(key=lambda item: item[0], reverse=True)
    rows = [
        checkpoint_country_row(
            run_id=run_id,
            checkpoint_year=checkpoint_year,
            date=date,
            rank=index,
            country_id=country_id,
            country_block=block,
            evidence_file=evidence_file or str(save_path),
        )
        for index, (_, country_id, block) in enumerate(eligible[:max_rows], start=1)
    ]
    summary = {
        "run_id": run_id,
        "checkpoint_year": checkpoint_year,
        "date": date,
        "save_path": str(save_path),
        "country_count": len(countries),
        "eligible_regular_country_count": len(eligible),
        "country_type_counts": dict(sorted(type_counts.items())),
        "excluded_special_or_outlier_countries": sorted(
            special,
            key=lambda row: float(row.get("economy_power") or 0),
            reverse=True,
        ),
        "rows": rows,
    }
    return rows, summary


def append_checkpoint_rows(run_dir: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with (run_dir / "checkpoints.csv").open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHECKPOINT_FIELDS)
        writer.writerows(rows)


def checkpoint_save_report_text(summary: dict[str, Any]) -> str:
    lines = [
        f"# Checkpoint {summary['checkpoint_year']} Save Benchmark",
        "",
        f"- Run: {summary['run_id']}",
        f"- Date: {summary['date']}",
        f"- Save: `{summary['save_path']}`",
        f"- Countries: {summary['country_count']}",
        f"- Eligible regular AI countries: {summary['eligible_regular_country_count']}",
        f"- Country types: {json.dumps(summary['country_type_counts'], sort_keys=True)}",
        "",
        "## Ranked Regular AI Countries",
        "",
        "| rank | country | id | economy | tech | fleet | naval used | research | alloys | CG | energy | minerals | food | pops | deficits |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summary["rows"]:
        lines.append(
            f"| {row['empire_rank']} | {row['empire_name']} | {row['country_id']} | "
            f"{row['economy_power']} | {row['tech_power']} | {row['fleet_power']} | "
            f"{row['naval_capacity_used']} | {row['research']} | {row['alloys_income']} | "
            f"{row['consumer_goods_income']} | {row['energy_income']} | {row['minerals_income']} | "
            f"{row['food_income']} | {row['pops']} | {row['deficits']} |"
        )
    lines.extend(["", "## Excluded Special Or Outlier Countries", ""])
    for row in summary["excluded_special_or_outlier_countries"][:12]:
        lines.append(
            f"- {row['country_id']} `{row['name'] or 'unknown'}` type {row['type']}: "
            f"economy {row['economy_power']}, fleet {row['fleet_power']}, pops {row['pops']}"
        )
    lines.append("")
    return "\n".join(lines)


def summarize_observer_run(run_dir: Path, write_files: bool = True) -> dict[str, Any]:
    metadata_path = run_dir / "metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing metadata.json in {run_dir}")

    metadata = read_json(metadata_path)
    rows = checkpoint_rows(run_dir)
    years = Counter(row.get("checkpoint_year", "").strip() or "unknown" for row in rows)
    ranks = Counter(row.get("empire_rank", "").strip() or "unknown" for row in rows)
    evidence_counts = {
        name: len(list((run_dir / name).glob("*")))
        for name in ("logs", "saves", "screenshots", "exports")
        if (run_dir / name).exists()
    }
    notes_path = run_dir / "manual-notes.md"
    notes_text = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
    summary = {
        "run_id": metadata["run_id"],
        "status": metadata.get("status", "unknown"),
        "target_game_version": metadata.get("target_game_version", ""),
        "hidden_economic_bonuses": metadata.get("hidden_economic_bonuses"),
        "checkpoint_row_count": len(rows),
        "checkpoint_year_counts": dict(sorted(years.items())),
        "empire_rank_counts": dict(sorted(ranks.items())),
        "evidence_file_counts": evidence_counts,
        "manual_notes_bytes": len(notes_text.encode("utf-8")),
        "has_patch_hypothesis_table": "| hypothesis | evidence | expected effect | patch status | result |" in notes_text,
        "summary_generated_at_utc": utc_now().isoformat(),
    }
    if write_files:
        write_json(run_dir / "summary.json", summary)
        write_text(run_dir / "summary.md", summary_markdown(summary))
    return summary


def summary_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# Observer Run Summary: {summary['run_id']}",
        "",
        f"- Status: {summary['status']}",
        f"- Target game version: {summary['target_game_version']}",
        f"- Hidden economic bonuses: {summary['hidden_economic_bonuses']}",
        f"- Checkpoint rows: {summary['checkpoint_row_count']}",
        f"- Checkpoint years: {json.dumps(summary['checkpoint_year_counts'], sort_keys=True)}",
        f"- Empire ranks: {json.dumps(summary['empire_rank_counts'], sort_keys=True)}",
        f"- Evidence files: {json.dumps(summary['evidence_file_counts'], sort_keys=True)}",
        f"- Manual notes bytes: {summary['manual_notes_bytes']}",
        f"- Patch hypothesis table present: {summary['has_patch_hypothesis_table']}",
        f"- Summary generated UTC: {summary['summary_generated_at_utc']}",
        "",
    ]
    return "\n".join(lines)
