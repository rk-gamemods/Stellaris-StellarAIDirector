"""Deterministic renderer for identity-only Stellar AI archetype triggers."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Iterable

try:
    from tools.stellar_ai_nation_model import (
        ARCHETYPE_PRECEDENCE,
        OUTSIDE_PRIMARY_PERSONALITIES,
        PEGASUS_444_PERSONALITY_SHA256,
        PRIMARY_PERSONALITY_GROUPS,
        REVIEWED_444_PERSONALITY_IDS,
        Archetype,
        EvidenceStrength,
        _ASCENSION_PERK_MARKERS,
        _AUTHORITY_MARKERS,
        _BEHAVIOR_MARKERS,
        _CIVIC_MARKERS,
        _ETHIC_MARKERS,
        _GOVERNMENT_MARKERS,
        _ORIGIN_MARKERS,
    )
except ModuleNotFoundError:
    from stellar_ai_nation_model import (  # type: ignore[no-redef]
        ARCHETYPE_PRECEDENCE,
        OUTSIDE_PRIMARY_PERSONALITIES,
        PEGASUS_444_PERSONALITY_SHA256,
        PRIMARY_PERSONALITY_GROUPS,
        REVIEWED_444_PERSONALITY_IDS,
        Archetype,
        EvidenceStrength,
        _ASCENSION_PERK_MARKERS,
        _AUTHORITY_MARKERS,
        _BEHAVIOR_MARKERS,
        _CIVIC_MARKERS,
        _ETHIC_MARKERS,
        _GOVERNMENT_MARKERS,
        _ORIGIN_MARKERS,
    )


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _evidence_assignments(
    primary_archetypes: tuple[Archetype, ...],
) -> dict[tuple[Archetype, EvidenceStrength], tuple[str, ...]]:
    """Project the H08a evidence vocabulary onto live country predicates."""

    working: dict[tuple[Archetype, EvidenceStrength], list[str]] = {
        (archetype, strength): []
        for archetype in primary_archetypes
        for strength in EvidenceStrength
    }

    for archetype in primary_archetypes:
        working[(archetype, EvidenceStrength.HARD)].extend(
            f"has_ai_personality = {personality_id}"
            for personality_id in PRIMARY_PERSONALITY_GROUPS[archetype]
        )

    marker_maps = (
        (_ETHIC_MARKERS, "has_ethic"),
        (_CIVIC_MARKERS, "has_valid_civic"),
        (_ASCENSION_PERK_MARKERS, "has_ascension_perk"),
        (_AUTHORITY_MARKERS, "has_authority"),
        (_GOVERNMENT_MARKERS, "has_government"),
        (_ORIGIN_MARKERS, "has_origin"),
    )
    for marker_map, predicate in marker_maps:
        for marker, (archetype, strength) in marker_map.items():
            if archetype is Archetype.BALANCED:
                raise RuntimeError("balanced archetype cannot own identity evidence")
            working[(archetype, strength)].append(f"{predicate} = {marker}")

    working[(Archetype.GESTALT_GROWTH, EvidenceStrength.STRONG)].append(
        "is_wilderness_empire = yes"
    )

    # The live predicate exposes the current effective personality behaviour but
    # not the H08a offline provenance enum. Treat it as the model's conservative
    # current-source supporting evidence; reviewed personality IDs remain hard.
    for behavior, archetype in _BEHAVIOR_MARKERS.items():
        working[(archetype, EvidenceStrength.SUPPORTING)].append(
            f"has_ai_personality_behaviour = {behavior}"
        )

    result: dict[tuple[Archetype, EvidenceStrength], tuple[str, ...]] = {}
    for key, assignments in working.items():
        if len(assignments) != len(set(assignments)):
            archetype, strength = key
            raise RuntimeError(
                "duplicate nation-model marker projection for "
                f"{archetype.value}/{strength.value}"
            )
        result[key] = tuple(assignments)
    return result


def _at_least_body(assignments: tuple[str, ...], count: int) -> list[str]:
    """Render a threshold over a small, fixed identity-marker set."""

    if count < 1 or count > len(assignments):
        raise ValueError("count threshold must be within the marker set")
    return [
        "calc_true_if = {",
        f"\tamount >= {count}",
        *[f"\t{assignment}" for assignment in assignments],
        "}",
    ]


def _indent(lines: Iterable[str], levels: int = 1) -> list[str]:
    prefix = "\t" * levels
    return [f"{prefix}{line}" for line in lines]


def render_archetype_triggers(personality_path: Path) -> str:
    """Render mutually exclusive country-identity triggers with no policy effects."""

    primary_archetypes = tuple(
        archetype
        for archetype in ARCHETYPE_PRECEDENCE
        if archetype is not Archetype.BALANCED
    )
    if tuple(PRIMARY_PERSONALITY_GROUPS) != primary_archetypes:
        raise RuntimeError(
            "nation-model personality groups are not in archetype precedence order"
        )

    grouped_personalities = tuple(
        personality_id
        for archetype in primary_archetypes
        for personality_id in PRIMARY_PERSONALITY_GROUPS[archetype]
    )
    if len(grouped_personalities) != len(set(grouped_personalities)):
        raise RuntimeError(
            "a personality appears in more than one primary archetype group"
        )
    if (set(grouped_personalities) | set(OUTSIDE_PRIMARY_PERSONALITIES)) != set(
        REVIEWED_444_PERSONALITY_IDS
    ):
        raise RuntimeError(
            "reviewed personality coverage is inconsistent with the nation model"
        )

    if not personality_path.is_file():
        raise FileNotFoundError(
            f"missing pinned personality source: {personality_path}"
        )
    actual_hash = _file_sha256(personality_path)
    if actual_hash != PEGASUS_444_PERSONALITY_SHA256:
        raise RuntimeError(
            "Pegasus 4.4.4 personality source drift: "
            f"expected {PEGASUS_444_PERSONALITY_SHA256}, got {actual_hash}"
        )
    source_text = personality_path.read_text(encoding="utf-8-sig")
    source_objects = set(
        re.findall(r"(?m)^([A-Za-z0-9_.~!@:+-]+)\s*=\s*\{", source_text)
    )
    missing_personalities = sorted(set(REVIEWED_444_PERSONALITY_IDS) - source_objects)
    if missing_personalities:
        raise RuntimeError(
            "reviewed personality IDs missing from pinned source: "
            + ", ".join(missing_personalities)
        )

    lines = [
        "# Generated by tools/generate_stellar_ai_archetype_triggers.py.",
        "# Also owned by tools/generate_stellar_ai_director_patch.py.",
        "# Pegasus 4.4.4 personality source SHA256:",
        f"# {PEGASUS_444_PERSONALITY_SHA256}",
        "# Identity classification only: no weights, resources, state, or orders.",
        "# H08a parity: hard, strong, then supporting marker counts; precedence breaks ties.",
        "# H08e exposes at most one lead secondary and never replaces the primary.",
        "",
    ]

    def add_trigger(name: str, body: Iterable[str]) -> None:
        lines.append(f"{name} = {{")
        lines.extend(f"\t{line}" if line else "" for line in body)
        lines.extend(("}", ""))

    def or_lines(assignments: Iterable[str]) -> list[str]:
        return ["OR = {"] + [f"\t{assignment}" for assignment in assignments] + ["}"]

    def nor_lines(assignments: Iterable[str]) -> list[str]:
        return ["NOR = {"] + [f"\t{assignment}" for assignment in assignments] + ["}"]

    def hard_name(archetype: Archetype) -> str:
        return f"staid_archetype_hard_{archetype.value}"

    def candidate_name(archetype: Archetype) -> str:
        return f"staid_archetype_candidate_{archetype.value}"

    def primary_name(archetype: Archetype) -> str:
        return f"staid_archetype_{archetype.value}"

    def lead_secondary_name(archetype: Archetype) -> str:
        return f"staid_archetype_lead_secondary_{archetype.value}"

    def threshold_name(
        archetype: Archetype, strength: EvidenceStrength, count: int
    ) -> str:
        return f"staid_archetype_{strength.value}_{archetype.value}_at_least_{count}"

    def ge_name(strength: EvidenceStrength, left: Archetype, right: Archetype) -> str:
        return f"staid_archetype_{strength.value}_{left.value}_ge_{right.value}"

    evidence_assignments = _evidence_assignments(primary_archetypes)

    add_trigger(
        "staid_archetype_eligible_country",
        ("is_country_type = default", "is_nomadic = no"),
    )
    for name, predicate in (
        ("staid_identity_megacorp", "is_megacorp = yes"),
        ("staid_role_subject", "is_subject = yes"),
        ("staid_role_overlord", "is_overlord = yes"),
        (
            "staid_identity_rogue_servitor",
            "has_valid_civic = civic_machine_servitor",
        ),
        (
            "staid_identity_assimilator",
            "has_valid_civic = civic_machine_assimilator",
        ),
        (
            "staid_identity_machine_exterminator",
            "has_valid_civic = civic_machine_terminator",
        ),
        (
            "staid_identity_devouring_swarm",
            "has_valid_civic = civic_hive_devouring_swarm",
        ),
        (
            "staid_identity_inward_perfection",
            "has_valid_civic = civic_inwards_perfection",
        ),
        (
            "staid_identity_barbaric_despoiler",
            "has_valid_civic = civic_barbaric_despoilers",
        ),
        ("staid_identity_nomadic", "is_nomadic = yes"),
    ):
        add_trigger(name, ("is_country_type = default", predicate))
    add_trigger(
        "staid_identity_ordinary_hive",
        (
            "is_country_type = default",
            "is_nomadic = no",
            "is_wilderness_empire = no",
            "is_hive_empire = yes",
            "NOT = { has_valid_civic = civic_hive_devouring_swarm }",
        ),
    )

    for archetype in primary_archetypes:
        add_trigger(
            hard_name(archetype),
            or_lines(evidence_assignments[(archetype, EvidenceStrength.HARD)]),
        )

    hard_names = tuple(hard_name(archetype) for archetype in primary_archetypes)
    add_trigger(
        "staid_archetype_identity_conflict",
        (
            "calc_true_if = {",
            "\tamount >= 2",
            *(f"\t{name} = yes" for name in hard_names),
            "}",
        ),
    )
    add_trigger(
        "staid_archetype_any_hard",
        or_lines(f"{name} = yes" for name in hard_names),
    )

    ranked_strengths = (EvidenceStrength.STRONG, EvidenceStrength.SUPPORTING)
    for archetype in primary_archetypes:
        for strength in ranked_strengths:
            assignments = evidence_assignments[(archetype, strength)]
            for count in range(1, len(assignments) + 1):
                add_trigger(
                    threshold_name(archetype, strength, count),
                    _at_least_body(assignments, count),
                )

    for strength in ranked_strengths:
        for left in primary_archetypes:
            for right in primary_archetypes:
                if left is right:
                    continue
                left_count = len(evidence_assignments[(left, strength)])
                right_count = len(evidence_assignments[(right, strength)])
                if right_count == 0:
                    body = ["always = yes"]
                else:
                    body = []
                    for count in range(1, right_count + 1):
                        right_threshold = threshold_name(right, strength, count)
                        if count > left_count:
                            body.append(f"{right_threshold} = no")
                        else:
                            body.extend(
                                (
                                    "OR = {",
                                    f"\t{right_threshold} = no",
                                    f"\t{threshold_name(left, strength, count)} = yes",
                                    "}",
                                )
                            )
                add_trigger(ge_name(strength, left, right), body)

    precedence_index = {
        archetype: index for index, archetype in enumerate(primary_archetypes)
    }

    def outranks_lines(left: Archetype, right: Archetype) -> list[str]:
        strong_left_ge = ge_name(EvidenceStrength.STRONG, left, right)
        strong_right_ge = ge_name(EvidenceStrength.STRONG, right, left)
        support_left_ge = ge_name(EvidenceStrength.SUPPORTING, left, right)
        support_right_ge = ge_name(EvidenceStrength.SUPPORTING, right, left)
        body = [
            "OR = {",
            "\tAND = {",
            f"\t\t{strong_left_ge} = yes",
            f"\t\t{strong_right_ge} = no",
            "\t}",
            "\tAND = {",
            f"\t\t{strong_left_ge} = yes",
            f"\t\t{strong_right_ge} = yes",
            f"\t\t{support_left_ge} = yes",
            f"\t\t{support_right_ge} = no",
            "\t}",
        ]
        if precedence_index[left] < precedence_index[right]:
            body.extend(
                (
                    "\tAND = {",
                    f"\t\t{strong_left_ge} = yes",
                    f"\t\t{strong_right_ge} = yes",
                    f"\t\t{support_left_ge} = yes",
                    f"\t\t{support_right_ge} = yes",
                    "\t}",
                )
            )
        body.append("}")
        return body

    for archetype in primary_archetypes:
        active_thresholds = [
            threshold_name(archetype, strength, 1)
            for strength in ranked_strengths
            if evidence_assignments[(archetype, strength)]
        ]
        body = [
            "OR = {",
            f"\t{hard_name(archetype)} = yes",
            "\tAND = {",
            "\t\tstaid_archetype_any_hard = no",
            "\t\tOR = {",
            *[f"\t\t\t{name} = yes" for name in active_thresholds],
            "\t\t}",
        ]
        for competitor in primary_archetypes:
            if competitor is archetype:
                continue
            body.extend(_indent(outranks_lines(archetype, competitor), 2))
        body.extend(("\t}", "}"))
        add_trigger(candidate_name(archetype), body)

    for archetype in primary_archetypes:
        add_trigger(
            primary_name(archetype),
            (
                "staid_archetype_eligible_country = yes",
                "staid_archetype_identity_conflict = no",
                f"{candidate_name(archetype)} = yes",
            ),
        )

    for archetype in primary_archetypes:
        active_evidence = [hard_name(archetype)] + [
            threshold_name(archetype, strength, 1)
            for strength in ranked_strengths
            if evidence_assignments[(archetype, strength)]
        ]
        body = [
            "staid_archetype_eligible_country = yes",
            "staid_archetype_identity_conflict = no",
            f"{primary_name(archetype)} = no",
            *or_lines(f"{name} = yes" for name in active_evidence),
        ]
        for competitor in primary_archetypes:
            if competitor is archetype:
                continue
            body.extend(
                (
                    "OR = {",
                    f"\t{primary_name(competitor)} = yes",
                    *_indent(outranks_lines(archetype, competitor)),
                    "}",
                )
            )
        add_trigger(lead_secondary_name(archetype), body)

    add_trigger(
        "staid_archetype_balanced",
        [
            "staid_archetype_eligible_country = yes",
            *nor_lines(
                f"staid_archetype_{archetype.value} = yes"
                for archetype in primary_archetypes
            ),
        ],
    )

    return "\n".join(lines).rstrip() + "\n"
