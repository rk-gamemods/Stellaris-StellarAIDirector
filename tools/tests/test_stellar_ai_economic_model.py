from __future__ import annotations

import unittest
from decimal import localcontext

from tools.stellar_ai_economic_model import (
    FAILED_C9,
    DEFICIT_ONLY_PLUS_ONE,
    DEFICIT_ONLY_PLUS_TWO,
    PARENT_ONLY,
    PREZERO_RUNWAY_PLUS_ONE,
    ActivationReason,
    AllOf,
    Atom,
    EconomicState,
    FactSet,
    FeasibilityCode,
    GateRule,
    Lane,
    ModelLimitError,
    PendingProject,
    Project,
    QuantityVector,
    Truth,
    advance_month,
    build_active_priority_set,
    compare_policy_variants,
    detect_lane_starvation,
    evaluate_bundle_feasibility,
    evaluate_gate_transitions,
    evaluate_policy_activation,
    evaluate_trigger,
    find_feasible_bundles,
    run_policy_variant,
    schedule_bundle,
)


def quantities(**values: float) -> QuantityVector:
    return QuantityVector.from_mapping(values)


def fact_set(**values: Truth) -> FactSet:
    return FactSet.from_mapping(values)


def state(
    *,
    stockpile: QuantityVector | None = None,
    capacity: QuantityVector | None = None,
    earned_income: QuantityVector | None = None,
    market_income: QuantityVector | None = None,
    active_upkeep: QuantityVector | None = None,
    budgets: QuantityVector | None = None,
    queue_capacity: QuantityVector | None = None,
    queue_used: QuantityVector | None = None,
    slot_capacity: QuantityVector | None = None,
    slot_used: QuantityVector | None = None,
    job_capacity: QuantityVector | None = None,
    job_used: QuantityVector | None = None,
    influence: float = 0,
    deficit_status: FactSet | None = None,
    unlocked_resources: frozenset[str] = frozenset(),
    pending: tuple[PendingProject, ...] = (),
) -> EconomicState:
    return EconomicState(
        stockpile=stockpile or quantities(),
        capacity=capacity or quantities(),
        earned_income=earned_income or quantities(),
        market_income=market_income or quantities(),
        active_upkeep=active_upkeep or quantities(),
        budgets=budgets or quantities(),
        queue_capacity=queue_capacity or quantities(),
        queue_used=queue_used or quantities(),
        slot_capacity=slot_capacity or quantities(),
        slot_used=slot_used or quantities(),
        job_capacity=job_capacity or quantities(),
        job_used=job_used or quantities(),
        influence=influence,
        deficit_status=deficit_status or FactSet(),
        unlocked_resources=unlocked_resources,
        pending=pending,
    )


