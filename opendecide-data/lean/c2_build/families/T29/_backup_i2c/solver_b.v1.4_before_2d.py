"""c2_build/families/T29/solver_b.py: T29 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts (G0 S13-S16):
  - the policy card (row.card on yes/no rows, the head of the instructions on choice rows: cards.split_rules) line by
    line with this module's own regular expressions; comparator, precedence and confirmation clauses through the
    lexicon registry (admitted forms only: G-LEX vouches for each form's meaning);
  - the state blocks (split on blank lines, classified by their headers): the call block, the snapshot in any of its
    four formats (key-value, table, console, JSON), the conversation line; the Mode T narrative through
    skin.parse_skin (Mode F narrative facts are left to G3-H); a trailing pressure line carries no fact;
  - the question through its wording template; on choice rows every option text back to its key.
Every fact printed twice must read the same, and the printed intermediates (local request time, minutes since the
edit) are re-derived here by integer epoch-minute arithmetic (brute.epoch_minutes) and checked against the text.
solve_b(view) loads the atoms and the facts into an in-memory sqlite database and decides with SQL: one query per
completion of the missing fields (G0 S28 witnesses: each threshold -1 / 0 / +1 and the domain floor; for
comparisons with a stated value, that value and one other), precedence by SQL (refuse > ask > go), and CANNOT DECIDE
when the completions disagree. Its own answer table maps the verdict to each question form (G0 S17-S21).
Imports no solver-A code (plugin.check_independence); nothing is written to disk (":memory:" only).
"""
from __future__ import annotations

import datetime as dt
import itertools
import json
import re
import sqlite3

from c2_kit import brute, cards
from c2_kit import skin as K
from c2_kit import slots as S

# ------------------------------------------------------------------------------------------------ G0 closed sets
TEAM_KEY = {"Finance": "finance", "Legal": "legal", "Platform": "platform", "Research": "research", "Sales": "sales",
            "Support": "support"}
ENV_KEY = {"production": "production", "staging": "staging", "development": "development", "sandbox": "sandbox"}
CLASS_KEY = {"personal": "personal", "internal": "internal", "public": "public"}
EFFECT_KEY = {"deletes data": "delete", "changes data": "change", "creates data": "create", "sends messages": "send",
              "pays money out": "pay", "exports data": "export", "changes access rights": "grant"}
REASON_SCHEMA = ("category", (("surfaces", (("audit", ("audit preparation",)), ("cleanup", ("quarterly cleanup",)),
                                            ("close", ("month-end close",)), ("incident", ("incident follow-up",)),
                                            ("migration", ("customer migration",)),
                                            ("onboarding", ("vendor onboarding",)))),))
RECORDS = (("unit", ("record", "records")),)
HOURS = (("unit", ("hour", "hours")),)
MINUTES = (("unit", ("minute", "minutes")),)
CENTS = (("currency", "USD"), ("symbol", "$"))
NARRATIVE_SCHEMA = {"REQUESTER": ("name", ()), "REASON": REASON_SCHEMA, "ACTION": ("id", ()), "TARGET": ("id", ())}
WORDING_SCHEMA = {"ACTION": ("id", ()), "TARGET": ("id", ())}
CONF_SCHEMA = {"ACT": ("id", ()), "TGT": ("id", ())}
PREC_SEM = "prec.t29.forbid_confirm_default"
CONF_SEMS = ("conf.t29.explicit", "conf.t29.mention")
TIER_KEY = {"forbidden": "forbid", "needs confirmation": "confirm"}
CMP_ALLOWED = {"bulk": ("cmp.gt", "cmp.ge"), "pay": ("cmp.gt", "cmp.ge"), "undo": ("cmp.lt", "cmp.le"),
               "recent": ("cmp.lt", "cmp.le")}
CMP_SCHEMA = {"bulk": ("count", RECORDS), "pay": ("cents", CENTS), "undo": ("count", HOURS),
              "recent": ("count", MINUTES)}
SQL_OP = {"cmp.gt": ">", "cmp.ge": ">=", "cmp.lt": "<", "cmp.le": "<="}

