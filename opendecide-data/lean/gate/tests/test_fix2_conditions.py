"""CPU tests for gate/fix2_conditions.py (A8-prime: steps 0a pairs, 0b probe-go, R c1parity, P precheck, N noninf).
No GPU, no network, no model. The real lean/ tree is only read; scratch trees live in pytest's tmp_path.

  ../.venv/bin/python -m pytest -q gate/tests/test_fix2_conditions.py

What is real and what is a stand-in:
- N and R run on the REAL job-1 reads: 4B-E (q35_4b_pxE_fresh) stands in for C4 and the main run (q35_4b_main500k) for
  C1R. They must reproduce logs/gate4b/look_ship1.txt with the sign flipped (full -1.19, primary -2.47, Brier +0.0085,
  perm 3.78 vs 2.43, (e) without hate 39/662 vs 32/662) and FAIL; C1 vs itself must PASS with every difference 0.
- 0a/0b/P run on the REAL F7 v1 probe file (598 aff/dneg pairs) with SYNTHETIC probabilities (known flip counts) and a
  synthetic devx (a slice of the probe renamed): plumbing and thresholds only.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "gate"))
import fix2_conditions as fc  # noqa: E402
import gate_dev as gd  # noqa: E402

V1 = LEAN / "data/v14_parts/f7_v1_backup"  # the F7 v1 probe (v14_parts now holds v2)
META = json.loads((LEAN / "preds_dev/q35_4b_main500k.meta.json").read_text())


@pytest.fixture(autouse=True)
def _roots():
    old = (fc.ROOT, gd.ROOT, gd._MODE)
    yield
    fc.ROOT, gd.ROOT, gd._MODE = old


def write_jsonl(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))


def read_jsonl(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def write_preds(root, split, name, probs_by_id):
    d = root / f"preds_{split}"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.jsonl").write_text("".join(json.dumps({"id": i, "probs": p}) + "\n" for i, p in probs_by_id.items()))
    m = copy.deepcopy(META)
    m.update(name=name, rows=len(probs_by_id))
    (d / f"{name}.meta.json").write_text(json.dumps(m))


def probe_root(tmp_path):
    """A scratch tree: the real v1 probe as data/f7_probe.jsonl, and a devx stand-in (the first 150 ladders, renamed)."""
    root = tmp_path / "lean"
    (root / "gate").mkdir(parents=True)
    rows = read_jsonl(V1 / "f7_probe.jsonl")
    rels = read_jsonl(V1 / "f7_probe_relations.jsonl")
    write_jsonl(root / "data/f7_probe.jsonl", rows)
    write_jsonl(root / "data/f7_probe_relations.jsonl", rels)
    keep = {r["call_id"] for r in rows[:450]}
    drows = [{**r, "id": "dx_" + r["id"], "split": "f7_devx"} for r in rows if r["call_id"] in keep]
    ids = {r["id"] for r in drows}
    drels = [{**x, "a": "dx_" + x["a"], "b": "dx_" + x["b"]} for x in rels if "dx_" + x["a"] in ids]
    write_jsonl(root / "data/f7_devx.jsonl", drows)
    write_jsonl(root / "data/f7_devx_relations.jsonl", drels)
    return root, rows, drows


def gold_probs(rows):
    return {r["id"]: ({"yes": 0.9, "no": 0.1} if r["gold"] == 1 else {"yes": 0.1, "no": 0.9}) for r in rows}


def with_flips(rows, pairs, k):
    """Every row answered right, then the dneg row of the first k pairs answered wrong: exactly k flips."""
    P = gold_probs(rows)
    for _, b, _ in pairs[:k]:
        P[b] = {"yes": 1 - P[b]["yes"], "no": 1 - P[b]["no"]}
    return P


def run(root, *argv):
    return fc.main([*argv, "--root", str(root)])


# ------------------------------------------------------------------------------------------------ 0a: pairs
def test_pairs_v1_and_freeze(tmp_path):
    root, rows, _ = probe_root(tmp_path)
    res = run(root, "pairs")
    pr = res["splits"]["f7_probe"]
    assert pr["pairs"] == 598 and pr["units"] == 598 and pr["depths"] == {2: 598}
    assert pr["excluded"] == {"not equiv": 598}  # the 598 aff<->neg complement relations
    assert res["splits"]["f7_devx"]["pairs"] == 150
    blob = (root / fc.PAIRS_FILE).read_bytes()
    run(root, "pairs")  # identical: accepted, unchanged
    assert (root / fc.PAIRS_FILE).read_bytes() == blob
    # a changed probe after the freeze: every later step stops, and the list is never rewritten
    write_jsonl(root / "data/f7_probe.jsonl", rows[:-3])
    with pytest.raises(SystemExit, match="differs from the file whose pairs were frozen"):
        fc.frozen_pairs("f7_probe")
    with pytest.raises(SystemExit, match="exists and differs"):
        run(root, "pairs")


def test_pairs_need_devx(tmp_path):
    root, _, _ = probe_root(tmp_path)
    (root / "data/f7_devx.jsonl").unlink()
    with pytest.raises(SystemExit, match="devx both exist"):
        run(root, "pairs")


def test_pairs_v2_schema(tmp_path):
    """Checklist-style ladders: only (R0, pure even depth >= 2) equiv pairs in holdout ladders count."""
    root = tmp_path / "lean"
    (root / "gate").mkdir(parents=True)
    rows, rels = [], []
    for lad, kind in (("L1", "holdout"), ("L2", "iid")):
        spec = [("R0", 0, 0), ("N1", 1, 0), ("N2", 2, 0), ("N3", 3, 0), ("N4", 4, 0), ("D", 2, 1), ("AR", 1, 0)]
        for rung, d, nd in spec:
            rows.append({"id": f"{lad}_{rung}", "call_id": lad, "group_id": lad, "qtype": "noul", "gold": 1,
                         "meta": {"rung": rung, "depth": d, "n_distractor": nd, "dev_kind": kind}})
        for b in ("N2", "N4", "D"):
            rels.append({"type": "equiv", "a": f"{lad}_R0", "b": f"{lad}_{b}"})
        rels.append({"type": "equiv", "a": f"{lad}_N1", "b": f"{lad}_N3"})
        rels.append({"type": "complement", "a": f"{lad}_R0", "b": f"{lad}_N1"})
    write_jsonl(root / "data/f7_probe.jsonl", rows)
    write_jsonl(root / "data/f7_probe_relations.jsonl", rels)
    fc.ROOT = root
    pairs, info = fc.select_pairs("f7_probe")
    assert sorted((a, b) for a, b, _ in pairs) == [("L1_R0", "L1_N2"), ("L1_R0", "L1_N4")]
    assert info["holdout_rule"] is True and info["depths"] == {2: 1, 4: 1}


# ------------------------------------------------------------------------------------------------ 0b: probe go rule
def test_probe_go(tmp_path):
    root, rows, _ = probe_root(tmp_path)
    run(root, "pairs")
    pairs, _ = fc.frozen_pairs("f7_probe")
    write_preds(root, "f7_probe", "c1_p0", with_flips(rows, pairs, 120))   # 20.07%
    write_preds(root, "f7_probe", "e_p0", with_flips(rows, pairs, 30))     # 5.02%
    r = run(root, "probe-go", "c1_p0", "e_p0")
    assert r["pass"] and r["c1_flips"] == 120 and r["ref_flips"] == 30 and r["lo"] > 0
    write_preds(root, "f7_probe", "c1_p0", with_flips(rows, pairs, 45))    # +2.51 pp: under the +3 pp bar
    r = run(root, "probe-go", "c1_p0", "e_p0")
    assert not r["pass"] and abs(r["diff_pp"] - 100 * 15 / 598) < 1e-9
    del r


# ------------------------------------------------------------------------------------------------ P: pre-check
def test_precheck(tmp_path):
    root, rows, drows = probe_root(tmp_path)
    run(root, "pairs")
    pairs, _ = fc.frozen_pairs("f7_probe")
    dpairs, _ = fc.frozen_pairs("f7_devx")
    write_preds(root, "f7_probe", "c1r", with_flips(rows, pairs, 120))
    write_preds(root, "f7_devx", "c1r", with_flips(drows, dpairs, 10))
    write_preds(root, "f7_probe", "c4", with_flips(rows, pairs, 60))      # exactly half: PASS
    write_preds(root, "f7_devx", "c4", with_flips(drows, dpairs, 10))
    r = run(root, "precheck", "c4", "c1r")
    assert r["pass"] and r["parts"]["probe"]["c4_flips"] == 60 and r["parts"]["devx"]["acc_pass"]
    write_preds(root, "f7_probe", "c4", with_flips(rows, pairs, 61))      # one over half: FAIL
    assert not run(root, "precheck", "c4", "c1r")["pass"]
    write_preds(root, "f7_probe", "c4", with_flips(rows, pairs, 0))
    write_preds(root, "f7_devx", "c4", with_flips(drows, dpairs, 11))     # devx: one more flip and one row worse
    r = run(root, "precheck", "c4", "c1r")
    assert not r["pass"] and not r["parts"]["devx"]["acc_pass"] and not r["parts"]["devx"]["flip_pass"]
    # consistency bought by a bias: no flips, but every yes row answered no -> probe accuracy falls -> FAIL
    P = {r_["id"]: {"yes": 0.1, "no": 0.9} for r_ in rows}
    write_preds(root, "f7_probe", "c4", P)
    write_preds(root, "f7_devx", "c4", with_flips(drows, dpairs, 0))
    r = run(root, "precheck", "c4", "c1r")
    assert r["parts"]["probe"]["c4_flips"] == 0 and not r["parts"]["probe"]["acc_pass"] and not r["pass"]
    # a missing prediction stops (no verdict)
    P = with_flips(rows, pairs, 0)
    P.pop(rows[5]["id"])
    write_preds(root, "f7_probe", "c4", P)
    with pytest.raises(SystemExit, match="must be complete"):
        run(root, "precheck", "c4", "c1r")


# ------------------------------------------------------------------------------------------------ N and R on real reads
def test_noninf_real_standin_fails_like_look_ship1():
    r = fc.main(["noninf", "q35_4b_pxE_fresh", "q35_4b_main500k"])
    n = r["numbers"]
    assert round(n["full"]["diff"], 2) == -1.19 and n["full"]["n"] == 7056
    assert round(n["primary"]["diff"], 2) == -2.47 and n["primary"]["n"] == 3847
    assert round(n["brier"]["diff"], 4) == 0.0085
    assert round(n["perm"]["cand"], 2) == 3.78 and round(n["perm"]["ref"], 2) == 2.43
    e = n["equiv_nonhate"]
    assert (e["pairs"], e["c4_flips"], e["c1r_flips"]) == (662, 39, 32)
    assert n["equiv_hate_report"] == {"pairs": 60, "c4_flips": 2, "c1r_flips": 32}
    status = {c["name"].split(" C4")[0].split(" without")[0]: c["pass"] for c in r["checks"]}
    assert status == {"full set (no tb_mixtral)": False, "primary (unseen sources)": False,
                      "calibrated yes/no Brier": False, "(f) permutation flips": False, "jagged ASR": True,
                      "OPI ASR": True, "(e)": False}
    assert r["pipeline_issues"] == [] and not r["pass"]


def test_noninf_real_identity_passes():
    r = fc.main(["noninf", "q35_4b_main500k", "q35_4b_main500k"])
    assert r["pass"] and all(c["pass"] for c in r["checks"])
    assert r["numbers"]["full"]["diff"] == 0 and r["numbers"]["equiv_nonhate"]["bar"] == pytest.approx(100 * 32 / 662 + 1)


def test_c1parity_real_and_perturbed(tmp_path):
    r = fc.main(["c1parity", "q35_4b_pxE_fresh", "q35_4b_pxE_parity"])
    assert r["pass"]
    root = tmp_path / "lean"
    root.mkdir()
    os.symlink(LEAN / "data", root / "data")
    for sp in fc.SPLITS9:
        d = root / f"preds_{sp}"
        d.mkdir()
        for nm in ("a", "b"):
            src = LEAN / f"preds_{sp}/q35_4b_pxE_fresh"
            m = json.loads(Path(f"{src}.meta.json").read_text())
            (d / f"{nm}.meta.json").write_text(json.dumps({**m, "name": nm}))
            lines = Path(f"{src}.jsonl").read_text().splitlines()
            if nm == "b":  # 2% of the rows: one option's probability moved by 0.2 -> max |dp| over the bar
                lines = [json.dumps({**json.loads(l), "probs": {k: (v + 0.2 if j == 0 else v) for j, (k, v) in
                                                                enumerate(json.loads(l)["probs"].items())}})
                         if i % 50 == 0 else l for i, l in enumerate(lines)]
            (d / f"{nm}.jsonl").write_text("\n".join(lines) + "\n")
    r = fc.main(["c1parity", "b", "a", "--root", str(root)])
    assert not r["pass"] and [c["pass"] for c in r["checks"]][2] is False
    shutil.rmtree(root / "preds_dev")


# ------------------------------------------------------------------------------------------------ 0a on the real F7 v2
V2_FILES = ("f7_probe.jsonl", "f7_probe_relations.jsonl", "f7_probe_meta.jsonl", "f7_devx.jsonl",
            "f7_devx_relations.jsonl", "f7_devx_meta.jsonl")


def v2_root(tmp_path):
    """A scratch tree with byte copies of the frozen F7 v2 probe and devx (+ relations and sidecars)."""
    root = tmp_path / "lean"
    (root / "gate").mkdir(parents=True)
    (root / "data").mkdir()
    for f in V2_FILES:
        shutil.copy2(LEAN / "data/v14_parts" / f, root / "data" / f)
    return root


def test_pairs_v2_real_probe_and_devx(tmp_path):
    """The sidecar decides depth / distractors; devx ladders count as held out; the pure subset is report-only."""
    root = v2_root(tmp_path)
    res = run(root, "pairs")
    pr, dx = res["splits"]["f7_probe"], res["splits"]["f7_devx"]
    # F7 v2 r6: r4's probe minus the depth-4 trim (82 rows; depth 4 <= 3% of the probe, CL:61)
    assert (pr["pairs"], pr["units"], pr["depths"]) == (252, 178, {2: 204, 4: 48})
    assert pr["with_distractor"] == 238 and len(pr["pure_subset_report_only"]) == 14
    assert pr["sidecar_sha256"] == "f4c8c3357730b34616e735e093d4d59ee11628ce1f6baaf65abc0634a57330d4"
    assert (dx["pairs"], len(dx["pure_subset_report_only"])) == (44, 16) and dx["depths"] == {2: 42, 4: 2}
    # every pair: R0 anchor + an even-depth N2 / N4 yes/no row of the same ladder, held out
    side = {json.loads(l)["id"]: json.loads(l) for l in open(root / "data/f7_probe_meta.jsonl")}
    for a, b, _ in fc.frozen_pairs("f7_probe")[0]:
        assert side[a]["rung"] == "R0" and side[b]["rung"] in ("N2", "N4") and side[a]["ladder_id"] == side[b]["ladder_id"]
        assert side[a]["dev_kind"] == side[b]["dev_kind"] == "holdout" and side[b]["depth"] % 2 == 0
    # a changed sidecar after the freeze stops every later step
    p = root / "data/f7_probe_meta.jsonl"
    p.write_text(p.read_text().replace('"n_distractor": 0', '"n_distractor": 1', 1))
    with pytest.raises(SystemExit, match="f7_probe_meta.jsonl is missing or differs"):
        fc.frozen_pairs("f7_probe")


def test_pairs_distractor_and_devx_kind(tmp_path):
    """Synthetic: a distractor on the even rung still counts; a devx-kind ladder counts; iid never does."""
    root = tmp_path / "lean"
    (root / "gate").mkdir(parents=True)
    rows, rels, side = [], [], []
    for lad, kind in (("H", "holdout"), ("I", "iid"), ("X", "devx")):
        for rung, d, nd in (("R0", 0, 0), ("N2", 2, 1), ("N4", 4, 0), ("D", 2, 1)):
            rid = f"{lad}_{rung}"
            rows.append({"id": rid, "call_id": lad, "group_id": lad, "qtype": "noul", "gold": 1,
                         "meta": {"rung": rung, "dev_kind": kind}})
            side.append({"id": rid, "ladder_id": lad, "rung": rung, "depth": d, "n_distractor": nd, "dev_kind": kind})
        rels += [{"type": "equiv", "a": f"{lad}_R0", "b": f"{lad}_{b}"} for b in ("N2", "N4", "D")]
    write_jsonl(root / "data/f7_probe.jsonl", rows)
    write_jsonl(root / "data/f7_probe_relations.jsonl", rels)
    write_jsonl(root / "data/f7_probe_meta.jsonl", side)
    fc.ROOT = root
    pairs, info = fc.select_pairs("f7_probe")
    assert sorted((a, b) for a, b, _ in pairs) == [("H_R0", "H_N2"), ("H_R0", "H_N4"), ("X_R0", "X_N2"), ("X_R0", "X_N4")]
    assert info["with_distractor"] == 2 and info["pure_subset_report_only"] == [["H_R0", "H_N4"], ["X_R0", "X_N4"]]


# ------------------------------------------------------------------------------------------------ fixer review (2 Oct)
def _v2_with_drops(tmp_path, ladders):
    root = v2_root(tmp_path)
    (root / "yn2b").mkdir()
    (root / "yn2b/f7_fix2_drops.json").write_text(json.dumps({"probe_report_only": {k: "test" for k in ladders}}))
    return root


def test_precheck_holdout_bar_and_frozen_exclusions(tmp_path):
    """P's accuracy bars: all probe rows minus the frozen audit-flagged rows, AND the held-out rows alone; a gain on
    iid rows cannot hide a loss on held-out rows; a loss confined to excluded rows does not count (report only)."""
    rows0 = read_jsonl(LEAN / "data/v14_parts/f7_probe.jsonl")
    held_lads = sorted({r["meta"]["latent_id"] for r in rows0 if r["meta"]["dev_kind"] == "holdout"})
    root = _v2_with_drops(tmp_path, held_lads[:3])
    res = run(root, "pairs")
    ex = res["accuracy_excluded"]
    assert ex["ladders"] == held_lads[:3] and ex["rows"] and not ex["ladders_not_in_file"]
    rows = read_jsonl(root / "data/f7_probe.jsonl")
    drows = read_jsonl(root / "data/f7_devx.jsonl")
    pairs, _ = fc.frozen_pairs("f7_probe")
    dpairs, _ = fc.frozen_pairs("f7_devx")
    in_pair = {x for a, b, _ in pairs for x in (a, b)}
    excl = set(ex["rows"])
    write_preds(root, "f7_devx", "c1r", gold_probs(drows))
    write_preds(root, "f7_devx", "c4", gold_probs(drows))
    # C1R wrong on 40 iid rows; C4 right there but wrong on 20 held-out rows (none in a pair, none excluded)
    iid = [r for r in rows if r["meta"]["dev_kind"] == "iid" and r["qtype"] == "noul" and r["id"] not in in_pair]
    hold = [r for r in rows if r["meta"]["dev_kind"] == "holdout" and r["qtype"] == "noul" and r["id"] not in in_pair
            and r["id"] not in excl]
    flip = lambda P, rs: {**P, **{r["id"]: {"yes": 1 - P[r["id"]]["yes"], "no": 1 - P[r["id"]]["no"]} for r in rs}}  # noqa: E731
    P1 = flip(gold_probs(rows), iid[:40])
    P4 = flip(gold_probs(rows), hold[:20])
    write_preds(root, "f7_probe", "c1r", P1)
    write_preds(root, "f7_probe", "c4", P4)
    r = run(root, "precheck", "c4", "c1r")
    pr = r["parts"]["probe"]
    assert pr["acc_pass"] and not pr["acc_holdout_pass"] and not r["pass"]
    assert pr["accuracy_excluded_rows"] == len(excl) and pr["accuracy_rows"] == len(rows) - len(excl)
    # C4 wrong only on frozen-excluded rows: both accuracy bars pass; the excluded rows are reported
    ex_rows = [r_ for r_ in rows if r_["id"] in excl and r_["qtype"] == "noul" and r_["id"] not in in_pair]
    write_preds(root, "f7_probe", "c1r", gold_probs(rows))
    write_preds(root, "f7_probe", "c4", flip(gold_probs(rows), ex_rows))
    r = run(root, "precheck", "c4", "c1r")
    pr = r["parts"]["probe"]
    assert r["pass"] and pr["acc_pass"] and pr["acc_holdout_pass"]
    assert pr["report_only"]["c4_acc_excluded_rows"] < pr["report_only"]["c1r_acc_excluded_rows"]


def test_pipeline_issue_is_no_verdict(tmp_path):
    """A pipeline problem gives NO VERDICT: exit 2 and no JSON record (gate_4b_fix2_l4.sh cond() then stops the job
    without a record; the step is re-run after a repair). The same rows with clean reads give a verdict."""
    import subprocess
    root, rows, drows = probe_root(tmp_path)
    run(root, "pairs")
    pairs, _ = fc.frozen_pairs("f7_probe")
    dpairs, _ = fc.frozen_pairs("f7_devx")
    for nm in ("c1r", "c4"):
        write_preds(root, "f7_probe", nm, with_flips(rows, pairs, 10))
        write_preds(root, "f7_devx", nm, with_flips(drows, dpairs, 0))
    m = json.loads((root / "preds_f7_probe/c4.meta.json").read_text())
    m.pop("load", None)   # no load record: not a clean od_gcp predict read
    (root / "preds_f7_probe/c4.meta.json").write_text(json.dumps(m))
    out = tmp_path / "P.json"
    cp = subprocess.run([sys.executable, str(LEAN / "gate/fix2_conditions.py"), "precheck", "c4", "c1r", "--root",
                         str(root), "--json", str(out)], capture_output=True, text=True)
    assert cp.returncode == 2 and not out.exists() and "NO VERDICT" in cp.stdout
    cp = subprocess.run([sys.executable, str(LEAN / "gate/fix2_conditions.py"), "probe-go", "c4", "c1r", "--root",
                         str(root), "--json", str(out)], capture_output=True, text=True)
    assert cp.returncode == 2 and not out.exists()
    # a missing read is no verdict either (exit 2, nothing recorded)
    write_preds(root, "f7_probe", "c4", with_flips(rows, pairs, 10))
    (root / "preds_f7_devx/c4.jsonl").unlink()
    cp = subprocess.run([sys.executable, str(LEAN / "gate/fix2_conditions.py"), "precheck", "c1r", "c4", "--root",
                         str(root), "--json", str(out)], capture_output=True, text=True)
    assert cp.returncode == 2 and not out.exists()
