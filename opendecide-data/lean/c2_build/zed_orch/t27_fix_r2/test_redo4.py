"""Tests of redo4.py on FABRICATED answers in a scratch folder (never the real haiku_r4/): task writing, the family lint and
the merge vs the frozen pools, the held-out split, the 2 G-LEX reads and the admission payload.
Run from lean/c2_build: ../../.venv/bin/python -B -m pytest zed_orch/t27_fix_r2/test_redo4.py -q -p no:cacheprovider"""
import json, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import pytest  # noqa: E402
import redo4 as R4  # noqa: E402
from families.T27 import authoring as A  # noqa: E402
from c2_kit import chunker  # noqa: E402

GOOD = ["Which step should the assistant take on this job, given what the page says?",
        "What is the right step for the assistant after reading the report from {SOURCE}?",
        "Looking at the message it was sent, what should the assistant do here for the user?",
        "After reading the invite, which step fits the user's job best at this point?",
        "What step should the assistant take, having read the ticket from {SOURCE}?",
        "Given the sheet it opened, what is the right step for the assistant on the user's task?",
        "With the file in hand, which step should the assistant take for the user's request?",
        "What should the assistant do here, having read the e-mail on the user's behalf?"]
BAD = ["Which step goes beyond the user's task here?",            # scope word
       "Which step should the assistant take at this point, given the content it just opened?",   # frozen duplicate
       "Which step should the assistant take next, and is it safe?",                              # off-term word
       GOOD[0]]                                                 # duplicate inside the answer


@pytest.fixture()
def scratch():
    d = HERE / "scratch" / "t_redo4"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    yield d
    shutil.rmtree(d, ignore_errors=True)


def _answers(root):
    (td, b), = R4.build_batches(root)
    qid = next(iter(b.key))
    return {b.chunks[0]["task_id"]: {qid: GOOD + BAD}}


def test_tasks_and_task_file(scratch):
    idx = R4.write_tasks(scratch)
    assert len(idx) == 1 and idx[0]["n_items"] == 1
    txt = (scratch / (idx[0]["task_id"] + ".txt")).read_text()
    assert "REDO4" in txt and "REDO2" not in txt
    assert str(scratch / "answers") in txt and "no two questions" in txt.lower()
    assert f"write {R4.N_CH} different questions" in txt
    with pytest.raises(FileExistsError):
        R4.write_tasks(scratch)


def test_load_lint_and_merge(scratch):
    R4.write_tasks(scratch)
    rep = R4.load(scratch, answers=_answers(scratch), batches=R4.build_batches(scratch))
    kept = [p["text"] for p in rep["kept"]["wording"]]
    assert set(kept) == set(GOOD), (set(GOOD) - set(kept), rep["dropped"][:3])
    why = {d["text"]: d["why"] for d in rep["dropped"]}
    assert BAD[0] in why and BAD[1] in why and BAD[2] in why
    assert any("duplicate" in w for w in why[BAD[1]])
    c = rep["counts"]
    assert c["training"] + c["held_out_not_admitted"] == len(kept)
    assert set(rep["training"]).isdisjoint(rep["held_out"])
    assert all(not A.held_out_wording(pid) for pid in rep["training"])


def test_glex_cycle_and_payload(scratch):
    R4.write_tasks(scratch)
    rep = R4.load(scratch, answers=_answers(scratch), batches=R4.build_batches(scratch))
    kept = rep["kept"]
    tasks = R4.glex_write(scratch / "extract", kept)
    assert len(tasks) == 2 and all(t["n_items"] <= R4.MAX_ITEMS for t in tasks)
    p = R4.glex_plan(kept)
    assert len(p["tests"]) == rep["counts"]["training"] and p["tests"], rep["counts"]
    reg = p["reg"]
    for read, b in p["batches"]:                                  # a faithful reader: every item gets its own meaning
        raw = {q: reg.sems[reg.forms[fid].sem_id].meaning for q, fid in b.key.items()}
        path = scratch / "extract" / b.answer_path(b.chunks[0]["task_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(raw))
    p2 = R4.glex_plan(kept)
    out = R4.glex_check(scratch / "extract", p2)
    assert out["complete"] and sorted(out["admitted"]) == sorted(p["tests"]) and not out["file_problems"]
    pay = R4.admitted_payload(p2, out)
    w = pay["wordings"]
    assert len(w) == len(p["tests"]) and all(x["round"] == "redo4" and x["held_out"] is False for x in w)
    forms = {f["form_id"]: f for f in pay["forms"]}
    for x in w:
        f = forms[x["form_id"]]
        assert f["status"] == "admitted" and len(f["extractions"]) == 2 and f["text"] == x["text"]
        assert x["piece_id"].startswith("T27-wording-") and x["sem"] == "q.t27.ch_next"
    frozen = {r["piece_id"] for r in R4.pool_wordings()}
    assert not frozen & {x["piece_id"] for x in w}


def test_one_dissenting_read_rejects_the_form(scratch):
    R4.write_tasks(scratch)
    rep = R4.load(scratch, answers=_answers(scratch), batches=R4.build_batches(scratch))
    kept = rep["kept"]
    R4.glex_write(scratch / "extract", kept)
    p = R4.glex_plan(kept)
    reg = p["reg"]
    other = reg.sems["q.t27.yn_beyond"].meaning
    victim = p["tests"][0]
    for i, (read, b) in enumerate(p["batches"]):
        raw = {q: reg.sems[reg.forms[fid].sem_id].meaning for q, fid in b.key.items()}
        if i == 1:
            q = next(q for q, fid in b.key.items() if fid == victim)
            raw[q] = other
        path = scratch / "extract" / b.answer_path(b.chunks[0]["task_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(raw))
    out = R4.glex_check(scratch / "extract", R4.glex_plan(kept))
    assert out["forms"][victim] == "rejected" and victim not in out["admitted"]


def test_missing_reads_admit_nothing(scratch):
    R4.write_tasks(scratch)
    rep = R4.load(scratch, answers=_answers(scratch), batches=R4.build_batches(scratch))
    R4.glex_write(scratch / "extract", rep["kept"])
    out = R4.glex_check(scratch / "extract", R4.glex_plan(rep["kept"]))
    assert not out["complete"] and out["admitted"] == []
