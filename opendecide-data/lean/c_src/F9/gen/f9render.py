"""F9 renderer: Struct -> `state` (F9's own containers, 1.6), query AST -> question sentence (closed wording, 1.2),
answers -> option strings (T21 / T22 formats). Card text is laid out by fmt1 (f9rows)."""
from __future__ import annotations

import html
import json
import re
from fractions import Fraction

from f9fmt import (fmt_date, fmt_dt, fmt_num, local_parts, round_half_up, to_frac)
from f9lex import CBD, MONTHS, NONE_OPT, CMP_T10, no_record_opt, set_opt, tie_opt
from f9solve_a import CBD as A_CBD, NO_RECORD, NONE, TIE

DEFAULT_FMT = {"nf": "plain", "df": "iso", "tf": "hm", "null_tok": "unknown", "bool": "tf", "csv": ",",
               "zone": 0, "round_dp": 1}


def art(w):
    return "an" if w[:1].lower() in "aeiou" or w[:1] in "AEFHILMNORSX" and w.isupper() else "a"


def cap1(s):
    return s[:1].upper() + s[1:]


def low1(s):
    return s[:1].lower() + s[1:]


# ------------------------------------------------------------------------------------------------ values
def cell_text(v, col, fm, masked=None):
    t = col["type"]
    if v is None:
        return fm["null_tok"]
    if t == "num":
        return fmt_num(to_frac(v), col["dp"], fm["nf"])
    if t == "date":
        return fmt_date(int(v), fm["df"])
    if t == "bool":
        return ("true" if v else "false") if fm["bool"] == "tf" else ("1" if v else "0")
    if t == "cat" and masked and masked["col"] == col["name"]:
        return masked["codes"][v]
    return str(v)


def lit_amount(v, unit, dp, fm):
    return f"{fmt_num(to_frac(v), dp, fm['nf'])} {unit}" if unit else fmt_num(to_frac(v), dp, fm["nf"])


def dp_for(v, coldp):
    q = to_frac(v)
    d = coldp
    while (q * 10 ** d).denominator != 1:
        d += 1
    return d


# ------------------------------------------------------------------------------------------------ predicates
def time_phrase(p, fm, typ="date"):
    f = p["_form"]
    if f == "half_open":
        return f"from {fmt_dt(p['lo'], fm['zone'], fm['df'], fm['tf'])} up to but not including " \
               f"{fmt_dt(p['hi'], fm['zone'], fm['df'], fm['tf'])}"
    D = lambda o: fmt_date(o, fm["df"])  # noqa: E731
    if f == "from_to":
        return f"from {D(p['lo'])} to {D(p['hi'])}"
    if f == "before":
        return f"before {D(p['hi'])}"
    if f == "after":
        return f"after {D(p['lo'])}"
    if f == "on_or_before":
        return f"on or before {D(p['hi'])}"
    if f == "on_or_after":
        return f"on or after {D(p['lo'])}"
    if f == "on":
        return f"on {D(p['lo'])}"
    if f == "in_month":
        import datetime as dt
        d = dt.date.fromordinal(p["lo"])
        return f"in {MONTHS[d.month - 1]} {d.year}"
    if f == "rolling":
        return f"in the {p['_N']} days ending on {D(p['hi'])}"
    raise KeyError(f)


DEFAULT_PH = {">=": "at least {X}", "<=": "at most {X}", ">": "more than {X}", "<": "less than {X}",
              "=": "exactly {X}", "!=": "not equal to {X}"}


def coldef(card, col, role=None):
    sc = card["schema"]
    for k in ("nums", "cats", "dates", "bools", "dim_nums", "dim_cats", "fact_nums", "fact_cats", "fact_dates"):
        for c in sc.get(k) or []:
            if c["name"] == col:
                return c
    if sc.get("obj"):
        for c in sc["obj"]["fields"]:
            if c["name"] == col:
                return c
    if sc.get("list"):
        for c in sc["list"]["sub"]:
            if c["name"] == col:
                return c
    if sc.get("text") and sc["text"]["name"] == col:
        return sc["text"]
    if sc.get("numf") and sc["numf"]["name"] == col:
        return sc["numf"]
    if sc.get("code") and sc["code"]["name"] == col:
        return sc["code"]
    raise KeyError(col)


