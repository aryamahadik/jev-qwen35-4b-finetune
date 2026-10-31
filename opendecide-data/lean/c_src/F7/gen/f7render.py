"""F7 renderer: criterion text, card IR (C-lines by 3.3, level definitions by 3.5 L03-L07), case Doc IR, and the row
fields through fmt1 (render_row_text + loader_check). Text only: no label is decided here.
"""
from __future__ import annotations

import datetime as dt
import sys
from fractions import Fraction
from pathlib import Path

LEAN = Path(__file__).resolve().parents[3]
FMT1 = LEAN / "c_src/formats/formats-1"
if str(FMT1) not in sys.path:
    sys.path.insert(0, str(FMT1))

from fmt1 import card as fcard  # noqa: E402
from fmt1 import pool  # noqa: E402
from fmt1.render import BLANK, OMIT, FormatError  # noqa: E402

import f7lex as LX  # noqa: E402
import f7model as M  # noqa: E402
import f7cards as CD  # noqa: E402


# ------------------------------------------------------------------------------------------------ values
def places(r: Fraction) -> int:
    p = 0
    x = Fraction(r)
    while x.denominator != 1:
        x *= 10
        p += 1
    return p


def fmt_num(x, item: dict) -> str:
    p = places(item["r"])
    x = Fraction(x)
    if p == 0:
        assert x.denominator == 1, x
        return str(x.numerator)
    q = x * 10 ** p
    assert q.denominator == 1
    n = int(q)
    sign = "-" if n < 0 else ""
    n = abs(n)
    s = str(n).rjust(p + 1, "0")
    return f"{sign}{s[:-p]}.{s[-p:]}"


def fmt_qty(x, item: dict) -> str:
    return f"{fmt_num(x, item)} {item['unit']}"


def fmt_date(d: int, style: str) -> str:
    x = M.from_day(d)
    if style == "iso":
        return x.isoformat()
    if style == "mdy":
        return f"{LX.MONTHS[x.month - 1]} {x.day}, {x.year}"
    return f"{x.day} {LX.MONTHS[x.month - 1]} {x.year}"


def fmt_value(x, item: dict, card: dict) -> str:
    k = item["kind"]
    if k == "num":
        return fmt_qty(x, item)
    if k == "date":
        return fmt_date(x, card["date_fmt"])
    if k == "ord":
        return item["ranks"][x]
    raise ValueError(k)


def _a(term: str) -> str:
    return ("an " if term[0].lower() in "aeiou" else "a ") + term


def dX(term: str, det: str) -> str:
    return f"{det} {term}" if det else term


# ------------------------------------------------------------------------------------------------ criteria
def cmp_template(a: dict) -> str:
    cls = "count" if a.get("count") else "noncount"
    table = {">=": LX.INCL_LO, "<=": LX.INCL_HI, ">": LX.EXCL_LO, "<": LX.EXCL_HI}[a["op"]][cls]
    return table[a["wv"] % len(table)]


def atom_text(a: dict, card: dict, prefix_ok: bool, term_override: str | None = None) -> str:
    it = card["items"][a["item"]]
    X = term_override or it["term"]
    k = it["kind"]
    if k == "bool":
        if it["fkind"] == "event":
            if a["op"] == "present":
                return LX.EVENT_POS.format(X=X)
            f = a.get("neg_form", 0) % 3
            if f == 2 and not prefix_ok:
                f = 0
            return LX.EVENT_NEG[f].format(X=X)
        if a["op"] == "present":
            return LX.STATE_POS.format(X=X)
        f = a.get("neg_form", 0) % 3
        use_prefix = f >= 1 and prefix_ok
        return LX.STATE_NEG[1 if use_prefix else 0].format(X=X)
    if k == "num":
        tmpl = cmp_template(a)
        N = fmt_qty(a["t"], it)
        if tmpl.startswith("exceeds"):
            return f"{X} exceeds {N}"
        return f"{X} is " + tmpl.format(N=N)
    if k == "date":
        if a["op"] == "within":
            return f"{X} is " + LX.DATE_CMP["within"].format(N=a["N"], D=fmt_date(a["t"], card["date_fmt"]))
        key = {"<=": "on_or_before", "<": "before", ">=": "on_or_after", ">": "after"}[a["op"]]
        return f"{X} is " + LX.DATE_CMP[key].format(D=fmt_date(a["t"], card["date_fmt"]))
    if k == "ord":
        key = {">=": "rge", ">": "rgt", "<=": "rle", "<": "rlt"}[a["op"]]
        return f"{X} is " + LX.RANK_CMP[key].format(r=it["ranks"][a["t"]])
    raise ValueError(k)


