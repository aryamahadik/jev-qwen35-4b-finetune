"""Attribute schemas for one F11 card from its pack view (G0 section 2: taxonomy object, glossary, value words)."""
from __future__ import annotations

import datetime as dt
from fractions import Fraction

from common import rng, toks
from names import pseudo_words, overlap_free, name_ok
from tax import Attr, CardInvalid

GENERIC_DATES = ("filing date", "log date", "opening date", "intake date", "booking date")


def _nominal(aid, src, r, nvals, terms_pool):
    vals = list(src["values"])
    r.shuffle(vals)
    vals = vals[:nvals]
    terms = {}
    for i in range(len(vals)):
        k = r.choice((1, 1, 2))
        terms[i] = [terms_pool.pop() for _ in range(k)]
    return Attr(aid, "nom", src["name"], values=vals, terms=terms)


def _numeric(aid, src, r, nbands, terms_pool):
    lo, hi, step = src["lo"], src["hi"], src["step"]
    n_grid = (hi - lo) // step + 1
    if n_grid < nbands * 4:
        raise CardInvalid("numeric range too small")
    for _ in range(100):
        idx = sorted(r.sample(range(3, n_grid - 3), nbands - 1))
        if all(b - a >= 4 for a, b in zip([0] + idx, idx + [n_grid])):
            break
    else:
        raise CardInvalid("no cut draw")
    cuts = [Fraction(lo + i * step) for i in idx]
    return Attr(aid, "num", src["name"], values=None, terms={"attr": [terms_pool.pop()]}, unit=tuple(src["unit"]),
                cuts=cuts, lo=Fraction(lo), hi=Fraction(lo + (n_grid - 1) * step), step=step)


def _presence(aid, src, r, terms_pool):
    terms = list(src["terms"][:1])
    if r.random() < 0.4:
        terms.append(terms_pool.pop())
    return Attr(aid, "pres", src["name"], values=["present", "absent"], terms={"attr": terms})


def _date(aid, name, window, r, nbands, terms_pool):
    a0 = dt.date.fromisoformat(window[0])
    a1 = dt.date.fromisoformat(window[1])
    span = (a1 - a0).days
    if span < 60:
        raise CardInvalid("date window too short")
    idx = sorted(r.sample(range(20, span - 20), nbands - 1))
    if any(b - a < 15 for a, b in zip(idx, idx[1:])):
        raise CardInvalid("date cuts too close")
    cuts = [a0 + dt.timedelta(days=i) for i in idx]
    ev = name.replace(" date", "").strip() or "logging"
    return Attr(aid, "date", name, terms={"attr": [terms_pool.pop()]}, cuts=cuts, lo=a0, hi=a1, event=ev)


_MARKER_TOKENS = None


def _marker_tokens():
    global _MARKER_TOKENS
    if _MARKER_TOKENS is None:
        import lex
        ph = (lex.ATTRIB_ACTIVE + lex.HEDGE_VERBS + lex.HEDGE_ADVERBS + lex.HEDGE_MODALS + lex.PRIOR_MARKERS
              + lex.LATER_MARKERS + lex.HYPO_MARKERS + lex.GENERIC_MARKERS + lex.BANNED_LATER_FINDING
              + lex.BANNED_PREP_ATTRIB + lex.BANNED_HABITUAL + lex.NOT_STATED + lex.ATTACK_MARKERS
              + ("at most", "no more than", "more than", "over", "up to", "between", "after", "by", "until", "since",
                 "through", "within", "only", "exactly", "below", "above", "under", "less", "least", "fewer", "of",
                 "is", "one", "for", "the", "a", "an", "and", "or", "if", "use", "group", "code", "unless", "both",
                 "otherwise", "any", "all", "not", "no", "none", "that", "this", "it", "its"))
        _MARKER_TOKENS = {t for p in ph for t in toks(p)} - {"the", "a", "an", "of"} | {"of", "is"}
    return _MARKER_TOKENS


def _fits(words, cand, banned_tokens) -> bool:
    if set(toks(cand)) & (banned_tokens | _marker_tokens()):
        return False
    return overlap_free(words + [cand])


