"""oc1.report: turn a session's result folder into one summary (JSON + a console table). Laptop side, CPU only.

    ../../../.venv/bin/python -m oc1.report results/session_YYYYMMDD_HHMMSS/volume/<run_id>   # or any folder with <config>/measure.json

For every config: boot seconds, parity vs the S1 baseline of the same session (argmax agreement with its 95% interval,
max |dp|, the flips and their margins = the near-tie analysis), the accuracy difference on the gate dev rows (gold stays on
the laptop: speed_bench.compare, read-only) and the verdict against the bars (99.5% agreement, |acc diff| <= 0.3 pt, 1.0 pt for
quantized arms); batch-1 / batch-8 latency, saturation throughput and GPU busy share, prefix-cache hit rate; the cost table
(USD per 1K decisions vs utilisation, vs Jev) from the MEASURED throughput; the end-to-end stage tables; vision and voice.
A change that fails the bar is reported, never adopted ("adopt" is only ever printed for a PASS).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from . import common as C
from . import costmodel as CM
from . import parity as PAR
from . import configs as K


def load_json(p):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return None


def accuracy_diff(items: list, cand: dict, ref: dict) -> dict | None:
    """Accuracy of cand and ref on the gate dev rows they both answered (speed_bench.compare, gate_dev definitions)."""
    try:
        sys.path.insert(0, str(C.LEAN / "hosting"))
        sys.path.insert(0, str(C.LEAN))
        import speed_bench as SB
        rows = {r["id"]: r for r in SB.dev_rows()}
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {str(e)[:120]}"}
    ids = [i for i in cand if i in ref and i in rows]
    rep = SB.compare([rows[i] for i in ids], cand, ref)
    return {"n": rep["n"], "acc_cand": rep["acc_cand"], "acc_ref": rep["acc_ref"], "acc_diff_pt": rep["acc_diff_pt"],
            "argmax_agree_speedbench": rep["argmax_agree"], "pass_speedbench": rep["pass"]}


def read_answers(p) -> dict:
    return {r["id"]: r["probs"] for r in C.read_jsonl(p)} if Path(p).exists() else {}


def config_summary(run: Path, name: str, items: list, base_answers: dict) -> dict:
    d = run / name
    cfg = K.CONFIGS.get(name)
    blk, meas = load_json(d / "block.json") or {}, load_json(d / "measure.json") or {}
    steps = meas.get("steps", {})
    out = {"config": name, "desc": blk.get("desc"), "boot_s": blk.get("boot_s"), "error": blk.get("error") or meas.get("fatal"),
           "skipped": blk.get("skipped"), "step_errors": meas.get("errors")}
    ans_path = d / ("answers_P.jsonl" if (d / "answers_P.jsonl").exists() else "answers_P_sub.jsonl")
    cand = read_answers(ans_path)
    if cand and base_answers and name != "s1":
        sub = [it for it in items if it["id"] in cand and it["id"] in base_answers]
        rep = PAR.compare_items(sub, cand, base_answers)
        acc = accuracy_diff(items, cand, base_answers)
        out["parity_vs_s1"] = {k: rep[k] for k in ("n", "argmax_agree", "agree_wilson95", "dp_mean", "dp_p99", "dp_max", "n_flips",
                                                 "flip_margin_p50", "flip_margin_max", "flips_near_tie", "by_bucket", "flips")}
        out["accuracy_vs_s1"] = acc
        out["verdict"] = PAR.verdict(rep, (acc or {}).get("acc_diff_pt"), fp8=bool(cfg and cfg.fp8))
        out["adopt"] = out["verdict"] == "PASS"
    sc = (steps.get("score_readout") or {}).get("parity") or {}
    if sc:
        out["score_readout_vs_generate"] = (sc.get("parity_vs_generate_same_boot") or {})
    lat = steps.get("latency") or {}
    out["latency_ms"] = {"batch1_N": ((lat.get("batch1_N") or {}).get("wall_ms")), "batch1_S_heavy": ((lat.get("batch1_S_heavy") or {}).get("wall_ms")),
                         "batched8_per_decision": (((lat.get("batched_N") or {}).get("one_call") or {}).get("per_decision_ms")),
                         "simultaneous8_per_call": (((lat.get("batched_N") or {}).get("simultaneous") or {}).get("per_call_ms"))}
    tp = steps.get("throughput") or {}
    s = (tp.get("S") or {})
    out["throughput"] = {k: {"decisions_per_h": v.get("decisions_per_h"), "whole_set_decisions_per_h": v.get("whole_set_decisions_per_h"),
                             "tokens_per_s": v.get("tokens_per_s"), "gpu_util_mean": (v.get("gpu") or {}).get("util_mean"),
                             "failed": v.get("failed")} for k, v in s.items()}
    out["throughput_N_c64"] = {k: v.get("decisions_per_h") for k, v in (tp.get("N_c64") or {}).items()}
    out["throughput_P_sat"] = {k: {"decisions_per_h": v.get("decisions_per_h"), "gpu_util_mean": (v.get("gpu") or {}).get("util_mean")}
                               for k, v in (tp.get("P_sat") or {}).items()}
    pf = steps.get("parity_full") or steps.get("parity_sub") or {}
    out["parity_pass_throughput"] = (pf.get("summary") or {}).get("decisions_per_h")
    out["gpu_busy_parity_pass"] = (pf.get("gpu") or {}).get("util_mean")
    out["prefix"] = {"R_cached_share": (steps.get("prefix") or {}).get("cached_token_share"),
                     "P_cached_share": pf.get("cached_token_share")}
    if meas.get("quant_report"):
        out["quant_report"] = meas["quant_report"]
    sr = steps.get("score_readout") or {}
    if sr:
        out["score_readout"] = {"latency_batch1_N": (sr.get("latency_batch1_N") or {}).get("wall_ms"),
                                "throughput_S": {k: v.get("decisions_per_h") for k, v in (sr.get("throughput_S") or {}).items()},
                                "parity_vs_generate": {k: (sr.get("parity") or {}).get("parity_vs_generate_same_boot", {}).get(k)
                                                       for k in ("n", "argmax_agree", "dp_max")}}
    return out


def voice_breakdown(voice: dict | None, vc1: dict | None) -> dict | None:
    """Voice latency after the end of speech = ASR final + C1 decision (cold, or with the static prefix already cached while
    the person spoke). Server-side numbers on the GPU; end-pointing (VAD hold / turn detection) and the network are NOT included."""
    if not voice or not vc1:
        return None
    lat = vc1.get("c1_latency_ms") or {}
    cold, warm = (lat.get("cold_flushed") or {}).get("p50"), (lat.get("prefix_warm") or {}).get("p50")
    out = {"c1_decision_ms_p50": {"cold": cold, "prefix_warm": warm}, "prefix_cached_share": lat.get("prefix_cached_share"), "modes": {}}
    for m, v in (voice.get("modes") or {}).items():
        asr = (v.get("final_flush_ms") or {}).get("p50") if m != "offline" else (v.get("total_ms") or {}).get("p50")
        asr95 = (v.get("final_flush_ms") or {}).get("p95") if m != "offline" else (v.get("total_ms") or {}).get("p95")
        agree = ((vc1.get("modes") or {}).get(m) or {}).get("argmax_agree")
        out["modes"][m] = {"asr_final_ms_p50": asr, "asr_final_ms_p95": asr95, "wer_mean": v.get("wer_mean"),
                           "decision_agreement_vs_text": agree,
                           "total_after_speech_ms_p50": {"cold": round(asr + cold, 1) if asr is not None and cold is not None else None,
                                                         "prefix_warm": round(asr + warm, 1) if asr is not None and warm is not None else None}}
    return out


def find_up(run: Path, name: str, levels: int = 4):
    d = run
    for _ in range(levels):
        if (d / name).exists():
            return load_json(d / name)
        d = d.parent
    return None


def build(run_dir, items_path=None, base_path=None) -> dict:
    """base_path: S1's answers_P.jsonl of ANOTHER session (the second session has no S1 parity block of its own)."""
    run = Path(run_dir)
    items = C.read_jsonl(items_path or C.ROOT / "data" / "P.jsonl")
    base = read_answers(base_path or run / "s1" / "answers_P.jsonl")
    configs = sorted([p.name for p in run.iterdir() if p.is_dir() and (p / "block.json").exists()],
                     key=lambda n: (K.CONFIGS[n].priority if n in K.CONFIGS else 99, n))
    out = {"run": str(run), "configs": {n: config_summary(run, n, items, base) for n in configs}}
    # Like-for-like cost basis: EVERY config's saturation throughput on the SAME workload (N_c64 = the 660-call traffic-like mix
    # at 64 concurrent; S c64 = the 660-call heavy mix is the second table). The first report took the best of all workloads per
    # config, which gave s1 its P_sat figure (359K/h, a bigger run) and the others their S figure (a harder mix): not comparable.
    thr, thr_s = {}, {}
    for n, c in out["configs"].items():
        v_s = ((c.get("throughput") or {}).get("c64") or {}).get("decisions_per_h")
        v = (c.get("throughput_N_c64") or {}).get("c64") or v_s       # N_c64; S c64 only when a config has no N run
        if v:
            thr[n] = {"dph": v}
        if v_s:
            thr_s[n] = {"dph": v_s}
    s1 = out["configs"].get("s1") or {}
    b8 = ((s1.get("latency_ms") or {}).get("batched8_per_decision") or {}).get("p50")
    if "s1" in thr and b8:
        thr["s1"]["ms_per_decision"] = b8
    out["cost_basis"] = "N_c64: 660 traffic-like calls, 64 concurrent, same for every config"
    out["cost"] = CM.table(thr) if thr else None
    out["cost_text"] = CM.render(out["cost"]) if out["cost"] else None
    out["cost_heavy_S_c64"] = CM.table(thr_s) if thr_s else None
    out["cost_heavy_text"] = CM.render(out["cost_heavy_S_c64"]) if out["cost_heavy_S_c64"] else None
    e2e = find_up(run, "e2e_client.json")
    if e2e:
        out["e2e"] = e2e
        for lv in e2e.get("levels", []):
            recs = [r["total_ms"] for r in lv.get("records", []) if r.get("ok") and r.get("total_ms") is not None]
            if len(recs) >= 50:
                p95 = C.pct(recs, 0.95)
                out["hedge_estimate"] = {"level": lv.get("name"), **CM.hedge_estimate(recs, hedge_after_ms=p95)}
                break
    cold = find_up(run, "cold_start.json")
    if cold:
        out["cold_start"] = cold
    jev = find_up(run, "jev_sample.json")
    if jev:
        out["jev_sample"] = {k: v for k, v in jev.items() if k != "records"}
    v = load_json(run / "s1" / "vision.json")
    if v:
        out["vision"] = {a: {k: x.get(k) for k in ("n", "acc", "agree_with_native", "ms_per_decision", "visual_tokens_pred", "token_mismatches", "by_suite")}
                         for a, x in (v.get("arms") or {}).items()}
    vc = load_json(run / "s1" / "voice_c1.json")
    if vc:
        out["voice_c1"] = vc
        vr = load_json(run.parent.parent / "voice" / "voice_result.json") or load_json(run / "voice_result.json")
        out["voice_breakdown"] = voice_breakdown(vr, vc)
    return out


