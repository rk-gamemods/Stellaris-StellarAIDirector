# Stellar AI Director Modeling Completion WebChatGPT Prompt

Use the uploaded StellarisMods context bundle as your source context. Search by the exact file, artifact, status, and entity names below. If a needed source file or large CSV is named in the bundle but not actually available as readable content, do not guess; record the exact missing file/content as required evidence.

Reasoning tier: Pro / deep research.

Role:
You are a Stellaris 4.4.x modding and data-modeling reviewer helping finish the Stellar AI Director modeling layer. Stellar AI Director is a self-contained Stellaris mod, not a patch mod.

Goal:
Eliminate the current remaining Stellar AI Director modeling blockers. The desired final state is zero unresolved blockers. The current 396 blocker rows are the starting inventory and work queue. They are not a target state, acceptance threshold, or acceptable final condition.

Current known blocker inventory:
- 396 total current blocker rows.
- 265 `benefit_formula_status` rows.
- 131 `unresolved_variable` rows.
- 0 `unknown_job` blockers.
- 0 `data_quality_flag` blockers.

Interpretation of the current inventory:
The counts above describe the problem to remove. They are included so you know the expected starting queue size and can detect missing row coverage. A successful result reduces those blockers to zero through source-backed deterministic resolution or classification. Zero blockers means every row has deterministic handling: safely scorable, explicitly not consumable, detected-only, zero-effect, inactive integration, source orphan, or still blocked with exact missing evidence. It does not mean inventing a positive numeric score for every row. If zero cannot be reached from the uploaded context, the remaining rows must be explicitly listed with exact missing evidence.

Primary context bundle files:
- `04_STELLAR_AI_DIRECTOR_CONTEXT.md`
- `06_DATASETS_AND_VALIDATION_REPORTS.md`
- `07_TOOLS_AND_VALIDATORS.md`
- `02_PROJECT_CONTROL_AND_GUIDANCE.md`
- `08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md`

Primary artifact names to find inside the context bundle:
- `MODELING_COMPLETION_LEDGER.md`
- `stellar-ai-director-build-plan-consumer-contract-2026-07-09.md`
- `stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv`
- `stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv`
- `stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv`
- `stellar-ai-director-research-capacity-buildings-2026-07-09.csv`
- `stellar-ai-director-research-capacity-development-2026-07-09.csv`
- `stellar-ai-director-research-capacity-jobs-2026-07-09.csv`
- `stellar-ai-director-build-plan-readiness-2026-07-09.csv`
- `stellar-ai-director-colony-role-targets-2026-07-09.csv`
- `build_stellar_ai_research_capacity_dataset.py`
- `stellar_ai_director_lib.py`
- `test_stellar_ai_director.py`

Important status and classification names:
- `benefit_formula_status`
- `unresolved_variable`
- `consumer_modeling_status`
- `blocked_unresolved_modeling`
- `benefit_formula_policy_required`
- `benefit_formula_mapping_required`
- `source_excluded_jobs`
- `inactive_external_acot_integration_modeled_zero_effect`
- `inactive_external_thaumstellaris_integration_modeled_zero_effect`
- `source_orphan_no_pop_job_definition_modeled_zero_effect`

Known already-classified inactive or orphan references:
- `job_brain_drone`
- `job_calculator`
- `job_giga_interstellar_researcher`
- `job_giga_interstellar_researcher_drone`
- `job_giga_interstellar_scavenger`
- `job_giga_interstellar_scavenger_drone`
- `job_tc_*` when gated by Thaumstellaris / `thaumstellaris_initialize`
- `job_acot_*` when gated by ACOT / `acot_giga_void_sphere`

Do not reopen those known references as unknown-job blockers unless you find direct contrary evidence in the uploaded context bundle.

Source-of-truth order:
1. Current task instructions in this prompt.
2. The uploaded context bundle files.
3. Current generated CSV artifacts inside the bundle.
4. Current generator and test code inside the bundle.
5. Inference only when no stronger source exists, and label it as inference.

Hard rules:
- Do not invent generic scores.
- Do not rename statuses or definitions to make unresolved data appear complete.
- Do not claim a row is safely scorable unless the uploaded context provides source-backed deterministic evidence.
- Do not force numeric scoring where the correct deterministic policy is detected-only, non-consumable, zero-effect, inactive integration, or source orphan.
- Do not treat the 396 current blocker rows as acceptable final output.
- Do not use "target", "goal", "complete", or "safe" language for the 396-row starting inventory.
- Do not claim full completion if any row remains unresolved without a deterministic classification.
- If the context bundle lacks readable evidence for a row, keep that row blocked and state the exact missing file, artifact, source object, row, or source content needed.

