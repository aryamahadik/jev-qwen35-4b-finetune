"""Card plan (round 1) and card finalisation: one pack per card (XF09), card flag set (section 2), containers,
styles (training or held-out), wordings (>= 5 per card), T5 domains, card IR with program-computed examples and
few-shot block (section 5), render key. Every decision is seeded from the card id."""
from __future__ import annotations

import random
from fractions import Fraction

from f9cards import FRAMES, TERM_FRAMES, card_ir, draw_card, f9_wordings, styles
from f9lex import uh
import f9packs

CARDS_R1 = {"S1": 20, "S2": 20, "S3": 17, "S4": 17, "S6": 16}
ROWS_R1 = {"S1": 900, "S2": 900, "S3": 750, "S4": 750, "S6": 750}
S5_CARDS = 16
CONTAINERS = {"S1": ["md", "csv", "html", "fw", "kv"], "S2": ["md", "csv", "html", "fw", "kv"],
              "S3": ["md", "csv", "html", "fw", "kv"], "S4": ["json_pretty", "json_compact", "jsonl", "yaml"],
              "S5": ["md"]}
SYNTAXES = ["bracket", "isocomp", "kv", "syslog"]


def _pack_ok(p, s, flags):
    if flags.get("term") and not (p["cats"] and len(p["cats"][-1]["values"]) >= 4):
        return False
    if flags.get("masked") and len(p["cats"][0]["values"]) < 3:
        return False
    if s in ("S3",) and len(p["nums"]) < 2:
        return False
    return True


# card profiles (1.8 length plan): a choice row prints its card twice (A16.1 g), so choice rows fit the 2,000-token
# cap only on short cards. "Light" cards (no UNKNOWN cells, no date windows, no group comparisons or averages, no
# override rules) carry most choice rows; "heavy" cards (T4 / T5, windows, comparisons, overrides, few-shot blocks)
# carry mostly yes/no rows. Per-sampler counts: (light: T2 / T1-complete, heavy: T4 / T5).
PROFILE = {"S1": {"L": (6, 7), "H": (3, 4)}, "S2": {"L": (6, 7), "H": (3, 4)}, "S3": {"L": (0, 11), "H": (3, 3)},
           "S4": {"L": (6, 7), "H": (2, 2)}, "S6": {"L": (0, 11), "H": (0, 5)}}
# repair r1: swapped choice rows were 4.4% / 3.9% (target 5 +/- 1) and masked 9.8% (target 10-15%): one more swap-word
# card (S1) and one more masked light card on S1 and S2 (heavy cards hold no choice rows)
TERMS = {"S1": {"inv": 4, "swap": 3, "heavy": 2}, "S2": {"inv": 4, "swap": 4, "heavy": 2},
         "S4": {"inv": 3, "swap": 3, "heavy": 2}}
MASKED = {"S1": (3, 1), "S2": (3, 1), "S3": (3, 1), "S4": (2, 1)}


