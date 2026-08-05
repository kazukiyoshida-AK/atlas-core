"""Canonical Artifact core model."""

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
class Artifact:
    """An immutable, independently distinguishable representation
    revision of information or content that Atlas deliberately
    retained or registered for durable reference, separate from
    Provenance, Source, External Resource, Observation, and
    Evidence."""

    artifact_id: str
    artifact_kind: str
    content_digest: str | None = None
    digest_algorithm: str | None = None
    media_type: str | None = None
    artifact_locator: str | None = None
    recorded_at: datetime

    def __post_init__(self) -> None:
        _validate_required_string(self.artifact_id, "artifact_id")
        _validate_required_string(self.artifact_kind, "artifact_kind")

        _validate_optional_string(self.content_digest, "content_digest")
        _validate_optional_string(self.digest_algorithm, "digest_algorithm")
        _validate_optional_string(self.media_type, "media_type")
        _validate_optional_string(self.artifact_locator, "artifact_locator")

        digest_set = self.content_digest is not None
        algorithm_set = self.digest_algorithm is not None

        if digest_set != algorithm_set:
            raise ValueError(
                "content_digest and digest_algorithm must be set together"
            )

        _validate_aware_datetime(self.recorded_at, "recorded_at")
