"""Pure, deterministic cross-priority economic model for bounded fixtures.

The module deliberately does no file or game I/O.  It models evidence that can
be known from a checkpoint and marks unsupported trigger facts indeterminate.
Feasibility is policy-neutral; policy activation and priority selection are
separate steps so a policy cannot make an impossible project look affordable.

All numeric state is normalized to :class:`~decimal.Decimal`.  That keeps
counterfactual runs exactly comparable and avoids platform-dependent float
drift in future CSV adapters.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from decimal import Context, Decimal, InvalidOperation, localcontext
from enum import Enum
from functools import wraps
from itertools import combinations
from typing import Callable, Iterable, Mapping, ParamSpec, TypeAlias, TypeVar


Number: TypeAlias = Decimal | int | float | str
ZERO = Decimal("0")
ONE = Decimal("1")
_MODEL_DECIMAL_CONTEXT = Context(prec=64)
_P = ParamSpec("_P")
_R = TypeVar("_R")


def _model_decimal_context(function: Callable[_P, _R]) -> Callable[_P, _R]:
    @wraps(function)
    def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        with localcontext(_MODEL_DECIMAL_CONTEXT):
            return function(*args, **kwargs)

    return wrapped


def _decimal(value: Number, *, label: str = "value") -> Decimal:
    if isinstance(value, bool):
        raise TypeError(f"{label} must be numeric, not bool")
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{label} is not a valid decimal: {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"{label} must be finite: {value!r}")
    return result


@dataclass(frozen=True)
class QuantityVector:
    """Immutable, canonical key/value quantities with explicit known zeroes."""

    values: tuple[tuple[str, Decimal], ...] = ()

    def __post_init__(self) -> None:
        normalized: dict[str, Decimal] = {}
        for key, value in self.values:
            if not key:
                raise ValueError("quantity keys must be non-empty")
            if key in normalized:
                raise ValueError(f"duplicate quantity key: {key}")
            normalized[key] = _decimal(value, label=key)
        object.__setattr__(self, "values", tuple(sorted(normalized.items())))

    @classmethod
    def from_mapping(cls, values: Mapping[str, Number]) -> QuantityVector:
        return cls(tuple((key, _decimal(value, label=key)) for key, value in values.items()))

    def get(self, key: str, default: Number = ZERO) -> Decimal:
        fallback = _decimal(default, label=f"default for {key}")
        for candidate, value in self.values:
            if candidate == key:
                return value
        return fallback

    def contains(self, key: str) -> bool:
        return any(candidate == key for candidate, _ in self.values)

    def keys(self) -> tuple[str, ...]:
        return tuple(key for key, _ in self.values)

    @_model_decimal_context
    def plus(self, *others: QuantityVector) -> QuantityVector:
        terms: dict[str, list[Decimal]] = {}
        for vector in (self, *others):
            for key, value in vector.values:
                terms.setdefault(key, []).append(value)
        result = {
            key: sum(sorted(values), start=ZERO)
            for key, values in terms.items()
        }
        return QuantityVector(tuple(result.items()))

    @_model_decimal_context
    def minus(self, other: QuantityVector) -> QuantityVector:
        result = dict(self.values)
        for key, value in other.values:
            result[key] = result.get(key, ZERO) - value
        return QuantityVector(tuple(result.items()))

    def with_value(self, key: str, value: Number) -> QuantityVector:
        result = dict(self.values)
        result[key] = _decimal(value, label=key)
        return QuantityVector(tuple(result.items()))


def _sum_vectors(vectors: Iterable[QuantityVector]) -> QuantityVector:
    total = QuantityVector()
    for vector in vectors:
        total = total.plus(vector)
    return total


def _validate_nonnegative(vector: QuantityVector, *, label: str) -> None:
    for key, value in vector.values:
        if value < ZERO:
            raise ValueError(f"{label}.{key} must be non-negative")


class Truth(str, Enum):
    TRUE = "true"
    FALSE = "false"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True)
class FactSet:
    """Immutable tri-state facts; a missing atom is indeterminate."""

    values: tuple[tuple[str, Truth], ...] = ()

    def __post_init__(self) -> None:
        normalized: dict[str, Truth] = {}
        for key, value in self.values:
            if not key:
                raise ValueError("fact names must be non-empty")
            if key in normalized:
                raise ValueError(f"duplicate fact: {key}")
            if not isinstance(value, Truth):
                raise TypeError(f"fact {key} must use Truth, got {value!r}")
            normalized[key] = value
        object.__setattr__(self, "values", tuple(sorted(normalized.items())))

    @classmethod
    def from_mapping(cls, values: Mapping[str, Truth]) -> FactSet:
        return cls(tuple(values.items()))

    def get(self, key: str) -> Truth:
        for candidate, value in self.values:
            if candidate == key:
                return value
        return Truth.INDETERMINATE

    def with_value(self, key: str, value: Truth) -> FactSet:
        result = dict(self.values)
        result[key] = value
        return FactSet(tuple(result.items()))


@dataclass(frozen=True)
class Atom:
    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("trigger atom names must be non-empty")


@dataclass(frozen=True)
class AllOf:
    terms: tuple[Trigger, ...] = ()


@dataclass(frozen=True)
class AnyOf:
    terms: tuple[Trigger, ...] = ()


@dataclass(frozen=True)
class Not:
    term: Trigger


Trigger: TypeAlias = Atom | AllOf | AnyOf | Not
ALWAYS = AllOf()


def evaluate_trigger(trigger: Trigger, facts: FactSet) -> Truth:
    """Evaluate a trigger with strong Kleene three-valued logic."""

    if isinstance(trigger, Atom):
        return facts.get(trigger.name)
    if isinstance(trigger, Not):
        value = evaluate_trigger(trigger.term, facts)
        if value is Truth.TRUE:
            return Truth.FALSE
        if value is Truth.FALSE:
            return Truth.TRUE
        return Truth.INDETERMINATE
    if isinstance(trigger, AllOf):
        values = tuple(evaluate_trigger(term, facts) for term in trigger.terms)
        if any(value is Truth.FALSE for value in values):
            return Truth.FALSE
        if all(value is Truth.TRUE for value in values):
            return Truth.TRUE
        return Truth.INDETERMINATE
    if isinstance(trigger, AnyOf):
        values = tuple(evaluate_trigger(term, facts) for term in trigger.terms)
        if any(value is Truth.TRUE for value in values):
            return Truth.TRUE
        if all(value is Truth.FALSE for value in values):
            return Truth.FALSE
        return Truth.INDETERMINATE
    raise TypeError(f"unsupported trigger node: {type(trigger).__name__}")


class Lane(str, Enum):
    COLONIZATION = "colonization"
    EXPANSION = "expansion"
    PLANETARY_DEVELOPMENT = "planetary_development"
    RESEARCH = "research"
    NEW_HULLS = "new_hulls"
    UPGRADES = "upgrades"
    CLAIMS = "claims"
    DEFENSE = "defense"
    WAR_PREPARATION = "war_preparation"
    STRATEGIC_PRODUCER = "strategic_producer"
    MARKET_BRIDGE = "market_bridge"
    MEGASTRUCTURE = "megastructure"


@dataclass(frozen=True)
class Project:
    """One legal candidate competing for resources and planning capacity."""

    project_id: str
    lane: Lane
    base_priority: Decimal
    one_time_cost: QuantityVector = field(default_factory=QuantityVector)
    budget_cost: QuantityVector = field(default_factory=QuantityVector)
    influence_cost: Decimal = ZERO
    queue: str | None = None
    queue_slots: Decimal = ONE
    slot_cost: QuantityVector = field(default_factory=QuantityVector)
    job_cost: QuantityVector = field(default_factory=QuantityVector)
    duration_months: int = 1
    completion_income: QuantityVector = field(default_factory=QuantityVector)
    completion_upkeep: QuantityVector = field(default_factory=QuantityVector)
    required_gates: frozenset[str] = frozenset()
    forbidden_gates: frozenset[str] = frozenset()
    add_gates: frozenset[str] = frozenset()
    remove_gates: frozenset[str] = frozenset()
    trigger: Trigger = ALWAYS
    strategic_resource: str | None = None
    repeatable: bool = False

    @_model_decimal_context
    def __post_init__(self) -> None:
        if not self.project_id:
            raise ValueError("project_id must be non-empty")
        if not isinstance(self.lane, Lane):
            raise TypeError("lane must be a Lane")
        object.__setattr__(
            self, "base_priority", _decimal(self.base_priority, label="base_priority")
        )
        object.__setattr__(
            self, "influence_cost", _decimal(self.influence_cost, label="influence_cost")
        )
        object.__setattr__(
            self, "queue_slots", _decimal(self.queue_slots, label="queue_slots")
        )
        for label, vector in (
            ("one_time_cost", self.one_time_cost),
            ("budget_cost", self.budget_cost),
            ("slot_cost", self.slot_cost),
            ("job_cost", self.job_cost),
            ("completion_income", self.completion_income),
            ("completion_upkeep", self.completion_upkeep),
        ):
            _validate_nonnegative(vector, label=label)
        if self.influence_cost < ZERO:
            raise ValueError("influence_cost must be non-negative")
        if self.queue_slots <= ZERO:
            raise ValueError("queue_slots must be positive")
        if self.duration_months < 1:
            raise ValueError("duration_months must be at least one")
        if self.required_gates & self.forbidden_gates:
            raise ValueError("a project cannot require and forbid the same gate")
        if self.add_gates & self.remove_gates:
            raise ValueError("a project cannot add and remove the same gate")
        if self.strategic_resource == "":
            raise ValueError("strategic_resource must be non-empty when supplied")
        if self.strategic_resource is not None:
            net_output = self.completion_income.get(
                self.strategic_resource
            ) - self.completion_upkeep.get(self.strategic_resource)
            if net_output <= ZERO:
                raise ValueError(
                    "a strategic producer must add positive net output for "
                    f"{self.strategic_resource}"
                )


@dataclass(frozen=True)
class PendingProject:
    project: Project
    completes_at_month: int

    def __post_init__(self) -> None:
        if self.completes_at_month < 1:
            raise ValueError("completion month must be positive")


@dataclass(frozen=True)
class EconomicState:
    """Immutable checkpoint at the start of a month."""

    month: int = 0
    stockpile: QuantityVector = field(default_factory=QuantityVector)
    capacity: QuantityVector = field(default_factory=QuantityVector)
    earned_income: QuantityVector = field(default_factory=QuantityVector)
    market_income: QuantityVector = field(default_factory=QuantityVector)
    active_upkeep: QuantityVector = field(default_factory=QuantityVector)
    budgets: QuantityVector = field(default_factory=QuantityVector)
    queue_capacity: QuantityVector = field(default_factory=QuantityVector)
    queue_used: QuantityVector = field(default_factory=QuantityVector)
    slot_capacity: QuantityVector = field(default_factory=QuantityVector)
    slot_used: QuantityVector = field(default_factory=QuantityVector)
    job_capacity: QuantityVector = field(default_factory=QuantityVector)
    job_used: QuantityVector = field(default_factory=QuantityVector)
    influence: Decimal = ZERO
    deficit_status: FactSet = field(default_factory=FactSet)
    unlocked_resources: frozenset[str] = frozenset()
    gates: frozenset[str] = frozenset()
    pending: tuple[PendingProject, ...] = ()
    started_projects: frozenset[str] = frozenset()
    completed_projects: frozenset[str] = frozenset()

    @_model_decimal_context
    def __post_init__(self) -> None:
        if self.month < 0:
            raise ValueError("month must be non-negative")
        ordered_pending = tuple(
            sorted(
                self.pending,
                key=lambda item: (
                    item.completes_at_month,
                    item.project.project_id,
                ),
            )
        )
        object.__setattr__(self, "pending", ordered_pending)
        nonrepeatable_pending = [
            item.project.project_id
            for item in ordered_pending
            if not item.project.repeatable
        ]
        if len(set(nonrepeatable_pending)) != len(nonrepeatable_pending):
            raise ValueError("a nonrepeatable project cannot be pending twice")
        object.__setattr__(
            self,
            "started_projects",
            self.started_projects
            | self.completed_projects
            | frozenset(item.project.project_id for item in ordered_pending),
        )
        object.__setattr__(self, "influence", _decimal(self.influence, label="influence"))
        for label, vector in (
            ("stockpile", self.stockpile),
            ("capacity", self.capacity),
            ("earned_income", self.earned_income),
            ("market_income", self.market_income),
            ("active_upkeep", self.active_upkeep),
            ("budgets", self.budgets),
            ("queue_capacity", self.queue_capacity),
            ("queue_used", self.queue_used),
            ("slot_capacity", self.slot_capacity),
            ("slot_used", self.slot_used),
            ("job_capacity", self.job_capacity),
            ("job_used", self.job_used),
        ):
            _validate_nonnegative(vector, label=label)
        if self.influence < ZERO:
            raise ValueError("influence must be non-negative")
        for used, capacity, label in (
            (self.queue_used, self.queue_capacity, "queue"),
            (self.slot_used, self.slot_capacity, "slot"),
        ):
            for key, value in used.values:
                if value > capacity.get(key):
                    raise ValueError(f"{label} use exceeds capacity for {key}")
        pending_queue_reservations: dict[str, Decimal] = {}
        for item in ordered_pending:
            if item.project.queue is not None:
                pending_queue_reservations[item.project.queue] = (
                    pending_queue_reservations.get(item.project.queue, ZERO)
                    + item.project.queue_slots
                )
        for queue, reserved in sorted(pending_queue_reservations.items()):
            if self.queue_used.get(queue) < reserved:
                raise ValueError(
                    f"pending queue reservations exceed recorded use for {queue}"
                )
        reserved_jobs = _sum_vectors(
            item.project.job_cost for item in self.pending
        )
        for key, value in self.job_used.plus(reserved_jobs).values:
            if value > self.job_capacity.get(key):
                raise ValueError(f"job use and reservations exceed capacity for {key}")
        for key, value in self.stockpile.values:
            if self.capacity.contains(key) and value > self.capacity.get(key):
                raise ValueError(f"stockpile exceeds capacity for {key}")
        if any(item.completes_at_month <= self.month for item in ordered_pending):
            raise ValueError("pending projects must complete after the checkpoint month")


class PolicyMode(str, Enum):
    PARENT_ONLY = "parent_only"
    ACTUAL_DEFICIT = "actual_deficit"
    ACTUAL_DEFICIT_OR_RUNWAY = "actual_deficit_or_runway"
    FAILED_LOW_INCOME_TARGET = "failed_low_income_target"


@dataclass(frozen=True)
class PolicyVariant:
    name: str
    mode: PolicyMode
    income_pressure: Decimal = ZERO
    priority_bonus: Decimal = ZERO
    runway_threshold_months: Decimal | None = None
    failed_income_target: Decimal = ZERO
    commitment_horizon_months: int = 24

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("policy name must be non-empty")
        object.__setattr__(
            self,
            "income_pressure",
            _decimal(self.income_pressure, label="income_pressure"),
        )
        object.__setattr__(
            self,
            "priority_bonus",
            _decimal(self.priority_bonus, label="priority_bonus"),
        )
        object.__setattr__(
            self,
            "failed_income_target",
            _decimal(self.failed_income_target, label="failed_income_target"),
        )
        if self.runway_threshold_months is not None:
            object.__setattr__(
                self,
                "runway_threshold_months",
                _decimal(self.runway_threshold_months, label="runway_threshold_months"),
            )
        if self.income_pressure < ZERO:
            raise ValueError("income_pressure must be non-negative")
        if self.commitment_horizon_months < 1:
            raise ValueError("commitment_horizon_months must be positive")


PARENT_ONLY = PolicyVariant("parent-only", PolicyMode.PARENT_ONLY)
DEFICIT_ONLY_PLUS_ONE = PolicyVariant(
    "deficit-only-plus-one",
    PolicyMode.ACTUAL_DEFICIT,
    income_pressure=ONE,
    priority_bonus=Decimal("100"),
)
DEFICIT_ONLY_PLUS_TWO = PolicyVariant(
    "deficit-only-plus-two",
    PolicyMode.ACTUAL_DEFICIT,
    income_pressure=Decimal("2"),
    priority_bonus=Decimal("150"),
)
PREZERO_RUNWAY_PLUS_ONE = PolicyVariant(
    "prezero-runway-plus-one",
    PolicyMode.ACTUAL_DEFICIT_OR_RUNWAY,
    income_pressure=ONE,
    priority_bonus=Decimal("100"),
    runway_threshold_months=Decimal("12"),
)
FAILED_C9 = PolicyVariant(
    "failed-c9da19b3",
    PolicyMode.FAILED_LOW_INCOME_TARGET,
    income_pressure=Decimal("4500"),
    priority_bonus=Decimal("4500"),
    failed_income_target=Decimal("4500"),
)


class ActivationReason(str, Enum):
    TRIGGER_FALSE = "trigger_false"
    TRIGGER_INDETERMINATE = "trigger_indeterminate"
    PARENT_OWNS = "parent_owns"
    RESOURCE_LOCKED = "resource_locked"
    USE_UNKNOWN = "use_unknown"
    NO_ACTIVE_USE = "no_active_use"
    INCOME_UNKNOWN = "income_unknown"
    EARNED_RECOVERY = "earned_recovery"
    DEFICIT_UNKNOWN = "deficit_unknown"
    NO_ACTUAL_DEFICIT = "no_actual_deficit"
    STOCKPILE_UNKNOWN = "stockpile_unknown"
    RUNWAY_SAFE = "runway_safe"
    COMMITTED_RECOVERY = "committed_recovery"
    CANDIDATE_NOT_FASTER_THAN_COMMITTED = (
        "candidate_not_faster_than_committed"
    )
    ACTUAL_DEFICIT = "actual_deficit"
    PREZERO_RUNWAY = "prezero_runway"
    FAILED_LOW_INCOME_TARGET = "failed_low_income_target"


@dataclass(frozen=True)
class ActivationResult:
    truth: Truth
    requested_income: Decimal
    remaining_pressure: Decimal
    active_use: Decimal | None
    net_earned_income: Decimal | None
    runway_months: Decimal | None
    committed_recovery: bool
    committed_net_output: Decimal
    committed_pressure_months: int | None
    reasons: tuple[ActivationReason, ...]


def _activation(
    truth: Truth,
    reason: ActivationReason,
    *,
    requested_income: Decimal = ZERO,
    remaining_pressure: Decimal | None = None,
    active_use: Decimal | None = None,
    net_earned_income: Decimal | None = None,
    runway_months: Decimal | None = None,
    committed_recovery: bool = False,
    committed_net_output: Decimal = ZERO,
    committed_pressure_months: int | None = None,
) -> ActivationResult:
    bounded_remaining = (
        requested_income if remaining_pressure is None else remaining_pressure
    )
    return ActivationResult(
        truth=truth,
        requested_income=requested_income if truth is Truth.TRUE else ZERO,
        remaining_pressure=bounded_remaining if truth is Truth.TRUE else ZERO,
        active_use=active_use,
        net_earned_income=net_earned_income,
        runway_months=runway_months,
        committed_recovery=committed_recovery,
        committed_net_output=committed_net_output,
        committed_pressure_months=committed_pressure_months,
        reasons=(reason,),
    )


@dataclass(frozen=True)
class _PendingRecoveryOutlook:
    timely_recovery: bool
    final_net_output: Decimal
    pressure_ready_months: int | None
    first_shortage_months: int | None
    final_net_income: Decimal


def _pending_recovery_outlook(
    state: EconomicState,
    resource: str,
    *,
    horizon_months: int,
    requested_output: Decimal,
) -> _PendingRecoveryOutlook:
    """Separate durable queued output from safe time-to-recovery."""

    relevant = tuple(
        pending
        for pending in sorted(
            state.pending,
            key=lambda item: (item.completes_at_month, item.project.project_id),
        )
        if (
            pending.project.completion_income.get(resource) != ZERO
            or pending.project.completion_upkeep.get(resource) != ZERO
        )
    )

    output_events: list[tuple[int, Decimal]] = []
    for pending in relevant:
        month = pending.completes_at_month - state.month
        delta = pending.project.completion_income.get(
            resource
        ) - pending.project.completion_upkeep.get(resource)
        if output_events and output_events[-1][0] == month:
            previous_month, previous_delta = output_events[-1]
            output_events[-1] = (previous_month, previous_delta + delta)
        else:
            output_events.append((month, delta))

    output_after_events: list[tuple[int, Decimal]] = []
    committed_net_output = ZERO
    for month, delta in output_events:
        committed_net_output += delta
        output_after_events.append((month, committed_net_output))

    pressure_ready_months = None
    if requested_output > ZERO:
        for index, (month, output) in enumerate(output_after_events):
            if output >= requested_output and all(
                later_output >= requested_output
                for _, later_output in output_after_events[index:]
            ):
                pressure_ready_months = month
                break

    stockpile = state.stockpile.get(resource)
    earned_income = state.earned_income.get(resource)
    active_upkeep = state.active_upkeep.get(resource)
    unbridged_shortage = False
    first_shortage_months = None
    for offset in range(1, horizon_months + 1):
        raw_stockpile = stockpile + earned_income - active_upkeep
        if raw_stockpile < ZERO:
            if first_shortage_months is None:
                first_shortage_months = offset
            if offset > 1:
                unbridged_shortage = True
        stockpile = max(raw_stockpile, ZERO)
        if state.capacity.contains(resource):
            stockpile = min(stockpile, state.capacity.get(resource))

        completion_month = state.month + offset
        completing = tuple(
            pending
            for pending in relevant
            if pending.completes_at_month == completion_month
            and pending.completes_at_month <= state.month + horizon_months
        )
        earned_income += sum(
            sorted(
                pending.project.completion_income.get(resource)
                for pending in completing
            ),
            start=ZERO,
        )
        active_upkeep += sum(
            sorted(
                pending.project.completion_upkeep.get(resource)
                for pending in completing
            ),
            start=ZERO,
        )
    return _PendingRecoveryOutlook(
        timely_recovery=bool(relevant)
        and not unbridged_shortage
        and earned_income >= active_upkeep,
        final_net_output=committed_net_output,
        pressure_ready_months=pressure_ready_months,
        first_shortage_months=first_shortage_months,
        final_net_income=earned_income - active_upkeep,
    )


@_model_decimal_context
def evaluate_policy_activation(
    state: EconomicState,
    variant: PolicyVariant,
    resource: str,
    *,
    trigger: Trigger = ALWAYS,
    facts: FactSet = FactSet(),
) -> ActivationResult:
    """Evaluate strategic pressure from actual use, earned net, and runway.

    Capacity and absolute stockpile are never activation targets by themselves.
    Market income is intentionally excluded from ``net_earned_income`` so a
    temporary bridge cannot masquerade as a durable producer recovery.
    For bounded variants, ``income_pressure`` is the maximum increment for one
    decision pass.  Actual burn and durable queued net output reduce the
    remaining pressure instead of multiplying it once per candidate.
    """

    trigger_truth = evaluate_trigger(trigger, facts)
    if trigger_truth is Truth.FALSE:
        return _activation(Truth.FALSE, ActivationReason.TRIGGER_FALSE)
    if trigger_truth is Truth.INDETERMINATE:
        return _activation(Truth.INDETERMINATE, ActivationReason.TRIGGER_INDETERMINATE)
    if variant.mode is PolicyMode.PARENT_ONLY:
        return _activation(Truth.FALSE, ActivationReason.PARENT_OWNS)
    if resource not in state.unlocked_resources:
        return _activation(Truth.FALSE, ActivationReason.RESOURCE_LOCKED)

    if variant.mode is PolicyMode.FAILED_LOW_INCOME_TARGET:
        if not state.earned_income.contains(resource):
            return _activation(Truth.INDETERMINATE, ActivationReason.INCOME_UNKNOWN)
        earned = state.earned_income.get(resource)
        upkeep = (
            state.active_upkeep.get(resource)
            if state.active_upkeep.contains(resource)
            else None
        )
        net_earned = earned - upkeep if upkeep is not None else None
        if earned < variant.failed_income_target:
            return _activation(
                Truth.TRUE,
                ActivationReason.FAILED_LOW_INCOME_TARGET,
                requested_income=variant.income_pressure,
                active_use=upkeep,
                net_earned_income=net_earned,
            )
        return _activation(
            Truth.FALSE,
            ActivationReason.EARNED_RECOVERY,
            active_use=upkeep,
            net_earned_income=net_earned,
        )

    if not state.active_upkeep.contains(resource):
        return _activation(Truth.INDETERMINATE, ActivationReason.USE_UNKNOWN)
    active_use = state.active_upkeep.get(resource)
    if (
        active_use <= ZERO
        and variant.mode is not PolicyMode.ACTUAL_DEFICIT_OR_RUNWAY
    ):
        return _activation(
            Truth.FALSE, ActivationReason.NO_ACTIVE_USE, active_use=active_use
        )
    if not state.earned_income.contains(resource):
        return _activation(
            Truth.INDETERMINATE,
            ActivationReason.INCOME_UNKNOWN,
            active_use=active_use,
        )
    earned = state.earned_income.get(resource)
    net_earned = earned - active_use
    deficit_truth = state.deficit_status.get(resource)
    if (
        net_earned >= ZERO
        and variant.mode is PolicyMode.ACTUAL_DEFICIT_OR_RUNWAY
    ):
        outlook = _pending_recovery_outlook(
            state,
            resource,
            horizon_months=variant.commitment_horizon_months,
            requested_output=variant.income_pressure,
        )
        threshold = variant.runway_threshold_months
        if (
            outlook.first_shortage_months is not None
            and threshold is not None
            and Decimal(max(outlook.first_shortage_months - 1, 0))
            <= threshold
        ):
            projected_burn = max(-outlook.final_net_income, ZERO)
            desired_increment = (
                min(variant.income_pressure, projected_burn)
                if projected_burn > ZERO
                else variant.income_pressure
            )
            remaining_pressure = max(
                desired_increment - max(outlook.final_net_output, ZERO),
                ZERO,
            )
            return _activation(
                Truth.TRUE,
                ActivationReason.PREZERO_RUNWAY,
                requested_income=desired_increment,
                remaining_pressure=remaining_pressure,
                active_use=active_use,
                net_earned_income=net_earned,
                runway_months=Decimal(
                    max(outlook.first_shortage_months - 1, 0)
                ),
                committed_net_output=outlook.final_net_output,
                committed_pressure_months=outlook.pressure_ready_months,
            )
        if outlook.first_shortage_months is not None:
            return _activation(
                Truth.FALSE,
                ActivationReason.RUNWAY_SAFE,
                active_use=active_use,
                net_earned_income=net_earned,
                runway_months=Decimal(
                    max(outlook.first_shortage_months - 1, 0)
                ),
            )
    if active_use <= ZERO:
        return _activation(
            Truth.FALSE,
            ActivationReason.NO_ACTIVE_USE,
            active_use=active_use,
            net_earned_income=net_earned,
        )
    if net_earned >= ZERO:
        return _activation(
            Truth.FALSE,
            ActivationReason.EARNED_RECOVERY,
            active_use=active_use,
            net_earned_income=net_earned,
        )

    burn = -net_earned
    desired_increment = min(variant.income_pressure, burn)
    runway: Decimal | None = None
    if state.stockpile.contains(resource):
        runway = state.stockpile.get(resource) / burn

    outlook = _pending_recovery_outlook(
        state,
        resource,
        horizon_months=variant.commitment_horizon_months,
        requested_output=desired_increment,
    )
    remaining_pressure = max(
        desired_increment - max(outlook.final_net_output, ZERO),
        ZERO,
    )
    if outlook.timely_recovery:
        return _activation(
            Truth.FALSE,
            ActivationReason.COMMITTED_RECOVERY,
            active_use=active_use,
            net_earned_income=net_earned,
            runway_months=runway,
            committed_recovery=True,
            committed_net_output=outlook.final_net_output,
            committed_pressure_months=outlook.pressure_ready_months,
        )

    if deficit_truth is Truth.TRUE:
        return _activation(
            Truth.TRUE,
            ActivationReason.ACTUAL_DEFICIT,
            requested_income=desired_increment,
            remaining_pressure=remaining_pressure,
            active_use=active_use,
            net_earned_income=net_earned,
            runway_months=runway,
            committed_net_output=outlook.final_net_output,
            committed_pressure_months=outlook.pressure_ready_months,
        )

    if variant.mode is PolicyMode.ACTUAL_DEFICIT:
        if deficit_truth is Truth.INDETERMINATE:
            return _activation(
                Truth.INDETERMINATE,
                ActivationReason.DEFICIT_UNKNOWN,
                active_use=active_use,
                net_earned_income=net_earned,
                runway_months=runway,
            )
        return _activation(
            Truth.FALSE,
            ActivationReason.NO_ACTUAL_DEFICIT,
            active_use=active_use,
            net_earned_income=net_earned,
            runway_months=runway,
        )

    projected_runway = (
        Decimal(max(outlook.first_shortage_months - 1, 0))
        if outlook.first_shortage_months is not None
        else runway
    )
    if projected_runway is None:
        return _activation(
            Truth.INDETERMINATE,
            ActivationReason.STOCKPILE_UNKNOWN,
            active_use=active_use,
            net_earned_income=net_earned,
        )
    threshold = variant.runway_threshold_months
    if threshold is not None and projected_runway <= threshold:
        return _activation(
            Truth.TRUE,
            ActivationReason.PREZERO_RUNWAY,
            requested_income=desired_increment,
            remaining_pressure=remaining_pressure,
            active_use=active_use,
            net_earned_income=net_earned,
            runway_months=projected_runway,
            committed_net_output=outlook.final_net_output,
            committed_pressure_months=outlook.pressure_ready_months,
        )
    return _activation(
        Truth.FALSE,
        ActivationReason.RUNWAY_SAFE,
        active_use=active_use,
        net_earned_income=net_earned,
        runway_months=projected_runway,
    )


class FeasibilityCode(str, Enum):
    RESOURCE = "resource"
    BUDGET = "budget"
    QUEUE = "queue"
    SLOT = "slot"
    JOB = "job"
    INFLUENCE = "influence"
    RUNWAY = "runway"
    MISSING_GATE = "missing_gate"
    FORBIDDEN_GATE = "forbidden_gate"


@dataclass(frozen=True)
class FeasibilityReason:
    code: FeasibilityCode
    key: str
    required: Decimal
    available: Decimal
    project_ids: tuple[str, ...]


@dataclass(frozen=True)
class BundleFeasibility:
    projects: tuple[Project, ...]
    feasible: bool
    reasons: tuple[FeasibilityReason, ...]

    @property
    def project_ids(self) -> tuple[str, ...]:
        return tuple(project.project_id for project in self.projects)


@dataclass(frozen=True)
class _RunwayFailure:
    first_month: int
    cumulative_shortfall: Decimal


def _runway_failures(
    state: EconomicState,
    pending: Iterable[PendingProject],
    stockpile: QuantityVector,
    *,
    horizon_months: int,
) -> dict[str, _RunwayFailure]:
    """Project earned-income runway failures, excluding temporary market bridges."""

    ordered_pending = tuple(
        sorted(
            pending,
            key=lambda item: (item.completes_at_month, item.project.project_id),
        )
    )
    current_stockpile = stockpile
    earned_income = state.earned_income
    active_upkeep = state.active_upkeep
    first_failure: dict[str, int] = {}
    cumulative_shortfall: dict[str, Decimal] = {}
    for offset in range(1, horizon_months + 1):
        resources = set(current_stockpile.keys())
        resources.update(earned_income.keys())
        resources.update(active_upkeep.keys())
        next_stockpile: dict[str, Decimal] = {}
        for resource in sorted(resources):
            raw = (
                current_stockpile.get(resource)
                + earned_income.get(resource)
                - active_upkeep.get(resource)
            )
            if raw < ZERO:
                first_failure.setdefault(resource, offset)
                cumulative_shortfall[resource] = (
                    cumulative_shortfall.get(resource, ZERO) - raw
                )
            value = max(raw, ZERO)
            if state.capacity.contains(resource):
                value = min(value, state.capacity.get(resource))
            next_stockpile[resource] = value
        current_stockpile = QuantityVector(tuple(next_stockpile.items()))

        completion_month = state.month + offset
        completing = tuple(
            item
            for item in ordered_pending
            if item.completes_at_month == completion_month
        )
        earned_income = earned_income.plus(
            _sum_vectors(item.project.completion_income for item in completing)
        )
        active_upkeep = active_upkeep.plus(
            _sum_vectors(item.project.completion_upkeep for item in completing)
        )
    return {
        resource: _RunwayFailure(
            first_month=first_failure[resource],
            cumulative_shortfall=shortfall,
        )
        for resource, shortfall in sorted(cumulative_shortfall.items())
    }


def _incremental_runway_reasons(
    state: EconomicState,
    projects: tuple[Project, ...],
    *,
    operating_horizon_months: int,
) -> tuple[FeasibilityReason, ...]:
    if not projects:
        return ()
    project_ids = tuple(project.project_id for project in projects)
    projection_months = max(
        project.duration_months for project in projects
    ) + operating_horizon_months
    baseline_failures = _runway_failures(
        state,
        state.pending,
        state.stockpile,
        horizon_months=projection_months,
    )
    added_pending = tuple(
        PendingProject(
            project=project,
            completes_at_month=state.month + project.duration_months,
        )
        for project in projects
    )
    projected_failures = _runway_failures(
        state,
        state.pending + added_pending,
        state.stockpile.minus(
            _sum_vectors(project.one_time_cost for project in projects)
        ),
        horizon_months=projection_months,
    )
    reasons = []
    for resource, failure in sorted(projected_failures.items()):
        baseline = baseline_failures.get(resource)
        if baseline is not None:
            no_earlier_failure = failure.first_month >= baseline.first_month
            no_deeper_shortfall = (
                failure.cumulative_shortfall <= baseline.cumulative_shortfall
            )
            if no_earlier_failure and no_deeper_shortfall:
                continue
        reasons.append(
            FeasibilityReason(
                FeasibilityCode.RUNWAY,
                resource,
                failure.cumulative_shortfall,
                baseline.cumulative_shortfall if baseline is not None else ZERO,
                project_ids,
            )
        )
    return tuple(reasons)


@_model_decimal_context
def evaluate_bundle_feasibility(
    state: EconomicState,
    projects: Iterable[Project],
    *,
    horizon_months: int = 12,
) -> BundleFeasibility:
    """Check start constraints plus post-completion operating support.

    ``horizon_months`` is the required operating window after the latest
    candidate completes, not a fixed window from the start date.
    """

    if horizon_months < 1:
        raise ValueError("horizon_months must be positive")
    ordered = tuple(sorted(projects, key=lambda project: project.project_id))
    project_ids = tuple(project.project_id for project in ordered)
    if len(set(project_ids)) != len(project_ids):
        raise ValueError("a bundle cannot contain duplicate project IDs")
    reasons: list[FeasibilityReason] = []

    for project in ordered:
        for gate in sorted(project.required_gates - state.gates):
            reasons.append(
                FeasibilityReason(
                    FeasibilityCode.MISSING_GATE,
                    gate,
                    ONE,
                    ZERO,
                    (project.project_id,),
                )
            )
        for gate in sorted(project.forbidden_gates & state.gates):
            reasons.append(
                FeasibilityReason(
                    FeasibilityCode.FORBIDDEN_GATE,
                    gate,
                    ZERO,
                    ONE,
                    (project.project_id,),
                )
            )

    checks = (
        (
            FeasibilityCode.RESOURCE,
            _sum_vectors(project.one_time_cost for project in ordered),
            state.stockpile,
        ),
        (
            FeasibilityCode.BUDGET,
            _sum_vectors(project.budget_cost for project in ordered),
            state.budgets,
        ),
        (
            FeasibilityCode.SLOT,
            state.slot_used.plus(
                _sum_vectors(project.slot_cost for project in ordered)
            ),
            state.slot_capacity,
        ),
        (
            FeasibilityCode.JOB,
            state.job_used.plus(
                _sum_vectors(item.project.job_cost for item in state.pending),
                _sum_vectors(project.job_cost for project in ordered),
            ),
            state.job_capacity,
        ),
    )
    for code, required, available in checks:
        for key, amount in required.values:
            available_amount = available.get(key)
            if amount > available_amount:
                reasons.append(
                    FeasibilityReason(
                        code, key, amount, available_amount, project_ids
                    )
                )

    queue_demand: dict[str, Decimal] = dict(state.queue_used.values)
    for project in ordered:
        if project.queue is not None:
            queue_demand[project.queue] = (
                queue_demand.get(project.queue, ZERO) + project.queue_slots
            )
    for queue, required in sorted(queue_demand.items()):
        available = state.queue_capacity.get(queue)
        if required > available:
            reasons.append(
                FeasibilityReason(
                    FeasibilityCode.QUEUE,
                    queue,
                    required,
                    available,
                    project_ids,
                )
            )

    influence_required = sum(
        (project.influence_cost for project in ordered), start=ZERO
    )
    if influence_required > state.influence:
        reasons.append(
            FeasibilityReason(
                FeasibilityCode.INFLUENCE,
                "influence",
                influence_required,
                state.influence,
                project_ids,
            )
        )

    if not any(reason.code is FeasibilityCode.RESOURCE for reason in reasons):
        reasons.extend(
            _incremental_runway_reasons(
                state,
                ordered,
                operating_horizon_months=horizon_months,
            )
        )

    ordered_reasons = tuple(
        sorted(reasons, key=lambda reason: (reason.code.value, reason.key, reason.project_ids))
    )
    return BundleFeasibility(ordered, not ordered_reasons, ordered_reasons)


class ModelLimitError(ValueError):
    """Raised when exact search is asked to exceed its fixture-sized bound."""


@dataclass(frozen=True)
class BundleSearchResult:
    feasible: tuple[BundleFeasibility, ...]
    rejected: tuple[BundleFeasibility, ...]


@_model_decimal_context
def find_feasible_bundles(
    state: EconomicState,
    projects: Iterable[Project],
    *,
    max_candidates: int = 12,
    max_bundle_size: int | None = None,
    horizon_months: int = 12,
) -> BundleSearchResult:
    """Enumerate all bounded candidate bundles exactly and deterministically."""

    candidates = tuple(sorted(projects, key=lambda project: project.project_id))
    if max_candidates < 1:
        raise ValueError("max_candidates must be positive")
    if len(candidates) > max_candidates:
        raise ModelLimitError(
            f"exact bundle search is capped at {max_candidates} candidates; "
            f"received {len(candidates)}"
        )
    if max_bundle_size is not None and max_bundle_size < 1:
        raise ValueError("max_bundle_size must be positive")
    if horizon_months < 1:
        raise ValueError("horizon_months must be positive")
    bundle_limit = (
        len(candidates)
        if max_bundle_size is None
        else min(max_bundle_size, len(candidates))
    )

    results = [evaluate_bundle_feasibility(state, (), horizon_months=horizon_months)]
    for size in range(1, bundle_limit + 1):
        results.extend(
            evaluate_bundle_feasibility(
                state, bundle, horizon_months=horizon_months
            )
            for bundle in combinations(candidates, size)
        )
    feasible = tuple(result for result in results if result.feasible)
    rejected = tuple(result for result in results if not result.feasible)
    return BundleSearchResult(feasible=feasible, rejected=rejected)


@dataclass(frozen=True)
class ActivePriority:
    project: Project
    priority: Decimal
    activation: ActivationResult | None


@dataclass(frozen=True)
class PriorityDecision:
    project: Project
    truth: Truth
    priority: Decimal
    activation: ActivationResult | None

    @property
    def active(self) -> bool:
        return self.truth is Truth.TRUE


@dataclass(frozen=True)
class ActivePrioritySet:
    decisions: tuple[PriorityDecision, ...]

    @property
    def active(self) -> tuple[ActivePriority, ...]:
        return tuple(
            ActivePriority(decision.project, decision.priority, decision.activation)
            for decision in self.decisions
            if decision.active
        )


@_model_decimal_context
def build_active_priority_set(
    state: EconomicState,
    projects: Iterable[Project],
    variant: PolicyVariant,
    *,
    facts: FactSet = FactSet(),
) -> ActivePrioritySet:
    """Apply trigger and policy activation without evaluating affordability."""

    ordered = tuple(sorted(projects, key=lambda project: project.project_id))
    if len({project.project_id for project in ordered}) != len(ordered):
        raise ValueError("candidate project IDs must be unique")
    decisions: list[PriorityDecision] = []
    for project in ordered:
        if not project.repeatable and project.project_id in state.started_projects:
            decisions.append(
                PriorityDecision(project, Truth.FALSE, project.base_priority, None)
            )
            continue
        if project.strategic_resource is None:
            truth = evaluate_trigger(project.trigger, facts)
            decisions.append(
                PriorityDecision(project, truth, project.base_priority, None)
            )
            continue
        activation = evaluate_policy_activation(
            state,
            variant,
            project.strategic_resource,
            trigger=project.trigger,
            facts=facts,
        )
        if (
            activation.truth is Truth.TRUE
            and activation.committed_pressure_months is None
        ):
            activation = replace(
                activation,
                requested_income=activation.remaining_pressure,
            )
        if (
            activation.truth is Truth.TRUE
            and activation.committed_pressure_months is not None
            and project.duration_months
            >= activation.committed_pressure_months
        ):
            activation = replace(
                activation,
                truth=Truth.FALSE,
                requested_income=ZERO,
                reasons=activation.reasons
                + (
                    ActivationReason.CANDIDATE_NOT_FASTER_THAN_COMMITTED,
                ),
            )
        decisions.append(
            PriorityDecision(
                project,
                activation.truth,
                project.base_priority + variant.priority_bonus,
                activation,
            )
        )
    return ActivePrioritySet(tuple(decisions))


@dataclass(frozen=True)
class SelectedBundle:
    """Selected projects and their bounded, resource-level selection score."""

    projects: tuple[Project, ...]
    total_priority: Decimal

    @property
    def project_ids(self) -> tuple[str, ...]:
        return tuple(project.project_id for project in self.projects)


@_model_decimal_context
def select_bundle(
    search: BundleSearchResult, priorities: ActivePrioritySet
) -> SelectedBundle:
    active = priorities.active
    effective_priority_by_id: dict[str, Decimal] = {}
    for item in active:
        project_id = item.project.project_id
        if project_id in effective_priority_by_id:
            raise ValueError("active priority project IDs must be unique")
        effective_priority_by_id[project_id] = item.priority

    searched_project_ids = {
        project.project_id
        for result in search.feasible + search.rejected
        for project in result.projects
    }
    missing_priority_ids = sorted(
        searched_project_ids - effective_priority_by_id.keys()
    )
    if missing_priority_ids:
        raise ValueError(
            "bundle search projects missing from active priorities: "
            + ", ".join(missing_priority_ids)
        )

    requested_by_resource: dict[str, Decimal] = {}
    bonus_by_resource: dict[str, Decimal] = {}
    for item in active:
        resource = item.project.strategic_resource
        if resource is None or item.activation is None:
            continue
        requested_by_resource[resource] = max(
            requested_by_resource.get(resource, ZERO),
            item.activation.requested_income,
        )
        bonus_by_resource[resource] = max(
            bonus_by_resource.get(resource, ZERO),
            item.priority - item.project.base_priority,
        )

    def net_output(project: Project, resource: str) -> Decimal:
        return project.completion_income.get(
            resource
        ) - project.completion_upkeep.get(resource)

    def has_redundant_recovery(projects: tuple[Project, ...]) -> bool:
        for resource, requested in sorted(requested_by_resource.items()):
            producers = tuple(
                project
                for project in projects
                if project.strategic_resource == resource
            )
            if len(producers) < 2 or requested <= ZERO:
                continue
            total = sum(
                (net_output(project, resource) for project in producers),
                start=ZERO,
            )
            if any(
                total - net_output(project, resource) >= requested
                for project in producers
            ):
                return True
        return False

    def recovery_fit(projects: tuple[Project, ...]) -> tuple[Decimal, Decimal]:
        shortfall = ZERO
        overshoot = ZERO
        for resource, requested in sorted(requested_by_resource.items()):
            output = sum(
                (
                    net_output(project, resource)
                    for project in projects
                    if project.strategic_resource == resource
                ),
                start=ZERO,
            )
            if output >= requested:
                overshoot += output - requested
            else:
                shortfall += requested - output
        return shortfall, overshoot

    ranked: list[
        tuple[
            Decimal,
            Decimal,
            Decimal,
            Decimal,
            int,
            tuple[str, ...],
            BundleFeasibility,
        ]
    ] = []
    for result in search.feasible:
        if has_redundant_recovery(result.projects):
            continue
        strategic_resources = {
            project.strategic_resource
            for project in result.projects
            if project.strategic_resource is not None
        }
        score = sum(
            (
                effective_priority_by_id[project.project_id]
                for project in result.projects
                if project.strategic_resource is None
            ),
            start=ZERO,
        ) + sum(
            (bonus_by_resource[resource] for resource in strategic_resources),
            start=ZERO,
        )
        producer_preference = sum(
            (
                project.base_priority
                for project in result.projects
                if project.strategic_resource is not None
            ),
            start=ZERO,
        )
        shortfall, overshoot = recovery_fit(result.projects)
        ranked.append(
            (
                -score,
                shortfall,
                overshoot,
                -producer_preference,
                len(result.projects),
                result.project_ids,
                result,
            )
        )
    if not ranked:
        raise ValueError("bundle search must include the feasible empty bundle")
    _, _, _, _, _, _, winner = min(
        ranked,
        key=lambda item: (
            item[0],
            item[1],
            item[2],
            item[3],
            item[4],
            item[5],
        ),
    )
    selected_resources = {
        project.strategic_resource
        for project in winner.projects
        if project.strategic_resource is not None
    }
    total = sum(
        (
            effective_priority_by_id[project.project_id]
            for project in winner.projects
            if project.strategic_resource is None
        ),
        start=ZERO,
    ) + sum(
        (bonus_by_resource[resource] for resource in selected_resources),
        start=ZERO,
    )
    return SelectedBundle(winner.projects, total)


@_model_decimal_context
def schedule_bundle(
    state: EconomicState,
    projects: Iterable[Project],
    *,
    horizon_months: int = 12,
) -> EconomicState:
    ordered = tuple(sorted(projects, key=lambda project: project.project_id))
    feasibility = evaluate_bundle_feasibility(
        state, ordered, horizon_months=horizon_months
    )
    if not feasibility.feasible:
        details = ", ".join(f"{reason.code.value}:{reason.key}" for reason in feasibility.reasons)
        raise ValueError(f"cannot schedule infeasible bundle: {details}")

    one_time_cost = _sum_vectors(project.one_time_cost for project in ordered)
    budget_cost = _sum_vectors(project.budget_cost for project in ordered)
    slot_cost = _sum_vectors(project.slot_cost for project in ordered)
    queue_used = state.queue_used
    pending = list(state.pending)
    for project in ordered:
        if project.queue is not None:
            queue_used = queue_used.with_value(
                project.queue,
                queue_used.get(project.queue) + project.queue_slots,
            )
        pending.append(
            PendingProject(
                project=project,
                completes_at_month=state.month + project.duration_months,
            )
        )
    pending.sort(key=lambda item: (item.completes_at_month, item.project.project_id))
    return replace(
        state,
        stockpile=state.stockpile.minus(one_time_cost),
        budgets=state.budgets.minus(budget_cost),
        queue_used=queue_used,
        slot_used=state.slot_used.plus(slot_cost),
        influence=state.influence
        - sum((project.influence_cost for project in ordered), start=ZERO),
        pending=tuple(pending),
        started_projects=state.started_projects
        | frozenset(project.project_id for project in ordered),
    )


@dataclass(frozen=True)
class GateRule:
    rule_id: str
    requires_all: frozenset[str] = frozenset()
    requires_any: frozenset[str] = frozenset()
    forbids: frozenset[str] = frozenset()
    add: frozenset[str] = frozenset()
    remove: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.rule_id:
            raise ValueError("gate rule IDs must be non-empty")
        if self.add & self.remove:
            raise ValueError("a gate rule cannot add and remove the same gate")


@dataclass(frozen=True)
class GateCascadeResult:
    gates: frozenset[str]
    fired_rules: tuple[str, ...]


def evaluate_gate_transitions(
    gates: frozenset[str], rules: Iterable[GateRule]
) -> GateCascadeResult:
    """Apply synchronous one-shot rule waves and reject ambiguous conflicts."""

    ordered = tuple(sorted(rules, key=lambda rule: rule.rule_id))
    if len({rule.rule_id for rule in ordered}) != len(ordered):
        raise ValueError("gate rule IDs must be unique")
    current = set(gates)
    fired: list[str] = []
    fired_set: set[str] = set()
    while True:
        eligible = tuple(
            rule
            for rule in ordered
            if rule.rule_id not in fired_set
            and rule.requires_all <= current
            and (not rule.requires_any or bool(rule.requires_any & current))
            and not rule.forbids & current
        )
        if not eligible:
            break
        additions = frozenset(gate for rule in eligible for gate in rule.add)
        removals = frozenset(gate for rule in eligible for gate in rule.remove)
        conflicts = additions & removals
        if conflicts:
            conflict_list = ", ".join(sorted(conflicts))
            rule_list = ", ".join(rule.rule_id for rule in eligible)
            raise ValueError(
                "conflicting gate transitions for "
                f"{conflict_list} in synchronous rule wave: {rule_list}"
            )
        current.difference_update(removals)
        current.update(additions)
        fired.extend(rule.rule_id for rule in eligible)
        fired_set.update(rule.rule_id for rule in eligible)
    return GateCascadeResult(frozenset(current), tuple(fired))


def _apply_monthly_flow(state: EconomicState) -> QuantityVector:
    resources = set(state.stockpile.keys())
    resources.update(state.earned_income.keys())
    resources.update(state.market_income.keys())
    resources.update(state.active_upkeep.keys())
    result: dict[str, Decimal] = {}
    for resource in sorted(resources):
        value = (
            state.stockpile.get(resource)
            + state.earned_income.get(resource)
            + state.market_income.get(resource)
            - state.active_upkeep.get(resource)
        )
        value = max(value, ZERO)
        if state.capacity.contains(resource):
            value = min(value, state.capacity.get(resource))
        result[resource] = value
    return QuantityVector(tuple(result.items()))


def _updated_deficit_status(
    previous: FactSet,
    stockpile: QuantityVector,
    earned_income: QuantityVector,
    upkeep: QuantityVector,
) -> FactSet:
    result = dict(previous.values)
    resources = set(result)
    resources.update(earned_income.keys())
    resources.update(upkeep.keys())
    for resource in sorted(resources):
        if not earned_income.contains(resource) or not upkeep.contains(resource):
            continue
        earned = earned_income.get(resource)
        used = upkeep.get(resource)
        if earned >= used:
            result[resource] = Truth.FALSE
            continue
        prior = result.get(resource, Truth.INDETERMINATE)
        if prior is Truth.TRUE or stockpile.get(resource) <= ZERO:
            result[resource] = Truth.TRUE
        elif prior is Truth.FALSE:
            result[resource] = Truth.FALSE
        else:
            result[resource] = Truth.INDETERMINATE
    return FactSet(tuple(result.items()))


@_model_decimal_context
def advance_month(
    state: EconomicState, *, gate_rules: Iterable[GateRule] = ()
) -> EconomicState:
    """Advance one month; projects complete after the current month's flow.

    Completion income and upkeep therefore become active at the returned month
    boundary and affect the following call, never the month in which the
    project completes.
    """

    next_month = state.month + 1
    stockpile = _apply_monthly_flow(state)
    completing = tuple(
        item for item in state.pending if item.completes_at_month <= next_month
    )
    remaining = tuple(
        item for item in state.pending if item.completes_at_month > next_month
    )
    earned_income = state.earned_income.plus(
        _sum_vectors(item.project.completion_income for item in completing)
    )
    upkeep = state.active_upkeep.plus(
        _sum_vectors(item.project.completion_upkeep for item in completing)
    )
    job_used = state.job_used.plus(
        _sum_vectors(item.project.job_cost for item in completing)
    )
    queue_used = state.queue_used
    add_gates: set[str] = set()
    remove_gates: set[str] = set()
    for item in completing:
        project = item.project
        if project.queue is not None:
            queue_used = queue_used.with_value(
                project.queue,
                queue_used.get(project.queue) - project.queue_slots,
            )
        add_gates.update(project.add_gates)
        remove_gates.update(project.remove_gates)
    if add_gates & remove_gates:
        conflicts = ", ".join(sorted(add_gates & remove_gates))
        raise ValueError(f"simultaneous project completions conflict on gates: {conflicts}")
    gates = set(state.gates)
    gates.difference_update(remove_gates)
    gates.update(add_gates)
    cascade = evaluate_gate_transitions(frozenset(gates), gate_rules)
    deficits = _updated_deficit_status(
        state.deficit_status, stockpile, earned_income, upkeep
    )
    return replace(
        state,
        month=next_month,
        stockpile=stockpile,
        earned_income=earned_income,
        active_upkeep=upkeep,
        job_used=job_used,
        queue_used=queue_used,
        deficit_status=deficits,
        gates=cascade.gates,
        pending=remaining,
        completed_projects=state.completed_projects
        | frozenset(item.project.project_id for item in completing),
    )


_SHARED_BOTTLENECK_CODES = frozenset(
    {
        FeasibilityCode.RESOURCE,
        FeasibilityCode.BUDGET,
        FeasibilityCode.QUEUE,
        FeasibilityCode.SLOT,
        FeasibilityCode.JOB,
        FeasibilityCode.INFLUENCE,
        FeasibilityCode.RUNWAY,
    }
)


@dataclass(frozen=True)
class BlockedOpportunity:
    project_id: str
    lane: Lane
    shared_reasons: tuple[FeasibilityReason, ...]


@dataclass(frozen=True)
class MonthSnapshot:
    month: int
    state_before: EconomicState
    priorities: ActivePrioritySet
    selected: SelectedBundle
    blocked_opportunities: tuple[BlockedOpportunity, ...]
    state_after: EconomicState


@dataclass(frozen=True)
class ScenarioFingerprint:
    projects: tuple[Project, ...]
    facts: FactSet
    gate_rules: tuple[GateRule, ...]
    months: int
    operating_horizon_months: int
    max_candidates: int
    max_bundle_size: int | None


@dataclass(frozen=True)
class PolicyRun:
    variant: PolicyVariant
    initial_state: EconomicState
    scenario: ScenarioFingerprint
    snapshots: tuple[MonthSnapshot, ...]
    final_state: EconomicState


def _blocked_opportunities(
    state: EconomicState,
    priorities: ActivePrioritySet,
    selected: SelectedBundle,
    *,
    horizon_months: int,
) -> tuple[BlockedOpportunity, ...]:
    selected_ids = set(selected.project_ids)
    selected_lanes = {project.lane for project in selected.projects}
    blocked: list[BlockedOpportunity] = []
    for active in priorities.active:
        project = active.project
        if project.project_id in selected_ids or project.lane in selected_lanes:
            continue
        singleton = evaluate_bundle_feasibility(
            state, (project,), horizon_months=horizon_months
        )
        if not singleton.feasible:
            shared = tuple(
                reason
                for reason in singleton.reasons
                if reason.code in _SHARED_BOTTLENECK_CODES
            )
            if shared:
                blocked.append(
                    BlockedOpportunity(project.project_id, project.lane, shared)
                )
            continue
        combined = evaluate_bundle_feasibility(
            state,
            selected.projects + (project,),
            horizon_months=horizon_months,
        )
        shared = tuple(
            reason
            for reason in combined.reasons
            if reason.code in _SHARED_BOTTLENECK_CODES
        )
        if shared:
            blocked.append(BlockedOpportunity(project.project_id, project.lane, shared))
    return tuple(sorted(blocked, key=lambda item: (item.lane.value, item.project_id)))


@_model_decimal_context
def run_policy_variant(
    initial_state: EconomicState,
    projects: Iterable[Project],
    variant: PolicyVariant,
    *,
    months: int,
    facts: FactSet = FactSet(),
    gate_rules: Iterable[GateRule] = (),
    operating_horizon_months: int = 12,
    max_candidates: int = 12,
    max_bundle_size: int | None = None,
) -> PolicyRun:
    """Run a bounded deterministic policy counterfactual from one checkpoint."""

    if months < 0:
        raise ValueError("months must be non-negative")
    if operating_horizon_months < 1:
        raise ValueError("operating_horizon_months must be positive")
    candidates = tuple(sorted(projects, key=lambda project: project.project_id))
    rules = tuple(sorted(gate_rules, key=lambda rule: rule.rule_id))
    scenario = ScenarioFingerprint(
        projects=candidates,
        facts=facts,
        gate_rules=rules,
        months=months,
        operating_horizon_months=operating_horizon_months,
        max_candidates=max_candidates,
        max_bundle_size=max_bundle_size,
    )
    current = initial_state
    snapshots: list[MonthSnapshot] = []
    for _ in range(months):
        priorities = build_active_priority_set(
            current, candidates, variant, facts=facts
        )
        search = find_feasible_bundles(
            current,
            (active.project for active in priorities.active),
            max_candidates=max_candidates,
            max_bundle_size=max_bundle_size,
            horizon_months=operating_horizon_months,
        )
        selected = select_bundle(search, priorities)
        blocked = _blocked_opportunities(
            current,
            priorities,
            selected,
            horizon_months=operating_horizon_months,
        )
        scheduled = schedule_bundle(
            current,
            selected.projects,
            horizon_months=operating_horizon_months,
        )
        after = advance_month(scheduled, gate_rules=rules)
        snapshots.append(
            MonthSnapshot(
                month=current.month,
                state_before=current,
                priorities=priorities,
                selected=selected,
                blocked_opportunities=blocked,
                state_after=after,
            )
        )
        current = after
    return PolicyRun(
        variant=variant,
        initial_state=initial_state,
        scenario=scenario,
        snapshots=tuple(snapshots),
        final_state=current,
    )


@dataclass(frozen=True)
class LaneStarvation:
    lane: Lane
    months: tuple[int, ...]
    shared_bottlenecks: tuple[tuple[FeasibilityCode, str], ...]
    counterfactual_selected_months: tuple[int, ...]


def _consecutive_runs(months: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    ordered = sorted(set(months))
    if not ordered:
        return ()
    runs: list[list[int]] = [[ordered[0]]]
    for month in ordered[1:]:
        if month == runs[-1][-1] + 1:
            runs[-1].append(month)
        else:
            runs.append([month])
    return tuple(tuple(run) for run in runs)


def detect_lane_starvation(
    policy_run: PolicyRun,
    policy_off_counterfactual: PolicyRun,
    *,
    minimum_consecutive_months: int = 3,
) -> tuple[LaneStarvation, ...]:
    """Attribute starvation only with shared pressure and policy-off progress."""

    if minimum_consecutive_months < 1:
        raise ValueError("minimum_consecutive_months must be positive")
    if policy_run.initial_state != policy_off_counterfactual.initial_state:
        raise ValueError("starvation comparisons require identical initial states")
    if policy_run.scenario != policy_off_counterfactual.scenario:
        raise ValueError("starvation comparisons require identical scenarios")
    if policy_off_counterfactual.variant.mode is not PolicyMode.PARENT_ONLY:
        raise ValueError("starvation comparisons require a policy-off counterfactual")
    counterfactual_by_month = {
        snapshot.month: snapshot for snapshot in policy_off_counterfactual.snapshots
    }
    results: list[LaneStarvation] = []
    for lane in Lane:
        blocked_by_month: dict[int, tuple[BlockedOpportunity, ...]] = {}
        for snapshot in policy_run.snapshots:
            blocked = tuple(
                item for item in snapshot.blocked_opportunities if item.lane is lane
            )
            if blocked:
                blocked_by_month[snapshot.month] = blocked
        for streak in _consecutive_runs(blocked_by_month):
            if len(streak) < minimum_consecutive_months:
                continue
            counterfactual_months = tuple(
                month
                for month in streak
                if month in counterfactual_by_month
                and {
                    project.project_id
                    for project in counterfactual_by_month[
                        month
                    ].selected.projects
                }
                & {
                    blocked.project_id
                    for blocked in blocked_by_month[month]
                }
            )
            if not counterfactual_months:
                continue
            bottlenecks = {
                (reason.code, reason.key)
                for month in streak
                for blocked in blocked_by_month[month]
                for reason in blocked.shared_reasons
            }
            if not bottlenecks:
                continue
            results.append(
                LaneStarvation(
                    lane=lane,
                    months=streak,
                    shared_bottlenecks=tuple(
                        sorted(bottlenecks, key=lambda item: (item[0].value, item[1]))
                    ),
                    counterfactual_selected_months=counterfactual_months,
                )
            )
    return tuple(sorted(results, key=lambda item: (item.lane.value, item.months)))


@dataclass(frozen=True)
class VariantComparison:
    variant: PolicyVariant
    run: PolicyRun
    starvation: tuple[LaneStarvation, ...]


@dataclass(frozen=True)
class PolicyComparison:
    baseline: PolicyRun
    variants: tuple[VariantComparison, ...]


@_model_decimal_context
def compare_policy_variants(
    initial_state: EconomicState,
    projects: Iterable[Project],
    *,
    baseline: PolicyVariant,
    variants: Iterable[PolicyVariant],
    months: int,
    facts: FactSet = FactSet(),
    gate_rules: Iterable[GateRule] = (),
    starvation_months: int = 3,
    operating_horizon_months: int = 12,
    max_candidates: int = 12,
    max_bundle_size: int | None = None,
) -> PolicyComparison:
    """Run policy variants from identical immutable starts and compare to baseline."""

    candidates = tuple(projects)
    rules = tuple(gate_rules)
    alternatives = tuple(variants)
    if baseline.mode is not PolicyMode.PARENT_ONLY:
        raise ValueError("the starvation baseline must be policy-off")
    names = (baseline.name,) + tuple(variant.name for variant in alternatives)
    if len(set(names)) != len(names):
        raise ValueError("policy variant names must be unique")
    baseline_run = run_policy_variant(
        initial_state,
        candidates,
        baseline,
        months=months,
        facts=facts,
        gate_rules=rules,
        operating_horizon_months=operating_horizon_months,
        max_candidates=max_candidates,
        max_bundle_size=max_bundle_size,
    )
    comparisons: list[VariantComparison] = []
    for variant in alternatives:
        run = run_policy_variant(
            initial_state,
            candidates,
            variant,
            months=months,
            facts=facts,
            gate_rules=rules,
            operating_horizon_months=operating_horizon_months,
            max_candidates=max_candidates,
            max_bundle_size=max_bundle_size,
        )
        comparisons.append(
            VariantComparison(
                variant=variant,
                run=run,
                starvation=detect_lane_starvation(
                    run,
                    baseline_run,
                    minimum_consecutive_months=starvation_months,
                ),
            )
        )
    return PolicyComparison(baseline_run, tuple(comparisons))


__all__ = [
    "FAILED_C9",
    "DEFICIT_ONLY_PLUS_ONE",
    "DEFICIT_ONLY_PLUS_TWO",
    "PARENT_ONLY",
    "PREZERO_RUNWAY_PLUS_ONE",
    "ActivationReason",
    "ActivationResult",
    "AllOf",
    "AnyOf",
    "Atom",
    "EconomicState",
    "FactSet",
    "FeasibilityCode",
    "FeasibilityReason",
    "GateRule",
    "Lane",
    "ModelLimitError",
    "Not",
    "PendingProject",
    "PolicyComparison",
    "PolicyMode",
    "PolicyVariant",
    "Project",
    "QuantityVector",
    "ScenarioFingerprint",
    "Truth",
    "advance_month",
    "build_active_priority_set",
    "compare_policy_variants",
    "detect_lane_starvation",
    "evaluate_bundle_feasibility",
    "evaluate_gate_transitions",
    "evaluate_policy_activation",
    "evaluate_trigger",
    "find_feasible_bundles",
    "run_policy_variant",
    "schedule_bundle",
    "select_bundle",
]