def atom_text(card, p, fm):
    k = p["k"]
    if k == "not":
        a = p["arg"]
        if a["k"] == "cmp" and a["op"] == "=":
            return f"{a['col']} is not {a['lit']}"
        if a["k"] == "in":
            return f"{a['col']} is neither {a['vals'][0]} nor {a['vals'][1]}"
        raise ValueError("NOT scope outside 1.2")
    col = p.get("col")
    if k == "cmp":
        c = coldef(card, col)
        if c["type"] == "num":
            amt = lit_amount(p["lit"], p.get("unit") or c["unit"], dp_for(p["lit"], c["dp"]), fm)
            ph = p.get("_ph") or DEFAULT_PH[p["op"]]
            return f"{col} is {ph.replace('{X}', amt)}"
        if p["op"] == "=":
            return f"{col} is {p['lit']}"
        if p["op"] == "!=":
            return f"{col} is not equal to {p['lit']}"
        raise ValueError("bad cmp")
    if k == "between":
        c = coldef(card, col)
        u = p.get("unit") or c["unit"]
        return f"{col} is between {lit_amount(p['lo'], u, dp_for(p['lo'], c['dp']), fm)} and " \
               f"{lit_amount(p['hi'], u, dp_for(p['hi'], c['dp']), fm)}"
    if k == "in":
        return f"{col} is {p['vals'][0]} or {p['vals'][1]}"
    if k == "win":
        return f"{col} is {time_phrase(p, fm)}"
    if k == "contains":
        return f'{col} contains "{p["s"]}"'
    raise ValueError(k)


def pred_text(card, p, fm, lead="whose"):
    """'whose <a1>' or 'whose <a1> and whose <a2>' (negated parts last, 1.2)."""
    if p["k"] == "and":
        return f" and {lead} ".join(atom_text(card, a, fm) for a in p["args"]).join([f"{lead} ", ""])
    return f"{lead} {atom_text(card, p, fm)}"


# S6 line phrases ----------------------------------------------------------------------------------------
def line_sg(p):
    lv, op, comp = p.get("level"), p.get("lvl_op", "="), p.get("comp")
    if lv is not None and op == ">=":
        s = f"a line at {lv} or higher"
    elif lv is not None:
        s = f"{art(lv)} {lv} line"
    else:
        s = "a line"
    if comp:
        s += f" from {comp}"
    return s


def line_pl(p):
    lv, op, comp = p.get("level"), p.get("lvl_op", "="), p.get("comp")
    if lv is not None and op == ">=":
        s = f"lines at {lv} or higher"
    elif lv is not None:
        s = f"{lv} lines"
    else:
        s = "lines"
    if comp:
        s += f" from {comp}"
    return s


def lift_text(p):
    if p["k"] == "and":
        return " and ".join(lift_text(a) for a in p["args"])
    if p["k"] == "not":
        a = p["arg"]["a"]
        return f"no {a['level']} line" if a.get("comp") is None else f"no line from {a['comp']}"
    return line_sg(p["a"])


def s6_filter_parts(f):
    """S6 count filter = AND(line atom, [window])."""
    parts = f["args"] if f and f["k"] == "and" else ([f] if f else [])
    line = next((x for x in parts if x["k"] == "line"), {"k": "line"})
    win = next((x for x in parts if x["k"] == "win"), None)
    return line, win


# ------------------------------------------------------------------------------------------------ questions
def line_bare(p):
    s = line_sg(p)
    return s.split(" ", 1)[1]


