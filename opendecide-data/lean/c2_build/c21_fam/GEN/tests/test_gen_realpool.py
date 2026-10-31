"""GEN against the REAL (Haiku-authored) wording pool. Skeptic build tests, 18 Oct 2026. CPU only; nothing is written; no model, no network.

The lane's earlier tests ran only on the TEST-ONLY pool, and solver B could not read one row built from the real pool. These tests close that:
  * the pool files match pools/manifest.json and the pool interface,
  * every fragment wording variant and every question wording (1,176 of them) is read back by solver B to the answer solver A stored,
  * the stem contract B relies on (one scene sentence with no data; question templates current) holds,
  * no question wording can be read two ways (the template reader refuses an ambiguous question).
"""
import copy
import json
import os
import re

import pytest

import builder as BU
import export_question_templates as EQT
import gen_common as g
import pool_loader as PL
from b_main import solve_row
from gen_common import FORMS, GenAllow, WordingPool

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BKEYS = ("form", "k", "carrier", "stem", "options")


@pytest.fixture(scope="module")
def real():
    return PL.load_real_pool()


@pytest.fixture(scope="module")
def vocab():
    return PL.predicate_vocab()


def _agree(rows):
    bad = []
    for r in rows:
        out = solve_row({k: r[k] for k in BKEYS})
        if out["status"] != "ok" or out["answer_index"] != r["label"]:
            bad.append((r["row_id"], out.get("status"), out.get("code"), out.get("detail")))
    return bad


def _restricted(pool, pick_fragment=None, one_question=None):
    """A pool where every fragment key keeps ONE variant (index pick_fragment mod len) and/or one question key keeps ONE wording."""
    ent = {k: list(v) for k, v in pool.entries.items()}
    if pick_fragment is not None:
        for k, v in ent.items():
            if not k.startswith("q."):
                ent[k] = [v[pick_fragment % len(v)]]
    if one_question is not None:
        key, idx = one_question
        ent[key] = [pool.entries[key][idx]]
    return WordingPool(ent, testonly=False, name="restricted")


def test_pool_files_match_manifest_and_interface(real):
    sha = PL.verify_files()
    assert len(sha) == 8
    assert not g.check_pool(real)
    for k in real.entries:
        if k.startswith("q."):
            assert len(real.entries[k]) >= 56 and len(real.train_ids(k)) >= 50 and len(real.dev_ids(k)) >= 1


def test_question_templates_file_is_current():
    cur = EQT.build()
    with open(EQT.OUT, "r", encoding="utf-8") as f:
        assert json.load(f) == cur, "run export_question_templates.py"


def test_scene_sentences_obey_the_stem_contract(real):
    for k, lst in real.entries.items():
        if k.startswith("scene."):
            for t in lst:
                assert t.endswith(".") and not re.search(r"[0-9{}=]|\. |\n", t), (k, t)


def test_predicate_vocabulary_is_closed_and_reader_safe(vocab):
    assert set(vocab) == set(g.TRAIN_DOMAINS + g.DEV_DOMAINS)
    flat = [p for v in vocab.values() for p in v]
    assert len(flat) == len(set(flat)) == 192


@pytest.mark.parametrize("variant", range(6))
def test_every_fragment_variant_is_read_back_by_solver_b(real, vocab, variant):
    pool = _restricted(real, pick_fragment=variant)
    bad = []
    for form in FORMS:
        b = BU.Builder("frag%d-%s" % (variant, form), pool, allow=GenAllow(), provisional=False, mode="dry", vocab=vocab, adversary=False)
        rows = []
        for i in range(14):
            rows.extend(b.unit(form, "train", i, pair_prob=0.3))
        assert len(rows) >= 10, (form, len(rows))
        bad += _agree(rows)
    assert not bad, bad[:5]


