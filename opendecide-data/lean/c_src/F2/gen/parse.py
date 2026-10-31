"""The F2 round-trip parser (G3; 3.3): rendered row text -> labeled problem LP -> canonical problem P.

It reads only the row (state, card, instructions, options, qtype, meta.format_style) and the lexicon; never the
generator's structure. Card text: the `card` field on yes/no rows; on choice rows the card block inside
`instructions` (CP1). The question is the last question-frame match in `instructions`. Document values come from
parse_doc (container-aware) and are looked up by the labels the card names (R2-12).
Rejections (a parse failure = G3 failure): SEM phrase in the document, null / "unknown" / banned markers, "not
recorded" on a closed-world card, a second governing rule for one exception, question-side violations (Q1, N1).
"""
from __future__ import annotations

import re
from decimal import Decimal

from . import lex
from .canon import canonize, structure_hash
from .parse_doc import parse_state, norm_key, ParseError

D = Decimal


class PErr(ValueError):
    pass


# ----------------------------------------------------------------------------------------------------------------- scanning

def _tpls_money():
    T = []
    T += [("W0", lex.W0), ("W1", lex.W1), ("W2", lex.W2), ("CATLIST", lex.CATLIST), ("R8", lex.R8), ("U5", lex.U5),
          ("R4", lex.R4), ("X4_ORDER", lex.X4_ORDER)]
    T += [(f"X5:{k}", v) for k, v in lex.X5.items()]
    T += [(f"X7:{k}", v) for k, v in lex.X7.items()]
    T += [("X1", lex.X1)]
    T += [(f"X3:{k}", v) for k, v in lex.X3.items()]
    T += [(f"R1:{k}", v) for k, v in lex.R1.items()]
    T += [(f"R2:{k}", v) for k, v in lex.R2.items()]
    T += [(f"R3:{k}", v) for k, v in lex.R3.items()]
    T += [(f"R5:{k}", v) for k, v in lex.R5.items()]
    T += [(f"U3:{k}", v) for k, v in lex.U3.items()]
    T += [("OP_MONEY", lex.OP_MONEY)]
    T += [(f"B1:{k}", v) for k, v in lex.B1_SENT.items()]
    T += [("X4_CAP", lex.X4_CAP), ("X4_MIN", lex.X4_MIN), ("X8", lex.X8)]
    T += [("G_UN1", lex.G_UN1), ("G_O1", lex.G_O1), ("G_O3", lex.G_O3), ("G_O2", lex.G_O2)]
    T += [("X2:rate:replace", lex.X2["rate"]["replace"]), ("X2:rate:add", lex.X2["rate"]["add"])]
    T += [("F_SUM", lex.F_SUM), ("F_DISC2", lex.F_DISC2), ("F_CAP", lex.F_CAP), ("F_MIN", lex.F_MIN),
          ("F_FEE_TOT", lex.F_FEE_TOT), ("F_PERK", lex.F_PERK), ("F_MUL", lex.F_MUL), ("F_DED", lex.F_DED),
          ("F_ADD", lex.F_ADD), ("F_DISC_X1", lex.F_DISC_X1), ("F_ADD_X1", lex.F_ADD_X1),
          ("F_RESULT_X1", lex.F_RESULT_X1), ("F_DISC", lex.F_DISC), ("F_PCT", lex.F_FEE), ("OUT_INTRO", lex.OUT_INTRO)]
    return T


def scan(text, tpls):
    """[(name, groupdict, line_no, start)] in text order; higher-priority templates mask their spans first."""
    out = []
    lines = text.split("\n")
    for li, ln in enumerate(lines):
        work = ln
        for name, tpl in tpls:
            rx = lex.compile_tpl(tpl)
            while True:
                m = rx.search(work)
                if not m:
                    break
                out.append((name, m.groupdict(), li, m.start()))
                work = work[:m.start()] + "\x00" * (m.end() - m.start()) + work[m.end():]
    out.sort(key=lambda x: (x[2], x[3]))
    return out


# ----------------------------------------------------------------------------------------------------------------- values

MONEY_RX = re.compile(r"^(\d+(?:\.\d+)?) ([A-Za-z]+)$")


