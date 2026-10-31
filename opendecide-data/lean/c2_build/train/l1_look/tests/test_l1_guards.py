"""CPU tests of the l1_look ordering guards, hash pins and plan (synthetic suite only; no real sealed file is opened).
  cd lean/c2_build/train && HF_HUB_OFFLINE=1 ../../../.venv/bin/python -B -m pytest -q l1_look/tests
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
TESTS = Path(__file__).resolve().parent
PKG = TESTS.parent
TRAIN = PKG.parent
for p in (str(TRAIN), str(TESTS)):
    sys.path.insert(0, p)

import synth as SY  # noqa: E402
from l1_look import l1common as L  # noqa: E402

P_REF = {"rows": 8143, "seq": 11957, "chars": 17175428}
pytestmark = pytest.mark.skipif(not SY.have_scorer_code(), reason="the sealed scorer / runner CODE files are not on this machine")
SHA_A, SHA_G = "a" * 64, "b" * 64


@pytest.fixture
def tree(tmp_path):
    suite = SY.make_suite()
    p, pins = SY.write_tree(tmp_path, suite)
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G)
    SY.write_parity(p, "last3_a07", SHA_A)
    return p, pins, suite


def plan(p, pins, **kw):
    kw.setdefault("trained_families", SY.trained_fn)
    return L.prepare_plan(p, "t1", pins=pins, p_ref=P_REF, spent_usd=0.0, **kw)


def a100_setup(p, monkeypatch, cand="final_a10", sha=SHA_A, failed=("b",)):
    """The A100 situation: pre-gate failed on (b) only, the waiver is on file, the A98 record is kept, a NEW CHOSEN.json names the candidate, parity passes."""
    SY.write_gate_files(p, cand, sha, SHA_G, pass_=False, decision="PRE-GATE FAIL (b)", rules=SY.rules_with(list(failed)))
    SY.write_waiver(p)
    SY.write_parity(p, cand, sha)
    monkeypatch.setattr(L, "A98_CHOSEN_SHA_PREFIX", SY.write_chosen(p, cand, sha))
    monkeypatch.setattr(L, "A100_ADAPTER_SHA256", sha)


def refusal(p, pins, **kw) -> str:
    with pytest.raises(L.Refused) as e:
        plan(p, pins, **kw)
    return str(e.value)


def test_a_clean_tree_gives_a_c1_c2_plan_with_no_content_in_it(tree):
    p, pins, suite = tree
    pl, rows = plan(p, pins)
    assert pl["mode"] == "c1c2" and [m["read_name"] for m in pl["models"]] == ["q35_4b_main500k_l1", "q35_4b_c2_l1"]
    assert pl["models"][0]["adapter_sha256"] == L.C1_ADAPTER_SHA256 and pl["models"][1]["adapter_sha256"] == SHA_A and pl["cand"] == "last3_a07"
    assert len(rows) == len(suite) == pl["final"]["n_rows"] and pl["final"]["rows_sha256"] == L.canon_sha(rows)
    blob = json.dumps({k: v for k, v in pl.items()})
    assert SY.MARK not in blob and "gold" not in blob                       # the plan holds no item text and no label
    assert all("gold" not in r and "meta" not in r for r in rows)              # the rows that leave the laptop carry no label
    assert pl["estimate"]["verdict"]["fits"] and pl["estimate"]["scenarios"]["likely"]["cost_usd"] > 0


def test_pre_gate_fail_reads_c1_alone(tree):
    p, pins, _ = tree
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=False, decision="FAIL")
    pl, _ = plan(p, pins)
    assert pl["mode"] == "c1" and [m["read_name"] for m in pl["models"]] == ["q35_4b_main500k_l1"]


def test_hash_pins_name_the_file_only(tree):
    p, pins, _ = tree
    assert L.check_hash_pins(p, pins) == []
    p.requests.write_text(p.requests.read_text() + " ")
    assert L.check_hash_pins(p, pins) == ["requests/ohs4_requests.jsonl"]
    msg = refusal(p, pins)
    assert msg == "REFUSED: hash mismatch: requests/ohs4_requests.jsonl" and SY.MARK not in msg


def test_hash_pin_of_the_suite_scorer_runner_and_manifest(tree):
    p, pins, _ = tree
    for f, name in ((p.suite, "suite/ohs4_suite.jsonl"), (p.scorer, "scorer/score_ohs4.py"), (p.jev_runner, "scorer/run_jev_ohs4.py")):
        old = f.read_text()
        f.write_text(old + "\n#")
        assert L.check_hash_pins(p, pins) == [name], name
        f.write_text(old)
    assert L.check_hash_pins(p, pins) == []
    old = p.manifest.read_text()
    p.manifest.write_text(old + " ")
    assert L.check_hash_pins(p, pins) == ["MANIFEST.json"]
    p.manifest.write_text(old)
    # a manifest that does not hold the file's hash, even with the PREREG pin intact for the other files
    m = json.loads(old)
    m["sha256"]["scorer"]["scorer/score_ohs4.py"] = "0" * 64
    p.manifest.write_text(json.dumps(m))
    assert L.check_hash_pins(p, {**pins, "MANIFEST.json": SY.sha(p.manifest)}) == ["scorer/score_ohs4.py"]


def test_real_pins_are_the_prereg_a38_values():
    assert L.A38_PINS["MANIFEST.json"].startswith("c0217e77") and L.A38_PINS["suite/ohs4_suite.jsonl"].startswith("5f303084")
    assert L.A38_PINS["requests/ohs4_requests.jsonl"] == "34993431" and L.A38_PINS["scorer/run_jev_ohs4.py"] == "5bc81eab"
    assert L.C1_ADAPTER_SHA256.startswith("507d1c29")


def test_owner_go2_is_required_and_validated(tree):
    p, pins, _ = tree
    p.owner_go.unlink()
    assert "L1_OWNER_GO2.json missing" in refusal(p, pins)
    p.owner_go.write_text(json.dumps({"owner_words": "x", "go": "GO #2", "written_utc": "t"}))
    assert "owner_words" in refusal(p, pins)
    p.owner_go.write_text(json.dumps({"owner_words": "real owner words here", "go": "nothing", "written_utc": "t"}))
    assert "GO #2" in refusal(p, pins)


def test_candidate_must_exist_and_match_the_grid_record(tree):
    p, pins, _ = tree
    cand = json.loads(p.candidate.read_text())
    p.candidate.unlink()
    assert "CANDIDATE_C2.json missing" in refusal(p, pins)
    p.candidate.write_text(json.dumps({**cand, "adapter_sha256": "c" * 64}))
    assert "same adapter sha256" in refusal(p, pins)
    p.candidate.write_text(json.dumps({**cand, "grid_candidate": "final_a10"}))
    assert "same adapter sha256" in refusal(p, pins)
    p.candidate.write_text(json.dumps({**cand, "name": "other"}))
    assert "names 'other'" in refusal(p, pins)
    p.candidate.write_text(json.dumps({**cand, "grid_sha256": "d" * 64}))
    assert "grid_sha256 differs" in refusal(p, pins)
    p.candidate.write_text(json.dumps({**cand, "symmetrised": True}))
    assert "symmetrised" in refusal(p, pins)
    p.candidate.write_text(json.dumps({**cand, "adapter_sha256": "zz"}))
    assert "no adapter sha256" in refusal(p, pins)
    p.candidate.write_text(json.dumps(cand))
    p.grid_record.unlink()
    assert "GRID_RECORD.json missing" in refusal(p, pins)


def test_pre_gate_result_is_required_and_belongs_to_the_candidate(tree):
    p, pins, _ = tree
    good = json.loads(p.pregate.read_text())
    p.pregate.unlink()
    assert "pre-gate must be computed" in refusal(p, pins)
    p.pregate.write_text(json.dumps({**good, "pass": "yes"}))
    assert "pre-gate must be computed" in refusal(p, pins)
    p.pregate.write_text(json.dumps({**good, "checks": {"candidate": {"adapter_sha256": "e" * 64}}}))
    assert "another adapter" in refusal(p, pins)
    p.pregate.write_text(json.dumps({**good, "cand": "q35_4b_other"}))
    assert "not 'q35_4b_c2'" in refusal(p, pins)
    p.pregate.write_text(json.dumps({**good, "time_unix": 50.0}))                  # the candidate record (t=100) is newer than the pre-gate
    assert "written after the pre-gate" in refusal(p, pins)


def test_only_one_look(tree):
    p, pins, _ = tree
    p.result.write_text("{}")
    assert "one look only" in refusal(p, pins)
    p.result.unlink()
    p.looks.write_text(json.dumps({"look": "L1", "status": "refused", "reason": "x"}) + "\n")
    plan(p, pins)                                                                    # a refused attempt does not use the look
    p.looks.write_text(json.dumps({"look": "L1", "status": "granted"}) + "\n")
    assert "granted L1" in refusal(p, pins)
    p.looks.unlink()
    p.raw_dir.mkdir(parents=True)
    (p.raw_dir / "x_raw.jsonl").write_text("")
    assert "raw reads of this look already exist" in refusal(p, pins)
    (p.raw_dir / "x_raw.jsonl").unlink()
    p.c1_answers.write_text("")
    assert "answer files of the look were already written" in refusal(p, pins)


def test_request_file_must_be_the_suites(tree):
    p, pins, suite = tree
    rows = [json.loads(l) for l in open(p.requests)]
    rows[0]["questions"]["q0"]["type"] = "choice" if rows[0]["questions"]["q0"]["type"] == "noul" else "noul"
    SY.write_jsonl(p.requests, rows)
    pins2 = {**pins, "requests/ohs4_requests.jsonl": SY.sha(p.requests)[:8]}
    m = json.loads(p.manifest.read_text())
    m["sha256"]["requests"]["requests/ohs4_requests.jsonl"] = SY.sha(p.requests)
    p.manifest.write_text(json.dumps(m))
    pins2["MANIFEST.json"] = SY.sha(p.manifest)
    msg = refusal(p, pins2)
    assert "request" in msg and SY.MARK not in msg


def test_every_refusal_is_content_free(tree):
    p, pins, _ = tree
    msgs = []
    for mutate in (lambda: p.owner_go.unlink(), lambda: p.candidate.unlink(), lambda: p.pregate.unlink(), lambda: p.result.write_text("{}")):
        mutate()
        msgs.append(refusal(p, pins))
    assert all(SY.MARK not in m and "gold" not in m.lower() for m in msgs)


def test_the_package_imports_where_it_sits_in_the_container(monkeypatch):
    """The A85 lesson: HERE.parents[2] raises IndexError when the package sits at /root/l1_look. Execute the module as if it were there."""
    monkeypatch.delenv("OD_LEAN", raising=False)
    ns = {"__file__": "/root/l1_look/l1common.py", "__name__": "l1_look_probe"}
    exec(compile((PKG / "l1common.py").read_text(), "/root/l1_look/l1common.py", "exec"), ns)
    assert str(ns["LEAN_DEFAULT"]) == "/root/lean" and str(ns["HERE"]) == "/root/l1_look"
    monkeypatch.setenv("OD_LEAN", "/somewhere/lean")
    ns2 = {"__file__": "/root/l1_look/l1common.py", "__name__": "l1_look_probe2"}
    exec(compile((PKG / "l1common.py").read_text(), "/root/l1_look/l1common.py", "exec"), ns2)
    assert str(ns2["LEAN_DEFAULT"]) == "/somewhere/lean"
    for mod in ("modal_app_l1.py", "l1session.py", "l1reader.py", "j_run.py", "l1_cli.py", "l1verdict.py", "l1temp.py"):
        src = (PKG / mod).read_text()
        assert "parents[2]" not in src and "parents[3]" not in src, mod        # no module computes the lean root from its own depth


def test_raw_writing_keeps_each_read_in_its_own_folder(tree):
    p, pins, _ = tree
    pl, _ = plan(p, pins)
    res = {"ok": True, "errors": [], "wall_s": 1.0, "spent_usd": 0.1, "path_sha256": "p", "env": {}, "models": {},
           "reads": {n: {L.MIXDEV_SPLIT: [{"id": "m1", "probs": {"yes": 0.5, "no": 0.5}}], L.FINAL_SPLIT: [{"id": "syn-1", "probs": {"yes": 0.6, "no": 0.4}}]}
                     for n in ("q35_4b_main500k_l1", "q35_4b_c2_l1")}}
    rec = L.write_raw(p, pl, res)
    assert (p.out_root / "t1" / "dev" / "q35_4b_c2_l1.jsonl").exists() and (p.raw_dir / "q35_4b_c2_l1_raw.jsonl").exists()
    assert not any("syn-1" in f.read_text() for f in (p.out_root / "t1").rglob("*") if f.is_file())          # no sealed id outside the sealed folder
    assert json.dumps(rec).count("syn-1") == 0
    assert (p.raw_dir / "q35_4b_c2_l1_raw.jsonl").stat().st_mode & 0o222 == 0                                   # read-only
    with pytest.raises(L.Refused):                                                                              # the GPU job cannot run twice
        L.guard_gpu_fresh(p)


# ------------------------------------------------------------------ PREREG Record A100: the owner waived pre-gate (b)
def test_b_only_failure_with_the_a100_waiver_is_read_as_pass_with_c1_and_c2(tree, monkeypatch):
    p, pins, _ = tree
    a100_setup(p, monkeypatch)
    pl, rows = plan(p, pins)
    assert pl["mode"] == "c1c2" and [m["read_name"] for m in pl["models"]] == ["q35_4b_main500k_l1", "q35_4b_c2_l1"] and pl["cand"] == "final_a10"
    assert pl["pregate"]["waived"] == ["b"] and pl["pregate"]["failed"] == ["b"] and pl["pregate"]["effective_pass"] and pl["pregate"]["pass"] is False
    assert pl["pregate"]["waiver_sha256"] == SY.sha(p.waiver_b)
    pg = L.load_pregate(p, L.load_candidate(p))
    assert pg["effective_pass"] and pg["waived"] == ["b"]


def test_a_b_only_failure_without_the_waiver_is_refused_not_read_as_c1_alone(tree):
    p, pins, _ = tree
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=False, decision="FAIL", rules=SY.rules_with(["b"]))
    msg = refusal(p, pins)
    assert "WAIVER_B_A100.json is absent" in msg and "one look is not spent on a guess" in msg


def test_the_waiver_only_covers_b_any_other_failed_check_means_c1_alone(tree):
    p, pins, _ = tree
    SY.write_waiver(p)
    for failed in (["a"], ["b", "c3"], ["c7"], ["d", "b"]):
        SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=False, decision="FAIL", rules=SY.rules_with(failed))
        pl, _ = plan(p, pins)
        assert pl["mode"] == "c1" and not pl["pregate"]["effective_pass"] and pl["pregate"]["waived"] == [], failed
        assert [m["read_name"] for m in pl["models"]] == ["q35_4b_main500k_l1"]


def test_the_waiver_record_is_checked_by_waiver_a100(tree, monkeypatch):
    p, pins, _ = tree
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=False, decision="FAIL", rules=SY.rules_with(["b"]))
    wa = SY.L_waiver_module()
    SY.write_waiver(p, record="A99")
    assert "not an active A100 waiver" in refusal(p, pins) and "not an A100 record" in refusal(p, pins)
    SY.write_waiver(p, waived_rule="a")
    assert "waives something other than check (b)" in refusal(p, pins)
    SY.write_waiver(p, waives=["b_transfer", "a_learning"])
    assert "waives something other than check (b)" in refusal(p, pins)
    SY.write_waiver(p, quote=wa.A100_QUOTE[:60])                                  # a truncated / prefix quote is not the full sentence
    assert "not the full verbatim A100 sentence" in refusal(p, pins)
    SY.write_waiver(p, quote=wa.A100_QUOTE + " Also waive (a).")
    assert "not the full verbatim A100 sentence" in refusal(p, pins)
    SY.write_waiver(p, prereg=False)
    assert "not in PREREG_FINAL.md Record A100" in refusal(p, pins)
    SY.write_waiver(p, prereg_text="> **Record A100 (18 Oct 2026; orchestrator note, no owner words)\n")
    assert "not in PREREG_FINAL.md Record A100" in refusal(p, pins)
    SY.write_waiver(p, owner_go=False)
    assert "not in OWNER_GO_C2.txt" in refusal(p, pins)
    p.waiver_b.write_text("[1]")
    assert "not an active A100 waiver" in refusal(p, pins)
    p.waiver_b.write_text("{not json")
    assert "not an active A100 waiver" in refusal(p, pins)
    SY.write_waiver(p)
    SY.write_parity(p, "last3_a07", SHA_A)
    assert "expects select_candidate to yield final_a10" in refusal(p, pins)          # a valid waiver, but the A100 ruling expects final_a10
    a100_setup(p, monkeypatch)
    assert plan(p, pins)[0]["mode"] == "c1c2"


def test_the_a100_adapter_is_pinned_in_code(tree, monkeypatch):
    p, pins, _ = tree
    assert L.A100_ADAPTER_SHA256 == "93aba519264b8ad3fa4b8e2a80a5b89fe7eb5d184d789cc5fcfdd32c46b08041"
    a100_setup(p, monkeypatch)
    monkeypatch.setattr(L, "A100_ADAPTER_SHA256", "7" * 64)
    assert "not the pinned 77777777... (final_a10)" in refusal(p, pins)


def test_a_clean_pass_and_the_pass_with_a_failed_list_are_told_apart(tree):
    p, pins, _ = tree
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=True, rules=SY.rules_with([]))
    pl, _ = plan(p, pins)
    assert pl["mode"] == "c1c2" and pl["pregate"]["waived"] == [] and pl["pregate"]["waiver_sha256"] is None
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=True, rules=SY.rules_with(["c2"]))
    assert "says PASS but lists failing checks" in refusal(p, pins)
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=False, decision="FAIL")          # no list of checks
    SY.write_waiver(p)
    assert "cannot tell whether only (b) failed" in refusal(p, pins)
    p.waiver_b.unlink()
    assert plan(p, pins)[0]["mode"] == "c1"


def test_a_gate_that_already_reports_pass_with_b_failing_still_needs_the_waiver_record(tree, monkeypatch):
    p, pins, _ = tree
    SY.write_gate_files(p, "final_a10", SHA_A, SHA_G, pass_=True, decision="PASS (b waived)", rules=SY.rules_with(["b"]))
    assert "WAIVER_B_A100.json is absent" in refusal(p, pins)
    a100_setup(p, monkeypatch)
    SY.write_gate_files(p, "final_a10", SHA_A, SHA_G, pass_=True, decision="PASS (b waived)", rules=SY.rules_with(["b"]))
    pl, _ = plan(p, pins)
    assert pl["mode"] == "c1c2" and pl["pregate"]["waived"] == ["b"] and pl["pregate"]["pass"] is True


def test_an_unmeasured_b_is_not_waived(tree):
    p, pins, _ = tree
    SY.write_waiver(p)
    rules = SY.rules_with([])
    rules[1]["status"] = "UNMEASURED"
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=False, decision="FAIL", rules=rules)
    pl, _ = plan(p, pins)
    assert pl["mode"] == "c1" and pl["pregate"]["waived"] == []


def test_the_real_waiver_file_has_a_shape_the_loader_accepts():
    """The orchestrator's real c2_build/train/WAIVER_B_A100.json and the real PREREG line (both non-sealed)."""
    real = L.L1Paths()
    if not real.waiver_b.exists():
        pytest.skip("no waiver file on this machine")
    w = L.load_waiver_b(real)
    assert w["record"] == "A100" and w["waived_rule"] == "b" and len(w["_sha256"]) == 64



