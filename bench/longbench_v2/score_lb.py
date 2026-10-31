"""Score a LongBench v2 run (run_lb.py or cascade_lb.py) and compare it with longjev's published Jev numbers.
Prints aggregates only (no item text, no per-item gold).

  opendecide-data/.venv/bin/python bench/longbench_v2/score_lb.py --run bench/longbench_v2/runs/lb2_q35_4b_main500k \\
      --kit bench/external_quarantine/longbench_v2/kit

PRIMARY (PREREG_longbench_v2.md section 5): accuracy on the test_proxy set (163 items: the reconstruction of longjev's
163 "test questions whose input had to be reduced"), a run's failures counted WRONG, against Jev's published 52.8%
(86/163, k inferred from the rounded percentage, unique for n = 163). longjev publishes no per-item Jev answers, so the
comparison is UNPAIRED: difference with a Newcombe (method 10) 95% interval; verdict "better" if the interval is above
0, "worse" if below, else "no significant difference". An unpaired percentile bootstrap is reported for information.
If per-item Jev answers ever appear (longjev's results/raw/items.jsonl format), --jev-items gives a paired bootstrap
and McNemar's exact test on the common items instead (gold from OUR gold file, never from theirs).
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lb_lib as lb  # noqa: E402

# longjev README results (LongBench v2), as quoted by web-search index snapshots of github.com/avshalomd/longjev read
# 2 Oct 2026. They are NOT in the repository at 9d31778 (results removed; its .gitignore: "TypeSafe's terms forbid
# publishing benchmarks or performance information about Jev"). k = the unique integer that rounds to the percentage.
JEV_SOURCE = ("github.com/avshalomd/longjev README results section (web-search index snapshot, read 2026-10-02); "
              "not present at commit 9d317786; per-item answers never published (results/raw is git-ignored)")
JEV = {
    "test_jev_8k": {"k": 86, "n": 163, "pct": 52.8, "what": "jev selector, keep 8K, test questions whose input had to be reduced"},
    "test_embed_16k": {"k": 80, "n": 163, "pct": 49.1},
    "test_embed_then_jev_16k": {"k": 79, "n": 163, "pct": 48.5},
    "test_truncate_16k": {"k": 66, "n": 163, "pct": 40.5},
    "test_vote": {"k": 60, "n": 163, "pct": 36.8, "what": "per-piece vote, no final call"},
    "dev_jev_8k": {"k": 24, "n": 42, "pct": 57.1, "what": "tuning split; 8K picked here (tie with 16K)"},
    "dev_jev_16k": {"k": 24, "n": 42, "pct": 57.1},
    "dev_jev_28k": {"k": 22, "n": 42, "pct": 52.4},
    "direct_fit": {"k": 45, "n": 93, "pct": 48.4, "what": "inputs that fit Jev's window, read whole"},
    "mcnemar_jev_vs_embed_test": {"only_jev": 16, "only_embed": 10, "p": 0.33},
    "median_cost_cents_jev_8k": 0.77, "median_seconds_jev_8k": 2.7,
}
for _k, _v in JEV.items():  # the inferred k must reproduce the published percentage
    if isinstance(_v, dict) and "pct" in _v:
        assert round(100 * _v["k"] / _v["n"], 1) == _v["pct"], _k


def acc_block(recs, gold, pick="pred"):
    """strict: failures (no prediction) count wrong; longjev_rule: failures dropped from n (eval/report.acc)."""
    n = len(recs)
    k = sum(1 for r in recs if r.get(pick) is not None and r[pick] == gold[r.get("item", r["id"])])
    answered = [r for r in recs if r.get(pick) is not None]
    k2 = sum(1 for r in answered if r[pick] == gold[r.get("item", r["id"])])
    lo, hi = lb.wilson(k, n)
    return {"k": k, "n": n, "acc": round(k / n, 4) if n else None, "wilson95": [round(lo, 4), round(hi, 4)],
            "longjev_rule": {"k": k2, "n": len(answered), "acc": round(k2 / len(answered), 4) if answered else None}}


def compare_unpaired(k, n, jk, jn, n_boot=10000, seed=0):
    d, lo, hi = lb.newcombe_diff(k, n, jk, jn)
    rng = random.Random(seed)
    ours = [1] * k + [0] * (n - k)
    pj = jk / jn
    ds = []
    for _ in range(n_boot):
        a = sum(rng.choice(ours) for _ in range(n)) / n
        b = sum(rng.random() < pj for _ in range(jn)) / jn
        ds.append(a - b)
    ds.sort()
    verdict = "better" if lo > 0 else "worse" if hi < 0 else "no significant difference"
    return {"diff_pp": round(100 * d, 2), "newcombe95_pp": [round(100 * lo, 2), round(100 * hi, 2)],
            "bootstrap95_pp_info": [round(100 * ds[int(0.025 * n_boot)], 2), round(100 * ds[int(0.975 * n_boot) - 1], 2)],
            "verdict": verdict, "kind": "unpaired (no per-item Jev answers published)"}


def compare_paired(recs, gold, jev_items_path, n_boot=10000, seed=0):
    jv = {}
    for r in lb.read_jsonl(jev_items_path):
        ch = (r.get("results", {}).get("jev@8000") or {}).get("choice")
        jv[r["id"]] = ch
    common = [r for r in recs if r["id"] in jv]
    if not common:
        return {"paired": None, "note": "no common items"}
    a = [int(r.get("pred") is not None and r["pred"] == gold[r["id"]]) for r in common]
    b = [int(jv[r["id"]] is not None and jv[r["id"]] == gold[r["id"]]) for r in common]
    rng = random.Random(seed)
    n = len(common)
    ds = []
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        ds.append(sum(a[i] - b[i] for i in idx) / n)
    ds.sort()
    only_a = sum(x and not y for x, y in zip(a, b))
    only_b = sum(y and not x for x, y in zip(a, b))
    lo, hi = ds[int(0.025 * n_boot)], ds[int(0.975 * n_boot) - 1]
    # longjev's own pairing (eval/report.paired): only items where BOTH sides gave an answer
    both = [(r["pred"] == gold[r["id"]], jv[r["id"]] == gold[r["id"]]) for r in common
            if r.get("pred") is not None and jv[r["id"]] is not None]
    lj_a, lj_b = sum(x and not y for x, y in both), sum(y and not x for x, y in both)
    return {"n_common": n, "diff_pp": round(100 * (sum(a) - sum(b)) / n, 2),
            "paired_bootstrap95_pp": [round(100 * lo, 2), round(100 * hi, 2)], "only_ours": only_a, "only_jev": only_b,
            "mcnemar_p": round(lb.mcnemar(only_a, only_b), 4),
            "longjev_pairing": {"n": len(both), "only_ours": lj_a, "only_jev": lj_b, "mcnemar_p": round(lb.mcnemar(lj_a, lj_b), 4)},
            "verdict": "better" if lo > 0 else "worse" if hi < 0 else "no significant difference", "kind": "paired"}


def jev_file_headline(jev_items_path, gold, test_ids, budget=lb.BUDGET):
    """longjev's own headline count (eval/report.acc(test, choice_at("jev", 8000)): long test rows, rows without a choice
    dropped from n) recomputed from a longjev results/raw/items.jsonl, gold from OUR gold file. Fed longjev's real file
    it must reproduce the published 86/163; also counts how many of its rows are in our test_proxy reconstruction."""
    rows = [r for r in lb.read_jsonl(jev_items_path) if not r.get("fits") and r.get("split") == "test"]
    picks = [((r.get("results") or {}).get(f"jev@{budget}") or {}).get("choice") for r in rows]
    hits = [p == gold[r["id"]] for p, r in zip(picks, rows) if p is not None]
    k, n = sum(hits), len(hits)
    j = JEV["test_jev_8k"]
    return {"k": k, "n": n, "acc": round(k / n, 4) if n else None, "pct": round(100 * k / n, 1) if n else None,
            "matches_published": (k, n) == (j["k"], j["n"]), "file_test_long_rows": len(rows),
            "file_rows_in_test_proxy": len({r["id"] for r in rows} & set(test_ids)), "test_proxy_n": len(test_ids)}


def breakdown(recs, gold, index, field):
    by = defaultdict(list)
    for r in recs:
        by[index[r.get("item", r["id"])][field]].append(r)
    return {k: acc_block(v, gold) for k, v in sorted(by.items())}


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def score(run_dir, kit, jev_items=None, allow_incomplete=False, overlap=None):
    run_dir, kit = Path(run_dir), Path(kit)
    man = json.loads((run_dir / "manifest.json").read_text())
    if man.get("status") != "complete" and not allow_incomplete:
        raise SystemExit(f"{run_dir}: run not complete")
    gold = {r["id"]: r["gold"] for r in lb.read_jsonl(kit / "lb_gold.jsonl")}
    index = {r["id"]: r for r in lb.read_jsonl(kit / "lb_index.jsonl")}
    kmeta = json.loads((kit / "lb_meta.json").read_text())
    ran_items = man.get("settings", {}).get("items_sha256") or man.get("items_sha256")
    if ran_items != kmeta["files"]["lb_items.jsonl"]:
        raise SystemExit("the run used a different items file than this kit")
    preds = lb.read_jsonl(run_dir / "preds.jsonl")
    main = [r for r in preds if r.get("arm", "keep8k").startswith("keep8k")]
    ctrl = [r for r in preds if r.get("arm") == "direct"]
    got = {r["id"] for r in main}
    res = {"run": str(run_dir), "name": man.get("name"), "status": man.get("status"), "jev_source": JEV_SOURCE,
           "sets": {}, "primary": None}
    for s in ("test_proxy", "dev_proxy", "all_proxy", "test_own", "dev_own", "all_own"):
        want = [i for i, m in index.items() if lb.in_set(m, s)]
        if not want:
            continue
        missing = [i for i in want if i not in got]
        recs = [r for r in main if r["id"] in set(want)] + [{"id": i, "pred": None, "pred_1view": None} for i in missing]
        blk = {**acc_block(recs, gold), "missing_items": len(missing),
               "one_view": acc_block(recs, gold, "pred_1view") if man.get("settings", {}).get("choice_readout") == "2view" else None,
               "by_difficulty": breakdown(recs, gold, index, "difficulty"),
               "by_length": breakdown(recs, gold, index, "length")}
        if s in ("test_proxy", "all_proxy"):
            blk["by_domain"] = breakdown(recs, gold, index, "domain")
        res["sets"][s] = blk
    tp = res["sets"].get("test_proxy")
    if tp:
        j = JEV["test_jev_8k"]
        res["primary"] = {"ours": {k: tp[k] for k in ("k", "n", "acc", "wilson95")},
                          "jev": {"k": j["k"], "n": j["n"], "acc": round(j["k"] / j["n"], 4),
                                  "wilson95": [round(x, 4) for x in lb.wilson(j["k"], j["n"])]},
                          "comparison": compare_unpaired(tp["k"], tp["n"], j["k"], j["n"])}
        if jev_items:
            tp_ids = {i for i, m in index.items() if lb.in_set(m, "test_proxy")}
            recs = [r for r in main if r["id"] in tp_ids]
            res["primary"]["paired"] = compare_paired(recs, gold, jev_items)
            res["primary"]["jev_file_headline"] = jev_file_headline(jev_items, gold, tp_ids)
    dp = res["sets"].get("dev_proxy")
    if dp:
        j = JEV["dev_jev_8k"]
        res["secondary_dev"] = {"ours": {k: dp[k] for k in ("k", "n", "acc")}, "jev": j,
                                "comparison": compare_unpaired(dp["k"], dp["n"], j["k"], j["n"]),
                                "note": "Jev's dev number is in-sample for longjev (8K was picked on it)"}
    if ctrl:
        want = [i for i, m in index.items() if lb.in_set(m, "control_proxy")]
        recs = [r for r in ctrl if r["item"] in set(want)]
        recs += [{"id": i, "item": i, "pred": None} for i in set(want) - {r["item"] for r in ctrl}]
        cb = acc_block(recs, gold)
        j = JEV["direct_fit"]
        res["secondary_control"] = {"ours": cb, "jev": j, "comparison": compare_unpaired(cb["k"], cb["n"], j["k"], j["n"]),
                                    "note": f"different n (our reconstruction {cb['n']} vs their 93); whole inputs up to "
                                            "~28K tokens, beyond the ~8K our model was trained on"}
    res["diagnostics"] = {
        "items_scored": len(main), "final_failed": sum(r.get("final_failed") is not None for r in main),
        "too_long_drops_items": sum((r.get("too_long_drops") or 0) > 0 for r in main),
        "failed_chunks": sum(r.get("failed_chunks") or 0 for r in main),
        "chunks": sum(r.get("n_chunks") or 0 for r in main),
        "kept_tokens_median": med(r.get("kept_tokens") for r in main),
        "kept_chars_median": med(r.get("kept_chars") for r in main),
        "n_kept_median": med(r.get("n_kept") for r in main),
        "budget_below_8000_items": sum((r.get("budget") or lb.BUDGET) < lb.BUDGET for r in main),
        "seconds_per_question_median": med((r.get("score_s") or 0) + (r.get("final_s") or 0) for r in main
                                           if r.get("score_s") is not None),
        "jev_reference": {"median_seconds": JEV["median_seconds_jev_8k"], "median_cost_cents": JEV["median_cost_cents_jev_8k"],
                          "note": "Jev: hosted API, 24 concurrent requests; ours: one L4, chunks batched, sequential items"},
    }
    if overlap:  # REPORT-ONLY sensitivity: test_proxy without the items our training data overlaps
        ov = json.loads(Path(overlap).read_text()).get("hit_ids")
        if ov is None:
            raise SystemExit(f"{overlap} has no hit_ids (counts-only file); use overlap_counts_c1_train.json")
        tp_ids = {i for i, m in index.items() if lb.in_set(m, "test_proxy")}
        res["sensitivity_overlap"] = {}
        for kind in ("question_option", "context"):
            drop = set(ov.get(kind) or [])
            keep = [r for r in main if r["id"] in tp_ids and r["id"] not in drop]
            keep += [{"id": i, "pred": None} for i in tp_ids - drop - {r["id"] for r in main}]
            res["sensitivity_overlap"][f"test_proxy_minus_{kind}"] = {**{k: v for k, v in acc_block(keep, gold).items()
                                                                       if k in ("k", "n", "acc", "wilson95")},
                                                                    "dropped": len(tp_ids & drop)}
    if "chunk_routed_share" in man:
        res["cascade"] = {k: man[k] for k in ("chunk_routed_share", "final_routed", "final_routed_share")}
    (run_dir / "score.json").write_text(json.dumps(res, indent=1))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--kit", default=str(lb.QUARANTINE / "kit"), help="dir with lb_gold.jsonl, lb_index.jsonl, lb_meta.json")
    ap.add_argument("--jev-items", default=None, help="per-item Jev answers in longjev's items.jsonl format (if ever published)")
    ap.add_argument("--allow-incomplete", action="store_true", help="tests only")
    ap.add_argument("--overlap", default=None, help="overlap_counts json with hit_ids: report-only sensitivity rows")
    a = ap.parse_args(argv)
    res = score(a.run, a.kit, a.jev_items, a.allow_incomplete, a.overlap)
    short = {"primary": res["primary"], "secondary_dev": res.get("secondary_dev"),
             "secondary_control": res.get("secondary_control"), "sensitivity_overlap": res.get("sensitivity_overlap"),
             "sets": {s: {k: v[k] for k in ("k", "n", "acc", "wilson95", "missing_items")} for s, v in res["sets"].items()},
             "diagnostics": res["diagnostics"]}
    print(json.dumps(short, indent=1))
    return res


if __name__ == "__main__":
    main()
