"""families/T07/haiku/redo3/test_build_redo3_reads.py: lint, dedup and the G-LEX read tasks of T07 redo3.

Everything is built in memory (the on-disk files are only compared); nothing is written. Run (from lean/):
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
      c2_build/families/T07/haiku/redo3/test_build_redo3_reads.py
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[4]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import merged_pools as MP  # noqa: E402
from families.T07.haiku import extract_build as EB  # noqa: E402
from families.T07.haiku.redo2 import build_redo2 as R2  # noqa: E402
from families.T07.haiku.redo3 import build_redo3_reads as B  # noqa: E402


@pytest.fixture(scope="module")
def st():
    return B.state()


@pytest.fixture(scope="module")
def built(st):
    return B.read_files(st)


def test_three_wordings_and_seventeen_packs_were_authored(st):
    assert sum(p["meta"]["piece"] == "wording" for p in st["pieces"]) == 3
    assert len(st["packs"]) == 17


def test_wording_lint_keeps_the_v1_checks_and_the_brief():
    good = "Reading the advertisement and its fine print, does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED}?"
    assert B.lint_wording(good) == []
    assert B.lint_wording("Has {CUSTOMER} lost out on {ASKED} with order {ORDER_ID}, going by the fine print?") == []
    # 'forfeit' and the other verbs the redo2 reads sent to other meanings are refused by the brief
    assert any("brief" in x for x in B.lint_wording(good.replace("lose out on", "forfeit")))
    assert any("brief" in x for x in B.lint_wording(
        "Does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} or fail to get it?"))
    # a negation cue, a missing placeholder, an article before {ASKED}, two questions: v1 lint
    assert B.lint_wording(good.replace("lose out on", "not lose out on"))
    assert B.lint_wording("Does order {ORDER_ID} lose out on {ASKED}?")
    assert B.lint_wording("Does order {ORDER_ID} from {CUSTOMER} lose out on the {ASKED}?")
    assert B.lint_wording(5) == ["not a string"]


def test_every_wording_passes_and_goes_to_the_reads(st):
    assert not st["wording_drops"]
    assert len(st["read_fids"]) == 3
    for fid in st["read_fids"]:
        f = st["reg"].forms[fid]
        assert f.sem_id == "q.t07.yn_misses" and f.unit_ok and f.source == "haiku" and not f.held_out
        assert st["reg"].status(fid) == "pending" and f.extractions == []


def test_dedup_sees_every_earlier_text():
    seen = B.seen_texts()
    pools = MP.load(through="redo2")
    old = next(f for f in pools["lexicon"] if f["sem_id"] == "q.t07.yn_misses" and f["status"] == "admitted")
    assert ("lex", EB.norm(old["text"])) in seen
    rej = next(f for f in pools["lexicon"] if f["sem_id"] == "q.t07.yn_misses" and f["status"] == "rejected")
    assert ("lex", EB.norm(rej["text"])) in seen
    drops: list = []
    p = {"piece_id": "x#0", "value": old["text"].upper(), "meta": {"piece": "wording"}}
    assert EB.dedup([p], drops, seen) == [] and drops[0]["stage"] == "dedup"      # case and spacing do not matter


def test_the_registry_keeps_every_earlier_status():
    reg, recorded = B.merged_registry()
    assert len(recorded) == len(reg.forms) == len(MP.load(through="redo2")["lexicon"])      # every v1 and redo2 form, none else
    assert all(reg.status(fid) == s for fid, s in recorded.items())


def test_two_independent_reads_each_its_own_files(st, built):
    files, index = built
    assert index["n_tasks"] == 2 and index["outputs_expected"] == 6
    assert [r["read"] for r in index["tasks"]] == list(B.READS)
    b1, b2 = (st["batches"][r] for r in B.READS)
    assert b1.batch_id != b2.batch_id
    assert {c["task_id"] for c in b1.chunks}.isdisjoint({c["task_id"] for c in b2.chunks})
    assert set(b1.key).isdisjoint(set(b2.key))
    ans = [r["answer_file"] for r in index["tasks"]]
    assert len(set(ans)) == 2
    for r in index["tasks"]:
        assert r["allowed_write"] == [r["answer_file"]]
        assert Path(r["answer_file"]).parent == B.READS_ROOT / "answers"
        assert Path(r["task_file"]).parent == B.READS_ROOT / "tasks"
        assert r["task_file"] in r["allowed_read"] and len(r["allowed_read"]) == 3
        assert 1 <= r["n_items"] <= chunker.MAX_ITEMS
    # the same three wordings, filled the same way, in each read; the choices differ in order between reads
    t1 = sorted(i["text"] for i in b1.chunks[0]["items"])
    t2 = sorted(i["text"] for i in b2.chunks[0]["items"])
    assert t1 == t2 and len(set(t1)) == 3
    assert B.check_reads(files, st) == []


def test_items_are_gold_free_and_hold_the_closed_question_meanings(st, built):
    files, _ = built
    meanings = sorted(A.Q_SEM_MEANING.values())
    for b in st["batches"].values():
        for c in b.chunks:
            for it in c["items"]:
                assert set(it) == {"qid", "text", "choices"}
                assert sorted(it["choices"]) == meanings
                assert "{" not in it["text"] and "ORD-" in it["text"]
            text = files[f"tasks/{c['task_id']}.md"]
            assert not any(fid in text for fid in st["reg"].forms)


def test_files_on_disk_are_the_rebuild(built):
    files, _ = built
    diff = [rel for rel, text in sorted(files.items())
            if rel != "answers/README.txt" and (not (B.READS_ROOT / rel).is_file()
                                                or (B.READS_ROOT / rel).read_text(encoding="utf-8") != text)]
    assert diff == []


def test_packs_all_kept_and_the_asked_line_is_met(st):
    kept = [d for d in st["packs"] if d["status"] == "kept"]
    assert len(kept) == 17 and all(not d["reasons"] for d in kept)
    assert len(R2.kept_packs()) + len(kept) >= 60                      # freeze_pools.PACK_ASKED, not lowered


def test_pack_checks_drop_bad_packs(st):
    base = [p for p in st["pieces"] if p["meta"]["piece"] == "pack"]
    mod = copy.deepcopy(base[:4])
    mod[0]["value"]["customers"][0] = "Sung-min Park"                      # the v1 spelling rule
    mod[1]["value"]["store"] = R2.kept_packs()[0]["store"]                 # a taken store name
    mod[2]["value"]["regions"][0] = R2.kept_packs()[0]["categories"][0].split()[0].title()   # a taken word
    out = B.pack_decisions(mod, [])
    by = {d["piece_id"]: d for d in out}
    assert by[mod[0]["piece_id"]]["status"] == "dropped" and "customers" in " ".join(by[mod[0]["piece_id"]]["reasons"])
    assert by[mod[1]["piece_id"]]["status"] == "dropped"
    assert by[mod[2]["piece_id"]]["status"] == "dropped"
    assert by[mod[3]["piece_id"]]["status"] == "kept"
    # a word of a wording that goes to the reads cannot be a pack word
    w = mod[3]["value"]["regions"][0]
    out2 = B.pack_decisions([copy.deepcopy(mod[3])], [f"Does order {{ORDER_ID}} from {{CUSTOMER}} lose out on {{ASKED}} in {w}?"])
    assert out2[0]["status"] == "dropped" and "new wording" in " ".join(out2[0]["reasons"])


def test_the_plan_is_orchestrator_side_and_reads_do_not_touch_packs(built):
    files, _ = built
    plan = json.loads(files["plan/READS_PLAN.json"])
    assert plan["packs"]["asked"] == 17 and plan["packs"]["kept_v1_plus_redo3"] == 66
    assert set(plan["lex"]) and all(v["sem"] == "q.t07.yn_misses" for v in plan["lex"].values())
    for rel, text in files.items():
        if rel.startswith("tasks/"):
            assert "pack" not in text.lower().split("## items")[1]
