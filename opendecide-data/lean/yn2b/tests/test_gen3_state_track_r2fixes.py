"""F3 generator fixes from reviewer R2 (gen3_state_track.py: MACH, surface_issues, mutations).

Hand-built worlds pin each fix (expected values worked out by hand from the rule texts), then a small real build is
re-derived by builder B's decide2 (golden_src/gen3/v3_state_track.py), which must agree on every row. CPU only;
nothing is written outside pytest's tmp_path.
"""
from __future__ import annotations

import random
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402
import gen3_state_track as g  # noqa: E402
import gen3_state_track_sim as sim  # noqa: E402
from gen3_state_track_sim import Ev, World  # noqa: E402

UTC = timezone.utc
T0 = datetime(2026, 3, 2, 8, 0, tzinfo=UTC)  # a Monday


def at(minutes):
    return T0 + timedelta(minutes=minutes)


def world(M, ents, target, evs, t_q=None, params=None, decoys=None):
    """evs: [(minute, eid, src, kind, ent, args)] or with a 7th item, the language template index lt."""
    events = []
    for i, ev in enumerate(evs):
        m, eid, src, kind, ent, a = ev[:6]
        events.append(Ev(i, eid, at(m), src, kind, ent, dict(a), "l" if len(ev) > 6 else "s",
                         ev[6] if len(ev) > 6 else 0))
    t_end = max([e.ts for e in events] + [T0]) + timedelta(minutes=5)
    tq = t_q if t_q is not None else t_end
    return World(M.name, T0, t_end, tq, tq == t_end, ents, target, decoys or {}, events, params or {}, "t", [], {},
                 "iso", [date(2025, 6, 1)] * 16)


# ------------------------------------------------------------------------------------------------ machines in use
def test_generator_uses_the_fixed_machines():
    assert set(g.MACH) == set(sim.MACHINES)
    for name in ("tickets", "flags", "inventory", "bookings", "dialogue", "docs"):
        assert type(g.MACH[name]).__name__.endswith("R2") and isinstance(g.MACH[name], type(sim.MACHINES[name]))
    src = Path(g.__file__).read_text()
    assert "sim.MACHINES[" not in src  # every label, twin and latent of the build comes from MACH


# ------------------------------------------------------------------------------------------------ tickets
TCK = "TCK-441720"


def _tickets(evs, t_q=None):
    P = {"roster": ["Ana Bel", "Cor Dan"], "outsiders": ["Out Sider"], "zone": "Europe/London", "holidays": [],
         "sla": 8, "opened": T0}
    return world(g.MACH["tickets"], {TCK: {"status": "new", "owner": None}}, TCK, evs, t_q=t_q, params=P)


def test_reassignment_records_only_the_owner_and_its_revert_keeps_the_status():
    evs = [(1, "E1", "dispatch", "assign", TCK, {"who": "Ana Bel"}),
           (2, "E2", "agent-console", "start", TCK, {}),
           (3, "E3", "dispatch", "assign", TCK, {"who": "Cor Dan"}),   # in_progress: changes the owner only
           (4, "E4", "agent-console", "resolve", TCK, {}),
           (5, "E5", "qa-bot", "close", TCK, {}),
           (6, "E6", "ops-console", "revert", TCK, {"of": "E3"}),      # owner back to Ana Bel; status stays closed
           (7, "E7", "dispatch", "assign", TCK, {"who": "Cor Dan"})]   # closed ticket: rejected
    W = _tickets(evs)
    o = sim.observe(g.MACH["tickets"], W)
    assert o[("status", TCK)] == "closed" and o[("owner", TCK)] == "Ana Bel"
    _, out = sim.replay(g.MACH["tickets"], W)
    assert out[6] == "guard"
    # the pre-review simulator restored the unchanged status too, so the later assignment went through
    old = sim.observe(sim.MACHINES["tickets"], W)
    assert old[("status", TCK)] == "in_progress" and old[("owner", TCK)] == "Cor Dan"


def test_first_assignment_still_records_the_status():
    st = g.MACH["tickets"].init(_tickets([]))
    e = Ev(0, "E1", at(1), "dispatch", "assign", TCK, {"who": "Ana Bel"})
    u = g.MACH["tickets"].apply(st, e, TCK, _tickets([]), frozenset())
    assert u == [("set", TCK, "owner", None), ("set", TCK, "status", "new")]
    assert st[TCK]["status"] == "assigned"


def test_revert_of_first_resolve_is_stated_and_clears_it():
    evs = [(1, "E1", "dispatch", "assign", TCK, {"who": "Ana Bel"}),
           (2, "E2", "agent-console", "start", TCK, {}),
           (3, "E3", "agent-console", "resolve", TCK, {}),
           (4, "E4", "mail-gateway", "reopen", TCK, {}),
           (5, "E5", "agent-console", "resolve", TCK, {}),             # not the first resolution
           (6, "E6", "ops-console", "revert", TCK, {"of": "E3"})]
    W = _tickets(evs)
    st, _ = sim.replay(g.MACH["tickets"], W)
    assert st[TCK]["res"] is None and st[TCK]["status"] == "in_progress"
    assert g.TicketsR2.RES_REVERT in g.MACH["tickets"].rules(W)


