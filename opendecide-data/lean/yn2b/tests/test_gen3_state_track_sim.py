"""F3 simulator semantics on hand-built worlds (expected values worked out by hand from each machine's rules text).

These fix what every rule means (guards, redeliveries, reverts, expiries at the exact boundary, look-alike ids,
business-hour SLAs across a weekend, a holiday and a DST change, dialogue references, partial tool batches), and that
each named shortcut solver really gets the trap wrong. CPU only; nothing is written.
"""
from __future__ import annotations

import random
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402
import gen3_state_track_sim as sim  # noqa: E402
from gen3_state_track_sim import Ev, Query, World  # noqa: E402

UTC = timezone.utc
T0 = datetime(2026, 3, 2, 8, 0, tzinfo=UTC)  # a Monday


def at(minutes):
    return T0 + timedelta(minutes=minutes)


def world(M, ents, target, evs, t_q=None, params=None, decoys=None, record=None):
    """evs: [(minute, eid, src, kind, ent, args)]"""
    events = [Ev(i, eid, at(m), src, kind, ent, dict(a)) for i, (m, eid, src, kind, ent, a) in enumerate(evs)]
    t_end = max([e.ts for e in events] + [T0]) + timedelta(minutes=5)
    tq = t_q if t_q is not None else t_end
    return World(M.name, T0, t_end, tq, tq == t_end, ents, target, decoys or {}, events, params or {}, "t", [], {},
                 "iso", [date(2025, 6, 1)] * 16, record)


def obs(M, W, flags=(), display=None):
    return sim.observe(M, W, frozenset(flags), display)


# ------------------------------------------------------------------------------------------------ orders
O = sim.MACHINES["orders"]


def test_orders_guard_resend_revert_decoy():
    ents = {"SO-4417203": {"status": "created", "customer": "A"}, "SO-4417230": {"status": "created", "customer": "B"}}
    evs = [(1, "E1111", "payments", "pay", "SO-4417203", {}),
           (2, "E1112", "carrier-api", "ship", "SO-4417203", {}),     # guard: not packed yet -> rejected
           (3, "E1113", "warehouse", "pack", "SO-4417203", {}),
           (4, "E1111", "payments", "pay", "SO-4417203", {}),          # redelivery of E1111: nothing
           (5, "E1114", "carrier-api", "ship", "SO-4417203", {}),
           (6, "E1115", "ops-console", "revert", "SO-4417203", {"of": "E1114"}),  # back to packed
           (7, "E1116", "support-desk", "cancel", "SO-4417230", {})]   # the look-alike order (a listed order)
    W = world(O, ents, "SO-4417203", evs, decoys={"SO-4417230": "SO-4417203"})
    k = ("status", "SO-4417203")
    assert obs(O, W)[k] == "packed"
    assert obs(O, W)[("status", "SO-4417230")] == "cancelled"
    _, out = sim.replay(O, W)
    assert out[1] == "guard" and out[3] == "dup" and out[5] == "ok"
    # the fuzzy-id solver cancels the queried order (cancel is allowed from packed)
    assert obs(O, W, ["fuzzy"])[k] == "cancelled"
    # last_event_wins: the last step named for SO-4417203 is ship (the revert names no status)
    assert O.last_event(W, k) == "shipped"
    q = Query("yn", "eq", k, "packed")
    assert sim.decide(O, W, q)[0] == "yes"
    assert sim.decide(O, W, Query("yn", "cancel", k))[0] == "yes"


