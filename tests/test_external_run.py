from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from atlas_core import ExternalRun, Provenance


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 4,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "external_run_id": "external-run:01HZY3K9G8N7Q2R5T6V8W0X1Y2",
        "external_run_kind": "request",
        "external_identifier": "chatcmpl-abc123",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_external_run_can_be_created() -> None:
    arguments = _valid_arguments()

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_id == (
        "external-run:01HZY3K9G8N7Q2R5T6V8W0X1Y2"
    )
    assert external_run.external_run_kind == "request"
    assert external_run.external_identifier == "chatcmpl-abc123"
    assert external_run.recorded_at == arguments["recorded_at"]


def test_external_run_is_exported_from_package_root() -> None:
    from atlas_core.external_run import ExternalRun as ModuleExternalRun

    assert ExternalRun is ModuleExternalRun


def test_external_run_is_immutable() -> None:
    external_run = ExternalRun(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        external_run.external_run_kind = "changed"  # type: ignore[misc]


def test_external_run_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        ExternalRun(*arguments.values())  # type: ignore[misc]


def test_external_run_has_slots() -> None:
    external_run = ExternalRun(**_valid_arguments())

    assert not hasattr(external_run, "__dict__")


def test_external_run_has_exact_approved_field_set_and_order() -> None:
    field_names = tuple(field.name for field in fields(ExternalRun))

    assert field_names == (
        "external_run_id",
        "external_run_kind",
        "external_identifier",
        "recorded_at",
    )


def test_external_run_field_count_is_four() -> None:
    assert len(fields(ExternalRun)) == 4


def test_three_fields_are_required() -> None:
    required = [
        field
        for field in fields(ExternalRun)
        if field.default is MISSING and field.default_factory is MISSING  # type: ignore[misc]
    ]
    required_names = {field.name for field in required}

    assert required_names == {"external_run_id", "external_run_kind", "recorded_at"}
    assert len(required) == 3


def test_one_field_is_optional_with_default_none() -> None:
    optional = [
        field
        for field in fields(ExternalRun)
        if field.default is not MISSING or field.default_factory is not MISSING  # type: ignore[misc]
    ]

    assert len(optional) == 1
    assert optional[0].name == "external_identifier"
    assert optional[0].default is None


def test_external_run_has_no_canonical_name_field() -> None:
    field_names = {field.name for field in fields(ExternalRun)}

    assert "canonical_name" not in field_names


def test_external_run_module_imports_only_standard_library() -> None:
    import ast
    import inspect

    import atlas_core.external_run as external_run_module

    source = inspect.getsource(external_run_module)
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
        "atlas_core.configuration_specification",
        "atlas_core.evidence",
        "atlas_core.execution_specification",
        "atlas_core.observation",
        "atlas_core.prompt_specification",
        "atlas_core.provenance",
        "atlas_core.source",
    }

    assert imported_modules.isdisjoint(prohibited_modules)

    for module_name in imported_modules:
        assert module_name in {"__future__", "dataclasses", "datetime"}


# --- Required strings: external_run_id, external_run_kind ---


