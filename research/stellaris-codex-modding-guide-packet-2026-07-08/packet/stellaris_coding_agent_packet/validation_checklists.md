# Stellaris 4.4.x Validation and Debugging Checklists

Target: Stellaris PC 4.4.4 stable. Public-source access date: 2026-07-08.

## Evidence hierarchy

1. Current generated files.
2. Active load order and resolved source folders.
3. Local vanilla 4.4.4 files.
4. Active parent mod files.
5. CWTools diagnostics.
6. Runtime logs/saves/tests, if allowed.
7. Public docs.
8. Community reports.
9. Roadmaps/notes/chat memory.

Only 1-6 support implementation claims.

## Static validation checklist

### Descriptor and layout

- [ ] `descriptor.mod` exists.
- [ ] external `.mod` path/archive file exists if needed.
- [ ] `supported_version` intentionally targets `4.4.*`.
- [ ] dependencies are intent only; active load order captured separately.
- [ ] no fabricated `remote_file_id`.
- [ ] folder structure mirrors vanilla.
- [ ] no misspelled folders such as `commons`, `event`, `localization`.

### PDXScript

- [ ] braces balance.
- [ ] quotes close.
- [ ] inline blocks formatted for review.
- [ ] no YAML loc syntax in `.txt`.
- [ ] no PDXScript braces in `.yml`.
- [ ] `always = no` only in trigger-compatible blocks.

### Object IDs and overrides

- [ ] new IDs mod-prefixed.
- [ ] same-ID overrides are full objects.
- [ ] provenance comments on full overrides.
- [ ] duplicate-ID matrix generated.
- [ ] winning parent source identified.
- [ ] generated mod loads after parent.

### Scope

- [ ] current scope identified for each edited block.
- [ ] country checks in planet scope use `owner`.
- [ ] country checks in starbase definition scope use `from` where confirmed.
- [ ] country checks in megastructure `ai_weight` use `from`.
- [ ] event ROOT/FROM chains documented.
- [ ] CWTools scope diagnostics reviewed.

### AI

- [ ] folder supports `ai_weight` before adding it.
- [ ] weights moderate; no broad `factor = 0` over-gating.
- [ ] buildings/districts/zones have production/resource signals if construction expected.
- [ ] economic plans/budgets inspected when behavior depends on major resources.
- [ ] parent AI mod checked as winning source.
- [ ] defines avoided unless necessary and source-proofed.

### References

- [ ] localisation keys exist.
- [ ] icons/sprites/entities exist.
- [ ] referenced techs, buildings, districts, zones, jobs, starbases, megastructures, components, sections, resources exist.
- [ ] DLC gates preserved.
- [ ] event namespace/IDs unique.
- [ ] on_actions not patched without local proof.

## Suggested audit commands

```bash
rg -n "^\s*<object_id>\s*=" <vanilla>/common <mods>/*/common <generated>/common
rg -n "ai_weight|ai_resource_production|economic_plan|ai_budget|ai_planet_specialization" <generated>
rg -n "has_technology|is_ai|is_at_war|has_valid_civic|has_authority" <generated>/common
rg -n "host_has_dlc|has_dlc" <generated>
rg -n "OVERRIDE PROVENANCE|Parent source|source hash" <generated>
rg -n "^\s*<loc_key>:" <generated>/localisation
```

## Minimal Python audit skeleton

```python
from pathlib import Path
import re, hashlib

TOP = re.compile(r'^\s*([A-Za-z0-9_.:-]+)\s*=\s*\{')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def scan_top_ids(root, rel_folder):
    out = []
    for p in (Path(root) / rel_folder).glob('**/*.txt'):
        for i, line in enumerate(p.read_text(errors='ignore').splitlines(), 1):
            m = TOP.match(line)
            if m:
                out.append((m.group(1), str(p), i, sha(p)))
    return out
```

This is only triage; a real parser should track brace depth and folder schema.

## CWTools workflow

Public CWTools docs say it validates syntax, localisation, trigger/effect/modifier existence, scope context, weights/AI chance, sprites, and multi-root mod workspaces.

1. Open generated mod folder in VS Code.
2. Select vanilla Stellaris folder.
3. Add parent mod folders as multi-root workspace in active order when feasible.
4. Wait for scan.
5. Export/screenshot diagnostics.
6. Fix or explicitly justify waivers.

## Logs

Public modding docs mention logs and crash folders under the Stellaris user data directory, plus launch parameters such as `-script_debug`, `-debug_mode`, `-debugtooltip`, `-logprefix`, `-logpostfix`, and `-logall`.

Typical Windows paths:

```text
%USERPROFILE%\Documents\Paradox Interactive\Stellaris\logs\
%USERPROFILE%\Documents\Paradox Interactive\Stellaris\crashes\
```

| Log | Use |
|---|---|
| `error.log` | parser errors, wrong scopes, missing refs, unsupported triggers/effects, loc/modifier warnings |
| `game.log` | runtime messages and scripted `log =` output |
| `setup.log` | setup/loading information |
| `system.log` | environment/system details |
| `crashes/` | crash dumps/logs when error.log is insufficient |
| launcher logs | playset/descriptor/load problems; path version-sensitive |

## Error triage

| Error | Risk | Response |
|---|---:|---|
| unknown trigger/effect/modifier | High | fix name/version/scope |
| wrong scope | High | add correct wrapper |
| unresolved object reference | High | add/gate/remove reference |
| missing tech tier/category | High | fix before launch |
| GUI parse/widget error | High | source-proof and runtime UI proof |
| missing localisation | Medium | fix |
| missing icon/sprite | Medium-high | fix |
| duplicate object ID | Medium-high | intentional only with provenance |
| supported_version warning | Low by itself | not proof of script failure |

## Runtime boundaries

Static validation can prove structure and references. It cannot prove AI behavior. If runtime is allowed:

- launch to main menu and inspect logs;
- start tiny galaxy only if explicitly allowed;
- no long observer run by default;
- for AI proof, capture settings, seed, logs/saves, metrics, and baseline comparison.

## Red flags

Reject or escalate patches that:

- edit diplomacy/species rights/ship sizes/components/sections/personalities without exact proof;
- overwrite huge parent files for one small weight;
- add unsupported `ai_weight`;
- put country triggers in object scopes directly;
- drop DLC gates;
- miss localisation;
- claim runtime behavior from static validation;
- revert current user intent due to stale roadmap.
