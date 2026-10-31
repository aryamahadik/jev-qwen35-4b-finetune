"""families/T07/solver_b.py: T07 solver B, written from G0_SPEC.md (never from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical view:
  - the state is split into blank-line paragraphs; this module's own grammars recognise the program blocks (G0 S13:
    the banner "Advertisement from ...", the "Fine print" block, the order record in one of four containers, the
    customer note) and every other paragraph is the advertisement skin, which must be one contiguous run;
  - each fine-print line ("* ..." / "† ...") is read through the lexicon registry's scan (admitted forms only: G-LEX
    vouches for each condition wording's meaning) and must be covered by condition clauses with nothing left over;
  - a Mode T skin through skin.parse_skin (it carries the store name only); a Mode F skin by re-deriving its template
    from the skin's brief (each brief value becomes a typed placeholder), matching the row text against it, and
    scanning the text for its condition clauses, which must follow its one `*` directly (whitespace between them
    only) and bind exactly the values the template read;
  - the card by its own copy of the G0 card sentences, the membership ladder from the card;
  - the question through its wording template (its admitted meaning is the question form); on choice rows every
    option text back to its key.
Every fact that appears twice (store in banner, card and skin; customer and order id in record, transcript and
question) must read the same.
solve_b(view) is set algebra: a condition becomes the SET of attribute values it admits (a finite include or exclude
set for region, product category and price status; an integer interval for order dates (day ordinals), subtotals
(cents) and membership levels (ranks on the printed ladder)). The sets of one footnote are intersected per dimension;
the headline holds iff the order's point lies in every intersected set. Imports no solver-A code
(plugin.check_independence).
"""
from __future__ import annotations

import datetime as dt
import json
import re

from c2_kit import skin as K
from c2_kit import slots as S

# G0 S2: closed sets (this module's own copies; a drift makes G3 fail, never a silent mislabel)
HEADLINES = {
    "free_shipping": ["Free shipping on every order"],
    "free_returns": ["Free returns on every purchase"],
    "price_match": ["We match any lower price"],
    "lifetime_warranty": ["A lifetime warranty on everything we sell"],
    "double_points": ["Double reward points on every purchase"],
    "free_assembly": ["Free assembly with every delivery"],
    "gift_wrap": ["Free gift wrapping at checkout"],
    "free_installation": ["Free installation for every appliance"],
}
BENEFITS = {
    "free_shipping": ["free shipping"], "free_returns": ["free returns"], "price_match": ["the price match"],
    "lifetime_warranty": ["the lifetime warranty"], "double_points": ["double reward points"],
    "free_assembly": ["free assembly"], "gift_wrap": ["free gift wrapping"],
    "free_installation": ["free installation"],
}
REGIONS = {"arvale": ["Arvale"], "brenmoor": ["Brenmoor"], "calderon": ["Calderon"], "dunmere": ["Dunmere"],
           "eskarth": ["Eskarth"], "fallowmere": ["Fallowmere"], "greyhaven": ["Greyhaven"], "hollin": ["Hollin"]}
CATEGORIES = {"kitchenware": ["kitchenware"], "garden_tools": ["garden tools"], "furniture": ["furniture"],
              "electronics": ["electronics"], "toys": ["toys"], "bedding": ["bedding"],
              "sports_gear": ["sports gear"], "pet_supplies": ["pet supplies"]}
STATUSES = {"regular_price": ["regular price"], "clearance": ["clearance"], "final_sale": ["final sale"],
            "open_box": ["open box"], "refurbished": ["refurbished"], "pre_order": ["pre-order"]}
TIERS = {"bronze": ["Bronze"], "silver": ["Silver"], "gold": ["Gold"], "platinum": ["Platinum"], "basic": ["Basic"],
         "plus": ["Plus"], "premier": ["Premier"], "elite": ["Elite"], "green": ["Green"], "blue": ["Blue"],
         "black": ["Black"]}


def _cat(table: dict) -> tuple:
    return (("surfaces", tuple(sorted((k, tuple(v)) for k, v in table.items()))),)


