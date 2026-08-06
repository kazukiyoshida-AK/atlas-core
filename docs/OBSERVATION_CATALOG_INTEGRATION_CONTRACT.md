# Atlas Core Observation Catalog Integration Contract v0.1

```text
Decision basis: ACR-015
Status: Approved
Version: 0.1
Approved date: 2026-08-06
```

This document is a normative Atlas Core contract. It is standalone: it
is not a Canonical Model, not a Core dataclass, not a Core database
table, not a shared JSON Schema, and not a Domain migration. The key
words MUST, MUST NOT, SHOULD, and MAY are used with their normal
meaning — MUST/MUST NOT are hard requirements, SHOULD is a strong
recommendation with room for a documented exception, MAY is optional.

## 1. Purpose

This Contract defines how a Domain-owned Observation Catalog
integrates with existing Atlas Core Canonical identities, without the
Catalog itself becoming a Canonical Model. It exists because the
current Canonical Model layer (Observation, Evidence, Provenance,
Source, Actor, AIModel, ExecutionSpecification, PromptSpecification,
ConfigurationSpecification, ExternalRun, Artifact, ExternalResource)
is conditionally closed and structurally sufficient to support Catalog
integration, but supplies no first-class Catalog concept of its own.
A Domain that wants Atlas Core-level identity, replay, and audit
guarantees over its own Catalog of Observation definitions MUST
conform to this Contract; a Domain that never adopts it is unaffected.

## 2. Scope

In scope:

* Catalog entry identity
* semantic revision identity
* retained definition
* production binding
* Provenance integration
* replay/audit obligations
* lifecycle boundary
* Domain adoption

Out of scope:

* shared Catalog schema
* global registry
* unit registry
* scheduler
* resource allocator
* extractor implementation
* Domain migration
* Catalog service

## 3. Terminology

```text
Catalog:
A Domain-owned collection of Catalog entries.

Catalog entry:
A Domain-owned, stably identified definition of one class of
observable fact (e.g. one metric, one indicator, one measurement
type).

Catalog entry revision:
One immutable semantic definition of a Catalog entry at a point in
time. A Catalog entry may accumulate many revisions over time; each
revision is immutable once it has been used to produce a Canonical
Observation.

definition Artifact:
The Canonical Artifact that retains the exact content of one Catalog
entry revision's definition.

Catalog production binding:
The immutable Domain-owned record asserting that one Provenance
activity applied one Catalog entry revision to govern one declared
observation_kind.

observation_kind:
The declared class of Canonical Observation output governed by a
Catalog entry revision (e.g. "numeric", "categorical", "verification").

semantic revision:
A Catalog entry revision change that alters meaning, unit, value
interpretation, applicability, normalization, or validation semantics.

execution revision:
A change to the reusable code that implements extraction or
measurement (ExecutionSpecification), without a change in meaning.

configuration revision:
A change to reusable runtime parameters (ConfigurationSpecification),
without a change in meaning.

lifecycle state:
A Domain-owned, mutable classification of a Catalog entry or revision
(e.g. draft, active, deprecated). Never part of an immutable
production binding.

definition_selector:
An immutable, deterministic Domain-owned value that resolves exactly
one Catalog entry revision inside a definition Artifact that bundles
more than one revision.
```

## 4. Ownership

* The Catalog MUST be Domain-owned.
* Catalog entry identity MUST be Domain-owned.
* Catalog entry revision identity MUST be Domain-owned.
* Catalog definition content MUST be Domain-owned.
* Catalog lifecycle MUST be Domain-owned.
* Atlas Core supplies integration identities only (Provenance,
  Artifact, and the other eleven Canonical Models); it does not own,
  mint, or store any Catalog identity.

## 5. Normative production binding

A conforming Domain MUST retain, for every Catalog entry revision used
to produce a Canonical Observation, an immutable production binding
with the following fields:

