"""r2_report.py: parity of a trial's answers vs the fresh L4 BF16 baseline, and the offline margin-gate replay.

Pure Python (stdlib). Counts and numbers only: no row text is ever written. Row ids appear only as short hashes.

  python3 r2_report.py parity  REF.jsonl CAND.jsonl [--out FILE]      # answers_P.jsonl of two runs
  python3 r2_report.py gate    REF.jsonl FP8.jsonl BF16RERUN.jsonl [--out FILE]   # fit tau on a hash half, test on the other

Definitions (hosting/speed_bench.compare = oc1.parity): answer = probabilities per row; argmax: yes/no -> p_yes > 0.5,
choice -> max over the options (first on a tie); a missing answer is a disagreement. Wilson = 95% interval of the agreement.
Bar: Wilson LOWER bound >= 0.995 on the full set (8,143). Per-bucket and per-view-type rows are reported with their own
Wilson bound; a bucket whose size cannot reach 0.995 even at 100% agreement is flagged UNDERPOWERED (its bound is not a pass/fail).
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                       # copy of ../r2_report.py for the H100 window (h100/)
P_PATH = HERE.parents[2] / "speed" / "opt_c1_20261017" / "data" / "P.jsonl"      # read-only 17 Oct workload (dev rows)
BAR = 0.995


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def load_items():
    items = {}
    with open(P_PATH) as f:
        for line in f:
            if not line.strip():
                continue
            it = json.loads(line)
            q = next(iter(it["request"]["questions"].values()))
            items[it["id"]] = {"bucket": it["bucket"], "qtype": it["qtype"], "options": q.get("options") if q["type"] == "choice" else None}
    return items


def load_answers(path):
    out = {}
    with open(path) as f:
        for line in f:
            if line.strip():
                d = json.loads(line)
                out[d["id"]] = d
    return out


def top(opts, p):
    if opts is None:
        return float(p.get("yes", 0.0)) > 0.5
    vals = {o: float(p.get(o, 0.0)) for o in opts}
    return max(vals, key=vals.get)


def margin(opts, p):
    if opts is None:
        return abs(2.0 * float(p.get("yes", 0.0)) - 1.0)
    v = sorted((float(p.get(o, 0.0)) for o in opts), reverse=True)
    return v[0] - v[1] if len(v) > 1 else v[0]


def dp(opts, a, b):
    keys = ["yes", "no"] if opts is None else list(opts)
    return max(abs(float(a.get(k, 0.0)) - float(b.get(k, 0.0))) for k in keys)


def hid(s):
    return hashlib.sha1(s.encode()).hexdigest()[:8]


def group_stats(rows):
    n = len(rows)
    k = sum(r["same"] for r in rows)
    lo, hi = wilson(k, n)
    fl = [r for r in rows if not r["same"]]
    return {"n": n, "agree": k, "flips": n - k, "agree_rate": round(k / n, 6) if n else None,
            "wilson95": [round(lo, 6), round(hi, 6)],
            "underpowered": bool(n and wilson(n, n)[0] < BAR),
            "pass_wilson": bool(n and lo >= BAR),
            "max_dp": round(max((r["dp"] for r in rows), default=0.0), 6),
            "flip_ref_margin_median": round(sorted(f["ref_margin"] for f in fl)[len(fl) // 2], 4) if fl else None,
            "flip_ref_margin_max": round(max((f["ref_margin"] for f in fl), default=0.0), 4) if fl else None}


def parity(ref, cand, items):
    rows = []
    for i, it in items.items():
        r = ref.get(i)
        if r is None:
            continue
        c = cand.get(i)
        o = it["options"]
        if c is None:
            rows.append({"id": i, "bucket": it["bucket"], "qtype": it["qtype"], "same": False, "dp": 1.0, "ref_margin": margin(o, r["probs"]),
                         "cand_margin": None, "missing": True, "views": None})
            continue
        same = top(o, c["probs"]) == top(o, r["probs"])
        vs = None
        if o is not None and r.get("views") and c.get("views"):
            vs = [top(o, a) == top(o, b) for a, b in zip(r["views"], c["views"])]
        rows.append({"id": i, "bucket": it["bucket"], "qtype": it["qtype"], "same": same, "dp": dp(o, c["probs"], r["probs"]),
                     "ref_margin": margin(o, r["probs"]), "cand_margin": margin(o, c["probs"]), "missing": False, "views": vs})
    rep = {"overall": group_stats(rows), "missing": sum(r["missing"] for r in rows)}
    rep["by_bucket"] = {b: group_stats([r for r in rows if r["bucket"] == b]) for b in sorted({r["bucket"] for r in rows})}
    rep["by_view_type"] = {t: group_stats([r for r in rows if r["qtype"] == t]) for t in sorted({r["qtype"] for r in rows})}
    ch = [r for r in rows if r["views"]]
    rep["choice_per_view_argmax_agree"] = {
        f"view{v}": {"n": len(ch), "agree": sum(r["views"][v] for r in ch)} for v in (0, 1) if ch and len(ch[0]["views"]) > v}
    fl = [r for r in rows if not r["same"]]
    rep["flips"] = {"n": len(fl), "ref_margin_le": {str(e): sum(1 for r in fl if r["ref_margin"] <= e) for e in (0.005, 0.01, 0.02, 0.05, 0.1)},
                    "examples": [{"h": hid(r["id"]), "bucket": r["bucket"], "ref_margin": round(r["ref_margin"], 4),
                                  "cand_margin": None if r["cand_margin"] is None else round(r["cand_margin"], 4), "dp": round(r["dp"], 4)}
                                 for r in sorted(fl, key=lambda r: -r["ref_margin"])[:15]]}
    dps = sorted(r["dp"] for r in rows if not r["missing"])
    rep["dp"] = {"mean": round(sum(dps) / len(dps), 7) if dps else None, "p99": round(dps[int(0.99 * (len(dps) - 1))], 6) if dps else None,
                 "max": round(dps[-1], 6) if dps else None}
    rep["verdict"] = ("PASS" if rep["overall"]["pass_wilson"] else "FAIL") + (
        "" if all(g["pass_wilson"] or g["underpowered"] for g in rep["by_view_type"].values()) else " (a view type is below the bar)")
    return rep, rows


def gate_replay(ref, fp8, rerun, items, taus=None, fit_target=0.998):
    """Final answer = FP8 answer when its own margin >= tau, else the BF16 re-run's answer; agreement vs `ref`.
    tau is fitted on one hash half (the smallest tau on the grid whose fit-half Wilson lower bound >= 0.998) and tested
    on the other half; both directions are reported."""
    ids = [i for i in items if i in ref and i in fp8 and i in rerun]
    half = {i: int(hashlib.sha1(i.encode()).hexdigest(), 16) & 1 for i in ids}
    grid = taus or [round(0.005 * j, 3) for j in range(0, 121)]

    def run(sub, tau):
        flips = deferred = 0
        for i in sub:
            o = items[i]["options"]
            m = margin(o, fp8[i]["probs"])
            final = fp8[i]["probs"] if m >= tau else rerun[i]["probs"]
            deferred += m < tau
            flips += top(o, final) != top(o, ref[i]["probs"])
        n = len(sub)
        lo, hi = wilson(n - flips, n)
        return {"n": n, "tau": tau, "deferred": deferred, "deferral_share": round(deferred / n, 4), "flips": flips,
                "agree_rate": round((n - flips) / n, 6), "wilson_lb": round(lo, 6)}

    out = {"n": len(ids), "no_gate_fp8": run(ids, 0.0), "all_bf16_rerun_vs_ref": run(ids, 1.1),
           "fixed_tau": {str(t): run(ids, t) for t in (0.05, 0.1, 0.15, 0.2, 0.3)}, "split_half": {}}
    for fit_h in (0, 1):
        fit = [i for i in ids if half[i] == fit_h]
        test = [i for i in ids if half[i] != fit_h]
        tau = next((t for t in grid if run(fit, t)["wilson_lb"] >= fit_target), None)
        if tau is None:
            out["split_half"][f"fit{fit_h}"] = {"tau": None, "note": f"no tau on the grid reaches fit-half Wilson LB {fit_target}"}
            continue
        out["split_half"][f"fit{fit_h}"] = {"tau": tau, "fit": run(fit, tau), "test": run(test, tau)}
    # a single tau for the full set: the larger of the two fitted taus (conservative)
    taus_f = [v["tau"] for v in out["split_half"].values() if v.get("tau") is not None]
    if taus_f:
        out["full_set_at_max_fitted_tau"] = run(ids, max(taus_f))
    return out


def main(argv):
    if len(argv) < 3 or argv[0] not in ("parity", "gate"):
        raise SystemExit(__doc__)
    items = load_items()
    out_path = None
    if "--out" in argv:
        j = argv.index("--out")
        out_path = argv[j + 1]
        argv = argv[:j] + argv[j + 2:]
    if argv[0] == "parity":
        rep, _ = parity(load_answers(argv[1]), load_answers(argv[2]), items)
    else:
        rep = gate_replay(load_answers(argv[1]), load_answers(argv[2]), load_answers(argv[3]), items)
    s = json.dumps(rep, indent=1)
    if out_path:
        Path(out_path).write_text(s)
    print(s)


if __name__ == "__main__":
    main(sys.argv[1:])
