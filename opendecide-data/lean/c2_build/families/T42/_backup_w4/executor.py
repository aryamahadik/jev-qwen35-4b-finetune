"""families/T42/executor.py: hermetic execution, the gold of T42 (solver A, execution side).

Every gold answer is the result of running the generated program in the pinned venv CPython 3.12 with PYTHONHASHSEED=0,
in a fresh subprocess (python -S -s -B -P exec_child.py) with a 5 s cap, an empty temp dir as cwd, a minimal
environment, no network (audit hook + no sockets) and no file side effects (audit hook + RLIMIT_FSIZE 0).

  run_snippets(jobs, confirm=False)   [{"id", "code", "kind"}] -> {id: result}; one subprocess per call
  run_equiv(f, g, sig, seed, ...)     the equivalence harness: grids, 10K fuzz, branch coverage
  equiv_label(res)                    the label rule (G0 section 4) from the raw counts
Results are cached in memory by content. confirm=True re-runs every uncached job in a SECOND fresh subprocess and
requires an identical result ("execution must agree on 2 runs"); a disagreement raises ExecError.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHILD = HERE / "exec_child.py"
VENV_PY = Path("/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python")
TIMEOUT_S = 5
HASHSEED = "0"                   # the audit (test_build.py) re-runs under another seed
FUZZ_N = 10_000
COV_BAR = 0.95
TYP_DIFF_BAR = 0.10
LABELS = ("SAME", "DIFFERS_TYPICAL", "DIFFERS_EDGE")


class ExecError(RuntimeError):
    pass


def python_exe() -> str:
    """The venv CPython 3.12 (falls back to sys.executable when that is the same 3.12 interpreter)."""
    if VENV_PY.exists():
        return str(VENV_PY)
    if sys.version_info[:2] == (3, 12):
        return sys.executable
    raise ExecError("no CPython 3.12 interpreter (venv missing)")


def _child_env() -> dict:
    return {"PYTHONHASHSEED": HASHSEED, "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}


def _spawn(job: dict) -> dict:
    tmp = tempfile.mkdtemp(prefix="t42_exec_")
    try:
        p = subprocess.run([python_exe(), "-S", "-s", "-B", "-P", str(CHILD)], input=json.dumps(job), text=True,
                           capture_output=True, cwd=tmp, env=_child_env(), timeout=TIMEOUT_S)
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
    return out


_SNIP: dict = {}
_EQ: dict = {}
STATS = {"spawns": 0, "confirm_spawns": 0}


def _key(kind: str, code: str) -> str:
    return kind + "\x00" + hashlib.sha256(code.encode()).hexdigest()


def run_snippets(jobs: list, *, cap: int = 700, confirm: bool = False) -> dict:
    """jobs: [{"id", "code", "kind"}] -> {id: {"s", "out", "exc", "steps"}}."""
    todo = {}                      # content key -> job (one run per distinct program)
    for j in jobs:
        k = _key(j["kind"], j["code"])
        c = _SNIP.get(k)
        if c is None or (confirm and not c["confirmed"]):
            todo[k] = j
    if todo:
        ids = {k: f"j{n}" for n, k in enumerate(todo)}
        fresh = [k for k in todo if k not in _SNIP]
        first = {}
        if fresh:
            STATS["spawns"] += 1
            batch = [{"id": ids[k], "code": todo[k]["code"], "kind": todo[k]["kind"]} for k in fresh]
            got = _spawn({"mode": "snippets", "jobs": batch, "cap": cap})["results"]
            first = {k: got[ids[k]] for k in fresh}
        second = {}
        if confirm:                # the confirming run is a second, fresh subprocess
            STATS["confirm_spawns"] += 1
            batch = [{"id": ids[k], "code": todo[k]["code"], "kind": todo[k]["kind"]} for k in todo]
            second = _spawn({"mode": "snippets", "jobs": batch, "cap": cap})["results"]
        for k in todo:
            r1 = first[k] if k in first else _SNIP[k]["res"]
            if confirm and r1 != second[ids[k]]:
                raise ExecError(f"two runs disagree: {r1} vs {second[ids[k]]}")
            _SNIP[k] = {"res": r1, "confirmed": bool(confirm)}
    return {j["id"]: _SNIP[_key(j["kind"], j["code"])]["res"] for j in jobs}


def run_one(code: str, kind: str = "print", *, confirm: bool = False) -> dict:
    return run_snippets([{"id": "x", "code": code, "kind": kind}], confirm=confirm)["x"]


def answer_key(res: dict, *, max_len: int = 70):
    """The option key of one execution: "out:<text>" or "exc:<Class>"; None when it cannot be an answer (cap,
    timeout, an unlisted exception, empty / multi-line / padded / address-bearing output)."""
    if res["s"] == "exc":
        return "exc:" + res["exc"]
    if res["s"] != "ok":
        return None
    t = res["out"]
    if t.endswith("\n"):
        t = t[:-1]
    if not t or "\n" in t or t != t.strip() or len(t) > max_len or " at 0x" in t or "object at" in t:
        return None
    return "out:" + t


def run_equiv(f_src: str, g_src: str, sig: tuple, *, seed: int, fuzz: int = FUZZ_N, confirm: bool = False) -> dict:
    k = _key("equiv", json.dumps([f_src, g_src, list(sig), seed, fuzz]))
    c = _EQ.get(k)
    if c is None or (confirm and not c["confirmed"]):
        job = {"mode": "equiv", "f": f_src, "g": g_src, "sig": list(sig), "seed": seed, "fuzz": fuzz}
        if c is None:
            STATS["spawns"] += 1
            first = _spawn(job)["equiv"]
        else:
            first = c["res"]
        if confirm:
            STATS["confirm_spawns"] += 1
            if first != _spawn(job)["equiv"]:
                raise ExecError("two equivalence runs disagree")
        c = _EQ[k] = {"res": first, "confirmed": bool(confirm)}
    return c["res"]


def prefetch_equiv(items: list) -> None:
    """Run several equivalence jobs (f, g, sig, seed) in parallel threads (one subprocess each) into the cache."""
    from concurrent.futures import ThreadPoolExecutor
    todo = [it for it in items if _key("equiv", json.dumps([it[0], it[1], list(it[2]), it[3], FUZZ_N])) not in _EQ]
    if len(todo) > 1:
        with ThreadPoolExecutor(max_workers=len(todo)) as ex:
            list(ex.map(lambda it: run_equiv(it[0], it[1], it[2], seed=it[3]), todo))


def equiv_label(r: dict):
    """(label, witness) by the G0 rule, or (None, reason) for an ambiguous / unusable pair.
      DIFFERS_TYPICAL  >= 10% of the typical grid differs (witness = the first differing typical input)
      DIFFERS_EDGE     the typical grid and the typical fuzz agree, an edge / cross input differs (the witness)
      SAME             nothing differs on the full grid or in 10K fuzz and branch coverage >= 95% for both functions
    """
    if r["timeouts"]:
        return None, "timeout"
    if r["stage"] == "ambiguous_typ":
        return None, "ambiguous: a few typical inputs differ"
    if r["typ_diff"] / r["n_typ"] >= TYP_DIFF_BAR:
        return "DIFFERS_TYPICAL", r["witness_typ"]
    if r["cross_diff"]:
        if r["typ_fuzz_diff"]:
            return None, "ambiguous: typical fuzz differs, typical grid agrees"
        return "DIFFERS_EDGE", r["witness_edge"]
    if r["fuzz_diff"]:
        return None, "ambiguous: only fuzz differs"
    if r["fuzz_n"] < FUZZ_N:
        return None, "fuzz too small"
    cov = r["cov"]
    if cov is None:
        return None, "no coverage"
    lo = min(cov[x][0] / cov[x][1] if cov[x][1] else 1.0 for x in ("f", "g"))
    if lo < COV_BAR:
        return None, f"coverage {lo:.2f}"
    return "SAME", None


def coverage_of(r: dict):
    cov = r.get("cov")
    if not cov:
        return None
    return min(cov[x][0] / cov[x][1] if cov[x][1] else 1.0 for x in ("f", "g"))
