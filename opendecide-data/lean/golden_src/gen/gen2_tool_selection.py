"""gen2_tool_selection: tool / function selection for an assistant that has a tool catalog (multiple choice, labels
exact by construction, fact-flip twins).  Gap-fill generator (29 Sep audit): no source in the golden set asks for the
single right tool call, a clarifying question, or a refusal under stated permissions.

Each row is one conversation turn of an assistant deployed with
  * a TOOL CATALOG of 5-12 tools, given as the definitions (card): each tool's purpose, required parameters,
    optional parameters and usage restriction ("only when <session field> is ...", "not available when ...",
    "<param> must be at most <limit>", "for environment production, only when ...", "only for the requester's own
    username unless role is ...", "not for bookings on a Basic fare"), plus two meta-actions:
    ask_clarifying_question and refuse_not_allowed;
  * the STATE: the deployment rules (one call per turn; argument values only from the conversation or the session
    details, never guessed or fetched with another tool; tool names mentioned by users are hints only; the
    multi-request priority rule; sometimes a tool switched off for this deployment), the session details (role,
    account status, verification, lists such as saved payees, bookings on file, recent card activity, upcoming
    events, assigned devices) and the user's message(s) (chat, email, voice note, team chat).
7 domains: online-shop customer support, retail banking app, travel booking, workplace calendar/email/docs,
internal IT help desk, cloud-operations chat bot, smart-home voice assistant (58 tools, 44 request types).

Labels are exact by construction:
  * the request acted on = the only request, or the one picked by the stated priority rule (first request still
    wanted / the one the user explicitly marks most urgent / tool tiers named in the rule; requests the user says are
    done or withdrawn do not count);
  * M = catalog tools that fit that request (fit is declared per request type and decided by one stated fact, e.g.
    misplaced vs stolen card, own account vs someone else, logs vs metrics, now vs every night, or by an amount above
    a stated limit for a fallback tool);  A = tools in M not barred for this session (own restriction or a
    deployment rule);  gold = refuse_not_allowed if M is non-empty and A is empty; else the unique tool in A whose
    required values are all stated (in the message, or in the session details: 'my landlord' -> the saved payee
    marked landlord, 'this order' -> the order on screen); else ask_clarifying_question.  A tool in A with all its
    values is unique by construction (generation rejects any state where two would qualify, where a restriction
    depends on a missing value, or where a catalog tool could look the missing value up).
  * traps: look-alike tools (get_order_status vs track_package vs search_orders, freeze_card vs report_card_stolen,
    get_balance vs list_transactions, create_event vs set_reminder vs find_free_slots, reset_password vs
    unlock_account, get_logs vs get_metrics ...), multi-request messages resolved by the stated priority rule
    (including 'most urgent' markers that the first-request rule ignores, and withdrawn / already-done requests),
    requests that NAME a tool but need another, fallback tools that fit only above a limit (boundary = allowed),
    vague references ('my card' with two cards on file, 'my booking' with two bookings) vs session-resolved ones,
    optional parameters that never require asking, restriction checked before missing values.
  * every base row has a fact-flip twin (meta.twin_of) that changes one decisive fact (a session field, one value,
    which request is first / marked urgent / withdrawn, the reason in the message, which tool is switched off) so the
    gold changes; twins share catalog, definitions, instruction and every surface choice.
Self-check: every row is recomputed by an independent evaluator that parses the RENDERED text: required parameters
and restrictions from the definition strings, the priority rule, tiers and switched-off tools from the rules block,
session fields from the session block, and checks that every value counted as stated appears in the conversation
(or in the matching session entry) and that no value of a missing parameter's kind appears anywhere in the
conversation.  Deterministic (seed 20260929), CPU only, no model calls, no third-party text.
"""
import collections
import copy
import datetime as dt
import hashlib
import json
import os
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "moral_social_norms"))
from common import EDGE_TAGS, check_rows, edge_tags, norm, write_defs  # noqa: E402

KEY = "gen2_tool_selection"
SEED = 20260929
FAMILY = "routing_dialogue"
MAX_ROWS = 330
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
ASK = "ask_clarifying_question"
REF = "refuse_not_allowed"
SPECIAL_DEFS = {
    ASK: ("Ask the user one clarifying question instead of calling a tool: every permitted tool that fits the request "
          "being acted on lacks a required value that the messages and session details do not state exactly (vague "
          "references do not count)."),
    REF: ("Decline the request: every tool that fits the request being acted on is barred for this user or session, "
          "by its own restriction or by the assistant rules; this check comes before any check for missing values."),
}


class Invalid(Exception):
    pass


def cap(s):
    return s[:1].upper() + s[1:]


