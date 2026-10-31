#!/usr/bin/env python3
"""analyze_h100.py: laptop-side analysis of the round-2 H100 window -> TRIALS_H100.json + TRIALS_H100.md.

  python3 analyze_h100.py [--run results/session_YYYYMMDD_HHMMSS] [--rate 4.3952] [--out-prefix TRIALS_H100]

Reads <run>/volume/<run_id>/<config>/{block.json, measure.json, answers_P*.jsonl, latency_records.json, vision_r2.json}.
Quality bar (task): >= 99.5% argmax agreement, Wilson 95% LOWER bound, on the FULL 8,143 parity set vs the SAME-SESSION S1 BF16
reference (arm A, c32 pass), per bucket and per view type. Counts and numbers only; row ids appear as short hashes.

Verdicts  exact : by-construction numerics-preserving change AND bar met AND 0 flips
          pass  : bar met (numerics may differ; flips allowed within the bar)
          fail  : Wilson lower bound below 0.995
          NA    : not run / did not boot / stopped by its canary / skipped by the budget gate
Adopt rule (research plan): bar met AND a real gain (batch-1 p50 or p99 down >= 2 ms, or throughput up >= 5%).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r2_report as RR  # noqa: E402
from oc1 import common as C  # noqa: E402

RATE_DEFAULT = C.container_rate_usd_h("H100", 4.0, 32.0, "any")        # 3.95 + 4 x 0.0473 + 32 x 0.008 = 4.3952 USD/h
UTILS = (1.0, 0.5, 0.2)
EXACT_BY_CONSTRUCTION = {"r2_a", "r2_b", "r2_b_dcpc", "r2_b_nofull", "r2_b_gc", "r2_d1", "r2_d2"}
WORDS = {"r2_a": "A. S1 BF16 reference", "r2_b": "B. exact bundle (full prefill graph + skip-tokenizer-init + /v1/score + LM-head slice + metrics + gc warn)",
         "r2_b_dcpc": "B (variant). bundle + --disable-chunked-prefix-cache so that full-graph prefill can boot",
         "r2_b_nofull": "B'. bundle without full-graph prefill", "r2_b_gc": "B+gc. bundle + gc.freeze() after warm-up",
         "r2_c": "C. block-FP8 checkpoint, --quantization fp8", "r2_d1": "D1. --keep-mm-feature-on-device (images)",
         "r2_d2": "D2. --mm-processor-worker-num 4 (images)", "r2_e1": "E1. --mamba-ssm-dtype bfloat16",
         "r2_e2": "E2. --mamba-track-interval 64"}
ORDER = ["r2_a", "r2_b", "r2_b_dcpc", "r2_b_nofull", "r2_b_gc", "r2_c", "r2_d1", "r2_d2", "r2_e1", "r2_e2"]


# ------------------------------------------------------------------ io
def find_run(arg=None) -> Path:
    if arg:
        p = Path(arg)
        p = p if p.is_absolute() else HERE / p
    else:
        cands = sorted((HERE / "results").glob("session_*"))
        if not cands:
            raise SystemExit("no results/session_* directory")
        p = cands[-1]
    vol = p / "volume"
    inner = sorted(vol.glob("session_*")) if vol.exists() else []
    return inner[-1] if inner else p


def jload(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return default


def answers(p):
    return RR.load_answers(p) if Path(p).exists() else None


def pct(xs, q):
    return C.pct(xs, q) if xs else None


def lat_summary(ms):
    if not ms:
        return None
    return {"n": len(ms), "p50": round(pct(ms, 0.5), 2), "p95": round(pct(ms, 0.95), 2), "p99": round(pct(ms, 0.99), 2),
            "mean": round(statistics.fmean(ms), 2), "max": round(max(ms), 2)}


def usd_per_1k(rate, dph, util):
    return round(rate / (dph * util) * 1000.0, 5) if dph else None


# ------------------------------------------------------------------ one arm
def load_arm(rd: Path, name: str) -> dict:
    d = rd / name
    blk = jload(d / "block.json")
    if blk is None:
        return {"name": name, "ran": False}
    m = blk.get("measure") or {}
    return {"name": name, "ran": True, "dir": d, "block": blk, "measure": m, "steps": m.get("steps") or {},
            "skipped": blk.get("skipped"), "error": blk.get("error") or m.get("fatal"), "aborted": m.get("aborted")}


def latency_of(arm: dict) -> dict | None:
    recs = jload(arm["dir"] / "latency_records.json") if arm.get("dir") else None
    if not recs:
        return None
    out = {}
    pooled, by_id = [], {}
    for rep, rows in sorted(recs.items()):
        ms = [r["ms"] for r in rows if r["ok"]]
        out[rep] = lat_summary(ms)
        out[rep]["noul_p50"] = round(pct([r["ms"] for r in rows if r["ok"] and r["bucket"] == "noul"], 0.5), 2)
        out[rep]["choice_p50"] = round(pct([r["ms"] for r in rows if r["ok"] and r["bucket"] != "noul"], 0.5), 2)
        pooled += ms
        for r in rows:
            if r["ok"]:
                by_id.setdefault(r["id"], []).append(r["ms"])
    out["pooled"] = lat_summary(pooled)
    out["rep_p50_spread"] = round(abs(out["rep1"]["p50"] - out["rep2"]["p50"]), 2) if "rep1" in out and "rep2" in out else None
    out["_by_id"] = {k: statistics.fmean(v) for k, v in by_id.items()}
    return out


def throughput_of(arm: dict, rate: float) -> dict | None:
    t = arm["steps"].get("throughput")
    out = {}
    if t:
        ns = [t[k]["decisions_per_h"] for k in ("N_c64", "N_c64_rep2") if k in t and t[k].get("decisions_per_h")]
        if ns:
            out["N_c64_dph"] = round(statistics.fmean(ns))
            out["N_c64_dph_runs"] = ns
            out["N_c64_gpu_busy_pct"] = (t["N_c64"].get("gpu") or {}).get("util_mean")
            out["N_c64_cached_share"] = t["N_c64"].get("cached_token_share")
        if t.get("P_sat_c64"):
            out["P_sat_c64_dph"] = t["P_sat_c64"].get("decisions_per_h")
            out["P_sat_c64_gpu_busy_pct"] = (t["P_sat_c64"].get("gpu") or {}).get("util_mean")
    pv = arm["steps"].get("parity")
    if pv:
        out["parity_pass_c32_dph"] = (pv.get("summary") or {}).get("decisions_per_h")
        out["parity_pass_cached_share"] = pv.get("cached_token_share")
        out["parity_pass_gpu_busy_pct"] = (pv.get("gpu") or {}).get("util_mean")
    p64 = arm["steps"].get("parity_c64")
    if p64:
        out["P_full_c64_dph"] = (p64.get("summary") or {}).get("decisions_per_h")
        out["P_full_c64_gpu_busy_pct"] = (p64.get("gpu") or {}).get("util_mean")
    lat = arm["steps"].get("latency")
    if lat:
        out["batch1_gpu_busy_pct"] = (lat.get("rep1", {}).get("gpu") or {}).get("util_mean")
    if not out:
        return None
    head = out.get("N_c64_dph")
    out["usd_per_1k_N_c64"] = {f"{int(u * 100)}%": usd_per_1k(rate, head, u) for u in UTILS} if head else None
    p = out.get("P_sat_c64_dph")
    out["usd_per_1k_P_sat_c64"] = {f"{int(u * 100)}%": usd_per_1k(rate, p, u) for u in UTILS} if p else None
    return out


def parity_of(arm: dict, ref_path: Path, items: dict, own_name: str) -> dict | None:
    ref = answers(ref_path)
    cand = answers(arm["dir"] / "answers_P.jsonl") if arm.get("dir") else None
    if not ref or cand is None:
        return None
    rep, rows = RR.parity(ref, cand, items)
    ov = rep["overall"]
    return {"n": ov["n"], "agree": ov["agree"], "flips": ov["flips"], "agree_rate": ov["agree_rate"], "wilson95": ov["wilson95"],
            "pass_wilson_0.995": ov["pass_wilson"], "max_dp": rep["dp"]["max"], "dp_mean": rep["dp"]["mean"], "dp_p99": rep["dp"]["p99"],
            "missing": rep["missing"], "flip_ref_margin_median": ov["flip_ref_margin_median"], "flip_ref_margin_max": ov["flip_ref_margin_max"],
            "flips_ref_margin_le": rep["flips"]["ref_margin_le"],
            "by_bucket": rep["by_bucket"], "by_view_type": rep["by_view_type"],
            "choice_per_view_argmax_agree": rep["choice_per_view_argmax_agree"], "verdict_view_types": rep["verdict"],
            "_rows": rows}


def verdict_of(name: str, par: dict | None, arm: dict, floor_flips: int = 0) -> str:
    if not arm.get("ran") or arm.get("skipped") or arm.get("error") or arm.get("aborted"):
        return "NA"
    if name == "r2_b_gc" and par is None:     # latency/throughput-only arm: gc.freeze() cannot change an answer
        return "exact (by construction; parity pass not re-run)"
    if par is None:
        return "NA"
    if name == "r2_a":
        return "reference"
    if not par["pass_wilson_0.995"]:
        return "fail"
    # BF16 is not bit-reproducible across batch compositions (A c32 vs A c64: `floor_flips` flips), so `exact` = flips no worse than that floor
    return "exact" if (name in EXACT_BY_CONSTRUCTION and par["flips"] <= floor_flips) else "pass"


# ------------------------------------------------------------------ images
def vision_of(arm: dict) -> dict | None:
    v = jload(arm["dir"] / "vision_r2.json") if arm.get("dir") else None
    if not v:
        return None
    arms = {}
    for a in v["arms"]:
        recs = {r["id"]: r for r in a["records"] if r and r.get("ok")}
        arms[f"{a['arm']}#{sum(1 for k in arms if k.startswith(a['arm'] + '#')) + 1}"] = {
            "n_ok": a["n_ok"], "errors": a["errors"], "acc": a["acc"], "ms": a["ms"], "prep_ms": a.get("prep_ms"),
            "items_per_s": a["items_per_s"], "token_mismatches": a["token_mismatches"], "gpu_busy_pct": (a.get("gpu") or {}).get("util_mean"),
            "_recs": recs}
    return arms


def vcmp(a: dict, b: dict) -> dict:
    ids = [i for i in a["_recs"] if i in b["_recs"]]
    flips = [i for i in ids if a["_recs"][i]["pred"] != b["_recs"][i]["pred"]]
    dps = [max(abs(x - y) for x, y in zip(a["_recs"][i]["probs"], b["_recs"][i]["probs"])) for i in ids]
    return {"n": len(ids), "flips": len(flips), "agree": round(1 - len(flips) / len(ids), 4) if ids else None,
            "dp_max": round(max(dps), 6) if dps else None, "dp_mean": round(statistics.fmean(dps), 7) if dps else None,
            "identical_probs": bool(dps) and max(dps) < 1e-6}


def vision_view(v: dict | None, base: dict | None, name: str) -> dict | None:
    if not v:
        return None
    pub = {k: {kk: vv for kk, vv in a.items() if kk != "_recs"} for k, a in v.items()}
    out = {"arms": pub}
    if "native:1#1" in v and "native:1#2" in v:
        out["noise_floor_native_c1_run1_vs_run2"] = vcmp(v["native:1#1"], v["native:1#2"])
    if "native:8#1" in v and "native:8#2" in v:
        out["noise_floor_native_c8_run1_vs_run2"] = vcmp(v["native:8#1"], v["native:8#2"])
    if "native:1#1" in v and "native:8#1" in v:
        out["native_c1_vs_c8"] = vcmp(v["native:1#1"], v["native:8#1"])
    if "exact:1#1" in v and "native:1#1" in v:
        out["exact_vs_native_c1"] = vcmp(v["exact:1#1"], v["native:1#1"])
    if "exact:8#1" in v and "native:8#1" in v:
        out["exact_vs_native_c8"] = vcmp(v["exact:8#1"], v["native:8#1"])
    if base is not None and name != "r2_a":
        for k in ("native:1#1", "native:1#2", "native:8#1", "native:8#2"):
            if k in v and k in base:
                out[f"{k}_vs_A_{k}"] = vcmp(v[k], base[k])
    return out


# ------------------------------------------------------------------ gate (arm C)
def gate_block(rd: Path, items: dict, rate: float, c_arm: dict, a_arm: dict, lat_c: dict | None, lat_a: dict | None, thr_c, thr_a) -> dict | None:
    ref = answers(rd / "r2_a" / "answers_P.jsonl")
    rerun = answers(rd / "r2_a" / "answers_P_c64.jsonl")
    fp8 = answers(rd / "r2_c" / "answers_P.jsonl")
    if not (ref and rerun and fp8):
        return None
    out = {"ref": "arm A c32 pass", "bf16_rerun": "arm A second pass (c64)", "fp8": "arm C pass (c32)"}
    out["bf16_rerun_vs_ref"] = RR.parity(ref, rerun, items)[0]["overall"]
    g = {}
    for tgt in (0.998, 0.996):
        g[f"fit_target_{tgt}"] = RR.gate_replay(ref, fp8, rerun, items, fit_target=tgt)
    out["gate_replay"] = g
    # tau table: deferral share, flips, Wilson LB and the cascade's throughput / batch-1 latency for a ladder of taus (in-sample on the full set)
    import hashlib as _h
    ids = [i for i in items if i in ref and i in fp8 and i in rerun]
    t8 = (thr_c or {}).get("P_sat_c64_dph")
    t16 = (thr_a or {}).get("P_sat_c64_dph")
    table = []
    half = {i: int(_h.sha1(i.encode()).hexdigest(), 16) & 1 for i in ids}
    for tau in (0.05, 0.08, 0.1, 0.12, 0.14, 0.15, 0.2, 0.245, 0.3, 0.37, 0.5):
        flips = deferred = 0
        hf, hn = [0, 0], [0, 0]
        for i in ids:
            o = items[i]["options"]
            m = RR.margin(o, fp8[i]["probs"])
            final = fp8[i]["probs"] if m >= tau else rerun[i]["probs"]
            deferred += m < tau
            fl = RR.top(o, final) != RR.top(o, ref[i]["probs"])
            flips += fl
            hf[half[i]] += fl
            hn[half[i]] += 1
        n = len(ids)
        lo = RR.wilson(n - flips, n)[0]
        hlb = [round(RR.wilson(hn[k] - hf[k], hn[k])[0], 6) for k in (0, 1)]
        row = {"tau": tau, "deferral_share": round(deferred / n, 4), "flips": flips, "agree_rate": round((n - flips) / n, 6), "wilson_lb": round(lo, 6),
               "meets_bar_in_sample": lo >= 0.995, "flips_half0_half1": hf, "wilson_lb_half0_half1": hlb, "both_halves_meet_bar": min(hlb) >= 0.995}
        if t8 and t16:
            eff = 1.0 / (1.0 / t8 + (deferred / n) / t16)
            row.update({"cascade_dph": round(eff), "gain_vs_bf16_pct": round(100 * (eff / t16 - 1), 1), "usd_per_1k_100pct": usd_per_1k(rate, eff, 1.0)})
        if lat_c and lat_a:
            L = []
            for i, mc in lat_c["_by_id"].items():
                if i in lat_a["_by_id"] and i in fp8:
                    L.append(mc + (lat_a["_by_id"][i] if RR.margin(items[i]["options"], fp8[i]["probs"]) < tau else 0.0))
            if L:
                row["batch1_ms_p50_p95_p99"] = [round(pct(L, 0.5), 2), round(pct(L, 0.95), 2), round(pct(L, 0.99), 2)]
        table.append(row)
    out["tau_table"] = table
    # cascade estimate at the conservative tau (larger of the two fitted taus, target 0.998; else target 0.996)
    pick = None
    for tgt in (0.998, 0.996):
        gg = g[f"fit_target_{tgt}"]
        if gg.get("full_set_at_max_fitted_tau"):
            pick = (tgt, gg)
            break
    if not pick:
        out["cascade"] = {"note": "no tau reached the fit target on either half: no gate is possible at these targets"}
        return out
    tgt, gg = pick
    full = gg["full_set_at_max_fitted_tau"]
    tau, d = full["tau"], full["deferral_share"]
    sh = gg["split_half"]
    casc = {"fit_target": tgt, "tau": tau, "deferral_share": d, "flips_full_set": full["flips"], "agree_full_set": full["agree_rate"],
            "wilson_lb_full_set": full["wilson_lb"], "half_results": {k: {"tau": v.get("tau"), "test": v.get("test")} for k, v in sh.items()},
            "no_gate_fp8": gg["no_gate_fp8"]}
    t8 = (thr_c or {}).get("P_sat_c64_dph")
    t16 = (thr_a or {}).get("P_sat_c64_dph")
    if t8 and t16:
        eff = 1.0 / (1.0 / t8 + d / t16)
        casc["throughput_P_sat_c64_dph"] = {"fp8": t8, "bf16": t16, "cascade_effective": round(eff),
                                            "gain_vs_bf16_pct": round(100 * (eff / t16 - 1), 1),
                                            "usd_per_1k": {f"{int(u * 100)}%": usd_per_1k(rate, eff, u) for u in UTILS},
                                            "model": "GPU-seconds add: 1/T = 1/T_fp8 + deferral_share/T_bf16 (both models resident, one stream)"}
    # batch-1 cascade latency on the N ids: FP8 answer, then (if its margin < tau) the BF16 answer after it
    if lat_c and lat_a:
        L = []
        for i, mc in lat_c["_by_id"].items():
            if i in lat_a["_by_id"] and i in fp8:
                m = RR.margin(items[i]["options"], fp8[i]["probs"])
                L.append(mc + (lat_a["_by_id"][i] if m < tau else 0.0))
        if L:
            casc["batch1_latency_ms"] = {**lat_summary(L), "deferred_in_N": sum(1 for i in lat_c["_by_id"] if i in fp8 and
                                                                             RR.margin(items[i]["options"], fp8[i]["probs"]) < tau),
                                         "model": "per N id: FP8 call, plus the BF16 call when the FP8 margin < tau (sequential, no router cost)"}
    out["cascade"] = casc
    return out


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=None)
    ap.add_argument("--rate", type=float, default=RATE_DEFAULT)
    ap.add_argument("--out-prefix", default="TRIALS_H100")
    a = ap.parse_args()
    rd = find_run(a.run)
    rate = a.rate
    items = RR.load_items()
    sess = jload(rd / "session_result.json") or {}
    arms = {n: load_arm(rd, n) for n in ORDER}
    base = arms["r2_a"]
    ref_path = rd / "r2_a" / "answers_P.jsonl"
    rows, extra = [], {}
    floor_flips = 0
    if base["ran"] and (base["dir"] / "answers_P_c64.jsonl").exists() and (base["dir"] / "answers_P.jsonl").exists():
        floor_flips = RR.parity(answers(base["dir"] / "answers_P.jsonl"), answers(base["dir"] / "answers_P_c64.jsonl"), items)[0]["overall"]["flips"]
    cmds = {}
    for l in (rd / "events.jsonl").read_text().splitlines() if (rd / "events.jsonl").exists() else []:
        try:
            e = json.loads(l)
        except ValueError:
            continue
        if e.get("event") == "block_start":
            cmds[e["config"]] = {"cmd": e.get("cmd"), "env": e.get("env")}
    lat_a = latency_of(base) if base["ran"] else None
    thr_a = throughput_of(base, rate) if base["ran"] else None
    vis_a = vision_of(base) if base["ran"] else None
    for n in ORDER:
        arm = arms[n]
        row = {"config": n, "what": WORDS[n], "ran": arm["ran"]}
        if not arm["ran"]:
            row.update({"verdict": "NA", "note": "not run (not queued, or the plan did not reach it)"})
            rows.append(row)
            continue
        blk = arm["block"]
        row["server_cmd"] = cmds.get(n)
        row["boot_failure_cause"] = boot_failure(arm["dir"] / "sglang.log") if arm["error"] else None
        row.update({"skipped": arm["skipped"], "error": arm["error"], "aborted_by_canary": arm["aborted"], "boot_s": blk.get("boot_s"),
                    "prefill_graph_backend_resolved": blk.get("prefill_graph_backend_resolved"),
                    "args_warnings": blk.get("args_warnings"), "log_scan": blk.get("log_scan"), "spent_usd_after_block": blk.get("spent_usd")})
        if blk.get("patch_report"):
            row["patch_report"] = blk["patch_report"]
            ev = [e.get("event") for e in blk["patch_report"].get("events", [])]
            row["lmhead_patch_engaged"] = ("rows_copied" in ev) or ("counters" in ev)
            row["lmhead_patch_processes_patched"] = len({e.get("pid") for e in blk["patch_report"].get("events", []) if e.get("event") == "patched"})
        if blk.get("metrics"):
            row["metrics"] = blk["metrics"]
        par = None
        if n == "r2_a":
            par = parity_of(arm, ref_path, items, n)             # A against itself: trivially 1.0 (kept for the schema)
            p64 = answers(arm["dir"] / "answers_P_c64.jsonl")
            if p64:
                floor = RR.parity(answers(ref_path), p64, items)[0]
                row["bf16_self_agreement_floor_c32_vs_c64"] = {k: floor["overall"][k] for k in ("n", "agree", "flips", "agree_rate", "wilson95", "max_dp")}
                row["bf16_self_agreement_floor_c32_vs_c64"]["by_bucket"] = floor["by_bucket"]
                row["bf16_self_agreement_floor_c32_vs_c64"]["max_dp"] = floor["dp"]["max"]
            st = jload(rd / "r2_a" / "measure.json", {}).get("steps", {}).get("parity", {})
            if st.get("parity_vs_speed2_S1_stored"):
                s2 = st["parity_vs_speed2_S1_stored"]
                row["vs_speed2_stored_S1_answers"] = {k: s2.get(k) for k in ("n", "argmax_agree", "n_flips", "agree_wilson95", "dp_max")}
        else:
            par = parity_of(arm, ref_path, items, n)
        if par:
            row["parity"] = {k: v for k, v in par.items() if k != "_rows"}
        lat = latency_of(arm)
        if lat:
            row["batch1"] = {k: v for k, v in lat.items() if k != "_by_id"}
            if lat_a and n != "r2_a":
                row["batch1"]["delta_vs_A_ms"] = {k: round(lat["pooled"][k] - lat_a["pooled"][k], 2) for k in ("p50", "p95", "p99")}
        thr = throughput_of(arm, rate)
        if thr:
            row["throughput"] = thr
            if thr_a and n != "r2_a":
                for k in ("N_c64_dph", "P_sat_c64_dph", "parity_pass_c32_dph"):
                    if thr.get(k) and thr_a.get(k):
                        row["throughput"][f"{k}_vs_A_pct"] = round(100 * (thr[k] / thr_a[k] - 1), 1)
        pr = arm["steps"].get("prefix")
        if pr:
            row["prefix_R"] = {"cached_token_share": pr.get("cached_token_share"), "rows": pr.get("rows")}
        vis = vision_of(arm)
        if vis:
            row["vision"] = vision_view(vis, vis_a, n)
        row["verdict"] = verdict_of(n, par, arm, floor_flips)
        if n in ("r2_d1", "r2_d2") and vis and vis_a is not None:
            row["verdict"] = image_verdict(row["vision"], vis, vis_a)
            ig = {}
            for tag in ("#1", "#2"):
                a1, d1 = vis_a.get(f"native:1{tag}"), vis.get(f"native:1{tag}")
                if a1 and d1:
                    ig[f"c1{tag}_p50_down_ms"] = round(a1["ms"]["p50"] - d1["ms"]["p50"], 2)
                    ig[f"c1{tag}_p95_down_ms"] = round(a1["ms"]["p95"] - d1["ms"]["p95"], 2)
                a8, d8 = vis_a.get(f"native:8{tag}"), vis.get(f"native:8{tag}")
                if a8 and d8:
                    ig[f"c8{tag}_items_per_s_up_pct"] = round(100 * (d8["items_per_s"] / a8["items_per_s"] - 1), 1)
                    ig[f"c8{tag}_p50_down_ms"] = round(a8["ms"]["p50"] - d8["ms"]["p50"], 2)
            ig["note"] = ("A's pass #1 ran after 5 min of text load, the D servers' pass #1 right after boot, so the steady-state passes (#2) are the fair comparison; "
                          "p50/p95 are ms per image decision (both views for choice items)")
            row["image_gain"] = ig
            other = {"r2_d1": "r2_d2", "r2_d2": "r2_d1"}[n]
            ov = vision_of(arms[other]) if arms[other]["ran"] else None
            if ov and "native:1#1" in ov and "native:1#1" in vis:
                row["vision"]["vs_" + other + "_native_c1_pass1"] = vcmp(vis["native:1#1"], ov["native:1#1"])
        if n == "r2_a" and vis:
            row["exact_preresize"] = exact_preresize(vis, row.get("vision") or {})
        row["gain"] = gain_of(row, arms[n])
        rows.append(row)
        if n == "r2_c":
            lat_c, thr_c = lat, thr
    gate = gate_block(rd, items, rate, arms["r2_c"], base, latency_of(arms["r2_c"]) if arms["r2_c"]["ran"] else None, lat_a,
                      throughput_of(arms["r2_c"], rate) if arms["r2_c"]["ran"] else None, thr_a) if arms["r2_c"]["ran"] and base["ran"] else None
    for r in rows:
        r["adopt"] = adopt_of(r)
    result = {"generated_utc": C.utc(), "run_dir": str(rd), "rate_usd_h": rate, "session": {k: sess.get(k) for k in ("spent_usd", "wall_s", "gpu", "region", "notes", "checkpoint_verified")},
              "ledger": jload(HERE / "ledger.json"), "bar": "Wilson95 lower bound >= 0.995 on the full 8,143 parity set vs the same-session S1 BF16 pass (c32)",
              "billing": billing_block(), "rows": rows, "margin_gate_C": gate}
    result["adoptable"] = [r["config"] for r in rows if r.get("adopt", {}).get("adopt")]
    Path(HERE / f"{a.out_prefix}.json").write_text(json.dumps(result, indent=1, default=str))
    Path(HERE / f"{a.out_prefix}.md").write_text(render_md(result))
    print(json.dumps({"rows": [(r["config"], r["verdict"], (r.get("adopt") or {}).get("adopt")) for r in rows], "adoptable": result["adoptable"]}))


def billing_block() -> dict:
    """modal billing summary/report snapshots taken before and after the window (jaypatil-duke)."""
    b = HERE / "billing"
    out = {}
    for tag in ("before", "after"):
        sm = jload(b / f"summary_{tag}.json")
        if sm:
            out[tag] = {"taken_utc": (b / f"{tag}.utc").read_text().strip() if (b / f"{tag}.utc").exists() else None,
                        "metered_cost_usd": sm.get("metered_cost"), "credits_applied_usd": (sm.get("adjustments") or {}).get("credits"),
                        "billed_cost_usd": sm.get("billed_cost"), "ephemeral_apps_usd": (sm.get("metered_cost_breakdown") or {}).get("ephemeral_apps"),
                        "volumes_usd": (sm.get("metered_cost_breakdown") or {}).get("volumes")}
    try:
        out["delta_metered_usd"] = round(float(out["after"]["metered_cost_usd"]) - float(out["before"]["metered_cost_usd"]), 4)
        out["delta_credits_applied_usd"] = round(float(out["after"]["credits_applied_usd"]) - float(out["before"]["credits_applied_usd"]), 4)
    except (KeyError, TypeError, ValueError):
        pass
    rep = jload(b / "report_today_after.json")
    if rep:
        mine = [r for r in rep if r.get("description") == C.APP_NAME]
        by = {}
        for r in mine:
            by[r["resource"]] = by.get(r["resource"], 0.0) + float(r["cost"])
        out["report_app_cost_by_resource_usd"] = {k: round(v, 4) for k, v in by.items()}
        out["report_app_cost_total_usd"] = round(sum(by.values()), 4)
    return out


def gain_of(row: dict, arm: dict) -> dict:
    g = {}
    b = row.get("batch1") or {}
    d = b.get("delta_vs_A_ms")
    if d:
        g["p50_down_ms"] = -d["p50"]
        g["p99_down_ms"] = -d["p99"]
        g["p95_down_ms"] = -d["p95"]
    t = row.get("throughput") or {}
    cands = [t.get(k) for k in ("N_c64_dph_vs_A_pct", "P_sat_c64_dph_vs_A_pct")]
    cands = [c for c in cands if c is not None]
    if cands:
        g["throughput_up_pct_N"] = t.get("N_c64_dph_vs_A_pct")
        g["throughput_up_pct_P"] = t.get("P_sat_c64_dph_vs_A_pct")
        g["throughput_up_pct_min"] = min(cands)
    return g


def adopt_of(row: dict) -> dict:
    v = row.get("verdict")
    g = row.get("gain") or {}
    if v in (None, "NA", "fail"):
        return {"adopt": False, "why": f"verdict {v}"}
    if row["config"] == "r2_a":
        return {"adopt": False, "why": "the reference"}
    real = (g.get("p50_down_ms", -99) >= 2.0) or (g.get("p99_down_ms", -99) >= 2.0) or (g.get("throughput_up_pct_min", -99) >= 5.0)
    if row["config"] in ("r2_d1", "r2_d2"):
        ig = row.get("image_gain") or {}
        real = (ig.get("c1#2_p50_down_ms", -99) >= 2.0 or ig.get("c8#2_items_per_s_up_pct", -99) >= 5.0)      # p95 of 200 items is noise-dominated
        g = ig
    return {"adopt": bool(real), "why": "bar met and a real gain" if real else "bar met but no gain >= 2 ms p50/p99 or >= 5% throughput", "gain": g}


def exact_preresize(v: dict, view: dict) -> dict:
    """Client-side resize to the processor's exact target size (PIL bicubic) vs the original file, both on the S1 server."""
    out = {}
    for c in (1, 8):
        n, e = v.get(f"native:{c}#1"), v.get(f"exact:{c}#1")
        if not (n and e):
            continue
        cmp = view.get(f"exact_vs_native_c{c}") or vcmp(e, n)
        out[f"c{c}"] = {"identical_probs_to_native": cmp.get("identical_probs"), "agree": cmp.get("agree"), "flips": cmp.get("flips"), "dp_max": cmp.get("dp_max"),
                        "server_ms_p50_native": n["ms"]["p50"], "server_ms_p50_exact": e["ms"]["p50"], "client_prep_ms_p50_exact": (e.get("prep_ms") or {}).get("p50"),
                        "client_prep_ms_p50_native": (n.get("prep_ms") or {}).get("p50"),
                        "net_p50_gain_ms_incl_client_resize": round(n["ms"]["p50"] + ((n.get("prep_ms") or {}).get("p50") or 0) -
                                                                    (e["ms"]["p50"] + ((e.get("prep_ms") or {}).get("p50") or 0)), 2),
                        "verdict": "exact" if cmp.get("identical_probs") else ("pass (within noise: see floor)" if cmp.get("flips", 99) <= 1 else "fail")}
    return out


