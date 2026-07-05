#!/usr/bin/env python3
"""Build the Stellar AI Director descriptor/playset dependency audit report."""

from stellar_ai_director_lib import generate_dependency_audit_artifacts


def main() -> None:
    generate_dependency_audit_artifacts()


if __name__ == "__main__":
    main()
