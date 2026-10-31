"""A17 phase-B pass rules B1 and B2, coded exactly as pre-registered (PREREG_FINAL.md A17, written before any result).
Aggregates only: no per-item output is written or printed.

A17 text:
  B1: fast-path p50 <= 50 ms compute on the H100. On clean math sets, the think path keeps >= 85% of full-thinking
      accuracy at <= 1 s median. FP8 loses <= 1 pt.
  B2: >= 25% fewer think tokens at >= 98% of B1's accuracy.
  A step that fails is not shipped.
Readings fixed here, before any result (each is printed in the output):
  R1 "clean math sets" = rows with think_type "math" in the finalised clean sets (clean_sets.py manifest), part
     dev_confirm by default (dev-confirm is run once). Pooled over the sets (micro); per-set numbers are reported only.
  R2 accuracy = the record's final_key (A17-B0b: an unparsed think answer falls back to C1's answer) equals the gold
     key; a row without a record counts as missing and makes the rule "incomplete" (= not passed).
  R3 "full-thinking accuracy" = policies.py full_think records (8,192 tokens, no early exit) on the same rows.
     keep ratio = acc(think path) / acc(full thinking) >= 0.85 (undefined when full thinking scores 0 -> not passed).
  R4 "median" = median per-request wall seconds (think + answer) of the think path on those rows, measured one request
     at a time (group_size 1) on the H100; records at batch > 1 do not count as a latency measurement -> not passed.
  R5 FP8: the same think path in FP8 and BF16 on the same rows, paired; loss = acc(BF16) - acc(FP8) in points <= 1.0
     (point estimate; a paired bootstrap 95% CI is reported). The FP8 rule gates FP8 only (FAST_THINK_PLAN S2 "keep
     FP8 only if ... else BF16"; FINAL_ARCHITECTURE 8 lists the FP8 check as its own step): no FP8 records, or FP8
     records that fail, = FP8 is not shipped and BF16 ships; B1 itself = fast path (R6) AND the math rule (R1-R4),
     whose --think records must then be the BF16 ones.
  R6 fast path: p50 ms per decision at batch 1 from the B1 app (modal_think.py summary.json b1_checks.fast_p50_ms).
  R7 B2 tokens = mean think_tokens_sum per row (every try counted); B2 rows = the rows of the B1 think-path records;
     pass = mean_tokens(B2) <= 0.75 * mean_tokens(B1) and acc(B2) >= 0.98 * acc(B1).

  python think/eval_think.py b1 --think T.jsonl --full F.jsonl [--fp8 P8.jsonl --bf16 P16.jsonl] \\
      (--b1-summary think/runs/<run>/summary.json | --fast-p50-ms X) [--part dev_confirm] [--out report.json]
  python think/eval_think.py b2 --b1 B1.jsonl --b2 B2.jsonl [--part dev_confirm] [--out report.json]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import gold_key, read_jsonl, sha256_file  # noqa: E402

CLEAN = HERE / "data" / "clean"
FAST_MS, KEEP, MEDIAN_S, FP8_PTS = 50.0, 0.85, 1.0, 1.0  # B1
TOK_CUT, ACC_KEEP = 0.75, 0.98  # B2


def load_rows(clean_dir=CLEAN, part="dev_confirm", think_type=None) -> dict:
    """Finalised clean rows (manifest sets only), filtered to one part and optionally one think_type."""
    man = json.loads((Path(clean_dir) / "manifest.json").read_text())
    out = {}
    for name, info in man["sets"].items():
        f = Path(clean_dir) / f"{name}.jsonl"
        if sha256_file(f) != info["sha256"]:
            raise SystemExit(f"{name}: file differs from the frozen manifest")
        for r in read_jsonl(f):
            if (part == "all" or r["split"] == part) and (think_type is None or r.get("think_type") == think_type):
                out[r["id"]] = r
    return out


def load_recs(path) -> dict:
    recs = {}
    for r in read_jsonl(path):
        if r["id"] in recs:
            raise SystemExit(f"{path}: duplicate record for one row")
        recs[r["id"]] = r
    return recs


def ok(row, rec) -> float:
    k = rec.get("final_key", rec.get("pred_key"))
    return float(k is not None and k == gold_key(row))


def _acc(rows, recs, ids=None) -> float:
    ids = list(ids if ids is not None else rows)
    return 100.0 * sum(ok(rows[i], recs[i]) for i in ids) / len(ids) if ids else float("nan")


def _missing(rows, recs) -> int:
    return sum(1 for i in rows if i not in recs)


def paired_ci(rows, a, b, n_boot=2000, seed=0) -> list:
    """95% bootstrap CI of acc(a) - acc(b) in points over the same rows."""
    ids = list(rows)
    d = np.array([ok(rows[i], a[i]) - ok(rows[i], b[i]) for i in ids])
    rng = np.random.default_rng(seed)
    bs = [100 * d[rng.integers(0, len(d), len(d))].mean() for _ in range(n_boot)]
    return [round(float(np.percentile(bs, 2.5)), 2), round(float(np.percentile(bs, 97.5)), 2)]


def per_set(rows, recs) -> dict:
    by = {}
    for i, r in rows.items():
        by.setdefault(r.get("set", "?"), []).append(i)
    return {s: {"n": len(ids), "acc": round(_acc(rows, recs, [i for i in ids if i in recs]), 2)} for s, ids in by.items()}


def rule_fast(p50_ms) -> dict:
    if p50_ms is None:
        return {"status": "not_measured", "pass": False}
    return {"status": "measured", "p50_ms": round(float(p50_ms), 3), "limit_ms": FAST_MS, "pass": float(p50_ms) <= FAST_MS}


def rule_math(rows, think, full) -> dict:
    """B1: on clean math rows, acc(think) >= 0.85 * acc(full thinking) and median wall <= 1 s (R1-R4)."""
    if not rows:
        return {"status": "no_math_rows", "pass": False}
    mt, mf = _missing(rows, think), _missing(rows, full)
    rep = {"n": len(rows), "missing_think": mt, "missing_full": mf}
    if mt or mf:
        return {**rep, "status": "incomplete", "pass": False}
    rep["think_policies"] = sorted({str(think[i].get("policy")) for i in rows})
    rep["full_policies"] = sorted({str(full[i].get("policy")) for i in rows})
    if "full_think" in rep["think_policies"] or set(rep["full_policies"]) - {"full_think", "None"}:
        return {**rep, "status": "wrong_policy (think must not be full_think; full must be full_think)", "pass": False}
    at, af = _acc(rows, think), _acc(rows, full)
    ratio = at / af if af > 0 else None
    walls = [float(think[i]["wall_s"]) for i in rows]
    batch1 = all(think[i].get("group_size") == 1 for i in rows)
    med = statistics.median(walls)
    ct, cf = (sum(ok(rows[i], x[i]) for i in rows) for x in (think, full))
    keep_ok = cf > 0 and 100 * ct >= round(100 * KEEP) * cf  # exact integer test of ct / cf >= 0.85
    lat_ok = batch1 and med <= MEDIAN_S
    return {**rep, "status": "measured", "acc_think": round(at, 2), "acc_full": round(af, 2),
            "keep_ratio": None if ratio is None else round(ratio, 4), "keep_min": KEEP, "keep_pass": keep_ok,
            "median_wall_s": round(med, 4), "median_max_s": MEDIAN_S, "latency_at_batch1": batch1,
            "latency_pass": lat_ok, "think_minus_full_ci95": paired_ci(rows, think, full),
            "fallback_share": round(sum(bool(think[i].get("fallback")) for i in rows) / len(rows), 4),
            "think_tokens_mean": round(statistics.mean(float(think[i].get("think_tokens", 0)) for i in rows), 1),
            "full_tokens_mean": round(statistics.mean(float(full[i].get("think_tokens", 0)) for i in rows), 1),
            "per_set": {"think": per_set(rows, think), "full": per_set(rows, full)}, "pass": keep_ok and lat_ok}


def rule_fp8(rows, fp8, bf16) -> dict:
    """B1: acc(BF16) - acc(FP8) <= 1.0 pt on the same rows (R5). Rows = the BF16 records' rows in this part."""
    if fp8 is None:
        return {"status": "n/a: FP8 not shipped (BF16 ships)", "pass": None}
    scope = {i: r for i, r in rows.items() if i in bf16}
    if not scope:
        return {"status": "no_rows", "pass": False}
    miss = _missing(scope, fp8)
    if miss:
        return {"status": "incomplete", "n": len(scope), "missing_fp8": miss, "pass": False}
    loss = _acc(scope, bf16) - _acc(scope, fp8)
    return {"status": "measured", "n": len(scope), "acc_bf16": round(_acc(scope, bf16), 2),
            "acc_fp8": round(_acc(scope, fp8), 2), "loss_pts": round(loss, 2), "max_loss_pts": FP8_PTS,
            "bf16_minus_fp8_ci95": paired_ci(scope, bf16, fp8),
            "pass": 100 * (sum(ok(scope[i], bf16[i]) for i in scope) - sum(ok(scope[i], fp8[i]) for i in scope))
            <= FP8_PTS * len(scope)}  # exact: loss in points <= 1.0


