"""Money rows: document IR (values only; R2-12), question text, few-shot and fragment examples."""
from __future__ import annotations

from decimal import Decimal

from . import lex, mcard, money, qtext
from .common import D, ONE, money_str, num_str, pct_str, quant
from .render import BLANK

INERT_LABELS = ["travel time logged", "parking receipt held", "deposit on file", "spare parts set aside",
                "previous invoice reference", "courier slots booked", "loyalty points balance", "visitor passes issued"]


def record_pairs(card, LP, eid, case_keys=()):
    m = card["m"]
    K = mcard.kinds(card)
    pairs = [(f"{card['ent_sg']} ID", eid)] if eid else []
    seen = set()
    for e in m["excs"]:
        for c in e["conds"]:
            f = c["f"]
            if f in seen or f in case_keys:
                continue
            seen.add(f)
            pairs.append((f, str(LP["facts"][f])))
    for ln in m["lines"]:
        k = ln["q"] if ln["p"] in ("mul", "perk") else ln["a"]
        if k in case_keys:
            continue
        kind = "qty" if ln["p"] in ("mul", "perk") else "money"
        pairs.append((k, mcard.value_text(card, LP["vals"][k], kind)))
    for st in m["steps"]:
        if st["op"] == "ded":
            for k in st["v"]:
                pairs.append((k, mcard.mstr(LP["vals"][k], card)))
    for name, v in (LP.get("printed") or {}).items():
        pairs.append((name, mcard.mstr(v, card)))
    return pairs


def schedule_pairs(card, LP):
    m = card["m"]
    K = mcard.kinds(card)
    pairs = []
    for ln in m["lines"]:
        if ln["p"] in ("mul", "perk"):
            pairs.append((ln["r"], mcard.mstr(LP["vals"][ln["r"]], card)))
    for st in m["steps"]:
        if st["op"] in ("disc", "fee", "pctof", "incfee"):
            pairs.append((st["v"], pct_str(LP["vals"][st["v"]])))
        elif st["op"] == "disc2":
            for k in st["v"]:
                pairs.append((k, pct_str(LP["vals"][k])))
        elif st["op"] in ("cap", "min", "add"):
            pairs.append((st["v"], mcard.mstr(LP["vals"][st["v"]], card)))
    for e in m["excs"]:
        kind = K[e["v"]]
        pairs.append((e["v"], pct_str(LP["vals"][e["v"]]) if kind == "pct" else mcard.mstr(LP["vals"][e["v"]], card)))
    return pairs


def doc_ir(card, spec, eid, *, single=False, inert=None, attack=None):
    """The row's document. inert: (label, value text) of an inert value line; attack: the injected line."""
    LP = spec["LP"]
    blocks = []
    if spec.get("qkind") == "cases":
        keys = spec["case_keys"]
        cols = ["case"] + list(keys)
        rows = []
        K = mcard.kinds(card)
        for c in spec["cases"]:
            r = [c["ref"]]
            for k in keys:
                if k in c["vals"]:
                    kind = K.get(k, "money")
                    r.append(mcard.value_text(card, c["vals"][k], kind))
                else:
                    r.append(str(c["facts"][k]))
            rows.append(r)
        rec = record_pairs(card, LP, None, case_keys=set(keys))
        blocks.append({"type": "table", "caption": card["cases_caption"], "columns": cols, "rows": rows})
        sched = schedule_pairs(card, LP) + rec
        blocks.append({"type": "fields", "label": card["sched_label"], "pairs": [list(p) for p in sched]})
    else:
        rec = record_pairs(card, LP, eid)
        if inert:
            rec.append(inert)
        sched = schedule_pairs(card, LP)
        if single:
            blocks.append({"type": "fields", "pairs": [list(p) for p in rec + sched]})
        else:
            blocks.append({"type": "fields", "label": card["rec_label"], "pairs": [list(p) for p in rec]})
            if sched:
                blocks.append({"type": "fields", "label": card["sched_label"], "pairs": [list(p) for p in sched]})
    if attack:
        blocks.append({"type": "para", "text": attack})
    doc = {"blocks": blocks}
    if card.get("doc_title"):
        doc["title"] = card["doc_title"]
    return doc


