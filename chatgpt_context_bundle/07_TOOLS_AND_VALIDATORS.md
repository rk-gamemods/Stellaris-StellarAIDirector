> Snapshot commit: `27aa7547b610e2876d897771a804656453f948ee` | Branch: `master` | Working tree: `dirty` | Generated: `2026-07-08T15:18:04-04:00`

# Tools And Validators

Scripts are deterministic local helpers for inventories, audits, generated patches, launcher descriptor installation, observer-run harnesses, log summaries, and tests. Prefer these over hand-recreating repeatable checks.

## tools/README.md

```markdown
# Tools

Use this folder for repeatable helper scripts, validators, packaging commands, or analysis utilities for Stellaris modding.

Prefer small, documented tools with clear inputs and outputs.

## Local Validation Surfaces

- Irony Mod Manager is the project-local tool for playset dependency, conflict, and load-order investigation.
- CWTools diagnostics should be used for PDXScript syntax/schema feedback when editing gameplay scripts.
- `python tools/build_stellar_ai_director_object_atlas.py` regenerates the Stellar AI Director object atlas, dependency edges, parent-AI support map, policy matrix, coverage report, and route report.
- Runtime validation should inspect `error.log` first, then `game.log`.
- Use generated script docs, current vanilla files, and source references before trusting an unfamiliar trigger, effect, modifier, scope, or folder path.

Reusable templates and matrices from the attached research bundle are under `research/stellaris-modding-research-bundle-2026-07-04/`.
```

## tools/add_stellar_ai_director_to_irony_collection.py

```python
#!/usr/bin/env python3
"""Append Stellar AI Director to the selected Irony collection without reordering existing mods."""

from stellar_ai_director_lib import append_director_to_selected_irony_collection


def main() -> None:
    result = append_director_to_selected_irony_collection()
    print(result)


if __name__ == "__main__":
    main()
```

## tools/build_active_playset_snapshot.py

```python
#!/usr/bin/env python3
"""Write the selected Irony collection snapshot for Stellar AI Director."""

from stellar_ai_director_lib import RESEARCH_ROOT, build_active_playset_snapshot, write_json


def main() -> None:
    write_json(RESEARCH_ROOT / "stellar-ai-director-active-playset-2026-07-04.json", build_active_playset_snapshot())


if __name__ == "__main__":
    main()

```

## tools/build_ai_roi_matrix.py

```python
#!/usr/bin/env python3
"""Generate the Stellar AI Director megastructure ROI matrix."""

from stellar_ai_director_lib import generate_roi_artifacts


def main() -> None:
    generate_roi_artifacts()


if __name__ == "__main__":
    main()

```

## tools/build_mod_snapshot_inventory.py

```python
#!/usr/bin/env python3
"""Build inventories for copied Stellaris Workshop source snapshots.

The input snapshot root is expected to contain one folder per copied mod plus a
snapshot-manifest.csv written by the copy step. The script emits deterministic
CSV maps that make large PDXScript mods searchable and comparable without
requiring a full PDX parser.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


TEXT_SUFFIXES = {
    ".asset",
    ".csv",
    ".gui",
    ".gfx",
    ".info",
    ".json",
    ".lua",
    ".mod",
    ".txt",
    ".yml",
    ".yaml",
}

AI_MARKERS = [
    "ai_weight",
    "ai_weight_coefficient",
    "ai_resource_production",
    "ai_priority",
    "ai_budget",
    "economic_plan",
    "desired_max",
    "focus",
    "potential",
    "scripted_trigger",
    "scripted_value",
    "on_action",
    "country_event",
    "planet_event",
    "megastructure",
    "technology",
    "strategic_resource",
    "ship_size",
    "component",
    "starbase",
    "personality",
]

TOP_OBJECT_RE = re.compile(r"^([A-Za-z0-9_.~!@:+-]+)\s*=\s*\{")
ASSIGNMENT_RE = re.compile(r"^\s*([A-Za-z0-9_.~!@:+-]+)\s*=\s*")
DESCRIPTOR_RE = re.compile(r'^(name|version|supported_version|remote_file_id)="([^"]*)"')


def read_manifest(snapshot_root: Path) -> list[dict[str, str]]:
    manifest_path = snapshot_root / "snapshot-manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return ""  # pragma: no cover - latin-1 fallback decodes arbitrary bytes.


def parse_descriptor(mod_path: Path) -> dict[str, str]:
    descriptor = mod_path / "descriptor.mod"
    result = {"name": "", "version": "", "supported_version": "", "remote_file_id": ""}
    if not descriptor.exists():
        return result
    for line in read_text(descriptor).splitlines():
        match = DESCRIPTOR_RE.match(line.strip())
        if match:
            result[match.group(1)] = match.group(2)
    return result


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build(snapshot_root: Path) -> None:
    manifest = read_manifest(snapshot_root)
    file_rows: list[dict[str, object]] = []
    object_rows: list[dict[str, object]] = []
    ai_rows: list[dict[str, object]] = []
    descriptor_rows: list[dict[str, object]] = []
    folder_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    marker_totals: dict[str, Counter[str]] = defaultdict(Counter)

    for mod in manifest:
        mod_id = mod["id"]
        slug = mod["slug"]
        mod_path = snapshot_root / f"{mod_id}-{slug}"
        descriptor = parse_descriptor(mod_path)
        descriptor_rows.append(
            {
                "mod_id": mod_id,
                "slug": slug,
                "name": descriptor["name"] or mod.get("name", ""),
                "version": descriptor["version"] or mod.get("version", ""),
                "supported_version": descriptor["supported_version"] or mod.get("supported_version", ""),
                "remote_file_id": descriptor["remote_file_id"] or mod_id,
                "snapshot_path": str(mod_path),
            }
        )

        for file_path in sorted(path for path in mod_path.rglob("*") if path.is_file()):
            rel = file_path.relative_to(mod_path).as_posix()
            parts = rel.split("/")
            top_dir = parts[0] if len(parts) > 1 else ""
            second_dir = parts[1] if len(parts) > 2 else ""
            suffix = file_path.suffix.lower()
            size = file_path.stat().st_size
            text = is_text_file(file_path)
            file_rows.append(
                {
                    "mod_id": mod_id,
                    "slug": slug,
                    "relative_path": rel,
                    "top_dir": top_dir,
                    "second_dir": second_dir,
                    "suffix": suffix,
                    "bytes": size,
                    "is_text": text,
                }
            )
            folder_counts[(mod_id, slug)][top_dir or "(root)"] += 1
            if not text:
                continue

            content = read_text(file_path)
            lower = content.lower()
            marker_counts = {marker: lower.count(marker.lower()) for marker in AI_MARKERS}
            if any(marker_counts.values()):
                row: dict[str, object] = {
                    "mod_id": mod_id,
                    "slug": slug,
                    "relative_path": rel,
                    "top_dir": top_dir,
                    "second_dir": second_dir,
                }
                row.update(marker_counts)
                ai_rows.append(row)
                for marker, count in marker_counts.items():
                    marker_totals[mod_id][marker] += count

            for line_number, line in enumerate(content.splitlines(), start=1):
                match = TOP_OBJECT_RE.match(line)
                if not match:
                    continue
                object_name = match.group(1)
                assignment = ASSIGNMENT_RE.match(line)
                object_rows.append(
                    {
                        "mod_id": mod_id,
                        "slug": slug,
                        "relative_path": rel,
                        "line": line_number,
                        "top_dir": top_dir,
                        "second_dir": second_dir,
                        "object_name": object_name,
                        "assignment_key": assignment.group(1) if assignment else object_name,
                    }
                )

    folder_rows: list[dict[str, object]] = []
    for (mod_id, slug), counts in sorted(folder_counts.items()):
        for folder, count in sorted(counts.items()):
            folder_rows.append({"mod_id": mod_id, "slug": slug, "folder": folder, "file_count": count})

    marker_rows: list[dict[str, object]] = []
    for mod_id, counts in sorted(marker_totals.items()):
        slug = next((row["slug"] for row in manifest if row["id"] == mod_id), "")
        row: dict[str, object] = {"mod_id": mod_id, "slug": slug}
        row.update({marker: counts[marker] for marker in AI_MARKERS})
        marker_rows.append(row)

    write_csv(
        snapshot_root / "descriptor-inventory.csv",
        descriptor_rows,
        ["mod_id", "slug", "name", "version", "supported_version", "remote_file_id", "snapshot_path"],
    )
    write_csv(
        snapshot_root / "file-inventory.csv",
        file_rows,
        ["mod_id", "slug", "relative_path", "top_dir", "second_dir", "suffix", "bytes", "is_text"],
    )
    write_csv(
        snapshot_root / "top-level-folder-summary.csv",
        folder_rows,
        ["mod_id", "slug", "folder", "file_count"],
    )
    write_csv(
        snapshot_root / "pdx-object-inventory.csv",
        object_rows,
        ["mod_id", "slug", "relative_path", "line", "top_dir", "second_dir", "object_name", "assignment_key"],
    )
    write_csv(
        snapshot_root / "ai-surface-inventory.csv",
        ai_rows,
        ["mod_id", "slug", "relative_path", "top_dir", "second_dir", *AI_MARKERS],
    )
    write_csv(
        snapshot_root / "ai-marker-summary.csv",
        marker_rows,
        ["mod_id", "slug", *AI_MARKERS],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory copied Stellaris mod source snapshots.")
    parser.add_argument("snapshot_root", type=Path, help="Dated snapshot root containing snapshot-manifest.csv")
    args = parser.parse_args()
    build(args.snapshot_root.resolve())


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_dependency_audit.py

```python
#!/usr/bin/env python3
"""Build the Stellar AI Director descriptor/playset dependency audit report."""

from stellar_ai_director_lib import generate_dependency_audit_artifacts


def main() -> None:
    generate_dependency_audit_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_file_audit.py

```python
#!/usr/bin/env python3
"""Build the Stellar AI Director generated-file surface audit report."""

from stellar_ai_director_lib import generate_file_audit_artifacts


def main() -> None:
    generate_file_audit_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_integration_policy_audit.py

```python
#!/usr/bin/env python3
"""Build the Stellar AI Director integration policy readiness audit."""

from stellar_ai_director_lib import generate_integration_policy_audit_artifacts


def main() -> None:
    generate_integration_policy_audit_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_irony_order_proof.py

```python
#!/usr/bin/env python3
"""Generate stable evidence that the selected Irony order only added Stellar AI Director."""

from stellar_ai_director_lib import generate_irony_order_proof_artifacts


def main() -> None:
    generate_irony_order_proof_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_launch_comparison.py

```python
#!/usr/bin/env python3
"""Build the Stellar AI Director baseline-vs-Director launch comparison report."""

from stellar_ai_director_lib import generate_launch_comparison_artifacts


def main() -> None:
    generate_launch_comparison_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_object_atlas.py

```python
#!/usr/bin/env python3
"""Generate the Stellar AI Director object atlas and derived knowledge reports."""

from stellar_ai_director_lib import generate_object_atlas_artifacts, validate_object_atlas_artifacts


def main() -> None:
    generate_object_atlas_artifacts()
    errors = validate_object_atlas_artifacts()
    if errors:
        raise SystemExit("Object atlas validation failed:\n" + "\n".join(errors))
    print("Stellar AI Director object atlas generated.")


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_observer_save_summary.py

```python
#!/usr/bin/env python3
"""Build the Stellar AI Director observer smoke save summary artifacts."""

from stellar_ai_director_lib import generate_observer_save_summary_artifacts


def main() -> None:
    generate_observer_save_summary_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_plan_status.py

```python
#!/usr/bin/env python3
"""Build the Stellar AI Director P0-P16 plan completion status report."""

from stellar_ai_director_lib import generate_plan_status_artifacts


def main() -> None:
    generate_plan_status_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_reference_audit.py

```python
#!/usr/bin/env python3
"""Build the Stellar AI Director generated-reference audit report."""

from stellar_ai_director_lib import generate_reference_audit_artifacts


def main() -> None:
    generate_reference_audit_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_director_roi_quality_audit.py

```python
#!/usr/bin/env python3
"""Build the Stellar AI Director ROI quality audit report."""

from stellar_ai_director_lib import generate_roi_quality_audit_artifacts


def main() -> None:
    generate_roi_quality_audit_artifacts()


if __name__ == "__main__":
    main()
```

