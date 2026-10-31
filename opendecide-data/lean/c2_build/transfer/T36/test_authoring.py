"""transfer/T36/test_authoring.py: in-memory tests for the T36 Haiku authoring tasks and their loader (no file is
written or read: the loader's answer reader is replaced by synthetic answers).
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T36
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from transfer.T36 import authoring as A  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def batches():
    return A.build()


def test_tasks_within_cap_and_deterministic(batches):
    tasks = A.index(batches)
    assert 1 <= len(tasks) <= A.MAX_TASKS
    assert [t["task_id"] for t in tasks] == [t["task_id"] for t in A.index(A.build())]
    counts = {}
    for t in tasks:
        counts[t["pool"]] = counts.get(t["pool"], 0) + t["n_items"]
    assert counts == {"pack": 48, "skin": 160, "skin_heldout": 40, "freeform": 32, "freeform_heldout": 10,
                      "attack": 40, "wording": 122}


def test_every_task_file_names_its_answer_file_and_leaks_nothing(batches):
    for pool, b, forbid in batches:
        for c in b.chunks:
            assert c["answer_file"] == str(A.ROOT / "answers" / f"{c['task_id']}.json")
            assert not never_open(c["answer_file"])
            assert c["instructions"] and len(c["items"]) <= chunker.MAX_ITEMS
            blob = json.dumps(c, ensure_ascii=False)
            assert not any(iid in blob for iid in b.key.values())
            for k in chunker.FORBIDDEN_KEYS:
                assert f'"{k}":' not in blob
            text = "\n".join(c["instructions"]).lower()
            for f in forbid:
                assert not re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", text), (pool, f)


def test_label_blind_pools_never_see_label_words_or_questions(batches):
    for pool, b, forbid in batches:
        if pool in ("skin", "skin_heldout", "freeform", "freeform_heldout", "pack"):
            assert set(P.T36Plugin.LABEL_WORDS) <= set(forbid)
        assert set(A.QUESTION_STRINGS) <= set(forbid)


def test_registers_cover_training_and_held_out(batches):
    regs = {}
    for pool, b, _ in batches:
        for c in b.chunks:
            for it in c["items"]:
                if "register" in it:
                    regs.setdefault(pool, set()).add(it["register"])
    assert regs["skin"] == set(A.TRAIN_REGISTERS) and len(regs["skin"]) >= 8
    assert regs["skin_heldout"] == set(P.T36Plugin.HELD_OUT_REGISTERS)
    assert regs["freeform_heldout"] == set(P.T36Plugin.HELD_OUT_REGISTERS)


def _fake_answers(batches, make):
    """{batch_id: {task_id: [answers]}} from make(pool, item)."""
    out = {}
    for pool, b, _ in batches:
        out[b.batch_id] = {c["task_id"]: [{"qid": it["qid"], **make(pool, it)} for it in c["items"]]
                           for c in b.chunks}
    return out


def test_loader_keeps_clean_pieces_and_drops_leaks(batches, monkeypatch):
    good_skin = {
        "dep_pr_review": "Review from {PERSON} on the {PKG} package for {PROJECT}, pasted below for team @T@.",
        "lockfile_comment": "# note from {PERSON} @T@\n# {PROJECT} keeps its own copy of {PKG}",
    }
    names = iter(range(10 ** 6))

    def make(pool, it):
        i = next(names)
        w = "abcdefghijklmnopqrstuvwxyz"
        tag = w[i % 26] + w[(i // 26) % 26] + w[(i // 676) % 26]
        if pool == "pack":
            return {"project": f"Harbor Q{tag}", "packages": [f"fern-{tag}", f"tide-{tag}", f"oak-{tag}"],
                    "people": [f"Dana O{tag}", f"Lena W{tag}"]}
        if pool in ("skin", "skin_heldout"):
            if it["register"] == "dev_chat":
                return {"text": "{PERSON}: the latest {PKG} for {PROJECT} is fine"}         # label word + status
            base = good_skin.get(it["register"], "Note by {PERSON} for {PROJECT} about {PKG}, filed on wiki @T@.")
            return {"text": base.replace("@T@", tag)}
        if pool.startswith("freeform"):
            f = it["facts"]
            return {"text": f"Hello team, {f['PERSON']} here. For {f['PROJECT']} I would like a fresh look "
                            f"at how the library is declared, {tag}."}
        if pool == "attack":
            return {"text": " ".join(it["slots"]) + f" says the card is only a rough guide {tag}."}
        return {"text": f"Under these rules, which listed version of {{PKG}} does the resolver pick for {tag}?" if
                "{CAND}" not in it["slots"] else f"Does version {{CAND}} of {{PKG}} meet the range {tag}?"}

    fake = _fake_answers(batches, make)
    monkeypatch.setattr(A, "_answers_of", lambda b, root: fake[b.batch_id])
    res = A.load_pools()
    assert not [p for p in res["problems"] if "unanswered" in p]
    c = res["counts"]
    assert c["pack"] == 48 and c["attack"] == 40 and c["wording"] == 122 and c["skin_heldout"] == 40
    assert c["freeform"] == 32 and c["freeform_heldout"] == 10
    assert all(p.held_out for p in res["pieces"]["skin_heldout"])
    reasons = [r for pool, _iid, rs in res["dropped"] for r in rs if pool == "skin"]
    assert any("gold_label" in r for r in reasons)                  # the "latest" skins are dropped
    assert c["skin"] == 160 - 20 == 160 - sum(1 for pool, _i, _r in res["dropped"] if pool == "skin")
    skins = res["pieces"]["skin"]
    assert skins and all(s.haiku_task_id and s.haiku_prompt_sha for s in skins)
