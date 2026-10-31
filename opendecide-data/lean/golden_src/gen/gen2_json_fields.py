"""gen2_json_fields (gap-fill generator, family qa_decisions): decisions over JSON-structured records, and enum-field
extraction from short realistic messages.  Program-generated, labels exact by construction; no dataset is read and
no model is called.  Deterministic (seed 20260929), CPU only.

Sub-task (a) JSON decisions (yes/no, ~400 rows, 21 record templates over 6 domains: orders, insurance claims, support
tickets, access logs, shipments, patient appointments).  The state is a JSON object (pretty, 4-space or compact;
sometimes wrapped as {"data": ..., "meta": ...}; varied preambles) and a short business rule is given either as a
"Policy:" line in the state or inside the one-sentence question.  Traps: look-alike keys (billing vs shipping
address, requested_roles vs roles, requested_priority vs priority, previous_plan vs plan, claimed vs assessed loss,
dimensional vs actual weight, exchange vs return window, pending vs granted zones, cancelled vs active lab tests,
emergency-contact vs patient phone, return_to vs ship_to, estimated vs promised date, renewal quote vs current term),
null / missing fields, arrays needing all / any / count checks, nested objects, units in field names (cents vs
dollars, minutes vs hours, g / kg / lb), boundaries (exactly at a threshold), and status histories or message lists
where the entry with the latest timestamp wins even when the list is shown newest-first or shuffled.  About 30% of
questions are asked with the opposite polarity ("must shipping be charged?") and have their own definitions.

Sub-task (b) enum extraction (choice, ~300 rows, 11 fields: payment method, currency, carrier, contact channel,
language requested, ticket priority (urgency), account type, refund vs exchange vs store credit, delivery option,
seat, appointment format).  Every field has an explicit "not stated" option.  Messages are emails, chats, web-form
notes or timestamped threads (oldest-first or newest-first).  Patterns: direct statement, failed attempt then final
choice, change of mind, self-correction, negation plus choice, negation only, someone else's quoted suggestion plus
the writer's own choice, quote only, merely considered options, multi-message threads where the latest confirmed
choice wins, and a withdrawn choice (-> not stated).  The gold is "the writer's own last stated choice".

Every base row has a FACT-FLIP TWIN (meta.twin_of) that changes one decisive fact so the gold changes.

Self-check (every row, before writing):
  (a) three evaluators must agree: the case the row was built for, the generator's truth function over its latent
      parameters, and an independent rule evaluator that re-parses the JSON out of the RENDERED state text; the twin
      must flip the truth value; only a few JSON leaves may differ between twins.
  (b) the construction gold must equal an independent resolver over the role-tagged mention list (latest 'final'
      mention in time order, 'retract' clears it); a lexical scan of the rendered text must find exactly the option
      values listed in the mention list (no stray or missing mentions, gold present unless not stated).
Output: data/v14_parts/raw/gen2_json_fields.jsonl + data/v14_parts/defs/gen2_json_fields__<qid>.json; MANIFEST record.
"""
import collections
import copy
import fcntl
import hashlib
import json
import os
import random
import re
import sys
import time
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
KEY = "gen2_json_fields"
FAMILY = "qa_decisions"
SEED = 20260929
N_JSON_PAIRS = 200
N_ENUM_PAIRS = 150
MAX_ROWS = 770
LICENCE = "CC0 1.0 (program-generated; Claude-written templates, vocabularies, rules and program; no third-party text or labels)"
NS = "not stated"
EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal", "numeric",
             "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit", "long_context", "table",
             "multi_hop", "ambiguous"}
MISSING = "__MISSING__"


# =============================================================================================== small helpers
def cp(x):
    return copy.deepcopy(x)


def cap(s):
    return s[:1].upper() + s[1:]


def ts(x):
    return x.strftime("%Y-%m-%dT%H:%M:%SZ")


def pts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def pds(s):
    return date.fromisoformat(s)


def money(c):
    return f"{c // 100}.{c % 100:02d}"


def rdate(rng):
    return date(2025, 1, 6) + timedelta(days=rng.randrange(0, 540))


def rdt(rng, lo=8, hi=18):
    d = rdate(rng)
    return datetime(d.year, d.month, d.day, rng.randrange(lo, hi), rng.randrange(60), rng.choice([0, 5, 12, 30, 41, 58]))


def norm(t):
    return re.sub(r"\W+", " ", t.lower()).strip()


FIRST = ["Maya", "Liam", "Aisha", "Tomas", "Priya", "Noah", "Elena", "Kofi", "Sofia", "Daniel", "Mei", "Omar", "Hannah",
         "Jonas", "Leila", "Mateo", "Grace", "Ravi", "Chloe", "Ibrahim", "Nora", "Felix", "Amara", "Lucas", "Yuki", "Samir",
         "Ingrid", "Diego", "Zara", "Owen", "Farah", "Viktor", "Imani", "Paulo", "Rosa", "Ethan"]
LAST = ["Okafor", "Lindqvist", "Patel", "Moreau", "Nakamura", "Silva", "Brennan", "Kowalski", "Haddad", "Fischer", "Osei",
        "Romero", "Chen", "Novak", "Adeyemi", "Larsen", "Duarte", "Walsh", "Costa", "Varga", "Mendes", "Holm", "Reyes",
        "Sato", "Byrne", "Kaur", "Weber", "Aydin", "Quinn", "Obi", "Petrov", "Ruiz"]


def person(rng):
    f, l = rng.choice(FIRST), rng.choice(LAST)
    return {"first": f, "last": l, "name": f"{f} {l}",
            "email": f"{f.lower()}.{l.lower()}@{rng.choice(['example.com', 'example.net', 'example.org'])}"}


def phone(rng):
    return f"+1-{rng.choice([212, 303, 312, 415, 503, 512, 617, 720, 919])}-555-01{rng.randrange(10, 100)}"


CITIES = {"US": [("Portland", "OR", "97205"), ("Austin", "TX", "78701"), ("Columbus", "OH", "43215"), ("Denver", "CO", "80202"),
                 ("Raleigh", "NC", "27601"), ("Madison", "WI", "53703"), ("Tucson", "AZ", "85701"), ("Boise", "ID", "83702")],
          "CA": [("Toronto", "ON", "M5V 2T6"), ("Calgary", "AB", "T2P 1J9"), ("Halifax", "NS", "B3J 1S9")],
          "MX": [("Guadalajara", "JAL", "44100"), ("Monterrey", "NL", "64000"), ("Puebla", "PUE", "72000")],
          "GB": [("Leeds", None, "LS1 4DY"), ("Bristol", None, "BS1 5TR"), ("Glasgow", None, "G1 3SL")],
          "DE": [("Leipzig", None, "04109"), ("Bremen", None, "28195"), ("Mainz", None, "55116")],
          "FR": [("Lyon", None, "69002"), ("Nantes", None, "44000"), ("Lille", None, "59000")],
          "AU": [("Perth", "WA", "6000"), ("Hobart", "TAS", "7000"), ("Adelaide", "SA", "5000")]}
STREETS = {"US": ["Maple Ave", "Harbor St", "Linden Rd", "Quarry Ln", "Birch Way", "Orchard Dr", "Mill Rd"],
           "CA": ["King St W", "Elm Ave", "Queen St E", "Rideau Rd"], "GB": ["High Street", "Mill Lane", "Station Road", "Park Row"],
           "DE": ["Lindenstrasse", "Bahnhofstrasse", "Gartenweg"], "FR": ["rue des Lilas", "avenue Jean Jaures", "rue du Port"],
           "MX": ["Av. Juarez", "Calle Morelos", "Av. Hidalgo"], "AU": ["George St", "Beach Rd", "Hay St"]}


def address(rng, cc, who=None, name=None):
    city, region, pc = rng.choice(CITIES[cc])
    n, st = rng.randrange(2, 980), rng.choice(STREETS[cc])
    line1 = f"{st} {n}" if cc in ("DE", "MX") else f"{n} {st}"
    a = {"name": name or (who["name"] if who else "Receiving"), "line1": line1, "city": city}
    if region:
        a["region"] = region
    a["postal_code"] = pc
    a["country"] = cc
    return a


def order_id(rng):
    return f"{rng.choice(['ORD', 'SO', 'WEB'])}-{rng.randrange(100000, 999999)}"


def sku(rng):
    return f"{rng.choice('ABCDEFGHKLMNPRSTW')}{rng.choice('ABCDEFGHKLMNPRSTW')}-{rng.randrange(1000, 9999)}"


PRODUCTS = ["Ceramic pour-over set", "Wool throw blanket", "Bamboo cutting board", "LED desk lamp", "Trail running socks (3 pack)",
            "Cast iron skillet 10in", "Linen napkins (set of 4)", "Stainless water bottle", "Hardcover notebook",
            "Espresso cups (set of 2)", "Yoga mat", "Herb planter box", "Canvas tote bag", "Scented candle trio",
            "Walnut photo frame", "Leather card holder", "Glass storage jars (set of 3)", "Silk sleep mask"]


def subtotal(items):
    return sum(i["qty"] * i["unit"] for i in items)


