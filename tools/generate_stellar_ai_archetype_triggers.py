#!/usr/bin/env python3
"""Regenerate only the Stellar AI Director nation-archetype trigger artifact."""

try:
    from tools.stellar_ai_director_lib import (
        MOD_ROOT,
        archetype_triggers_text,
        write_text_file,
    )
except ModuleNotFoundError:
    from stellar_ai_director_lib import (  # type: ignore[no-redef]
        MOD_ROOT,
        archetype_triggers_text,
        write_text_file,
    )


OUTPUT_PATH = (
    MOD_ROOT
    / "common"
    / "scripted_triggers"
    / "zzzz_staid_21_nation_archetype_triggers.txt"
)


def main() -> None:
    write_text_file(OUTPUT_PATH, archetype_triggers_text())


if __name__ == "__main__":
    main()