def test_orders_revert_of_rejected_event_and_display_order():
    ents = {"SO-5512345": {"status": "created", "customer": "A"}}
    evs = [(1, "E2001", "payments", "pay", "SO-5512345", {}),
           (2, "E2002", "warehouse", "pack", "SO-5512345", {}),
           (3, "E2003", "carrier-api", "deliver", "SO-5512345", {}),                 # rejected (not shipped)
           (4, "E2004", "ops-console", "revert", "SO-5512345", {"of": "E2003"})]      # reverts nothing
    W = world(O, ents, "SO-5512345", evs)
    k = ("status", "SO-5512345")
    assert obs(O, W)[k] == "packed"
    newest = [3, 2, 1, 0]
    # listed newest first, the display-order solver applies pack before pay: pack rejected, then pay -> paid
    assert obs(O, W, ["display"], newest)[k] == "paid"
    # ignore_guards: deliver goes through, so the revert of E2003 now takes effect and restores packed
    assert obs(O, W, ["guards"])[k] == "packed"


def test_orders_ignore_guards_with_revert_restores():
    ents = {"SO-5512345": {"status": "created", "customer": "A"}}
    evs = [(1, "E2001", "payments", "pay", "SO-5512345", {}),
           (3, "E2003", "carrier-api", "deliver", "SO-5512345", {}),
           (4, "E2004", "ops-console", "revert", "SO-5512345", {"of": "E2003"})]
    W = world(O, ents, "SO-5512345", evs)
    k = ("status", "SO-5512345")
    assert obs(O, W)[k] == "paid"
    assert obs(O, W, ["guards"])[k] == "paid"  # delivered, then reverted to paid


def test_orders_query_time_counts_events_at_or_before():
    ents = {"SO-5512345": {"status": "created", "customer": "A"}}
    evs = [(10, "E2001", "payments", "pay", "SO-5512345", {}), (20, "E2002", "warehouse", "pack", "SO-5512345", {})]
    W = world(O, ents, "SO-5512345", evs, t_q=at(20))
    assert obs(O, W)[("status", "SO-5512345")] == "packed"  # an event exactly at the stated time counts
    W = world(O, ents, "SO-5512345", evs, t_q=at(19))
    assert obs(O, W)[("status", "SO-5512345")] == "paid"


# ------------------------------------------------------------------------------------------------ tickets (SLA)
TK = sim.MACHINES["tickets"]


def tickets_world(zone, opened, sla, holidays, evs, t_q):
    ents = {"TCK-441720": {"status": "new", "owner": None}}
    P = {"roster": ["Ana Bel", "Cor Dan"], "outsiders": ["Eve Fox"], "zone": zone, "holidays": holidays, "sla": sla,
         "opened": opened}
    events = [Ev(i, eid, ts, src, kind, "TCK-441720", dict(a)) for i, (ts, eid, src, kind, a) in enumerate(evs)]
    W = World("tickets", opened, t_q, t_q, True, ents, "TCK-441720", {}, events, P, "t", [], {}, "iso",
              [date(2025, 6, 1)] * 16)
    return W


def test_tickets_due_over_weekend_and_holiday():
    # opened Friday 2026-03-06 15:00 Berlin (14:00 UTC), 4 business hours: 2 h on Friday (to 17:00), Monday
    # 2026-03-09 is a listed holiday, so the remaining 2 h run Tuesday 09:00-11:00 Berlin = 08:00-10:00 UTC.
    opened = datetime(2026, 3, 6, 14, 0, tzinfo=UTC)
    W = tickets_world("Europe/Berlin", opened, 4, [date(2026, 3, 9)], [], datetime(2026, 3, 11, 12, 0, tzinfo=UTC))
    assert TK.due(W) == datetime(2026, 3, 10, 10, 0, tzinfo=UTC)
    # resolved Tuesday 12:30 Berlin (11:30 UTC): 1.5 business hours late -> overdue, level 1
    evs = [(opened + timedelta(minutes=5), "E1", "dispatch", "assign", {"who": "Ana Bel"}),
           (opened + timedelta(minutes=9), "E2", "agent-console", "start", {}),
           (datetime(2026, 3, 10, 11, 30, tzinfo=UTC), "E3", "agent-console", "resolve", {})]
    W = tickets_world("Europe/Berlin", opened, 4, [date(2026, 3, 9)], evs, datetime(2026, 3, 11, 12, 0, tzinfo=UTC))
    o = obs(TK, W)
    assert o[("overdue", "TCK-441720")] is True and o[("level", "TCK-441720")] == 1
    assert o[("owner", "TCK-441720")] == "Ana Bel"
    # resolved exactly at the due time: on time, level 0
    evs[2] = (datetime(2026, 3, 10, 10, 0, tzinfo=UTC), "E3", "agent-console", "resolve", {})
    W = tickets_world("Europe/Berlin", opened, 4, [date(2026, 3, 9)], evs, datetime(2026, 3, 11, 12, 0, tzinfo=UTC))
    assert obs(TK, W)[("overdue", "TCK-441720")] is False and obs(TK, W)[("level", "TCK-441720")] == 0