def find_scope(q):
    while True:
        if q.get("_scope"):
            return True
        if q["op"] in ("not", "thr"):
            q = q["inner"]
            continue
        return False


def question(card, frame, q, fm):
    sc = card["schema"]
    t = _question(card, frame, q, fm)
    if find_scope(q):
        t = f"Among the listed {sc.get('rec_pl') or sc.get('ent_pl')}, {low1(t)}"
    return t


def _question(card, frame, q, fm):
    if q["op"] == "not":
        form = q.get("_neg", "itnc")
        if form == "itnc":
            return f"Is it not the case that {claim(card, frame, q['inner'], fm)}?"
        if form == "there_no":
            return "Is there " + claim(card, frame, q, fm)[len("there is "):] + "?"
        if form == "have_no":
            b = q["inner"]
            return f"Does request {b['req']} have no {b['a']['level']} line?"
        raise KeyError(form)
    return _q(card, frame, q, fm)


def exists_body(card, frame, b, fm):
    sc = card["schema"]
    rs = sc.get("rec_sg")
    if frame == "Y_EXISTS":
        return rs, pred_text(card, b["f"], fm)
    if frame == "Y_TERMX":
        return rs, f"that counts as {b['f']['name']}"
    if frame == "Y_PRES":
        return rs, f"with {card['idcol']} {b['id']}"
    if frame == "Y_LEX":
        line, win = s6_filter_parts(b["f"])
        wt = f" {time_phrase(win, fm, 'dt')}" if win else ""
        return None, line_bare(line) + " logged" + wt
    raise KeyError(frame)


def claim(card, frame, q, fm):
    """Declarative claim of a yes/no question (for 'Is it not the case that <claim>?', 1.7 wide-scope forms)."""
    sc = card["schema"]
    if q["op"] == "not":
        form = q.get("_neg", "itnc")
        if form == "there_no":
            noun, body = exists_body(card, frame, q["inner"], fm)
            return f"there is no {noun} {body}" if noun else f"there is no {body}"
        if form == "have_no":
            b = q["inner"]
            return f"request {b['req']} has no {b['a']['level']} line"
        raise KeyError(form)
    b = q["inner"] if q["op"] == "thr" else q
    if frame in ("Y_EXISTS", "Y_TERMX", "Y_PRES", "Y_LEX"):
        noun, body = exists_body(card, frame, b, fm)
        if noun:
            return f"there is {art(noun)} {noun} {body}"
        line, _ = s6_filter_parts(b["f"])
        return f"there is {line_sg(line).split(' ', 1)[0]} {body}"
    if frame in ("Y_LOOKN", "Y_LOOKC"):
        a = b["p"]
        col = a.get("col") or a["arg"]["col"]
        return f"the {col} of {b['id']} is {atom_text(card, a, fm).split(' is ', 1)[1]}"
    if frame == "Y_TERM":
        a = b["p"]
        if a["k"] == "not":
            return f"{b['id']} does not count as {a['arg']['name']}"
        return f"{b['id']} counts as {a['name']}"
    if frame == "Y_FORALL":
        return f"every {sc['rec_sg']} {pred_text(card, b['a'], fm)} is also one {pred_text(card, b['b'], fm)}"
    if frame == "Y_COMPARE":
        return f"{group_text(card, b, 'a', fm)} is {b['_ph']} {group_text(card, b, 'b', fm)}"
    if frame == "Y_COUNT":
        return f"the number of {sc['rec_pl']} {pred_text(card, b['f'], fm)} is {cmp_count_text(q, fm)}"
    if frame == "Y_MEAN":
        return f"the average {b['col']} of the {sc['rec_pl']} {pred_text(card, b['f'], fm)} is " \
               f"{cmp_amount_text(card, q, fm)}"
    if frame == "Y_ANY":
        it = sc["list"]
        verb = "has no" if b["q"] == "no" else "has any"
        return f"{b['id']} {verb} {it['sg']} {pred_text(card, b['cond'], fm)}"
    if frame == "Y_EVERY":
        it = sc["list"]
        return f"every {it['sg']} of {b['id']} is one {pred_text(card, b['cond'], fm)}"
    if frame == "Y_EANY":
        return f"{b['key']} has any {sc['ev_sg']} {pred_text(card, b['fe'], fm)}"
    if frame == "Y_ESUM":
        tail = f" {pred_text(card, b['fe'], fm)}" if b.get("fe") else ""
        return f"the total {b['col']} of the {sc['ev_pl']} of {b['key']}{tail} is {cmp_amount_text(card, q, fm)}"
    if frame == "Y_GCOUNT":
        return f"the number of {sc['ev_pl']} of the {sc['ent_pl']} {pred_text(card, b['fd'], fm)} is " \
               f"{cmp_count_text(q, fm)}"
    if frame == "Y_LCOUNT":
        line, win = s6_filter_parts(b["f"])
        wt = f" {time_phrase(win, fm, 'dt')}" if win else ""
        return f"the number of {line_pl(line)} logged{wt} is {cmp_count_text(q, fm)}"
    if frame == "Y_REQ":
        return f"request {b['req']} has {line_sg(b['a'])}"
    if frame == "Y_CELL":
        m = sc["measure"]
        return f"the {m['name']} of {b['ent']} in {b['period']} is {cmp_amount_text(card, q, fm, unit=m['unit'])}"
    raise KeyError(frame)


