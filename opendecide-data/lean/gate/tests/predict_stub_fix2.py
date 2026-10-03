"""CPU stand-in for `od_gcp.py predict` in the job-3 simulation (gate/tests/sim_gate_fix2.py). Same arguments, needs
models/<name>/train_meta.json, writes preds_<split>/<out>.jsonl in data order plus a .meta.json shaped like
cmd_predict's. Probabilities are COPIED or SYNTHETIC, so every number is meaningless; only the plumbing is tested.

GATE_STUB_MAP (JSON) maps an output name to:
  "src"           pred name copied on the 9 gate splits (default: q35_4b_pxE_parity; _perm reads q35_4b_pxE_tta)
  "src_attack"    pred name copied on eval_* (default q35_4b_pxE)
  "improve_noul"  share of 9-split yes/no rows set to 0.9 on the gold side
  "degrade_noul"  share of 9-split yes/no rows with yes/no swapped
  "fix_equiv"     true: every 9-split row in an 'equiv' relation is set to 0.9 on the gold side (no (e) flips)
  "f7_flip"       F7 probe / devx / memo rows (no source preds): every row answered right (0.9 on the gold side),
                  then this share of the even-depth rows (rung N2 / N4 in the sidecar) answered wrong (default 0.0)
  "no_load"       true: the .meta.json has no load record (a pipeline problem: the conditions give NO VERDICT)
The meta records the TTA flags of the arguments (--tta / --tta-choice / --tta-noul) like od_gcp does.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path.cwd()
sys.path.insert(0, str(HERE))
import od_gcp  # noqa: E402

CHAT_TEMPLATE_SHA = "a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715"
NINE = {"dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev"}


def h(s):
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % 1000


def gold_side(r, right=True):
    if r["qtype"] == "noul":
        y = 0.9 if (r["gold"] == 1) == right else 0.1
        return {"yes": y, "no": 1 - y}
    opts = r["options"]
    g = r["gold"] if right else next(o for o in opts if o != r["gold"])
    rest = (0.1 / (len(opts) - 1)) if len(opts) > 1 else 0.0
    return {o: (0.9 if o == g else rest) for o in opts}


def main():
    a = od_gcp.parser().parse_args(["predict"] + sys.argv[1:])
    if not (HERE / "models" / a.name / "train_meta.json").exists():
        sys.exit(f"stub: models/{a.name}/train_meta.json missing")
    out = od_gcp.out_name(a.name, a.tag)
    spec = json.loads(Path(os.environ["GATE_STUB_MAP"]).read_text()).get(out, {}) if os.environ.get("GATE_STUB_MAP") else {}
    src = spec.get("src", "q35_4b_pxE_tta" if a.perm_seed is not None else "q35_4b_pxE_parity")
    src_attack = spec.get("src_attack", "q35_4b_pxE")
    deg, imp, f7f = float(spec.get("degrade_noul", 0.0)), float(spec.get("improve_noul", 0.0)), float(spec.get("f7_flip", 0.0))
    kw = od_gcp.tta_kwargs(a)
    for s in a.splits.split(","):
        rows = [json.loads(l) for l in open(HERE / f"data/{s}.jsonl")]
        pd = HERE / f"preds_{s}"
        pd.mkdir(exist_ok=True)
        side_p = HERE / f"data/{s}_meta.jsonl"
        side = {json.loads(l)["id"]: json.loads(l) for l in open(side_p)} if side_p.exists() else {}
        sname = src_attack if s.startswith("eval_") else (src if s in NINE else None)
        fixed = set()
        rp = HERE / f"data/{s}_relations.jsonl"
        if spec.get("fix_equiv") and s in NINE and rp.exists():
            for l in open(rp):
                x = json.loads(l)
                if x["type"] == "equiv":
                    fixed |= {x["a"], x["b"]}
        P = {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(pd / f"{sname}.jsonl")} if sname else None
        with open(pd / f"{out}.jsonl", "w") as f:
            for r in rows:
                if P is not None:
                    p = dict(P[r["id"]])
                    k = h(r["id"])
                    if deg and r["qtype"] == "noul" and k < deg * 1000:
                        p = {"yes": p["no"], "no": p["yes"]}
                    if imp and r["qtype"] == "noul" and k >= 1000 - imp * 1000:
                        p = gold_side(r)
                    if r["id"] in fixed:
                        p = gold_side(r)
                else:
                    rung = (side.get(r["id"]) or {}).get("rung") or (r.get("meta") or {}).get("rung")
                    wrong = rung in ("N2", "N4") and h(out + r["id"]) < f7f * 1000
                    p = gold_side(r, right=not wrong)
                f.write(json.dumps({"id": r["id"], "model": out, "probs": p}) + "\n")
        load = {"adapters": [str(HERE / "models" / a.name)], "layout": a.layout, "style": "cygnet", "base": a.base,
                "revision": a.revision, "saved": {"layout": a.layout, "style": "cygnet", "base": a.base},
                "saved_in": {str(HERE / "models" / a.name): "train_meta.json"}, "forced": [], "prism_x": False,
                "chat_template_sha": CHAT_TEMPLATE_SHA}
        meta = {"name": out, "rows": len(rows), "layout": a.layout, "style": "cygnet", "base": a.base, "host": "gcp",
                "gpu": "NVIDIA L4", "torch": "2.14.0+cu130", "cuda": "13.0", "sec": 0, **od_gcp.tta_meta(kw),
                "perm_seed": a.perm_seed, "load": load,
                "stub": f"gate/tests/predict_stub_fix2.py ({sname or 'synthetic'}); NOT a model read"}
        if spec.get("no_load"):
            meta.pop("load")
        (pd / f"{out}.meta.json").write_text(json.dumps(meta, indent=2))
        print(f"wrote {pd.name}/{out}.jsonl ({len(rows)} rows, stub {sname or 'synthetic'})", flush=True)


if __name__ == "__main__":
    main()
