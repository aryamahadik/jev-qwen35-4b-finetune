"""Engine adapter for S4 calendar and business-day cards."""
from __future__ import annotations

import copy
import datetime as dt

from . import dateeval as DE, dcard, dgen, lex, qtext, render as R, rowkit
from .cards import common_card, style_set, DV_BY_STYLE, case_ref_fn
from .money import Reject, gate_true
from .mrows import gen_entity_id

NAME = "date"
TASKS_D = ["Apply these date rules to the {ent} in the text.", "Use these rules to settle the question about the {ent} in the text."]


def make_card(card, pack, rng, **kw):
    common_card(card, pack, rng)
    if card["schema"] == "CH-O" and card["world"] == "closed" and not card.get("force_ext"):
        card["no_ext"] = True
    dcard.build(card, pack, rng)
    s = card["d"]
    if card.get("no_ext") and s["ext"] and not card.get("force_ext"):
        s["ext"] = None
        s["sem"].pop("D12", None)
        card["shown"].discard("D12")
    sem = s["sem"]
    flips = []
    if "D4" in sem:
        flips.append(("D4", {"D4": "b"}))
    if "D7" in sem:
        flips.append(("D7", {"D7": rng.choice([x for x in ("fwd", "back", "none") if x != sem["D7"]])}))
    if s["ext"]:
        flips.append(("D12", {"D12": "post"}))
    if "D5" in sem:
        flips.append(("D5", {"D5": "both" if sem["D5"] == "excl" else "excl"}))
    if "D14" in sem:
        flips.append(("D14", {"D14": "both" if sem["D14"] == "after" else "after"}))
    if "B1w" in sem:
        flips.append(("B1", {"B1w": "lower" if sem["B1w"] == "upper" else "upper"}))
    rng.shuffle(flips)
    card["variants"] = [{"dim": d, "over": o} for d, o in flips[:rng.choice([1, 2, 2])]]
    card["short"] = False
    card["defs_style"] = rng.choice(["one_line", "decision_list", "one_line"]) if card["instr"] != "fewshot" else "one_line"
    card["dv"] = rng.choice(DV_BY_STYLE[card["defs_style"]])
    card["task"] = rng.choice(TASKS_D).format(ent=card["ent_sg"])
    card["none_ok"] = card["schema"] == "CL" and rng.random() < 0.4
    card["none_text"] = "None of the listed cases"
    if card["schema"] == "CL":
        card["case_ref_id"] = rng.choice(["IVN01", "IVN03", "IVN04", "IVN05", "IVN07"])
        card["case_refs"] = case_ref_fn(card)
        card["ncase_choices"] = [5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20]
        card["frame"] = None if card["none_ok"] else rng.choice(["IVC04", "IVC05", None])
    card["open_k"] = [3]
    card["styles"] = style_set(rng, card["card_id"], card.get("held_out", False), card["schema"] == "CL")
    if card["instr"] == "fewshot":
        card["instr"] = "std"     # S4 few-shot examples need a strip per example; the S4 few-shot card is skipped
    return card


def gen_row(card, rng, var=0, want=None):
    return dgen.gen_row(card, rng, var, want)


def new_eid(card, rng, used):
    return gen_entity_id(card, rng, used)


def question(card, spec, eid, rng):
    s = card["d"]
    qk = spec["qkind"]
    act = s["act_w"]
    side = card["side_date"]
    if qk in ("ontime", "late"):
        neg = spec["LP"]["q"]["neg"]
        tf = spec.get("tf", False) or neg > 0
        info = {"neg": neg, "tf": int(tf)}
        pos = lex.P_ONTIME if qk == "ontime" else lex.P_LATE
        if not tf:
            q = lex.fill(rng.choice(lex.Q_ONTIME if qk == "ontime" else lex.Q_LATE), act=act, id=eid)
        else:
            frame = rng.choice(lex.TF_FRAMES)
            if neg == 0:
                P = lex.fill(rng.choice(pos), act=act, id=eid)
            elif neg == 1:
                if rng.random() < 0.5:
                    P = lex.fill(rng.choice(lex.P_ONTIME_NEG if qk == "ontime" else lex.P_LATE_NEG), act=act, id=eid)
                else:
                    P = lex.OPN + lex.fill(rng.choice(pos), act=act, id=eid)
            else:
                P = lex.OPN + lex.fill(rng.choice(lex.P_ONTIME_NEG[:1] if qk == "ontime" else lex.P_LATE_NEG), act=act, id=eid)
            q = frame.replace("{P}", P)
        info["pol"] = qtext.pol_tag("ontime" if qk == "ontime" else "late", side, neg)
        return q, info
    if qk == "lastday":
        return lex.fill(rng.choice(lex.Q_LASTDAY), act=act, id=eid), {"neg": 0, "tf": 0}
    if qk == "count":
        return lex.fill(rng.choice(lex.Q_COUNT), cnt=s["cnt"], id=eid), {"neg": 0, "tf": 0}
    if qk == "window":
        return lex.fill(rng.choice(lex.Q_WINDOW), wkind=s["wkind"], act=act, id=eid), {"neg": 0, "tf": 0}
    if qk == "cases":
        return rng.choice(lex.Q_CASES_LATE), {"neg": 0, "tf": 0}
    raise ValueError(qk)