def _q(card, frame, q, fm):
    sc = card["schema"]
    rs, rp = sc.get("rec_sg"), sc.get("rec_pl")
    b = q["inner"] if q["op"] == "thr" else q
    if frame in ("Y_EXISTS", "Y_TERMX", "Y_PRES", "Y_LEX", "Y_LOOKN", "Y_LOOKC", "Y_FORALL", "Y_COMPARE",
                 "Y_COUNT", "Y_MEAN", "Y_EVERY", "Y_ESUM", "Y_GCOUNT", "Y_LCOUNT", "Y_CELL"):
        c = claim(card, frame, q, fm)
        if c.startswith("there is "):
            return "Is there " + c[len("there is "):] + "?"
        if frame in ("Y_FORALL", "Y_EVERY"):
            head, tail = c.split(" is ", 1) if frame == "Y_EVERY" else c.split(" is also one ", 1)
            return f"Is {head} {'also one ' if frame == 'Y_FORALL' else ''}{tail}?"
        if frame == "Y_COMPARE":
            return f"Is {group_text(card, b, 'a', fm)} {b['_ph']} {group_text(card, b, 'b', fm)}?"
        head, tail = _split_is(c)
        return f"Is {head} {tail}?"
    if frame == "Y_TERM":
        a = b["p"]
        if a["k"] == "not":
            return f"Does {b['id']} not count as {a['arg']['name']}?"
        return f"Does {b['id']} count as {a['name']}?"
    if frame == "Y_ANY":
        it = sc["list"]
        verb = "have no" if b["q"] == "no" else "have any"
        return f"Does {b['id']} {verb} {it['sg']} {pred_text(card, b['cond'], fm)}?"
    if frame == "Y_EANY":
        return f"Does {b['key']} have any {sc['ev_sg']} {pred_text(card, b['fe'], fm)}?"
    if frame == "Y_REQ":
        return f"Does request {b['req']} have {line_sg(b['a'])}?"
    if frame == "V_COUNT":
        return f"How many {rp} are there {pred_text(card, b['f'], fm)}?"
    if frame == "V_TCOUNT":
        return f"How many {rp} count as {b['f']['name']}?"
    if frame == "V_SUM":
        c = coldef(card, b["col"])
        return f"In {c['unit']}, what is the total {b['col']} of the {rp} {pred_text(card, b['f'], fm)}?"
    if frame == "V_MEAN":
        c = coldef(card, b["col"])
        return f"In {c['unit']}, what is the average {b['col']} of the {rp} {pred_text(card, b['f'], fm)}?"
    if frame == "V_EXT":
        c = coldef(card, b["col"])
        if c["type"] == "date":
            w = "earliest" if b["op"] == "min" else "latest"
            return f"What is the {w} {b['col']} of the {rp} {pred_text(card, b['f'], fm)}?"
        w = "highest" if b["op"] == "max" else "lowest"
        return f"In {c['unit']}, what is the {w} {b['col']} of the {rp} {pred_text(card, b['f'], fm)}?"
    if frame == "V_LOOK":
        c = coldef(card, b["col"])
        if c["type"] == "num":
            return f"In {c['unit']}, what is the {b['col']} of {b['id']}?"
        return f"What is the {b['col']} of {b['id']}?"
    if frame == "V_CDIST":
        return f"How many different {b['col']} values do the {rp} {pred_text(card, b['f'], fm)} have?"
    if frame == "R_EXT":
        c = coldef(card, b["col"])
        if c["type"] == "date":
            w = "earliest" if b["op"] == "argmin" else "latest"
        else:
            w = "highest" if b["op"] == "argmax" else "lowest"
        return f"Which {rs} {pred_text(card, b['f'], fm)} has the {w} {b['col']}?"
    if frame == "R_COND":
        return f"Which of these {rp} is one {pred_text(card, b['f'], fm)}?"
    if frame == "R_INV":
        return f"Which of these {rp} counts as {b['f']['name']}?"
    if frame == "SET_SEL":
        return f"Which {rp} are the ones {pred_text(card, b['f'], fm)}?"
    if frame == "SET_TERM":
        return f"Which {rp} count as {b['f']['name']}?"
    if frame == "V_ESUM":
        c = coldef(card, b["col"])
        tail = f" {pred_text(card, b['fe'], fm)}" if b.get("fe") else ""
        return f"In {c['unit']}, what is the total {b['col']} of the {sc['ev_pl']} of {b['key']}{tail}?"
    if frame == "V_GCOUNT":
        return f"How many {sc['ev_pl']} belong to the {sc['ent_pl']} {pred_text(card, b['fd'], fm)}?"
    if frame == "V_EATTR":
        c = coldef(card, b["col"])
        if c["type"] == "num":
            return f"In {c['unit']}, what is the {b['col']} of {b['key']}?"
        return f"What is the {b['col']} of {b['key']}?"
    if frame == "E_GMAX":
        tail = f" {pred_text(card, b['fe'], fm)}" if b.get("fe") else ""
        if b["agg"] == "count":
            return f"Which {sc['ent_sg']} has the most {sc['ev_pl']}{tail}?"
        return f"Which {sc['ent_sg']} has the highest total {b['col']} over its {sc['ev_pl']}{tail}?"
    if frame == "E_COND":
        return f"Which of these {sc['ent_pl']} has any {sc['ev_sg']} {pred_text(card, b['f']['fe'], fm)}?"
    if frame == "SET_ENT":
        return f"Which {sc['ent_pl']} have any {sc['ev_sg']} {pred_text(card, b['f']['fe'], fm)}?"
    if frame in ("V_LCOUNT", "V_FIRST", "C_COMP"):
        line, win = s6_filter_parts(b["f"])
        wt = f" {time_phrase(win, fm, 'dt')}" if win else ""
        if frame == "V_LCOUNT":
            return f"How many {line_pl(line)} were logged{wt}?"
        if frame == "V_FIRST":
            w = "first" if b["op"] == "first" else "last"
            return f"At what time was the {w} {line_bare(line)} logged{wt}?"
        return f"Which {sc['comp_sg']} logged the most {line_pl(line)}{wt}?"
    if frame == "C_REQ":
        return f"Which of these requests has {lift_text(b['f'])}?"
    if frame == "SET_REQ":
        return f"Which requests have {lift_text(b['f'])}?"
    if frame == "V_ROWT":
        m = sc["measure"]
        return f"In {m['unit']}, what is the total {m['name']} of {b['ent']} over all periods?"
    if frame == "R_TOP":
        m = sc["measure"]
        return f"Which {sc['ent_sg']} has the {'highest' if b['dir'] == 'max' else 'lowest'} total {m['name']}?"
    if frame == "V_COLC":
        m = sc["measure"]
        amt = lit_amount(b["lit"], m["unit"], 0, fm)
        return f"How many {sc['ent_pl']} have a {m['name']} of {b['_ph'].replace('{X}', amt)} in {b['period']}?"
    raise KeyError(frame)