def rule_b2(rows, b1, b2) -> dict:
    """B2 (R7): mean think tokens(B2) <= 0.75 x B1 and acc(B2) >= 0.98 x acc(B1), on the B1 records' rows."""
    scope = {i: r for i, r in rows.items() if i in b1}
    if not scope:
        return {"status": "no_rows", "pass": False}
    miss = _missing(scope, b2)
    if miss:
        return {"status": "incomplete", "n": len(scope), "missing_b2": miss, "pass": False}
    tok = lambda recs: [float(recs[i].get("think_tokens_sum", recs[i].get("think_tokens", 0))) for i in scope]
    t1, t2 = sum(tok(b1)), sum(tok(b2))
    k1, k2 = (sum(ok(scope[i], x[i]) for i in scope) for x in (b1, b2))
    tok_ok = 100 * t2 <= round(100 * TOK_CUT) * t1  # exact: mean(B2) <= 0.75 * mean(B1), same rows
    acc_ok = 100 * k2 >= round(100 * ACC_KEEP) * k1  # exact: acc(B2) >= 0.98 * acc(B1)
    n = len(scope)
    return {"status": "measured", "n": n, "tokens_mean_b1": round(t1 / n, 1), "tokens_mean_b2": round(t2 / n, 1),
            "token_cut": round(1 - t2 / t1, 4) if t1 else None, "token_cut_min": 1 - TOK_CUT, "tokens_pass": tok_ok,
            "acc_b1": round(100 * k1 / n, 2), "acc_b2": round(100 * k2 / n, 2),
            "acc_ratio": round(k2 / k1, 4) if k1 else None, "acc_ratio_min": ACC_KEEP, "acc_pass": acc_ok,
            "b2_minus_b1_ci95": paired_ci(scope, b2, b1), "per_set": {"b1": per_set(scope, b1), "b2": per_set(scope, b2)},
            "pass": tok_ok and acc_ok}


