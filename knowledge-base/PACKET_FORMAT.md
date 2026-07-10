# Knowledge Packet Format

A knowledge packet is a reviewed JSON document applied by `python tools\stellaris_kb.py packet`. It turns already-cataloged evidence into version-scoped items, claims, assessments, questions, and relations without embedding raw source datasets in SQLite.

## Required envelope

```json
{
  "packet_version": 1,
  "packet_key": "unique-immutable-key",
  "target_version": "4.4.4",
  "title": "Human-readable title",
  "purpose": "Why this evidence belongs in the knowledge base.",
  "repository_commit": "optional Git SHA",
  "actor": {
    "key": "ai:codex",
    "display_name": "Codex",
    "type": "ai_agent"
  },
  "items": [],
  "evidence": [],
  "claims": [],
  "questions": [],
  "relations": []
}
```

`packet_key` identifies immutable packet content. Reapplication of the same canonical payload is a no-op; the same key with different content is rejected. `target_version` must be exactly `4.4.4` for this installation.

## Items

Items provide stable concepts for retrieval and graph edges:

```json
{
  "key": "subsystem:war-planning",
  "type": "subsystem",
  "display_name": "War planning",
  "summary": "Native AI readiness and declaration-planning surfaces."
}
```

Use an existing canonical key when the catalog has already created the item. New item types must exist in the production vocabulary.

## Evidence

Evidence must resolve to a current catalog artifact by `corpus` plus `relative_path`, or to a current external dataset handle by `dataset_handle`:

```json
{
  "key": "default-country-type-ai",
  "corpus": "vanilla",
  "relative_path": "common/country_types/00_country_types.txt",
  "locator_type": "script_object",
  "symbol_or_object_key": "default",
  "line_start": 1,
  "line_end": 80,
  "summary": "The exact 4.4.4 default country-type AI readiness block.",
  "retrieval_instructions": "Open the cataloged vanilla artifact and inspect the default ai block."
}
```

For structured data, set `use_dataset_schema` only when the resolved artifact has the intended registered schema. Include `record_set`, `record_key`, `row_number`, `column_name`, `json_path`, or `query_text` when they materially improve repeatable retrieval. An excerpt is context, not a replacement for the source.

## Claims and assessments

```json
{
  "key": "claim:war-readiness-default-gates-4.4.4",
  "type": "behavior",
  "primary_item": "object:country_type:default",
  "statement": "In Stellaris 4.4.4, the default country type requires at least half of desired naval size and at least six assault armies before ordinary war planning can proceed.",
  "context": "Pegasus 4.4.4 (5505), default country type.",
  "epistemic_note": "Static trigger evidence establishes the configured gates; runtime results are linked separately.",
  "state": "verified",
  "confidence": "high",
  "basis_summary": "Exact build-attested vanilla definition plus project analysis.",
  "evidence": [
    {
      "key": "default-country-type-ai",
      "stance": "supports",
      "directness": 5,
      "strength": 5,
      "interpretation": "Direct definition of both readiness thresholds."
    }
  ]
}
```

Claim keys and statements are immutable identities. A later packet may supersede the current assessment for the same claim/version, but changing the meaning requires a new claim key. Preserve contradictory evidence and classify uncertainty; do not rewrite history.

## Questions

```json
{
  "key": "question:merged-economic-plan-subplans-4.4.4",
  "primary_item": "subsystem:economic-planning",
  "question": "What is the final merged 4.4.4 economic-plan and nested-subplan graph for the current active 116-mod playset?",
  "uncertainty_reason": "Object-level winner rows do not prove nested merge semantics, and the previous playset snapshot is stale.",
  "status": "open",
  "evidence_mode": "static",
  "runtime_approval_required": false,
  "priority": 95,
  "next_action": "Reconstruct the merged nested plan graph from the current active source roots.",
  "evidence": ["economic-plan-atlas"]
}
```

`status` is workflow state: `open`, `investigating`, `blocked`, `resolved`, or `wont_fix`. `evidence_mode` is the required research route: `static`, `runtime`, `tooling`, or `mixed`. Runtime and mixed questions must set `runtime_approval_required` to `true`; this records that the database does not itself authorize launching Stellaris. Resolved questions should name a packet claim in `resolution_claim`.

## Relations

```json
{
  "key": "relation:default-country-type-controls-war-planning-4.4.4",
  "source": "object:country_type:default",
  "type": "controls",
  "target": "subsystem:war-planning",
  "confidence": "high",
  "risk": "high",
  "source_claim": "claim:war-readiness-default-gates-4.4.4",
  "rationale": "The default country-type AI block supplies readiness gates to ordinary AI empires.",
  "impact_explanation": "Changing these gates changes when otherwise eligible AI empires can enter war planning.",
  "review_action": "Review the final winning country-type definition and compatibility overrides.",
  "validation_action": "Run static validation and, only with approval, an observer comparison.",
  "evidence": ["default-country-type-ai"]
}
```

Relations are version-scoped and participate in bounded impact traversal. Use an existing relation type and keep review/validation actions operational.

## Safe workflow

1. Research and retrieve exact evidence before acquiring a writer lock.
2. Refresh the source catalog if required evidence is absent or stale.
3. Create or edit the packet with a new immutable `packet_key`.
4. Run `packet dry-run` and inspect resolved artifact IDs and counts.
5. Apply once. The CLI serializes backup and mutation, uses `BEGIN IMMEDIATE`, records a change set, and validates foreign keys.
6. Run `validate`, then rerun the relevant `dossier`, `impact`, and `gaps` queries.
7. Commit the packet and source changes when they are ready; never commit the runtime database or backups.
