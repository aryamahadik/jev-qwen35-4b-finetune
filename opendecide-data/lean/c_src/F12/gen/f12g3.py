"""G2 + G3 on one emitted row: parse the rendered text back (f12parse), re-solve with solver B (f12solve_b) and map
the displayed options to canonical options; the row passes only if (a) the parsed structure equals the sampled one on
every decisive field, (b) solver B's gold equals the row's gold, and (c) the option -> canonical map is exact."""
from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal

import f12audit_b as AB
import f12lex as L
import f12parse as PZ
import f12render as RD
import f12solve_b as B
from fmt1 import pool as fpool

ALL_OUT = {}
for i, s in enumerate(RD.OUT_NAME_SETS):
    for k, v in s.items():
        ALL_OUT[v] = k


def lex_b(pk):
    lx = PZ.lexicon(pk)
    lx["idkeys"] = [e["idkey"] for e in pk["etypes"]]
    lx["namekeys"] = [e["namekey"] for e in pk["etypes"]]
    lx["dimkey"] = pk["dim"]["key"]
    return lx


def question_of(row):
    txt = row["instructions"]
    for form, q in RD.QUESTIONS.items():
        rx = re.escape(q).replace(r"\{p\}", r"(?P<p>\w+)").replace(r"\{T\}", r"(?P<T>\w+)")
        m = re.search(rx, txt)
        if m and row["qtype"] == "choice":
            return form, None, 0, m.groupdict()
    for (form, fr), qs in RD.YN.items():
        for neg in (2, 1, 0):
            rx = re.escape(qs[neg]).replace(r"\{T\}", r"(?P<T>\w+)")
            m = re.search(rx, txt)
            if m and row["qtype"] == "noul":
                return form, fr, neg, m.groupdict()
    raise PZ.ParseError("question")


def canon_options(row, defs, form=None):
    out = []
    for o in row["options"]:
        if o in ALL_OUT and form in (None, "C-OUT"):
            out.append(("out", ALL_OUT[o]))
            continue
        d = defs.get(o)
        if d is not None:
            k = next((k for k, v in RD.OUT_DEFS.items() if v == d), None) if form in (None, "C-OUT") else None
            if k:
                out.append(("out", k))
                continue
            for kk in ("unable", "answer"):
                if d == RD.ACT_DEFS[kk]:
                    out.append((kk,))
                    break
            else:
                m = re.fullmatch(r"call the tool (\w+) next", d)
                if m:
                    out.append(("call", m.group(1)))
                    continue
                m = re.fullmatch(r"ask the user for (\w+)", d)
                if m:
                    out.append(("ask", m.group(1)))
                    continue
                raise PZ.ParseError("definition line")
            continue
        fixed = {v: k for k, v in RD.TXT.items()}
        if o in fixed:
            out.append((fixed[o],))
            continue
        m = re.fullmatch(r"Call (\w+)", o)
        if m:
            out.append(("call", m.group(1)))
            continue
        m = re.fullmatch(r"Ask for (\w+)", o)
        if m:
            out.append(("ask", m.group(1)))
            continue
        out.append(("text", o))
    return out


def card_defs(row):
    d = {}
    for ln in (row.get("card") or "").split("\n") if row["qtype"] == "choice" else []:
        m = re.match(r"^- (.+?): (.+)$", ln)
        if m:
            d[m.group(1)] = m.group(2)
    return d


def problem_param(tool, vals, unclear, now):
    pm = {p["name"]: p for p in tool["params"]}
    out = []
    for p in tool["params"]:
        n = p["name"]
        if n in vals:
            ok, _ = B.check({"params": [dict(p, required=False)]}, {n: vals[n]}, [], now)
            if not ok:
                out.append(n)
        elif n in unclear and p["required"]:
            out.append(n)
        elif p["required"]:
            out.append(n)
    return out


def value_canon(p, text, now):
    t = p["type"]
    if t == "date":
        return dt.date.fromordinal(B.day_ord(text, now)).isoformat()
    if t in ("integer", "decimal"):
        num = text.split(" ")[0]
        return L.fmt_dec(Decimal(num)) + ((" " + p["unit"]) if p.get("unit") else "")
    if t == "enum":
        return next(x for x in p["members"] if x.casefold() == text.casefold())
    return text