def _split_is(c):
    """'the X of Y is Z' -> ('the X of Y', 'Z') at the LAST ' is ' that starts the comparison part."""
    i = c.rfind(" is ")
    return c[:i], c[i + 4:]


def cmp_count_text(q, fm):
    return q["_ph"].replace("{X}", fmt_num(to_frac(q["lit"]), 0, fm["nf"]))


def cmp_amount_text(card, q, fm, unit=None):
    b = q["inner"]
    c = None
    try:
        c = coldef(card, b["col"])
    except (KeyError, TypeError):
        pass
    u = q.get("unit") or unit or (c["unit"] if c else None)
    dp = dp_for(q["lit"], c["dp"] if c else 0)
    return q["_ph"].replace("{X}", lit_amount(q["lit"], u, dp, fm))


def group_text(card, b, g, fm):
    rp = card["schema"]["rec_pl"]
    if b["agg"] == "count":
        return f"the number of {rp} {pred_text(card, b[g], fm)}"
    w = "total" if b["agg"] == "sum" else "average"
    return f"the {w} {b['col']} of the {rp} {pred_text(card, b[g], fm)}"


# ------------------------------------------------------------------------------------------------ options
def ans_text(card, frame, q, a, fm, alt=None):
    sc = card["schema"]
    if a == NO_RECORD:
        noun = sc.get("rec_sg") or sc.get("ent_sg") or "line"
        if frame in ("V_FIRST", "V_LCOUNT"):
            noun = "line"
        return no_record_opt(noun)
    if a == A_CBD:
        return CBD
    if a == NONE:
        return NONE_OPT
    if a == TIE:
        return tie_opt(sc.get("rec_pl") or sc.get("ent_pl") or sc.get("comp_pl"))
    if isinstance(a, frozenset):
        if not a:
            noun = sc.get("rec_sg") or sc.get("ent_sg") or "request"
            return no_record_opt(noun)
        return set_opt(a)
    b = q["inner"] if q["op"] in ("thr", "not") else q
    op = b["op"]
    if op in ("count", "cdist", "g_count", "count_lines", "col_count"):
        return fmt_num(Fraction(a), 0, fm["nf"])
    if op in ("first", "last"):
        return fmt_dt(int(a), fm["zone"], fm["df"], fm["tf"])
    if op in ("argmax", "argmin", "g_argmax", "comp_argmax", "cpick", "row_top"):
        return str(a)
    col = b.get("col")
    if op in ("row_total", "cell"):
        return fmt_num(to_frac(a), 0, fm["nf"])
    c = coldef(card, col)
    if c["type"] == "num":
        v = to_frac(a)
        if op == "mean":
            from f9solve_a import display_round
            v = display_round(v, fm["round_dp"], alt)
            return fmt_num(v, fm["round_dp"], fm["nf"])
        return fmt_num(v, c["dp"], fm["nf"])
    if c["type"] == "date":
        return fmt_date(int(a), fm["df"])
    if c["type"] == "cat" and card.get("masked") and card["masked"]["col"] == col and not fm.get("_short"):
        return card["masked"]["codes"][a]
    return str(a)


