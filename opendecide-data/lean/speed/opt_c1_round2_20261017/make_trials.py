"""make_trials.py: build TRIALS.json + TRIALS.md from ./results/<trial>/ (pulled with pull_results.sh) and the offline checks.

Every trial row is computed from files; a trial with no summary.json is reported NOT RUN (verdict NA). Numbers only.
Verdicts: exact = 0 flips and max|dp| <= 1e-5 vs T0a; pass = Wilson 95% lower bound >= 0.995 on all 8,143 and on each view type
(not bit-exact); fail = bar missed, refused boot or errors; NA = not run / not applicable.
Gain: batch-1 p50/p95/p99 (mean of the two 320-call reps) and c64 decisions/h against T0a (L4 absolute numbers do not transfer
to H100; the relative change does). Noise = |T0a - T0b| on the same quantities.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r2_report as RP  # noqa: E402

RES = HERE / "results"

TRIALS = [
    ("T0a", "BF16 baseline (reference for every parity), production flags on port 30010", ""),
    ("T0b", "BF16 baseline again after a reboot + a second parity pass at c64 (self-agreement floor)", ""),
    ("T1", "diagnostics: --enable-metrics --enable-cache-report --gc-warning-threshold-secs 0.005 + py-spy", "diag only"),
    ("T2", "--cuda-graph-backend-prefill full (GDN layers must be inside the capture, no fallback)", "--cuda-graph-backend-prefill full"),
    ("T4a", "input_ids (as today) + --skip-tokenizer-init, /generate readout", "--skip-tokenizer-init"),
    ("T4b", "/v1/score readout on token ids", "backend=score"),
    ("T4c", "/v1/score + --skip-tokenizer-init", "backend=score --skip-tokenizer-init"),
    ("T5", "LM head sliced to the 141 option-token rows (copied rows, fp32 accumulate, embed_tokens untouched)", "R2_LMHEAD_IDS patch"),
    ("T3", "GC fix: gc.freeze() after warm-up (only if T1 shows pauses)", "R2_GC_FREEZE patch"),
    ("T8", "block-FP8 checkpoint (128x128 weights, dynamic activations), --quantization fp8", "--quantization fp8, model c1_fp8_block"),
    ("T6", "--mamba-ssm-dtype bfloat16", "--mamba-ssm-dtype bfloat16"),
    ("T7", "--mamba-track-interval 64", "--mamba-track-interval 64"),
    ("T10a", "image noise floor: native x2 at c1 and c8 (200 images)", "vision, no flag"),
    ("T10b", "image: --keep-mm-feature-on-device", "--keep-mm-feature-on-device"),
    ("T10c", "image: --mm-processor-worker-num 4", "--mm-processor-worker-num 4"),
    ("T10d", "image: client-side exact-size pre-resize", "vision, client side"),
    ("T9", "live FP8 + BF16 cascade (only if T8 or the gate passes on held-out data)", "two servers + router"),
    ("T11", "--prefill-only-disable-kv-cache + --disable-radix-cache (exploratory)", "two flags"),
]


def lat(summary):
    reps = [summary["phases"][k]["wall_ms"] for k in ("lat1", "lat2") if k in summary["phases"]]
    if not reps:
        return None
    out = {q: round(sum(r[q] for r in reps) / len(reps), 2) for q in ("p50", "p95", "p99", "mean")}
    out["reps"] = [{q: r[q] for q in ("p50", "p95", "p99")} for r in reps]
    return out


def thr(summary):
    t = summary["phases"].get("thr")
    if not t:
        return None
    s = next(iter(t.values()))
    return {"decisions_per_h": s["decisions_per_h"], "tokens_per_s": s["tokens_per_s"], "ok": s["ok"], "calls": s["calls"],
            "failed": s["failed"], "gpu_busy_mean": (s.get("gpu") or {}).get("util_mean"), "cached_token_share": s.get("cached_token_share")}


def row_for(name, desc, flags, items, ref):
    row = {"trial": name, "what": desc, "flags": flags, "status": "NOT RUN", "verdict": "NA"}
    d = RES / name
    sm = d / "summary.json"
    if not sm.exists():
        return row
    s = json.loads(sm.read_text())
    row["status"] = "RAN"
    row["lat_batch1_ms"] = lat(s)
    row["throughput_c64"] = thr(s)
    p = s["phases"].get("parity")
    if p:
        row["gpu_busy_parity"] = (p.get("gpu") or {}).get("util_mean")
        row["token_count_equal"] = (p["n_missing"] == 0)
        row["cached_token_share_parity"] = p.get("cached_token_share")
    la = s["phases"].get("lat1")
    if la:
        row["gpu_busy_batch1"] = (la.get("gpu") or {}).get("util_mean")
    pr = s["phases"].get("prefix")
    if pr:
        row["R_prefix_cached_share"] = pr["cached_token_share"]
    ans = d / "answers_P.jsonl"
    if ref is not None and ans.exists() and name != "T0a":
        rep, _ = RP.parity(ref, RP.load_answers(ans), items)
        row["parity_vs_T0a"] = rep
        o = rep["overall"]
        if rep["missing"] or not o["pass_wilson"] or any(not (g["pass_wilson"] or g["underpowered"]) for g in rep["by_view_type"].values()):
            row["verdict"] = "fail"
        elif o["flips"] == 0 and rep["dp"]["max"] is not None and rep["dp"]["max"] <= 1e-5:
            row["verdict"] = "exact"
        else:
            row["verdict"] = "pass"
    elif name == "T0a":
        row["verdict"] = "NA"
        row["note"] = "reference"
    return row


def main():
    items = RP.load_items()
    ref = RP.load_answers(RES / "T0a" / "answers_P.jsonl") if (RES / "T0a" / "answers_P.jsonl").exists() else None
    rows = [row_for(n, d, f, items, ref) for n, d, f in TRIALS]
    base = next((r for r in rows if r["trial"] == "T0a" and r.get("lat_batch1_ms")), None)
    for r in rows:
        if base and r.get("lat_batch1_ms") and r["trial"] != "T0a":
            r["delta_vs_T0a"] = {q: round(r["lat_batch1_ms"][q] - base["lat_batch1_ms"][q], 2) for q in ("p50", "p95", "p99")}
            if r.get("throughput_c64") and base.get("throughput_c64"):
                r["delta_vs_T0a"]["throughput_pct"] = round(100 * (r["throughput_c64"]["decisions_per_h"] / base["throughput_c64"]["decisions_per_h"] - 1), 2)
    doc = json.loads((HERE / "TRIALS_STATIC.json").read_text()) if (HERE / "TRIALS_STATIC.json").exists() else {}
    doc["rows"] = rows
    (HERE / "TRIALS.json").write_text(json.dumps(doc, indent=1))
    md = [doc.get("md_head", "# TRIALS (round 2, Track A)\n"), "\n## Trial table\n",
          "| trial | what | status | verdict | agree vs T0a (Wilson LB) | flips | max dp | batch-1 p50/p95/p99 ms | c64 dec/h | GPU busy % (b1 / c64) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        pv = r.get("parity_vs_T0a", {}).get("overall", {})
        l = r.get("lat_batch1_ms") or {}
        t = r.get("throughput_c64") or {}
        md.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            r["trial"], r["what"], r["status"], r["verdict"],
            f"{pv.get('agree_rate')} ({pv.get('wilson95', [None])[0]})" if pv else "-", pv.get("flips", "-"),
            r.get("parity_vs_T0a", {}).get("dp", {}).get("max", "-") if pv else "-",
            f"{l.get('p50')}/{l.get('p95')}/{l.get('p99')}" if l else "-", t.get("decisions_per_h", "-"),
            f"{r.get('gpu_busy_batch1', '-')} / {t.get('gpu_busy_mean', '-')}"))
    md.append("\n" + doc.get("md_tail", ""))
    (HERE / "TRIALS.md").write_text("\n".join(md))
    print("wrote TRIALS.json and TRIALS.md;", sum(1 for r in rows if r["status"] == "RAN"), "of", len(rows), "trials have results")


if __name__ == "__main__":
    main()
