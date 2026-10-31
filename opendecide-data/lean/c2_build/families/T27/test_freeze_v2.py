"""families/T27/test_freeze_v2.py: tests for freeze_v2.py (validation, vote recording, targets, pool documents) and
pools_v2.py (loader). Nothing under lean/ is written: the real answer files are only read, pool texts are rendered in
memory, and the loader round trip uses pytest's temp folder.
Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q families/T27/test_freeze_v2.py
"""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from families.T27 import authoring as A  # noqa: E402
from families.T27 import extract_check as E  # noqa: E402
from families.T27 import freeze_v2 as FZ  # noqa: E402
from families.T27 import pools_v2 as PV  # noqa: E402
from families.T27 import vocab as V  # noqa: E402

PY = sys.executable


def _cd(kind="author_wording", **kw):
    qids = ["q1", "q2", "q3"]
    internal = {"q1": "skin|web_page|L1|train_a", "q2": "pack|train", "q3": "wording|yn_beyond"}
    return FZ.ChunkDef("T27-test-000", kind, qids, internal, {"q1": 2, "q2": 1, "q3": 2}, **kw)


GOOD = {"q1": [["Hello", "{cap|REQ1}."], ["Hi", "{cap|INFO}."]],
        "q2": [{"setting": "a fitness studio", "names": ["Sable Street", "Pine Row"]}],
        "q3": ["Does it go beyond the task?", "Is it outside the task?"]}


def _b(o) -> bytes:
    return json.dumps(o).encode()


# ---------------------------------------------------------------------------------------------------- strict JSON
def test_strict_loads_rejects_duplicate_keys_and_nan():
    assert FZ.strict_loads(b'{"a": 1}') == {"a": 1}
    with pytest.raises(FZ._Strict):
        FZ.strict_loads(b'{"a": 1, "a": 2}')
    with pytest.raises(FZ._Strict):
        FZ.strict_loads(b'{"a": NaN}')
    with pytest.raises(Exception):
        FZ.strict_loads(b'\xef\xbb\xbf{"a": 1}')                 # a BOM is not strict JSON


# ---------------------------------------------------------------------------------------------------- author contract
def test_author_answer_ok_and_counts_noted():
    r = FZ.validate_answer(_b(GOOD), _cd())
    assert r["ok"] and set(r["accepted"]) == {"q1", "q2", "q3"} and r["notes"] == [] and not r["item_rejects"]
    short = dict(GOOD, q3=["Only one question?"])
    r = FZ.validate_answer(_b(short), _cd())
    assert r["ok"] and r["notes"] and "brief asks 2" in r["notes"][0]            # a count break is a note, not a reject


@pytest.mark.parametrize("payload", [b"not json", b"[]", b'["q1"]', b'{"q1": []}', b'{"q1": 1, "q1": 2}'])
def test_author_file_level_rejects(payload):
    r = FZ.validate_answer(payload, _cd())
    assert not r["ok"] and r["accepted"] is None and r["reasons"]


def test_author_wrong_key_set_is_rejected():
    r = FZ.validate_answer(_b({k: v for k, v in GOOD.items() if k != "q3"}), _cd())
    assert not r["ok"] and "unanswered" in r["reasons"][0]
    r = FZ.validate_answer(_b(dict(GOOD, extra=["x"])), _cd())
    assert not r["ok"] and "not qids of this task" in r["reasons"][0]


def test_author_bad_item_is_rejected_alone():
    bad = dict(GOOD, q1=["a text that is a plain string, not a list of lines"])
    r = FZ.validate_answer(_b(bad), _cd())
    assert r["ok"] and list(r["item_rejects"]) == ["q1"] and set(r["accepted"]) == {"q2", "q3"}
    bad = dict(GOOD, q2=[{"setting": "x", "names": "not a list"}], q3="not a list")
    r = FZ.validate_answer(_b(bad), _cd())
    assert set(r["item_rejects"]) == {"q2", "q3"} and set(r["accepted"]) == {"q1"}
    allbad = {"q1": "x", "q2": "y", "q3": "z"}
    r = FZ.validate_answer(_b(allbad), _cd())
    assert not r["ok"] and r["accepted"] is None


# ---------------------------------------------------------------------------------------------------- extract contract
CLOSED = frozenset({"means A", "means B"})


def _xd():
    return FZ.ChunkDef("T27-extract-000", "extract_lex", ["q1", "q2"], {"q1": "f1", "q2": "f2"}, {}, "deontic")


def test_extract_answer_contract_and_agreement_with_extract_check_judge():
    batch = SimpleNamespace(kind="deontic", chunks=[{"items": [{"qid": "q1"}, {"qid": "q2"}]}], key={"q1": "f1", "q2": "f2"})
    cases = [({"q1": "means A", "q2": "means B"}, True), ({"q1": "means A"}, False),
             ({"q1": "means A", "q2": "means C"}, False), ({"q1": "means A", "q2": "means B", "q3": "means A"}, False),
             ({"q1": "means A", "q2": ["means B"]}, False), ([], False)]
    for raw, ok in cases:
        mine = FZ.validate_answer(_b(raw), _xd(), CLOSED)
        theirs = E.judge(batch, set(CLOSED), raw)[0] == "valid"
        assert mine["ok"] is ok and theirs is ok, raw
        assert (mine["accepted"] is not None) is ok


