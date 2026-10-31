"""families/T33/solver_b.py: T33 solver B, written from G0_SPEC.md (not from plugin.py). Paradigm sql_sqlite.

parse(row, ctx) reads the RENDERED row back into the canonical facts, with this module's own parsers:
  - the tool log in any of its four containers (JSON lines through json, CSV through csv, plain text and markdown
    table through its own patterns). Every try of a step must agree on tool, target, idempotency key, field and
    request; try numbers count up from 1; a 202 try names a job and every poll names the job of its step's 202 try;
    steps are numbered 1..n in order of first appearance;
  - the headers ("Request from ...:", "Agent's final message to ...:") by its own patterns;
  - the context or message skin through skin.parse_skin (claim clauses through the lexicon; admitted forms only);
  - the rule block (read through c2_kit.cards.split_rules: the card on yes/no rows, the head of the instructions on
    choice rows): it must equal one of the G0 styles (full, short) for the facts the row shows (listed checks or
    claims, the log container), i.e. exactly the need-to-know bullets; criterion checks through lexicon.parse_exact
    (admitted forms only);
  - the question through its wording template; on choice rows, every option text back to its key.
Facts that appear twice (user, target, step) must read the same.
solve_b(view) loads steps and lines into an in-memory sqlite database and decides by SQL: tries, done, result and
duration per step; each criterion check is a SQL predicate from a decision table; claims are joined to steps on the
target and compared through this module's own unit table. A claim whose target matches two steps raises BindError
(the row is dropped, spec 3.3). Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import csv
import json
import re
import sqlite3

from c2_kit import cards
from c2_kit import skin as K
from c2_kit import slots as S

# ------------------------------------------------------------------------------------------------ G0 text (S7-S9)
LOG_HEAD = "Tool log:\n"
REQ_RE = re.compile(r"Request from (?P<user>[^\n:]+):\n")
MSG_RE = re.compile(r"Agent's final message to (?P<user>[^\n:]+):\n")
# G0 section 2 as amended (section 8): the rules block, own copy of the texts. Bullets appear only when the row needs
# them; two styles ("full" is the frozen phrasing, "short" the terse one on about 15% of rows).
LOG_HEAD_LINE = "Log rules (lines in time order):"
DONE_LINE = {
    "full": "- A step is done if a try got 200, 201 or 204, a retry with the same idempotency key got 409, or a try got "
            "202 and the job's last poll says succeeded.",
    "short": "- A step is done if a try got 200, 201 or 204, a retry with the same key got 409, or a try got 202 and the "
             "job's last poll says succeeded."}
OTHER_LINE = {"full": "- Any other try status does nothing. A poll's status 200 means nothing; its state counts."}
OTHER_LINE["short"] = OTHER_LINE["full"]
RESULT_LINE = {   # (fields named, style)
    ("amount_cents", "full"): "- Result: amount_cents on the try that got 200 or 201, else on the job's last poll.",
    ("amount_cents", "short"): "- Result: amount_cents on the 200 or 201 try, else on the job's last poll.",
    ("rows_written", "full"): "- Result: rows_written on the try that got 200 or 201, else on the job's last poll.",
    ("rows_written", "short"): "- Result: rows_written on the 200 or 201 try, else on the job's last poll.",
    ("both", "full"): "- Result: amount_cents or rows_written on the try that got 200 or 201, else on the job's last "
                      "poll.",
    ("both", "short"): "- Result: amount_cents or rows_written on the 200 or 201 try, else on the job's last poll."}
UNIT_LINE = {
    ("cents", "full"): "- amount_cents is cents (100 = $1).", ("cents", "short"): "- amount_cents: cents (100 = $1).",
    ("ms", "full"): "- duration_ms is milliseconds.", ("ms", "short"): "- duration_ms: milliseconds.",
    ("both", "full"): "- amount_cents is cents (100 = $1); duration_ms is milliseconds.",
    ("both", "short"): "- amount_cents: cents (100 = $1); duration_ms: milliseconds."}
TABLE_LINE = {"full": "- Table: requested and result are in the unit named by field.",
              "short": "- Table: requested and result use the unit named by field."}
CRIT_RE = re.compile(r"Success criterion for step (?P<step>[^:\n]+): every check must hold(?P<rest>[^\n]*)\.")
CRIT_DEP = {"full": "; a check on a value the log does not show fails", "short": "; a check on a value the log lacks fails"}
CRIT_TRIES = "; polls are not tries"
CHECK_RE = re.compile(r"\((?P<n>[1-9])\) (?P<text>[^\n]+)")
TIE_CHECK_LINE = {"full": "If several checks fail, answer the lowest-numbered one; if none fails, answer None.",
                  "short": "Answer the lowest-numbered failing check; if none fails, answer None."}
CLAIM_HEAD = "Claim rules: a claim is about the step whose target it names."
CLAIM_NOT_SHOWN = "No step in the log has that target: not shown in the log."
TIE_CLAIM_LINE = {"full": "If several claims are contradicted or not shown, answer the one first in the message; if "
                          "none, answer None.",
                  "short": "Answer the first claim in the message that is contradicted or not shown, or None if none "
                           "is."}
CLOSED_LINE = "The log is complete and the only evidence: no other call, retry or poll took place."
MONEY_CLAIMS = ("claim.refund", "claim.charge", "claim.credit", "claim.payout")
ROW_CLAIMS = ("claim.import", "claim.export", "claim.sync")
STYLES = ("full", "short")
COLUMNS = ("step", "line", "tool", "target", "idempotency_key", "field", "requested", "status", "job", "state",
           "result", "duration_ms")
CSV_HEAD = ",".join(COLUMNS)
MD_HEAD = "| " + " | ".join(COLUMNS) + " |"
MD_SEP = "|" + "---|" * len(COLUMNS)
STATE_WORDS = ("queued", "running", "succeeded", "failed")
REQUEST_FIELD = {"amount_cents": "amount_cents", "rows_requested": "rows"}     # JSON / text name -> field
RESULT_FIELD = {"amount_cents": "amount_cents", "rows_written": "rows"}
TABLE_FIELDS = ("amount_cents", "rows")
TRY_TEXT = re.compile(r"step (?P<step>\d+) try (?P<try>\d+) \| (?P<tool>[^\s|]+) target=(?P<target>[^\s|]+) "
                      r"idempotency_key=(?P<key>[^\s|]+)(?: (?P<rk>amount_cents|rows_requested)=(?P<req>\d+))? "
                      r"\| status (?P<status>\d+)(?: \| (?:job=(?P<job>[^\s|]+)|(?P<sk>amount_cents|rows_written)="
                      r"(?P<res>\d+)))?")
POLL_TEXT = re.compile(r"step (?P<step>\d+) poll (?P<job>[^\s|]+) \| status (?P<status>\d+) \| state=(?P<state>[a-z]+)"
                       r"(?: (?P<sk>amount_cents|rows_written)=(?P<res>\d+))?(?: duration_ms=(?P<dur>\d+))?")
SUB = {"yn_step_ok": "a", "yn_step_failed": "a", "yn_step_fail_to": "a", "yn_step_not_ok": "a",
       "yn_dneg_step_ok": "a", "ch_failed_check": "a", "yn_all_supported": "b", "yn_any_bad": "b",
       "yn_not_all_supported": "b", "yn_dneg_all_supported": "b", "ch_bad_claim": "b", "ch_claim_verdict": "b"}
CHECK_SCHEMA = {"R": ("count", (("unit", ("try", "tries")),)), "D": ("count", (("unit", ("second", "seconds")),))}
CONTEXT_SCHEMA = {"USER": ("name", ()), "TARGET": ("id", ())}
MESSAGE_SCHEMA = {"USER": ("name", ()), **{f"K{j}": ("clause", ()) for j in range(1, 5)}}
QUESTION_SCHEMA = {"STEP": ("count", ()), "TARGET": ("id", ())}
NONE_TEXTS = {"ch_failed_check": "None: every check holds", "ch_bad_claim": "None: every claim is supported"}
VERDICT_OF = {"Supported by the log": "supported", "Contradicted by the log": "contradicted",
              "Not shown in the log": "not_shown"}
CLAIM_OPTION_RE = re.compile(r"The claim about (?P<t>\S+)")
# claim sem -> unit of its stated value (None: the claim states no value) -- G0 S9
CLAIM_UNIT = {"claim.refund": "claim_cents", "claim.charge": "claim_cents", "claim.credit": "claim_cents",
              "claim.payout": "claim_cents", "claim.import": "claim_rows", "claim.export": "claim_rows",
              "claim.sync": "claim_rows", "claim.send": None, "claim.book": None, "claim.cancel": None,
              "claim.update": None}
# own unit table: name -> (base unit, factor to the base unit)
UNIT_ROWS = (("amount_cents", "cents", 1), ("rows", "rows", 1), ("claim_cents", "cents", 1), ("claim_rows", "rows", 1),
             ("second", "ms", 1000))
CHECK_SQL = {
    "crit.finished": "done = 1",
    "crit.all_written": "result IS NOT NULL AND field = 'rows' AND result = requested",
    "crit.amount_match": "result IS NOT NULL AND field = 'amount_cents' AND result = requested",
    "crit.max_tries": "tries <= :p",
    "crit.max_duration": "duration IS NOT NULL AND duration <= :p * (SELECT factor FROM unit WHERE name = 'second')",
}


class ParseError(ValueError):
    pass


class BindError(ParseError):
    """A claim's target matches two steps: the row is dropped (spec 3.3)."""