# ------------------------------------------------------------------------------------------------ JSON / YAML
def json_num(v, dp):
    return fmt_num(to_frac(v), dp, "plain")


def _jval(v, col):
    if v is None:
        return "null"
    t = col["type"]
    if t == "num":
        return json_num(v, col["dp"])
    if t == "bool":
        return "true" if v else "false"
    return json.dumps(str(v), ensure_ascii=False)


def _jsub(sub, subcols):
    return "{" + ", ".join(f'"{c["name"]}": {_jval(x, c)}' for c, x in zip(subcols, sub)) + "}"


def json_record(rec, cols, fm, pretty, indent="  "):
    """rec: dict col -> value; cols: list of col dicts (S4: top-level, obj.* fields, list col). Dates as strings."""
    parts = []
    obj = {}
    for c in cols:
        if "." in c["name"]:
            o, f = c["name"].split(".", 1)
            obj.setdefault(o, []).append((f, c))
    seen_obj = set()
    for c in cols:
        n = c["name"]
        if c.get("_absent"):
            continue
        if "." in n:
            o = n.split(".", 1)[0]
            if o in seen_obj:
                continue
            seen_obj.add(o)
            inner = ", ".join(f'"{f}": {_jv(rec[o + "." + f], cc, fm)}' for f, cc in obj[o])
            parts.append((o, "{" + inner + "}"))
        elif c["type"] == "list":
            v = rec[n]
            if v is None:
                parts.append((n, "null"))
            else:
                parts.append((n, "[" + ", ".join(_jsub(s, c["sub"]) for s in v) + "]"))
        else:
            parts.append((n, _jv(rec[n], c, fm)))
    if pretty:
        body = (",\n" + indent * 2).join(f'"{k}": {v}' for k, v in parts)
        return indent + "{\n" + indent * 2 + body + "\n" + indent + "}"
    return "{" + ", ".join(f'"{k}": {v}' for k, v in parts) + "}"


