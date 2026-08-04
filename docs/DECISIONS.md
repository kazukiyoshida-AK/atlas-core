# Atlas Core Decisions

## ACR-001 — Atlas Core Canonical Repository Strategy

```text
Decision ID: ACR-001
Title: Atlas Core Canonical Repository Strategy
Status: Approved
Decision date: 2026-08-02
Approved by: User
Selected option: Independent Atlas Core repository/package
Existing domain repositories: Unchanged
Existing database changes: Not authorized
Existing migration changes: Not authorized
Existing code reuse: Separate Entity-by-Entity Review required
```

## ACR-002 Revision 1 — Atlas Core Canonical Observation Model v0.1

```text
Decision ID: ACR-002
Revision: Revision 1
Title: Atlas Core Canonical Observation Model v0.1
Status: Approved
Decision date: 2026-08-02
Approved by: User
Canonical definition: Domain-independent atomic evidence-referenced fact record
Content model: Atomic normalized statement
Evidence: One or more Evidence references required
Provenance: Provenance reference required
Confidence: No single confidence score
Lifecycle: No mutable lifecycle status
Correction: Append-only new Observation and relation records
Deduplication: Outside Canonical Observation
Domain extension: Separate Domain Model
Existing Global Intelligence Observation: Global Intelligence Domain-specific Structured Measurement Model
Existing Model modification: Not authorized
Existing table modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Global Intelligence DB connection: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-003 — Atlas Core Canonical Evidence Model v0.1

```text
Decision ID: ACR-003
Title: Atlas Core Canonical Evidence Model v0.1
Status: Approved
Decision date: 2026-08-02
Approved by: User
Canonical definition: Domain-independent immutable reference to a captured evidence artifact or selected artifact range
Required source reference: Yes
Required provenance reference: Yes
Required artifact locator: Yes
Evidence kind: Extensible identifier
Raw payload embedding: Not allowed
Binary embedding: Not allowed
Content digest: Optional
Digest algorithm: Optional and paired with content digest
Mutable processing status: Not included
Mutable availability status: Not included
Single confidence score: Not included
Replacement: New Evidence plus append-only relation records
Deduplication: Outside Canonical Evidence
Storage design: Storage-neutral
Existing RawIngestionRecord: Global Intelligence Domain-specific Ingestion Record
Existing Repository modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-004 — Atlas Core Canonical Provenance Model v0.1

```text
Decision ID: ACR-004
Title: Atlas Core Canonical Provenance Model v0.1
Status: Approved
Decision date: 2026-08-03
Approved by: User
Canonical unit: One completed atomic activity occurrence
Required actor reference: Yes
Activity kind: Extensible identifier
Input references: Optional opaque references
Parent provenance references: Optional opaque references
Execution reference: Optional
Model reference: Optional
Prompt reference: Optional
Configuration reference: Optional
External run reference: Optional
Output references: Not included
Raw payload embedding: Not allowed
Observation content embedding: Not allowed
Prompt content embedding: Not allowed
Mutable workflow status: Not included
Failed attempts: Separate future model
Validation results: Not included
Single confidence score: Not included
Secret storage: Not allowed
Retry and rerun: New Provenance
Revision: New Provenance plus future append-only relation
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-005 Revision 1 — Atlas Core Canonical Source Model v0.1

```text
Decision ID: ACR-005
Revision: Revision 1
Title: Atlas Core Canonical Source Model v0.1
Status: Approved
Decision date: 2026-08-03
Approved by: User
Canonical unit: Specific identifiable originating identity directly attributed by Atlas as the origin of information captured by Evidence
Exact field count: 4
Required fields: 4
Optional fields: 0
Field order: source_id, source_kind, canonical_name, recorded_at
Source kind: Extensible opaque identifier
Canonical name: Primary label adopted by Atlas at record creation
Canonical name uniqueness: Not guaranteed
Canonical name currency: Not guaranteed
Canonical name authority: Not guaranteed
Normalization: Not allowed
Relationships: Deferred to future Source Relationship Model
Parent source reference: Not included
Established time: Not included
Locator and endpoint fields: Not included
Provider fields: Not included
Reliability and assessment fields: Not included
Mutable lifecycle status: Not included
Platform-specific identifiers: Not included
Personal contact information: Not included
Secret storage: Not allowed
Raw payload embedding: Not allowed
Evidence content embedding: Not allowed
Observation content embedding: Not allowed
Unknown and anonymous Sources: Complete non-empty Canonical records
Evidence relationship: Opaque source_ref to source_id
Reverse Evidence references: Not included
Entity resolution: Outside Core
Deduplication: Outside Core
Merge and split logic: Outside Core
Observation modification: Not authorized
Evidence modification: Not authorized
Provenance modification: Not authorized
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-006 — Atlas Core Canonical Actor Model v0.1

