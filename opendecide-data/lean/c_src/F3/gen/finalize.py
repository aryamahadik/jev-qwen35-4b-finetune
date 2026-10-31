"""Finalise one output part: run the sealed checker on it, drop every row with a blocking hit (a hit base row takes
its twins with it; relations follow), generate replacement rows for the same cards with a fresh seed (ids carry an
'r<k>.' prefix), sealed-check the replacements, merge, and repeat until no hit is left.

  python finalize.py --part candidates|qc|dev-raw
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys

import build as BLD
import cardfit
import cards as CARDS
import sealed
from f3common import OUT, TMP, log_progress

FILES = {"candidates": OUT / "candidates_r1.jsonl", "qc": OUT / "qc_sample.jsonl", "dev-raw": TMP / "dev_raw.jsonl"}


def _load(p):
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


def _write(p, objs):
    with open(p, "w", encoding="utf-8") as f:
        for o in objs:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True, choices=list(FILES))
    ap.add_argument("--max-rounds", type=int, default=4)
    ap.add_argument("--min-rows", type=int, default=0, help="top up to at least this many rows (fresh seed, 't1.' ids)")
    a = ap.parse_args()
    path = str(FILES[a.part])
    base = path[:-6]
    rows, side, rels = _load(path), _load(base + ".sidecar.jsonl"), _load(base + ".relations.jsonl")
    purpose = "dev" if a.part == "dev-raw" else a.part
    cards = CARDS.make_dev_cards() if purpose == "dev" else CARDS.make_training_cards()
    cardfit.fit(cards, BLD.tokenizer())
    by_id = {c["card_id"]: c for c in cards}
    n_rows = BLD.plan_rows(cards, purpose, 1.0)
    probs = BLD.qt_probs(cards, n_rows)
    BLD.GIT_SHA = BLD.git_sha()
    report = {"rounds": []}
    if a.min_rows and len(rows) < a.min_rows:
        # top-up: spread the shortfall over cards with headroom under the 128 cap (124 with unit margin)
        have = collections.Counter(r["meta"]["card_id"] for r in rows)
        need = a.min_rows - len(rows) + 30
        # cards that met their planned size generate reliably; take those with the most headroom first
        order = sorted([c for c in cards if have[c["card_id"]] >= n_rows[c["card_id"]]] or cards,
                       key=lambda c: have[c["card_id"]])
        add = collections.Counter()
        # repair r2.2 (G11 on the pool: max 128 rows per card, <= 2,500 rows per sampler): a card is topped up only
        # while it stays <= 120 before its last unit, and a sampler only while it stays <= 2,450
        samp = collections.Counter(r["meta"]["sampler"] for r in rows)
        i = 0
        while need > 0 and i < 10000:
            c = order[i % len(order)]
            if have[c["card_id"]] + add[c["card_id"]] + 5 <= 120 and samp[c["sampler"]] + 5 <= 2450:
                add[c["card_id"]] += 5
                samp[c["sampler"]] += 5
                need -= 5
            i += 1
        pre = {"candidates": "c1", "qc": "q1", "dev": "d1"}[purpose]
        for cid, k in add.items():
            g = BLD.Gen(by_id[cid], purpose, k, probs[cid], f"{purpose}-top", parser=True, id_prefix=f"t1.{pre}.")
            g.run()
            for r in g.rows:
                r.pop("_info", None)
            rows += g.rows
            side += g.side
            rels += g.rels
        report["topup"] = {"added_rows": sum(1 for r in rows if r["id"].startswith("t1.")), "cards": len(add)}
        log_progress(f"finalize {a.part}: top-up added {report['topup']['added_rows']} rows over "
                     f"{len(add)} cards (fresh seed)")
    for rnd in range(1, a.max_rounds + 1):
        _write(path, rows)
        hits, summ = sealed.run(path)
        report["rounds"].append({"round": rnd, "rows": len(rows), "blocking_hits": len(hits)})
        log_progress(f"sealed_check {a.part} round {rnd}: {len(rows)} rows, {len(hits)} with a blocking hit")
        if not hits:
            break
        hit = set(hits)
        drop = set(hit) | {r["id"] for r in rows if r["meta"]["twin_of"] in hit}
        lost = collections.Counter(r["meta"]["card_id"] for r in rows if r["id"] in drop)
        rows = [r for r in rows if r["id"] not in drop]
        side = [s for s in side if s["id"] not in drop]
        rels = [x for x in rels if x["a"] not in drop and x["b"] not in drop]
        # replacements: same cards, fresh seed, distinct id prefix
        new_rows, new_side, new_rels = [], [], []
        for cid, k in lost.items():
            g = BLD.Gen(by_id[cid], purpose, k, probs[cid], f"{purpose}-repl{rnd}", parser=True,
                        id_prefix=f"r{rnd}.{ {'candidates': 'c1', 'qc': 'q1', 'dev': 'd1'}[purpose]}.")
            g.run()
            for r in g.rows:
                r.pop("_info", None)
            new_rows += g.rows
            new_side += g.side
            new_rels += g.rels
        rows += new_rows
        side += new_side
        rels += new_rels
    _write(path, rows)
    _write(base + ".sidecar.jsonl", side)
    _write(base + ".relations.jsonl", rels)
    hits, summ = sealed.run(path)
    report["final"] = {"rows": len(rows), "blocking_hits": len(hits)}
    with open(base + ".finalize.json", "w") as f:
        json.dump(report, f, indent=1)
    log_progress(f"finalize {a.part}: {len(rows)} rows, sealed blocking hits {len(hits)}")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
