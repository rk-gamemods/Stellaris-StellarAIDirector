#!/usr/bin/env python3
"""Validate the generated Stellar AI Director patch against local sources."""

from stellar_ai_director_lib import validate_generated_patch


def main() -> None:
    errors = validate_generated_patch()
    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors))
    print("Stellar AI Director validation passed.")


if __name__ == "__main__":
    main()
