"""Oracle end-to-end mapping check for od_engine (CPU, no weights; counts and aggregate scores only, no item text).

A stub replaces decoder_io.cand_logits. For every view the engine reads, it renders the REAL prompt
(Readout.prompt(row, perm)), finds the one label the gold option is shown under, and puts +12 on that letter. Everything
else is the real path: od_engine.build_row, Readout.prompt, decoder_io.to_probs (perm handling), the 2-view average,
the key mapping back to the harness keys, harness validate, and harness score_run on the sample suite. If option order,
label names, yes/no polarity or the reversal were mapped wrong, benchmarks would score below their ceiling.
Gold for ToolRet/BRIGHT (expected = None) comes from the harness's own qrels (relevant -> yes).

  PYTHONPATH=bench/external_quarantine/decision_index/repo:bench/decision_index HF_HUB_OFFLINE=1 \
      opendecide-data/.venv/bin/python bench/decision_index/check_oracle.py --name sample10k
  -> bench/decision_index/check_oracle_<name>.json (per-benchmark oracle score vs ceiling). The per-item oracle results
     encode gold, so they are deleted after scoring.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import shutil
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
JEV = HERE.parents[1]
Q = JEV / "bench/external_quarantine/decision_index"
sys.path.insert(0, str(Q / "repo"))
sys.path.insert(0, str(HERE))


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} check-oracle: {msg}"
    print(line, flush=True)
    with open(HERE / "progress.log", "a") as f:
        f.write(line + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="sample10k")
    a = ap.parse_args()
    import torch
    import od_engine
    from decision_index.engines import validate
    from decision_index.pipeline import score_run
    from decision_index.scoring.metrics import score_query
    from decision_index.suite.io import Suite, dumps

    eng = od_engine.ODEngine(adapter=str(JEV / "backups/modal_models/q35_4b_main500k"),
                             lean=str(JEV / "opendecide-data/lean"), fake=True, base="Qwen/Qwen3.5-4B",
                             revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    dio = eng.dio
    st = collections.Counter()

    def stub(model, ro, rows, dev, perms=None):
        perms = perms or [None] * len(rows)
        out = []
        for r, p in zip(rows, perms):
            lr = dio.as_letter_row(r)
            n = len(lr["options"])
            lg = torch.zeros(n)
            g = r.get("_gold")
            if g is not None:
                pr = ro.prompt(r, p)
                hits = [i for i in range(n) if f"\n{dio.label(i)}. {g}\n" in pr or f"\n{dio.label(i)}. {g}: " in pr]
                disp = lr["options"] if p is None else [lr["options"][j] for j in p]
                exp_i = disp.index(g)
                if len(hits) == 1:
                    i = hits[0]
                    st["views_gold_label_found_in_prompt"] += 1
                    st["views_prompt_label_ne_perm_position"] += int(i != exp_i)
                else:
                    st[f"views_gold_label_hits_{min(len(hits), 2)}"] += 1
                    i = exp_i
                lg[i] = 12.0
            out.append(lg)
        return out

    dio.cand_logits = stub
    orig_build = od_engine.build_row
    cur = {}

    def build_w(s, q, qid):
        row, info = orig_build(s, q, qid)
        gk = cur.get(qid)
        if gk is not None:
            row["_gold"] = (info["options"][info["keys"].index(gk)] if info["kind"] == "choice"
                            else ("Yes" if gk == info["keys"][0] else "No"))
        return row, info

    od_engine.build_row = build_w
    out_dir = Q / "runs" / f"oracle_{a.name}"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    rows = [json.loads(x) for x in gzip.open(Q / "sample" / f"{a.name}.jsonl.gz", "rt")]
    log(f"{a.name}: {len(rows)} requests")
    t0 = time.time()
    with open(out_dir / "results.jsonl", "w") as f:
        for j, r in enumerate(rows):
            e = r["_evaluation"]
            cur.clear()
            for idx, (k, q) in enumerate(r["questions"].items()):
                g = r["expected"].get(k)
                if g is None and e["catalog_id"] in (2, 36):
                    rel = r["scoring"]["qrels"].get(r["scoring"]["field_to_document"].get(k), 0)
                    g = next(x for x in q["criteria"] if str(x).lower() == ("yes" if rel > 0 else "no"))
                cur[f"q{idx}"] = g
                st["questions_gold_none" if g is None else "questions_gold_set"] += 1
            try:
                resp, _ = eng(r["state"], r["questions"])
                validate(r["questions"], resp)
                status = "ok"
            except od_engine.Unsupported:
                resp, status = None, "unsupported"
            st[f"requests_{status}"] += 1
            f.write(dumps({**e, "status": status, "response": resp, "total_wall_ms": 1.0,
                           "model_request_wall_ms": 1.0}) + "\n")
            if (j + 1) % 1000 == 0:
                log(f"{a.name}: {j + 1}/{len(rows)} ({time.time() - t0:.0f}s)")
    s = score_run(Suite(Q / "sample" / f"suite_{a.name}"), out_dir / "results.jsonl", "oracle", out_dir / "scored")
    # ceilings: nDCG of the best possible ranking of the scored candidates; RouterBench mean best quality
    groups, best6 = collections.defaultdict(list), []
    for r in rows:
        n = r["_evaluation"]["catalog_id"]
        if n in (2, 36):
            groups[(n, r["_evaluation"]["group_id"])].append(r)
        if n == 6 and "quality" in r["questions"]:
            best6.append(max(o["quality"] for o in r["scoring"]["outcomes"].values()))
    ceil = collections.defaultdict(list)
    for (n, _), rs in groups.items():
        sc, qr = rs[0]["scoring"], rs[0]["scoring"]["qrels"]
        m = max(qr.values()) if qr else 1
        docs = {d for x in rs for d in x["scoring"]["field_to_document"].values()}
        ceil[n].append(score_query(sc, {d: (qr.get(d, 0) / m if m else 0.0) for d in docs})["ndcg_at_10"] or 0.0)
    ceilings = {"2": statistics.mean(ceil[2]) if ceil[2] else None, "36": statistics.mean(ceil[36]) if ceil[36] else None,
                "6": statistics.mean(best6) if best6 else None}
    bench = []
    for k, b in sorted(s["index_benchmarks"].items(), key=lambda x: int(x[0])):
        if b.get("coverage", 0) == 0 and int(k) in (7, 13, 15, 16, 17, 19):
            continue  # interactive placeholders, not in the static index
        bench.append({"catalog_id": int(k), "dataset": s["benchmarks"].get(k, {}).get("dataset"), "in_index": True,
                      "oracle_raw": round(b["raw"], 4), "coverage": round(b["coverage"], 4),
                      "ceiling": round(ceilings[k], 4) if ceilings.get(k) is not None else 1.0})
    for k, b in sorted(s["benchmarks"].items(), key=lambda x: int(x[0])):
        if not b.get("in_index"):
            bench.append({"catalog_id": int(k), "dataset": b.get("dataset"), "in_index": False, "metric": b.get("metric"),
                          "oracle_score": b.get("score")})
    res = {"name": a.name, "what": __doc__.split("\n\n")[0], "view_and_request_counts": dict(st),
           "oracle_index": s["decision_index"], "counts": s["counts"], "benchmarks": bench,
           "note": "ceiling = 1.0 except ToolRet/BRIGHT (best nDCG@10 of the scored candidates under the qrels) and "
                   "RouterBench (mean best outcome quality); coverage < 1 = the requests over the 16,384-token limit"}
    (HERE / f"check_oracle_{a.name}.json").write_text(json.dumps(res, indent=2) + "\n")
    shutil.rmtree(out_dir)  # per-item oracle answers encode gold: keep aggregates only
    below = [x["catalog_id"] for x in bench if x["in_index"] and x["coverage"] == 1 and x["oracle_raw"] < x["ceiling"] - 1e-4]
    below += [x["catalog_id"] for x in bench if not x["in_index"] and x.get("oracle_score") not in (None, 1, 1.0)
              and not str(x.get("metric", "")).startswith("Brier")]
    partial = [x["catalog_id"] for x in bench if x["in_index"] and x["coverage"] < 1]
    log(f"{a.name}: oracle index {s['decision_index']} counts {s['counts']}; views {dict(st)}; fully covered benchmarks "
        f"below ceiling: {below}; benchmarks with refused requests: {partial} -> check_oracle_{a.name}.json")


if __name__ == "__main__":
    main()
