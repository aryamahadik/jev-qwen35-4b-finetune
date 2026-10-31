"""Score runs on the JevBench v1.5.4 PUBLIC items with the v1.5 formulas (unofficial: our run, official formulas).

  python score_v154.py RUN [RUN ...] [--ref jev_p1] [--kinds gpu,api] [--prices 0.03,0.042] [--out-prices 0.15,0]
                       [--items all|A|B] [--type-weights equal|frozen] [--no-bootstrap]
  python score_v154.py --check-leaderboard       # recompute every published v1.5.4 row from its published parts

RUN is a folder name under bench/runs (results.jsonl + manifest.json) or a path to such a folder / results.jsonl.
All runs are scored on the items they have in common (the count is printed), so a subset run never mixes item sets.

What this is and is not:
  * Public items only: the 231 v1.2 items in the repository (easy 48 / standard 72 / hard 111; no judge items are
    published). The official v1.5.4 board scores 1,624 decisions (904 open, 601 published, + 720 sealed); the 370 new
    v1.5 open items are not in the public repository, so they cannot be run here.
  * Intelligence = I_open on these items: per type, per tier chance-corrected competence (Choice 1/options, Noul with the
    0.2/0.8 abstention band, Score nMAE vs uniform guessing), tier weights 10/20/(30)/40 renormalised over the present
    tiers, types weighted equally (headline A amendment). No sealed half, so no gap penalty. The INTELLIGENCE-ONLY number
    is the fair comparison with Jev (same items, same formula).
  * Calibration = typed calibration (Choice: ECE on hard items + TVD to gold_probs; Noul: ECE on P(yes);
    Score: normalised RPS + top-level ECE), equal type weights.
  * Speed = mean of speed points of p50 and p95 over the standard (+judge) items, self-hosted latency x2 + 0.15 s.
  * Cost = pooled tokens x price ($ per 1,000 decisions); our models use the frozen base-model reference price.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
sys.path.insert(0, str(HERE))
import v154lib as L  # noqa: E402

JB = BENCH / "jevbench_v154"
LEADERBOARD = HERE / "leaderboard_v154.json"


def load_run(spec):
    p = Path(spec)
    if not p.exists():
        p = BENCH / "runs" / spec
    if p.is_dir():
        res, man = p / "results.jsonl", p / "manifest.json"
    else:
        res, man = p, p.parent / "manifest.json"
    recs = {}
    for line in open(res):
        if line.strip():
            r = json.loads(line)
            recs[r["task_id"]] = r
    manifest = json.loads(man.read_text()) if man.exists() else {}
    return recs, manifest


def default_kind(manifest):
    if manifest.get("adapter") in ("typesafe", "openai_compat") or str(manifest.get("endpoint", "")).startswith("http"):
        return "api"
    return "gpu"


def score_run(outs, kind, price_in, price_out, type_w):
    intel, detail = L.intelligence_open(outs, type_w)
    intel_axis = max(0.0, min(100.0, intel))
    calib, cparts = L.calibration(outs, type_w)
    sp_items = [o["latency_s"] for o in outs if o["tier"] in ("standard", "judge") and o["latency_s"] is not None]
    all_lat = [o["latency_s"] for o in outs if o["latency_s"] is not None]
    p50, p95 = L.percentile(sp_items, 0.5), L.percentile(sp_items, 0.95)
    spd = L.speed(p50, p95, kind) if sp_items else None
    tin = sum((o["usage"].get("input_tokens") or 0) for o in outs) / len(outs)
    tout = sum((o["usage"].get("output_tokens") or 0) for o in outs) / len(outs)
    usd = (tin * price_in + tout * price_out) / 1e6 * 1000
    cst = L.cost(usd) if usd > 0 else None
    axes = {"intelligence": intel_axis, "calibration": calib, "speed": spd, "cost": cst}
    noul = [o for o in outs if o["type"] == "noul"]
    diag = {
        "argmax_correct_v14": sum(bool(o["correct"]) if o["type"] != "noul" else o["argmax_correct"] for o in outs),
        "noul_abstention_rate": L._mean(o["abstain"] for o in noul) if noul else None,
        "noul_cc_if_argmax": 100 * (L._mean(o["argmax_correct"] for o in noul) - 0.5) / 0.5 if noul else None,
        "invalid": sum(not o["valid"] for o in outs),
        "p50_all_s": L.percentile(all_lat, 0.5), "p95_all_s": L.percentile(all_lat, 0.95),
    }
    return {"n": len(outs), "I_open": intel, "types": detail, "axes": axes, "calibration_parts": cparts,
            "speed": {"kind": kind, "n": len(sp_items), "p50_s_raw": p50, "p95_s_raw": p95,
                      "p50_s_adjusted": L.adjusted_latency(p50, kind) if p50 else None,
                      "p95_s_adjusted": L.adjusted_latency(p95, kind) if p95 else None},
            "cost": {"input_tokens_per_decision": tin, "output_tokens_per_decision": tout, "price_in_per_m": price_in,
                     "price_out_per_m": price_out, "usd_per_1000": usd},
            "scores": L.composites(axes), "diagnostics": diag}


def fmt(x, w=5, d=1):
    return f"{x:{w}.{d}f}" if isinstance(x, (int, float)) else f"{'-':>{w}s}"


def leaderboard_context(names_scored):
    if not LEADERBOARD.exists():
        return
    d = json.loads(LEADERBOARD.read_text())
    sysm = {s["key"]: s for s in d["systems"]}
    print(f"\nPublished v1.5.4 board ({d['revision']}, {d['sample']['total']} decisions per system = "
          f"{d['sample']['open']} open + {d['sample']['sealed']} sealed; NOT the same item set as above):")
    order = d["board"]["A"]["order"]
    show = order[:5] + [k for k in ("jev-1.13.0", "plumb-4b", "decider-4b-v2", "decider-2b", "malkuth-2b")
                        if k not in order[:5]]
    print(f"  {'rank':>4s} {'system':34s} {'Score A':>7s} | {'I':>5s} {'C':>5s} {'S':>5s} {'$':>5s} | I_open I_sealed")
    for k in show:
        s = sysm.get(k)
        if not s or not s.get("axes"):
            continue
        ax, it = s["axes"], s.get("intelligence") or {}
        print(f"  {s.get('ranks', {}).get('A') or '-':>4} {s['display'][:34]:34s} {s['scores']['A']:7.2f} | "
              f"{fmt(ax['intelligence'])} {fmt(ax['calibration'])} {fmt(ax['speed'])} {fmt(ax['cost'])} | "
              f"{fmt(it.get('I_open'), 6)} {fmt(it.get('I_sealed'), 6)}")


def check_leaderboard():
    """Recompute each published row's axes and composites from its published parts (aggregation-level check of the
    formulas in v154lib; the per-item rules cannot be checked because sealed and most open items are private)."""
    d = json.loads(LEADERBOARD.read_text())
    g_med = d["G_med"]
    worst = {}
    n_rows = 0
    for s in d["systems"]:
        ax = s.get("axes") or {}
        it = s.get("intelligence")
        if not ax or not it or ax.get("intelligence") is None:
            continue
        n_rows += 1
        split_i = {}
        for split in ("open", "sealed"):
            ccs = {}
            for qt in L.TYPES:
                cell = it["per_type_split"].get(f"{split}|{qt}")
                if not cell:
                    continue
                tiers = {t: v for t, v in cell["tiers"].items() if (cell.get("n") or {}).get(t, 1) and v is not None}
                cc = L.wavg(tiers, L.TIER_W)
                worst["type_cc"] = max(worst.get("type_cc", 0), abs(cc - cell["cc"]))
                ccs[qt] = cc
            split_i[split] = L.wavg(ccs, L.TYPE_W["equal"])
        worst["I_open"] = max(worst.get("I_open", 0), abs(split_i["open"] - it["I_open"]))
        worst["I_sealed"] = max(worst.get("I_sealed", 0), abs(split_i["sealed"] - it["I_sealed"]))
        base = L.SEALED_SHARE * it["I_open"] + (1 - L.SEALED_SHARE) * it["I_sealed"]
        _, _, pen = L.overfit_penalty(it["I_open"], it["I_sealed"], g_med)
        worst["intelligence"] = max(worst.get("intelligence", 0), abs(max(0, min(100, base * pen)) - ax["intelligence"]))
        cp = (s.get("calibration") or {}).get("parts") or {}
        typed = {}
        for qt, p in cp.items():
            if qt == "choice":
                v = L.calib_choice(p.get("ece_hard"), p.get("mean_tvd"))
            elif qt == "noul":
                v = L.ece_score(p.get("ece"))
            else:
                v = L.calib_score(p["nrps"], p["top_ece"]) if p.get("nrps") is not None else None
            if v is not None and p.get("score") is not None:
                worst["calib_part"] = max(worst.get("calib_part", 0), abs(v - p["score"]))
            typed[qt] = p.get("score")
        sup = [qt for qt, v in (s.get("support") or {}).items() if v not in (None, "not supported", "unsupported")]
        c = L.wavg({qt: (typed.get(qt) or 0.0) for qt in sup}, L.TYPE_W["equal"]) if sup else None
        if c is not None and ax.get("calibration") is not None:
            worst["calibration"] = max(worst.get("calibration", 0), abs(c - ax["calibration"]))
        sp = s.get("speed") or {}
        if sp.get("p50_s_adjusted") and ax.get("speed") is not None:
            v = (L.speed_point(sp["p50_s_adjusted"]) + L.speed_point(sp["p95_s_adjusted"])) / 2
            worst["speed"] = max(worst.get("speed", 0), abs(v - ax["speed"]))
        cs = s.get("cost") or {}
        if cs.get("usd_per_1000") and ax.get("cost") is not None:
            worst["cost"] = max(worst.get("cost", 0), abs(L.cost(cs["usd_per_1000"]) - ax["cost"]))
        comp = L.composites(ax)
        for k in ("A", "B", "C"):
            if (s.get("scores") or {}).get(k) is not None:
                worst[f"score_{k}"] = max(worst.get(f"score_{k}", 0), abs(comp[k] - s["scores"][k]))
        for k, v in (s.get("views") or {}).items():
            if v is not None and comp.get(k) is not None:
                worst["views"] = max(worst.get("views", 0), abs(comp[k] - v))
    print(f"v1.5.4 leaderboard recompute over {n_rows} rows with published axes (max |ours - published|):")
    for k, v in worst.items():
        print(f"  {k:14s} {v:.2e}  {'OK' if v < 1e-6 else 'MISMATCH'}")
    return all(v < 1e-6 for v in worst.values())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="*")
    ap.add_argument("--ref", default=None, help="run for the paired bootstrap (default: the first run)")
    ap.add_argument("--kinds", default=None, help="api|gpu|demo per run (default: from the manifest)")
    ap.add_argument("--prices", default=None, help="$/M input tokens per run (default: api 0.042, gpu 0.03)")
    ap.add_argument("--out-prices", default=None, help="$/M output tokens per run (default: api 0, gpu 0.15)")
    ap.add_argument("--items", default="all", help="all | A | B | path to a jsonl of ids")
    ap.add_argument("--type-weights", default="equal", choices=list(L.TYPE_W))
    ap.add_argument("--jevbench", default=str(JB))
    ap.add_argument("--no-bootstrap", action="store_true")
    ap.add_argument("--check-leaderboard", action="store_true")
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    if a.check_leaderboard:
        ok = check_leaderboard()
        if not a.runs:
            sys.exit(0 if ok else 1)
    if not a.runs:
        ap.error("give at least one run")
    split = None if a.items == "all" else (a.items if Path(a.items).exists() else BENCH / f"splits/jevbench_{a.items}.jsonl")
    items = L.load_public(a.jevbench, split)
    runs = {}
    for spec in a.runs:
        recs, man = load_run(spec)
        runs[Path(spec).name if Path(spec).is_dir() else spec] = (recs, man)
    names = list(runs)
    common = sorted(set(items).intersection(*[set(r) for r, _ in runs.values()]))
    kinds = a.kinds.split(",") if a.kinds else [default_kind(runs[n][1]) for n in names]
    pin = [float(x) for x in a.prices.split(",")] if a.prices else \
        [L.JEV_LIST[0] if k == "api" else L.QWEN35_4B_REF[0] for k in kinds]
    pout = [float(x) for x in a.out_prices.split(",")] if a.out_prices else \
        [L.JEV_LIST[1] if k == "api" else L.QWEN35_4B_REF[1] for k in kinds]
    outs = {n: [L.item_outcome(items[i], runs[n][0][i]) for i in common] for n in names}
    res = {n: score_run(outs[n], k, pi, po, a.type_weights) for n, k, pi, po in zip(names, kinds, pin, pout)}
    tiers_present = sorted({items[i]["tier"] for i in common}, key=L.TIERS.index)
    print(f"JevBench v1.5.4 formulas on PUBLIC items: n={len(common)} common items ({a.items}), tiers {tiers_present}; "
          f"type weights {a.type_weights}.\nUnofficial: our run of the public items with the official formulas; not a "
          f"leaderboard position (no sealed half, no judge tier, no gap penalty).\n")
    print(f"{'run':26s} {'kind':4s} | {'INTEL':>5s} | {'Calib':>5s} {'Speed':>5s} {'Cost':>5s} | {'Score A':>7s} "
          f"{'B':>6s} {'C':>6s} | {'p50/p95 adj ms':>15s} {'$/1k':>7s} | v1.4 argmax")
    for n in names:
        r = res[n]
        ax, sc, sp = r["axes"], r["scores"], r["speed"]
        lat = f"{sp['p50_s_adjusted'] * 1000:.0f}/{sp['p95_s_adjusted'] * 1000:.0f}" if sp["p50_s_adjusted"] else "-"
        print(f"{n[:26]:26s} {r['speed']['kind']:4s} | {fmt(ax['intelligence'])} | {fmt(ax['calibration'])} "
              f"{fmt(ax['speed'])} {fmt(ax['cost'])} | {fmt(sc['A'], 7, 2)} {fmt(sc['B'], 6, 2)} {fmt(sc['C'], 6, 2)} | "
              f"{lat:>15s} {r['cost']['usd_per_1000']:7.4f} | {r['diagnostics']['argmax_correct_v14']}/{r['n']}")
    print("\nIntelligence detail (chance-corrected competence per type; tiers easy/standard/hard; n in brackets):")
    for n in names:
        r = res[n]
        cells = []
        for qt in L.TYPES:
            d = r["types"].get(qt)
            if not d:
                continue
            tv = " ".join(f"{fmt(d['tiers'][t], 5)}[{d['n'][t]}]" for t in L.TIERS if d["n"][t])
            cells.append(f"{qt} {d['cc']:5.1f} ({tv})")
        dg = r["diagnostics"]
        print(f"  {n[:26]:26s} " + " | ".join(cells))
        print(f"  {'':26s} noul abstention {100 * (dg['noul_abstention_rate'] or 0):.1f}% (0.2<P(yes)<0.8 counts "
              f"wrong); noul CC if argmax {fmt(dg['noul_cc_if_argmax'])}; invalid {dg['invalid']}")
    print("\nCalibration parts:")
    for n in names:
        cp = res[n]["calibration_parts"]
        c, no, s = cp.get("choice", {}), cp.get("noul", {}), cp.get("score", {})
        print(f"  {n[:26]:26s} choice {fmt(c.get('score'))} (ECE_hard {fmt(c.get('ece_hard'), 5, 3)}, TVD "
              f"{fmt(c.get('mean_tvd'), 5, 3)} n={c.get('n_tvd')}) | noul {fmt(no.get('score'))} (ECE {fmt(no.get('ece'), 5, 3)}, "
              f"Brier {fmt(no.get('brier'), 5, 3)}) | score {fmt(s.get('score'))} (nRPS {fmt(s.get('nrps'), 5, 3)}, "
              f"topECE {fmt(s.get('top_ece'), 5, 3)})")
    ref = a.ref or names[0]
    if len(names) > 1 and not a.no_bootstrap:
        bs = L.paired_bootstrap_intel(outs, ref, type_w=a.type_weights)
        print(f"\nPaired stratified bootstrap (type x tier, B=2000, seed 15) of the public INTELLIGENCE difference vs {ref}:")
        for n, b in bs.items():
            dlt = res[n]["axes"]["intelligence"] - res[ref]["axes"]["intelligence"]
            tie = b["ci95"][0] <= 0 <= b["ci95"][1]
            print(f"  {n[:26]:26s} {dlt:+6.1f} [{b['ci95'][0]:+.1f}, {b['ci95'][1]:+.1f}]  P(better) {b['p_better']:.3f}"
                  f"  {'statistical tie' if tie else ('better' if dlt > 0 else 'worse')}")
            res[n]["paired_vs_" + ref] = {"diff": dlt, **b}
    leaderboard_context(names)
    if a.json_out:
        Path(a.json_out).write_text(json.dumps({"items": a.items, "n": len(common), "runs": res}, indent=1, default=float))


if __name__ == "__main__":
    main()