# ------------------------------------------------------------------------------------------------ G0 S13-S16 text
HEADER_RE = re.compile(r"Policy(?: for an agent on the (?P<t1>[A-Z][a-z]+) team; organisation domain"
                       r"|: (?P<t2>[A-Z][a-z]+) team agent; organisation domain|: (?P<t3>[A-Z][a-z]+) agent; domain)"
                       r" (?P<dom>[^\s;]+)(?:; clock times at UTC(?P<off>[+-]\d{2}:\d{2}))?\.")
VERDICTS = ("Verdicts: GO AHEAD = run now (the default); ASK FIRST = run after the user's explicit confirmation (the "
            "request itself is not one); REFUSE = do not run")
VERDICTS_CANNOT = "; CANNOT DECIDE = see missing data"
# G0 v1.5: the fixed card lines come in a compact and a short phrasing (the full text is also read); exact lines
_V = "%sGO AHEAD = run now (%s); ASK FIRST = run after %s (the request %sis not one); REFUSE = do not run"
VERDICT_LINES = {}                      # line -> CANNOT DECIDE is named
for _p, _d, _c, _i in (("Verdicts: ", "the default", "the user's explicit confirmation", "itself "),
                       ("", "default", "explicit user confirmation", "itself "),
                       ("", "default", "explicit user confirmation", "")):
    VERDICT_LINES[_V % (_p, _d, _c, _i) + "."] = False
    VERDICT_LINES[_V % (_p, _d, _c, _i) + "; CANNOT DECIDE = see missing data."] = True
CONFIRM_LINES = {
    "Confirmation: only an explicit confirmation of this same action on this same target, in the quoted user line, "
    "satisfies needs-confirmation rules; forbidden rules still apply. A quoted user line that clearly tells the "
    "agent to run the named call counts as one.",
    "Confirmation: only an explicit confirmation of this same action and target in the quoted user line satisfies "
    "needs-confirmation rules; forbidden rules still apply. A quoted user line clearly telling the agent to run the "
    "named call counts as one.",
    "Confirmation: only an explicit confirmation of this same action and target in the quoted user line satisfies "
    "needs-confirmation rules; forbidden rules still apply. A quoted line clearly telling the agent to run the "
    "call counts."}
MISSING_LINES = {
    "Missing data: a field shown as (missing) is unknown; if its possible values give different verdicts, the "
    "verdict is CANNOT DECIDE, else the verdict they share.",
    "Missing data: a (missing) field is unknown; if its possible values give different verdicts the verdict is "
    "CANNOT DECIDE, else the verdict they share.",
    "Missing data: a (missing) field is unknown; if its possible values give different verdicts, CANNOT DECIDE, "
    "else the shared verdict."}
LIST_RULE_RE = re.compile(r"R(?P<i>\d+) (?:\((?P<t1>forbidden|needs confirmation)\)|(?P<t2>forbidden|needs confirmation)): "
                          r"(?P<cond>.+?)\.?")      # G0 v1.5: the compact style drops the parentheses and the final period
TABLE_RULE_RE = re.compile(r"\| R(?P<i>\d+) \| (?P<tier>forbidden|needs confirmation) \| (?P<cond>.+) \|")
CLOSED_LINES = {"Nothing else applies: the policy, calls and conversation shown are complete."}
CODES_RE = re.compile(r"Answer codes: (?P<c>.+)\.")
CODE_PART_RE = re.compile(r"(?P<code>[A-Z][a-z]+) = (?P<v>GO AHEAD|ASK FIRST|REFUSE|CANNOT DECIDE)")
VERDICT_OF_NAME = {"GO AHEAD": "go", "ASK FIRST": "ask", "REFUSE": "refuse", "CANNOT DECIDE": "cannot"}
ATOM_RES = (
    ("bulk", re.compile(r"the call affects (?P<c>.+)")),
    ("pay", re.compile(r"the amount paid out is (?P<c>.+)")),
    ("undo", re.compile(r"the undo window is (?P<c>.+)")),
    ("recent", re.compile(r"a person last edited the target record (?P<c>.+) before the request time")),
    ("external", re.compile(r"the destination domain is not (?P<d>\S+)")),
    ("other_team", re.compile(r"the record owner team is not (?P<t>[A-Z][a-z]+)")),
    ("prod", re.compile(r"the environment is production")),
    ("pii", re.compile(r"the data class is personal")),
    ("delete", re.compile(r"the effect is deletes data")),
    ("export", re.compile(r"the effect is exports data")),
    ("grant", re.compile(r"the effect is changes access rights")),
    ("off_hours", re.compile(r"the request time at UTC(?P<o>[+-]\d{2}:\d{2}) is before (?P<s>\d{2}:\d{2}) or "
                             r"(?:at (?P<e1>\d{2}:\d{2}) or later|after (?P<e2>\d{2}:\d{2}))")),
)
CALL_RE = re.compile(r"Proposed call: (?P<a>\S+) on (?P<t>\S+)\nCatalog entry: effect (?P<e>[a-z ]+)"
                     r"(?:; undo window (?P<u>[^\n]+))?\.")
