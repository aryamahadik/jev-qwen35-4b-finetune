"""Card and row-spec planning (G0 section 7 cell counts, section 6 display / option buckets / balance).

Every draw here reads ids and the spec only (never a label it computed), so display, k, frame, wording and style
never depend on the gold.
"""
from __future__ import annotations

import random

from .common import rng_for
from . import packs_f6

# r1 sampler x form cells (G0 s7); candidates = 1.5x
CELLS = {
    "S1": {"qdet": 100, "qest": 50, "qplain": 50, "c_out": 584, "c_gap": 216},
    "S2": {"qdet": 94, "qest": 94, "c_out": 496, "c_case": 216},
    "S3": {"qdet": 306, "qest": 120, "qplain": 186, "c_rec": 288},
    "S4": {"qdet": 400, "qest": 186, "qplain": 214},
}
# cards per sampler and schema (r1; G0 s7)
CARDS = {
    "S1": {"yn": 5, "c_out": 4, "c_out_t": 10, "c_gap": 5},
    "S2": {"yn": 4, "c_out": 7, "c_case": 9},
    "S3": {"yn": 14, "c_rec": 6},
    "S4": {"yn": 16},
}
# C-OUT option buckets (r1 rows; G0 s6 table): C-OUT 2-4: 306, 5-9: 522, 10-19: 162, 20-32: 90. k >= 10 comes only from
# S1 outcome-table cards (S2 C-OUT uses k <= 9); the 2-4 / 5-9 rows split between S1 and S2 by their C-OUT rows.
# Repair r1: with the shorter switch sentences the k 10-24 rows fit the 1,900-token cap (G0 s1); k 25-32 does not
# (an outcome table of 25-30 composite names plus the option list passes the cap), so C-OUT's 20-32 rows use k 20-24.
# Repair r1 v3b: k 20-24 failed the cap on every draw (78 of 127 units on length); the 20-32 bucket now uses k 20-21
# on dedicated pure outcome-table cards (PURE_TABLE: no quantity, so no quantity-domain or comparison-word lines;
# only k >= COUT_PURE_MIN_K rows, whose policy is the table alone).
# Repair r1 v3d (PREREG A22, tmp/repair/INFEASIBLE_length.md): rows may run to 7,900 tokens once the 1,900 cap fails on
# every redraw, so the 20-60 bucket is back to the G0 s6 range k 20-32 (uniform) and C-REC to k 20-60.
COUT_K = {"S1": {(2, 4): 123, (5, 9): 209, (10, 19): 162, (20, 32): 90},
          "S2": {(2, 4): 183, (5, 6): 313}}
COUT_PURE_MIN_K = 14   # repair r1 v3c: pure cards (no quantity, one off-path category, one notice, open world, short
                       # names, no row 10) fit k 14-21 under the rendered 1,900 cap; k 22-32 does not (INFEASIBLE note)
PURE_TABLE = {f"F6-S1-c_out_t-{i:02d}" for i in (0, 2, 4)}   # v3c: the table cards whose packs have the shortest outcome names
COUT_TABLE_MIN_K = 6           # S1: k 6-32 on outcome-table cards (one rule holds the catalog), k 2-5 on plain cards
# C-REC: compact containers (CSV, markdown) with 3 columns; 10-19: 108, 20-60: 180 (G0 s6 table). Repair r1: k 51-60
# passes the 1,900-token cap (table of k records in `state` plus k ID options), so the 20-60 rows use k 20-50.
CREC_K = {(10, 19): 108, (20, 60): 180}
CCASE_K = {(3, 4): 108, (5, 6): 108}


def _pack_caps(v: dict) -> set:
    """Polarity capabilities of a pack (repair r1: every yes/no claim carries a 'yes = bad' valence, s6 / XF04)."""
    from .emit import outcome_valence
    caps = set()
    if any(q.get("adverse") for q in v["qty"]):
        caps.add("pq")
    pol = [v.get("ev_pol", {}).get(e) for e in v["events"]]
    if "good" in pol and "bad" in pol:
        caps.add("gb")
    ov = [outcome_valence({"pack": v}, o) for o in v["outcomes"]]
    if ov.count("bad") >= 2 and ov.count("good") >= 2:
        caps.add("outs")
    if len(v["outcomes"]) >= 8 and len(v["outcomes"]) * len(v["places"]) >= 40 and len(v["places"]) >= 6:
        caps.add("table")              # an outcome table of up to 6 x 5 distinct outcomes (G0 s7 S1)
    if len(v["outcomes"]) >= 8:
        caps.add("cat8")               # k up to 7 on plain C-OUT cards (catalog = rule heads + default)
    return caps


