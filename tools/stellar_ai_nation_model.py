"""Deterministic nation identity and strategic-pressure model.

This module is comparative planning evidence, not a Stellaris engine emulator.
It deliberately performs no file, game, launcher, or mod I/O.  Static identity
classification is kept separate from dynamic strategic observations so a bad
outcome cannot rewrite what an empire is.  Policy output is categorical and
bounded; it does not map preferences to mutable gameplay priority numbers.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Iterable, Mapping, TypeAlias

from tools.stellar_ai_economic_model import Lane


Number: TypeAlias = Decimal | int | str


class TriState(str, Enum):
    """Explicit three-valued observation state."""

    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


class Archetype(str, Enum):
    EXTERMINATION = "extermination"
    GESTALT_GROWTH = "gestalt_growth"
    DEFENSIVE = "defensive"
    RESEARCH = "research"
    DIPLOMATIC = "diplomatic"
    CONQUEST = "conquest"
    BALANCED = "balanced"


class ClassificationStatus(str, Enum):
    CLASSIFIED = "classified"
    EXCLUDED = "excluded"
    CONFLICT = "conflict"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class EvidenceStrength(str, Enum):
    HARD = "hard"
    STRONG = "strong"
    SUPPORTING = "supporting"


class PersonalitySource(str, Enum):
    SERIALIZED_ID = "serialized_id"
    CURRENT_SOURCE_RESOLVED = "current_source_resolved"
    SAVE_TIME_WINNER_VERIFIED = "save_time_winner_verified"


class FleetPresence(str, Enum):
    UNKNOWN = "unknown"
    NONE = "no_fleet"
    PRESENT = "present"


class TemplateState(str, Enum):
    UNKNOWN = "unknown"
    ABSENT = "absent"
    UNDERFILLED = "underfilled"
    FILLED = "filled"
    OVERFILLED = "overfilled"


class ShipyardState(str, Enum):
    UNKNOWN = "unknown"
    NONE = "no_shipyard"
    IDLE = "idle"
    ACTIVE = "active"
    SATURATED = "saturated"


class NavalHeadroomState(str, Enum):
    UNKNOWN = "unknown"
    NONE = "no_headroom"
    AVAILABLE = "available"


class ResourceCapacityState(str, Enum):
    UNKNOWN = "unknown"
    ZERO = "zero"
    POSITIVE = "positive"


class ResourceUseState(str, Enum):
    UNKNOWN = "unknown"
    UNUSED = "unused"
    IN_USE = "in_use"


class PressureLevel(str, Enum):
    SUPPRESS = "suppress"
    DEEMPHASIZE = "deemphasize"
    NEUTRAL = "neutral"
    EMPHASIZE = "emphasize"
    URGENT = "urgent"


class FleetPolicy(str, Enum):
    HOLD = "hold"
    REPLACE = "replace"
    EXPAND = "expand"
    EMERGENCY_DEFENSE = "emergency_defense"


class ResearchPolicy(str, Enum):
    HOLD = "hold"
    PRESERVE = "preserve"
    LEAD = "lead"


class ExpansionPolicy(str, Enum):
    NONE = "no_expansion"
    PEACEFUL = "peaceful"
    CLAIM = "claim"
    CONQUEST = "conquest"


class DefensePolicy(str, Enum):
    NORMAL = "normal"
    FRONTIER = "frontier"
    EMERGENCY = "emergency"


class DiplomacyPolicy(str, Enum):
    COOPERATIVE = "cooperative"
    TRANSACTIONAL = "transactional"
    LIBERATING = "liberating"
    SUBJUGATING = "subjugating"
    EXTERMINATING = "exterminating"


_ARCHETYPE_PRECEDENCE = (
    Archetype.EXTERMINATION,
    Archetype.GESTALT_GROWTH,
    Archetype.DEFENSIVE,
    Archetype.RESEARCH,
    Archetype.DIPLOMATIC,
    Archetype.CONQUEST,
    Archetype.BALANCED,
)
_ARCHETYPE_INDEX = {
    archetype: index for index, archetype in enumerate(_ARCHETYPE_PRECEDENCE)
}
_PRESSURE_ORDER = (
    PressureLevel.SUPPRESS,
    PressureLevel.DEEMPHASIZE,
    PressureLevel.NEUTRAL,
    PressureLevel.EMPHASIZE,
    PressureLevel.URGENT,
)
_PRESSURE_INDEX = {value: index for index, value in enumerate(_PRESSURE_ORDER)}


def _normalize_token(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    return normalized or None


def _canonical_tokens(values: Iterable[str]) -> tuple[str, ...]:
    if isinstance(values, str):
        raise TypeError("token collections must not be a bare string")
    normalized = {_normalize_token(value) for value in values}
    normalized.discard(None)
    return tuple(sorted(normalized))  # type: ignore[arg-type]


def _decimal_or_none(value: Number | None, *, label: str) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{label} must be a finite decimal") from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f"{label} must be finite and non-negative")
    return result


def _validate_count(value: int | None, *, label: str) -> None:
    if value is not None and (
        not isinstance(value, int) or isinstance(value, bool) or value < 0
    ):
        raise ValueError(f"{label} must be a non-negative integer or None")


@dataclass(frozen=True)
class ResolvedPersonalityProfile:
    """Optional personality body with provenance separate from its saved ID."""

    behaviors: tuple[str, ...] = ()
    source: PersonalitySource = PersonalitySource.CURRENT_SOURCE_RESOLVED
    source_ref: str | None = None
    aggressiveness: Decimal | None = None
    bravery: Decimal | None = None
    military_spending: Decimal | None = None
    colony_spending: Decimal | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "behaviors", _canonical_tokens(self.behaviors))
        object.__setattr__(self, "source_ref", _normalize_token(self.source_ref))
        for field_name in (
            "aggressiveness",
            "bravery",
            "military_spending",
            "colony_spending",
        ):
            object.__setattr__(
                self,
                field_name,
                _decimal_or_none(getattr(self, field_name), label=field_name),
            )


@dataclass(frozen=True)
class NationIdentity:
    """Static identity evidence only; no economy or outcome statistics belong here."""

    country_type: str = "default"
    personality_id: str | None = None
    ethics: tuple[str, ...] = ()
    civics: tuple[str, ...] = ()
    ascension_perks: tuple[str, ...] = ()
    authority: str | None = None
    government: str | None = None
    origin: str | None = None
    is_nomadic: TriState = TriState.UNKNOWN
    is_wilderness: TriState = TriState.UNKNOWN
    personality: ResolvedPersonalityProfile | None = None

    def __post_init__(self) -> None:
        country_type = _normalize_token(self.country_type)
        if country_type is None:
            raise ValueError("country_type must be non-empty")
        object.__setattr__(self, "country_type", country_type)
        object.__setattr__(
            self, "personality_id", _normalize_token(self.personality_id)
        )
        object.__setattr__(self, "ethics", _canonical_tokens(self.ethics))
        object.__setattr__(self, "civics", _canonical_tokens(self.civics))
        object.__setattr__(
            self, "ascension_perks", _canonical_tokens(self.ascension_perks)
        )
        object.__setattr__(self, "authority", _normalize_token(self.authority))
        object.__setattr__(self, "government", _normalize_token(self.government))
        object.__setattr__(self, "origin", _normalize_token(self.origin))
        for field_name in ("is_nomadic", "is_wilderness"):
            if not isinstance(getattr(self, field_name), TriState):
                raise TypeError(f"{field_name} must use TriState")


@dataclass(frozen=True, order=True)
class EvidenceCounts:
    hard: int = 0
    strong: int = 0
    supporting: int = 0

    def __post_init__(self) -> None:
        for field_name in ("hard", "strong", "supporting"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"{field_name} evidence count must be non-negative")

    @property
    def positive(self) -> bool:
        return bool(self.hard or self.strong or self.supporting)

    @property
    def rank(self) -> tuple[int, int, int]:
        return (self.hard, self.strong, self.supporting)


@dataclass(frozen=True)
class ArchetypeEvidence:
    archetype: Archetype
    counts: EvidenceCounts = EvidenceCounts()
    ethic_pressure_units: int = 0
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.ethic_pressure_units < 0:
            raise ValueError("ethic pressure units must be non-negative")
        object.__setattr__(self, "reason_codes", _canonical_tokens(self.reason_codes))


@dataclass(frozen=True)
class NationClassification:
    status: ClassificationStatus
    primary: Archetype | None
    secondary: tuple[Archetype, ...]
    evidence: tuple[ArchetypeEvidence, ...]
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if tuple(item.archetype for item in self.evidence) != _ARCHETYPE_PRECEDENCE:
            raise ValueError("evidence must contain every archetype in canonical order")
        if len(set(self.secondary)) != len(self.secondary):
            raise ValueError("secondary archetypes must be unique")
        if self.primary is not None and self.primary in self.secondary:
            raise ValueError("primary archetype cannot also be secondary")
        if self.status is ClassificationStatus.CLASSIFIED and self.primary is None:
            raise ValueError("classified identities require a primary archetype")
        if self.status is ClassificationStatus.INSUFFICIENT_EVIDENCE:
            if self.primary is not Archetype.BALANCED or self.secondary:
                raise ValueError(
                    "insufficient evidence must use only the balanced fallback"
                )
        elif (
            self.status is not ClassificationStatus.CLASSIFIED
            and self.primary is not None
        ):
            raise ValueError("excluded or conflicting identities cannot have a primary")
        object.__setattr__(self, "reason_codes", _canonical_tokens(self.reason_codes))

    def for_archetype(self, archetype: Archetype) -> ArchetypeEvidence:
        return self.evidence[_ARCHETYPE_INDEX[archetype]]


_PERSONALITY_MARKERS: Mapping[str, tuple[Archetype, EvidenceStrength]] = {
    "fanatic_purifiers": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "devouring_swarm": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "metalhead": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "exterminators": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "became_the_crisis": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "scorching_infernals": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "hyperthermia_empire": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "hive_mind": (Archetype.GESTALT_GROWTH, EvidenceStrength.HARD),
    "machine_intelligence": (Archetype.GESTALT_GROWTH, EvidenceStrength.HARD),
    "assimilators": (Archetype.GESTALT_GROWTH, EvidenceStrength.HARD),
    "servitors": (Archetype.GESTALT_GROWTH, EvidenceStrength.HARD),
    "hive_mind_friend": (Archetype.GESTALT_GROWTH, EvidenceStrength.HARD),
    "decadent_hierarchy": (Archetype.DEFENSIVE, EvidenceStrength.HARD),
    "harmonious_hierarchy": (Archetype.DEFENSIVE, EvidenceStrength.HARD),
    "xenophobic_isolationists": (Archetype.DEFENSIVE, EvidenceStrength.HARD),
    "erudite_explorers": (Archetype.RESEARCH, EvidenceStrength.HARD),
    "spiritual_seekers": (Archetype.DIPLOMATIC, EvidenceStrength.HARD),
    "federation_builders": (Archetype.DIPLOMATIC, EvidenceStrength.HARD),
    "peaceful_traders": (Archetype.DIPLOMATIC, EvidenceStrength.HARD),
    "migrating_flock": (Archetype.DIPLOMATIC, EvidenceStrength.HARD),
    "honorbound_warriors": (Archetype.CONQUEST, EvidenceStrength.HARD),
    "evangelising_zealots": (Archetype.CONQUEST, EvidenceStrength.HARD),
    "ruthless_capitalists": (Archetype.CONQUEST, EvidenceStrength.HARD),
    "hegemonic_imperialists": (Archetype.CONQUEST, EvidenceStrength.HARD),
    "slaving_despots": (Archetype.CONQUEST, EvidenceStrength.HARD),
    "democratic_crusaders": (Archetype.CONQUEST, EvidenceStrength.HARD),
    "fanatic_befrienders": (Archetype.CONQUEST, EvidenceStrength.HARD),
}

_ETHIC_MARKERS: Mapping[str, tuple[Archetype, EvidenceStrength]] = {
    "ethic_fanatic_pacifist": (Archetype.DEFENSIVE, EvidenceStrength.HARD),
    "ethic_pacifist": (Archetype.DEFENSIVE, EvidenceStrength.STRONG),
    "ethic_fanatic_militarist": (Archetype.CONQUEST, EvidenceStrength.STRONG),
    "ethic_militarist": (Archetype.CONQUEST, EvidenceStrength.SUPPORTING),
    "ethic_fanatic_materialist": (Archetype.RESEARCH, EvidenceStrength.STRONG),
    "ethic_materialist": (Archetype.RESEARCH, EvidenceStrength.SUPPORTING),
    "ethic_fanatic_xenophile": (Archetype.DIPLOMATIC, EvidenceStrength.STRONG),
    "ethic_xenophile": (Archetype.DIPLOMATIC, EvidenceStrength.SUPPORTING),
    "ethic_fanatic_egalitarian": (Archetype.DIPLOMATIC, EvidenceStrength.STRONG),
    "ethic_gestalt_consciousness": (Archetype.GESTALT_GROWTH, EvidenceStrength.STRONG),
    "ethic_egalitarian": (Archetype.DIPLOMATIC, EvidenceStrength.SUPPORTING),
    "ethic_fanatic_authoritarian": (Archetype.CONQUEST, EvidenceStrength.STRONG),
    "ethic_authoritarian": (Archetype.CONQUEST, EvidenceStrength.SUPPORTING),
}

_CIVIC_MARKERS: Mapping[str, tuple[Archetype, EvidenceStrength]] = {
    "civic_fanatic_purifiers": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "civic_hive_devouring_swarm": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "civic_machine_terminator": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "civic_scorched_earth": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "civic_hive_scorched_earth": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "civic_inwards_perfection": (Archetype.DEFENSIVE, EvidenceStrength.HARD),
    "civic_distinguished_admiralty": (Archetype.CONQUEST, EvidenceStrength.STRONG),
    "civic_nationalistic_zeal": (Archetype.CONQUEST, EvidenceStrength.STRONG),
    "civic_barbaric_despoilers": (Archetype.CONQUEST, EvidenceStrength.STRONG),
    "civic_machine_assimilator": (Archetype.CONQUEST, EvidenceStrength.STRONG),
    "civic_technocracy": (Archetype.RESEARCH, EvidenceStrength.STRONG),
    "civic_meritocracy": (Archetype.RESEARCH, EvidenceStrength.SUPPORTING),
    "civic_free_haven": (Archetype.DIPLOMATIC, EvidenceStrength.STRONG),
    "civic_diplomatic_corps": (Archetype.DIPLOMATIC, EvidenceStrength.STRONG),
    "civic_environmentalist": (Archetype.DEFENSIVE, EvidenceStrength.SUPPORTING),
}

_ASCENSION_PERK_MARKERS: Mapping[str, tuple[Archetype, EvidenceStrength]] = {
    "ap_become_the_crisis": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
}

_AUTHORITY_MARKERS: Mapping[str, tuple[Archetype, EvidenceStrength]] = {
    "auth_hive_mind": (Archetype.GESTALT_GROWTH, EvidenceStrength.STRONG),
    "auth_machine_intelligence": (Archetype.GESTALT_GROWTH, EvidenceStrength.STRONG),
}

_GOVERNMENT_MARKERS: Mapping[str, tuple[Archetype, EvidenceStrength]] = {
    "gov_devouring_swarm": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "gov_purity_assembly": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "gov_purity_order": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
    "gov_machine_terminator": (Archetype.EXTERMINATION, EvidenceStrength.HARD),
}

_ORIGIN_MARKERS: Mapping[str, tuple[Archetype, EvidenceStrength]] = {
    "origin_common_ground": (Archetype.DIPLOMATIC, EvidenceStrength.STRONG),
    "origin_hegemon": (Archetype.CONQUEST, EvidenceStrength.STRONG),
}

_BEHAVIOR_MARKERS: Mapping[str, Archetype] = {
    "purger": Archetype.EXTERMINATION,
    "attack_neutrals": Archetype.EXTERMINATION,
    "conqueror": Archetype.CONQUEST,
    "subjugator": Archetype.CONQUEST,
    "dominator": Archetype.CONQUEST,
    "propagator": Archetype.CONQUEST,
    "isolationist": Archetype.DEFENSIVE,
    "liberator": Archetype.DIPLOMATIC,
    "multispecies": Archetype.DIPLOMATIC,
    "uplifter": Archetype.DIPLOMATIC,
}

PEGASUS_444_PERSONALITY_SHA256 = (
    "1F89C8D6C9444F575526A8635DB59DF78140AD43401538214E6B62F685298BAA"
)
SAVE_2270_04_15_SHA256 = (
    "7E49527196CAA35DCCD5FB22FF24E77C08A1EEA84C9263A52E87DF95492784B7"
)
OUTSIDE_PRIMARY_PERSONALITIES = frozenset(
    {
        "galactic_defense_force",
        "imperial_origin_overlord_ai",
        "decadent_capitalists",
    }
)
REVIEWED_444_PERSONALITY_IDS = (
    frozenset(_PERSONALITY_MARKERS) | OUTSIDE_PRIMARY_PERSONALITIES
)


def _empty_evidence() -> dict[Archetype, dict[str, object]]:
    return {
        archetype: {
            EvidenceStrength.HARD.value: 0,
            EvidenceStrength.STRONG.value: 0,
            EvidenceStrength.SUPPORTING.value: 0,
            "ethic_pressure_units": 0,
            "reasons": set(),
        }
        for archetype in _ARCHETYPE_PRECEDENCE
    }


def _add_evidence(
    working: dict[Archetype, dict[str, object]],
    archetype: Archetype,
    strength: EvidenceStrength,
    reason: str,
) -> None:
    row = working[archetype]
    row[strength.value] = int(row[strength.value]) + 1
    reasons = row["reasons"]
    assert isinstance(reasons, set)
    reasons.add(reason)


def _materialize_evidence(
    working: dict[Archetype, dict[str, object]],
) -> tuple[ArchetypeEvidence, ...]:
    result: list[ArchetypeEvidence] = []
    for archetype in _ARCHETYPE_PRECEDENCE:
        row = working[archetype]
        reasons = row["reasons"]
        assert isinstance(reasons, set)
        result.append(
            ArchetypeEvidence(
                archetype=archetype,
                counts=EvidenceCounts(
                    hard=int(row[EvidenceStrength.HARD.value]),
                    strong=int(row[EvidenceStrength.STRONG.value]),
                    supporting=int(row[EvidenceStrength.SUPPORTING.value]),
                ),
                ethic_pressure_units=int(row["ethic_pressure_units"]),
                reason_codes=tuple(reasons),
            )
        )
    return tuple(result)


def _record_marker(
    working: dict[Archetype, dict[str, object]],
    marker_map: Mapping[str, tuple[Archetype, EvidenceStrength]],
    source_kind: str,
    value: str | None,
) -> None:
    if value is None or value not in marker_map:
        return
    archetype, strength = marker_map[value]
    _add_evidence(
        working, archetype, strength, f"{source_kind}:{value}:{strength.value}"
    )


def _record_ethic_marker(
    working: dict[Archetype, dict[str, object]], value: str
) -> None:
    marker = _ETHIC_MARKERS.get(value)
    if marker is None:
        return
    archetype, strength = marker
    _add_evidence(working, archetype, strength, f"ethic:{value}:{strength.value}")
    units = 3 if value.startswith("ethic_fanatic_") else 1
    working[archetype]["ethic_pressure_units"] = (
        int(working[archetype]["ethic_pressure_units"]) + units
    )


def classify_nation(identity: NationIdentity) -> NationClassification:
    """Classify one static identity with deterministic tier-count evidence."""

    working = _empty_evidence()
    if identity.country_type != "default":
        return NationClassification(
            status=ClassificationStatus.EXCLUDED,
            primary=None,
            secondary=(),
            evidence=_materialize_evidence(working),
            reason_codes=(f"country_type:{identity.country_type}:excluded",),
        )
    if identity.is_nomadic is TriState.TRUE:
        return NationClassification(
            status=ClassificationStatus.EXCLUDED,
            primary=None,
            secondary=(),
            evidence=_materialize_evidence(working),
            reason_codes=("identity:nomadic:excluded",),
        )

    _record_marker(
        working, _PERSONALITY_MARKERS, "personality", identity.personality_id
    )
    for ethic in identity.ethics:
        _record_ethic_marker(working, ethic)
    for civic in identity.civics:
        _record_marker(working, _CIVIC_MARKERS, "civic", civic)
    for perk in identity.ascension_perks:
        _record_marker(working, _ASCENSION_PERK_MARKERS, "ascension_perk", perk)
    _record_marker(working, _AUTHORITY_MARKERS, "authority", identity.authority)
    _record_marker(working, _GOVERNMENT_MARKERS, "government", identity.government)
    _record_marker(working, _ORIGIN_MARKERS, "origin", identity.origin)
    if identity.is_wilderness is TriState.TRUE:
        _add_evidence(
            working,
            Archetype.GESTALT_GROWTH,
            EvidenceStrength.STRONG,
            "identity:wilderness:strong",
        )

    if identity.personality is not None:
        behavior_strength = (
            EvidenceStrength.STRONG
            if identity.personality.source
            is PersonalitySource.SAVE_TIME_WINNER_VERIFIED
            else EvidenceStrength.SUPPORTING
        )
        for behavior in identity.personality.behaviors:
            archetype = _BEHAVIOR_MARKERS.get(behavior)
            if archetype is not None:
                _add_evidence(
                    working,
                    archetype,
                    behavior_strength,
                    f"behavior:{behavior}:{behavior_strength.value}",
                )

    evidence = _materialize_evidence(working)
    hard_archetypes = tuple(item.archetype for item in evidence if item.counts.hard)
    if len(hard_archetypes) > 1:
        return NationClassification(
            status=ClassificationStatus.CONFLICT,
            primary=None,
            secondary=(),
            evidence=evidence,
            reason_codes=tuple(
                f"hard_conflict:{archetype.value}" for archetype in hard_archetypes
            ),
        )

    active = [item for item in evidence if item.counts.positive]
    if not active:
        return NationClassification(
            status=ClassificationStatus.INSUFFICIENT_EVIDENCE,
            primary=Archetype.BALANCED,
            secondary=(),
            evidence=evidence,
            reason_codes=("identity:no_recognized_markers:balanced_fallback",),
        )

    ordered = sorted(
        active,
        key=lambda item: (
            -item.counts.hard,
            -item.counts.strong,
            -item.counts.supporting,
            _ARCHETYPE_INDEX[item.archetype],
        ),
    )
    return NationClassification(
        status=ClassificationStatus.CLASSIFIED,
        primary=ordered[0].archetype,
        secondary=tuple(item.archetype for item in ordered[1:]),
        evidence=evidence,
        reason_codes=(f"primary:{ordered[0].archetype.value}",),
    )


@dataclass(frozen=True)
class StrategicContext:
    threat: TriState = TriState.UNKNOWN
    at_war: TriState = TriState.UNKNOWN
    boxed_in: TriState = TriState.UNKNOWN
    peaceful_expansion_available: TriState = TriState.UNKNOWN
    legal_claim_target: TriState = TriState.UNKNOWN
    legal_conquest_target: TriState = TriState.UNKNOWN
    economic_recovery_required: TriState = TriState.UNKNOWN
    post_completion_runway_safe: TriState = TriState.UNKNOWN
    fleet_ship_count: int | None = None
    template_count: int | None = None
    template_target_size: int | None = None
    template_current_size: int | None = None
    naval_capacity_used: Decimal | None = None
    naval_capacity: Decimal | None = None
    shipyard_capacity: int | None = None
    shipyard_queued: int | None = None
    tracked_resource_capacity: Decimal | None = None
    tracked_resource_use: Decimal | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "threat",
            "at_war",
            "boxed_in",
            "peaceful_expansion_available",
            "legal_claim_target",
            "legal_conquest_target",
            "economic_recovery_required",
            "post_completion_runway_safe",
        ):
            if not isinstance(getattr(self, field_name), TriState):
                raise TypeError(f"{field_name} must use TriState")
        for field_name in (
            "fleet_ship_count",
            "template_count",
            "template_target_size",
            "template_current_size",
            "shipyard_capacity",
            "shipyard_queued",
        ):
            _validate_count(getattr(self, field_name), label=field_name)
        for field_name in (
            "naval_capacity_used",
            "naval_capacity",
            "tracked_resource_capacity",
            "tracked_resource_use",
        ):
            object.__setattr__(
                self,
                field_name,
                _decimal_or_none(getattr(self, field_name), label=field_name),
            )


@dataclass(frozen=True)
class DerivedStrategicState:
    fleet_presence: FleetPresence
    template_state: TemplateState
    shipyard_state: ShipyardState
    naval_headroom_state: NavalHeadroomState
    naval_headroom: Decimal | None
    resource_capacity_state: ResourceCapacityState
    resource_use_state: ResourceUseState
    serialized_reinforcement_demand: int | None
    template_creation_gap: TriState
    template_expansion_gap: TriState


def derive_strategic_state(context: StrategicContext) -> DerivedStrategicState:
    """Derive threshold-free structural observations from one context."""

    if context.fleet_ship_count is None:
        fleet_presence = FleetPresence.UNKNOWN
    elif context.fleet_ship_count == 0:
        fleet_presence = FleetPresence.NONE
    else:
        fleet_presence = FleetPresence.PRESENT

    if context.template_count is None:
        template_state = TemplateState.UNKNOWN
        reinforcement_demand = None
        creation_gap = TriState.UNKNOWN
    elif context.template_count == 0:
        template_state = TemplateState.ABSENT
        reinforcement_demand = 0
        creation_gap = TriState.TRUE
    elif context.template_target_size is None or context.template_current_size is None:
        template_state = TemplateState.UNKNOWN
        reinforcement_demand = None
        creation_gap = TriState.FALSE
    else:
        difference = context.template_target_size - context.template_current_size
        reinforcement_demand = max(0, difference)
        creation_gap = TriState.FALSE
        if difference > 0:
            template_state = TemplateState.UNDERFILLED
        elif difference == 0:
            template_state = TemplateState.FILLED
        else:
            template_state = TemplateState.OVERFILLED

    if context.shipyard_capacity is None or (
        context.shipyard_capacity > 0 and context.shipyard_queued is None
    ):
        shipyard_state = ShipyardState.UNKNOWN
    elif context.shipyard_capacity == 0:
        shipyard_state = ShipyardState.NONE
    elif context.shipyard_queued == 0:
        shipyard_state = ShipyardState.IDLE
    elif context.shipyard_queued is not None and (
        context.shipyard_queued >= context.shipyard_capacity
    ):
        shipyard_state = ShipyardState.SATURATED
    else:
        shipyard_state = ShipyardState.ACTIVE

    if context.naval_capacity is None or context.naval_capacity_used is None:
        naval_headroom_state = NavalHeadroomState.UNKNOWN
        naval_headroom = None
    else:
        naval_headroom = max(
            Decimal("0"), context.naval_capacity - context.naval_capacity_used
        )
        naval_headroom_state = (
            NavalHeadroomState.AVAILABLE
            if naval_headroom > 0
            else NavalHeadroomState.NONE
        )

    if context.tracked_resource_capacity is None:
        resource_capacity_state = ResourceCapacityState.UNKNOWN
    elif context.tracked_resource_capacity == 0:
        resource_capacity_state = ResourceCapacityState.ZERO
    else:
        resource_capacity_state = ResourceCapacityState.POSITIVE

    if context.tracked_resource_use is None:
        resource_use_state = ResourceUseState.UNKNOWN
    elif context.tracked_resource_use == 0:
        resource_use_state = ResourceUseState.UNUSED
    else:
        resource_use_state = ResourceUseState.IN_USE

    if template_state is not TemplateState.FILLED:
        expansion_gap = (
            TriState.FALSE
            if template_state is not TemplateState.UNKNOWN
            else TriState.UNKNOWN
        )
    elif (
        shipyard_state is ShipyardState.UNKNOWN
        or naval_headroom_state is NavalHeadroomState.UNKNOWN
    ):
        expansion_gap = TriState.UNKNOWN
    elif (
        shipyard_state is ShipyardState.IDLE
        and naval_headroom_state is NavalHeadroomState.AVAILABLE
    ):
        expansion_gap = TriState.TRUE
    else:
        expansion_gap = TriState.FALSE

    return DerivedStrategicState(
        fleet_presence=fleet_presence,
        template_state=template_state,
        shipyard_state=shipyard_state,
        naval_headroom_state=naval_headroom_state,
        naval_headroom=naval_headroom,
        resource_capacity_state=resource_capacity_state,
        resource_use_state=resource_use_state,
        serialized_reinforcement_demand=reinforcement_demand,
        template_creation_gap=creation_gap,
        template_expansion_gap=expansion_gap,
    )


@dataclass(frozen=True)
class NationPolicy:
    lane_pressure: tuple[tuple[Lane, PressureLevel], ...]
    fleet: FleetPolicy
    research: ResearchPolicy
    expansion: ExpansionPolicy
    defense: DefensePolicy
    diplomacy: DiplomacyPolicy
    derived: DerivedStrategicState
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if tuple(lane for lane, _ in self.lane_pressure) != tuple(Lane):
            raise ValueError("lane pressure must contain every lane in canonical order")
        object.__setattr__(self, "reason_codes", _canonical_tokens(self.reason_codes))

    def pressure_for(self, lane: Lane) -> PressureLevel:
        return self.lane_pressure[list(Lane).index(lane)][1]


_PRIMARY_LANE_PRESSURE: Mapping[Archetype, Mapping[Lane, PressureLevel]] = {
    Archetype.EXTERMINATION: {
        Lane.NEW_HULLS: PressureLevel.EMPHASIZE,
        Lane.WAR_PREPARATION: PressureLevel.EMPHASIZE,
        Lane.DEFENSE: PressureLevel.EMPHASIZE,
        Lane.RESEARCH: PressureLevel.EMPHASIZE,
    },
    Archetype.CONQUEST: {
        Lane.NEW_HULLS: PressureLevel.EMPHASIZE,
        Lane.CLAIMS: PressureLevel.EMPHASIZE,
        Lane.WAR_PREPARATION: PressureLevel.EMPHASIZE,
        Lane.DEFENSE: PressureLevel.EMPHASIZE,
    },
    Archetype.GESTALT_GROWTH: {
        Lane.COLONIZATION: PressureLevel.EMPHASIZE,
        Lane.EXPANSION: PressureLevel.EMPHASIZE,
        Lane.PLANETARY_DEVELOPMENT: PressureLevel.EMPHASIZE,
        Lane.RESEARCH: PressureLevel.EMPHASIZE,
    },
    Archetype.DEFENSIVE: {
        Lane.DEFENSE: PressureLevel.EMPHASIZE,
        Lane.RESEARCH: PressureLevel.EMPHASIZE,
        Lane.CLAIMS: PressureLevel.SUPPRESS,
        Lane.WAR_PREPARATION: PressureLevel.DEEMPHASIZE,
    },
    Archetype.RESEARCH: {
        Lane.RESEARCH: PressureLevel.EMPHASIZE,
        Lane.PLANETARY_DEVELOPMENT: PressureLevel.EMPHASIZE,
    },
    Archetype.DIPLOMATIC: {
        Lane.RESEARCH: PressureLevel.EMPHASIZE,
        Lane.COLONIZATION: PressureLevel.EMPHASIZE,
        Lane.EXPANSION: PressureLevel.EMPHASIZE,
        Lane.CLAIMS: PressureLevel.SUPPRESS,
        Lane.WAR_PREPARATION: PressureLevel.DEEMPHASIZE,
    },
    Archetype.BALANCED: {},
}

_SECONDARY_LANE_PRESSURE: Mapping[Archetype, tuple[Lane, ...]] = {
    Archetype.EXTERMINATION: (Lane.NEW_HULLS, Lane.WAR_PREPARATION),
    Archetype.CONQUEST: (Lane.NEW_HULLS, Lane.CLAIMS, Lane.WAR_PREPARATION),
    Archetype.GESTALT_GROWTH: (Lane.COLONIZATION, Lane.EXPANSION),
    Archetype.DEFENSIVE: (Lane.DEFENSE,),
    Archetype.RESEARCH: (Lane.RESEARCH,),
    Archetype.DIPLOMATIC: (Lane.RESEARCH, Lane.EXPANSION),
    Archetype.BALANCED: (),
}


def pressure_rank(value: PressureLevel) -> int:
    """Return the stable ordinal rank without exposing a gameplay priority value."""

    return _PRESSURE_INDEX[value]


def _raise_pressure(
    pressures: dict[Lane, PressureLevel], lane: Lane, target: PressureLevel
) -> None:
    if pressure_rank(target) > pressure_rank(pressures[lane]):
        pressures[lane] = target


def _cap_pressure(
    pressures: dict[Lane, PressureLevel], lane: Lane, cap: PressureLevel
) -> None:
    if pressure_rank(pressures[lane]) > pressure_rank(cap):
        pressures[lane] = cap


def _profile_behaviors(identity: NationIdentity) -> frozenset[str]:
    if identity.personality is None:
        return frozenset()
    return frozenset(identity.personality.behaviors)


def build_nation_policy(
    identity: NationIdentity,
    classification: NationClassification,
    context: StrategicContext,
) -> NationPolicy:
    """Build bounded categorical pressure without changing feasibility or legality."""

    derived = derive_strategic_state(context)
    pressures = {lane: PressureLevel.NEUTRAL for lane in Lane}
    reasons: set[str] = set()

    if classification.status in {
        ClassificationStatus.EXCLUDED,
        ClassificationStatus.CONFLICT,
    }:
        reasons.add(f"classification:{classification.status.value}:neutral")
        return NationPolicy(
            lane_pressure=tuple((lane, pressures[lane]) for lane in Lane),
            fleet=FleetPolicy.HOLD,
            research=ResearchPolicy.HOLD,
            expansion=ExpansionPolicy.NONE,
            defense=DefensePolicy.NORMAL,
            diplomacy=DiplomacyPolicy.TRANSACTIONAL,
            derived=derived,
            reason_codes=tuple(reasons),
        )
    if classification.status is ClassificationStatus.INSUFFICIENT_EVIDENCE:
        reasons.add("classification:insufficient_evidence:balanced_fallback")

    assert classification.primary is not None
    primary = classification.primary
    primary_map = _PRIMARY_LANE_PRESSURE[primary]
    for lane, pressure in primary_map.items():
        pressures[lane] = pressure
    primary_suppressed = {
        lane
        for lane, pressure in primary_map.items()
        if pressure is PressureLevel.SUPPRESS
    }
    for archetype in classification.secondary:
        for lane in _SECONDARY_LANE_PRESSURE[archetype]:
            if lane not in primary_suppressed:
                _raise_pressure(pressures, lane, PressureLevel.EMPHASIZE)

    research = (
        ResearchPolicy.LEAD
        if primary is Archetype.RESEARCH
        else ResearchPolicy.PRESERVE
    )
    defense = (
        DefensePolicy.FRONTIER
        if primary is Archetype.DEFENSIVE or context.boxed_in is TriState.TRUE
        else DefensePolicy.NORMAL
    )
    behaviors = _profile_behaviors(identity)
    if primary is Archetype.EXTERMINATION:
        diplomacy = DiplomacyPolicy.EXTERMINATING
    elif "liberator" in behaviors:
        diplomacy = DiplomacyPolicy.LIBERATING
    elif "subjugator" in behaviors:
        diplomacy = DiplomacyPolicy.SUBJUGATING
    elif primary is Archetype.DIPLOMATIC:
        diplomacy = DiplomacyPolicy.COOPERATIVE
    else:
        diplomacy = DiplomacyPolicy.TRANSACTIONAL

    military_identity = bool(
        {primary, *classification.secondary}
        & {Archetype.EXTERMINATION, Archetype.CONQUEST}
    )
    safe_to_expand_fleet = (
        context.economic_recovery_required is TriState.FALSE
        and context.post_completion_runway_safe is TriState.TRUE
        and derived.naval_headroom_state is NavalHeadroomState.AVAILABLE
        and derived.shipyard_state is ShipyardState.IDLE
    )
    fleet = FleetPolicy.HOLD
    if context.at_war is TriState.TRUE:
        _raise_pressure(pressures, Lane.DEFENSE, PressureLevel.EMPHASIZE)
        _raise_pressure(pressures, Lane.NEW_HULLS, PressureLevel.EMPHASIZE)
        _raise_pressure(pressures, Lane.WAR_PREPARATION, PressureLevel.EMPHASIZE)
        reasons.add("war:replacement_raised")
        if context.post_completion_runway_safe is TriState.TRUE:
            fleet = FleetPolicy.REPLACE
    if context.threat is TriState.TRUE:
        defense = DefensePolicy.EMERGENCY
        _raise_pressure(pressures, Lane.DEFENSE, PressureLevel.URGENT)
        _raise_pressure(pressures, Lane.NEW_HULLS, PressureLevel.EMPHASIZE)
        reasons.add("threat:defense_raised")
        if context.post_completion_runway_safe is TriState.TRUE:
            fleet = FleetPolicy.EMERGENCY_DEFENSE

    if military_identity and safe_to_expand_fleet and fleet is FleetPolicy.HOLD:
        if derived.template_creation_gap is TriState.TRUE:
            fleet = FleetPolicy.EXPAND
            _raise_pressure(pressures, Lane.NEW_HULLS, PressureLevel.URGENT)
            reasons.add("fleet:template_creation_gap")
        elif derived.template_expansion_gap is TriState.TRUE:
            fleet = FleetPolicy.EXPAND
            _raise_pressure(pressures, Lane.NEW_HULLS, PressureLevel.URGENT)
            reasons.add("fleet:template_expansion_gap")

    expansion = ExpansionPolicy.NONE
    if (
        context.economic_recovery_required is TriState.FALSE
        and context.post_completion_runway_safe is TriState.TRUE
    ):
        if (
            primary in {Archetype.EXTERMINATION, Archetype.CONQUEST}
            and context.legal_conquest_target is TriState.TRUE
        ):
            expansion = ExpansionPolicy.CONQUEST
        elif (
            primary is Archetype.CONQUEST
            and context.legal_claim_target is TriState.TRUE
        ):
            expansion = ExpansionPolicy.CLAIM
        elif context.peaceful_expansion_available is TriState.TRUE:
            expansion = ExpansionPolicy.PEACEFUL

    if context.legal_claim_target is not TriState.TRUE:
        pressures[Lane.CLAIMS] = PressureLevel.SUPPRESS
        reasons.add("legal:no_verified_claim_target")
    if expansion is ExpansionPolicy.NONE:
        pressures[Lane.EXPANSION] = PressureLevel.SUPPRESS
        pressures[Lane.COLONIZATION] = PressureLevel.SUPPRESS
        reasons.add("legal:no_verified_expansion_route")

    if context.economic_recovery_required is TriState.TRUE:
        _raise_pressure(pressures, Lane.STRATEGIC_PRODUCER, PressureLevel.URGENT)
        _raise_pressure(pressures, Lane.MARKET_BRIDGE, PressureLevel.EMPHASIZE)
        for lane in Lane:
            if lane not in {Lane.STRATEGIC_PRODUCER, Lane.MARKET_BRIDGE}:
                cap = (
                    PressureLevel.EMPHASIZE
                    if lane is Lane.DEFENSE and context.threat is TriState.TRUE
                    else PressureLevel.DEEMPHASIZE
                )
                _cap_pressure(pressures, lane, cap)
        fleet = (
            FleetPolicy.REPLACE
            if context.threat is TriState.TRUE
            and context.post_completion_runway_safe is TriState.TRUE
            else FleetPolicy.HOLD
        )
        expansion = ExpansionPolicy.NONE
        research = ResearchPolicy.PRESERVE
        reasons.add("recovery:dominates_preferences")

    if context.post_completion_runway_safe is TriState.FALSE:
        _raise_pressure(pressures, Lane.STRATEGIC_PRODUCER, PressureLevel.URGENT)
        _raise_pressure(pressures, Lane.MARKET_BRIDGE, PressureLevel.EMPHASIZE)
        for lane in Lane:
            if lane not in {Lane.STRATEGIC_PRODUCER, Lane.MARKET_BRIDGE}:
                pressures[lane] = PressureLevel.SUPPRESS
        fleet = FleetPolicy.HOLD
        expansion = ExpansionPolicy.NONE
        research = ResearchPolicy.PRESERVE
        reasons.add("runway:unsafe_suppresses_discretionary_pressure")

    return NationPolicy(
        lane_pressure=tuple((lane, pressures[lane]) for lane in Lane),
        fleet=fleet,
        research=research,
        expansion=expansion,
        defense=defense,
        diplomacy=diplomacy,
        derived=derived,
        reason_codes=tuple(reasons),
    )
