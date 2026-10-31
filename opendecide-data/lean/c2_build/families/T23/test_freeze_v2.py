"""families/T23/test_freeze_v2.py: tests of freeze_v2.py (the T23 pool re-freeze after redo2). Nothing is written to disk.

  targets        the G0 minimums are pinned to the numbers in G0_SPEC.md (never lowered); shortfalls are named and exact
  validation     answer-file contracts: every file-level and item-level rejection, the invalid-read rule, round
                 bookkeeping (missing / stray / ignored), the ambiguity-pass file
  votes          G-LEX recording on synthetic registries (a code test, never data): the v1 reads count only with BOTH
                 redo2 reads, any other pick / decoy / invalid choice rejects, 3 reads for strict kinds
  G3-H           exact compare, note-level and register-level 98% templates, kept-note rule
  real data      ONE in-memory build of the real pools (about 100 s): READY with every G0 minimum, v1 reproduced and
                 untouched, the v2 documents hold admitted forms only, outputs go under pools_v2/ only
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T23/test_freeze_v2.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T23 import fixtures as FX  # noqa: E402
from families.T23 import freeze_v2 as F  # noqa: E402
from families.T23 import haiku_author as A  # noqa: E402
from families.T23 import plugin as P  # noqa: E402

HERE = Path(__file__).resolve().parent


# ======================================================================================================= helpers
def _answers(b, per_internal: dict) -> dict:
    """{task_id: [answer objects with qid]} for a TaskBatch from {internal id: answer fields}."""
    inv = {v: k for k, v in b.key.items()}
    out = defaultdict(list)
    for iid, a in per_internal.items():
        out[b.task_of[inv[iid]]].append({"qid": inv[iid], **a})
    return dict(out)


def _registry(n: int = 3) -> LexiconRegistry:
    reg = LexiconRegistry("T23")
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem("T23", qf), "question", meaning)
    for sem, meaning in A.QUESTION_DECOYS.items():
        reg.declare(sem, "question", meaning)
    for _id, qf, text, decl in FX.WORDINGS[:n]:
        reg.add(text, question_sem("T23", qf), slots=dict(decl))
    reg.unit_test_all()
    return reg


def _read_batches(reg: LexiconRegistry, fids: list) -> list:
    out = []
    for r in range(2):
        items = reg.lexicon_items(fids, seed=f"t-r{r}")
        b = chunker.make_batch("extract_lex", "T23", items, seed=f"t-read{r}", prompt="pick the meaning", max_items=50)
        out.append((f"glex-r2read{r}", b))
    return out


def _pick(reg, fid, other=False):
    """The choice text of the form's own meaning (or of another question meaning)."""
    f = reg.forms[fid]
    if other:
        sem = next(s for s in reg.sems.values() if s.kind == "question" and s.sem_id != f.sem_id)
        return sem.meaning
    return reg.sems[f.sem_id].meaning


@pytest.fixture
def no_path_guard(monkeypatch):
    """pytest temp folders are not the subject of the never-open guard."""
    monkeypatch.setattr(F.paths, "check_path", lambda p: Path(p))


# ======================================================================================================= targets
def test_targets_are_the_g0_numbers_and_never_lowered():
    assert F.TARGET == {"wording_total": 30, "wording_per_form": 6, "double_negation_per_positive_form": 3,
                        "packs_used": 25, "skin_registers_training": 8, "skin_registers_heldout": 2, "g3h_rate": 0.98}
    g0 = (HERE / "G0_SPEC.md").read_text(encoding="utf-8")
    assert ">= 30 in total, >= 6 admitted per form" in g0
    assert ">= 3 admitted wordings per positive yn form" in g0
    assert ">= 25 used, one per card" in g0
    assert g3h.PASS_RATE == 0.98
    assert hashlib.sha256(g0.encode("utf-8")).hexdigest() == P.T23.G0_SHA256


def _full_counts(**over):
    base = dict(train_by_form={q: 10 for q in P.QF}, ho_by_form={q: 2 for q in P.QF},
                dneg_by_form={q: 3 for q in F.POSITIVE}, packs_train_by_dom={d: 3 for d in P.DOMAIN_KEYS},
                packs_ho_by_dom={d: 1 for d in P.DOMAIN_KEYS}, train_regs=list(P.T23.REGISTERS[:8]),
                ho_regs=list(P.T23.HELD_OUT_REGISTERS), g3h_note_rate=1.0, g3h_register_rate=0.98)
    base.update(over)
    return base


