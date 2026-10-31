"""G2 / G3 per-row checks for program rows (G0 section 7 'Checks, on every row'): parse the rendered row back with the
independent parsers, re-solve with solvers B and C, and compare with solver A, the generator's structures and the
row's gold. The comparator may see both sides; the parsers and solvers B / C never see the generator."""
from __future__ import annotations

import common  # noqa: F401 (sys.path)

import re

import lex
import negcount
import parse as PZ
import solverb as SB
from common import toks, cstr
from tax import PRES

Q_PREFIXES = ("The question to answer:", "Question:", "Q:")


class CheckFail(ValueError):
    pass


def _wordings():
    from rows import f11_wordings
    return [w["text"] for w in f11_wordings()]


_WT = None


def strip_question_block(instr: str) -> tuple[str, str]:
    """Remove the wording, the question (with its register prefix) and the row-level statements; return (card text,
    question sentence)."""
    global _WT
    if _WT is None:
        _WT = sorted(_wordings(), key=len, reverse=True)
    s = instr
    for w in _WT:
        s = s.replace(w, "\n")
    qre = []
    for k, q in lex.Q.items():
        pat = re.escape(q)
        for ph in ("report", "reports", "K", "G", "target", "T"):
            pat = pat.replace(re.escape("{" + ph + "}"), r"(.+?)")
        qre.append(pat)
    question = None
    for pat in qre:
        m = re.search(pat, s)
        if m:
            question = m.group(0)
            a, b = m.start(), m.end()
            pre = s[:a].rstrip()
            for p in Q_PREFIXES:
                if pre.endswith(p):
                    a = len(pre) - len(p)
                    break
            s = s[:a] + "\n" + s[b:]
            break
    rs = []
    for k, t in lex.ROW_SEM.items():
        pat = re.escape(t)
        for ph in ("report", "reports", "K", "G", "none", "heading", "entity"):
            pat = pat.replace(re.escape("{" + ph + "}"), r"(.+?)")
        rs.append(pat)
    for pat in sorted(rs, key=len, reverse=True):
        s = re.sub(pat, "\n", s)
    return s, question


def gen_conds(card, aid, allowed):
    a = card.attrs[card.ai[aid]]
    s = sorted(allowed)
    if a.kind == "nom":
        return [(a.name, "in", frozenset(a.values[i] for i in s))]
    if a.kind == "pres":
        return [(a.name, "pres" if s == [PRES] else "abs", None)]
    out = []
    if s[0] > 0:
        out.append((a.name, "ge", a.cuts[s[0] - 1]))
    if s[-1] < a.n - 1:
        out.append((a.name, "lt", a.cuts[s[-1]]))
    return out


