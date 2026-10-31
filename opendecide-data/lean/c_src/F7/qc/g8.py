"""G8 for F7 (independent checker). C_DATA_SPEC 8 G8 (spec set-up: frozen MiniLM-L6, 64 partitions split 50/50 by card,
linear models, tau 0.75, predictable share < 10%) AND the shared A19 tool c_src/common/g8_aflite.py (G8v2: label-
permuted nulls K=20 within card + K=20 global; pass = real share <= min q95 AND pooled acc <= chance + 2 pp).
c_build/g8v2/A19_ADOPTED does not exist, so the spec rule (old raw share < 10%) is the verdict and G8v2 is reported.
The shared tool has no F7 adapter; this script registers one IN-PROCESS (the tool file is not changed):
  split "sent" (question = sentences of `instructions` holding '?'), sep "\n\n", options with their card definition
  line (as served), choice features [q, card, state, opt, opt*q], seed0 7700. Every F7 row is a choice row.
Embedding cache and run logs go to F7/tmp/chk (not c_build). Usage: g8.py [candidates_r1] [jobs]"""
import json, os, sys, time
from pathlib import Path
F7 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F7")
sys.path.insert(0, str(F7.parent / "common"))
import g8_aflite as g8

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 4
g8.ADAPTERS["F7"] = dict(g8._BASE, split="sent", opt_defs=True, seed0=7700)
g8.FAMILY_G8["F7"] = F7 / "qc/__no_family_g8__.json"
g8.OUTDIR = F7 / "tmp/chk/g8v2"; g8.CACHE = g8.OUTDIR / "cache"; g8.CACHE.mkdir(parents=True, exist_ok=True)


def main():
    out = F7 / f"qc/g8_{NAME}.json"
    rep = g8.family_report("F7", str(F7 / f"out/{NAME}.jsonl"), str(out), JOBS)
    d = rep["parts"]["choice"]
    spec = {"rule": "C_DATA_SPEC 8 G8: predictable share < 10% (grouped by card, all rows)",
            "raw_share": rep["old_rule"]["raw_share_all_rows"], "pass": rep["old_rule"]["verdict_lt_10pct"]}
    v2 = {"rule": rep["rule"], "real_share": d["real"]["share"], "threshold_min_q95": d["threshold"],
          "acc": d["real"]["acc"], "chance": d["chance"], "pass": rep["pass"],
          "null_within_q95": d["null_within_card"].get("q95"), "null_global_q95": d["null_global"].get("q95")}
    rep["F7_summary"] = {"A19_ADOPTED": (g8.LEAN / "c_build/g8v2/A19_ADOPTED").exists(), "spec_G8": spec, "G8v2": v2,
                         "verdict_source": "G8v2" if (g8.LEAN / "c_build/g8v2/A19_ADOPTED").exists() else "spec_G8"}
    out.write_text(json.dumps(rep, indent=1))
    print("F7_SUMMARY", json.dumps(rep["F7_summary"]))


if __name__ == "__main__":
    main()