def doc_ir(card, spec, eid, inert=None, attack=None):
    s = card["d"]
    LP = spec["LP"]
    rec = []
    relevant = []
    extra = []
    if spec["qkind"] == "cases":
        cols = ["case", s["evt"], s["act"]] + ([c["f"] for c in s["ext"]["conds"]] if s["ext"] else [])
        rows = []
        for c in spec["cases"]:
            r = [c["ref"], dcard.dstr(card, c["dates"][s["evt"]]), dcard.dstr(card, c["dates"][s["act"]])]
            r += [c["facts"][cc["f"]] for cc in s["ext"]["conds"]] if s["ext"] else []
            rows.append(r)
            relevant += list(c["dates"].values())
            L2 = {**LP, "dates": c["dates"], "facts": c["facts"], "q": {"kind": "late", "neg": 0}}
            for eid_, rd in dcard.alt_readings(L2, card["shown"]):
                try:
                    extra.append(DE.last_day(L2, rd)[0])
                except Reject:
                    pass
            extra.append(DE.last_day(L2)[0])
        blocks = [{"type": "table", "caption": card["cases_caption"], "columns": cols, "rows": rows}]
    else:
        rec.append((f"{card['ent_sg']} ID", eid))
        for k in (s["evt"], s["act"]):
            if k in LP["dates"]:
                rec.append((k, dcard.dstr(card, LP["dates"][k])))
                relevant.append(LP["dates"][k])
        if s["ext"]:
            for c in s["ext"]["conds"]:
                rec.append((c["f"], str(LP["facts"][c["f"]])))
        blocks = []
        if spec["qkind"] in ("ontime", "late", "lastday", "window"):
            fsets = [LP["facts"]]
            unk = [k for k, v in LP["facts"].items() if v == "not recorded"]
            if unk:
                dom = (LP.get("cats") or {}).get(unk[0]) or ["yes", "no"]
                fsets = [{**LP["facts"], unk[0]: x} for x in dom]
            for fs in fsets:
                for rd in [{}] + [x[1] for x in dcard.alt_readings(LP, card["shown"])]:
                    try:
                        extra.append(DE.last_day(LP, rd, facts=fs)[0])
                    except Reject:
                        pass
        extra += spec.get("opt_dates", []) + spec.get("edge_dates", [])
    if inert:
        rec.append(inert)
    if s["d6a"]:
        hol = LP.get("holidays", [])
        rec.append((lex.HOL_NOTE, "; ".join(dcard.dstr(card, h) for h in hol) if hol else "none"))
    rel_all = relevant + [x for x in extra if isinstance(x, dt.date)]
    if dcard.needs_strip(card, LP, rel_all):
        anchors = [LP["dates"][s["evt"]]] if s["evt"] in LP.get("dates", {}) else []
        if spec["qkind"] == "cases":
            anchors = [c["dates"][s["evt"]] for c in spec["cases"]]
        strip = strip_for(card, LP, rel_all, anchors)
        rec.append((lex.STRIP_NOTE, "; ".join(dcard.dstr(card, d) for d in strip)))
    if rec:
        blocks.append({"type": "fields", "label": card["rec_label"], "pairs": [list(p) for p in rec]})
    if attack:
        blocks.append({"type": "para", "text": attack})
    doc = {"blocks": blocks}
    if card.get("doc_title"):
        doc["title"] = card["doc_title"]
    return doc


def strip_for(card, LP, rel, anchor_dates=()):
    """Strip span: every relevant date with independent 3-10 day margins, <= 45 dates; if longer, the anchor leaves the
    relevant set (a local strip; D9 still states the anchor's weekday); else the row is resampled (1.1)."""
    import random
    rng = random.Random(str(sorted(str(x) for x in rel)))
    m1, m2 = rng.randint(3, 10), rng.randint(3, 10)
    anchors = set(anchor_dates)
    for rr in (rel, [x for x in rel if x not in anchors]):
        if not rr:
            continue
        lo, hi = min(rr) - dt.timedelta(days=m1), max(rr) + dt.timedelta(days=m2)
        n = (hi - lo).days + 1
        if n <= 45:
            return [lo + dt.timedelta(days=i) for i in range(n)]
    raise Reject("strip too long")


