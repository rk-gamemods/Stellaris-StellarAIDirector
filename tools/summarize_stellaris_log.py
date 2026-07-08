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
