"""F10 renderer: hidden structure -> card IR (fmt1 blocks), record Doc IR, question and options, placed by the row
layouts L1-L8 (G0 section 2 Row layout; A16.1 (g)). Every phrase comes from lexicon.py; every card-level choice
(phrase variants, definition style, reading-rule paraphrases) is fixed per card in card['rc']."""
from __future__ import annotations

import hashlib

import lexicon as L
import model as M
from common import uhash
from values import date_text, list_text, num_text, val_text


def pick(lst, *key):
    return lst[int(uhash(*key) * len(lst)) % len(lst)]


def vtext(card, s, g):
    return val_text(card["legend"][s], g, card)


def atom_text(card, at, key, alt=0):
    """One atom in the operator lexicon. key fixes the phrase variant (card-fixed); alt shifts it (S6 rewrites)."""
    leg = card["legend"]
    t = at["t"]
    a = leg[at["a"]]
    an = a["name"]

    def ch(lst):
        return lst[(int(uhash(card["card_id"], key) * 997) + alt) % len(lst)]
    if t == "cmp":
        if a["type"] == "date":
            return ch(L.DATE_CMP[at["op"]]).format(a=an, D=date_text(at["c"], card["rc"]["date_fmt"]))
        pool = list(L.CMP[at["op"]])
        if a["type"] == "count" and at["op"] in ("ge", "lt"):
            pool += L.CMP[at["op"] + "_count"]
        v = val_text(a, at["c"], card, conv_u1=True) if at.get("u1") else vtext(card, at["a"], at["c"])
        return ch(pool).format(a=an, v=v)
    if t == "rng":
        if a["type"] == "date":
            return ch(L.WINDOW).format(a=an, D=date_text(at["lo"], card["rc"]["date_fmt"]),
                                       D2=date_text(at["hi"], card["rc"]["date_fmt"]))
        tpl = ch(L.HALF) if at["half"] else ch(L.RNG)
        return tpl.format(a=an, v=vtext(card, at["a"], at["lo"]), w=vtext(card, at["a"], at["hi"]))
    if t == "rel":
        return ch(L.REL[at["dir"]]).format(a=an, N=at["n"], E=leg[at["e"]]["name"])
    if t == "cat":
        S = list_text(at["S"])
        if not at["neg"]:
            return ch(L.CAT_IN1 if len(at["S"]) == 1 else L.CAT_INN).format(a=an, S=S)
        st = at.get("style")
        if st == "other":
            return ch(L.CAT_OTHER).format(a=an, S=S)
        if st == "except":
            return ch(L.CAT_EXCEPT).format(a=an, S=S)
        return ch(L.CAT_NOT1 if len(at["S"]) == 1 else L.CAT_NOTN).format(a=an, S=S)
    if t == "flag":
        return ch(L.FLAG[at["v"]]).format(a=an)
    if t == "tag":
        return ch(L.TAG[at["m"]]).format(a=an, S=list_text(at["S"]), k=at["kk"])
    raise ValueError(t)


def ref_text(card, ref):
    to = ref["to"]
    nm = card["names"][to]
    if card["defs"][to]["helper"]:
        return (L.WREF_NEG if ref["neg"] else L.WREF_POS).format(W=nm)
    return (L.REF_NEG if ref["neg"] else L.REF_POS).format(Y=nm)


def cond_text(card, c, key, alt=0):
    return ref_text(card, c) if c["k"] == "ref" else atom_text(card, c, key, alt)


def item_text(card, it, key, alt=0):
    if it["k"] == "ref":
        return ref_text(card, it)
    a = atom_text(card, it["atom"], key + ("a",), alt)
    if it.get("unless") is not None:
        return L.UNLESS.format(A=a, B=cond_text(card, it["unless"], key + ("u",), alt))
    return a


def body_text(card, did, body, key, alt=0, line_form=False, order=None):
    f = body["form"]
    its = body["items"]
    idx = order if order is not None else list(range(len(its)))
    txt = [item_text(card, its[i], key + (i,), alt) for i in idx]
    if f == "single":
        return txt[0]
    if f == "XOR":
        return L.XOR.format(A=txt[0], B=txt[1])
    if f == "NEITHER":
        return L.NEITHER.format(A=txt[0], B=txt[1])
    head = L.LIST_HEAD[f]
    if line_form:
        return head + ":\n" + "\n".join("- " + x for x in txt)
    return head + ": " + L.ITEM_SEP.join(txt)


def def_text(card, did, alt=0, name=None, line_form=False):
    """The definition's text after its name frame: body sentence, then ONLY-IF and Exception sentences."""
    d = card["defs"][did]
    nm = name or card["names"][did]
    key = (did,)
    out = body_text(card, did, d["body"], key, alt, line_form=line_form) + "."
    if d.get("onlyif") is not None:
        out += " " + L.ONLYIF.format(T=nm, C=cond_text(card, d["onlyif"], key + ("o",), alt))
    if d.get("exc") is not None:
        c = d["exc"]
        if c["k"] == "ref":
            to = c["to"]
            if card["defs"][to]["helper"]:
                out += " " + L.EXC_WREF.format(W=card["names"][to], T=nm)
            else:
                out += " " + L.EXC_REF.format(Y=card["names"][to], T=nm)
        else:
            out += " " + L.EXC_ATOM.format(B=atom_text(card, c, key + ("e",), alt), T=nm)
    return out


# S5 (held out, dev only): FAQ / clarification-thread glossary. The base line is the body; every narrowing part
# (ONLY-IF = AND scope limit, Exception = AND NOT) is one FAQ answer in its registered sentence frame; a term with no
# narrowing part gets one restate answer that repeats a printed boundary reading rule exactly (ST14-ST18, ST20-ST22).
FAQ_Q_NARROW = ["Does every record like that count as {T}?", "Is anything left out of {T}?",
                "Are there limits on what counts as {T}?"]
FAQ_Q_RESTATE = ["How are values at a boundary read for {T}?", "Do edge values count for {T}?"]
FAQ_RESTATE_IDS = ("ST14", "ST15", "ST16", "ST17", "ST18", "ST20", "ST21", "ST22")


def faq_def_text(card, did, restate_rules):
    d = card["defs"][did]
    nm = card["names"][did]
    key = (did,)
    out = body_text(card, did, d["body"], key, 0) + "."
    ans = []
    if d.get("onlyif") is not None:
        ans.append(L.ONLYIF.format(T=nm, C=cond_text(card, d["onlyif"], key + ("o",), 0)))
    if d.get("exc") is not None:
        c = d["exc"]
        if c["k"] == "ref":
            to = c["to"]
            if card["defs"][to]["helper"]:
                ans.append(L.EXC_WREF.format(W=card["names"][to], T=nm))
            else:
                ans.append(L.EXC_REF.format(Y=card["names"][to], T=nm))
        else:
            ans.append(L.EXC_ATOM.format(B=atom_text(card, c, key + ("e",), 0), T=nm))
    h = int(hashlib.sha256(f"{card['card_id']}|{did}|faq".encode()).hexdigest(), 16)
    for i, a in enumerate(ans):
        out += " Q: " + FAQ_Q_NARROW[(h + i) % len(FAQ_Q_NARROW)].format(T=nm) + " A: " + a
    if (not ans or h % 3 == 0) and restate_rules:
        out += " Q: " + FAQ_Q_RESTATE[h % len(FAQ_Q_RESTATE)].format(T=nm) + " A: " + restate_rules[h % len(restate_rules)]
    return out
