# Mechanist origin robot-assembly consumer

Target: active Pegasus 4.4.4 vanilla `building_robot_assembly_plant` and `building_robot_assembly_complex`. The Director already modeled the `pop_assembly_snowball_core` route and Mechanist preference, but the focused H08 generator did not emit either native building consumer. This slice materializes exactly those two full source objects.

The copied legality, policy, slot, destruction, job, cost, upkeep, upgrade, and prerequisite rules remain authoritative. The Director adds its existing route readiness veto, coefficients, and bounded identity tie-breakers: Mechanist or synthetic empires receive factor 1.5, and Materialist empires factor 1.15. These factors may combine, so the maximum identity multiplier is 1.725; the route still cannot activate unless `staid_pop_assembly_snowball_ready` is true, which excludes Nomads and catastrophic collapse and requires safe runway, high-scale pressure, or construction spenddown plus a time/capacity/research condition.

## Top five risks and controls

1. **Vanilla object drift:** a copied building could silently lose updated legality or costs. Control: exact two-object SHA-256 locks fail generation closed.
2. **Assembly crowds out urgent infrastructure:** compounding growth may be attractive while immediate jobs are needed. Control: original AI slot safeguards remain, and the Director route is disabled outside its readiness state.
3. **Economic overcommitment:** robot assembly consumes building slots, energy, minerals, and later crystals. Control: original costs/upkeep remain and the route requires an economy/runway pressure signal; runtime observation must still verify sustained affordability.
4. **Excessive modifier stacking:** Mechanist/synthetic and Materialist factors multiply. Control: the factors were reduced from dormant 6×4 values to bounded tie-breakers with a tested combined ceiling of 1.725.
5. **Overbroad origin work:** emitting every assembly building would broaden behavior to machines, clones, and hives without a completed evidence review. Control: fixed allowlist contains only the two robot-assembly objects; all five other modeled assembly objects remain absent.

## Proof boundary and rollback

Static proof covers the exact allowlist, source hashes, legality markers, route gate, identity multipliers, exclusion of other assembly objects, parser validity, and focused generator idempotence. Static weighting cannot prove that a planet has a legal slot, that the planner queues the building, or that growth repays its opportunity cost. Runtime acceptance should compare Mechanist and otherwise-similar non-Mechanist empires across queue timing, energy/mineral runway, unemployment, and sustained assembly output.

Rollback is one fine-grained commit removing the focused artifact and its renderer wiring while leaving the previously dormant general route model intact.
