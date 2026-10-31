"""t37b/haiku/redo2/test_t37b_redo2.py: the T37b redo2 tasks (build_redo2.py), built in memory.

Checks: gold-free chunks of <= 8 items with only the chunker's author_wording fields; no forbidden string (answer
words, truth frames, banned patterns) in any task file; every task file names its own answer path and holds the inline
contract; new ids (no v1 id, qid or task id); each blocker's fix is in its items; the gate is unchanged: the v1
failure modes still fail author_pool.lint_one + gsl_pool_lint.gsl_check, and the redo2 required forms pass it; the
extract lint drops v1 duplicates and G-SL failures and keeps passing texts; admission stays 2/2 'same'; the merged pool
loader refuses a supplement that is not tied to the frozen v1 pool or repeats a v1 paraphrase; files on disk (if
written) are the same bytes as the rebuild. Nothing is written under lean/ and no answer file is made up: the probe
texts below are gate inputs in memory, never answers.
Run (from lean/): ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/t37b/haiku/redo2
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import importlib.util  # noqa: E402

import pytest  # noqa: E402

_spec = importlib.util.spec_from_file_location("t37b_build_redo2", HERE / "build_redo2.py")   # unique module name
R = importlib.util.module_from_spec(_spec)
sys.modules["t37b_build_redo2"] = R
_spec.loader.exec_module(R)
from c2_kit import chunker  # noqa: E402
from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import gsl_pool_lint as GL  # noqa: E402


@pytest.fixture(scope="module")
def built():
    files, index = R.author_files()
    return files, index, R.author_batch()


def test_author_check_is_clean_and_tasks_self_contained(built):
    files, index, b = built
    assert R.check_author(files, index) == []
    assert index["n_tasks"] == 3 and index["n_items"] == 22 and index["outputs_expected"] == 110
    for row in index["tasks"]:
        text = files[str(Path(row["task_file"]).relative_to(R.ROOT))]
        assert row["answer_file"] in text and "ANSWER CONTRACT" in text
        assert "/t37b/haiku/redo2/answers/" in row["answer_file"] and row["allowed_write"] == [row["answer_file"]]
        assert row["task_file"] in row["allowed_read"]
        assert hashlib.sha256(text.encode()).hexdigest() == row["task_sha256"]
    for c in b.chunks:
        assert 1 <= len(c["items"]) <= R.CHUNK
        for it in c["items"]:
            assert set(it) == {"qid"} | set(chunker.TASK_KINDS["author_wording"])


def test_new_ids_never_v1(built):
    _f, _i, b = built
    v1 = AP.author_batch()
    assert b.batch_id != v1.batch_id
    assert not set(b.key) & set(v1.key)
    assert not set(b.key.values()) & set(v1.key.values())
    assert all(iid.startswith("t37b-r2|") for iid in b.key.values())


def test_each_fix_is_in_its_items(built):
    _f, _i, b = built
    items, plan = R.author_items()
    per = {}
    for iid, it in items:
        key = plan[iid]["entry"]
        per[key] = per.get(key, 0) + 1
        rules = " ".join(it["rules"])
        assert R.WORDS_RULE in it["rules"]
        if key == "gd_comve/against":
            assert R.COMVE_SHAPE in it["rules"] and R.COMVE_COUNT in it["rules"] and R.COMVE_SLOT in it["rules"]
        elif key in R.LEAST_NOUN:
            assert "at least a single " + R.LEAST_NOUN[key] in rules and "'least'" in rules
        else:
            assert R.FINAL_RULE in it["rules"]
            assert "Per the assistant's latest message, is {SPAN} confirmed for {ORDER}?" in rules   # v1 taken
        assert "'last message'" not in rules.replace(R.FINAL_RULE, "")                     # the v1 example is gone
    assert per == {k: n for k, n, _b, _x in R.PLAN}


def test_gate_is_unchanged():
    assert BL.g0_problems() == []
    assert BL.G0_SHA256 == "9733b721fcab18c1bbfaf15567d99e6a52433fd7918c221963a8b3eb46da9cd4"
    assert hashlib.sha256(R.V1_POOL.read_bytes()).hexdigest() == R.V1_POOL_SHA256
    for key, text in R.V1_FAILS.items():
        assert R.gate(key, text), key                                   # the diagnosed v1 drops still drop
    for key, text in R.R2_FORMS.items():
        assert R.gate(key, text) == [], (key, R.gate(key, text))       # the redo2 forms pass the same gate
    # G-SL still reads a mid-sentence 'Statement' as a name and 'one' / 'last' as CORE words (no allowance added)
    rec = AP.record("gd_comve/against", "Of the statements shown, does Statement {N} go against common sense?", "x", "y")
    assert {v.rule for v in GL.gsl_check(rec)} == {"name"}


def test_lint_r2_in_memory(built):
    _f, _i, b = built
    _items, plan = R.author_items()
    iid = {plan[i]["entry"]: i for i in sorted(plan)}
    seen = R.v1_seen()
    v1_dup = R.taken("gd_taskmaster1/status")[0]                    # the v1 admitted text: passes lint, then dedups
    answers = {   # stand-in answer objects (memory only), keyed by internal id as chunker.load_answers returns them
        iid["gd_comve/against"]: {"questions": [
            R.R2_FORMS["gd_comve/against"],
            "Of the statements shown, does Statement {N} go against common sense?",           # G-SL name
            R.V1_FAILS["gd_comve/against"]]},                                                  # v1 duplicate
        iid["gd_multiwoz21_sysacts/match"]: {"questions": [R.R2_FORMS["gd_multiwoz21_sysacts/match"],
                                                           R.R2_FORMS["gd_multiwoz21_sysacts/match"]]},  # duplicate
        iid["gd_nhtsa_complaints/injury"]: {"questions": [
            "Does this vehicle safety complaint say that at least one person was actually hurt?"]},   # G-SL number
        iid["gd_taskmaster1/status"]: {"questions": [R.R2_FORMS["gd_taskmaster1/status"], v1_dup]},
    }
    cands, gdrops, rep = R.lint_r2(b, plan, answers, seen)
    assert sorted(c["template"] for c in cands) == sorted(R.R2_FORMS[k] for k in
                                                          ("gd_comve/against", "gd_multiwoz21_sysacts/match",
                                                           "gd_taskmaster1/status"))
    assert rep["dropped"] == {"G-SL": 2, "duplicate of a v1 text": 2, "duplicate": 1}
    assert {d["sem"] for d in gdrops} == {"gd_comve/against", "gd_nhtsa_complaints/injury"}
    pa, pb = R.polarity_batches(cands)
    assert pa.batch_id != pb.batch_id and len(pa.key) == len(cands) == len(pb.key)
    assert pa.prompt == AP.POOL_POLARITY_PROMPT
    ka = {k: {"relation": "same"} for k in pa.key.values()}
    kb = dict(ka)
    kb[AP.rec_pair_key(cands[0])] = {"relation": "unclear"}
    admitted, arep = AP.admit(cands, ka, kb)
    assert len(admitted) == len(cands) - 1 and all(a["reads"] == ["same", "same"] for a in admitted)


def test_merged_pool_loader(tmp_path):
    v1 = AP.load_pool(R.V1_POOL)
    assert len(R.load_merged_pool(R.V1_POOL, tmp_path / "absent.json").paraphrases) == len(v1.paraphrases)
    rec = AP.record("gd_taskmaster1/status", R.R2_FORMS["gd_taskmaster1/status"], "t", "p") | {
        "reads": ["same", "same"], "status": "admitted"}
    good = {"family": "T37b", "g0_sha256": BL.G0_SHA256, "frozen": True, "supplement_of": R.V1_POOL_SHA256,
            "paraphrases": [rec]}
    p = tmp_path / "supp.json"
    p.write_text(json.dumps(good), encoding="utf-8")
    assert len(R.load_merged_pool(R.V1_POOL, p).paraphrases) == len(v1.paraphrases) + 1
    p.write_text(json.dumps(good | {"supplement_of": "0" * 64}), encoding="utf-8")
    with pytest.raises(RuntimeError):
        R.load_merged_pool(R.V1_POOL, p)
    p.write_text(json.dumps(good | {"paraphrases": [v1.paraphrases[0]]}), encoding="utf-8")
    with pytest.raises(RuntimeError):
        R.load_merged_pool(R.V1_POOL, p)
    p.write_text(json.dumps(good | {"paraphrases": [rec | {"reads": ["same", "unclear"]}]}), encoding="utf-8")
    with pytest.raises(RuntimeError):
        R.load_merged_pool(R.V1_POOL, p)


def test_files_on_disk_match_the_rebuild(built):
    files, _i, _b = built
    if not (R.ROOT / "TASKS.json").is_file():
        pytest.skip("author tasks not written yet")
    assert R.check_on_disk(R.ROOT, files) == []
