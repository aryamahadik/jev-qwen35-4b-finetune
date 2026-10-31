"""transfer/T19/test_redo3.py: in-memory tests of the T19 redo round 3 (redo3.py). Nothing here writes a file; the
sample sentences are test stand-ins built from the item openings, never answers to a task."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import skin as K  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import redo2 as RD  # noqa: E402
from transfer.T19 import redo3 as R  # noqa: E402
import negcount  # noqa: E402


@pytest.fixture(scope="module")
def tasks():
    return R.build()


def _opening(frame: str) -> str:
    m = re.fullmatch(r"open with '(.+)'", frame)
    assert m, frame
    return m.group(1)


def _sample(frame: str) -> str:
    return f"{_opening(frame)} is {{SITE}} not compliant with its checklist on the audit date?"


def test_one_task_sized_to_the_gap(tasks):
    short = R.shortfalls()
    assert [(s["item"], s["shortfall"]) for s in short] == [(R.CELL, 1)]       # STAGE_A3_REPORT, this family
    assert R.n_items(1) == 2 and R.n_items(2) == 3 and R.n_items(4) == 6 and R.n_items(0) == 0
    assert len(tasks) == 1
    t = tasks[0]
    assert t["n_items"] == 2 and t["n_candidates"] == 3 and t["outputs_expected"] == 6
    assert set(t["cells"].values()) == {R.CELL}
    assert t["answer_file"].startswith(str(R.ROOT / "answers")) and t["answer_file"] in t["text"]
    assert t["allowed_read"] == [t["task_file"]] and t["allowed_write"] == [t["answer_file"]]
    assert not never_open(t["task_file"]) and not never_open(t["answer_file"])


def test_no_read_is_pending():
    assert R.pending_reads() == {"haiku/extract": [], "haiku/redo2/extract": []}


def test_qids_are_new_opaque_and_unique(tasks):
    t = tasks[0]
    assert len(set(t["qids"])) == 2
    assert all(re.fullmatch(r"q[0-9a-f]{10}", q) for q in t["qids"])
    assert not set(t["qids"]) & R.used_qids()
    assert "qb8572add92" not in t["text"]                                  # the open item's qid is lineage only
    assert R.new_qids(2) == t["qids"]                                      # deterministic


def test_openings_are_new_and_unique():
    assert len(set(R.FRAMES3)) == len(R.FRAMES3) == 6
    assert not set(R.FRAMES3) & set(RD.FRAMES)
    low = " ".join(_opening(f).lower() for f in R.FRAMES3)
    for s in HA.STYLES:
        m = re.search(r"'(.+?)'", s)
        if m:
            assert m.group(1).lower() not in low
    for f in RD.FRAMES:
        m = re.search(r"'(.+?)'", f)
        assert m and m.group(1).lower().replace(" ...?", "") not in low


@pytest.mark.parametrize("frame", R.FRAMES3)
def test_each_opening_gives_a_lint_clean_pinned_question(frame):
    text = _sample(frame)
    obj, v = HA.check_wording("x", text, {"qform": R.QFORM}, "tid", "psha", set())
    assert not v and obj[0] == R.QFORM
    assert RD.phrase_problems(R.QFORM, text) == []
    assert re.search(R.KEY_REGEX, text.lower())
    c = negcount.count(K.PH_RE.sub("the site", text))
    assert (c.k_all, c.k_syn) == HA.NEG_EXACT[R.QFORM] == (1, 1)
    assert text.count("{SITE}") == 1 and text not in HA.QSTRINGS


def test_samples_differ_from_every_frozen_wording(tasks):
    frozen = {" ".join(w["text"].split()).lower() for w in json.loads((R.POOLS_V2 / "wordings.json").read_text())}
    frozen |= {" ".join(f["text"].split()).lower() for q in json.loads((R.POOLS_V2 / "quarantine.json").read_text()).values()
               for f in q.get("forms_not_admitted", [])}
    samples = {_sample(f).lower() for f in R.FRAMES3}
    assert len(samples) == 6 and not samples & frozen


def test_task_text_is_self_contained_and_leaks_nothing(tasks):
    t = tasks[0]
    text = t["text"]
    assert text.startswith("# Haiku REDO-3 task T19-redo3-wordings-000 (family T19, kind author_wording): 2 item(s), "
                           "3 candidates each")
    assert "REDO-2" not in text
    assert "## Answer contract (exact)" in text and "Literal example of the required shape:" in text
    assert re.search(r'\{"qid": "q[0-9a-f]{10}", "texts": \["<text A>", "<text B>", "<text C>"\]\}', text)
    assert R.instructions() in text and "## Redo note" in text
    assert "candidate 1, candidate 2, candidate 3" in text and "for each candidate" in text
    assert "candidate 1, candidate 2)" not in text and "for candidate 1 and for candidate 2" not in text
    # nothing else of redo2's prompt changed: undo the two edits and compare
    undone = R.instructions().replace("(candidate 1, candidate 2, candidate 3)", "(candidate 1, candidate 2)") \
        .replace("for each candidate: follow it exactly", "for candidate 1 and for candidate 2: follow it exactly")
    assert undone == RD.wording_prompt(3) + "\n\n## Redo note\n\n" + RD.NOTES["wordings"]
    block = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
    assert [b["qid"] for b in block] == t["qids"]
    for b in block:
        assert set(b) == {"qid", "brief", "slots", "rules"} and b["brief"] == HA.WORDING_BRIEF[R.QFORM][0]
        assert any(f"'{R.KEY_PHRASE}'" in r for r in b["rules"]) and R.SHAPE in b["rules"]
        assert len([r for r in b["rules"] if r.startswith("Candidate ")]) == 3
    assert [r for b in block for r in b["rules"] if r.startswith("Candidate ")] == \
        [f"Candidate {i % 3 + 1}: {f}." for i, f in enumerate(R.FRAMES3)]
    assert "t19a." not in text and "yn_" not in text and "ch_gap" not in text
    low = text.lower()
    for f in RD.FORBID["wordings"]:
        assert not re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low), f


def test_files_and_index_in_memory(tasks):
    fs = R.files(tasks)
    assert set(fs) == {"T19-redo3-wordings-000.md", "REDO3_INDEX.json", "answers/README.txt"}
    idx = json.loads(fs["REDO3_INDEX.json"])
    assert idx["g0_changed"] is False and idx["a_pending_reads"]["rewrapped"] == []
    assert idx["order"] == tasks[0]["qids"]
    assert idx["b_authoring"] == {"gap": 1, "ask_factor": "3/2", "items": 2, "candidates_per_item": 3, "cell": R.CELL}
    assert idx["phrase_stats"]["not compliant with"] == {"forms": 9, "admitted": 9}
    assert idx["phrase_stats"]["not in compliance with"]["read_as_other"] == 4
    assert "may not exceed its target 14" in idx["keep_rule"]
    assert idx["tasks"][0]["qids"] == tasks[0]["qids"] and "text" not in idx["tasks"][0]
    # the Haiku-facing text never carries the lineage (internal id, old qid)
    assert "t19a.wording" not in fs["T19-redo3-wordings-000.md"]


def test_build_is_deterministic(tasks):
    assert [t["task_sha256"] for t in R.build()] == [t["task_sha256"] for t in tasks]