CONV_RE = re.compile(r'Earlier in this conversation the user wrote: "(?P<c>[^\n]+)"')
LABEL_KEY = {"records": "records_affected", "amount paid out": "amount_paid_out",
             "destination": "destination_domain", "owner team": "record_owner_team",
             "environment": "environment", "data class": "data_class", "request time": "request_time",
             "last edit": "last_human_edit", "minutes since edit": "minutes_since_edit"}
_LABELS = r"request time at UTC[+-]\d{2}:\d{2}|" + "|".join(sorted(map(re.escape, LABEL_KEY), key=len, reverse=True))
KV_RE = re.compile(rf"- (?P<l>{_LABELS}): (?P<v>.+)")
TABLE_RE = re.compile(rf"\| (?P<l>{_LABELS}) \| (?P<v>.+) \|")
CONSOLE_RE = re.compile(rf"(?P<l>{_LABELS}) = (?P<v>.+)")
INPUT_KEYS = ("records_affected", "amount_paid_out", "destination_domain", "record_owner_team", "environment",
              "data_class", "request_time", "last_human_edit")
PRINTED_KEYS = ("request_time_local", "minutes_since_edit")
OPTION_KEY = {"Go ahead right now": "go", "Ask the user first": "ask", "Refuse it outright": "refuse",
              "Cannot decide here": "cannot"}                # G0 v1.2 S12: four labels of 18 characters
NONE_OPTION = "No rule applies (default)"
YES_SET = {"yn_go": {"go"}, "yn_go_dneg": {"go"}, "yn_not_go": {"ask", "refuse"},
           "yn_go_framed": {"ask", "refuse"}, "yn_ask": {"ask"},
           "yn_ask_framed": {"go", "refuse"}, "yn_refuse": {"refuse"}, "yn_permitted": {"go", "ask"},
           "yn_not_forbidden": {"go", "ask"}}


class ParseError(ValueError):
    pass


def _minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def _offset_minutes(text: str) -> int:
    sign = -1 if text[0] == "-" else 1
    h, m = text[1:].split(":")
    return sign * (int(h) * 60 + int(m))


def _clock_offset(t: dt.datetime) -> int:
    off = t.utcoffset()
    return off.days * 1440 + off.seconds // 60


# ------------------------------------------------------------------------------------------------ parse: card
def _atom(text: str, ctx, header: dict):
    """One atom dict from one condition text, or None when the text is not exactly one atom."""
    for kind, rx in ATOM_RES:
        m = rx.fullmatch(text)
        if not m:
            continue
        if kind in CMP_ALLOWED:
            try:
                sem, _fid, vals = ctx.lexicon.parse_exact(m["c"], {"X": CMP_SCHEMA[kind]}, admitted_only=True)
            except ValueError:
                return None
            if sem not in CMP_ALLOWED[kind]:
                raise ParseError(f"{kind} with comparator {sem}")
            return {"type": kind, "cmp": sem, "value": vals["X"]}
        if kind == "external":
            if m["d"] != header["org_domain"]:
                raise ParseError("the external rule names another organisation domain")
            return {"type": kind}
        if kind == "other_team":
            if TEAM_KEY.get(m["t"]) != header["agent_team"]:
                raise ParseError("the owner rule names another team than the header")
            return {"type": kind}
        if kind == "off_hours":
            if m["o"] != header["offset"]:
                raise ParseError("the off-hours rule names another offset than the header")
            incl = m["e2"] is not None
            return {"type": kind, "start": _minutes(m["s"]), "end": _minutes(m["e2"] if incl else m["e1"]),
                    "end_incl": incl}
        return {"type": kind}
    return None


