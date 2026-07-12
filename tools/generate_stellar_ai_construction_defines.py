#!/usr/bin/env python3
"""Regenerate only the Stellar AI Director construction-define artifact."""

try:
    from tools.stellar_ai_director_lib import (
        MOD_ROOT,
        high_scale_ai_defines_text,
        write_text_file,
    )
except ModuleNotFoundError:
    from stellar_ai_director_lib import (  # type: ignore[no-redef]
        MOD_ROOT,
        high_scale_ai_defines_text,
        write_text_file,
    )


OUTPUT_PATH = (
    MOD_ROOT / "common" / "defines" / "zzzz_staid_14_high_scale_ai_defines.txt"
)


def main() -> None:
    write_text_file(OUTPUT_PATH, high_scale_ai_defines_text())


if __name__ == "__main__":
    main()
