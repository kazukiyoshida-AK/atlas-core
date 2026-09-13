import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from atlas_core import CorrectionRecord, Outcome
from atlas_core.store import RecordConflictError, RecordCorruptedError, WriterLockError
from atlas_core.store.write import (
    _LOCK_FILE_NAME,
    register_correction_record,
    register_outcome,
)


def _aware_datetime(hour: int = 10, tz: timezone = timezone.utc) -> datetime:
    return datetime(2026, 8, 2, hour, tzinfo=tz)


def _valid_outcome(**overrides: object) -> Outcome:
    arguments: dict[str, object] = {
        "outcome_id": "outcome-001",
        "outcome_kind": "metric-observed",
        "subject_ref": "video-001",
        "evidence_refs": ("evidence-001",),
        "provenance_ref": "provenance-001",
        "observed_at": _aware_datetime(),
        "recorded_at": _aware_datetime(),
        "forecast_ref": None,
    }
    arguments.update(overrides)
    return Outcome(**arguments)  # type: ignore[arg-type]


def _valid_correction_record(**overrides: object) -> CorrectionRecord:
    arguments: dict[str, object] = {
        "correction_id": "correction-001",
        "subject_concept": "Outcome",
        "superseded_ref": "outcome-001",
        "superseding_ref": "outcome-002",
        "correction_kind": "value-correction",
        "provenance_ref": "provenance-002",
        "recorded_at": _aware_datetime(),
    }
    arguments.update(overrides)
    return CorrectionRecord(**arguments)  # type: ignore[arg-type]


def _outcome_file(store_root: Path, outcome_id: str) -> Path:
    import hashlib

    digest = hashlib.sha256(outcome_id.encode("utf-8")).hexdigest()
    return store_root / "outcomes" / f"{digest}.json"


def test_register_outcome_creates_expected_file(tmp_path: Path) -> None:
    outcome = _valid_outcome()

    register_outcome(outcome, store_root=tmp_path)

    path = _outcome_file(tmp_path, outcome.outcome_id)
    assert path.exists()

    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert envelope["record"]["outcome_id"] == "outcome-001"
    assert envelope["schema_version"] == 1
    assert envelope["store_schema_version"] == 1
    assert envelope["digest_algorithm"] == "sha256"
    assert isinstance(envelope["content_digest"], str) and len(envelope["content_digest"]) == 64
    assert "registered_at" in envelope


def test_register_outcome_returns_the_outcome(tmp_path: Path) -> None:
    outcome = _valid_outcome()

    result = register_outcome(outcome, store_root=tmp_path)

    assert result is outcome


def test_register_correction_record_creates_expected_file(tmp_path: Path) -> None:
    correction = _valid_correction_record()

    register_correction_record(correction, store_root=tmp_path)

    import hashlib

    digest = hashlib.sha256(correction.correction_id.encode("utf-8")).hexdigest()
    path = tmp_path / "corrections" / f"{digest}.json"
    assert path.exists()

    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert envelope["record"]["correction_id"] == "correction-001"
    assert envelope["record"]["subject_concept"] == "Outcome"


def test_register_outcome_is_idempotent_for_identical_resubmission(tmp_path: Path) -> None:
    outcome = _valid_outcome()

    register_outcome(outcome, store_root=tmp_path)
    result = register_outcome(_valid_outcome(), store_root=tmp_path)

    assert result.outcome_id == outcome.outcome_id
    path = _outcome_file(tmp_path, outcome.outcome_id)
    assert path.exists()


def test_register_outcome_rejects_conflicting_resubmission(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)

    with pytest.raises(RecordConflictError):
        register_outcome(_valid_outcome(outcome_kind="different-kind"), store_root=tmp_path)


def test_register_outcome_conflict_leaves_existing_file_unchanged(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)
    path = _outcome_file(tmp_path, "outcome-001")
    original_bytes = path.read_bytes()

    with pytest.raises(RecordConflictError):
        register_outcome(_valid_outcome(outcome_kind="different-kind"), store_root=tmp_path)

    assert path.read_bytes() == original_bytes


