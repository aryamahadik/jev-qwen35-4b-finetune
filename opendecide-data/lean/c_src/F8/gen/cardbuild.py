"""Build one F8 card from a plan cell: rules, names, SEM line sets per version, wordings, styles, row-mix knobs.

Card-level draws happen once, before any row (F8-R1-09, F8-R2-10, F8-R4-C2): label form (plain / masked / swapped),
card version set, SEM lines and their wordings, definition style, few-shot flag, worlds hosted, card yes rate.
"""
from __future__ import annotations

import re
from fractions import Fraction as Fr

import cards as C
import lexicon as L
import packs_f8
from common import rng_for
from fmt1 import labels as flabels
from fmt1 import pool as fpool

MASKED_CARDS = {"tier": 2, "pred": 3, "mat": 1}      # cards per schema with masked names (10-15% of choice rows)
OPEN_PCT_CHOICE = 62                                 # repair r1: per-row open rate on BIN, RANK-top, DEC, INV cards
OPEN_PCT_YN = 45                                     # repair r1: per-row open rate on eligible YN cards
EDGE_TARGET = 0.17                                   # BIN edge rows (15% +/- 3 of BIN rows; flip twins dilute)
FEWSHOT_CARDS = 6                                    # cards with 2-3 worked examples (5-10% of 84)
EXAMPLE_CARDS = 46                                   # cards with >= 1 worked example (about 50%, some fail to fit)
SWAPPED_CARDS = {"tier": 1, "mat": 1}                # about 5% of choice rows
FEWSHOT_RATE = 0.08                                  # 5-10% of cards
EXAMPLES_RATE = 0.45                                 # one-line + example(s) on about 50% of cards (with few-shot)


def _ok_label_set(labels: list) -> bool:
    norm = [re.sub(r"[^a-z0-9]+", " ", x.lower()).strip() for x in labels]
    return len(set(norm)) == len(norm)


def _pick_group(rng, pack, kmin, kmax, need_polar=False):
    groups = [g for g in pack["groups"] if len(g["labels"]) >= kmin and _ok_label_set(g["labels"])]
    if need_polar:
        groups = [g for g in groups if sum(g["pol"][x] in ("adverse", "favourable") for x in g["labels"]) >= 1]
    if not groups:
        return None
    g = rng.choice(groups)
    k = rng.randint(kmin, min(kmax, len(g["labels"])))
    labs = list(g["labels"])
    if need_polar:
        polar = [x for x in labs if g["pol"][x] in ("adverse", "favourable")]
        rest = [x for x in labs if x not in polar]
        rng.shuffle(polar)
        rng.shuffle(rest)
        chosen = polar[:max(1, min(len(polar), k))] + rest
        chosen = chosen[:k]
        labs = [x for x in g["labels"] if x in chosen]
    else:
        labs = sorted(rng.sample(labs, k), key=lambda x: g["labels"].index(x))
    return {"name": g["name"], "labels": labs, "pol": {x: g["pol"][x] for x in labs}}


def _events(pack, pol=None):
    return [e for e in pack["events"] if pol is None or e["pol"] == pol]


def _signs(rng, pack, n=1, exclude=()):
    labs = [f["label"] for f in pack["factors"] if f["label"] not in exclude]
    rng.shuffle(labs)
    return labs[:n]


def _bins(rng, K):
    """K bins over [0, 1]: interior edges on the whole-percent grid (coarse: multiples of 5 where possible)."""
    for _ in range(500):
        if K <= 9:
            step = 5 if K <= 8 else 1
            cand = list(range(step, 100, step))
        else:
            cand = list(range(2, 99, 1))
        edges = sorted(rng.sample(cand, K - 1))
        gaps = [b - a for a, b in zip([0] + edges, edges + [100])]
        if min(gaps) >= (3 if K <= 9 else 2):
            return [Fr(e, 100) for e in edges]
    raise ValueError("bins")


