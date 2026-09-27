"""2B v0.12 stage (continue from q35_2b_v11r): the new Claude-written hard items for the 2B's dev weak spots + replay.
  hard12 (x2)       data/v12_parts/hard12_train.jsonl (build_v12_hard.py): policy, NLI, procedural reasoning, speaker
                    intent, codebook coding, emotion in context. Families chosen from the 2B's dev gaps only (dev_nc,
                    hard_dev, pg_dev); OHS-2 task families were excluded at authoring time. Gold labels only (no kd).
  replay            rows from the 2B mix (train_2b_kd.jsonl, with the 4B teacher's soft labels) weighted to the same weak
                    families: v0.11 hard items, procedural (pg), judge, taskbank, negation, claims, intents, binj, std
Overlap filter as in build_train_v11c.py: any shared 12-word run with a held-out test, or an exact dev text, drops the unit.
Writes data/train_2b_v12.jsonl + data/train_2b_v12_relations.jsonl.
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
rj = lambda p: [json.loads(l) for l in open(p)] if Path(p).exists() else []
rng = random.Random(20261012)


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
    new = rj(D / "v12_parts/hard12_train.jsonl")
    assert new, "run build_v12_hard.py first"
    mix = rj(D / "train_2b_kd.jsonl")
    fam = lambda r: r["source"].split("_")[0]
    by = defaultdict(list)
    for r in mix:
        s = r["source"]
        key = ("hard" if s.startswith("hard_") else "std" if s.startswith("std_") else "pg" if s.startswith("pg_")
               else "judge" if s.startswith("judge") else "binj" if s.startswith("binj") else "tb" if s.startswith("tb")
               else "other")
        by[key].append(r)
    rows = (new + [{**r, "id": r["id"] + "_x2", "call_id": r["call_id"] + "_x2"} for r in new]
            + take_units(by["hard"], 2000) + take_units(by["pg"], 2500) + take_units(by["judge"], 1200)
            + take_units(by["tb"], 2500) + take_units(by["std"], 800) + take_units(by["binj"], 800)
            + take_units(by["other"], 3000))
    rows = list({r["id"]: r for r in rows}.values())
    words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()

    def grams(t):
        w = words(t)
        return {" ".join(w[i:i + 12]) for i in range(max(0, len(w) - 11))}
    held = set()  # held-out tests (any shared 12-word run) and dev sets (exact text) must not appear in training
    for f in ["ohs", "ohs2", "ohs3", "eval", "eval_card", "eval_jagged", "eval_opi", "eval_long", "eval_multi"]:
        for x in rj(D / f"{f}.jsonl"):
            held |= grams(x["state"])
    dev_exact = {" ".join(words(x["state"])) for f in ["dev", "devzs", "devzs2", "devp_card", "pg_dev", "debate_dev", "dev_nc",
                 "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims"] for x in rj(D / f"{f}.jsonl")}
    dev_exact |= {" ".join(words(x["state"])) for x in rj(D / "v12_parts/hard12_dev.jsonl")}
    bad = {r["call_id"] for r in rows if (grams(r["state"]) & held) or " ".join(words(r["state"])) in dev_exact}
    print("dropped for overlap:", Counter(r["source"] for r in rows if r["call_id"] in bad))
    rows = [r for r in rows if r["call_id"] not in bad]
    rng.shuffle(rows)
    ids = {r["id"] for r in rows}
    rels = rj(D / "train_2b_relations.jsonl") + rj(D / "v12_parts/hard12_relations.jsonl")
    rels = [x for x in {(x["type"], x["a"], x["b"]): x for x in rels}.values() if x["a"] in ids and x["b"] in ids]
    (D / "train_2b_v12.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (D / "train_2b_v12_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    print(json.dumps({"rows": len(rows), "new": len(new), "relations": dict(Counter(x["type"] for x in rels)),
                      "kd_rows": sum(isinstance((r.get("meta") or {}).get("teacher"), dict) for r in rows),
                      "top_sources": Counter(fam(r) for r in rows).most_common(12)}, indent=1))


if __name__ == "__main__":
    main()
