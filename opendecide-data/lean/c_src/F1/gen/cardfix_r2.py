"""Repair r2 card patch, applied at card load after yplan (deterministic; nothing here reads a row's gold).

1. Longest option per gold source (G0 8 A28: "longest option is gold within +/- 2 pp of 1/k, overall, per gold source
   and per bucket"). On Q1 rows the options are the card's outcome names plus the CBD label, the same on every row of a
   card, so which role holds the longest option is a card property. In r1.1 the CBD label (20-27 characters) was the
   longest option on 67% of the rows that show it and the default outcome on 7% (r1.1 candidates: CBD-source rows
   longest-gold +49 pp, D -11 pp on Q1). Here, on Q1 cards only, the CBD label is chosen from label variants of
   different lengths and the default outcome is re-chosen among the card's plain outcomes (never the escalate, M or
   fallback outcome), so that, weighted by the card's expected gold-source counts, each source's longest-gold rate is
   close to its mean 1/k. Every outcome keeps its name, meaning and valence; only which plain outcome the card names
   as the default changes. Expected counts come from the r1.1 build (cardfix_r2_counts.json, counts only).
2. Rows per card (G0 8 amendment shares 0 / 1 / 2 / 3 = 35 / 30 / 20 / 15%). Notice-free cards give 0 notices on
   every row and held 41.6% of the planned rows, above the 35% target for 0. The planned rows per card are refitted
   (iterative proportional fitting from the r1 plan) to the sampler totals, the question-type totals and a 33% share of
   rows on notice-free cards. Per-card yes rates are unchanged (yplan runs on the r1 plan before this patch).
"""
from __future__ import annotations

import itertools
import json
import os
import random

from cards import QTYPE_ROWS, SAMPLER_ROWS

# CBD label variants (card-level placeholder `<CBD label>`, G0 6; read from statement 38 by both parsers)
CBD_VARIANTS = ["unclear", "undecided", "unsettled", "unresolved", "undetermined", "unclear on file",
                "cannot be determined", "undetermined from the file", "the file does not settle it"]
# r2 pass B: "unclear" / "undecided" / "unsettled" added: on masked and swapped cards the option names are 4-11
# characters, so every earlier CBD label (>= 10) was the longest option there (pass A: MANY-source rows -5.5 pp)
NOTICE_FREE_SHARE = 0.33
# Q2 cards whose text leaves room for 20+ options under the 2,000-token cap (card fit <= 1,700 tokens; the r2 smoke
# showed the longer Q2 cards fail the cap on every 20-option draw): they draw 85% of their rows with 20-23 options
# and carry half of the Q2 rows (G0 1.1: half the Q2 rows 10-19 options, half 20-60)
Q2_BIG_FIT = 1730
# r2 pass B: the cards that produced 20+ option rows on the first pass B run (C006, C049, C058 failed the length cap on
# every 20-option draw although their fit is <= 1,730); they take 128 rows each and the other Q2 cards share the rest
# of the Q2 rows (no other card's planned rows change, so the y plan and the other cards' shards are unaffected)
Q2_BIG_CARDS = ("F1-C007", "F1-C011", "F1-C012", "F1-C015", "F1-C107")
Q2_BIG_SHARE = 0.95
Q2_A22 = True   # r3: see tmp/repair/INFEASIBLE_length.md (A22)
Q2_BIG_ROWS = 0.65
SEED = 20261006
SOURCES_W = {"CBD": 1.0, "D": 1.0, "ONE": 1.0, "MANY": 1.5, "mixed": 1.0, "T": 12.0, "F": 0.2}


def _counts():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cardfix_r2_counts.json")
    return json.load(open(p)) if os.path.exists(p) else None


def _ok_label(card, lab):
    names = [str(card["display"][o]).lower() for o in card["outcomes"]] + [str(card["subj"]).lower()]
    lab_l = lab.lower()
    return all(lab_l != n and lab_l not in n and n not in lab_l for n in names)


