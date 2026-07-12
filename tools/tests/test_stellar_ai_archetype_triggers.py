from __future__ import annotations

import inspect
import tempfile
import unittest
from collections import Counter
from itertools import combinations
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
from tools.stellar_ai_archetype_triggers import render_archetype_triggers
from tools.stellar_ai_nation_model import (
    ARCHETYPE_PRECEDENCE,
    OUTSIDE_PRIMARY_PERSONALITIES,
    PEGASUS_444_PERSONALITY_SHA256,
    PRIMARY_PERSONALITY_GROUPS,
    REVIEWED_444_PERSONALITY_IDS,
    Archetype,
    _ASCENSION_PERK_MARKERS,
    _BEHAVIOR_MARKERS,
    _CIVIC_MARKERS,
    _ETHIC_MARKERS,
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

    def test_hard_conflict_trigger_contains_every_pair_once(self) -> None:
        conflict = self.top["staid_archetype_identity_conflict"]
        self.assertIsInstance(conflict, PDXBlock)
        or_assignment = block_assignments(conflict, "OR")
        self.assertEqual(len(or_assignment), 1)
        self.assertIsInstance(or_assignment[0].value, PDXBlock)
        pair_blocks = block_assignments(or_assignment[0].value, "AND")
        actual_pairs = {
            frozenset(
                assignment.key
                for assignment in block_assignments(pair.value)
                if assignment.key.startswith("staid_archetype_hard_")
            )
            for pair in pair_blocks
            if isinstance(pair.value, PDXBlock)
        }
        hard_names = tuple(
            f"staid_archetype_hard_{archetype.value}"
            for archetype in PRIMARY_ARCHETYPES
        )
        expected_pairs = {frozenset(pair) for pair in combinations(hard_names, 2)}
        self.assertEqual(actual_pairs, expected_pairs)
        self.assertEqual(len(pair_blocks), len(expected_pairs))
        for pair in pair_blocks:
            self.assertIsInstance(pair.value, PDXBlock)
            references = block_assignments(pair.value)
            self.assertEqual(len(references), 2)
            self.assertTrue(
                all(atom_value(reference) == "yes" for reference in references)
            )

    def test_primary_precedence_is_candidate_based_and_mutually_exclusive(self) -> None:
        preceding_candidates: list[str] = []
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

            nor_assignments = block_assignments(block, "NOR")
            if not preceding_candidates:
                self.assertEqual(nor_assignments, [])
            else:
                self.assertEqual(len(nor_assignments), 1)
                self.assertIsInstance(nor_assignments[0].value, PDXBlock)
                exclusions = block_assignments(nor_assignments[0].value)
                excluded = {assignment.key for assignment in exclusions}
                self.assertEqual(excluded, set(preceding_candidates))
                self.assertEqual(len(exclusions), len(preceding_candidates))
                self.assertTrue(
                    all(atom_value(exclusion) == "yes" for exclusion in exclusions)
                )
            preceding_candidates.append(candidate)

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

    def test_mixed_diplomatic_conquest_signals_preserve_model_precedence(self) -> None:
        diplomatic = self.top["staid_archetype_candidate_diplomatic"]
        self.assertIsInstance(diplomatic, PDXBlock)
        or_assignment = block_assignments(diplomatic, "OR")
        self.assertEqual(len(or_assignment), 1)
        self.assertIsInstance(or_assignment[0].value, PDXBlock)
        fallback = block_assignments(or_assignment[0].value, "AND")
        self.assertEqual(len(fallback), 1)
        self.assertIsInstance(fallback[0].value, PDXBlock)
        veto = block_assignments(fallback[0].value, "NOR")
        self.assertEqual(len(veto), 1)
        self.assertIsInstance(veto[0].value, PDXBlock)
        vetoed_behaviors = {
            atom_value(assignment)
            for assignment in block_assignments(veto[0].value)
            if assignment.key == "has_ai_personality_behaviour"
        }
        self.assertEqual(vetoed_behaviors, {"conqueror"})

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

        self.assertLessEqual(max(depth(name) for name in graph), 4)

    def test_every_trigger_reference_and_fixed_boolean_has_exact_polarity(self) -> None:
        names = set(self.top)
        actual_references = Counter(
            (owner, assignment.key, atom_value(assignment))
            for owner, block in self.top.items()
            for assignment in iter_assignments(block)
            if assignment.key in names
        )
        expected_references: Counter[tuple[str, str, str]] = Counter()

        hard_names = tuple(
            f"staid_archetype_hard_{archetype.value}"
            for archetype in PRIMARY_ARCHETYPES
        )
        for left, right in combinations(hard_names, 2):
            expected_references[("staid_archetype_identity_conflict", left, "yes")] += 1
            expected_references[
                ("staid_archetype_identity_conflict", right, "yes")
            ] += 1

        for index, archetype in enumerate(PRIMARY_ARCHETYPES):
            candidate = f"staid_archetype_candidate_{archetype.value}"
            expected_references[(candidate, hard_names[index], "yes")] += 1
            if archetype is Archetype.EXTERMINATION:
                excluded_hard = hard_names[1:]
            elif archetype is Archetype.GESTALT_GROWTH:
                excluded_hard = hard_names[2:]
            elif archetype is Archetype.DEFENSIVE:
                excluded_hard = hard_names[3:]
            elif archetype is Archetype.RESEARCH:
                excluded_hard = hard_names[4:]
            elif archetype is Archetype.DIPLOMATIC:
                expected_references[(candidate, hard_names[-1], "no")] += 1
                excluded_hard = ()
            else:
                excluded_hard = ()
            for hard_name in excluded_hard:
                expected_references[(candidate, hard_name, "yes")] += 1

        preceding_candidates: list[str] = []
        for archetype in PRIMARY_ARCHETYPES:
            primary = f"staid_archetype_{archetype.value}"
            candidate = f"staid_archetype_candidate_{archetype.value}"
            expected_references[
                (primary, "staid_archetype_eligible_country", "yes")
            ] += 1
            expected_references[
                (primary, "staid_archetype_identity_conflict", "no")
            ] += 1
            expected_references[(primary, candidate, "yes")] += 1
            for preceding in preceding_candidates:
                expected_references[(primary, preceding, "yes")] += 1
            preceding_candidates.append(candidate)

        expected_references[
            ("staid_archetype_balanced", "staid_archetype_eligible_country", "yes")
        ] += 1
        for primary in PRIMARY_TRIGGER_NAMES[:-1]:
            expected_references[("staid_archetype_balanced", primary, "yes")] += 1

        self.assertEqual(actual_references, expected_references)

        fixed_keys = {
            "is_country_type",
            "is_nomadic",
            "is_hive_empire",
            "is_machine_empire",
            "is_wilderness_empire",
            "is_pacifist",
            "has_federator_personality",
        }
        actual_fixed = Counter(
            (owner, assignment.key, atom_value(assignment))
            for owner, block in self.top.items()
            for assignment in iter_assignments(block)
            if assignment.key in fixed_keys
        )
        expected_fixed = Counter(
            {
                ("staid_archetype_eligible_country", "is_country_type", "default"): 1,
                ("staid_archetype_eligible_country", "is_nomadic", "no"): 1,
                (
                    "staid_archetype_candidate_gestalt_growth",
                    "is_hive_empire",
                    "yes",
                ): 1,
                (
                    "staid_archetype_candidate_gestalt_growth",
                    "is_machine_empire",
                    "yes",
                ): 1,
                (
                    "staid_archetype_candidate_gestalt_growth",
                    "is_wilderness_empire",
                    "yes",
                ): 1,
                ("staid_archetype_candidate_defensive", "is_pacifist", "yes"): 1,
                (
                    "staid_archetype_candidate_defensive",
                    "has_federator_personality",
                    "no",
                ): 1,
                (
                    "staid_archetype_candidate_research",
                    "has_federator_personality",
                    "no",
                ): 1,
                (
                    "staid_archetype_candidate_diplomatic",
                    "has_federator_personality",
                    "yes",
                ): 1,
            }
        )
        self.assertEqual(actual_fixed, expected_fixed)

    def test_artifact_uses_only_identity_predicates_and_known_markers(self) -> None:
        names = set(self.top)
        allowed_keys = names | {
            "OR",
            "AND",
            "NOR",
            "NOT",
            "is_country_type",
            "is_nomadic",
            "has_ai_personality",
            "has_ai_personality_behaviour",
            "has_valid_civic",
            "has_ascension_perk",
            "has_ethic",
            "is_hive_empire",
            "is_machine_empire",
            "is_wilderness_empire",
            "has_federator_personality",
            "is_pacifist",
        }
        assignment_keys = {assignment.key for assignment in iter_assignments(self.root)}
        self.assertEqual(assignment_keys - allowed_keys, set())

        required_values = {
            "has_ai_personality": set().union(*PRIMARY_PERSONALITY_GROUPS.values()),
            "has_ai_personality_behaviour": set(_BEHAVIOR_MARKERS),
            "has_valid_civic": {
                "civic_fanatic_purifiers",
                "civic_hive_devouring_swarm",
                "civic_machine_terminator",
                "civic_scorched_earth",
                "civic_hive_scorched_earth",
                "civic_inwards_perfection",
                "civic_technocracy",
                "civic_distinguished_admiralty",
                "civic_nationalistic_zeal",
                "civic_barbaric_despoilers",
                "civic_machine_assimilator",
            },
            "has_ascension_perk": {"ap_become_the_crisis"},
            "has_ethic": {
                "ethic_fanatic_pacifist",
                "ethic_materialist",
                "ethic_fanatic_materialist",
                "ethic_xenophile",
                "ethic_fanatic_xenophile",
                "ethic_egalitarian",
                "ethic_fanatic_egalitarian",
                "ethic_militarist",
                "ethic_fanatic_militarist",
            },
        }
        self.assertTrue(required_values["has_valid_civic"].issubset(_CIVIC_MARKERS))
        self.assertTrue(
            required_values["has_ascension_perk"].issubset(_ASCENSION_PERK_MARKERS)
        )
        self.assertTrue(required_values["has_ethic"].issubset(_ETHIC_MARKERS))
        for predicate, expected in required_values.items():
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