def crit_text(c: dict, card: dict) -> str:
    t = c["t"]
    if t == "atom":
        return atom_text(c["a"], card, True)
    if t in ("and", "or"):
        return f" {t} ".join(crit_text_inline(p, card) for p in c["parts"])
    if t == "unless":
        return f"{crit_text_inline(c['a'], card)} unless {atom_text(c['b'], card, False)}"
    if t in ("allof", "anyof"):
        head = "all of" if t == "allof" else "any of"
        parts = []
        for i, p in enumerate(c["parts"]):
            if p["t"] in ("allof", "anyof"):
                assert i == len(c["parts"]) - 1
                inner = "all of" if p["t"] == "allof" else "any of"
                parts.append(f"{inner} (" + "; ".join(atom_text(q["a"], card, True) for q in p["parts"]) + ")")
            else:
                parts.append(atom_text(p["a"], card, True))
        return f"{head}: " + "; ".join(parts)
    if t == "onlyif":
        raise ValueError("onlyif is rendered by level_text")
    raise ValueError(t)


def crit_text_inline(c: dict, card: dict) -> str:
    if c["t"] == "atom":
        return atom_text(c["a"], card, False)
    if c["t"] == "and":
        return " and ".join(crit_text_inline(p, card) for p in c["parts"])
    raise ValueError(c["t"])


def opt_ref(card: dict, k: int) -> str:
    return f"{card['plan']['level_word']} {card['levels']['nums'][k]}"


def band_text(card: dict, lo: int, hi: int, unit: str | None, smallest: bool, largest: bool) -> str:
    u = f" {unit}" if unit else ""
    if largest:
        return f"{lo}{u} or more"
    if smallest and card.get("low_word") == "or fewer":
        return f"{hi}{u} or fewer"
    return f"{lo}-{hi}{u}"


def level_text(card: dict, k: int) -> str | None:
    """Definition text of level index k (None: no definition line, L_0 on ladder / highest / grid)."""
    mode = card["mode"]
    if mode in ("ladder", "highest"):
        if k == 0:
            return None
        c = card["crits"][k]
        if c["t"] == "onlyif":
            return f"{crit_text(c['main'], card)}. {opt_ref(card, k)} applies only if {atom_text(c['c'], card, True)}"
        return crit_text(c, card)
    if mode in ("count", "points"):
        bv = card["band_by_value"]
        lo, hi = card["bands"][k]
        j = bv.index((lo, hi))
        return band_text(card, lo, hi, None, j == 0, j == len(bv) - 1)
    if mode == "cut":
        it = card["items"][card["qty"]]
        K = card["K"]
        j = k if card["rising"] else K - 1 - k
        cuts = card["cuts"]
        if card["integer"]:
            lo = cuts[j - 1] if j >= 1 else it["lo"]
            hi = cuts[j] - 1 if j < K - 1 else None
            if j == K - 1:
                return f"{fmt_num(lo, it)} {it['unit']} or more"
            if j == 0 and card.get("low_word") == "or fewer":
                return f"{fmt_num(hi, it)} {it['unit']} or fewer"
            return f"{fmt_num(lo, it)}-{fmt_num(hi, it)} {it['unit']}"
        q = lambda x: fmt_qty(x, it)  # noqa: E731
        if card["side"] == "high":
            if j == 0:
                return f"below {q(cuts[0])}"
            if j == K - 1:
                return f"{q(cuts[-1])} or more"
            return f"{q(cuts[j - 1])} or more and below {q(cuts[j])}"
        if j == 0:
            return f"{q(cuts[0])} or less"
        if j == K - 1:
            return f"above {q(cuts[-1])}"
        return f"above {q(cuts[j - 1])} and at most {q(cuts[j])}"
    if mode == "grid":
        return None
    raise ValueError(mode)


def grid_cell(a: dict | None, card: dict) -> str:
    if a is None:
        return "not required"
    it = card["items"][a["item"]]
    txt = atom_text(a, card, False)
    head = it["term"] + " "
    assert txt.startswith(head)
    cell = txt[len(head):]
    if cell.startswith("is ") and it["kind"] in ("num", "date", "ord"):
        cell = cell[3:]
    return cell


