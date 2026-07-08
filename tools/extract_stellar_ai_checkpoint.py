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
