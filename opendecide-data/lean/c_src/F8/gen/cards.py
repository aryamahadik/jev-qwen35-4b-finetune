"""F8 card plan and card construction (G0 spec 0 card-size plan, 1 label schemas, 3.1 card versions, 10.1 diversity).

A card is one 2.1 task card: (F8, sampler, pack, label schema, instruction family). One pack per card (XF09), one label
schema per card (F8-R2-C1). Rules (scorecard, cut table, limits, overrides, bins, matrix, action rules, INV rule) are
card content; case data are row content. SEM lines are fixed per card version (F8-R1-09).
"""
from __future__ import annotations

import json
import re
from fractions import Fraction as Fr

import packs_f8
from common import FMT2, rng_for

# ------------------------------------------------------------------------------------------------ card plan (r1)
# (schema, sub) -> per sampler counts; sizes per (schema, sub) as (large, small)
ALLOC = {
    "S1": [("yn", "points", 3), ("yn", "bayes", 2), ("yn", "expected", 4), ("yn", "rank", 1), ("bin", "bayes", 1),
           ("tier", "points", 1), ("mat", "rank", 1), ("rank_top", "rank", 1), ("dec", "expected", 2),
           ("pred", "bayes", 3), ("inv", "points", 1), ("inv", "expected", 1)],
    "S2": [("yn", "points", 3), ("yn", "bayes", 3), ("yn", "expected", 4), ("yn", "rank", 1), ("bin", "bayes", 2),
           ("tier", "points", 3), ("mat", "rank", 2), ("rank_top", "rank", 2), ("dec", "expected", 1)],
    "S3": [("bin", "bayes", 4), ("rank_order", "rank", 5), ("inv", "expected", 3), ("inv", "rank", 2),
           ("inv", "points", 1), ("yn", "bayes", 3), ("yn", "expected", 2), ("pred", "bayes", 1)],
    "S4": [("yn", "points", 5), ("yn", "bayes", 2), ("yn", "expected", 3), ("yn", "rank", 1), ("bin", "bayes", 1),
           ("tier", "points", 2), ("rank_top", "rank", 1), ("dec", "expected", 2), ("pred", "bayes", 2),
           ("inv", "expected", 1), ("inv", "points", 1)],
}
SIZES = {("yn", "points"): (8, 3), ("yn", "bayes"): (6, 4), ("yn", "expected"): (9, 4), ("yn", "rank"): (1, 2),
         ("bin", "bayes"): (4, 4), ("tier", "points"): (3, 3), ("mat", "rank"): (1, 2), ("rank_top", "rank"): (1, 3),
         ("rank_order", "rank"): (2, 3), ("dec", "expected"): (2, 3), ("pred", "bayes"): (2, 4),
         ("inv", "points"): (1, 2), ("inv", "expected"): (2, 3), ("inv", "rank"): (1, 1)}
LARGE_SEL, SMALL_SEL = 42, 12          # selected rows per card (plan; 0 card-size plan)
CANDIDATE_TOTAL = 3375                 # 1.5 x 2,250 (r1 F8 rows, C_DATA_SPEC 2.2)
SAMPLER_CONTAINERS = {
    "S1": ["prose", "memo", "email_thread", "bullet_sop"],
    "S2": ["form", "json", "yaml", "memo", "html_snippet"],
    "S3": ["markdown_table", "html_snippet", "json", "yaml", "memo", "key_value", "csv"],
    "S4": ["prose", "memo", "email_thread"],
    "S5": ["prose", "memo", "json", "yaml", "markdown_table", "html_snippet", "bullet_sop"],
}


# ------------------------------------------------------------------------------------------------ wordings
def wordings() -> list:
    out = []
    with open(FMT2 / "wordings" / "family_pools.jsonl", encoding="utf-8") as f:
        for line in f:
            w = json.loads(line)
            if w.get("family") == "F8":
                out.append(w)
    return out


_W_CONCEPT = {"points": re.compile(r"points|tier|scor|tally", re.I),
              "chance": re.compile(r"chance|probab|odds|base rate", re.I)}


def wording_ok(w: dict, qtype: str, concepts: set) -> bool:
    forms = w["forms"]
    if "any" not in forms and ((qtype == "noul" and "yn" not in forms) or (qtype == "choice" and "choice" not in forms)):
        return False
    hit = {c for c, rx in _W_CONCEPT.items() if rx.search(w["text"])}
    return not hit or bool(hit & concepts) or hit == {"points", "chance"}


# ------------------------------------------------------------------------------------------------ conditions
CMP_OPS = [">", ">=", "<", "<="]


