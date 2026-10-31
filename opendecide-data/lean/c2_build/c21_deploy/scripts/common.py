"""c21_deploy.common: shared helpers for the L-D deployment measurement scripts (stdlib only, CPU).

Provenance rule (L-D gate): every number that leaves these scripts carries a tag.
  author-run   measured by us on our own box/client. REQUIRES n (calls, rows, boots, ...) and a source.
  modelled     computed by a script from tagged inputs (simulation or arithmetic). Carries the input tags, the seed
               and the simulated size. Never reported as a measurement.
  assumed      a scenario value chosen by the orchestrator/owner (load, user location, ...). No n.
  not-measured a placeholder for a number the plan asks for but nobody has produced yet. value is None.
  third-party  a vendor/price-page/doc figure. Never reported as author-run; carries the fetch date and url.
`tag()` raises when an author-run number has no n, so an untagged measurement cannot be written by accident.

Hard rules enforced here (the task rules):
  * never Modal: any URL/host containing "modal" is refused by `refuse_modal()`;
  * never port 30000 for anything that starts/stops/probes-with-load a server we did not start (`refuse_prod_port()`);
  * never the OHS data: `refuse_ohs()` rejects any path with "ohs" in it;
  * GPU-side scripts only run inside a window the orchestrator opened: `require_window()`.
No script here calls an LLM API or reads Jev outputs.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                    # c21_deploy/
LEAN = ROOT.parent.parent             # opendecide-data/lean
KINDS = ("author-run", "modelled", "assumed", "not-measured", "third-party")
PROD_PORT = 30000
# same pattern as speed/opt_c1_round2_20261017/vmcode/prod_stop.sh: a C2 read job is running on the VM
C2_JOB_PATTERN = r"[c]rowd_driver|[f]ast_read\.py (label|predict|parity)|[r]eplay_c2|[r]eplay"
PARITY_BAR = 0.995          # S1 rule: argmax agreement >= 99.5% (hosting/speed_bench.BARS)
ACC_DIFF_BAR_PT = 0.3       # S1 rule: |accuracy diff| <= 0.3 pt (1.0 pt only for FP8 arms, which are not in L-D)


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ------------------------------------------------------------------ tags
def tag(kind: str, n: int | None = None, source: str | None = None, **extra) -> dict:
    """Provenance stamp. author-run needs a positive integer n and a source; every kind needs a known name."""
    if kind not in KINDS:
        raise ValueError(f"unknown tag kind {kind!r}; use one of {KINDS}")
    if kind == "author-run":
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            raise ValueError("an author-run number needs n (a positive integer: calls, rows, boots, ...)")
        if not source:
            raise ValueError("an author-run number needs a source (file, session or command)")
    t = {"tag": kind}
    if n is not None:
        t["n"] = n
    if source:
        t["source"] = source
    t.update(extra)
    return t


def val(value, kind: str, n: int | None = None, source: str | None = None, unit: str | None = None, **extra) -> dict:
    """A tagged number: {"value", "unit", "tag", "n", "source", ...}. not-measured forces value None."""
    if kind == "not-measured":
        value = None
    d = {"value": value}
    if unit:
        d["unit"] = unit
    d.update(tag(kind, n, source, **extra))
    return d


def check_tagged(d, path="") -> list:
    """Walk a JSON structure; every dict that has a "value" key must carry a valid tag (author-run needs n). Returns the
    list of problems (empty = ok). Used by the tests and by `cost_calc.py --check`."""
    bad = []
    if isinstance(d, dict):
        if "value" in d and ("tag" in d or "unit" in d):
            t = d.get("tag")
            if t not in KINDS:
                bad.append(f"{path}: missing/unknown tag {t!r}")
            elif t == "author-run" and not (isinstance(d.get("n"), int) and d["n"] >= 1 and d.get("source")):
                bad.append(f"{path}: author-run without n/source")
            elif t == "not-measured" and d.get("value") is not None:
                bad.append(f"{path}: not-measured with a value")
        for k, v in d.items():
            bad += check_tagged(v, f"{path}/{k}")
    elif isinstance(d, list):
        for i, v in enumerate(d):
            bad += check_tagged(v, f"{path}[{i}]")
    return bad


# ------------------------------------------------------------------ statistics (same conventions as the repo)
def pct(xs, q: float):
    """Nearest rank: s[min(n-1, int(q*n))] (client_bench.pct, oc1.common.pct)."""
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))] if s else None


def summarize(xs, nd: int = 2) -> dict:
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    if not xs:
        return {"n": 0}
    r = lambda v: round(v, nd)  # noqa: E731
    return {"n": len(xs), "p50": r(pct(xs, 0.5)), "p90": r(pct(xs, 0.9)), "p95": r(pct(xs, 0.95)),
            "p99": r(pct(xs, 0.99)), "mean": r(sum(xs) / len(xs)), "min": r(min(xs)), "max": r(max(xs))}


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


# ------------------------------------------------------------------ io
def sha256_file(p, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def read_jsonl(p) -> list:
    refuse_ohs(p)
    out = []
    with open(p) as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def write_json(p, obj) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, default=str))
    os.replace(tmp, p)


def md_table(header: list, rows: list) -> str:
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join("" if c is None else str(c) for c in r) + " |")
    return "\n".join(out)


# ------------------------------------------------------------------ refusals
def refuse_ohs(p) -> None:
    if "ohs" in str(p).lower():
        raise SystemExit(f"refusing path with 'ohs' in it: {p}")


def refuse_modal(url_or_host: str) -> None:
    if re.search(r"modal", str(url_or_host), re.I):
        raise SystemExit(f"refusing a Modal endpoint (never Modal): {url_or_host}")


def refuse_prod_port(port: int, what: str = "this action") -> None:
    if int(port) == PROD_PORT:
        raise SystemExit(f"refusing port {PROD_PORT} for {what}: it is the production server (not started by this task)")


def c2_busy() -> list:
    """Lines of C2 read jobs that are running on THIS host (empty = none). Same pattern as prod_stop.sh."""
    try:
        out = subprocess.run(["pgrep", "-af", C2_JOB_PATTERN], capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [ln[:160] for ln in out.splitlines() if ln.strip()]


def require_window(label_env: str = "LD_WINDOW") -> str:
    """GPU-side scripts run only inside a window an authorised caller opened: env LD_WINDOW=<label> and no C2 read job.
    The label ends up in every output so a result can be traced to its window. Exit 9 mirrors prod_stop.sh."""
    lab = os.environ.get(label_env, "").strip()
    if not lab:
        raise SystemExit(f"{label_env} is not set: this script only runs inside an authorised L-D window (queue priority 5, "
                         f"after C2's grid reads). Use --dry-run to see the plan.")
    busy = c2_busy()
    if busy:
        print("C2_JOB_RUNNING:\n  " + "\n  ".join(busy), file=sys.stderr)
        raise SystemExit(9)
    return lab


def gpu_mem_used_mib() -> int | None:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=10).stdout.strip().splitlines()
        return int(float(out[0]))
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return None
