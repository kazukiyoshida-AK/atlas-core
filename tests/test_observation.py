from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timezone

import pytest

from atlas_core import Observation


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 2,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    observed_at = _aware_datetime()

    return {
        "observation_id": "observation-001",
        "normalized_statement": (
            "Video reference V had 12,340 views at the observed time."
        ),
        "statement_language": "en",
        "evidence_refs": ("evidence-001",),
        "provenance_ref": "provenance-001",
        "observed_at": observed_at,
        "recorded_at": observed_at,
        "occurred_at": None,
        "source_published_at": None,
    }


def test_observation_can_be_created() -> None:
    arguments = _valid_arguments()

    observation = Observation(**arguments)

    assert observation.observation_id == "observation-001"
    assert observation.normalized_statement == (
        "Video reference V had 12,340 views at the observed time."
    )
    assert observation.statement_language == "en"
    assert observation.evidence_refs == ("evidence-001",)
    assert observation.provenance_ref == "provenance-001"
    assert observation.observed_at == arguments["observed_at"]
    assert observation.recorded_at == arguments["recorded_at"]
    assert observation.occurred_at is None
    assert observation.source_published_at is None


def test_observation_is_exported_from_package_root() -> None:
    from atlas_core.observation import Observation as ModuleObservation

    assert Observation is ModuleObservation


def test_observation_is_immutable() -> None:
    observation = Observation(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        observation.normalized_statement = "Changed statement"


@pytest.mark.parametrize(
    "field_name",
    (
        "observation_id",
        "normalized_statement",
        "statement_language",
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
        Observation(**arguments)


def test_required_string_rejects_non_string() -> None:
    arguments = _valid_arguments()
    arguments["observation_id"] = 123

    with pytest.raises(TypeError):
        Observation(**arguments)


def test_evidence_refs_must_be_a_tuple() -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = ["evidence-001"]

    with pytest.raises(TypeError):
        Observation(**arguments)


def test_evidence_refs_must_not_be_empty() -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = ()

    with pytest.raises(ValueError):
        Observation(**arguments)


@pytest.mark.parametrize(
    "invalid_reference",
    (
        "",
        " ",
        " leading",
        "trailing ",
    ),
)
def test_evidence_refs_reject_invalid_strings(
    invalid_reference: str,
) -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = (invalid_reference,)

    with pytest.raises(ValueError):
        Observation(**arguments)


def test_evidence_refs_reject_non_string_elements() -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = (123,)

    with pytest.raises(TypeError):
        Observation(**arguments)


def test_evidence_refs_reject_duplicates() -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = (
        "evidence-001",
        "evidence-001",
    )

    with pytest.raises(ValueError):
        Observation(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "observed_at",
        "recorded_at",
        "occurred_at",
        "source_published_at",
    ),
)
def test_timestamp_fields_reject_naive_datetime(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = datetime(2026, 8, 2, 10)

    with pytest.raises(ValueError):
        Observation(**arguments)


def test_required_timestamp_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["observed_at"] = "2026-08-02T10:00:00Z"

    with pytest.raises(TypeError):
        Observation(**arguments)


def test_optional_timestamps_accept_timezone_aware_values() -> None:
    occurred_at = _aware_datetime(hour=9)
    source_published_at = _aware_datetime(hour=8)

    arguments = _valid_arguments()
    arguments["occurred_at"] = occurred_at
    arguments["source_published_at"] = source_published_at

    observation = Observation(**arguments)

    assert observation.occurred_at == occurred_at
    assert observation.source_published_at == source_published_at


def test_cross_field_chronological_order_is_not_hard_validated() -> None:
    arguments = _valid_arguments()
    arguments["observed_at"] = _aware_datetime(hour=10)
    arguments["recorded_at"] = _aware_datetime(hour=9)
    arguments["occurred_at"] = _aware_datetime(hour=11)
    arguments["source_published_at"] = _aware_datetime(hour=12)

    observation = Observation(**arguments)

    assert observation.observed_at == _aware_datetime(hour=10)
    assert observation.recorded_at == _aware_datetime(hour=9)
    assert observation.occurred_at == _aware_datetime(hour=11)
    assert observation.source_published_at == _aware_datetime(hour=12)


def test_observation_has_exact_approved_field_set() -> None:
    field_names = tuple(field.name for field in fields(Observation))

    assert field_names == (
        "observation_id",
        "normalized_statement",
        "statement_language",
        "evidence_refs",
        "provenance_ref",
        "observed_at",
        "recorded_at",
        "occurred_at",
        "source_published_at",
    )


def test_observation_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(Observation)}

    prohibited_fields = {
        "source_id",
        "indicator_id",
        "raw_ingestion_record_id",
        "value",
        "unit",
        "currency",
        "raw_payload",
        "domain_payload",
        "metadata",
        "confidence",
        "status",
        "valid_from",
        "valid_to",
        "provider",
        "model",
    }

    assert field_names.isdisjoint(prohibited_fields)