Task:
1. Use `stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv` as the main work queue.
2. For every `unresolved_variable` row, determine whether the variable can be resolved or source-classified from the uploaded context.
3. For every `benefit_formula_status` row, determine whether a deterministic formula, deterministic mapping policy, detected-only non-scoring policy, zero-effect classification, or exact missing-evidence blocker is justified.
4. Cross-check your decisions against the current consumer policy, benefit taxonomy, buildings, development, jobs, readiness, role-target, generator, and test artifacts listed above.
5. Produce implementation-ready outputs that Codex can use for the next corrective pass.
6. Do not implement code. Codex will implement after reviewing your returned files.

Context-bundle search guidance:
- Start with `MODELING_COMPLETION_LEDGER.md` and `stellar-ai-director-build-plan-consumer-contract-2026-07-09.md` for the current contract and known correction history.
- Use `stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv` for row coverage.
- Use the artifact names in `08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md` to locate whether related large CSVs or source files are actually readable in the uploaded bundle.
- Use generator/test names to find current implementation expectations and avoid recommending schema changes that contradict tests without saying which tests must change.

Allowed decisions for `unresolved_variable` rows:
- `resolved_literal_value`
- `resolved_source_local_variable`
- `resolved_global_variable`
- `source_backed_zero_effect`
- `inactive_external_integration_zero_effect`
- `source_orphan_zero_effect`
- `still_blocked_missing_evidence`

Allowed decisions for `benefit_formula_status` rows:
- `numeric_formula_defined`
- `detected_only_non_scoring_policy`
- `consumer_policy_mapping_defined`
- `source_backed_zero_effect`
- `still_blocked_missing_policy_or_evidence`

Output files required:
Do not answer only in chat. Produce downloadable files with these exact filenames.

1. `unresolved_variable_resolutions.csv`

Required columns:
`source_artifact,object_type,object_id,issue_key,source_mod,source_file,current_status,decision,resolved_value_or_policy,evidence,confidence,codex_action`

One row per current `unresolved_variable` blocker row.

2. `benefit_formula_policy_matrix.csv`

Required columns:
`benefit_class,object_type,object_id,source_mod,source_file,current_status,decision,formula_or_policy,evidence,confidence,codex_action`

One row per current `benefit_formula_status` blocker row.

3. `generator_change_plan.md`

Include:
- exact recommended changes for `build_stellar_ai_research_capacity_dataset.py`;
- exact recommended changes for `stellar_ai_director_lib.py`;
- exact recommended test changes for `test_stellar_ai_director.py`;
- any expected blocker-count changes after implementation;
- any row-count or schema changes expected in generated CSV artifacts.

4. `remaining_missing_evidence_or_human_decisions.md`

Include only items that truly require user decision or missing source evidence. Do not include rows that can be resolved from the uploaded context. For each item, identify the exact file, source object, row, policy choice, or source content that is missing.

5. `final_summary.md`

Include:
- how many current blockers can be eliminated;
- how many blockers, if any, must remain;
- why each remaining blocker cannot be resolved from the uploaded context, with exact missing evidence;
- whether the model can honestly be called complete;
- exact next Codex implementation steps.

Validation expectations:
- The sum of rows in `unresolved_variable_resolutions.csv` must equal the current count of `unresolved_variable` rows in the blocker CSV unless you explicitly explain why the context bundle contains a different current count.
- The sum of rows in `benefit_formula_policy_matrix.csv` must equal the current count of `benefit_formula_status` rows in the blocker CSV unless you explicitly explain why the context bundle contains a different current count.
- Every row must have a decision, evidence, confidence, and Codex action.
- Confidence values must be `high`, `medium`, or `low`.
- `still_blocked_*` decisions must include exact missing evidence, not generic uncertainty.
- The final summary must explicitly say whether the desired zero-blocker state is achieved, not merely whether the analysis is complete.

Success criteria:
- Best case: all 396 current blocker rows receive source-backed deterministic resolution or classification, and Codex can implement a zero-blocker corrective pass.
- Acceptable fallback: any row that cannot be resolved from the uploaded context remains explicitly blocked with exact missing evidence and a precise Codex/user follow-up.
- Failure: generic scoring, fake completion, vague uncertainty, missing row coverage, or treating the 396 current blockers as an acceptable final state.
