-- Deterministic production bootstrap vocabulary for SKB2.
-- Derived from the validated revision-2 design, with 4.4.4 as the sole primary target.
PRAGMA foreign_keys=ON;
BEGIN IMMEDIATE;
INSERT INTO schema_metadata(metadata_key,metadata_value,description) VALUES ('seed_profile','production_bootstrap_2026-07-10','Controlled vocabulary only; no representative claims or demo fixtures.');
INSERT INTO actor(actor_id,actor_key,display_name,actor_type,external_identifier,notes) VALUES
  (1,'human:mod-owner','Mod owner','human',NULL,'Primary local maintainer.'),
  (2,'ai:codex','Codex','ai_agent','codex','Supervised Codex agent.'),
  (3,'tool:repo-validator','Repository validator','tool','tools/validate_stellar_ai_director_patch.py','Deterministic project validator.'),
  (4,'system:knowledge-base','Knowledge-base system','system',NULL,'Database-maintained records.'),
  (5,'tool:stellaris-kb','Stellaris knowledge-base CLI','tool','tools/stellaris_kb.py','Deterministic catalog, ingestion, query, and maintenance CLI.');
INSERT INTO change_set(change_set_id,change_set_key,title,purpose,actor_id,state,opened_at,committed_at,repository_commit,transaction_note) VALUES (1,'bootstrap:production-v3','Production SKB2 bootstrap','Install controlled vocabularies and exact version axes without representative claims.',5,'committed','2026-07-10T00:00:00Z','2026-07-10T00:00:00Z',NULL,'Foundational production bootstrap.');
INSERT INTO lifecycle_state(lifecycle_state_id,state_code,state_name,is_active,description) VALUES
  (1,'active','Active',1,'Current and available for normal use.'),
  (2,'draft','Draft',1,'Not yet accepted as current project knowledge.'),
  (3,'retired','Retired',0,'Preserved for history but no longer current.');
INSERT INTO confidence_level(confidence_level_id,confidence_code,confidence_name,rank_value,description) VALUES
  (1,'unknown','Unknown',0,'No defensible confidence assigned.'),
  (2,'low','Low',25,'Tentative; material gaps remain.'),
  (3,'medium','Medium',50,'Plausible and partly supported.'),
  (4,'high','High',75,'Strongly supported with limited residual uncertainty.'),
  (5,'very_high','Very high',95,'Multiple direct, reproducible sources or an authoritative direct source.');
INSERT INTO assessment_state(assessment_state_id,state_code,state_name,rank_value,is_usable_as_fact,description) VALUES
  (1,'verified','Verified',100,1,'Directly supported for the stated version span.'),
  (2,'inferred','Inferred',70,1,'Reasoned from evidence but not directly demonstrated.'),
  (3,'uncertain','Uncertain',40,0,'Material uncertainty remains.'),
  (4,'contradicted','Contradicted',20,0,'Material evidence contradicts the statement.'),
  (5,'stale','Stale',30,0,'Previously useful but overdue or version-invalidated.'),
  (6,'unknown','Unknown',0,0,'No adequate evidence yet.'),
  (7,'not_applicable','Not applicable',100,0,'Does not apply to the stated version or context.');
