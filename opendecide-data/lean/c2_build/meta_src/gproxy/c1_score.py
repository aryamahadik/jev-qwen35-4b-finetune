#!/usr/bin/env python3
"""Scores the C1 read of the G-proxy (counts and rates only; no row text). C1 output is a measurement here, never a label or a target.
Reads data/c2_gproxy/pab_gproxy.jsonl (hash-checked against GPROXY_HASH.json) and
data/c2_gproxy/c1_read/preds_pab_gproxy/q35_4b_main500k_pab.jsonl; the score is gate_dev.score (argmax of the read, ties are wrong).
Writes data/c2_gproxy/c1_read/C1_GPROXY_RESULT.json: accuracy overall / base rows / twins / per source / per task family, the
pair joint accuracy (both members right, and the 'flip' rate), the cluster-bootstrap 95% CI of accuracy (clusters = verdict.clusters,
10,000 resamples, seed 0), and the sha256 of the preds, meta and pab_gproxy files.
Run from lean/c2_build:  ../../.venv/bin/python -B meta_src/gproxy/c1_score.py"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BUILD = HERE.parents[1]
LEAN = BUILD.parent
sys.path.insert(0, str(BUILD / "pilot_ab"))
import verdict as V  # noqa: E402
import gate_dev as G  # noqa: E402

import os  # noqa: E402
D = Path(os.environ.get("GPROXY_DATA_DIR") or LEAN / "data" / "c2_gproxy")   # env override is for tests only
PRED = D / "c1_read" / "preds_pab_gproxy" / "q35_4b_main500k_pab.jsonl"
META = D / "c1_read" / "preds_pab_gproxy" / "q35_4b_main500k_pab.meta.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    rec = json.loads((D / "GPROXY_HASH.json").read_text())
    comb_sha = sha(D / "pab_gproxy.jsonl")
    assert comb_sha == rec["sha256"]["pab_gproxy.jsonl"], "pab_gproxy.jsonl differs from the recorded hash"
    rows = [json.loads(x) for x in (D / "pab_gproxy.jsonl").read_text().splitlines() if x.strip()]
    rels = [json.loads(x) for x in (D / "pab_gproxy_relations.jsonl").read_text().splitlines() if x.strip()]
    pr = {}
    for x in PRED.read_text().splitlines():
        if x.strip():
            o = json.loads(x)
            pr[o["id"]] = o["probs"]
    missing = [r["id"] for r in rows if r["id"] not in pr]
    extra = set(pr) - {r["id"] for r in rows}
    assert not missing and not extra, f"preds do not match the rows: missing {len(missing)}, extra {len(extra)}"
    meta = json.loads(META.read_text())
    ok = {r["id"]: G.score(r, pr[r["id"]])[0] for r in rows}
    pyes = {r["id"]: float(pr[r["id"]]["yes"]) for r in rows}
    is_twin = lambda r: bool((r.get("meta") or {}).get("twin_of"))
    lab, cinfo = V.clusters(rows, rels)

    def acc(sel):
        sel = list(sel)
        return {"n": len(sel), "ok": int(sum(ok[r["id"]] for r in sel)), "acc_pt": round(100.0 * sum(ok[r["id"]] for r in sel) / max(len(sel), 1), 2)}

    bysrc, byfam = defaultdict(list), defaultdict(list)
    for r in rows:
        bysrc[r["source"]].append(r)
        byfam[r["meta"]["task"].split(".")[0]].append(r)
    byid = {r["id"]: r for r in rows}
    both = flip_ok = 0
    for x in rels:
        a, b = x["a"], x["b"]
        both += int(ok[a] and ok[b])
        # a 'flip': the read's yes-probability moves to the other side of 0.5 between base and twin
        flip_ok += int((pyes[a] > 0.5) != (pyes[b] > 0.5))
    # cluster bootstrap (10,000 resamples, seed 0) of pooled accuracy
    cl = defaultdict(lambda: [0.0, 0])
    for r in rows:
        c = cl[lab[r["id"]]]
        c[0] += ok[r["id"]]
        c[1] += 1
    arr = np.array(list(cl.values()), dtype=float)
    rng = np.random.default_rng(0)
    idx = rng.integers(0, len(arr), size=(10000, len(arr)))
    accs = 100.0 * arr[idx, 0].sum(1) / arr[idx, 1].sum(1)
    res = {"gate": "A42-D 12.4: C1 reads the G-proxy; a measurement, never a label",
           "rows": len(rows), "clusters": cinfo["clusters"], "complement_pairs": cinfo["pairs"],
           "all": acc(rows), "base_rows": acc(r for r in rows if not is_twin(r)), "twin_rows": acc(r for r in rows if is_twin(r)),
           "ci95_all_acc_pt_cluster_bootstrap": [round(float(np.percentile(accs, 2.5)), 2), round(float(np.percentile(accs, 97.5)), 2)],
           "per_source": {k: acc(v) for k, v in sorted(bysrc.items())},
           "per_task_family": {k: acc(v) for k, v in sorted(byfam.items())},
           "pair_both_right": both, "pair_both_right_share": round(both / max(len(rels), 1), 4), "pair_yes_prob_side_flips": flip_ok,
           "mean_p_yes_gold_yes": round(float(np.mean([pyes[r["id"]] for r in rows if r["gold"] == 1])), 4),
           "mean_p_yes_gold_no": round(float(np.mean([pyes[r["id"]] for r in rows if r["gold"] == 0])), 4),
           "share_read_yes": round(float(np.mean([pyes[r["id"]] > 0.5 for r in rows])), 4),
           "engine": meta.get("engine"), "sglang_version": meta.get("sglang_version"), "read_sec": meta.get("read_sec"),
           "rows_per_sec": meta.get("rows_per_sec"), "tta_choice": meta.get("tta_choice"),
           "sha256": {"pab_gproxy.jsonl": comb_sha, "preds": sha(PRED), "preds_meta": sha(META)}}
    (D / "c1_read" / "C1_GPROXY_RESULT.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: res[k] for k in ("rows", "clusters", "complement_pairs", "all", "base_rows", "twin_rows", "ci95_all_acc_pt_cluster_bootstrap",
                                           "per_source", "pair_both_right", "pair_both_right_share", "share_read_yes", "engine", "read_sec", "sha256")}, indent=1))


if __name__ == "__main__":
    main()
