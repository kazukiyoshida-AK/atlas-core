"""Shared, internal support for the Core File Store (ACR-029 / ACI-CORE-002).

This module holds only what both ``atlas_core.store.write`` and
``atlas_core.store.read`` need in common (exceptions, canonical
serialization, digest computation, path derivation). It deliberately does
not import either of those submodules and exposes no public register_*/
get_*/list_* names itself, so that importing ``atlas_core.store.read``
never pulls in the write path.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import fields
from datetime import datetime, timezone
from pathlib import Path

DIGEST_ALGORITHM = "sha256"
SCHEMA_VERSION = 1
STORE_SCHEMA_VERSION = 1

DEFAULT_STORE_ROOT = Path(__file__).resolve().parents[3] / "canonical_store"

_ENVELOPE_KEYS = frozenset(
    {
        "schema_version",
        "record",
        "content_digest",
        "digest_algorithm",
        "store_schema_version",
        "registered_at",
    }
)


class OutcomeStoreError(Exception):
    """Base class for all Core File Store errors."""


class RecordConflictError(OutcomeStoreError):
    """Same canonical ID, different content. Never silently overwritten."""


class RecordCorruptedError(OutcomeStoreError):
    """On-disk content is malformed or fails digest self-verification."""


class WriterLockError(OutcomeStoreError):
    """Writer lock could not be acquired (multi-writer or indeterminate)."""


class UnsupportedStoreFilesystemError(OutcomeStoreError):
    """The target filesystem does not support the required atomic primitive."""


def _utc_isoformat(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _to_json_safe(value: object) -> object:
    if isinstance(value, datetime):
        return _utc_isoformat(value)
    return value


def _ordered_dict_from_instance(instance: object) -> dict[str, object]:
    return {
        field.name: _to_json_safe(getattr(instance, field.name))
        for field in fields(instance)  # type: ignore[arg-type]
    }


def _ordered_dict_from_raw(raw_record: object, cls: type) -> dict[str, object]:
    if not isinstance(raw_record, dict):
        raise RecordCorruptedError("record must be a JSON object")

    expected_keys = {field.name for field in fields(cls)}
    actual_keys = set(raw_record.keys())
    if actual_keys != expected_keys:
        raise RecordCorruptedError(
            f"record fields do not match {cls.__name__}: "
            f"expected {sorted(expected_keys)}, got {sorted(actual_keys)}"
        )

    return {field.name: raw_record[field.name] for field in fields(cls)}


def _canonical_bytes_from_ordered(ordered: dict[str, object]) -> bytes:
    return json.dumps(ordered, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _compute_digest_from_ordered(ordered: dict[str, object]) -> str:
    return hashlib.sha256(_canonical_bytes_from_ordered(ordered)).hexdigest()


def _path_for(kind: str, record_id: str, store_root: Path) -> Path:
    digest_hex = hashlib.sha256(record_id.encode("utf-8")).hexdigest()
    return Path(store_root) / kind / f"{digest_hex}.json"


def _read_envelope_json(path: Path) -> dict[str, object]:
    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RecordCorruptedError(f"unable to read {path}: {exc}") from exc

    try:
        envelope = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise RecordCorruptedError(f"invalid JSON in {path}: {exc}") from exc

    if not isinstance(envelope, dict) or set(envelope.keys()) != set(_ENVELOPE_KEYS):
        raise RecordCorruptedError(
            f"envelope in {path} does not have the exact required keys "
            f"{sorted(_ENVELOPE_KEYS)}"
        )

    return envelope


def _verify_and_get_ordered_record(
    envelope: dict[str, object], cls: type
) -> dict[str, object]:
    ordered = _ordered_dict_from_raw(envelope["record"], cls)
    expected_digest = _compute_digest_from_ordered(ordered)

    stored_digest = envelope.get("content_digest")
    stored_algorithm = envelope.get("digest_algorithm")

    if stored_algorithm != DIGEST_ALGORITHM:
        raise RecordCorruptedError(
            f"unsupported or missing digest_algorithm: {stored_algorithm!r}"
        )

    if stored_digest != expected_digest:
        raise RecordCorruptedError(
            "content_digest does not match recomputed digest "
            "(stored record may be corrupted)"
        )

    return ordered


def _build_envelope(
    ordered_record: dict[str, object], registered_at: datetime
) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "record": ordered_record,
        "content_digest": _compute_digest_from_ordered(ordered_record),
        "digest_algorithm": DIGEST_ALGORITHM,
        "store_schema_version": STORE_SCHEMA_VERSION,
        "registered_at": _utc_isoformat(registered_at),
    }
