"""Engine adapter for S3 tiered rate tables."""
from __future__ import annotations

import copy

from . import bandeval as BE, bcard, bgen, lex, qtext, render as R, rowkit
from .cards import common_card, style_set, DV_BY_STYLE, TASKS, case_ref_fn
from .common import D, ONE
from .money import Reject
from .mrows import gen_entity_id
from .render import flabels, fpool

NAME = "band"


def make_card(card, pack, rng, **kw):
    common_card(card, pack, rng)
    bcard.build(card, pack, rng)
    s = card["b"]
    sch = card["schema"]
    r = rng.random()
    card["named"] = card.get("named_force") or ("masked" if r < 0.4 else "swapped" if r < 0.57 else "plain")
    n = 14
    if card["named"] == "masked":
        card["band_disp"] = flabels.masked_ids(rng.choice(["MS01", "MS05", "MS07", "MS16", "MS19", "MS04"]), n, card["card_id"])
    elif card["named"] == "swapped":
        words = [w["word"] for w in fpool.swap_words() if not w["ordered"] and w["group"] in
                 ("colour", "material", "weather", "animal", "plant", "shape")]
        rng.shuffle(words)
        card["band_disp"] = [w.capitalize() for w in words[:n]]
    else:
        base = s["names"]
        card["band_disp"] = base + [f"{base[0]} {i}" for i in range(2, 2 + n - len(base))]
    card["table_caption"] = rng.choice(["Band table", "Rate bands", "Tariff bands"])
    flips = []
    sem = s["sem"]
    if not (s["count"] and sem["B2"] == "marginal"):
        flips.append(("B1", {"B1": "lower" if sem["B1"] == "upper" else "upper"}))
    if s["rate_kind"] != "flat" and not s["count"] and not s["x10"] and sch != "CL":
        flips.append(("B2", {"B2": "marginal" if sem["B2"] == "flat" else "flat"}))
    if "R1" in sem:
        modes = [x for x in ("half_up", "half_even", "floor", "ceiling") if x != sem["R1"]]
        flips.append(("R1", {"R1": rng.choice(modes)}))
    rng.shuffle(flips)
    card["variants"] = [{"dim": d, "over": o} for d, o in flips[:rng.choice([1, 2, 2])]]
    card["short"] = False
    card["defs_style"] = (rng.choice(["one_line", "one_line_examples", "one_line_examples", "decision_list"])
                          if card["instr"] != "fewshot" and sch != "CL" else rng.choice(["one_line", "decision_list"]))
    card["dv"] = rng.choice(DV_BY_STYLE[card["defs_style"]])
    card["task"] = rng.choice(TASKS).format(res=s["final"], ent=card["ent_sg"])
    card["none_ok"] = sch in ("CH-V", "CL") and card["world"] == "closed" and rng.random() < 0.4
    card["none_text"] = "None of the listed " + ("amounts" if sch == "CH-V" else "cases")
    if sch == "CL":
        card["case_ref_id"] = rng.choice(["IVN01", "IVN03", "IVN04", "IVN05", "IVN07"])
        card["case_refs"] = case_ref_fn(card)
        card["ncase_choices"] = [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24]
        card["frame"] = None if card["none_ok"] else rng.choice(["IVC04", "IVC05", None])
    card["styles"] = style_set(rng, card["card_id"], card.get("held_out", False), True)
    card["res_unit"] = s["unit"]
    card["k_choices"] = [3, 4, 5, 5, 6, 6, 7, 7, 8, 9]
    card["open_k"] = [3]
    if card["instr"] == "fewshot":
        blk = build_fewshot(card, rng)
        if blk is None:
            card["instr"] = "std"
        else:
            card["fewshot_block"] = blk
    return card


def gen_row(card, rng, var=0, want=None):
    return bgen.gen_row(card, rng, var, want)


def new_eid(card, rng, used):
    return gen_entity_id(card, rng, used)


def question(card, spec, eid, rng):
    s = card["b"]
    qk = spec["qkind"]
    LP = spec["LP"]
    side = card["side_money"]
    if qk == "thr":
        T = bcard.mstr(LP["q"]["T"], card)
        op = LP["q"]["cmp"]
        q, info = qtext.thr_question(s["final"], eid, op, T, LP["q"]["neg"], spec.get("tf", False), rng)
        info["pol"] = qtext.pol_tag("up" if op in ("ge", "gt") else "down", side, LP["q"]["neg"])
        return q, info
    if qk == "value":
        return lex.fill(rng.choice(lex.Q_VALUE), res=s["final"], id=eid), {"neg": 0, "tf": 0}
    if qk == "band":
        return lex.fill(rng.choice(lex.Q_BAND), amt=s["amt"], id=eid), {"neg": 0, "tf": 0}
    if qk == "cases":
        T = bcard.mstr(LP["q"]["T"], card)
        op = LP["q"]["cmp"]
        ph, negcmp, _ = qtext.cmp_phrase(op, T, rng.randrange(len(lex.Q_CMP[op])))
        return lex.fill(rng.choice(lex.Q_CASES), res=s["final"], cmpT=ph), {"neg": 0, "tf": 0, "negcmp": negcmp}
    raise ValueError(qk)


