"""G3 round trip (1.6 checks) for one row: parse the rendered row (f9parse / f9qparse), rebuild the structure hash,
compare the parsed query with the generator's (normal form), run solver B (f9solve_b) on the parsed structure and
check gold, the single correct option, and every option's tag reproduction. Returns (ok, reason)."""
from __future__ import annotations

import re
from fractions import Fraction

from f9alt import REWRITE, rewrite
from f9ast import q_equal, structure_hash
from f9fmt import (DATE_RE, NUM_FORMATS, fmt_date, fmt_dt, fmt_num, num_regex, parse_date, parse_dt, parse_num,
                   to_frac)
from f9lex import CBD as CBD_TXT, NONE_OPT, id_key
from f9parse import (Fmt, KIND, ParseError, QP, fail, find_blocks, parse_card, parse_grid, parse_log, parse_pivot,
                     parse_s4, split_instructions, table_from_grid)
from f9qparse import QParser
from f9solve_b import CBD, NO_RECORD, NONE, SPECIALS, TIE, BReject, BUndefined, SolverB, half_even, half_up
from fmt1 import pool as fpool

_W = None


def wordings():
    global _W
    if _W is None:
        from f9cards import f9_wordings
        _W = {w["id"]: w["text"] for w in f9_wordings()}
    return _W


