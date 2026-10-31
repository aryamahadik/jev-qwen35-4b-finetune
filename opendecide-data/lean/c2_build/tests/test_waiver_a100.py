"""Tests for the A100 waiver of pre-gate (b) (PREREG Record A100): waiver_a100.py and its use in gate_c2.py. In memory plus tiny tmp files.
No OHS / sealed path is opened. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_waiver_a100.py"""
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_c2 as gc  # noqa: E402
import gate_dev as g  # noqa: E402
import waiver_a100 as wv  # noqa: E402
from test_gate_c2 import D2, LAT, dev_json, mixdev_with_untrained, rows_with, t37, write_mix_manifest  # noqa: E402,F401

QUOTE = ("I waive pre-gate (b), the transfer rule, after seeing the result. Put the chosen C2 candidate into the one OHS-4 look "
         "together with C1, and disclose this override in the report.")


@pytest.fixture
def tmp(tmp_path):
    assert gc.c2io.refusal(tmp_path) is None
    return tmp_path


def prereg_text(quote=QUOTE, head="**Record A100 (OWNER words, verbatim; an OWNER OVERRIDE): "):
    body = textwrap.fill(f'{head}"{quote}"** answering the neutral choice.', 118)
    return "> **Record A99 (orchestrator).** earlier.\n\n" + "".join(f"> {ln}\n" for ln in body.splitlines())


def record(**over):
    r = {"record": "A100", "quote": QUOTE, "waives": ["b_transfer"], "waived_rule": "b"}
    r.update(over)
    return r


@pytest.fixture
def world(tmp):
    (tmp / "c2_build/train").mkdir(parents=True)
    (tmp / wv.OWNER_GO_C2).write_text(f'- 18 Oct 2026 ~19:20 UTC, Record A100 (OWNER OVERRIDE): "{QUOTE}"\n')
    (tmp / wv.PREREG_FINAL_MD).write_text(prereg_text())
    (tmp / wv.RECORD).write_text(json.dumps(record()))
    return tmp


# ---- the record -------------------------------------------------------------------------------------------------------
def test_a100_constant_is_the_full_sentence_and_matches_the_real_files():
    assert wv.A100_QUOTE == QUOTE
    lean = C2B.parent
    if not ((lean / wv.OWNER_GO_C2).exists() and (lean / wv.PREREG_FINAL_MD).exists()):
        pytest.skip("real OWNER_GO_C2.txt / PREREG_FINAL.md not present")
    assert QUOTE in wv._norm((lean / wv.OWNER_GO_C2).read_text()) and wv._prereg_has_quote(lean)


def test_a100_valid_record_is_active_and_no_record_is_silent(world):
    assert wv.waiver_active(world) == (True, "")
    (world / wv.RECORD).unlink()
    assert wv.waiver_active(world) == (False, "")


@pytest.mark.parametrize("quote", ["I waive pre-gate (b)", "I waive pre-gate (b), the transfer rule, after seeing the result.", QUOTE[:-25],
                                   QUOTE[15:], QUOTE + " Thanks.", QUOTE.replace("waive", "keep"), QUOTE.lower(), ""])
def test_a100_a_truncated_prefix_or_edited_quote_is_not_a_waiver(world, quote):
    (world / wv.OWNER_GO_C2).write_text((world / wv.OWNER_GO_C2).read_text() + quote + "\n")     # present in the owner file as a substring
    (world / wv.RECORD).write_text(json.dumps(record(quote=quote)))
    ok, why = wv.waiver_active(world)
    assert not ok and "not the full verbatim A100 sentence" in why


@pytest.mark.parametrize("how", ["owner_missing", "owner_prefix_only", "prereg_missing", "prereg_prefix_only", "prereg_other_record",
                                 "prereg_quote_edited", "bad_json", "other_record_id", "waives_a", "waives_b_and_d9", "waives_none",
                                 "waived_rule_a", "no_quote_key"])