def compare_card(card, pc, *, render):
    """Check 1: parsed taxonomy equals the generator's up to a name bijection (IDs are the bijection here)."""
    if card.form != "short":
        if [a["name"] for a in pc.attrs] != [a.name for a in card.attrs]:
            raise CheckFail("attribute list differs")
        for a, p in zip(card.attrs, pc.attrs):
            if a.kind != p["kind"]:
                raise CheckFail("attribute kind")
            if a.kind == "nom":
                if p["values"] != a.values or any(p["terms"][v] != a.terms.get(i, []) for i, v in enumerate(a.values)):
                    raise CheckFail("glossary values / terms")
            elif p.get("aterms") != a.terms["attr"]:
                raise CheckFail("attribute terms")
            if a.kind == "num" and tuple(p["unit"]) != tuple(a.unit):
                raise CheckFail("unit")
    t = card.tax
    want_fields = {a.name: card.fields[i] for i, a in enumerate(card.attrs)} if getattr(card, "records", False) else {}
    if pc.fields != want_fields:
        raise CheckFail("record field designations differ")
    if card.form == "short":
        if pc.short_attrs != [a.name for a in card.attrs]:
            raise CheckFail("short attrs")
        names = [nm for nm, _ in pc.short_names]
        if sorted(names) != sorted(card.names):
            raise CheckFail("short names")
        return
    if card.shape == "box":
        if set(pc.codes) != set(card.ids):
            raise CheckFail("code set differs")
        for k, cd in enumerate(t.codes):
            p = pc.codes[card.ids[k]]
            want = []
            for aid, s in cd.parts(card.attrs):
                want += gen_conds(card, aid, s)
            if sorted(map(cstr, want)) != sorted(map(cstr, p["parts"])):
                raise CheckFail(f"definition of {card.ids[k]} differs")
            if cd.rule:
                gc = gen_conds(card, *cd.rule["cond"])
                if p["rule"] is None or p["rule"][0] != cd.rule["kind"] or [p["rule"][1]] != gc or \
                        p["rule"][2] != card.ids[cd.rule["target"]]:
                    raise CheckFail("redirect rule differs")
            elif p["rule"] is not None:
                raise CheckFail("extra rule")
            if bool(p.get("mark")) != bool(cd.mark):
                raise CheckFail("mark differs")
            if render == "base" and card.form == "oneline" and p.get("name") not in (None, card.names[k]):
                raise CheckFail("name differs")
        want_notes = sorted((card.ids[w], card.ids[l]) for w, l in t.notes)
        got_notes = sorted((w, ({a, b} - {w}).pop()) for a, b, w in pc.notes)
        if want_notes != got_notes:
            raise CheckFail("notes differ")
    elif card.shape == "group":
        g_attr = t.attrs[t.ai[t.gattr]]
        if len(pc.groups) != len(t.groups):
            raise CheckFail("group count")
        byname = {g["name"]: g for g in pc.groups}
        for gi, g in enumerate(t.groups):
            p = byname.get(card.gnames[gi])
            if p is None or sorted(p["vals"]) != sorted(g_attr.values[i] for i in g["vals"]):
                raise CheckFail("group heading")
            if sorted(p["leaves"]) != sorted(card.ids[k] for k in g["leaves"]):
                raise CheckFail("group leaves")
            if (p["residual"] is None) != (g["residual"] is None) or \
                    (g["residual"] is not None and p["residual"] != card.ids[g["residual"]]):
                raise CheckFail("residual")
            for k in g["leaves"]:
                want = []
                for aid, s in t.codes[k].box.items():
                    want += gen_conds(card, aid, s)
                if sorted(map(cstr, want)) != sorted(map(cstr, pc.codes[card.ids[k]]["parts"])):
                    raise CheckFail("leaf definition")
        want_sc = sorted((card.gnames[s["src"]], card.gnames[s["dst"]], str(gen_conds(card, *s["cond"])))
                         for s in t.scope_notes)
        got_sc = sorted((a, b, str([c])) for a, b, c in pc.scope)
        if want_sc != got_sc:
            raise CheckFail("scope notes")
    elif card.shape == "list":
        if len(pc.entries) != len(t.entries) or pc.catch != card.ids[t.catch]:
            raise CheckFail("entry list")
        for (conds, k), (pconds, pid) in zip(t.entries, pc.entries):
            want = []
            for aid, s in conds:
                want += gen_conds(card, aid, s)
            if pid != card.ids[k] or sorted(map(cstr, want)) != sorted(map(cstr, pconds)):
                raise CheckFail("entry differs")
    elif card.shape == "key":
        for n, cp in t.couplets.items():
            p = pc.couplets.get(n)
            ref = lambda x: str(x[1]) if x[0] == "n" else card.ids[x[1]]  # noqa: E731
            if p is None or p["b"] != ref(cp["b"]) or p["a"][1] != ref(cp["a"]):
                raise CheckFail("couplet")
            if [p["a"][0]] != gen_conds(card, *cp["cond"]):
                raise CheckFail("couplet condition")
            if pc.gnames.get(n) != (card.gnames[cp["group"]] if cp.get("group") is not None else None):
                raise CheckFail("couplet group name")


def gen_vec(card, it):
    out = {}
    for i, a in enumerate(card.attrs):
        if not it.stated(i):
            continue
        v = it.cell[i]
        if a.kind == "nom":
            out[a.name] = a.values[v]
        elif a.kind == "pres":
            out[a.name] = "present" if v == PRES else "absent"
        else:
            out[a.name] = it.exact[i]
    return out


def gen_frames(card, it):
    out = []
    for fr in it.frames:
        a = card.attrs[fr["attr"]]
        if a.kind == "nom":
            v = a.values[fr["value"]]
        elif a.kind == "pres":
            v = "present"
        else:
            v = fr["exact"]
        out.append((fr["kind"], a.name, v))
    if it.cue:
        out.append(("CUE", None, None))
    return sorted(map(cstr, out))