# ------------------------------------------------------------------------------------------------ C-lines (3.3)
def c_lines(card: dict, subject: str) -> list[tuple[str, str]]:
    """(tag, text) of every C-line the card's features map to, in a fixed card order (row-specific only in C21)."""
    p = card["plan"]
    f = card["features"]
    lv = card["levels"]
    LW = p["level_word"]
    K = card["K"]
    nums = lv["nums"]
    out = [("C17", LX.C["C17"].format(LW=LW, n0=nums[0], nK=nums[K - 1], MB=lv["MB"], Q=lv["Q"]))]
    mode = card["mode"]
    if mode == "ladder":
        out.append(("C16", LX.C["C16_ladder"]))
        out.append(("C18", LX.C["C18_ladder"].format(LW=LW, n0=nums[0], n1=nums[1])))
    elif mode == "highest":
        if p["defs_style"] == "decision_list":
            out.append(("C16", LX.C["C16_dlist"].format(LW=LW, n=nums[K - 1])))
        else:
            out.append(("C16", LX.C["C16_highest"]))
        out.append(("C18", LX.C["C18_highest"].format(LW=LW, n0=nums[0])))
    elif mode == "count":
        out.append(("C16", LX.C["C16_count"]))
    elif mode == "points":
        out.append(("C16", LX.C["C16_points"]))
    elif mode == "cut":
        out.append(("C16", LX.C["C16_cut"].format(Q="the " + card["items"][card["qty"]]["term"])))
    elif mode == "grid":
        out.append(("C16", LX.C["C16_grid"]))
        out.append(("C18", LX.C["C18_grid"].format(LW=LW, n0=nums[0])))
    out.append(("C19", LX.C["C19"]))
    # C1
    bools = [it for it in card["items"].values() if it["kind"] == "bool"]
    if not bools or card["c1_form"] == "generic":
        out.append(("C1", LX.C["C1_generic"]))
    elif card["c1_form"] == "list" and len(bools) >= 2:
        terms = [it["term"] for it in sorted(bools, key=lambda it: card["item_order"].index(it["key"]))]
        out.append(("C1", LX.C["C1_list"].format(FL=", ".join(terms))))
    else:
        for it in sorted(bools, key=lambda it: card["item_order"].index(it["key"])):
            out.append(("C1", LX.C["C1_one"].format(F=it["term"])))
    out.append(("C2", LX.C["C2"]))
    if p["sampler"] == "S4":
        out.append(("C3", LX.C["C3"].format(R=fmt_date(card["R"], card["date_fmt"]))))
    if f["unless"]:
        out.append(("C4", LX.C["C4"]))
    if f["onlyif"]:
        for k in range(1, K):
            if card["crits"][k]["t"] == "onlyif":
                out.append(("C5", LX.C["C5"].format(LW=LW, n=nums[k])))
    if f["and"]:
        out.append(("C6", LX.C["C6"]))
    if f["or"]:
        out.append(("C7", LX.C["C7"]))
    if f["incl_words"]:
        out.append(("C8", LX.C["C8"].format(WL=_wl(f["incl_words"]))))
    if f["excl_words"]:
        out.append(("C9", LX.C["C9"].format(WL=_wl(f["excl_words"]))))
    if f["date"]:
        out.append(("C10", LX.C["C10"].format(R=fmt_date(card["R"], card["date_fmt"]))))
    if mode in ("count", "points") or (mode == "cut" and card["integer"]):
        out.append(("C11", LX.C["C11_int"]))
    elif mode == "cut":
        out.append(("C11", LX.C["C11_high"] if card["side"] == "high" else LX.C["C11_low"]))
    if f["continuous"]:
        out.append(("C12", LX.C["C12"]))
    if f["override"]:
        out.append(("C13", LX.C["C13_prec"].format(LW=LW)))
        if f["both"]:
            w = "maximum" if card["winner"] == "cap" else "minimum"
            mw = next(o["m"] for o in card["overrides"] if o["type"] == card["winner"])
            out.append(("C13", LX.C["C13_both"].format(W=w, LW=LW, n=nums[mw])))
    if mode in ("count", "points"):
        out.append(("C14", LX.C["C14"]))
    if card.get("c15"):
        out.append(("C15", LX.C["C15_key"] if card["c15"] == "key" else LX.C["C15_blank"]))
    if p["sampler"] == "S4":
        out.append(("C20", LX.C["C20"]))
    if card.get("c21"):
        out.append(("C21", LX.C["C21"].format(S=subject, ENTS=card["ents"])))
    if p.get("attack"):
        out.append(("C24", LX.C["C24"]))
    if f["ord"]:
        it = next(it for it in card["items"].values() if it["kind"] == "ord")
        out.append(("C25", LX.C["C25"].format(RL=", ".join(it["ranks"]))))
    return out


def _wl(words: list[str]) -> str:
    q = [f"'{w}'" for w in words]
    if len(q) == 1:
        return q[0]
    return ", ".join(q[:-1]) + " and " + q[-1]