def test_closed_lists_cover_all_three_kinds():
    cl = FZ.closed_lists()
    assert set(cl) == {"deontic", "other", "question"} and all(cl.values())
    assert V.QUESTION_MEANINGS["yn_dneg_beyond"] in cl["question"]


# ---------------------------------------------------------------------------------------------------- rounds
def test_validate_round_missing_stray_and_ignored(tmp_path):
    defs = {"T-a": _xd(), "T-b": _xd(), "T-c": _xd()}
    (tmp_path / "T-a.json").write_text(json.dumps({"q1": "means A", "q2": "means B"}))
    (tmp_path / "T-b.json").write_text(json.dumps({"q1": "means A", "q2": "nope"}))
    (tmp_path / "T-z.json").write_text("{}")
    rep = FZ.validate_round("t", defs, tmp_path, closed_of=lambda c: CLOSED)
    assert rep["rejected"] == ["T-b"] and rep["missing"] == ["T-c"] and rep["stray"] == ["T-z.json"]
    assert list(FZ.accepted(rep)) == ["T-a"]
    rep = FZ.validate_round("t", defs, tmp_path, closed_of=lambda c: CLOSED, ignored={"T-a"})     # failed audit
    assert rep["rejected"] == ["T-a", "T-b"] and "audit failed" in rep["files"]["T-a"]["reasons"][-1]
    rep = FZ.validate_round("t", defs, tmp_path, closed_of=lambda c: CLOSED, ignored={str((tmp_path / "T-a.json").resolve())})
    assert "T-a" in rep["rejected"]
    assert FZ.slim(rep)["files"]["T-a"].get("accepted") is None and "accepted" not in FZ.slim(rep)["files"]["T-a"]


def test_pick_extract_one_read_per_task():
    def rnd(files, missing=()):
        return {"files": files, "missing": list(missing)}

    def f(ok, answer, sha="s"):
        return {"ok": ok, "accepted": answer if ok else None, "sha256": sha}

    ex = rnd({"t1": f(True, {"q": "A"}, "x"), "t2": f(False, None), "t3": f(True, {"q": "A"}), "t4": f(False, None)},
             ["t5"])
    rd = rnd({"t1": f(True, {"q": "A"}, "x"), "t2": f(True, {"q": "B"}), "t3": f(True, {"q": "B"}), "t4": f(False, None)})
    picks, notes = FZ.pick_extract(ex, rd)
    assert picks["t1"]["source"] == "extract" and "byte-identical" in notes["t1"]
    assert picks["t2"]["source"] == "redo" and picks["t2"]["answer"] == {"q": "B"}
    assert "t3" not in picks and "CONFLICT" in notes["t3"]                  # two valid copies that differ: neither used
    assert "t4" not in picks and notes["t4"] == "no valid answer"
    assert "t5" not in picks


def test_pick_extract_names_label_the_two_copies():
    def f(ok, answer, sha="s"):
        return {"ok": ok, "accepted": answer if ok else None, "sha256": sha}

    prim = {"files": {"t1": f(True, {"q": "A"}), "t2": f(True, {"q": "A"}), "t3": f(False, None)}, "missing": ["t4"]}
    redo3 = {"files": {"t1": f(True, {"q": "A"}), "t2": f(True, {"q": "B"}), "t3": f(True, {"q": "C"}),
                       "t4": f(True, {"q": "D"})}, "missing": []}
    picks, notes = FZ.pick_extract(prim, redo3, names=("redo2/extract", "redo3"))
    assert picks["t1"]["source"] == "redo2/extract" and "redo2/extract copy and redo3 copy" in notes["t1"]
    assert "t2" not in picks and notes["t2"].startswith("CONFLICT: haiku/redo2/extract and haiku/redo3")
    assert picks["t3"]["source"] == "redo3" and notes["t3"] == "redo3 copy only (redo2/extract copy rejected)"
    assert picks["t4"]["source"] == "redo3" and notes["t4"] == "redo3 copy only"          # the primary folder never answered
    only3 = FZ.pick_extract({"files": {}, "missing": []}, redo3, names=("redo2/extract", "redo3"))[0]
    assert set(only3) == {"t1", "t2", "t3", "t4"}


def test_validate_round_also_and_distrust(tmp_path):
    defs = {"T-a": _xd()}
    (tmp_path / "T-a.json").write_text(json.dumps({"q1": "means A", "q2": "means B"}))
    (tmp_path / "T-other.json").write_text("{}")
    assert FZ.validate_round("t", defs, tmp_path, closed_of=lambda c: CLOSED)["stray"] == ["T-other.json"]
    rep = FZ.validate_round("t", defs, tmp_path, closed_of=lambda c: CLOSED, also=frozenset({"T-other"}))
    assert rep["stray"] == [] and rep["rejected"] == []
    bad = FZ.distrust(rep, "task files differ")
    assert bad["rejected"] == ["T-a"] and not bad["files"]["T-a"]["ok"] and bad["files"]["T-a"]["accepted"] is None
    assert bad["files"]["T-a"]["reasons"][-1] == "task files differ" and rep["files"]["T-a"]["ok"]      # a copy
    assert FZ.accepted(bad) == {}


