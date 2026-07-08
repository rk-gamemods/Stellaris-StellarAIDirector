# Stellaris Codex Modding Packet

Target baseline: Stellaris PC 4.4.4 stable.

This packet is designed for implementation agents working on local mods and heavy playsets where runtime observer games may not be safe by default. It prioritizes static validation, source inspection, load-order evidence, provenance, and careful scope/AI-layer decisions.

Start with:
1. `stellaris_modding_quick_reference.md`
2. `folder_surface_matrix.csv`
3. `scope_atlas.md`
4. `ai_modding_reference.md`
5. `validation_checklists.md`
6. `stellaris_modding_guide.md`

Limitations:
- Public sources and CWTools schema were used where possible.
- Exact 4.4.4 vanilla source and active Workshop mod files must be inspected locally.
- Version-sensitive or uncertain items are tracked in `open_questions.md`.
