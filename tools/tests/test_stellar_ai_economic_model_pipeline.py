from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import tools.simulate_stellar_ai_economy as pipeline

from tools.simulate_stellar_ai_economy import (
    ACTIVATION_MATRIX,
    ACTIVE_PRIORITY,
    COMPARATIVE_REPORT_ATTESTATION,
    COMPARATIVE_REPORT_ATTESTED_ONLY,
    COMPARATIVE_REPORT_AVAILABLE,
    COMPARATIVE_REPORT_EXPECTED_SHA256,
    CONCURRENT_FEASIBILITY,
    DEFICIT_ONLY_PLUS_ONE,
    FAILED_C9,
    LANE_STARVATION,
    LEGACY_SUMMARY_FIELDS,
    LEGACY_TIMELINE_FIELDS,
    MODEL_ACTIVATION_CASES,
    MODEL_CANDIDATES,
    MODEL_CHECKPOINTS,
    MODEL_EVIDENCE_CLASS,
    MODEL_OUTPUTS,
    MODEL_OUTPUT_SCHEMAS,
    MODEL_POLICIES,
    MODEL_PROVENANCE,
    POLICY_COUNTERFACTUAL,
    PARENT_ONLY,
    PROVENANCE_HASH_NORMALIZED_TEXT_LF,
    PROVENANCE_HASH_RAW_BYTES,
    ROOT,
    SCENARIOS,
    STRATEGIC_RECOVERY_PLAN,
    STRATEGIC_RESOURCES,
    SUMMARY,
    TIMELINE,
    build_legacy_artifact_rows,
    build_cross_priority_artifacts,
    load_comparative_report_attestation,
    load_and_validate_model_policies,
    load_model_candidates,
    load_model_checkpoints,
    model_source_provenance,
    parse_strategic_recovery_plan,
    serialize_csv_rows,
    verify_model_artifact_freshness,
    verify_optional_comparative_report,
)
from tools.stellar_ai_economic_model import Lane


def head_blob(path: Path) -> bytes:
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


class EconomicModelPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifacts, cls.provenance_id, cls.sources = build_cross_priority_artifacts()

    def test_legacy_serialized_csv_matches_current_head_blob_and_hash(self) -> None:
        timeline, summary = build_legacy_artifact_rows()
        self.assertEqual(len(timeline), 1320)
        self.assertEqual(len(summary), 10)
        for path, rows, fields in (
            (TIMELINE, timeline, LEGACY_TIMELINE_FIELDS),
            (SUMMARY, summary, LEGACY_SUMMARY_FIELDS),
        ):
            serialized = serialize_csv_rows(rows, fields)
            head = head_blob(path)
            self.assertEqual(serialized, head, path.name)
            self.assertEqual(
                hashlib.sha256(serialized).hexdigest(),
                hashlib.sha256(head).hexdigest(),
                path.name,
            )

    def test_csv_serialization_is_lf_only(self) -> None:
        payload = serialize_csv_rows(
            [{"first": "alpha", "second": "beta"}],
            ("first", "second"),
        )
        self.assertEqual(payload, b"first,second\nalpha,beta\n")
        self.assertNotIn(b"\r", payload)

    def test_internal_text_provenance_is_newline_invariant(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            lf = root / "lf.txt"
            crlf = root / "crlf.txt"
            cr = root / "cr.txt"
            lf.write_bytes(b"alpha\nbeta\n")
            crlf.write_bytes(b"alpha\r\nbeta\r\n")
            cr.write_bytes(b"alpha\rbeta\r")
            normalized_hash = hashlib.sha256(lf.read_bytes()).hexdigest()
            self.assertEqual(pipeline._sha256_normalized_text_lf(lf), normalized_hash)
            self.assertEqual(pipeline._sha256_normalized_text_lf(crlf), normalized_hash)
            self.assertEqual(pipeline._sha256_normalized_text_lf(cr), normalized_hash)
            self.assertNotEqual(pipeline._sha256(crlf), normalized_hash)

    def test_model_data_paths_have_effective_lf_git_contract(self) -> None:
        paths = (
            SCENARIOS,
            MODEL_CHECKPOINTS,
            MODEL_CANDIDATES,
            MODEL_POLICIES,
            MODEL_ACTIVATION_CASES,
            COMPARATIVE_REPORT_ATTESTATION,
            *MODEL_OUTPUTS,
            MODEL_PROVENANCE,
        )
        for path in paths:
            with self.subTest(path=path.name):
                relative = path.relative_to(ROOT).as_posix()
                result = subprocess.run(
                    ["git", "check-attr", "text", "eol", "--", relative],
                    cwd=ROOT,
                    check=True,
                    stdout=subprocess.PIPE,
                    text=True,
                ).stdout
                self.assertIn(f"{relative}: text: set", result)
                self.assertIn(f"{relative}: eol: lf", result)

    def test_strategic_recovery_plan_is_exact_and_rejects_mutations(self) -> None:
        rules = parse_strategic_recovery_plan()
        self.assertEqual(
            {rule.resource: rule.income for rule in rules},
            {resource: 1 for resource in STRATEGIC_RESOURCES},
        )
        self.assertEqual(load_and_validate_model_policies()[1], DEFICIT_ONLY_PLUS_ONE)

        source = STRATEGIC_RECOVERY_PLAN.read_text(encoding="utf-8")
        mutations = {
            "non_optional": source.replace("optional = yes", "optional = no", 1),
            "scaling": source.replace(
                "optional = yes", "optional = yes\n\t\tscaling = yes", 1
            ),
            "wrong_trigger": source.replace(
                "has_deficit = volatile_motes",
                "has_resource = volatile_motes",
                1,
            ),
            "unbounded_income": source.replace(
                "income = { volatile_motes = 1 }",
                "income = { volatile_motes = 2 }",
                1,
            ),
            "extra_key": source.replace(
                'set_name = "Stellar AI Director actual-deficit recovery - volatile motes"',
                'set_name = "Stellar AI Director actual-deficit recovery - volatile motes"\n'
                "\t\tweight = 1",
                1,
            ),
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(FileNotFoundError):
                parse_strategic_recovery_plan(root / "missing.txt")
            for label, mutated in mutations.items():
                with self.subTest(label=label):
                    path = root / f"{label}.txt"
                    path.write_text(mutated, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        parse_strategic_recovery_plan(path)

    def test_fixture_ids_and_booleans_are_strict(self) -> None:
        source = MODEL_CHECKPOINTS.read_text(encoding="utf-8")
        mutations = {
            "id": source.replace("rich_opening,", "Rich-Opening,", 1),
            "boolean": source.replace(
                ",true,report fixture rich opening empire",
                ",TRUE,report fixture rich opening empire",
                1,
            ),
        }
        with tempfile.TemporaryDirectory() as temporary:
            for label, mutated in mutations.items():
                with self.subTest(label=label):
                    path = Path(temporary) / f"{label}.csv"
                    path.write_text(mutated, encoding="utf-8", newline="")
                    with self.assertRaises(ValueError):
                        load_model_checkpoints(path)

    def test_fixtures_cover_all_lanes_and_stay_within_exact_search_limit(self) -> None:
        candidates = load_model_candidates()
        checkpoints = load_model_checkpoints()
        self.assertEqual({candidate.project.lane for candidate in candidates}, set(Lane))
        for checkpoint in checkpoints:
            legal = [candidate for candidate in candidates if candidate.scenario_id == checkpoint.scenario_id and candidate.legal]
            self.assertLessEqual(len(legal), 12, checkpoint.scenario_id)

    def test_activation_family_coverage_and_observed_unsafe_classification(self) -> None:
        rows = self.artifacts[ACTIVATION_MATRIX]
        expected_families = {
            "low_capacity_low_use",
            "positive_low_use",
            "actual_deficit",
            "market_bridge_not_earned",
            "locked_resource",
            "prezero_runway",
            "earned_recovery",
            "no_active_use",
        }
        self.assertEqual(len(rows), 120)
        self.assertEqual({row["resource"] for row in rows}, set(STRATEGIC_RESOURCES))
        for resource in STRATEGIC_RESOURCES:
            self.assertEqual(
                {row["case_family"] for row in rows if row["resource"] == resource},
                expected_families,
            )
        self.assertTrue(all(row["expectation_met"] for row in rows))
        unsafe = [row for row in rows if row["unsafe_predeficit_activation"]]
        self.assertTrue(unsafe)
        self.assertEqual({row["policy_id"] for row in unsafe}, {FAILED_C9.name})
        self.assertTrue(all(row["activation_result"] == "true" for row in unsafe))
        self.assertTrue(all(not row["actual_deficit"] for row in unsafe))
        permitted_prezero = [
            row
            for row in rows
            if row["case_family"] == "prezero_runway"
            and row["policy_id"] == "prezero-runway-plus-one"
        ]
        self.assertTrue(all(row["activation_result"] == "true" for row in permitted_prezero))
        self.assertTrue(all(not row["unsafe_predeficit_activation"] for row in permitted_prezero))
        low_use = [
            row
            for row in rows
            if row["case_family"] == "low_capacity_low_use"
            and row["policy_id"] == DEFICIT_ONLY_PLUS_ONE.name
        ]
        self.assertTrue(all(row["activation_result"] == "false" for row in low_use))
        recovered = [row for row in rows if row["case_family"] == "earned_recovery"]
        self.assertTrue(all(row["net_earned_income"] == "0" for row in recovered))
        self.assertTrue(all(row["earned_income_recovered"] for row in recovered))

    def test_required_concurrency_fixtures_select_joint_bundles(self) -> None:
        rows = self.artifacts[CONCURRENT_FEASIBILITY]
        expected = {
            ("research_gas_deficit", DEFICIT_ONLY_PLUS_ONE.name): {"research_lane", "gas_recovery_lane"},
            ("research_motes_deficit", DEFICIT_ONLY_PLUS_ONE.name): {"motes_research_lane", "motes_recovery_lane"},
            ("defense_crystals_deficit", DEFICIT_ONLY_PLUS_ONE.name): {"crystals_defense_lane", "crystals_recovery_lane"},
            ("threat_strategic_deficit", DEFICIT_ONLY_PLUS_ONE.name): {"threat_defense", "threat_hulls", "threat_gas"},
            ("influence_sharing", PARENT_ONLY.name): {"share_claim", "share_outpost"},
            ("habitat_non_veto", PARENT_ONLY.name): {"colonize_existing_habitat", "start_new_habitat"},
        }
        for key, project_ids in expected.items():
            selected = [
                row
                for row in rows
                if (row["scenario_id"], row["policy_id"]) == key and row["selected_by_policy"]
            ]
            self.assertEqual(len(selected), 1, key)
            self.assertEqual(set(str(selected[0]["project_ids"]).split("|")), project_ids)
            self.assertTrue(selected[0]["feasible"])

    def test_pending_projects_cover_full_fractional_slow_and_consumer_risk(self) -> None:
        checkpoints = {
            checkpoint.scenario_id: checkpoint for checkpoint in load_model_checkpoints()
        }
        self.assertEqual(
            checkpoints["pending_gas_full_commitment"].state.pending[0]
            .project.completion_income.get("exotic_gases"),
            Decimal("1"),
        )
        self.assertEqual(
            checkpoints["pending_gas_fractional_commitment"].state.pending[0]
            .project.completion_income.get("exotic_gases"),
            Decimal("0.5"),
        )
        self.assertEqual(
            checkpoints["pending_gas_slow_commitment"].state.pending[0]
            .completes_at_month,
            36,
        )
        self.assertEqual(
            checkpoints["pending_consumer_runway"].state.pending[0]
            .project.completion_upkeep.get("energy"),
            Decimal("10.5"),
        )

        active = {
            row["scenario_id"]: row
            for row in self.artifacts[ACTIVE_PRIORITY]
            if row["policy_id"] == DEFICIT_ONLY_PLUS_ONE.name
            and row["scenario_id"].startswith("pending_")
        }
        self.assertEqual(
            active["pending_gas_full_commitment"]["activation_reasons"],
            "committed_recovery",
        )
        self.assertEqual(active["pending_gas_full_commitment"]["activation_state"], "false")
        self.assertEqual(active["pending_gas_full_commitment"]["requested_income"], "0")
        self.assertEqual(active["pending_gas_full_commitment"]["remaining_pressure"], "0")
        self.assertEqual(
            active["pending_gas_fractional_commitment"]["activation_reasons"],
            "actual_deficit",
        )
        self.assertEqual(active["pending_gas_fractional_commitment"]["activation_state"], "true")
        self.assertEqual(active["pending_gas_fractional_commitment"]["requested_income"], "0.5")
        self.assertEqual(active["pending_gas_fractional_commitment"]["remaining_pressure"], "0.5")
        self.assertEqual(
            active["pending_gas_slow_commitment"]["activation_reasons"],
            "actual_deficit",
        )
        self.assertEqual(active["pending_gas_slow_commitment"]["activation_state"], "true")
        self.assertEqual(active["pending_gas_slow_commitment"]["requested_income"], "1")
        self.assertEqual(active["pending_gas_slow_commitment"]["remaining_pressure"], "0")
        consumer = active["pending_consumer_runway"]
        self.assertFalse(consumer["affordable_now"])
        self.assertIn('"code":"runway"', consumer["feasibility_reasons"])

    def test_no_legal_producer_is_reported_as_legality_not_more_desire(self) -> None:
        rows = [
            row
            for row in self.artifacts[ACTIVE_PRIORITY]
            if row["scenario_id"] == "no_legal_producer"
            and row["policy_id"] == DEFICIT_ONLY_PLUS_ONE.name
        ]
        blocked = next(row for row in rows if row["project_id"] == "blocked_gas_producer")
        bridge = next(row for row in rows if row["project_id"] == "native_market_bridge")
        self.assertEqual(blocked["activation_state"], "blocked_legality")
        self.assertFalse(blocked["legal"])
        self.assertTrue(bridge["legal"])

    def test_checkpoint_horizon_rejects_delayed_upkeep_outside_old_default(self) -> None:
        row = next(
            row
            for row in self.artifacts[ACTIVE_PRIORITY]
            if row["scenario_id"] == "rich_opening"
            and row["policy_id"] == PARENT_ONLY.name
            and row["project_id"] == "rich_megastructure"
        )
        self.assertEqual(row["horizon_months"], 24)
        self.assertFalse(row["affordable_now"])
        self.assertIn('"code":"runway"', row["feasibility_reasons"])

    def test_failed_c9_is_classified_unsafe_with_research_starvation(self) -> None:
        starvation = [
            row
            for row in self.artifacts[LANE_STARVATION]
            if row["scenario_id"] == "failed_c9_collateral"
            and row["policy_id"] == FAILED_C9.name
            and row["lane"] == Lane.RESEARCH.value
        ]
        self.assertTrue(starvation[0]["starved"])
        counterfactual = next(
            row
            for row in self.artifacts[POLICY_COUNTERFACTUAL]
            if row["scenario_id"] == "failed_c9_collateral"
            and row["policy_id"] == FAILED_C9.name
        )
        self.assertTrue(counterfactual["unsafe"])
        self.assertIn("cross_priority_starvation", counterfactual["unsafe_reason_codes"])

    def test_artifacts_are_labeled_as_model_evidence_not_runtime_proof(self) -> None:
        for path, rows in self.artifacts.items():
            self.assertTrue(rows)
            self.assertEqual({row["evidence_class"] for row in rows}, {MODEL_EVIDENCE_CLASS})
            self.assertEqual({row["source_provenance_id"] for row in rows}, {self.provenance_id})
            expected_fields = set(MODEL_OUTPUT_SCHEMAS[path])
            self.assertTrue(
                all(set(row) == expected_fields for row in rows),
                f"strict output schema mismatch for {path.name}",
            )
        counterfactual_fields = set(MODEL_OUTPUT_SCHEMAS[POLICY_COUNTERFACTUAL])
        for resource in STRATEGIC_RESOURCES:
            self.assertIn(f"durable_strict_positive_month_{resource}", counterfactual_fields)
            self.assertIn(f"durable_earned_recovery_month_{resource}", counterfactual_fields)
            self.assertNotIn(f"durable_positive_month_{resource}", counterfactual_fields)

    def test_checked_in_artifacts_are_byte_exact_and_current(self) -> None:
        verified_id, row_counts = verify_model_artifact_freshness()
        self.assertEqual(verified_id, self.provenance_id)
        self.assertEqual(
            row_counts,
            {
                TIMELINE.name: 1320,
                SUMMARY.name: 10,
                **{path.name: len(rows) for path, rows in self.artifacts.items()},
            },
        )

    def test_provenance_is_content_only_and_output_allowlist_cannot_touch_mod(self) -> None:
        repeated_id, repeated_sources = model_source_provenance()
        self.assertEqual(repeated_id, self.provenance_id)
        self.assertEqual(repeated_sources, self.sources)
        serialized = json.dumps(self.sources).lower()
        self.assertNotIn("timestamp", serialized)
        self.assertNotIn("git_head", serialized)
        self.assertTrue(all(path.resolve().parent == (ROOT / "research" / "stellar-ai").resolve() for path in MODEL_OUTPUTS))

    def test_external_report_attestation_is_portable_and_raw_hash_safe(self) -> None:
        attestation = load_comparative_report_attestation()
        self.assertEqual(attestation["sha256"], COMPARATIVE_REPORT_EXPECTED_SHA256)
        self.assertEqual(attestation["hash_mode"], PROVENANCE_HASH_RAW_BYTES)
        attestation_source = next(
            source
            for source in self.sources
            if source["logical_path"]
            == "research/stellar-ai/stellar-ai-director-comparative-report-attestation.json"
        )
        self.assertEqual(
            attestation_source["hash_mode"], PROVENANCE_HASH_NORMALIZED_TEXT_LF
        )
        self.assertEqual(
            {source["hash_mode"] for source in self.sources},
            {PROVENANCE_HASH_NORMALIZED_TEXT_LF},
        )
        self.assertIn(
            verify_optional_comparative_report(),
            {COMPARATIVE_REPORT_AVAILABLE, COMPARATIVE_REPORT_ATTESTED_ONLY},
        )
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing.md"
            with patch.object(pipeline, "COMPARATIVE_REPORT", missing):
                self.assertEqual(
                    verify_optional_comparative_report(),
                    COMPARATIVE_REPORT_ATTESTED_ONLY,
                )
                missing_id, missing_sources = model_source_provenance()
                self.assertEqual(missing_id, self.provenance_id)
                self.assertEqual(missing_sources, self.sources)
                legacy_timeline, legacy_summary = build_legacy_artifact_rows()
                verified_id, _ = verify_model_artifact_freshness(
                    legacy_timeline,
                    legacy_summary,
                    self.artifacts,
                )
                self.assertEqual(verified_id, self.provenance_id)
            changed = Path(temporary) / "changed.md"
            changed.write_text("changed comparative report", encoding="utf-8")
            with patch.object(pipeline, "COMPARATIVE_REPORT", changed):
                with self.assertRaisesRegex(ValueError, "hash mismatch"):
                    verify_optional_comparative_report()
                with self.assertRaisesRegex(ValueError, "hash mismatch"):
                    model_source_provenance()


if __name__ == "__main__":
    unittest.main()
