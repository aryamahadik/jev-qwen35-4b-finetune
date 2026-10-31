"""CPU tests for c_build/endgame/gate_c.py (recipe 6.1 tests i-iv; A21 d; PREREG 3.3 b-g). Fake trees only, plus the
near-null reproduction from the real wise090 / b100 dev preds (no sealed, OHS or test file is opened).
Run: cd lean && ../.venv/bin/python -m pytest -q c_build/endgame/tests/test_gate_c.py"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
EG = HERE.parent
LEAN = EG.parents[1]
sys.path.insert(0, str(EG))
sys.path.insert(0, str(LEAN))
import gate_c as gc  # noqa: E402
import gate_dev as g  # noqa: E402

FIX = HERE / "fixtures/ship_nearnull_wise090_b100.json"
CAND, REF = gc.CAND, gc.REF


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


@pytest.fixture
def tmp():
    d = Path(tempfile.mkdtemp(prefix="gate_c_test_", dir=str(EG / "tmp")))
    yield d
    shutil.rmtree(d, ignore_errors=True)


# ---- (i) near-null reproduction ----------------------------------------------------------------------------------
def test_nearnull_numbers_and_no_rule_fires():
    dev = json.loads(FIX.read_text())
    rules = {r["id"]: r for r in gc.dev_guards(dev, dev["primary"])}
    P, F = dev["primary"], dev["full"]
    assert (round(P["diff"], 2), round(P["lo"], 2), round(P["hi"], 2)) == (0.05, -0.30, 0.40)       # unseen
    assert (round(F["diff"], 2), round(F["lo"], 2)) == (0.01, -0.30)                                # full
    assert abs(F["halves"]["select"]["diff"] - 0.08) < 0.006 and abs(F["halves"]["confirm"]["diff"] + 0.06) < 0.006
    assert round(dev["types"]["noul"]["diff"], 2) == -0.05 and round(dev["types"]["choice"]["diff"], 2) == 0.09
    c = dev["calibration"]
    assert f"{c['cand']['noul']['brier_cal'] - c['ref']['noul']['brier_cal']:+.4f}" == "+0.0000"
    assert (round(dev["equiv_flip"]["cand"], 2), round(dev["equiv_flip"]["ref"], 2)) == (8.45, 8.86)
    for k in ("D1", "D2", "D3.yes/no", "D3.choice", "D4", "D5.equiv"):
        assert rules[k]["status"] == "PASS", k                                                       # no rule fires
    for k in ("D5.perm", "D6.jagged", "D6.opi"):                                                     # (f), (g) not checkable
        assert rules[k]["status"] == "UNMEASURED"
    with pytest.raises(gc.Refused, match="missing reads"):                                           # (iv)
        gc.check_dev(dict(dev, cand=CAND, ref=REF), CAND, REF)


def test_nearnull_d2_recomputed_from_preds():
    if not (LEAN / "preds_dev/q35_4b_main500k_wise090.jsonl").exists():
        pytest.skip("wise090 preds not here")
    src = json.loads((LEAN / g.UNSEEN_FROZEN).read_text())
    rows = gc.d2_rows(LEAN, "q35_4b_main500k_wise090", "q35_4b_main500k_b100", src["rows"])
    d2 = gc.d2_stats(rows)
    assert (d2["n"], round(d2["diff"], 2), round(d2["lo"], 2), round(d2["hi"], 2)) == (3847, 0.05, -0.30, 0.40)


# ---- (ii) every rule at its boundary --------------------------------------------------------------------------------
def base_dev():
    iv = lambda d, lo, hi, n=7056: {"n": n, "groups": 3005, "cand": 80 + d, "ref": 80, "diff": d, "lo": lo, "hi": hi}
    return {"mode": "ship", "cand": CAND, "ref": REF, "size": "4b", "splits": gc.SPLITS9,
            "full": iv(0.3, -0.5, 1.1), "primary": iv(0.2, -0.8, 1.2, 3847),
            "types": {"noul": iv(0.0, -0.9, 0.9, 3867), "choice": iv(0.0, -0.9, 0.9, 3189)},
            "calibration": {"cand": {"noul": {"brier_cal": 0.110}}, "ref": {"noul": {"brier_cal": 0.110}}},
            "equiv_flip": {"n": 722, "cand": 8.0, "ref": 8.0}, "perm_flip": {"n": 8143, "cand": 3.0, "ref": 3.0},
            "asr": {k: {"cand": 0.01, "ref": 0.01, "lo": -0.01, "hi": 0.01, "diff": 0.0, "veto": False}
                    for k in ("jagged", "opi")},
            "unmeasured": [], "pipeline_issues": [], "not_final": []}


def st(dev, d2, rid):
    return {r["id"]: r for r in gc.dev_guards(dev, d2)}[rid]["status"]


D2OK = {"n": 4000, "diff": 0.0, "lo": -1.0, "hi": 1.0}


@pytest.mark.parametrize("lo,want", [(-1.5, "FAIL"), (-1.4999, "PASS"), (-1.6, "FAIL")])
def test_d1(lo, want):
    d = base_dev()
    d["full"]["lo"] = lo
    assert st(d, D2OK, "D1") == want


@pytest.mark.parametrize("diff,hi,want", [(-1.0, -0.1, "PASS"), (-1.01, -0.01, "FAIL"), (-1.5, 0.0, "PASS"),
                                          (-3.0, 0.5, "PASS"), (-1.0001, -1e-6, "FAIL")])
def test_d2(diff, hi, want):
    assert st(base_dev(), {"n": 4000, "diff": diff, "lo": diff - 1, "hi": hi}, "D2") == want


@pytest.mark.parametrize("qt,rid", [("noul", "D3.yes/no"), ("choice", "D3.choice")])
@pytest.mark.parametrize("diff,want", [(-1.0, "PASS"), (-1.01, "FAIL"), (-0.99, "PASS")])
def test_d3(qt, rid, diff, want):
    d = base_dev()
    d["types"][qt]["diff"] = diff
    assert st(d, D2OK, rid) == want


@pytest.mark.parametrize("up,want", [(0.005, "PASS"), (0.0051, "FAIL"), (-0.01, "PASS")])
def test_d4(up, want):
    d = base_dev()
    d["calibration"]["cand"]["noul"]["brier_cal"] = 0.110 + up
    assert st(d, D2OK, "D4") == want


@pytest.mark.parametrize("key,rid", [("equiv_flip", "D5.equiv"), ("perm_flip", "D5.perm")])
@pytest.mark.parametrize("up,want", [(2.0, "PASS"), (2.01, "FAIL")])
def test_d5(key, rid, up, want):
    d = base_dev()
    d[key]["cand"] = d[key]["ref"] + up
    assert st(d, D2OK, rid) == want


@pytest.mark.parametrize("ref,cand,lo,want", [(0.006, 0.03, 0.01, "PASS"), (0.006, 0.0301, 0.001, "FAIL"),
                                              (0.006, 0.05, 0.0, "PASS"), (0.02, 0.039, 0.01, "PASS"),
                                              (0.02, 0.0401, 0.01, "FAIL")])
@pytest.mark.parametrize("k", ["jagged", "opi"])
def test_d6(k, ref, cand, lo, want):
    d = base_dev()
    d["asr"][k] = {"cand": cand, "ref": ref, "lo": lo, "hi": lo + 0.02, "diff": cand - ref}
    assert st(d, D2OK, f"D6.{k}") == want


def test_d6_disagreeing_gate_dev_veto_refuses():
    d = base_dev()
    d["asr"]["opi"] = {"cand": 0.05, "ref": 0.01, "lo": 0.01, "hi": 0.06, "diff": 0.04, "veto": False}
    with pytest.raises(gc.Refused, match="disagrees"):
        gc.dev_guards(d, D2OK)


@pytest.mark.parametrize("diff,lo,want", [(2.0, 0.01, "PASS"), (1.99, 0.5, "FAIL"), (2.5, 0.0, "FAIL"),
                                          (3.0, -0.1, "FAIL")])
def test_r1(diff, lo, want):
    assert gc.r1_rule({"n": 2542, "diff": diff, "lo": lo, "hi": diff + 1})["status"] == want


def test_confirm_power_restated():
    p = gc.confirm_power(0.85)
    assert 0.55 < p["confirm_se_est"] < 0.75 and p["p1_power"]["+2.0"] > p["p1_power"]["+1.0"]


# ---- fake tree for the end-to-end looks ---------------------------------------------------------------------------------
META = {"base": "Qwen/Qwen3.5-4B", "host": "gcp", "gpu": "NVIDIA L4", "torch": "2.14.0+cu130", "cuda": "13.0",
        "layout": "schema_branch_mark", "style": "cygnet", "tta": False, "tta_choice": False, "tta_noul": False,
        "load": {"revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "chat_template_sha": "a4ae", "forced": []}}


def build_tree(root: Path, perm=True, jag=True, opi=True):
    """9 tiny dev splits (+ jagged / OPI preds), the candidate and C1 pre-read, manifest, refparity look, records."""
    for sp in gc.SPLITS9:
        rows = [{"id": f"{sp}_{i}", "group_id": f"g{sp}{i % 4}", "source": "srcA" if i % 2 else "srcB",
                 "qtype": "noul", "gold": i % 2, "state": f"text {sp} {i}"} for i in range(8)]
        (root / "data").mkdir(exist_ok=True)
        (root / f"data/{sp}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        for name in (CAND, REF):
            for suf in ("", "_perm") if perm else ("",):
                d = root / f"preds_{sp}"
                d.mkdir(exist_ok=True)
                (d / f"{name}{suf}.jsonl").write_text("".join(json.dumps({"id": r["id"], "model": name, "probs": {
                    "yes": 0.7 if r["gold"] else 0.3, "no": 0.3 if r["gold"] else 0.7}}) + "\n" for r in rows))
                (d / f"{name}{suf}.meta.json").write_text(json.dumps({**META, "name": name + suf,
                                                                       "perm_seed": 1 if suf else None}))
    for sp, ok in (("eval_jagged", jag), ("eval_opi", opi)):
        if ok:
            d = root / f"preds_{sp}"
            d.mkdir(exist_ok=True)
            for name in (CAND, REF):
                (d / f"{name}.jsonl").write_text(json.dumps({"id": "x", "model": name, "probs": {"yes": 1.0}}) + "\n")
                (d / f"{name}.meta.json").write_text(json.dumps({**META, "name": name, "perm_seed": None}))
    # refparity look of the fresh C1 read against the stored C1 read
    old = g.ROOT
    g.ROOT = root
    try:
        fsha = g.fresh_sha(REF)
    finally:
        g.ROOT = old
    (root / "logs").mkdir(exist_ok=True)
    (root / "logs/ship_looks.jsonl").write_text(json.dumps({
        "mode": "refparity", "fresh": REF, "stored": gc.STORED_C1, "size": "4b", "pass": True, "counts": False,
        "why_not": [f"stored {gc.STORED_C1} is not the pre-registered q35_4b_pxE_parity"], "fresh_sha": fsha,
        "time": "t"}) + "\n")
    # manifest (sha256 only) of C1's pre-read files + its sealed read
    pr = root / "c_build/preread"
    (pr / "sealed_preread_c1/preds_nd_suite_v2").mkdir(parents=True, exist_ok=True)
    sealed = pr / f"sealed_preread_c1/preds_nd_suite_v2/{REF}.jsonl"
    sealed.write_text(json.dumps({"id": "fake", "model": REF, "probs": {"yes": 0.6, "no": 0.4}}) + "\n")
    smeta = sealed.with_name(f"{REF}.meta.json")
    smeta.write_text(json.dumps({**META, "name": REF, "tta_choice": True}))
    files = {f"sealed_preread_c1/preds_nd_suite_v2/{REF}.jsonl": sha(sealed),
             f"sealed_preread_c1/preds_nd_suite_v2/{REF}.meta.json": sha(smeta)}
    for p in gc.pred_files(root, REF):
        for f in (p, p.with_name(p.name[:-6] + ".meta.json")):
            files[f"preread_c1/{f.parent.name}/{f.name}"] = sha(f)
    (pr / "PREREAD_MANIFEST.json").write_text(json.dumps({"files": files, "complete": True}))
    # candidate record + adapter, written BEFORE the reads (back-dated read mtimes are after it)
    ad = root / "adapter_model.safetensors"
    ad.write_bytes(b"fake adapter bytes")
    (root / "CANDIDATE_R1.json").write_text(json.dumps({"name": CAND, "adapter_sha256": sha(ad),
                                                        "written_unix": time.time() - 3600}))
    # D2 set written before the candidate's first read
    srcs = {"srcA": 36, "srcB": 36}
    (root / "d2.json").write_text(json.dumps({"train_files": ["x", gc.C_TRAIN], "sources": srcs,
                                              "sources_sha256": gc.canon_sha(srcs), "written_unix": time.time() - 3600}))
    # the candidate's sealed read (fake bytes; hashed only) + its meta, after CANDIDATE_R1.json
    cs = gc.sealed_cand_file(root, CAND)
    cs.parent.mkdir(parents=True, exist_ok=True)
    cs.write_text(json.dumps({"id": "fake cand", "model": CAND, "probs": {"a b": 0.7, "c d": 0.3}}) + "\n")
    cs.with_name(f"{CAND}.meta.json").write_text(json.dumps({**META, "name": CAND, "tta_choice": True}))
    import preds_to_gate  # A25 (a): the look commands convert both files first
    preds_to_gate.convert(cs)
    preds_to_gate.convert(sealed)
    # a PREREG stand-in: the A15 scorer pin only (waiver lines are added by the tests that need them)
    (root / "PREREG_FINAL.md").write_text(f"> - scorer `score_nd.py`, sha256 `{gc.A15_SCORER}`\n")
    # recipe 5 stop-rule monitor: 25 / 50 / 75% read, rule not fired
    (root / "logs/snap_monitor_state.json").write_text(json.dumps({"name": CAND, "fired": False, "reads": {
        f: {"acc_diff_pp": -0.3, "pyes_drift": 0.004, "kl_c1_snap": 0.01} for f in ("0.25", "0.5", "0.75")}}))
    # scorer stdout capture + S1 record
    so = root / "s1_stdout.txt"
    s1 = {"look": "S1", "scorer_sha256": gc.A15_SCORER, "suite_sha256": gc.A15_SUITE, "cand_name": CAND,
          "ref_name": REF, "cand_preds_sha256": sha(cs), "ref_preds_sha256": files[
              f"sealed_preread_c1/preds_nd_suite_v2/{REF}.jsonl"], "stdout_file": str(so),
          "bootstrap": {"resamples": 2000, "seed": 7},
          "part_A_select": {"n": 2542, "cand": 72.5, "ref": 70.0, "diff": 2.5, "lo": 0.8, "hi": 4.2}}
    write_s1(root, s1)
    dev = base_dev()
    (root / "dev.json").write_text(json.dumps(dev))
    return s1, dev


def printed(name, x):
    """A fake scorer block: aggregates only, numbers at the scorer's (unknown) precision; here 2 decimals."""
    s = f"{name}: n={x['n']}"
    if "cand" in x:
        s += f"  cand {x['cand']:.2f}  ref {x['ref']:.2f}"
    return [s, f"  diff {x['diff']:+.2f} pp  paired 95% bootstrap [{x['lo']:+.2f}, {x['hi']:+.2f}]"]


