# Open Questions and Local Verification Tasks

This packet targets Stellaris PC 4.4.4 stable and avoids inventing uncertain behavior.

## Highest-value local checks

1. Exact 4.4.4 schema and scope for `common/economic_plans/`.
2. Exact 4.4.4 schema and scope for `common/ai_budget/`.
3. Actual launcher active playset format and order on the user's machine.
4. `common/on_actions` merge behavior in Stellaris 4.4.4.
5. District/zone/zone-slot interactions under 4.4.4 and Planetary Diversity.
6. Starbase module/building `ai_weight` scope in local 4.4.4 and Starbase Extended.
7. Pop job resource block scopes.
8. Diplomacy/species-right actor/recipient/species/country scopes.
9. NSC3/ESC active winning ship sizes, sections, components, component sets, and global designs.
10. AI personality field semantics in local 4.4.4.
11. Trigger/effect names used in examples: verify all against local script documentation/CWTools before shipping.
12. Whether parent AI mod uses special scripted triggers/values that should be reused instead of new helpers.

## 4.5+ items to research separately

The target is 4.4.4. Label 4.5 findings separately. Verify:

- district/zone schema changes;
- economic plan additions/removals;
- AI budget syntax changes;
- new triggers/effects;
- launcher metadata changes;
- new DLC gates and DLC names;
- updated CWTools Stellaris config.

## Runtime-only questions

Static validation cannot answer:

- whether AI builds a specific megastructure over 50-100 years;
- whether modded component upkeep collapses economy;
- whether starbase spending crowds out fleets;
- whether research weights produce desired adoption;
- whether GUI layout is visually correct;
- whether diplomacy/personality changes create sane wars.

Define a controlled observer-run protocol only if the user permits runtime testing.

## Public-source gaps

Public docs do not fully specify:

- exact merge semantics for every folder;
- exact object order inside every folder;
- all supported `ai_weight` fields;
- all current 4.4.4 triggers/effects and scopes;
- hardcoded AI dominance over scriptable plans;
- launcher dependency resolution.

Use local game files, active mod files, CWTools, generated script documentation, and logs as source of truth.
