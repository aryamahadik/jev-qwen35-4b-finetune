"""families/T45/executor.py: solver A, execution side: the parent of exec_child.py.

  run_exec(kind, params)   two INDEPENDENT hermetic runs (fresh subprocesses, venv CPython 3.12, PYTHONHASHSEED=0, empty
                           temp cwd, 5 s cap, minimal environment, localhost only inside the child); the structured results
                           must be identical, else ExecError (the spec is dropped, never relabelled). Cached in memory by
                           the sha256 of (kind, params); nothing is written to disk.
  classify(res)            the label and next move from the EXECUTED states (the diff between the post-state and the
                           intended effect, computed by program) and the executed retry / repair; it raises Inconsistent
                           when the runner's tag class (the wrapper's reading of the real error text) contradicts what the
                           retry and the repair actually did.
  prefetch(jobs, workers)  run many uncached jobs in parallel threads (each job is still two fresh processes).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHILD = HERE / "exec_child.py"
VENV_PY = Path("/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python")
TIMEOUT_S = 5
HASHSEED = "0"
LABELS = ("SUCCESS", "NEUTRAL", "SILENT_PARTIAL", "SILENT_WRONG", "LOUD_RETRYABLE", "LOUD_PERMANENT")
MOVES = ("ADVANCE", "RETRY", "REPAIR_ARGS", "ESCALATE")
CLS_MOVE = {"T": "RETRY", "A": "REPAIR_ARGS", "0": "REPAIR_ARGS", "H": "ESCALATE"}
_CACHE: dict = {}
_LOCK = threading.Lock()
STATS = {"runs": 0, "hits": 0, "seconds": 0.0}


class ExecError(RuntimeError):
    pass


def load_cache(path: str) -> int:
    """Optional development cache (JSON lines of canonical execution results, kept OUTSIDE the repo by the caller).
    Not used by the gates' final runs unless the caller sets T45_EXEC_CACHE; it holds execution results, never rows."""
    n = 0
    p = Path(path)
    if p.exists():
        for ln in p.read_text().splitlines():
            try:
                k, v = json.loads(ln)
            except ValueError:
                continue
            _CACHE[k] = v
            n += 1
    return n


def _append_cache(k: str, v: dict) -> None:
    path = os.environ.get("T45_EXEC_CACHE")
    if path:
        with open(path, "a") as f:
            f.write(json.dumps([k, v]) + "\n")


class Inconsistent(ExecError):
    pass


def python_exe() -> str:
    if VENV_PY.exists():
        return str(VENV_PY)
    if sys.version_info[:2] == (3, 12):
        return sys.executable
    raise ExecError("no CPython 3.12 interpreter (venv missing)")


