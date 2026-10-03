"""Decision Index helpers for the A13 report-only run (counts and aggregates only; never prints item text or gold).

  P=bench/external_quarantine/decision_index/venv/bin/python      # harness + rebuild deps (no torch)
  Q=bench/external_quarantine/decision_index                      # quarantine: suite, samples, per-item results
  $P bench/decision_index/di_tools.py sample   --n 10000            # harness sampler -> $Q/sample/ + sample_manifest.json
  $P bench/decision_index/di_tools.py sample   --n 50 --name smoke50
  opendecide-data/.venv/bin/python bench/decision_index/di_tools.py preflight --name sample10k   # token counts (tokenizer)
  $P bench/decision_index/di_tools.py check-index-math              # harness index math on Jev's published v0.1 values
  $P bench/decision_index/di_tools.py check-parity                  # harness scorer + rebuilt suite vs a published run
  $P bench/decision_index/di_tools.py score --name sample10k --run $Q/runs/c1_sample10k   # harness score + report vs Jev

Item text, gold and per-item results live only under the quarantine dir (.gitignore '*'). This file and the reports in
bench/decision_index/ hold counts, hashes and aggregate scores only.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import math
import os
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
JEV = HERE.parents[1]
Q = JEV / "bench/external_quarantine/decision_index"
REPO = Q / "repo"
SUITE = Q / "work/artifacts/benchmark-suite/release-v1-rebuilt"  # rebuilt frozen suite (selected-rows.jsonl.gz)
SPACE = Q / "space/data/index-v0.1.json"  # published board for this harness's panel (core25-observed-protocol-v1)
PROGRESS = HERE / "progress.log"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
    print(line, flush=True)
    with open(PROGRESS, "a") as f:
        f.write(line + "\n")


def sha256_file(path, gunzip=False):
    with (gzip.open if gunzip else open)(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def read_jsonl(path):
    from decision_index.suite.io import read_jsonl as r
    return r(path)


def suite_dir_for(name):
    return Q / "sample" / f"suite_{name}"


def ensure_suite_files(d: Path):
    """The rebuilt suite dir needs the harness's exclusions (hub/excluded-questions.json, pinned sha256)."""
    from decision_index import constants as C
    ex = d / C.SUITE_EXCLUSIONS_FILE
    if not ex.exists():
        shutil.copyfile(REPO / "hub/excluded-questions.json", ex)
    if sha256_file(ex) != C.SUITE_EXCLUSIONS_SHA256:
        raise SystemExit("excluded-questions.json does not match the harness's pinned sha256")


# ------------------------------------------------------------------ sample

