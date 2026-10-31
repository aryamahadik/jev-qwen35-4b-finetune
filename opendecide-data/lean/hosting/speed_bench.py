"""speed_bench: the SPEED-2 dev-only A/B benchmark client for C1 serving arms (hosting/SPEED1_DESIGN.md, API v1).
NEW file; plain Python (httpx), no Modal, no GPU. It never starts or deploys a server: it talks to an endpoint that is
already up (any engine speaking API v1), stops it only with `ab --shutdown-after` (POST /shutdown), and talks to
OpenRouter only in `jev ... --go`.

Commands, run from lean/ with ../.venv/bin/python:
  hosting/speed_bench.py workloads [--no-tokens] [--check]
      P (all 8,143 gate dev rows once), S (387 choice rows with >= 10 options + 273 yes/no, seed 0), N (660 rows,
      seed 1), R (repeated schema, seed 2) -> speed/workloads/{P,S,N,R}.jsonl + manifest.json (row ids, counts,
      sha256) + token_profile.json; prints the token-length profile (C1 tokenizer + decoder_io prompt, counts only).
      --check rebuilds in memory and compares with the manifest's sha256 (writes nothing).
  hosting/speed_bench.py ab --url URL --token-file F --session NAME [--arms A0,A2,A1] [--shutdown-after] [--go]
      per arm (hosting/speed_arms.json), in the given order (default A0, A2, A1: the main arm before A1, so a short
      serving window cuts the least important arm): /health snapshot + boot check + fit check, POST /admin/config,
      flags read back, then P at c=16 (every row once, answers saved), S at c=1,2,4,8,16, N at c=1, R at c=1 and 8,
      POST /admin/flush before every level, /health + flags re-checked between workloads -> speed/<session>/<arm>/.
      Fit check: an arm whose plan at --fit-gpu-ms (default 40 ms/call, conservative) + 60 s does not fit the
      endpoint's /health serve_remaining_s is refused before any timing (not checked when the endpoint reports no
      window; --fit-gpu-ms 0 turns it off). Abort: a level stops at 20 failed calls in a row, or at >= 20 failed calls
      that are > 5% of its calls (a dead GPU, a closed window); the arm is then summarised as aborted, and the session
      stops (later arms skipped) when /health is then not ok or unreachable (a healthy endpoint goes on with the next
      arm: the failures were the arm's own). --shutdown-after: POST /shutdown when the command ends (all arms run, an
      abort, or Ctrl-C), so the GPU stops billing at once instead of after the host's idle timer; not when every arm
      was refused before timing (that boot may still serve the right arms). Without --go (or with --dry-run) it prints
      the plan and the estimated wall time per arm and sends nothing.
  hosting/speed_bench.py jev --session NAME [--go] [--max-calls 660]
      S at c=1 through OpenRouter (client_bench's Jev route), dev only, report-only -> speed/<session>/JEV/.
      Without --go it prints the plan only. Jev outputs are never used for training (Jev ToS).
  hosting/speed_bench.py report --session NAME [--baseline A0]
      speed/<session>/REPORT.md + report.json: latency, throughput, $/1K, parity PASS/FAIL per arm vs the baseline
      arm (gated) and vs the stored L4 reads (context), the reversed-view check, Jev if present.
  hosting/speed_bench.py cost --dph N    $/1K at 100% and 40% utilisation for a sustained decisions/hour figure.

Workloads as built (speed/workloads/manifest.json; a rebuild gives the same sha256):
  P 8,143 calls (order shuffled, seed 0); S 660 = 387 choice (153 with 10-25 options, 234 with 26+) + 273 yes/no;
  N 660; R = 68 tasks (50 yes/no, 18 choice) of >= 20 rows sharing type + instructions + option set + the definitions
  the prompt shows, 3,305 rows, 1,158 of them put in their task's canonical option order (its most frequent order).
  Token profile (identity view, C1 tokenizer): S choice rows > 1024 tokens 36.7%, > 2048 29.5% (= the design's).

Method:
  One dev row = one API v1 call with one question "q0" (type, instructions, options, card exactly as in the dev row).
  Closed loop (copied from prep89/load_test_c1.run_level, never imported: that file imports ohs3_lib): c threads, one
  keep-alive connection each (client_bench.Ours: TCP_NODELAY, no retries), calls back to back in workload order;
  warm-up (5 s or the first 10% of the level's calls, whichever ends first), then a measurement window (60 s); a call
  counts when it completes inside the window. No call repeats inside a level (a prefix cache must not see the same row
  twice), so a level's window ends early when its workload runs out.
  Sustained decisions/hour = the best S level with 0 failed calls (load_test_c1's rule). Percentiles: nearest rank
  s[int(q*n)] (client_bench.pct). $/1K = rate_usd_h x region_mult / sustained decisions per hour x 1000, at 100% and
  at 0.4 utilisation; the region multipliers are CLI arguments, to be confirmed against Modal's billing page.
  Parity: gate_dev's load/score/argmax_label/half (imported read-only; nothing here writes gate logs). Bars
  (SPEED1_DESIGN.md): argmax agreement >= 99.5% and |accuracy diff| <= 0.3 pt (1.0 pt for FP8 arms), gated against
  the baseline arm of the SAME session; the stored L4 reads (preds_<split>/q35_4b_main500k_pre_served.jsonl, 2view,
  and _pre.jsonl, identity view) are reported as context. The gate = P vs baseline (every row; a missing answer counts
  as a disagreement and as wrong) and R vs baseline on the rows both arms answered (R levels are time windows). When
  either arm lacks an answer for some P row (an aborted arm, failed calls, a cut window) the gate reads INCOMPLETE
  (never PASS), or FAIL if the rows both arms answered already fail a bar.
  Reversed-view check: the L4 reversed view is 2 x served - identity; an arm's is read from per-view answers
  ("view_probabilities") or from an identity pass (speed_arms.json identity_flags), else reported as not available.

Cost guards: this client starts nothing billable. ab/jev send traffic only with --go; ab refuses an arm whose boot,
adapter sha256 or flags do not match (no timing on the wrong model); the OHS splits are refused before any file is
opened; the OpenRouter key is read from the environment or opendecide-data/.env and never printed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import statistics
import sys
import threading
import time
from collections import Counter, defaultdict
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
for _p in (str(LEAN), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import client_bench as cb  # noqa: E402  (read-only: Ours, Jev, load_env, pct, OPENROUTER_BASE)
import gate_dev  # noqa: E402  (read-only: SPLITS, ROOT, load, score, argmax_label, half; never its log writers)

SPEED = LEAN / "speed"
WORKLOADS = SPEED / "workloads"
ARMS_FILE = HERE / "speed_arms.json"
ADAPTER_DIR = LEAN.parent.parent / "backups" / "modal_models" / "q35_4b_main500k"  # tokenizer + train_meta only
BASE, REVISION = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
C1_MODEL = "q35_4b_main500k"
C1_ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
STORED = {"served": "q35_4b_main500k_pre_served", "identity": "q35_4b_main500k_pre"}  # L4 od_gcp predict reads
ROW_KEYS = ("id", "state", "instructions", "qtype", "options", "card", "gold", "group_id")
WORKLOAD_NAMES = ("P", "S", "N", "R")
SEEDS = {"P": 0, "S": 0, "N": 1, "R": 2}
PARAMS = {"S_min_options": 10, "S_noul": 273, "N_calls": 660, "R_min_rows": 20}
EXPECT = {"P": 8143, "S_ge10": 387, "S": 660, "N": 660}  # SPEED1_DESIGN.md numbers (checked, printed if different)
BUCKETS = (("2-4", 2, 4), ("5-9", 5, 9), ("10-25", 10, 25), ("26+", 26, 10 ** 9))
GROUPS = ("noul",) + tuple(b[0] for b in BUCKETS)
BARS = {"argmax_agree_min": 0.995, "acc_diff_max_pt": 0.3, "acc_diff_max_pt_fp8": 1.0}
RATE_USD_H = 3.95  # Modal H100 base rate, `modal billing rates` 12 Oct (SPEED1_DESIGN.md)
REGION_MULT = {"any": 1.0, "us-east": 1.75}  # TO BE CONFIRMED: modal_direct_host.REGION_MULT "narrow" (us-east) = 1.75
UTILS = (1.0, 0.4)
PLAN = (("P", (16,)), ("S", (1, 2, 4, 8, 16)), ("N", (1,)), ("R", (1, 8)))
DEFAULT_ARMS = "A0,A2,A1"  # one BF16 boot: baseline first, then the main arm, A1 last (a cut window costs the least)
ABORT = {"consecutive": 20, "failed_min": 20, "failed_frac": 0.05}  # a level stops early (dead or closed endpoint)
SETTINGS = {"warmup_s": 5.0, "window_s": 60.0, "timeout_s": 120.0, "warmup_max_frac": 0.1, "abort": ABORT}
EST = {"net_ms": 75.0, "gpu_ms": 20.0, "admin_s": 3.0}  # dry-run wall estimate only (tunnel ~72 ms; B1a 14-19 ms/call)
# Fit check: the GPU time per call assumed when checking that an arm fits the endpoint's remaining window. Conservative:
# A0 reads 2view as one batch of 2 (56.5 ms eager at ~818 tokens/view, extra/SPEED_RESULT_30sep.md); P's choice rows
# average ~565 tokens/view and its 4,329 yes/no rows need one read, so A0's P pass should average below 40 ms/call
# (an estimate, not a measurement; windowed levels are capped at warm-up + window whatever the GPU time).
FIT_GPU_MS = 40.0
FIT_MARGIN_S = 60.0
JEV_DIR = "JEV"


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(p):
    with open(p) as f:
        return [json.loads(x) for x in f if x.strip()]


def write_jsonl(p, recs):
    Path(p).write_text("".join(json.dumps(r, ensure_ascii=False, default=str) + "\n" for r in recs))


def write_json(p, obj):
    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=str) + "\n")


def _dio():
    import decoder_io  # lazy: imports torch
    return decoder_io


# ------------------------------------------------------------------ workloads

def check_split(sp):
    if "ohs" in sp.lower() or "jev" in sp.lower():
        raise SystemExit(f"refusing split {sp!r}: gate dev splits only (OHS is never opened)")


def dev_rows(root=None, splits=None) -> list:
    """The gate dev rows, in gate_dev.SPLITS order then file order (ROW_KEYS + split)."""
    root = Path(root or gate_dev.ROOT)
    splits = list(splits or gate_dev.SPLITS.split(","))
    for sp in splits:
        check_split(sp)
    out = []
    for sp in splits:
        for r in read_jsonl(root / "data" / f"{sp}.jsonl"):
            out.append({**{k: r.get(k) for k in ROW_KEYS}, "split": sp})
    ids = [r["id"] for r in out]
    if len(set(ids)) != len(ids):
        raise SystemExit("dev row ids are not unique across the splits")
    return out


def bucket(qtype, n) -> str:
    if qtype == "noul":
        return "noul"
    return next(name for name, lo, hi in BUCKETS if lo <= n <= hi) if n >= 2 else "1"


def api_request(row, options=None) -> dict:
    """API v1 body for one dev row: one question "q0"; the card only when the row has one (as the prompt reads it)."""
    q = {"type": row["qtype"], "instructions": row["instructions"]}
    if row["qtype"] == "choice":
        q["options"] = list(options if options is not None else row["options"])
    if row.get("card"):
        q["card"] = row["card"]
    return {"id": row["id"], "state": row["state"], "questions": {"q0": q}}


def make_item(row, options=None, **extra) -> dict:
    opts = list(options if options is not None else (row["options"] or []))
    return {"id": row["id"], "split": row["split"], "qtype": row["qtype"], "n_options": len(opts),
            "bucket": bucket(row["qtype"], len(opts)), **extra, "request": api_request(row, options)}


def request_row(req, name="q0") -> dict:
    """The decoder_io row the host builds from a request (state, instructions, qtype, options, card)."""
    q = req["questions"][name]
    return {"state": req["state"], "instructions": q["instructions"], "qtype": q["type"], "options": q.get("options"),
            "card": q.get("card")}


def schema_key(row):
    """What the prompt's schema part depends on: type, instructions, option set and the definitions the prompt shows
    (choice: card_defs of the options, order-free; yes/no: the card text verbatim)."""
    if row["qtype"] == "choice":
        defs = _dio().card_defs(row.get("card"))
        return ("choice", row["instructions"], tuple(sorted(row["options"])),
                tuple(sorted((o, defs[o]) for o in row["options"] if o in defs)))
    return ("noul", row["instructions"], (), row.get("card") or "")


def build_P(rows, seed=SEEDS["P"]):
    items = [make_item(r) for r in rows]
    random.Random(seed).shuffle(items)  # long-row splits do not cluster in time
    return items


def build_S(rows, seed=SEEDS["S"], min_options=PARAMS["S_min_options"], n_noul=PARAMS["S_noul"]):
    rng = random.Random(seed)
    ge = [r for r in rows if r["qtype"] == "choice" and len(r["options"]) >= min_options]
    noul = rng.sample([r for r in rows if r["qtype"] == "noul"], n_noul)
    items = [make_item(r) for r in ge + noul]
    rng.shuffle(items)
    return items


def build_N(rows, seed=SEEDS["N"], n=PARAMS["N_calls"]):
    return [make_item(r) for r in random.Random(seed).sample(rows, n)]


def build_R(rows, seed=SEEDS["R"], min_rows=PARAMS["R_min_rows"]):
    """Tasks = rows sharing schema_key, kept when >= min_rows; a choice task's options are put in its canonical order
    (its most frequent order; ties -> the smallest tuple). Rows of all tasks are then shuffled (seed): tasks interleave
    as several tenants' traffic would. Returns (items, task info)."""
    groups = {}
    for r in rows:
        groups.setdefault(schema_key(r), []).append(r)
    items, tasks = [], []
    for t, v in enumerate([v for v in groups.values() if len(v) >= min_rows]):  # first-appearance order
        canon = None
        if v[0]["qtype"] == "choice":
            cnt = Counter(tuple(r["options"]) for r in v)
            canon = min(cnt, key=lambda o: (-cnt[o], o))
        re_n = 0
        for r in v:
            moved = canon is not None and tuple(r["options"]) != canon
            re_n += moved
            items.append(make_item(r, list(canon) if canon else None, task=t, reordered=moved))
        tasks.append({"task": t, "qtype": v[0]["qtype"], "n_options": len(canon or ()), "rows": len(v),
                      "reordered_rows": re_n, "distinct_orders": len({tuple(r["options"] or ()) for r in v}),
                      "splits": dict(Counter(r["split"] for r in v)), "card_chars": len(v[0].get("card") or ""),
                      "instructions": v[0]["instructions"][:90]})
    random.Random(seed).shuffle(items)
    return items, tasks