def card_ir_for(card, var):
    sem = dgen.var_sem(card, var)
    cl = dcard.clauses(card, sem, card["shown"], card["world"])
    extra = []
    if card["schema"] == "CH-O":
        extra.append({"type": "para", "text": lex.fill(lex.WIN_INTRO, act=card["d"]["act_w"], kind=card["d"]["wkind"])})
        extra.append({"type": "items", "items": dcard.window_items(card, sem)})
    if card["schema"] == "CL" and card.get("frame"):
        from .render import fcard
        extra.append({"type": "para", "text": fcard.inverted_frame(card["frame"])})
    return R.card_ir(card, cl, extra_blocks=extra)


def to_row(card, spec, rng, *, row_id, var=0, eid=None, inert=None, attack=None, role="clean", style_key=None):
    q, qinfo = question(card, spec, eid, rng)
    spec["decisive"] = decisive_dims(card, spec)
    doc_fn = lambda single: doc_ir(card, spec, eid, inert=inert, attack=attack)  # noqa: E731
    cir = card_ir_for(card, var)
    row, res, P = rowkit.assemble(card, spec, row_id=row_id, var=var, doc_fn=doc_fn, question=q, qinfo=qinfo,
                                  card_ir_=cir, role=role, style_key=style_key)
    if any(t.startswith("aid:") for t in row["meta"]["edge"]) is False and "calendar" in row["state"]:
        row["meta"]["edge"] = sorted(set(row["meta"]["edge"] + ["aid:strip"]))
    return row, res, P, q


def decisive_dims(card, spec):
    LP = spec["LP"]
    if spec["qkind"] == "cases" or LP.get("world") == "open":
        return []
    out = set()
    try:
        g = DE.answer(LP)
    except Reject:
        return []
    for eid, rd in dcard.alt_readings(LP, card["shown"]):
        if not eid.startswith("E-alt:"):
            continue
        try:
            if DE.answer(LP, rd) != g:
                out.add(eid.split(":")[1])
        except Reject:
            continue
    return sorted(out)


def can_negate(spec):
    return spec.get("qkind") in ("ontime", "late")


def with_neg(spec, n):
    s = copy.deepcopy(spec)
    s["LP"]["q"]["neg"] = n
    s["neg"] = n
    s["gold"] = s["aff"] ^ (n % 2 == 1)
    s["tf"] = True
    return s


def boundary_twin(card, spec, rng):
    """Move the act date by one day across the last allowed day (MR10)."""
    if spec.get("qkind") not in ("ontime", "late"):
        return None
    LP = spec["LP"]
    for dd in (1, -1):
        LP2 = copy.deepcopy(LP)
        a = LP2["dates"][LP2["act"]] + dt.timedelta(days=dd)
        if a <= LP2["dates"][LP2["evt"]]:
            continue
        LP2["dates"][LP2["act"]] = a
        try:
            a2 = DE.answer(LP2)
        except Reject:
            continue
        if a2 != spec["aff"]:
            s2 = copy.deepcopy(spec)
            s2["LP"], s2["aff"], s2["gold"] = LP2, a2, a2 ^ (spec["neg"] % 2 == 1)
            return s2
    return None


def flip_twin(card, spec, var):
    if spec.get("qkind") not in ("ontime", "late", "lastday", "count", "window") or card["world"] != "closed":
        return None
    LP = spec["LP"]
    LP2 = copy.deepcopy(LP)
    LP2["sem"] = dgen.var_sem(card, var)
    try:
        a2 = DE.answer(LP2)
        a1 = DE.answer(LP)
    except Reject:
        return None
    if a2 == a1:
        return None
    s2 = copy.deepcopy(spec)
    s2["LP"] = LP2
    if spec["qkind"] in ("ontime", "late"):
        s2["aff"], s2["gold"] = a2, a2 ^ (spec["neg"] % 2 == 1)
        return s2
    if spec["qkind"] == "lastday":
        g2 = dcard.dstr(card, a2, wd=False)
    elif spec["qkind"] == "count":
        g2 = f"{a2} " + ("calendar days" if card["d"]["ckind"] == "cal" else "business days")
    else:
        g2 = a2
    if g2 not in spec["options"]:
        return None
    s2["gold"] = g2
    return s2


def inert_pair(card, spec, rng, used):
    labs = [x for x in ("file reference", "previous visit date", "courier tracking number", "pages enclosed")
            if x not in used]
    if not labs:
        return None
    lab = rng.choice(labs)
    if lab == "previous visit date":
        ev = spec["LP"]["dates"].get(card["d"]["evt"])
        if ev is None:
            return None
        return (lab, dcard.dstr(card, ev - dt.timedelta(days=rng.randint(60, 300))))
    if lab == "pages enclosed":
        return (lab, str(rng.randint(2, 40)))
    return (lab, f"{card['prefix']}-{rng.randint(1000, 9999)}")


def labels_in(card):
    s = card["d"]
    out = {s["evt"].lower(), s["act"].lower()}
    if s["ext"]:
        out |= {c["f"].lower() for c in s["ext"]["conds"]}
    return out
