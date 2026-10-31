"""Option-shortcut heuristics (G-S2 panel). Shared by the gate (gates.py) and by the builder's anti-shortcut filter.
Pure functions of (option texts, stem text). No training, no model."""
import datetime as dt
import re

import numpy as np

_NUM = re.compile(r"-?\d+(?:\.\d+)?")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_DUR = re.compile(r"(\d+) days? (\d+) hours? (\d+) minutes?|(\d+) hours? (\d+) minutes?|(\d+) minutes?")

NUMERIC_HEURISTICS = ("median_value", "largest", "smallest", "closest_to_mean", "farthest_from_mean", "nearest_stem_number",
                      "sum_or_difference_of_two_others")
STRING_HEURISTICS = ("most_shared_digits", "longest_string", "shortest_string", "most_shared_tokens")


def option_value(text):
    t = text.strip()
    if _DATE.fullmatch(t):
        return float(dt.date.fromisoformat(t).toordinal())
    m = _DUR.fullmatch(t)
    if m:
        g = m.groups()
        if g[0] is not None:
            return int(g[0]) * 1440 + int(g[1]) * 60 + int(g[2])
        if g[3] is not None:
            return int(g[3]) * 60 + int(g[4])
        return int(g[5])
    ns = _NUM.findall(t)
    if len(ns) == 1:
        return float(ns[0])
    return None


def option_values(options):
    vals = [option_value(o) for o in options]
    return vals if all(v is not None for v in vals) else None


def stem_numbers(stem):
    return [float(x) for x in _NUM.findall(stem)]


def _arg(vals, fn):
    """Index of the unique max / min of vals; None on a tie (a tied heuristic abstains)."""
    best = fn(vals)
    idx = [i for i, v in enumerate(vals) if v == best]
    return idx[0] if len(idx) == 1 else None


def predictions(options, stem):
    """{heuristic name: predicted option index}; heuristics that do not apply, or that tie, are absent."""
    out = {}

    def put(name, i):
        if i is not None:
            out[name] = i
    vals = option_values(options)
    if vals is not None:
        med = float(np.median(vals))
        mean = float(np.mean(vals))
        put("median_value", _arg([-abs(v - med) for v in vals], max))
        put("largest", _arg(vals, max))
        put("smallest", _arg(vals, min))
        put("closest_to_mean", _arg([-abs(v - mean) for v in vals], max))
        put("farthest_from_mean", _arg([abs(v - mean) for v in vals], max))
        sn = stem_numbers(stem)
        if sn:
            put("nearest_stem_number", _arg([-min(abs(v - s) for s in sn) for v in vals], max))
        hits = []
        for i, v in enumerate(vals):
            others = [vals[j] for j in range(len(vals)) if j != i]
            for a in range(len(others)):
                for b in range(a + 1, len(others)):
                    if abs(v - (others[a] + others[b])) < 1e-9 or abs(v - abs(others[a] - others[b])) < 1e-9:
                        hits.append(i)
        if len(set(hits)) == 1:
            out["sum_or_difference_of_two_others"] = hits[0]
    ds = [set(ch for ch in t if ch.isdigit()) for t in options]
    put("most_shared_digits", _arg([sum(len(ds[i] & ds[j]) for j in range(len(options)) if j != i) for i in range(len(options))], max))
    put("longest_string", _arg([len(t) for t in options], max))
    put("shortest_string", _arg([len(t) for t in options], min))
    toks = [set(t.lower().replace(",", " ").split()) for t in options]
    put("most_shared_tokens", _arg([sum(len(toks[i] & toks[j]) for j in range(len(options)) if j != i) for i in range(len(options))], max))
    return out


def hits_on(options, correct_idx, stem):
    """How many applicable heuristics pick the correct option, and how many apply."""
    p = predictions(options, stem)
    return sum(1 for v in p.values() if v == correct_idx), len(p)


# ------------------------------------------------------------------------------------------------
# Option features for the option-only shortcut probe (gate G-S1) AND for the builder's adversarial filter (adversary.py).
# One function, so what the gate can see is exactly what the builder screens against. Skeptic addition 18 Oct: the first version of the
# feature set (rank, distance from median / mean, shared digits) missed the structure that makes near-miss distractors give the answer
# away: the distractors sit at fixed offsets from the correct value (same residue mod 7 / 60 / 1,440, one day off, a neighbour on the number
# line), so the correct option is the one with the most neighbours.
# ------------------------------------------------------------------------------------------------
RESIDUE_MODS = (2, 3, 5, 7, 10, 60, 100, 1440)


def _scaled_int(v):
    return int(round(v * 100)) if abs(v - round(v)) > 1e-9 else int(round(v))


def option_features(options, stem):
    """-> list (one per option) of equal-length float lists. Pure function of the option texts and the stem."""
    n = len(options)
    texts = [t.strip() for t in options]
    ds = [set(ch for ch in t if ch.isdigit()) for t in texts]
    toks = [set(t.lower().replace(",", " ").split()) for t in texts]
    lens = [len(t) for t in texts]
    vals = option_values(options)
    sn = stem_numbers(stem)
    order = sorted(range(n), key=lambda i: texts[i])
    lex_rank = {i: r for r, i in enumerate(order)}
    out = []
    if vals is not None:
        lo, hi = min(vals), max(vals)
        rng = (hi - lo) or 1.0
        srt = sorted(vals)
        med = float(np.median(vals))
        mean = float(np.mean(vals))
        ints = [_scaled_int(v) for v in vals]
        dps = [(len(t.split(".")[1].split()[0]) if "." in t and t.split(".")[1][:1].isdigit() else 0) for t in texts]
    for i, t in enumerate(texts):
        f = [lens[i], len(t.split()), sum(ch.isdigit() for ch in t), int(lens[i] == max(lens)), int(lens[i] == min(lens)),
             sum(len(ds[i] & ds[j]) for j in range(n) if j != i), sum(len(toks[i] & toks[j]) for j in range(n) if j != i),
             lex_rank[i], sum(1 for j in range(n) if j != i and t.split()[:1] == texts[j].split()[:1]),
             sum(1 for j in range(n) if j != i and t[-1:] == texts[j][-1:])]
        if vals is not None:
            v = vals[i]
            others = [vals[j] for j in range(n) if j != i]
            gaps = sorted(abs(v - o) for o in others)
            below = [v - o for o in others if o < v]
            above = [o - v for o in others if o > v]
            f += [srt.index(v), abs(v - med) / rng, abs(v - mean) / rng, int(v == hi), int(v == lo), (v - lo) / rng,
                  gaps[0] / rng, gaps[1] / rng, (min(below) / rng if below else 1.0), (min(above) / rng if above else 1.0),
                  sum(1 for g in gaps if g <= 1.0), sum(1 for g in gaps if g <= 0.15 * rng)]
            for m in RESIDUE_MODS:
                f.append(sum(1 for j in range(n) if j != i and ints[j] % m == ints[i] % m))
            f += [sum(1 for j in range(n) if j != i and dps[j] == dps[i]), int(any(abs(v - s) < 1e-9 for s in sn)),
                  (min(abs(v - s) for s in sn) / rng) if sn else 1.0]
            f.append(int(any(abs(v - (a + b)) < 1e-9 or abs(v - abs(a - b)) < 1e-9 for ai, a in enumerate(others) for b in others[ai + 1:])))
        else:
            f += [0.0] * (12 + len(RESIDUE_MODS) + 4)
        out.append(f)
    return out