def build_all(rows) -> tuple:
    w = {"P": build_P(rows), "S": build_S(rows), "N": build_N(rows)}
    w["R"], tasks = build_R(rows)
    for name, items in w.items():
        for i, it in enumerate(items):
            it["i"] = i
    return w, tasks


def workload_bytes(items) -> bytes:
    return "".join(json.dumps(it, ensure_ascii=False, sort_keys=True) + "\n" for it in items).encode("utf-8")


def manifest_for(w, tasks, root, splits) -> dict:
    root = Path(root)
    man = {"version": 1, "design": "hosting/SPEED1_DESIGN.md, Workloads", "built_by": "hosting/speed_bench.py",
           "splits": splits, "data_sha256": {sp: sha256_file(root / "data" / f"{sp}.jsonl") for sp in splits},
           "seeds": SEEDS, "params": PARAMS, "workloads": {},
           "notes": {"P": "every gate dev row once, order shuffled (seed 0)",
                     "S": "all choice rows with >= 10 options + 273 yes/no rows drawn without replacement "
                          "(random.Random(0).sample, then the same RNG shuffles the 660 calls)",
                     "N": "660 rows uniform without replacement, random.Random(1).sample",
                     "R": "tasks = rows sharing (type, instructions, option set, definitions shown in the prompt) "
                          "with >= 20 rows; options in the task's canonical order (most frequent order); rows "
                          "shuffled with random.Random(2); no stored reference: compared live with the baseline arm"}}
    for name, items in w.items():
        man["workloads"][name] = {
            "file": f"{name}.jsonl", "sha256": sha256_bytes(workload_bytes(items)), "calls": len(items),
            "unique_rows": len({it["id"] for it in items}), "groups": dict(Counter(it["bucket"] for it in items)),
            "qtypes": dict(Counter(it["qtype"] for it in items)),
            "by_split": dict(Counter(it["split"] for it in items)),
            "with_card": sum(1 for it in items if it["request"]["questions"]["q0"].get("card")),
            "row_ids_sha256": sha256_bytes("\n".join(it["id"] for it in items).encode()),
            "row_ids": [it["id"] for it in items]}
    man["workloads"]["R"].update(tasks=len(tasks), reordered_rows=sum(t["reordered_rows"] for t in tasks),
                                 task_types=dict(Counter(t["qtype"] for t in tasks)))
    man["R_tasks"] = tasks
    man["expected_vs_design"] = {"P": [len(w["P"]), EXPECT["P"]], "S": [len(w["S"]), EXPECT["S"]],
                                 "S_ge10": [sum(it["qtype"] == "choice" for it in w["S"]), EXPECT["S_ge10"]],
                                 "N": [len(w["N"]), EXPECT["N"]]}
    return man


def write_workloads(out_dir=WORKLOADS, root=None, splits=None, log=print) -> dict:
    root = Path(root or gate_dev.ROOT)
    splits = list(splits or gate_dev.SPLITS.split(","))
    rows = dev_rows(root, splits)
    w, tasks = build_all(rows)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, items in w.items():
        (out_dir / f"{name}.jsonl").write_bytes(workload_bytes(items))
    man = manifest_for(w, tasks, root, splits)
    write_json(out_dir / "manifest.json", man)
    for k, (got, want) in man["expected_vs_design"].items():
        if got != want:
            log(f"NOTE {k}: {got} calls, the design says {want}")
    return {"workloads": w, "manifest": man, "rows": rows}


def check_workloads(wl_dir=WORKLOADS, root=None) -> dict:
    """Rebuild in memory and compare every workload's sha256 with the manifest (nothing written)."""
    man = json.loads((Path(wl_dir) / "manifest.json").read_text())
    rows = dev_rows(root, man["splits"])
    w, _ = build_all(rows)
    return {n: {"manifest": man["workloads"][n]["sha256"], "rebuilt": sha256_bytes(workload_bytes(w[n])),
                "on_disk": sha256_file(Path(wl_dir) / f"{n}.jsonl")} for n in w}


def load_workload(wl_dir, name, man=None) -> list:
    wl_dir = Path(wl_dir)
    man = man or json.loads((wl_dir / "manifest.json").read_text())
    p = wl_dir / man["workloads"][name]["file"]
    if sha256_file(p) != man["workloads"][name]["sha256"]:
        raise SystemExit(f"{p}: sha256 differs from manifest.json (rebuild with `workloads`)")
    return read_jsonl(p)


# ------------------------------------------------------------------ token-length profile (counts only)

def c1_counter(adapter_dir=ADAPTER_DIR):
    """-> (count(texts) -> token counts, prompt(row, perm) -> text, info). The C1 tokenizer from the adapter folder and
    decoder_io's prompt in C1's layout/style (from its train_meta), as the server renders it. The full Readout is built:
    its vocabulary scan sets the two-letter labels used after Z. Sets decoder_io.LAYOUT/STYLE in THIS client process."""
    dio = _dio()
    path = dio.adapter_prompt_path(BASE, str(adapter_dir), revision=REVISION)
    dio.LAYOUT, dio.STYLE = path["layout"], path["style"]
    tok = path["tok"]
    ro = dio.Readout(tok)

    def count(texts):
        return [len(x) for x in tok(list(texts), add_special_tokens=False)["input_ids"]]

    return count, ro.prompt, {"layout": path["layout"], "style": path["style"], "tokenizer": path["src"],
                              "max_len": dio.MAX_LEN}


def dist(xs) -> dict:
    if not xs:
        return {"n": 0}
    s = sorted(xs)
    n = len(s)
    return {"n": n, "mean": round(sum(s) / n, 1), "p10": cb.pct(s, 0.1), "p50": cb.pct(s, 0.5), "p90": cb.pct(s, 0.9),
            "p99": cb.pct(s, 0.99), "max": s[-1], "gt1024": round(sum(x > 1024 for x in s) / n, 4),
            "gt2048": round(sum(x > 2048 for x in s) / n, 4), "gt4096": round(sum(x > 4096 for x in s) / n, 4)}


def token_profile(workloads, count, prompt) -> dict:
    """Per workload: identity-view tokens per row (what the server's input_tokens_first_view must equal) and the
    tokens of all reads (choice = given + reversed order, the 2view readout; yes/no = one read)."""
    cache, out = {}, {}
    todo = []
    for items in workloads.values():
        for it in items:
            row = request_row(it["request"])
            key = json.dumps(it["request"], sort_keys=True)
            if key in cache:
                continue
            cache[key] = None
            todo.append((key, prompt(row)))
            if row["qtype"] == "choice":
                todo.append((key + "#rev", prompt(row, list(range(len(row["options"])))[::-1])))
    counts = count([t for _, t in todo])
    tok = dict(zip([k for k, _ in todo], counts))
    for name, items in workloads.items():
        ident, reads, per = [], [], {}
        by_group = defaultdict(list)
        for it in items:
            key = json.dumps(it["request"], sort_keys=True)
            n1 = tok[key]
            n2 = tok.get(key + "#rev", 0)
            per[it["id"]] = n1
            ident.append(n1)
            reads.append(n1 + n2)
            by_group[it["bucket"]].append(n1)
        out[name] = {"calls": len(items), "identity_tokens": dist(ident), "all_reads_tokens_total": sum(reads),
                     "identity_tokens_total": sum(ident),
                     "by_group": {g: dist(by_group[g]) for g in GROUPS if by_group.get(g)}, "per_row": per}
    return out


def print_profile(prof, info, log=print):
    log(f"token-length profile (C1 tokenizer {info.get('tokenizer')}, layout {info.get('layout')}, style "
        f"{info.get('style')}; identity-view prompt tokens; counts only)")
    log(f"{'set':4s} {'group':6s} {'n':>5s} " + " ".join(f"{h:>6s}" for h in ("p50", "p90", "p99", "max", ">1024",
                                                                         ">2048", ">4096")))
    for name, p in prof.items():
        for g, d in [("all", p["identity_tokens"])] + list(p["by_group"].items()):
            log(f"{name:4s} {g:6s} {d['n']:5d} {d['p50']:6d} {d['p90']:6d} {d['p99']:6d} {d['max']:6d} "
                f"{d['gt1024']:6.1%} {d['gt2048']:6.1%} {d['gt4096']:6.1%}")
        log(f"{name:4s} total identity tokens {p['identity_tokens_total']:,}; all reads (2view on choice) "
            f"{p['all_reads_tokens_total']:,}")


# ------------------------------------------------------------------ HTTP client (API v1)

class V1(cb.Ours):
    """client_bench.Ours (one keep-alive connection, TCP_NODELAY, no retries, Bearer token) + the API v1 routes."""

    def call(self, req):
        t = time.perf_counter()
        try:
            r = self.c.post("/decide", json=req)
            st = r.status_code
            d = r.json() if st == 200 else None
            err = None if st == 200 else f"HTTP {st}: {r.text[:300]}"
        except Exception as e:  # noqa: BLE001 - counted as a failed call
            return None, (time.perf_counter() - t) * 1000, None, f"{type(e).__name__}: {e}"[:300]
        return d, (time.perf_counter() - t) * 1000, st, err

    def _ok(self, r, what):
        if r.status_code != 200:
            raise ArmRefused(f"{what}: HTTP {r.status_code} {r.text[:300]}")
        return r.json() if r.content else {}

    def health(self):
        return self._ok(self.c.get("/health"), "GET /health")

    def config(self, flags):
        return self._ok(self.c.post("/admin/config", json={"flags": flags}), "POST /admin/config")

    def flush(self):
        return self._ok(self.c.post("/admin/flush"), "POST /admin/flush")


class ArmRefused(Exception):
    """The endpoint does not serve this arm (boot, adapter or flags): nothing is timed."""


