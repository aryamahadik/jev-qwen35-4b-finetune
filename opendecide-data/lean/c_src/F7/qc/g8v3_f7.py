"""G8 for F7 under the adopted rule (PREREG A19.1, c_build/g8v2/A19_ADOPTED): choice parts pass if the G8v3 exact
within-card permutation p-value > 0.009 (shared tool c_src/common/g8_aflite.py, not changed). F7 rows are all choice
rows. The shared tool has no F7 adapter; it is registered IN-PROCESS exactly as qc/g8.py registers it (split "sent",
options with their card definition line, seed0 7700). The old raw share (spec 8: < 10%) is reported too.
Cache and run files go to F7/tmp/chk/g8v3. Usage: g8v3_f7.py [candidates_r1] [jobs]"""
import json, sys
from pathlib import Path
F7 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F7")
sys.path.insert(0, str(F7.parent / "common"))
import g8_aflite as g8

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 4
g8.ADAPTERS["F7"] = dict(g8._BASE, split="sent", opt_defs=True, seed0=7700)
g8.FAMILY_G8["F7"] = F7 / "qc/__no_family_g8__.json"
g8.OUTDIR = F7 / "tmp/chk/g8v3"
g8.CACHE = g8.OUTDIR / "cache"
g8.CACHE.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    out = F7 / f"qc/g8v3_{NAME}.json"
    rep = g8.family_report("F7", str(F7 / f"out/{NAME}.jsonl"), str(out), JOBS)
    d = rep["parts"]["choice"]
    summ = {"rule": "A19.1: choice part PASS if G8v3 p > 0.009", "p": d["test"].get("p"), "K": d["test"].get("K"),
            "verdict": d["test"].get("verdict"), "pass": d["pass"], "real": d["real"],
            "old_raw_share_seed0": rep.get("old_rule", {}).get("raw_share_all_rows_seed0"),
            "old_rule_lt_10pct": rep.get("old_rule", {}).get("verdict_lt_10pct")}
    print("F7_G8V3", json.dumps(summ))
