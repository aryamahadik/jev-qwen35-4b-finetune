"""Unit tests for golden_src/gen3/v3_state_track.py (F3 decide2, builder B).

Every expected answer below was worked out by hand from the rule texts of the small hand-written worlds in this file
(no generator code, no program gold). The worlds cover each of the 10 machines and the traps SPEC F3 lists:
guard-failing requests, resends, reverts, expiries at the exact end time, look-alike ids, partial tool batches,
display order != time order, SLA business hours across a weekend, a holiday and a DST change.

Run:  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider yn2b/tests/test_v3_state_track_unit.py
"""
from __future__ import annotations

import csv
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
GEN3 = Path(__file__).resolve().parents[2] / "golden_src" / "gen3"
if str(GEN3) not in sys.path:
    sys.path.insert(0, str(GEN3))

import v3_state_track as v3  # noqa: E402

# ---------------------------------------------------------------------------------------------------------------
# Rule texts (the rendered F3 rule sentences, with this file's own parameters)
# ---------------------------------------------------------------------------------------------------------------
COMMON_E = [
    "Each event line is a request. A request that breaks a rule at the moment it happens is rejected and changes "
    "nothing.",
    "Events take effect in timestamp order, whatever order they are listed in. Times written with a UTC offset are "
    "converted to UTC before they are compared.",
    "Each event id takes effect at most once. A later line that repeats an id that already took effect is a "
    "redelivery and changes nothing.",
]
AT_TIME = "The state at a stated time counts only the events timestamped at or before that time."
REVERT_RESTORE = ("A revert line names an earlier event id. If that event took effect and has not been reverted "
                  "yet, every value it changed goes back to what it was just before that event; otherwise the revert "
                  "changes nothing.")


def only(kind: str) -> str:
    return (f"Only the {kind} listed in the starting state exist. An event that names any other id changes nothing, "
            "even when the id looks almost the same: ids must match character for character.")


