# Best practices, tools, resources, and maintenance

## Baseline toolchain

| Tool | Use |
|---|---|
| VS Code | Project editor. |
| CWTools | PDXScript syntax validation, autocomplete, errors, missing localisation, formatting. `[S007] [S013]` |
| Paradox Syntax Highlighting | Readability. `[S007]` |
| Git | Version control and safe rollback. `[S007] [S013]` |
| Irony Mod Manager | Playset management and conflict solving. `[S011] [S012]` |
| WinMerge/Meld/Beyond Compare | Vanilla/mod diffing. |
| cwtools-action | CI validation for PDXScript. `[S014]` |
| 7-Zip | Archive and save-file inspection. `[S007]` |
| GIMP/Paint.net | Asset work. `[S007]` |

## Development workflow

1. Create mod through launcher or manually.
2. Initialize Git before writing content.
3. Add only one feature at a time.
4. Keep file and object names prefixed.
5. Run CWTools validation.
6. Launch with debug flags.
7. Check `error.log` after every test.
8. Test a clean playset.
9. Test intended compatibility playset.
10. Document every vanilla override.

## Professional repository practices

- `README.md` with install/load order.
- `CHANGELOG.md` with game-version support.
- `docs/compatibility.md` with conflict information.
- `docs/porting-4.5.md` if touching pops/factions/ethics.
- `test-notes/` with actual test saves and outcomes.
- Branches per game version.
- Release tags per game version.

## Mod maintenance checklist after Stellaris patch

- Read official patch notes and dev diary modding section.
- Diff vanilla folders your mod touches.
- Search removed/deprecated triggers/effects/modifiers.
- Regenerate or update CWTools vanilla cache if used.
- Run clean load test.
- Run target playset with Irony conflict scan.
- Review `error.log` and `game.log`.
- Test UI screens if any UI file copied from vanilla.
- Test saves started before patch only if claiming save compatibility.

## Community resources

- Stellaris Wiki modding tutorial and reference pages. `[S007] [S008] [S009] [S010]`
- Stellaris Modding Den Discord, referenced by the official tutorial. `[S007]`
- Irony Mod Manager documentation/community. `[S011] [S012]`
- CWTools documentation and GitHub repositories. `[S013] [S014]`
- Public maintained mods with source repositories.

## AI-assisted best practices

AI/Codex can be useful for:

- Summarizing patch notes into mod-specific TODOs.
- Turning repeated blocks into scripted triggers/effects.
- Generating localisation scaffolds.
- Comparing old and new vanilla files.
- Explaining error logs.
- Producing test matrices.

AI/Codex should not:

- Invent folders, triggers, or effects.
- Assume old 3.x economy/pop behavior.
- Assume load order is universally last-wins.
- Generate full vanilla-file replacements unless explicitly requested.
- Emit arbitrary console commands based on LLM reasoning.

Validation gates:

- Current vanilla files.
- CWTools errors.
- `trigger_docs` output.
- Irony conflict view.
- Runtime `error.log`.
