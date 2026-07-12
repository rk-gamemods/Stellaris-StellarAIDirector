from __future__ import annotations

import csv
import inspect
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import generate_stellar_ai_archetype_triggers as dedicated_generator
from tools.stellar_ai_director_lib import (
    PDXAssignment,
    PDXAtom,
    PDXBlock,
    archetype_triggers_text,
    block_assignments,
    generate_mod_files,
    iter_assignments,
    parse_pdx,
)
from tools.stellar_ai_archetype_triggers import (
    _evidence_assignments,
    render_archetype_triggers,
)
from tools.stellar_ai_nation_model import (
    ARCHETYPE_PRECEDENCE,
    OUTSIDE_PRIMARY_PERSONALITIES,
    PEGASUS_444_PERSONALITY_SHA256,
    PRIMARY_PERSONALITY_GROUPS,
    REVIEWED_444_PERSONALITY_IDS,
    Archetype,
    ClassificationStatus,
    EvidenceStrength,
    NationIdentity,
    PersonalitySource,
    ResolvedPersonalityProfile,
    TriState,
    classify_nation,
)


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = (
    ROOT
    / "mods"
    / "StellarAIDirector"
    / "common"
    / "scripted_triggers"
    / "zzzz_staid_21_nation_archetype_triggers.txt"
)
ARCHETYPE_CASES = (
    ROOT / "research" / "stellar-ai" / "stellar-ai-director-nation-archetype-cases.csv"
)
PRIMARY_ARCHETYPES = tuple(
    archetype
    for archetype in ARCHETYPE_PRECEDENCE
    if archetype is not Archetype.BALANCED
)
PRIMARY_TRIGGER_NAMES = tuple(
    f"staid_archetype_{archetype.value}" for archetype in ARCHETYPE_PRECEDENCE
)


def atom_value(assignment: PDXAssignment) -> str:
    if not isinstance(assignment.value, PDXAtom):
        raise AssertionError(f"expected scalar assignment for {assignment.key}")
    return assignment.value.value


def _tokens(value: str | None) -> tuple[str, ...]:
    return tuple(token for token in (value or "").split("|") if token)


def _optional(value: str | None) -> str | None:
    return value or None


def _identity_from_row(row: dict[str, str]) -> NationIdentity:
    behaviors = _tokens(row.get("behaviors"))
    personality = None
    if behaviors:
        personality = ResolvedPersonalityProfile(
            behaviors=behaviors,
            source=PersonalitySource(row["personality_source"]),
            source_ref=row["source_ref"],
        )
    return NationIdentity(
        country_type=row["country_type"],
        personality_id=_optional(row.get("personality_id")),
        ethics=_tokens(row.get("ethics")),
        civics=_tokens(row.get("civics")),
        ascension_perks=_tokens(row.get("ascension_perks")),
        authority=_optional(row.get("authority")),
        government=_optional(row.get("government")),
        origin=_optional(row.get("origin")),
        is_nomadic=TriState(row["is_nomadic"]),
        is_wilderness=TriState(row["is_wilderness"]),
        personality=personality,
    )