def _condition(cond: str, ctx, header: dict) -> list:
    one = _atom(cond, ctx, header)
    reads = [[one]] if one is not None else []
    for m in re.finditer(r" and ", cond):
        a, b = _atom(cond[:m.start()], ctx, header), _atom(cond[m.end():], ctx, header)
        if a is not None and b is not None:
            reads.append([a, b])
    if len(reads) != 1:
        raise ParseError(f"condition reads {len(reads)} ways: {cond!r}")
    return reads[0]


def _card(card: str, ctx) -> dict:
    lines = card.split("\n")
    m = HEADER_RE.fullmatch(lines[0])
    team = m and (m["t1"] or m["t2"] or m["t3"])
    if not m or team not in TEAM_KEY:
        raise ParseError("policy header")
    out = {"agent_team": TEAM_KEY[team], "org_domain": S.parse("id", m["dom"]), "offset": m["off"]}
    if lines[1] not in VERDICT_LINES or lines[2] != "Rules:":
        raise ParseError("verdict line or rules heading")
    out["_cannot_named"] = VERDICT_LINES[lines[1]]
    k = 3
    table = lines[k] == "| rule | tier | applies when |"
    if table:
        if lines[k + 1] != "|---|---|---|":
            raise ParseError("rule table separator")
        k += 2
    rules = []
    while not lines[k].startswith("Precedence: "):
        rm = (TABLE_RULE_RE if table else LIST_RULE_RE).fullmatch(lines[k])
        if not rm or int(rm["i"]) != len(rules) + 1:
            raise ParseError(f"rule line {lines[k]!r}")
        gd = rm.groupdict()
        rules.append({"rid": f"R{rm['i']}", "tier": TIER_KEY[gd.get("tier") or gd.get("t1") or gd.get("t2")],
                      "atoms": _condition(rm["cond"], ctx, out)})
        k += 1
    if not 3 <= len(rules) <= 6:
        raise ParseError(f"{len(rules)} rules")
    sem, _fid, _ = ctx.lexicon.parse_exact(lines[k][len("Precedence: "):], {}, admitted_only=True)
    if sem != PREC_SEM:
        raise ParseError(f"precedence clause reads {sem}")
    out.update(rules=rules, precedence=sem)
    k += 1
    out["_confirm_line"] = lines[k] in CONFIRM_LINES
    k += int(out["_confirm_line"])
    out["_missing_line"] = lines[k] in MISSING_LINES
    k += int(out["_missing_line"])
    if out["_missing_line"] != out["_cannot_named"]:
        raise ParseError("CANNOT DECIDE is named in the verdict line iff the missing-data line is printed")
    codes = None
    cm = CODES_RE.fullmatch(lines[k])
    if cm:
        codes = {}
        for part in cm["c"].split(", "):
            pm = CODE_PART_RE.fullmatch(part)
            if not pm or pm["code"] in codes:
                raise ParseError("answer codes")
            codes[pm["code"]] = VERDICT_OF_NAME[pm["v"]]
        if sorted(codes.values()) not in (sorted(("go", "ask", "refuse")), sorted(("go", "ask", "refuse", "cannot"))):
            raise ParseError("answer codes cover GO AHEAD, ASK FIRST and REFUSE once each (+ CANNOT DECIDE if offered)")
        k += 1
    if len(lines[k:]) != 1 or lines[k] not in CLOSED_LINES:
        raise ParseError("closed-world sentence")
    out["codes"] = codes
    return out


# ------------------------------------------------------------------------------------------------ parse: state
def _value(key: str, text):
    if text is None or text == "(missing)":
        return None
    text = str(text)
    if key == "records_affected":
        return S.parse("count", text, RECORDS)
    if key == "minutes_since_edit":
        return S.parse("count", text, MINUTES)
    if key == "amount_paid_out":
        return S.parse("cents", text, CENTS)
    if key == "destination_domain":
        return S.parse("id", text)
    if key == "record_owner_team":
        return TEAM_KEY[text]
    if key == "environment":
        return ENV_KEY[text]
    if key == "data_class":
        return CLASS_KEY[text]
    return S.parse("datetime", text).isoformat()          # request_time, request_time_local, last_human_edit