INSERT INTO item_type(item_type_id,type_code,type_name,description) VALUES
  (1,'mechanic_family','Mechanic family','Broad family used to organize mechanics.'),
  (2,'mechanic','Mechanic','A coherent Stellaris behavior or modding concept.'),
  (3,'subsystem','Mod subsystem','A maintainable subsystem of the target mod.'),
  (4,'game_object','Game object','A vanilla, mod, generated, or external-mod definition.'),
  (5,'field','Object field','A named field on a class of scripted object.'),
  (6,'trigger','Trigger','Built-in or scripted condition surface.'),
  (7,'effect','Effect','Built-in or scripted action surface.'),
  (8,'scope','Scope','Script execution or object scope.'),
  (9,'modifier','Modifier','Named modifier surface.'),
  (10,'define','Define','Engine define exposed through data files.'),
  (11,'resource','Resource','Stellaris resource represented as a typed game object.'),
  (12,'technology','Technology','Stellaris technology represented as a typed game object.'),
  (13,'file','File or corpus path','A precise implementation or evidence path.'),
  (14,'tool','Tool','An existing authoritative or investigative tool.'),
  (15,'checklist','Checklist','A reusable change and validation plan.'),
  (16,'system','System or environment','A corpus, playset, runtime, or other environment.'),
  (17,'other','Other','A stable item not yet assigned a more specific type.'),
  (18,'mod','Mod package','Vanilla, project, Workshop, compatibility, utility, or reference mod identity.'),
  (19,'playset','Playset','Stable logical playset whose captured membership changes over time.'),
  (20,'analysis_model','Analysis model','Registered inventory, valuation, policy, diagnostic, comparison, coverage, or observer model.'),
  (21,'benefit_class','Benefit class','Controlled strategic-benefit taxonomy class used by modeling policy.'),
  (22,'dlc','DLC or expansion','Versioned DLC/content assumption attached to an execution context.'),
  (23,'strategic_route','Strategic route','Named AI strategy or progression route used across policy surfaces.'),
  (24,'setting','Game or test setting','Galaxy, launcher, observer, or experimental setting relevant to evidence applicability.');
INSERT INTO object_kind(object_kind_id,kind_code,kind_name,definition_folder,description) VALUES
  (1,'economic_plan','Economic plan','common/economic_plans','AI economic-plan definition.'),
  (2,'ai_budget','AI budget','common/ai_budget','AI resource-budget definition.'),
  (3,'country_type','Country type','common/country_types','Country-type definition and AI eligibility surface.'),
  (4,'personality','AI personality','common/personalities','Diplomacy and strategic personality definition.'),
  (5,'building','Building','common/buildings','Planet building definition.'),
  (6,'job','Job','common/pop_jobs','Pop job definition.'),
  (7,'resource','Resource','common/resources','Resource definition or stable resource key.'),
  (8,'technology','Technology','common/technology','Technology definition.'),
  (9,'policy','Policy','common/policies','Policy definition.'),
  (10,'war_goal','War goal','common/war_goals','War-goal definition.'),
  (11,'casus_belli','Casus belli','common/casus_belli','Casus-belli definition.'),
  (12,'district','District','common/districts','Planet, habitat, ring-world, or modded district definition.'),
  (13,'colony_type','Colony type','common/colony_types','Planet designation and AI specialization definition.'),
  (14,'ascension_perk','Ascension perk','common/ascension_perks','Ascension-perk definition and AI weighting.'),
  (15,'tradition','Tradition','common/traditions','Tradition-tree or tradition definition.'),
  (16,'megastructure','Megastructure','common/megastructures','Megastructure construction and upgrade definition.'),
  (17,'starbase_building','Starbase building','common/starbase_buildings','Starbase building definition.'),
  (18,'starbase_module','Starbase module','common/starbase_modules','Starbase module definition.'),
  (19,'component_template','Component template','common/component_templates','Ship or station component template.'),
  (20,'component_set','Component set','common/component_sets','Component-set metadata definition.'),
  (21,'component_tag','Component tag','common/component_tags','Component tag identifier.'),
  (22,'ship_behavior','Ship behavior','common/ship_behaviors','Combat or movement behavior definition.'),
  (23,'ship_size','Ship size','common/ship_sizes','Ship-size or section-bearing hull definition.'),
  (24,'scripted_modifier','Scripted modifier','common/scripted_modifiers','Reusable scripted modifier.'),
  (25,'edict','Edict','common/edicts','Edict definition.'),
  (26,'decision','Decision','common/decisions','Planet or country decision definition.'),
  (27,'federation_type','Federation type','common/federation_types','Federation type definition.'),
  (28,'bombardment_stance','Bombardment stance','common/bombardment_stances','Fleet bombardment stance definition.'),
  (29,'trait','Trait','common/traits','Species or leader trait definition.'),
  (30,'civic','Civic','common/governments/civics','Government civic definition.'),
  (31,'on_action','On action','common/on_actions','Engine hook registration.'),
  (32,'event','Event','events','Country, planet, ship, or other event definition.'),
  (33,'zone','Zone','common/zones','Planetary zone or build-out surface.'),
  (34,'inline_script','Inline script','common/inline_scripts','Reusable inline-script template.'),
  (35,'script_value','Script value','common/script_values','Reusable numeric expression.'),
  (36,'scripted_variable','Scripted variable','common/scripted_variables','Script-level variable constant.');