# ------------------------------------------------------------------------------------------------ parse a row
def parse_row(row):
    m = row["meta"]
    st = fpool.style(m["format_style"])
    ip = fpool.instr_position(st["instr_position"])
    reg = fpool.register(st["register"])
    qpre = reg["q_prefix"] if ip["q_prefix"] else ""
    card_text, qtext = split_instructions(row, wordings()[m["wording_id"]], {"ip": ip["id"]}, qpre)
    c = parse_card(card_text)
    mode = "none" if not card_text else ("full" if c.get("df") else "short")
    blocks = find_blocks(row["state"])
    kinds = [k for k, _ in blocks if k not in ("caption", "pivot_caption")]
    if any(k in ("json", "jsonl", "yaml") for k in kinds):
        sampler = "S4"
    elif any(k in ("log", "indent") for k in kinds):
        sampler = "S6"
    elif any(k == "pivot_caption" for k, _ in blocks):
        sampler = "S5"
    elif len(kinds) == 2:
        sampler = "S3"
    elif len(kinds) == 1:
        sampler = m["sampler"] if m["sampler"] in ("S1", "S2") else fail("sampler")
    else:
        fail("container count")
    if sampler != m["sampler"] and not (sampler in ("S1", "S2") and m["sampler"] in ("S1", "S2")):
        fail("sampler differs from meta")
    fm = Fmt(c, sampler)
    tables = []
    if sampler in ("S1", "S2"):
        k, body = blocks[0] if blocks[0][0] != "caption" else blocks[1]
        hdr, data = parse_grid(KIND[k], body, fm)
        tables.append(table_from_grid(hdr, data, fm, "main"))
    elif sampler == "S3":
        grids = [(k, b) for k, b in blocks if k != "caption"]
        caps = [b for k, b in blocks if k == "caption"]
        if len(caps) != 2:
            fail("captions")
        for (k, body), role in zip(grids, ("dim", "fact")):
            hdr, data = parse_grid(KIND[k], body, fm)
            tables.append(table_from_grid(hdr, data, fm, role))
        key = tables[0]["cols"][0]["name"]
        fk = [c2 for c2 in tables[1]["cols"] if c2["name"] == key]
        if not fk:
            fail("no key column in the events table")
        fk[0]["type"] = "fk"
        dimkeys = {r[0] for r in tables[0]["rows"]}
    elif sampler == "S4":
        k, body = [(k, b) for k, b in blocks][0]
        tables.append(parse_s4(k, body, fm))
    elif sampler == "S6":
        k, body = blocks[0]
        syn, lines, keys = parse_log(body, fm)
        others = [x for x in keys if x != "req"]
        num_k = [x for x in others if all(re.fullmatch(num_regex(fm.nf), ln["kv"][x]) for ln in lines if x in ln["kv"])]
        cat_k = [x for x in others if x not in num_k]
        if len(num_k) > 1 or len(cat_k) > 1:
            fail("log fields")
        cols = [{"name": "time", "type": "dt"}, {"name": "level", "type": "lvl"},
                {"name": "component", "type": "comp"}, {"name": "request", "type": "req"}]
        if cat_k:
            cols.append({"name": cat_k[0], "type": "cat"})
        if num_k:
            cols.append({"name": num_k[0], "type": "num", "unit": None, "dp": 0})
        cols.append({"name": "message", "type": "cat"})
        rows = []
        for ln in lines:
            r = [ln["time"], ln["level"], ln["component"], ln["kv"].get("req", "")]
            if cat_k:
                r.append(ln["kv"].get(cat_k[0]))
            if num_k:
                v = ln["kv"].get(num_k[0])
                r.append(None if v is None else parse_num(v, fm.nf))
            r.append(ln["message"])
            rows.append(r)
        tables.append({"role": "log", "cols": cols, "rows": rows})
    else:
        body = [b for k, b in blocks if k == "md"][0]
        pv = parse_pivot(body, fm)
    # ---- a numeric column whose unit is stated only on the card (T28 Units clause; S4 JSON / YAML keys name none)
    #      carries that unit into solver B too, so a restated column (MR22) compares through the stated factor
    for t in tables:
        for col in t["cols"]:
            subs = (col.get("sub") or []) if col["type"] == "list" else [col]
            for cc in subs:
                if cc.get("type") == "num" and not cc.get("unit") and fm.units.get(cc["name"]):
                    cc["unit"] = fm.units[cc["name"]]
    # ---- column registry for the question parser
    cols = {}
    for t in tables:
        for col in t["cols"]:
            u = col.get("unit") or (fm.units.get(col["name"]) if col["type"] == "num" else None)
            cols.setdefault(col["name"], {"type": col["type"], "unit": u, "role": t["role"], "dp": col.get("dp")})
    if sampler == "S6":
        for nm, u in fm.units.items():
            if nm in cols:
                cols[nm]["unit"] = u
    card_ctx = {"conv": c.get("conv", {}), "t10": c.get("t10"), "check_t10": mode in ("full", "short")}
    qp = QP(cols, fm, card_ctx)
    item_qp = None
    lst = None
    if sampler == "S4":
        lc = [col for col in tables[0]["cols"] if col["type"] == "list"]
        if lc:
            lst = lc[0]["name"]
            icols = {s["name"]: {"type": s["type"], "unit": fm.units.get(s["name"]), "role": "item", "dp": s.get("dp")}
                     for s in lc[0]["sub"]}
            item_qp = QP(icols, fm, card_ctx)
    fact_qp = qp
    if sampler == "S3":
        fact_qp = QP({k: v for k, v in cols.items() if v["role"] == "fact"}, fm, card_ctx)
    # terms (T7-T9, T30)
    terms = {}
    for name, t in (c.get("terms") or {}).items():
        tt = {"name": name, "kind": t["kind"]}
        if t["kind"] == "T7":
            tt["A"], tt["B"] = qp.atom(t["_A"]), qp.atom(t["_B"])
        elif t["kind"] == "T8":
            tt["A"], tt["C"] = qp.atom(t["_A"]), qp.atom(t["_C"])
        else:
            tt["list"] = [qp.atom(x) for x in t["_L"]]
        ovs = []
        for v, cond in t.get("_O", []):
            a = qp.atom(cond)
            ovs.append({"val": v, "cond": a})
        if ovs:
            # all overrides key on the column whose category values include the named value
            keycol = None
            for t2 in tables:
                for col in t2["cols"]:
                    if col["type"] == "cat" and all(any(str(r[t2["cols"].index(col)]).lower() == o["val"].lower()
                                                        for r in t2["rows"] if r[t2["cols"].index(col)] is not None)
                                                    or True for o in ovs):
                        pass
            keycol = _override_col(ovs, tables, c, t)
            for o in ovs:
                o["col"] = keycol
            tt["overrides"] = ovs
        terms[name] = tt
    qctx = {"sampler": sampler, "terms": set(terms), "levels": c.get("levels") or _levels_seen(tables),
            "item_qp": item_qp, "list": lst, "fact_qp": fact_qp}
    q = QParser(qp, qctx).parse(qtext)
    # T5 domains
    t5 = {}
    if c.get("missing") == "T5":
        t5 = parse_t5(c["t5"], cols, fm)
    stated = {}
    if mode != "none":
        stated["world"] = c.get("world") or fail("no world clause")
        if c.get("missing"):
            stated["missing"] = c["missing"]
            stated["null"] = c.get("null") or fail("no null token")
        if mode == "short":
            stated["t10"] = sorted(c.get("t10") or [])
        else:
            stated["t21"] = [fm.nf, fm.df, c.get("tf") if sampler == "S6" else None,
                             c.get("zone") if sampler == "S6" else None, c.get("csv")]
            stated["tie"] = c.get("tie")
            stated["round_dp"] = c.get("round_dp")
            stated["bool"] = c.get("bool")
            stated["merged"] = c.get("merged") if sampler == "S6" else None
            stated["terms"] = sorted(terms)
            lg = c.get("legend")
            stated["masked"] = sorted((v, k) for k, v in lg["codes"].items()) if lg else None
    if sampler == "S5":
        btables = [{"role": "pivot", "cols": [{"name": "entity", "type": "id"}, {"name": "period", "type": "cat"},
                                              {"name": "value", "type": "num", "dp": 0},
                                              {"name": "marked", "type": "bool"}],
                    "rows": [[e, p, Fraction(pv["cells"][e][j]), [e, j] in pv["marks"]]
                             for e in pv["entities"] for j, p in enumerate(pv["periods"])]}]
    else:
        btables = tables
    idcol = tables[0]["cols"][0]["name"] if tables else "entity"
    ctx = {"sampler": sampler, "world": c.get("world", "T1"), "missing": c.get("missing"), "t5": t5,
           "terms": terms, "tie": c.get("tie"), "levels": qctx["levels"], "round_dp": c.get("round_dp", 1),
           "conv": c.get("conv", {}), "zone": fm.zone, "idcol": idcol, "key": idcol}
    P = {"sampler": sampler, "mode": mode, "card": c, "fm": fm, "tables": tables, "btables": btables, "q": q,
         "ctx": ctx, "stated": stated, "qtext": qtext, "cols": cols}
    P["render_key"] = lambda qq, a: render_payload(P, qq, a)
    P["options"] = parse_options(P, row)
    return P