def _int(v) -> int:
    if isinstance(v, bool) or not isinstance(v, int):
        raise ParseError(f"not an integer: {v!r}")
    return v


def _text(v) -> str:
    if not isinstance(v, str) or not v:
        raise ParseError(f"not a non-empty string: {v!r}")
    return v


def _num(s: str | None):
    if s is None or s == "":
        return None
    if not re.fullmatch(r"\d+", s):
        raise ParseError(f"not a plain number: {s!r}")
    return int(s)


def _rec(step, kind, try_no, tool, target, key, field, requested, status, job, state, result, duration) -> dict:
    return {"step": step, "kind": kind, "try": try_no, "tool": tool, "target": target, "key": key, "field": field,
            "requested": requested, "status": status, "job": job, "state": state, "result": result,
            "duration": duration}


# ------------------------------------------------------------------------------------------------ log containers
def _from_json(line: str) -> dict:
    o = json.loads(line)
    if not isinstance(o, dict):
        raise ParseError("log line is not a JSON object")
    if set(o) in ({"step", "try", "tool", "args", "status", "result"}, {"step", "try", "tool", "args", "status"}):
        args, res = o["args"], o.get("result", {})              # a try with no result prints no result object
        if not isinstance(args, dict) or not isinstance(res, dict):
            raise ParseError("args / result are not objects")
        extra = sorted(set(args) - {"target", "idempotency_key"})
        if (len(extra) > 1 or (extra and extra[0] not in REQUEST_FIELD)
                or not {"target", "idempotency_key"} <= set(args)):
            raise ParseError(f"unexpected args {sorted(args)}")
        field = REQUEST_FIELD[extra[0]] if extra else None
        requested = _int(args[extra[0]]) if extra else None
        job = result = None
        if set(res) == {"job"}:
            job = _text(res["job"])
        elif len(res) == 1 and next(iter(res)) in RESULT_FIELD:
            if RESULT_FIELD[next(iter(res))] != field:
                raise ParseError("result field differs from the request field")
            result = _int(next(iter(res.values())))
        elif res:
            raise ParseError(f"unexpected result {sorted(res)}")
        return _rec(_int(o["step"]), "try", _int(o["try"]), _text(o["tool"]), _text(args["target"]),
                    _text(args["idempotency_key"]), field, requested, _int(o["status"]), job, None, result, None)
    if set(o) == {"step", "poll", "status", "result"}:
        res = o["result"]
        if not isinstance(res, dict) or "state" not in res:
            raise ParseError("poll without a state")
        vals = sorted(set(res) - {"state", "duration_ms"})
        if len(vals) > 1 or (vals and vals[0] not in RESULT_FIELD):
            raise ParseError(f"unexpected poll result {sorted(res)}")
        return _rec(_int(o["step"]), "poll", None, None, None, None, RESULT_FIELD[vals[0]] if vals else None, None,
                    _int(o["status"]), _text(o["poll"]), _text(res["state"]),
                    _int(res[vals[0]]) if vals else None,
                    _int(res["duration_ms"]) if "duration_ms" in res else None)
    raise ParseError(f"unexpected log keys {sorted(o)}")


