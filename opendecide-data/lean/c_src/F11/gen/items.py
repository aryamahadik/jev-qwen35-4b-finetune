"""F11 item objects and prose report realization (G0 section 2: item object, frames, item guards).

An Item is the hidden focal vector plus its frames. realize() turns it into sentences: one frame per sentence, every
value-word sentence names its subject by its one designator (or the generic class form), carries its own marker, and
holds no anaphor (F11-R4-02). Sentence templates are renderer-side; the parser reads only the lexicon markers.
"""
from __future__ import annotations

import datetime as dt
from fractions import Fraction

import lex
from cards import fmt_num, fmt_date, unit_form
from tax import neighbours_of_cell, PRES, ABS

FRAME_KINDS = ("OTHER", "PRIOR", "LATER", "HYPO", "HEDGED", "GENERIC", "NEG")


class Item:
    def __init__(self, cell, missing=None):
        self.cell = tuple(cell)         # value index per attribute (the missing attribute keeps its index slot)
        self.missing = missing          # attribute index left unstated (SEM-03) or None
        self.exact = {}                 # attr idx -> exact Fraction / date of the focal value (num, date)
        self.surf = {}                  # attr idx -> surface word (nominal value word; presence term)
        self.pform = {}                 # presence attr idx -> 'has' | 'no' | 'lacks' | 'without' | 'denial'
        self.frames = []                # non-FOCAL frames: {'kind', 'attr', 'value', 'exact', 'surf', 'other'}
        self.inert = []                 # inert sentences
        self.desig = None
        self.attack = None
        self.cue = False                # a not-stated cue sentence about the focal entity (nominal missing attr)

    def stated(self, i) -> bool:
        return i != self.missing


def focal_value_text(card, item, i) -> str:
    a = card.attrs[i]
    if a.kind == "nom":
        return item.surf[i]
    if a.kind == "num":
        x = item.exact[i]
        return f"{fmt_num(x)} {unit_form(a, x)}"
    if a.kind == "date":
        return fmt_date(item.exact[i])
    raise ValueError


def frame_value_text(card, fr) -> str:
    a = card.attrs[fr["attr"]]
    if a.kind == "nom":
        return fr["surf"]
    if a.kind == "num":
        return f"{fmt_num(fr['exact'])} {unit_form(a, fr['exact'])}"
    if a.kind == "date":
        return fmt_date(fr["exact"])
    return fr["surf"]


def attr_word(card, item, i, key) -> str:
    """Attribute name or one listed term (numeric and date attributes: both are value words)."""
    a = card.attrs[i]
    if a.kind in ("num", "date"):
        opts = [a.name] + a.terms["attr"]
        return opts[key % len(opts)]
    return a.name


def focal_sentences(card, item, r) -> list[dict]:
    """FOCAL sentences: one attribute per sentence (presence in its own sentence)."""
    out = []
    D = item.desig
    for i, a in enumerate(card.attrs):
        if not item.stated(i):
            continue
        t = r.randrange(5)
        if a.kind == "pres":
            T = item.surf[i]
            f = item.pform[i]
            if f == "has":
                s = [f"{D} has {T}.", f"{r.choice(card.people)} reported that {D} has {T}.",
                     f"It was recorded that {D} has {T}."][t % 3]
            elif f == "no":
                s = f"{D} has no {T}."
            elif f == "lacks":
                s = f"{D} lacks {T}."
            elif f == "without":
                s = f"{D} is without {T}."
            else:
                s = f"{D} does not have {T}."
            out.append({"text": s, "frame": "FOCAL", "attr": i})
            continue
        A = attr_word(card, item, i, r.randrange(4))
        X = focal_value_text(card, item, i)
        verb = r.choice(("stated", "reported", "wrote", "said", "recorded"))
        s = [f"The {A} of {D} is {X}.", f"For {D}, the {A} is {X}.",
             f"{r.choice(card.people)} {verb} that the {A} of {D} is {X}.",
             f"It was recorded that the {A} of {D} is {X}.", f"The {A} of {D} is {X}."][t]
        out.append({"text": s, "frame": "FOCAL", "attr": i})
    return out


def frame_sentence(card, item, fr, r) -> str:
    a = card.attrs[fr["attr"]]
    D = item.desig
    ev = card.event
    k = fr["kind"]
    if a.kind == "pres":
        T = fr["surf"]
        if k == "OTHER":
            return f"{fr['other']} has {T}."
        if k == "PRIOR":
            return f"{r.choice(('In an earlier', 'At a previous', 'During a prior'))} {ev}, {D} had {T}."
        if k == "LATER":
            return f"{r.choice(('At the next', 'In a later', 'During a future'))} {ev}, {D} will have {T}."
        if k == "HYPO":
            return f"Hypothetically, {D} would have {T}."
        if k == "HEDGED":
            return f"{r.choice(card.people)} {fr['hedge']} that {D} has {T}."
        if k == "GENERIC":
            return f"Across all {card.entities}, {T} is common."
        raise ValueError("no negated lure on a presence attribute")
    A = attr_word(card, item, fr["attr"], r.randrange(4))
    X = frame_value_text(card, fr)
    if k == "OTHER":
        return r.choice((f"The {A} of {fr['other']} is {X}.", f"For {fr['other']}, the {A} is {X}."))
    if k == "PRIOR":
        return f"{r.choice(('In an earlier', 'At a previous', 'During a prior'))} {ev}, the {A} of {D} was {X}."
    if k == "LATER":
        return f"{r.choice(('At the next', 'In a later', 'During a future'))} {ev}, the {A} of {D} will be {X}."
    if k == "HYPO":
        return f"Hypothetically, the {A} of {D} would be {X}."
    if k == "HEDGED":
        return f"{r.choice(card.people)} {fr['hedge']} that the {A} of {D} is {X}."
    if k == "GENERIC":
        if a.kind == "nom":
            return f"Across all {card.entities}, the {A} {X} is common."
        return f"Across all {card.entities}, a {A} of {X} is common."
    if k == "NEG":
        return f"The {A} of {D} is not {X}."
    raise ValueError(k)


