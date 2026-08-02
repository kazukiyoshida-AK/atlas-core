from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timezone

import pytest

from atlas_core import Evidence, Observation


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 2,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    captured_at = _aware_datetime()

    return {
        "evidence_id": "evidence-001",
        "evidence_kind": "api-response",
        "source_ref": "source-001",
        "artifact_locator": "atlas-object://artifact/001",
        "provenance_ref": "provenance-001",
        "captured_at": captured_at,
        "recorded_at": captured_at,
        "content_selector": None,
        "media_type": None,
        "content_digest": None,
        "digest_algorithm": None,
        "byte_length": None,
        "source_published_at": None,
    }


# --- Construction and representation ---


def test_evidence_can_be_created() -> None:
    arguments = _valid_arguments()

    evidence = Evidence(**arguments)

    assert evidence.evidence_id == "evidence-001"
    assert evidence.evidence_kind == "api-response"
    assert evidence.source_ref == "source-001"
    assert evidence.artifact_locator == "atlas-object://artifact/001"
    assert evidence.provenance_ref == "provenance-001"
    assert evidence.captured_at == arguments["captured_at"]
    assert evidence.recorded_at == arguments["recorded_at"]


def test_optional_fields_default_to_none() -> None:
    arguments = _valid_arguments()
    del arguments["content_selector"]
    del arguments["media_type"]
    del arguments["content_digest"]
    del arguments["digest_algorithm"]
    del arguments["byte_length"]
    del arguments["source_published_at"]

    evidence = Evidence(**arguments)

    assert evidence.content_selector is None
    assert evidence.media_type is None
    assert evidence.content_digest is None
    assert evidence.digest_algorithm is None
    assert evidence.byte_length is None
    assert evidence.source_published_at is None


def test_evidence_is_exported_from_package_root() -> None:
    from atlas_core.evidence import Evidence as ModuleEvidence

    assert Evidence is ModuleEvidence