def find_cached(usage):
    """Any cached-token count the engine reports (e.g. usage.cached_tokens): (key, value) or (None, None)."""
    for k, v in (usage or {}).items():
        if "cache" in k.lower() and isinstance(v, (int, float)) and not isinstance(v, bool):
            return k, v
    return None, None


def answer_probs(ans, qtype, options):
    """API v1 answer -> gate-format probabilities (yes/no: {"yes", "no" = 1 - yes}; choice: {option: p})."""
    if not isinstance(ans, dict):
        return None
    if qtype == "noul":
        p = ans.get("noul", (ans.get("probabilities") or {}).get("yes"))
        return None if p is None else {"yes": float(p), "no": 1.0 - float(p)}
    pr = ans.get("probabilities")
    if not isinstance(pr, dict):
        return None
    return {o: float(pr.get(o, 0.0)) for o in options}


def answer_views(ans, qtype, options):
    """Per-view probabilities when the engine returns them ("view_probabilities": {"identity", "reversed"} or a
    [identity, reversed] list, keyed by option): -> {"identity", "reversed"} or None."""
    if qtype != "choice" or not isinstance(ans, dict):
        return None
    v = ans.get("view_probabilities", ans.get("views_probabilities"))
    if isinstance(v, list) and len(v) == 2:
        v = {"identity": v[0], "reversed": v[1]}
    if not isinstance(v, dict) or not all(isinstance(v.get(k), dict) for k in ("identity", "reversed")):
        return None
    return {k: {o: float(v[k].get(o, 0.0)) for o in options} for k in ("identity", "reversed")}


def make_record(item, i, w, t0, t1, d, ms, st, err, t_base) -> dict:
    rec = {"i": i, "id": item["id"], "w": w, "t0": round(t0 - t_base, 6), "t1": round(t1 - t_base, 6),
           "ok": err is None and d is not None, "status": st, "client_ms": round(ms, 3), "error": err}
    if d:
        q = (d.get("answers") or {}).get("q0")
        usage = d.get("usage") or {}
        qu = (q or {}).get("usage") if isinstance(q, dict) else None
        ck, cv = find_cached(usage)
        qk, qv = find_cached(qu)
        rec.update(server_ms=d.get("server_ms"), timing=d.get("timing"), usage=usage, q_usage=qu,
                   batch_rows=d.get("batch_rows"), path=d.get("path"), engine=d.get("engine"),
                   cached_tokens=cv if cv is not None else qv, cached_key=ck or qk)
        opts = item["request"]["questions"]["q0"].get("options")
        rec["probs"] = answer_probs(q, item["qtype"], opts)
        if rec["probs"] is None:
            rec["ok"], rec["error"] = False, "no usable answer for q0"
        views = answer_views(q, item["qtype"], opts)
        if views:
            rec["views"] = views
    return rec


def pcts(xs, nd=2) -> dict:
    xs = [x for x in xs if isinstance(x, (int, float)) and not isinstance(x, bool)]
    if not xs:
        return {"n": 0}
    s = sorted(xs)
    return {"n": len(s), "p50": round(cb.pct(s, 0.5), nd), "p95": round(cb.pct(s, 0.95), nd),
            "p99": round(cb.pct(s, 0.99), nd), "mean": round(statistics.fmean(s), nd), "max": round(s[-1], nd)}


def summarize_level(recs, win, conc, lo, hi, mode, tok_counts=None, flags=None) -> dict:
    ok = [r for r in win if r["ok"]]
    span = max(hi - lo, 1e-9)
    timing_keys = sorted({k for r in ok for k in (r.get("timing") or {})})
    nets = [r["client_ms"] - r["server_ms"] for r in ok if isinstance(r.get("server_ms"), (int, float))]
    inp = [(r.get("usage") or {}).get("input_tokens") for r in ok]
    cached = [(r["cached_tokens"], (r.get("usage") or {}).get("input_tokens")) for r in ok
              if r.get("cached_tokens") is not None and (r.get("usage") or {}).get("input_tokens")]
    out = {"concurrency": conc, "mode": mode, "window_s": round(span, 3), "window": [round(lo, 3), round(hi, 3)],
           "calls_sent": len(recs), "calls_ok_in_window": len(ok), "failed_calls": sum(not r["ok"] for r in recs),
           "decisions_in_window": len(ok), "decisions_per_hour": round(len(ok) / span * 3600, 1),
           "client_ms": pcts([r["client_ms"] for r in ok]), "server_ms": pcts([r.get("server_ms") for r in ok]),
           "network_ms": pcts(nets),
           "timing_ms": {k: pcts([(r.get("timing") or {}).get(k) for r in ok]) for k in timing_keys},
           "input_tokens": {"mean": round(statistics.fmean([x for x in inp if x]), 1) if any(inp) else None,
                            "sum": sum(x for x in inp if x)},
           "batch_rows": {"mean": round(statistics.fmean([r["batch_rows"] for r in ok
                                                          if isinstance(r.get("batch_rows"), (int, float))]), 3)
                          if any(isinstance(r.get("batch_rows"), (int, float)) for r in ok) else None,
                          "hist": dict(Counter(str(r.get("batch_rows")) for r in ok))},
           "paths": dict(Counter(str(r.get("path")) for r in ok)), "engines": dict(Counter(str(r.get("engine"))
                                                                                       for r in ok)),
           "cached_token_share": round(sum(c for c, _ in cached) / sum(t for _, t in cached), 4) if cached else None,
           "cached_field": sorted({r["cached_key"] for r in ok if r.get("cached_key")}) or None,
           "error_examples": [r["error"] for r in recs if r["error"]][:3]}
    if flags:
        out.update(flags)
    if tok_counts:
        pairs = [(tok_counts.get(r["id"]), (r.get("q_usage") or {}).get("input_tokens_first_view")) for r in ok]
        pairs = [(a, b) for a, b in pairs if a is not None]
        out["token_check"] = {"checked": len(pairs), "equal": sum(a == b for a, b in pairs),
                              "server_missing": sum(b is None for _, b in pairs),
                              "max_abs_diff": max((abs(a - b) for a, b in pairs if b is not None), default=None)}
    return out


def run_level(url, token, items, conc, warm_s=SETTINGS["warmup_s"], win_s=SETTINGS["window_s"],
              timeout=SETTINGS["timeout_s"], wrap=False, start_at=0, tok_counts=None, stop=None,
              warm_frac=SETTINGS["warmup_max_frac"], abort=None):
    """One closed-loop level (load_test_c1.run_level, copied): `conc` threads, one keep-alive connection each, send
    calls back to back in workload order from start_at. win_s=None is a PASS: every call exactly once, no warm-up,
    throughput over the whole pass. Otherwise a warm-up, then a window of win_s; a call counts when it completes inside
    the window. The warm-up ends after warm_s seconds or when the first warm_frac of the level's calls have started,
    whichever is first (S has 660 rows: a fast arm at c=16 would otherwise spend the whole level warming up).
    wrap=False (default): no call is sent twice in a level, and the window ends when the workload runs out (from then
    on fewer than conc calls are in flight). abort (default ABORT): the level stops early after `consecutive` failed
    calls in a row, or once >= `failed_min` calls failed and they are > `failed_frac` of the calls done (0 turns a
    rule off); the summary then carries "aborted" (why). -> (summary, records, next index)."""
    lock, nxt, recs, drained, warmed = threading.Lock(), [start_at], [], [None], [None]
    stop = stop or threading.Event()
    ab = {**ABORT, **(abort or {})}
    halt, why, t_halt, cnt = threading.Event(), [None], [None], {"run": 0, "failed": 0, "done": 0}
    n, passing = len(items), win_s is None
    warm_n = int(warm_frac * n)
    t_base = time.perf_counter()
    t_warm = t_base + (0.0 if passing else warm_s)
    t_end = math.inf if passing else t_warm + win_s

    def tally(ok):  # under lock
        cnt["done"] += 1
        cnt["run"] = 0 if ok else cnt["run"] + 1
        cnt["failed"] += not ok
        if why[0] is None:
            if ab["consecutive"] and cnt["run"] >= ab["consecutive"]:
                why[0] = f"{cnt['run']} failed calls in a row"
            elif (ab["failed_min"] and cnt["failed"] >= ab["failed_min"]
                  and cnt["failed"] > ab["failed_frac"] * cnt["done"]):
                why[0] = f"{cnt['failed']} of {cnt['done']} calls failed (> {ab['failed_frac']:.0%})"
            if why[0] is not None:
                t_halt[0] = time.perf_counter()
                halt.set()

    def worker(w):
        c = V1(url, token, timeout)
        try:
            while not stop.is_set() and not halt.is_set() and time.perf_counter() < t_end:
                with lock:
                    i = nxt[0]
                    if not wrap and i - start_at >= n:
                        if drained[0] is None:
                            drained[0] = time.perf_counter()
                        return
                    nxt[0] += 1
                    if warmed[0] is None and i - start_at >= warm_n:
                        warmed[0] = time.perf_counter()  # the first call after the warm-up share starts
                item = items[i % n]
                t0 = time.perf_counter()
                d, ms, st, err = c.call(item["request"])
                t1 = time.perf_counter()
                rec = make_record(item, i, w, t0, t1, d, ms, st, err, t_base)
                with lock:
                    recs.append(rec)
                    tally(rec["ok"])
        finally:
            c.close()

    th = [threading.Thread(target=worker, args=(w,), daemon=True) for w in range(conc)]
    for t in th:
        t.start()
    try:
        for t in th:
            while t.is_alive():
                t.join(0.5)
    except KeyboardInterrupt:
        stop.set()
        raise
    recs.sort(key=lambda r: (r["t0"], r["i"]))
    flags = {}
    if why[0] is not None:
        flags["aborted"] = why[0]
    if passing:
        lo, hi, win, mode = 0.0, max((r["t1"] for r in recs), default=0.0), recs, "pass"
    else:
        mode = "window"
        lo = min(t_warm, warmed[0] if warmed[0] is not None else math.inf) - t_base
        hi = min(t_end, drained[0] if drained[0] is not None else math.inf,
                 t_halt[0] if t_halt[0] is not None else math.inf) - t_base
        flags["drained"] = drained[0] is not None
        flags["warmup_ended_by"] = "time" if lo >= warm_s - 1e-9 else f"first {warm_frac:.0%} of calls"
        if hi <= lo:  # the workload ran out inside the warm-up: measure everything, flagged
            lo, hi = 0.0, hi
            flags["short_workload"] = True
        win = [r for r in recs if lo <= r["t1"] <= hi]
    return summarize_level(recs, win, conc, lo, hi, mode, tok_counts, flags), recs, nxt[0]


def first_answers(recs) -> dict:
    out = {}
    for r in sorted(recs, key=lambda r: r["i"]):
        if r["ok"] and r["id"] not in out:
            out[r["id"]] = {"id": r["id"], "probs": r["probs"], **({"views": r["views"]} if r.get("views") else {})}
    return out


def sustained(levels) -> tuple:
    """load_test_c1's rule: the highest throughput over the levels with 0 failed calls -> (decisions/h, concurrency)."""
    good = [lv for lv in levels if lv["failed_calls"] == 0 and lv["decisions_in_window"] > 0]
    best = max(good, key=lambda lv: lv["decisions_per_hour"]) if good else None
    return (best["decisions_per_hour"], best["concurrency"]) if best else (None, None)


def cost_table(dph, rate=RATE_USD_H, mults=None, utils=UTILS) -> dict:
    """$/1K decisions = rate x region_mult / decisions per hour x 1000, divided by the utilisation."""
    mults = mults or REGION_MULT
    out = {"rate_usd_h_base": rate, "region_mult": dict(mults), "utilisations": list(utils),
           "sustained_decisions_per_hour": dph, "usd_per_1k": {}}
    for reg, m in mults.items():
        out["usd_per_1k"][reg] = {f"{round(u * 100)}%": (round(rate * m / (dph * u) * 1000, 6) if dph else None)
                                  for u in utils}
    return out


# ------------------------------------------------------------------ parity

def load_stored(name, splits=None) -> dict:
    """{id: probs} of a stored L4 read over the gate dev splits (gate_dev.load: read-only)."""
    out = {}
    for sp in (splits or gate_dev.SPLITS.split(",")):
        check_split(sp)
        out.update(gate_dev.load(sp, name) or {})
    return out


