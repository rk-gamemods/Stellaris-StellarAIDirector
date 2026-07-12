#!/usr/bin/env python3
"""Regenerate only the Stellar AI Director native army-budget artifact."""

try:
    from tools.stellar_ai_director_lib import (
        MOD_ROOT,
        army_recruitment_budget_text,
        write_text_file,
    )
except ModuleNotFoundError:
    from stellar_ai_director_lib import (  # type: ignore[no-redef]
        MOD_ROOT,
        army_recruitment_budget_text,
        write_text_file,
    )


OUTPUT_PATH = (
    MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_army_recruitment_budget.txt"
)


def main() -> None:
    write_text_file(OUTPUT_PATH, army_recruitment_budget_text())


if __name__ == "__main__":
    main()
