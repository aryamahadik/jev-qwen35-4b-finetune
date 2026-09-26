"""Build procedural-generator (PG) train/dev rows from the 7 pg/ families.

Usage: python3 build_pg.py [--n 1300] [--n-dev 150]
Writes data/pg_train.jsonl, data/pg_dev.jsonl, data/pg_dev_relations.jsonl (empty).
Train seed = 20260926 + family index; dev seed = 20260926 + 1000 + family index.
Dev items whose state also appears in train are dropped (and replaced), so the
two files share no state text.
"""
import argparse
import collections
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pg import conflict, evidence, multihop, numeric, policy, routing, temporal  # noqa: E402

FAMILIES = [
    ("temporal", temporal),
    ("numeric", numeric),
    ("policy", policy),
    ("multihop", multihop),
    ("evidence", evidence),
    ("conflict", conflict),
    ("routing", routing),
]
BASE_SEED = 20260926
DEV_OFFSET = 1000
DATA = os.path.join(HERE, "data")


def to_row(item, family, split_tag, split, i):
    meta = dict(item.get("meta") or {})
    meta["anchor"] = False
    # train_decoder.py reads soft targets from meta.gold_probs
    if item.get("gold_probs") is not None:
        meta["gold_probs"] = item["gold_probs"]
    row = {
        "id": f"r_pg_{family}_{split_tag}_{i}",
        "group_id": f"g:pg:{family}:{split_tag}:{i}",
        "call_id": f"c_pg_{family}_{split_tag}_{i}",
        "split": split,
        "track": "PG",
        "source": f"pg_{family}",
        "state": item["state"],
        "qtype": item["qtype"],
        "instructions": item["instructions"],
        "options": item.get("options"),
        "gold": item["gold"],
        "role": "choice" if item["qtype"] == "choice" else "aff",
        "meta": meta,
    }
    if item.get("card"):
        row["card"] = item["card"]
    return row


def gen_unique(mod, n, seed, exclude):
    """Generate n items with states unique within the batch and not in `exclude`."""
    out, seen, extra = [], set(exclude), 0
    while len(out) < n:
        batch = mod.generate(n + extra, seed)
        out, seen = [], set(exclude)
        for it in batch:
            if it["state"] in seen:
                continue
            seen.add(it["state"])
            out.append(it)
            if len(out) == n:
                break
        extra += max(10, n // 10)
        if extra > n * 2:
            raise RuntimeError(f"{mod.__name__}: cannot reach {n} unique items")
    return out


def validate(rows):
    errs = []
    ids = collections.Counter(r["id"] for r in rows)
    errs += [f"dup id {k}" for k, v in ids.items() if v > 1]
    req = ["id", "group_id", "call_id", "split", "track", "source", "state",
           "qtype", "instructions", "options", "gold", "role", "meta"]
    for r in rows:
        for k in req:
            if k not in r:
                errs.append(f"{r.get('id')}: missing {k}")
        if not isinstance(r["state"], str) or not r["state"].strip():
            errs.append(f"{r['id']}: empty state")
        if not isinstance(r["instructions"], str) or not r["instructions"].strip():
            errs.append(f"{r['id']}: empty instructions")
        if r["meta"].get("anchor") is not False:
            errs.append(f"{r['id']}: anchor not False")
        if r["qtype"] == "choice":
            o = r["options"]
            if not isinstance(o, list) or len(o) < 2 or len(set(o)) != len(o):
                errs.append(f"{r['id']}: bad options")
            elif r["gold"] not in o:
                errs.append(f"{r['id']}: gold not in options")
            if r["role"] != "choice":
                errs.append(f"{r['id']}: role")
        elif r["qtype"] == "noul":
            if r["gold"] not in (0, 1) or isinstance(r["gold"], bool):
                errs.append(f"{r['id']}: noul gold {r['gold']!r}")
            if r["options"] is not None:
                errs.append(f"{r['id']}: noul options not None")
            if r["role"] != "aff":
                errs.append(f"{r['id']}: role")
        else:
            errs.append(f"{r['id']}: qtype {r['qtype']}")
        gp = r["meta"].get("gold_probs")
        if gp is not None:
            if abs(sum(gp.values()) - 1) > 1e-3:
                errs.append(f"{r['id']}: gold_probs sum {sum(gp.values())}")
            if set(gp) != set(r["options"] or []):
                errs.append(f"{r['id']}: gold_probs keys != options")
        if r.get("card") is not None and not isinstance(r["card"], str):
            errs.append(f"{r['id']}: card not str")
    return errs


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p / 100 * len(xs)))]


