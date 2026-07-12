# Stellar AI Director Threat Response Retirement

## H09a Decision

- Retire the production `on_war_beginning` event chain, galaxy-wide observer
  loop, timed flags, relation writes, and threat-readiness economic subplan.
- Preserve the ten legacy opinion IDs and localization as zero-effect
  compatibility definitions so serialized references in copied saves resolve.
- Do not add a migration event. Existing flags are inert because no production
  trigger, plan, event, or on-action consumes them.

## Save Classification

Cleanup-required, copied-save-only. Static checks prove the absence of new
writes and live consumers. A copied-save runtime check is still required to
prove the retained zero-effect definitions load cleanly while old timed
references expire.

## Follow-up Boundary

Any later threat or arms-race behavior must be a separate native-only,
stateless, bounded slice. It must not restore these event, state, or absolute
income/stockpile mechanisms.
