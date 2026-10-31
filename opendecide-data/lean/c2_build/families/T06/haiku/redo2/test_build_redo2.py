"""families/T06/haiku/redo2/test_build_redo2.py: the T06 redo2 tasks (build_redo2.py), built in memory.

Checks: gold-free chunks of <= 50 items with only the chunker's fields; no label word (Mode F) or fixture question
(both) in any task file; every task file names its own answer path and holds the inline contract; the B1 brief bans
"from" and its own phrasings pass the UNCHANGED v1 check_wording while the v1 failure mode still fails it; the B2 facts
are plain item names (no container word) with new skin ids; planned outputs cover each deficit; the extract-stage
helpers (v1 dedup sets, frozen registry, wording merge, G-LEX and G3-H batch builders) run on the frozen v1 pools; the
files on disk (if written) are the same bytes as the rebuild. Nothing is written and no answer is made up: the one
probe text below is a check_wording input, never an answer file.
Run (from lean/): ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T06/haiku/redo2
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[3]
for p in (str(C2_BUILD), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest  # noqa: E402

import build_redo2 as R  # noqa: E402
from c2_kit import chunker  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402
from families.T06 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def built():
    files, index = R.author_files()
    return files, index, R.build_batches()


def test_author_check_is_clean_and_tasks_self_contained(built):
    files, index, batches = built
    assert R.check_author(files, index) == []
    assert index["n_tasks"] == 3 and index["outputs_expected"] == 16 + 61
    for row in index["tasks"]:
        text = files[str(Path(row["task_file"]).relative_to(R.ROOT))]
        assert row["answer_file"] in text and "ANSWER CONTRACT" in text
        assert "/haiku/redo2/answers/" in row["answer_file"] and row["allowed_write"] == [row["answer_file"]]
        assert row["task_file"] in row["allowed_read"]
    for _name, (b, _plan, _spec) in batches.items():
        for c in b.chunks:
            assert 1 <= len(c["items"]) <= chunker.MAX_ITEMS
            for it in c["items"]:
                assert set(it) - {"qid"} <= set(chunker.TASK_KINDS[b.kind])


def test_no_label_word_or_fixture_question_reaches_a_brief(built):
    files, index, _b = built
    for row in index["tasks"]:
        low = files[str(Path(row["task_file"]).relative_to(R.ROOT))].lower()
        for q in H.QSTRINGS:
            assert q.lower() not in low
        if row["kind"] == "author_freeform":
            for w in P.T06Plugin.LABEL_WORDS:
                assert not re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low), w


def test_b1_brief_bans_from_and_the_v1_gate_is_unchanged():
    assert 'Never write the word "from"' in R.WD_PROMPT and "withdraw from" not in R.WD_BRIEF
    assert "from" not in R.WD_BRIEF.split() and "Never write the word 'from'" in R.WD_RULE
    meta = {"qform": R.QF, "held_out": False}
    for nm in R.WD_NAMES:
        assert H.check_wording("p", f"On which date does {nm} end?", meta, "t", "0" * 64, set())[1] == []
    v = H.check_wording("p", "On which date does the customer's legal right to withdraw from the purchase for any "
                        "reason end?", meta, "t", "0" * 64, set())[1]
    assert v == ["ch_end names the anchor"]
    assert len(R.taken_wordings()) == 4


def test_b1_items_cover_the_ask(built):
    _f, _i, batches = built
    _b, plan, _s = batches["wordings"]
    assert sum(1 for m in plan.values() if not m["held_out"]) == 12 >= 2 * (H.WORDING_PLAN[R.QF][0] - 2)
    assert sum(1 for m in plan.values() if m["held_out"]) == 4 >= H.WORDING_PLAN[R.QF][1] - 2 + 1
    assert {m["style"] for m in plan.values() if m["held_out"]} == set(H.STYLE_HELD)
    assert {m["style"] for m in plan.values() if not m["held_out"]} == set(H.STYLE_TRAIN)


def test_b2_facts_are_plain_and_cover_the_deficits(built):
    _f, _i, batches = built
    _b, plan, _s = batches["freeform"]
    assert set(R.CONTAINER_ITEMS) == {"pair of hiking boots", "pair of custom-fit insoles",
                                      "pair of made-to-measure curtains", "box of pastries", "fresh fruit box"}
    for m in plan.values():
        assert m["facts"]["ITEM"] in R.PLAIN_ITEMS[m["goods"]] and not R.CONTAINER.search(m["facts"]["ITEM"])
    v1 = json.loads((R.POOLS / "manifest.json").read_text(encoding="utf-8"))["summary"]["targets"]
    short = {t["item"].rsplit(" ", 1)[1]: t["shortfall"] for t in v1 if t["item"].startswith("documents, ")}
    asked = {r: n for r, n, _h in R.FREE_PLAN}
    for reg, s in short.items():
        assert asked[reg] >= max(s + 3, -(-3 * s // 2)), (reg, s, asked[reg])
    assert {r for r, _n, h in R.FREE_PLAN if h} == set(H.FREEFORM_HELD)
    assert all(m["held_out"] == (m["register"] in H.FREEFORM_HELD) for m in plan.values())
    assert "YOUR OWN words only" in R.FREE_PROMPT and "first name alone" in R.FREE_PROMPT


def test_extract_helpers_run_on_the_frozen_pools():
    wd, ff = R.v1_seen()
    assert len(wd) >= 118 and len(ff) >= 202
    reg = R.frozen_registry()
    n_old = len(reg.forms)
    new, drops = R.merge_wordings(reg, [])
    assert new == {} and drops == [] and len(reg.forms) == n_old
    taken = R.taken_wordings()[0]                                  # an admitted v1 text: a duplicate, dropped
    new, drops = R.merge_wordings(reg, [("t06r2.wording.x", (R.QF, taken, False, "tid", "0" * 64))])
    assert new == {} and drops[0]["class"] == "dedup"
    probe = f"On which date does {R.WD_NAMES[1]} end?"           # a check_wording probe, not an answer
    new, drops = R.merge_wordings(reg, [("t06r2.wording.y", (R.QF, probe, False, "tid", "0" * 64))])
    assert len(new) == 1 and drops == []
    fid = next(iter(new))
    assert reg.forms[fid].sem_id == LX.question_sem("T06", R.QF) and reg.status(fid) == "pending"
    gl = R.glex_batches(reg, [fid])
    assert [g[0] for g in gl] == list(R.LEX_READS)
    for _label, _k, _g, b in gl:
        assert len(b.chunks) == 1 and fid not in json.dumps(b.chunks[0])
        assert H.QUESTION_MEANINGS[R.QF] in b.prompt and H.QUESTION_DECOYS["q.t06.x_notice_end"] in b.prompt
    assert gl[0][3].prompt != gl[1][3].prompt                       # own meaning order per read
    assert R.g3h_batch([]) == (None, {})


def test_files_on_disk_match_the_rebuild(built):
    files, _i, _b = built
    if (R.ROOT / "TASKS.json").exists():
        assert R.check_on_disk(R.ROOT, files) == []
