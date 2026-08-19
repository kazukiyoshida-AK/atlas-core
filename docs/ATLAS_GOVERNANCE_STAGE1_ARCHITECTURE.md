# Atlas Governance Stage 1 Architecture — Consolidated Reference

This document consolidates the Atlas Head / Cognitive Governance ("AH-CGR")
decision chain (AH-CGR-001 through AH-CGR-008B1), approved in a controlling
design/review session prior to repository canonicalization. It is
**referenced by** ACR-019 through ACR-027 in `docs/DECISIONS.md`, which
remains the authoritative Decision Ledger. This document does not create
competing authority; where any wording differs, `docs/DECISIONS.md` governs.

Canonicalization note: these decisions were approved in the controlling
session and are recorded here on the date of canonicalization. Where a
distinct original approval date is not independently known, the
canonicalization date is used for both fields, per ACR-019 through ACR-027
in the Ledger.

## Implementation State (authoritative, applies to all sections below)

```text
Governance architecture: APPROVED / CANONICAL
Governance DB:            NOT YET CREATED
Alembic:                  NOT YET INITIALIZED
Migration implementation: NOT YET STARTED
Runtime:                  NOT YET IMPLEMENTED
```

No table, role, schema, function, grant, or migration described below has
been created. This document records approved design only.

## Philosophy Alignment

All sections below were evaluated against ACR-018 (Atlas Foundry Persistent
Intelligence Philosophy): Reality Sovereignty, Evidence Before Authority,
Failure Is Data, Human Sovereignty, Controlled Evolution, Persistent
Intelligence, historical preservation, and no silent deletion/overwrite of
failure. No material conflict was found in any AH-CGR decision against
ACR-018. This does not replace or reinterpret ACR-018.

---

## 1. Canonical Reconciliation (→ ACR-019)

- `atlas-core` is a dependency-free Canonical Contract package: 12 frozen
  dataclasses, no ORM, no SQLAlchemy, no Alembic, no SQL, no auth/role
  implementation.
- Core references are opaque string IDs.
- No Canonical `RawArtifact`; a generic `Artifact` Canonical Model exists
  (ACR-012).
- Canonical Actor is a semantic/accountable identity — distinct from
  Authentication Principal and DB Role (see §4 / ACR-022).
- A Governance physical FK to Core is not required and not selected;
  Canonical ID reference integration is compatible with Core as-is.

## 2. Physical DB Ownership (→ ACR-020)

```text
atlas-core:
  Canonical contracts / philosophy / invariants / decisions

atlas-governance:
  Governance runtime
  PostgreSQL owner
  Alembic owner
  DB Role owner
  SECURITY DEFINER owner
  Audit owner
  Policy / Permit owner
```

Primary schema: `atlas_governance`. Governance → Core reference type:
**CANONICAL ID REFERENCE** (TEXT), no physical FK. Direct Domain writes to
the Governance DB: **PROHIBITED**. Artifact tombstone ownership: Governance
owns tombstone/audit continuity; Domain/storage layer owns actual physical
byte deletion.

## 3. Governance Repository Bootstrap Boundary (→ ACR-021)

A dedicated `atlas-governance` repository was selected and bootstrapped.
At the time of this Decision: no runtime DB, no migration, no DB roles, and
no implementation exist. The repository exists solely as the designated
future Governance implementation owner. No claim of Stage 1 implementation
is made by this Decision.

## 4. Identity & Authority Boundary (→ ACR-022)

```text
Canonical Actor          != Authentication Principal
Canonical Actor          != Service Identity
Canonical Actor          != Database Role
```

- **Canonical Actor** — durable, accountable, semantic identity (atlas-core).
- **Authentication Principal** — authenticated request/session identity.
- **Service Identity** — durable, non-human, operational identity.
- **Authorization Evaluator** — a Canonical Actor acting in evaluator
  capacity for a Policy Decision.
- **Database Role** — PostgreSQL privilege identity only; never implies
  Actor identity or policy authority.

Mappings: Principal → Actor; Service Identity → Actor; Service Identity →
external credential (1:N); Request Context → Principal; Policy Decision →
evaluator Actor. `initiator_actor_id` and `decision_evaluator_actor_id`
remain Canonical Actor IDs. Credential material is never stored in Actor
records or Governance epistemic history.

Stage 1 DB-role strategy: one `atlas_app_role` (application/domain
governed mutations), one separate `auth_service_role` (authentication
lifecycle only).

## 5. API / Domain Integration Contract (→ ACR-023)

Stage 1 integration architecture: **HYBRID**.

| Operation | Synchrony |
|---|---|
| Factual Projection | ASYNC |
| Epistemic Proposal | ASYNC |
| Governed Action Request | SYNC |
| Outcome Submission | ASYNC |
| Reconciliation | ASYNC / on-demand |

Core invariant: `Domain factual ingestion != Governance runtime availability`.

