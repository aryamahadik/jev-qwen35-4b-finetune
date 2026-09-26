"""Train set v0.6: breadth + trained-in task cards + base-model anchoring, on top of the v0.5 robustness data.

Changes vs v0.5 (all selection happens on the fresh panel D, data/devp.jsonl):
  * de-monoculture: keep every robustness row (negation L2, injection/distractor/long/multi L3, traps) but only half
    of the plain Banking77/CLINC base rows (72% of v0.5 was intent/topic)
  * breadth (meta.anchor = True -> KL to the frozen base model in train_decoder.py): ARC-Challenge, CommonsenseQA,
    COPA, RTE, QNLI, MRPC, Amazon polarity, toxic conversations, MNLI 3-way with an "undetermined" option,
    Yelp 1-5 stars as ordinal score questions
  * task cards (compile_cards.py, Qwen3-235B, label names only) on ~50% of rows of recurring label sets, and
    symbol-renamed labels on ~15% of carded choice rows so the model must read the card
Excluded everywhere: eval sets, the burned eval-ZS rows, devzs/devzs2, every panel-D dataset, JevBench.
"""
from __future__ import annotations

import json
import os
import random
from collections import Counter
from pathlib import Path

from datasets import load_dataset

from build_data import NONE_TRAIN, OUT, Builder, frame, norm, rng
from build_train_v03 import NEW_AFF, NEW_NEG
from compile_cards import card_text, compile_card, input_kind

HERE = Path(__file__).resolve().parent
for line in (HERE.parent / ".env").read_text().splitlines():
    if "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

T = Builder("train")
added = Counter()
LETTERS = "ABCDE"


def add_choice(group, state, src, instr, opts, gold, prop=None, negate=False, rr=None, anchor=True):
    T.row(group=group, state=state, source=src, track="L0", qtype="choice", instructions=instr, options=opts, gold=gold,
          role="choice", meta={"anchor": anchor})
    if prop:
        tgt = gold if rr.random() < 0.5 else rr.choice([o for o in opts if o != gold])
        g = int(tgt == gold)
        a = T.row(group=group, state=state, source=src, track="L0", qtype="noul", instructions=frame(rr.choice(NEW_AFF), prop(tgt)),
                  options=None, gold=g, role="aff", meta={"anchor": anchor})
        if negate:
            n_ = T.row(group=group, state=state, source=src, track="L2", qtype="noul", instructions=frame(rr.choice(NEW_NEG), prop(tgt)),
                       options=None, gold=1 - g, role="neg", meta={"anchor": False})
            T.rel("complement", a, n_, "train")
    added[src] += 1


