"""Canonical Outcome core model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


def _validate_required_string(value: object, field_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    if not value:
        raise ValueError(f"{field_name} must not be empty")

    if value != value.strip():
        raise ValueError(
            f"{field_name} must not contain leading or trailing whitespace"
        )


def _validate_optional_string(value: object, field_name: str) -> None:
    if value is None:
        return

    _validate_required_string(value, field_name)


def _validate_aware_datetime(value: object, field_name: str) -> None:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


@dataclass(frozen=True, slots=True, kw_only=True)
class Outcome:
    """A Core Canonical, append-only record of what actually occurred."""

    outcome_id: str
    outcome_kind: str
    subject_ref: str
    evidence_refs: tuple[str, ...]
    provenance_ref: str
    observed_at: datetime
    recorded_at: datetime
    forecast_ref: str | None = None

    def __post_init__(self) -> None:
        _validate_required_string(self.outcome_id, "outcome_id")
        _validate_required_string(self.outcome_kind, "outcome_kind")
        _validate_required_string(self.subject_ref, "subject_ref")
        _validate_required_string(self.provenance_ref, "provenance_ref")

        if not isinstance(self.evidence_refs, tuple):
            raise TypeError("evidence_refs must be a tuple")

        if not self.evidence_refs:
            raise ValueError(
                "evidence_refs must contain at least one reference"
            )

        for evidence_ref in self.evidence_refs:
            _validate_required_string(evidence_ref, "evidence_ref")

        if len(set(self.evidence_refs)) != len(self.evidence_refs):
            raise ValueError(
                "evidence_refs must not contain duplicate references"
            )

        _validate_aware_datetime(self.observed_at, "observed_at")
        _validate_aware_datetime(self.recorded_at, "recorded_at")

        _validate_optional_string(self.forecast_ref, "forecast_ref")