def _from_text(line: str) -> dict:
    m = TRY_TEXT.fullmatch(line)
    if m:
        field = REQUEST_FIELD[m["rk"]] if m["rk"] else None
        if m["sk"] and RESULT_FIELD[m["sk"]] != field:
            raise ParseError("result field differs from the request field")
        return _rec(int(m["step"]), "try", int(m["try"]), m["tool"], m["target"], m["key"], field, _num(m["req"]),
                    int(m["status"]), m["job"], None, _num(m["res"]), None)
    m = POLL_TEXT.fullmatch(line)
    if m:
        return _rec(int(m["step"]), "poll", None, None, None, None, RESULT_FIELD[m["sk"]] if m["sk"] else None,
                    None, int(m["status"]), m["job"], m["state"], _num(m["res"]), _num(m["dur"]))
    raise ParseError(f"unreadable log line {line!r}")


def _from_cells(cells: list) -> dict:
    if len(cells) != len(COLUMNS):
        raise ParseError(f"table row has {len(cells)} cells")
    c = dict(zip(COLUMNS, cells))
    field = c["field"] or None
    if field is not None and field not in TABLE_FIELDS:
        raise ParseError(f"unknown field {field!r}")
    m = re.fullmatch(r"try (\d+)", c["line"])
    if m:
        if c["state"] or c["duration_ms"]:
            raise ParseError("a try row with a state or duration")
        if (field is None) != (c["requested"] == ""):
            raise ParseError("requested without its field (or the reverse)")
        return _rec(_num(c["step"]), "try", int(m.group(1)), _text(c["tool"]), _text(c["target"]),
                    _text(c["idempotency_key"]), field, _num(c["requested"]), _num(c["status"]), c["job"] or None,
                    None, _num(c["result"]), None)
    if c["line"] == "poll":
        if c["tool"] or c["target"] or c["idempotency_key"] or c["requested"]:
            raise ParseError("a poll row with call fields")
        if (field is None) != (c["result"] == ""):
            raise ParseError("poll result without its field (or the reverse)")
        return _rec(_num(c["step"]), "poll", None, None, None, None, field, None, _num(c["status"]),
                    _text(c["job"]), _text(c["state"]), _num(c["result"]), _num(c["duration_ms"]))
    raise ParseError(f"unknown line kind {c['line']!r}")