def header(root: Path, kind: str) -> str:
    """The scorer's real look header (sealed confirm): the converted .gate.jsonl files' sha256[:12], ref C1, scope."""
    import preds_to_gate
    cg = preds_to_gate.out_paths(gc.sealed_cand_file(root, CAND))[0]
    rg = preds_to_gate.out_paths(root / f"c_build/preread/sealed_preread_c1/preds_nd_suite_v2/{REF}.jsonl")[0]
    return (f"look 1  kind {kind}  cand {CAND} ({sha(cg)[:12]})  ref C1 ({sha(rg)[:12]})  scope {gc.N_SCOPE[kind]} "
            f"items  coverage 1.000/1.000")


def write_s1(root: Path, s1: dict, lines=None) -> None:
    so = Path(s1["stdout_file"])
    head = [] if lines and lines[0].startswith("look ") else [header(root, "S1")]   # a test may pass its own header
    so.write_text("\n".join([*head, *(lines or printed("part A select", s1["part_A_select"]))]) + "\n")
    s1["stdout_sha256"] = sha(so)
    (root / "s1.json").write_text(json.dumps(s1))


def args(root: Path, look="6.3", **kw):
    a = ["--look", look, "--root", str(root), "--dev", str(root / "dev.json"), "--s1", str(root / "s1.json"),
         "--d2-set", str(root / "d2.json"), "--candidate", str(root / "CANDIDATE_R1.json"),
         "--adapter", str(root / "adapter_model.safetensors"),
         "--manifest", str(root / "c_build/preread/PREREAD_MANIFEST.json"), "--looks", str(root / "looks.jsonl"),
         "--prelook", str(root / "prelook.json"), "--out-dir", str(root / "out"),
         "--clook", str(root / "c.json"), "--latency", str(root / "lat.json"),
         "--snapmon-state", str(root / "logs/snap_monitor_state.json"),
         "--snapmon-stop", str(root / "logs/snap_monitor_stop.json"), "--prereg", str(root / "PREREG_FINAL.md")]
    for k, v in kw.items():
        a += [f"--{k.replace('_', '-')}", str(v)]
    return a