CALLS_HEAD = ("Proposed calls:", "Proposed calls: ", "admin-console> list proposed calls", "Proposed calls (JSON), columns ")
SAME = "same"          # the local-time cell of a candidate already at the policy's offset


def _calls_table(block: str) -> tuple:
    """G0 v1.5: ONE table of candidate actions (shared header, one line per candidate), in any of the four layouts.
    Returns (labels, [cells per candidate]); a JSON null is None."""
    lines = block.split("\n")
    h = lines[0]
    if h == "Proposed calls:":
        if len(lines) < 5 or not (lines[1].startswith("| ") and lines[1].endswith(" |")):
            raise ParseError("calls table header")
        labels = lines[1][2:-2].split(" | ")
        if lines[2] != "|" + "---|" * len(labels):
            raise ParseError("calls table separator")
        body = []
        for ln in lines[3:]:
            if not (ln.startswith("| ") and ln.endswith(" |")):
                raise ParseError(f"calls table line {ln!r}")
            body.append(ln[2:-2].split(" | "))
    elif h == "admin-console> list proposed calls":
        if not lines[1].startswith("# "):
            raise ParseError("console header")
        labels, body = lines[1][2:].split("; "), [ln.split("; ") for ln in lines[2:]]
    elif h.startswith("Proposed calls (JSON), columns ") and h.endswith(":"):
        labels = json.loads(h[len("Proposed calls (JSON), columns "):-1])
        body = [json.loads(ln) for ln in lines[1:]]
    elif h.startswith("Proposed calls: "):
        labels, body = h[len("Proposed calls: "):].split(" | "), [ln.split(" | ") for ln in lines[1:]]
    else:
        raise ParseError("calls header")
    if len(set(labels)) != len(labels) or labels[:2] != ["call", "effect"]:
        raise ParseError("calls columns")
    if any(len(r) != len(labels) for r in body):
        raise ParseError("a candidate line has another number of cells than the header")
    return labels, body


def _row_snapshot(labels: list, cells: list, offset) -> dict:
    out = {}
    for label, raw in zip(labels[2:], cells[2:]):
        if label == "undo window":
            continue
        if label.startswith("request time at UTC"):
            if label != f"request time at UTC{offset}":
                raise ParseError("local request time printed at another offset than the policy's")
            if raw == SAME:
                continue
            key = "request_time_local"
        elif label in LABEL_KEY:
            key = LABEL_KEY[label]
        else:
            raise ParseError(f"snapshot label {label!r}")
        if key in out or key not in INPUT_KEYS + PRINTED_KEYS:
            raise ParseError(f"snapshot key {key!r}")
        out[key] = _value(key, raw)
    return out


def _check_printed(snap: dict, offset, off_hours: bool) -> None:
    """G0 S4: the printed local time and minutes since the edit equal this module's own epoch-minute arithmetic."""
    if "request_time" not in snap:
        if "request_time_local" in snap or "last_human_edit" in snap or off_hours:
            raise ParseError("local time, edit time or an off-hours rule without the request time")
        return
    if snap["request_time"] is None:
        raise ParseError("request time is never missing (G0 S5)")
    now = dt.datetime.fromisoformat(snap["request_time"])
    if not off_hours:
        if "request_time_local" in snap:
            raise ParseError("a local request time is printed but no off-hours rule reads it")
    elif "request_time_local" in snap:
        pol = _offset_minutes(offset)
        loc = dt.datetime.fromisoformat(snap["request_time_local"])
        if _clock_offset(loc) != pol or brute.epoch_minutes(loc) != brute.epoch_minutes(now):
            raise ParseError("the printed local request time is not the request time at the policy offset")
        if _clock_offset(now) == pol:
            raise ParseError("a local line is printed although the offsets agree")
    elif _clock_offset(now) != _offset_minutes(offset):
        raise ParseError("the request time is at another offset and no local line is printed")
    if "last_human_edit" in snap:
        last = snap["last_human_edit"]
        mins = snap.get("minutes_since_edit", "absent")
        if last is None:
            if mins is not None:
                raise ParseError("minutes printed for a missing edit time")
        elif mins != brute.epoch_minutes(now) - brute.epoch_minutes(dt.datetime.fromisoformat(last)):
            raise ParseError("printed minutes since the edit disagree with the times")
    elif "minutes_since_edit" in snap:
        raise ParseError("minutes printed without the edit time")


