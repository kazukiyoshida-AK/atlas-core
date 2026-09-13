"""Core File Store read path (ACR-029 / ACI-CORE-002).

Read-only. Never imports atlas_core.store.write, so any caller (Head
included) that imports only this module never touches the write path.
Every read re-verifies the record's content_digest; corruption is never
silently trusted.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from atlas_core.correction_record import CorrectionRecord
from atlas_core.outcome import Outcome
from atlas_core.store import (
    DEFAULT_STORE_ROOT,
    _path_for,
    _read_envelope_json,
    _verify_and_get_ordered_record,
)


def _outcome_from_ordered(ordered: dict[str, object]) -> Outcome:
    return Outcome(
        outcome_id=ordered["outcome_id"],  # type: ignore[arg-type]
        outcome_kind=ordered["outcome_kind"],  # type: ignore[arg-type]
        subject_ref=ordered["subject_ref"],  # type: ignore[arg-type]
        evidence_refs=tuple(ordered["evidence_refs"]),  # type: ignore[arg-type]
        provenance_ref=ordered["provenance_ref"],  # type: ignore[arg-type]
        observed_at=datetime.fromisoformat(ordered["observed_at"]),  # type: ignore[arg-type]
        recorded_at=datetime.fromisoformat(ordered["recorded_at"]),  # type: ignore[arg-type]
        forecast_ref=ordered["forecast_ref"],  # type: ignore[arg-type]
    )


def _correction_record_from_ordered(ordered: dict[str, object]) -> CorrectionRecord:
    return CorrectionRecord(
        correction_id=ordered["correction_id"],  # type: ignore[arg-type]
        subject_concept=ordered["subject_concept"],  # type: ignore[arg-type]
        superseded_ref=ordered["superseded_ref"],  # type: ignore[arg-type]
        superseding_ref=ordered["superseding_ref"],  # type: ignore[arg-type]
        correction_kind=ordered["correction_kind"],  # type: ignore[arg-type]
        provenance_ref=ordered["provenance_ref"],  # type: ignore[arg-type]
        recorded_at=datetime.fromisoformat(ordered["recorded_at"]),  # type: ignore[arg-type]
    )


def get_outcome(
    outcome_id: str, *, store_root: Path | str = DEFAULT_STORE_ROOT
) -> Outcome | None:
    path = _path_for("outcomes", outcome_id, Path(store_root))
    if not path.exists():
        return None

    envelope = _read_envelope_json(path)
    ordered = _verify_and_get_ordered_record(envelope, Outcome)
    return _outcome_from_ordered(ordered)


def get_correction_record(
    correction_id: str, *, store_root: Path | str = DEFAULT_STORE_ROOT
) -> CorrectionRecord | None:
    path = _path_for("corrections", correction_id, Path(store_root))
    if not path.exists():
        return None

    envelope = _read_envelope_json(path)
    ordered = _verify_and_get_ordered_record(envelope, CorrectionRecord)
    return _correction_record_from_ordered(ordered)


def list_outcomes(*, store_root: Path | str = DEFAULT_STORE_ROOT) -> tuple[Outcome, ...]:
    directory = Path(store_root) / "outcomes"
    if not directory.is_dir():
        return ()

    results = []
    for path in sorted(directory.glob("*.json")):
        envelope = _read_envelope_json(path)
        ordered = _verify_and_get_ordered_record(envelope, Outcome)
        results.append(_outcome_from_ordered(ordered))
    return tuple(results)


def list_correction_records(
    *, store_root: Path | str = DEFAULT_STORE_ROOT
) -> tuple[CorrectionRecord, ...]:
    directory = Path(store_root) / "corrections"
    if not directory.is_dir():
        return ()

    results = []
    for path in sorted(directory.glob("*.json")):
        envelope = _read_envelope_json(path)
        ordered = _verify_and_get_ordered_record(envelope, CorrectionRecord)
        results.append(_correction_record_from_ordered(ordered))
    return tuple(results)