def money_val(s, cur=None, seen=None):
    m = MONEY_RX.match(s.strip())
    if not m:
        raise PErr(f"not a money value: {s!r}")
    if cur and m.group(2) != cur:
        raise PErr("currency differs")
    if seen is not None:
        seen.append(m.group(1))
        seen.append("CUR:" + m.group(2))
    return D(m.group(1)), m.group(2)


def num_lead(s):
    m = re.match(r"^(\d+(?:\.\d+)?)(?:%| [A-Za-z][A-Za-z \-]*)?$", s.strip())
    if not m:
        raise PErr(f"not a number: {s!r}")
    return D(m.group(1))


def pct_val(s):
    m = re.match(r"^(\d+(?:\.\d+)?)%$", s.strip())
    if not m:
        raise PErr(f"not a percentage: {s!r}")
    return D(m.group(1))


def labels_list(s):
    """'the A, the B and the C' -> [A, B, C]."""
    s = s.strip()
    parts = re.split(r", the | and the ", s)
    if not parts[0].startswith("the "):
        raise PErr("label list")
    parts[0] = parts[0][4:]
    return [p.strip() for p in parts]


DOC_SEM_PHRASES = ["up to and including", "up to but not including", "only if", "unless", "either or both",
                   "but not both", "is capped at", "with a minimum of", "rounds up", "round only", "is per claim",
                   "cannot go below", "applies if", "is not counted", "business day is", "last allowed day is",
                   "calendar days after", "business days after", "counting the day"]
BANNED_MARKERS = re.compile(r"(?<![A-Za-z])(n/a|N/A|TBD|unknown|null)(?![A-Za-z])")


def doc_checks(doc, world):
    probs = []
    for k, v in doc.pairs:
        t = f"{k} {v}".lower()
        for ph in DOC_SEM_PHRASES:
            if ph in t:
                probs.append(f"SEM phrase in the document: {ph}")
        if BANNED_MARKERS.search(f" {v} "):
            probs.append("banned marker in the document")
        if v.strip() == "not recorded" and world == "closed":
            probs.append("'not recorded' on a closed-world card")
    for cols, rows, cap in doc.tables:
        for r in rows:
            for c in r:
                if BANNED_MARKERS.search(f" {c} "):
                    probs.append("banned marker in a table")
    return probs


# ----------------------------------------------------------------------------------------------------------------- question

def _q_rx():
    out = []
    cmp_alts = []
    for op, lst in lex.Q_CMP.items():
        for ph, pos, negcmp in lst:
            cmp_alts.append((op, ph, pos, negcmp, False))
    for op, lst in lex.Q_CMP_VERB.items():
        for ph, negcmp in lst:
            cmp_alts.append((op, ph, "pre", negcmp, True))
    return cmp_alts


CMP_ALTS = _q_rx()
TF_RX = [re.compile("^" + re.escape(f.split("{P}")[0]) + r"(?P<P>.+)" + re.escape(f.split("{P}")[1]) + "$")
         for f in lex.TF_FRAMES]


def parse_cmpT(s, cur):
    """'at least 450.00 USD' / '450.00 USD or more' / 'exceeds 450.00 USD' -> (op, T, negcmp, verb)."""
    s = s.strip()
    best = None
    for op, ph, pos, negcmp, verb in CMP_ALTS:
        if pos == "post":
            post = ph.replace("{T}", "").strip()
            m = re.match(r"^(\d+(?:\.\d+)? [A-Za-z]+) " + re.escape(post) + "$", s)
            if m:
                cand = (len(ph), op, m.group(1), negcmp, verb)
        else:
            m = re.match("^" + re.escape(ph) + r" (\d+(?:\.\d+)? [A-Za-z]+)$", s)
            cand = (len(ph), op, m.group(1), negcmp, verb) if m else None
        if m and (best is None or cand[0] > best[0]):
            best = cand
    if not best:
        raise PErr(f"no comparator in {s!r}")
    _, op, T, negcmp, verb = best
    return op, money_val(T, cur)[0], negcmp, verb


BANNED_Q = ["not more than", "not less than", "not before", "not after", "or not", "whether or not", "yes or no",
            "up to ", "a maximum of", "a minimum of", "between", "either", "(either or both)", "but not both",
            "hardly", "unless", "other than", "lack", "deny", "refuse", "rule out", "isn't", "doesn't", "wasn't",
            "didn't", "is it not true", "false", "untrue", "incorrect"]