def _p_longest(card, default, cbd, src_n, fallback=None):
    """Per gold source: P(gold option is the longest | source) on this card (ties share credit), and 1/k."""
    disp = card["display"]
    keys = list(card["outcomes"]) + (["__CBD__"] if card["world"] == "open" else [])
    L = {o: len(disp[o]) for o in card["outcomes"]}
    if card["world"] == "open":
        L["__CBD__"] = len(cbd)
    m = max(L.values())
    ties = [o for o in keys if L[o] == m]
    share = {o: (1.0 / len(ties) if o in ties else 0.0) for o in keys}
    k = len(keys)
    N = sum(src_n.values())
    fb, esc = (fallback or card.get("fallback")), card.get("escalate")
    # rule-source gold over outcomes: per-option slot share N/k minus what D / F / T already give that outcome
    w = {}
    for o in card["outcomes"]:
        if o == card.get("M"):
            continue
        x = N / k
        if o == default:
            x -= src_n.get("D", 0)
        if o == fb:
            x -= src_n.get("F", 0)
        if o == esc and card.get("tie") == "esc":
            x -= src_n.get("T", 0)
        w[o] = max(0.3, x)
    tw = sum(w.values())
    p_rule = sum(share[o] * w[o] for o in w) / tw
    if card.get("tie") == "strict" and card.get("strict"):
        least = card["strict"][-1]
        tset = [o for o in card["outcomes"] if o != least and o != card.get("M")]
        p_t = sum(share[o] for o in tset) / len(tset)
    else:
        p_t = share.get(esc, 0.0)
    out = {"CBD": share.get("__CBD__", 0.0), "D": share[default], "F": share[fb] if fb else 0.0, "T": p_t,
           "ONE": p_rule, "MANY": p_rule, "mixed": p_rule}
    return out, 1.0 / k


def _objective(state, cards, cnt, const):
    acc = {s: [const.get(s, [0, 0, 0])[0], const.get(s, [0, 0, 0])[1], const.get(s, [0, 0, 0])[2]] for s in SOURCES_W}
    for c in cards:
        src_n = cnt.get(c["card_id"], {})
        st = state[c["card_id"]]
        d, cbd = st[0], st[1]
        fbk = st[2] if len(st) > 2 else None
        p, ik = _p_longest(c, d, cbd, src_n, fbk)
        for s in SOURCES_W:
            n = src_n.get(s, 0)
            acc[s][0] += n * p[s]
            acc[s][1] += n * ik
            acc[s][2] += n
    tot = 0.0
    dev = {}
    for s, (a, b, n) in acc.items():
        if n:
            dv = (a - b) / n
            dev[s] = round(100 * dv, 2)
            tot += SOURCES_W[s] * (n / 100.0) * dv * dv
    return tot, dev


def plan_longest(cards):
    C = _counts()
    if C is None:
        return {}, {}
    cnt, const = C["q1_sources"], C["q2q4_longest"]
    q1 = sorted([c for c in cards if c["qtype"] == "Q1" and c["card_id"] in cnt], key=lambda c: c["card_id"])
    choices = {}
    for c in q1:
        elig = [o for o in c["outcomes"] if c["roles"][o] in ("default", "other")]
        labs = [x for x in CBD_VARIANTS if _ok_label(c, x)] if c["world"] == "open" else [c["cbd_label"]]
        if c["world"] == "open" and c["cbd_label"] not in labs:
            labs.append(c["cbd_label"])
        choices[c["card_id"]] = list(itertools.product(elig, labs))
    orig = {c["card_id"]: (c["default"], c["cbd_label"]) for c in q1}
    state = dict(orig)
    rng = random.Random(SEED)

    def score(st):
        v, _ = _objective(st, q1, cnt, const)
        return v + 1e-4 * sum(1 for x in st if st[x] != orig[x])   # a small cost per changed card

    best = score(state)
    _, before = _objective(state, q1, cnt, const)
    for sweep in range(12):
        order = list(q1)
        rng.shuffle(order)
        changed = False
        for c in order:
            cid = c["card_id"]
            cur = state[cid]
            for ch in choices[cid]:
                if ch == cur:
                    continue
                state[cid] = ch
                v = score(state)
                if v < best - 1e-12:
                    best, cur, changed = v, ch, True
                state[cid] = cur
        if not changed:
            break
    _, dev = _objective(state, q1, cnt, const)
    return state, {"model_dev_pp_before": before, "model_dev_pp_after": dev}


