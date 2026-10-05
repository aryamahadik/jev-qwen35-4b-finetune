"""clean_sets.py + check_overlap_di.py on CPU with tiny fake source records (no network)."""
import json

import pytest

import check_overlap_di as O
import clean_sets as C
from common import write_jsonl

MMLU = [{"question": "What is 2 + 2 here?", "subject": "elementary_mathematics", "choices": ["3", "4", "5", "6"], "answer": 1},
        {"question": "Capital of France?", "subject": "geography", "choices": ["Paris", "Rome", "Oslo", "Bern"], "answer": 0},
        {"question": "Dup options?", "subject": "geography", "choices": ["a", "a", "b", "c"], "answer": 0}]
ARC = [{"id": "Q1", "question": "Which is a metal?", "choices": {"text": ["iron", "wood", "glass"], "label": ["1", "2", "3"]},
        "answerKey": "1"}]
SCI = [{"uuid": f"u{i}", "question": f"Science question number {i} about energy levels in atoms?",
        "options": [f"opt{i}_{k}" for k in range(10)], "answer": f"opt{i}_3", "discipline": "Science",
        "field": "Mathematics" if i % 2 else "Physics", "subfield": "x", "difficulty": "hard"} for i in range(6)]
SCI.append({**SCI[0], "uuid": "easy", "difficulty": "easy"})


def test_make_row_validation():
    assert C.make_row("s", "1", "Q?", ["a", "a"], 0, "src", "math", {}) is None  # duplicate options
    assert C.make_row("s", "1", "", ["a", "b"], 0, "src", "math", {}) is None
    assert C.make_row("s", "1", "Q?", ["a", "b"], 5, "src", "math", {}) is None
    r = C.make_row("s", "1", " Q? ", [" a ", "b"], 1, "src", "math", {})
    assert r["gold"] == "b" and r["options"] == ["a", "b"] and r["split"] in ("dev_fit", "dev_confirm")
    assert r["instructions"] == C.INSTR and r["qtype"] == "choice"


def test_converters():
    rows = [r for r in C.conv_mmlu(MMLU, "validation") if r]
    assert [r["think_type"] for r in rows] == ["math", "knowledge"] and rows[0]["gold"] == "4"
    arc = C.conv_arc(ARC, "ARC-Challenge", "train")
    assert arc[0]["gold"] == "iron" and arc[0]["id"] == "k_arc:ARC-Challenge:Q1"
    sci = C.conv_sci(SCI)
    assert len(sci) == 6 and all(len(r["options"]) == 4 for r in sci)  # 'easy' dropped; 4 options each
    assert all(r["gold"] == f"opt{r['id'].split(':u')[1]}_3" for r in sci)
    assert {r["think_type"] for r in sci} == {"math", "science"}
    assert C.conv_sci(SCI) == sci  # deterministic


def test_gsm8k_recipe():
    opts, pos = C.gsm8k_options(18.0, "train:1")
    assert len(opts) == 4 and len(set(opts)) == 4 and opts[pos] == "18"
    assert C.gsm8k_options(18.0, "train:1") == (opts, pos)
    positions = {C.gsm8k_options(10.0, f"train:{i}")[1] for i in range(40)}
    assert positions == {0, 1, 2, 3}  # gold position not fixed / not centred
    rows = C.conv_gsm8k([{"question": "Q one?", "answer": "work\n#### 1,200"}])
    assert rows[0]["gold"] == "1200"


def test_fetch_refuses_test_split():
    with pytest.raises(SystemExit):
        C.fetch("cais/mmlu", "all/test-00000-of-00001.parquet")


def test_build_overlap_finalize(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "OUT", tmp_path)
    monkeypatch.setattr(C, "fetch", lambda repo, fn, allow_test=False: (fn, "rev"))
    fake = {"all/validation-00000-of-00001.parquet": MMLU, "all/dev-00000-of-00001.parquet": [],
            "SuperGPQA-all.jsonl": SCI}
    monkeypatch.setattr(C, "records", lambda p: fake.get(p, ARC if "ARC-Challenge/train" in p else []))
    C.main(["build"])
    man = json.loads((tmp_path / "build_manifest.json").read_text())
    assert man["sets"]["k_mmlu"]["rows"] == 2 and man["sets"]["k_mmlu"]["invalid_or_dup"] == 1
    with pytest.raises(SystemExit):
        C.main(["finalize"])  # no overlap check yet
    held = tmp_path / "held"
    held.mkdir()
    long_q = SCI[2]["question"] + " " + " ".join(SCI[2]["options"])
    write_jsonl(held / "di.jsonl", [{"state": {"text": long_q}, "_evaluation": {"dataset": "X"}},
                                    {"state": "Capital of France?", "questions": {"q": {"criteria": {"A": "Paris"}}}}])
    res = O.run(tmp_path, [("di", held)], n=8, boiler=20)
    assert res["drop_ids"]["k_sci"] == ["k_sci:u2"] and res["counts"]["k_sci"]["dropped"] == 1
    assert res["drop_ids"]["k_mmlu"] == []  # 3 words < exact minimum; no shared 8-gram
    rep = (tmp_path / "overlap_report.json").read_text()
    assert "energy levels" not in rep and "drop_ids" not in rep  # counts only
    C.main(["finalize"])
    fm = json.loads((tmp_path / "manifest.json").read_text())
    assert fm["sets"]["k_sci"]["rows"] == 5 and fm["sets"]["k_sci"]["dropped_overlap"] == 1
    assert fm["sets"]["k_sci"]["dev_fit"] + fm["sets"]["k_sci"]["dev_confirm"] == 5
    (tmp_path / "k_arc.candidates.jsonl").write_text("")  # candidates changed after the check
    with pytest.raises(SystemExit):
        C.main(["finalize"])


def test_exact_match_rule(tmp_path):
    write_jsonl(tmp_path / "k_x.candidates.jsonl",
                [{"id": "k_x:1", "state": "Which planet is known as the red planet today?", "options": ["Mars", "Venus"]}])
    write_jsonl(tmp_path / "ref.jsonl", [{"question": "Which planet is known as the red planet today?", "x": 1}])
    res = O.run(tmp_path, [("pub", tmp_path / "ref.jsonl")], n=13)
    assert res["counts"]["k_x"]["per_ref"]["pub"] == {"ngram": 0, "exact": 1} and res["drop_ids"]["k_x"] == ["k_x:1"]
