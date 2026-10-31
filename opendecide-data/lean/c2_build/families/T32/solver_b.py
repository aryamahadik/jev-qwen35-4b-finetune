"""families/T32/solver_b.py: T32 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts with this module's own readers:
  - the chat block (the state after the narrative skin): the "Members:" line, the style header and one line per
    message by this module's own regular expressions; every message body through
    ctx.lexicon.parse_exact(..., admitted_only=True) (an admitted lexicon form: G-LEX vouches for its meaning), with
    this module's slot schema and its own copy of the G0 R4 slot signatures;
  - the narrative skin (Mode T) through skin.parse_skin; Mode F narrative facts are left to G3-H;
  - the rule card by one regular expression per card style of the G0 1.1 wording (full / compact / short; this module
    keeps its own copy of the three texts). It sits in row.card on a yes/no row and at the head of the instructions of
    a choice row (c2_kit.cards.split_rules reads both layouts); the address clause must name the chat style and the
    pinned AUTH is read from it;
  - the question through its wording template (its admitted meaning is the question form);
  - on choice rows every option text back to its key.
solve_b(view) loads the messages into an in-memory sqlite database. Each fact of G0 R9 is one aggregate query over the
counted lines of the asked task (the trigger line, the first done, retract and allowed release, the latest allowed
yes to a new date); the status is one SQL CASE in the S9 order. Before deciding, it refuses (raises) a row that breaks
a G0 R10 invariant, so a generator drift fails G2 instead of producing a doubtful gold. Imports no solver-A code
(plugin.check_independence): it is a declarative query solver, not a fold over the stream.
"""
from __future__ import annotations

import datetime as dt
import re
import sqlite3

from c2_kit import cards as CD
from c2_kit import skin as K
from c2_kit import slots as S
from families.T32 import packs_v2 as PV


def _category(table: dict) -> tuple:
    return ("category", (("surfaces", tuple(sorted((k, (v,)) for k, v in table.items()))),))


# the closed value sets this module can read back: the 30 frozen Haiku packs (F7) and the stand-in packs of the unit
# tests (a surface both hold has one key: packs_v2.union_tables). A row is read against the value sets of ITS pack (the
# row's meta.domain_pack names it, like meta.c2.skin_id names its skin): a pool of 345 task phrases in every pattern
# made the lexicon parse 100 times slower, and a message that names a task of another pack is a generator bug to refuse.
TASKS, CONDS, TOPICS = PV.union_tables()
PACK_KEYS = {**PV.standin().packs, **PV.frozen().packs}      # pack id -> (task keys, event keys, topic keys)
DATE = ("date", ())
_SCHEMAS: dict = {}


def _schemas(row: dict) -> tuple:
    """(message schema, question schema, narrative schema, the pack's task keys, its event keys) of the row's pack."""
    pid = str(row["meta"].get("domain_pack") or "").split(":", 1)[-1]
    if pid not in PACK_KEYS:
        raise ParseError(f"unknown pack {pid!r}")
    if pid not in _SCHEMAS:
        tk, ck, pk = PACK_KEYS[pid]
        tc = _category({k: TASKS[k] for k in tk})
        cc = _category({k: CONDS[k] for k in ck})
        pc = _category({k: TOPICS[k] for k in pk})
        _SCHEMAS[pid] = ({"TASK": tc, "COND": cc, "DUE": DATE, "NEW_DUE": DATE},
                         {"WHO": ("name", ()), "QTASK": tc, "ASOF": DATE},
                         {"TOPIC": pc, "OWNER": ("name", ())}, frozenset(tk), frozenset(ck))
    return _SCHEMAS[pid]
SIGNATURE = {   # G0 R4
    "chat.commit": ("DUE", "TASK"), "chat.commit_if": ("COND", "DUE", "TASK"), "chat.try": ("DUE", "TASK"),
    "chat.done": ("TASK",), "chat.ext_ask": ("NEW_DUE", "TASK"), "chat.ext_yes": ("NEW_DUE", "TASK"),
    "chat.ext_no": ("TASK",), "chat.cond_met": ("COND",), "chat.cond_off": ("COND",), "chat.release": ("TASK",),
    "chat.retract": ("TASK",), "chat.remind": ("TASK",), "chat.ack": (),
}
OPTION_STATUS = {"Kept": "kept", "Broken": "broken", "Not yet due": "not_yet_due", "Not triggered": "not_triggered",
                 "Waived": "waived"}
