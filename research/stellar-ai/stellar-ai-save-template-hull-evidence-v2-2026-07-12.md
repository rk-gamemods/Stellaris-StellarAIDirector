# Save template hull evidence v2

The read-only save evidence extractor now resolves fleet-template target and current ships through serialized design IDs and `ship_design.growth_stages.ship_size`. JSON exposes per-template and per-empire target, current, and reinforcement-demand hull maps; CSV includes stable JSON columns for the three aggregate maps.

The newest inspected save, `autosave_2269.07.01.sav`, was hash-identical before and after extraction. Empire 0 has exactly the same target and current composition: 16 Corvettes, 3 Frigates, 1 Destroyer, and 1 Battlecruiser. Every per-hull reinforcement deficit is zero. This directly confirms that 35 idle shipyard slots and abundant resources cannot produce ships while the serialized templates request none.

## Risks and controls

1. **Design growth-stage mismatch:** a ship can reference a nonzero growth stage. Control: resolve the serialized stage index and fall back only when the indexed stage is unavailable.
2. **Missing ship/design records:** stale references can undercount a hull. Control: classify the hull as `unknown` and preserve a warning rather than silently dropping it.
3. **Queued-hull ambiguity:** `all_queued` does not expose a proven hull mapping in the current parser. Control: per-hull reinforcement is emitted only when the queued count is zero; aggregate reinforcement retains the prior conservative contract.
4. **Human/AI misclassification:** absence of human history does not prove current AI control. Control: retain the existing explicit uncertainty classification.
5. **Save mutation:** diagnostic extraction must never alter user state. Control: input/output overwrite guard, deterministic ZIP read, hash-before/after runtime check, and synthetic read-only regression test.

Static extraction proves serialized state only. It does not prove when the executable reevaluates fractions or refreshes templates. Runtime A/B remains necessary to observe whether the new Battleship-era composition changes template targets on an existing save.