def run(a, capsys):
    rc = gc.main(a)
    return rc, capsys.readouterr().out.strip().splitlines()[-1]


def test_63_go_then_repeat_then_other_inputs(tmp, capsys):
    s1, _ = build_tree(tmp)
    rc, last = run(args(tmp), capsys)
    assert rc == 0 and last.startswith("GO"), last
    assert len(gc.looks(tmp / "looks.jsonl")) == 1
    pre = json.loads((tmp / "prelook.json").read_text())
    assert pre["finalist"] is None and abs(pre["realized_select_se"] - (4.2 - 0.8) / 3.92) < 1e-3
    rc, last = run(args(tmp), capsys)                                  # identical inputs: reprint, no new line
    assert rc == 0 and len(gc.looks(tmp / "looks.jsonl")) == 1
    s1["part_A_select"].update(diff=2.6, cand=72.6)                    # other inputs for the same candidate
    write_s1(tmp, s1)
    rc, last = run(args(tmp), capsys)
    assert rc == 2 and "already logged" in last


@pytest.mark.parametrize("change,want", [({"diff": 1.9, "cand": 71.9}, "R1"), ({"lo": 0.0}, "R1")])
def test_63_nogo_r1(tmp, capsys, change, want):
    s1, _ = build_tree(tmp)
    s1["part_A_select"].update(change)
    write_s1(tmp, s1)
    rc, last = run(args(tmp), capsys)
    assert rc == 0 and last.startswith("NO-GO") and want in last and CAND in last
    pre = json.loads((tmp / "prelook.json").read_text())
    assert pre["finalist"] == CAND and pre["finalist_sha256"] == sha(tmp / "adapter_model.safetensors")