def check_row(row, side, pk):
    """Returns (ok, why)."""
    st = fpool.style(row["meta"]["format_style"])
    extra_dims = sorted({t.get("dimw") for t in side["S"]["tools"] if t.get("dimw")})
    P = PZ.parse_state(row["state"], st["container"], pk, extra_dims=extra_dims)
    cardtxt = row["instructions"] + "\n" + (row.get("card") or "")
    pol = PZ.parse_policies(cardtxt)
    if side["card_mode"] != "full":
        # a short or no card shows no policy line: take the sampled settings (nothing to parse) and check below that
        # the label holds under every POL-INVALID setting (card_free_ok: no card policy is decisive)
        if not side["card_free_ok"]:
            return False, "short or no card on a row that is not card_free_ok"
        pol = dict(side["S"]["pol"])
    # (a) structure: decisive fields equal the sampled structure
    S = side["S"]
    why = compare(P, S, pol)
    if why:
        return False, "parse: " + why
    form, framing, neg, qa = question_of(row)
    if form != side["form"]:
        return False, "form"
    lx = lex_b(pk)
    if form == "C-INV":
        if [c for c in (P.get("cases") or {}).values()] != [[{k: v for k, v in x.items() if not k.startswith("_")}
                                                             for x in c] for c in side["cases"]]:
            return False, "parse: cases"
        golds = []
        for ref, st in P["cases"].items():
            r1 = B.solve(dict(P, conv=[{"who": "user", "ts": P["now"][11:], "st": st}]), pol, lx)
            if r1["outcome"] == "CALL" and r1["tool"] == qa["T"] and not r1.get("tie") and not r1.get("chain"):
                golds.append(ref)
        if len(golds) != 1:
            return False, f"C-INV: {len(golds)} cases meet T (B)"
        opts = canon_options(row, {}, form)
        g = ("text", golds[0])
        shown = opts[row["options"].index(row["gold"])]
        return (shown == g), f"C-INV solver B gold {g} vs row {shown}"
    res = B.solve(P, pol, lx)
    o = res["outcome"]
    if side["outcome"] is not None and o != side["outcome"]:
        return False, f"solver B outcome {o} vs A {side['outcome']}"
    if side["card_mode"] != "full":
        for inv in ("A", "B"):
            r_alt = B.solve(P, dict(pol, invalid=inv, role=False, tie=False), lx)
            if (r_alt["outcome"], r_alt.get("tool")) != (o, res.get("tool")):
                return False, f"card-free row depends on a card policy (invalid {inv})"
    if row["qtype"] == "noul":
        T = qa.get("T")
        if form == "Y-CALLX":
            base = o == "CALL" and res["tool"] == T
        elif form == "Y-ASK":
            base = o == "CALL"
        elif form == "Y-FIT":
            base = o in ("CALL", "ASK")
        elif form == "Y-DIRECT":
            base = o == "ANSWER"
        elif form == "Y-VALID":
            base = not AB.validate(P["tools"], P["call"])
        elif form == "Y-CORRECT":
            base = AB.correct(P, res, P["call"])
        else:
            return False, "unknown yes/no form"
        if framing == "N" and form in ("Y-VALID", "Y-CORRECT"):
            base = not base
        elif framing == "N":
            base = {"Y-CALLX": not base, "Y-DIRECT": not base, "Y-ASK": o == "ASK", "Y-FIT": o == "UNABLE"}[form]
        lab = base if neg != 1 else not base
        return (int(lab) == row["gold"]), f"solver B yes/no {int(lab)} vs {row['gold']}"
    defs = card_defs(row)
    opts = canon_options(row, defs, form)
    by = {t["name"]: t for t in P["tools"]}
    if form == "C-OUT":
        g = ("out", o)
    elif form in ("C-ACT", "C-TOOL", "C-PARAM"):
        if o == "CALL":
            g = {"C-ACT": ("call", res["tool"]), "C-TOOL": ("text", res["tool"]), "C-PARAM": ("nothing",)}[form]
        elif o == "ASK":
            T = by[res["fits"][0]]
            pp = problem_param(T, res["vals"], res["unclear"], P["now"])
            if len(pp) != 1:
                return False, "ask target not unique (B)"
            g = ("ask", pp[0]) if form == "C-ACT" else ("text", pp[0])
        elif o == "UNABLE":
            g = ("unable",) if form == "C-ACT" else ("none",)
        else:
            g = ("answer",)
    elif form == "C-VALUE":
        T = by[qa["T"]]
        p = next(x for x in T["params"] if x["name"] == qa["p"])
        if p["name"] in res["vals"]:
            g = ("text", value_canon(p, res["vals"][p["name"]], P["now"]))
        elif p["name"] in res["unclear"] or p["default"] is None:
            g = ("novalue",)
        else:
            g = ("text", p["default"])
    elif form == "C-DEFECT":
        errs = AB.validate(P["tools"], P["call"])
        if len(errs) > 1:
            return False, "C-DEFECT call has more than one defect (B)"
        g = ("valid",) if not errs else ("text", defect_text_b(errs[0]))
    else:
        return False, "form not handled by G3"
    if g not in opts:
        return False, f"solver B gold {g} not among options"
    shown = opts[row["options"].index(row["gold"])]
    return (shown == g), f"solver B gold {g} vs row {shown}"


