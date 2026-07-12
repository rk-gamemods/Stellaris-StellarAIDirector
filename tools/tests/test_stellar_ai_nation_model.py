from __future__ import annotations

import csv
import unittest
from collections import Counter
from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from pathlib import Path

from tools.stellar_ai_economic_model import Lane
from tools.stellar_ai_nation_model import (
    Archetype,
    ClassificationStatus,
    DefensePolicy,
    DiplomacyPolicy,
    ExpansionPolicy,
    FleetPolicy,
    FleetPresence,
    NationIdentity,
    NavalHeadroomState,
    PersonalitySource,
    REVIEWED_444_PERSONALITY_IDS,
    PressureLevel,
    ResearchPolicy,
    ResolvedPersonalityProfile,
    ResourceCapacityState,
    ResourceUseState,
    ShipyardState,
    StrategicContext,
    TemplateState,
    TriState,
    build_nation_policy,
    classify_nation,
    pressure_rank,
    _BEHAVIOR_MARKERS,
)


ROOT = Path(__file__).resolve().parents[2]
ARCHETYPE_CASES = (
    ROOT / "research" / "stellar-ai" / "stellar-ai-director-nation-archetype-cases.csv"
)
POLICY_CASES = (
    ROOT / "research" / "stellar-ai" / "stellar-ai-director-nation-policy-cases.csv"
)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise AssertionError(f"fixture is empty: {path}")
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise AssertionError(f"malformed fixture row in {path}: {row}")
    return rows


def tokens(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split("|") if part.strip())


def optional_string(value: str) -> str | None:
    value = value.strip()
    return value or None


def optional_int(value: str) -> int | None:
    value = value.strip()
    return int(value) if value else None


def optional_decimal(value: str) -> Decimal | None:
    value = value.strip()
    return Decimal(value) if value else None


def identity_from_row(row: dict[str, str]) -> NationIdentity:
    profile = None
    if row["personality_source"] or row["behaviors"]:
        profile = ResolvedPersonalityProfile(
            behaviors=tokens(row["behaviors"]),
            source=PersonalitySource(
                row["personality_source"] or "current_source_resolved"
            ),
            source_ref=row.get("source_ref") or "fixture",
        )
    return NationIdentity(
        country_type=row["country_type"],
        personality_id=optional_string(row["personality_id"]),
        ethics=tokens(row["ethics"]),
        civics=tokens(row["civics"]),
        ascension_perks=tokens(row.get("ascension_perks", "")),
        authority=optional_string(row["authority"]),
        government=optional_string(row["government"]),
        origin=optional_string(row["origin"]),
        is_nomadic=TriState(row.get("is_nomadic") or "unknown"),
        is_wilderness=TriState(row.get("is_wilderness") or "unknown"),
        personality=profile,
    )


def context_from_row(row: dict[str, str]) -> StrategicContext:
    return StrategicContext(
        threat=TriState(row["threat"]),
        at_war=TriState(row["at_war"]),
        boxed_in=TriState(row["boxed_in"]),
        peaceful_expansion_available=TriState(row["peaceful_expansion_available"]),
        legal_claim_target=TriState(row["legal_claim_target"]),
        legal_conquest_target=TriState(row["legal_conquest_target"]),
        economic_recovery_required=TriState(row["economic_recovery_required"]),
        post_completion_runway_safe=TriState(row["post_completion_runway_safe"]),
        fleet_ship_count=optional_int(row["fleet_ship_count"]),
        template_count=optional_int(row["template_count"]),
        template_target_size=optional_int(row["template_target_size"]),
        template_current_size=optional_int(row["template_current_size"]),
        naval_capacity_used=optional_decimal(row["naval_capacity_used"]),
        naval_capacity=optional_decimal(row["naval_capacity"]),
        shipyard_capacity=optional_int(row["shipyard_capacity"]),
        shipyard_queued=optional_int(row["shipyard_queued"]),
        tracked_resource_capacity=optional_decimal(row["tracked_resource_capacity"]),
        tracked_resource_use=optional_decimal(row["tracked_resource_use"]),
    )


class StellarAiNationModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.archetype_rows = load_rows(ARCHETYPE_CASES)
        cls.policy_rows = load_rows(POLICY_CASES)
        cls.identity_rows = {row["case_id"]: row for row in cls.archetype_rows}
        cls.policy_rows_by_id = {row["case_id"]: row for row in cls.policy_rows}
        if len(cls.identity_rows) != len(cls.archetype_rows):
            raise AssertionError("duplicate archetype fixture case_id")
        if len(cls.policy_rows_by_id) != len(cls.policy_rows):
            raise AssertionError("duplicate policy fixture case_id")

    def classification_for(self, identity_case_id: str):
        identity = identity_from_row(self.identity_rows[identity_case_id])
        return identity, classify_nation(identity)

    def policy_for(self, policy_case_id: str):
        row = self.policy_rows_by_id[policy_case_id]
        identity, classification = self.classification_for(row["identity_case_id"])
        context = context_from_row(row)
        return build_nation_policy(identity, classification, context)

    def test_archetype_fixtures_cover_all_primary_classes_and_statuses(self) -> None:
        observed_primaries: set[Archetype] = set()
        observed_statuses: set[ClassificationStatus] = set()
        for row in self.archetype_rows:
            with self.subTest(case_id=row["case_id"]):
                classification = classify_nation(identity_from_row(row))
                expected_status = ClassificationStatus(row["expected_status"])
                expected_primary = (
                    Archetype(row["expected_primary"])
                    if row["expected_primary"]
                    else None
                )
                expected_secondary = tuple(
                    Archetype(value) for value in tokens(row["expected_secondary"])
                )
                self.assertEqual(classification.status, expected_status)
                self.assertEqual(classification.primary, expected_primary)
                self.assertEqual(classification.secondary, expected_secondary)
                self.assertTrue(row["source_ref"])
                self.assertEqual(
                    tuple(item.archetype for item in classification.evidence),
                    tuple(Archetype),
                )
                observed_statuses.add(classification.status)
                if classification.primary is not None:
                    observed_primaries.add(classification.primary)

        self.assertEqual(observed_primaries, set(Archetype))
        self.assertTrue(
            {
                ClassificationStatus.CLASSIFIED,
                ClassificationStatus.EXCLUDED,
                ClassificationStatus.CONFLICT,
                ClassificationStatus.INSUFFICIENT_EVIDENCE,
            }.issubset(observed_statuses)
        )

    def test_fanatic_ethics_contribute_three_secondary_pressure_units(self) -> None:
        normal = classify_nation(
            NationIdentity(ethics=("ethic_materialist",))
        ).for_archetype(Archetype.RESEARCH)
        fanatic = classify_nation(
            NationIdentity(ethics=("ethic_fanatic_materialist",))
        ).for_archetype(Archetype.RESEARCH)
        self.assertEqual(normal.ethic_pressure_units, 1)
        self.assertEqual(fanatic.ethic_pressure_units, 3)

    def test_identity_vocabulary_is_source_reviewed(self) -> None:
        self.assertEqual(
            REVIEWED_444_PERSONALITY_IDS,
            {
                "honorbound_warriors",
                "evangelising_zealots",
                "erudite_explorers",
                "spiritual_seekers",
                "ruthless_capitalists",
                "peaceful_traders",
                "hegemonic_imperialists",
                "slaving_despots",
                "decadent_hierarchy",
                "democratic_crusaders",
                "harmonious_hierarchy",
                "federation_builders",
                "xenophobic_isolationists",
                "fanatic_purifiers",
                "hive_mind",
                "devouring_swarm",
                "migrating_flock",
                "metalhead",
                "machine_intelligence",
                "assimilators",
                "exterminators",
                "servitors",
                "fanatic_befrienders",
                "became_the_crisis",
                "galactic_defense_force",
                "imperial_origin_overlord_ai",
                "hive_mind_friend",
                "decadent_capitalists",
                "scorching_infernals",
                "hyperthermia_empire",
            },
        )
        self.assertEqual(
            set(_BEHAVIOR_MARKERS),
            {
                "purger",
                "attack_neutrals",
                "conqueror",
                "subjugator",
                "dominator",
                "propagator",
                "isolationist",
                "liberator",
                "multispecies",
                "uplifter",
            },
        )

    def test_balanced_fallback_is_explicit_and_neutral(self) -> None:
        identity, classification = self.classification_for("balanced_fallback")
        self.assertEqual(
            classification.status, ClassificationStatus.INSUFFICIENT_EVIDENCE
        )
        self.assertEqual(classification.primary, Archetype.BALANCED)
        policy = build_nation_policy(identity, classification, StrategicContext())
        self.assertIn(
            "classification:insufficient_evidence:balanced_fallback",
            policy.reason_codes,
        )
        self.assertTrue(
            all(
                pressure_rank(pressure) <= pressure_rank(PressureLevel.NEUTRAL)
                for _, pressure in policy.lane_pressure
            )
        )

    def test_recent_save_primary_distribution_is_identity_only(self) -> None:
        save_rows = [
            row for row in self.archetype_rows if row["case_id"].startswith("save_")
        ]
        self.assertEqual(len(save_rows), 10)
        observed = Counter(
            classify_nation(identity_from_row(row)).primary for row in save_rows
        )
        self.assertEqual(
            observed,
            Counter(
                {
                    Archetype.EXTERMINATION: 3,
                    Archetype.CONQUEST: 4,
                    Archetype.DEFENSIVE: 1,
                    Archetype.RESEARCH: 1,
                    Archetype.DIPLOMATIC: 1,
                }
            ),
        )
        self.assertTrue(
            all("7E49527196CAA35D" in row["source_ref"] for row in save_rows)
        )

    def test_non_default_country_is_excluded_before_identity_markers(self) -> None:
        _, classification = self.classification_for("special_excluded")
        self.assertEqual(classification.status, ClassificationStatus.EXCLUDED)
        self.assertIsNone(classification.primary)
        self.assertTrue(
            all(not item.counts.positive for item in classification.evidence)
        )

    def test_contradictory_hard_markers_fail_closed(self) -> None:
        _, classification = self.classification_for("hard_conflict")
        self.assertEqual(classification.status, ClassificationStatus.CONFLICT)
        hard = {
            item.archetype for item in classification.evidence if item.counts.hard > 0
        }
        self.assertEqual(hard, {Archetype.EXTERMINATION, Archetype.DEFENSIVE})
        self.assertIsNone(classification.primary)

    def test_identity_and_profile_order_are_canonical_and_permutation_stable(
        self,
    ) -> None:
        profile_a = ResolvedPersonalityProfile(
            behaviors=("subjugator", "dominator", "conqueror"),
            source=PersonalitySource.SAVE_TIME_WINNER_VERIFIED,
        )
        profile_b = ResolvedPersonalityProfile(
            behaviors=("conqueror", "subjugator", "dominator"),
            source=PersonalitySource.SAVE_TIME_WINNER_VERIFIED,
        )
        identity_a = NationIdentity(
            personality_id="hegemonic_imperialists",
            ethics=("ethic_fanatic_materialist", "ethic_fanatic_militarist"),
            civics=("civic_meritocracy", "civic_nationalistic_zeal"),
            personality=profile_a,
        )
        identity_b = NationIdentity(
            personality_id="hegemonic_imperialists",
            ethics=("ethic_fanatic_militarist", "ethic_fanatic_materialist"),
            civics=("civic_nationalistic_zeal", "civic_meritocracy"),
            personality=profile_b,
        )
        self.assertEqual(identity_a, identity_b)
        self.assertEqual(classify_nation(identity_a), classify_nation(identity_b))

    def test_identity_schema_is_immutable_and_contains_no_outcome_fields(self) -> None:
        identity = NationIdentity(personality_id="erudite_explorers")
        with self.assertRaises(FrozenInstanceError):
            identity.personality_id = "fanatic_purifiers"  # type: ignore[misc]
        self.assertFalse(
            {
                "military_power",
                "tech_power",
                "alloy_stockpile",
                "fleet_ship_count",
            }
            & set(NationIdentity.__dataclass_fields__)
        )

    def test_policy_fixture_contracts(self) -> None:
        for row in self.policy_rows:
            with self.subTest(case_id=row["case_id"]):
                policy = self.policy_for(row["case_id"])
                derived = policy.derived
                self.assertEqual(policy.fleet, FleetPolicy(row["expected_fleet"]))
                self.assertEqual(
                    policy.research, ResearchPolicy(row["expected_research"])
                )
                self.assertEqual(
                    policy.expansion, ExpansionPolicy(row["expected_expansion"])
                )
                self.assertEqual(policy.defense, DefensePolicy(row["expected_defense"]))
                self.assertEqual(
                    policy.diplomacy, DiplomacyPolicy(row["expected_diplomacy"])
                )
                self.assertEqual(
                    derived.fleet_presence,
                    FleetPresence(row["expected_fleet_presence"]),
                )
                self.assertEqual(
                    derived.template_state,
                    TemplateState(row["expected_template_state"]),
                )
                self.assertEqual(
                    derived.shipyard_state,
                    ShipyardState(row["expected_shipyard_state"]),
                )
                self.assertEqual(
                    derived.naval_headroom_state,
                    NavalHeadroomState(row["expected_headroom_state"]),
                )
                self.assertEqual(
                    derived.resource_capacity_state,
                    ResourceCapacityState(row["expected_resource_capacity_state"]),
                )
                self.assertEqual(
                    derived.resource_use_state,
                    ResourceUseState(row["expected_resource_use_state"]),
                )
                self.assertEqual(
                    derived.template_creation_gap,
                    TriState(row["expected_creation_gap"]),
                )
                self.assertEqual(
                    derived.template_expansion_gap,
                    TriState(row["expected_expansion_gap"]),
                )
                self.assertEqual(
                    derived.serialized_reinforcement_demand,
                    optional_int(row["expected_reinforcement_demand"]),
                )
                self.assertEqual(
                    policy.pressure_for(Lane.DEFENSE),
                    PressureLevel(row["expected_defense_pressure"]),
                )
                self.assertEqual(
                    policy.pressure_for(Lane.CLAIMS),
                    PressureLevel(row["expected_claims_pressure"]),
                )
                self.assertEqual(
                    policy.pressure_for(Lane.NEW_HULLS),
                    PressureLevel(row["expected_new_hulls_pressure"]),
                )
                self.assertEqual(
                    tuple(lane for lane, _ in policy.lane_pressure), tuple(Lane)
                )

    def test_low_capacity_and_low_use_do_not_create_an_emergency(self) -> None:
        policy = self.policy_for("low_capacity_low_use")
        self.assertEqual(
            policy.derived.resource_capacity_state, ResourceCapacityState.POSITIVE
        )
        self.assertEqual(policy.derived.resource_use_state, ResourceUseState.UNUSED)
        self.assertEqual(policy.fleet, FleetPolicy.HOLD)
        self.assertEqual(policy.defense, DefensePolicy.NORMAL)
        self.assertLess(
            pressure_rank(policy.pressure_for(Lane.DEFENSE)),
            pressure_rank(PressureLevel.URGENT),
        )

    def test_no_template_is_not_zero_desired_force_demand(self) -> None:
        policy = self.policy_for("exterminator_no_templates")
        self.assertEqual(policy.derived.serialized_reinforcement_demand, 0)
        self.assertEqual(policy.derived.template_creation_gap, TriState.TRUE)
        self.assertEqual(policy.fleet, FleetPolicy.EXPAND)
        self.assertIn("fleet:template_creation_gap", policy.reason_codes)

    def test_filled_tiny_template_exposes_expansion_gap(self) -> None:
        policy = self.policy_for("conquest_filled_tiny")
        self.assertEqual(policy.derived.template_state, TemplateState.FILLED)
        self.assertEqual(policy.derived.serialized_reinforcement_demand, 0)
        self.assertEqual(policy.derived.template_expansion_gap, TriState.TRUE)
        self.assertEqual(policy.fleet, FleetPolicy.EXPAND)
        self.assertIn("fleet:template_expansion_gap", policy.reason_codes)

    def test_wartime_replacement_is_not_overwritten_by_expansion_gap(self) -> None:
        identity, classification = self.classification_for("honorbound_conquest")
        context = replace(
            context_from_row(self.policy_rows_by_id["conquest_filled_tiny"]),
            at_war=TriState.TRUE,
        )
        policy = build_nation_policy(identity, classification, context)
        self.assertEqual(policy.fleet, FleetPolicy.REPLACE)
        self.assertIn("war:replacement_raised", policy.reason_codes)

    def test_threat_monotonically_raises_bounded_defense(self) -> None:
        safe = self.policy_for("diplomatic_safe")
        threatened = self.policy_for("diplomatic_threat")
        self.assertLess(
            pressure_rank(safe.pressure_for(Lane.DEFENSE)),
            pressure_rank(threatened.pressure_for(Lane.DEFENSE)),
        )
        self.assertEqual(threatened.pressure_for(Lane.DEFENSE), PressureLevel.URGENT)
        self.assertEqual(threatened.defense, DefensePolicy.EMERGENCY)
        self.assertEqual(threatened.diplomacy, safe.diplomacy)

    def test_pacifist_without_legal_target_never_selects_conquest(self) -> None:
        policy = self.policy_for("pacifist_boxed_no_target")
        self.assertEqual(policy.expansion, ExpansionPolicy.NONE)
        self.assertEqual(policy.pressure_for(Lane.CLAIMS), PressureLevel.SUPPRESS)
        self.assertNotEqual(policy.diplomacy, DiplomacyPolicy.EXTERMINATING)

    def test_unknown_and_known_zero_naval_capacity_remain_distinct(self) -> None:
        unknown = self.policy_for("unknown_naval_capacity")
        zero = self.policy_for("zero_naval_capacity")
        self.assertEqual(
            unknown.derived.naval_headroom_state, NavalHeadroomState.UNKNOWN
        )
        self.assertIsNone(unknown.derived.naval_headroom)
        self.assertEqual(zero.derived.naval_headroom_state, NavalHeadroomState.NONE)
        self.assertEqual(zero.derived.naval_headroom, Decimal("0"))
        self.assertEqual(unknown.fleet, FleetPolicy.HOLD)
        self.assertEqual(zero.fleet, FleetPolicy.HOLD)

    def test_recovery_and_runway_dominate_identity_preferences(self) -> None:
        recovery = self.policy_for("recovery_dominates_extermination")
        unsafe = self.policy_for("unsafe_runway_dominates_threat")
        self.assertEqual(recovery.expansion, ExpansionPolicy.NONE)
        self.assertEqual(recovery.fleet, FleetPolicy.HOLD)
        self.assertEqual(
            recovery.pressure_for(Lane.STRATEGIC_PRODUCER), PressureLevel.URGENT
        )
        self.assertEqual(
            recovery.pressure_for(Lane.NEW_HULLS), PressureLevel.DEEMPHASIZE
        )
        self.assertEqual(unsafe.expansion, ExpansionPolicy.NONE)
        self.assertEqual(unsafe.fleet, FleetPolicy.HOLD)
        for lane in Lane:
            if lane not in {Lane.STRATEGIC_PRODUCER, Lane.MARKET_BRIDGE}:
                self.assertEqual(unsafe.pressure_for(lane), PressureLevel.SUPPRESS)

    def test_unknown_observations_fail_neutral(self) -> None:
        identity, classification = self.classification_for("honorbound_conquest")
        policy = build_nation_policy(identity, classification, StrategicContext())
        self.assertEqual(policy.fleet, FleetPolicy.HOLD)
        self.assertEqual(policy.expansion, ExpansionPolicy.NONE)
        self.assertEqual(policy.derived.fleet_presence, FleetPresence.UNKNOWN)
        self.assertEqual(policy.derived.template_state, TemplateState.UNKNOWN)
        self.assertEqual(
            policy.derived.naval_headroom_state, NavalHeadroomState.UNKNOWN
        )

    def test_policy_is_deterministic_across_equivalent_identity_permutations(
        self,
    ) -> None:
        context = context_from_row(self.policy_rows_by_id["conquest_filled_tiny"])
        identity_a = NationIdentity(
            personality_id="hegemonic_imperialists",
            ethics=("ethic_fanatic_militarist", "ethic_fanatic_materialist"),
            civics=("civic_nationalistic_zeal", "civic_meritocracy"),
        )
        identity_b = NationIdentity(
            personality_id="hegemonic_imperialists",
            ethics=("ethic_fanatic_materialist", "ethic_fanatic_militarist"),
            civics=("civic_meritocracy", "civic_nationalistic_zeal"),
        )
        policy_a = build_nation_policy(identity_a, classify_nation(identity_a), context)
        policy_b = build_nation_policy(identity_b, classify_nation(identity_b), context)
        self.assertEqual(policy_a, policy_b)

    def test_pressure_is_bounded_categorical_not_a_gameplay_number(self) -> None:
        self.assertEqual(len(PressureLevel), 5)
        for value in PressureLevel:
            self.assertIsInstance(value.value, str)
            self.assertGreaterEqual(pressure_rank(value), 0)
            self.assertLess(pressure_rank(value), len(PressureLevel))

    def test_enormous_observations_cannot_escape_categorical_bounds(self) -> None:
        identity, classification = self.classification_for("honorbound_conquest")
        huge = 10**100
        policy = build_nation_policy(
            identity,
            classification,
            StrategicContext(
                threat=TriState.TRUE,
                at_war=TriState.TRUE,
                economic_recovery_required=TriState.FALSE,
                post_completion_runway_safe=TriState.TRUE,
                fleet_ship_count=huge,
                template_count=1,
                template_target_size=huge,
                template_current_size=huge,
                naval_capacity_used=Decimal(huge),
                naval_capacity=Decimal(huge * 2),
                shipyard_capacity=huge,
                shipyard_queued=0,
                tracked_resource_capacity=Decimal(huge),
                tracked_resource_use=Decimal(huge),
            ),
        )
        self.assertEqual(policy.defense, DefensePolicy.EMERGENCY)
        self.assertEqual(policy.fleet, FleetPolicy.EMERGENCY_DEFENSE)
        self.assertTrue(
            all(
                0 <= pressure_rank(pressure) < len(PressureLevel)
                for _, pressure in policy.lane_pressure
            )
        )


if __name__ == "__main__":
    unittest.main()