def test_evaluate_targets_passes_exactly_at_the_floors():
    targets, shortfalls = F.evaluate_targets(**_full_counts(train_by_form={q: 6 for q in P.QF}))
    assert shortfalls == [], shortfalls
    assert targets["base"]["wording_total_training"]["got"] == 66


@pytest.mark.parametrize("over,name", [
    ({"train_by_form": {**{q: 10 for q in P.QF}, "yn_outcome_not": 5}}, "wording yn_outcome_not"),
    ({"train_by_form": {q: 2 for q in P.QF}}, "wording"),
    ({"dneg_by_form": {"yn_version": 3, "yn_claim": 3, "yn_outcome": 2}}, "double-negation wording yn_outcome"),
    ({"packs_train_by_dom": {**{d: 3 for d in P.DOMAIN_KEYS}, "refunds": 2}}, "training packs for domain refunds"),
    ({"packs_ho_by_dom": {**{d: 1 for d in P.DOMAIN_KEYS}, "licences": 0}}, "held-out packs for domain licences"),
    ({"train_regs": list(P.T23.REGISTERS[:7])}, "skin registers (training)"),
    ({"ho_regs": ["notice"]}, "skin registers (held out)"),
    ({"g3h_note_rate": 0.9799}, "G3-H pass rate (template = note)"),
    ({"g3h_register_rate": 0.9}, "G3-H pass rate (template = register)"),
])
def test_evaluate_targets_names_each_shortfall(over, name):
    _t, shortfalls = F.evaluate_targets(**_full_counts(**over))
    assert shortfalls and any(x["target"].startswith(name) for x in shortfalls), shortfalls
    assert all(x["short_by"] > 0 and x["got"] < x["bar"] for x in shortfalls)


def test_pending_forms_are_reported_next_to_the_shortfall():
    _t, shortfalls = F.evaluate_targets(**_full_counts(dneg_by_form={}, cand_train={"yn_version": 9}))
    sf = next(x for x in shortfalls if x["target"].startswith("double-negation wording yn_version"))
    assert sf["short_by"] == 3 and sf["waiting_for_reads"] == 9


def test_pack_card_rule_follows_the_plugin():
    train, held = F.pack_cards()
    assert sum(train.values()) == 24 and sum(held.values()) == 6          # 4 training samplers x 6 cards; S5 x 6
    assert set(train) == set(P.DOMAIN_KEYS) and max(train.values()) == 3


def test_cap_2pct_estimate_uses_the_g0_shares():
    est = F.cap_2pct_estimate({q: 100 for q in P.QF})
    assert est["ch_version"]["wordings_needed"] == 16 and est["ch_term"]["wordings_needed"] == 12
    assert all(v["ok"] for v in est.values())
    assert not F.cap_2pct_estimate({q: 1 for q in P.QF})["ch_version"]["ok"]


# ======================================================================================================= validation
def _def(kind, n=3, choices=None):
    qids = [f"q{i:010d}" for i in range(n)]
    return F.ChunkDef("T23-x-0", kind, qids, {q: list(choices) for q in qids} if choices else {})


def _file(objs) -> bytes:
    return json.dumps(objs).encode("utf-8")


def _ok_text(cd):
    return [{"qid": q, "text": f"text {i}"} for i, q in enumerate(cd.qids)]


def test_valid_files_of_every_kind_are_accepted():
    cd = _def("author_wording")
    rep = F.validate_answer_bytes(_file(_ok_text(cd)), cd)
    assert rep["ok"] and rep["n_valid_items"] == 3 and not rep["item_problems"]
    cd = _def("author_pack")
    assert F.validate_answer_bytes(_file([{"qid": q, "pack": {"doc": "x"}} for q in cd.qids]), cd)["ok"]
    cd = _def("extract_lex", choices=["a", "b"])
    assert F.validate_answer_bytes(_file([{"qid": q, "choice": "a"} for q in cd.qids]), cd)["n_valid_items"] == 3
    cd = _def("extract_g3h")
    row = {"customer": "A B", "org": "C D", "item": None, "case_id": "CASE-1"}
    rep = F.validate_answer_bytes(_file([{"qid": q, **row} for q in cd.qids]), cd)
    assert rep["ok"] and rep["n_valid_items"] == 3                                        # null is allowed for a G3-H field