RULES = {
    "orders": [
        "Order statuses change only by these steps: pay (created to paid), pack (paid to packed), ship (packed to "
        "shipped), deliver (shipped to delivered), cancel (created, paid or packed to cancelled), return (delivered "
        "to returned).",
        "Language lines map to steps: a payment line is pay, a packing line is pack, a carrier or courier collection "
        "line is ship, a delivery line is deliver, a cancellation line is cancel, a returned parcel line is return, "
        "and an undo or revert line is a revert.",
        *COMMON_E, only("orders"), AT_TIME, REVERT_RESTORE],
    "tickets": [
        "Ticket statuses: new, assigned, in_progress, waiting, resolved, closed. Steps: start (assigned to "
        "in_progress), wait (in_progress to waiting), resume (waiting to in_progress, when the customer answers), "
        "resolve (in_progress or waiting to resolved), reopen (resolved to in_progress), close (resolved to closed).",
        "An assignment sets the owner and moves a new ticket to assigned. It is allowed only while the ticket is new, "
        "assigned, in_progress or waiting, and only to a person on the support roster: Tami Rook, Enzo Vale.",
        "Resolution is due 4 business hours after the ticket was opened. Business hours are 09:00 to 17:00 local time "
        "in Europe/London, Monday to Friday, except these holidays: 2026-03-30.",
        "A ticket is on time if it first reached resolved at or before its due time; later reopening does not change "
        "the first resolution time. It is overdue at a stated time if that time is after the due time and it had not "
        "first reached resolved by the due time.",
        "Escalation level at a stated time: level 0 if the ticket is not overdue; otherwise measure the business time "
        "from the due time to its first resolution (or to the stated time, if it was not resolved by then): under 4 "
        "business hours is level 1, 4 to under 8 is level 2, 8 to under 16 is level 3, and 16 or more is level 4.",
        *COMMON_E, only("tickets"), AT_TIME, REVERT_RESTORE],
    "inventory": [
        "Available units = units on hand minus units under an active hold minus units in quarantine (never below 0).",
        "A receive adds units on hand. A ship removes units on hand and is allowed only if that many units are "
        "available at that moment. A hold reserves units for the stated number of minutes and is allowed only if "
        "that many units are available; it stops counting at its start time plus those minutes (it no longer counts "
        "at exactly that time), or when it is released.",
        "A release names the event id of an earlier hold that is still active; otherwise it changes nothing. A "
        "quarantine moves available units into quarantine (only if that many are available); a clear returns "
        "quarantined units (only up to the number in quarantine).",
        "A cycle count sets the units on hand to the counted number; holds and quarantine stay as they are.",
        *COMMON_E, only("SKUs"), AT_TIME,
        "A revert line names an earlier event id. If that event took effect and has not been reverted yet, its own "
        "change is undone: units it received are taken off again (never below 0), units it shipped are put back, a "
        "hold it placed is removed, a hold it released comes back, units it quarantined return to available (never "
        "below 0 in quarantine), units it cleared go back into quarantine, and a cycle count's on-hand number goes "
        "back to what it was just before the count. Later events keep their effect. Otherwise the revert changes "
        "nothing."],
    "ledger": [
        "Amounts are in EUR. The posted balance changes with deposits, fees, transfers and posted authorisations. The "
        "available balance is the posted balance minus the authorisations still pending.",
        "A card authorisation is allowed only if its amount is at most the available balance at that moment. It "
        "stays pending until it is posted, and it lapses 6 hours after it was made (it no longer counts at exactly "
        "that time).",
        "A post names the event id of an authorisation that is still pending and not lapsed: its amount leaves the "
        "posted balance and it stops being pending. Any other post changes nothing.",
        "A transfer out is allowed only if its amount is at most the available balance at that moment. Deposits and "
        "fees are always applied.",
        *COMMON_E, only("accounts"), AT_TIME,
        "A reversal line names an earlier event id. If that event took effect and has not been reversed yet, its own "
        "change is undone: a deposit's amount is taken off again, a fee's or transfer's amount is added back, an "
        "authorisation stops being pending, and a post adds its amount back and makes the authorisation pending "
        "again with its original lapse time. Later events keep their effect. Otherwise the reversal changes "
        "nothing."],
    "bookings": [
        "A hold reserves a slot for one person for the stated minutes (default 15). It stops counting at its start "
        "time plus those minutes (it no longer counts at exactly that time).",
        "A hold is allowed only if the slot has no confirmed booking and no active hold by another person.",
        "A confirmation is allowed only for the person whose hold on that slot is active at that moment; it turns "
        "the hold into that person's confirmed booking.",
        "A cancellation is allowed only for the person who holds the confirmed booking; it frees the slot. A release "
        "is allowed only for the person whose hold is active; it ends the hold.",
        "A slot is free for a new hold when it has no confirmed booking and no active hold.",
        *COMMON_E, only("slots"), AT_TIME, REVERT_RESTORE],
    "access": [
        "Roles on a resource rank viewer < editor < owner. A person's access is the highest role among the grants in "
        "force for them, given to them directly or to a group they belong to at the stated time.",
        "Only these admins may change access: Kara Voss, Juno Pell. A change logged by anyone else is rejected and "
        "changes nothing.",
        "A grant with a number of hours stops counting at its start time plus those hours (it no longer counts at "
        "exactly that time). A grant without hours lasts until it is revoked.",
        "A revoke names the event id of an earlier grant; that grant stops counting. A revoke of a grant that never "
        "took effect, or is already revoked, changes nothing.",
        "A deny rule blocks the person from the resource whatever grants they hold, until the deny rule is lifted.",
        "Renaming a group keeps its members and grants. After a rename, only the new name refers to the group; a "
        "line using the old name changes nothing.",
        "Viewing needs viewer or higher; editing needs editor or higher.",
        *COMMON_E, only("resources"), AT_TIME],
    "dialogue": [
        "Slots and their allowed values: seat: window, aisle, table seat; coach: coach A, coach B, coach C, coach D; "
        "meal: standard meal, vegetarian meal, vegan meal, no meal.",
        "Only the customer's own requests about booking BK-7000001 change its slots. A request with no booking "
        "reference is about this booking. The assistant's proposals, the customer's 'no' to a proposal, and what "
        "other people want change nothing.",
        "A confirmation by the assistant counts only when it repeats the slot's current value; it makes that value "
        "the slot's most recent confirmed value. Any other confirmation changes nothing.",
        "'Same as before' (or 'go back to what we had before') sets the slot to its most recent confirmed value.",
        "'Not X' (or 'anything but X') removes X from the slot's allowed values. If X was the current value, or the "
        "slot had no value, the slot then takes the only remaining allowed value when exactly one remains; otherwise "
        "it has no value. A request for a value that is not allowed changes nothing.",
        "The starting state lists the confirmed values from before this chat; they count as confirmed.",
        "Messages take effect in timestamp order. A message id that already took effect changes nothing when it "
        "appears again.",
        "Booking references must match character for character; a message about any other reference changes nothing "
        "for BK-7000001."],
    "agent": [
        "Each line is one tool call by the assistant, with the tool's result after the arrow. Only the parts the "
        "result reports as ok change anything: 'ok' means every part succeeded, 'error' means none did, and "
        "'partial' lists each part as ok or failed.",
        "{tools}",
        "A line that repeats a call id is a retry. A call id takes effect at most once: a retry of a call that "
        "already took effect changes nothing.",
        "An undo call names an earlier call id. If that call took effect and has not been undone yet, its successful "
        "parts are undone: quantities it added are taken off again (never below 0), quantities it removed are put "
        "back, and a quantity it set or a file it moved, deleted or restored goes back to what it was just before "
        "that call. Later calls keep their effect. Otherwise the undo changes nothing.",
        "Calls take effect in timestamp order, whatever order they are listed in.",
        "{only}",
        "The state at a stated time counts only the calls timestamped at or before that time."],
    "flags": [
        "A flag is on for a person in production when no kill switch is engaged and either an override for that "
        "person is in force (then the override decides) or the flag is enabled in production and the person's "
        "bucket number is below the production rollout percentage.",
        "Changes to production (enable, disable, rollout, clearing a kill switch) take effect only with an approved "
        "change ticket: CHG-1111, CHG-2222. Anything else is rejected and changes nothing. Staging changes never "
        "affect production.",
        "Anyone on call may engage a kill switch without a ticket. An override lasts the stated hours from its time "
        "(it no longer counts at exactly the end time).",
        "Every line in the log asks for one change. If that change breaks a rule at the time it is asked for, it is "
        "refused and nothing changes.",
        "Changes apply in the order of their timestamps, not the order the lines appear in. Convert any time that "
        "carries a UTC offset to UTC before comparing.",
        "An event id can apply only once. If the same id shows up again after it already applied, the repeat is "
        "ignored.",
        "For a question about a given time, only lines timestamped at or before that time count.",
        "A revert names an earlier event id. If that event applied and was not reverted before, the values it "
        "changed return to what they were right before it; otherwise the revert does nothing."],
    "docs": [
        "Each save or restore adds one new version at the end; the current version is the last one. A restore of "
        "version k adds a new version with the content of version k. Version 1 is the starting content.",
        "A lock gives one person sole editing for 60 minutes from the lock time (it no longer counts at exactly the "
        "end time), or until that person unlocks it. While a lock is in force, saves and restores by anyone else are "
        "rejected, and a new lock is rejected.",
        "Only these approvers can approve a version: Pia Lund, Oto Marsh. An approval by anyone else, or of a version "
        "that does not exist yet, is rejected. The current version is approved when an approval names its number.",
        "Every line in the log asks for one change. If that change breaks a rule at the time it is asked for, it is "
        "refused and nothing changes.",
        "Changes apply in the order of their timestamps, not the order the lines appear in. Convert any time that "
        "carries a UTC offset to UTC before comparing.",
        "An event id can apply only once. If the same id shows up again after it already applied, the repeat is "
        "ignored.",
        "For a question about a given time, only lines timestamped at or before that time count."],
}
TITLE = {"orders": "order", "tickets": "ticket", "inventory": "SKU", "ledger": "account", "bookings": "slot",
         "access": "resource", "dialogue": "booking", "agent": "item", "flags": "flag", "docs": "document"}


