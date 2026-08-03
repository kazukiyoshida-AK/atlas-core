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

