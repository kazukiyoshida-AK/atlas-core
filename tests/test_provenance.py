from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timezone

import pytest

from atlas_core import Evidence, Observation, Provenance


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 3,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-001",
        "activity_kind": "retrieve",
        "actor_ref": "actor-001",
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
        "input_refs": (),
        "parent_provenance_refs": (),
        "execution_ref": None,
        "model_ref": None,
        "prompt_ref": None,
        "configuration_ref": None,
        "external_run_ref": None,
    }


# --- Construction and representation ---


def test_provenance_can_be_created() -> None:
    arguments = _valid_arguments()

    provenance = Provenance(**arguments)

    assert provenance.provenance_id == "provenance-001"
    assert provenance.activity_kind == "retrieve"
    assert provenance.actor_ref == "actor-001"
    assert provenance.started_at == arguments["started_at"]
    assert provenance.completed_at == arguments["completed_at"]
    assert provenance.recorded_at == arguments["recorded_at"]
    assert provenance.input_refs == ()
    assert provenance.parent_provenance_refs == ()
    assert provenance.execution_ref is None
    assert provenance.model_ref is None
    assert provenance.prompt_ref is None
    assert provenance.configuration_ref is None
    assert provenance.external_run_ref is None


def test_optional_fields_default_without_being_passed() -> None:
    arguments = _valid_arguments()
    del arguments["input_refs"]
    del arguments["parent_provenance_refs"]
    del arguments["execution_ref"]
    del arguments["model_ref"]
    del arguments["prompt_ref"]
    del arguments["configuration_ref"]
    del arguments["external_run_ref"]

    provenance = Provenance(**arguments)

    assert provenance.input_refs == ()
    assert provenance.parent_provenance_refs == ()
    assert provenance.execution_ref is None
    assert provenance.model_ref is None
    assert provenance.prompt_ref is None
    assert provenance.configuration_ref is None
    assert provenance.external_run_ref is None


def test_provenance_is_exported_from_package_root() -> None:
    from atlas_core.provenance import Provenance as ModuleProvenance

    assert Provenance is ModuleProvenance