# ---------------------------------------------------------------------------------------------------------------
# A small renderer of this test's own (from the notes' surface description), for 12 of the renderers
# ---------------------------------------------------------------------------------------------------------------
def render(mach, ctx, start, ents, events, fmt="log", record=None, rules=None):
    """events: list of (time, id, by, text) in LISTING order. ents: list of (id, [(k, v), ...])."""
    rules = rules or RULES[mach]
    title = f"Testco - {TITLE[mach]} event log"
    rl = [f"R{i} (in force from 2025-01-0{1 + i % 9}) {t}" for i, t in enumerate(rules, 1)]
    if fmt == "json":
        d = {"title": title, "context": dict(ctx), "rules": rl,
             "starting_state": {"as_of": start, "entries": [{"id": i, **dict(f)} for i, f in ents]},
             "events": [{"time": t, "id": e, "by": b, "event": x} for t, e, b, x in events],
             "agent_record": None if record is None else {"written_at": record[0], "entries": record[1]},
             "notes": ["Times are shown as each source system recorded them."]}
        return json.dumps(d, indent=1, ensure_ascii=False)
    if fmt == "kv":
        out = [f"title: {title}"] + [f"context.{k}: {v}" for k, v in ctx]
        out += [f"rules.{i}: {r}" for i, r in enumerate(rl, 1)]
        out.append(f"starting_state.as_of: {start}")
        for n, (i, f) in enumerate(ents, 1):
            out.append(f"starting_state.entries.{n}.id: {i}")
            out += [f"starting_state.entries.{n}.{k}: {v}" for k, v in f]
        for n, (t, e, b, x) in enumerate(events, 1):
            out += [f"events.{n}.time: {t}", f"events.{n}.id: {e}", f"events.{n}.by: {b}", f"events.{n}.event: {x}"]
        if record is None:
            out.append("agent_record: none")
        else:
            out.append(f"agent_record.written_at: {record[0]}")
            out += [f"agent_record.entries.{n}: {x}" for n, x in enumerate(record[1], 1)]
        out.append("notes.1: Export requested by the audit desk.")
        return "\n".join(out)
    start_lines = [f"- {i}: " + ", ".join(f"{k} = {v}" for k, v in f) for i, f in ents]
    rec_lines = [] if record is None else [f"Agent record (written at {record[0]}):"] + [f"- {x}" for x in record[1]]
    if fmt == "markdown":
        out = [f"# {title}", "", "## Context"] + [f"- {k}: {v}" for k, v in ctx] + ["", "## Rules"]
        out += [r.replace(") ", ") ", 1).replace(f"R{n} (", f"R{n}. (", 1) for n, r in enumerate(rl, 1)]
        out += ["", f"## Starting state at {start}"] + start_lines + ["", "## Events"]
        out += [f"- {t} | {e} | {b} | {x}" for t, e, b, x in events]
        if record is not None:
            out += ["", f"## Agent record (written at {record[0]})"] + [f"- {x}" for x in record[1]]
        return "\n".join(out + ["", "## Notes", "- Lines are copied from the source systems without edits."])
    head = [title] + [f"{k}: {v}" for k, v in ctx] + ["", "Rules:"] + rl + [""]
    if fmt == "prose":
        head = [title, "; ".join(f"{k}: {v}" for k, v in ctx) + ".", "", "Rules:"] + rl + [""]
        st = "; ".join(f"{i} (" + ", ".join(f"{k} {v}" for k, v in f) + ")" for i, f in ents)
        sents = []
        for t, e, b, x in events:
            sents.append(f"At {t}, {b} logged {e}: {x}" + ("" if x.endswith((".", "?", "!")) else "."))
        paras = [" ".join(sents[k:k + 4]) for k in range(0, len(sents), 4)]
        body = [f"At {start} the starting state was: {st}.", "", "What happened:"] + paras
        return "\n".join(head + body + ([""] + rec_lines if rec_lines else []) + ["", "Notes:", "- Exported."])
    body = [f"Starting state at {start}:"] + start_lines + [""]
    if fmt == "log":
        body += ["Event log:"] + [f"{t} [{b}] #{e} {x}" for t, e, b, x in events]
    elif fmt == "log:grouped":
        body.append("Event log:")
        groups: dict[str, list] = {}
        for t, e, b, x in events:
            groups.setdefault(b, []).append((t, e, x))
        for g, lst in groups.items():
            body += [f"== {g} =="] + [f"{t} #{e} {x}" for t, e, x in lst] + [""]
        body.pop()
    elif fmt == "email":
        body.append("Message thread:")
        for n, (t, e, b, x) in enumerate(events):
            if n:
                body += ["", "-" * 10]
            body += ["", f"From: {b}", f"Date: {t}", f"Subject: event {e}", "", x]
    elif fmt == "chat":
        body += ["Transcript:"] + [f"[{t}] {b} ({e}): {x}" for t, e, b, x in events]
    elif fmt == "table:md":
        body += ["Event table:", "| time | id | by | event |", "|---|---|---|---|"]
        body += [f"| {t} | {e} | {b} | {x} |" for t, e, b, x in events]
    elif fmt == "table:csv":
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["time", "id", "by", "event"])
        for ev in events:
            w.writerow(ev)
        body += ["Event table:"] + buf.getvalue().rstrip("\n").split("\n")
    elif fmt == "table:records":
        body += ["Event table:"] + [f"- time: {t}; id: {e}; by: {b}; event: {x}" for t, e, b, x in events]
    else:
        raise ValueError(fmt)
    return "\n".join(head + body + ([""] + rec_lines if rec_lines else []) + ["", "Notes:", "- Exported."])


def ask(state, q, options=("yes", "no")):
    return v3.decide2_row({"state": state, "instructions": q, "options": list(options)})


def explain(state, q, options=("yes", "no")):
    return v3.explain_row({"state": state, "instructions": q, "options": list(options)})


# ---------------------------------------------------------------------------------------------------------------
# Times and renderers
# ---------------------------------------------------------------------------------------------------------------
def test_parse_time_styles():
    u = datetime(2026, 3, 2, 8, 5, tzinfo=timezone.utc)
    assert v3.parse_time("2026-03-02T08:05:00Z") == u
    assert v3.parse_time("2026-03-02T09:05:00+01:00") == u
    assert v3.parse_time("2026-03-02 08:05 UTC") == u
    assert v3.parse_time("2026-03-02 03:05 UTC-05:00") == u
    with pytest.raises(v3.SolverError):
        v3.parse_time("2026-03-02 8:05")


ORD_CTX = [("system", "order desk"), ("orders tracked", "2"), ("log exported at", "2026-03-02T17:00:00Z")]
ORD_START = "2026-03-02T08:00:00Z"
ORD_ENTS = [("SO-1111111", [("status", "created"), ("customer", "Lena Hart")]),
            ("SO-2222222", [("status", "paid"), ("customer", "Omar Fitch")])]
# listed out of time order on purpose (display order != time order); one time written with an offset
ORD_EVENTS = [
    ("2026-03-02T13:00:00Z", "E1005", "ops-console", "revert event=E1002"),
    ("2026-03-02T09:00:00Z", "E1001", "payments", "pay order=SO-1111111"),
    ("2026-03-02T12:00:00+01:00", "E1003", "carrier-api", "ship order=SO-1111112"),
    ("2026-03-02T10:00:00Z", "E1002", "warehouse", "Warehouse finished packing order SO-1111111."),
    ("2026-03-02T12:00:00Z", "E1004", "carrier-api", "Carrier collected order SO-1111111."),
    ("2026-03-02T14:00:00Z", "E1002", "warehouse", "Warehouse finished packing order SO-1111111."),
    ("2026-03-02T15:00:00Z", "E1006", "support-desk", "Customer asked to cancel order SO-2222222."),
    ("2026-03-02T16:00:00Z", "E1007", "returns-desk", "return order=SO-2222222"),
]
FORMATS = ["json", "kv", "markdown", "prose", "log", "log:grouped", "email", "chat", "table:md", "table:csv",
           "table:records"]