def cmp_word(rng, op: str) -> str:
    import lexicon as L
    return rng.choice([w["w"] for w in L.COMPARATORS[op]])


def _money_grid(rng, lo=200, hi=20000, step=50):
    return Fr(rng.randrange(lo // step, hi // step + 1) * step)


def make_part(rng, pack: dict, kinds: list, used: set, amt_vals: dict | None = None):
    for _ in range(50):
        kind = rng.choice(kinds)
        if kind == "bool" and pack["factors"]:
            f = rng.choice(pack["factors"])["label"]
            if ("bool", f) in used:
                continue
            used.add(("bool", f))
            return {"t": "bool", "f": f}
        if kind == "cat" and pack["cats"]:
            c = rng.choice(pack["cats"])
            if ("cat", c["name"]) in used:
                continue
            used.add(("cat", c["name"]))
            return {"t": "cat", "name": c["name"], "v": rng.choice(c["values"])}
        if kind == "amt" and pack["amounts"]:
            a = rng.choice(pack["amounts"])["name"]
            if ("amt", a) in used:
                continue
            used.add(("amt", a))
            op = rng.choice(CMP_OPS)
            return {"t": "amt", "name": a, "op": op, "v": _money_grid(rng), "w": cmp_word(rng, op)}
    f = rng.choice(pack["factors"])["label"]
    return {"t": "bool", "f": f}


def make_cond(rng, pack, *, kinds=("bool", "bool", "bool", "cat", "amt"), nparts=None, conns=("and", "or"),
              xor_ok=False, used=None):
    used = set() if used is None else used
    n = nparts or rng.choices([1, 2, 3], [60, 30, 10])[0]
    kinds = [k for k in kinds if (k != "cat" or pack["cats"]) and (k != "amt" or pack["amounts"])] or ["bool"]
    parts = []
    for _ in range(n):
        p = make_part(rng, pack, kinds, used)
        if p not in parts:
            parts.append(p)
    if len(parts) == 1:
        return {"conn": "and", "parts": parts}
    conn = rng.choice(list(conns) + (["xor1"] if xor_ok else []))
    return {"conn": conn, "parts": parts}


# ------------------------------------------------------------------------------------------------ rule builders
def make_scorecard(rng, pack, *, n_lines=None, allow_neg=True):
    labels = [f["label"] for f in pack["factors"]]
    n = n_lines or rng.randint(4, min(8, max(4, len(labels) + 2)))
    lines = []
    used_conds = set()
    for i in range(n):
        for _ in range(30):
            nparts = rng.choices([1, 2, 3], [62, 30, 8])[0]
            c = make_cond(rng, pack, nparts=nparts, xor_ok=(nparts >= 2 and rng.random() < 0.18))
            key = json.dumps(c, sort_keys=True, default=str)
            if key not in used_conds:
                used_conds.add(key)
                break
        pts = rng.randint(1, 6)
        if allow_neg and rng.random() < 0.18:
            pts = -pts
        ln = {"cond": c, "pts": pts}
        if rng.random() < 0.28:
            u = make_cond(rng, pack, nparts=1, kinds=("bool", "bool", "cat"),
                          used={("bool", p["f"]) for p in c["parts"] if p["t"] == "bool"})
            ln["unless"] = u
        lines.append(ln)
    pos = sum(l["pts"] for l in lines if l["pts"] > 0)
    F = 0 if rng.random() < 0.75 else rng.randint(1, 2)
    M = max(F + 6, min(pos, rng.randint(max(F + 6, pos // 2 + 2), max(F + 7, pos))))
    return {"lines": lines, "F": F, "M": M}


def make_cut_table(rng, sc, K):
    F, M = sc["F"], sc["M"]
    # cuts c2..cK with F < c2 < ... < cK <= M  (every tier reachable, F8-AMB-45)
    span = list(range(F + 1, M + 1))
    if len(span) < K - 1:
        raise ValueError("score range too small for K tiers")
    cuts = sorted(rng.sample(span, K - 1))
    return cuts


def tier_names(rng, pack, K, form):
    pool = [t for t in pack["tiers"] if len(t) >= K]
    if pool:
        base = rng.choice(pool)
        idx = sorted(rng.sample(range(len(base)), K))
        names = [base[i] for i in idx]
    else:
        g = ["low", "guarded", "elevated", "high", "severe", "critical"]
        idx = sorted(rng.sample(range(len(g)), K))
        names = [g[i] for i in idx]
    return [n[:1].upper() + n[1:] for n in names]


# ------------------------------------------------------------------------------------------------ the card plan
def plan_cards() -> list:
    """84 cards: 21 per training sampler, 43 large + 41 small, one distinct pack per card."""
    rng = rng_for("cardplan")
    cells = []
    for s, lst in ALLOC.items():
        for schema, sub, k in lst:
            for _ in range(k):
                cells.append({"sampler": s, "schema": schema, "sub": sub})
    # sizes per (schema, sub): deterministic assignment spread over samplers
    by = {}
    for c in cells:
        by.setdefault((c["schema"], c["sub"]), []).append(c)
    target = {"S1": 550, "S2": 625, "S3": 550, "S4": 525}     # rows per sampler (0, r1)
    best, best_err = None, None
    for trial in range(3000):
        assign = {}
        for key, lst in sorted(by.items()):
            L, S = SIZES[key]
            if L + S != len(lst):
                raise ValueError(f"size plan mismatch {key}: {L}+{S} vs {len(lst)}")
            order = sorted(range(len(lst)), key=lambda i: rng.random())
            for j, i in enumerate(order):
                assign[id(lst[i])] = "large" if j < L else "small"
        tot = {s: 0 for s in target}
        for c in cells:
            tot[c["sampler"]] += LARGE_SEL if assign[id(c)] == "large" else SMALL_SEL
        err = sum(abs(tot[s] - target[s]) for s in target)
        if best_err is None or err < best_err:
            best, best_err = assign, err
    for c in cells:
        c["size"] = best[id(c)]
    packs = [p for p in packs_f8.load() if p["split"] == "train" and all(p["usable"].values())]
    packs = sorted(packs, key=lambda p: p["pid"])
    rng.shuffle(packs)
    if len(packs) < len(cells):
        raise ValueError("not enough packs")
    for i, c in enumerate(cells):
        c["card_id"] = f"F8-C{i + 1:03d}"
        c["pack"] = packs[i]["pid"]
    nL = sum(c["size"] == "large" for c in cells)
    tot_sel = nL * LARGE_SEL + (len(cells) - nL) * SMALL_SEL
    # candidate rows per card (1.5x of the selected plan, scaled to exactly CANDIDATE_TOTAL)
    raw = [(LARGE_SEL if c["size"] == "large" else SMALL_SEL) * CANDIDATE_TOTAL / tot_sel for c in cells]
    base = [int(x) for x in raw]
    rem = CANDIDATE_TOTAL - sum(base)
    order = sorted(range(len(cells)), key=lambda i: -(raw[i] - base[i]))
    for i in order[:rem]:
        base[i] += 1
    for c, n in zip(cells, base):
        c["n_cand"] = n
    # option-count class per card (1 option-count plan): alternate small / large level counts within each schema
    seen = {}
    for c in sorted(cells, key=lambda c: c["card_id"]):
        k = seen.get(c["schema"], 0)
        c["kc"] = k % 2
        seen[c["schema"]] = k + 1
    return cells


if __name__ == "__main__":
    import collections
    cs = plan_cards()
    print(len(cs), collections.Counter(c["size"] for c in cs), sum(c["n_cand"] for c in cs))
    print(collections.Counter(c["sampler"] for c in cs))
    for s in ("S1", "S2", "S3", "S4"):
        print(s, sum(c["n_cand"] for c in cs if c["sampler"] == s))


# ------------------------------------------------------------------------------------------------ S5 (held out)
S5_CELLS = [("yn", "points"), ("yn", "bayes"), ("yn", "expected"), ("bin", "bayes"), ("tier", "points"),
            ("mat", "rank"), ("rank_top", "rank"), ("rank_order", "rank"), ("dec", "expected"), ("pred", "bayes"),
            ("inv", "expected"), ("inv", "points"), ("yn", "bayes")]
S5_TOTAL = 400


def plan_s5_cards() -> list:
    """S5 cards: the held-out probability-tree sampler on held-out packs (mix-tuning dev only, never trained)."""
    rng = rng_for("s5plan")
    packs = sorted([p for p in packs_f8.load() if p["split"] == "heldout" and all(p["usable"].values())],
                   key=lambda p: p["pid"])
    rng.shuffle(packs)
    cells = []
    for i, (sch, sub) in enumerate(S5_CELLS):
        cells.append({"sampler": "S5", "schema": sch, "sub": sub, "size": "large", "card_id": f"F8-D{i + 1:03d}",
                      "pack": packs[i % len(packs)]["pid"], "kc": i % 2})
    base = S5_TOTAL // len(cells)
    for i, c in enumerate(cells):
        c["n_cand"] = base + (1 if i < S5_TOTAL - base * len(cells) else 0)
    return cells