def read_log(text: str) -> tuple:
    """(records, container) from the log block."""
    lines = text.split("\n")
    if not lines or not lines[0]:
        raise ParseError("empty log")
    if lines[0].startswith("{"):
        return [_from_json(x) for x in lines], "jsonl"
    if lines[0] == CSV_HEAD:
        rows = list(csv.reader(lines[1:]))
        return [_from_cells(r) for r in rows], "csv"
    if lines[0] == MD_HEAD:
        if len(lines) < 2 or lines[1] != MD_SEP:
            raise ParseError("markdown table without its separator row")
        out = []
        for x in lines[2:]:
            if not (x.startswith("| ") and x.endswith(" |")):
                raise ParseError(f"bad markdown row {x!r}")
            out.append(_from_cells([cell.strip() for cell in x[2:-2].split(" | ")]))
        return out, "md"
    if lines[0].startswith("step "):
        return [_from_text(x) for x in lines], "text"
    raise ParseError("unknown log container")


def steps_and_lines(recs: list) -> tuple:
    """Group the records into steps (consistency checks) and the canonical line list."""
    steps, order, lines = {}, [], []
    for r in recs:
        if r["status"] is None or r["step"] is None:
            raise ParseError("a log line without its step or status")
        if r["kind"] == "try":
            s = steps.get(r["step"])
            same = ("tool", "target", "key", "field", "requested")
            if s is None:
                if r["try"] != 1:
                    raise ParseError("a step starts with a try other than 1")
                s = steps[r["step"]] = {k: r[k] for k in same} | {"job": None, "last_try": 1}
                order.append(r["step"])
            else:
                if any(s[k] != r[k] for k in same):
                    raise ParseError(f"step {r['step']}: tries disagree on the call")
                if r["try"] != s["last_try"] + 1:
                    raise ParseError(f"step {r['step']}: try numbers do not count up")
                s["last_try"] = r["try"]
            if r["status"] == 202:
                if s["job"] is not None or r["job"] is None:
                    raise ParseError("a 202 try must name a job, once per step")
                s["job"] = r["job"]
            elif r["job"] is not None:
                raise ParseError("a job on a try that is not a 202")
            lines.append([r["step"], "try", r["try"], r["status"], None, r["result"], None])
        else:
            s = steps.get(r["step"])
            if s is None or s["job"] is None or s["job"] != r["job"]:
                raise ParseError("a poll of a job its step never started")
            if r["state"] not in STATE_WORDS:
                raise ParseError(f"unknown job state {r['state']!r}")
            if (r["result"] is not None) != (s["field"] is not None) or (r["field"] not in (None, s["field"])):
                raise ParseError("poll value does not match the step's field")
            lines.append([r["step"], "poll", None, r["status"], r["state"], r["result"], r["duration"]])
    if order != list(range(1, len(order) + 1)):
        raise ParseError("steps are not numbered 1..n in order")
    rows = [[k, s["tool"], s["target"], s["key"], s["field"], s["requested"], s["job"]]
            for k, s in sorted(steps.items())]
    return rows, lines


