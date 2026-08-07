# Atlas Global Intelligence Observation Catalog Full Production-Conformance Pilot Plan v0.1

```text
Decision basis: ACR-017
Status: Approved
Version: 0.1
Approved date: 2026-08-07
Implementation status: Not started
```

This document is a standalone, normative, implementation-neutral plan.
It contains no executable Python, SQL, Alembic code, shell mutation
commands, or runtime credentials. MUST/MUST NOT are hard requirements;
SHOULD is a strong recommendation with room for a documented exception;
MAY is optional.

## 1. Purpose

This plan defines a bounded full production-conformance pilot that
proves the ACR-015 Observation Catalog Integration Contract can be
satisfied end to end — Canonical Actor, Canonical Source,
ExecutionSpecification, ConfigurationSpecification, Canonical
Provenance, a raw-input Artifact, Canonical Evidence, a Canonical
Observation, and the actual ACR-015 Catalog production binding — for
exactly one real, prospective Domain production activity.

## 2. Status and limits

```text
This is a full production-conformance pilot for one bounded activity.
It is not a general-purpose Canonical integration for
atlas-global-intelligence.
It does not authorize repeated or scheduled production use.
```

## 3. Governing Decisions

```text
ACR-015 — Atlas Core Observation Catalog Integration Contract v0.1
ACR-016 — Atlas Global Intelligence Observation Catalog Adoption Trial v0.1
ACR-017 — Atlas Global Intelligence Observation Catalog Full
          Production-Conformance Pilot v0.1
```

## 4. Empirical basis

```text
AGI-DAP-002 — Definition Artifact pre-pilot for OWID_GDP_PER_CAPITA_WLD,
completed successfully.
```

The full pilot MUST reuse, not regenerate, that pre-pilot's exact
semantic revision and definition Artifact if Repository Truth still
matches (§9).

## 5. Selected production activity

A thin pilot-only orchestration around existing, unmodified production
primitives:

```text
* creates exactly one IngestionRun
* constructs a directly-instantiated ManualCsvAdapter, pointed at a
  deterministically-derived one-row pilot CSV file, instead of going
  through build_adapter() (which has no adapter-override hook)
* reuses the exact CsvColumnMapping values already registered for
  OWID_GDP_PER_CAPITA_WLD, rather than hardcoding them independently
* calls the existing, unmodified ingest_page()
* produces exactly one new RawIngestionRecord
* produces exactly one new Domain Observation
```

This MUST NOT be described as conforming if it produces more than one
new Domain Observation. The following shape is explicitly rejected:

```text
one activity -> multiple new Domain Observations -> only one of them
Canonicalized
```

That shape does not establish conformance of the activity as a whole.

```text
New Domain Observation count: 1
Canonical Observation count: 1
```

No existing production ingestion service, adapter, or model is
modified. No parallel replacement ingestion architecture is introduced.

## 6. Execution environment

```text
Selected execution database: ISOLATED LOCAL TEST DATABASE
REMOTE production DB write: NO
REMOTE DB network required: NO
Other external network required: NO
```

Before any full-pilot runtime execution:

```text
Local isolated DB available: REQUIRED
Full existing atlas-global-intelligence test suite: REQUIRED PASS
```

The pilot exercises the same Domain models, services, and transaction
structure production uses; it does so against the project's own
existing local isolated test-DB infrastructure, not the remote runtime
database.

## 7. One-row raw input

```text
1. Read the committed OWID fixture, read-only.
2. Preserve the exact header line.
3. Filter rows to entity == "World".
4. Select the maximum year among those rows.
5. Preserve that row's exact literal text.
6. Construct exact bytes: <header line>\n<selected row line>\n
7. UTF-8 encode.
8. Compute the SHA-256 digest of those exact bytes.
9. Retain those exact bytes, content-addressed, no-overwrite, at:
   backend/catalog_pilot/raw_inputs/<content_digest>.csv
```