# ------------------------------------------------------------------------------------------------ flags
FF = "FF-4417"
FP = {"users": ["Ana Bel", "Cor Dan", "Eve Fox"], "buckets": {"Ana Bel": 99, "Cor Dan": 70, "Eve Fox": 10},
      "user": "Ana Bel", "eng": ["En One"], "chg_ok": ["CHG-1234", "CHG-2345"], "chg_bad": "CHG-9999"}


def _flags(evs, t_q):
    return world(g.MACH["flags"], {FF: {"enabled": True, "rollout": 0}}, FF, evs, t_q=t_q, params=dict(FP))


OVS = [(0, "E1", "En One", "override", FF, {"u": "Ana Bel", "on": True, "h": 24}),
       (60, "E2", "En One", "override", FF, {"u": "Ana Bel", "on": False, "h": 1})]


@pytest.mark.parametrize("minute,expect,old", [(30, True, True), (90, False, False), (120, True, False),
                                               (150, True, False)])
def test_overlapping_overrides_most_recent_in_force_decides(minute, expect, old):
    W = _flags(OVS, at(minute))
    assert sim.observe(g.MACH["flags"], W)[("on", "Ana Bel")] is expect
    # the pre-review simulator let the 1-hour override end the 24-hour one: off from minute 120 on
    assert sim.observe(sim.MACHINES["flags"], W)[("on", "Ana Bel")] is old


def test_override_rule_is_stated_and_expiry_shortcut_still_differs():
    W = _flags(OVS, at(150))
    assert g.FlagsR2.OVERLAP in g.MACH["flags"].rules(W)
    assert sim.observe(g.MACH["flags"], W, frozenset({"expiry"}))[("on", "Ana Bel")] is False  # E2 never ends


def test_revert_of_the_newer_override_restores_the_older_one():
    evs = OVS + [(70, "E3", "En One", "revert", FF, {"of": "E2"})]
    W = _flags(evs, at(90))
    assert sim.observe(g.MACH["flags"], W)[("on", "Ana Bel")] is True
    assert g.surface_issues(g.MACH["flags"], W) == []


def test_revert_of_the_older_override_is_never_generated():
    evs = OVS + [(70, "E3", "En One", "revert", FF, {"of": "E1"})]
    assert g.surface_issues(g.MACH["flags"], _flags(evs, at(90))) == ["revert_of_older_override"]


def test_revert_of_an_event_that_changed_nothing_is_never_generated():
    evs = [(0, "E1", "En One", "rollout", FF, {"env": "production", "p": 0, "chg": "CHG-1234"}),  # already 0
           (10, "E2", "En One", "rollout", FF, {"env": "production", "p": 50, "chg": "CHG-1234"}),
           (20, "E3", "En One", "revert", FF, {"of": "E1"})]
    assert g.surface_issues(g.MACH["flags"], _flags(evs, at(30))) == ["revert_of_noop"]
    evs[0] = (0, "E1", "En One", "rollout", FF, {"env": "production", "p": 25, "chg": "CHG-1234"})
    assert g.surface_issues(g.MACH["flags"], _flags(evs, at(30))) == []


# ------------------------------------------------------------------------------------------------ stated rules
def test_new_rule_sentences_are_stated_once_and_the_old_texts_are_unchanged():
    pool = mv.NamePool("train")
    want = {"tickets": g.TicketsR2.RES_REVERT, "flags": g.FlagsR2.OVERLAP, "inventory": g.InventoryR2.CLEAR,
            "bookings": g.BookingsR2.REHOLD, "dialogue": g.DialogueR2.SAME_EXCLUDED,
            "docs": g.DocsR2.RESTORE_MISSING}
    for name, sentence in want.items():
        M = g.MACH[name]
        W = sim.sample_world(M, random.Random(3), pool, sim.Spec("standard", 8, {"guard": 1}))
        new, old = M.rules(W), sim.MACHINES[name].rules(W)
        assert new.count(sentence) == 1 and [r for r in new if r != sentence] == old
        assert len(new) <= len(W.rule_dates)


# ------------------------------------------------------------------------------------------------ surfaces
def _dialogue(evs):
    D = sim.MACHINES["dialogue"]
    slots = {s: list(v) for s, v in D.SCHEMAS["dinner"].items()}
    P = {"schema": "dinner", "slots": slots, "qslot": "time", "customer": "Ana Bel", "colleague": "Cor"}
    ents = {"BK-4417203": {"schema": "dinner", "confirmed": {"area": "terrace", "time": "18:00",
                                                              "menu": "set menu"}}}
    return world(g.MACH["dialogue"], ents, "BK-4417203", evs, params=P, decoys={"BK-4417230": "BK-4417203"})


