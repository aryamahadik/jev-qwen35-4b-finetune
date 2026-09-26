"""v0.11c stage (continue from q35_4b_v11b): standard-doctrine items + recover procedural reasoning.
  std_train (x2)   Claude-written items on standard rules (US hearsay, trademark spectrum, hate-speech contrasts,
                   contrastive claim/evidence), blind-solved (build_v11_std.py)
  pg/ohr/lah/judge procedural and judging replay (v0.11 had less of it; JevBench half A slipped 104 -> 100)
  binj             the v0.11b binary judgments (keep the bias fix)
  v0.11 replay     task bank, hard items, negation, claims, intents
Writes data/train_v11c.jsonl + data/train_v11c_relations.jsonl.
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D, P = HERE / "data", HERE / "data/v11_parts"
rj = lambda p: [json.loads(l) for l in open(p)] if Path(p).exists() else []
rng = random.Random(20261004)


def take_units(rows, n):
    u = defaultdict(list)
    for r in rows:
        u[r["call_id"]].append(r)
    us = list(u.values())
    rng.shuffle(us)
    out = []
    for x in us:
        if len(out) >= n:
            break
        out.extend(x)
    return out


def main():
    std = rj(P / "std_train.jsonl")
    v11_ids = {json.loads(l)["id"] for l in open(D / "train_v11.jsonl")}
    parts = {k: [r for r in rj(P / f"{k}_train.jsonl") if r["id"] in v11_ids] for k in ("taskbank", "hard", "negation", "claims", "intent")}
    rows = (std + [{**r, "id": r["id"] + "_x2", "call_id": r["call_id"] + "_x2"} for r in std]
            + take_units(rj(D / "pg_train.jsonl"), 3500) + take_units(rj(D / "ohr_train.jsonl"), 1500) + rj(D / "lah_train.jsonl")
            + take_units(rj(D / "judge_train.jsonl"), 2000) + rj(P / "binj_train.jsonl")
            + take_units(parts["taskbank"], 2500) + take_units(parts["hard"], 1000) + take_units(parts["negation"], 1000)
            + take_units(parts["claims"], 800) + take_units(parts["intent"], 500))
    rows = list({r["id"]: r for r in rows}.values())
    words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
    def grams(t):
        w = words(t)
        return {" ".join(w[i:i + 12]) for i in range(max(0, len(w) - 11))}
    held = set()  # held-out tests (any shared 12-word run) and dev sets (exact text) must not appear in training
    for f in ["ohs", "ohs2", "eval", "eval_card", "eval_jagged", "eval_opi", "eval_long", "eval_multi"]:
        for x in rj(D / f"{f}.jsonl"):
            held |= grams(x["state"])
    dev_exact = {" ".join(words(x["state"])) for f in ["dev", "devzs", "devzs2", "devp_card", "pg_dev", "debate_dev", "dev_nc",
                 "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims"] for x in rj(D / f"{f}.jsonl")}
    bad = {r["call_id"] for r in rows if (grams(r["state"]) & held) or " ".join(words(r["state"])) in dev_exact}
    print("dropped for overlap:", Counter(r["source"] for r in rows if r["call_id"] in bad))
    rows = [r for r in rows if r["call_id"] not in bad]
    ids = {r["id"] for r in rows}
    rels = rj(D / "train_v11_relations.jsonl") + rj(D / "judge_train_relations.jsonl") + rj(P / "std_relations.jsonl")
    rels = [x for x in {(x["type"], x["a"], x["b"]): x for x in rels}.values() if x["a"] in ids and x["b"] in ids]
    (D / "train_v11c.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (D / "train_v11c_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    print(json.dumps({"rows": len(rows), "std": len(std), "relations": dict(Counter(x["type"] for x in rels)),
                      "top_sources": Counter(r["source"] for r in rows).most_common(10)}, indent=1))


if __name__ == "__main__":
    main()