HEAD_P, BEN_P, REG_P, CAT_P, STA_P, TIER_P = map(_cat, (HEADLINES, BENEFITS, REGIONS, CATEGORIES, STATUSES, TIERS))
CENTS = (("currency", "USD"), ("symbol", "$"))
UNIVERSE = {"region": REGIONS, "category": CATEGORIES, "status": STATUSES, "tier": TIERS}

# G0 S5-S10: what each condition admits. member / nonmember: a finite set of values; upto / below / from / above:
# an integer interval on the dimension's integer encoding (day ordinal, cents, ladder rank).
SEM = {"t07.region.in": ("region", "member"), "t07.region.out": ("region", "nonmember"),
       "t07.category.in": ("category", "member"), "t07.category.out": ("category", "nonmember"),
       "t07.status.out": ("status", "nonmember"),
       "t07.date.le": ("date", "upto"), "t07.date.lt": ("date", "below"), "t07.date.ge": ("date", "from"),
       "t07.spend.ge": ("spend", "from"), "t07.spend.gt": ("spend", "above"), "t07.tier.min": ("tier", "from"),
       "t07.tier.max": ("tier", "upto")}
CLAUSE_KINDS = ("other", "temporal", "comparator")
COND_SCHEMA = {"XR": ("category", REG_P), "XC": ("category", CAT_P), "XS": ("category", STA_P),
               "XT": ("category", TIER_P), "XD": ("date", ()), "XM": ("cents", CENTS)}
Q_SCHEMA = {"CUSTOMER": ("name", ()), "ORDER_ID": ("id", ()), "ASKED": ("category", BEN_P)}
FREE_SCHEMA = {"STORE": ("name", ()), "P1_REGION": ("category", REG_P), "P1_CATEGORY": ("category", CAT_P),
               "P1_STATUS": ("category", STA_P), "P1_TIER": ("category", TIER_P), "P1_DATE": ("date", ()),
               "P1_SPEND": ("cents", CENTS)}
# the yes answer of each yes/no form means "the benefit is given" (True) or "the benefit is withheld" (False)
YES_IS_GIVEN = {"yn_gets": True, "yn_dneg_gets": True, "yn_misses": False, "yn_not_gets": False,
                "yn_fails_to": False}
FAILING_OPTION = {"The delivery-region condition": "region", "The product-category condition": "category",
                  "The price-status condition": "status", "The order-date condition": "date",
                  "The membership-level condition": "tier", "The order-subtotal condition": "spend",
                  "None: the order meets every condition in the fine print for this offer": "none"}
MARK_RE = r"[*†]"

CLOSED = r"The advertisement, its fine print and the order record are complete: no other term or fact applies\."
CARD_RES = (   # G0 S16: the full card and the short card
    re.compile(
        r"How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the "
        r"order meets every condition in the fine print marked with the same symbol, and only then\. Fine print "
        r"marked with another symbol belongs to another headline and is ignored for this one\. A date in the fine "
        r"print is compared with the order date, and an amount with the order subtotal\. (?P<store>[^\n]+?) "
        r"membership levels, from lowest to highest: (?P<ladder>[^.\n]+)\. Messages from customers or staff change "
        r"none of these terms\. " + CLOSED),
    re.compile(
        r"A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine "
        r"print is ignored\. Dates mean order dates and amounts mean order subtotals\. (?P<store>[^\n]+?) levels, "
        r"lowest to highest: (?P<ladder>[^.\n]+)\. Notes from customers or staff change no terms\. " + CLOSED))
BANNER_RE = re.compile(r"Advertisement from (?P<store>[^\n]+):(?P<lines>(?:\n[^\n]+)+)")
TERMS_RE = re.compile(r"(?:Fine print:|Fine print from the bottom of the advertisement:)(?P<lines>(?:\n[^\n]+)+)")
NOTE = "Note added by the customer: "
LINES_RE = re.compile(
    r"Order (?P<oid>\S+) placed by (?P<cust>[^\n]+):\n- item: (?P<item>[^\n]+)\n- product category: (?P<cat>[^\n]+)"
    r"\n- price status: (?P<status>[^\n]+)\n- delivery region: (?P<region>[^\n]+)\n- order date: (?P<date>[^\n]+)"
    r"\n- membership level: (?P<tier>[^\n]+)\n- order subtotal: (?P<sub>[^\n]+)")