# ------------------------------------------------------------------ RULING_L1_PRELOOK item 8: parity, A100 preconditions; item 1: the fit rows
def test_a_passing_h100_parity_record_is_required_for_c2_and_the_file_is_named(tree):
    p, pins, _ = tree
    f = SY.write_parity(p, "last3_a07", SHA_A)
    pl, _ = plan(p, pins)
    assert pl["parity"]["argmax_agree"] == 0.9985 and pl["parity"]["n"] == 2000 and pl["parity"]["sha256"] == SY.sha(f)
    f.unlink()
    msg = refusal(p, pins)
    assert "PARITY_last3_a07.json missing" in msg and "c2_build/train/PARITY_last3_a07.json" in msg and "no ship without a passing H100 parity record" in msg


@pytest.mark.parametrize("over,why", [({"agree": 0.994}, "below 0.995"), ({"n": 1999}, "fewer than 2000"), ({"gpu": "NVIDIA L4"}, "not an H100"),
                                       ({"bar": {"PASS": False, "PASS_gate": False}}, "did not pass"), ({"bar": {"PASS": True, "PASS_gate": False}}, "did not pass"),
                                       ({"served_problems": ["server config changed"]}, "lists problems"), ({"ref_meta_problems": ["x"]}, "lists problems"),
                                       ({"adapter_sha256": "9" * 64}, "no record names this candidate"), ({"cand": "final_a10"}, "no record names this candidate")])