## tools/build_stellar_ai_economic_valuation_dataset.py

```python
#!/usr/bin/env python3
"""Build the active-stack building/zone/district economic valuation dataset."""

from stellar_ai_director_lib import generate_economic_valuation_dataset


def main() -> None:
    rows = generate_economic_valuation_dataset()
    print(f"generated {len(rows)} economic valuation rows")


if __name__ == "__main__":
    main()
```

## tools/disable_stellar_ai_director_in_dlc_load.py

```python
#!/usr/bin/env python3
"""Disable the local Stellar AI Director descriptor in Stellaris dlc_load.json."""

from stellar_ai_director_lib import disable_director_in_dlc_load


def main() -> None:
    print(disable_director_in_dlc_load())


if __name__ == "__main__":
    main()
```

## tools/enable_stellar_ai_director_in_dlc_load.py

```python
#!/usr/bin/env python3
"""Enable the local Stellar AI Director descriptor in Stellaris dlc_load.json."""

from stellar_ai_director_lib import enable_director_in_dlc_load


def main() -> None:
    print(enable_director_in_dlc_load())


if __name__ == "__main__":
    main()
```

## tools/extract_stellar_ai_checkpoint.py

```python
#!/usr/bin/env python3
"""Extract Stellar AI observer checkpoint rows from a Stellaris save."""

from __future__ import annotations

import argparse
from pathlib import Path

from stellar_ai_observer_loop import (
    append_checkpoint_rows,
    checkpoint_save_report_text,
    extract_checkpoint_rows_from_save,
    latest_observer_run,
    write_json,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", required=True, type=Path, help="Checkpoint .sav file to parse.")
    parser.add_argument("--run-dir", type=Path, help="Observer run directory. Defaults to latest run.")
    parser.add_argument("--checkpoint-year", required=True, type=int, help="Checkpoint year, such as 2250.")
    parser.add_argument("--max-rows", type=int, default=12, help="Maximum ranked regular AI rows to emit.")
    parser.add_argument("--append", action="store_true", help="Append rows to checkpoints.csv.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir or latest_observer_run()
    run_id = run_dir.name
    evidence_file = str(args.save.relative_to(run_dir)) if args.save.is_relative_to(run_dir) else str(args.save)
    rows, summary = extract_checkpoint_rows_from_save(
        args.save,
        run_id=run_id,
        checkpoint_year=args.checkpoint_year,
        max_rows=args.max_rows,
        evidence_file=evidence_file,
    )
    export_base = run_dir / "exports" / f"checkpoint-{args.checkpoint_year}-benchmark"
    write_json(export_base.with_suffix(".json"), summary)
    write_text(export_base.with_suffix(".md"), checkpoint_save_report_text(summary))
    if args.append:
        append_checkpoint_rows(run_dir, rows)
    print(
        f"checkpoint={args.checkpoint_year} date={summary['date']} "
        f"eligible_regular_countries={summary['eligible_regular_country_count']} rows={len(rows)} "
        f"appended={args.append}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tools/generate_stellar_ai_director_patch.py

```python
#!/usr/bin/env python3
"""Generate Stellar AI Director mod files and research artifacts."""

from stellar_ai_director_lib import run_all


def main() -> None:
    run_all()


if __name__ == "__main__":
    main()

```

## tools/install_stellar_ai_director_launcher_descriptor.py

```python
#!/usr/bin/env python3
"""Install the local Stellar AI Director descriptor for the Paradox launcher."""

from stellar_ai_director_lib import install_launcher_descriptor


def main() -> None:
    print(install_launcher_descriptor())


if __name__ == "__main__":
    main()
```

## tools/manage_stellaris_commands_at_date.py

```python
#!/usr/bin/env python3
"""Manage the live Stellaris commands_at_date observer-control file."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DEFAULT_STELLARIS_USER_DIR = Path.home() / "Documents" / "Paradox Interactive" / "Stellaris"
DEFAULT_COMMANDS_PATH = DEFAULT_STELLARIS_USER_DIR / "commands_at_date.txt"

OBSERVER_COMMAND_SCHEDULE = """# Observer-loop console command schedule for a manually approved AI benchmark run.
# This file must not remain installed after the observer run ends.
# Use `python tools/manage_stellaris_commands_at_date.py disable` to remove it.
# `game_speed 5` is intentional: in Stellaris 4.4.x it unlocks the dev-only
# higher simulation speed displayed by the UI as GAME_SPEED_6.
2200.01.01 = "help human_ai"
2200.01.01 = "help observe"
2200.01.01 = "human_ai"
2200.01.01 = "observe"
2200.01.01 = "help game_speed"
2200.01.01 = "game_speed 5"
2200.01.02 = "help human_ai"
2200.01.02 = "help observe"
2200.01.02 = "human_ai"
2200.01.02 = "observe"
2200.01.02 = "help game_speed"
2200.01.02 = "game_speed 5"
2250.01.01 = "game_paused"
2300.01.01 = "game_paused"
2325.01.01 = "game_paused"
2350.01.01 = "game_paused"
"""

OBSERVER_MARKERS = (
    "Observer-loop console command schedule",
    "human_ai",
    "observe",
    "game_paused",
)


@dataclass(frozen=True)
class CommandsStatus:
    path: Path
    exists: bool
    managed_observer_schedule: bool
    contains_game_pause: bool
    contains_observer_commands: bool
    size_bytes: int

    def as_dict(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "exists": self.exists,
            "managed_observer_schedule": self.managed_observer_schedule,
            "contains_game_pause": self.contains_game_pause,
            "contains_observer_commands": self.contains_observer_commands,
            "size_bytes": self.size_bytes,
        }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def commands_status(path: Path = DEFAULT_COMMANDS_PATH) -> CommandsStatus:
    text = read_text(path)
    return CommandsStatus(
        path=path,
        exists=path.exists(),
        managed_observer_schedule=all(marker in text for marker in OBSERVER_MARKERS),
        contains_game_pause="game_paused" in text,
        contains_observer_commands=any(command in text for command in ("human_ai", "observe", "ticks_per_turn")),
        size_bytes=path.stat().st_size if path.exists() else 0,
    )


def enable_observer_schedule(path: Path = DEFAULT_COMMANDS_PATH, *, force: bool = False) -> Path:
    if path.exists() and not force:
        status = commands_status(path)
        raise FileExistsError(
            f"{path} already exists; status={status.as_dict()}. "
            "Disable or archive it first, or pass --force intentionally."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(OBSERVER_COMMAND_SCHEDULE, encoding="utf-8", newline="\n")
    return path


def disable_commands(path: Path = DEFAULT_COMMANDS_PATH, *, archive: bool = True) -> Path | None:
    if not path.exists():
        return None
    if not archive:
        path.unlink()
        return path
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = path.with_name(f"commands_at_date.disabled-by-codex-{stamp}.txt")
    suffix = 1
    while target.exists():
        target = path.with_name(f"commands_at_date.disabled-by-codex-{stamp}-{suffix}.txt")
        suffix += 1
    path.rename(target)
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("status", "enable", "disable"))
    parser.add_argument("--path", type=Path, default=DEFAULT_COMMANDS_PATH, help="Live commands_at_date.txt path.")
    parser.add_argument("--force", action="store_true", help="Allow enable to overwrite an existing command file.")
    parser.add_argument("--delete", action="store_true", help="Delete on disable instead of archiving by rename.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.action == "status":
        payload = commands_status(args.path).as_dict()
    elif args.action == "enable":
        enabled_path = enable_observer_schedule(args.path, force=args.force)
        payload = {"action": "enabled", "path": str(enabled_path), **commands_status(enabled_path).as_dict()}
    else:
        disabled_path = disable_commands(args.path, archive=not args.delete)
        payload = {
            "action": "disabled" if disabled_path is not None else "already_absent",
            "path": str(args.path),
            "disabled_path": str(disabled_path) if disabled_path is not None else None,
            **commands_status(args.path).as_dict(),
        }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tools/new_stellar_ai_observer_run.py

```python
#!/usr/bin/env python3
"""Create a standard Stellar AI Director observer-run folder."""

from stellar_ai_observer_loop import create_observer_run


def main() -> None:
    run_dir = create_observer_run()
    print(run_dir)


if __name__ == "__main__":
    main()
```

## tools/record_stellar_ai_director_main_menu_proof.py

```python
#!/usr/bin/env python3
"""Record a manual main-menu proof marker for the current Stellaris playset mode."""

from stellar_ai_director_lib import MAIN_MENU_PROOF_PATH, record_main_menu_proof_marker


def main() -> None:
    status = record_main_menu_proof_marker()
    print(f"{MAIN_MENU_PROOF_PATH}: main_menu_proven={status['main_menu_proven']}")


if __name__ == "__main__":
    main()
```

## tools/stellar_ai_director_lib.py

_Omitted inline because this file is 525531 bytes. See the source manifest and use the local repo or JDataMunch/JDocMunch/JCodeMunch for exact retrieval._

## tools/stellar_ai_observer_loop.py

```python
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
```

## tools/summarize_stellar_ai_observer_run.py

```python
#!/usr/bin/env python3
"""Summarize the latest Stellar AI Director observer-run folder."""

from stellar_ai_observer_loop import latest_observer_run, summarize_observer_run


def main() -> None:
    run_dir = latest_observer_run()
    summarize_observer_run(run_dir)
    print(run_dir)


if __name__ == "__main__":
    main()
```

## tools/summarize_stellaris_log.py

```python
#!/usr/bin/env python3
"""Group large Stellaris logs into compact, expandable summaries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


DEFAULT_LOG_ROOT = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs")
ENTRY_RE = re.compile(r"^\[(?P<time>\d\d:\d\d:\d\d)\]\[(?P<source>[^\]]+)\]:\s?(?P<message>.*)$")
VOLATILE_PATTERNS = (
    (re.compile(r"\bmod/ugc_\d+\.mod\b", re.IGNORECASE), "mod/ugc_<id>.mod"),
    (re.compile(r"\bugc_\d+\b", re.IGNORECASE), "ugc_<id>"),
    (re.compile(r"\bline:\s*\d+\b", re.IGNORECASE), "line: <n>"),
    (re.compile(r"\b(line|column)\s+\d+\b", re.IGNORECASE), r"\1 <n>"),
    (re.compile(r"\b0x[0-9a-f]+\b", re.IGNORECASE), "0x<hex>"),
    (re.compile(r"\b\d{2,}\b"), "<n>"),
    (re.compile(r"[A-Z]:\\[^:\n]+", re.IGNORECASE), "<path>"),
)


@dataclass
class LogEntry:
    path: Path
    start_line: int
    end_line: int
    time: str
    source: str
    lines: list[str]


@dataclass
class LogGroup:
    signature: str
    source: str
    severity: str
    count: int = 0
    first_path: str = ""
    first_line: int = 0
    first_time: str = ""
    last_path: str = ""
    last_line: int = 0
    last_time: str = ""
    samples: list[dict[str, object]] = field(default_factory=list)

    def add(self, entry: LogEntry, sample_limit: int) -> None:
        self.count += 1
        if self.count == 1:
            self.first_path = str(entry.path)
            self.first_line = entry.start_line
            self.first_time = entry.time
        self.last_path = str(entry.path)
        self.last_line = entry.start_line
        self.last_time = entry.time
        if len(self.samples) < sample_limit:
            self.samples.append(
                {
                    "path": str(entry.path),
                    "start_line": entry.start_line,
                    "end_line": entry.end_line,
                    "time": entry.time,
                    "text": "\n".join(entry.lines),
                }
            )


def iter_entries(path: Path) -> Iterable[LogEntry]:
    current_lines: list[str] = []
    current_time = ""
    current_source = ""
    current_start = 0
    last_line_no = 0
    with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        for line_no, raw_line in enumerate(handle, 1):
            last_line_no = line_no
            line = raw_line.rstrip("\n")
            match = ENTRY_RE.match(line)
            if match:
                if current_lines:
                    yield LogEntry(path, current_start, line_no - 1, current_time, current_source, current_lines)
                current_start = line_no
                current_time = match.group("time")
                current_source = normalize_source(match.group("source"))
                current_lines = [match.group("message")]
            elif current_lines:
                current_lines.append(line)
            else:
                current_start = line_no
                current_time = ""
                current_source = "unframed"
                current_lines = [line]
    if current_lines:
        yield LogEntry(path, current_start, last_line_no, current_time, current_source, current_lines)