def test_tickets_dst_and_guards():
    # New York switches to DST on Sunday 2026-03-08: Friday business hours are 14:00-22:00 UTC, Monday's 13:00-21:00.
    opened = datetime(2026, 3, 6, 20, 0, tzinfo=UTC)  # Friday 15:00 New York
    W = tickets_world("America/New_York", opened, 8, [], [], datetime(2026, 3, 12, 0, 0, tzinfo=UTC))
    # 2 h on Friday, 6 h on Monday from 13:00 UTC -> due Monday 19:00 UTC
    assert TK.due(W) == datetime(2026, 3, 9, 19, 0, tzinfo=UTC)
    evs = [(opened + timedelta(minutes=1), "E1", "dispatch", "assign", {"who": "Eve Fox"}),  # not on the roster
           (opened + timedelta(minutes=2), "E2", "agent-console", "resolve", {})]             # new -> rejected
    W = tickets_world("America/New_York", opened, 8, [], evs, datetime(2026, 3, 12, 0, 0, tzinfo=UTC))
    o = obs(TK, W)
    assert o[("owner", "TCK-441720")] == "nobody" and o[("status", "TCK-441720")] == "new"
    assert o[("overdue", "TCK-441720")] is True
    # Monday 19:00 UTC to Wednesday 24:00 UTC: 2 h Mon + 8 h Tue + 8 h Wed = 18 business hours -> level 4
    assert o[("level", "TCK-441720")] == 4
    g = obs(TK, W, ["guards"])
    assert g[("owner", "TCK-441720")] == "Eve Fox" and g[("overdue", "TCK-441720")] is False


# ------------------------------------------------------------------------------------------------ access
AC = sim.MACHINES["access"]


def access_world(evs, t_q=None, members=None):
    P = {"users": ["Ana Bel", "Cor Dan", "Eve Fox"], "admins": ["Adm One", "Adm Two"], "outsider": "Out Sider",
         "groups": ["kora-team"], "members": members or {"kora-team": ["Cor Dan"]}, "user": "Ana Bel", "renamed": {}}
    ents = {"RES-4417203": {"kind": "repository"}}
    return world(AC, ents, "RES-4417203", evs, t_q=t_q, params=P, decoys={"RES-4417230": "RES-4417203"})


