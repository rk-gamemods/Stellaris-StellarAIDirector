from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Iterator


SUPPORTED_SUFFIXES = {".csv", ".tsv", ".json", ".jsonl", ".ndjson"}
NULL_TEXT = {"", "null", "none", "na", "n/a"}
BOOLEAN_TEXT = {"true", "false", "yes", "no"}
INTEGER_RE = re.compile(r"^[+-]?\d+$")
REAL_RE = re.compile(r"^[+-]?(?:\d+\.\d*|\d*\.\d+)(?:[eE][+-]?\d+)?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}")


@dataclass
class ColumnProfile:
    name: str
    observed_types: set[str] = field(default_factory=set)
    nullable: bool = False
    candidate_values: set[str] | None = None
    candidate_overflow: bool = False

    def observe(self, value: Any, *, track_unique_limit: int = 200_000) -> None:
        if value is None or (isinstance(value, str) and value.strip().lower() in NULL_TEXT):
            self.nullable = True
            return
        self.observed_types.add(value_type(value))
        if self.candidate_values is not None and not self.candidate_overflow:
            normalized = stable_text(value)
            if len(self.candidate_values) >= track_unique_limit and normalized not in self.candidate_values:
                self.candidate_overflow = True
                self.candidate_values = None
            else:
                self.candidate_values.add(normalized)

    @property
    def logical_type(self) -> str:
        types = self.observed_types
        if not types:
            return "unknown"
        if types <= {"boolean"}:
            return "boolean"
        if types <= {"integer"}:
            return "integer"
        if types <= {"integer", "real"}:
            return "real"
        if types <= {"date"}:
            return "date"
        if types <= {"date", "timestamp"}:
            return "timestamp"
        if types <= {"json"}:
            return "json"
        if types <= {"path"}:
            return "path"
        if types <= {"identifier"}:
            return "identifier"
        if types <= {"expression"}:
            return "expression"
        return "text"


@dataclass
class DatasetProfile:
    format_code: str
    row_count: int
    columns: list[ColumnProfile]
    delimiter: str | None
    has_header: bool
    stable_key_columns: list[str]
    notes: list[str] = field(default_factory=list)

    @property
    def schema_hash(self) -> str:
        payload = [
            {
                "ordinal": index,
                "name": column.name,
                "logical_type": column.logical_type,
                "nullable": column.nullable,
            }
            for index, column in enumerate(self.columns, start=1)
        ]
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()