def _levels_seen(tables):
    for t in tables:
        if t["role"] == "log":
            j = [c["name"] for c in t["cols"]].index("level")
            return sorted({r[j] for r in t["rows"]})
    return []


def _override_col(ovs, tables, c, t):
    vals = {o["val"].lower() for o in ovs}
    cands = []
    for t2 in tables:
        for j, col in enumerate(t2["cols"]):
            if col["type"] != "cat":
                continue
            seen = {str(r[j]).lower() for r in t2["rows"] if r[j] is not None}
            dom = set(seen)
            cands.append((col["name"], dom))
    # the override key column is the one whose value set contains the named value; ties: the column named in the
    # term's general definition
    hits = [n for n, dom in cands if vals & dom]
    if len(hits) == 1:
        return hits[0]
    gen = t.get("_B") or t.get("_C") or " ".join(t.get("_L") or [])
    for n, dom in cands:
        if gen and gen.startswith(n + " "):
            return n
    for n, dom in cands:
        if gen and (" " + n + " ") in (" " + gen + " "):
            return n
    if hits:
        return hits[0]
    fail("override key column")


def parse_t5(seg, cols, fm):
    out = {}
    for sent in re.split(r"(?<=\.) (?=[a-z])", seg.strip()):
        m = re.fullmatch(r"([a-z_.]+) is one of (.+)\.", sent)
        if m:
            vals = m.group(2).split(", ")
            if fm.legend and fm.legend["col"] == m.group(1):
                vals = [fm.legend["codes"][v] for v in vals]
            out[m.group(1)] = vals
            continue
        m = re.fullmatch(rf"([a-z_.]+) is a whole number of (\S+) from ({num_regex(fm.nf)}) to ({num_regex(fm.nf)})\.",
                         sent)
        if m:
            lo, hi = parse_num(m.group(3), fm.nf), parse_num(m.group(4), fm.nf)
            out[m.group(1)] = [Fraction(x) for x in range(int(lo), int(hi) + 1)]
            continue
        m = re.fullmatch(rf"([a-z_.]+) is from ({num_regex(fm.nf)}) to ({num_regex(fm.nf)}) (\S+) in steps of "
                         rf"({num_regex(fm.nf)})\.", sent)
        if m:
            lo, hi, st = (parse_num(m.group(i), fm.nf) for i in (2, 3, 5))
            n = int((hi - lo) / st)
            out[m.group(1)] = [lo + st * i for i in range(n + 1)]
            continue
        fail("T5 domain sentence")
    return out


