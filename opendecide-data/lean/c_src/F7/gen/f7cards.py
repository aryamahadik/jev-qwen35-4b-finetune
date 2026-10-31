"""F7 card samplers: the family-level card plan (2.1 / 6 / 7 quotas) and card construction per sampler (section 8).

S1 forward random points (ladder 60%, highest 40%), S2 label-first boundaries (ladder 50%, highest 25%, ladder +
override 25%), S3 scoring sheets (count 50%, points 50%), S4 narratives (ladder 50%, highest 25%, count 25%), S6
cut-point rubrics, S5 grid (held-out packs, mix-tuning dev only).
"""
from __future__ import annotations

import collections
import hashlib
import itertools
import math
import random
from fractions import Fraction

import f7model as M
from f7lex import LEVEL_NAMES, LEVEL_WORDS, MASK_SCHEMES, SCALE_Q

SAMPLERS_TRAIN = ["S1", "S2", "S3", "S4", "S6"]
CONTAINERS = {
    "S1": ["key_value", "bullet_sop", "memo", "form", "json", "yaml", "markdown_table", "html_snippet"],
    "S2": ["key_value", "bullet_sop", "markdown_table", "memo", "form", "csv", "html_snippet"],
    "S3": ["form", "markdown_table", "json", "yaml", "csv", "html_snippet", "key_value"],
    "S4": ["prose", "memo", "email_thread", "bullet_sop"],
    "S6": ["key_value", "prose", "memo", "json", "yaml", "form", "markdown_table"],
    "S5": ["prose", "memo", "key_value", "json", "yaml", "form", "markdown_table", "html_snippet", "csv",
           "bullet_sop", "email_thread"],
}
OPEN_TOP = 10 ** 6
STRUCTURED = {"key_value","form", "json", "yaml", "csv", "markdown_table", "html_snippet"}
SENTENCE_OK = {"memo", "bullet_sop", "form", "json", "yaml", "markdown_table", "html_snippet", "prose", "email_thread"}


def rng_for(*key) -> random.Random:
    return random.Random(int(hashlib.sha256("\x1f".join(map(str, key)).encode()).hexdigest()[:16], 16))


def _spread(n: int, shares: list[tuple], rng: random.Random) -> list:
    """n labels drawn by largest remainder from (label, share) pairs, shuffled."""
    raw = [(lab, n * s) for lab, s in shares]
    out = []
    base = [int(x) for _, x in raw]
    rem = n - sum(base)
    order = sorted(range(len(raw)), key=lambda i: -(raw[i][1] - base[i]))
    for i in order[:rem]:
        base[i] += 1
    for (lab, _), b in zip(raw, base):
        out += [lab] * b
    rng.shuffle(out)
    return out


# ------------------------------------------------------------------------------------------------ family card plan
# G12 r1b (capacity): cards per sampler and planned rows per card. A card's rows at one level need distinct case
# structures (one surface form per structure, G12), so rows per card follow each mode's per-level structure capacity:
# COUNT / POINTS bands are drawn to hold >= ceil(n / K) presence vectors each (build_count_card), CUT cards have
# 3 (K - 1) at / below / above values, so S6 uses one small card per packs-3 training pack (X03: one pack per card).
R1B_CARDS = {"S1": 16, "S2": 16, "S3": 28, "S4": 20}
COUNT_N = {3: 36, 4: 20, 5: 25}
POINTS_N = {3: 36, 4: 32, 5: 35, 6: 30, 7: 28}
CUT_N = {3: 8, 4: 10, 5: 13, 6: 15, 7: 18}
SAMPLER_ROWS = 945


def plan_rows(plans: list[dict], per_sampler: int = SAMPLER_ROWS) -> None:
    """p["n"] for every plan: fixed by (mode, K) for COUNT, POINTS and CUT cards; LADDER / HIGHEST cards share the rest
    of their sampler's rows evenly."""
    for s in SAMPLERS_TRAIN:
        ps = [p for p in plans if p["sampler"] == s]
        fixed = 0
        for p in ps:
            tab = {"count": COUNT_N, "points": POINTS_N, "cut": CUT_N}.get(p["mode"])
            if tab:
                p["n"] = max(2 * p["K"], tab[p["K"]])
                fixed += p["n"]
        free = [p for p in ps if p["mode"] in ("ladder", "highest")]
        if free:
            base, extra = divmod(max(0, per_sampler - fixed), len(free))
            for i, p in enumerate(free):
                p["n"] = max(2 * p["K"], base + (1 if i < extra else 0))


def pick_rows(cands: list[dict], share: float, rng: random.Random, key: str, val, plans: list[dict]) -> list[dict]:
    """Row-weighted quota per sampler: set p[key] = val on cards (random order) until their planned rows reach
    share x the sampler's planned rows (cards differ in planned rows, so a card count would miss a row share)."""
    picked = []
    for s in SAMPLERS_TRAIN:
        tgt = share * sum(p["n"] for p in plans if p["sampler"] == s)
        cs = [p for p in cands if p["sampler"] == s]
        rng.shuffle(cs)
        acc = 0
        for p in cs:
            if acc >= tgt:
                break
            if acc + p["n"] <= tgt + p["n"] / 2:
                p[key] = val
                picked.append(p)
                acc += p["n"]
    return picked


