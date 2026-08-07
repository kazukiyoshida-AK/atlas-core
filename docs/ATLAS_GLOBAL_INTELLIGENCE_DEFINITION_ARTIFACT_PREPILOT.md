# Atlas Global Intelligence Definition Artifact Pre-Pilot Plan v0.1

```text
Decision basis: ACR-016
Status: Approved
Version: 0.1
Approved date: 2026-08-06
Implementation status: Not started
```

This document is a standalone, normative, implementation-neutral plan.
It contains no executable Python, SQL, Alembic code, shell mutation
commands, or runtime credentials. MUST/MUST NOT are hard requirements;
SHOULD is a strong recommendation with room for a documented exception;
MAY is optional.

## 1. Purpose

This plan defines a bounded pre-pilot that tests the ACR-015
definition-retention boundary — the part of the Observation Catalog
Integration Contract with zero existing analog in
atlas-global-intelligence today — before any attempt at full
Observation production integration (Provenance, Evidence, Canonical
Observation, and the ACR-015 production binding itself).

## 2. Status and limits

```text
This is a Definition Artifact pre-pilot.
It is not a complete Observation Catalog adoption.
It does not establish full ACR-015 production conformance.
```

## 3. Governing Decisions

```text
ACR-015 — Atlas Core Observation Catalog Integration Contract v0.1
ACR-016 — Atlas Global Intelligence Observation Catalog Adoption Trial v0.1
```

## 4. Target Domain

```text
Repository: /Users/AI/Documents/atlas-global-intelligence
Branch: main
Investigated HEAD: 80977992127b3e726bc4ef7028cba1b4d0fdef2c
Investigated commit count: 10
Investigated working tree: dirty
  Modified:   backend/app/models/enums.py
  Untracked:  backend/.env.before-neon
  Untracked:  backend/alembic/versions/0007_create_knowledge_enum_types.py
  Untracked:  backend/mac_atlas_data.dump
  Untracked:  backend/tests/models/test_knowledge_enums.py
```

No implementation MAY begin until a separately verified clean baseline
exists in this repository. This plan does not authorize cleanup of the
above state.

## 5. Selected Indicator

```text
Indicator code: OWID_GDP_PER_CAPITA_WLD
Indicator name: GDP per capita, PPP (World) — Our World in Data / World Bank
Unit: 2017 international $
Frequency: ANNUAL
Country code: None
Source: MANUAL_CSV
Adapter: ManualCsvAdapter
Repository Truth source: backend/scripts/seed_masters.py
```

Qualification: the seed script proves an implemented, idempotent
Indicator creation path with these exact values. It does not prove the
row exists in every runtime database. A future implementation MUST
verify the exact runtime row exists and matches these values, and MUST
stop without modifying seed data if the row is absent or different.

## 6. Selected observation kind

```text
economic_indicator_value
```

This is semantic definition content only at this stage. Recording it
does not create a Canonical Observation of this kind, and does not
replace catalog_entry_id as the distinguishing identity between
Indicators.

## 7. Pre-pilot scope

In scope:

* one Domain Catalog entry identity
* one immutable semantic revision identity
* one exact definition document
* one Canonical Artifact representation
* one immutable revision-to-Artifact mapping
* deterministic lookup
* retained unit/value semantics
* rollback-by-stopping-future-writes

Out of scope:

* production binding
* Provenance
* Evidence
* Canonical Observation
* ingestion-pipeline integration
* execution/configuration identities
* historical backfill
* database migration
* Domain Observation mutation
* full ACR-015 conformance

## 8. Persistence form

Selected form: C1.

```text
immutable definition document
Canonical Artifact identity
immutable manifest entry
physical byte storage
```

These are four separate concerns. This plan does not specify a final
runtime path or serialization format for any of them; those are left
for the future implementation design, which is itself a separate task
not authorized here.

## 9. Revision-to-Artifact mapping

Required fields:

```text
catalog_entry_id
catalog_entry_revision_id
definition_artifact_id
recorded_at
```

* MUST be append-only
* MUST be immutable once written
* MUST NOT be called, or treated as, a production binding
* MUST NOT contain provenance_id
* MUST NOT contain observation_kind
* MUST NOT contain output_observation_ids

