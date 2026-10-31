"""CPU tests for the P6 grid tooling: grid_plan.py (grid record, read plan, CANDIDATE_C2 timing), grid_elig.py (the 11
eligibility booleans per candidate) and sym_reads.py (q / flip-q records and latency). Tiny fake tensors and tmp trees; no Modal,
no network, no G13, no OHS path.
  cd lean/c2_build/train && ../../../.venv/bin/python -B -m pytest -q tests/test_grid_tools.py"""
import json
import os
import random
import sys
from pathlib import Path

import pytest

TRAIN = Path(__file__).resolve().parents[1]
C2B = TRAIN.parent
LEAN = C2B.parent
sys.path.insert(0, str(TRAIN))
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(TRAIN / "tests"))
import gate_c2 as gc  # noqa: E402
import gate_dev as g  # noqa: E402
import grid_elig as ge  # noqa: E402
import grid_plan as gp  # noqa: E402
import merge_avg as ma  # noqa: E402
import select_candidate as sc  # noqa: E402
import sym_reads as sr  # noqa: E402
import symmetrise as sy  # noqa: E402
from test_train_tools import fake_adapter  # noqa: E402


# ------------------------------------------------------------------------------------------------ fixtures
@pytest.fixture
def real_grid(tmp_path, monkeypatch):
    n = 1000
    fake_adapter(tmp_path / "c1", 1)
    run = tmp_path / "run"
    fake_adapter(run, 2, n_steps=n)
    for k, f in enumerate((0.25, 0.33, 0.5, 0.67, 0.75, 0.83, 0.92)):
        fake_adapter(run / "snaps" / f"s{int(f * n):06d}", 10 + k)
    grid = ma.build_grid(tmp_path / "c1", run, tmp_path / "grid")
    monkeypatch.setattr(gp, "C1_SHA_PREFIX", grid["c1_adapter_sha256"][:8])
    return tmp_path, grid