# ------------------------------------------------------------------------------------------------ options
def _base(q):
    while q["op"] in ("thr", "not"):
        q = q["inner"]
    return q


def answer_kind(P):
    b = _base(P["q"])
    op = b["op"]
    if op in ("count", "cdist", "g_count", "count_lines", "col_count"):
        return "count"
    if op in ("first", "last"):
        return "dt"
    if op in ("argmax", "argmin", "g_argmax", "comp_argmax", "row_top", "cpick"):
        return "id"
    if op == "select":
        return "set"
    if op in ("sum", "mean", "ent_sum", "row_total"):
        return "num"
    if op in ("min", "max", "lookup", "ent_attr"):
        col = P["tables"] and _coltype(P, b["col"])
        return {"num": "num", "date": "date", "cat": "cat"}[col]
    return "yn"


def _coltype(P, col):
    for t in P["tables"]:
        for c in t["cols"]:
            if c["name"] == col:
                return c["type"]
    fail("column")


def parse_options(P, row):
    if row["qtype"] == "noul":
        return None
    fm = P["fm"]
    kind = answer_kind(P)
    c = P["card"]
    out = []
    for o in row["options"]:
        if o == CBD_TXT:
            out.append(CBD)
        elif o == NONE_OPT:
            out.append(NONE)
        elif re.fullmatch(r"no such [a-z ]+", o):
            if c.get("no_record") and o != c["no_record"] and kind != "set":
                fail("no-record wording differs from the card")
            out.append(frozenset() if kind == "set" else NO_RECORD)
        elif re.fullmatch(r"two or more [a-z ]+ tie", o):
            if P["mode"] == "full" and c.get("tie_opt") != o:
                fail("tie wording differs from the card")
            out.append(TIE)
        elif kind == "count":
            out.append(int(parse_num(o, fm.nf)))
        elif kind == "num":
            out.append(parse_num(o, fm.nf))
        elif kind == "date":
            out.append(parse_date(o, fm.df))
        elif kind == "dt":
            out.append(parse_dt(o, fm.zone, fm.df, fm.tf))
        elif kind == "cat":
            if fm.legend and fm.legend["col"] == _base(P["q"])["col"]:
                out.append(fm.legend["codes"].get(o) or fail("code"))
            else:
                out.append(o)
        elif kind == "id":
            if not re.fullmatch(r"[A-Z]{2,3}-\d{2,4}", o):
                fail("id option")
            out.append(o)
        elif kind == "set":
            m = re.fullmatch(r"((?:[A-Z]{2,3}-\d{4})(?: and [A-Z]{2,3}-\d{4})*) only", o)
            if not m:
                fail("set option")
            ids = m.group(1).split(" and ")
            if ids != sorted(ids, key=id_key):
                fail("set option order")
            out.append(frozenset(ids))
        else:
            fail("option kind")
    return out