@pytest.mark.parametrize("fmt", FORMATS)
def test_every_renderer_parses_back_the_same_events(fmt):
    st = render("orders", ORD_CTX, ORD_START, ORD_ENTS, ORD_EVENTS, fmt=fmt)
    d = v3.parse_state(st)
    assert v3.machine_of(d) == "orders"
    # prose adds a period to lines that do not end in one; compare texts without a trailing period
    got = sorted((e.t, e.eid, e.by, e.text.rstrip(".")) for e in d.events)
    want = sorted((v3.parse_time(t), i, b, x.rstrip(".")) for t, i, b, x in ORD_EVENTS)
    assert got == want
    assert d.start == v3.parse_time(ORD_START)
    assert [i for i, _ in d.entities] == ["SO-1111111", "SO-2222222"]
    assert len(d.rules) == len(RULES["orders"])


@pytest.mark.parametrize("fmt", FORMATS)
def test_orders_answers_do_not_depend_on_renderer(fmt):
    st = render("orders", ORD_CTX, ORD_START, ORD_ENTS, ORD_EVENTS, fmt=fmt)
    # E1001 pay -> paid; E1002 pack -> packed; E1003 names a look-alike id -> nothing; E1003's +01:00 time is 11:00Z;
    # E1004 ship -> shipped; E1005 reverts E1002 -> the status goes back to its value before E1002: paid;
    # E1002 again at 14:00 is a redelivery -> nothing. SO-2222222: cancel -> cancelled; return rejected.
    q = "What status does order SO-1111111 have at the end of the log, under the numbered rules?"
    assert ask(st, q, ["shipped", "paid", "packed", "created"]) == "paid"
    q = "Under the order rules, which status is order SO-1111111 in at 2026-03-02T12:00:00Z?"
    assert ask(st, q, ["shipped", "paid", "packed", "created"]) == "shipped"  # an event AT the stated time counts
    assert ask(st, "Under the order rules, which status is order SO-1111111 in at 2026-03-02T11:59:00Z?",
               ["shipped", "paid", "packed", "created"]) == "packed"


def test_orders_question_kinds():
    st = render("orders", ORD_CTX, ORD_START, ORD_ENTS, ORD_EVENTS)
    assert ask(st, "Can order SO-1111111 still be cancelled at the end of the log?") == "yes"
    assert ask(st, "Would a cancellation request for order SO-2222222 be rejected at the end of the log?") == "yes"
    assert ask(st, "Is order SO-2222222 in any status other than cancelled at the end of the log?") == "no"
    opts = ["none of the 2 listed orders", "1 of the 2 listed orders", "2 of the 2 listed orders"]
    assert ask(st, "How many of the listed orders are shipped or delivered at 2026-03-02T12:30:00Z?", opts) == opts[1]
    # a mirror: the rules' value (paid) is not offered
    assert ask(st, "Under the order rules, which status is order SO-1111111 in at the end of the log?",
               ["shipped", "packed", "created", "None of these"]) == "None of these"
    jb = ["Order SO-2222222 is not in status cancelled at the end of the log.",
          "Order SO-2222222 is in status cancelled at the end of the log."]
    assert ask(st, "Which statement follows from the log under the numbered rules?", jb) == jb[1]
    fb = ["yes, this holds", "no, this does not hold"]
    assert ask(st, "Under the numbered rules, does this statement hold? Order SO-1111111 can still be cancelled at "
                   "the end of the log.", fb) == fb[0]


@pytest.mark.parametrize("fmt", ["log", "json", "kv", "markdown", "prose"])
def test_judge_record(fmt):
    q = "Is the agent's recorded state consistent with the log under the numbered rules?"
    ok = ("2026-03-02T17:00:00Z", ["order SO-1111111 status: paid", "order SO-2222222 status: cancelled"])
    bad = ("2026-03-02T17:00:00Z", ["order SO-1111111 status: shipped", "order SO-2222222 status: cancelled"])
    early = ("2026-03-02T12:30:00Z", ["order SO-1111111 status: shipped", "order SO-2222222 status: paid"])
    for rec, want in [(ok, "yes"), (bad, "no"), (early, "yes")]:
        st = render("orders", ORD_CTX, ORD_START, ORD_ENTS, ORD_EVENTS, fmt=fmt, record=rec)
        assert ask(st, q) == want


# ---------------------------------------------------------------------------------------------------------------
# Tickets: roster guard, SLA across a weekend + holiday + DST change
# ---------------------------------------------------------------------------------------------------------------
TCK_CTX = [("system", "support desk"), ("sla clock zone", "Europe/London"), ("log exported at", "2026-04-01T12:00:00Z")]
TCK_ENTS = [("TCK-100001", [("status", "new"), ("owner", "nobody"), ("opened", "2026-03-27T16:00:00Z")]),
            ("TCK-100002", [("status", "assigned"), ("owner", "Enzo Vale")])]
TCK_EVENTS = [
    ("2026-03-27T16:20:00Z", "E2000", "dispatch", "Ticket TCK-100001 assigned to Zed Outly."),  # not on roster
    ("2026-03-27T16:30:00Z", "E2001", "dispatch", "Tami Rook now owns ticket TCK-100001."),
    ("2026-03-31T09:00:00+01:00", "E2002", "agent-console", "start ticket=TCK-100001"),
    ("2026-03-31T13:30:00Z", "E2003", "agent-console", "Fix confirmed for ticket TCK-100001."),
    ("2026-03-31T14:00:00Z", "E2004", "mail-gateway", "Ticket TCK-100001 reopened."),
    ("2026-03-31T15:00:00Z", "E2005", "agent-console", "resolve ticket=TCK-100001"),
    ("2026-03-31T15:30:00Z", "E2006", "dispatch", "assign ticket=TCK-100001 owner=Enzo Vale"),  # resolved: rejected
]


def test_ticket_sla_due_time_crosses_weekend_holiday_and_dst():
    st = render("tickets", TCK_CTX, "2026-03-27T16:00:00Z", TCK_ENTS, TCK_EVENTS)
    s = v3.Solver({"state": st, "instructions": "", "options": []})
    sim = s.sim(s.world.end)
    # Fri 27 Mar 16:00-17:00 GMT = 1 h; weekend; Mon 30 Mar is a listed holiday; the clocks change on Sun 29 Mar,
    # so Tue 31 Mar 09:00 London (BST) = 08:00Z and 3 more hours end at 12:00 London = 11:00Z.
    assert sim.due("TCK-100001") == datetime(2026, 3, 31, 11, 0, tzinfo=timezone.utc)
    # business time from the due time to 13:30Z (14:30 London) is 2.5 hours
    assert sim.business(sim.due("TCK-100001"), datetime(2026, 3, 31, 13, 30, tzinfo=timezone.utc)).seconds == 9000
    # and from Friday 16:00Z to Tuesday 09:00Z it is Friday's hour plus Tuesday 08:00-09:00Z
    assert sim.business(datetime(2026, 3, 27, 16, 0, tzinfo=timezone.utc),
                        datetime(2026, 3, 31, 9, 0, tzinfo=timezone.utc)).seconds == 7200