Mutating requests: caller-generated `integration_request_id`; uniqueness
scope `(service_identity_id, integration_request_id)`; `payload_digest`
required. Same ID + same digest = same logical request (idempotent replay).
Same ID + different digest = `IDEMPOTENCY_CONFLICT`.

Canonical references are ID-only by default; an optional historical
snapshot may be retained but never replaces Core as source of truth. Direct
Domain→Governance DB writes: **PROHIBITED**; Domain registration is
required before integration. High-impact governed actions are synchronous.
Audit failure blocks the governed mutation transaction (atomicity).

## 6. Physical Schema Design (→ ACR-024)

Primary schema: `atlas_governance`. Table count: **25**.

1. service_identities
2. authentication_principals
3. identity_actor_mappings
4. authenticated_request_contexts
5. domain_registrations
6. domain_registration_operation_classes
7. integration_requests
8. policy_decisions
9. epistemic_nodes
10. epistemic_evidence_links
11. epistemic_observation_links
12. epistemic_relations
13. epistemic_revisions
14. epistemic_status_events
15. evidence_snapshots
16. evidence_snapshot_items
17. artifact_tombstones
18. model_runs
19. disagreement_aggregations
20. proposals
21. permits
22. decision_outcomes
23. audit_chain_heads
24. audit_events
25. domain_reconciliation_states

Fixed schema decisions: Governance-native PKs UUID by default; Canonical
references TEXT; no Governance→Core physical FK; TIMESTAMPTZ for all
timestamps; PostgreSQL ENUM not used; closed vocabularies are
CHECK-constrained TEXT; hard DELETE is prohibited on the runtime path;
`epistemic_nodes.current_status` is a stored cache only, status-event
history is authoritative; evidence snapshots are historical-context-only,
raw snapshot content is not stored by default; permits are one-time in
Stage 1; the audit hash chain is scoped per service; `decision_outcomes`
and `domain_reconciliation_states` are dedicated tables.

## 7. DB Role / SECURITY DEFINER Boundary (→ ACR-025)

```text
atlas_governance_owner     = NOLOGIN owner
atlas_governance_migrator  = administrative LOGIN migration identity
auth_service_role          = runtime auth role
atlas_app_role             = runtime app role
```

Runtime direct DML — both `auth_service_role` and `atlas_app_role`:
INSERT NO / UPDATE NO / DELETE NO. All runtime mutation is
function-mediated.

SECURITY DEFINER invariants: hardened `search_path` required; `PUBLIC`
EXECUTE revoked; owner is non-superuser/non-runtime; caller identity is
derived from stored request context, never from DB role; no runtime
upward `SET ROLE`; no direct runtime EXECUTE on the audit-append internal
function; audit mutation is atomic with the governed change it records.

Additional invariants: Validated/Rejected/Superseded epistemic status
transitions require an associated Policy Decision. Permit issuance is
function-only. Permit consumption is concurrency-safe. A consumed permit
is terminal and cannot later be revoked. Domain registration scope change
preserves history via a replacement record, not in-place mutation.
`atlas_governance_owner`/`atlas_governance_migrator` remain a trusted
administrative root boundary, technically privileged outside runtime
restrictions by design.

## 8. Migration Architecture & Function Inventory (→ ACR-026)

Migration architecture: **MULTIPLE DEPENDENCY-BOUNDED REVISIONS**.

Infrastructure boundary: DB creation outside Alembic; role creation
outside Alembic; schema creation inside Alembic.

Conceptual sequence: B001 (Infrastructure/DB provisioning, non-Alembic) →
B002 (Role Bootstrap, non-Alembic) → M001–M014 (Alembic chain: schema →
identity tables → domain/integration tables → epistemic core → policy/
permit → epistemic status events → snapshot/tombstone/outcome → audit
infrastructure → reconciliation state → functions grouped by
dependency/security family → runtime grants/revokes → verification/
lockdown). Runtime is enabled only after the final verification/lockdown
gate passes.

**Database ownership boundary** (clarification added 2026-08-19, task
AH-CGR-010A1, following empirical PostgreSQL 16.15 execution findings in
AH-CGR-010/AH-CGR-010A/AH-CGR-010A0 — not present in the original ACR-026
canonicalization): B001 provisions the PostgreSQL database under the
infrastructure/admin identity. B002 creates the four approved Governance
DB roles and, as its final administrative handoff step, transfers
ownership of the target database to `atlas_governance_owner`. M001
remains responsible for creating schema `atlas_governance`, owned by
`atlas_governance_owner` — this does not change.

Final target PostgreSQL database owner: `atlas_governance_owner`.
`atlas_governance_migrator` derives its required database-level `CREATE`
capability (needed for `CREATE SCHEMA` in M001) from its existing
inheritable membership in `atlas_governance_owner`, once
`atlas_governance_owner` owns the database — no standalone
`CREATE ON DATABASE` grant is required. The same mechanism, via the
dynamic `pg_database_owner` pseudo-role that owns the `public` schema,
gives the migrator `CREATE` on `public` without any standalone
`CREATE ON SCHEMA public` grant either. `PUBLIC`, `auth_service_role`, and
`atlas_app_role` remain unable to create anything in `public`.

