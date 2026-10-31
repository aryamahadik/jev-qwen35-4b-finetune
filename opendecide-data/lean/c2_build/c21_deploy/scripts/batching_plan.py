"""batching_plan.py: how to keep utilisation above the break-even (about 59%) at the expected load, from a measured capacity
curve (CPU, stdlib; output tagged "modelled" from author-run inputs).

Definitions (the same as cost_calc.py / the C1 cost table):
  utilisation u = served decisions per hour / T_sat, T_sat = the instance's sustained saturated throughput on the call mix
  ($/1K = rate / (T_sat u) * 1000, so u below the break-even u* = cost_at_100% / Jev $/1K means Jev is cheaper).
The capacity curve is the closed-loop ladder from capacity_ladder.py: for each concurrency c the decisions/hour T(c) and the
server-side per-decision latency p50/p95 (loopback client, so no network). Open-loop operating point at a throughput r: the
smallest ladder concurrency whose T(c) >= r (Little's law: an open system at throughput r sits at the concurrency whose
closed-loop throughput is r); its latency is the measured latency at that c (conservative: next-higher ladder point).

Three things come out:
 1. UTILISATION CEILING UNDER THE SLO: the highest throughput whose measured p95 stays within the latency SLO, as a share of
    T_sat. If this ceiling is below u*, no amount of traffic makes the instance beat Jev on cost while meeting the SLO: the only
    levers left are the three below. If it is above u*, the instance needs at least u* x T_sat of load to pay.
 2. PER-SCENARIO TABLE: for N = 1.. instances (fixed pool, load balanced), the mean utilisation over the scenario's day, the share
    of hours at or above u*, the peak p95, and the background (latency-insensitive) traffic per hour that would lift the mean to u*.
 3. THE LEVERS, with the numbers each needs: right-size N to the load (autoscaling on the busy hours, a warm floor of 1 off-peak),
    pool all customers on one fleet (multiplexing), and fill the gaps with a lower-priority class (evals, nearline, retries;
    LinkedIn reports about +25% effective throughput from this shaping; their figure, not ours) so interactive traffic keeps its
    headroom while the GPU stays busy. Multi-question calls are cheaper per decision (H100 batch-8: 11.3 ms vs 32 ms at batch 1,
    author-run 17 Oct); the ladder measures per decision, so an agent that bundles its questions moves right on the curve.

  batching_plan.py plan --curves inputs/capacity_curves.json --curve h100_s1_modal_reference \\
       --scenarios inputs/warm_pool_inputs.json --u-star 0.59 --slo-p95-ms 60 --out out/batching_plan.json --md out/batching_plan.md
  batching_plan.py validate --curves ... --curve NAME --openloop out/openloop_L4.json   (model vs the M3 open-loop runs)
  batching_plan.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import warm_pool_sim as W  # noqa: E402


# ------------------------------------------------------------------ curve helpers
def points_of(curve: dict) -> list:
    pts = [p for p in curve.get("points", []) if p.get("dph") is not None]
    return sorted(pts, key=lambda p: p["c"])


def t_sat(curve: dict) -> float | None:
    pts = points_of(curve)
    return max(p["dph"] for p in pts) if pts else None


def op_point(curve: dict, dph: float) -> dict | None:
    """The first ladder point whose throughput is at least `dph` (conservative); None above the saturated throughput."""
    for p in points_of(curve):
        if p["dph"] >= dph:
            return p
    return None


def ceiling(curve: dict, slo_p95_ms: float) -> dict:
    pts = points_of(curve)
    ts = t_sat(curve)
    if not pts or any(p.get("p95_ms") is None for p in pts):
        return {"computable": False, "why": "need a measured p95 at every ladder point (capacity_ladder.py)"}
    ok = [p for p in pts if p["p95_ms"] <= slo_p95_ms]
    if not ok:
        return {"computable": True, "c": None, "dph": 0.0, "share_of_sat": 0.0, "slo_p95_ms": slo_p95_ms,
                "note": "even the lowest ladder level misses the SLO"}
    best = max(ok, key=lambda p: p["dph"])
    return {"computable": True, "c": best["c"], "dph": best["dph"], "share_of_sat": round(best["dph"] / ts, 4),
            "slo_p95_ms": slo_p95_ms}


# ------------------------------------------------------------------ scenario table
def day_rates(spec: dict, step_s: float = 60.0, days: int = 7) -> list:
    f = W.rate_fn(spec)
    n = int(days * 86400 / step_s)
    return [f(i * step_s + step_s / 2) for i in range(n)]       # decisions per second


def table_for(curve: dict, spec: dict, u_star: float, slo_p95_ms: float | None, n_max: int = 12) -> dict:
    ts = t_sat(curve)
    rates = day_rates(spec)
    mean_dph = sum(rates) / len(rates) * 3600.0
    peak_dph = max(rates) * 3600.0
    rows = []
    for n in range(1, n_max + 1):
        per = [r * 3600.0 / n for r in rates]                   # per-instance dph at each minute
        us = [min(x / ts, 1.0) for x in per]
        saturated = sum(1 for x in per if x > ts) / len(per)
        mean_u = sum(us) / len(us)
        hrs_ge = sum(1 for u in us if u >= u_star) / len(us)
        op = op_point(curve, peak_dph / n)
        p95 = op.get("p95_ms") if op else None
        fill = max(0.0, u_star * ts * n - mean_dph)             # background decisions/hour to lift the mean to u*
        rows.append({"n": n, "mean_util": round(mean_u, 4), "share_time_util_ge_ustar": round(hrs_ge, 4),
                     "share_time_overloaded": round(saturated, 4), "peak_p95_ms": p95,
                     "peak_over_capacity": peak_dph / n > ts, "background_fill_dph_to_reach_ustar": round(fill),
                     "meets_slo_at_peak": None if (slo_p95_ms is None or p95 is None) else p95 <= slo_p95_ms})
        if mean_u < 0.005 and n > 3:
            break
    n_needed = next((r["n"] for r in rows if not r["peak_over_capacity"] and r["meets_slo_at_peak"] is not False), None)
    return {"mean_dph": round(mean_dph), "peak_dph": round(peak_dph), "peak_dec_per_s": round(peak_dph / 3600.0, 2),
            "n_min_for_peak": n_needed, "rows": rows}


def min_load_for_ustar(curve: dict, u_star: float) -> dict:
    ts = t_sat(curve)
    return {"dph": round(ts * u_star), "dec_per_s": round(ts * u_star / 3600.0, 2)} if ts else {}


def validate(curve: dict, openloop: dict) -> dict:
    """openloop: {"levels": [{"target_dph", "ok", "calls", "p50_ms", "p95_ms", "p99_ms", "util"?}]} from the M3 run."""
    out = []
    for lv in openloop["levels"]:
        op = op_point(curve, lv["target_dph"])
        out.append({"target_dph": lv["target_dph"], "model_p50_ms": op.get("p50_ms") if op else None,
                    "model_p95_ms": op.get("p95_ms") if op else None, "measured_p50_ms": lv.get("p50_ms"),
                    "measured_p95_ms": lv.get("p95_ms"), "measured_p99_ms": lv.get("p99_ms"),
                    "calls": lv.get("calls"), "ok": lv.get("ok"),
                    "p95_ratio_measured_over_model": (round(lv["p95_ms"] / op["p95_ms"], 2) if op and op.get("p95_ms") and lv.get("p95_ms") else None)})
    return {"levels": out, "note": "ratio near or below 1 = the closed-loop model is a safe (conservative) predictor of open-loop latency"}


# ------------------------------------------------------------------ cli
def check_curve(curve: dict) -> list:
    t = curve.get("tag")
    bad = []
    if t not in C.KINDS:
        bad.append("curve has no valid tag")
    elif t == "author-run" and not (isinstance(curve.get("n_per_point"), int) and curve.get("source")):
        bad.append("an author-run curve needs n_per_point and source")
    return bad


def render_md(res: dict) -> str:
    L = [f"# Batching plan ({res['tag']['tag']}) curve `{res['curve']}`", "",
         f"Curve tag: {res['curve_tag']}. u* = {res['u_star']} (break-even vs Jev; cost_calc.py computes it from rate and T_sat). "
         f"T_sat = {res['t_sat_dph']:,} decisions/h; one instance needs {res['min_load_for_ustar']['dph']:,} decisions/h "
         f"({res['min_load_for_ustar']['dec_per_s']} per second) to stay at u*.", ""] + [f"WARNING: {w}" for w in res["warnings"]] + [""]
    c = res["ceiling"]
    if c.get("computable"):
        L += [f"SLO server p95 <= {c['slo_p95_ms']} ms: utilisation ceiling = {c['share_of_sat']} of T_sat (ladder c = {c['c']}). " +
              ("This is BELOW u*: interactive traffic alone cannot reach break-even within the SLO; use the levers." if c["share_of_sat"] < res["u_star"] else
               "This is above u*: an instance loaded between u* and the ceiling both meets the SLO and beats Jev."), ""]
    else:
        L += [f"SLO ceiling: not computable ({c['why']}).", ""]
    for name, t in res["scenarios"].items():
        L += [f"## {name}", f"mean {t['mean_dph']:,} dph, peak {t['peak_dec_per_s']} dec/s; instances needed for the peak: {t['n_min_for_peak']}", "",
              C.md_table(["N", "mean util", "time at util >= u*", "time overloaded", "peak p95 ms", "meets SLO at peak", "background fill dph to reach u*"],
                         [[r["n"], r["mean_util"], r["share_time_util_ge_ustar"], r["share_time_overloaded"], r["peak_p95_ms"],
                           r["meets_slo_at_peak"], f"{r['background_fill_dph_to_reach_ustar']:,}"] for r in t["rows"]]), ""]
    return "\n".join(L)


def selftest() -> None:
    curve = {"tag": "assumed", "points": [{"c": 1, "dph": 100000, "p50_ms": 30, "p95_ms": 40}, {"c": 4, "dph": 200000, "p50_ms": 70, "p95_ms": 90},
                                          {"c": 16, "dph": 300000, "p50_ms": 190, "p95_ms": 260}]}
    assert t_sat(curve) == 300000
    c = ceiling(curve, 100)
    assert c["c"] == 4 and abs(c["share_of_sat"] - 2 / 3) < 1e-3, c
    assert op_point(curve, 150000)["c"] == 4 and op_point(curve, 400000) is None
    t = table_for(curve, {"kind": "constant", "rate_per_s": 50.0}, 0.59, 100, n_max=3)   # 180000 dph
    assert t["rows"][0]["mean_util"] == 0.6 and t["rows"][0]["share_time_util_ge_ustar"] == 1.0 and t["n_min_for_peak"] == 1, t
    assert t["rows"][1]["mean_util"] == 0.3
    print("selftest ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", nargs="?", choices=("plan", "validate"))
    ap.add_argument("--curves", default=str(C.ROOT / "inputs" / "capacity_curves.json"))
    ap.add_argument("--curve", default="h100_s1_modal_reference")
    ap.add_argument("--scenarios", default=str(C.ROOT / "inputs" / "warm_pool_inputs.json"))
    ap.add_argument("--scenario", default="all")
    ap.add_argument("--u-star", type=float, default=0.59)
    ap.add_argument("--slo-p95-ms", type=float, default=None, help="server-side p95 SLO per decision (ASSUMED until the owner sets it)")
    ap.add_argument("--openloop")
    ap.add_argument("--out"), ap.add_argument("--md")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    if not a.cmd:
        ap.error("plan or validate")
    curve = json.loads(Path(a.curves).read_text())["curves"][a.curve]
    bad = check_curve(curve)
    if bad:
        raise SystemExit("; ".join(bad))
    if t_sat(curve) is None:
        raise SystemExit(f"curve {a.curve!r} has no measured points (not-measured): run capacity_ladder.py (M2) first")
    if a.cmd == "validate":
        res = {"tag": C.tag("modelled", source="batching_plan.py validate"), **validate(curve, json.loads(Path(a.openloop).read_text()))}
        if a.out:
            C.write_json(a.out, res)
        print(json.dumps(res, indent=1))
        return 0
    scen = json.loads(Path(a.scenarios).read_text())["scenarios"]
    scen = [s for s in scen if a.scenario in ("all", s["name"])]
    res = {"tag": C.tag("modelled", source="batching_plan.py plan; closed-loop ladder -> open-loop operating point", u_star=a.u_star),
           "curve": a.curve, "curve_tag": {k: curve.get(k) for k in ("tag", "n_per_point", "source", "mix")},
           "u_star": a.u_star, "t_sat_dph": t_sat(curve), "min_load_for_ustar": min_load_for_ustar(curve, a.u_star),
           "ceiling": ceiling(curve, a.slo_p95_ms) if a.slo_p95_ms else {"computable": False, "why": "no --slo-p95-ms given"},
           "scenarios": {s["name"]: table_for(curve, s, a.u_star, a.slo_p95_ms) for s in scen}, "utc": C.utc(),
           "warnings": ([f"the curve has only {len(points_of(curve))} measured points (fewer than 5): the operating point is a coarse "
                         f"step function; rerun with the full ladder"] if len(points_of(curve)) < 5 else []),
           "caveat": "scenarios are ASSUMED; the open-loop point comes from a closed-loop ladder (validate it with the M3 run)"}
    if a.out:
        C.write_json(a.out, res)
    md = render_md(res)
    if a.md:
        Path(a.md).parent.mkdir(parents=True, exist_ok=True)
        Path(a.md).write_text(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
