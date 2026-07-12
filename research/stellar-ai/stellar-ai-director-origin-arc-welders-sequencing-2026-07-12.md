# Arc Welders origin sequencing

Target: the active Pegasus 4.4.4 stack. This slice adds one bounded native-AI preference to the existing Director-owned `orbital_arc_furnace_1` start object. An empire with `origin_arc_welders` receives factor 1.15 when the existing Arc Furnace route, economy, and recovery gates already permit construction. The modifier evaluates the owning country through the megastructure object's established `from` scope and requires `is_nomadic = no`.

This is a sequencing preference, not a directive. It does not create an Arc Furnace, reserve resources, alter placement or prerequisites, rewrite the origin, or affect continuation stages. `origin_arc_welders_nomadic`, habitats, ring repairs, events, fleet templates, costs, and effects remain unchanged. No persistent origin classifier or helper state is introduced.

## Top five risks and controls

1. **Duplicating native origin preference:** an already-favored project could crowd out other useful starts. Control: one 1.15 factor on the exact start object; existing route weights and legality remain authoritative.
2. **Economic distraction:** an Arc Welder could start the project during collapse. Control: safe basic-economy runway is required, while survival, recovery, catastrophic collapse, and short-runway core deficit disable the preference.
3. **Wrong-scope evaluation:** checking the megastructure scope for an origin would silently fail. Control: generated regression proof requires the established country `from` scope.
4. **Nomad leakage:** the mobile Arc Welders variant could inherit stationary infrastructure assumptions. Control: `is_nomadic = no` is explicit and the nomadic origin identifier is absent.
5. **Stacking or source drift:** Megacorp and origin preferences can combine, or copied objects can lose parent behavior. Control: the intended combined ceiling is 1.15 x 1.10 = 1.265; shared-renderer additive parity and full-object validation preserve every non-`ai_weight` field.

## Proof boundary and rollback

Static proof covers the exact object, country scope, origin/Nomad conditions, bounded factor, safety gates, additive rendering, parser/reference validity, and absence of state mutation. Only runtime observation can prove that a legal site exists, a constructor selects it, the project starts, and the resulting economy remains healthy. No game launch or save mutation was performed.

Rollback is one fine-grained commit removing the single origin-specific modifier and this focused contract while retaining all broader identity megastructure sequencing.