def render_payload(P, q, a):
    """Display basis for comparisons (T22 rounding on averages; rendered strings otherwise)."""
    if isinstance(a, (bool, frozenset)) or a in SPECIALS:
        return repr(sorted(a)) if isinstance(a, frozenset) else repr(a)
    b = _base(q)
    if b["op"] == "mean" and isinstance(a, Fraction):
        return str(half_up(a, P["ctx"]["round_dp"]))
    return repr(a)


def display(P, q, a, alt=None):
    if isinstance(a, Fraction) and _base(q)["op"] == "mean":
        dp = P["ctx"]["round_dp"]
        return half_even(a, dp) if alt and alt[0] == "E23" else half_up(a, dp)
    return a


# ------------------------------------------------------------------------------------------------ checks
def check(row, side, card=None):
    try:
        return _check(row, side)
    except (ParseError, BReject, BUndefined, KeyError, ValueError, IndexError, TypeError, ZeroDivisionError) as e:
        return False, f"{type(e).__name__}: {str(e)[:80]}"
    except Exception as e:  # any other failure of the parse / solver B is a G3 failure, never a pass
        return False, f"{type(e).__name__}: {str(e)[:80]}"


def _compound_req_atom(q):
    """True when a request condition (req_any atom or a T41 lift) holds a line atom with a level and a component."""
    def bad(a):
        return isinstance(a, dict) and a.get("k") == "line" and "level" in a and "comp" in a

    def walk(x):
        if isinstance(x, dict):
            if x.get("op") == "req_any" and bad(x.get("a")):
                return True
            if x.get("k") == "lift" and bad(x.get("a")):
                return True
            return any(walk(v) for v in x.values())
        if isinstance(x, (list, tuple)):
            return any(walk(v) for v in x)
        return False
    return walk(q)


def _check(row, side):
    P = parse_row(row)
    from f9g3ex import check_examples
    check_examples(P, side.get("n_examples", 0))
    q = P["q"]
    if not q_equal(q, side["q"]):
        return False, "parsed Q differs"
    # S6 wording lint (1.2, F9-R2-03, F9-R3-01): every lifted atom of a request / session condition is one line
    # phrase of the closed list; a compound condition on one line ("an <ERROR> line from <C5>") is never asked
    if P["sampler"] == "S6" and _compound_req_atom(q):
        return False, "compound one-line request condition"
    shown = None
    if _base(q)["op"] == "cpick":
        shown = [x for x in P["options"] if isinstance(x, str) and x not in SPECIALS]
    tabs = hash_tables(P)
    sh = structure_hash(tabs, P["stated"], q, extra={"shown": sorted(shown or [], key=id_key)})
    if sh != row["meta"]["structure_hash"]:
        return False, "structure hash differs"
    B = SolverB(P)
    a = B.answer(q, shown=shown)
    if row["qtype"] == "noul":
        if not isinstance(a, bool) or int(a) != row["gold"]:
            return False, "solver B gold differs (yes/no)"
        return True, "ok"
    opts = P["options"]
    gi = row["options"].index(row["gold"])
    gp = opts[gi]
    da = display(P, q, a)
    if isinstance(a, frozenset) and not a:
        da = frozenset()
    correct = [i for i, o in enumerate(opts) if o == da]
    if gp == NONE and da not in SPECIALS:
        # T37b: built by deleting the gold option, so solver B checks that no remaining option is correct (repair
        # r1: record-set rows included, 1.3 / F9-R1-33; an empty answer set is correct for no shown set option)
        if correct:
            return False, "solver B: an option is correct on a 'none of these' row"
    elif correct != [gi]:
        return False, f"solver B single correct option fails ({len(correct)} correct)"
    # option tag reproduction
    for (text, tag), payload in zip(side["options"], opts):
        if not _tag_ok(P, B, q, tag, payload, a, shown, opts):
            return False, f"option tag {tag[0]} not reproduced"
    # S3: no key named in the question, an option or the gold is an orphan key (T29)
    if P["sampler"] == "S3":
        dim = {r[0] for r in P["tables"][0]["rows"]}
        fk = {r[0] for r in P["tables"][1]["rows"]}
        orphans = fk - dim
        named = set(re.findall(r"[A-Z]{2,3}-\d{4}", P["qtext"])) | {x for o in opts if isinstance(o, frozenset)
                                                                     for x in o} | {o for o in opts if isinstance(o, str)}
        if named & orphans:
            return False, "orphan key named"
    return True, "ok"