def refit_rows(cards):
    """IPF of n_rows on three margins (sampler totals, question-type totals, notice-free share), from the r1 plan."""
    w = {c["card_id"]: float(c["n_rows"]) for c in cards}
    total = sum(w.values())
    qtot = {q: total * f for q, f in QTYPE_ROWS.items()}
    stot = {s: total * v / sum(SAMPLER_ROWS.values()) for s, v in SAMPLER_ROWS.items()}
    nf_t = total * NOTICE_FREE_SHARE
    for _ in range(200):
        for s, t in stot.items():
            cs = [c for c in cards if c["sampler"] == s]
            f = t / sum(w[c["card_id"]] for c in cs)
            for c in cs:
                w[c["card_id"]] *= f
        for q, t in qtot.items():
            cs = [c for c in cards if c["qtype"] == q]
            f = t / sum(w[c["card_id"]] for c in cs)
            for c in cs:
                w[c["card_id"]] *= f
        q2 = [c for c in cards if c["qtype"] == "Q2"]
        q2b = [c for c in q2 if (c.get("fit_tokens") or 9999) <= Q2_BIG_FIT]
        if q2b:
            t2 = sum(w[c["card_id"]] for c in q2)
            fb = Q2_BIG_ROWS * t2 / sum(w[c["card_id"]] for c in q2b)
            fo = (1 - Q2_BIG_ROWS) * t2 / sum(w[c["card_id"]] for c in q2 if c not in q2b)
            for c in q2:
                w[c["card_id"]] *= fb if c in q2b else fo
        nf = [c for c in cards if "notices" not in c["constructs"]]
        f_nf = nf_t / sum(w[c["card_id"]] for c in nf)
        f_n = (total - nf_t) / sum(w[c["card_id"]] for c in cards if "notices" in c["constructs"])
        for c in cards:
            w[c["card_id"]] *= f_nf if "notices" not in c["constructs"] else f_n
        for c in cards:
            w[c["card_id"]] = min(128.0, max(24.0, w[c["card_id"]]))
    out = {cid: int(round(x)) for cid, x in w.items()}
    q2 = [c["card_id"] for c in cards if c["qtype"] == "Q2"]
    big = [cid for cid in q2 if cid in Q2_BIG_CARDS]
    if big:
        tot = sum(out[cid] for cid in q2)
        rest = [cid for cid in q2 if cid not in Q2_BIG_CARDS]
        left = tot - 128 * len(big)
        sw = sum(out[cid] for cid in rest)
        for cid in big:
            out[cid] = 128
        for cid in rest:
            out[cid] = max(24, int(round(out[cid] * left / sw)))
    return out


def search_longest(cards, restarts=24, seed=SEED):
    """Random-restart coordinate descent over the per-card (default, CBD label) choices (offline; the result is saved
    to cardfix_r2_plan.json, which apply() reads)."""
    C = _counts()
    cnt, const = C["q1_sources"], C["q2q4_longest"]
    q1 = sorted([c for c in cards if c["qtype"] == "Q1" and c["card_id"] in cnt], key=lambda c: c["card_id"])
    choices = {}
    for c in q1:
        elig = [o for o in c["outcomes"] if c["roles"][o] in ("default", "other")]
        labs = [x for x in CBD_VARIANTS if _ok_label(c, x)] if c["world"] == "open" else [c["cbd_label"]]
        if c["world"] == "open" and c["cbd_label"] not in labs:
            labs.append(c["cbd_label"])
        fbs = [None]
        if c.get("fallback"):
            fbs = [o for o in c["outcomes"] if c["roles"][o] in ("fallback", "other", "default")]
        choices[c["card_id"]] = [(d, lab, f) for d, lab, f in itertools.product(elig, labs, fbs)
                                 if f is None or f != d]
    orig = {c["card_id"]: (c["default"], c["cbd_label"], c.get("fallback")) for c in q1}

    def score(st):
        v, _ = _objective(st, q1, cnt, const)
        return v + 1e-4 * sum(1 for x in st if st[x] != orig[x])

    rng = random.Random(seed)
    best_all, best_state = None, None
    for rs in range(restarts):
        state = dict(orig) if rs == 0 else {cid: rng.choice(ch) for cid, ch in choices.items()}
        best = score(state)
        for sweep in range(15):
            order = list(q1)
            rng.shuffle(order)
            changed = False
            for c in order:
                cid = c["card_id"]
                cur = state[cid]
                for ch in choices[cid]:
                    if ch == cur:
                        continue
                    state[cid] = ch
                    v = score(state)
                    if v < best - 1e-12:
                        best, cur, changed = v, ch, True
                    state[cid] = cur
            if not changed:
                break
        if best_all is None or best < best_all:
            best_all, best_state = best, dict(state)
    _, before = _objective(orig, q1, cnt, const)
    _, dev = _objective(best_state, q1, cnt, const)
    return best_state, {"model_dev_pp_before": before, "model_dev_pp_after": dev}


