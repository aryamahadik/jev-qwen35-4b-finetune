"""Tests for families/T28/freeze_v2.py (nothing is written to the pools; Haiku is never run).

  contract     validate_answer / read_answer_file: exact keys, qids from the task's chunk, each answered once, a G-LEX
               choice copied exactly; an invalid, missing or excluded (audit failed) file is rejected whole and never edited
  votes        record_lex_votes follows the kit rule: 2 agreeing reads admit, one other pick rejects for good, one read is
               pending, precedence needs 3; g3h_results: exact match per memo, an unanswered or wrong memo is dropped
  merge        merge_author_items runs redo pieces through the v1 loader checks: duplicates (in a batch and across
               batches) reject the new piece, a later round fills only what is still open
  redo3        a later round with the redo2 layout is found by itself (discover_rounds), its three attempts at one open
               piece fill it once (the first passing attempt), its reads are recorded, and its task files are checked
               byte for byte against build_redo3.py (rebuild_round: a changed or extra file blocks the freeze)
  integration  one in-memory assemble() over the real files: v1 is reproduced and kept unchanged, targets are the v1
               targets, the verdict follows the gates, pending forms never enter the pool, provenance points at real
               files, the output is deterministic, no existing file changes, write goes to pools_v2 only and refuses
               a re-freeze or a blocked run, load_pools round-trips
Run (from lean/):  ../.venv/bin/python -B -m pytest -q -p no:cacheprovider c2_build/families/T28/test_freeze_v2.py
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
import types
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import lexicon as L  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T28 import freeze_v2 as FZ  # noqa: E402
from families.T28 import pool_freeze as PF  # noqa: E402

T28 = Path(__file__).resolve().parent


# ------------------------------------------------------------------------------------------------ helpers
def _bytes(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def _items(n=3, kind="text"):
    return {f"q{i:010d}": {"qid": f"q{i:010d}", kind: "x"} for i in range(n)}


def _good(items, key="text", value="a skin"):
    return [{"qid": q, key: value} for q in items]


# ------------------------------------------------------------------------------------------------ contract
def test_validate_answer_accepts_the_exact_contract():
    it = _items()
    ans, probs = FZ.validate_answer("author_skin", _bytes(_good(it)), it)
    assert probs == [] and set(ans) == set(it) and all(set(a) == {"text"} for a in ans.values())
    ans, probs = FZ.validate_answer("author_pack", _bytes(_good(it, "pack", {"org": "x"})), it)
    assert probs == []
    ans, probs = FZ.validate_answer("extract_g3h", _bytes([{"qid": q, "user": "A", "agent": None} for q in it]), it)
    assert probs == [] and ans[next(iter(it))] == {"user": "A", "agent": None}


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
])
def test_validate_answer_rejects_the_whole_file(name, mutate):
    it = _items()
    ans, probs = FZ.validate_answer("author_skin", mutate(it), it)
    assert ans is None and probs, name


def test_validate_answer_lex_and_g3h_value_rules():
    it = {"qa": {"qid": "qa", "text": "t", "choices": ["m1", "m2"]}}
    assert FZ.validate_answer("extract_lex", _bytes([{"qid": "qa", "choice": "m2"}]), it)[1] == []
    for bad in ("m3", None, 2, ["m1"]):
        ans, probs = FZ.validate_answer("extract_lex", _bytes([{"qid": "qa", "choice": bad}]), it)
        assert ans is None and probs, bad
    g = {"qa": {"qid": "qa", "text": "t", "schema": []}}
    ans, probs = FZ.validate_answer("extract_g3h", _bytes([{"qid": "qa", "user": 5, "agent": "A"}]), g)
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
    assert ans is None and rec["status"] == "excluded"
    assert ok.read_bytes() == before and bad.read_bytes() == b"not json"      # never edited


# ------------------------------------------------------------------------------------------------ G-LEX votes
def _lex_reg():
    reg = L.LexiconRegistry("T99")
    reg.declare("cmp.le", "comparator", "at most the bound")
    reg.declare("cmp.lt", "comparator", "less than the bound")
    reg.declare("prec.P1", "precedence", "deny beats ask beats allow")
    reg.declare("prec.P2", "precedence", "the first listed rule decides")
    a = reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
    b = reg.add("a deny rule always beats an ask rule", "prec.P1")
    reg.unit_test_all()
    return reg, a.form_id, b.form_id


def _read(reg, name, picks, *, text_override=None):
    """A ReadBatch where each form id is answered with the meaning of the given sem (the form's own or another)."""
    items, key, answers = {}, {}, {}
    for i, (fid, sem) in enumerate(picks.items()):
        qid = f"q{name}{i}"
        it = dict(reg.lexicon_items([fid])[0][1])
        if text_override:
            it["text"] = text_override
        items[qid] = {"qid": qid, **it}
        key[qid] = fid
        meaning = reg.sems[sem].meaning
        answers[qid] = {"choice": meaning}
    rb = FZ.ReadBatch("t", name, "extract_lex", "B-" + name, key, "psha", [("task-" + name, Path("x"), items)],
                      FZ.meaning_table(reg), answers, {"task-" + name: "sha"})
    return rb


def test_glex_two_agreeing_reads_admit_and_one_dissent_rejects():
    reg, cmp_fid, prec_fid = _lex_reg()
    probs = []
    FZ.record_lex_votes(reg, _read(reg, "r0", {cmp_fid: "cmp.le"}), probs)
    assert reg.status(cmp_fid) == "pending"
    FZ.record_lex_votes(reg, _read(reg, "r1", {cmp_fid: "cmp.le"}), probs)
    assert reg.status(cmp_fid) == "admitted" and probs == []
    reg, cmp_fid, _ = _lex_reg()
    FZ.record_lex_votes(reg, _read(reg, "r0", {cmp_fid: "cmp.le"}), [])
    c = FZ.record_lex_votes(reg, _read(reg, "r1", {cmp_fid: "cmp.lt"}), [])
    assert reg.status(cmp_fid) == "rejected" and c["listed_other_sense"] == 1


def test_glex_precedence_needs_three_reads():
    reg, _, prec_fid = _lex_reg()
    for i in range(2):
        FZ.record_lex_votes(reg, _read(reg, f"r{i}", {prec_fid: "prec.P1"}), [])
    assert reg.status(prec_fid) == "pending" and reg.forms[prec_fid].required == 3
    FZ.record_lex_votes(reg, _read(reg, "r2", {prec_fid: "prec.P1"}), [])
    assert reg.status(prec_fid) == "admitted"


def test_glex_same_extractor_twice_and_foreign_text_give_no_vote():
    reg, cmp_fid, _ = _lex_reg()
    probs = []
    FZ.record_lex_votes(reg, _read(reg, "r0", {cmp_fid: "cmp.le"}), probs)
    FZ.record_lex_votes(reg, _read(reg, "r0", {cmp_fid: "cmp.le"}), probs)       # same extractor id again
    assert any("already extracted" in p for p in probs) and len(reg.forms[cmp_fid].extractions) == 1
    reg, cmp_fid, _ = _lex_reg()
    probs = []
    FZ.record_lex_votes(reg, _read(reg, "r0", {cmp_fid: "cmp.le"}, text_override="something else"), probs)
    assert probs and reg.forms[cmp_fid].extractions == []


# ------------------------------------------------------------------------------------------------ G3-H
def _memo(i, user="Dana Okafor", agent="Atlas Desk"):
    return K.make_skin(f"T28-MF-{i:03d}", "T28", f"{user} passed the work to {agent} in a hurry.",
                       {"USER": "name", "AGENT": "name"}, register="memo", author_mode="F",
                       brief={"USER": user, "AGENT": agent}, haiku_task_id="t", haiku_prompt_sha="p")


def _g3h_read(name, memos, answers, *, text=None):
    items, key, ans = {}, {}, {}
    for i, (sid, sk) in enumerate(memos.items()):
        qid = f"q{name}{i}"
        items[qid] = {"qid": qid, "text": text or sk.text, "schema": []}
        key[qid] = sid
        if sid in answers:
            ans[qid] = answers[sid]
    return FZ.ReadBatch("t", name, "extract_g3h", "G-" + name, key, "psha", [("task-" + name, Path("x"), items)], {},
                        ans, {"task-" + name: "sha"})


def test_g3h_exact_match_unanswered_and_mismatch():
    memos = {m.skin_id: m for m in (_memo(1), _memo(2), _memo(3), _memo(4, "Ines Moreau", "Wren"))}
    good = {"user": "Dana Okafor", "agent": "Atlas Desk"}
    rb = _g3h_read("g0", memos, {"T28-MF-001": good, "T28-MF-002": {"user": "dana okafor", "agent": "Atlas Desk"},
                                 "T28-MF-004": {"user": "Ines Moreau", "agent": "Wren"}})      # 003 unanswered
    probs = []
    ok_of, rep = FZ.g3h_results(memos, [rb], probs)
    assert ok_of["T28-MF-001"][0] and ok_of["T28-MF-004"][0]
    assert not ok_of["T28-MF-002"][0] and ok_of["T28-MF-003"] == (False, ["unanswered"])
    assert not rep["all_templates_pass"] and set(rep["quarantined"]) == {"T28-MF-002", "T28-MF-003"}


def test_g3h_every_read_must_match_and_the_item_must_be_the_memo():
    memos = {"T28-MF-001": _memo(1)}
    good = {"user": "Dana Okafor", "agent": "Atlas Desk"}
    bad = {"user": "Dana Okafor", "agent": None}
    ok_of, _ = FZ.g3h_results(memos, [_g3h_read("a", memos, {"T28-MF-001": good}),
                                      _g3h_read("b", memos, {"T28-MF-001": bad})], [])
    assert not ok_of["T28-MF-001"][0]
    probs = []
    ok_of, _ = FZ.g3h_results(memos, [_g3h_read("a", memos, {"T28-MF-001": good}, text="another text")], probs)
    assert ok_of["T28-MF-001"] == (False, ["unanswered"]) and probs


# ------------------------------------------------------------------------------------------------ merge
SKIN_OK = "{USER}: Handing over the timetable tidy-up for the depot, the usual way.\n{AGENT}: Got it, starting on that from the top.\n{USER}: Thanks, that is the lot."
SKIN_ONE = "Dear {AGENT},\n\nThe clean-up is passed to you from {USER} in the usual way, and the step ahead is a routine one.\n\nThanks,"
WORDING_OK = "Per the policy, does the agent check with the user and make this call only if the user agrees?"


def _st1():
    return {"loaded": {"skins": {}, "freeform": {}, "attacks": {}, "wordings": [], "precedence": [], "comparators": [],
                       "packs": []}}


def _ai(pool, iid, payload, rnd="redo1", meta=None):
    meta = meta or {"skins": {"role": "skin", "register": "chat", "escape": "text", "held_out": False},
                    "wordings": {"role": "wording", "qform": "yn_ask", "held_out": False}}.get(pool, {})
    return FZ.AuthorItem(pool, iid, payload, rnd, f"task-{rnd}", "psha", "f.json", "sha", meta)


def test_merge_accepts_good_rejects_g_sl_and_duplicates():
    items = [_ai("skins", "t28a.skin.chat.001", SKIN_OK),
             _ai("skins", "t28a.skin.chat.002", SKIN_ONE),                       # 'one' is a G-SL number word
             _ai("skins", "t28a.skin.chat.003", SKIN_OK),                        # duplicate of the first
             _ai("wordings", "t28a.wording.yn_ask.001", WORDING_OK),
             _ai("wordings", "t28a.wording.yn_ask.002", WORDING_OK)]             # duplicate wording
    mg = FZ.merge_author_items(_st1(), {}, items, [])
    assert set(mg["accepted"]["skins"]) == {"t28a.skin.chat.001"}
    assert set(mg["accepted"]["wordings"]) == {"t28a.wording.yn_ask.001"}
    assert any("number" in r for r in mg["attempts"][("skins", "t28a.skin.chat.002")][0]["reasons"])
    assert mg["attempts"][("skins", "t28a.skin.chat.003")][0]["reasons"]
    assert mg["provenance"][("skins", "t28a.skin.chat.001")]["answer_file"] == "f.json"


def test_merge_cross_batch_duplicate_and_v1_text_reject_the_new_piece():
    st1 = _st1()
    st1["loaded"]["freeform"] = {"T28-MF-001": types.SimpleNamespace(text=SKIN_OK)}     # the same text, in another batch
    mg = FZ.merge_author_items(st1, {}, [_ai("skins", "t28a.skin.chat.001", SKIN_OK)], [])
    assert not mg["accepted"]["skins"]
    assert "another batch" in mg["attempts"][("skins", "t28a.skin.chat.001")][0]["reasons"][0]
    st1 = _st1()
    st1["loaded"]["skins"] = {"T28-SK-chat.009": K.make_skin("T28-SK-chat.009", "T28", SKIN_OK,
                                                              {"USER": "name", "AGENT": "name"})}
    mg = FZ.merge_author_items(st1, {}, [_ai("skins", "t28a.skin.chat.001", SKIN_OK)], [])
    assert not mg["accepted"]["skins"] and "duplicate" in mg["attempts"][("skins", "t28a.skin.chat.001")][0]["reasons"][0]


def test_merge_later_round_fills_only_what_is_open():
    first = _ai("skins", "t28a.skin.chat.001", SKIN_ONE, "redo1")
    second = _ai("skins", "t28a.skin.chat.001", SKIN_OK, "redo2")
    third = _ai("skins", "t28a.skin.chat.001", SKIN_OK.replace("lot", "whole job"), "redo3")
    mg = FZ.merge_author_items(_st1(), {}, [third, second, first], [])
    assert mg["accepted"]["skins"]["t28a.skin.chat.001"].text == SKIN_OK            # redo2, not redo3
    tries = mg["attempts"][("skins", "t28a.skin.chat.001")]
    assert [t["round"] for t in tries] == ["redo1", "redo2", "redo3"] and tries[2].get("ignored")
    assert mg["provenance"][("skins", "t28a.skin.chat.001")]["round"] == "redo2"


def test_merge_three_attempts_at_one_open_piece_first_passing_one_fills_it():
    """The redo3 pattern: three agents answer the SAME piece; the first attempt that passes the loader fills it, later
    ones are logged as unused, and a failing attempt does not block a later one."""
    a = _ai("skins", "t28a.skin.chat.001", SKIN_ONE, "redo3")                            # 'one' fails G-SL
    b = _ai("skins", "t28a.skin.chat.001", SKIN_OK, "redo3")
    c = _ai("skins", "t28a.skin.chat.001", SKIN_OK.replace("lot", "whole job"), "redo3")
    a, b, c = (dataclasses.replace(x, task=f"task-{t}") for x, t in ((a, "a"), (b, "b"), (c, "c")))
    mg = FZ.merge_author_items(_st1(), {}, [a, b, c], [])
    key = ("skins", "t28a.skin.chat.001")
    assert mg["accepted"]["skins"]["t28a.skin.chat.001"].text == SKIN_OK
    assert mg["provenance"][key]["task"] == "task-b" and mg["provenance"][key]["round"] == "redo3"
    tries = mg["attempts"][key]
    assert [t["task"] for t in tries] == ["task-a", "task-b", "task-c"]
    assert tries[0]["reasons"] and not tries[0].get("accepted")
    assert tries[1].get("accepted") and tries[2].get("ignored")
    mg = FZ.merge_author_items(_st1(), {}, [a], [])                                      # all attempts fail: still open
    assert not mg["accepted"]["skins"] and key not in mg["provenance"]


def _pack(org="brindle"):
    verbs = ("send", "forward", "draft", "reply", "archive", "tag", "export", "digest", "pin", "label")
    return {"org": org, "partner": "copperton", "outside": "postwise", "locals": ["mira", "ops", "billing", "tomas"],
            "roots": [{"root": "/data/prod", "near_miss": "/data/production"},
                      {"root": "/srv/exports", "near_miss": "/srv/exports-old"},
                      {"root": "/home/shared", "near_miss": "/home/shared2"}],
            "subdirs": ["archive", "reports"], "files": ["ledger.csv", "notes.md", "dump.sql"],
            "namespaces": {"mail": {v: ["to"] for v in verbs}, "billing": {v: ["amount"] for v in verbs},
                           "files": {v: ["path"] for v in verbs}}}


def test_merge_pack_org_must_be_new():
    st1 = _st1()
    st1["loaded"]["packs"] = [{"org": "taken"}]
    mg = FZ.merge_author_items(st1, {}, [_ai("packs", "t28a.pack.001", _pack("brindle"), meta={"held_out": False}),
                                         _ai("packs", "t28a.pack.002", _pack("taken"), meta={"held_out": False}),
                                         _ai("packs", "t28a.pack.003", _pack("brindle"), meta={"held_out": False})], [])
    assert set(mg["accepted"]["packs"]) == {"t28a.pack.001"}
    assert "org label repeats another pack" in mg["attempts"][("packs", "t28a.pack.002")][0]["reasons"]


# ------------------------------------------------------------------------------------------------ redo3 / rebuild check
def _round_dir(tmp_path, files, n=3, script=True):
    d = tmp_path / f"redo{n}"
    for rel_, text in files.items():
        (d / rel_).parent.mkdir(parents=True, exist_ok=True)
        (d / rel_).write_text(text, encoding="utf-8")
    (d / "answers").mkdir(exist_ok=True)
    (d / "answers" / "T28-x-000.json").write_text("[]", encoding="utf-8")            # answers are never generated files
    if script:
        (d / f"build_redo{n}.py").write_text(
            "FILES = %r\n\ndef build():\n    return dict(FILES), {}\n" % (files,), encoding="utf-8")
    return d


def test_rebuild_round_is_byte_for_byte_and_ignores_answers_and_the_script(tmp_path):
    files = {"tasks/T-000.md": "task text\n", "plan/p.json": "{}\n", "REDO3_INDEX.json": "{}\n"}
    d = _round_dir(tmp_path, files)
    assert FZ.load_build_module(3, d).build()[0] == files
    assert FZ.rebuild_round(3, d) == {"files": 3, "differ_or_missing": [], "extra_on_disk": []}
    (d / "tasks" / "T-000.md").write_text("task text, edited\n", encoding="utf-8")        # a changed task file
    (d / "tasks" / "T-001.md").write_text("an extra task\n", encoding="utf-8")            # a file the build does not make
    (d / "plan" / "p.json").unlink()                                                        # a missing file
    out = FZ.rebuild_round(3, d)
    assert out["differ_or_missing"] == ["plan/p.json", "tasks/T-000.md"]
    assert out["extra_on_disk"] and out["extra_on_disk"][0].endswith("tasks/T-001.md")


def test_rebuild_round_without_a_build_script_checks_nothing_and_blocks_nothing(tmp_path):
    d = _round_dir(tmp_path, {"REDO4_INDEX.json": "{}\n"}, n=4, script=False)
    assert FZ.load_build_module(4, d) is None
    out = FZ.rebuild_round(4, d)
    assert list(out) == ["rebuild"] and "no build script" in out["rebuild"]
    assert not out.get("differ_or_missing") and not out.get("extra_on_disk")


def test_discover_rounds_finds_redo3_in_numeric_order_and_the_real_build_script_loads():
    found, unknown = FZ.discover_rounds()
    assert [n for n, _d, _i in found] == [1, 2, 3] and unknown == []
    n, d, idx = found[2]
    assert d == FZ.HAIKU / "redo3" and idx.name == "REDO3_INDEX.json"
    mod = FZ.load_build_module(3, d)                                  # imported, not run (build() takes about a minute)
    assert callable(mod.build) and mod.OPEN_PIECE == "t28a.skin.email.025"
    assert FZ.load_build_module(2, FZ.HAIKU / "redo2") is not None


# ------------------------------------------------------------------------------------------------ integration
def _snapshot() -> dict:
    """sha256 of every existing file the freeze reads or could touch: T28 (except pools_v2 and this step's own files)
    and the kit."""
    mine = {"freeze_v2.py", "test_freeze_v2.py"}
    out = {}
    for root in (T28, C2_BUILD / "c2_kit"):
        for p in sorted(root.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or "pools_v2" in p.parts or p.name in mine:
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
    assert a["integrity"]["ok"], a["integrity"]["problems"]
    assert a["blockers"] == [], a["blockers"]
    assert _snapshot() == before                                  # no answer, plan, pool or code file was touched
    man = json.loads((FZ.POOLS_V1 / "MANIFEST.json").read_text(encoding="utf-8"))
    assert man["version"] == "freeze-v1" and a["integrity"]["manifest_sha256"] == FZ.sha_file(FZ.POOLS_V1 / "MANIFEST.json")


def test_targets_are_the_v1_targets_and_the_verdict_follows_the_gates(run_a):
    a, _ = run_a
    man = json.loads((FZ.POOLS_V1 / "MANIFEST.json").read_text(encoding="utf-8"))
    assert FZ.G0_TARGETS is PF.G0_TARGETS and FZ.G0_TARGETS == man["targets_g0"]       # never lowered
    assert a["short"] == PF.shortfalls(a["c2"])
    glex, g3 = a["gates"]["G-LEX"], a["gates"]["G3-H"]
    assert a["ready"] == (not a["short"] and glex["pass"] and g3["pass"] and not a["blockers"])
    files = FZ.build_files(a)
    m = json.loads(files["MANIFEST.json"])
    assert m["ready"] == a["ready"] and m["shortfalls"] == a["short"] and m["targets_g0"] == man["targets_g0"]
    assert m["status"].split(":")[0] in ("READY", "SHORT", "BLOCKED")
    if not a["ready"] and not a["blockers"]:
        assert m["status"].startswith("SHORT") and all(s in m["status"] for s in a["short"])


def test_v1_pieces_carry_over_unchanged_and_counts_only_grow(run_a):
    a, _ = run_a
    st1, st2 = a["st1"], a["st2"]
    for sid, sk in st1["skins"].items():
        assert st2["skins"][sid] == sk
    for sid, sk in st1["memos"].items():
        assert st2["memos"][sid] == sk
    assert st2["attacks"] is st1["attacks"]
    assert st2["wordings"][:len(st1["wordings"])] == st1["wordings"]
    assert st2["packs"][:len(st1["packs"])] == st1["packs"]
    assert len(st2["skins"]) >= len(st1["skins"]) and len(st2["memos"]) >= len(st1["memos"])
    for fid, f1 in a["reg1"].forms.items():                      # v1 reads and rejections stand
        assert a["st2"]["status_of"][fid] == a["reg1"].status(fid)
        assert st2["reg"].forms[fid].extractions == f1.extractions


def test_pool_holds_only_admitted_forms_and_pending_forms_stay_out(run_a):
    a, _ = run_a
    st2 = a["st2"]
    reg = st2["reg"]
    assert all(reg.status(w["form_id"]) == "admitted" for w in st2["wordings"])
    pending = [fid for fid, s in st2["status_of"].items() if s == "pending"]
    assert not {w["form_id"] for w in st2["wordings"]} & set(pending)
    for fid, f in reg.forms.items():                             # the kit rule, form by form
        agree = {e for e, s in f.extractions if s == f.sem_id}
        if st2["status_of"][fid] == "admitted":
            assert f.unit_ok and len(agree) >= f.required and all(s == f.sem_id for _, s in f.extractions)
        elif st2["status_of"][fid] == "rejected":
            assert any(s != f.sem_id for _, s in f.extractions)
        elif st2["status_of"][fid] == "pending":
            assert f.unit_ok and len(f.extractions) < f.required


def test_added_pieces_have_provenance_that_matches_the_answer_files(run_a):
    a, _ = run_a
    prov = a["merge"]["provenance"]
    for (pool, iid), p in prov.items():
        f = C2_BUILD / p["answer_file"]
        assert f.is_file() and FZ.sha_file(f) == p["answer_sha256"], (pool, iid)
        assert p["round"].startswith("redo") and p["task"].endswith("@redo1") == (p["round"] == "redo1")
    added_skins = set(a["st2"]["skins"]) - set(a["st1"]["skins"])
    assert added_skins == {f"T28-SK-{iid.split('.', 2)[2]}" for (pool, iid) in prov if pool == "skins"}
    for sk in (a["st2"]["skins"][s] for s in added_skins):
        assert sk.haiku_task_id and sk.haiku_prompt_sha


def test_answer_records_cover_every_file_and_stay_valid_or_rejected_whole(run_a):
    a, _ = run_a
    recs = a["records"]
    assert {r["status"] for r in recs} <= {"valid", "invalid", "missing", "excluded"}
    assert len({r["file"] for r in recs}) == len(recs)
    assert all(r["sha256"] for r in recs if r["status"] in ("valid", "invalid"))
    for r in recs:
        if r["status"] != "valid":
            assert r["problems"]


def test_output_is_deterministic_and_the_manifest_hashes_match(run_a):
    a, _ = run_a
    f1, f2 = FZ.build_files(a), FZ.build_files(a)
    assert f1 == f2
    m = json.loads(f1["MANIFEST.json"])
    assert set(m["sha256"]) == set(f1) - {"MANIFEST.json"}
    assert all(hashlib.sha256(f1[n].encode("utf-8")).hexdigest() == h for n, h in m["sha256"].items())
    assert "created" not in f1["MANIFEST.json"] and m["supersedes"]["version"] == "freeze-v1"
    q = json.loads(f1["QUARANTINE.json"])
    assert q["count"] == len(q["rows"]) == len(a["quarantine"])
    assert len(q["resolved_by_redo"]) == m["resolved_from_v1_quarantine"]
    v1q = json.loads((FZ.POOLS_V1 / "QUARANTINE.json").read_text(encoding="utf-8"))
    stages = ("load-check", "G-SL", "value-lint")
    v1_load = {r["piece"] for r in v1q["rows"] if r["stage"] in stages}
    resolved = {r["piece"] for r in q["resolved_by_redo"]}
    kept = {r["piece"] for r in q["rows"] if r["stage"] in stages}
    assert resolved.isdisjoint(kept) and v1_load <= resolved | kept          # every v1 failure is resolved or still open
    assert all("resolved_by" in r for r in q["resolved_by_redo"])


def test_registry_round_trips_and_load_pools_reads_a_pool_dir(run_a, tmp_path):
    a, _ = run_a
    files = FZ.build_files(a)
    for name, text in files.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    pools = FZ.load_pools(tmp_path)
    st2 = a["st2"]
    assert set(pools["skins"]) == set(st2["skins"]) and set(pools["documents"]) == set(st2["memos"])
    for sid, sk in st2["skins"].items():
        assert pools["skins"][sid] == sk
    assert [w["form_id"] for w in pools["wordings"]] == [w["form_id"] for w in st2["wordings"]]
    assert len(pools["packs"]) == len(st2["packs"]) and pools["manifest"]["version"] == "freeze-v2"
    reg = pools["lexicon"]
    for fid in st2["status_of"]:
        assert reg.status(fid) == st2["status_of"][fid]
    d = json.loads((FZ.POOLS_V1 / "skins.json").read_text(encoding="utf-8"))["skins"][0]
    assert json.loads(json.dumps(dataclasses.asdict(FZ.skin_from_json(d)))) == d


def test_freeze_writes_only_pools_v2_and_refuses_re_freeze_and_blocked_runs(run_a, tmp_path, monkeypatch):
    a, _ = run_a
    target = tmp_path / "pools_v2"
    written = {}
    monkeypatch.setattr(FZ, "POOLS_V2", target)
    monkeypatch.setattr(FZ, "assemble", lambda **kw: a)
    monkeypatch.setattr(FZ.paths, "write_files", lambda root, files, **kw: written.update(root=Path(root), files=files))
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
    target.mkdir()
    (target / "MANIFEST.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(FZ, "assemble", lambda **kw: pytest.fail("a re-freeze must stop before any work"))
    with pytest.raises(SystemExit):
        FZ.run(write=True, rebuild_check=False)


def test_excluded_task_is_ignored_whole_and_the_verdict_follows():
    a = FZ.assemble(rebuild_check=False, exclude=("T28-extract_g3h-d208f80e-000",))     # a failed-audit G3-H read
    rec = [r for r in a["records"] if r["task_id"] == "T28-extract_g3h-d208f80e-000"][0]
    assert rec["status"] == "excluded"
    assert {"T28-MF-070", "T28-MF-092"} <= {s for s, (ok, _) in a["g_ok"].items() if not ok}
    assert not a["ready"] and not a["gates"]["G3-H"]["pass"]
    assert "T28-MF-070" not in a["st2"]["memos"] and "T28-MF-092" not in a["st2"]["memos"]
    assert any("memos" in s for s in a["short"])


def test_redo3_answers_are_folded_into_the_real_freeze(run_a):
    a, _ = run_a
    r3 = [r for r in a["records"] if r["round"] == "redo3"]
    assert len(r3) == 5 and all(r["status"] == "valid" and r["sha256"] and not r["problems"] for r in r3)
    assert {r["kind"] for r in r3} == {"author_skin", "extract_lex"}
    assert a["redo_checks"]["redo3"]["tasks"] == 5 and a["redo_checks"]["redo3"]["valid"] == 5
    assert a["redo_checks"]["redo3"]["rebuild"].startswith("skipped")                # rebuild_check=False in this fixture
    assert a["stray"] == [] and a["unrecognised_rounds"] == []
    # the one open piece (skins email 74 of 75) is filled by exactly one redo3 attempt; the others are logged as unused
    key = ("skins", "t28a.skin.email.025")
    prov = a["merge"]["provenance"][key]
    assert prov["round"] == "redo3" and prov["task"].startswith("T28-author_skin-")
    assert FZ.sha_file(C2_BUILD / prov["answer_file"]) == prov["answer_sha256"]
    tries = [t for t in a["merge"]["attempts"][key] if t["round"] == "redo3"]
    assert len(tries) == 3 and sum(1 for t in tries if t.get("accepted")) == 1
    at = next(i for i, t in enumerate(tries) if t.get("accepted"))
    assert all(t["reasons"] for t in tries[:at])                                       # attempts before it failed a check
    assert all(t.get("ignored") for t in tries[at + 1:])                               # attempts after it are unused
    sk = a["st2"]["skins"]["T28-SK-email.025"]
    assert "T28-SK-email.025" not in a["st1"]["skins"] and sk.haiku_task_id == prov["task"]
    assert a["c2"]["skins_by_register"]["email"]["admitted"] >= 75
    # the redo3 G-LEX reads are recorded: every redo wording they cover has its 2 independent reads and is admitted
    assert set(a["vote_counts"]) >= {"redo3:r3read0", "redo3:r3read1"}
    assert a["vote_counts"]["redo3:r3read0"] == a["vote_counts"]["redo3:r3read1"]
    pending = [f for f, s_ in a["st2"]["status_of"].items() if s_ == "pending"]
    assert pending == []


def test_a_redo3_rebuild_difference_blocks_the_freeze(monkeypatch):
    def fake(n, d, mod=None):
        if n == 3:
            return {"files": 27, "differ_or_missing": ["tasks/T28-author_skin-648cabac-000.md"], "extra_on_disk": []}
        return {"files": 30, "differ_or_missing": [], "extra_on_disk": []}
    monkeypatch.setattr(FZ, "rebuild_round", fake)
    a = FZ.assemble(rebuild_check=True)
    assert a["redo_checks"]["redo3"]["rebuild"]["differ_or_missing"]
    assert a["redo_checks"]["redo2"]["rebuild"]["differ_or_missing"] == []
    assert any(b.startswith("redo3 rebuild differs from disk") for b in a["blockers"])
    assert not a["ready"]


def test_the_merged_pools_plug_into_the_plugin_in_memory(run_a, tmp_path):
    """Load the freeze as the generator would and build real units (nothing is written): every unit passes G2, G3, G4,
    G-SL, G-LEX and G-TW, and only admitted forms are ever offered."""
    from c2_kit import pipeline
    from families.T28 import plugin as P
    a, _ = run_a
    for name, text in FZ.build_files(a).items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    pools = FZ.load_pools(tmp_path)
    ctx = FZ.make_ctx(pools)
    assert all(ctx.lexicon.status(s.lexicon_ids[0]) == "admitted" for s in ctx.skins.values() if s.kind == "wording")
    plugin = P.T28Plugin(lexicon=ctx.lexicon)
    bad = []
    for seed in range(12):
        for smp in plugin.SAMPLERS:
            r = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            if not r.ok:
                bad.append((seed, smp, r.problems[:2]))
    assert bad == []
