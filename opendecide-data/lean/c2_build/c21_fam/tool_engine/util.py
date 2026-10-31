"""Shared helpers for the L-T tool-scenario engine (C2.1; code only, no rows).

Deterministic: every random choice comes from `rng_for(*parts)`, a random.Random seeded from SHA-256 of a JSON
array of the parts, so the same (family, seed, key...) always gives the same stream on every machine.
"""
import hashlib
import json
import math
import random

LETTERS = "ABCDEFGHIJKLMNOP"


def canon_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rng_for(*parts):
    digest = hashlib.sha256(json.dumps([str(p) for p in parts], ensure_ascii=True).encode("ascii")).digest()
    return random.Random(int.from_bytes(digest[:16], "big"))


def largest_remainder(total, weights):
    """Integer allocation of `total` over `weights` (dict key -> non-negative number), exact sum, stable order."""
    keys = list(weights)
    s = float(sum(weights.values()))
    if s <= 0:
        raise ValueError("weights sum to zero")
    raw = {k: total * weights[k] / s for k in keys}
    out = {k: int(math.floor(raw[k] + 1e-9)) for k in keys}
    rest = total - sum(out.values())
    order = sorted(keys, key=lambda k: (-(raw[k] - out[k]), keys.index(k)))
    for k in order[:rest]:
        out[k] += 1
    return out


def balanced_cycle(n, k, rng):
    """n ints in range(k), each value appearing floor(n/k) or ceil(n/k) times, in random order."""
    base = [i % k for i in range(n)]
    rng.shuffle(base)
    return base


def place_gold(labels, gold, gold_pos, rng):
    """Return the option order (list of labels) with `gold` at index gold_pos and the others shuffled."""
    others = [x for x in labels if x != gold]
    rng.shuffle(others)
    order = others[:gold_pos] + [gold] + others[gold_pos:]
    return order


def non_identity_permutation(n, rng):
    if n < 2:
        raise ValueError("need at least 2 options")
    ident = list(range(n))
    while True:
        p = ident[:]
        rng.shuffle(p)
        if p != ident:
            return p


def shares(counter, total=None):
    total = total if total is not None else sum(counter.values())
    return {k: (v / total if total else 0.0) for k, v in counter.items()}


def tv_distance(p, q):
    """Total-variation distance between two dict distributions (each normalised here)."""
    keys = set(p) | set(q)
    sp, sq = float(sum(p.values())) or 1.0, float(sum(q.values())) or 1.0
    return 0.5 * sum(abs(p.get(k, 0) / sp - q.get(k, 0) / sq) for k in keys)


def approx_tokens(text):
    """CPU proxy for a token count (words and punctuation x 1.3). The real count comes from L-0's token histogram
    program, injected into gates as `token_fn`; this proxy exists only so unit tests and the dry run have a number."""
    import re
    return int(math.ceil(len(re.findall(r"\w+|[^\w\s]", text)) * 1.3))