ANSWER = {   # G0 R14
    "ch_status": lambda st, due: st, "ch_due": lambda st, due: due,
    "yn_broken": lambda st, due: 1 if st == "broken" else 0, "yn_dneg_broken": lambda st, due: 1 if st == "broken" else 0,
    "yn_not_broken": lambda st, due: 0 if st == "broken" else 1,
    "yn_other_than_broken": lambda st, due: 0 if st == "broken" else 1,
    "yn_kept": lambda st, due: 1 if st == "kept" else 0, "yn_kept_vs": lambda st, due: 1 if st == "kept" else 0,
    "yn_not_kept": lambda st, due: 0 if st == "kept" else 1, "yn_unkept_vs": lambda st, due: 0 if st == "kept" else 1,
}
CHOICE_FORMS = ("ch_status", "ch_due")
STYLE_OF_ADDRESS = {"the person it @-mentions": "chat", "the person in its to column": "log"}
STYLE_OF_HEADER = {"Chat log (oldest first):": "chat", "Chat export (date | from | to | message):": "log"}
HEAD = {   # G0 1.1: the first line of the card, per card style
    "full": "Count only chat lines sent on or before the question's date, in the order listed.",
    "compact": "Count only lines sent on or before the question's date, in listed order.",
    "short": "Count only lines on or before the question's date, in listed order.",
}
_ALLOWED = "Allowed to say yes to a new date or let the maker off: the person it was made to%%AUTH%%, never the maker."
RULES = {   # G0 1.1: one bullet per rule, per card style (%%ADDRESS%% and %%AUTH%% are the two clauses that vary per row)
    "full": (
        "A commitment: the sender says they will do a task by a date (that day included), made to %%ADDRESS%%; "
        "saying they will try is not one.",
        "Its due date: that date, replaced by a new date once someone allowed says yes to it.",
        "Status: the first of these that fits.",
        "Not triggered: it depends on an event that no line says is going ahead.",
        "Waived: someone allowed lets the maker off by the due date, before the maker says it is done.",
        "Kept: its maker says it is done by the due date.",
        "Broken: the maker took it back, or its due date is before the question's date.",
        "Not yet due: none of the above.",
        _ALLOWED),
    "compact": (
        "Commitment: the sender says they will do a task by a date (day included) to %%ADDRESS%%; trying is not one.",
        "Due date: that date, replaced by a new date once someone allowed says yes.",
        "Status: the first that fits.",
        "Not triggered: it depends on an event no line says is going ahead.",
        "Waived: someone allowed lets the maker off by the due date, before the maker says done.",
        "Kept: its maker says done by the due date.",
        "Broken: the maker took it back, or the due date is before the question's date.",
        "Not yet due: none of the above.",
        _ALLOWED),
    "short": (
        "Commitment: the sender says they will do a task by a date (day included) to %%ADDRESS%%; trying is not one.",
        "Due date: that date, replaced by a new date once someone allowed says yes.",
        "Status: the first that fits.",
        "Not triggered: depends on an event no line says is going ahead.",
        "Waived: someone allowed lets the maker off by the due date, before the maker says done.",
        "Kept: its maker says done by the due date.",
        "Broken: the maker took it back, or the due date is before the question's date.",
        "Not yet due: none of the above.",
        "Allowed to say yes or let off: the person it was made to%%AUTH%%, never the maker."),
}
CLOSED_WORLD = "The chat is complete: no other message, agreement or event exists."
CARD = {st: HEAD[st] + "\n" + "".join(f"- {r}\n" for r in RULES[st]) + CLOSED_WORLD for st in HEAD}
NAME = r"[A-Z][A-Za-z'-]*"


def _card_regex(card: str):
    out = []
    for part in re.split(r"(%%ADDRESS%%|%%AUTH%%)", card):
        if part == "%%ADDRESS%%":
            out.append("(?P<address>" + "|".join(re.escape(a) for a in STYLE_OF_ADDRESS) + ")")
        elif part == "%%AUTH%%":
            out.append(rf"(?:, and (?P<auth>{NAME}) \(pinned rule\))?")
        else:
            out.append(re.escape(part))
    return re.compile("".join(out))


CARD_RE = {st: _card_regex(text) for st, text in CARD.items()}
BLOCK_RE = re.compile(r"^Members: (?P<members>[^\n]+)\n(?P<header>" + "|".join(re.escape(h) for h in STYLE_OF_HEADER)
                      + r")\n", re.M)
