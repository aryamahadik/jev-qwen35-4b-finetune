"""tg_output: the output-check items of yn2b family F2 gen3_tool_guard (SPEC 5 F2 "Output check yes/no").

The state holds one tool result and the assistant's output (a one-line JSON object, the only assistant turn of the
conversation) plus four numbered output requirements:
  R-keys      a JSON object with exactly three keys and their JSON types
  R-words     the summary string has exactly N words (a word = a maximal run of non-space characters)
  R-decimals  the number is written with exactly D decimal places (digits after the point; none written = 0)
  R-content   always one content rule: the total equals the sum of the tool result's line amounts / the value is the
              tool result's actual value, not its adjusted one (feels-like vs actual) / a value is copied exactly
Exactly 0 or 1 fact of the output is perturbed. decide_output() evaluates the four requirements on the output TEXT
(exact arithmetic with Fraction, decimals counted as written); no model, no judgment. The wording says "output",
never "reply" (SPEC 4.7 judge words). CPU only, stdlib only, deterministic.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import mv_core as mv  # noqa: E402
import tg_packs as tp  # noqa: E402
import tg_core as tc  # noqa: E402
from tg_core import UTC  # noqa: E402

SCENARIOS = ("sum", "actual", "value")
LINES = {
    "banking": ("card fee", "wire fee", "statement copy", "overdraft charge", "fee rebate"),
    "workspace": ("design seats", "video seats", "storage add-on", "admin seats", "loyalty credit"),
    "cloud": ("compute", "block storage", "network egress", "support plan", "committed-use credit"),
    "hr": ("hotel night", "train fare", "team dinner", "taxi", "advance returned"),
    "crm": ("onboarding", "annual plan", "extra users", "training day", "renewal credit"),
    "dbadmin": ("hot tier", "cold tier", "snapshots", "restore job", "volume discount"),
    "ecommerce": ("desk lamp", "linen cushion", "delivery", "gift wrap", "promo code"),
    "travel": ("flight", "hotel", "rail pass", "seat upgrade", "voucher"),
    "it_access": ("laptops", "docking stations", "monitors", "cables", "trade-in credit"),
    "support": ("outage credit", "delivery refund", "late fee waiver", "service call", "goodwill adjustment"),
    "smart_home": ("air filters", "light bulbs", "batteries", "smoke detector", "member discount"),
    "clinic": ("late cancellation fee", "form fee", "copy of records", "reminder texts", "hardship waiver"),
}
ACTUAL = {  # pack -> (actual field, adjusted field, output key, decimals, unit, lo, hi)
    "banking": ("available_balance", "current_balance", "available", 2, "EUR", 200, 9000),
    "workspace": ("seats_used", "seats_paid", "seats", 0, "seats", 20, 400),
    "cloud": ("measured_ms", "target_ms", "latency_ms", 1, "ms", 40, 900),
    "hr": ("net_pay", "gross_pay", "net", 2, "GBP", 1500, 6000),
    "crm": ("signed_value", "forecast_value", "deal", 2, "EUR", 2000, 60000),
    "dbadmin": ("row_count", "estimated_rows", "rows", 0, "rows", 1000, 900000),
    "ecommerce": ("charged_total", "list_total", "charged", 2, "GBP", 10, 900),
    "travel": ("temperature_c", "feels_like_c", "temperature_c", 1, "C", -5, 35),
    "it_access": ("devices_active", "devices_assigned", "devices", 0, "devices", 10, 900),
    "support": ("hours_open", "business_hours_open", "hours", 1, "hours", 1, 300),
    "smart_home": ("temperature_c", "feels_like_c", "temperature_c", 1, "C", 12, 28),
    "clinic": ("wait_minutes", "estimated_wait_minutes", "wait_minutes", 0, "minutes", 3, 90),
}
SUMMARIES = {  # grammatical summary sentences; the word count of the chosen one is the requirement's N
    "sum": ("Total of every bill line", "Total of every line on the bill", "Here is the total of every bill line",
            "Here is the total of every line on this bill", "The total below covers every line of the bill, credits "
            "included", "The total below adds up every line of this bill, including any credit lines",
            "Bill total for the 3-day period, every line counted", "Total sent by e-mail at 18:00 for every bill line"),
    "actual": ("Latest measured value", "Here is the latest measured value", "The figure below is the latest "
               "measured value", "The figure below is the measured value, not the adjusted one",
               "Measured value from the follow-up reading at 18:00", "This is the well-known measured value from the "
               "latest reading, as requested"),
    "value": ("Reference and amount on record", "Here are the reference and amount", "The reference and amount "
              "below come from the record", "Reference and amount copied from the record for the 3-day review",
              "The reference below is copied from the record as it stands at 18:00", "Here is the record's "
              "reference, copied exactly, with its amount"),
}
FILLER_WORDS = ("today", "again", "please", "thanks", "below", "now")
REPORT_TOOLS_HOLD = {
    "sum": tp.Tool("fetch_invoice_breakdown", "read", "lists each charge on an invoice.",
                   [tp.A("invoice_code", "id", prefix="BIL", n=5, label="invoice")], "itemise a charge",
                   ("What do these charges add up to?", "Sum up this invoice for me.", "Tally the charges, please.")),
    "actual": tp.Tool("read_metric", "read", "reports a metric as measured and as adjusted.",
                      [tp.A("metric_code", "id", prefix="MT", n=5, label="metric")], "see a live figure",
                      ("Where does the figure stand?", "Report the latest measurement.", "What's the value right now?")),
    "value": tp.Tool("fetch_entry", "read", "shows one entry with its reference, state and amount.",
                     [tp.A("entry_code", "id", prefix="ENT", n=5, label="entry")], "read an entry",
                     ("Pull that entry up for me.", "Show me the entry details.", "Get the entry's reference.")),
}
SUMMARIES_HOLD = {
    "sum": ("Charges tallied", "All charges tallied below", "Every charge on the invoice tallied below",
            "The figure below tallies every charge on this invoice, credits too",
            "Tallied at 18:00 across the 3-day invoice period"),
    "actual": ("Measured figure", "The measured figure is below", "Below is the figure as measured, not adjusted",
               "Figure from the follow-up measurement at 18:00, unadjusted"),
    "value": ("Entry reference and amount", "Entry reference copied exactly with its amount",
              "The reference below is copied exactly from the entry at 18:00"),
}
REPORT_TOOLS = {  # the read tool whose result the output summarises (added to the catalog of output items)
    "sum": tp.Tool("get_bill_lines", "read", "returns the lines of one bill or invoice.",
                   [tp.A("bill_ref", "id", prefix="INV", n=5, label="bill")], "see what a bill is made of",
                   ("Please total this bill for me.", "What does this bill come to?", "Add up the bill, please.")),
    "actual": tp.Tool("get_reading", "read", "returns the latest measured and adjusted values of one metric.",
                      [tp.A("reading_ref", "id", prefix="RD", n=5, label="reading")], "check a current figure",
                      ("What is the current figure?", "Can you tell me the latest value?",
                       "Give me the number as it stands now.")),
    "value": tp.Tool("get_record", "read", "returns one record with its reference, status and amount.",
                     [tp.A("record_ref", "id", prefix="REC", n=5, label="record")], "look up a record",
                     ("Can you pull the reference and amount?", "What is on this record?",
                      "Please fetch the record details.")),
}
PERTURB = ("keys_missing", "keys_extra", "keys_renamed", "type_string", "words_off", "decimals_off", "content_off")
REQ_T = {  # (training text, held-out text): dev_holdout / devx use held-out wording (SPEC 6, 7.6)
    "keys": ("The output is one JSON object with exactly the keys {k1}, {k2} and {k3}: {k1} is a string, {k2} is a "
             "number and {k3} is a string.",
             "Shape: a single JSON object whose only keys are {k1} (string), {k2} (number) and {k3} (string)."),
    "words": ("The {k1} string has exactly {n} words.",
              "Length: {k1} contains {n} words, no more and no fewer."),
    "decimals": ("{k2} is a number written with exactly {d} decimal places.",
                 "Precision: {k2} shows {d} digits after its decimal point."),
    "sum": ("{k2} equals the sum of the amount values of all lines in the tool result.",
            "Arithmetic: {k2} is the total of every line amount the tool returned."),
    "actual": ("{k2} equals the tool result's {actual} value, not its {adjusted} value.",
               "Source: {k2} reports {actual} from the tool response and never {adjusted}."),
    "value": ("{k3} equals the reference value in the tool result, character for character.",
              "Fidelity: {k3} reproduces the tool response's reference exactly."),
}
ANNEX_OUT = ({"label": "output format", "value": "one JSON object on a single line"},
             {"label": "response layout", "value": "exactly one single-line JSON object"})


@dataclass
class OItem:
    pack: str
    org: str
    tz: str
    now: datetime
    user_name: str
    user_id: str
    role: str
    rtype: str
    sid: str
    tool: str
    call_id: str
    scenario: str
    keys: tuple
    n_words: int
    decimals: int
    result: dict                # the tool result object (numbers as exact decimal strings in 'lit')
    result_text: str
    output_text: str
    reqs: list                  # [(no, date, text, kind)]
    request: str
    perturb: str | None = None
    edge: set = field(default_factory=set)
    notes: dict = field(default_factory=dict)

    @property
    def P(self):
        return tp.PACKS[self.pack]

    @property
    def T(self):
        return (REPORT_TOOLS_HOLD if self.notes.get("hold") else REPORT_TOOLS)[self.scenario]


def dec(x: Fraction, d: int) -> str:
    """Exact decimal text with d places (x must be exact at d places)."""
    s = mv.fmt_amount(x, d, commas=False) if d else str(int(x))
    return s


TRICKY_RX = re.compile(r"\d-day|e-mail|18:00|follow-up|well-known")


def summary_text(rng, scen: str, hold: bool = False) -> str:
    return rng.choice((SUMMARIES_HOLD if hold else SUMMARIES)[scen]) + "."


def out_json(pairs: list) -> str:
    """A one-line JSON object text from (key, literal JSON text) pairs (numbers keep their written decimals)."""
    return "{" + ", ".join(f"{json.dumps(k)}: {v}" for k, v in pairs) + "}"


RENAME = {"summary": "summary_text", "currency": "currency_code", "unit": "units", "reference": "ref"}


def sample_output(pack: str, split: str, perturb: str | None, seed: int, pool) -> OItem:
    """One output-check item. Everything but the perturbation comes from Random(seed), so calling it again with the
    same seed and another perturbation gives the contrast twin (only the output line differs)."""
    import random
    rng = random.Random(seed)
    prng = random.Random(mv.derive_seed(seed, "perturb", perturb))
    P = tp.PACKS[pack]
    org = pool.org(rng)
    tz = rng.choice(("Europe/Berlin", "America/New_York", "Asia/Singapore", "Europe/London", "Australia/Sydney"))
    d0 = date(2026, 1, 5) + timedelta(days=rng.randrange(0, 340))
    now = datetime(d0.year, d0.month, d0.day, rng.randrange(7, 21), rng.choice([0, 10, 20, 30, 40, 50]), tzinfo=UTC)
    scen = rng.choice(SCENARIOS)
    hold = split in ("dev_holdout", "devx")
    tool = (REPORT_TOOLS_HOLD if hold else REPORT_TOOLS)[scen]
    edge = {"numeric"}
    if scen == "sum":
        k1, k2, k3 = "summary", "total", "currency"
        d = 2
        names = rng.sample(LINES[pack][:4], rng.choice([2, 3, 3, 4]))
        lines = [(nm, Fraction(rng.randrange(150, 90000), 100)) for nm in names]
        if rng.random() < 0.4:
            lines.append((LINES[pack][4], -Fraction(rng.randrange(100, min(2000, int(sum(x for _, x in lines) * 50))),
                                                    100)))
            edge.add("negation")
        total = sum(x for _, x in lines)
        if total <= 0:
            raise mv.Reject("out_total")
        cur = P.home
        call_ref = f"{tool.args[0].prefix}-{rng.randrange(10000, 99999)}"
        res_pairs = [("ref", json.dumps(call_ref)),
                     ("lines", "[" + ", ".join(out_json([("name", json.dumps(nm)), ("amount", dec(x, 2))])
                                             for nm, x in lines) + "]"),
                     ("subtotal_before_credits", dec(sum(x for _, x in lines if x > 0), 2)), ("currency", json.dumps(cur))]
        good = {"k2": dec(total, 2), "k3": json.dumps(cur)}
        result = {"lines": lines, "total": total}
    elif scen == "actual":
        act, adj, k2, d, unit, lo, hi = ACTUAL[pack]
        k1, k3 = "summary", "unit"
        q = Fraction(10) ** d
        a = Fraction(rng.randrange(int(lo * q), int(hi * q)), q)
        b = a + Fraction(rng.choice([-1, 1]) * rng.randrange(1, max(2, int((hi - lo) * q) // 20)), q)
        if b == a:
            b = a + Fraction(1, q)
        call_ref = f"{tool.args[0].prefix}-{rng.randrange(10000, 99999)}"
        res_pairs = [("reading", json.dumps(call_ref)), (act, dec(a, d)), (adj, dec(b, d)),
                     ("unit", json.dumps(unit))]
        good = {"k2": dec(a, d), "k3": json.dumps(unit)}
        result = {"actual": a, "adjusted": b, "act": act, "adj": adj}
        edge.add("conflicting_evidence")
    else:
        k1, k2, k3 = "summary", "amount", "reference"
        d = 2
        ref = f"{rng.choice(['W', 'INV', 'TCK', 'BK'])}-{rng.randrange(1000000, 9999999)}"
        call_ref = f"{tool.args[0].prefix}-{rng.randrange(10000, 99999)}"
        amt = Fraction(rng.randrange(100, 500000), 100)
        res_pairs = [("record", json.dumps(call_ref)), ("reference", json.dumps(ref)), ("status", json.dumps(rng.choice(["open", "settled", "pending"]))),
                     ("amount", dec(amt, 2)), ("related", json.dumps(mv.decoy_id(ref, rng)))]
        good = {"k2": dec(amt, 2), "k3": json.dumps(ref)}
        result = {"reference": ref, "amount": amt}
        edge.add("hc:decoy_id")
    summ = summary_text(rng, scen, hold)
    n_words = len(summ.split())
    if TRICKY_RX.search(summ):
        edge.add("quantifier")
    reqs_kinds = ["keys", "words", "decimals", scen]
    slots = {"k1": k1, "k2": k2, "k3": k3, "n": str(n_words), "d": str(d),
             "actual": result.get("act", ""), "adjusted": result.get("adj", "")}
    dd0 = now.date() - timedelta(days=rng.randrange(60, 300))
    reqs = []
    for i, k in enumerate(reqs_kinds, 1):
        dd0 += timedelta(days=rng.randrange(1, 20))
        reqs.append((i, dd0.isoformat(), re.sub(r"\{(\w+)\}", lambda m: slots[m.group(1)], REQ_T[k][int(hold)]), k))
    user = pool.person(rng)
    uid = "u-" + str(rng.randrange(10000, 99999))
    role = rng.choice(P.roles)
    sid = f"S-{rng.randrange(100000, 999999)}"
    cid = f"c-{rng.randrange(100000, 999999)}"
    request = rng.choice(tool.asks)
    decoy_ref = mv.decoy_id(result["reference"], rng) if scen == "value" else None
    pairs = [(k1, json.dumps(summ)), (k2, good["k2"]), (k3, good["k3"])]
    # ---- exactly 0 or 1 perturbed fact (its random choices come from prng only)
    rng = prng
    if perturb == "keys_missing":
        drop = rng.choice([k1, k3])
        pairs = [p for p in pairs if p[0] != drop]
    elif perturb == "keys_extra":
        pairs.append((rng.choice(["note", "source", "status_text"]), json.dumps(rng.choice(["ok", "done", "auto"]))))
    elif perturb == "keys_renamed":
        i = rng.choice([0, 2])
        pairs[i] = (RENAME[pairs[i][0]], pairs[i][1])
    elif perturb == "type_string":  # the number written as a string with its unit (a JSON type error)
        unit = json.loads(good["k3"]) if scen != "value" else P.home
        pairs[1] = (k2, json.dumps(f"{pairs[1][1]} {unit}"))
    elif perturb == "words_off":
        w = summ.split()
        summ2 = " ".join(w[:-2] + [w[-1]]) if rng.random() < 0.5 and len(w) > 3 else \
            " ".join(w[:-1] + [rng.choice(FILLER_WORDS), w[-1]])
        pairs[0] = (k1, json.dumps(summ2))
        edge.add("hc:boundary_off1")
    elif perturb == "decimals_off":
        v = pairs[1][1]
        x = Fraction(v)
        dd = rng.choice([x_ for x_ in (d - 1, d + 1) if x_ >= 0])
        if dd == d - 1 and x == round(x, dd):
            pairs[1] = (k2, dec(x, dd))
        else:
            pairs[1] = (k2, v + "0" if d else v + ".0")
    elif perturb == "content_off":
        if scen == "sum":
            ls = result["lines"]
            neg = [x for _, x in ls if x < 0]
            wrong = result["total"] - (neg[0] if neg else ls[-1][1])  # the credit line (or one line) left out
            pairs[1] = (k2, dec(wrong, 2))
        elif scen == "actual":
            pairs[1] = (k2, dec(result["adjusted"], d))
        else:
            pairs[2] = (k3, json.dumps(decoy_ref))
    elif perturb is not None:
        raise ValueError(perturb)
    output = out_json(pairs)
    return OItem(pack, org, tz, now, user, uid, role, tool.rtype, sid, tool.name, cid, scen, (k1, k2, k3), n_words, d,
                 result, out_json(res_pairs), output, reqs, request, perturb, edge, {"call_ref": call_ref, "hold": hold})


# ------------------------------------------------------------------------------------------------ evaluation
def _num_literal(text: str, key: str):
    m = re.search(rf'"{re.escape(key)}": (-?\d+(?:\.\d+)?)(?=[,}}])', text)
    return m.group(1) if m else None


def check_reqs(it: OItem) -> dict:
    """{requirement no: True/False} on the output text."""
    k1, k2, k3 = it.keys
    out = {}
    try:
        o = json.loads(it.output_text)
    except ValueError:
        return {no: False for no, *_ in it.reqs}
    res = json.loads(it.result_text)
    for no, _, _, kind in it.reqs:
        if kind == "keys":
            ok = isinstance(o, dict) and len(o) == 3 and all(k in o for k in (k1, k2, k3))
            ok = ok and isinstance(o.get(k1), str) and isinstance(o.get(k3), str) and \
                isinstance(o.get(k2), (int, float)) and not isinstance(o.get(k2), bool)
        elif kind == "words":
            ok = isinstance(o.get(k1), str) and len(o[k1].split()) == it.n_words
        elif kind == "decimals":
            lit = _num_literal(it.output_text, k2)
            ok = lit is not None and (len(lit.split(".")[1]) if "." in lit else 0) == it.decimals
        elif kind == "sum":
            lit = _num_literal(it.output_text, k2)
            amounts = [Fraction(m) for m in re.findall(r'"amount": (-?\d+(?:\.\d+)?)', it.result_text)]
            ok = lit is not None and Fraction(lit) == sum(amounts)
        elif kind == "actual":
            lit = _num_literal(it.output_text, k2)
            act = _num_literal(it.result_text, it.result["act"])
            ok = lit is not None and act is not None and Fraction(lit) == Fraction(act)
        elif kind == "value":
            ok = isinstance(o.get(k3), str) and o.get(k3) == res.get("reference")
        else:
            raise ValueError(kind)
        out[no] = bool(ok)
    return out


def decide_output(it: OItem):
    """(meets every requirement, trace)."""
    r = check_reqs(it)
    failed = sorted(n for n, ok in r.items() if not ok)
    return not failed, {"failed": failed, "perturb": it.perturb}


# ------------------------------------------------------------------------------------------------ document
def canon_output(it: OItem) -> dict:
    tool = it.T
    ax = ANNEX_OUT[int(bool(it.notes.get("hold")))]
    args = {tool.args[0].name: it.notes["call_ref"]}  # the id the tool was called with is the one its result shows
    at = it.now - timedelta(minutes=3)
    return {
        "kind": "output",
        "about": it.P.about.format(org=it.org),
        "tools": [tc.tool_line(tool)],
        "rtypes": [[tool.rtype, tool.name]],
        "org": it.org,
        "rules": [[no, dt, text] for no, dt, text, _ in it.reqs],
        "annex": [[ax["label"], ax["value"]], ["time zone", it.tz]],
        "session": [["user", f"{it.user_name} ({it.user_id})"], ["role", it.role], ["request type", it.rtype],
                    ["session", it.sid], ["time", tc.ts(it.now)]],
        "confs": [],
        "resources": [],
        "log": [{"at": tc.ts(at), "call": it.call_id, "tool": tool.name, "user": it.user_id, "session": it.sid,
                 "args": args, "status": "ok"}],
        "conv": [["user", it.user_name, it.request], ["assistant", "assistant", it.output_text]],
        "results": [[tool.name, it.call_id, it.result_text]],
        "call": {},
    }