```text
catalog_entry_id           MUST
catalog_entry_revision_id  MUST
definition_artifact_id     MUST
provenance_id               MUST
observation_kind            MUST
recorded_at                  MUST
definition_selector         Conditional
```

`definition_selector` MUST be present when `definition_artifact_id`
references an Artifact that contains more than one Catalog entry
revision; it MUST be absent or ignored otherwise.

This binding is a normative Domain-owned shape. It is NOT a Core
dataclass, NOT a shared database table, and NOT a Canonical Model. A
Domain MAY implement it as a database row, an immutable log record, or
any other Domain-local mechanism, provided the invariants in §6 hold.

## 6. Binding invariants

1. `catalog_entry_id` MUST be stable within its owning Domain.
2. `catalog_entry_revision_id` MUST identify exactly one immutable
   semantic revision.
3. `definition_artifact_id` MUST reference a Canonical Artifact that
   preserves the exact semantic definition of that revision.
4. `provenance_id` MUST identify the Provenance activity that applied
   the revision.
5. `observation_kind` MUST identify the declared Canonical Observation
   output class governed by the binding.
6. Binding records MUST be immutable once written.
7. A binding MUST NOT contain complete definition content — only a
   reference to it.
8. A binding MUST NOT contain mutable lifecycle state.
9. A binding MUST NOT duplicate fields already held by Provenance
   (execution_ref, configuration_ref, prompt_ref, model_ref,
   external_run_ref).
10. Raw Domain Catalog IDs MUST NOT be inserted into Core
    `Provenance.input_refs`.
11. Within one Provenance activity, one `observation_kind` MUST
    resolve to exactly one Catalog production binding.
12. If a single Provenance activity would otherwise need to apply two
    different Catalog entry revisions to the same `observation_kind`,
    the Domain MUST either record separate Provenance activities, or
    retain explicit `output_observation_ids` in a Domain-local binding
    extension. This Contract does not claim exact per-Observation
    reverse auditability when neither is done.
13. No generic subject/predicate/object representation is used for
    the binding.

## 7. Definition Artifact policy

* Every production-used Catalog entry revision MUST have an exact
  retained definition Artifact.
* A Domain SHOULD use one definition Artifact per Catalog entry
  revision as the default representation.
* A bundled Artifact containing multiple entries or revisions MAY be
  used only when the production binding retains an immutable,
  deterministic `definition_selector` that resolves exactly one
  revision inside it.
* This Contract does not define a universal selector syntax;
  `definition_selector` syntax is Domain-owned but MUST remain
  deterministic and interpretable together with the retained Artifact.
* Canonical Artifact identity alone does NOT guarantee that the
  underlying bytes remain physically available forever, and does NOT
  guarantee that byte-level integrity has been verified.
* A definition Artifact is NOT the Catalog entry identity, NOT the
  Catalog revision identity, NOT an execution identity, NOT the
  production activity, and NOT Evidence by default.

## 8. Semantic definition content

The retained definition (in the Artifact referenced by
`definition_artifact_id`) MUST preserve:

```text
observation meaning
value interpretation
value type
unit or explicit unitless status
nullability and unknown behavior
applicability
normalization semantics
validation semantics
non-scalar representation policy
```

No Core unit registry or closed Core type enum is introduced by this
Contract; these obligations are satisfied entirely within Domain-owned
definition content.

## 9. Provenance integration

Execution-related identity remains conditional on the existing
Provenance references:

```text
Provenance.execution_ref
Provenance.configuration_ref
Provenance.prompt_ref
Provenance.model_ref
Provenance.external_run_ref
Provenance.input_refs
```

Only approved Canonical IDs (Artifact, Observation, Evidence, Source,
ExternalResource, under existing approved semantics) MAY appear in
`Provenance.input_refs`. A definition Artifact's `artifact_id` MAY
appear in `input_refs` when that Artifact was materially consumed by,
or governed, the activity under existing approved semantics. Raw
Domain Catalog IDs MUST NOT appear in `input_refs` under any
circumstance.