def test_ticket_questions():
    st = render("tickets", TCK_CTX, "2026-03-27T16:00:00Z", TCK_ENTS, TCK_EVENTS)
    lv = ["level 0 - not overdue", "level 1 - overdue by under 4 business hours",
          "level 2 - overdue by 4 to under 8 business hours", "level 3 - overdue by 8 to under 16 business hours",
          "level 4 - overdue by 16 business hours or more"]
    # first resolution 13:30Z = 14:30 London; due 11:00Z: 2.5 business hours late -> level 1 (reopening later does
    # not change the first resolution time)
    assert ask(st, "What escalation level does ticket TCK-100001 have at the end of the log?", lv) == lv[1]
    assert ask(st, "What escalation level does ticket TCK-100001 have at 2026-03-31T11:00:00Z?", lv) == lv[0]
    assert ask(st, "Is ticket TCK-100001 overdue at 2026-03-31T11:01:00Z under the SLA rules?") == "yes"
    assert ask(st, "Had ticket TCK-100001 missed its resolution due time at 2026-03-31T10:59:00Z?") == "no"
    assert ask(st, "Is ticket TCK-100001 still within its SLA at the end of the log, with no missed due time?") == "no"
    own = ["Tami Rook", "Enzo Vale", "Zed Outly", "nobody"]
    assert ask(st, "Who owns ticket TCK-100001 at the end of the log, under the numbered rules?", own) == "Tami Rook"
    assert ask(st, "Who owns ticket TCK-100001 at 2026-03-27T16:25:00Z, under the numbered rules?", own) == "nobody"
    assert ask(st, "Is Tami Rook the owner of ticket TCK-100001 at the end of the log?") == "yes"


# ---------------------------------------------------------------------------------------------------------------
# Inventory: hold expiry at the exact end, guard, clear over quarantine, revert of a count
# ---------------------------------------------------------------------------------------------------------------
INV_CTX = [("system", "warehouse stock ledger"), ("site", "Test warehouse"), ("log exported at", "2026-03-02T11:00:00Z")]
INV_ENTS = [("SKU-100001", [("item", "valve"), ("on hand", "10"), ("holds", "none"), ("quarantine", "0")])]
INV_EVENTS = [
    ("2026-03-02T09:00:00Z", "E3001", "sales-orders", "Reserved 4 units of SKU-100001 for 30 minutes."),
    ("2026-03-02T09:10:00Z", "E3002", "picking", "ship sku=SKU-100001 qty=7"),  # 6 available: rejected
    ("2026-03-02T09:30:00Z", "E3003", "picking", "Picked and shipped 7 units of SKU-100001."),  # hold gone at 09:30
    ("2026-03-02T09:40:00Z", "E3004", "quality", "quarantine sku=SKU-100001 qty=2"),
    ("2026-03-02T09:50:00Z", "E3005", "quality", "Quality released 5 units of SKU-100001 from quarantine."),
    ("2026-03-02T10:00:00Z", "E3006", "cycle-count", "Shelf count for SKU-100001 came to 8 units."),
    ("2026-03-02T10:10:00Z", "E3007", "ops-console", "Operator reverted event E3006."),
]


def test_inventory():
    st = render("inventory", INV_CTX, "2026-03-02T08:00:00Z", INV_ENTS, INV_EVENTS)
    u = ["0 units", "1 unit", "3 units", "6 units", "10 units"]
    q = "Under the stock rules, what is the available quantity of SKU-100001 at {}?"
    assert ask(st, q.format("2026-03-02T09:29:00Z"), u) == "6 units"
    assert ask(st, q.format("2026-03-02T09:30:00Z"), u) == "3 units"  # hold expired exactly then; the ship applies
    # clear of 5 with 2 in quarantine: rejected under this solver's reading; the count is reverted -> on hand 3
    assert ask(st, q.format("the end of the log"), u) == "1 unit"
    bands = ["0 units", "1 to 4 units", "5 to 9 units", "10 units or more"]
    assert ask(st, "Which band does the available quantity of SKU-100001 fall in at 2026-03-02T10:05:00Z?",
               bands) == "5 to 9 units"
    assert ask(st, "Are fewer than 2 units of SKU-100001 available at the end of the log?") == "yes"


def test_inventory_alternative_clear_reading():
    st = render("inventory", INV_CTX, "2026-03-02T08:00:00Z", INV_ENTS, INV_EVENTS)
    saved = dict(v3.READINGS)
    try:
        v3.READINGS["clear_over_quarantine"] = "clamp"
        ex = explain(st, "Under the stock rules, what is the available quantity of SKU-100001 at the end of the log?",
                     ["1 unit", "3 units"])
        assert ex["answer"] == "3 units" and "clear_more_than_quarantine" in ex["notes"]
    finally:
        v3.READINGS.clear()
        v3.READINGS.update(saved)


# ---------------------------------------------------------------------------------------------------------------
# Ledger: authorisation lapse at the exact time, guarded transfer, reversal of a fee
# ---------------------------------------------------------------------------------------------------------------
LED_CTX = [("system", "account ledger"), ("currency", "EUR"), ("log exported at", "2026-03-02T18:00:00Z")]
LED_ENTS = [("ACC-1000001", [("holder", "Rhea Dunn"), ("posted balance", "100.00 EUR"), ("pending", "none")])]
LED_EVENTS = [
    ("2026-03-02T08:00:00Z", "E4001", "card-network", "authorise account=ACC-1000001 amount=60.00 EUR"),
    ("2026-03-02T09:00:00Z", "E4002", "payments-hub", "Transfer of 50.00 EUR sent from ACC-1000001."),  # rejected
    ("2026-03-02T10:00:00Z", "E4003", "billing", "Monthly fee of 5.00 EUR charged to ACC-1000001."),
    ("2026-03-02T14:00:00Z", "E4004", "card-network", "post auth=E4001"),  # lapsed exactly at 14:00: nothing
    ("2026-03-02T15:00:00Z", "E4005", "payments-hub", "ACC-1000001 paid out 90.00 EUR by transfer."),
    ("2026-03-02T16:00:00Z", "E4006", "back-office", "Reversal of event E4003 booked."),
]