def render(summary: dict) -> str:
    lines = []
    for n, c in summary["configs"].items():
        p = c.get("parity_vs_s1") or {}
        lat = (c.get("latency_ms") or {}).get("batch1_N") or {}
        b8 = (c.get("latency_ms") or {}).get("batched8_per_decision") or {}
        tp = (c.get("throughput") or {})
        best = max([(v.get("decisions_per_h") or 0) for v in tp.values()] or [0])
        n64 = ((c.get("throughput_N_c64") or {}).get("c64") or 0)
        lines.append(f"{n:18s} boot {c.get('boot_s')}s  parity {p.get('argmax_agree')} (flips {p.get('n_flips')}, max|dp| {p.get('dp_max')})  "
                     f"{c.get('verdict', '-'):>9s}  b1 p50/p95 {lat.get('p50')}/{lat.get('p95')} ms  b8/dec {b8.get('p50')} ms  "
                     f"sat N {n64:.0f}/h, S {best:.0f}/h  err {c.get('error') or c.get('skipped') or ''}")
    if summary.get("cost_text"):
        lines += ["", "USD per 1K decisions (Modal on-demand, any region) by utilisation:", summary["cost_text"]]
    return "\n".join(lines)


if __name__ == "__main__":
    s = build(sys.argv[1], base_path=(sys.argv[2] if len(sys.argv) > 2 else None))
    C.write_json(Path(sys.argv[1]) / "summary.json", s)
    print(render(s))