def touch(path: Path, mtime: float, text="x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    os.utime(path, (mtime, mtime))


# ------------------------------------------------------------------------------------------------ grid_plan: the grid
def test_constants_are_merge_avgs_and_the_sha_formula_is_the_same(real_grid):
    root, grid = real_grid
    assert gp.ALPHAS == ma.ALPHAS and gp.BASES == ma.BASES and gp.EARLY_FRAC == ma.EARLY_FRAC
    assert gp.expected_names() == [c["name"] for c in grid["candidates"]]
    assert gp.canon_grid_sha(grid) == grid["grid_sha256"] and len(gp.expected_names()) == 18
    assert gp.check_grid(grid, root / "grid") == []


def test_check_grid_catches_edits_and_wrong_shapes(real_grid):
    root, grid = real_grid
    g2 = json.loads(json.dumps(grid))
    g2["candidates"][3]["alpha"] = 0.9
    assert any("grid_sha256 does not match" in p for p in gp.check_grid(g2))
    g3 = json.loads(json.dumps(grid))
    g3["candidates"].pop()
    assert any("18" in p for p in gp.check_grid(g3))
    g4 = json.loads(json.dumps(grid))
    next(c for c in g4["candidates"] if c["name"] == "final_a10")["adapter_sha256"] = "0" * 64
    g4["grid_sha256"] = gp.canon_grid_sha(g4)                       # re-signed: still not the frozen grid (final_a10 != final)
    assert any("final_a10" in p for p in gp.check_grid(g4))
    open(root / "grid" / "last3_a07" / "adapter_model.safetensors", "ab").write(b"0")
    assert any("last3_a07" in p and "on disk" in p for p in gp.check_grid(grid, root / "grid"))
    g5 = json.loads(json.dumps(grid))
    g5["bases"]["earlylate"] = {"s000250": 0.5, "final": 0.5}      # not the checkpoint nearest 33%
    g5["grid_sha256"] = gp.canon_grid_sha(g5)
    assert any("earlylate" in p for p in gp.check_grid(g5))


def test_record_once_before_any_look_and_verify(real_grid):
    root, grid = real_grid
    lean = root / "lean"
    (lean).mkdir()
    out = root / "GRID_RECORD.json"
    rec = gp.record(root / "grid" / "grid.json", out, root / "grid", lean, now=1000.0)
    assert rec["grid_sha256"] == grid["grid_sha256"] and "recorded before any grid read" in rec["addendum_line"]
    with pytest.raises(gp.Refused, match="exists"):
        gp.record(root / "grid" / "grid.json", out, None, lean)
    ok = gp.verify_record(out, root / "grid" / "grid.json", lean)
    assert ok["ok"] and ok["first_read_unix"] is None
    touch(lean / "preds_dev" / "q35_4b_c2grid_last3_a07.jsonl", 2000.0)       # a read after the record: fine
    assert gp.verify_record(out, root / "grid" / "grid.json", lean)["ok"]
    touch(lean / "preds_dev" / "q35_4b_c2grid_final_a10.jsonl", 500.0)        # a read BEFORE the record
    bad = gp.verify_record(out, root / "grid" / "grid.json", lean)
    assert not bad["ok"] and any("after the first grid read" in p for p in bad["problems"])
    (root / "grid" / "grid.json").write_text((root / "grid" / "grid.json").read_text() + " ")
    assert any("changed after it was recorded" in p for p in gp.verify_record(out, root / "grid" / "grid.json", lean)["problems"])


def test_record_refuses_when_a_candidate_was_already_read(real_grid):
    root, _ = real_grid
    lean = root / "lean"
    touch(lean / "preds_dev_nc" / "q35_4b_c2grid_earlylate_a05.jsonl", 10.0)
    with pytest.raises(gp.Refused, match="before any look"):
        gp.record(root / "grid" / "grid.json", root / "R.json", None, lean)
    # the C1 reference read is not a look at a candidate
    (lean / "preds_dev_nc" / "q35_4b_c2grid_earlylate_a05.jsonl").unlink()
    touch(lean / "preds_dev_nc" / f"{gp.REF_NAME}.jsonl", 10.0)
    assert gp.record(root / "grid" / "grid.json", root / "R.json", None, lean)["grid_sha256"]


# ------------------------------------------------------------------------------------------------ grid_plan: the read plan
def test_read_plan_shape_commands_and_no_server_actions(tmp_path):
    (tmp_path / "data").mkdir()
    for sp, n in (("dev", 3), ("c2_transfer_dev", 2)):
        (tmp_path / "data" / f"{sp}.jsonl").write_text("{}\n" * n)
    plan = gp.build_plan(tmp_path, None)
    assert plan["n_candidates"] == 18 and len(plan["reads"]) == 19 and plan["read_order"][:2] == ["REF", "final_a10"]
    assert plan["reads"][0]["name"] == gp.REF_NAME and plan["reads"][1]["name"] == "q35_4b_c2grid_final_a10"
    names = [r["name"] for r in plan["reads"]]
    assert len(set(names)) == 19 and all("4b" in n.split("_") for n in names)         # gate_dev infers the size from the name
    a, b, c = plan["reads"][2]["jobs"]
    assert "--perm-seed 1 --tag _perm" in b["cmd"] and "--perm-seed" not in a["cmd"] and "--perm-seed" not in c["cmd"]
    assert "--tta-choice" in c["cmd"] and "--tta-choice" not in a["cmd"] and "--tta-choice" not in b["cmd"]
    assert gp.GPROXY_SPLIT in c["cmd"] and "c2_mixdev" in a["cmd"] and "eval_jagged" in a["cmd"]
    text = json.dumps([r["jobs"] for r in plan["reads"]] + [plan["sequence"]])
    for forbidden in ("pkill", "fast_read.py stop", "fast_read.py serve", "start_server", "30000", "modal ", "kill", "systemctl"):
        assert forbidden not in text, forbidden
    assert plan["split_rows"]["dev"] == 3 and plan["split_rows"]["c2_mixdev"] is None
    assert plan["minutes_per_read"]["unknown_row_counts"] and plan["estimate_hours"]["reads"] > 0
    assert len(plan["open_questions"]) >= 6 and plan["grid_sha256"] is None


def test_plan_from_a_real_grid_lists_adapter_shas(real_grid):
    root, grid = real_grid
    plan = gp.build_plan(root, grid)
    assert plan["grid_sha256"] == grid["grid_sha256"]
    byname = {r.get("candidate"): r for r in plan["reads"]}
    assert byname["last3_a07"]["adapter_sha256"] == next(c["adapter_sha256"] for c in grid["candidates"] if c["name"] == "last3_a07")
    cfg = gp.default_cfg(root)
    assert cfg["name_tpl"] == gp.READ_TPL and cfg["ref"] == gc.REF and cfg["run_name"] == gc.CAND


def test_plan_names_match_the_gate(tmp_path):
    assert gp.REF_NAME == gc.REF and gp.RUN_NAME == gc.CAND and gp.SPLITS9 == tuple(gc.SPLITS9)
    assert (gp.C2_DEV == (gc.MIXDEV, gc.TRANSFER, gc.T37B_DEV))


# ------------------------------------------------------------------------------------------------ CANDIDATE_C2 timing
def _cand_setup(tmp_path, real_grid):
    root, grid = real_grid
    lean = root / "lean"
    lean.mkdir(exist_ok=True)
    gpath, rec = root / "grid" / "grid.json", root / "REC.json"
    gp.record(gpath, rec, None, lean, now=1000.0)
    chosen = "last3_a08"
    sha = next(c["adapter_sha256"] for c in grid["candidates"] if c["name"] == chosen)
    for sp in ("dev", "pg_dev"):
        touch(lean / f"preds_{sp}" / "q35_4b_c2grid_final_a10.jsonl", 2000.0)       # grid reads
    cand = root / "CANDIDATE_C2.json"
    cand.write_text(json.dumps({"name": "q35_4b_c2", "grid_candidate": chosen, "adapter_sha256": sha,
                                "grid_sha256": grid["grid_sha256"], "written_unix": 3000.0}))
    os.utime(cand, (3000.0, 3000.0))
    ch = root / "CHOSEN.json"
    ch.write_text(json.dumps({"chosen": chosen, "chosen_adapter_sha256": sha, "grid_sha256": grid["grid_sha256"]}))
    ad = root / "gate" / "adapter_model.safetensors"
    ad.parent.mkdir()
    ad.write_bytes((root / "grid" / chosen / "adapter_model.safetensors").read_bytes())
    return root, lean, gpath, rec, cand, ch, ad


def test_candidate_check_ok_before_the_official_reads(tmp_path, real_grid):
    root, lean, gpath, rec, cand, ch, ad = _cand_setup(tmp_path, real_grid)
    r = gp.candidate_check(cand, gpath, rec, ch, ad, lean)
    assert r["ok"] and r["status"] == "OK_BEFORE_READS", r
    touch(lean / "preds_dev" / "q35_4b_c2.jsonl", 4000.0)                              # official read after the record: fine
    assert gp.candidate_check(cand, gpath, rec, ch, ad, lean)["status"] == "OK_READS_AFTER"


def test_candidate_check_failures(tmp_path, real_grid):
    root, lean, gpath, rec, cand, ch, ad = _cand_setup(tmp_path, real_grid)
    touch(lean / "preds_dev" / "q35_4b_c2.jsonl", 2500.0)                              # an official read BEFORE the record
    r = gp.candidate_check(cand, gpath, rec, ch, ad, lean)
    assert not r["ok"] and any("after the first official read" in p for p in r["problems"])
    (lean / "preds_dev" / "q35_4b_c2.jsonl").unlink()
    ad.write_bytes(b"other")
    assert any("gate's path" in p for p in gp.candidate_check(cand, gpath, rec, ch, ad, lean)["problems"])
    ad.write_bytes((root / "grid" / "last3_a08" / "adapter_model.safetensors").read_bytes())
    d = json.loads(cand.read_text())
    d["adapter_sha256"] = "1" * 64
    cand.write_text(json.dumps(d))
    assert any("not grid.json's sha" in p for p in gp.candidate_check(cand, gpath, rec, ch, ad, lean)["problems"])
    d.update(adapter_sha256=next(c["adapter_sha256"] for c in json.loads(gpath.read_text())["candidates"] if c["name"] == "last3_a08"),
             written_unix=1500.0)
    cand.write_text(json.dumps(d))
    r = gp.candidate_check(cand, gpath, rec, ch, ad, lean)
    assert any("before the last grid read" in p for p in r["problems"])
    d["written_unix"] = 500.0
    cand.write_text(json.dumps(d))
    assert any("older than the grid record" in p for p in gp.candidate_check(cand, gpath, rec, ch, ad, lean)["problems"])
    cand.unlink()
    assert gp.candidate_check(cand, gpath, rec, ch, ad, lean)["status"] == "NOT_WRITTEN"


def test_candidate_check_agrees_with_gate_c2_check_candidate(tmp_path, real_grid):
    """The gate's own refusal (record written after the first read of q35_4b_c2) is the one the check anticipates."""
    root, lean, gpath, rec, cand, ch, ad = _cand_setup(tmp_path, real_grid)
    gate_root = lean
    off = lean / "preds_dev" / "q35_4b_c2.jsonl"
    touch(off, 2500.0)                                                                    # read before the record (3000)
    with pytest.raises(gc.Refused, match="after the candidate's first read"):
        gc.check_candidate(cand, ad, "q35_4b_c2", gate_root)
    assert not gp.candidate_check(cand, gpath, rec, ch, ad, lean)["ok"]
    off.unlink()
    touch(off, 4000.0)
    assert gc.check_candidate(cand, ad, "q35_4b_c2", gate_root)["name"] == "q35_4b_c2"
    assert gp.candidate_check(cand, gpath, rec, ch, ad, lean)["ok"]


def test_select_candidate_output_passes_the_timing_check_shape(tmp_path, real_grid):
    """select_candidate.py --candidate-out writes name / grid_candidate / adapter_sha256 / grid_sha256 / written_unix."""
    root, grid = real_grid
    recs = {}
    for c in grid["candidates"]:
        recs[c["name"]] = {"candidate": c["name"], "items": {"gproxy": {"id": ["a", "b"], "cluster": ["a", "b"], "correct": [1, 0]},
                                                           "rmixdev": {"id": ["a", "b"], "cluster": ["a", "b"], "correct": [1, 0]}},
                           "eligibility": {k: c["name"] != "final_a10" for k in sc.ELIG_KEYS}}
    d = root / "reads"
    d.mkdir()
    for n, r in recs.items():
        (d / f"{n}.json").write_text(json.dumps(r))
    rc = sc.main(["--reads", str(d), "--grid", str(root / "grid" / "grid.json"), "--out", str(root / "CH.json"),
                  "--candidate-out", str(root / "CAND.json"), "--resamples", "200"])
    c = json.loads((root / "CAND.json").read_text())
    assert rc == 0 and {"name", "grid_candidate", "adapter_sha256", "grid_sha256", "written_unix"} <= set(c)
    assert c["adapter_sha256"] == next(x["adapter_sha256"] for x in grid["candidates"] if x["name"] == c["grid_candidate"])


# ------------------------------------------------------------------------------------------------ grid_elig: the booleans
def synth_rules(**over):
    ids = [i for ids in ge.RULE_MAP.values() for i in ids]
    rules = [{"id": i, "name": i, "status": "PASS", "detail": ""} for i in ids]
    for r in rules:
        if r["id"] in over:
            r["status"] = over[r["id"]]
    return rules


GP_PASS = {"status": "PASS"}


def test_booleans_map_every_rule_and_keys_equal_select_candidates():
    assert ge.ELIG_KEYS == sc.ELIG_KEYS and len(ge.ELIG_KEYS) == 11
    ok = ge.booleans(synth_rules(), GP_PASS)
    assert all(ok.values()) and set(ok) == set(sc.ELIG_KEYS)
    # a double rule (D3, D5, D6) fails when either half fails
    for rid, key in (("c3.choice", "c3_D3"), ("c3.yes/no", "c3_D3"), ("c5.perm", "c5_D5"), ("c5.equiv", "c5_D5"),
                     ("c6.jagged", "c6_D6"), ("c6.opi", "c6_D6"), ("a", "a_learning"), ("d", "d_complement"), ("c7", "c7_D9")):
        b = ge.booleans(synth_rules(**{rid: "FAIL"}), GP_PASS)
        assert b[key] is False and sum(not v for v in b.values()) == 1, rid
    assert ge.booleans(synth_rules(), {"status": "FAIL"})["gproxy_rule_4_3"] is False


def test_unmeasured_or_missing_is_a_refusal_never_a_pass():
    with pytest.raises(gc.Refused, match="UNMEASURED"):
        ge.booleans(synth_rules(c4="UNMEASURED"), GP_PASS)
    with pytest.raises(gc.Refused, match="no rule"):
        ge.booleans([r for r in synth_rules() if r["id"] != "c6.opi"], GP_PASS)
    with pytest.raises(gc.Refused, match="G-proxy"):
        ge.booleans(synth_rules(), {"status": "UNMEASURED"})
    ok, bad = sc.eligible({"eligibility": {**{k: True for k in sc.ELIG_KEYS}, "c7_D9": None}})
    assert not ok and bad == ["c7_D9"]


def _gp_rows(n=2000, docs=500):
    rows = [{"id": f"r{i}", "group_id": f"g{i}", "qtype": "noul", "gold": i % 2, "meta": {"source_doc": f"d{i % docs}"}} for i in range(n)]
    return rows


def _preds(rows, wrong):
    return {r["id"]: ({"yes": 0.1, "no": 0.9} if (r["gold"] == 1) == (r["id"] in wrong) else {"yes": 0.9, "no": 0.1}) for r in rows}


def test_gproxy_rule_has_no_point_threshold_only_the_upper_bound():
    rows = _gp_rows()
    rels = []
    ref = _preds(rows, set())
    # a -1.0 pt point change with a wide interval: UB is above -0.5, so NOT rejected (4.3: there is no point threshold)
    mild = _preds(rows, {f"r{i}" for i in range(0, 2000, 100)})                      # 20 more wrong = -1.0 pt
    r = ge.gproxy_result(rows, rels, mild, ref)
    assert r["status"] == "PASS" and r["diff_pt"] == pytest.approx(-1.0) and r["ci95"][1] > -0.5
    bad = _preds(rows, {f"r{i}" for i in range(0, 2000, 20)})                         # 100 more wrong = -5 pt
    r2 = ge.gproxy_result(rows, rels, bad, ref)
    assert r2["status"] == "FAIL" and r2["ci95"][1] < -0.5
    same = ge.gproxy_result(rows, rels, ref, ref)
    assert same["status"] == "PASS" and same["diff_pt"] == 0.0 and len(same["items"]["id"]) == 2000
    assert same["items"]["correct"] == [1] * 2000
    with pytest.raises(gc.Refused, match="without a candidate"):
        ge.gproxy_result(rows, rels, {k: v for k, v in ref.items() if k != "r5"}, ref)


def test_gproxy_clusters_match_the_pilot_verdict_and_pairs_are_one_cluster():
    rows = [{"id": "a", "group_id": "ga", "meta": {"source_doc": "D1"}}, {"id": "b", "group_id": "gb", "meta": {"source_doc": "D2"}},
            {"id": "c", "group_id": "gc", "meta": {"source_doc": "D2"}}, {"id": "d", "group_id": "gd", "meta": {}}]
    rels = [{"a": "a", "b": "d", "type": "complement"}]
    lab, info = ge.gproxy_clusters(rows, rels)
    assert lab["a"] == lab["d"] and lab["b"] == lab["c"] and len({lab["a"], lab["b"]}) == 2
    assert info == {"pairs": 1, "clusters": 2, "rows_with_group_id_fallback": 1}
    sys.path.insert(0, str(C2B / "pilot_ab"))
    try:
        import verdict as pv
    except Exception:  # noqa: BLE001
        pytest.skip("pilot_ab.verdict not importable here")
    lab2, info2 = pv.clusters(rows, rels)
    assert lab == lab2 and info == info2
    with pytest.raises(gc.Refused, match="outside"):
        ge.gproxy_clusters(rows, [{"a": "a", "b": "zz", "type": "complement"}])


# ------------------------------------------------------------------------------------------------ grid_elig: the glue
def mk_meta(**over):
    m = {"base": "Qwen/Qwen3.5-4B", "host": "gcp", "gpu": "L4", "torch": "2.14", "cuda": "13.0", "layout": "schema_branch_mark",
         "style": "cygnet", "tta": False, "tta_choice": True, "tta_noul": False, "perm_seed": None,
         "load": {"revision": "r1", "chat_template_sha": "t1", "forced": []}}
    m.update(over)
    return m


def write_preds(root, split, name, preds, meta=None):
    d = root / f"preds_{split}"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.jsonl").write_text("".join(json.dumps({"id": k, "probs": v}) + "\n" for k, v in preds.items()))
    (d / f"{name}.meta.json").write_text(json.dumps(meta or mk_meta()))


def test_same_job_issues(tmp_path):
    rows = _gp_rows(10)
    for n in ("c", "r"):
        write_preds(tmp_path, "pab_gproxy", n, _preds(rows, set()))
    assert ge.same_job_issues(tmp_path, ["pab_gproxy"], "c", "r") == []
    write_preds(tmp_path, "pab_gproxy", "c", _preds(rows, set()), mk_meta(torch="2.15"))
    assert any("torch differs" in p for p in ge.same_job_issues(tmp_path, ["pab_gproxy"], "c", "r"))
    write_preds(tmp_path, "pab_gproxy", "c", _preds(rows, set()), mk_meta(tta_choice=False))
    assert any("readout" in p for p in ge.same_job_issues(tmp_path, ["pab_gproxy"], "c", "r"))
    write_preds(tmp_path, "pab_gproxy", "c", _preds(rows, set()), mk_meta(load={"revision": "r1", "chat_template_sha": "t1", "forced": [{"k": 1}]}))
    assert any("forced" in p for p in ge.same_job_issues(tmp_path, ["pab_gproxy"], "c", "r"))
    with pytest.raises(gc.Refused, match="meta.json missing"):
        ge.same_job_issues(tmp_path, ["pab_gproxy"], "c", "nothere")


def sy_rows(n, acc_c, acc_r, seed, qtype="choice", family="T28", groups=None):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        oc, orr = float(rnd.random() < acc_c), float(rnd.random() < acc_r)
        out.append({"split": "s", "id": f"r{i}", "group_id": f"g{i if groups is None else i % groups}", "source": "x", "qtype": qtype,
                    "gold": "a", "options": ["a", "b"], "family": family, "ok_c": oc, "ok_r": orr,
                    "p_c": {"a": 0.9 if oc else 0.1, "b": 0.1 if oc else 0.9}, "p_r": {"a": 0.9 if orr else 0.1, "b": 0.1 if orr else 0.9}})
    return out


def t37(n=200, viol_c=0.05, viol_r=0.15):
    rows, rels = [], []
    for i in range(n):
        a, b = f"a{i}", f"b{i}"
        rows += [{"id": a, "group_id": f"g{i}", "qtype": "noul", "p_c": {"yes": 0.8}, "p_r": {"yes": 0.8}},
                 {"id": b, "group_id": f"g{i}", "qtype": "noul", "p_c": {"yes": 0.2 + viol_c}, "p_r": {"yes": 0.2 + viol_r}}]
        rels.append({"a": a, "b": b, "type": "complement"})
    return rows, rels


def dev_json(cand, ref):
    sys.path.insert(0, str(C2B / "tests"))
    from test_gate_c2 import dev_json as dj                                    # the pre-gate's own fixture
    return dj(cand=cand, ref=ref)


@pytest.fixture
def glue(tmp_path, real_grid, monkeypatch):
    """A Run over the real fake grid with gate_c2's file loaders replaced by in-memory ones (the rules, the bootstrap and
    evaluate() are gate_c2's own)."""
    root, grid = real_grid
    lean = root / "lean"
    lean.mkdir(exist_ok=True)
    gp.record(root / "grid" / "grid.json", root / "REC.json", None, lean, now=1000.0)
    gprows = _gp_rows(300, docs=100)
    (lean / "data" / "c2_gproxy").mkdir(parents=True)
    (lean / "data" / "c2_gproxy" / "pab_gproxy.jsonl").write_text("".join(json.dumps(r) + "\n" for r in gprows))
    (lean / "data" / "c2_gproxy" / "pab_gproxy_relations.jsonl").write_text(json.dumps({"a": "r0", "b": "r1", "type": "complement"}) + "\n")
    cfg = {**gp.default_cfg(lean), "root": str(lean), "grid": str(root / "grid" / "grid.json"), "grid_record": str(root / "REC.json"),
           "ship_tpl": str(root / "ship_{cand}.json"), "latency_tpl": str(root / "lat_{cand}.json"), "d2_set": str(root / "d2.json")}
    run = ge.Run(cfg, lean)
    cand = "last3_a07"
    name = run.read_names[cand]
    for n in (name, gc.REF):
        write_preds(lean, "pab_gproxy", n, _preds(gprows, set()))
    (root / f"ship_{cand}.json").write_text("{}")
    (root / f"lat_{cand}.json").write_text(json.dumps({"cand_p50_ms": 99.0, "ref_p50_ms": 98.0, "served_path": "s1"}))
    (lean / "data" / "c2_parts").mkdir(parents=True, exist_ok=True)                 # A80 (c): the trained families come from the written mix manifest
    (lean / "data" / "c2_parts" / "c2_mix_manifest.json").write_text(json.dumps({"counts": {"by_block": {"T28": 2247, "T01": 1600, "replay": 5000}}}))
    mix = sy_rows(400, 0.9, 0.7, 1, groups=300)                                    # +20 pp: (a) passes
    tr = sy_rows(300, 0.8, 0.7, 2, groups=250)                                     # +10 pp: (b) passes
    t37_rows, rels = t37()
    dev = dev_json(name, gc.REF)
    mp = monkeypatch
    mp.setattr(gc, "check_dev", lambda *a, **k: None)
    mp.setattr(gc, "load_d2_set", lambda *a, **k: {"sources": {"x": 1}, "sources_sha256": "d2sha", "written_unix": 5.0})
    mp.setattr(gc, "d2_rows", lambda dev_rows, sources: dev_rows)
    mp.setattr(gc, "jload", lambda p, what: dev if "ship" in str(p) else json.loads(Path(p).read_text()))
    mp.setattr(g, "complete_rows", lambda splits, c, r: sy_rows(500, 0.8, 0.805, 3, groups=400))
    mp.setattr(g, "pipeline_check", lambda names, reads: ([], {}))
    mp.setattr(gc, "split_rows", lambda split, c, r, root: {gc.MIXDEV: mix, gc.TRANSFER: tr, gc.T37B_DEV: t37_rows}[split])
    mp.setattr(gc, "relations", lambda split, root: rels)
    return run, cand, name, gc.REF, mix, tr, t37_rows, rels, dev, lean, mp


def test_evaluate_one_candidate_end_to_end(glue):
    run, cand, name, ref, mix, tr, t37_rows, rels, dev, lean, mp = glue
    rec = run.evaluate(cand)
    assert rec["candidate"] == cand and rec["read_name"] == name
    assert set(rec["eligibility"]) == set(sc.ELIG_KEYS)
    assert rec["eligibility"]["a_learning"] and rec["eligibility"]["b_transfer"] and rec["eligibility"]["gproxy_rule_4_3"]
    assert rec["eligibility"]["d_complement"] and rec["eligibility"]["c7_D9"] and rec["eligible"] is True, rec["failed_checks"]
    assert set(rec["items"]) == {"gproxy", "rmixdev"} and len(rec["items"]["rmixdev"]["id"]) == 400
    assert len(rec["items"]["gproxy"]["id"]) == 300 and rec["grid_sha256"] == run.grid["grid_sha256"]
    assert "A42-D 12.2 unmet" in rec["caveat"]
    assert sc.eligible(rec) == (True, []) and sc.components_of(rec) == ("gproxy", "rmixdev")
    out = Path(run.root).parent / "out"
    assert ge.write_once(out, rec) == "written" and ge.write_once(out, rec) == "unchanged"
    with pytest.raises(gc.Refused, match="other inputs"):
        ge.write_once(out, {**rec, "inputs_sha256": "different"})


def test_a80_untrained_family_rows_are_report_only_for_rule_a_and_the_r_term(glue):
    run, cand, name, ref, mix, tr, t37_rows, rels, dev, lean, mp = glue
    off = sy_rows(300, 0.30, 0.75, 9, family="T33", groups=250)                    # a family that left the mix: C2 is worse than C1 on it
    for x in off:
        x["id"], x["group_id"] = "T33_" + x["id"], "T33_" + x["group_id"]
    mp.setattr(gc, "split_rows", lambda split, c, r, root: {gc.MIXDEV: mix + off, gc.TRANSFER: tr, gc.T37B_DEV: t37_rows}[split])
    rec = run.evaluate(cand)
    assert rec["eligibility"]["a_learning"] is True and rec["trained_families"] == ["T01", "T28"]      # the T33 rows would have sunk rule (a)
    assert len(rec["items"]["rmixdev"]["id"]) == 400 and not any(i.startswith("T33_") for i in rec["items"]["rmixdev"]["id"])
    ro = rec["report_only"]["mixdev_trained_families"]
    assert ro["report_only_families"] == ["T33"] and ro["report_only_rows"] == 300 and ro["label"] == "family not trained in C2"
    (lean / "data" / "c2_parts" / "c2_mix_manifest.json").write_text(json.dumps({"counts": {"by_block": {"T28": 1, "T33": 88}}}))
    rec2 = run.evaluate(cand)
    assert rec2["eligibility"]["a_learning"] is False and len(rec2["items"]["rmixdev"]["id"]) == 700 and rec2["inputs_sha256"] != rec["inputs_sha256"]   # T33 trained: its 300 rows count
    os.remove(lean / "data" / "c2_parts" / "c2_mix_manifest.json")
    with pytest.raises(gc.Refused, match="mix manifest"):
        run.evaluate(cand)


def test_a_failing_gate_rule_makes_the_candidate_ineligible_and_names_it(glue):
    run, cand, name, ref, mix, tr, t37_rows, rels, dev, lean, mp = glue
    weak = sy_rows(300, 0.72, 0.7, 2, groups=250)                                  # +2 pp: (b) fails
    mp.setattr(gc, "split_rows", lambda split, c, r, root: {gc.MIXDEV: mix, gc.TRANSFER: weak, gc.T37B_DEV: t37_rows}[split])
    rec = run.evaluate(cand)
    assert rec["eligible"] is False and rec["failed_checks"] == ["b_transfer"]


def test_missing_latency_ship_json_or_reads_refuse(glue, tmp_path):
    run, cand, name, ref, mix, tr, t37_rows, rels, dev, lean, mp = glue
    os.remove(run.inputs_for(cand)["latency"])
    def jl(p, what):
        if "ship" in str(p):
            return dev
        if not Path(p).exists():
            raise gc.Refused(f"{what}: {p} missing or not JSON")
        return json.loads(Path(p).read_text())
    mp.setattr(gc, "jload", jl)
    with pytest.raises(gc.Refused, match="latency record"):
        run.evaluate(cand)
    (Path(run.root).parent / "lat_last3_a07.json").write_text(json.dumps({"cand_p50_ms": 99.0, "ref_p50_ms": 98.0, "served_path": "s1"}))
    mp.setattr(g, "pipeline_check", lambda names, reads: (["torch is not one value"], {}))
    with pytest.raises(gc.Refused, match="one clean predict job"):
        run.evaluate(cand)


def test_check_once_needs_the_record_the_stop_rule_refparity_and_an_early_d2_set(glue):
    run, cand, name, ref, mix, tr, t37_rows, rels, dev, lean, mp = glue
    root = Path(run.root).parent
    mp.setattr(gc, "check_stop_rule", lambda *a, **k: {"reads": [0.25, 0.5, 0.75]})
    mp.setattr(gc, "check_refparity", lambda *a, **k: {"agree": 1.0})
    (root / "d2.json").write_text(json.dumps({"sources_sha256": "x", "written_unix": 500.0}))
    snap = (root / "a", root / "b", root / "c")
    info = run.check_once(snap)
    assert info["d2_set_sha256"] == "x" and info["stop_rule"]["reads"]
    (root / "d2.json").write_text(json.dumps({"sources_sha256": "x", "written_unix": 2000.0}))
    touch(Path(run.root) / "preds_dev" / f"{name}.jsonl", 1500.0)                    # a grid read older than the D2 set
    with pytest.raises(gc.Refused, match="D2 set was written after the first grid read"):
        run.check_once(snap)
    (Path(run.root) / "preds_dev" / f"{name}.jsonl").unlink()
    mp.setattr(gc, "check_stop_rule", lambda *a, **k: (_ for _ in ()).throw(gc.Refused("the stop rule fired")))
    with pytest.raises(gc.Refused, match="stop rule fired"):
        run.check_once(snap)
    mp.setattr(gc, "check_stop_rule", lambda *a, **k: {"reads": []})
    (root / "REC.json").unlink()
    with pytest.raises(gc.Refused, match="grid record"):
        run.check_once(snap)


def test_status_lists_what_is_missing(glue):
    run = glue[0]
    st = ge.status(run)
    assert len(st) == 18 and st[0]["reads"].startswith("0/") and st[0]["ship_json"] is False
    assert "c2_mixdev" in st[0]["missing_reads"]


def test_the_eligibility_cli_refuses_ohs_paths_and_never_runs_gate_jobs(tmp_path, capsys):
    bad = tmp_path / "ohs_cfg.json"
    bad.write_text("{}")
    assert ge.main(["status", "--cfg", str(bad)]) == 2 and "REFUSED" in capsys.readouterr().out
    src = Path(ge.__file__).read_text() + Path(gp.__file__).read_text() + Path(sr.__file__).read_text()
    assert "import g13" not in src and "g13_c2.py" not in src and "decontam_g13" not in src
    assert "subprocess" not in src and "os.system" not in src


# ------------------------------------------------------------------------------------------------ symmetrisation: flips
class FakeFlipper:
    """flips every row whose id ends with an even digit"""

    def flip(self, item):
        if int(item["id"][-1]) % 2:
            return None
        return {**item, "id": item["id"] + "::flip", "instructions": "NOT " + item["instructions"], "gold": 1 - int(item["gold"])}


def sym_tree(tmp_path):
    root = tmp_path / "lean"
    (root / "data" / "c2_gproxy").mkdir(parents=True)
    for sp in sr.SPLITS9:
        rows = [{"id": f"{sp}{i}", "group_id": f"g{sp}{i}", "qtype": "noul" if i % 3 else "choice", "source": "src" if i < 5 else "tb_mixtral",
                 "gold": i % 2, "instructions": f"Q {i}?", "state": "s", "options": None} for i in range(6)]
        (root / "data" / f"{sp}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    gpr = [{"id": f"gp{i}", "group_id": f"gg{i}", "qtype": "noul", "gold": i % 2, "instructions": f"G {i}?", "state": "s", "card": "",
            "role": "base" if i < 4 else "complement", "source": "gp_x", "options": None} for i in range(8)]
    (root / "data" / "c2_gproxy" / "pab_gproxy.jsonl").write_text("".join(json.dumps(r) + "\n" for r in gpr))
    rel = [{"a": f"gp{i}", "b": f"gp{i + 4}", "pair_id": f"gp_pair:{i:03d}", "pattern": f"H:P{i}", "type": "complement"} for i in range(4)]
    (root / "data" / "c2_gproxy" / "pab_gproxy_relations.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rel))
    return root


def test_catalogue_flipper_reads_the_real_field_name_and_swaps_the_card():
    f = sy.CatalogueFlipper()
    row = {"id": "x", "instructions": "Read the record. Does the airport have an airline code?", "gold": 1, "qtype": "noul",
           "card": "- yes: The IATA code field is filled.\n- no: The IATA code field is empty."}
    out = f.flip(row)
    assert out and out["id"] == "x::flip" and "instructions" in out and out["instructions"].startswith("Read the record. ")
    assert out["instructions"] != row["instructions"] and out["gold"] == 0 and out["flip_of"] == "x"
    assert out["card"] == "- yes: The IATA code field is empty.\n- no: The IATA code field is filled."
    # the test-fixture spelling still works
    assert f.flip({"id": "a", "instruction": "Read the policy. Does the vendor allow refunds after 30 days?"})["id"] == "a::flip"
    assert f.flip({"id": "n", "instructions": "Summarise the policy."}) is None


def test_items_are_staged_outside_data_and_counts_are_exact(tmp_path):
    root = sym_tree(tmp_path)
    with pytest.raises(sr.Refused, match="outside data/"):
        sr.write_items(root, root / "data" / "staged", FakeFlipper())
    man = sr.write_items(root, tmp_path / "stage", FakeFlipper())
    d1 = 9 * 3                                        # per split rows 1,2,4,5 are noul; rows >= 5 are tb_mixtral: 1,2,4 kept
    assert man["sets"]["d1_yesno"] == 9 * 3 and man["sets"]["gproxy"] == 8 and man["pairs"] == 4
    flips = [json.loads(x) for x in (tmp_path / "stage" / "sym_flip.jsonl").read_text().splitlines()]
    ids = [f["id"] for f in flips]
    assert len(ids) == len(set(ids)) == man["flip_rows"] and all(i.endswith("::flip") for i in ids)
    assert man["flipped"]["d1_yesno"] + man["flipped"]["gproxy"] == len(flips)
    assert man["no_flip_ids"] == man["sets"]["d1_yesno"] + man["sets"]["gproxy"] - len(flips)
    assert all(f["split"] == sr.FLIP_SPLIT for f in flips)
    assert json.loads((tmp_path / "stage" / "trained_pids.json").read_text()) and not any(p.startswith("H:") for p in sr.trained_pids())


def test_records_join_calibration_and_pairs_feed_adopt(tmp_path):
    root = sym_tree(tmp_path)
    it = sr.build_items(root, FakeFlipper())
    name = "q35_4b_c2grid_x"
    rnd = random.Random(0)
    for sp in (*sr.SPLITS9, sr.GPROXY_SPLIT):
        rows = [json.loads(x) for x in (root / "data" / (f"{sp}.jsonl" if sp != sr.GPROXY_SPLIT else "c2_gproxy/pab_gproxy.jsonl")).read_text().splitlines()]
        write_preds(root, sp, name, {r["id"]: {"yes": rnd.random(), "no": 0.0} for r in rows if r["qtype"] == "noul"})
    write_preds(root, sr.FLIP_SPLIT, name, {f["id"]: {"yes": rnd.random(), "no": 0.0} for f in it["flips"].values()})
    recs = sr.build_records(root, name, it, "select")
    sets = {s: [r for r in recs if r["set"] == s] for s in ("d1_yesno", "gproxy", "pair", "calib")}
    assert len(sets["d1_yesno"]) == 27 and len(sets["gproxy"]) == 8 and len(sets["pair"]) == 8
    assert all(r["p_flip"] is None for r in sets["d1_yesno"] if r["id"] not in it["flips"])
    assert sum(r["p_flip"] is not None for r in sets["d1_yesno"]) == sum(r["id"] in it["flips"] for r in it["d1"])
    assert {r["role"] for r in sets["pair"]} == {"q", "nq"} and all(r["pattern_id"].startswith("H:") for r in sets["pair"])
    assert all(g.half(next(x for x in it["d1"] if x["id"] == r["id"])["group_id"]) == "select" for r in sets["calib"])
    assert not [r for r in sr.build_records(root, name, it, "none") if r["set"] == "calib"]
    res = sy.adopt(recs, {"c1_p50_ms": 100.0, "sym_p50_ms": 104.0}, trained_pids=set(sr.trained_pids()))
    assert set(res["checks"]) >= {"violation_drop", "gproxy_acc", "d1_yesno_acc", "d9_latency"} and res["pairs"] == 4
    # a missing flip prediction is a refusal, not a silent unsymmetrised row
    d = root / f"preds_{sr.FLIP_SPLIT}" / f"{name}.jsonl"
    lines = d.read_text().splitlines()
    d.write_text("\n".join(lines[1:]) + "\n")
    with pytest.raises(sr.Refused, match="no flip-q prediction"):
        sr.build_records(root, name, it, "select")


def test_missing_reads_refuse(tmp_path):
    root = sym_tree(tmp_path)
    with pytest.raises(sr.Refused, match="no preds"):
        sr.build_records(root, "nothere", sr.build_items(root, FakeFlipper()))


# ------------------------------------------------------------------------------------------------ symmetrisation: latency
def test_latency_measures_one_call_per_decision_and_pairs_share_the_call():
    calls, t = [], [0.0]

    def read_fn(batch):
        calls.append([b["id"] for b in batch])
        t[0] += 0.010 if len(batch) == 1 else 0.0105            # +5% for the shared-prefix pair

    clock = lambda: t[0]  # noqa: E731
    rows = [{"id": f"a{i}"} for i in range(40)]
    flips = {r["id"]: {"id": r["id"] + "::flip"} for r in rows}
    plain = sr.measure(read_fn, rows, flips, "plain", warmup=5, clock=clock)
    n_plain = len(calls)
    sym = sr.measure(read_fn, rows, flips, "sym", warmup=5, clock=clock)
    assert plain["p50_ms"] == pytest.approx(10.0) and sym["p50_ms"] == pytest.approx(10.5) and sym["n_with_flip"] == 40
    assert all(len(c) == 2 for c in calls[n_plain + 5:]) and plain["n_with_flip"] == 0
    # items without a flip are served plain on the sym path
    sym2 = sr.measure(read_fn, rows, {}, "sym", warmup=0, clock=clock)
    assert sym2["n_with_flip"] == 0 and sym2["p50_ms"] == pytest.approx(10.0)
    with pytest.raises(ValueError):
        sr.measure(read_fn, rows, flips, "other")


def test_latency_join_requires_one_served_path_and_one_item_set():
    p = {"mode": "plain", "p50_ms": 100.0, "served_path": "s1", "items_sha256": "i"}
    s = {"mode": "sym", "p50_ms": 104.0, "served_path": "s1", "items_sha256": "i"}
    j = sr.join_latency(p, s)
    assert j["c1_p50_ms"] == 100.0 and j["sym_p50_ms"] == 104.0 and j["ratio"] == 1.04
    assert sy.adopt([], j)["adopt"] is False                                         # shape accepted by symmetrise.adopt (no records)
    for bad in ({**s, "served_path": "other"}, {**s, "items_sha256": "j"}, {**s, "mode": "plain"}):
        with pytest.raises(sr.Refused):
            sr.join_latency(p, bad)
    assert sr.percentile([1, 2, 3, 4, 5], 0.5) == 3 and sr.percentile([1, 2], 0.95) == pytest.approx(1.95)
