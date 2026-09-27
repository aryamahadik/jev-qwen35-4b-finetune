"""v0.13 BREADTH corpus: assemble data/v13_parts/raw/*.jsonl + defs/*.json (23 public, human-written and human-labelled
datasets, train splits only, built and verified by breadth_src/build_<key>.py) into OpenDecide training rows.

Per raw row
  yes/no (options {yes, no})  -> qtype noul, gold 1/0, card "- yes: ... / - no: ..." (what yes and no mean here)
  choice                      -> qtype choice, card "- <option>: <definition>" for exactly the row's options;
                                 in 30% of choice rows with 3+ options the option names are replaced by opaque codes
                                 ("Class Q", "Code 17", ...) with the same definitions, so the model must read the card
  annotator distributions     -> meta.teacher ({"yes": p} or {option: p}) = soft targets for the kd loss
Derived consistency bundles: for 25% of choice rows, an "Is the answer X?" yes/no row (X = gold half the time, else
another option) plus its negated twin ("Is it wrong to answer X?", role neg), linked by a complement relation.
Decontamination: a group is dropped if any of its texts shares a 12-word run with a held-out test (OHS-1/2/3, eval*,
JevBench public items, every string field) or equals a dev state exactly (all dev splits, v12 devs).
Split: 10% of groups per dataset -> breadth_dev (in-family measurement), the rest -> breadth_train.
Outputs (data/v13_parts/): breadth_train.jsonl, breadth_dev.jsonl, breadth_relations.jsonl, breadth_dev_relations.jsonl,
breadth_summary.json. Deterministic (seed 20261105), CPU only.
"""
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D, V = HERE / "data", HERE / "data/v13_parts"
BENCH = HERE.parent.parent / "bench/jevbench/datasets/public"
SEED = 20261105
CODES = ([f"Class {c}" for c in "ABCDEFGHJKLMNPQRSTUVWXYZ"] + [f"Code {i}" for i in range(10, 60)]
         + [f"Option {c}" for c in "ABCDEFGHJKLMNPQRSTUVWXYZ"])
words = lambda t: re.sub(r"[^\w]+", " ", (t or "").lower()).split()
h = lambda *p: int(hashlib.sha256(":".join(map(str, (SEED, *p))).encode()).hexdigest(), 16)
cid = lambda ins, st, opts: "c_" + hashlib.sha1(json.dumps([ins, st, opts], ensure_ascii=False).encode()).hexdigest()[:12]


def grams(text):
    w = words(text)
    return {" ".join(w[i:i + 12]) for i in range(len(w) - 11)} if len(w) >= 12 else ({" ".join(w)} if w else set())


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def held_out_grams():
    g = set()
    for f in ["ohs", "ohs2", "ohs3", "eval", "eval_card", "eval_jagged", "eval_opi", "eval_long", "eval_multi"]:
        p = D / f"{f}.jsonl"
        if p.exists():
            for l in open(p):
                g |= grams(json.loads(l).get("state", ""))
    for p in sorted(BENCH.glob("*.jsonl")):
        for l in open(p):
            for s in strings(json.loads(l)):
                g |= grams(s)
    return g


def dev_exact():
    out = set()
    for f in ["dev", "devzs", "devzs2", "devp_card", "pg_dev", "debate_dev", "dev_nc", "taskbank_dev", "hard_dev",
              "dev_negwords", "dev_claims", "hard12_dev", "proc12_dev", "planted12_dev"]:
        p = D / f"{f}.jsonl"
        if p.exists():
            out |= {" ".join(words(json.loads(l)["state"])) for l in open(p)}
    return out


def card(pairs):
    return "\n".join(f"- {a}: {b}" for a, b in pairs)