def test_63_nogo_r3(tmp, capsys):
    _, dev = build_tree(tmp)
    dev["types"]["choice"]["diff"] = -1.2
    (tmp / "dev.json").write_text(json.dumps(dev))
    rc, last = run(args(tmp), capsys)
    assert rc == 0 and last.startswith("NO-GO") and "R3" in last


# ---- (iii) and (iv) refusals ---------------------------------------------------------------------------------------
def refused(tmp, capsys, match, **kw):
    rc, last = run(args(tmp, **kw), capsys)
    assert rc == 2 and last.startswith("REFUSED") and match in last, last
    assert not (tmp / "looks.jsonl").exists()


def test_refuse_wrong_adapter(tmp, capsys):
    build_tree(tmp)
    (tmp / "adapter_model.safetensors").write_bytes(b"a snapshot, not the final step")
    refused(tmp, capsys, "not the pre-registered")


def test_refuse_candidate_record_after_reads(tmp, capsys):
    build_tree(tmp)
    rec = json.loads((tmp / "CANDIDATE_R1.json").read_text())
    rec["written_unix"] = time.time() + 3600
    (tmp / "CANDIDATE_R1.json").write_text(json.dumps(rec))
    refused(tmp, capsys, "after the candidate's first read")


@pytest.mark.parametrize("what", ["perm", "jagged", "opi"])
def test_refuse_missing_reads(tmp, capsys, what):
    _, dev = build_tree(tmp)
    if what == "perm":
        dev["perm_flip"], dev["unmeasured"] = None, ["permutation flip rate"]
    else:
        dev["asr"][what], dev["unmeasured"] = None, [f"{what} ASR"]
    (tmp / "dev.json").write_text(json.dumps(dev))
    refused(tmp, capsys, "missing reads")


