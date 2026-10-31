"""t37b/test_author_pool.py: in-memory tests for the T37b equiv paraphrase pool (nothing is written; no Haiku).

  tasks     <= 40 tasks; every pool entry has items; items carry only brief / slots / rules and none of the forbidden
            strings; slotted items name their slots; every task file names its exact answer path; deterministic
  lint      good paraphrase templates pass both programs on every probe fill; negation, antonym, quantifier, frame,
            placeholder and local-ban faults are dropped; duplicates drop; answers outside a chunk are refused
  admit     only 'same' / 'same' is admitted; shortfalls are reported against the targets
  pool      choices / records / judged feed the plan and the builder; the equiv partner is the filled template
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/t37b
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import fixtures as FX  # noqa: E402
from t37b import select as SEL  # noqa: E402
from t37b import sources as SRC  # noqa: E402

E = SRC.ENTRY_BY_KEY


@pytest.fixture(scope="module")
def batch():
    return AP.author_batch()


def test_tasks_shape(batch):
    assert 1 <= len(batch.chunks) <= AP.MAX_TASKS
    entries = {iid.split("|")[1] for iid in batch.key.values()}
    assert entries == {e.key for e in AP.pool_entries()}
    assert not entries & set(SRC.NO_POOL)
    for ch in batch.chunks:
        assert len(ch["items"]) <= AP.CHUNK
        for it in ch["items"]:
            assert set(it) == {"qid", "brief", "slots", "rules"}
            blob = json.dumps(it).lower()
            for f in AP.FORBID:
                assert f" {f} " not in f" {blob} ".replace('"', " ").replace(",", " ").replace(".", " ")
            ph = SRC.placeholders(it["brief"])
            assert sorted(ph) == it["slots"]
    assert AP.author_batch().batch_id == batch.batch_id          # deterministic (lint rebuilds it)


def test_every_task_file_names_its_answer_path(batch, tmp_path):
    files, rows = AP.task_files(batch, tmp_path, title="t", answer_format=AP.AUTHOR_FORMAT, kind_label="k")
    assert len(rows) == len(batch.chunks)
    for r in rows:
        text = files[str(Path(r["task_file"]).relative_to(tmp_path))]
        assert r["answer_file"] in text and r["answer_file"].endswith(".json")
        assert r["task_file"] in r["audit_allowed_read"] and r["audit_allowed_write"] == [r["answer_file"]]
        assert "key/" not in text


def test_slotted_entries_have_more_items(batch):
    per = {}
    for iid in batch.key.values():
        k = iid.split("|")[1]
        per[k] = per.get(k, 0) + 1
    for k, n in per.items():
        assert n == (AP.ITEMS_SLOTTED if SRC.pool_template(E[k])[1] else AP.ITEMS_FIXED)


GOOD = {
    "gd_check_covid/support": "Is the claim backed up by the evidence?",
    "gd_comve/against": "Of the two statements, is Statement {N} the one that goes against common sense?",
    "gd_taskmaster1/status": "Does the assistant's last message confirm {SPAN} for {ORDER}?",
    "gd_cards/claim": "Is this paragraph putting forward the contrarian climate claim that {CLAIM}?",
    "gd_multiwoz21_sysacts/match": "In its reply, did the assistant come up with at least one option that meets "
                                   "everything the customer asked for?",
    "gd_sc101/legal": "In most places, is this action against the law?",
}
BAD = [
    ("gd_check_covid/support", "Does the evidence not support the claim?"),               # adds a negation
    ("gd_check_covid/support", "Does the evidence contradict the claim?"),                # the closed antonym
    ("gd_check_covid/support", "Is it true that the evidence supports the claim?"),       # truth frame
    ("gd_check_covid/support", "Does the evidence support all of the claim?"),           # adds a quantifier
    ("gd_comve/against", "Of the two statements, is Statement 1 the one that goes against common sense?"),  # slot gone
    ("gd_comve/against", "Of the two statements, does the other one than Statement {N} make sense?"),  # antonym
    ("gd_taskmaster1/status", "Does the assistant's last message confirm {SPAN}?"),       # drops {ORDER}
    ("gd_cards/claim", "Is the correct answer that this paragraph makes the claim that {CLAIM}?"),  # local ban
    ("gd_multiwoz21_sysacts/match", "In its reply, did the assistant find any option that meets everything the "
                                    "customer asked for?"),                               # at least one -> any
    ("gd_sc101/legal", "Is this action against the law in many places?"),                 # most -> many
    ("gd_check_covid/support", "Does the evidence support the claim"),                    # no question mark
]


@pytest.mark.parametrize("key", sorted(GOOD))
def test_lint_passes_good_templates(key):
    assert AP.lint_one(E[key], GOOD[key]) == []


@pytest.mark.parametrize("key,text", BAD, ids=[f"{k}:{t[:30]}" for k, t in BAD])
def test_lint_drops_bad_templates(key, text):
    assert AP.lint_one(E[key], text)


def _raw(batch, fn):
    return {c["task_id"]: [{"qid": it["qid"], "questions": fn(batch.key[it["qid"]])} for it in c["items"]]
            for c in batch.chunks}


def test_lint_end_to_end_with_stand_in_answers(batch):
    def answer(iid):
        k = iid.split("|")[1]
        good = GOOD.get(k)
        return ([good] if good else []) + ["Does the evidence not support the claim?", "no question mark"]
    cands, rep = AP.lint(batch, _raw(batch, answer))
    assert rep["load_problems"] == []
    assert {c["sem"] for c in cands} == set(GOOD)                    # duplicates across items collapse to one
    assert len(cands) == len(GOOD) and rep["dropped"]["duplicate"] > 0
    for c in cands:
        assert AP.rec_pair_key(c) == BL.pair_key(SRC.pool_template(E[c["sem"]])[0], c["template"])
        assert c["haiku_task_id"].startswith(batch.batch_id) and c["qform"] == "equiv"
    raw = _raw(batch, lambda iid: [])
    first, second = batch.chunks[0]["task_id"], batch.chunks[1]["task_id"]
    raw[first].append({"qid": batch.chunks[1]["items"][0]["qid"], "questions": ["x?"]})   # a qid of another chunk
    _c, rep2 = AP.lint(batch, raw)
    assert any(second in p for p in rep2["load_problems"])


def test_polarity_reads_are_two_independent_batches(batch):
    cands, _ = AP.lint(batch, _raw(batch, lambda iid: [GOOD.get(iid.split("|")[1], "x")]))
    a, b = AP.polarity_batches(cands)
    assert a.batch_id != b.batch_id and a.key != b.key
    assert set(a.key.values()) == set(b.key.values()) == {AP.rec_pair_key(c) for c in cands}
    for ch in a.chunks + b.chunks:
        for it in ch["items"]:
            assert set(it) == {"qid", "question_a", "question_b"}


def test_admit_needs_two_same_reads(batch):
    cands, _ = AP.lint(batch, _raw(batch, lambda iid: [GOOD.get(iid.split("|")[1], "x")]))
    keys = [AP.rec_pair_key(c) for c in cands]
    ans_a = {k: {"relation": "same"} for k in keys}
    ans_b = {k: "same" for k in keys}
    ans_b[keys[0]] = "unclear"
    ans_a[keys[1]] = "opposite"
    admitted, rep = AP.admit(cands, ans_a, ans_b)
    assert len(admitted) == len(cands) - 2 and rep["admitted"] == len(admitted)
    assert all(c["reads"] == ["same", "same"] and c["status"] == "admitted" for c in admitted)
    assert not any("author_item" in c for c in admitted)
    assert rep["shortfall"] and all(v > 0 for v in rep["shortfall"].values())


def test_pool_feeds_plan_and_builder():
    pool = AP.Pool(FX.stand_in_pool())
    bases = SEL.eligible(FX.many_rows(4), [], status=FX.keep_all, strict_inputs=False)[0]
    plan, rep = SEL.plan_block(bases, n_complement=0, n_equiv=30, equiv_pool=pool.choices(), source_cap=1.0,
                               template_cap=1.0)
    eq = [i for i in plan if i.kind == "equiv"]
    assert eq and rep["equiv"] == len(eq)
    cands = BL.build_candidates(eq, records=pool.records)
    for c in cands:
        assert c.ok, c.problems
        vals = SRC.slot_values(c.item.base.entry, c.item.base.row["instructions"])
        assert c.question == SRC.fill(c.item.meta["para_text"], vals)
        assert BL.polarity_of(c, {}, {}, pool.judged) == ("same", "same")
    assert AP.pool_strings(pool)


def test_pool_file_texts_are_only_the_paraphrases():
    """g13_c2 reads pools/*.json record lists and checks every non-metadata string: only the paraphrase text.
    In memory: a stand-in path object serves the file text (nothing is written)."""
    import importlib
    g13 = importlib.import_module("g13_c2")
    pool = AP.Pool(FX.stand_in_pool())
    body = json.dumps({"family": "T37b", "g0_sha256": BL.G0_SHA256, "frozen": True, "paraphrases": pool.paraphrases})

    class _File:
        suffix = ".json"

        def read_text(self, **_kw):
            return body

    class _Log:
        def record(self, _p):
            pass
    recs = g13.pool_records(_File(), _Log())
    assert len(recs) == len(pool.paraphrases)
    for _line, rec in recs:
        assert g13.pool_texts(rec) == [rec["template"]]


def test_writers_refuse_before_a38():
    with pytest.raises(paths.DataBeforeFreeze):
        AP.write_author_tasks(prereg_text="no freeze ruling here")
    with pytest.raises(paths.DataBeforeFreeze):
        AP.run_lint(prereg_text="no freeze ruling here")
    with pytest.raises(paths.DataBeforeFreeze):
        AP.run_admit(prereg_text="no freeze ruling here")


def test_answers_are_only_flags():
    """Haiku's pool answers never reach a gold: partner gold comes from the base row alone (A37 b)."""
    pool = AP.Pool(FX.stand_in_pool())
    bases = SEL.eligible(FX.rows(), [], status=FX.keep_all, strict_inputs=False)[0]
    plan, _ = SEL.plan_block(bases, n_complement=0, n_equiv=10, equiv_pool=pool.choices(), source_cap=1.0,
                             template_cap=1.0)
    for c in BL.build_candidates(plan, records=pool.records):
        r = BL.partner_row(c)
        assert r["gold"] == c.item.base.row["gold"] and r["card"] == c.item.base.row["card"]
    with pytest.raises(chunker.ChunkError):
        chunker.make_batch("author_wording", "T37b", [("x", {"brief": "Question: Is it so that a holds?",
                                                             "slots": [], "rules": []})],
                           seed="s", prompt="p", forbid_strings=AP.FORBID)
