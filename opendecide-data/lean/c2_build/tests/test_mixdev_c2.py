"""Tests for mixdev_c2.py (the merged C2 mixdev writer and the predict-job manifests; spec 7.1, A39 h, A62). Synthetic trees in a
temp folder; the only real-file reads are two read-only smoke checks of the row form. Nothing is written into data/, no G13 tool
is imported or run, no OHS / sealed path is opened. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_mixdev_c2.py
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import c2io  # noqa: E402
import gate_c2 as gc  # noqa: E402
import mixdev_c2 as md  # noqa: E402


# ------------------------------------------------------------------------------------------------------------- fixtures
def mrow(fam, i, *, qtype="noul", unit=None, sampler="S5", prefix=None):
    p = prefix or fam.lower()
    unit = i if unit is None else unit
    r = {"id": f"{p}:r{i}", "group_id": f"{p}:g{unit}", "call_id": f"{p}:c{unit}", "source": p, "state": f"state {i}",
         "qtype": qtype, "instructions": "q", "options": None if qtype == "noul" else ["a", "b", "c"],
         "gold": (i % 2) if qtype == "noul" else "a", "role": "base", "card": None,
         "meta": {"family": fam, "sampler": sampler, "dev_only": True, "card_id": f"{fam}:S5:c{i}"}}
    return r


def jl_write(p: Path, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture
def lean(tmp_path):
    assert c2io.refusal(tmp_path) is None
    return tmp_path


def make_family(lean: Path, fam: str, n: int, *, qc: bool = True, cand: int = 5, units_of: int = 1, sampler="S5", extra_cand=None):
    f = md.fam_paths(fam, lean)
    rows = [mrow(fam, i, qtype="choice" if i % 3 == 0 else "noul", unit=i // units_of, sampler=sampler) for i in range(n)]
    msha = jl_write(f["mixdev"], rows)
    crows = [mrow(fam, 10_000 + i, prefix=fam.lower() + "t", sampler="S1") for i in range(cand)] + (extra_cand or [])
    csha = jl_write(f["cand"], crows)
    rsha = jl_write(f["rel"], [])
    f["manifest"].parent.mkdir(parents=True, exist_ok=True)
    f["manifest"].write_text(json.dumps({"family": fam, "mixdev": {"mixdev_S5.jsonl": {"sha256": msha, "rows": n}}}))
    if qc:
        f["qc"].parent.mkdir(parents=True, exist_ok=True)
        f["qc"].write_text(json.dumps({"pass": True, "passed_utc": "2026-10-16T06:00:00+00:00", "fix_iterations": 0, "family": fam,
                                       "files": {f["cand"].name: {"sha256": csha, "rows": cand}, f["rel"].name: {"sha256": rsha, "rows": 0}},
                                       "mixdev": {"mixdev_S5.jsonl": {"sha256": msha, "rows": n}}}))
    return rows


def build(lean, **kw):
    return md.build(c2io.C2InputLog(), lean, **kw)


# -------------------------------------------------------------------------------------------------------------- layout
@pytest.mark.parametrize("fam", ["T28", "T01", "T25", "F5", "F6", "F11", "F4", "GB", "SB5"])
def test_fam_paths_agree_with_c2io(fam):
    mine, theirs = md.fam_paths(fam), c2io.fam_files(fam)
    assert mine["mixdev"] == theirs["mixdev"] and mine["cand"] == theirs["cand"] and mine["qc"] == theirs["qc"]
    assert mine["manifest"] == theirs["manifest"]


def test_scope_follows_the_rulings():
    assert "T27" in md.TRAINED_PROGRAM and md.REPORT_ONLY_FAMILIES == ("T27",)        # A62 b
    assert set(md.CARRY_FULL) == {"F5", "F6", "F11"} and md.PER_FAMILY == 150           # spec 7.1
    assert "GB" in md.REPORT_BLOCKS and not set(md.REPORT_BLOCKS) & set(md.TRAINED_PROGRAM)   # A39 h
    assert not set(c2io.TRANSFER_DEV) & set(md.SCOPE)


# ------------------------------------------------------------------------------------------------------------ row checks
def test_row_problems_clean_and_each_fault():
    ok = [mrow("T28", i, qtype="choice" if i % 2 else "noul") for i in range(6)]
    assert md.row_problems("T28", ok) == []
    cases = {
        "duplicate id": lambda r: r.__setitem__("id", ok[0]["id"]),
        "meta.family": lambda r: r["meta"].__setitem__("family", "T29"),
        "not an S5": lambda r: r["meta"].update(sampler="S1", dev_only=False),
        "private key": lambda r: r.__setitem__("_x", 1),
        "noul gold": lambda r: r.__setitem__("gold", 2),
        "noul gold bool": lambda r: r.__setitem__("gold", True),
        "qtype": lambda r: r.__setitem__("qtype", "free"),
    }
    for want, mut in cases.items():
        rows = [json.loads(json.dumps(r)) for r in ok]
        mut(rows[2] if want != "duplicate id" else rows[3])
        out = md.row_problems("T28", rows)
        assert out, want
    rows = [json.loads(json.dumps(r)) for r in ok]
    ch = next(r for r in rows if r["qtype"] == "choice")
    ch["gold"] = "zzz"
    assert any("choice gold" in p for p in md.row_problems("T28", rows))
    rows = [{"id": "x"}]
    assert any("missing" in p for p in md.row_problems("T28", rows))
    rows = [mrow("T28", 1) | {"meta": "no"}]
    assert any("meta object" in p for p in md.row_problems("T28", rows))


def test_disjoint_problems():
    rows = [mrow("T28", i) for i in range(3)]
    assert md.disjoint_problems("T28", rows, [mrow("T28", 99, prefix="x")]) == []
    cand = [mrow("T28", 1, prefix="x") | {"group_id": rows[0]["group_id"]}]
    out = md.disjoint_problems("T28", rows, cand)
    assert len(out) == 1 and "group_id" in out[0]
    assert len(md.disjoint_problems("T28", rows, rows[:1])) == 3                         # id, group_id, call_id


def test_recorded_sha_problems(tmp_path):
    p = tmp_path / "mixdev_S5.jsonl"
    p.write_text("x\n")
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    good = {"mixdev": {"mixdev_S5.jsonl": {"sha256": sha}}}
    probs, rec = md.recorded_sha_problems("T01", p, good, good)
    assert probs == [] and rec["recorded"] and rec["qc_record"] == sha
    probs, _ = md.recorded_sha_problems("T01", p, {"mixdev": {"mixdev_S5.jsonl": {"sha256": "0" * 64}}}, None)
    assert len(probs) == 1 and "stale" in probs[0]
    probs, rec = md.recorded_sha_problems("F5", p, None, {"outputs": {"mixdev": {"mixdev_S5.jsonl": {"sha256": "1" * 64}}}})
    assert len(probs) == 1                                                                 # deep search on a carry-over manifest
    probs, rec = md.recorded_sha_problems("F5", p, None, {"outputs": {"relations": {"mixdev_S5.relations.jsonl": {"sha256": "1" * 64}}}})
    assert probs == [] and rec["recorded"] is False                                       # a relations sha is not the mixdev's


# ------------------------------------------------------------------------------------------------------------- selection
def test_components_join_group_and_call_ids():
    rows = [mrow("T28", 0, unit=0), mrow("T28", 1, unit=0), mrow("T28", 2, unit=1)]
    rows[2]["call_id"] = rows[0]["call_id"]                         # joins unit 1 to unit 0 through the call id
    rows.append(mrow("T28", 3, unit=7))
    comp = md.components(rows)
    assert sorted(len(v) for v in comp.values()) == [1, 3]


def test_pick_units_whole_units_cap_and_determinism():
    rows = [mrow("T28", i, unit=i // 4) for i in range(400)]        # 100 units of 4
    a, info = md.pick_units("T28", rows, 150)
    b, _ = md.pick_units("T28", rows, 150)
    assert a == b and info["truncated"] and len(a) == 148            # 37 whole units of 4; 38 would be 152 > 150
    assert len({r["group_id"] for r in a}) * 4 == len(a)
    assert [r["id"] for r in a] == sorted((r["id"] for r in a), key=lambda s: int(s.split("r")[-1]))      # source order kept
    other, _ = md.pick_units("T29", rows, 150)
    assert [r["id"] for r in other] != [r["id"] for r in a]          # the family name seeds the order
    assert md.pick_units("T28", rows, 150, seed=1)[0] != a
    exact, info = md.pick_units("T28", rows[:150], 150)
    assert exact == rows[:150] and not info["truncated"]
    short, info = md.pick_units("T28", rows[:140], 150)
    assert short == rows[:140] and not info["truncated"]             # a shortfall is never refilled


def test_pick_units_fills_to_exactly_n_when_units_are_single_rows():
    rows = [mrow("T01", i) for i in range(900)]
    out, _ = md.pick_units("T01", rows, 150)
    assert len(out) == 150 and len({r["id"] for r in out}) == 150


# --------------------------------------------------------------------------------------------------------------- build
def test_build_rules_trained_vs_report_only(lean):
    make_family(lean, "T28", 400, units_of=5)
    make_family(lean, "T33", 141)
    make_family(lean, "T27", 150)
    make_family(lean, "F5", 400)
    make_family(lean, "F4", 700)
    make_family(lean, "GB", 1650)
    make_family(lean, "T31", 150)                                      # exists but is not entered below
    res = build(lean, families=["T28", "T33", "T27", "F5", "F4", "GB"])
    assert res["problems"] == []
    by = res["report"]["main_by_family"]
    assert by == {"T28": 150, "T33": 141, "F5": 400, "F4": 150}        # F5 whole; F4 capped at 150; T33 keeps its 141
    fams = {r["meta"]["family"] for r in res["main"]}
    assert fams == {"T28", "T33", "F5", "F4"}                          # no T27 (A62), no GB (A39 h), no T31 (not entered)
    assert {r["meta"]["family"] for r in res["report_only"]} == {"T27", "GB"}
    assert res["report"]["shortfalls"] == {"T33": 9}
    assert res["report"]["report_only"]["GB"]["rows_out"] == 1650
    assert res["report"]["main_rows"] == len(res["main"])
    order = []
    for r in res["main"]:
        if not order or order[-1] != r["meta"]["family"]:
            order.append(r["meta"]["family"])
    assert order == ["T28", "T33", "F5", "F4"]                         # c2io.PROGRAM order, then the carry-over pools


def test_build_is_deterministic_and_rows_unchanged(lean):
    src = make_family(lean, "T28", 150)
    a = build(lean, families=["T28"])
    b = build(lean, families=["T28"])
    assert a["main"] == b["main"] == src                              # taken as generated: no edit, no relabel, no re-order
    assert [json.dumps(r) for r in a["main"]] == [json.dumps(r) for r in src]


def test_entered_family_without_mixdev_is_a_problem(lean):
    make_family(lean, "T28", 150)
    md.fam_paths("T28", lean)["mixdev"].unlink()
    res = build(lean, families=["T28"])
    assert any("no mixdev file" in p for p in res["problems"])


def test_stale_qc_record_is_a_problem(lean):
    make_family(lean, "T28", 150)
    p = md.fam_paths("T28", lean)["mixdev"]
    rows = [json.loads(x) for x in p.read_text().splitlines()]
    rows[0]["state"] = "edited after the QC record"
    jl_write(p, rows)
    res = build(lean, families=["T28"])
    assert any("stale record" in x for x in res["problems"])


def test_candidate_overlap_and_bad_rows_are_problems(lean):
    make_family(lean, "T28", 150)
    f = md.fam_paths("T28", lean)
    rows = [json.loads(x) for x in f["mixdev"].read_text().splitlines()]
    jl_write(f["cand"], [rows[0]])                                     # a mixdev row sitting in the candidates
    res = build(lean, families=["T28"])
    assert any("also candidate" in x for x in res["problems"])
    make_family(lean, "T29", 150, sampler="S1")
    f = md.fam_paths("T29", lean)
    rs = [json.loads(x) for x in f["mixdev"].read_text().splitlines()]
    for r in rs:
        r["meta"]["dev_only"] = False
    jl_write(f["mixdev"], rs)
    assert any("not an S5" in x for x in build(lean, families=["T29"])["problems"])


def test_ids_and_groups_must_not_collide_across_families(lean):
    make_family(lean, "T28", 150)
    make_family(lean, "T29", 150)
    f = md.fam_paths("T29", lean)
    rs = [json.loads(x) for x in f["mixdev"].read_text().splitlines()]
    rs[0]["id"] = "t28:r1"
    rs[1]["group_id"] = "t28:g2"
    jl_write(f["mixdev"], rs)
    out = build(lean, families=["T28", "T29"])["problems"]
    assert any("occur twice" in x for x in out) and any("shared by two families" in x for x in out)


def test_transfer_dev_must_be_disjoint_from_mixdev(lean):
    make_family(lean, "T28", 150)
    jl_write(lean / "data" / "c2_transfer_dev.jsonl", [mrow("T28", 1, prefix="t28") | {"id": "t28:r1"}])
    assert any("transfer dev share" in x for x in build(lean, families=["T28"])["problems"])


def test_unknown_family_and_entered_from(lean, tmp_path):
    with pytest.raises(md.Problem):
        build(lean, families=["T36"])                                  # transfer-dev family: never a mixdev block
    make_family(lean, "T28", 150)
    make_family(lean, "T29", 150)
    rep = tmp_path / "mix_dry.json"
    rep.write_text(json.dumps({"entry": {"entered": ["T29", "GW"], "left_out": {"T28": ["cut"]}}}))
    res = build(lean, entered_from=rep)
    assert res["report"]["trained_families"] == ["T29"] and res["report"]["entry"]["source"] == "mix report"
    assert res["report"]["entry"]["left_out"] == {"T28": ["cut"]}
    rep.write_text(json.dumps({"nothing": 1}))
    with pytest.raises(md.Problem):
        build(lean, entered_from=rep)


def test_admission_entry_uses_the_mix_test(lean):
    make_family(lean, "T28", 150)
    make_family(lean, "T29", 150, qc=False)
    make_family(lean, "T30", 150)
    q = md.fam_paths("T30", lean)["qc"]
    d = json.loads(q.read_text())
    d["passed_utc"] = "2026-10-23T00:00:00+00:00"                      # after the cutoff
    q.write_text(json.dumps(d))
    make_family(lean, "T32", 150)
    q = md.fam_paths("T32", lean)["qc"]
    d = json.loads(q.read_text())
    d["files"]["candidates_c2.jsonl"]["sha256"] = "0" * 64              # stale pass
    q.write_text(json.dumps(d))
    entered, left, src = md.entered_set(c2io.C2InputLog(), lean)
    assert entered == ["T28"]
    assert "no QC_REPORT.json" in " ".join(left["T29"]) and "cutoff" in " ".join(left["T30"]) and "T32" in left
    assert left["T01"] == ["no candidates on disk"]
    assert src["source"].startswith("mix_c2.admission")


def test_new_family_own_dev_is_not_merged(lean):
    make_family(lean, "T28", 150)
    res = build(lean, families=["T28"])
    assert res["report"]["excluded"]["own_dev_families_entered"] is None
    assert all(b not in res["report"]["trained_families"] for b in md.OWN_DEV_FAMILIES)


# -------------------------------------------------------------------------------------------------------------- writers
def test_write_build_and_verify(lean, tmp_path):
    make_family(lean, "T28", 150)
    make_family(lean, "T27", 150)
    out = lean / "c2_build" / "staged" / "mixdev"
    res = build(lean, families=["T28"])
    info = md.write_build(res, out, md.PlainWriter(), lean)
    for n in (md.MAIN, md.REPORT_ONLY):
        p = out / n
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        assert (out / f"{n}.sha256").read_text() == f"{sha}  {n}\n"
    rpt = json.loads((out / md.BUILD_REPORT).read_text())
    assert rpt["staged"]["main"]["sha256"] == info["main"]["sha256"] and rpt["staged"]["main"]["rows"] == 150
    assert {"predict_c2_mixdev.json", "predict_c2_mixdev_report.json", "predict_c2_t37b_dev.json", "predict_pab_gproxy.json",
            "predict_jobs_index.json"} <= set(info["manifests"])
    assert md.verify(out, lean) == []
    (out / md.MAIN).write_text("tampered\n")
    assert any("differs" in x for x in md.verify(out, lean))
    assert not (lean / "data" / md.MAIN).exists()                      # nothing is written into data/


def test_out_dir_under_data_is_refused(lean):
    with pytest.raises(md.Problem):
        md.check_out_dir(lean / "data", lean)
    with pytest.raises(md.Problem):
        md.check_out_dir(lean / "data" / "x" / "y", lean)
    assert md.check_out_dir(lean / "c2_build" / "staged" / "mixdev", lean)
    with pytest.raises(md.Problem):
        md.check_out_dir(md.LEAN / "data", md.LEAN)
    assert md.main(["build", "--families", "T28", "--out-dir", str(md.LEAN / "data" / "zz")]) == 2


def test_guarded_writer_refuses_never_open_and_outside_lean(tmp_path):
    w = md.GuardedWriter()
    with pytest.raises(c2io.C2Refused):
        w.text(md.LEAN / "c2_build" / "staged" / "ohs_x" / "a.txt", "x")
    with pytest.raises(PermissionError):
        w.text(tmp_path / "a.txt", "x")
    assert not (tmp_path / "a.txt").exists()


def test_module_never_imports_or_runs_g13():
    tree = ast.parse(Path(md.__file__).read_text())
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            mods.add(n.module)
    assert not {m for m in mods if m and ("g13" in m or "decontam" in m)}
    src = Path(md.__file__).read_text()
    assert "subprocess" not in src and "os.system" not in src


# ------------------------------------------------------------------------------------------------------------- manifests
def staged_lean(lean):
    make_family(lean, "T28", 150)
    out = lean / "c2_build" / "staged" / "mixdev"
    md.write_build(build(lean, families=["T28"]), out, md.PlainWriter(), lean)
    return out


def test_manifests_name_the_gate_splits_and_reads(lean):
    out = staged_lean(lean)
    ms = md.mixdev_manifests(out, lean)
    m = ms["predict_c2_mixdev.json"]
    assert m["set"] == gc.MIXDEV == "c2_mixdev" and m["gate_input"] and not m["report_only"]
    assert m["data"]["rows"] == 150 and m["data"]["sha256"] == hashlib.sha256((out / md.MAIN).read_bytes()).hexdigest()
    assert m["data"]["install_to"] == "data/c2_mixdev.jsonl" and "staged" in m["data"]["staged"]
    assert [x["model"] for x in m["models"]] == [gc.CAND, gc.REF]
    for r in m["reads"]:
        assert r["preds"] == f"preds_c2_mixdev/{r['model']}.jsonl" and "od_gcp.py predict" in r["command"]
        assert md.sm.REV in r["command"] and "--tta" not in r["command"]
    assert any("--tag _c2" in r["command"] and "--name q35_4b_main500k " in r["command"] for r in m["reads"])      # REF = C1 + tag _c2
    assert any(f"--name {gc.CAND} " in r["command"] and "--tag" not in r["command"] for r in m["reads"])
    assert m["vm"]["verify"].startswith("cd ~/lean/data") and m["data"]["sha256"] in m["vm"]["verify"]
    assert "snapshot_reads_report_only" in m and "never a candidate" in m["snapshot_reads_report_only"]["rule"]
    rep = ms["predict_c2_mixdev_report.json"]
    assert rep["report_only"] and not rep["gate_input"] and "snapshot_reads_report_only" not in rep and rep["set"] == md.REPORT_SPLIT
    idx = ms["predict_jobs_index.json"]
    assert set(gc.SPLITS9) <= set(idx["gate_job"]["splits"]) and gc.MIXDEV in idx["gate_job"]["splits"]
    assert gc.TRANSFER in idx["gate_job"]["splits"] and gc.T37B_DEV in idx["gate_job"]["splits"]
    assert md.GPROXY_SPLIT not in idx["gate_job"]["splits"] and md.REPORT_SPLIT not in idx["gate_job"]["splits"]
    for c in idx["gate_job"]["commands"]:
        assert "--splits dev_nc," in c and "--tta" not in c
    assert "snapshot" in idx["snapshot_reads"] or "25" in idx["snapshot_reads"]


def test_transfer_dev_manifest_when_present(lean):
    out = staged_lean(lean)
    jl_write(lean / "data" / "c2_transfer_dev.jsonl", [mrow("T19", i, prefix="t19") for i in range(4)] + [mrow("T21", i, prefix="t21") for i in range(2)])
    m = md.mixdev_manifests(out, lean)["predict_c2_transfer_dev.json"]
    assert m["set"] == gc.TRANSFER and m["gate_input"] and m["data"]["families"] == {"T19": 4, "T21": 2} and m["data"]["staged"] is None
    assert m["status"] == "frozen in data/"


def test_t37b_manifest_pending_then_staged_then_problems(lean):
    out = staged_lean(lean)
    m = md.mixdev_manifests(out, lean)["predict_c2_t37b_dev.json"]
    assert m["status"].startswith("pending") and m["expected"]["pairs"] == 300 and m["set"] == gc.T37B_DEV
    s = lean / "c2_build" / "staged" / "t37bdev"
    rows, rels = [], []
    for i in range(300):
        a, b = mrow("T37b", 2 * i, unit=i, prefix="a"), mrow("T37b", 2 * i + 1, unit=i, prefix="b")
        rows += [a, b]
        rels.append({"a": a["id"], "b": b["id"], "type": "complement"})
    jl_write(s / "c2_t37b_dev.jsonl", rows)
    jl_write(s / "c2_t37b_dev_relations.jsonl", rels)
    m = md.mixdev_manifests(out, lean)["predict_c2_t37b_dev.json"]
    assert m["status"] == "staged" and m["relations"]["pairs"] == 300 and m["gate_input"] and m["data"]["rows"] == 600
    assert m["data"]["staged"].endswith("c2_t37b_dev.jsonl") and "push_relations" in m["vm"]
    assert m["reads"][0]["preds"] == "preds_c2_t37b_dev/q35_4b_c2.jsonl"
    jl_write(s / "c2_t37b_dev_relations.jsonl", rels[:299] + [{"a": "nope", "b": rels[0]["b"], "type": "complement"}])
    m = md.mixdev_manifests(out, lean)["predict_c2_t37b_dev.json"]
    assert m["status"] == "staged with problems" and any("point at missing" in n for n in m["notes"]) and any("299" in n or "300" in n for n in m["notes"])
    (s / "c2_t37b_dev_relations.jsonl").unlink()
    m = md.mixdev_manifests(out, lean)["predict_c2_t37b_dev.json"]
    assert any("relations.jsonl missing" in n for n in m["notes"])


def test_gproxy_manifest_pins_and_the_label():
    m = md.gproxy_manifest(md.LEAN)                                     # frozen files: hashing only
    assert m["set"] == "pab_gproxy" and m["status"] == "frozen in data/c2_gproxy", m["notes"]
    assert m["data"]["sha256"] == m["data"]["pinned_sha256"] and m["c1_read"]["exists"]
    assert "UNMET" in m["role"] and "NOT a ship rule" in m["role"] and not m["gate_input"]
    assert "--tag _pab" in m["reads"][0]["command"] and "fast_read.py predict" in m["reads"][0]["command"]
    assert m["reads"][0]["preds"] == "preds_pab_gproxy/q35_4b_c2_pab.jsonl"


def test_gproxy_manifest_flags_a_pin_mismatch(lean):
    g = lean / "data" / "c2_gproxy"
    g.mkdir(parents=True)
    (g / "pab_gproxy.jsonl").write_text("x\n")
    (g / "GPROXY_HASH.json").write_text(json.dumps({"sha256": {"pab_gproxy.jsonl": "0" * 64}}))
    m = md.gproxy_manifest(lean)
    assert m["status"] == "PIN MISMATCH" and m["notes"]


def test_manifests_command_roundtrip_with_gate_c2_names(lean):
    out = staged_lean(lean)
    for name, m in md.mixdev_manifests(out, lean).items():
        if m.get("gate_input"):
            assert m["set"] in (gc.MIXDEV, gc.TRANSFER, gc.T37B_DEV)
    assert md.predict_cmd("a", ["x", "y"], "_t") == (f"python -B od_gcp.py predict --name a --base {md.sm.BASE} --splits x,y "
                                                      f"--layout {md.sm.LAYOUT} --revision {md.sm.REV} --tag _t")


# ----------------------------------------------------------------------------------------- gate_c2 can read the staged file
def test_staged_file_is_consumable_by_gate_c2(lean):
    make_family(lean, "T28", 150)
    make_family(lean, "T26", 150)
    res = build(lean, families=["T28", "T26"])
    jl_write(lean / "data" / "c2_mixdev.jsonl", res["main"])           # what the orchestrator's install step would produce
    pdir = lean / "preds_c2_mixdev"
    for name, acc in ((gc.CAND, 0.9), (gc.REF, 0.5)):
        pdir.mkdir(exist_ok=True)
        with open(pdir / f"{name}.jsonl", "w") as f:
            for i, r in enumerate(res["main"]):
                ok = (i % 10) < acc * 10
                if r["qtype"] == "noul":
                    p = {"yes": 0.9 if (r["gold"] == 1) == ok else 0.1, "no": 0.0}
                    p["no"] = 1 - p["yes"]
                else:
                    other = next(o for o in r["options"] if o != r["gold"])
                    p = {o: (0.8 if (o == r["gold"]) == ok and (o == r["gold"] or o == other) else 0.1) for o in r["options"]}
                f.write(json.dumps({"id": r["id"], "model": name, "probs": p}) + "\n")
    rows = gc.split_rows(gc.MIXDEV, gc.CAND, gc.REF, lean)
    assert len(rows) == 300 and {r["family"] for r in rows} == {"T28", "T26"}
    assert gc.per_family(rows)


# --------------------------------------------------------------------------------------------------- real-file smoke (read-only)
@pytest.mark.parametrize("fam", ["T28", "T26", "T29", "F5"])
def test_real_mixdev_rows_have_the_gate_form(fam):
    f = md.fam_paths(fam)["mixdev"]
    if not f.exists():
        pytest.skip("mixdev not on disk")
    rows = [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
    assert md.row_problems(fam, rows) == []
    a, _ = md.pick_units(fam, rows, 150)
    b, _ = md.pick_units(fam, rows, 150)
    assert a == b and len(a) == min(len(rows), 150) if len(rows) <= 150 else len(a) <= 150