def test_provenance_is_immutable() -> None:
    provenance = Provenance(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        provenance.actor_ref = "changed"  # type: ignore[misc]


def test_provenance_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        Provenance(*arguments.values())  # type: ignore[misc]


def test_provenance_has_slots() -> None:
    provenance = Provenance(**_valid_arguments())

    assert not hasattr(provenance, "__dict__")


def test_provenance_has_exact_approved_field_set_and_order() -> None:
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


def test_required_and_optional_field_classification() -> None:
    field_map = {field.name: field for field in fields(Provenance)}

    required_fields = (
        "provenance_id",
        "activity_kind",
        "actor_ref",
        "started_at",
        "completed_at",
        "recorded_at",
    )

    for field_name in required_fields:
        assert field_map[field_name].default is MISSING
        assert field_map[field_name].default_factory is MISSING  # type: ignore[misc]

    optional_defaults = {
        "input_refs": (),
        "parent_provenance_refs": (),
        "execution_ref": None,
        "model_ref": None,
        "prompt_ref": None,
        "configuration_ref": None,
        "external_run_ref": None,
    }

    for field_name, expected_default in optional_defaults.items():
        assert field_map[field_name].default == expected_default


# --- Required strings ---


@pytest.mark.parametrize(
    "field_name",
    ("provenance_id", "activity_kind", "actor_ref"),
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
        Provenance(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("provenance_id", "activity_kind", "actor_ref"),
)
def test_required_strings_reject_non_string(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = 123

    with pytest.raises(TypeError):
        Provenance(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("provenance_id", "activity_kind", "actor_ref"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        Provenance(**arguments)


# --- Optional strings ---


@pytest.mark.parametrize(
    "field_name",
    (
        "execution_ref",
        "model_ref",
        "prompt_ref",
        "configuration_ref",
        "external_run_ref",
    ),
)
def test_optional_strings_accept_none(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = None

    provenance = Provenance(**arguments)

    assert getattr(provenance, field_name) is None


@pytest.mark.parametrize(
    "field_name",
    (
        "execution_ref",
        "model_ref",
        "prompt_ref",
        "configuration_ref",
        "external_run_ref",
    ),
)
def test_optional_strings_accept_valid_opaque_string(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = f"{field_name}-value"

    provenance = Provenance(**arguments)

    assert getattr(provenance, field_name) == f"{field_name}-value"


@pytest.mark.parametrize(
    "field_name",
    (
        "execution_ref",
        "model_ref",
        "prompt_ref",
        "configuration_ref",
        "external_run_ref",
    ),
)
@pytest.mark.parametrize(
    "invalid_value",
    ("", " ", " leading", "trailing "),
)
def test_optional_strings_reject_invalid_values(
    field_name: str,
    invalid_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(ValueError):
        Provenance(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "execution_ref",
        "model_ref",
        "prompt_ref",
        "configuration_ref",
        "external_run_ref",
    ),
)
def test_optional_strings_reject_non_string(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = 123

    with pytest.raises(TypeError):
        Provenance(**arguments)


# --- Activity kind extensibility ---


def test_unknown_but_valid_activity_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["activity_kind"] = "some-brand-new-activity-kind"

    provenance = Provenance(**arguments)

    assert provenance.activity_kind == "some-brand-new-activity-kind"


# --- Actor reference ---


def test_actor_ref_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["actor_ref"]

    with pytest.raises(TypeError):
        Provenance(**arguments)


def test_unknown_but_valid_actor_ref_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["actor_ref"] = "some-unregistered-actor-identifier"

    provenance = Provenance(**arguments)

    assert provenance.actor_ref == "some-unregistered-actor-identifier"


# --- Input references ---


@pytest.mark.parametrize(
    "valid_value",
    (
        (),
        ("evidence:e-1",),
        ("evidence:e-1", "observation:o-2"),
    ),
)
def test_input_refs_accepts_valid_tuples(
    valid_value: tuple[str, ...],
) -> None:
    arguments = _valid_arguments()
    arguments["input_refs"] = valid_value

    provenance = Provenance(**arguments)

    assert provenance.input_refs == valid_value


def test_input_refs_must_be_a_tuple() -> None:
    arguments = _valid_arguments()
    arguments["input_refs"] = ["evidence:e-1"]

    with pytest.raises(TypeError):
        Provenance(**arguments)


def test_input_refs_rejects_non_string_element() -> None:
    arguments = _valid_arguments()
    arguments["input_refs"] = (123,)

    with pytest.raises(TypeError):
        Provenance(**arguments)


@pytest.mark.parametrize(
    "invalid_reference",
    ("", " ", " leading", "trailing "),
)
def test_input_refs_rejects_invalid_string_elements(
    invalid_reference: str,
) -> None:
    arguments = _valid_arguments()
    arguments["input_refs"] = (invalid_reference,)

    with pytest.raises(ValueError):
        Provenance(**arguments)


def test_input_refs_rejects_duplicate_reference() -> None:
    arguments = _valid_arguments()
    arguments["input_refs"] = ("evidence:e-1", "evidence:e-1")

    with pytest.raises(ValueError):
        Provenance(**arguments)


def test_input_refs_preserves_order_without_sorting() -> None:
    arguments = _valid_arguments()
    arguments["input_refs"] = ("evidence:e-2", "evidence:e-1")

    provenance = Provenance(**arguments)

    assert provenance.input_refs == ("evidence:e-2", "evidence:e-1")


# --- Parent provenance references ---


@pytest.mark.parametrize(
    "valid_value",
    (
        (),
        ("provenance:p-1",),
        ("provenance:p-1", "provenance:p-2"),
    ),
)
def test_parent_provenance_refs_accepts_valid_tuples(
    valid_value: tuple[str, ...],
) -> None:
    arguments = _valid_arguments()
    arguments["parent_provenance_refs"] = valid_value

    provenance = Provenance(**arguments)

    assert provenance.parent_provenance_refs == valid_value


def test_parent_provenance_refs_must_be_a_tuple() -> None:
    arguments = _valid_arguments()
    arguments["parent_provenance_refs"] = ["provenance:p-1"]

    with pytest.raises(TypeError):
        Provenance(**arguments)


def test_parent_provenance_refs_rejects_non_string_element() -> None:
    arguments = _valid_arguments()
    arguments["parent_provenance_refs"] = (123,)

    with pytest.raises(TypeError):
        Provenance(**arguments)


@pytest.mark.parametrize(
    "invalid_reference",
    ("", " ", " leading", "trailing "),
)
def test_parent_provenance_refs_rejects_invalid_string_elements(
    invalid_reference: str,
) -> None:
    arguments = _valid_arguments()
    arguments["parent_provenance_refs"] = (invalid_reference,)

    with pytest.raises(ValueError):
        Provenance(**arguments)


def test_parent_provenance_refs_rejects_duplicate_reference() -> None:
    arguments = _valid_arguments()
    arguments["parent_provenance_refs"] = (
        "provenance:p-1",
        "provenance:p-1",
    )

    with pytest.raises(ValueError):
        Provenance(**arguments)


def test_parent_provenance_refs_rejects_self_reference() -> None:
    arguments = _valid_arguments()
    arguments["provenance_id"] = "provenance:p-001"
    arguments["parent_provenance_refs"] = ("provenance:p-001",)

    with pytest.raises(ValueError):
        Provenance(**arguments)


def test_parent_provenance_refs_allows_distinct_parents() -> None:
    arguments = _valid_arguments()
    arguments["provenance_id"] = "provenance:p-003"
    arguments["parent_provenance_refs"] = (
        "provenance:p-left",
        "provenance:p-right",
    )

    provenance = Provenance(**arguments)

    assert provenance.parent_provenance_refs == (
        "provenance:p-left",
        "provenance:p-right",
    )


# --- Timestamps ---


@pytest.mark.parametrize(
    "field_name",
    ("started_at", "completed_at", "recorded_at"),
)
def test_timestamp_fields_reject_naive_datetime(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = datetime(2026, 8, 3, 10)

    with pytest.raises(ValueError):
        Provenance(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("started_at", "completed_at", "recorded_at"),
)
def test_timestamp_fields_reject_non_datetime(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "2026-08-03T10:00:00Z"

    with pytest.raises(TypeError):
        Provenance(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("started_at", "completed_at", "recorded_at"),
)
def test_timestamp_fields_accept_timezone_aware_value(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = _aware_datetime(hour=9)

    provenance = Provenance(**arguments)

    assert getattr(provenance, field_name) == _aware_datetime(hour=9)


def test_cross_field_chronological_order_is_not_hard_validated() -> None:
    arguments = _valid_arguments()
    arguments["started_at"] = _aware_datetime(hour=10)
    arguments["completed_at"] = _aware_datetime(hour=9)
    arguments["recorded_at"] = _aware_datetime(hour=8)

    provenance = Provenance(**arguments)

    assert provenance.started_at == _aware_datetime(hour=10)
    assert provenance.completed_at == _aware_datetime(hour=9)
    assert provenance.recorded_at == _aware_datetime(hour=8)


# --- No normalization ---


def test_values_are_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["activity_kind"] = "Custom-Activity-Kind"
    arguments["actor_ref"] = "Actor-Ref-001"
    arguments["input_refs"] = ("Evidence:E-1",)
    arguments["parent_provenance_refs"] = ("Provenance:P-0",)
    arguments["execution_ref"] = "Execution-Ref"
    arguments["model_ref"] = "Model-Ref"
    arguments["prompt_ref"] = "Prompt-Ref"
    arguments["configuration_ref"] = "Configuration-Ref"
    arguments["external_run_ref"] = "External-Run-Ref"

    provenance = Provenance(**arguments)

    assert provenance.activity_kind == "Custom-Activity-Kind"
    assert provenance.actor_ref == "Actor-Ref-001"
    assert provenance.input_refs == ("Evidence:E-1",)
    assert provenance.parent_provenance_refs == ("Provenance:P-0",)
    assert provenance.execution_ref == "Execution-Ref"
    assert provenance.model_ref == "Model-Ref"
    assert provenance.prompt_ref == "Prompt-Ref"
    assert provenance.configuration_ref == "Configuration-Ref"
    assert provenance.external_run_ref == "External-Run-Ref"


# --- Retry boundary ---


def test_retry_with_same_inputs_creates_distinct_provenance() -> None:
    arguments = _valid_arguments()
    arguments["provenance_id"] = "provenance:p-first"

    first = Provenance(**arguments)

    arguments["provenance_id"] = "provenance:p-retry"

    second = Provenance(**arguments)

    assert first.provenance_id != second.provenance_id
    assert first.activity_kind == second.activity_kind
    assert first.actor_ref == second.actor_ref
    assert first is not second


# --- Prohibited fields ---


def test_provenance_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(Provenance)}

    prohibited_fields = {
        "output_refs",
        "evidence_id",
        "evidence_ref",
        "evidence_refs",
        "evidences",
        "observation_id",
        "observation_ref",
        "observation_refs",
        "observations",
        "raw_payload",
        "payload",
        "content",
        "content_text",
        "content_bytes",
        "binary_data",
        "raw_json",
        "raw_html",
        "raw_response",
        "prompt_text",
        "system_prompt",
        "user_prompt",
        "confidence",
        "fact_confidence",
        "extraction_confidence",
        "source_reliability",
        "reliability_score",
        "trust_score",
        "validation_result",
        "human_reviewed",
        "is_verified",
        "integrity_verified",
        "status",
        "workflow_status",
        "processing_status",
        "queue_status",
        "processed_at",
        "succeeded",
        "failed",
        "cancelled",
        "partial",
        "timed_out",
        "retrying",
        "retry_count",
        "next_retry_at",
        "error_message",
        "stack_trace",
        "actor_name",
        "actor_email",
        "actor_phone",
        "person_name",
        "email",
        "phone_number",
        "address",
        "api_key",
        "access_token",
        "token",
        "password",
        "cookie",
        "session_id",
        "authorization_header",
        "credential",
        "database_url",
        "connection_string",
        "secret",
        "provider",
        "model_provider",
        "openai_model",
        "anthropic_model",
        "gemini_model",
        "deployment_name",
        "temperature",
        "top_p",
        "max_tokens",
        "youtube_video_id",
        "youtube_channel_id",
        "fred_series_id",
        "indicator_id",
        "property_id",
        "post_id",
        "article_id",
        "customer_id",
        "tenant_id",
        "video_id",
        "view_count",
        "like_count",
        "comment_count",
        "value",
        "unit",
        "currency",
        "ingestion_run_id",
        "backfill_job_id",
        "collection_run_id",
        "analysis_run_id",
        "job_id",
        "batch_id",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Observation and Evidence compatibility ---


def _valid_evidence_arguments(provenance_id: str) -> dict[str, object]:
    captured_at = _aware_datetime()

    return {
        "evidence_id": "evidence-001",
        "evidence_kind": "api-response",
        "source_ref": "source-001",
        "artifact_locator": "atlas-object://artifact/001",
        "provenance_ref": provenance_id,
        "captured_at": captured_at,
        "recorded_at": captured_at,
    }


def _valid_observation_arguments(provenance_id: str) -> dict[str, object]:
    observed_at = _aware_datetime()

    return {
        "observation_id": "observation-001",
        "normalized_statement": "A validated atomic fact.",
        "statement_language": "en",
        "evidence_refs": ("evidence-001",),
        "provenance_ref": provenance_id,
        "observed_at": observed_at,
        "recorded_at": observed_at,
    }


def test_provenance_id_can_be_passed_to_evidence_provenance_ref() -> None:
    provenance = Provenance(**_valid_arguments())

    evidence = Evidence(**_valid_evidence_arguments(provenance.provenance_id))

    assert evidence.provenance_ref == provenance.provenance_id


def test_provenance_id_can_be_passed_to_observation_provenance_ref() -> None:
    provenance = Provenance(**_valid_arguments())

    observation = Observation(
        **_valid_observation_arguments(provenance.provenance_id)
    )

    assert observation.provenance_ref == provenance.provenance_id


def test_evidence_and_observation_can_share_same_provenance_id() -> None:
    provenance = Provenance(**_valid_arguments())

    evidence = Evidence(**_valid_evidence_arguments(provenance.provenance_id))
    observation = Observation(
        **_valid_observation_arguments(provenance.provenance_id)
    )

    assert evidence.provenance_ref == observation.provenance_ref
    assert evidence.provenance_ref == provenance.provenance_id


def test_evidence_holds_id_string_not_provenance_object() -> None:
    provenance = Provenance(**_valid_arguments())

    evidence = Evidence(**_valid_evidence_arguments(provenance.provenance_id))

    assert isinstance(evidence.provenance_ref, str)
    assert not isinstance(evidence.provenance_ref, Provenance)


def test_observation_holds_id_string_not_provenance_object() -> None:
    provenance = Provenance(**_valid_arguments())

    observation = Observation(
        **_valid_observation_arguments(provenance.provenance_id)
    )

    assert isinstance(observation.provenance_ref, str)
    assert not isinstance(observation.provenance_ref, Provenance)


def test_provenance_has_no_reverse_evidence_or_observation_reference() -> None:
    field_names = {field.name for field in fields(Provenance)}

    assert "evidence_id" not in field_names
    assert "evidence_ref" not in field_names
    assert "evidence_refs" not in field_names
    assert "evidences" not in field_names
    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "observation_refs" not in field_names
    assert "observations" not in field_names
    assert "output_refs" not in field_names


def test_provenance_module_does_not_import_evidence_or_observation() -> None:
    import inspect

    import atlas_core.provenance as provenance_module

    source = inspect.getsource(provenance_module)

    assert "import Evidence" not in source
    assert "import Observation" not in source
    assert "atlas_core.evidence" not in source
    assert "atlas_core.observation" not in source


def test_package_root_import_succeeds() -> None:
    import atlas_core

    assert atlas_core.Provenance is Provenance


# --- Raise-only validation ---


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_actor_ref = " actor-with-leading-space"

    arguments = _valid_arguments()
    arguments["actor_ref"] = original_actor_ref

    with pytest.raises(ValueError):
        Provenance(**arguments)

    assert arguments["actor_ref"] == original_actor_ref


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.provenance as provenance_module

    source = inspect.getsource(provenance_module)

    assert "object.__setattr__" not in source