def test_ledger():
    st = render("ledger", LED_CTX, "2026-03-02T07:00:00Z", LED_ENTS, LED_EVENTS)
    opts = ["10.00 EUR", "5.00 EUR", "-30.00 EUR", "95.00 EUR"]
    assert ask(st, "What is the posted balance of account ACC-1000001 at the end of the log, under the numbered "
                   "rules?", opts) == "10.00 EUR"
    assert ask(st, "Is the available balance of account ACC-1000001 at least 40.00 EUR at 2026-03-02T13:59:00Z?") \
        == "no"  # 95 - 60 pending
    assert ask(st, "Is the available balance of account ACC-1000001 at least 40.00 EUR at 2026-03-02T14:00:00Z?") \
        == "yes"  # the authorisation no longer counts at exactly 14:00
    bands = ["below 50.00 EUR", "50.00 to 99.99 EUR", "100.00 or more EUR"]
    assert ask(st, "Which band does the available balance of account ACC-1000001 fall in at the end of the log?",
               bands) == bands[0]


# ---------------------------------------------------------------------------------------------------------------
# Bookings: hold expiry, confirmation needs an active hold, default minutes
# ---------------------------------------------------------------------------------------------------------------
BKG_CTX = [("system", "desk booking"), ("people", "Tavi Moren, Oska Dunmere"),
           ("log exported at", "2026-03-02T10:00:00Z")]
BKG_ENTS = [("DESK-0001", [("confirmed booking", "none"), ("hold", "none")]),
            ("DESK-0002", [("confirmed booking", "Tavi Moren"), ("hold", "none")])]
BKG_EVENTS = [
    ("2026-03-02T09:00:00Z", "E5001", "booking-app", "hold slot=DESK-0001 user=Tavi Moren minutes=10"),
    ("2026-03-02T09:05:00Z", "E5002", "booking-app", "Oska Dunmere put a 10-minute hold on DESK-0001."),
    ("2026-03-02T09:10:00Z", "E5003", "booking-app", "Booking of DESK-0001 confirmed by Tavi Moren."),
    ("2026-03-02T09:12:00Z", "E5004", "booking-app", "hold slot=DESK-0001 user=Oska Dunmere"),  # default 15 minutes
    ("2026-03-02T09:20:00Z", "E5005", "booking-app", "Oska Dunmere confirmed the booking of DESK-0001."),
    ("2026-03-02T09:30:00Z", "E5006", "booking-app", "cancel slot=DESK-0001 user=Tavi Moren"),
    ("2026-03-02T09:40:00Z", "E5007", "booking-app", "Tavi Moren cancelled the booking of DESK-0002."),
    ("2026-03-02T09:50:00Z", "E5008", "front-desk", "Undo of event E5007 requested."),
]


def test_bookings():
    st = render("bookings", BKG_CTX, "2026-03-02T08:00:00Z", BKG_ENTS, BKG_EVENTS)
    who = ["Tavi Moren", "Oska Dunmere", "nobody"]
    assert ask(st, "Who holds the confirmed booking of DESK-0001 at the end of the log, under the numbered rules?",
               who) == "Oska Dunmere"
    assert ask(st, "Is DESK-0001 free for a new hold at 2026-03-02T09:09:00Z?") == "no"
    assert ask(st, "Is DESK-0001 free for a new hold at 2026-03-02T09:10:00Z?") == "yes"
    assert ask(st, "Does Tavi Moren hold the confirmed booking of DESK-0002 at 2026-03-02T09:45:00Z?") == "no"
    assert ask(st, "Does Tavi Moren hold the confirmed booking of DESK-0002 at the end of the log?") == "yes"
    cnt = ["none of the 2 listed slots", "1 of the 2 listed slots", "2 of the 2 listed slots"]
    assert ask(st, "How many of the listed slots have a confirmed booking at the end of the log?", cnt) == cnt[2]


# ---------------------------------------------------------------------------------------------------------------
# Access: admin-only changes, group rename, old name ignored, deny, grant expiry, revoke
# ---------------------------------------------------------------------------------------------------------------
ACC_CTX = [("system", "access registry"), ("people tracked", "Lio Parn, Mira Solt, Dex Arno"),
           ("log exported at", "2026-03-02T12:00:00Z")]
ACC_ENTS = [("RES-1000001", [("kind", "dashboard"), ("grants", "none")]),
            ("alpha-team", [("members", "Lio Parn")])]
ACC_EVENTS = [
    ("2026-03-02T09:00:00Z", "E6001", "Kara Voss", "grant role=editor to=alpha-team resource=RES-1000001"),
    ("2026-03-02T09:10:00Z", "E6002", "Juno Pell", "Mira Solt was granted viewer access to RES-1000001 for 2 hours."),
    ("2026-03-02T09:20:00Z", "E6003", "Dex Arno", "grant role=owner to=Dex Arno resource=RES-1000001"),
    ("2026-03-02T09:30:00Z", "E6004", "Kara Voss", "Group alpha-team is now called alphaops-team."),
    ("2026-03-02T09:40:00Z", "E6005", "Kara Voss", "add_member user=Dex Arno group=alpha-team"),
    ("2026-03-02T09:50:00Z", "E6006", "Kara Voss", "Kara Voss added Mira Solt to group alphaops-team."),
    ("2026-03-02T10:00:00Z", "E6007", "Juno Pell", "deny user=Lio Parn resource=RES-1000001"),
    ("2026-03-02T11:30:00Z", "E6008", "Kara Voss", "Grant E6001 withdrawn by Kara Voss."),
]


def test_access():
    st = render("access", ACC_CTX, "2026-03-02T08:00:00Z", ACC_ENTS, ACC_EVENTS)
    lv = ["no access", "viewer", "editor", "owner", "blocked by a deny"]
    q = "What access does {} have to RES-1000001 at {}, under the numbered rules?"
    assert ask(st, q.format("Lio Parn", "the end of the log"), lv) == "blocked by a deny"
    assert ask(st, q.format("Lio Parn", "2026-03-02T09:59:00Z"), lv) == "editor"
    assert ask(st, q.format("Mira Solt", "2026-03-02T10:30:00Z"), lv) == "editor"
    assert ask(st, q.format("Mira Solt", "2026-03-02T11:10:00Z"), lv) == "editor"  # own grant ended; group remains
    assert ask(st, q.format("Mira Solt", "the end of the log"), lv) == "no access"
    assert ask(st, q.format("Dex Arno", "the end of the log"), lv) == "no access"  # non-admin; old group name
    assert ask(st, "Can Mira Solt edit RES-1000001 at 2026-03-02T10:30:00Z?") == "yes"
    assert ask(st, "Is Mira Solt shut out of viewing RES-1000001 at the end of the log?") == "yes"
    cnt = ["none of the 3 tracked people", "1 of the 3 tracked people", "2 of the 3 tracked people",
           "3 of the 3 tracked people"]
    assert ask(st, "How many of the tracked people can edit RES-1000001 at 2026-03-02T10:30:00Z?", cnt) == cnt[1]


