from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timezone

import pytest

from atlas_core import Evidence, Observation, Provenance, Source


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 3,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "source_id": "source:bank-of-japan",
        "source_kind": "government_body",
        "canonical_name": "Bank of Japan",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_source_can_be_created() -> None:
    arguments = _valid_arguments()

    source = Source(**arguments)

    assert source.source_id == "source:bank-of-japan"
    assert source.source_kind == "government_body"
    assert source.canonical_name == "Bank of Japan"
    assert source.recorded_at == arguments["recorded_at"]


def test_source_is_exported_from_package_root() -> None:
    from atlas_core.source import Source as ModuleSource

    assert Source is ModuleSource


def test_source_is_immutable() -> None:
    source = Source(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        source.canonical_name = "changed"  # type: ignore[misc]


def test_source_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        Source(*arguments.values())  # type: ignore[misc]


def test_source_has_slots() -> None:
    source = Source(**_valid_arguments())

    assert not hasattr(source, "__dict__")


def test_source_has_exact_approved_field_set_and_order() -> None:
    field_names = tuple(field.name for field in fields(Source))

    assert field_names == (
        "source_id",
        "source_kind",
        "canonical_name",
        "recorded_at",
    )


def test_source_field_count_is_four() -> None:
    assert len(fields(Source)) == 4


def test_all_fields_are_required() -> None:
    for field in fields(Source):
        assert field.default is MISSING
        assert field.default_factory is MISSING  # type: ignore[misc]


# --- Required strings ---


@pytest.mark.parametrize(
    "field_name",
    ("source_id", "source_kind", "canonical_name"),
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
        Source(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("source_id", "source_kind", "canonical_name"),
)
def test_required_strings_reject_non_string(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = 123

    with pytest.raises(TypeError):
        Source(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("source_id", "source_kind", "canonical_name"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        Source(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("source_id", "source_kind", "canonical_name"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    source = Source(**arguments)

    assert getattr(source, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


# --- source_kind extensibility ---


def test_unknown_but_valid_source_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["source_kind"] = "some-brand-new-source-kind"

    source = Source(**arguments)

    assert source.source_kind == "some-brand-new-source-kind"


# --- canonical_name semantics ---


def test_duplicate_canonical_name_is_permitted_across_distinct_sources() -> None:
    arguments_a = _valid_arguments()
    arguments_a["source_id"] = "source:a"
    arguments_a["canonical_name"] = "Central Bank"

    arguments_b = _valid_arguments()
    arguments_b["source_id"] = "source:b"
    arguments_b["canonical_name"] = "Central Bank"

    source_a = Source(**arguments_a)
    source_b = Source(**arguments_b)

    assert source_a.canonical_name == source_b.canonical_name
    assert source_a.source_id != source_b.source_id


def test_canonical_name_is_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["canonical_name"] = "Reuters Business"

    source = Source(**arguments)

    assert source.canonical_name == "Reuters Business"


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    source = Source(**arguments)

    assert source.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    from datetime import timedelta

    non_utc = datetime(2026, 8, 3, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    source = Source(**arguments)

    assert source.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 3, 10)

    with pytest.raises(ValueError):
        Source(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-03T10:00:00Z"

    with pytest.raises(TypeError):
        Source(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        Source(**arguments)


# --- Prohibited fields ---


def test_source_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(Source)}

    prohibited_fields = {
        "parent_source_ref",
        "established_at",
        "organization_ref",
        "owner_ref",
        "operator_ref",
        "publisher_ref",
        "platform_ref",
        "relationship_refs",
        "predecessor_ref",
        "successor_ref",
        "url",
        "base_url",
        "canonical_locator",
        "endpoint",
        "api_endpoint",
        "profile_url",
        "feed_url",
        "provider_ref",
        "reliability_score",
        "credibility_score",
        "trust_score",
        "bias_score",
        "authority_score",
        "quality_score",
        "verified",
        "validation_result",
        "active",
        "is_active",
        "status",
        "processing_status",
        "suspended",
        "retired",
        "deleted",
        "blocked",
        "last_fetched_at",
        "next_fetch_at",
        "retry_count",
        "polling_interval",
        "job_id",
        "batch_id",
        "updated_at",
        "youtube_channel_id",
        "platform_account_id",
        "x_user_id",
        "facebook_page_id",
        "instagram_account_id",
        "tiktok_account_id",
        "fred_series_id",
        "sensor_station_code",
        "indicator_id",
        "property_id",
        "customer_id",
        "tenant_id",
        "raw_payload",
        "payload",
        "evidence_content",
        "observation_content",
        "prompt",
        "model_name",
        "crawler_name",
        "personal_email",
        "personal_phone",
        "personal_address",
        "government_id",
        "birth_date",
        "api_key",
        "access_token",
        "password",
        "cookie",
        "session_id",
        "authorization_header",
        "credential",
        "connection_string",
        "secret",
        "aliases",
        "display_name",
        "current_name",
        "previous_name",
        "former_names",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Evidence compatibility ---


def _valid_evidence_arguments(source_id: str) -> dict[str, object]:
    captured_at = _aware_datetime()

    return {
        "evidence_id": "evidence-001",
        "evidence_kind": "api-response",
        "source_ref": source_id,
        "artifact_locator": "atlas-object://artifact/001",
        "provenance_ref": "provenance-001",
        "captured_at": captured_at,
        "recorded_at": captured_at,
    }


def test_source_id_can_be_passed_to_evidence_source_ref() -> None:
    source = Source(**_valid_arguments())

    evidence = Evidence(**_valid_evidence_arguments(source.source_id))

    assert evidence.source_ref == source.source_id


def test_evidence_holds_id_string_not_source_object() -> None:
    source = Source(**_valid_arguments())

    evidence = Evidence(**_valid_evidence_arguments(source.source_id))

    assert isinstance(evidence.source_ref, str)
    assert not isinstance(evidence.source_ref, Source)


def test_source_has_no_reverse_evidence_reference() -> None:
    field_names = {field.name for field in fields(Source)}

    assert "evidence_id" not in field_names
    assert "evidence_ref" not in field_names
    assert "evidence_refs" not in field_names
    assert "evidences" not in field_names


# --- Observation and Provenance compatibility ---


def test_observation_and_provenance_remain_importable() -> None:
    import atlas_core

    assert atlas_core.Observation is Observation
    assert atlas_core.Provenance is Provenance


def test_package_exports_all_core_models() -> None:
    import atlas_core

    assert set(atlas_core.__all__) == {
        "AIModel",
        "Actor",
        "Evidence",
        "Observation",
        "Provenance",
        "Source",
        "__version__",
    }


def test_source_has_no_observation_or_provenance_reference() -> None:
    field_names = {field.name for field in fields(Source)}

    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "observation_refs" not in field_names
    assert "provenance_ref" not in field_names
    assert "provenance_refs" not in field_names
    assert "actor_ref" not in field_names
    assert "model_ref" not in field_names


def test_source_module_does_not_import_evidence_observation_or_provenance() -> None:
    import inspect

    import atlas_core.source as source_module

    source = inspect.getsource(source_module)

    assert "import Evidence" not in source
    assert "import Observation" not in source
    assert "import Provenance" not in source
    assert "atlas_core.evidence" not in source
    assert "atlas_core.observation" not in source
    assert "atlas_core.provenance" not in source


# --- Unknown and anonymous Source ---


def test_anonymous_source_is_accepted_as_complete_record() -> None:
    source = Source(
        source_id="source:confidential:014",
        source_kind="anonymous",
        canonical_name="confidential-field-source-014",
        recorded_at=_aware_datetime(),
    )

    assert source.source_kind == "anonymous"
    assert source.canonical_name == "confidential-field-source-014"


def test_unknown_source_is_accepted_as_complete_record() -> None:
    source = Source(
        source_id="source:unknown:weather-feed-002",
        source_kind="unknown",
        canonical_name="unknown-weather-origin-002",
        recorded_at=_aware_datetime(),
    )

    assert source.source_kind == "unknown"
    assert source.canonical_name == "unknown-weather-origin-002"


def test_empty_identifiers_remain_rejected_for_anonymous_sources() -> None:
    arguments = _valid_arguments()
    arguments["source_kind"] = "anonymous"
    arguments["canonical_name"] = ""

    with pytest.raises(ValueError):
        Source(**arguments)


# --- Retry, rename, and duplicate boundary ---


def test_distinct_source_ids_with_same_kind_produce_independent_records() -> None:
    arguments = _valid_arguments()
    arguments["source_id"] = "source:first"

    first = Source(**arguments)

    arguments["source_id"] = "source:second"

    second = Source(**arguments)

    assert first.source_id != second.source_id
    assert first.canonical_name == second.canonical_name
    assert first is not second


def test_source_has_no_alias_or_revision_field() -> None:
    field_names = {field.name for field in fields(Source)}

    assert "aliases" not in field_names
    assert "alias_refs" not in field_names
    assert "revision_of" not in field_names
    assert "previous_source_ref" not in field_names


def test_source_has_no_relationship_field() -> None:
    field_names = {field.name for field in fields(Source)}

    assert "parent_source_ref" not in field_names
    assert "relationship_refs" not in field_names
    assert "account_of_ref" not in field_names


# --- Raise-only validation ---


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_canonical_name = " Bank of Japan"

    arguments = _valid_arguments()
    arguments["canonical_name"] = original_canonical_name

    with pytest.raises(ValueError):
        Source(**arguments)

    assert arguments["canonical_name"] == original_canonical_name


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.source as source_module

    source = inspect.getsource(source_module)

    assert "object.__setattr__" not in source