def read_answers(p) -> tuple:
    """answers_<W>.jsonl -> ({id: probs}, {id: views})."""
    probs, views = {}, {}
    if Path(p).exists():
        for r in read_jsonl(p):
            probs[r["id"]] = r["probs"]
            if r.get("views"):
                views[r["id"]] = r["views"]
    return probs, views


def row_group(r) -> str:
    return bucket(r["qtype"], len(r.get("options") or []))


def compare(rows, cand, ref, acc_bar=BARS["acc_diff_max_pt"], agree_min=BARS["argmax_agree_min"]) -> dict:
    """cand vs ref ({id: probs}) on rows (dev rows with gold): argmax agreement (missing = disagree), gate accuracy of
    each and the difference (pt; missing = wrong), per-row max |dp| (mean / p99 / max over rows both answered), by
    type/options bucket and by dev half; PASS when agreement >= agree_min and |diff| <= acc_bar."""
    def block(rs):
        n = len(rs)
        if not n:
            return {"n": 0}
        both = [x for x in rs if x[1] is not None and x[2] is not None]
        dps = [x[3] for x in both]
        agree = sum(x[4] for x in both)
        okc, okr = sum(x[5] for x in rs), sum(x[6] for x in rs)
        return {"n": n, "compared": len(both), "missing_cand": sum(x[1] is None for x in rs),
                "missing_ref": sum(x[2] is None for x in rs), "argmax_agree": round(agree / n, 6),
                "argmax_disagree_rows": n - agree, "acc_cand": round(100 * okc / n, 3),
                "acc_ref": round(100 * okr / n, 3),
                "acc_diff_pt": round(100 * (okc - okr) / n, 3),
                "dp_mean": round(statistics.fmean(dps), 6) if dps else None,
                "dp_p99": round(cb.pct(sorted(dps), 0.99), 6) if dps else None,
                "dp_max": round(max(dps), 6) if dps else None}

    per = []
    for r in rows:
        c, f = cand.get(r["id"]), ref.get(r["id"])
        keys = ["yes", "no"] if r["qtype"] == "noul" else list(r["options"])
        dp = max(abs(float(c.get(k, 0.0)) - float(f.get(k, 0.0))) for k in keys) if c and f else None
        ag = bool(c and f and gate_dev.argmax_label(r, c) == gate_dev.argmax_label(r, f))
        per.append((r, c, f, dp, ag, gate_dev.score(r, c)[0], gate_dev.score(r, f)[0]))
    out = block(per)
    out["by_group"] = {g: block([x for x in per if row_group(x[0]) == g]) for g in GROUPS
                       if any(row_group(x[0]) == g for x in per)}
    out["by_half"] = {h: block([x for x in per if x[0].get("group_id") is not None
                                and gate_dev.half(x[0]["group_id"]) == h]) for h in ("select", "confirm")}
    out["bar"] = {"argmax_agree_min": agree_min, "acc_diff_max_pt": acc_bar}
    out["pass"] = bool(out["n"] and out["argmax_agree"] >= agree_min and abs(out["acc_diff_pt"]) <= acc_bar)
    return out


def reversed_from(served, identity, rows) -> dict:
    """The reversed-order view of a 2view read: served = (identity + reversed) / 2 per option, so
    reversed = 2 * served - identity (choice rows where both reads exist)."""
    out = {}
    for r in rows:
        s, p = served.get(r["id"]), identity.get(r["id"])
        if r["qtype"] == "choice" and s and p:
            out[r["id"]] = {o: 2 * float(s.get(o, 0.0)) - float(p.get(o, 0.0)) for o in r["options"]}
    return out


def view_consistency(rev, tol=1e-4) -> dict:
    """A reconstructed reversed view must be a distribution: every value in [0, 1] and the sum 1 (within tol)."""
    bad, worst = 0, 0.0
    for p in rev.values():
        v = max([max(-x, x - 1.0, 0.0) for x in p.values()] + [abs(sum(p.values()) - 1.0)])
        worst = max(worst, v)
        bad += v > tol
    return {"rows": len(rev), "invalid_rows": bad, "max_violation": round(worst, 8), "tol": tol,
            "pass": bool(rev) and bad == 0}


def reversed_view_check(rows, cand_served, cand_views, cand_identity, ref_served, ref_identity, acc_bar) -> dict:
    """Identity view vs the reference's identity read, and reversed view vs the reference's reversed view
    (2 * served - identity), on choice rows. The candidate's views come from per-view answers, else from an identity
    pass (reversed = 2 * served - identity). -> {"available": False} when the candidate has neither."""
    ch = [r for r in rows if r["qtype"] == "choice"]
    if cand_views:
        c_id = {k: v["identity"] for k, v in cand_views.items()}
        c_rev = {k: v["reversed"] for k, v in cand_views.items()}
        src = "per-view answers"
    elif cand_identity:
        c_id, c_rev, src = cand_identity, reversed_from(cand_served, cand_identity, ch), "identity pass"
    else:
        return {"available": False, "why": "the arm returned only the 2view average (no per-view answers, no "
                                           "identity pass)"}
    have = [r for r in ch if r["id"] in c_id]
    r_rev = reversed_from(ref_served, ref_identity, have)
    return {"available": True, "source": src, "rows": len(have),
            "identity": compare(have, c_id, ref_identity, acc_bar),
            "reversed": compare(have, c_rev, r_rev, acc_bar),
            "cand_reversed_consistency": view_consistency({k: c_rev[k] for k in c_rev if k in r_rev})}


# ------------------------------------------------------------------ Jev (report-only)

class JevS(cb.Jev):
    """client_bench.Jev for single-question API v1 requests. The dev card goes in as the choice options' descriptions
    (criteria {option: definition}); the Jev API takes no definitions on a yes/no question, so a yes/no card is dropped
    (counted) unless noul_card="instructions" (then "Definitions:" + card is put before the question). With the
    typesafe SDK installed the SDK route of client_bench.Jev is used; without it (this venv) the same
    POST /v1/systemone body goes out through httpx on OpenRouter's endpoint. Retries off; the key is never printed."""

    def __init__(self, base_url=None, model=None, timeout=60.0, noul_card="drop"):
        self.noul_card, self.raw = noul_card, None
        try:
            import typesafe_sdk  # noqa: F401
            sdk = True
        except ImportError:
            sdk = False
        if sdk:
            super().__init__(base_url, model, timeout)
            return
        cb.load_env()
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise SystemExit("NO_KEY: set OPENROUTER_API_KEY (env or opendecide-data/.env)")
        base = base_url or os.environ.get("JEV_BASE_URL") or cb.OPENROUTER_BASE
        self.route = "openrouter (httpx, no SDK)" if base == cb.OPENROUTER_BASE else f"override {base} (httpx)"
        self.model = model or os.environ.get("JEV_MODEL") or "jev-1.13"
        self.raw = httpx.Client(base_url=base.rstrip("/"), timeout=timeout,
                                transport=httpx.HTTPTransport(retries=0),
                                headers={"Authorization": f"Bearer {key}"})

    def questions(self, req) -> tuple:
        dio = _dio()
        qs, dropped = {}, 0
        for k, q in req["questions"].items():
            if q["type"] == "noul":
                ins = q["instructions"]
                if q.get("card"):
                    if self.noul_card == "instructions":
                        ins = f"Definitions:\n{q['card']}\n\n{ins}"
                    else:
                        dropped += 1
                qs[k] = {"type": "noul", "instructions": ins}
            else:
                defs = dio.card_defs(q.get("card"))
                qs[k] = {"type": "choice", "instructions": q["instructions"],
                         "criteria": {o: defs.get(o) for o in q["options"]}}
        return qs, dropped

    def decide(self, req):
        """-> (normalised {"model", "usage", "answers", "request_id", "timing_headers"}, ms, error, cards dropped)."""
        qs, dropped = self.questions(req)
        if self.raw is None:  # SDK route (as client_bench.Jev.decide, with the definitions)
            from typesafe_sdk import Choice, Noul
            sq = {k: Noul(instructions=q["instructions"]) if q["type"] == "noul"
                  else Choice(instructions=q["instructions"], criteria=q["criteria"]) for k, q in qs.items()}
            t = time.perf_counter()
            try:
                res = self.client.system_one(state=req["state"], questions=sq, model=self.model)
            except Exception as e:  # noqa: BLE001
                return None, (time.perf_counter() - t) * 1000, f"{type(e).__name__}: {e}"[:300], dropped
            ms = (time.perf_counter() - t) * 1000
            raw = res.__dict__.get("_raw")
            return ({"model": res.model, "usage": res.usage.model_dump() if res.usage else None,
                     "answers": {k: v.model_dump() for k, v in res.answers.items()},
                     "request_id": res.__dict__.get("_request_id"),
                     "timing_headers": {k: v for k, v in (raw.headers.items() if raw is not None else [])
                                        if any(w in k.lower() for w in cb.TIMING_HEADER_WORDS)}}, ms, None, dropped)
        body = {"model": self.model, "state": req["state"], "questions": qs}
        t = time.perf_counter()
        try:
            r = self.raw.post("/v1/systemone", json=body)
            d = r.json() if r.status_code == 200 else None
        except Exception as e:  # noqa: BLE001
            return None, (time.perf_counter() - t) * 1000, f"{type(e).__name__}: {e}"[:300], dropped
        ms = (time.perf_counter() - t) * 1000
        if d is None:
            return None, ms, f"HTTP {r.status_code}: {r.text[:300]}", dropped
        hdr = {k: v for k, v in r.headers.items() if any(w in k.lower() for w in cb.TIMING_HEADER_WORDS)}
        return ({"model": d.get("model"), "usage": d.get("usage"), "answers": d.get("answers") or {},
                 "request_id": r.headers.get("x-typesafe-request-id") or r.headers.get("x-request-id"),
                 "timing_headers": hdr}, ms, None, dropped)

    def close(self):
        if self.raw is not None:
            self.raw.close()
        else:
            super().close()


def jev_probs(ans, item):
    """Jev answer -> gate-format probabilities (choice: renormalised over the row's options, as cb.jev_probs)."""
    if not isinstance(ans, dict):
        return None
    if item["qtype"] == "noul":
        p = ans.get("noul")
        return None if p is None else {"yes": float(p), "no": 1.0 - float(p)}
    pr = {k: float(v) for k, v in (ans.get("probabilities") or {}).items()}
    opts = item["request"]["questions"]["q0"]["options"]
    s = sum(pr.get(o, 0.0) for o in opts)
    return {o: pr.get(o, 0.0) / s for o in opts} if s > 0 else None


