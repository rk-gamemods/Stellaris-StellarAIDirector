# Stellar AI Director Corpus Status

Recorded 2026-07-04 21:06 America/New_York after refreshing the active Munch surfaces for the Stellar AI Director work.

## Active Playset Source Roots

The source snapshot manifest covers five required parent roots from the active Irony playset:

- Stellar AI (`3610149307`)
- Gigastructural Engineering & More (4.4) (`1121692237`)
- NSC3 (`683230077`)
- Extra Ship Components NEXT (`2648658105`)
- Starbase Extended 3.0 (`3250900527`)

Each row in `research/mod-source-snapshots/2026-07-04/snapshot-manifest.csv` maps the Steam Workshop source path to a stable local snapshot path. `descriptor-inventory.csv` records the matching descriptor names, versions, supported versions, remote file IDs, and snapshot paths.

## Indexed Corpus

- JDocMunch repo `local/StellarisMods-docs-2026-07-04` was rebuilt with embeddings disabled for `plans/`, root `README.md`, Director README/notes, and `research/stellar-ai/`. It indexed 31 files and 1132 sections. `verify_index` reported 0 drift, 0 missing, and 0 errors.
- JCodeMunch repo `local/StellarisMods-223b92bc` refreshed the `tools/` source index after the latest test/status-gate edits. It reported 57065 symbols, 2 changed files, 0 no-symbol files, and no unreadable/too-large/secret skips.
- JDataMunch indexed and validated `stellar_ai_snapshot_manifest`, `stellar_ai_descriptor_inventory`, `stellar_ai_pdx_object_inventory`, and `stellar_ai_ai_surface_inventory`.

## Inventory Coverage

- `snapshot-manifest.csv`: 5 rows, 10 columns, integrity ok.
- `descriptor-inventory.csv`: 5 rows, 7 columns, integrity ok.
- `pdx-object-inventory.csv`: 35991 rows, 8 columns, integrity ok.
- `ai-surface-inventory.csv`: 1696 rows, 26 columns, integrity ok.

The PDX object inventory includes the required P1 gameplay-heavy surfaces: `ai_budget`, `economic_plans`, `megastructures`, `technology`, `ascension_perks`, `traditions`, `starbase_modules`, `starbase_buildings`, `buildings`, `ship_sizes`, `component_templates`, `scripted_triggers`, `script_values`, `on_actions`, `country_event`, and `planet_event`-bearing files.

## Omissions And Follow-Up

No required parent source root is omitted from the 2026-07-04 snapshot set. JDocMunch section verification skipped empty heading byte ranges only; it reported no drift, missing sections, or errors. JCodeMunch reported one wrong-extension skip during `tools/` indexing, which is outside the Python source-symbol surface.

P1 is considered current for offline source/index evidence as of this recorded refresh. Future gameplay edits should rerun the snapshot inventory builders and refresh JDocMunch/JCodeMunch/JDataMunch before relying on old corpus evidence.