def test_a_parity_record_that_does_not_pass_is_refused(tree, over, why):
    p, pins, _ = tree
    SY.write_parity(p, "last3_a07", SHA_A, **over)
    assert why in refusal(p, pins)


def test_the_parity_record_is_also_found_where_the_grid_tool_writes_it(tree):
    p, pins, _ = tree
    (p.train / "PARITY_last3_a07.json").unlink()
    SY.write_parity(p, "last3_a07", SHA_A, where="grid_results")
    assert plan(p, pins)[0]["parity"]["file"].endswith("PARITY_last3_a07.json")


def test_c1_alone_needs_no_parity_record(tree):
    p, pins, _ = tree
    (p.train / "PARITY_last3_a07.json").unlink()
    SY.write_gate_files(p, "last3_a07", SHA_A, SHA_G, pass_=False, decision="FAIL", rules=SY.rules_with(["a"]))
    pl, _ = plan(p, pins)
    assert pl["mode"] == "c1" and pl["parity"] is None


def test_a100_preconditions_candidate_a98_record_and_new_chosen(tree, monkeypatch):
    p, pins, _ = tree
    a100_setup(p, monkeypatch)
    assert plan(p, pins)[0]["cand"] == "final_a10"
    # the tool yielded another candidate than the ruling expects
    SY.write_gate_files(p, "last3_a09", SHA_A, SHA_G, pass_=False, decision="FAIL", rules=SY.rules_with(["b"]), candidates={"last3_a09": SHA_A, "final_a10": SHA_A})
    SY.write_parity(p, "last3_a09", SHA_A)
    assert "stop and report to the owner" in refusal(p, pins)
    a100_setup(p, monkeypatch)
    # the A98 record must be kept for audit
    p.chosen_a98.unlink()
    assert "CHOSEN_A98_NOCANDIDATE.json missing" in refusal(p, pins)
    monkeypatch.setattr(L, "A98_CHOSEN_SHA_PREFIX", SY.write_chosen(p, "final_a10", SHA_A))
    p.chosen_a98.write_text("something else")
    assert "missing or not the A98 record" in refusal(p, pins)
    monkeypatch.setattr(L, "A98_CHOSEN_SHA_PREFIX", SY.write_chosen(p, "final_a10", SHA_A))
    # a new CHOSEN.json must exist, differ from the A98 record and name the candidate
    p.chosen.write_text(p.chosen_a98.read_text())
    assert "has not written a new CHOSEN record" in refusal(p, pins)
    p.chosen.write_text(json.dumps({"chosen": "final_a10", "chosen_adapter_sha256": "8" * 64}))
    assert "does not name the candidate and adapter sha256" in refusal(p, pins)
    p.chosen.write_text(json.dumps({"chosen": "last3_a09", "chosen_adapter_sha256": SHA_A}))
    assert "does not name the candidate" in refusal(p, pins)
    p.chosen.unlink()
    assert "has not written a new CHOSEN record" in refusal(p, pins)


