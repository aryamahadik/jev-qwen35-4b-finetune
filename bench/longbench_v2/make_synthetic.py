"""SYNTHETIC LongBench-v2-shaped data for the kit's tests (random words; no real item is read or copied).

  opendecide-data/.venv/bin/python bench/longbench_v2/make_synthetic.py --out bench/longbench_v2/synthetic/data.json

Same fields as LongBench v2's data.json. 130 items so the sha256(_id) dev split (first 100) leaves a test part; about
24 contexts are long enough to need reduction (> ~104K chars), the rest fit. Edge cases: one item with two identical
options, one with a ~66K-character question (its budget drops below 8,000 and its prompts are too long for the reader,
so its chunks fail and its final read fails), one long context without any separator (hard split), one with CJK text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

WORDS = ("alpha beta gamma delta river stone ledger audit clause tenant budget invoice harbor signal vector "
         "orchid copper meadow lantern quarry summit tunnel valley willow yonder zephyr amber basil cedar dune "
         "ember fjord grove heron island jasper kelp lagoon maple nectar opal pebble quill rook sable thistle").split()


def para(rng, n_words):
    out, k = [], 0
    while k < n_words:
        m = rng.randint(6, 18)
        out.append(" ".join(rng.choice(WORDS) for _ in range(m)).capitalize() + ".")
        k += m
    return " ".join(out)


def context(rng, n_chars, kind="normal"):
    if kind == "nosep":
        return "".join(rng.choice("abcdefghij") for _ in range(n_chars))
    if kind == "cjk":
        return "\n\n".join("".join(rng.choice("数据分析报告合同条款审计") for _ in range(rng.randint(200, 900)))
                           for _ in range(max(1, n_chars // 550)))[:n_chars]
    parts, size = [], 0
    while size < n_chars:
        p = para(rng, rng.randint(40, 400))
        if rng.random() < 0.2:
            p = p.replace(". ", ".\n", 2)
        parts.append(p)
        size += len(p) + 2
    return "\n\n".join(parts)[:n_chars]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=130)
    ap.add_argument("--n-long", type=int, default=24)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--long-min", type=int, default=110_000)
    ap.add_argument("--long-max", type=int, default=170_000)
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    items = []
    for i in range(a.n):
        long_ = i < a.n_long
        n = rng.randint(a.long_min, a.long_max) if long_ else rng.randint(2_000, 9_000)
        kind = "nosep" if i == 3 else "cjk" if i == 5 else "normal"
        it = {"_id": hashlib.sha256(f"synthetic-{a.seed}-{i}".encode()).hexdigest()[:24],
              "domain": rng.choice(["Single-Document QA", "Multi-Document QA", "Code Repository Understanding"]),
              "sub_domain": rng.choice(["Synthetic A", "Synthetic B"]),
              "difficulty": rng.choice(["easy", "hard"]), "length": rng.choice(["short", "medium", "long"]),
              "question": "Synthetic question " + para(rng, rng.randint(5, 25)),
              **{f"choice_{L}": "Synthetic option " + para(rng, rng.randint(2, 12)) for L in "ABCD"},
              "answer": rng.choice("ABCD"), "context": context(rng, n, kind)}
        if i == 1:
            it["choice_C"] = it["choice_B"] + "  "  # identical after strip()
        if i == 2:
            it["question"] = "Synthetic long question " + para(rng, 11_000)[:66_000]
        items.append(it)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(items, ensure_ascii=False))
    print(json.dumps({"synthetic": str(out), "items": len(items), "long_target": a.n_long}))


if __name__ == "__main__":
    main()