def override_lines(card: dict) -> list[str]:
    out = []
    LW = card["plan"]["level_word"]
    for o in card.get("overrides", []):
        cond = crit_text(o["cond"], card)
        key = "C13_floor" if o["type"] == "floor" else "C13_cap"
        out.append(LX.C[key].format(COND=cond, LW=LW, n=card["levels"]["nums"][o["m"]]))
    return out


def listed_lines(card: dict) -> list[str]:
    if card["mode"] == "count":
        return [card["items"][k]["term"] for k in card["listed"]]
    if card["mode"] == "points":
        return [f"{card['items'][k]['term']}: {card['weights'][k]} point" + ("s" if card["weights"][k] != 1 else "")
                for k in card["listed"]]
    return []


def alias_lines(card: dict) -> list[str]:
    out = []
    for k in card["item_order"]:
        it = card["items"][k]
        if it["kind"] == "bool" and card.get("aliases_on") and it.get("alias"):
            out.append(f"{it['term']} (also written {it['alias']})")
    return out


# ------------------------------------------------------------------------------------------------ card IR (3.5)
def card_ir(card: dict, subject: str, *, descending: bool = False, fewshot: list | None = None) -> dict:
    p = card["plan"]
    K = card["K"]
    opts = card["levels"]["options"]
    style = p["defs_style"]
    blocks = []
    lines = c_lines(card, subject)
    paras = [t for _, t in lines]
    paras += override_lines(card)
    al = alias_lines(card)
    if al:
        paras += al
    ll = listed_lines(card)
    defs_entries = []
    for k in range(K):
        t = level_text(card, k)
        if t is not None:
            defs_entries.append({"name": opts[k], "text": t})
    if style in ("short",):
        for x in paras:
            blocks.append({"type": "para", "text": x})
        if ll:
            blocks.append({"type": "para", "text": ("Listed factors" if card["mode"] == "count" else
                                                    "Points per listed factor") + ":"})
            blocks.append({"type": "items", "items": ll})
        ents = defs_entries[::-1] if descending else defs_entries
        for e in ents:
            blocks.append({"type": "para", "text": f"{e['name']}: {e['text']}"})
    else:
        for x in paras:
            blocks.append({"type": "para", "text": x})
        if ll:
            blocks.append({"type": "para", "text": ("Listed factors" if card["mode"] == "count" else
                                                    "Points per listed factor") + ":"})
            blocks.append({"type": "items", "items": ll})
        if card["mode"] == "grid":
            cols = card["grid_cols"]
            hdr = [card["plan"]["level_word"]] + [card["items"][c]["term"] for c in cols]
            rows = []
            rng_rows = list(range(1, K))
            if descending:
                rng_rows = rng_rows[::-1]
            for k in rng_rows:
                cells = {a["item"]: a for a in card["grid"][k]}
                rows.append([opts[k]] + [grid_cell(cells.get(c), card) for c in cols])
            blocks.append({"type": "table", "columns": hdr, "rows": rows, "caption": None})
        elif style in ("one_line", "one_line_examples"):
            blocks.append({"type": "defs", "variant": card["dv"], "heading": None, "entries": defs_entries})
        elif style == "rubric_table":
            ents = defs_entries[::-1] if descending else defs_entries
            blocks.append({"type": "defs", "variant": card["dv"], "heading": None, "columns": card["table_cols"],
                           "entries": ents})
        elif style == "decision_list":
            blocks.append({"type": "defs", "variant": "DV35", "heading": None, "entries": defs_entries[::-1]})
    if fewshot:
        blocks.append({"type": "fewshot", "template": card["ft"], "heading": None, "examples": fewshot})
    blocks.append({"type": "task", "text": card["task_line"]})
    return {"title": None, "blocks": blocks}


# ------------------------------------------------------------------------------------------------ case text
def sentence(fact: dict, card: dict, case: dict) -> str:
    who = fact["who"]
    k = fact["kind"]
    if k in ("bool", "plan", "partial", "filler"):
        if k == "filler":
            X, det, fk = fact["term"], fact["det"], fact["fkind"]
        else:
            it = card["items"][fact["item"]]
            if fact.get("alias"):
                X, det = it["alias"], it["alias_det"]
            else:
                X, det = it["term"], it["det"]
            fk = it["fkind"]
        dx = dX(X, det)
        fi = fact.get("frame", 0)
        if k == "plan":
            fr = LX.F_EVENT_PLAN if fk == "event" else LX.F_STATE_PLAN
        elif k == "partial":
            fr = LX.F_EVENT_PARTIAL if fk == "event" else LX.F_STATE_PARTIAL
        elif fact["polarity"]:
            fr = LX.F_EVENT_AFF if fk == "event" else LX.F_STATE_AFF
        else:
            fr = LX.F_EVENT_NEG if fk == "event" else LX.F_STATE_NEG
        return fr[fi % len(fr)].format(S=who, X=X, dX=dx)
    if k == "value":
        it = card["items"][fact["item"]]
        return LX.F_VALUE.format(S=who, aT=_a(it["term"]), V=fmt_value(fact["value"], it, card))
    if k == "inert":
        return LX.F_VALUE.format(S=who, aT=_a(fact["term"]), V=fact["value"])
    if k == "inject":
        return fact["text"]
    raise ValueError(k)


