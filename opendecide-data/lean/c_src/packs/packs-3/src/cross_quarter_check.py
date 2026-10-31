"""Cross-quarter check of packs-3 against the other domain-pack quarters (review fix 4). Read-only on the other
quarters' pack files; writes counts and pack ids only (no pack text) to cross_quarter_check.json.

Checks:
  jargon   exact jargon-term clash (case-insensitive) between a packs-3 pack and any pack of packs-1/2/4 (blocking)
  seeds    ROUGE-L >= 0.7 between packs-3 seed fields and the other quarters' matching fields (G11, blocking)
Usage (from packs-3/): python src/cross_quarter_check.py [--packs FILE] [--out FILE]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import lints  # noqa: E402

OTHERS = {"packs-1": ROOT.parent / "packs-1" / "packs.jsonl",
          "packs-2": ROOT.parent / "packs-2" / "packs.jsonl",
          "packs-4": ROOT.parent / "packs-4" / "packs.jsonl"}
# matching seed fields per quarter (packs-3 field -> other quarter's field)
SEED_MAP = {"packs-1": {"setting": "setting", "org": "org", "decider_role": "deciding_role"},
            "packs-2": {"setting": "setting", "org": "org_name", "decider_role": "decider_role"},
            "packs-4": {"setting": "setting", "title": "title"}}


def jargon_terms(p):
    out = []
    for x in p.get("jargon_candidates", p.get("jargon", [])) or []:
        t = x.get("term") if isinstance(x, dict) else x
        if isinstance(t, str):
            out.append(t.strip().lower())
    return out


def text(v):
    return v if isinstance(v, str) else (json.dumps(v) if v is not None else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packs", default=str(ROOT / "packs-3.jsonl"))
    ap.add_argument("--out", default=str(ROOT / "cross_quarter_check.json"))
    a = ap.parse_args()
    mine = [json.loads(l) for l in open(a.packs)]
    res = {"packs3_input": Path(a.packs).name,
           "packs3_sha256": hashlib.sha256(Path(a.packs).read_bytes()).hexdigest(),
           "others": {}, "jargon_clashes": [], "seed_rouge_l_ge_0_7": [], "max_seed_rouge_l": {}}
    for q, f in OTHERS.items():
        if not f.exists():
            res["others"][q] = {"path": str(f.relative_to(ROOT.parent)), "missing": True}
            continue
        other = [json.loads(l) for l in open(f)]
        res["others"][q] = {"path": str(f.relative_to(ROOT.parent)),
                            "sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "packs": len(other)}
        idx = {}
        for o in other:
            for t in jargon_terms(o):
                idx.setdefault(t, []).append(o["id"])
        for p in mine:
            for t in jargon_terms(p):
                for oid in idx.get(t, []):
                    res["jargon_clashes"].append({"packs3_id": p["id"], "quarter": q, "other_id": oid})
        for mf, of in SEED_MAP[q].items():
            best = 0.0
            for p in mine:
                for o in other:
                    if of not in o:
                        continue
                    r = lints.rouge_l(text(p[mf]), text(o[of]))
                    best = max(best, r)
                    if r >= 0.7:
                        res["seed_rouge_l_ge_0_7"].append({"field": mf, "packs3_id": p["id"], "quarter": q,
                                                           "other_id": o["id"], "rouge_l": round(r, 3)})
            res["max_seed_rouge_l"][f"{q}:{mf}"] = round(best, 3)
    res["blocking"] = len(res["jargon_clashes"]) + len(res["seed_rouge_l_ge_0_7"])
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps({"jargon_clashes": len(res["jargon_clashes"]),
                      "seed_rouge_l_ge_0_7": len(res["seed_rouge_l_ge_0_7"]),
                      "max_seed_rouge_l": res["max_seed_rouge_l"]}))
    return 3 if res["blocking"] else 0


if __name__ == "__main__":
    sys.exit(main())