@pytest.mark.parametrize("mutate,expect", [
    (lambda o: o[:-1], "2 objects"),                                              # an unanswered qid
    (lambda o: o + [dict(o[0])], "used twice"),
    (lambda o: [{**o[0], "qid": "qunknown"}] + o[1:], "unknown qid"),
    (lambda o: [{"qid": o[0]["qid"]}] + o[1:], "keys"),
    (lambda o: [{**o[0], "extra": 1}] + o[1:], "keys"),
    (lambda o: ["text"] + o[1:], "not an object"),
    (lambda o: [{**o[0], "qid": 5}] + o[1:], "qid is not a string"),
])
def test_file_level_rejections(mutate, expect):
    cd = _def("author_wording")
    rep = F.validate_answer_bytes(_file(mutate(_ok_text(cd))), cd)
    assert not rep["ok"] and rep["items"] == [] and any(expect in p for p in rep["file_problems"]), rep["file_problems"]


@pytest.mark.parametrize("data,expect", [
    (b"\xff\xfe[]", "not UTF-8"),
    ("﻿[]".encode("utf-8"), "byte-order mark"),
    (b"not json", "not valid JSON"),
    (b'[{"qid": "q", "qid": "r"}]', "duplicate key"),
    (b"[NaN]", "NaN"),
    (b'{"qid": "q0"}', "not a JSON array"),
])
def test_unreadable_files_are_rejected_whole(data, expect):
    rep = F.validate_answer_bytes(data, _def("author_wording"))
    assert not rep["ok"] and any(expect in p for p in rep["file_problems"]), rep["file_problems"]


def test_unknown_kind_is_rejected():
    assert not F.validate_answer_bytes(b"[]", F.ChunkDef("t", "bogus", [])) ["ok"]


def test_item_level_rejections_keep_the_file_but_drop_the_item():
    cd = _def("author_wording")
    objs = _ok_text(cd)
    objs[1]["text"] = "   "
    rep = F.validate_answer_bytes(_file(objs), cd)
    assert rep["ok"] and rep["n_valid_items"] == 2 and len(rep["item_problems"]) == 1
    cd = _def("author_pack")
    rep = F.validate_answer_bytes(_file([{"qid": q, "pack": "x"} for q in cd.qids]), cd)
    assert rep["ok"] and rep["n_valid_items"] == 0 and len(rep["item_problems"]) == 3
    cd = _def("extract_g3h")
    bad = {"customer": 5, "org": "o", "item": "i", "case_id": "c"}
    rep = F.validate_answer_bytes(_file([{"qid": q, **bad} for q in cd.qids]), cd)
    assert rep["ok"] and rep["n_valid_items"] == 0 and "customer" in rep["item_problems"][0]


def test_an_off_list_choice_stays_as_an_invalid_read_and_is_reported():
    cd = _def("extract_lex", choices=["a", "b"])
    objs = [{"qid": q, "choice": "a"} for q in cd.qids]
    objs[2]["choice"] = "something else"
    rep = F.validate_answer_bytes(_file(objs), cd)
    assert rep["ok"] and rep["n_valid_items"] == 3 and "invalid read" in rep["item_problems"][0]
    objs[2]["choice"] = ""
    rep = F.validate_answer_bytes(_file(objs), cd)
    assert rep["n_valid_items"] == 2                                              # an empty choice is no read at all


def test_validate_round_missing_stray_and_ignored(tmp_path, no_path_guard):
    defs = {t: F.ChunkDef(t, "author_wording", [f"{t}-q"]) for t in ("T23-a-0", "T23-a-1", "T23-a-2", "T23-a-3")}
    d = tmp_path / "answers"
    d.mkdir()
    for t in ("T23-a-0", "T23-a-1", "T23-a-3"):
        (d / f"{t}.json").write_text(json.dumps([{"qid": f"{t}-q", "text": "hello there"}]), encoding="utf-8")
    (d / "T23-a-1.json").write_text("garbage", encoding="utf-8")
    (d / "stray.json").write_text("[]", encoding="utf-8")
    (d / "notes.txt").write_text("x", encoding="utf-8")
    rep = F.validate_round("r", defs, d, ignore=("T23-a-3",))
    assert rep["missing"] == ["T23-a-2"] and sorted(rep["stray"]) == ["notes.txt", "stray.json"]
    assert rep["rejected"] == ["T23-a-1"] and rep["ignored"] == ["T23-a-3"]
    assert sorted(F.accepted(rep)) == ["T23-a-0"]                                 # rejected and ignored files are not used
    assert "items" not in next(iter(F.slim(rep)["files"].values()))


def test_nothing_is_edited_by_validation(tmp_path, no_path_guard):
    d = tmp_path / "answers"
    d.mkdir()
    f = d / "T23-a-0.json"
    f.write_text("garbage", encoding="utf-8")
    before = f.read_bytes()
    F.validate_round("r", {"T23-a-0": F.ChunkDef("T23-a-0", "author_wording", ["q"])}, d)
    assert f.read_bytes() == before


