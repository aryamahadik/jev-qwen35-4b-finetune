"""Eval slices aimed at Jev's documented weaknesses (separate files; the frozen v0.1 eval is untouched).

HC   high-cardinality choice. Same in-scope ID states as the core eval, asked to pick from
     (a) the dataset's FULL label space (Banking77: 77, CLINC150: 150, + "none of the listed topics"),
     (b) that space padded to 500 and (c) to 2,000 options with Google-product-taxonomy categories
     (filtered so none is semantically close to any intent label). Jev is native up to 255 options
     and switches to a two-stage method above that. Gold is the human intent label.
LONG long irrelevant state. The same message buried among ~1,500 or ~4,500 words of wikitext TEST
     paragraphs (the eval filler corpus). Same choice + yes/no question and gold as the clean core rows.

Writes data/eval_hc.jsonl, data/eval_hc_calls.jsonl, data/eval_long.jsonl, data/eval_long_calls.jsonl.
"""
from __future__ import annotations

import json
from collections import defaultdict

import numpy as np
from datasets import load_dataset

from build_data import NONE_EVAL, OUT, ROOT, Builder, embed, filler_pool, load_keys, norm, rng

LEVELS = ["full", 500, 2000]


def product_labels(intent_keys):
    lines = (ROOT / "assets/weak/google_product_taxonomy.txt").read_text().splitlines()
    leaves = sorted({l.split(" > ")[-1].strip().lower() for l in lines if l and not l.startswith("#")})
    intents = {norm(k) for k in intent_keys}
    leaves = [l for l in leaves if norm(l) not in intents]
    E, I = embed(leaves), embed(list(intent_keys))
    mx = (E @ I.T).max(axis=1)
    return [l for l, m in zip(leaves, mx) if m < 0.5], int((mx >= 0.5).sum())


def write(name, B):
    with open(OUT / f"{name}.jsonl", "w") as f:
        for r in B.rows:
            f.write(json.dumps(r) + "\n")
    calls = defaultdict(list)
    states = {}
    for r in B.rows:
        calls[r["call_id"]].append(r["id"])
        states[r["call_id"]] = r["state"]
    with open(OUT / f"{name}_calls.jsonl", "w") as f:
        for c, ids in calls.items():
            f.write(json.dumps({"call_id": c, "state": states[c], "row_ids": ids}) + "\n")
    return len(B.rows), len(calls)


def main():
    ev = [json.loads(l) for l in open(OUT / "eval.jsonl")]
    core = [r for r in ev if r["track"] == "ID" and r["qtype"] == "choice" and r["gold"] != NONE_EVAL]
    aff = {r["group_id"]: r for r in ev if r["track"] == "ID" and r["role"] == "aff"}
    keys = {ds: [v["key"] for v in load_keys(ds).values() if v.get("kind") == "intent"] for ds in ("banking77", "clinc150")}
    distract, n_dropped = product_labels(keys["banking77"] + keys["clinc150"])
    print(f"product-taxonomy distractors kept {len(distract)}, dropped as too close to an intent: {n_dropped}")

    H = Builder("eval_hc")
    for r in core:
        full = keys[r["source"]] + [NONE_EVAL]
        assert r["gold"] in full
        for lev in LEVELS:
            rr = rng("eval_hc", r["id"], lev)
            opts = list(full) if lev == "full" else list(full) + rr.sample(distract, lev - len(full))
            rr.shuffle(opts)
            H.row(group=r["group_id"], state=r["state"], source=r["source"], track="HC",
                  qtype="choice", instructions=r["instructions"], options=opts, gold=r["gold"], role="choice",
                  meta={"level": str(lev), "n_options": len(opts), "clean_id": r["id"]})
    # HC rows share state and wording across levels: give each level its own row id and call id
    for row in H.rows:
        row["id"] = row["id"] + "_" + row["meta"]["level"]
        row["call_id"] = row["call_id"] + "_" + row["meta"]["level"]
    assert len({row["id"] for row in H.rows}) == len(H.rows)

    wiki = filler_pool(load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="test")["text"])
    L = Builder("eval_long")
    rl = rng("eval_long", "sample")
    by_src = defaultdict(list)
    for r in core:
        by_src[r["source"]].append(r)
    picked = rl.sample(by_src["banking77"], 50) + rl.sample(by_src["clinc150"], 50)
    for r in picked:
        a = aff[r["group_id"]]
        for words in (1500, 4500):
            rr = rng("eval_long", r["id"], words)
            paras, n = [], 0
            while n < words:
                p = wiki[rr.randrange(len(wiki))]
                paras.append(p)
                n += len(p.split())
            paras.insert(rr.randint(0, len(paras)), r["state"])
            state = "\n\n".join(paras)
            meta = {"length_words": words, "position": paras.index(r["state"]) / max(1, len(paras) - 1)}
            L.row(group=r["group_id"], state=state, source=r["source"], track="LONG", qtype="choice", instructions=r["instructions"],
                  options=r["options"], gold=r["gold"], role="choice", meta={**meta, "clean_id": r["id"]})
            L.row(group=r["group_id"], state=state, source=r["source"], track="LONG", qtype="noul", instructions=a["instructions"],
                  options=None, gold=a["gold"], role="aff", meta={**meta, "clean_id": a["id"]})

    for name, B in (("eval_hc", H), ("eval_long", L)):
        n_rows, n_calls = write(name, B)
        print(f"{name}: {n_rows} rows, {n_calls} calls")
    lv = defaultdict(list)
    for r in H.rows:
        lv[r["meta"]["level"]].append(r["meta"]["n_options"])
    print({k: (min(v), max(v)) for k, v in lv.items()})


if __name__ == "__main__":
    main()
