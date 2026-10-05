"""eval_think.py: the A17 B1/B2 rules at their exact boundaries, on synthetic records (aggregates only)."""
import json

import pytest

import eval_think as E
from common import sha256_file, write_jsonl


def clean_dir(tmp_path, n=20, math=20, other=0):
    rows = [{"id": f"m{i}", "qtype": "choice", "state": "s", "instructions": "i", "options": ["a", "b"], "gold": "a",
             "set": "k_x" if i % 2 else "k_y", "think_type": "math", "split": "dev_confirm"} for i in range(math)]
    rows += [{"id": f"o{i}", "qtype": "choice", "state": "s", "instructions": "i", "options": ["a", "b"], "gold": "a",
              "set": "k_x", "think_type": "science", "split": "dev_confirm"} for i in range(other)]
    rows.append({**rows[0], "id": "fit0", "split": "dev_fit"})
    write_jsonl(tmp_path / "k_all.jsonl", rows)
    (tmp_path / "manifest.json").write_text(json.dumps({"sets": {"k_all": {"sha256": sha256_file(tmp_path / "k_all.jsonl")}}}))
    return tmp_path


def recs(ids, n_right, wall=0.5, gs=1, tokens=100, **kw):
    return {i: {"id": i, "final_key": "a" if k < n_right else "b", "wall_s": wall, "group_size": gs,
                "think_tokens": tokens, "think_tokens_sum": tokens, **kw} for k, i in enumerate(ids)}


def test_math_rule_boundaries(tmp_path):
    rows = E.load_rows(clean_dir(tmp_path), "dev_confirm", "math")
    ids = sorted(rows)
    assert len(ids) == 20 and "fit0" not in rows
    full = recs(ids, 20)
    assert E.rule_math(rows, recs(ids, 17), full)["pass"] is True  # 17/20 = exactly 85% of 20/20
    assert E.rule_math(rows, recs(ids, 16), full)["pass"] is False
    r = E.rule_math(rows, recs(ids, 20, wall=1.0), full)
    assert r["pass"] and r["median_wall_s"] == 1.0  # median exactly 1 s passes
    assert E.rule_math(rows, recs(ids, 20, wall=1.01), full)["latency_pass"] is False
    assert E.rule_math(rows, recs(ids, 20, gs=8), full)["pass"] is False  # not measured one request at a time
    assert E.rule_math(rows, recs(ids, 20), recs(ids, 0))["pass"] is False  # full thinking scores 0: undefined
    part = dict(list(recs(ids, 20).items())[:-1])
    assert E.rule_math(rows, part, full)["status"] == "incomplete"
    assert E.rule_math(rows, recs(ids, 20, policy="full_think"), full)["pass"] is False  # reference as think path
    assert E.rule_math(rows, recs(ids, 20), recs(ids, 20, policy="capped_think"))["pass"] is False


def test_fp8_rule_boundaries(tmp_path):
    rows = E.load_rows(clean_dir(tmp_path, math=100), "dev_confirm")
    ids = sorted(rows)
    bf = recs(ids, 90)
    assert E.rule_fp8(rows, recs(ids, 89), bf)["pass"] is True  # loss exactly 1.0 pt
    assert E.rule_fp8(rows, recs(ids, 88), bf)["pass"] is False
    assert E.rule_fp8(rows, None, bf)["pass"] is None  # FP8 not shipped -> n/a


def test_b2_rule_boundaries(tmp_path):
    rows = E.load_rows(clean_dir(tmp_path, math=50), "dev_confirm")
    ids = sorted(rows)
    b1 = recs(ids, 50, tokens=400)
    assert E.rule_b2(rows, b1, recs(ids, 49, tokens=300))["pass"] is True  # -25% tokens, 98% accuracy
    assert E.rule_b2(rows, b1, recs(ids, 48, tokens=300))["acc_pass"] is False
    assert E.rule_b2(rows, b1, recs(ids, 50, tokens=301))["tokens_pass"] is False


def test_cli_b1_and_b2(tmp_path, capsys):
    (tmp_path / "c").mkdir()
    d = clean_dir(tmp_path / "c")
    ids = sorted(E.load_rows(d, "dev_confirm", "math"))
    for name, r in (("t", recs(ids, 18)), ("f", recs(ids, 20)), ("b1", recs(ids, 18, tokens=400)),
                    ("b2", recs(ids, 18, tokens=200))):
        write_jsonl(tmp_path / f"{name}.jsonl", r.values())
    summ = tmp_path / "summary.json"
    summ.write_text(json.dumps({"b1_checks": {"fast_p50_ms": 31.5}}))
    out = tmp_path / "b1.json"
    E.main(["b1", "--clean", str(d), "--think", str(tmp_path / "t.jsonl"), "--full", str(tmp_path / "f.jsonl"),
            "--b1-summary", str(summ), "--out", str(out)])
    rep = json.loads(out.read_text())
    assert rep["pass"] is True and rep["ship_fp8"] is False and rep["fast"]["p50_ms"] == 31.5
    for name, r in (("p16", recs(ids, 20)), ("p8", recs(ids, 18))):  # FP8 loses 10 pts: FP8 not shipped, B1 stands
        write_jsonl(tmp_path / f"{name}.jsonl", r.values())
    E.main(["b1", "--clean", str(d), "--think", str(tmp_path / "t.jsonl"), "--full", str(tmp_path / "f.jsonl"),
            "--fp8", str(tmp_path / "p8.jsonl"), "--bf16", str(tmp_path / "p16.jsonl"), "--fast-p50-ms", "31.5",
            "--out", str(out)])
    rep = json.loads(out.read_text())
    assert rep["fp8"]["pass"] is False and rep["pass"] is True and rep["ship_fp8"] is False
    assert len(rep["readings"]) >= 7 and '"m0"' not in out.read_text()  # aggregates only, no per-item ids
    E.main(["b2", "--clean", str(d), "--b1", str(tmp_path / "b1.jsonl"), "--b2", str(tmp_path / "b2.jsonl")])
    assert '"pass": true' in capsys.readouterr().out
    with pytest.raises(SystemExit):
        E.main(["b1", "--clean", str(d), "--think", str(tmp_path / "t.jsonl"), "--full", str(tmp_path / "f.jsonl"),
                "--fp8", str(tmp_path / "t.jsonl")])
