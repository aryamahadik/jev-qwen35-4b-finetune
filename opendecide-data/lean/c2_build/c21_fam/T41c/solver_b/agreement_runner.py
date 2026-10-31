"""Aggregate agreement run: solver A vs solver B on in-memory rows (test-fixture pool, native names) over several seeds and
blocks, plus the K6(i) exhaustive truth tables. Writes ONE counts-only JSON (AGREEMENT_RESULT.json) and SHAS.json.

    python3 solver_b/agreement_runner.py --seeds 5 --n 2000 --out solver_b/

Nothing but counts and shas is written; no row text. Refuses to overwrite a result whose K6(i) or agreement figures are worse
than the 98% / 100% bars without saying so (the result file records pass flags)."""
import argparse
import collections
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import harness  # noqa: E402


def sha_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--out", required=True)
    ap.add_argument("--truth-limit", type=int, default=0, help="0 = exhaustive T1 and T2")
    a = ap.parse_args(argv)
    t0 = time.time()
    tot = collections.Counter()
    strata = collections.defaultdict(lambda: [0, 0])
    anomalies = collections.Counter()
    runs = 0
    for k in range(a.seeds):
        res = harness.run(n=a.n, seed="agree-%d" % k, blocks=("train", "ho", "bd", "ls"))
        runs += 1
        tot["rows"] += res["rows"]
        tot["disagree"] += res["disagree"]
        for st, v in res["strata_agreement"].items():
            strata[st][0] += v["n"]
            strata[st][1] += v["agree"]
        anomalies.update(res["b_anomaly_counts"])
    truth = {}
    for tb in ("T1", "T2", "T3"):
        lim = a.truth_limit if tb != "T3" and a.truth_limit else None
        r = harness.run_truth((tb,), limit=lim)
        truth[tb] = {"cases": r["cases"], "mismatches": r["mismatches"], "render_failures": r["render_failures"],
                     "mismatch_ids": r["mismatch_ids"], "exhaustive": lim is None}
    out = {
        "what": "T41c solver B vs solver A, in-memory rows, test-fixture pool (NOT the production pool), native TRAINING-salt names, counts only",
        "runs": runs, "rows": tot["rows"], "disagree": tot["disagree"],
        "agreement_pct": round(100.0 * (tot["rows"] - tot["disagree"]) / max(1, tot["rows"]), 4),
        "b_anomaly_counts": dict(anomalies),
        "strata": {k: {"n": v[0], "agree": v[1]} for k, v in sorted(strata.items())},
        "k6i_truth": truth,
        "pass": tot["disagree"] == 0 and all(t["mismatches"] == 0 and t["render_failures"] == 0 for t in truth.values()),
        "seconds": round(time.time() - t0, 1),
    }
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "AGREEMENT_RESULT.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    gen = {fn: sha_file(os.path.join(FAM, "t41c", fn)) for fn in sorted(os.listdir(os.path.join(FAM, "t41c"))) if fn.endswith(".py")}
    sb = {}
    for fn in ("agreement_runner.py", "b_program.py", "harness.py", "verbs.py", "pytest.ini", "__init__.py",
               "AGREEMENT_RESULT.json"):
        sb[fn] = sha_file(os.path.join(HERE, fn))
    for fn in ("conftest.py", "test_agreement.py", "test_b.py"):
        sb["tests/" + fn] = sha_file(os.path.join(HERE, "tests", fn))
    fam = os.path.join(os.path.dirname(os.path.dirname(FAM)), "zed_orch", "c21", "families")
    inputs = {"G0_LITE.md": sha_file(os.path.join(fam, "T41c", "G0_LITE.md")),
              "G0_ADDENDUM_v32.md": sha_file(os.path.join(fam, "T41c", "G0_ADDENDUM_v32.md")),
              "handoff/ROW_SCHEMA_FOR_B.json": sha_file(os.path.join(FAM, "handoff", "ROW_SCHEMA_FOR_B.json"))}
    with open(os.path.join(a.out, "SHAS.json"), "w", encoding="utf-8") as f:
        json.dump({"generator_code_shas_at_run": gen, "solver_b": sb, "inputs": inputs, "verbs_version": "b-verbs-v1"}, f,
                  indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps({k: out[k] for k in ("runs", "rows", "disagree", "agreement_pct", "pass", "seconds")}))
    print(json.dumps(truth))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