def parse(row: dict, ctx) -> dict:
    card, question = cards.split_rules(row)      # G0 v1.2 S13: a yes/no row holds the policy in row.card
    if not card or not question:
        raise ParseError("policy and question are not separated")
    view = _card(card, ctx)
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, WORDING_SCHEMA)
    view["qform"] = wording.qform
    blocks = row["state"].split("\n\n")
    calls = [b for b in blocks if b.startswith(CALLS_HEAD)]
    convs = [b for b in blocks if b.startswith("Earlier in this conversation the user wrote: ")]
    rest = [b for b in blocks if b not in calls + convs]
    if len(calls) != 1 or len(convs) > 1 or not 1 <= len(rest) <= 2:
        raise ParseError("state blocks: one table of candidate calls, at most one conversation line, a narrative")
    # G0 v1.5: ONE table, one line per candidate (call, target, effect, [undo window], snapshot fields)
    reads = {a["type"] for r in view["rules"] for a in r["atoms"]}
    labels, body = _calls_table(calls[0])
    if not 3 <= len(body) <= 5:
        raise ParseError("three to five candidate calls")
    if ("off_hours" in reads) != (view["offset"] is not None) or ("undo" in reads) != ("undo window" in labels):
        raise ParseError("the clock (undo window) is printed iff an off-hours (undo) rule reads it")
    cands = []
    for cells in body:
        cm = dict(zip(labels, cells))
        if cm["effect"] not in EFFECT_KEY:
            raise ParseError("call line")
        undo_h = S.parse("count", cm["undo window"], HOURS) if "undo window" in labels else None
        snap = _row_snapshot(labels, cells, view["offset"])
        _check_printed(snap, view["offset"], "off_hours" in reads)
        call = re.fullmatch(r"(?P<a>\S+) on (?P<t>\S+)", cm["call"])
        if not call:
            raise ParseError(f"call cell {cm['call']!r}")
        cands.append({"action": S.parse("id", call["a"]), "target": S.parse("id", call["t"]),
                      "effect": EFFECT_KEY[cm["effect"]], "undo_h": undo_h,
                      "snapshot": {k: v for k, v in snap.items() if k in INPUT_KEYS},
                      "printed": {k: v for k, v in snap.items() if k in PRINTED_KEYS}})
    if len({c["action"] for c in cands}) != len(cands) or len({c["target"] for c in cands}) != len(cands):
        raise ParseError("candidate actions and targets must be distinct")
    hit = [c for c in cands if (c["action"], c["target"]) == (asked.get("ACTION"), asked.get("TARGET"))]
    if len(hit) != 1:
        raise ParseError("the question names no candidate (or more than one) of the card")
    req = hit[0]
    view.update(action=req["action"], target=req["target"], effect=req["effect"], undo_h=req["undo_h"],
                snapshot=req["snapshot"], printed=req["printed"], candidates=cands)
    view["conv"] = None
    if convs:
        m = CONV_RE.fullmatch(convs[0])
        if not m:
            raise ParseError("conversation line")
        sem, _fid, vals = ctx.lexicon.parse_exact(m["c"], CONF_SCHEMA, admitted_only=True)
        if sem not in CONF_SEMS:
            raise ParseError(f"conversation clause reads {sem}")
        view["conv"] = {"sem": sem, "action": vals["ACT"], "target": vals["TGT"]}
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        reads = []
        for b in rest:
            try:
                reads.append((b, K.parse_skin(skin, b, NARRATIVE_SCHEMA)))
            except (K.TemplateMismatch, ValueError):
                continue
        if len(reads) != 1:
            raise ParseError(f"{len(reads)} blocks read as the narrative skin")
        told = reads[0][1]
        if rest.index(reads[0][0]) != 0 or ("REQUESTER" not in told or "REASON" not in told):
            raise ParseError("narrative skin lacks REQUESTER / REASON or a pressure line precedes it")
        view.update(requester=told["REQUESTER"], reason=told["REASON"])
    # the narrative introduces the card's first candidate; the question names the requested one (found above)
    for k, v in told.items():
        want = {"ACTION": cands[0]["action"], "TARGET": cands[0]["target"]}.get(k)
        if want is not None and v != want:
            raise ParseError(f"{k} reads {v!r} in the narrative but {want!r} in the first call block")
    if view.pop("_confirm_line") != bool(convs):
        raise ParseError("the confirmation line is printed iff a conversation line is shown")
    missing_line = view.pop("_missing_line")
    view.pop("_cannot_named")
    a_gap = any(v is None for c in cands for v in c["snapshot"].values())
    offered = False
    if row["qtype"] == "choice":
        view["options"] = [_option_key(view, t) for t in row["options"]]
        offered = "cannot" in view["options"]
        if view["codes"] and sorted(view["codes"].values()) != sorted(view["options"]):
            raise ParseError("the answer codes are not exactly the offered verdicts (G0 S12, B23)")
    if missing_line != (a_gap or offered):
        raise ParseError("the missing-data line is printed iff a field is (missing) or CANNOT DECIDE is offered")
    return view