INSERT INTO script_symbol_kind(script_symbol_kind_id,kind_code,kind_name,description) VALUES
  (1,'trigger','Built-in trigger','Engine-exposed condition.'),
  (2,'effect','Built-in effect','Engine-exposed action.'),
  (3,'scripted_trigger','Scripted trigger','Reusable trigger implemented in script.'),
  (4,'scripted_effect','Scripted effect','Reusable effect implemented in script.'),
  (5,'modifier','Modifier','Named modifier identifier.'),
  (6,'define','Define','Named value in a defines surface.');
INSERT INTO claim_type(claim_type_id,type_code,type_name,description) VALUES
  (1,'behavior','Behavior','How a mechanic behaves.'),
  (2,'structure','Structure','What an object, field, or script surface contains.'),
  (3,'compatibility','Compatibility','Version, DLC, or mod-stack compatibility claim.'),
  (4,'process','Process','Required investigative or maintenance procedure.'),
  (5,'hypothesis','Hypothesis','Testable explanation not yet verified.'),
  (6,'negative','Negative finding','A verified absence, limitation, or lack of proof.');
INSERT INTO evidence_source_type(evidence_source_type_id,type_code,type_name,default_reliability_rank,authoritative_scope,is_primary_evidence,description) VALUES
  (1,'vanilla_files','Vanilla files',95,'Scripted definitions in the captured game version',1,'Exact local vanilla files.'),
  (2,'generated_docs','Generated Stellaris documentation',85,'Exposed triggers, effects, modifiers, and scopes',1,'Version-matched generated documentation.'),
  (3,'cwtools','CWTools',85,'Schema and static diagnostics',1,'CWTools schema and diagnostics.'),
  (4,'irony','Irony Mod Manager',90,'Active-playset conflicts, ordering, and merged winners',1,'Conflict and load-order evidence.'),
  (5,'repository','Project repository',90,'Current mod source and deterministic scripts',1,'Version-controlled project files.'),
  (6,'research_note','Research note',65,'Documented conclusions and investigation history',0,'Source-backed local notes.'),
  (7,'runtime_log','Runtime log',80,'Observed parser/runtime messages for a specific run',1,'Game and error logs.'),
  (8,'save','Save evidence',80,'Persisted state for a specific game date and playset',1,'Save-field evidence.'),
  (9,'experiment','Controlled experiment',90,'Specified setup and observed result',1,'Reproducible experiment result.'),
  (10,'git_history','Git history',85,'Repository change provenance',1,'Commit and diff evidence.'),
  (11,'web','Web source',55,'Externally published information',0,'Web evidence; local revalidation may still be required.'),
  (12,'tool_output','Repository tool output',85,'Deterministic output for the captured inputs',1,'Validator, audit, or report output.'),
  (13,'patch_notes','Patch notes',80,'Declared version changes',1,'Official or preserved patch-note source.'),
  (14,'generated_dataset','Generated structured dataset',88,'Deterministic generated records for captured inputs',1,'CSV/JSON/JSONL outputs remain authoritative for their own rows and schemas.'),
  (15,'playset_snapshot','Captured playset snapshot',90,'Membership, order, and captured integration state for one playset snapshot',1,'Structured active-playset or Irony export.'),
  (16,'source_snapshot','Captured mod/source root',90,'Exact files present in a captured vanilla, Workshop, or project source root',1,'Path-preserving source snapshot or live root identity.'),
  (17,'runtime_observation','User/runtime observation',65,'Human-observed behavior correlated to a named run or save',0,'Observation must remain distinct from fields directly serialized or logged.');