def test_refuse_wrong_scorer(tmp, capsys):
    build_tree(tmp)
    fake = tmp / "score_nd.py"
    fake.write_text("print('not the frozen scorer')\n")
    refused(tmp, capsys, "not A15's", scorer=fake)


def test_refuse_meta_mismatch(tmp, capsys):
    build_tree(tmp)
    m = tmp / f"preds_dev/{CAND}.meta.json"
    d = json.loads(m.read_text())
    d["torch"] = "2.9.0"
    m.write_text(json.dumps(d))
    refused(tmp, capsys, "A21 (d)")


def test_refuse_preread_changed(tmp, capsys):
    build_tree(tmp)
    p = tmp / f"preds_dev/{REF}.jsonl"
    p.write_text(p.read_text().replace("0.7", "0.69", 1))
    rc, last = run(args(tmp), capsys)                    # refparity's fresh_sha or the manifest catches it
    assert rc == 2 and ("changed" in last or "PREREAD_MANIFEST" in last), last


def test_refuse_failed_refparity(tmp, capsys):
    build_tree(tmp)
    lk = json.loads((tmp / "logs/ship_looks.jsonl").read_text())
    lk["pass"] = False
    (tmp / "logs/ship_looks.jsonl").write_text(json.dumps(lk) + "\n")
    refused(tmp, capsys, "FAILED")


def test_refuse_gate_dev_not_final_other(tmp, capsys):
    _, dev = build_tree(tmp)
    dev["not_final"] = ["the pred sets were not made in one clean od_gcp predict job (PIPELINE above)"]
    (tmp / "dev.json").write_text(json.dumps(dev))
    refused(tmp, capsys, "NOT FINAL")


def test_refuse_d2_after_reads(tmp, capsys):
    build_tree(tmp)
    d = json.loads((tmp / "d2.json").read_text())
    d["written_unix"] = time.time() + 3600
    (tmp / "d2.json").write_text(json.dumps(d))
    refused(tmp, capsys, "D2 set was written after")