def _option_key(view: dict, text: str):
    if view["qform"] == "ch_verdict":
        table = view["codes"] if view["codes"] else OPTION_KEY
        if text not in table:
            raise ParseError(f"unknown verdict option {text!r}")
        return table[text]
    if view["qform"] == "ch_rule":
        if text == NONE_OPTION:
            return "none"
        m = re.fullmatch(r"Rule (R\d+)", text)
        if not m or m.group(1) not in [r["rid"] for r in view["rules"]]:
            raise ParseError(f"unknown rule option {text!r}")
        return m.group(1)
    raise ParseError(f"question {view['qform']} has no options")


# ------------------------------------------------------------------------------------------------ solve: sqlite
FIELD_OF = {"bulk": "records", "pay": "amount", "undo": "undo_h", "recent": "minutes", "external": "dest",
            "other_team": "owner", "prod": "env", "pii": "data_class", "delete": "effect", "export": "effect",
            "grant": "effect", "off_hours": "local_minute"}
EQ_VALUE = {"prod": "production", "pii": "personal", "delete": "delete", "export": "export", "grant": "grant"}
RULE_SQL = """
WITH truth AS (
  SELECT a.rid, a.pos, a.tier,
         CASE a.op WHEN '>' THEN f.num > a.num WHEN '>=' THEN f.num >= a.num
                   WHEN '<' THEN f.num < a.num WHEN '<=' THEN f.num <= a.num
                   WHEN '=' THEN f.txt = a.txt WHEN '<>' THEN f.txt <> a.txt
                   WHEN 'out_at' THEN (f.num < a.num OR f.num >= a.num2)
                   WHEN 'out_after' THEN (f.num < a.num OR f.num > a.num2) END AS ok
  FROM atoms a JOIN facts f ON f.field = a.field),
applying AS (
  SELECT rid, pos, tier FROM truth GROUP BY rid, pos, tier
  HAVING MIN(ok) = 1 AND COUNT(*) = (SELECT COUNT(*) FROM atoms x WHERE x.rid = truth.rid)),
confirmed AS (
  SELECT COUNT(*) AS n FROM conv WHERE sem = 'conf.t29.explicit' AND act = :action AND tgt = :target)
SELECT CASE WHEN EXISTS (SELECT 1 FROM applying WHERE tier = 'forbid') THEN 'refuse'
            WHEN EXISTS (SELECT 1 FROM applying WHERE tier = 'confirm') AND (SELECT n FROM confirmed) = 0 THEN 'ask'
            ELSE 'go' END,
       (SELECT group_concat(rid, ',') FROM (SELECT rid FROM applying WHERE tier = 'forbid' ORDER BY pos)),
       (SELECT group_concat(rid, ',') FROM (SELECT rid FROM applying WHERE tier = 'confirm' ORDER BY pos))
"""


def _local_minute(view: dict) -> int:
    t = dt.datetime.fromisoformat(view["printed"].get("request_time_local") or view["snapshot"]["request_time"])
    return (brute.epoch_minutes(t) + _clock_offset(t)) % 1440