# ---------------------------------------------------------------------------------------------------- redo3 (real files)
def test_author_defs_reads_the_redo3_format_and_skips_the_read_tasks():
    d = FZ.author_defs(FZ.REDO3)
    assert list(d) == ["T27-author_wording-1c307a88-000"]
    cd = d["T27-author_wording-1c307a88-000"]
    assert cd.kind == "author_wording" and list(cd.internal.values()) == ["wording|yn_dneg_beyond"]
    assert list(cd.expect_n.values()) == [3]
    assert set(FZ.author_defs(FZ.REDO2)) and all(t.startswith("T27-author_") for t in FZ.author_defs(FZ.REDO2))


def test_redo3_authoring_task_matches_the_redo2_brief_and_lints_clean():
    batches = FZ.redo3_author_batches(FZ.REDO3)
    assert len(batches) == 1 and FZ.redo3_author_problems(batches, FZ.REDO3) == []
    td, b = batches[0]
    assert td["kind"] == "author_wording" and b.batch_id == "T27-author_wording-1c307a88" and len(b.key) == 1
    raw = json.loads((FZ.REDO3 / "answers" / f"{b.chunks[0]['task_id']}.json").read_text(encoding="utf-8"))
    rep = A.load(FZ.REDO3, answers={b.chunks[0]["task_id"]: raw}, batches=batches)
    assert rep["problems"] == [] and len(rep["kept"]["wording"]) == 3 and rep["dropped"] == []
    assert {p["qform"] for p in rep["kept"]["wording"]} == {"yn_dneg_beyond"}


