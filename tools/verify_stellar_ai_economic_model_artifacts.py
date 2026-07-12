"""Fail unless every checked-in Stellar AI economic-model artifact is current."""

from __future__ import annotations

from simulate_stellar_ai_economy import (
    verify_model_artifact_freshness,
    verify_optional_comparative_report,
)


def main() -> int:
    external_report_status = verify_optional_comparative_report()
    provenance_id, row_counts = verify_model_artifact_freshness()
    print(
        f"Economic-model artifacts are byte-exact/current: "
        f"provenance={provenance_id}; rows={sum(row_counts.values())}; "
        f"external_report={external_report_status}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