def run_jev(session_dir, items, go=False, max_calls=None, warm=3, base_url=None, model=None, timeout=60.0,
            noul_card="drop", overwrite=False, log=print) -> dict:
    """S at concurrency 1 through Jev (OpenRouter), dev only, report-only. Without go: the plan only."""
    items = items[:max_calls] if max_calls else items
    plan = {"calls_timed": len(items), "warmup_calls_not_timed": min(warm, len(items)), "concurrency": 1,
            "noul_card": noul_card, "cards_on_noul_rows": sum(1 for it in items if it["qtype"] == "noul"
                                                              and it["request"]["questions"]["q0"].get("card")),
            "note": "OpenRouter bills per call (Jev price per call is not known here); report-only, never trained on"}
    if not go:
        log("JEV PLAN (nothing sent; add --go): " + json.dumps(plan))
        return {"plan": plan}
    out = Path(session_dir) / JEV_DIR
    if (out / "summary.json").exists() and not overwrite:
        raise SystemExit(f"{out} already has a summary.json (pass --overwrite)")
    out.mkdir(parents=True, exist_ok=True)
    jv = JevS(base_url, model, timeout, noul_card)
    recs, dropped, interrupted = [], 0, False
    try:
        for it in items[:warm]:  # not recorded (connection, OpenRouter routing)
            jv.decide(it["request"])
        for k, it in enumerate(items):
            d, ms, err, dr = jv.decide(it["request"])
            dropped += dr
            rec = {"i": k, "id": it["id"], "client_ms": round(ms, 3), "error": err, "card_dropped": bool(dr)}
            if d is not None:
                probs = jev_probs((d.get("answers") or {}).get("q0"), it)
                rec.update(model=d.get("model"), usage=d.get("usage"), request_id=d.get("request_id"),
                           timing_headers=d.get("timing_headers"), probs=probs)
                if probs is None:
                    rec["error"] = "no usable answer for q0"
            recs.append(rec)
            if (k + 1) % 50 == 0:
                log(f"  jev {k + 1}/{len(items)}")
    except KeyboardInterrupt:  # paid calls already made are kept
        interrupted = True
        log(f"interrupted after {len(recs)} calls: writing what was answered")
    finally:
        jv.close()
    good = [r for r in recs if r["error"] is None]
    write_jsonl(out / "calls_S_c1.jsonl", recs)
    write_jsonl(out / "answers_S.jsonl", [{"id": r["id"], "probs": r["probs"]} for r in good])
    s = {"name": JEV_DIR, "utc": utc(), "route": jv.route, "model": jv.model, "workload": "S", "concurrency": 1,
         "calls": len(recs), "errors": len(recs) - len(good), "error_examples": [r["error"] for r in recs
                                                                                 if r["error"]][:3],
         "client_ms": pcts([r["client_ms"] for r in good]), "cards_dropped": dropped, "noul_card": noul_card,
         "models": dict(Counter(str(r.get("model")) for r in good)), "interrupted": interrupted,
         "do_not_train_on_jev_outputs": True}
    write_json(out / "summary.json", s)
    log(f"jev: {len(good)}/{len(recs)} answered, client p50 {s['client_ms'].get('p50')} ms -> {out}")
    return s


# ------------------------------------------------------------------ arms + the ab orchestration

def load_arms(path=ARMS_FILE) -> dict:
    cfg = json.loads(Path(path).read_text())
    for name, a in cfg["arms"].items():
        for k in ("engine", "flags", "fp8"):
            if k not in a:
                raise SystemExit(f"{path}: arm {name} has no {k!r}")
    return cfg


def _quant(v):
    return None if v in (None, False, "", "none", "None", "bf16", "BF16") else str(v).lower()


def lookup(h, k):
    return h[k] if k in h else (h.get("flags") or {}).get(k)


def check_boot(h, arm, acfg, adapter_sha=C1_ADAPTER_SHA256):
    """The endpoint must serve C1 (adapter sha256) on this arm's boot (expect_health)."""
    if h.get("ok") is False:
        raise ArmRefused(f"{arm}: /health ok=false {json.dumps(h.get('problems') or [])[:300]}")
    if h.get("adapter_sha256") != adapter_sha:
        raise ArmRefused(f"{arm}: /health adapter_sha256 {str(h.get('adapter_sha256'))[:16]} is not C1's "
                         f"{adapter_sha[:16]}")
    for k, want in (acfg.get("expect_health") or {}).items():
        got = lookup(h, k)
        same = _quant(got) == _quant(want) if k == "quantization" else got == want
        if not same:
            raise ArmRefused(f"{arm}: /health {k}={got!r}, this arm needs {want!r} (run it from its own boot)")


def check_flags(h, arm, flags):
    hf = h.get("flags") or {}
    bad = {k: [v, hf.get(k, "<absent>")] for k, v in flags.items() if hf.get(k, object()) != v}
    if bad:
        raise ArmRefused(f"{arm}: flags not read back from /health after /admin/config (sent, got): {bad}")


def est_level_s(n_calls, conc, passing, warm_s, win_s, est=EST) -> float:
    """Wall estimate for the dry run: no cross-request batching assumed (GPU-serialised), so an upper-ish bound."""
    rate = min(conc * 1000.0 / (est["net_ms"] + est["gpu_ms"]), 1000.0 / est["gpu_ms"])  # calls/s
    t = n_calls / rate
    return t if passing else min(warm_s + win_s, t)


def plan_arm(arm, acfg, man, settings, est=EST, plan=PLAN) -> dict:
    steps = [{"step": "health + boot check + /admin/config + flags read-back", "est_s": est["admin_s"]}]
    frac = settings.get("warmup_max_frac", SETTINGS["warmup_max_frac"])
    win = (f" (warm-up <= {settings['warmup_s']} s or the first {frac:.0%} of calls, then window "
           f"{settings['window_s']} s, no repeats)")
    for W, levels in plan:
        n = man["workloads"][W]["calls"]
        for c in levels:
            passing = W == "P"
            est_s = est_level_s(n, c, passing, settings["warmup_s"], settings["window_s"], est) + 0.5
            px = f", request + {json.dumps(acfg['p_request_extra'])}" if passing and acfg.get("p_request_extra") else ""
            steps.append({"step": f"{W} c={c}" + (f" (pass: every row once, answers saved{px})" if passing else win),
                          "calls_max": n, "est_s": round(est_s, 1)})
    if acfg.get("identity_flags"):
        n = man["workloads"]["P"]["groups"]
        nc = sum(v for g, v in n.items() if g != "noul")
        steps.append({"step": "identity pass: P choice rows c=16 with identity_flags", "calls_max": nc,
                      "est_s": round(est_level_s(nc, 16, True, 0, 0, est), 1)})
    total = sum(s["est_s"] for s in steps)
    return {"arm": arm, "engine": acfg["engine"], "boot": acfg.get("boot"), "flags": acfg["flags"],
            "expect_health": acfg.get("expect_health"), "steps": steps, "est_wall_s": round(total, 1)}


def print_plan(plans, settings, rate, mults, est=EST, log=print, fit=None):
    """fit (optional): {arm: conservative wall seconds at the fit GPU time, "gpu_ms": ...} (what --go checks against
    the endpoint's remaining serving window)."""
    log(f"PLAN (nothing sent). Estimate assumes network {est['net_ms']} ms + GPU {est['gpu_ms']} ms per call and NO "
        f"cross-request batching (an upper-ish bound; batching arms finish sooner).")
    tot = 0.0
    for p in plans:
        log(f"\n[{p['arm']}] engine {p['engine']} boot {p['boot']} flags {json.dumps(p['flags'])}")
        for s in p["steps"]:
            cap = f"  ({s['calls_max']} calls max)" if "calls_max" in s else ""
            log(f"   {s['est_s']:7.1f} s  {s['step']}{cap}")
        fx = f" ({fit[p['arm']] / 60:.1f} min at {fit['gpu_ms']:g} ms/call, the fit check)" if fit else ""
        log(f"   = {p['est_wall_s'] / 60:.1f} min{fx}")
        tot += p["est_wall_s"]
    h = tot / 3600
    usd = {reg: round(h * rate * m, 2) for reg, m in mults.items()}
    log(f"\nall arms: {tot / 60:.1f} min of client time; the endpoint bills while it is up: about "
        + ", ".join(f"${v} ({k})" for k, v in usd.items()) + f" at ${rate}/h x region multiplier (to be confirmed)")
    out = {"total_s": round(tot, 1), "usd_estimate": usd}
    if fit:
        out["fit_total_s"] = round(sum(v for k, v in fit.items() if k != "gpu_ms"), 1)
        log(f"conservative (fit check, GPU {fit['gpu_ms']:g} ms/call): {out['fit_total_s'] / 60:.1f} min; each arm "
            f"must fit the endpoint's /health serve_remaining_s (+{FIT_MARGIN_S:.0f} s) when it starts")
    return out


def run_workload(url, token, W, items, levels, settings, out_dir, tok_counts=None, passing=False, stop=None,
                 log=print) -> dict:
    """The levels of one workload, POST /admin/flush before each. Stops at the first aborted level (or a failed
    flush: the endpoint is down) and returns what ran, with "aborted" (why)."""
    levels_out, recs_all, aborted = [], [], None
    for c in levels:
        cl = V1(url, token, settings["timeout_s"])
        try:
            cl.flush()
        except Exception as e:  # noqa: BLE001 - down or refusing: nothing more is timed on it
            aborted = f"POST /admin/flush before {W} c={c} failed: {type(e).__name__}: {e}"[:400]
        finally:
            cl.close()
        if aborted:
            log(f"  ABORTED {aborted}")
            break
        summ, recs, _ = run_level(url, token, items, c, settings["warmup_s"], None if passing else settings["window_s"],
                                  settings["timeout_s"], tok_counts=tok_counts, stop=stop,
                                  warm_frac=settings.get("warmup_max_frac", SETTINGS["warmup_max_frac"]),
                                  abort=settings.get("abort"))
        write_jsonl(out_dir / f"calls_{W}_c{c}.jsonl", recs)
        levels_out.append(summ)
        recs_all += recs
        log(f"  {W} c={c:2d}: {summ['decisions_per_hour']:,.0f} decisions/h, ok {summ['calls_ok_in_window']}/"
            f"{summ['calls_sent']}, failed {summ['failed_calls']}, client p50 {summ['client_ms'].get('p50')} / p99 "
            f"{summ['client_ms'].get('p99')} ms, server p50 {summ['server_ms'].get('p50')} ms, batch_rows "
            f"{summ['batch_rows']['mean']}, cached {summ['cached_token_share']}")
        if summ.get("aborted"):
            aborted = f"{W} c={c}: {summ['aborted']} (e.g. {(summ['error_examples'] or ['?'])[0]})"[:400]
            log(f"  ABORTED {aborted}")
            break
    ans = first_answers(recs_all)
    write_jsonl(out_dir / f"answers_{W}.jsonl", list(ans.values()))
    out = {"levels": levels_out, "answers": len(ans), "rows": len({it['id'] for it in items})}
    if aborted:
        out["aborted"] = aborted
    return out


def check_fit(h, arm, need_s, margin_s=FIT_MARGIN_S):
    """Refuse (ArmRefused, nothing timed) an arm whose conservative wall estimate need_s + margin_s does not fit the
    endpoint's remaining serving window (/health serve_remaining_s). -> the remaining seconds, or None when either is
    unknown (not checked)."""
    rem = h.get("serve_remaining_s")
    if need_s is None or isinstance(rem, bool) or not isinstance(rem, (int, float)):
        return None
    if need_s + margin_s > rem:
        raise ArmRefused(f"{arm}: does not fit the endpoint's serving window: needs ~{need_s / 60:.1f} min "
                         f"(+{margin_s:.0f} s margin, plan at the fit GPU time), {rem / 60:.1f} min left; run it from "
                         f"its own boot")
    return rem


def recheck(url, token, arm, acfg, adapter_sha, timeout):
    """Between workloads: the endpoint must still be healthy, on C1, on this arm's boot and on its flags. -> None, or
    why not (the arm is then aborted: its later workloads are not timed)."""
    cl = V1(url, token, timeout)
    try:
        h = cl.health()
        check_boot(h, arm, acfg, adapter_sha)
        check_flags(h, arm, acfg["flags"])
    except Exception as e:  # noqa: BLE001 - ArmRefused, HTTP errors, a dead tunnel
        return f"{type(e).__name__}: {e}"[:400]
    finally:
        cl.close()
    return None


def endpoint_problem(url, token, timeout=30.0):
    """None when GET /health answers and is not ok=false; else why not (after an aborted arm: stop the session?)."""
    c = V1(url, token, timeout)
    try:
        h = c.health()
        return None if h.get("ok") is not False else f"/health ok=false {json.dumps(h.get('problems') or [])[:300]}"
    except Exception as e:  # noqa: BLE001 - unreachable (window closed, tunnel gone)
        return f"{type(e).__name__}: {e}"[:300]
    finally:
        c.close()


def post_shutdown(url, token, timeout=30.0, log=print) -> dict:
    """POST /shutdown: the host stops serving and its GPU stops billing. Never raises (it may already be gone)."""
    c = V1(url, token, timeout)
    try:
        r = c.c.post("/shutdown")
        out = {"ok": r.status_code == 200, "status": r.status_code}
    except Exception as e:  # noqa: BLE001
        out = {"ok": False, "error": f"{type(e).__name__}: {e}"[:300]}
    finally:
        c.close()
    log(f"POST /shutdown: {json.dumps(out)}")
    return out


