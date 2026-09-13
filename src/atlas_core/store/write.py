"""Core File Store write path (ACR-029 / ACI-CORE-002).

Intended for Domain callers only (organizational control; see
AH-CORE-013/017 -- no technical enforcement mechanism restricts who may
import this module). Provides exactly two public functions and no
update/delete API of any kind.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from atlas_core.correction_record import CorrectionRecord
from atlas_core.outcome import Outcome
from atlas_core.store import (
    DEFAULT_STORE_ROOT,
    RecordConflictError,
    UnsupportedStoreFilesystemError,
    WriterLockError,
    _build_envelope,
    _compute_digest_from_ordered,
    _ordered_dict_from_instance,
    _path_for,
    _read_envelope_json,
    _verify_and_get_ordered_record,
)

_LOCK_FILE_NAME = ".writer.lock"


class _WriterLock:
    """Enforces the single-process/single-checkout topology (AH-CORE-017 SS4).

    Acquisition is atomic (O_CREAT|O_EXCL). A pre-existing lock file is
    never removed unconditionally -- it is only ever replaced when a
    concrete, positive liveness check (POSIX only) proves the recorded
    PID is no longer running. Anywhere that check cannot be performed
    (non-POSIX platforms, unreadable lock content, inconclusive result),
    acquisition fails safe.
    """

    def __init__(self, store_root: Path) -> None:
        self._lock_path = Path(store_root) / _LOCK_FILE_NAME
        self._acquired = False

    def __enter__(self) -> "_WriterLock":
        self._lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._acquire()
        return self

    def __exit__(self, *exc_info: object) -> None:
        if self._acquired:
            try:
                self._lock_path.unlink(missing_ok=True)
            finally:
                self._acquired = False

    def _acquire(self) -> None:
        try:
            self._create_lock_file()
            self._acquired = True
            return
        except FileExistsError:
            pass

        if self._reclaim_if_confirmed_stale():
            try:
                self._create_lock_file()
                self._acquired = True
                return
            except FileExistsError:
                pass

        raise WriterLockError(
            f"writer lock {self._lock_path} is held (or its state could not "
            "be safely determined); refusing to register concurrently. If "
            "no other Atlas Core process is running, verify and remove the "
            "lock file manually."
        )

    def _create_lock_file(self) -> None:
        fd = os.open(
            self._lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY
        )
        try:
            os.write(fd, str(os.getpid()).encode("ascii"))
            os.fsync(fd)
        finally:
            os.close(fd)

    def _reclaim_if_confirmed_stale(self) -> bool:
        if os.name != "posix":
            return False

        try:
            existing_pid_text = self._lock_path.read_text(encoding="ascii").strip()
            existing_pid = int(existing_pid_text)
        except (OSError, ValueError):
            return False

        try:
            os.kill(existing_pid, 0)
        except ProcessLookupError:
            pass
        except OSError:
            return False
        else:
            return False

        try:
            self._lock_path.unlink()
        except OSError:
            return False
        return True


def _write_atomic(final_path: Path, payload: bytes) -> None:
    final_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = final_path.parent / f".{final_path.name}.tmp-{os.getpid()}-{uuid4().hex}"

    fd = os.open(temp_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)

    try:
        os.link(temp_path, final_path)
    except FileExistsError:
        raise
    except OSError as exc:
        raise UnsupportedStoreFilesystemError(
            f"atomic publish of {final_path} failed on this filesystem "
            f"(os.link not supported or refused): {exc}"
        ) from exc
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


def _register(
    *,
    kind: str,
    record_id: str,
    instance: object,
    store_root: Path,
) -> None:
    final_path = _path_for(kind, record_id, Path(store_root))
    ordered = _ordered_dict_from_instance(instance)
    envelope = _build_envelope(ordered, registered_at=datetime.now(timezone.utc))
    payload = json.dumps(envelope, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )

    try:
        _write_atomic(final_path, payload)
        return
    except FileExistsError:
        pass

    existing_envelope = _read_envelope_json(final_path)
    existing_ordered = _verify_and_get_ordered_record(existing_envelope, type(instance))
    existing_digest = _compute_digest_from_ordered(existing_ordered)
    new_digest = _compute_digest_from_ordered(ordered)

    if existing_digest == new_digest:
        return

    raise RecordConflictError(
        f"{kind}/{record_id} is already registered with different content "
        "(same canonical ID, different digest); registration rejected, "
        "existing record left unchanged"
    )


def register_outcome(
    outcome: Outcome, *, store_root: Path | str = DEFAULT_STORE_ROOT
) -> Outcome:
    """Register an Outcome as Core Canonical. Idempotent on identical resubmission."""
    root = Path(store_root)
    with _WriterLock(root):
        _register(
            kind="outcomes",
            record_id=outcome.outcome_id,
            instance=outcome,
            store_root=root,
        )
    return outcome


def register_correction_record(
    correction: CorrectionRecord, *, store_root: Path | str = DEFAULT_STORE_ROOT
) -> CorrectionRecord:
    """Register a CorrectionRecord as Core Canonical. Never mutates the superseded record."""
    root = Path(store_root)
    with _WriterLock(root):
        _register(
            kind="corrections",
            record_id=correction.correction_id,
            instance=correction,
            store_root=root,
        )
    return correction