## 10. Observation production obligations

A conforming Domain MUST ensure, for every Observation produced under
this Contract:

* the Domain Catalog entry identity exists
* the Domain Catalog entry revision identity exists
* the exact definition revision is durably retained
* the definition Artifact identity is known
* the producing Provenance identity is known
* `Observation.provenance_ref` matches that Provenance
* the Observation kind matches the definition
* failed validation does not produce a false Observation
* historical semantic interpretation remains possible for as long as
  the definition Artifact and binding are retained

## 11. Observation-to-binding uniqueness

```text
Within one Provenance activity, one observation_kind MUST resolve to
exactly one Catalog production binding.
```

When a Domain cannot satisfy this invariant for a given activity, it
MUST fall back to one of:

```text
recording separate Provenance activities
or
retaining explicit output_observation_ids in a Domain-local binding
extension
```

This Contract does not mandate `output_observation_ids` as a baseline
field; it is required only as the fallback above.

## 12. Replay and audit levels

```text
Identity replay:
Which Catalog entry and revision governed this Observation? Supported
after Contract adoption through the retained Domain production
binding.

Semantic replay:
What did that revision mean? Supported after Contract adoption through
the retained exact definition Artifact.

Execution replay:
Which execution, configuration, prompt, model, and external run were
used? Partially supported through Provenance's existing conditional
references; also requires Domain code, dependency, and environment
availability.

Audit-only traceability:
Can Atlas prove which retained identities and definitions were claimed
to govern the activity? Available only after Contract adoption and
conforming retention.

Reproduction:
Byte-for-byte reproduction of the original result is NOT guaranteed by
this Contract.
```

## 13. Execution and configuration

```text
ExecutionSpecification:
Reusable extraction, parsing, normalization, measurement, or
validation implementation identity.

ConfigurationSpecification:
Reusable runtime parameter selection: threshold, applicability filter,
enabled entry set, depth selection, or resource-budget selection.
```

Catalog semantic meaning is neither of these. A change to
implementation without a change to meaning is an ExecutionSpecification
revision only. A change to meaning — even from a small code edit —
REQUIRES a new Catalog semantic revision.

## 14. Prompt and AI model

Separate concerns:

```text
Catalog semantic definition — independent of any prompt or model
PromptSpecification — reusable prompt identity
rendered prompt Artifact — the actual text sent for one activity
AIModel — reusable model identity
ExternalRun — the actual inference invocation
Provenance — links execution/configuration/prompt/model/external-run
             refs for one activity
Observation — the produced fact
```

A prompt or model change creates a new Catalog semantic revision only
when it changes meaning, unit, value type, applicability,
normalization, or validation semantics. Otherwise it is an
execution-layer change only, captured by a new PromptSpecification or
AIModel reference on Provenance under the same
`catalog_entry_revision_id`.

## 15. Source and ExternalResource applicability

* Source *kind* and ExternalResource *kind* applicability belong in
  definition content, and MAY be mirrored in ConfigurationSpecification
  for runtime filtering.
* Specific Source and ExternalResource *identities* are runtime facts;
  they belong to `Provenance.input_refs` under existing approved
  semantics when materially consumed, or to Domain-local runtime data.
  They MUST NOT be embedded in the Catalog production binding.
* Source is NOT automatically the Catalog owner.
* ExternalResource is NOT automatically the observed object.

## 16. Evidence boundary

```text
Catalog definitions, extraction procedures, and validation rules are
NOT Evidence merely because they govern Observation production.
```

A validation report MAY be classified as an Artifact, as Evidence, or
as Domain-only, depending on whether it independently supports the
correctness of the Observation for a downstream consumer. This
Contract does not modify the Evidence Model.

## 17. Lifecycle

* Catalog lifecycle (draft, active, experimental, disabled, deprecated,
  retired, superseded, unknown) is Domain-owned.
