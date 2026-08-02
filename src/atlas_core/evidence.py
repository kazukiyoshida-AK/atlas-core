"""Canonical Evidence core model."""

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


def _validate_optional_aware_datetime(value: object, field_name: str) -> None:
    if value is None:
        return

    _validate_aware_datetime(value, field_name)


@dataclass(frozen=True, slots=True, kw_only=True)
class Evidence:
    """A domain-independent reference to a captured evidence artifact."""

    evidence_id: str
    evidence_kind: str
    source_ref: str
    artifact_locator: str
    provenance_ref: str
    captured_at: datetime
    recorded_at: datetime
    content_selector: str | None = None
    media_type: str | None = None
    content_digest: str | None = None
    digest_algorithm: str | None = None
    byte_length: int | None = None
    source_published_at: datetime | None = None

    def __post_init__(self) -> None:
        _validate_required_string(self.evidence_id, "evidence_id")
        _validate_required_string(self.evidence_kind, "evidence_kind")
        _validate_required_string(self.source_ref, "source_ref")
        _validate_required_string(
            self.artifact_locator,
            "artifact_locator",
        )
        _validate_required_string(self.provenance_ref, "provenance_ref")

        _validate_optional_string(
            self.content_selector,
            "content_selector",
        )
        _validate_optional_string(self.media_type, "media_type")
        _validate_optional_string(self.content_digest, "content_digest")
        _validate_optional_string(
            self.digest_algorithm,
            "digest_algorithm",
        )

        digest_set = self.content_digest is not None
        algorithm_set = self.digest_algorithm is not None

        if digest_set != algorithm_set:
            raise ValueError(
                "content_digest and digest_algorithm must be set together"
            )

        if self.byte_length is not None:
            if isinstance(self.byte_length, bool) or not isinstance(
                self.byte_length,
                int,
            ):
                raise TypeError("byte_length must be an int")

            if self.byte_length < 0:
                raise ValueError("byte_length must not be negative")

        _validate_aware_datetime(self.captured_at, "captured_at")
        _validate_aware_datetime(self.recorded_at, "recorded_at")
        _validate_optional_aware_datetime(
            self.source_published_at,
            "source_published_at",
        )