def test_access_expiry_boundary_deny_rename():
    R = "RES-4417203"
    evs = [(0, "E1", "Adm One", "grant", R, {"role": "editor", "to": "Ana Bel", "hours": 2}),
           (5, "E2", "Out Sider", "grant", R, {"role": "owner", "to": "Ana Bel", "hours": None}),  # not an admin
           (10, "E3", "Adm Two", "grant", R, {"role": "viewer", "to": "kora-team", "hours": None}),
           (15, "E4", "Adm One", "join", None, {"to": "Eve Fox", "g": "kora-team"}),
           (20, "E5", "Adm One", "rename", None, {"g": "kora-team", "g2": "kora-core-team"}),
           (25, "E6", "Adm One", "grant", R, {"role": "owner", "to": "kora-team", "hours": None}),  # old name: nothing
           (30, "E7", "Adm One", "deny", R, {"to": "Cor Dan"}),
           (35, "E8", "Adm One", "grant", "RES-4417230", {"role": "owner", "to": "Ana Bel", "hours": None})]
    W = access_world(evs, t_q=at(120))  # exactly when Ana's timed grant ends: it no longer counts
    o = obs(AC, W)
    assert o[("access", "Ana Bel")] == "no access"
    assert o[("access", "Eve Fox")] == "viewer"          # member via the renamed group
    assert o[("access", "Cor Dan")] == "blocked by a deny"
    assert obs(AC, W, ["expiry"])[("access", "Ana Bel")] == "editor"
    assert obs(AC, W, ["guards"])[("access", "Ana Bel")] == "owner"
    assert obs(AC, W, ["fuzzy"])[("access", "Ana Bel")] == "owner"
    W2 = access_world(evs, t_q=at(119))
    assert obs(AC, W2)[("access", "Ana Bel")] == "editor"
    assert sim.decide(AC, W2, Query("yn", "edit", ("access", "Ana Bel")))[0] == "yes"
    assert sim.decide(AC, W, Query("yn", "view", ("access", "Eve Fox")))[0] == "yes"


def test_access_redelivered_timed_grant_counts_once():
    R = "RES-4417203"
    evs = [(0, "E1", "Adm One", "grant", R, {"role": "editor", "to": "Ana Bel", "hours": 1}),
           (50, "E1", "Adm One", "grant", R, {"role": "editor", "to": "Ana Bel", "hours": 1})]
    W = access_world(evs, t_q=at(90))
    assert obs(AC, W)[("access", "Ana Bel")] == "no access"
    assert obs(AC, W, ["resend"])[("access", "Ana Bel")] == "editor"


# ------------------------------------------------------------------------------------------------ inventory
IV = sim.MACHINES["inventory"]


def test_inventory_holds_quarantine_count_reversal():
    S = "SKU-441720"
    ents = {S: {"on_hand": 5, "item": "valve"}}
    evs = [(0, "E1", "receiving", "receive", S, {"q": 4}),                 # on hand 9
           (5, "E2", "sales-orders", "hold", S, {"q": 3, "m": 30}),        # hold until minute 35
           (10, "E3", "picking", "ship", S, {"q": 7}),                     # available 6 -> rejected
           (15, "E4", "quality", "quarantine", S, {"q": 2}),               # available 9-3-2 = 4
           (20, "E5", "cycle-count", "count", S, {"q": 8}),                # on hand 8 -> available 3
           (25, "E1", "receiving", "receive", S, {"q": 4}),                # redelivery: nothing
           (40, "E6", "ops-console", "revert", S, {"of": "E4"})]           # quarantine undone
    W = world(IV, ents, S, evs, t_q=at(35))  # the hold ends exactly at 35: it no longer counts
    assert obs(IV, W)[("avail", S)] == 6          # on hand 8, quarantine 2 (revert at 40 is after the query time)
    assert obs(IV, W, ["expiry"])[("avail", S)] == 3
    assert obs(IV, W, ["resend"])[("avail", S)] == 10  # the redelivered receive counted again (after the count)
    assert obs(IV, W, ["guards"])[("avail", S)] == 6   # the rejected ship happened before the count overwrote on hand
    W2 = world(IV, ents, S, evs)
    assert obs(IV, W2)[("avail", S)] == 8
    assert sim.decide(IV, W2, Query("yn", "ge", ("avail", S), 8))[0] == "yes"
    assert sim.decide(IV, W2, Query("yn", "ge", ("avail", S), 9))[0] == "no"


def test_inventory_reversal_never_below_zero():
    S = "SKU-441720"
    ents = {S: {"on_hand": 0, "item": "valve"}}
    evs = [(0, "E1", "receiving", "receive", S, {"q": 4}), (5, "E2", "picking", "ship", S, {"q": 4}),
           (10, "E3", "ops-console", "revert", S, {"of": "E1"})]
    W = world(IV, ents, S, evs)
    assert obs(IV, W)[("avail", S)] == 0