def plan_cards(set_tag: str = "r1") -> list[dict]:
    """80 cards, one distinct train pack each (XF09). Yes/no cards take packs whose polarity metadata lets every
    claim carry a valence (S4: polar quantities and good/bad events; S3: polar quantities; S1/S2: polar outcomes)."""
    P = packs_f6.packs("train")
    rng = rng_for("cards", set_tag)
    order = list(range(len(P)))
    rng.shuffle(order)
    caps = {i: _pack_caps(P[i]) for i in order}
    slots = []
    for smp in ("S1", "S2", "S3", "S4"):
        for schema, n in CARDS[smp].items():
            for j in range(n):
                slots.append((smp, schema, j))
    need = {("S4", "yn"): {"pq", "gb"}, ("S3", "yn"): {"pq"}, ("S1", "yn"): {"outs"}, ("S2", "yn"): {"outs"},
            ("S1", "c_out_t"): {"table"}, ("S1", "c_out"): {"cat8"}, ("S2", "c_out"): {"cat8"}}
    prio = sorted(range(len(slots)), key=lambda i: -len(need.get(slots[i][:2], set())))
    used, got = set(), {}
    for si in prio:
        req = need.get(slots[si][:2], set())
        pick = next((i for i in order if i not in used and req <= caps[i]), None)
        if pick is None:
            pick = next(i for i in order if i not in used)
        used.add(pick)
        got[si] = pick
    out = []
    for si, (smp, schema, j) in enumerate(slots):
        out.append({"card_id": f"F6-{smp}-{schema}-{j:02d}", "sampler": smp, "schema": schema,
                    "pack": P[got[si]]["pid"]})
    return out


