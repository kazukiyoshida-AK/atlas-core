"""Canonical External Resource core model."""

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
class ExternalResource:
    """An immutable record of one durable and independently
    re-referenceable object identity authoritatively recognized by an
    external system, independent of any specific execution, mutable
    observed state, or Artifact representation of that object."""

    external_resource_id: str
    external_resource_kind: str
    external_identifier: str | None = None
    resource_locator: str | None = None
    recorded_at: datetime

    def __post_init__(self) -> None:
        _validate_required_string(self.external_resource_id, "external_resource_id")
        _validate_required_string(
            self.external_resource_kind, "external_resource_kind"
        )
        _validate_optional_string(self.external_identifier, "external_identifier")
        _validate_optional_string(self.resource_locator, "resource_locator")

        _validate_aware_datetime(self.recorded_at, "recorded_at")