INSERT INTO locator_type(locator_type_id,type_code,type_name,description) VALUES
  (1,'file_lines','File line range','Path and line range.'),
  (2,'object_key','Object key','Object identifier within a source file or corpus.'),
  (3,'symbol','Symbol','Trigger, effect, modifier, define, or code symbol.'),
  (4,'dataset_record','Dataset record','Dataset name plus stable record key.'),
  (5,'command_output','Command output','Command and output region.'),
  (6,'log_range','Log range','Timestamped or line-bounded runtime log evidence.'),
  (7,'save_field','Save field','Save path and field/key locator.'),
  (8,'commit','Git commit','Commit SHA, path, and optional diff anchor.'),
  (9,'url_section','URL section','URL plus heading or section.'),
  (10,'note_section','Note section','Named section in a research or design note.'),
  (11,'dataset_cell','Dataset row/column','Dataset schema plus stable record key, optional row number, and column.'),
  (12,'json_path','JSON path','Artifact plus JSONPath-like path into a structured document.'),
  (13,'archive_member','Archive member','Archive artifact plus member path and optional byte range.'),
  (14,'file_hash','File hash identity','Cryptographic identity, size, and external retrieval path.'),
  (15,'playset_position','Playset load position','Captured playset member and load-order position.'),
  (16,'validation_finding','Validation finding','Run-specific finding key and result location.');
INSERT INTO evidence_stance(evidence_stance_id,stance_code,stance_name,description) VALUES
  (1,'supports','Supports','Evidence tends to support the claim or relation.'),
  (2,'contradicts','Contradicts','Evidence tends to contradict it.'),
  (3,'qualifies','Qualifies','Evidence narrows, conditions, or limits it.'),
  (4,'context','Context only','Relevant context without directional support.');
INSERT INTO risk_level(risk_level_id,risk_code,risk_name,rank_value,description) VALUES
  (1,'low','Low',20,'Localized review is normally sufficient.'),
  (2,'medium','Medium',50,'Several connected surfaces should be reviewed.'),
  (3,'high','High',75,'Cross-system or compatibility consequences are likely.'),
  (4,'critical','Critical',95,'Failure can invalidate broad behavior or prevent loading.');
INSERT INTO relation_type(relation_type_id,type_code,type_name,inverse_name,description,impact_propagation_mode,is_transitive_hint) VALUES
  (1,'part_of','is part of','contains','Child belongs to a broader mechanic, family, or subsystem.','both',1),
  (2,'field_of','is a field of','has field','Field belongs to an object or object class.','both',1),
  (3,'implements','implements','is implemented by','Definition or object implements a mechanic.','both',1),
  (4,'implemented_in','is implemented in','implements item','Mechanic or object is implemented in a file.','both',1),
  (5,'depends_on','depends on','is dependency of','Source requires target; target changes propagate back to source.','reverse',1),
  (6,'references','references','is referenced by','Source names or calls target; target changes propagate back to source.','reverse',1),
  (7,'controls','controls or influences','is controlled by','Source directly influences target behavior or demand.','forward',1),
  (8,'interacts_with','interacts with','interacts with','Bidirectional operational or compatibility interaction.','both',1),
  (9,'uses_scope','uses scope','scope used by','Symbol or mechanic is valid in or evaluates a scope.','reverse',0),
  (10,'validated_by','is validated by','validates','Investigation route; not an impact dependency.','none',0),
  (11,'supersedes','supersedes','is superseded by','Historical replacement relation.','none',0),
  (12,'compatible_with','has compatibility concern with','has compatibility concern with','Mutual compatibility relationship.','both',1),
  (13,'produced_by','is produced by','produces','Source output is produced by target; producer changes affect output.','reverse',1),
  (14,'overrides','overrides','is overridden by','One definition intentionally supersedes another for the same loadable object.','both',1),
  (15,'gated_by','is gated by','gates','Availability or use of the source depends on the target prerequisite or condition.','reverse',1),
  (16,'unlocks','unlocks','is unlocked by','Source unlocks access to target.','forward',1),
  (17,'consumes','consumes','is consumed by','Source consumes target resources or capacity; changes can affect both supply and demand review.','both',1),
  (18,'generated_from','is generated from','generates','Generated model or artifact derives from target inputs.','reverse',1),
  (19,'evaluated_by','is evaluated by','evaluates','Investigation or validation route without implying gameplay impact.','none',0),
  (20,'feeds_model','feeds model','is fed by','Source evidence or dataset contributes inputs to the target model.','forward',1),
  (21,'resolves_to','resolves to','is resolution of','Context-specific resolution relationship; not a gameplay impact edge.','none',0);