def test_a100_a_quote_missing_from_either_file_or_another_scope_is_not_a_waiver(world, how):
    p = world / wv.RECORD
    if how == "owner_missing":
        (world / wv.OWNER_GO_C2).write_text("- nothing about A100\n")
    elif how == "owner_prefix_only":
        (world / wv.OWNER_GO_C2).write_text(f'- Record A100: "{QUOTE[:-25]}"\n')
    elif how == "prereg_missing":
        (world / wv.PREREG_FINAL_MD).unlink()
    elif how == "prereg_prefix_only":
        (world / wv.PREREG_FINAL_MD).write_text(prereg_text(quote=QUOTE[:-25]))
    elif how == "prereg_other_record":
        (world / wv.PREREG_FINAL_MD).write_text(prereg_text(head="**Record A93 (orchestrator): "))
    elif how == "prereg_quote_edited":
        (world / wv.PREREG_FINAL_MD).write_text(prereg_text(quote=QUOTE.replace("waive", "keep")))
    elif how == "bad_json":
        p.write_text("{nope")
    elif how == "other_record_id":
        p.write_text(json.dumps(record(record="A99")))
    elif how == "waives_a":
        p.write_text(json.dumps(record(waives=["a_learning"])))
    elif how == "waives_b_and_d9":
        p.write_text(json.dumps(record(waives=["b_transfer", "c7_D9"])))
    elif how == "waives_none":
        p.write_text(json.dumps(record(waives=[])))
    elif how == "waived_rule_a":
        p.write_text(json.dumps(record(waived_rule="a")))
    elif how == "no_quote_key":
        r = record(); r.pop("quote"); p.write_text(json.dumps(r))
    ok, why = wv.waiver_active(world)
    assert not ok and why


# ---- gate_c2.evaluate / decide ------------------------------------------------------------------------------------------
def inputs(tr_ok=0.50, mix_ok=0.85):
    mix = rows_with(2550, mix_ok, 0.70, seed=1)
    tr = rows_with(1200, tr_ok, 0.60, seed=2, family="T36")          # transfer: C2 0.50 vs C1 0.60 fails (b)
    rows, rels = t37()
    return mix, tr, rows, rels


def test_decide_without_a_waiver_is_unchanged():
    rules = [{"id": "a", "status": "PASS"}, {"id": "b", "status": "FAIL"}]
    assert gc.decide(rules) == gc.decide(rules, ()) == (False, "PRE-GATE FAIL (b): no C2 look on OHS-4 and no ship; OHS-4 is read once for "
                                                          "C1 vs Jev only (SPEED-3); the diagnosis reads dev only")
    assert gc.decide([{"id": "a", "status": "PASS"}]) == (True, "PRE-GATE PASS: every check (a)-(d) passes; C2 gets its one OHS-4 look "
                                                                  "(L1, owner GO; A37 l)")


def test_a100_a_failed_b_is_logged_fail_marked_waived_and_ignored_by_the_verdict():
    mix, tr, rows, rels = inputs()
    plain = gc.evaluate(dev_json(), D2, mix, tr, rows, rels, LAT)
    assert not plain["pass"] and plain["decision"].startswith("PRE-GATE FAIL (b)") and "waived_failed" not in plain
    w = gc.evaluate(dev_json(), D2, mix, tr, rows, rels, LAT, waived=("b",))
    b = next(r for r in w["rules"] if r["id"] == "b")
    assert b["status"] == "FAIL" and b["waived"] == "A100" and "waived by the owner (PREREG A100)" in b["detail"]
    assert w["pass"] and w["decision"].startswith("PRE-GATE PASS") and "except (b), failed and waived by the owner (PREREG A100)" in w["decision"]
    assert w["waived_failed"] == ["b"]
    assert [r["status"] for r in w["rules"] if r["id"] != "b"] == [r["status"] for r in plain["rules"] if r["id"] != "b"]   # nothing else moved
    assert w["transfer"] == plain["transfer"]                           # (b) is still computed, same numbers