def plan_cards():
    """Round-1 training cards: [(card_id, sampler, pack, flags)], deterministic. Quotas: one pack per card (XF09);
    examples ~50% of cards, rubric ~20%, few-shot 5-10% (7), inverted 10-15% (11), swap-word cards (7)."""
    rng = random.Random("f9-plan-r1")
    packs = list(f9packs.training_packs())
    rng.shuffle(packs)
    plan = []
    for s, n in CARDS_R1.items():
        prof = PROFILE[s]
        slots = []
        for w, k in zip(("T2", "T1"), prof["L"]):
            slots += [{"light": True, "world": w if s not in ("S3", "S6") else "T1", "missing": None}] * k
        for m, k in zip(("T4", "T5"), prof["H"]):
            slots += [{"light": False, "world": "T1", "missing": m if s != "S6" else None}] * k
        slots = [dict(x) for x in slots]
        assert len(slots) == n, (s, len(slots))
        r = random.Random("f9-plan-" + s)
        light = [x for x in slots if x["light"]]
        heavy = [x for x in slots if not x["light"]]
        if s in TERMS:
            t = TERMS[s]
            lt = r.sample(light, t["inv"] + t["swap"])
            for x in lt[:t["inv"]]:
                x.update(term=True, inverted=True)
            for x in lt[t["inv"]:]:
                x.update(term=True, swap=True)
            for x in r.sample(heavy, t["heavy"]):
                x.update(term=True)
        if s in MASKED:
            ml, mh = MASKED[s]
            for x in r.sample([x for x in light if not x.get("term")] or light, ml) + r.sample(heavy, mh):
                x["masked"] = True
        r.shuffle(slots)
        for i, fl in enumerate(slots):
            plan.append([f"F9-{s}-c{i + 1:02d}", s, None, fl])
    heavy = [row for row in plan if not row[3]["light"]]
    light = [row for row in plan if row[3]["light"]]
    rng.shuffle(heavy)
    rng.shuffle(light)
    # definition examples (about 50% of cards) go to the S1 / S2 light cards first: their tables are short, while S3,
    # S4 and S6 light choice rows need every token of the 1.8 cap (the card prints twice)
    light.sort(key=lambda row: (row[1] not in ("S1", "S2"), bool(row[3].get("term")), row[3].get("world") == "T2"))
    # S4 heavy cards (nested records, T4 / T5) have the least room under the 1.8 cap: no rubric table and no
    # few-shot block on them (one-line definitions with examples instead)
    heavy.sort(key=lambda row: row[1] == "S4")
    for k, row in enumerate(heavy):
        row[3]["defs_style"] = "rubric_table" if k < 18 else "one_line_examples"
    for k, row in enumerate(light):
        row[3]["defs_style"] = "one_line_examples" if k < 33 else "one_line"
    for row in rng.sample([h for h in heavy if h[1] != "S4"], 7):
        row[3]["fewshot"] = True
    used = set()
    for row in plan:
        cid, s, _, fl = row
        for p in packs:
            if p["pack_id"] in used or not _pack_ok(p, s, fl):
                continue
            row[2] = p
            used.add(p["pack_id"])
            break
        if row[2] is None:
            raise RuntimeError("no pack for " + cid)
    return [tuple(x) for x in plan]


def plan_s5():
    packs = list(f9packs.heldout_packs())
    rng = random.Random("f9-plan-s5")
    rng.shuffle(packs)
    out = []
    for i in range(S5_CARDS):
        cid = f"F9-S5-c{i + 1:02d}"
        fl = {"world": "T1", "defs_style": ["one_line", "one_line_examples", "rubric_table"][i % 3]}
        out.append((cid, "S5", packs[i], fl))
    return out


# ------------------------------------------------------------------------------------------------ finalisation
def _t5(card):
    sc = card["schema"]
    s = card["sampler"]
    if s == "S3":
        cc = [sc["fact_cats"][0], sc["fact_nums"][0]]
    else:
        cc = [sc["cats"][0], sc["nums"][0]]
    card["t5_cols"] = [c["name"] for c in cc]

    def dv(c):
        if c["type"] == "cat":
            return list(c["values"])
        k = int((c["hi"] - c["lo"]) / c["step"])
        return [c["lo"] + c["step"] * i if c["dp"] else Fraction(int(c["lo"] + c["step"] * i)) for i in range(k + 1)]
    card["t5_domains"] = {c["name"]: {"col": c, "values": dv(c)} for c in cc}


def _style_ok(card, sid, held_out):
    from fmt1 import card as fcard
    from fmt1 import pool as fpool
    st = fpool.dev_style(sid) if held_out else fpool.training_style(sid)
    try:
        fcard.render_card(card["ir"], st)
        ent, rest, tk = fcard._split_choice_card(card["ir"], st, ["X1", "X2", "X3"])
        if ent:
            return False
        if rest["blocks"] or rest.get("title"):
            fcard.render_card(rest, st)
    except Exception:
        return False
    return True


