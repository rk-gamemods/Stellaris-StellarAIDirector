You are helping create a downloadable skill-authoring packet for Codex.

Reasoning tier: regular/high-intelligence WebChatGPT is acceptable; Pro/deep-research mode is preferred if available.

Downloadable files required: produce a downloadable zip file. Do not make the final deliverable chat-only.

## Task

Create handcrafted Codex `SKILL.md` files for the Stellaris modding roadmap in the attached context packet.

The priority is baseline/core Stellaris modding skills first. Do not spend effort on mod-specific compatibility rabbit holes until the core roadmap is done.

The user cares about making our own Stellaris modding and AI modding workflow strong and standalone. Assume external AI mods such as Stellar AI may be removed later. Do not center the work on fragile third-party mod compatibility unless a roadmap row itself is explicitly a compatibility skill and the core categories have already been handled.

## Context Packet

Read the attached packet before writing anything. It contains:

- repository rules and local environment context;
- roadmap table, catalog, build order, and ledgers;
- proposed skill specs grouped by category;
- Stellaris modding guide and validation workflow;
- current local Stellar AI Director project context as an example of our own mod surface;
- skill-creator instructions for valid Codex skill shape.

## Hard Priority Rule

Work in this order:

1. Core baseline categories first:
   - `00_foundation`
   - `01_schema_and_research`
   - `02_script_surfaces`
   - `03_ai_economy_planets`
   - `04_gameplay_domains`
   - `05_ships_war_starbases`
   - `06_megastructures`
   - `07_ui_localization_assets`
   - `08_validation_diagnostics`
   - `10_packaging_release`
2. Defer `09_compatibility` mod-specific skills until the core categories above are complete, except for any compatibility skill that is needed only as a brief cross-reference.
3. Do not author broad compatibility essays. Skills must be reusable workflow instructions for baseline Stellaris modding.

## Skill Quality Contract

For every skill you author, create a directory named exactly as the `skill_id`, containing:

- `SKILL.md`
- `agents/openai.yaml`

Each `SKILL.md` must be handcrafted, specific, and useful. It must include:

- YAML frontmatter with `name` and an actionable `description` that states when to use the skill;
- primary job;
- do-not-use cases;
- required inputs;
- optional inputs;
- source-of-truth order;
- workflow steps;
- validation expectations;
- final output contract;
- related skills/resources;
- uncertainty and escalation guidance.

Do not output placeholders, TODOs, generic filler, or generated-template prose.
Do not invent Stellaris triggers, effects, folders, scopes, or loader behavior. Where exact mechanics are uncertain, write how Codex should verify them.
Do not require launching Stellaris or running observer simulations by default. Runtime work requires explicit user approval.
Keep the skills narrow and composable.

## Output Files To Produce

Create a downloadable zip with:

1. `README.md`
   - What you produced.
   - How to import the files back into `C:\Users\Admin\.agents\skills`.
   - Which roadmap rows are covered.

2. `skill_authoring_manifest.csv`
   - Columns: `skill_id`, `category`, `priority`, `status`, `output_path`, `source_spec_used`, `notes`.

3. `core_priority_order.md`
   - The recommended order for finishing all baseline/core skills.
   - Explain which rows are deferred because they are third-party compatibility.

4. `skills/<skill_id>/SKILL.md`
   - One handcrafted skill per completed roadmap row.

5. `skills/<skill_id>/agents/openai.yaml`
   - UI metadata for each completed skill.

6. `remaining_work.md`
   - Rows not completed in the zip, why they remain, and the next batch order.

## Scope For This Run

If you can complete all baseline/core skills in one zip, do that.

If output size is too large, complete the largest coherent first batch from the core priority order, starting at the first incomplete baseline/core row. Do not switch to compatibility rows merely because they are easier.

The first batch should prioritize foundation/schema/script/validation skills over third-party mod compatibility. Include enough skills to be meaningfully useful, but do not lower quality to maximize count.

## Quality Review Before Final

Before producing the zip, self-check:

- no placeholder text remains;
- every skill has a concrete trigger and non-trigger;
- every skill is baseline/core focused unless explicitly marked deferred;
- no third-party compatibility rabbit hole dominates the output;
- every skill gives Codex a validation path;
- every skill names related skills for routing without duplicating all global rules.

## Codex Handoff

The user will download your zip and provide it back to Codex. Make the files complete enough that Codex can copy them into `C:\Users\Admin\.agents\skills`, run skill validation, update the ledger, and continue from the manifest.