def test_ambiguity_pass_file_validates_and_mutations_fail(tmp_path):
    path = HERE / "haiku" / "ambiguity" / "amb_T23_points.json"
    rep = F.validate_ambiguity(path)
    assert rep["ok"] and rep["n_points"] == 48 and not rep["file_problems"]
    assert len(rep["item_problems"]) == 1 and "no competing readings" in rep["item_problems"][0]
    o = json.loads(path.read_text(encoding="utf-8"))

    def run(obj):
        p = tmp_path / "amb.json"
        p.write_text(json.dumps(obj), encoding="utf-8")
        return F.validate_ambiguity(p)
    bad = copy.deepcopy(o)
    bad["points"][0]["issue"] = "changed"
    assert not run(bad)["ok"]                                                     # the sha no longer matches
    bad = copy.deepcopy(o)
    bad["n_points"] = 47
    assert not run(bad)["ok"]
    bad = copy.deepcopy(o)
    del bad["points"][0]["where"]
    assert not run(bad)["ok"]
    bad = copy.deepcopy(o)
    bad["extra"] = 1
    assert not run(bad)["ok"]


def test_chunk_integrity_detects_a_changed_chunk(tmp_path):
    root = tmp_path / "round"
    for sub in ("chunks", "manifest", "prompts"):
        (root / sub).mkdir(parents=True)
    items = [("form-id-0001", {"text": "hello", "choices": ["x", "y"]})]
    b = chunker.make_batch("extract_lex", "T23", items, seed="s", prompt="prompt text")
    for rel, text in b.files().items():
        if not rel.startswith("key/"):
            (root / rel).write_text(text, encoding="utf-8")
    assert F.chunk_integrity(root)["ok"]
    cf = root / b.chunk_path(b.chunks[0]["task_id"])
    cf.write_text(cf.read_text(encoding="utf-8").replace("hello", "HELLO"), encoding="utf-8")
    rep = F.chunk_integrity(root)
    assert not rep["ok"] and "differs from its manifest" in rep["problems"][0]


# ======================================================================================================= votes
def test_record_reads_maps_choices_to_sems_and_flags_invalid_reads():
    reg = _registry(4)
    fids = sorted(reg.forms)
    named = _read_batches(reg, fids)
    raw0 = _answers(named[0][1], {fids[0]: {"choice": _pick(reg, fids[0])}, fids[1]: {"choice": _pick(reg, fids[1], True)},
                                  fids[2]: {"choice": "not a listed choice"}, fids[3]: {"choice": _pick(reg, fids[3])}})
    votes, summ, probs = F.record_reads(reg, named[:1], raw0)
    assert [votes[f][0]["sem"] == reg.forms[f].sem_id for f in fids[:2] + fids[3:]] == [True, False, True]
    assert votes[fids[2]][0]["sem"] is None and votes[fids[2]][0]["valid"] is False
    assert summ[0]["outcomes"] == {"match": 2, "other_meaning": 1, "invalid": 1} and not probs
    assert [reg.status(f) for f in fids] == ["pending", "rejected", "rejected", "pending"]      # invalid rejects (kit rule)


def test_an_unanswered_item_gets_no_record():
    reg = _registry(2)
    fids = sorted(reg.forms)
    named = _read_batches(reg, fids)
    votes, summ, probs = F.record_reads(reg, named[:1], _answers(named[0][1], {fids[0]: {"choice": _pick(reg, fids[0])}}))
    assert fids[1] not in votes and summ[0]["outcomes"]["unanswered"] == 1 and probs   # reported by the chunk loader
    assert reg.status(fids[1]) == "pending" and not reg.forms[fids[1]].extractions


def _with_v1_votes(reg, fids):
    for f in fids:
        reg.record_extraction(f, "glex-read0", reg.forms[f].sem_id)
        reg.record_extraction(f, "glex-read1", reg.forms[f].sem_id)


def test_v1_reads_alone_admit_nothing_and_both_redo2_reads_are_needed():
    reg = _registry(3)
    fids = sorted(reg.forms)
    _with_v1_votes(reg, fids)
    assert [reg.status(f) for f in fids] == ["admitted"] * 3                      # the kit alone would admit on v1 reads
    assert [F.r2_status(reg, f) for f in fids] == ["pending_read_missing"] * 3    # G0 v3 10 B1: they admit nothing alone
    reg.record_extraction(fids[0], "glex-r2read0", reg.forms[fids[0]].sem_id)
    assert F.r2_status(reg, fids[0]) == "pending_read_missing"                    # one redo2 read is not enough
    reg.record_extraction(fids[0], "glex-r2read1", reg.forms[fids[0]].sem_id)
    assert F.r2_status(reg, fids[0]) == "admitted"


