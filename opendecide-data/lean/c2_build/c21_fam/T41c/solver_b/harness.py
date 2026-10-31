"""Agreement harness: solver A (the lane generator's own label, via t41c.spec.label_of) vs solver B (solver_b.py).

Generates rows IN MEMORY only (test pool, proxy names), runs both solvers, prints/returns COUNTS and disagreement
classes (never item text). Writes nothing into the repo; `--out` goes to a path the caller chooses (use a temp dir).

    python3 solver_b/harness.py --n 2000 --seed s1 --blocks train,ho,bd --out /tmp/x/report.json
"""
import argparse
import collections
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
INFRA = os.path.join(os.path.dirname(os.path.dirname(FAM)), "c21_infra")
for p in (FAM, INFRA):
    if p not in sys.path:
        sys.path.insert(0, p)

def _load_b():
    # b_program imports its sibling `verbs`; put this folder first on the path (solver B never imports t41c)
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import b_program
    return b_program


def load_schema():
    with open(os.path.join(FAM, "handoff", "ROW_SCHEMA_FOR_B.json"), encoding="utf-8") as f:
        return json.load(f)


def _plan_build(n, seed, block, pool, heldout):
    from t41c import build, planner
    if block == "train":
        specs, _ = planner.plan_specs(n, seed=seed, block="train", heldout=heldout, proxy_names=False)
    elif block == "ho":
        specs, _ = planner.plan_heldout(heldout=heldout, seed="ho-" + seed, proxy_names=False)
    elif block == "bd":
        specs, _ = planner.plan_benign_dev(heldout=heldout, seed="bd-" + seed, proxy_names=False)
    elif block == "ls":
        specs, _ = planner.plan_long_slice(heldout=heldout, seed="ls-" + seed, proxy_names=False)
    else:
        raise SystemExit("unknown block %s" % block)
    rows, rep = build.build_rows(specs, pool, proxy_names=False)
    return specs, rows, rep


def classify(spec, bres, a_label):
    """Disagreement class key: coarse, no text."""
    dirs = bres["directives"]
    kinds = sorted({d["cls"].split(".")[0] for d in dirs}) or ["none"]
    rules = sorted({d["rule"] for d in dirs}) or [1]
    risks = sorted({str(d["risk"]) for d in dirs}) or ["-"]
    return {"pair": "A=%s|B=%s" % (a_label, bres["label"]),
            "facts": "present" if bres["facts_present"] else "absent",
            "src": ",".join(sorted({d["src"] for d in dirs})) or "-",
            "kinds": "+".join(kinds), "b_rules": ",".join(map(str, rules)), "b_risk": ",".join(risks),
            "n_dir": len(dirs)}


def run(n=2000, seed="s1", blocks=("train",), per_cell=12, verbose=False):
    from t41c import pools
    from t41c import planner
    from t41c.render import export_for_b
    from t41c.spec import label_of
    sb = _load_b()
    schema = load_schema()
    necessary = {k: tuple(v) for k, v in schema["necessary_steps"].items()}
    pool = pools.make_test_pool(per_cell=per_cell)
    heldout = planner.draw_heldout()
    res = {"seed": seed, "n_requested": n, "pool_kind": pool.kind, "blocks": {}}
    tot = collections.Counter()
    dis_total = collections.Counter()
    anomalies = collections.Counter()
    by_stratum = collections.defaultdict(lambda: [0, 0])
    confusion = collections.Counter()
    classes = collections.Counter()
    diag = collections.Counter()
    for block in blocks:
        specs, rows, rep = _plan_build(n, seed, block, pool, heldout)
        agree = dis = 0
        for s, r in rows:
            a = label_of(s)
            br = sb.solve_b(export_for_b(r), necessary)
            b = br["label"]
            ex = export_for_b(r)
            for d in br["directives"]:
                diag["rule%d" % d["rule"]] += 1
                for why in d["risk_reasons"]:
                    diag["risk:" + why] += 1
            for sub, mode, hv in sb.pointer_stats(ex):
                diag["pointer:%s:%s" % (sub, "verb" if hv else "NO_VERB")] += 1
            for an in br["anomalies"]:
                anomalies[an.split(":")[0] if an.startswith("anchor") else an] += 1
            strata = ["ALL", "facts=" + ("present" if br["facts_present"] else "absent"), "label_A=" + a,
                      "block=" + block, "carrier=" + s.carrier_type, "subtype=" + s.subtype,
                      "multi_directive=" + str(len(br["directives"]) > 1)]
            if br["facts_present"] is False:
                strata.append("facts_absent&label_A=" + a)
            for st in strata:
                by_stratum[st][0] += 1
            confusion[(a, b)] += 1
            if a == b:
                agree += 1
                for st in strata:
                    by_stratum[st][1] += 1
            else:
                dis += 1
                c = classify(s, br, a)
                key = " | ".join("%s=%s" % (k, c[k]) for k in ("pair", "facts", "src", "kinds", "b_rules", "b_risk", "n_dir"))
                classes[key] += 1
        res["blocks"][block] = {"built": len(rows), "agree": agree, "disagree": dis, "build_report": {
            k: rep[k] for k in ("candidates", "kept", "kept_groups", "drops")}}
        tot["rows"] += len(rows)
        tot["agree"] += agree
        tot["dis"] += dis
    res["rows"] = tot["rows"]
    res["agreement"] = tot["agree"] / max(1, tot["rows"])
    res["disagree"] = tot["dis"]
    res["confusion"] = {"A=%s,B=%s" % k: v for k, v in sorted(confusion.items())}
    res["strata_agreement"] = {k: {"n": v[0], "agree": v[1], "pct": round(100.0 * v[1] / max(1, v[0]), 3)}
                               for k, v in sorted(by_stratum.items())}
    res["disagreement_classes"] = dict(classes.most_common())
    res["b_anomaly_counts"] = dict(anomalies.most_common())
    res["b_diagnostics"] = dict(sorted(diag.items()))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", default="s1")
    ap.add_argument("--blocks", default="train")
    ap.add_argument("--per-cell", type=int, default=12)
    ap.add_argument("--out", default=None, help="write the counts-only JSON here (use a temp dir)")
    a = ap.parse_args(argv)
    res = run(a.n, a.seed, tuple(a.blocks.split(",")), a.per_cell)
    txt = json.dumps(res, indent=1, sort_keys=True)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(txt + "\n")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())


# ---------------------------------------------------------------------------------------------------------------
# K6(i): exhaustive truth tables, driven through the lane's own truth harness (cases are rendered by the real renderer;
# only the rendered export reaches B). B's answer is adapted to the harness shape {label, directives: {did: {risk, label}}}.
# ---------------------------------------------------------------------------------------------------------------
def b_for_truth(export):
    sb = _load_b()
    schema = load_schema()
    necessary = {k: tuple(v) for k, v in schema["necessary_steps"].items()}
    r = sb.solve_b(export, necessary)
    return {"label": r["label"], "directives": {d["did"]: {"risk": d["risk"], "label": d["label"]} for d in r["directives"]}}


def run_truth(tables=("T1", "T2", "T3"), limit=None):
    from t41c import truth
    return truth.run_k6_truth(b_for_truth, tables=tables, limit=limit)