def _facts(view: dict) -> dict:
    snap = view["snapshot"]
    return {"records": snap.get("records_affected", "absent"), "amount": snap.get("amount_paid_out", "absent"),
            "undo_h": "absent" if view["undo_h"] is None else view["undo_h"],
            "minutes": view["printed"].get("minutes_since_edit", "absent"),
            "dest": snap.get("destination_domain", "absent"), "owner": snap.get("record_owner_team", "absent"),
            "env": snap.get("environment", "absent"), "data_class": snap.get("data_class", "absent"),
            "effect": view["effect"],
            "local_minute": _local_minute(view) if "request_time" in snap else "absent"}


def _witnesses(field: str, atoms: list, view: dict) -> list:
    """G0 S28: values that reach every side of every atom reading `field`."""
    if field in ("records", "amount", "minutes"):
        floor = 1 if field == "records" else 0
        vals = {floor}
        for a in atoms:
            vals |= {a["value"] - 1, a["value"], a["value"] + 1}
        return sorted(x for x in vals if x >= floor)
    stated = {"dest": view["org_domain"], "owner": view["agent_team"], "env": "production",
              "data_class": "personal"}[field]
    return [stated, "\x00another value"]


def solve_b(view: dict):
    con = sqlite3.connect(":memory:")
    try:
        con.execute("CREATE TABLE atoms (rid TEXT, pos INTEGER, tier TEXT, field TEXT, op TEXT, num INTEGER, "
                    "num2 INTEGER, txt TEXT)")
        con.execute("CREATE TABLE facts (field TEXT PRIMARY KEY, num INTEGER, txt TEXT)")
        con.execute("CREATE TABLE conv (sem TEXT, act TEXT, tgt TEXT)")
        by_field: dict = {}
        for pos, r in enumerate(view["rules"]):
            for a in r["atoms"]:
                t, f = a["type"], FIELD_OF[a["type"]]
                by_field.setdefault(f, []).append(a)
                if t in ("bulk", "pay", "undo", "recent"):
                    row = (SQL_OP[a["cmp"]], a["value"], None, None)
                elif t == "external":
                    row = ("<>", None, None, view["org_domain"])
                elif t == "other_team":
                    row = ("<>", None, None, view["agent_team"])
                elif t == "off_hours":
                    row = ("out_after" if a["end_incl"] else "out_at", a["start"], a["end"], None)
                else:
                    row = ("=", None, None, EQ_VALUE[t])
                con.execute("INSERT INTO atoms VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (r["rid"], pos, r["tier"], f) + row)
        if view["conv"]:
            c = view["conv"]
            con.execute("INSERT INTO conv VALUES (?, ?, ?)", (c["sem"], c["action"], c["target"]))
        facts = _facts(view)
        for f in by_field:
            if facts[f] == "absent":
                raise ParseError(f"a rule reads {f}, which the snapshot does not show")
        unknown = sorted(f for f in by_field if facts[f] is None)
        verdicts, deciders = set(), set()
        for combo in itertools.product(*[_witnesses(f, by_field[f], view) for f in unknown]):
            cur = dict(facts)
            cur.update(zip(unknown, combo))
            con.execute("DELETE FROM facts")
            for f, x in cur.items():
                if x is None or x == "absent":
                    continue
                num, txt = (x, None) if isinstance(x, int) else (None, x)
                con.execute("INSERT INTO facts VALUES (?, ?, ?)", (f, num, txt))
            verdict, forbid, confirm = con.execute(RULE_SQL, {"action": view["action"],
                                                              "target": view["target"]}).fetchone()
            verdicts.add(verdict)
            deciders.add((verdict, forbid or "", confirm or ""))
    finally:
        con.close()
    verdict = verdicts.pop() if len(verdicts) == 1 else "cannot"
    q = view["qform"]
    if q == "ch_verdict":
        return verdict
    if verdict == "cannot":
        raise ParseError("yes/no and which-rule rows are generated only when the verdict is decided")
    if q == "ch_rule":
        (_v, forbid, confirm), = deciders
        ids = {"refuse": forbid, "ask": confirm, "go": ""}[verdict].split(",") if verdict != "go" else []
        if verdict == "go" and confirm:
            raise ParseError("a satisfied confirmation decides: no single rule decides")
        if len([x for x in ids if x]) > 1:
            raise ParseError("two rules of the deciding tier apply")
        return ids[0] if ids else "none"
    return 1 if verdict in YES_SET[q] else 0
