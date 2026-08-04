"""Canonical External Run core model."""

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
class ExternalRun:
    """An immutable record of one externally recognized and
    independently distinguishable execution occurrence, at the
    highest logical execution level made available by the external
    system, separate from Atlas's own Provenance occurrence, from any
    External Resource it may produce, and from any AI Model, Prompt
    Specification, Execution Specification, or Configuration
    Specification used to perform it."""

    external_run_id: str
    external_run_kind: str
    external_identifier: str | None = None
    recorded_at: datetime

    def __post_init__(self) -> None:
        _validate_required_string(self.external_run_id, "external_run_id")
        _validate_required_string(self.external_run_kind, "external_run_kind")
        _validate_optional_string(self.external_identifier, "external_identifier")

        _validate_aware_datetime(self.recorded_at, "recorded_at")