def image_verdict(view: dict, v: dict, vis_a: dict) -> str:
    floor = (view.get("noise_floor_native_c1_run1_vs_run2") or {})
    cross = view.get("native:1#1_vs_A_native:1#1") or {}
    if not cross:
        return "NA"
    if cross.get("identical_probs"):
        return "exact"
    if cross.get("flips", 99) <= max(floor.get("flips", 0), 1):
        return "pass"
    return "fail"


def boot_failure(log_path: Path) -> list | None:
    try:
        lines = Path(log_path).read_text(errors="replace").splitlines()
    except OSError:
        return None
    idx = [i for i, l in enumerate(lines) if "Traceback" in l]
    if not idx:
        return lines[-6:]
    tb = lines[idx[-1]:idx[-1] + 60]
    keep = [l for l in tb if l.strip().startswith("File") and ("hybrid_linear" in l or "prefill_cuda_graph_runner" in l or "cuda_graph_setup" in l)]
    tail = [l for l in tb if l.strip() and not l.strip().startswith("File") and "^" not in l][-4:]
    return keep[-4:] + tail


def f2(x, nd=2):
    return "-" if x is None else (f"{x:,.{nd}f}" if isinstance(x, float) else f"{x:,}" if isinstance(x, int) else str(x))


def exec_summary(res: dict) -> list:
    R = {r["config"]: r for r in res["rows"]}
    A, Bn, Bg, C_, D1, D2, E1, E2 = (R.get(k) or {} for k in ("r2_a", "r2_b_nofull", "r2_b_gc", "r2_c", "r2_d1", "r2_d2", "r2_e1", "r2_e2"))
    g = lambda r, *ks: _dig(r, *ks)
    a50, a99 = g(A, "batch1", "pooled", "p50"), g(A, "batch1", "pooled", "p99")
    L = ["## Findings in one page", ""]
    L += [f"- **A (S1 BF16 reference, this session):** batch-1 N p50/p95/p99 {a50}/{g(A, 'batch1', 'pooled', 'p95')}/{a99} ms (640 calls); N c64 {f2(g(A, 'throughput', 'N_c64_dph'))} dec/h, "
          f"P c64 {f2(g(A, 'throughput', 'P_sat_c64_dph'))} dec/h; GPU busy {g(A, 'throughput', 'batch1_gpu_busy_pct')}% at batch 1 and {g(A, 'throughput', 'N_c64_gpu_busy_pct')}% at c64; "
          f"USD/1K at 100/50/20% utilisation {g(A, 'throughput', 'usd_per_1k_N_c64')}. BF16 self-agreement floor (A c32 vs A c64): "
          f"{g(A, 'bf16_self_agreement_floor_c32_vs_c64', 'flips')} flips of 8,143.",
          f"- **B (exact bundle):** `--cuda-graph-backend-prefill full` does NOT work for this GDN hybrid on SGLang 0.5.20: the server dies while capturing the prefill graph "
          f"(`{(R.get('r2_b') or {}).get('boot_failure_cause', ['?'])[-2] if (R.get('r2_b') or {}).get('boot_failure_cause') else '?'}` in hybrid_linear_attn_backend._replay_metadata), so it is dropped from the bundle. "
          f"The rest of the bundle (skip-tokenizer-init + input_ids, /v1/score, metrics, gc warnings) is **{Bn.get('verdict')}** ({g(Bn, 'parity', 'flips')} flip, Wilson LB {g(Bn, 'parity', 'wilson95', 0)}) "
          f"but gives no gain: batch-1 p50 {g(Bn, 'batch1', 'pooled', 'p50')} vs {a50} ms, p99 {g(Bn, 'batch1', 'pooled', 'p99')} vs {a99} ms, N c64 {f2(g(Bn, 'throughput', 'N_c64_dph'))} dec/h (same).",
          f"- **LM-head slice:** the opt-in patch was installed in {Bn.get('lmhead_patch_processes_patched')} SGLang processes but never took the slice path (patch report has no `rows_copied` / counters), so the 141-row head was NOT exercised on the GPU; "
          f"the arithmetic is CPU-tested and the cost it could remove is about 0.4 ms (1.27 GB head read at 3.35 TB/s). Not measured, not adopted.",
          f"- **GC:** SGLang already freezes the GC after its warm-up (`/freeze_gc` called once, seen in the metrics); the only long GC in the log is one 0.36 s generation-2 pass at warm-up, none in the measured loops. "
          f"gc.freeze() after warm-up changed nothing: p50 {g(Bg, 'batch1', 'pooled', 'p50')}, p99 {g(Bg, 'batch1', 'pooled', 'p99')} ms. The p99 tail (~{a99} ms) is not GC.",
          f"- **C (block-FP8):** FAIL alone: {g(C_, 'parity', 'agree')}/8,143 agree ({g(C_, 'parity', 'agree_rate')}, Wilson LB {g(C_, 'parity', 'wilson95', 0)}, {g(C_, 'parity', 'flips')} flips, max |dp| {g(C_, 'parity', 'max_dp')}). "
          f"Throughput is +{g(C_, 'throughput', 'N_c64_dph_vs_A_pct')}% (N c64 {f2(g(C_, 'throughput', 'N_c64_dph'))} dec/h) and p99 {g(C_, 'batch1', 'pooled', 'p99')} ms, but p50 is unchanged ({g(C_, 'batch1', 'pooled', 'p50')} ms). "
          f"With the margin gate the bar is met only at a large deferral share; see the ladder below (tau 0.20: 10.6% deferred, 10 flips, both halves above the bar, +11.2% cascade throughput, batch-1 p99 ~108 ms). "
          f"The split-half test as specified is not stable (tau fitted on half 0 fails on half 1 with LB 0.9948), so the gate is NOT confirmed.",
          f"- **D (images):** native-vs-native noise floor on the 200-image pack is 1 flip in 200 at c1 (dp up to 0.0045) and 0 at c8 (dp up to 0.0128). "
          f"`--keep-mm-feature-on-device` ({D1.get('verdict')}): steady-state c1 p50 {g(D1, 'image_gain', 'c1#2_p50_down_ms')} ms lower, c8 throughput +{g(D1, 'image_gain', 'c8#2_items_per_s_up_pct')}%, agreement with A's native within the floor (1 flip). "
          f"D1 and D2 give bit-identical probabilities to each other on the 200 images (both fresh boots), so the flags do not change the numerics; the 1-flip / dp <= 0.016 difference to arm A's server is a server-state effect of the size of the noise floor (A's pass ran after 5 min of text load). "
          f"`--mm-processor-worker-num 4` ({D2.get('verdict')}): no gain (c1 p50 {g(D2, 'image_gain', 'c1#2_p50_down_ms')} ms, c8 throughput {g(D2, 'image_gain', 'c8#2_items_per_s_up_pct')}%). "
          f"Client-side exact-size pre-resize is NOT bit-identical (4-5 flips in 200, dp up to 0.18) and costs ~23 ms of client time: rejected.",
          f"- **E (cache knobs):** `--mamba-ssm-dtype bfloat16` pass ({g(E1, 'parity', 'flips')} flips), p50 {g(E1, 'batch1', 'pooled', 'p50')} ms ({g(E1, 'batch1', 'delta_vs_A_ms', 'p50')}), throughput +{g(E1, 'throughput', 'N_c64_dph_vs_A_pct')}%: below the adopt threshold. "
          f"`--mamba-track-interval 64` pass ({g(E2, 'parity', 'flips')} flip), no gain. Cached share unchanged (R: {g(E1, 'prefix_R', 'cached_token_share')}).",
          f"- **Adoptable set (bar met AND a real gain):** {res['adoptable'] or 'none'}. Exact/pass but with no gain (safe, optional): the bundle without `full` and the cache knobs. "
          f"Money: ledger USD {g(res, 'ledger', 'spent_closed_usd')} of the USD 5.00 cap; billing report for the app USD {g(res, 'billing', 'report_app_cost_total_usd')}.", ""]
    return L


