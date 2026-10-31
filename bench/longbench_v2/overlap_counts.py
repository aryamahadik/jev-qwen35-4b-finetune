#!/usr/bin/env python3
"""COUNTS-ONLY overlap check: LongBench v2 (questions + options; sampled context 13-grams) vs our train/dev jsonl.
Never prints item text or gold labels: only counts and our own file names. Pattern of
bench/external_quarantine/ejs5/overlap_counts.py (13-gram and exact-string matches, lower-cased word tokens).

  opendecide-data/.venv/bin/python bench/longbench_v2/overlap_counts.py \\
      --data bench/external_quarantine/longbench_v2/hf_2b48e494/data.json \\
      --index bench/external_quarantine/longbench_v2/kit/lb_index.jsonl
Writes bench/external_quarantine/longbench_v2/overlap_counts.json (counts, our file names, and the LongBench _id values
of hit items, for score_lb.py --overlap sensitivity rows). For one training file only:
  ... --files opendecide-data/lean/data/v14_parts/golden_train.jsonl --out <quarantine>/overlap_counts_c1_train.json
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
from multiprocessing import Pool

ROOTS = ["/Users/aryamahadik/Documents/jev/opendecide-data/lean/data",
         "/Users/aryamahadik/Documents/jev/opendecide-data/data"]
N = 13
CTX_EVERY = 20  # context 13-grams: every 20th start position of the union items' contexts
TOK = re.compile(r"[a-z0-9]+")
G_Q, G_C, EX = {}, {}, {}


def build(data_path, index_path):
    items = json.load(open(data_path, encoding="utf-8"))
    union = set()
    for line in open(index_path):
        m = json.loads(line)
        if m.get("long_proxy") or m.get("long_own"):
            union.add(m["id"])
    gq, gc, ex = collections.defaultdict(set), collections.defaultdict(set), {}
    for i, it in enumerate(items):
        for s in [it["question"]] + [it[f"choice_{L}"] for L in "ABCD"]:
            tk = TOK.findall(s.lower())
            if len(tk) >= 6:
                ex.setdefault(" ".join(tk), set()).add(i)
            for j in range(len(tk) - N + 1):
                gq[" ".join(tk[j:j + N])].add(i)
        if it["_id"] in union:
            tk = TOK.findall(it["context"].lower())
            for j in range(0, len(tk) - N + 1, CTX_EVERY):
                gc[" ".join(tk[j:j + N])].add(i)
    return gq, gc, ex, len(items), len(union)


def strings(o, out):
    if isinstance(o, str):
        out.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            strings(v, out)
    elif isinstance(o, list):
        for v in o:
            strings(v, out)


def chunks(path, size=48 << 20):
    n = os.path.getsize(path)
    out, start = [], 0
    with open(path, "rb") as fh:
        while start < n:
            end = min(n, start + size)
            if end < n:
                fh.seek(end)
                fh.readline()
                end = fh.tell()
            out.append((path, start, end))
            start = end
    return out


def init(gq, gc, ex):
    G_Q.update(gq)
    G_C.update(gc)
    EX.update(ex)


def work(job):
    path, start, end = job
    r = {"records": 0, "bad": 0, "q_rec": 0, "c_rec": 0, "ex_rec": 0, "q_items": set(), "c_items": set(),
         "ex_items": set()}
    with open(path, "rb") as fh:
        fh.seek(start)
        data = fh.read(end - start)
    for line in data.split(b"\n"):
        if not line.strip():
            continue
        r["records"] += 1
        try:
            rec = json.loads(line)
        except Exception:
            r["bad"] += 1
            continue
        ss = []
        strings(rec, ss)
        hq, hc, he = set(), set(), set()
        for s in ss:
            tk = TOK.findall(s.lower())
            if not tk:
                continue
            j = " ".join(tk)
            if j in EX:
                he |= EX[j]
            if len(tk) >= N:
                for g in {" ".join(tk[i:i + N]) for i in range(len(tk) - N + 1)}:
                    if g in G_Q:
                        hq |= G_Q[g]
                    if g in G_C:
                        hc |= G_C[g]
        for key, hit in (("q", hq), ("c", hc), ("ex", he)):
            if hit:
                r[f"{key}_rec"] += 1
                r[f"{key}_items"] |= hit
    return path, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--index", required=True)
    ap.add_argument("--out", default="/Users/aryamahadik/Documents/jev/bench/external_quarantine/longbench_v2/overlap_counts.json")
    ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--files", nargs="*", default=None, help="only these jsonl files (default: every jsonl under ROOTS)")
    a = ap.parse_args()
    gq, gc, ex, n_items, n_union = build(a.data, a.index)
    files = sorted(a.files) if a.files else sorted({p for r in ROOTS for p in glob.glob(os.path.join(r, "**", "*.jsonl"),
                                                                                        recursive=True)})
    # held-out OHS-3 files (data/ohs3*, data/ohs3_parts/) are never opened, not even for counts
    files = [p for p in files if not any(part.startswith("ohs3") for part in os.path.normpath(p).split(os.sep))]
    jobs = [c for f in files for c in chunks(f)]
    print(f"bench: {len(gq)} question/option {N}-grams, {len(gc)} sampled context {N}-grams, {len(ex)} exact strings;"
          f" our files {len(files)}, chunks {len(jobs)}", flush=True)
    per, items_q, items_c, items_e = {}, set(), set(), set()
    with Pool(a.procs, initializer=init, initargs=(gq, gc, ex)) as pool:
        for path, r in pool.imap_unordered(work, jobs, chunksize=1):
            p = per.setdefault(os.path.relpath(path, "/Users/aryamahadik/Documents/jev"),
                               {"records": 0, "bad": 0, "q_rec": 0, "c_rec": 0, "ex_rec": 0})
            for k in p:
                p[k] += r[k]
            items_q |= r["q_items"]
            items_c |= r["c_items"]
            items_e |= r["ex_items"]
    hit_files = {k: v for k, v in per.items() if v["q_rec"] or v["c_rec"] or v["ex_rec"]}
    ids = [it["_id"] for it in json.load(open(a.data, encoding="utf-8"))]
    flags = {}
    for line in open(a.index):
        m = json.loads(line)
        flags[m["id"]] = m
    def by_set(hit):  # counts of hit items per kit set (ids only, no text)
        hs = {ids[i] for i in hit}
        tp = lambda m: m.get("long_proxy") and m["split"] == "test"  # noqa: E731
        return {"total": len(hs), "test_proxy": sum(1 for i in hs if tp(flags[i])),
                "all_proxy": sum(1 for i in hs if flags[i].get("long_proxy")),
                "union": sum(1 for i in hs if flags[i].get("long_proxy") or flags[i].get("long_own"))}
    res = {"n_items": n_items, "n_union_contexts_sampled": n_union, "files": len(files),
           "records": sum(v["records"] for v in per.values()),
           "items_with_question_option_13gram_hit": len(items_q), "items_with_exact_question_or_option_hit": len(items_e),
           "items_with_sampled_context_13gram_hit": len(items_c),
           "records_hit": {"q": sum(v["q_rec"] for v in per.values()), "ctx": sum(v["c_rec"] for v in per.values()),
                           "exact": sum(v["ex_rec"] for v in per.values())},
           "items_by_set": {"question_option": by_set(items_q), "exact": by_set(items_e), "context": by_set(items_c)},
           "hit_ids": {"question_option": sorted(ids[i] for i in items_q), "exact": sorted(ids[i] for i in items_e),
                       "context": sorted(ids[i] for i in items_c)},  # LongBench _id values only (no text)
           "files_with_hits": hit_files}
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ("files_with_hits", "hit_ids")}, indent=1))
    print("files with hits:", len(hit_files))


if __name__ == "__main__":
    main()
