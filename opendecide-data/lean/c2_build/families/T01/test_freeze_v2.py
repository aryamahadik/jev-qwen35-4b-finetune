"""Tests for families/T01/freeze_v2.py (nothing is written to the pools; Haiku is never run).

  contract     validate_answer / read_answer_file: exact keys, qids from the task's chunk, each answered once, a G-LEX
               meaning copied exactly; an invalid, missing or excluded (audit failed) file is rejected whole, never edited
  votes        record_lex_votes follows the kit rule (2 agreeing reads admit, 3 for window rules, one other pick rejects for
               good, the same extractor never votes twice); lex_state adds H45 (a form is used only with every confirmation
               read: r1b + r2b, plus r3b for window forms); g3h_results: exact match per note, unanswered is not a match
  merge        pack rules 6-13 of the redo2 prompts, merge_packs (own replacement, then the first passing spare, which takes
               the slot's held-out flag), wording rules and variant order a-then-b, notes, all through the v1 loader checks
  integration  one in-memory assemble() over the real files: v1 is reproduced and kept unchanged, targets are freeze.TARGET,
               the verdict follows the gates, only used forms are in the pool, output is deterministic, no existing file
               changes, write goes to pools_v2 only and refuses a ready re-freeze or a blocked run, load_pools round-trips
               and the loaded pools drive the plugin with G2, G3, G4, G-SL, G-LEX and G-TW all green
  redo3        merge_skins / merge_windows / check_backup_notes, the stricter lex_state (the first G-LEX reads are needed too),
               load_redo3, the baseline check against pools_v2_prev/, the overwrite guard, and the real redo3 round in memory:
               every G0 shortfall closed, provenance, surplus skins listed and not kept, exclusions, the backup-note path
Run (from lean/c2_build):  ../.venv/bin/python -B -m pytest -q -p no:cacheprovider families/T01/test_freeze_v2.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import lexicon as L  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import freeze as F1  # noqa: E402
from families.T01 import freeze_v2 as FZ  # noqa: E402
from families.T01 import haiku_author as A  # noqa: E402

T01 = Path(__file__).resolve().parent


# ------------------------------------------------------------------------------------------------ helpers
def _bytes(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def _items(n=3, **extra):
    return {f"q{i:010d}": {"qid": f"q{i:010d}", **(extra or {"text": "x"})} for i in range(n)}


def _good(items, key="text", value="a skin"):
    return [{"qid": q, key: value} for q in items]


# ------------------------------------------------------------------------------------------------ contract
def test_validate_answer_accepts_the_exact_contract():
    it = _items()
    ans, probs = FZ.validate_answer("author_skin", _bytes(_good(it)), it)
    assert probs == [] and set(ans) == set(it) and all(set(a) == {"text"} for a in ans.values())
    ans, probs = FZ.validate_answer("author_pack", _bytes(_good(it, "pack", {"people": []})), it)
    assert probs == []
    g = [{"qid": q, "person": "Dana Okafor", "ref": "POL-1", "topic": "claim"} for q in it]
    ans, probs = FZ.validate_answer("extract_g3h", _bytes(g), it)
    assert probs == [] and ans[next(iter(it))] == {"person": "Dana Okafor", "ref": "POL-1", "topic": "claim"}
    lx = _items(2, text="t", choices=["m1", "m2"])
    ans, probs = FZ.validate_answer("extract_lex", _bytes(_good(lx, "meaning", "m2")), lx)
    assert probs == [] and all(a == {"meaning": "m2"} for a in ans.values())


@pytest.mark.parametrize("name,mutate", [
    ("not json", lambda it: b"[{"),
    ("bad utf-8", lambda it: b"\xff\xfe[]"),
    ("top level object", lambda it: _bytes({"a": 1})),
    ("entry not an object", lambda it: _bytes(["x"])),
    ("extra key", lambda it: _bytes([{"qid": q, "text": "a", "note": "b"} for q in it])),
    ("missing key", lambda it: _bytes([{"qid": q} for q in it])),
    ("wrong key", lambda it: _bytes([{"qid": q, "pack": "a"} for q in it])),
    ("unknown qid", lambda it: _bytes(_good(it) + [{"qid": "qZZZ", "text": "a"}])),
    ("duplicate qid", lambda it: _bytes(_good(it) + _good(it)[:1])),
    ("unanswered", lambda it: _bytes(_good(it)[:-1])),
    ("text not a string", lambda it: _bytes([{"qid": q, "text": 3} for q in it])),
    ("duplicate json key", lambda it: b'[{"qid": "q0000000000", "text": "a", "text": "b"}]'),
    ("empty list", lambda it: b"[]"),
    ("bom", lambda it: b"\xef\xbb\xbf" + _bytes(_good(it))),
])
def test_validate_answer_rejects_the_whole_file(name, mutate):
    it = _items()
    ans, probs = FZ.validate_answer("author_skin", mutate(it), it)
    assert ans is None and probs, name


def test_validate_answer_value_rules_for_lex_g3h_and_pack():
    it = {"qa": {"qid": "qa", "text": "t", "choices": ["m1", "m2"]}}
    assert FZ.validate_answer("extract_lex", _bytes([{"qid": "qa", "meaning": "m2"}]), it)[1] == []
    for bad in ("m3", None, 2, ["m1"], "M1"):
        ans, probs = FZ.validate_answer("extract_lex", _bytes([{"qid": "qa", "meaning": bad}]), it)
        assert ans is None and probs, bad
    g = {"qa": {"qid": "qa", "text": "t", "schema": []}}
    for bad in ({"person": 5, "ref": "R", "topic": "t"}, {"person": "P", "ref": None, "topic": "t"},
                {"person": "P", "ref": "R"}, {"person": "P", "ref": "R", "topic": "t", "extra": "x"}):
        ans, probs = FZ.validate_answer("extract_g3h", _bytes([{"qid": "qa", **bad}]), g)
        assert ans is None and probs, bad
    ans, probs = FZ.validate_answer("author_pack", _bytes([{"qid": "qa", "pack": "text"}]), g)
    assert ans is None and probs
    assert FZ.validate_answer("nope", b"[]", {})[1]


def test_read_answer_file_statuses_and_no_edit(tmp_path):
    it = _items()
    ok = tmp_path / "ok.json"
    ok.write_bytes(_bytes(_good(it)))
    before = ok.read_bytes()
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-1", ok, it, set())
    assert ans and rec["status"] == "valid" and rec["sha256"] == hashlib.sha256(before).hexdigest()
    assert rec["n_expected"] == rec["n_answered"] == 3
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-1", tmp_path / "missing.json", it, set())
    assert ans is None and rec["status"] == "missing"
    bad = tmp_path / "bad.json"
    bad.write_bytes(b"not json")
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-2", bad, it, set())
    assert ans is None and rec["status"] == "invalid" and rec["problems"]
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-1", ok, it, {"T-1"})
    assert ans is None and rec["status"] == "excluded" and rec["sha256"] == hashlib.sha256(before).hexdigest()
    assert ok.read_bytes() == before and bad.read_bytes() == b"not json"      # never edited


def test_the_guard_refuses_a_never_open_path(tmp_path):
    bad = Path(FZ.C2_BUILD) / "x" / "ohs4_sealed" / "a.json"
    with pytest.raises(PermissionError):
        FZ.safe_read(bad)
    with pytest.raises(PermissionError):
        FZ.safe_read(Path(FZ.C2_BUILD) / "jev_out.json")


# ------------------------------------------------------------------------------------------------ G-LEX votes
def _lex_reg():
    reg = L.LexiconRegistry("T99")
    reg.declare("cmp.gt", "comparator", "strictly greater than the bound")
    reg.declare("cmp.ge", "comparator", "greater than or equal to the bound")
    reg.declare("win.later_anchor", "window", "a period counted from the later of two dates")
    reg.declare("win.earlier_anchor", "window", "a period counted from the earlier of two dates")
    a = reg.add("more than {X}", "cmp.gt", slots={"X": "cents"})
    w = reg.add("within {N} after the later of these two dates", "win.later_anchor", slots={"N": "count"})
    reg.unit_test_all()
    assert a.unit_ok and w.unit_ok
    return reg, a.form_id, w.form_id


def _read(reg, name, picks, *, text_override=None, plan=True, skip=()):
    """A ReadBatch where each form id is answered with the meaning of the given sem (its own or another)."""
    items, key, answers = {}, {}, {}
    for i, (fid, sem) in enumerate(picks.items()):
        qid = f"q{name}{i}"
        it = dict(reg.lexicon_items([fid])[0][1])
        filled = it["text"]
        if text_override:
            it["text"] = text_override
        items[qid] = {"qid": qid, **it}
        key[qid] = fid
        if fid not in skip:
            answers[qid] = {"meaning": reg.sems[sem].meaning if sem else "not a listed meaning"}
    pl = {fid: {"filled": reg.lexicon_items([fid])[0][1]["text"], "sem_id": reg.forms[fid].sem_id}
          for fid in picks} if plan else {}
    return FZ.ReadBatch("t", name, "extract_lex", "B-" + name, key, "psha", [("task-" + name, Path("x"), items)],
                        plan=pl, answers=answers, used_tasks={"task-" + name: "sha"})


def _v1_votes(reg, fid, n):
    for i in range(n):
        reg.record_extraction(fid, f"glex-r{i + 1}", reg.forms[fid].sem_id)


def test_kit_rule_two_agree_admit_three_for_windows_and_one_dissent_rejects():
    reg, cmp_fid, win_fid = _lex_reg()
    probs = []
    FZ.record_lex_votes(reg, _read(reg, "glex-r1", {cmp_fid: "cmp.gt", win_fid: "win.later_anchor"}), probs)
    assert reg.status(cmp_fid) == "pending" and reg.status(win_fid) == "pending"
    FZ.record_lex_votes(reg, _read(reg, "glex-r2", {cmp_fid: "cmp.gt", win_fid: "win.later_anchor"}), probs)
    assert reg.status(cmp_fid) == "admitted" and reg.status(win_fid) == "pending"      # window needs 3
    assert reg.forms[win_fid].required == 3 and reg.forms[cmp_fid].required == 2
    FZ.record_lex_votes(reg, _read(reg, "glex-r3", {win_fid: "win.later_anchor"}), probs)
    assert reg.status(win_fid) == "admitted" and probs == []
    c = FZ.record_lex_votes(reg, _read(reg, "glex-r1b", {cmp_fid: "cmp.ge"}), probs)
    assert reg.status(cmp_fid) == "rejected" and c["other_sense"] == 1


def test_an_unlisted_meaning_records_none_and_rejects():
    reg, cmp_fid, _ = _lex_reg()
    _v1_votes(reg, cmp_fid, 2)
    c = FZ.record_lex_votes(reg, _read(reg, "glex-r1b", {cmp_fid: None}), [])
    assert c["unlisted"] == 1 and reg.forms[cmp_fid].extractions[-1] == ("glex-r1b", None)
    assert reg.status(cmp_fid) == "rejected"


def test_same_extractor_twice_a_foreign_text_and_an_unused_task_give_no_vote():
    reg, cmp_fid, _ = _lex_reg()
    probs = []
    FZ.record_lex_votes(reg, _read(reg, "glex-r1b", {cmp_fid: "cmp.gt"}), probs)
    FZ.record_lex_votes(reg, _read(reg, "glex-r1b", {cmp_fid: "cmp.gt"}), probs)        # same extractor id again
    assert any("already extracted" in p for p in probs) and len(reg.forms[cmp_fid].extractions) == 1
    reg, cmp_fid, _ = _lex_reg()
    probs = []
    FZ.record_lex_votes(reg, _read(reg, "glex-r1b", {cmp_fid: "cmp.gt"}, text_override="something else"), probs)
    assert probs and reg.forms[cmp_fid].extractions == []
    reg, cmp_fid, _ = _lex_reg()
    rb = _read(reg, "glex-r1b", {cmp_fid: "cmp.gt"})
    rb.used_tasks.clear()                                           # the file was invalid or excluded
    FZ.record_lex_votes(reg, rb, [])
    assert reg.forms[cmp_fid].extractions == []


def test_h45_a_form_is_used_only_with_every_confirmation_read():
    reg, cmp_fid, win_fid = _lex_reg()
    _v1_votes(reg, cmp_fid, 2)
    _v1_votes(reg, win_fid, 3)
    assert reg.status(cmp_fid) == reg.status(win_fid) == "admitted"
    assert FZ.lex_state(reg, cmp_fid)[0] == "unconfirmed" and FZ.lex_state(reg, win_fid)[0] == "unconfirmed"
    for name in FZ.CONFIRM_READS:
        FZ.record_lex_votes(reg, _read(reg, name, {cmp_fid: "cmp.gt", win_fid: "win.later_anchor"}), [])
    assert FZ.lex_state(reg, cmp_fid)[0] == "used"
    s, why = FZ.lex_state(reg, win_fid)
    assert s == "unconfirmed" and "glex-r3b" in why                 # a window form also needs r3b
    FZ.record_lex_votes(reg, _read(reg, "glex-r3b", {win_fid: "win.later_anchor"}), [])
    assert FZ.lex_state(reg, win_fid)[0] == "used"
    assert FZ.confirm_need("window") == FZ.CONFIRM_READS_WINDOW and FZ.confirm_need("question") == FZ.CONFIRM_READS


def test_h45_a_dissenting_confirmation_read_rejects_for_good():
    reg, cmp_fid, win_fid = _lex_reg()
    _v1_votes(reg, cmp_fid, 2)
    _v1_votes(reg, win_fid, 3)
    FZ.record_lex_votes(reg, _read(reg, "glex-r1b", {cmp_fid: "cmp.gt", win_fid: "win.later_anchor"}), [])
    FZ.record_lex_votes(reg, _read(reg, "glex-r2b", {cmp_fid: "cmp.ge", win_fid: "win.earlier_anchor"}), [])
    for fid in (cmp_fid, win_fid):
        s, why = FZ.lex_state(reg, fid)
        assert s == "rejected" and "disagrees" in why
    assert reg.gate(used_form_ids=[]) ["pass"] and not reg.gate()["pass"]


def test_copy_registry_keeps_the_original_votes_untouched():
    reg, cmp_fid, _ = _lex_reg()
    _v1_votes(reg, cmp_fid, 2)
    cp = FZ.copy_registry(reg)
    cp.record_extraction(cmp_fid, "glex-r1b", cp.forms[cmp_fid].sem_id)
    assert len(reg.forms[cmp_fid].extractions) == 2 and len(cp.forms[cmp_fid].extractions) == 3


# ------------------------------------------------------------------------------------------------ G3-H
def _doc(pid, person="Dana Okafor", ref="POL-2217", topic="claim review"):
    return {"pid": pid, "text": f"{person} sends file {ref} about the {topic}.",
            "g3h_expect": {"person": person, "ref": ref, "topic": topic}}


def _g3h_read(name, docs, answers, *, text=None, valid=True):
    items, key, ans = {}, {}, {}
    for i, (pid, d) in enumerate(docs.items()):
        qid = f"q{name}{i}"
        items[qid] = {"qid": qid, "text": text or d["text"], "schema": []}
        key[qid] = pid
        if pid in answers:
            ans[qid] = answers[pid]
    return FZ.ReadBatch("t", name, "extract_g3h", "G-" + name, key, "psha", [("task-" + name, Path("x"), items)],
                        answers=ans, used_tasks={"task-" + name: "sha"} if valid else {})


def test_g3h_exact_match_unanswered_and_mismatch():
    docs = {d["pid"]: d for d in (_doc("a"), _doc("b"), _doc("c"), _doc("d", "Ines Moreau", "CASE-1", "visa stay count"))}
    good = {"person": "Dana Okafor", "ref": "POL-2217", "topic": "claim review"}
    rb = _g3h_read("g0", docs, {"a": good, "b": dict(good, person="dana okafor"),
                                "d": {"person": "Ines Moreau", "ref": "CASE-1", "topic": "visa stay count"}})   # c unread
    probs = []
    ok_of, rep = FZ.g3h_results(docs, [rb], probs)
    assert ok_of["a"][0] is True and ok_of["d"][0] is True
    assert ok_of["b"][0] is False and "person" in ok_of["b"][1][0]
    assert ok_of["c"] == (None, ["unanswered"])               # unread is not a mismatch and not a match
    assert rep["quarantined"] == ["b"] and not rep["all_templates_pass"] and probs == []


def test_g3h_every_read_must_match_and_the_item_must_be_the_note():
    docs = {"a": _doc("a")}
    good = {"person": "Dana Okafor", "ref": "POL-2217", "topic": "claim review"}
    ok_of, _ = FZ.g3h_results(docs, [_g3h_read("r1", docs, {"a": good}),
                                     _g3h_read("r2", docs, {"a": dict(good, ref="POL-2218")})], [])
    assert ok_of["a"][0] is False
    probs = []
    ok_of, _ = FZ.g3h_results(docs, [_g3h_read("r1", docs, {"a": good}, text="another text")], probs)
    assert ok_of["a"] == (None, ["unanswered"]) and probs
    ok_of, _ = FZ.g3h_results(docs, [_g3h_read("r1", docs, {"a": good}, valid=False)], [])     # the file was excluded
    assert ok_of["a"] == (None, ["unanswered"])


# ------------------------------------------------------------------------------------------------ packs
FIRST = ["Ilse", "Tomas", "Amaia", "Kofi", "Mina", "Rafael", "Nora", "Hugo", "Selma", "Pavel", "Lotte", "Bruno", "Wanda",
         "Oskar", "Greta", "Felix", "Yusuf", "Zora", "Piet", "Quinn", "Ravi", "Sven", "Tilda", "Uma", "Vera", "Wim"]
SUR = ["Adler", "Brandt", "Cassel", "Dorn", "Eklund", "Faber", "Gruber", "Hale", "Ivers", "Jansen", "Keller", "Lund",
       "Dahl", "Ebert", "Fisk", "Gale", "Hart", "Iles", "Jost", "Kemp", "Lane", "Abel", "Berg", "Cobb", "Dunn", "Eames"]
VEND = ["Larchmont Goods", "Kestrel Supply", "Hollis Trading", "Fairmont Stores", "Ironbridge Wares", "Edgewood Depot",
        "Gladstone Parts", "Birchfield Mart", "Dunmore Traders", "Cobalt Tools", "Alder Foods", "Harbor Pantry",
        "Kingsley Goods", "Lowell Supply", "Hartwell Trading", "Fenwick Stores", "Garrow Wares", "Eastham Depot",
        "Ingram Parts", "Jarvis Mart", "Dalton Traders", "Carver Tools", "Abbott Foods", "Bexley Pantry"]


def mk_pack(i: int) -> dict:
    """A valid pack whose six people and three vendors are unique to index i (0 <= i < 4)."""
    return {"people": [f"{FIRST[i * 6 + j]} {SUR[i * 6 + j]}" for j in range(6)],
            "topics": {"rolling": "seasonal stay tally", "anchor": "appeal deadline form", "waiting": "hail damage claim",
                       "purchase": "kitchen supply order", "cash": "till ledger review", "notice": "permit reply"},
            "filing": {"action": "appeal", "event_a": "decision date", "event_b": "posting date"},
            "perils": ["hail damage", "theft", "frozen pipe damage"],
            "vendors": [VEND[i * 3 + k] for k in range(3)]}


def test_mk_pack_is_valid_and_unique():
    names = []
    for i in range(4):
        p = mk_pack(i)
        assert A.validate_pack(p) == [] and E.lint_pack(p) == [] and FZ.pack_extra_problems(p, "A-L", set()) == []
        names += p["people"] + p["vendors"]
    assert len(set(names)) == len(names)


def _edit(p, path, value):
    q = json.loads(json.dumps(p))
    d = q
    for k in path[:-1]:
        d = d[k]
    d[path[-1]] = value
    return q


@pytest.mark.parametrize("name,pack,initials,fragment", [
    ("surname outside the range", mk_pack(0), "A-C", "rule 7"),
    ("vendor outside the range", mk_pack(0), "A-B", "rule 7"),
    ("no initials in the plan", mk_pack(0), None, "rule 7"),
    ("apostrophe name", _edit(mk_pack(0), ["people", 0], "Ilse O'Brien"), "A-L", "rule 8"),
    ("inner capital", _edit(mk_pack(0), ["people", 0], "Ilse McKay"), "A-Z", "rule 8"),
    ("hyphen in a first name", _edit(mk_pack(0), ["people", 0], "Anne-Lise Adler"), "A-L", "rule 8"),
    ("accented name", _edit(mk_pack(0), ["people", 0], "Ilse Adlér"), "A-L", "rule 8"),
    ("vendor with a hyphen", _edit(mk_pack(0), ["vendors", 0], "Larch-mont Goods"), "A-L", "rule 8"),
    ("month in a topic", _edit(mk_pack(0), ["topics", "rolling"], "march stay tally"), "A-L", "rule 9"),
    ("weekday short form in a peril", _edit(mk_pack(0), ["perils", 1], "sun damage"), "A-L", "rule 9"),
    ("number word in a peril", _edit(mk_pack(0), ["perils", 1], "second fire"), "A-L", "rule 9"),
    ("negation stem in a peril", _edit(mk_pack(0), ["perils", 1], "pump failure"), "A-L", "rule 11"),
    ("negation phrase", _edit(mk_pack(0), ["topics", "notice"], "reply other than mail"), "A-L", "rule 11"),
    ("report in the cash topic", _edit(mk_pack(0), ["topics", "cash"], "cash report review"), "A-L", "rule 13"),
])
def test_pack_extra_rules(name, pack, initials, fragment):
    probs = FZ.pack_extra_problems(pack, initials, set())
    assert any(fragment in x for x in probs), (name, probs)


def test_pack_taken_list_rule():
    p = mk_pack(0)
    probs = FZ.pack_extra_problems(p, "A-L", {p["people"][0].lower(), p["vendors"][1].lower()})
    assert sum("rule 6" in x for x in probs) == 2


def _cand(i, iid, *, replaces=None, spare=False, held=None, initials="A-L", pack=None):
    meta = {"role": "pack", "replaces": replaces, "spare": spare, "held_out": held, "initials": initials}
    return FZ.AuthorItem("packs", iid, pack if pack is not None else mk_pack(i), "redo2", "task-x", "psha", "f.json",
                          "sha", "tsha", meta)


def test_merge_packs_own_replacement_then_first_passing_spare_with_the_slots_flag():
    kept = [{"pid": "t01a.pack.000", "pack": mk_pack(3), "held_out": False}]
    open_slots = {"s1": False, "s2": True, "s3": False}
    bad = _edit(mk_pack(1), ["people", 0], "Ilse O'Brien")                    # fails rule 8 / the loader name shape
    cands = [_cand(0, "r.s1", replaces="s1", held=False),
             _cand(1, "r.s2", replaces="s2", held=True, pack=bad),
             _cand(2, "r.s3", replaces="s3", held=False, pack=mk_pack(3)),     # repeats the kept pack's names
             _cand(1, "r.spare0", spare=True), _cand(2, "r.spare1", spare=True)]
    probs = []
    mg = FZ.merge_packs(kept, open_slots, cands, set(), probs)
    by_slot = {slot: (it.iid, held, spare) for slot, it, held, spare in mg["accepted"]}
    assert by_slot["s1"] == ("r.s1", False, False)
    assert by_slot["s2"] == ("r.spare0", True, True)                           # first spare in sorted order, slot's flag
    assert by_slot["s3"] == ("r.spare1", False, True)
    assert mg["unplaced_slots"] == [] and probs == []
    assert mg["attempts"]["r.s2"][0]["accepted"] is False and mg["attempts"]["r.s3"][0]["reasons"]


def test_merge_packs_at_most_one_per_slot_cross_pack_names_and_kept_slots_ignored():
    kept = []
    cands = [_cand(0, "r.a", replaces="s1", held=False), _cand(0, "r.b", replaces="s2", held=False),   # same names
             _cand(1, "r.c", replaces="kept-slot", held=False)]
    probs = []
    mg = FZ.merge_packs(kept, {"s1": False, "s2": False}, cands, set(), probs)
    assert [(s, it.iid) for s, it, _h, _sp in mg["accepted"]] == [("s1", "r.a")]        # s2's names repeat s1's pack
    assert mg["unplaced_slots"] == ["s2"]
    assert any("kept-slot" in p for p in probs)
    mg = FZ.merge_packs([], {"s1": False}, [_cand(0, "r.a", replaces="s1", held=False)], {mk_pack(0)["people"][0]}, [])
    assert mg["accepted"] == [] and mg["unplaced_slots"] == ["s1"]                   # rule 6: on the TAKEN list


# ------------------------------------------------------------------------------------------------ wordings, notes
def test_wording_extra_rules():
    ok = "Which final date keeps the {ACTION} in case {REF} within the time limit under the filing rule?"
    assert FZ.wording_extra_problems(ok, "ch_deadline") == []
    for text, q in (("Which last date counts for {ACTION}?", "ch_deadline"),
                    ("May {PERSON} file the {ACTION} in time?", "yn_timely"),
                    ("Which date is the deadline for {ACTION} in case {REF}?", "ch_deadline"),
                    ("Is the person probably over the stay limit?", "yn_over"),
                    ("Is it true that the person is not above the limit?", "yn_not_over"),
                    ("Did the person fail to be on time with the {ACTION}?", "yn_fail_time"),
                    ("Did {PERSON} not file the {ACTION}?", "yn_not_timely")):
        assert FZ.wording_extra_problems(text, q), text
    assert FZ.wording_extra_problems("Is it true that the person is not over the stay limit?", "yn_not_over") == []
    assert FZ.wording_extra_problems("Was the {ACTION} from {PERSON} not filed in time?", "yn_not_timely") == []
    assert FZ.wording_extra_problems("Did the person fail to file the {ACTION} by the deadline?", "yn_fail_time") == []


def _w(iid, text, variant):
    meta = {"role": "wording", "qform": "yn_over", "kind": "rolling", "slots": ["PERSON", "REF_DATE"], "held_out": False,
            "replaces": "slot-1", "variant": variant}
    return FZ.AuthorItem("wordings", iid, text, "redo2", "task-w", "psha", "f.json", "sha", "tsha", meta)


def test_merge_wordings_variant_a_first_b_only_if_a_fails_and_one_per_slot():
    good_a = "Does the record show {PERSON} over the stay limit on {REF_DATE}?"
    good_b = "Is {PERSON} over the stay limit in the window ending on {REF_DATE}?"
    slots = {"slot-1": {"qform": "yn_over"}}
    mg = FZ.merge_wordings(set(), slots, [_w("w.b", good_b, "b"), _w("w.a", good_a, "a")])
    assert [(s, it.iid) for s, it, _o in mg["accepted"]] == [("slot-1", "w.a")] and len(mg["attempts"]["slot-1"]) == 1
    mg = FZ.merge_wordings(set(), slots, [_w("w.a", "Is {PERSON} not over the stay limit on {REF_DATE}?", "a"),
                                          _w("w.b", good_b, "b")])
    assert [(s, it.iid) for s, it, _o in mg["accepted"]] == [("slot-1", "w.b")]
    assert [t["accepted"] for t in mg["attempts"]["slot-1"]] == [False, True]
    mg = FZ.merge_wordings({good_a.lower()}, slots, [_w("w.a", good_a, "a"), _w("w.b", good_a, "b")])     # a kept text
    assert mg["accepted"] == [] and mg["unplaced_slots"] == ["slot-1"]
    mg = FZ.merge_wordings(set(), slots, [_w("w.a", "Does {PERSON} stay late today on {REF_DATE}?", "a")])
    assert mg["accepted"] == []                                              # a redo2 word ban ('today') or the loader check
    mg = FZ.merge_wordings(set(), slots, [_w("w.a", "Is {PERSON} over the previously stated limit on {REF_DATE}?", "a")])
    assert mg["accepted"] == [] and any("previously" in r for t in mg["attempts"]["slot-1"] for r in t["reasons"])


NOTE_OK = ("Internal memo for the desk.\n\nAmara Fontaine sends file LED-6330 about the loss claim to the desk, with the "
           "review team copied in. Thank you for your careful work on this matter.")
NOTE_BAD = NOTE_OK.replace("careful work", "careful order")


def _n(iid, text, variant):
    meta = {"role": "freeform", "register": "memo", "tone": "x", "held_out": False, "variant": variant,
            "replaces": "slot-n", "facts": {"PERSON": "Amara Fontaine", "REF": "LED-6330", "TOPIC": "loss claim"}}
    return FZ.AuthorItem("freeform", iid, text, "redo2", "task-n", "psha", "f.json", "sha", "tsha", meta)


def test_merge_freeform_variant_order_and_pending_only():
    mg = FZ.merge_freeform(set(), {"slot-n"}, [_n("n.a", NOTE_OK, "a"), _n("n.b", NOTE_OK + " Thanks again.", "b")])
    assert [(s, it.iid) for s, it, _sk in mg["accepted"]] == [("slot-n", "n.a")]
    sk = mg["accepted"][0][2]
    assert sk.author_mode == "F" and dict(sk.brief)["REF"] == "LED-6330"
    mg = FZ.merge_freeform(set(), {"slot-n"}, [_n("n.a", NOTE_BAD, "a"), _n("n.b", NOTE_OK, "b")])
    assert [(s, it.iid) for s, it, _sk in mg["accepted"]] == [("slot-n", "n.b")]
    assert mg["attempts"]["slot-n"][0]["reasons"] and not mg["attempts"]["slot-n"][0]["accepted"]
    mg = FZ.merge_freeform({A._norm(NOTE_OK)}, {"slot-n"}, [_n("n.a", NOTE_OK, "a")])        # a duplicate of a kept note
    assert mg["accepted"] == []


# ------------------------------------------------------------------------------------------------ targets
def test_targets_are_the_v1_targets_and_shortfalls_use_them():
    assert FZ.TARGET is F1.TARGET
    c = {"packs": {"total": 80, "held_out": 16, "training": 64},
         "skins_training": {r: 56 for r in FZ.TRAIN_REGISTERS}, "skins_held_out": {r: 28 for r in FZ.HELD_REGISTERS},
         "skins_total": 504, "documents_admitted": 120, "wordings_admitted": 30,
         "windows_by_sem": {s: 14 for s in FZ.WINDOW_SEMS}, "comparators_by_sem": {s: 12 for s in FZ.COMPARATOR_SEMS}}
    assert FZ.shortfalls(c) == []
    for path, value, text in ((("packs", "held_out"), 15, "packs held out"), (("documents_admitted",), 119, "documents"),
                              (("wordings_admitted",), 29, "wordings admitted"), (("skins_total",), 503, "skins total")):
        d = json.loads(json.dumps(c))
        t = d
        for k in path[:-1]:
            t = t[k]
        t[path[-1]] = value
        assert any(text in s for s in FZ.shortfalls(d)), text
    d = json.loads(json.dumps(c))
    d["windows_by_sem"]["win.wait_after"] = 13
    d["comparators_by_sem"]["cmp.gt"] = 11
    d["skins_training"]["chat"] = 55
    assert len(FZ.shortfalls(d)) == 3


def test_cli_passes_exclusions_and_the_rebuild_flag(monkeypatch, capsys):
    seen = {}
    monkeypatch.setattr(FZ, "run", lambda write, rebuild_check=True, exclude=(): seen.update(w=write, r=rebuild_check, e=exclude) or {})
    FZ.main(["freeze", "--no-rebuild-check", "--exclude-task", "T01-a", "--exclude-task", "T01-b"])
    assert seen == {"w": True, "r": False, "e": ("T01-a", "T01-b")}
    FZ.main(["check"])
    assert seen == {"w": False, "r": True, "e": ()}


# ------------------------------------------------------------------------------------------------ integration
def _snapshot() -> dict:
    """sha256 of every existing file the freeze reads or could touch: the T01 tree (except pools_v2, the baseline
    pools_v2_prev and this step's own files) and the kit. The top-level c2_build/*.py scripts belong to other families'
    work (edited while this suite runs) and nothing here imports or writes them."""
    mine = {"freeze_v2.py", "test_freeze_v2.py"}
    out = {}
    for root in (T01, C2_BUILD / "c2_kit"):
        for p in sorted(root.rglob("*")):
            if (not p.is_file() or "__pycache__" in p.parts or "pools_v2" in p.parts or "pools_v2_prev" in p.parts
                    or p.name in mine):
                continue
            out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


@pytest.fixture(scope="module")
def run_a():
    before = _snapshot()
    a = FZ.assemble(rebuild_check=False)
    return a, before


def test_v1_is_reproduced_and_nothing_existing_changed(run_a):
    a, before = run_a
    assert a["v1"]["integrity"]["ok"], a["v1"]["integrity"]["problems"]
    assert a["blockers"] == [], a["blockers"]
    assert _snapshot() == before                                  # no answer, plan, pool or code file was touched
    man = json.loads((FZ.POOLS_V1 / "manifest.json").read_text(encoding="utf-8"))
    assert man["freeze"] == "v1" and a["v1"]["integrity"]["manifest_sha256"] == FZ.sha_file(FZ.POOLS_V1 / "manifest.json")
    for name, text in a["v1"]["texts"].items():                   # the rebuilt v1 text is the frozen file
        assert FZ.sha_bytes(text.encode("utf-8")) == man["files"][name]["sha256"] == FZ.sha_file(FZ.POOLS_V1 / name)


def test_every_answer_file_is_recorded_once_and_rejected_whole_if_not_valid(run_a):
    a, _ = run_a
    recs = a["records"]
    assert {r["round"] for r in recs} == {"v1-author", "v1-extract", "redo", "redo2", "redo3", "redo3-reads"}
    assert {r["status"] for r in recs} <= {"valid", "invalid", "missing", "excluded"}
    assert len({(r["round"], r["file"]) for r in recs}) == len(recs)
    assert a["stray"] == [] and a["unrecognised"] == []
    assert all(r["sha256"] for r in recs if r["status"] in ("valid", "invalid"))
    for r in recs:
        if r["status"] != "valid":
            assert r["problems"]
        else:
            assert r["n_answered"] == r["n_expected"] and (C2_BUILD / r["file"]).is_file()
    # the redo g3h answers are the same bytes as the copies the v1 g3h batch reads
    by = {(r["round"], r["task_id"]): r["sha256"] for r in recs}
    for (rnd, tid), sha in by.items():
        if rnd == "redo":
            assert by[("v1-extract", tid)] == sha
    # a kind-by-kind count of the real files
    assert sum(1 for r in recs if r["round"] == "redo2") == 34 and sum(1 for r in recs if r["round"] == "redo") == 3
    assert sum(1 for r in recs if r["round"] == "redo3") == 6 and sum(1 for r in recs if r["round"] == "redo3-reads") == 6
    assert len(recs) == 109


def test_targets_and_the_verdict_follow_the_gates(run_a):
    a, _ = run_a
    assert a["short"] == FZ.shortfalls(a["counts"])
    glex, g3 = a["gates"]["G-LEX"], a["gates"]["G3-H"]
    assert a["ready"] == (not a["short"] and glex["pass"] and g3["pass"] and not a["blockers"])
    assert glex["pass"]                                         # the gate over the forms the pool uses
    files = FZ.build_files(a)
    m = json.loads(files["MANIFEST.json"])
    assert m["ready"] == a["ready"] and m["shortfalls_vs_g0"] == a["short"]
    assert m["targets_g0"]["documents"] == 120 and m["targets_g0"]["windows_per_sem"] == 14
    assert m["status"].split(":")[0] in ("READY", "SHORT", "BLOCKED")
    if not a["ready"] and not a["blockers"]:
        assert m["status"].startswith("SHORT") and all(s in m["status"] for s in a["short"])
    if a["ready"]:
        assert not a["unanswered"] and not a["pend_forms"]


def test_v1_pieces_carry_over_unchanged_and_the_pool_only_grows_where_a_slot_was_open(run_a):
    a, _ = run_a
    p1 = a["v1"]["out"]["pools"]
    pools = a["pools"]
    assert pools["skins"][:len(p1["skins"])] == p1["skins"]        # redo3 skins are appended, only into open v1 slots
    new_skins = pools["skins"][len(p1["skins"]):]
    assert all(r["round"] == "redo3" and r["slot"] in a["open_slots"]["skins"] for r in new_skins)
    assert len({r["slot"] for r in new_skins}) == len(new_skins)
    assert pools["packs"][:len(p1["packs"])] == p1["packs"]
    assert {r["pid"] for r in pools["packs"]} >= {r["pid"] for r in p1["packs"]}
    new = pools["packs"][len(p1["packs"]):]
    assert all(r["round"] == "redo2" and r["slot"] in a["open_slots"]["packs"] for r in new)
    assert len({r["slot"] for r in new}) == len(new)              # at most one pack per failed slot
    for fid, f1 in a["v1"]["rb"]["reg"].forms.items():            # v1 reads and rejections stand
        f2 = a["reg"].forms[fid]
        assert f2.extractions[:len(f1.extractions)] == f1.extractions
        if a["v1"]["rb"]["reg"].status(fid) == "rejected":
            assert a["reg"].status(fid) == "rejected" and fid not in a["used"]
    held = sum(1 for r in pools["packs"] if r["held_out"])
    assert held == sum(1 for r in p1["packs"] if r["held_out"]) + sum(1 for r in new if r["held_out"])
    for r in new:                                                 # a slot keeps its held-out flag
        assert r["held_out"] == A._pack_items()[1][r["slot"]]["held_out"]


def test_pool_holds_only_forms_that_are_admitted_and_confirmed(run_a):
    a, _ = run_a
    reg = a["reg"]
    rows = a["pools"]["wordings"] + a["pools"]["windows"] + a["pools"]["comparators"]
    assert {r["form_id"] for r in rows} == set(a["used"]) and len(rows) == len(set(a["used"]))
    for r in rows:
        f = reg.forms[r["form_id"]]
        reads = dict(f.extractions)
        assert reg.status(f.form_id) == "admitted" and f.unit_ok
        assert all(s == f.sem_id for _e, s in f.extractions)             # one other pick would have rejected it
        assert len({e for e, _ in f.extractions}) >= f.required + len(FZ.confirm_need(f.kind))
        assert all(c in reads for c in FZ.confirm_need(f.kind))          # H45: every confirmation read is there
        assert r["g_lex"]["required"] == f.required and r["g_lex"]["reads"] == [[e, s] for e, s in f.extractions]
    assert a["gate_used"]["pass"]
    for fid, f in reg.forms.items():                                     # a new redo2 wording has no vote and is not used
        if fid not in a["used"]:
            assert fid not in {r["form_id"] for r in rows}
    for slot, it, fid, *_r in a["new_forms"]:
        assert reg.forms[fid].extractions == [] and reg.status(fid) == "pending" and fid not in a["used"]
    for fid, (s, _why) in a["state"].items():
        assert (s == "used") == (fid in a["used"])


def test_documents_are_admitted_only_by_g3h_compare(run_a):
    a, _ = run_a
    docs = a["pools"]["documents"]
    pend = a["pools"]["documents_pending_g3h"]
    ids = [r["pid"] for r in docs] + [r["pid"] for r in pend]
    assert len(ids) == len(set(ids))
    assert all(r["status"] == "admitted_g3h" and r["g3h"]["read"] == "g3h-r1" and r["g3h"]["match"] is True
               and len(r["g3h"]["reads"]) == 1 for r in docs)
    by_task = {(r["round"], r["task_id"]): r["sha256"] for r in a["records"]}
    for r in docs:                       # the read of a v1 note is a v1 read; the read of a redo2 note is the redo3 one
        rd = r["g3h"]["reads"][0]
        rnd = "redo3" if r.get("round") == "redo2" else "v1-extract"
        assert by_task[(rnd, rd["task_id"])] == rd["answer_sha256"], r["pid"]
    assert all(a["g_ok"][r["pid"]][0] is True for r in docs)
    assert all(a["g_ok"][r["pid"]][0] is None for r in pend)             # no read, so pending: never admitted
    assert set(a["unanswered"]) == {r["pid"] for r in pend}
    redo2_notes = {r["pid"] for r in docs if r.get("round") == "redo2"}
    assert redo2_notes == {"t01r2.free.email.031a", "t01r2.free.memo.070a"}          # admitted by the redo3 g3h-r1 read
    assert all(r["g3h"]["reads"][0]["task_id"] == "T01-extract_g3h-d8f4b7aa-000" for r in docs if r["pid"] in redo2_notes)
    # every admitted v1 note's read is the one in the v1 batch, and compare really ran
    assert a["gates"]["G3-H"]["matched"] == len(docs) and a["counts"]["documents_admitted"] == len(docs)


def test_slot_accounting_balances_and_counts_are_the_pool(run_a):
    a, _ = run_a
    assert a["slot_counts"]["problems"] == []
    g = a["slot_counts"]["by_group"]
    c = a["counts"]
    assert g["packs"]["admitted"] == c["packs"]["total"] and g["freeform"]["admitted"] == c["documents_admitted"]
    assert g["wordings"]["admitted"] == c["wordings_admitted"]
    assert g["windows"]["admitted"] == sum(c["windows_by_sem"].values())
    assert g["comparators"]["admitted"] == sum(c["comparators_by_sem"].values())
    for d in g.values():
        assert d["authored"] == d["admitted"] + d["pending"] + d["quarantined"]


def test_added_pieces_have_provenance_that_matches_the_answer_files(run_a):
    a, _ = run_a
    by_task = {r["task_id"]: r for r in a["records"] if r["round"] == "redo2"}
    for r in a["pools"]["packs"]:
        if r.get("round") == "redo2":
            assert by_task[r["task_id"]]["status"] == "valid" and r["prompt_sha"]
    for slot, it, fid, *_rest in a["new_forms"]:
        f = a["reg"].forms[fid]
        assert f.source == "haiku" and f.haiku_task_id in by_task and f.haiku_prompt_sha
        ans = json.loads((C2_BUILD / by_task[f.haiku_task_id]["file"]).read_text(encoding="utf-8"))
        assert any(x["text"].split() == f.text.split() or " ".join(x["text"].split()) == f.text for x in ans)
    for tid, r in by_task.items():
        assert FZ.sha_file(C2_BUILD / r["file"]) == r["sha256"]


def test_output_is_deterministic_and_the_manifest_hashes_match(run_a):
    a, _ = run_a
    f1, f2 = FZ.build_files(a), FZ.build_files(a)
    assert f1 == f2
    assert set(f1) == set(FZ.POOL_FILES) | {"VALIDATION_REPORT.json", "MANIFEST.json"}
    m = json.loads(f1["MANIFEST.json"])
    assert set(m["sha256"]) == set(f1) - {"MANIFEST.json"}
    assert all(hashlib.sha256(f1[n].encode("utf-8")).hexdigest() == h for n, h in m["sha256"].items())
    assert m["supersedes"]["version"] == "v1" and m["supersedes"]["sha256"] == a["v1"]["integrity"]["manifest_sha256"]
    assert m["bindings"]["g0_spec_matches_plugin"] and m["bindings"]["c2_data_spec_matches_a37"]
    assert m["excluded_tasks_audit_failed"] == [] and "audit_note" in m
    assert len(f1["quarantine.jsonl"].splitlines()) == m["quarantine_rows"] == len(a["quarantine"])
    assert len(m["resolved_from_v1_quarantine"]) == len(a["resolved"])
    v1q = [json.loads(x) for x in (FZ.POOLS_V1 / "quarantine.jsonl").read_text(encoding="utf-8").splitlines() if x]
    kept_v1 = [q for q in json.loads("[" + ",".join(f1["quarantine.jsonl"].splitlines()) + "]") if "stage" in q
               and q["stage"] in ("authoring_check", "lint_gsl", "dedup", "lexicon_form")]
    assert len(kept_v1) + len(a["resolved"]) == len([q for q in v1q if q["stage"] in
                                                     ("authoring_check", "lint_gsl", "dedup", "lexicon_form")])
    assert all("resolved_by" in r for r in a["resolved"])
    val = json.loads(f1["VALIDATION_REPORT.json"])
    assert val["files_total"] == len(a["records"]) and val["files_valid"] == len(a["records"]) - a["n_bad_files"]


def test_the_redo2_task_set_is_exactly_what_build_redo2_builds():
    chk = FZ.redo2_rebuild_check()
    assert chk["differ_or_missing"] == [] and chk["extra_on_disk"] == [], chk
    assert chk["builder_sha256"] == FZ.sha_file(FZ.REDO2 / "build_redo2.py")


def test_load_pools_round_trips_and_offers_only_used_forms(run_a, tmp_path):
    a, _ = run_a
    files = FZ.build_files(a)
    for name, text in files.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    pools = FZ.load_pools(tmp_path)
    assert len(pools["skins"]) == len(a["pools"]["skins"]) and len(pools["documents"]) == len(a["pools"]["documents"])
    assert [w["form_id"] for w in pools["wordings"]] == [r["form_id"] for r in a["pools"]["wordings"]]
    assert len(pools["packs"]) == len(a["pools"]["packs"]) and pools["manifest"]["version"] == "freeze-v2"
    reg = pools["lexicon"]
    assert set(reg.forms) == set(a["used"])                      # nothing else can be offered
    assert all(reg.status(f) == "admitted" for f in reg.forms) and reg.gate()["pass"]
    for fid in reg.forms:
        assert reg.forms[fid].extractions == a["reg"].forms[fid].extractions
    ctx = FZ.make_ctx(pools)
    wd = [s for s in ctx.skins.values() if s.kind == "wording"]
    assert len(wd) == len(pools["wordings"]) and all(reg.status(s.lexicon_ids[0]) == "admitted" for s in wd)
    assert all(s.family == "T01" for s in ctx.skins.values())


def _dropped(problems) -> bool:
    """G0 v4 12.2: an option set that cannot share the gold's visible cues is dropped whole (a render drop, not a gate
    failure); a unit that fails any gate is still a failure."""
    return all(g == "render" and ("leave a side of the gold empty" in p or "copies a printed date" in p)
               for g, p in problems)


def test_the_loaded_pools_drive_the_plugin_in_memory(run_a, tmp_path):
    """Load the freeze as the generator would and build real units (nothing is written): every unit passes G2, G3, G4,
    G-SL, G-LEX and G-TW. Skipped for a qform or sem the pool cannot yet serve."""
    from c2_kit import pipeline
    from families.T01 import plugin as P
    a, _ = run_a
    for name, text in FZ.build_files(a).items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    ctx = FZ.make_ctx(FZ.load_pools(tmp_path))
    plugin = P.T01(lexicon=ctx.lexicon)
    bad, built = [], 0
    for seed in range(8):
        for smp in plugin.SAMPLERS:
            r = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            built += 1
            if not r.ok and not _dropped(r.problems):
                bad.append((seed, smp, r.problems[:2]))
    assert built >= 8 * len(plugin.SAMPLERS) and bad == []


def test_freeze_writes_only_pools_v2_and_refuses_a_ready_re_freeze_or_a_blocked_run(run_a, tmp_path, monkeypatch):
    a, _ = run_a
    target = tmp_path / "pools_v2"
    written = {}
    monkeypatch.setattr(FZ, "POOLS_V2", target)
    monkeypatch.setattr(FZ, "assemble", lambda **kw: a)
    monkeypatch.setattr(FZ.paths, "write_files", lambda root, files, **kw: written.update(root=Path(root), files=files))
    prev_dir = tmp_path / "pools_v2_prev"                               # redo3's baseline, already moved aside
    prev_dir.mkdir()
    (prev_dir / "MANIFEST.json").write_text(json.dumps({"ready": False, "status": "SHORT: baseline"}), encoding="utf-8")
    monkeypatch.setattr(FZ, "POOLS_V2_PREV", prev_dir)
    out = FZ.run(write=True, rebuild_check=False)
    assert written["root"] == target != FZ.POOLS_V1 and set(written["files"]) == set(out["files"])
    assert "MANIFEST.json" in written["files"] and out["ready"] == a["ready"]
    written.clear()
    out = FZ.run(write=False, rebuild_check=False)                              # check: nothing is written
    assert out["written"] is False and not written
    monkeypatch.setattr(FZ, "assemble", lambda **kw: dict(a, blockers=["x is wrong"]))
    with pytest.raises(SystemExit):
        FZ.run(write=True, rebuild_check=False)
    assert not written
    monkeypatch.setattr(FZ, "assemble", lambda **kw: a)
    target.mkdir()
    (target / "MANIFEST.json").write_text(json.dumps({"ready": False, "status": "SHORT: x"}), encoding="utf-8")
    prev_sha = FZ.sha_file(target / "MANIFEST.json")
    FZ.run(write=True, rebuild_check=False)                                     # a SHORT freeze may be replaced ...
    assert json.loads(written["files"]["MANIFEST.json"])["replaces_previous_v2"]["sha256"] == prev_sha
    written.clear()
    (target / "MANIFEST.json").write_text(json.dumps({"ready": True}), encoding="utf-8")
    monkeypatch.setattr(FZ, "assemble", lambda **kw: pytest.fail("a ready re-freeze must stop before any work"))
    with pytest.raises(SystemExit):                                              # ... a READY one never
        FZ.run(write=True, rebuild_check=False)
    (target / "MANIFEST.json").write_text("not json", encoding="utf-8")
    with pytest.raises(SystemExit):
        FZ.run(write=True, rebuild_check=False)
    assert not written


def test_an_excluded_task_is_ignored_whole_and_the_verdict_follows(run_a):
    a0, _ = run_a
    victims = ("T01-extract_lex-5b6263d2-002", "T01-extract_lex-99b2d94a-000")      # a glex-r2b task and the first r3b task
    a = FZ.assemble(rebuild_check=False, exclude=victims)
    recs = {r["task_id"]: r for r in a["records"] if r["round"] == "redo2"}
    assert all(recs[v]["status"] == "excluded" for v in victims)
    assert a["excluded"] == sorted(victims) and not a["ready"]
    # the forms those tasks should have confirmed are unused (never admitted), the rest are unchanged
    assert len(a["used"]) < len(a0["used"]) and set(a["used"]) <= set(a0["used"])
    assert any(s == "unconfirmed" for s, _w in a["state"].values())
    assert a["gate_used"]["pass"]
    for fid in set(a0["used"]) - set(a["used"]):
        assert a["state"][fid][0] == "unconfirmed" and "confirmation read" in a["state"][fid][1]
    assert any("window" in s for s in a["short"])                                   # no window form has its r3b read
    assert a["pools"]["packs"] == a0["pools"]["packs"]
    m = json.loads(FZ.build_files(a)["MANIFEST.json"])
    assert m["excluded_tasks_audit_failed"] == sorted(victims)


def test_a_v1_author_or_glex_read_cannot_be_excluded_without_blocking(run_a):
    tid = next(r["task_id"] for r in run_a[0]["records"] if r["round"] == "v1-extract" and r["kind"] == "extract_lex")
    a = FZ.assemble(rebuild_check=False, exclude=(tid,))
    assert a["blockers"] and not a["ready"] and any(tid in b for b in a["blockers"])
    tid = next(r["task_id"] for r in run_a[0]["records"] if r["round"] == "v1-author")
    a = FZ.assemble(rebuild_check=False, exclude=(tid,))
    assert any(tid in b for b in a["blockers"]) and not a["ready"]


def test_a_g3h_task_excluded_leaves_its_notes_unread_not_admitted(run_a):
    tid = "T01-extract_g3h-2529bc9d-000"
    a = FZ.assemble(rebuild_check=False, exclude=(tid,))
    assert a["blockers"] == []                                       # v1 never depended on the g3h reads
    recs = [r for r in a["records"] if r["task_id"] == tid]
    assert {r["round"] for r in recs} == {"v1-extract", "redo"} and all(r["status"] == "excluded" for r in recs)
    assert len(a["pools"]["documents"]) < len(run_a[0]["pools"]["documents"])
    assert len(a["unanswered"]) > len(run_a[0]["unanswered"]) and not a["gates"]["G3-H"]["pass"]
    assert all(r["status"] == "pending_g3h" for r in a["pools"]["documents_pending_g3h"])


# ------------------------------------------------------------------------------------------------ redo3: unit tests
SKIN_OK = ("Desk memo: {PERSON} forwards file {REF} about the {TOPIC} to the review team.",
           "Memo: {PERSON} shares file {REF} about the {TOPIC} with the help desk.",
           "Internal memo: {PERSON} hands in file {REF} about the {TOPIC} for the admin team.",
           "Entry on the {TOPIC}: {PERSON} brings in file {REF} for the intake team.")


def _skin(iid, text, register="memo", held=False, task="task-s"):
    meta = {"role": "skin", "register": register, "held_out": held, "escape": "text"}
    return FZ.AuthorItem("skins", iid, text, "redo3", task, "psha", "f.json", "sha", "tsha", meta)


def test_merge_skins_fills_the_open_slots_in_order_and_keeps_no_surplus():
    slots = {"memo": ["t01a.skin.memo.003", "t01a.skin.memo.009"], "email": ["t01a.skin.email.001"]}
    cands = [_skin(f"t01r3.skin.memo.{56 + i:03d}", t) for i, t in enumerate(SKIN_OK)]
    mg = FZ.merge_skins(set(), slots, list(reversed(cands)))                  # the order given does not matter
    assert [(s, it.iid) for s, it, _sk in mg["accepted"]] == [("t01a.skin.memo.003", "t01r3.skin.memo.056"),
                                                               ("t01a.skin.memo.009", "t01r3.skin.memo.057")]
    assert [it.iid for it in mg["surplus"]] == ["t01r3.skin.memo.058", "t01r3.skin.memo.059"]
    assert all(v["reasons"] == [] for v in mg["attempts"].values())
    assert mg["unplaced_slots"] == ["t01a.skin.email.001"]                    # no email candidate: that slot stays open
    assert all(sk.register == "memo" and not sk.held_out for _s, _i, sk in mg["accepted"])


def test_merge_skins_rejects_what_the_v1_check_rejects_and_never_counts_it():
    slots = {"memo": ["t01a.skin.memo.003"]}
    bad = _skin("t01r3.skin.memo.056", "Memo: {PERSON} sends file {REF} about the {TOPIC} shortly.")      # relative time
    nofact = _skin("t01r3.skin.memo.057", "Memo: file {REF} about the {TOPIC} is attached.")             # PERSON missing
    dup = _skin("t01r3.skin.memo.058", SKIN_OK[0])
    ok = _skin("t01r3.skin.memo.059", SKIN_OK[1])
    mg = FZ.merge_skins({A._norm(SKIN_OK[0])}, slots, [bad, nofact, dup, ok])
    assert [it.iid for _s, it, _sk in mg["accepted"]] == ["t01r3.skin.memo.059"]
    for iid in ("t01r3.skin.memo.056", "t01r3.skin.memo.057", "t01r3.skin.memo.058"):
        assert mg["attempts"][iid]["reasons"] and not mg["attempts"][iid]["accepted"]
    assert mg["surplus"] == [] and mg["unplaced_slots"] == []
    # a held-out flag that disagrees with the register, and an id that a kept skin already has
    mg = FZ.merge_skins(set(), {"faq": ["t01a.skin.faq.001"], "memo": ["t01a.skin.memo.003"]},
                        [_skin("t01r3.skin.faq.028", SKIN_OK[0], "faq", held=False),
                         _skin("t01r3.skin.memo.056", SKIN_OK[1], "memo", held=True),
                         _skin("t01a.skin.memo.020", SKIN_OK[2])], kept_ids={"t01a.skin.memo.020"})
    assert mg["accepted"] == [] and sorted(mg["unplaced_slots"]) == ["t01a.skin.faq.001", "t01a.skin.memo.003"]
    assert all("held_out" in v["reasons"][0] or "collides" in v["reasons"][0] for v in mg["attempts"].values())
    mg = FZ.merge_skins(set(), {"faq": ["t01a.skin.faq.001"]}, [_skin("t01r3.skin.faq.028", SKIN_OK[0], "faq", held=True)])
    assert mg["accepted"][0][2].held_out is True                               # a held-out skin stays held out


def _win(iid, text, sem="win.later_anchor", slot="N", task="task-w"):
    meta = {"role": "lexicon", "kind": "window", "sem": sem, "slots": {slot: "count"}}
    return FZ.AuthorItem("windows", iid, text, "redo3", task, "psha", "f.json", "sha", "tsha", meta)


def test_merge_windows_applies_the_clause_check_dedup_and_logs_lint_flags():
    cands = [_win("w.014", "inside a span of {N} that runs after the later of these dates"),
             _win("w.015", "within {N} past the later of the dates below"),
             _win("w.016", "Inside {N} after the later of these dates"),                 # capital start
             _win("w.017", "inside 7 days after the later of these dates"),              # a digit, no slot
             _win("w.018", "inside {N} after the earlier of these dates"),               # not the later date (H9)
             _win("w.019", "within {N} past the later of the dates below"),              # the same text as w.015
             _win("w.020", "a waiting period of {W} that starts on the day after its start date", "win.wait_after", "W"),
             _win("w.021", "a waiting period of {W} that starts on the next business day after its start date",
                  "win.wait_after", "W")]
    mg = FZ.merge_windows({"within {n} counted forward from the later among these dates"}, cands)
    assert [it.iid for it, _p in mg["kept"]] == ["w.014", "w.015", "w.020"]
    assert {i: bool(v["reasons"]) for i, v in mg["attempts"].items()} == {
        "w.014": False, "w.015": False, "w.016": True, "w.017": True, "w.018": True, "w.019": True, "w.020": False,
        "w.021": True}
    piece = dict(mg["kept"][0][1])
    assert piece["group"] == "windows" and piece["lexkind"] == "window" and piece["sem"] == "win.later_anchor"
    assert piece["slots"] == {"N": "count"} and piece["held_out"] is False
    assert isinstance(piece["gsl_flags"], list) and any("later" in f for f in piece["gsl_flags"])    # flagged, not dropped
    again = FZ.merge_windows({"inside a span of {n} that runs after the later of these dates"}, cands[:1])
    assert again["kept"] == [] and "duplicate" in again["attempts"]["w.014"]["reasons"][0]


def test_check_backup_notes_uses_the_family_check_and_dedups():
    facts = {"PERSON": "Lena Hartmann", "REF": "ZZ-0001", "TOPIC": "garden fence repair"}
    meta = {"role": "freeform", "register": "memo", "facts": facts, "backup_for": ["n1"]}
    good = "Internal memo. Lena Hartmann forwards file ZZ-0001 about the garden fence repair to the desk."
    cands = [FZ.AuthorItem("backup_notes", f"b.{i}", t, "redo3", "task-b", "psha", "f", "s", "t", dict(meta))
             for i, t in enumerate([good, good + " Thanks.", "Lena Hartmann sends it, who knows.", good])]
    out = FZ.check_backup_notes({A._norm(good + " Thanks.")}, cands)
    assert [it.iid for it, _sk in out["passing"]] == ["b.0"]
    assert out["attempts"]["b.1"]["reasons"] and out["attempts"]["b.2"]["reasons"] and out["attempts"]["b.3"]["reasons"]
    assert out["passing"][0][1].author_mode == "F"


def test_h45_the_confirmation_reads_never_stand_in_for_the_first_reads():
    reg, cmp_fid, win_fid = _lex_reg()
    for name in FZ.CONFIRM_READS_WINDOW:                              # three agreeing confirmation reads, no glex-r1..r3
        FZ.record_lex_votes(reg, _read(reg, name, {win_fid: "win.later_anchor"}), [])
    assert reg.status(win_fid) == "admitted"                          # the kit rule counts three agreeing extractors ...
    s, why = FZ.lex_state(reg, win_fid)
    assert s == "unconfirmed" and "independent" in why and "glex-r1," in why     # ... the freeze does not use the form
    for name in FZ.INDEPENDENT_READS_WINDOW:
        FZ.record_lex_votes(reg, _read(reg, name, {win_fid: "win.later_anchor"}), [])
    assert FZ.lex_state(reg, win_fid) == ("used", "")
    assert FZ.independent_need("window") == FZ.INDEPENDENT_READS_WINDOW and FZ.independent_need("comparator") == ("glex-r1", "glex-r2")


def test_redo3_is_a_recognised_round_and_its_files_load():
    assert "redo3" in FZ.KNOWN_ROUNDS and FZ.discover_unrecognised_rounds() == []
    probs = []
    recs, authors, reads, info = FZ.load_redo3(set(), probs)
    assert probs == [] and len(recs) == 12 and all(r["status"] == "valid" for r in recs)
    assert {r["round"] for r in recs} == {"redo3", "redo3-reads"} and info["authoring"] == 6 and info["reads"] == 6
    assert Counter(i.pool for i in authors) == {"skins": 48, "windows": 11, "backup_notes": 3}
    assert all(i.round == "redo3" and i.meta["role"] in ("skin", "lexicon", "freeform") for i in authors)
    by = {(rb.round, rb.name): rb for rb in reads}
    assert set(by) == {("redo3", "g3h-r1")} | {("redo3-reads", n) for n in
                                               (*FZ.INDEPENDENT_READS_WINDOW, *FZ.CONFIRM_READS_WINDOW)}
    g = by[("redo3", "g3h-r1")]
    assert g.kind == "extract_g3h" and len(g.key) == 2 and len(g.answers) == 2 and g.prompt_sha
    assert set(g.key.values()) == {"t01r2.free.email.031a", "t01r2.free.memo.070a"}
    for n in FZ.INDEPENDENT_READS_WINDOW + FZ.CONFIRM_READS_WINDOW:
        rb = by[("redo3-reads", n)]
        assert rb.kind == "extract_lex" and len(rb.key) == 11 == len(rb.answers) and len(rb.plan) == 11
    # excluding a task rejects its whole file
    probs = []
    recs, authors, reads, _ = FZ.load_redo3({"T01-author_lexicon-4f479381-000"}, probs)
    assert {r["task_id"]: r["status"] for r in recs}["T01-author_lexicon-4f479381-000"] == "excluded"
    assert Counter(i.pool for i in authors) == {"skins": 48, "backup_notes": 3}


def _fake_manifest(root: Path, files: dict, ready=False):
    for n, t in files.items():
        (root / n).write_text(t, encoding="utf-8")
    (root / "MANIFEST.json").write_text(json.dumps({"ready": ready, "version": "freeze-v2", "sha256": {
        n: hashlib.sha256(t.encode("utf-8")).hexdigest() for n, t in files.items()}}), encoding="utf-8")


def test_baseline_check_compares_the_rebuilt_base_freeze_with_the_baseline_on_disk(tmp_path, monkeypatch):
    monkeypatch.setattr(FZ, "REDO3", tmp_path / "no_redo3")          # no TASKS.json here: only the file-by-file comparison
    files = {n: f"content of {n}\n" for n in FZ.BASE_DATA_FILES}
    base = tmp_path / "pools_v2_prev"
    base.mkdir()
    _fake_manifest(base, files)
    ok = FZ.baseline_check(files, base)
    assert ok["ok"] is True and ok["problems"] == [] and ok["skipped"] is False
    assert ok["manifest_sha256"] == FZ.sha_file(base / "MANIFEST.json")
    other = dict(files, **{"skins.jsonl": "another skin pool\n"})
    bad = FZ.baseline_check(other, base)
    assert bad["ok"] is False and any(p.startswith("skins.jsonl") for p in bad["problems"])
    (base / "packs.jsonl").write_text("edited on disk\n", encoding="utf-8")        # a file edited after the freeze
    bad = FZ.baseline_check(files, base)
    assert bad["ok"] is False and any("packs.jsonl" in p and "MANIFEST sha256" in p for p in bad["problems"])
    none = FZ.baseline_check(files, None)
    assert none["ok"] is False and none["skipped"] is True and "no baseline" in none["problems"][0]


def test_baseline_dir_prefers_pools_v2_prev_and_previous_v2_reads_it(tmp_path, monkeypatch):
    live, prev = tmp_path / "pools_v2", tmp_path / "pools_v2_prev"
    monkeypatch.setattr(FZ, "POOLS_V2", live)
    monkeypatch.setattr(FZ, "POOLS_V2_PREV", prev)
    assert FZ.baseline_dir() is None and FZ.previous_v2() is None
    live.mkdir()
    (live / "MANIFEST.json").write_text(json.dumps({"ready": False, "status": "SHORT: a"}), encoding="utf-8")
    assert FZ.baseline_dir() == live and FZ.previous_v2()["dir"] == "pools_v2"
    prev.mkdir()
    (prev / "MANIFEST.json").write_text(json.dumps({"ready": False, "status": "SHORT: b"}), encoding="utf-8")
    assert FZ.baseline_dir() == prev                                # the earlier freeze is the baseline once it was moved aside
    assert FZ.previous_v2()["dir"] == "pools_v2"                    # ... and the live one is what a re-freeze replaces
    live_sha = FZ.sha_file(live / "MANIFEST.json")
    (live / "MANIFEST.json").unlink()
    assert FZ.previous_v2()["sha256"] != live_sha and FZ.previous_v2()["dir"] == "pools_v2_prev"


def test_freeze_refuses_to_replace_pools_v2_until_the_baseline_is_moved_aside(run_a, tmp_path, monkeypatch):
    a, _ = run_a
    live = tmp_path / "pools_v2"
    prev = tmp_path / "pools_v2_prev"
    live.mkdir()
    (live / "MANIFEST.json").write_text(json.dumps({"ready": False, "status": "SHORT: x"}), encoding="utf-8")
    written = {}
    monkeypatch.setattr(FZ, "POOLS_V2", live)
    monkeypatch.setattr(FZ, "POOLS_V2_PREV", prev)
    monkeypatch.setattr(FZ, "assemble", lambda **kw: a)
    monkeypatch.setattr(FZ.paths, "write_files", lambda root, files, **kw: written.update(root=Path(root), files=files))
    with pytest.raises(SystemExit, match="move it aside"):         # redo3 was built against this pools_v2/
        FZ.run(write=True, rebuild_check=False)
    assert not written
    out = FZ.run(write=False, rebuild_check=False)                 # a check never writes and never refuses for this
    assert out["written"] is False
    prev.mkdir()
    (prev / "MANIFEST.json").write_text(json.dumps({"ready": False, "status": "SHORT: w"}), encoding="utf-8")
    FZ.run(write=True, rebuild_check=False)
    assert written["root"] == live
    assert json.loads(written["files"]["MANIFEST.json"])["replaces_previous_v2"]["dir"] == "pools_v2"


# ------------------------------------------------------------------------------------------------ redo3: the real round
def test_redo3_closes_every_t01_shortfall_and_the_gates_pass(run_a):
    a, _ = run_a
    assert a["blockers"] == [] and a["problems"] == [], (a["blockers"], a["problems"])
    assert a["short"] == [] and a["ready"] is True                    # every G0 minimum met (freeze.TARGET, not lowered)
    assert a["gates"]["G-LEX"]["pass"] and a["gates"]["G3-H"]["pass"]
    c = a["counts"]
    assert c["skins_training"] == {r: 56 for r in FZ.TRAIN_REGISTERS} and c["skins_held_out"] == {r: 28 for r in FZ.HELD_REGISTERS}
    assert c["skins_total"] == 504 and c["documents_admitted"] == 120 and c["documents_pending"] == 0
    assert c["windows_by_sem"] == {"win.rolling_cap": 14, "win.later_anchor": 16, "win.wait_after": 16}
    assert c["packs"] == {"total": 80, "held_out": 16, "training": 64} and c["wordings_admitted"] >= 30
    assert a["baseline"]["ok"] is True and a["baseline"]["problems"] == []
    m = json.loads(FZ.build_files(a)["MANIFEST.json"])
    assert m["ready"] is True and m["status"].startswith("READY") and m["shortfalls_vs_g0"] == []
    assert m["rounds_ingested"][-2:] == ["redo3", "redo3/reads"] and m["redo3"]["active"] is True
    assert m["redo3_baseline"]["manifest_sha256"] == a["baseline"]["manifest_sha256"]


def test_redo3_skins_fill_only_open_v1_slots_and_surplus_is_listed_not_kept(run_a):
    a, _ = run_a
    ms, r3 = a["ms"], a["redo3"]["skins"]
    assert len(ms["accepted"]) == 30 and ms["unplaced_slots"] == [] and r3["answered"] == 48 == r3["passed_checks"]
    assert r3["placed"] == 30 and sum(r3["placed_by_register"].values()) == 30 and r3["failed"] == {}
    assert len(r3["surplus_not_kept"]) == 18                           # 48 passing, 30 needed
    pids = {r["pid"] for r in a["pools"]["skins"]}
    assert len(pids) == len(a["pools"]["skins"]) == 504
    assert not (pids & {x["pid"] for x in r3["surplus_not_kept"]})
    texts = [A._norm(r["text"]) for r in a["pools"]["skins"]]
    assert len(set(texts)) == len(texts)                               # no duplicate skin text in the pool
    plans = A._skin_items()[1]
    for r in a["pools"]["skins"]:
        if r.get("round") == "redo3":
            assert plans[r["slot"]]["register"] == r["register"] and r["held_out"] == (r["register"] in FZ.HELD_REGISTERS)
            assert int(r["pid"].rsplit(".", 1)[1]) >= (28 if r["held_out"] else 56)      # numbering continues v1's
            sk, why = A.check_skin(r["pid"], r["text"], {"register": r["register"], "escape": r["escape"],
                                                         "held_out": r["held_out"]}, r["task_id"], r["prompt_sha"], set())
            assert why == [] and sk.text == r["text"]                  # the stored skin passes the v1 check again
    res = {x["pid"]: x["resolved_by"] for x in a["resolved"] if x["group"] == "skins"}
    assert len(res) == 30 and set(res.values()) == {r["pid"] for r in a["pools"]["skins"] if r.get("round") == "redo3"}
    assert not [q for q in a["quarantine"] if q["group"] == "skins"]  # every v1 skin quarantine row is resolved


def test_redo3_windows_are_new_forms_used_only_with_all_six_reads(run_a):
    a, _ = run_a
    r3 = a["redo3"]["windows"]
    assert r3["answered"] == 11 == r3["passed_checks"] and r3["check_failed"] == {} and r3["form_not_added"] == []
    assert r3["used_by_sem"] == {"win.later_anchor": 6, "win.wait_after": 5}
    new_rows = [r for r in a["pools"]["windows"] if r.get("round") == "redo3"]
    assert len(new_rows) == 11 and {r["form_id"] for r in new_rows} == set(r3["used"])
    for r in new_rows:
        assert [e for e, _s in r["g_lex"]["reads"]] == [*FZ.INDEPENDENT_READS_WINDOW, *FZ.CONFIRM_READS_WINDOW]
        assert {s for _e, s in r["g_lex"]["reads"]} == {r["sem_id"]} and r["g_lex"]["required"] == 3
        assert r["group"] == "windows" and r["lexkind"] == "window" and r["held_out"] is False and r["gsl_flags"] is not None
        f = a["reg"].forms[r["form_id"]]
        assert f.source == "haiku" and f.haiku_task_id == "T01-author_lexicon-4f479381-000" and f.unit_ok
    assert set(a["vote_counts"]) >= {f"redo3-reads:{n}" for n in FZ.INDEPENDENT_READS_WINDOW + FZ.CONFIRM_READS_WINDOW}
    assert all(v == {"listed": 11} for k, v in a["vote_counts"].items() if k.startswith("redo3-reads:"))
    tr = json.loads((FZ.REDO3_READS / "TASKS.json").read_text(encoding="utf-8"))["new_forms"]
    assert {x["form_id"] for x in tr} == set(r3["used"])               # the forms the reads were built for
    wins = a["pools"]["windows"]
    assert [r["pid"] for r in wins] == sorted(r["pid"] for r in wins)          # a deterministic order


def test_redo3_g3h_read_admits_the_two_redo2_notes_and_no_backup_is_used(run_a):
    a, _ = run_a
    bk = a["redo3"]["backup_notes"]
    assert a["redo3"]["g3h_reads"] == {"t01r2.free.email.031a": {"match": True, "diffs": []},
                                       "t01r2.free.memo.070a": {"match": True, "diffs": []}}
    assert bk["answered"] == 3 and bk["passed_checks"] == 3 and bk["used"] == [] and len(bk["unused"]) == 3
    assert a["pools"]["documents_pending_g3h"] == [] and a["unanswered"] == [] and a["mismatched"] == []
    assert not [q for q in a["quarantine"] if q["stage"] == "G3-H"]
    pids = {r["pid"] for r in a["pools"]["documents"]}
    assert not (pids & set(bk["unused"]))


def test_redo3_provenance_matches_the_answer_files(run_a):
    a, _ = run_a
    by_task = {r["task_id"]: r for r in a["records"] if r["round"] in ("redo3", "redo3-reads")}
    assert len(by_task) == 12 and all(r["status"] == "valid" for r in by_task.values())
    for r in a["pools"]["skins"] + a["pools"]["windows"]:
        if r.get("round") == "redo3":
            rec = by_task[r["task_id"]]
            ans = json.loads((C2_BUILD / rec["file"]).read_text(encoding="utf-8"))
            assert any(" ".join(x["text"].split()) == " ".join(r["text"].split()) or x["text"].strip() == r["text"]
                       for x in ans), r["pid"]
            assert r["prompt_sha"] and FZ.sha_file(C2_BUILD / rec["file"]) == rec["sha256"]
    for name, t in a["redo_checks"].items():
        assert t["valid"] == t["tasks"]
    rb = {(x.round, x.name): x for x in a["read_batches"]}
    for n in FZ.INDEPENDENT_READS_WINDOW + FZ.CONFIRM_READS_WINDOW:
        x = rb[("redo3-reads", n)]
        assert len(x.answers) == 11 and all(FZ.sha_file(p) == x.used_tasks[tid] for tid, p, _i in x.tasks)


def test_excluding_redo3_tasks_leaves_exactly_their_pieces_open(run_a):
    a0, _ = run_a
    skin_tasks = tuple(f"T01-author_skin-e8e8fa3e-00{i}" for i in range(3))
    g3h_task, r3b_task = "T01-extract_g3h-d8f4b7aa-000", "T01-extract_lex-11d182c7-000"
    a = FZ.assemble(rebuild_check=False, exclude=skin_tasks + (g3h_task, r3b_task))
    recs = {r["task_id"]: r for r in a["records"] if r["round"].startswith("redo3")}
    assert all(recs[t]["status"] == "excluded" for t in skin_tasks + (g3h_task, r3b_task))
    assert a["blockers"] == [] and not a["ready"]
    assert a["counts"]["skins_total"] == 474 and len(a["ms"]["unplaced_slots"]) == 30     # back to the redo2 pool
    assert a["counts"]["documents_admitted"] == 118 and sorted(a["unanswered"]) == ["t01r2.free.email.031a",
                                                                                     "t01r2.free.memo.070a"]
    assert not a["gates"]["G3-H"]["pass"]
    wins = [fid for _i, _p, fid in a["new_win"]]
    assert len(wins) == 11 and all(a["state"][f][0] == "unconfirmed" and "glex-r3b" in a["state"][f][1] for f in wins)
    assert a["counts"]["windows_by_sem"] == {"win.rolling_cap": 14, "win.later_anchor": 10, "win.wait_after": 11}
    assert a["gate_used"]["pass"]                                      # unused forms never fail the gate over the used ones
    assert len([q for q in a["quarantine"] if q["group"] == "skins" and q["stage"] == "authoring_check"]) == 30
    assert any(q["stage"] == "redo3" and q["status"] == "slot_open" for q in a["quarantine"])
    assert a["pools"]["packs"] == a0["pools"]["packs"] and a["pools"]["wordings"] == a0["pools"]["wordings"]
    sh = a["short"]
    assert any(x.startswith("skins ") for x in sh) and any(x.startswith("window win.later_anchor") for x in sh)
    assert any(x.startswith("documents admitted") for x in sh)
    m = json.loads(FZ.build_files(a)["MANIFEST.json"])
    assert m["status"].startswith("SHORT") and m["excluded_tasks_audit_failed"] == sorted(skin_tasks + (g3h_task, r3b_task))


def test_excluding_the_window_authoring_task_leaves_the_reads_without_forms(run_a):
    a = FZ.assemble(rebuild_check=False, exclude=("T01-author_lexicon-4f479381-000",))
    assert a["new_win"] == [] and a["blockers"] == [] and not a["ready"]
    assert a["counts"]["windows_by_sem"]["win.later_anchor"] == 10 and a["counts"]["windows_by_sem"]["win.wait_after"] == 11
    assert sum(1 for p in a["problems"] if "none of its forms exists" in p) == 6        # one note per read, not 66
    assert a["counts"]["skins_total"] == 504 and a["counts"]["documents_admitted"] == 120
    assert any(x.startswith("window win.later_anchor") for x in a["short"])


def test_a_dropped_note_is_replaced_by_a_passing_backup_that_then_waits_for_its_own_read(run_a, monkeypatch):
    real = FZ.load_redo3

    def tampered(excluded, problems):
        recs, authors, reads, info = real(excluded, problems)
        for rb in reads:
            if rb.kind == "extract_g3h":
                qid = next(q for q, pid in rb.key.items() if pid == "t01r2.free.email.031a")
                rb.answers[qid] = dict(rb.answers[qid], topic="a different topic")         # an in-memory mismatch
        return recs, authors, reads, info

    monkeypatch.setattr(FZ, "load_redo3", tampered)
    a = FZ.assemble(rebuild_check=False)
    assert a["mismatched"] == ["t01r2.free.email.031a"] and a["blockers"] == []
    used = a["redo3"]["backup_notes"]["used"]
    assert [u["replaces"] for u in used] == ["t01r2.free.email.031a"] and len(used) == 1
    pend = a["pools"]["documents_pending_g3h"]
    assert [r["pid"] for r in pend] == [used[0]["backup"]] and pend[0]["backup_for"] == "t01r2.free.email.031a"
    assert pend[0]["status"] == "pending_g3h" and pend[0]["round"] == "redo3"
    assert a["counts"]["documents_admitted"] == 119 and a["unanswered"] == [used[0]["backup"]]
    assert not a["ready"] and not a["gates"]["G3-H"]["pass"]
    assert any(x.startswith("documents admitted") and "119 of 120" in x for x in a["short"])
    assert any(q["stage"] == "G3-H" and q["pid"] == "t01r2.free.email.031a" for q in a["quarantine"])
    assert a["slot_counts"]["problems"] == []
    # both notes mismatch: two backups, and a third stays unused
    def both(excluded, problems):
        recs, authors, reads, info = real(excluded, problems)
        for rb in reads:
            if rb.kind == "extract_g3h":
                for q in rb.answers:
                    rb.answers[q] = dict(rb.answers[q], ref="XX-0000")
        return recs, authors, reads, info
    monkeypatch.setattr(FZ, "load_redo3", both)
    a = FZ.assemble(rebuild_check=False)
    assert sorted(a["mismatched"]) == ["t01r2.free.email.031a", "t01r2.free.memo.070a"]
    assert len(a["redo3"]["backup_notes"]["used"]) == 2 and len(a["redo3"]["backup_notes"]["unused"]) == 1
    assert a["counts"]["documents_admitted"] == 118 and len(a["pools"]["documents_pending_g3h"]) == 2


def test_the_redo3_rebuild_check_reproduces_every_task_and_read_file():
    chk = FZ.redo3_rebuild_check(FZ.baseline_dir())
    assert chk["skipped"] is None, chk
    assert chk["differ_or_missing"] == [] and chk["extra_on_disk"] == [], chk
    assert chk["redo3_files"] == 28 and chk["reads_files"] == 31
    assert chk["builder_sha256"]["build_redo3.py"] == FZ.sha_file(FZ.REDO3 / "build_redo3.py")
    none = FZ.redo3_rebuild_check(None)
    assert none["skipped"] == "no baseline freeze to read" and none["differ_or_missing"] == []


def test_a_redo3_pool_row_loads_and_the_loaded_pools_use_the_new_windows(run_a, tmp_path):
    a, _ = run_a
    for name, text in FZ.build_files(a).items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    pools = FZ.load_pools(tmp_path)
    assert len(pools["skins"]) == 504 and len(pools["documents"]) == 120
    ids = {r["form_id"] for r in pools["windows"]}
    assert set(a["redo3"]["windows"]["used"]) <= ids and all(pools["lexicon"].status(f) == "admitted" for f in ids)
    assert "T01-SK-memo.056" in pools["skins"] and "T01-SK-faq.028" in pools["skins"]
    assert pools["skins"]["T01-SK-faq.028"].held_out is True


# ------------------------------------------------------------------------------------------------ the frozen pools_v2/
@pytest.mark.skipif(not (FZ.POOLS_V2 / "MANIFEST.json").is_file(), reason="pools_v2/ is not frozen")
def test_the_frozen_pools_v2_on_disk_are_what_the_script_produces_now(run_a):
    """Reproducibility: the nine pool data files and VALIDATION_REPORT.json on disk equal the in-memory freeze (the MANIFEST
    is left out: it records the freeze it replaced). A changed answer file, plan or code after the freeze shows up here."""
    a, _ = run_a
    man = json.loads((FZ.POOLS_V2 / "MANIFEST.json").read_text(encoding="utf-8"))
    files = FZ.build_files(a)
    for name, text in files.items():
        if name == "MANIFEST.json":
            continue
        assert (FZ.POOLS_V2 / name).read_text(encoding="utf-8") == text, name
        assert man["sha256"][name] == FZ.sha_bytes(text.encode("utf-8"))
    assert man["ready"] == a["ready"] and man["shortfalls_vs_g0"] == a["short"]
    assert man["redo3_baseline"]["manifest_sha256"] == a["baseline"]["manifest_sha256"]
    assert man["replaces_previous_v2"]["sha256"] == a["baseline"]["manifest_sha256"]      # the SHORT freeze kept as pools_v2_prev/


@pytest.mark.skipif(not (FZ.POOLS_V2 / "MANIFEST.json").is_file(), reason="pools_v2/ is not frozen")
def test_the_frozen_pools_v2_drive_the_plugin_and_the_redo3_windows_appear_in_rows():
    from c2_kit import pipeline
    from families.T01 import plugin as P
    pools = FZ.load_pools()
    ctx = FZ.make_ctx(pools)
    plugin = P.T01(lexicon=ctx.lexicon)
    new_ids = {r["form_id"] for r in pools["windows"] if r.get("round") == "redo3"}
    assert len(new_ids) == 11
    seen, bad = set(), []
    for seed in range(30):
        for smp in plugin.SAMPLERS:
            r = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            if not r.ok and not _dropped(r.problems):
                bad.append((seed, smp, r.problems[:2]))
            for row in r.rows:
                seen |= set(row["meta"]["c2"]["lexicon_ids"]) & new_ids
    assert bad == []                                    # G2, G3, G4, G-SL, G-LEX and G-TW all green with the new clauses
    assert len(seen) >= 6, sorted(seen)                 # the generator really draws the new clauses
