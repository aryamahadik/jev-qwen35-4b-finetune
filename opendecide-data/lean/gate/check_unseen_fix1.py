"""A8 precondition (CPU, read only, no look): adding C4's extra training file data/v14_parts/fix1_train.jsonl to the 12
registered training files leaves the ship rule's unseen-source set exactly as frozen, so the frozen 12-file derivation
that gate_dev.py --mode ship uses (and needs for a FINAL verdict) stays valid for C4.

Runs yn2b/check_unseen.check("v14_parts/fix1_train") (gate_dev.derive_unseen over the 12 files + fix1_train: name rule
and text guard) and requires:
  - the derived set equals gate_dev.UNSEEN_FROZEN_ROWS (17 sources, 3,847 rows) and the text guard flags nothing;
  - every fix1 source is either a golden_train source (already in the 12 files) or a gd_gen3_* (yn2b) source;
  - no gd_gen3_* source name matches a dev source (gate_dev.source_seen, both directions).
check_unseen's two yn2b-file-only assertions ("only gd_gen3_* sources", "no fix1 source name equals a dev source") do
not apply to a file that holds golden_train replay rows: those sources are golden_train's and are already "seen" through
the 12 files. They are replaced by the second and third conditions above. Exit 0 = pass, 1 = fail.
  python gate/check_unseen_fix1.py
"""
import json
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "yn2b"))
import check_unseen as cu  # noqa: E402
import gate_dev  # noqa: E402

FIX1 = "v14_parts/fix1_train"
YN2B_ONLY = ("yn2b source names match dev sources", "yn2b file holds non-gd_gen3_* sources")


def sources(path):
    out = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.add(json.loads(line)["source"])
    return out


def main():
    res = cu.check(FIX1)
    out = {"unseen_sources": res.get("unseen_sources"), "unseen_rows": res.get("unseen_rows"),
           "flagged": res.get("flagged"), "overlap": res.get("overlap"), "problems": []}
    out["problems"] += [p for p in res["problems"] if not p.startswith(YN2B_ONLY)]
    fix1 = set(res.get("yn2b_sources") or sources(LEAN / f"data/{FIX1}.jsonl"))
    gen3 = {s for s in fix1 if s.startswith("gd_gen3_")}
    golden = sources(LEAN / "data/v14_parts/golden_train.jsonl")
    new = sorted(fix1 - gen3 - golden)
    if new:
        out["problems"].append(f"fix1 sources outside golden_train and gd_gen3_*: {new}")
    dev = set()
    for sp in gate_dev.SPLITS.split(","):
        dev |= sources(LEAN / f"data/{sp}.jsonl")
    clash = {g: hits for g in sorted(gen3) if (hits := gate_dev.source_seen(g, sorted(dev)))}
    clash.update({d: hits for d in sorted(dev) if (hits := gate_dev.source_seen(d, sorted(gen3)))})
    if clash:
        out["problems"].append(f"gd_gen3_* source names match dev sources: {clash}")
    if (out["unseen_sources"], out["unseen_rows"]) != (17, 3847) or out["flagged"]:
        out["problems"].append(f"unseen set {out['unseen_sources']} sources / {out['unseen_rows']} rows, flagged {out['flagged']}")
    out.update({"fix1_sources": len(fix1), "fix1_gen3_sources": sorted(gen3), "fix1_golden_sources": len(fix1 & golden)})
    print(json.dumps(out, indent=1))
    print("check_unseen_fix1: " + ("PASS" if not out["problems"] else "FAIL: " + " | ".join(out["problems"])))
    return 0 if not out["problems"] else 1


if __name__ == "__main__":
    sys.exit(main())
