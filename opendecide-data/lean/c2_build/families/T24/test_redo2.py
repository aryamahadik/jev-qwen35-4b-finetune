"""families/T24/test_redo2.py: the T24 redo2 Mode F e-mail task (redo2.py), built in memory.

Checks: one gold-free chunk of 50 e-mail items naming its own answer path, every T24 customer name, 30 sign-off and 20
self-introduction items; the prompt is the v1 Mode F prompt plus the e-mail rules (a new prompt, so a new G3-H
template, G0 3.2 v2.1), and the read reuses the v1 G3-H prompt and field; the writer check flags a name in the greeting
and passes a signed or self-introduced e-mail; G3-H templates are scored apart; the files on disk (when written) equal
the rebuild. Nothing is written.

Run (from lean/):  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
                   c2_build/families/T24/test_redo2.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h  # noqa: E402
from families.T24 import authoring as A  # noqa: E402
from families.T24 import extract_stage as X  # noqa: E402
from families.T24 import plugin as P  # noqa: E402
from families.T24 import redo2 as R  # noqa: E402

GREETED = "Hi Oscar Byrne,\nThis is a short message regarding my case. Could someone please have a look at the request " \
          "when that suits you?\nMany thanks,"
SIGNED = "Hello,\nThanks for reading this e-mail. This is my opening message about my case. Could someone please look " \
         "at the request and let me know where things stand?\nKind regards,\nInes Duarte"
INTRO = "Good day,\nThis is Ines Duarte, writing about my case. Could someone please look at the request when there is " \
        "a moment? Thank you for your help.\nKind regards,"


@pytest.fixture(scope="module")
def task():
    tasks = R.build_tasks()
    assert len(tasks) == 1
    return tasks[0]


def test_one_small_gold_free_chunk_with_its_answer_path(task):
    assert R.check_author([task]) == []
    assert len(task.batch.chunks) == 1 and len(task.chunk["items"]) == R.N_EMAIL <= chunker.MAX_ITEMS
    text = task.text()
    assert str(task.answer_file()) in text and task.answer_file().name == f"{task.task_id}.json"
    assert str(task.answer_file()).startswith(str(R.ROOT / "answers"))
    assert not any(iid in text for iid in task.batch.key.values())
    for it in task.chunk["items"]:
        assert set(it) - {"qid"} <= set(chunker.TASK_KINDS["author_freeform"])
        assert it["register"] == "email" and set(it["facts"]) == {"CUSTOMER"}
    assert {m["customer"] for m in task.meta.values()} == set(P.CUSTOMERS)
    assert Counter(m["placement"] for m in task.meta.values()) == {"signoff": 30, "intro": 20}
    files, manifest = R.author_files([task])
    row = manifest["tasks"][0]
    assert row["allowed_read"] == [str(task.task_file())] and row["allowed_write"] == [str(task.answer_file())]
    assert not R._forbidden_hits(files[str(task.task_file().relative_to(R.ROOT))])


def test_prompt_is_v1_mode_f_plus_the_writer_rules(task):
    base = A.FREEFORM_PROMPT[: -len(A._answer_block("text"))]
    assert task.batch.prompt.startswith(base) and task.batch.prompt.endswith(A._answer_block("text"))
    for rule in ("7. The CUSTOMER is the person who raised the case and the WRITER",
                 "9. The greeting line names nobody", "10. Put the customer's name where the item's rules say"):
        assert rule in task.batch.prompt
    assert task.batch.prompt_sha != chunker.sha(A.FREEFORM_PROMPT)          # a new prompt: a new G3-H template
    v1 = [t for t in A.build_tasks() if t.kind == "author_freeform"]
    assert {t.batch.prompt_sha for t in v1} == {chunker.sha(A.FREEFORM_PROMPT)}   # v1: template = register
    assert task.template_id != R.template_id("email", chunker.sha(A.FREEFORM_PROMPT))


def test_writer_check_flags_the_greeting_and_passes_signed_or_introduced():
    assert R.email_role_problems(GREETED, "Oscar Byrne")
    assert R.email_role_problems("Hello,\nI write about my case and the request.\nThanks,", "Oscar Byrne")
    for text, name in ((SIGNED, "Ines Duarte"), (INTRO, "Ines Duarte")):
        assert R.email_role_problems(text, name) == []
        assert A.check_freeform(text, name) == [] and X.freeform_rule_problems(text, name) == []


def test_lint_drops_v1_duplicates_and_bad_emails(task):
    base = {"task_id": task.task_id, "prompt_sha": task.batch.prompt_sha, "template": task.template_id,
            "held_out": False, "register": "email", "placement": "signoff"}
    pieces = [dict(base, iid="a", customer="Oscar Byrne", text=GREETED),
              dict(base, iid="b", customer="Ines Duarte", text=SIGNED),
              dict(base, iid="c", customer="Ines Duarte", text=INTRO),
              dict(base, iid="d", customer="Ines Duarte", text=INTRO)]
    kept, drops = R.lint(pieces, {X.norm(SIGNED): "t24-v1-free-b-40#0"})
    assert [p["iid"] for p in kept] == ["c"]
    assert {d["iid"]: d["stage"] for d in drops} == {"a": "lint", "b": "dedup", "d": "dedup"}


def test_read_task_reuses_the_v1_read_prompt_and_field(task):
    pieces = [{"iid": "x1", "text": SIGNED}, {"iid": "x2", "text": INTRO}]
    b = R.read_batch(pieces)
    assert b.prompt_sha == chunker.sha(X.G3H_PROMPT)
    (c,) = b.chunks
    text = R.read_text(b, c)
    assert str(R.EX_ROOT / b.answer_path(c["task_id"])) in text
    assert '"qid" and "customer"' in text and "return null" in text
    assert all(it["schema"] == [{"field": "customer", "type": "name",
                                 "describe": "the person who raised the case, as written"}] for it in c["items"])
    assert "x1" not in text and "x2" not in text


def test_templates_are_scored_apart_and_the_bar_is_unchanged(task):
    v1 = [("email", f"v1-{i}", i >= 10) for i in range(20)]                  # 10/20: the v1 e-mail template
    new = [(task.template_id, f"r2-{i}", True) for i in range(49)] + [(task.template_id, "r2-49", False)]
    rep = g3h.template_report(v1 + new)
    assert g3h.PASS_RATE == 0.98
    assert rep["quarantined"] == ["email"] and task.template_id not in rep["quarantined"]
    assert "r2-49" in rep["drop_rows"] and all(f"v1-{i}" in rep["drop_rows"] for i in range(20))


def test_files_on_disk_equal_the_rebuild(task):
    if not (R.ROOT / "TASKS.json").is_file():
        pytest.skip("redo2 author files not written yet")
    files, _m = R.author_files([task])
    assert R.check_on_disk(R.ROOT, files) == []