SPEC_PTS, DEER_PTS, DEER_MIN_EXITS = 2.0, 2.0, 20  # A30 (FAST_THINK_PLAN 4a S1 / T1)


def rule_spec_acc(rows, spec, ref) -> dict:
    """A30 S1 accuracy part: a speculation arm's short_cot answers (batch 1) are within +-2 pts of the no-spec arm's
    short_cot answers (batched) on the same rows, every row present (speculation is lossless; a gap means a bug)."""
    if not rows:
        return {"status": "no_rows", "pass": False}
    ms, mr = _missing(rows, spec), _missing(rows, ref)
    if ms or mr:
        return {"status": "incomplete", "n": len(rows), "missing_spec": ms, "missing_ref": mr, "pass": False}
    cs = int(sum(ok(rows[i], spec[i]) for i in rows))
    cr = int(sum(ok(rows[i], ref[i]) for i in rows))
    return {"status": "measured", "n": len(rows), "acc_spec": round(100 * cs / len(rows), 2),
            "acc_nospec": round(100 * cr / len(rows), 2), "diff_pts": round(100 * (cs - cr) / len(rows), 2),
            "max_abs_pts": SPEC_PTS, "spec_minus_nospec_ci95": paired_ci(rows, spec, ref),
            "pass": 100 * abs(cs - cr) <= SPEC_PTS * len(rows)}  # exact: |diff| in points <= 2.0