@pytest.mark.parametrize(
    "field_name",
    ("external_run_id", "external_run_kind"),
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
        ExternalRun(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("external_run_id", "external_run_kind"),
)
@pytest.mark.parametrize("invalid_value", (123, None, [], {}))
def test_required_strings_reject_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        ExternalRun(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("external_run_id", "external_run_kind"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        ExternalRun(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("external_run_id", "external_run_kind"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    external_run = ExternalRun(**arguments)

    assert getattr(external_run, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_kind = " request"

    arguments = _valid_arguments()
    arguments["external_run_kind"] = original_kind

    with pytest.raises(ValueError):
        ExternalRun(**arguments)

    assert arguments["external_run_kind"] == original_kind


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.external_run as external_run_module

    source = inspect.getsource(external_run_module)

    assert "object.__setattr__" not in source


# --- Optional external_identifier ---


def test_external_identifier_omitted_defaults_to_none() -> None:
    arguments = _valid_arguments()
    del arguments["external_identifier"]

    external_run = ExternalRun(**arguments)

    assert external_run.external_identifier is None


def test_external_identifier_explicit_none_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = None

    external_run = ExternalRun(**arguments)

    assert external_run.external_identifier is None


@pytest.mark.parametrize("invalid_value", (123, [], {}))
def test_external_identifier_rejects_non_none_non_string(
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = invalid_value

    with pytest.raises(TypeError):
        ExternalRun(**arguments)


@pytest.mark.parametrize(
    "invalid_value",
    ("", " ", " leading", "trailing "),
)
def test_external_identifier_rejects_invalid_string_values(
    invalid_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = invalid_value

    with pytest.raises(ValueError):
        ExternalRun(**arguments)


def test_external_identifier_preserves_internal_content() -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )

    external_run = ExternalRun(**arguments)

    assert external_run.external_identifier == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


def test_external_identifier_preserves_provider_issued_prefix() -> None:
    # ACR-011 §19.1/§19.2: a prefix genuinely issued by the external
    # system is preserved verbatim — this differs from Atlas
    # constructing a prefix itself, which is prohibited.
    arguments = _valid_arguments()
    arguments["external_identifier"] = "chatcmpl-abc123"

    external_run = ExternalRun(**arguments)

    assert external_run.external_identifier == "chatcmpl-abc123"


@pytest.mark.parametrize(
    "provider_style_identifier",
    ("chatcmpl-abc123", "batch_01ABC", "run_xyz789"),
)
def test_provider_style_identifier_examples_are_accepted(
    provider_style_identifier: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = provider_style_identifier

    external_run = ExternalRun(**arguments)

    assert external_run.external_identifier == provider_style_identifier


def test_external_identifier_is_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = "MixedCase-ID_123"

    external_run = ExternalRun(**arguments)

    assert external_run.external_identifier == "MixedCase-ID_123"


def test_duplicate_external_identifier_permitted_across_distinct_records() -> None:
    # ACR-011 §30 Risk 3/§14: collisions across Providers or reused
    # IDs after retention expiry are a named, unresolved v0.1 risk —
    # Core performs no uniqueness enforcement.
    arguments_a = _valid_arguments()
    arguments_a["external_run_id"] = "external-run:a"
    arguments_a["external_identifier"] = "shared-id-123"

    arguments_b = _valid_arguments()
    arguments_b["external_run_id"] = "external-run:b"
    arguments_b["external_identifier"] = "shared-id-123"

    external_run_a = ExternalRun(**arguments_a)
    external_run_b = ExternalRun(**arguments_b)

    assert external_run_a.external_identifier == external_run_b.external_identifier
    assert external_run_a.external_run_id != external_run_b.external_run_id


def test_frozen_dataclass_equality_is_ordinary_value_equality() -> None:
    arguments = _valid_arguments()

    first = ExternalRun(**arguments)
    second = ExternalRun(**arguments)

    assert first == second
    assert first is not second


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    external_run = ExternalRun(**arguments)

    assert external_run.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    non_utc = datetime(2026, 8, 4, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    external_run = ExternalRun(**arguments)

    assert external_run.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 4, 10)

    with pytest.raises(ValueError):
        ExternalRun(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-04T10:00:00Z"

    with pytest.raises(TypeError):
        ExternalRun(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        ExternalRun(**arguments)


# --- external_run_kind: execution architecture axis only ---


@pytest.mark.parametrize(
    "recommended_kind",
    (
        "request",
        "job",
        "batch",
        "workflow",
        "operation",
        "delivery",
        "unknown",
    ),
)
def test_recommended_external_run_kind_values_are_accepted(
    recommended_kind: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_run_kind"] = recommended_kind

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_kind == recommended_kind


def test_custom_execution_architecture_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["external_run_kind"] = "custom_execution_architecture"

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_kind == "custom_execution_architecture"


def test_external_run_kind_is_not_a_closed_enum() -> None:
    arguments = _valid_arguments()
    arguments["external_run_kind"] = "domain_local_experimental_kind"

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_kind == "domain_local_experimental_kind"


@pytest.mark.parametrize(
    "excluded_response_context_value",
    ("stream", "session", "thread", "conversation", "response", "result"),
)
def test_excluded_response_context_strings_remain_technically_constructible(
    excluded_response_context_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_run_kind"] = excluded_response_context_value

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_kind == excluded_response_context_value


@pytest.mark.parametrize(
    "excluded_transport_value",
    ("http", "webhook", "queue", "rpc", "sdk", "cli"),
)
def test_excluded_transport_strings_remain_technically_constructible(
    excluded_transport_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_run_kind"] = excluded_transport_value

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_kind == excluded_transport_value


@pytest.mark.parametrize(
    "excluded_purpose_value",
    ("generation", "publication", "collection", "analysis", "upload", "download"),
)
def test_excluded_functional_purpose_strings_remain_technically_constructible(
    excluded_purpose_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_run_kind"] = excluded_purpose_value

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_kind == excluded_purpose_value


# --- Known, Known-without-identifier, Unknown examples ---


def test_known_external_run_with_identifier_example() -> None:
    external_run = ExternalRun(
        external_run_id="external-run:openai-request-001",
        external_run_kind="request",
        external_identifier="chatcmpl-abc123",
        recorded_at=_aware_datetime(),
    )

    assert external_run.external_identifier == "chatcmpl-abc123"


def test_known_external_run_without_stored_identifier_example() -> None:
    # ACR-011 §20.1: occurrence and kind confirmed, identifier
    # unavailable, withheld, or unsuitable to store — still Known.
    external_run = ExternalRun(
        external_run_id="external-run:x-post-001",
        external_run_kind="request",
        recorded_at=_aware_datetime(),
    )

    assert external_run.external_identifier is None
    assert external_run.external_run_kind == "request"


def test_unknown_external_run_is_accepted_as_complete_record() -> None:
    external_run = ExternalRun(
        external_run_id="external-run:unknown:3e9b7f1a5c82",
        external_run_kind="unknown",
        recorded_at=_aware_datetime(),
    )

    assert external_run.external_run_kind == "unknown"
    assert external_run.external_identifier is None


def test_unknown_external_run_may_carry_a_confirmed_execution_identifier() -> (
    None
):
    # An Unknown record MAY carry an identifier if Atlas can confirm it
    # was issued by the external system for an execution occurrence —
    # ACR-011 §20.2. This is a semantic admission judgment, not a
    # runtime constraint; Core accepts either shape.
    external_run = ExternalRun(
        external_run_id="external-run:unknown:8a1d4e7c9f02",
        external_run_kind="unknown",
        external_identifier="op-8a1d4e7c9f02",
        recorded_at=_aware_datetime(),
    )

    assert external_run.external_identifier == "op-8a1d4e7c9f02"


def test_arbitrary_opaque_external_run_id_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["external_run_id"] = "01HZY3K9G8N7Q2R5T6V8W0X1Y2"

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_id == "01HZY3K9G8N7Q2R5T6V8W0X1Y2"


def test_no_required_id_prefix_is_enforced() -> None:
    arguments = _valid_arguments()
    arguments["external_run_id"] = "just-any-non-empty-string"

    external_run = ExternalRun(**arguments)

    assert external_run.external_run_id == "just-any-non-empty-string"


# --- Prohibited fields ---


def test_external_run_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(ExternalRun)}

    prohibited_fields = {
        # Naming (occurrence, not Specification)
        "canonical_name",
        "version",
        "revision",
        # Time (recorded_at only)
        "started_at",
        "completed_at",
        "external_started_at",
        "external_completed_at",
        # Status
        "status",
        "updated_at",
        # Attempt
        "attempt_number",
        "attempt_id",
        "retry_count",
        "parent_external_run_ref",
        # Provider
        "provider_ref",
        "external_system_ref",
        # Other Concepts / reverse reference
        "execution_ref",
        "model_ref",
        "prompt_ref",
        "configuration_ref",
        "actor_ref",
        "provenance_ref",
        # Resource / Artifact
        "resource_ref",
        "result_ref",
        "input_refs",
        "output_refs",
        # Unbounded / secret / personal
        "metadata",
        "raw_payload",
        "request_payload",
        "response_payload",
        "api_key",
        "access_token",
        "credential",
        "secret",
        "personal_information",
        "session_id",
        "thread_id",
        "conversation_id",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Provenance compatibility ---


def _valid_provenance_arguments(
    external_run_id: str | None,
) -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-external-run-001",
        "activity_kind": "summarize",
        "actor_ref": "actor:atlas:summarization-service",
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
        "external_run_ref": external_run_id,
    }


def test_external_run_id_can_be_passed_to_provenance_external_run_ref() -> None:
    external_run = ExternalRun(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments(external_run.external_run_id)
    )

    assert provenance.external_run_ref == external_run.external_run_id


def test_provenance_holds_id_string_not_external_run_object() -> None:
    external_run = ExternalRun(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments(external_run.external_run_id)
    )

    assert isinstance(provenance.external_run_ref, str)
    assert not isinstance(provenance.external_run_ref, ExternalRun)


def test_provenance_external_run_ref_remains_optional_and_none_is_accepted() -> (
    None
):
    provenance = Provenance(**_valid_provenance_arguments(None))

    assert provenance.external_run_ref is None


def test_external_run_has_no_reverse_provenance_reference() -> None:
    field_names = {field.name for field in fields(ExternalRun)}

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


def test_package_exports_all_eleven_core_models() -> None:
    import atlas_core

    assert set(atlas_core.__all__) == {
        "AIModel",
        "Actor",
        "Artifact",
        "ConfigurationSpecification",
        "Evidence",
        "ExecutionSpecification",
        "ExternalRun",
        "Observation",
        "PromptSpecification",
        "Provenance",
        "Source",
        "__version__",
    }


def test_package_root_import_succeeds() -> None:
    import atlas_core

    assert atlas_core.ExternalRun is ExternalRun


def test_external_run_has_no_other_core_model_reference() -> None:
    field_names = {field.name for field in fields(ExternalRun)}

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
    assert "prompt_specification_id" not in field_names
    assert "prompt_ref" not in field_names
    assert "configuration_specification_id" not in field_names
    assert "configuration_ref" not in field_names


def test_no_existing_core_model_imports_external_run() -> None:
    import ast
    import inspect

    import atlas_core.actor as actor_module
    import atlas_core.ai_model as ai_model_module
    import atlas_core.configuration_specification as configuration_specification_module
    import atlas_core.evidence as evidence_module
    import atlas_core.execution_specification as execution_specification_module
    import atlas_core.observation as observation_module
    import atlas_core.prompt_specification as prompt_specification_module
    import atlas_core.provenance as provenance_module
    import atlas_core.source as source_module

    for module in (
        actor_module,
        ai_model_module,
        configuration_specification_module,
        evidence_module,
        execution_specification_module,
        observation_module,
        prompt_specification_module,
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

        assert "atlas_core.external_run" not in imported_modules
