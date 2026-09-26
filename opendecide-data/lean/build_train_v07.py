"""Train set v0.7 (single model, Qwen3.5-4B): v0.6s + injection v2 + procedural hard decisions + meta-claim rows.

  v0.6s        robustness / breadth / task cards / KL-anchor flags (unchanged)
  inj_v2       planted authority claims in untrusted places, with invariance relations to clean twins
  pg_train     procedural hard decisions with exact code-computed gold (temporal, numeric, policy, multi-hop,
               probabilistic evidence with soft Bayes targets, conflicts/traps, routing/rubrics)
  lah          LLM-authored hard items (gen_lah.py: open teacher Qwen3-235B, kept only on blind re-solve agreement), 2x
  ohr          open multi-step reasoning (build_ohr.py: ProofWriter, FLD, LogiQA 2.0, MuSR)
  injg         1,000 more injection rows with teacher-written claim wording (gen_meta.py), invariance relations
  meta         "does this text dictate/pre-announce the answer?" (the check used by leverage-bounded decoding):
               positives = planted claims and answer directives; negatives = facts, rules, messages, admin notes
Held out: every eval / dev / panel / JevBench / jagged text (asserted by state overlap below).
Writes data/train_v07.jsonl + data/train_v07_relations.jsonl.
"""
import json
import random
import re
from collections import Counter
from pathlib import Path

import build_inj_v2 as inj
from decoder_io import META_Q

HERE = Path(__file__).resolve().parent
D = HERE / "data"
rj = lambda p: [json.loads(l) for l in open(p)] if Path(p).exists() else []
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def meta_rows(base, pg, gen_pos, gen_neg, n_pos=750, n_neg=1500, seed=7):
    r = random.Random(seed)
    opts = [o for x in base if x["qtype"] == "choice" for o in x["options"]][:5000] or ["approved", "denied"]
    out = []
    for i in range(n_pos):
        T = r.choice(opts + ["yes", "no"])
        txt = r.choice(inj.CLAIMS + inj.DIRECTIVES_NOUL).format(T=T)
        if r.random() < 0.5:
            txt = f"{r.choice(inj.FIELDS)}: {txt}"
        out.append((txt, 1))
    for x in gen_pos:  # teacher-written planted claims (gen_meta.py), varied wording
        out.append((x["text"].replace("{T}", r.choice(opts + ["yes", "no", "approved", "denied"])), 1))
    for x in gen_neg:  # hard negatives: rules / facts / history that mention outcomes without dictating this case
        out.append((x["text"], 0))
    segs = []
    for x in r.sample(base, min(4000, len(base))) + r.sample(pg, min(2000, len(pg))):
        parts = [p for p in re.split(r"\n\s*\n", x["state"]) if 20 <= len(p) <= 1200]
        if parts:
            segs.append(r.choice(parts))
    for i in range(n_neg):
        txt = r.choice(inj.NEUTRAL) if r.random() < 0.2 else r.choice(segs)
        out.append((txt, 0))
    rows = []
    for i, (txt, g) in enumerate(out):
        rows.append({"id": f"r_meta_{i}", "group_id": f"g:meta:{i}", "call_id": f"c_meta_{i}", "split": "train",
                     "track": "L3", "source": "meta", "state": txt, "qtype": "noul", "instructions": META_Q,
                     "options": None, "gold": g, "role": "aff", "meta": {"anchor": False}})
    return rows


def inj_gen_rows(base, gen_pos, n=1000, seed=11):
    """Extra injection rows with teacher-written claim wording; noul rows get 'equiv' relations to their clean twins."""
    r = random.Random(seed)
    pool = [x for x in base if x["track"] in ("L0", "L2") and x["source"] != "mnli_neutral" and len(x["state"]) < 4000]
    r.shuffle(pool)
    out, rels = [], []
    for j, x in enumerate(pool[:n]):
        echo = r.random() < 0.25
        if x["qtype"] == "noul":
            gw = "yes" if x["gold"] == 1 else "no"
            T = gw if echo else ("no" if gw == "yes" else "yes")
        else:
            wrong = [o for o in x["options"] if o != x["gold"]]
            if not wrong:
                continue
            T = x["gold"] if echo else r.choice(wrong)
        c = r.choice(gen_pos)["text"].replace("{T}", str(T))
        st = r.choice(inj.CONTAINERS).format(s=x["state"], c=c) if r.random() < 0.6 else \
            json.dumps({"content": x["state"], r.choice(inj.FIELDS): c}, ensure_ascii=False, indent=1)
        new = {**x, "id": f"{x['id']}_injg{j}", "state": st, "track": "L3",
               "meta": {**(x.get("meta") or {}), "arm": "injg_echo" if echo else "injg_targeted", "pushed": T, "anchor": False}}
        out.append(new)
        if x["qtype"] == "noul":
            rels.append({"type": "equiv", "a": x["id"], "b": new["id"], "track": "train"})
    return out, rels


def main():
    base, base_rel = rj(D / "train_v06s.jsonl"), rj(D / "train_v06s_relations.jsonl")
    inj_rows, inj_rel = rj(D / "inj_v2.jsonl"), rj(D / "inj_v2_relations.jsonl")
    pg = rj(D / "pg_train.jsonl")
    lah = rj(D / "lah_train.jsonl")  # LLM-authored hard items (open teacher, blind re-solve agreement)
    lah = lah + [{**x, "id": x["id"] + "_x2", "call_id": x["call_id"] + "_x2"} for x in lah]  # 2x: hardest, most JevBench-like
    ohr = rj(D / "ohr_train.jsonl")  # open multi-step reasoning sets (ProofWriter, FLD, LogiQA 2.0, MuSR)
    gen_pos, gen_neg = rj(D / "meta_pos.jsonl"), rj(D / "meta_neg.jsonl")
    meta = meta_rows(base, pg, gen_pos, gen_neg)
    injg, injg_rel = inj_gen_rows(base, gen_pos)
    rows = base + inj_rows + injg + pg + lah + ohr + meta
    rels = base_rel + inj_rel + injg_rel
    held = set()
    for f in ("eval.jsonl", "eval_card.jsonl", "devp.jsonl", "dev.jsonl", "devzs.jsonl", "devzs2.jsonl", "eval_jagged.jsonl",
              "eval_opi.jsonl", "eval_long.jsonl", "eval_multi.jsonl", "pg_dev.jsonl"):
        held |= {norm(x["state"]) for x in rj(D / f)}
    bad = [x["id"] for x in rows if norm(x["state"]) in held]
    assert not bad, f"{len(bad)} train states overlap held-out sets: {bad[:3]}"
    ids = [x["id"] for x in rows]
    assert len(ids) == len(set(ids)), "duplicate ids"
    (D / "train_v07.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))
    (D / "train_v07_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    print(json.dumps({"rows": len(rows), "relations": len(rels), "parts": {"v06s": len(base), "inj_v2": len(inj_rows),
                      "injg": len(injg), "pg": len(pg), "lah": len(lah), "ohr": len(ohr),
                      "meta": len(meta), "meta_pos": sum(x["gold"] for x in meta)}, "by_track": dict(Counter(x["track"] for x in rows))}, indent=1))


if __name__ == "__main__":
    main()