# ------------------------------------------------------------------------------------------------ parse
def _split_state(state: str, sub: str) -> tuple:
    """(user, skin text, log text)."""
    if state.count(LOG_HEAD) != 1:
        raise ParseError("the row must hold exactly one tool log")
    at = state.index(LOG_HEAD)
    log = state[at + len(LOG_HEAD):].split("\n\n", 1)[0]
    if sub == "a":
        m = REQ_RE.match(state)
        if not m or not state[:at].endswith("\n\n"):
            raise ParseError("request header and log are not where G0 puts them")
        return m["user"], state[m.end():at - 2], log
    ms = list(MSG_RE.finditer(state))
    if len(ms) != 1:
        raise ParseError("the row must hold exactly one agent message")
    m = ms[0]
    if m.start() < at:
        if m.start() != 0 or state[at - 2:at] != "\n\n":
            raise ParseError("message-first row out of shape")
        return m["user"], state[m.end():at - 2], log
    if at != 0 or not state[:m.start()].endswith("\n\n"):
        raise ParseError("log-first row out of shape")
    return m["user"], state[m.end():], log


def _admitted(ctx, form_id: str) -> None:
    if ctx.lexicon.status(form_id) != "admitted":
        raise ParseError(f"lexicon form {form_id} is not admitted")


def _expected_rules(style: str, qform: str, sub: str, need: dict, step: str | None, check_lines: list) -> list:
    """The rules block of one style, line by line, for the facts the row shows (G0 section 2 as amended)."""
    out = [LOG_HEAD_LINE, DONE_LINE[style], OTHER_LINE[style]]
    if need["money"] or need["rows"]:
        out.append(RESULT_LINE[("both" if need["money"] and need["rows"] else
                                "amount_cents" if need["money"] else "rows_written", style)])
    if need["money"] or need["dur"]:
        out.append(UNIT_LINE[("both" if need["money"] and need["dur"] else "cents" if need["money"] else "ms", style)])
    if need["table"] and (need["money"] or need["rows"]):
        out.append(TABLE_LINE[style])
    if sub == "a":
        out.append(f"Success criterion for step {step}: every check must hold"
                   + (CRIT_DEP[style] if need["dep"] else "") + (CRIT_TRIES if need["tries"] else "") + ".")
        out += check_lines
        if qform == "ch_failed_check":
            out.append(TIE_CHECK_LINE[style])
    else:
        differs = ""
        if need["money"] or need["rows"]:
            what = "amount or row count" if need["money"] and need["rows"] else ("amount" if need["money"]
                                                                               else "row count")
            differs = f", or the claim's {what} differs from its result"
        if style == "full":
            out += [CLAIM_HEAD, "- " + CLAIM_NOT_SHOWN, f"- That step is not done{differs}: contradicted.",
                    "- Otherwise: supported."]
        else:
            out.append(CLAIM_HEAD + " No step in the log has that target: not shown in the log. "
                       f"That step is not done{differs}: contradicted. Otherwise: supported.")
        if qform == "ch_bad_claim":
            out.append(TIE_CLAIM_LINE[style])
    out.append(CLOSED_LINE)
    return out


