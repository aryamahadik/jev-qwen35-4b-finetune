"""In-memory tests for haiku/redo3/build_redo3.py (nothing is written; Haiku is never run).

  gaps      the gaps equal STAGE_A3_REPORT.json and pools_v2; each piece is asked ceil(1.5 x gap); at most 12 tasks
  rebuild   build() reproduces every non-answer file on disk byte for byte (skipped when pools_v2 changed)
  contract  every task file names its exact answer file under haiku/redo3/answers/ and a literal JSON example that
            parses; items match the chunk; label-blind prompts hold no T01 label word; no never-open path
  checks    the literal examples and a plan-shaped good answer pass the family's own checks (check_skin, check_lexicon,
            check_freeform); the G3-H prompt is the unchanged extract.G3H_PROMPT
Run (from lean/):  ../.venv/bin/python -B -m pytest -q -p no:cacheprovider c2_build/families/T01/haiku/redo3
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[3]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit.paths import never_open  # noqa: E402
from families.T01 import haiku_author as HA  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

_spec = importlib.util.spec_from_file_location("t01_build_redo3", HERE / "build_redo3.py")
B3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B3)


def _baseline():
    """The freeze this round was authored against: pools_v2_prev/ once the re-freeze that folded redo3 in moved it aside,
    else pools_v2/ while it still carries the input shas of TASKS.json. None when neither does."""
    man = json.loads((HERE / "TASKS.json").read_text(encoding="utf-8"))
    want = {f: s for f, s in man["inputs_sha256"].items() if f != "STAGE_A3_REPORT.json"}
    for d in (B3.T01_DIR / "pools_v2_prev", B3.T01_DIR / "pools_v2"):
        if d.is_dir() and all((d / f).is_file() and B3._sha(d / f) == s for f, s in want.items()):
            return d
    return None


_BASE = _baseline()
if _BASE is not None:
    B3.POOLS_V2 = _BASE          # build() re-reads the gaps from the freeze it was written against, not the current one


@pytest.fixture(scope="module")
def res():
    if _BASE is None:
        pytest.skip("the pools_v2 freeze that redo3 was built against is gone (no pools_v2_prev/ with its input shas)")
    try:
        return B3.build()
    except SystemExit as e:      # check_gaps re-reads the T01 shortfalls from STAGE_A3_REPORT.json and the baseline freeze
        pytest.skip(f"the gaps this round was planned for can no longer be derived: {str(e)[:120]}")


def test_gaps_and_ask(res):
    g = res["gaps"]
    assert g["skins"] == B3.SKIN_GAP and sum(B3.SKIN_GAP.values()) == 30
    assert g["windows"] == {"win.later_anchor": 4, "win.wait_after": 3} and g["documents"] == 2
    for x in list(B3.SKIN_GAP.values()) + list(B3.WINDOW_GAP.values()) + [B3.DOC_GAP]:
        assert B3.ask(x) * 2 >= 3 * x and B3.ask(x) <= x * 2        # at least 50% more, never double
    assert [B3.ask(x) for x in (4, 3, 2, 1, 5, 6)] == [6, 5, 3, 2, 8, 9]
    assert len(res["tasks"]) <= 12


def test_counts(res):
    items = {}
    for t in res["tasks"]:
        items[t["label"]] = items.get(t["label"], 0) + t["n_items"]
    assert items == {"skins": sum(B3.ask(g) for g in B3.SKIN_GAP.values()), "windows": 11, "freeform_backup": 3,
                     "g3h_pending": 2}
    assert items["skins"] == 48
    assert all(t["n_items"] <= 50 for t in res["tasks"])


def test_rebuild_matches_disk(res):
    man = json.loads((HERE / "TASKS.json").read_text(encoding="utf-8"))
    now = {f: B3._sha(B3.POOLS_V2 / f) for f in man["inputs_sha256"] if f != "STAGE_A3_REPORT.json"}
    if any(man["inputs_sha256"][f] != s for f, s in now.items()) or \
            man["inputs_sha256"]["STAGE_A3_REPORT.json"] != B3._sha(B3.A3_REPORT):
        pytest.skip("pools_v2 or STAGE_A3_REPORT.json changed since redo3 was built")
    for rel, text in res["files"].items():
        assert (HERE / rel).read_text(encoding="utf-8") == text, rel
    assert [t["task_id"] for t in man["tasks"]] == [t["task_id"] for t in res["tasks"]]


def test_task_files_are_self_contained(res):
    for t in res["tasks"]:
        txt = res["files"][f"tasks/{t['task_id']}.txt"]
        assert f"ANSWER FILE (write exactly this path) : {t['answer_file']}" in txt
        assert t["answer_file"].startswith(str(HERE / "answers") + "/")
        assert never_open(t["task_file"]) is None and never_open(t["answer_file"]) is None
        assert t["audit_allowed_read"] == [t["task_file"]] and t["audit_allowed_write"] == [t["answer_file"]]
        i = txt.index("=== ITEMS")
        items = [json.loads(x) for x in txt[i:].splitlines()[1:] if x.strip()]
        assert len(items) == t["n_items"] and len({x["qid"] for x in items}) == len(items)
        j = txt.index("Literal example")
        a = txt.index("[", j)
        b = txt.index("\n]", a) + 2
        assert len(json.loads(txt[a:b])) == 2
        assert "=== INSTRUCTIONS" in txt and "=== ANSWER CONTRACT" in txt
        low = txt.lower()
        assert "ohs" not in low and "sealed_nd" not in low and "preread" not in low and "claude-501" not in low


def test_label_blind_prompts(res):
    for label, b, _plan in res["groups"]:
        if b.kind in ("author_skin", "author_freeform"):
            low = b.prompt.lower()
            for w in P.T01.LABEL_WORDS:
                assert not re.search(r"(?<![a-z0-9])" + re.escape(w.lower()) + r"(?![a-z0-9])", low), (label, w)
            for it in (x for c in b.chunks for x in c["items"]):
                blob = json.dumps(it).lower()
                for q in HA.QSTRINGS:
                    assert q.lower() not in blob


def test_g3h_prompt_unchanged(res):
    b = [g for g in res["groups"] if g[0] == "g3h_pending"][0][1]
    assert b.prompt == E.G3H_PROMPT
    assert b.prompt_sha == "f2e2e80b3c130ecc2bbcf4fafb591293ee2dcc2e8b11f45c5197e3cbe5499ac6"   # as in haiku/extract


def test_examples_pass_family_checks():
    for ex, reg, esc in ((B3.SKIN_EXAMPLE[0], "memo", "text"), (B3.SKIN_EXAMPLE[1], "yaml", "yaml")):
        sk, v = HA.check_skin(f"t01r3.skin.{reg}.999", ex["text"], {"register": reg, "escape": esc, "held_out": False},
                              "t", "p", set())
        assert not v, v
    for ex, sem, slots in ((B3.WINDOW_EXAMPLE[0], "win.later_anchor", {"N": "count"}),
                           (B3.WINDOW_EXAMPLE[1], "win.wait_after", {"W": "count"})):
        _o, v = HA.check_lexicon("x", ex["text"], {"sem": sem, "kind": "window", "slots": slots}, "t", "p", set())
        assert not v, v
    facts = {"PERSON": "Lena Hartmann", "REF": "ZZ-0000", "TOPIC": "garden fence repair"}
    for ex, reg in zip(B3.FREEFORM_EXAMPLE, ("email", "chat")):
        _s, v = HA.check_freeform(f"t01r3.free.{reg}.999", ex["text"], {"register": reg, "facts": facts}, "t", "p", set())
        assert not v, v


def test_plan_meta_drives_the_checks(res):
    plans = {label: (b, plan) for label, b, plan in res["groups"]}
    _b, pf = plans["freeform_backup"]
    for iid, m in pf.items():
        f = m["facts"]
        assert f["TOPIC"] in B3.CLEAN_TOPICS
        txt = f"Internal memo. {f['PERSON']} forwards file {f['REF']} about the {f['TOPIC']} to the desk."
        _s, v = HA.check_freeform(iid, txt, m, "t", "p", set())
        assert not v, v
    _b, ps = plans["skins"]
    assert {m["register"] for m in ps.values()} == set(B3.TRAIN + B3.HELD)
    assert all(iid.split(".")[-1].isdigit() and int(iid.split(".")[-1]) >= (28 if m["held_out"] else 56)
               for iid, m in ps.items())
