"""families/T07/haiku/redo3/test_build_redo3.py: the T07 redo3 author tasks (the two remaining shortfall lines).

Everything is built in memory; nothing is written. Run (from lean/):
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
      c2_build/families/T07/haiku/redo3/test_build_redo3.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[4]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import validate_answers as VA  # noqa: E402
from families.T07.haiku.redo2 import build_redo2 as R2  # noqa: E402
from families.T07.haiku.redo3 import build_redo3 as B  # noqa: E402


@pytest.fixture(scope="module")
def g():
    return B.gaps()


@pytest.fixture(scope="module")
def built(g):
    return B.author_files(g=g)


@pytest.fixture(scope="module")
def batches(g):
    return B.build_batches(g)


def test_gaps_are_the_two_a3_shortfalls(g):
    assert g == {"wording": 1, "packs": 11}            # STAGE_A3_REPORT.json: yn_misses training 19/20, packs 49/60


def test_asks_are_about_fifty_percent_over_the_gap(g, built):
    _files, index = built
    assert index["asked"] == {B.LINE_WORD: 3, B.LINE_PACKS: 17}
    for gap, got in ((g["wording"], 3), (g["packs"], 17)):
        assert got >= math.ceil(1.5 * gap) and got >= gap + 2
    assert index["n_tasks"] == 2 <= 12


def test_no_pending_reads(built):
    _files, index = built
    pend = index["pending_reads"]
    assert pend["none_pending"] and all(not r["pending"] for r in pend["result"].values())
    assert {r["chunks"] for r in pend["result"].values()} == {r["answers"] for r in pend["result"].values()} or \
        all(r["chunks"] == r["answers"] for r in pend["result"].values())


def test_checks_pass(g, built):
    files, _index = built
    assert B.check_author(files, g) == []


def test_files_on_disk_match_rebuild(built):
    files, _index = built
    assert B.check_on_disk(B.ROOT, files) == []


def test_no_stale_files_on_disk(built):
    files, _ = built
    # code files of this folder; the agents' answer files; reads/ is the next stage (build_redo3_reads.py, own tests)
    ours = {"build_redo3.py", "test_build_redo3.py", "build_redo3_reads.py", "test_build_redo3_reads.py",
            "admit_redo3.py", "test_admit_redo3.py"}                          # admit_redo3: the pools/redo3 freeze
    on_disk = {str(p.relative_to(B.ROOT)) for p in B.ROOT.rglob("*")
               if p.is_file() and "__pycache__" not in p.parts and ".pytest_cache" not in p.parts
               and p.relative_to(B.ROOT).parts[0] != "reads"
               and not (p.relative_to(B.ROOT).parts[0] == "answers" and p.suffix == ".json")}
    assert on_disk - ours == set(files)                                             # nothing left from an older build
    task_ids = {t["task_id"] for t in json.loads(files["TASKS.json"])["tasks"]}
    assert {p.stem for p in (B.ROOT / "answers").glob("*.json")} <= task_ids        # answers are written by agents only


def test_task_files_are_self_contained(batches, built):
    files, index = built
    for name, (b, plan, spec) in batches.items():
        for c in b.chunks:
            tid = c["task_id"]
            text = files[f"tasks/{tid}.md"]
            head = text.split("\n")
            assert head[3] == str(B.ROOT / "answers" / f"{tid}.json")           # the exact answer path, on top
            assert "/redo3/answers/" in head[3]
            assert "ANSWER CONTRACT" in text and "Literal JSON example" in text
            assert b.prompt.rstrip() in text                                      # the full prompt, inline
            assert json.dumps(c["items"], ensure_ascii=False, indent=1) in text   # the items, inline
            for it in c["items"]:
                assert it["qid"] in text
            assert "prompts/" not in text and "chunks/" not in text               # nothing to open elsewhere
    for r in index["tasks"]:
        assert r["allowed_read"] == [r["task_file"]] and len(r["allowed_write"]) == 1
        assert r["allowed_write"][0].startswith(str(B.ROOT / "answers") + "/")


def test_literal_example_is_json_with_the_real_qid(batches, built):
    files, _ = built
    for name, (b, plan, spec) in batches.items():
        tid = b.chunks[0]["task_id"]
        line = next(x for x in files[f"tasks/{tid}.md"].split("\n") if x.startswith("Literal JSON example"))
        arr = json.loads(line.split("): ", 1)[1])                      # the whole example is valid JSON
        assert arr[0]["qid"] == b.chunks[0]["items"][0]["qid"] and set(arr[0]) == {"qid", spec[2]}


def test_wording_brief_is_lose_out_on_only(batches):
    b, plan, _spec = batches["wordings"]
    (it,) = b.chunks[0]["items"]
    meaning = it["brief"]["meaning"]
    assert "lose out on" in meaning and not re.search(r"forfeit|go short|shut out", meaning, re.I)
    assert it["brief"]["how_many"] == 3 and set(it["slots"]) == {"CUSTOMER", "ORDER_ID", "ASKED"}
    assert b.prompt == R2.WORDING_PROMPT                                          # the family's unchanged prompt
    (iid,) = plan
    assert plan[iid]["qform"] == "yn_misses" and not plan[iid]["held_out"]


def test_pack_items(batches):
    b, plan, _spec = batches["packs"]
    items = [x for c in b.chunks for x in c["items"]]
    assert len(items) == 17 and set(plan) == set(b.key.values())
    assert all(set(x) == {"qid", "brief"} for x in items)                          # author_pack: brief only
    assert sum(1 for p in plan.values() if p["v1_dropped"]) == 11                  # every dropped v1 shop kind again
    assert not any(p["held_out"] for p in plan.values())
    kept = R2.kept_packs()
    n3 = sum(len(p["ladder"]) == 3 for p in kept) + sum(p["ladder_levels"] == 3 for p in plan.values())
    n4 = len(kept) + len(plan) - n3
    assert abs(n3 - n4) <= 1                                                       # kept + new ladders even out
    assert all(x["brief"]["shop_kind"] in A.PACK_SETTINGS for x in items)


def test_pack_prompt_closes_the_v1_losses(batches):
    b, _plan, _spec = batches["packs"]
    words = set(A._words(b.prompt))
    assert all(w in words for w in R2.PACK_WORDS if not A._bad(w))                 # R3: the taken words are listed
    for store in B.taken_stores():
        assert store in b.prompt
    assert "Sung-min Park" in b.prompt and "MacLeod" in b.prompt                  # the spelling rule that cost 10 of 11
    assert B.EXAMPLE_PACK["store"] not in B.taken_stores()
    assert A.lint_pack(B.EXAMPLE_PACK, 3) == []


def test_pack_prompt_lists_the_pool_vocabulary(batches):
    b, _plan, _spec = batches["packs"]
    vocab = B.pool_vocab()
    words = set(A._words(b.prompt))
    assert len(vocab) > 1000 and all(w in words for w in vocab if not A._bad(w))
    assert not vocab & B.TAKEN_WORDS and "garden" not in vocab                   # taken words are listed once, apart
    assert B.pack_pool_collisions(B.EXAMPLE_PACK) == []                           # the example is itself clean
    assert B.pack_pool_collisions({"ladder": ["Standard"], "regions": [], "categories": ["office chairs"]}) \
        == ["office", "standard"] or B.pack_pool_collisions({"ladder": ["Standard"], "regions": [],
                                                              "categories": []}) == ["standard"]


def test_example_pack_survives_check_packs():
    kept, dropped = A.check_packs(R2.kept_packs() + [B.EXAMPLE_PACK])
    assert not dropped and len(kept) == len(R2.kept_packs()) + 1


def test_synthetic_answers_pass_and_break_the_validator(batches):
    # a valid answer for each task passes the strict validator; common breaks are caught (nothing is written)
    for name, (b, plan, spec) in batches.items():
        chunk, field = b.chunks[0], spec[2]
        good = []
        for it in chunk["items"]:
            if field == "pack":
                pk = dict(B.EXAMPLE_PACK)
                pk["ladder"] = B.EXAMPLE_PACK["ladder"][:it["brief"]["ladder_levels"]] + \
                    ["Anvil"] * (it["brief"]["ladder_levels"] - 3)
                good.append({"qid": it["qid"], "pack": pk})
            else:
                good.append({"qid": it["qid"], "wordings": ["x?"] * it["brief"]["how_many"]})
        assert VA.check_answer_array(b.kind, field, chunk, good, len(chunk["items"])) == []
        assert VA.check_answer_array(b.kind, field, chunk, good[:-1], len(chunk["items"]))        # a missing item
        assert VA.check_answer_array(b.kind, field, chunk, {"answers": good}, len(chunk["items"]))  # not one array
        bad = [dict(good[0], qid="qxxxxxxxxxx")] + good[1:]
        assert VA.check_answer_array(b.kind, field, chunk, bad, len(chunk["items"]))              # a foreign qid
        loaded, probs = chunker.load_answers(b, {chunk["task_id"]: good})
        assert not probs and len(loaded) == len(chunk["items"])


def test_no_label_or_question_leaks(built):
    files, _ = built
    for rel, text in files.items():
        if not rel.startswith(("tasks/", "chunks/")):
            continue
        low = text.lower()
        for f in A.FORBID:
            assert not (f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low)), (rel, f)


def test_chunk_and_task_ids_are_unique(batches):
    tids = [c["task_id"] for b, _p, _s in batches.values() for c in b.chunks]
    qids = [it["qid"] for b, _p, _s in batches.values() for c in b.chunks for it in c["items"]]
    assert len(set(tids)) == len(tids) and len(set(qids)) == len(qids)
    assert Counter(t.split("-")[1] for t in tids) == {"author_pack": 1, "author_wording": 1}
