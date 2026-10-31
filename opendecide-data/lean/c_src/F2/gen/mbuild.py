"""Money card construction for S1 / S2 (and the sweep): plan choice, SEM options, flip variants, short cards, CH-O
outcome tables, CL settings."""
from __future__ import annotations

from decimal import Decimal

from . import mcard, money
from .cards import common_card, style_set, DV_BY_STYLE, TASKS, case_ref_fn
from .common import D, ONE, quant, uhash
from .render import flabels, fpool

S1_PLANS = ["unit", "unit", "unit_fee", "unit_fee", "cap", "pct", "min", "disc", "disc", "disc_min", "net", "net",
            "disc2", "perk", "listed"]
S2_PLANS = ["unit_fee", "min", "disc_min", "cap", "perk", "unit", "unit_fee", "min"]
CL_PLANS = ["cap", "unit", "disc", "pct"]


def flip_candidates(card):
    m = card["m"]
    sem = m["sem"]
    c = []
    if "R1" in sem:
        modes = [x for x in ("half_up", "half_even", "floor", "ceiling") if x != sem["R1"]
                 and not (x == "half_even" and D(sem["R1u"]) > ONE)]
        c.append(("R1", {"R1": modes[0]}))
        if card["schema"] == "YN-T" and not card.get("op_item"):
            c.append(("R3", {"R3": "unrounded"}))
    if "R2" in sem:
        c.append(("R2", {"R2": "line" if sem["R2"] == "final" else "final"}))
    if "R5" in sem:
        c.append(("R5", {"R5": "floor" if sem["R5"] == "ceil" else "ceil"}))
    if "U3" in sem:
        c.append(("U3", {"U3": "full_k" if sem["U3"] == "pro_rata" else "pro_rata"}))
    if "X5" in sem:
        c.append(("X5", {"X5": "added" if sem["X5"] == "succ" else "succ"}))
    if "X7" in sem:
        c.append(("X7", {"X7": "before" if sem["X7"] == "include" else "include"}))
    if "X3" in sem:
        c.append(("X3", {"X3": "alone_higher" if sem["X3"] != "alone_higher" else "alone_lower"}))
    if "X1" in sem:
        c.append(("X1", {"X1": list(reversed(sem["X1"]))}))
    if "X4" in sem and len(m["lines"]) > 1:
        sid, sc = next(iter(sem["X4"].items()))
        c.append(("X4", {"X4": {sid: "line" if sc == "total" else "total"}}))
    for e in m["excs"]:
        if e["join"] in ("or1", "or2") and e["conn"] in ("O2", "UN1"):
            c.append((f"OR:{e['no']}", {"ORJ": {str(e["no"]): "or2" if e["join"] == "or1" else "or1"}}))
        if e["kind"] in ("rate", "pct"):
            c.append((f"X2:{e['no']}", {"X2": {str(e["no"]): "add"}}))
    if card["schema"] == "CH-O":
        c.append(("B1", {"B1o": "lower" if card["b1"] == "upper" else "upper"}))
    return c