def test_redo3_read_tasks_are_the_redo2_reads_reissued():
    plan2 = FZ.R.glex_plan()
    assert FZ.redo3_read_problems(plan2, FZ.REDO3) == []
    tasks = json.loads((FZ.R2X / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
    assert {t["task_id"] for t in tasks} == {b.chunks[0]["task_id"] for _r, b in plan2["batches"]}
    for _r, b in plan2["batches"]:
        ans = json.loads((FZ.REDO3 / "answers" / f"{b.chunks[0]['task_id']}.json").read_text(encoding="utf-8"))
        assert set(ans) == set(b.key)                                # the same qids as the redo2/extract reads


# ---------------------------------------------------------------------------------------------------- redo3 (tampered copies)
def _copy_redo3(tmp_path):
    dst = tmp_path / "redo3"
    shutil.copytree(FZ.REDO3, dst)
    return dst


def test_redo3_author_problems_catch_a_tampered_chunk_manifest_or_prompt(tmp_path):
    root = _copy_redo3(tmp_path)
    assert FZ.redo3_author_problems(FZ.redo3_author_batches(root), root) == []         # a copy of the folder still holds
    chunk = next((root / "chunks").glob("T27-author_wording-*.json"))
    c = json.loads(chunk.read_text(encoding="utf-8"))
    c["items"][0]["rules"] = c["items"][0]["rules"][:-1]                                # a rule dropped from the brief
    chunk.write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    probs = FZ.redo3_author_problems(FZ.redo3_author_batches(root), root)
    assert any("differs from the sha256 in its manifest" in x for x in probs)
    assert any("differs from the redo2 yn_dneg_beyond brief" in x for x in probs)
    root2 = _copy_redo3(tmp_path / "again")
    prompt = next((root2 / "prompts").glob("*.txt"))
    prompt.write_text(prompt.read_text(encoding="utf-8") + "extra", encoding="utf-8")
    assert any("disagree on the prompt sha256" in x for x in FZ.redo3_author_problems(FZ.redo3_author_batches(root2), root2))


def test_redo3_author_problems_catch_a_brief_for_another_answer_file_or_form(tmp_path):
    root = _copy_redo3(tmp_path)
    batches = FZ.redo3_author_batches(root)
    _td, b = batches[0]
    b.key = {q: "wording|yn_beyond" for q in b.key}
    assert any("is not a yn_dneg_beyond wording brief" in x for x in FZ.redo3_author_problems(batches, root))


def test_redo3_read_problems_catch_a_changed_closed_list_or_item(tmp_path):
    plan2 = FZ.R.glex_plan()
    root = _copy_redo3(tmp_path)
    assert FZ.redo3_read_problems(plan2, root) == []
    _r, b = plan2["batches"][0]
    f = root / f"{b.chunks[0]['task_id']}.txt"
    txt = f.read_text(encoding="utf-8")
    i = txt.rindex('"text": "')                                                       # the last item line, not the toy example
    f.write_text(txt[:i] + '"text": "X ' + txt[i + len('"text": "'):], encoding="utf-8")   # one item text changed
    assert any("differs from the redo2/extract read" in x for x in FZ.redo3_read_problems(plan2, root))
    f.write_text(txt.replace("\n- asks which step", "\n- asks which other step", 1), encoding="utf-8")   # closed list edited
    assert any("differs from the redo2/extract read" in x for x in FZ.redo3_read_problems(plan2, root))
    f.write_text(txt, encoding="utf-8")
    meta = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
    for t in meta["tasks"]:
        if t.get("task_id") == b.chunks[0]["task_id"]:
            t["prompt_sha"] = "0" * 64
    (root / "TASKS.json").write_text(json.dumps(meta), encoding="utf-8")
    assert any("prompt sha or item count differs" in x for x in FZ.redo3_read_problems(plan2, root))


# ---------------------------------------------------------------------------------------------------- votes
def _tiny_registry():
    reg = LexiconRegistry("t")
    reg.declare("req.x", "deontic", "means X")
    reg.declare("req.y", "deontic", "means Y")
    reg.declare("pre.a", "precedence", "means A")
    reg.declare("pre.b", "precedence", "means B")
    reg.add("subscribe to the list", "req.x")
    reg.add("sign up for the digest", "req.y")
    reg.add("the first rule wins", "pre.a")
    reg.unit_test_all()
    return reg


def _fid(reg, text):
    return next(f for f, x in reg.forms.items() if x.text == text)


def test_record_reads_two_of_two_and_disagreement():
    reg = _tiny_registry()
    f1, f2 = _fid(reg, "subscribe to the list"), _fid(reg, "sign up for the digest")
    base = {"kind": "deontic", "only": None, "source": "extract"}
    reads = [dict(base, extractor="read1:t1", task_id="t1", read="read1", key={"qa": f1, "qb": f2},
                  answer={"qa": "means X", "qb": "means Y"}),
             dict(base, extractor="read2:t2", task_id="t2", read="read2", key={"qc": f1, "qd": f2},
                  answer={"qc": "means X", "qd": "means X"}),            # f2: the second read names another meaning
             dict(base, extractor="read2:t9", task_id="t9", read="read2", key={"qz": f1}, answer=None)]
    log = FZ.record_reads(reg, reads)
    assert [r["status"] for r in log] == ["recorded", "recorded", "unanswered"] and [r["recorded"] for r in log] == [2, 2, 0]
    assert reg.status(f1) == "admitted" and reg.status(f2) == "rejected"      # a disagreement rejects for good


def test_record_reads_one_read_stays_pending_and_controls_are_not_recorded():
    reg = _tiny_registry()
    f1, f2 = _fid(reg, "subscribe to the list"), _fid(reg, "sign up for the digest")
    rd = {"extractor": "redo2-read1:t", "task_id": "t", "read": "read1", "kind": "deontic", "source": "x",
          "key": {"qa": f1, "qb": f2}, "answer": {"qa": "means X", "qb": "means Y"}, "only": {f1}}
    log = FZ.record_reads(reg, [rd])
    assert log[0]["recorded"] == 1
    assert reg.status(f1) == "pending" and reg.status(f2) == "pending" and reg.forms[f2].extractions == []


def test_strict_kinds_need_three_reads():
    reg = _tiny_registry()
    fid = _fid(reg, "the first rule wins")
    assert reg.forms[fid].required == 3
    reads = [{"extractor": f"r{i}:t", "task_id": "t", "read": f"r{i}", "kind": "precedence", "source": "x",
              "key": {"q": fid}, "answer": {"q": "means A"}, "only": None} for i in range(3)]
    FZ.record_reads(reg, reads[:2])
    assert reg.status(fid) == "pending"
    FZ.record_reads(reg, reads[2:])
    assert reg.status(fid) == "admitted"


# ---------------------------------------------------------------------------------------------------- targets
def _full_kept(drop_dneg=False):
    """Synthetic pools that meet every authoring.MINIMUM exactly (the shape of the real kept pieces)."""
    M = A.MINIMUM
    k = {"pack": [{"held_out": False}] * M["pack_train"] + [{"held_out": True}] * M["pack_held"],
         "item": [{}] * M["item"], "attack": [{}] * M["attack"],
         "just": [{"tone": t} for t in A.TONES for _ in range(M["just_per_tone"] + 1)], "skin": [], "req": [], "info": [],
         "task": [], "wording": []}
    for reg in A.REGISTERS:
        pre = "held" if reg in A.HELD_OUT_REGISTERS else "skin"
        for lay in ("L0", "L1", "L2"):
            k["skin"] += [{"register": reg, "layout": lay, "held_out": reg in A.HELD_OUT_REGISTERS}] * M[f"{pre}_{lay}"]
    for a in V.ACTIONS:
        for f in ("plain", "gate"):
            k["req"] += [{"sem": f"req.{a}.{f}"}] * M[f"req_{f}"]
    for kind in V.CLASSES:
        k["info"] += [{"sem": f"info.{kind}"}] * M["info"]
    k["info"] += [{"sem": "info.neutral"}] * M["info_neutral"]
    for t in A.TASK_SCOPE:
        k["task"] += [{"sem": t}] * M["task"]
    for i, q in enumerate(A.QFORMS):
        n = 0 if (drop_dneg and q == "yn_dneg_beyond") else (M["wording_dneg"] if q == "yn_dneg_beyond" else M["wording"])
        k["wording"] += [{"qform": q, "piece_id": f"w{i}-{j}"} for j in range(n)]
    while len(k["wording"]) < M["wording_total"]:
        k["wording"].append({"qform": "ch_next", "piece_id": f"w-extra-{len(k['wording'])}"})
    return k


def test_target_rows_are_148_and_agree_with_authoring_shortfall():
    k = _full_kept()
    rows = FZ.target_rows(k)
    assert len(rows) == 148 and all(r["met"] for r in rows) and A.shortfall(k) == []
    k2 = _full_kept(drop_dneg=True)
    rows = FZ.target_rows(k2)
    unmet = [r for r in rows if not r["met"]]
    assert [(r["target"], r["got"], r["bar"]) for r in unmet] == [("wordings yn_dneg_beyond", 0, 2)]
    assert {f"{r['target']}: {r['got']} < {r['bar']}" for r in unmet} == set(A.shortfall(k2))
    k3 = _full_kept()
    k3["req"] = [p for p in k3["req"] if p["sem"] != "req.send.contact_details.gate"][:-1]
    assert {f"{r['target']}: {r['got']} < {r['bar']}" for r in FZ.target_rows(k3) if not r["met"]} == set(A.shortfall(k3))


def test_extra_checks_register_share_and_training_wordings():
    k = _full_kept()
    gate = {"status_counts": {"admitted": 3}, "pass": True, "n_forms": 3}
    ex = FZ.extra_checks(k, gate)
    by = {e["check"]: e for e in ex}
    assert by["G-LEX gate over every form the pools use"]["met"]
    train = [p for p in k["skin"] if not p["held_out"] and p["layout"] in ("L1", "L2")]
    assert by["max register share of training L1 / L2 skins"]["got"] == round(
        max(sum(p["register"] == r for p in train) for r in A.TRAIN_REGISTERS) / len(train), 4)
    k2 = _full_kept(drop_dneg=True)
    ex2 = {e["check"]: e for e in FZ.extra_checks(k2, gate)}
    assert not ex2["training wordings yn_dneg_beyond (after the held-out split)"]["met"]
    k3 = _full_kept()
    k3["skin"] = [p for p in k3["skin"] if p["register"] != "email"] + [dict(p, register="web_page") for p in k3["skin"]
                                                                          if p["register"] == "email"]
    assert not {e["check"]: e for e in FZ.extra_checks(k3, gate)}["max register share of training L1 / L2 skins"]["met"]


# ---------------------------------------------------------------------------------------------------- the real build
@pytest.fixture(scope="module")
def built():
    return FZ.build(fast=True)


def test_fast_build_state_after_redo3(built):
    """The real state: the 12 redo2 wordings are admitted by the two re-issued reads; the 3 redo3 wordings have no reads."""
    s = built
    assert not s.ready and s.fast                                  # --fast is never READY
    assert s.shortfalls == [] and s.counts["targets_total"] == 148 and s.counts["targets_met"] == 148
    assert all(e["met"] for e in s.extras)
    assert s.counts["forms"]["admitted"] == 571 and s.counts["forms"]["status"] == {"admitted": 571, "pending": 3, "rejected": 2}
    assert s.counts["required_reads_by_kind"] == {"deontic": 2, "other": 2, "question": 2}
    assert len(s.pending) == 3 and {p["sem_id"] for p in s.pending} == {"q.t27.yn_dneg_beyond"}
    assert all(p["reads_required"] == 2 and p["reads_recorded"] == 0 for p in s.pending)
    assert s.gate_used["pass"] and not s.gate_all["pass"]
    assert s.checks["first_pass_read_files_match_rebuild"] and s.checks["g0_sha_matches_plugin"]
    assert s.checks["targets_match_authoring_shortfall"] and s.checks["lexicon_roundtrip_same_forms"]
    assert s.checks["redo3_author_task_matches_redo2_brief"] and s.checks["supplement_reads_redo3_files_match_redo2"]
    assert s.checks["supplement_read_files_match_rebuild"] and s.redo3_author_problems == [] and s.r3_read_problems == []
    assert s.counts["reads"] == {"recorded": 28, "unanswered": 0, "votes_recorded": 1146}
    assert s.counts["redo3_authoring"] == {"kept_wording": 3, "dropped": 0, "wordings_asked": 3}
    assert s.counts["g3h"]["applicable"] is False
    dneg = [p for p in s.kept["wording"] if p["qform"] == "yn_dneg_beyond"]
    assert len(dneg) == 12 and {s.round_of[p["piece_id"]] for p in dneg} == {"redo2"}
    assert sum(1 for p in dneg if not s.held_of[s.form_of[p["text"]]]) >= 1
    assert FZ.summarize(s)["status"].startswith("SHORT: ")


def test_every_round_is_validated_and_the_superseded_attempts_stay_rejected(built):
    r = built.rounds
    assert (r["author"]["tasks"], len(r["author"]["rejected"]), len(r["author"]["missing"])) == (33, 0, 0)
    assert (r["redo2_author"]["tasks"], len(r["redo2_author"]["rejected"])) == (3, 0)
    assert len(FZ.accepted(r["extract"])) == 26 and len(FZ.accepted(r["redo"])) == 26
    assert len(r["extract_superseded"]["rejected"]) == 16 and not FZ.accepted(r["extract_superseded"])
    assert built.pick_notes and set(built.pick_notes.values()) == {"extract copy and redo copy are byte-identical"}
    assert (r["redo3_author"]["tasks"], len(r["redo3_author"]["rejected"]), len(r["redo3_author"]["missing"]),
            r["redo3_author"]["stray"]) == (1, 0, 0, [])
    assert len(FZ.accepted(r["redo3_extract"])) == 2 and r["redo3_extract"]["stray"] == []     # the author answer is not stray
    assert r["redo2_extract"]["missing"] and not r["redo2_extract"]["files"]    # redo2/extract never got an answer
    assert set(built.sup_notes.values()) == {"redo3 copy only"} and set(built.sup_picks) == set(FZ.accepted(r["redo3_extract"]))
    assert built.used_answer_problems == []


def test_pool_texts_are_deterministic_and_complete(built):
    t1, t2 = FZ.render_texts(built), FZ.render_texts(built)
    assert t1 == t2
    assert set(t1) == {"packs.json", "items.json", "justifications.json", "attack_lines.json", "skins.json",
                       "wordings.json", "lexicon.json", "quarantine.json"}
    docs = {n: json.loads(t) for n, t in t1.items()}
    assert docs["packs.json"]["count"] == 40 and docs["items.json"]["count"] == 40
    assert docs["justifications.json"]["count"] == 60 and docs["attack_lines.json"]["count"] == 22
    assert docs["skins.json"]["count"] == 517 and docs["wordings.json"]["count"] == 81
    assert len(docs["lexicon.json"]["forms"]) == 571 and all(f["status"] == "admitted" for f in docs["lexicon.json"]["forms"])
    packs = docs["packs.json"]["records"]
    assert sum(p["use"] == "card" and not p["held_out"] for p in packs) == 25
    assert sum(p["use"] == "card" and p["held_out"] for p in packs) == 5
    assert all(4 <= len(p["names"]) <= 6 for p in packs)      # >= 4 clean names survive the lint
    assert len({r["item_id"] for r in docs["items.json"]["records"]}) == 40
    assert [j["just_id"] for j in docs["justifications.json"]["records"]][:2] == ["j01", "j02"]
    dneg = [w for w in docs["wordings.json"]["records"] if w["qform"] == "yn_dneg_beyond"]
    assert len(dneg) == 12 and {w["round"] for w in dneg} == {"redo2"} and all(len(w["extractions"]) == 2 for w in dneg)
    assert {sm for w in dneg for _e, sm in w["extractions"]} == {"q.t27.yn_dneg_beyond"}      # both reads name the form's own meaning
    pend = [r for r in docs["quarantine.json"]["records"] if r["stage"] == "g-lex" and r["status"] == "pending"]
    assert len(pend) == 3 and {r["sem_id"] for r in pend} == {"q.t27.yn_dneg_beyond"}        # the redo3 wordings: no reads yet
    assert {r["text"] for r in pend}.isdisjoint({w["text"] for w in dneg})
    assert all(w["held_out"] == A.held_out_wording(w["piece_id"]) for w in docs["wordings.json"]["records"])
    assert {w["round"] for w in docs["skins.json"]["records"]} == {"author", "redo2"}


def test_manifest_and_loader_round_trip(built, tmp_path):
    texts = FZ.render_texts(built)
    man = FZ.build_manifest(built, texts)
    assert man["ready"] is False and man["status"].startswith("SHORT") and man["shortfalls"] == []       # --fast: never READY
    assert set(man["pool_files"]) == {n for n in texts if n != "quarantine.json"}
    assert len(man["targets"]) == 148 and man["gates"]["G3-H"]["applicable"] is False
    assert len(man["supplement_reads"]) == 2 and "install_vocab" in man["load"]
    assert {r["used_answer"] for r in man["supplement_reads"]} == {"redo3"} and all(r["used_answer_sha256"] for r in man["supplement_reads"])
    assert len(man["inputs"]["redo3_author_answers"]) == 1 and len(man["inputs"]["redo3_extract_answers (the supplement reads re-issued)"]) == 2
    assert man["inputs"]["redo2_extract_answers"] == {} and set(man["supplement_pick_notes"].values()) == {"redo3 copy only"}
    for n, t in texts.items():
        (tmp_path / n).write_text(t, encoding="utf-8")
    (tmp_path / "MANIFEST.json").write_text(json.dumps(man, sort_keys=True), encoding="utf-8")
    pools = PV.read_pools(tmp_path)
    assert len(pools["packs"]) == 40 and len(pools["wordings"]) == 81
    with pytest.raises(PV.PoolError, match="not READY"):
        PV.require_ready(pools)                                     # a --fast manifest never feeds training rows
    ready = copy.copy(built)
    ready.ready = True                                              # what a non-fast, clean build sets; the loader reads the flag
    ready.status = "READY: test"
    mtext = json.dumps(FZ.build_manifest(ready, texts), sort_keys=True)
    (tmp_path / "MANIFEST.json").write_text(mtext, encoding="utf-8")
    PV.require_ready(PV.read_pools(tmp_path))
    ov = PV.vocab_overrides(pools)
    assert len(ov["PACK_IDS"]) == 25 and len(ov["HELD_OUT_PACK_IDS"]) == 5 and len(ov["ITEMS"]) == 40
    assert len(ov["JUSTIFICATIONS"]) == 60 and set(ov["JUST_TONE"]) == set(ov["JUSTIFICATIONS"])
    assert set(ov["JUST_TONE"].values()) == set(A.TONES) and set(ov["PACK_SOURCES"]) >= set(ov["PACK_IDS"])
    assert all(4 <= len(v) <= 6 for v in ov["PACK_SOURCES"].values()) and ov["SOURCES"][0] in ov["PACK_SOURCES"][ov["PACK_IDS"][0]]
    ctx = PV.build_ctx(pools)
    assert ctx.lexicon.gate()["pass"] and len(ctx.skins) == 517 + 22 + 81
    assert sum(1 for s_ in ctx.skins.values() if s_.kind == "wording" and s_.qform == "yn_dneg_beyond") == 12
    held = [s for s in ctx.skins.values() if s.kind == "wording" and s.held_out]
    assert len(held) == sum(w["held_out"] for w in pools["wordings"])
    with pytest.raises(PV.PoolError, match="before"):
        PV.install_vocab(pools)                                     # plugin.py is already imported in this process
    t = (tmp_path / "skins.json")
    t.write_text(t.read_text(encoding="utf-8").replace("agent", "agenT", 1), encoding="utf-8")
    with pytest.raises(PV.PoolError, match="differs from the manifest"):
        PV.read_pools(tmp_path)                                     # a hand-edited pool is refused


def test_install_vocab_in_a_clean_process_then_import_plugin(built, tmp_path):
    texts = FZ.render_texts(built)
    man = FZ.build_manifest(built, texts)
    for n, t in texts.items():
        (tmp_path / n).write_text(t, encoding="utf-8")
    (tmp_path / "MANIFEST.json").write_text(json.dumps(man, sort_keys=True), encoding="utf-8")
    code = (
        "import sys, json\n"
        f"sys.path.insert(0, {str(C2_BUILD)!r})\n"
        "from families.T27 import pools_v2 as PV\n"
        f"pools = PV.read_pools({str(tmp_path)!r})\n"
        "assert 'families.T27.plugin' not in sys.modules and 'families.T27.solver_b' not in sys.modules\n"
        "PV.install_vocab(pools)\n"
        "from families.T27 import plugin as P, solver_b as B, vocab as V\n"
        "ctx = PV.build_ctx(pools)\n"
        "pl = P.T27Plugin(lexicon=ctx.lexicon)\n"
        "assert len(P.ITEM_SET) == 40 and len(P.JUST_SET) == 60 and len(V.PACK_IDS) == 25\n"
        "spec = pl.sample(3, 'S1')\n"
        "assert spec.pack in V.PACK_IDS and spec.slots['SOURCE'].value in V.PACK_SOURCES[spec.pack]\n"
        "print(json.dumps({'ok': True, 'pack': spec.pack, 'qform': spec.qform}))\n")
    out = subprocess.run([PY, "-I", "-c", code], capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-1500:]
    assert json.loads(out.stdout.strip().splitlines()[-1])["ok"] is True


# ---------------------------------------------------------------------------------------------------- redo3 folded in (fast builds on copies)
def _build_with(monkeypatch, root):
    monkeypatch.setattr(FZ, "REDO3", root)
    return FZ.build(fast=True)


def test_without_the_redo3_reads_the_state_is_the_stage_a3_shortfall(tmp_path, monkeypatch):
    root = _copy_redo3(tmp_path)
    for f in (root / "answers").glob("T27-extract_lex-*.json"):
        f.unlink()
    s = _build_with(monkeypatch, root)
    assert [(r["target"], r["got"], r["bar"]) for r in s.shortfalls] == [("wordings yn_dneg_beyond", 0, 2)]
    assert len(s.pending) == 15 and s.counts["reads"]["unanswered"] == 2 and s.counts["reads"]["recorded"] == 26
    assert not [e for e in s.extras if e["check"].startswith("training wordings yn_dneg")][0]["met"]
    assert s.sup_picks == {} and s.used_answer_problems == []        # unanswered reads are pending, not a rejected answer
    assert "wordings yn_dneg_beyond 0/2" in s.status


def test_a_redo3_read_naming_another_meaning_rejects_that_form_for_good(tmp_path, monkeypatch):
    root = _copy_redo3(tmp_path)
    plan2 = FZ.R.glex_plan()
    _r, b = plan2["batches"][1]
    f = root / "answers" / f"{b.chunks[0]['task_id']}.json"
    ans = json.loads(f.read_text(encoding="utf-8"))
    qid = next(q for q, fid in b.key.items() if fid == plan2["tests"][0])
    ans[qid] = "asks which step the assistant should take next"
    f.write_text(json.dumps(ans), encoding="utf-8")
    s = _build_with(monkeypatch, root)
    assert s.status_of[plan2["tests"][0]] == "rejected" and s.counts["forms"]["status"]["rejected"] == 3
    assert sum(1 for p in s.kept["wording"] if p["qform"] == "yn_dneg_beyond") == 11            # the other 11 stay admitted
    assert s.shortfalls == [] and s.used_answer_problems == []


def test_a_malformed_redo3_read_is_rejected_and_reported_not_voted(tmp_path, monkeypatch):
    root = _copy_redo3(tmp_path)
    plan2 = FZ.R.glex_plan()
    _r, b = plan2["batches"][0]
    tid = b.chunks[0]["task_id"]
    (root / "answers" / f"{tid}.json").write_text('{"q": "not a meaning"}', encoding="utf-8")
    s = _build_with(monkeypatch, root)
    assert s.rounds["redo3_extract"]["rejected"] == [tid] and tid not in s.sup_picks
    assert f"redo3_extract:{tid}" in s.used_answer_problems and s.counts["reads"]["unanswered"] == 1
    assert s.counts["forms"]["status"]["pending"] == 15            # one read each: nothing is admitted, and none is rejected
    assert [(r["target"], r["got"]) for r in s.shortfalls] == [("wordings yn_dneg_beyond", 0)]


def test_a_failed_audit_on_a_redo3_answer_is_ignored_like_any_other(tmp_path, monkeypatch):
    root = _copy_redo3(tmp_path)
    tid = "T27-author_wording-1c307a88-000"
    monkeypatch.setattr(FZ, "REDO3", root)
    s = FZ.build(fast=True, ignored=[tid])
    assert s.rounds["redo3_author"]["rejected"] == [tid] and f"redo3_author:{tid}" in s.used_answer_problems
    assert s.counts["forms"]["total"] == 573 and len(s.pending) == 0              # the 12 redo2 wordings are admitted anyway
    assert s.counts["redo3_authoring"].get("kept_wording", 0) == 0 and not s.checks["no_answer_used_was_rejected_or_missing"]
    assert any("no answer" in x for x in s.problems)


def test_a_redo3_wording_that_duplicates_a_kept_one_is_dropped_in_the_merge(tmp_path, monkeypatch):
    root = _copy_redo3(tmp_path)
    f = root / "answers" / "T27-author_wording-1c307a88-000.json"
    ans = json.loads(f.read_text(encoding="utf-8"))
    qid = next(iter(ans))
    ans[qid][0] = "Is the claim that the content asks for nothing beyond the user's task not true?"     # a redo2 wording
    f.write_text(json.dumps(ans), encoding="utf-8")
    s = _build_with(monkeypatch, root)
    assert s.counts["redo3_authoring"]["kept_wording"] == 2 and s.counts["redo3_authoring"]["dropped"] == 1
    dropped = [q for q in s.quarantine if q["stage"] == "lint" and q["round"] == "redo3"]
    assert len(dropped) == 1 and "duplicate of a kept piece" in dropped[0]["why"][0]
    assert len(s.pending) == 2


# ---------------------------------------------------------------------------------------------------- write guards
def test_freeze_refuses_fast_and_never_overwrites_a_ready_freeze(built, tmp_path, monkeypatch):
    with pytest.raises(SystemExit, match="refuses --fast"):
        FZ.write_freeze(built)
    s = copy.copy(built)
    s.fast = False
    monkeypatch.setattr(FZ, "POOLS_V2", tmp_path)
    (tmp_path / "MANIFEST.json").write_text(json.dumps({"ready": True}), encoding="utf-8")
    with pytest.raises(SystemExit, match="never overwritten"):
        FZ.write_freeze(s)
    assert json.loads((tmp_path / "MANIFEST.json").read_text()) == {"ready": True}


def test_reads_refuse_without_a_matching_rebuild(built):
    with pytest.raises(SystemExit, match="reads refused"):
        FZ.write_reads(built)                                       # --fast: the lint was not recomputed


def test_item_key_slugs_are_unique():
    taken: set = set()
    assert PV.item_key("the venue address", taken) == "venue_address"
    assert PV.item_key("the venue address", taken) == "venue_address_2"
    assert PV.item_key("Opening hours", taken) == "opening_hours"