def question_checks(q):
    probs = []
    ql = q.lower()
    for b in BANNED_Q:
        if b in ql:
            probs.append(f"banned in a question: {b}")
    return probs


def find_question(instr):
    """Question candidates in instructions, last first (the row's question is the last sentence that parses as an F2
    question frame; wordings and few-shot cases may hold other question marks)."""
    cands = []
    for li, ln in enumerate(instr.split("\n")):
        for m in re.finditer(r"(?:^|(?<=\s))[A-Z]", ln):
            j = ln.find("?", m.start())
            if j > 0:
                cands.append((li, m.start(), ln[m.start():j + 1]))
    if not cands:
        raise PErr("no question")
    return [c[2] for c in reversed(cands)]


def _cmpT_rx():
    alts = []
    for op, ph, pos, negcmp, verb in CMP_ALTS:
        if pos == "post":
            alts.append(r"\d+(?:\.\d+)? [A-Za-z]+ " + re.escape(ph.replace("{T}", "").strip()))
        else:
            alts.append(re.escape(ph) + r" \d+(?:\.\d+)? [A-Za-z]+")
    alts.sort(key=len, reverse=True)
    return "(?P<T>" + "|".join(alts) + ")"


CMPT = _cmpT_rx()


def _q_rx_of(tpl, slot):
    """Compile a question template whose comparator slot is matched by the comparator alternation."""
    a, b = tpl.split("{" + slot + "}")
    ra = lex.compile_tpl(a).pattern if a else ""
    rb = lex.compile_tpl(b).pattern if b else ""
    return re.compile("^" + ra + CMPT + rb + "$")


def parse_thr_question(q, cur):
    """-> dict(kind='thr', res, id, op, T, neg, tf, negcmp) or kind='op'."""
    info = {"tf": 0, "neg": 0}
    P = None
    for rx in TF_RX:
        m = rx.match(q)
        if m:
            P = m.group("P")
            info["tf"] = 1
            break
    if P is None:
        for tpl in lex.Q_DIRECT:
            rx = _q_rx_of(tpl, "cmpT")
            m = rx.match(q)
            if m:
                op, T, negcmp, verb = parse_cmpT(m.group("T"), cur)
                return {"kind": "thr", "res": m.group("res"), "id": m.group("id"), "op": op, "T": T, "neg": 0,
                        "tf": 0, "negcmp": negcmp}
        for tpl in lex.Q_OWED_DIRECT:
            m = lex.compile_tpl(tpl, anchored=True).match(q)
            if m:
                return {"kind": "op", "item": m.group("item"), "id": m.group("id"), "neg": 0, "tf": 0}
        raise PErr("question frame not recognised")
    neg = 0
    if P.startswith(lex.OPN):
        neg += 1
        P = P[len(lex.OPN):]
    m = _q_rx_of(lex.P_THR_NEG, "cmpT").match(P)
    if m:
        op, T, negcmp, verb = parse_cmpT(m.group("T"), cur)
        return {"kind": "thr", "res": m.group("res"), "id": m.group("id"), "op": op, "T": T, "neg": neg + 1, "tf": 1,
                "negcmp": negcmp}
    m = _q_rx_of(lex.P_THR, "cmpT").match(P)
    if m:
        op, T, negcmp, verb = parse_cmpT(m.group("T"), cur)
        if verb:
            raise PErr("verb comparator after 'is'")
        return {"kind": "thr", "res": m.group("res"), "id": m.group("id"), "op": op, "T": T, "neg": neg, "tf": 1,
                "negcmp": negcmp}
    m = _q_rx_of(lex.P_THR_VERB, "verbT").match(P)
    if m:
        op, T, negcmp, verb = parse_cmpT(m.group("T"), cur)
        if not verb:
            raise PErr("adjectival comparator without 'is'")
        return {"kind": "thr", "res": m.group("res"), "id": m.group("id"), "op": op, "T": T, "neg": neg, "tf": 1,
                "negcmp": negcmp}
    for i, tpl in enumerate([lex.P_OWED] + lex.P_OWED_NEG):
        m = lex.compile_tpl(tpl, anchored=True).match(P)
        if m:
            return {"kind": "op", "item": m.group("item"), "id": m.group("id"), "neg": neg + (1 if i else 0), "tf": 1}
    raise PErr("proposition not recognised")