def _alloc(total: int, cards: list) -> list[int]:
    n = len(cards)
    base = [total // n] * n
    for i in range(total - sum(base)):
        base[i] += 1
    return base


def _display(rng, k):
    if k == 2:
        return False, False
    nei_p, none_p = min(1.0, 0.1 * k), min(1.0, 0.05 * k)
    if k <= 4:
        u = rng.random()
        if u < nei_p:
            return True, False
        if u < nei_p + none_p:
            return False, True
        return False, False
    return rng.random() < nei_p, rng.random() < none_p


def _gold_slot(rng, k, nei, none, w_abstain):
    slots = ["concrete"] * (k - nei - none) + (["nei"] if nei else []) + (["none"] if none else [])
    w = [1.0 if s == "concrete" else w_abstain for s in slots]
    return rng.choices(slots, weights=w)[0]


class _Systematic:
    """Repair r1 v3f (G10 abstain display / abstain gold per k; G7 'opt:of' via None gold): systematic sampling of the
    display draw and the gold slot. Every spec keeps its s6 probability (P(NEI shown | k) = min(1, 0.1k), P(None shown
    | k) = min(1, 0.05k), independent at k >= 5 and disjoint at 3-4; each slot gold w.p. 1/k), but within one cell
    (k for display, (form group, k) for the gold slot) the realised counts stay within about 1-2 of the
    expected counts (stratified blocks of 20 uniforms per cell, from a separate seeded rng). v3e drew them i.i.d.:
    the planned NEI share at k = 3 was 0.243 vs 0.30 and None gold over None-shown rows 105 vs 87.2 expected.
    Label-free: reads k, display and the spec's form only. The main spec rng is still advanced exactly as before (the
    i.i.d. draws are made and discarded), so k, card and every other planned field are unchanged."""

    def __init__(self, set_tag):
        self.rng = rng_for("specs_sys", set_tag)
        self.u = {}

    BLOCK = 20

    def pick(self, cell, probs):
        """probs: ordered {category: p}. Stratified blocks per cell: each block of BLOCK draws takes one uniform from
        each stratum [m / BLOCK, (m + 1) / BLOCK) in a random order, so every u is uniform (each spec keeps exactly its
        s6 probabilities), the counts per category stay within about 1 of the expected counts per block, and cells
        are independent of each other (own random order and jitter). Category = inverse CDF of u."""
        q = self.u.get(cell)
        if not q:
            order = list(range(self.BLOCK))
            self.rng.shuffle(order)
            q = self.u[cell] = [(m + self.rng.random()) / self.BLOCK for m in order]
        x, acc = q.pop(), 0.0
        cats = list(probs)
        for c in cats:
            acc += probs[c]
            if x < acc:
                return c
        return cats[-1]

    def display(self, k):
        if k == 2:
            return False, False
        p1, p2 = min(1.0, 0.1 * k), min(1.0, 0.05 * k)
        if k <= 4:
            c = self.pick(("disp", k), {"nei": p1, "none": p2, "neither": 1.0 - p1 - p2})
            return c == "nei", c == "none"
        nei = self.pick(("nei", k), {True: p1, False: 1.0 - p1})
        none = self.pick(("none", k, nei), {True: p2, False: 1.0 - p2}) if p2 < 1.0 else True
        return nei, none

    def gold(self, grp, k, nei, none, w_abstain):
        conc = k - nei - none
        tot = conc + w_abstain * (nei + none)
        probs = {}
        if nei:
            probs["nei"] = w_abstain / tot
        if none:
            probs["none"] = w_abstain / tot
        probs["concrete"] = conc / tot
        return self.pick(("gold", grp, k), probs)          # one sequence per k: NEI slot first, then None


def plan_specs(cards: list[dict], scale: float, set_tag: str, w_abstain: float = 1.0) -> list[dict]:
    """Row specs (one per planned row; twins and relation units consume several) for every card."""
    rng = rng_for("specs", set_tag)
    sysd = _Systematic(set_tag)
    specs = []
    by = {}
    for c in cards:
        by.setdefault((c["sampler"], c["schema"]), []).append(c)
    for smp, cells in CELLS.items():
        for form, n in cells.items():
            n = round(n * scale)
            if form in ("qdet", "qest", "qplain"):
                cs = by[(smp, "yn")]
            elif form == "c_out" and smp == "S1":
                cs = by[(smp, "c_out")] + by[(smp, "c_out_t")]
            else:
                cs = by[(smp, {"c_out": "c_out", "c_gap": "c_gap", "c_case": "c_case", "c_rec": "c_rec"}[form])]
            if form == "c_out":
                buckets = COUT_K[smp]
                tot = sum(buckets.values())
                plain = [c for c in cs if c["schema"] == "c_out"]
                tab = [c for c in cs if c["schema"] == "c_out_t" and c["card_id"] not in PURE_TABLE]
                pure = [c for c in cs if c["card_id"] in PURE_TABLE]
                ip = it = iq = 0
                cap = {c["card_id"]: len(packs_f6.pack(c["pack"])["outcomes"]) for c in plain}
                for (lo, hi), m in buckets.items():
                    for i in range(round(n * m / tot)):
                        k = rng.randint(lo, hi)
                        if smp == "S1" and k >= COUT_PURE_MIN_K and pure:
                            c = pure[iq % len(pure)]
                            iq += 1
                        elif smp == "S1" and k >= COUT_TABLE_MIN_K:
                            c = tab[it % len(tab)]
                            it += 1
                        else:
                            # repair r1: a card whose pack has enough outcome names for k (no k relaxation later)
                            el = [x for x in plain if cap[x["card_id"]] >= k + 1] or \
                                [max(plain, key=lambda x: cap[x["card_id"]])]
                            c = el[ip % len(el)]
                            ip += 1
                        nei, none = _display(rng, k)                 # advances rng as before (v3f)
                        _gold_slot(rng, k, nei, none, w_abstain)
                        nei, none = sysd.display(k)
                        g = sysd.gold("ch", k, nei, none, w_abstain)
                        specs.append({"sampler": smp, "form": "c_out", "card": c["card_id"], "k": k, "nei": nei,
                                      "none": none, "gold": g})
            elif form == "c_rec":
                tot = sum(CREC_K.values())
                for (lo, hi), m in CREC_K.items():
                    for i in range(round(n * m / tot)):
                        k = rng.randint(lo, hi)
                        nei, none = _display(rng, k)                 # advances rng as before (v3f)
                        _gold_slot(rng, k, nei, none, w_abstain)
                        nei, none = sysd.display(k)
                        g = sysd.gold("ch", k, nei, none, w_abstain)
                        specs.append({"sampler": smp, "form": "c_rec", "card": cs[i % len(cs)]["card_id"], "k": k,
                                      "nei": nei, "none": none, "gold": g})
            elif form == "c_case":
                tot = sum(CCASE_K.values())
                for (lo, hi), m in CCASE_K.items():
                    for i in range(round(n * m / tot)):
                        k = rng.randint(lo, hi)
                        specs.append({"sampler": smp, "form": "c_case", "card": cs[i % len(cs)]["card_id"], "k": k,
                                      "gold": rng.choice(["can", "cannot"])})
            elif form == "c_gap":
                for i in range(n):
                    k = rng.choice([3, 4])
                    w = [w_abstain] + [1.0] * (k - 1)
                    rng.choices(["nothing", "gap"], weights=[w[0], k - 1])     # advances rng as before (v3f)
                    g = sysd.pick(("cgap", k), {"nothing": w[0] / (w[0] + k - 1), "gap": (k - 1) / (w[0] + k - 1)})
                    specs.append({"sampler": smp, "form": "c_gap", "card": cs[i % len(cs)]["card_id"], "k": k,
                                  "gold": g})
            else:
                for i in range(n):
                    specs.append({"sampler": smp, "form": form, "card": cs[i % len(cs)]["card_id"]})
    for i, s in enumerate(specs):
        s["sid"] = f"{set_tag}-{i:06d}"
        s["seed"] = i
    return specs


def yes_rates(cards: list[dict], set_tag: str, profiles: dict | None = None) -> dict:
    """Per yes/no card yes rate U[20, 80], drawn in complementary pairs (r, 1 - r) so the aggregate stays at 50%.
    Repair r1: the pairs are cards of one sampler with the most similar card profile (switch set, question kinds,
    world), so a card-level text feature shared by a pair sits at 50% (G7 raw multi-card features)."""
    rng = rng_for("yesrate", set_tag)
    profiles = profiles or {}
    out = {}
    yn_all = [c for c in cards if c["schema"] == "yn"]
    for smp in sorted({c["sampler"] for c in yn_all}):
        yn = [c for c in yn_all if c["sampler"] == smp]
        left = sorted(yn, key=lambda c: c["card_id"])
        pairs = []
        while len(left) >= 2:
            a = left.pop(0)
            pa = set(profiles.get(a["card_id"], ()))
            best = max(range(len(left)), key=lambda i: (len(pa & set(profiles.get(left[i]["card_id"], ()))) -
                                                        len(pa ^ set(profiles.get(left[i]["card_id"], ()))), -i))
            pairs.append((a, left.pop(best)))
        for a, b in pairs:
            r = rng.uniform(0.2, 0.8)
            out[a["card_id"]] = r
            out[b["card_id"]] = 1 - r
        for c in left:
            out[c["card_id"]] = 0.5
    # repair r1: the drawn rates are permuted among the yes/no cards by gen/rate_assign.py (shared-vocabulary
    # features near 50%); the multiset of drawn rates is unchanged
    import json as _json
    from .common import GEN as _GEN
    p = _GEN / "yesrate_assign.json"
    if set_tag in ("cand", "qc") and p.exists():      # the QC sample uses the same cards, so the same rates
        a = _json.load(open(p))["rates"]
        out.update({k: v for k, v in a.items() if k in out})
    return out


# ---------------------------------------------------------------- S5 mix-tuning dev (400 items; held-out packs and styles)
S5_CELLS = {"qdet": 100, "qest": 50, "qplain": 50, "c_out": 150, "c_gap": 50}
S5_CARDS = {"yn": 5, "c_out": 5, "c_gap": 4}


def plan_dev_cards() -> list[dict]:
    P = packs_f6.packs("heldout")
    out, i = [], 0
    for schema, n in S5_CARDS.items():
        for j in range(n):
            out.append({"card_id": f"F6-S5-{schema}-{j:02d}", "sampler": "S5", "schema": schema,
                        "pack": P[i % len(P)]["pid"]})
            i += 1
    return out


def plan_dev_specs(cards: list[dict]) -> list[dict]:
    rng = rng_for("specs", "dev")
    by = {}
    for c in cards:
        by.setdefault(c["schema"], []).append(c)
    specs = []
    for form, n in S5_CELLS.items():
        cs = by["yn" if form in ("qdet", "qest", "qplain") else form]
        for i in range(n):
            c = cs[i % len(cs)]
            if form == "c_out":
                k = rng.randint(2, 5)
                nei, none = _display(rng, k)
                specs.append({"sampler": "S5", "form": form, "card": c["card_id"], "k": k, "nei": nei, "none": none,
                              "gold": _gold_slot(rng, k, nei, none, 1.0)})
            elif form == "c_gap":
                k = rng.choice([3, 4])
                specs.append({"sampler": "S5", "form": form, "card": c["card_id"], "k": k,
                              "gold": rng.choices(["nothing", "gap"], weights=[1, k - 1])[0]})
            else:
                specs.append({"sampler": "S5", "form": form, "card": c["card_id"]})
    for i, s in enumerate(specs):
        s["sid"] = f"dev-{i:06d}"
        s["seed"] = i
    return specs