The Alembic version table, `public.alembic_version`, is migration
metadata, not Governance runtime data, and is the one approved
administrative relation permitted in `public`; it is not counted among
the 25 Stage 1 tables. `atlas_governance_owner` remains the NOLOGIN
administrative/object owner and `atlas_governance_migrator` remains the
LOGIN migration executor — the migrator is never made database owner
directly, preserving the owner/executor separation.

Empirically verified on PostgreSQL 16.15 (AH-CGR-010A0): before the
ownership transfer, migrator database-CREATE and public-CREATE were both
`FALSE`; after `ALTER DATABASE ... OWNER TO atlas_governance_owner`, both
became `TRUE`; rollback-wrapped probes of `CREATE TABLE` in `public` and
`CREATE SCHEMA ... AUTHORIZATION atlas_governance_owner`, both executed as
`atlas_governance_migrator`, both succeeded and left no permanent trace.

Production data protection: destructive downgrade of data-bearing tables
is prohibited; forward-fix is preferred once historical data exists.
Governance runtime audit (`audit_events`) is distinct from
migration/deployment audit (administrative operational history) — never
conflated. No business seed data is included in migrations.

Function inventory:

```text
Stage 1 SECURITY DEFINER functions: 32
Externally callable:                31
Internal-only:                      1
```

| Family | Functions | Role |
|---|---|---|
| Auth | `create_authentication_principal`, `create_authenticated_request_context` | auth_service_role |
| Identity | `register_service_identity`, `deactivate_service_identity`, `remap_identity_actor_mapping` | atlas_app_role |
| Domain | `register_domain`, `revoke_domain_registration`, `change_domain_operation_scope` | atlas_app_role |
| Integration | `begin_integration_request`, `complete_integration_request` | atlas_app_role |
| Epistemic | `create_epistemic_node`, `add_epistemic_revision`, `transition_epistemic_status`, `add_evidence_link`, `add_observation_link`, `add_epistemic_relation` | atlas_app_role |
| Proposal | `submit_proposal`, `accept_proposal`, `reject_proposal` | atlas_app_role |
| Policy | `record_policy_decision` | atlas_app_role |
| Permit | `issue_permit`, `consume_permit`, `revoke_permit` | atlas_app_role |
| Snapshot | `create_evidence_snapshot` | atlas_app_role |
| Tombstone | `record_artifact_tombstone` | atlas_app_role |
| Outcome | `record_decision_outcome` | atlas_app_role |
| Model | `begin_model_run`, `complete_model_run` | atlas_app_role |
| Disagreement | `create_disagreement_aggregation`, `update_disagreement_resolution` | atlas_app_role |
| Reconciliation | `update_domain_reconciliation_state` | atlas_app_role |
| Internal | `append_audit_event` | none (internal-only) |

Grant counts: `auth_service_role` → 2; `atlas_app_role` → 29;
`append_audit_event` → runtime EXECUTE none.

## 9. First-Root Service Identity Bootstrap (→ ACR-027)

Selected architecture: **Option B modified** — reuse the existing approved
`register_service_identity` function; no new permanent DB role, table, or
SECURITY DEFINER function. Bootstrap executor: `atlas_governance_migrator`,
via its existing capability to assume/inherit `atlas_governance_owner`
authority. Bootstrap occurs strictly **after M014**.

First-bootstrap exception: no normal Request Context is used; the ceremony
accepts an externally-established Canonical Actor ID; production requires
explicit human approval; `request_context_id` may be `NULL` only while
`service_identities` is empty, evaluated under a concurrency-safe guard;
Service Identity creation, `audit_chain_head` initialization, and the
`BOOTSTRAP_SERVICE_IDENTITY` audit event are committed atomically; any
failure rolls back the entire transaction; a successful bootstrap without
its audit event is prohibited by the approved function path; after the
first successful identity, the bootstrap exception structurally and
permanently closes. All later Service Identities use the fully normal
governed `register_service_identity` path.

`bootstrap_operation_id`: required, purpose is **traceability only** (not
a strict idempotency/replay key). Strict request idempotency: **NO**.
Retry safety: **YES** (via atomicity + the empty-table guard). Unknown
outcome after an ambiguous invocation requires read-only state
verification before any retry decision.

Function count impact: **none** — remains 32.

---

## Cross-Reference Index

| Ledger Entry | Source Design Chain |
|---|---|
| ACR-019 | AH-CGR-001 |
| ACR-020 | AH-CGR-002 |
| ACR-021 | AH-CGR-003 |
| ACR-022 | AH-CGR-004 |
| ACR-023 | AH-CGR-005 |
| ACR-024 | AH-CGR-006 |
| ACR-025 | AH-CGR-007, AH-CGR-007A |
| ACR-026 | AH-CGR-008, AH-CGR-008A |
| ACR-027 | AH-CGR-008B, AH-CGR-008B1 |