class EconomicModelContractTests(unittest.TestCase):
    def test_lane_vocabulary_is_the_twelve_explicit_competing_lanes(self) -> None:
        self.assertEqual(
            {lane.value for lane in Lane},
            {
                "colonization",
                "expansion",
                "planetary_development",
                "research",
                "new_hulls",
                "upgrades",
                "claims",
                "defense",
                "war_preparation",
                "strategic_producer",
                "market_bridge",
                "megastructure",
            },
        )

    def test_small_capacity_and_tiny_balanced_use_are_safe(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0.05),
            capacity=quantities(exotic_gases=0.10),
            earned_income=quantities(exotic_gases=0.01),
            active_upkeep=quantities(exotic_gases=0.01),
            deficit_status=fact_set(exotic_gases=Truth.FALSE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )

        deficit_only = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )
        prezero = evaluate_policy_activation(
            checkpoint, PREZERO_RUNWAY_PLUS_ONE, "exotic_gases"
        )

        self.assertIs(deficit_only.truth, Truth.FALSE)
        self.assertIs(prezero.truth, Truth.FALSE)
        self.assertEqual(deficit_only.requested_income, 0)
        self.assertEqual(prezero.requested_income, 0)

    def test_prezero_policy_uses_measured_runway_not_absolute_storage(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=2),
            capacity=quantities(exotic_gases=1000),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.FALSE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )

        activation = evaluate_policy_activation(
            checkpoint, PREZERO_RUNWAY_PLUS_ONE, "exotic_gases"
        )
        deficit_only = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )

        self.assertIs(activation.truth, Truth.TRUE)
        self.assertEqual(activation.runway_months, 2)
        self.assertEqual(activation.requested_income, 1)
        self.assertIs(deficit_only.truth, Truth.FALSE)

    def test_missing_deficit_observation_remains_indeterminate(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=2),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            unlocked_resources=frozenset({"exotic_gases"}),
        )

        activation = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )

        self.assertIs(activation.truth, Truth.INDETERMINATE)
        self.assertEqual(activation.requested_income, 0)

    def test_unknown_trigger_atom_is_indeterminate_and_fails_closed(self) -> None:
        trigger = AllOf((Atom("hidden_engine_gate"),))
        self.assertIs(evaluate_trigger(trigger, FactSet()), Truth.INDETERMINATE)

        project = Project(
            project_id="unknown-gated-research",
            lane=Lane.RESEARCH,
            base_priority=10,
            trigger=trigger,
        )
        priorities = build_active_priority_set(
            state(), (project,), PARENT_ONLY, facts=FactSet()
        )

        self.assertEqual(priorities.active, ())
        self.assertIs(priorities.decisions[0].truth, Truth.INDETERMINATE)

    def test_deficit_only_pressure_is_bounded_and_resource_specific(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0, rare_crystals=100),
            capacity=quantities(exotic_gases=100, rare_crystals=100),
            earned_income=quantities(exotic_gases=0, rare_crystals=2),
            active_upkeep=quantities(exotic_gases=1, rare_crystals=1),
            deficit_status=fact_set(
                exotic_gases=Truth.TRUE, rare_crystals=Truth.FALSE
            ),
            unlocked_resources=frozenset({"exotic_gases", "rare_crystals"}),
        )
        projects = (
            Project(
                project_id="gas-producer",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=20,
                strategic_resource="exotic_gases",
                completion_income=quantities(exotic_gases=1),
            ),
            Project(
                project_id="crystal-producer",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=20,
                strategic_resource="rare_crystals",
                completion_income=quantities(rare_crystals=1),
            ),
        )

        priorities = build_active_priority_set(
            checkpoint, projects, DEFICIT_ONLY_PLUS_ONE
        )
        self.assertEqual(
            tuple(priority.project.project_id for priority in priorities.active),
            ("gas-producer",),
        )
        self.assertEqual(priorities.active[0].activation.requested_income, 1)

        plus_two = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_TWO, "exotic_gases"
        )
        self.assertIs(plus_two.truth, Truth.TRUE)
        self.assertEqual(plus_two.requested_income, 1)

    def test_committed_producer_suppresses_duplicate_recovery_pressure(self) -> None:
        producer = Project(
            project_id="already-building-gas",
            lane=Lane.STRATEGIC_PRODUCER,
            base_priority=10,
            duration_months=2,
            completion_income=quantities(exotic_gases=1),
        )
        checkpoint = state(
            stockpile=quantities(exotic_gases=2),
            capacity=quantities(exotic_gases=10),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
            pending=(PendingProject(project=producer, completes_at_month=2),),
        )

        activation = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )

        self.assertIs(activation.truth, Truth.FALSE)
        self.assertTrue(activation.committed_recovery)

    def test_eventual_recovery_does_not_masquerade_as_timely_recovery(self) -> None:
        slow_producer = Project(
            project_id="slow-gas-recovery",
            lane=Lane.STRATEGIC_PRODUCER,
            base_priority=10,
            duration_months=24,
            completion_income=quantities(exotic_gases=1),
        )
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=10),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
            pending=(
                PendingProject(project=slow_producer, completes_at_month=24),
            ),
        )

        activation = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )
        fast_candidate = Project(
            project_id="fast-gas-recovery",
            lane=Lane.STRATEGIC_PRODUCER,
            base_priority=10,
            duration_months=1,
            strategic_resource="exotic_gases",
            completion_income=quantities(exotic_gases=1),
        )
        priorities = build_active_priority_set(
            checkpoint, (fast_candidate,), DEFICIT_ONLY_PLUS_ONE
        )
        same_speed_candidate = Project(
            project_id="same-speed-gas-recovery",
            lane=Lane.STRATEGIC_PRODUCER,
            base_priority=10,
            duration_months=24,
            strategic_resource="exotic_gases",
            completion_income=quantities(exotic_gases=1),
        )
        same_speed = build_active_priority_set(
            checkpoint, (same_speed_candidate,), DEFICIT_ONLY_PLUS_ONE
        )

        self.assertIs(activation.truth, Truth.TRUE)
        self.assertFalse(activation.committed_recovery)
        self.assertEqual(activation.runway_months, 0)
        self.assertEqual(
            tuple(item.project.project_id for item in priorities.active),
            ("fast-gas-recovery",),
        )
        self.assertEqual(same_speed.active, ())
        self.assertIn(
            ActivationReason.CANDIDATE_NOT_FASTER_THAN_COMMITTED,
            same_speed.decisions[0].activation.reasons,
        )

    def test_slow_committed_output_caps_duplicate_slow_producers(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=100),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )
        slow = Project(
            project_id="repeatable-slow-gas",
            lane=Lane.STRATEGIC_PRODUCER,
            base_priority=10,
            duration_months=12,
            strategic_resource="exotic_gases",
            completion_income=quantities(exotic_gases=1),
            repeatable=True,
        )

        run = run_policy_variant(
            checkpoint,
            (slow,),
            DEFICIT_ONLY_PLUS_ONE,
            months=12,
        )

        self.assertEqual(
            tuple(snapshot.selected.project_ids for snapshot in run.snapshots),
            (("repeatable-slow-gas",),) + ((),) * 11,
        )
        self.assertEqual(run.final_state.earned_income.get("exotic_gases"), 1)
        self.assertEqual(run.final_state.pending, ())

    def test_pending_output_beyond_commitment_horizon_still_caps_duplicates(self) -> None:
        for output, expected_starts in ((1, 1), (0.6, 2)):
            with self.subTest(output=output):
                checkpoint = state(
                    stockpile=quantities(exotic_gases=0),
                    capacity=quantities(exotic_gases=100),
                    earned_income=quantities(exotic_gases=0),
                    active_upkeep=quantities(exotic_gases=1),
                    deficit_status=fact_set(exotic_gases=Truth.TRUE),
                    unlocked_resources=frozenset({"exotic_gases"}),
                )
                producer = Project(
                    project_id=f"very-slow-gas-{output}",
                    lane=Lane.STRATEGIC_PRODUCER,
                    base_priority=10,
                    duration_months=36,
                    strategic_resource="exotic_gases",
                    completion_income=quantities(exotic_gases=output),
                    repeatable=True,
                )

                run = run_policy_variant(
                    checkpoint,
                    (producer,),
                    DEFICIT_ONLY_PLUS_ONE,
                    months=12,
                )

                starts = sum(
                    bool(snapshot.selected.projects)
                    for snapshot in run.snapshots
                )
                self.assertEqual(starts, expected_starts)
                self.assertEqual(len(run.final_state.pending), expected_starts)

    def test_partial_pending_output_only_requests_the_remaining_gap(self) -> None:
        partial = Project(
            project_id="partial-slow-gas",
            lane=Lane.STRATEGIC_PRODUCER,
            base_priority=10,
            duration_months=12,
            strategic_resource="exotic_gases",
            completion_income=quantities(exotic_gases=0.6),
            repeatable=True,
        )
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=100),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
            pending=(PendingProject(partial, completes_at_month=12),),
        )

        activation = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )
        run = run_policy_variant(
            checkpoint,
            (partial,),
            DEFICIT_ONLY_PLUS_ONE,
            months=2,
        )

        self.assertEqual(activation.requested_income, quantities(x=0.4).get("x"))
        self.assertEqual(
            tuple(snapshot.selected.project_ids for snapshot in run.snapshots),
            (("partial-slow-gas",), ()),
        )
        self.assertEqual(len(run.final_state.pending), 2)

    def test_bounded_increment_responds_to_burn_without_multiplying_it(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=100),
            earned_income=quantities(exotic_gases=1),
            active_upkeep=quantities(exotic_gases=10),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )

        activation = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )

        self.assertIs(activation.truth, Truth.TRUE)
        self.assertEqual(activation.net_earned_income, -9)
        self.assertEqual(activation.requested_income, 1)

    def test_committed_recovery_counts_net_output_after_future_upkeep(self) -> None:
        consumer = Project(
            project_id="gas-consuming-project",
            lane=Lane.RESEARCH,
            base_priority=10,
            completion_income=quantities(exotic_gases=1),
            completion_upkeep=quantities(exotic_gases=1),
        )
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=10),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
            pending=(PendingProject(project=consumer, completes_at_month=1),),
        )

        activation = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )

        self.assertIs(activation.truth, Truth.TRUE)
        self.assertFalse(activation.committed_recovery)

    def test_market_bridge_does_not_masquerade_as_earned_recovery(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=10),
            earned_income=quantities(exotic_gases=0),
            market_income=quantities(exotic_gases=2),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )

        activation = evaluate_policy_activation(
            checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
        )

        self.assertIs(activation.truth, Truth.TRUE)
        self.assertEqual(activation.net_earned_income, -1)
        self.assertEqual(activation.requested_income, 1)

    def test_prezero_policy_projects_known_pending_consumers(self) -> None:
        consumer = Project(
            project_id="future-gas-consumer",
            lane=Lane.RESEARCH,
            base_priority=10,
            duration_months=2,
            completion_upkeep=quantities(exotic_gases=2),
        )
        checkpoint = state(
            stockpile=quantities(exotic_gases=1),
            capacity=quantities(exotic_gases=10),
            earned_income=quantities(exotic_gases=1),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.FALSE),
            unlocked_resources=frozenset({"exotic_gases"}),
            pending=(PendingProject(consumer, completes_at_month=2),),
        )

        activation = evaluate_policy_activation(
            checkpoint, PREZERO_RUNWAY_PLUS_ONE, "exotic_gases"
        )

        self.assertIs(activation.truth, Truth.TRUE)
        self.assertIn(ActivationReason.PREZERO_RUNWAY, activation.reasons)
        self.assertEqual(activation.runway_months, 2)
        self.assertEqual(activation.requested_income, 1)

        unused_checkpoint = state(
            stockpile=quantities(exotic_gases=1),
            capacity=quantities(exotic_gases=10),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=0),
            deficit_status=fact_set(exotic_gases=Truth.FALSE),
            unlocked_resources=frozenset({"exotic_gases"}),
            pending=(PendingProject(consumer, completes_at_month=2),),
        )
        future_use = evaluate_policy_activation(
            unused_checkpoint,
            PREZERO_RUNWAY_PLUS_ONE,
            "exotic_gases",
        )
        self.assertIs(future_use.truth, Truth.TRUE)
        self.assertEqual(future_use.runway_months, 2)

    def test_bundle_feasibility_prevents_double_spending(self) -> None:
        checkpoint = state(stockpile=quantities(minerals=100))
        first = Project(
            project_id="first",
            lane=Lane.RESEARCH,
            base_priority=10,
            one_time_cost=quantities(minerals=60),
        )
        second = Project(
            project_id="second",
            lane=Lane.DEFENSE,
            base_priority=10,
            one_time_cost=quantities(minerals=60),
        )

        self.assertTrue(evaluate_bundle_feasibility(checkpoint, (first,)).feasible)
        self.assertTrue(evaluate_bundle_feasibility(checkpoint, (second,)).feasible)
        combined = evaluate_bundle_feasibility(checkpoint, (first, second))

        self.assertFalse(combined.feasible)
        self.assertIn(
            (FeasibilityCode.RESOURCE, "minerals"),
            {(reason.code, reason.key) for reason in combined.reasons},
        )

    def test_queue_capacity_is_distinct_from_affordability(self) -> None:
        checkpoint = state(
            stockpile=quantities(minerals=1000),
            queue_capacity=quantities(planetary=1),
            queue_used=quantities(planetary=1),
        )
        project = Project(
            project_id="queued-lab",
            lane=Lane.RESEARCH,
            base_priority=10,
            one_time_cost=quantities(minerals=100),
            queue="planetary",
        )

        result = evaluate_bundle_feasibility(checkpoint, (project,))

        self.assertFalse(result.feasible)
        self.assertEqual(
            {(reason.code, reason.key) for reason in result.reasons},
            {(FeasibilityCode.QUEUE, "planetary")},
        )

    def test_pending_queue_reservations_must_match_queue_usage(self) -> None:
        queued = Project(
            project_id="already-building",
            lane=Lane.RESEARCH,
            base_priority=10,
            queue="planetary",
            duration_months=2,
        )

        with self.assertRaisesRegex(ValueError, "pending queue reservations"):
            state(
                queue_capacity=quantities(planetary=1),
                queue_used=quantities(planetary=0),
                pending=(PendingProject(queued, completes_at_month=2),),
            )

    def test_budget_pools_are_not_fungible(self) -> None:
        checkpoint = state(
            budgets=quantities(construction=100, military=0),
        )
        project = Project(
            project_id="new-corvette",
            lane=Lane.NEW_HULLS,
            base_priority=10,
            budget_cost=quantities(military=10),
        )

        result = evaluate_bundle_feasibility(checkpoint, (project,))

        self.assertFalse(result.feasible)
        self.assertEqual(
            {(reason.code, reason.key) for reason in result.reasons},
            {(FeasibilityCode.BUDGET, "military")},
        )

    def test_completion_upkeep_must_preserve_operating_runway(self) -> None:
        project = Project(
            project_id="unsupported-upkeep",
            lane=Lane.MEGASTRUCTURE,
            base_priority=10,
            completion_upkeep=quantities(energy=100),
        )

        result = evaluate_bundle_feasibility(state(), (project,))

        self.assertFalse(result.feasible)
        self.assertIn(
            (FeasibilityCode.RUNWAY, "energy"),
            {(reason.code, reason.key) for reason in result.reasons},
        )

    def test_operating_window_starts_after_long_construction_completes(self) -> None:
        checkpoint = state(
            stockpile=quantities(energy=1000),
            capacity=quantities(energy=1000),
            earned_income=quantities(energy=10),
            active_upkeep=quantities(energy=0),
        )
        project = Project(
            project_id="long-build-unsupported-upkeep",
            lane=Lane.MEGASTRUCTURE,
            base_priority=10,
            duration_months=12,
            completion_upkeep=quantities(energy=100),
        )

        result = evaluate_bundle_feasibility(
            checkpoint, (project,), horizon_months=12
        )

        self.assertFalse(result.feasible)
        self.assertIn(
            (FeasibilityCode.RUNWAY, "energy"),
            {(reason.code, reason.key) for reason in result.reasons},
        )
        search = find_feasible_bundles(
            checkpoint, (project,), horizon_months=12
        )
        self.assertEqual(search.feasible[0].project_ids, ())
        self.assertEqual(search.rejected[0].project_ids, (project.project_id,))
        with self.assertRaisesRegex(ValueError, "runway:energy"):
            schedule_bundle(checkpoint, (project,), horizon_months=12)

    def test_new_upkeep_cannot_deepen_an_existing_deficit(self) -> None:
        checkpoint = state(
            stockpile=quantities(energy=0),
            earned_income=quantities(energy=0),
            active_upkeep=quantities(energy=1),
        )
        project = Project(
            project_id="deficit-amplifier",
            lane=Lane.MEGASTRUCTURE,
            base_priority=10,
            completion_upkeep=quantities(energy=100),
        )

        result = evaluate_bundle_feasibility(checkpoint, (project,))

        self.assertFalse(result.feasible)
        runway = next(
            reason
            for reason in result.reasons
            if reason.code is FeasibilityCode.RUNWAY and reason.key == "energy"
        )
        self.assertGreater(runway.required, runway.available)

    def test_slot_job_and_influence_constraints_are_first_class(self) -> None:
        checkpoint = state(
            slot_capacity=quantities(building=1),
            slot_used=quantities(building=1),
            job_capacity=quantities(specialist=2),
            job_used=quantities(specialist=2),
            influence=4,
        )
        project = Project(
            project_id="constrained-project",
            lane=Lane.EXPANSION,
            base_priority=10,
            slot_cost=quantities(building=1),
            job_cost=quantities(specialist=1),
            influence_cost=5,
        )

        result = evaluate_bundle_feasibility(checkpoint, (project,))

        self.assertEqual(
            {reason.code for reason in result.reasons},
            {FeasibilityCode.SLOT, FeasibilityCode.JOB, FeasibilityCode.INFLUENCE},
        )

    def test_completion_and_upkeep_begin_at_the_month_boundary(self) -> None:
        checkpoint = state(
            stockpile=quantities(energy=100),
            capacity=quantities(energy=1000),
            earned_income=quantities(energy=0),
            market_income=quantities(energy=0),
            active_upkeep=quantities(energy=0),
            queue_capacity=quantities(planetary=1),
            queue_used=quantities(planetary=0),
        )
        project = Project(
            project_id="power-plant",
            lane=Lane.PLANETARY_DEVELOPMENT,
            base_priority=10,
            queue="planetary",
            duration_months=1,
            completion_income=quantities(energy=3),
            completion_upkeep=quantities(energy=1),
            add_gates=frozenset({"plant_complete"}),
        )
        rules = (
            GateRule(
                rule_id="plant-opens-grid",
                requires_all=frozenset({"plant_complete"}),
                add=frozenset({"grid_online"}),
            ),
            GateRule(
                rule_id="grid-opens-upgrade",
                requires_all=frozenset({"grid_online"}),
                add=frozenset({"upgrade_available"}),
            ),
        )

        scheduled = schedule_bundle(checkpoint, (project,))
        at_completion = advance_month(scheduled, gate_rules=rules)

        self.assertEqual(at_completion.month, 1)
        self.assertEqual(at_completion.stockpile.get("energy"), 100)
        self.assertEqual(at_completion.earned_income.get("energy"), 3)
        self.assertEqual(at_completion.active_upkeep.get("energy"), 1)
        self.assertEqual(at_completion.queue_used.get("planetary"), 0)
        self.assertTrue(
            {"plant_complete", "grid_online", "upgrade_available"}
            <= at_completion.gates
        )

        one_month_operating = advance_month(at_completion, gate_rules=rules)
        self.assertEqual(one_month_operating.stockpile.get("energy"), 102)

    def test_jobs_are_reserved_at_start_but_consumed_only_on_completion(self) -> None:
        checkpoint = state(
            job_capacity=quantities(specialist=1),
            job_used=quantities(specialist=0),
        )
        first = Project(
            project_id="first-specialist-workplace",
            lane=Lane.RESEARCH,
            base_priority=10,
            duration_months=2,
            job_cost=quantities(specialist=1),
        )
        second = Project(
            project_id="second-specialist-workplace",
            lane=Lane.PLANETARY_DEVELOPMENT,
            base_priority=10,
            duration_months=2,
            job_cost=quantities(specialist=1),
        )

        scheduled = schedule_bundle(checkpoint, (first,))
        self.assertEqual(scheduled.job_used.get("specialist"), 0)
        self.assertFalse(evaluate_bundle_feasibility(scheduled, (second,)).feasible)

        building = advance_month(scheduled)
        self.assertEqual(building.job_used.get("specialist"), 0)
        completed = advance_month(building)
        self.assertEqual(completed.job_used.get("specialist"), 1)

    def test_runs_are_reproducible_without_mutating_the_start(self) -> None:
        checkpoint = state(
            stockpile=quantities(minerals=20),
            capacity=quantities(minerals=100),
            earned_income=quantities(minerals=10),
        )
        project = Project(
            project_id="lab",
            lane=Lane.RESEARCH,
            base_priority=10,
            one_time_cost=quantities(minerals=10),
        )

        first = run_policy_variant(checkpoint, (project,), PARENT_ONLY, months=2)
        second = run_policy_variant(checkpoint, (project,), PARENT_ONLY, months=2)

        self.assertEqual(first, second)
        self.assertEqual(checkpoint.month, 0)
        self.assertEqual(checkpoint.stockpile.get("minerals"), 20)
        self.assertEqual(checkpoint.pending, ())

    def test_equal_priority_ties_are_deterministic_across_input_order(self) -> None:
        checkpoint = state(stockpile=quantities(minerals=60))
        alpha = Project(
            project_id="alpha",
            lane=Lane.RESEARCH,
            base_priority=10,
            one_time_cost=quantities(minerals=60),
        )
        beta = Project(
            project_id="beta",
            lane=Lane.DEFENSE,
            base_priority=10,
            one_time_cost=quantities(minerals=60),
        )

        forward = run_policy_variant(
            checkpoint, (alpha, beta), PARENT_ONLY, months=1
        )
        reverse = run_policy_variant(
            checkpoint, (beta, alpha), PARENT_ONLY, months=1
        )

        self.assertEqual(forward.snapshots[0].selected.project_ids, ("alpha",))
        self.assertEqual(reverse.snapshots[0].selected.project_ids, ("alpha",))

    def test_one_requested_income_does_not_select_two_full_producers(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=100),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )
        projects = tuple(
            Project(
                project_id=f"gas-producer-{index}",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=10,
                strategic_resource="exotic_gases",
                completion_income=quantities(exotic_gases=1),
            )
            for index in range(2)
        )

        run = run_policy_variant(
            checkpoint, projects, DEFICIT_ONLY_PLUS_ONE, months=1
        )

        self.assertEqual(run.snapshots[0].selected.project_ids, ("gas-producer-0",))

    def test_two_requested_income_selects_two_but_not_three_full_producers(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=100),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=2),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )
        projects = tuple(
            Project(
                project_id=f"gas-producer-{index}",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=10,
                strategic_resource="exotic_gases",
                completion_income=quantities(exotic_gases=1),
            )
            for index in range(3)
        )

        run = run_policy_variant(
            checkpoint, projects, DEFICIT_ONLY_PLUS_TWO, months=1
        )

        self.assertEqual(
            run.snapshots[0].selected.project_ids,
            ("gas-producer-0", "gas-producer-1"),
        )

    def test_fractional_producers_allow_only_unavoidable_overshoot(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=100),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )
        projects = tuple(
            Project(
                project_id=f"fractional-gas-{index}",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=10,
                strategic_resource="exotic_gases",
                completion_income=quantities(exotic_gases=0.6),
            )
            for index in range(3)
        )

        run = run_policy_variant(
            checkpoint, projects, DEFICIT_ONLY_PLUS_ONE, months=1
        )

        self.assertEqual(
            run.snapshots[0].selected.project_ids,
            ("fractional-gas-0", "fractional-gas-1"),
        )

    def test_exact_recovery_beats_high_priority_extreme_overshoot(self) -> None:
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=1000),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )
        projects = (
            Project(
                project_id="exact-plus-one",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=1,
                strategic_resource="exotic_gases",
                completion_income=quantities(exotic_gases=1),
            ),
            Project(
                project_id="oversized-plus-hundred",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=100,
                strategic_resource="exotic_gases",
                completion_income=quantities(exotic_gases=100),
            ),
            Project(
                project_id="fractional-high-a",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=100,
                strategic_resource="exotic_gases",
                completion_income=quantities(exotic_gases=0.9),
            ),
            Project(
                project_id="fractional-high-b",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=100,
                strategic_resource="exotic_gases",
                completion_income=quantities(exotic_gases=0.9),
            ),
        )

        run = run_policy_variant(
            checkpoint, projects, DEFICIT_ONLY_PLUS_ONE, months=1
        )

        self.assertEqual(
            run.snapshots[0].selected.project_ids,
            ("exact-plus-one",),
        )

    def test_pending_nonrepeatable_project_is_not_started_twice(self) -> None:
        project = Project(
            project_id="nonrepeatable",
            lane=Lane.RESEARCH,
            base_priority=10,
            duration_months=2,
        )
        checkpoint = state(
            pending=(PendingProject(project, completes_at_month=2),),
        )

        run = run_policy_variant(checkpoint, (project,), PARENT_ONLY, months=1)

        self.assertEqual(run.snapshots[0].selected.project_ids, ())
        self.assertEqual(
            tuple(item.project.project_id for item in run.final_state.pending),
            ("nonrepeatable",),
        )

    def test_pending_input_order_does_not_change_committed_recovery(self) -> None:
        projects = (
            Project(
                project_id="huge",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=1,
                completion_income=quantities(exotic_gases="1e28"),
            ),
            Project(
                project_id="small-a",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=1,
                completion_income=quantities(exotic_gases=6),
            ),
            Project(
                project_id="small-b",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=1,
                completion_income=quantities(exotic_gases=6),
            ),
        )

        def activation(pending_projects: tuple[Project, ...]):
            checkpoint = state(
                stockpile=quantities(exotic_gases=0),
                capacity=quantities(exotic_gases="1e30"),
                earned_income=quantities(exotic_gases=0),
                active_upkeep=quantities(
                    exotic_gases="10000000000000000000000000015"
                ),
                deficit_status=fact_set(exotic_gases=Truth.TRUE),
                unlocked_resources=frozenset({"exotic_gases"}),
                pending=tuple(
                    PendingProject(project, completes_at_month=1)
                    for project in pending_projects
                ),
            )
            return evaluate_policy_activation(
                checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
            )

        self.assertEqual(activation(projects), activation(tuple(reversed(projects))))

    def test_external_decimal_precision_cannot_change_policy_outcomes(self) -> None:
        pending = tuple(
            PendingProject(
                Project(
                    project_id=project_id,
                    lane=Lane.STRATEGIC_PRODUCER,
                    base_priority=1,
                    completion_income=quantities(exotic_gases=output),
                ),
                completes_at_month=1,
            )
            for project_id, output in (
                ("large", "1000"),
                ("fraction-a", "0.6"),
                ("fraction-b", "0.6"),
            )
        )
        checkpoint = state(
            stockpile=quantities(exotic_gases=0),
            capacity=quantities(exotic_gases=10000),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases="1001.1"),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
            pending=pending,
        )

        with localcontext() as context:
            context.prec = 3
            low_precision = evaluate_policy_activation(
                checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
            )
        with localcontext() as context:
            context.prec = 28
            normal_precision = evaluate_policy_activation(
                checkpoint, DEFICIT_ONLY_PLUS_ONE, "exotic_gases"
            )

        self.assertEqual(low_precision, normal_precision)
        self.assertTrue(low_precision.committed_recovery)

    def test_simultaneous_gate_add_remove_conflict_fails_independent_of_rule_ids(self) -> None:
        rules = (
            GateRule(
                rule_id="add-x",
                requires_all=frozenset({"seed"}),
                add=frozenset({"x"}),
            ),
            GateRule(
                rule_id="remove-x",
                requires_all=frozenset({"seed"}),
                remove=frozenset({"x"}),
            ),
        )

        with self.assertRaisesRegex(ValueError, "conflicting gate transitions"):
            evaluate_gate_transitions(frozenset({"seed"}), rules)

    def test_failed_c9_variant_causes_counterfactual_collateral_starvation(self) -> None:
        checkpoint = state(
            stockpile=quantities(minerals=60, exotic_gases=0),
            capacity=quantities(minerals=1000, exotic_gases=1000),
            earned_income=quantities(minerals=60, exotic_gases=0),
            active_upkeep=quantities(exotic_gases=0),
            deficit_status=fact_set(exotic_gases=Truth.FALSE),
            unlocked_resources=frozenset({"exotic_gases"}),
            queue_capacity=quantities(planetary=1),
            queue_used=quantities(planetary=0),
        )
        projects = (
            Project(
                project_id="gas-overreaction",
                lane=Lane.STRATEGIC_PRODUCER,
                base_priority=10,
                one_time_cost=quantities(minerals=60),
                queue="planetary",
                duration_months=1,
                completion_income=quantities(exotic_gases=1),
                strategic_resource="exotic_gases",
                repeatable=True,
            ),
            Project(
                project_id="research-lab",
                lane=Lane.RESEARCH,
                base_priority=100,
                one_time_cost=quantities(minerals=60),
                queue="planetary",
                duration_months=1,
                repeatable=True,
            ),
        )

        comparison = compare_policy_variants(
            checkpoint,
            projects,
            baseline=PARENT_ONLY,
            variants=(FAILED_C9,),
            months=3,
            starvation_months=3,
        )
        failed = comparison.variants[0]

        self.assertEqual(
            tuple(snapshot.selected.project_ids for snapshot in failed.run.snapshots),
            (("gas-overreaction",),) * 3,
        )
        self.assertEqual(len(failed.starvation), 1)
        self.assertIs(failed.starvation[0].lane, Lane.RESEARCH)
        self.assertIn(
            (FeasibilityCode.RESOURCE, "minerals"),
            failed.starvation[0].shared_bottlenecks,
        )

        with self.assertRaisesRegex(ValueError, "policy-off counterfactual"):
            detect_lane_starvation(
                failed.run, failed.run, minimum_consecutive_months=3
            )

    def test_policy_upkeep_can_cause_persistent_runway_starvation(self) -> None:
        checkpoint = state(
            stockpile=quantities(energy=0, exotic_gases=0),
            capacity=quantities(energy=1000, exotic_gases=100),
            earned_income=quantities(energy=10, exotic_gases=0),
            active_upkeep=quantities(energy=0, exotic_gases=1),
            deficit_status=fact_set(exotic_gases=Truth.TRUE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )
        gas = Project(
            project_id="gas-recovery-with-energy-upkeep",
            lane=Lane.STRATEGIC_PRODUCER,
            base_priority=1,
            duration_months=1,
            completion_income=quantities(exotic_gases=1),
            completion_upkeep=quantities(energy=6),
            strategic_resource="exotic_gases",
        )
        research = Project(
            project_id="energy-using-research",
            lane=Lane.RESEARCH,
            base_priority=100,
            duration_months=1,
            completion_upkeep=quantities(energy=6),
        )

        comparison = compare_policy_variants(
            checkpoint,
            (gas, research),
            baseline=PARENT_ONLY,
            variants=(DEFICIT_ONLY_PLUS_ONE,),
            months=3,
            starvation_months=3,
            operating_horizon_months=12,
        )
        bounded = comparison.variants[0]

        self.assertEqual(
            bounded.run.snapshots[0].selected.project_ids,
            ("gas-recovery-with-energy-upkeep",),
        )
        self.assertEqual(len(bounded.starvation), 1)
        self.assertIs(bounded.starvation[0].lane, Lane.RESEARCH)
        self.assertEqual(bounded.starvation[0].months, (0, 1, 2))
        self.assertIn(
            (FeasibilityCode.RUNWAY, "energy"),
            bounded.starvation[0].shared_bottlenecks,
        )

    def test_starvation_requires_the_same_counterfactual_project(self) -> None:
        checkpoint = state(
            stockpile=quantities(minerals=0, exotic_gases=0),
            capacity=quantities(minerals=100, exotic_gases=100),
            earned_income=quantities(exotic_gases=0),
            active_upkeep=quantities(exotic_gases=0),
            deficit_status=fact_set(exotic_gases=Truth.FALSE),
            unlocked_resources=frozenset({"exotic_gases"}),
        )
        gas = Project(
            project_id="failed-policy-gas",
            lane=Lane.STRATEGIC_PRODUCER,
            base_priority=1,
            completion_income=quantities(exotic_gases=1),
            strategic_resource="exotic_gases",
            repeatable=True,
        )
        impossible = Project(
            project_id="inherently-impossible-research",
            lane=Lane.RESEARCH,
            base_priority=1,
            one_time_cost=quantities(minerals=100),
            repeatable=True,
        )
        feasible = Project(
            project_id="different-feasible-research",
            lane=Lane.RESEARCH,
            base_priority=100,
            repeatable=True,
        )

        comparison = compare_policy_variants(
            checkpoint,
            (gas, impossible, feasible),
            baseline=PARENT_ONLY,
            variants=(FAILED_C9,),
            months=3,
            starvation_months=3,
            max_bundle_size=1,
        )

        self.assertEqual(comparison.variants[0].starvation, ())

    def test_starvation_comparison_rejects_mismatched_scenarios(self) -> None:
        checkpoint = state()
        first = Project(
            project_id="first",
            lane=Lane.RESEARCH,
            base_priority=1,
        )
        second = Project(
            project_id="second",
            lane=Lane.RESEARCH,
            base_priority=1,
        )
        policy_run = run_policy_variant(
            checkpoint, (first,), FAILED_C9, months=1
        )
        policy_off = run_policy_variant(
            checkpoint, (second,), PARENT_ONLY, months=1
        )

        with self.assertRaisesRegex(ValueError, "identical scenarios"):
            detect_lane_starvation(policy_run, policy_off)

    def test_exact_bundle_search_refuses_non_fixture_candidate_counts(self) -> None:
        projects = tuple(
            Project(
                project_id=f"candidate-{index:02d}",
                lane=Lane.RESEARCH,
                base_priority=1,
            )
            for index in range(13)
        )

        with self.assertRaises(ModelLimitError):
            find_feasible_bundles(
                state(), projects, max_candidates=12, max_bundle_size=2
            )

    def test_default_exact_search_does_not_silently_cap_bundle_width(self) -> None:
        projects = tuple(
            Project(
                project_id=f"lane-{index}",
                lane=lane,
                base_priority=1,
            )
            for index, lane in enumerate(tuple(Lane)[:5])
        )

        search = find_feasible_bundles(state(), projects)

        self.assertIn(
            tuple(project.project_id for project in projects),
            {result.project_ids for result in search.feasible},
        )


if __name__ == "__main__":
    unittest.main()