## 10. Preferred representation

A Domain MAY maintain a separate, mutable current-preferred-
representation selection identifying which Artifact representation is
currently preferred for one semantic revision. This selection MUST
remain separate from the immutable mapping entries. Historical mapping
entries MUST NOT be rewritten, regardless of any later preferred-
representation change.

## 11. Definition Artifact requirements

* one Artifact per one semantic revision by default
* no definition_selector required
* content_digest/digest_algorithm support integrity checking after
  retrieval only — they do not prove availability
* Artifact identity does not guarantee physical availability forever
* the Artifact is not Evidence
* the Artifact is not the Catalog revision identity
* the Artifact is not the manifest entry

## 12. Definition content

The definition MUST retain at minimum:

```text
catalog_entry_id
catalog_entry_revision_id
name
observation_kind
value interpretation
value type
unit or explicit unitless status
frequency
scope interpretation
target_code semantics
observation_date semantics
period_start semantics
period_end semantics
released_at semantics
vintage_at semantics
nullability
unknown handling
normalization semantics
validation semantics
precision
scale
non-scalar policy
```

## 13. Semantic revision rules

New semantic revision REQUIRED for changes to:

```text
unit
frequency
country or scope
value interpretation
value type
precision or scale
period interpretation
observation-date interpretation
release or vintage interpretation
Source-kind applicability
normalization semantics
validation semantics
```

New semantic revision NOT required by default for:

```text
display-label correction
documentation typo
formatting correction
representation-only correction
lifecycle change
specific Source selection
runtime date range
batch size
```

## 14. Representation-only corrections

A representation-only correction (bytes change, meaning unchanged)
MAY create a new immutable Artifact representation under the same
catalog_entry_revision_id. It MUST NOT change, remove, or rewrite any
prior mapping entry.

## 15. Source and adapter boundary

* MANUAL_CSV is the selected Source
* ManualCsvAdapter is the implemented adapter
* specific Source identity is runtime context, not semantic definition
  content
* adapter implementation is an execution-layer concern
* full ExecutionSpecification／ConfigurationSpecification work is
  deferred to a future full pilot

## 16. Success criteria

The future pre-pilot succeeds only if it demonstrates:

1. exact selected Indicator row exists and matches §5
2. stable catalog_entry_id
3. immutable catalog_entry_revision_id
4. exact definition bytes
5. valid Canonical Artifact identity
6. deterministic revision-to-Artifact lookup
7. retained unit/value semantics
8. no Core Model modification
9. no existing Domain data mutation
10. no migration
11. no historical backfill
12. existing Artifact/mapping retention after rollback
13. no claim of full production conformance

## 17. Stop criteria

* dirty target repository
* Indicator row absent or different from §5
* secret/dump handling required
* migration required
* existing data mutation required
* Artifact digest/locator cannot be produced
* exact definition cannot be reconstructed
* Core Model change required
* production binding required to complete this bounded stage
* live ingestion required
* generic Relationship required

## 18. Rollback

Rollback means stopping all additional pre-pilot writes and disabling
future use of the trial output. Already-created definition Artifacts
and immutable revision-to-Artifact mapping entries remain retained for
auditability. No existing Indicator or Observation data is repaired or
deleted.

## 19. Known limitations

* no runtime production test
* no transaction test
* no Provenance/Evidence/Observation
* no uniqueness test
* file/manifest approach is not a scalable Catalog store
* physical byte availability is Domain-dependent
* a full pilot remains required to reach ACR-015 conformance

## 20. Future full pilot

A separate future Decision must evaluate:

```text
Actor
Source
ExecutionSpecification
ConfigurationSpecification
Provenance
Evidence
Observation
full Catalog production binding
Domain-to-Canonical mappings
```

None of these are designed or authorized by this plan.

## 21. Prohibited actions

This plan explicitly prohibits, for this pre-pilot stage:

* atlas-global-intelligence modification
* seed execution
* database write
* migration
* Artifact runtime creation
* manifest runtime creation
* cleanup of dirty files
* opening or copying secret or dump content
* Atlas Core source/test changes
* a full production pilot