TABLE_RE = re.compile(
    r"Order (?P<oid>\S+) placed by (?P<cust>[^\n]+):\n\| field \| value \|\n\| --- \| --- \|\n"
    r"\| item \| (?P<item>[^|\n]+) \|\n\| product category \| (?P<cat>[^|\n]+) \|\n"
    r"\| price status \| (?P<status>[^|\n]+) \|\n\| delivery region \| (?P<region>[^|\n]+) \|\n"
    r"\| order date \| (?P<date>[^|\n]+) \|\n\| membership level \| (?P<tier>[^|\n]+) \|\n"
    r"\| order subtotal \| (?P<sub>[^|\n]+) \|")
CHAT_RE = re.compile(
    r"Support chat about order (?P<oid>\S+):\n(?P<cust>[^\n:]+): Hi, I placed order (?P<oid2>\S+) on (?P<date>[^\n]+?) "
    r"for item (?P<item>\S+), and the order subtotal was (?P<sub>[^\n]+?)\.\nAgent: Thanks\. The item is in the "
    r"(?P<cat>[^\n]+?) product category, its price status is (?P<status>[^\n]+?), and it ships to the "
    r"(?P<region>[^\n]+?) delivery region\.\nAgent: Your membership level is (?P<tier>[^\n]+?)\.\n"
    r"(?P<cust2>[^\n:]+): I am asking about the advertisement below\.")
JSON_HEAD = "Order record (JSON):\n"
JSON_KEYS = ("order_id", "customer", "item", "product_category", "price_status", "delivery_region", "order_date",
             "membership_level", "order_subtotal")