def _mat(rng, pack, cur_places, kc=0):
    nl = rng.choice([3, 4])
    ni = rng.choice([3, 4])
    lik_edges = sorted(rng.sample(range(5, 95, 5), nl - 1))
    lik_edges = [Fr(e, 100) for e in lik_edges]
    base = rng.choice([100, 200, 250, 500, 1000])
    imp = sorted(rng.sample(range(1, 40), ni - 1))
    imp_edges = [Fr(x * base) for x in imp]
    K = rng.choice([3, 4]) if kc == 0 else rng.choice([5, 6])
    if K > nl + ni - 1:
        K = nl + ni - 1
    # rating grid non-decreasing along both axes, every rating used at least once
    for _ in range(2000):
        g = [[0] * ni for _ in range(nl)]
        for i in range(nl):
            for j in range(ni):
                lo = max(g[i - 1][j] if i else 0, g[i][j - 1] if j else 0)
                hi = min(K - 1, lo + rng.choice([0, 0, 1, 1, 2]))
                g[i][j] = rng.randint(lo, hi)
        used = {x for row in g for x in row}
        if used == set(range(K)) and g[0][0] == 0 and g[-1][-1] == K - 1:
            break
    else:
        K = len({x for row in g for x in row})
        remap = {v: i for i, v in enumerate(sorted({x for row in g for x in row}))}
        g = [[remap[x] for x in row] for row in g]
    return {"lik_edges": lik_edges, "lik_conv": "lo" if rng.random() < 0.7 else "hi", "imp_edges": imp_edges,
            "grid": g, "K": K, "lik_names": L.LIKELIHOOD_LEVELS[:nl] if nl == 4 else
            [L.LIKELIHOOD_LEVELS[i] for i in (0, 2, 3)], "imp_names": L.IMPACT_LEVELS[:ni],
            "impact": "loss" if rng.random() < 0.6 else "expected"}


def _names(rng, card, base_names: list, kind: str):
    """Plain names, masked codes (fmt1 labels.masked_ids, LR04/LR05) or swapped words (LR07-LR09)."""
    K = len(base_names)
    form = card["label_form"]
    if form == "masked":
        scheme = rng.choice(["MS01", "MS03", "MS05", "MS12", "MS16", "MS17"])
        ids = flabels.masked_ids(scheme, K, card["card_id"] + kind)
        rank = [int(re.sub(r"\D", "", x) or 0) for x in ids]
        return ids, rank
    if form == "swapped" and kind in ("tier", "rating"):
        words = flabels.swapped_names("group", K, card["card_id"] + kind, order=list(range(K)),
                                      groups=["severity", "priority", "risk", "quality"],
                                      exclude=[n for n in base_names])
        wr = {w["word"].lower(): w.get("rank") or 0 for w in fpool.swap_words()}
        rank = [wr.get(w.lower(), 0) for w in words]
        return words, rank
    return list(base_names), None


def _wordings(rng, card, concepts):
    allw = C.wordings()
    qtype = "noul" if card["schema"] == "yn" else "choice"
    ok = [w for w in allw if C.wording_ok(w, qtype, concepts)]
    if card.get("q", {}).get("k") != "risk":
        # 'risk' appears only on rows that render SEM-22 (G0 1 quantity lexicon; lint)
        ok = [w for w in ok if not re.search(r"\brisk", w["text"], re.I)]
    rng.shuffle(ok)
    k = rng.randint(5, 7)
    return [w["id"] for w in ok[:k]]


def _styles(rng, card):
    conts = C.SAMPLER_CONTAINERS[card["sampler"]]
    held = card["sampler"] == "S5"
    st = [s for s in (fpool.styles(held_out=True) if held else fpool.styles()) if s["container"] in conts]
    st = [s for s in st if s["skin"] not in ("json.array", "json.lines")]
    rng.shuffle(st)
    return [s["id"] for s in st[:14]]


