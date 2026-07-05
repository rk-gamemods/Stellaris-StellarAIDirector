#!/usr/bin/env python3
"""Build the Stellar AI Director generated-reference audit report."""

from stellar_ai_director_lib import generate_reference_audit_artifacts


def main() -> None:
    generate_reference_audit_artifacts()


if __name__ == "__main__":
    main()