# ---------------------------------------------------------------------------------------------------------------
# Dialogue: confirmations, same as before, not X, proposals, other people, other bookings
# ---------------------------------------------------------------------------------------------------------------
DLG_CTX = [("system", "rail booking chat"), ("customer", "Sela Brun"), ("log exported at", "2026-03-02T10:30:00Z")]
DLG_ENTS = [("BK-7000001", [("seat", "window"), ("coach", "coach A"), ("meal", "standard meal")])]
DLG_EVENTS = [
    ("2026-03-02T10:00:00Z", "M101", "Customer", "Please set the coach to coach B."),
    ("2026-03-02T10:01:00Z", "M102", "Assistant", "Confirmed: the coach is coach C."),  # not the current value
    ("2026-03-02T10:02:00Z", "M103", "Assistant", "Done - the coach is now coach B."),
    ("2026-03-02T10:03:00Z", "M104", "Customer", "I'd like the coach to be coach D, please."),
    ("2026-03-02T10:04:00Z", "M105", "Customer", "Let's go back to the coach we had before."),  # -> coach B
    ("2026-03-02T10:05:00Z", "M106", "Assistant", "Shall I switch the meal to vegan meal?"),
    ("2026-03-02T10:06:00Z", "M107", "Customer", "Rina says the meal should be no meal."),
    ("2026-03-02T10:07:00Z", "M108", "Customer", "Anything but aisle for the seat."),
    ("2026-03-02T10:08:00Z", "M109", "Customer", "Not the window, please."),  # only table seat remains
    ("2026-03-02T10:09:00Z", "M110", "Customer", "For my other booking BK-7000010, please set the meal to vegan meal."),
    ("2026-03-02T10:10:00Z", "M111", "Customer", "On booking BK-7000001 I want the meal changed to vegetarian meal."),
    ("2026-03-02T10:11:00Z", "M112", "Customer", "On booking BK-7000010 I want the meal changed to no meal."),
]


@pytest.mark.parametrize("fmt", ["log", "chat", "prose", "json"])
def test_dialogue(fmt):
    st = render("dialogue", DLG_CTX, "2026-03-02T09:59:00Z", DLG_ENTS, DLG_EVENTS, fmt=fmt)
    assert ask(st, "What is the seat of booking BK-7000001 at the end of the chat, under the numbered rules?",
               ["window", "aisle", "table seat"]) == "table seat"
    assert ask(st, "Is the coach of booking BK-7000001 coach B at the end of the chat?") == "yes"
    assert ask(st, "Is the coach of booking BK-7000001 coach D at 2026-03-02T10:03:30Z?") == "yes"
    assert ask(st, "Is the meal of booking BK-7000001 something other than vegetarian meal at "
                   "2026-03-02T10:09:30Z?") == "yes"
    assert ask(st, "Under the chat rules, which meal does booking BK-7000001 have at the end of the chat?",
               ["standard meal", "vegetarian meal", "vegan meal", "no meal"]) == "vegetarian meal"


# ---------------------------------------------------------------------------------------------------------------
# Agent tool logs: retries, partial batches, undo, unknown items
# ---------------------------------------------------------------------------------------------------------------
CART_RULES = [r.format(tools="cart.add adds the quantity; cart.remove removes up to the quantity (never below 0); "
                             "cart.set_quantity sets it; the _many and update_many calls do the same per listed item.",
                       only="Only the SKUs listed in the starting state exist; a call part naming anything else "
                            "changes nothing, even when the name looks almost the same.") for r in RULES["agent"]]
FILE_RULES = [r.format(tools="files.move puts the file in the named folder; files.delete moves it to trash; "
                             "files.restore moves it from trash to inbox; the _many and update_many calls do the same "
                             "per listed file.",
                       only="Only the files listed in the starting state exist; a call part naming anything else "
                            "changes nothing, even when the name looks almost the same.") for r in RULES["agent"]]


def test_agent_cart():
    ctx = [("system", "assistant tool log - shopping cart"), ("user", "Pell Idris"),
           ("log exported at", "2026-03-02T11:30:00Z")]
    ents = [("SKU-100001", [("quantity in cart", "1")]), ("SKU-100002", [("quantity in cart", "0")])]
    evs = [
        ("2026-03-02T11:00:00Z", "C101", "assistant", "cart.add(sku=SKU-100001, qty=2) -> error: timeout"),
        ("2026-03-02T11:01:00Z", "C101", "assistant", "cart.add(sku=SKU-100001, qty=2) -> ok"),  # first effect
        ("2026-03-02T11:02:00Z", "C101", "assistant", "cart.add(sku=SKU-100001, qty=2) -> ok"),  # retry: nothing
        ("2026-03-02T11:03:00Z", "C102", "assistant",
         "cart.update_many(remove SKU-100001 x5, add SKU-100002 x2) -> partial: SKU-100001 ok, SKU-100002 failed"),
        ("2026-03-02T11:04:00Z", "C103", "assistant", "cart.undo(call=C102) -> ok"),  # puts back the 3 removed
        ("2026-03-02T11:05:00Z", "C104", "assistant", "cart.set_quantity(sku=SKU-100020, qty=4) -> ok"),
    ]
    st = render("agent", ctx, "2026-03-02T10:59:00Z", ents, evs, rules=CART_RULES)
    u = ["0 units", "1 unit", "3 units", "5 units"]
    assert ask(st, "How many units of SKU-100001 are in the cart at the end of the session, under the numbered "
                   "rules?", u) == "3 units"
    assert ask(st, "Does the cart hold at least 1 of SKU-100001 at 2026-03-02T11:03:30Z?") == "no"
    cnt = ["none of the 2 listed items", "1 of the 2 listed items", "2 of the 2 listed items"]
    assert ask(st, "How many of the listed items are in the cart (quantity 1 or more) at the end of the session?",
               cnt) == cnt[1]


