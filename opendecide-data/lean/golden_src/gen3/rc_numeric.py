"""rc_numeric: yn2b F1b numeric claim checks (yn2b/SPEC.md section 5 F1, part F1b).

Input: 1-4 sentences of dated evidence with figures, revisions, "as of" reports, units and a crisp claim. The card
states every rule a reader needs (figures as printed, only the latest revision counts, the base of a percentage
change, the conversion factor, the tolerance of "about", what "as of" means). Labels come from exact rational
arithmetic in `truth()`; nothing else labels a row. 30% of claims sit exactly at the boundary and 30% within one
unit or one percent of it (SPEC). Shortcut solvers (tiers and distractors only): ignore_amendments (use the first
printed figure, ignoring revisions), latest_dated (use the latest report, ignoring the "as of" date),
all_inclusive (strict comparisons read as inclusive), wrong_base (a percentage change measured against the later
figure), unit_blind (no conversion), ignore_tolerance ("about" read as "exactly"), keyword_overlap (yes iff the
claim's number is printed in the evidence).
"""
from __future__ import annotations

import datetime as dt
import re
from fractions import Fraction

import mv_core as mv
from nd_common import ftrim  # noqa: E402  (exact decimal text, reused from golden_src/gen)
from pe_atoms import OPS  # noqa: E402

OPW = {"ge": "at least", "gt": "more than", "le": "at most", "lt": "less than"}
KINDS = ("threshold", "pct", "difference", "unit", "about", "sum")
NB_MODES = ("ignore_amendments", "latest_dated", "all_inclusive", "wrong_base", "unit_blind", "ignore_tolerance")

PACKS_B = {  # subj: the claim subject; after: the words after a figure in the evidence; core: the noun in "N more ..."
    "city_services": dict(subj="the number of pothole repair requests", after="pothole repair requests",
                          core="pothole repair requests", unit=None, rng=(300, 4000), dp=0,
                          sources=("the city dashboard", "the council's monthly bulletin"), ents="the {x} district",
                          conv=None),
    "retail_sales": dict(subj="the online sales total", after="in online sales", core="in online sales", unit="money",
                         rng=(20000, 900000), dp=0, sources=("the company's sales report", "the finance team's update"),
                         ents="the {x} store", conv=("EUR", "USD", Fraction(108, 100), "1 EUR = 1.08 USD")),
    "sports_league": dict(subj="the points scored", after="points scored", core="points", unit=None,
                          rng=(300, 2500), dp=0, sources=("the league table", "the club's season review"),
                          ents="the {x} Rovers", conv=None),
    "freight": dict(subj="the freight handled", after="of freight handled", core="freight handled",
                    unit=("tonne", "tonnes"), rng=(1200, 60000), dp=1,
                    sources=("the port's traffic report", "the harbour board's notice"), ents="the {x} terminal",
                    conv=(("tonne", "tonnes"), ("kilogram", "kilograms"), Fraction(1000),
                          "1 tonne = 1,000 kilograms")),
    "energy_use": dict(subj="the electricity used", after="of electricity used", core="electricity used",
                       unit=("kWh", "kWh"), rng=(5000, 400000), dp=0,
                       sources=("the utility's meter summary", "the site energy log"), ents="the {x} site",
                       conv=(("kWh", "kWh"), ("MJ", "MJ"), Fraction(36, 10), "1 kWh = 3.6 MJ")),
    "school_enrolment": dict(subj="the number of pupils enrolled", after="pupils enrolled", core="pupils enrolled",
                             unit=None, rng=(150, 3000), dp=0,
                             sources=("the school census", "the district's enrolment note"), ents="{x} Primary",
                             conv=None),
    "transit": dict(subj="the number of weekday riders", after="weekday riders", core="weekday riders", unit=None,
                    rng=(2000, 90000), dp=0, sources=("the transit agency's ridership table", "the route survey"),
                    ents="the {x} line", conv=None),
    "library": dict(subj="the number of book loans", after="book loans", core="book loans", unit=None,
                    rng=(800, 40000), dp=0, sources=("the library's annual return", "the branch statistics sheet"),
                    ents="the {x} branch", conv=None),
}