def make_money_card(card, pack, rng, *, sweep_depth=None):
    """card has sampler, schema, card_id, world, instr ('std' | 'fewshot' | 'inverted'), held_out."""
    common_card(card, pack, rng)
    sch = card["schema"]
    s = card["sampler"]
    if "plan" not in card:
        if sch == "CL":
            card["plan"] = rng.choice(CL_PLANS)
        elif sch == "CH-O":
            card["plan"] = rng.choice(["unit", "cap", "min", "disc_min", "perk", "unit_fee"])
        elif s == "S2":
            card["plan"] = rng.choice(S2_PLANS)
        else:
            card["plan"] = rng.choice(S1_PLANS)
    plan = card["plan"]
    card.setdefault("dec2", rng.random() < 0.5)
    if card["world"] == "open":
        card["nexc"] = 1
        card["joins"] = {1: rng.choice(["and", "or1"])}
        card["conns"] = {1: "O2"}
        card["unk_type"] = rng.choice(["flag", "cat"])
        if plan not in ("unit", "unit_fee", "cap", "pct", "min", "disc", "disc_min"):
            card["plan"] = plan = rng.choice(["unit", "cap", "pct", "min", "disc_min"])
    else:
        card.setdefault("nexc", rng.choice([0, 1, 1, 2]) if sch not in ("CL", "CH-O") else
                        (1 if sch == "CL" else rng.choice([1, 1, 2])))
    card.setdefault("with_add", rng.random() < 0.7)
    card.setdefault("partial", plan in ("unit", "unit_fee") and (sch == "CL" or rng.random() < 0.7))
    card.setdefault("nlines", 2 if (plan in ("unit", "unit_fee", "cap", "net") and rng.random() < 0.4
                                    and sch != "CL") else 1)
    if card["nlines"] == 2 and card.get("partial") and sch != "CL":
        card["partial"] = rng.random() < 0.15
    card.setdefault("nded", 2 if rng.random() < 0.3 else 1)
    card.setdefault("scope", rng.choice(["total", "line"]) if card["nlines"] > 1 else "total")
    if s == "S2" and plan in ("unit_fee", "min", "disc_min", "perk", "pct", "disc"):
        card["dec2"] = rng.random() < 0.6
    mcard.build(card, pack, rng)
    m = card["m"]
    sem = m["sem"]
    if "R1" in sem and s == "S2":
        if m["dec2"]:
            sem["R1u"] = ONE
        else:
            sem["R1u"] = D(10)
            if sem["R1"] == "half_even":
                sem["R1"] = rng.choice(["half_up", "floor", "ceiling"])
    card["res_unit"] = m["unit"]
    if plan == "net" and sch == "YN-T":
        card["op_item"] = rng.choice(["balance", "net amount"])
    # open world: the unknown field is the exception's first condition field (read by a rule; R1-27)
    if card["world"] == "open":
        if not m["excs"]:
            raise ValueError("open card without exception")
        c0 = m["excs"][0]["conds"][0]
        card["unknown_field"] = c0["f"]
        card["unknown_dom"] = c0["dom"] if c0["ftype"] == "cat" else ["yes", "no"]
    # relevant / shown / omitted (short cards: about 15% of rows; omit filter dims with p = 0.5)
    relevant = set(k for k in sem if k not in ("R1u",))
    if "R1" in sem:
        relevant |= {"R4"}
    card["short"] = card.get("short", False)
    if sch == "CH-O":
        setup_outcomes(card, rng)
    flips = flip_candidates(card)
    rng.shuffle(flips)
    nvar = 0 if sweep_depth is not None else (2 if s == "S2" else rng.choice([1, 2, 2]))
    card["variants"] = [{"dim": d, "over": o} for d, o in flips[:nvar]]
    planned = {v["dim"].split(":")[0] for v in card["variants"]}
    omitted = []
    if card["short"]:
        for d in ("R1", "R5", "U3", "X8"):
            if d in relevant and d not in planned and rng.random() < 0.5:
                omitted.append(d)
    card["omitted"] = omitted
    shown = set(relevant) - set(omitted)
    if "R1" in omitted:
        shown -= {"R2", "R3", "R4"}
    card["shown"] = shown
    # definition style
    if card["short"]:
        card["defs_style"] = "short"
    elif card["instr"] == "fewshot":
        card["defs_style"] = rng.choice(["one_line", "decision_list"])
    elif sch == "CL":
        card["defs_style"] = rng.choice(["one_line", "decision_list"])
    else:
        card["defs_style"] = rng.choice(["one_line", "one_line_examples", "one_line_examples", "decision_list"])
    card["dv"] = rng.choice(DV_BY_STYLE[card["defs_style"]])
    card["task"] = rng.choice(TASKS).format(res=m["res"], ent=card["ent_sg"])
    # choice settings
    card["k_choices"] = [3, 4, 5, 5, 6, 6, 7, 7, 8, 9] if s != "S2" else [2, 3, 4, 4, 5, 6, 7]
    card["open_k"] = [3]
    card["none_ok"] = sch in ("CH-V", "CL") and card["world"] == "closed" and rng.random() < 0.4
    card["none_text"] = "None of the listed " + ("amounts" if sch == "CH-V" else card["ent_pl"] if sch != "CL" else "cases")
    if sch == "CL":
        card["case_ref_id"] = rng.choice(["IVN01", "IVN03", "IVN04", "IVN05", "IVN07"])
        card["case_refs"] = case_ref_fn(card)
        narrow = not (card["m"]["excs"] or any(s_["op"] in ("cap", "min") for s_ in card["m"]["steps"]))
        card["ncase_choices"] = ([5, 6, 7, 8, 9, 10, 11, 12] if narrow else
                                 [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26])
        card["frame"] = None if card["none_ok"] else rng.choice(["IVC04", "IVC05", None])
    card["need_table"] = sch == "CL"
    card["styles"] = style_set(rng, card["card_id"], card.get("held_out", False), card["need_table"])
    return card


def setup_outcomes(card, rng):
    """CH-O named outcomes: 3-6 B1-form ranges of the final value, edges from a pilot of the card's values."""
    m = card["m"]
    vals = []
    for _ in range(300):
        v, f = mcard.draw(card, rng)
        LP = mcard.make_lp(card, v, f, {"kind": "value"}, m["sem"])
        try:
            vals.append(money.evaluate(LP, {})[0])
        except Exception:
            pass
    vals.sort()
    n = rng.randint(3, 6)
    step = D("10") if not m["dec2"] else D("5")
    edges = []
    for i in range(1, n):
        e = vals[int(len(vals) * i / n)]
        e = quant(e, step, "half_up")
        if e <= 0 or (edges and e <= edges[-1]):
            e = (edges[-1] if edges else D(0)) + step
        edges.append(e)
    from .mcard import OUTCOME_SETS, OUTCOME_KINDS
    names = rng.choice(OUTCOME_SETS)[:n]
    outs = []
    for i in range(n):
        outs.append({"name": names[i], "lo": edges[i - 1] if i > 0 else None, "hi": edges[i] if i < n - 1 else None})
    _b1 = rng.choice(["upper", "lower"])
    card["b1"] = card.get("b1") or _b1
    card["okind"] = rng.choice(OUTCOME_KINDS)
    r = rng.random()
    card["named"] = card.get("named_force") or ("masked" if r < 0.4 else "swapped" if r < 0.57 else "plain")
    if card["named"] == "masked":
        disp = flabels.masked_ids(rng.choice(["MS01", "MS03", "MS05", "MS07", "MS16", "MS19"]), n, card["card_id"])
    elif card["named"] == "swapped":
        words = [w["word"] for w in fpool.swap_words() if not w["ordered"] and w["group"] in
                 ("colour", "material", "weather", "animal", "plant", "shape")]
        rng.shuffle(words)
        disp = [w.capitalize() for w in words[:n]]
    else:
        disp = [x.capitalize() for x in names]
    for o, d in zip(outs, disp):
        o["name"] = d
    card["outs"] = outs
    card["out_disp"] = disp
    card["outs_q"] = [{"name": o["name"], "lo": o["lo"], "hi": o["hi"]} for o in outs]