def parse_choice_question(q):
    for tpl in lex.Q_VALUE:
        m = lex.compile_tpl(tpl, anchored=True).match(q)
        if m:
            return {"kind": "value", "res": m.group("res"), "id": m.group("id")}
    for tpl in lex.Q_OUTCOME:
        m = lex.compile_tpl(tpl, anchored=True).match(q)
        if m:
            return {"kind": "outcome", "okind": m.group("kind"), "id": m.group("id")}
    for tpl in lex.Q_CASES:
        m = _q_rx_of(tpl, "cmpT").match(q)
        if m:
            return {"kind": "cases", "res": m.group("res"), "T": m.group("T")}
    raise PErr("choice question not recognised")


# ----------------------------------------------------------------------------------------------------------------- money

def _cond_parse(s):
    """One condition: 'the F is at least 5' / 'the F is 5 or more' / 'the F is V'."""
    for ph_op in (("ge", lex.CMP_CARD["ge"]), ("gt", lex.CMP_CARD["gt"]), ("le", lex.CMP_CARD["le"]),
                  ("lt", lex.CMP_CARD["lt"])):
        op, phs = ph_op
        for ph in sorted(phs, key=len, reverse=True):
            m = re.match(r"^the (?P<f>.+?) is " + re.escape(ph) + r" (?P<x>\d+)$", s)
            if m:
                return {"f": m.group("f"), "op": op, "v": m.group("x")}
    for op, post in lex.CMP_CARD_POST.items():
        m = re.match(r"^the (?P<f>.+?) is (?P<x>\d+) " + re.escape(post) + "$", s)
        if m:
            return {"f": m.group("f"), "op": op, "v": m.group("x")}
    m = re.match(r"^the (?P<f>.+?) is (?P<v>.+)$", s)
    if m:
        return {"f": m.group("f"), "op": "is", "v": m.group("v")}
    raise PErr(f"condition not recognised: {s!r}")


def _gate_parse(name, g):
    if name == "G_O1":
        a, b = _split_and_or(g["c1"] + " and " + g["c2"], " and ")
        return "O1", "and", [_cond_parse(a), _cond_parse(b)]
    if name == "G_O3":
        a, b = _split_and_or(g["c1"] + " or " + g["c2"], " or ")
        return "O3", "or1", [_cond_parse(a), _cond_parse(b)]
    conn = "UN1" if name == "G_UN1" else "O2"
    c = g["c"]
    m = re.match(r"^either (?P<a>.+), but not both$", c)
    if m:
        a, b = _split_and_or(m.group("a"), " or ")
        return conn, "or2", [_cond_parse(a), _cond_parse(b)]
    m = re.match(r"^(?P<a>.+) \(either or both\)$", c)
    if m:
        a, b = _split_and_or(m.group("a"), " or ")
        return conn, "or1", [_cond_parse(a), _cond_parse(b)]
    if " and the " in c:
        a, b = _split_and_or(c, " and ")
        return conn, "and", [_cond_parse(a), _cond_parse(b)]
    return conn, "single", [_cond_parse(c)]


def _split_and_or(s, sep):
    parts = s.split(sep + "the ")
    if len(parts) != 2:
        raise PErr("two conditions expected")
    return parts[0], "the " + parts[1]


CASE = object()