def test_one_disagreeing_or_decoy_or_invalid_read_rejects_for_good():
    reg = _registry(4)
    fids = sorted(reg.forms)
    _with_v1_votes(reg, fids)
    reg.record_extraction(fids[0], "glex-r2read0", reg.forms[fids[0]].sem_id)
    reg.record_extraction(fids[0], "glex-r2read1", next(s for s in reg.sems if s != reg.forms[fids[0]].sem_id))
    reg.record_extraction(fids[1], "glex-r2read0", "q.t23.decoy_today")
    reg.record_extraction(fids[2], "glex-r2read0", None)                          # an invalid read
    assert [F.r2_status(reg, f) for f in fids[:3]] == ["rejected"] * 3
    assert F.r2_status(reg, fids[3]) == "pending_read_missing"
    reg.record_extraction(fids[1], "glex-r2read1", reg.forms[fids[1]].sem_id)
    assert F.r2_status(reg, fids[1]) == "rejected"                                # no re-vote after a bad read


def test_a_v1_disagreement_stays_final_whatever_the_redo2_reads_say():
    reg = _registry(1)
    fid = sorted(reg.forms)[0]
    reg.record_extraction(fid, "glex-read0", reg.forms[fid].sem_id)
    reg.record_extraction(fid, "glex-read1", "q.t23.yn_claim_contra")
    for r in range(2):
        reg.record_extraction(fid, f"glex-r2read{r}", reg.forms[fid].sem_id)
    assert F.r2_status(reg, fid) == "rejected"


def test_strict_kinds_need_three_distinct_redo2_reads():
    reg = _registry(0)
    reg.declare("prec.P1", "precedence", "deny rules beat ask rules")
    f = reg.add("deny rules beat ask rules, which beat allow rules", "prec.P1", slots={})
    reg.unit_test_all()
    assert f.required == 3
    for i in range(2):
        reg.record_extraction(f.form_id, f"glex-r2read{i}", "prec.P1")
    assert F.r2_status(reg, f.form_id) == "pending_read_missing"                  # 2/2 is not enough for precedence
    reg.record_extraction(f.form_id, "glex-r2read2", "prec.P1")
    assert F.r2_status(reg, f.form_id) == "admitted"


def test_a_form_without_a_passed_unit_test_is_never_admitted():
    reg = _registry(1)
    fid = sorted(reg.forms)[0]
    reg.forms[fid].unit_ok = False
    for r in range(2):
        reg.record_extraction(fid, f"glex-r2read{r}", reg.forms[fid].sem_id)
    assert F.r2_status(reg, fid) == "unit_fail"


# ======================================================================================================= G3-H
def _g3_batch(n: int, register_of=lambda i: "memo"):
    fields = P.T23.extract_fields(None, None)
    items, expected = [], {}
    for i in range(n):
        sid = f"S{i:03d}"
        items.append((sid, g3h.extraction_item(f"note {i}", fields)))
        expected[sid] = {"register": register_of(i), "expected": {"customer": f"Cu {i}", "org": f"Or {i}",
                                                                   "item": f"item {i}", "case_id": f"CASE-{i}"}}
    return chunker.make_batch("extract_g3h", "T23", items, seed="g", prompt="read", max_items=40), expected


def _g3_answers(b, expected, bad=()):
    per = {}
    for sid, e in expected.items():
        a = dict(e["expected"])
        if sid in bad:
            a["item"] = "the " + a["item"]
        per[sid] = a
    return _answers(b, per)


def test_g3h_all_exact_passes_at_both_template_levels():
    b, exp = _g3_batch(10)
    rep = F.g3h_compare(b, exp, _g3_answers(b, exp))
    assert rep["pass"] == rep["kept"] == 10 and rep["pass_ok"] and rep["per_register"]["all_templates_pass"]


def test_g3h_a_determiner_is_a_mismatch_and_the_note_is_dropped():
    b, exp = _g3_batch(50)
    rep = F.g3h_compare(b, exp, _g3_answers(b, exp, bad={"S007"}))
    assert rep["pass"] == 49 and rep["kept"] == 49                                # 49/50 = 98%: the register passes
    r = next(x for x in rep["rows"] if x["sid"] == "S007")
    assert not r["ok"] and not r["kept"] and "item" in r["diffs"][0]
    assert rep["per_note"]["quarantined"] == ["S007"] and not rep["pass_ok"]       # the note-level template fails


