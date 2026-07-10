# Stellaris Knowledge Base

This directory contains the project-local, evidence-backed Stellaris knowledge base. The live database targets **Stellaris PC 4.4.4** and is operated through one deterministic Python command:

```powershell
python tools\stellaris_kb.py <command>
```

Do not write to the SQLite database with ad hoc SQL. Read-only SQL is available through the bounded `sql` command; all durable changes go through catalog refreshes, reviewed migrations, or versioned knowledge packets.

## What is live

- Live database: `knowledge-base/runtime/stellaris_knowledge_base.sqlite3`
- SQLite identity: `application_id=1397441074` (`SKB2`)
- Production schema: `user_version=4`
- Sole primary game target: `4.4.4`
- Runtime database, WAL companions, locks, and backups are generated local state and are Git-ignored.
- The checked-in design files preserve the exact attached design bundle. Production migrations harden that design and deliberately do not load the representative example data.

The database catalogs current Git-visible project files, relevant local 4.4.4 vanilla files, structured schemas, registered JDataMunch handles, normalized object-atlas rows, dependency edges, curated claims, evidence, and research questions. Large CSV/JSONL sources and Munch indexes remain authoritative in their original systems; the database stores their identity, fingerprint, schema, locator, and only selected durable conclusions.

## Daily use

Check the installation before relying on it:

```powershell
python tools\stellaris_kb.py status
python tools\stellaris_kb.py validate
python tools\stellaris_kb.py doctor
```

Discover and retrieve knowledge without writing:

```powershell
python tools\stellaris_kb.py search "war readiness assault armies"
python tools\stellaris_kb.py dossier "object:country_type:default" --version 4.4.4
python tools\stellaris_kb.py impact "object:country_type:default" --version 4.4.4 --max-depth 2 --limit 100
python tools\stellaris_kb.py impact "mechanic:ai-war-declaration-readiness" --version 4.4.4 --relation-type implements
python tools\stellaris_kb.py gaps --version 4.4.4
python tools\stellaris_kb.py sources "00_country_types.txt"
```

The `sql` command accepts a single bounded `SELECT` or `WITH` statement. It opens the database with URI `mode=ro` and `query_only=ON`; mutation and multi-statement input are rejected.

```powershell
python tools\stellaris_kb.py sql "SELECT version_label,is_primary_target FROM game_version ORDER BY version_label"
```

Impact results include canonical item paths, relation paths and IDs, evidence-locator paths, risk, review actions, and validation actions. Start at depth 1-2 and add repeatable `--relation-type` filters before increasing depth; broad compatibility graphs can become noisy.

## Codex skills

Four user-level skills are installed under `C:\Users\Admin\.codex\skills`:

- `stl-knowledge-base-query`: read-only dossiers, evidence, impact, gaps, and source retrieval.
- `stl-knowledge-base-update`: immutable evidence-packet dry-run and application.
- `stl-knowledge-base-maintenance`: installation, refresh, validation, locks, backup, migration, and restore.
- `stl-knowledge-base-gap-research`: prioritized 4.4.4 gap research with Munch routing and explicit runtime approval boundaries.

Each skill calls this CLI rather than constructing database writes. New Codex tasks discover the installed skills automatically.

## Refresh current sources

Use `refresh` after meaningful project, vanilla, or registered dataset changes:

```powershell
python tools\stellaris_kb.py refresh
```

The command performs source discovery and profiling before acquiring the writer lock. It then serializes the validated online backup and the write transaction, rechecks input fingerprints, records one auditable change set and ingest run, validates the database, and releases the lock. A second refresh with unchanged inputs is safe and should not create new artifact revisions.

Refresh does not turn every source row into a claim. Claims require a reviewed packet with exact evidence and explicit 4.4.4 applicability.

## Curated updates

Knowledge packets are immutable, canonical JSON inputs. Always dry-run before apply:

```powershell
python tools\stellaris_kb.py packet dry-run knowledge-base\manifests\initial_4_4_4_knowledge.json
python tools\stellaris_kb.py packet apply knowledge-base\manifests\initial_4_4_4_knowledge.json
```

Apply creates and validates an online backup while holding the same exclusive maintenance lock used for the packet transaction. Reapplying an identical packet is a no-op. Reusing a packet key with different content is a hard error. Evidence must resolve to a currently cataloged artifact or registered JDataMunch handle. See [PACKET_FORMAT.md](PACKET_FORMAT.md).

## Backup, checkpoint, and restore

Create a self-contained validated backup with SQLite's online backup API:

```powershell
python tools\stellaris_kb.py backup
python tools\stellaris_kb.py backup --output C:\safe\stellaris-kb.sqlite3
```

Do not copy the live main file while WAL mode is active. Do not delete `-wal` or `-shm` manually. For single-file transport, coordinate maintenance and run:

```powershell
python tools\stellaris_kb.py checkpoint
```

Restore is intentionally explicit and destructive to the selected database path. It verifies the input, takes a safety backup of the current database under the exclusive lock, checkpoints it, installs a temporary validated copy atomically, and validates the result:

```powershell
python tools\stellaris_kb.py restore --input C:\safe\stellaris-kb.sqlite3 --confirm-replace
```

Use `--database <path>` before the subcommand for disposable testing. Automatic backups for a non-live database are placed in a `backups` directory beside that database, keeping disposable tests isolated from production backups. Never test restore against the live database when a temporary destination is sufficient.

## Installation and migration

`install` creates a new database only when the destination does not exist. It builds and validates a temporary database before publishing it atomically:

```powershell
python tools\stellaris_kb.py --database C:\temp\stellaris-kb.sqlite3 install
```

`migrate` is for an eligible production v2 database only. It refuses the representative-example profile and takes a validated backup under the exclusive writer lock before applying the reviewed migration.

## Authority and version rules

Use evidence in this order:

1. The current user instruction and explicit target version.
2. Exact build-attested 4.4.4 vanilla or active-mod sources.
3. Generated artifacts and deterministic local tools.
4. JCodeMunch for code, JDocMunch for prose, and JDataMunch for row/column datasets.
5. CWTools, Irony, logs, saves, or a user-approved runtime experiment where the question requires them.
6. Official primary web sources when local evidence is insufficient.
7. Historical notes and labeled inference last.

Artifact names do not establish version or playset applicability. Evidence from 4.4.5, a beta, or an older playset cannot become verified 4.4.4 knowledge without explicit comparative proof. Static evidence must not be presented as runtime proof. Stellaris is never launched by these commands.

## Failure handling

- If `status` or `doctor` reports an active writer, inspect its recorded PID, acquisition time, and purpose. Coordination files persist as metadata after release; do not delete them based on pathname existence.
- If validation fails, stop writes, preserve the database and companions, and use the most recent validated backup for diagnosis.
- If Munch tool handles fail with `Transport closed`, repair or remount the active Codex thread before doing Munch-dependent work; do not silently replace the required tool path.
- If a packet cannot resolve evidence, refresh the catalog or correct the exact corpus/path/handle. Do not weaken the evidence requirement.
- If decisive evidence requires a game run, leave an `open_runtime` question unless the user explicitly approves launching Stellaris.

## File map

- `design/`: exact attached design, schema, and representative examples; examples are never production seed data.
- `migrations/`: reviewed production bootstrap and hardening migrations.
- `manifests/`: registered external dataset handles and reviewed knowledge packets.
- `runtime/`: ignored live SQLite state.
- `backups/`: ignored validated online backups.
- `tools/stellaris_knowledge_base/`: deterministic implementation.
- `tools/tests/test_stellaris_knowledge_base.py`: focused safety and behavior tests.
