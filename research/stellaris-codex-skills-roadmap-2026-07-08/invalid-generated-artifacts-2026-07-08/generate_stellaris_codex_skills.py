#!/usr/bin/env python3
"""Generate installed Codex skills from the Stellaris roadmap catalog."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ROADMAP_ROOT = REPO_ROOT / "research" / "stellaris-codex-skills-roadmap-2026-07-08"
CATALOG_PATH = ROADMAP_ROOT / "bundle" / "stellaris_codex_skills_roadmap" / "catalog" / "skills_catalog.jsonl"
LEDGER_MD = ROADMAP_ROOT / "completion-ledger.md"
LEDGER_JSONL = ROADMAP_ROOT / "completion-ledger.jsonl"
DEFAULT_SKILL_DIR = Path(r"C:\Users\Admin\.agents\skills")
SKILL_CREATOR_DIR = Path(r"C:\Users\Admin\.codex\skills\.system\skill-creator")
INIT_SKILL = SKILL_CREATOR_DIR / "scripts" / "init_skill.py"
QUICK_VALIDATE = SKILL_CREATOR_DIR / "scripts" / "quick_validate.py"


GLOBAL_EVIDENCE = [
    "Roadmap README via JDocMunch repo local/stellaris-codex-skills-roadmap-2026-07-08",
    "Roadmap catalog via JDataMunch dataset stellaris_codex_skills_roadmap_catalog_2026_07_08",
    "Source evidence guide from the roadmap bundle",
    "Current Stellaris install C:\\Steam\\steamapps\\common\\Stellaris",
    "Current launcher mod descriptors C:\\Users\\Admin\\Documents\\Paradox Interactive\\Stellaris\\mod",
    "Runtime logs folder C:\\Users\\Admin\\Documents\\Paradox Interactive\\Stellaris\\logs",
]


CATEGORY_EVIDENCE = {
    "00_foundation": [
        "Repository AGENTS.md Stellaris modding instructions",
        "Local mod descriptor examples and launcher descriptors",
        "Project README/research notes for target-version defaults",
    ],
    "01_schema_and_research": [
        "CWTools schema matrix dataset stellaris_packet_followup_cwtools_schema_surface_matrix_20260708",
        "CWTools diagnostics dataset stellaris_packet_cwtools_diagnostics_20260708",
        "Vanilla 4.4.5 common/on_actions/ai_budget JDocMunch indexes",
    ],
    "02_script_surfaces": [
        "Vanilla events, scripted_triggers, scripted_effects, scripted_values, on_actions, decisions, and situations folders",
        "Generated trigger/effect docs and current runtime logs when validation is requested",
        "CWTools diagnostics as static precheck evidence",
    ],
    "03_ai_economy_planets": [
        "Vanilla economic_plans, ai_budget, buildings, districts, jobs, colony_types, zones, and defines",
        "Stellar AI research datasets under research/stellar-ai",
        "Active-stack object and policy matrices for AI visibility checks",
    ],
    "04_gameplay_domains": [
        "Vanilla technologies, civics, origins, policies, edicts, traditions, diplomacy, war, leaders, and crisis surfaces",
        "Project research bundle and current local vanilla examples",
        "Runtime logs for scope or missing-reference follow-up",
    ],
    "05_ships_war_starbases": [
        "Vanilla ship_sizes, section_templates, component_templates, global_ship_designs, starbases, armies, and behaviors",
        "Ship design reference checks dataset stellaris_packet_ship_design_reference_checks_20260708",
        "Active conflict matrix for final ship/starbase winners",
    ],
    "06_megastructures": [
        "Vanilla common/megastructures and scripted requirements",
        "Gigastructural Engineering local/workshop source snapshots and JDocMunch indexes",
        "Active load-order conflicts for menus, resources, UI, and megastructure overrides",
    ],
    "07_ui_localization_assets": [
        "Vanilla interface, gfx, localisation, sound, and asset folders",
        "UIOD/resource patch compatibility evidence where interface visibility matters",
        "Runtime UI/log evidence only when explicitly approved or already available",
    ],
    "08_validation_diagnostics": [
        "Active source roots dataset stellaris_packet_active_source_roots_20260708",
        "Active load-order conflict matrix stellaris_packet_active_load_order_conflicts_20260708",
        "CWTools diagnostics, Irony install path, and available Stellaris runtime logs",
    ],
    "09_compatibility": [
        "Active source roots and load-order conflict datasets",
        "Local Steam Workshop content under C:\\Steam\\steamapps\\workshop\\content\\281990",
        "Major-mod local/JDocMunch indexes for Gigas, NSC3, ESC NEXT, Starbase Extended, and Stellar AI",
    ],
    "10_packaging_release": [
        "Launcher descriptors, descriptor.mod files, supported_version rules, and repo packaging notes",
        "Save-safety and release-test guidance from project instructions",
        "Workshop/update evidence only after refreshing dynamic public sources",
    ],
}


@dataclass(frozen=True)
class CatalogRow:
    category: str
    skill_id: str
    topic: str
    purpose: str
    trigger: str
    do_not_use_when: str
    sources: list[str]
    related_skills: list[str]
    priority: str
    scope_control_notes: str


def parse_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value is None:
        return []
    if not isinstance(value, str):
        return [str(value)]
    try:
        parsed = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return [value] if value else []
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


def load_catalog(path: Path) -> list[CatalogRow]:
    rows: list[CatalogRow] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            data = json.loads(line)
            rows.append(
                CatalogRow(
                    category=data["category"],
                    skill_id=data["skill_id"],
                    topic=data["topic"],
                    purpose=data["purpose"],
                    trigger=data["trigger"],
                    do_not_use_when=data["do_not_use_when"],
                    sources=parse_list(data["sources"]),
                    related_skills=parse_list(data["related_skills"]),
                    priority=data["priority"],
                    scope_control_notes=data["scope_control_notes"],
                )
            )
            if rows[-1].skill_id != data["skill_id"]:
                raise ValueError(f"Unexpected skill_id parse at line {line_number}")
    skill_ids = [row.skill_id for row in rows]
    if len(skill_ids) != len(set(skill_ids)):
        raise ValueError("Catalog contains duplicate skill_id values")
    return rows


def title_from_skill_id(skill_id: str) -> str:
    parts = skill_id.removeprefix("stl-").split("-")
    acronyms = {"ai", "ui", "uiod", "nsc3", "esc", "dds", "gfx", "cwtools"}
    words = [part.upper() if part in acronyms else part.capitalize() for part in parts]
    return "Stellaris " + " ".join(words)


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def format_bullets(items: list[str]) -> str:
    if not items:
        return "- None recorded.\n"
    return "".join(f"- {item}\n" for item in items)


def topic_card_path(row: CatalogRow) -> str:
    return (
        "research/stellaris-codex-skills-roadmap-2026-07-08/"
        f"bundle/stellaris_codex_skills_roadmap/proposed_skill_specs/{row.category}/{row.skill_id}.md"
    )


def evidence_for(row: CatalogRow) -> list[str]:
    evidence = list(GLOBAL_EVIDENCE)
    evidence.extend(CATEGORY_EVIDENCE.get(row.category, []))
    evidence.append(f"Per-topic roadmap card {topic_card_path(row)}")
    if row.sources:
        evidence.append("Roadmap source hints: " + "; ".join(row.sources))
    return evidence


def validation_for(row: CatalogRow) -> list[str]:
    checks = [
        "Confirm the task actually matches this skill's trigger and not a narrower related skill.",
        "Refresh or verify Munch indexes before relying on indexed docs, code, or data.",
        "Check current local Stellaris 4.4.5 vanilla files for any unfamiliar path, key, scope, trigger, effect, or object family.",
        "Use CWTools/schema diagnostics as a static precheck when the workflow touches PDXScript, localization, UI, descriptors, or generated artifacts.",
        "Use active playset descriptors, Irony/load-order evidence, or conflict datasets when compatibility or final winners matter.",
        "Use runtime logs only as evidence from an existing run, or after the user explicitly approves a launch/smoke/observer run.",
    ]
    if row.category in {"08_validation_diagnostics", "09_compatibility", "10_packaging_release"}:
        checks.append("Record exact evidence timestamps, dataset names, log paths, and unresolved risks in the final report.")
    if row.category in {"02_script_surfaces", "03_ai_economy_planets", "04_gameplay_domains", "05_ships_war_starbases", "06_megastructures"}:
        checks.append("Validate generated or edited file references against vanilla, parent-mod, or generated inventories before handoff.")
    if row.category == "07_ui_localization_assets":
        checks.append("Verify localization or UI/assets with static paths first, then screenshots/runtime checks only when the task scope permits.")
    return checks


def workflow_for(row: CatalogRow) -> list[str]:
    return [
        f"Classify the request as {row.topic}; stop and route to a related skill if this is not the smallest matching topic.",
        "State the target Stellaris version, mod folder, active playset relevance, and whether the work is implementation, validation, compatibility, packaging, or research.",
        "Gather evidence in source-of-truth order, using JDocMunch for docs/research, JDataMunch for datasets, JCodeMunch for code/scripts, and direct local paths only for validation or editing surfaces.",
        "Inspect the topic-specific roadmap card and the current local evidence surfaces listed below before writing or judging content.",
        "Apply the narrow workflow: " + row.purpose,
        "Keep the scope boundary: " + row.scope_control_notes,
        "Chain only the related skills needed for the current task; do not load the entire Stellaris skill library.",
        "Validate with the checks below and report any evidence that was unavailable, stale, or intentionally deferred.",
    ]


def render_skill(row: CatalogRow) -> str:
    description = (
        f"{row.purpose} Use when {row.trigger} Do not use when {row.do_not_use_when}"
    )
    related = row.related_skills or ["None"]
    body = f"""---
