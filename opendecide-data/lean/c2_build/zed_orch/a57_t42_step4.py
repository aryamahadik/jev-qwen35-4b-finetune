"""a57_t42_step4.py: A57 step 4 G13-seed stage 1 for T42 program templates (3 rules + 9 wordings; T42 has no Haiku pool,
so g13_c2 seed finds no pool dir). Builds the same TEMPLATE units pool_units would, runs g13_c2.run('seed') in memory
(write=False), then the OHS-AC checkers (RUN only) and the OHS-AC / OHS-4 hash compares. Counts and ids only. Mac only.
  ../../.venv/bin/python -B zed_orch/a57_t42_step4.py [--no-side]
"""
import json, sys, subprocess, hashlib
from pathlib import Path
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import g13_c2 as G
from families.T42 import texts as T

LEAN = G.LEAN
OUTF = C2 / "logs" / "a57_T42_step4_g13seed.json"
tx = C2 / "families" / "T42" / "texts.py"
rel = G.lean_rel(tx)

def tmpl_units():
    us = []
    i = 0
    for k, v in T.RULES.items():
        us.append(("rule:" + k, v))
    for k, ws in T.WORDINGS.items():
        for j, w in enumerate(ws):
            us.append((f"wording:{k}:{j}", w))
    out = []
    for n, (tid, t) in enumerate(us):
        out.append({"key": f"pool:{rel}#{tid}", "rows": [], "source": "pool:T42", "seed": True, "public": False,
                    "line": n + 1, "template": True, "template_id": tid, "file": rel, "texts": [("pool", t)]})
    return out

def fake_build_sets(run, blocks, ilog):
    before = G._sha_map([tx, *G.code_files(C2 / "families" / "T42")])
    units = tmpl_units()
    code, cshas = G.code_seed_units("T42", C2 / "families" / "T42")
    return {"c2_seed_T42": {"units": units, "code": code, "train_shas": {},
                            "seed_shas": {rel: G.g.sha256_file(tx), **cshas}, "train_path": None, "block": "T42",
                            "guard_shas": {G.lean_rel(p): s for p, s in before.items()}}}

def main():
    side = "--no-side" not in sys.argv
    embed = "--no-embed" not in sys.argv
    G.build_sets = fake_build_sets
    recs = G.run("seed", ["T42"], embed=embed, side=side, write=False)
    r = recs["c2_seed_T42"]
    keep = {k: r.get(k) for k in ("run", "complete", "incomplete_why", "quarantine_templates", "quarantine",
                                  "counts_by_target_and_method", "code_seed_hits", "report_only", "ohs4", "engine",
                                  "inputs_at_start") if k in r}
    keep["n_template_units"] = len(tmpl_units())
    OUTF.write_text(json.dumps(keep, indent=1, default=str))
    print(json.dumps({"complete": r.get("complete"), "n_incomplete_why": len(r.get("incomplete_why") or []),
                      "quarantine_templates": r.get("quarantine_templates"),
                      "counts": r.get("counts_by_target_and_method")}, default=str)[:3000])

if __name__ == "__main__":
    main()