def split_items(rng, target):
    for _ in range(200):
        n = rng.choice([1, 2, 2, 3])
        if target < 900 * n:
            n = 1
        names = rng.sample(PRODUCTS, n)
        parts, rem = [], target
        for i in range(n - 1):
            hi = min(rem - 700 * (n - 1 - i), target * 2 // n)
            if hi < 600:
                break
            x = rng.randrange(600, hi + 1)
            parts.append(x)
            rem -= x
        if len(parts) != n - 1 or rem < 400:
            continue
        parts.append(rem)
        items = []
        for k, (nm, part) in enumerate(zip(names, parts)):
            q = 1
            if k < n - 1 and part % 2 == 0 and rng.random() < 0.35:
                q = 2
            items.append({"sku": sku(rng), "name": nm, "qty": q, "unit": part // q})
        assert subtotal(items) == target
        return items
    raise RuntimeError("split_items failed")


def flat(o, pre=""):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(flat(v, f"{pre}.{k}" if pre else k))
        if not o:
            out[pre] = "{}"
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out.update(flat(v, f"{pre}[{i}]"))
        if not o:
            out[pre] = "[]"
    else:
        out[pre] = json.dumps(o)
    return out


def nleaves(o):
    return max(1, len(flat(o)))


def cdiff(a, b):
    """Changed leaves between two JSON values; arrays are compared as multisets (order changes are free)."""
    if isinstance(a, dict) and isinstance(b, dict):
        return sum(cdiff(a[k], b[k]) if k in a and k in b else nleaves(a.get(k, b.get(k))) for k in set(a) | set(b))
    if isinstance(a, list) and isinstance(b, list):
        ca = collections.Counter(json.dumps(x, sort_keys=True) for x in a)
        cb = collections.Counter(json.dumps(x, sort_keys=True) for x in b)
        oa = [json.loads(x) for x in (ca - cb).elements()]
        ob = [json.loads(x) for x in (cb - ca).elements()]
        n = sum(cdiff(x, y) for x, y in zip(oa, ob))
        return n + sum(nleaves(x) for x in oa[len(ob):]) + sum(nleaves(x) for x in ob[len(oa):])
    return 0 if a == b else 1


# =============================================================================================== (a) JSON templates
DOM_PRE = {
    "orders": ["Order record returned by the shop API:", "GET /api/v2/orders/{id} ->", "Order {id} as stored in the order-management system:",
               "Order export (JSON):"],
    "insurance": ["Claim record exported from the claims system:", "GET /claims/{id} response:", "Claim file {id} (JSON):"],
    "tickets": ["Ticket data from the help-desk API:", "Support ticket {id} (JSON export):", "Help-desk record:"],
    "access": ["Access-control record:", "Security log extract (JSON):", "Identity service output for {id}:"],
    "shipments": ["Shipment record from the carrier API:", "Tracking data for {id}:", "Shipment JSON:"],
    "appointments": ["Appointment record from the clinic scheduling system:", "Scheduling API response for {id}:",
                     "Patient appointment record (JSON):"],
}


class JT:
    name = dom = ""
    yes_cases = no_cases = ()
    policy = ask_pos = ask_neg = ()
    defs_pos = defs_neg = None

    def id_of(self, p):
        return p["id"]

    def edges(self, p):
        return []


# ------------------------------------------------------------------------------------------- orders
class FreeShipping(JT):
    name, dom = "order_free_shipping", "orders"
    yes_cases, no_cases = ("plain", "bill_abroad", "boundary"), ("ship_abroad", "subtotal_low")
    policy = ("free shipping applies only when the order's shipping address is in the US and its pre-tax subtotal is at least $50.00",
              "an order ships free only if it is being shipped to a US address and its subtotal before tax is $50.00 or more")
    ask_pos = ("does this order qualify for free shipping?", "does this order ship free?")
    ask_neg = ("must the customer be charged for shipping on this order?",)
    defs_pos = {"yes": "The order ships free: the shipping address (not the billing address) is in the US and the subtotal before tax "
                       "is at least $50.00 (5000 cents); exactly $50.00 qualifies.",
                "no": "The order does not ship free: the shipping address is outside the US, or the subtotal before tax is below "
                      "$50.00, even if the billing address is in the US or the total with tax reaches $50.00."}
    defs_neg = {"yes": "Shipping must be charged: the shipping address (not the billing address) is outside the US, or the subtotal "
                       "before tax is below $50.00, even if the total with tax reaches $50.00.",
                "no": "No shipping charge: the shipping address is in the US and the subtotal before tax is at least $50.00 (exactly "
                      "$50.00 qualifies), wherever the billing address is."}

    def sample(self, rng, case):
        who = person(rng)
        p = dict(case=case, id=order_id(rng), who=who, placed=ts(rdt(rng)), cents=rng.random() < 0.6,
                 rate=rng.choice([700, 725, 800, 825, 875, 950, 1025]), bill_first=rng.random() < 0.5,
                 method=rng.choice(["standard", "ground", "economy"]),
                 note=rng.choice([None, None, "Leave with the concierge", "Ring the side bell"]))
        p["alt_us"], p["alt_fo"] = address(rng, "US", who), address(rng, rng.choice(["CA", "MX", "GB", "AU"]), who)
        if case == "ship_abroad":
            p["ship"], p["bill"] = cp(p["alt_fo"]), address(rng, "US", who)
        elif case == "bill_abroad":
            p["ship"], p["bill"] = address(rng, "US", who), address(rng, rng.choice(["CA", "GB", "DE", "FR"]), who)
        else:
            p["ship"] = address(rng, "US", who)
            p["bill"] = cp(p["ship"]) if rng.random() < 0.5 else address(rng, "US", who)
        target = 5000 if case == "boundary" else rng.randrange(4700, 5000) if case == "subtotal_low" else rng.randrange(5000, 13000)
        p["items"] = split_items(rng, target)
        return p

    def build(self, p):
        s = subtotal(p["items"])
        tax = (s * p["rate"] + 5000) // 10000
        o = {"order_id": p["id"], "placed_at": p["placed"], "customer": {"name": p["who"]["name"], "email": p["who"]["email"]}}
        ab = [("billing_address", cp(p["bill"])), ("shipping_address", cp(p["ship"]))]
        if not p["bill_first"]:
            ab.reverse()
        o.update(ab)
        if p["cents"]:
            o["line_items"] = [{"sku": i["sku"], "name": i["name"], "quantity": i["qty"], "unit_price_cents": i["unit"]} for i in p["items"]]
            o.update(currency="USD", subtotal_cents=s, tax_cents=tax, total_cents=s + tax)
        else:
            o["line_items"] = [{"sku": i["sku"], "name": i["name"], "quantity": i["qty"], "unit_price": money(i["unit"])} for i in p["items"]]
            o["amounts"] = {"currency": "USD", "subtotal": money(s), "tax": money(tax), "total": money(s + tax)}
        o["shipping_method"] = p["method"]
        o["delivery_note"] = p["note"]
        return o

    def truth(self, p):
        return p["ship"]["country"] == "US" and subtotal(p["items"]) >= 5000

    def check(self, o):
        if (o.get("shipping_address") or {}).get("country") != "US":
            return False
        sub = Decimal(o["subtotal_cents"]) / 100 if "subtotal_cents" in o else Decimal(o["amounts"]["subtotal"])
        return sub >= Decimal("50.00")

    @staticmethod
    def _set_sub(p, new):
        q = cp(p)
        last = q["items"][-1]
        assert last["qty"] == 1
        d = new - subtotal(q["items"])
        if last["unit"] + d < 300:
            return None
        last["unit"] += d
        return q

    def flips(self, p, rng):
        c, out = p["case"], []
        if c in ("plain", "boundary"):
            q = cp(p)
            q["ship"], q["case"] = cp(p["alt_fo"]), "ship_abroad"
            out.append(("shipping address changed to a non-US address", q))
        if c == "bill_abroad":
            q = cp(p)
            q["ship"], q["bill"], q["case"] = cp(p["bill"]), cp(p["ship"]), "ship_abroad"
            out.append(("billing and shipping addresses swapped", q))
        if c in ("plain", "boundary", "bill_abroad"):
            q = self._set_sub(p, rng.randrange(4700, 5000))
            if q:
                q["case"] = "subtotal_low"
                out.append(("one item price lowered so the pre-tax subtotal is below $50.00", q))
        if c == "ship_abroad":
            q = cp(p)
            q["ship"], q["case"] = cp(p["alt_us"]), "plain"
            out.append(("shipping address changed to a US address", q))
        if c == "subtotal_low":
            new = 5000 if rng.random() < 0.4 else rng.randrange(5001, 5600)
            q = self._set_sub(p, new)
            q["case"] = "boundary" if new == 5000 else "plain"
            out.append(("one item price raised so the pre-tax subtotal reaches $50.00", q))
        return out

    def edges(self, p):
        return ["numeric", "multi_hop"] + (["units"] if p["cents"] else [])


class GiftWrap(JT):
    name, dom = "order_gift_wrap", "orders"
    yes_cases, no_cases = ("all_true",), ("one_false", "one_null", "one_missing")
    policy = ("gift wrapping can be added only if every line item in the order is marked gift-wrap eligible, where a null or missing flag "
              "counts as not eligible",
              "an order can be gift-wrapped only when all of its line items have gift_wrap_eligible set to true (null or a missing flag "
              "means not eligible)")
    ask_pos = ("can this order be gift-wrapped?", "is gift wrapping available for this order?")
    ask_neg = ("must gift wrapping be declined for this order?",)
    defs_pos = {"yes": "Every line item has gift_wrap_eligible exactly true, so the order can be gift-wrapped; whether the customer asked "
                       "for wrapping, and other item flags such as fragile, do not matter.",
                "no": "At least one line item has gift_wrap_eligible false, null or missing, so the order cannot be gift-wrapped, even "
                      "if wrapping was requested and the other items are eligible."}
    defs_neg = {"yes": "Gift wrapping must be declined: at least one line item has gift_wrap_eligible false, null or missing, even if "
                       "wrapping was requested and the other items are eligible.",
                "no": "Gift wrapping need not be declined: every line item has gift_wrap_eligible exactly true; the request flag and "
                      "other item flags such as fragile do not matter."}
    BAD = {"one_false": False, "one_null": None, "one_missing": MISSING}

    def sample(self, rng, case):
        n = rng.randint(2, 5)
        items = [{"sku": sku(rng), "name": nm, "quantity": rng.choice([1, 1, 1, 2, 3]), "fragile": rng.random() < 0.3, "gw": True}
                 for nm in rng.sample(PRODUCTS, n)]
        p = dict(case=case, id=order_id(rng), who=person(rng), placed=ts(rdt(rng)), items=items, requested=rng.random() < 0.8,
                 msg=rng.choice([None, "Happy birthday, Sam!", "Congratulations on the new place!", None]), bad=None)
        if case != "all_true":
            p["bad"] = rng.randrange(n)
            items[p["bad"]]["gw"] = self.BAD[case]
        return p

    def build(self, p):
        its = []
        for it in p["items"]:
            d = {"sku": it["sku"], "name": it["name"], "quantity": it["quantity"], "fragile": it["fragile"]}
            if it["gw"] != MISSING:
                d["gift_wrap_eligible"] = it["gw"]
            its.append(d)
        return {"order_id": p["id"], "placed_at": p["placed"], "customer_email": p["who"]["email"],
                "gift_wrap_requested": p["requested"], "gift_message": p["msg"], "line_items": its}

    def truth(self, p):
        return all(it["gw"] is True for it in p["items"])

    def check(self, o):
        return all(li.get("gift_wrap_eligible") is True for li in o["line_items"])

    def flips(self, p, rng):
        if p["case"] == "all_true":
            out = []
            for how in self.BAD:
                q = cp(p)
                k = rng.randrange(len(q["items"]))
                q["items"][k]["gw"], q["case"], q["bad"] = self.BAD[how], how, k
                out.append((f"line item {k + 1} gift_wrap_eligible set to {how.split('_')[1]}", q))
            return out
        q = cp(p)
        q["items"][p["bad"]]["gw"], q["case"], q["bad"] = True, "all_true", None
        return [(f"line item {p['bad'] + 1} gift_wrap_eligible set to true", q)]

    def edges(self, p):
        return ["quantifier"] + (["missing_info"] if p["case"] in ("one_null", "one_missing") else [])


class OrderCancel(JT):
    name, dom = "order_cancel", "orders"
    yes_cases, no_cases = ("early",), ("packed", "shipped")
    policy = ("a customer may cancel an order only while its most recent status (the status_history entry with the latest timestamp) "
              "is placed or payment_confirmed",
              "orders can be cancelled only if the latest status by timestamp in status_history is either placed or payment_confirmed")
    ask_pos = ("can this order still be cancelled?", "is the customer still allowed to cancel this order?")
    ask_neg = ("is it too late to cancel this order?",)
    defs_pos = {"yes": "The status_history entry with the latest timestamp, wherever it sits in the list, is placed or payment_confirmed, "
                       "so the order can still be cancelled.",
                "no": "The status_history entry with the latest timestamp is a later stage such as packed or shipped, so the order can "
                      "no longer be cancelled, even if the list's first or last item says placed."}
    defs_neg = {"yes": "Too late: the status_history entry with the latest timestamp is a later stage such as packed or shipped, even "
                       "if the list's first or last item says placed.",
                "no": "Not too late: the status_history entry with the latest timestamp, wherever it sits in the list, is placed or "
                      "payment_confirmed."}
    BY = {"placed": "customer", "payment_confirmed": "payments", "packed": "warehouse", "shipped": "carrier", "delivered": "carrier"}

    def sample(self, rng, case):
        prepaid = rng.random() < 0.7
        prog = ["placed", "payment_confirmed", "packed", "shipped", "delivered"] if prepaid else ["placed", "packed", "shipped", "delivered"]
        t, times = rdt(rng), []
        for _ in prog:
            times.append(ts(t))
            t += timedelta(minutes=rng.randrange(7, 1800))
        k = {"early": 1 if prepaid else 0, "packed": prog.index("packed"), "shipped": prog.index("shipped")}[case]
        return dict(case=case, id=order_id(rng), who=person(rng), prepaid=prepaid, prog=prog, times=times, k=k,
                    display=rng.choice(["oldest", "newest", "newest", "shuffled"]), skey={s: rng.random() for s in prog},
                    channel=rng.choice(["web", "ios_app", "android_app"]), fc=rng.choice(["FC-EAST-2", "FC-WEST-1", "FC-CENTRAL-4"]))

    def build(self, p):
        h = [{"status": s, "at": p["times"][i], "by": self.BY[s]} for i, s in enumerate(p["prog"][:p["k"] + 1])]
        if p["display"] == "newest":
            h = h[::-1]
        elif p["display"] == "shuffled":
            h = sorted(h, key=lambda e: p["skey"][e["status"]])
        return {"order_id": p["id"], "channel": p["channel"], "customer": {"email": p["who"]["email"]},
                "payment": {"method": "card" if p["prepaid"] else "cash_on_delivery"}, "fulfillment_center": p["fc"],
                "status_history": h, "cancellation_reason": None}

    def truth(self, p):
        return p["prog"][p["k"]] in ("placed", "payment_confirmed")

    def check(self, o):
        return max(o["status_history"], key=lambda e: pts(e["at"]))["status"] in ("placed", "payment_confirmed")

    def flips(self, p, rng):
        q = cp(p)
        if p["case"] == "early":
            q["k"], q["case"] = p["k"] + 1, "packed"
            return [("a later 'packed' entry added to status_history", q)]
        q["k"] = 1 if p["prepaid"] else 0
        q["case"] = "early"
        return [("order had not yet progressed past " + p["prog"][q["k"]], q)]

    def edges(self, p):
        return ["temporal"]


class ReturnWindow(JT):
    name, dom = "order_return_window", "orders"
    yes_cases, no_cases = ("inside", "boundary"), ("late", "undelivered")
    policy = ("a return is accepted only if the order has a recorded delivery date and the return was requested no more than the store's "
              "return-window number of days after that delivery date",
              "returns are accepted only for delivered orders, and only when the request date is at most return_window_days days after "
              "the delivery date")
    ask_pos = ("should this return request be accepted?", "is this return within the rules?")
    ask_neg = ("should this return request be rejected?",)
    defs_pos = {"yes": "The order has a delivery date and the return was requested at most return_window_days days after it (the last "
                       "day counts); the shipping date and the exchange window are irrelevant.",
                "no": "The delivery date is null or missing, or the request came more days after delivery than return_window_days "
                      "allows, even if it falls inside the exchange window."}
    defs_neg = {"yes": "Reject: the delivery date is null or missing, or the request came more days after delivery than "
                       "return_window_days allows, even if it falls inside the exchange window.",
                "no": "Accept: the order has a delivery date and the request came at most return_window_days days after it (the last "
                      "day counts); the shipping date and exchange window are irrelevant."}

    def sample(self, rng, case):
        W = rng.choice([14, 30, 30, 45, 60])
        X = rng.choice([d for d in (7, 14, 21, 30, 60, 90) if d != W])
        od = rdate(rng)
        sh = od + timedelta(days=rng.randrange(1, 4))
        gap = rng.randrange(2, 7)
        dl = sh + timedelta(days=gap)
        p = dict(case=case, id=order_id(rng), who=person(rng), W=W, X=X, od=od.isoformat(), sh=sh.isoformat(), dl=dl.isoformat(),
                 reason=rng.choice(["wrong size", "changed my mind", "arrived damaged", "not as described"]),
                 n=rng.randint(1, 3), deliv=True)
        if case == "inside":
            k = rng.randrange(max(0, W - gap + 1), W) if rng.random() < 0.5 else rng.randrange(0, W)
        elif case == "boundary":
            k = W
        elif case == "late":
            k = W + rng.randrange(1, 7)
        else:
            k = rng.randrange(0, W - 1)
            p["deliv"] = False
        p["req"] = (dl + timedelta(days=k)).isoformat()
        return p

    def build(self, p):
        return {"order_id": p["id"], "order_date": p["od"], "shipped_on": p["sh"], "delivered_on": p["dl"] if p["deliv"] else None,
                "delivery_status": "delivered" if p["deliv"] else "in_transit",
                "return_request": {"requested_on": p["req"], "reason": p["reason"], "items": p["n"]},
                "store_policy": {"return_window_days": p["W"], "exchange_window_days": p["X"]}}

    def truth(self, p):
        return p["deliv"] and 0 <= (pds(p["req"]) - pds(p["dl"])).days <= p["W"]

    def check(self, o):
        d = o.get("delivered_on")
        if not d:
            return False
        k = (pds(o["return_request"]["requested_on"]) - pds(d)).days
        return 0 <= k <= o["store_policy"]["return_window_days"]

    def flips(self, p, rng):
        c, out, dl = p["case"], [], pds(p["dl"])
        if c in ("inside", "boundary"):
            q = cp(p)
            q["req"], q["case"] = (dl + timedelta(days=p["W"] + rng.randrange(1, 5))).isoformat(), "late"
            out.append(("return requested later, past the return window", q))
            q = cp(p)
            q["deliv"], q["case"] = False, "undelivered"
            out.append(("delivery date removed (order not delivered)", q))
        elif c == "late":
            q = cp(p)
            k = p["W"] if rng.random() < 0.4 else rng.randrange(max(0, p["W"] - 6), p["W"])
            q["req"], q["case"] = (dl + timedelta(days=k)).isoformat(), "boundary" if k == p["W"] else "inside"
            out.append(("return requested earlier, inside the return window", q))
        else:
            q = cp(p)
            q["deliv"], q["case"] = True, "inside"
            out.append(("delivery date recorded", q))
        return out

    def edges(self, p):
        return ["temporal", "numeric", "multi_hop"] + (["missing_info"] if not p["deliv"] else [])


# ------------------------------------------------------------------------------------------- insurance
DOC_TYPES = ["photos", "repair_estimate", "police_report", "receipt", "proof_of_ownership", "id_document"]
LOSS_TYPES = ["water damage", "hail damage", "theft", "kitchen fire", "burst pipe", "fallen tree", "vandalism"]


def claim_id(rng, year=None):
    return f"CLM-{year or rng.randrange(2025, 2027)}-{rng.randrange(10000, 99999)}"


def policy_no(rng):
    return f"{rng.choice(['HO', 'AU', 'RN'])}-{rng.randrange(1000000, 9999999)}"


class ClaimAutoApprove(JT):
    name, dom = "claim_auto_approve", "insurance"
    yes_cases, no_cases = ("ok", "boundary"), ("over", "doc_bad")
    policy = ("a claim is auto-approved if its claimed amount is at most $2,000.00 and every attached document has status verified; "
              "otherwise it goes to manual review",
              "only claims of $2,000.00 or less whose documents are all verified are auto-approved, and all other claims go to manual review")
    ask_pos = ("can this claim be auto-approved?", "does this claim qualify for auto-approval?")
    ask_neg = ("does this claim need manual review instead of auto-approval?",)
    defs_pos = {"yes": "The claimed amount (converted from cents where the field is in cents) is at most $2,000.00 and every document's "
                       "status is exactly verified; the repair estimate and policy limit do not matter.",
                "no": "The claimed amount is above $2,000.00, or at least one document is pending, rejected, or has a null status, so "
                      "the claim goes to manual review."}
    defs_neg = {"yes": "Manual review: the claimed amount (converted from cents where needed) is above $2,000.00, or at least one "
                       "document is pending, rejected or has a null status.",
                "no": "No manual review: the claimed amount is at most $2,000.00 and every document is verified; the repair estimate "
                      "and policy limit do not matter."}

    def sample(self, rng, case):
        if case == "ok":
            amt = rng.randrange(40000, 200000)
        elif case == "boundary":
            amt = 200000
        elif case == "over":
            amt = rng.randrange(200001, 212000) if rng.random() < 0.5 else rng.randrange(212000, 350000)
        else:
            amt = rng.randrange(40000, 200001)
        trap = rng.random() < 0.5
        big = amt > 200000
        est = rng.randrange(2100, 4000) if (trap != big) else rng.randrange(900, 1990)
        docs = [{"type": t, "status": "verified", "day": rng.randrange(0, 6)} for t in rng.sample(DOC_TYPES, rng.randint(2, 4))]
        ld = rdate(rng)
        p = dict(case=case, id=claim_id(rng, ld.year), pol=policy_no(rng), who=person(rng), amt=amt, est=est,
                 unit=rng.choice(["cents", "cents", "usd", "obj"]), limit=rng.choice([10000, 25000, 50000]),
                 loss=rng.choice(LOSS_TYPES), ld=ld.isoformat(), docs=docs, bad=None)
        if case == "doc_bad":
            p["bad"] = rng.randrange(len(docs))
            docs[p["bad"]]["status"] = rng.choice(["pending", "rejected", None])
        return p

    def build(self, p):
        o = {"claim_id": p["id"], "policy_number": p["pol"], "claimant": {"name": p["who"]["name"], "email": p["who"]["email"]},
             "loss_type": p["loss"], "loss_date": p["ld"]}
        if p["unit"] == "cents":
            o["claimed_amount_cents"] = p["amt"]
        elif p["unit"] == "usd":
            o["claimed_amount_usd"] = float(money(p["amt"]))
        else:
            o["claimed_amount"] = {"value": float(money(p["amt"])), "currency": "USD"}
        o["estimated_repair_usd"] = p["est"]
        o["policy_limit_usd"] = p["limit"]
        base = pds(p["ld"])
        o["documents"] = [{"type": d["type"], "status": d["status"], "uploaded_on": (base + timedelta(days=1 + d["day"])).isoformat()}
                          for d in p["docs"]]
        o["assigned_adjuster"] = None
        return o

    def truth(self, p):
        return p["amt"] <= 200000 and all(d["status"] == "verified" for d in p["docs"])

    def check(self, o):
        if "claimed_amount_cents" in o:
            a = Decimal(o["claimed_amount_cents"]) / 100
        elif "claimed_amount_usd" in o:
            a = Decimal(str(o["claimed_amount_usd"]))
        else:
            a = Decimal(str(o["claimed_amount"]["value"]))
        return a <= Decimal("2000") and all(d.get("status") == "verified" for d in o["documents"])

    def flips(self, p, rng):
        c, out = p["case"], []
        if c in ("ok", "boundary"):
            q = cp(p)
            q["amt"], q["case"] = rng.randrange(200001, 240000), "over"
            out.append(("claimed amount raised above $2,000.00", q))
            q = cp(p)
            k = rng.randrange(len(q["docs"]))
            q["docs"][k]["status"], q["bad"], q["case"] = rng.choice(["pending", "rejected", None]), k, "doc_bad"
            out.append((f"document {k + 1} status no longer verified", q))
        elif c == "over":
            q = cp(p)
            b = rng.random() < 0.35
            q["amt"], q["case"] = (200000, "boundary") if b else (rng.randrange(150000, 200000), "ok")
            out.append(("claimed amount lowered to at most $2,000.00", q))
        else:
            q = cp(p)
            q["docs"][p["bad"]]["status"], q["bad"], q["case"] = "verified", None, "ok"
            out.append((f"document {p['bad'] + 1} status set to verified", q))
        return out

    def edges(self, p):
        e = ["numeric", "quantifier"] + (["units"] if p["unit"] == "cents" else [])
        if any(d["status"] is None for d in p["docs"]):
            e.append("missing_info")
        return e


class CoveragePeriod(JT):
    name, dom = "claim_coverage_period", "insurance"
    yes_cases, no_cases = ("inside", "start", "end"), ("after", "before")
    policy = ("a claim is covered only if the incident happened on a date within the policy's current term, from its effective date "
              "through its expiration date inclusive",
              "coverage requires the incident date to fall on or after the policy's effective_date and on or before its expiration_date")
    ask_pos = ("is this incident within the policy term?", "does the policy term cover this incident?")
    ask_neg = ("does the incident date fall outside the policy term?",)
    defs_pos = {"yes": "The incident date is on or after policy.effective_date and on or before policy.expiration_date (both ends count); "
                       "the report date and any renewal quote are irrelevant.",
                "no": "The incident date is before policy.effective_date or after policy.expiration_date, even if the report date or "
                      "an unaccepted renewal quote's dates would cover it."}
    defs_neg = {"yes": "Outside: the incident date is before policy.effective_date or after policy.expiration_date, even if the report "
                       "date or an unaccepted renewal quote's dates would cover it.",
                "no": "Inside: the incident date is on or after policy.effective_date and on or before policy.expiration_date (both ends "
                      "count); the report date and renewal quote are irrelevant."}

    def sample(self, rng, case):
        eff = rdate(rng)
        term = rng.choice([182, 365])
        exp = eff + timedelta(days=term - 1)
        inc = {"inside": eff + timedelta(days=rng.randrange(1, term - 1)), "start": eff, "end": exp,
               "after": exp + timedelta(days=rng.randrange(1, 45)), "before": eff - timedelta(days=rng.randrange(1, 30))}[case]
        return dict(case=case, id=claim_id(rng, max(inc, eff).year), who=person(rng), pol=policy_no(rng), eff=eff.isoformat(), exp=exp.isoformat(), term=term,
                    inc=inc.isoformat(), rgap=rng.randrange(0, 21), prem=rng.randrange(600, 2400),
                    prem2=rng.randrange(600, 2600), product=rng.choice(["Homeowners HO-3", "Renters HO-4", "Condo HO-6", "Personal Auto"]),
                    desc=rng.choice(["Ceiling leak after heavy rain", "Bike stolen from garage", "Windscreen cracked by debris",
                                     "Smoke damage from a pan fire", "Basement flooding"]))

    def build(self, p):
        exp = pds(p["exp"])
        r_eff = exp + timedelta(days=1)
        return {"claim_id": p["id"], "claimant": {"name": p["who"]["name"]}, "incident_date": p["inc"],
                "reported_date": (pds(p["inc"]) + timedelta(days=p["rgap"])).isoformat(), "loss_description": p["desc"],
                "policy": {"number": p["pol"], "product": p["product"], "effective_date": p["eff"], "expiration_date": p["exp"],
                           "annual_premium_usd": p["prem"]},
                "renewal_quote": {"effective_date": r_eff.isoformat(), "expiration_date": (r_eff + timedelta(days=p["term"] - 1)).isoformat(),
                                  "status": "quoted", "annual_premium_usd": p["prem2"]}}

    def truth(self, p):
        return p["eff"] <= p["inc"] <= p["exp"]

    def check(self, o):
        return pds(o["policy"]["effective_date"]) <= pds(o["incident_date"]) <= pds(o["policy"]["expiration_date"])

    def flips(self, p, rng):
        eff, exp, out = pds(p["eff"]), pds(p["exp"]), []
        if p["case"] in ("inside", "start", "end"):
            q = cp(p)
            q["inc"], q["case"] = (exp + timedelta(days=rng.randrange(1, 20))).isoformat(), "after"
            out.append(("incident date moved after the expiration date", q))
            q = cp(p)
            q["inc"], q["case"] = (eff - timedelta(days=rng.randrange(1, 12))).isoformat(), "before"
            out.append(("incident date moved before the effective date", q))
        else:
            q = cp(p)
            if rng.random() < 0.4:
                q["inc"], q["case"] = (p["exp"], "end") if p["case"] == "after" else (p["eff"], "start")
            else:
                q["inc"] = (exp - timedelta(days=rng.randrange(1, 30)) if p["case"] == "after" else eff + timedelta(days=rng.randrange(1, 30))).isoformat()
                q["case"] = "inside"
            out.append(("incident date moved inside the policy term", q))
        return out

    def edges(self, p):
        return ["temporal", "multi_hop"]


class Deductible(JT):
    name, dom = "claim_deductible", "insurance"
    yes_cases, no_cases = ("above",), ("below", "equal")
    policy = ("the insurer pays only the part of the adjuster's assessed loss that exceeds the deductible still remaining for the year",
              "a payment is made only when the assessed loss is greater than the remaining deductible, and the payment is the difference")
    ask_pos = ("will the insurer pay anything on this claim?", "does this claim result in a payment?")
    ask_neg = ("will the insurer pay nothing on this claim?",)
    defs_pos = {"yes": "The adjuster's assessed_loss_usd is greater than coverage.deductible_remaining_usd, so some amount is paid, even "
                       "if the loss is below the full annual deductible.",
                "no": "The assessed loss is at most the remaining deductible (equal pays nothing), even if the claimant's claimed amount "
                      "is larger."}
    defs_neg = {"yes": "Nothing is paid: the adjuster's assessed_loss_usd is at most coverage.deductible_remaining_usd (equal pays "
                       "nothing), even if the claimed amount is larger.",
                "no": "Something is paid: the assessed loss is greater than the remaining deductible, even if it is below the full "
                      "annual deductible."}

    def sample(self, rng, case):
        annual = rng.choice([500, 1000, 1500, 2500])
        met = rng.randrange(0, annual - 150, 50)
        rem = annual - met
        if case == "above":
            if met > 0 and rng.random() < 0.6:
                assessed = rng.randrange(rem + 1, annual)
            else:
                assessed = rem + rng.randrange(1, 1600)
            claimed = assessed + rng.randrange(0, 700)
        elif case == "below":
            assessed = rng.randrange(max(40, rem - 600), rem)
            claimed = rem + rng.randrange(50, 900) if rng.random() < 0.6 else assessed + rng.randrange(0, rem - assessed + 1)
        else:
            assessed = rem
            claimed = assessed + rng.randrange(0, 600)
        on = rdate(rng)
        return dict(case=case, id=claim_id(rng, on.year), pol=policy_no(rng), annual=annual, met=met, assessed=assessed, claimed=claimed,
                    ctype=rng.choice(["dwelling", "personal_property", "collision", "comprehensive"]), limit=rng.choice([25000, 100000, 300000]),
                    adj=person(rng), on=on.isoformat(), loss=rng.choice(LOSS_TYPES))

    def build(self, p):
        return {"claim_id": p["id"], "policy_number": p["pol"], "loss_type": p["loss"], "claimed_amount_usd": p["claimed"],
                "assessed_loss_usd": p["assessed"],
                "coverage": {"type": p["ctype"], "annual_deductible_usd": p["annual"], "deductible_met_usd": p["met"],
                             "deductible_remaining_usd": p["annual"] - p["met"], "limit_usd": p["limit"]},
                "adjuster": {"name": p["adj"]["name"], "assessed_on": p["on"]}}

    def truth(self, p):
        return p["assessed"] > p["annual"] - p["met"]

    def check(self, o):
        return o["assessed_loss_usd"] > o["coverage"]["deductible_remaining_usd"]

    def flips(self, p, rng):
        rem, q = p["annual"] - p["met"], cp(p)
        if p["case"] == "above":
            if rng.random() < 0.35:
                q["assessed"], q["case"] = rem, "equal"
            else:
                q["assessed"], q["case"] = rng.randrange(max(40, rem - 400), rem), "below"
            return [("assessed loss lowered to at most the remaining deductible", q)]
        q["assessed"], q["case"] = rem + rng.randrange(1, 500), "above"
        return [("assessed loss raised above the remaining deductible", q)]

    def edges(self, p):
        return ["numeric", "multi_hop"]


class SpecialInvestigation(JT):
    name, dom = "claim_special_investigation", "insurance"
    yes_cases, no_cases = ("two_in",), ("one_in",)
    policy = ("a claim is referred to special investigation when the policyholder has two or more prior claims whose loss date is "
              "within the 365 days before this claim's loss date",
              "referral to special investigation is required if at least two entries in prior_claims have a loss date in the 365 days "
              "before the current loss date")
    ask_pos = ("must this claim be referred to special investigation?", "does this claim trigger a special-investigation referral?")
    ask_neg = ("can this claim skip special investigation?",)
    defs_pos = {"yes": "At least two prior_claims entries have a loss_date within the 365 days before this claim's loss_date, whatever "
                       "their status or amount, so the claim is referred.",
                "no": "Fewer than two prior claims fall within the 365 days before this claim's loss date; older claims and the open "
                      "claims count do not count."}
    defs_neg = {"yes": "It can skip: fewer than two prior_claims entries have a loss_date within the 365 days before this claim's "
                       "loss_date; older claims and the open claims count do not count.",
                "no": "It cannot skip: at least two prior claims have a loss date within the 365 days before this claim's loss date, "
                      "whatever their status or amount."}

    def sample(self, rng, case):
        loss = rdate(rng) + timedelta(days=500)
        n_in = 2 if case == "two_in" else 1
        prior = [("in", rng.randrange(10, 356)) for _ in range(n_in)]
        n_out = rng.randrange(0, 3) if case == "two_in" else rng.randrange(1, 3)
        for j in range(n_out):
            prior.append(("out", rng.randrange(372, 430) if j == 0 else rng.randrange(430, 900)))
        rng.shuffle(prior)
        pcs = []
        for w, days in prior:
            st = rng.choice(["paid", "paid", "closed_without_payment", "denied"])
            pcs.append({"id": claim_id(rng, (loss - timedelta(days=days)).year), "days": days, "type": rng.choice(LOSS_TYPES), "status": st,
                        "paid": rng.randrange(300, 9000) if st == "paid" else 0})
        return dict(case=case, id=claim_id(rng, loss.year), who=person(rng), loss=loss.isoformat(), since=(loss - timedelta(days=rng.randrange(900, 3000))).isoformat(),
                    open=rng.randrange(0, 2), pcs=pcs, desc=rng.random() < 0.5)

    def build(self, p):
        loss = pds(p["loss"])
        pcs = sorted(p["pcs"], key=lambda c: c["days"], reverse=not p["desc"])
        return {"claim_id": p["id"], "loss_date": p["loss"], "policyholder": {"name": p["who"]["name"], "customer_since": p["since"]},
                "open_claims_count": p["open"],
                "prior_claims": [{"claim_id": c["id"], "loss_date": (loss - timedelta(days=c["days"])).isoformat(), "type": c["type"],
                                  "status": c["status"], "paid_usd": c["paid"]} for c in pcs]}

    def truth(self, p):
        return sum(1 <= c["days"] <= 365 for c in p["pcs"]) >= 2

    def check(self, o):
        loss = pds(o["loss_date"])
        return sum(1 <= (loss - pds(c["loss_date"])).days <= 365 for c in o["prior_claims"]) >= 2

    def flips(self, p, rng):
        q = cp(p)
        if p["case"] == "two_in":
            k = rng.choice([i for i, c in enumerate(p["pcs"]) if c["days"] <= 365])
            q["pcs"][k]["days"], q["case"] = rng.randrange(380, 460), "one_in"
            return [(f"prior claim {p['pcs'][k]['id']} moved outside the 365-day window", q)]
        k = min((i for i, c in enumerate(p["pcs"]) if c["days"] > 365), key=lambda i: p["pcs"][i]["days"])
        q["pcs"][k]["days"], q["case"] = rng.randrange(200, 356), "two_in"
        return [(f"prior claim {p['pcs'][k]['id']} moved inside the 365-day window", q)]

    def edges(self, p):
        return ["temporal", "quantifier", "numeric"]


# ------------------------------------------------------------------------------------------- support tickets
SUBJECTS = ["Cannot export invoices to CSV", "Password reset email never arrives", "Sync stuck at 99%", "Charged twice for March",
            "Webhook returns 500", "Calendar invites missing", "Mobile app logs me out", "Report totals do not match"]


def ticket_id(rng):
    return f"{rng.choice(['T', 'SUP', 'HD'])}-{rng.randrange(10000, 99999)}"


class FirstResponseSLA(JT):
    name, dom = "ticket_first_response_sla", "tickets"
    yes_cases, no_cases = ("late", "null_overdue"), ("ontime", "boundary", "null_pending")
    policy = ("the first-response SLA is breached if the first agent response came more than the SLA's first-response target after the "
              "ticket was created, or if there is still no first response and more than that target has passed by as_of",
              "a ticket breaches its first-response target when the first response arrived later than the target after creation, or when "
              "first_response_at is null and as_of is already more than the target after creation")
    ask_pos = ("has this ticket breached its first-response SLA?", "is this ticket in breach of the first-response target?")
    ask_neg = ("has this ticket avoided a first-response SLA breach so far?",)
    defs_pos = {"yes": "Breached: first_response_at minus created_at exceeds the sla first-response target (convert hours to minutes), "
                       "or first_response_at is null and as_of minus created_at exceeds the target.",
                "no": "Not breached: the first response came within the target (exactly at the target counts as met), or there is no "
                      "response yet but the target has not been exceeded by as_of; resolution targets are irrelevant."}
    defs_neg = {"yes": "No breach so far: the first response came within the sla first-response target (exactly at it counts as met), "
                       "or there is no response yet and as_of is not past the target.",
                "no": "Breached: first_response_at minus created_at exceeds the target (convert hours to minutes), or there is no "
                      "response and as_of minus created_at exceeds it."}

    def sample(self, rng, case):
        created = rdt(rng)
        hours = rng.random() < 0.5
        tgt = rng.choice([1, 2, 4, 8]) * 60 if hours else rng.choice([30, 60, 90, 120])
        resp = {"late": tgt + rng.randrange(1, 180), "ontime": rng.randrange(3, tgt), "boundary": tgt}.get(case)
        if resp is not None:
            asof = tgt + rng.randrange(200, 3000)
        elif case == "null_overdue":
            asof = tgt + rng.randrange(1, 300)
        else:
            asof = rng.randrange(2, tgt)
        upd = max(1, asof - rng.randrange(0, 30))
        return dict(case=case, id=ticket_id(rng), who=person(rng), created=ts(created), hours=hours, tgt=tgt, resp=resp, asof=asof,
                    upd=upd, lcm=rng.randrange(0, upd + 1), res=rng.choice([24, 48, 72]), subj=rng.choice(SUBJECTS),
                    ch=rng.choice(["email", "web", "chat"]), plan=rng.choice(["Standard", "Premium", "Business"]))

    def build(self, p):
        c = pts(p["created"])
        at = lambda m: ts(c + timedelta(minutes=m))
        sla = {"policy": p["plan"]}
        if p["hours"]:
            sla["first_response_hours"] = p["tgt"] // 60
        else:
            sla["first_response_minutes"] = p["tgt"]
        sla["resolution_hours"] = p["res"]
        return {"ticket_id": p["id"], "subject": p["subj"], "channel": p["ch"], "requester": {"email": p["who"]["email"]},
                "created_at": p["created"], "first_response_at": at(p["resp"]) if p["resp"] is not None else None,
                "last_customer_message_at": at(p["lcm"]), "updated_at": at(p["upd"]), "as_of": at(p["asof"]), "sla": sla}

    def truth(self, p):
        return (p["resp"] if p["resp"] is not None else p["asof"]) > p["tgt"]

    def check(self, o):
        s = o["sla"]
        tgt = s["first_response_minutes"] if "first_response_minutes" in s else s["first_response_hours"] * 60
        c = pts(o["created_at"])
        end = pts(o["first_response_at"]) if o.get("first_response_at") else pts(o["as_of"])
        return (end - c) > timedelta(minutes=tgt)

    def flips(self, p, rng):
        c, out = p["case"], []
        if c == "late":
            q = cp(p)
            q["resp"], q["case"] = (p["tgt"], "boundary") if rng.random() < 0.4 else (rng.randrange(3, p["tgt"]), "ontime")
            out.append(("first response moved within the target", q))
        elif c in ("ontime", "boundary"):
            q = cp(p)
            q["resp"], q["case"] = p["tgt"] + rng.randrange(1, 150), "late"
            out.append(("first response moved past the target", q))
            q = cp(p)
            q["resp"], q["case"] = None, "null_overdue"
            out.append(("first response removed (null)", q))
        elif c == "null_overdue":
            q = cp(p)
            q["resp"], q["case"] = rng.randrange(3, p["tgt"] + 1), "ontime"
            if q["resp"] == p["tgt"]:
                q["case"] = "boundary"
            q["resp"] = min(q["resp"], p["asof"])
            out.append(("first response recorded within the target", q))
        else:
            q = cp(p)
            q["asof"], q["case"] = p["tgt"] + rng.randrange(1, 200), "null_overdue"
            out.append(("as_of moved past the target with still no response", q))
        return out

    def edges(self, p):
        return ["temporal", "numeric"] + (["units"] if p["hours"] else []) + (["missing_info"] if p["resp"] is None else [])


class Escalate(JT):
    name, dom = "ticket_escalate", "tickets"
    yes_cases, no_cases = ("urgent", "ent_reopen"), ("req_urgent", "prev_ent", "ent_once")
    policy = ("a ticket is escalated to tier 2 if its assigned priority (not the priority the customer asked for) is urgent, or if the "
              "customer's current plan is enterprise and the ticket has been reopened at least twice",
              "a ticket goes to tier 2 when its priority field is urgent, or when the customer is currently on the enterprise plan and "
              "reopen_count is 2 or more")
    ask_pos = ("should this ticket be escalated to tier 2?", "does this ticket meet the tier-2 escalation rule?")
    ask_neg = ("should this ticket stay with tier 1?",)
    defs_pos = {"yes": "The ticket's own priority is urgent, or the customer's current plan is enterprise and reopen_count is at least 2 "
                       "(exactly 2 counts).",
                "no": "Priority is not urgent (a requested_priority of urgent does not count) and the customer is not currently "
                      "enterprise (previous_plan does not count) or reopen_count is below 2 (reply_count does not count)."}
    defs_neg = {"yes": "Stays in tier 1: priority is not urgent (requested_priority does not count) and either the current plan is not "
                       "enterprise (previous_plan does not count) or reopen_count is below 2.",
                "no": "Escalated: the ticket's own priority is urgent, or the customer's current plan is enterprise and reopen_count is "
                      "at least 2 (exactly 2 counts)."}

    def sample(self, rng, case):
        pr = rng.choice(["high", "normal"])
        req = rng.choice(["high", "normal", "low", None])
        plan = rng.choice(["starter", "business"])
        prev = rng.choice([None, "starter", "business"])
        reopen = rng.randrange(0, 2)
        if case == "urgent":
            pr = "urgent"
            plan = rng.choice(["starter", "business", "enterprise"])
            req = rng.choice(["urgent", "high", None])
        elif case == "ent_reopen":
            plan, reopen = "enterprise", rng.choice([2, 2, 3, 4])
            prev = rng.choice([None, "business"])
        elif case == "req_urgent":
            req, reopen = "urgent", rng.randrange(0, 4)
        elif case == "prev_ent":
            plan, prev, reopen = "business", "enterprise", rng.choice([2, 3, 4])
        else:
            plan, reopen = "enterprise", 1
        return dict(case=case, id=ticket_id(rng), pr=pr, req=req, plan=plan, prev=prev, reopen=reopen,
                    replies=rng.randrange(1, 4) if case != "ent_once" else rng.randrange(6, 15), acct=f"ACC-{rng.randrange(1000, 9999)}",
                    org=rng.choice(["Northwind Clinics", "Bluefin Logistics", "Harbor Legal", "Quill Press", "Ridge Analytics"]),
                    seats=rng.choice([12, 40, 150, 800]), subj=rng.choice(SUBJECTS),
                    tags=rng.sample(["billing", "api", "mobile", "sso", "export", "regression"], 2))

    def build(self, p):
        return {"ticket_id": p["id"], "subject": p["subj"], "priority": p["pr"], "requested_priority": p["req"],
                "customer": {"account_id": p["acct"], "name": p["org"], "plan": p["plan"], "previous_plan": p["prev"], "seats": p["seats"]},
                "reopen_count": p["reopen"], "reply_count": p["replies"], "tags": p["tags"]}

    def truth(self, p):
        return p["pr"] == "urgent" or (p["plan"] == "enterprise" and p["reopen"] >= 2)

    def check(self, o):
        return o["priority"] == "urgent" or (o["customer"]["plan"] == "enterprise" and o["reopen_count"] >= 2)

    def flips(self, p, rng):
        c, q = p["case"], cp(p)
        if c == "urgent":
            q["pr"] = rng.choice(["high", "normal"])
            q["case"] = "req_urgent" if p["req"] == "urgent" else "not_urgent"
            if p["plan"] == "enterprise" and p["reopen"] >= 2:
                return []
            return [("assigned priority lowered from urgent", q)]
        if c == "ent_reopen":
            if rng.random() < 0.5:
                q["reopen"], q["case"] = 1, "ent_once"
                return [("reopen_count lowered to 1", q)]
            q["plan"], q["prev"], q["case"] = "business", "enterprise", "prev_ent"
            return [("customer moved from enterprise to the business plan", q)]
        if c == "req_urgent":
            q["pr"], q["case"] = "urgent", "urgent"
            return [("assigned priority set to urgent", q)]
        if c == "prev_ent":
            q["plan"], q["prev"], q["case"] = "enterprise", "business", "ent_reopen"
            return [("customer's current plan set to enterprise", q)]
        q["reopen"], q["case"] = 2, "ent_reopen"
        return [("reopen_count raised to 2", q)]

    def edges(self, p):
        return ["multi_hop", "numeric"]


AGENT_MSGS = ["Could you send us the full error text you see?", "We've applied a fix on our side; could you check again?",
              "Could you share a screenshot of what you see?", "Here are the steps we'd like you to try; let us know how it goes.",
              "We've passed this to our engineers and made a change; please confirm whether it's resolved.",
              "Could you confirm which browser and app version you use?"]
CUST_MSGS = ["Still seeing the same error after the update.", "Thanks, I'll try that tomorrow morning.", "Attached the log you asked for.",
             "It worked once, then failed again.", "Can you check again? Nothing has changed on my side.", "Sorry for the delay, I was travelling."]


class AutoClose(JT):
    name, dom = "ticket_auto_close", "tickets"
    yes_cases, no_cases = ("agent_old",), ("customer_last", "agent_recent")
    policy = ("a ticket may be auto-closed only if its most recent message (by sent_at) was written by an agent and at least 72 hours "
              "separate that message from as_of",
              "auto-close is allowed only when the latest message by timestamp comes from an agent and as_of is 72 or more hours after it")
    ask_pos = ("can this ticket be auto-closed?", "does this ticket qualify for auto-close?")
    ask_neg = ("must the ticket be left open for now rather than auto-closed?",)
    defs_pos = {"yes": "The message with the latest sent_at, wherever it sits in the list, has author_role agent, and as_of is at least "
                       "72 hours after it (exactly 72 hours counts).",
                "no": "The latest message by sent_at is from the customer, or it is from an agent but less than 72 hours before as_of; "
                      "older agent messages do not count."}
    defs_neg = {"yes": "Leave open: the latest message by sent_at is from the customer, or it is from an agent but less than 72 hours "
                       "before as_of; older agent messages do not count.",
                "no": "Auto-close allowed: the message with the latest sent_at is from an agent and as_of is at least 72 hours after "
                      "it (exactly 72 hours counts)."}

    def sample(self, rng, case):
        t = rdt(rng)
        agents = rng.sample(AGENT_MSGS, 3)
        custs = rng.sample(CUST_MSGS, 3)
        subj = rng.choice(SUBJECTS)
        msgs = [("customer", t, rng.choice(["{s} since yesterday.", "{s} - can you help?", "{s}; this is blocking our team."]).format(s=subj))]
        rounds = rng.randrange(1, 3)
        for r in range(rounds):
            t = t + timedelta(minutes=rng.randrange(40, 1200))
            msgs.append(("agent", t, agents[r]))
            if r < rounds - 1:
                t = t + timedelta(minutes=rng.randrange(60, 1500))
                msgs.append(("customer", t, custs[r]))
        tl = msgs[-1][1]
        p = dict(case=case, id=ticket_id(rng), who=person(rng), agent=rng.choice(["Dana (Support)", "Ilya (Support)", "Marta (Support)"]),
                 subj=subj, display=rng.choice(["oldest", "newest", "shuffled"]), late_c=custs[2])
        if case == "agent_old":
            asof = tl + (timedelta(hours=72) if rng.random() < 0.2 else timedelta(minutes=72 * 60 + rng.randrange(1, 3000)))
        elif case == "agent_recent":
            asof = tl + timedelta(minutes=rng.randrange(40 * 60, 72 * 60))
        else:
            asof = tl + timedelta(minutes=72 * 60 + rng.randrange(1, 3000))
            msgs.append(("customer", tl + timedelta(minutes=rng.randrange(60, 40 * 60)), custs[2]))
        p["msgs"] = [(a, ts(x), b) for a, x, b in msgs]
        p["asof"] = ts(asof)
        p["skey"] = [rng.random() for _ in range(len(msgs) + 1)]
        return p

    def build(self, p):
        ms = [{"author_role": a, "author": p["agent"] if a == "agent" else p["who"]["name"], "sent_at": s, "body_preview": b}
              for a, s, b in p["msgs"]]
        if p["display"] == "newest":
            ms = ms[::-1]
        elif p["display"] == "shuffled":
            ms = [m for _, m in sorted(zip(p["skey"], ms), key=lambda x: x[0])]
        return {"ticket_id": p["id"], "status": "open", "subject": p["subj"], "as_of": p["asof"], "messages": ms}

    def truth(self, p):
        last = max(p["msgs"], key=lambda m: pts(m[1]))
        return last[0] == "agent" and pts(p["asof"]) - pts(last[1]) >= timedelta(hours=72)

    def check(self, o):
        last = max(o["messages"], key=lambda m: pts(m["sent_at"]))
        return last["author_role"] == "agent" and pts(o["as_of"]) - pts(last["sent_at"]) >= timedelta(hours=72)

    def flips(self, p, rng):
        c, out = p["case"], []
        tl = pts(max(p["msgs"], key=lambda m: pts(m[1]))[1])
        if c == "agent_old":
            q = cp(p)
            q["asof"], q["case"] = ts(tl + timedelta(minutes=rng.randrange(40 * 60, 72 * 60))), "agent_recent"
            out.append(("as_of moved to less than 72 hours after the agent's last message", q))
            q = cp(p)
            q["msgs"].append(("customer", ts(tl + timedelta(minutes=rng.randrange(60, 40 * 60))), p["late_c"]))
            q["case"] = "customer_last"
            out.append(("a later customer message added", q))
        elif c == "agent_recent":
            q = cp(p)
            q["asof"], q["case"] = ts(tl + timedelta(minutes=72 * 60 + rng.randrange(0, 1500))), "agent_old"
            out.append(("as_of moved to 72 or more hours after the agent's last message", q))
        else:
            q = cp(p)
            q["msgs"] = q["msgs"][:-1]
            q["case"] = "agent_old"
            out.append(("the latest customer message removed", q))
        return out

    def edges(self, p):
        return ["temporal", "numeric"]


# ------------------------------------------------------------------------------------------- access
ROLES = ["viewer", "editor", "support", "analyst", "billing", "auditor"]
DEPTS = ["Finance", "Customer Success", "Engineering", "Operations", "Legal", "Marketing"]


def req_id(rng):
    return f"req_{rng.randrange(16 ** 7, 16 ** 8):08x}"


class AdminConsole(JT):
    name, dom = "access_admin_console", "access"
    yes_cases, no_cases = ("ok",), ("requested_only", "mfa_false", "mfa_null", "mfa_missing")
    policy = ("access to the admin console is granted only if the user's current roles include admin and the user is enrolled in MFA, "
              "where a null or missing enrollment value counts as not enrolled",
              "the admin console opens only for users whose roles list contains admin and whose mfa.enrolled is true (null or missing "
              "means not enrolled)")
    ask_pos = ("should this admin console request be granted?", "does this user get into the admin console?")
    ask_neg = ("should this admin console request be denied?",)
    defs_pos = {"yes": "user.roles contains admin and user.mfa.enrolled is exactly true; roles only in requested_roles and the "
                       "required_by_policy flag do not count.",
                "no": "admin is missing from user.roles (being in requested_roles is not enough), or mfa.enrolled is false, null or "
                      "missing."}
    defs_neg = {"yes": "Deny: admin is missing from user.roles (being only in requested_roles is not enough), or mfa.enrolled is false, "
                       "null or missing.",
                "no": "Grant: user.roles contains admin and user.mfa.enrolled is exactly true; requested_roles and required_by_policy "
                      "do not count."}
    ENR = {"ok": True, "requested_only": True, "mfa_false": False, "mfa_null": None, "mfa_missing": MISSING}

    def sample(self, rng, case):
        roles = rng.sample(ROLES, rng.randint(1, 3))
        reqd = rng.sample([r for r in ROLES if r not in roles], rng.randint(0, 1))
        if case == "requested_only":
            reqd.insert(rng.randrange(len(reqd) + 1), "admin")
        else:
            roles.insert(rng.randrange(len(roles) + 1), "admin")
        who = person(rng)
        return dict(case=case, id=req_id(rng), who=who, uid=f"u_{rng.randrange(10000, 99999)}", dept=rng.choice(DEPTS),
                    roles=roles, reqd=reqd, enr=self.ENR[case], meth=rng.choice(["totp", "webauthn", "sms"]),
                    at=ts(rdt(rng)), ip=f"203.0.113.{rng.randrange(2, 250)}")

    def build(self, p):
        mfa = {}
        if p["enr"] != MISSING:
            mfa["enrolled"] = p["enr"]
        mfa["method"] = p["meth"] if p["enr"] is True else None
        mfa["required_by_policy"] = True
        return {"request_id": p["id"], "requested_at": p["at"], "resource": "admin_console", "source_ip": p["ip"],
                "user": {"id": p["uid"], "email": p["who"]["email"], "department": p["dept"], "roles": p["roles"],
                         "requested_roles": p["reqd"], "mfa": mfa}}

    def truth(self, p):
        return "admin" in p["roles"] and p["enr"] is True

    def check(self, o):
        u = o["user"]
        return "admin" in u["roles"] and u["mfa"].get("enrolled") is True

    def flips(self, p, rng):
        c, out = p["case"], []
        if c == "ok":
            q = cp(p)
            q["roles"].remove("admin")
            q["reqd"].append("admin")
            q["case"] = "requested_only"
            out.append(("admin moved from roles to requested_roles", q))
            for how in ("mfa_false", "mfa_null", "mfa_missing"):
                q = cp(p)
                q["enr"], q["case"] = self.ENR[how], how
                out.append((f"mfa.enrolled set to {how[4:]}", q))
        elif c == "requested_only":
            q = cp(p)
            q["reqd"].remove("admin")
            q["roles"].append("admin")
            q["case"] = "ok"
            out.append(("admin granted in roles", q))
        else:
            q = cp(p)
            q["enr"], q["case"] = True, "ok"
            out.append(("mfa.enrolled set to true", q))
        return out

    def edges(self, p):
        return ["multi_hop"] + (["missing_info"] if p["enr"] is None or p["enr"] == MISSING else [])


class Lockout(JT):
    name, dom = "access_lockout", "access"
    yes_cases, no_cases = ("five_in",), ("four_in", "other_acct")
    policy = ("an account is locked when it has at least five failed login attempts in the 15 minutes up to and including as_of, where "
              "only that account's own events count and successful logins do not reset the count",
              "the account is locked if five or more of its own login events with result failure are timestamped no earlier than 15 minutes "
              "before as_of (and no later than as_of)")
    ask_pos = ("should this account be locked?", "does this account hit the lockout rule?")
    ask_neg = ("should this account stay unlocked?",)
    defs_pos = {"yes": "At least five events for this account with result failure fall between as_of minus 15 minutes and as_of, both "
                       "ends included; successes in between do not reset the count.",
                "no": "Fewer than five of this account's own failures fall in that 15-minute window; failures just before the window "
                      "and failures of other accounts do not count."}
    defs_neg = {"yes": "Stay unlocked: fewer than five of this account's own failures fall between as_of minus 15 minutes and as_of; "
                       "earlier failures and other accounts' failures do not count.",
                "no": "Lock: at least five failures of this account fall in that 15-minute window, both ends included; successes in "
                      "between do not reset the count."}

    def sample(self, rng, case):
        who, other = person(rng), person(rng)
        acct = f"{who['first'][0].lower()}{who['last'].lower()}"
        oacct = f"{other['first'][0].lower()}{other['last'].lower()}"
        if oacct == acct:
            oacct += "2"
        asof = rdt(rng)
        W = 15 * 60
        used = set()

        def sec(lo, hi):
            while True:
                s = rng.randrange(lo, hi)
                if s not in used:
                    used.add(s)
                    return s

        ev = []
        n_in = 5 if case == "five_in" else 4
        bnd = rng.random() < 0.2
        for j in range(n_in):
            ev.append({"acct": acct, "res": "failure", "s": W if (bnd and j == 0) else sec(0, W)})
        if bnd:
            used.add(W)
        if case == "four_in":
            ev.append({"acct": acct, "res": "failure", "s": sec(W + 20, W + 10 * 60), "near": True})
        if case == "other_acct":
            for _ in range(rng.randint(1, 2)):
                ev.append({"acct": oacct, "res": "failure", "s": sec(0, W), "oth": True})
        for _ in range(rng.randint(0, 2)):
            ev.append({"acct": acct, "res": "success", "s": sec(0, 40 * 60)})
        for _ in range(rng.randint(0, 2)):
            ev.append({"acct": acct, "res": "failure", "s": sec(W + 11 * 60, 60 * 60)})
        if case != "other_acct" and rng.random() < 0.5:
            ev.append({"acct": oacct, "res": rng.choice(["failure", "success"]), "s": sec(0, 50 * 60)})
        for e in ev:
            e["ip"] = f"{rng.choice(['198.51.100', '203.0.113'])}.{rng.randrange(2, 250)}"
        return dict(case=case, id=acct, acct=acct, asof=ts(asof), ev=ev, desc=rng.random() < 0.3, bnd=bnd)

    def build(self, p):
        a = pts(p["asof"])
        evs = sorted(p["ev"], key=lambda e: e["s"], reverse=not p["desc"])
        return {"account": p["acct"], "as_of": p["asof"],
                "events": [{"at": ts(a - timedelta(seconds=e["s"])), "account": e["acct"], "result": e["res"], "source_ip": e["ip"]}
                           for e in evs]}

    def truth(self, p):
        return sum(e["acct"] == p["acct"] and e["res"] == "failure" and 0 <= e["s"] <= 900 for e in p["ev"]) >= 5

    def check(self, o):
        a = pts(o["as_of"])
        lo = a - timedelta(minutes=15)
        return sum(e["account"] == o["account"] and e["result"] == "failure" and lo <= pts(e["at"]) <= a for e in o["events"]) >= 5

    def flips(self, p, rng):
        q = cp(p)
        used = {e["s"] for e in p["ev"]}
        if p["case"] == "five_in":
            ks = [i for i, e in enumerate(p["ev"]) if e["acct"] == p["acct"] and e["res"] == "failure" and 0 <= e["s"] < 900]
            k = rng.choice(ks)
            s = rng.randrange(16 * 60, 25 * 60)
            while s in used:
                s += 1
            q["ev"][k]["s"], q["case"] = s, "four_in"
            return [("one of the account's failures moved to just before the 15-minute window", q)]
        if p["case"] == "four_in":
            k = next(i for i, e in enumerate(p["ev"]) if e.get("near"))
            s = rng.randrange(60, 880)
            while s in used:
                s += 1
            q["ev"][k]["s"], q["case"] = s, "five_in"
            return [("the account's failure just before the window moved inside it", q)]
        k = next(i for i, e in enumerate(p["ev"]) if e.get("oth"))
        q["ev"][k]["acct"], q["case"] = p["acct"], "five_in"
        return [("one in-window failure belongs to this account instead of another", q)]

    def edges(self, p):
        return ["temporal", "quantifier", "numeric"]


ZONES = ["lobby", "lab", "server_room", "warehouse", "office_3f", "loading_dock", "records", "clean_room"]


class BadgeEntry(JT):
    name, dom = "access_badge_entry", "access"
    yes_cases, no_cases = ("ok",), ("pending_zone", "expired", "suspended")
    policy = ("a badge opens a door only if the badge status is active, the event date is on or before the badge's valid_until date, and "
              "the door's zone is one of the zones the badge currently grants",
              "entry is allowed only when badge.status is active, the badge has not expired by the event date, and the door zone appears in "
              "badge.zones")
    ask_pos = ("should the door open for this badge?", "is this badge allowed through this door?")
    ask_neg = ("should the door stay locked for this badge?",)
    defs_pos = {"yes": "badge.status is active, the event's date is on or before valid_until (the last valid day counts), and the "
                       "event's zone is in badge.zones.",
                "no": "The badge is not active (e.g. suspended), valid_until is before the event date, or the zone is not in "
                      "badge.zones (a zone only in pending_zones does not count)."}
    defs_neg = {"yes": "Stay locked: the badge is not active, valid_until is before the event date, or the zone is not in badge.zones "
                       "(a zone only in pending_zones does not count).",
                "no": "Open: badge.status is active, the event's date is on or before valid_until (the last valid day counts), and the "
                      "zone is in badge.zones."}

    def sample(self, rng, case):
        z = rng.choice(ZONES)
        others = [x for x in ZONES if x != z]
        zones = rng.sample(others, rng.randint(1, 3))
        pend = rng.sample([x for x in others if x not in zones], rng.randint(0, 1))
        if case == "pending_zone":
            pend.insert(rng.randrange(len(pend) + 1), z)
        else:
            zones.insert(rng.randrange(len(zones) + 1), z)
        at = rdt(rng, 7, 20)
        vu = at.date() + timedelta(days=0 if rng.random() < 0.2 else rng.randrange(1, 200))
        if case == "expired":
            vu = at.date() - timedelta(days=rng.randrange(1, 20))
        who = person(rng)
        return dict(case=case, id=f"B-{rng.randrange(10000, 99999)}", who=who, dept=rng.choice(DEPTS), z=z, zones=zones, pend=pend,
                    at=ts(at), vu=vu.isoformat(), status="suspended" if case == "suspended" else "active",
                    door=f"{rng.choice('ABCD')}{rng.randrange(1, 5)}-{rng.randrange(10, 60)}")

    def build(self, p):
        return {"event": {"door_id": p["door"], "zone": p["z"], "at": p["at"]},
                "badge": {"id": p["id"], "holder": {"name": p["who"]["name"], "department": p["dept"]}, "status": p["status"],
                          "issued_on": (pds(p["vu"]) - timedelta(days=365)).isoformat(), "valid_until": p["vu"],
                          "zones": p["zones"], "pending_zones": p["pend"]}}

    def truth(self, p):
        return p["status"] == "active" and pts(p["at"]).date() <= pds(p["vu"]) and p["z"] in p["zones"]

    def check(self, o):
        b, e = o["badge"], o["event"]
        return b["status"] == "active" and pts(e["at"]).date() <= pds(b["valid_until"]) and e["zone"] in b["zones"]

    def flips(self, p, rng):
        c, out, d = p["case"], [], pts(p["at"]).date()
        if c == "ok":
            q = cp(p)
            q["zones"].remove(p["z"])
            q["pend"].append(p["z"])
            q["case"] = "pending_zone"
            out.append(("door zone moved from zones to pending_zones", q))
            q = cp(p)
            q["vu"], q["case"] = (d - timedelta(days=rng.randrange(1, 15))).isoformat(), "expired"
            out.append(("valid_until moved before the event date", q))
            q = cp(p)
            q["status"], q["case"] = "suspended", "suspended"
            out.append(("badge suspended", q))
        elif c == "pending_zone":
            q = cp(p)
            q["pend"].remove(p["z"])
            q["zones"].append(p["z"])
            q["case"] = "ok"
            out.append(("door zone granted in zones", q))
        elif c == "expired":
            q = cp(p)
            q["vu"], q["case"] = (d + timedelta(days=0 if rng.random() < 0.3 else rng.randrange(1, 90))).isoformat(), "ok"
            out.append(("valid_until extended to the event date or later", q))
        else:
            q = cp(p)
            q["status"], q["case"] = "active", "ok"
            out.append(("badge reactivated", q))
        return out

    def edges(self, p):
        return ["temporal", "multi_hop", "quantifier"]


# ------------------------------------------------------------------------------------------- shipments
HUBS = ["Memphis, TN", "Louisville, KY", "Indianapolis, IN", "Reno, NV", "Allentown, PA", "Ontario, CA", "Dallas, TX"]


def track_no(rng):
    return f"1Z{rng.randrange(10 ** 9, 10 ** 10)}" if rng.random() < 0.5 else f"TRK{rng.randrange(10 ** 8, 10 ** 9)}"


class OnTimeDelivery(JT):
    name, dom = "shipment_on_time", "shipments"
    yes_cases, no_cases = ("ontime",), ("late", "not_delivered")
    policy = ("a shipment counts as delivered on time only if its latest tracking event (by timestamp) is delivered and that event's date "
              "is on or before the promised delivery date",
              "on-time delivery means the most recent tracking event is a delivered event dated no later than promised_delivery_date")
    ask_pos = ("was this shipment delivered on time?", "does this shipment count as delivered on time?")
    ask_neg = ("does this shipment fail to count as delivered on time?",)
    defs_pos = {"yes": "The tracking event with the latest timestamp has status delivered and its date is on or before "
                       "promised_delivery_date (the same day counts); the revised estimated date is irrelevant.",
                "no": "The latest event is not delivered (e.g. out_for_delivery), or delivery happened after promised_delivery_date, "
                      "even if it met the revised estimated_delivery_date."}
    defs_neg = {"yes": "Not on time: the latest tracking event is not delivered, or the delivery date is after "
                       "promised_delivery_date, even if it met the revised estimated_delivery_date.",
                "no": "On time: the latest event by timestamp is delivered and its date is on or before promised_delivery_date (same "
                      "day counts)."}

    def sample(self, rng, case):
        promised = rdate(rng) + timedelta(days=10)
        final = {"ontime": promised - timedelta(days=rng.choice([0, 0, 1, 2])), "late": promised + timedelta(days=rng.randrange(1, 4)),
                 "not_delivered": promised - timedelta(days=rng.randrange(0, 2))}[case]
        n_tr = rng.randrange(1, 4)
        start = final - timedelta(days=n_tr + 1)
        ev = [("label_created", datetime(start.year, start.month, start.day, rng.randrange(8, 12), rng.randrange(60)), "Shipper"),
              ("picked_up", datetime(start.year, start.month, start.day, rng.randrange(15, 19), rng.randrange(60)), rng.choice(HUBS))]
        for i in range(n_tr):
            d = start + timedelta(days=i + 1)
            ev.append(("in_transit", datetime(d.year, d.month, d.day, rng.randrange(1, 23), rng.randrange(60)), rng.choice(HUBS)))
        city = rng.choice(CITIES["US"])
        loc = f"{city[0]}, {city[1]}"
        ev.append(("out_for_delivery", datetime(final.year, final.month, final.day, rng.randrange(7, 10), rng.randrange(60)), loc))
        dlv = ("delivered", datetime(final.year, final.month, final.day, rng.randrange(12, 19), rng.randrange(60)), loc)
        if case != "not_delivered":
            ev.append(dlv)
        est = final + timedelta(days=rng.randrange(0, 2)) if case == "late" else promised - timedelta(days=rng.randrange(0, 2))
        return dict(case=case, id=track_no(rng), promised=promised.isoformat(), est=est.isoformat(),
                    ev=[(s, ts(t), l) for s, t, l in ev], dlv=(dlv[0], ts(dlv[1]), dlv[2]), newest=rng.random() < 0.5,
                    svc=rng.choice(["Ground", "2Day", "Home Delivery", "Standard"]))

    def build(self, p):
        ev = [{"status": s, "at": t, "location": l} for s, t, l in p["ev"]]
        if p["newest"]:
            ev = ev[::-1]
        return {"tracking_number": p["id"], "service": p["svc"], "promised_delivery_date": p["promised"],
                "estimated_delivery_date": p["est"], "tracking_events": ev}

    def truth(self, p):
        last = max(p["ev"], key=lambda e: pts(e[1]))
        return last[0] == "delivered" and pts(last[1]).date() <= pds(p["promised"])

    def check(self, o):
        last = max(o["tracking_events"], key=lambda e: pts(e["at"]))
        return last["status"] == "delivered" and pts(last["at"]).date() <= pds(o["promised_delivery_date"])

    def flips(self, p, rng):
        c, q = p["case"], cp(p)
        dd = pts(p["dlv"][1]).date()
        if c == "ontime":
            if rng.random() < 0.5:
                q["promised"], q["case"] = (dd - timedelta(days=rng.randrange(1, 3))).isoformat(), "late"
                return [("promised delivery date moved before the delivery day", q)]
            q["ev"] = [e for e in p["ev"] if e[0] != "delivered"]
            q["case"] = "not_delivered"
            return [("delivered event removed (latest is out_for_delivery)", q)]
        if c == "late":
            q["promised"], q["case"] = (dd + timedelta(days=rng.randrange(0, 2))).isoformat(), "ontime"
            return [("promised delivery date moved to the delivery day or later", q)]
        q["ev"] = p["ev"] + [p["dlv"]]
        q["case"] = "ontime"
        return [("delivered event added on the out-for-delivery day", q)]

    def edges(self, p):
        return ["temporal"]


class WeightSurcharge(JT):
    name, dom = "shipment_weight_surcharge", "shipments"
    yes_cases, no_cases = ("over",), ("under", "exact")
    policy = ("a heavy-parcel surcharge applies when the package's actual (scale) weight is over 20 kg, and dimensional weight does not count",
              "the heavy-parcel surcharge is added only if the actual weight of the package exceeds 20 kilograms (dimensional weight is ignored)")
    ask_pos = ("does the heavy-parcel surcharge apply to this package?", "is this package charged the heavy-parcel surcharge?")
    ask_neg = ("can this package ship without the heavy-parcel surcharge?",)
    defs_pos = {"yes": "The actual weight, converted to kilograms from the unit in the field name or unit field (1000 g = 1 kg, 1 lb = "
                       "0.45359237 kg), is strictly more than 20 kg; dim_weight_kg is ignored.",
                "no": "The actual weight converted to kilograms is 20 kg or less (exactly 20 kg is not over), even if the dimensional "
                      "weight is above 20 kg."}
    defs_neg = {"yes": "No surcharge: the actual weight converted to kilograms (1000 g = 1 kg, 1 lb = 0.45359237 kg) is 20 kg or less "
                       "(exactly 20 kg is not over), even if dim_weight_kg is above 20.",
                "no": "Surcharge: the actual weight converted to kilograms is strictly more than 20 kg; the dimensional weight is "
                      "ignored."}
    LB = Decimal("0.45359237")

    def _val(self, rng, rep, side):
        if rep == "g":
            return {"over": rng.randrange(20050, 20900) if rng.random() < 0.5 else rng.randrange(20900, 32000),
                    "under": rng.randrange(8000, 20000), "exact": 20000}[side]
        if rep in ("kg", "kg_obj"):
            return {"over": rng.randrange(201, 320) / 10, "under": rng.randrange(80, 200) / 10, "exact": 20.0}[side]
        return {"over": rng.randrange(455, 700) / 10, "under": rng.randrange(200, 425) / 10}[side]

    def sample(self, rng, case):
        rep = rng.choice(["g", "kg", "lb", "kg_obj", "lb_obj"])
        if case == "exact" and rep in ("lb", "lb_obj"):
            rep = rng.choice(["g", "kg", "kg_obj"])
        w = self._val(rng, rep, case)
        heavy = case == "over"
        trap = rng.random() < 0.5
        for _ in range(500):
            l, wd, h = rng.randrange(20, 90), rng.randrange(20, 70), rng.randrange(10, 60)
            dim = round(l * wd * h / 5000, 1)
            if (dim > 20.5) == (trap != heavy) and 3 < dim < 60 and abs(dim - 20) > 0.5:
                break
        return dict(case=case, id=f"SHP-{rng.randrange(100000, 999999)}", rep=rep, w=w, dims=(l, wd, h), dim=dim,
                    svc=rng.choice(["Ground", "Freight Saver", "Express"]),
                    contents=rng.choice(["cast iron cookware", "books", "garden tools", "ceramic tiles", "an espresso machine", "a rowing machine part"]))

    def build(self, p):
        pk = {}
        if p["rep"] == "g":
            pk["weight_g"] = p["w"]
        elif p["rep"] == "kg":
            pk["weight_kg"] = p["w"]
        elif p["rep"] == "lb":
            pk["weight_lb"] = p["w"]
        else:
            pk["weight"] = {"value": p["w"], "unit": "kg" if p["rep"] == "kg_obj" else "lb"}
        pk["dimensions_cm"] = {"length": p["dims"][0], "width": p["dims"][1], "height": p["dims"][2]}
        pk["dim_weight_kg"] = p["dim"]
        return {"shipment_id": p["id"], "service": p["svc"], "contents": p["contents"], "package": pk}

    def kg(self, rep, w):
        w = Decimal(str(w))
        return w / 1000 if rep == "g" else w * self.LB if rep in ("lb", "lb_obj") else w

    def truth(self, p):
        return self.kg(p["rep"], p["w"]) > 20

    def check(self, o):
        pk = o["package"]
        if "weight_g" in pk:
            kg = Decimal(str(pk["weight_g"])) / 1000
        elif "weight_kg" in pk:
            kg = Decimal(str(pk["weight_kg"]))
        elif "weight_lb" in pk:
            kg = Decimal(str(pk["weight_lb"])) * Decimal("0.45359237")
        else:
            v = Decimal(str(pk["weight"]["value"]))
            kg = v if pk["weight"]["unit"] == "kg" else v * Decimal("0.45359237")
        return kg > 20

    def flips(self, p, rng):
        q = cp(p)
        if p["case"] == "over":
            side = "exact" if p["rep"] not in ("lb", "lb_obj") and rng.random() < 0.35 else "under"
            q["w"], q["case"] = self._val(rng, p["rep"], side), side
            return [("actual weight lowered to 20 kg or less", q)]
        q["w"], q["case"] = self._val(rng, p["rep"], "over"), "over"
        return [("actual weight raised above 20 kg", q)]

    def edges(self, p):
        return ["units", "numeric"]


class CommercialInvoice(JT):
    name, dom = "shipment_commercial_invoice", "shipments"
    yes_cases, no_cases = ("intl_high",), ("domestic", "intl_low")
    policy = ("a commercial invoice is required when the shipment goes from one country to another (ship-from versus ship-to) and its "
              "total declared value, quantity times unit value summed over all items, is more than $800",
              "a commercial invoice is needed only for cross-border shipments (ship_from and ship_to in different countries) whose items' "
              "total declared value exceeds $800")
    ask_pos = ("does this shipment need a commercial invoice?", "is a commercial invoice required for this shipment?")
    ask_neg = ("can this shipment go without a commercial invoice?",)
    defs_pos = {"yes": "ship_from and ship_to are in different countries and the sum over items of quantity times unit_value_usd is "
                       "strictly more than $800; the return_to address and insured value are irrelevant.",
                "no": "ship_from and ship_to are in the same country (a foreign return_to address does not count), or the declared "
                      "total is $800 or less, even if the insured value is higher."}
    defs_neg = {"yes": "No invoice needed: ship_from and ship_to are in the same country (a foreign return_to does not count), or the "
                       "summed quantity times unit value is $800 or less, whatever the insured value.",
                "no": "Invoice needed: ship_from and ship_to are in different countries and the summed quantity times unit_value_usd "
                      "is strictly more than $800."}
    GOODS = ["Merino sweater", "Bluetooth speaker", "Leather boots", "Watercolor set", "Mechanical keyboard", "Camera lens hood",
             "Silk scarf", "Hiking backpack", "Drone battery", "Ceramic vase"]

    def _items(self, rng, total):
        for _ in range(300):
            n = rng.randint(1, 3)
            goods = rng.sample(self.GOODS, n)
            its, rem = [], total
            for g in goods[:-1]:
                qn = rng.randint(1, 3)
                u = rng.randrange(20, max(21, (total // n) // qn + 1))
                its.append({"d": g, "q": qn, "u": u})
                rem -= qn * u
            if rem < 15:
                continue
            its.append({"d": goods[-1], "q": 1, "u": rem})
            return its
        raise RuntimeError

    def sample(self, rng, case):
        a = rng.choice(["US", "GB", "DE", "CA"])
        b = rng.choice([c for c in CITIES if c != a])
        total = {"intl_high": rng.randrange(801, 900) if rng.random() < 0.5 else rng.randrange(900, 3000),
                 "domestic": rng.randrange(801, 3000), "intl_low": 800 if rng.random() < 0.3 else rng.randrange(150, 800)}[case]
        sender = rng.choice(["Fjord Outfitters", "Copperleaf Studio", "Northgate Supply", "Tallow & Twine"])
        who = person(rng)
        p = dict(case=case, id=f"SHP-{rng.randrange(100000, 999999)}", frm=address(rng, a, name=sender),
                 to_dom=address(rng, a, who), to_intl=address(rng, b, who), intl=case != "domestic",
                 ret=address(rng, rng.choice([c for c in CITIES if c != a]) if rng.random() < 0.5 else a, name=sender + " Returns"),
                 items=self._items(rng, total), svc=rng.choice(["Express", "Economy", "Priority"]))
        p["ins"] = rng.randrange(820, 1500) if (case == "intl_low" and rng.random() < 0.5) else total + rng.randrange(0, 200)
        return p

    def build(self, p):
        return {"shipment_id": p["id"], "service": p["svc"], "ship_from": p["frm"], "ship_to": p["to_intl"] if p["intl"] else p["to_dom"],
                "return_to": p["ret"], "items": [{"description": i["d"], "quantity": i["q"], "unit_value_usd": i["u"]} for i in p["items"]],
                "insured_value_usd": p["ins"]}

    def truth(self, p):
        return p["intl"] and sum(i["q"] * i["u"] for i in p["items"]) > 800

    def check(self, o):
        return o["ship_from"]["country"] != o["ship_to"]["country"] and sum(i["quantity"] * i["unit_value_usd"] for i in o["items"]) > 800

    def flips(self, p, rng):
        c, q = p["case"], cp(p)
        tot = sum(i["q"] * i["u"] for i in p["items"])
        if c == "intl_high":
            if rng.random() < 0.5:
                q["intl"], q["case"] = False, "domestic"
                return [("ship_to changed to an address in the ship-from country", q)]
            new = 800 if rng.random() < 0.3 else rng.randrange(600, 800)
            if q["items"][-1]["u"] - (tot - new) < 15:
                q["intl"], q["case"] = False, "domestic"
                return [("ship_to changed to an address in the ship-from country", q)]
            q["items"][-1]["u"] -= tot - new
            q["case"] = "intl_low"
            return [("last item's unit value lowered so the total is at most $800", q)]
        if c == "domestic":
            q["intl"], q["case"] = True, "intl_high"
            return [("ship_to changed to an address in another country", q)]
        q["items"][-1]["u"] += rng.randrange(801, 900) - tot
        q["case"] = "intl_high"
        return [("last item's unit value raised so the total exceeds $800", q)]

    def edges(self, p):
        return ["numeric", "multi_hop"]


# ------------------------------------------------------------------------------------------- appointments
CLINICS = ["Riverside Family Practice", "Northside Dental", "Lakeview Physio", "Cedar Grove Clinic", "Harbor Eye Center"]
PROVIDERS = ["Dr. Amina Yusuf", "Dr. Paul Hendricks", "Dr. Lena Kovacs", "Dr. Marco Bianchi", "Dr. Sun-hee Park", "Dr. Owen Grady"]


def appt_id(rng):
    return f"APT-{rng.randrange(100000, 999999)}"


class SmsReminder(JT):
    name, dom = "appt_sms_reminder", "appointments"
    yes_cases, no_cases = ("ok",), ("consent_false", "consent_null", "no_mobile")
    policy = ("an SMS reminder may be sent only if the patient's own contact record has SMS consent set to true and a mobile phone number "
              "on file, where null or missing values count as no",
              "an SMS reminder may be sent only when patient.contact.sms_consent is true and patient.contact.mobile_phone is present and not null")
    ask_pos = ("may the clinic send an SMS reminder for this appointment?", "can an SMS reminder go out for this appointment?")
    ask_neg = ("must the clinic skip the SMS reminder for this appointment?",)
    defs_pos = {"yes": "In the patient's own contact record, sms_consent is exactly true and mobile_phone holds a number; email consent, "
                       "the home phone and the emergency contact's mobile are irrelevant.",
                "no": "The patient's sms_consent is false, null or missing, or the patient's own mobile_phone is null or missing, even "
                      "if a home phone or the emergency contact's mobile is on file."}
    defs_neg = {"yes": "Skip: the patient's sms_consent is false, null or missing, or the patient's own mobile_phone is null or missing, "
                       "even if a home phone or the emergency contact's mobile is on file.",
                "no": "Send allowed: in the patient's own contact record sms_consent is exactly true and mobile_phone holds a number."}
    CONS = {"ok": True, "no_mobile": True, "consent_false": False}

    def sample(self, rng, case):
        who, ec = person(rng), person(rng)
        cons = self.CONS.get(case, rng.choice([None, MISSING]))
        return dict(case=case, id=appt_id(rng), who=who, pid=f"P{rng.randrange(100000, 999999)}", start=ts(rdt(rng)),
                    clinic=rng.choice(CLINICS), mob=None if case == "no_mobile" else phone(rng), alt_mob=phone(rng),
                    home=phone(rng) if (case == "no_mobile" or rng.random() < 0.5) else None, cons=cons,
                    econs=rng.choice([True, False, None]), ec=ec, rel=rng.choice(["spouse", "daughter", "son", "sister", "friend"]),
                    ecm=phone(rng))

    def build(self, p):
        c = {"mobile_phone": p["mob"], "home_phone": p["home"], "email": p["who"]["email"]}
        if p["cons"] != MISSING:
            c["sms_consent"] = p["cons"]
        c["email_consent"] = p["econs"]
        return {"appointment_id": p["id"], "start": p["start"], "clinic": p["clinic"],
                "patient": {"id": p["pid"], "name": p["who"]["name"], "contact": c,
                            "emergency_contact": {"name": p["ec"]["name"], "relationship": p["rel"], "mobile_phone": p["ecm"]}}}

    def truth(self, p):
        return p["cons"] is True and bool(p["mob"])

    def check(self, o):
        c = o["patient"]["contact"]
        return c.get("sms_consent") is True and bool(c.get("mobile_phone"))

    def flips(self, p, rng):
        c, out = p["case"], []
        if c == "ok":
            q = cp(p)
            q["cons"], q["case"] = False, "consent_false"
            out.append(("sms_consent set to false", q))
            q = cp(p)
            q["cons"], q["case"] = rng.choice([None, MISSING]), "consent_null"
            out.append(("sms_consent null or missing", q))
            q = cp(p)
            q["mob"], q["case"] = None, "no_mobile"
            out.append(("patient mobile_phone set to null", q))
        elif c == "no_mobile":
            q = cp(p)
            q["mob"], q["case"] = p["alt_mob"], "ok"
            out.append(("patient mobile_phone recorded", q))
        else:
            q = cp(p)
            q["cons"], q["case"] = True, "ok"
            out.append(("sms_consent set to true", q))
        return out

    def edges(self, p):
        return ["multi_hop"] + (["missing_info"] if p["case"] in ("consent_null", "no_mobile") else [])


class LateCancelFee(JT):
    name, dom = "appt_late_cancel_fee", "appointments"
    yes_cases, no_cases = ("late",), ("early", "clinic", "reinstated")
    policy = ("a late-cancellation fee applies only if the appointment's latest status (by timestamp) is cancelled_by_patient and that "
              "cancellation was recorded less than 24 hours before the scheduled start",
              "the late-cancellation fee is charged only when the most recent status_history entry is cancelled_by_patient and its time is under "
              "24 hours before scheduled_start")
    ask_pos = ("should the patient be charged the late-cancellation fee?", "does the late-cancellation fee apply here?")
    ask_neg = ("should no late-cancellation fee be charged here?",)
    defs_pos = {"yes": "The status_history entry with the latest timestamp is cancelled_by_patient and it was recorded less than 24 hours "
                       "before scheduled_start (exactly 24 hours is not less).",
                "no": "The latest entry is not cancelled_by_patient (e.g. cancelled_by_clinic, or a later reinstated entry), or the "
                      "patient cancelled 24 or more hours before the start."}
    defs_neg = {"yes": "No fee: the latest status entry is not cancelled_by_patient (e.g. cancelled_by_clinic or a later reinstated), or "
                       "the patient cancelled 24 or more hours before scheduled_start.",
                "no": "Fee: the entry with the latest timestamp is cancelled_by_patient and was recorded less than 24 hours before "
                      "scheduled_start (exactly 24 hours is not less)."}

    def sample(self, rng, case):
        start = rdt(rng, 9, 17)
        booked = start - timedelta(days=rng.randrange(5, 40), minutes=rng.randrange(0, 600))
        gap = {"late": rng.randrange(60, 1440), "early": 1440 if rng.random() < 0.25 else rng.randrange(1441, 4320),
               "clinic": rng.randrange(60, 1440), "reinstated": rng.randrange(60, 1440)}[case]
        return dict(case=case, id=appt_id(rng), pid=f"P{rng.randrange(100000, 999999)}", prov=rng.choice(PROVIDERS),
                    svc=rng.choice(["new patient consult", "follow-up", "cleaning", "physio session", "eye exam"]),
                    start=ts(start), booked=ts(booked), conf=ts(booked + timedelta(minutes=rng.randrange(30, 1440))), gap=gap,
                    who="clinic" if case == "clinic" else "patient", rein=case == "reinstated",
                    rein_after=rng.randrange(10, min(gap, 300)), display=rng.choice(["oldest", "newest", "shuffled"]),
                    skey=[rng.random() for _ in range(4)])

    def hist(self, p):
        s = pts(p["start"])
        c = s - timedelta(minutes=p["gap"])
        h = [("booked", p["booked"], "patient"), ("confirmed", p["conf"], "patient"),
             ("cancelled_by_patient" if p["who"] == "patient" else "cancelled_by_clinic", ts(c), "patient" if p["who"] == "patient" else "front_desk")]
        if p["rein"]:
            h.append(("reinstated", ts(c + timedelta(minutes=p["rein_after"])), "front_desk"))
        return h

    def build(self, p):
        h = [{"status": a, "at": b, "by": d} for a, b, d in self.hist(p)]
        if p["display"] == "newest":
            h = h[::-1]
        elif p["display"] == "shuffled":
            h = [x for _, x in sorted(zip(p["skey"], h), key=lambda z: z[0])]
        return {"appointment_id": p["id"], "patient_id": p["pid"], "provider": p["prov"], "service": p["svc"],
                "scheduled_start": p["start"], "booked_at": p["booked"], "status_history": h}

    def truth(self, p):
        last = max(self.hist(p), key=lambda e: pts(e[1]))
        return last[0] == "cancelled_by_patient" and pts(p["start"]) - pts(last[1]) < timedelta(hours=24)

    def check(self, o):
        last = max(o["status_history"], key=lambda e: pts(e["at"]))
        return last["status"] == "cancelled_by_patient" and pts(o["scheduled_start"]) - pts(last["at"]) < timedelta(hours=24)

    def flips(self, p, rng):
        c, out = p["case"], []
        if c == "late":
            q = cp(p)
            q["gap"], q["case"] = (1440 if rng.random() < 0.3 else rng.randrange(1441, 3000)), "early"
            out.append(("cancellation recorded 24 or more hours before the start", q))
            q = cp(p)
            q["rein"], q["case"] = True, "reinstated"
            out.append(("a later reinstated entry added", q))
            q = cp(p)
            q["who"], q["case"] = "clinic", "clinic"
            out.append(("cancellation made by the clinic instead of the patient", q))
        elif c == "early":
            q = cp(p)
            q["gap"], q["case"] = rng.randrange(60, 1440), "late"
            q["rein_after"] = min(q["rein_after"], q["gap"] - 1)
            out.append(("cancellation recorded less than 24 hours before the start", q))
        elif c == "clinic":
            q = cp(p)
            q["who"], q["case"] = "patient", "late"
            out.append(("cancellation made by the patient", q))
        else:
            q = cp(p)
            q["rein"], q["case"] = False, "late"
            out.append(("the reinstated entry removed", q))
        return out

    def edges(self, p):
        return ["temporal", "numeric"]


LAB = [("LIPID", "Lipid panel"), ("CMP", "Comprehensive metabolic panel"), ("BMP", "Basic metabolic panel"), ("A1C", "Hemoglobin A1c"),
       ("TSH", "Thyroid stimulating hormone"), ("CBC", "Complete blood count"), ("VITD", "Vitamin D, 25-hydroxy"), ("GLU", "Glucose, plasma"),
       ("FERR", "Ferritin"), ("B12", "Vitamin B12"), ("UA", "Urinalysis"), ("INS", "Insulin, serum")]


class FastingNotice(JT):
    name, dom = "appt_fasting_notice", "appointments"
    yes_cases, no_cases = ("one_true",), ("none",)
    policy = ("fasting instructions are sent only if at least one test in the order's active lab_tests list has requires_fasting set to true",
              "the patient gets fasting instructions when any currently ordered lab test (orders.lab_tests) requires fasting")
    ask_pos = ("should fasting instructions be sent to this patient?", "does this patient need fasting instructions?")
    ask_neg = ("can the fasting instructions be left out for this appointment?",)
    defs_pos = {"yes": "At least one entry in orders.lab_tests has requires_fasting exactly true.",
                "no": "No entry in orders.lab_tests has requires_fasting true (false, null or a missing flag does not count), even if a "
                      "test in cancelled_lab_tests requires fasting."}
    defs_neg = {"yes": "They can be left out: no entry in orders.lab_tests has requires_fasting true (false, null or missing does not "
                       "count), even if a cancelled test requires fasting.",
                "no": "They are needed: at least one entry in orders.lab_tests has requires_fasting exactly true."}
    OFF = [False, False, None, MISSING]

    def sample(self, rng, case):
        tests = rng.sample(LAB, rng.randint(3, 6))
        n = rng.randint(1, min(4, len(tests) - 1))
        act = [{"code": c, "name": nm, "f": rng.choice(self.OFF)} for c, nm in tests[:n]]
        canc = [{"code": c, "name": nm, "f": rng.choice([True, False])} for c, nm in tests[n:n + rng.randint(0, 2)]]
        k = rng.randrange(n)
        if case == "one_true":
            act[k]["f"] = True
        elif canc and rng.random() < 0.7:
            canc[0]["f"] = True
        return dict(case=case, id=appt_id(rng), pid=f"P{rng.randrange(100000, 999999)}", start=ts(rdt(rng, 7, 11)), act=act, canc=canc,
                    k=k, by=rng.choice(PROVIDERS), alt=rng.choice(self.OFF))

    def build(self, p):
        def enc(t):
            d = {"code": t["code"], "name": t["name"]}
            if t["f"] != MISSING:
                d["requires_fasting"] = t["f"]
            return d
        return {"appointment_id": p["id"], "patient_id": p["pid"], "visit_type": "lab draw", "scheduled_start": p["start"],
                "orders": {"ordered_by": p["by"], "lab_tests": [enc(t) for t in p["act"]], "cancelled_lab_tests": [enc(t) for t in p["canc"]]}}

    def truth(self, p):
        return any(t["f"] is True for t in p["act"])

    def check(self, o):
        return any(t.get("requires_fasting") is True for t in o["orders"]["lab_tests"])

    def flips(self, p, rng):
        q = cp(p)
        if p["case"] == "one_true":
            q["act"][p["k"]]["f"], q["case"] = p["alt"], "none"
            return [(f"lab test {p['act'][p['k']]['code']} no longer requires fasting", q)]
        q["act"][p["k"]]["f"], q["case"] = True, "one_true"
        return [(f"lab test {p['act'][p['k']]['code']} requires fasting", q)]

    def edges(self, p):
        return ["quantifier"] + (["missing_info"] if any(t["f"] is None or t["f"] == MISSING for t in p["act"]) else [])


SPECS = ["cardiology", "dermatology", "orthopedics", "neurology", "endocrinology", "gastroenterology", "rheumatology", "ENT"]


class ReferralCheck(JT):
    name, dom = "appt_referral_check", "appointments"
    yes_cases, no_cases = ("no_ref_needed", "approved_ref"), ("coverage_ended", "ref_pending", "ref_other")
    policy = ("a specialist appointment can be confirmed only if the insurance coverage is still in force on the appointment date and, when "
              "the plan requires a referral, there is an approved referral for that same specialty",
              "a specialist visit is confirmed only when coverage_end is on or after the appointment date and either referral_required is false "
              "or some referral for the appointment's specialty has status approved")
    ask_pos = ("can this specialist appointment be confirmed?", "does this appointment pass the insurance and referral check?")
    ask_neg = ("should confirmation of this specialist appointment be refused?",)
    defs_pos = {"yes": "coverage_end is on or after the appointment date (that day counts), and either referral_required is false or a "
                       "referral with the same specialty has status approved.",
                "no": "Coverage ended before the appointment date, or a referral is required and none for this specialty is approved "
                      "(pending or denied, or approved only for another specialty)."}
    defs_neg = {"yes": "Refuse: coverage ended before the appointment date, or a referral is required and none for this specialty is "
                       "approved (pending, denied, or approved only for another specialty).",
                "no": "Confirm: coverage_end is on or after the appointment date and either no referral is required or an approved "
                      "referral exists for the same specialty."}

    def sample(self, rng, case):
        d = rdate(rng) + timedelta(days=30)
        spec = rng.choice(SPECS)
        other = rng.choice([s for s in SPECS if s != spec])
        cend = d - timedelta(days=rng.randrange(1, 60)) if case == "coverage_ended" else d + timedelta(days=0 if rng.random() < 0.2 else rng.randrange(1, 300))
        req = case != "no_ref_needed"
        refs = []
        if case in ("approved_ref", "coverage_ended"):
            refs.append([spec, "approved"])
        elif case == "ref_pending":
            refs.append([spec, rng.choice(["pending", "pending", "denied"])])
        elif case == "ref_other":
            refs.append([other, "approved"])
        else:
            if rng.random() < 0.5:
                refs.append([spec, "pending"])
        if rng.random() < 0.5:
            refs.append([rng.choice([s for s in SPECS if s not in (spec,)]), rng.choice(["approved", "expired", "pending"])])
        rng.shuffle(refs)
        refs = [{"id": f"REF-{rng.randrange(1000, 9999)}", "sp": s, "st": st, "iss": (d - timedelta(days=rng.randrange(5, 90))).isoformat()}
                for s, st in refs]
        who = person(rng)
        return dict(case=case, id=appt_id(rng), who=who, d=d.isoformat(), spec=spec, prov=rng.choice(PROVIDERS), cend=cend.isoformat(),
                    cstart=(d - timedelta(days=rng.randrange(100, 700))).isoformat(), req=req, refs=refs,
                    plan=rng.choice(["Silver HMO", "Gold PPO", "Bronze EPO", "Platinum PPO"]), mid=f"M{rng.randrange(10 ** 7, 10 ** 8)}")

    def build(self, p):
        return {"appointment": {"id": p["id"], "date": p["d"], "specialty": p["spec"], "provider": p["prov"]},
                "patient": {"name": p["who"]["name"]},
                "insurance": {"plan_name": p["plan"], "member_id": p["mid"], "coverage_start": p["cstart"], "coverage_end": p["cend"],
                              "referral_required": p["req"]},
                "referrals": [{"id": r["id"], "specialty": r["sp"], "status": r["st"], "issued_on": r["iss"]} for r in p["refs"]]}

    def truth(self, p):
        ok_ref = (not p["req"]) or any(r["sp"] == p["spec"] and r["st"] == "approved" for r in p["refs"])
        return p["cend"] >= p["d"] and ok_ref

    def check(self, o):
        a, ins = o["appointment"], o["insurance"]
        if pds(ins["coverage_end"]) < pds(a["date"]):
            return False
        return (ins["referral_required"] is False) or any(r["specialty"] == a["specialty"] and r["status"] == "approved" for r in o["referrals"])

    def flips(self, p, rng):
        c, out, d = p["case"], [], pds(p["d"])
        same = [i for i, r in enumerate(p["refs"]) if r["sp"] == p["spec"]]
        if c in ("no_ref_needed", "approved_ref"):
            q = cp(p)
            q["cend"], q["case"] = (d - timedelta(days=rng.randrange(1, 40))).isoformat(), "coverage_ended"
            out.append(("coverage_end moved before the appointment date", q))
        if c == "no_ref_needed":
            q = cp(p)
            q["req"], q["case"] = True, "ref_pending"
            if not any(r["sp"] == p["spec"] and r["st"] == "approved" for r in p["refs"]):
                out.append(("plan now requires a referral", q))
        if c == "approved_ref":
            k = next(i for i in same if p["refs"][i]["st"] == "approved")
            q = cp(p)
            q["refs"][k]["st"], q["case"] = "pending", "ref_pending"
            out.append(("the same-specialty referral is pending instead of approved", q))
        if c == "coverage_ended":
            q = cp(p)
            q["cend"], q["case"] = (d + timedelta(days=rng.randrange(0, 200))).isoformat(), "approved_ref"
            out.append(("coverage_end extended past the appointment date", q))
        if c == "ref_pending":
            k = same[0]
            q = cp(p)
            q["refs"][k]["st"], q["case"] = "approved", "approved_ref"
            out.append(("the same-specialty referral approved", q))
        if c == "ref_other":
            k = next(i for i, r in enumerate(p["refs"]) if r["st"] == "approved" and r["sp"] != p["spec"])
            q = cp(p)
            if any(r["sp"] == p["spec"] for r in p["refs"]):
                return []
            q["refs"][k]["sp"], q["case"] = p["spec"], "approved_ref"
            out.append(("the approved referral is for the appointment's specialty", q))
        return out

    def edges(self, p):
        return ["multi_hop", "temporal", "quantifier"]


JSON_TEMPLATES = [FreeShipping(), GiftWrap(), OrderCancel(), ReturnWindow(), ClaimAutoApprove(), CoveragePeriod(), Deductible(),
                  SpecialInvestigation(), FirstResponseSLA(), Escalate(), AutoClose(), AdminConsole(), Lockout(), BadgeEntry(),
                  OnTimeDelivery(), WeightSurcharge(), CommercialInvoice(), SmsReminder(), LateCancelFee(), FastingNotice(), ReferralCheck()]

POLICY_LABELS = ["Policy:", "Rule:", "Business rule:"]
INS_A = ["Under the policy above, {ask}", "According to the stated rule, {ask}", "{Ask}"]
INS_B = ["Given that {policy}, {ask}", "Assuming {policy}, {ask}", "Under a rule that says {policy}, {ask}"]


def unwrap(o):
    if isinstance(o, dict) and set(o) == {"data", "meta"}:
        return o["data"]
    return o


def render_json_state(T, p, S):
    o = T.build(p)
    if S["wrap"]:
        o = {"data": o, "meta": {"request_id": S["req"], "api_version": S["apiv"]}}
    js = json.dumps(o, ensure_ascii=False) if S["indent"] is None else json.dumps(o, indent=S["indent"], ensure_ascii=False)
    pre = DOM_PRE[T.dom][S["pre"]].format(id=T.id_of(p)) if S["pre"] is not None else None
    body = (pre + "\n" if pre else "") + js
    if S["mode"] == "A":
        head = f"{POLICY_LABELS[S['plab']]} {cap(T.policy[S['pv']])}."
        assert "{" not in head
        return head + "\n\n" + body
    return body


def json_instructions(T, S):
    asks = T.ask_neg if S["neg"] else T.ask_pos
    ask = asks[S["av"] % len(asks)]
    if S["mode"] == "A":
        return INS_A[S["iv"]].format(ask=ask, Ask=cap(ask))
    return INS_B[S["iv"]].format(policy=T.policy[S["pv"]], ask=ask)


def parse_state_json(state):
    return unwrap(json.loads(state[state.index("{"):]))


def make_json_pair(T, case, rng, idx, used=None):
    p = T.sample(rng, case)
    fl = T.flips(p, rng)
    if not fl:
        return None
    used = used if used is not None else collections.Counter()
    lo = min(used[q["case"]] for _, q in fl)
    desc, q = rng.choice([(d, q) for d, q in fl if used[q["case"]] == lo])  # the least-covered trap for this template
    S = dict(wrap=rng.random() < 0.2, req=req_id(rng), apiv=rng.choice(["v2", "2026-03-01", "v1.4"]),
             indent=rng.choice([2, 2, 2, 4, None]), pre=None if rng.random() < 0.15 else rng.randrange(len(DOM_PRE[T.dom])),
             mode="A" if rng.random() < 0.55 else "B", plab=rng.randrange(len(POLICY_LABELS)), pv=rng.randrange(len(T.policy)),
             neg=rng.random() < 0.3, av=rng.randrange(6), iv=rng.randrange(3))
    ins = json_instructions(T, S)
    qid = T.name + ("_neg" if S["neg"] else "")
    rows, chk = [], []
    rid0 = f"{KEY}-json-{T.name}-{idx:04d}"
    for j, pp in enumerate((p, q)):
        tr = T.truth(pp)
        assert tr == (pp["case"] in T.yes_cases), (T.name, pp["case"], tr)
        state = render_json_state(T, pp, S)
        o = parse_state_json(state)
        assert T.check(o) == tr, (T.name, pp["case"], "independent check disagrees")
        gold = "yes" if tr != S["neg"] else "no"
        edges = list(T.edges(pp)) + (["negation"] if S["neg"] else [])
        meta = {"dataset": f"program generator golden_src/gen/{KEY}.py", "config": f"json:{T.name}:{pp['case']}", "revision": None,
                "licence": LICENCE, "split": "train",
                "orig_label": {"rule_holds": tr, "case": pp["case"], "polarity": "neg" if S["neg"] else "pos", "template": T.name,
                               "domain": T.dom, **({"changed": desc} if j == 1 else {})},
                "family": FAMILY, "edge": ",".join(dict.fromkeys(edges)) or None, "defs": qid}
        if j == 1:
            meta["twin_of"] = rid0
        rows.append({"key": KEY, "rid": rid0 if j == 0 else rid0 + "-twin", "state": state, "instructions": ins,
                     "options": ["yes", "no"], "gold": gold, "soft": None, "meta": meta})
        chk.append(o)
    assert rows[0]["gold"] != rows[1]["gold"]
    ndiff = cdiff(chk[0], chk[1])
    assert 1 <= ndiff <= 12, (T.name, ndiff, desc)
    rows[1]["meta"]["orig_label"]["json_leaves_changed"] = ndiff
    return rows


# =============================================================================================== (b) enum fields
RETRACT = ["Please hold off on that for now; I'm not sure anymore and will get back to you.",
           "Actually, scratch that for now. I need to check a few things first and will confirm later."]

FIELDS = {
    "payment_method": dict(
        what="payment method", noun="a method",
        opts={"card": "credit or debit card", "paypal": "PayPal", "bank": "bank transfer", "cash": "cash"},
        desc={"card": "a credit or debit card (Visa, Mastercard and the like)", "paypal": "PayPal", "bank": "a bank or wire transfer",
              "cash": "cash"},
        surf={"card": ["my Visa card", "my debit card", "my credit card", "my Mastercard"], "paypal": ["PayPal", "my PayPal account"],
              "bank": ["a bank transfer", "a wire transfer"], "cash": ["cash"]},
        rx={"card": r"\b([Cc]ard|Visa|Mastercard)\b", "paypal": r"PayPal", "bank": r"\b([Bb]ank|[Ww]ire) transfer\b", "cash": r"\b[Cc]ash\b"},
        subj=["Payment for order {ref}", "Invoice {ref}", "Re: your balance on {ref}"],
        open=["This is about order {ref}.", "Quick note on invoice {ref} for the sofa delivery.", "I'm writing about the balance on booking {ref}."],
        who=["accountant", "partner", "brother", "office manager"], no_tried={"cash"},
        T={"final": ["I paid using {v}.", "In the end I paid the full amount using {v}.", "The payment was made using {v} this morning."],
           "tried": ["My first attempt was using {v}, but it didn't go through.", "I tried paying using {v} first, but it was declined."],
           "final_after_tried": ["I paid using {v} after my attempt with {w} was declined.",
                                 "The payment was made using {v}, because the attempt with {w} failed."],
           "neg": ["I'm not using {v} for this.", "{V} is not an option for me."],
           "quote": ['My {who} told me, "Just pay using {v}."', 'The note from my {who} says: "Use {v} for this one."'],
           "own_despite_quote": ['I paid using {v}, even though my {who} had said, "Just use {w}."'],
           "consider": ["I might pay using {v}, but I haven't decided.", "Maybe I'll use {v}?"],
           "undecided": ["I haven't paid yet and haven't decided how I will.", "I'll sort out the payment once I've checked the total."],
           "ask": ["Which payment methods do you accept?", "Could you tell me what payment options you offer?"],
           "change": ["I had chosen {a} at first, but I switched to {b} before paying.", "I changed the payment from {a} to {b}."],
           "change_goldfirst": ["I ended up paying using {b}, not {a} as I first planned."],
           "correction": ["Sorry, I misspoke: I paid using {b}, not {a}."],
           "t_first": ["I'll pay using {v}.", "Planning to pay using {v}."],
           "t_change": ["Change of plan: I'll pay using {v} instead.", "Update: I'm switching to {v}."],
           "t_revert": ["Please ignore my last message; I'll pay using {v} after all.", "Sorry, going back to {v} as first planned."],
           "t_confirm": ["Confirming that I'll pay using {v}.", "Just confirming: {v}."]},
        q=["Which payment method did the customer settle on?", "Which payment method should be recorded, based on the customer's own final choice?",
           "According to the message, which payment method did the writer finally choose or use?"]),
    "currency": dict(
        what="billing currency", noun="a currency",
        opts={"usd": "US dollars", "eur": "euros", "gbp": "British pounds", "jpy": "Japanese yen"},
        desc={"usd": "US dollars (USD)", "eur": "euros (EUR)", "gbp": "British pounds (GBP, sterling)", "jpy": "Japanese yen (JPY)"},
        surf={"usd": ["US dollars", "USD"], "eur": ["euros", "EUR"], "gbp": ["British pounds", "GBP", "pounds sterling"], "jpy": ["Japanese yen", "JPY"]},
        rx={"usd": r"\bUSD\b|US dollars?", "eur": r"\bEUR\b|\b[Ee]uros?\b", "gbp": r"\bGBP\b|British pounds?|pounds sterling|\bsterling\b",
            "jpy": r"\bJPY\b|\b[Yy]en\b"},
        subj=["Invoice for {ref}", "Quote {ref}", "Subscription renewal {ref}"],
        open=["A note about the invoice for the translation work ({ref}).", "Regarding your quote {ref} for the conference booth.",
              "About our annual subscription renewal ({ref})."],
        who=["CFO", "controller", "procurement lead", "project manager"], no_tried=set(),
        T={"final": ["Please issue the invoice in {v}.", "We'd like to be billed in {v}.", "Our finance team has confirmed we will pay in {v}."],
           "tried": ["We tried to set up payment in {v}, but our account doesn't support it.", "We looked into paying in {v}, but our bank can't handle it."],
           "final_after_tried": ["Please bill us in {v}; setting up payment in {w} didn't work with our bank."],
           "neg": ["Please don't bill us in {v}.", "We can't pay in {v}."],
           "quote": ['Our {who} wrote, "Ask them to bill in {v}."', 'Forwarding a note from our {who}: "Billing in {v} would be simplest for us."'],
           "own_despite_quote": ['Please bill us in {v}, even though our {who} wrote, "Ask them to bill in {w}."'],
           "consider": ["We might want {v}, but it's not settled.", "Could {v} be an option?"],
           "undecided": ["We're still deciding which currency works best.", "Finance hasn't picked a currency yet."],
           "ask": ["Which currencies can you invoice in?", "What currencies do you support for billing?"],
           "change": ["We had asked for {a}, but please switch the invoice to {b}.", "Please change the billing currency from {a} to {b}."],
           "change_goldfirst": ["Please invoice in {b} rather than {a}, which we asked for earlier."],
           "correction": ["Correction: please use {b}, not {a}."],
           "t_first": ["Please invoice us in {v}.", "We'd like the invoice in {v}."],
           "t_change": ["Update: we need the invoice in {v} instead.", "Change of plan: {v}, please."],
           "t_revert": ["Sorry, disregard that; {v} is fine after all.", "Going back to {v} as originally requested."],
           "t_confirm": ["Confirming {v} for the invoice.", "Just confirming the invoice should be in {v}."]},
        q=["Which currency does the customer want to be billed in?", "Based on the customer's own final request, what currency should the invoice use?",
           "In which currency should the invoice be issued, according to the message?"]),
    "carrier": dict(
        what="shipping carrier", noun="a carrier",
        opts={"ups": "UPS", "fedex": "FedEx", "dhl": "DHL", "usps": "USPS"},
        desc={"ups": "UPS", "fedex": "FedEx", "dhl": "DHL", "usps": "USPS (the US Postal Service)"},
        surf={"ups": ["UPS"], "fedex": ["FedEx"], "dhl": ["DHL"], "usps": ["USPS"]},
        rx={"ups": r"\bUPS\b", "fedex": r"FedEx", "dhl": r"\bDHL\b", "usps": r"\bUSPS\b"},
        subj=["Shipping for order {ref}", "Replacement part ({ref})", "Samples shipment {ref}"],
        open=["This is about order {ref}.", "Regarding the replacement part for ticket {ref}.", "About the samples you're sending us ({ref})."],
        who=["warehouse lead", "receptionist", "office manager", "colleague"], no_tried=set(),
        T={"final": ["Please ship it with {v}.", "We'd like it sent via {v}.", "Go ahead and use {v} for this shipment."],
           "tried": ["We tried to book a {v} pickup, but there were no slots.", "We tried {v} last time and the parcel was held for a week."],
           "final_after_tried": ["Please ship it with {v}; we tried to book a {w} pickup but there were no slots."],
           "neg": ["Please don't use {v}.", "Not {v}, please."],
           "quote": ['Our {who} said, "Send everything with {v}."', 'From our {who}: "{V} is usually fastest to us."'],
           "own_despite_quote": ['Please ship it with {v}, even though our {who} said, "Send it with {w}."'],
           "consider": ["{V} might be an option.", "Maybe {v} would be quicker?"],
           "undecided": ["We haven't decided on a carrier yet.", "I'll let you know which carrier to use."],
           "ask": ["Which carriers do you ship with?", "What shipping carriers can you use?"],
           "change": ["I had asked for {a}, but please use {b} instead.", "Please switch the shipment from {a} to {b}."],
           "change_goldfirst": ["Please use {b} instead of {a}, which I asked for earlier."],
           "correction": ["Correction: please ship with {b}, not {a}."],
           "t_first": ["Please ship with {v}.", "We'd like {v} for this one."],
           "t_change": ["Change of plan: use {v} instead.", "Update: please switch to {v}."],
           "t_revert": ["Ignore that last message; {v} is fine.", "Sorry, back to {v} as first requested."],
           "t_confirm": ["Confirming {v} for this shipment.", "Just confirming: {v}."]},
        q=["Which carrier does the customer want the order shipped with?", "Based on the writer's own final instruction, which shipping carrier should be used?",
           "Which carrier should be booked, according to the message?"]),
    "contact_channel": dict(
        what="contact channel", noun="a channel",
        opts={"email": "email", "call": "phone call", "text": "text message", "post": "postal mail"},
        desc={"email": "email", "call": "a phone call", "text": "a text message (SMS)", "post": "postal mail (a letter)"},
        surf={"email": ["email"], "call": ["a phone call"], "text": ["a text message", "an SMS"], "post": ["postal mail"]},
        rx={"email": r"\b[Ee]-?mail\b", "call": r"[Pp]hone call", "text": r"[Tt]ext message|\bSMS\b", "post": r"[Pp]ostal mail"},
        subj=["Case {ref}", "Warranty claim {ref}", "Appointment request {ref}"],
        open=["I'm following up on case {ref}.", "This is about my warranty claim {ref}.", "Regarding my appointment request {ref}."],
        who=["husband", "daughter", "caregiver", "assistant"], no_tried=set(),
        T={"final": ["The best way to reach me is {v}.", "Please use {v} for any follow-ups.", "I'd prefer {v} from now on."],
           "tried": ["You tried {v} last week, but I missed it.", "Your office tried {v} on Monday, but it didn't reach me."],
           "final_after_tried": ["Please use {v} for follow-ups; you tried {w} last week and I missed it."],
           "neg": ["Please don't use {v}.", "{V} doesn't work for me."],
           "quote": ['My {who} wrote to you: "Use {v} to reach us."', 'My {who} suggested, "Just use {v}."'],
           "own_despite_quote": ['Please use {v} for follow-ups, even though my {who} wrote to you, "Use {w} to reach us."'],
           "consider": ["Maybe {v} would work?", "I could possibly do {v}."],
           "undecided": ["I'm not sure yet how you should reach me.", "I'll confirm the best way to reach me later."],
           "ask": ["How do you usually contact customers about this?", "What contact options do you have?"],
           "change": ["I had asked for {a}, but please use {b} from now on.", "Please switch my contact preference from {a} to {b}."],
           "change_goldfirst": ["Please use {b} from now on rather than {a}, which I gave before."],
           "correction": ["Correction: please use {b}, not {a}."],
           "t_first": ["Please use {v} to reach me.", "I'd like {v} for updates."],
           "t_change": ["Update: {v} is better for me now.", "Change of plan: please use {v}."],
           "t_revert": ["Actually, please go back to {v}.", "Sorry, {v} as before is best."],
           "t_confirm": ["Confirming: {v} is best.", "Just confirming {v} for updates."]},
        q=["How does the customer want to be contacted?", "Based on the writer's own final preference, which contact channel should be used for follow-ups?",
           "Which contact channel did the writer ask for?"]),
    "language": dict(
        what="requested language", noun="a language",
        opts={"en": "English", "es": "Spanish", "fr": "French", "de": "German", "pt": "Portuguese"},
        desc={"en": "English", "es": "Spanish", "fr": "French", "de": "German", "pt": "Portuguese"},
        surf={"en": ["English"], "es": ["Spanish"], "fr": ["French"], "de": ["German"], "pt": ["Portuguese"]},
        rx={"en": r"\bEnglish\b", "es": r"\bSpanish\b", "fr": r"\bFrench\b", "de": r"\bGerman\b", "pt": r"\bPortuguese\b"},
        subj=["Interpreter booking {ref}", "Lease documents {ref}", "Support session {ref}"],
        open=["I'm booking an interpreter for the hearing ({ref}).", "This is about the lease documents for unit {ref}.",
              "I'd like to schedule a support session ({ref})."],
        who=["neighbor", "lawyer", "son", "coworker"], no_tried=set(),
        T={"final": ["Please provide everything in {v}.", "I need the service in {v}.", "Please send the documents in {v}."],
           "tried": ["We tried a session in {v} last time, but it didn't work out.", "Last year we had the forms in {v}, which was hard for us."],
           "final_after_tried": ["Please provide it in {v}; we tried a session in {w} last time and it didn't work out."],
           "neg": ["Please don't send it in {v}.", "{V} won't work for us."],
           "quote": ['My {who} suggested, "Request {v}."', 'My {who} told me, "Ask them for {v}."'],
           "own_despite_quote": ['Please provide everything in {v}, even though my {who} suggested, "Request {w}."'],
           "consider": ["{V} might be easier for my family.", "Could it maybe be in {v}?"],
           "undecided": ["We haven't settled on a language yet.", "I'll confirm the language once I've checked with the family."],
           "ask": ["Which languages do you offer?", "What languages are available?"],
           "change": ["I had asked for {a}, but please switch to {b}.", "Please change the language from {a} to {b}."],
           "change_goldfirst": ["Please switch to {b}; I had asked for {a} earlier."],
           "correction": ["Correction: I need {b}, not {a}."],
           "t_first": ["Please book it in {v}.", "We'd like it in {v}."],
           "t_change": ["Change: we need {v} instead.", "Update: please make it {v}."],
           "t_revert": ["Sorry, ignore that; {v} as originally planned.", "Going back to {v}, please."],
           "t_confirm": ["Confirming {v}.", "Just confirming {v} for the booking."]},
        q=["Which language does the writer request?", "Based on the writer's own final request, which language should the service be provided in?",
           "What language did the writer ask for?"]),
    "priority": dict(
        what="ticket priority", noun="a priority",
        opts={"urgent": "urgent", "high": "high", "normal": "normal", "low": "low"},
        desc={"urgent": "urgent", "high": "high priority", "normal": "normal priority", "low": "low priority"},
        surf={"urgent": ["urgent"], "high": ["high priority"], "normal": ["normal priority"], "low": ["low priority"]},
        rx={"urgent": r"\b[Uu]rgent\b", "high": r"[Hh]igh priority", "normal": r"[Nn]ormal priority", "low": r"[Ll]ow priority"},
        subj=["Dashboard charts blank ({ref})", "Invoice export failing ({ref})", "App logging me out ({ref})"],
        open=["Our reporting dashboard shows blank charts since this morning ({ref}).", "The invoice export fails for one of our accounts ({ref}).",
              "The mobile app logs me out every few minutes ({ref})."],
        who=["team lead", "manager", "colleague"], no_tried=set(), skip={"TRY", "CONS"},
        T={"final": ["Please mark this ticket as {v}.", "Please file this as {v}.", "I'm setting this to {v}."],
           "neg": ["Please don't mark this as {v}.", "This is not {v}."],
           "quote": ['My {who} said, "Mark it as {v}."', 'My {who} wrote, "This one is {v}."'],
           "own_despite_quote": ['Please mark this ticket as {v}, even though my {who} said, "Mark it as {w}."'],
           "undecided": ["I'll leave the priority to you.", "Set whatever priority you think fits."],
           "ask": ["Which priority should I choose for this?", "How do I pick the right priority level?"],
           "change": ["I first marked this as {a}, but please change it to {b}.", "Please move it from {a} to {b}."],
           "change_goldfirst": ["Please change it to {b}; I had first marked it as {a}."],
           "correction": ["Correction: please file it as {b}, not {a}."],
           "t_first": ["Please mark this as {v}.", "Filing this as {v}."],
           "t_change": ["Update: please make it {v} instead.", "Change of plan: {v}."],
           "t_revert": ["Sorry, keep it at {v} after all.", "Please go back to {v}."],
           "t_confirm": ["Confirming {v}.", "Just confirming it should be {v}."]},
        q=["Which priority does the writer ask for this ticket?", "Based on the writer's own final request, what priority should the ticket get?",
           "What priority level did the writer choose?"]),
    "account_type": dict(
        what="account type", noun="an account type",
        opts={"personal": "personal", "business": "business", "joint": "joint", "student": "student"},
        desc={"personal": "a personal account", "business": "a business account", "joint": "a joint account", "student": "a student account"},
        surf={"personal": ["personal account"], "business": ["business account"], "joint": ["joint account"], "student": ["student account"]},
        rx={"personal": r"personal account", "business": r"business account", "joint": r"joint account", "student": r"student account"},
        subj=["New account enquiry", "Opening an account ({ref})", "Follow-up to appointment {ref}"],
        open=["I'm interested in opening an account with your bank.", "I've just moved to the area and want to open an account ({ref}).",
              "I'm following up on my branch appointment {ref}."],
        who=["father", "wife", "roommate", "accountant"], no_tried=set(),
        T={"final": ["I'd like to open a {v}.", "Please set me up with a {v}.", "I've decided on a {v}."],
           "tried": ["I applied for a {v} online, but the form rejected my documents.", "I started a {v} application last month but never finished it."],
           "final_after_tried": ["Please set me up with a {v}; my online application for a {w} was rejected."],
           "neg": ["I don't want a {v}.", "A {v} isn't what I need."],
           "quote": ['The advisor told me, "A {v} would suit you."', 'My {who} said, "Just get a {v}."'],
           "own_despite_quote": ['I\'d like to open a {v}, even though the advisor told me, "A {w} would suit you."'],
           "consider": ["I'm considering a {v}.", "Maybe a {v} makes sense?"],
           "undecided": ["I haven't decided which type of account to open.", "I'm not sure yet which account is right for me."],
           "ask": ["What account types do you offer?", "Can you explain the differences between your accounts?"],
           "change": ["I had picked a {a}, but I'd now rather open a {b}.", "Please change my application from a {a} to a {b}."],
           "change_goldfirst": ["I'd now rather open a {b} than the {a} I picked first."],
           "correction": ["Correction: I want a {b}, not a {a}."],
           "t_first": ["I'd like a {v}.", "Please start a {v} for me."],
           "t_change": ["Change of plan: I'd prefer a {v}.", "Update: make it a {v} instead."],
           "t_revert": ["Sorry, scratch that; a {v} as first planned.", "Going back to the {v}, please."],
           "t_confirm": ["Confirming: a {v}.", "Just confirming I want the {v}."]},
        q=["Which type of account does the writer want to open?", "Based on the writer's own final choice, which account type should be opened?",
           "What account type did the writer settle on?"]),
    "resolution": dict(
        what="return resolution", noun="a resolution",
        opts={"refund": "refund", "exchange": "exchange", "credit": "store credit"},
        desc={"refund": "a refund of the money paid", "exchange": "an exchange for another item or size", "credit": "store credit"},
        surf={"refund": ["a refund", "a full refund"], "exchange": ["an exchange", "an exchange for a different size"], "credit": ["store credit"]},
        rx={"refund": r"\b[Rr]efund\b", "exchange": r"\b[Ee]xchange\b", "credit": r"[Ss]tore credit"},
        subj=["Return for order {ref}", "Damaged item ({ref})", "Boots from order {ref}"],
        open=["I'm returning the rain jacket from order {ref}.", "The blender I bought ({ref}) arrived with a cracked jug.",
              "This is about the boots from order {ref} that don't fit."],
        who=["sister", "friend", "partner"], no_tried=set(),
        T={"final": ["I'd like {v}.", "Please process {v}.", "What I want is {v}."],
           "tried": ["I asked the store for {v}, but they said it isn't possible in store.", "I requested {v} at the counter, but the system wouldn't allow it."],
           "final_after_tried": ["Please process {v}; I asked the store for {w}, but they said it isn't possible in store."],
           "neg": ["I don't want {v}.", "Please don't give me {v}."],
           "quote": ['The clerk said, "You can get {v}."', 'My {who} told me, "Just ask for {v}."'],
           "own_despite_quote": ['I\'d like {v}, even though the clerk said, "You can get {w}."'],
           "consider": ["I'm wondering whether {v} would be better.", "Maybe {v}?"],
           "undecided": ["I haven't decided what I want yet.", "I'd like to know my options before choosing."],
           "ask": ["What are my options?", "What can you offer me for this?"],
           "change": ["I first asked for {a}, but I'd now prefer {b}.", "Please change my request from {a} to {b}."],
           "change_goldfirst": ["I'd now prefer {b} instead of {a}, which I asked for first."],
           "correction": ["Correction: I want {b}, not {a}."],
           "t_first": ["I'd like {v}, please.", "Please arrange {v}."],
           "t_change": ["Update: I'd prefer {v} instead.", "Change of plan: {v}, please."],
           "t_revert": ["Actually, {v} as I first asked.", "Sorry, going back to {v}."],
           "t_confirm": ["Confirming: {v}.", "Just confirming I want {v}."]},
        q=["What resolution does the customer want for the return?", "Which resolution did the customer finally ask for?",
           "Based on the customer's own final request, how should this return be resolved?"]),
    "delivery_option": dict(
        what="delivery option", noun="an option",
        opts={"home": "home delivery", "store": "store pickup", "locker": "parcel locker"},
        desc={"home": "delivery to the customer's home", "store": "pickup at a store", "locker": "pickup from a parcel locker"},
        surf={"home": ["home delivery"], "store": ["store pickup", "in-store pickup"], "locker": ["parcel locker pickup"]},
        rx={"home": r"[Hh]ome delivery", "store": r"[Ss]tore pickup", "locker": r"[Pp]arcel locker"},
        subj=["Order {ref}", "Desk chair order {ref}", "Delivery for {ref}"],
        open=["This is about my order {ref} (a desk chair).", "Regarding order {ref}.", "My order {ref} is ready to be sent out."],
        who=["roommate", "husband", "neighbor"], no_tried=set(),
        T={"final": ["I'll go with {v}.", "Please set the order to {v}.", "My choice is {v}."],
           "tried": ["I tried to choose {v} on the website, but it wasn't offered for this item.", "I picked {v} in the app, but it kept erroring."],
           "final_after_tried": ["My choice is {v}; I tried to choose {w} on the website, but it wasn't offered."],
           "neg": ["I don't want {v}.", "{V} won't work for me."],
           "quote": ['My {who} said, "Just pick {v}."', 'My {who} texted me: "{V} is easiest."'],
           "own_despite_quote": ['I\'ll go with {v}, even though my {who} said, "Just pick {w}."'],
           "consider": ["{V} might be easier.", "Maybe {v}?"],
           "undecided": ["I haven't decided how to receive it yet.", "I'll choose the delivery option later."],
           "ask": ["What delivery options do I have?", "How can I receive the order?"],
           "change": ["I had selected {a}, but please change it to {b}.", "Please switch the order from {a} to {b}."],
           "change_goldfirst": ["Please change it to {b}; I had selected {a} before."],
           "correction": ["Correction: I want {b}, not {a}."],
           "t_first": ["Please set it to {v}.", "I'd like {v}."],
           "t_change": ["Change of plan: {v} instead.", "Update: please switch to {v}."],
           "t_revert": ["Sorry, back to {v}.", "Actually, {v} as I first chose."],
           "t_confirm": ["Confirming {v}.", "Just confirming {v}."]},
        q=["How does the customer want to receive the order?", "Based on the writer's own final choice, which delivery option should be set?",
           "Which delivery option did the customer choose?"]),
    "seat": dict(
        what="seat preference", noun="a seat",
        opts={"window": "window", "aisle": "aisle", "middle": "middle"},
        desc={"window": "a window seat", "aisle": "an aisle seat", "middle": "a middle seat"},
        surf={"window": ["a window seat"], "aisle": ["an aisle seat"], "middle": ["a middle seat"]},
        rx={"window": r"[Ww]indow seat", "aisle": r"[Aa]isle seat", "middle": r"[Mm]iddle seat"},
        subj=["Seat request, booking {ref}", "Flight {ref}", "Return flight {ref}"],
        open=["I'm on flight {ref} next week.", "This is about booking {ref}.", "About my return flight, booking {ref}."],
        who=["travel agent", "colleague", "wife"], no_tried=set(),
        T={"final": ["Please give me {v}.", "I'd like {v}.", "Please assign me {v}."],
           "tried": ["I tried to select {v} in the app, but it showed as taken.", "I asked for {v} at the kiosk, but none were left then."],
           "final_after_tried": ["Please assign me {v}; I tried to select {w} in the app, but it showed as taken."],
           "neg": ["Please don't put me in {v}.", "I don't want {v}."],
           "quote": ['My {who} said, "Ask for {v}."', 'My {who} told me, "Get {v}, trust me."'],
           "own_despite_quote": ['I\'d like {v}, even though my {who} said, "Ask for {w}."'],
           "consider": ["{V} might be nice.", "Maybe {v}?"],
           "undecided": ["I haven't decided on a seat.", "I'll decide on my seat at check-in."],
           "ask": ["Which seats are still free?", "Can you tell me what seats are left?"],
           "change": ["I had asked for {a}, but I'd now prefer {b}.", "Please change my request from {a} to {b}."],
           "change_goldfirst": ["I'd now prefer {b} rather than {a}, which I asked for before."],
           "correction": ["Correction: I want {b}, not {a}."],
           "t_first": ["Please give me {v}.", "I'd like {v}, please."],
           "t_change": ["Update: I'd rather have {v}.", "Change of plan: {v}."],
           "t_revert": ["Sorry, {v} as originally requested.", "Actually, back to {v}."],
           "t_confirm": ["Confirming {v}.", "Just confirming {v}."]},
        q=["Which seat does the passenger want?", "Based on the passenger's own final request, which seat type should be assigned?",
           "What seat did the passenger ask for?"]),
    "appointment_format": dict(
        what="appointment format", noun="a format",
        opts={"inperson": "in person", "video": "video call", "phone": "phone call"},
        desc={"inperson": "an in-person visit", "video": "a video call", "phone": "a phone call"},
        surf={"inperson": ["an in-person visit", "an in-person appointment"], "video": ["a video call", "a video appointment"],
              "phone": ["a phone call", "a phone appointment"]},
        rx={"inperson": r"[Ii]n-person", "video": r"[Vv]ideo (call|appointment)", "phone": r"[Pp]hone (call|appointment)"},
        subj=["Follow-up booking {ref}", "Physio review {ref}", "Annual check-in {ref}"],
        open=["I need to book my follow-up with Dr. {lname} ({ref}).", "This is about my physiotherapy review {ref}.",
              "I'm scheduling my annual check-in {ref}."],
        who=["daughter", "husband", "carer"], no_tried=set(),
        T={"final": ["I'd like {v}.", "Please book it as {v}.", "Please make it {v}."],
           "tried": ["We tried {v} last time, but it didn't work well for me.", "I had {v} last year and it was hard to follow."],
           "final_after_tried": ["Please book it as {v}; we tried {w} last time and it didn't work well for me."],
           "neg": ["I don't want {v}.", "Please don't book {v}."],
           "quote": ['The receptionist said, "{V} is easiest."', 'My {who} said, "Just do {v}."'],
           "own_despite_quote": ['I\'d like {v}, even though the receptionist said, "{W} is easiest."'],
           "consider": ["{V} could work.", "Maybe {v}?"],
           "undecided": ["I haven't decided which format works best.", "I'll confirm the format later."],
           "ask": ["What appointment formats do you offer?", "Which formats are available?"],
           "change": ["I had booked {a}, but please change it to {b}.", "Please switch it from {a} to {b}."],
           "change_goldfirst": ["Please change it to {b}; I had booked {a}."],
           "correction": ["Correction: I want {b}, not {a}."],
           "t_first": ["Please book {v}.", "I'd like {v}."],
           "t_change": ["Change: I'd prefer {v}.", "Update: please make it {v}."],
           "t_revert": ["Sorry, back to {v}.", "Actually, {v} as first booked."],
           "t_confirm": ["Confirming {v}.", "Just confirming {v}."]},
        q=["Which appointment format does the patient want?", "Based on the patient's own final request, how should the appointment be held?",
           "What appointment format did the patient ask for?"]),
}

# roles of the mentions each sentence template makes (resolver input)
ROLE = {"final": lambda x: [(x["v"], "final")], "tried": lambda x: [(x["v"], "tried")],
        "final_after_tried": lambda x: [(x["v"], "final"), (x["w"], "tried")], "neg": lambda x: [(x["v"], "neg")],
        "quote": lambda x: [(x["v"], "quoted")], "own_despite_quote": lambda x: [(x["v"], "final"), (x["w"], "quoted")],
        "consider": lambda x: [(x["v"], "considered")], "undecided": lambda x: [], "ask": lambda x: [],
        "change": lambda x: [(x["a"], "superseded"), (x["b"], "final")], "change_goldfirst": lambda x: [(x["b"], "final"), (x["a"], "superseded")],
        "correction": lambda x: [(x["b"], "final"), (x["a"], "corrected")], "t_first": lambda x: [(x["v"], "final")],
        "t_change": lambda x: [(x["v"], "final")], "t_revert": lambda x: [(x["v"], "final")], "t_confirm": lambda x: [(x["v"], "final")],
        "t_retract": lambda x: [(None, "retract")]}

PATTERN_W = {"D": 1.0, "TRY": 1.2, "CHG": 1.0, "COR": 0.8, "NEGF": 1.0, "QO": 1.1, "CONS": 0.7, "THR": 1.2, "RET": 0.6}
THREAD = {"THR", "RET"}


def enum_sents(pat, A, B, order, twin):
    """Sentence plan (template key, slot values) and the construction gold. A is the base gold value where the base has one."""
    if pat == "D":
        return ([("final", {"v": A})], A) if not twin else ([("neg", {"v": A}), ("undecided", {})], NS)
    if pat in ("TRY", "CHG", "COR"):
        g, o = (A, B) if not twin else (B, A)
        if pat == "TRY":
            return ([("tried", {"v": o}), ("final", {"v": g})] if order == 0 else [("final_after_tried", {"v": g, "w": o})]), g
        if pat == "CHG":
            return ([("change", {"a": o, "b": g})] if order == 0 else [("change_goldfirst", {"a": o, "b": g})]), g
        return [("final", {"v": o}), ("correction", {"a": o, "b": g})], g
    if pat == "NEGF":
        x = ("final", {"v": A}) if not twin else ("undecided", {})
        return ([("neg", {"v": B}), x] if order == 0 else [x, ("neg", {"v": B})]), (A if not twin else NS)
    if pat == "QO":
        if twin:
            return [("quote", {"v": B}), ("undecided", {})], NS
        return ([("quote", {"v": B}), ("final", {"v": A})] if order == 0 else [("own_despite_quote", {"v": A, "w": B})]), A
    if pat == "CONS":
        return ([("consider", {"v": A}), ("ask", {})], NS) if not twin else ([("final", {"v": A})], A)
    if pat == "THR":
        if twin:
            return [("t_first", {"v": B}), ("t_change", {"v": A}), ("t_revert", {"v": B})], B
        return [("t_first", {"v": B}), ("t_change", {"v": A})] + ([("t_confirm", {"v": A})] if order == 1 else []), A
    if pat == "RET":
        return ([("t_first", {"v": A}), ("t_retract", {})], NS) if not twin else ([("t_first", {"v": A}), ("t_confirm", {"v": A})], A)
    raise ValueError(pat)


def resolve(seq):
    """Independent resolver: seq = [(time, mentions)]; the writer's choice is the latest 'final' mention; 'retract' clears it."""
    cur = None
    for _, ms in sorted(seq, key=lambda x: x[0]):
        fin = [v for v, r in ms if r == "final"]
        assert len(fin) <= 1
        if any(r == "retract" for _, r in ms):
            cur = None
        if fin:
            cur = fin[0]
    return cur if cur is not None else NS


def fill(F, S, tkey, vals):
    if tkey == "t_retract":
        return RETRACT[S["tidx"].setdefault(tkey, S["rng"].randrange(len(RETRACT)))]
    lst = F["T"][tkey]
    tpl = lst[S["tidx"].setdefault(tkey, S["rng"].randrange(len(lst)))]
    m = {k: S["surf"][v] for k, v in vals.items()}
    m.update({k.upper(): cap(x) for k, x in list(m.items())})
    m["who"] = S["who"]
    return tpl.format(**m)


def render_enum(F, S, plan, thread):
    """Render the message; returns (state, [(time, mentions)])."""
    seq = []
    name = S["writer"]["name"]
    opener = F["open"][S["open"]].format(ref=S["ref"], lname=S["lname"])
    if thread:
        lines = []
        for i, (tkey, vals) in enumerate(plan):
            txt = fill(F, S, tkey, vals)
            if i == 0:
                txt = opener + " " + txt
            t = S["times"][i]
            lines.append(f"[{t.strftime('%a %d %b, %H:%M')}] {txt}")
            seq.append((t, ROLE[tkey](vals)))
        order = "newest first" if S["newest"] else "oldest first"
        if S["newest"]:
            lines = lines[::-1]
        return f"Messages from {name} about {S['ref']} ({order}):\n" + "\n".join(lines), seq
    body = []
    for i, (tkey, vals) in enumerate(plan):
        body.append(fill(F, S, tkey, vals))
        seq.append((i, ROLE[tkey](vals)))
    text = opener + " " + " ".join(body)
    fmt = S["fmt"]
    if fmt == "email":
        subj = F["subj"][S["open"] % len(F["subj"])].format(ref=S["ref"])  # subject matches the opener
        greet = ["Hi,", "Hello,", "Good afternoon,", "Dear team,"][S["greet"]]
        sign = ["Thanks,", "Best regards,", "Cheers,", "Kind regards,"][S["sign"]]
        return f"Subject: {subj}\n\n{greet}\n\n{text}\n\n{sign}\n{name}", seq
    if fmt == "chat":
        return f"Live chat, customer {name}: {['Hi!', 'Hello there.', 'Hey there.'][S['greet'] % 3]} {text}", seq
    return f"Web form submission\nName: {name}\nReference: {S['ref']}\nMessage: {text}", seq


def mention_spans(F, text):
    out = []
    for v, rx in F["rx"].items():
        for m in re.finditer(rx, text):
            out.append((m.start(), v))
    return sorted(out)


def enum_defs(F):
    d = {}
    for v, lab in F["opts"].items():
        d[lab] = (f"The writer's own last stated {F['what']} is {F['desc'][v]}; {F['noun']} only tried, ruled out, later changed, quoted "
                  f"from someone else or merely considered does not count.")
    d[NS] = (f"The writer never settles on a {F['what']} of their own: they only ask, rule options out, quote someone else, consider "
             f"options, or withdraw an earlier choice without naming a new one.")
    return d


def make_enum_pair(fname, pat, A, B, rng, idx):
    F = FIELDS[fname]
    writer = person(rng)
    t0 = rdt(rng, 7, 12)
    times = [t0]
    for _ in range(3):
        times.append(times[-1] + timedelta(minutes=rng.randrange(25, 1500)))
    S = dict(rng=random.Random(rng.randrange(2 ** 31)), tidx={}, writer=writer, lname=rng.choice(LAST),
             ref=rng.choice(["#", "No. ", ""]) + str(rng.randrange(10000, 99999)) if fname != "seat" else f"{rng.choice('BCDFHJKLMNPQRSTVWXZ')}{rng.choice('BCDFHJKLMNPQRSTVWXZ')}{rng.randrange(1000, 9999)}",
             open=rng.randrange(len(F["open"])), subj=rng.randrange(len(F["subj"])), greet=rng.randrange(4), sign=rng.randrange(4),
             fmt=rng.choice(["email", "email", "chat", "form"]), who=rng.choice(F["who"]),
             surf={v: rng.choice(s) for v, s in F["surf"].items()}, times=times, newest=rng.random() < 0.5)
    order = rng.randrange(2)
    options = [F["opts"][v] for v in F["opts"]] + [NS]
    rng.shuffle(options)  # 'not stated' is not always last
    qv = rng.randrange(len(F["q"]))
    rows = []
    rid0 = f"{KEY}-enum-{fname}-{idx:04d}"
    golds = []
    for j in range(2):
        plan, g = enum_sents(pat, A, B, order, twin=j == 1)
        state, seq = render_enum(F, S, plan, pat in THREAD)
        # --- self-check 1: construction gold == independent resolver over the role-tagged mentions
        assert resolve(seq) == g, (fname, pat, j, resolve(seq), g)
        # --- self-check 2: the text mentions exactly the option values the plan mentions (no stray / missing mentions)
        want = {v for _, ms in seq for v, _ in ms if v is not None}
        got = {v for _, v in mention_spans(F, state)}
        assert got == want, (fname, pat, j, got, want, state)
        assert g == NS or g in got
        gold = F["opts"][g] if g != NS else NS
        assert gold in options
        sp = mention_spans(F, state)
        pos = {"first": sp[0][1] if sp else None, "last": sp[-1][1] if sp else None}
        edges = {"D": [] if j == 0 else ["negation", "missing_info"], "TRY": ["temporal"], "CHG": ["temporal"], "COR": ["conflicting_evidence"],
                 "NEGF": ["negation"] + (["missing_info"] if j == 1 else []), "QO": ["reported_speech"] + (["missing_info"] if j == 1 else []),
                 "CONS": ["hypothetical", "missing_info"] if j == 0 else [], "THR": ["temporal", "conflicting_evidence"],
                 "RET": ["temporal", "missing_info"] if j == 0 else ["temporal"]}[pat]
        meta = {"dataset": f"program generator golden_src/gen/{KEY}.py", "config": f"enum:{fname}:{pat}", "revision": None,
                "licence": LICENCE, "split": "train",
                "orig_label": {"field": fname, "pattern": pat, "value": g, "mentions": [[str(t), v, r] for t, ms in seq for v, r in ms],
                               "first_mentioned": pos["first"], "last_mentioned": pos["last"],
                               **({"changed": "decisive statement changed so the writer's final choice differs"} if j == 1 else {})},
                "family": FAMILY, "edge": ",".join(edges) or None, "defs": f"enum_{fname}"}
        if j == 1:
            meta["twin_of"] = rid0
        rows.append({"key": KEY, "rid": rid0 if j == 0 else rid0 + "-twin", "state": state, "instructions": F["q"][qv],
                     "options": list(options), "gold": gold, "soft": None, "meta": meta})
        golds.append(g)
    assert golds[0] != golds[1] and rows[0]["state"] != rows[1]["state"]
    return rows


# =============================================================================================== main
def _key_of(ln):
    try:
        return json.loads(ln).get("key") if ln.strip() else None
    except Exception:  # noqa: BLE001
        return None


def upsert_manifest(rec):
    """New key -> one O_APPEND write (other builders append concurrently); re-run -> replace our own line under a lock."""
    line = json.dumps(rec, ensure_ascii=False)
    MANIFEST.touch(exist_ok=True)
    with open(MANIFEST, "r+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        text = f.read()
        lines = text.splitlines()
        if not any(_key_of(ln) == rec["key"] for ln in lines):
            f.seek(0, os.SEEK_END)
            f.write(("" if text.endswith("\n") or not text else "\n") + line + "\n")
        else:
            keep = [ln for ln in lines if _key_of(ln) != rec["key"]] + [line]
            f.seek(0)
            f.write("\n".join(keep) + "\n")
            f.truncate()
        fcntl.flock(f, fcntl.LOCK_UN)


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    rows, seen_k, seen_s = [], set(), set()
    stats = collections.Counter()

    def add(pr):
        ks = [norm(r["state"]) + "||" + norm(r["instructions"]) for r in pr]
        ss = [norm(r["state"]) for r in pr]
        if any(k in seen_k for k in ks) or any(s in seen_s for s in ss) or ss[0] == ss[1]:
            stats["dup"] += 1
            return False
        seen_k.update(ks)
        seen_s.update(ss)
        rows.extend(pr)
        return True

    # ---- (a) JSON decisions: pairs spread evenly over the templates; base truth alternates, cases cycle
    nT = len(JSON_TEMPLATES)
    quota = [N_JSON_PAIRS // nT + (1 if i < N_JSON_PAIRS % nT else 0) for i in range(nT)]
    idx = 0
    for ti, T in enumerate(JSON_TEMPLATES):
        made, tries = 0, 0
        cu = collections.Counter()
        while made < quota[ti]:
            tries += 1
            assert tries < 400, (T.name, made)
            cases = T.yes_cases if made % 2 == 0 else T.no_cases
            case = min(cases, key=lambda c: (cu[c], rng.random()))
            pr = make_json_pair(T, case, rng, idx, cu)
            if pr is None:
                stats["noflip:" + T.name] += 1
                continue
            if add(pr):
                made += 1
                idx += 1
                stats["json:" + T.name] += 1
                for r in pr:
                    cu[r["meta"]["orig_label"]["case"]] += 1

    # ---- (b) enum extraction: fields round-robin, patterns cycle per field, base gold value = least used so far
    fnames = list(FIELDS)
    fquota = {f: N_ENUM_PAIRS // len(fnames) + (1 if i < N_ENUM_PAIRS % len(fnames) else 0) for i, f in enumerate(fnames)}
    used = {f: collections.Counter() for f in fnames}
    pats = {}
    for f in fnames:
        allowed = [p for p in PATTERN_W if p not in FIELDS[f].get("skip", set())]
        seq, cur = [], {p: 0.0 for p in allowed}  # smooth weighted round-robin, rotated per field
        tot = sum(PATTERN_W[p] for p in allowed)
        rot = random.Random(f"{SEED}:{f}").randrange(len(allowed))
        allowed = allowed[rot:] + allowed[:rot]
        while len(seq) < fquota[f] + 20:
            for p in allowed:
                cur[p] += PATTERN_W[p]
            best = max(allowed, key=lambda p: cur[p])
            cur[best] -= tot
            seq.append(best)
        pats[f] = seq
    for f in fnames:
        made, k = 0, 0
        vals = list(FIELDS[f]["opts"])
        while made < fquota[f]:
            pat = pats[f][k]
            k += 1
            A = min(vals, key=lambda v: (used[f][v], rng.random()))
            others = [v for v in vals if v != A]
            if pat == "TRY":
                # the failed attempt must be a plausible thing to try, and after the swap in the twin, so must A
                others = [v for v in others if v not in FIELDS[f]["no_tried"]]
                if A in FIELDS[f]["no_tried"]:
                    A = rng.choice([v for v in vals if v not in FIELDS[f]["no_tried"]])
                    others = [v for v in vals if v != A and v not in FIELDS[f]["no_tried"]]
            B = rng.choice(others)
            pr = make_enum_pair(f, pat, A, B, rng, idx)
            if add(pr):
                made += 1
                idx += 1
                for r in pr:
                    v = r["meta"]["orig_label"]["value"]
                    if v != NS:
                        used[f][v] += 1
                stats["enum:" + f + ":" + pat] += 1

    assert len(rows) <= MAX_ROWS, len(rows)
    # ---- whole-file checks
    for r in rows:
        assert set(r) == {"key", "rid", "state", "instructions", "options", "gold", "soft", "meta"}
        assert r["gold"] in r["options"] and r["state"].strip() and r["instructions"].strip()
        e = r["meta"]["edge"]
        assert e is None or all(x in EDGE_TAGS for x in e.split(",")), e
    rids = [r["rid"] for r in rows]
    assert len(set(rids)) == len(rids)
    by = {r["rid"]: r for r in rows}
    for r in rows:
        if "twin_of" in r["meta"]:
            b = by[r["meta"]["twin_of"]]
            assert b["gold"] != r["gold"] and b["instructions"] == r["instructions"] and b["options"] == r["options"]

    src = Path(__file__).resolve()
    rev = "gen-v1+sha256:" + hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    for r in rows:
        r["meta"]["revision"] = rev
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{KEY}.jsonl"
    with open(out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    back = [json.loads(x) for x in open(out, encoding="utf-8")]
    assert back == rows

    # ---- defs
    DEFS_DIR.mkdir(parents=True, exist_ok=True)
    used_q = {r["meta"]["defs"] for r in rows}
    written = []
    for T in JSON_TEMPLATES:
        for qid, d in ((T.name, T.defs_pos), (T.name + "_neg", T.defs_neg)):
            if qid in used_q:
                assert set(d) == {"yes", "no"}
                for k2, v in d.items():
                    assert len(v.split()) <= 48, (qid, k2, len(v.split()))
                (DEFS_DIR / f"{KEY}__{qid}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
                written.append(qid)
    for f, F in FIELDS.items():
        d = enum_defs(F)
        for k2, v in d.items():
            assert len(v.split()) <= 48, (f, k2, len(v.split()))
        qrows = [r for r in rows if r["meta"]["defs"] == f"enum_{f}"]
        assert all(set(r["options"]) == set(d) for r in qrows)
        (DEFS_DIR / f"{KEY}__enum_{f}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        written.append(f"enum_{f}")
    assert used_q <= set(written), used_q - set(written)

    # ---- summary
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    ch = [r for r in rows if r["options"] != ["yes", "no"]]
    ysh = round(sum(r["gold"] == "yes" for r in yn) / len(yn), 4)
    print(f"rows {len(rows)} | json yes/no {len(yn)} (yes share {ysh}) | enum choice {len(ch)} | {time.time() - t0:.1f}s")
    print("json by template:", dict(collections.Counter(r["meta"]["orig_label"]["template"] for r in yn)))
    print("json neg-polarity rows:", sum(r["meta"]["orig_label"]["polarity"] == "neg" for r in yn))
    print("json cases:", dict(collections.Counter(r["meta"]["config"].split(":", 1)[1] for r in yn)))
    gch = collections.Counter(r["gold"] for r in ch)
    print("enum gold:", dict(gch.most_common()), "max share", round(max(gch.values()) / len(ch), 3), "NS share", round(gch[NS] / len(ch), 3))
    print("enum by field/gold:", {f: dict(collections.Counter(r["gold"] for r in ch if r["meta"]["orig_label"]["field"] == f)) for f in FIELDS})
    print("enum patterns:", dict(collections.Counter(r["meta"]["orig_label"]["pattern"] for r in ch)))
    val = [r for r in ch if r["meta"]["orig_label"]["value"] != NS]
    lastm = sum(r["meta"]["orig_label"]["last_mentioned"] == r["meta"]["orig_label"]["value"] for r in val) / len(val)
    firstm = sum(r["meta"]["orig_label"]["first_mentioned"] == r["meta"]["orig_label"]["value"] for r in val) / len(val)
    print(f"enum gold == last-mentioned value: {lastm:.3f}; == first-mentioned: {firstm:.3f} (over {len(val)} rows with a value)")
    edges = collections.Counter(x for r in rows for x in (r["meta"]["edge"] or "").split(",") if x)
    print("edges:", dict(edges.most_common()))
    L = sorted(len(r["state"]) for r in rows)
    print("state chars min/med/max:", L[0], L[len(L) // 2], L[-1])
    print("stats:", {k: v for k, v in stats.items() if not k.startswith(("json:", "enum:"))})
    n_tpl = len(JSON_TEMPLATES) + sum(len(F["T"]) for F in FIELDS.values())
    if os.environ.get("GEN2_NO_MANIFEST"):
        return
    upsert_manifest({
        "key": KEY, "family": FAMILY, "dataset": f"{KEY} (program generator, golden_src/gen/{KEY}.py)", "licence": LICENCE,
        "rows": len(rows), "qtype": "yesno (JSON-record decisions, 21 templates, pos + neg polarity) + choice (enum field extraction, "
                                    "11 fields, each with an explicit 'not stated' option)",
        "yesno_share": ysh, "edge_tags": sorted(edges),
        "notes": (f"Gap-fill generator (29 Sep audit: structured-record decisions and field extraction). (a) {len(yn)} yes/no rows: "
                  f"decisions over JSON records (orders, insurance claims, support tickets, access logs, shipments, patient "
                  f"appointments) under a short rule given as a Policy line or inside the question; traps: look-alike keys "
                  f"(billing vs shipping address, requested_roles vs roles, requested_priority vs priority, previous_plan vs plan, "
                  f"claimed vs assessed loss, dimensional vs actual weight, exchange vs return window, pending vs granted zones, "
                  f"cancelled vs active lab tests, emergency-contact vs patient phone, return_to vs ship_to, estimated vs promised "
                  f"date, renewal quote vs current term), null / missing fields, all / any / count over arrays, nested objects, "
                  f"units in field names (cents vs dollars, minutes vs hours, g / kg / lb), exact-threshold boundaries, and "
                  f"histories where the latest timestamp wins even when listed newest-first or shuffled; yes share {ysh}; 30% "
                  f"opposite-polarity questions with their own cards. (b) {len(ch)} choice rows: enum extraction from emails, chats, "
                  f"web forms and timestamped threads (payment method, currency, carrier, contact channel, language, ticket "
                  f"priority, account type, refund/exchange/store credit, delivery option, seat, appointment format) with "
                  f"corrections, failed attempts, changes of mind, negation, quoted suggestions from others, merely considered "
                  f"options, newest-first threads and withdrawn choices; gold = the writer's own last stated choice or 'not "
                  f"stated' ({gch[NS]} rows). {n_tpl} Claude-written templates. Every base row has a fact-flip twin "
                  f"(meta.twin_of) with a different gold. Self-check: (a) case, latent-parameter truth and an independent rule "
                  f"evaluator over the JSON re-parsed from the rendered state agree on every row; (b) construction gold equals an "
                  f"independent resolver over role-tagged mentions and a lexical scan finds exactly the planned option mentions. "
                  f"gen2_* rows are added on top of the target by build_v14_golden.py (no bundles, attack twins or defswaps).")})
    print("manifest updated")


if __name__ == "__main__":
    main()
