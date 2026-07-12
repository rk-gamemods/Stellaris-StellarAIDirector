#!/usr/bin/env python3
"""Regenerate only the Stellar AI Director economic-plan artifact."""

try:
    from tools.stellar_ai_director_lib import MOD_ROOT, economic_plan_text, write_text_file
except ModuleNotFoundError:
    from stellar_ai_director_lib import (  # type: ignore[no-redef]
        MOD_ROOT,
        economic_plan_text,
        write_text_file,
    )


OUTPUT_PATH = (
    MOD_ROOT
    / "common"
    / "economic_plans"
    / "zzzz_staid_additive_economic_plan.txt"
)


def main() -> None:
    write_text_file(OUTPUT_PATH, economic_plan_text())


if __name__ == "__main__":
    main()
