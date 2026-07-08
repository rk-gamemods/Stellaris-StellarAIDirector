# Load order, overrides, and conflict behavior

## Core rule

Do not model Stellaris as purely “last mod wins.”

The practical behavior is:

- Launcher/Irony playsets have an order.
- Later/lower mods often override earlier/top mods for LIOS-style content.
- Some folders/elements are FIOS-style, where the first served definition wins.
- File name collisions are not sufficient to identify real conflicts.
- Element-level conflict inspection is required for serious compatibility work.

Irony Mod Manager documentation says Irony understands game structures, FIOS/LIOS rules, and deterministic load-order management. A tool-author/community discussion explains that filename-only conflict checking can be misleading and that Irony detects conflicts by loading game elements, not just comparing filenames. `[S011] [S012]`

## Conflict matrix

| Conflict | Typical result | What Codex should do |
|---|---|---|
| Unique object IDs in unique files | Both load | Additive generation is safest. |
| Duplicate object key | One definition wins or errors | Stop and ask for intended override/merge; create patch. |
| Duplicate localisation key | Last/replace key generally wins | Use unique keys unless intentionally overriding; use `localisation/replace` for overrides. `[S008]` |
| Full copied vanilla file | High conflict risk | Diff against current vanilla; reduce to minimal override if possible. |
| `interface/*.gui` copied from vanilla | High UI breakage risk | Manual merge and runtime UI testing required. |
| GFX path collision | Later asset can shadow earlier | Use unique asset paths. |
| Same event ID/namespace | Broken behavior or wrong event fired | Use unique namespace and numeric IDs. |
| on_action edits | Add/replace behavior can be folder/key-specific | Inspect vanilla and resolve with patch. |
| `replace_path` | Destructive replacement of a folder path | Avoid except total conversions. |

## Practical playset ordering

General-purpose order for users:

1. Unofficial patches / base fixes.
2. Large overhauls / total conversions.
3. Gameplay systems and add-ons.
4. AI/economy/combat balance mods.
5. Submods.
6. Compatibility patches.
7. UI mods.
8. UI compatibility/final patches.

This is a heuristic, not a law. The actual rule is element-level conflict resolution.

## Compatibility patch design

A patch mod should contain only merged definitions and bridge code.

Recommended patch README fields:

```text
Patch name:
Target game version:
Required mods:
Required load order:
Patched files/keys:
Conflicts resolved:
Known unresolved conflicts:
Tested with:
```

## Codex implementation rules

When asked to generate mod code:

1. Prefer additive files and unique keys.
2. Do not copy whole vanilla files unless the user explicitly wants a full override.
3. If overriding, include a comment naming the vanilla key and target game version.
4. Generate a conflict note for every duplicate key.
5. If there is an upstream mod dependency, generate a separate compatibility patch, not a modification to the parent mod.
6. Recommend Irony conflict scan for any playset with UI/overhaul/economy mods.

## FIOS/LIOS caveat

The exact FIOS/LIOS classification is folder/content-type specific. The accessible source confirms that such rules exist and that Irony understands them, but this bundle does not include a full current folder-by-folder mapping. Validate exact behavior against:

- Current vanilla files.
- Irony Mod Manager conflict solver.
- CWTools full vanilla cache.
- Runtime logs.
