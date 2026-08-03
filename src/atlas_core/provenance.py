"""Canonical Provenance core model."""

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


def _validate_reference_tuple(value: object, field_name: str) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")

    for element in value:
        _validate_required_string(element, f"{field_name} element")

    if len(set(value)) != len(value):
        raise ValueError(f"{field_name} must not contain duplicate references")


def _validate_aware_datetime(value: object, field_name: str) -> None:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


@dataclass(frozen=True, slots=True, kw_only=True)
class Provenance:
    """A completed, domain-independent activity lineage record."""

    provenance_id: str
    activity_kind: str
    actor_ref: str
    started_at: datetime
    completed_at: datetime
    recorded_at: datetime
    input_refs: tuple[str, ...] = ()
    parent_provenance_refs: tuple[str, ...] = ()
    execution_ref: str | None = None
    model_ref: str | None = None
    prompt_ref: str | None = None
    configuration_ref: str | None = None
    external_run_ref: str | None = None

    def __post_init__(self) -> None:
        _validate_required_string(self.provenance_id, "provenance_id")
        _validate_required_string(self.activity_kind, "activity_kind")
        _validate_required_string(self.actor_ref, "actor_ref")

        _validate_aware_datetime(self.started_at, "started_at")
        _validate_aware_datetime(self.completed_at, "completed_at")
        _validate_aware_datetime(self.recorded_at, "recorded_at")

        _validate_reference_tuple(self.input_refs, "input_refs")
        _validate_reference_tuple(
            self.parent_provenance_refs,
            "parent_provenance_refs",
        )

        if self.provenance_id in self.parent_provenance_refs:
            raise ValueError(
                "parent_provenance_refs must not contain a self-reference"
            )

        _validate_optional_string(self.execution_ref, "execution_ref")
        _validate_optional_string(self.model_ref, "model_ref")
        _validate_optional_string(self.prompt_ref, "prompt_ref")
        _validate_optional_string(
            self.configuration_ref,
            "configuration_ref",
        )
        _validate_optional_string(
            self.external_run_ref,
            "external_run_ref",
        )