def build_card(cell: dict) -> dict:
    rng = rng_for("card", cell["card_id"])
    pack = packs_f8.by_id()[cell["pack"]]
    card = dict(cell)
    sch, sub = cell["schema"], cell["sub"]
    card["doc_word"] = rng.choice(L.DOC_WORDS[cell["sampler"]])
    card["id_width"] = 2 if sch == "rank_order" else 4
    card["cur"] = pack["currency"]
    card["persona_seed"] = (pack["persona_seed"] or {}).get("onet_code") if isinstance(pack["persona_seed"], dict) \
        else pack["persona_seed"]
    card["case"] = pack["case"]
    rules = {}
    R = card
    R["label_form"] = "plain"
    # ------------------------------------------------------------------ quantity / content by schema
    if sch in ("yn", "inv") and sub == "points" or sch == "tier":
        sc = C.make_scorecard(rng, pack, n_lines=rng.randint(4, 6) if sch in ("tier", "inv") else None)
        rules["scorecard"] = sc
        R["q"] = {"k": "score"}
    if sch == "tier":
        K = rng.choice([3, 4]) if cell.get("kc", 0) == 0 else rng.choice([5, 6])
        while True:
            try:
                rules["cuts"] = C.make_cut_table(rng, rules["scorecard"], K)
                break
            except ValueError:
                rules["scorecard"] = C.make_scorecard(rng, pack, n_lines=rng.randint(4, 6))
        base = C.tier_names(rng, pack, K, "tier")
        R["tier_base"] = base
        rules["only_if"] = {}
        for t in rng.sample(range(1, K), min(K - 1, rng.choice([1, 2]))):
            rules["only_if"][t] = C.make_cond(rng, pack, nparts=rng.choice([1, 1, 2]), kinds=("bool", "bool", "cat",
                                                                                                "amt"))
        rules["overrides"] = []
        for _ in range(rng.choice([1, 1, 2])):
            rules["overrides"].append({"cond": C.make_cond(rng, pack, nparts=rng.choice([1, 2]),
                                                           kinds=("bool", "cat", "amt")),
                                       "tier": rng.randrange(1, K)})
    if sch in ("yn", "bin", "pred") and sub == "bayes":
        if sch == "pred":
            K = rng.choice([3, 4]) if cell.get("kc", 0) == 0 else rng.choice([5, 6])
            g = _pick_group(rng, pack, K, K) or _pick_group(rng, pack, 3, 6)
        else:
            g = _pick_group(rng, pack, 2, 3, need_polar=(sch == "yn"))
        R["hyp"] = g
        R["signs"] = _signs(rng, pack, 2)
        if cell["sampler"] == "S5" and sch in ("yn", "pred"):
            R["two_signs"] = True                 # two-stage evidence with SEM-26 independence (8.5)
        R["data_forms"] = ["counts"] if cell["sampler"] == "S3" else (
            ["rates", "counts", "nE"] if sch == "pred" else ["counts", "counts", "nE", "joint", "rates"])
        R["q"] = {"k": "post"}
    if sch == "bin":
        # repair r1 (option-count plan, 1): S3 cards are fine (K = 10-18); the other BIN cards alternate coarse K = 3
        # (n = 3 closed / 4 open, both 2-4) and K = 5-8 (n <= 9 open), so the BIN plan 62 / 62 / 101 holds
        fine = cell["sampler"] == "S3"
        K = rng.randint(10, 18) if fine else (3 if cell.get("kc", 0) == 0 else rng.randint(5, 8))
        rules["bins"] = _bins(rng, K)
        rules["bin_conv"] = "lo" if rng.random() < 0.7 else "hi"
    if sub == "expected" and sch in ("yn", "inv", "dec"):
        ev = _events(pack, "adverse") or pack["events"]
        R["events"] = [e["label"] for e in ev]
        if sch == "dec":
            R["mode"] = "loss"
            R["q"] = {"k": "tec"}
            # DEC actions: the pack's actions plus its decision outcomes (5-9 option rows need >= 5 actions)
            acts = list(pack["actions"])
            have = {a["label"].lower() for a in acts}
            for g in pack["groups"]:
                if g["name"] == "outcome":
                    for lab in g["labels"]:
                        if lab.lower() not in have:
                            acts.append({"label": lab, "pol": "neutral", "defn": None})
                            have.add(lab.lower())
            R["actions"] = acts
        elif sch == "inv":
            R["mode"] = "loss"
            R["q"] = rng.choice([{"k": "el"}, {"k": "el"}, {"k": "tec"}])
        else:
            kind = rng.choices(["el", "tec", "ev", "en"], [45, 20, 20, 15])[0]
            R["mode"] = "net" if kind == "ev" else "loss"
            R["q"] = {"k": kind}
            if kind == "en":
                R["units"] = rng.choice(L.UNIT_WORDS)
        if R["q"]["k"] in ("tec",):
            R["actions"] = pack["actions"]
    if sub == "rank":
        ev = _events(pack, "adverse") or pack["events"]
        R["events"] = [e["label"] for e in ev]
        R["mode"] = "loss"
        if sch == "mat":
            rules["mat"] = _mat(rng, pack, 0, cell.get("kc", 0))
            R["q"] = {"k": "rating"}
        else:
            d = rng.choice(["el", "chance", "el", "chance"] + (["score"] if sch == "rank_top"
                                                               and len(pack["factors"]) >= 5 else []))
            R["q"] = {"k": "risk", "def": d}
            if d == "score":
                rules["scorecard"] = C.make_scorecard(rng, pack, n_lines=rng.randint(4, 6))
    if sch == "yn" and sub == "points" or (sch == "inv" and sub == "points" and rng.random() < 0.4):
        # action rules (SEM-31): at most one rule per action (F8-R4-03)
        acts = [a for a in pack["actions"]]
        rng.shuffle(acts)
        ar = {}
        for a in acts[:rng.choice([1, 2])]:
            kinds = ("bool", "bool", "cat", "amt")
            c = C.make_cond(rng, pack, nparts=rng.choice([1, 2, 2, 3]), kinds=kinds)
            if rng.random() < 0.35 and "scorecard" in rules:
                # one quantity comparison on the score (F < v < M, never a cut point)
                sc = rules["scorecard"]
                v = rng.randint(sc["F"] + 1, sc["M"] - 1)
                op = rng.choice(C.CMP_OPS)
                c["parts"] = c["parts"][:2] + [{"t": "q", "q": {"k": "score"}, "op": op, "v": Fr(v),
                                                "w": C.cmp_word(rng, op)}]
                if len(c["parts"]) == 1:
                    c["conn"] = "and"
                elif c["conn"] == "xor1":
                    c["conn"] = "and"
            ar[a["label"]] = c
        rules["arules"] = ar
        R["act_pol"] = {a["label"]: a["pol"] for a in pack["actions"]}
    if sch == "inv":
        # INV rules are quantity comparisons (type (a)); chance-only INV rules are not used because no named error
        # other than E5 applies to them, so half of their gold slots could never carry a named-error distractor
        rules.pop("arules", None)
        if R["q"].get("k") == "risk":
            R["q"] = {"k": "risk", "def": "el"}
        R["inv_kind"] = "q"
        if R["inv_kind"] == "act":
            a = rng.choice(list(rules["arules"]))
            rules["inv"] = {"kind": "act", "action": a}
        else:
            qk = R["q"]["k"] if R["q"]["k"] != "risk" else R["q"]["def"]
            # inclusive comparisons: a qualifying case planted exactly on the value gives the E5 distractor
            op = rng.choice([">=", "<="]) if qk == "score" else ">="
            if qk == "score":
                sc = rules["scorecard"]
                v = Fr(rng.randint(sc["F"] + 2, sc["M"] - 2))
            elif qk in ("el", "tec"):
                v = Fr(rng.choice([500, 750, 1000, 1200, 1500, 2000, 2500, 3000, 4000, 5000]))
            else:
                v = Fr(rng.randint(10, 60), 100)
            rules["inv"] = {"kind": "q", "q": {"k": qk}, "op": op, "v": v, "w": C.cmp_word(rng, op)}
    R["rules"] = rules
    # ------------------------------------------------------------------ label form (per card, F8-R2-10)
    return card