def run_arm(url, token, arm, acfg, wls, tok_prof, settings, out_dir, plan=PLAN, adapter_sha=C1_ADAPTER_SHA256,
            rate=RATE_USD_H, mults=None, stop=None, need_s=None, log=print) -> dict:
    """One arm on the endpoint. Refused (ArmRefused, nothing timed or written) on a wrong boot, flags that do not read
    back, or when need_s (its conservative wall estimate) does not fit /health serve_remaining_s. Once timing started,
    a failed /health or flags re-check between workloads, a failed flush or an aborted level ends the arm: the summary
    then has "aborted" (and "complete": false) and the caller stops the session."""
    idf = acfg.get("identity_flags")
    if idf and not (isinstance(idf, dict) and isinstance(idf.get("on"), dict) and isinstance(idf.get("off"), dict)):
        raise ArmRefused(f"{arm}: identity_flags must be null or {{\"on\": {{...}}, \"off\": {{...}}}}")
    cl = V1(url, token, settings["timeout_s"])
    try:
        h0 = cl.health()
        check_boot(h0, arm, acfg, adapter_sha)
        rem = check_fit(h0, arm, need_s)
        resp = cl.config(acfg["flags"])
        h1 = cl.health()
        check_flags(h1, arm, acfg["flags"])
    finally:
        cl.close()
    out_dir.mkdir(parents=True, exist_ok=True)  # only for an arm the endpoint really serves
    write_json(out_dir / "health_before.json", h0)
    write_json(out_dir / "config.json", {"flags": acfg["flags"], "response": resp})
    write_json(out_dir / "health.json", h1)
    fit = (f"fits: ~{need_s / 60:.1f} min needed, {rem / 60:.1f} min left" if rem is not None else
           "fit not checked (the endpoint reports no serving window)" if need_s is not None else "fit check off")
    log(f"[{arm}] engine {h1.get('engine')} gpu {h1.get('gpu')} region {h1.get('region')} flags read back OK; {fit}")
    t0 = time.time()
    res, aborted = {}, None
    extra = acfg.get("p_request_extra") or {}
    for k, (W, levels) in enumerate(plan):
        if k:  # the endpoint may have died (CUDA-fatal error), closed its window or lost the arm's flags
            why = recheck(url, token, arm, acfg, adapter_sha, settings["timeout_s"])
            if why:
                aborted = f"/health re-check before {W}: {why}"
                log(f"  ABORTED {aborted}")
                break
        tc = (tok_prof or {}).get(W, {}).get("per_row")
        items = wls[W]
        if W == "P" and extra:  # e.g. return_views: per-view answers for the reversed-view check (no extra pass)
            items = [{**it, "request": {**it["request"], **extra}} for it in items]
        res[W] = run_workload(url, token, W, items, levels, settings, out_dir, tc, passing=(W == "P"), stop=stop,
                              log=log)
        if res[W].get("aborted"):
            aborted = res[W]["aborted"]
            break
    if idf and not aborted:  # reversed-view check: P's choice rows once in the identity view, then the arm's flags back
        on, off = {**acfg["flags"], **idf["on"]}, {**acfg["flags"], **idf["off"]}
        cl = V1(url, token, settings["timeout_s"])
        try:
            cl.config(on)
            check_flags(cl.health(), arm, on)
            cl.flush()
            ch = [it for it in wls["P"] if it["qtype"] == "choice"]
            summ, recs, _ = run_level(url, token, ch, 16, 0, None, settings["timeout_s"], stop=stop)
            write_jsonl(out_dir / "calls_P_identity_c16.jsonl", recs)
            write_jsonl(out_dir / "answers_P_identity.jsonl", list(first_answers(recs).values()))
            res["P_identity"] = {"levels": [summ]}
            log(f"  P identity pass: {summ['calls_ok_in_window']}/{summ['calls_sent']} ok")
        finally:
            try:
                cl.config(off)
                check_flags(cl.health(), arm, off)
            finally:
                cl.close()
    cl = V1(url, token, settings["timeout_s"])
    try:
        h2 = cl.health()
    except Exception as e:  # noqa: BLE001 - after an abort the endpoint may be gone; the summary is still written
        h2 = {"error": f"{type(e).__name__}: {e}"[:300]}
    finally:
        cl.close()
    write_json(out_dir / "health_after.json", h2)
    dph, at = sustained(res["S"]["levels"]) if "S" in res else (None, None)
    has_p = any(W == "P" for W, _ in plan)
    p_ans, p_rows = (res.get("P") or {}).get("answers", 0), len({it["id"] for it in wls["P"]}) if has_p else 0
    complete = aborted is None and p_ans == p_rows
    if not complete:
        log(f"  WARNING [{arm}] {'aborted: ' + aborted if aborted else 'not aborted'}; P answered {p_ans}/{p_rows} "
            f"rows: its parity gate will read INCOMPLETE (or FAIL)")
    s = {"arm": arm, "utc": utc(), "wall_s": round(time.time() - t0, 1), "engine": h1.get("engine"),
         "gpu": h1.get("gpu"), "region": h1.get("region"), "boot_s": h1.get("boot_s"), "model": h1.get("model"),
         "adapter_sha256": h1.get("adapter_sha256"), "config_sha256": h1.get("config_sha256"),
         "flags": acfg["flags"], "p_request_extra": extra, "fp8": bool(acfg.get("fp8")), "settings": settings,
         "aborted": aborted, "complete": complete, "p_answered": p_ans, "p_rows": p_rows,
         "fit": {"need_s": need_s, "remaining_s_at_start": rem},
         "workloads": res, "sustained_decisions_per_hour": dph, "sustained_at_concurrency": at,
         "sustained_rule": "max decisions/h over the S levels with 0 failed calls",
         "cost": cost_table(dph, rate, mults or REGION_MULT),
         "served_before_after": [h0.get("served"), h2.get("served")]}
    write_json(out_dir / "summary.json", s)
    return s


def run_ab(url, token, session, arms, arms_cfg, wl_dir=WORKLOADS, out_root=SPEED, settings=None, go=False,
           overwrite=False, rate=RATE_USD_H, mults=None, est=EST, adapter_sha=C1_ADAPTER_SHA256, log=print,
           shutdown_after=False, fit_gpu_ms=FIT_GPU_MS) -> dict:
    """The arms in the given order on one endpoint. An aborted arm stops the session (the rest are skipped) when
    /health is then not ok or unreachable (dead GPU, closed window); a refused arm, or an aborted one on a healthy
    endpoint (the arm's own failures), does not. shutdown_after: POST /shutdown when this ends (all arms, an abort,
    Ctrl-C), unless every arm was refused before timing."""
    settings = {**SETTINGS, **(settings or {})}
    mults = mults or REGION_MULT
    unknown = [a for a in arms if a not in arms_cfg["arms"]]
    if unknown:
        raise SystemExit(f"unknown arms {unknown}; defined: {list(arms_cfg['arms'])}")
    if "/" in session or session in ("workloads", "") or session.startswith("."):
        raise SystemExit(f"bad --session {session!r}")
    man = json.loads((Path(wl_dir) / "manifest.json").read_text())
    plans = [plan_arm(a, arms_cfg["arms"][a], man, settings, est) for a in arms]
    fit = None
    if fit_gpu_ms:
        fest = {**est, "gpu_ms": max(float(est["gpu_ms"]), float(fit_gpu_ms))}
        fit = {a: plan_arm(a, arms_cfg["arms"][a], man, settings, fest)["est_wall_s"] for a in arms}
        fit["gpu_ms"] = fest["gpu_ms"]
    if not go:
        p = print_plan(plans, settings, rate, mults, est, log, fit=fit)
        log("\nadd --go to run it against the endpoint (it must already be up; this client starts nothing)")
        return {"plan": plans, **p}
    sdir = Path(out_root) / session
    for a in arms:
        if (sdir / a / "summary.json").exists() and not overwrite:
            raise SystemExit(f"{sdir / a} already has a summary.json (pass --overwrite or another --session)")
    wls = {W: load_workload(wl_dir, W, man) for W in WORKLOAD_NAMES}
    tp = Path(wl_dir) / "token_profile.json"
    tok_prof = json.loads(tp.read_text()) if tp.exists() else None
    if tok_prof and (tok_prof.get("info") or {}).get("workloads_sha256") != {
            W: man["workloads"][W]["sha256"] for W in WORKLOAD_NAMES}:
        log(f"{tp} does not belong to these workloads: no token check")
        tok_prof = None
    sdir.mkdir(parents=True, exist_ok=True)
    sess_p = sdir / "session.json"
    sess = json.loads(sess_p.read_text()) if sess_p.exists() else {"session": session, "runs": []}
    msha = sha256_file(Path(wl_dir) / "manifest.json")
    if sess.get("workloads_manifest_sha256") not in (None, msha):
        raise SystemExit(f"{sess_p}: this session was run on other workloads (manifest sha256 differs)")
    sess.update(workloads_dir=str(Path(wl_dir).resolve()), workloads_manifest_sha256=msha,
                arms_file_sha256=sha256_bytes(json.dumps(arms_cfg, sort_keys=True).encode()), arms_cfg=arms_cfg)
    stop, done, refused, aborted, skipped, shut, interrupted = threading.Event(), {}, {}, {}, [], None, False
    try:
        for j, a in enumerate(arms):
            run, bad = {"arm": a, "utc_start": utc(), "url_host": httpx.URL(url).host, "settings": settings}, None
            try:
                s = run_arm(url, token, a, arms_cfg["arms"][a], wls, tok_prof, settings, sdir / a,
                            adapter_sha=adapter_sha, rate=rate, mults=mults, stop=stop,
                            need_s=(fit or {}).get(a), log=log)
                run.update(utc_end=utc(), ok=s["aborted"] is None, complete=s["complete"], gpu=s["gpu"],
                           region=s["region"], engine=s["engine"])
                if s["aborted"]:
                    aborted[a] = s["aborted"]
                    run["aborted"] = s["aborted"]
                else:
                    done[a] = s
            except ArmRefused as e:
                refused[a] = str(e)
                run.update(utc_end=utc(), ok=False, refused=str(e))
                log(f"REFUSED {e}")
            if a in aborted:  # a dead GPU / closed window stops the session; an arm's own failures do not
                bad = endpoint_problem(url, token, settings["timeout_s"])
                run["endpoint_after_abort"] = bad or "ok"
            sess["runs"].append(run)
            write_json(sess_p, sess)
            if a in aborted:
                if bad is None:
                    log(f"{a} aborted but the endpoint is still healthy: going on with the next arm")
                    continue
                skipped = list(arms[j + 1:])
                if skipped:
                    log(f"session stopped after the aborted arm {a} ({bad}): {skipped} not run (rerun them from a "
                        f"new boot)")
                break
    except KeyboardInterrupt:
        stop.set()
        interrupted = True
        log("interrupted: partial results kept" + ("" if shutdown_after else
                                                    "; the endpoint is NOT stopped by this client"))
    finally:
        if shutdown_after and (done or aborted or interrupted):
            shut = post_shutdown(url, token, log=log)
        elif shutdown_after:  # every arm was refused before timing: this boot may still serve other arms
            log("--shutdown-after: nothing was timed (every arm refused), so the endpoint is left up; its idle timer "
                "stops it, or POST /shutdown / Ctrl-C the launcher")
    return {"done": list(done), "refused": refused, "aborted": aborted, "skipped": skipped, "shutdown": shut,
            "session_dir": str(sdir)}


# ------------------------------------------------------------------ report

def _fmt(x, nd=1, pct_=False):
    if x is None:
        return "-"
    return f"{x:.{nd}%}" if pct_ else f"{x:,.{nd}f}"


def verdict(p):
    return "N/A" if p is None else ("PASS" if p else "FAIL")


def gate_verdict(par) -> str:
    """The gate of an arm vs the baseline. FAIL when a gated comparison fails on the rows both arms answered;
    INCOMPLETE when it would pass there but some P row has no answer from the arm or the baseline (an aborted arm,
    failed calls, a cut serving window): a missing answer is never a PASS, and is not reported as a parity failure.
    Sets P_vs_baseline["verdict"] (the report's P row)."""
    if "P_vs_baseline" not in par:
        return "N/A (no P answers)"
    pv, pa = par["P_vs_baseline"], par.get("P_vs_baseline_answered")
    r_fail = "R_vs_baseline" in par and not par["R_vs_baseline"]["pass"]
    if pa is None:  # every P row answered by both
        pv["verdict"] = verdict(pv["pass"])
        return verdict(pv["pass"] and not r_fail)
    p_fail = bool(pa.get("n")) and not pa["pass"]
    pv["verdict"] = "FAIL" if p_fail else "INCOMPLETE"
    if p_fail or r_fail:
        return "FAIL"
    return f"INCOMPLETE ({pa.get('n', 0)}/{pv['n']} P rows answered by both)"