def stable_text(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return str(value).strip()


def value_type(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "real"
    if isinstance(value, (dict, list)):
        return "json"
    text = str(value).strip()
    lowered = text.lower()
    if lowered in BOOLEAN_TEXT:
        return "boolean"
    if INTEGER_RE.fullmatch(text):
        return "integer"
    if REAL_RE.fullmatch(text):
        return "real"
    if TIMESTAMP_RE.match(text):
        try:
            datetime.fromisoformat(text.replace("Z", "+00:00"))
            return "timestamp"
        except ValueError:
            pass
    if DATE_RE.fullmatch(text):
        return "date"
    if ("/" in text or "\\" in text) and len(text) < 1024:
        return "path"
    if any(marker in text for marker in ("=", "{", "}", "factor", "weight")) and len(text) < 2048:
        return "expression"
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.:-]*", text):
        return "identifier"
    return "text"


def semantic_role(name: str, logical_type: str) -> str:
    lowered = name.lower()
    if lowered in {"id", "key", "name"} or lowered.endswith(("_id", "_key")):
        return "identifier"
    if any(token in lowered for token in ("path", "file", "uri", "url", "line", "row", "column")):
        return "locator"
    if any(token in lowered for token in ("status", "state", "result", "outcome", "valid")):
        return "status"
    if any(token in lowered for token in ("source", "hash", "commit", "version", "captured", "observed")):
        return "provenance"
    if lowered.endswith("_count") or lowered in {"count", "rows", "columns"}:
        return "count"
    if logical_type in {"integer", "real", "boolean"}:
        return "metric"
    if logical_type == "expression":
        return "expression"
    if any(token in lowered for token in ("type", "kind", "category", "group", "scenario", "resource")):
        return "dimension"
    return "text"


def _candidate_column(name: str) -> bool:
    lowered = name.lower()
    return lowered in {"id", "key", "name", "object_id", "record_key"} or lowered.endswith(
        ("_id", "_key")
    )


def _decode_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", raw, 0, 1, f"No supported text encoding for {path}")


def _profile_rows(
    rows: Iterable[dict[str, Any]],
    field_names: list[str] | None = None,
) -> tuple[int, list[ColumnProfile]]:
    profiles: dict[str, ColumnProfile] = {}
    order: list[str] = []
    if field_names:
        for name in field_names:
            order.append(name)
            profiles[name] = ColumnProfile(
                name=name,
                candidate_values=set() if _candidate_column(name) else None,
            )
    row_count = 0
    for row in rows:
        row_count += 1
        for name in row:
            if name not in profiles:
                order.append(name)
                profiles[name] = ColumnProfile(
                    name=name,
                    candidate_values=set() if _candidate_column(name) else None,
                )
        for name in order:
            profiles[name].observe(row.get(name))
    return row_count, [profiles[name] for name in order]


def _csv_rows(text: str, delimiter: str) -> tuple[list[str], Iterator[dict[str, Any]]]:
    lines = text.splitlines()
    reader = csv.DictReader(lines, delimiter=delimiter)
    names = [name if name is not None else "" for name in (reader.fieldnames or [])]
    if not names or any(not name for name in names):
        raise ValueError("Structured file has a missing or blank header name.")
    if len(set(names)) != len(names):
        raise ValueError("Structured file has duplicate header names.")
    return names, iter(reader)


def _json_records(value: Any) -> tuple[list[dict[str, Any]], list[str]]:
    notes: list[str] = []
    if isinstance(value, list):
        if all(isinstance(row, dict) for row in value):
            return list(value), notes
        return [{"value": item} for item in value], ["Top-level list was not object-shaped."]
    if isinstance(value, dict):
        if value and all(isinstance(row, dict) for row in value.values()):
            rows = []
            for record_key, row in value.items():
                expanded = {"_record_key": record_key}
                expanded.update(row)
                rows.append(expanded)
            notes.append("Top-level mapping-of-records was normalized with _record_key.")
            return rows, notes
        return [value], notes
    return [{"value": value}], ["Top-level scalar was normalized to a value column."]


def profile_structured_file(path: Path) -> DatasetProfile:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported structured format: {path.suffix}")
    text, encoding = _decode_text(path)
    notes = [f"Decoded as {encoding}."]
    if suffix in {".csv", ".tsv"}:
        delimiter = "," if suffix == ".csv" else "\t"
        names, rows = _csv_rows(text, delimiter)
        row_count, columns = _profile_rows(rows, names)
        format_code = "csv" if suffix == ".csv" else "tsv"
    elif suffix in {".jsonl", ".ndjson"}:
        parsed_rows: list[dict[str, Any]] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                value = {"value": value}
            value = {"_line_number": line_number, **value}
            parsed_rows.append(value)
        row_count, columns = _profile_rows(parsed_rows)
        delimiter = None
        format_code = "jsonl"
    else:
        records, json_notes = _json_records(json.loads(text))
        notes.extend(json_notes)
        row_count, columns = _profile_rows(records)
        delimiter = None
        format_code = "json"
    stable_keys = [
        column.name
        for column in columns
        if column.candidate_values is not None
        and not column.candidate_overflow
        and not column.nullable
        and row_count > 0
        and len(column.candidate_values) == row_count
    ][:3]
    if not stable_keys:
        notes.append("No unique deterministic key column was inferred; use row-number locators.")
    return DatasetProfile(
        format_code=format_code,
        row_count=row_count,
        columns=columns,
        delimiter=delimiter,
        has_header=True,
        stable_key_columns=stable_keys,
        notes=notes,
    )