def make_attrs(view, plan: dict, *key):
    """plan: {'nom': [nvals, ...], 'num': nbands | None, 'pres': bool, 'date': nbands | None}. Returns [Attr].
    Words are taken greedily so that no value word, term or attribute name overlaps another (F11-R5-08)."""
    r = rng("attrs", view["pack_id"], *key)
    banned = {t for s in [view["entity"], view["entities"]] + view["people"] for t in toks(s)}
    for attempt in range(25):
        terms_pool = pseudo_words(40, view["pack_id"], attempt, *key)
        words = []
        try:
            attrs = []
            noms = list(view["nominal"])
            r.shuffle(noms)
            noms.sort(key=lambda x: -len(x["values"]))
            for nv in sorted(plan.get("nom", []), reverse=True):
                got = None
                while noms and got is None:
                    src = noms.pop(0)
                    if not _fits(words, src["name"], banned):
                        # drop entity / marker tokens from the pack's attribute name ("clock part" -> "part")
                        alt = " ".join(t for t in toks(src["name"]) if t not in banned | _marker_tokens())
                        if not alt or not _fits(words, alt, banned):
                            continue
                        src = dict(src, name=alt)
                    vals = list(src["values"])
                    r.shuffle(vals)
                    keep = []
                    for v in vals:
                        if len(keep) < nv and _fits(words + [src["name"]] + keep, v, banned):
                            keep.append(v)
                    if len(keep) >= 3:
                        got = (src["name"], keep)
                if got is None:
                    raise CardInvalid("not enough nominal attributes")
                words += [got[0]] + got[1]
                terms = {}
                for i in range(len(got[1])):
                    terms[i] = [terms_pool.pop() for _ in range(r.choice((1, 1, 2)))]
                    words += terms[i]
                attrs.append(Attr("", "nom", got[0], values=got[1], terms=terms))
            r.shuffle(attrs)
            if plan.get("num"):
                srcs = [q for q in view["numeric"] if _fits(words, q["name"], banned)
                        and not set(toks(" ".join(q["unit"]))) & {t for w in words for t in toks(w)}]
                if not srcs:
                    raise CardInvalid("no numeric attribute")
                a = _numeric("", r.choice(srcs), r, plan["num"], terms_pool)
                words += [a.name] + a.terms["attr"]
                attrs.append(a)
            if plan.get("pres"):
                srcs = [b for b in view["presence"] if _fits(words, b["name"], banned)
                        and all(_fits(words + [b["name"]], t, banned) for t in b["terms"][:1])]
                if not srcs:
                    raise CardInvalid("no presence field")
                a = _presence("", r.choice(srcs), r, terms_pool)
                words += [a.name] + a.terms["attr"]
                attrs.append(a)
            if plan.get("date"):
                dns = ([view["dates"][0]["name"]] if view["dates"] else []) + list(GENERIC_DATES)
                dns = [d for d in dns if _fits(words, d, banned)]
                if not dns:
                    raise CardInvalid("no date attribute")
                a = _date("", dns[0], view["date_window"], r, plan["date"], terms_pool)
                words += [a.name] + a.terms["attr"]
                attrs.append(a)
            for j, a in enumerate(attrs):
                a.aid = f"a{j}"
            check_words(attrs, view)
            return attrs
        except CardInvalid:
            continue
    raise CardInvalid("attribute draw failed")


def value_words(attrs) -> list[str]:
    """Every value word of the card (F11-R3-07): nominal value names and terms, presence terms, numeric and date
    attribute names and terms."""
    out = []
    for a in attrs:
        if a.kind == "nom":
            out += a.values
            for ts in a.terms.values():
                out += ts
        elif a.kind == "pres":
            out += a.terms["attr"]
        else:
            out += [a.name] + a.terms["attr"]
    return out


def check_words(attrs, view):
    vw = value_words(attrs)
    names = [a.name for a in attrs if a.kind in ("nom", "pres")]
    allw = vw + names
    if not overlap_free(allw):
        raise CardInvalid("value words overlap")
    if not all(name_ok(x) for x in allw):
        raise CardInvalid("reserved word in a value word")
    vt = {t for w in vw for t in toks(w)}
    # the entity nouns, people and units never hold a value word token
    for s in [view["entity"], view["entities"]] + view["people"]:
        if set(toks(s)) & vt:
            raise CardInvalid("pack word holds a value word")
    for a in attrs:
        if a.kind == "num":
            if set(toks(" ".join(a.unit))) & vt:
                raise CardInvalid("unit holds a value word")
    return True