def _same_rules(lines: list, qform: str, sub: str, need: dict, step: str | None, check_lines: list) -> None:
    """The row's rules block must equal one style's text for exactly the rules it needs (no more, no fewer)."""
    for style in STYLES:
        if lines == _expected_rules(style, qform, sub, need, step, check_lines):
            return
    raise ParseError("the rules block differs from the G0 text (no style matches the need-to-know bullets)")


def parse(row: dict, ctx) -> dict:
    wording = ctx.skin(row["meta"]["wording_id"])
    qform = wording.qform
    sub = SUB[qform]
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    if skin.author_mode != "T":
        raise ParseError("Mode F rows are read by G3-H, not by this parser")
    user, skin_text, log_text = _split_state(row["state"], sub)
    user = S.parse("name", user)
    recs, container = read_log(log_text)
    steps, lines = steps_and_lines(recs)
    by_step = {s[0]: s for s in steps}
    rules, question = cards.split_rules(row)            # the card on yes/no rows, the instructions' head on choice rows
    if not rules:
        raise ParseError("the row carries no rules block")
    rest = rules.split("\n")
    asked = K.match_template(wording.text, question, QUESTION_SCHEMA)
    view = {"qform": qform, "user": user, "target": None, "steps": steps, "lines": lines}
    if sub == "a":
        told = K.parse_skin(skin, skin_text, CONTEXT_SCHEMA)
        at = next((i for i, x in enumerate(rest) if x.startswith("Success criterion for step ")), None)
        m = CRIT_RE.fullmatch(rest[at]) if at is not None else None
        if not m:
            raise ParseError("criterion header differs from the G0 text")
        step = S.parse("count", m["step"])
        checks, texts, pos = [], [], at + 1
        while pos < len(rest) and CHECK_RE.fullmatch(rest[pos]):
            cm = CHECK_RE.fullmatch(rest[pos])
            if int(cm["n"]) != len(checks) + 1:
                raise ParseError("checks are not numbered 1..n")
            sem, form_id, vals = ctx.lexicon.parse_exact(cm["text"], CHECK_SCHEMA, admitted_only=True)
            checks.append([sem, vals.get("R", vals.get("D"))])
            texts.append(rest[pos])
            pos += 1
        if not checks:
            raise ParseError("a criterion without checks")
        sems = [c[0] for c in checks]
        need = {"money": "crit.amount_match" in sems, "rows": "crit.all_written" in sems,
                "dur": "crit.max_duration" in sems, "tries": "crit.max_tries" in sems,
                "dep": any(x in sems for x in ("crit.amount_match", "crit.all_written", "crit.max_duration")),
                "table": container in ("csv", "md")}
        _same_rules(rest, qform, "a", need, m["step"], texts)
        if step not in by_step:
            raise ParseError("the criterion names a step the log does not have")
        for k, v in (("STEP", step), ("TARGET", by_step[step][2]), ("USER", user)):
            for got in (told.get(k), asked.get(k)):
                if got is not None and got != v:
                    raise ParseError(f"{k} reads {got!r} in the text but {v!r} elsewhere")
        view.update(step=step, checks=checks, target=by_step[step][2])
    else:
        told = K.parse_skin(skin, skin_text, MESSAGE_SCHEMA, lexicon=ctx.lexicon)
        if told.get("USER", user) != user:
            raise ParseError("the message greets another user")
        claims = []
        for j in range(1, 5):
            c = told.get(f"K{j}")
            if c is None:
                break
            _admitted(ctx, c["form"])
            if c["sem"] not in CLAIM_UNIT:
                raise ParseError(f"{c['sem']} is not a T33 claim")
            want = {"T", "V"} if CLAIM_UNIT[c["sem"]] else {"T"}
            if set(c["values"]) != want:
                raise ParseError(f"claim {j} carries {sorted(c['values'])}")
            claims.append([c["sem"], c["values"]["T"], c["values"].get("V")])
        if len(claims) < 2 or any(f"K{j}" in told for j in range(len(claims) + 1, 5)):
            raise ParseError("claims are not numbered 1..n")
        need = {"money": any(c[0] in MONEY_CLAIMS for c in claims), "rows": any(c[0] in ROW_CLAIMS for c in claims),
                "dur": False, "tries": False, "dep": False, "table": container in ("csv", "md")}
        _same_rules(rest, qform, "b", need, None, [])
        if qform == "ch_claim_verdict":
            if "TARGET" not in asked or asked["TARGET"] not in [c[1] for c in claims]:
                raise ParseError("the question asks about a claim the message does not make")
            view["target"] = asked["TARGET"]
        view["claims"] = claims
    if row["qtype"] == "choice":
        view["options"] = [_option_key(qform, t, ctx) for t in row["options"]]
    return view