# ------------------------------------------------------------------------------------------------ bookings
BK = sim.MACHINES["bookings"]


def test_bookings_hold_expiry_and_holder():
    D = "DESK-4417"
    P = {"users": ["Ana Bel", "Cor Dan", "Eve Fox"], "user": "Ana Bel", "hold_default": 10}
    ents = {D: {"booked": None}}
    evs = [(0, "E1", "booking-app", "hold", D, {"u": "Ana Bel", "m": 10}),
           (4, "E2", "booking-app", "confirm", D, {"u": "Cor Dan"}),       # not the holder
           (10, "E3", "booking-app", "confirm", D, {"u": "Ana Bel"})]      # hold ended at minute 10 exactly
    W = world(BK, ents, D, evs, params=P)
    o = obs(BK, W)
    assert o[("booked", D)] == "nobody" and o[("free", D)] is True
    assert obs(BK, W, ["expiry"])[("booked", D)] == "Ana Bel"
    assert obs(BK, W, ["guards"])[("booked", D)] == "Ana Bel"  # both confirmations go through; Ana's is last
    assert sim.decide(BK, W, Query("yn", "booked", ("booked", D)))[0] == "no"


# ------------------------------------------------------------------------------------------------ ledger
LG = sim.MACHINES["ledger"]


def test_ledger_auth_lapse_post_and_reversal():
    A = "ACC-4417203"
    P = {"cur": "EUR", "lapse": 6}
    ents = {A: {"posted": 100000, "holder": "Ana Bel"}}
    evs = [(0, "E1", "card-network", "auth", A, {"c": 30000}),       # pending, lapses at minute 360
           (10, "E2", "core-banking", "deposit", A, {"c": 5050}),
           (20, "E3", "payments-hub", "transfer", A, {"c": 80000}),   # available 1,050.50 - 300.00 = 755.50 -> rejected
           (30, "E2", "core-banking", "deposit", A, {"c": 5050}),     # redelivery
           (400, "E4", "card-network", "post", A, {"of": "E1"}),      # lapsed -> rejected
           (410, "E5", "back-office", "revert", A, {"of": "E2"})]     # deposit taken off again
    W = world(LG, ents, A, evs, params=P)
    o = obs(LG, W)
    assert o[("posted", A)] == 100000 and o[("avail", A)] == 100000
    W2 = world(LG, ents, A, evs, params=P, t_q=at(360))  # exactly at the lapse time: no longer pending
    assert obs(LG, W2)[("avail", A)] == 105050
    W3 = world(LG, ents, A, evs, params=P, t_q=at(359))
    assert obs(LG, W3)[("avail", A)] == 75050
    assert obs(LG, W, ["expiry"])[("posted", A)] == 70000  # the post goes through when nothing lapses
    assert sim.decide(LG, W3, Query("yn", "ge", ("avail", A), 75050))[0] == "yes"
    assert sim.decide(LG, W3, Query("yn", "ge", ("avail", A), 75051))[0] == "no"


# ------------------------------------------------------------------------------------------------ dialogue
DG = sim.MACHINES["dialogue"]


def dialogue_world(evs):
    P = {"schema": "rail", "slots": {k: list(v) for k, v in DG.SCHEMAS["rail"].items()}, "qslot": "seat",
         "customer": "Ana Bel", "colleague": "Cor"}
    ents = {"BK-4417203": {"schema": "rail", "confirmed": {"seat": "aisle", "coach": "coach B",
                                                           "meal": "standard meal"}}}
    return world(DG, ents, "BK-4417203", evs, params=P, decoys={"BK-4417230": "BK-4417203"})