def family_plan(packs: list[dict], cards_per_sampler: int, seed: int, tag: str = "r1", packs_s6=None,
                counts: dict | None = None) -> list[dict]:
    """Card-level choices for the training samplers (one pack per card, XF09). r1b: S6 cards take the packs-3
    training packs (`packs_s6`), S1-S4 the packs-2 packs, with `counts` cards per sampler."""
    rng = rng_for("plan", seed, tag)
    counts = dict(counts or {s: cards_per_sampler for s in SAMPLERS_TRAIN})
    pk = list(packs)
    rng.shuffle(pk)
    p6 = None
    if packs_s6 is not None:
        p6 = list(packs_s6)
        rng.shuffle(p6)
        counts["S6"] = min(counts.get("S6", len(p6)), len(p6))
    n = sum(counts[s] for s in SAMPLERS_TRAIN)
    assert len(pk) >= n - (counts["S6"] if p6 is not None else 0), (len(pk), n)
    plans = []
    words = _spread(n, LEVEL_WORDS, rng)
    meanings = _spread(n, [("severity", .5), ("quality", .5)], rng)
    wfam = _spread(n, [(f"F7.{x}", 1 / 6) for x in "ABCDEF"], rng)
    start0 = _spread(n, [(True, .2), (False, .8)], rng)
    i = 0
    for s in SAMPLERS_TRAIN:
        for j in range(counts[s]):
            pack = p6[j] if (s == "S6" and p6 is not None) else pk.pop(0)
            plans.append({"sampler": s, "pack": pack, "K": None, "level_word": words[i], "meaning": meanings[i],
                          "wording_family": wfam[i], "start0": start0[i], "idx": i})
            i += 1
    # modes per sampler
    for s, shares in (("S1", [("ladder", .6), ("highest", .4)]),
                      ("S2", [("ladder", .5), ("highest", .25), ("ladder_ov", .25)]),
                      ("S3", [("count", .5), ("points", .5)]),
                      ("S4", [("ladder", .5), ("highest", .25), ("count", .25)]),
                      ("S6", [("cut", 1.0)])):
        ps = [p for p in plans if p["sampler"] == s]
        modes = _spread(len(ps), shares, rng)
        for p, m in zip(ps, modes):
            p["mode"] = "ladder" if m == "ladder_ov" else m
            p["override"] = m == "ladder_ov"
    # K (card shares pooled over F7, R20). r1b capacity: a COUNT card's bands over 0..m (m <= 6) hold one vector at an
    # end band when K >= 6, so K 6-7 go to cards other than COUNT cards and S4 (S4 COUNT cards mirror S4's K spread)
    Ks = _spread(n, [(3, .20), (4, .25), (5, .25), (6, .15), (7, .15)], rng)
    big = [k for k in Ks if k >= 6]
    small = [k for k in Ks if k < 6]
    elig = [p for p in plans if p["sampler"] != "S4" and p["mode"] != "count"]
    rng.shuffle(elig)
    assert len(elig) >= len(big), (len(elig), len(big))
    for p, k in zip(elig, big):
        p["K"] = k
    rest = [p for p in plans if p["K"] is None]
    rng.shuffle(small)
    for p, k in zip(rest, small):
        p["K"] = k
    # overrides on about 25% of ladder / highest cards of S1 and S4 (S2's ladder_ov cards already set)
    for s in ("S1", "S4"):
        lh = [p for p in plans if p["sampler"] == s and p["mode"] in ("ladder", "highest")]
        k = round(0.25 * len(lh))
        for p in rng.sample(lh, k):
            p["override"] = True
    ov = [p for p in plans if p.get("override")]
    sets = _spread(len(ov), [("floor", .35), ("cap", .35), ("both", .30)], rng)
    for p, st in zip(ov, sets):
        p["ov_set"] = st
    both = [p for p in ov if p["ov_set"] == "both"]
    wins = ["cap", "floor"] * len(both)
    for p, w in zip(both, wins):
        p["winner"] = w
    # S4 mixes ladder / highest rows (cue targets {1, 2}) with count rows (cue targets {6, 7}); give its count cards
    # a K spread proportional to the sampler's, so the mode mix is the same at every level (6.3 per-sampler test)
    s4 = [p for p in plans if p["sampler"] == "S4"]
    ks = sorted(p["K"] for p in s4)
    nc = sum(1 for p in s4 if p["mode"] == "count")
    if nc:
        pick = [ks[int((i + 0.5) * len(ks) / nc)] for i in range(nc)]
        rest = list(ks)
        for k in pick:
            rest.remove(k)
        rng.shuffle(rest)
        for p in s4:
            p["K"] = pick.pop(0) if p["mode"] == "count" else rest.pop(0)
    # count / points / cut directions
    for s in ("S3", "S4", "S6"):
        for mode in ("count", "points", "cut"):
            ps = [p for p in plans if p["sampler"] == s and p["mode"] == mode]
            if mode in ("count", "points"):  # alternate rising / falling within each K (6.3: twin cue shifts cancel)
                for K in sorted({p["K"] for p in ps}):
                    q = [p for p in ps if p["K"] == K]
                    first = rng.random() < 0.5
                    for j, p in enumerate(q):
                        p["rising"] = first if j % 2 == 0 else not first
            elif mode != "cut":
                for meaning in ("severity", "quality"):
                    q = [p for p in ps if p["meaning"] == meaning]
                    for p, r in zip(q, _spread(len(q), [(True, .5), (False, .5)], rng)):
                        p["rising"] = r
    s6 = [p for p in plans if p["sampler"] == "S6"]
    ints = _spread(len(s6), [(True, .5), (False, .5)], rng)
    for p, it in zip(s6, ints):
        p["integer_pref"] = it
    # G10 r1 (G0 6.4 T16, C11 direction): continuous cards get their side here (larger values 70%, smaller 30%), and
    # rising vs falling alternates within each group (integer cards; continuous x side) in K order, so the at-cut rows
    # of rising and falling cards (about K - 1 per card) balance inside each side.
    cont = [p for p in s6 if not p["integer_pref"]]
    for p, sd in zip(cont, _spread(len(cont), [("high", .7), ("low", .3)], rng)):
        p["side_pref"] = sd
    for grp in ([p for p in s6 if p["integer_pref"]], [p for p in cont if p["side_pref"] == "high"],
                [p for p in cont if p["side_pref"] == "low"]):
        grp = sorted(grp, key=lambda p: (p["K"], p["idx"]))
        first = rng.random() < 0.5
        for j, p in enumerate(grp):
            p["rising"] = first if (j % 2 == 0) else (not first)
    plan_rows(plans)
    # numbering: reversed on about 8% of cards (never override, masked, swapped)
    cand = [p for p in plans if not p.get("override")]
    for p in rng.sample(cand, max(1, round(0.075 * n))):
        p["reversed"] = True
    # name forms (per card): masked about 12% of rows, swapped about 5%
    cand = [p for p in plans if not p.get("reversed")]
    pick_rows(cand, 0.125, rng, "name_form", "masked", plans)  # r1b: row-weighted per sampler
    pick_rows([p for p in cand if not p.get("name_form")], 0.05, rng, "name_form", "swapped", plans)
    # definition styles: short 15% of rows (cards), few-shot 7.5% of cards, one_line_examples about 50% of cards,
    # decision lists only on highest cards
    order = list(plans)
    rng.shuffle(order)
    nfew = max(1, round(0.075 * n))
    nex = round(0.5 * n)
    pick_rows(order, 0.15, rng, "defs_style", "short", plans)  # r1b: short cards hold 15% of rows per sampler
    rest = [p for p in order if p.get("defs_style") != "short"]
    rng.shuffle(rest)
    for p in rest[:nfew]:
        p["fewshot"] = True
        p["defs_style"] = rng.choice(["one_line", "rubric_table"] + (["decision_list"] if p["mode"] == "highest" else []))
    for p in rest[nfew:nfew + nex]:
        p["defs_style"] = "one_line_examples"
    for j, p in enumerate(rest[nfew + nex:]):
        if p["mode"] == "highest" and j % 2 == 0:
            p["defs_style"] = "decision_list"
        else:
            p["defs_style"] = ["one_line", "rubric_table"][j % 2]
    # S6 needs a numeric quantity with room for K ranges; S3 needs >= 4 factors: swap packs where needed
    def ok_for(p, pack):
        if p["sampler"] == "S6":
            return any(int((a["hi"] - a["lo"]) / a["r"]) >= 4 * p["K"] + 10 for a in pack["nums"])
        if p["mode"] in ("count", "points"):  # r1b: m = 6 listed factors give the band capacity (build_count_card)
            return len(pack["factors"]) >= 6
        return len(pack["nums"]) >= 1 or len(pack["factors"]) >= 5
    for p in plans:
        if ok_for(p, p["pack"]):
            continue
        for q in plans:
            if q is not p and (p["sampler"] == "S6") == (q["sampler"] == "S6") and ok_for(p, q["pack"]) \
                    and ok_for(q, p["pack"]):
                p["pack"], q["pack"] = q["pack"], p["pack"]
                break
    # attack cards (C24): half of each sampler's cards
    for s in SAMPLERS_TRAIN:
        ps = [p for p in plans if p["sampler"] == s]
        for p in rng.sample(ps, len(ps) // 2):
            p["attack"] = True
    # deep cards: floor + cap cards, plus a few deep criteria / points cards (<= 10% of rows)
    for p in plans:
        p["deep"] = p.get("ov_set") == "both"
    extra = [p for p in plans if p["sampler"] in ("S1", "S3", "S4") and not p["deep"] and p["mode"] in
             ("ladder", "highest", "points") and not p.get("override")]
    tot_rows = sum(p["n"] for p in plans)  # r1b: deep rows (floor + cap cards included) about 7.5% of planned rows
    acc = sum(p["n"] for p in plans if p["deep"])
    rng.shuffle(extra)
    for p in extra:
        if acc + p["n"] > 0.075 * tot_rows + p["n"] / 2:
            continue
        p["deep"] = True
        acc += p["n"]
    # containers: fixed per card
    for s in SAMPLERS_TRAIN:
        ps = [p for p in plans if p["sampler"] == s]
        cs = CONTAINERS[s]
        for j, p in enumerate(ps):
            p["container"] = cs[j % len(cs)]
        rng.shuffle(cs)
    for p in plans:
        p.setdefault("reversed", False)
        p.setdefault("name_form", "plain")
        p.setdefault("fewshot", False)
        p.setdefault("attack", False)
        p.setdefault("override", False)
        p["card_id"] = f"F7-{tag}-{p['sampler']}-{p['idx']:03d}"
    return plans


def s5_plan(packs: list[dict], seed: int, n_cards: int = 10) -> list[dict]:
    rng = rng_for("plan-s5", seed)
    plans = []
    Ks = _spread(n_cards, [(3, .2), (4, .25), (5, .25), (6, .15), (7, .15)], rng)
    for i, p in enumerate(packs[:n_cards]):
        plans.append({"sampler": "S5", "pack": p, "K": Ks[i], "level_word": rng.choice(["Level", "Tier", "Grade"]),
                      "meaning": rng.choice(["severity", "quality"]), "wording_family": f"F7.{'ABCDEF'[i % 6]}",
                      "start0": rng.random() < 0.2, "idx": i, "mode": "grid", "override": False,
                      "reversed": False, "name_form": "plain", "fewshot": False, "attack": False, "deep": False,
                      "defs_style": "grid_table", "container": CONTAINERS["S5"][i % len(CONTAINERS["S5"])],
                      "card_id": f"F7-dev-S5-{i:03d}"})
    return plans


# ------------------------------------------------------------------------------------------------ levels and names
def level_presentation(plan: dict, rng: random.Random) -> dict:
    K = plan["K"]
    meaning = plan["meaning"]
    if plan["name_form"] == "swapped":
        seq = rng.choice(LEVEL_NAMES[meaning])
    else:
        pools = LEVEL_NAMES[meaning] + (LEVEL_NAMES["neutral"] if rng.random() < 0.25 else [])
        seq = rng.choice(pools)
    pos = sorted(rng.sample(range(7), K))
    names = [seq[i] for i in pos]
    usual = list(range(K))
    if plan["name_form"] == "swapped":
        for _ in range(500):
            perm = list(range(K))
            rng.shuffle(perm)
            if perm == list(range(K)) or perm == list(range(K))[::-1]:
                continue
            if K == 3:
                ok = not (perm[0] <= perm[1] <= perm[2] or perm[0] >= perm[1] >= perm[2])
            else:
                n = K
                d = sum((a - b) ** 2 for a, b in zip(perm, range(K)))
                rho = 1 - 6 * d / (n * (n * n - 1))
                ok = abs(rho) < 0.5
            # G10 r1: as many levels whose C19 alt (the level showing the usual-rank name) sits above as below
            ok = ok and sum(p_ < k for k, p_ in enumerate(perm)) == sum(p_ > k for k, p_ in enumerate(perm))
            if ok:
                break
        usual = perm
        names = [names[i] for i in perm]  # level k shows the name whose usual rank is perm[k]
    if plan["name_form"] == "masked":
        from fmt1 import labels as _labels
        scheme = rng.choice(MASK_SCHEMES)
        names = _labels.masked_ids(scheme, K, plan["card_id"])
    start = 0 if plan["start0"] else 1
    nums = list(range(start, start + K))
    if plan["reversed"]:
        nums = nums[::-1]
    lw = plan["level_word"]
    opts = [f"{lw} {nums[k]} - {names[k]}" for k in range(K)]
    q = rng.choice(SCALE_Q.get(meaning, ["severity"])) if meaning in SCALE_Q else "severity"
    return {"names": names, "usual_rank": usual, "nums": nums, "options": opts, "Q": q,
            "MB": "more" if meaning == "severity" else "better"}


# ------------------------------------------------------------------------------------------------ items
def _bool_item(f: dict, d: int) -> dict:
    return {"key": f["key"], "kind": "bool", "term": f["term"], "det": f["det"], "alias": f["alias"],
            "alias_det": f["alias_det"], "fkind": f["kind"], "dir": d, "concept": f["concept"], "about": f["about"]}


def _num_item(a: dict, d: int) -> dict:
    return {"key": a["key"], "kind": "num", "term": a["term"], "unit": a["unit"], "int": a["int"], "r": a["r"],
            "lo": a["lo"], "hi": a["hi"], "dir": d, "concept": a["concept"], "about": a["about"]}


def _date_item(a: dict, d: int, lo: int, hi: int) -> dict:
    return {"key": a["key"], "kind": "date", "term": a["term"], "dir": d, "lo": lo, "hi": hi, "r": 1,
            "concept": a["concept"], "about": a["about"]}


def _ord_item(a: dict, d: int) -> dict:
    return {"key": a["key"], "kind": "ord", "term": a["term"], "ranks": a["ranks"], "dir": d, "lo": 0,
            "hi": len(a["ranks"]) - 1, "r": 1, "concept": a["concept"], "about": a["about"]}


def bool_direction(f: dict, meaning: str, want_down: bool) -> int:
    return -1 if want_down else 1


def pick_bools(pack: dict, n: int, rng: random.Random, meaning: str, exclude=()) -> list[dict]:
    """n factors with distinct 'about' keys, half down-direction (R08); direction follows polarity where it can."""
    fs = [f for f in pack["factors"] if f["key"] not in exclude]
    rng.shuffle(fs)
    out = []
    n_down = n // 2 + (1 if (n % 2 and rng.random() < 0.5) else 0)
    downs = []
    for f in fs:
        if len(out) >= n:
            break
        natural_down = (f["pol"] == "favourable") == (meaning == "severity")
        out.append(f)
        downs.append(natural_down)
    # set directions: prefer natural ones, then fix the count
    dirs = [-1 if dn else 1 for dn in downs]
    while sum(1 for d in dirs if d == -1) > n_down:
        i = next(i for i, d in enumerate(dirs) if d == -1)
        dirs[i] = 1
    while sum(1 for d in dirs if d == -1) < n_down:
        i = next(i for i, d in enumerate(dirs) if d == 1)
        dirs[i] = -1
    return [_bool_item(f, d) for f, d in zip(out, dirs)]


def thresholds_for(item: dict, n: int, rng: random.Random, spacing_steps: int = 4) -> list:
    """n increasing thresholds on the item's grid, >= spacing_steps * r apart, with room on both ends."""
    lo, hi, r = item["lo"], item["hi"], item["r"]
    steps = int((hi - lo) / r)
    margin = max(spacing_steps, steps // 12)
    for _ in range(200):
        pts = sorted(rng.sample(range(margin, steps - margin + 1), n)) if steps - 2 * margin + 1 >= n else None
        if pts is None:
            return []
        if all(b - a >= spacing_steps for a, b in zip(pts, pts[1:])):
            return [lo + p * r for p in pts]
    return []


# ------------------------------------------------------------------------------------------------ atoms
def make_atom(item: dict, up_context: bool, t=None, rng: random.Random | None = None, *, incl: bool | None = None,
              within: tuple | None = None) -> dict:
    """An atom on `item` that holds in the item's up direction when up_context (level criteria, floors, unless-A,
    only-if C), or in its down direction (cap conditions, unless-B)."""
    rng = rng or random.Random(0)
    kind = item["kind"]
    want_up = up_context
    if kind == "bool":
        present_moves_up = item["dir"] == 1
        op = "present" if (present_moves_up == want_up) else "absent"
        return {"item": item["key"], "kind": "bool", "op": op, "neg_form": rng.randrange(3)}
    if kind == "date" and within is not None:
        D, N = within
        return {"item": item["key"], "kind": "date", "op": "within", "t": D, "N": N}
    larger_holds = (item["dir"] == 1) == want_up
    if incl is None:
        incl = rng.random() < 0.5
    op = (">=" if incl else ">") if larger_holds else ("<=" if incl else "<")
    a = {"item": item["key"], "kind": kind, "op": op, "t": t}
    if kind == "num":
        a["count"] = bool(item["int"])
        a["wv"] = rng.randrange(4)
    return a


# ------------------------------------------------------------------------------------------------ card construction
class CardFail(Exception):
    pass


def _items_for_lh(plan: dict, rng: random.Random) -> tuple[list, list]:
    """Rubric items for ladder / highest cards (and the override condition items, kept separate)."""
    pack = plan["pack"]
    K = plan["K"]
    nb = rng.randint(2, 4) if pack["nums"] else rng.randint(4, 6)
    nn = min(len(pack["nums"]), rng.randint(1, 2) if K <= 4 else rng.randint(2, 3))
    use_date = bool(pack["dates"]) and rng.random() < (0.3 if plan["sampler"] == "S4" else 0.2)
    use_ord = bool(pack["ords"]) and rng.random() < 0.3
    n_ov = (2 if plan["ov_set"] == "both" else 1) if plan.get("override") else 0
    allb = pick_bools(pack, nb + n_ov, rng, plan["meaning"])
    ov_items, bools = allb[:n_ov], allb[n_ov:]
    nums = [_num_item(a, rng.choice([1, -1])) for a in rng.sample(pack["nums"], nn)]
    items = bools + nums
    if use_date:
        a = rng.choice(pack["dates"])
        start = M.day(__import__("datetime").date.fromisoformat(pack["date_start"]))
        items.append(_date_item(a, rng.choice([1, -1]), start, start + min(pack["date_span"], 500)))
    if use_ord:
        a = rng.choice(pack["ords"])
        items.append(_ord_item(a, rng.choice([1, -1])))
    # distinct about keys (H02)
    seen, keep = set(), []
    for it in items:
        if it["about"] in seen:
            continue
        seen.add(it["about"])
        keep.append(it)
    return keep, ov_items


SHAPES = ["atom"] * 6 + ["and"] * 2 + ["or"] + ["unless"] + ["allof", "anyof"]
C1_LADDER_RUNGS = 3  # r1i: at most this many carrier rungs on a LADDER card (one reserved up-direction Boolean each)


def c1_carrier_rungs(plan: dict, K: int, bools: list, deep_level, rng: random.Random) -> dict:
    """r1i (G10 T02, C1 decisive 40-60% of unmentioned rows; was 0.24-0.34). An unmentioned factor can be decisive
    only where reading it as present moves the level: LADDER, a factor of c_{g+1}; HIGHEST, a factor of some h_k with
    k > g. A level-free factor (C1 keys are level-free, r1e) sits only in an "or" / "any of" part or a floor, and the
    old shapes put such parts on few rungs (S1 mid levels: 15 of 141 unmentioned rows decisive). S1 / S2 / S4 LADDER /
    HIGHEST cards therefore reserve an up-direction Boolean (op "present", C1-eligible) as one part of an "or" /
    "any of" rung: HIGHEST the top rung (S2: K - 2, its top rung stays and / all of), so every lower level can move;
    LADDER up to C1_LADDER_RUNGS rungs (S2: below K - 1). -> {rung k: Boolean item}"""
    if plan["sampler"] not in ("S1", "S2", "S4") or plan["mode"] not in ("ladder", "highest"):
        return {}
    if plan.get("container") in ("json", "yaml"):
        # r1j: a C15 "key" card (f7build: json / yaml with a Boolean factor) never has an unmentioned factor (C15, T02:
        # a left-out key is a missing entry), so carrier rungs there only made one-way "above" C15 entries (build 10:
        # C15 S1 above share 0.94)
        return {}
    if plan["sampler"] == "S2" and K <= 3:
        return {}  # r1j: S2 K = 3 carrier on rung 1 broke the level-0/1 S2 rows (build 10: 3 cards under quota)
    top = K - 1 if plan["sampler"] != "S2" else K - 2
    if top < 1:
        return {}
    ups = [b for b in bools if int(b["dir"]) == 1]
    rng.shuffle(ups)
    if plan["mode"] == "highest":
        want = [top] if top != deep_level else []
    else:
        cand = [k for k in range(1, top + 1) if k != deep_level]
        rng.shuffle(cand)
        want = cand[:C1_LADDER_RUNGS]
    return {k: b for k, b in zip(sorted(want, reverse=True), ups)}
NEED = {"atom": 1, "and": 2, "or": 2, "unless": 2, "allof": 3, "anyof": 3, "and_unless": 3, "nested": 4}


def build_lh_card(plan: dict, rng: random.Random) -> dict:
    """Ladder / highest card (S1, S2, S4): shapes and item use per level first, then thresholds per numeric use,
    stricter with the level (so every level stays reachable), then override conditions on their own items."""
    K = plan["K"]
    items, ov_items = _items_for_lh(plan, rng)
    bools = [it for it in items if it["kind"] == "bool"]
    others = [it for it in items if it["kind"] != "bool"]
    used_bool = set()
    specs = {}
    deep_level = None
    if plan.get("deep") and not plan.get("override"):
        deep_level = rng.randint(1, K - 1)
    c1_res = c1_carrier_rungs(plan, K, bools, deep_level, rng)
    used_bool |= {b["key"] for b in c1_res.values()}
    for k in range(1, K):
        if k in c1_res:
            # r1i (G10 T02): a C1 carrier rung reads "F or X" / "any of" with a reserved up-direction Boolean F
            free_b = [b for b in bools if b["key"] not in used_bool]
            pool_ = free_b + others
            if pool_:
                n_o = 2 if len(pool_) >= 2 and rng.random() < 0.3 else 1
                picks = [c1_res[k]] + rng.sample(pool_, n_o)
                rng.shuffle(picks)
                for it in picks:
                    if it["kind"] == "bool":
                        used_bool.add(it["key"])
                specs[k] = ("or" if n_o == 1 else "anyof", picks, None)
            else:
                specs[k] = ("atom", [c1_res[k]], None)
            continue
        shape = rng.choice(SHAPES)
        if plan["sampler"] == "S2" and k == K - 1:
            shape = rng.choice(["and", "allof"])
        if k == deep_level:
            shape = "nested"
        free_b = [b for b in bools if b["key"] not in used_bool]
        avail = len(free_b) + len(others)
        if NEED[shape] > avail:
            shape = "and" if avail >= 2 and rng.random() < 0.5 else "atom"
        if shape == "unless" and not (free_b and (len(free_b) + len(others)) >= 2):
            shape = "atom"
        # choose items: the unless part B is a free Boolean factor (down context)
        picks = []
        pool_ = free_b + others
        if shape == "unless":
            b_item = rng.choice(free_b)
            used_bool.add(b_item["key"])
            rest = [x for x in pool_ if x is not b_item]
            a_item = rng.choice(rest)
            if a_item["kind"] == "bool":
                used_bool.add(a_item["key"])
            specs[k] = ("unless", [a_item], b_item)
            continue
        n = NEED[shape]
        if len(pool_) < n:
            shape, n = "atom", 1
        picks = rng.sample(pool_, n)
        for it in picks:
            if it["kind"] == "bool":
                used_bool.add(it["key"])
        specs[k] = (shape, picks, None)
    # numeric uses per item, in level order -> thresholds stricter with the level
    uses = {}
    for k in range(1, K):
        for it in specs[k][1]:
            if it["kind"] != "bool":
                uses.setdefault(it["key"], []).append(k)
    thr = {}
    for key, lv in uses.items():
        it = next(x for x in others if x["key"] == key)
        n = len(lv)
        if it["kind"] == "num":
            ts = thresholds_for(it, n, rng)
        elif it["kind"] == "date":
            span = int(it["hi"] - it["lo"])
            if span < 40 + 8 * n:
                raise CardFail("date span")
            ts = sorted(rng.sample(range(int(it["lo"]) + 20, int(it["hi"]) - 20, 6), n))
        else:
            nr = len(it["ranks"])
            if n > nr - 2:
                raise CardFail("ranks")
            ts = sorted(rng.sample(range(1, nr - 1), n))
        if len(ts) < n:
            raise CardFail("no thresholds")
        if it["dir"] == -1:
            ts = ts[::-1]
        thr[key] = dict(zip(lv, ts))
    incl = {it["key"]: rng.random() < 0.5 for it in others}

    def atom_on(it, k, up=True):
        if it["kind"] == "bool":
            return {"t": "atom", "a": make_atom(it, up, rng=rng)}
        return {"t": "atom", "a": make_atom(it, up, thr[it["key"]][k], rng, incl=incl[it["key"]] if rng.random() < 0.8
                                            else None)}
    crits = {}
    for k in range(1, K):
        shape, picks, b_item = specs[k]
        if shape == "atom":
            crits[k] = atom_on(picks[0], k)
        elif shape in ("and", "or"):
            crits[k] = {"t": shape, "parts": [atom_on(it, k) for it in picks]}
        elif shape == "unless":
            crits[k] = {"t": "unless", "a": atom_on(picks[0], k), "b": make_atom(b_item, False, rng=rng)}
        elif shape in ("allof", "anyof"):
            crits[k] = {"t": shape, "parts": [atom_on(it, k) for it in picks]}
        elif shape == "nested":
            outer = rng.choice(["allof", "anyof"])
            inner = "anyof" if outer == "allof" else "allof"
            crits[k] = {"t": outer, "parts": [atom_on(picks[0], k), atom_on(picks[1], k),
                                              {"t": inner, "parts": [atom_on(picks[2], k), atom_on(picks[3], k)]}]}
    # 'only if' on highest cards with no override (C5): one level, a single free Boolean atom
    if plan["mode"] == "highest" and not plan.get("override") and rng.random() < 0.3 and K >= 3:
        n = rng.randint(1, K - 1)
        free_b = [b for b in bools if b["key"] not in used_bool]
        if crits[n]["t"] not in ("unless",) and M.n_ops(crits[n]) <= 1 and free_b and n not in c1_res:
            it = rng.choice(free_b)
            used_bool.add(it["key"])
            crits[n] = {"t": "onlyif", "main": crits[n], "c": make_atom(it, True, rng=rng)}
    used = {a["item"] for c in crits.values() for a in M.atoms_of(c)}
    card = {"K": K, "mode": plan["mode"], "items": {it["key"]: it for it in items if it["key"] in used},
            "crits": crits}
    if plan.get("override"):
        st = plan["ov_set"]
        oi = list(ov_items)
        ovs = []
        for it in oi:
            card["items"][it["key"]] = it
        if st in ("floor", "both"):
            it = oi.pop(0)
            m_f = rng.randint(1, K - 1)
            ovs.append({"type": "floor", "cond": {"t": "atom", "a": make_atom(it, True, rng=rng)}, "m": m_f})
        if st in ("cap", "both"):
            it = oi.pop(0)
            if st == "both":
                m_c = rng.randint(0, ovs[0]["m"] - 1)
            else:
                m_c = rng.randint(0, K - 2)
            ovs.append({"type": "cap", "cond": {"t": "atom", "a": make_atom(it, False, rng=rng)}, "m": m_c})
        card["overrides"] = ovs
        if st == "both":
            card["winner"] = plan["winner"]
    return card


def build_count_card(plan: dict, rng: random.Random) -> dict:
    pack = plan["pack"]
    K = plan["K"]
    mode = plan["mode"]
    rising = plan.get("rising", True)
    nf = len(pack["factors"])
    lo_m = max(4, K - 1)
    # G12 r1d: COUNT cards may list 7 factors (G0 S3 4-8; f >= m, m + f <= 16): with m <= 6 a K = 3 or K = 5 COUNT
    # card has one band layout per direction meeting the band capacity, so cards shared rubrics and rows of different
    # cards shared structures (G12 structure hash, cross-card). POINTS keeps m <= 6.
    hi_m = min(7 if mode == "count" else 6, nf)
    if lo_m > hi_m:
        raise CardFail("not enough factors")
    # G12 r1b: every band must hold >= Q distinct presence vectors (Q = ceil(n / K), n = the card's planned rows), so
    # the card can give each of its rows at a level its own structure; m, weights and cuts stay random among the
    # draws that meet it (Z02), and a card that cannot is redrawn (CardFail).
    Q = -(-int(plan.get("n") or 0) // K) if plan.get("n") else 0
    for _outer in range(80):
        m = rng.randint(lo_m, hi_m)
        fs = rng.sample(pack["factors"], m)
        d = 1 if rising else -1
        items = [_bool_item(f, d) for f in fs]
        listed = [it["key"] for it in items]
        card = {"K": K, "mode": mode, "items": {it["key"]: it for it in items}, "listed": listed, "rising": rising}
        mult = collections.Counter()
        if mode == "count":
            for c in range(0, m + 1):
                mult[c] = math.comb(m, c)
        else:
            P = 4 if not plan.get("deep") else rng.randint(5, min(6, m))
            card["P"] = P
            for _ in range(200):
                w = {f: rng.randint(1, 3) for f in listed}
                if len(set(w.values())) >= 2:
                    break
            card["weights"] = w
            for r in range(0, min(P, m) + 1):
                for sub in itertools.combinations(listed, r):
                    mult[sum(w[f] for f in sub)] += 1
            if max(mult) > 3 * m:
                continue
        totals = sorted(mult)
        span_lo, span_hi = 0, (m if mode == "count" else max(totals))
        if span_hi - span_lo < K - 1:
            continue
        found = None
        for _ in range(300):
            cuts = sorted(rng.sample(range(span_lo + 1, span_hi + 1), K - 1))
            bounds = [span_lo] + cuts + [span_hi + 1]
            bbv = [(bounds[j], bounds[j + 1] - 1) for j in range(K)]
            if all(sum(mult[t] for t in range(lo, hi + 1)) >= Q + 2 for lo, hi in bbv):  # + worked cases, flips
                if mode == "count" and (K, m, rising, tuple(bbv)) in plan.get("_avoid_rub", ()):
                    continue  # r1d: COUNT rubric already used by another card of the group (G12 cross-card)
                found = bbv
                break
        if found:
            break
    else:
        raise CardFail("bands: capacity")
    bands_by_value = found
    card["rub_key"] = (K, m, rising, tuple(found))
    bands_by_value[-1] = (bands_by_value[-1][0], OPEN_TOP)  # largest-value band: "<N> or more" (C11)
    bands = bands_by_value if rising else bands_by_value[::-1]
    card["bands"] = bands
    card["band_by_value"] = bands_by_value
    return card


def build_cut_card(plan: dict, rng: random.Random) -> dict:
    pack = plan["pack"]
    K = plan["K"]
    nums = list(pack["nums"])
    rng.shuffle(nums)
    pref = plan.get("integer_pref", True)
    nums.sort(key=lambda a: 0 if a["int"] == pref else 1)
    for a in nums:
        it = _num_item(a, 1 if plan.get("rising", True) else -1)
        steps = int((it["hi"] - it["lo"]) / it["r"])
        if steps < 4 * K + 10:
            continue
        cuts = thresholds_for(it, K - 1, rng, spacing_steps=4)
        if not cuts:
            continue
        integer = bool(it["int"])
        side_draw = "high" if rng.random() < 0.7 else "low"
        side = "high" if integer else (plan.get("side_pref") or side_draw)
        return {"K": K, "mode": "cut", "items": {it["key"]: it}, "qty": it["key"], "cuts": cuts, "integer": integer,
                "side": side, "rising": plan.get("rising", True)}
    raise CardFail("no cut quantity")


def build_grid_card(plan: dict, rng: random.Random) -> dict:
    pack = plan["pack"]
    K = plan["K"]
    nb = rng.randint(1, 2)
    nn = min(len(pack["nums"]), rng.randint(1, 2))
    bools = pick_bools(pack, nb + 1, rng, plan["meaning"])
    nums = [_num_item(a, rng.choice([1, -1])) for a in rng.sample(pack["nums"], nn)]
    items = bools + nums
    if len(items) < 2:
        raise CardFail("grid items")
    thr = {it["key"]: (thresholds_for(it, 3, rng) if it["dir"] == 1 else thresholds_for(it, 3, rng)[::-1])
           for it in nums}
    if any(not v for v in thr.values()):
        raise CardFail("grid thr")
    # nested rows: row 1 holds 1 requirement; each next row adds one requirement or one stricter threshold
    rows = {}
    current = {}
    stage = {it["key"]: -1 for it in nums}
    for k in range(1, K):
        options = [it for it in items if it["key"] not in current]
        stricter = [it for it in nums if it["key"] in current and stage[it["key"]] < len(thr[it["key"]]) - 1]
        choice = None
        if options and (not stricter or rng.random() < 0.6):
            choice = ("add", rng.choice(options))
        elif stricter:
            choice = ("strict", rng.choice(stricter))
        else:
            raise CardFail("grid exhausted")
        how, it = choice
        if it["kind"] == "bool":
            current[it["key"]] = make_atom(it, True, rng=rng)
        else:
            stage[it["key"]] += 1
            t = thr[it["key"]][stage[it["key"]]]
            prev = current.get(it["key"])
            incl = prev["op"] in (">=", "<=") if prev else None
            current[it["key"]] = make_atom(it, True, t, rng, incl=incl)
        rows[k] = [dict(a) for a in current.values()]
    return {"K": K, "mode": "grid", "items": {it["key"]: it for it in items}, "grid": rows,
            "grid_cols": [it["key"] for it in items]}


def quick_check(card: dict, rng: random.Random, n: int = 4000) -> bool:
    """Generator-side sanity: every level reachable by random draws (the real proofs are solver B's, 4.3)."""
    seen = set()
    for _ in range(n):
        v = random_values(card, rng)
        seen.add(M.final_level(card, v))
        if len(seen) == card["K"]:
            return True
    return False


def random_values(card: dict, rng: random.Random, near: float = 0.5) -> dict:
    v = {}
    thr = collect_thresholds(card)
    for k, it in card["items"].items():
        if it["kind"] == "bool":
            v[k] = rng.random() < 0.5
        elif it["kind"] in ("num", "date", "ord"):
            r = it["r"]
            ts = thr.get(k, [])
            if ts and rng.random() < near:
                t = rng.choice(ts)
                x = t + rng.choice([-1, 0, 1]) * r
            else:
                steps = int((it["hi"] - it["lo"]) / r)
                x = it["lo"] + rng.randint(0, steps) * r
            x = min(max(x, it["lo"]), it["hi"])
            v[k] = x
    if card["mode"] == "points":
        on = [f for f in card["listed"] if v[f]]
        rng.shuffle(on)
        for f in on[card["P"]:]:
            v[f] = False
    return v


def collect_thresholds(card: dict) -> dict:
    out = {}

    def add(a):
        if a.get("kind") in ("num", "date", "ord") and a["op"] != "within":
            out.setdefault(a["item"], set()).add(a["t"])
        elif a["op"] == "within":
            out.setdefault(a["item"], set()).update({a["t"], a["t"] + a["N"]})
    for c in card.get("crits", {}).values():
        for a in M.atoms_of(c):
            add(a)
    for o in card.get("overrides", []):
        for a in M.atoms_of(o["cond"]):
            add(a)
    for row in card.get("grid", {}).values():
        for a in row:
            add(a)
    if card["mode"] == "cut":
        out[card["qty"]] = set(card["cuts"])
    return {k: sorted(v) for k, v in out.items()}


def build_card(plan: dict, attempt: int = 0) -> dict:
    rng = rng_for("card", plan["card_id"], attempt)
    mode = plan["mode"]
    if mode in ("ladder", "highest"):
        card = build_lh_card(plan, rng)
    elif mode in ("count", "points"):
        card = build_count_card(plan, rng)
    elif mode == "cut":
        card = build_cut_card(plan, rng)
    elif mode == "grid":
        card = build_grid_card(plan, rng)
    else:
        raise ValueError(mode)
    card["plan"] = {k: v for k, v in plan.items() if k != "pack"}
    card["pack_id"] = plan["pack"]["id"]
    card["card_id"] = plan["card_id"]
    card["sampler"] = plan["sampler"]
    if mode in ("ladder", "highest", "grid"):
        for l in range(card["K"]):
            if not _reach(card, rng, l):
                raise CardFail("unreachable level")
    elif not quick_check(card, rng):
        raise CardFail("unreachable level")
    return card


def _reach(card, rng, l, tries=80):
    import f7rows as _RW
    for _ in range(tries):
        v = _RW.construct(card, rng, l)
        if v is not None and M.mode_level(card, v) == l:
            return True
    return False