def cmd_sample(a):
    from decision_index import constants as C
    from decision_index.suite.io import Suite
    ensure_suite_files(SUITE)
    out_dir = Q / "sample"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{a.name}.jsonl.gz"
    log(f"sample {a.name}: harness sampler n={a.n} seed={a.seed} over {SUITE}")
    # the harness's own CLI (decision_index suite sample), same process tree, nothing re-implemented
    r = subprocess.run([sys.executable, "-m", "decision_index", "suite", "sample", "--dir", str(SUITE), "--n", str(a.n),
                        "--seed", str(a.seed), "--out", str(out)], capture_output=True, text=True, cwd=str(REPO),
                       env={**os.environ, "PYTHONPATH": str(REPO)})
    if r.returncode != 0:
        raise SystemExit(r.stderr[-2000:])
    res = json.loads(r.stdout)
    # a suite dir holding only the sample: the harness scores the sample against itself (denominator = the sample)
    sd = suite_dir_for(a.name)
    sd.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(out, sd / C.SUITE_ROWS_FILE)
    ensure_suite_files(sd)
    suite = Suite(SUITE)
    full = collections.Counter(r["_evaluation"]["catalog_id"] for r in suite.rows(apply_exclusions=True))
    names, per, groups, fields = {}, collections.Counter(), collections.defaultdict(set), collections.Counter()
    kinds = collections.Counter()
    from od_engine import build_row, state_text
    from decision_index.engines import Unsupported
    for row in read_jsonl(out):
        e = row["_evaluation"]
        n = e["catalog_id"]
        names[n] = e["dataset"]
        per[n] += 1
        groups[n].add(e["group_id"])
        fields[n] += len(row["questions"])
        st = state_text(row["state"])
        for k, q in row["questions"].items():
            try:
                _, info = build_row(st, q, k)
                kinds[(n, info["kind"], info["mode"])] += 1
            except Unsupported:
                kinds[(n, "unsupported_type", "-")] += 1
    from decision_index.scoring.index import panel_ids
    pids = panel_ids()
    bench = []
    for n in sorted(per):
        km = collections.Counter({f"{k}/{m}": c for (b, k, m), c in kinds.items() if b == n})
        bench.append({"catalog_id": n, "dataset": names[n], "in_index": n in pids, "requests": per[n],
                      "groups": len(groups[n]), "questions": fields[n], "full_suite_requests": full[n],
                      "share_of_benchmark": round(per[n] / full[n], 4), "mapping": dict(km)})
    missing = sorted(set(full) ^ set(per))
    tot_k = collections.Counter()
    for (b, k, m), c in kinds.items():
        tot_k[f"{k}/{m}"] += c
    man = {
        "name": a.name, "harness_repo": "github.com/flaviusburca/decision-index", "harness_commit": git_head(REPO),
        "command": f"python -m decision_index suite sample --dir <rebuilt suite> --n {a.n} --seed {a.seed} --out {out.name}",
        "seed": a.seed, "n_requested": a.n, "sampler_result": {k: v for k, v in res.items() if k != "path"},
        "complete_groups": True, "exclusions_applied": True,
        "sample_sha256_gz": sha256_file(out), "sample_sha256": sha256_file(out, gunzip=True),
        "suite_rows_sha256": sha256_file(SUITE / "selected-rows.jsonl"),
        "suite_rows_sha256_pinned_full": C.SUITE_ROWS_SHA256,
        "requests": sum(per.values()), "groups": sum(len(g) for g in groups.values()), "questions": sum(fields.values()),
        "benchmarks_in_sample": len(per), "benchmarks_in_index_in_sample": sum(1 for n in per if n in pids),
        "missing_vs_rebuilt_suite": missing, "question_mapping_totals": dict(tot_k),
        "benchmarks": bench, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (HERE / f"sample_manifest_{a.name}.json").write_text(json.dumps(man, indent=2) + "\n")
    log(f"sample {a.name}: {man['requests']} requests, {man['questions']} questions, {len(per)} benchmarks, "
        f"sha256 {man['sample_sha256'][:16]} (gz {man['sample_sha256_gz'][:16]}) -> sample_manifest_{a.name}.json")


def git_head(path):
    try:
        return subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        return None


# ------------------------------------------------------------------ preflight (token counts, real tokenizer)

def cmd_preflight(a):
    """Builds every prompt the engine will read (both views on choice), with the real tokenizer; counts only."""
    sys.path.insert(0, str(a.lean))
    import decoder_io as dio
    from transformers import AutoTokenizer
    from decision_index.engines import Unsupported
    from od_engine import build_row, state_text
    info = dio.resolve_prompt([str(a.adapter)], "Qwen/Qwen3.5-4B", None, None, None)
    dio.LAYOUT, dio.STYLE = info["layout"], info["style"]
    tok = AutoTokenizer.from_pretrained(str(a.adapter))
    ro = dio.Readout(tok)
    path = Q / "sample" / f"{a.name}.jsonl.gz"
    rows = list(read_jsonl(path))
    log(f"preflight {a.name}: {len(rows)} requests, layout {dio.LAYOUT} style {dio.STYLE}")
    per = collections.defaultdict(lambda: {"requests": 0, "questions": 0, "reads": 0, "tokens": [], "req_tokens": [],
                                           "over_limit_requests": 0, "unsupported_type": 0, "max_options": 0})
    names = {}
    t0 = time.time()
    for i, row in enumerate(rows):
        e = row["_evaluation"]
        n = e["catalog_id"]
        names[n] = e["dataset"]
        s = per[n]
        s["requests"] += 1
        st = state_text(row["state"])
        over, rt = False, 0
        for k, q in row["questions"].items():
            s["questions"] += 1
            try:
                r, inf = build_row(st, q, k)
            except Unsupported:
                s["unsupported_type"] += 1
                continue
            t1 = len(tok(ro.prompt(r), add_special_tokens=False)["input_ids"])
            reads = 1
            t2 = 0
            if r["qtype"] == "choice":
                s["max_options"] = max(s["max_options"], len(r["options"]))
                t2 = len(tok(ro.prompt(r, list(range(len(r["options"])))[::-1]), add_special_tokens=False)["input_ids"])
                reads = 2
                if len(ro.cand(r)) != len(r["options"]):
                    raise SystemExit(f"catalog {n}: candidate groups != options")
            s["reads"] += reads
            s["tokens"].append(max(t1, t2))
            rt += t1 + t2
            over |= max(t1, t2) > dio.MAX_LEN
        s["req_tokens"].append(rt)
        s["over_limit_requests"] += over
        if (i + 1) % 500 == 0:
            log(f"preflight {a.name}: {i + 1}/{len(rows)} requests ({time.time() - t0:.0f}s)")

    def pct(x, p):
        x = sorted(x)
        return x[min(len(x) - 1, max(0, math.ceil(len(x) * p) - 1))] if x else None
    out = []
    for n in sorted(per):
        s = per[n]
        tk = s["tokens"]
        out.append({"catalog_id": n, "dataset": names[n], "requests": s["requests"], "questions": s["questions"],
                    "reads": s["reads"], "tokens_per_question_mean": round(statistics.mean(tk), 1) if tk else None,
                    "tokens_p50": pct(tk, .5), "tokens_p95": pct(tk, .95), "tokens_max": max(tk) if tk else None,
                    "read_tokens_total": sum(s["req_tokens"]), "max_options": s["max_options"],
                    "over_limit_requests": s["over_limit_requests"], "unsupported_type": s["unsupported_type"]})
    tot = {k: sum(b[k] for b in out) for k in ("requests", "questions", "reads", "read_tokens_total",
                                                "over_limit_requests", "unsupported_type")}
    res = {"name": a.name, "context_limit": dio.MAX_LEN, "layout": dio.LAYOUT, "style": dio.STYLE, "totals": tot,
           "benchmarks": out, "decoder_io_sha256": sha256_file(dio.__file__)}
    (HERE / f"preflight_{a.name}.json").write_text(json.dumps(res, indent=2) + "\n")
    log(f"preflight {a.name}: {tot} -> preflight_{a.name}.json")


# ------------------------------------------------------------------ sanity checks

def jev_v01():
    d = json.loads(SPACE.read_text())
    if d["suite"]["panel_id"] != "core25-observed-protocol-v1":
        raise SystemExit("index-v0.1.json is not this harness's panel")
    return d


def cmd_check_index_math(a):
    """Feeds Jev's published v0.1 per-benchmark values into the harness's own index code (recompute) and compares the
    areas and the three index numbers with the published ones. Also re-derives every panel benchmark's skill."""
    from decision_index.scoring import index as I
    d = jev_v01()
    j = d["jev"]
    scored = {}
    for k, b in j["benchmarks"].items():
        n = int(k)
        scored[n] = {"catalog_id": n, "raw": b["raw"], "skill": b["skill"], "coverage": b.get("coverage", 1),
                     "pending": b.get("pending", 0), "tracks": []}
    from decision_index import constants as C
    for n in C.INTERACTIVE:
        scored.setdefault(n, I.interactive_placeholder(n))
    scores, cats = I.recompute(scored)
    rows = []
    for c in cats:
        pub = next(x for x in j["categories"] if x["id"] == c["id"])
        rows.append({"area": c["id"], "raw": round(c["raw"], 4), "raw_pub": pub["raw"], "skill": round(c["skill"], 4),
                     "skill_pub": pub["skill"], "n": c["n"], "n_pub": pub["n"]})
    res = {"jev_published": j["scores"], "harness_recomputed": {k: round(v, 2) for k, v in scores.items()},
           "match_2dp": all(abs(round(scores[k], 2) - j["scores"][k]) <= 0.011 for k in j["scores"]),
           "areas": rows, "area_max_abs_diff": max(abs(r["raw"] - r["raw_pub"]) for r in rows),
           "jev_index_benchmarks": len(j["benchmarks"]), "panel_ids_harness": sorted(I.panel_ids())}
    (HERE / "check_index_math.json").write_text(json.dumps(res, indent=2) + "\n")
    log(f"check-index-math: Jev published {j['scores']} vs harness {res['harness_recomputed']} match={res['match_2dp']}")
    print(json.dumps(res, indent=2))


def cmd_check_parity(a):
    """Scores a PUBLISHED full v0.1 run (another entrant's results.jsonl.gz, Hub dataset) with this harness on our rebuilt
    suite and compares every benchmark with the scores.json published next to it: checks the rebuild + scorer end to end.
    HLE (45, gated) is absent from our rebuild, so it is pending here (display-only, not in the index)."""
    from decision_index.pipeline import score_run
    from decision_index.suite.io import Suite
    pub = Q / "published"
    pub.mkdir(exist_ok=True)
    base = "https://huggingface.co/datasets/Kshetrajna/decision-index-results/resolve/main/runs/reflex-27b-p2-full-r8-p32"
    for f in ("results.jsonl.gz", "scores.json"):
        if not (pub / f"parity_{f}").exists():
            log(f"check-parity: downloading {f}")
            subprocess.run(["curl", "-sfL", "-o", str(pub / f"parity_{f}"), f"{base}/{f}"], check=True)
    ensure_suite_files(SUITE)
    out = pub / "parity_rescored"
    log("check-parity: scoring the published run with the harness on the rebuilt suite")
    mine = score_run(Suite(SUITE), pub / "parity_results.jsonl.gz", "parity", out)
    theirs = json.loads((pub / "parity_scores.json").read_text())
    diffs = []
    for k, b in theirs["benchmarks"].items():
        m = mine["benchmarks"].get(k)
        if m is None:
            diffs.append({"catalog_id": int(k), "dataset": b.get("dataset"), "published": b.get("score"), "rescored": None})
            continue
        diffs.append({"catalog_id": int(k), "dataset": b.get("dataset"), "published": b.get("score"),
                      "rescored": m.get("score"), "abs_diff": None if b.get("score") is None or m.get("score") is None
                      else round(abs(b["score"] - m["score"]), 6), "requests_pub": b.get("requests"),
                      "requests_rescored": m.get("requests")})
    ib = []
    for k, b in theirs["index_benchmarks"].items():
        m = mine["index_benchmarks"].get(k, {})
        ib.append({"catalog_id": int(k), "raw_pub": b["raw"], "raw_rescored": m.get("raw"),
                   "abs_diff": None if m.get("raw") is None else round(abs(b["raw"] - m["raw"]), 6)})
    res = {"published_run": "Kshetrajna/decision-index-results runs/reflex-27b-p2-full-r8-p32 (complete v0.1 run)",
           "published_index": theirs["scores"], "rescored_index": mine["scores"],
           "index_benchmarks_max_abs_diff": max(x["abs_diff"] for x in ib if x["abs_diff"] is not None),
           "index_benchmarks": ib,
           "benchmarks_exact": sum(1 for x in diffs if x.get("abs_diff") == 0),
           "benchmarks_compared": sum(1 for x in diffs if x.get("abs_diff") is not None), "benchmarks": diffs,
           "results_sha256_gz": sha256_file(pub / "parity_results.jsonl.gz")}
    (HERE / "check_parity.json").write_text(json.dumps(res, indent=2) + "\n")
    log(f"check-parity: published {theirs['scores']} rescored {mine['scores']}; index benchmarks max diff "
        f"{res['index_benchmarks_max_abs_diff']}; per-benchmark exact {res['benchmarks_exact']}/{res['benchmarks_compared']}")


# ------------------------------------------------------------------ score + report vs Jev

def cmd_score(a):
    from decision_index.pipeline import score_run
    from decision_index.suite.io import Suite
    run = Path(a.run).resolve()
    sd = suite_dir_for(a.name)
    out = Path(a.out).resolve() if a.out else run / "scored"
    s = score_run(Suite(sd), run / "results.jsonl", a.engine, out)
    man = json.loads((HERE / f"sample_manifest_{a.name}.json").read_text())
    d = jev_v01()
    j = d["jev"]
    others = sorted(((m["name"], m["scores"]["balanced_raw"]) for m in d["models"]), key=lambda x: -x[1])
    rows = []
    for k, b in s["index_benchmarks"].items():
        jb = j["benchmarks"].get(k, {})
        mb = next((x for x in man["benchmarks"] if str(x["catalog_id"]) == k), {})
        rows.append({"catalog_id": int(k), "dataset": s["benchmarks"].get(k, {}).get("dataset"),
                     "ours_raw": b["raw"], "jev_raw": jb.get("raw"), "diff_pp": None if jb.get("raw") is None
                     else round(100 * (b["raw"] - jb["raw"]), 2), "ours_coverage": b["coverage"],
                     "sample_requests": mb.get("requests"), "full_requests": mb.get("full_suite_requests")})
    disp = []
    for k, b in s["benchmarks"].items():
        jr = j["results"].get(k, {})
        disp.append({"catalog_id": int(k), "dataset": b.get("dataset"), "metric": b.get("metric"), "ours": b.get("score"),
                     "jev": jr.get("score"), "in_index": b.get("in_index"), "requests": b.get("requests"),
                     "answered": b.get("answered"), "unsupported": b.get("unsupported"), "errors": b.get("errors"),
                     "median_ms": b.get("median_ms")})
    areas = []
    for c in s["areas"]:
        jc = next(x for x in j["categories"] if x["id"] == c["id"])
        areas.append({"area": c["id"], "ours_raw": c["raw"], "jev_raw": jc["raw"],
                      "diff_pp": round(100 * (c["raw"] - jc["raw"]), 2), "ours_coverage": c["coverage"]})
    rep = {"name": a.name, "engine": a.engine, "report_only": "PREREG_FINAL A13: never used to choose data, families, "
           "weights or models", "sample": {k: man[k] for k in ("seed", "sample_sha256", "requests", "questions")},
           "ours": {"index": s["decision_index"], "scores": s["scores"], "counts": s["counts"]},
           "jev_published_v01_full_suite": {"index": j["scores"]["balanced_raw"], "scores": j["scores"]},
           "board_v01_top5": others[:5], "areas": areas, "index_benchmarks": sorted(rows, key=lambda r: r["catalog_id"]),
           "all_benchmarks": sorted(disp, key=lambda r: r["catalog_id"]),
           "caveat": "ours = the ~10K stratified SAMPLE scored by the harness against the sample; Jev = its published "
                     "full-suite v0.1 numbers (not paired items). Retrieval nDCG, RouterBench and macro metrics on a "
                     "sample are noisier than accuracy."}
    (HERE / f"report_{a.name}.json").write_text(json.dumps(rep, indent=2) + "\n")
    log(f"score {a.name}: index {s['decision_index']} (Jev v0.1 published {j['scores']['balanced_raw']}); "
        f"counts {s['counts']} -> report_{a.name}.json")


# ------------------------------------------------------------------ overlap (A13 disclosure, counts only)

def cmd_overlap(a):
    """Counts-only 12-gram overlap between the sample's items and C1's training file (state + instructions + card +
    options of every training row), as the OHS-3 overlap check. Words = lowercase [a-z0-9]+ runs (decontam.py rule);
    12-grams hashed (polynomial mod 2^64, collision chance negligible). Boilerplate rule: a 12-gram found in more than
    --boiler sample requests is template text, not an item, and is ignored. Reports per benchmark how many sample
    requests share >= 1 12-gram with training rows, and which training sources they come from. No text is printed."""
    import numpy as np
    import re
    from numpy.lib.stride_tricks import sliding_window_view
    W = re.compile(r"[a-z0-9]+")
    MASK = (1 << 64) - 1
    rng = np.random.default_rng(12345)
    POW = rng.integers(1, 2 ** 63, size=a.n, dtype=np.uint64) | np.uint64(1)

    def grams(text):
        ws = W.findall(text.lower())
        if len(ws) < a.n:
            return np.empty(0, dtype=np.uint64)
        ids = np.fromiter((hash(w) & MASK for w in ws), dtype=np.uint64, count=len(ws))
        with np.errstate(over="ignore"):
            return np.unique((sliding_window_view(ids, a.n) * POW).sum(axis=1, dtype=np.uint64))

    def item_text(row):
        parts = [row["state"] if isinstance(row["state"], str) else json.dumps(row["state"], ensure_ascii=False)]
        for q in row["questions"].values():
            parts.append(q["instructions"] if isinstance(q.get("instructions"), str) else json.dumps(q.get("instructions")))
            for k, d in q["criteria"].items():
                parts.append(f"{k} {d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)}")
        return "\n".join(parts)

    rows = list(read_jsonl(Q / "sample" / f"{a.name}.jsonl.gz"))
    log(f"overlap {a.name}: hashing {len(rows)} sample requests ({a.n}-grams)")
    per_req = [grams(item_text(r)) for r in rows]
    allg = np.concatenate(per_req) if per_req else np.empty(0, dtype=np.uint64)
    uniq, cnt = np.unique(allg, return_counts=True)
    S = uniq[cnt <= a.boiler]
    log(f"overlap {a.name}: {len(uniq)} distinct grams, {int((cnt > a.boiler).sum())} boilerplate dropped")
    train = Path(a.train)
    hit_src = collections.Counter()
    gram_src = collections.defaultdict(set)
    t0 = time.time()
    n = 0
    with open(train) as f:
        for line in f:
            r = json.loads(line)
            n += 1
            g = grams("\n".join([r.get("state") or "", r.get("instructions") or "", r.get("card") or "",
                                 "\n".join(r.get("options") or [])]))
            if len(g):
                i = np.searchsorted(S, g)
                i[i >= len(S)] = 0
                h = g[S[i] == g] if len(S) else g[:0]
                if len(h):
                    hit_src[r.get("source")] += 1
                    for x in h.tolist():
                        gram_src[x].add(r.get("source"))
            if n % 50000 == 0:
                log(f"overlap {a.name}: {n} training rows scanned ({time.time() - t0:.0f}s), {sum(hit_src.values())} hit")
    per_b = collections.defaultdict(lambda: {"requests": 0, "overlap_requests": 0, "sources": collections.Counter()})
    names = {}
    for r, g in zip(rows, per_req):
        e = r["_evaluation"]
        b = per_b[e["catalog_id"]]
        names[e["catalog_id"]] = e["dataset"]
        b["requests"] += 1
        srcs = set()
        for x in g.tolist():
            if x in gram_src:
                srcs |= gram_src[x]
        if srcs:
            b["overlap_requests"] += 1
            b["sources"].update(srcs)
    out = {"name": a.name, "ngram": a.n, "boilerplate_threshold_requests": a.boiler, "train_file": str(train),
           "train_rows": n, "train_rows_sharing_a_gram": sum(hit_src.values()),
           "train_sources_sharing": dict(hit_src.most_common()),
           "benchmarks": [{"catalog_id": k, "dataset": names[k], "requests": v["requests"],
                           "overlap_requests": v["overlap_requests"],
                           "overlap_share": round(v["overlap_requests"] / v["requests"], 4),
                           "top_sources": dict(v["sources"].most_common(5))} for k, v in sorted(per_b.items())],
           "note": "counts only; an overlapping request shares at least one non-boilerplate 12-gram with >= 1 training row"}
    (HERE / f"overlap_{a.name}.json").write_text(json.dumps(out, indent=2) + "\n")
    tot = sum(v["overlap_requests"] for v in per_b.values())
    log(f"overlap {a.name}: {tot}/{len(rows)} sample requests share a 12-gram with C1 training "
        f"({sum(hit_src.values())} training rows) -> overlap_{a.name}.json")


# ------------------------------------------------------------------ verify the rebuild against the published manifest

def cmd_verify_rebuild(a):
    """Per benchmark: normalized source sha256, selected group ids, request and field counts of our rebuild vs the
    harness's hub/manifest.json (the lab's frozen suite). Also checks that, with the missing benchmarks' rows cut out of
    the published order, our selected-rows file is the frozen file minus those benchmarks (by counts)."""
    pub = json.loads((REPO / "hub/manifest.json").read_text())
    ours = json.loads((SUITE / "manifest.json").read_text())
    pb = {b["catalog_id"]: b for b in pub["benchmarks"]}
    ob = {b["catalog_id"]: b for b in ours["benchmarks"]}
    rows = []
    for n in sorted(pb):
        p, o = pb[n], ob.get(n)
        if o is None:
            rows.append({"catalog_id": n, "dataset": p["dataset"], "status": "MISSING in rebuild", "requests_pub": p["requests"]})
            continue
        ps = {s["path"]: s["sha256"] for s in p["sources"]}
        os_ = {s["path"]: s["sha256"] for s in o["sources"]}
        gid_ok = sorted(map(str, pub["selected_group_ids"][str(n)])) == sorted(map(str, o["selected_group_ids"]))
        rows.append({"catalog_id": n, "dataset": p["dataset"], "sources_identical": ps == os_,
                     "selected_groups_identical": gid_ok, "requests": o["requests"], "requests_pub": p["requests"],
                     "fields": o["fields"], "fields_pub": p["fields"],
                     "status": "IDENTICAL" if ps == os_ and gid_ok and o["requests"] == p["requests"]
                     and o["fields"] == p["fields"] else "DIFFERS"})
    res = {"rebuilt_rows_sha256": ours["selected_rows_sha256"], "pinned_full_sha256": pub["files"]["selected-rows.jsonl.gz"]["uncompressed_sha256"],
           "identical": sum(r["status"] == "IDENTICAL" for r in rows), "differs": [r["catalog_id"] for r in rows if r["status"] == "DIFFERS"],
           "missing": [r["catalog_id"] for r in rows if r["status"].startswith("MISSING")],
           "requests_rebuilt": ours["requests"], "requests_pub": pub["requests"], "benchmarks": rows}
    (HERE / "verify_rebuild.json").write_text(json.dumps(res, indent=2) + "\n")
    log(f"verify-rebuild: {res['identical']}/{len(rows)} benchmarks byte-identical sources + same groups/counts; "
        f"differs {res['differs']}; missing {res['missing']}; requests {ours['requests']} vs {pub['requests']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sample")
    p.add_argument("--n", type=int, default=10000)
    p.add_argument("--seed", type=int, default=20260919)
    p.add_argument("--name", default="sample10k")
    p.set_defaults(func=cmd_sample)
    p = sub.add_parser("preflight")
    p.add_argument("--name", default="sample10k")
    p.add_argument("--lean", default=str(JEV / "opendecide-data/lean"))
    p.add_argument("--adapter", default=str(JEV / "backups/modal_models/q35_4b_main500k"))
    p.set_defaults(func=cmd_preflight)
    p = sub.add_parser("check-index-math")
    p.set_defaults(func=cmd_check_index_math)
    p = sub.add_parser("check-parity")
    p.set_defaults(func=cmd_check_parity)
    p = sub.add_parser("verify-rebuild")
    p.set_defaults(func=cmd_verify_rebuild)
    p = sub.add_parser("overlap")
    p.add_argument("--name", default="sample10k")
    p.add_argument("--n", type=int, default=12)
    p.add_argument("--boiler", type=int, default=20)
    p.add_argument("--train", default=str(JEV / "opendecide-data/lean/data/v14_parts/golden_train.jsonl"))
    p.set_defaults(func=cmd_overlap)
    p = sub.add_parser("score")
    p.add_argument("--name", default="sample10k")
    p.add_argument("--run", required=True)
    p.add_argument("--out", default=None)
    p.add_argument("--engine", default="opendecide_c1")
    p.set_defaults(func=cmd_score)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
