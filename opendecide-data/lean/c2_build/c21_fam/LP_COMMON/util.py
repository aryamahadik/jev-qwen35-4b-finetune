"""Deterministic helpers: every random choice comes from `rng_for(*parts)` (SHA-256 of a JSON array of the parts)."""
import hashlib
import json
import math
import random
import re

LETTERS = "ABCDEFGHIJKLMNOP"


def canon_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_obj(obj):
    return sha256_text(canon_json(obj))


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
    """Integer allocation of `total` over `weights` (key -> non-negative number): exact sum, stable order."""
    keys = list(weights)
    s = float(sum(weights.values()))
    if s <= 0:
        raise ValueError("weights sum to zero")
    raw = {k: total * weights[k] / s for k in keys}
    out = {k: int(math.floor(raw[k] + 1e-9)) for k in keys}
    rest = total - sum(out.values())
    for k in sorted(keys, key=lambda k: (-(raw[k] - out[k]), keys.index(k)))[:rest]:
        out[k] += 1
    return out


def balanced_cycle(n, k, rng):
    """n ints in range(k), each value floor(n/k) or ceil(n/k) times, shuffled."""
    base = [i % k for i in range(n)]
    rng.shuffle(base)
    return base


def place_gold(labels, gold, gold_pos, rng):
    others = [x for x in labels if x != gold]
    rng.shuffle(others)
    return others[:gold_pos] + [gold] + others[gold_pos:]


def approx_tokens(text):
    """CPU proxy for the token count (words, numbers, punctuation, newlines, indentation runs); over-counts BPE a little.
    The real Qwen tokenizer is injected by L-0 (`tokens.set_counter`)."""
    return len(re.findall(r"[A-Za-z_]+|\d+|\n| {2,}|[^\sA-Za-z_0-9]", text))


def shares(counter, total=None):
    total = total if total is not None else sum(counter.values())
    return {k: (v / total if total else 0.0) for k, v in counter.items()}


def tokens_estimate(text):
    return approx_tokens(text)


def opaque_id(row_id):
    """Opaque stand-in for a row id in a SOLVER B view. Row ids carry the group id and a member letter ("-a" is the YES / first member of a pair in
    several families, block ids name all-ALLOW or all-BLOCK blocks), so the real id must never reach B: a label can be read off it."""
    return "b-" + sha256_text("od-solver-b-view|" + str(row_id))[:16]