def normalize_source(source: str) -> str:
    return re.sub(r":\d+$", ":<line>", source.strip())


def normalize_text(text: str) -> str:
    normalized = text.strip()
    for pattern, replacement in VOLATILE_PATTERNS:
        normalized = pattern.sub(replacement, normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized[:500]


def entry_signature(entry: LogEntry) -> str:
    meaningful_lines = [line for line in entry.lines if line.strip()]
    if not meaningful_lines:
        meaningful_lines = [""]
    normalized_lines = [normalize_text(line) for line in meaningful_lines[:8]]
    return f"{entry.source}: " + " | ".join(normalized_lines)


def find_prefixed_line(lines: Iterable[str], prefix: str) -> str:
    prefix_lower = prefix.lower()
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith(prefix_lower):
            return normalize_text(stripped)
    return ""


def entry_family_signature(entry: LogEntry) -> str:
    meaningful_lines = [line for line in entry.lines if line.strip()]
    first = normalize_text(meaningful_lines[0] if meaningful_lines else "")
    wrong_scope = re.match(r"Wrong scope for trigger '([^']+)'", first, re.IGNORECASE)
    if wrong_scope:
        current_scope = find_prefixed_line(meaningful_lines, "Current scope:")
        supported_scopes = find_prefixed_line(meaningful_lines, "Supported Scopes:")
        return " | ".join(
            part
            for part in (
                f"{entry.source}: Wrong scope for trigger '{wrong_scope.group(1)}'",
                current_scope,
                supported_scopes,
            )
            if part
        )
    invalid_supported_version = re.match(r"Invalid supported_version\b", first, re.IGNORECASE)
    if invalid_supported_version:
        return f"{entry.source}: Invalid supported_version"
    script_error = re.match(r"Script Error:\s*(.*)", first, re.IGNORECASE)
    if script_error:
        error_line = find_prefixed_line(meaningful_lines, "Error:")
        scope_line = find_prefixed_line(meaningful_lines, "Current Scope:")
        return " | ".join(
            part
            for part in (
                f"{entry.source}: Script Error: {script_error.group(1)}",
                error_line,
                scope_line,
            )
            if part
        )
    missing = re.match(r"(Couldn't find|Could not find|Missing|Invalid|Failed)\b[^:]*", first, re.IGNORECASE)
    if missing:
        return f"{entry.source}: {missing.group(0)}"
    return f"{entry.source}: {first[:160]}"


def infer_severity(entry: LogEntry) -> str:
    text = "\n".join(entry.lines).lower()
    source = entry.source.lower()
    if "fatal" in text or "exception" in text or "crash" in text:
        return "fatal"
    if "error" in text or "failed" in text or "invalid" in text or "missing" in text or "wrong scope" in text:
        return "error"
    if "warning" in text or "warn" in source:
        return "warning"
    return "info"


def summarize_logs(paths: Iterable[Path], sample_limit: int = 2) -> dict[str, object]:
    groups: dict[str, LogGroup] = {}
    families: dict[str, LogGroup] = {}
    severity_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    total_entries = 0
    total_lines = 0
    files = []
    for path in paths:
        file_entry_count = 0
        file_line_count = 0
        for entry in iter_entries(path):
            total_entries += 1
            file_entry_count += 1
            entry_lines = max(1, entry.end_line - entry.start_line + 1)
            total_lines += entry_lines
            file_line_count += entry_lines
            signature = entry_signature(entry)
            family_signature = entry_family_signature(entry)
            severity = infer_severity(entry)
            severity_counts[severity] += 1
            source_counts[entry.source] += 1
            group = groups.get(signature)
            if group is None:
                group = LogGroup(signature=signature, source=entry.source, severity=severity)
                groups[signature] = group
            group.add(entry, sample_limit)
            family = families.get(family_signature)
            if family is None:
                family = LogGroup(signature=family_signature, source=entry.source, severity=severity)
                families[family_signature] = family
            family.add(entry, sample_limit)
        files.append(
            {
                "path": str(path),
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else 0,
                "entries": file_entry_count,
                "lines": file_line_count,
            }
        )
    sorted_groups = sorted(groups.values(), key=lambda group: (-group.count, group.severity, group.signature))
    sorted_families = sorted(families.values(), key=lambda group: (-group.count, group.severity, group.signature))
    return {
        "files": files,
        "total_entries": total_entries,
        "total_lines": total_lines,
        "group_count": len(sorted_groups),
        "family_count": len(sorted_families),
        "severity_counts": dict(sorted(severity_counts.items())),
        "source_counts": dict(source_counts.most_common()),
        "families": [group.__dict__ for group in sorted_families],
        "groups": [group.__dict__ for group in sorted_groups],
    }


def render_markdown(summary: dict[str, object], top: int) -> str:
    families = summary["families"][:top]  # type: ignore[index]
    groups = summary["groups"][:top]  # type: ignore[index]
    lines = [
        "# Stellaris Log Summary",
        "",
        f"Files: {len(summary['files'])}",
        f"Entries: {summary['total_entries']}",
        f"Raw entry lines: {summary['total_lines']}",
        f"Families: {summary['family_count']}",
        f"Groups: {summary['group_count']}",
        "",
        "## Severity Counts",
        "",
        "| severity | entries |",
        "| --- | ---: |",
    ]
    for severity, count in summary["severity_counts"].items():  # type: ignore[union-attr]
        lines.append(f"| {severity} | {count} |")
    lines.extend(["", "## Top Families", ""])
    for index, group in enumerate(families, 1):
        lines.extend(
            [
                f"### {index}. {group['count']}x `{group['source']}` [{group['severity']}]",
                "",
                f"Family: `{group['signature']}`",
                "",
                f"First: `{group['first_path']}:{group['first_line']}` at `{group['first_time']}`",
                f"Last: `{group['last_path']}:{group['last_line']}` at `{group['last_time']}`",
                "",
                "Samples:",
                "",
            ]
        )
        for sample in group["samples"]:
            lines.extend(
                [
                    f"- `{sample['path']}:{sample['start_line']}`-`{sample['end_line']}` at `{sample['time']}`",
                    "",
                    "```text",
                    str(sample["text"])[:2000],
                    "```",
                    "",
                ]
            )
    lines.extend(["", "## Top Exact Groups", ""])
    for index, group in enumerate(groups, 1):
        lines.extend(
            [
                f"### {index}. {group['count']}x `{group['source']}` [{group['severity']}]",
                "",
                f"Signature: `{group['signature']}`",
                "",
                f"First: `{group['first_path']}:{group['first_line']}` at `{group['first_time']}`",
                f"Last: `{group['last_path']}:{group['last_line']}` at `{group['last_time']}`",
                "",
                "Samples:",
                "",
            ]
        )
        for sample in group["samples"]:
            lines.extend(
                [
                    f"- `{sample['path']}:{sample['start_line']}`-`{sample['end_line']}` at `{sample['time']}`",
                    "",
                    "```text",
                    str(sample["text"])[:2000],
                    "```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def default_paths() -> list[Path]:
    return [DEFAULT_LOG_ROOT / "error.log", DEFAULT_LOG_ROOT / "game.log"]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="*", type=Path, help="Log files to summarize. Defaults to live error.log and game.log.")
    parser.add_argument("--format", choices=("md", "json"), default="md", help="Output format.")
    parser.add_argument("--top", type=int, default=25, help="Number of groups to include in Markdown output.")
    parser.add_argument("--samples", type=int, default=2, help="Sample entries retained per group.")
    parser.add_argument("--output", type=Path, help="Optional output file. Defaults to stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    paths = args.logs or default_paths()
    missing = [path for path in paths if not path.exists()]
    if missing:
        for path in missing:
            print(f"missing log file: {path}", file=sys.stderr)
        return 2
    summary = summarize_logs(paths, sample_limit=args.samples)
    if args.format == "json":
        output = json.dumps(summary, indent=2)
    else:
        output = render_markdown(summary, top=args.top)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tools/tests/test_stellar_ai_director.py

```python
import csv
import re
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stellar_ai_director_lib import (
    AI_SUPPORT_MAP_CSV,
    DEPENDENCY_EDGES_CSV,
    ECONOMIC_VALUATION_DATASET_CSV,
    ECONOMIC_VALUATION_DATASET_MD,
    ECONOMIC_VALUATION_EVIDENCE_MD,
    ECONOMIC_VALUATION_CANONICAL_COLUMNS,
    ECONOMIC_VALUATION_SOURCE_FACT_COLUMNS,
    EmpireState,
    GENERATED_VERSION_INVENTORY_MD,
    MANUAL_STATIC_VALIDATION_MD,
    MOD_ROOT,
    MOD_STACK_COMPATIBILITY_MD,
    OBJECT_ATLAS_CSV,
    POLICY_MATRIX_CSV,
    RESEARCH_ROOT,
    SNAPSHOT_ROOT,
    block_assignments,
    collect_generated_conflict_rows,
    collect_generated_file_audit_rows,
    collect_generated_reference_rows,
    collect_object_names,
    economic_valuation_evidence_passes,
    economic_valuation_dataset_passes,
    dataset_job_pressure_override_rows,
    dataset_ai_resource_production_amounts,
    extract_top_level_object_text,
    fresh_economic_valuation_source_facts,
    generated_unresolved_at_variable_rows,
    generate_economic_valuation_dataset,
    generate_mod_files,
    generate_object_atlas_artifacts,
    mod_source_root_for_id,
    NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV,
    NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_MD,
    nonconstruction_economic_valuation_dataset_passes,
    parse_file,
    parse_pdx,
    resource_waste_pressure,
    research_under_curve,
    surplus_sink_pressure,
    validate_staid_scripted_trigger_cycles,
    validate_generated_patch,
    validate_object_atlas_artifacts,
)


class ActiveStackEconomicValuationMaintenanceTests(unittest.TestCase):
    def test_generated_economic_values_match_current_active_mod_files(self):
        dataset_rows = []
        for path in (ECONOMIC_VALUATION_DATASET_CSV, NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV):
            with path.open("r", encoding="utf-8", newline="") as handle:
                dataset_rows.extend(list(csv.DictReader(handle)))

        fresh_facts = fresh_economic_valuation_source_facts(dataset_rows)
        drift_rows = []
        missing_rows = []
        for row in dataset_rows:
            object_key = (row["object_type"], row["object_id"])
            if row["object_type"] not in {
                "ascension_perk",
                "building",
                "colony_type",
                "decision",
                "deposit",
                "district",
                "edict",
                "policy",
                "pop_job",
                "resource",
                "starbase_building",
                "starbase_module",
                "technology",
                "tradition",
                "zone",
            }:
                continue
            actual = fresh_facts.get(object_key)
            if actual is None:
                missing_rows.append(f"{row['object_type']} `{row['object_id']}` expected at {row['winning_file']}")
                continue
            for column in ECONOMIC_VALUATION_SOURCE_FACT_COLUMNS:
                expected_value = str(row.get(column, ""))
                actual_value = str(actual.get(column, ""))
                if expected_value != actual_value:
                    drift_rows.append(
                        f"{row['object_type']} `{row['object_id']}` column `{column}` drifted: "
                        f"dataset={expected_value[:240]} current={actual_value[:240]} "
                        f"(dataset file {row['winning_file']}, current file {actual.get('winning_file', 'unknown')})"
                    )
                    break

        details = "\n".join([*missing_rows[:25], *drift_rows[:25]])
        overflow = len(missing_rows) + len(drift_rows) - 25
        if overflow > 0:
            details += f"\n... {overflow} more drift rows omitted"
        self.assertFalse(
            missing_rows or drift_rows,
            "Active mod economic source drift detected. Re-run the Stellar AI Director generator after reviewing the changed "
            "mod files; do not hand-edit the generated values.\n"
            + details,
        )


class GeneratedModValidityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        generate_object_atlas_artifacts(SNAPSHOT_ROOT)
        generate_mod_files()

    def test_generated_files_are_valid_load_surfaces(self):
        rows = collect_generated_file_audit_rows(MOD_ROOT)
        self.assertTrue(rows, "No generated mod files were found to validate.")
        bad_rows = [row for row in rows if row["status"] != "ok"]
        self.assertEqual(bad_rows, [])

    def test_generated_references_resolve_to_known_objects(self):
        rows = collect_generated_reference_rows(MOD_ROOT, SNAPSHOT_ROOT)
        self.assertTrue(rows, "No generated references were found to validate.")
        missing_rows = [row for row in rows if row["status"] == "missing"]
        self.assertEqual(missing_rows, [])

    def test_generated_ai_budget_overrides_known_budget_objects(self):
        known_budget_objects = collect_object_names(SNAPSHOT_ROOT)["ai_budget"]
        budget_root = MOD_ROOT / "common" / "ai_budget"
        budget_files = sorted(budget_root.glob("*.txt"))
        self.assertTrue(budget_files, "No generated AI budget files were found.")
        unknown = []
        for file_path in budget_files:
            parsed = parse_file(file_path)
            for assignment in block_assignments(parsed):
                if assignment.key not in known_budget_objects:
                    unknown.append((file_path.relative_to(MOD_ROOT).as_posix(), assignment.key))
        self.assertEqual(unknown, [])

    def test_generated_conflict_rows_ignore_source_local_variables(self):
        rows = collect_generated_conflict_rows(MOD_ROOT, SNAPSHOT_ROOT)
        variable_rows = [row for row in rows if row["object_name"].startswith("@")]
        self.assertEqual(variable_rows, [])

    def test_active_stack_economic_valuation_dataset_covers_buildings_zones_and_districts(self):
        rows = generate_economic_valuation_dataset()
        self.assertTrue(rows)
        self.assertTrue(ECONOMIC_VALUATION_DATASET_CSV.exists())
        self.assertTrue(ECONOMIC_VALUATION_DATASET_MD.exists())
        self.assertTrue(economic_valuation_dataset_passes())

        object_types = {row["object_type"] for row in rows}
        self.assertIn("building", object_types)
        self.assertIn("zone", object_types)
        self.assertIn("district", object_types)

        esc_buildings = [
            row
            for row in rows
            if row["object_type"] == "building" and row["winning_mod_id"] == "2648658105"
        ]
        gigas_objects = [
            row
            for row in rows
            if row["object_type"] in {"building", "district"} and row["winning_mod_id"] == "1121692237"
        ]
        self.assertTrue(esc_buildings, "ESC advanced buildings were not captured.")
        self.assertTrue(gigas_objects, "Gigas advanced buildings or districts were not captured.")
        self.assertTrue(any(float(row["jobs_created_total_estimate"]) > 0 for row in rows))
        self.assertTrue(any(float(row["roi_2250_to_2350_estimate"]) > 0 for row in rows))

    def test_nonconstruction_economic_valuation_dataset_extends_without_duplicate_construction_surfaces(self):
        self.assertTrue(NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.exists())
        self.assertTrue(NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_MD.exists())
        self.assertTrue(nonconstruction_economic_valuation_dataset_passes())
        self.assertTrue(economic_valuation_evidence_passes())
        self.assertTrue(ECONOMIC_VALUATION_EVIDENCE_MD.exists())

        with NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            self.assertEqual(set(reader.fieldnames or []), set(ECONOMIC_VALUATION_CANONICAL_COLUMNS))
        with ECONOMIC_VALUATION_DATASET_CSV.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            construction_rows = list(reader)
            self.assertEqual(set(reader.fieldnames or []), set(ECONOMIC_VALUATION_CANONICAL_COLUMNS))

        self.assertFalse(
            [
                (row["object_type"], row["object_id"], column)
                for row in [*construction_rows, *rows]
                for column in ECONOMIC_VALUATION_CANONICAL_COLUMNS
                if row.get(column, "") == ""
            ]
        )
        object_types = {row["object_type"] for row in rows}
        self.assertFalse({"building", "zone", "district", "megastructure"} & object_types)
        self.assertTrue(
            {
                "pop_job",
                "decision",
                "edict",
                "deposit",
                "resource",
                "starbase_building",
                "starbase_module",
                "technology",
                "colony_type",
                "policy",
                "ascension_perk",
                "tradition",
            }.issubset(object_types)
        )

        evidence_text = ECONOMIC_VALUATION_EVIDENCE_MD.read_text(encoding="utf-8")
        self.assertIn("Construction Dataset Counts", evidence_text)
        self.assertIn("Nonconstruction Dataset Counts", evidence_text)
        self.assertIn("resource", evidence_text)

    def test_dataset_job_pressure_overrides_use_live_valuation_rows(self):
        rows = dataset_job_pressure_override_rows()
        self.assertGreaterEqual(len(rows), 50)
        self.assertTrue(all(float(row["jobs_created_total_estimate"]) > 0 for row in rows))
        self.assertTrue(all(float(row["roi_2250_to_2350_estimate"]) > 0 for row in rows))
        self.assertIn("consumer_goods_repair", {row["pressure_family"] for row in rows})

        generated_files = [
            MOD_ROOT / "common" / "buildings" / "zzzz_staid_13_dataset_job_pressure_buildings.txt",
            MOD_ROOT / "common" / "districts" / "zzzz_staid_13_dataset_job_pressure_districts.txt",
        ]
        combined_text = ""
        for file_path in generated_files:
            self.assertTrue(file_path.exists(), f"{file_path} was not generated")
            text = file_path.read_text(encoding="utf-8")
            combined_text += text
            self.assertIn("staid_dataset_job_pressure", text)
            self.assertIn("num_unemployed > 0", text)
            self.assertIn("free_jobs < 1", text)
            self.assertIn("ai_weight_coefficient", text)
            parse_file(file_path)
        self.assertIn("family:consumer_goods_repair", combined_text)
        self.assertIn("staid_high_scale_snowball_pressure", combined_text)
        self.assertIn(
            "owner = { country_uses_consumer_goods = yes NOT = { staid_consumer_goods_runway_safe = yes } }",
            combined_text,
        )
        self.assertNotIn("factor = 0.35 owner = { staid_core_deficit_short_runway = yes }", combined_text)
        for invalid_marker in (
            "has_unemployed_pop_of_category",
            "job_acot_",
            "district_giga_frameworld_fortress_bunker",
            "district_generator_uncapped",
            "building_gas_extractors_max",
            "building_mote_harvesters_max",
            "building_crystal_mines_max",
        ):
            self.assertNotIn(invalid_marker, combined_text)
        district_text = generated_files[1].read_text(encoding="utf-8")
        self.assertNotIn("trade_value_add", district_text)

    def test_high_scale_ai_defines_remove_vanilla_construction_and_war_hesitation(self):
        defines_path = MOD_ROOT / "common" / "defines" / "zzzz_staid_14_high_scale_ai_defines.txt"
        self.assertTrue(defines_path.exists(), f"{defines_path} was not generated")
        parse_file(defines_path)
        text = defines_path.read_text(encoding="utf-8")
        for marker in (
            "AI_FREE_JOBS_BUILDING_BUILD_CAP = 5000",
            "AI_FOCUS_SCORE_MULT = 12",
            "AI_POPS_SCORE_MULT = 0.25",
            "AI_RESOURCE_TARGET_EXPIRATION_MONTHS = 6",
            "UNDERDEVELOPED_PLANET_LIMIT = 999",
            "BUILDING_BUILD_THRESHOLD = 0.1",
        ):
            self.assertIn(marker, text)
        for user_tuned_define in (
            "AI_AGGRESSIVENESS_BASE",
            "AI_WAR_PREPARATION_MIN_MONTHS",
            "WAR_DECLARATION_MAX_DISTANCE",
        ):
            self.assertRegex(text, rf"\b{user_tuned_define}\s*=")

    def test_minerals_planet_construction_budget_spends_harder_when_rich_or_crowded(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_minerals_planet_construction_budget.txt"
        self.assertTrue(budget_path.exists(), f"{budget_path} was not generated")
        parse_file(budget_path)
        text = budget_path.read_text(encoding="utf-8")
        for marker in (
            "minerals_expenditure_planets_low = {",
            "minerals_expenditure_planets_med = {",
            "minerals_expenditure_planets_high = {",
            "category = planets",
            "staid_high_scale_snowball_pressure",
            "staid_core_deficit_short_runway",
            "any_owned_planet = { num_unemployed > 0 free_jobs < 1 }",
            "weight = 28.0",
            "modifier = { factor = 40 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }",
            "modifier = { add = 300000 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }",
            "resource_stockpile_compare = { resource = minerals value > 25000 }",
        ):
            self.assertIn(marker, text)

    def test_mod_source_root_falls_back_to_live_workshop_when_snapshot_missing(self):
        root = mod_source_root_for_id("819148835")
        self.assertTrue(root.exists())
        self.assertIn("819148835", str(root))

    def test_pdx_parser_accepts_anonymous_nested_policy_blocks(self):
        parse_pdx(
            """
            orbital_bombardment = {
                option = {
                    name = "orbital_bombardment_indiscriminate"
                    in_breach_of = {
                        {
                            key = resolution_rulesofwar_independent_tribunals
                        }
                    }
                }
            }
            """
        )

    def test_static_validator_reports_no_invalid_references(self):
        self.assertEqual(validate_generated_patch(), [])

    def test_july7_computed_strategy_kernel_surfaces_are_generated(self):
        opening = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_10_opening_strategy_triggers.txt"
        kernel = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_20_strategy_kernel_triggers.txt"
        doctrine = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_11_fleet_doctrine_triggers.txt"
        for path in (opening, kernel, doctrine):
            self.assertTrue(path.exists(), f"Missing generated July 7 trigger surface: {path}")
            parse_file(path)

        opening_text = opening.read_text(encoding="utf-8")
        for marker in (
            "staid_opening_direct_research",
            "staid_opening_unity_to_research",
            "staid_opening_military_to_pops",
            "staid_opening_defensive_tall_research",
            "staid_opening_trade_to_research",
            "staid_opening_hive_growth_research",
            "staid_opening_machine_growth_research",
            "staid_opening_nomad_arkship_research",
        ):
            self.assertIn(marker, opening_text)

        kernel_text = kernel.read_text(encoding="utf-8")
        for marker in (
            "staid_is_opening_phase",
            "staid_is_midgame_scaling_phase",
            "staid_has_safe_basic_stockpiles",
            "staid_can_afford_research_push",
            "staid_security_threatened",
            "staid_security_existential",
            "staid_megastructure_prereq_release",
            "staid_fleet_strategic_aggression_mode",
        ):
            self.assertIn(marker, kernel_text)

        doctrine_text = doctrine.read_text(encoding="utf-8")
        for marker in (
            "staid_fleet_energy_shield_doctrine",
            "staid_fleet_kinetic_armor_doctrine",
            "staid_fleet_missile_evasion_doctrine",
            "staid_fleet_carrier_strikecraft_doctrine",
            "staid_fleet_balanced_filler_doctrine",
        ):
            self.assertIn(marker, doctrine_text)

    def test_july7_policy_and_edict_overrides_are_generated_from_verified_ids(self):
        policy = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        edicts = MOD_ROOT / "common" / "edicts" / "zzzz_staid_10_opening_growth_edicts.txt"
        for path in (policy, edicts):
            self.assertTrue(path.exists(), f"Missing generated July 7 policy/edict surface: {path}")
            parse_file(path)

        policy_text = policy.read_text(encoding="utf-8")
        self.assertIn("diplomatic_stance", policy_text)
        self.assertIn("diplo_stance_cooperative", policy_text)
        self.assertIn("staid_opening_route_research_priority", policy_text)
        self.assertIn("diplo_stance_cooperative_nomad", policy_text)

        edicts_text = edicts.read_text(encoding="utf-8")
        for marker in (
            "research_subsidies",
            "encourage_free_thought",
            "map_the_stars",
            "capacity_subsidies",
            "mining_subsidies",
            "farming_subsidies",
            "fortify_the_border",
            "staid_security_threatened",
        ):
            self.assertIn(marker, edicts_text)

    def test_planetary_diversity_outpost_decisions_are_director_weighted(self):
        decisions_path = MOD_ROOT / "common" / "decisions" / "zzzz_staid_12_planetary_diversity_outpost_decisions.txt"
        triggers_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        self.assertTrue(decisions_path.exists(), "Missing generated Planetary Diversity decision override file.")
        parse_file(decisions_path)

        decisions_text = decisions_path.read_text(encoding="utf-8")
        triggers_text = triggers_path.read_text(encoding="utf-8")
        economy_text = economy_path.read_text(encoding="utf-8")
        for decision_id in (
            "decision_build_pd_moon_base",
            "decision_build_pd_moon_base_moon_colony",
            "decision_build_pd_mining_base",
            "decision_build_pd_mining_base_2",
            "decision_build_pd_mining_base_3",
            "decision_build_pd_food_base",
            "decision_build_pd_food_base_2",
            "decision_build_pd_food_base_3",
            "decision_build_pd_energy_base",
            "decision_build_pd_energy_base_2",
            "decision_build_pd_energy_base_3",
            "decision_build_pd_research_base",
            "decision_build_pd_research_base_2",
            "decision_build_pd_research_base_3",
        ):
            self.assertIn(f"{decision_id} = {{", decisions_text)

        research_block = decisions_text[
            decisions_text.index("decision_build_pd_research_base = {") : decisions_text.index(
                "decision_build_pd_research_base_2 = {"
            )
        ]
        ai_weight = re.search(r"ai_weight\s*=\s*\{(?P<body>.*?)\n\t\}", research_block, re.S)
        self.assertIsNotNone(ai_weight)
        ai_weight_text = ai_weight.group("body")
        self.assertIn("Availability owns prerequisites", ai_weight_text)
        self.assertIn("Lifetime value formula", ai_weight_text)
        self.assertIn("modifier = { factor = 16 years_passed < 30 }", ai_weight_text)
        self.assertIn("modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 8 owner = { staid_pd_research_outpost_priority_ready = yes } }", ai_weight_text)
        self.assertIn("modifier = { factor = 7 is_capital = yes }", ai_weight_text)
        self.assertNotIn("has_technology", ai_weight_text)
        self.assertNotIn("pd_domed_research_site", ai_weight_text)
        self.assertIn("staid_planetary_diversity_outpost_investment_ready", triggers_text)
        self.assertIn("Stellar AI Director Planetary Diversity outpost reserve", economy_text)

    def test_planetary_diversity_modifier_profiles_drive_building_roles(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_12_planetary_diversity_value_triggers.txt"
        building_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_12_planetary_diversity_buildings.txt"
        profile_path = RESEARCH_ROOT / "stellar-ai-director-planetary-diversity-profile-2026-07-07.md"
        for path in (trigger_path, building_path):
            self.assertTrue(path.exists(), f"Missing generated PD profile surface: {path}")
            parse_file(path)

        trigger_text = trigger_path.read_text(encoding="utf-8")
        building_text = building_path.read_text(encoding="utf-8")
        profile_text = profile_path.read_text(encoding="utf-8")
        for marker in (
            "staid_pd_planet_research_value",
            "staid_pd_planet_alloys_value",
            "staid_pd_planet_minerals_value",
            "staid_pd_planet_energy_value",
            "staid_pd_planet_growth_value",
        ):
            self.assertIn(marker, trigger_text)
        self.assertIn("building_megalfora_lab", building_text)
        self.assertIn("pd_economic_role = research", building_text)
        self.assertIn("strategic value horizon year", (MOD_ROOT / "notes" / "tuning-notes.md").read_text(encoding="utf-8"))
        self.assertIn("Hostile Space Fauna Clearance", profile_text)

    def test_militarist_conquest_and_raiding_surfaces_are_generated(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        policies_path = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        bombardment_path = MOD_ROOT / "common" / "bombardment_stances" / "zzzz_staid_12_militarist_raiding_bombardment.txt"
        ascension_path = MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt"
        for path in (policies_path, bombardment_path):
            self.assertTrue(path.exists(), f"Missing generated militarist surface: {path}")
            parse_file(path)
        policies = policies_path.read_text(encoding="utf-8")
        bombardment = bombardment_path.read_text(encoding="utf-8")
        ascension_perks = ascension_path.read_text(encoding="utf-8")
        for marker in (
            "staid_militarist_conquest_strategy",
            "staid_raiding_pop_growth_strategy",
            "staid_hostile_fauna_clearance_strategy",
            "staid_raiding_pop_acquisition_priority",
        ):
            self.assertIn(marker, triggers)
        conquest_block = triggers[
            triggers.index("staid_militarist_conquest_strategy = {") : triggers.index(
                "staid_raiding_pop_growth_strategy = {"
            )
        ]
        raiding_block = triggers[
            triggers.index("staid_raiding_pop_growth_strategy = {") : triggers.index(
                "staid_raiding_pop_acquisition_priority = {"
            )
        ]
        self.assertIn("used_naval_capacity_percent < 1.95", conquest_block)
        self.assertIn("used_naval_capacity_percent < 2.00", raiding_block)
        self.assertIn("staid_catastrophic_collapse_mode", conquest_block + raiding_block)
        self.assertNotIn("staid_core_deficit_short_runway", conquest_block + raiding_block)
        self.assertNotIn("staid_survival_mode", conquest_block + raiding_block)
        self.assertNotIn("recently_lost_war", conquest_block + raiding_block)
        for marker in (
            "Stellar AI Director militarist conquest fleet reserve",
            "Stellar AI Director raiding pop acquisition reserve",
            "Stellar AI Director hostile fauna clearance reserve",
        ):
            self.assertIn(marker, economy)
        self.assertIn("staid_militarist_conquest_strategy", policies)
        self.assertIn("orbital_bombardment = {", policies)
        self.assertIn("orbital_bombardment_indiscriminate", policies)
        self.assertNotIn("factor = 24 staid_raiding_pop_growth_strategy = yes", policies)
        self.assertIn("factor = 18 staid_militarist_conquest_strategy = yes", policies)
        self.assertIn("orbital_bombardment_accept_surrender = {", policies)
        self.assertIn("orbital_bombardment_surrender_forbidden", policies)
        self.assertIn("base = 1", policies)
        self.assertIn("factor = 80 staid_raiding_pop_growth_strategy = yes", policies)
        self.assertNotIn("Orbital bombardment policy is documented as a follow-up", policies)
        self.assertIn("raiding = {", bombardment)
        self.assertIn("abduct_pops = yes", bombardment)
        self.assertIn("factor = 60 owner = { staid_raiding_pop_growth_strategy = yes }", bombardment)
        self.assertIn("ap_nihilistic_acquisition", ascension_perks)
        self.assertIn("staid_raiding_pop_acquisition_priority", ascension_perks)

    def test_dataset_job_pressure_adds_ai_resource_production(self):
        amounts = dataset_ai_resource_production_amounts(
            {
                "object_id": "building_test_research_jobs",
                "object_type": "building",
                "jobs_created_total_estimate": "300",
                "direct_monthly_output_json": "{}",
                "modifier_keys": "job_researcher_add|planet_researchers_physics_research_produces_add",
                "pressure_family": "research_scaling",
            }
        )
        self.assertEqual(amounts["physics_research"], 1)
        self.assertIn("society_research", amounts)
        self.assertIn("engineering_research", amounts)

        direct_amounts = dataset_ai_resource_production_amounts(
            {
                "object_id": "building_test_factory",
                "object_type": "building",
                "jobs_created_total_estimate": "0",
                "direct_monthly_output_json": '{"consumer_goods":35.0}',
                "modifier_keys": "",
                "pressure_family": "consumer_goods_repair",
            }
        )
        self.assertEqual(direct_amounts, {"consumer_goods": 35})

    def test_high_scale_construction_plan_and_budget_pressure_are_generated(self):
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_minerals_planet_construction_budget.txt"
        building_pressure_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_13_dataset_job_pressure_buildings.txt"
        district_pressure_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_13_dataset_job_pressure_districts.txt"
        zone_pressure_path = MOD_ROOT / "common" / "zones" / "zzzz_staid_13_dataset_job_pressure_zones.txt"
        for path in (economy_path, budget_path, building_pressure_path, district_pressure_path):
            self.assertTrue(path.exists(), f"Missing generated high-scale construction surface: {path}")
            parse_file(path)
        self.assertFalse(zone_pressure_path.exists(), "Zone full-object copies are runtime-unsafe and must not load.")
        economy = economy_path.read_text(encoding="utf-8")
        budget = budget_path.read_text(encoding="utf-8")
        pressure = (
            building_pressure_path.read_text(encoding="utf-8")
            + district_pressure_path.read_text(encoding="utf-8")
        )
        for marker in (
            "Stellar AI Director construction spenddown reserve",
            "Stellar AI Director unemployed pop construction catch-up",
            "Stellar AI Director open slot construction catch-up",
            "Stellar AI Director rich empire spend-down construction",
        ):
            self.assertIn(marker, economy)
        self.assertIn("staid_construction_spenddown_pressure = yes", economy)
        self.assertNotIn("empire_size =", economy)
        self.assertIn("staid_construction_spenddown_pressure = {", pressure + (
            MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        ).read_text(encoding="utf-8"))
        self.assertIn("modifier = { factor = 40 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }", budget)
        self.assertIn("modifier = { factor = 35 staid_construction_spenddown_pressure = yes }", budget)
        self.assertIn("resource_stockpile_compare = { resource = minerals value > 25000 }", budget)
        self.assertIn("ai_resource_production = {", pressure)
        self.assertIn("owner = { staid_construction_spenddown_pressure = yes }", pressure)
        self.assertNotIn("factor = 0 owner = { AND = { staid_survival_mode = yes", pressure)
        trigger_text = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        construction_block = trigger_text[
            trigger_text.index("staid_construction_spenddown_pressure = {") : trigger_text.index(
                "staid_research_under_curve = {"
            )
        ]
        self.assertIn("NOT = { staid_catastrophic_collapse_mode = yes }", construction_block)
        self.assertNotIn("staid_recovery_mode", construction_block)

    def test_staid_scripted_trigger_graph_has_no_cycles(self):
        self.assertEqual(validate_staid_scripted_trigger_cycles(MOD_ROOT), [])

    def test_july7_inventory_and_static_validation_notes_are_generated(self):
        for path in (GENERATED_VERSION_INVENTORY_MD, MOD_STACK_COMPATIBILITY_MD, MANUAL_STATIC_VALIDATION_MD):
            self.assertTrue(path.exists(), f"Missing generated July 7 note: {path}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("Generated by `tools/generate_stellar_ai_director_patch.py`", text)
        inventory = GENERATED_VERSION_INVENTORY_MD.read_text(encoding="utf-8")
        self.assertIn("4.4.5", inventory)
        self.assertIn("v4.4.*", inventory)
        compatibility = MOD_STACK_COMPATIBILITY_MD.read_text(encoding="utf-8")
        self.assertIn("computed scripted triggers", compatibility)
        validation = MANUAL_STATIC_VALIDATION_MD.read_text(encoding="utf-8")
        self.assertIn("no Stellaris launch", validation)

    def test_stockpile_waste_and_low_research_activate_surplus_sink(self):
        state = EmpireState(
            incomes={
                "energy": 200,
                "alloys": 80,
                "trade": 20,
                "minerals": 900,
                "food": 300,
                "consumer_goods": 300,
                "physics_research": 500,
                "society_research": 500,
                "engineering_research": 700,
            },
            stockpiles={
                "minerals": 82000,
                "food": 82000,
                "consumer_goods": 65000,
            },
            research_sink_available=True,
        )
        self.assertTrue(resource_waste_pressure(state))
        self.assertTrue(research_under_curve(state, years_passed=165))
        self.assertTrue(surplus_sink_pressure(state))

    def test_generated_research_and_market_safety_surfaces_cover_runtime_failures(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        market_events = (MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt").read_text(
            encoding="utf-8"
        )
        for marker in (
            "staid_resource_waste_pressure",
            "resource_stockpile_compare = { resource = minerals value > 25000 }",
            "resource_stockpile_compare = { resource = consumer_goods value > 18000 }",
            "staid_consumer_goods_runway_safe",
            "staid_food_runway_safe",
            "staid_research_input_runway_safe",
            "Stellar AI Director consumer goods runway repair",
            "Stellar AI Director food break-even repair",
            "staid_research_under_curve",
            "Stellar AI Director capped stockpile research conversion",
            "Stellar AI Director 2360 engineering catchup",
            "value:stellarai_market_sell_value|RESOURCE|minerals|AMOUNT|5000|",
            "value:stellarai_market_sell_value|RESOURCE|giga_sr_sentient_metal|AMOUNT|250|",
            "staid_high_scale_snowball_pressure",
            "Stellar AI Director pathological snowball reserve",
            "Stellar AI Director megastructure spam reserve",
        ):
            self.assertIn(marker, triggers + economy + market_events)

    def test_generated_stranded_fleet_recovery_uses_guarded_vanilla_mia(self):
        on_action_path = MOD_ROOT / "common" / "on_actions" / "zzz_staid_market_and_fleet_safety_on_actions.txt"
        event_path = MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt"
        parse_file(on_action_path)
        parse_file(event_path)
        text = event_path.read_text(encoding="utf-8")
        for marker in (
            "staid_homeland_under_attack = yes",
            "can_go_mia = yes",
            "is_fleet_idle = yes",
            "is_in_combat = no",
            "has_fleet_flag = staid_stranded_fleet_warning",
            "set_timed_fleet_flag",
            "set_mia = mia_return_home",
            "space_owner = { NOT = { is_same_value = root } }",
        ):
            self.assertIn(marker, text)

    def test_route_overrides_carry_source_local_variables(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        technology_text = technology_path.read_text(encoding="utf-8")
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        for marker in ("@tier4cost4 = 28000", "@tier5weight3 = 20"):
            self.assertIn(marker, technology_text)
        for marker in ("@giga_mega_unity_cost", "@giga_giga_unity_cost"):
            self.assertIn(marker, megastructure_text)
        self.assertEqual(generated_unresolved_at_variable_rows(MOD_ROOT), [])

    def test_megastructure_route_weights_use_country_from_scope(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        parse_file(megastructure_path)
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        macro_test_site_block = megastructure_text[
            megastructure_text.index("macro_test_site_3 = {") : megastructure_text.index("atmosphere_shredder_0 = {")
        ]
        for marker in (
            "modifier = { factor = 0 from = { staid_survival_mode = yes } }",
            "modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }",
            "modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }",
            "modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }",
            "modifier = { factor = 3 from = { staid_research_under_curve = yes } }",
        ):
            self.assertIn(marker, macro_test_site_block)
        for marker in (
            "modifier = { factor = 0 staid_survival_mode = yes }",
            "modifier = { factor = 0 NOT = { staid_science_kilo_build_priority_ready = yes } }",
            "modifier = { factor = 4 staid_science_kilo_build_priority_ready = yes }",
            "modifier = { factor = 4 has_technology = giga_tech_engineering_test_site }",
            "modifier = { factor = 3 staid_research_under_curve = yes }",
        ):
            self.assertNotIn(marker, macro_test_site_block)

    def test_research_and_pop_assembly_buildings_have_owner_economy_gates(self):
        research_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_06_research_infrastructure_buildings.txt"
        pop_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_07_pop_assembly_buildings.txt"
        parse_file(research_path)
        parse_file(pop_path)
        research_text = research_path.read_text(encoding="utf-8")
        pop_text = pop_path.read_text(encoding="utf-8")
        self.assertIn(
            "modifier = { factor = 0 owner = { NOT = { staid_research_input_runway_safe = yes } } }",
            research_text,
        )
        self.assertIn(
            "modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }",
            pop_text,
        )

    def test_habitat_route_override_repairs_gigas_spawn_effect_parameters(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        parse_file(megastructure_path)
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        habitat_block = megastructure_text[
            megastructure_text.index("habitat_central_complex = {") : megastructure_text.index(
                "interstellar_habitat_0 = {"
            )
        ]
        self.assertIn("spawn_habitat_effect = {", habitat_block)
        self.assertIn("HABITAT_OWNER = root", habitat_block)
        self.assertIn("TARGET_PLANET = event_target:target_planet", habitat_block)
        self.assertNotIn("spawn_habitat_effect = {\n                DISTANCE =", habitat_block)

    def test_gigas_habitat_compat_effects_fail_closed_on_removed_orbital_ship_sizes(self):
        scripted_effects_path = (
            MOD_ROOT / "common" / "scripted_effects" / "zzz_staid_gigas_habitat_compat_effects.txt"
        )
        parse_file(scripted_effects_path)
        text = scripted_effects_path.read_text(encoding="utf-8")
        for marker in (
            "science_kilo_update_orbital_effect = {",
            "giga_dismantle_science_kilo_effect = {",
            "always = no # removed stale major_orbital_resource ship-size probe",
            "always = no # removed stale minor_orbital_resource ship-size probe",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("is_ship_size = major_orbital_resource", text)
        self.assertNotIn("is_ship_size = minor_orbital_resource", text)
        self.assertNotIn("is_ship_size = major_orbital", text)
        self.assertNotIn("is_ship_size = minor_orbital", text)
        self.assertNotIn("is_ship_size = habitat_major_orbital", text)
        self.assertNotIn("is_ship_size = habitat_minor_orbital", text)

    def test_ai_budget_overrides_do_not_emit_unsupported_ai_weight_blocks(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        parse_file(budget_path)
        text = budget_path.read_text(encoding="utf-8")
        self.assertIn("influence_expenditure_claims = {", text)
        self.assertIn("weight = {", text)
        self.assertNotIn("ai_weight = {", text)

    def test_starbase_route_weights_use_owner_country_scope(self):
        starbase_path = (
            MOD_ROOT / "common" / "starbase_buildings" / "zzzz_staid_05_starbase_defense_starbase_buildings.txt"
        )
        module_path = MOD_ROOT / "common" / "starbase_modules" / "zzzz_staid_05_starbase_defense_starbase_modules.txt"
        parse_file(starbase_path)
        parse_file(module_path)
        text = starbase_path.read_text(encoding="utf-8")
        module_text = module_path.read_text(encoding="utf-8")
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn("modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }", text)
        self.assertIn("modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }", text)
        self.assertIn("modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }", text)
        self.assertNotIn("modifier = { factor = 0 owner = { staid_survival_mode = yes } }", text)
        self.assertNotIn("modifier = { factor = 0 staid_survival_mode = yes }", text)
        self.assertIn("staid_militarist_conquest_strategy = yes", triggers)
        self.assertNotIn("NOT = { staid_aggressive_fleet_pressure = yes }", triggers)
        self.assertIn("alloys = 2200", economy)
        self.assertIn("naval_cap = 1000", economy)
        for marker in (
            "esc_starbase_reactor = {",
            "adv_starbase_defenses = {",
            "reinforced_defenses = {",
            "strategic_defenses = {",
        ):
            self.assertIn(marker, text)
        for marker in (
            "gun_battery = {",
            "missile_battery = {",
            "hangar_bay = {",
            "large_battery = {",
            "armor_module = {",
            "orbital_ring_gun_battery = {",
            "orbital_ring_missile_battery = {",
            "orbital_ring_hangar_bay = {",
            "orbital_ring_large_gun_battery = {",
            "orbital_ring_armor_module = {",
        ):
            self.assertIn(marker, module_text)
        self.assertIn(
            "modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }",
            module_text,
        )
        self.assertIn("modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }", module_text)
        for object_id in ("gun_battery", "missile_battery", "orbital_ring_gun_battery", "orbital_ring_missile_battery"):
            block = extract_top_level_object_text(module_text, object_id)
            depth = 0
            top_level_potentials = 0
            for line in block.splitlines():
                if depth == 1 and re.match(r"^\s*potential\s*=", line):
                    top_level_potentials += 1
                depth += line.count("{") - line.count("}")
            self.assertEqual(top_level_potentials, 1, f"{object_id} should merge duplicate top-level potential blocks")

    def test_threat_response_war_goal_checks_use_block_syntax(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_threat_response_triggers.txt"
        parse_file(trigger_path)
        text = trigger_path.read_text(encoding="utf-8")
        self.assertIn("using_war_goal = { type = wg_conquest owner = root }", text)
        self.assertIn("using_war_goal = { type = wg_subjugation owner = root }", text)
        self.assertIn("using_war_goal = { type = wg_humiliation owner = root }", text)
        self.assertNotIn("using_war_goal = wg_", text)

    def test_threat_response_observer_event_reads_attacker_war_goal_flags(self):
        event_path = MOD_ROOT / "events" / "zzz_staid_threat_response_events.txt"
        parse_file(event_path)
        text = event_path.read_text(encoding="utf-8")
        for marker in (
            "set_timed_country_flag = { flag = staid_tr_war_goal_subjugation",
            "set_timed_country_flag = { flag = staid_tr_war_goal_conquest",
            "set_timed_country_flag = { flag = staid_tr_war_goal_humiliation",
            "limit = { from = { has_country_flag = staid_tr_war_goal_subjugation } }",
            "limit = { from = { has_country_flag = staid_tr_war_goal_conquest } }",
            "limit = { from = { has_country_flag = staid_tr_war_goal_humiliation } }",
        ):
            self.assertIn(marker, text)
        observer_event = text[text.index("id = staid_tr.2") :]
        self.assertNotIn("staid_tr_is_subjugation_war_goal", observer_event)
        self.assertNotIn("staid_tr_is_conquest_war_goal", observer_event)
        self.assertNotIn("staid_tr_is_humiliation_war_goal", observer_event)

    def test_gigas_habitat_zone_slot_compat_districts_cover_new_habitat_route(self):
        district_path = (
            MOD_ROOT / "common" / "districts" / "zzzz_staid_09_gigas_habitat_zone_slot_compat_districts.txt"
        )
        parse_file(district_path)
        text = district_path.read_text(encoding="utf-8")
        expected_slots = {
            "district_giga_hab_city": "slot_habitat_01",
            "district_giga_hab_hive": "slot_habitat_01",
            "district_giga_hab_nexus": "slot_habitat_01",
            "district_giga_hab_science": "slot_habitat_research",
            "district_giga_hab_scavenger": "slot_habitat_minerals",
            "district_giga_orbital_farming": "slot_city_01",
            "district_giga_orbital_sanctuary": "slot_city_government",
            "district_giga_orbital_preserve": "slot_city_01",
            "district_giga_orbital_logistics": "slot_city_government",
        }
        for object_id, slot in expected_slots.items():
            block = text[text.index(f"{object_id} = {{") :]
            block = block[: block.find("\n}\n") + 3]
            self.assertIn("zone_slots = {", block)
            self.assertIn(slot, block)
        self.assertNotIn("is_capped_by_modifier", text)

    def test_route_research_weights_do_not_self_gate_unlock_targets(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        technology_text = technology_path.read_text(encoding="utf-8")
        mega_shipyard_block = technology_text[
            technology_text.index("tech_mega_shipyard = {") : technology_text.index("giga_tech_planet_assembly = {")
        ]
        self.assertIn("# policy_route = mega_shipyard_core", mega_shipyard_block)
        self.assertIn("staid_core_unlock_research_priority_ready = yes", mega_shipyard_block)
        self.assertNotIn("staid_shipyard_expansion_ready = yes", mega_shipyard_block)

    def test_gigas_progression_overrides_cover_deep_unlocks_and_build_gates(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        text = (
            technology_path.read_text(encoding="utf-8")
            + megastructure_path.read_text(encoding="utf-8")
            + trigger_path.read_text(encoding="utf-8")
        )
        for marker in (
            "giga_tech_war_moon_1 = {",
            "giga_tech_war_moon_2 = {",
            "giga_tech_war_system_6 = {",
            "tech_nm_utilization_1 = {",
            "staid_war_moon_research_priority_ready = yes",
            "staid_systemcraft_research_priority_ready = yes",
            "staid_gigas_special_resource_unlock_ready = yes",
            "staid_war_moon_build_priority_ready = yes",
            "staid_systemcraft_build_priority_ready = yes",
            "has_ascension_perk = ap_celestial_printing",
        ):
            self.assertIn(marker, text)

    def test_phase_machine_and_modded_conversion_gates_are_generated(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(trigger_path)
        text = technology_path.read_text(encoding="utf-8") + trigger_path.read_text(encoding="utf-8")
        for marker in (
            "staid_phase_mega_engineering_rush = {",
            "staid_phase_galactic_wonders_entry = {",
            "staid_phase_gigastructural_constructs_rush = {",
            "staid_phase_planetcraft_rush = {",
            "staid_phase_systemcraft_escalation = {",
            "staid_phase_fleet_conversion_repeatables = {",
            "staid_nsc3_capital_hull_unlock_ready = {",
            "staid_esc_component_unlock_ready = {",
            "staid_advanced_component_resource_support_ready = {",
            "staid_modded_fleet_conversion_ready = {",
            "resource = sr_dark_matter value > 1",
            "resource = giga_sr_sentient_metal value > 1",
            "staid_nsc3_capital_hull_unlock_ready = yes",
            "staid_esc_component_unlock_ready = yes",
            "NOT = { staid_advanced_component_resource_support_ready = yes }",
            "has_technology = tech_Flagship_1",
            "has_technology = esc_tech_dark_matter_power_core_2",
        ):
            self.assertIn(marker, text)

    def test_fleet_conversion_gates_have_income_pressure_lane(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(trigger_path)
        text = trigger_path.read_text(encoding="utf-8")
        shipyard_block = text[
            text.index("staid_shipyard_payoff_ready = {") : text.index("staid_fleet_buildup_economy_safe = {")
        ]
        fleet_block = text[
            text.index("staid_fleet_buildup_economy_safe = {") : text.index("staid_resource_waste_pressure = {")
        ]
        for block in (shipyard_block, fleet_block):
            self.assertIn("NOT = { staid_catastrophic_collapse_mode = yes }", block)
            self.assertNotIn("staid_survival_mode = yes", block)
            self.assertNotIn("staid_core_deficit_short_runway = yes", block)
        self.assertIn("used_naval_capacity_percent < 1.60", shipyard_block)
        self.assertIn("has_monthly_income = { resource = alloys value > 80 }", shipyard_block)
        self.assertNotIn("staid_militarist_conquest_strategy = yes", shipyard_block)
        self.assertNotIn("staid_raiding_pop_growth_strategy = yes", shipyard_block)
        self.assertIn("used_naval_capacity_percent < 1.85", fleet_block)
        self.assertIn("has_monthly_income = { resource = alloys value > 40 }", fleet_block)
        self.assertIn("has_monthly_income = { resource = energy value > 40 }", fleet_block)
        self.assertNotIn("staid_aggressive_fleet_pressure = yes", fleet_block)
        self.assertNotIn("staid_militarist_conquest_strategy = yes", fleet_block)
        self.assertNotIn("staid_raiding_pop_growth_strategy = yes", fleet_block)
        self.assertNotIn("has_monthly_income = { resource = alloys value > 200 }", shipyard_block)
        self.assertIn("resource_stockpile_compare = { resource = alloys value >", shipyard_block)
        self.assertIn("resource_stockpile_compare = { resource = energy value > 8000 }", fleet_block)

    def test_research_infrastructure_overrides_drive_labs_and_habitat_science(self):
        buildings_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_06_research_infrastructure_buildings.txt"
        districts_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt"
        parse_file(buildings_path)
        parse_file(districts_path)
        buildings_text = buildings_path.read_text(encoding="utf-8")
        districts_text = districts_path.read_text(encoding="utf-8")
        for marker in (
            "# policy_route = research_throughput_infrastructure",
            "building_research_lab_1 = {",
            "building_research_lab_2 = {",
            "building_research_lab_3 = {",
            "building_institute = {",
            "building_supercomputer = {",
            "building_archaeostudies_faculty = {",
            "ai_weight_coefficient = 12",
            "additional_ai_weight = 1200",
            "script = stellarai/rare_resource_guard_modifiers",
        ):
            self.assertIn(marker, buildings_text)
        for marker in (
            "# policy_route = crowded_tall_route",
            "district_hab_science = {",
            "ai_weight_coefficient = 4",
            "additional_ai_weight = 500",
        ):
            self.assertIn(marker, districts_text)

    def test_unresolved_source_local_variables_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir)
            common = mod_root / "common" / "technology"
            common.mkdir(parents=True)
            (common / "broken.txt").write_text("tech_test = { cost = @missing_cost }\n", encoding="utf-8")
            self.assertEqual(
                generated_unresolved_at_variable_rows(mod_root),
                [
                    {
                        "generated_file": "common/technology/broken.txt",
                        "line": "1",
                        "variable": "@missing_cost",
                    }
                ],
            )

    def test_object_atlas_artifacts_are_static_valid(self):
        self.assertEqual(validate_object_atlas_artifacts(), [])
        for path in (OBJECT_ATLAS_CSV, DEPENDENCY_EDGES_CSV, AI_SUPPORT_MAP_CSV, POLICY_MATRIX_CSV):
            self.assertTrue(path.exists(), f"Missing generated atlas artifact: {path}")

    def test_object_atlas_contains_required_route_objects(self):
        atlas_text = OBJECT_ATLAS_CSV.read_text(encoding="utf-8")
        for marker in (
            "planetcraft",
            "systemcraft",
            "mega_shipyard",
            "esc_tech_dark_matter_power_core_2",
            "building_research_lab_1",
            "district_hab_science",
        ):
            self.assertIn(marker, atlas_text)

    def test_policy_matrix_references_atlas_objects(self):
        with OBJECT_ATLAS_CSV.open("r", encoding="utf-8", newline="") as handle:
            atlas_rows = list(csv.DictReader(handle))
        with POLICY_MATRIX_CSV.open("r", encoding="utf-8", newline="") as handle:
            policy_rows = list(csv.DictReader(handle))
        atlas_ids = {row["object_id"] for row in atlas_rows if row["validation_status"] == "ok"}
        self.assertTrue(policy_rows, "Policy matrix did not contain any rows.")
        missing = sorted({row["object_id"] for row in policy_rows if row["object_id"] not in atlas_ids})
        self.assertEqual(missing, [])

    def test_route_override_surfaces_cover_required_families(self):
        with (RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.csv").open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        covered_routes = {row["route_id"] for row in rows}
        required_routes = {
            "mega_engineering_core",
            "mega_shipyard_core",
            "economy_megastructure_core",
            "early_kilo_economy_core",
            "science_kilo_snowball_core",
            "research_megastructure_core",
            "planetary_computer_research_core",
            "pop_assembly_snowball_core",
            "ring_world_growth_core",
            "storage_cap_core",
            "planetcraft_route",
            "war_moon_route",
            "systemcraft_route",
            "nsc3_capital_hull_route",
            "esc_component_route",
            "crowded_tall_route",
            "conquest_escape_route",
            "apex_site_preservation_core",
            "fallen_empire_benchmark_route",
            "research_throughput_infrastructure",
            "research_diplomacy_core",
        }
        self.assertTrue(required_routes.issubset(covered_routes))
        for row in rows:
            generated_file = Path(row["generated_file"])
            self.assertTrue(generated_file.exists(), f"Missing route override file: {generated_file}")
            self.assertIn(row["object_id"], generated_file.read_text(encoding="utf-8"))
        self.assertTrue((RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.md").exists())

    def test_snowball_checkpoint_routes_cover_research_surface_storage_and_early_kilos(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        buildings_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_07_pop_assembly_buildings.txt"
        districts_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt"
        claim_budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        federation_path = MOD_ROOT / "common" / "federation_types" / "zzzz_staid_15_research_diplomacy_federation_types.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(technology_path)
        parse_file(megastructure_path)
        parse_file(buildings_path)
        parse_file(districts_path)
        parse_file(claim_budget_path)
        parse_file(federation_path)
        parse_file(trigger_path)
        text = (
            technology_path.read_text(encoding="utf-8")
            + megastructure_path.read_text(encoding="utf-8")
            + buildings_path.read_text(encoding="utf-8")
            + districts_path.read_text(encoding="utf-8")
            + claim_budget_path.read_text(encoding="utf-8")
            + federation_path.read_text(encoding="utf-8")
            + trigger_path.read_text(encoding="utf-8")
        )
        for marker in (
            "tech_science_nexus = {",
            "tech_ring_world = {",
            "tech_orbital_arc_furnace = {",
            "giga_tech_asteroid_manufactory = {",
            "giga_tech_engineering_test_site = {",
            "giga_tech_macro_scale_weather_manipulation = {",
            "giga_tech_planetary_computer = {",
            "tech_robotic_workers = {",
            "tech_cloning = {",
            "giga_tech_kugelblitz = {",
            "giga_tech_matrioshka_brain_1 = {",
            "giga_tech_neutronium_gigaforge = {",
            "giga_tech_nidavellir = {",
            "giga_tech_interstellar_habitat = {",
            "giga_tech_stellar_ring_habitat = {",
            "think_tank_0 = {",
            "think_tank_3 = {",
            "ring_world_1 = {",
            "ring_world_3_intermediate = {",
            "kugelblitz_0 = {",
            "kugelblitz_3 = {",
            "habitat_central_complex = {",
            "interstellar_habitat_0 = {",
            "stellar_ring_habitat_0 = {",
            "orbital_arc_furnace_1 = {",
            "asteroid_manufactory_0 = {",
            "macro_test_site_0 = {",
            "macro_test_site_3 = {",
            "atmosphere_shredder_0 = {",
            "atmosphere_shredder_3 = {",
            "planetary_computer_0 = {",
            "planetary_computer_1 = {",
            "matrioshka_brain_0_o_star = {",
            "dyson_sphere_0_o_star = {",
            "neutronium_gigaforge_0 = {",
            "nidavellir_forge_0 = {",
            "district_giga_pcc_science = {",
            "building_robot_assembly_plant = {",
            "building_clone_vats = {",
            "building_spawning_pool = {",
            "influence_expenditure_claims = {",
            "influence_expenditure_claims_militarist = {",
            "influence_expenditure_claims_fanatic_militarist = {",
            "research_federation = {",
            "# policy_route = early_kilo_economy_core",
            "# policy_route = science_kilo_snowball_core",
            "# policy_route = research_megastructure_core",
            "# policy_route = planetary_computer_research_core",
            "# policy_route = pop_assembly_snowball_core",
            "# policy_route = ring_world_growth_core",
            "# policy_route = storage_cap_core",
            "# policy_route = apex_site_preservation_core",
            "# policy_route = conquest_escape_route",
            "staid_phase_early_kilo_economy = {",
            "staid_phase_science_kilo_snowball = {",
            "staid_phase_pop_assembly_snowball = {",
            "staid_phase_science_nexus_rush = {",
            "staid_phase_planetary_computer_research = {",
            "staid_phase_ring_world_growth = {",
            "staid_phase_storage_cap_expansion = {",
            "staid_phase_boxed_tall_habitat_escape = {",
            "staid_site_limited_expansion_ready = {",
            "staid_apex_site_preservation_ready = {",
            "staid_science_nexus_build_priority_ready = yes",
            "staid_science_kilo_build_priority_ready = yes",
            "staid_planetary_computer_build_priority_ready = yes",
            "staid_pop_assembly_snowball_ready = yes",
            "staid_ring_world_build_priority_ready = yes",
            "staid_storage_cap_build_priority_ready = yes",
            "staid_early_kilo_economy_build_priority_ready = yes",
            "staid_apex_site_preservation_ready = yes",
            "staid_research_diplomacy_priority_ready = {",
        ):
            self.assertIn(marker, text)

    def test_research_federation_weight_is_generated_without_unsafe_diplomacy_overrides(self):
        federation_path = MOD_ROOT / "common" / "federation_types" / "zzzz_staid_15_research_diplomacy_federation_types.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(federation_path)
        parse_file(trigger_path)

        text = federation_path.read_text(encoding="utf-8")
        trigger_text = trigger_path.read_text(encoding="utf-8")
        research_federation = extract_top_level_object_text(text, "research_federation")

        self.assertIn("# policy_route = research_diplomacy_core", text)
        self.assertIn("host_has_dlc = Federations", research_federation)
        self.assertIn("research_federation_passive", research_federation)
        self.assertIn("ai_weight = {", research_federation)
        self.assertIn("staid_research_diplomacy_core", research_federation)
        self.assertIn("from = { staid_research_diplomacy_priority_ready = yes }", research_federation)
        self.assertIn("has_active_tradition = tr_discovery_federations_finish", research_federation)
        self.assertIn("staid_research_diplomacy_priority_ready = {", trigger_text)

        self.assertFalse((MOD_ROOT / "common" / "diplomatic_actions").exists())
        self.assertFalse((MOD_ROOT / "common" / "personalities").exists())

    def test_megastructure_upgrade_stages_are_prioritized_over_new_starts(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(megastructure_path)
        parse_file(trigger_path)

        text = megastructure_path.read_text(encoding="utf-8")
        trigger_text = trigger_path.read_text(encoding="utf-8")
        self.assertIn("staid_megastructure_continuation_priority_ready = {", trigger_text)
        self.assertIn("staid_unfinished_kugelblitz_exists = {", trigger_text)
        self.assertIn("any_owned_megastructure = {", trigger_text)
        for unfinished_stage in ("kugelblitz_0", "kugelblitz_1", "kugelblitz_2", "kugelblitz_restored"):
            self.assertIn(f"is_megastructure_type = {unfinished_stage}", trigger_text)
        self.assertIn("staid_kugelblitz_new_start_budget_ready = {", trigger_text)
        self.assertIn("NOT = { staid_unfinished_kugelblitz_exists = yes }", trigger_text)
        self.assertIn("NOT = { check_variable = { which = giga_current_kugel value >= 10 } }", trigger_text)

        starter = extract_top_level_object_text(text, "kugelblitz_0")
        first_upgrade = extract_top_level_object_text(text, "kugelblitz_1")
        final_upgrade = extract_top_level_object_text(text, "kugelblitz_3")

        self.assertNotIn("megastructure_continuation_priority = finish_existing_before_new_start", starter)
        self.assertIn("kugelblitz_start_budget = empty_silos_are_capped_storage_not_income", starter)
        self.assertIn("modifier = { factor = 0 from = { check_variable = { which = giga_current_kugel value >= 10 } } }", starter)
        self.assertIn("modifier = { factor = 0 from = { has_country_flag = is_currently_building_kugelblitz } }", starter)
        self.assertIn("modifier = { factor = 0 from = { staid_unfinished_kugelblitz_exists = yes } }", starter)
        self.assertIn("modifier = { factor = 0.02 from = { check_variable = { which = giga_current_kugel value >= 9 } } }", starter)
        for block in (first_upgrade, final_upgrade):
            self.assertIn("upgrade_from = {", block)
            self.assertIn("megastructure_continuation_priority = finish_existing_before_new_start", block)
            self.assertIn("staid_megastructure_continuation_priority_ready = yes", block)
            self.assertIn("modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }", block)
            self.assertNotIn("kugelblitz_start_budget = empty_silos_are_capped_storage_not_income", block)


if __name__ == "__main__":
    unittest.main()
```

## tools/tests/test_stellar_ai_observer_loop.py

```python
import csv
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stellar_ai_observer_loop import (
    CHECKPOINT_FIELDS,
    checkpoint_save_report_text,
    create_observer_run,
    extract_checkpoint_rows_from_save,
    latest_observer_run,
    summarize_observer_run,
)
from manage_stellaris_commands_at_date import (
    OBSERVER_COMMAND_SCHEDULE,
    commands_status,
    disable_commands,
    enable_observer_schedule,
)


class StellarAiObserverLoopTests(unittest.TestCase):
    def test_commands_at_date_uses_dev_only_game_speed_five(self):
        self.assertIn('2200.01.01 = "game_speed 5"', OBSERVER_COMMAND_SCHEDULE)
        self.assertIn('2200.01.02 = "game_speed 5"', OBSERVER_COMMAND_SCHEDULE)
        self.assertNotIn('game_speed 4"', OBSERVER_COMMAND_SCHEDULE)
        self.assertIn("GAME_SPEED_6", OBSERVER_COMMAND_SCHEDULE)

    def test_commands_at_date_observer_schedule_is_explicit_and_removable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            live_path = Path(temp_dir) / "commands_at_date.txt"

            self.assertFalse(commands_status(live_path).exists)
            enable_observer_schedule(live_path)

            enabled_status = commands_status(live_path)
            self.assertTrue(enabled_status.exists)
            self.assertTrue(enabled_status.managed_observer_schedule)
            self.assertTrue(enabled_status.contains_game_pause)
            self.assertTrue(enabled_status.contains_observer_commands)

            disabled_path = disable_commands(live_path)

            self.assertIsNotNone(disabled_path)
            self.assertFalse(live_path.exists())
            self.assertTrue(disabled_path.exists())
            self.assertIn("disabled-by-codex", disabled_path.name)

    def test_commands_at_date_enable_refuses_to_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            live_path = Path(temp_dir) / "commands_at_date.txt"
            live_path.write_text('2250.01.01 = "some_user_command"\n', encoding="utf-8")

            with self.assertRaises(FileExistsError):
                enable_observer_schedule(live_path)

            self.assertEqual(live_path.read_text(encoding="utf-8"), '2250.01.01 = "some_user_command"\n')

    def test_create_observer_run_writes_standard_layout(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = create_observer_run(root=root, run_id="observer-test")

            for relative_path in (
                "README.md",
                "metadata.json",
                "manual-notes.md",
                "checkpoints.csv",
                "metrics.json",
                "summary.json",
                "summary.md",
                "logs",
                "saves",
                "screenshots",
                "exports",
            ):
                self.assertTrue((run_dir / relative_path).exists(), relative_path)

            metadata = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["run_id"], "observer-test")
            self.assertFalse(metadata["hidden_economic_bonuses"])
            self.assertEqual(metadata["standard_checkpoints"], [2250, 2300, 2325, 2350])

            with (run_dir / "checkpoints.csv").open("r", encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle)
                self.assertEqual(next(reader), CHECKPOINT_FIELDS)

    def test_create_observer_run_refuses_duplicate_run_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            create_observer_run(root=root, run_id="observer-test")

            with self.assertRaises(FileExistsError):
                create_observer_run(root=root, run_id="observer-test")

    def test_summarize_observer_run_counts_checkpoint_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = create_observer_run(root=root, run_id="observer-test")
            with (run_dir / "checkpoints.csv").open("a", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=CHECKPOINT_FIELDS)
                writer.writerow(
                    {
                        "run_id": "observer-test",
                        "checkpoint_year": "2250",
                        "date": "2250.01.01",
                        "empire_rank": "1",
                        "empire_name": "Test Empire",
                    }
                )
                writer.writerow(
                    {
                        "run_id": "observer-test",
                        "checkpoint_year": "2250",
                        "date": "2250.01.01",
                        "empire_rank": "median",
                        "empire_name": "Middle Empire",
                    }
                )

            summary = summarize_observer_run(run_dir)

            self.assertEqual(summary["checkpoint_row_count"], 2)
            self.assertEqual(summary["checkpoint_year_counts"], {"2250": 2})
            self.assertEqual(summary["empire_rank_counts"], {"1": 1, "median": 1})
            self.assertTrue((run_dir / "summary.json").exists())
            self.assertTrue((run_dir / "summary.md").exists())

    def test_latest_observer_run_chooses_most_recent_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            older = create_observer_run(root=root, run_id="observer-old")
            newer = create_observer_run(root=root, run_id="observer-new")

            older.touch()
            newer.touch()

            self.assertEqual(latest_observer_run(root=root), newer)

    def test_extract_checkpoint_rows_filters_special_countries(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            save_path = Path(temp_dir) / "checkpoint.sav"
            gamestate = """
date="2250.01.01"
country={
  1={
    initialized=yes
    type=country
    name={ key="Alpha League" }
    economy_power=1200
    tech_power=800
    fleet_size=130
    used_naval_capacity=80
    naval_capacity=96
    num_sapient_pops=1234
    owned_megastructures={
      21 22
    }
    owned_planets={
      7 8 9
    }
    controlled_colonies={
      7 8
    }
    budget={
      current_month={
        income={
          country_base={
            energy=20
            minerals=20
            food=20
            physics_research=10
            society_research=10
            engineering_research=10
            consumer_goods=15
            alloys=5
          }
          planet_jobs={
            energy=30
            minerals=40
            food=-5
            physics_research=3
            society_research=4
            engineering_research=5
            consumer_goods=6
            alloys=7
          }
        }
      }
    }
  }
  2={
    initialized=yes
    type=10
    name={ key="Fallen Outlier" }
    economy_power=30000
    tech_power=1000000
    fleet_size=2500
    used_naval_capacity=2500
    num_sapient_pops=20000
  }
  4={
    initialized=yes
    type=10
    name={ key="Late Regularized Empire" }
    economy_power=4200
    tech_power=9000
    fleet_size=700
    used_naval_capacity=650
    num_sapient_pops=7000
  }
  3={
    initialized=yes
    type=guardian_horror
    economy_power=1
    fleet_size=250
  }
}
"""
            with zipfile.ZipFile(save_path, "w") as archive:
                archive.writestr("gamestate", gamestate)

            rows, summary = extract_checkpoint_rows_from_save(
                save_path,
                run_id="observer-test",
                checkpoint_year=2250,
                evidence_file="saves/checkpoint.sav",
            )

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["empire_name"], "Late Regularized Empire")
            self.assertEqual(rows[1]["empire_name"], "Alpha League")
            self.assertEqual(rows[1]["research"], "42")
            self.assertEqual(rows[1]["energy_income"], "50")
            self.assertEqual(rows[1]["food_income"], "15")
            self.assertEqual(rows[1]["naval_capacity_available"], "96")
            self.assertEqual(rows[1]["colonies"], "2")
            self.assertEqual(rows[1]["megastructures"], "2")
            self.assertEqual(rows[1]["deficits"], "")
            self.assertEqual(summary["eligible_regular_country_count"], 2)
            self.assertEqual(summary["excluded_special_or_outlier_countries"][0]["name"], "Fallen Outlier")
            self.assertIn("Alpha League", checkpoint_save_report_text(summary))


if __name__ == "__main__":
    unittest.main()
```

## tools/tests/test_summarize_stellaris_log.py

```python
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from summarize_stellaris_log import render_markdown, summarize_logs


class StellarisLogSummaryTests(unittest.TestCase):
    def test_groups_repeated_single_line_errors_with_volatile_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "error.log"
            path.write_text(
                "\n".join(
                    [
                        "[20:30:36][dlc.cpp:339]: Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9",
                        "[20:30:37][dlc.cpp:339]: Invalid supported_version in  file: mod/ugc_1199002146.mod line: 12",
                        "[20:30:38][asset.cpp:11]: Missing texture file: gfx/example.dds",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = summarize_logs([path], sample_limit=1)

        self.assertEqual(summary["total_entries"], 3)
        self.assertEqual(summary["group_count"], 2)
        self.assertEqual(summary["family_count"], 2)
        top_group = summary["groups"][0]
        self.assertEqual(top_group["count"], 2)
        self.assertIn("mod/ugc_<id>.mod", top_group["signature"])
        self.assertEqual(len(top_group["samples"]), 1)

    def test_groups_multiline_script_errors_and_renders_samples(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "error.log"
            path.write_text(
                "\n".join(
                    [
                        "[22:02:01][trigger_impl.cpp:1191]: Script Error: Invalid context switch",
                        "  file: common/megastructures/example.txt line: 10",
                        "  Current Scope: galactic_object",
                        "[22:02:02][trigger_impl.cpp:1191]: Script Error: Invalid context switch",
                        "  file: common/megastructures/example.txt line: 22",
                        "  Current Scope: galactic_object",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = summarize_logs([path], sample_limit=2)
            markdown = render_markdown(summary, top=5)

        self.assertEqual(summary["total_entries"], 2)
        self.assertEqual(summary["group_count"], 1)
        self.assertEqual(summary["family_count"], 1)
        self.assertIn("2x `trigger_impl.cpp:<line>`", markdown)
        self.assertIn("Current Scope: galactic_object", markdown)

    def test_families_collapse_wrong_scope_errors_across_source_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "error.log"
            path.write_text(
                "\n".join(
                    [
                        "[20:32:19][trigger.cpp:1034]: Wrong scope for trigger 'uses_ship_category' at file_a.txt:10",
                        "Current scope: ship_growth_stage",
                        "Supported Scopes: country",
                        "[20:32:19][trigger.cpp:1034]: Wrong scope for trigger 'uses_ship_category' at file_b.txt:20",
                        "Current scope: ship_growth_stage",
                        "Supported Scopes: country",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = summarize_logs([path], sample_limit=1)

        self.assertEqual(summary["group_count"], 2)
        self.assertEqual(summary["family_count"], 1)
        self.assertEqual(summary["families"][0]["count"], 2)
        self.assertEqual(summary["families"][0]["severity"], "error")


if __name__ == "__main__":
    unittest.main()
```

## tools/validate_stellar_ai_director_patch.py

```python
#!/usr/bin/env python3
"""Validate the generated Stellar AI Director patch against local sources."""

from stellar_ai_director_lib import validate_generated_patch


def main() -> None:
    errors = validate_generated_patch()
    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors))
    print("Stellar AI Director validation passed.")


if __name__ == "__main__":
    main()

```