def parse_money(row, doc, M, qinfo, card_text):
    names = [x[0] for x in M]
    g = {}
    for x in M:
        g.setdefault(x[0], []).append(x[1])
    world = "open" if "W2" in g else "closed"
    if "W0" not in g or (("W1" in g) == ("W2" in g)):
        raise PErr("world clauses")
    sem = {}
    LP = {"eng": "money", "world": world, "vals": {}, "facts": {}, "lines": [], "steps": [], "excs": []}
    vals, facts = {}, {}
    cur = None
    seen = []        # every money literal the rules read: currency and display grid come from these

    case_cols = set()
    if qinfo["kind"] == "cases":
        for cols, rows_, cap in doc.tables:
            if rows_ and any(r[0] in (row.get("options") or []) for r in rows_):
                case_cols = {norm_key(c) for c in cols[1:]}

    def dv(label, kind):
        if norm_key(label) in case_cols:
            return CASE
        v = doc.get(label)
        if v is None:
            raise PErr(f"document has no value for {label!r}")
        if v == "not recorded":
            return v
        if kind == "money":
            return money_val(v, None, seen)[0]
        if kind == "pct":
            return pct_val(v)
        return num_lead(v)

    lc_of = {}
    priced = []
    for x in M:
        if x[0] == "F_MUL":
            gg = x[1]
            vals[gg["q"]] = dv(gg["q"], "num")
            vals[gg["r"]] = dv(gg["r"], "money")
            LP["lines"].append({"p": "mul", "q": gg["q"], "r": gg["r"]})
            lc_of[gg["lc"]] = f"line{len(LP['lines']) - 1}"
        elif x[0] == "F_PERK":
            gg = x[1]
            vals[gg["q"]] = dv(gg["q"], "num")
            vals[gg["r"]] = dv(gg["r"], "money")
            LP["lines"].append({"p": "perk", "q": gg["q"], "r": gg["r"], "k": D(gg["k"])})
            lc_of[gg["lc"]] = f"line{len(LP['lines']) - 1}"
    sub = None
    if "F_SUM" in g:
        gg = g["F_SUM"][0]
        sub = gg["tot"]
        labs = labels_list(gg["lines"])
        if not LP["lines"]:
            for lb in labs:
                vals[lb] = dv(lb, "money")
                LP["lines"].append({"p": "stated", "a": lb})
        elif set(labs) != set(lc_of):
            raise PErr("sum names other lines")
        base = sub
    elif LP["lines"]:
        base = list(lc_of)[0]
    else:
        base = None
    if sub:
        lc_of[sub] = "sum"
    # steps
    steps = []
    order_mode = "X1" in g

    def stated_base(lbl):
        if not LP["lines"]:
            vals[lbl] = dv(lbl, "money")
            LP["lines"].append({"p": "stated", "a": lbl})

    fee_names = {}
    pct_sents = [x for x in M if x[0] == "F_PCT"]
    min_bases = {x[1]["base"] for x in M if x[0] == "F_MIN"}
    tot_fees = {x[1]["fee"]: x[1] for x in M if x[0] == "F_FEE_TOT"}
    for x in M:
        n, gg = x[0], x[1]
        if n == "F_DISC":
            stated_base(gg["base"])
            vals[gg["pct"]] = dv(gg["pct"], "pct")
            steps.append({"op": "disc", "id": "disc", "v": gg["pct"]})
        elif n == "F_DISC_X1":
            vals[gg["pct"]] = dv(gg["pct"], "pct")
            steps.append({"op": "disc", "id": "disc", "v": gg["pct"]})
        elif n == "F_ADD_X1":
            vals[gg["fixed"]] = dv(gg["fixed"], "money")
            steps.append({"op": "add", "id": "add", "v": gg["fixed"]})
        elif n == "F_RESULT_X1":
            stated_base(gg["base"])
        elif n == "F_DISC2":
            stated_base(gg["base"])
            vals[gg["pct1"]] = dv(gg["pct1"], "pct")
            vals[gg["pct2"]] = dv(gg["pct2"], "pct")
            steps.append({"op": "disc2", "id": "disc2", "v": [gg["pct1"], gg["pct2"]]})
        elif n == "F_PCT":
            stated_base(gg["base"])
            vals[gg["pct"]] = dv(gg["pct"], "pct")
            if gg["fee"] in min_bases:
                steps.append({"op": "pctof", "id": "pctof", "v": gg["pct"]})
            else:
                steps.append({"op": "fee", "id": "fee", "v": gg["pct"]})
                fee_names[gg["fee"]] = "fee"
        elif n == "F_CAP":
            vals[gg["cap"]] = dv(gg["cap"], "money")
            steps.append({"op": "cap", "id": "cap", "v": gg["cap"], "scope": None})
        elif n == "F_MIN":
            vals[gg["min"]] = dv(gg["min"], "money")
            steps.append({"op": "min", "id": "min", "v": gg["min"], "scope": None})
        elif n == "F_ADD":
            vals[gg["fixed"]] = dv(gg["fixed"], "money")
            steps.append({"op": "add", "id": "add", "v": gg["fixed"]})
        elif n == "F_DED":
            labs = labels_list(gg["lines"])
            stated_base(gg["gross"])
            for lb in labs:
                vals[lb] = dv(lb, "money")
            steps.append({"op": "ded", "id": "ded", "v": labs})
            if "X8" in g:
                steps.append({"op": "floor0", "id": "floor0"})
        elif n.startswith("X7:"):
            stated_base(gg["listed"])
            vals[gg["pct"]] = dv(gg["pct"], "pct")
            steps.append({"op": "incfee", "id": "incfee", "v": gg["pct"]})
            sem["X7"] = n.split(":")[1]
            fee_names[gg["fee"]] = "fee"
        elif n == "X4_CAP":
            for s in steps:
                if s["op"] == "cap" and s["v"] == gg["cap"]:
                    s["scope"] = "line" if gg["per"] == "line" else "total"
        elif n == "X4_MIN":
            for s in steps:
                if s["op"] == "min" and s["v"] == gg["min"]:
                    s["scope"] = "line" if gg["per"] == "line" else "total"
        elif n.startswith("X5:"):
            sem["X5"] = n.split(":")[1]
    for s in steps:
        if s.get("scope", "x") is None:
            raise PErr("cap or minimum without its scope sentence (X4)")
    if any(s["op"] in ("cap", "min") for s in steps):
        sem["X4"] = {s["id"]: s["scope"] for s in steps if s["op"] in ("cap", "min")}
    if "X8" in g:
        sem["X8"] = "floor"
    if order_mode:
        names_order = [p.strip() for p in g["X1"][0]["steps"].split(lex.X1_SEP)]
        idx = []
        for nm in names_order:
            if not nm.startswith("the "):
                raise PErr("X1 step name")
            lb = nm[4:]
            hit = [i for i, s in enumerate(steps) if s.get("v") == lb]
            if len(hit) != 1:
                raise PErr("X1 names an unknown step")
            idx.append(hit[0])
        if sorted(idx) != list(range(len(steps))):
            raise PErr("X1 must name every adjustment step")
        sem["X1"] = idx
    LP["steps"] = steps
    # exceptions: one governing rule per exception number (R1-04)
    gates = {}
    for x in M:
        if x[0] in ("G_UN1", "G_O1", "G_O3", "G_O2"):
            no = int(x[1]["n"])
            if no in gates:
                raise PErr("second governing rule for one exception (R1-04)")
            gates[no] = _gate_parse(x[0], x[1])
    effects = {}
    for x in M:
        if x[0].startswith("X2:"):
            no = int(x[1]["n"])
            form = x[0].split(":")[2]
            effects[no] = (form, x[1]["erate"], x[1]["grate"])
    if set(gates) != set(effects):
        raise PErr("exception without its effect sentence")
    rate_labels = {l.get("r") for l in LP["lines"]}
    pct_labels = {s["v"] for s in steps if s["op"] in ("fee", "pctof", "disc")}
    for no in sorted(gates):
        conn, join, conds = gates[no]
        form, v, on = effects[no]
        if on in rate_labels:
            kind = "rate"
            vals[v] = dv(v, "money")
        elif on in pct_labels:
            kind = "pct"
            vals[v] = dv(v, "pct")
        else:
            kind = "add"
            vals[v] = dv(v, "money")
            if on not in vals:
                vals[on] = dv(on, "money")
        for c in conds:
            if norm_key(c["f"]) in case_cols:
                continue
            raw = doc.get(c["f"])
            if raw is None:
                raise PErr(f"no document value for condition field {c['f']!r}")
            facts[c["f"]] = raw.strip()
        LP["excs"].append({"no": no, "conn": conn, "join": join, "kind": kind, "v": v, "on": on, "conds": conds})
        sem.setdefault("X2", {})[str(no)] = form
    for x in M:
        if x[0].startswith("X3:"):
            f = x[0].split(":")[1]
            sem["X3"] = "fold" if f.startswith("fold") else f
    for x in M:
        k = x[0]
        if k.startswith("R1:"):
            sem["R1"] = k.split(":")[1]
            sem["R1u"] = money_val(x[1]["u"], cur)[0]
        elif k.startswith("R2:"):
            sem["R2"] = k.split(":")[1]
        elif k.startswith("R3:"):
            sem["R3"] = k.split(":")[1]
        elif k.startswith("R5:"):
            sem["R5"] = k.split(":")[1]
        elif k.startswith("U3:"):
            sem["U3"] = k.split(":")[1]
    if any(k.startswith(("R2:", "R3:")) for k in names) and "R1" not in sem:
        raise PErr("R2 / R3 without R1")
    # open world: categories
    cats = {}
    for x in M:
        if x[0] == "CATLIST":
            cats[x[1]["f"]] = [v.strip() for v in x[1]["list"].split(", ")]
    LP["vals"] = {k: v for k, v in vals.items() if v is not CASE}
    LP["facts"] = facts
    LP["sem"] = sem
    if qinfo["kind"] == "cases":
        money_cols = {norm_key(l["a"]) for l in LP["lines"] if l.get("a")}
        for cols_, rows_, cap_ in doc.tables:
            if rows_ and any(r[0] in (row.get("options") or []) for r in rows_):
                for r in rows_:
                    for c, x in zip(cols_[1:], r[1:]):
                        if norm_key(c) in money_cols and MONEY_RX.match(x.strip()):
                            money_val(x, None, seen)
    curs = {s[4:] for s in seen if s.startswith("CUR:")}
    if len(curs) > 1:
        raise PErr("currency differs")
    cur = curs.pop() if curs else None
    nums = [s for s in seen if not s.startswith("CUR:")]
    LP["unit"] = D("0.01") if any("." in s for s in nums) else D(1)
    if "R1u" in sem:
        pass
    if world == "open":
        LP["cats"] = {k: v for k, v in cats.items() if k in facts}
    # target and question
    LP["target"] = "final"
    q = qinfo
    if fee_names and not any(x[0] == "F_FEE_TOT" for x in M):
        LP["target"] = "fee"
    if q["kind"] == "thr":
        LP["q"] = {"kind": "thr", "cmp": q["op"], "T": q["T"], "neg": q["neg"]}
    elif q["kind"] == "op":
        LP["q"] = {"kind": "op", "neg": q["neg"]}
    elif q["kind"] == "value":
        LP["q"] = {"kind": "value"}
    elif q["kind"] == "outcome":
        LP["q"] = parse_outcomes(M, card_text, cur, row)
    elif q["kind"] == "cases":
        LP["q"] = parse_cases(row, doc, q, cur, vals, facts, LP)
    # printed intermediates: document values named by the card's line, subtotal or fee names
    printed, pn = {}, {}
    for nm, node in list(lc_of.items()) + [(f, "fee") for f in fee_names if any(x[0] == "F_FEE_TOT" for x in M)]:
        v = doc.get(nm)
        if v is not None:
            printed[nm] = money_val(v, cur)[0]
            pn[nm] = node
    if printed:
        LP["printed"] = printed
        LP["printed_nodes"] = pn
    LP["_cur"] = cur
    return LP


