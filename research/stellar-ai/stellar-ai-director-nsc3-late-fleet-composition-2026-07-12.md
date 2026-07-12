# NSC3 late-tech fleet composition compatibility

Target: active Pegasus 4.4.4 stack with NSC3 (Steam 683230077). Runtime launch is not authorized. The user-observed save had roughly 91/509 naval capacity, 35 idle shipyard slots, zero queued ships, satisfied 21/21 templates, and a small-hull-heavy serialized template despite unlocked capital hulls. This proves affordability and throughput were not the immediate demand blockers.

NSC3 documents `ship_size.ai_ship_data.fraction` as the native desired-composition surface: buildable hulls are filtered, fractions are normalized, and desired ship count is divided by `size_multiplier`. No exposed data surface was found for forcing fleet-template creation or refresh. This patch therefore improves future late-tech desired composition but does not claim to rewrite or expand an already-satisfied serialized template.

## Exact boundary

The focused generator copies exactly nine active NSC3 final-winner objects: Corvette, Frigate, Destroyer, Cruiser, Battleship, StrikeCruiser, Battlecruiser, Carrier, and Dreadnought. Each source object is hash-locked. All content outside `ai_ship_data` is byte-equivalent after normalization.

Early and gate-false fractions remain exactly NSC3. Once Battleships are available:

- Corvette, Frigate, Destroyer, Cruiser, StrikeCruiser, and Battlecruiser receive factor 0.
- Battleship, Carrier, and Dreadnought retain their parent fractions.

No hull definition, design, or construction rule is disabled and no absolute `min` is added; only desired AI composition changes. A neutral model of the user save's Battleship + StrikeCruiser + Battlecruiser unlock set requests only Battleships among those unlocked standard hulls and reduces expected entity count. Carrier and Dreadnought become eligible through their unchanged parent fractions when separately unlocked. This is deterministic composition math, not runtime template proof.

## Top five risks and controls

1. **Existing template does not refresh:** fraction changes may affect only newly formed or reevaluated templates. Control: do not claim demand resolution; runtime A/B records template targets/current counts over 2–5 years.
2. **No mixed-fleet screens:** Battleship-era fleets will not request smaller screening hulls. Control: this is the user's explicit doctrine; it activates only after Battleships and leaves all hulls legal for player or special-script use.
3. **Fewer entities also means less total demand:** larger hulls reduce ship count and may not fill unused naval capacity if templates remain stale. Control: recurring wartime affordability remains separate; no unsafe `min` mode or Corvette inflation is used.
4. **NSC3 source drift:** a Workshop update could make copied full objects stale. Control: per-object SHA-256 checks fail generation closed and tests compare every non-`ai_ship_data` byte.
5. **Global or special-hull spill:** standard fleet weights could accidentally affect bioships, federation ships, Arkships, or civilians. Control: exact nine-object allowlist; no other ship size, section, design, event, order, or resource surface is generated.

## Static and runtime proof boundary

Static proof covers the exact objects, active-source hashes, source parity outside `ai_ship_data`, late-tech-only modifiers, non-increasing small-hull factors, absence of absolute minima, modeled entity/share direction, parseability, and native-AI-only constraints. It cannot prove template refresh, queues, utilization, composition actually built, fleet power, performance, or war completion.

Runtime acceptance on a copied save records, per country: max/used naval capacity; template target/current/queued hull counts; reinforcement deficit; shipyard capacity/active/queued; unlocked/buildable designs; expected active-source fractions; actual hull counts; and fleet power at baseline and after 2–5 years. Rollback is one fine-grained commit deleting the generated ship-size file and its focused generator/tests/note.