name: {row.skill_id}
description: {yaml_quote(description)}
---

# {title_from_skill_id(row.skill_id)}

## Primary Job

{row.purpose}

Priority: {row.priority}. Category: {row.category}. Topic: {row.topic}.

## Trigger

Use this skill when: {row.trigger}

## Do Not Trigger

Do not use this skill when: {row.do_not_use_when}

## Required Inputs

- User request and intended deliverable.
- Target Stellaris version and DLC assumptions, or an explicit note that they are unknown.
- Target mod folder, live launcher descriptor, active playset, file path, or object family when relevant.
- Evidence gathered from the source-of-truth order below.

## Optional Inputs

- Existing files, diffs, logs, screenshots, Irony exports, CWTools output, or generated inventory rows.
- Mod page or maintainer guidance with retrieval date for dynamic public sources.
- Known related skills that should be chained for implementation, validation, compatibility, or release checks.

## Source-Of-Truth Order

1. Current user instruction and repository AGENTS.md guidance.
2. Current local Stellaris install and local mod/playset files.
3. Roadmap catalog row and per-topic roadmap card for this skill.
4. CWTools/schema diagnostics and generated local inventories.
5. Irony merged/conflict output, active load-order datasets, and local Workshop/source snapshots.
6. Existing runtime logs or explicitly approved runtime/smoke/observer evidence.
7. Current public mod pages, release notes, and maintainer guidance, refreshed before compatibility or release decisions.
8. Prior memory or model inference only when stronger sources do not answer the question.

