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

## ACR-010 — Atlas Core Canonical Configuration Specification v0.1

```text
Decision ID: ACR-010
Title: Atlas Core Canonical Configuration Specification v0.1
Status: Approved
Decision date: 2026-08-04
Approved by: User
One-sentence definition: A Configuration Specification is the stable, reusable, revision-distinguishable identity of a definition of adjustable parameters Atlas selected for an activity, separate from AIModel, PromptSpecification, ExecutionSpecification, Actor, Deployment, Runtime, Provider, Secret, and Resolved Configuration
Canonical unit: One specific, named, revision-distinguishable, reusable definition of a set of adjustable parameters (a Configuration Profile) selected for reuse across activities
Exact field count: 4
Required fields: 4
Optional fields: 0
Defaults: 0
Field order: configuration_specification_id, configuration_kind, canonical_name, recorded_at
Configuration content in Core: NO
Resolved values in Core: NO
Content hash in Core: NO
Secrets/credentials in Core: NO
Configuration Artifact: Deferred, not designed or implemented in v0.1
Resolved Configuration: Deferred, not designed or implemented in v0.1
Exact reproducibility: Not guaranteed by Core alone; documented v0.1 Operational Limitation (parameter names/values, defaults, overrides, and inheritance cannot be reconstructed; effective behavior cannot be fully reproduced; configuration drift and content integrity cannot be verified; loss of external content is not repairable from canonical_name, until future Configuration Artifact and Resolved Configuration Concepts exist)
configuration_kind classification axis: Structural architecture only
configuration_kind recommended vocabulary: parameter_profile, settings_bundle, policy_profile, feature_flag_set, unknown
configuration_kind excludes: functional purpose (model_generation, routing, collection, analysis, publication, retry, timeout, scheduling) and source format/loading mechanism (environment, json, yaml, toml, command_line, env_file, settings_class); functional purpose is expressible via Provenance.activity_kind, ExecutionSpecification, or Domain-local policy instead
Canonical name: Primary label adopted by Atlas at record creation, identifying the specific registered Configuration revision, not merely the family; revision identifier carried inside canonical_name (e.g. "Summarizer Generation Parameters gen-params-v1"), no separate version/revision field
Mutable alias as Known identity: Not permitted (production, staging, default, current, latest alone are insufficient); not runtime-rejected, an admission-rule concern only
Specification-revision vs. runtime-override boundary: A reusable registered profile definition change requires a new Configuration Specification; an occurrence-only effective-value change (single request/run/attempt override, temporary environment/CLI/request-payload resolution, secret rotation, Deployment-only or Runtime-only change, source-format-only change, source-file-location-only change, comment/whitespace-only change with unchanged effective definition, or key/serialization-order-only change) does not; an occurrence override pattern later formally registered for reuse becomes a new Configuration Specification at the moment of registration
API endpoint/Deployment/Provider boundary: An endpoint selected or varied per registered Configuration profile is a Configuration content candidate (deferred to future Artifact, value never stored in Core); an endpoint fixed per process/service/environment/cluster/region is Deployment/Runtime, not Configuration; the Provider identity behind an endpoint is a separate, deferred Concept; no API URL, database URL, hostname, or region field exists on this Concept
Known Configuration Specification: Requires stable reusable revision-distinguishable identity, explicit registration, reuse across multiple Provenance occurrences, immutable treatment; not automatically promoted from a Settings class, .env file, configuration file, environment name, CLI argument set, source filename, variable name, external Configuration ID, Domain constant, or existing content-bearing Domain table
Confidential Known Configuration: Withheld or confidential parameter values alone do not force Unknown classification when identity is known; sanitized canonical_name permitted; no content stored regardless
Unknown Configuration Specification: A complete, non-empty record is valid when some Configuration use is known but identity itself is unresolved or unavailable
configuration_ref = None: Distinct from an Unknown Configuration Specification record; means no registered Configuration applies, hardcoded/default behavior was used without a registered identity, or Configuration use was not recorded
Secret and confidential-data policy: Raw secret values, credentials, API keys, tokens, passwords, private keys, secret references, and secret/environment-variable names are never stored, Known or Unknown alike; secret rotation alone never changes Configuration Specification identity; no secret manager, secret resolution, access-control policy, confidentiality classifier, or redaction engine is designed or implemented
Correction and invalid-record policy: No in-place mutation, no automatic merge, no ID reuse; old and corrected records remain unresolved within Core pending a future Resolution/Revision Concept (documented v0.1 Operational Limitation)
Duplicate-record risk: Known Operational Risk in the absence of a minting authority and Resolution mechanism; no automatic deduplication, value-based deduplication, semantic deduplication, or hash-based deduplication performed
Provenance.configuration_ref: Unchanged, str | None, opaque
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Environment loader: Not authorized
Secret manager: Not authorized
Deployment integration: Not authorized
Configuration execution engine: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-011 — Atlas Core Canonical External Run v0.1

```text
Decision ID: ACR-011
Title: Atlas Core Canonical External Run v0.1
Status: Approved
Decision date: 2026-08-04
Approved by: User
Canonical model type: Immutable occurrence identity record, not a reusable Specification
Canonical name: Not included; occurrences do not have Atlas-adopted human labels, unlike Actor/AIModel/ExecutionSpecification/PromptSpecification/ConfigurationSpecification
Canonical unit: One externally recognized and independently distinguishable execution occurrence at the highest logical execution level made available by the external system
Hierarchy rule: If a Provider exposes a Job/Workflow Run ID, the Job/Workflow is the v0.1 External Run; if a Provider exposes only request/attempt-level IDs, each request/attempt is its own External Run; if a Provider exposes both a parent Run ID and Attempt IDs, the parent Run is the v0.1 External Run and Attempts are deferred; if a Provider retries internally under one Run ID, that is one External Run; if Atlas independently reissues external requests, each reissued request is a separate External Run
Exact field count: 4
Required fields: 3 (external_run_id, external_run_kind, recorded_at)
Optional fields: 1 (external_identifier)
Defaulted fields: 1 (external_identifier=None)
Field order: external_run_id, external_run_kind, external_identifier, recorded_at
external_run_kind classification axis: External execution architecture only
external_run_kind recommended vocabulary: request, job, batch, workflow, operation, delivery, unknown
external_run_kind excludes: response/context architecture (stream, session, thread, conversation, response, result), protocol/transport (http, webhook, queue, rpc, sdk, cli — webhook is transport, the occurrence-architecture equivalent is delivery), and functional purpose (generation, publication, collection, analysis, upload, download), all expressible via Provenance.activity_kind, ExecutionSpecification, or Domain-local policy instead
External identifier policy: external_identifier, when present, is the execution-occurrence identifier issued by the external system, preserved verbatim; Atlas must never add a Provider prefix, construct a compound key, parse, normalize, case-convert, truncate, hash, mask, redact, or sanitize it; a sanitized/hashed/redacted substitute must never be stored under this field; if the exact identifier cannot appropriately be stored, external_identifier=None
Prohibited identifier sources: Atlas-generated UUIDs, correlation IDs, compound/dedup keys, local database IDs, and External Resource IDs (post IDs, video IDs, listing IDs, article IDs, uploaded file IDs) must never be stored as external_identifier
Security and privacy policy: Secrets, credentials, API keys, tokens, passwords, authorization headers, signed URLs, request/response payloads, raw error messages, personal information, direct user identifiers, session identifiers, thread/conversation identifiers, and External Resource IDs must never be stored anywhere in this record
Known External Run: Requires Atlas to reasonably confirm the external system accepted, registered, or executed one independent occurrence, that the logical execution unit is distinguishable, and that execution semantics are understood; attempting to send a request, a local function call, a retry counter increment, an Atlas UUID, a timeout, or an unconfirmed acceptance are insufficient alone
Known without stored identifier: Valid when occurrence and execution semantics are confirmed but the identifier was not issued, not returned, lost, confidential, or otherwise unsuitable to store
Unknown External Run: Valid when the external occurrence is confirmed but logical identity or execution semantics remain unresolved; external_run_kind="unknown" is recommended, not enforced; an identifier may be stored only if Atlas can confirm it was issued by the external system for an execution occurrence, never as a generic container for an ambiguous ID; confidential identifiers alone do not force Unknown
external_run_ref = None: Distinct from both Known and Unknown; means no external system was invoked, Atlas failed before external acceptance was confirmed, external execution could not be confirmed, or External Run use was not recorded
Time policy: recorded_at means only the time Atlas recorded the record; no started_at, completed_at, or other external timestamp field exists in v0.1
Status policy: No mutable status field exists; external status changes never update this record; deferred to a future External Run State/Timeline Concept
Correction policy: No in-place mutation, no automatic merge, no ID reuse, no automatic deduplication; a corrected record is newly minted; old/new relationship remains unresolved within Core pending a future Resolution/Revision Concept (documented v0.1 Operational Limitation)
Duplicate/collision risk: Known Operational Risk — the same identifier string may be issued by different Providers or reused after retention expiry; not detected, not prevented, not resolved in v0.1
Cardinality: Provenance.external_run_ref remains singular, str | None, unchanged; sufficient for the currently observed one-Provenance-to-at-most-one-external-occurrence recording pattern; NOT sufficient for one Provenance orchestrating multiple external Runs, one Provenance retaining every retry identifier, one parent Run with separately addressable Attempts, or many-to-many Provenance/External Run relationships requiring relationship metadata (documented v0.1 Operational Limitation, deferred to a future Provenance revision, Provenance–External Run Relationship Concept, or External Attempt Concept)
Provider/External System Concept: Deferred, not designed or implemented
External Resource Concept: Deferred, not designed or implemented
External Attempt Concept: Deferred, not designed or implemented
External Run State/Timeline Concept: Deferred, not designed or implemented
Provenance.external_run_ref: Unchanged, str | None, opaque
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Provider integration: Not authorized
Request execution: Not authorized
Retry engine: Not authorized
Webhook handler: Not authorized
Status polling: Not authorized
External API client: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-012 — Atlas Core Canonical Artifact v0.1