def _env() -> dict:
    return {"PYTHONHASHSEED": HASHSEED, "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}


TIMEOUT_RETRIES = 4          # a timeout is not a result: on a loaded machine the run is repeated (each attempt keeps the 5 s cap)


def _spawn(job: dict) -> dict:
    for attempt in range(TIMEOUT_RETRIES + 1):
        tmp = tempfile.mkdtemp(prefix="t45_cwd_")
        try:
            p = subprocess.run([python_exe(), "-S", "-s", "-B", "-P", str(CHILD)], input=json.dumps(job), text=True,
                               capture_output=True, cwd=tmp, env=_env(), timeout=TIMEOUT_S)
            break
        except subprocess.TimeoutExpired as e:
            STATS["timeouts"] = STATS.get("timeouts", 0) + 1
            if attempt == TIMEOUT_RETRIES:
                raise ExecError(f"child exceeded the {TIMEOUT_S} s cap {TIMEOUT_RETRIES + 1} times") from e
        finally:
            try:
                os.rmdir(tmp)
            except OSError:
                pass
    if p.returncode != 0:
        raise ExecError(f"child failed ({p.returncode}): {p.stderr[-400:]}")
    try:
        return json.loads(p.stdout)
    except ValueError as e:
        raise ExecError(f"child output is not JSON: {p.stdout[-200:]}") from e


def _strip(r: dict) -> dict:
    return {k: v for k, v in r.items() if k != "debug"}


def exec_key(kind: str, params: dict) -> str:
    return hashlib.sha256(json.dumps({"kind": kind, "params": params}, sort_keys=True).encode()).hexdigest()


def run_exec(kind: str, params: dict, *, confirm: bool = True) -> dict:
    k = exec_key(kind, params)
    with _LOCK:
        if k in _CACHE:
            STATS["hits"] += 1
            return _CACHE[k]
    job = {"kind": kind, "params": params}
    a = _spawn(job)
    if confirm:
        b = _spawn(job)
        if _strip(a) != _strip(b):
            raise ExecError(f"two independent runs disagree for {kind}/{params['fault']}")
    with _LOCK:
        STATS["runs"] += 2 if confirm else 1
        _CACHE[k] = _strip(a)
        _append_cache(k, _CACHE[k])
    return _CACHE[k]


def prefetch(jobs: list, workers: int = 4) -> None:
    todo = [(k, p) for k, p in jobs if exec_key(k, p) not in _CACHE]

    def one(kp):
        try:
            run_exec(*kp)
        except ExecError:
            pass
    if todo:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(one, todo))


# ------------------------------------------------------------------------------------------------ the label
def holds(item_key: str, intent: dict, state: dict) -> bool:
    return state.get(item_key) == intent[item_key]


def outcome(intent: dict, before: dict, after: dict, exit_status: int, retry_full: bool) -> str:
    """The diff between the post-state and the intended effect (G0 section 2)."""
    if exit_status != 0:
        return "LOUD_RETRYABLE" if retry_full else "LOUD_PERMANENT"
    held_b = {k for k in intent if holds(k, intent, before)}
    held_a = {k for k in intent if holds(k, intent, after)}
    wrong = {k for k in intent if k in after and after[k] != intent[k]}
    newly = held_a - held_b
    if len(held_a) == len(intent):
        return "SUCCESS" if newly else "NEUTRAL"
    if newly and not wrong:
        return "SILENT_PARTIAL"
    return "SILENT_WRONG"


def full(intent: dict, state: dict) -> bool:
    return all(holds(k, intent, state) for k in intent)


def classify(res: dict) -> dict:
    intent, before, m = res["intent"], res["before"], res["main"]
    retry_full = bool(res.get("retry")) and full(intent, res["retry"]["after"]) and res["retry"]["exit"] == 0
    repair_full = bool(res.get("repair")) and full(intent, res["repair"]["after"]) and res["repair"]["exit"] == 0
    label = outcome(intent, before, m["after"], m["exit"], retry_full)
    if label in ("SUCCESS", "NEUTRAL"):
        move = "ADVANCE"
    elif retry_full:
        move = "RETRY"
    elif repair_full:
        move = "REPAIR_ARGS"
    else:
        move = "ESCALATE"
    cls = m["cls"]
    if cls == "?":
        raise Inconsistent("the runner's reading of the error text found no class")
    if label in ("SUCCESS", "NEUTRAL"):
        if cls != "0":
            raise Inconsistent(f"{label} with remark class {cls}")
    else:
        if CLS_MOVE[cls] != move:
            raise Inconsistent(f"tag class {cls} says {CLS_MOVE[cls]} but the executed retry/repair say {move}")
        if (label == "LOUD_RETRYABLE") != (cls == "T" and m["exit"] != 0):
            raise Inconsistent(f"label {label} vs tag class {cls}")
        if m["exit"] != 0 and cls == "0":
            raise Inconsistent("a failed step with no remark class")
    return {"label": label, "move": move, "cls": cls, "retry_full": retry_full, "repair_full": repair_full}


if os.environ.get("T45_EXEC_CACHE"):
    load_cache(os.environ["T45_EXEC_CACHE"])
