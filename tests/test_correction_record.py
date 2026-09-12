from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timezone

import pytest

from atlas_core import CorrectionRecord


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 2,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "correction_id": "correction-001",
        "subject_concept": "Observation",
        "superseded_ref": "observation-001",
        "superseding_ref": "observation-002",
        "correction_kind": "factual-correction",
        "provenance_ref": "provenance-001",
        "recorded_at": _aware_datetime(),
    }


def test_correction_record_can_be_created() -> None:
    arguments = _valid_arguments()

    correction_record = CorrectionRecord(**arguments)

    assert correction_record.correction_id == "correction-001"
    assert correction_record.subject_concept == "Observation"
    assert correction_record.superseded_ref == "observation-001"
    assert correction_record.superseding_ref == "observation-002"
    assert correction_record.correction_kind == "factual-correction"
    assert correction_record.provenance_ref == "provenance-001"
    assert correction_record.recorded_at == arguments["recorded_at"]


def test_correction_record_is_exported_from_package_root() -> None:
    from atlas_core.correction_record import (
        CorrectionRecord as ModuleCorrectionRecord,
    )

    assert CorrectionRecord is ModuleCorrectionRecord


def test_correction_record_is_immutable() -> None:
    correction_record = CorrectionRecord(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        correction_record.correction_kind = "changed"


def test_correction_record_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        CorrectionRecord(*arguments.values())  # type: ignore[misc]


def test_correction_record_has_slots() -> None:
    correction_record = CorrectionRecord(**_valid_arguments())

    assert not hasattr(correction_record, "__dict__")


def test_correction_record_has_exact_approved_field_set() -> None:
    field_names = tuple(field.name for field in fields(CorrectionRecord))

    assert field_names == (
        "correction_id",
        "subject_concept",
        "superseded_ref",
        "superseding_ref",
        "correction_kind",
        "provenance_ref",
        "recorded_at",
    )


@pytest.mark.parametrize(
    "field_name",
    (
        "correction_id",
        "superseded_ref",
        "superseding_ref",
        "correction_kind",
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
        CorrectionRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "correction_id",
        "subject_concept",
        "superseded_ref",
        "superseding_ref",
        "correction_kind",
        "provenance_ref",
    ),
)
def test_required_strings_reject_non_string(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = 123

    with pytest.raises(TypeError):
        CorrectionRecord(**arguments)


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 2, 10)

    with pytest.raises(ValueError):
        CorrectionRecord(**arguments)


def test_recorded_at_accepts_timezone_aware_value() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=8)

    correction_record = CorrectionRecord(**arguments)

    assert correction_record.recorded_at == _aware_datetime(hour=8)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-02T10:00:00Z"

    with pytest.raises(TypeError):
        CorrectionRecord(**arguments)


@pytest.mark.parametrize(
    "allowed_subject_concept",
    ("Evidence", "Observation", "Outcome"),
)
def test_allowed_subject_concepts_are_accepted(
    allowed_subject_concept: str,
) -> None:
    arguments = _valid_arguments()
    arguments["subject_concept"] = allowed_subject_concept

    correction_record = CorrectionRecord(**arguments)

    assert correction_record.subject_concept == allowed_subject_concept


@pytest.mark.parametrize(
    "disallowed_subject_concept",
    ("Forecast", "Evaluation", "Actor", "Provenance", "outcome", "evidence"),
)
def test_disallowed_subject_concepts_are_rejected(
    disallowed_subject_concept: str,
) -> None:
    arguments = _valid_arguments()
    arguments["subject_concept"] = disallowed_subject_concept

    with pytest.raises(ValueError):
        CorrectionRecord(**arguments)


def test_identical_superseded_and_superseding_ref_is_rejected() -> None:
    arguments = _valid_arguments()
    arguments["superseding_ref"] = arguments["superseded_ref"]

    with pytest.raises(ValueError):
        CorrectionRecord(**arguments)


def test_correction_record_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(CorrectionRecord)}

    prohibited_fields = {
        "relationship_type",
        "edge_type",
        "target_concept",
        "predicate",
        "status",
        "confidence",
        "deleted",
        "overwritten_at",
    }

    assert field_names.isdisjoint(prohibited_fields)
