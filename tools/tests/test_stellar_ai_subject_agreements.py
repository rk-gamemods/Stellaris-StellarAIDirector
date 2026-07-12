from __future__ import annotations

import sys
import unittest
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_ROOT))

from stellar_ai_director_lib import (  # noqa: E402
    IDENTITY_SUBJECT_AGREEMENT_SOURCES,
    STELLARIS_INSTALL_ROOT,
    extract_assignment_block,
    extract_top_level_object_text,
    identity_subject_agreement_object_text,
    normalize_text_file_content,
    parse_pdx,
    render_identity_subject_agreement_artifacts,
)


def without_identity_lines(text: str) -> str:
    return "\n".join(
        line
        for line in normalize_text_file_content(text).splitlines()
        if "staid_archetype_" not in line and "staid_role_" not in line
    ).rstrip() + "\n"


class IdentitySubjectAgreementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifacts = render_identity_subject_agreement_artifacts()
        cls.source_root = STELLARIS_INSTALL_ROOT / "common" / "agreement_presets"

    def test_manifest_is_exactly_four_files_and_eighteen_objects(self) -> None:
        self.assertEqual(len(self.artifacts), 4)
        self.assertEqual(
            sum(
                len(object_hashes)
                for _output, object_hashes in IDENTITY_SUBJECT_AGREEMENT_SOURCES.values()
            ),
            18,
        )
        for path, text in self.artifacts.items():
            self.assertEqual(path.parent.name, "agreement_presets")
            parse_pdx(text)

    def test_only_weight_modifiers_change_source_objects(self) -> None:
        for source_file, (output_file, object_hashes) in IDENTITY_SUBJECT_AGREEMENT_SOURCES.items():
            source_text = (self.source_root / source_file).read_text(encoding="utf-8-sig")
            rendered = next(
                text for path, text in self.artifacts.items() if path.name == output_file
            )
            for object_id in object_hashes:
                source_block = extract_top_level_object_text(source_text, object_id)
                rendered_block = extract_top_level_object_text(rendered, object_id)
                self.assertEqual(
                    without_identity_lines(rendered_block),
                    normalize_text_file_content(source_block),
                    object_id,
                )

    def test_family_role_weights_are_bounded_and_negative_subject_variants_unchanged(self) -> None:
        combined = "\n".join(self.artifacts.values())
        families = {
            "bulwark": "defensive",
            "scholarium": "research",
            "prospectorium": "gestalt_growth",
        }
        for family, archetype in families.items():
            for suffix in ("", "_nice_01", "_nice_02", "_mean_01", "_mean_02", "_mean_03"):
                object_id = f"preset_{family}{suffix}"
                block = extract_top_level_object_text(combined, object_id)
                overlord_weight = extract_assignment_block(block, "overlord_weight")
                subject_weight = extract_assignment_block(block, "subject_weight")
                self.assertEqual(
                    overlord_weight.count(f"staid_archetype_{archetype} = yes"),
                    1,
                )
                self.assertEqual(
                    overlord_weight.count(
                        f"staid_archetype_lead_secondary_{archetype} = yes"
                    ),
                    1,
                )
                self.assertEqual(
                    subject_weight.count(f"staid_archetype_{archetype} = yes"),
                    0 if "_mean_" in object_id else 1,
                )
                self.assertEqual(
                    subject_weight.count(
                        f"staid_archetype_lead_secondary_{archetype} = yes"
                    ),
                    0 if "_mean_" in object_id else 1,
                )
                self.assertNotIn("staid_role_overlord", block)
                self.assertNotIn("staid_role_subject", block)
                for line in block.splitlines():
                    if "staid_archetype_identity_conflict = no" not in line:
                        continue
                    self.assertTrue("factor = 1.15" in line or "factor = 1.05" in line)
                    for gate in (
                        "staid_archetype_identity_conflict = no",
                        "staid_archetype_eligible_country = yes",
                        "staid_basic_economy_runway_safe = yes",
                        "staid_survival_mode = no",
                        "staid_recovery_mode = no",
                        "staid_catastrophic_collapse_mode = no",
                        "staid_core_deficit_short_runway = no",
                    ):
                        self.assertIn(gate, line)

    def test_nomad_generic_contract_and_state_mutation_surfaces_are_absent(self) -> None:
        combined = "\n".join(self.artifacts.values())
        for forbidden_object in (
            "preset_vassal = {",
            "preset_subsidiary = {",
            "preset_tributary = {",
            "preset_satrapy = {",
        ):
            self.assertNotIn(forbidden_object, combined)
        for forbidden in (
            "country_event =",
            "set_country_flag =",
            "set_subject_of =",
            "set_agreement_preset =",
        ):
            self.assertNotIn(forbidden, combined)

    def test_source_hash_drift_fails_closed(self) -> None:
        source_file, (_output_file, object_hashes) = next(
            iter(IDENTITY_SUBJECT_AGREEMENT_SOURCES.items())
        )
        object_id = next(iter(object_hashes))
        source_text = (self.source_root / source_file).read_text(encoding="utf-8-sig")
        with self.assertRaisesRegex(ValueError, "Active specialist preset drifted"):
            identity_subject_agreement_object_text(source_text, object_id, "0" * 64)


if __name__ == "__main__":
    unittest.main()