def parse_outcomes(M, card_text, cur, row):
    b1 = None
    for x in M:
        if x[0].startswith("B1:"):
            b1 = x[0].split(":")[1]
    if b1 is None:
        raise PErr("outcome table without its B1 sentence")
    items = []
    for ln in card_text.split("\n"):
        s = re.sub(r"^\s*(?:(?:[-*+•·>]|\d+[.)])\s*)+", "", ln).strip()
        m = re.match(r"^(?P<name>[^:]+): (?P<range>.+)$", s)
        if not m:
            continue
        rng = m.group("range").strip()
        lo = hi = None
        pos = None
        for p_, tpl in lex.OUT_RANGE[b1].items():
            rx = lex.compile_tpl(tpl.replace("{lo}", "{x1}").replace("{hi}", "{x2}"), anchored=True)
            mm = re.match("^" + tpl.replace("{lo}", r"(?P<lo>\d+(?:\.\d+)? [A-Za-z]+)")
                          .replace("{hi}", r"(?P<hi>\d+(?:\.\d+)? [A-Za-z]+)") + "$", rng)
            if mm:
                pos = p_
                lo = money_val(mm.group("lo"), cur)[0] if "lo" in mm.groupdict() and mm.group("lo") else None
                hi = money_val(mm.group("hi"), cur)[0] if "hi" in mm.groupdict() and mm.group("hi") else None
                break
        if pos is None:
            continue
        items.append({"name": m.group("name").strip(), "lo": lo, "hi": hi, "pos": pos})
    if len(items) < 2 or items[0]["pos"] != "low" or items[-1]["pos"] != "high":
        raise PErr("outcome table")
    for a, b in zip(items, items[1:]):
        if a["hi"] != b["lo"]:
            raise PErr("adjacent outcomes do not share an edge (R3-06)")
    return {"kind": "outcome", "outs": [{"name": i["name"], "lo": i["lo"], "hi": i["hi"]} for i in items], "b1": b1}


