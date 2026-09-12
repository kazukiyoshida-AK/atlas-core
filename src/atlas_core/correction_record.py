"""Canonical CorrectionRecord core model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

ALLOWED_SUBJECT_CONCEPTS = ("Evidence", "Observation", "Outcome")


def _validate_required_string(value: object, field_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    if not value:
        raise ValueError(f"{field_name} must not be empty")

    if value != value.strip():
        raise ValueError(
            f"{field_name} must not contain leading or trailing whitespace"
        )


def _validate_aware_datetime(value: object, field_name: str) -> None:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


@dataclass(frozen=True, slots=True, kw_only=True)
class CorrectionRecord:
    """A Core Canonical, append-only correction/supersession relationship."""

    correction_id: str
    subject_concept: str
    superseded_ref: str
    superseding_ref: str
    correction_kind: str
    provenance_ref: str
    recorded_at: datetime

    def __post_init__(self) -> None:
        _validate_required_string(self.correction_id, "correction_id")
        _validate_required_string(self.subject_concept, "subject_concept")

        if self.subject_concept not in ALLOWED_SUBJECT_CONCEPTS:
            raise ValueError(
                "subject_concept must be one of: "
                + ", ".join(ALLOWED_SUBJECT_CONCEPTS)
            )

        _validate_required_string(self.superseded_ref, "superseded_ref")
        _validate_required_string(self.superseding_ref, "superseding_ref")

        if self.superseded_ref == self.superseding_ref:
            raise ValueError(
                "superseded_ref and superseding_ref must not be the same "
                "reference"
            )

        _validate_required_string(self.correction_kind, "correction_kind")
        _validate_required_string(self.provenance_ref, "provenance_ref")

        _validate_aware_datetime(self.recorded_at, "recorded_at")
