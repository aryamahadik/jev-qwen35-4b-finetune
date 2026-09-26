"""Train set v0.5 = train_v04 (v0.3 + multi-record rows) + a broader public task mix for zero-shot breadth.

Added: MASSIVE intents (CC-BY-4.0), Civil Comments toxicity (CC0), Yelp polarity sentiment. Each state gets a choice
row and a yes/no row, and half get a negation (complement link). Held out from ALL training, as before: the eval ZS
datasets (SMS Spam, Twitter Financial News), the selection dev sets (AG News, Emotion, Enron spam, TweetEval) and every
eval/dev wording. No spam/phishing or financial-sentiment data is added.
"""
import json
from collections import Counter

from datasets import load_dataset

from build_data import NONE_TRAIN, OUT, Builder, embed, frame, norm, rng
from build_train_v03 import NEW_AFF, NEW_NEG

T = Builder("train")
added = Counter()
eval_states = {norm(json.loads(l)["state"]) for l in open(OUT / "eval.jsonl")}


def add(group, state, src, instr, opts, gold, prop, negate, rr):
    if norm(state) in eval_states:
        return
    T.row(group=group, state=state, source=src, track="L0", qtype="choice", instructions=instr, options=opts, gold=gold, role="choice")
    tgt = gold if rr.random() < 0.5 else rr.choice([o for o in opts if o != gold and o != NONE_TRAIN])
    g = int(tgt == gold)
    a = T.row(group=group, state=state, source=src, track="L0", qtype="noul", instructions=frame(rr.choice(NEW_AFF), prop(tgt)),
              options=None, gold=g, role="aff")
    if negate:
        n_ = T.row(group=group, state=state, source=src, track="L2", qtype="noul", instructions=frame(rr.choice(NEW_NEG), prop(tgt)),
                   options=None, gold=1 - g, role="neg")
        T.rel("complement", a, n_, "train")
    added[src] += 1


# MASSIVE intents: 8 nearest intent labels as options (hard negatives), like Banking77/CLINC
ms = load_dataset("mteb/amazon_massive_intent", "en", split="train")
labels = sorted(set(ms["label_text"]))
nice = {l: l.replace("_", " ") for l in labels}
E = embed([nice[l] for l in labels])
S = E @ E.T
near = {labels[i]: [labels[j] for j in (-S[i]).argsort() if j != i] for i in range(len(labels))}
r = rng("v05", "massive")
for j, x in enumerate(r.sample(list(ms), 600)):
    rr = rng("v05", "massive", j)
    opts = [nice[o] for o in near[x["label_text"]][:7]] + [nice[x["label_text"]]]
    rr.shuffle(opts)
    add(f"g:massive:{x['id']}", f"Voice assistant request:\n{x['text']}", "massive", "Which intent does this request express?",
        opts + [NONE_TRAIN], nice[x["label_text"]], lambda k: f"the user wants: {k}", j % 2 == 0, rr)

# Civil Comments toxicity (clear cases only: >= 0.6 toxic, == 0 clean)
cc = load_dataset("google/civil_comments", split="train[:200000]")
r = rng("v05", "civil")
tox = [x for x in cc if x["toxicity"] >= 0.6 and 5 <= len(x["text"].split()) <= 120]
cln = [x for x in cc if x["toxicity"] == 0.0 and 5 <= len(x["text"].split()) <= 120]
for j, x in enumerate(r.sample(tox, 200) + r.sample(cln, 200)):
    rr = rng("v05", "civil", j)
    gold = "toxic" if x["toxicity"] >= 0.6 else "not toxic"
    opts = ["toxic", "not toxic"]
    rr.shuffle(opts)
    add(f"g:civil:{j}", f"User comment:\n{x['text']}", "civil_comments", "Is this comment toxic or not?", opts, gold,
        lambda k: "the comment is toxic" if k == "toxic" else "the comment is civil and not toxic", j % 2 == 0, rr)

# Yelp polarity sentiment
yp = load_dataset("fancyzhx/yelp_polarity", split="train[:50000]")
r = rng("v05", "yelp")
yp = [x for x in yp if 10 <= len(x["text"].split()) <= 120]
for j, x in enumerate(r.sample(yp, 400)):
    rr = rng("v05", "yelp", j)
    gold = "positive" if x["label"] == 1 else "negative"
    opts = ["positive", "negative"]
    rr.shuffle(opts)
    add(f"g:yelp:{j}", f"Business review:\n{x['text']}", "yelp", "What is the overall tone of this review?", opts, gold,
        lambda k: f"the review is {k}", j % 2 == 0, rr)

base = [json.loads(l) for l in open(OUT / "train_v04.jsonl")]
ids = {x["id"] for x in base}
new = [x for x in T.rows if x["id"] not in ids]
assert len(new) == len({x["id"] for x in new})
with open(OUT / "train_v05.jsonl", "w") as f:
    for x in base + new:
        f.write(json.dumps(x) + "\n")
rels = (OUT / "train_v04_relations.jsonl").read_text() + "".join(json.dumps(x) + "\n" for x in T.rels)
(OUT / "train_v05_relations.jsonl").write_text(rels)
print(f"train_v05: {len(base) + len(new)} rows ({len(new)} new), added states {dict(added)}")