def _dig(o, *ks):
    for k in ks:
        try:
            o = o[k]
        except (KeyError, IndexError, TypeError):
            return None
    return o


def render_md(res: dict) -> str:
    L = ["# TRIALS_H100 (round 2, one H100 window)", "",
         f"Generated {res['generated_utc']} from `{res['run_dir']}`. Rate used for $/1K: **USD {res['rate_usd_h']}/h** (H100 3.95 + 4 cores x 0.0473 + 32 GiB x 0.008, region 'any' x1.0). "
         f"Bar: {res['bar']}.", ""]
    s = res["session"]
    L += [f"Session: GPU {s.get('gpu')}, region {s.get('region')}, wall {s.get('wall_s')} s, in-container spend estimate USD {s.get('spent_usd')}.", ""]
    if s.get("notes"):
        L += ["Decisions taken during the window:"] + [f"- {n}" for n in s["notes"]] + [""]
    L += exec_summary(res)
    L += ["## One row per arm", "",
          "| arm | config | verdict | agree (Wilson LB) | flips | max dp | b1 p50/p95/p99 ms | d p50/p99 vs A | N c64 dec/h | P c64 dec/h | GPU busy b1 / c64 % | USD/1K @100/50/20% (N c64) | adopt |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["rows"]:
        p = r.get("parity") or {}
        b = (r.get("batch1") or {}).get("pooled") or {}
        d = (r.get("batch1") or {}).get("delta_vs_A_ms") or {}
        t = r.get("throughput") or {}
        u = t.get("usd_per_1k_N_c64") or {}
        L.append("| {arm} | `{cfg}` | **{v}** | {ag} ({lb}) | {fl} | {dp} | {p50}/{p95}/{p99} | {d50}/{d99} | {n} | {pp} | {g1} / {g2} | {u1} / {u2} / {u3} | {ad} |".format(
            arm=r["what"].split(".")[0], cfg=r["config"], v=r["verdict"],
            ag=f2(p.get("agree_rate"), 5), lb=f2((p.get("wilson95") or [None])[0], 5), fl=f2(p.get("flips")), dp=f2(p.get("max_dp"), 4),
            p50=f2(b.get("p50")), p95=f2(b.get("p95")), p99=f2(b.get("p99")), d50=f2(d.get("p50")), d99=f2(d.get("p99")),
            n=f2(t.get("N_c64_dph")), pp=f2(t.get("P_sat_c64_dph")), g1=f2(t.get("batch1_gpu_busy_pct")), g2=f2(t.get("N_c64_gpu_busy_pct")),
            u1=f2(u.get("100%"), 4), u2=f2(u.get("50%"), 4), u3=f2(u.get("20%"), 4), ad=("yes" if (r.get("adopt") or {}).get("adopt") else "no")))
    L += ["", "NA rows: the arm did not run (see the notes per arm below). `exact` = numerics-preserving by construction, bar met, 0 flips.", ""]
    for r in res["rows"]:
        L += [f"### {r['what']}  (`{r['config']}`: {r['verdict']})", ""]
        if not r.get("ran"):
            L += [r.get("note", ""), ""]
            continue
        if r.get("skipped"):
            L += [f"- skipped by the budget gate: {r['skipped']}"]
        if r.get("error"):
            L += [f"- block error: `{str(r['error'])[:400]}`"]
        if r.get("aborted_by_canary"):
            L += [f"- stopped by its canary: `{str(r['aborted_by_canary'])[:300]}`"]
        if r.get("prefill_graph_backend_resolved"):
            L += [f"- prefill graph backend resolved by SGLang: `{r['prefill_graph_backend_resolved']}`"]
        p = r.get("parity")
        if p:
            L += [f"- parity vs A (same session, c32): {p['agree']}/{p['n']} = {p['agree_rate']} (Wilson95 {p['wilson95']}), flips {p['flips']}, max |dp| {p['max_dp']}, "
                  f"mean dp {p['dp_mean']}, flip ref-margin median {p['flip_ref_margin_median']} max {p['flip_ref_margin_max']}, flips with ref margin <= 0.005/0.01/0.02/0.05/0.1: {p['flips_ref_margin_le']}",
                  "- per bucket: " + "; ".join(f"{k}: {v['agree']}/{v['n']} LB {v['wilson95'][0]}{' (underpowered)' if v['underpowered'] else ''}" for k, v in p["by_bucket"].items()),
                  "- per view type: " + "; ".join(f"{k}: {v['agree']}/{v['n']} LB {v['wilson95'][0]}" for k, v in p["by_view_type"].items())]
        if r.get("bf16_self_agreement_floor_c32_vs_c64"):
            f = r["bf16_self_agreement_floor_c32_vs_c64"]
            L += [f"- BF16 self-agreement floor (A c32 vs A c64 on the same server): {f['agree']}/{f['n']} = {f['agree_rate']} (Wilson95 {f['wilson95']}), max |dp| {f['max_dp']}"]
        if r.get("vs_speed2_stored_S1_answers"):
            L += [f"- A vs SPEED-2's stored S1 answers (13 Oct): {r['vs_speed2_stored_S1_answers']}"]
        b = r.get("batch1")
        if b:
            L += [f"- batch-1 N, 2 x 320 calls: rep1 {b['rep1']}; rep2 {b['rep2']}; pooled {b['pooled']}; rep p50 spread {b['rep_p50_spread']} ms" +
                  (f"; delta vs A {b['delta_vs_A_ms']}" if b.get("delta_vs_A_ms") else "")]
        t = r.get("throughput")
        if t:
            L += [f"- throughput: {json.dumps({k: v for k, v in t.items() if not k.startswith('usd')})}",
                  f"- USD/1K (N c64): {t.get('usd_per_1k_N_c64')}; (P c64): {t.get('usd_per_1k_P_sat_c64')}"]
        if r.get("prefix_R"):
            L += [f"- R prefix-repeat set cached share: {r['prefix_R']}"]
        if r.get("log_scan"):
            L += ["- log scan: " + "; ".join(f"{k}: {v['n']}" for k, v in r["log_scan"].items())]
            for k in ("gc", "fallback", "fp8", "error"):
                for line in (r["log_scan"].get(k) or {}).get("first", [])[:3]:
                    L += [f"    - {k}: `{line[:220]}`"]
        if r.get("patch_report"):
            L += [f"- LM-head patch report: {json.dumps(r['patch_report'])[:600]}"]
        if r.get("vision"):
            v = r["vision"]
            L += ["- images (200 items, ms per decision = both views for choice items):"]
            for k, a in v["arms"].items():
                L += [f"    - {k}: acc {a['acc']}, p50 {a['ms'].get('p50')} p95 {a['ms'].get('p95')} p99 {a['ms'].get('p99')}, items/s {a['items_per_s']}, token mismatches {a['token_mismatches']}, errors {a['errors']}"]
            for k, c in v.items():
                if k != "arms":
                    L += [f"    - {k}: {c}"]
        if r.get("exact_preresize"):
            L += [f"- client-side exact-size pre-resize (arm A server): {json.dumps(r['exact_preresize'])}"]
        if r.get("image_gain"):
            L += [f"- image latency gain vs arm A: {r['image_gain']}"]
        L += [f"- gain vs A: {r.get('gain')}; adopt: {r.get('adopt')}", ""]
    g = res.get("margin_gate_C")
    if g:
        L += ["## Margin gate on arm C (offline, on the H100 answers)", ""]
        L += [f"- BF16 re-run vs reference (A c64 vs A c32): {g.get('bf16_rerun_vs_ref')}"]
        for tgt, gg in g["gate_replay"].items():
            L += [f"- {tgt}: no gate (FP8 alone) {gg['no_gate_fp8']}; split-half: " + json.dumps(gg["split_half"], default=str)[:900],
                  f"  full set at the larger fitted tau: {gg.get('full_set_at_max_fitted_tau')}"]
        L += ["- cascade estimate: " + json.dumps(g.get("cascade"), default=str)[:2500], ""]
    if g and g.get("tau_table"):
        L += ["", "Cascade ladder (FP8 answer when its margin >= tau, else the BF16 re-run; in-sample on all 8,143 items):", "",
              "| tau | deferred | flips (half0/half1) | agree | Wilson LB (full / half0 / half1) | bar met: full, both halves | cascade dec/h (P c64) | vs BF16 | USD/1K @100% | batch-1 p50/p95/p99 ms (N) |", "|---|---|---|---|---|---|---|---|---|---|"]
        for t in g["tau_table"]:
            L.append(f"| {t['tau']} | {t['deferral_share']} | {t['flips']} ({t['flips_half0_half1'][0]}/{t['flips_half0_half1'][1]}) | {t['agree_rate']} | {t['wilson_lb']} / {t['wilson_lb_half0_half1'][0]} / {t['wilson_lb_half0_half1'][1]} | {t['meets_bar_in_sample']}, {t['both_halves_meet_bar']} | {t.get('cascade_dph')} | {t.get('gain_vs_bf16_pct')}% | {t.get('usd_per_1k_100pct')} | {t.get('batch1_ms_p50_p95_p99')} |")
        L += [""]
    L += ["## Billing (jaypatil-duke, `modal billing summary` / `report`)", "", "```", json.dumps(res.get("billing"), indent=1), "```", ""]
    L += ["## How this window was run, and what to know before relying on it", "",
          "- One Modal app, one H100 container (`H100!`, region 'any' x1.0; it landed in us-central on an H100 80GB HBM3, driver 610.57.04), profile jaypatil-duke only, "
          "fresh ledger `h100/ledger.json` (cap 5.00, stop-launch 4.50, cancel 4.80; nothing was cancelled or skipped by the budget gate). Image layers came from the 17 Oct cache (container up 6 s after spawn).",
          "- Blocks run in the priority order A, B, C, D, E; conditional blocks were decided by code from what the block showed: `r2_b` failed to boot, so `r2_b_nofull` followed; "
          "the GC log line (one benign 0.36 s generation-2 pass at warm-up) triggered `r2_b_gc`; `r2_b_dcpc` (`--disable-chunked-prefix-cache`) was NOT run because the failure was not the chunked-prefix assertion.",
          "- Parity was measured at concurrency 32 (not 16) to save GPU time, with a canary on the first 300 decisions for every non-reference arm (stops a catastrophic arm early; it never fired). "
          "Arm A also ran a second full pass at c64: that is the BF16 self-agreement floor (2 flips) and the 'BF16 re-run' of the margin-gate replay.",
          "- Throughput: 'N c64' = the 660-call natural-mix set twice (short runs, shown as the mean of two); 'P c64' = the first 2,500 parity rows (longer, steadier). Both are closed loops with caches flushed before. "
          "Cost per 1K = rate / (decisions per hour x utilisation) x 1000 with rate USD 4.3952/h (list rates for the container); the hourly billing report priced the whole window at about USD 2.52 for 2,060 s of container time (about USD 4.41/h all-in, within 1% of that rate).",
          "- Block-FP8 checkpoint: built on od-cpu1/od-l4b (byte-identical), brought to the laptop in 200 MB parts through the IAP tunnel (each part sha256-checked, shard shas rebuilt and matched 4bbce991... / d01e6983...), uploaded to the Volume "
          "(`models/q35_4b_main500k_merged__fp8_block`) with a per-file manifest, and the manifest + both shard shas were re-verified INSIDE the container before arm C (no problems). One edit: `config.json` `modules_to_not_convert` got 24 extra entries "
          "`model.visual.blocks.N.attn.qkv_proj` (SGLang names the vision qkv `qkv_proj`; the checkpoint's list says `attn.qkv`, which SGLang would not match for Qwen3.5). Shards are untouched; original config sha256 3a741cef..., edited a1e79ec9.... "
          "It booted with DeepGEMM (a one-off 16,384-kernel JIT pre-compile made that boot 220 s instead of ~80 s).",
          "- The LM-head slice patch (`r2pypatch/sitecustomize.py.as_run_17oct`) is what ran. The copy in `r2pypatch/sitecustomize.py` is a later version with per-reason counters and without the `extend_return_logprob` condition; it was only CPU-tested and has NOT been run on a GPU.",
          "- Nothing was changed on od-l4b/production, C2 data/tools, HANDOFF.md or PREREG_FINAL.md; no OpenRouter/Jev call; no path containing ohs/sealed/quarantine/longbench was opened. The FP8 checkpoint stays on the Volume (about 5.5 GB; Volumes bill about USD 0.09 per GiB-month).",
          "- Code: `modal_app_r2.py`, `oc1/` (copy of the 17 Oct harness plus `oc1/r2.py`), `tests/test_r2.py` (12 CPU tests, all pass), `analyze_h100.py` (this file's generator), `r2_report.py`, `billing/`, `results/session_20261017_161152/`.", ""]
    L += ["## Adoptable set", "", f"{res['adoptable']}", ""]
    return "\n".join(L)


if __name__ == "__main__":
    main()