def question(card, spec, eid, rng):
    """(question text, info) for a money row."""
    m = card["m"]
    LP = spec["LP"]
    qk = spec["qkind"]
    side = card["side_money"]
    res = m["res"]
    if qk == "thr":
        T = mcard.mstr(LP["q"]["T"], card)
        op = LP["q"]["cmp"]
        q, info = qtext.thr_question(res, eid, op, T, LP["q"]["neg"], spec.get("tf", False), rng)
        prop = "up" if op in ("ge", "gt") else "down"
        info["pol"] = qtext.pol_tag(prop, side, LP["q"]["neg"])
        info["cmpfam"] = qtext.cmp_family(op)
        return q, info
    if qk == "op":
        q, info = qtext.owed_question(card["op_item"], eid, LP["q"]["neg"], spec.get("tf", False), rng)
        info["pol"] = qtext.pol_tag("owed", side, LP["q"]["neg"])
        info["cmpfam"] = "op"
        return q, info
    if qk == "value":
        return lex.fill(rng.choice(lex.Q_VALUE), res=res, id=eid), {"neg": 0, "tf": 0, "negcmp": False}
    if qk == "outcome":
        return lex.fill(rng.choice(lex.Q_OUTCOME), kind=card["okind"], id=eid), {"neg": 0, "tf": 0, "negcmp": False}
    if qk == "cases":
        T = mcard.mstr(LP["q"]["T"], card)
        op = LP["q"]["cmp"]
        idx = rng.randrange(len(lex.Q_CMP[op]))
        ph, negcmp, _ = qtext.cmp_phrase(op, T, idx)
        return lex.fill(rng.choice(lex.Q_CASES), res=res, cmpT=ph), {"neg": 0, "tf": 0, "negcmp": negcmp}
    raise ValueError(qk)


def fragment_examples(card, sem):
    """Definition-style examples (one clause on a fragment, no document, no question; R1-29), per card variant."""
    m = card["m"]
    out = {}
    cur = m["cur"]
    dec2 = m["dec2"]
    if "R1" in sem:
        u = D(sem["R1u"])
        mode = sem["R1"]
        if u < 1:
            raw, raw2 = D("12.345"), D("8.212")
        else:
            raw, raw2 = (D("47.5"), D("38.2")) if u == 1 else (D("415"), D("1238"))
        def r(x):
            return quant(x, u, mode)
        fmt = (lambda x: f"{x:f}")
        out["R1"] = [f"{num_str(raw)} {cur} becomes {money_str(r(raw), u < 1)} {cur}",
                     f"{num_str(raw2)} {cur} becomes {money_str(r(raw2), u < 1)} {cur}"]
    if "R5" in sem:
        q = D("2.25")
        res = {"ceil": "3", "floor": "2", "exact": "2.25"}[sem["R5"]]
        out["R5"] = [f"2.25 {m['qpl']} are charged as {res} {m['qpl']}"]
    if "U3" in sem and m.get("k"):
        k = D(m["k"])
        q = k + k / 2
        blocks = {"pro_rata": num_str(q / k), "full_k": "2", "blocks": "1"}.get(sem["U3"], "2")
        out["U3"] = [f"{num_str(q)} {m['qpl']} count as {blocks} blocks of {num_str(k)}"]
    for st in m["steps"]:
        if st["op"] == "cap":
            a, c = (D("520.00"), D("480.00")) if dec2 else (D("520"), D("480"))
            out["X4"] = [f"a computed {money_str(a, dec2)} {cur} with a cap of {money_str(c, dec2)} {cur} gives "
                         f"{money_str(c, dec2)} {cur}"]
        if st["op"] == "min":
            a, c = (D("12.00"), D("25.00")) if dec2 else (D("12"), D("25"))
            out["X4"] = [f"a computed {money_str(a, dec2)} {cur} with a minimum of {money_str(c, dec2)} {cur} gives "
                         f"{money_str(c, dec2)} {cur}"]
        if st["op"] == "disc":
            out["R8"] = [f"a 10% discount on 200 {cur} means paying 180 {cur}"]
    return out
