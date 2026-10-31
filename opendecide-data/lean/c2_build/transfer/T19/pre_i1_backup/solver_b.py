"""transfer/T19/solver_b.py: T19 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the card by full-text comparison with this module's own copy;
  - the site profile (list, table or export layout), the checklist lines, the evidence log and the audit date by
    this module's own regular expressions; profile and scope values map to keys through this module's own surface
    table; dates and day counts through slots.parse;
  - the narrative skin (Mode T) through skin.parse_skin, the question through its wording template;
  - on choice rows, every option text back to its key.
A printed last valid day must equal the evidence date + N days (sqlite's own date arithmetic), and every evidence
date must be before the audit date (G0 S4); otherwise ParseError, which fails G2 and drops the unit.
solve_b(view) loads the view into an in-memory sqlite database (profile, control, scope tables) and decides by SQL:
one query gives every control's status (scope by EXISTS joins, the exclusion by EXISTS, validity by
date(ev, '+N days') >= audit), aggregates give the verdict, ORDER BY ord gives the first gap. Imports no solver-A code.
"""
from __future__ import annotations

import re
import sqlite3

from c2_kit import skin as K
from c2_kit import slots as S

CLOSED = "The profile, the checklist and the evidence log are complete: nothing else changes the answer."
CARD = ("How to read this checklist:\n"
        "- A control applies to the site when the site's profile shows one of the control's listed values for the "
        "named attribute, unless the profile shows the control's excluded value. A control for every site applies "
        "whatever the profile shows, unless the profile shows its excluded value. Each profile attribute has exactly "
        "one value.\n"
        "- Evidence dated D that stays valid for N days covers each calendar date from D through D + N days: on day "
        "D + N it still counts, and from the next day on it has expired. Every evidence date in these records is "
        "earlier than the audit date.\n"
        "- An applying control passes when its evidence covers the audit date. It fails when that evidence has "
        "expired by the audit date or no evidence is on file. If its evidence date is not recorded, its result is "
        "unknown.\n"
        "- The site is compliant on the audit date when every applying control passes, and non-compliant when at "
        "least one applying control fails. When no applying control fails but some applying control's result is "
        "unknown, compliance cannot be determined.\n"
        "- Controls are checked in the listed order: the first gap is the first applying control that fails.\n"
        + CLOSED)
SURFACE = {"hosting": {"cloud": "cloud", "on-premises": "onprem", "hybrid": "hybrid"},
           "data": {"public": "public", "internal": "internal", "personal data": "personal",
                    "payment data": "payment"},
           "stype": {"office": "office", "warehouse": "warehouse", "data centre": "datacentre", "store": "store"}}
LABEL = {"hosting": "hosting", "data handled": "data", "site type": "stype"}
DAYS = (("unit", ("day", "days")),)
OPTION = {"Compliant": "compliant", "Non-compliant": "noncompliant",
          "Cannot be determined from the records": "undetermined"}
ANSWER = {"yn_compliant": {"compliant": 1, "noncompliant": 0}, "yn_out_of": {"compliant": 0, "noncompliant": 1},
          "yn_not_compliant": {"compliant": 0, "noncompliant": 1}, "yn_fails": {"compliant": 0, "noncompliant": 1}}
SCHEMA = {"SITE": ("name", ()), "AUDITOR": ("name", ())}
_ATTR = r"(?:hosting|data handled|site type)"
PROFILE_RES = (
    re.compile(r"Site profile for (?P<site>[^\n]+):\n- hosting: (?P<h>[^\n]+)\n- data handled: (?P<d>[^\n]+)\n"
               r"- site type: (?P<t>[^\n]+)"),
    re.compile(r"Site profile for (?P<site>[^\n]+):\n\| attribute \| value \|\n\|---\|---\|\n"
               r"\| hosting \| (?P<h>[^|\n]+) \|\n\| data handled \| (?P<d>[^|\n]+) \|\n"
               r"\| site type \| (?P<t>[^|\n]+) \|"),
    re.compile(r"export site_profile:\n  site: (?P<site>[^\n]+)\n  hosting: (?P<h>[^\n]+)\n  data handled: "
               r"(?P<d>[^\n]+)\n  site type: (?P<t>[^\n]+)"),
)
CONTROL_RE = re.compile(rf"- (?P<cid>\S+) (?P<name>[^:\n]+): (?:applies to every site|applies to sites whose "
                        rf"(?P<attr>{_ATTR}) is (?P<vals>[^,;\n]+?))(?:, except sites whose (?P<xattr>{_ATTR}) is "
                        rf"(?P<xval>[^;\n]+))?; its evidence stays valid for (?P<n>[^\n]+?) after the evidence date\.")
