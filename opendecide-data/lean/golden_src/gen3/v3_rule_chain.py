"""v3_rule_chain: the independent decide2 for F1 `gen3_rule_chain` (yn2b SPEC 5 F1, 8.1).

Written by builder E from yn2b/F1_RULE_CHAIN_FORMAT.md, the SPEC and the RENDERED rows only. It never imports or reads
the generator or its decide (gen3_rule_chain.py, rc_core.py, rc_render.py, rc_numeric.py, rc_repair.py, rc_gen2.py).
The only generator-side import is `rc_skins`, the vocabulary file the format doc names (nouns, flag phrases, outcome
texts, procedure sentences; it holds no logic). decide2 never reads a row's gold, trace, edge, tier or shortcut fields.
It reads state, instructions and options, plus the printed card (meta.defs -> yn2b_defs) for F1b, whose rules
(conversion factor, "about" tolerance) are printed only there.

What it does, per raw row:
  F1a (a rule document plus a case file)
    1. split_state(state)          -> document lines + the case-file part; untrusted notes (attack plants) are cut off
                                      by channel: the json `correspondence` list, any email after the office reply, a
                                      markdown `## Correspondence` section, or a trailing "Note attached to the file by".
    2. parse_document(lines)       -> Doc: every clause line is matched by a strict pattern (train and held-out
                                      wordings); an unknown line raises ParseError (nothing is silently skipped).
    3. parse_case(part)            -> Case, from any of the 10 case-file formats (json, kv, markdown, prose, email,
                                      log x3, table x2).
    4. evaluate(doc, case, deleted) -> Result: the outcome code (INELIG/LATE/DOCS/EXCL/PARTIAL/FULL) and the amount
                                      granted, applying the document's own General clauses (counting rule and
                                      holidays, exceptions and exceptions to them, amendments in force on the received
                                      date, missing facts, order of grounds, limits and the precedence rule).
                                      `deleted` removes clauses (the "which clause is decisive" question).
  F1b (numeric claim checks)
    5. parse_nb(state) + card rules -> the claim's truth with exact rational arithmetic.
  6. decide2_row(row)              -> 'yes' / 'no' / the gold option string (mv_core.UNDEFINED when the row cannot be
                                      read unambiguously; verify_labels counts that as a failure).

Readings. Where the text leaves room, decide2 uses DEFAULT_READINGS, fixed from the documents' own wording before any
comparison with gold. `sensitivity` re-runs every row under each alternative and lists the rows whose answer depends
on it: that is the ambiguity report.

CLI (from lean/):
  ../.venv/bin/python golden_src/gen3/v3_rule_chain.py           agreement, structure, sensitivity (prints)
  ../.venv/bin/python golden_src/gen3/v3_rule_chain.py --quick   agreement only
  ../.venv/bin/python golden_src/gen3/v3_rule_chain.py --write   also writes yn2b/v3_rule_chain_agreement.json and
                                                                  appends its sha256 to MANIFEST_yn2b.jsonl
Tests: yn2b/tests/test_v3_rule_chain_{parse,eval,written}.py.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import re
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
DEFS = LEAN / "data" / "v14_parts" / "yn2b_defs"
KEY = "gen3_rule_chain"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import rc_skins  # noqa: E402  vocabulary only (nouns, phrases, outcome texts); no decision logic


class ParseError(Exception):
    """The rendered row could not be read unambiguously. decide2 never guesses."""


DEFAULT_READINGS = {
    # "which clause is decisive": deleting the clause changes the outcome (the outcome code / outcome text).
    # "code+amount" also counts a change of the amount granted under the same outcome text.
    "decisive_outcome": "code",
    # F1b as-of claims: a revision counts whatever its date (the card: "only the most recent revision of it counts").
    # True: a revision dated after the as-of date is not used for the figure as of that date.
    "nb_revision_by_date": False,
    # F1b percentage claims: "fell by" a negative amount when the figure rose (the format doc: "with the sign of
    # rose / fell"). "strict": a rise is never a fall of at most P%, and vice versa.
    "nb_pct_direction": "signed",
    # Business-day limits: the documents define "the date N business days before/after X" by counting business days
    # back/forward from X, and the limit compares the received date with that date. "count": compare the number of
    # business days between the received date and X instead (differs only when the received date is not a business
    # day and sits next to the deadline).
    "business_limit": "date",
}

ALT_READINGS = {
    "decisive_outcome=code+amount": {"decisive_outcome": "code+amount"},
    "nb_revision_by_date=True": {"nb_revision_by_date": True},
    "nb_pct_direction=strict": {"nb_pct_direction": "strict"},
    "business_limit=count": {"business_limit": "count"},
}

# Ablation probes (not readings of the text): each switches one mechanism off. A probe that changes many rows while
# the gold follows it on none shows that the data exercises that mechanism and that decide2 agrees with the gold on it.
PROBES = {
    "probe:ignore_holidays": {"probe_ignore_holidays": True},
    "probe:calendar_for_business": {"probe_calendar_days": True},
    "probe:all_bounds_inclusive": {"probe_inclusive": True},
    "probe:no_exception_to_exception": {"probe_no_exc_to_exc": True},
    "probe:no_exceptions": {"probe_no_exceptions": True},
    "probe:no_amendments": {"probe_no_amendments": True},
    "probe:withdrawn_amendments_apply": {"probe_withdrawn_apply": True},
    "probe:no_period_exception": {"probe_no_period_exc": True},
    "probe:lower_limit_always": {"probe_prec_lower": True},
    "probe:category_lists_ignored": {"probe_ignore_cats": True},
    "probe:nb_no_revisions": {"probe_nb_no_revisions": True},
    "probe:nb_asof_ignored": {"probe_nb_asof_latest": True},
    "probe:nb_no_conversion": {"probe_nb_no_conversion": True},
}

CODES = ("INELIG", "LATE", "DOCS", "EXCL", "PARTIAL", "FULL")
REFUSALS = ("INELIG", "LATE", "DOCS", "EXCL")

# ------------------------------------------------------------------------------------------------ small helpers
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")
_M = "|".join(MONTHS)
DATE_RE = rf"(?:\d{{4}}-\d\d-\d\d|\d{{1,2}} (?:{_M}) \d{{4}}|(?:{_M}) \d{{1,2}}, \d{{4}})"
NUM_RE = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"
CMP_RE = r"(?:at least|more than|at most|less than)"
REF_RE = r"(?:[Ss]ection \d+\.\d+|[Cc]lause \d+\.\d+|Rule \d+|[Aa]nswer \d+|C\d+|Table \d+)"


def to_date(s: str) -> dt.date:
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d\d)-(\d\d)", s)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r"(\d{1,2}) ([A-Z][a-z]+) (\d{4})", s)
    if m and m[2] in MONTHS:
        return dt.date(int(m[3]), MONTHS.index(m[2]) + 1, int(m[1]))
    m = re.fullmatch(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})", s)
    if m and m[1] in MONTHS:
        return dt.date(int(m[3]), MONTHS.index(m[1]) + 1, int(m[2]))
    raise ParseError(f"not a date: {s!r}")


def to_num(s: str) -> Fraction:
    s = s.strip()
    if not re.fullmatch(NUM_RE, s):
        raise ParseError(f"not a number: {s!r}")
    return Fraction(s.replace(",", ""))


def _unit_plurals() -> dict:
    out = {"day": "days", "days": "days"}
    for s in rc_skins.SKINS.values():
        for u in (s["unit"], s["elig"]["unit"]):
            if isinstance(u, tuple):
                out[u[0]] = u[1]
                out[u[1]] = u[1]
    return out


UNIT_PL = _unit_plurals()


@dataclass(frozen=True)
class Qty:
    v: Fraction
    u: str  # "$" or a plural unit word

    def __str__(self):
        return f"${self.v}" if self.u == "$" else f"{self.v} {self.u}"


def to_qty(s: str) -> Qty:
    s = s.strip()
    m = re.fullmatch(r"\$(" + NUM_RE + ")", s)
    if m:
        return Qty(to_num(m[1]), "$")
    m = re.fullmatch(r"(" + NUM_RE + r") (.+)", s)
    if m and m[2] in UNIT_PL:
        return Qty(to_num(m[1]), UNIT_PL[m[2]])
    raise ParseError(f"not a quantity: {s!r}")


def to_period(s: str) -> tuple:
    m = re.fullmatch(r"(\d+) (business )?days?", s.strip())
    if not m:
        raise ParseError(f"not a period: {s!r}")
    return int(m[1]), bool(m[2])


def cmp_ok(x: Fraction, op: str, y: Fraction) -> bool:
    if op == "at least":
        return x >= y
    if op == "more than":
        return x > y
    if op == "at most":
        return x <= y
    if op == "less than":
        return x < y
    raise ParseError(f"unknown comparison {op!r}")


def article(noun: str) -> str:
    return "an" if noun[:1].lower() in "aeiou" else "a"


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def split_sentences(text: str) -> list[str]:
    return [x for x in re.split(r"(?<=\.)\s+(?=[A-Z])", text.strip()) if x]


# ------------------------------------------------------------------------------------------------ vocabulary
class Vocab:
    """The vocabulary of one document family (rc_skins), plus the exact sentences it produces."""

    def __init__(self, key: str):
        s = rc_skins.SKINS[key]
        ho = rc_skins.HO_TEXT.get(key, {})
        self.key = key
        self.s = s
        self.doc = s["doc"]
        self.req, self.req_pl = s["req"], s["req_pl"]
        self.a_req = f"{article(self.req)} {self.req}"
        self.who, self.who_pl = s["who"], s["who_pl"]
        self.benefit, self.benefit_cap = s["benefit"], s["benefit_cap"]
        self.grant_vp, self.deny_vp = s["grant_vp"], s["deny_vp"]
        self.amount_np, self.amount_label = s["amount_np"], s["amount_label"]
        self.elig = s["elig"]
        self.time = s["time"]
        self.docs = s["docs"]
        self.docs2 = s["docs2"]
        self.types = tuple(s["types"])
        self.cat_by_sing = {sing: k for k, sing, pl in s["cats"]}
        self.cat_by_pl = {pl: k for k, sing, pl in s["cats"]}
        self.cat_pl = {k: pl for k, sing, pl in s["cats"]}
        self.flags = s["flags"]
        self.flag_by_pos = {f["pos"]: k for k, f in s["flags"].items()}
        self.outcomes = dict(s["outcomes"])
        self.code_by_text = {v: k for k, v in self.outcomes.items()}
        self.office = s["office"]
        self.proc = set(s["proc"]) | set(ho.get("proc", ()))
        # case-file labels (lower case) -> field name
        lab = {"reference": "ref", self.who.lower(): "who", "category": "cat", "request type": "rtype",
               self.elig["label"].lower(): "elig", self.time["label"].lower(): "event", "received": "received",
               self.docs["label"].lower(): "docs", self.amount_label.lower(): "amount",
               "decision recorded": "decision", "linked file": "linked"}
        for k, f in self.flags.items():
            lab[f["label"].lower()] = "flag:" + k
        self.labels = lab

    # -- lists
    def cats(self, text: str) -> frozenset:
        parts = re.split(r", | and ", text)
        out = set()
        for p in parts:
            if p not in self.cat_by_pl:
                raise ParseError(f"unknown category list {text!r}")
            out.add(self.cat_by_pl[p])
        return frozenset(out)

    def conds(self, text: str) -> tuple:
        atoms = []
        for a in text.split(" and "):
            if a in self.flag_by_pos:
                atoms.append(("flag", self.flag_by_pos[a]))
                continue
            m = re.fullmatch(re.escape(self.amount_np) + rf" is ({CMP_RE}) (.+)", a)
            if m:
                atoms.append(("amt", m[1], to_qty(m[2])))
                continue
            raise ParseError(f"unknown condition {a!r} in {text!r}")
        return tuple(atoms)


@lru_cache(maxsize=None)
def vocab(key: str) -> Vocab:
    return Vocab(key)


def detect_skin(lines: list[str]) -> Vocab:
    """The document family, from its entitlement clause (the only clause that names who may apply)."""
    hits = set()
    for key in rc_skins.SKINS:
        v = vocab(key)
        a = f" {v.a_req} under this {v.doc} for "
        b = f"Under this {v.doc}, {v.who_pl} can submit {v.a_req} for "
        for ln in lines:
            if a in ln or b in ln:
                hits.add(key)
    if len(hits) != 1:
        raise ParseError(f"document family not identified ({sorted(hits)})")
    return vocab(hits.pop())


# ------------------------------------------------------------------------------------------------ state split
CASE_HEADS = ("Case file", "Case summary", "Correspondence", "Case log")


@dataclass
class Split:
    fmt: str              # json | markdown | kv | table:csv | table:md | prose | email | log
    doc_lines: list
    case: object          # dict (json) or text


def split_state(state: str) -> Split:
    s = state
    if s.lstrip().startswith("{"):
        try:
            obj = json.loads(s)
        except json.JSONDecodeError as e:
            raise ParseError(f"bad json state: {e}")
        if set(obj) != {"document", "case", "correspondence"}:
            raise ParseError(f"unexpected json keys {sorted(obj)}")
        return Split("json", list(obj["document"]), obj["case"])  # correspondence = untrusted notes, ignored
    if s.startswith("## Document\n"):
        body = s[len("## Document\n"):]
        if body.count("\n## Case file\n") != 1:
            raise ParseError("markdown state without one '## Case file' section")
        doc, case = body.split("\n## Case file\n")
        case = re.split(r"\n## |\n\nNote attached to the file by ", "\n" + case)[0]  # cut '## Correspondence' / notes
        return Split("markdown", doc.split("\n"), case.strip("\n"))
    lines = s.split("\n")
    idx = [i for i, ln in enumerate(lines) if ln in CASE_HEADS and i > 0 and lines[i - 1] == ""]
    if not idx:
        raise ParseError("no case-file heading")
    i = idx[0]
    head = lines[i]
    rest = "\n".join(lines[i + 1:])
    rest = rest.split("\n\nNote attached to the file by ")[0]
    if head == "Case summary":
        fmt = "prose"
    elif head == "Correspondence":
        fmt = "email"
    elif head == "Case log":
        fmt = "log"
    elif rest.startswith("Field,Value\n"):
        fmt = "table:csv"
    elif rest.startswith("| Field | Value |\n"):
        fmt = "table:md"
    elif rest.startswith("case."):
        fmt = "kv"
    else:
        raise ParseError(f"unknown case-file format after {head!r}")
    return Split(fmt, lines[:i - 1], rest)


# ------------------------------------------------------------------------------------------------ case file
@dataclass
class Case:
    ref: str | None = None
    who: str | None = None
    cat: str | None = None           # category key
    rtype: str | None = None
    elig: Qty | None = None
    event: dt.date | None = None
    received: dt.date | None = None
    docs: bool = False
    flags: dict = field(default_factory=dict)  # key -> bool
    amount: Qty | None = None
    decision: str | None = None
    shown: set = field(default_factory=set)    # fields the case file shows


def _fields_from_pairs(pairs, v: Vocab) -> dict:
    out = {}
    for lab, val in pairs:
        f = v.labels.get(lab.strip().lower())
        if f is None:
            raise ParseError(f"unknown case-file label {lab!r}")
        if f in out:
            raise ParseError(f"case-file label {lab!r} given twice")
        out[f] = val.strip()
    return out


def _pairs_lines(text: str, rx: str) -> list:
    pairs = []
    for ln in text.split("\n"):
        if not ln.strip():
            continue
        m = re.fullmatch(rx, ln)
        if not m:
            raise ParseError(f"unreadable case-file line {ln!r}")
        pairs.append((m[1], m[2]))
    return pairs


def _email_pairs(text: str, v: Vocab) -> list:
    msgs = text.split("\n\n----------\n\n")
    if len(msgs) < 2:
        raise ParseError("email case file without the office reply")
    office = f"From: {cap(v.office)} <"
    if not msgs[1].startswith(office):
        raise ParseError("second email is not the office reply")
    pairs = []
    for msg in msgs[:2]:  # the applicant's email and the office reply; later emails are untrusted notes
        head, _, body = msg.partition("\n\n")
        if not head.startswith("From: "):
            raise ParseError("email without a From line")
        for ln in body.split("\n"):
            m = re.fullmatch(r"([^:]+): (.+)", ln)
            if m and m[1].lower() in v.labels:
                pairs.append((m[1], m[2]))
            elif ":" in ln and not ln.endswith(":"):
                raise ParseError(f"unknown email line {ln!r}")
    return pairs


def _log_pairs(text: str) -> list:
    pairs = []
    for ln in text.split("\n"):
        if not ln.strip() or re.fullmatch(r"== \w+ ==", ln):
            continue
        m = re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ (?:\[\w+\] )?([^:]+): (.+)", ln)
        if not m:
            raise ParseError(f"unreadable log line {ln!r}")
        pairs.append((m[1], m[2]))
    return pairs


def _prose_fields(text: str, v: Vocab) -> dict:
    out = {}
    req = re.escape(v.req)

    def put(k, val):
        if k in out:
            raise ParseError(f"prose gives {k} twice")
        out[k] = val

    rx_intro = [re.compile(rf"(?P<who>.+) \((?P<cat>[^()]+)\) made {article(v.req)} {req} for an? (?P<rtype>.+), "
                           rf"reference (?P<ref>[A-Z]\d+)\."),
                re.compile(rf"Reference (?P<ref>[A-Z]\d+): (?P<who>.+) \((?P<cat>[^()]+)\) submitted "
                           rf"{article(v.req)} {req} for an? (?P<rtype>.+)\.")]
    vals = {"elig": v.elig["noun"], "event": v.time["event"], "amount": v.amount_np}
    for sent in split_sentences(text):
        done = False
        for rx in rx_intro:
            m = rx.fullmatch(sent)
            if m:
                for k in ("who", "cat", "rtype", "ref"):
                    put(k, m[k])
                done = True
                break
        if done:
            continue
        for k, noun in vals.items():
            m = re.fullmatch(re.escape(cap(noun)) + r" is (.+)\.", sent) or \
                re.fullmatch(r"The file gives " + re.escape(noun) + r" as (.+)\.", sent)
            if m:
                put(k, m[1])
                done = True
                break
        if done:
            continue
        m = re.fullmatch(rf"The {req} (?:was received on|arrived on) ({DATE_RE})\.", sent)
        if m:
            put("received", m[1])
            continue
        dn = re.escape(v.docs["noun"])
        m = re.fullmatch(rf"The {req} (included|came with|did not include|came without) {dn}\.", sent)
        if m:
            put("docs", "included" if m[1] in ("included", "came with") else "not included")
            continue
        m = re.fullmatch(re.escape(cap(v.office)) + r' (?:recorded the decision as "(.+)"|entered the decision "(.+)" '
                         r'in the file)\.', sent)
        if m:
            put("decision", m[1] or m[2])
            continue
        if re.fullmatch(r"A separate file, [A-Z]\d+, from [^()]+ \([^()]+\), is decided on its own\.", sent) or \
                re.fullmatch(r"File [A-Z]\d+ \([^()]+\) is a separate matter\.", sent):
            put("linked", sent)  # a separate case: never used
            continue
        body = sent[len("It is recorded that "):] if sent.startswith("It is recorded that ") else sent
        hit = None
        for k, f in v.flags.items():
            for pol, ph in (("yes", f["pos"]), ("no", f["neg"])):
                if body in (ph + ".", cap(ph) + "."):
                    hit = (k, pol)
        if hit:
            put("flag:" + hit[0], hit[1])
            continue
        raise ParseError(f"unknown prose sentence {sent!r}")
    return out


def parse_case(sp: Split, v: Vocab) -> Case:
    if sp.fmt == "json":
        if not isinstance(sp.case, dict):
            raise ParseError("json case is not an object")
        f = _fields_from_pairs(sp.case.items(), v)
    elif sp.fmt == "kv":
        f = _fields_from_pairs(_pairs_lines(sp.case, r"case\.([^:]+): (.+)"), v)
    elif sp.fmt == "markdown":
        f = _fields_from_pairs(_pairs_lines(sp.case, r"- ([^:]+): (.+)"), v)
    elif sp.fmt == "table:csv":
        rows = list(csv.reader(io.StringIO(sp.case)))
        if not rows or rows[0] != ["Field", "Value"] or any(len(r) != 2 for r in rows[1:] if r):
            raise ParseError("bad csv case file")
        f = _fields_from_pairs([tuple(r) for r in rows[1:] if r], v)
    elif sp.fmt == "table:md":
        lines = [ln for ln in sp.case.split("\n") if ln.strip()]
        if lines[:2] != ["| Field | Value |", "|---|---|"]:
            raise ParseError("bad markdown table case file")
        f = _fields_from_pairs(_pairs_lines("\n".join(lines[2:]), r"\| (.+?) \| (.+) \|"), v)
    elif sp.fmt == "email":
        f = _fields_from_pairs(_email_pairs(sp.case, v), v)
    elif sp.fmt == "log":
        f = _fields_from_pairs(_log_pairs(sp.case), v)
    elif sp.fmt == "prose":
        f = _prose_fields(sp.case, v)
    else:
        raise ParseError(sp.fmt)
    c = Case(shown=set(f))
    c.ref, c.who, c.rtype = f.get("ref"), f.get("who"), f.get("rtype")
    if "cat" in f:
        if f["cat"] not in v.cat_by_sing:
            raise ParseError(f"unknown category {f['cat']!r}")
        c.cat = v.cat_by_sing[f["cat"]]
    if "elig" in f:
        c.elig = to_qty(f["elig"])
    if "event" in f:
        c.event = to_date(f["event"])
    if "received" in f:
        c.received = to_date(f["received"])
    if "docs" in f:
        if f["docs"] not in ("included", "not included"):
            raise ParseError(f"document field {f['docs']!r}")
        c.docs = f["docs"] == "included"
    for k in v.flags:
        val = f.get("flag:" + k)
        if val is not None and val not in ("yes", "no"):
            raise ParseError(f"flag value {val!r}")
        c.flags[k] = val == "yes"   # a flag the case file does not show is not established
    if "amount" in f:
        c.amount = to_qty(f["amount"])
    c.decision = f.get("decision")
    if c.rtype is not None and c.rtype not in v.types:
        raise ParseError(f"unknown request type {c.rtype!r}")
    return c


# ------------------------------------------------------------------------------------------------ document
@dataclass
class Clause:
    key: str
    pos: int
    kind: str
    text: str
    d: dict = field(default_factory=dict)


@dataclass
class Doc:
    v: Vocab
    style: str
    clauses: list
    by_key: dict
    counting: str | None = None          # calendar | business
    holidays: frozenset = frozenset()
    prec: list = field(default_factory=list)        # general precedence rules: category | later | lower
    named_prec: list = field(default_factory=list)  # (keyA, keyB, winner)
    slots: dict = field(default_factory=dict)       # (clause key, slot) -> original value
    chains: dict = field(default_factory=dict)      # (clause key, slot) -> [amendment clauses, by date]
    waivers: dict = field(default_factory=dict)     # target key -> [waiver exception clauses]
    notes: list = field(default_factory=list)

    def of(self, *kinds):
        return [c for c in self.clauses if c.kind in kinds]


HEADINGS = {"general", "exclusions", "exceptions", "amendments", "limits and amounts",
            "who may apply and what is required", "other provisions"}
LABEL_RES = (("code", re.compile(r"(\d+\.\d+) (.+)"), "S"),
             ("handbook", re.compile(r"Rule (\d+)\. (.+)"), "R"),
             ("faq", re.compile(r"A(\d+)\. (.+)"), "A"),
             ("table", re.compile(r"C(\d+)\. (.+)"), "C"))


def ref_key(ref: str) -> str:
    m = re.fullmatch(r"(?:[Ss]ection|[Cc]lause) (\d+\.\d+)", ref)
    if m:
        return "S" + m[1]
    for rx, p in ((r"Rule (\d+)", "R"), (r"[Aa]nswer (\d+)", "A"), (r"C(\d+)", "C"), (r"Table (\d+)", "T")):
        m = re.fullmatch(rx, ref)
        if m:
            return p + m[1]
    raise ParseError(f"not a clause reference {ref!r}")


def _general_rules(v: Vocab) -> dict:
    d, rp, ar = v.doc, v.req_pl, v.a_req
    return {
        "g_exc": {"An exception applies only to the clause it names, and only when every condition it states is met; "
                  "an exception does not apply where another clause says that it does not apply.",
                  "An exception covers only the clause it refers to, and only if all of its conditions are "
                  "satisfied; it has no effect where another clause switches it off."},
        "g_amend": {f"An amendment replaces the figure it names for {rp} received on or after the date it comes into "
                    f"force; {rp} received earlier keep the earlier figure, and a withdrawn amendment has no effect.",
                    f"An amendment changes the figure it refers to for {rp} received on or after its start date; {rp} "
                    f"received before that date use the previous figure, and a withdrawn amendment changes nothing."},
        "g_order": {f"If more than one ground for refusal applies to {ar}, the ground stated first in this {d} is the "
                    f"one recorded.",
                    f"Where {ar} meets more than one ground for refusal, the ground that appears first in this {d} is "
                    f"the one entered."},
        "g_missing": {"A fact that the case file does not show is treated as not established, and a document that the "
                      "case file does not show as included is treated as not included.",
                      "Anything the case file does not show counts as not established, and a document the case file "
                      "does not list as included counts as not included."},
        "prec:category": {f"Where the general limit and a category limit both apply to {ar}, the category limit "
                          f"prevails.",
                          f"If both the general limit and a category limit cover {ar}, the category limit takes "
                          f"priority."},
        "prec:later": {f"Where two limits both apply to {ar}, the one that appears later in this {d} prevails.",
                       f"If two limits cover {ar}, the one placed later in this {d} takes priority."},
        "prec:lower": {f"Where two limits both apply to {ar}, the lower of the two applies.",
                       f"If two limits cover {ar}, the smaller limit is used."},
        "g_count_cal": {f"Periods in this {d} are counted in calendar days: the date a stated number of days after or "
                        f"before a given date is found by counting that many calendar days forward or back from it.",
                        f"All periods in this {d} run in calendar days; to find the date that lies a given number of "
                        f"days before or after another date, count that number of calendar days back or forward from "
                        f"it."},
    }


@lru_cache(maxsize=None)
def _clause_res(key: str) -> dict:
    v = vocab(key)
    E = re.escape
    d, req = E(v.doc), E(v.req)
    elig_cmp = rf"(?P<cmp>{CMP_RE}) (?P<q>.+)"
    return {
        "entitle": [re.compile(rf"{E(cap(v.who_pl))} may make {E(v.a_req)} under this {d} for an? (?P<type>.+); the "
                               rf"{E(v.benefit)} is granted only as this {d} allows\."),
                    re.compile(rf"Under this {d}, {E(v.who_pl)} can submit {E(v.a_req)} for an? (?P<type>.+); the "
                               rf"{E(v.benefit)} is given only in the ways this {d} sets out\.")],
        "elig": [re.compile(rf"{E(v.grant_vp)} only (?:if|where) {E(v.elig['noun'])} is {elig_cmp}\.")],
        "elig_term": [re.compile(rf"{E(v.elig['def_req'])}(?:, and in no other case)?\.")],
        "def": [re.compile(r'"(?P<term>[^"]+)" means (?P<rest>.+)\.'),
                re.compile(rf'In this {d}, "(?P<term>[^"]+)" refers to (?P<rest>.+)\.')],
        "time": [re.compile(rf"The {req} (?:must|shall) be received (?P<t>.+)\."),
                 re.compile(rf"Each {req} (?:has to|shall) arrive (?P<t>.+)\.")],
        "docs": [re.compile(rf"The {req} (?:must|shall) include (?P<docs>.+)\."),
                 re.compile(rf"Each {req} (?:has to|shall) come with (?P<docs>.+)\.")],
        "docs_other": [re.compile(rf"For an? (?P<type>.+), the {req} (?:must|shall) also include (?P<docs>.+)\."),
                       re.compile(rf"An? {req} for an? (?P<type>.+) also (?:has to|shall) come with (?P<docs>.+)\.")],
        "glimit": [re.compile(rf"{E(v.benefit_cap)} may not be more than (?P<q>.+) for one {req}\."),
                   re.compile(rf"{E(v.benefit_cap)} is capped at (?P<q>.+) for each {req}\.")],
        "catlim": [re.compile(r"The category limits are: (?P<list>.+)\."),
                   re.compile(r"Category limits apply as follows: (?P<list>.+)\.")],
        "cover": [re.compile(rf"{E(v.benefit_cap)} covers {E(v.amount_np)}, but not more than the limit that applies "
                             rf"under this {d}; if {E(v.amount_np)} is more than that limit, the {E(v.benefit)} is cut "
                             rf"to that limit\."),
                  re.compile(rf"{E(v.benefit_cap)} is given for {E(v.amount_np)} up to the limit that applies under "
                             rf"this {d}; where {E(v.amount_np)} goes over that limit, the {E(v.benefit)} stops at the "
                             rf"limit\.")],
        "excl": [re.compile(rf"{E(v.deny_vp)}(?: for (?P<cats>.+?))? (?:if|where) (?P<conds>.+)\.")],
        "exc": [re.compile(rf"(?P<ref>{REF_RE}) (?:does not apply|is set aside)(?: (?:to|for) (?P<cats>.+?))?"
                           rf"(?: (?:if|where) (?P<conds>.+))?\.")],
        "pexc": [re.compile(rf"(?:For (?P<cats>.+?), )?(?:(?:[Ii]f) (?P<conds>.+?), )?[Tt]he period in (?P<ref>{REF_RE}) "
                            rf"is (?P<p>\d+ (?:business )?days?) instead\."),
                 re.compile(rf"(?:For (?P<cats>.+?), )?(?:(?:[Ww]here) (?P<conds>.+?), )?[Tt]he period in "
                            rf"(?P<ref>{REF_RE}) becomes (?P<p>\d+ (?:business )?days?)\.")],
        "amend": [re.compile(rf'Amendment (?P<k>\d+), in force from (?P<d>{DATE_RE}): in (?P<ref>{REF_RE}), '
                             rf'"(?P<old>[^"]+)" is replaced by "(?P<new>[^"]+)"\.'),
                  re.compile(rf'Amendment (?P<k>\d+) \(starting (?P<d>{DATE_RE})\) changes (?P<ref>{REF_RE}) so that '
                             rf'"(?P<old>[^"]+)" becomes "(?P<new>[^"]+)"\.')],
        "amend_row": [re.compile(rf"Amendment (?P<k>\d+), in force from (?P<d>{DATE_RE}): in (?P<ref>{REF_RE}), the "
                                 rf"limit for (?P<cats>.+?) changes from (?P<old>.+?) to (?P<new>.+?)\."),
                      re.compile(rf"Amendment (?P<k>\d+) \(starting (?P<d>{DATE_RE})\) changes (?P<ref>{REF_RE}) so "
                                 rf"that the limit for (?P<cats>.+?) goes from (?P<old>.+?) to (?P<new>.+?)\.")],
        "amend_w": [re.compile(rf"Amendment (?P<k>\d+), which was to come into force on (?P<d>{DATE_RE}), was "
                               rf"withdrawn before that date; in (?P<ref>{REF_RE}), (?P<rest>.+) under it\."),
                    re.compile(rf"Amendment (?P<k>\d+) was withdrawn before its planned start on (?P<d>{DATE_RE}); it "
                               rf"would have changed (?P<ref>{REF_RE}) so that (?P<rest>.+)\.")],
        "repealed": [re.compile(rf'Former provision, repealed with effect from (?P<d>{DATE_RE}) and no longer in '
                                rf'force: "(?P<old>.+)"'),
                     re.compile(rf'Repealed on (?P<d>{DATE_RE}) and kept for reference only: "(?P<old>.+)"')],
        "named_prec": [re.compile(rf"Where (?P<a>{REF_RE}) and (?P<b>{REF_RE}) both set a limit for {E(v.a_req)}, "
                                  rf"(?P<w>{REF_RE}) prevails\."),
                       re.compile(rf"If (?P<a>{REF_RE}) and (?P<b>{REF_RE}) both set a limit for {E(v.a_req)}, "
                                  rf"(?P<w>{REF_RE}) takes priority\.")],
        "count_bus": [re.compile(rf"Periods in this {d} are counted in business days, which are Monday to Friday "
                                 rf"except the public holidays listed in (?P<ref>{REF_RE}): the date a stated number "
                                 rf"of business days after or before a given date is found by counting that many "
                                 rf"business days forward or back from it\."),
                      re.compile(rf"All periods in this {d} run in business days, meaning Monday to Friday other "
                                 rf"than the public holidays in (?P<ref>{REF_RE}); to find the date that lies a given "
                                 rf"number of business days before or after another date, count that number of "
                                 rf"business days back or forward from it\.")],
        "holidays": [re.compile(rf"The public holidays for this {d} are (?P<list>.+)\."),
                     re.compile(rf"This {d} treats these dates as public holidays: (?P<list>.+)\.")],
        "general": _general_rules(v),
    }


def _time_phrase(t: str, v: Vocab) -> dict:
    ev = re.escape(v.time["event"])
    m = re.fullmatch(rf"(?P<cmp>at least|more than) (?P<n>\d+) (?P<b>business )?days? before {ev}", t)
    if m:
        return {"dir": "before", "cmp": m["cmp"], "period": (int(m["n"]), bool(m["b"]))}
    m = re.fullmatch(rf"(?P<cmp>no later than|before) the (?P<n>\d+)(?:st|nd|rd|th) (?P<b>business )?day after {ev}",
                     t)
    if m:
        return {"dir": "after", "cmp": m["cmp"], "period": (int(m["n"]), bool(m["b"]))}
    raise ParseError(f"unknown time phrase {t!r}")


def _limit_list(text: str, v: Vocab, held: bool) -> list:
    rows = []
    for item in text.split("; "):
        m = re.fullmatch(r"(?P<cats>.+?) at (?P<q>\S.*)" if held else r"(?P<cats>.+?), (?P<q>\$?[\d,.]+(?: \w+)?)", item)
        if not m:
            raise ParseError(f"unreadable category limit {item!r}")
        rows.append((v.cats(m["cats"]), to_qty(m["q"])))
    return rows


def classify_clause(text: str, v: Vocab) -> tuple:
    """(kind, data) for one clause text. Raises ParseError for any text that is not a known clause form."""
    R = _clause_res(v.key)
    for kind in ("repealed", "amend_w", "amend_row", "amend"):
        for rx in R[kind]:
            m = rx.fullmatch(text)
            if m:
                g = m.groupdict()
                out = {"date": to_date(g["d"])}
                if "k" in g:
                    out["k"] = int(g["k"])
                if "ref" in g:
                    out["target"] = ref_key(g["ref"])
                if kind == "amend_w":
                    out["rest"] = g["rest"]
                if kind == "amend_row":
                    out["cats"] = v.cats(g["cats"])
                    out["old"], out["new"] = to_qty(g["old"]), to_qty(g["new"])
                elif kind == "amend":
                    out["old"], out["new"] = g["old"], g["new"]
                return kind, out
    for kind, texts in R["general"].items():
        if text in texts:
            return kind, {}
    for rx in R["count_bus"]:
        m = rx.fullmatch(text)
        if m:
            return "g_count_bus", {"ref": ref_key(m["ref"])}
    for rx in R["holidays"]:
        m = rx.fullmatch(text)
        if m:
            ds = re.findall(DATE_RE, m["list"])
            rest = re.sub(DATE_RE, "", m["list"])
            if not ds or re.sub(r", | and ", "", rest).strip():
                raise ParseError(f"unreadable holiday list {text!r}")
            return "g_holidays", {"dates": frozenset(to_date(x) for x in ds)}
    for rx in R["named_prec"]:
        m = rx.fullmatch(text)
        if m:
            a, b, w = ref_key(m["a"]), ref_key(m["b"]), ref_key(m["w"])
            if w not in (a, b):
                raise ParseError(f"named precedence names a third clause {text!r}")
            return "named_prec", {"a": a, "b": b, "w": w}
    for rx in R["def"]:
        m = rx.fullmatch(text)
        if m:
            subj = re.escape(v.elig["subject"])
            mm = re.fullmatch(rf"{subj} is (?P<cmp>{CMP_RE}) (?P<q>.+)", m["rest"])
            if mm:
                return "def_elig", {"term": m["term"], "cmp": mm["cmp"], "q": to_qty(mm["q"])}
            return "def_other", {"term": m["term"]}
    for rx in R["entitle"]:
        m = rx.fullmatch(text)
        if m:
            return "entitle", {"type": m["type"]}
    for rx in R["elig_term"]:
        if rx.fullmatch(text):
            return "elig_term", {"term": v.elig["term"]}
    for rx in R["elig"]:
        m = rx.fullmatch(text)
        if m:
            return "elig", {"cmp": m["cmp"], "q": to_qty(m["q"])}
    for rx in R["docs_other"]:
        m = rx.fullmatch(text)
        if m:
            if m["type"] not in v.types or m["docs"] != v.docs2:
                raise ParseError(f"unknown other-type requirement {text!r}")
            return "docs_other", {"type": m["type"]}
    for rx in R["time"]:
        m = rx.fullmatch(text)
        if m:
            return "time", _time_phrase(m["t"], v)
    for rx in R["docs"]:
        m = rx.fullmatch(text)
        if m:
            if m["docs"] != v.docs["noun"]:
                raise ParseError(f"unknown document {m['docs']!r}")
            return "docs", {}
    for rx in R["glimit"]:
        m = rx.fullmatch(text)
        if m:
            return "glimit", {"q": to_qty(m["q"])}
    for i, rx in enumerate(R["catlim"]):
        m = rx.fullmatch(text)
        if m:
            return "catlim", {"rows": _limit_list(m["list"], v, held=i == 1)}
    for rx in R["cover"]:
        if rx.fullmatch(text):
            return "cover", {}
    for rx in R["excl"]:
        m = rx.fullmatch(text)
        if m:
            return "excl", {"cats": v.cats(m["cats"]) if m["cats"] else None, "conds": v.conds(m["conds"])}
    for rx in R["pexc"]:
        m = rx.fullmatch(text)
        if m:
            return "pexc", {"target": ref_key(m["ref"]), "cats": v.cats(m["cats"]) if m["cats"] else None,
                            "conds": v.conds(m["conds"]) if m["conds"] else (), "period": to_period(m["p"])}
    for rx in R["exc"]:
        m = rx.fullmatch(text)
        if m:
            return "exc", {"target": ref_key(m["ref"]), "cats": v.cats(m["cats"]) if m["cats"] else None,
                           "conds": v.conds(m["conds"]) if m["conds"] else ()}
    if text in v.proc:
        return "proc", {}
    raise ParseError(f"unknown clause {text!r}")


def _is_heading(ln: str) -> bool:
    m = re.fullmatch(r"(?:Part \d+ - |\d+\. )?(.+)", ln)
    return bool(m) and m[1].lower() in HEADINGS


_TITLE2 = re.compile(r"Issued by .+\. Version in force from .+\.|This document is issued by .+ and applies from .+\."
                     r"|.+ - text of .+|.+, version of .+|Published by .+; this version applies from .+\.")


def parse_document(lines: list) -> Doc:
    lines = [ln for ln in lines]
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) < 3 or not _TITLE2.fullmatch(lines[1]):
        raise ParseError("document without a title and issuer line")
    v = detect_skin(lines)
    clauses, style = [], None
    table = None
    pos = 0
    for ln in lines[2:]:
        if table is not None:
            if ln == "Table (first row is the header):" and table["stage"] == 0:
                table["stage"] = 1
                continue
            if ln == "| Category | Limit |" and table["stage"] in (0, 1):
                table["stage"] = 2
                continue
            if ln == "|---|---|" and table["stage"] == 2 and not table["clause"].d["rows"] and not table.get("rule"):
                table["rule"] = True
                continue
            m = re.fullmatch(r"\| (.+?) \| (.+?) \|", ln)
            if m and table["stage"] == 2:
                table["clause"].d["rows"].append((v.cats(m[1]), to_qty(m[2])))
                continue
            if table["stage"] != 2 or not table["clause"].d["rows"]:
                raise ParseError("incomplete category table")
            table = None
        if not ln.strip() or re.fullmatch(r"Q\d+\. .+\?", ln) or _is_heading(ln):
            continue
        m = re.fullmatch(r"Table (\d+) - Category limits", ln)
        if m:
            pos += 1
            c = Clause("T" + m[1], pos, "catlim", ln, {"rows": []})
            clauses.append(c)
            table = {"stage": 0, "clause": c}
            continue
        hit = None
        for st, rx, p in LABEL_RES:
            m = rx.fullmatch(ln)
            if m:
                hit = (st, p + m[1], m[2])
                break
        if not hit:
            raise ParseError(f"unknown document line {ln!r}")
        st, key, text = hit
        if style is None:
            style = st
        elif style != st:
            raise ParseError(f"mixed clause styles {style}/{st}")
        pos += 1
        kind, d = classify_clause(text, v)
        clauses.append(Clause(key, pos, kind, text, d))
    if table is not None and not table["clause"].d["rows"]:
        raise ParseError("incomplete category table")
    by_key = {}
    for c in clauses:
        if c.key in by_key:
            raise ParseError(f"clause {c.key} given twice")
        by_key[c.key] = c
    doc = Doc(v, style, clauses, by_key)
    _finish(doc)
    return doc


def _slot_values(c: Clause) -> dict:
    if c.kind in ("elig", "def_elig", "glimit"):
        return {"q": c.d["q"]}
    if c.kind in ("time", "pexc"):
        return {"period": c.d["period"]}
    if c.kind == "catlim":
        return {("row", i): q for i, (cats, q) in enumerate(c.d["rows"])}
    if c.kind in ("exc", "excl"):
        return {("atom", j): a[2] for j, a in enumerate(c.d["conds"]) if a[0] == "amt"}
    return {}


def _finish(doc: Doc):
    v = doc.v
    kinds = [c.kind for c in doc.clauses]
    if kinds.count("g_count_cal") + kinds.count("g_count_bus") != 1:
        raise ParseError("not exactly one counting rule")
    if "g_count_bus" in kinds:
        doc.counting = "business"
        cnt = doc.of("g_count_bus")[0]
        hol = doc.by_key.get(cnt.d["ref"])
        if hol is None or hol.kind != "g_holidays":
            raise ParseError("the counting rule names no holiday clause")
        doc.holidays = hol.d["dates"]
    else:
        doc.counting = "calendar"
        if "g_holidays" in kinds:
            raise ParseError("holidays without business-day counting")
    for k in ("g_exc", "g_amend", "g_order", "g_missing"):
        if kinds.count(k) != 1:
            raise ParseError(f"general rule {k} appears {kinds.count(k)} times")
    doc.prec = [k.split(":")[1] for k in kinds if k.startswith("prec:")]
    if len(doc.prec) > 1:
        raise ParseError("two general precedence rules")
    for c in doc.of("named_prec"):
        doc.named_prec.append((c.d["a"], c.d["b"], c.d["w"]))
    ent = doc.of("entitle")
    if len(ent) != 1:
        raise ParseError("not exactly one entitlement clause")
    doc.entitle_type = ent[0].d["type"]
    for c in doc.clauses:
        for s, val in _slot_values(c).items():
            doc.slots[(c.key, s)] = val
    # every reference must name a clause of this document
    for c in doc.clauses:
        t = c.d.get("target")
        if t is not None and t not in doc.by_key:
            raise ParseError(f"{c.key} names a clause that does not exist ({t})")
    for a, b, w in doc.named_prec:
        for k in (a, b):
            if k not in doc.by_key or doc.by_key[k].kind not in ("glimit", "catlim"):
                raise ParseError("named precedence between clauses that set no limit")
    # waivers (exceptions and exceptions to exceptions)
    for c in doc.of("exc"):
        tk = doc.by_key[c.d["target"]].kind
        if tk not in ("elig", "elig_term", "time", "docs", "excl", "exc", "pexc", "glimit", "catlim"):
            raise ParseError(f"exception {c.key} to a {tk} clause")
        doc.waivers.setdefault(c.d["target"], []).append(c)
    for c in doc.of("pexc"):
        if doc.by_key[c.d["target"]].kind != "time":
            raise ParseError(f"period exception {c.key} to a non-time clause")
    # amendment chains: (clause, slot) -> amendments in date order
    hist = {k: [val] for k, val in doc.slots.items()}
    for a in sorted(doc.of("amend", "amend_row"), key=lambda c: (c.d["date"], c.d["k"])):
        tc = doc.by_key[a.d["target"]]
        slots = [s for (k, s) in doc.slots if k == tc.key]
        if a.kind == "amend_row":
            if tc.kind != "catlim":
                raise ParseError(f"{a.key} changes a category limit of a {tc.kind} clause")
            hits = [("row", i) for i, (cats, q) in enumerate(tc.d["rows"]) if cats == a.d["cats"]]
            if len(hits) != 1:
                raise ParseError(f"{a.key} names a category row that is not in {tc.key}")
            slot = hits[0]
            old, new = a.d["old"], a.d["new"]
        else:
            if not slots:
                raise ParseError(f"{a.key} amends {tc.key}, which has no figure")
            conv = to_period if tc.kind in ("time", "pexc") else to_qty
            old, new = conv(a.d["old"]), conv(a.d["new"])
            if len(slots) == 1:
                slot = slots[0]
            else:
                cand = [s for s in slots if old in hist[(tc.key, s)]]
                if len(cand) != 1:
                    raise ParseError(f"{a.key}: the figure it replaces is not unique in {tc.key}")
                slot = cand[0]
        a.d["slot"], a.d["old_v"], a.d["new_v"] = slot, old, new
        if hist[(tc.key, slot)][-1] != old:
            doc.notes.append(f"{a.key}: replaces {old} but the figure before it is {hist[(tc.key, slot)][-1]}")
        if isinstance(old, Qty) and (old.u != new.u or old.u != hist[(tc.key, slot)][0].u):
            raise ParseError(f"{a.key}: unit change")
        if isinstance(old, tuple) and old[1] != new[1]:
            raise ParseError(f"{a.key}: calendar/business change")
        hist[(tc.key, slot)].append(new)
        doc.chains.setdefault((tc.key, slot), []).append(a)


# ------------------------------------------------------------------------------------------------ evaluation
@dataclass
class Result:
    code: str
    granted: Qty | None
    grounds: list
    limit: Qty | None = None
    trace: list = field(default_factory=list)

    def text(self, v: Vocab) -> str:
        return v.outcomes[self.code]


def shift(d: dt.date, n: int, sign: int, business: bool, holidays) -> dt.date:
    if not business:
        return d + dt.timedelta(days=sign * n)
    k = 0
    while k < n:
        d += dt.timedelta(days=sign)
        if d.weekday() < 5 and d not in holidays:
            k += 1
    return d


def _business_count_ok(received: dt.date, event: dt.date, direction: str, op: str, n: int, holidays) -> bool:
    """The 'count' reading: business days in [received, event) for 'before' limits, in (event, received] for 'after'."""
    def bd(a: dt.date, b: dt.date) -> int:  # business days in [a, b)
        k, d = 0, a
        while d < b:
            k += d.weekday() < 5 and d not in holidays
            d += dt.timedelta(days=1)
        return k
    if direction == "before":
        k = bd(received, event) if received < event else -bd(event, received)
        return k >= n if op == "at least" else k > n
    k = bd(event + dt.timedelta(days=1), received + dt.timedelta(days=1)) if received > event else 0
    return k <= n if op == "no later than" else k < n


def effective(doc: Doc, received: dt.date | None, deleted=frozenset(), rd: dict | None = None) -> dict:
    """Figures in force on the received date: the latest amendment in force (not withdrawn, not deleted) wins."""
    rd = rd or {}
    eff = dict(doc.slots)
    if rd.get("probe_no_amendments"):
        return eff
    for ks, chain in doc.chains.items():
        live = [a for a in chain if a.key not in deleted and received is not None and a.d["date"] <= received]
        if live:
            eff[ks] = live[-1].d["new_v"]
    if rd.get("probe_withdrawn_apply"):
        for a in doc.of("amend_w"):
            m = re.fullmatch(r'"([^"]+)" is replaced by "([^"]+)"|"([^"]+)" becomes "([^"]+)"', a.d.get("rest", ""))
            if m and a.d["date"] <= (received or a.d["date"]):
                tc = doc.by_key[a.d["target"]]
                conv = to_period if tc.kind in ("time", "pexc") else to_qty
                slots = [s for (k, s) in doc.slots if k == tc.key]
                if len(slots) == 1:
                    eff[(tc.key, slots[0])] = conv(m[2] or m[4])
    return eff


def evaluate(doc: Doc, case: Case, deleted=frozenset(), readings: dict | None = None) -> Result:
    rd = {**DEFAULT_READINGS, **(readings or {})}
    eff = effective(doc, case.received, deleted, rd)
    trace = []
    memo = {}
    holidays = frozenset() if rd.get("probe_ignore_holidays") else doc.holidays
    incl = {"more than": "at least", "less than": "at most", "before": "no later than"} \
        if rd.get("probe_inclusive") else {}

    def conds_hold(c: Clause) -> bool:
        cats = c.d.get("cats")
        if cats is not None and case.cat not in cats and not rd.get("probe_ignore_cats"):
            return False
        for j, a in enumerate(c.d.get("conds", ())):
            if a[0] == "flag":
                if case.flags.get(a[1]) is not True:
                    return False
            else:
                q = eff[(c.key, ("atom", j))]
                if case.amount is None or case.amount.u != q.u or not cmp_ok(case.amount.v, a[1], q.v):
                    return False
        return True

    def applies(e: Clause) -> bool:  # an exception (or exception to one) that applies
        return e.key not in deleted and conds_hold(e) and not waived(e.key)

    def waived(key: str) -> bool:
        if key in memo:
            return memo[key]
        memo[key] = False
        if rd.get("probe_no_exceptions") or (rd.get("probe_no_exc_to_exc") and doc.by_key[key].kind in ("exc", "pexc")):
            return False
        memo[key] = any(applies(e) for e in doc.waivers.get(key, ()))
        return memo[key]

    def active(c: Clause) -> bool:
        return c.key not in deleted and not waived(c.key)

    grounds = []
    # eligibility
    for c in doc.of("elig", "elig_term"):
        if not active(c):
            trace.append(f"{c.key} eligibility: not applied")
            continue
        if c.kind == "elig":
            op, q = c.d["cmp"], eff[(c.key, "q")]
        else:
            defs = [x for x in doc.of("def_elig") if x.d["term"].lower() == c.d["term"].lower()]
            if len(defs) != 1:
                raise ParseError(f"{c.key}: the eligibility term is not defined exactly once")
            op, q = defs[0].d["cmp"], eff[(defs[0].key, "q")]
        if case.elig is not None and case.elig.u != q.u:
            raise ParseError(f"eligibility unit {case.elig.u} vs {q.u}")
        op = incl.get(op, op)
        ok = case.elig is not None and cmp_ok(case.elig.v, op, q.v)
        trace.append(f"{c.key} eligibility: {case.elig} {op} {q} -> {ok}")
        if not ok:
            grounds.append((c.pos, "INELIG", c.key))
    # time
    for c in doc.of("time"):
        if not active(c):
            trace.append(f"{c.key} time: not applied")
            continue
        period = eff[(c.key, "period")]
        pex = [p for p in doc.of("pexc") if p.d["target"] == c.key and applies(p)
               and not rd.get("probe_no_period_exc") and not rd.get("probe_no_exceptions")]
        if len({eff[(p.key, "period")] for p in pex}) > 1:
            raise ParseError(f"{c.key}: two period exceptions with different periods apply")
        if pex:
            period = eff[(pex[0].key, "period")]
            trace.append(f"{c.key}: period from {pex[0].key}")
        n, bus = period
        if bus != (doc.counting == "business"):
            raise ParseError(f"{c.key}: period unit does not match the counting rule")
        if rd.get("probe_calendar_days"):
            bus = False
        op = incl.get(c.d["cmp"], c.d["cmp"])
        if case.event is None or case.received is None:
            ok = False
        elif bus and rd["business_limit"] == "count":
            ok = _business_count_ok(case.received, case.event, c.d["dir"], op, n, holidays)
            trace.append(f"{c.key} time (business-day count reading): {ok}")
        elif c.d["dir"] == "before":
            dl = shift(case.event, n, -1, bus, holidays)
            ok = case.received <= dl if op == "at least" else case.received < dl
            trace.append(f"{c.key} time: received {case.received} vs {c.d['cmp']} {n}{'b' if bus else ''} before "
                         f"{case.event} (= {dl}) -> {ok}")
        else:
            dl = shift(case.event, n, +1, bus, holidays)
            ok = case.received <= dl if op == "no later than" else case.received < dl
            trace.append(f"{c.key} time: received {case.received} vs {c.d['cmp']} day {n}{'b' if bus else ''} "
                         f"after {case.event} (= {dl}) -> {ok}")
        if not ok:
            grounds.append((c.pos, "LATE", c.key))
    # documents
    for c in doc.of("docs"):
        if active(c) and not case.docs:
            grounds.append((c.pos, "DOCS", c.key))
        trace.append(f"{c.key} docs: {'not applied' if not active(c) else case.docs}")
    for c in doc.of("docs_other"):
        if case.rtype == c.d["type"]:
            raise ParseError(f"{c.key}: the other-type requirement names the case's request type")
    # exclusions
    for c in doc.of("excl"):
        if active(c) and conds_hold(c):
            grounds.append((c.pos, "EXCL", c.key))
            trace.append(f"{c.key} exclusion applies")
    grounds.sort()
    if grounds:
        return Result(grounds[0][1], None, grounds, None, trace)
    # limits
    G = [c for c in doc.of("glimit") if active(c)]
    K = [c for c in doc.of("catlim") if active(c)]
    if len(G) > 1 or len(K) > 1:
        raise ParseError("two general limits or two category-limit clauses in force")
    g = (G[0], eff[(G[0].key, "q")]) if G else None
    k = None
    if K:
        rows = [i for i, (cats, q) in enumerate(K[0].d["rows"]) if case.cat in cats]
        if len(rows) > 1:
            raise ParseError("the category appears in two limit rows")
        if rows:
            k = (K[0], eff[(K[0].key, ("row", rows[0]))])
    if g and k:
        named = [w for a, b, w in doc.named_prec if {a, b} == {g[0].key, k[0].key}]
        if rd.get("probe_prec_lower"):
            lim = g if g[1].v < k[1].v else k
        elif named:
            lim = g if named[0] == g[0].key else k
            trace.append(f"limit: named precedence -> {lim[0].key}")
        elif doc.named_prec:
            raise ParseError("named precedence names other clauses")
        elif doc.prec == ["category"]:
            lim = k
        elif doc.prec == ["later"]:
            lim = g if g[0].pos > k[0].pos else k
        elif doc.prec == ["lower"]:
            lim = g if g[1].v < k[1].v else k
        else:
            raise ParseError("two limits and no precedence rule")
        limit = lim[1]
    else:
        limit = g[1] if g else (k[1] if k else None)
    if case.amount is None:
        raise ParseError("no amount requested")
    if limit is not None and limit.u != case.amount.u:
        raise ParseError(f"limit unit {limit.u} vs amount unit {case.amount.u}")
    trace.append(f"limit {limit} (general {g[1] if g else None}, category {k[1] if k else None}); "
                 f"requested {case.amount}")
    if limit is not None and case.amount.v > limit.v:
        return Result("PARTIAL", limit, [], limit, trace)
    return Result("FULL", case.amount, [], limit, trace)


CANDIDATES = ("elig", "elig_term", "time", "docs", "docs_other", "excl", "exc", "pexc", "amend", "amend_row",
              "amend_w", "glimit", "catlim")


def _ref_text(doc: Doc, key: str, lower: bool) -> str:
    p, n = key[0], key[1:]
    word = {"S": "clause" if doc.contract else "section", "R": "Rule", "A": "answer", "C": "C", "T": "Table"}[p]
    if p in "ST" or p == "A":
        word = word if lower else cap(word)
    return f"{word}{'' if p == 'C' else ' '}{n}"


def describe(doc: Doc, c: Clause) -> set:
    """The option descriptions that may name clause c in a 'which clause is decisive' question."""
    v = doc.v
    if c.kind in ("elig", "elig_term"):
        return {v.elig["label"].lower() + " requirement"}
    if c.kind == "docs":
        return {v.docs["label"].lower() + " requirement"}
    if c.kind == "docs_other":
        return {f"extra requirement for {article(c.d['type'])} {c.d['type']}"}
    if c.kind == "time":
        return {"time limit"}
    if c.kind == "excl":
        return {"exclusion"}
    if c.kind in ("exc", "pexc"):
        tk = doc.by_key[c.d["target"]].kind
        word = "limit on" if tk in ("exc", "pexc") else "exception to"
        return {f"{word} {_ref_text(doc, c.d['target'], lower=True)}"}
    if c.kind in ("amend", "amend_row", "amend_w"):
        return {f"Amendment {c.d['k']}"}
    if c.kind == "glimit":
        return {"general limit"}
    if c.kind == "catlim":
        return {"category limits"}
    return set()


def decisive(doc: Doc, case: Case, base: Result, key: str, readings: dict) -> bool:
    r = evaluate(doc, case, frozenset({key}), readings)
    if readings["decisive_outcome"] == "code":
        return r.code != base.code
    return (r.code, r.granted) != (base.code, base.granted)


# ------------------------------------------------------------------------------------------------ F1a questions
def _q_res(v: Vocab) -> list:
    d, req = re.escape(v.doc), re.escape(v.req)
    O = r'"(?P<out>[^"]+)"'
    return [
        ("pos", re.compile(rf"Under the {d}, is the outcome of this {req} {O}\?")),
        ("pos", re.compile(rf"Applying the {d} to the case file, is the outcome of this {req} {O}, rather than a "
                           rf"different outcome\?")),
        ("pos", re.compile(rf"Does the {d} give this {req} the outcome {O}, rather than a different one\?")),
        ("inv", re.compile(rf"Under the {d}, is the outcome of this {req} different from {O}\?")),
        ("inv", re.compile(rf"Applying the {d} to the case file, is the outcome of this {req} a different outcome "
                           rf"from {O}\?")),
        ("jdg", re.compile(rf"The case file shows a decision recorded for this {req}\. Is that recorded decision "
                           rf"consistent with the {d}, rather than at odds with it\?")),
        ("jdg", re.compile(rf"Is the decision recorded for this {req} supported by the {d} when it is applied to the "
                           rf"case file\?")),
        ("jdg", re.compile(rf"Is the decision recorded for this {req} in line with the {d}, rather than at odds with "
                           rf"it\?")),
        ("jinv", re.compile(rf"Is the decision recorded for this {req} at odds with the {d} when it is applied to the "
                            rf"case file\?")),
        ("out", re.compile(rf"Under the {d}, what is the outcome of this {req}\?")),
        ("out", re.compile(rf"Which outcome does the {d} give this {req}\?")),
        ("dec", re.compile(rf"Which of these clauses decides this {req} under the {d}, that is, deleting that one "
                           rf"clause alone would change the outcome\?")),
        ("dec", re.compile(rf"Deleting which one of these clauses of the {d} would, on its own, change the outcome of "
                           rf"this {req}\?")),
        ("amt", re.compile(rf"Under the {d}, which range contains the (?P<what>amount|number of \w+) given for this "
                           rf"{req}\?")),
        ("amt", re.compile(rf"Which of these ranges holds the (?P<what>amount|number of \w+) that this {req} receives "
                           rf"under the {d}\?")),
        ("jbq", re.compile(rf"Which of these statements about this {req} does the {d} bear out\?")),
        ("jbf", re.compile(rf"Does the {d} bear out this statement about this {req}: the outcome is {O}\?")),
    ]


def classify_question(instr: str, v: Vocab):
    for q, rx in _q_res(v):
        m = rx.fullmatch(instr)
        if m:
            return q, m.groupdict()
    raise ParseError(f"unknown question {instr!r}")


def _range(opt: str, unit: str):
    """(lo, hi) inclusive bounds of an amount-range option (None = open)."""
    N = r"(\$?[\d,]+(?:\.\d+)?)"
    u = "" if unit == "$" else " " + re.escape(unit)
    for rx, f in ((rf"less than {N}{u}", lambda a: (None, a, True)),
                  (rf"{N} to {N}{u}", lambda a, b: (a, b, False)),
                  (rf"{N}{u} or more", lambda a: (a, None, False))):
        m = re.fullmatch(rx, opt)
        if m:
            vals = []
            for g in m.groups():
                if (unit == "$") != g.startswith("$"):
                    raise ParseError(f"range option unit {opt!r}")
                vals.append(to_num(g.lstrip("$")))
            return f(*vals)
    raise ParseError(f"unreadable range option {opt!r}")


def _in_range(x: Fraction, r) -> bool:
    lo, hi, strict_hi = r
    if lo is not None and x < lo:
        return False
    if hi is not None and (x >= hi if strict_hi else x > hi):
        return False
    return True


def parse_f1a(state: str):
    sp = split_state(state)
    doc = parse_document(sp.doc_lines)
    doc.contract = any(re.search(r"\b[Cc]lause \d+\.\d+", c.text) for c in doc.clauses) or \
        any(ln.startswith("This document is issued by ") for ln in sp.doc_lines[:2])
    case = parse_case(sp, doc.v)
    if case.rtype is not None and case.rtype != doc.entitle_type:
        raise ParseError("the case's request type is not the entitlement's type")
    return sp, doc, case


def solve_f1a(row: dict, readings: dict) -> dict:
    sp, doc, case = parse_f1a(row["state"])
    v = doc.v
    res = evaluate(doc, case, frozenset(), readings)
    q, g = classify_question(row["instructions"], v)
    opts = list(row["options"])
    out_text = res.text(v)
    info = {"q": q, "code": res.code, "granted": str(res.granted) if res.granted else None, "fmt": sp.fmt,
            "skin": v.key, "style": doc.style, "grounds": [x[1:] for x in res.grounds], "notes": list(doc.notes),
            "trace": res.trace}
    if len(res.grounds) > 1:
        info["notes"].append(f"{len(res.grounds)} grounds for refusal")
    if q in ("pos", "inv", "jdg", "jinv", "jbf"):
        if q in ("jdg", "jinv"):
            if case.decision is None:
                raise ParseError("judge question without a recorded decision")
            named = case.decision
        else:
            named = g["out"]
        if named not in v.code_by_text:
            raise ParseError(f"the question names an unknown outcome {named!r}")
        holds = named == out_text
        if q == "jbf":
            if opts != ["yes, this holds", "no, this does not hold"]:
                raise ParseError("unexpected jbf options")
            info["gold2"] = opts[0] if holds else opts[1]
        else:
            if opts != ["yes", "no"]:
                raise ParseError("yes/no row without yes/no options")
            info["gold2"] = "yes" if holds == (q in ("pos", "jdg")) else "no"
        return info
    if q == "jbq":
        if len(opts) != 2:
            raise ParseError("jb row without 2 options")
        m1 = re.fullmatch(rf'Under the {re.escape(v.doc)}, the outcome of this {re.escape(v.req)} is "([^"]+)"\.',
                          opts[0])
        m2 = re.fullmatch(rf'Under the {re.escape(v.doc)}, the outcome of this {re.escape(v.req)} is some other '
                          rf'outcome than "([^"]+)"\.', opts[1])
        if not (m1 and m2 and m1[1] == m2[1] and m1[1] in v.code_by_text):
            raise ParseError("unexpected jbq options")
        info["gold2"] = opts[0] if m1[1] == out_text else opts[1]
        return info
    if q == "out":
        for o in opts:
            if o not in v.code_by_text and o != "None of the outcomes listed":
                raise ParseError(f"unknown outcome option {o!r}")
        if out_text in opts:
            info["gold2"] = out_text
        elif "None of the outcomes listed" in opts:
            info["gold2"] = "None of the outcomes listed"
        else:
            raise ParseError("the outcome is not among the options and no 'none' option")
        return info
    if q == "amt":
        if res.code not in ("PARTIAL", "FULL"):
            raise ParseError("amount question on a refusal")
        unit = res.granted.u
        if (g["what"] == "amount") != (unit == "$") or (unit != "$" and g["what"] != f"number of {unit}"):
            raise ParseError(f"amount question asks for {g['what']!r} but the unit is {unit!r}")
        hits = [o for o in opts if _in_range(res.granted.v, _range(o, unit))]
        if len(hits) != 1:
            raise ParseError(f"amount {res.granted} falls in {len(hits)} options")
        info["gold2"] = hits[0]
        return info
    if q == "dec":
        piv, seen = [], []
        none_opt = "None of the clauses listed"
        for o in opts:
            if o == none_opt:
                continue
            m = re.fullmatch(rf"(?P<ref>{REF_RE}) \((?P<desc>.+)\)", o)
            if not m:
                raise ParseError(f"unreadable clause option {o!r}")
            key = ref_key(m["ref"])
            c = doc.by_key.get(key)
            if c is None or c.kind not in CANDIDATES:
                raise ParseError(f"option {o!r} names no candidate clause")
            if m["desc"] not in describe(doc, c):
                raise ParseError(f"option {o!r}: description does not fit {c.kind} {c.text!r}")
            seen.append(key)
            if decisive(doc, case, res, key, readings):
                piv.append(o)
        all_piv = [c.key for c in doc.clauses if c.kind in CANDIDATES and decisive(doc, case, res, c.key, readings)]
        info["pivotal_all"] = all_piv
        if len(all_piv) != 1:
            info["notes"].append(f"{len(all_piv)} decisive clauses in the document")
        if len(piv) > 1:
            raise ParseError(f"two listed clauses are decisive: {piv}")
        if piv:
            info["gold2"] = piv[0]
        elif none_opt in opts:
            info["gold2"] = none_opt
        else:
            raise ParseError("no listed clause is decisive and no 'none' option")
        return info
    raise ParseError(f"question kind {q}")


# ------------------------------------------------------------------------------------------------ F1b
NB_QUESTIONS = {
    "Under the rules in the card, does the evidence establish the claim?": ("claim", True),
    "Read with the card's rules, do the figures in the evidence establish the claim, rather than fail to establish "
    "it?": ("claim", True),
    "Under the rules in the card, does the evidence fail to establish the claim?": ("claim", False),
    "The fact-check log has an entry for this claim. Is that entry consistent with the evidence under the card's "
    "rules, rather than at odds with it?": ("log", True),
    "Under the card's rules, is the fact-check log entry for this claim supported by the evidence?": ("log", True),
    "Under the card's rules, is the fact-check log entry for this claim at odds with the evidence, rather than "
    "supported by it?": ("log", False),
}


@dataclass
class NB:
    evidence: list
    claim: str
    log: str | None


def parse_nb(state: str) -> NB:
    s = state
    if s.lstrip().startswith("{"):
        obj = json.loads(s)
        if set(obj) != {"evidence", "claim", "fact_check_log", "notes"}:
            raise ParseError(f"unexpected json keys {sorted(obj)}")
        return NB(list(obj["evidence"]), obj["claim"], obj["fact_check_log"])
    if s.startswith("## Evidence\n"):
        secs = {}
        for part in ("\n" + s).split("\n## ")[1:]:
            title, _, body = part.partition("\n")
            secs[title] = body.strip("\n")
        if not {"Evidence", "Claim"} <= set(secs) or set(secs) - {"Evidence", "Claim", "Fact-check log", "Notes"}:
            raise ParseError(f"unexpected markdown sections {sorted(secs)}")
        ev = []
        for ln in secs["Evidence"].split("\n"):
            if not ln.startswith("- "):
                raise ParseError(f"bad evidence line {ln!r}")
            ev.append(ln[2:])
        log = None
        if "Fact-check log" in secs:
            m = re.fullmatch(r"Entry for this claim: (SUPPORTED|NOT SUPPORTED)", secs["Fact-check log"])
            if not m:
                raise ParseError("bad fact-check log section")
            log = m[1]
        return NB(ev, secs["Claim"], log)
    body = s.split("\n\nNote added by ")[0]
    if body.startswith("evidence.1: "):
        ev, claim, log = [], None, None
        for ln in body.split("\n"):
            m = re.fullmatch(r"evidence\.\d+: (.+)", ln)
            if m:
                ev.append(m[1])
                continue
            m = re.fullmatch(r"claim: (.+)", ln)
            if m:
                claim = m[1]
                continue
            m = re.fullmatch(r"fact_check_log: (SUPPORTED|NOT SUPPORTED)", ln)
            if m:
                log = m[1]
                continue
            raise ParseError(f"bad kv line {ln!r}")
        if claim is None:
            raise ParseError("no claim")
        return NB(ev, claim, log)
    paras = body.split("\n\n")
    ev = []
    if paras[0].startswith("Evidence log\n"):
        for ln in paras[0].split("\n")[1:]:
            m = re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ \[report\] (.+)", ln)
            if not m:
                raise ParseError(f"bad evidence log line {ln!r}")
            ev.append(m[1])
    else:
        ev = split_sentences(paras[0])
    claim, log = None, None
    for p in paras[1:]:
        m = re.fullmatch(r"Claim: (.+)", p)
        if m:
            claim = m[1]
            continue
        m = re.fullmatch(r"Fact-check log entry: (SUPPORTED|NOT SUPPORTED)", p)
        if m:
            log = m[1]
            continue
        raise ParseError(f"bad paragraph {p[:60]!r}")
    if claim is None:
        raise ParseError("no claim")
    return NB(ev, claim, log)


@dataclass
class Report:
    date: dt.date
    value: Fraction
    unit: str
    text: str
    period: str | None
    entity: str | None
    revisions: list = field(default_factory=list)   # (date, from, to)


def _fig(s: str):
    """(value, unit token, rest) of a figure text such as '$558,590 in online sales' or '112,529 kWh of ...'."""
    m = re.fullmatch(r"(\$)?(" + NUM_RE + r")(?: (.+))?", s.strip())
    if not m:
        raise ParseError(f"not a figure {s!r}")
    rest = m[3] or ""
    unit = "$" if m[1] else (rest.split(" ")[0] if rest else "")
    return to_num(m[2]), unit, rest


CARD_LOOKUP = None  # optional hook: fn(qid) -> card dict (for in-memory rows whose card file is not written yet)


def set_card_lookup(fn) -> None:
    """Lets a caller holding unwritten cards (e.g. a FamilyBuilder's .defs.get) supply them; None restores disk."""
    global CARD_LOOKUP
    CARD_LOOKUP = fn


def nb_card(row: dict) -> dict:
    """The printed card of an F1b row (meta.defs -> yn2b_defs/<key>__<qid>.json): the rules the question refers to."""
    qid = row["meta"].get("defs")
    if not qid:
        raise ParseError("F1b row without a card")
    card = CARD_LOOKUP(qid) if CARD_LOOKUP else None
    if card is None:
        p = DEFS / f"{KEY}__{qid}.json"
        if not p.exists():
            raise ParseError(f"card file missing: {p.name}")
        card = json.loads(p.read_text())
    rules = {}
    for k, val in card.items():
        if k in ("yes", "no"):
            continue
        if k == "figures" and val == "Figures are used exactly as printed; nothing is rounded.":
            rules["figures"] = True
        elif k == "revisions" and val == "When a figure is revised, only the most recent revision of it counts.":
            rules["revisions"] = True
        elif k == "as of" and val == "A figure as of a date is the latest figure reported on or before that date.":
            rules["asof"] = True
        elif k == "percent change" and val == ("A percentage change is measured against the earlier of the two "
                                               "figures."):
            rules["pct_base_earlier"] = True
        elif k == "about":
            m = re.fullmatch(r'"About N" means within (\$)?(' + NUM_RE + r')(?: (\S+))? of N, counting both ends\.',
                             val)
            if not m:
                raise ParseError(f"unknown about rule {val!r}")
            rules["about"] = (to_num(m[2]), "$" if m[1] else (m[3] or ""))
        elif k == "conversion":
            m = re.fullmatch(r"For this check, (" + NUM_RE + r") (\S+) = (" + NUM_RE + r") (\S+)\.", val)
            if not m:
                raise ParseError(f"unknown conversion rule {val!r}")
            rules["conv"] = (m[2], to_num(m[3]) / to_num(m[1]), m[4])
        else:
            raise ParseError(f"unknown card rule {k!r}: {val!r}")
    return {"rules": rules, "card": card}


_UNIT_ALIASES = {"tonne": "tonnes", "tonnes": "tonnes", "kilograms": "kilograms", "kilogram": "kilograms",
                 "kWh": "kWh", "MJ": "MJ", "EUR": "EUR", "USD": "USD", "$": "USD"}


def _unit_norm(u: str) -> str:
    return _UNIT_ALIASES.get(u, u)


def nb_truth(nb: NB, rules: dict, readings: dict) -> dict:
    reps = []
    for e in nb.evidence:
        m = re.fullmatch(rf"As of (?P<d>{DATE_RE}), (?P<src>.+?) reported (?P<fig>.+?)"
                         rf"(?: for the (?P<per>first|second) period)?(?: for (?P<ent>(?!the (?:first|second) period)"
                         rf".+?))?\.", e)
        if m:
            val, unit, rest = _fig(m["fig"])
            reps.append(Report(to_date(m["d"]), val, unit, m["fig"], m["per"], m["ent"]))
            continue
        m = re.fullmatch(rf"On (?P<d>{DATE_RE}), (?P<src>.+?) revised that figure from (?P<a>.+?) to (?P<b>.+?)\.", e)
        if m:
            reps.append(("rev", to_date(m["d"]), _fig(m["a"]), _fig(m["b"])))
            continue
        raise ParseError(f"unknown evidence sentence {e!r}")
    figs = [r for r in reps if isinstance(r, Report)]
    revs = sorted([r for r in reps if not isinstance(r, Report)], key=lambda r: r[1])
    if revs and not rules.get("revisions"):
        raise ParseError("revisions without the card's revision rule")
    for _, d, a, b in revs:
        cand = [f for f in figs if (f.revisions[-1][2] if f.revisions else f.value) == a[0] and f.date <= d]
        if len(cand) != 1:
            raise ParseError(f"revision from {a[0]}: {len(cand)} matching figures")
        f = cand[0]
        for x in (a, b):
            if x[2] and x[1] != f.unit:
                raise ParseError("revision unit")
        f.revisions.append((d, a[0], b[0]))

    def value(f: Report, asof: dt.date | None = None) -> Fraction:
        rs = [] if readings.get("probe_nb_no_revisions") else f.revisions
        if asof is not None and readings["nb_revision_by_date"]:
            rs = [r for r in rs if r[0] <= asof]
        return rs[-1][2] if rs else f.value

    def series(period=None, entity=None, asof=None) -> Report:
        cand = [f for f in figs if f.period == period and (f.entity or "").lower() == (entity or "").lower()]
        if asof is not None and readings.get("probe_nb_asof_latest"):
            top = max(f.date for f in cand)
            cand = [f for f in cand if f.date == top]
        elif asof is not None:
            if not rules.get("asof"):
                raise ParseError("as-of claim without the card's as-of rule")
            cand = [f for f in cand if f.date <= asof]
            if not cand:
                raise ParseError("no figure on or before the as-of date")
            top = max(f.date for f in cand)
            cand = [f for f in cand if f.date == top]
        if len(cand) != 1:
            raise ParseError(f"{len(cand)} figures for period={period} entity={entity} asof={asof}")
        return cand[0]

    claim = nb.claim
    out = {"claim": claim}

    def conv(f: Report, x: Fraction, cunit: str) -> Fraction:
        fu, cu = _unit_norm(f.unit), _unit_norm(cunit)
        if "conv" in rules and not readings.get("probe_nb_no_conversion"):
            su, fac, du = rules["conv"]
            su, du = _unit_norm(su), _unit_norm(du)
            if fu == su and cu == du:
                return x * fac
            if fu == du and cu == su:
                return x / fac
        return x

    m = re.fullmatch(rf"Taken together, (?P<ents>.+) had (?P<cmp>{CMP_RE}) (?P<c>.+)\.", claim)
    if m:
        ents = [f.entity for f in figs if f.entity]
        pair = [(a, b) for a in ents for b in ents if a != b and m["ents"].lower() == f"{a} and {b}".lower()]
        if len(pair) != 1:
            raise ParseError("sum claim: entities not found")
        e1, e2 = series(entity=pair[0][0]), series(entity=pair[0][1])
        c, cu, _ = _fig(m["c"])
        x = value(e1) + value(e2)
        out.update(kind="sum", x=x, c=c, holds=cmp_ok(x, m["cmp"], c))
        return out
    m = re.fullmatch(rf"(?P<e1>.+?) had (?P<cmp>{CMP_RE}) (?P<c>\$?{NUM_RE}(?: (?:kWh|MJ|tonnes?|kilograms|EUR|USD))?) "
                     rf"more (?P<noun>.+?) than (?P<e2>.+)\.", claim)
    if m:
        e1, e2 = series(entity=m["e1"]), series(entity=m["e2"])
        c, cu, _ = _fig(m["c"])
        if e1.unit != e2.unit:
            raise ParseError("difference of figures in two units")
        x = conv(e1, value(e1) - value(e2), cu)
        out.update(kind="difference", x=x, c=c, holds=cmp_ok(x, m["cmp"], c))
        return out
    m = re.fullmatch(rf"(?P<subj>.+?) (?P<dir>rose|fell) by (?P<cmp>{CMP_RE}) (?P<p>{NUM_RE})% from the first "
                     rf"period to the second period\.", claim)
    if m:
        if not rules.get("pct_base_earlier"):
            raise ParseError("percentage claim without the card's base rule")
        f1, f2 = series(period="first"), series(period="second")
        if f1.date > f2.date:
            raise ParseError("first-period figure reported after the second")
        a, b = value(f1), value(f2)
        ch = (b - a) / a * 100
        x = ch if m["dir"] == "rose" else -ch
        p = to_num(m["p"])
        holds = cmp_ok(x, m["cmp"], p)
        if readings["nb_pct_direction"] == "strict" and x < 0:
            holds = False
        out.update(kind="pct", x=x, c=p, holds=holds)
        return out
    m = re.fullmatch(rf"(?P<subj>.+?)(?: as of (?P<d>{DATE_RE}))? was about (?P<c>.+)\.", claim)
    if m:
        if "about" not in rules:
            raise ParseError("about claim without the card's tolerance")
        f = series(asof=to_date(m["d"]) if m["d"] else None)
        c, cu, _ = _fig(m["c"])
        x = conv(f, value(f, to_date(m["d"]) if m["d"] else None), cu)
        tol, tu = rules["about"]
        out.update(kind="about", x=x, c=c, holds=abs(x - c) <= tol)
        return out
    m = re.fullmatch(rf"(?P<subj>.+?)(?: as of (?P<d>{DATE_RE}))? was (?P<cmp>{CMP_RE}) (?P<c>.+)\.", claim)
    if m:
        asof = to_date(m["d"]) if m["d"] else None
        f = series(asof=asof)
        c, cu, _ = _fig(m["c"])
        x = conv(f, value(f, asof), cu)
        out.update(kind="threshold", x=x, c=c, holds=cmp_ok(x, m["cmp"], c))
        return out
    raise ParseError(f"unknown claim {claim!r}")


def solve_nb(row: dict, readings: dict) -> dict:
    qk, pos = NB_QUESTIONS[row["instructions"]]
    if list(row["options"]) != ["yes", "no"]:
        raise ParseError("F1b row without yes/no options")
    nb = parse_nb(row["state"])
    card = nb_card(row)
    t = nb_truth(nb, card["rules"], readings)
    if qk == "claim":
        ans = t["holds"] == pos
    else:
        if nb.log is None:
            raise ParseError("log question without a fact-check log entry")
        ans = ((nb.log == "SUPPORTED") == t["holds"]) == pos
    return {"q": "nb_" + qk, "gold2": "yes" if ans else "no", "kind": t["kind"], "holds": t["holds"],
            "x": str(t["x"]), "c": str(t["c"]), "notes": []}


# ------------------------------------------------------------------------------------------------ entry points
def solve(row: dict, readings: dict | None = None) -> dict:
    rd = {**DEFAULT_READINGS, **(readings or {})}
    if row["instructions"] in NB_QUESTIONS:
        return solve_nb(row, rd)
    return solve_f1a(row, rd)


def decide2_row_strict(row: dict, readings: dict | None = None) -> str:
    """decide2 on the rendered row; raises ParseError when the row cannot be read unambiguously."""
    return solve(row, readings)["gold2"]


def decide2_row(row: dict, readings: dict | None = None):
    """SPEC 8.1 decide2 for mv_core.verify_labels: 'yes'/'no' or the gold option string; mv_core.UNDEFINED when the
    row cannot be read (a failure there). Never raises on a row it cannot read."""
    try:
        return decide2_row_strict(row, readings)
    except (ParseError, KeyError, ValueError, ZeroDivisionError, json.JSONDecodeError):
        import mv_core
        return mv_core.UNDEFINED


decide2_row_safe = decide2_row  # the name the other families' decide2 modules use


# ------------------------------------------------------------------------------------------------ reports
def load_rows(split: str = "train") -> list[dict]:
    p = RAW / (f"{KEY}.jsonl" if split == "train" else f"dev/{KEY}.jsonl")
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def load_rels(split: str = "train") -> list[dict]:
    p = RAW / ("relations" if split == "train" else "dev/relations") / f"{KEY}.jsonl"
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def _tab_key(r: dict) -> str:
    m = r["meta"]
    return f"{m.get('dev_kind') or 'train'}/{'F1b' if m['pack'].startswith('nb_') else 'F1a'}/{m['qkind']}/{m['view']}"


def _try(row: dict, readings: dict | None = None):
    try:
        return solve(row, readings), None
    except (ParseError, KeyError, ValueError, ZeroDivisionError, json.JSONDecodeError) as e:
        return None, f"{type(e).__name__}: {e}"


def agreement(rows: list[dict], readings: dict | None = None) -> dict:
    from collections import Counter, defaultdict
    tab = defaultdict(Counter)
    dis, answers, infos = [], {}, {}
    for r in rows:
        info, err = _try(r, readings)
        g2 = info["gold2"] if info else None
        answers[r["rid"]] = g2
        infos[r["rid"]] = info
        ok = g2 == r["gold"]
        tab[_tab_key(r)]["rows"] += 1
        tab[_tab_key(r)]["agree"] += int(ok)
        if not ok:
            dis.append({"rid": r["rid"], "gold": r["gold"], "decide2": g2, "error": err, "tpl": r["meta"]["tpl"],
                        "view": r["meta"]["view"], "fmt": r["meta"]["fmt"], "renderer": r["meta"]["renderer"],
                        "info": {k: v for k, v in (info or {}).items() if k != "trace"}})
    n = len(rows)
    agree = n - len(dis)
    return {"rows": n, "agree": agree, "rate": round(agree / max(1, n), 6),
            "table": {k: dict(v) for k, v in sorted(tab.items())}, "disagreements": dis, "answers": answers,
            "infos": infos}


def structure_under_decide2(rows: list[dict], rels: list[dict], answers: dict) -> dict:
    """SPEC 8.3 under decide2 alone: contrast twins flip, equiv views keep, complement views invert, inv (attack)
    twins keep the answer; complement pairs are yes/no pairs."""
    by = {r["rid"]: r for r in rows}
    out = {"contrast_pairs": 0, "contrast_not_flipped": [], "equiv": 0, "equiv_changed": [], "complement": 0,
           "complement_bad": [], "inv": 0, "inv_changed": [], "unknown_rel": []}
    for r in rows:
        tw = r["meta"].get("twin_of")
        if r["meta"]["view"] == "contrast" and tw and tw in by:
            out["contrast_pairs"] += 1
            a, b = answers.get(r["rid"]), answers.get(tw)
            same_q = r["instructions"] == by[tw]["instructions"] and r["options"] == by[tw]["options"]
            if a is None or b is None or (same_q and a == b):
                out["contrast_not_flipped"].append(r["rid"])
    for rel in rels:
        a, b, t = rel["a"], rel["b"], rel["type"]
        A, B = answers.get(a), answers.get(b)
        if t == "equiv":
            out["equiv"] += 1
            if A is None or A != B:
                out["equiv_changed"].append((a, b))
        elif t == "complement":
            out["complement"] += 1
            if A is None or B is None or {A, B} != {"yes", "no"}:
                out["complement_bad"].append((a, b))
        elif t == "inv":
            out["inv"] += 1
            if A is None or A != B:
                out["inv_changed"].append((a, b))
        else:
            out["unknown_rel"].append(rel)
    out["ok"] = not (out["contrast_not_flipped"] or out["equiv_changed"] or out["complement_bad"]
                     or out["inv_changed"] or out["unknown_rel"])
    return out


def sensitivity(rows: list[dict], base_answers: dict, probes: bool = True) -> dict:
    """For each alternative reading (and each ablation probe): the rows whose decide2 answer changes, and how many of
    them the program gold agrees with under the alternative (which reading the generator follows)."""
    out = {}
    for name, rd in {**ALT_READINGS, **(PROBES if probes else {})}.items():
        changed, follows = [], 0
        for r in rows:
            info, _ = _try(r, rd)
            a = info["gold2"] if info else None
            if a != base_answers.get(r["rid"]):
                changed.append(r["rid"])
                follows += int(a == r["gold"])
        out[name] = {"changed": len(changed), "gold_follows_alt": follows, "rids": changed}
    return out


def notes_report(rows: list[dict], infos: dict) -> dict:
    """Things decide2 noticed while reading (not failures): amendment chains whose 'old' figure is not the figure in
    force before them, documents with 0 or 2+ decisive clauses, rows with two refusal grounds, F1b rows whose card
    rules are needed but whose card style prints no card."""
    from collections import Counter
    c, ex = Counter(), {}
    for r in rows:
        info = infos.get(r["rid"])
        if not info:
            continue
        for n in info.get("notes", []):
            k = re.sub(r"[A-Z]?\d[\d.]*", "N", n)
            c[k] += 1
            ex.setdefault(k, []).append(r["rid"])
        if info.get("q", "").startswith("nb_") and r["meta"].get("card_style") == "none":
            card = nb_card(r)["rules"]
            for need in ("conv", "about"):
                if need in card:
                    c[f"F1b card rule '{need}' needed but card_style none"] += 1
                    ex.setdefault(f"F1b card rule '{need}' needed but card_style none", []).append(r["rid"])
    return {k: {"rows": v, "examples": ex[k][:8]} for k, v in sorted(c.items())}


_CARD_YES = {
    "pos": "Applying every clause of the {doc} that bears on the case (requirements, exceptions, exclusions, "
           "amendments in force, limits and the precedence rule) gives exactly the outcome named in the question.",
    "inv": "Applying every clause of the {doc} that bears on the case (requirements, exceptions, exclusions, "
           "amendments in force, limits and the precedence rule) gives an outcome other than the one named in the "
           "question.",
    "jdg": "The decision recorded in the case file is the outcome that the {doc} gives when every clause that bears "
           "on the case is applied.",
    "jinv": "The {doc}, applied in full, gives an outcome other than the decision recorded in the case file.",
    ("nb_claim", True): "Under these rules the evidence establishes the claim.",
    ("nb_claim", False): "Under these rules the evidence does not establish the claim.",
    ("nb_log", True): "The fact-check log entry matches what the evidence establishes under these rules.",
    ("nb_log", False): "The fact-check log entry does not match what the evidence establishes under these rules.",
}


def card_report(rows: list[dict], infos: dict) -> dict:
    """yes/no rows: the card file (meta.defs) must say that 'yes' answers the question decide2 read (the same
    proposition and the same polarity). Rows whose card is not printed (card_style none) are checked too."""
    bad, n = [], 0
    for r in rows:
        info = infos.get(r["rid"])
        if not info or r["meta"]["qkind"] != "yn":
            continue
        qid = r["meta"].get("defs")
        p = DEFS / f"{KEY}__{qid}.json"
        if not qid or not p.exists():
            bad.append(r["rid"])
            continue
        yes = json.loads(p.read_text()).get("yes")
        if info["q"].startswith("nb_"):
            want = _CARD_YES[(info["q"], NB_QUESTIONS[r["instructions"]][1])]
        else:
            d = vocab(info["skin"]).doc
            want = _CARD_YES[info["q"]].format(doc=d, Doc=cap(d))
        n += 1
        if yes != want:
            bad.append(r["rid"])
    return {"yn_rows_checked": n, "card_question_mismatch": bad}


def meta_crosscheck(rows: list[dict], infos: dict) -> dict:
    """decide2 read the family and style from the text; compare with meta.pack / meta.renderer (report only)."""
    bad = []
    for r in rows:
        info = infos.get(r["rid"])
        if not info or "skin" not in info:
            continue
        m = r["meta"]
        style = {"code": "code", "contract": "code", "handbook": "handbook", "faq": "faq", "table": "table"}
        if m["pack"] != "a_" + info["skin"] or style.get(m["renderer"]) != info["style"]:
            bad.append(r["rid"])
        fmt = m["fmt"].split(":")[0] if m["fmt"].startswith("log") else m["fmt"]
        if fmt != info["fmt"]:
            bad.append(r["rid"])
    return {"mismatch": sorted(set(bad))}


DIAGNOSES = {}


def diagnose(row: dict) -> dict:
    """For a disagreement: which named reading (if any) reproduces the gold."""
    hits = []
    for name, rd in ALT_READINGS.items():
        info, _ = _try(row, rd)
        if info and info["gold2"] == row["gold"]:
            hits.append(name)
    if hits:
        return {"reading": hits, "class": "ambiguous_item", "why": "the gold follows another reading"}
    return {"reading": [], "class": "unexplained (trace by hand)", "why": ""}


def full_report(splits=("train", "dev"), probes: bool = True) -> dict:
    rep = {}
    for split in splits:
        rows, rels = load_rows(split), load_rels(split)
        ag = agreement(rows)
        by = {r["rid"]: r for r in rows}
        for d in ag["disagreements"]:
            d["diagnosis"] = diagnose(by[d["rid"]])
        rep[split] = {"agreement": {k: v for k, v in ag.items() if k not in ("answers", "infos")},
                      "structure": structure_under_decide2(rows, rels, ag["answers"]),
                      "sensitivity": sensitivity(rows, ag["answers"], probes),
                      "notes": notes_report(rows, ag["infos"]),
                      "cards": card_report(rows, ag["infos"]),
                      "meta_crosscheck": meta_crosscheck(rows, ag["infos"])}
    return rep


def _rel(p: Path) -> str:
    p = Path(p).resolve()
    return str(p.relative_to(LEAN)) if p.is_relative_to(LEAN) else str(p)


def write_agreement(out_path: Path | None = None, manifest: bool = True, probes: bool = True) -> dict:
    """Writes yn2b/v3_rule_chain_agreement.json (the SPEC 8.1 record for F1) and appends its sha256 to
    golden_src/gen3/MANIFEST_yn2b.jsonl. Reads the raw rows only; writes nothing under data/."""
    import hashlib
    out_path = Path(out_path or LEAN / "yn2b" / "v3_rule_chain_agreement.json")
    rep = {"tool": "golden_src/gen3/v3_rule_chain.py", "key": KEY,
           "author": "builder E (independent of decide; read only F1_RULE_CHAIN_FORMAT.md, rc_skins vocabulary and "
                     "the rendered rows)",
           "readings": DEFAULT_READINGS, "inputs": {}, "parts": {}}
    full = full_report(probes=probes)
    for split in ("train", "dev"):
        p = RAW / (f"{KEY}.jsonl" if split == "train" else f"dev/{KEY}.jsonl")
        rep["inputs"][split] = {"path": str(p.relative_to(LEAN)), "rows": full[split]["agreement"]["rows"],
                                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        ag = full[split]["agreement"]
        rep["parts"][split] = {"rows": ag["rows"], "agree": ag["agree"], "disagree": ag["rows"] - ag["agree"],
                               "rate": ag["rate"], "by_part_kind_qkind_view": ag["table"],
                               "disagreements": ag["disagreements"], "structure": full[split]["structure"],
                               "sensitivity": full[split]["sensitivity"], "notes": full[split]["notes"],
                               "cards": full[split]["cards"],
                               "meta_crosscheck": full[split]["meta_crosscheck"]}
    text = json.dumps(rep, indent=1, ensure_ascii=False, default=str) + "\n"
    out_path.write_text(text)
    if manifest:
        sys.path.insert(0, str(LEAN / "yn2b"))
        import yn2b_common as yc
        yc.manifest_append({"tool": "golden_src/gen3/v3_rule_chain.py", "key": KEY, "part": "decide2_agreement",
                            "path": _rel(out_path), "rows": sum(v["rows"] for v in rep["parts"].values()),
                            "sha256": hashlib.sha256(text.encode()).hexdigest(), "inputs": rep["inputs"],
                            "agree": {k: [v["agree"], v["rows"]] for k, v in rep["parts"].items()}})
    return rep


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", help="write the full report here (scratch path; never under data/)")
    ap.add_argument("--quick", action="store_true", help="agreement only")
    ap.add_argument("--write", action="store_true",
                    help="write yn2b/v3_rule_chain_agreement.json and append its sha256 to MANIFEST_yn2b.jsonl")
    a = ap.parse_args(argv)
    if a.write:
        rep = write_agreement()
        for k, v in rep["parts"].items():
            print(f"{k}: {v['agree']}/{v['rows']} agree; disagreements {[d['rid'] for d in v['disagreements']]}")
        return rep
    rep = {}
    for split in ("train", "dev"):
        rows = load_rows(split)
        ag = agreement(rows)
        rep[split] = {"agreement": {k: v for k, v in ag.items() if k not in ("answers", "infos")}}
        print(f"== {split}: {ag['agree']}/{ag['rows']} agree ({100 * ag['rate']:.2f}%)")
        for k, v in ag["table"].items():
            print(f"  {k:34s} {v.get('agree', 0):5d}/{v['rows']:5d}")
        for d in ag["disagreements"][:40]:
            print("  DIS", d["rid"], d["tpl"], d["fmt"], "gold", repr(d["gold"])[:50], "d2", repr(d["decide2"])[:50],
                  d["error"])
        if a.quick:
            continue
        rels = load_rels(split)
        st = structure_under_decide2(rows, rels, ag["answers"])
        rep[split]["structure"] = st
        print(f"  structure: contrast {st['contrast_pairs']} (not flipped {len(st['contrast_not_flipped'])}), "
              f"equiv {st['equiv']} (changed {len(st['equiv_changed'])}), complement {st['complement']} "
              f"(bad {len(st['complement_bad'])}), inv {st['inv']} (changed {len(st['inv_changed'])})")
        se = sensitivity(rows, ag["answers"])
        rep[split]["sensitivity"] = se
        for name, v in se.items():
            print(f"  reading {name:32s} changes {v['changed']:4d} rows; gold follows it on {v['gold_follows_alt']}"
                  + (f"  {v['rids'][:8]}" if v["changed"] else ""))
        nr = notes_report(rows, ag["infos"])
        rep[split]["notes"] = nr
        for k, v in nr.items():
            print(f"  note: {k}: {v['rows']} rows {v['examples'][:4]}")
        cr = card_report(rows, ag["infos"])
        rep[split]["cards"] = cr
        print(f"  cards: {cr['yn_rows_checked']} yes/no rows checked; card/question mismatches "
              f"{cr['card_question_mismatch'][:8]}")
        mc = meta_crosscheck(rows, ag["infos"])
        rep[split]["meta_crosscheck"] = mc
        print(f"  family/style/format read from the text vs meta: {len(mc['mismatch'])} mismatches")
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1, default=str))
    return rep


if __name__ == "__main__":
    main()