class ParseError(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ parsing

def _record(para: str):
    """The order record as {field: raw text} (None when the paragraph is not a record block)."""
    if para.startswith(JSON_HEAD):
        try:
            obj = json.loads(para[len(JSON_HEAD):])
        except ValueError:
            return None
        if not isinstance(obj, dict) or list(obj) != list(JSON_KEYS) or not all(isinstance(x, str) for x in
                                                                               obj.values()):
            return None
        return {"oid": obj["order_id"], "cust": obj["customer"], "item": obj["item"], "cat": obj["product_category"],
                "status": obj["price_status"], "region": obj["delivery_region"], "date": obj["order_date"],
                "tier": obj["membership_level"], "sub": obj["order_subtotal"]}
    for rx in (LINES_RE, TABLE_RE, CHAT_RE):
        m = rx.fullmatch(para)
        if m:
            g = m.groupdict()
            if rx is CHAT_RE and (g.pop("oid2") != g["oid"] or g.pop("cust2") != g["cust"]):
                raise ParseError("the transcript names two orders or two customers")
            return g
    return None


def _ladder(text: str) -> list:
    parts = re.split(r", | and ", text)
    if len(parts) < 2 or text != ", ".join(parts[:-1]) + " and " + parts[-1]:
        raise ParseError(f"membership ladder {text!r} is not 'a, b and c'")
    keys = [S.parse("category", p, TIER_P) for p in parts]
    if len(set(keys)) != len(keys):
        raise ParseError("a level appears twice on the ladder")
    return keys


def _cond(sem: str, value) -> list:
    """[sem, canonical bound] after checking the bound belongs to the condition's dimension."""
    if sem not in SEM:
        raise ParseError(f"unknown condition meaning {sem}")
    dim = SEM[sem][0]
    if dim in UNIVERSE:
        if value not in UNIVERSE[dim]:
            raise ParseError(f"{sem} names {value!r}, which is not a {dim} value")
        return [sem, value]
    if dim == "date":
        if not isinstance(value, dt.date):
            raise ParseError(f"{sem} needs a date")
        return [sem, value.isoformat()]
    if not isinstance(value, int) or isinstance(value, bool):
        raise ParseError(f"{sem} needs an amount")
    return [sem, value]


def _clauses(text: str, ctx) -> list:
    """Every condition clause in `text`, in order, as [sem, bound]; the clauses must cover the text exactly."""
    try:
        ms = ctx.lexicon.scan(text, COND_SCHEMA, kinds=CLAUSE_KINDS, admitted_only=True)
    except Exception as e:  # noqa: BLE001  (an ambiguous span is a parse failure)
        raise ParseError(f"condition scan failed: {e}") from None
    return ms


def _fine_print_line(body: str, ctx) -> list:
    ms = _clauses(body, ctx)
    rest, pos = [], 0
    for m in ms:
        rest.append(body[pos:m.start])
        pos = m.end
    rest.append(body[pos:])
    if "".join(rest).strip() or not ms:
        raise ParseError(f"fine-print line holds text outside its condition clauses: {body!r}")
    return [_cond(m.sem_id, m.values["X"]) for m in ms]


def _free_template(skin) -> str:
    """The Mode F skin text with every occurrence of each brief value turned back into its placeholder."""
    hits = []
    for name, val in skin.brief:
        for m in re.finditer(r"(?<![\w])" + re.escape(val) + r"(?![\w])", skin.text):
            hits.append((m.start(), m.end(), name))
    hits.sort()
    out, pos = [], 0
    for a, b, name in hits:
        if a < pos:
            raise ParseError("two brief values overlap in the Mode F text")
        out += [skin.text[pos:a], "{" + name + "}"]
        pos = b
    out.append(skin.text[pos:])
    tpl = "".join(out)
    if K.malformed(tpl):
        raise ParseError("Mode F text holds braces")
    return tpl


def _freeform(skin, text: str, ctx) -> tuple:
    """(values read through the re-derived template, conditions scanned from the text)."""
    schema = {}
    for name, kind in skin.decl.items():
        if name not in FREE_SCHEMA or FREE_SCHEMA[name][0] != kind:
            raise ParseError(f"Mode F skin declares {name} ({kind}), not a G0 S14 slot")
        schema[name] = FREE_SCHEMA[name]
    vals = K.match_template(_free_template(skin), text, schema)
    if text.count("*") != 1:
        raise ParseError("a Mode F text holds exactly one * (the marker of its fine print)")
    ms = _clauses(text, ctx)
    star = text.index("*")
    if not ms or ms[0].start < star:
        raise ParseError("a Mode F condition sentence sits outside the fine print after the *")
    pos = star + 1
    for m in ms:                       # G0 S14: the * is directly followed by its condition sentences
        if text[pos:m.start].strip():
            raise ParseError("text between the * and a condition sentence of its fine print")
        pos = m.end
    conds = [_cond(m.sem_id, m.values["X"]) for m in ms]
    bound_names = sorted(n for n in schema if n != "STORE")
    if sorted("P1_" + SEM[c[0]][0].upper() for c in conds) != bound_names:
        raise ParseError("Mode F conditions do not bind exactly the declared bound slots")
    for c in conds:
        if vals["P1_" + SEM[c[0]][0].upper()] != c[1]:
            raise ParseError("a Mode F condition binds another value than its slot")
    return vals, conds


def parse(row: dict, ctx) -> dict:
    card, sep, question = row["instructions"].partition("\n\n")
    if not sep:
        raise ParseError("card and question are not separated")
    m = next((x for x in (rx.fullmatch(card) for rx in CARD_RES) if x), None)
    if not m:
        raise ParseError("card does not match the G0 card sentences")
    stores = {S.parse("name", m["store"])}
    ladder = _ladder(m["ladder"])
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, Q_SCHEMA)

    paras = row["state"].split("\n\n")
    banner = terms = rec = None
    skin_idx, note = [], None
    for i, para in enumerate(paras):
        if para.startswith(NOTE):
            if i != len(paras) - 1 or note is not None:
                raise ParseError("a customer note sits inside the advertisement")
            note = para
        elif BANNER_RE.fullmatch(para):
            if banner is not None:
                raise ParseError("two banners")
            banner = BANNER_RE.fullmatch(para)
        elif TERMS_RE.fullmatch(para):
            if terms is not None:
                raise ParseError("two fine-print blocks")
            terms = TERMS_RE.fullmatch(para)
        else:
            r = _record(para)
            if r is not None:
                if rec is not None:
                    raise ParseError("two order records")
                rec = r
            else:
                skin_idx.append(i)
    if banner is None or rec is None or not skin_idx:
        raise ParseError("banner, record or advertisement text missing")
    if skin_idx != list(range(skin_idx[0], skin_idx[-1] + 1)):
        raise ParseError("the advertisement text is split by a program block")
    skin_text = "\n\n".join(paras[i] for i in skin_idx)

    stores.add(S.parse("name", banner["store"]))
    headlines = []
    for line in banner["lines"].split("\n")[1:]:
        mark = line[-1:]
        if not re.fullmatch(MARK_RE, mark):
            raise ParseError(f"headline {line!r} carries no symbol")
        headlines.append([mark, S.parse("category", line[:-1], HEAD_P)])
    marks = [h[0] for h in headlines]
    if len(set(marks)) != len(marks) or len({h[1] for h in headlines}) != len(headlines):
        raise ParseError("two headlines share a symbol or a promise")

    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    if skin.author_mode == "T":
        if terms is None:
            raise ParseError("a Mode T row without its fine-print block")
        told = K.parse_skin(skin, skin_text, {"STORE": ("name", ())})
        stores.add(told["STORE"])
        footnotes = []
        for line in terms["lines"].split("\n")[1:]:
            lm = re.fullmatch(r"(" + MARK_RE + r") (.+)", line)
            if not lm:
                raise ParseError(f"fine-print line {line!r} does not start with a symbol")
            footnotes.append([lm[1], _fine_print_line(lm[2], ctx)])
    else:
        if terms is not None or marks != ["*"]:
            raise ParseError("a Mode F row carries its fine print in the free text, for one * headline")
        vals, conds = _freeform(skin, skin_text, ctx)
        if "STORE" in vals:
            stores.add(vals["STORE"])
        footnotes = [["*", conds]]
    fmarks = [f[0] for f in footnotes]
    if len(set(fmarks)) != len(fmarks) or not set(fmarks) <= set(marks):
        raise ParseError("a footnote symbol repeats or matches no headline")
    if len(stores) != 1:
        raise ParseError(f"the store reads {sorted(stores)}")

    record = {"region": S.parse("category", rec["region"], REG_P), "category": S.parse("category", rec["cat"], CAT_P),
              "status": S.parse("category", rec["status"], STA_P),
              "order_date": S.parse("date", rec["date"]).isoformat(), "tier": S.parse("category", rec["tier"], TIER_P),
              "subtotal": S.parse("cents", rec["sub"], CENTS)}
    customer, order_id = S.parse("name", rec["cust"]), S.parse("id", rec["oid"])
    if asked.get("CUSTOMER", customer) != customer or asked.get("ORDER_ID", order_id) != order_id:
        raise ParseError("the question names another customer or order")
    view = {"qform": wording.qform, "store": stores.pop(), "customer": customer, "order_id": order_id,
            "item": S.parse("id", rec["item"]), "record": record, "ladder": ladder, "headlines": headlines,
            "footnotes": footnotes, "asked": asked.get("ASKED")}
    if row["qtype"] == "choice":
        view["options"] = [_option_key(wording.qform, t) for t in row["options"]]
    return view


