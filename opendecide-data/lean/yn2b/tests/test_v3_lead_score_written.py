"""The F5 decide2 on the WRITTEN rows (data/v14_parts/yn2b_raw/[dev/]gen3_lead_score.jsonl): SPEC 8.1 agreement,
8.3 structure under decide2 alone, format parity, and decide2's independence from the generator. Read-only."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from v3f5_helpers import v3

pytestmark = pytest.mark.skipif(not (v3.RAW / f"{v3.KEY}.jsonl").exists(), reason="F5 raw rows not written")


@pytest.fixture(scope="module")
def parts():
    out = {}
    for split in ("train", "dev"):
        rows = v3.load_rows(split)
        out[split] = (rows, v3.load_rels(split), v3.agreement(rows))
    return out


def test_every_row_parses(parts):
    for split, (rows, _, ag) in parts.items():
        errs = [d for d in ag["disagreements"] if d["error"]]
        assert not errs, f"{split}: {errs[:5]}"


def test_dev_agrees_100(parts):
    rows, _, ag = parts["dev"]
    assert ag["agree"] == ag["rows"] == len(rows)


def test_train_disagreements_are_only_the_gate_score_reading(parts):
    """Known open item (reported to the generator's owner): 'N of M gates passed' is not defined by the rubric text.
    decide2 counts every gate passed; the generator counts gates passed in order up to the first failure. Every train
    disagreement must be of exactly that kind (the answer flips to the gold under the other reading) and nothing else."""
    rows, _, ag = parts["train"]
    by = {r["rid"]: r for r in rows}
    for d in ag["disagreements"]:
        r = by[d["rid"]]
        o = v3.solve(r)
        assert o["q"] == "judge" and o["result"].archetype == "gated", d
        assert v3.decide2_row(r, {"gate_score": "consecutive"}) == r["gold"], d
    assert ag["rows"] - ag["agree"] <= 7          # the count at the time of writing; a fixed generator gives 0


def test_structure_under_decide2(parts):
    for split, (rows, rels, ag) in parts.items():
        st = v3.structure_under_decide2(rows, rels, ag["answers"])
        assert not st["equiv_changed"] and not st["inv_changed"] and not st["unknown_rel"], split
        assert not st["format_fact_mismatch"], (split, st["format_fact_mismatch"][:3])
        dis_latents = {d["rid"].rsplit("-", 1)[0] for d in ag["disagreements"]}
        assert {x.rsplit("-", 1)[0] for x in st["contrast_not_flipped"]} <= dis_latents, split


def test_cards_match_questions(parts):
    for split, (rows, _, _) in parts.items():
        assert v3.card_report(rows)["card_question_mismatch"] == [], split


def test_mv_core_verify_labels_api(parts):
    import mv_core
    rows, _, _ = parts["dev"]
    assert mv_core.verify_labels(rows, v3.decide2_row_safe)["ok"]


def test_decide2_is_deterministic(parts):
    rows, _, ag = parts["train"]
    for r in rows[:200]:
        try:
            a = v3.decide2_row(r)
        except v3.ParseError:
            a = None
        assert a == ag["answers"][r["rid"]]


def test_independent_of_the_generator():
    src = Path(v3.__file__).read_text()
    assert not re.search(r"^\s*(import|from)\s+gen3_lead_score\b", src, re.M)
    assert "gen3_lead_score.py" not in src.replace("`gen3_lead_score.py`", "")   # only named in the docstring
    code = src.split('"""', 2)[2]                                                  # after the module docstring
    for token in ('["gold"]', "['gold']", '["meta"]'):
        # gold/meta are read only by the report helpers, never by solve()/decide2_row()
        body = code.split("def solve(")[1].split("\ndef ", 1)[0]
        assert token not in body, token


def test_write_agreement_goes_to_the_given_path_and_the_redirected_manifest(tmp_path, _tmp_manifest):
    import json
    out = tmp_path / "agree.json"
    rep = v3.write_agreement(out)
    assert json.loads(out.read_text())["parts"]["dev"]["disagree"] == 0 == rep["parts"]["dev"]["disagree"]
    recs = [json.loads(x) for x in _tmp_manifest.read_text().splitlines()]
    assert len(recs) == 1 and recs[0]["part"] == "decide2_agreement" and recs[0]["path"].endswith("agree.json")
    for d in rep["parts"]["train"]["disagreements"]:
        assert d["diagnosis"]["reading"][0] == "gate_score=consecutive"