def parse_cases(row, doc, q, cur, vals, facts, LP):
    op, T, negcmp, verb = parse_cmpT(q["T"], cur)
    refs = list(row["options"])
    tabs = [t for t in doc.tables if t[1] and any(r[0] in refs for r in t[1])]
    if len(tabs) != 1:
        raise PErr("case table")
    cols, rows, cap = tabs[0]
    cases = []
    by_ref = {}
    for r in rows:
        by_ref[r[0]] = r
    shown_refs = [x for x in refs if x in by_ref]
    if set(by_ref) != set(shown_refs):
        raise PErr("state lists a case that is not an option")
    for ref in shown_refs:
        r = by_ref[ref]
        cv, cf = {}, {}
        cand_labels = list(vals) + list(facts) + [ln.get("q") for ln in LP["lines"]] + \
            [ln.get("a") for ln in LP["lines"]] + [cc["f"] for e in LP["excs"] for cc in e["conds"]]
        for c, x in zip(cols[1:], r[1:]):
            lab = None
            for l in cand_labels:
                if l and norm_key(l) == norm_key(c):
                    lab = l
            if lab is None:
                raise PErr(f"case column {c!r} is read by no rule")
            if lab in facts or any(lab == cc["f"] for e in LP["excs"] for cc in e["conds"]):
                cf[lab] = x.strip()
            elif any(lab == ln.get("a") for ln in LP["lines"]):
                cv[lab] = money_val(x, cur)[0]
            else:
                cv[lab] = num_lead(x)
        cases.append({"vals": cv, "facts": cf, "ref": ref})
    return {"kind": "cases", "cmp": op, "T": T, "cases": [{"vals": c["vals"], "facts": c["facts"]} for c in cases],
            "_refs": [c["ref"] for c in cases]}