EVIDENCE_RE = re.compile(r"- (?P<cid>\S+): (?:(?P<none>no evidence on file)|(?P<unk>evidence on file, date not "
                         r"recorded)|evidence dated (?P<ev>.+?)(?: \(last valid day (?P<t>.+?)\))?)")
STATUS_SQL = """
SELECT c.cid, c.ord,
  CASE
    WHEN NOT (c.attr = 'all' OR EXISTS (SELECT 1 FROM scope s JOIN profile p ON p.attr = c.attr AND p.val = s.val
                                        WHERE s.cid = c.cid))
      OR EXISTS (SELECT 1 FROM profile p WHERE c.xattr IS NOT NULL AND p.attr = c.xattr AND p.val = c.xval)
      THEN 'na'
    WHEN c.evidence = 'none' THEN 'fail'
    WHEN c.evidence = 'unknown' THEN 'unknown'
    WHEN date(c.ev, '+' || c.days || ' days') >= :audit THEN 'pass'
    ELSE 'fail'
  END AS status
FROM control c ORDER BY c.ord
"""


class ParseError(ValueError):
    pass


def _key(attr: str, surface: str) -> str:
    if surface not in SURFACE[attr]:
        raise ParseError(f"{surface!r} is not a {attr} value")
    return SURFACE[attr][surface]


def _block(state: str, head: str, nxt: str) -> list:
    m = re.search(re.escape(head) + r"\n(?P<body>.*?)(?=" + re.escape(nxt) + ")", state, re.S)
    if not m:
        raise ParseError(f"no {head!r} block")
    return [x for x in m["body"].split("\n") if x]


