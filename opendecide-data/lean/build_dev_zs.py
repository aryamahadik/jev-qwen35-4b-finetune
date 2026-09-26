"""Dev set of zero-shot tasks for model SELECTION (never used for training, never the reported eval).

AG News (topic) and Emotion (dair-ai) test items, with dev-only wordings (same as dev.jsonl).
Tasks are disjoint from every train source and from the eval ZS tasks (SMS spam, financial tweets).
Writes data/devzs.jsonl + data/devzs_relations.jsonl (track "DEV" so score.py --split devzs works).
"""
from datasets import load_dataset

from build_data import DEV_AFF, DEV_CHOICE, DEV_NEG, OUT, Builder, frame, rng

AG = {0: "world news", 1: "sports", 2: "business", 3: "science and technology"}
EMO = {0: "sadness", 1: "joy", 2: "love", 3: "anger", 4: "fear", 5: "surprise"}
SPECS = [
    ("ag_news", "fancyzhx/ag_news", "text", AG, "News article:\n{t}",
     lambda k, neg=False: f"the article is {'not ' if neg else ''}about {k}"),
    ("emotion", "dair-ai/emotion", "text", EMO, "Social media post:\n{t}",
     lambda k, neg=False: f"the writer is {'not ' if neg else ''}expressing {k}"),
]

D = Builder("devzs")
for src, hf, col, labmap, wrap, prop in SPECS:
    ds = load_dataset(hf, split="test")
    r = rng("devzs", src)
    by = {}
    for i, x in enumerate(ds):
        by.setdefault(x["label"], []).append((i, x))
    per = 100 // len(labmap) + 1
    items = []
    for lab in sorted(by):
        items += r.sample(by[lab], per)
    items = items[:100]
    for j, (i, x) in enumerate(items):
        rr = rng("devzs", src, i)
        group = f"g:{src}:{i}"
        state = wrap.format(t=x[col].strip())
        gold = labmap[x["label"]]
        opts = list(labmap.values())
        rr.shuffle(opts)
        D.row(group=group, state=state, source=src, track="DEV", qtype="choice", instructions=DEV_CHOICE,
              options=opts, gold=gold, role="choice")
        tgt = gold if j % 2 == 0 else rr.choice([o for o in opts if o != gold])
        g = int(tgt == gold)
        a = D.row(group=group, state=state, source=src, track="DEV", qtype="noul", instructions=frame(DEV_AFF[0], prop(tgt)),
                  options=None, gold=g, role="aff")
        n_ = D.row(group=group, state=state, source=src, track="DEV", qtype="noul", instructions=frame(DEV_NEG[0], prop(tgt)),
                   options=None, gold=1 - g, role="neg")
        d = D.row(group=group, state=state, source=src, track="DEV", qtype="noul",
                  instructions=frame(DEV_NEG[0], prop(tgt, neg=True)), options=None, gold=g, role="dneg")
        D.rel("complement", a, n_, "DEV")
        D.rel("equiv", a, d, "DEV")

import json  # noqa: E402

with open(OUT / "devzs.jsonl", "w") as f:
    for row in D.rows:
        f.write(json.dumps(row) + "\n")
with open(OUT / "devzs_relations.jsonl", "w") as f:
    for x in D.rels:
        f.write(json.dumps(x) + "\n")
print(f"devzs: {len(D.rows)} rows, {len(D.rels)} relations")