def rule_deer(rows, deer, plain) -> dict:
    """A30 (FAST_THINK_PLAN 4a T1): on the rows where DEER exited early, acc(DEER) >= acc(same rows, full 1,024 budget
    without DEER) - 2 pts; at least 20 early exits. Pass = DEER stays on in capped_think; else capped_think runs plain."""
    if not rows:
        return {"status": "no_rows", "pass": False}
    md, mp = _missing(rows, deer), _missing(rows, plain)
    if md or mp:
        return {"status": "incomplete", "n": len(rows), "missing_deer": md, "missing_plain": mp, "pass": False}
    ex = [i for i in rows if deer[i].get("exit") == "deer"]
    tok = lambda d: statistics.mean(float(d[i].get("think_tokens", 0)) for i in rows)  # noqa: E731
    rep = {"n": len(rows), "early_exits": len(ex), "acc_deer_all": round(_acc(rows, deer), 2),
           "acc_plain_all": round(_acc(rows, plain), 2), "tokens_ratio": round(tok(deer) / max(1e-9, tok(plain)), 4),
           "min_exits": DEER_MIN_EXITS, "max_loss_pts": DEER_PTS}
    if len(ex) < DEER_MIN_EXITS:
        return {**rep, "status": "too_few_early_exits", "pass": False}
    cd = int(sum(ok(rows[i], deer[i]) for i in ex))
    cp = int(sum(ok(rows[i], plain[i]) for i in ex))
    return {**rep, "status": "measured", "acc_deer_exited": round(100 * cd / len(ex), 2),
            "acc_plain_same_rows": round(100 * cp / len(ex), 2), "pass": 100 * cd >= 100 * cp - DEER_PTS * len(ex)}


def fast_p50(a):
    if a.fast_p50_ms is not None:
        return a.fast_p50_ms, "flag"
    if a.b1_summary:
        s = json.loads(Path(a.b1_summary).read_text())
        return (s.get("b1_checks") or {}).get("fast_p50_ms"), a.b1_summary
    return None, None


READINGS = [l.strip() for l in __doc__.split("Readings fixed here")[1].split("python think/eval_think.py")[0]
            .splitlines()[1:] if l.strip()]


def cmd_b1(a):
    if a.fp8 and not a.bf16:
        raise SystemExit("--fp8 needs --bf16 (the paired BF16 run of the same think path)")
    math_rows = load_rows(a.clean, a.part, "math")
    all_rows = load_rows(a.clean, a.part)
    p50, src = fast_p50(a)
    rep = {"rule": "B1", "part": a.part, "fast": {**rule_fast(p50), "source": src},
           "math": rule_math(math_rows, load_recs(a.think), load_recs(a.full)),
           "fp8": rule_fp8(all_rows, load_recs(a.fp8) if a.fp8 else None, load_recs(a.bf16) if a.bf16 else {})}
    rep["pass"] = bool(rep["fast"]["pass"] and rep["math"]["pass"])  # R5: FP8 gates FP8 only
    rep["ship_fp8"] = bool(rep["pass"] and rep["fp8"]["pass"] is True)
    _finish(a, rep, {"think": a.think, "full": a.full, "fp8": a.fp8, "bf16": a.bf16})


def cmd_b2(a):
    rep = {"rule": "B2", "part": a.part, **rule_b2(load_rows(a.clean, a.part), load_recs(a.b1), load_recs(a.b2))}
    _finish(a, rep, {"b1": a.b1, "b2": a.b2})


def _finish(a, rep, inputs):
    rep["readings"] = READINGS
    rep["inputs"] = {k: {"path": v, "sha256": sha256_file(v)} for k, v in inputs.items() if v}
    rep["clean_manifest_sha256"] = sha256_file(Path(a.clean) / "manifest.json")
    if a.out:
        Path(a.out).write_text(json.dumps(rep, indent=2) + "\n")
    brief = {k: (v.get("pass") if isinstance(v, dict) else v) for k, v in rep.items() if k not in ("readings", "inputs")}
    print(json.dumps(brief, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("b1", "b2"):
        p = sub.add_parser(name)
        p.add_argument("--clean", default=str(CLEAN))
        p.add_argument("--part", default="dev_confirm", choices=["dev_confirm", "dev_fit", "all"])
        p.add_argument("--out", default=None)
        if name == "b1":
            p.add_argument("--think", required=True, help="policies.py records of the think path (H100, batch 1)")
            p.add_argument("--full", required=True, help="policies.py --policy full_think records, same rows")
            p.add_argument("--fp8", default=None)
            p.add_argument("--bf16", default=None)
            p.add_argument("--b1-summary", default=None, help="modal_think.py runs/<run>/summary.json")
            p.add_argument("--fast-p50-ms", type=float, default=None)
            p.set_defaults(func=cmd_b1)
        else:
            p.add_argument("--b1", required=True)
            p.add_argument("--b2", required=True)
            p.set_defaults(func=cmd_b2)
    a = ap.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