def test_evidence_is_immutable() -> None:
    evidence = Evidence(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        evidence.artifact_locator = "changed"


def test_evidence_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        Evidence(*arguments.values())  # type: ignore[misc]


def test_evidence_has_slots() -> None:
    evidence = Evidence(**_valid_arguments())

    assert not hasattr(evidence, "__dict__")


def test_evidence_has_exact_approved_field_set_and_order() -> None:
    field_names = tuple(field.name for field in fields(Evidence))

    assert field_names == (
        "evidence_id",
        "evidence_kind",
        "source_ref",
        "artifact_locator",
        "provenance_ref",
        "captured_at",
        "recorded_at",
        "content_selector",
        "media_type",
        "content_digest",
        "digest_algorithm",
        "byte_length",
        "source_published_at",
    )


# --- Required strings ---


@pytest.mark.parametrize(
    "field_name",
    (
        "evidence_id",
        "evidence_kind",
        "source_ref",
        "artifact_locator",
        "provenance_ref",
    ),
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
        Evidence(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "evidence_id",
        "evidence_kind",
        "source_ref",
        "artifact_locator",
        "provenance_ref",
    ),
)
def test_required_strings_reject_non_string(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = 123

    with pytest.raises(TypeError):
        Evidence(**arguments)


# --- Optional strings ---


@pytest.mark.parametrize(
    "field_name",
    ("content_selector", "media_type", "content_digest", "digest_algorithm"),
)
def test_optional_strings_accept_none(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = None
    if field_name in ("content_digest", "digest_algorithm"):
        arguments["content_digest"] = None
        arguments["digest_algorithm"] = None

    evidence = Evidence(**arguments)

    assert getattr(evidence, field_name) is None


@pytest.mark.parametrize(
    "field_name",
    ("content_selector", "media_type"),
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
        Evidence(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("content_selector", "media_type"),
)
def test_optional_strings_reject_non_string(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = 123

    with pytest.raises(TypeError):
        Evidence(**arguments)


# --- Source and locator ---


def test_source_ref_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["source_ref"]

    with pytest.raises(TypeError):
        Evidence(**arguments)


def test_unknown_but_valid_source_ref_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["source_ref"] = "some-unregistered-source-identifier"

    evidence = Evidence(**arguments)

    assert evidence.source_ref == "some-unregistered-source-identifier"


def test_opaque_locator_is_accepted_without_parsing() -> None:
    arguments = _valid_arguments()
    arguments["artifact_locator"] = "not a real uri :: but opaque"

    evidence = Evidence(**arguments)

    assert evidence.artifact_locator == "not a real uri :: but opaque"


def test_unknown_evidence_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["evidence_kind"] = "some-brand-new-kind"

    evidence = Evidence(**arguments)

    assert evidence.evidence_kind == "some-brand-new-kind"


# --- Content hash pair ---


def test_digest_pair_both_absent_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = None
    arguments["digest_algorithm"] = None

    evidence = Evidence(**arguments)

    assert evidence.content_digest is None
    assert evidence.digest_algorithm is None


def test_digest_pair_both_present_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = "abc123"
    arguments["digest_algorithm"] = "sha256"

    evidence = Evidence(**arguments)

    assert evidence.content_digest == "abc123"
    assert evidence.digest_algorithm == "sha256"


def test_digest_only_is_rejected() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = "abc123"
    arguments["digest_algorithm"] = None

    with pytest.raises(ValueError):
        Evidence(**arguments)


def test_algorithm_only_is_rejected() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = None
    arguments["digest_algorithm"] = "sha256"

    with pytest.raises(ValueError):
        Evidence(**arguments)


def test_digest_value_is_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = "ABC123"
    arguments["digest_algorithm"] = "SHA256"

    evidence = Evidence(**arguments)

    assert evidence.content_digest == "ABC123"
    assert evidence.digest_algorithm == "SHA256"


# --- Media type ---


def test_media_type_is_held_as_provided() -> None:
    arguments = _valid_arguments()
    arguments["media_type"] = "Application/JSON; charset=UTF-8"

    evidence = Evidence(**arguments)

    assert evidence.media_type == "Application/JSON; charset=UTF-8"


# --- Byte length ---


@pytest.mark.parametrize("valid_value", (None, 0, 1, 1024))
def test_byte_length_accepts_valid_values(valid_value: int | None) -> None:
    arguments = _valid_arguments()
    arguments["byte_length"] = valid_value

    evidence = Evidence(**arguments)

    assert evidence.byte_length == valid_value


def test_byte_length_rejects_negative_value() -> None:
    arguments = _valid_arguments()
    arguments["byte_length"] = -1

    with pytest.raises(ValueError):
        Evidence(**arguments)


def test_byte_length_rejects_float() -> None:
    arguments = _valid_arguments()
    arguments["byte_length"] = 1.5

    with pytest.raises(TypeError):
        Evidence(**arguments)


def test_byte_length_rejects_string() -> None:
    arguments = _valid_arguments()
    arguments["byte_length"] = "100"

    with pytest.raises(TypeError):
        Evidence(**arguments)


def test_byte_length_rejects_true() -> None:
    arguments = _valid_arguments()
    arguments["byte_length"] = True

    with pytest.raises(TypeError):
        Evidence(**arguments)


def test_byte_length_rejects_false() -> None:
    arguments = _valid_arguments()
    arguments["byte_length"] = False

    with pytest.raises(TypeError):
        Evidence(**arguments)


# --- Timestamps ---


@pytest.mark.parametrize(
    "field_name",
    ("captured_at", "recorded_at", "source_published_at"),
)
def test_timestamp_fields_reject_naive_datetime(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = datetime(2026, 8, 2, 10)

    with pytest.raises(ValueError):
        Evidence(**arguments)


@pytest.mark.parametrize("field_name", ("captured_at", "recorded_at"))
def test_required_timestamp_rejects_non_datetime(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "2026-08-02T10:00:00Z"

    with pytest.raises(TypeError):
        Evidence(**arguments)


def test_source_published_at_accepts_none() -> None:
    arguments = _valid_arguments()
    arguments["source_published_at"] = None

    evidence = Evidence(**arguments)

    assert evidence.source_published_at is None


def test_source_published_at_accepts_timezone_aware_value() -> None:
    arguments = _valid_arguments()
    arguments["source_published_at"] = _aware_datetime(hour=8)

    evidence = Evidence(**arguments)

    assert evidence.source_published_at == _aware_datetime(hour=8)


def test_cross_field_chronological_order_is_not_hard_validated() -> None:
    arguments = _valid_arguments()
    arguments["captured_at"] = _aware_datetime(hour=10)
    arguments["recorded_at"] = _aware_datetime(hour=9)
    arguments["source_published_at"] = _aware_datetime(hour=12)

    evidence = Evidence(**arguments)

    assert evidence.captured_at == _aware_datetime(hour=10)
    assert evidence.recorded_at == _aware_datetime(hour=9)
    assert evidence.source_published_at == _aware_datetime(hour=12)


# --- Prohibited fields ---


def test_evidence_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(Evidence)}

    prohibited_fields = {
        "raw_payload",
        "payload",
        "content",
        "content_text",
        "content_bytes",
        "binary_data",
        "raw_json",
        "raw_html",
        "raw_response",
        "ingestion_run_id",
        "backfill_job_id",
        "processing_status",
        "processed_at",
        "is_processed",
        "pipeline_status",
        "retry_count",
        "status",
        "availability_status",
        "is_verified",
        "integrity_verified",
        "signature_verified",
        "source_authenticity",
        "human_reviewed",
        "tamper_detected",
        "deleted",
        "unavailable",
        "expired",
        "lost",
        "corrupted",
        "confidence",
        "fact_confidence",
        "extraction_confidence",
        "reliability_score",
        "source_reliability",
        "trust_score",
        "indicator_id",
        "video_id",
        "post_id",
        "property_id",
        "ticker",
        "value",
        "unit",
        "currency",
        "view_count",
        "like_count",
        "comment_count",
        "local_file_path",
        "s3_bucket",
        "s3_key",
        "gcs_bucket",
        "azure_blob_key",
        "database_table",
        "database_primary_key",
        "cdn_url",
        "observation_id",
        "observation_ref",
        "observation_refs",
        "observations",
        "retrieved_at",
        "created_at",
        "valid_from",
        "valid_to",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Observation compatibility ---


def test_evidence_id_can_be_passed_to_observation_evidence_refs() -> None:
    evidence = Evidence(**_valid_arguments())

    observation = Observation(
        observation_id="observation-001",
        normalized_statement="A validated atomic fact.",
        statement_language="en",
        evidence_refs=(evidence.evidence_id,),
        provenance_ref="observation-provenance",
        observed_at=_aware_datetime(),
        recorded_at=_aware_datetime(),
    )

    assert observation.evidence_refs == (evidence.evidence_id,)


def test_observation_does_not_hold_evidence_object() -> None:
    evidence = Evidence(**_valid_arguments())

    observation = Observation(
        observation_id="observation-001",
        normalized_statement="A validated atomic fact.",
        statement_language="en",
        evidence_refs=(evidence.evidence_id,),
        provenance_ref="observation-provenance",
        observed_at=_aware_datetime(),
        recorded_at=_aware_datetime(),
    )

    for value in observation.evidence_refs:
        assert isinstance(value, str)
        assert not isinstance(value, Evidence)


def test_evidence_has_no_reverse_observation_reference() -> None:
    field_names = {field.name for field in fields(Evidence)}

    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "observation_refs" not in field_names
    assert "observations" not in field_names


# --- Raise-only validation ---


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_locator = "atlas-object://artifact/001 "

    arguments = _valid_arguments()
    arguments["artifact_locator"] = original_locator

    with pytest.raises(ValueError):
        Evidence(**arguments)

    assert arguments["artifact_locator"] == original_locator