def stats(rows, label):
    print(f"\n=== {label}: {len(rows)} rows ===")
    by = collections.defaultdict(list)
    for r in rows:
        by[r["source"][3:]].append(r)
    bad = []
    for fam, rs in by.items():
        L = [len(r["state"]) for r in rs]
        noul = [r for r in rs if r["qtype"] == "noul"]
        yes = sum(r["gold"] for r in noul) / max(1, len(noul))
        ch = [r for r in rs if r["qtype"] == "choice"]
        # gold-position uniformity: observed vs expected share at position 0..k-1
        obs, exp = collections.Counter(), collections.Counter()
        for r in ch:
            k = len(r["options"])
            obs[r["options"].index(r["gold"])] += 1
            for j in range(k):
                exp[j] += 1 / k
        chi = sum((obs[j] - exp[j]) ** 2 / exp[j] for j in exp if exp[j] > 0)
        dfree = max(1, len(exp) - 1)
        pos = " ".join(f"{j}:{obs[j]}/{exp[j]:.0f}" for j in sorted(exp) if exp[j] >= 1)
        print(f"{fam:9s} n={len(rs)} choice={len(ch)} noul={len(noul)} yes={yes:.3f} "
              f"len p10/50/90/max={pct(L,10)}/{pct(L,50)}/{pct(L,90)}/{max(L)} "
              f"gp={sum(1 for r in rs if r['meta'].get('gold_probs'))}")
        print(f"          gold pos obs/exp {pos}  chi2={chi:.1f} df={dfree}")
        if noul and not (0.40 <= yes <= 0.60):
            bad.append(f"{fam}: noul yes-rate {yes:.3f}")
        # crude: chi2 far beyond df suggests positional bias
        if chi > dfree + 4 * math.sqrt(2 * dfree) + 5:
            bad.append(f"{fam}: gold position non-uniform chi2={chi:.1f}")
    L = [len(r["state"]) for r in rows]
    print(f"ALL len p10/25/50/75/90/max = {pct(L,10)}/{pct(L,25)}/{pct(L,50)}/"
          f"{pct(L,75)}/{pct(L,90)}/{max(L)}; short<600={sum(x<600 for x in L)} "
          f"long>2500={sum(x>2500 for x in L)}")
    oc = collections.Counter(len(r["options"]) for r in rows if r["qtype"] == "choice")
    print("option-count hist:", dict(sorted(oc.items())))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1300)
    ap.add_argument("--n-dev", type=int, default=150)
    a = ap.parse_args()

    train, dev = [], []
    for idx, (fam, mod) in enumerate(FAMILIES):
        tr = gen_unique(mod, a.n, BASE_SEED + idx, set())
        tr_states = {it["state"] for it in tr}
        dv = gen_unique(mod, a.n_dev, BASE_SEED + DEV_OFFSET + idx, tr_states)
        train += [to_row(it, fam, "train", "train", i)
                  for i, it in enumerate(tr)]
        dev += [to_row(it, fam, "dev", "pg_dev", i) for i, it in enumerate(dv)]
        print(f"{fam}: train {len(tr)} dev {len(dv)}", flush=True)

    errs = validate(train + dev)
    assert not ({r["state"] for r in train} & {r["state"] for r in dev}), "train/dev overlap"
    bad = stats(train, "pg_train") + stats(dev, "pg_dev")
    if errs:
        print("VALIDATION ERRORS:", len(errs), errs[:20])
        sys.exit(1)
    if bad:
        print("DISTRIBUTION WARNINGS:", bad)

    os.makedirs(DATA, exist_ok=True)
    for name, rows in (("pg_train.jsonl", train), ("pg_dev.jsonl", dev)):
        with open(os.path.join(DATA, name), "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    open(os.path.join(DATA, "pg_dev_relations.jsonl"), "w").close()
    print(f"\nwrote {len(train)} train, {len(dev)} dev rows; validation OK")


if __name__ == "__main__":
    main()
