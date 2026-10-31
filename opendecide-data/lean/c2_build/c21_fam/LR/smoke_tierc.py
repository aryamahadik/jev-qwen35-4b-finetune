"""IN-MEMORY smoke of the nine tier-C mappers on the real TRAIN files (placeholder wording pools, dry_run). Writes NO row file:
only counts, drop reasons and set-report numbers go to logs/smoke_tierc.json. Two runs per dataset: (a) at the dataset's cap (what
production would take), (b) an AVAILABILITY run with a huge cap (how many rows the mapper can make from the whole train split).
MBPP needs the sandbox hook for its execution gold (none here): only candidate counts are reported. CommitPackFT is measured on a
per-language sample (the diff step is slow); its availability is then a SAMPLE measurement, labelled as such.
Usage: python3 smoke_tierc.py [dataset ...]
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

ORDER = ["cuad", "ecare", "social_iqa", "quartz", "strategyqa", "finqa", "swe_gym", "commitpackft", "mbpp"]
BIG = 10 ** 9
CPFT_SAMPLE_PER_LANG = int(os.environ.get("CPFT_SAMPLE_PER_LANG", "300"))   # 0 = every row (full read)


def reader(mod, name):
    if name == "commitpackft":
        return list(mod.read_train(max_rows_per_lang=CPFT_SAMPLE_PER_LANG or None))
    return list(mod.read_train())


def summarize(rows):
    out = {}
    for f in sorted({r["form"] for r in rows}):
        rr = [r for r in rows if r["form"] == f]
        yn = all(r["kind"] == "yesno" for r in rr)
        rep = lc.set_report(rr, yes_no=yn)
        out[f] = {"n": len(rr), "tokens_mean": round(rep["tokens"]["mean"], 1), "tokens_max": rep["tokens"]["max"],
                  "over1024_share": round(rep["tokens"]["over1024_share"], 4), "R6_pass": rep["R6_pass"],
                  "R5_position_pass": rep["R5_position_pass"], "k_share": rep["k_share"], "R8_pass": rep["R8_pass"],
                  "exact_dup": rep["exact_duplicate_renderings"], "near_duplicates": rep["near_duplicates"], "yes_rate": rep.get("yes_rate"),
                  "R9_pass": rep["R9_pass"]}
    return out


def run_one(name):
    mod = importlib.import_module(name)
    pools = lc.WordingPools.placeholder_pools(mod.FORMS)
    t = time.time()
    recs = reader(mod, name)
    res = {"dataset": name, "lr_id": mod.META["lr_id"], "cap": mod.META["cap"], "source_records_read": len(recs)}
    if name == "mbpp":
        m = mod.Mapper(pools, seed=1)
        m.map_records(recs)
        n_cand = 0
        for r in recs:
            if r.get("test_list") and r.get("code"):
                n_cand += 1 + len(mod.simple_mutants(mod.normalise_code(r["code"]), mod.MAX_MUTANTS, 1))
        res.update({"rows": 0, "note": "no exec_fn hook in CPU smoke: gold needs the sandbox", "problems": len(recs),
                    "candidate_(code,test)_pairs_before_execution": n_cand, "drops": m.drops.c, "seconds": round(time.time() - t, 1)})
        return res
    m = mod.Mapper(pools, seed=1)
    rows = m.map_records(list(recs))
    res.update({"rows_at_cap": len(rows), "drops_at_cap": m.drops.c, "forms_at_cap": summarize(rows), "length_histogram": lc.length_histogram(rows)})
    if rows:       # the bars of G0-lite section 6 are per DATASET (all forms together), so report them that way as well
        rep = lc.set_report(rows, yes_no=all(r["kind"] == "yesno" for r in rows))
        res["dataset_level_at_cap"] = {"n": len(rows), "tokens_mean": round(rep["tokens"]["mean"], 1), "tokens_max": rep["tokens"]["max"],
                                       "over1024_share": round(rep["tokens"]["over1024_share"], 4), "R6_pass": rep["R6_pass"],
                                       "R5_position_pass": rep["R5_position_pass"], "R8_pass": rep["R8_pass"], "R9_pass": rep["R9_pass"],
                                       "near_duplicates": rep["near_duplicates"], "yes_rate": rep.get("yes_rate"), "k_share": rep["k_share"]}
    m2 = mod.Mapper(pools, seed=1)
    allrows = m2.map_records(list(recs), cap=BIG)
    res.update({"rows_available": len(allrows), "drops_available_run": m2.drops.c,
                "available_by_form": {f: sum(1 for r in allrows if r["form"] == f) for f in sorted({r["form"] for r in allrows})},
                "available_yes_rate": (round(sum(1 for r in allrows if r["answer_text"] == "Yes") / len(allrows), 4) if allrows and allrows[0]["kind"] == "yesno" else None),
                "available_is_sample_measurement": name == "commitpackft" and bool(CPFT_SAMPLE_PER_LANG), "seconds": round(time.time() - t, 1)})
    return res


if __name__ == "__main__":
    names = sys.argv[1:] or ORDER
    path = os.path.join(HERE, "logs", "smoke_tierc.json")
    old = {r["dataset"]: r for r in (json.load(open(path)) if os.path.isfile(path) else [])}
    for n in names:
        try:
            r = run_one(n)
        except Exception as e:  # noqa: BLE001
            r = {"dataset": n, "error": repr(e)[:400]}
        old[n] = r
        print(json.dumps({k: r.get(k) for k in ("dataset", "rows_at_cap", "rows_available", "source_records_read", "seconds", "drops_at_cap", "error", "note")}), flush=True)
        with open(path, "w") as f:
            json.dump([old[x] for x in ORDER if x in old], f, indent=1)