def cue_sentence(card, D, i, r) -> str:
    a = card.attrs[i]
    cue = r.choice(lex.NOT_STATED_CUES)
    return f"The {a.name} of {D} {cue}."


def realize(card, item, r) -> list[dict]:
    """All report sentences (subject line excluded) in report order: FOCAL, frames, cue, inert."""
    sents = focal_sentences(card, item, r)
    for fr in item.frames:
        sents.append({"text": frame_sentence(card, item, fr, r), "frame": fr["kind"], "attr": fr["attr"]})
    if item.cue:
        sents.append({"text": cue_sentence(card, item.desig, item.missing, r), "frame": "INERT", "attr": None})
    for s in item.inert:
        sents.append({"text": s, "frame": "INERT", "attr": None})
    r.shuffle(sents)
    return sents


# ------------------------------------------------------------------------------------------------ value draws
def exact_in_band(a, b, r, *, place=None):
    """An exact grid value in band b. place: 'at' (the band's lower cut), 'below_next' (one grid step under the next
    cut), 'mid' (anywhere)."""
    vals = a.grid_values(b)
    lo, hi = a.band_range(b)
    if place == "at" and lo is not None:
        return lo
    if place == "below" and hi is not None:
        return vals[-1]
    if place == "above" and lo is not None:
        return vals[1] if len(vals) > 1 else vals[0]
    # anywhere, but >= 1 grid step from every cut on both sides (keeps the at / below / above shares honest)
    inner = vals[1:-1] if len(vals) > 3 else vals
    return r.choice(inner)


def surface_for(card, i, v, r):
    a = card.attrs[i]
    if a.kind == "nom" and card.form == "short":
        return a.values[v]
    if a.kind == "nom":
        opts = [a.values[v]] + a.terms.get(v, [])
        return r.choice(opts)
    if a.kind == "pres":
        return r.choice(a.terms["attr"])
    return None


def fill_focal(card, item, r, *, num_place=None):
    for i, a in enumerate(card.attrs):
        if not item.stated(i):
            continue
        v = item.cell[i]
        if a.kind in ("num", "date"):
            item.exact[i] = exact_in_band(a, v, r, place=(num_place or {}).get(i))
        elif a.kind == "nom":
            item.surf[i] = surface_for(card, i, v, r)
        else:
            item.surf[i] = surface_for(card, i, v, r)
            if v == PRES:
                item.pform[i] = "has"
            else:
                item.pform[i] = r.choice(("no", "lacks", "without", "denial"))


def lure_value(card, item, i, v, r):
    """The exact or surface form of value v of attribute i for a lure / echo frame."""
    a = card.attrs[i]
    fr = {"attr": i, "value": v}
    if a.kind in ("num", "date"):
        fr["exact"] = exact_in_band(a, v, r)
        if a.kind == "num" and i in item.exact and fr["exact"] == item.exact[i]:
            fr["exact"] = exact_in_band(a, v, r)
    else:
        fr["surf"] = surface_for(card, i, v, r)
    return fr


def allowed_kinds(card, a, *, primary=False):
    ks = list(card.frame_kinds)
    if a.kind == "pres" or (a.kind == "nom" and a.n < 3) or a.kind == "date":
        ks = [k for k in ks if k != "NEG"]
    return ks


def make_frame(card, item, i, v, r, *, kind=None, others=None):
    a = card.attrs[i]
    fr = lure_value(card, item, i, v, r)
    ks = allowed_kinds(card, a)
    if v == item.cell[i]:
        ks = [k for k in ks if k != "NEG"]            # echoes are never negated (R14)
        if getattr(card, "records", False):
            ks = [k for k in ks if k != "OTHER"]      # records: another record's field equal to the focal shows no frame
    if kind is None:
        w = [0.12 if k == "OTHER" else 1.0 for k in ks]
        kind = r.choices(ks, weights=w)[0]
    if kind not in ks:
        return None
    fr["kind"] = kind
    if kind == "OTHER":
        fr["other"] = r.choice(others)
    if kind == "HEDGED":
        fr["hedge"] = r.choice(card.hedges_used)
    return fr


def n_s(tax, attrs, item, gold):
    """N_s(v): codes one stated-attribute neighbour step away, minus gold (R04). Returns {code: [(i, value)]}."""
    cell = tax.resolve_cell(item.cell, item.missing)
    out = {}
    for i, c2 in neighbours_of_cell(attrs, cell, fixed=item.missing):
        k = tax.table[c2]
        if k != gold:
            out.setdefault(k, []).append((i, c2[i]))
    return out


def n_all(tax, attrs, item, gold):
    cell = tax.resolve_cell(item.cell, item.missing)
    out = {}
    for i, c2 in neighbours_of_cell(attrs, cell):
        k = tax.table[c2]
        if k != gold:
            out.setdefault(k, []).append((i, c2[i]))
    return out


def frame_target(tax, item, fr):
    """Assign(v with a := x) for a lure / echo frame (wherever it lands)."""
    cell = list(tax.resolve_cell(item.cell, item.missing))
    cell[fr["attr"]] = fr["value"]
    return tax.table[tuple(cell)]