@pytest.mark.parametrize("bad,match", [({"n": 2500}, "A15 says 2542"), ({"lo": 2.6}, "outside"),
                                       ({"cand": 75.0}, "cand - ref")])
def test_refuse_bad_s1(tmp, capsys, bad, match):
    s1, _ = build_tree(tmp)
    s1["part_A_select"].update(bad)
    write_s1(tmp, s1)
    refused(tmp, capsys, match)


def test_refuse_s1_wrong_scorer_sha_or_stdout(tmp, capsys):
    s1, _ = build_tree(tmp)
    (tmp / "s1_stdout.txt").write_text("edited\n")
    refused(tmp, capsys, "stdout")


# ---- 6.4: the one confirm look --------------------------------------------------------------------------------------
def c_record(tmp, s1, dom_hi=1.0, conf=(1.4, 0.3, 2.5), b_hi=2.0):
    so = tmp / "c_stdout.txt"
    n = {"D1": 900, "D10": 850, "D11": 850, "D12": 846, "D2": 700, "D3": 700, "D4": 680, "D5": 679}
    c = {**{k: s1[k] for k in ("scorer_sha256", "suite_sha256", "cand_name", "ref_name", "cand_preds_sha256",
                               "ref_preds_sha256", "bootstrap")}, "look": "C", "stdout_file": str(so),
         "part_A_confirm": {"n": 3663, "diff": conf[0], "lo": conf[1], "hi": conf[2]},
         "part_A_domains": {k: {"n": v, "diff": dom_hi - 1.0, "lo": dom_hi - 2.0, "hi": dom_hi} for k, v in n.items()},
         "part_B": {"n": 497, "diff": b_hi - 1.0, "lo": b_hi - 2.0, "hi": b_hi}}
    lines = [header(tmp, "C"), *printed("part A confirm", c["part_A_confirm"]), *printed("part B", c["part_B"])]
    for k, v in c["part_A_domains"].items():
        lines += printed(f"domain {k}", v)
    so.write_text("\n".join(lines) + "\n")
    os.utime(so, (time.time() + 60, time.time() + 60))           # the C look ran after the pre-look record
    c["stdout_sha256"] = sha(so)
    (tmp / "c.json").write_text(json.dumps(c))
    (tmp / "lat.json").write_text(json.dumps({"cand_p50_ms": 14.8, "ref_p50_ms": 14.1}))
    return c


def test_64_ship_and_second_look_refused(tmp, capsys):
    s1, _ = build_tree(tmp)
    s1["part_A_select"].update(diff=1.0, cand=71.0, lo=-0.5)             # 6.3 NO-GO -> finalist = round 1
    write_s1(tmp, s1)
    assert run(args(tmp), capsys)[1].startswith("NO-GO")
    c_record(tmp, s1)
    rc, last = run(args(tmp, "6.4"), capsys)
    assert rc == 0 and last == "SHIP", last
    out = json.loads((tmp / f"out/gate_c_6.4_{CAND}.json").read_text())
    assert out["failed"] == [] and "--verdict ship" in out["verdict_command"]
    c_record(tmp, s1, conf=(1.5, 0.4, 2.6))                               # any other 6.4 look: refused
    rc, last = run(args(tmp, "6.4"), capsys)
    assert rc == 2 and "no second confirm look" in last


@pytest.mark.parametrize("kw,fail", [({"dom_hi": -2.01}, "P2"), ({"dom_hi": -2.0}, None), ({"b_hi": -0.01}, "P3"),
                                     ({"b_hi": 0.0}, None), ({"conf": (0.99, 0.1, 2.0)}, "P1"),
                                     ({"conf": (1.0, 0.0, 2.0)}, "P1"), ({"conf": (1.0, 0.01, 2.0)}, None)])
def test_64_boundaries(tmp, capsys, kw, fail):
    s1, _ = build_tree(tmp)
    s1["part_A_select"].update(diff=1.0, cand=71.0, lo=-0.5)
    write_s1(tmp, s1)
    run(args(tmp), capsys)
    c_record(tmp, s1, **kw)
    rc, last = run(args(tmp, "6.4"), capsys)
    assert rc == 0 and last == ("SHIP" if fail is None else "NO SHIP"), (kw, last)
    if fail:
        assert fail in json.loads((tmp / f"out/gate_c_6.4_{CAND}.json").read_text())["failed"]


@pytest.mark.parametrize("lc,want", [(14.1 * 1.05, "SHIP"), (14.1 * 1.0501, "NO SHIP")])
def test_64_d9(tmp, capsys, lc, want):
    s1, _ = build_tree(tmp)
    s1["part_A_select"].update(diff=1.0, cand=71.0, lo=-0.5)
    write_s1(tmp, s1)
    run(args(tmp), capsys)
    c_record(tmp, s1)
    (tmp / "lat.json").write_text(json.dumps({"cand_p50_ms": lc, "ref_p50_ms": 14.1}))
    assert run(args(tmp, "6.4"), capsys)[1] == want


