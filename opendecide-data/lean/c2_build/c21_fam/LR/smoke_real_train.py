"""IN-MEMORY smoke of every tier-A mapper on the real TRAIN files (placeholder wording pools, dry_run). Writes NO row file:
only counts, drop reasons and set-report numbers go to logs/smoke_real_train.json. Run: python3 smoke_real_train.py [dataset ...]
"""
import importlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mappers"))
import lr_common as lc  # noqa: E402

ORDER = ["aya_redteaming_en", "gandalf_summarization", "juliet_1_3", "datadog_malicious_packages", "logchunks", "hwu64",
         "snips_2017_06", "abcd", "multiwoz_2_2", "taskmaster", "scifact", "qasper", "commonsenseqa", "ethics_mturk", "boardgameqa"]


def run_one(name):
    mod = importlib.import_module(name)
    pools = lc.WordingPools.placeholder_pools(mod.FORMS)
    # the DataDog mapper is blocked by design (LR-B5 / T63-M3); the smoke overrides both gates ONLY to measure the mechanics on positives
    kw = {"approved_fn": (lambda: True), "record_fn": (lambda: True)} if name == "datadog_malicious_packages" else {}
    m = mod.Mapper(pools, seed=1, **kw)
    t = time.time()
    recs = mod.read_train()
    if hasattr(m, "map_with_twins"):
        rows = m.map_with_twins(list(recs), None)
    else:
        rows = m.map_records(recs)
    out = {"dataset": name, "lr_id": mod.META["lr_id"], "rows": len(rows), "cap": mod.META["cap"], "seconds": round(time.time() - t, 1),
           "drops": m.drops.c, "forms": {}}
    forms = sorted({r["form"] for r in rows})
    for f in forms:
        rr = [r for r in rows if r["form"] == f]
        yn = all(r["kind"] == "yesno" for r in rr)
        rep = lc.set_report(rr, yes_no=yn)
        out["forms"][f] = {"n": len(rr), "tokens_mean": round(rep["tokens"]["mean"], 1), "tokens_max": rep["tokens"]["max"],
                           "over1024_share": round(rep["tokens"]["over1024_share"], 4), "R6_pass": rep["R6_pass"],
                           "R5_position_pass": rep["R5_position_pass"], "k_share": rep["k_share"], "R8_pass": rep["R8_pass"],
                           "near_duplicates": rep["near_duplicates"], "yes_rate": rep.get("yes_rate"),
                           "answer_share_top": dict(list(rep["answer_share"].items())[:6])}
    out["length_histogram"] = lc.length_histogram(rows)
    return out


if __name__ == "__main__":
    names = sys.argv[1:] or ORDER
    res = []
    for n in names:
        try:
            r = run_one(n)
        except Exception as e:  # noqa: BLE001
            r = {"dataset": n, "error": repr(e)[:300]}
        res.append(r)
        print(json.dumps({k: r.get(k) for k in ("dataset", "rows", "cap", "seconds", "drops", "error")}), flush=True)
    path = os.path.join(HERE, "logs", "smoke_real_train.json")
    old = {r["dataset"]: r for r in (json.load(open(path)) if os.path.isfile(path) else [])}
    old.update({r["dataset"]: r for r in res})            # merge by dataset: a partial run never drops the others
    with open(path, "w") as f:
        json.dump([old[n] for n in ORDER if n in old], f, indent=1)
