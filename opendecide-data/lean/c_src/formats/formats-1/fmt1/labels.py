"""Masked and swapped label names (spec 2.1; rules in data/label_rules.jsonl, LR01-LR13).

Every function is deterministic in its seed key and never reads gold: the name map is drawn per card (or per row for
row-level renders) from ids only.
"""
from __future__ import annotations

import hashlib
import random
import re

from . import pool
from .render import FormatError

DEFAULT_RATES = {"masked": 0.12, "swapped": 0.05}
F10_RATES = {"masked": 0.40, "swapped": 0.30}


def _rng(*key: str) -> random.Random:
    return random.Random(int(hashlib.sha256("\x1f".join(key).encode()).hexdigest()[:16], 16))


def label_form(family: str, card_id: str, row_key: str, rates: dict | None = None) -> str:
    """'masked', 'swapped' or 'plain' from ids only (LR03). Rates: DEFAULT_RATES, or F10_RATES for F10."""
    r = rates or DEFAULT_RATES
    if r["masked"] + r["swapped"] > 1:
        raise ValueError("rates add up above 1")
    u = pool.unit_hash("label_form", family, card_id, row_key)
    if u < r["masked"]:
        return "masked"
    if u < r["masked"] + r["swapped"]:
        return "swapped"
    return "plain"


# ----------------------------------------------------------------------------------------------------------------------
# masked IDs

def _draw_id(pattern: str, rng: random.Random, letters: str, digits: str) -> str:
    return re.sub(r"\{([LD])\}", lambda m: rng.choice(letters if m.group(1) == "L" else digits), pattern)


def _core(pattern: str, s: str) -> str:
    """The variable part of an ID (prefix words and fixed punctuation removed), for the distance check."""
    fixed = re.split(r"\{[LD]\}", pattern)
    core = s
    for f in fixed:
        if f:
            core = core.replace(f, "", 1)
    return core


def _dist(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b))


def masked_ids(scheme_id: str, n: int, seed_key: str) -> list[str]:
    """n distinct neutral IDs in one scheme (LR04, LR05). Pairwise distance >= 2 when the scheme allows it; for
    n >= 3 the list is never in ascending or descending order."""
    sch = pool.mask_scheme(scheme_id)
    pat, L, D = sch["pattern"], sch["letters"], sch["digits"]
    n_slots = len(re.findall(r"\{[LD]\}", pat))
    cap = 1
    for m in re.findall(r"\{([LD])\}", pat):
        cap *= len(L) if m == "L" else len(D)
    if n < 1 or n > cap:
        raise FormatError(f"scheme {scheme_id} cannot give {n} IDs")
    rng = _rng("masked_ids", scheme_id, str(n), seed_key)
    for attempt in range(50):
        out, cores = [], []
        want_far = n_slots >= 2
        tries = 0
        while len(out) < n and tries < 20000:
            tries += 1
            s = _draw_id(pat, rng, L, D)
            c = _core(pat, s)
            if s in out:
                continue
            if want_far and tries < 4000 and any(_dist(c, x) < 2 for x in cores):
                continue
            out.append(s)
            cores.append(c)
        if len(out) < n:
            continue
        if n >= 3 and (out == sorted(out) or out == sorted(out, reverse=True)):
            rng.shuffle(out)
            if out == sorted(out) or out == sorted(out, reverse=True):
                continue
        return out
    raise FormatError("could not draw IDs")


# ----------------------------------------------------------------------------------------------------------------------
# swapped names

def _spearman(a: list[float], b: list[float]) -> float:
    def ranks(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return 0.0 if den == 0 else num / den


def monotone_ok(word_ranks: list[int], order: list[int]) -> bool:
    """LR08: words from an ordered group must not follow the card's label order."""
    n = len(order)
    if n <= 2:
        return False
    if n == 3:
        pairs = sorted(zip(order, word_ranks))
        rk = [r for _, r in pairs]
        return not (rk[0] <= rk[1] <= rk[2] or rk[0] >= rk[1] >= rk[2])
    return abs(_spearman([float(r) for r in word_ranks], [float(o) for o in order])) < 0.5


def _prefix_clash(words: list[str], exclude: list[str]) -> bool:
    lw = [w.lower() for w in words]
    ex = [e.lower() for e in exclude]
    for i, w in enumerate(lw):
        for j, x in enumerate(lw):
            if i < j and (w[:4] == x[:4] or w in x or x in w):
                return True
        for x in ex:
            for tok in re.findall(r"[a-z]+", x):
                if w == tok or (len(tok) >= 4 and w[:4] == tok[:4]):
                    return True
    return False


def swapped_names(mode: str, n: int, seed_key: str, *, natural_names: list[str] | None = None,
                  order: list[int] | None = None, groups: list[str] | None = None, exclude: list[str] = (),
                  capitalize: bool = True) -> list[str]:
    """Names for a swapped render (LR07-LR09).
    mode 'perm': a derangement of natural_names (each label gets another label's natural name).
    mode 'group': n words from one group; mode 'mixed': n words from 2 or more groups.
    order: the labels' scale positions (0..n-1) when the labels are ordered; ordered groups then must not follow it.
    exclude: every other name, term and code on the card (no shared word or 4-letter prefix)."""
    rng = _rng("swapped", mode, str(n), seed_key)
    if mode == "perm":
        if not natural_names or len(natural_names) != n or n < 2:
            raise FormatError("perm mode needs the card's n >= 2 natural names")
        idx = list(range(n))
        for _ in range(1000):
            rng.shuffle(idx)
            if all(i != k for k, i in enumerate(idx)):
                return [natural_names[i] for i in idx]
        raise FormatError("no derangement found")
    words = pool.swap_words()
    by_g: dict[str, list[dict]] = {}
    for w in words:
        if groups is None or w["group"] in groups:
            by_g.setdefault(w["group"], []).append(w)
    names = sorted(by_g)
    excl = list(exclude) + list(natural_names or [])
    for _ in range(4000):
        if mode == "group":
            g = rng.choice(names)
            if len(by_g[g]) < n:
                continue
            pick = rng.sample(by_g[g], n)
        elif mode == "mixed":
            gs = rng.sample(names, min(len(names), max(2, min(n, 4))))
            pool_w = [w for g in gs for w in by_g[g]]
            if len(pool_w) < n:
                continue
            pick = rng.sample(pool_w, n)
            if len({w["group"] for w in pick}) < 2:
                continue
        else:
            raise FormatError(f"unknown swap mode {mode}")
        ws = [w["word"] for w in pick]
        if _prefix_clash(ws, excl):
            continue
        if natural_names and any(w.lower() == x.lower() for w, x in zip(ws, natural_names)):
            continue
        if order is not None:
            ordered = [w for w in pick if w["ordered"]]
            if len({w["group"] for w in ordered}) == 1 and len(ordered) == n:
                if not monotone_ok([w["rank"] for w in pick], list(order)):
                    continue
        return [w.capitalize() if capitalize else w for w in ws]
    raise FormatError("could not draw swapped names under the constraints")
