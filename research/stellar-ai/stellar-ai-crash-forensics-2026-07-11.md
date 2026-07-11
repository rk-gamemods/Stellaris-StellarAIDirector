# Stellar AI crash forensics — 2026-07-11 09:41 EDT

## Investigation boundary

- Game: Stellaris 4.4.4, modified 116-mod stack reported by `meta.yml`.
- Crash folder: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\crashes\stellaris_20260711_094142`.
- Exception time: 2026-07-11 09:41:43 EDT.
- Latest pre-crash save: `autosave_2239.01.01.sav`, 2,318,898 bytes, written 6.572 seconds before the exception.
- Fresh runtime cutoffs: copied crash `error.log` ends at 09:41:40; live `game.log` ends at 09:41:41. Startup-only families were excluded from the five-minute comparison below.
- No Stellaris process, observer run, or save mutation was started during this investigation.

## What the native crash evidence establishes

The crash is a `C0000005 (EXCEPTION_ACCESS_VIOLATION)` at `0x00007FF7E7E1CF13`. The complete 12-frame native stack is byte-for-byte identical after address normalization to crash `stellaris_20260706_220724`. Its first four frames also match `stellaris_20260710_183859`, whose frame 5 onward follows a different native path.

This proves a recurring native crash family. It does not identify the owning script or mod because the report has no symbols beyond misleading nearest-export labels such as `PHYSFS_swapSLE64`.

## Five-minute pre-crash comparison

| Crash | Entries | Severity | Families | Director matches |
| --- | ---: | --- | ---: | ---: |
| 2026-07-11 09:41 | 70 | 65 error, 5 info | 52 | 0 |
| 2026-07-10 18:38 | 185 | 153 error, 32 info | 138 | 0 |
| 2026-07-06 22:07 | 140 | 139 error, 1 info | 42 | 104 |

There are zero normalized log families common to all three five-minute windows. Consequently, no recurring script error currently explains the recurring native stack.

Fresh findings for the 2026-07-11 crash:

- Guilli's Planet Modifiers (`events/gpm_dig_site_events.txt`, Workshop 865040033) emitted 14 invalid `from.planet` context switches and 6 wrong-scope `set_site_progress_locked` calls between 09:39:10 and 09:39:57.
- Smarter Hyper Relays (`common/megastructures/zzz_shrimpai_hyper_relay_overwrite.txt`, Workshop 2815767345) emitted one wrong-scope `fleet_event` at 09:38:43.
- `events/galactic_features_events.txt` emitted two invalid `star` context switches, most recently at 09:41:04. The current vanilla file has the referenced `star = { ... }` at line 4140, but the active load-order winner was not proven from the available 2026-07-08 source-root dataset.
- Vanilla `events/nomads_events_1.txt` emitted an invalid `from` context at 09:41:39.
- At 09:41:40, two seconds before the exception, `generate_start_buildings_and_districts` failed to add `zone_research_unity` to city-district zone slot 1 while creating a Lost Colony parent from `federations_initializers.txt`. This is fresh runtime evidence, not a startup line. It is unique among the inspected crash windows and logged at info severity, so temporal adjacency makes it worth preserving but does not prove causation.
- `game.log` continued through 09:41:41 with first-contact and Grand Archive event selection. No Director event or file appears in the final five-minute window.

## Ranked causal assessment

1. **Recurring native engine/state-corruption path — medium causal confidence, high family confidence.** The identical full stack across 2026-07-06 and 2026-07-11, plus the same first four frames on 2026-07-10, is the strongest recurring evidence. The unsymbolized stack cannot distinguish an engine defect from invalid mod state reaching the same engine instruction.
2. **Invalid active-mod or vanilla script state feeding that native path — medium-low confidence.** The latest run has multiple fresh wrong-scope/context failures, especially GPM archaeology. However, none recur across all three matching crash windows, so no individual family is supported as the cause.
3. **Runtime country/colony initialization and zone-add failure — low confidence but high preservation priority.** It is the closest structured runtime anomaly, two seconds before the exception, and directly involves construction initialization. It occurred only once and the engine logged a handled failure.
4. **Autosave/write path — low confidence.** The latest crash followed an autosave by 6.572 seconds and the identical 2026-07-06 crash followed one by 4.607 seconds. Saves were being written roughly every ten seconds at accelerated game speed, so this proximity is expected for many random crash times and is not causal proof.
5. **Duplicate Stellaris instance — unsupported for this recurrence.** The current artifacts contain no already-running, mutex, or duplicate-process evidence. This recurrence means the earlier duplicate-instance A/B result was not a sufficient general explanation, although process multiplicity during this exact run cannot be reconstructed after the fact.

## Bounded recorder gap and correction

The prior recorder produced only `stellaris_exit_20260710_194446`, with zero-byte captured logs, then terminated. It therefore did not cover the 2026-07-11 run. It also recorded the globally newest crash folder without proving that folder belonged to the monitored session.

`tools/monitor_stellaris_crash_window.py` now:

- remains active across multiple Stellaris runs by default; `--once` retains explicit one-run behavior;
- associates a crash folder only when it was absent at session start and its modification time falls inside the session/exit freshness boundary;
- labels each packet `crash` or `normal_exit` rather than attaching stale crash metadata;
- records session sequence, attach-mid-session state, save age/freshness, and per-log captured bytes and lines;
- copies only small fresh `exception.txt`, `meta.yml`, and `system.log` evidence;
- adds no game log statements and retains the existing five-minute, 8 MiB-per-log, newest-three-snapshots bounds.

The monitor remains a manual external diagnostic. It does not launch Stellaris and is not part of automatic tests or the production mod.

## Validation

```text
python -m py_compile tools\monitor_stellaris_crash_window.py tools\tests\test_monitor_stellaris_crash_window.py
python -m unittest tools.tests.test_monitor_stellaris_crash_window
```

The focused suite covers time/byte trimming, save hashing, stale/known crash rejection, fresh crash selection, and the complete snapshot-to-metadata contract.

## Remaining evidence gap

The next recurrence needs one complete recorder packet. The decisive comparison fields are: exact native frames, truly new final-five-minute log families, fresh crash-folder association, save age/hash, and whether the same runtime object/event family appears again. A symbolic root cause still requires Paradox symbols or a controlled mod-stack reduction/reproduction; neither is available from the current minidump alone.
