# Standalone Baseline Cleanup Archive Index

Date: 2026-07-08

This index marks historical Stellar AI Director evidence that should not be read
as the current standalone launch state. Generator-owned files are not relocated
by hand; this index is the archive boundary for interpretation.

## Historical Or Superseded Evidence

| Artifact | Archive reason | Current replacement |
| --- | --- | --- |
| `stellar-ai-director-observer-smoke-save-summary-2026-07-04.md` | Historical observer smoke summary. It is useful evidence, but it is not proof for the post-standalone cleanup state. | Run a new user-approved observer pass after the committed standalone baseline. |
| `observer-runs/observer-20260707T*/` | Historical observer-run evidence and checkpoint/log summaries. These runs must not be treated as current standalone proof unless explicitly revalidated against the post-cleanup live descriptor and `dlc_load.json`. | Current gap document keeps runtime observer proof open. |
| `stellar-ai-director-full-replacement-plan-2026-07-06.md` | Historical broad replacement plan. Some surfaces are now implemented or deliberately deferred by the standalone parity inventory. | `stellar-ai-director-standalone-parity-inventory-2026-07-08.md` and `stellar-ai-director-standalone-baseline-cleanup-2026-07-08.md`. |
| `stellar-ai-director-high-scale-replacement-audit-2026-07-06.md` | Historical high-scale audit. It remains provenance for route choices but not the current gap list. | Current parity inventory, route reports, generated audits, and cleanup gap table. |
| `stellar-ai-director-route-overrides-2026-07-06.*` | Generated route evidence remains useful, but old manual-review blockers are now interpreted through the standalone gap list. | Current route/generated audits plus the cleanup gap table. |
| `stellar-ai-director-launch-comparison-2026-07-04.md` and older launch notes when present | Historical launch-state evidence from before this cleanup. | Live descriptor and `dlc_load.json` checks from the current validation run. |

## Current Reading Rule

Use current files first:

- `mods/StellarAIDirector/README.md`
- `mods/StellarAIDirector/descriptor.mod`
- `mods/StellarAIDirector/notes/load-order.md`
- `research/stellar-ai/README.md`
- `research/stellar-ai/stellar-ai-director-standalone-parity-inventory-2026-07-08.md`
- `research/stellar-ai/stellar-ai-director-standalone-baseline-cleanup-2026-07-08.md`

Use historical files only for provenance or when a future task explicitly asks
to revisit the old launch, observer, or replacement-planning evidence.