def test_mixdev_must_be_the_gates_file(tree):
    p, pins, _ = tree
    SY.write_grid_plan(p, SY.sha(p.mixdev))
    plan(p, pins)
    SY.write_grid_plan(p, "0" * 64)
    assert "differs from the file the gate read" in refusal(p, pins)


def test_the_fit_needs_two_groups_per_type_among_the_trained_families(tree):
    p, pins, _ = tree
    pl, _ = plan(p, pins)
    assert pl["trained_families"] == SY.TRAINED and "T05" not in pl["trained_families"]
    assert "fewer than 2 groups" in refusal(p, pins, trained_families=lambda p_: ["no-such-family"])
    rows = [json.loads(l) for l in open(p.mixdev)]
    only_choice = [r for r in rows if r["qtype"] == "choice"]
    SY.write_jsonl(p.mixdev, only_choice)
    pins2 = pins
    assert "fewer than 2 groups for ['noul']" in refusal(p, pins2)


def test_the_fit_rows_are_the_trained_family_rows_of_the_mixdev(tree):
    p, pins, _ = tree
    rows = L.mixdev_fit_rows(p, SY.TRAINED)
    assert rows and all(r["meta"]["family"] in SY.TRAINED for r in rows)
    assert len(rows) < sum(1 for _ in open(p.mixdev))                              # the untrained family is out


