"""transfer/T36/test_redo2.py: tests for the T36 redo round 2 (G0_SPEC.md v2.1 sections 6 and 7, ruling v2.1).

Nothing is written. The task plan reads the round 1 answers, haiku/redo/ and pools/ (read only); candidate texts in the
selection and G3-H tests are synthetic test strings, never Haiku answers.
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T36/test_redo2.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from transfer.T36 import extract as E  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402
from transfer.T36 import redo2 as R  # noqa: E402

pytestmark = pytest.mark.skipif(not (R.POOLS / "documents.json").exists() or not (R.REDO / "REDO_INDEX.json").exists(),
                                reason="needs the frozen pools and haiku/redo/ (after A38)")


@pytest.fixture(scope="module")
def tasks():
    return R.build()


def test_plan_covers_exactly_the_shortfalls(tasks):
    by_kind = {}
    for t in tasks:
        by_kind.setdefault(t["author_kind"], []).extend(t["qids"])
    # Mode T: the two redo items whose redo text still fails; Mode F: every item without a frozen document
    assert sorted(by_kind["author_skin"]) == ["qa2b46e4961", "qe04bfa1329"]
    assert len(by_kind["author_freeform"]) == 41
    src = R._batches()
    frozen = {d["text"] for d in R._read_json(R.POOLS / "documents.json")}
    mode_f_all = set()
    for tid, (pool, b, c) in src.items():
        if pool in R.MODE_F:
            ans = {a["qid"]: a["text"].strip() for a in R._read_json(R.AUTHOR / b.answer_path(tid))}
            mode_f_all |= {it["qid"] for it in c["items"] if ans.get(it["qid"]) not in frozen}
    assert set(by_kind["author_freeform"]) == mode_f_all
    assert {t["held_out"] for t in tasks if t["pool"] == "freeform_heldout"} == {True}
    assert sum(t["n_items"] for t in tasks if t["pool"] == "freeform_heldout") == 10


def test_task_files_are_self_contained_and_label_free(tasks):
    src = R._batches()
    for t in tasks:
        text = t["text"]
        assert t["answer_file"] == str(R.ROOT / "answers" / f"{t['name']}.json") and t["answer_file"] in text
        assert R.task_problems(text) == []
        _pool, b, c = src[t["source_task_id"]]
        assert not any(iid in text for iid in b.key.values())
        assert f"exactly {t['n_candidates']} different strings" in text
        assert "third-party package" not in text and "about its third-party" not in text
        items = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
        source = {it["qid"]: it for it in c["items"]}
        assert [it["qid"] for it in items] == t["qids"]
        for it in items:
            assert it["register"] == source[it["qid"]]["register"]
            assert it.get("facts") == source[it["qid"]].get("facts")      # facts never change
        if t["author_kind"] == "author_freeform":
            assert "Maintainer statement (required)" in text and "who maintains <PROJECT>" in text


def test_selection_keeps_the_first_passing_candidate(tasks, monkeypatch):
    t_skin = next(t for t in tasks if t["pool"] == "skin_heldout")
    t_free = next(t for t in tasks if t["pool"] == "freeform_heldout")
    src = R._batches()
    q_f = t_free["qids"][0]
    facts = next(it for it in src[t_free["source_task_id"]][2]["items"] if it["qid"] == q_f)["facts"]
    good_f = (f"{facts['PROJECT']} is maintained by {facts['PERSON']}.\n- The team is looking at how the library is "
              "wired into the build, and notes from this review go to the shared board.")
    synth = {
        t_skin["name"]: {t_skin["qids"][0]: [
            "# Notes from {PERSON} on the {PKG} package inside {PROJECT}.",          # reserved place word
            "# Notes from {PERSON} on the {PKG} package in {PROJECT}, for reviewers of this file.",
            "# A second note from {PERSON} on {PKG} in {PROJECT}."]},              # number word; never reached
        t_free["name"]: {q_f: [good_f.replace("is maintained by", "is looked after by") + " Third-party notes.",
                               good_f]},
    }
    monkeypatch.setattr(R, "read_candidates", lambda t: (synth.get(t["name"], {}), []))
    sel = R.select([t_skin, t_free], set())
    rows = {r["qid"]: r for r in sel["items"]}
    skin_row = rows[t_skin["qids"][0]]
    assert skin_row["kept"] == 1 and not skin_row["candidates"][0]["ok"]
    assert any(x.startswith("gold_label") for x in skin_row["candidates"][0]["reasons"])
    free_row = rows[q_f]
    assert [c["ok"] for c in free_row["candidates"]] == [False, True]
    assert any(x.startswith("number") for x in free_row["candidates"][0]["reasons"])

    # the G3-H read: every lint-clean Mode F candidate, the frozen prompt and fields, no generator value in a chunk
    b, expected, fs = R.g3h_batch(sel)
    assert b.prompt_sha == hashlib.sha256(E.G3H_PROMPT.encode()).hexdigest()
    assert [f.describe for f in E.g3h_fields()] == ["the project whose dependency is discussed, as written",
                                                    "the person who maintains the project, as written"]
    assert len(expected) == 1 and expected[0]["expected"] == {"project": facts["PROJECT"], "person": facts["PERSON"]}
    chunk = json.loads(fs[b.chunk_path(b.chunks[0]["task_id"])])
    assert chunk["instructions"] == E.G3H_PROMPT.split("\n")
    assert chunk["answer_file"].startswith(str(R.G3H_ROOT / "answers"))
    assert set(chunk["items"][0]) == {"qid", "text", "schema"}
    assert "g3h2|" not in json.dumps(chunk)


def test_g0_v21_states_the_ruling():
    """The v2.1 ruling (Mode F maintainer statement, redo rule) is still on the page of the current version (v2.2)."""
    text = P.T36Plugin.G0_LITE.read_text()
    assert "v2, FROZEN" in text and "**v2.1**" in text and len(text.splitlines()) <= 200
    flat = " ".join(text.split())
    assert "in plain words that PERSON maintains PROJECT" in flat
    assert "Ruling v2.1" in text and "first candidate in written order" in flat
    assert hashlib.sha256(P.T36Plugin.G0_LITE.read_bytes()).hexdigest() == P.T36Plugin.G0_SHA256