def code_of(card, k):
    return card.names[k] if card.form == "short" else card.ids[k]


def solve_both(pc, tree, vec):
    b = tree.solve(vec)
    c = SB.solver_c(pc, vec)
    if b != c:
        raise CheckFail(f"solver B {b} != solver C {c}")
    return b


def check_row(card, row, tree_cache):
    spec = row["_spec"]
    f = spec["form"]
    qtype = row["qtype"]
    if qtype == "noul":
        card_text, instr_rest = row["card"], None
        _, question = strip_question_block(row["instructions"])
    else:
        instr_rest, question = strip_question_block(row["instructions"])
        card_text = row["card"]
    if question is None:
        raise CheckFail("question not found")
    try:
        pc = PZ.parse_card(card_text, instr_rest, row.get("options"), qtype=qtype)
    except PZ.ParseError as e:
        raise CheckFail(f"card parse: {e}")
    render = {"masked": "masked", "swapped": "swapped"}.get(spec.get("label"), "base") if f == "choice" else "base"
    compare_card(card, pc, render=render)
    key = (card.card_id, render, qtype == "noul")
    tree = SB.Tree(pc)
    if len(pc.examples) != len(card.examples):
        raise CheckFail("example count differs")
    for cid, txt in pc.examples:
        try:
            pex = PZ.parse_report(txt, pc, inline=True)
        except PZ.ParseError as e:
            raise CheckFail(f"example parse: {e}")
        if pex.frames or pex.attacks or solve_both(pc, tree, pex.vec) != cid:
            raise CheckFail("example does not re-solve to its code")
    if len(pc.worked) != len(card.worked):
        raise CheckFail("worked-item count differs")
    for (k, txt), (pid, ptxt) in zip(card.worked, pc.worked):
        if pid != card.ids[k] or ptxt != txt:
            raise CheckFail("worked item differs")
        try:
            pex = PZ.parse_report(ptxt, pc, inline=True)
        except PZ.ParseError as e:
            raise CheckFail(f"worked parse: {e}")
        if pex.frames or pex.attacks or solve_both(pc, tree, pex.vec) != pid:
            raise CheckFail("worked item does not re-solve to its answer")
    t = card.tax
    # question parse (negcount on the question sentence alone: k_syn = k_all = n_frame)
    nc = negcount.count(question)
    if f in ("yn", "gyn"):
        if not (nc.k_syn == nc.k_all == spec["n_frame"]):
            raise CheckFail("negcount on the question != n_frame")
    if f == "inverted":
        blocks = split_inverted(row["state"], spec["refs"])
        got = None
        for ref, txt in blocks:
            pit = PZ.parse_record(txt, pc) if pc.fields else PZ.parse_report(txt, pc)
            k = solve_both(pc, tree, pit.vec)
            want_it = next(x for x in spec["reps"] if x.desig == pit.desig)
            if pit.vec != gen_vec(card, want_it):
                raise CheckFail("inverted report vector")
            if k == code_of(card, spec["K"]):
                if got is not None:
                    raise CheckFail("two reports get K")
                got = ref
        want = got if got is not None else lex.NONE_REPORTS
        if want != row["gold"]:
            raise CheckFail("inverted gold")
        return {"ok": True}
    it = spec["item"]
    try:
        pit = PZ.parse_record(row["state"], pc) if pc.fields else PZ.parse_report(row["state"], pc)
    except PZ.ParseError as e:
        raise CheckFail(f"item parse: {e}")
    if pit.desig != it.desig:
        raise CheckFail("subject line")
    if pit.vec != gen_vec(card, it):
        raise CheckFail(f"focal vector differs: {pit.vec} vs {gen_vec(card, it)}")
    if sorted(map(cstr, pit.frames)) != gen_frames(card, it):
        raise CheckFail(f"frames differ: {sorted(map(cstr, pit.frames))} vs {gen_frames(card, it)}")
    if bool(pit.attacks) != bool(it.attack):
        raise CheckFail("attack frame")
    # every attribute stated unless it is the row's missing attribute with a card default
    for a in pc.attrs if card.form != "short" else []:
        if a["name"] not in pit.vec and not (pc.default and pc.default[0] == a["name"]):
            raise CheckFail("attribute not stated without a missing rule")
    kB = solve_both(pc, tree, pit.vec)
    kA = code_of(card, spec["gold_code"])
    if kB != kA:
        raise CheckFail(f"G2: solver B {kB} != solver A {kA}")
    if f == "yn":
        m = None
        for qk in ("yn", "yn_neg", "yn_dneg"):
            pat = re.escape(lex.Q[qk]).replace(re.escape("{report}"), r"(.+?)").replace(re.escape("{K}"), r"(.+?)")
            mm = re.fullmatch(pat, question)
            if mm:
                m = (qk, mm.group(2))
                break
        if m is None:
            raise CheckFail("yes/no question frame")
        Kt = m[1]
        if card.form != "short" and Kt not in pc.codes:
            # name-form question: map name -> ID through the parsed card
            ids = [cid for cid, c in pc.codes.items() if c.get("name") == Kt]
            if len(ids) != 1:
                raise CheckFail("asked name")
            Kt = ids[0]
        nf = lex.N_FRAME[m[0]]
        gold = 1 if ((kB == Kt) != (nf == 1)) else 0
        if gold != row["gold"]:
            raise CheckFail("yes/no gold")
    elif f == "gyn":
        G = spec["G"]
        if pc.shape == "key":
            path = SB.walk_key(pc, SB.with_default(pc, pit.vec))[1]
            hit = card.gnames[G] in {pc.gnames[n] for n in path if n in pc.gnames}
        else:
            gb = SB.groups_c(pc, pit.vec)
            hit = gb == card.gnames[G]
        nf = spec["n_frame"]
        if (1 if hit != (nf == 1) else 0) != row["gold"]:
            raise CheckFail("group yes/no gold")
    elif f == "coarse":
        if pc.shape == "key":
            path = SB.walk_key(pc, SB.with_default(pc, pit.vec))[1]
            gb = [pc.gnames[n] for n in path if n in pc.gnames]
            if len(gb) != 1 or gb[0] != row["gold"]:
                raise CheckFail("coarse gold (key)")
        elif SB.groups_c(pc, pit.vec) != row["gold"]:
            raise CheckFail("coarse gold")
    elif f == "choice":
        opts = row["options"]
        lf = spec["label"]
        # map options to codes through the parsed card
        offered = {}
        for o in opts:
            if o == lex.NONE_CODES:
                continue
            if card.form == "short":
                offered[o] = o
            elif o in pc.codes:
                offered[o] = o
            else:
                hits = [cid for cid, c in pc.codes.items() if c.get("option") == o or c.get("name") == o]
                if len(hits) != 1:
                    if lf == "swapped":
                        hits = [card.ids[k] for k in range(len(t.codes)) if card.swapped[k] == o]
                    if len(hits) != 1:
                        raise CheckFail(f"option {o!r} maps to no code")
                offered[o] = hits[0]
        want_shown = sorted(code_of(card, k) for k in spec["shown"])
        if sorted(offered.values()) != want_shown:
            raise CheckFail("displayed code set differs")
        inv = {v: k for k, v in offered.items()}
        want = inv.get(kB, lex.NONE_CODES)
        if want == lex.NONE_CODES and lex.NONE_CODES not in opts:
            raise CheckFail("gold not offered and no none option")
        if want != row["gold"]:
            raise CheckFail(f"choice gold {row['gold']!r} != parsed {want!r}")
    return {"ok": True}


def split_inverted(state: str, refs):
    """Report blocks of an inverted row: each begins with its case reference line."""
    lines = state.split("\n")
    out, cur, curref = [], [], None
    for ln in lines:
        s = re.sub(r"^(?:\d+\. |[-*•+·] )", "", ln.strip())
        if s in refs:
            if curref is not None:
                out.append((curref, "\n".join(cur)))
            curref, cur = s, []
        elif curref is not None:
            cur.append(ln)
    if curref is not None:
        out.append((curref, "\n".join(cur)))
    if sorted(r for r, _ in out) != sorted(refs):
        raise CheckFail("case references do not map one to one to report blocks")
    return out