def test_disclosure_lines_are_the_rulings(tree, monkeypatch):
    p, pins, _ = tree
    pl, _ = plan(p, pins)
    assert pl["disclosure"] == [L.SPEED3_LINE] and L.SPEED3_LINE.startswith("SPEED-3 was not run: the load test was not built before the one-shot final")
    assert "any latency or cost figure quoted comes from earlier C1 measurements (SPEED-2 / C1 optimisation) and is labelled as such." in L.SPEED3_LINE
    a100_setup(p, monkeypatch)
    w = json.loads(p.waiver_b.read_text())
    w["b_numbers_at_waiver"] = {"final_a10": "-4.83 pp [-8.59, -1.02] (n 600)"}
    p.waiver_b.write_text(json.dumps(w))
    pl, _ = plan(p, pins)
    assert pl["disclosure"][0] == ("OWNER OVERRIDE (PREREG A100, 18 Oct 2026 ~19:20 UTC / 3:20 PM ET, after the result): pre-gate (b) transfer FAILED: "
                                   "final_a10 C2 \u2212 C1 = \u22124.83 pp [\u22128.59, \u22121.02] (n 600; the rule needs \u2265 +3.0 pp and LB > 0; all 18 candidates failed (b)). "
                                   "The owner waived (b) and put the A42-D 9.5 candidate into the one OHS-4 look with C1. Without the waiver the pre-gate fails and L1 reads "
                                   "C1 alone. Every other check, parity and S1-S6 bind unchanged.")
    assert pl["disclosure"][1] == L.SPEED3_LINE


