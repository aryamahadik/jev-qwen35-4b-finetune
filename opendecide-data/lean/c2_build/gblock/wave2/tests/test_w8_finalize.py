"""Tests: W8 finalize seeded cap (builders/w8_finalize.py). CPU only, in memory (no test writes a file). Run from lean/:
  ../.venv/bin/python -I -m pytest -q -p no:cacheprovider c2_build/gblock/wave2/tests/test_w8_finalize.py
"""
from __future__ import annotations

import random
from collections import Counter

from builders import w8_finalize as F


def pool_of(counts: dict, seed: int = 1) -> list:
    rng = random.Random(seed)
    rows, i = [], 0
    for label, n in counts.items():
        for _ in range(n):
            i += 1
            rows.append({"id": f"c2_wave2:W8:x:{i:05d}", "source": "haiku" if rng.random() < 0.9 else "opus",
                         "gold": label})
    return rows


def test_under_cap_is_identity():
    pool = pool_of({"a": 30, "b": 20})
    out = F.seeded_cap(pool, 1200)
    assert [p["id"] for p in out] == sorted(p["id"] for p in pool)


def test_cap_is_exact_and_unique():
    pool = pool_of({"a": 700, "b": 500, "c": 300, "d": 128})
    out = F.seeded_cap(pool, 1200)
    assert len(out) == 1200
    assert len({p["id"] for p in out}) == 1200
    assert set(p["id"] for p in out) <= set(p["id"] for p in pool)


def test_cap_is_uniform_within_label():
    counts = {"a": 700, "b": 500, "c": 300, "d": 128}
    pool = pool_of(counts)
    out = F.seeded_cap(pool, 1200)
    kept = Counter(p["gold"] for p in out)
    frac = 1200 / sum(counts.values())
    for label, n in counts.items():
        # every label keeps the same fraction, up to one row of largest-remainder rounding
        assert abs(kept[label] - n * frac) <= 1.0, (label, kept[label], n * frac)


def test_cap_keeps_every_label():
    pool = pool_of({"big": 900, "tiny": 4, "mid": 300})
    out = F.seeded_cap(pool, 1200 - 800)
    assert set(Counter(p["gold"] for p in out)) == {"big", "tiny", "mid"}


def test_cap_is_deterministic_and_seeded():
    pool = pool_of({"a": 700, "b": 500, "c": 300, "d": 128})
    first = [p["id"] for p in F.seeded_cap(pool, 1200)]
    again = [p["id"] for p in F.seeded_cap(list(reversed(pool)), 1200)]
    assert first == again