def build_report(session_dir, arms_cfg=None, baseline=None, root=None, rate=RATE_USD_H, mults=None,
                 log=print) -> dict:
    session_dir = Path(session_dir)
    sess = json.loads((session_dir / "session.json").read_text())
    arms_cfg = arms_cfg or sess.get("arms_cfg") or load_arms()
    mults = mults or REGION_MULT
    baseline = baseline or arms_cfg.get("baseline", "A0")
    bars = {**BARS, **(arms_cfg.get("bars") or {})}
    wl_dir = Path(sess["workloads_dir"])
    man = json.loads((wl_dir / "manifest.json").read_text())
    if sha256_file(wl_dir / "manifest.json") != sess["workloads_manifest_sha256"]:
        raise SystemExit(f"{wl_dir}/manifest.json changed since this session ran")
    items = {W: load_workload(wl_dir, W, man) for W in WORKLOAD_NAMES}
    dev = {r["id"]: r for r in dev_rows(root, man["splits"])}
    rows_of = {W: [{**dev[it["id"]], "options": it["request"]["questions"]["q0"].get("options")} for it in items[W]]
               for W in WORKLOAD_NAMES}
    order = list(arms_cfg["arms"])
    arms = sorted([d.name for d in session_dir.iterdir() if d.is_dir() and d.name != JEV_DIR
                   and (d / "summary.json").exists()], key=lambda a: (order.index(a) if a in order else 99, a))
    summ = {a: json.loads((session_dir / a / "summary.json").read_text()) for a in arms}
    stored_s, stored_i = load_stored(STORED["served"], man["splits"]), load_stored(STORED["identity"], man["splits"])
    P_rows = rows_of["P"]
    stored_rev = reversed_from(stored_s, stored_i, P_rows)
    rep = {"session": sess["session"], "utc": utc(), "baseline": baseline, "bars": bars,
           "workloads_manifest_sha256": sess["workloads_manifest_sha256"],
           "workloads": {W: {k: man["workloads"][W][k] for k in ("calls", "sha256", "groups")} for W in WORKLOAD_NAMES},
           "R_tasks": man["workloads"]["R"].get("tasks"), "arms": {},
           "stored": {"served": STORED["served"], "identity": STORED["identity"], "rows_served": len(stored_s),
                      "rows_identity": len(stored_i), "reversed_view_consistency": view_consistency(stored_rev)}}
    base_ans = {W: read_answers(session_dir / baseline / f"answers_{W}.jsonl")[0] for W in ("P", "R")} \
        if baseline in summ else None
    for a in arms:
        acfg = arms_cfg["arms"].get(a, {})
        acc_bar = bars["acc_diff_max_pt_fp8"] if acfg.get("fp8") or summ[a].get("fp8") else bars["acc_diff_max_pt"]
        ansP, viewsP = read_answers(session_dir / a / "answers_P.jsonl")
        ansR, _ = read_answers(session_dir / a / "answers_R.jsonl")
        identP, _ = read_answers(session_dir / a / "answers_P_identity.jsonl")
        par = {"acc_bar_pt": acc_bar}
        if ansP:
            par["P_vs_stored_L4_context"] = compare(P_rows, ansP, stored_s, acc_bar, bars["argmax_agree_min"])
            par["reversed_view"] = reversed_view_check(P_rows, ansP, viewsP, identP, stored_s, stored_i, acc_bar)
        if base_ans is not None and a != baseline:
            if ansP or base_ans["P"]:
                pv = compare(P_rows, ansP, base_ans["P"], acc_bar, bars["argmax_agree_min"])
                par["P_vs_baseline"] = pv
                if pv["missing_cand"] or pv["missing_ref"]:  # also judged on the rows both arms answered
                    bp = [r for r in P_rows if r["id"] in ansP and r["id"] in base_ans["P"]]
                    par["P_vs_baseline_answered"] = compare(bp, ansP, base_ans["P"], acc_bar,
                                                            bars["argmax_agree_min"]) if bp else {"n": 0}
            both = [r for r in rows_of["R"] if r["id"] in ansR and r["id"] in base_ans["R"]]
            if both:  # R levels are time windows: each arm answers a prefix of R, so compare the rows both answered
                par["R_vs_baseline"] = compare(both, ansR, base_ans["R"], acc_bar, bars["argmax_agree_min"])
                par["R_vs_baseline"]["coverage"] = {"rows_both": len(both), "rows_workload": len(rows_of["R"]),
                                                    "rows_arm": len(ansR), "rows_baseline": len(base_ans["R"])}
            par["gate"] = gate_verdict(par)
        elif a == baseline:
            par["gate"] = "BASELINE" if len(ansP) >= len(P_rows) else \
                f"BASELINE (INCOMPLETE: {len(ansP)}/{len(P_rows)} P rows answered)"
        else:
            par["gate"] = "N/A (baseline arm not in this session)"
        S = summ[a]["workloads"].get("S", {}).get("levels", [])
        dph, at = sustained(S) if S else (None, None)
        rep["arms"][a] = {"engine": summ[a].get("engine"), "gpu": summ[a].get("gpu"), "region": summ[a].get("region"),
                          "aborted": summ[a].get("aborted"), "p_answered": len(ansP), "p_rows": len(P_rows),
                          "flags": summ[a].get("flags"), "fp8": summ[a].get("fp8"), "boot_s": summ[a].get("boot_s"),
                          "workloads": summ[a]["workloads"], "sustained_decisions_per_hour": dph,
                          "sustained_at_concurrency": at, "cost": cost_table(dph, rate, mults), "parity": par,
                          "token_check_P": (summ[a]["workloads"].get("P", {}).get("levels") or [{}])[0].get(
                              "token_check")}
    jdir = session_dir / JEV_DIR
    if (jdir / "summary.json").exists():
        js = json.loads((jdir / "summary.json").read_text())
        jans, _ = read_answers(jdir / "answers_S.jsonl")
        S_rows = rows_of["S"]
        jrep = {"summary": js, "vs_stored_L4": compare(S_rows, jans, stored_s)}
        if base_ans is not None:
            jrep["vs_baseline_P_answers_on_S_rows"] = compare(S_rows, jans, base_ans["P"])
        rep["jev"] = jrep
    write_json(session_dir / "report.json", rep)
    (session_dir / "REPORT.md").write_text(report_md(rep))
    log(f"wrote {session_dir / 'REPORT.md'} and report.json")
    return rep


def _lv(arm, W, c):
    for lv in arm["workloads"].get(W, {}).get("levels", []):
        if lv["concurrency"] == c:
            return lv
    return None


