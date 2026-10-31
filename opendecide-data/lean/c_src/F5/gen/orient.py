"""Repair r2: orientation of the antithetic card pairs (G7 matched twins at card level; see plan.orient_pairs).

  python -m gen.orient --set candidates_r1 --tag r1

Reads the first-pass rows (built with no orientation file), counts for every word unigram / bigram of the
model-visible text (card + instructions + state, the G7 feature set) each card's rows and yes rows, and picks which
pairs to flip (r <-> 1 - r) by seeded local searches that minimize sum_f (z_f^2)^p (p = 2, 4, 6; 24 starts; lowest max z wins) over features seen in >= 2 cards
(z_f = the feature's yes-share z-score). A flip negates both cards' signed yes excess. Writes tmp/orient_<tag>.json.
The pair's r and every card's r_card stay uniform on 20-80% (the flip is a sign, chosen from words, not labels of
any held-out item)."""
from __future__ import annotations

import argparse
import collections
import json
import random
import re

import numpy as np

from .common import OUT, TMP, progress, read_jsonl

TOK = re.compile(r"[a-z0-9]+")


def feats(r):
    t = TOK.findall("\n\n".join([r.get("card") or "", r["instructions"], r["state"]]).lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--compose", action="store_true", help="rows were built with tmp/orient_<tag>.json: XOR onto it")
    a = ap.parse_args(argv)
    prev = set(json.load(open(TMP / f"orient_{a.tag}.json"))["flip"]) if a.compose else set()
    cards = {c["card_id"]: c for c in read_jsonl(OUT / f"{a.set}.cards.jsonl")}
    n = collections.defaultdict(collections.Counter)
    y = collections.defaultdict(collections.Counter)
    for r in read_jsonl(OUT / f"{a.set}.jsonl"):
        c = r["meta"]["card_id"]
        for f in feats(r):
            n[f][c] += 1
            y[f][c] += r["gold"]
    fl = [f for f in n if len(n[f]) >= 2 and sum(n[f].values()) >= 20]
    pis = sorted({c["pair_index"] for c in cards.values()})
    pidx = {p: i for i, p in enumerate(pis)}
    U = np.zeros((len(pis), len(fl)))
    N = np.zeros(len(fl))
    for j, f in enumerate(fl):
        N[j] = sum(n[f].values())
        for c, k in n[f].items():
            U[pidx[cards[c]["pair_index"]], j] += y[f][c] - k / 2
    Z2 = 4.0 / N                  # z^2 = 4 D^2 / N; objective sum (z^2)^p, p in 2-6 (the run with the lowest max z wins)
    best = None
    for seed in range(24):
        pw = (2, 4, 6)[seed % 3]

        def obj(D, pw=pw):
            return float(np.sum((Z2 * D ** 2) ** pw))
        rng = random.Random(20261005 + seed)
        s = np.ones(len(pis))
        if seed:
            s = np.array([rng.choice((-1.0, 1.0)) for _ in pis])
        D = s @ U
        cur = obj(D)
        improved = True
        while improved:
            improved = False
            order = list(range(len(pis)))
            rng.shuffle(order)
            for i in order:
                D2 = D - 2 * s[i] * U[i]
                o2 = obj(D2)
                if o2 < cur - 1e-9:
                    s[i] = -s[i]
                    D, cur = D2, o2
                    improved = True
        zmax = float(np.max(2 * np.abs(D) / np.sqrt(N)))
        key = (zmax, int((2 * np.abs(D) / np.sqrt(N) > 4).sum()))
        if best is None or key < best[0]:
            best = (key, s.copy(), D.copy())
    cur, s, D = best
    z = 2 * np.abs(D) / np.sqrt(N)
    z0 = 2 * np.abs(np.ones(len(pis)) @ U) / np.sqrt(N)
    flip = sorted({int(pis[i]) for i in range(len(pis)) if s[i] < 0} ^ prev)
    out = {"set": a.set, "tag": a.tag, "flip": flip, "n_pairs": len(pis), "features": len(fl),
           "max_z_before": round(float(z0.max()), 2), "max_z_after": round(float(z.max()), 2),
           "n_z_over_4_before": int((z0 > 4).sum()), "n_z_over_4_after": int((z > 4).sum())}
    json.dump(out, open(TMP / f"orient_{a.tag}.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "flip"}, indent=1), len(flip), "flips")
    progress(f"orient {a.tag}: {len(flip)}/{len(pis)} pairs flipped; shared-feature max z {out['max_z_before']} -> "
             f"{out['max_z_after']} (expected, first-pass rows)")


if __name__ == "__main__":
    main()