def F(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(str(x))


def num(x, dp: int) -> str:
    return mv.fmt_amount(F(x), dp) if dp else f"{int(F(x)):,}"


def qty(pack: dict, x, unit_override=None, dp=None) -> str:
    """A figure as printed in a claim: bare number (counts), $ (money), or number + unit."""
    u = unit_override if unit_override is not None else pack["unit"]
    dp = pack["dp"] if dp is None else dp
    if u == "money":
        return "$" + num(x, dp)
    if u is None:
        return num(x, dp)
    if isinstance(u, str):
        return f"{num(x, dp)} {u}"
    v = F(x)
    return f"{num(v, dp)} {u[0] if v == 1 else u[1]}"


def ev_qty(pack: dict, x, unit_override=None) -> str:
    """A figure as printed in the evidence: the number, its unit and the words after it."""
    u = unit_override if unit_override is not None else pack["unit"]
    if u == "money":
        return f"${num(x, pack['dp'])} {pack['after']}"
    if isinstance(u, str) and u != "money":
        return f"{num(x, pack['dp'])} {u} {pack['after']}"
    return f"{qty(pack, x, u)} {pack['after']}"


def _dec_places(x: Fraction) -> int:
    for k in range(0, 7):
        if (x * 10 ** k).denominator == 1:
            return k
    raise ValueError(x)


def pct_text(p) -> str:
    return ftrim(F(p), 3) + "%"


# ================================================================================================ evaluation
def value(f: dict, mode: str | None = None) -> Fraction:
    """The figure the claim is about, computed exactly from the facts (mode: a shortcut solver)."""
    def fig(item):
        if item.get("revised") is not None and mode != "ignore_amendments":
            return F(item["revised"])
        return F(item["value"])

    items = f["items"]
    if f["kind"] in ("threshold", "unit", "about"):
        if f.get("asof"):
            dated = sorted(items, key=lambda i: i["date"])
            if mode == "latest_dated":
                x = fig(dated[-1])
            else:
                x = fig([i for i in dated if i["date"] <= f["asof"]][-1])
        else:
            x = fig(items[0])
        if f["kind"] == "unit" and mode != "unit_blind":
            x = x * F(f["factor"])
        return x
    a, b = fig(items[0]), fig(items[1])
    if f["kind"] == "pct":
        base = b if mode == "wrong_base" else a
        return (b - a) / base * 100 * (1 if f["dir"] == "rose" else -1)
    if f["kind"] == "difference":
        return a - b
    if f["kind"] == "sum":
        return a + b
    raise ValueError(f["kind"])


def truth(f: dict, mode: str | None = None) -> bool:
    v = value(f, mode)
    c = F(f["claim"])
    if f["kind"] == "about":
        if mode == "ignore_tolerance":
            return v == c
        return abs(v - c) <= F(f["tol"])
    op = f["op"]
    if mode == "all_inclusive":
        op = {"gt": "ge", "lt": "le"}.get(op, op)
    return OPS[op](v, c)


def decide(f: dict):
    """(gold yes/no, trace) for the claim, or UNDEFINED for a malformed item."""
    try:
        t = truth(f)
    except (IndexError, ZeroDivisionError):
        return mv.UNDEFINED, {}
    return ("yes" if t else "no"), {"value": str(value(f))}


def shortcut_truths(f: dict) -> dict:
    """{mode: truth or None}: None when the solver's misreading changes nothing in the item (it abstains)."""
    v0 = value(f)
    out = {}
    for m in NB_MODES:
        engaged = False
        if m == "ignore_amendments":
            engaged = any(i.get("revised") is not None for i in f["items"]) and value(f, m) != v0
        elif m == "latest_dated":
            engaged = bool(f.get("asof")) and value(f, m) != v0
        elif m == "all_inclusive":
            engaged = f["kind"] != "about" and f["op"] in ("gt", "lt") and value(f) == F(f["claim"])
        elif m == "wrong_base":
            engaged = f["kind"] == "pct"
        elif m == "unit_blind":
            engaged = f["kind"] == "unit"
        elif m == "ignore_tolerance":
            engaged = f["kind"] == "about" and v0 != F(f["claim"])
        t = truth(f, m) if engaged else None
        out[m] = None if t is None or t == truth(f) else t   # a solver that ends where the truth is abstains
    return out


# ================================================================================================ sampling
def _round(x: Fraction, dp: int) -> Fraction:
    q = Fraction(10) ** dp
    return Fraction(round(x * q)) / q


def _rand_fig(rng, pack) -> Fraction:
    lo, hi = pack["rng"]
    x = Fraction(rng.randint(lo * 10 ** pack["dp"], hi * 10 ** pack["dp"]), 10 ** pack["dp"])
    if pack["unit"] == "money":
        x = Fraction(int(x) // 10 * 10)
    return x


def _d(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def sample(rng, pool: mv.NamePool, pack_key: str, plan: dict) -> dict:
    """One proposal: plan = {kind, gold ('yes'/'no'), boundary (None|exact|off1), revised (bool), asof (bool),
    record (None | 'SUPPORTED' | 'NOT SUPPORTED' for judge latents, set by the builder)}."""
    pack = PACKS_B[pack_key]
    kind = plan["kind"]
    gold = plan["gold"] == "yes"
    bnd = plan.get("boundary")
    dp = pack["dp"]
    unit_step = Fraction(1, 10 ** dp)
    base_day = dt.date(2026, rng.randint(1, 10), rng.randint(1, 28))
    src = rng.choice(pack["sources"])
    f = {"pack": pack_key, "kind": kind, "items": [], "source": src, "op": None, "claim": None, "tol": None,
         "factor": None, "asof": None, "dir": None, "ents": None, "record": None, "dp": dp, "cdp": dp}
    if kind == "unit" and not pack["conv"]:
        raise mv.Reject("unit", "pack without a conversion")
    # ---- figures
    if kind in ("threshold", "unit", "about"):
        if plan.get("asof"):
            n = 3
            days = sorted(rng.sample(range(0, 80), n))
            for d in days:
                f["items"].append({"value": str(_rand_fig(rng, pack)), "date": (base_day + dt.timedelta(days=d))
                                   .isoformat(), "revised": None})
            k = rng.randint(0, 1)
            lo = _d(f["items"][k]["date"])
            hi = _d(f["items"][k + 1]["date"])
            f["asof"] = (lo + dt.timedelta(days=rng.randint(0, max(0, (hi - lo).days - 1)))).isoformat()
        else:
            f["items"].append({"value": str(_rand_fig(rng, pack)), "date": base_day.isoformat(), "revised": None})
    elif kind == "pct":
        a = _rand_fig(rng, pack)
        p = Fraction(rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25]))
        f["dir"] = rng.choice(["rose", "fell"])
        sgn = 1 if f["dir"] == "rose" else -1
        b = _round(a * (1 + sgn * p / 100 + Fraction(rng.randint(-40, 40), 1000)), dp)
        if (b > a) != (sgn > 0) or b == a:
            b = _round(a * (1 + sgn * p / 100), dp)
        f["items"] = [{"value": str(a), "date": base_day.isoformat(), "revised": None, "period": "first"},
                      {"value": str(b), "date": (base_day + dt.timedelta(days=rng.randint(28, 120))).isoformat(),
                       "revised": None, "period": "second"}]
    else:
        e1, e2 = pool.stem(rng), pool.stem(rng)
        while e2 == e1:
            e2 = pool.stem(rng)
        f["ents"] = [pack["ents"].format(x=e1), pack["ents"].format(x=e2)]
        f["ent_stems"] = [e1, e2]
        a, b = _rand_fig(rng, pack), _rand_fig(rng, pack)
        if kind == "difference" and a <= b:
            a, b = b, a
            if a == b:
                a += unit_step * 7
        f["items"] = [{"value": str(a), "date": base_day.isoformat(), "revised": None},
                      {"value": str(b), "date": base_day.isoformat(), "revised": None}]
    if kind == "unit":
        f["factor"] = str(pack["conv"][2])
    # ---- a revision of one figure (printed later, it replaces the earlier figure)
    if plan.get("revised"):
        cands = [i for i in f["items"]]
        it = rng.choice(cands) if not f.get("asof") else rng.choice([i for i in f["items"] if i["date"] <= f["asof"]])
        old = F(it["value"])
        new = _round(old * (1 + Fraction(rng.choice([-1, 1]) * rng.randint(1, 9), 100)), dp)
        if new == old:
            new = old + unit_step * 3
        it["revised"] = str(new)
        rd = _d(it["date"]) + dt.timedelta(days=rng.randint(2, 20))
        if f.get("asof") and rd.isoformat() > f["asof"]:
            rd = _d(f["asof"])
        it["revised_date"] = rd.isoformat()
    # ---- the claim
    V = value(f)
    if kind == "about":
        tol = {0: Fraction(rng.choice([5, 10, 20, 50])), 1: Fraction(rng.choice([5, 10, 20]), 10)}[min(dp, 1)]
        if pack["unit"] == "money":
            tol = Fraction(rng.choice([100, 500, 1000]))
        f["tol"] = str(tol)
        if bnd == "exact":
            off = tol
        elif bnd == "off1":
            off = tol + unit_step
        else:
            off = tol * Fraction(rng.randint(2, 30), 10) if not gold else tol * Fraction(rng.randint(0, 9), 10)
        if bnd in ("exact", "off1") and gold != (off <= tol):
            raise mv.Reject("about", "boundary does not give the planned gold")
        c = V + off * rng.choice([-1, 1])
        f["claim"] = str(_round(c, dp))
        if (abs(V - F(f["claim"])) <= tol) != gold:
            raise mv.Reject("about", "rounding moved the claim")
        f["op"] = "about"
        return f
    cdp = dp + (_dec_places(F(f["factor"])) if kind == "unit" else 0)
    f["cdp"] = cdp
    unit_step = Fraction(1, 10 ** cdp)
    step = Fraction(1) if kind == "pct" else unit_step
    if kind == "pct":
        if V <= 0:      # R2 (1 Oct): a revision reversed the change; 'fell by at most P%' of a rise is two readings
            raise mv.Reject("pct", "the change runs against the claimed direction")
        if bnd == "exact" and V.denominator != 1 and (V * 100).denominator != 1:
            raise mv.Reject("pct", "not an exact percentage")
    if bnd == "exact":
        c = V
        op = rng.choice(["ge", "le"]) if gold else rng.choice(["gt", "lt"])
    else:
        if bnd == "off1":
            delta = step if kind != "pct" else Fraction(1)
        else:
            mag = abs(V) if V != 0 else Fraction(100)
            delta = _round(mag * Fraction(rng.randint(3, 25), 100), cdp if kind != "pct" else 1) or step
        side = rng.choice([-1, 1])
        c = V + side * delta
        # with c below V: V >= c and V > c are true; with c above: V <= c, V < c true
        if side < 0:
            op = rng.choice(["ge", "gt"]) if gold else rng.choice(["le", "lt"])
        else:
            op = rng.choice(["le", "lt"]) if gold else rng.choice(["ge", "gt"])
    if kind == "pct":
        if c <= 0:
            raise mv.Reject("pct", "non-positive claimed change")
        c = _round(c, 1)
    else:
        c = _round(c, cdp)
        if c <= 0:
            raise mv.Reject("claim", "non-positive claim")
    f["claim"] = str(c)
    f["op"] = op
    if truth(f) != gold:
        raise mv.Reject("claim", "rounding changed the planned gold")
    return f


# ================================================================================================ rendering
CARD_RULES = {
    "figures": "Figures are used exactly as printed; nothing is rounded.",
    "revisions": "When a figure is revised, only the most recent revision of it counts.",
    "percent change": "A percentage change is measured against the earlier of the two figures.",
    "as of": "A figure as of a date is the latest figure reported on or before that date.",
}


def card_defs(f: dict, judge: bool, inverted: bool = False) -> dict:
    d = {"figures": CARD_RULES["figures"]}
    if any(i.get("revised") is not None for i in f["items"]):
        d["revisions"] = CARD_RULES["revisions"]
    if f["kind"] == "pct":
        d["percent change"] = CARD_RULES["percent change"]
    if f.get("asof"):
        d["as of"] = CARD_RULES["as of"]
    if f["kind"] == "unit":
        d["conversion"] = f"For this check, {PACKS_B[f['pack']]['conv'][3]}."
    if f["kind"] == "about":
        p = PACKS_B[f["pack"]]
        d["about"] = (f"\"About N\" means within {qty(p, f['tol'])} of N, counting both ends.")
    if judge:
        d["yes"] = "The fact-check log entry matches what the evidence establishes under these rules."
        d["no"] = "The fact-check log entry does not match what the evidence establishes under these rules."
    elif inverted:
        d["yes"] = "Under these rules the evidence does not establish the claim."
        d["no"] = "Under these rules the evidence establishes the claim."
    else:
        d["yes"] = "Under these rules the evidence establishes the claim."
        d["no"] = "Under these rules the evidence does not establish the claim."
    return d


def _fd(s: str, st: str) -> str:
    d = _d(s)
    months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December")
    if st == "iso":
        return s
    if st == "long":
        return f"{d.day} {months[d.month - 1]} {d.year}"
    return f"{months[d.month - 1]} {d.day}, {d.year}"


def evidence_lines(f: dict, dstyle: str) -> list[tuple[str, str]]:
    """[(date, sentence)] of the evidence (each sentence states one dated figure or one revision)."""
    p = PACKS_B[f["pack"]]
    src = f["source"]
    out = []
    unit = p["conv"][0] if f["kind"] == "unit" else None
    for i, it in enumerate(f["items"]):
        d = _fd(it["date"], dstyle)
        q = ev_qty(p, it["value"], unit)
        if f["kind"] == "pct":
            s = f"As of {d}, {src} reported {q} for the {'first' if i == 0 else 'second'} period."
        elif f["kind"] in ("difference", "sum"):
            s = f"As of {d}, {src} reported {q} for {f['ents'][i]}."
        else:
            s = f"As of {d}, {src} reported {q}."
        out.append((it["date"], s))
        if it.get("revised") is not None:
            rd = _fd(it["revised_date"], dstyle)
            out.append((it["revised_date"], f"On {rd}, {src} revised that figure from {qty(p, it['value'], unit)} "
                                            f"to {qty(p, it['revised'], unit)}."))
    return out


def _cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def claim_text(f: dict, dstyle: str) -> str:
    p = PACKS_B[f["pack"]]
    subj = p["subj"]
    cdp = f.get("cdp")
    if f["kind"] == "about":
        when = f" as of {_fd(f['asof'], dstyle)}" if f.get("asof") else ""
        return f"{_cap(subj)}{when} was about {qty(p, f['claim'])}."
    if f["kind"] == "pct":
        return f"{_cap(subj)} {f['dir']} by {OPW[f['op']]} {pct_text(f['claim'])} from the first period to the " \
               f"second period."
    if f["kind"] == "difference":
        return f"{_cap(f['ents'][0])} had {OPW[f['op']]} {qty(p, f['claim'])} more {p['core']} than {f['ents'][1]}."
    if f["kind"] == "sum":
        return f"Taken together, {f['ents'][0]} and {f['ents'][1]} had {OPW[f['op']]} {qty(p, f['claim'])} " \
               f"{p['after']}."
    unit = p["conv"][1] if f["kind"] == "unit" else None
    when = f" as of {_fd(f['asof'], dstyle)}" if f.get("asof") else ""
    return f"{_cap(subj)}{when} was {OPW[f['op']]} {qty(p, f['claim'], unit, cdp)}."


def render_state(f: dict, fmt: str, dstyle: str, plant: dict | None = None, perm_seed=None) -> str:
    ev = evidence_lines(f, dstyle)
    cl = claim_text(f, dstyle)
    rec = f.get("record")
    base, _, var = fmt.partition(":")
    if base == "json":
        obj = {"evidence": [s for _, s in ev], "claim": cl, "fact_check_log": rec,
               "notes": ([{"from": plant["sender"], "text": plant["text"]}] if plant else [])}
        return mv.render_json(obj)
    if base == "markdown":
        secs = [("Evidence", [s for _, s in ev]), ("Claim", cl)]
        if rec:
            secs.append(("Fact-check log", f"Entry for this claim: {rec}"))
        if plant:
            secs.append(("Notes", [f"From {plant['sender']}: {plant['text']}"]))
        return mv.render_markdown(secs)
    if base == "kv":
        obj = {"evidence": [s for _, s in ev], "claim": cl}
        if rec:
            obj["fact_check_log"] = rec
        out = mv.render_kv(obj)
    elif base == "prose":
        out = " ".join(s for _, s in ev) + "\n\nClaim: " + cl + (f"\n\nFact-check log entry: {rec}" if rec else "")
    elif base == "log":
        import random as _r
        ents = []
        used = set()
        for d, s in ev:
            t = dt.datetime.fromisoformat(d).replace(hour=9, tzinfo=dt.timezone.utc)
            while t in used:
                t += dt.timedelta(minutes=7)
            used.add(t)
            ents.append(mv.Entry(t, "report", s))
        out = "Evidence log\n" + mv.render_log(ents, var or "chrono", _r.Random(perm_seed), "iso") + \
            "\n\nClaim: " + cl + (f"\n\nFact-check log entry: {rec}" if rec else "")
    else:
        raise ValueError(fmt)
    if plant:
        out += f"\n\nNote added by {plant['sender']}: {plant['text']}"
    return out


FMTS_B = ("json", "markdown", "kv", "prose", "log")


# ================================================================================================ parse-back
_MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
           "November", "December")