def field_pair(fact: dict, card: dict, typed: bool, markers: tuple) -> list:
    k = fact["kind"]
    if k == "missing":
        it = card["items"][fact["item"]]
        return [it["term"], OMIT if typed else BLANK]
    if k in ("bool", "filler"):
        term = fact["term"] if k == "filler" else (card["items"][fact["item"]]["alias"] if fact.get("alias")
                                                   else card["items"][fact["item"]]["term"])
        return [term, markers[0] if fact["polarity"] else markers[1]]
    if k == "value":
        it = card["items"][fact["item"]]
        return [it["term"], fmt_value(fact["value"], it, card)]
    if k == "inert":
        return [fact["term"], fact["value"]]
    raise ValueError(k)


def case_doc(card: dict, case: dict, container: str, *, for_example: bool = False) -> dict | str:
    """Doc IR of the case record (state), or a single-line text for a worked case."""
    facts = case["facts"]
    if for_example:
        return " ".join(sentence(f, card, case) for f in facts if f["kind"] not in ("inject", "missing"))
    typed = container in ("json", "yaml")
    markers = card["markers"]
    if case["layout"] == "fields":
        pairs = [[card["singular"], case["subject"]]]
        sents = []
        nrem = [0]

        def rkey():
            nrem[0] += 1
            return card["remark_key"] if nrem[0] == 1 else f"{card['remark_key']} {nrem[0]}"
        for f in facts:
            if f["kind"] == "repeat":
                pairs.append([rkey(), sentence(f["of"], card, case)])
            elif f["who"] == case["subject"] and f["kind"] in ("bool", "filler", "value", "inert", "missing"):
                pairs.append(field_pair(f, card, typed, markers))
            else:
                sents.append(sentence(f, card, case))
        blocks = [{"type": "fields", "label": None, "pairs": pairs}]
        if sents:
            if container in ("key_value", "csv"):
                for s_ in sents:
                    blocks[0]["pairs"].append([rkey(), s_])
            else:
                blocks.append({"type": "para", "text": " ".join(sents)})
        return {"title": None, "meta": [], "blocks": blocks}
    # narrative layout
    sents = []
    for f in facts:
        if f["kind"] == "repeat":
            sents.append(sentence(f["of"], card, case))
        else:
            sents.append(sentence(f, card, case))
    if container == "email_thread":
        roles = card["roles"]
        n = 2 if len(sents) < 6 else 3
        chunks = _chunks(sents, n)
        msgs = []
        for i, ch in enumerate(chunks):
            a, b = roles[i % 2], roles[(i + 1) % 2]
            msgs.append({"speaker": a, "to": b, "text": " ".join(ch)})
        return {"title": None, "meta": [], "blocks": [{"type": "messages", "messages": msgs}]}
    if container == "bullet_sop":
        return {"title": None, "meta": [], "blocks": [{"type": "items", "items": sents}]}
    n = 1 if len(sents) <= 3 else 2 if len(sents) <= 7 else 3
    return {"title": None, "meta": [], "blocks": [{"type": "para", "text": " ".join(ch)} for ch in _chunks(sents, n)]}


def _chunks(xs: list, n: int) -> list:
    n = max(1, min(n, len(xs)))
    k, r = divmod(len(xs), n)
    out, i = [], 0
    for j in range(n):
        m = k + (1 if j < r else 0)
        out.append(xs[i:i + m])
        i += m
    return [c for c in out if c]


# ------------------------------------------------------------------------------------------------ row fields
def render_fields(style: dict, card: dict, case: dict, cir: dict, question: str, wording: str) -> dict:
    doc = case_doc(card, case, style["container"])
    return fcard.render_row_text(style, doc=doc, question=question, qtype="choice", card=cir,
                                 options=card["levels"]["options"], wording=wording)


def must_show(cir: dict, question: str, wording: str) -> list[str]:
    return fcard.must_show(cir, question=question, wording=wording)