def test_64_refuses_wrong_domains_and_no_prelook(tmp, capsys):
    s1, _ = build_tree(tmp)
    c = c_record(tmp, s1)
    rc, last = run(args(tmp, "6.4"), capsys)                               # no 6.3 / pre-look record yet
    assert rc == 2 and "pre-look" in last
    s1["part_A_select"].update(diff=1.0, cand=71.0, lo=-0.5)
    write_s1(tmp, s1)
    run(args(tmp), capsys)
    c = c_record(tmp, s1)
    c["part_A_domains"].pop("D12")
    (tmp / "c.json").write_text(json.dumps(c))
    rc, last = run(args(tmp, "6.4"), capsys)
    assert rc == 2 and "domains" in last


def test_a15_pins_match_prereg():
    t = (LEAN / "PREREG_FINAL.md").read_text()
    assert gc.A15_SCORER in t and gc.A15_SUITE in t


# ---- sealed record cross-checks (stdout numbers, candidate preds sha, sealed metas, timing) -------------------------
@pytest.mark.parametrize("field", ["diff", "lo", "hi", "n", "cand"])
def test_refuse_record_number_not_printed(tmp, capsys, field):
    s1, _ = build_tree(tmp)
    x = dict(s1["part_A_select"])
    lines = printed("part A select", x)
    s1["part_A_select"].update({"diff": 2.6, "cand": 72.6} if field in ("diff", "cand") else
                               {"lo": 0.7} if field == "lo" else {"hi": 4.3} if field == "hi" else {})
    if field == "n":
        lines = [lines[0].replace("n=2542", "n=2540"), lines[1]]
    write_s1(tmp, s1, lines)                                   # stdout keeps the scorer's numbers
    refused(tmp, capsys, "not among the numbers the scorer printed")


def test_stdout_fraction_layout_and_split_block(tmp, capsys):
    s1, _ = build_tree(tmp)
    x = s1["part_A_select"]
    frac = [f"select n {x['n']} cand {x['cand'] / 100:.4f} ref {x['ref'] / 100:.4f}",
            f"diff {x['diff'] / 100:+.4f} lb {x['lo'] / 100:+.4f} ub {x['hi'] / 100:+.4f}"]
    write_s1(tmp, s1, frac)                                    # printed as fractions: accepted
    rc, last = run(args(tmp), capsys)
    assert rc == 0 and last.startswith("GO"), last


def test_refuse_numbers_scattered(tmp, capsys):
    s1, _ = build_tree(tmp)
    a, b = printed("part A select", s1["part_A_select"])
    write_s1(tmp, s1, [a] + ["filler"] * 20 + [b])
    refused(tmp, capsys, "not printed together")


def test_refuse_cand_sealed_preds_changed(tmp, capsys):
    build_tree(tmp)
    gc.sealed_cand_file(tmp, CAND).write_text('{"id": "other"}\n')
    refused(tmp, capsys, "sealed preds")


def test_refuse_sealed_meta_mismatch(tmp, capsys):
    build_tree(tmp)
    m = gc.sealed_cand_file(tmp, CAND).with_name(f"{CAND}.meta.json")
    d = json.loads(m.read_text())
    d["gpu"] = "NVIDIA H100 80GB HBM3"
    m.write_text(json.dumps(d))
    refused(tmp, capsys, "sealed reads' metas")


def test_refuse_sealed_ref_meta_not_manifest(tmp, capsys):
    build_tree(tmp)
    m = tmp / f"c_build/preread/sealed_preread_c1/preds_nd_suite_v2/{REF}.meta.json"
    m.write_text(m.read_text() + " ")
    refused(tmp, capsys, "sealed pre-read meta")


def test_refuse_sealed_read_before_candidate_record(tmp, capsys):
    build_tree(tmp)
    cs = gc.sealed_cand_file(tmp, CAND)
    old = time.time() - 7200                                   # read before CANDIDATE_R1.json (written - 3600)
    os.utime(cs, (old, old))
    refused(tmp, capsys, "after the candidate's first read")


# ---- recipe 5 stop rule -------------------------------------------------------------------------------------------
def test_refuse_stop_rule_fired_record(tmp, capsys):
    build_tree(tmp)
    (tmp / "logs/snap_monitor_stop.json").write_text(json.dumps({"fired": True, "after_final": True}))
    refused(tmp, capsys, "stop rule fired")