The existing full committed fixture MUST remain read-only and MUST NOT
be modified by the pilot. This single retained file serves both as the
adapter's actual input and as the durably-retained raw-input Artifact
content — no separate duplicate copy is created.

## 8. Quality gate

```text
Exact Observation-level persisted QualityIssue linkage available: NO
```

`DataQualityIssue.observation_id` exists as a schema column but is
never populated by the write paths this pilot exercises. The approved
mechanism is Policy A: the pilot invokes the adapter's own validation
function itself, in-memory, against the exact single selected
normalized record, rather than relying on any invented or unpopulated
database linkage.

```text
ERROR:   blocks Canonical Observation construction
WARNING: allowed
INFO:    allowed
```

## 9. Definition Artifact reuse

```text
Selected semantic revision:
OWID_GDP_PER_CAPITA_WLD:rev-a9f85919c24016f5f590c754ce1a81ee6330c804827d574a227704b867b84e44

Existing definition_artifact_id:
artifact:OWID_GDP_PER_CAPITA_WLD:rev-a9f85919c24016f5f590c754ce1a81ee6330c804827d574a227704b867b84e44:63dd98d2d806ad9c6d06df1b4ba01e29c3fcca561eb73263ea9b67439fcaa0df

Existing content_digest:
63dd98d2d806ad9c6d06df1b4ba01e29c3fcca561eb73263ea9b67439fcaa0df
```

The pilot MUST re-derive this exact semantic revision and content
digest from current Repository Truth before proceeding, and MUST reuse
them unchanged if they still match. If either integrity check fails,
the pilot MUST STOP; it MUST NOT silently mint a new semantic revision.

## 10. Canonical chain

The pilot MUST construct Core-conformant representations for:

```text
Canonical Actor
Canonical Source
ExecutionSpecification
ConfigurationSpecification
Canonical Provenance
a raw-input Artifact
Canonical Evidence
a Canonical Observation
the actual ACR-015 Catalog production binding
```

No Canonical Model is added to Atlas Core. No Atlas Core Model is
modified. No generic Relationship is introduced anywhere in this chain.

### 10.1 Actor

```text
actor_id: atlas-global-intelligence:pipeline:manual-csv-ingestion
actor_kind: system
canonical_name: atlas-global-intelligence MANUAL_CSV ingestion pipeline
```

Stable and reusable across runs; not minted per run; not a
human-trigger Actor; Source MUST NOT be misused as Actor.

### 10.2 Source boundary

```text
Domain Source row (code MANUAL_CSV): represents the ingestion
mechanism -- how Atlas acquires a copy of the file -- not the data's
origin.

Canonical Source: represents the actual information origin, Our World
in Data / World Bank, grounded in the Domain's own data-source
documentation and the Indicator's own name field.

Direct Domain Source -> Canonical Source identity mapping: NO
```

The Domain `MANUAL_CSV` Source row's role is already fully captured by
ExecutionSpecification (the adapter mechanism) and by
`source_kind_applicability` (already committed inside the Definition
Artifact); it MUST NOT additionally be forced into its own Canonical
Source identity.

### 10.3 ExecutionSpecification

Represents the `ManualCsvAdapter` implementation (its normalization and
validation logic), independent of any one run. Implementation version
is pinned by module/file path plus the exact git commit that last
changed that specific file — not the repository's overall HEAD, so
unrelated commits never spuriously mint a new specification. Runtime
occurrence values MUST NOT be folded into this identity.

### 10.4 ConfigurationSpecification

Represents the stable, reusable CSV column-mapping rules already
registered for this Indicator (date column, value column, date format,
entity column, entity filter, frequency). The one-row pilot file's path
and content are run-specific raw material, captured via the raw-input
Artifact and Evidence (§7, §10.6) — they MUST NOT be folded into
ConfigurationSpecification identity.

### 10.5 Provenance

