"""l4_parity_check.py: parity of the L4 serving path against the H100 S1 reference on the dev parity set P (CPU only).

The gate is the S1 rule (hosting/speed_bench.compare, SPEED-2 gate): on all 8,143 P decisions
  (1) argmax agreement of the candidate (L4, SGLang S1 path) with the reference (H100, SGLang S1, merged bf16) >= 99.5%
      (a missing candidate answer counts as a disagreement), AND
  (2) |accuracy(candidate) - accuracy(reference)| <= 0.3 pt (needs gold; a missing gold file makes the gate INCOMPLETE),
plus the L-D additions of plan section 6 (v3):
  (3) the prompt audit (prompt_audit.py) passed: identical rendered-prompt sha in trainer, gate and server, and thinking OFF
      in every rendered prompt (Qwen3.5 thinks by default; enable_thinking False).
Reported next to the gate, never replacing it (round-2 convention, oc1.parity): the Wilson 95% lower bound of the agreement
(bar 0.995; buckets too small to reach it are flagged UNDERPOWERED), per view type and per options bucket, max/mean/p99 |dp|,
the flips with the reference margin, the reference-vs-reference drift (H100 13 Oct vs H100 17 Oct) and the candidate's own
self-agreement floor (the same L4 server read at another batch size; BF16 batch-size noise).

  l4_parity_check.py --cand L4/answers_P.jsonl --ref REF/answers_P.jsonl [--ref2 REF2/answers_P.jsonl]
                     [--floor L4/answers_P_c1.jsonl] [--gold-dir ../../data | --gold gold.jsonl]
                     [--prompt-audit out/prompt_audit.json] [--cand-info server_info.json] --out out/l4_parity.json

Answer files: one JSON object per line {"id", "probs": {"yes","no"} | {option: p}} ("views" ignored). The reference files that
exist today for C1: speed/opt_c1_round2_20261017/h100/results/session_20261017_161152/.../r2_a/answers_P.jsonl (H100 S1 bf16,
17 Oct, c32 pass) and speed/speed2_20261013/S1/answers_P.jsonl (13 Oct). For a C2.1 model there is no H100 reference (a new
H100 session is paid and Modal is forbidden): use the HF-adapter read on the free L4 as the reference (plan section 6 base
rule, same 99.5%) and ask the owner about an H100 reference as a money question.
Counts and numbers only; row ids appear as 8-character hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

P_DEFAULT = C.LEAN / "speed" / "workloads" / "P.jsonl"
P_SHA256 = "95764485fcdfbec5a88b2382dd25b9e29c82f4f297f0921da9d34fe99a32876e"   # speed/workloads/manifest.json
P_CALLS = 8143


def hid(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()[:8]


def load_items(p_path) -> dict:
    items = {}
    for it in C.read_jsonl(p_path):
        q = next(iter(it["request"]["questions"].values()))
        items[it["id"]] = {"bucket": it["bucket"], "qtype": it["qtype"], "split": it.get("split"),
                           "options": list(q["options"]) if q.get("type") == "choice" else None}
    return items


def load_answers(path) -> dict:
    out = {}
    for d in C.read_jsonl(path):
        p = d.get("probs") or d.get("probabilities") or d.get("p")
        if p is not None:
            out[d["id"]] = {k: float(v) for k, v in p.items()}
    return out


def argmax_label(opts, p):
    """gate_dev.argmax_label: noul -> p_yes > 0.5; choice -> first maximum over the options."""
    if opts is None:
        return float(p.get("yes", 0.0)) > 0.5
    v = {o: float(p.get(o, 0.0)) for o in opts}
    return max(v, key=v.get)


def margin(opts, p) -> float:
    if opts is None:
        return abs(2.0 * float(p.get("yes", 0.0)) - 1.0)
    v = sorted((float(p.get(o, 0.0)) for o in opts), reverse=True)
    return v[0] - v[1] if len(v) > 1 else v[0]


def row_dp(opts, a, b) -> float:
    keys = ["yes", "no"] if opts is None else opts
    return max(abs(float(a.get(k, 0.0)) - float(b.get(k, 0.0))) for k in keys)


def load_gold(items: dict, gold_path=None, gold_dir=None) -> dict | None:
    """{id: gold} for the P ids. --gold FILE ({"id","gold"} per line) or --gold-dir DIR (reads DIR/<split>.jsonl of the dev
    splits named in P; refuses any path with 'ohs'). noul gold 1 -> "yes"; choice gold = the option text."""
    gold = {}
    if gold_path:
        for d in C.read_jsonl(gold_path):
            gold[d["id"]] = d["gold"]
    elif gold_dir:
        for sp in sorted({v["split"] for v in items.values() if v["split"]}):
            p = Path(gold_dir) / f"{sp}.jsonl"
            if not p.exists():
                return None
            for r in C.read_jsonl(p):
                if r["id"] in items:
                    gold[r["id"]] = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
    else:
        return None
    if len(gold) < len(items):
        print(f"WARNING: gold covers {len(gold)} of {len(items)} P ids: accuracy diff NOT computed", file=sys.stderr)
        return None
    return gold


def is_correct(opts, p, g) -> bool:
    """gate_dev.score: correct only when the set of maximal options is exactly {gold} (a tie counts as wrong)."""
    if p is None:
        return False
    keys = ["yes", "no"] if opts is None else opts
    v = {k: float(p.get(k, 0.0)) for k in keys}
    best = max(v.values())
    return [k for k, x in v.items() if x == best] == [g]


def group(rows: list) -> dict:
    n = len(rows)
    k = sum(r["same"] for r in rows)
    lo, hi = C.wilson(k, n)
    return {"n": n, "agree": k, "flips": n - k, "agree_rate": round(k / n, 6) if n else None,
            "wilson95": [round(lo, 6), round(hi, 6)],
            "underpowered": bool(n and C.wilson(n, n)[0] < C.PARITY_BAR),
            "wilson_lb_pass": bool(n and lo >= C.PARITY_BAR),
            "max_dp": round(max((r["dp"] for r in rows), default=0.0), 6)}


def compare(items: dict, cand: dict, ref: dict, gold: dict | None) -> dict:
    rows = []
    for i, it in items.items():
        if i not in ref:
            continue
        o, r, c = it["options"], ref[i], cand.get(i)
        if c is None:
            rows.append({"id": i, "bucket": it["bucket"], "qtype": it["qtype"], "same": False, "dp": 1.0, "missing": True,
                         "ref_margin": margin(o, r), "ok_c": False, "ok_r": gold is not None and is_correct(o, r, gold.get(i))})
            continue
        rows.append({"id": i, "bucket": it["bucket"], "qtype": it["qtype"], "missing": False,
                     "same": argmax_label(o, c) == argmax_label(o, r), "dp": row_dp(o, c, r), "ref_margin": margin(o, r),
                     "ok_c": gold is not None and is_correct(o, c, gold.get(i)),
                     "ok_r": gold is not None and is_correct(o, r, gold.get(i))})
    n = len(rows)
    rep = {"overall": group(rows), "missing_cand": sum(r["missing"] for r in rows)}
    rep["by_bucket"] = {b: group([r for r in rows if r["bucket"] == b]) for b in sorted({r["bucket"] for r in rows})}
    rep["by_view_type"] = {t: group([r for r in rows if r["qtype"] == t]) for t in sorted({r["qtype"] for r in rows})}
    dps = sorted(r["dp"] for r in rows if not r["missing"])
    rep["dp"] = {"mean": round(sum(dps) / len(dps), 7) if dps else None, "p99": round(C.pct(dps, 0.99), 6) if dps else None,
                 "max": round(dps[-1], 6) if dps else None}
    fl = [r for r in rows if not r["same"]]
    rep["flips"] = {"n": len(fl),
                    "ref_margin_le": {str(e): sum(1 for r in fl if r["ref_margin"] <= e) for e in (0.005, 0.01, 0.02, 0.05, 0.1)},
                    "examples": [{"h": hid(r["id"]), "bucket": r["bucket"], "ref_margin": round(r["ref_margin"], 4),
                                  "dp": round(r["dp"], 4)} for r in sorted(fl, key=lambda r: -r["ref_margin"])[:15]]}
    if gold is not None and n:
        okc, okr = sum(r["ok_c"] for r in rows), sum(r["ok_r"] for r in rows)
        rep["accuracy"] = {"acc_cand": round(100 * okc / n, 3), "acc_ref": round(100 * okr / n, 3),
                           "diff_pt": round(100 * (okc - okr) / n, 3), "n": n}
    return rep


def gate(rep: dict, expect_n: int | None, audit: dict | None) -> dict:
    ov = rep["overall"]
    agree_ok = bool(ov["n"] and ov["agree_rate"] >= C.PARITY_BAR)
    acc = rep.get("accuracy")
    acc_ok = None if acc is None else abs(acc["diff_pt"]) <= C.ACC_DIFF_BAR_PT
    full = expect_n is None or ov["n"] == expect_n
    audit_ok = None if audit is None else (audit.get("verdict") == "PASS")
    if not full:
        verdict = "INCOMPLETE (compared %d rows, expected %s)" % (ov["n"], expect_n)
    elif not agree_ok:
        verdict = "FAIL (argmax agreement below 99.5%)"
    elif acc_ok is False:
        verdict = "FAIL (accuracy difference above 0.3 pt)"
    elif audit_ok is False:
        verdict = "FAIL (prompt audit failed)"
    elif acc_ok is None or audit_ok is None:
        verdict = "INCOMPLETE (agreement passes; %s missing)" % " and ".join(
            x for x, v in (("gold/accuracy", acc_ok), ("prompt audit", audit_ok)) if v is None)
    else:
        verdict = "PASS"
    return {"verdict": verdict, "agreement_ge_995": agree_ok, "accuracy_diff_le_0p3pt": acc_ok, "prompt_audit_pass": audit_ok,
            "rule": "S1 rule (hosting/speed_bench.compare): argmax agreement >= 0.995 and |acc diff| <= 0.3 pt, on all P rows; "
                    "plus prompt audit (sha identity, thinking OFF)",
            "wilson_lb_ge_995_report_only": ov["wilson_lb_pass"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cand", required=True, help="L4 answers_P.jsonl")
    ap.add_argument("--ref", required=True, help="H100 S1 answers_P.jsonl (or, for C2.1, the HF-adapter read on the L4)")
    ap.add_argument("--ref2", help="a second reference run (reference drift)")
    ap.add_argument("--floor", help="the same L4 server read again at another batch size (self-agreement floor)")
    ap.add_argument("--p", default=str(P_DEFAULT))
    ap.add_argument("--gold", help="gold.jsonl: {id, gold} per line")
    ap.add_argument("--gold-dir", help="lean/data (reads <split>.jsonl of the dev splits named in P)")
    ap.add_argument("--prompt-audit", help="out/prompt_audit.json from prompt_audit.py")
    ap.add_argument("--cand-info", help="the L4 server's /server_info JSON (flags are recorded, never judged)")
    ap.add_argument("--ref-info", help="free text or JSON path describing the reference (GPU, date, session)")
    ap.add_argument("--allow-subset", action="store_true", help="test runs: accept fewer than 8,143 rows")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)

    items = load_items(a.p)
    p_sha = C.sha256_file(a.p)
    cand, ref = load_answers(a.cand), load_answers(a.ref)
    gold = load_gold(items, a.gold, a.gold_dir)
    audit = json.loads(Path(a.prompt_audit).read_text()) if a.prompt_audit else None
    expect = None if a.allow_subset else P_CALLS
    rep = compare(items, cand, ref, gold)
    res = {"utc": C.utc(), "window": os.environ.get("LD_WINDOW"),
           "tag": C.tag("author-run", n=rep["overall"]["n"], source=f"{a.cand} vs {a.ref}") if rep["overall"]["n"] else
                  C.tag("not-measured"),
           "inputs": {"P": a.p, "P_sha256": p_sha, "P_sha_matches_manifest": p_sha == P_SHA256,
                      "cand": a.cand, "cand_sha256": C.sha256_file(a.cand), "ref": a.ref, "ref_sha256": C.sha256_file(a.ref),
                      "gold": "none (accuracy diff not computed)" if gold is None else "dev gold, %d rows" % len(gold)},
           "parity": rep}
    if a.ref2:
        r2 = load_answers(a.ref2)
        res["reference_drift"] = {"what": "ref vs ref2 (same rule); shows how stable the H100 reference itself is",
                                  **compare(items, r2, ref, gold)["overall"]}
    if a.floor:
        fl = load_answers(a.floor)
        sub = {i: v for i, v in items.items() if i in fl}
        f = compare(sub, fl, cand, gold)
        res["self_floor"] = {"what": "the L4 candidate vs the same L4 server read at another batch size, on the ids the floor "
                                     "pass covers (BF16 batch noise)", "rows": len(sub), **f["overall"],
                             "dp": f["dp"]}
    if a.cand_info:
        try:
            si = json.loads(Path(a.cand_info).read_text())
            keep = {k: si.get(k) for k in ("version", "model_path", "attention_backend", "mem_fraction_static", "dtype",
                                           "quantization", "disable_radix_cache", "max_running_requests", "enable_fp32_lm_head",
                                           "cuda_graph_max_bs", "tp_size") if k in si}
            res["cand_server"] = keep
        except (OSError, ValueError) as e:
            res["cand_server"] = {"error": str(e)}
    if a.ref_info:
        res["ref_info"] = a.ref_info
    res["gate"] = gate(rep, expect, audit)
    if audit is not None:
        res["prompt_audit"] = {k: audit.get(k) for k in ("verdict", "n", "problems_n")}
    C.write_json(a.out, res)
    ov = rep["overall"]
    print(f"n={ov['n']} agree={ov['agree_rate']} flips={ov['flips']} wilson95={ov['wilson95']} -> {res['gate']['verdict']}")
    return 0 if res["gate"]["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