* Lifecycle changes MUST NOT mutate historical production bindings.
* Deprecation MUST NOT invalidate historical Observations.
* Deprecated or retired revisions MUST remain semantically resolvable
  for as long as their definition Artifact and bindings are retained.
* Lifecycle state MUST NOT be copied into a production binding.

## 18. Multi-depth processing

For fast/deep/verification-style processing depth:

* depth normally changes ExecutionSpecification and/or
  ConfigurationSpecification identity, not the semantic Catalog
  revision.
* a new semantic revision is required only when meaning, unit, value
  interpretation, applicability, normalization, or validation
  semantics change — not merely because execution intensity changed.
* verification output MAY be a new immutable Observation (when it
  re-affirms or corrects an asserted fact) or a validation Artifact
  with no new Observation (when it only produces supporting material);
  which applies is a Domain- and entry-specific determination.

## 19. Non-scalar outputs

For vectors, embeddings, bounding boxes, time series, structured
objects, large text, images, audio segments, and video segments:

* the complete value MAY be retained as an Artifact or a Domain
  record.
* the Canonical Observation retains the normalized assertion or
  summary that its existing fields can validly express.
* Atlas Core currently has NO dedicated Observation-to-output-Artifact
  reference.
* exact linkage from one Observation to one non-scalar output Artifact
  remains a Domain-local mapping when it must be preserved.
* this is a known, non-blocking limitation. It does not approve or
  reopen the deferred Provenance–Artifact Output Relationship, the
  deferred Evidence–Artifact Relationship, a generic Relationship, or
  a new Observation field.

## 20. Domain adoption

Adoption under this Contract is additive and optional for every
Domain. No migration is authorized by this Contract.

```text
atlas-global-intelligence:
Indicator.code is a plausible Domain entry identity. Existing
adapter/normalization code maps to ExecutionSpecification candidates.
Existing Observation.indicator_id remains the Domain-local output
mapping.

ai-video-tracker:
Current fixed VideoAIAnalysis output fields are plausible initial
entry candidates if adopted. Future fine-grained definitions, and
Prompt/AIModel/Execution bindings, remain design-only until adopted.

atlas-x-engine:
Individual hardcoded, duplicated metrics are plausible entry
candidates; adoption would consolidate currently duplicated
definitions rather than change behavior.

etsy-analyzer:
Existing scoring features are Domain analysis logic and are NOT
automatically Catalog entries or Canonical Observations. They become
Catalog entry candidates only if the Domain later explicitly
classifies their outputs as observations governed by this Contract.
```

## 21. Conformance

A Domain conforms to this Contract only when all of the following
hold:

* the required production binding fields (§5) exist for every
  Catalog-governed Observation
* the exact revision definition is retained via a definition Artifact
* the uniqueness invariant (§11) holds, or its fallback is recorded
* raw Domain Catalog IDs are not placed in `Provenance.input_refs`
* historical semantic interpretation remains possible for retained
  bindings and definitions
* historical bindings are preserved immutably regardless of lifecycle
  changes

## 22. Known limitations

* Atlas Core does not enforce Domain binding correctness; conformance
  is a Domain responsibility.
* There is no global Catalog ID namespace across Domains or
  repositories.
* There is no guarantee of physical Artifact byte availability.
* There is no guarantee of byte-for-byte reproduction.
* Non-scalar output Artifact linkage remains Domain-local.
* Catalog aliasing, split/merge, and supersession remain Domain
  concerns; this Contract does not formalize them.

## 23. Prohibited interpretations

This Contract explicitly prohibits treating:

* Artifact as Catalog identity
* ConfigurationSpecification as Catalog semantic definition
* ExecutionSpecification as Catalog semantic definition
* Source as the Catalog owner
* ExternalResource as automatically being the observed object
* a Catalog definition as Evidence by default
* Core Specification IDs (Execution/Configuration/Prompt/Model) as a
  substitute for Catalog entry revision identity
