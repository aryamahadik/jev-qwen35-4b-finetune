"""A25 (a) converter: od_gcp {id, model, probs} -> {id, choice} / {id, p_yes}; a top tie -> the first tied option in
the readout's fixed order. CPU only; synthetic rows only. The frozen scorer's CODE is compiled from its sha-checked
bytes (score_items only); no sealed suite or sealed preds are read."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import preds_to_gate as pg  # noqa: E402


def _w(p, rows):
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))


ROWS = [{"id": 1, "model": "m", "probs": {"yes": 0.7, "no": 0.3}},
        {"id": 2, "model": "m", "probs": {"opt a": 0.2, "opt b": 0.5, "opt c": 0.3}},
        {"id": 3, "model": "m", "probs": {"opt a": 0.2, "opt b": 0.4, "opt c": 0.4}},
        {"id": 4, "model": "m", "probs": {"yes": 0.5, "no": 0.5}},
        {"id": 5, "model": "m", "probs": {}},
        {"id": 6, "model": "m", "probs": {"no": 0.5, "yes": 0.5}},
        {"id": 7, "model": "m", "probs": {"B": 0.1, "A": 0.6, "C": 0.3}}]


def test_rules_and_record(tmp_path):
    src = tmp_path / "m.jsonl"
    _w(src, ROWS)
    rec = pg.convert(src)
    out = [json.loads(x) for x in (tmp_path / "m.gate.jsonl").read_text().splitlines()]
    assert out == [{"id": 1, "p_yes": 0.7, "choice": "yes"}, {"id": 2, "choice": "opt b"},
                   {"id": 3, "choice": "opt b"},                      # tie: first tied option in the probs' order
                   {"id": 4, "p_yes": 0.5, "choice": "yes"}, {"id": 6, "p_yes": 0.5, "choice": "no"},
                   {"id": 7, "choice": "A"}]
    assert rec["counts"] == {"rows": 7, "yes_no": 3, "choice": 3, "tie": 3, "no_probs": 1}
    assert rec["converter_sha256"] == pg.converter_sha() and pg.check(src) is None
    pg.convert(src)                                                   # deterministic: same bytes again
    assert json.loads((tmp_path / "m.gate.json").read_text())["out_sha256"] == rec["out_sha256"]
    src.write_text(src.read_text() + json.dumps({"id": 8, "model": "m", "probs": {"yes": 1.0, "no": 0.0}}) + "\n")
    assert "changed" in pg.check(src)


@pytest.mark.parametrize("bad", [[{"id": 1, "probs": {"a": 1}}, {"id": 1, "probs": {"a": 1}}],
                                 [{"id": 1, "model": "x", "probs": {"a": 1}}, {"id": 2, "model": "y", "probs": {"a": 1}}],
                                 [{"id": 1, "choice": "a"}]])
def test_refuses(tmp_path, bad):
    src = tmp_path / "b.jsonl"
    _w(src, bad)
    assert pg.main([str(src)]) == 2 and not (tmp_path / "b.gate.jsonl").exists()


def test_frozen_scorer_scores_converted_rows_as_the_readout(tmp_path):
    """The A15 scorer's own score_items on converted rows: tie -> first option, letter-like option text exact, yes/no
    via p_yes (0.5 = half), a choice item with yes/no options via choice, a dropped row = missing."""
    si = pg.frozen_scorer()["score_items"]
    suite = [{"id": "1", "qtype": "noul", "gold": 1}, {"id": "2", "qtype": "choice", "options": ["opt a", "opt b", "opt c"],
              "gold": "opt b"}, {"id": "3", "qtype": "choice", "options": ["opt a", "opt b", "opt c"], "gold": "opt b"},
             {"id": "4", "qtype": "noul", "gold": 0}, {"id": "5", "qtype": "noul", "gold": 0},
             {"id": "6", "qtype": "choice", "options": ["no", "yes"], "gold": "no"},
             {"id": "7", "qtype": "choice", "options": ["B", "A", "C"], "gold": "A"}]
    src = tmp_path / "m.jsonl"
    _w(src, ROWS)
    pg.convert(src)
    preds = {str(json.loads(x)["id"]): json.loads(x) for x in (tmp_path / "m.gate.jsonl").read_text().splitlines()}
    sc, ok, br = si(suite, preds)
    assert sc.tolist() == [1.0, 1.0, 1.0, 0.5, 0.0, 1.0, 1.0]
    assert ok.tolist() == [True, True, True, True, False, True, True]
    assert abs(br[0] - 0.09) < 1e-12 and abs(br[3] - 0.25) < 1e-12


def _tree(tmp_path, probs_rows, data_rows):
    pre, data = tmp_path / "pre/preds_dev", tmp_path / "data"
    pre.mkdir(parents=True)
    data.mkdir()
    _w(data / "dev.jsonl", data_rows)
    _w(pre / f"{pg.C1_PRE}.jsonl", probs_rows)
    return tmp_path / "pre", data, tmp_path / "proof.json"


DATA = [{"id": "a", "qtype": "noul", "gold": 1}, {"id": "b", "qtype": "choice", "options": ["x", "y"], "gold": "y"},
        {"id": "c", "qtype": "choice", "options": ["x", "y", "z"], "gold": "x"}]


def test_prove_passes_and_records(tmp_path, monkeypatch):
    probs = [{"id": "a", "model": "m", "probs": {"yes": 0.9, "no": 0.1}},
             {"id": "b", "model": "m", "probs": {"x": 0.3, "y": 0.7}},
             {"id": "c", "model": "m", "probs": {"x": 0.2, "y": 0.5, "z": 0.3}}]
    root, data, out = _tree(tmp_path, probs, DATA)
    assert pg.prove(root, data, out) == 0
    rec = json.loads(out.read_text())
    assert rec["pass"] and rec["by_split"]["dev"]["_pre"]["acc_dev"] == pytest.approx(200 / 3, abs=1e-3)
    monkeypatch.setattr(pg, "PROOF", out)
    assert pg.proof_problem(out) is None
    rec["converter_sha256"] = "0" * 64
    out.write_text(json.dumps(rec))
    assert "another converter" in pg.proof_problem(out)


def test_prove_fails_on_a_tie_gate_dev_scores_wrong(tmp_path):
    """gate_dev.score counts a top tie wrong; the converter breaks it by the fixed order (A25 a). On C1's dev reads
    there are 0 ties (the proof counts them); a tie whose first option is gold would show as a mismatch here."""
    probs = [{"id": "a", "model": "m", "probs": {"yes": 0.9, "no": 0.1}},
             {"id": "b", "model": "m", "probs": {"x": 0.3, "y": 0.7}},
             {"id": "c", "model": "m", "probs": {"x": 0.4, "y": 0.4, "z": 0.2}}]
    root, data, out = _tree(tmp_path, probs, DATA)
    assert pg.prove(root, data, out) == 1
    x = json.loads(out.read_text())["by_split"]["dev"]["_pre"]
    assert x["row_mismatches"] == 1 and x["ties"] == 1