def test_dialogue_references():
    B = "BK-4417203"
    evs = [(0, "M101", "Customer", "set", B, {"slot": "seat", "v": "window"}),
           (1, "M102", "Assistant", "confirm", B, {"slot": "seat", "v": "table seat"}),   # not the current value
           (2, "M103", "Assistant", "propose", B, {"slot": "seat", "v": "table seat"}),
           (3, "M104", "Customer", "decline", B, {"slot": "seat"}),
           (4, "M105", "Customer", "third", B, {"slot": "seat", "v": "table seat", "who": "Cor"}),
           (5, "M106", "Customer", "same", B, {"slot": "seat"}),                          # back to aisle
           (6, "M107", "Customer", "oset", "BK-4417230", {"slot": "seat", "v": "window"})]
    W = dialogue_world(evs)
    k = ("slot", "seat")
    assert obs(DG, W)[k] == "aisle"
    assert obs(DG, W, ["fuzzy"])[k] == "window"
    assert DG.last_event(W, k) == "window"
    assert sim.decide(DG, W, Query("yn", "eq", k, "aisle"))[0] == "yes"


def test_dialogue_not_x_open_value_is_undefined():
    B = "BK-4417203"
    evs = [(0, "M101", "Customer", "set", B, {"slot": "seat", "v": "window"}),
           (1, "M102", "Customer", "not", B, {"slot": "seat", "v": "window"})]   # aisle and table seat remain: open
    W = dialogue_world(evs)
    assert obs(DG, W)[("slot", "seat")] is None
    assert mv.is_undefined(sim.decide(DG, W, Query("value", "slot", ("slot", "seat")))[0])
    evs.append((2, "M103", "Customer", "not", B, {"slot": "seat", "v": "table seat"}))  # one left: aisle
    W = dialogue_world(evs)
    assert obs(DG, W)[("slot", "seat")] == "aisle"


# ------------------------------------------------------------------------------------------------ agent
AG = sim.MACHINES["agent"]


def test_agent_partial_batch_retry_undo():
    P = {"dom": "cart", "user": "Ana Bel"}
    ents = {"SKU-441720": {"qty": 0}, "SKU-518833": {"qty": 1}}
    evs = [(0, "C101", "assistant", "call", "SKU-441720",
            {"parts": [("SKU-441720", "add", 2, True), ("SKU-518833", "add", 1, False)]}),   # partial
           (1, "C101", "assistant", "call", "SKU-441720",
            {"parts": [("SKU-441720", "add", 2, True), ("SKU-518833", "add", 1, False)]}),   # retry: nothing
           (2, "C102", "assistant", "call", "SKU-518833", {"parts": [("SKU-518833", "remove", 5, True)]}),
           (3, "C103", "assistant", "revert", "SKU-518833", {"of": "C102"})]                  # undo: 1 back
    W = world(AG, ents, "SKU-441720", evs, params=P)
    o = obs(AG, W)
    assert o[("qty", "SKU-441720")] == 2 and o[("qty", "SKU-518833")] == 1
    assert obs(AG, W, ["resend"])[("qty", "SKU-441720")] == 4
    assert obs(AG, W, ["guards"])[("qty", "SKU-518833")] == 2
    _, out = sim.replay(AG, W)
    assert AG.guard_present(W, out)


# ------------------------------------------------------------------------------------------------ flags (held out)
FL = sim.MACHINES["flags"]


def test_flags_ticket_kill_override():
    F = "FF-4417"
    P = {"users": ["Ana Bel", "Cor Dan", "Eve Fox"], "buckets": {"Ana Bel": 30, "Cor Dan": 70, "Eve Fox": 10},
         "user": "Ana Bel", "eng": ["En One"], "chg_ok": ["CHG-1234"], "chg_bad": "CHG-9999"}
    ents = {F: {"enabled": True, "rollout": 25}}
    evs = [(0, "E1", "En One", "rollout", F, {"env": "production", "p": 50, "chg": "CHG-9999"}),  # bad ticket
           (5, "E2", "En One", "rollout", F, {"env": "staging", "p": 100, "chg": "CHG-1234"}),     # staging only
           (10, "E3", "En One", "override", F, {"u": "Ana Bel", "on": True, "h": 1})]
    W = world(FL, ents, F, evs, params=P, t_q=at(70))  # the override ended at minute 70 exactly
    o = obs(FL, W)
    assert o[("on", "Ana Bel")] is False and o[("rollout", F)] == 25   # bucket 30 is not below 25
    assert obs(FL, W, ["expiry"])[("on", "Ana Bel")] is True
    assert obs(FL, W, ["guards"])[("on", "Ana Bel")] is True           # rollout 50 would include bucket 30
    assert o[("on", "Eve Fox")] is True