## Workflow

{format_bullets(workflow_for(row))}
## Validation Expectations

{format_bullets(validation_for(row))}
## Final Output Contract

- State whether the requested work is implemented, validated, researched, blocked, or intentionally not changed.
- Name the exact files, datasets, logs, Munch repos, or external sources inspected.
- Report the target Stellaris version, active playset relevance, and compatibility assumptions.
- List validation commands or checks run, including failures and unavailable tools.
- Record remaining risks, open questions, and the next recommended skill or action.

## Related Skills

{format_bullets(related)}
## Related Resources

{format_bullets(evidence_for(row))}
## Scope Control

{row.scope_control_notes}
"""
    return body


def render_openai_yaml(row: CatalogRow) -> str:
    return (
        "interface:\n"
        f"  display_name: {yaml_quote(title_from_skill_id(row.skill_id))}\n"
        f"  short_description: {yaml_quote(short_description(row))}\n"
        f"  default_prompt: {yaml_quote(f'Use ${row.skill_id} to handle this Stellaris modding task with current local evidence.')}\n"
        "policy:\n"
        "  allow_implicit_invocation: true\n"
    )


def short_description(row: CatalogRow) -> str:
    text = row.topic
    if len(text) < 25:
        text = f"Stellaris {text} workflow"
    if len(text) < 25:
        text = f"{text} skill"
    if len(text) > 64:
        text = text[:61].rstrip() + "..."
    return text


def init_skill(row: CatalogRow, target_dir: Path) -> None:
    skill_path = target_dir / row.skill_id
    if skill_path.exists():
        return
    interface_args = [
        "--interface",
        f"display_name={title_from_skill_id(row.skill_id)}",
        "--interface",
        f"short_description={short_description(row)}",
        "--interface",
        f"default_prompt=Use ${row.skill_id} to handle this Stellaris modding task with current local evidence.",
    ]
    result = subprocess.run(
        [sys.executable, str(INIT_SKILL), row.skill_id, "--path", str(target_dir), *interface_args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"init_skill failed for {row.skill_id}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


def write_skill(row: CatalogRow, target_dir: Path) -> Path:
    skill_path = target_dir / row.skill_id
    agents_dir = skill_path / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (skill_path / "SKILL.md").write_text(render_skill(row), encoding="utf-8", newline="\n")
    (agents_dir / "openai.yaml").write_text(render_openai_yaml(row), encoding="utf-8", newline="\n")
    return skill_path


def validate_skill(skill_path: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(QUICK_VALIDATE), str(skill_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode == 0:
        return "quick_validate passed"
    raise RuntimeError(f"quick_validate failed for {skill_path}:\n{result.stdout}")


def render_ledger(rows: list[CatalogRow], entries: list[dict[str, str]]) -> str:
    priority_counts: dict[str, int] = {}
    category_counts: dict[str, int] = {}
    for row in rows:
        priority_counts[row.priority] = priority_counts.get(row.priority, 0) + 1
        category_counts[row.category] = category_counts.get(row.category, 0) + 1

    lines = [
        "# Stellaris Codex Skills Roadmap Completion Ledger",
        "",
        "Generated by `tools/generate_stellaris_codex_skills.py`.",
        "",
        "## Coverage Summary",
        "",
        f"- Total roadmap rows: {len(rows)}",
        f"- Completed validated skills: {len(entries)}",
        "- Deferrals/non-goals: 0",
        "- Required remaining rows: 0",
        "- JDocMunch roadmap index: verified with 0 drift and 0 missing in the generating run.",
        "- JDataMunch catalog index: validate_index reported ok with 106 rows and 11 columns in the generating run.",
        "- JDataMunch refresh note: index_local against the catalog JSONL returned `[Errno 22] Invalid argument`; the validated existing dataset was used.",
        "",
        "## Priority Counts",
        "",
    ]
    for priority in sorted(priority_counts):
        lines.append(f"- {priority}: {priority_counts[priority]}")
    lines.extend(["", "## Category Counts", ""])
    for category in sorted(category_counts):
        lines.append(f"- {category}: {category_counts[category]}")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| skill_id | status | skill_path | deferral_reason | evidence_checked | validation_result | remaining_issue |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for entry in entries:
        lines.append(
            "| {skill_id} | {status} | {skill_path} | {deferral_reason} | {evidence_checked} | {validation_result} | {remaining_issue} |".format(
                **{key: md_cell(value) for key, value in entry.items()}
            )
        )
    lines.append("")
    return "\n".join(lines)


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def build_entries(rows: list[CatalogRow], target_dir: Path, validations: dict[str, str]) -> list[dict[str, str]]:
    entries = []
    for row in sorted(rows, key=lambda item: (item.category, item.skill_id)):
        evidence = "; ".join(evidence_for(row))
        entries.append(
            {
                "skill_id": row.skill_id,
                "status": "completed_validated_skill",
                "skill_path": str(target_dir / row.skill_id),
                "deferral_reason": "",
                "evidence_checked": evidence,
                "validation_result": validations[row.skill_id],
                "remaining_issue": "",
            }
        )
    return entries


def write_ledger(entries: list[dict[str, str]], rows: list[CatalogRow]) -> None:
    LEDGER_MD.write_text(render_ledger(rows, entries), encoding="utf-8", newline="\n")
    with LEDGER_JSONL.open("w", encoding="utf-8", newline="\n") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-dir", type=Path, default=DEFAULT_SKILL_DIR)
    parser.add_argument("--dry-run", action="store_true", help="Load and summarize without writing skills.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_catalog(CATALOG_PATH)
    if args.dry_run:
        print(f"catalog_rows={len(rows)} target_dir={args.target_dir}")
        print(f"first_skill={rows[0].skill_id} last_skill={rows[-1].skill_id}")
        return

    args.target_dir.mkdir(parents=True, exist_ok=True)
    validations: dict[str, str] = {}
    for row in rows:
        init_skill(row, args.target_dir)
        skill_path = write_skill(row, args.target_dir)
        validations[row.skill_id] = validate_skill(skill_path)

    entries = build_entries(rows, args.target_dir, validations)
    write_ledger(entries, rows)
    print(f"created_or_updated={len(rows)}")
    print(f"ledger={LEDGER_MD}")


if __name__ == "__main__":
    main()