def main():
    held, devx = held_out_grams(), dev_exact()
    out, rels, report, dropped = [], [], {}, Counter()
    for rp in sorted((V / "raw").glob("*.jsonl")):
        key = rp.stem
        defs = json.load(open(V / "defs" / f"{key}.json"))
        raw = [json.loads(l) for l in open(rp)]
        rng = random.Random(h("rows", key))
        n, rep = 0, Counter()
        for r in raw:
            st, ins, opts, gold = r["state"], r["instructions"], list(r["options"]), r["gold"]
            if (grams(st) & held) or " ".join(words(st)) in devx:
                dropped[key] += 1
                continue
            gid = f"g:br:{key}:{r['rid']}"
            split = "dev" if h("split", gid) % 10 == 0 else "train"
            soft = r.get("soft") or None
            base_meta = {"dataset": r["meta"].get("dataset"), "licence": r["meta"].get("licence"), "domain": key}
            yn = sorted(o.lower() for o in opts) == ["no", "yes"]
            if yn:
                g = 1 if str(gold).lower() == "yes" else 0
                c = card([(k, defs[k]) for k in ("yes", "no") if k in defs])
                meta = dict(base_meta)
                if soft:
                    meta["teacher"] = {"yes": float({k.lower(): v for k, v in soft.items()}.get("yes", g))}
                n += 1
                out.append({"id": f"r_br_{key}_{n}", "group_id": gid, "call_id": cid(ins, st, None), "split": split,
                            "track": "BR", "source": f"br_{key}", "state": st, "qtype": "noul", "instructions": ins,
                            "options": None, "gold": g, "role": "aff", "card": c, "meta": meta})
                rep["noul"] += 1
                continue
            if any(o not in defs for o in opts) or gold not in opts:
                dropped[key + ":no_def_or_gold"] += 1
                continue
            show, mp = opts, {o: o for o in opts}
            if 3 <= len(opts) <= 50 and rng.random() < 0.30:  # opaque codes: the definitions carry the meaning
                fams = [f for f in ("Class", "Code", "Option") if sum(x.startswith(f) for x in CODES) >= len(opts)]
                fam = rng.choice(fams)
                pool = [x for x in CODES if x.startswith(fam)]
                rng.shuffle(pool)
                mp = dict(zip(opts, pool[:len(opts)]))
                show = [mp[o] for o in opts]
            meta = dict(base_meta, **({"renamed": True} if show != opts else {}))
            if soft:
                tot = sum(float(soft.get(o, 0.0)) for o in opts) or 1.0
                meta["teacher"] = {mp[o]: float(soft.get(o, 0.0)) / tot for o in opts}
            n += 1
            base_id = f"r_br_{key}_{n}"
            out.append({"id": base_id, "group_id": gid, "call_id": cid(ins, st, show), "split": split, "track": "BR",
                        "source": f"br_{key}", "state": st, "qtype": "choice", "instructions": ins, "options": show,
                        "gold": mp[gold], "role": "choice", "card": card([(mp[o], defs[o]) for o in opts]), "meta": meta})
            rep["choice"] += 1
            rep["renamed"] += show != opts
            if rng.random() < 0.25:  # yes/no bundle with a complement relation
                x = gold if rng.random() < 0.5 else rng.choice([o for o in opts if o != gold])
                others = [o for o in opts if o not in (x, gold)]
                rng.shuffle(others)
                lines = [(o, defs[o]) for o in dict.fromkeys([x, gold] + others[:4])]
                c2 = card(lines)
                g_aff = int(x == gold)
                p_x = (float(soft.get(x, 0.0)) / (sum(float(soft.get(o, 0.0)) for o in opts) or 1.0)) if soft else None
                q_aff = f'{ins}\nIs the correct answer "{x}"?'
                q_neg = f'{ins}\nIs it wrong to answer "{x}"?'
                for suf, q, g_, role, p in (("ya", q_aff, g_aff, "aff", p_x),
                                            ("yn", q_neg, 1 - g_aff, "neg", None if p_x is None else 1 - p_x)):
                    m2 = dict(base_meta, asked_label=x, **({"teacher": {"yes": p}} if p is not None else {}))
                    out.append({"id": f"{base_id}_{suf}", "group_id": gid, "call_id": cid(q, st, None), "split": split,
                                "track": "BR", "source": f"br_{key}", "state": st, "qtype": "noul", "instructions": q,
                                "options": None, "gold": g_, "role": role, "card": c2, "meta": m2})
                rels.append({"type": "complement", "a": f"{base_id}_ya", "b": f"{base_id}_yn", "track": split})
                rep["bundles"] += 1
        report[key] = dict(rep, raw=len(raw), dropped=dropped[key], no_def=dropped[key + ":no_def_or_gold"])
    ids = [r["id"] for r in out]
    assert len(ids) == len(set(ids)), "duplicate ids"
    sys.path.insert(0, str(HERE))
    from train_decoder import check_rows
    check_rows(out, kd=0.5)
    train = [r for r in out if r["split"] == "train"]
    dev = [r for r in out if r["split"] == "dev"]
    tr_ids = {r["id"] for r in train}
    dump = lambda name, rows: (V / name).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    dump("breadth_train.jsonl", train)
    dump("breadth_dev.jsonl", dev)
    dump("breadth_relations.jsonl", [x for x in rels if x["a"] in tr_ids])
    dump("breadth_dev_relations.jsonl", [x for x in rels if x["a"] not in tr_ids])
    summ = {"rows": len(out), "train": len(train), "dev": len(dev), "relations": len(rels),
            "soft_rows": sum("teacher" in r["meta"] for r in out), "qtype": dict(Counter(r["qtype"] for r in out)),
            "dropped_overlap": dict(dropped), "datasets": report}
    (V / "breadth_summary.json").write_text(json.dumps(summ, indent=1))
    print(json.dumps({k: v for k, v in summ.items() if k != "datasets"}, indent=1))


if __name__ == "__main__":
    main()