def test_the_real_parity_record_has_a_shape_the_guard_accepts():
    """The orchestrator's real PARITY_<cand>.json and CANDIDATE_C2.json (both non-sealed), when they are on this machine."""
    real = L.L1Paths()
    if not (real.candidate.exists() and real.grid_record.exists()):
        pytest.skip("no candidate record on this machine")
    cand = L.load_candidate(real)
    if not L.parity_files(real, cand["grid_candidate"]):
        pytest.skip("no parity record yet")
    par = L.load_parity(real, cand)
    assert par["argmax_agree"] >= 0.995 and par["n"] >= 2000 and "H100" in par["gpu"] and len(par["sha256"]) == 64


# ------------------------------------------------------------------ BLOCKING 2: the pre-gate's identity and order are required, never skipped
@pytest.mark.parametrize("drop", ["cand_written_unix", "time_unix", "adapter_sha", "cand"])
def test_a_missing_identity_or_time_field_is_refused_not_skipped(tree, drop):
    p, pins, _ = tree
    if drop == "cand_written_unix":
        c = json.loads(p.candidate.read_text())
        c.pop("written_unix")
        p.candidate.write_text(json.dumps(c))
    else:
        pg = json.loads(p.pregate.read_text())
        {"time_unix": lambda: pg.pop("time_unix"), "adapter_sha": lambda: pg["checks"]["candidate"].pop("adapter_sha256"), "cand": lambda: pg.pop("cand")}[drop]()
        p.pregate.write_text(json.dumps(pg))
    msg = refusal(p, pins)
    assert "missing or invalid" in msg and "cannot be checked" in msg