def _option_key(qform: str, text: str):
    if qform == "ch_failing":
        if text not in FAILING_OPTION:
            raise ParseError(f"unknown condition option {text!r}")
        return FAILING_OPTION[text]
    if qform == "ch_offers":
        if text == "Both offers":
            return "both"
        if text == "Neither offer":
            return "neither"
        m = re.fullmatch(r"Only (.+)", text)
        if not m:
            raise ParseError(f"unknown offer option {text!r}")
        return "only:" + S.parse("category", m[1], BEN_P)
    raise ParseError(f"question {qform} has no options")


# ------------------------------------------------------------------------------------------------ set algebra

def _encode(dim: str, value, ladder: list):
    """The integer encoding of an ordinal value (day ordinal, cents, ladder rank); category values stay as keys."""
    if dim == "date":
        return dt.date.fromisoformat(value).toordinal()
    if dim == "tier":
        if value not in ladder:
            raise ParseError(f"membership level {value!r} is not on the printed ladder")
        return ladder.index(value)
    return value


def _admits(sem: str, bound, ladder: list):
    """The set a condition admits: ("set", include?, frozenset) or ("iv", lo, hi) with None for an open end."""
    dim, shape = SEM[sem]
    x = _encode(dim, bound, ladder)
    if shape == "member":
        return ("set", True, frozenset({x}))
    if shape == "nonmember":
        return ("set", False, frozenset({x}))
    return {"upto": ("iv", None, x), "below": ("iv", None, x - 1), "from": ("iv", x, None),
            "above": ("iv", x + 1, None)}[shape]