def _term_phrases(card):
    """Term / override predicates on numeric columns carry the card's own comparison phrase for their operator (and
    a phrase the card does not list yet is added to it), so the card's T10 sentences state every phrase its
    definitions use (G3: the parser refuses an unstated phrase)."""
    from f9lex import CMP_T10
    from f9render import DEFAULT_PH

    def fix(a):
        if isinstance(a, dict):
            if a.get("k") == "cmp" and a.get("unit") is not None and a.get("op") in (">=", "<=", ">", "<") \
                    and not a.get("_ph"):
                ph = next((p for p in card["cmp_amount"] if CMP_T10.get(p) == a["op"]), None)
                if ph is None:
                    ph = DEFAULT_PH[a["op"]]
                    card["cmp_amount"].append(ph)
                a["_ph"] = ph
            for k, v in a.items():
                if k != "usual":
                    fix(v)
        elif isinstance(a, list):
            for v in a:
                fix(v)
    fix(card.get("terms") or {})


def finalize(cid, s, pack, fl, held_out=False):
    from f9emit import used_flags
    from f9rows import render_key_fn
    rng = random.Random("f9-card:" + cid)
    card = draw_card(cid, s, pack, rng, flags=fl)
    card["held_out"] = held_out
    card["light"] = bool(fl.get("light"))
    lean_card(card, random.Random("f9-lean:" + cid))
    _term_phrases(card)
    if card["sem"].get("missing") == "T5":
        _t5(card)
    if s == "S6":
        card["syntaxes"] = list(SYNTAXES)
        card["containers"] = []
    elif s == "S4":
        card["containers"] = list(CONTAINERS["S4"])
    elif s == "S5":
        card["containers"] = ["md"]
    else:
        ks = list(CONTAINERS[s])
        r = random.Random("f9-cont:" + cid)
        r.shuffle(ks)
        card["containers"] = sorted(ks[:3])
    card["used"] = used_flags(card)
    W = f9_wordings()
    r = random.Random("f9-words:" + cid)
    anyw = [w["id"] for w in W if w["forms"][0] == "any"]
    ynw = [w["id"] for w in W if w["forms"][0] == "yn"]
    chw = [w["id"] for w in W if w["forms"][0] == "choice"]
    card["wordings"] = r.sample(anyw, 4) + r.sample(ynw, 2) + r.sample(chw, 2)
    from f9examples import attach_examples
    attach_examples(card, rng)
    card["ir"] = card_ir(card, card["used"], card.get("examples"), card.get("fewshot_block"))
    pool = [x["id"] for x in styles(held_out=held_out)]
    r = random.Random("f9-styles:" + cid)
    r.shuffle(pool)
    ok = []
    for sid in pool:
        if _style_ok(card, sid, held_out):
            ok.append(sid)
        if len(ok) >= 10:
            break
    if len(ok) < 5:
        raise RuntimeError(f"{cid}: only {len(ok)} styles render")
    card["styles"] = ok
    card["render_key"] = render_key_fn(card)
    return card


# ------------------------------------------------------------------------------------------------ lean cards (1.8)
YN_POOL = {"S1": ["Y_EXISTS", "Y_COUNT", "Y_LOOKN", "Y_LOOKC", "Y_FORALL", "Y_PRES"],
           "S3": ["Y_EANY", "Y_ESUM", "Y_GCOUNT"], "S4": ["Y_EXISTS", "Y_COUNT", "Y_LOOKN", "Y_LOOKC", "Y_PRES"],
           "S6": ["Y_LEX", "Y_LCOUNT", "Y_REQ"], "S5": ["Y_CELL"]}
YN_POOL["S2"] = YN_POOL["S1"]