def assign_label_forms(cards: list) -> None:
    """Masked names on about 12% and swapped names on about 5% of choice rows (10.1), met by choosing cards (per card,
    never per row, F8-R2-10): masking covers tier, rating and outcome names; swapping covers tier and rating names."""
    rng = rng_for("labelforms")
    choice_rows = sum(c.get("n_cand", 0) for c in cards if c["schema"] != "yn")
    for form, schemas, share in (("swapped", ("tier", "mat"), 5), ("masked", ("tier", "mat", "pred"), 12)):
        cand = [c for c in cards if c["schema"] in schemas and c["label_form"] == "plain"]
        rng.shuffle(cand)
        target = choice_rows * share // 100
        got = 0
        for c in sorted(cand, key=lambda c: c.get("n_cand", 0)):
            if got >= target:
                break
            if got + c.get("n_cand", 0) > target * 11 // 10 and got > 0:
                continue
            c["label_form"] = form
            got += c.get("n_cand", 0)


def finish_card(card: dict) -> None:
    """Names, versions, SEM sets, definition style, wordings and styles (after label forms are assigned)."""
    rng = rng_for("cardfinish", card["card_id"])
    sch = card["schema"]
    if sch == "tier":
        names, rank = _names(rng, card, card["tier_base"], "tier")
        card["rules"]["tiers"] = names
        card["rules"]["name_rank"] = rank
    if sch == "mat":
        m = card["rules"]["mat"]
        base = [w[:1].upper() + w[1:] for w in rng.sample(L.RATING_WORDS, m["K"])]
        base = sorted(base, key=lambda w: L.RATING_WORDS.index(w.lower()))
        names, rank = _names(rng, card, base, "rating")
        m["ratings"] = names
        card["rules"]["name_rank"] = rank
    if sch == "pred":
        hyp = card["hyp"]
        if card["label_form"] == "masked":
            codes, _ = _names(rng, card, hyp["labels"], "outcome")
            card["hyp_display"] = codes
            card["hyp_defs"] = {c: l for c, l in zip(codes, hyp["labels"])}
        else:
            card["hyp_display"] = list(hyp["labels"])
    elif card.get("hyp"):
        card["hyp_display"] = list(card["hyp"]["labels"])
    # worlds hosted (per card; rows draw their world, F8-R1-15)
    # repair r1 (G10 world mode): every eligible card hosts open rows; the per-row rate is set so open rows are about
    # 25% of all choice rows (BIN, RANK-top, DEC and INV only) and about 15% of YN rows, counted by each row's own world
    if sch in ("bin", "rank_top", "dec", "inv"):
        card["open_pct"] = OPEN_PCT_CHOICE
    elif sch == "yn" and card["sub"] in ("points", "bayes", "expected") and card["q"]["k"] != "en":
        card["open_pct"] = OPEN_PCT_YN
    else:
        card["open_pct"] = 0
    card["open_rate"] = card["open_pct"]
    # versions: full always; short or none on some cards (about 15% of rows overall)
    card["versions"] = ["full"]
    card["short_rate"] = 0.0
    if rng.random() < 0.36:
        card["versions"].append("none" if (card["sub"] != "points" and sch not in ("mat", "tier", "inv")
                                           and rng.random() < 0.5) else "short")
        card["short_rate"] = 0.42
    # definition style (10.4; formats-1 DS names); which cards carry worked examples is planned family-wide in
    # assign_examples (repair r1, G11: few-shot 5-10% of cards, one-line + examples on about 50%)
    card["defs_style"] = rng.choice(["one_line", "decision_list", "rubric_table"]) \
        if sch in ("tier", "mat") else rng.choice(["one_line", "decision_list"])
    card["fewshot"] = 0
    card["fewshot_template"] = rng.choice(["FT01", "FT02", "FT03", "FT05", "FT08", "FT11"])
    if sch == "yn":
        card["sem_variant"] = {k: rng.randrange(len(v)) for k, v in L.SEM.items()}
    else:
        # choice rows print instructions twice: use the most compact wording of each SEM line (1 choice-row layout)
        card["sem_variant"] = {k: min(range(len(v)), key=lambda i: len(v[i])) for k, v in L.SEM.items()}
    card["flip_incl"] = {k: (rng.random() < 0.85) for k in ("SEM-04", "SEM-05", "SEM-07", "SEM-11", "SEM-14",
                                                             "SEM-15", "SEM-16", "SEM-17", "SEM-20", "SEM-21",
                                                             "SEM-24", "SEM-28", "SEM-18", "SEM-23")}
    if sch != "yn":
        # multi-entity and tier rows almost never stay invariant to these readings: the lines are always rendered
        for k in ("SEM-04", "SEM-07", "SEM-14", "SEM-16", "SEM-20", "SEM-21", "SEM-24"):
            card["flip_incl"][k] = True
    card["flip_keep"] = sch != "yn"
    concepts = {"points"} if card["sub"] == "points" or sch == "tier" else {"chance"}
    if card.get("q", {}).get("def") == "score":
        concepts = {"points"}
    card["wordings"] = _wordings(rng, card, concepts)
    card["styles"] = _styles(rng, card)
    card["yes_rate"] = Fr(1, 2)          # set per card in assign_yes_rates (antithetic pairs, 20-80%)
    card["reps"] = rng.sample(["pct0", "pct1", "dec", "frac", "ain", "aoutof"], 4)
    card["t_reps"] = ["pct0", "pct1", "frac"]
    card["frac_denoms"] = sorted(rng.sample([4, 5, 8, 10, 20, 25, 40, 50], 4))
    card["attack_rows"] = False          # blocked on the named shared attack pool (F8-R2-19; tmp/repair/INFEASIBLE_G10_attack.md)
    fit_length(card)
    if sch == "tier":
        _tier_fit(card)
    if sch == "bin":
        # edge rows are drawn on closed full-card rows only: rate = 15% / (share of BIN rows that are closed and full)
        full = 1 - (card["short_rate"] if len(card["versions"]) > 1 else 0)
        K = len(card["rules"]["bins"]) + 1
        openr = 0 if K >= 19 else card["open_pct"] / 100
        cf = max(0.05, full * (1 - openr))
        card["edge_k"] = max(1, min(14, int(round(20 * EDGE_TARGET / cf))))