def apply(cards):
    """Patch the training cards in place; returns a log dict (written to tmp/repair/cardfix_r2.json by build)."""
    train = [c for c in cards if not c.get("held_out")]
    pp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cardfix_r2_plan.json")
    if os.path.exists(pp):
        P = json.load(open(pp))
        state = {cid: tuple(v) for cid, v in P["state"].items()}
        info = {k: v for k, v in P.items() if k != "state"}
    else:
        state, info = plan_longest(train)
    # r3 (c-lanes-v3 repair round 1): cardfix_r3_plan.json re-chooses (default, CBD label, fallback) on the Q1 cards it
    # lists and gives them per-set (gold source | longest) row quotas, so the A28 longest-option-per-source balance
    # holds on the regenerated cards by construction (tmp/repair/r3/NOTES.md)
    p3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cardfix_r3_plan.json")
    r3 = json.load(open(p3)) if os.path.exists(p3) else {"cards": {}}
    for cid, v in r3["cards"].items():
        if v.get("state"):
            state[cid] = tuple(v["state"])
    changed = []
    for c in train:
        st = state.get(c["card_id"])
        if st is None:
            continue
        d, lab = st[0], st[1]
        fbn = st[2] if len(st) > 2 else c.get("fallback")
        if d != c["default"] or fbn != c.get("fallback"):
            for o in (c["default"], c.get("fallback")):
                if o is not None:
                    c["roles"][o] = "other"
            c["roles"][d] = "default"
            c["default"] = d
            if fbn is not None:
                c["roles"][fbn] = "fallback"
                if fbn != c.get("fallback"):
                    changed.append((c["card_id"], "fallback"))
                c["fallback"] = fbn
            changed.append((c["card_id"], "default"))
        if lab != c["cbd_label"]:
            c["cbd_label"] = lab
            changed.append((c["card_id"], "cbd_label"))
    # T-source cap (plan "t_caps"): on Q1 cards where the escalate outcome is the longest option whatever the choices
    # above and the tie rule gives escalate, tie-decided (T) gold rows are kept rare; escalate stays gold at its
    # role rate through rules that give it (the role-rate rule counts the role, not the source)
    for c in train:
        v = r3["cards"].get(c["card_id"])
        if v and v.get("src_quota"):
            c["src_quota"] = v["src_quota"]
    for cid in (info.get("t_caps") or {}):
        for c in train:
            if c["card_id"] == cid:
                c["t_src_cap"] = 0.02
    for c in train:
        if c["qtype"] == "Q2":
            # r3 (A22: Q2 rows <= 7,900 tokens): every Q2 card draws half its rows with 20-23 options (G0 1.1)
            c["q2_big_share"] = 0.5 if Q2_A22 else (Q2_BIG_SHARE if c["card_id"] in Q2_BIG_CARDS else 0.0)
    old_rows = {c["card_id"]: c["n_rows"] for c in train}
    new_rows = refit_rows(train)
    if Q2_A22:
        # r3: the Q2 rows (same total) go back to the cards in proportion to their r1 plan, since every Q2 card can
        # now carry 20-60 option rows (r2 moved 128 rows each onto the five cards that fit 20 options under 2,000)
        q2 = [c["card_id"] for c in train if c["qtype"] == "Q2"]
        tot, w1 = sum(new_rows[x] for x in q2), sum(old_rows[x] for x in q2)
        for x in q2:
            new_rows[x] = min(128, max(24, int(round(tot * old_rows[x] / w1))))
    for c in train:
        c["n_rows_r1"] = old_rows[c["card_id"]]
        c["n_rows"] = new_rows[c["card_id"]]
    nf = sum(c["n_rows"] for c in train if "notices" not in c["constructs"]) / sum(c["n_rows"] for c in train)
    info.update({"changed": changed, "notice_free_row_share": round(nf, 4),
                 "rows_total": sum(c["n_rows"] for c in train), "rows_total_r1": sum(old_rows.values())})
    return info


