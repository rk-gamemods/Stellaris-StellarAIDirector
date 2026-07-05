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