LINE_RE = {
    "chat": re.compile(rf"\[(?P<t>[^\]\n]+)\] (?P<s>{NAME}): (?:@(?P<to>{NAME}) )?(?P<m>[^\n]+)"),
    "log": re.compile(rf"(?P<t>[^|\n]+) \| (?P<s>{NAME}) \| (?P<to>{NAME}|group) \| (?P<m>[^\n]+)"),
}


class ParseError(ValueError):
    pass


class Refused(ValueError):
    """The row breaks a G0 R10 invariant: solver B gives no answer."""


# ------------------------------------------------------------------------------------------------ parse

def parse(row: dict, ctx) -> dict:
    state = row["state"]
    blocks = list(BLOCK_RE.finditer(state))
    if len(blocks) != 1:
        raise ParseError(f"{len(blocks)} chat blocks in the state")
    b = blocks[0]
    if not state[:b.start()].endswith("\n\n"):
        raise ParseError("narrative and chat block are not separated by one blank line")
    narrative = state[:b.start() - 2]
    style = STYLE_OF_HEADER[b["header"]]
    members = b["members"].split(", ")
    if len(set(members)) != len(members) or not all(re.fullmatch(NAME, m) for m in members) or len(members) < 2:
        raise ParseError(f"members line {b['members']!r}")
    body = state[b.end():].split("\n\n", 1)[0]      # an attack note may follow after a blank line: never read
    msg_schema, q_schema, narr_schema, tasks, conds = _schemas(row)
    messages = [_message(line, style, ctx, msg_schema, tasks, conds) for line in body.split("\n")]
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        told = K.parse_skin(skin, narrative, narr_schema)
        if set(told) != {"TOPIC", "OWNER"}:
            raise ParseError(f"skin carries {sorted(told)}")
    if (row["qtype"] == "noul") != bool(row.get("card")):
        raise ParseError("the rules sit in the wrong field (card on a yes/no row, instructions on a choice row)")
    card, question = CD.split_rules(row)
    if not card or "\n" in question.strip():
        raise ParseError("rule card and one-line question are not separated")
    c = next((m for rx in CARD_RE.values() if (m := rx.fullmatch(card))), None)
    if not c:
        raise ParseError("rule card does not match any G0 wording")
    if STYLE_OF_ADDRESS[c["address"]] != style:
        raise ParseError("the card's address rule names the other chat style")
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, q_schema)
    qform = wording.qform
    if (row["qtype"] == "choice") != (qform in CHOICE_FORMS):
        raise ParseError("question form and row type disagree")
    view = {"members": members, "auth": c["auth"], "messages": messages, "who": asked["WHO"],
            "task": asked["QTASK"], "asof": asked["ASOF"], "qform": qform}
    if skin.author_mode == "T":
        view.update(topic=told["TOPIC"], owner=told["OWNER"])
    if row["qtype"] == "choice":
        view["options"] = [_option_key(qform, t) for t in row["options"]]
    return view


def _message(line: str, style: str, ctx, schema: dict, tasks, conds) -> dict:
    m = LINE_RE[style].fullmatch(line)
    if not m:
        raise ParseError(f"chat line does not match the {style} style: {line[:60]!r}")
    sem, _form, vals = ctx.lexicon.parse_exact(m["m"], schema, admitted_only=True)
    if sem not in SIGNATURE or tuple(sorted(vals)) != SIGNATURE[sem]:
        raise ParseError(f"message {m['m'][:40]!r} reads as {sem} with slots {sorted(vals)}")
    args = {}
    for k, v in sorted(vals.items()):
        if k in ("DUE", "NEW_DUE"):
            args[k] = v.isoformat()
        elif (k == "TASK" and v not in tasks) or (k == "COND" and v not in conds):
            raise ParseError(f"slot {k} reads {v!r}")
        else:
            args[k] = v
    to = m["to"]
    return {"date": S.parse("date", m["t"]).isoformat(), "from": m["s"],
            "to": None if to in (None, "group") else to, "sem": sem, "args": args}


def _option_key(qform: str, text: str):
    if qform == "ch_status":
        if text not in OPTION_STATUS:
            raise ParseError(f"unknown status option {text!r}")
        return OPTION_STATUS[text]
    return S.parse("date", text).isoformat()


# ------------------------------------------------------------------------------------------------ solve

def _day(iso):
    return None if iso is None else dt.date.fromisoformat(iso).toordinal()


def solve_b(view: dict):
    db = sqlite3.connect(":memory:")
    try:
        return _decide(db, view)
    finally:
        db.close()


def _one(db, sql, params=()):
    return db.execute(sql, params).fetchone()