def test_every_question_wording_is_read_back_by_solver_b(real, vocab):
    """1,176 question templates, one row each: B recovers the slots (so the SAME answer) from every wording."""
    bad, n = [], 0
    for key in sorted(k for k in real.entries if k.startswith("q.")):
        form = key[2:].split(".")[0]
        variant = "overlap" if key.endswith(".overlap") else None
        for j in range(len(real.entries[key])):
            pool = _restricted(real, one_question=(key, j))
            b = BU.Builder("q%d-%s" % (j, key), pool, allow=GenAllow(), provisional=False, mode="dry", vocab=vocab, adversary=False)
            rows = []
            for i in range(30):
                for r in b.unit(form, "train", i, pair_prob=0.0):
                    if variant is None or r["spec"].get("variant") == variant:
                        if form != "TM-T4" or (r["spec"].get("variant") == "overlap") == (variant == "overlap"):
                            rows.append(r)
                if rows:
                    break
            assert rows, (key, j)
            n += len(rows)
            bad += _agree(rows[:1])
    assert n >= 1176
    assert not bad, bad[:5]


def test_ambiguous_question_is_refused_not_guessed():
    """Two templates that read the same text with different slot values must make B refuse (ParseFail), never pick one."""
    import b_questions as BQ
    BQ._load()
    saved = BQ._CACHE["sets"]
    try:
        BQ._CACHE["sets"] = {"q.X": [("a", "Find {offset} after {start}.", BQ._compile("Find {offset} after {start}.")),
                                     ("b", "Find {start} after {start}.", BQ._compile("Find {start} after {start}."))]}
        text = "Some facts.\nFind 3 days after 2026-01-01."
        BQ.read_question("q.X", text)                       # only one reading: fine
        BQ._CACHE["sets"] = {"q.X": [("a", "Find {offset} after {start}.", BQ._compile("Find {offset} after {start}.")),
                                     ("b", "Find {pc} after {pd}.", BQ._compile("Find {pc} after {pd}."))]}
        BQ._CACHE["sets"]["q.X"][0] = ("a", "Find {pa} after {pb}.", BQ._compile("Find {pa} after {pb}."))
        with pytest.raises(Exception) as ei:
            BQ.read_question("q.X", text)
        assert "ambiguous_question" in str(ei.value)
    finally:
        BQ._CACHE["sets"] = saved


def test_no_relation_fact_is_ever_negated_in_a_spec(real, vocab):
    """Skeptic fix: a pair edit used to flip a relation fact to negative while the stem still said it positively."""
    bad = 0
    for form in ("LG-L1", "LG-L2", "LG-L4"):
        b = BU.Builder("relneg-" + form, real, allow=GenAllow(), provisional=False, mode="rows", vocab=vocab, adversary=False)
        for i in range(400):
            for r in b.unit(form, "train", i, pair_prob=0.9):
                for a, s in r["spec"]["facts"]:
                    if tuple(a)[0] == "R" and not s:
                        bad += 1
    assert bad == 0


def test_trap_budget_never_freezes_a_form():
    """Skeptic fix: CA-C3 on the dev split once produced 14 rows out of 600 units (the trap cap froze the form)."""
    pool = g.make_testonly_pool()
    for split in ("train", "dev"):
        b = BU.Builder("freeze-CA-C3-" + split, pool, allow=GenAllow(), provisional=False, mode="dry")
        rows = []
        for i in range(300):
            rows.extend(b.unit("CA-C3", split, i, pair_prob=0.35))
        assert len(rows) >= 330, (split, len(rows))


def test_vocab_rows_name_check_and_share(real, vocab):
    n_v = n = 0
    for form in ("LG-L1", "LG-L2", "LG-L4"):
        b = BU.Builder("vocab-" + form, real, allow=GenAllow(), provisional=False, mode="rows", vocab=vocab, adversary=False)
        for i in range(120):
            for r in b.unit(form, "train", i, pair_prob=0.0):
                n += 1
                assert BU.validate_row(r) == []
                if r["spec"]["pred_source"] == "vocab":
                    n_v += 1
                    assert all(p in vocab[r["domain_id"]] for p in r["spec"]["pred_names"])
    assert 0.35 < n_v / n < 0.65