# ------------------------------------------------------------------------------------------------ docs (held out)
DC = sim.MACHINES["docs"]


def test_docs_lock_expiry_restore_approval():
    D = "DOC-441720"
    P = {"editors": ["Ed One", "Ed Two", "Ed Three"], "approvers": ["Ed Two", "Ap Four"], "lock_min": 60}
    ents = {D: {"v1": "pricing draft"}}
    evs = [(0, "E1", "Ed One", "lock", D, {}),
           (10, "E2", "Ed Two", "save", D, {"lab": "board version"}),       # locked by Ed One -> rejected
           (20, "E3", "Ed One", "save", D, {"lab": "short summary"}),       # v2
           (60, "E4", "Ed Two", "save", D, {"lab": "final wording"}),       # the lock ended at 60 -> v3
           (70, "E5", "Ed Three", "restore", D, {"k": 2}),                  # v4 = short summary
           (80, "E6", "Ed Two", "approve", D, {"k": 4}),
           (90, "E7", "Ed One", "approve", D, {"k": 3})]                   # not an approver
    W = world(DC, ents, D, evs, params=P)
    o = obs(DC, W)
    assert o[("content", D)] == "short summary" and o[("nvers", D)] == 4 and o[("approved", D)] is True
    assert obs(DC, W, ["expiry"])[("nvers", D)] == 2   # the lock never ends: the save and the restore are rejected
    assert DC.level(W, Query("score", "nvers", ("nvers", D)), o) == 3


# ------------------------------------------------------------------------------------------------ sampler + shortcuts
def test_sampled_worlds_are_deterministic_and_self_consistent():
    pool = mv.NamePool("train")
    for name, M in sim.MACHINES.items():
        for i in range(12):
            spec = sim.Spec(("easy", "standard", "judge", "hard")[i % 4], 4 + 3 * i, {"guard": 1, "resend": 1,
                                                                                     "decoy": 1,
                                                                                     "after": i % 2},
                            at_end=i % 2 == 0, lang=0.5, mixed=i % 3 == 0)
            try:
                a = sim.sample_world(M, random.Random(i), pool, spec)
            except mv.Reject:
                continue
            b = sim.sample_world(M, random.Random(i), pool, spec)
            assert [(e.eid, e.ts, e.kind, e.ent, e.a) for e in a.events] == \
                   [(e.eid, e.ts, e.kind, e.ent, e.a) for e in b.events]
            assert len({e.ts for e in a.events}) == len(a.events)          # unique times: order recoverable
            assert sim.observe(M, a) == sim.observe(M, b)
            if not a.at_end:
                assert any(e.ts > a.t_q for e in a.events) and all(e.ts != a.t_q for e in a.events)


def test_shortcut_answer_abstains_without_its_trap():
    O_ = sim.MACHINES["orders"]
    ents = {"SO-5512345": {"status": "created", "customer": "A"}}
    W = world(O_, ents, "SO-5512345", [(1, "E2001", "payments", "pay", "SO-5512345", {})])
    q = Query("value", "status", ("status", "SO-5512345"))
    ip = sim.in_play(O_, W, [0])
    assert not any(ip.values())
    assert all(sim.shortcut_answer(O_, W, q, n, [0], ip) is None for n in sim.SHORTCUT_NAMES)