def _option_key(qform: str, text: str, ctx):
    if text == NONE_TEXTS.get(qform):
        return "none"
    if qform == "ch_claim_verdict":
        if text not in VERDICT_OF:
            raise ParseError(f"unknown verdict option {text!r}")
        return VERDICT_OF[text]
    if qform == "ch_bad_claim":
        m = CLAIM_OPTION_RE.fullmatch(text)
        if not m:
            raise ParseError(f"unknown claim option {text!r}")
        return m["t"]
    if qform == "ch_failed_check":
        return ctx.lexicon.parse_exact(text, CHECK_SCHEMA, admitted_only=True)[0]
    raise ParseError(f"question {qform} has no options")


# ------------------------------------------------------------------------------------------------ solve (sqlite)
SCHEMA_SQL = """
CREATE TABLE step (n INTEGER PRIMARY KEY, tool TEXT, target TEXT, key TEXT, field TEXT, requested INTEGER, job TEXT);
CREATE TABLE line (seq INTEGER PRIMARY KEY, step INTEGER, kind TEXT, try_no INTEGER, status INTEGER, state TEXT,
                   result INTEGER, duration INTEGER, key TEXT, job TEXT);
CREATE TABLE unit (name TEXT PRIMARY KEY, base TEXT, factor INTEGER);
CREATE TABLE claim (pos INTEGER PRIMARY KEY, sem TEXT, target TEXT, value INTEGER, unit TEXT);
"""
FACTS_SQL = """
CREATE TABLE facts AS
SELECT n, target, field, requested, tries,
       CASE WHEN direct_seq IS NOT NULL OR by_conflict = 1
                 OR (queued = 1 AND (SELECT state FROM line WHERE seq = last_poll) = 'succeeded') THEN 1 ELSE 0 END
         AS done,
       CASE WHEN direct_seq IS NOT NULL THEN (SELECT result FROM line WHERE seq = direct_seq)
            ELSE (SELECT result FROM line WHERE seq = last_poll) END AS result,
       (SELECT duration FROM line WHERE seq = last_poll) AS duration
FROM (
  SELECT s.n, s.target, s.field, s.requested,
         (SELECT COUNT(*) FROM line t WHERE t.step = s.n AND t.kind = 'try') AS tries,
         (SELECT MAX(t.seq) FROM line t WHERE t.step = s.n AND t.kind = 'try' AND t.status IN (200, 201, 204))
           AS direct_seq,
         EXISTS (SELECT 1 FROM line t WHERE t.step = s.n AND t.kind = 'try' AND t.status = 409 AND EXISTS (
                   SELECT 1 FROM line e WHERE e.step = t.step AND e.kind = 'try' AND e.seq < t.seq AND e.key = t.key))
           AS by_conflict,
         EXISTS (SELECT 1 FROM line t WHERE t.step = s.n AND t.kind = 'try' AND t.status = 202) AS queued,
         (SELECT MAX(p.seq) FROM line p WHERE p.kind = 'poll' AND p.job = s.job) AS last_poll
  FROM step s
);
"""
VERDICT_SQL = """
SELECT g.pos, g.target, g.hits,
       CASE WHEN g.hits = 0 THEN 'not_shown'
            WHEN g.done = 0 THEN 'contradicted'
            WHEN g.value IS NOT NULL AND (g.result IS NULL OR fu.factor IS NULL
                 OR g.value * cu.factor <> g.result * fu.factor) THEN 'contradicted'
            ELSE 'supported' END AS verdict,
       cu.base AS claim_base, fu.base AS field_base
FROM (SELECT c.pos AS pos, c.target AS target, c.value AS value, c.unit AS unit, COUNT(f.n) AS hits,
             MAX(f.done) AS done, MAX(f.result) AS result, MAX(f.field) AS field
      FROM claim c LEFT JOIN facts f ON f.target = c.target GROUP BY c.pos) g
LEFT JOIN unit cu ON cu.name = g.unit LEFT JOIN unit fu ON fu.name = g.field
ORDER BY g.pos
"""