def card_ir_for(card, var):
    sem = bgen.var_sem(card, var)
    cl = bcard.clauses(card, sem, card["shown"], card["world"])
    extra = []
    if card["schema"] == "CL" and card.get("frame"):
        from .render import fcard
        extra.append({"type": "para", "text": fcard.inverted_frame(card["frame"])})
    ex = None
    if card["defs_style"] == "one_line_examples":
        ex = {}
        if "R1" in sem:
            from .common import quant, money_str, num_str
            u = D(sem["R1u"])
            raw = D("12.345") if u < 1 else D("47.5")
            ex["R1"] = [f"{num_str(raw)} {card['b']['cur']} becomes {money_str(quant(raw, u, sem['R1']), u < 1)} {card['b']['cur']}"]
    return R.card_ir(card, cl, examples=ex, extra_blocks=extra, fewshot=card.get("fewshot_block"))


def to_row(card, spec, rng, *, row_id, var=0, eid=None, inert=None, attack=None, role="clean", style_key=None):
    q, qinfo = question(card, spec, eid, rng)
    spec["decisive"] = decisive_dims(card, spec)
    LP = spec["LP"]

    def doc_fn(single):
        cases = None
        if spec["qkind"] == "cases":
            s = card["b"]
            cols = ["case"] + list(spec["case_keys"])
            rows = []
            for c in spec["cases"]:
                r = [c["ref"]]
                for k in spec["case_keys"]:
                    if k in c["vals"]:
                        r.append(bcard.amt_text(c["vals"][k], card) if k == s.get("amt") or k == s.get("p")
                                 else bcard.num_str(D(c["vals"][k])))
                    else:
                        r.append(str(c["facts"][k]))
                rows.append(r)
            cases = {"type": "table", "caption": card["cases_caption"], "columns": cols, "rows": rows}
        return bcard.doc_ir(card, LP, eid if spec["qkind"] != "cases" else None, inert=inert, attack=attack, cases=cases)
    cir = card_ir_for(card, var)
    row, res, P = rowkit.assemble(card, spec, row_id=row_id, var=var, doc_fn=doc_fn, question=q, qinfo=qinfo,
                                  card_ir_=cir, role=role, style_key=style_key)
    return row, res, P, q


def decisive_dims(card, spec):
    LP = spec["LP"]
    if spec["qkind"] in ("cases",) or LP.get("world") == "open":
        return []
    out = set()

    def lab(rd):
        if spec["qkind"] == "thr":
            return BE.aff(LP, rd)
        if spec["qkind"] == "band":
            return BE.band_of(LP, rd)
        return BE.evaluate(LP, rd)[0]
    try:
        g = lab({})
    except Reject:
        return []
    for eid, rd in bcard.alt_readings(LP, card["shown"]):
        if not eid.startswith("E-alt:"):
            continue
        try:
            if lab(rd) != g:
                out.add(eid.split(":")[1])
        except (Reject, ArithmeticError):
            continue
    return sorted(out)


def can_negate(spec):
    return spec.get("qkind") == "thr"


def with_neg(spec, n):
    s = copy.deepcopy(spec)
    s["LP"]["q"]["neg"] = n
    s["neg"] = n
    s["gold"] = s["aff"] ^ (n % 2 == 1)
    s["tf"] = True
    return s


def boundary_twin(card, spec, rng):
    if spec.get("qkind") != "thr" or spec.get("printed"):
        return None
    LP = spec["LP"]
    s = card["b"]
    keys = [s["q"], s["p"]] if s["computed"] else [s["amt"]]
    u = ONE if s["count"] else s["unit"]
    cands = [(k, d) for k in keys for d in (u, -u)]
    rng.shuffle(cands)
    for k, d in cands:
        LP2 = copy.deepcopy(LP)
        nv = D(LP2["vals"][k]) + (d if k != s.get("q") else (ONE if d > 0 else -ONE))
        if nv <= 0:
            continue
        LP2["vals"][k] = nv
        if not bgen.grid_ok(LP2, card):
            continue
        try:
            a2 = BE.aff(LP2, {})
        except (Reject, ArithmeticError):
            continue
        if a2 != spec["aff"]:
            s2 = copy.deepcopy(spec)
            s2["LP"] = LP2
            s2["aff"] = a2
            s2["gold"] = a2 ^ (spec["neg"] % 2 == 1)
            return s2
    return None