def parse(row: dict, ctx) -> dict:
    card, sep, question = row["instructions"].partition("\n\n")
    if not sep or card != CARD:
        raise ParseError("the card is not the G0 card")
    state = row["state"]
    narrative, sep, rest = state.partition("\n\n")
    if not sep:
        raise ParseError("no blank line after the narrative")
    pm = None
    for rx in PROFILE_RES:
        pm = rx.match(rest)
        if pm:
            break
    if pm is None:
        raise ParseError("no site profile block")
    profile = {"hosting": _key("hosting", pm["h"]), "data": _key("data", pm["d"]), "stype": _key("stype", pm["t"])}
    site = S.parse("name", pm["site"])
    controls = []
    for line in _block(state, "\nChecklist:", "\n\nEvidence log:"):
        m = CONTROL_RE.fullmatch(line)
        if not m:
            raise ParseError(f"checklist line {line!r}")
        attr = LABEL[m["attr"]] if m["attr"] else "all"
        vals = [_key(attr, v) for v in m["vals"].split(" or ")] if m["attr"] else []
        xattr = LABEL[m["xattr"]] if m["xattr"] else None
        controls.append({"id": S.parse("id", m["cid"]), "name": S.parse("name", m["name"]), "attr": attr,
                         "vals": vals, "xattr": xattr, "xval": _key(xattr, m["xval"]) if xattr else None,
                         "days": S.parse("count", m["n"], DAYS), "evidence": None, "date": None, "through": None})
    ev_lines = _block(state, "\nEvidence log:", "\n\nAudit date:")
    if len(ev_lines) != len(controls):
        raise ParseError("evidence log and checklist differ in length")
    for c, line in zip(controls, ev_lines):
        m = EVIDENCE_RE.fullmatch(line)
        if not m or m["cid"] != c["id"]:
            raise ParseError(f"evidence line {line!r} does not follow the checklist order")
        if m["none"]:
            c["evidence"] = "none"
        elif m["unk"]:
            c["evidence"] = "unknown"
        else:
            c["evidence"] = "date"
            c["date"] = S.parse("date", m["ev"]).isoformat()
            if m["t"]:
                c["through"] = S.parse("date", m["t"]).isoformat()
    am = list(re.finditer(r"\n\nAudit date: (?P<a>[^\n]+)", state))
    if len(am) != 1:
        raise ParseError("need exactly one audit date")
    audit = S.parse("date", am[0]["a"]).isoformat()
    for c in controls:                          # G0 S4: the card says every evidence date is before the audit date
        if c["date"] is not None and not c["date"] < audit:
            raise ParseError(f"{c['id']}: evidence dated {c['date']}, not before the audit date {audit}")
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = K.parse_skin(skin, narrative, SCHEMA) if skin.author_mode == "T" else {}
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, SCHEMA)
    for k, v in list(told.items()) + list(asked.items()):
        if k == "SITE" and v != site:
            raise ParseError("the narrative names another site")
    view = {"site": site, "audit": audit, "profile": profile, "controls": controls, "qform": wording.qform}
    if skin.author_mode == "T":
        view["auditor"] = told["AUDITOR"]
    if row["qtype"] == "choice":
        view["options"] = [OPTION.get(t, t) for t in row["options"]]
    return view


def _db(view: dict):
    con = sqlite3.connect(":memory:")
    con.executescript("CREATE TABLE profile(attr TEXT PRIMARY KEY, val TEXT);"
                      "CREATE TABLE control(cid TEXT PRIMARY KEY, ord INTEGER, attr TEXT, xattr TEXT, xval TEXT, "
                      "days INTEGER, evidence TEXT, ev TEXT);"
                      "CREATE TABLE scope(cid TEXT, val TEXT);")
    con.executemany("INSERT INTO profile VALUES (?, ?)", sorted(view["profile"].items()))
    for i, c in enumerate(view["controls"]):
        con.execute("INSERT INTO control VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (c["id"], i, c["attr"], c["xattr"], c["xval"], c["days"], c["evidence"], c["date"]))
        con.executemany("INSERT INTO scope VALUES (?, ?)", [(c["id"], v) for v in c["vals"]])
        if c["through"] is not None:
            got = con.execute("SELECT date(?, '+' || ? || ' days')", (c["date"], c["days"])).fetchone()[0]
            if got != c["through"]:
                raise ParseError(f"{c['id']}: printed last valid day {c['through']} != {got}")
    return con


def solve_b(view: dict):
    con = _db(view)
    con.execute("CREATE TEMP TABLE st AS " + STATUS_SQL.replace(":audit", "'" + view["audit"] + "'"))
    fails, unknown = con.execute("SELECT COALESCE(SUM(status = 'fail'), 0), COALESCE(SUM(status = 'unknown'), 0) "
                                 "FROM st").fetchone()
    verdict = "noncompliant" if fails else ("undetermined" if unknown else "compliant")
    q = view["qform"]
    if q == "ch_verdict":
        return verdict
    if q == "ch_gap":
        first = con.execute("SELECT cid, ord FROM st WHERE status = 'fail' ORDER BY ord LIMIT 1").fetchone()
        if first is None:
            raise ParseError("ch_gap without a failing control")
        before = con.execute("SELECT COUNT(*) FROM st WHERE status = 'unknown' AND ord < ?", (first[1],)).fetchone()[0]
        if before:
            raise ParseError("ch_gap with an unknown result before the first failure")
        return first[0]
    if verdict == "undetermined":
        raise ParseError("a yes/no row whose answer cannot be determined")
    return ANSWER[q][verdict]