The production binding's `provenance_id` MUST be the actual Canonical
Provenance's `provenance_id`. Domain `IngestionRun.id` is never a
substitute. `provenance_id` is deterministically derived from
`IngestionRun.id` and `IngestionRun.started_at`; no additional database
mapping table is required for this relationship. Raw Domain Catalog IDs
MUST NOT appear in `Provenance.input_refs` under any circumstance.

### 10.6 Raw-input Artifact

Distinct from the Definition Artifact. The following MUST agree
exactly:

```text
RawIngestionRecord.content_hash
==
Canonical raw-input Artifact.content_digest
==
SHA-256 of the retained raw-input file
```

Locator: `repo-relative:backend/catalog_pilot/raw_inputs/<content_digest>.csv`.

### 10.7 Evidence

Derived from the exact retained raw material plus the Canonical Source
and Provenance identities. MAY carry a precise selector (e.g. entity
and year) identifying which row within the retained file it concerns.
MUST NOT invent an original source publication timestamp that is not
present in Repository Truth.

### 10.8 Canonical Observation

The Domain SQLAlchemy `Observation` row remains distinct and MUST NOT
be modified or reinterpreted in place; a new, additional Canonical
Observation instance is constructed.

```text
observed_at convention: Observation.observation_date at 00:00:00 UTC
```

### 10.9 Persisted value formatting

The Canonical `normalized_statement` MUST use the value actually
persisted in the Domain Observation row (`Numeric(20,6)`), never a
transient raw/adapter value, and MUST NOT pass through a float
conversion at any point.

```text
Formatting: fixed six decimal places, derived from the persisted
Decimal via quantization.
Example: 21405.117000
```

Exact template:

```text
GDP per capita, PPP (World), for {year} was {persisted_value_scale_6} {unit} (source: Our World in Data / World Bank; catalog entry {catalog_entry_id}).
```

### 10.10 Observation identity

Deterministic, derived from the catalog identity plus the Domain's own
natural temporal identity (`observation_date`, `vintage_at`). Stable,
idempotent on rerun, independent of mutable prose, and distinct from
the raw Domain integer primary key.

### 10.11 Domain Observation to Canonical mapping

An immutable file per mapping, at
`backend/catalog_pilot/observation_mappings/<digest>.json`. No Domain
database schema change.

### 10.12 Production binding

Exactly six fields:

```text
catalog_entry_id
catalog_entry_revision_id
definition_artifact_id
provenance_id
observation_kind
recorded_at
```

No `output_observation_ids` extension — the corrected activity produces
exactly one Observation, so the single-target case applies. Persisted
at `backend/catalog_pilot/bindings/<sha256(canonical_json({provenance_id, observation_kind}))>.json`.
This IS the actual ACR-015 production binding, not a Domain-local
substitute for it.

## 11. Uniqueness invariant

```text
(provenance_id, observation_kind) -> at most one binding
```

Enforced by the binding's deterministic filename, immutable
no-overwrite persistence, validate-or-reuse logic, and a supporting
test, in combination. No database unique constraint and no generic
Relationship are used.

## 12. Cross-store transaction and failure model

The Domain database transaction commits first, in full, via the
existing unmodified pipeline. Canonical/file projection strictly
follows and never claims to share one distributed atomic transaction
with it.

```text
Domain write fails: Canonical construction never begins.
Domain succeeds, Canonical projection fails partway: the Domain data
  remains valid and authoritative; the Canonical projection is simply
  incomplete.
Retry: resumes Canonical construction only, from the exact completed
  pilot run; MUST NOT rerun Domain ingestion merely to repair missing
  Canonical files.
Reconciliation queue: not required for this bounded, single
  manually-triggered pilot.
```

Retry identification: derive the deterministic one-row bytes and digest
again; look up a matching `RawIngestionRecord` by `(source_id,
content_hash)`; if found, identify that record's completed
`IngestionRun` and its single linked Domain Observation, and resume
Canonical construction only against that already-durable state.

## 13. Canonical persistence surface

```text
backend/catalog_pilot/
  actors/
  sources/
  execution_specs/
  configuration_specs/
  provenance/
  raw_inputs/
  raw_artifacts/
  evidence/
  observations/
  observation_mappings/
  bindings/
```