INSERT INTO change_kind(change_kind_id,kind_code,kind_name,description) VALUES
  (1,'added','Added','New surface appeared.'),
  (2,'removed','Removed','Surface was removed.'),
  (3,'modified','Modified','Meaning, fields, or behavior changed.'),
  (4,'renamed','Renamed','Identifier changed.'),
  (5,'behavioral','Behavioral','Runtime behavior changed without a simple structural classification.'),
  (6,'unknown','Unknown','Change is observed but not yet classified.');
INSERT INTO change_type(change_type_id,type_code,type_name,description) VALUES
  (1,'field_change','Field change','Change a field value or expression.'),
  (2,'object_change','Object change','Add, remove, or modify a scripted object.'),
  (3,'mechanic_change','Mechanic change','Change a mechanic across multiple surfaces.'),
  (4,'subsystem_change','Subsystem change','Change a complete mod subsystem.'),
  (5,'version_port','Version port','Port or revalidate against a new Stellaris version.');
INSERT INTO investigation_task_type(investigation_task_type_id,task_code,task_name,description) VALUES
  (1,'locate_definition','Locate definition','Retrieve exact object or field definitions.'),
  (2,'schema_validate','Schema validation','Check syntax, type, scope, and allowed fields.'),
  (3,'conflict_analysis','Conflict analysis','Determine active winner and load-order interactions.'),
  (4,'source_diff','Source diff','Compare files or symbols between versions.'),
  (5,'static_validate','Static validation','Run deterministic repository validation.'),
  (6,'runtime_log_check','Runtime log check','Inspect game/error logs for the target behavior.'),
  (7,'save_inspection','Save inspection','Inspect persisted state for a specified run.'),
  (8,'controlled_experiment','Controlled experiment','Run a bounded comparison to resolve a hypothesis.'),
  (9,'impact_review','Impact review','Traverse dependencies and review affected items.'),
  (10,'documentation_lookup','Documentation lookup','Retrieve generated or narrative documentation.'),
  (11,'history_review','History review','Inspect Git changes and prior decisions.'),
  (12,'dataset_inspection','Dataset inspection','Retrieve rows, columns, aggregates, and schema from an authoritative external dataset.'),
  (13,'model_revalidation','Model revalidation','Regenerate a registered model and compare counts, schemas, policies, and issues.'),
  (14,'playset_resolution','Playset object resolution','Resolve the winning definition and conflict set for a captured playset.'),
  (15,'observer_analysis','Observer/save analysis','Analyze a named observer run, save set, or log set without conflating state with causation.'),
  (16,'schema_drift_review','Dataset schema-drift review','Compare registered versions of an external dataset schema and update mappings.');
INSERT INTO game_version(game_version_id,version_label,version_order,major,minor,patch,codename,build_id,release_channel,released_on,is_primary_target,notes,created_in_change_set_id) VALUES
  (1,'4.4.4',40404,4,4,4,'Pegasus','5505','stable',NULL,1,'Primary operating target verified from local launcher-settings.json: Pegasus v4.4.4 (5505).',1),
  (2,'4.4.5',40405,4,4,5,'Pegasus',NULL,'stable',NULL,0,'Comparative/historical target; not the current operating baseline.',1),
  (3,'4.5-beta',40500,4,5,NULL,NULL,NULL,'beta',NULL,0,'Separate compatibility and porting branch.',1);
INSERT INTO version_span(version_span_id,span_code,span_name,min_version_id,max_version_id,boundary_note,created_in_change_set_id) VALUES
  (1,'all','All catalogued versions',NULL,NULL,'Open-ended catalog span.',1),
  (2,'v4.4.4','Current Stellaris 4.4.4 target',1,1,'Exact current operating version verified locally.',1),
  (3,'v4.4.5','Stellaris 4.4.5 only',2,2,'Comparative historical version.',1),
  (4,'v4.4.x','Stellaris 4.4.4 through 4.4.5',1,2,'Known 4.4 project versions.',1),
  (5,'v4.5-beta','Stellaris 4.5 beta only',3,3,'Separate porting target.',1),
  (6,'v4.4.5-plus','Stellaris 4.4.5 and later catalogued versions',2,NULL,'Open-ended comparative span.',1),
  (7,'v4.4.4-through-v4.5-beta','All three representative versions',1,3,'Comparison span.',1);
COMMIT;