def test_g3h_a_register_below_98_percent_drops_every_note_of_it():
    b, exp = _g3_batch(60, register_of=lambda i: "memo" if i < 40 else "chat")
    rep = F.g3h_compare(b, exp, _g3_answers(b, exp, bad={"S001", "S002"}))        # memo: 38/40 = 95%
    assert rep["per_register"]["quarantined"] == ["memo"]
    assert rep["kept"] == 20 and all(r["kept"] == (r["register"] == "chat") for r in rep["rows"])
    assert rep["pass"] == 58 and not rep["pass_ok"]


def test_g3h_an_unanswered_note_fails():
    b, exp = _g3_batch(5)
    ans = _g3_answers(b, exp)
    first = next(iter(ans))
    ans[first] = ans[first][:-1]
    rep = F.g3h_compare(b, exp, ans)
    assert rep["pass"] == 4 and any(r["diffs"] == ["unanswered"] for r in rep["rows"])
    assert rep["problems"]                                                        # the chunk loader reports it


def test_g3h_missing_task_is_reported():
    b, exp = _g3_batch(5)
    rep = F.g3h_compare(b, exp, {})
    assert rep["pass"] == 0 and rep["missing_tasks"] and not rep["pass_ok"]


# ======================================================================================================= write guard
def test_the_writer_refuses_the_v1_folder_and_needs_a38(monkeypatch):
    with pytest.raises(PermissionError):
        F.refuse_v1_path(F.V1_POOLS / "x.json")
    with pytest.raises(PermissionError):
        F.refuse_v1_path(F.V1_POOLS)
    F.refuse_v1_path(F.POOLS_V2 / "MANIFEST.json")                               # pools_v2 is fine
    assert F.POOLS_V2 != F.V1_POOLS and F.POOLS_V2.name == "pools_v2"

    def no_a38(*a, **k):
        raise paths.DataBeforeFreeze("no A38")
    monkeypatch.setattr(F.paths, "require_a38", no_a38)
    with pytest.raises(paths.DataBeforeFreeze):
        F.write_freeze(object(), {})


def test_cli_rejects_unknown_commands(capsys):
    assert F.main(["bogus"]) == 2


# ======================================================================================================= real data
def _memo_dneg(calls: dict, orig):
    """A test-level memo of the (slow) double-negation registry step, keyed by the authoring answers only."""
    def wrapper(R, reg1, raw):
        key = json.dumps({k: v for k, v in raw.items() if "author_wording" in k}, sort_keys=True)
        if key not in calls:
            calls[key] = orig(R, reg1, raw)
        out = calls[key]
        return (copy.deepcopy(out[0]),) + out[1:]
    return wrapper


@pytest.fixture(scope="module")
def real():
    """ONE build of the real pools (about 100 s). The double-negation registry step is memoised so that the sensitivity
    test below does not repeat its unit tests."""
    calls = {}
    orig = F.dneg_forms_validated
    F.dneg_forms_validated = _memo_dneg(calls, orig)
    try:
        s = F.build()
        s.summary = F.summarize(s)
        s.memo, s.orig_dneg = calls, orig
        yield s
    finally:
        F.dneg_forms_validated = orig


def test_real_freeze_is_ready_and_every_g0_minimum_is_met(real):
    s = real
    assert s.ready, (s.shortfalls, s.failed_checks, s.answer_problems)
    assert s.shortfalls == [] and s.failed_checks == [] and s.answer_problems == []
    assert len(s.notes) == 1 and "point 47" in s.notes[0]                       # informational: the ambiguity pass
    assert s.summary["status"].startswith("READY")
    assert s.gate_used["pass"] and s.gate_used["n_forms"] == s.counts["lexicon"]["status"]["admitted"]
    assert s.g3h_pass and s.g3["pass"] == s.g3["n"] == len(s.kept["freeform"]) == 172
    walk = list(s.targets["wording_per_form"].values()) + list(s.targets["double_negation"].values()) + \
        list(s.targets["base"].values()) + list(s.targets["packs"].values())
    assert all(x["pass"] for x in walk)
    assert all(v["training"]["pass"] and v["held_out"]["pass"] for v in s.targets["pack_cards"]["coverage"].values())
    for qf in P.QF:
        assert s.targets["wording_per_form"][qf]["bar"] == 6
    for qf in F.POSITIVE:
        assert s.targets["double_negation"][qf]["bar"] == 3 and s.targets["double_negation"][qf]["got"] >= 3