def card_chars(card: dict) -> int:
    import render as RD
    from fmt1 import card as fcard
    ir = RD.card_ir(card, "full")
    return max(len(fcard.render_card(ir, fpool.style(sid))) for sid in card["styles"][:3]) if ir else 0


def fit_length(card: dict, salt=None) -> None:
    """A card version whose block is too long for rows to stay under 2,000 counted tokens is rebuilt at creation
    (1 choice-row layout): drop optional lines first, then when-it-flips lines (rows must then be invariant)."""
    budget = 5200 if card["schema"] == "yn" else 2600
    order = ["SEM-28", "SEM-18"] + ([] if card.get("flip_keep") else
                                    ["SEM-20", "SEM-24", "SEM-21", "SEM-16", "SEM-04", "SEM-07", "SEM-14"])
    for k in order:
        if card_chars(card) <= budget:
            break
        card["flip_incl"][k] = False
    rng = rng_for("fitlen", card["card_id"]) if salt is None else rng_for("fitlen", card["card_id"], salt)
    pack = packs_f8.by_id()[card["pack"]]
    tries = 0
    while card_chars(card) > budget and card["rules"].get("scorecard") and tries < 40:
        tries += 1
        R = card["rules"]
        sc = C.make_scorecard(rng, pack, n_lines=4)
        if R.get("cuts") is not None:
            try:
                R["cuts"] = C.make_cut_table(rng, sc, len(R["tiers"]))
            except ValueError:
                continue
            if len(R.get("overrides") or []) > 1:
                R["overrides"] = R["overrides"][:1]
            for t in list(R.get("only_if") or {})[1:]:
                del R["only_if"][t]
        if R.get("inv") and R["inv"]["kind"] == "q" and R["inv"]["q"]["k"] == "score":
            R["inv"]["v"] = Fr(rng.randint(sc["F"] + 1, sc["M"] - 1))
        R["scorecard"] = sc
    card["chars"] = card_chars(card)


