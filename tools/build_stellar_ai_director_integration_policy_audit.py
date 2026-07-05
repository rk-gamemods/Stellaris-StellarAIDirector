#!/usr/bin/env python3
"""Build the Stellar AI Director integration policy readiness audit."""

from stellar_ai_director_lib import generate_integration_policy_audit_artifacts


def main() -> None:
    generate_integration_policy_audit_artifacts()


if __name__ == "__main__":
    main()