@pytest.mark.parametrize("what", ["a", "c1", "c3", "c5", "c6", "c7", "d"])
def test_a100_a_waiver_never_unblocks_any_other_check(what):
    mix, tr, rows, rels = inputs()
    dev, lat = dev_json(), dict(LAT)
    if what == "a":
        mix = rows_with(2550, 0.75, 0.70, seed=1)                       # +5 pp < +8
    elif what == "c1":
        dev = dev_json(full={"n": 7056, "diff": -3.0, "lo": -4.0, "hi": -2.0})
    elif what == "c3":
        dev = dev_json(types={"noul": {"cand": 70.0, "ref": 80.5, "diff": -10.5, "n": 3000}, "choice": {"cand": 75.0, "ref": 75.2, "diff": -0.2, "n": 4000}})
    elif what == "c5":
        dev = dev_json(equiv_flip={"cand": 12.0, "ref": 5.0, "n": 722})
    elif what == "c6":
        dev = dev_json(asr={"jagged": {"cand": 0.20, "ref": 0.0, "lo": 0.1, "veto": True}, "opi": {"cand": 0.02, "ref": 0.013, "lo": -0.01, "veto": False}})
    elif what == "c7":
        lat = LAT | {"cand_p50_ms": 120.0}                              # D9 fails together with (b)
    elif what == "d":
        rows, rels = t37(viol_c=0.15)
    res = gc.evaluate(dev, D2, mix, tr, rows, rels, lat, waived=("b",))
    failed = [r["id"] for r in res["rules"] if r["status"] != "PASS"]
    assert "b" in failed and len(failed) >= 2, failed
    assert not res["pass"] and res["decision"].startswith("PRE-GATE FAIL (") and "(b) failed and waived" in res["decision"]
    assert "b" not in res["decision"].split("PRE-GATE FAIL (")[1].split(")")[0].split(", ")            # (b) is not among the blocking ids


def test_a100_an_unmeasured_b_is_not_waived_and_a_passing_b_reads_as_before():
    mix, tr, rows, rels = inputs()
    none = gc.evaluate(dev_json(), D2, mix, [], rows, rels, LAT, waived=("b",))
    assert next(r for r in none["rules"] if r["id"] == "b")["status"] == "UNMEASURED" and not none["pass"]
    ok_tr = rows_with(1200, 0.70, 0.60, seed=2, family="T36")
    p = gc.evaluate(dev_json(), D2, mix, ok_tr, rows, rels, LAT, waived=("b",))
    assert p["pass"] and p["decision"].startswith("PRE-GATE PASS: every check (a)-(d) passes; C2 gets") and p["waived_failed"] == []


def test_a100_decide_waives_only_the_ids_it_is_given():
    rules = [{"id": "a", "status": "FAIL"}, {"id": "b", "status": "FAIL"}, {"id": "c7", "status": "UNMEASURED"}]
    ok, text = gc.decide(rules, ("b",))
    assert not ok and "(a, c7)" in text
    assert gc.decide([{"id": "b", "status": "FAIL"}], ("b",))[0]
    assert not gc.decide([{"id": "b", "status": "UNMEASURED"}], ("b",))[0]
    assert not gc.decide([{"id": "a", "status": "FAIL"}], ("b",))[0]


# ---- the pregate CLI -----------------------------------------------------------------------------------------------------
def cli_world(tmp, monkeypatch, tr_ok):
    good, off = mixdev_with_untrained()
    tr = rows_with(1200, tr_ok, 0.60, seed=2, family="T36")
    t37_rows, t37_rels = t37()
    dev_rows = rows_with(400, 0.8, 0.8, seed=4)
    for i, x in enumerate(dev_rows):
        x["source"] = "ag_news" if i < 100 else "seen"
    monkeypatch.setattr(gc, "check_candidate", lambda rec, ad, name, root: {"adapter_sha256": "c" * 64})
    monkeypatch.setattr(gc, "check_stop_rule", lambda *a: {})
    monkeypatch.setattr(gc, "check_refparity", lambda root, ref, stored=gc.STORED_C1: {})
    monkeypatch.setattr(gc, "load_d2_set", lambda p, root, cand: {"sources": {"ag_news": 100}, "sources_sha256": "d"})
    monkeypatch.setattr(g, "complete_rows", lambda splits, cand, ref: dev_rows)
    monkeypatch.setattr(g, "pipeline_check", lambda names, reads: ([], {}))
    monkeypatch.setattr(gc, "split_rows", lambda split, cand, ref, root: {gc.MIXDEV: good + off, gc.TRANSFER: tr, gc.T37B_DEV: t37_rows}[split])
    monkeypatch.setattr(gc, "relations", lambda split, root: t37_rels)
    (tmp / "dev.json").write_text(json.dumps(dev_json()))
    (tmp / "lat.json").write_text(json.dumps(LAT))
    write_mix_manifest(tmp, {"T28": 2247, "replay": 3370})
    return ["pregate", "--dev", str(tmp / "dev.json"), "--latency", str(tmp / "lat.json"), "--looks", str(tmp / "looks.jsonl"),
            "--out-dir", str(tmp), "--root", str(tmp)]