def test_dialogue_speaker_and_reference_surfaces():
    ok = [(1, "M101", "Customer", "set", "BK-4417203", {"slot": "time", "v": "19:00"}, 0),
          (2, "M102", "Assistant", "propose", "BK-4417203", {"slot": "time", "v": "20:00"}, 1),
          (3, "M103", "Customer", "oset", "BK-4417230", {"slot": "time", "v": "18:30"}, 0)]
    assert g.surface_issues(g.MACH["dialogue"], _dialogue(ok)) == []
    bad = [(1, "M101", "Assistant", "set", "BK-4417203", {"slot": "time", "v": "19:00"}, 1)]
    assert g.surface_issues(g.MACH["dialogue"], _dialogue(bad)) == ["speaker"]
    bad = [(1, "M101", "Customer", "propose", "BK-4417203", {"slot": "time", "v": "19:00"}, 1)]
    assert g.surface_issues(g.MACH["dialogue"], _dialogue(bad)) == ["speaker"]
    self_ref = [(1, "M101", "Customer", "oset", "BK-4417203", {"slot": "time", "v": "19:00"}, 0)]
    W = _dialogue(self_ref)
    assert "For my other booking BK-4417203" in g.MACH["dialogue"].text(W.events[0], W)
    assert g.surface_issues(g.MACH["dialogue"], W) == ["other_booking_self"]
    neutral = [(1, "M101", "Customer", "oset", "BK-4417203", {"slot": "time", "v": "19:00"}, 1)]
    W = _dialogue(neutral)
    assert g.MACH["dialogue"].text(W.events[0], W).startswith("On booking BK-4417203")
    assert g.surface_issues(g.MACH["dialogue"], W) == []


def test_dialogue_twins_keep_the_speaker_with_the_kind_and_drop_other_booking():
    evs = [(1, "M101", "Assistant", "propose", "BK-4417203", {"slot": "time", "v": "20:00"}, 1),
           (2, "M102", "Customer", "set", "BK-4417203", {"slot": "time", "v": "19:00"}, 0),
           (3, "M103", "Customer", "oset", "BK-4417230", {"slot": "time", "v": "18:30"}, 0)]
    W = _dialogue(evs)
    muts = g.mutations(g.MACH["dialogue"], W, random.Random(0))
    seen = Counter()
    for W2 in muts:
        for e in W2.events:
            assert g.DialogueR2.SPEAKER[e.kind] == e.src, (e.kind, e.src)
            if e.kind == "oset" and e.ent == W.target:
                assert e.lt % 2 == 1
                seen["self"] += 1
        assert g.surface_issues(g.MACH["dialogue"], W2) == []
    assert seen["self"] >= 1


def test_agent_restore_of_a_file_not_in_trash_is_never_generated():
    A = g.MACH["agent"]
    P = {"dom": "files", "user": "Ana Bel"}
    ents = {"notes-2285.pdf": {"where": "archive"}, "plan-4412.pdf": {"where": "trash"}}
    bad = [(1, "C101", "assistant", "call", "notes-2285.pdf",
            {"parts": [("notes-2285.pdf", "restore", "inbox", True)]})]
    assert g.surface_issues(A, world(A, ents, "notes-2285.pdf", bad, params=P)) == ["restore_not_in_trash"]
    ok = [(1, "C101", "assistant", "call", "plan-4412.pdf", {"parts": [("plan-4412.pdf", "restore", "inbox", True)]}),
          (2, "C102", "assistant", "call", "notes-2285.pdf",
           {"parts": [("notes-2285.pdf", "restore", "inbox", False)]})]   # failed part: changes nothing anyway
    assert g.surface_issues(A, world(A, ents, "notes-2285.pdf", ok, params=P)) == []


# ------------------------------------------------------------------------------------------------ real build vs decide2
@pytest.fixture(scope="module")
def small_build(tmp_path_factory):
    root = tmp_path_factory.mktemp("f3r2")
    fb = mv.FamilyBuilder(g.KEY, generator_file=g.__file__, raw_dir=root / "raw", defs_dir=root / "defs",
                          manifest=root / "MANIFEST_yn2b.jsonl")
    fb, log = g.build(fb=fb, limit=40)
    return fb, log


def _raw_rows(fb):
    rows = []
    for part in ("train", "dev"):
        rows += fb.rows_for(part)
    return rows


def test_small_build_agrees_with_decide2_on_every_row(small_build):
    v3 = pytest.importorskip("v3_state_track")
    fb, _ = small_build
    rows = _raw_rows(fb)
    assert rows
    bad = []
    for r in rows:
        ex = v3.explain_row(r)
        if ex["answer"] is v3.UNDEFINED or ex["answer"] != r["gold"]:
            bad.append((r["rid"], r["gold"], ex.get("answer"), ex.get("error")))
        notes = set(ex.get("notes", ()))
        # the ambiguous surfaces decide2 knows are gone (the explicit rules settle the others)
        assert not notes & {"assistant_request_wording", "customer_proposal_wording", "customer_confirm_wording",
                            "other_booking_names_this_booking", "revert_of_revert"}, (r["rid"], notes)
    assert bad == []
    assert any(r["meta"]["pack"] == "flags" for r in rows) and any(r["meta"]["pack"] == "dialogue" for r in rows)


def test_export_latents_have_no_ambiguous_surface():
    out = g.export_latents("devx", 12)
    assert len(out) == 12 and {x["latent"]["machine"] for x in out} <= set(sim.HOLDOUT_MACHINES)
