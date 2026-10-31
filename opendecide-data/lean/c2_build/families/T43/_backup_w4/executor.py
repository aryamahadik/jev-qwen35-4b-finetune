"""families/T43/executor.py: hermetic execution, the gold of T43 (solver A, execution side).

Every gold is the result of running the generated programs in the pinned venv CPython 3.12 with PYTHONHASHSEED=0, in a
fresh subprocess (python -S -s -B -P exec_child.py) with a 5 s cap, an empty temp dir as cwd, a minimal environment, no
network and no file writes (exec_child.py). Jobs are cached by content; confirm=True re-runs every job that is not yet
confirmed in a SECOND fresh subprocess and requires an identical result ("execution must agree on 2 runs").

  run(jobs, confirm=False)            -> list of results (one subprocess for all uncached jobs)
  pair(a, b, calls) / judge(...)       job builders
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHILD = HERE / "exec_child.py"
VENV_PY = Path("/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python")
TIMEOUT_S = 5
HASHSEED = "0"
NSEED = 240                          # seeded property-generated cases per function and patch (G0: >= 200)


class ExecError(RuntimeError):
    pass


def python_exe() -> str:
    if VENV_PY.exists():
        return str(VENV_PY)
    if sys.version_info[:2] == (3, 12):
        return sys.executable
    raise ExecError("no CPython 3.12 interpreter (venv missing)")


def _env() -> dict:
    return {"PYTHONHASHSEED": HASHSEED, "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}


def _spawn(jobs: list) -> list:
    tmp = tempfile.mkdtemp(prefix="t43_exec_")
    try:
        p = subprocess.run([python_exe(), "-S", "-s", "-B", "-P", str(CHILD)], input=json.dumps({"jobs": jobs}), text=True,
                           capture_output=True, cwd=tmp, env=_env(), timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired as e:
        raise ExecError(f"child exceeded the {TIMEOUT_S} s cap") from e
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if p.returncode != 0:
        raise ExecError(f"child exit {p.returncode}: {p.stderr[-300:]}")
    out = json.loads(p.stdout)
    m = out["meta"]
    if m["py"][:2] != [3, 12] or m["hashseed"] != HASHSEED:
        raise ExecError(f"child is not CPython 3.12 with PYTHONHASHSEED={HASHSEED}: {m}")
    for r in out["results"]:
        if isinstance(r, dict) and "error" in r:
            raise ExecError(r["error"])
    return out["results"]


_CACHE: dict = {}
STATS = {"spawns": 0, "confirm_spawns": 0}


def _key(job: dict) -> str:
    return hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()


def run(jobs: list, *, confirm: bool = False) -> list:
    keys = [_key(j) for j in jobs]
    todo = {}
    for k, j in zip(keys, jobs):
        c = _CACHE.get(k)
        if c is None or (confirm and not c["confirmed"]):
            todo[k] = j
    if todo:
        ks = list(todo)
        fresh = [k for k in ks if k not in _CACHE]
        first = {}
        if fresh:
            STATS["spawns"] += 1
            got = _spawn([todo[k] for k in fresh])
            first = dict(zip(fresh, got))
        second = {}
        if confirm:
            STATS["confirm_spawns"] += 1
            second = dict(zip(ks, _spawn([todo[k] for k in ks])))
        for k in ks:
            r1 = first[k] if k in first else _CACHE[k]["res"]
            if confirm and r1 != second[k]:
                raise ExecError("two runs disagree")
            _CACHE[k] = {"res": r1, "confirmed": bool(confirm)}
    return [_CACHE[k]["res"] for k in keys]


def pair_job(a: str, b: str, calls: list) -> dict:
    return {"op": "pair", "a": a, "b": b, "calls": list(calls)}


def judge_job(orig: str, fns: list, cands: list, tests: list, seed: int, nseed: int = NSEED) -> dict:
    return {"op": "judge", "orig": orig, "fns": [{"name": f["name"], "types": f["types"], "entry": bool(f.get("entry"))} for f in fns],
            "cands": [{"id": i, "src": s} for i, s in cands], "tests": [list(t) for t in tests], "seed": seed, "nseed": nseed}


def label_of(r: dict) -> str | None:
    """The patch class of one judged candidate (A fixes / B does not fix / C passes the tests but is wrong), None when
    it cannot be used (load error, timeout, ambiguous: the seeded cases find a difference the grid does not)."""
    if r["load"] != "ok" or r["slow"]:
        return None
    if any(t != "p" for t in r["tests"]):
        return "B"
    if r["grid_diff"]:
        return "C"
    if r["seeded_diff"]:
        return None
    return "A"