# ----------------------------------------------------------------------------------------------------------------- entry

def card_text_of(row):
    return row["card"] if row["qtype"] == "noul" else row["instructions"]


def doc_currency(doc):
    for k, v in doc.pairs:
        m = MONEY_RX.match(v.strip())
        if m:
            return m.group(2)
    for cols, rows, cap in doc.tables:
        for r in rows:
            for c in r:
                m = MONEY_RX.match(c.strip())
                if m:
                    return m.group(2)
    return None


def engine_of(M):
    names = {x[0].split(":")[0] for x in M}
    if "STMT" in names:
        return "stmt"
    if names & {"BT_INTRO", "B2", "BAND_LOOKUP"}:
        return "band"
    if names & {"D4A", "D4B", "D6A", "D6B", "D8", "D17", "D5", "D14", "D15"}:
        return "date"
    return "money"


def parse_row(row):
    sid = row["meta"]["format_style"]
    doc = parse_state(row["state"], sid)
    ctext = card_text_of(row)
    from . import parse_more
    eng, tpls = parse_more.engine_and_tpls(ctext)
    M = scan(ctext, tpls)
    last = None
    for q in find_question(row["instructions"]):
        try:
            if eng != "money":
                qinfo = parse_more.parse_question(eng, row, q)
            else:
                qinfo = parse_thr_question(q, None) if row["qtype"] == "noul" else parse_choice_question(q)
            break
        except PErr as e:
            last = e
            continue
    else:
        raise last or PErr("no question")
    probs = question_checks(q)
    if probs:
        raise PErr("; ".join(probs))
    if eng != "money":
        LP = parse_more.parse(eng, row, doc, M, qinfo, ctext)
    else:
        LP = parse_money(row, doc, M, qinfo, ctext)
        if qinfo["kind"] == "thr" and qinfo.get("Tcur") and qinfo["Tcur"] != LP["_cur"]:
            raise PErr("question currency differs")
    dp = doc_checks(doc, LP["world"])
    if dp:
        raise PErr("; ".join(dp))
    return LP
