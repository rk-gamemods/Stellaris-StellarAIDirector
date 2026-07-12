#!/usr/bin/env python3
"""Regenerate only the fleet-economy model, trigger, and alloy-budget surfaces."""

from __future__ import annotations

import json

from stellar_ai_director_lib import (
    DECISION_STATE_TRIGGER_PATH,
    FLEET_ALLOY_BUDGET_PATH,
    ai_budget_text,
    render_core_ai_artifacts,
    write_text_file,
)
from stellar_ai_fleet_economy_model import REPORT_PATH, build_report


def main() -> int:
    core = render_core_ai_artifacts()
    write_text_file(DECISION_STATE_TRIGGER_PATH, core[DECISION_STATE_TRIGGER_PATH])
    write_text_file(FLEET_ALLOY_BUDGET_PATH, ai_budget_text({}))
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(build_report(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(DECISION_STATE_TRIGGER_PATH)
    print(FLEET_ALLOY_BUDGET_PATH)
    print(REPORT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