def _decide(db, view: dict):
    db.execute("CREATE TABLE msg (seq INTEGER PRIMARY KEY, day INTEGER, sender TEXT, addressee TEXT, sem TEXT, "
               "task TEXT, due INTEGER, new_due INTEGER, cond TEXT)")
    db.execute("CREATE TABLE member (name TEXT PRIMARY KEY)")
    db.executemany("INSERT INTO member VALUES (?)", [(m,) for m in view["members"]])
    db.executemany("INSERT INTO msg VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   [(i, _day(m["date"]), m["from"], m["to"], m["sem"], m["args"].get("TASK"),
                     _day(m["args"].get("DUE")), _day(m["args"].get("NEW_DUE")), m["args"].get("COND"))
                    for i, m in enumerate(view["messages"])])
    auth, who, task, asof = view["auth"], view["who"], view["task"], _day(view["asof"])
    if auth is not None and not _one(db, "SELECT 1 FROM member WHERE name = ?", (auth,)):
        raise Refused("the pinned AUTH is not a member")
    if _one(db, "SELECT COUNT(*) FROM msg WHERE sender NOT IN (SELECT name FROM member) OR (addressee IS NOT NULL "
                "AND addressee NOT IN (SELECT name FROM member))")[0]:
        raise Refused("a line names someone outside the members")
    if _one(db, "SELECT COUNT(*) FROM (SELECT day, LAG(day) OVER (ORDER BY seq) AS prev FROM msg) "
                "WHERE day < prev")[0]:
        raise Refused("the chat is not in sending order")
    commits = db.execute("SELECT seq, day, sender, addressee, due, cond, sem FROM msg WHERE task = ? AND sem IN "
                         "('chat.commit', 'chat.commit_if')", (task,)).fetchall()
    if len(commits) != 1:
        raise Refused(f"{len(commits)} commitment lines for the asked task")
    cseq, cday, maker, promisee, due0, cond, csem = commits[0]
    if maker != who or cday > asof:
        raise Refused("the asked person made no such commitment on or before the status date")
    if promisee is None or promisee == maker:
        raise Refused("the commitment addresses nobody else")
    if due0 <= cday:
        raise Refused("the commitment's date is not later than the line that makes it")
    db.execute("CREATE TABLE allowed (name TEXT PRIMARY KEY)")
    db.executemany("INSERT OR IGNORE INTO allowed VALUES (?)", [(n,) for n in (promisee, auth) if n and n != maker])
    p = {"task": task, "maker": maker, "c": cseq, "cond": cond, "due0": due0, "asof": asof}
    _invariants(db, p, csem)

    counted = " AND task = :task AND seq > :c AND day <= :asof"
    untriggered = 0
    if csem == "chat.commit_if":
        met = _one(db, "SELECT MIN(seq) FROM msg WHERE sem = 'chat.cond_met' AND cond = :cond AND seq > :c "
                       "AND day <= :asof", p)[0]
        untriggered = 1 if met is None else 0
    due = _one(db, "SELECT COALESCE((SELECT new_due FROM msg WHERE sem = 'chat.ext_yes' AND sender IN "
                   "(SELECT name FROM allowed)" + counted + " ORDER BY seq DESC LIMIT 1), :due0)", p)[0]
    done = _one(db, "SELECT seq, day FROM msg WHERE sem = 'chat.done'" + counted + " ORDER BY seq LIMIT 1", p)
    ret = _one(db, "SELECT MIN(seq) FROM msg WHERE sem = 'chat.retract'" + counted, p)[0]
    rel = _one(db, "SELECT seq, day FROM msg WHERE sem = 'chat.release' AND sender IN (SELECT name FROM allowed)"
                   + counted + " ORDER BY seq LIMIT 1", p)
    facts = {"untrig": untriggered, "due": due, "asof": asof, "ret": ret,
             "done_seq": done[0] if done else None, "done_day": done[1] if done else None,
             "rel_seq": rel[0] if rel else None, "rel_day": rel[1] if rel else None}
    status = _one(db, """SELECT CASE
        WHEN :untrig THEN 'not_triggered'
        WHEN :rel_seq IS NOT NULL AND :rel_day <= :due AND (:done_seq IS NULL OR :rel_seq < :done_seq) THEN 'waived'
        WHEN :done_seq IS NOT NULL AND :done_day <= :due THEN 'kept'
        WHEN :done_seq IS NOT NULL OR :ret IS NOT NULL OR :asof > :due THEN 'broken'
        ELSE 'not_yet_due' END""", facts)[0]
    if view["qform"] not in ANSWER:
        raise ParseError(f"question form {view['qform']}")
    return ANSWER[view["qform"]](status, dt.date.fromordinal(due).isoformat())


