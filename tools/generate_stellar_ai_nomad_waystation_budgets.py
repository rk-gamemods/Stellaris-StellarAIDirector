#!/usr/bin/env python3
"""Regenerate only the Stellar AI Director Nomad Waystation budget artifact."""

try:
    from tools.stellar_ai_director_lib import (
        MOD_ROOT,
        nomad_waystation_budget_text,
        write_text_file,
    )
except ModuleNotFoundError:
    from stellar_ai_director_lib import (  # type: ignore[no-redef]
        MOD_ROOT,
        nomad_waystation_budget_text,
        write_text_file,
    )


OUTPUT_PATH = (
    MOD_ROOT
    / "common"
    / "ai_budget"
    / "zzzzz_staid_22_nomad_waystation_budgets.txt"
)


def main() -> None:
    write_text_file(OUTPUT_PATH, nomad_waystation_budget_text())


if __name__ == "__main__":
    main()