def _jv(v, c, fm):
    if v is None:
        return "null"
    if c["type"] == "date":
        return json.dumps(fmt_date(int(v), fm["df"]))
    if c["type"] == "cat" and fm.get("_masked") and fm["_masked"]["col"] == c["name"]:
        return json.dumps(fm["_masked"]["codes"][v])
    return _jval(v, c)


def yaml_scalar(v, c, fm):
    if v is None:
        return "null"
    t = c["type"]
    if t == "num":
        return json_num(v, c["dp"])
    if t == "bool":
        return "true" if v else "false"
    if t == "date":
        return json.dumps(fmt_date(int(v), fm["df"]))
    s = str(v)
    if t == "cat" and fm.get("_masked") and fm["_masked"]["col"] == c["name"]:
        s = fm["_masked"]["codes"][v]
    return json.dumps(s, ensure_ascii=False)  # every string is double-quoted (YAML 1.1 coercion never applies)


def yaml_records(recs, cols, fm):
    lines = []
    for rec in recs:
        first = True
        seen_obj = set()
        for c in cols:
            n = c["name"]
            pre = "- " if first else "  "
            if "." in n:
                o = n.split(".", 1)[0]
                if o in seen_obj:
                    continue
                seen_obj.add(o)
                lines.append(f"{pre}{o}:")
                for c2 in cols:
                    if c2["name"].startswith(o + "."):
                        lines.append(f"    {c2['name'].split('.', 1)[1]}: {yaml_scalar(rec[c2['name']], c2, fm)}")
            elif c["type"] == "list":
                v = rec[n]
                if v is None:
                    lines.append(f"{pre}{n}: null")
                elif not v:
                    lines.append(f"{pre}{n}: []")
                else:
                    lines.append(f"{pre}{n}:")
                    for s in v:
                        for j, (sc, x) in enumerate(zip(c["sub"], s)):
                            lines.append(f"    {'- ' if j == 0 else '  '}{sc['name']}: {yaml_scalar(x, sc, fm)}")
            else:
                lines.append(f"{pre}{n}: {yaml_scalar(rec[n], c, fm)}")
            first = False
    return "\n".join(lines)