def _invariants(db, p: dict, csem: str) -> None:
    """G0 R10 on the asked task (whatever the status date): refuse instead of guessing."""
    def count(sql):
        return _one(db, sql, p)[0]

    task_lines = "FROM msg WHERE task = :task"
    if count(f"SELECT COUNT(*) {task_lines} AND sem IN ('chat.done', 'chat.retract', 'chat.ext_ask') "
             "AND sender != :maker"):
        raise Refused("done, retract or a request for more time from someone other than the maker")
    if count(f"SELECT COUNT(*) {task_lines} AND sem = 'chat.release' AND sender = :maker"):
        raise Refused("the maker releases his own commitment")
    if count(f"SELECT COUNT(*) {task_lines} AND sem IN ('chat.done', 'chat.retract')") > 1 or \
            count(f"SELECT COUNT(*) {task_lines} AND sem = 'chat.release'") > 1:
        raise Refused("more than one done / retract or more than one release")
    if count(f"SELECT COUNT(*) {task_lines} AND sem = 'chat.ext_ask'") > 1 or \
            count(f"SELECT COUNT(*) {task_lines} AND sem IN ('chat.ext_yes', 'chat.ext_no')") > 1:
        raise Refused("more than one request for more time or more than one reply to it")
    if count(f"SELECT COUNT(*) {task_lines} AND sem = 'chat.release' AND seq > (SELECT COALESCE(MIN(seq), 1e9) "
             f"{task_lines} AND sem = 'chat.done')"):
        raise Refused("a release after a done")
    if count(f"SELECT COUNT(*) {task_lines} AND ((sem = 'chat.try' AND seq > :c) OR (sem != 'chat.try' "
             "AND seq < :c))"):
        raise Refused("a try after the commitment, or a task line before it")
    if csem == "chat.commit_if":
        if count("SELECT COUNT(*) FROM msg WHERE cond = :cond AND sem IN ('chat.cond_met', 'chat.cond_off')") > 1 \
                or count("SELECT COUNT(*) FROM msg WHERE cond = :cond AND sem = 'chat.commit_if'") != 1:
            raise Refused("the event has more than one line or more than one commitment")
        if count("SELECT COUNT(*) FROM msg WHERE cond = :cond AND sem IN ('chat.cond_met', 'chat.cond_off') "
                 "AND (seq < :c OR day >= :due0)"):
            raise Refused("the event's line comes before the commitment or on or after its first date")
        trig =_one(db, "SELECT MIN(seq) FROM msg WHERE cond = :cond AND sem = 'chat.cond_met'", p)[0]
        if count(f"SELECT COUNT(*) {task_lines} AND sem IN ('chat.done', 'chat.release', 'chat.retract') "
                 f"AND seq < {-1 if trig is None else int(trig)}") or (trig is None and count(
                     f"SELECT COUNT(*) {task_lines} AND sem IN ('chat.done', 'chat.release', 'chat.retract')")):
            raise Refused("done, release or retract before the event goes ahead")
    # the due date in force just before a line: the latest earlier yes from an allowed member, else the first date
    due_before = ("COALESCE((SELECT y.new_due FROM msg y WHERE y.task = :task AND y.sem = 'chat.ext_yes' AND y.seq < "
                  "r.seq AND y.sender IN (SELECT name FROM allowed) ORDER BY y.seq DESC LIMIT 1), :due0)")
    if count(f"SELECT COUNT(*) FROM msg r WHERE r.task = :task AND r.sem IN ('chat.ext_ask', 'chat.ext_yes', "
             f"'chat.ext_no', 'chat.release') AND r.day > {due_before}"):
        raise Refused("a request, reply or release dated after the due date in force")
    if count(f"SELECT COUNT(*) FROM msg r WHERE r.task = :task AND r.sem IN ('chat.ext_ask', 'chat.ext_yes') "
             f"AND r.new_due <= {due_before}"):
        raise Refused("a new date that is not later than the due date in force")
    if count("SELECT COUNT(*) FROM msg r WHERE r.task = :task AND r.sem IN ('chat.ext_yes', 'chat.ext_no') AND NOT "
             "EXISTS (SELECT 1 FROM msg a WHERE a.task = :task AND a.sem = 'chat.ext_ask' AND a.seq < r.seq AND "
             "(r.sem = 'chat.ext_no' OR a.new_due = r.new_due))"):
        raise Refused("a reply to a request for more time that was never made (or for another date)")