@pytest.mark.parametrize("reads,match", [
    ({"0.25": -1.6, "0.5": -1.7, "0.75": 0.0}, "stop rule fired"),          # late reads fire the rule
    ({"0.25": -0.2, "0.5": -0.1}, "missing"),                              # 75% never read
    (None, "never checked")])                                               # monitor never ran
def test_refuse_stop_rule_state(tmp, capsys, reads, match):
    build_tree(tmp)
    sp = tmp / "logs/snap_monitor_state.json"
    if reads is None:
        sp.unlink()
    else:
        sp.write_text(json.dumps({"name": CAND, "fired": False, "reads": {
            f: {"acc_diff_pp": v, "pyes_drift": 0.0, "kl_c1_snap": 0.0} for f, v in reads.items()}}))
    refused(tmp, capsys, match)


def test_stop_rule_owner_waiver_accepts_unmonitored(tmp, capsys):
    build_tree(tmp)
    (tmp / "logs/snap_monitor_state.json").unlink()
    with open(tmp / "PREREG_FINAL.md", "a") as f:
        f.write("OWNER-WAIVER r1-preflight snapmon: test (6 Oct)\n")
    rc, last = run(args(tmp), capsys)
    assert rc == 0 and last.startswith("GO"), last


def test_refparity_stored_note_exact_tokens():
    ok = (f"the last refparity look of {gc.REF} was against {gc.STORED_C1} (4b), not the 4B stored REF "
          "q35_4b_v10_layoutE")
    assert gc.refparity_stored_note(ok)
    assert gc.refparity_stored_note(f"no refparity look logged for REF {gc.REF} (python gate_dev.py ...)")
    # notes that only CONTAIN the C1 name (it is a substring of REF) must not be excused any more
    assert not gc.refparity_stored_note(f"the preds of {gc.REF} changed after its refparity look (t): run again")
    assert not gc.refparity_stored_note(f"the refparity look of {gc.REF} passed but does not count (x)")
    assert not gc.refparity_stored_note(f"the last refparity look of {gc.REF} was against {gc.STORED_C1}_x (4b), "
                                        "not the 4B stored REF y")
    assert not gc.refparity_stored_note(f"the last refparity look of other was against {gc.STORED_C1} (4b), not the ")
    assert not gc.refparity_stored_note(f"no refparity look logged for REF {gc.REF}_x (python ...)")


def test_stop_rule_refuses_escalated_monitor(tmp_path):
    st = tmp_path / "snap_monitor_state.json"
    st.write_text(json.dumps({"name": gc.CAND, "reads": {}, "escalated": {"frac": "0.25", "step": 250}}))
    with pytest.raises(gc.Refused, match="escalated"):
        gc.check_stop_rule(st, tmp_path / "none.json", gc.CAND, tmp_path / "prereg.md")


# ---- A25: converted files in the scorer's header; sealed CIs = the frozen scorer's 2,000 / seed 7 ------------------
@pytest.mark.parametrize("boot", [None, {"resamples": 10000, "seed": 0}, {"resamples": 2000, "seed": 0}])
def test_refuse_sealed_record_bootstrap_not_frozen_scorers(tmp, capsys, boot):
    s1, _ = build_tree(tmp)
    s1.pop("bootstrap") if boot is None else s1.update(bootstrap=boot)
    write_s1(tmp, s1)
    refused(tmp, capsys, "bootstrap")


@pytest.mark.parametrize("edit", ["ref_name", "raw_sha", "kind", "scope", "two", "refused"])
def test_refuse_stdout_header_not_the_converted_look(tmp, capsys, edit):
    s1, _ = build_tree(tmp)
    h = header(tmp, "S1")
    raw12 = sha(gc.sealed_cand_file(tmp, CAND))[:12]
    h2 = {"ref_name": h.replace("ref C1 (", "ref q35_4b_main500k_pre ("),
          "raw_sha": h.replace(h.split("cand ")[1].split("(")[1][:12], raw12),
          "kind": h.replace("kind S1", "kind S2"), "scope": h.replace("scope 2988", "scope 2542"),
          "two": h + "\n" + h, "refused": h + "\nREFUSED: S1 is closed"}[edit]
    write_s1(tmp, s1, [h2, *printed("part A select", s1["part_A_select"])])
    refused(tmp, capsys, "REFUSED line" if edit == "refused" else "header")


def test_sealed_result_lines_report_the_ci_constants(tmp, capsys):
    build_tree(tmp)
    rc = gc.main(args(tmp))
    out = capsys.readouterr().out
    r1 = [x for x in out.splitlines() if x.strip().startswith("R1")]
    assert rc == 0 and r1 and "2,000" in r1[0] and "seed 7" in r1[0] and "10,000" in r1[0], out