def _median_score_rule(card: dict) -> None:
    """INV score rules: the comparison value sits at the median score of drawn cases, so meeting and failing cases
    are both common (strictly inside the floor and cap)."""
    import samplers as SP
    from solver_a import CV, quantity
    r = card["rules"]["inv"]
    if r["kind"] != "q" or r["q"]["k"] != "score":
        return
    rng = rng_for("invmedian", card["card_id"])
    pack = packs_f8.by_id()[card["pack"]]
    sc = card["rules"]["scorecard"]
    S = {"form": "inv", "sub": "points", "rules": card["rules"], "ents": [], "q": {"k": "score"}}
    vals = []
    for i in range(300):
        e = SP.points_ent(rng, card, pack, f"X-{1000 + i}", version="short", p_true=[25, 45, 65][i % 3])
        vals.append(int(quantity(S, e, {"k": "score"}, CV())))
    vals.sort()
    v = vals[len(vals) // 2]
    v = min(max(v, sc["F"] + 1), sc["M"] - 1)
    r["v"] = Fr(v)


def _tier_feas(card: dict, n: int = 3000) -> dict:
    """(tier, step) -> count of drawn fact sets (same draw as samplers._tier_pool); used only at card creation."""
    import samplers as SP
    pack = packs_f8.by_id()[card["pack"]]
    rng = rng_for("tierfeas", card["card_id"], card.get("_tier_try", 0))
    card.pop("_tier_pool", None)
    card.pop("_tier_pool_n", None)
    pool = SP._tier_pool(card, pack, {"version": "full"}, rng, n=n)
    card.pop("_tier_pool", None)
    card.pop("_tier_pool_n", None)
    return {k: len(v) for k, v in pool.items()}


def _tier_ok(card: dict, cnt: dict) -> tuple:
    K = len(card["rules"]["tiers"])
    F = {t: [s for s in (None, "only_if", "override") if cnt.get((t, s), 0) >= 12] for t in range(K)}
    dec = sum(1 for t in range(K) if any(x is not None for x in F[t]))
    return all(F[t] for t in range(K)) and dec / K >= 0.5, F


def _tier_fit(card: dict) -> None:
    """Repair r1 (G10 TIER): a TIER card's rules are redrawn at creation (before any row) until every tier is
    constructible and an only-if or override step can decide at least half of its tiers (XF08: >= 50% of TIER rows
    decisive). The planner then plans (tier, step) only from this feasibility map, so the gold tier is uniform per card
    and every tier with a feasible decisive step is planned decisive. K keeps its option-count class (3-4 or 5-6)."""
    import copy as _copy
    pack = packs_f8.by_id()[card["pack"]]
    best = None
    lo = 5 if card.get("kc", 0) else 3
    for i in range(200):
        card["_tier_try"] = i
        ok, F = _tier_ok(card, _tier_feas(card))
        K = len(card["rules"]["tiers"])
        if ok:
            card["_tier_F"] = {t: v for t, v in F.items()}
            return
        if all(F[t] for t in range(K)):
            dec = sum(1 for t in range(K) if any(x is not None for x in F[t])) / K
            if best is None or dec > best[0]:
                best = (dec, _copy.deepcopy(card["rules"]), F)
        rng = rng_for("tierredraw", card["card_id"], i)
        R = card["rules"]
        if i and i % 100 == 0 and K > lo:
            K -= 1
            names, rank = _names(rng_for("tiernames", card["card_id"], K), card, card["tier_base"][:K], "tier")
            R["tiers"], R["name_rank"] = names, rank
            best = None
        big = K >= 5
        R["scorecard"] = C.make_scorecard(rng, pack, n_lines=4 if big else rng.randint(4, 5))
        for _ in range(50):
            try:
                R["cuts"] = C.make_cut_table(rng, R["scorecard"], K)
                break
            except ValueError:
                R["scorecard"] = C.make_scorecard(rng, pack, n_lines=4 if big else rng.randint(4, 5))
        R["only_if"] = {}
        for t in rng.sample(range(1, K), 2 if big else min(K - 1, rng.choice([1, 2]))):
            R["only_if"][t] = C.make_cond(rng, pack, nparts=1 if big else rng.choice([1, 1, 2]),
                                          kinds=("bool", "bool", "cat", "amt"))
        R["overrides"] = []
        for _ in range(2 if big else rng.choice([1, 1, 2])):
            R["overrides"].append({"cond": C.make_cond(rng, pack, nparts=1 if big else rng.choice([1, 2]),
                                                       kinds=("bool", "cat", "amt")),
                                   "tier": rng.randrange(1, K)})
        fit_length(card, salt=i)
    if best is None:
        raise ValueError(f"TIER card {card['card_id']}: no feasible rule draw")
    card["rules"] = best[1]
    card["_tier_F"] = {t: v for t, v in best[2].items()}


def assign_yes_rates(cards: list) -> None:
    """Per-card yes rates drawn uniformly from 20-80% (2.1) as antithetic pairs (r, 100 - r) over YN cards that share
    sub-skill, action rules, open-world hosting, card versions and size class, so every aggregate cell is 50%."""
    rng = rng_for("yesrates")
    yn = [c for c in cards if c["schema"] == "yn"]
    yn.sort(key=lambda c: (c["sub"], bool(c["rules"].get("arules")), c.get("open_pct", 0) > 0,
                           len(c["versions"]) > 1, c.get("size"), c["card_id"]))
    for i in range(0, len(yn) - 1, 2):
        r = rng.randint(4, 16) * 5
        yn[i]["yes_rate"] = Fr(r, 100)
        yn[i + 1]["yes_rate"] = Fr(100 - r, 100)
    if len(yn) % 2:
        yn[-1]["yes_rate"] = Fr(1, 2)


def assign_examples(cards: list) -> None:
    """Worked examples planned family-wide (10.4; G11): FEWSHOT_CARDS YN cards get 2-3 examples (few-shot cards);
    more cards get one example, up to EXAMPLE_CARDS cards with >= 1 example. Choice cards of forms whose option lists
    are too long to repeat (RANK-order, INV) or whose card block is near the budget are never chosen."""
    rng = rng_for("examplesplan")
    yn = sorted([c for c in cards if c["schema"] == "yn"], key=lambda c: c["card_id"])
    ch = sorted([c for c in cards if c["schema"] not in ("yn", "rank_order", "inv") and c.get("chars", 0) <= 2300],
                key=lambda c: c["card_id"])
    rng.shuffle(yn)
    rng.shuffle(ch)
    few = yn[:FEWSHOT_CARDS]
    rest = yn[FEWSHOT_CARDS:] + ch
    one = rest[:max(0, EXAMPLE_CARDS - len(few))]
    for c in few:
        c["defs_style"] = "one_line_examples"
        c["fewshot"] = rng.choice([2, 3])
    for c in one:
        c["defs_style"] = "one_line_examples"
        c["fewshot"] = 1
    for c in few + one:
        fit_length(c)


def build_all(cells: list) -> list:
    cards = [build_card(c) for c in cells]
    assign_label_forms(cards)
    for c in cards:
        finish_card(c)
        if c["schema"] == "inv":
            _median_score_rule(c)
    assign_examples(cards)
    assign_yes_rates(cards)
    return cards
