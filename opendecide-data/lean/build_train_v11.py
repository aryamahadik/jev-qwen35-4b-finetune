"""v0.11 training mix: ONE consolidated stage from the base model (no chaining), fixed quotas, whole call units kept.
Blocks (data/v11_parts/ unless noted):
  taskbank_train      label-set breadth, Claude-written definitions, 30% labels renamed to codes
  hard_train (x2)     Claude-authored hard definition-application items, blind-solved agreement only
  intent_train        clinc/banking/MASSIVE with random option sets (3-80 options, 12% 'none' gold)
  dbpedia_train       class-balanced
  claims_train        45/45/10 planted claims + flipped twins, 'inv' relations
  negation_train      ~300 new templates, complement/equiv pairs (sampled)
  judge/lah/debate/pg/ohr (data/)   reasoning and judging replay (debates class-balanced)
  v0.7 classification (non-intent, non-dbpedia, non-injection) with KL-anchor flags; a small claim-check (meta) sample
Everything overlapping held-out or selection data (OHS-1, JevBench public, all dev/eval files) is dropped by 12-word
runs. Writes data/train_v11.jsonl + data/train_v11_relations.jsonl and copies the v11 dev sets to data/.
"""
import json
import random
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D, P = HERE / "data", HERE / "data/v11_parts"
rj = lambda p: [json.loads(l) for l in open(p)] if Path(p).exists() else []
words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
rng = random.Random(20261002)


def units(rows):
    u = defaultdict(list)
    for r in rows:
        u[r["call_id"]].append(r)
    return list(u.values())


def sample_units(rows, n_rows, key=None):
    us = units(rows)
    rng.shuffle(us)
    if key:  # class-balance whole units by a key of their first row
        by = defaultdict(list)
        for u in us:
            by[key(u[0])].append(u)
        order = []
        for grp in zip(*by.values()):
            order.extend(grp)
        us = order
    out = []
    for u in us:
        if len(out) >= n_rows:
            break
        out.extend(u)
    return out


def dup(rows, tag):
    return [{**r, "id": r["id"] + tag, "call_id": r["call_id"] + tag} for r in rows]


def grams(t, n=12):
    w = words(t)
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))} or ({" ".join(w)} if w else set())


def main():
    v07 = rj(D / "train_v07.jsonl")
    blocks = {
        "taskbank": rj(P / "taskbank_train.jsonl"),
        "hard": rj(P / "hard_train.jsonl"),
        "intent": rj(P / "intent_train.jsonl"),
        "dbpedia": rj(P / "dbpedia_train.jsonl"),
        "claims": rj(P / "claims_train.jsonl"),
        "negation": sample_units(rj(P / "negation_train.jsonl"), 7000),
        "judge": sample_units(rj(D / "judge_train.jsonl"), 3500),
        "lah": rj(D / "lah_train.jsonl"),
        "debate": sample_units(rj(D / "debate_train.jsonl"), 1800, key=lambda r: r["meta"].get("deleted")),
        "pg": sample_units(rj(D / "pg_train.jsonl"), 3000),
        "ohr": sample_units(rj(D / "ohr_train.jsonl"), 2000),
        "v07_cls": sample_units([r for r in v07 if r["track"] in ("L0", "L2") and r["source"] not in
                                 ("clinc150", "banking77", "massive", "dbpedia") and not r["source"].startswith("lah")], 5000),
        "meta": sample_units([r for r in v07 if r["source"] == "meta"], 1500),
    }
    blocks["hard_x2"] = dup(blocks["hard"], "_x2")
    rows = [r for b in blocks.values() for r in b]
    rows = list({r["id"]: r for r in rows}.values())
    # drop anything overlapping held-out tests, JevBench public, dev or eval sets
    # held-out tests: any shared 12-word run drops the call; dev sets (selection only, often from the same generators,
    # so template sentences repeat): only exact duplicate texts are dropped
    held, dev_exact = set(), set()
    for f in ["ohs.jsonl", "eval.jsonl", "eval_card.jsonl", "eval_jagged.jsonl", "eval_opi.jsonl", "eval_long.jsonl", "eval_multi.jsonl"]:
        for x in rj(D / f):
            held |= grams(x["state"])
    for f in [D / "dev.jsonl", D / "devzs.jsonl", D / "devzs2.jsonl", D / "devp_card.jsonl", D / "pg_dev.jsonl",
              D / "debate_dev.jsonl"] + [P / f"{n}.jsonl" for n in ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims")]:
        for x in rj(f):
            dev_exact.add(" ".join(words(x["state"])))
    jb = HERE.parents[1] / "bench/jevbench/datasets/public"
    for f in jb.glob("*.jsonl"):
        for l in open(f):
            x = json.loads(l)
            held |= grams(json.dumps(x.get("state"), ensure_ascii=False) + " " + json.dumps(x.get("question"), ensure_ascii=False), 10)
    bad_calls = {r["call_id"] for r in rows if (grams(r["state"]) & held) or " ".join(words(r["state"])) in dev_exact}
    dropped = Counter(r["source"] for r in rows if r["call_id"] in bad_calls)
    rows = [r for r in rows if r["call_id"] not in bad_calls]
    ids = {r["id"] for r in rows}
    rels = []
    for f in ["taskbank_relations.jsonl", "claims_relations.jsonl", "negation_relations.jsonl", "hard_relations.jsonl"]:
        rels += rj(P / f)
    rels += rj(D / "judge_train_relations.jsonl") + rj(D / "train_v07_relations.jsonl")
    rels = [x for x in {(x["type"], x["a"], x["b"]): x for x in rels}.values() if x["a"] in ids and x["b"] in ids]
    for r in rows:  # new blocks learn freely; only the old classification rows keep their KL-anchor flag
        r.setdefault("meta", {})
    (D / "train_v11.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (D / "train_v11_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    for f in ["dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims"]:
        shutil.copy(P / f"{f}.jsonl", D / f"{f}.jsonl")
        if (P / f"{f}_relations.jsonl").exists():
            shutil.copy(P / f"{f}_relations.jsonl", D / f"{f}_relations.jsonl")
    summ = {"rows": len(rows), "relations": dict(Counter(x["type"] for x in rels)),
            "blocks": {k: len(v) for k, v in blocks.items()}, "dropped_for_overlap": dict(dropped),
            "anchor_rows": sum(bool(r["meta"].get("anchor")) for r in rows),
            "option_hist": dict(Counter(min(len(r["options"] or [0, 0]), 99) for r in rows).most_common(12)),
            "qtype": dict(Counter(r["qtype"] for r in rows))}
    (D / "train_v11_summary.json").write_text(json.dumps(summ, indent=1))
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