@pytest.mark.parametrize("field,bad", [("time_unix", "200"), ("time_unix", True), ("time_unix", None), ("cand", ""), ("cand", 5)])
def test_a_wrongly_typed_identity_field_is_refused(tree, field, bad):
    p, pins, _ = tree
    pg = json.loads(p.pregate.read_text())
    pg[field] = bad
    p.pregate.write_text(json.dumps(pg))
    assert "missing or invalid" in refusal(p, pins)


def test_the_pre_gate_must_be_newer_or_equal_and_match_adapter_and_cand(tree):
    p, pins, _ = tree
    pg = json.loads(p.pregate.read_text())
    plan(p, pins)
    p.pregate.write_text(json.dumps({**pg, "time_unix": 100.0}))                       # equal times pass (written_unix <= time_unix)
    plan(p, pins)
    p.pregate.write_text(json.dumps({**pg, "time_unix": 99.9}))
    assert "written after the pre-gate" in refusal(p, pins)
    p.pregate.write_text(json.dumps({**pg, "checks": {"candidate": {"adapter_sha256": "e" * 64}}}))
    assert "another adapter" in refusal(p, pins)
    p.pregate.write_text(json.dumps({**pg, "checks": {"candidate": {"adapter_sha256": "short"}}}))
    assert "missing or invalid" in refusal(p, pins)
    p.pregate.write_text(json.dumps({**pg, "cand": "q35_4b_other"}))
    assert "not 'q35_4b_c2'" in refusal(p, pins)