```text
Decision ID: ACR-006
Title: Atlas Core Canonical Actor Model v0.1
Status: Approved
Decision date: 2026-08-03
Approved by: User
Canonical unit: Stable Human or Non-human attribution identity to which Atlas attributes activity performance
Exact field count: 4
Required fields: 4
Optional fields: 0
Field order: actor_id, actor_kind, canonical_name, recorded_at
Actor kind: Extensible opaque identifier
Canonical name: Primary label adopted by Atlas at record creation
Canonical name uniqueness: Not guaranteed
Actor is distinct from: Source, Provenance, Tool, Model, Provider, Execution, Job, Account, Credential, Authorization Principal, and Role
Source and Actor boundary: Contextual role, not entity-type based; no cross-Concept identity assumption
Tool, Model, and Provider fields: Not included in Actor
Relationship fields: Not included; deferred to future Actor Relationship Model
Role fields: Not included; expressed via separate Activities, not intrinsic to Actor
Account and Credential fields: Not included
Authorization Principal fields: Not included
Lifecycle and status fields: Not included
Personal contact information: Not included
Secret storage: Not allowed
Unknown and anonymous Actors: Complete non-empty Canonical records
Provenance actor_ref cardinality: Unchanged, one opaque actor_ref per Provenance record
Multiple-Actor boundary: Distinct activities performed by distinct Actors use separate Provenance records
Known co-performers: Must not be arbitrarily discarded merely to fit one actor_ref
Multi-participant implementation: Not authorized
Observation modification: Not authorized
Evidence modification: Not authorized
Source modification: Not authorized
Provenance modification: Not authorized
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-007 Revision 1 — Atlas Core Canonical AI Model v0.1

```text
Decision ID: ACR-007
Revision: Revision 1
Title: Atlas Core Canonical AI Model v0.1
Status: Approved
Decision date: 2026-08-03
Approved by: User
Canonical unit: One specific identifiable Provider-neutral AI/ML model release, or one persistent separately attributable derivative admitted under the Identity Admission Rule
Exact field count: 4
Required fields: 4
Optional fields: 0
Field order: model_id, model_kind, canonical_name, recorded_at
Model kind: Extensible opaque identifier; initial Recommended Vocabulary documented, not enforced
Canonical name: Primary label adopted by Atlas at record creation
Canonical name uniqueness: Not guaranteed
Identity admission rule: Family-only and mutable-alias-only labels are insufficient for Known Model minting; Unknown Model records are valid and distinct from model_ref = None
Correction and invalid-record policy: No in-place mutation, no automatic merge, no ID reuse; old and corrected records remain unresolved within Core pending a future Resolution/Revision Concept (documented v0.1 Operational Limitation)
Duplicate-record risk: Known Operational Risk in the absence of a minting authority and Resolution mechanism; no automatic deduplication performed
Derivative policy: Persistent fine-tune, continued pretraining, instruction tuning, RLHF-derived release, distillation, or model merge may be a new Model identity; runtime-only LoRA, quantization alone, format conversion, endpoint/Provider/hosting change, and configuration change are not, by default
Lineage fields: Not included (no base_model_ref, parent_model_ref, derivation_kind)
Provider, Deployment, Endpoint, Tool, Prompt, Configuration, Capability, Evaluation, Lifecycle fields: Not included
Relationships: Deferred to future Model Family, Alias, Relationship, Resolution, Revision, and Artifact Concepts
Provenance.model_ref: Unchanged, str | None, opaque
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-008 — Atlas Core Canonical Execution Specification v0.1

