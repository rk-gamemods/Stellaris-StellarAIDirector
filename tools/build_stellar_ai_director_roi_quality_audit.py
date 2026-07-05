#!/usr/bin/env python3
"""Build the Stellar AI Director ROI quality audit report."""

from stellar_ai_director_lib import generate_roi_quality_audit_artifacts


def main() -> None:
    generate_roi_quality_audit_artifacts()


if __name__ == "__main__":
    main()