def lean_menu(card, rng):
    """A card's question menu: a subset of its sampler's frames, so that its card flag set (section 2; the clauses
    its wording base needs) stays short enough for the 1.8 token caps on the served prompt (A16.1 g: a choice row
    prints the card twice). Every form the sampler plans keeps at least one frame."""
    s = card["sampler"]
    full = dict(card["menu"])
    if s == "S5":
        return full
    light = card.get("light", False)
    pool = [f for f in YN_POOL[s] if f in full]
    keep = set(rng.sample(pool, min(len(pool), 3 if s != "S3" else 2)))
    if light and s == "S6":
        keep.discard("Y_REQ")
    s4 = s == "S4"  # S4 cards: no group comparisons or averages (T22 / T35 clauses; 1.8 card length)
    if "Y_COMPARE" in full and not light and not s4 and rng.random() < 0.5:
        keep.add("Y_COMPARE")
    if "Y_MEAN" in full and not light and not s4 and rng.random() < 0.4:
        keep.add("Y_MEAN")
    if s == "S4":
        t14 = rng.choice(["Y_ANY", "Y_EVERY"])
        if not light:  # T14 list questions sit on heavy S4 cards (light cards: no T14 clause, 1.8)
            keep.add(t14)
    vals = [f for f, v in full.items() if v == "value" and f not in ("V_TCOUNT", "V_MEAN")]
    keep |= set(rng.sample(vals, min(2, len(vals))))
    if card["sem"]["world"] == "T2" and "V_LOOK" in full:
        keep.add("V_LOOK")  # T2 lookups carry the premise-removal pairs (1.7)
    if "V_MEAN" in full and not light and not s4 and ("Y_MEAN" in keep or rng.random() < 0.15):
        keep.add("V_MEAN")
    recs = [f for f, v in full.items() if v == "record" and f != "R_INV"]
    if rng.random() < 0.7:
        keep |= set(recs)
    else:
        # repair r1: a card with one record frame keeps a condition pick when it has one (an extreme pick needs two
        # named-error distractors and was blocked on many cards, leaving their choice rows to 2-4 value / set picks)
        cond = [f for f in recs if f in ("R_COND", "E_COND", "C_REQ")]
        keep |= set(rng.sample(cond or recs, 1))
    keep |= {f for f, v in full.items() if v == "set" and f != "SET_TERM"}
    if light and s == "S6" and rng.random() >= 0.7:
        keep.discard("SET_REQ")  # T41 (76 tokens) only on S6 cards with request questions; light: about 1 in 3
    if card.get("terms"):
        keep |= set(rng.sample(["Y_TERM", "Y_TERMX"], 1 if light else rng.choice([1, 2])))
        tc = rng.choice(["V_TCOUNT", "SET_TERM"])
        keep |= {"V_TCOUNT", "SET_TERM"} if card.get("swap") else {tc}
        if card.get("inverted"):
            keep.add("R_INV")
    if light and s == "S6":
        if "SET_REQ" in keep:
            keep.discard("C_COMP")  # a light request card has T41; no T24 tie clause beside it (1.8)
            if "C_REQ" in full:
                # repair r1 (option buckets): the T41 request card's record pick is the request pick, which can show
                # 5-30 request ids (the component pick holds 2-6 components), with no extra card clause
                keep.add("C_REQ")
        else:
            keep.discard("C_REQ")
    return {f: v for f, v in full.items() if f in keep}


def lean_card(card, rng):
    s = card["sampler"]
    card["menu"] = lean_menu(card, rng)
    # keep every comparison phrase the drawn card content already uses (term, override and derived-field
    # predicates), so the card's T10 sentences state each phrase that appears anywhere on it (G3, 1.5)
    held = set()

    def _phs(x):
        if isinstance(x, dict):
            if isinstance(x.get("_ph"), str):
                held.add(x["_ph"])
            for k, v in x.items():
                if k not in ("cmp_count", "cmp_amount", "menu"):
                    _phs(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                _phs(v)
    _phs(card)
    card["cmp_count"] = card["cmp_count"][:2] + [p for p in card["cmp_count"][2:] if p in held]
    card["cmp_amount"] = card["cmp_amount"][:3] + [p for p in card["cmp_amount"][3:] if p in held]
    light = card.get("light", False)
    # S4 questions use no date windows (3.4), so S4 cards carry no T15 / T16 clause (1.8: card length)
    card["time_forms"] = [] if (light or s == "S4") else card["time_forms"][:2]
    card["use_in2"] = (not light) and rng.random() < 0.5
    card["use_not"] = card["use_not"] and rng.random() < 0.7
    card["use_between"] = card["use_between"] and rng.random() < 0.6
    if light or s == "S4":  # no override rules (T30) on light cards or on S4 cards (1.8 card length)
        for t in (card.get("terms") or {}).values():
            t.pop("overrides", None)