class _TriggerEvaluator:
    """Evaluate the generated identity-only subset against one H08a identity."""

    def __init__(self, top: dict[str, PDXAtom | PDXBlock], identity: NationIdentity):
        self.top = top
        self.identity = identity
        self.cache: dict[str, bool] = {}

    def trigger(self, name: str) -> bool:
        if name not in self.cache:
            value = self.top[name]
            if not isinstance(value, PDXBlock):
                raise AssertionError(f"expected trigger block for {name}")
            self.cache[name] = self.block(value)
        return self.cache[name]

    def block(self, block: PDXBlock) -> bool:
        return all(
            self.assignment(assignment) for assignment in block_assignments(block)
        )

    def assignment(self, assignment: PDXAssignment) -> bool:
        if assignment.key == "calc_true_if":
            if not isinstance(assignment.value, PDXBlock):
                raise AssertionError("expected calc_true_if block")
            items = assignment.value.items
            if len(items) < 3 or not all(
                isinstance(item, PDXAtom) for item in items[:3]
            ):
                raise AssertionError("malformed calc_true_if amount clause")
            amount_key, comparator, amount_value = (
                item.value for item in items[:3] if isinstance(item, PDXAtom)
            )
            if amount_key != "amount" or comparator != ">=":
                raise AssertionError("unsupported calc_true_if comparator")
            conditions = items[3:]
            if not all(isinstance(item, PDXAssignment) for item in conditions):
                raise AssertionError("calc_true_if conditions must be assignments")
            true_count = sum(
                self.assignment(item)
                for item in conditions
                if isinstance(item, PDXAssignment)
            )
            return true_count >= int(amount_value)

        if assignment.key in {"OR", "AND", "NOR", "NOT"}:
            if not isinstance(assignment.value, PDXBlock):
                raise AssertionError(f"expected block for {assignment.key}")
            values = [
                self.assignment(child) for child in block_assignments(assignment.value)
            ]
            if assignment.key == "OR":
                return any(values)
            if assignment.key == "AND":
                return all(values)
            if assignment.key == "NOR":
                return not any(values)
            return not all(values)

        expected = atom_value(assignment)
        if assignment.key in self.top:
            return self.trigger(assignment.key) is (expected == "yes")
        actual = self.predicate(assignment.key, expected)
        return actual

    def predicate(self, key: str, expected: str) -> bool:
        identity = self.identity
        if key == "always":
            return expected == "yes"
        if key == "is_country_type":
            return identity.country_type == expected
        if key == "is_nomadic":
            actual = identity.is_nomadic is TriState.TRUE
            return actual is (expected == "yes")
        if key == "is_wilderness_empire":
            actual = identity.is_wilderness is TriState.TRUE
            return actual is (expected == "yes")
        if key == "has_ai_personality":
            return identity.personality_id == expected
        if key == "has_ethic":
            return expected in identity.ethics
        if key == "has_valid_civic":
            return expected in identity.civics
        if key == "has_ascension_perk":
            return expected in identity.ascension_perks
        if key == "has_authority":
            return identity.authority == expected
        if key == "has_government":
            return identity.government == expected
        if key == "has_origin":
            return identity.origin == expected
        if key == "has_ai_personality_behaviour":
            behaviors = identity.personality.behaviors if identity.personality else ()
            return expected in behaviors
        raise AssertionError(f"unsupported identity predicate: {key} = {expected}")


class StellarAiArchetypeTriggerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rendered = archetype_triggers_text()
        cls.artifact_text = ARTIFACT.read_text(encoding="utf-8")
        cls.root = parse_pdx(cls.artifact_text)
        cls.top_assignments = block_assignments(cls.root)
        cls.top = {
            assignment.key: assignment.value for assignment in cls.top_assignments
        }

    def test_artifact_is_parseable_and_byte_equivalent_to_renderer(self) -> None:
        self.assertEqual(self.artifact_text, self.rendered)
        self.assertEqual(
            self.artifact_text.count(PEGASUS_444_PERSONALITY_SHA256),
            1,
        )

    def test_top_level_trigger_ids_are_unique_and_seven_primaries_exist(self) -> None:
        keys = [assignment.key for assignment in self.top_assignments]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len(PRIMARY_TRIGGER_NAMES), 7)
        self.assertTrue(set(PRIMARY_TRIGGER_NAMES).issubset(keys))

    def test_personality_groups_match_model_and_cover_reviewed_source(self) -> None:
        rendered_personalities: set[str] = set()
        for archetype in PRIMARY_ARCHETYPES:
            block = self.top[f"staid_archetype_hard_{archetype.value}"]
            self.assertIsInstance(block, PDXBlock)
            ids = {
                atom_value(assignment)
                for assignment in iter_assignments(block)
                if assignment.key == "has_ai_personality"
            }
            self.assertEqual(ids, set(PRIMARY_PERSONALITY_GROUPS[archetype]))
            rendered_personalities.update(ids)

        self.assertEqual(
            rendered_personalities | set(OUTSIDE_PRIMARY_PERSONALITIES),
            set(REVIEWED_444_PERSONALITY_IDS),
        )
        self.assertTrue(
            rendered_personalities.isdisjoint(OUTSIDE_PRIMARY_PERSONALITIES)
        )

    def test_hard_conflict_counts_distinct_hard_archetypes_once(self) -> None:
        conflict = self.top["staid_archetype_identity_conflict"]
        self.assertIsInstance(conflict, PDXBlock)
        calc_assignments = block_assignments(conflict, "calc_true_if")
        self.assertEqual(len(calc_assignments), 1)
        calc = calc_assignments[0].value
        self.assertIsInstance(calc, PDXBlock)
        amount_tokens = [
            item.value for item in calc.items[:3] if isinstance(item, PDXAtom)
        ]
        self.assertEqual(amount_tokens, ["amount", ">=", "2"])
        hard_names = tuple(
            f"staid_archetype_hard_{archetype.value}"
            for archetype in PRIMARY_ARCHETYPES
        )
        references = block_assignments(calc)
        self.assertEqual([reference.key for reference in references], list(hard_names))
        self.assertTrue(all(atom_value(reference) == "yes" for reference in references))

    def test_public_primaries_reference_only_the_exact_winner_candidate(self) -> None:
        for archetype in PRIMARY_ARCHETYPES:
            name = f"staid_archetype_{archetype.value}"
            block = self.top[name]
            self.assertIsInstance(block, PDXBlock)
            eligible = block_assignments(block, "staid_archetype_eligible_country")
            conflict = block_assignments(block, "staid_archetype_identity_conflict")
            self.assertEqual(len(eligible), 1)
            self.assertEqual(len(conflict), 1)
            self.assertEqual(atom_value(eligible[0]), "yes")
            self.assertEqual(atom_value(conflict[0]), "no")
            candidate = f"staid_archetype_candidate_{archetype.value}"
            selected = block_assignments(block, candidate)
            self.assertEqual(len(selected), 1)
            self.assertEqual(atom_value(selected[0]), "yes")
            assignments = block_assignments(block)
            self.assertEqual(
                [assignment.key for assignment in assignments],
                [
                    "staid_archetype_eligible_country",
                    "staid_archetype_identity_conflict",
                    candidate,
                ],
            )

    def test_balanced_is_eligible_fail_closed_fallback(self) -> None:
        balanced = self.top["staid_archetype_balanced"]
        self.assertIsInstance(balanced, PDXBlock)
        assignments = block_assignments(balanced)
        eligible = block_assignments(balanced, "staid_archetype_eligible_country")
        self.assertEqual(len(eligible), 1)
        self.assertEqual(atom_value(eligible[0]), "yes")
        nor_assignment = block_assignments(balanced, "NOR")
        self.assertEqual(len(nor_assignment), 1)
        self.assertIsInstance(nor_assignment[0].value, PDXBlock)
        exclusions = block_assignments(nor_assignment[0].value)
        excluded = {assignment.key for assignment in exclusions}
        self.assertEqual(excluded, set(PRIMARY_TRIGGER_NAMES[:-1]))
        self.assertEqual(len(exclusions), len(PRIMARY_TRIGGER_NAMES) - 1)
        self.assertTrue(all(atom_value(exclusion) == "yes" for exclusion in exclusions))
        self.assertEqual(len(assignments), 2)

    def selected_primary(self, identity: NationIdentity) -> Archetype | None:
        evaluator = _TriggerEvaluator(self.top, identity)
        selected = [
            archetype
            for archetype in ARCHETYPE_PRECEDENCE
            if evaluator.trigger(f"staid_archetype_{archetype.value}")
        ]
        self.assertLessEqual(len(selected), 1, identity)
        return selected[0] if selected else None

    def assert_model_primary_parity(self, identity: NationIdentity) -> None:
        classification = classify_nation(identity)
        if classification.status is ClassificationStatus.EXCLUDED:
            expected = None
        elif classification.status is ClassificationStatus.CONFLICT:
            expected = Archetype.BALANCED
        else:
            expected = classification.primary
        self.assertEqual(self.selected_primary(identity), expected, identity)

    def test_all_h08a_identity_fixtures_select_the_same_neutralized_primary(
        self,
    ) -> None:
        with ARCHETYPE_CASES.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 30)
        for row in rows:
            with self.subTest(case_id=row["case_id"]):
                self.assert_model_primary_parity(_identity_from_row(row))

    def test_adversarial_mixed_strength_identities_match_h08a_ranking(self) -> None:
        cases = {
            "strong_beats_earlier_supporting": NationIdentity(
                ethics=("ethic_fanatic_militarist",),
                personality=ResolvedPersonalityProfile(behaviors=("purger",)),
            ),
            "two_strong_beat_one_earlier_strong": NationIdentity(
                ethics=("ethic_pacifist", "ethic_fanatic_materialist"),
                civics=("civic_technocracy",),
            ),
            "supporting_breaks_equal_strong_toward_later": NationIdentity(
                ethics=("ethic_militarist",),
                civics=(
                    "civic_technocracy",
                    "civic_distinguished_admiralty",
                ),
            ),
            "precedence_breaks_exact_tier_tie": NationIdentity(
                civics=(
                    "civic_technocracy",
                    "civic_distinguished_admiralty",
                ),
            ),
            "multiple_supporting_beat_earlier_single_support": NationIdentity(
                personality=ResolvedPersonalityProfile(
                    behaviors=("liberator", "dominator", "propagator")
                ),
            ),
            "multiple_diplomatic_support_beat_later_single_support": NationIdentity(
                personality=ResolvedPersonalityProfile(
                    behaviors=("liberator", "uplifter", "dominator")
                ),
            ),
            "gestalt_count_beats_defensive_count": NationIdentity(
                ethics=("ethic_gestalt_consciousness", "ethic_pacifist"),
                authority="auth_hive_mind",
            ),
            "hard_overrides_many_strong": NationIdentity(
                ethics=(
                    "ethic_fanatic_pacifist",
                    "ethic_fanatic_militarist",
                    "ethic_fanatic_authoritarian",
                ),
                civics=(
                    "civic_distinguished_admiralty",
                    "civic_nationalistic_zeal",
                    "civic_barbaric_despoilers",
                ),
                origin="origin_hegemon",
            ),
            "hard_conflict_fails_neutral": NationIdentity(
                civics=("civic_fanatic_purifiers", "civic_inwards_perfection")
            ),
            "unknown_identity_falls_back_neutral": NationIdentity(),
            "nomadic_hard_identity_is_excluded": NationIdentity(
                personality_id="fanatic_purifiers",
                is_nomadic=TriState.TRUE,
            ),
            "diplomatic_origin_signal": NationIdentity(origin="origin_common_ground"),
            "conquest_origin_signal": NationIdentity(origin="origin_hegemon"),
        }
        for name, identity in cases.items():
            with self.subTest(case=name):
                self.assert_model_primary_parity(identity)

    def test_trigger_graph_is_acyclic_and_has_bounded_depth(self) -> None:
        names = set(self.top)
        graph = {
            name: {
                assignment.key
                for assignment in iter_assignments(block)
                if assignment.key in names
            }
            for name, block in self.top.items()
        }
        for name, references in graph.items():
            self.assertNotIn(name, references)

        depths: dict[str, int] = {}

        def depth(name: str, trail: tuple[str, ...] = ()) -> int:
            if name in trail:
                self.fail(
                    "cyclic archetype trigger graph: " + " -> ".join((*trail, name))
                )
            if name not in depths:
                depths[name] = 1 + max(
                    (depth(child, (*trail, name)) for child in graph[name]),
                    default=0,
                )
            return depths[name]

        self.assertLessEqual(max(depth(name) for name in graph), 5)

    def test_count_circuit_shape_and_reference_polarity_are_exact(self) -> None:
        evidence = _evidence_assignments(PRIMARY_ARCHETYPES)
        expected_thresholds = {
            f"staid_archetype_{strength.value}_{archetype.value}_at_least_{count}"
            for archetype in PRIMARY_ARCHETYPES
            for strength in (EvidenceStrength.STRONG, EvidenceStrength.SUPPORTING)
            for count in range(1, len(evidence[(archetype, strength)]) + 1)
        }
        actual_thresholds = {
            name
            for name in self.top
            if re.fullmatch(
                r"staid_archetype_(?:strong|supporting)_.+_at_least_\d+", name
            )
        }
        self.assertEqual(actual_thresholds, expected_thresholds)

        for archetype in PRIMARY_ARCHETYPES:
            for strength in (
                EvidenceStrength.STRONG,
                EvidenceStrength.SUPPORTING,
            ):
                markers = evidence[(archetype, strength)]
                for count in range(1, len(markers) + 1):
                    name = (
                        f"staid_archetype_{strength.value}_{archetype.value}"
                        f"_at_least_{count}"
                    )
                    threshold = self.top[name]
                    self.assertIsInstance(threshold, PDXBlock)
                    calc_assignments = block_assignments(threshold, "calc_true_if")
                    self.assertEqual(len(calc_assignments), 1)
                    calc = calc_assignments[0].value
                    self.assertIsInstance(calc, PDXBlock)
                    amount_tokens = [
                        item.value
                        for item in calc.items[:3]
                        if isinstance(item, PDXAtom)
                    ]
                    self.assertEqual(amount_tokens, ["amount", ">=", str(count)])
                    conditions = block_assignments(calc)
                    rendered_conditions = [
                        f"{condition.key} = {atom_value(condition)}"
                        for condition in conditions
                    ]
                    self.assertEqual(rendered_conditions, list(markers))

        expected_ge = {
            f"staid_archetype_{strength.value}_{left.value}_ge_{right.value}"
            for strength in (EvidenceStrength.STRONG, EvidenceStrength.SUPPORTING)
            for left in PRIMARY_ARCHETYPES
            for right in PRIMARY_ARCHETYPES
            if left is not right
        }
        actual_ge = {
            name
            for name in self.top
            if re.fullmatch(r"staid_archetype_(?:strong|supporting)_.+_ge_.+", name)
        }
        self.assertEqual(actual_ge, expected_ge)

        for name in expected_ge:
            block = self.top[name]
            self.assertIsInstance(block, PDXBlock)
            for reference in iter_assignments(block):
                if reference.key in self.top:
                    self.assertIn(reference.key, expected_thresholds)
                    self.assertIn(atom_value(reference), {"yes", "no"})

        any_hard = self.top["staid_archetype_any_hard"]
        self.assertIsInstance(any_hard, PDXBlock)
        hard_references = [
            assignment
            for assignment in iter_assignments(any_hard)
            if assignment.key.startswith("staid_archetype_hard_")
        ]
        self.assertEqual(
            {assignment.key for assignment in hard_references},
            {
                f"staid_archetype_hard_{archetype.value}"
                for archetype in PRIMARY_ARCHETYPES
            },
        )
        self.assertTrue(
            all(atom_value(reference) == "yes" for reference in hard_references)
        )

        for archetype in PRIMARY_ARCHETYPES:
            candidate = self.top[f"staid_archetype_candidate_{archetype.value}"]
            self.assertIsInstance(candidate, PDXBlock)
            hard = [
                assignment
                for assignment in iter_assignments(candidate)
                if assignment.key == f"staid_archetype_hard_{archetype.value}"
            ]
            any_hard_references = [
                assignment
                for assignment in iter_assignments(candidate)
                if assignment.key == "staid_archetype_any_hard"
            ]
            self.assertEqual([atom_value(item) for item in hard], ["yes"])
            self.assertEqual([atom_value(item) for item in any_hard_references], ["no"])

    def test_artifact_uses_only_identity_predicates_and_known_markers(self) -> None:
        names = set(self.top)
        evidence = _evidence_assignments(PRIMARY_ARCHETYPES)
        projected_values: dict[str, set[str]] = {}
        for assignments in evidence.values():
            for assignment in assignments:
                predicate, value = assignment.split(" = ", 1)
                projected_values.setdefault(predicate, set()).add(value)

        allowed_keys = (
            names
            | set(projected_values)
            | {
                "OR",
                "AND",
                "NOR",
                "NOT",
                "calc_true_if",
                "always",
                "is_country_type",
                "is_nomadic",
            }
        )
        assignment_keys = {assignment.key for assignment in iter_assignments(self.root)}
        self.assertEqual(assignment_keys - allowed_keys, set())

        for predicate, expected in projected_values.items():
            actual = {
                atom_value(assignment)
                for assignment in iter_assignments(self.root)
                if assignment.key == predicate
            }
            self.assertEqual(actual, expected, predicate)

    def test_mod_has_no_duplicate_staid_scripted_trigger_ids(self) -> None:
        owners: dict[str, list[Path]] = {}
        for path in sorted(ARTIFACT.parent.glob("*.txt")):
            root = parse_pdx(path.read_text(encoding="utf-8-sig"))
            for assignment in block_assignments(root):
                if assignment.key.startswith("staid_"):
                    owners.setdefault(assignment.key, []).append(path)
        duplicates = {name: paths for name, paths in owners.items() if len(paths) > 1}
        self.assertEqual(duplicates, {})

    def test_renderer_fails_closed_on_personality_source_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            drifted = Path(temp_dir) / "00_personalities.txt"
            drifted.write_text("unknown = {}\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "personality source drift"):
                render_archetype_triggers(drifted)

    def test_dedicated_generator_has_one_fixed_output(self) -> None:
        self.assertEqual(dedicated_generator.OUTPUT_PATH, ARTIFACT)
        with mock.patch.object(dedicated_generator, "write_text_file") as write:
            dedicated_generator.main()
        write.assert_called_once_with(ARTIFACT, self.rendered)
        source = Path(dedicated_generator.__file__).read_text(encoding="utf-8")
        self.assertNotIn("argparse", source)
        self.assertNotIn("sys.argv", source)

    def test_broad_generator_owns_the_same_artifact_without_running_it(self) -> None:
        source = inspect.getsource(generate_mod_files)
        self.assertIn("zzzz_staid_21_nation_archetype_triggers.txt", source)
        self.assertIn("archetype_triggers_text()", source)


if __name__ == "__main__":
    unittest.main()
