"""CPU tests of od_engine (fake model: random 1-layer Qwen3 + the real C1 tokenizer). Synthetic questions only, no Index
item is read here (the 50-request smoke run through the harness is separate, see README.md).

  PYTHONPATH=bench/external_quarantine/decision_index/repo:bench/decision_index \
      opendecide-data/.venv/bin/python -m pytest -q bench/decision_index/test_od_engine.py
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
JEV = HERE.parents[1]
sys.path.insert(0, str(JEV / "bench/external_quarantine/decision_index/repo"))
sys.path.insert(0, str(HERE))
LEAN = JEV / "opendecide-data/lean"
ADAPTER = JEV / "backups/modal_models/q35_4b_main500k"

from decision_index.engines import Unsupported, validate  # noqa: E402

import od_engine  # noqa: E402

LETTERS = [chr(65 + i) for i in range(26)]


def q_choice(n, positional=True, desc=True, ins="Pick the best option."):
    keys = LETTERS[:n] if (positional and n <= 26) else ([f"option_{i}" for i in range(n)] if positional
                                                          else [f"label{i}" for i in range(n)])
    return {"type": "choice", "instructions": ins,
            "criteria": {k: (f"synthetic option number {i}" if desc else None) for i, k in enumerate(keys)}}


def q_yes_no(order=("yes", "no"), desc=True):
    d = {"yes": "the synthetic condition holds", "no": "the synthetic condition does not hold"}
    return {"type": "choice", "instructions": "Does the synthetic condition hold?",
            "criteria": {k: (d[k] if desc else None) for k in order}}


@pytest.fixture(scope="module")
def eng():
    return od_engine.ODEngine(adapter=str(ADAPTER), lean=str(LEAN), fake=True, base="Qwen/Qwen3.5-4B",
                              revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")


def test_layout_from_train_meta(eng):
    assert eng.dio.LAYOUT == "schema_branch_mark" and eng.dio.STYLE == "cygnet"
    assert eng.limit == 16384


def test_mapping_rules():
    st = od_engine.state_text({"a": 1})
    r, i = od_engine.build_row(st, q_choice(4), "q")
    assert i["kind"] == "choice" and i["mode"] == "plain" and r["options"][0] == "synthetic option number 0"
    r, i = od_engine.build_row(st, q_choice(3, positional=False), "q")
    assert i["mode"] == "named_card" and r["options"] == ["label0", "label1", "label2"] and "- label1: synthetic" in r["card"]
    r, i = od_engine.build_row(st, q_choice(3, positional=False, desc=False), "q")
    assert i["mode"] == "plain" and "card" not in r
    r, i = od_engine.build_row(st, q_yes_no(("no", "yes")), "q")
    assert r["qtype"] == "noul" and i["keys"] == ["yes", "no"] and r["card"].startswith("- Yes: ")
    r, i = od_engine.build_row(st, {"type": "choice", "instructions": "x", "criteria": {"True": None, "False": None}}, "q")
    assert r["qtype"] == "noul" and i["keys"] == ["True", "False"] and "card" not in r
    dup = {"type": "choice", "instructions": "x", "criteria": {"A": "same", "B": "same", "C": "other"}}
    r, i = od_engine.build_row(st, dup, "q")
    assert i["mode"] == "key_desc_dedup" and len(set(r["options"])) == 3
    multi = {"type": "choice", "instructions": "x", "criteria": {"k1": "line one\nline two", "k2": "plain"}}
    r, i = od_engine.build_row(st, multi, "q")
    assert r["options"][0] == "k1: line one\nline two" and r["options"][1] == "k2" and "- k2: plain" in r["card"]
    with pytest.raises(Unsupported):
        od_engine.build_row(st, q_choice(256), "q")
    assert od_engine.state_text({}) == "(empty)" and od_engine.state_text("") == "(empty)"


def test_prompt_shows_definitions(eng):
    r, _ = od_engine.build_row("some state", q_choice(3, positional=False), "q")
    p = eng.ro.prompt(r)
    assert "A. label0: synthetic option number 0" in p and "Options: A. label0; B. label1; C. label2" in p
    rev = eng.ro.prompt(r, [2, 1, 0])
    assert "A. label2: synthetic option number 2" in rev


def test_equals_decoder_io_predict(eng):
    """The engine's read == decoder_io.predict(tta_choice=True, tta_noul=False) on the same rows (shipped A5 readout)."""
    qs = [q_choice(4), q_choice(30), q_choice(5, positional=False), q_yes_no(), q_yes_no(("no", "yes"), desc=False),
          q_choice(2, positional=False, desc=False)]
    rows = [od_engine.build_row("A synthetic state with a few words.", q, f"r{i}")[0] for i, q in enumerate(qs)]
    ntok = [eng._ntok(r) for r in rows]
    mine = eng.read_rows(rows, ntok)
    ref = eng.dio.predict(eng.model, eng.tok, rows, batch_size=16, dev="cpu", tta_choice=True, tta_noul=False)
    diff = max(abs(mine[i][k] - ref[i][k]) for i in range(len(rows)) for k in ref[i])
    assert diff < 1e-6, diff
    one = []  # batch 1 (as run_ejs5 2view) agrees too, up to float noise
    for r in rows:
        one += eng.read_rows([r], [eng._ntok(r)])
    assert max(abs(one[i][k] - ref[i][k]) for i in range(len(rows)) for k in ref[i]) < 1e-4


def test_harness_contract(eng):
    questions = {"a": q_choice(4), "b": q_yes_no(("no", "yes")), "c": q_choice(40), "d": q_choice(3, positional=False)}
    resp, raw = eng({"k": "v"}, questions)
    validate(questions, resp)
    assert set(resp["answers"]["b"]["probabilities"]) == {"yes", "no"}
    assert raw["a"]["reads"] == 2 and raw["b"]["reads"] == 1
    for k, a in resp["answers"].items():
        p = a["probabilities"]
        assert abs(sum(p.values()) - 1) < 1e-6 and a["choice"] == max(p, key=p.get)


def test_refuses_over_limit(eng):
    old = eng.limit
    eng.limit = 50
    try:
        with pytest.raises(Unsupported):
            eng("word " * 200, {"q": q_choice(3)})
    finally:
        eng.limit = old