Every immutable record MUST use a deterministic identity, a
filesystem-safe filename, no-overwrite creation, validate-or-reuse
logic, and a hard stop on any mismatched existing content. All pilot
output MUST be Git-tracked. No mutable generic Relationship store is
introduced anywhere in this surface.

## 14. Domain database migration

```text
Domain database migration required: NO
```

## 15. Selected implementation option

```text
Option A — File-backed Canonical shadow pilot.
```

Kept explicitly separate from the selected production activity (§5, the
thin one-row pilot orchestration) and from the selected execution
database (§6, the isolated local test database) — these are three
independent decisions, not one bundled choice.

## 16. Core runtime integration

```text
Runtime atlas_core dependency: NO
```

The pilot continues Domain-local, Core-conformant representations,
re-affirmed after comparing all seven relevant Core dataclasses field by
field. This carries a real, disclosed Core-contract-drift risk, not a
hidden one; an explicit trigger to revisit is a third Domain adopting
ACR-015.

## 17. Success criteria

The pilot succeeds only if it proves at minimum:

```text
1. exact approved baseline (both repositories)
2. isolated local DB available
3. full existing atlas-global-intelligence test suite passes before
   the pilot runs
4. exact Definition Artifact integrity check passes
5. exactly one pilot IngestionRun created
6. exactly one RawIngestionRecord created
7. exactly one new Domain Observation created
8. exactly that Domain Observation is Canonicalized
9. exact raw input bytes retained
10. three-way raw digest equality (RawIngestionRecord.content_hash,
    raw-input Artifact content_digest, retained-file SHA-256)
11. Actor valid
12. Source valid
13. ExecutionSpecification valid
14. ConfigurationSpecification valid
15. Provenance valid
16. Evidence valid
17. Canonical Observation valid
18. quality gate applied (Policy A)
19. six-field production binding created
20. uniqueness invariant proven
21. no raw Domain Catalog ID in Provenance.input_refs
22. no historical multi-row insert
23. no historical backfill
24. no Domain Observation mutation
25. no Domain database migration
26. no Atlas Core modification
27. no generic Relationship
28. idempotent retry proven
29. partial Canonical failure recoverable without rerunning Domain
    ingestion
30. REMOTE production DB untouched
```

## 18. Stop criteria

```text
* baseline drift in either repository
* Definition Artifact integrity mismatch
* semantic definition changed since AGI-DAP-002
* isolated local DB unavailable
* full existing test suite failure
* selected activity would create more than one Domain Observation
* historical-series insertion required
* exact raw bytes cannot be retained
* RawIngestionRecord hash mismatch against the retained file
* Evidence cannot be constructed
* quality gate cannot use the approved Policy A mechanism
* Canonical Observation invalid against Core's own required fields
* uniqueness invariant fails
* raw Domain IDs would be required in Provenance.input_refs
* Domain database migration required
* REMOTE DB mutation required
* historical mutation required
* generic Relationship required
* Atlas Core modification required
* secret/dump file access required
* Canonical recovery would require rerunning Domain ingestion
```

## 19. Prohibited actions

This plan explicitly prohibits, for this pilot's implementation stage:

```text
* atlas-core source or test modification
* atlas-global-intelligence production ingestion/service/model
  modification
* REMOTE production database access of any kind
* Docker or local test-DB startup as part of this documentation task
* database migration
* seed execution
* historical backfill or historical multi-row processing
* opening or copying secret or dump content
* a claim of full ACR-015 conformance beyond this one bounded activity
```

## 20. Future work

A separate, later Decision must evaluate: introducing a shared
`atlas_core` runtime package if a third Domain adopts ACR-015;
DB-indexing the Canonical records if scale ever requires it; a
reconciliation queue if continuous, unattended production adoption is
pursued; and synchronous versus asynchronous Canonical projection for a
real production deployment. None of these are designed or authorized by
this plan.