_DATE = (r"(?:\d{4}-\d{2}-\d{2}|\d{1,2} (?:" + "|".join(_MONTHS) + r") \d{4}|(?:" + "|".join(_MONTHS) +
         r") \d{1,2}, \d{4})")
_NUM = r"\$?([\d,]+(?:\.\d+)?)"
_OPS = {v: k for k, v in OPW.items()}


def _pd(s: str) -> str:
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    m = re.fullmatch(r"(\d{1,2}) (\w+) (\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), _MONTHS.index(m.group(2)) + 1, int(m.group(1))).isoformat()
    m = re.fullmatch(r"(\w+) (\d{1,2}), (\d{4})", s)
    return dt.date(int(m.group(3)), _MONTHS.index(m.group(1)) + 1, int(m.group(2))).isoformat()


def _n(s: str) -> str:
    return str(Fraction(s.replace(",", "")))


def parse_state(state: str, fmt: str, pack_key: str, defs: dict) -> dict:
    """This builder's parse-back of an F1b state (+ its card definitions) into facts (a self-check of the
    renderers; the independent decide2 is agent E's)."""
    import json as _json
    p = PACKS_B[pack_key]
    base = fmt.split(":")[0]
    rec = None
    if base == "json":
        o = _json.loads(state)
        ev, cl, rec = o["evidence"], o["claim"], o["fact_check_log"]
    elif base == "markdown":
        secs = dict(mv.parse_markdown(state))
        ev = [x[2:] for x in secs["Evidence"].split("\n")]
        cl = secs["Claim"]
        if "Fact-check log" in secs:
            rec = secs["Fact-check log"].split(": ", 1)[1]
    elif base == "kv":
        kv = mv.parse_kv(state.split("\n\nNote added by ")[0])
        ev = [v for k, v in sorted(kv.items(), key=lambda kv_: int(kv_[0].split(".")[1]) if kv_[0].startswith(
            "evidence.") else 0) if k.startswith("evidence.")]
        cl = kv["claim"]
        rec = kv.get("fact_check_log")
    else:
        body = state.split("\n\nNote added by ")[0]
        m = re.search(r"\n\nClaim: (.+?)(?:\n\nFact-check log entry: (.+))?$", body, re.S)
        cl, rec = m.group(1), m.group(2)
        head = body[:m.start()]
        if base == "log":
            ev = [e.text for e in sorted(mv.parse_log(head), key=lambda e: e.ts)]
        else:
            ev = re.findall(r"(?:As of|On) .+?\.(?= As of | On |$)", head)
    f = {"pack": pack_key, "items": [], "record": rec, "asof": None, "tol": None, "factor": None, "dir": None,
         "ents": None, "dp": p["dp"]}
    ents = []
    for s in ev:
        m = re.fullmatch(r"On (" + _DATE + r"), .+? revised that figure from " + _NUM + r"(?: \S+)? to " + _NUM +
                         r"(?: \S+)?\.", s)
        if m:
            old = _n(m.group(2))
            it = next(i for i in reversed(f["items"]) if i["value"] == old)
            it["revised"] = _n(m.group(3))
            it["revised_date"] = _pd(m.group(1))
            continue
        m = re.fullmatch(r"As of (" + _DATE + r"), .+? reported " + _NUM + r"(.*?)(?: for (the first period|the "
                         r"second period|.+))?\.", s)
        it = {"value": _n(m.group(2)), "date": _pd(m.group(1)), "revised": None}
        who = m.group(4)
        if who and who not in ("the first period", "the second period"):
            ents.append(who)
        f["items"].append(it)
    if ents:
        f["ents"] = ents
    if "conversion" in defs:
        f["kind"] = "unit"
        f["factor"] = str(p["conv"][2])
    if "about" in defs:
        f["kind"] = "about"
        m = re.search(r"within " + _NUM, defs["about"])
        f["tol"] = _n(m.group(1))
        m = re.search(r"about " + _NUM, cl)
        f["claim"], f["op"] = _n(m.group(1)), "about"
        m = re.search(r" as of (" + _DATE + r") was about", cl)
        if m:
            f["asof"] = _pd(m.group(1))
    elif (m := re.fullmatch(r".+ (rose|fell) by (at least|more than|at most|less than) ([\d.]+)% from the first "
                            r"period to the second period\.", cl)):
        f.update(kind="pct", dir=m.group(1), op=_OPS[m.group(2)], claim=_n(m.group(3)))
    elif (m := re.fullmatch(r".+ had (at least|more than|at most|less than) " + _NUM + r".* more .+ than .+\.", cl)):
        f.update(kind="difference", op=_OPS[m.group(1)], claim=_n(m.group(2)))
    elif (m := re.fullmatch(r"Taken together, .+ had (at least|more than|at most|less than) " + _NUM + r".*\.", cl)):
        f.update(kind="sum", op=_OPS[m.group(1)], claim=_n(m.group(2)))
    else:
        m = re.fullmatch(r".+?(?: as of (" + _DATE + r"))? was (at least|more than|at most|less than) " + _NUM +
                         r".*\.", cl)
        f.update(op=_OPS[m.group(2)], claim=_n(m.group(3)))
        if m.group(1):
            f["asof"] = _pd(m.group(1))
        f.setdefault("kind", "threshold")
    return f
