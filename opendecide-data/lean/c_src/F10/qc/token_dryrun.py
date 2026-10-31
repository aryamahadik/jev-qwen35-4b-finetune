"""F10 token dry run (G0 section 1, R2-11, R2-25, R5-G): real-tokenizer lengths of the served prompt
(decoder_io cygnet, schema_branch_mark; `instructions` counted twice) per sampler, layout, bucket and k, from the
rendered rows of the given parts (out/<part>.gates_tokens.json from qc/gates.py). Writes qc/token_dryrun.json.
Feasible k (strict) = every sampled row with that k is < 2,000; weak = at least one row < 2,000.
Counterfactual `once` = served tokens minus one copy of `instructions` (report only; not a G0 figure)."""
from __future__ import annotations

import collections as C
import json
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "gen"))


def summ(v):
    v = sorted(v)
    return {"n": len(v), "min": v[0], "p50": st.median(v), "max": v[-1], "n_ge_2000": sum(x >= 2000 for x in v),
            "n_gt_900": sum(x > 900 for x in v)} if v else {"n": 0}


def main(parts):
    import gates
    import lexicon as L
    tok = gates.tokenizer()
    ntok = lambda s: len(tok(s, add_special_tokens=False)["input_ids"]) if s else 0
    stmed = {k: st.median([ntok(p) for p in v]) for k, v in L.ST.items() if isinstance(v, list) and v
             and all(isinstance(p, str) for p in v)}
    rep = {"parts": parts, "tokenizer": "Qwen/Qwen3.5-4B@851bf6e8", "prompt": "decoder_io cygnet schema_branch_mark",
           "by_part": {}}
    allt, allonce = [], []
    by_lay, by_bucket, by_k, by_card = (C.defaultdict(list) for _ in range(4))
    once_lay = C.defaultdict(list)
    for part in parts:
        toks = json.loads((OUT / f"{part}.gates_tokens.json").read_text())
        side = {}
        for l in open(OUT / f"{part}.sidecar.jsonl"):
            m = json.loads(l)
            side[m["id"]] = m
        cards = {json.loads(l)["card_id"]: json.loads(l) for l in open(OUT / f"{part}.cards.jsonl")}
        pt = []
        for l in open(OUT / f"{part}.jsonl"):
            r = json.loads(l)
            m = side[r["id"]]
            t = toks[r["id"]]
            ch = m["form"] != "yn"
            once = t - (ntok(r["instructions"]) if ch else 0)
            pt.append(t)
            if part == "mixdev_S5":
                continue
            allt.append(t)
            allonce.append(once)
            by_lay[f'{m["sampler"]}|{m["form"]}|{m["layout"]}'].append(t)
            once_lay[f'{m["sampler"]}|{m["form"]}|{m["layout"]}'].append(once)
            if ch:
                by_bucket[f'{m["sampler"]}|{m["bucket"]}'].append(t)
                by_k[f'{m["sampler"]}|{m["k"]:02d}'].append(t)
            c = cards.get(m["card_id"], {})
            by_card[m["sampler"]].append((m["card_id"], c.get("n_terms"), len(c.get("rules") or []),
                                          sum(stmed.get(x, 20) for x in (c.get("rules") or []))))
        rep["by_part"][part] = summ(pt)
    rep["training_parts_all"] = summ(allt)
    rep["training_parts_all"]["mean"] = round(sum(allt) / len(allt), 1)
    rep["counterfactual_instructions_once"] = summ(allonce)
    rep["by_sampler_form_layout"] = {k: summ(v) for k, v in sorted(by_lay.items())}
    rep["by_sampler_form_layout_once"] = {k: summ(v) for k, v in sorted(once_lay.items())}
    rep["choice_by_sampler_bucket"] = {k: summ(v) for k, v in sorted(by_bucket.items())}
    kk = {k: summ(v) for k, v in sorted(by_k.items())}
    rep["choice_by_sampler_k"] = kk
    feas = C.defaultdict(lambda: {"strict": [], "weak": [], "none": []})
    for k, s in kk.items():
        sm, kv = k.split("|")
        feas[sm]["strict" if s["max"] < 2000 else "weak" if s["min"] < 2000 else "none"].append(int(kv))
    rep["feasible_k"] = feas
    rb = {}
    for sm, lst in by_card.items():
        u = {x[0]: x for x in lst}.values()
        rb[sm] = {"cards": len(u), "rules_rows_p50": st.median([x[2] for x in u]),
                  "rules_tokens_est_p50": st.median([x[3] for x in u]),
                  "rules_tokens_est_min": min(x[3] for x in u), "n_terms_p50": st.median([x[1] or 0 for x in u])}
    rep["rules_block_by_sampler"] = rb
    (HERE / "token_dryrun.json").write_text(json.dumps(rep, indent=1))
    a = rep["training_parts_all"]
    print(f"rows {a['n']} median {a['p50']} mean {a['mean']} ge2000 {a['n_ge_2000']} gt900 {a['n_gt_900']}; "
          f"once median {rep['counterfactual_instructions_once']['p50']}")
    for sm, f in sorted(feas.items()):
        print(sm, "strict", f["strict"], "weak", f["weak"], "none", f["none"])
    for sm, x in sorted(rb.items()):
        print(sm, x)


if __name__ == "__main__":
    main(sys.argv[1:] or ["candidates_r1", "qc_sample"])