def join_or(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " or " + xs[-1]


def split_or(s):
    parts = re.split(r", | or ", s)
    return [p.strip() for p in parts if p.strip()]


def num_of(s):
    m = re.search(r"\d[\d,]*", str(s))
    return int(m.group(0).replace(",", "")) if m else None


FIRST = ["Aisha", "Ben", "Carmen", "Dmitri", "Elena", "Farid", "Grace", "Hiro", "Ines", "Jonah", "Kavya", "Liam", "Maya",
         "Nikhil", "Olga", "Pedro", "Quinn", "Rosa", "Samir", "Tessa", "Umar", "Vera", "Wen", "Yusuf", "Zoe", "Priya",
         "Tomasz", "Leila", "Marcus", "Hannah", "Kofi", "Anneke", "Rafael", "Sunita", "Declan", "Mei"]
LAST = ["Okafor", "Lindqvist", "Moreau", "Tanaka", "Ruiz", "Chen", "Novak", "Haddad", "Brennan", "Kowalski", "Mensah",
        "Ferreira", "Nair", "Osei", "Petrov", "Quintero", "Sato", "Walsh", "Yilmaz", "Abara", "Delgado", "Fischer"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DATE_RE = r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b"
TIME_RE = r"\b\d{1,2}(?::\d{2})? ?(?:am|pm)\b|\b\d{1,2}:\d{2}\b|\btomorrow\b"


def fday(d, wd=True):
    s = f"{d.day} {MON[d.month - 1]}"
    return f"{WEEKDAYS[d.weekday()]} {s}" if wd else s


def ftoday(d):
    return f"{WEEKDAYS[d.weekday()][:3]} {d.day} {MON[d.month - 1]} {d.year}"


def money(n):
    return f"${n:,}"


# =============================================================================================== model objects
class CtxField:
    """A session field holds the value ('order on screen: W1234567'), or the none text."""
    kind = "field"

    def __init__(self, field, desc, fmt="{v}", none="none"):
        self.field, self.desc, self.fmt, self.none = field, desc, fmt, none


class CtxList:
    """A session list holds entries; the user refers to one entry by a descriptor built from its key."""
    kind = "list"

    def __init__(self, field, entry, desc, always=True):
        self.field, self.entry, self.desc, self.always = field, entry, desc, always


class CtxSelf:
    """The requester's own account: the value is in the session's requester line."""
    kind = "self"

    def __init__(self, field, desc):
        self.field, self.desc = field, desc


class Param:
    def __init__(self, name, gen, np=("{v}",), vague=(), regex=None, vocab=None, ctx=None, silent=False,
                 can_omit=False, gloss=None, provided=("present",)):
        self.name, self.gen, self.np, self.vague, self.regex, self.vocab = name, gen, list(np), list(vague), regex, vocab
        self.ctx, self.silent, self.can_omit, self.gloss = ctx, silent, can_omit, gloss
        self.provided = list(provided)

    def found(self, text, extra=()):
        if self.regex and re.search(self.regex, text):
            return True
        low = text.lower()
        for v in list(self.vocab or ()) + [x for x in extra if x]:
            if str(v).lower() in low:
                return True
        return False


class Rs:
    """One restriction clause.  kinds: allow / deny (session field), max (param <= limit key), self_or_role, fare,
    ifp (condition on a param value, wrapping another clause)."""

    def __init__(self, kind, field=None, values=(), param=None, lim=None, fmt=None, roles=(), inner=None, pval=None):
        self.kind, self.field, self.values, self.param, self.lim, self.fmt = kind, field, list(values), param, lim, fmt
        self.roles, self.inner, self.pval = list(roles), inner, pval

    def text(self, W):
        k = self.kind
        if k == "allow":
            return f"only when {self.field} is {join_or(self.values)}"
        if k == "deny":
            return f"not available when {self.field} is {join_or(self.values)}"
        if k == "max":
            return f"{self.param} must be at most {self.fmt(W['limits'][self.lim])}"
        if k == "self_or_role":
            return f"only for the requester's own username unless role is {join_or(self.roles)}"
        if k == "fare":
            return f"not for bookings on a {join_or(self.values)} fare (see bookings on file)"
        if k == "ifp":
            return f"for {self.param} {self.pval}, {self.inner.text(W)}"
        raise ValueError(k)

    def blocked(self, D, W, t):
        k = self.kind
        if k == "allow":
            return W["sess"][self.field] not in self.values
        if k == "deny":
            return W["sess"][self.field] in self.values
        if k == "max":
            if not has(D, t, self.param):
                raise Invalid("max restriction on a missing value")
            return t["ps"][self.param]["num"] > W["limits"][self.lim]
        if k == "self_or_role":
            if not has(D, t, self.param):
                raise Invalid("self_or_role on a missing value")
            return t["ps"][self.param]["value"] != W["requester_user"] and W["sess"]["role"] not in self.roles
        if k == "fare":
            if not has(D, t, self.param):
                raise Invalid("fare restriction on a missing booking")
            e = find_entry(W, "bookings on file", t["ps"][self.param]["value"])
            if e is None:
                raise Invalid("booking not on file")
            return e["attrs"]["fare"] in self.values
        if k == "ifp":
            if not has(D, t, self.param):
                raise Invalid("ifp on a missing value")
            if t["ps"][self.param]["value"] != self.pval:
                return False
            return self.inner.blocked(D, W, t)
        raise ValueError(k)


class Tool:
    def __init__(self, name, desc, req, opt=(), restr=(), fallback_of=None):
        self.name, self.desc, self.req, self.opt, self.restr = name, desc, list(req), list(opt), list(restr)
        self.fallback_of = fallback_of


class Intent:
    def __init__(self, name, fits, params, q, vp, facts=None, phrases=None, rel=None, extras=None, implicit=None, excl=None):
        self.name, self.fits, self.params, self.q, self.vp = name, fits, params, q, vp
        self.excl = excl
        self.facts = facts or {}
        self.phrases = phrases or {}
        self.rel = rel
        self.extras = extras
        self.implicit = implicit


class Dom:
    def __init__(self, name):
        self.name = name
        self.params, self.tools, self.intents = {}, {}, {}
        self.tiers, self.lookups, self.sess_order, self.values = [], {}, [], {}
        self.fillers, self.list_min = {}, {}
        self.orgs, self.layouts, self.user_label, self.assistant = [], [], "User", ""
        self.init = None
        self.fb = []  # (intent, fact dict, param, limit key, primary, fallback)

    def P(self, *a, **k):
        p = Param(*a, **k)
        self.params[p.name] = p

    def T(self, *a, **k):
        t = Tool(*a, **k)
        self.tools[t.name] = t

    def I(self, *a, **k):
        i = Intent(*a, **k)
        self.intents[i.name] = i


def find_entry(W, field, value):
    for e in W["lists"].get(field, []):
        if e["value"] == value:
            return e
    return None


def person(rng, used=None):
    for _ in range(100):
        f, l = rng.choice(FIRST), rng.choice(LAST)
        if used is None or (f"{f} {l}" not in used and f not in {u.split()[0] for u in used}):
            if used is not None:
                used.add(f"{f} {l}")
            return f, l
    raise Invalid("names")


def rid_chars(rng, n):
    for _ in range(50):
        s = "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(n))
        if re.search(r"\d", s) and re.search(r"[A-Z]", s):
            return s
    raise Invalid("ref")


# =============================================================================================== domains
def dom_retail():
    D = Dom("retail")
    D.orgs = ["Harbor & Pine", "Kestrel Outdoor", "Lumen & Loom", "Brightwell Kitchen"]
    D.assistant = "the customer-support assistant of {org}, an online shop"
    D.user_label, D.layouts = "Customer", ["chat", "chat2", "email", "voice"]
    PRODUCTS = ["walnut serving board", "linen duvet cover", "ceramic table lamp", "cast-iron skillet", "wool throw",
                "stoneware mug set", "bamboo bath mat", "brass floor lamp", "rattan laundry basket", "glass cake stand"]
    STREETS = ["Alder", "Mill", "Harcourt", "Juniper", "Station", "Quarry", "Orchard", "Beacon"]
    CITIES = ["Leeds LS6 2QT", "Bristol BS3 4LP", "York YO10 5DD", "Norwich NR2 3AB", "Exeter EX4 6PX"]
    D.P("order_id", lambda r, W, t: {"value": f"{r.choice('WKLB')}{r.randint(1000000, 9999999)}"},
        np=["order {v}", "order #{v}", "order number {v}"], vague=["my order", "my latest order", "the order I placed last week"],
        regex=r"\b[A-Z]\d{7}\b", can_omit=True, provided=["present", "present", "ctx"],
        ctx=CtxField("order on screen", ["this order", "the order I have open", "the order on my screen"]))
    D.P("tracking_number", lambda r, W, t: {"value": "1Z" + "".join(r.choice("ABCDEFGHJKLMNPRSTUVWXY0123456789") for _ in range(6))
                                            + "".join(r.choice("0123456789") for _ in range(10))},
        np=["the parcel with tracking number {v}", "tracking number {v}"], vague=["my parcel"], regex=r"\b1Z[0-9A-Z]{16}\b",
        can_omit=True, gloss="the carrier's")
    D.P("item_name", lambda r, W, t: {"value": r.choice(PRODUCTS)}, np=["the {v}", "the {v} I bought"],
        vague=["one of the items", "something I bought"], vocab=PRODUCTS)
    D.P("new_address", lambda r, W, t: {"value": f"{r.randint(2, 98)} {r.choice(STREETS)} {r.choice(['Road', 'Street', 'Lane', 'Avenue'])}, {r.choice(CITIES)}"},
        np=["{v}"], vague=["my new address", "my work address", "my sister's place"],
        regex=r"\b\d+ [A-Z][a-z]+ (?:Road|Street|Lane|Avenue)\b", can_omit=True)
    D.P("new_email", lambda r, W, t: {"value": f"{W['names']['first'].lower()}.{W['names']['last'].lower()}{r.randint(2, 98)}@{r.choice(['mailbox.example', 'post.example', 'inbox.example'])}"},
        np=["{v}"], vague=["my new work email", "my other email address"], regex=r"[\w.]+@[\w.]+")
    D.P("gift_card_number", lambda r, W, t: {"value": " ".join(f"{r.randint(0, 9999):04d}" for _ in range(4))},
        np=["gift card {v}", "the gift card numbered {v}"], vague=["the gift card my aunt gave me", "my gift card"],
        regex=r"\b\d{4} \d{4} \d{4} \d{4}\b")
    D.P("customer_id", lambda r, W, t: {"value": W["customer_id"]}, silent=True,
        ctx=CtxField("customer", [], fmt="{name} (customer ID {v})"))
    pay_hold = [Rs("deny", field="account status", values=["payment hold"])]
    ident = [Rs("allow", field="identity check", values=["passed"])]
    D.T("get_order_status", "returns the current status and expected delivery date of one order.", ["order_id"])
    D.T("track_package", "returns the carrier's latest scan and location for one parcel; it takes the carrier's tracking "
        "number, not an order number.", ["tracking_number"])
    D.T("search_orders", "lists the signed-in customer's orders (number, date, total), optionally for a date range; it "
        "shows no delivery progress.", ["customer_id"], opt=["date_from", "date_to"])
    D.T("cancel_order", "cancels a whole order that has not shipped yet.", ["order_id"], restr=pay_hold)
    D.T("change_delivery_address", "changes where one not-yet-shipped order will be delivered.", ["order_id", "new_address"],
        restr=pay_hold)
    D.T("start_return", "opens a return for an item the customer no longer wants (not for broken or damaged items) and "
        "emails a prepaid label.", ["order_id", "item_name"])
    D.T("report_damaged_item", "records an item that arrived broken or damaged and ships a free replacement.",
        ["order_id", "item_name"])
    D.T("update_account_email", "changes the email address on the signed-in customer's account.",
        ["customer_id", "new_email"], restr=ident)
    D.T("check_gift_card_balance", "returns the remaining balance of one gift card.", ["gift_card_number"])
    D.T("delete_account", "permanently deletes the signed-in customer's account and order history.", ["customer_id"],
        restr=ident)
    D.lookups = {"order_id": ["search_orders"]}
    wk = lambda r, W, t: {"weekday": WEEKDAYS[(W["today"].weekday() - r.randint(1, 3)) % 7],
                          "month": MONTHS[(W["today"].month - r.randint(3, 7)) % 12]}
    D.I("where_is", [("get_order_status", None), ("track_package", None)], ["order_id", "tracking_number"],
        q=["Where is <order_id> right now?", "Any news on <order_id>? It was due on {x:weekday} and still isn't here.",
           "<^order_id> hasn't arrived yet. Where is it?", "Where's my parcel?[ The order number is {v:order_id}.]",
           "Can you check where <tracking_number> has got to?",
           "My parcel still hasn't come.[ The tracking number is {v:tracking_number}.] Where is it now?"],
        vp=["check where <order_id> is", "find out where <tracking_number> has got to"], extras=wk,
        excl=["order_id", "tracking_number"])
    D.I("list_orders", [("search_orders", None)], ["customer_id"],
        q=["Can you pull up a list of everything I've ordered since {x:month}?",
           "I need a list of all my orders this year for my budget spreadsheet.", "Could you show me my full order history?"],
        vp=["list everything I've ordered since {x:month}", "pull up my full order history"], extras=wk)
    D.I("cancel", [("cancel_order", None)], ["order_id"],
        q=["Please cancel <order_id>; I picked the wrong size.", "I'd like to cancel <order_id> before it ships.",
           "Can you cancel <order_id>? I found it cheaper elsewhere."], vp=["cancel <order_id>"])
    D.I("change_address", [("change_delivery_address", None)], ["order_id", "new_address"],
        q=["Can you send <order_id> to <new_address> instead?",
           "I've just moved. Please change the delivery address on <order_id>[ to {v:new_address}].",
           "Could <order_id> be delivered to <new_address> rather than my old flat?"],
        vp=["send <order_id> to <new_address> instead"])
    D.I("sort_item", [("start_return", ("fact", "reason", "unwanted")), ("report_damaged_item", ("fact", "reason", "damaged"))],
        ["order_id", "item_name"], facts={"reason": ["unwanted", "damaged"]},
        phrases={"reason": {"unwanted": ["I've changed my mind about it", "the colour clashes with everything in the room",
                                         "it's far too big for the space I had in mind", "I ordered two by mistake and only need one"],
                            "damaged": ["it arrived cracked", "it arrived broken in the box", "it was badly dented when I unpacked it",
                                        "it was in pieces when I opened the box"]}},
        q=["About <item_name> from <order_id>: {f:reason}. What can you do?",
           "<^item_name> from <order_id> - {f:reason}. Can you sort it out?",
           "I need help with <item_name> in <order_id>: {f:reason}."],
        vp=["sort out <item_name> from <order_id>"])
    D.I("change_email", [("update_account_email", None)], ["customer_id", "new_email"],
        q=["Please change the email on my account to <new_email>.",
           "I've lost access to my old inbox - can you switch my account email to <new_email>?",
           "Update my contact email to <new_email>, please."], vp=["change my account email to <new_email>"])
    D.I("gift_card", [("check_gift_card_balance", None)], ["gift_card_number"],
        q=["How much is left on <gift_card_number>?", "Could you tell me the balance of <gift_card_number>?"],
        vp=["check the balance of <gift_card_number>"])
    D.I("delete", [("delete_account", None)], ["customer_id"],
        q=["Please close my account for good and delete my details.", "I want my account and my order history deleted."],
        vp=["delete my account"])
    D.tiers = [["cancel_order", "change_delivery_address"], ["report_damaged_item", "start_return"]]
    D.sess_order = ["customer", "account status", "identity check", "order on screen", "today"]
    D.values = {"account status": ["active", "payment hold"], "identity check": ["passed", "not done"]}

    def init(rng, W):
        W["customer_id"] = f"C-{rng.randint(10000, 99999)}"
        W["sess"].update({"customer": f"{W['names']['name']} (customer ID {W['customer_id']})",
                          "account status": rng.choice(D.values["account status"]),
                          "identity check": rng.choice(D.values["identity check"]), "order on screen": "none",
                          "today": ftoday(W["today"])})
    D.init = init
    return D


def dom_bank():
    D = Dom("bank")
    D.orgs = ["Meridian Credit Union", "Northgate Bank", "Alder Savings", "Crestline Bank"]
    D.assistant = "the in-app banking assistant of {org}"
    D.user_label, D.layouts = "Customer", ["chat", "chat2", "voice"]
    PAYEES = [("landlord", True), ("plumber", True), ("sister", True), ("piano teacher", True), ("childminder", True),
              ("window cleaner", True), ("electricity supplier", False), ("gym", False)]
    COMPANIES = ["Tidewater Energy", "Northside Fitness", "Brightline Power", "Summit Gym"]
    MERCHANTS = ["QuickMart", "CityRide", "Luna Cafe", "PageTurner Books", "FreshBasket", "StreamBox", "Harbour Fuel"]

    def g_payee(r, W, t):
        used = {e["key"] for e in W["lists"].get("saved payees", [])} | W["used_keys"]["saved payees"]
        rel, human = r.choice([p for p in PAYEES if p[0] not in used])
        if human:
            f, l = person(r, W["used_names"])
            name = f"{f} {l}"
        else:
            name = r.choice([c for c in COMPANIES if ("Energy" in c or "Power" in c) == (rel == "electricity supplier")])
        return {"value": name, "key": rel}

    def g_card(r, W, t):
        kind = r.choice(["Debit", "Credit"])
        return {"value": f"{r.randint(1000, 9999)}", "key": kind}

    def g_tx(r, W, t):
        used = W["used_keys"]["recent card activity"]
        m = r.choice([x for x in MERCHANTS if x not in used])
        amt = f"${r.randint(4, 180)}.{r.randint(0, 99):02d}"
        d = W["today"] - dt.timedelta(days=r.randint(1, 9))
        return {"value": f"T-{r.randint(10000, 99999)}", "key": m, "attrs": {"amt": amt, "date": fday(d, wd=False)}}

    D.P("account", lambda r, W, t: {"value": r.choice(["checking", "savings"])}, np=["my {v} account", "my {v}"])
    D.P("from_account", lambda r, W, t: {"value": "checking"}, np=["my checking account", "checking"])
    D.P("to_account", lambda r, W, t: {"value": "savings"}, np=["my savings account", "savings"])
    D.P("amount", lambda r, W, t: _amt(r, W), np=["{v}"], vague=["some money", "a bit of money", "the usual amount"],
        regex=r"\$\d")
    D.P("payee", g_payee, np=["{v}"], vague=["a friend of mine", "someone from my running club"],
        ctx=CtxList("saved payees", "{v} ({key})", ["my {key}"], always=False), provided=["present", "ctx"])
    D.P("card", g_card, np=["the card ending {v}", "my card ending in {v}"], vague=["my card", "one of my cards"],
        regex=r"ending (?:in )?\d{4}", ctx=CtxList("cards", "{key} card ending {v}", ["my {lkey} card"]),
        provided=["present", "ctx", "ctx"])
    D.P("transaction_id", g_tx, np=["transaction {v}"], vague=["a charge", "a payment"], regex=r"\bT-\d{5}\b",
        ctx=CtxList("recent card activity", "{v} {key} {amt} ({date})", ["the {key} charge of {amt}", "the {amt} payment to {key}"]),
        gloss="from recent card activity", provided=["ctx", "ctx", "present"])
    D.P("new_limit", lambda r, W, t: {"value": money(r.choice([3000, 4000, 5000, 7500, 10000]))}, np=["{v}"],
        vague=["something higher", "a bigger number"], regex=r"\$\d", can_omit=True)
    two = [Rs("allow", field="2-step verified this session", values=["yes"])]
    D.T("get_balance", "returns the current and available balance of one of the customer's own accounts.", ["account"])
    D.T("list_transactions", "lists the payments in and out of one account, for the last 30 days unless dates are given.",
        ["account"], opt=["date_from", "date_to"])
    D.T("transfer_between_own_accounts", "moves money between two accounts that both belong to the customer.",
        ["from_account", "to_account", "amount"])
    D.T("send_payment", "pays another person or company from the customer's checking account.", ["payee", "amount"],
        restr=[Rs("max", param="amount", lim="pay", fmt=money)] + two)
    D.T("request_payment_review", "queues a payment to another person or company that is above the send_payment limit, "
        "for a staff review within one business day.", ["payee", "amount"], restr=two, fallback_of="send_payment")
    D.T("freeze_card", "temporarily blocks a card the customer has misplaced; it can be unfrozen later.", ["card"])
    D.T("report_card_stolen", "permanently cancels a card that was stolen and orders a replacement.", ["card"])
    D.T("dispute_transaction", "opens a dispute about one card transaction the customer does not recognise or was "
        "wrongly charged.", ["transaction_id"])
    D.T("increase_credit_limit", "requests a higher limit on the customer's credit card.", ["new_limit"],
        restr=[Rs("deny", field="credit account status", values=["in arrears"])])
    D.lookups = {"transaction_id": ["list_transactions"]}
    D.I("account_info", [("get_balance", ("fact", "want", "balance")), ("list_transactions", ("fact", "want", "activity"))],
        ["account"], facts={"want": ["balance", "activity"]},
        phrases={"want": {"balance": ["how much money is in <account> right now", "what the balance of <account> is today"],
                          "activity": ["what has gone in and out of <account> this month",
                                       "what I've spent from <account> over the last few weeks"]}},
        q=["Could you tell me {f:want}?", "I'd like to know {f:want}."], vp=["tell me {f:want}"])
    D.I("move_money", [("transfer_between_own_accounts", ("fact", "dest", "own")), ("send_payment", ("fact", "dest", "other")),
                       ("request_payment_review", ("and", ("fact", "dest", "other"), ("over", "amount", "send_payment")))],
        ["from_account", "to_account", "amount", "payee"], facts={"dest": ["own", "other"]},
        phrases={"dest": {"own": ["<to_account>"], "other": ["<payee>"]}},
        rel=lambda f: ["from_account", "to_account", "amount"] if f["dest"] == "own" else ["from_account", "amount", "payee"],
        q=["Please move <amount> from <from_account> to {f:dest}.", "Can you transfer <amount> out of <from_account> to {f:dest} today?"],
        vp=["move <amount> from <from_account> to {f:dest}"])
    D.I("card_problem", [("freeze_card", ("fact", "what", "misplaced")), ("report_card_stolen", ("fact", "what", "stolen"))],
        ["card"], facts={"what": ["misplaced", "stolen"]},
        phrases={"what": {"misplaced": ["I can't find it anywhere, it's probably somewhere in the house",
                                        "I think I left it at a friend's place last night",
                                        "it's gone missing, maybe down the back of the sofa"],
                          "stolen": ["my bag was snatched on the train with it inside",
                                     "it was stolen along with my wallet at the market this morning",
                                     "someone broke into my car and took it"]}},
        q=["I need help with <card>: {f:what}.", "Can you sort out <card>? {F:what}."],
        vp=["sort out <card>"])
    D.I("dispute", [("dispute_transaction", None)], ["transaction_id"],
        q=["I don't recognise <transaction_id>. Can you look into it?", "There's <transaction_id> on my statement that I never made.",
           "<^transaction_id> is wrong - I was charged twice for the same thing."], vp=["dispute <transaction_id>"])
    D.I("raise_limit", [("increase_credit_limit", None)], ["new_limit"],
        q=["Could I get my credit card limit raised[ to {v:new_limit}]?", "I'd like my credit limit increased to <new_limit>, please."],
        vp=["raise my credit limit to <new_limit>"])
    D.tiers = [["report_card_stolen", "freeze_card", "dispute_transaction"],
               ["send_payment", "request_payment_review", "transfer_between_own_accounts"]]
    D.sess_order = ["customer", "accounts", "cards", "2-step verified this session", "credit account status", "saved payees",
                    "recent card activity", "today"]
    D.values = {"2-step verified this session": ["yes", "no"], "credit account status": ["good standing", "in arrears"]}
    D.list_min = {"saved payees": 2, "cards": 2, "recent card activity": 3}
    def f_card(r, W, t):
        free = [k for k in ("Debit", "Credit") if k not in W["used_keys"]["cards"] and k not in {e["key"] for e in W["lists"]["cards"]}]
        return {"value": f"{r.randint(1000, 9999)}", "key": free[0]} if free else None

    D.fillers = {"saved payees": g_payee, "cards": f_card, "recent card activity": g_tx}
    D.fb = [("move_money", {"dest": "other"}, "amount", "pay", "send_payment", "request_payment_review")]

    def init(rng, W):
        W["limits"]["pay"] = rng.choice([1000, 2500, 5000])
        W["sess"].update({"customer": W["names"]["name"],
                          "accounts": f"Everyday checking (ending {rng.randint(1000, 9999)}); Savings (ending {rng.randint(1000, 9999)})",
                          "2-step verified this session": rng.choice(D.values["2-step verified this session"]),
                          "credit account status": rng.choice(D.values["credit account status"]), "today": ftoday(W["today"])})
    D.init = init
    return D


def _amt(r, W):
    lim = W["limits"].get("pay", 2500)
    n = r.choice([40, 75, 120, 180, 250, 320, 450, 600, 850])
    n = min(n, lim - 100)
    return {"value": money(n), "num": n}


def dom_travel():
    D = Dom("travel")
    D.orgs = ["Skyloom Travel", "Bluefin Airways", "Northstar Trips"]
    D.assistant = "the booking assistant of {org}"
    D.user_label, D.layouts = "Traveller", ["chat", "chat2", "email"]
    CITIES = ["Lisbon", "Paris", "Rome", "Madrid", "Vienna", "Prague", "Dublin", "Athens", "Oslo", "Berlin"]
    COUNTRIES = ["Japan", "Brazil", "Canada", "Turkey", "Vietnam", "Morocco", "Australia", "India"]
    NATS = ["Irish", "Canadian", "Brazilian", "Indian", "Japanese", "Kenyan", "Mexican", "Polish"]

    def g_booking(r, W, t):
        used = W["used_keys"]["bookings on file"] | {e["key"] for e in W["lists"].get("bookings on file", [])}
        dest = r.choice([c for c in CITIES if c not in used and c != W["home_city"]])
        orig = W["home_city"]
        d = W["today"] + dt.timedelta(days=r.randint(10, 60))
        return {"value": rid_chars(r, 6), "key": dest,
                "attrs": {"orig": orig, "date": fday(d, wd=False), "fare": r.choice(["Basic", "Standard", "Flex"]), "d": d.isoformat()}}

    def g_newdate(r, W, t):
        d = W["today"] + dt.timedelta(days=r.randint(62, 90))
        return {"value": fday(d, wd=False)}

    def g_bags(r, W, t):
        n = r.choice([1, 2])
        return {"value": f"{n} extra bag{'s' if n > 1 else ''}", "num": n}

    D.P("booking_ref", g_booking, np=["booking {v}", "booking reference {v}"], vague=["my booking", "my trip"],
        regex=r"\b(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z0-9]{6}\b",
        ctx=CtxList("bookings on file", "{v}: {orig} to {key}, {date} ({fare} fare)",
                    ["my {key} trip", "my flight to {key}", "the {key} booking"]), provided=["present", "ctx"])
    D.P("new_date", g_newdate, np=["{v}"], vague=["a later date", "another day next month"], regex=DATE_RE)
    D.P("origin", lambda r, W, t: {"value": r.choice(CITIES[:5])}, np=["{v}"])
    D.P("destination", lambda r, W, t: {"value": r.choice(CITIES[5:])}, np=["{v}"])
    D.P("travel_date", lambda r, W, t: {"value": fday(W["today"] + dt.timedelta(days=r.randint(5, 40)), wd=False)},
        np=["on {v}"], vague=["sometime next month", "around the holidays"], regex=DATE_RE, can_omit=True)
    D.P("flight_number", lambda r, W, t: {"value": f"{r.choice(['BF', 'SK', 'NS'])} {r.randint(100, 989)}"},
        np=["flight {v}"], vague=["my flight", "our flight"], regex=r"\b[A-Z]{2} ?\d{3}\b")
    D.P("bags", g_bags, np=["{v}"], vague=["some extra bags", "more bags"], regex=r"\b\d+ extra bags?\b")
    D.P("seat", lambda r, W, t: {"value": f"{r.randint(6, 34)}{r.choice('ACDF')}"}, np=["seat {v}"],
        vague=["a window seat", "a seat near the front"], regex=r"\b\d{1,2}[A-F]\b")
    D.P("nationality", lambda r, W, t: {"value": r.choice(NATS)}, np=["{v}"], vocab=NATS, can_omit=True)
    D.P("destination_country", lambda r, W, t: {"value": r.choice(COUNTRIES)}, np=["{v}"])
    D.T("search_flights", "finds available flights for a route on one date; it books nothing.",
        ["origin", "destination", "travel_date"])
    D.T("get_booking", "shows the details of one existing booking: flights, passengers and extras.", ["booking_ref"])
    D.T("check_flight_status", "shows today's live status of one flight: delays, cancellations and gate.", ["flight_number"])
    D.T("change_flight", "moves an existing booking to a different travel date.", ["booking_ref", "new_date"],
        restr=[Rs("fare", param="booking_ref", values=["Basic"])])
    D.T("cancel_booking", "cancels an existing booking and refunds whatever its fare allows.", ["booking_ref"])
    D.T("add_baggage", "adds checked bags to an existing booking.", ["booking_ref", "bags"],
        restr=[Rs("max", param="bags", lim="bags", fmt=lambda n: str(n))])
    D.T("select_seat", "assigns a specific seat on an existing booking.", ["booking_ref", "seat"],
        restr=[Rs("allow", field="loyalty tier", values=["Silver", "Gold"])])
    D.T("check_entry_requirements", "returns the passport and visa rules for a nationality visiting a destination country.",
        ["nationality", "destination_country"])
    D.lookups = {"flight_number": ["get_booking"]}
    D.I("flight_status", [("check_flight_status", None)], ["flight_number"],
        q=["Is <flight_number> on time today?", "Has <flight_number> been delayed? I'm about to leave for the airport.",
           "What's the latest on <flight_number> - is it still going?"], vp=["check whether <flight_number> is on time"])
    D.I("search", [("search_flights", None)], ["origin", "destination", "travel_date"],
        q=["Can you find me flights from <origin> to <destination>[ on {v:travel_date}]?",
           "What flights are there from <origin> to <destination> <travel_date>?"],
        vp=["look up flights from <origin> to <destination> <travel_date>"])
    D.I("alter_trip", [("change_flight", ("fact", "what", "change")), ("cancel_booking", ("fact", "what", "cancel"))],
        ["booking_ref", "new_date"], facts={"what": ["change", "cancel"]},
        phrases={"what": {"change": ["I can't make that day any more, so please move me to <new_date>",
                                     "please push it back to <new_date>"],
                          "cancel": ["I can't make the trip at all any more, so please cancel it",
                                     "the conference was called off and I won't be going at all, so please cancel it"]},
                 "what_vp": {"change": ["move <booking_ref> to <new_date>"], "cancel": ["cancel <booking_ref>"]}},
        rel=lambda f: ["booking_ref", "new_date"] if f["what"] == "change" else ["booking_ref"],
        q=["About <booking_ref>: {f:what}.", "Regarding <booking_ref> - {f:what}."], vp=["{f:what_vp}"])
    D.I("bags", [("add_baggage", None)], ["booking_ref", "bags"],
        q=["Please add <bags> to <booking_ref>.", "Can I get <bags> added to <booking_ref>? We're moving abroad."],
        vp=["add <bags> to <booking_ref>"])
    D.I("seat", [("select_seat", None)], ["booking_ref", "seat"],
        q=["Can I have <seat> on <booking_ref>?", "Please put me in <seat> for <booking_ref>."],
        vp=["put me in <seat> on <booking_ref>"])
    D.I("entry", [("check_entry_requirements", None)], ["nationality", "destination_country"],
        q=["[My passport is {v:nationality}. ]What do I need to enter <destination_country>?",
           "Do I need a visa for <destination_country>?[ My passport is {v:nationality}.]"],
        vp=["check the entry rules for <destination_country>[ - my passport is {v:nationality}]"])
    D.tiers = [["change_flight", "cancel_booking"]]
    D.sess_order = ["traveller", "loyalty tier", "bookings on file", "today"]
    D.values = {"loyalty tier": ["none", "Silver", "Gold"]}
    D.list_min = {"bookings on file": 2}
    D.fillers = {"bookings on file": g_booking}

    def init(rng, W):
        W["limits"]["bags"] = 3
        W["home_city"] = rng.choice(CITIES)
        W["used_keys"]["bookings on file"].add(W["home_city"])
        W["sess"].update({"traveller": W["names"]["name"], "loyalty tier": rng.choice(D.values["loyalty tier"]),
                          "today": ftoday(W["today"])})
    D.init = init
    return D


def dom_work():
    D = Dom("workplace")
    D.orgs = ["Fernhill Partners", "Quarry Labs", "Oakridge Council", "Tessellate"]
    D.assistant = "the calendar, email and documents assistant used by staff at {org}"
    D.user_label, D.layouts = "User", ["chat", "slack", "email"]
    TOPICS = ["launch plan", "Q3 budget", "hiring pipeline", "client renewal", "office move", "training schedule"]
    CHORES = ["call the dentist", "submit my timesheet", "book the team lunch", "renew my parking permit", "chase the printer quote"]
    MSGS = ["the quarterly report will be a day late", "Thursday's workshop has moved to Room 3", "the invoice has been paid",
            "the draft contract is ready for review"]
    ROOMS = ["Larch Room", "Boardroom", "Garden Studio", "Harbour Room"]
    EVENTS = ["budget review", "vendor demo", "project kickoff", "design critique", "quarterly planning session",
              "team retrospective"]
    DOCS = ["Q3 budget draft", "hiring plan", "supplier shortlist", "office move checklist"]

    def g_time(r, W, t):
        if r.random() < 0.3:
            h = r.choice([9, 10, 11, 14, 15, 16])
            return {"value": f"tomorrow at {h if h <= 12 else h - 12}{'am' if h < 12 else 'pm'}", "rel": True}
        d = W["today"] + dt.timedelta(days=r.randint(2, 9))
        return {"value": f"{fday(d)} at {r.choice(['09:30', '10:00', '11:15', '13:00', '14:30', '16:00'])}"}

    def g_event(r, W, t):
        used = W["used_keys"]["upcoming events"] | {e["key"] for e in W["lists"].get("upcoming events", [])}
        name = r.choice([e for e in EVENTS if e not in used])
        d = W["today"] + dt.timedelta(days=r.randint(1, 8))
        return {"value": f"EV-{r.randint(1000, 9999)}", "key": name,
                "attrs": {"when": f"{fday(d)} {r.choice(['09:00', '10:30', '14:00', '15:30'])}", "Key": cap(name)}}

    def g_people(r, W, t):
        n = r.choice([1, 2])
        ps = [" ".join(person(r, W["used_names"])) for _ in range(n)]
        return {"value": " and ".join(ps)}

    def g_email(r, W, t):
        f, l = person(r, W["used_names"])
        return {"value": f"{f.lower()}.{l.lower()}@{r.choice(['partner.example', 'supplier.example', 'client.example'])}"}

    D.P("attendees", g_people, np=["{v}"])
    D.P("start_time", g_time, np=["{v}"], vague=["sometime next week", "later this week"], regex=TIME_RE)
    D.P("text", lambda r, W, t: {"value": r.choice(CHORES)}, np=["{v}"])
    D.P("day", lambda r, W, t: {"value": fday(W["today"] + dt.timedelta(days=r.randint(2, 8)))}, np=["on {v}"],
        vague=["sometime soon", "one day next week"], regex=DATE_RE)
    D.P("event", g_event, vague=["my meeting", "that meeting"],
        ctx=CtxList("upcoming events", "{v} {Key} ({when})", ["the {key}", "the {key} on my calendar"]), provided=["ctx"])
    D.P("new_time", g_time, np=["{v}"], vague=["a bit later", "another day"], regex=TIME_RE)
    D.P("recipient", g_email, np=["{v}"], vague=["the new supplier", "the person from yesterday's call"], regex=r"[\w.]+@[\w.]+")
    D.P("message", lambda r, W, t: {"value": r.choice(MSGS)}, np=["{v}"])
    D.P("document", lambda r, W, t: {"value": f"DOC-{r.randint(1000, 9999)}", "attrs": {"title": r.choice(DOCS)}},
        np=["document {v}"], vague=["that spreadsheet from last week"], regex=r"\bDOC-\d{4}\b",
        ctx=CtxField("document open", ["this document", "the file I have open"], fmt="{v} ({title})"),
        provided=["ctx", "present"])
    D.P("share_with", g_email, np=["{v}"], vague=["the new contractor", "someone from finance"], regex=r"[\w.]+@[\w.]+")
    D.P("room", lambda r, W, t: {"value": r.choice(ROOMS)}, np=["the {v}"], vague=["a room", "somewhere quiet"], vocab=ROOMS)
    D.T("create_event", "adds a new meeting to the user's calendar and sends invitations to the attendees.",
        ["start_time", "attendees"], opt=["title"])
    D.T("find_free_slots", "finds times on one day when all the named people are free; it books nothing.", ["attendees", "day"])
    D.T("reschedule_event", "moves an existing calendar event to a new time and tells the attendees.", ["event", "new_time"])
    D.T("cancel_event", "cancels an existing calendar event and notifies its attendees.", ["event"])
    D.T("set_reminder", "sets a private reminder for the user alone; nobody is invited.", ["start_time", "text"])
    D.T("send_email", "sends an email from the user's mailbox.", ["recipient", "message"])
    D.T("share_document", "gives another person access to one document.", ["document", "share_with"],
        restr=[Rs("deny", field="role", values=["contractor"])])
    D.T("book_room", "reserves a meeting room for a time slot.", ["room", "start_time"],
        restr=[Rs("allow", field="role", values=["employee", "manager"])])
    ex_topic = lambda r, W, t: {"topic": r.choice(TOPICS), "clock": r.choice(["10am", "11:30", "2pm", "3:30pm"])}
    D.I("calendar_block", [("create_event", ("fact", "who", "others")), ("set_reminder", ("fact", "who", "self"))],
        ["start_time", "attendees", "text"], facts={"who": ["others", "self"]},
        phrases={"who": {"others": ["a catch-up with <attendees> about the {x:topic}", "time with <attendees> to go through the {x:topic}"],
                         "self": ["a reminder for me to <text>", "a private note to myself to <text>"]}},
        rel=lambda f: ["start_time", "attendees"] if f["who"] == "others" else ["start_time", "text"],
        q=["Can you put in {f:who} for <start_time>?", "For <start_time>, please set up {f:who}."],
        vp=["set up {f:who} for <start_time>"], extras=ex_topic)
    D.I("plan_meeting", [("create_event", ("fact", "ask", "time")), ("find_free_slots", ("fact", "ask", "free"))],
        ["attendees", "day"], facts={"ask": ["time", "free"]},
        phrases={"ask": {"time": ["please book it for {x:clock}.", "put it in at {x:clock}."],
                         "free": ["when are we all free?", "which slots work for all of us?"]}},
        q=["I need an hour with <attendees> <day> to plan the {x:topic}. {F:ask}",
           "Can you set aside an hour <day> for me and <attendees> to discuss the {x:topic}? {F:ask}"],
        vp=["set aside an hour with <attendees> <day> for the {x:topic}"], extras=ex_topic,
        implicit=lambda t: ({"start_time": [t["ps"]["day"]["value"], t["x"]["clock"]]}
                            if t["facts"]["ask"] == "time" and t["ps"]["day"]["mode"] == "present" else {}))
    D.I("move_or_cancel", [("reschedule_event", ("fact", "act", "move")), ("cancel_event", ("fact", "act", "cancel"))],
        ["event", "new_time"], facts={"act": ["move", "cancel"]},
        phrases={"act": {"move": ["please move it to <new_time>", "please shift it to <new_time>"],
                         "cancel": ["please just cancel it, we can skip it this time", "please cancel it altogether"]},
                 "act_vp": {"move": ["move <event> to <new_time>"], "cancel": ["cancel <event>"]}},
        rel=lambda f: ["event", "new_time"] if f["act"] == "move" else ["event"],
        q=["<^event> clashes with a client visit - {f:act}.", "Something came up with <event>: {f:act}."],
        vp=["{f:act_vp}"])
    D.I("email", [("send_email", None)], ["recipient", "message"],
        q=["Please email <recipient> to say <message>.", "Can you drop <recipient> a line saying <message>?"],
        vp=["email <recipient> to say <message>"])
    D.I("share", [("share_document", None)], ["document", "share_with"],
        q=["Please share <document> with <share_with>.", "Can you give <share_with> access to <document>?"],
        vp=["share <document> with <share_with>"])
    D.I("room", [("book_room", None)], ["room", "start_time"],
        q=["Can you book <room> for <start_time>?", "Please reserve <room> for <start_time>; I'm running a workshop."],
        vp=["book <room> for <start_time>"])
    D.tiers = [["cancel_event", "reschedule_event"]]
    D.sess_order = ["user", "role", "today", "upcoming events", "document open"]
    D.values = {"role": ["employee", "manager", "contractor", "intern"]}
    D.list_min = {"upcoming events": 2}
    D.fillers = {"upcoming events": g_event}

    def init(rng, W):
        W["sess"].update({"user": W["names"]["name"], "role": rng.choice(D.values["role"]), "today": ftoday(W["today"]),
                          "document open": "none"})
    D.init = init
    return D


def dom_it():
    D = Dom("it_desk")
    D.orgs = ["Fernhill Partners", "Harlow Logistics", "Quarry Labs", "Oakridge Council"]
    D.assistant = "the internal IT help-desk assistant at {org}"
    D.user_label, D.layouts = "Employee", ["chat", "slack", "email"]
    RES = ["the Finance shared drive", "the payroll app", "the Legal SharePoint site", "the design team's project folder"]
    SOFT = ["the diagram editor", "the statistics package", "the PDF editor", "the screen recorder"]
    KINDS = [("laptop", "LT"), ("desktop computer", "PC"), ("monitor", "MN"), ("docking station", "DS"), ("desk phone", "DP")]

    def g_user(r, W, t):
        f, l = person(r, W["used_names"])
        return {"value": f"{f[0].lower()}.{l.lower()}"}

    def g_asset(r, W, t):
        used = W["used_keys"]["assigned devices"] | {e["key"] for e in W["lists"].get("assigned devices", [])}
        kinds = KINDS[:2] if t is not None and t["intent"] == "install" else KINDS  # software goes on a computer only
        k, pre = r.choice([x for x in kinds if x[0] not in used])
        return {"value": f"{pre}-{r.randint(10000, 99999)}", "key": k}

    D.P("username", g_user, np=["the account {v}", "{v}'s account"], vague=["my colleague's account", "the new intern's account"],
        regex=r"\b[a-z]\.[a-z]+\b", ctx=CtxSelf("requester", ["my account", "my own account"]), provided=["ctx", "present"])
    D.P("resource", lambda r, W, t: {"value": r.choice(RES)}, np=["{v}"], vague=["the usual folders", "whatever the team uses"],
        vocab=RES)
    D.P("asset_tag", g_asset, np=["asset {v}", "device {v}"], regex=r"\b[A-Z]{2}-\d{5}\b",
        ctx=CtxList("assigned devices", "{v} ({key})", ["my {key}"]), provided=["ctx", "present"])
    D.P("ticket_id", lambda r, W, t: {"value": f"INC-{r.randint(100000, 999999)}"}, np=["ticket {v}"],
        vague=["my ticket", "the ticket I raised last week"], regex=r"\bINC-\d+\b",
        ctx=CtxField("ticket in view", ["this ticket", "the ticket I have open"]), provided=["present", "ctx"])
    D.P("software", lambda r, W, t: {"value": r.choice(SOFT)}, np=["{v}"], vague=["some software I need", "the tool the team uses"],
        vocab=SOFT)
    D.P("starter_name", lambda r, W, t: {"value": " ".join(person(r, W["used_names"]))}, np=["{v}"])
    D.P("start_date", lambda r, W, t: {"value": fday(W["today"] + dt.timedelta(days=r.randint(7, 30)))}, np=["on {v}"],
        vague=["soon", "sometime next month"], regex=DATE_RE)
    D.T("reset_password", "sets a temporary password for an account whose user has forgotten the password.", ["username"],
        restr=[Rs("self_or_role", param="username", roles=["it_admin"])])
    D.T("unlock_account", "unlocks an account that was locked after too many failed sign-ins; the password stays the same.",
        ["username"])
    D.T("grant_access", "gives an account access to a shared folder, site or application.", ["username", "resource"],
        restr=[Rs("allow", field="role", values=["manager", "it_admin"])])
    D.T("report_hardware_fault", "logs a fault with one piece of company hardware for a technician visit.", ["asset_tag"])
    D.T("check_ticket_status", "shows the progress of one existing IT ticket.", ["ticket_id"])
    D.T("install_software", "installs an approved application on one company device.", ["software", "asset_tag"],
        restr=[Rs("deny", field="role", values=["contractor"])])
    D.T("provision_new_starter", "creates accounts and orders equipment for a new employee.", ["starter_name", "start_date"],
        restr=[Rs("allow", field="role", values=["manager"])])
    FAULTS = ["keeps switching itself off", "won't power on at all", "has started making a loud buzzing noise"]
    D.I("pw", [("reset_password", ("fact", "issue", "forgot")), ("unlock_account", ("fact", "issue", "locked"))],
        ["username"], facts={"issue": ["forgot", "locked"]},
        phrases={"issue": {"forgot": ["needs a new password because the old one has been forgotten",
                                      "can't be signed into because the password has been forgotten"],
                           "locked": ["is locked after too many failed sign-in attempts",
                                      "got locked out this morning after too many wrong passwords"]},
                 "issue_vp": {"forgot": ["set a new password on <username>"], "locked": ["unlock <username>"]}},
        q=["<^username> {f:issue}. Can you help?", "Help please - <username> {f:issue}."], vp=["{f:issue_vp}"])
    D.I("access", [("grant_access", None)], ["username", "resource"],
        q=["Please give <username> access to <resource>.", "Can <username> get access to <resource>? It's needed for the audit."],
        vp=["give <username> access to <resource>"])
    D.I("hardware", [("report_hardware_fault", None)], ["asset_tag"],
        q=["<^asset_tag> {x:fault}. Can someone take a look?", "Could you get a technician to look at <asset_tag>? It {x:fault}."],
        vp=["get someone to look at <asset_tag>"], extras=lambda r, W, t: {"fault": r.choice(FAULTS)})
    D.I("ticket", [("check_ticket_status", None)], ["ticket_id"],
        q=["Any update on <ticket_id>?", "What's happening with <ticket_id>? It's been a week."], vp=["check on <ticket_id>"])
    D.I("install", [("install_software", None)], ["software", "asset_tag"],
        q=["Can you install <software> on <asset_tag>?", "I need <software> on <asset_tag> for a project starting Monday."],
        vp=["install <software> on <asset_tag>"])
    D.I("newstarter", [("provision_new_starter", None)], ["starter_name", "start_date"],
        q=["We have a new starter, <starter_name>, joining <start_date>. Please get their accounts and laptop ready.",
           "Please set up accounts and equipment for <starter_name>, who starts <start_date>."],
        vp=["set everything up for <starter_name>, who starts <start_date>"])
    D.tiers = [["unlock_account", "reset_password"]]
    D.sess_order = ["requester", "role", "department", "assigned devices", "ticket in view", "today"]
    D.values = {"role": ["staff", "manager", "it_admin", "contractor"]}
    D.list_min = {"assigned devices": 2}
    D.fillers = {"assigned devices": g_asset}

    def init(rng, W):
        f, l = W["names"]["first"], W["names"]["last"]
        W["requester_user"] = f"{f[0].lower()}.{l.lower()}"
        W["sess"].update({"requester": f"{f} {l} (username {W['requester_user']})", "role": rng.choice(D.values["role"]),
                          "department": rng.choice(["Finance", "Operations", "Marketing", "Legal", "Engineering"]),
                          "ticket in view": "none", "today": ftoday(W["today"])})
    D.init = init
    return D


def dom_ops():
    D = Dom("cloud_ops")
    D.orgs = ["Quarry Labs", "Tessellate", "Parcelwise", "Brightwell Kitchen"]
    D.assistant = "the operations chat bot of the {org} platform team"
    D.user_label, D.layouts = "Engineer", ["slack", "chat"]
    SERVICES = ["checkout-api", "search-indexer", "billing-worker", "auth-gateway", "image-resizer"]
    BUCKETS = ["tmp-exports-2023", "old-report-archive", "staging-uploads-v1", "legacy-thumbnails"]

    def g_rep(r, W, t):
        n = r.choice([6, 8, 10, 12, 14])
        return {"value": str(n), "num": n}

    D.P("service", lambda r, W, t: {"value": r.choice(SERVICES)}, np=["{v}"])
    D.P("environment", lambda r, W, t: {"value": r.choice(["production", "staging"])}, np=["in {v}"],
        regex=r"\b(?:production|staging|prod)\b", can_omit=True)
    D.P("version", lambda r, W, t: {"value": f"v{r.randint(1, 4)}.{r.randint(0, 19)}.{r.randint(0, 9)}"}, np=["{v}"],
        vague=["the latest build", "the new build"], regex=r"\bv\d+\.\d+\.\d+\b")
    D.P("replicas", g_rep, np=["{v} replicas"], vague=["a lot more replicas", "more replicas"], regex=r"\b\d+ replicas\b")
    D.P("severity", lambda r, W, t: {"value": r.choice(["SEV1", "SEV2", "SEV3"])}, np=["at {v}", "as a {v}"],
        regex=r"\bSEV ?\d\b", can_omit=True)
    D.P("bucket", lambda r, W, t: {"value": r.choice(BUCKETS)}, np=["the bucket {v}", "bucket {v}"])
    viewer = [Rs("deny", field="role", values=["viewer"])]
    D.T("deploy_service", "deploys a given version of a service to an environment.", ["service", "version", "environment"],
        restr=[Rs("ifp", param="environment", pval="production", inner=Rs("allow", field="role", values=["release_manager"])),
               Rs("ifp", param="environment", pval="production", inner=Rs("deny", field="production freeze", values=["on"]))])
    D.T("rollback_deployment", "returns a service to the version it ran before its latest deployment.",
        ["service", "environment"], restr=viewer)
    D.T("scale_service", "sets the number of running replicas of a service.", ["service", "environment", "replicas"],
        restr=[Rs("max", param="replicas", lim="rep", fmt=lambda n: str(n))])
    D.T("request_capacity_increase", "files a request for more replicas than the scale_service limit; a platform engineer "
        "approves it.", ["service", "environment", "replicas"], restr=viewer, fallback_of="scale_service")
    D.T("get_logs", "returns recent log lines and error messages of a service.", ["service", "environment"], opt=["since"])
    D.T("get_metrics", "returns CPU, memory and latency graphs of a service.", ["service", "environment"])
    D.T("open_incident", "opens an incident, pages the on-call engineer and creates a status channel.", ["service", "severity"])
    D.T("restart_service", "restarts every running instance of a service without changing its version.",
        ["service", "environment"], restr=viewer)
    D.T("delete_bucket", "permanently deletes a storage bucket and everything in it.", ["bucket"],
        restr=[Rs("allow", field="role", values=["sre"])])
    D.I("deploy", [("deploy_service", None)], ["service", "version", "environment"],
        q=["Please deploy <version> of <service>[ to {v:environment}].", "Ship <version> of <service>[ to {v:environment}] when you can."],
        vp=["deploy <version> of <service>[ to {v:environment}]"])
    D.I("rollback", [("rollback_deployment", None)], ["service", "environment"],
        q=["<service> has been throwing errors since its last deploy[ <environment>]. Please put back the version that was running before.",
           "Undo today's deploy of <service>[ <environment>] - put the previous version back."],
        vp=["roll back <service>[ <environment>]"])
    D.I("scale", [("scale_service", None), ("request_capacity_increase", ("over", "replicas", "scale_service"))],
        ["service", "environment", "replicas"],
        q=["Traffic is spiking - scale <service>[ <environment>] to <replicas>.",
           "Please run <replicas> of <service>[ <environment>] until the sale ends."],
        vp=["scale <service>[ <environment>] to <replicas>"])
    D.I("look", [("get_logs", ("fact", "what", "logs")), ("get_metrics", ("fact", "what", "metrics"))],
        ["service", "environment"], facts={"what": ["logs", "metrics"]},
        phrases={"what": {"logs": ["pull up the last hour of logs for <service>", "show me the error messages <service> has been printing"],
                          "metrics": ["show me how <service>'s latency has looked over the last hour",
                                      "pull up the CPU and memory graphs for <service>"]}},
        q=["Can you {f:what}[ <environment>]?", "Quick one - {f:what}[ <environment>], please."], vp=["{f:what}[ <environment>]"])
    D.I("incident", [("open_incident", None)], ["service", "severity"],
        q=["<service> is returning errors for most users. Please open an incident[ <severity>].",
           "We have an outage on <service>. Open an incident[ <severity>] and page whoever is on call."],
        vp=["open an incident for <service>[ <severity>]"])
    D.I("restart", [("restart_service", None)], ["service", "environment"],
        q=["<service> is stuck and not processing jobs. Please restart it[ <environment>].",
           "Could you restart <service>[ <environment>]? Its memory keeps creeping up."],
        vp=["restart <service>[ <environment>]"])
    D.I("drop_bucket", [("delete_bucket", None)], ["bucket"],
        q=["Please delete <bucket>; nobody has used it since last year.", "We no longer need <bucket>. Can you delete it?"],
        vp=["delete <bucket>"])
    D.tiers = [["open_incident", "rollback_deployment"], ["restart_service", "scale_service", "request_capacity_increase"]]
    D.sess_order = ["user", "role", "production freeze", "today"]
    D.values = {"role": ["developer", "sre", "release_manager", "viewer"], "production freeze": ["on", "off"]}
    D.fb = [("scale", {}, "replicas", "rep", "scale_service", "request_capacity_increase")]

    def init(rng, W):
        W["limits"]["rep"] = 20
        W["sess"].update({"user": W["names"]["name"], "role": rng.choice(D.values["role"]),
                          "production freeze": rng.choice(D.values["production freeze"]), "today": ftoday(W["today"])})
    D.init = init
    return D


def dom_home():
    D = Dom("smart_home")
    D.orgs = ["Hearthly", "Nestwise Home", "Brightlock"]
    D.assistant = "the {org} smart-home voice assistant"
    D.user_label, D.layouts = "Speaker", ["voice", "chat"]
    DOORS, ZONES, CAMS = ["front door", "back door", "side door"], ["upstairs", "downstairs", "living-room"], \
        ["porch camera", "garden camera", "garage camera"]
    ROOMS = ["kitchen", "hallway", "garden", "study"]

    def g_temp(r, W, t):
        n = r.choice([19, 20, 21, 22, 23])
        return {"value": str(n), "num": n}

    D.P("door", lambda r, W, t: {"value": r.choice(W["home"]["doors"])}, np=["the {v}"], vague=["the door"], vocab=DOORS)
    D.P("zone", lambda r, W, t: {"value": r.choice(W["home"]["zones"])}, np=["the {v} thermostat"], vague=["the heating"],
        vocab=[z + " thermostat" for z in ZONES])
    D.P("temperature", g_temp, np=["{v} °C"], vague=["something cosier", "a bit warmer"], regex=r"\d+ ?°")
    D.P("camera", lambda r, W, t: {"value": r.choice(W["home"]["cams"])}, np=["the {v}"], vague=["the camera"], vocab=CAMS)
    D.P("alarm_mode", lambda r, W, t: {"value": r.choice(["away", "home"])}, np=["in {v} mode"],
        regex=r"\b(?:away|home) mode\b", can_omit=True)
    D.P("room", lambda r, W, t: {"value": r.choice(ROOMS)}, np=["{v}"])
    D.T("set_thermostat", "sets the target temperature of one thermostat.", ["zone", "temperature"],
        restr=[Rs("max", param="temperature", lim="temp", fmt=lambda n: f"{n} °C")])
    D.T("lock_door", "locks one smart door lock.", ["door"])
    D.T("unlock_door", "unlocks one smart door lock.", ["door"], restr=[Rs("deny", field="profile", values=["guest", "child"])])
    D.T("arm_alarm", "arms the house alarm in home or away mode.", ["alarm_mode"])
    D.T("view_camera", "streams the live picture from one camera.", ["camera"], restr=[Rs("deny", field="profile", values=["guest"])])
    D.T("turn_off_lights", "switches off the lights in one room right now.", ["room"])
    D.T("create_routine", "saves an automation that repeats every day at a set time.", ["routine_time", "routine_action"],
        restr=[Rs("deny", field="profile", values=["guest"])])
    D.I("temp", [("set_thermostat", None)], ["zone", "temperature"],
        q=["Set <zone> to <temperature>, please.", "It's freezing in here - can you put <zone> up to <temperature>?"],
        vp=["set <zone> to <temperature>"])
    D.I("lock", [("lock_door", None)], ["door"], q=["Lock <door>, please.", "Did anyone lock up? Please lock <door>."],
        vp=["lock <door>"])
    D.I("unlock", [("unlock_door", None)], ["door"],
        q=["Unlock <door>, please - {x:visitor} is here.", "Can you unlock <door>? I'm standing outside with the shopping."],
        vp=["unlock <door>"], extras=lambda r, W, t: {"visitor": r.choice(["the dog walker", "my mum", "the plumber"])})
    D.I("alarm", [("arm_alarm", None)], ["alarm_mode"],
        q=["Please arm the alarm[ <alarm_mode>].", "Arm the house alarm[ <alarm_mode>], would you?"],
        vp=["arm the alarm[ <alarm_mode>]"])
    D.I("camera", [("view_camera", None)], ["camera"],
        q=["Show me <camera>, I heard a noise outside.", "Can I see what <camera> is seeing right now?"], vp=["show me <camera>"])
    D.I("lights", [("turn_off_lights", ("fact", "when", "now")), ("create_routine", ("fact", "when", "daily"))],
        ["room"], facts={"when": ["now", "daily"]},
        phrases={"when": {"now": ["right now", "now, please"],
                          "daily": ["every night at {x:clock}", "at {x:clock} each night from now on"]},
                 "when_vp": {"now": ["turn off the <room> lights"], "daily": ["switch the <room> lights off every night at {x:clock}"]}},
        q=["Turn off the lights in the <room> {f:when}.", "Switch the <room> lights off {f:when}."], vp=["{f:when_vp}"],
        extras=lambda r, W, t: {"clock": r.choice(["22:30", "23:00", "23:30", "midnight"])},
        implicit=lambda t: ({"routine_time": [t["x"]["clock"]], "routine_action": [t["ps"]["room"]["value"]]}
                            if t["facts"]["when"] == "daily" else {}))
    D.tiers = [["unlock_door", "lock_door", "arm_alarm"]]
    D.sess_order = ["speaker", "profile", "devices", "time"]
    D.values = {"profile": ["owner", "adult", "child", "guest"]}

    def init(rng, W):
        W["limits"]["temp"] = 26
        doors = rng.sample(DOORS, rng.choice([2, 3]))
        zones = rng.sample(ZONES, 2)
        cams = rng.sample(CAMS, 2)
        W["home"] = {"doors": doors, "zones": zones, "cams": cams}
        dev = [f"{d} lock" for d in doors] + [f"{z} thermostat" for z in zones] + cams + ["alarm panel"]
        W["sess"].update({"speaker": W["names"]["first"], "profile": rng.choice(D.values["profile"]), "devices": "; ".join(dev),
                          "time": f"{rng.randint(7, 22):02d}:{rng.choice(['05', '20', '40', '55'])}"})
    D.init = init
    return D


DOMAINS = [dom_retail(), dom_bank(), dom_travel(), dom_work(), dom_it(), dom_ops(), dom_home()]
DOM = {D.name: D for D in DOMAINS}
for _D in DOMAINS:  # static consistency of the domain tables
    for _t in _D.tools.values():
        for _p in _t.req:
            assert _p in _D.params or _p in ("routine_time", "routine_action"), (_D.name, _t.name, _p)
    for _i in _D.intents.values():
        for _tn, _c in _i.fits:
            assert _tn in _D.tools, (_D.name, _i.name, _tn)
        for _p in _i.params:
            assert _p in _D.params, (_D.name, _i.name, _p)


# =============================================================================================== template engine
SEG_RE = re.compile(r"\[([^\[\]]*)\]")
SLOT_RE = re.compile(r"<(\^?)(\w+)>|\{v:(\w+)\}|\{x:(\w+)\}")
FACT_RE = re.compile(r"\{(f|F):(\w+)\}")


def relevant(I, t):
    return I.rel(t["facts"]) if I.rel else list(I.params)


def expand_facts(tpl, I, t):
    def rep(m):
        fam = m.group(2)
        fact = fam.split("_")[0]
        opts = I.phrases[fam][t["facts"][fact]]
        s = opts[t["fr"].get(fam, 0) % len(opts)]
        return cap(s) if m.group(1) == "F" else s
    for _ in range(3):
        tpl = FACT_RE.sub(rep, tpl)
    return tpl


def occ(txt):
    np_ = {m[1] for m in re.findall(r"<(\^?)(\w+)>", txt)}
    v_ = set(re.findall(r"\{v:(\w+)\}", txt))
    return np_, v_


def compat(D, I, t, tpl, open_task=True):
    if open_task and I.facts:
        fams = {m.split("_")[0] for m in re.findall(r"\{[fF]:(\w+)\}", tpl)}
        if not set(I.facts) <= fams:
            return False
    s = expand_facts(tpl, I, t)
    (onp, ov) = occ(SEG_RE.sub("", s))
    segs = [occ(x) for x in SEG_RE.findall(s)]
    rel = set(relevant(I, t))
    allp = onp | ov
    for a, b in segs:
        if len(a | b) != 1:
            return False
        allp |= a | b
    if allp - rel:
        return False
    for p in rel:
        P, m = D.params[p], t["ps"][p]["mode"]
        in_np = p in onp or any(p in a for a, b in segs)
        if m == "present":
            ok = p in allp
        elif m == "vague":
            ok = in_np and p not in ov and bool(P.vague)
        elif m in ("ctx", "ctx_none"):
            ok = (p not in allp) if P.silent else (in_np and p not in ov and t["ps"][p].get("desc") is not None)
        elif m == "omit":
            ok = p not in onp and p not in ov and P.can_omit
        else:
            raise ValueError(m)
        if not ok:
            return False
    return True


def render_tpl(D, I, t, tpl):
    s = expand_facts(tpl, I, t)

    def seg(m):
        a, b = occ(m.group(1))
        if any(t["ps"][p]["mode"] == "omit" for p in a) or any(t["ps"][p]["mode"] != "present" for p in b):
            return ""
        return m.group(1)
    s = SEG_RE.sub(seg, s)

    def fill(m):
        if m.group(2):
            p = m.group(2)
            ps, P = t["ps"][p], D.params[p]
            if ps["mode"] == "present":
                out = P.np[int(ps["r"] * len(P.np))].format(v=ps["value"])
            elif ps["mode"] in ("ctx", "ctx_none"):
                out = ps["desc"]
            elif ps["mode"] == "vague":
                out = P.vague[int(ps["r2"] * len(P.vague))]
            else:
                raise ValueError(ps["mode"])
            if m.group(1) and not (ps["mode"] == "present" and out.startswith(str(ps["value"]))):
                out = cap(out)  # a value that starts the sentence keeps its own spelling (usernames, service names)
            return out
        if m.group(3):
            return t["ps"][m.group(3)]["value"]
        return t["x"][m.group(4)]
    s = SLOT_RE.sub(fill, s)
    assert "<" not in s and "{" not in s and "[" not in s, s
    return re.sub(r"\s+", " ", s).strip()


WRAPS = ["Please {vp}.", "Could you {vp}?", "I need you to {vp}."]
DONE = ["I was going to ask you to {vp}, but I've already done that myself.",
        "No need to {vp} any more - I managed it myself this morning."]
WITHDRAWN = ["Please don't {vp} after all; I've changed my mind.",
             "Forget what I said earlier about needing you to {vp} - I no longer want that."]
MARKERS = ["Most urgent: ", "This is the most urgent one: ", "Top priority: "]


def candidates(I):
    return list(I.q) + [w.replace("{vp}", v) for v in I.vp for w in WRAPS]


def pick_tpl(D, tb, tt, lst, open_task):
    I = D.intents[tb["intent"]]
    both = [x for x in lst if compat(D, I, tb, x, open_task) and (tt is None or compat(D, I, tt, x, open_task))]
    if both:
        return both[int(tb["tr"] * len(both))], both[int(tb["tr"] * len(both))]
    a = [x for x in lst if compat(D, I, tb, x, open_task)]
    b = [x for x in lst if tt is not None and compat(D, I, tt, x, open_task)]
    if not a or (tt is not None and not b):
        raise Invalid(f"no template for {tb['intent']}")
    return a[int(tb["tr"] * len(a))], (b[int(tb["tr"] * len(b))] if tt is not None else None)


# =============================================================================================== world state
def has(D, t, p):
    I = D.intents[t["intent"]]
    if I.implicit and p in I.implicit(t):
        return True
    if p not in t["ps"] or p not in relevant(I, t):
        return False
    return t["ps"][p]["mode"] in ("present", "ctx")


def new_world(rng, D):
    W = {"dom": D.name, "org": rng.choice(D.orgs), "sess": {}, "lists": collections.defaultdict(list), "limits": {},
         "bans": [], "tasks": [], "catalog": None, "used_keys": collections.defaultdict(set), "used_names": set(),
         "today": dt.date(2025, 9, 1) + dt.timedelta(days=rng.randint(0, 420))}
    f, l = person(rng, W["used_names"])
    W["names"] = {"first": f, "last": l, "name": f"{f} {l}"}
    D.init(rng, W)
    kinds = ["first", "urgent"] + (["tier"] if D.tiers else [])
    W["rule"] = {"kind": rng.choice(kinds)}
    W["style"] = {k: rng.random() for k in ("sess", "rules", "layout", "greet", "close", "instr", "l1", "l2", "l3", "l4",
                                             "ban", "conn", "opt", "mention", "marker", "subj")}
    W["style"]["order_seed"] = rng.randrange(1 << 30)
    return W


def default_mode(rng, D, p):
    P = D.params[p]
    if P.ctx is not None and P.silent:
        return "ctx"
    return rng.choice(P.provided)


def new_ps(rng, D, W, t, p, mode):
    P = D.params[p]
    g = P.gen(rng, W, t)
    ps = {"mode": None, "r": rng.random(), "r2": rng.random(), "value": g["value"], "num": g.get("num"),
          "attrs": dict(g.get("attrs", {})), "key": g.get("key"), "desc": None, "entry": None, "rel": g.get("rel", False)}
    if P.ctx is not None and P.ctx.kind == "list":
        ps["attrs"]["lkey"] = (ps["key"] or "").lower()
        ps["entry"] = P.ctx.entry.format(v=ps["value"], key=ps["key"], **ps["attrs"])
        ps["desc"] = P.ctx.desc[int(ps["r"] * len(P.ctx.desc))].format(key=ps["key"], **ps["attrs"])
        W["used_keys"][P.ctx.field].add(ps["key"])
    elif P.ctx is not None and P.ctx.kind == "field":
        if P.ctx.desc:
            ps["desc"] = P.ctx.desc[int(ps["r"] * len(P.ctx.desc))]
    elif P.ctx is not None and P.ctx.kind == "self":
        ps["desc"] = P.ctx.desc[int(ps["r"] * len(P.ctx.desc))]
        ps["other"] = g["value"]
        if ps["other"] == W["requester_user"]:
            raise Invalid("other username equals requester")
    t["ps"][p] = ps
    set_mode(D, W, t, p, mode)
    return ps


def set_mode(D, W, t, p, mode):
    P, ps = D.params[p], t["ps"][p]
    ps["mode"] = mode
    if P.ctx is None:
        assert mode in ("present", "vague", "omit"), (p, mode)
        return
    c = P.ctx
    if c.kind == "field":
        if P.silent:
            assert mode == "ctx"
            W["sess"][c.field] = c.fmt.format(v=ps["value"], name=W["names"]["name"], **ps["attrs"])
            return
        W["sess"][c.field] = c.fmt.format(v=ps["value"], **ps["attrs"]) if mode == "ctx" else c.none
    elif c.kind == "list":
        L = W["lists"][c.field]
        here = [e for e in L if e["value"] == ps["value"] and e.get("task")]
        want = mode == "ctx" or (c.always and mode in ("present", "vague"))
        if want and not here:
            L.append({"key": ps["key"], "value": ps["value"], "text": ps["entry"], "attrs": ps["attrs"], "task": True,
                      "pos": ps["r2"]})
        if not want:
            W["lists"][c.field] = [e for e in L if not (e["value"] == ps["value"] and e.get("task"))]
    elif c.kind == "self":
        assert mode in ("ctx", "present", "vague")
        ps["value"] = W["requester_user"] if mode == "ctx" else ps["other"]


def make_task(rng, D, W, intent, facts=None, modes=None):
    I = D.intents[intent]
    t = {"intent": intent, "facts": {}, "fr": {}, "ps": {}, "x": {}, "status": "open", "urgent": False, "mention": None,
         "tr": rng.random(), "sr": rng.random()}
    for f, vals in I.facts.items():
        t["facts"][f] = (facts or {}).get(f, rng.choice(vals))
    for fam in I.phrases:
        t["fr"][fam] = rng.randrange(1000)
    t["x"] = I.extras(rng, W, t) if I.extras else {}
    for p in I.params:
        new_ps(rng, D, W, t, p, (modes or {}).get(p) or default_mode(rng, D, p))
    if I.excl:  # exactly one of these identifiers is given (the others are not mentioned)
        keep = rng.choice(I.excl)
        for p in I.excl:
            if p != keep:
                set_mode(D, W, t, p, "omit")
    return t


def fill_lists(rng, D, W):
    for field, mn in D.list_min.items():
        L = W["lists"][field]
        guard = 0
        while len(L) < mn + (1 if rng.random() < 0.4 else 0):
            guard += 1
            if guard > 20:
                raise Invalid("fill")
            g = D.fillers[field](rng, W, None)
            if g is None:
                break
            if g["key"] in W["used_keys"][field] or any(e["key"] == g["key"] for e in L):
                continue
            attrs = dict(g.get("attrs", {}))
            attrs["lkey"] = g["key"].lower()
            P = next(P for P in D.params.values() if P.ctx is not None and getattr(P.ctx, "field", None) == field)
            L.append({"key": g["key"], "value": g["value"], "text": P.ctx.entry.format(v=g["value"], key=g["key"], **attrs),
                      "attrs": attrs, "task": False, "pos": rng.random()})


def refresh_entry(D, W, field, e):
    P = next(P for P in D.params.values() if P.ctx is not None and getattr(P.ctx, "field", None) == field)
    e["text"] = P.ctx.entry.format(v=e["value"], key=e["key"], **e["attrs"])


# =============================================================================================== primary evaluator
def cond_ok(D, W, t, c):
    if c is None:
        return True
    if c[0] == "fact":
        return t["facts"][c[1]] == c[2]
    if c[0] == "and":
        return all(cond_ok(D, W, t, x) for x in c[1:])
    if c[0] == "over":
        p, tool = c[1], c[2]
        if not has(D, t, p):
            raise Invalid("over on a missing value")
        lim = next(r.lim for r in D.tools[tool].restr if r.kind == "max" and r.param == p)
        return t["ps"][p]["num"] > W["limits"][lim]
    raise ValueError(c)


def fits(D, W, t, tool):
    return any(tn == tool and cond_ok(D, W, t, c) for tn, c in D.intents[t["intent"]].fits)


def blocked(D, W, t, tool):
    if tool in W["bans"]:
        return True
    return any(r.blocked(D, W, t) for r in D.tools[tool].restr)


def cat_tiers(D, W):
    return [[x for x in tier if x in W["catalog"]] for tier in D.tiers if any(x in W["catalog"] for x in tier)]


def task_tier(D, W, t, tiers):
    tools = [x for x, c in D.intents[t["intent"]].fits if x in W["catalog"]]
    lv = {next((i for i, tier in enumerate(tiers) if x in tier), len(tiers)) for x in tools}
    if len(lv) != 1:
        raise Invalid("tools of one request in different tiers")
    return lv.pop()


def select(D, W):
    open_ = [t for t in W["tasks"] if t["status"] == "open"]
    if not open_:
        raise Invalid("no open request")
    if len(W["tasks"]) == 1:
        return open_[0]
    k = W["rule"]["kind"]
    if k == "first":
        return open_[0]
    if k == "urgent":
        u = [t for t in open_ if t["urgent"]]
        if len(u) > 1 or any(t["urgent"] and t["status"] != "open" for t in W["tasks"]):
            raise Invalid("urgent marks")
        return u[0] if u else open_[0]
    tiers = cat_tiers(D, W)
    return min(open_, key=lambda t: (task_tier(D, W, t, tiers), W["tasks"].index(t)))


def evaluate(D, W):
    t = select(D, W)
    M = [x for x in W["catalog"] if fits(D, W, t, x)]
    if not M:
        raise Invalid("nothing fits")
    A = [x for x in M if not blocked(D, W, t, x)]
    info = {"request": t["intent"], "request_index": W["tasks"].index(t), "fitting": M, "permitted": A}
    if not A:
        return REF, info
    R = [x for x in A if all(has(D, t, p) for p in D.tools[x].req)]
    info["with_all_values"] = R
    info["missing"] = {x: [p for p in D.tools[x].req if not has(D, t, p)] for x in A if x not in R}
    if len(R) > 1:
        raise Invalid("two tools qualify")
    return (R[0] if R else ASK), info


# =============================================================================================== scenario helpers
def set_clause(rng, D, W, t, r, block):
    k = r.kind
    if k in ("allow", "deny"):
        dom = D.values[r.field]
        bad = [v for v in dom if (v not in r.values if k == "allow" else v in r.values)]
        good = [v for v in dom if v not in bad]
        W["sess"][r.field] = rng.choice(bad if block else good)
    elif k == "max":
        ps = t["ps"][r.param]
        if ps["mode"] not in ("present",):
            set_mode(D, W, t, r.param, "present")
        lim = W["limits"][r.lim]
        step = {"pay": [100, 250, 500], "rep": [4, 8, 10], "bags": [1, 2], "temp": [1, 2]}[r.lim]
        if block:
            n = lim + rng.choice(step)
        else:
            n = lim if rng.random() < 0.45 else lim - rng.choice(step)
        ps["num"] = n
        ps["value"] = {"pay": money, "rep": str, "temp": str,
                       "bags": lambda x: f"{x} extra bag{'s' if x > 1 else ''}"}[r.lim](n)
        ps["boundary"] = n == lim
    elif k == "self_or_role":
        if block:
            if t["ps"][r.param]["mode"] == "ctx":
                raise Invalid("self request cannot be blocked")
            W["sess"]["role"] = rng.choice([v for v in D.values["role"] if v not in r.roles])
        else:
            W["sess"]["role"] = rng.choice(r.roles)
    elif k == "fare":
        e = find_entry(W, "bookings on file", t["ps"][r.param]["value"])
        if e is None:
            raise Invalid("fare: booking not on file")
        e["attrs"]["fare"] = rng.choice(r.values) if block else rng.choice(["Standard", "Flex"])
        refresh_entry(D, W, "bookings on file", e)
    elif k == "ifp":
        if t["ps"][r.param]["value"] != r.pval or t["ps"][r.param]["mode"] != "present":
            t["ps"][r.param]["value"] = r.pval
            set_mode(D, W, t, r.param, "present")
        set_clause(rng, D, W, t, r.inner, block)
    else:
        raise ValueError(k)


def permit(rng, D, W, t, tool):
    W["bans"] = [b for b in W["bans"] if b != tool]
    for r in D.tools[tool].restr:
        try:
            if r.blocked(D, W, t):
                set_clause(rng, D, W, t, r, False)
        except Invalid:
            pass


def tools_for(D, W, t):
    """Tools that fit the task under its facts (ignoring 'over' conditions)."""
    out = []
    for tn, c in D.intents[t["intent"]].fits:
        try:
            if cond_ok(D, W, t, c):
                out.append(tn)
        except Invalid:
            pass
    return out


def missing_modes(D, t, p):
    P, ps = D.params[p], t["ps"][p]
    out = []
    pm = "present" if "present" in P.provided else P.provided[0]
    if P.vague:
        out.append(("vague", pm))
    if P.can_omit and "present" in P.provided:
        out.append(("omit", "present"))
    if P.ctx is not None and P.ctx.kind in ("field", "list") and not P.silent:
        out.append(("ctx_none", "ctx"))
    return out


def build_catalog(rng, D, W, exclude=(), extra=()):
    must = set(extra)
    for t in W["tasks"]:
        must |= {x for x, c in D.intents[t["intent"]].fits}
    must -= set(exclude)
    for x in list(must):
        if D.tools[x].fallback_of:
            must.add(D.tools[x].fallback_of)
    pool = [x for x in D.tools if x not in must and x not in exclude]
    hi = min(12, len(must) + len(pool))
    lo = max(5, len(must))
    if lo > hi:
        raise Invalid("catalog size")
    n = rng.randint(lo, hi)
    cat = sorted(must) + rng.sample(pool, n - len(must))
    for x in list(cat):
        fb = D.tools[x].fallback_of
        if fb and fb not in cat:
            raise Invalid("fallback without primary")
    W["catalog"] = sorted(cat)


def lookups_to_exclude(D, W):
    ex = set()
    for t in W["tasks"]:
        for p, ps in t["ps"].items():
            if ps["mode"] in ("vague", "omit", "ctx_none"):
                ex |= set(D.lookups.get(p, ()))
    return ex


# =============================================================================================== pair builders
def fact_intents(D):
    out = []
    for I in D.intents.values():
        facs = [c for tn, c in I.fits if c is not None and c[0] == "fact"]
        if I.facts and len({c[2] for c in facs}) >= 2:
            out.append(I)
    return out


def restricted(D):
    return [x for x in D.tools if D.tools[x].restr and not D.tools[x].fallback_of]


def intents_for_tool(D, tool):
    out = []
    for I in D.intents.values():
        for tn, c in I.fits:
            if tn == tool and (c is None or c[0] == "fact"):
                out.append((I, {c[1]: c[2]} if c else {}))
    return out


def b_lookalike(rng, D, W):
    I = rng.choice(fact_intents(D))
    f = next(iter(I.facts))
    v0, v1 = rng.sample(I.facts[f], 2)
    t = make_task(rng, D, W, I.name, facts={f: v0})
    W["tasks"] = [t]
    build_catalog(rng, D, W)
    for x in D.intents[I.name].fits:
        permit(rng, D, W, t, x[0])

    def flip(Wt):
        Wt["tasks"][0]["facts"][f] = v1
    return flip, ("tool", "tool"), {"flip": f"fact {f}: {v0} -> {v1}"}


def b_lookparam(rng, D, W):
    t = make_task(rng, D, W, "where_is")
    W["tasks"] = [t]
    kind = rng.choice(["tt", "tt", "at"])
    if kind == "tt":
        a, b = rng.sample(["order_id", "tracking_number"], 2)
        set_mode(D, W, t, a, "ctx" if a == "order_id" and rng.random() < 0.3 else "present")
        set_mode(D, W, t, b, "omit")
        build_catalog(rng, D, W)

        def flip(Wt):
            tt = Wt["tasks"][0]
            set_mode(D, Wt, tt, a, "omit")
            set_mode(D, Wt, tt, b, "present")
        return flip, ("tool", "tool"), {"flip": f"identifier given: {a} -> {b}"}
    mm = rng.choice(["vague", "omit", "ctx_none"])
    set_mode(D, W, t, "order_id", mm)
    set_mode(D, W, t, "tracking_number", "omit")
    pm = "ctx" if mm == "ctx_none" else "present"
    build_catalog(rng, D, W, exclude=D.lookups.get("order_id", ()))

    def flip(Wt):
        set_mode(D, Wt, Wt["tasks"][0], "order_id", pm)
    return flip, ("ask", "tool"), {"flip": f"order_id {mm} -> {pm}"}


def main_tool(D, W, t):
    """The non-fallback tool that fits the request under its facts, preferring one whose values are all stated."""
    tl = [x for x in tools_for(D, W, t) if not D.tools[x].fallback_of]
    full = [x for x in tl if all(has(D, t, p) for p in D.tools[x].req)]
    if not tl:
        raise Invalid("no main tool")
    return (full or tl)[0]


def reblock_others(rng, D, W, t, tool, keep):
    """After blocking one clause, make every other clause of the tool permit the request (one decisive clause)."""
    for r in D.tools[tool].restr:
        if r is keep:
            continue
        if r.blocked(D, W, t):
            set_clause(rng, D, W, t, r, False)
    if not keep.blocked(D, W, t):
        raise Invalid("clause no longer blocks")


def b_missing(rng, D, W):
    I = rng.choice(list(D.intents.values()))
    t = make_task(rng, D, W, I.name)
    W["tasks"] = [t]
    tool = main_tool(D, W, t)
    if not all(has(D, t, p) for p in D.tools[tool].req):
        raise Invalid("tool lacks values before the flip")
    opts = [(p, mm, pm) for p in D.tools[tool].req if p in relevant(I, t) for mm, pm in missing_modes(D, t, p)]
    if not opts:
        raise Invalid("nothing missable")
    p, mm, pm = rng.choice(opts)
    set_mode(D, W, t, p, mm)
    build_catalog(rng, D, W, exclude=lookups_to_exclude(D, W))
    permit(rng, D, W, t, tool)

    def flip(Wt):
        set_mode(D, Wt, Wt["tasks"][0], p, pm)
    return flip, ("ask", "tool"), {"flip": f"{p}: {mm} -> {pm}"}


def b_restricted(rng, D, W):
    use_ban = rng.random() < 0.25
    tool = rng.choice(list(D.tools) if use_ban else restricted(D))
    if D.tools[tool].fallback_of:
        raise Invalid("fallback")
    I, facts = rng.choice(intents_for_tool(D, tool))
    t = make_task(rng, D, W, I.name, facts=facts)
    W["tasks"] = [t]
    if tool not in tools_for(D, W, t):
        raise Invalid("tool does not fit")
    ex = {fb.name for fb in D.tools.values() if fb.fallback_of == tool}
    build_catalog(rng, D, W, exclude=ex)
    permit(rng, D, W, t, tool)
    if use_ban:
        others = [x for x in W["catalog"] if x != tool and x not in tools_for(D, W, t)]
        other = rng.choice(others)
        W["bans"] = [tool]

        def flip(Wt):
            Wt["bans"] = [other]
        return flip, ("refuse", "tool"), {"flip": f"switched-off tool: {tool} -> {other}"}
    r = rng.choice(D.tools[tool].restr)
    set_clause(rng, D, W, t, r, True)
    reblock_others(rng, D, W, t, tool, r)

    def flip(Wt):
        set_clause(rng, D, Wt, Wt["tasks"][0], r, False)
    return flip, ("refuse", "tool"), {"flip": f"restriction ({r.kind}) of {tool}: blocked -> permitted"}


def b_fallback(rng, D, W):
    if not D.fb:
        raise Invalid("no fallback")
    intent, facts, p, lim, prim, fb = rng.choice(D.fb)
    t = make_task(rng, D, W, intent, facts=facts)
    W["tasks"] = [t]
    with_fb = rng.random() < 0.7
    build_catalog(rng, D, W, exclude=() if with_fb else (fb,), extra=(fb,) if with_fb else ())
    for x in (prim, fb):
        for r in D.tools[x].restr:
            if r.kind != "max":
                set_clause(rng, D, W, t, r, False)
    r = next(r for r in D.tools[prim].restr if r.kind == "max")
    set_clause(rng, D, W, t, r, True)

    def flip(Wt):
        set_clause(rng, D, Wt, Wt["tasks"][0], r, False)
    return flip, (("tool", "tool") if with_fb else ("refuse", "tool")), \
        {"flip": f"{p}: above -> at or under the {prim} limit" + ("" if with_fb else " (no fallback tool in the catalog)")}


def b_refuse_ask(rng, D, W):
    tool = rng.choice(restricted(D))
    cl = [r for r in D.tools[tool].restr if r.kind in ("allow", "deny")]
    if not cl:
        raise Invalid("no session clause")
    I, facts = rng.choice(intents_for_tool(D, tool))
    t = make_task(rng, D, W, I.name, facts=facts)
    W["tasks"] = [t]
    if tool not in tools_for(D, W, t):
        raise Invalid("tool does not fit")
    opts = [(p, mm) for p in D.tools[tool].req if p in relevant(I, t) for mm, pm in missing_modes(D, t, p)]
    if not opts:
        raise Invalid("nothing missable")
    p, mm = rng.choice(opts)
    set_mode(D, W, t, p, mm)
    build_catalog(rng, D, W, exclude=lookups_to_exclude(D, W))
    permit(rng, D, W, t, tool)
    r = rng.choice(cl)
    set_clause(rng, D, W, t, r, True)

    def flip(Wt):
        set_clause(rng, D, Wt, Wt["tasks"][0], r, False)
    return flip, ("refuse", "ask"), {"flip": f"restriction ({r.kind}) of {tool}: blocked -> permitted, while {p} stays {mm}"}


def b_mention(rng, D, W):
    if D.name == "retail" and rng.random() < 0.35:
        t = make_task(rng, D, W, "where_is")
        W["tasks"] = [t]
        a, b = rng.sample(["order_id", "tracking_number"], 2)
        set_mode(D, W, t, a, "present")
        set_mode(D, W, t, b, "omit")
        t["mention"] = "track_package" if b == "tracking_number" else "get_order_status"
        build_catalog(rng, D, W)

        def flip(Wt):
            tt = Wt["tasks"][0]
            set_mode(D, Wt, tt, a, "omit")
            set_mode(D, Wt, tt, b, "present")
        return flip, ("tool", "tool"), {"flip": f"identifier given: {a} -> {b}", "mention": t["mention"]}
    flip, exp, info = b_lookalike(rng, D, W)
    t = W["tasks"][0]
    I = D.intents[t["intent"]]
    f = next(iter(I.facts))
    other = [x for x in I.facts[f] if x != t["facts"][f]][0]
    t["mention"] = next(tn for tn, c in I.fits if c is not None and c[0] == "fact" and c[2] == other)
    info["mention"] = t["mention"]
    return flip, exp, info


def missable(D, p):
    P = D.params[p]
    return bool(P.vague) or P.can_omit or (P.ctx is not None and not P.silent)


def clash(D, pa, pb):
    """Two requests clash when they share a parameter that can be missing, or a session field that supplies values."""
    fa = {D.params[p].ctx.field for p in pa if D.params[p].ctx is not None}
    fb = {D.params[p].ctx.field for p in pb if D.params[p].ctx is not None}
    return any(missable(D, p) for p in pa & pb) or bool(fa & fb)


def b_multi(rng, D, W):
    kind = W["rule"]["kind"]
    outcome = rng.choice(["tool", "tool", "ask", "refuse"])
    names = list(D.intents)
    ia, ib = rng.sample(names, 2)
    A = make_task(rng, D, W, ia)
    B = make_task(rng, D, W, ib)
    pa = {p for p in relevant(D.intents[ia], A) if not D.params[p].silent}
    pb = {p for p in relevant(D.intents[ib], B) if not D.params[p].silent}
    ta, tb = tools_for(D, W, A), tools_for(D, W, B)
    if clash(D, pa, pb) or set(ta) & set(tb) or any(D.tools[x].fallback_of for x in ta + tb):
        raise Invalid("requests clash")
    toolA, toolB = main_tool(D, W, A), main_tool(D, W, B)
    if not all(has(D, B, p) for p in D.tools[toolB].req) or not all(has(D, A, p) for p in D.tools[toolA].req):
        raise Invalid("values missing before configuration")
    extra_tasks = []
    if rng.random() < 0.35:
        ic = rng.choice([n for n in names if n not in (ia, ib)])
        C = make_task(rng, D, W, ic)
        pc = {p for p in relevant(D.intents[ic], C) if not D.params[p].silent}
        if not clash(D, pc, pa | pb) and not set(tools_for(D, W, C)) & set(ta + tb):
            C["status"] = rng.choice(["done", "withdrawn"])
            extra_tasks.append(C)
    W["tasks"] = list(extra_tasks)
    pos = rng.randint(0, len(W["tasks"]))
    W["tasks"][pos:pos] = [A, B]  # A directly before B; a done or withdrawn request may come before or after them
    if outcome == "ask":
        opts = [(p, mm) for p in D.tools[toolA].req if p in relevant(D.intents[ia], A) for mm, pm in missing_modes(D, A, p)]
        if not opts:
            raise Invalid("A not missable")
        p, mm = rng.choice(opts)
        set_mode(D, W, A, p, mm)
    ex = lookups_to_exclude(D, W)
    for x in ta:
        ex |= {fbt.name for fbt in D.tools.values() if fbt.fallback_of == x}
    build_catalog(rng, D, W, exclude=ex)
    permit(rng, D, W, B, toolB)
    permit(rng, D, W, A, toolA)
    if outcome == "refuse":
        if D.tools[toolA].restr and rng.random() < 0.7:
            r = rng.choice(D.tools[toolA].restr)
            set_clause(rng, D, W, A, r, True)
            reblock_others(rng, D, W, A, toolA, r)
        else:
            W["bans"] = [toolA]
    flipk = rng.choice(["status", "order"] if kind == "first" else ["status", "urgent"] if kind == "urgent" else ["status"])
    if kind == "urgent" and (flipk == "urgent" or rng.random() < 0.5):
        A["urgent"] = True
    if kind == "first" and rng.random() < 0.2:
        B["urgent"] = True  # a 'most urgent' marker that the first-request rule ignores
    if kind == "tier":
        tiers = cat_tiers(D, W)
        if not tiers:
            raise Invalid("no tiers in catalog")
        la, lb = task_tier(D, W, A, tiers), task_tier(D, W, B, tiers)
        if la > lb or la == len(tiers):
            raise Invalid("tier order")
        if la < lb and rng.random() < 0.5:
            i, j = W["tasks"].index(A), W["tasks"].index(B)
            W["tasks"][i], W["tasks"][j] = W["tasks"][j], W["tasks"][i]  # the higher tier comes second in the message
    st = rng.choice(["done", "withdrawn"])

    def flip(Wt):
        At = next(x for x in Wt["tasks"] if x["intent"] == ia)
        Bt = next(x for x in Wt["tasks"] if x["intent"] == ib)
        if flipk == "status":
            At["status"] = st
            At["urgent"] = False
        elif flipk == "order":
            i, j = Wt["tasks"].index(At), Wt["tasks"].index(Bt)
            Wt["tasks"][i], Wt["tasks"][j] = Wt["tasks"][j], Wt["tasks"][i]
        else:
            At["urgent"], Bt["urgent"] = False, True
    return flip, (outcome, "tool"), {"flip": f"multi-request ({kind} rule): {flipk}", "requests": [ia, ib]}


BUILDERS = {"lookalike": b_lookalike, "lookparam": b_lookparam, "missing": b_missing, "restricted": b_restricted,
            "fallback": b_fallback, "refuse_ask": b_refuse_ask, "mention": b_mention, "multi": b_multi}


def gold_kind(g):
    return "ask" if g == ASK else "refuse" if g == REF else "tool"


def build_pair(rng, D, ptype):
    W = new_world(rng, D)
    if ptype == "lookparam" and D.name != "retail":
        raise Invalid("lookparam is retail only")
    flip, exp, info = BUILDERS[ptype](rng, D, W)
    if ptype != "multi":
        W["rule"]["kind"] = rng.choice(["first", "urgent"] + (["tier"] if D.tiers else []))
    fill_lists(rng, D, W)
    Wt = copy.deepcopy(W)
    flip(Wt)
    gb, ib = evaluate(D, W)
    gt, it = evaluate(D, Wt)
    if (gold_kind(gb), gold_kind(gt)) != exp or gb == gt:
        raise Invalid(f"expectation {exp} vs {gb}/{gt}")
    decoy_sess(D, W, Wt, gb, gt, ib, it)
    if rng.random() < 0.5 and ptype not in ("multi",):
        W, Wt, gb, gt, ib, it = Wt, W, gt, gb, it, ib  # the base row is the twin half the time
        info = dict(info, flip=reverse_flip(info["flip"]))  # describe the change from the (new) base to its twin
    return W, Wt, gb, gt, ib, it, info


FLIP_RE = re.compile(r"^(.*?: |order_id )(.+?) -> (.+?)((?:, while | \(no fallback).*)?$")


def reverse_flip(s):
    m = FLIP_RE.match(s)
    if not m:
        raise AssertionError(f"flip text not reversible: {s}")
    return f"{m.group(1)}{m.group(3)} -> {m.group(2)}{m.group(4) or ''}"


def decoy_sess(D, W, Wt, gb, gt, ib, it):
    """Re-draw every access-type session field (role, profile, account status, ...) that is equal in both halves of the
    pair, uniformly among the values that leave both labels and both evaluations unchanged, so that a blocking value
    (guest, staff, payment hold, viewer, ...) is not a shortcut to refuse_not_allowed.  Uses its own RNG, so the main
    stream (and every other pair) is unchanged."""
    r2 = random.Random(f"{SEED}:decoy:{W['style']['order_seed']}")
    for f in sorted(D.values):
        if f not in W["sess"] or W["sess"][f] != Wt["sess"][f]:
            continue
        cur, ok = W["sess"][f], []
        for v in D.values[f]:
            W["sess"][f] = Wt["sess"][f] = v
            try:
                same = evaluate(D, W) == (gb, ib) and evaluate(D, Wt) == (gt, it)
            except Invalid:
                same = False
            if same:
                ok.append(v)
        assert cur in ok, (f, cur, ok)
        W["sess"][f] = Wt["sess"][f] = r2.choice(ok)


# =============================================================================================== rendering
RULE_ONE = ["Each turn the assistant does exactly one thing: call one tool, ask the user one question, or decline.",
            "Per turn, make a single decision: one tool call, one clarifying question, or a refusal."]
RULE_VALS = ["Tool arguments may only use values stated in the conversation or the session details; never guess them and "
             "never call another tool just to look them up.",
             "Use only argument values that the user or the session details state; do not guess, and do not fetch missing "
             "values with other tools."]
RULE_NAMES = ["Choose a tool by what the user needs; a tool name the user mentions is only a suggestion.",
              "If the user names a tool, treat that as a hint, not an instruction - pick by the task."]
RULE_FIRST = ["If a message contains several requests, act on the first one written that the user still wants; requests "
              "already done or withdrawn do not count, and the others wait.",
              "When several requests arrive together, handle the earliest one in the message that is still wanted (ignore "
              "any the user has already done or called off); the rest wait."]
RULE_URGENT = ["If a message contains several requests, act on the one the user explicitly marks as most urgent; if none is "
               "marked, the first one written. Requests already done or withdrawn do not count.",
               "When several requests arrive together, handle the one the user flags as most urgent, or the earliest one if "
               "nothing is flagged; requests already done or called off do not count."]
BAN_TPL = ["The assistant must not call {t} in this channel.", "{t} is switched off for this deployment.",
           "Never use {t} here, whoever asks."]
INSTR = [
    "Given the tool catalog in the definitions and the rules, session details and conversation in the text, what is the "
    "assistant's correct next action?",
    "Using only the defined tools and the rules and session details shown, which single next step should the assistant take "
    "for this conversation?",
    "Which option is the assistant's correct next move here - one of the catalog tools, a clarifying question, or a refusal - "
    "applying the stated rules and session details?",
    "Acting as this assistant under the deployment rules and session details in the text, which one action should it take next?",
    "Apply the assistant rules and session details in the text to the tool definitions: what should the assistant do next?",
    "What is the single correct next action for the assistant - call one defined tool, ask a clarifying question, or refuse - "
    "given everything stated in the text?",
    "For the latest user message, which next action do the tool definitions, the assistant rules and the session details require?",
    "Choose the assistant's next action for this conversation, judging only by the tool catalog and the rules and session "
    "details it was given.",
]
MENTION = ["Could you use {t} for this?", "I think the tool you need is {t}.", "(Maybe run {t}?)", "Please just run {t}."]
GREET = ["", "Hi!", "Hello there.", "Hi there.", "Hey!"]
CLOSE = ["", "Thanks.", "Cheers!", "Thank you so much.", "Thanks in advance."]
CONN = ["", "Also, ", "And "]
SAFE_LC = {"Please", "Can", "Could", "Where", "What", "Any", "Is", "Has", "About", "Regarding", "Help", "Undo", "Traffic",
           "Set", "Lock", "Unlock", "Arm", "Turn", "Switch", "Show", "Quick", "Ship", "For", "Did", "Update", "How",
           "Something", "There's", "It's", "We", "Do", "My"}


def pick(xs, r):
    return xs[int(r * len(xs)) % len(xs)]


def rule_text(D, W):
    k, s = W["rule"]["kind"], W["style"]["l4"]
    if k == "first":
        return pick(RULE_FIRST, s)
    if k == "urgent":
        return pick(RULE_URGENT, s)
    tiers = cat_tiers(D, W)
    if not tiers:
        W["rule"]["kind"] = "first"
        return pick(RULE_FIRST, s)
    if s < 0.5:
        parts = [f"act first on one that needs {join_or(tiers[0])}"] + [f"then on one that needs {join_or(x)}" for x in tiers[1:]]
        return ("If a message contains several requests, " + "; ".join(parts) + "; otherwise the first one written. "
                "Requests already done or withdrawn do not count.")
    parts = [f"requests needing {join_or(tiers[0])} come first"] + [f"then requests needing {join_or(x)}" for x in tiers[1:]]
    return ("Priority when several requests arrive: " + "; ".join(parts) + "; then the rest in the order written. "
            "Requests already done or withdrawn do not count.")


def rules_block(D, W):
    st = W["style"]
    lines = [pick(RULE_ONE, st["l1"]), pick(RULE_VALS, st["l2"]), pick(RULE_NAMES, st["l3"]), rule_text(D, W)]
    for b in W["bans"]:
        lines.append(pick(BAN_TPL, st["ban"]).format(t=b))
    org = W["org"]
    f = int(st["rules"] * 3)
    if f == 0:
        return f"Assistant rules ({org}):\n" + "\n".join(f"{i + 1}. {l}" for i, l in enumerate(lines))
    if f == 1:
        return f"You are {D.assistant.format(org=org)}. Rules:\n" + "\n".join(f"- {l}" for l in lines)
    return f"DEPLOYMENT NOTES - {org} assistant\n" + "\n".join(f"* {l}" for l in lines)


def sess_items(D, W):
    out = []
    for f in D.sess_order:
        if f in D.list_min:
            L = sorted(W["lists"].get(f, []), key=lambda e: e["pos"])
            out.append((f, "; ".join(e["text"] for e in L) if L else "none"))
        else:
            out.append((f, W["sess"][f]))
    return out


def sess_block(D, W):
    items = sess_items(D, W)
    f = int(W["style"]["sess"] * 3)
    for k, v in items:
        assert " | " not in v and "\n" not in v and ": " not in k and " = " not in k, (k, v)
    if f == 0:
        return "Session details:\n" + "\n".join(f"- {cap(k)}: {v}" for k, v in items)
    if f == 1:
        return "SESSION | " + " | ".join(f"{k}: {v}" for k, v in items)
    return "[session]\n" + "\n".join(f"{k} = {v}" for k, v in items)


def lc_ok(s):
    w = s.split(" ")[0].rstrip(",")
    return w in SAFE_LC and w not in {"My"}


def render_conv(D, W, tpls):
    """tpls: per task (template chosen jointly with the twin).  Returns conversation text + per-task sentences."""
    st = W["style"]
    sents = []
    for i, t in enumerate(W["tasks"]):
        I = D.intents[t["intent"]]
        if t["status"] == "open":
            s = render_tpl(D, I, t, tpls[i])
        else:
            vp = render_tpl(D, I, t, tpls[i])
            s = pick(DONE if t["status"] == "done" else WITHDRAWN, t["sr"]).format(vp=vp)
        marker = pick(MARKERS, st["marker"]) if t["urgent"] else ""
        sents.append({"sent": s, "marker": marker})
    parts = []
    for i, x in enumerate(sents):
        s = x["marker"] + x["sent"]
        if i > 0 and not x["marker"]:
            c = pick(CONN, (st["conn"] + 0.37 * i) % 1)
            if c and lc_ok(x["sent"]):
                s = c + x["sent"][:1].lower() + x["sent"][1:]
                x["conn"] = c
        parts.append(s)
    t0 = W["tasks"][0]
    if len(W["tasks"]) == 1 and t0.get("mention"):
        parts.append(pick(MENTION, st["mention"]).format(t=t0["mention"]))
    g, c = pick(GREET, st["greet"]), pick(CLOSE, st["close"])
    msg = " ".join(x for x in [g] + parts + [c] if x)
    lay = pick(D.layouts, st["layout"])
    name, first = W["names"]["name"], W["names"]["first"]
    U = D.user_label
    if lay == "chat":
        conv = f"{U}: {msg}"
    elif lay == "chat2":
        conv = f"Assistant: Hi {first}, what can I do for you today?\n{U}: {msg}"
    elif lay == "email":
        subj = pick(["Quick request", "Help please", "A few things", "Question"], st["subj"])
        conv = f"Email to the assistant\nFrom: {name}\nSubject: {subj}\n\n{msg}\n\n{first}"
    elif lay == "voice":
        conv = f"[Voice message, transcribed] {msg}"
    elif lay == "slack":
        ch = {"workplace": "#assistant", "it_desk": "#it-help", "cloud_ops": "#ops-bot"}[D.name]
        conv = f"{ch} | {name}: @assistant {msg}"
    else:
        raise ValueError(lay)
    return conv, sents


def tool_def(D, W, name):
    T = D.tools[name]
    req = ", ".join(p + (f" ({D.params[p].gloss})" if p in D.params and D.params[p].gloss else "") for p in T.req)
    s = f"Tool {name}: {T.desc} Required: {req}."
    if T.opt:
        s += f" Optional: {', '.join(T.opt)}."
    s += " Restriction: " + ("; ".join(r.text(W) for r in T.restr) if T.restr else "none") + "."
    return s


def render_pair(D, Wb, Wt):
    tb, tt = Wb["tasks"], Wt["tasks"]
    assert sorted(x["intent"] for x in tb) == sorted(x["intent"] for x in tt) and len({x["intent"] for x in tb}) == len(tb)
    ch_b, ch_t = {}, {}
    for a in tb:
        b = next(x for x in tt if x["intent"] == a["intent"])
        I = D.intents[a["intent"]]
        if a["status"] == "open" and b["status"] == "open":
            x, y = pick_tpl(D, a, b, candidates(I), True)
        elif a["status"] != "open" and b["status"] != "open":
            x, y = pick_tpl(D, a, b, I.vp, False)
        else:
            xo, _ = pick_tpl(D, a, None, candidates(I) if a["status"] == "open" else I.vp, a["status"] == "open")
            yo, _ = pick_tpl(D, b, None, candidates(I) if b["status"] == "open" else I.vp, b["status"] == "open")
            x, y = xo, yo
        ch_b[a["intent"]] = x
        ch_t[a["intent"]] = y
    out = []
    for W, ch in ((Wb, ch_b), (Wt, ch_t)):
        conv, sents = render_conv(D, W, [ch[x["intent"]] for x in W["tasks"]])
        state = rules_block(D, W) + "\n\n" + sess_block(D, W) + "\n\n" + conv
        out.append((state, conv, sents))
    return out


# =============================================================================================== independent re-check
def parse_rules(txt):
    lines = txt.split("\n")[1:]
    body = " ".join(re.sub(r"^(?:\d+\. |- |\* )", "", l) for l in lines)
    if "act first on one that needs" in body or "Priority when several requests arrive" in body:
        kind = "tier"
        seg = body[body.find("several requests"):]
        seg = seg[:seg.find("Requests already done")]
        tiers = [split_or(m) for m in re.findall(r"need(?:s|ing) ([a-z_]+(?:(?:, | or )[a-z_]+)*)", seg)]
    elif "marks as most urgent" in body or "flags as most urgent" in body:
        kind, tiers = "urgent", []
    elif "first one written that the user still wants" in body or "earliest one in the message that is still wanted" in body:
        kind, tiers = "first", []
    else:
        raise AssertionError("rule not found")
    bans = re.findall(r"must not call ([a-z_]+) in this channel", body) + re.findall(r"([a-z_]+) is switched off for this", body) \
        + re.findall(r"Never use ([a-z_]+) here", body)
    return kind, tiers, bans


def parse_sess(txt):
    lines = txt.split("\n")
    out = {}
    if lines[0] == "Session details:":
        for l in lines[1:]:
            k, v = l[2:].split(": ", 1)
            out[k.lower()] = v
    elif lines[0].startswith("SESSION | "):
        for part in lines[0].split(" | ")[1:]:
            k, v = part.split(": ", 1)
            out[k.lower()] = v
    else:
        assert lines[0] == "[session]"
        for l in lines[1:]:
            k, v = l.split(" = ", 1)
            out[k.lower()] = v
    return out


def parse_clause(c):
    m = re.fullmatch(r"for (\w+) (\w+), (.+)", c)
    if m:
        return ("ifp", m.group(1), m.group(2), parse_clause(m.group(3)))
    m = re.fullmatch(r"only when (.+?) is (.+)", c)
    if m:
        return ("allow", m.group(1).lower(), split_or(m.group(2)))
    m = re.fullmatch(r"not available when (.+?) is (.+)", c)
    if m:
        return ("deny", m.group(1).lower(), split_or(m.group(2)))
    m = re.fullmatch(r"(\w+) must be at most (.+)", c)
    if m:
        return ("max", m.group(1), num_of(m.group(2)))
    m = re.fullmatch(r"only for the requester's own username unless role is (.+)", c)
    if m:
        return ("self_or_role", split_or(m.group(1)))
    m = re.fullmatch(r"not for bookings on a (.+?) fare \(see bookings on file\)", c)
    if m:
        return ("fare", split_or(m.group(1)))
    raise AssertionError(f"unparsed clause: {c}")


def parse_tool_def(name, d):
    assert d.startswith(f"Tool {name}: "), d
    req = re.search(r" Required: (.+?)\.(?: Optional| Restriction)", d).group(1)
    req = [re.sub(r" \(.*?\)$", "", x.strip()) for x in re.split(r", (?![^()]*\))", req)]
    rs = re.search(r" Restriction: (.+)\.$", d).group(1)
    clauses = [] if rs == "none" else [parse_clause(c) for c in rs.split("; ")]
    return {"req": req, "restr": clauses}


def recheck(D, row, chk):
    rules_txt, sess_txt, conv = row["state"].split("\n\n", 2)
    assert conv == chk["conv"]
    kind, tiers, bans = parse_rules(rules_txt)
    sess = parse_sess(sess_txt)
    defs = chk["defs"]
    assert list(defs) == row["options"] or set(defs) == set(row["options"])
    tools = {o: parse_tool_def(o, defs[o]) for o in row["options"] if o not in (ASK, REF)}
    assert set(tools) == set(chk["catalog"]) and 5 <= len(tools) <= 12
    tasks = chk["tasks"]
    pos = []
    for t, s in zip(tasks, chk["sents"]):
        i = conv.find(s["sent"][1:])  # the first letter may be lower-cased after a connector
        assert i >= 0, (s["sent"], conv)
        pos.append(i)
        if t["urgent"]:
            assert s["marker"] + s["sent"] in conv
        if t["status"] == "done":
            assert "already done that myself" in s["sent"] or "managed it myself" in s["sent"]
        if t["status"] == "withdrawn":
            assert "after all" in s["sent"] or "no longer want" in s["sent"]
    assert pos == sorted(pos)
    open_ = [i for i, t in enumerate(tasks) if t["status"] == "open"]
    if len(tasks) == 1:
        sel = open_[0]
    elif kind == "first":
        sel = open_[0]
    elif kind == "urgent":
        u = [i for i in open_ if tasks[i]["urgent"]]
        sel = u[0] if u else open_[0]
    else:
        def tier_of(i):
            ts = [x for x, c in D.intents[tasks[i]["intent"]].fits if x in tools]
            lv = {next((k for k, tr in enumerate(tiers) if x in tr), len(tiers)) for x in ts}
            assert len(lv) == 1
            return lv.pop()
        sel = min(open_, key=lambda i: (tier_of(i), i))
    t = tasks[sel]
    I = D.intents[t["intent"]]
    rel = I.rel(t["facts"]) if I.rel else list(I.params)
    impl = I.implicit(t) if I.implicit else {}

    def value2(p):
        if p in impl:
            for s in impl[p]:
                assert s in conv, (p, s)
            return True
        if p not in t["ps"] or p not in rel:
            return False
        ps, P = t["ps"][p], D.params[p]
        m = ps["mode"]
        if m == "present":
            assert ps["value"] in conv, (p, ps["value"])
            if P.ctx is not None and P.ctx.kind == "field" and not P.silent:
                assert sess[P.ctx.field] == P.ctx.none
            return True
        if m == "ctx":
            c = P.ctx
            if c.kind == "field":
                assert ps["value"] in sess[c.field], (p, sess[c.field])
            elif c.kind == "self":
                assert f"(username {ps['value']})" in sess[c.field]
            else:
                hits = [e for e in sess[c.field].split("; ") if re.search(r"\b" + re.escape(ps["key"]) + r"\b", e, re.I)]
                assert len(hits) == 1 and ps["value"] in hits[0], (p, hits)
            if not P.silent:
                assert ps["desc"].lower() in conv.lower(), (p, ps["desc"])
            return True
        # missing: no value of this kind anywhere in the conversation; the session does not supply it either
        assert not P.found(conv, [ps["value"]]), (p, m, conv)
        if P.ctx is not None:
            c = P.ctx
            if c.kind == "field":
                assert sess[c.field] == c.none, (p, sess[c.field])
            elif c.kind == "list":
                hits = [e for e in sess[c.field].split("; ") if re.search(r"\b" + re.escape(ps["key"]) + r"\b", e, re.I)]
                if m == "ctx_none":
                    assert not hits and ps["desc"].lower() in conv.lower(), (p, hits)
                else:  # vague: two or more entries are possible
                    assert len(sess[c.field].split("; ")) >= 2
        return False

    def cond2(c):
        if c is None:
            return True
        if c[0] == "fact":
            return t["facts"][c[1]] == c[2]
        if c[0] == "and":
            return all(cond2(x) for x in c[1:])
        if c[0] == "over":
            assert value2(c[1])
            lim = next(x[2] for x in tools[c[2]]["restr"] if x[0] == "max" and x[1] == c[1])
            return num_of(t["ps"][c[1]]["value"]) > lim
        raise ValueError(c)

    def clause2(cl):
        k = cl[0]
        if k == "allow":
            return sess[cl[1]] not in cl[2]
        if k == "deny":
            return sess[cl[1]] in cl[2]
        if k == "max":
            assert value2(cl[1])
            return num_of(t["ps"][cl[1]]["value"]) > cl[2]
        if k == "self_or_role":
            assert value2("username")
            me = re.search(r"\(username ([a-z.]+)\)", sess["requester"]).group(1)
            return t["ps"]["username"]["value"] != me and sess["role"] not in cl[1]
        if k == "fare":
            assert value2("booking_ref")
            e = [x for x in sess["bookings on file"].split("; ") if x.startswith(t["ps"]["booking_ref"]["value"] + ":")]
            assert len(e) == 1
            return re.search(r"\((\w+) fare\)", e[0]).group(1) in cl[1]
        if k == "ifp":
            assert value2(cl[1])
            return t["ps"][cl[1]]["value"] == cl[2] and clause2(cl[3])
        raise ValueError(k)

    M = [x for x in tools if any(tn == x and cond2(c) for tn, c in I.fits)]
    assert M
    A = [x for x in M if x not in bans and not any(clause2(cl) for cl in tools[x]["restr"])]
    if not A:
        g2 = REF
    else:
        R = [x for x in A if all(value2(p) for p in tools[x]["req"])]
        assert len(R) <= 1
        g2 = R[0] if R else ASK
    assert g2 == row["gold"], (row["rid"], g2, row["gold"])
    return True


# =============================================================================================== rows
def edges_for(D, W, g, info, ptype, state):
    e = []
    t = W["tasks"][info["request_index"]]
    if g == ASK:
        e.append("missing_info")
    if g == REF or any(D.tools[x].fallback_of for x in [g] if x in D.tools):
        e.append("exception")
    if any(ps.get("boundary") for ps in t["ps"].values()) or ptype == "fallback" or \
            any(r.kind == "max" for x in info["fitting"] for r in D.tools[x].restr):
        e.append("numeric")
    if any(ps["mode"] in ("ctx", "ctx_none") and not D.params[p].silent for p, ps in t["ps"].items() if p in relevant(D.intents[t["intent"]], t)):
        e.append("multi_hop")
    if len(W["tasks"]) > 1:
        e.append("multi_hop")
    if any(x["status"] == "withdrawn" for x in W["tasks"]):
        e.append("negation")
    if t.get("mention") or ptype in ("lookalike", "lookparam"):
        e.append("implicit")
    if any(ps.get("rel") and ps["mode"] == "present" for ps in t["ps"].values()) or "tomorrow" in state:
        e.append("temporal")
    if len(state) > 1400:
        e.append("long_context")
    e = [x for x in dict.fromkeys(e)]
    for x in e:
        assert x in EDGE_TAGS
    return ",".join(e) or None


def leak_free(D, W, inf, conv):
    """A value counted as missing must not appear in the conversation in any form of its kind, and a vague reference
    to a session list must have at least two candidates."""
    t = W["tasks"][inf["request_index"]]
    I = D.intents[t["intent"]]
    for p, ps in t["ps"].items():
        if p not in relevant(I, t) or ps["mode"] not in ("vague", "omit", "ctx_none"):
            continue
        if D.params[p].found(conv, [ps["value"]]):
            return False
        c = D.params[p].ctx
        if ps["mode"] == "vague" and c is not None and c.kind == "list" and len(W["lists"][c.field]) < 2:
            return False
    return True


def make_rows(D, idx, ptype, Wb, Wt, gb, gt, ib, it, info):
    (sb, cb, xb), (st, ct, xt) = render_pair(D, Wb, Wt)
    if sb == st:
        raise Invalid("twin identical")
    if not leak_free(D, Wb, ib, cb) or not leak_free(D, Wt, it, ct):
        raise Invalid("a missing value leaks into the conversation")
    defs = {x: tool_def(D, Wb, x) for x in Wb["catalog"]}
    defs_t = {x: tool_def(D, Wt, x) for x in Wt["catalog"]}
    if defs != defs_t:
        raise Invalid("twin changed a definition")
    defs.update(SPECIAL_DEFS)
    for k, v in defs.items():
        if len(v.split()) > 48:
            raise Invalid(f"def too long {k}")
    opts = list(Wb["catalog"]) + [ASK, REF]
    random.Random(Wb["style"]["order_seed"]).shuffle(opts)
    instr = pick(INSTR, Wb["style"]["instr"])
    did = f"{D.name}_{idx:03d}"
    rows = []
    for which, W, s, conv, sents, g, inf in (("base", Wb, sb, cb, xb, gb, ib), ("twin", Wt, st, ct, xt, gt, it)):
        rid = f"{KEY}-{D.name}-{idx:03d}" + ("-twin" if which == "twin" else "")
        orig = {"action": g, "action_kind": gold_kind(g), "pair_type": ptype, "rule": W["rule"]["kind"],
                "request_acted_on": inf["request"], "request_index": inf["request_index"],
                "fitting_tools": inf["fitting"], "permitted_fitting_tools": inf["permitted"],
                "permitted_with_all_values": inf.get("with_all_values"), "missing_values": inf.get("missing"),
                "switched_off": W["bans"], "twin_change": info["flip"],
                "requests": [{"type": t["intent"], "status": t["status"], "urgent": t["urgent"], "facts": t["facts"],
                              "values": {p: ps["mode"] for p, ps in t["ps"].items() if p in relevant(D.intents[t["intent"]], t)}}
                             for t in W["tasks"]]}
        if info.get("mention"):
            orig["mentioned_tool"] = info["mention"]
        meta = {"dataset": f"program generator golden_src/gen/{KEY}.py", "config": f"{D.name}:{ptype}", "revision": "gen-v1",
                "licence": "Generated by Claude-written program in this repo (no third-party text)", "split": "train",
                "orig_label": orig, "family": FAMILY, "edge": edges_for(D, W, g, inf, ptype, s), "defs": did}
        if which == "twin":
            meta["twin_of"] = f"{KEY}-{D.name}-{idx:03d}"
        chk = {"conv": conv, "defs": defs, "catalog": list(W["catalog"]), "sents": sents,
               "tasks": [{"intent": t["intent"], "facts": t["facts"], "status": t["status"], "urgent": t["urgent"],
                          "x": t["x"], "ps": {p: {k: ps[k] for k in ("mode", "value", "key", "desc")} for p, ps in t["ps"].items()}}
                         for t in W["tasks"]]}
        rows.append(({"key": KEY, "rid": rid, "state": s, "instructions": instr, "options": opts, "gold": g, "soft": None,
                      "meta": meta}, chk))
    return rows, did, defs


# =============================================================================================== main
PLAN = [("lookalike", 14), ("lookparam", 6), ("missing", 32), ("restricted", 28), ("fallback", 10), ("multi", 30),
        ("mention", 12), ("refuse_ask", 18)]


def append_manifest(rec):
    line = json.dumps(rec, ensure_ascii=False)
    for _ in range(20):
        text = MANIFEST.read_text() if MANIFEST.exists() else ""
        lines = text.splitlines()
        mine = [i for i, ln in enumerate(lines) if ln.strip() and json.loads(ln).get("key") == rec["key"]]
        if not mine:
            with open(MANIFEST, "a") as fh:
                fh.write(line + "\n")
            return
        if len(mine) == 1 and lines[mine[0]] == line:
            return
        for i in mine:
            assert json.loads(lines[i]).get("family") == FAMILY
        new = [ln for i, ln in enumerate(lines) if i not in set(mine)] + [line]
        tmp = MANIFEST.with_suffix(".jsonl.tmp_ts")
        tmp.write_text("\n".join(new) + "\n")
        if (MANIFEST.read_text() if MANIFEST.exists() else "") == text:
            os.replace(tmp, MANIFEST)
            return
        tmp.unlink()
        time.sleep(0.2)
    raise RuntimeError("manifest kept changing")


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    rows, chks, defs_out = [], [], {}
    seen = set()
    fails = collections.Counter()
    idx = 0
    di = 0
    for ptype, n in PLAN:
        made = 0
        tries = 0
        while made < n:
            tries += 1
            assert tries < n * 400, (ptype, made, fails.most_common(8))
            doms = [D for D in DOMAINS if (ptype != "lookparam" or D.name == "retail") and (ptype != "fallback" or D.fb)]
            D = doms[di % len(doms)]
            di += 1
            try:
                Wb, Wt, gb, gt, ib, it, info = build_pair(rng, D, ptype)
                pr, did, defs = make_rows(D, idx, ptype, Wb, Wt, gb, gt, ib, it, info)
            except Invalid as e:
                fails[(ptype, D.name, str(e)[:40])] += 1
                continue
            keys = [norm(r["state"]) + "||" + norm(r["instructions"]) for r, _ in pr]
            if any(k in seen for k in keys):
                fails[(ptype, "dup")] += 1
                continue
            seen.update(keys)
            for r, c in pr:
                rows.append(r)
                chks.append((D, c))
            defs_out[did] = defs
            made += 1
            idx += 1
        print(f"{ptype}: {made} pairs ({tries} tries)", flush=True)
    assert len(rows) <= MAX_ROWS
    # ------------------------------------------------------------ self-check every row (independent evaluator)
    for r, (D, c) in zip(rows, chks):
        recheck(D, r, c)
    src = Path(__file__).resolve()
    rev = "gen-v1+sha256:" + hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    for r in rows:
        r["meta"]["revision"] = rev
    check_rows(rows)
    by = {r["rid"]: r for r in rows}
    for r in rows:
        if "twin_of" in r["meta"]:
            b = by[r["meta"]["twin_of"]]
            assert b["gold"] != r["gold"] and b["instructions"] == r["instructions"] and b["options"] == r["options"]
            assert b["meta"]["defs"] == r["meta"]["defs"] and b["state"] != r["state"]
    out = Path(os.environ.get("TS_OUT") or RAW / f"{KEY}.jsonl")
    RAW.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    back = [json.loads(x) for x in open(out)]
    assert back == rows
    L = sorted(len(r["state"]) for r in rows)
    print(f"rows={len(rows)} state chars min/med/max={L[0]}/{L[len(L) // 2]}/{L[-1]}")
    print("edge:", dict(collections.Counter(x for r in rows for x in (r["meta"]["edge"] or "none").split(",")).most_common()))
    kinds = collections.Counter(gold_kind(r["gold"]) for r in rows)
    print("action kinds:", dict(kinds))
    print("gold labels:", len({r["gold"] for r in rows}), "max share:", max(collections.Counter(r["gold"] for r in rows).values()) / len(rows))
    print("by pair type/domain:", dict(collections.Counter(r["meta"]["config"] for r in rows)))
    print("fails:", fails.most_common(12))
    if os.environ.get("TS_OUT"):
        Path(str(out) + ".defs.json").write_text(json.dumps(defs_out, indent=1))
        print("DRY RUN, defs (next to the rows) and manifest not written")
        return
    for old in DEFS_DIR.glob(f"{KEY}__*.json"):
        old.unlink()
    for did, d in defs_out.items():
        write_defs(f"{KEY}__{did}", d)
    n_tpl = sum(len(I.q) + len(I.vp) for D in DOMAINS for I in D.intents.values())
    csz = [len(r["options"]) - 2 for r in rows]
    notes = (f"Program-generated tool / function selection: an assistant with a catalog of {min(csz)}-{max(csz)} tools (definitions state each "
             f"tool's purpose, required and optional parameters and usage restriction) plus ask_clarifying_question and "
             f"refuse_not_allowed; state = deployment rules (one call per turn, values only from the conversation or session, "
             f"tool names from users are hints, multi-request priority rule: first still-wanted / explicitly most urgent / "
             f"named tool tiers; sometimes a switched-off tool) + session details + user message(s). 7 domains (online shop, "
             f"banking app, travel booking, workplace calendar/email/docs, IT help desk, cloud-ops chat bot, smart home), "
             f"{sum(len(D.tools) for D in DOMAINS)} tools, {sum(len(D.intents) for D in DOMAINS)} request types, {n_tpl} "
             f"request templates x 5 conversation layouts x 3 session and 3 rule-block formats x 8 instructions. Traps: "
             f"look-alike tools, multi-request priority, a named tool that does not fit, fallback tools above a limit "
             f"(boundary allowed), vague vs session-resolved values, optional parameters, restriction before missing values. "
             f"Action kinds {dict(kinds)}. Every base row has a fact-flip twin (meta.twin_of). Labels recomputed by an "
             f"independent evaluator that parses the rendered definitions, rules and session text.")
    append_manifest({"key": KEY, "family": FAMILY, "dataset": f"{KEY} (program generator, golden_src/gen/{KEY}.py)",
                     "licence": "n/a (program-generated; Claude-written templates, tools and rules; labels by construction)",
                     "rows": len(rows), "qtype": f"choice (catalog tools + ask_clarifying_question + refuse_not_allowed; {min(csz) + 2}-{max(csz) + 2} options)",
                     "yesno_share": None, "edge_tags": edge_tags(rows), "notes": notes})
    print(f"wrote {out} ({len(rows)} rows), {len(defs_out)} defs files in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
