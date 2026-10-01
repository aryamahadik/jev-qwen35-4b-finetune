"""CPU stand-in for `od_gcp.py predict` in the gate simulation (gate/tests/sim_gate.py). It takes the same arguments,
needs the same models/<name>/train_meta.json, and writes the same files (preds_<split>/<out>.jsonl in data order plus a
.meta.json shaped like cmd_predict's), but the probabilities are COPIED from existing pred files, so every number it
leads to is meaningless; only the plumbing (names, order, completeness, metas, looks) is being tested.

GATE_STUB_MAP (a JSON file) maps an output name to {"src": pred name for the 9 splits, "src_attack": pred name for
eval_*, "degrade_noul": share of yes/no rows whose yes/no probabilities are swapped (deterministic by id),
"improve_noul": share of yes/no rows set to 0.9 on the gold side}.
Defaults: standard reads copy q35_4b_pxE_parity, _perm reads copy q35_4b_pxE_tta, eval_* copy q35_4b_pxE.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path.cwd()  # the simulated lean/ folder (the gate script cd's there)
sys.path.insert(0, str(HERE))
import od_gcp  # noqa: E402  (parser and out_name only; nothing heavy is imported at module level)

CHAT_TEMPLATE_SHA = "a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715"


def main():
    a = od_gcp.parser().parse_args(["predict"] + sys.argv[1:])
    if not (HERE / "models" / a.name / "train_meta.json").exists():
        sys.exit(f"stub: models/{a.name}/train_meta.json missing")
    out = od_gcp.out_name(a.name, a.tag)
    spec = json.loads(Path(os.environ["GATE_STUB_MAP"]).read_text()).get(out, {}) if os.environ.get("GATE_STUB_MAP") else {}
    src = spec.get("src", "q35_4b_pxE_tta" if a.perm_seed is not None else "q35_4b_pxE_parity")
    src_attack = spec.get("src_attack", "q35_4b_pxE")
    deg = float(spec.get("degrade_noul", 0.0))
    imp = float(spec.get("improve_noul", 0.0))  # share of yes/no rows set to 0.9 on the gold side (a "better" model)
    for s in a.splits.split(","):
        rows = [json.loads(l) for l in open(HERE / f"data/{s}.jsonl")]
        sname = src_attack if s.startswith("eval_") else src
        P = {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(HERE / f"preds_{s}/{sname}.jsonl")}
        pd = HERE / f"preds_{s}"
        with open(pd / f"{out}.jsonl", "w") as f:
            for r in rows:
                p = dict(P[r["id"]])
                h = int(hashlib.sha256(r["id"].encode()).hexdigest(), 16) % 1000
                if deg and r["qtype"] == "noul" and h < deg * 1000:
                    p = {"yes": p["no"], "no": p["yes"]}
                if imp and r["qtype"] == "noul" and h >= 1000 - imp * 1000:
                    p = {"yes": 0.9, "no": 0.1} if r["gold"] == 1 else {"yes": 0.1, "no": 0.9}
                f.write(json.dumps({"id": r["id"], "model": out, "probs": p}) + "\n")
        load = {"adapters": [str(HERE / "models" / a.name)], "layout": a.layout, "style": "cygnet", "base": a.base,
                "revision": a.revision, "saved": {"layout": a.layout, "style": "cygnet", "base": a.base},
                "saved_in": {str(HERE / "models" / a.name): "train_meta.json"}, "forced": [], "prism_x": False,
                "chat_template_sha": CHAT_TEMPLATE_SHA}
        meta = {"name": out, "rows": len(rows), "layout": a.layout, "style": "cygnet", "base": a.base, "host": "gcp",
                "gpu": "NVIDIA L4", "torch": "2.14.0+cu130", "cuda": "13.0", "sec": 0, "tta": False, "tta_choice": False,
                "tta_noul": False, "perm_seed": a.perm_seed, "load": load,
                "stub": f"gate/tests/predict_stub.py copied {sname}; NOT a model read"}
        (pd / f"{out}.meta.json").write_text(json.dumps(meta, indent=2))
        print(f"wrote {pd.name}/{out}.jsonl ({len(rows)} rows, stub copy of {sname})", flush=True)


if __name__ == "__main__":
    main()
