import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from atlas_core import CorrectionRecord, Outcome
from atlas_core.store import RecordCorruptedError
from atlas_core.store.read import (
    get_correction_record,
    get_outcome,
    list_correction_records,
    list_outcomes,
)
from atlas_core.store.write import register_correction_record, register_outcome


def _aware_datetime(hour: int = 10) -> datetime:
    return datetime(2026, 8, 2, hour, tzinfo=timezone.utc)


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


def test_get_outcome_returns_none_when_missing(tmp_path: Path) -> None:
    assert get_outcome("does-not-exist", store_root=tmp_path) is None


def test_get_correction_record_returns_none_when_missing(tmp_path: Path) -> None:
    assert get_correction_record("does-not-exist", store_root=tmp_path) is None


def test_get_outcome_roundtrips_registered_value(tmp_path: Path) -> None:
    outcome = _valid_outcome()
    register_outcome(outcome, store_root=tmp_path)

    result = get_outcome(outcome.outcome_id, store_root=tmp_path)

    assert result is not None
    assert result.outcome_id == outcome.outcome_id
    assert result.outcome_kind == outcome.outcome_kind
    assert result.subject_ref == outcome.subject_ref
    assert result.evidence_refs == outcome.evidence_refs
    assert result.provenance_ref == outcome.provenance_ref
    assert result.observed_at == outcome.observed_at
    assert result.recorded_at == outcome.recorded_at
    assert result.forecast_ref == outcome.forecast_ref


def test_get_correction_record_roundtrips_registered_value(tmp_path: Path) -> None:
    correction = _valid_correction_record()
    register_correction_record(correction, store_root=tmp_path)

    result = get_correction_record(correction.correction_id, store_root=tmp_path)

    assert result is not None
    assert result.correction_id == correction.correction_id
    assert result.subject_concept == correction.subject_concept
    assert result.superseded_ref == correction.superseded_ref
    assert result.superseding_ref == correction.superseding_ref
    assert result.correction_kind == correction.correction_kind
    assert result.provenance_ref == correction.provenance_ref
    assert result.recorded_at == correction.recorded_at


def test_list_outcomes_is_empty_when_directory_missing(tmp_path: Path) -> None:
    assert list_outcomes(store_root=tmp_path) == ()


def test_list_correction_records_is_empty_when_directory_missing(tmp_path: Path) -> None:
    assert list_correction_records(store_root=tmp_path) == ()


def test_list_outcomes_returns_all_registered(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(outcome_id="outcome-a"), store_root=tmp_path)
    register_outcome(_valid_outcome(outcome_id="outcome-b"), store_root=tmp_path)

    results = list_outcomes(store_root=tmp_path)

    assert {outcome.outcome_id for outcome in results} == {"outcome-a", "outcome-b"}


def test_list_correction_records_returns_all_registered(tmp_path: Path) -> None:
    register_correction_record(
        _valid_correction_record(correction_id="correction-a"), store_root=tmp_path
    )
    register_correction_record(
        _valid_correction_record(correction_id="correction-b"), store_root=tmp_path
    )

    results = list_correction_records(store_root=tmp_path)

    assert {correction.correction_id for correction in results} == {
        "correction-a",
        "correction-b",
    }


def test_get_outcome_detects_invalid_json(tmp_path: Path) -> None:
    path = _outcome_file(tmp_path, "outcome-001")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(RecordCorruptedError):
        get_outcome("outcome-001", store_root=tmp_path)


def test_get_outcome_detects_digest_tampering(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)
    path = _outcome_file(tmp_path, "outcome-001")

    envelope = json.loads(path.read_text(encoding="utf-8"))
    envelope["content_digest"] = "0" * 64
    path.write_text(json.dumps(envelope), encoding="utf-8")

    with pytest.raises(RecordCorruptedError):
        get_outcome("outcome-001", store_root=tmp_path)


def test_get_outcome_detects_record_field_tampering(tmp_path: Path) -> None:
    register_outcome(_valid_outcome(), store_root=tmp_path)
    path = _outcome_file(tmp_path, "outcome-001")

    envelope = json.loads(path.read_text(encoding="utf-8"))
    envelope["record"]["outcome_kind"] = "tampered-without-updating-digest"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    with pytest.raises(RecordCorruptedError):
        get_outcome("outcome-001", store_root=tmp_path)


def test_get_outcome_detects_missing_envelope_keys(tmp_path: Path) -> None:
    path = _outcome_file(tmp_path, "outcome-001")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"record": {}}), encoding="utf-8")

    with pytest.raises(RecordCorruptedError):
        get_outcome("outcome-001", store_root=tmp_path)


def test_importing_read_module_does_not_import_write_module() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src_path = str(repo_root / "src")
    env = dict(os.environ)
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not existing else f"{src_path}{os.pathsep}{existing}"

    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import atlas_core.store.read; "
            "print('atlas_core.store.write' in sys.modules)",
        ],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )

    assert completed.stdout.strip() == "False"
