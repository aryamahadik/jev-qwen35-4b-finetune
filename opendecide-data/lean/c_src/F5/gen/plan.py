"""Card plan (G0 sections 1, 3.1, 8): one pack per card (XF09), sampler and world cells, antithetic per-card yes rates
(r_card uniform 20-80%, f_card, a_card), contrast-pair share p_card, card constants (rule set), cue-family sets,
definition styles, few-shot and inverted cards, instruction wordings (>= 5 per card) and a fixed style subset."""
from __future__ import annotations

import json
import math

from .common import FMT2, rng_for, read_jsonl
from .packs import views

SHARES_TRAIN = {"S1": 0.2683, "S2": 0.2439, "S3": 0.2439, "S4": 0.2439}   # S6 share moved to S1-S4 (S6 not buildable)
WORLD = {"S1": 0.60, "S2": 0.70, "S3": 0.40, "S4": 1.0, "S5": 0.75}      # closed share per sampler
C_PAIR = 0.60   # raised from about 0.42: open S2 / S3 cards cannot hold contrast pairs (see manifest)
FAMS = {
    "S1": ["C1", "C2", "C6", "C13", "C16", "C9", "C12", "C5"],
    "S2": ["C1", "C2", "C3", "C10", "C15"],
    "S3": ["C1", "C2", "C6", "C5", "C8", "C13", "C16", "C11"],
    "S4": ["C1", "C2", "C8", "C9", "C11", "C14", "C16"],
    "S5": ["C1", "C2", "C7", "C16"],
}
DEFS_VARIANTS = {"one_line": ["DV01", "DV02", "DV03", "DV04", "DV05", "DV06"],
                 "one_line_examples": ["DV11", "DV12", "DV13", "DV14", "DV15", "DV16"],
                 "rubric_table": ["DV21", "DV22", "DV23", "DV24"],
                 "decision_list": ["DV31", "DV33", "DV35"]}


def f_card(r):
    return max(0.15, 1 / r - 4, (4 * r - 3) / (1 - r))


def a_card(r, f):
    return (r * (4 + f) - 1) / (2 + f)


def wordings():
    rows = [w for w in read_jsonl(FMT2 / "wordings" / "family_pools.jsonl") if w["family"] == "F5"]
    return sorted(rows, key=lambda w: w["id"])