def report_md(rep) -> str:
    L = [f"# SPEED-2 report: session `{rep['session']}`", "",
         f"Generated {rep['utc']} by hosting/speed_bench.py. Dev rows only (gate dev splits). Workloads manifest "
         f"sha256 "
         f"`{rep['workloads_manifest_sha256'][:16]}`; calls P {rep['workloads']['P']['calls']}, S "
         f"{rep['workloads']['S']['calls']}, N {rep['workloads']['N']['calls']}, R {rep['workloads']['R']['calls']} "
         f"({rep.get('R_tasks')} tasks).",
         f"Parity bars: argmax agreement >= {rep['bars']['argmax_agree_min']:.1%}, |accuracy diff| <= "
         f"{rep['bars']['acc_diff_max_pt']} pt ({rep['bars']['acc_diff_max_pt_fp8']} pt for FP8 arms); gated against "
         f"the baseline arm **{rep['baseline']}** of this session; the stored L4 reads are context only.", "",
         "## Arms", "", "| arm | engine | GPU | region | boot s | flags |", "|---|---|---|---|---|---|"]
    for a, x in rep["arms"].items():
        L.append(f"| {a} | {x['engine']} | {x['gpu']} | {x['region']} | {x['boot_s']} | `{json.dumps(x['flags'])}` |")
    for a, x in rep["arms"].items():
        if x.get("aborted") or x.get("p_answered", 0) < x.get("p_rows", 0):
            L.append(f"\n- **{a} incomplete**: P answered {x.get('p_answered')}/{x.get('p_rows')} rows"
                     + (f"; aborted: {x['aborted']}" if x.get("aborted") else "") + ".")
    if len({x.get("region") for x in rep["arms"].values()}) > 1:
        L.append("\n- Arms ran in different regions: compare latency on server_ms (client and network ms include "
                 "each region's network path).")
    L += ["", "## Latency, S at concurrency 1 (ms, client = laptop round trip)", "",
          "| arm | client p50 | p95 | p99 | server p50 | server p95 | network p50 | failed |",
          "|---|---|---|---|---|---|---|---|"]
    for a, x in rep["arms"].items():
        lv = _lv(x, "S", 1)
        if lv:
            L.append(f"| {a} | {_fmt(lv['client_ms'].get('p50'))} | {_fmt(lv['client_ms'].get('p95'))} | "
                     f"{_fmt(lv['client_ms'].get('p99'))} | {_fmt(lv['server_ms'].get('p50'))} | "
                     f"{_fmt(lv['server_ms'].get('p95'))} | {_fmt(lv['network_ms'].get('p50'))} | "
                     f"{lv['failed_calls']} |")
    if "jev" in rep:
        j = rep["jev"]["summary"]["client_ms"]
        L.append(f"| Jev (OpenRouter) | {_fmt(j.get('p50'))} | {_fmt(j.get('p95'))} | {_fmt(j.get('p99'))} | - | - | "
                 f"- | {rep['jev']['summary']['errors']} |")
    levels = sorted({lv["concurrency"] for x in rep["arms"].values() for lv in x["workloads"].get("S", {})
                     .get("levels", [])})
    L += ["", "## Throughput, S closed loop (decisions/hour; failed calls in brackets)", "",
          "| arm | " + " | ".join(f"c={c}" for c in levels) + " | sustained | at c |",
          "|---|" + "---|" * (len(levels) + 2)]
    for a, x in rep["arms"].items():
        cells = []
        for c in levels:
            lv = _lv(x, "S", c)
            cells.append("-" if not lv else f"{lv['decisions_per_hour']:,.0f}" + (f" [{lv['failed_calls']}]"
                                                                                  if lv["failed_calls"] else ""))
        L.append(f"| {a} | " + " | ".join(cells) + f" | {_fmt(x['sustained_decisions_per_hour'], 0)} | "
                 f"{x['sustained_at_concurrency'] or '-'} |")
    regs = list(next(iter(rep["arms"].values()))["cost"]["usd_per_1k"]) if rep["arms"] else []
    utils = list(next(iter(rep["arms"].values()))["cost"]["usd_per_1k"][regs[0]]) if regs else []
    if regs:
        c0 = next(iter(rep["arms"].values()))["cost"]
        L += ["", f"## Cost, $ per 1,000 decisions (rate ${c0['rate_usd_h_base']}/h x region multiplier "
                  f"{json.dumps(c0['region_mult'])}, multipliers to be confirmed; / utilisation)", "",
              "| arm | " + " | ".join(f"{r} @ {u}" for r in regs for u in utils) + " |",
              "|---|" + "---|" * (len(regs) * len(utils))]
        for a, x in rep["arms"].items():
            L.append(f"| {a} | " + " | ".join(_fmt(x["cost"]["usd_per_1k"][r][u], 4) for r in regs for u in utils)
                     + " |")
    L += ["", "## Other workloads", "",
          "| arm | P pass c=16 decisions/h | P pass s | N c=1 p50 / p99 ms | R c=1 p50 ms | R c=8 decisions/h | "
          "R c=8 cached-token share | batch rows mean (S c=16) |", "|---|---|---|---|---|---|---|---|"]
    for a, x in rep["arms"].items():
        p, n1, r1, r8, s16 = _lv(x, "P", 16), _lv(x, "N", 1), _lv(x, "R", 1), _lv(x, "R", 8), _lv(x, "S", 16)
        L.append(f"| {a} | {_fmt(p and p['decisions_per_hour'], 0)} | {_fmt(p and p['window_s'])} | "
                 f"{_fmt(n1 and n1['client_ms'].get('p50'))} / {_fmt(n1 and n1['client_ms'].get('p99'))} | "
                 f"{_fmt(r1 and r1['client_ms'].get('p50'))} | {_fmt(r8 and r8['decisions_per_hour'], 0)} | "
                 f"{_fmt(r8 and r8['cached_token_share'], 1, True)} | "
                 f"{_fmt(s16 and s16['batch_rows']['mean'], 2)} |")
    L += ["", f"## Parity, gated vs {rep['baseline']} (same session)", "",
          "| arm | set | rows | argmax agree | acc arm | acc base | diff pt | bar pt | mean / p99 / max abs dp "
          "| result |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for a, x in rep["arms"].items():
        par = x["parity"]
        for k, setn in (("P_vs_baseline", "P"), ("R_vs_baseline", "R (rows both answered)")):
            if k in par:
                c = par[k]
                L.append(f"| {a} | {setn} | {c['n']} | {_fmt(c.get('argmax_agree'), 2, True)} | "
                         f"{_fmt(c.get('acc_cand'), 2)} | {_fmt(c.get('acc_ref'), 2)} | "
                         f"{_fmt(c.get('acc_diff_pt'), 2)} | {par['acc_bar_pt']} | "
                         f"{_fmt(c.get('dp_mean'), 4)} / {_fmt(c.get('dp_p99'), 4)} / {_fmt(c.get('dp_max'), 4)} | "
                         f"{c.get('verdict') or verdict(c['pass'])} |")
        L.append(f"| {a} | **gate** | | | | | | | | **{par['gate']}** |")
    L += ["", "### By type and options bucket (P vs baseline: argmax agree / diff pt / max abs dp)", ""]
    for a, x in rep["arms"].items():
        c = x["parity"].get("P_vs_baseline")
        if c:
            L.append(f"- {a}: " + "; ".join(f"{g} n={b['n']} {_fmt(b['argmax_agree'], 2, True)} / "
                                            f"{_fmt(b['acc_diff_pt'], 2)} / {_fmt(b['dp_max'], 4)}"
                                            for g, b in c["by_group"].items()))
    L += ["", "## Parity vs the stored L4 reads (context, not gated; 2view served read)", "",
          "| arm | rows | argmax agree | acc arm | acc L4 | diff pt | mean / p99 / max abs dp | bars |",
          "|---|---|---|---|---|---|---|---|"]
    for a, x in rep["arms"].items():
        c = x["parity"].get("P_vs_stored_L4_context")
        if c:
            L.append(f"| {a} | {c['n']} | {_fmt(c.get('argmax_agree'), 2, True)} | {_fmt(c.get('acc_cand'), 2)} | "
                     f"{_fmt(c.get('acc_ref'), 2)} | {_fmt(c.get('acc_diff_pt'), 2)} | {_fmt(c.get('dp_mean'), 4)} / "
                     f"{_fmt(c.get('dp_p99'), 4)} / {_fmt(c.get('dp_max'), 4)} | {verdict(c['pass'])} |")
    sc = rep["stored"]["reversed_view_consistency"]
    L += ["", "## Reversed-view check", "",
          f"Stored L4 reads: reversed view = 2 x served - identity on {sc['rows']} choice rows; invalid rows "
          f"{sc['invalid_rows']}, max violation {sc['max_violation']} -> {verdict(sc['pass'])}.", ""]
    for a, x in rep["arms"].items():
        rv = x["parity"].get("reversed_view")
        if not rv:
            continue
        if not rv["available"]:
            L.append(f"- {a}: not available ({rv['why']}).")
        else:
            L.append(f"- {a} ({rv['source']}, {rv['rows']} rows): identity view vs L4 identity agree "
                     f"{_fmt(rv['identity']['argmax_agree'], 2, True)}, max dp {_fmt(rv['identity']['dp_max'], 4)}; "
                     f"reversed view vs L4 reversed agree {_fmt(rv['reversed']['argmax_agree'], 2, True)}, max dp "
                     f"{_fmt(rv['reversed']['dp_max'], 4)}; reconstruction valid "
                     f"{verdict(rv['cand_reversed_consistency']['pass'])}.")
    L += ["", "## Token check (server identity-view tokens == local C1 count, P)", ""]
    for a, x in rep["arms"].items():
        t = x.get("token_check_P")
        L.append(f"- {a}: " + ("no local token profile" if not t else
                               f"{t['equal']}/{t['checked']} equal, server missing {t['server_missing']}, max abs diff "
                               f"{t['max_abs_diff']}"))
    if "jev" in rep:
        j = rep["jev"]
        v = j["vs_stored_L4"]
        L += ["", "## Jev (report-only, dev S rows, concurrency 1; never used for training)", "",
              f"Route {j['summary']['route']}, model {j['summary']['model']}; {j['summary']['calls']} calls, "
              f"{j['summary']['errors']} errors, yes/no cards dropped {j['summary']['cards_dropped']}.",
              f"Accuracy on S: Jev {_fmt(v.get('acc_cand'), 2)} vs stored C1 L4 {_fmt(v.get('acc_ref'), 2)} "
              f"(argmax agreement with C1 {_fmt(v.get('argmax_agree'), 2, True)})."]
        if "vs_baseline_P_answers_on_S_rows" in j:
            b = j["vs_baseline_P_answers_on_S_rows"]
            L.append(f"Same rows, {rep['baseline']} answers: accuracy {_fmt(b.get('acc_ref'), 2)}.")
    L += ["", "## Notes", "",
          "- Latency is from this client's network position; server_ms excludes the network.",
          "- Sustained = best S level with 0 failed calls; no call repeats inside a level; caches flushed between "
          "levels.",
          "- A missing answer counts as a disagreement and as wrong; percentiles are nearest rank. A gate with P rows "
          "unanswered by the arm or the baseline reads INCOMPLETE (FAIL if the rows both answered fail a bar).",
          "- Region multipliers are CLI inputs to be confirmed against Modal's billing page.", ""]
    return "\n".join(L)


# ------------------------------------------------------------------ CLI

def parse_mults(s) -> dict:
    out = {}
    for part in (s or "").split(","):
        if part.strip():
            k, v = part.split("=", 1)
            out[k.strip()] = float(v)
    return out or dict(REGION_MULT)


def read_token(path) -> str:
    t = Path(path).read_text().strip()
    if not t:
        raise SystemExit(f"{path} is empty")
    return t


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("workloads", help="build P/S/N/R + manifest + token profile")
    w.add_argument("--out", default=str(WORKLOADS))
    w.add_argument("--no-tokens", action="store_true", help="skip the token-length profile (no tokenizer load)")
    w.add_argument("--adapter-dir", default=str(ADAPTER_DIR))
    w.add_argument("--check", action="store_true", help="rebuild in memory and compare sha256 with the manifest")
    for name in ("ab", "jev", "report", "cost"):
        p = sub.add_parser(name)
        p.add_argument("--rate", type=float, default=RATE_USD_H, help="$/h base GPU rate (Modal H100 list: 3.95)")
        p.add_argument("--region-mult", default=",".join(f"{k}={v}" for k, v in REGION_MULT.items()),
                       help="region multipliers, e.g. any=1.0,us-east=1.75 (TO BE CONFIRMED)")
        if name != "cost":
            p.add_argument("--session", required=True)
            p.add_argument("--out-root", default=str(SPEED))
            p.add_argument("--workloads", default=str(WORKLOADS))
            p.add_argument("--arms-file", default=str(ARMS_FILE))
    ab = sub.choices["ab"]
    ab.add_argument("--url")
    ab.add_argument("--token-file")
    ab.add_argument("--arms", default=DEFAULT_ARMS, help="run in this order (default: the main arm A2 before A1)")
    ab.add_argument("--shutdown-after", action="store_true",
                    help="POST /shutdown when this command ends (all arms, an abort, or Ctrl-C): no idle GPU tail")
    ab.add_argument("--fit-gpu-ms", type=float, default=FIT_GPU_MS,
                    help="GPU ms per call assumed when checking that an arm fits the endpoint's serve_remaining_s "
                         "(conservative; 0 = no fit check)")
    ab.add_argument("--go", action="store_true", help="really send traffic (default: plan only)")
    ab.add_argument("--dry-run", action="store_true", help="plan only (the default without --go)")
    ab.add_argument("--overwrite", action="store_true")
    ab.add_argument("--warmup-s", type=float, default=SETTINGS["warmup_s"])
    ab.add_argument("--window-s", type=float, default=SETTINGS["window_s"])
    ab.add_argument("--timeout-s", type=float, default=SETTINGS["timeout_s"])
    ab.add_argument("--est-net-ms", type=float, default=EST["net_ms"])
    ab.add_argument("--est-gpu-ms", type=float, default=EST["gpu_ms"])
    jv = sub.choices["jev"]
    jv.add_argument("--go", action="store_true")
    jv.add_argument("--max-calls", type=int, default=0, help="cap the timed calls (0 = all of S)")
    jv.add_argument("--warm", type=int, default=3)
    jv.add_argument("--noul-card", choices=("drop", "instructions"), default="drop")
    jv.add_argument("--overwrite", action="store_true")
    rp = sub.choices["report"]
    rp.add_argument("--baseline", default=None)
    cs = sub.choices["cost"]
    cs.add_argument("--dph", type=float, required=True, help="sustained decisions per hour")
    a = ap.parse_args(argv)
    if a.cmd == "workloads":
        if a.check:
            res = check_workloads(a.out)
            for n, r in res.items():
                print(f"{n}: manifest {r['manifest'][:16]} rebuilt {r['rebuilt'][:16]} on disk {r['on_disk'][:16]} "
                      f"{'OK' if r['manifest'] == r['rebuilt'] == r['on_disk'] else 'DIFFERS'}")
            return res
        out = write_workloads(a.out)
        man = out["manifest"]
        for n, x in man["workloads"].items():
            print(f"{n}: {x['calls']} calls, {x['unique_rows']} rows, groups {x['groups']}, sha256 {x['sha256'][:16]}")
        print(f"R: {man['workloads']['R']['tasks']} tasks ({man['workloads']['R']['task_types']}), "
              f"{man['workloads']['R']['calls']} rows, {man['workloads']['R']['reordered_rows']} reordered")
        if not a.no_tokens:
            count, prompt, info = c1_counter(a.adapter_dir)
            prof = token_profile(out["workloads"], count, prompt)
            info["workloads_sha256"] = {W: man["workloads"][W]["sha256"] for W in WORKLOAD_NAMES}
            write_json(Path(a.out) / "token_profile.json", {"info": info, **prof})
            print_profile(prof, info)
        print(f"wrote {a.out}")
        return man
    mults = parse_mults(a.region_mult)
    if a.cmd == "cost":
        t = cost_table(a.dph, a.rate, mults)
        print(json.dumps(t, indent=1))
        return t
    arms_cfg = load_arms(a.arms_file)
    sdir = Path(a.out_root) / a.session
    if a.cmd == "ab":
        go = a.go and not a.dry_run
        if go and not (a.url and a.token_file):
            ap.error("--url and --token-file are required with --go")
        token = read_token(a.token_file) if go else None
        est = {**EST, "net_ms": a.est_net_ms, "gpu_ms": a.est_gpu_ms}
        return run_ab(a.url, token, a.session, [x.strip() for x in a.arms.split(",") if x.strip()], arms_cfg,
                      a.workloads, a.out_root, {"warmup_s": a.warmup_s, "window_s": a.window_s,
                                                "timeout_s": a.timeout_s}, go, a.overwrite, a.rate, mults, est,
                      shutdown_after=a.shutdown_after, fit_gpu_ms=a.fit_gpu_ms)
    if a.cmd == "jev":
        man = json.loads((Path(a.workloads) / "manifest.json").read_text())
        items = load_workload(a.workloads, "S", man)
        return run_jev(sdir, items, a.go, a.max_calls or None, a.warm, noul_card=a.noul_card, overwrite=a.overwrite)
    if a.cmd == "report":
        return build_report(sdir, arms_cfg, a.baseline, rate=a.rate, mults=mults)


if __name__ == "__main__":
    main()
