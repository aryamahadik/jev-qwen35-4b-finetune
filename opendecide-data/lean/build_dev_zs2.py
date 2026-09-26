"""Second selection-only dev set, closer in KIND to the eval ZS tasks but from different datasets:
Enron email spam (spam vs legitimate) and TweetEval sentiment (negative / neutral / positive).
Never trained on, never reported as eval. Writes data/devzs2.jsonl + data/devzs2_relations.jsonl.
"""
import json

from datasets import load_dataset

from build_data import DEV_AFF, DEV_CHOICE, DEV_NEG, OUT, Builder, frame, rng

D = Builder("devzs2")
en = [x for x in load_dataset("SetFit/enron_spam", split="test") if 5 <= len(x["text"].split()) <= 80]
tw = load_dataset("cardiffnlp/tweet_eval", "sentiment", split="test")
r = rng("devzs2")
items = [("enron_spam", x, {"1": "spam", "0": "legitimate"}[str(x["label"])], "Email:\n" + x["text"]) for x in
         r.sample([x for x in en if str(x["label"]) == "1"], 50) + r.sample([x for x in en if str(x["label"]) == "0"], 50)]
names = ["negative", "neutral", "positive"]
for lab in range(3):
    items += [("tweet_sentiment", x, names[lab], "Tweet:\n" + x["text"]) for x in r.sample([x for x in tw if x["label"] == lab], 30)]
PROP = {"spam": ("this email is spam", "this email is not spam"),
        "legitimate": ("this email is a legitimate message", "this email is not a legitimate message"),
        "negative": ("the tweet expresses a negative sentiment", "the tweet does not express a negative sentiment"),
        "neutral": ("the tweet is neutral", "the tweet is not neutral"),
        "positive": ("the tweet expresses a positive sentiment", "the tweet does not express a positive sentiment")}
for j, (src, x, gold, state) in enumerate(items):
    rr = rng("devzs2", src, j)
    opts = ["spam", "legitimate"] if src == "enron_spam" else list(names)
    rr.shuffle(opts)
    group = f"g:{src}:{j}"
    D.row(group=group, state=state, source=src, track="DEV", qtype="choice", instructions=DEV_CHOICE, options=opts, gold=gold, role="choice")
    tgt = gold if j % 2 == 0 else rr.choice([o for o in opts if o != gold])
    g = int(tgt == gold)
    p, negp = PROP[tgt]
    a = D.row(group=group, state=state, source=src, track="DEV", qtype="noul", instructions=frame(DEV_AFF[0], p), options=None, gold=g, role="aff")
    n_ = D.row(group=group, state=state, source=src, track="DEV", qtype="noul", instructions=frame(DEV_NEG[0], p), options=None, gold=1 - g, role="neg")
    d = D.row(group=group, state=state, source=src, track="DEV", qtype="noul", instructions=frame(DEV_NEG[0], negp), options=None, gold=g, role="dneg")
    D.rel("complement", a, n_, "DEV")
    D.rel("equiv", a, d, "DEV")
with open(OUT / "devzs2.jsonl", "w") as f:
    for row in D.rows:
        f.write(json.dumps(row) + "\n")
with open(OUT / "devzs2_relations.jsonl", "w") as f:
    for x in D.rels:
        f.write(json.dumps(x) + "\n")
print(f"devzs2: {len(D.rows)} rows")