```text
Decision ID: ACR-012
Title: Atlas Core Canonical Artifact v0.1
Status: Approved
Decision date: 2026-08-04
Approved by: User
Canonical model type: Immutable representation-revision identity record
Canonical unit: One immutable, independently distinguishable representation revision of information or content that Atlas deliberately retained or registered for durable reference. Artifact is not a capture occurrence; capture, download, generation, conversion, and serialization are Provenance activities, and Artifact is the representation those activities deliberately retained or registered.
Exact field count: 7
Required fields: 3 (artifact_id, artifact_kind, recorded_at)
Optional fields: 4 (content_digest, digest_algorithm, media_type, artifact_locator)
Defaulted fields: 4, all default to None
Field order: artifact_id, artifact_kind, content_digest, digest_algorithm, media_type, artifact_locator, recorded_at
Digest pair invariant: content_digest and digest_algorithm must be both present or both absent, enforced
canonical_name: Not included; a representation revision is not a human-adopted reusable label
byte_length / size_bytes: Not included in v0.1, deliberately diverging from Evidence's shape; deferred to a future Artifact Integrity Concept
Raw content in Core: NO, under any circumstance
Identity semantics: representation identity, never semantic identity, never capture-occurrence identity; two representations with different bytes are always different Artifacts regardless of matching meaning; a matching digest and algorithm across two records is evidence supporting byte-representation equality but never causes Core to merge, reuse, or deduplicate identities
content_digest semantics: a Domain-supplied digest of the exact registered representation bytes; never computed, normalized, or canonicalized by Core
artifact_locator semantics: the opaque locator Atlas recorded for the representation at registration time; not guaranteed current or retrievable; prohibited from containing signed URLs, credentials, API keys, access tokens, passwords, authorization data, personal information, or confidential query parameters
media_type semantics: opaque, finer representation metadata, distinct from artifact_kind's structural axis, never MIME-parsed or validated
artifact_kind classification axis: representation architecture only (text, binary, structured, collection, unknown); media family, semantic purpose, and storage format are explicitly excluded from the recommended vocabulary
Git/temporary/cache rule: Git tracking status, filename, directory name, cache name, or temporary storage path alone neither establishes nor disqualifies Artifact status; the determining fact is deliberate retention or registration for durable reference
Prompt/Configuration representations: Prompt template content, rendered Prompts, Configuration parameter bundles, resolved Configuration snapshots, and API request/response representations may become Canonical Artifacts when durably retained/registered; a future Prompt Artifact or Configuration Artifact Concept is not decided to be exclusive of Canonical Artifact
Known Artifact: May validly contain only artifact_id, artifact_kind, and recorded_at when digest, locator, and media_type cannot appropriately be stored; confidentiality alone does not force Unknown status
Unknown Artifact: Valid only when a durable/registered Artifact is known to have existed but its representation identity or kind is unresolved or unavailable; never used merely because a response occurred but was never retained
Absence from input_refs: Provenance.input_refs == () does not imply an Unknown Artifact exists
Security and privacy: no raw content, secrets, credentials, API keys, tokens, passwords, authorization headers, signed URLs, or personal information may be stored anywhere in this record; digest of secret content is never required
Time policy: recorded_at means only the time Atlas recorded the record, never content creation, capture, retrieval, modification, publication, deletion, or expiry time
Immutability and correction: records are never overwritten or mutated; a changed byte representation always requires a new Artifact identity; a corrected record is newly minted with the old/new relationship unresolved within Core; duplicate records and duplicate digest values remain technically constructible
Input/output roles: relationships, not intrinsic Artifact fields; no artifact_role, produced_by_provenance_ref, input_provenance_refs, or output_provenance_refs field exists
Provenance.input_refs: Unchanged, tuple[str, ...] = (); Artifact.artifact_id is one valid semantic referent among several (Artifact, Observation, Evidence, Source when materially consumed), not the only possible referent; pre-existing ACR-004 heterogeneity is unchanged
input_refs heterogeneity limitation: input_refs contains opaque strings and does not expose which Canonical Concept a given reference targets; deferred to a future typed Provenance Input Relationship Concept
Evidence compatibility: Evidence remains entirely unmodified; Evidence.artifact_locator is not declared equal to, or automatically resolved into, Artifact.artifact_id; recorded as a Named Compatibility Limitation and Open Question
Deferred relationship Concepts: Provenance–Artifact Relationship, Artifact Derivation, Artifact Collection Membership, Artifact Storage Location, Artifact Integrity, Artifact–External Resource Relationship, Artifact–Observation/Evidence Relationship, Typed Provenance Input Relationship, Evidence–Artifact Relationship
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Object storage: Not authorized
Content ingestion: Not authorized
Hash computation: Not authorized
MIME detection: Not authorized
External Resource integration: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-013 — Atlas Core Canonical External Resource v0.1

```text
Decision ID: ACR-013
Title: Atlas Core Canonical External Resource v0.1
Status: Approved
Decision date: 2026-08-05
Approved by: User
Canonical model type: Immutable historical external-object identity record
Canonical unit: One durable and independently re-referenceable object identity authoritatively recognized by an external system, independent of any specific execution, mutable observed state, or Artifact representation of that object. "Durable" means the object identity exists or existed independently of one request, response, function call, execution, or capture occurrence; it does not mean permanent storage, current existence, current retrievability, or current locator validity. A deleted resource may still qualify as Known if it was once independently recognized.
Exact field count: 5
Required fields: 3 (external_resource_id, external_resource_kind, recorded_at)
Optional fields: 2 (external_identifier, resource_locator)
Defaulted fields: 2, both default to None
Field order: external_resource_id, external_resource_kind, external_identifier, resource_locator, recorded_at
canonical_name: Not included; external titles, handles, and usernames are mutable and often absent entirely, evidenced across all four investigated repositories
external_resource_kind classification axis: external resource architecture only (object, account, document, file, record, collection, dataset, message, model, deployment, unknown); media/content type, Domain semantic type, and Provider-specific type are explicitly excluded from the recommended vocabulary
external_identifier semantics: the identifier issued or authoritatively recognized by the external system for the durable object, preserved verbatim; never Atlas-constructed, normalized, prefixed, parsed, or Provider-inferred; not globally unique; not verified by Core
URL identifier-versus-locator rule: a URL may serve as external_identifier only when the external system itself authoritatively treats the exact URL as the object's identifier and no distinct authoritative object ID is available or used; otherwise the URL belongs in resource_locator
YouTube clarification: external_identifier is the authoritative YouTube video ID, resource_locator is the YouTube video URL; the complete video URL is not used as external_identifier merely because an existing Domain repository currently stores only the URL, and the same URL is not automatically placed in both fields
Atlas-generated composite key rule: Atlas-constructed compound keys (e.g. series+date, symbol+timestamp) are prohibited as external_identifier; only externally-authoritative composite keys are permitted
resource_locator semantics: the opaque locator Atlas recorded for addressing the external resource at registration time; historical only, never guaranteed current or reachable; distinct from Artifact.artifact_locator and Evidence.artifact_locator, which address Atlas's own captured copy rather than the live external object
Provider context: absent from Core by design; v0.1 permits registration without Provider context while explicitly accepting unresolved cross-provider collision and identity-scoping limitations; not described as collision-safe
Source/Provider relationship: Deferred; source_ref, provider_ref, external_system_ref, and owner_ref are not included because origin, ownership, publication, and syndication cardinality may differ by Domain
Known/Unknown/No Resource rules: Known may validly contain only external_resource_id, external_resource_kind, and recorded_at with both optional fields None; confidentiality alone does not force Unknown; Unknown requires a confirmed durable external object whose specific identity or semantics are unresolved and is never a generic container for an arbitrary unresolved ID; no record exists when only a transient response or execution occurred
Confidential identity-only Known records: explicitly permitted; both external_identifier and resource_locator may be None simultaneously without forcing Unknown status
Mutable state boundary: mutable/measured state (titles, prices, metrics, follower counts, availability) belongs to Observation or a future External Resource State Concept, never to this identity record; content representations belong to Artifact; executions belong to ExternalRun
Account/channel/shop dual identity: an account, channel, or shop may have both a separate External Resource record and a separate Actor record when both aspects are needed; no relationship field is added and the IDs are never merged
input_refs: Provenance.input_refs unchanged, tuple[str, ...] = (); ExternalResource.external_resource_id is one valid semantic referent among several (Artifact, Observation, Evidence, Source, External Resource) when an activity materially targets, consumes, reads, updates, or deletes the external object, not the only possible referent
input_refs limitation: input_refs cannot expose target Concept, relationship role, or Provider scope; this pre-existing ACR-004 heterogeneity is unchanged and extended, not resolved, by this Decision
Security and privacy: secrets, credentials, API keys, access tokens, passwords, authorization data, signed URLs, session IDs, private conversation/thread IDs, email addresses, phone numbers, and other direct personal identifiers must never be stored in external_identifier or resource_locator; when unsafe, both fields are None rather than a sanitized, masked, truncated, or hashed substitute
Time policy: recorded_at only, meaning solely the time Atlas recorded the record, never external creation, publication, update, deletion, restoration, or locator-change time
Immutability and correction: none of title change, price change, metrics change, content change, locator change, redirect, temporary unavailability, deletion, restoration, or ownership change mutate the record; a genuinely new external object identity requires a new record; an incorrect record is never overwritten, mutated, merged, or reused, and any corrected record is newly minted with the old/new relationship unresolved within Core v0.1
Existing-model compatibility: Provenance, Source, Actor, Artifact, ExternalRun, Observation, Evidence, AIModel, ExecutionSpecification, PromptSpecification, and ConfigurationSpecification remain entirely unmodified; Provenance remains exactly 13 fields
Deferred relationship Concepts: External Resource–Source Relationship, External Resource–Provider Relationship, External Resource–Actor Relationship, External Resource–Artifact Relationship, External Resource–ExternalRun Relationship, External Resource–Observation Relationship, External Resource Hierarchy/Membership, External Resource Location, External Resource Revision, External Resource Redirect/Equivalence, External Resource Ownership/Publication/Syndication Relationship, Typed Provenance Input Relationship
Existing Domain Model automatic promotion: No
Existing Repository modification: Not authorized
Existing Database modification: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Provider integration: Not authorized
Network access: Not authorized
Resource synchronization: Not authorized
Initial implementation: Pure Core Model only
```

## ACR-014 — Atlas Core Canonical Reference Frontier and Pre-Phase-3 Closure v0.1

```text
Decision ID: ACR-014
Title: Atlas Core Canonical Reference Frontier and Pre-Phase-3 Closure v0.1
Status: Approved
Decision date: 2026-08-06
Approved by: User
Current Canonical Model layer: Conditionally closed
Approved current Model count: 12
Undefined committed reference targets: 0
Current reference closure: Complete for the present Core layer
Approved closure set: Observation, Evidence, Provenance, Source, Actor, AIModel, ExecutionSpecification, PromptSpecification, ConfigurationSpecification, ExternalRun, Artifact, ExternalResource
Meaning of conditionally closed: the current twelve Canonical Models are sufficient for the present Core foundation and for entry into the next phase; no additional Canonical Model is required before the next phase; conditionally closed does not mean permanently or universally complete, and a future ACR may reopen the Model layer when new cross-Domain evidence establishes a blocking requirement
Terminology correction: Source, Actor, AIModel, ExecutionSpecification, PromptSpecification, and ConfigurationSpecification share a four-field named reusable identity shape; only ExecutionSpecification, PromptSpecification, and ConfigurationSpecification are Specifications; Source, Actor, and AIModel are identities, not Specifications
Provenance.input_refs: Unchanged, tuple[str, ...] = (); no Provenance field changes are approved by this Decision
input_refs target-type ambiguity: Accepted non-blocking limitation
input/target/context role ambiguity: Accepted non-blocking limitation
Generic Canonical Relationship: Rejected
Typed Provenance Input Relationship: Deferred, not required before next phase
Provenance Output Relationship: Deferred, not required before next phase
Narrow Provenance–Artifact Output Relationship: the highest-priority future Relationship candidate; not required before the next phase
Phase-entry blocker from missing Provenance–Artifact producer link: No
Real producer-lineage replay/audit limitation: Yes; the missing producer relationship does not prevent construction of valid current Core records, but it prevents complete producer-lineage replay and audit when a workflow must prove exactly which Provenance activity produced one specific Artifact
Deferred: ExternalResource–Artifact Relationship, Evidence–Artifact Relationship, Artifact Derivation
Rejected for the present scope, not as a permanent universal prohibition: Generic Canonical Relationship/Edge, Provenance–ExternalResource Creation Relationship, HypothesisRevision as an independent Core task before Canonical Hypothesis exists
Domain relationship evidence: the investigated Domains show different relationship pressures — atlas-x-engine: production lineage; ai-video-tracker: run membership; atlas-global-intelligence: knowledge/reasoning graph; etsy-analyzer: no current persistent Core relationship call site; these do not establish one stable universal relationship atomic unit
Canonical Hypothesis: Domain-only for the present phase; not required before next phase; the implemented atlas-global-intelligence Hypothesis is mutable, Domain-specific, uses Domain enums, and references targets through target_type plus target_code rather than a Canonical Core reference; a future Canonical Hypothesis is not permanently rejected
Canonical HypothesisRevision: Invalid as an independent Core Concept before Canonical Hypothesis; not required before next phase; a Canonical Revision Concept must not be designed before the identity and atomic unit it revises have been canonically defined; no separate Decision Ledger clarification is required beyond this ACR-014 record
Canonical AnalysisSnapshot: Domain-only in its currently implemented form; not required before next phase; the implemented atlas-global-intelligence AnalysisSnapshot is a Domain-specific one-to-one AnalysisRun companion with JSON-bearing rule and input content; its immutability or append-only enforcement was not established by the inspected code and is not claimed by this Decision
Observation Catalog requires a new Canonical Model before integration: No
Approved next approach: Observation Catalog Integration Contract, which may use existing IDs from Observation, Provenance, Artifact, ConfigurationSpecification, Source, and ExternalResource
ObservationSpecification: not pre-approved; remains only a future candidate if the Integration Contract proves that the existing Models are insufficient
Next phase entry: Approved in principle, subject to recording ACR-014 in the Decision Ledger; that recording condition is satisfied by this ACI-023 commit
Potential next Design Decision: Atlas Core Observation Catalog Integration Contract v0.1; not started or designed by this Decision
Existing Domain Model automatic promotion: No
Canonical Model implementation: Not authorized
Relationship implementation: Not authorized
Observation Catalog implementation: Not authorized
ObservationSpecification implementation: Not authorized
Hypothesis implementation: Not authorized
HypothesisRevision implementation: Not authorized
AnalysisSnapshot implementation: Not authorized
Knowledge implementation: Not authorized
Phase 3 implementation: Not authorized
Database: Not authorized
Migration: Not authorized
Adapter: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Provider integration: Not authorized
Network access: Not authorized
```

## ACR-015 — Atlas Core Observation Catalog Integration Contract v0.1

```text
Decision ID: ACR-015
Title: Atlas Core Observation Catalog Integration Contract v0.1
Status: Approved
Decision date: 2026-08-06
Approved by: User
Selected outcome: Integration Contract only
ObservationSpecification required now: No
Current twelve Models sufficient for initial Catalog integration: Yes
Canonical Model layer: Unchanged, conditionally closed
Observation Catalog ownership: Domain
Catalog entry identity ownership: Domain
Catalog revision identity ownership: Domain
Catalog definition content ownership: Domain
Catalog lifecycle ownership: Domain
Primary Integration Contract form: Standalone Atlas Core contract document (docs/OBSERVATION_CATALOG_INTEGRATION_CONTRACT.md); not a Core dataclass, not a Core database table, not a shared JSON Schema, not a Canonical Relationship Model, not a Domain migration
Leading contract atomic unit: one immutable Domain-owned Catalog production binding stating that one Provenance activity applied one Domain Catalog entry revision to govern one declared Canonical observation_kind
Mandatory production binding fields: catalog_entry_id, catalog_entry_revision_id, definition_artifact_id, provenance_id, observation_kind, recorded_at
Conditional production binding field: definition_selector, required only when the referenced Artifact contains more than one Catalog entry revision
Observation-to-binding uniqueness invariant: within one Provenance activity, one observation_kind must resolve to exactly one Catalog production binding
Output Observation IDs: not mandatory when the uniqueness invariant is satisfied; when it cannot be satisfied the Domain must record separate Provenance activities or retain explicit output_observation_ids in a Domain-local binding extension
Definition Artifact retention: mandatory for every production-used Catalog entry revision; preferred default is one definition Artifact per Catalog entry revision; a bundled Artifact covering multiple entries or revisions is permitted only with an immutable deterministic definition_selector that resolves exactly one revision; Artifact identity does not guarantee physical byte availability or verified byte-level integrity
Artifact is not: Catalog entry identity, Catalog revision identity, execution identity, the production activity, or Evidence by default
Provenance.input_refs: Unchanged, tuple[str, ...] = (); no Provenance field changes are approved by this Decision
Raw Domain Catalog IDs (catalog_entry_id, catalog_entry_revision_id) in Provenance.input_refs: Prohibited
Canonical definition Artifact ID in Provenance.input_refs: Conditional, only under existing approved material-input or governing-input semantics
Execution-related identity: remains on Provenance.execution_ref, Provenance.configuration_ref, Provenance.prompt_ref, Provenance.model_ref, Provenance.external_run_ref; these do not replace Catalog semantic revision identity
Identity replay: supported after Contract adoption through the retained Domain production binding
Semantic replay: supported after Contract adoption through the retained exact definition Artifact
Execution replay: partial and environment-dependent, through Provenance references plus Domain code/dependency/environment availability
Byte-for-byte reproduction: not guaranteed
Complete Catalog audit traceability before Contract adoption: No
Complete Catalog audit traceability after conforming adoption: Yes, subject to retained binding and definition availability
Observation immutability alone: insufficient for historical semantic interpretation; the exact retained definition revision is additionally required
Execution/Configuration/Prompt/Model IDs as Catalog revision identity substitute: Rejected; Catalog entry revision requires its own Domain-owned revision identity
ExecutionSpecification: reusable extraction, parsing, normalization, measurement, or validation implementation identity; not Catalog semantic meaning
ConfigurationSpecification: reusable runtime parameter selection, threshold, applicability filter, enabled entry set, depth, or resource-budget selection; not Catalog semantic meaning
PromptSpecification and AIModel change: creates a new Catalog semantic revision only when meaning, unit, value interpretation, applicability, normalization, or validation semantics change; otherwise it is an execution-layer change only
Source: origin of information, not automatically Catalog owner; Source kind belongs in definition/applicability content, Source identity is a runtime fact
ExternalResource: potential observed object, not automatically the observed object; ExternalResource kind belongs in definition/applicability content, ExternalResource identity is a runtime fact
Evidence: Catalog definitions, extraction procedures, and validation rules are not Evidence merely because they govern production; a validation report may be Artifact, Evidence, or Domain-only depending on independent support of the Observation; Evidence Model unchanged
Unit and value-type policy: value interpretation, value type, unit or explicit unitless status, nullability/unknown behavior, normalization semantics, and non-scalar representation policy are preserved as definition content; no Core unit registry, no closed Core type enum, no arbitrary JSON added to Observation
Lifecycle: Domain-owned; lifecycle changes do not mutate historical production bindings; deprecation does not invalidate historical Observations; deprecated revisions remain resolvable; lifecycle state is not copied into production bindings
Multi-depth processing (fast/deep/verification): depth normally changes ExecutionSpecification and/or ConfigurationSpecification identity, not semantic revision; a new semantic revision is required only when meaning, unit, value interpretation, applicability, normalization, or validation semantics change
Non-scalar output limitation: Atlas Core currently has no dedicated Observation-to-output-Artifact reference; exact linkage from one Observation to one non-scalar output Artifact (vector, embedding, bounding box, time series, structured object, large text, image, audio, or video segment) remains a Domain-local, non-blocking limitation; this does not approve or reopen the deferred Provenance–Artifact Output Relationship, the deferred Evidence–Artifact Relationship, a generic Relationship, or a new Observation field
Domain adoption: additive and optional for atlas-global-intelligence, ai-video-tracker, atlas-x-engine, and etsy-analyzer; for etsy-analyzer, existing scoring features are Domain analysis logic and are not automatically Catalog entries or Canonical Observations, and become Catalog entry candidates only if the Domain later explicitly classifies their outputs as observations governed by this Contract; no migration authorized by this Decision
Compatibility: Observation, Evidence, Provenance, Source, Actor, AIModel, ExecutionSpecification, PromptSpecification, ConfigurationSpecification, ExternalRun, Artifact, and ExternalResource are all unchanged by this Decision
Canonical Model implementation: Not authorized
ObservationSpecification implementation: Not authorized
Catalog database table: Not authorized
Core production-binding dataclass: Not authorized
Shared JSON Schema: Not authorized
Domain Adapter implementation: Not authorized
Domain migration: Not authorized
Backfill: Not authorized
Dual-write: Not authorized
Catalog service: Not authorized
Schema registry: Not authorized
Network access: Not authorized
Package installation: Not authorized
Phase 3 implementation: Not authorized
Next task ID: ACI-024, Record ACR-015 and Add Observation Catalog Integration Contract v0.1, Documentation-only Implementation
Next Decision after ACI-024: first Domain adoption trial requires a separate future Decision
```

## ACR-016 — Atlas Global Intelligence Observation Catalog Adoption Trial v0.1

```text
Decision ID: ACR-016
Title: Atlas Global Intelligence Observation Catalog Adoption Trial v0.1
Status: Approved
Decision date: 2026-08-06
Approved by: User
First adoption Domain: atlas-global-intelligence
Suitable as first adoption trial: Yes, for a bounded Definition Artifact pre-pilot
Selected adoption stage: Definition Artifact pre-pilot
Selected adoption option: C
Selected persistence form: C1, File/manifest pre-pilot
Selected Indicator code: OWID_GDP_PER_CAPITA_WLD
Selected Indicator name: GDP per capita, PPP (World) — Our World in Data / World Bank
Selected Indicator unit: 2017 international $
Selected Indicator frequency: ANNUAL
Selected Indicator country code: None
Selected Source: MANUAL_CSV
Selected adapter: ManualCsvAdapter
Repository Truth source for the selected Indicator: backend/scripts/seed_masters.py (an implemented, idempotent Indicator creation path with the approved exact values); this proves the creation path exists, not that the row exists in every runtime database — a future implementation must verify the exact runtime row and stop without modifying seed data if it is absent or different
Selected observation_kind: economic_indicator_value; recorded as semantic definition content only at this stage, and does not by itself create a Canonical Observation of that kind
Pre-pilot persistence: one immutable definition document, one Canonical Artifact representation, one immutable Domain revision-to-Artifact manifest entry; no Domain database table; no Alembic migration
Domain revision-to-Artifact manifest fields: catalog_entry_id, catalog_entry_revision_id, definition_artifact_id, recorded_at
Domain revision-to-Artifact mapping is not the ACR-015 Catalog production binding, and must never be called a production binding; the ACR-015 production binding remains exactly catalog_entry_id, catalog_entry_revision_id, definition_artifact_id, provenance_id, observation_kind, recorded_at, and is not created by this pre-pilot
Immutable mapping boundary: each revision-to-Artifact mapping entry is append-only; existing mapping entries and Artifact identities are never overwritten or deleted; a mutable current-preferred-representation selection, if introduced, must remain separate from the immutable mapping, and is not a production binding, not a Canonical lifecycle Model, and not a replacement for an earlier Artifact
Rollback: stopping future pre-pilot writes and disabling future use of trial output; existing definition Artifacts and immutable mapping entries remain retained for auditability; no existing Indicator or Observation data is repaired or deleted
Creates Catalog production binding: No
Creates Canonical Provenance: No
Creates Canonical Evidence: No
Creates Canonical Observation: No
Validates Observation-to-binding uniqueness: No
Validates full ACR-015 production conformance: No
Complete production-conformance pilot still required later: Yes
Atlas Core Model modification: No
New Canonical Model: No
ObservationSpecification: No
Domain database migration: No
Historical backfill: No
Existing Domain Observation mutation: No
Existing Domain Indicator mutation: No
Definition Artifact policy: one definition Artifact per one Indicator semantic revision; definition_selector not required; Artifact identity, definition bytes, manifest entry, and physical byte storage are four distinct concerns; Artifact identity does not guarantee permanent physical availability; the definition Artifact is not Catalog revision identity, not Evidence, not the production activity, and not the manifest entry
Semantic definition content retained at minimum: catalog_entry_id, catalog_entry_revision_id, name, observation_kind, value interpretation, value type, unit or explicit unitless status, frequency, scope interpretation, target_code semantics, observation_date semantics, period_start semantics, period_end semantics, released_at semantics, vintage_at semantics, nullability, unknown handling, normalization semantics, validation semantics, precision, scale, non-scalar policy
New semantic revision required for changes to: unit, frequency, country or scope, value interpretation, value type, precision or scale, period interpretation, observation-date interpretation, release or vintage interpretation, Source-kind applicability, normalization semantics, validation semantics
No semantic revision by default for: display-label correction, documentation typo, formatting correction, representation-only correction, lifecycle change, specific Source selection, runtime date range, batch size; a representation-only correction may create another immutable Artifact under the same semantic revision without changing prior mapping entries
Investigated Domain baseline: repository /Users/AI/Documents/atlas-global-intelligence, branch main, HEAD 80977992127b3e726bc4ef7028cba1b4d0fdef2c, commit count 10, working tree dirty (modified backend/app/models/enums.py; untracked backend/.env.before-neon, backend/alembic/versions/0007_create_knowledge_enum_types.py, backend/mac_atlas_data.dump, backend/tests/models/test_knowledge_enums.py)
ACR-016 read-only design investigation: Permitted
Any future pre-pilot or full-pilot implementation from this dirty working tree: Prohibited; before future implementation the exact clean HEAD must be recorded, the working tree must be clean, staged and untracked paths must be verified, secret/dump files must not be staged, existing migration work must be resolved separately, and no cleanup is authorized by ACR-016
Canonical Observation construction gap: the Domain's SQLAlchemy Observation row is not, and must not be treated as, a Canonical Observation instance; Canonical Observation requires a non-empty evidence_refs tuple and a provenance_ref with no direct Domain source, and observed_at requires an unresolved date-to-timezone-aware-datetime mapping decision; a future full pilot seeking literal Contract conformance must construct new, additional Canonical Observation instances, not reinterpret the existing row
Evidence construction gap: Canonical Evidence's required fields map cleanly onto RawIngestionRecord's content_hash/external_ref/fetched_at fields, but require minting a Canonical Source instance and a Canonical Provenance instance first, and cannot be constructed for Observation rows where raw_ingestion_record_id is NULL, which a future pilot must skip rather than reject
Next task ID: ACI-025, Record ACR-016 and Add Atlas Global Intelligence Definition Artifact Pre-Pilot Plan v0.1, Documentation-only Implementation
Next step after ACI-025: a separate, explicitly verified clean implementation baseline in atlas-global-intelligence is required before any Domain pre-pilot or full-pilot implementation task
```

## ACR-017 — Atlas Global Intelligence Observation Catalog Full Production-Conformance Pilot v0.1

```text
Decision ID: ACR-017
Title: Atlas Global Intelligence Observation Catalog Full Production-Conformance Pilot v0.1
Status: Approved
Decision date: 2026-08-07
Approved by: User
Governing contract: ACR-015 — Observation Catalog Integration Contract v0.1
Preceding adoption decision: ACR-016 — Atlas Global Intelligence Observation Catalog Adoption Trial v0.1
Empirical pre-pilot result: AGI-DAP-002, Definition Artifact pre-pilot, completed successfully
Target Domain baseline at approval: repository /Users/AI/Documents/atlas-global-intelligence, branch main, HEAD f467763b6be41a4013068a18f2032841b7c12d9a, commit count 13
Atlas Core baseline at approval: HEAD 4a93572d5888d85b039a3393bbb62e51e9361cb4
Selected production activity: a thin pilot-only orchestration around existing, unmodified production primitives — creates exactly one IngestionRun, constructs a directly-instantiated ManualCsvAdapter pointed at a deterministically-derived one-row pilot CSV file (the latest World row in the committed OWID fixture), and calls the existing, unmodified ingest_page(); reuses the same CsvColumnMapping values already registered in _MANUAL_CSV_REGISTRY rather than hardcoding them independently. run_ingestion() itself cannot be reused unmodified because build_adapter() has no adapter-override hook and always resolves the registry's own fixed file path; every other production primitive (IngestionRun, ingest_page, ManualCsvAdapter, RawIngestionRecord, Observation, DataQualityIssue) is reused exactly as-is. This is not a parallel replacement ingestion architecture.
Rejected production-activity shape: one activity producing multiple new Domain Observations (e.g. an unmodified run_ingestion() call against the full 1990-2024 fixture) with only one of them Canonicalized. That shape does not establish full-activity conformance and is explicitly not the approved design.
New Domain Observation count for the pilot: 1
Canonical Observation count for the pilot: 1
Selected execution database: isolated local test database (the project's own existing local Postgres test-DB infrastructure, e.g. the Makefile's `atlas_test` database)
REMOTE production DB write: No — not authorized by this Decision
REMOTE DB network required: No
Other external network required: No
Pre-runtime prerequisite: the local isolated test DB MUST be available and the atlas-global-intelligence repository's full existing pytest suite MUST pass before any full-pilot runtime execution
One-row raw input derivation: read the committed OWID fixture read-only; preserve the exact header line; filter rows to entity="World"; select the maximum year; preserve that row's exact literal text; construct bytes as the header line, a newline, the selected row line, and a newline; UTF-8 encode; compute the SHA-256 digest; retain those exact bytes, content-addressed, no-overwrite, at backend/catalog_pilot/raw_inputs/<content_digest>.csv. The full committed fixture is read-only and must never be modified by the pilot.
Definition Artifact reuse — exact approved semantic revision: OWID_GDP_PER_CAPITA_WLD:rev-a9f85919c24016f5f590c754ce1a81ee6330c804827d574a227704b867b84e44
Definition Artifact reuse — exact existing definition_artifact_id: artifact:OWID_GDP_PER_CAPITA_WLD:rev-a9f85919c24016f5f590c754ce1a81ee6330c804827d574a227704b867b84e44:63dd98d2d806ad9c6d06df1b4ba01e29c3fcca561eb73263ea9b67439fcaa0df
Definition Artifact reuse — exact existing content_digest: 63dd98d2d806ad9c6d06df1b4ba01e29c3fcca561eb73263ea9b67439fcaa0df
Definition Artifact reuse rule: the full pilot MUST re-derive this exact semantic revision and content_digest from current Repository Truth and MUST reuse them unchanged if they still match; if either integrity check fails, the pilot MUST STOP rather than silently mint a new semantic revision.
Canonical chain the full pilot MUST construct: Canonical Actor, Canonical Source, ExecutionSpecification, ConfigurationSpecification, Canonical Provenance, a raw-input Artifact, Canonical Evidence, a Canonical Observation, and the actual ACR-015 Catalog production binding. No Canonical Model is added to Atlas Core. No Atlas Core Model is modified. No generic Relationship is introduced anywhere in this chain.
Actor: actor_id "atlas-global-intelligence:pipeline:manual-csv-ingestion", actor_kind "system", canonical_name "atlas-global-intelligence MANUAL_CSV ingestion pipeline"; stable and reusable across runs, not minted per run, not a human-trigger Actor, not Source misused as Actor.
Source boundary — Domain Source row: the Domain Source row coded MANUAL_CSV represents the ingestion mechanism (how Atlas acquires a copy of the file), not the data's origin; its own canonical_name is literally "Manual CSV import".
Source boundary — Canonical Source: represents the actual information origin, Our World in Data / World Bank, grounded in the Domain's own docs/phase1-data-sources.md attribution and the Indicator's own name field, not derived from any Domain Source DB row.
Direct Domain Source to Canonical Source identity mapping: No — the Domain MANUAL_CSV Source row's role is already fully captured elsewhere, by ExecutionSpecification (the adapter mechanism) and by source_kind_applicability (already committed inside the Definition Artifact); it does not additionally require, and does not get, its own Canonical Source.
ExecutionSpecification: Yes — represents the ManualCsvAdapter implementation (its normalization and validation logic), independent of any one run; implementation version is pinned by module/file path plus the exact git commit that last changed that specific file (not the repository's overall HEAD, so unrelated commits never spuriously mint a new specification); runtime occurrence values are never folded into this identity.
ConfigurationSpecification: Yes — represents the stable, reusable CSV column-mapping rules already registered in _MANUAL_CSV_REGISTRY (date_column, value_column, date_format, entity_column, entity_filter, frequency); the one-row pilot file's path and content are run-specific raw material captured via the raw-input Artifact and Evidence, not folded into ConfigurationSpecification identity, to keep it genuinely reusable across future runs.
Canonical Provenance: Yes — the actual ACR-015 production binding's provenance_id MUST be the actual Canonical Provenance.provenance_id; Domain IngestionRun.id is never a substitute. Domain activity to Provenance mapping: provenance_id is deterministically derived from IngestionRun.id and IngestionRun.started_at; no DB mapping table is required for this relationship. Raw Domain Catalog IDs MUST NOT appear in Provenance.input_refs under any circumstance.
Raw-input Artifact: Yes — distinct from the Definition Artifact. Required equality: RawIngestionRecord.content_hash equals the Canonical raw-input Artifact's content_digest equals the SHA-256 of the retained raw-input file, guaranteed by construction since the adapter reads exactly the retained file. Locator: repo-relative:backend/catalog_pilot/raw_inputs/<content_digest>.csv.
Evidence: Yes — derived from the exact retained raw material plus the Canonical Source and Provenance identities above; MAY carry a precise selector such as entity=World, year=<selected year>; MUST NOT invent an original source publication timestamp not present in Repository Truth.
Quality gate — exact Observation-level persisted QualityIssue linkage available: No; DataQualityIssue.observation_id exists as a schema column but is never populated by the ingest_page()/upsert_normalized_record() write paths this pilot exercises. Approved mechanism: Policy A — the pilot invokes ManualCsvAdapter.validate() itself, in-memory, against the exact single selected NormalizedRecord (a pure function), rather than relying on any invented or unpopulated DB linkage. Gate: ERROR blocks Canonical Observation construction; WARNING is allowed; INFO is allowed.
Canonical Observation: Yes — the Domain SQLAlchemy Observation row remains distinct and is never modified or reinterpreted in place; a new, additional Canonical Observation instance is constructed. Approved observed_at convention: Observation.observation_date at 00:00:00 UTC.
Persisted value formatting: the Canonical normalized_statement MUST use the value actually persisted in the Domain Observation row (Numeric(20,6)), never a transient raw/adapter value and never a float conversion. Approved formatting: fixed six decimal places, derived from the persisted Decimal via quantization (e.g. 21405.117000). Exact template: "GDP per capita, PPP (World), for {year} was {persisted_value_scale_6} {unit} (source: Our World in Data / World Bank; catalog entry {catalog_entry_id})."
Observation identity: deterministic, derived from the catalog identity plus the Domain's own natural temporal identity (observation_date, vintage_at); stable, idempotent on rerun, independent of mutable prose, and distinct from the raw Domain integer primary key.
Domain Observation to Canonical mapping: an immutable file per mapping, at backend/catalog_pilot/observation_mappings/<digest>.json; no Domain database schema change.
Production binding fields, exactly six: catalog_entry_id, catalog_entry_revision_id, definition_artifact_id, provenance_id, observation_kind, recorded_at. No output_observation_ids extension — the corrected activity produces exactly one Observation, so the single-target case genuinely applies. Persistence: an immutable file at backend/catalog_pilot/bindings/<sha256(canonical_json({provenance_id, observation_kind}))>.json. This is the actual ACR-015 production binding, not a Domain-local substitute.
Uniqueness invariant: (provenance_id, observation_kind) resolves to at most one binding, enforced by the binding's deterministic filename plus immutable no-overwrite persistence plus validate-or-reuse logic plus a supporting test, in combination; no DB unique constraint and no generic Relationship are used.
Cross-store transaction model: the Domain DB transaction commits first, in full, via the existing unmodified pipeline; Canonical/file projection strictly follows and is never claimed to share one distributed atomic transaction with it. If the Domain write succeeds and Canonical projection fails partway, the Domain data remains valid and authoritative and the Canonical projection is simply incomplete; retry resumes canonicalization only, from the exact completed pilot run, and MUST NOT rerun Domain ingestion merely to repair missing Canonical files. No reconciliation queue is required for this bounded, single manually-triggered pilot.
Retry identification: derive the deterministic one-row bytes and digest again; look up a matching RawIngestionRecord by (source_id, content_hash); if found, identify that record's completed IngestionRun and its single linked Domain Observation, and resume Canonical construction only against that already-durable state; if not found, this is a genuinely first run.
Canonical persistence surface: backend/catalog_pilot/ containing actors/, sources/, execution_specs/, configuration_specs/, provenance/, raw_inputs/, raw_artifacts/, evidence/, observations/, observation_mappings/, and bindings/. Every immutable record uses a deterministic identity, a filesystem-safe filename, no-overwrite creation, validate-or-reuse logic, and a hard stop on any mismatched existing content. All pilot output is Git-tracked.
Domain database migration required: No.
Selected implementation option: A, a file-backed Canonical shadow pilot; kept explicitly separate from the selected production activity (the thin one-row pilot orchestration) and from the selected execution database (the isolated local test database) — these are three independent decisions, not one bundled choice.
Runtime atlas_core dependency: No — the pilot continues Domain-local, Core-conformant representations, re-affirmed after comparing all seven relevant Core dataclasses field by field; the underlying Core contract drift risk this carries is explicitly acknowledged, not hidden, with an explicit trigger to revisit (a third Domain adopting ACR-015).
Historical multi-row insert: No. Historical backfill: No. Existing Domain Observation mutation: No. Atlas Core modification: No. Generic Relationship: No.
Full isolated test DB required before runtime pilot execution: Yes. Full existing atlas-global-intelligence test suite PASS required before runtime pilot execution: Yes.
Consequences — positive: real Domain production transaction semantics are exercised; the full Canonical chain is exercised; the production binding invariant is exercised; no production DB mutation occurs; no Domain migration is required; the pilot's scope is bounded to exactly one row; exact raw bytes are retained.
Consequences — negative: file-backed Canonical storage is not a production-scale mechanism; there is no cross-store atomicity; Core contract drift risk exists; a pilot-specific orchestration exists alongside the normal run_ingestion() wrapper; a future, separate productionization Decision remains required.
Risks: Core contract drift; the pilot orchestration diverging from the normal wrapper over time; local DB environment drift; unbounded file accumulation if repeated carelessly; partial Canonical projection; retry misclassification; file-lookup scalability at larger scope; Source-origin semantic drift; Execution/Configuration identity drift; normalized-statement wording governance.
Open questions: when to introduce a shared atlas_core runtime package; when file-backed Canonical records would need DB indexing; whether continuous production would need a reconciliation queue; synchronous versus asynchronous Canonical projection in a real production setting.
Next task ID: ACI-027, implement and run the ACR-017 full production-conformance pilot, Implementation Task (not yet authorized to begin by this Decision alone)
Next step after ACI-026: a separate, explicitly verified clean implementation baseline and an available, passing local isolated test DB in atlas-global-intelligence are required before any full-pilot implementation task begins
```