def test_real_status_counts_and_redo2_reads(real):
    s = real
    assert s.counts["lexicon"]["status"] == {"admitted": 222, "excluded_frame": 10, "rejected_v1": 1}
    assert len(s.new_forms) == 27 and s.counts["wordings"]["double_negation_by_qform"] == {
        "yn_claim": 9, "yn_outcome": 9, "yn_version": 9}
    for stage in s.r2_summaries.values():
        for rd in stage:
            assert not rd["tasks_without_valid_answer"] and set(rd["outcomes"]) <= {"match", "other_meaning", "invalid",
                                                                                    "unanswered"}
    assert not s.pending and not s.dn_drops
    # every admitted form carries 2 v1 reads (v1 forms) and 2 distinct redo2 reads
    for fid, st in s.status.items():
        if st == "admitted":
            ex = [e for e, _ in s.reg.forms[fid].extractions]
            assert sum(e.startswith("glex-r2") for e in ex) == 2 and len(set(ex)) == len(ex)


def test_real_checks_all_hold_and_the_inputs_are_what_was_issued(real):
    s = real
    assert s.checks and all(s.checks.values()), {k: v for k, v in s.checks.items() if not v}
    for must in ("author_batches_match_disk", "extract_batches_match_disk", "v1_registry_reproduced",
                 "redo2_stage_a_files_match_disk", "redo2_stage_b_files_match_disk", "g3h_batch_matches_disk",
                 "chunk_files_match_manifests", "loader_drops_match_v1_quarantine", "ambiguity_pass_file_valid"):
        assert s.checks[must] is True
    for name, r in s.rounds.items():
        assert not r["rejected"] and not r["missing"] and not r["stray"] and not r["ignored"], name
    assert [len(r["files"]) for r in s.rounds.values()] == [23, 15, 16]
    assert sorted(s.redo2_tasks["A"] + s.redo2_tasks["B"]) == sorted(s.rounds["redo2"]["files"])
    assert len(s.redo2_tasks["B"]) == 2


def test_real_v1_is_reproduced_and_untouched(real):
    s = real
    c = s.summary["v1_comparison"]
    for rel in ("packs.json", "skins.json", "attacks.json"):
        assert c[rel]["identical_to_v1"] and c[rel]["v1_file_matches_its_manifest"]
    assert c["v1_pool_files_untouched"]
    assert c["freeform.json"]["every_v1_note_kept_unchanged"] and c["freeform.json"]["v1_reproduced_from_v1_g3h_read"]
    assert (c["freeform.json"]["v1_notes"], c["freeform.json"]["v2_notes"], len(c["freeform.json"]["added_vs_v1"])) == (
        162, 172, 10)
    w = c["wordings.json"]
    assert w["kept_fields_unchanged"] and w["kept_v1_extractions_are_a_prefix"]
    assert (w["v1_admitted"], w["v1_kept"], len(w["v1_dropped"]), len(w["v2_new"])) == (199, 195, 4, 27)
    q = c["quarantine.json"]
    assert q["v1_entries_otherwise_missing"] == [] and q["v1_entries_superseded"] == 10
    on_disk = {k: hashlib.sha256((F.V1_POOLS / k).read_bytes()).hexdigest()
               for k in json.loads((F.V1_POOLS / "manifest.json").read_text(encoding="utf-8"))["pool_files_sha256"]}
    assert on_disk == json.loads((F.V1_POOLS / "manifest.json").read_text(encoding="utf-8"))["pool_files_sha256"]


def test_real_documents_hold_admitted_forms_only(real):
    s = real
    R = s.R
    lex = s.docs["lexicon.json"]
    admitted = set(lex["admitted_form_ids"])
    assert {f["form_id"] for f in lex["forms"]} == admitted == {w["form_id"] for w in s.wordings}
    assert not admitted & set(lex["not_admitted"])
    assert set(lex["not_admitted"].values()) == {"excluded_frame", "rejected_v1"}
    for w in s.wordings:
        assert not R.frame_problems(w["text"]), w["text"]                         # the frame rule holds on every form
        assert w["double_negation"] == (R.k_syn(w["text"]) == 2)
        if w["double_negation"]:
            assert not R.no_word_hits(w["text"]) and not w["held_out"]
        ex = [e for e, _ in w["extractors"]]
        assert all(sem == w["form_id"].split("#")[0] for _e, sem in w["extractors"]) and len(ex) >= 2
    reg = LexiconRegistry.from_json(lex)
    assert reg.gate()["pass"] and len(reg.forms) == len(admitted)
    # held-out wordings and skins stay apart from the training ones
    assert not [w for w in s.wordings if w["held_out"] and w["double_negation"]]
    assert {sk["register"] for sk in s.kept["skins"] if sk["held_out"]} == set(P.T23.HELD_OUT_REGISTERS)
    assert not {sk["register"] for sk in s.kept["skins"] if not sk["held_out"]} & set(P.T23.HELD_OUT_REGISTERS)
    for pk in s.kept["packs"]:
        assert pk["held_out"] == pk["iid"].endswith(".3")
    assert Counter(a["held_out"] for a in s.kept["attacks"]) == {False: 48, True: 11}