# ---------------------------------------------------------------- r2 pass B model (observed per-option gold counts)

def _counts2():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cardfix_r2_counts2.json")
    return json.load(open(p)) if os.path.exists(p) else None


def _p_longest2(card, st, src_opt):
    """Like _p_longest, but the rule-source and tie-source gold spread over the options is the one observed on the
    pass A rows of this card (D, F and CBD gold follow the chosen default, fallback and CBD label)."""
    d, cbd = st[0], st[1]
    fb = st[2] if len(st) > 2 and st[2] is not None else card.get("fallback")
    disp = card["display"]
    keys = list(card["outcomes"]) + (["__CBD__"] if card["world"] == "open" else [])
    L = {o: len(disp[o]) for o in card["outcomes"]}
    if card["world"] == "open":
        L["__CBD__"] = len(cbd)
    m = max(L.values())
    ties = [o for o in keys if L[o] == m]
    share = {o: (1.0 / len(ties) if o in ties else 0.0) for o in keys}
    k = len(keys)
    out = {"CBD": share.get("__CBD__", 0.0), "D": share[d], "F": share[fb] if fb else 0.0}
    for s in ("ONE", "MANY", "mixed", "T"):
        q = src_opt.get(s) or {}
        n = sum(q.values())
        out[s] = (sum(share.get(o, 0.0) * v for o, v in q.items()) / n) if n else 0.0
    return out, 1.0 / k


def search_longest2(cards, restarts=24, seed=SEED, weights=None):
    C = _counts2()
    so, const = C["q1_src_opt"], C["q2q4_longest"]
    W = dict(SOURCES_W)
    W.update(weights or {})
    q1 = sorted([c for c in cards if c["qtype"] == "Q1" and c["card_id"] in so], key=lambda c: c["card_id"])
    choices = {}
    for c in q1:
        elig = [o for o in c["outcomes"] if c["roles"][o] in ("default", "other")]
        labs = [x for x in CBD_VARIANTS if _ok_label(c, x)] if c["world"] == "open" else [c["cbd_label"]]
        if c["world"] == "open" and c["cbd_label"] not in labs:
            labs.append(c["cbd_label"])
        fbs = [None]
        if c.get("fallback"):
            fbs = [o for o in c["outcomes"] if c["roles"][o] in ("fallback", "other", "default")]
        choices[c["card_id"]] = [(d, lab, f) for d, lab, f in itertools.product(elig, labs, fbs) if f is None or f != d]
    orig = {c["card_id"]: (c["default"], c["cbd_label"], c.get("fallback")) for c in q1}

    def obj(st):
        acc = {s: list(const.get(s, [0, 0, 0])) for s in W}
        for c in q1:
            src_opt = so[c["card_id"]]
            p, ik = _p_longest2(c, st[c["card_id"]], src_opt)
            for s in W:
                n = sum((src_opt.get(s) or {}).values())
                acc[s][0] += n * p[s]
                acc[s][1] += n * ik
                acc[s][2] += n
        tot, dev = 0.0, {}
        for s, (a, b, n) in acc.items():
            if n:
                dv = (a - b) / n
                dev[s] = round(100 * dv, 2)
                tot += W[s] * (n / 100.0) * dv * dv
        return tot + 1e-4 * sum(1 for x in st if st[x] != orig[x]), dev

    rng = random.Random(seed)
    best_all, best_state = None, None
    for rs in range(restarts):
        state = dict(orig) if rs == 0 else {cid: rng.choice(ch) for cid, ch in choices.items()}
        best, _ = obj(state)
        for sweep in range(15):
            order = list(q1)
            rng.shuffle(order)
            changed = False
            for c in order:
                cid = c["card_id"]
                cur = state[cid]
                for ch in choices[cid]:
                    if ch == cur:
                        continue
                    state[cid] = ch
                    v, _ = obj(state)
                    if v < best - 1e-12:
                        best, cur, changed = v, ch, True
                    state[cid] = cur
            if not changed:
                break
        if best_all is None or best < best_all:
            best_all, best_state = best, dict(state)
    return best_state, {"model2_dev_pp_before": obj(orig)[1], "model2_dev_pp_after": obj(best_state)[1]}