# ------------------------------------------------------------------------------------------------ tables
def header_label(c, fw=False):
    if c["type"] == "num" and c.get("unit"):
        return f"{c['name']}({c['unit']})" if fw else f"{c['name']} ({c['unit']})"
    return c["name"]


def table_text(kind, cols, rows, fm, masked=None):
    """kind: md | csv | html | fw | kv. rows: list of value lists aligned with cols."""
    cells = [[cell_text(v, c, fm, masked) for v, c in zip(r, cols)] for r in rows]
    if kind == "md":
        hdr = [header_label(c) for c in cols]
        out = ["| " + " | ".join(hdr) + " |", "| " + " | ".join("---" for _ in hdr) + " |"]
        out += ["| " + " | ".join(x.replace("|", "\\|") for x in r) + " |" for r in cells]
        return "\n".join(out)
    if kind == "csv":
        import csv
        import io
        buf = io.StringIO()
        w = csv.writer(buf, delimiter=fm["csv"], lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow([header_label(c) for c in cols])
        for r in cells:
            w.writerow(r)
        return "```csv\n" + buf.getvalue().rstrip("\n") + "\n```"
    if kind == "html":
        out = ["<table>", "  <tr>" + "".join(f"<th>{html.escape(header_label(c))}</th>" for c in cols) + "</tr>"]
        for r in cells:
            out.append("  <tr>" + "".join(f"<td>{html.escape(x)}</td>" for x in r) + "</tr>")
        out.append("</table>")
        return "\n".join(out)
    if kind == "fw":
        hdr = [header_label(c, fw=True) for c in cols]
        w = [max(len(h), *(len(r[j]) for r in cells)) if cells else len(h) for j, h in enumerate(hdr)]
        line = lambda xs: "  ".join(x.ljust(w[j]) for j, x in enumerate(xs)).rstrip()  # noqa: E731
        return "```table\n" + "\n".join([line(hdr)] + [line(r) for r in cells]) + "\n```"
    if kind == "kv":
        blocks = []
        for r in cells:
            blocks.append("\n".join(f"{header_label(c)}: {x}" for c, x in zip(cols, r)))
        return "```records\n" + "\n\n".join(blocks) + "\n```"
    raise KeyError(kind)


# ------------------------------------------------------------------------------------------------ logs (S6)
SYNTAXES = ("bracket", "isocomp", "kv", "syslog")


def log_line(syntax, r, fm, numf, code):
    t = fmt_dt(int(r["time"]), fm["zone"], fm["df"], fm["tf"])
    kv = []
    if r.get("request"):
        kv.append(f"req={r['request']}")
    if r.get(code) is not None:
        kv.append(f"{code}={r[code]}")
    if r.get(numf["name"]) is not None:
        kv.append(f"{numf['name']}={fmt_num(to_frac(r[numf['name']]), 0, fm['nf'])}")
    msg = r["message"]
    tail = (" " + " ".join(kv)) if kv else ""
    if syntax == "bracket":
        return f"[{t}] [{r['level']}] {r['component']}: {msg}{tail}"
    if syntax == "isocomp":
        return f"{t} {r['component']} {r['level']} {msg}{tail}"
    if syntax == "kv":
        return f'time="{t}" level={r["level"]} component={r["component"]} msg="{msg}"{tail}'
    if syntax == "syslog":
        return f"{t} {r['component']}[{r['level']}]: {msg}{tail}"
    raise KeyError(syntax)


def log_text(syntax, rows, cols, fm, numf, code, fence):
    names = [c["name"] for c in cols]
    lines = [log_line(syntax, dict(zip(names, r)), fm, numf, code) for r in rows]
    if fence == "indent":
        return "\n".join("    " + ln for ln in lines)
    return "```log\n" + "\n".join(lines) + "\n```"
