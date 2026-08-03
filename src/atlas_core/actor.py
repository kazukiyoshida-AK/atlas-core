"""Canonical Actor core model."""

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
class Actor:
    """A stable Human or Non-human attribution identity to which Atlas
    attributes performance of an activity."""

    actor_id: str
    actor_kind: str
    canonical_name: str
    recorded_at: datetime

    def __post_init__(self) -> None:
        _validate_required_string(self.actor_id, "actor_id")
        _validate_required_string(self.actor_kind, "actor_kind")
        _validate_required_string(self.canonical_name, "canonical_name")

        _validate_aware_datetime(self.recorded_at, "recorded_at")