# ------------------------------------------------------------------ (f) ALL manifest files
def test_every_file_the_manifest_lists_is_rechecked(tree):
    p, pins, _ = tree
    extra = p.sealed / "exports" / "ngrams_x.bin"
    extra.parent.mkdir(parents=True)
    extra.write_bytes(b"synthetic export bytes")
    m = json.loads(p.manifest.read_text())
    m["sha256"]["exports"] = {"exports/ngrams_x.bin": SY.sha(extra), "exports/gone.json": "0" * 64}
    p.manifest.write_text(json.dumps(m))
    pins2 = {**pins, "MANIFEST.json": SY.sha(p.manifest)}
    assert L.check_hash_pins(p, pins2) == ["exports/gone.json (missing)"]
    extra.write_bytes(b"tampered")
    assert sorted(L.check_hash_pins(p, pins2)) == ["exports/gone.json (missing)", "exports/ngrams_x.bin"]
    msg = refusal(p, pins2)
    assert msg.startswith("REFUSED: hash mismatch: ") and SY.MARK not in msg


def test_the_real_manifest_entries_are_all_present_and_checked():
    real = L.L1Paths()
    man = L.read_json(real.manifest)
    if not man:
        pytest.skip("no sealed folder on this machine")
    n = sum(len(v) for v in man["sha256"].values())
    assert n == 243 and L.check_hash_pins(real) == []                                  # all 243 files, names only on a difference


# ------------------------------------------------------------------ (a) a second launch cannot overwrite the raw reads; (g) no region from the environment
def test_write_raw_refuses_before_touching_existing_raw_reads(tree):
    p, pins, _ = tree
    pl, _ = plan(p, pins)
    res = {"ok": True, "errors": [], "wall_s": 1.0, "spent_usd": 0.1, "path_sha256": "p", "env": {}, "models": {},
           "reads": {n: {L.MIXDEV_SPLIT: [{"id": "m1", "probs": {"yes": 0.5, "no": 0.5}}], L.FINAL_SPLIT: [{"id": "syn-1", "probs": {"yes": 0.6, "no": 0.4}}]}
                     for n in ("q35_4b_main500k_l1", "q35_4b_c2_l1")}}
    L.write_raw(p, pl, res)
    before = {f.name: f.read_bytes() for f in p.raw_dir.iterdir()}
    res2 = json.loads(json.dumps(res))
    res2["reads"]["q35_4b_c2_l1"][L.FINAL_SPLIT][0]["probs"] = {"yes": 0.1, "no": 0.9}
    with pytest.raises(L.Refused, match="raw reads of this look already exist"):
        L.write_raw(p, pl, res2)
    assert {f.name: f.read_bytes() for f in p.raw_dir.iterdir()} == before


def test_the_region_is_never_read_from_the_environment(tree, monkeypatch):
    p, pins, _ = tree
    monkeypatch.setenv("L1_REGION", "us")
    pl, _ = plan(p, pins)
    assert pl["limits"]["region"].startswith("any")
    for f in PKG.glob("*.py"):
        assert "L1_REGION" not in f.read_text(), f.name                       # no module even names the variable: unpinned is the only mode