def test_register_correction_record_rejects_conflicting_resubmission(tmp_path: Path) -> None:
    register_correction_record(_valid_correction_record(), store_root=tmp_path)

    with pytest.raises(RecordConflictError):
        register_correction_record(
            _valid_correction_record(correction_kind="different-kind"), store_root=tmp_path
        )


def test_register_outcome_detects_preexisting_corruption(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)
    path = _outcome_file(tmp_path, "outcome-001")

    envelope = json.loads(path.read_text(encoding="utf-8"))
    envelope["record"]["outcome_kind"] = "tampered"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    with pytest.raises(RecordCorruptedError):
        register_outcome(_valid_outcome(), store_root=tmp_path)


def test_write_module_has_no_update_or_delete_functions() -> None:
    import atlas_core.store.write as write_module

    public_names = {name for name in dir(write_module) if not name.startswith("_")}
    assert not any("update" in name for name in public_names)
    assert not any("delete" in name for name in public_names)


def test_no_temp_files_left_after_successful_registration(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)

    leftovers = list((tmp_path / "outcomes").glob(".*.tmp-*"))
    assert leftovers == []


def test_no_temp_files_left_after_conflict(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)

    with pytest.raises(RecordConflictError):
        register_outcome(_valid_outcome(outcome_kind="different-kind"), store_root=tmp_path)

    leftovers = list((tmp_path / "outcomes").glob(".*.tmp-*"))
    assert leftovers == []


def test_timezone_is_normalized_to_utc_in_storage(tmp_path: Path) -> None:
    plus_nine = timezone(timedelta(hours=9))
    outcome = _valid_outcome(
        observed_at=_aware_datetime(hour=19, tz=plus_nine),
        recorded_at=_aware_datetime(hour=19, tz=plus_nine),
    )

    register_outcome(outcome, store_root=tmp_path)

    path = _outcome_file(tmp_path, outcome.outcome_id)
    envelope = json.loads(path.read_text(encoding="utf-8"))
    assert envelope["record"]["observed_at"].endswith("+00:00")
    assert envelope["record"]["observed_at"].startswith("2026-08-02T10:00:00")


def test_writer_lock_file_removed_after_successful_registration(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)

    assert not (tmp_path / _LOCK_FILE_NAME).exists()


def test_writer_lock_file_removed_after_conflict_error(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)

    with pytest.raises(RecordConflictError):
        register_outcome(_valid_outcome(outcome_kind="different-kind"), store_root=tmp_path)

    assert not (tmp_path / _LOCK_FILE_NAME).exists()


def test_writer_lock_rejects_a_second_writer(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    lock_path = tmp_path / _LOCK_FILE_NAME
    # os.getpid() of this very test process is guaranteed to be alive.
    lock_path.write_text(str(os.getpid()), encoding="ascii")

    with pytest.raises(WriterLockError):
        register_outcome(_valid_outcome(), store_root=tmp_path)

    # The lock this call did not create must not be removed by it.
    assert lock_path.exists()


@pytest.mark.skipif(os.name != "posix", reason="POSIX-only stale lock reclamation")
def test_writer_lock_reclaims_a_confirmed_dead_pid(tmp_path: Path) -> None:
    import subprocess
    import sys

    tmp_path.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run([sys.executable, "-c", "pass"], check=True)
    dead_pid = completed.pid if hasattr(completed, "pid") else None
    # subprocess.run does not expose pid after completion on all versions;
    # fall back to Popen to obtain a pid guaranteed dead after wait().
    if dead_pid is None:
        proc = subprocess.Popen([sys.executable, "-c", "pass"])
        proc.wait()
        dead_pid = proc.pid

    lock_path = tmp_path / _LOCK_FILE_NAME
    lock_path.write_text(str(dead_pid), encoding="ascii")

    register_outcome(_valid_outcome(), store_root=tmp_path)

    assert not lock_path.exists()


@pytest.mark.skipif(os.name == "posix", reason="exercises the non-POSIX fail-safe path")
def test_writer_lock_fails_safe_on_non_posix_platform(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    lock_path = tmp_path / _LOCK_FILE_NAME
    lock_path.write_text("999999999", encoding="ascii")

    with pytest.raises(WriterLockError):
        register_outcome(_valid_outcome(), store_root=tmp_path)

    assert lock_path.exists()