def main():
    # ---- multiple-choice reasoning (per-question options: no card) ----
    arc = load_dataset("allenai/ai2_arc", "ARC-Challenge", split="train")
    for j, x in enumerate(rng("v06", "arc").sample(list(arc), 700)):
        opts = x["choices"]["text"]
        if x["answerKey"] not in x["choices"]["label"]:
            continue
        gold = opts[x["choices"]["label"].index(x["answerKey"])]
        add_choice(f"g:arc:{x['id']}", f"Science question:\n{x['question']}", "arc", "Which answer is correct?", opts, gold, anchor=True)
    cq = load_dataset("tau/commonsense_qa", split="train")
    for j, x in enumerate(rng("v06", "csqa").sample(list(cq), 800)):
        opts = x["choices"]["text"]
        gold = opts[x["choices"]["label"].index(x["answerKey"])]
        add_choice(f"g:csqa:{x['id']}", f"Question:\n{x['question']}", "csqa", "Which answer is the most sensible?", opts, gold)
    cp = load_dataset("aps/super_glue", "copa", split="train")
    for x in cp:
        rr = rng("v06", "copa", x["idx"])
        opts = [x["choice1"], x["choice2"]]
        add_choice(f"g:copa:{x['idx']}", f"Situation:\n{x['premise']}", "copa",
                   f"Which option is the more plausible {'cause' if x['question'] == 'cause' else 'result'}?", opts, opts[x["label"]])
    # ---- sentence-pair tasks with fixed label sets (cardable) ----
    pairs = [("rte", ("nyu-mll/glue", "rte"), 500, "sentence1", "sentence2", ["follows", "does not follow"],
              "Does the statement follow from the passage?", lambda k: f"the statement {k} from the passage"),
             ("qnli", ("nyu-mll/glue", "qnli"), 500, "question", "sentence", ["answers the question", "does not answer the question"],
              "Does the sentence answer the question?", lambda k: f"the sentence {k}"),
             ("mrpc", ("nyu-mll/glue", "mrpc"), 400, "sentence1", "sentence2", ["different meaning", "same meaning"],
              "Do the two sentences say the same thing?", lambda k: f"the two sentences have the {k}")]
    for src, (hf, cfg), n, a_, b_, labs, instr, prop in pairs:
        ds = load_dataset(hf, cfg, split="train")
        for x in rng("v06", src).sample(list(ds), n):
            rr = rng("v06", src, x["idx"])
            gold = labs[x["label"]] if src != "mrpc" else labs[x["label"]]
            if src in ("rte", "qnli"):
                gold = labs[0] if x["label"] == 0 else labs[1]
            opts = list(labs)
            rr.shuffle(opts)
            state = f"Passage:\n{x[a_]}\n\nStatement:\n{x[b_]}" if src != "qnli" else f"Question:\n{x[a_]}\n\nSentence:\n{x[b_]}"
            if src == "mrpc":
                state = f"Sentence 1:\n{x[a_]}\n\nSentence 2:\n{x[b_]}"
            add_choice(f"g:{src}:{x['idx']}", state, src, instr, opts, gold, prop, negate=rr.random() < 0.5, rr=rr)
    mn = load_dataset("nyu-mll/multi_nli", split="train[60000:90000]")
    labs3 = ["follows from the passage", "conflicts with the passage", "cannot be determined from the passage"]
    for j, x in enumerate(rng("v06", "mnli3").sample(list(mn), 600)):
        rr = rng("v06", "mnli3", j)
        opts = list(labs3)
        rr.shuffle(opts)
        add_choice(f"g:mnli3:{x['pairID']}", f"Passage:\n{x['premise']}\n\nStatement:\n{x['hypothesis']}", "mnli3",
                   "What is the relation between the statement and the passage?", opts, labs3[x["label"]],
                   lambda k: f"the statement {k}", negate=True, rr=rr)
    # ---- single-text classification + ordinal score ----
    ap = load_dataset("fancyzhx/amazon_polarity", split="test[:30000]")
    for j, x in enumerate(rng("v06", "amz").sample([x for x in ap if 8 <= len(x["content"].split()) <= 120], 400)):
        rr = rng("v06", "amz", j)
        opts = ["negative", "positive"]
        rr.shuffle(opts)
        add_choice(f"g:amz:{j}", f"Product review:\n{x['title']}. {x['content']}", "amazon_polarity", "Is this review positive or negative?",
                   opts, ["negative", "positive"][x["label"]], lambda k: f"the review is {k}", negate=True, rr=rr)
    tc = load_dataset("SetFit/toxic_conversations_50k", split="train")
    tox = [x for x in tc if x["label"] == 1 and 5 <= len(x["text"].split()) <= 100]
    ok = [x for x in tc if x["label"] == 0 and 5 <= len(x["text"].split()) <= 100]
    r = rng("v06", "toxconv")
    for j, x in enumerate(r.sample(tox, 200) + r.sample(ok, 200)):
        rr = rng("v06", "toxconv", j)
        opts = ["toxic", "not toxic"]
        rr.shuffle(opts)
        add_choice(f"g:toxconv:{j}", f"Online comment:\n{x['text']}", "toxic_conv", "Is this comment toxic?", opts,
                   "toxic" if x["label"] == 1 else "not toxic", lambda k: f"the comment is {k}", negate=True, rr=rr)
    yf = load_dataset("Yelp/yelp_review_full", split="test[:20000]")
    levels = ["1 star: very negative", "2 stars: negative", "3 stars: mixed or neutral", "4 stars: positive", "5 stars: very positive"]
    for j, x in enumerate(rng("v06", "yelp5").sample([x for x in yf if 10 <= len(x["text"].split()) <= 120], 600)):
        add_choice(f"g:yelp5:{j}", f"Business review:\n{x['text']}", "yelp5",
                   "Rate the review's overall sentiment on this scale. Use the level the text supports best.",
                   [f"{i}: {l}" for i, l in enumerate(levels)], f"{x['label']}: {levels[x['label']]}", anchor=True)

    base = [json.loads(l) for l in open(OUT / "train_v05.jsonl")]
    base_rels = [json.loads(l) for l in open(OUT / "train_v05_relations.jsonl")]
    # ---- de-monoculture: drop half of the plain intent base rows (their groups keep every robustness variant) ----
    rd = random.Random(20260926)
    keep_ids = set()
    for x in base:
        plain_intent = x["source"] in ("banking77", "clinc150") and x["track"] == "L0"
        if not plain_intent or rd.random() < 0.5:
            keep_ids.add(x["id"])
    base = [x for x in base if x["id"] in keep_ids]
    rels = [x for x in base_rels if x["a"] in keep_ids and x["b"] in keep_ids]
    rows = base + T.rows
    rels += T.rels

    # ---- task cards on recurring label sets (compiled from label names only) ----
    by = {}
    for x in rows:
        if x["qtype"] == "choice" and x["source"] not in ("arc", "csqa", "copa", "banking77", "clinc150", "massive", "yahoo", "dbpedia"):
            by.setdefault((input_kind(x["state"]), tuple(sorted(x["options"]))), []).append(x)
    cards = {}
    for (kind, labs), rs in by.items():
        if len(rs) >= 100:
            cards[rs[0]["source"], labs] = compile_card(kind, rs[0]["instructions"], list(rs[0]["options"]))
    src_card = {s: c for (s, _), c in cards.items()}
    rc = random.Random(7)
    SYMS = ["Label-K", "Label-Q", "Label-Z", "Label-W", "Label-J", "Label-V"]
    for x in rows:
        c = src_card.get(x["source"])
        if not c or rc.random() >= 0.5:
            continue
        if x["qtype"] == "choice" and sorted(x["options"]) == sorted(c["labels"]) and rc.random() < 0.3:
            mp = dict(zip(c["labels"], rc.sample(SYMS, len(c["labels"]))))  # symbol tuning: names carry no meaning
            renamed = {"labels": [mp[l] for l in c["labels"]], "cards": {mp[l]: c["cards"][l] for l in c["labels"]}}
            x["options"] = [mp[o] for o in x["options"]]
            x["gold"] = mp[x["gold"]]
            x["card"] = card_text(renamed)
            x["meta"] = {**x["meta"], "symbols": True}
            added["symbol_rows"] += 1
        else:
            x["card"] = card_text(c)
            added["card_rows"] += 1
    ev = {norm(json.loads(l)["state"]) for f in ("eval.jsonl", "devp.jsonl", "devzs.jsonl", "devzs2.jsonl") for l in open(OUT / f)}
    bad = [x for x in rows if norm(x["state"]) in ev]
    assert not bad, f"{len(bad)} rows overlap eval/dev states"
    assert len({x["id"] for x in rows}) == len(rows)
    with open(OUT / "train_v06.jsonl", "w") as f:
        for x in rows:
            f.write(json.dumps(x) + "\n")
    with open(OUT / "train_v06_relations.jsonl", "w") as f:
        for x in rels:
            f.write(json.dumps(x) + "\n")
    print(json.dumps({"rows": len(rows), "new_rows": len(T.rows), "cards_compiled": len(cards), "added": dict(added),
                      "anchor_rows": sum(bool(x.get("meta", {}).get("anchor")) for x in rows),
                      "by_source": dict(Counter(x["source"] for x in rows).most_common())}, indent=1))


if __name__ == "__main__":
    main()
