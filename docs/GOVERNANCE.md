# Atlas Core Governance

## Observation and Interpretation

Observation and Interpretation are separate concerns.

Observed facts must not be silently replaced by inferred meaning.

## Append-only Decision Ledger

Approved Decisions are recorded append-only.

Existing Decision records are not silently overwritten or deleted. A later Decision may supersede an earlier Decision while preserving the earlier record.

## Revision model

Hypothesis and Knowledge evolve through additional Revisions rather than silent replacement.

## Domain independence

Atlas Core is domain-independent.

Video, Global Intelligence, real estate, and other domains remain separate Domain Applications.

Domain-specific assumptions must not be introduced into Atlas Core without an approved Decision and Implementation Task.

## AI provider independence

An AI provider is a replaceable inference component.

Atlas Core must not be designed around one provider without explicit approval.

No AI provider implementation is authorized by ACI-001.

## Status separation

The following statuses are distinct:

- Proposal
- Approved
- Implemented
- Verified

Approval does not mean implementation.

Implementation does not mean verification.

## Room authority separation

The Design and Decision Room owns architecture and design decisions.

The Implementation Room executes approved Implementation Tasks within their authorized scope.

The Implementation Room must not independently make architecture, Entity, database, migration, API, security, or repository-boundary decisions.

## Stop conditions

Implementation must stop when:

- Required authorization is missing
- Approved scope would be exceeded
- Architecture or Entity decisions are required
- Database, migration, or API changes are required without approval
- Existing work would need to be overwritten or discarded
- Secret information would need to be exposed
- Acceptance criteria cannot be met

## Decision Request

A Decision Request must include:

1. Confirmed facts
2. The decision required
3. Available options
4. Impact of each option
5. Recommended option and rationale
6. Scope that remains unchanged