def _meet(s, t):
    """Intersection of two admitted sets of one dimension."""
    if s[0] == "iv":
        lo = s[1] if t[1] is None else (t[1] if s[1] is None else max(s[1], t[1]))
        hi = s[2] if t[2] is None else (t[2] if s[2] is None else min(s[2], t[2]))
        return ("iv", lo, hi)
    (_, inc_a, a), (_, inc_b, b) = s, t
    if inc_a and inc_b:
        return ("set", True, a & b)
    if inc_a:
        return ("set", True, a - b)
    if inc_b:
        return ("set", True, b - a)
    return ("set", False, a | b)


def _contains(s, x) -> bool:
    if s[0] == "iv":
        return (s[1] is None or s[1] <= x) and (s[2] is None or x <= s[2])
    return (x in s[2]) == s[1]


def _point(view: dict) -> dict:
    rec, ladder = view["record"], view["ladder"]
    return {"region": rec["region"], "category": rec["category"], "status": rec["status"],
            "date": _encode("date", rec["order_date"], ladder), "tier": _encode("tier", rec["tier"], ladder),
            "spend": rec["subtotal"]}


def _gets(conds: list, point: dict, ladder: list) -> bool:
    region: dict = {}
    for sem, bound in conds:
        dim = SEM[sem][0]
        s = _admits(sem, bound, ladder)
        region[dim] = _meet(region[dim], s) if dim in region else s
    return all(_contains(s, point[dim]) for dim, s in region.items())


def solve_b(view: dict):
    ladder = view["ladder"]
    point = _point(view)
    by_mark = {mark: conds for mark, conds in view["footnotes"]}
    q = view["qform"]
    if q == "ch_offers":
        if len(view["headlines"]) != 2:
            raise ParseError("ch_offers needs two headlines")
        held = [key for mark, key in view["headlines"] if _gets(by_mark.get(mark, []), point, ladder)]
        return "both" if len(held) == 2 else ("neither" if not held else "only:" + held[0])
    marks = [mark for mark, key in view["headlines"] if key == view["asked"]]
    if len(marks) != 1:
        raise ParseError("the asked benefit names no single headline")
    conds = by_mark.get(marks[0], [])
    if q == "ch_failing":
        missed = [SEM[sem][0] for sem, bound in conds if not _contains(_admits(sem, bound, ladder),
                                                                       point[SEM[sem][0]])]
        if len(missed) > 1:
            raise ParseError("more than one condition is missed: the question has no single answer")
        return missed[0] if missed else "none"
    if q not in YES_IS_GIVEN:
        raise ParseError(f"unknown question form {q}")
    return 1 if _gets(conds, point, ladder) == YES_IS_GIVEN[q] else 0