```text
Decision ID: ACR-008
Title: Atlas Core Canonical Execution Specification v0.1
Status: Approved
Decision date: 2026-08-04
Approved by: User
Canonical unit: One revision-distinguishable, first-class, reusable implementation definition of the Tool, Adapter, Parser, Pipeline, Workflow, or Analysis Engine used to perform an activity
Exact field count: 4
Required fields: 4
Optional fields: 0
Field order: execution_specification_id, execution_kind, canonical_name, recorded_at
Execution kind: Extensible opaque identifier; initial Recommended Vocabulary documented, not enforced (tool, adapter, parser, pipeline, workflow, analyzer, engine, collector, classifier, client, service, function, unknown)
Canonical name: Primary label adopted by Atlas at record creation; must identify the specific implementation revision adopted, not merely a bare shared label
Canonical name uniqueness: Not guaranteed
Version or code_revision field: Not included; a materially distinct code revision is a new independent record, never a field update
Bare shared label sufficiency: A bare shared label (e.g. a label reused across several distinct implementations) is not sufficient for Known identity when it fails to distinguish the specific revision; Core does not enforce this at construction time
First-class invocation boundary: A standalone Function may be Known only when directly selected or invoked as the activity's executable unit, independently named, and reusable across occurrences; an internal helper method or function called only within a larger Tool/Adapter/Pipeline is not independently admitted
Known Execution Specification: Requires a stable, reusable, revision-distinguishable implementation definition, reused across multiple Provenance occurrences; not merely a Job/Run/Attempt identifier; not merely a deployment/container/runtime identifier; not automatically promoted from an existing Domain class name
Unknown Execution Specification: A complete, non-empty record is valid when code/Tool use is known but exact identity is unresolved, unavailable, withheld, or confidential
execution_ref = None: Distinct from an Unknown Execution Specification record; means no Execution Specification applies or Tool use was not recorded
Job, Attempt, Run, request, retry: Not included; occurrence-level, excluded from this Concept
Deployment, Runtime, Container, Provider fields: Not included
Configuration, AIModel, Actor fields: Not included; already separate Concepts/Provenance fields
Correction and invalid-record policy: No in-place mutation, no automatic merge, no ID reuse; old and corrected records remain unresolved within Core pending a future Resolution/Revision Concept (documented v0.1 Operational Limitation)
Duplicate-record risk: Known Operational Risk in the absence of a minting authority and Resolution mechanism; no automatic deduplication performed
Provenance.execution_ref: Unchanged, str | None, opaque
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-009 — Atlas Core Canonical Prompt Specification v0.1

```text
Decision ID: ACR-009
Title: Atlas Core Canonical Prompt Specification v0.1
Status: Approved
Decision date: 2026-08-04
Approved by: User
One-sentence definition: A Prompt Specification is the stable, reusable, revision-distinguishable instructional definition Atlas selected for an activity, separate from AIModel, ExecutionSpecification, Actor, Configuration, Rendered Prompt, retrieved context, user input, and conversation history
Canonical unit: One specific, named, revision-distinguishable, reusable instructional definition selected for reuse across activities
Exact field count: 4
Required fields: 4
Optional fields: 0
Defaults: 0
Field order: prompt_specification_id, prompt_kind, canonical_name, recorded_at
Prompt content in Core: NO
Content hash in Core: NO
Rendered Prompt in Core: NO
Prompt Artifact: Deferred, not designed or implemented in v0.1
Exact reproducibility: Not guaranteed by Core alone; documented v0.1 Operational Limitation (content cannot be reconstructed, content integrity cannot be verified, loss of external content is not repairable from canonical_name, until a future Prompt Artifact Concept exists)
prompt_kind classification axis: Structural architecture only
prompt_kind recommended vocabulary: instruction, message_template, message_bundle, unknown
prompt_kind excludes: message role (system, developer, user) and functional purpose (summarization, classification, routing, extraction, generation, analysis, evaluation); these are expressed via Provenance.activity_kind, ExecutionSpecification, or Domain policy, not prompt_kind
Canonical name: Primary label adopted by Atlas at record creation, identifying the specific Prompt revision, not merely the Prompt family; revision identifier carried inside canonical_name (e.g. "Article Summarization Prompt prompt-v1"), no separate version/revision field
Mutable alias as Known identity: Not permitted (production, latest, default, current alone are insufficient); not runtime-rejected, an admission-rule concern only
Known Prompt Specification: Requires stable reusable revision-distinguishable identity, explicit registration, reuse across multiple Provenance occurrences, immutable treatment; not automatically promoted from a source filename or constant name
Confidential Known Prompt: Withheld or confidential content alone does not force Unknown classification when identity is known; sanitized canonical_name permitted; no content stored regardless
Unknown Prompt Specification: A complete, non-empty record is valid when some Prompt use is known but identity itself is unresolved or unavailable
prompt_ref = None: Distinct from an Unknown Prompt Specification record; means no Prompt applies or Prompt use was not recorded
One-off manually entered Prompt: Not automatically minted as Known unless registered as reusable; occurrence content belongs to a future Rendered Prompt/Input Artifact
Dynamically generated Prompt: The generating Tool/Pipeline is an ExecutionSpecification, the generation occurrence is Provenance, the generated concrete output is a future Rendered Prompt/Artifact; not auto-minted per generated instance; only a registered stable generator skeleton may be Known
New-identity rule: Materially distinct instructional wording, role assignment, message order, few-shot examples, variable contract, embedded output-format/JSON-schema, safety instructions, or independently operated translations require a new record; AIModel-only, ExecutionSpecification-only, Configuration-only, retrieved-context-only, user-input-only, conversation-history-only, request/retry/run-only, payload-serialization-only, and comment-only changes do not; whitespace/punctuation/spelling/formatting-only changes require explicit manual admission judgment, never automated
Correction and invalid-record policy: No in-place mutation, no automatic merge, no ID reuse; old and corrected records remain unresolved within Core pending a future Resolution/Revision Concept (documented v0.1 Operational Limitation)
Duplicate-record risk: Known Operational Risk in the absence of a minting authority and Resolution mechanism; no automatic deduplication, semantic deduplication, or hash-based deduplication performed
Provenance.prompt_ref: Unchanged, str | None, opaque
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Provider integration: Not authorized
Prompt execution engine: Not authorized
Initial implementation: Pure Core Model only
```