def test_agent_files():
    ctx = [("system", "assistant tool log - file store"), ("user", "Pell Idris"),
           ("log exported at", "2026-03-02T12:30:00Z")]
    ents = [("report-1001.pdf", [("folder", "inbox")]), ("plan-1002.pdf", [("folder", "shared")])]
    evs = [
        ("2026-03-02T12:00:00Z", "C201", "assistant", "files.delete(path=report-1001.pdf) -> ok"),
        ("2026-03-02T12:01:00Z", "C202", "assistant", "files.restore(path=report-1001.pdf) -> ok"),
        ("2026-03-02T12:02:00Z", "C203", "assistant", "files.move_many(report-1001.pdf to archive, plan-1002.pdf to "
                                                      "reports) -> partial: report-1001.pdf failed, plan-1002.pdf ok"),
        ("2026-03-02T12:03:00Z", "C204", "assistant", "files.undo(call=C203) -> ok"),
        ("2026-03-02T12:05:00Z", "C205", "assistant", "files.restore(path=plan-1002.pdf) -> ok"),  # not in trash
    ]
    st = render("agent", ctx, "2026-03-02T11:59:00Z", ents, evs, rules=FILE_RULES)
    f = ["inbox", "shared", "archive", "reports", "trash"]
    assert ask(st, "Which folder is report-1001.pdf in at the end of the session, under the numbered rules?", f) \
        == "inbox"
    assert ask(st, "Which folder is plan-1002.pdf in at 2026-03-02T12:02:30Z, under the numbered rules?", f) \
        == "reports"
    ex = explain(st, "Which folder is plan-1002.pdf in at the end of the session, under the numbered rules?", f)
    assert ex["answer"] == "shared" and "restore_not_in_trash" in ex["notes"]


# ---------------------------------------------------------------------------------------------------------------
# Flags (held out) and docs (held out)
# ---------------------------------------------------------------------------------------------------------------
def test_flags():
    ctx = [("system", "feature flag service"), ("environment asked about", "production"),
           ("log exported at", "2026-03-02T16:00:00Z")]
    ents = [("FF-1001", [("production", "enabled"), ("rollout", "10%"), ("kill switch", "off")]),
            ("Ivo Brandt", [("bucket", "30")]), ("Nel Sarro", [("bucket", "5")])]
    evs = [
        ("2026-03-02T13:00:00Z", "E7001", "Rafe Ostin", "set_rollout flag=FF-1001 env=production percent=50 "
                                                        "change=CHG-9999"),
        ("2026-03-02T13:10:00Z", "E7002", "Rafe Ostin", "Rollout of FF-1001 in staging is now 100% per CHG-1111."),
        ("2026-03-02T13:20:00Z", "E7003", "Rafe Ostin", "Rafe Ostin set the production rollout of FF-1001 to 50% "
                                                        "(CHG-1111)."),
        ("2026-03-02T13:30:00Z", "E7004", "Rafe Ostin", "Temporary override: FF-1001 off for Ivo Brandt, 24 hours."),
        ("2026-03-02T13:40:00Z", "E7005", "Rafe Ostin", "override flag=FF-1001 user=Ivo Brandt value=on hours=1"),
        ("2026-03-02T14:00:00Z", "E7006", "Rafe Ostin", "kill flag=FF-1001"),
        ("2026-03-02T15:00:00Z", "E7007", "Rafe Ostin", "Emergency stop on FF-1001 lifted under CHG-2222 by Rafe "
                                                        "Ostin."),
    ]
    st = render("flags", ctx, "2026-03-02T12:00:00Z", ents, evs)
    assert ask(st, "What is the production rollout percentage of FF-1001 at the end of the log, under the numbered "
                   "rules?", ["10%", "50%", "100%"]) == "50%"
    assert ask(st, "Is FF-1001 on for Nel Sarro in production at 2026-03-02T14:30:00Z?") == "no"  # kill switch
    assert ask(st, "Is FF-1001 on for Nel Sarro in production at the end of the log?") == "yes"
    assert ask(st, "Is FF-1001 on for Ivo Brandt in production at 2026-03-02T13:50:00Z?") == "yes"
    # at the end the 1-hour 'on' override has ended; the 24-hour 'off' one still lasts (this solver's reading)
    assert ask(st, "Is FF-1001 on for Ivo Brandt in production at the end of the log?") == "no"


def test_docs():
    ctx = [("system", "document store"), ("editors", "Ben Kerr, Ada Fenn"), ("log exported at", "2026-03-02T11:00:00Z")]
    ents = [("DOC-100001", [("version 1 content", "final wording"), ("lock", "none")])]
    evs = [
        ("2026-03-02T09:00:00Z", "E8001", "Ben Kerr", "lock doc=DOC-100001"),
        ("2026-03-02T09:10:00Z", "E8002", "Ada Fenn", 'save doc=DOC-100001 content="summer edition"'),  # locked
        ("2026-03-02T09:20:00Z", "E8003", "Ben Kerr", 'Ben Kerr saved a new version of DOC-100001: "pricing draft".'),
        ("2026-03-02T09:30:00Z", "E8004", "Pia Lund", "approve doc=DOC-100001 version=3"),  # no version 3 yet
        ("2026-03-02T10:00:00Z", "E8005", "Ada Fenn", 'save doc=DOC-100001 content="board version"'),  # lock over
        ("2026-03-02T10:10:00Z", "E8006", "Pia Lund", "Pia Lund approved version 3 of DOC-100001."),
        ("2026-03-02T10:20:00Z", "E8007", "Ada Fenn", "restore doc=DOC-100001 version=2"),
    ]
    st = render("docs", ctx, "2026-03-02T08:00:00Z", ents, evs)
    n = ["1 version", "2 versions", "3 versions", "4 or more versions"]
    assert ask(st, "How many versions does DOC-100001 have at the end of the log?", n) == n[3]
    assert ask(st, "Is the current version of DOC-100001 approved at 2026-03-02T10:15:00Z?") == "yes"
    assert ask(st, "Is the current version of DOC-100001 approved at the end of the log?") == "no"
    assert ask(st, 'Is the current version of DOC-100001 the "pricing draft" content at the end of the log?') == "yes"


# ---------------------------------------------------------------------------------------------------------------
# Refusals and independence
# ---------------------------------------------------------------------------------------------------------------
def test_unknown_question_or_line_is_undefined_not_guessed():
    st = render("orders", ORD_CTX, ORD_START, ORD_ENTS, ORD_EVENTS)
    assert ask(st, "Is order SO-1111111 happy at the end of the log?") is v3.UNDEFINED
    bad = ORD_EVENTS + [("2026-03-02T16:30:00Z", "E1099", "warehouse", "Order SO-1111111 was teleported.")]
    st2 = render("orders", ORD_CTX, ORD_START, ORD_ENTS, bad)
    assert ask(st2, "Can order SO-1111111 still be cancelled at the end of the log?") is v3.UNDEFINED


def test_module_never_imports_the_generator():
    src = (GEN3 / "v3_state_track.py").read_text()
    for name in ("gen3_state_track", "gen3_state_track_sim"):
        assert f"import {name}" not in src and f"from {name}" not in src
    assert "meta" not in src.split("def decide2_row")[1].split("def explain_row")[0]
