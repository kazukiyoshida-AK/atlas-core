from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from atlas_core import Provenance, PromptSpecification


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 4,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "prompt_specification_id": "prompt-spec:article-summarization-v1",
        "prompt_kind": "message_bundle",
        "canonical_name": "Article Summarization Prompt prompt-v1",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_prompt_specification_can_be_created() -> None:
    arguments = _valid_arguments()

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.prompt_specification_id == (
        "prompt-spec:article-summarization-v1"
    )
    assert prompt_specification.prompt_kind == "message_bundle"
    assert prompt_specification.canonical_name == (
        "Article Summarization Prompt prompt-v1"
    )
    assert prompt_specification.recorded_at == arguments["recorded_at"]


def test_prompt_specification_is_exported_from_package_root() -> None:
    from atlas_core.prompt_specification import (
        PromptSpecification as ModulePromptSpecification,
    )

    assert PromptSpecification is ModulePromptSpecification


def test_prompt_specification_is_immutable() -> None:
    prompt_specification = PromptSpecification(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        prompt_specification.canonical_name = "changed"  # type: ignore[misc]


def test_prompt_specification_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        PromptSpecification(*arguments.values())  # type: ignore[misc]


def test_prompt_specification_has_slots() -> None:
    prompt_specification = PromptSpecification(**_valid_arguments())

    assert not hasattr(prompt_specification, "__dict__")


def test_prompt_specification_has_exact_approved_field_set_and_order() -> None:
    field_names = tuple(field.name for field in fields(PromptSpecification))

    assert field_names == (
        "prompt_specification_id",
        "prompt_kind",
        "canonical_name",
        "recorded_at",
    )


def test_prompt_specification_field_count_is_four() -> None:
    assert len(fields(PromptSpecification)) == 4


def test_all_fields_are_required() -> None:
    for field in fields(PromptSpecification):
        assert field.default is MISSING
        assert field.default_factory is MISSING  # type: ignore[misc]


def test_prompt_specification_module_imports_only_standard_library() -> None:
    import ast
    import inspect

    import atlas_core.prompt_specification as prompt_specification_module

    source = inspect.getsource(prompt_specification_module)
    tree = ast.parse(source)

    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.add(node.module)

    prohibited_modules = {
        "atlas_core.actor",
        "atlas_core.ai_model",
        "atlas_core.evidence",
        "atlas_core.execution_specification",
        "atlas_core.observation",
        "atlas_core.provenance",
        "atlas_core.source",
    }

    assert imported_modules.isdisjoint(prohibited_modules)

    for module_name in imported_modules:
        assert module_name in {"__future__", "dataclasses", "datetime"}


# --- Required strings ---


@pytest.mark.parametrize(
    "field_name",
    ("prompt_specification_id", "prompt_kind", "canonical_name"),
)
@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        " ",
        " leading",
        "trailing ",
    ),
)
def test_required_strings_reject_invalid_values(
    field_name: str,
    invalid_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(ValueError):
        PromptSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("prompt_specification_id", "prompt_kind", "canonical_name"),
)
@pytest.mark.parametrize("invalid_value", (123, None, [], {}))
def test_required_strings_reject_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        PromptSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("prompt_specification_id", "prompt_kind", "canonical_name"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        PromptSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("prompt_specification_id", "prompt_kind", "canonical_name"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    prompt_specification = PromptSpecification(**arguments)

    assert getattr(prompt_specification, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_canonical_name = " Article Summarization Prompt prompt-v1"

    arguments = _valid_arguments()
    arguments["canonical_name"] = original_canonical_name

    with pytest.raises(ValueError):
        PromptSpecification(**arguments)

    assert arguments["canonical_name"] == original_canonical_name


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.prompt_specification as prompt_specification_module

    source = inspect.getsource(prompt_specification_module)

    assert "object.__setattr__" not in source


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    non_utc = datetime(2026, 8, 4, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 4, 10)

    with pytest.raises(ValueError):
        PromptSpecification(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-04T10:00:00Z"

    with pytest.raises(TypeError):
        PromptSpecification(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        PromptSpecification(**arguments)


# --- prompt_kind: structural axis only, extensible, no closed enum ---


@pytest.mark.parametrize(
    "recommended_kind",
    (
        "instruction",
        "message_template",
        "message_bundle",
        "unknown",
    ),
)
def test_recommended_prompt_kind_values_are_accepted(recommended_kind: str) -> None:
    arguments = _valid_arguments()
    arguments["prompt_kind"] = recommended_kind

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.prompt_kind == recommended_kind


def test_custom_structural_prompt_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["prompt_kind"] = "custom_structural_kind"

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.prompt_kind == "custom_structural_kind"


def test_prompt_kind_is_not_a_closed_enum() -> None:
    arguments = _valid_arguments()
    arguments["prompt_kind"] = "domain_local_experimental_kind"

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.prompt_kind == "domain_local_experimental_kind"


@pytest.mark.parametrize(
    "role_or_purpose_value",
    (
        "system",
        "developer",
        "user",
        "summarization",
        "classification",
        "routing",
        "extraction",
        "generation",
        "analysis",
        "evaluation",
    ),
)
def test_role_and_purpose_strings_remain_technically_constructible(
    role_or_purpose_value: str,
) -> None:
    # ACR-009: system/developer/user (role) and summarization/
    # classification/etc. (functional purpose) are excluded from the
    # RECOMMENDED prompt_kind vocabulary because prompt_kind's single
    # axis is structural architecture, not role or purpose. Core does
    # not runtime-enforce vocabulary membership, so these strings are
    # not rejected — the exclusion is governance, not validation.
    arguments = _valid_arguments()
    arguments["prompt_kind"] = role_or_purpose_value

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.prompt_kind == role_or_purpose_value


# --- canonical_name / revision-distinguishable identity ---


def test_duplicate_canonical_name_is_permitted_across_distinct_records() -> None:
    arguments_a = _valid_arguments()
    arguments_a["prompt_specification_id"] = "prompt-spec:a"
    arguments_a["canonical_name"] = "Shared Label"

    arguments_b = _valid_arguments()
    arguments_b["prompt_specification_id"] = "prompt-spec:b"
    arguments_b["canonical_name"] = "Shared Label"

    prompt_specification_a = PromptSpecification(**arguments_a)
    prompt_specification_b = PromptSpecification(**arguments_b)

    assert (
        prompt_specification_a.canonical_name
        == prompt_specification_b.canonical_name
    )
    assert (
        prompt_specification_a.prompt_specification_id
        != prompt_specification_b.prompt_specification_id
    )


def test_canonical_name_is_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["canonical_name"] = "Routing Classification Prompt routing-classify-v1"

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.canonical_name == (
        "Routing Classification Prompt routing-classify-v1"
    )


def test_revision_qualified_canonical_name_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["canonical_name"] = "Article Summarization Prompt prompt-v1"

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.canonical_name == (
        "Article Summarization Prompt prompt-v1"
    )


@pytest.mark.parametrize(
    "mutable_alias",
    ("production", "latest", "default", "current"),
)
def test_mutable_alias_strings_remain_technically_constructible(
    mutable_alias: str,
) -> None:
    # ACR-009 §16/§19: a mutable alias alone is insufficient for the
    # semantic Known-identity Admission Rule, but that is a governance
    # rule evaluated at minting time, not a Core runtime constraint —
    # Core only enforces string shape.
    arguments = _valid_arguments()
    arguments["canonical_name"] = mutable_alias

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.canonical_name == mutable_alias


def test_arbitrary_opaque_prompt_specification_id_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["prompt_specification_id"] = "01HZY3K9G8N7Q2R5T6V8W0X1Y2"

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.prompt_specification_id == (
        "01HZY3K9G8N7Q2R5T6V8W0X1Y2"
    )


def test_no_required_id_prefix_is_enforced() -> None:
    arguments = _valid_arguments()
    arguments["prompt_specification_id"] = "just-any-non-empty-string"

    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.prompt_specification_id == (
        "just-any-non-empty-string"
    )


def test_a_materially_revised_prompt_is_a_new_independent_record() -> None:
    revision_one = PromptSpecification(
        prompt_specification_id="prompt-spec:article-summarization-v1",
        prompt_kind="message_bundle",
        canonical_name="Article Summarization Prompt prompt-v1",
        recorded_at=_aware_datetime(),
    )
    revision_two = PromptSpecification(
        prompt_specification_id="prompt-spec:article-summarization-v2",
        prompt_kind="message_bundle",
        canonical_name="Article Summarization Prompt prompt-v2",
        recorded_at=_aware_datetime(),
    )

    # No field links the two records — a materially distinct revision
    # is an entirely new, independent identity, never a mutation.
    assert revision_one.prompt_specification_id != (
        revision_two.prompt_specification_id
    )
    assert revision_one.canonical_name != revision_two.canonical_name


def test_frozen_dataclass_equality_is_ordinary_value_equality() -> None:
    arguments = _valid_arguments()

    first = PromptSpecification(**arguments)
    second = PromptSpecification(**arguments)

    # Ordinary dataclass value equality only — Core performs no
    # identity-merging, no deduplication, and no semantic comparison
    # beyond what @dataclass(frozen=True) provides by default.
    assert first == second
    assert first is not second


# --- Known, Confidential Known, Unknown examples ---


def test_known_message_bundle_example() -> None:
    prompt_specification = PromptSpecification(
        prompt_specification_id="prompt-spec:routing-classify-v1",
        prompt_kind="message_bundle",
        canonical_name="Routing Classification Prompt routing-classify-v1",
        recorded_at=_aware_datetime(),
    )

    assert prompt_specification.prompt_kind == "message_bundle"


def test_known_instruction_example() -> None:
    prompt_specification = PromptSpecification(
        prompt_specification_id="prompt-spec:etsy-analysis-instruction-v1",
        prompt_kind="instruction",
        canonical_name="Etsy Analysis Instruction v1",
        recorded_at=_aware_datetime(),
    )

    assert prompt_specification.prompt_kind == "instruction"


def test_confidential_known_prompt_uses_sanitized_canonical_name() -> None:
    # ACR-009 §18.3: withheld/confidential content alone does not force
    # Unknown classification when revision-distinguishable identity is
    # known. No content field exists on this model regardless.
    prompt_specification = PromptSpecification(
        prompt_specification_id="prompt-spec:confidential:9d4e2f8a1c73",
        prompt_kind="message_bundle",
        canonical_name="confidential-internal-prompt-9d4e2f8a1c73",
        recorded_at=_aware_datetime(),
    )

    assert prompt_specification.canonical_name == (
        "confidential-internal-prompt-9d4e2f8a1c73"
    )


def test_unknown_prompt_specification_is_accepted_as_complete_record() -> None:
    prompt_specification = PromptSpecification(
        prompt_specification_id="prompt-spec:unknown:3e9b7f1a5c82",
        prompt_kind="unknown",
        canonical_name="Unknown Prompt Specification 3e9b7f1a5c82",
        recorded_at=_aware_datetime(),
    )

    assert prompt_specification.prompt_kind == "unknown"
    assert prompt_specification.canonical_name == (
        "Unknown Prompt Specification 3e9b7f1a5c82"
    )


def test_empty_identifiers_remain_rejected_for_unknown_records() -> None:
    arguments = _valid_arguments()
    arguments["prompt_kind"] = "unknown"
    arguments["canonical_name"] = ""

    with pytest.raises(ValueError):
        PromptSpecification(**arguments)


# --- Content-free model ---


def test_prompt_specification_has_no_content_fields() -> None:
    field_names = {field.name for field in fields(PromptSpecification)}

    content_fields = {
        "template_text",
        "content",
        "messages",
        "message_template",
        "system_template",
        "developer_template",
        "user_template",
        "few_shot_examples",
        "variable_schema",
        "output_schema",
        "content_hash",
        "language",
        "raw_payload",
        "personal_information",
        "secret",
        "credential",
    }

    assert field_names.isdisjoint(content_fields)


def test_message_template_is_a_prompt_kind_value_not_a_field() -> None:
    field_names = {field.name for field in fields(PromptSpecification)}
    assert "message_template" not in field_names

    arguments = _valid_arguments()
    arguments["prompt_kind"] = "message_template"
    prompt_specification = PromptSpecification(**arguments)

    assert prompt_specification.prompt_kind == "message_template"


# --- Other prohibited fields ---


def test_prompt_specification_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(PromptSpecification)}

    prohibited_fields = {
        # Version / revision (folded into canonical_name)
        "version",
        "revision",
        "revision_id",
        "semantic_version",
        # Other Concepts (already separate / already on Provenance)
        "model_ref",
        "execution_ref",
        "actor_ref",
        "configuration_ref",
        "provider_ref",
        "source_ref",
        # Occurrence-level (Job/Attempt/Run)
        "job_id",
        "attempt_id",
        "run_id",
        "request_id",
        "generation_id",
        "invocation_id",
        "retry_count",
        # Deployment / Runtime / Container
        "deployment_ref",
        "runtime_ref",
        "container_image_ref",
        "region",
        # Lifecycle / policy
        "status",
        "active",
        "inactive",
        "deprecated",
        "retired",
        "approved",
        "blocked",
        "deprecated_at",
        "retired_at",
        "updated_at",
        # Unbounded / secret
        "metadata",
        "arbitrary_json",
        "api_key",
        "access_token",
        "credential",
        "secret",
        # Reverse references / correction machinery (not implemented)
        "provenance_refs",
        "prompt_refs",
        "supersedes_ref",
        "resolved_ref",
        "duplicate_of_ref",
        "revision_of_ref",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Provenance compatibility ---


def _valid_provenance_arguments(
    prompt_specification_id: str | None,
) -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-prompt-spec-001",
        "activity_kind": "summarize",
        "actor_ref": "actor:atlas:summarization-service",
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
        "prompt_ref": prompt_specification_id,
    }


def test_prompt_specification_id_can_be_passed_to_provenance_prompt_ref() -> None:
    prompt_specification = PromptSpecification(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments(
            prompt_specification.prompt_specification_id
        )
    )

    assert provenance.prompt_ref == prompt_specification.prompt_specification_id


def test_provenance_holds_id_string_not_prompt_specification_object() -> None:
    prompt_specification = PromptSpecification(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments(
            prompt_specification.prompt_specification_id
        )
    )

    assert isinstance(provenance.prompt_ref, str)
    assert not isinstance(provenance.prompt_ref, PromptSpecification)


def test_provenance_prompt_ref_remains_optional_and_none_is_accepted() -> None:
    provenance = Provenance(**_valid_provenance_arguments(None))

    assert provenance.prompt_ref is None


def test_prompt_specification_has_no_reverse_provenance_reference() -> None:
    field_names = {field.name for field in fields(PromptSpecification)}

    assert "provenance_id" not in field_names
    assert "provenance_ref" not in field_names
    assert "provenance_refs" not in field_names


def test_provenance_retains_exact_approved_thirteen_field_set() -> None:
    field_names = tuple(field.name for field in fields(Provenance))

    assert field_names == (
        "provenance_id",
        "activity_kind",
        "actor_ref",
        "started_at",
        "completed_at",
        "recorded_at",
        "input_refs",
        "parent_provenance_refs",
        "execution_ref",
        "model_ref",
        "prompt_ref",
        "configuration_ref",
        "external_run_ref",
    )
    assert len(field_names) == 13


# --- Package export and cross-Concept isolation ---


def test_package_exports_all_nine_core_models() -> None:
    import atlas_core

    assert set(atlas_core.__all__) == {
        "AIModel",
        "Actor",
        "ConfigurationSpecification",
        "Evidence",
        "ExecutionSpecification",
        "Observation",
        "PromptSpecification",
        "Provenance",
        "Source",
        "__version__",
    }


def test_package_root_import_succeeds() -> None:
    import atlas_core

    assert atlas_core.PromptSpecification is PromptSpecification


def test_prompt_specification_has_no_other_core_model_reference() -> None:
    field_names = {field.name for field in fields(PromptSpecification)}

    assert "evidence_id" not in field_names
    assert "evidence_ref" not in field_names
    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "source_id" not in field_names
    assert "source_ref" not in field_names
    assert "actor_id" not in field_names
    assert "actor_ref" not in field_names
    assert "model_id" not in field_names
    assert "model_ref" not in field_names
    assert "execution_specification_id" not in field_names
    assert "execution_ref" not in field_names


def test_no_existing_core_model_imports_prompt_specification() -> None:
    import ast
    import inspect

    import atlas_core.actor as actor_module
    import atlas_core.ai_model as ai_model_module
    import atlas_core.evidence as evidence_module
    import atlas_core.execution_specification as execution_specification_module
    import atlas_core.observation as observation_module
    import atlas_core.provenance as provenance_module
    import atlas_core.source as source_module

    for module in (
        actor_module,
        ai_model_module,
        evidence_module,
        execution_specification_module,
        observation_module,
        provenance_module,
        source_module,
    ):
        tree = ast.parse(inspect.getsource(module))
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.add(node.module)

        assert "atlas_core.prompt_specification" not in imported_modules