def solve_b(view: dict):
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(SCHEMA_SQL)
        db.executemany("INSERT INTO unit VALUES (?, ?, ?)", UNIT_ROWS)
        key_of, job_of = {}, {}
        for n, tool, target, key, field, requested, job in view["steps"]:
            db.execute("INSERT INTO step VALUES (?, ?, ?, ?, ?, ?, ?)", (n, tool, target, key, field, requested, job))
            key_of[n], job_of[n] = key, job
        for seq, (n, kind, try_no, status, state, result, duration) in enumerate(view["lines"], 1):
            db.execute("INSERT INTO line VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (seq, n, kind, try_no, status, state, result, duration,
                        key_of[n] if kind == "try" else None,
                        job_of[n] if (kind == "poll" or status == 202) else None))
        db.executescript(FACTS_SQL)
        qform = view["qform"]
        if SUB[qform] == "a":
            results = []
            for sem, p in view["checks"]:
                if sem not in CHECK_SQL:
                    raise ParseError(f"unknown check {sem}")
                got = db.execute(f"SELECT CASE WHEN {CHECK_SQL[sem]} THEN 1 ELSE 0 END FROM facts WHERE n = :step",
                                 {"p": p, "step": view["step"]}).fetchone()
                results.append((sem, bool(got[0])))
            failing = [sem for sem, ok in results if not ok]
            return {"yn_step_ok": lambda: 0 if failing else 1,
                    "yn_dneg_step_ok": lambda: 0 if failing else 1,
                    "yn_step_failed": lambda: 1 if failing else 0,
                    "yn_step_fail_to": lambda: 1 if failing else 0,
                    "yn_step_not_ok": lambda: 1 if failing else 0,
                    "ch_failed_check": lambda: failing[0] if failing else "none"}[qform]()
        for pos, (sem, target, value) in enumerate(view["claims"], 1):
            db.execute("INSERT INTO claim VALUES (?, ?, ?, ?, ?)", (pos, sem, target, value, CLAIM_UNIT[sem]))
        verdicts = []
        for pos, target, hits, verdict, claim_base, field_base in db.execute(VERDICT_SQL):
            if hits > 1:
                raise BindError(f"claim {pos} binds to {hits} steps")
            if hits == 1 and claim_base is not None and claim_base != field_base:
                raise ParseError(f"claim {pos} states {claim_base} but its step logs {field_base}")
            verdicts.append((target, verdict))
        bad = [t for t, v in verdicts if v != "supported"]
        if qform == "ch_claim_verdict":
            return [v for t, v in verdicts if t == view["target"]][0]
        return {"yn_all_supported": lambda: 0 if bad else 1,
                "yn_dneg_all_supported": lambda: 0 if bad else 1,
                "yn_any_bad": lambda: 1 if bad else 0,
                "yn_not_all_supported": lambda: 1 if bad else 0,
                "ch_bad_claim": lambda: bad[0] if bad else "none"}[qform]()
    finally:
        db.close()
