"""Canonical Observation core model."""

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


def _validate_aware_datetime(value: object, field_name: str) -> None:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


@dataclass(frozen=True, slots=True, kw_only=True)
class Observation:
    """A domain-independent, atomic, evidence-referenced fact record."""

    observation_id: str
    normalized_statement: str
    statement_language: str
    evidence_refs: tuple[str, ...]
    provenance_ref: str
    observed_at: datetime
    recorded_at: datetime
    occurred_at: datetime | None = None
    source_published_at: datetime | None = None

    def __post_init__(self) -> None:
        _validate_required_string(self.observation_id, "observation_id")
        _validate_required_string(
            self.normalized_statement,
            "normalized_statement",
        )
        _validate_required_string(
            self.statement_language,
            "statement_language",
        )
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

        if self.occurred_at is not None:
            _validate_aware_datetime(self.occurred_at, "occurred_at")

        if self.source_published_at is not None:
            _validate_aware_datetime(
                self.source_published_at,
                "source_published_at",
            )