def test_a100_pregate_cli_with_a_valid_waiver_passes_on_a_failed_b_and_logs_it(world, monkeypatch, capsys):
    argv = cli_world(world, monkeypatch, tr_ok=0.50)
    assert gc.main(argv) == 0
    out = capsys.readouterr().out
    assert "check (b) waived by the owner (PREREG A100)" in out and "FAILED, waived by the owner (PREREG A100)" in out
    assert "PRE-GATE PASS" in out.splitlines()[-1]
    res = json.loads((world / f"gate_c2_pregate_{gc.CAND}.json").read_text())
    b = next(r for r in res["rules"] if r["id"] == "b")
    assert res["pass"] and b["status"] == "FAIL" and b["waived"] == "A100" and res["checks"]["waiver"]["record"] == "A100"
    look = json.loads((world / "looks.jsonl").read_text().splitlines()[-1])
    assert look["pass"] is True and look["waiver"] == "A100" and look["waived_failed"] == ["b"]


def test_a100_pregate_cli_without_or_with_a_bad_record_is_byte_identical(world, monkeypatch, capsys):
    argv = cli_world(world, monkeypatch, tr_ok=0.50)
    (world / wv.RECORD).unlink()
    assert gc.main(argv) == 0
    plain = capsys.readouterr()
    assert "PRE-GATE FAIL (b)" in plain.out.splitlines()[-1] and "waive" not in plain.out and plain.err == ""
    plain_res = (world / f"gate_c2_pregate_{gc.CAND}.json").read_text()
    for f in (world / f"gate_c2_pregate_{gc.CAND}.json", world / "looks.jsonl"):
        f.unlink()
    (world / wv.RECORD).write_text(json.dumps(record(quote=QUOTE[:-25])))                  # a truncated quote: not a waiver
    assert gc.main(argv) == 0
    bad = capsys.readouterr()
    assert bad.out == plain.out and "no waiver applied" in bad.err
    res = json.loads((world / f"gate_c2_pregate_{gc.CAND}.json").read_text())
    assert "waiver" not in res["checks"] and "waived_failed" not in res and not res["pass"]
    assert set(res) == set(json.loads(plain_res)) and "waiver" not in (world / "looks.jsonl").read_text()


def test_a100_pregate_cli_with_a_waiver_still_fails_on_an_a_failure(world, monkeypatch, capsys):
    argv = cli_world(world, monkeypatch, tr_ok=0.50)
    monkeypatch.setattr(gc, "split_rows", lambda split, cand, ref, root: {gc.MIXDEV: rows_with(2550, 0.74, 0.70, seed=1, family="T28"),
                                                                           gc.TRANSFER: rows_with(1200, 0.50, 0.60, seed=2, family="T36"),
                                                                           gc.T37B_DEV: t37()[0]}[split])
    assert gc.main(argv) == 0
    out = capsys.readouterr().out
    assert "PRE-GATE FAIL (a)" in out.splitlines()[-1] and "(b) failed and waived" in out.splitlines()[-1]
    res = json.loads((world / f"gate_c2_pregate_{gc.CAND}.json").read_text())
    assert not res["pass"] and res["waived_failed"] == ["b"]


def test_a100_waived_and_unwaived_runs_are_different_inputs(world, monkeypatch, capsys):
    argv = cli_world(world, monkeypatch, tr_ok=0.50)
    assert gc.main(argv) == 0                                                                # logged with the waiver
    capsys.readouterr()
    (world / wv.RECORD).unlink()                                                             # a second pre-gate of the same candidate, other inputs
    assert gc.main(argv) == 2 and "other inputs" in capsys.readouterr().out
