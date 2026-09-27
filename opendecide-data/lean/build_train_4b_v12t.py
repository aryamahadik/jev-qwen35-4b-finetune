"""v0.12-4B teacher round T (PRISM_2B_MASTER_PLAN.md §6): continue q35_4b_v11c on the new Claude-written data + a CLEAN
replay, gold labels only (no distillation).
  hard12 (x2)   data/v12_parts/hard12_train.jsonl: 2B dev-gap families (policy, NLI, procedure, intent, codebook, emotion)
  proc12        data/v12_parts/proc12_train.jsonl: procedural decisions (replaces the legacy Qwen3-235B lah_* items)
  planted12     data/v12_parts/planted12_train.jsonl: "does this text dictate the answer?" (replaces legacy meta_*)
  replay        data/train_2b.jsonl minus lah_* / meta_* rows, with the Qwen3-235B card definitions swapped for the
                Claude-written ones (data/v12_parts/card_swap.json), sampled by unit across the v0.11 skill families
Overlap filter: a unit is dropped if its state shares a 12-word run with a held-out test (OHS-1/2/3, eval*) or equals a
dev state exactly (including the new v12 dev splits). Also writes the v12 dev splits to data/ for evaluation.
Writes data/train_4b_v12t.jsonl + data/train_4b_v12t_relations.jsonl. CPU only, deterministic (seed 20261015).
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D, V = HERE / "data", HERE / "data/v12_parts"
rj = lambda p: [json.loads(l) for l in open(p)] if Path(p).exists() else []
rng = random.Random(20261015)
LEGACY = ("lah_", "meta")


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


def swap_cards(r, swap):
    if not r.get("card"):
        return r, 0
    lines, n = [], 0
    for ln in r["card"].split("\n"):
        if ln.startswith("- ") and ": " in ln:
            lab, d = ln[2:].split(": ", 1)
            if d in swap:
                ln, n = f"- {lab}: {swap[d]}", n + 1
        lines.append(ln)
    return ({**r, "card": "\n".join(lines)} if n else r), n


def fam(s):
    for p in ("hard_", "std_", "pg_", "judge", "binj", "tb_", "wiki"):
        if s.startswith(p):
            return p.rstrip("_")
    return "other"


def main():
    swap = json.load(open(V / "card_swap.json"))
    base = [r for r in rj(D / "train_2b.jsonl") if not r["source"].startswith(LEGACY)]
    swapped = 0
    rows2 = []
    for r in base:
        r2, n = swap_cards(r, swap)
        swapped += n > 0
        rows2.append(r2)
    legacy_left = sum(1 for r in rows2 for ln in (r.get("card") or "").split("\n")
                      if ln.startswith("- ") and ": " in ln and ln[2:].split(": ", 1)[1] in swap)
    assert legacy_left == 0, legacy_left
    by = defaultdict(list)
    for r in rows2:
        by[fam(r["source"])].append(r)
    replay = (take_units(by["tb"], 1100) + take_units(by["hard"], 500) + take_units(by["pg"], 500)
              + take_units(by["judge"], 350) + take_units(by["std"], 250) + take_units(by["binj"], 250)
              + take_units(by["wiki"], 150) + take_units(by["other"], 1100))
    new = {k: rj(V / f"{k}12_train.jsonl") for k in ("hard", "proc", "planted")}
    assert all(new.values()), {k: len(v) for k, v in new.items()}
    rows = (new["hard"] + [{**r, "id": r["id"] + "_x2", "call_id": r["call_id"] + "_x2"} for r in new["hard"]]
            + new["proc"] + new["planted"] + replay)
    rows = list({r["id"]: r for r in rows}.values())
    words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()

    def grams(t):
        w = words(t)
        return {" ".join(w[i:i + 12]) for i in range(max(0, len(w) - 11))}
    held = set()
    for f in ["ohs", "ohs2", "ohs3", "eval", "eval_card", "eval_jagged", "eval_opi", "eval_long", "eval_multi"]:
        for x in rj(D / f"{f}.jsonl"):
            held |= grams(x["state"])
    devs = ["dev", "devzs", "devzs2", "devp_card", "pg_dev", "debate_dev", "dev_nc", "taskbank_dev", "hard_dev",
            "dev_negwords", "dev_claims"]
    dev_exact = {" ".join(words(x["state"])) for f in devs for x in rj(D / f"{f}.jsonl")}
    for k in ("hard", "proc", "planted"):  # new in-family dev splits, also copied to data/ for evaluation
        dv = rj(V / f"{k}12_dev.jsonl")
        (D / f"{k}12_dev.jsonl").write_text("".join(json.dumps(x) + "\n" for x in dv))
        dev_exact |= {" ".join(words(x["state"])) for x in dv}
    bad = {r["call_id"] for r in rows if (grams(r["state"]) & held) or " ".join(words(r["state"])) in dev_exact}
    print("dropped for overlap:", Counter(r["source"] for r in rows if r["call_id"] in bad))
    rows = [r for r in rows if r["call_id"] not in bad]
    rng.shuffle(rows)
    ids = {r["id"] for r in rows}
    rels = rj(D / "train_2b_relations.jsonl") + [x for k in ("hard", "proc", "planted") for x in rj(V / f"{k}12_relations.jsonl")]
    rels = [x for x in {(x["type"], x["a"], x["b"]): x for x in rels}.values() if x["a"] in ids and x["b"] in ids]
    (D / "train_4b_v12t.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (D / "train_4b_v12t_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    print(json.dumps({"rows": len(rows), "new": {k: len(v) for k, v in new.items()}, "replay": len(replay),
                      "legacy_rows_removed": 59723 - len(base), "replay_pool_rows_with_swapped_cards": swapped,
                      "relations": dict(Counter(x["type"] for x in rels)),
                      "legacy_sources_left": sum(r["source"].startswith(LEGACY) for r in rows),
                      "top_families": Counter(fam(r["source"]) for r in rows).most_common(10)}, indent=1))


if __name__ == "__main__":
    main()