def test_real_freeform_notes_all_match_and_keep_their_facts(real):
    s = real
    rows = {r["sid"]: r for r in s.g3["rows"]}
    assert all(r["ok"] and r["kept"] and not r["diffs"] for r in rows.values())
    for note in s.kept["freeform"]:
        assert note["author_mode"] == "F" and note["skin_id"] in rows
        facts = dict(map(tuple, note["brief"]))
        assert all(v in note["text"] for v in facts.values())                     # fact-lock: every fact verbatim
    assert set(s.g3["per_register"]["templates"]) == set(A.FREEFORM_REGISTERS)


def test_real_outputs_go_under_pools_v2_only(real, monkeypatch):
    s = real
    summary = copy.deepcopy(s.summary)
    written = {}
    monkeypatch.setattr(F.paths, "write_files", lambda root, files, **kw: written.update(root=Path(root), files=files))
    F.write_freeze(s, summary)
    assert written["root"] == F.POOLS_V2 != F.V1_POOLS
    assert set(written["files"]) == set(F.FILES_V2) | {"validation_report.json", "glex_votes_report.json",
                                                       "g3h_compare_report.json", "MANIFEST.json"}
    man = json.loads(written["files"]["MANIFEST.json"])
    assert man["ready"] is True and man["status"].startswith("READY") and man["audit_failed_ignored"] == []
    for name, meta in man["pool_files"].items():
        assert meta["sha256"] == hashlib.sha256(written["files"][name].encode("utf-8")).hexdigest()
        assert meta["bytes"] == len(written["files"][name].encode("utf-8"))
    for name, meta in man["reports"].items():
        assert meta["sha256"] == hashlib.sha256(written["files"][name].encode("utf-8")).hexdigest()
    assert man["g0"]["sha256"] == man["g0"]["pinned_in_plugin"] == P.T23.G0_SHA256
    assert man["supersedes"]["sha256"] == hashlib.sha256((F.V1_POOLS / "manifest.json").read_bytes()).hexdigest()
    assert "plugin.py reads no pool path" in man["promote"]
    # the quarantine and the lexicon carry no pending form and no label word was authored into a pool by this script
    assert json.loads(written["files"]["lexicon.json"])["not_admitted"] == s.docs["lexicon.json"]["not_admitted"]


def test_real_outputs_are_deterministic_and_g13_skips_the_reports(real):
    s = real
    a, b = F.freeze_outputs(s, copy.deepcopy(s.summary)), F.freeze_outputs(s, copy.deepcopy(s.summary))
    assert a == b
    src = (C2_BUILD.parent / "c_build" / "decontam_g13.py").read_text(encoding="utf-8")       # code only, never imported
    line = next(ln for ln in src.splitlines() if ln.startswith("SEED_SKIP = re.compile("))
    skip = re.compile(re.search(r're\.compile\(r"([^"]+)"', line).group(1), re.I)
    assert {n for n in a if skip.search(n)} == {"validation_report.json", "glex_votes_report.json",
                                                "g3h_compare_report.json", "MANIFEST.json"}


def test_real_audit_failed_stage_b_files_would_make_it_short(real, monkeypatch):
    """Sensitivity: if the two stage-B answer files were ignored, the 27 new double-negation forms stay pending (no
    redo2 reads), no positive form has its 3 double negations and the freeze is SHORT, never READY."""
    ids = tuple(real.redo2_tasks["B"])
    monkeypatch.setattr(F, "dneg_forms_validated", _memo_dneg(real.memo, real.orig_dneg))
    s2 = F.build(audit_failed=ids)
    assert not s2.ready and s2.audit_failed == sorted(ids)
    assert sorted(s2.rounds["redo2"]["ignored"]) == sorted(ids)
    dn = {x["target"]: x for x in s2.shortfalls if x["target"].startswith("double-negation")}
    assert len(dn) == 3 and all(x["got"] == 0 and x["short_by"] == 3 and x["waiting_for_reads"] == 9 for x in dn.values())
    assert len(s2.pending) == 27 and s2.counts["lexicon"]["status"]["pending_read_missing"] == 27
    assert s2.gate_used["pass"]                                                   # the used forms are still all admitted
    assert F.summarize(s2)["status"].startswith("SHORT")