def plan_cards(n_cards: int, *, split="train", samplers=None, seed_tag="r1", shares=None, held_pids=None):
    """Card list for one split. Training: S1-S4 cells; antithetic partners inside (sampler, world, inverted) cells."""
    shares = shares or SHARES_TRAIN
    rng = rng_for("f5-plan", seed_tag, split)
    pks = views(split) if held_pids is None else [v for v in views("heldout") if v["pid"] in held_pids]
    pks = sorted(pks, key=lambda v: v["pid"])
    rng.shuffle(pks)
    if len(pks) < n_cards:
        raise SystemExit(f"need {n_cards} packs, have {len(pks)}")
    samplers = samplers or list(shares)
    counts = {s: int(round(n_cards * shares[s])) for s in samplers}
    while sum(counts.values()) > n_cards:
        counts[max(counts, key=counts.get)] -= 1
    while sum(counts.values()) < n_cards:
        counts[min(counts, key=counts.get)] += 1
    for s in counts:            # even counts so every card has an antithetic partner
        if counts[s] % 2:
            counts[s] += 1
    W = wordings()
    cards = []
    i = 0
    for s in samplers:
        n = counts[s]
        n_closed = int(round(n * WORLD[s] / 2)) * 2
        n_inv = {"S1": 8, "S4": 6}.get(s, 0) if split == "train" else 0
        for j in range(n):
            if i >= len(pks):
                break
            pv = pks[i]
            i += 1
            world = "closed" if (j < n_closed or s == "S4") else "open"
            inverted = j < n_inv
            cards.append({"sampler": s, "pack": pv, "world": world, "inverted": inverted})
    # antithetic pairs inside (sampler, world, inverted) cells, leftovers paired with each other
    cells = {}
    for c in cards:
        cells.setdefault((c["sampler"], c["world"], c["inverted"]), []).append(c)
    pairs, left = [], []
    for key in sorted(cells):
        lst = cells[key]
        for a, b in zip(lst[0::2], lst[1::2]):
            pairs.append((a, b))
        if len(lst) % 2:
            left.append(lst[-1])
    rng.shuffle(left)
    for a, b in zip(left[0::2], left[1::2]):
        pairs.append((a, b))
    if len(left) % 2:
        cards.remove(left[-1])
    out = []
    for pi, (a, b) in enumerate(pairs):
        r = 0.2 + 0.6 * rng.random() if split == "train" else 0.25 + 0.5 * rng.random()
        for c, rr in ((a, r), (b, 1 - r)):
            c["r_card"] = rr
            if split == "train":
                c["f_card"] = f_card(rr)
                c["a_card"] = a_card(rr, c["f_card"])
                infeasible = c["inverted"] or c["sampler"] not in ("S1", "S2", "S3", "S4") or \
                    (c["sampler"] in ("S2", "S3") and c["world"] == "open")
                c["p_card"] = 0.0 if infeasible else min(C_PAIR, 2 * c["a_card"], 2 * (1 - c["a_card"]))
            else:
                c["f_card"] = 0.0
                c["a_card"] = (4 * rr - 1) / 2
                c["p_card"] = 0.0
            c["pair_index"] = pi
        a["partner"], b["partner"] = b, a
        out += [a, b]
    for n, c in enumerate(out):
        crng = rng_for("f5-card", seed_tag, split, c["pack"]["pid"])
        c["card_id"] = f"F5-{seed_tag}-{split[:2]}-{c['sampler']}-{c['pack']['pid']}"
        c["split"] = split
        fams = list(FAMS[c["sampler"]])
        core = {"S1": ["C1", "C2", "C13"], "S2": ["C1", "C2", "C3", "C10"], "S3": ["C1", "C2", "C8"],
                "S4": ["C1", "C2", "C8", "C9"], "S5": ["C1", "C2", "C7"]}[c["sampler"]]
        opt = [f for f in fams if f not in core]
        crng.shuffle(opt)
        keep = core + opt[:max(2, int(len(opt) * 0.7))]
        c["fams"] = {f: (f in keep) for f in fams}
        c["defs_style"] = crng.choices(["one_line", "one_line_examples", "rubric_table", "decision_list"],
                                       [30, 50, 10, 10])[0]
        if c["sampler"] == "S2":       # S2 cards are the longest (logs + SEM-11 / -16 / -19 / -20 / -33): no examples
            c["defs_style"] = crng.choice(["one_line", "decision_list"])
        c["defs_variant"] = crng.choice(DEFS_VARIANTS[c["defs_style"]])
        c["sem_variant"] = "c" if c["sampler"] == "S2" else crng.choice(["a", "b", "c"])
        c["fewshot"] = False
        pool_w = [w for w in W if w["n_words"] <= 14] if c["sampler"] == "S2" else W   # S2: length cap
        c["wordings"] = sorted(crng.sample(pool_w, 6), key=lambda w: w["id"])
        c["seed"] = int(crng.random() * 2 ** 31)
    for c in out:   # S2: negative aspect (C15, SEM-26 on the card) on about 30% of card pairs (length cap)
        if c["sampler"] == "S2" and "C15" in c["fams"]:
            c["fams"]["C15"] = (c["pair_index"] % 10) < 3
    for c in out:   # antithetic partners share the cue-family set (mirrored V templates need the same families)
        if c["pair_index"] is not None and c is not c["partner"] and out.index(c) > out.index(c["partner"]):
            c["fams"] = dict(c["partner"]["fams"])
            # repair r2 (G7 / G10 matched twins): partners also share the instruction wordings, the definition style
            # and variant and the SEM variant, so every card-layout and wording n-gram is seen at r and 1 - r and the
            # mirrored slots of the two cards balance each wording cell exactly (S2's short-wording pool wins)
            src = c["partner"] if not (c["sampler"] == "S2" and c["partner"]["sampler"] != "S2") else c
            dst = c if src is c["partner"] else c["partner"]
            dst["wordings"] = src["wordings"]
            # S2 is the longest sampler (length cap): an S2 pair takes the one-line definitions when either card drew them
            # (an S2 card's own draw is never examples; a mixed pair takes the S2 card's draw)
            sd = src
            s2 = [x for x in (c["partner"], c) if x["sampler"] == "S2"]
            if s2:
                sd = next((x for x in s2 if x["defs_style"] == "one_line"), s2[0])
            for k in ("defs_style", "defs_variant", "sem_variant"):
                (c if sd is c["partner"] else c["partner"])[k] = sd[k]
    if split == "train":
        orient_pairs(out, seed_tag)
    if split == "train":
        # few-shot cards: 5-10% of cards (whole antithetic pairs, so per-card rates stay mirrored)
        idx = list(range(0, len(out), 2))
        rng.shuffle(idx)
        for k in idx[:max(1, int(round(len(out) * 0.075 / 2)))]:
            out[k]["fewshot"] = out[k + 1]["fewshot"] = True
    return out


def card_summary(c):
    return {k: c[k] for k in ("card_id", "sampler", "world", "inverted", "r_card", "f_card", "a_card", "p_card",
                              "defs_style", "defs_variant", "sem_variant", "fewshot")} | {
        "pack": c["pack"]["pid"], "partner": c["partner"]["card_id"], "fams": sorted(f for f, x in c["fams"].items()
                                                                                      if x),
        "wordings": [w["id"] for w in c["wordings"]], "persona_seed": c["pack"]["persona_seed"],
        "pair_index": c.get("pair_index"),
        "constants": c.get("constants"), "rule_signature": c.get("rule_signature")}


if __name__ == "__main__":
    cs = plan_cards(120)
    import collections
    print(collections.Counter((c["sampler"], c["world"], c["inverted"]) for c in cs))
    print(len(cs), sum(c["fewshot"] for c in cs), sum(c["inverted"] for c in cs))
    print(json.dumps(card_summary(cs[0]), indent=1)[:800])
    print(sum(c["a_card"] for c in cs) / len(cs), sum(c["f_card"] for c in cs) / len(cs))


def orient_pairs(cards, seed_tag):
    """Repair r2 (G7 matched twins at card level): which card of an antithetic pair takes r and which 1 - r is free
    (r is uniform on 20-80%, so both cards stay uniform). A seeded local search on a first-pass vocabulary file
    (tmp/orient_<tag>.json, written by gen/orient.py from that pass's rows) picks the orientation so that words shared
    by several cards are seen at balanced rates. No file: the plan's own orientation (first pass)."""
    from .common import TMP
    p = TMP / f"orient_{seed_tag}.json"
    if not p.exists():
        return
    flips = set(json.load(open(p))["flip"])
    seen = set()
    for c in cards:
        pi = c["pair_index"]
        if pi in flips and pi not in seen:
            seen.add(pi)
            a, b = c, c["partner"]
            for k in ("r_card", "a_card"):
                a[k], b[k] = b[k], a[k]
