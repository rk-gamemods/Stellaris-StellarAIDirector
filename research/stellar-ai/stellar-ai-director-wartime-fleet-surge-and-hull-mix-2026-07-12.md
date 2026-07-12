# Wartime fleet surge and larger-hull mix

Target: Stellaris 4.4.4 active stack with NSC3 683230077; Stellar AI Director is the final enabled mod.

## Save evidence

Read-only forensic source: `autosave_2269.07.01.sav`, SHA256 `2F8465E2323E35E4E06D3CA8D76447BD647E191E0C9790F57A31FF4AA2D21CC7`.

Empire 0 was at war for roughly 13.6 years with 285,771.918 alloys and +2,503.799 alloys/month. It used 91 of an estimated 509 naval capacity (17.9%), had 35 parallel shipyard slots, and had no queued ships. Its two fleet templates were exactly satisfied at 21/21 ships, so reinforcement demand was zero. The 21 ships were 16 Corvettes, 3 Frigates, 1 Destroyer, and 1 Battlecruiser despite legal Cruiser, Battleship, Strike Cruiser, and Battlecruiser designs. Coalition mobile power exceeded the defender by roughly 7.2x, but the war remained unresolved.

This proves the immediate blocker is native desired-template/composition formation, not global alloy affordability or ship-budget potential.
The serialized 91 used naval capacity is exactly `15 Corvettes * 5 + 2 Frigates * 8`; in this active NSC3 stack those are `size_multiplier` costs. `fleet_slot_size` is command-limit usage, not the divisor in normalized `ai_ship_data` desired-count calculations.

## Native correction

- `staid_wartime_fleet_surge_ready` requires war, standard alloy ships, no collapse/core short-runway, safe two-month energy/alloy runway, less than 90% naval-cap use, at least one capital-hull technology, and an alloy stockpile above 5,000.
- `alloys_expenditure_ships` preserves vanilla potential, base weight, and 3x war factor. The surge adds a bounded 1.5 category factor and 5,000 desired minimum so the partitioned lane can afford a capital-hull decision. It cannot create a template or ship.
- No composition override ships in this slice. The evaluated all-hull minimum design could suppress parent fractions at smaller naval capacities, while the bounded two-object fallback created demand by raising Corvette/screen share—the opposite of the explicit larger-hull/performance requirement. Both were rejected before commit.

## Top five risks and controls

1. Template inertia: extra budget cannot refresh an already satisfied template by itself. Runtime acceptance therefore measures new/expanded template targets, not merely available budget.
2. Composition overreaction: raising small-hull fractions would recreate Corvette spam. This release leaves NSC3 composition untouched pending a native demand surface that can raise utilization while lowering Corvette share.
3. Capital-hull throughput: large ships take longer per slot and can temporarily reduce reinforcement responsiveness. Runtime follow-up must distinguish throughput delay from missing template demand.
4. Economic overreaction: wartime pressure could starve colonies or upgrades. The modifier requires real burn runway, stops at 90% cap, excludes biological fleets, and is only 1.5 on top of the native war factor.
5. NSC3 drift/load conflicts: a future composition patch will require active source hashes, exact parent parity tests, active-playset inventory, and final-load placement. No full-object NSC3 copy is included now.

## Runtime acceptance boundary

Static validation proves valid references, bounded gates, and absence of events/orders/free ships. It cannot prove the engine refreshes templates. Over the next 2-5 game years, record template target/current counts, queued and active shipyard slots, naval-cap utilization, hull mix by naval-cap share, fleet power, and war completion. The affordability slice succeeds if budget partitioning no longer blocks legal capital-hull construction; template growth and Cruiser-or-larger preference remain separate unresolved acceptance requirements.
