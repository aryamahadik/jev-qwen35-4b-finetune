"""c2_build/families/T29/test_authoring.py: the T29 Haiku authoring tasks, built in memory (nothing is written).

Checks: <= 40 tasks, one chunk of <= 50 gold-free items each; no label word, option text, code word or stand-in
question string in any task file (the precedence task may name the tier word "forbidden"); every task file names its
own answer path; the planned outputs cover the G0 section 2 pools with room for G-SL / G-LEX losses.
Run (from lean/): ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T29/test_authoring.py
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pytest  # noqa: E402

from c2_kit import chunker  # noqa: E402
from families.T29 import authoring as A  # noqa: E402
from families.T29 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def tasks():
    return A.build_tasks()


def test_tasks_are_few_small_gold_free_and_name_their_answer_file(tasks):
    assert len(tasks) <= A.MAX_TASKS
    assert A.check(tasks) == []
    ids = [t.task_id for t in tasks]
    assert len(set(ids)) == len(ids)
    for t in tasks:
        assert len(t.batch.chunks) == 1 and 1 <= len(t.chunk["items"]) <= chunker.MAX_ITEMS
        text = t.text()
        assert str(t.answer_file()) in text and t.answer_file().name == f"{t.task_id}.json"
        for it in t.chunk["items"]:
            assert set(it) - {"qid"} <= set(chunker.TASK_KINDS[t.kind])
        assert not any(i in text for i in t.batch.key.values())


def test_label_words_reach_no_brief(tasks):
    for t in tasks:
        low = t.text().lower()
        for w in P.T29Plugin.LABEL_WORDS:
            if t.name == "lex-prec" and w == "forbidden":
                continue
            assert f" {w} " not in f" {low} ".replace("\n", " "), (t.name, w)
        for code in P.CODE_WORDS:
            assert code.lower() not in low


def test_planned_outputs_cover_the_g0_pools(tasks):
    out = collections.Counter()
    for t in tasks:
        out[(t.pool, t.held_out)] += t.outputs
    assert out[("skins", False)] >= 8 * 100 and out[("skins", True)] >= 2 * 40      # >= 8 + 2 registers
    regs = collections.Counter(it["register"] for t in tasks if t.pool == "skins" for it in t.chunk["items"])
    assert set(regs) == set(P.T29Plugin.REGISTERS)
    assert out[("wordings", False)] >= 30 * 5 and out[("wordings", True)] >= 30          # >= 30 per family
    wq = {it["brief"]["meaning"] for t in tasks if t.pool == "wordings" for it in t.chunk["items"]}
    # every question form of the v1 plan; the double-negation form has its own round (build_dneg_tasks, FIX-6)
    assert wq == {A.Q_MEANING[q] for q in P.T29Plugin.QFORMS if q not in P.DNEG_FORMS}
    assert out[("freeform", False)] >= 100 and out[("packs", False)] >= 75
    assert out[("lexicon:precedence", False)] >= 20 and out[("lexicon:comparator", False)] >= 60
    assert out[("lexicon:confirmation", False)] >= 60 and out[("attack", False)] >= 60
    assert out[("actions", False)] >= 120
