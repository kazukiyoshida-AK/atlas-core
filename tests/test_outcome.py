from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timezone

import pytest

from atlas_core import Outcome


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
        "outcome_id": "outcome-001",
        "outcome_kind": "metric-observed",
        "subject_ref": "video-001",
        "evidence_refs": ("evidence-001",),
        "provenance_ref": "provenance-001",
        "observed_at": observed_at,
        "recorded_at": observed_at,
        "forecast_ref": None,
    }


def test_outcome_can_be_created() -> None:
    arguments = _valid_arguments()

    outcome = Outcome(**arguments)

    assert outcome.outcome_id == "outcome-001"
    assert outcome.outcome_kind == "metric-observed"
    assert outcome.subject_ref == "video-001"
    assert outcome.evidence_refs == ("evidence-001",)
    assert outcome.provenance_ref == "provenance-001"
    assert outcome.observed_at == arguments["observed_at"]
    assert outcome.recorded_at == arguments["recorded_at"]
    assert outcome.forecast_ref is None


def test_outcome_is_exported_from_package_root() -> None:
    from atlas_core.outcome import Outcome as ModuleOutcome

    assert Outcome is ModuleOutcome


def test_outcome_is_immutable() -> None:
    outcome = Outcome(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        outcome.outcome_kind = "changed"


def test_outcome_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        Outcome(*arguments.values())  # type: ignore[misc]


def test_outcome_has_slots() -> None:
    outcome = Outcome(**_valid_arguments())

    assert not hasattr(outcome, "__dict__")


def test_outcome_has_exact_approved_field_set() -> None:
    field_names = tuple(field.name for field in fields(Outcome))

    assert field_names == (
        "outcome_id",
        "outcome_kind",
        "subject_ref",
        "evidence_refs",
        "provenance_ref",
        "observed_at",
        "recorded_at",
        "forecast_ref",
    )


@pytest.mark.parametrize(
    "field_name",
    (
        "outcome_id",
        "outcome_kind",
        "subject_ref",
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
        Outcome(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "outcome_id",
        "outcome_kind",
        "subject_ref",
        "provenance_ref",
    ),
)
def test_required_strings_reject_non_string(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = 123

    with pytest.raises(TypeError):
        Outcome(**arguments)


def test_evidence_refs_must_be_a_tuple() -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = ["evidence-001"]

    with pytest.raises(TypeError):
        Outcome(**arguments)


def test_evidence_refs_must_not_be_empty() -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = ()

    with pytest.raises(ValueError):
        Outcome(**arguments)


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
        Outcome(**arguments)


def test_evidence_refs_reject_non_string_elements() -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = (123,)

    with pytest.raises(TypeError):
        Outcome(**arguments)


def test_evidence_refs_reject_duplicates() -> None:
    arguments = _valid_arguments()
    arguments["evidence_refs"] = (
        "evidence-001",
        "evidence-001",
    )

    with pytest.raises(ValueError):
        Outcome(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("observed_at", "recorded_at"),
)
def test_timestamp_fields_reject_naive_datetime(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = datetime(2026, 8, 2, 10)

    with pytest.raises(ValueError):
        Outcome(**arguments)


@pytest.mark.parametrize("field_name", ("observed_at", "recorded_at"))
def test_required_timestamp_rejects_non_datetime(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "2026-08-02T10:00:00Z"

    with pytest.raises(TypeError):
        Outcome(**arguments)


def test_forecast_ref_defaults_to_none() -> None:
    arguments = _valid_arguments()
    del arguments["forecast_ref"]

    outcome = Outcome(**arguments)

    assert outcome.forecast_ref is None


def test_forecast_ref_accepts_reference_string() -> None:
    arguments = _valid_arguments()
    arguments["forecast_ref"] = "forecast-001"

    outcome = Outcome(**arguments)

    assert outcome.forecast_ref == "forecast-001"


@pytest.mark.parametrize(
    "invalid_value",
    ("", " ", " leading", "trailing "),
)
def test_forecast_ref_rejects_invalid_string(invalid_value: str) -> None:
    arguments = _valid_arguments()
    arguments["forecast_ref"] = invalid_value

    with pytest.raises(ValueError):
        Outcome(**arguments)


def test_outcome_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(Outcome)}

    prohibited_fields = {
        "forecast",
        "evaluation",
        "evaluation_verdict",
        "verdict",
        "evaluation_ref",
        "status",
        "confidence",
        "value",
        "unit",
        "currency",
    }

    assert field_names.isdisjoint(prohibited_fields)


def test_outcome_has_no_mutation_or_delete_methods() -> None:
    outcome = Outcome(**_valid_arguments())

    assert not hasattr(outcome, "delete")
    assert not hasattr(outcome, "overwrite")
    assert not hasattr(outcome, "update")