def flip_twin(card, spec, var):
    if spec.get("qkind") not in ("thr", "value", "band") or card["world"] != "closed" or spec.get("printed"):
        return None
    LP = spec["LP"]
    LP2 = copy.deepcopy(LP)
    LP2["sem"] = bgen.var_sem(card, var)
    if not bgen.grid_ok(LP2, card):
        return None
    try:
        if spec["qkind"] == "thr":
            a2 = BE.aff(LP2, {})
            if a2 == spec["aff"]:
                return None
            s2 = copy.deepcopy(spec)
            s2["LP"], s2["aff"], s2["gold"] = LP2, a2, a2 ^ (spec["neg"] % 2 == 1)
            return s2
        if spec["qkind"] == "band":
            g2 = BE.band_of(LP2, {})
            if g2 == spec["gold"] or g2 not in spec["options"]:
                return None
            s2 = copy.deepcopy(spec)
            s2["LP"], s2["gold"] = LP2, g2
            return s2
        v2 = BE.evaluate(LP2, {})[0]
        g2 = bcard.mstr(v2, card)
        if g2 == spec["gold"] or g2 not in spec["options"]:
            return None
        from .options import single_hook_values
        single = {bcard.mstr(v, card): e for v, e in single_hook_values(bcard.hooks(LP2, card["shown"], v2)).items()}
        for o in spec["options"]:
            if o != g2 and o not in single and o != card.get("none_text"):
                return None
        s2 = copy.deepcopy(spec)
        s2["LP"], s2["gold"] = LP2, g2
        return s2
    except (Reject, ArithmeticError):
        return None


def inert_pair(card, spec, rng, used):
    from .mdoc import INERT_LABELS
    labs = [x for x in INERT_LABELS if x.lower() not in used]
    if not labs:
        return None
    lab = rng.choice(labs)
    if lab in ("loyalty points balance", "courier slots booked", "visitor passes issued", "travel time logged"):
        return (lab, str(rng.randint(2, 300)))
    if lab == "previous invoice reference":
        return (lab, f"{card['prefix']}-{rng.randint(1000, 9999)}")
    return (lab, bcard.mstr(D(rng.randint(20, 900)), card))


def labels_in(card):
    s = card["b"]
    out = {s["amt"].lower(), s["charge"].lower(), s["final"].lower()}
    for k in ("q", "p", "lim"):
        if s.get(k):
            out.add(s[k].lower())
    if s["x10"]:
        out.add(s["x10"]["f"].lower())
    return out


def build_fewshot(card, rng):
    exs = []
    for t in range(40):
        if len(exs) >= 1:
            break
        try:
            spec = bgen.gen_row(card, rng, 0, {"neg": 0})
        except Reject:
            continue
        if spec["qkind"] == "cases" or spec.get("printed"):
            continue
        eid = f"{card['prefix']}-{rng.randint(1000, 9999)}"
        spec["tf"] = False
        q, _ = question(card, spec, eid, rng)
        LP = spec["LP"]
        s = card["b"]
        lines = []
        if s["computed"]:
            lines += [f"{s['q']}: {bcard.num_str(D(LP['vals'][s['q']]))}", f"{s['p']}: {bcard.amt_text(LP['vals'][s['p']], card)}"]
        else:
            lines.append(f"{s['amt']}: {bcard.amt_text(LP['vals'][s['amt']], card)}")
        for b in LP["bands"]:
            lo = bcard.num_str(D(b["lo"])) if b.get("lo") is not None else "no lower edge"
            hi = bcard.num_str(D(b["hi"])) if b.get("hi") is not None else "no upper edge"
            rt = bcard.pct_str(D(b["rate"])) if s["rate_kind"] == "pct" else bcard.mstr(b["rate"], card)
            lines.append(f"{b['name']}: {lo} to {hi}, rate {rt}")
        if s["minmax"]:
            lines.append(f"{s['lim']}: {bcard.mstr(LP['vals'][s['lim']], card)}")
        if s["x10"]:
            lines.append(f"{s['x10']['f']}: {LP['facts'][s['x10']['f']]}")
        case = "\n".join(lines) + "\n" + q
        if len(case.split()) > 130:
            continue
        ans = ("Yes" if spec["gold"] else "No") if card["qtype"] == "noul" else spec["gold"]
        exs.append({"case": case, "answer": ans})
    if not exs:
        return None
    return {"type": "fewshot", "template": rng.choice(["FT01", "FT02", "FT05", "FT11", "FT12", "FT14"]), "examples": exs}