PHRASE_B = {1: "Tool name not listed", 2: "Unknown parameter", 3: "Missing needed value", 4: "Wrong type",
            5: "Not a listed choice", 6: "Outside the limits", 7: "Wrong ID format", 8: "Only-if rule broken",
            9: "Unless rule broken", 10: "Exactly-one rule broken", 11: "At-least-one rule broken",
            12: "At-most-one rule broken"}
def defect_text_b(e):
    return PHRASE_B[e[0]] if e[0] == 1 else PHRASE_B[e[0]] + " on " + " and ".join(e[1])


def _cv(v):
    if isinstance(v, dict) and "num" in v:
        return ("n", str(Decimal(v["num"])))
    if isinstance(v, bool):
        return ("b", v)
    if isinstance(v, (int, Decimal)):
        return ("n", str(Decimal(v)))
    return ("s", v)


def compare(P, S, pol):
    if P["now"] != S["now"]:
        return "now"
    if (P["role"] or None) != (S["role"] if S["pol"]["role"] else None):
        return "role"
    for k in ("invalid", "tie", "role", "chain", "fresh"):
        if pol[k] != S["pol"][k]:
            return f"policy {k}"
    if [t["name"] for t in P["tools"]] != [t["name"] for t in S["tools"]]:
        return "tool list"
    for pt, st in zip(P["tools"], S["tools"]):
        if pt["a"] != st["a"] or (pt["scope"] or None) != (st["scope"] or None) or pt["pre"] != st["pre"]:
            return f"tool {st['name']} head"
        if pol["role"] and pt["roles"] != st["roles"]:
            return f"tool {st['name']} roles"
        if pol["tie"] and (pt["cost"], pt["pref"]) != (st["cost"], st["pref"]):
            return f"tool {st['name']} tie"
        if len(pt["params"]) != len(st["params"]):
            return f"tool {st['name']} params"
        for a, b in zip(pt["params"], st["params"]):
            for k in ("name", "type", "required", "default", "unit", "places", "members", "prefix", "n", "minlen",
                      "maxlen"):
                va, vb = a.get(k), b.get(k)
                if va != vb and not (va is None and vb is None):
                    return f"param {st['name']}.{b['name']}.{k}"
            for k in ("min", "max"):
                va, vb = a.get(k), b.get(k)
                if (va is None) != (vb is None) or (va and (str(va[0]) != str(vb[0]) and Decimal(str(va[0])) !=
                                                            Decimal(str(vb[0])) or va[1] != vb[1])):
                    return f"param {st['name']}.{b['name']}.{k}"
    for pt, st in zip(P["tools"], S["tools"]):
        if (pt.get("cons") or []) != (st.get("cons") or []):
            return f"tool {st['name']} rules"
    if (P.get("call") is None) != (S.get("call") is None):
        return "call presence"
    if S.get("call"):
        pc, sc = P["call"], S["call"]
        if pc["tool"] != sc["tool"] or [(k, _cv(v)) for k, v in pc["args"]] != [(k, _cv(v)) for k, v in sc["args"]]:
            return "call"
    if [r["fields"] for r in P["records"]] != [r["fields"] for r in S["records"]]:
        return "records"
    if [(s["tool"], s["ts"], s["fields"]) for s in P["stored"]] != [(s["tool"], s["ts"], s["fields"])
                                                                     for s in S["stored"]]:
        return "stored"
    pc = [_conv_key(c) for c in P["conv"]]
    sc = [_conv_key(c) for c in S["conv"]]
    if pc != sc:
        return "conversation"
    return None


def _conv_key(c):
    if c["who"] == "user":
        return ("user", c["ts"], [{k: v for k, v in s.items() if not k.startswith("_")} for s in c["st"]])
    if c["who"] == "assistant":
        return ("assistant", c["ts"], c.get("ask"))
    return ("tool", c["ts"], c["tool"], c["fields"])