def _tag_ok(P, B, q, tag, payload, gold, shown, opts):
    t = tag[0]
    if t in ("gold", "gold_cbd_member"):
        return True
    if t == "EA":
        return payload in SPECIALS or payload == frozenset()
    b = _base(q)
    op = b["op"]
    if t == "E0":
        x = tag[1]
        if op in ("lookup", "ent_attr"):
            q2 = dict(q)
            q2["id" if op == "lookup" else "key"] = x
            try:
                v = B.answer(q2)
            except (BUndefined, BReject):
                return False
            return display(P, q, v) == payload
        ids = {r[0] for r in P["btables"][0]["rows"]} if P["sampler"] != "S6" else (
            {r[2] for r in P["btables"][0]["rows"]} | {r[3] for r in P["btables"][0]["rows"]})
        if op == "cpick":
            return x in ids and B.answer(q, shown=[x]) == NONE
        return x in ids and payload == x and payload != gold
    if t in ("ES", "ES2"):
        kind, x = tag[1], tag[2]
        bases = [o for o in opts if isinstance(o, frozenset)] if t == "ES2" else [gold]
        for bs in bases:
            if isinstance(bs, frozenset) and ((kind == "add" and bs | {x} == payload) or (
                    kind == "remove" and bs - {x} == payload)):
                return True
        return False
    alt = tuple(tag)
    q2 = rewrite(q, alt) if alt[0] in REWRITE else q
    m = alt if alt[0] not in REWRITE else None
    if op == "cpick":
        qs = {**q2, "op": "select"}
        try:
            sel = B.answer(qs, alt=m)
            sel0 = B.answer({**q, "op": "select"})
        except (BUndefined, BReject):
            return False
        return isinstance(sel, frozenset) and payload in sel and payload not in (sel0 if isinstance(sel0, frozenset)
                                                                               else set())
    try:
        v = B.answer(q2, alt=m, shown=shown)
    except (BUndefined, BReject):
        return False
    return display(P, q, v, alt) == payload


def hash_tables(P):
    if P["sampler"] == "S5":
        return [{"role": "pivot", "cols": [{"name": "entity", "type": "id"}, {"name": "period", "type": "cat"},
                                           {"name": "value", "type": "num", "dp": 0},
                                           {"name": "marked", "type": "bool"}],
                 "rows": [list(r) for r in P["btables"][0]["rows"]]}]
    out = []
    for t in P["tables"]:
        cols, rows = [], []
        for c in t["cols"]:
            if c["type"] == "list":
                cols.append({"name": c["name"], "type": "list"})
            else:
                cols.append({"name": c["name"], "type": c["type"], "dp": c.get("dp") if c["type"] == "num" else None,
                             "unit": (c.get("unit") or P["fm"].units.get(c["name"])) if c["type"] == "num" else None,
                             "group": c["name"].split(".", 1)[0] if "." in c["name"] else "top"})
        for r in t["rows"]:
            rr = []
            for c, v in zip(t["cols"], r):
                rr.append(v)  # datetimes stay epoch seconds (1.1 step 6), as the generator side hashes them
            rows.append(rr)
        out.append({"role": t["role"], "cols": cols, "rows": rows})
    return out
