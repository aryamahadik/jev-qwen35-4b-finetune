"""CPU tests for gate/teacher_switch.py and gate/teacher_switch_l4.sh (PREREG_FINAL.md 6 (c) and (d)). No GPU, no
network, no model; the real lean/ tree is only read (scratch trees live in pytest's tmp_path).

  ../.venv/bin/python -m pytest -q -s gate/tests/test_teacher_switch.py            (-s prints the stand-in numbers)
  ../.venv/bin/python -m pytest -q gate/tests/test_teacher_switch.py -m "not slow"  (skips the L4-job simulation)

What is real and what is a stand-in:
- the dev rows, the frozen training-row sample and its sha256 are the real ones;
- test_standin_4bE: 4B-E stands in for the candidate. Dev side = its clean od_gcp predict read q35_4b_pxE_parity;
  (c) REF = the stored in-process read q35_4b_pxE (no fresh read exists yet); training side = 4B-E's own teacher-label
  read (od_gcp label, a seeded permuted view per row) of the 290 of the 3,209 sampled rows that it labelled (the
  others were never labelled). 4B-E never trained on golden_train itself, but 2,896 of the 3,209 sampled states occur
  in its lineage's training files (train_v07 .. train_v13t, train_prism_arms); none of the 290 labelled ones do. The
  numbers are PLUMBING ONLY: they say nothing about the new 4B or about memorisation;
- test_sim_l4_chain: the whole L4 sequence (gate/gate_4b_l4.sh vm-job1, then teacher_switch_l4.sh vm-memo, then
  check) with gate/tests/predict_stub.py in place of od_gcp predict; the memo probabilities are SYNTHETIC.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
PY = str(LEAN.parent / ".venv/bin/python")
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "gate"))
import gate_dev as gd  # noqa: E402
import teacher_switch as ts  # noqa: E402

SPLITS9 = gd.SPLITS.split(",")
LABELS = LEAN / "data/v14_label_shards/labels_q35_4b_pxE"
BACKUP = Path("/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k")
REF_BACKUP = Path("/Users/aryamahadik/Documents/jev/backups/gcp_models/q35_4b_pxE")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


@pytest.fixture(autouse=True)
def _roots(monkeypatch):
    """Every test starts on the real tree and restores the module roots afterwards (main() rebinds them)."""
    monkeypatch.setattr(ts, "ROOT", LEAN)
    monkeypatch.setattr(gd, "ROOT", LEAN)
    monkeypatch.setattr(gd, "_MODE", "teacher_switch")


# ------------------------------------------------------------------------------------------------ the row sets
def test_frozen_lists_match_prereg_text():
    ts.check_frozen_lists()
    fam = Counter()
    for s, n in ts.DEV_SEEN_ROWS.items():
        fam[ts.family(s)] += n
    assert dict(fam) == {"clinc150": 881, "banking77": 559, "pg_*": 1049, "hard_*": 208, "tb_label_nli": 113, "hate": 399}
    assert sum(fam.values()) == 3209
    assert sum(1 for s in ts.DEV_SEEN_ROWS if s.startswith("pg_")) == 7
    assert sum(1 for s in ts.DEV_SEEN_ROWS if s.startswith("hard_")) == 12
    assert ts.TRAIN_POOL["hate"] == ["gd_ghc_hate", "std_hate"]


def test_dev_rows_rederived_from_data_equal_prereg():
    derived, pools, issues = ts.derive_dev_seen(SPLITS9)
    assert issues == []
    assert derived == ts.DEV_SEEN_ROWS and sum(derived.values()) == 3209
    assert pools["hate"] == ["gd_ghc_hate", "std_hate"]
    assert pools["hard_affect"] == ["hard_affect", "hard_affect_c"]
    # none of them is in the frozen unseen (primary-test) set: (d)'s dev rows are exactly PREREG 3.2's seen rows
    # without tb_mixtral (REF lineage only, not golden_train)
    assert not set(derived) & set(gd.UNSEEN_FROZEN_ROWS)


def test_derivation_difference_is_reported():
    gsrc = ts.golden_sources()
    del gsrc["tb_label_nli"]
    gsrc["hard_scales_extra"] = 1
    _, _, issues = ts.derive_dev_seen(SPLITS9, gsrc)
    text = "\n".join(issues)
    assert "family tb_label_nli: derived 0 rows, PREREG 113" in text
    assert "source tb_label_nli: derived None rows, frozen list 113" in text
    assert "source hard_scales: name rule matches ['hard_scales', 'hard_scales_extra']" in text
    assert "total: derived 3096 rows, PREREG 3209" in text


def test_memo_sample_frozen_and_reproducible():
    lines, info, _ = ts.sample_lines()
    data = "".join(lines).encode()
    assert sha(data) == ts.MEMO_SHA256 == ts.sha256_file(LEAN / "data/memo4b_train_rows.jsonl")
    assert (LEAN / "data/memo4b_train_rows.jsonl").read_bytes() == data
    rows = [json.loads(l) for l in lines]
    assert len(rows) == 3209 and len({r["id"] for r in rows}) == 3209
    owner = {k: s for s, v in ts.TRAIN_POOL.items() for k in v}
    assert Counter(owner[r["source"]] for r in rows) == Counter(ts.DEV_SEEN_ROWS)
    assert all(r["split"] == "train" for r in rows)
    man = json.loads((LEAN / ts.MEMO_MANIFEST).read_text())
    assert man["sha256"] == ts.MEMO_SHA256 and man["rows"] == 3209 and man["by_dev_source"] == info
    assert man["dev_rows"]["derivation_issues"] == []
    assert man["training_pass"]["sampled_rows_not_trained"] == []  # every sampled row was in the run's single pass
    # a second draw is byte-identical (seed 0, sorted sources, file order)
    assert "".join(ts.draw(ts.pools_from_golden()[0])[0]) == "".join(lines)


def test_memo_rows_are_golden_train_lines_verbatim():
    want = {json.loads(l)["id"] for l in open(LEAN / "data/memo4b_train_rows.jsonl")}
    memo = {json.loads(l)["id"]: l for l in open(LEAN / "data/memo4b_train_rows.jsonl")}
    found = 0
    with open(LEAN / "data/v14_parts/golden_train.jsonl") as f:
        for l in f:
            i = json.loads(l)["id"]
            if i in want:
                assert memo[i] == l.rstrip("\n") + "\n"
                found += 1
    assert found == 3209


def test_predict_command_parses_and_names_the_file():
    import od_gcp
    out = subprocess.run(["bash", str(LEAN / "gate/teacher_switch_l4.sh"), "plan", "q35_4b_main500k"],
                         capture_output=True, text=True, cwd=LEAN)
    assert out.returncode == 0, out.stderr
    line = next(l for l in out.stdout.splitlines() if "od_gcp.py predict" in l)
    args = line.split("od_gcp.py predict ", 1)[1].split()
    a = od_gcp.parser().parse_args(["predict"] + args)
    assert (a.name, a.base, a.revision, a.layout, a.splits) == ("q35_4b_main500k", "Qwen/Qwen3.5-4B",
                                                                 "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
                                                                 "schema_branch_mark", "memo4b_train_rows")
    assert (a.tag, a.perm_seed, a.tta, a.tta_choice, a.tta_noul, a.force) == ("", None, False, False, False, False)
    assert od_gcp.out_name(a.name, a.tag) == "q35_4b_main500k"


# ------------------------------------------------------------------------------------------------ the arithmetic
def _noul(gold, p_yes, src="clinc150"):
    return ({"qtype": "noul", "gold": gold, "options": None, "source": src}, {"yes": p_yes, "no": 1 - p_yes})


def _choice(gold, probs, src="banking77"):
    return ({"qtype": "choice", "gold": gold, "options": list(probs), "source": src}, probs)


def test_gold_probability_and_ties():
    r, p = _noul(1, 0.7)
    assert ts.p_gold(r, p) == pytest.approx(0.7)
    r, p = _noul(0, 0.7)
    assert ts.p_gold(r, p) == pytest.approx(0.3)
    r, p = _choice("b", {"a": 0.2, "b": 0.5, "c": 0.3})
    assert ts.p_gold(r, p) == 0.5
    tie = _choice("a", {"a": 0.4, "b": 0.4, "c": 0.2})
    assert ts.summarize([tie])["acc"] == 0.0  # a tie for the top is wrong (gate_dev.score)
    assert ts.summarize([_noul(1, 0.5)])["acc"] == 0.0


def _items(n, n_ok, pg_ok=0.8, src="clinc150"):
    """n yes/no rows (gold 1), n_ok of them right with p(yes) = pg_ok, the rest wrong with p(yes) = 0.3."""
    return [_noul(1, pg_ok if i < n_ok else 0.3, src) for i in range(n)]


@pytest.mark.parametrize("tr_ok,dev_ok,acc_pass", [(820, 800, True), (821, 800, False), (700, 800, True)])
def test_accuracy_gap_threshold(tr_ok, dev_ok, acc_pass):
    # 1,000 rows each: 82.0 - 80.0 = 2.0 pp exactly passes; 2.1 fails; a negative gap passes
    tr, dev = _items(1000, tr_ok), _items(1000, dev_ok)
    # p(gold) stays within 0.03 here (right 0.8, wrong 0.3), so the accuracy gap alone decides
    d = ts.memo_gaps(dev, tr)
    assert d["acc_gap_pp"] == pytest.approx((tr_ok - dev_ok) / 10)
    assert d["acc_pass"] is acc_pass


@pytest.mark.parametrize("delta,pg_pass", [(0.03, True), (0.031, False), (-0.15, True)])
def test_pgold_gap_threshold(delta, pg_pass):
    dev = [_noul(1, 0.70) for _ in range(100)]
    tr = [_noul(1, 0.70 + delta) for _ in range(100)]
    d = ts.memo_gaps(dev, tr)
    assert d["acc_gap_pp"] == 0.0 and d["acc_pass"]
    assert d["pgold_gap"] == pytest.approx(delta)
    assert d["pgold_pass"] is pg_pass and d["pass"] is pg_pass


def test_both_gaps_needed():
    dev = [_noul(1, 0.6) for _ in range(50)] + [_noul(1, 0.4) for _ in range(50)]  # 50% right, p(gold) 0.50
    tr = [_noul(1, 0.6) for _ in range(51)] + [_noul(1, 0.4) for _ in range(49)]   # +1 pp, p(gold) 0.502
    assert ts.memo_gaps(dev, tr)["pass"] is True
    tr2 = [_noul(1, 0.9) for _ in range(51)] + [_noul(1, 0.4) for _ in range(49)]  # +1 pp but p(gold) +0.155
    d = ts.memo_gaps(dev, tr2)
    assert d["acc_pass"] and not d["pgold_pass"] and not d["pass"]


def test_qtype_matched_info_gap():
    dev = [_noul(1, 0.8, "s")] * 3 + [_choice("a", {"a": 0.9, "b": 0.1}, "s")] * 1
    tr = [_noul(1, 0.8, "s")] * 1 + [_choice("a", {"a": 0.4, "b": 0.6}, "s")] * 3
    m = ts.matched_gap(dev, tr)
    assert m["dev_rows_covered"] == 4
    assert m["acc_gap_pp"] == pytest.approx((3 * 0 + 1 * -100) / 4)  # yes/no cell 0, choice cell -100 pp


def _sel_rows(n, kc, kr, half="select"):
    return [{"half": half, "ok_c": float(i < kc), "ok_r": float(i < kr)} for i in range(n)]


@pytest.mark.parametrize("kc,kr,ok", [(810, 800, True), (809, 800, False), (900, 800, True), (700, 800, False)])
def test_select_margin_threshold(kc, kr, ok):
    rows = _sel_rows(1000, kc, kr) + _sel_rows(500, 0, 500, "confirm")  # confirm rows never count for (c)
    c = ts.select_margin(rows)
    assert c["n"] == 1000 and c["diff"] == pytest.approx((kc - kr) / 10) and c["pass"] is ok
    assert c["info_confirm"]["diff"] == pytest.approx(-100.0)


# ------------------------------------------------------------------------------------------------ scratch trees
def _tree(tmp: Path, memo_lines: list[str] | None = None) -> Path:
    """A lean/-shaped tree: the 9 splits and golden_train linked read-only, the real pred dirs linked read-only, and
    data/memo4b_train_rows.jsonl (the real one, or memo_lines)."""
    root = tmp / "lean"
    (root / "data").mkdir(parents=True)
    for s in SPLITS9:
        (root / f"data/{s}.jsonl").symlink_to(LEAN / f"data/{s}.jsonl")
        (root / f"preds_{s}").symlink_to(LEAN / f"preds_{s}")
    (root / "data/v14_parts").symlink_to(LEAN / "data/v14_parts")
    m = root / "data/memo4b_train_rows.jsonl"
    if memo_lines is None:
        m.symlink_to(LEAN / "data/memo4b_train_rows.jsonl")
    else:
        m.write_text("".join(memo_lines))
    (root / "preds_memo4b_train_rows").mkdir()
    return root


def _label_probs(ids):
    out, meta = {}, None
    for f in sorted(LABELS.glob("shard_*.jsonl")):
        for l in open(f):
            r = json.loads(l)
            if r["id"] in ids:
                out[r["id"]] = r["probs"]
        if meta is None:
            meta = json.loads(f.with_suffix(".meta.json").read_text())
    return out, meta


def _write_preds(root, name, rows, probs, meta):
    d = root / "preds_memo4b_train_rows"
    with open(d / f"{name}.jsonl", "w") as f:
        for r in rows:
            if r["id"] in probs:
                f.write(json.dumps({"id": r["id"], "model": name, "probs": probs[r["id"]]}) + "\n")
    (d / f"{name}.meta.json").write_text(json.dumps(meta, indent=2))


def test_check_refuses_incomplete_memo_read(tmp_path):
    root = _tree(tmp_path)
    rows = [json.loads(l) for l in open(LEAN / "data/memo4b_train_rows.jsonl")]
    probs, lmeta = _label_probs({r["id"] for r in rows})
    _write_preds(root, "q35_4b_pxE_parity", rows, probs, {"name": "x", "rows": len(probs)})
    with pytest.raises(SystemExit, match=r"lacks 2919 of 3209 rows"):
        ts.main(["check", "q35_4b_pxE_parity", "q35_4b_pxE", "--root", str(root), "--no-rederive"])


def test_check_refuses_other_memo_file(tmp_path):
    lines = open(LEAN / "data/memo4b_train_rows.jsonl").readlines()
    root = _tree(tmp_path, lines[:-1])  # one row short: another file
    with pytest.raises(SystemExit, match="is not the frozen MEMO_SHA256"):
        ts.main(["check", "q35_4b_pxE_parity", "q35_4b_pxE", "--root", str(root), "--no-rederive"])


def test_check_refuses_missing_dev_preds(tmp_path):
    root = _tree(tmp_path)
    with pytest.raises(SystemExit, match="must be complete"):
        ts.main(["check", "no_such_model_4b", "q35_4b_pxE", "--root", str(root), "--no-rederive"])


def test_standin_4bE(tmp_path, monkeypatch, capsys):
    """PLUMBING ONLY: 4B-E as a stand-in candidate (see the module docstring)."""
    rows = [json.loads(l) for l in open(LEAN / "data/memo4b_train_rows.jsonl")]
    probs, lmeta = _label_probs({r["id"] for r in rows})
    assert len(probs) == 290
    for r in rows:  # the label read is keyed by the row's own options
        if r["id"] in probs:
            assert set(probs[r["id"]]) == ({"yes", "no"} if r["qtype"] == "noul" else set(r["options"]))
    keep = [l for l in open(LEAN / "data/memo4b_train_rows.jsonl") if json.loads(l)["id"] in probs]
    root = _tree(tmp_path, keep)
    monkeypatch.setattr(ts, "MEMO_SHA256", sha("".join(keep).encode()))
    meta = {"name": "q35_4b_pxE_parity", "rows": len(keep), "stand_in": "4B-E teacher labels (od_gcp label)",
            "base": lmeta["settings"]["base"], "perm_seed": lmeta["settings"]["perm_seed"], "tta": False,
            "layout": lmeta["load"]["layout"], "style": lmeta["style"], "load": lmeta["load"]}
    _write_preds(root, "q35_4b_pxE_parity", rows, probs, meta)
    out = tmp_path / "standin.json"
    other = tmp_path / "look_ship_other.json"  # a ship look of this CAND against ANOTHER REF: (b) not found here
    other.write_text(json.dumps({"mode": "ship", "cand": "q35_4b_pxE_parity", "ref": "q35_4b_pxE_fresh2",
                                 "verdict": "SHIP", "final": True}))
    res = ts.main(["check", "q35_4b_pxE_parity", "q35_4b_pxE", "--root", str(root), "--json", str(out),
                   "--ship-json", str(other)])
    text = capsys.readouterr().out
    with capsys.disabled():
        print("\n===== STAND-IN, PLUMBING ONLY (4B-E as candidate; 290-row label subset on the training side) =====")
        print(text)
    assert res["c"]["n"] == sum(1 for x in gd.complete_rows(SPLITS9, "q35_4b_pxE_parity", "q35_4b_pxE")
                                if x["half"] == "select")
    assert res["d"]["dev"]["n"] == 3209 and res["d"]["train"]["n"] == 290
    assert res["final"] is False
    nf = "\n".join(res["not_final"])
    assert "stored 4B-E read" in nf and "q35_4b_pxE: path train-in-process" in nf
    assert "perm_seed 20260930" in nf and "meta says 290 rows" in nf
    assert res["b"] is None and "none of the --ship-json looks is q35_4b_pxE_parity vs q35_4b_pxE" in nf
    j = json.loads(out.read_text())
    assert j["d"]["acc_gap_pp"] == pytest.approx(res["d"]["acc_gap_pp"]) and j["memo_sha256"] == ts.MEMO_SHA256


# ------------------------------------------------------------------------------------------------ the L4 sequence
SIM_FILES = ("gate_dev.py", "od_gcp.py", "decoder_io.py", "prism_x.py", "writeblock.py", "ship_unseen_sources.json")
ADAPTER_FILES = ("adapter_config.json", "adapter_model.safetensors", "tokenizer.json", "tokenizer_config.json",
                 "chat_template.jinja", "train_meta.json")
# gate/tests/sim_gate.py A_ship: a slightly better C1 (stub gives it the gold side on 4% of yes/no rows) -> SHIP
SHIP_MAP = {"q35_4b_main500k": {"improve_noul": 0.04}, "q35_4b_main500k_c2": {"improve_noul": 0.02}}


def _sim_tree(root: Path):
    root.mkdir(parents=True)
    (root / "data").symlink_to(LEAN / "data")  # read-only use: the jobs write only preds_*/, models/, logs/
    for f in SIM_FILES:
        shutil.copy2(LEAN / f, root / f)
    (root / "runs").mkdir()
    shutil.copy2(LEAN / "runs/q35_4b_main.json", root / "runs")
    shutil.copytree(LEAN / "gate", root / "gate", ignore=shutil.ignore_patterns("__pycache__", "manifest_*"))
    for s in SPLITS9:
        (root / f"preds_{s}").mkdir()
        for n in ("q35_4b_pxE", "q35_4b_pxE_parity", "q35_4b_pxE_tta"):
            for ext in (".jsonl", ".meta.json"):
                shutil.copy2(LEAN / f"preds_{s}/{n}{ext}", root / f"preds_{s}")
    for s in ("eval_jagged", "eval_opi", "eval_redef"):
        (root / f"preds_{s}").mkdir()
        for ext in (".jsonl", ".meta.json"):
            shutil.copy2(LEAN / f"preds_{s}/q35_4b_pxE{ext}", root / f"preds_{s}")
    m = root / "models"
    m.mkdir()
    (m / "q35_4b_pxE").symlink_to(REF_BACKUP)
    fin = m / "q35_4b_main500k"
    (fin / "snaps").mkdir(parents=True)
    for f in ADAPTER_FILES:  # the REAL final adapter and snapshots, linked read-only
        (fin / f).symlink_to(BACKUP / f)
    for s in ("s025888", "s027411", "s028934"):
        (fin / "snaps" / s).symlink_to(BACKUP / "snaps" / s)
    (root / "logs").mkdir()
    # the stub copies probabilities from preds_<split>/<src>.jsonl: a SYNTHETIC source for the memo rows
    d = root / "preds_memo4b_train_rows"
    d.mkdir()
    with open(d / "q35_4b_pxE_parity.jsonl", "w") as f:
        for l in open(LEAN / "data/memo4b_train_rows.jsonl"):
            r = json.loads(l)
            h = int(hashlib.sha256(r["id"].encode()).hexdigest(), 16) % 100
            ok = h >= 12  # 88% right
            if r["qtype"] == "noul":
                py = (0.8 if ok else 0.3) if r["gold"] == 1 else (0.2 if ok else 0.7)
                p = {"yes": py, "no": 1 - py}
            else:
                o = r["options"]
                tgt = r["gold"] if ok else next(x for x in o if x != r["gold"])
                p = {x: (0.8 if x == tgt else 0.2 / (len(o) - 1)) for x in o}
            f.write(json.dumps({"id": r["id"], "model": "synthetic", "probs": p}) + "\n")


def _run(root, script, phase, *args, extra=None):
    env = {**os.environ, "LEAN": str(root), "PY": PY, "GATE_SIM": "1", "NO_SHUTDOWN": "1",
           "PREDICT_CMD": f"{PY} gate/tests/predict_stub.py", "BACKUP": str(root / "models/q35_4b_main500k"),
           "GATE_STUB_MAP": str(root / "stub_map.json"), **(extra or {})}
    p = subprocess.run(["bash", str(root / "gate" / script), phase, *args], env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def test_vm_memo_refuses_other_rows_file(tmp_path):
    """The VM read stops (exit 2) before any model work when data/memo4b_train_rows.jsonl is not the frozen file."""
    root = tmp_path / "lean"
    (root / "data").mkdir(parents=True)
    lines = open(LEAN / "data/memo4b_train_rows.jsonl").readlines()
    (root / "data/memo4b_train_rows.jsonl").write_text("".join(lines[1:]))
    shutil.copy2(LEAN / "gate_dev.py", root / "gate_dev.py")
    shutil.copytree(LEAN / "gate", root / "gate", ignore=shutil.ignore_patterns("__pycache__", "manifest_*"))
    rc, log = _run(root, "teacher_switch_l4.sh", "vm-memo", "q35_4b_main500k")
    assert rc == 2 and "is not the frozen 8ec3029c" in log, log
    assert not (root / "preds_memo4b_train_rows").exists()


@pytest.mark.slow
@pytest.mark.skipif(not (BACKUP / "train_meta.json").exists() or not REF_BACKUP.exists(), reason="adapters not here")
def test_sim_l4_chain(tmp_path):
    root = tmp_path / "lean"
    _sim_tree(root)
    (root / "stub_map.json").write_text(json.dumps(SHIP_MAP))
    rc, log = _run(root, "gate_4b_l4.sh", "manifest")
    assert rc == 0, log
    rc, log = _run(root, "gate_4b_l4.sh", "vm-job1")
    sm = json.loads((root / "logs/gate4b/summary.json").read_text())
    assert rc == 0 and sm["outcome"] == "ship:q35_4b_main500k", log[-3000:]
    c_sum = sm["teacher_switch_c_dev_select_diff_pp"]
    memo_pred = root / "preds_memo4b_train_rows/q35_4b_main500k.jsonl"
    # vm-memo without a CAND reads only after a SHIP with (c) >= +1.0 (summary.json); the stub's C1 is only a little
    # better, so the summary is edited here to drive each branch
    sp = root / "logs/gate4b/summary.json"
    keep = sp.read_text()
    sp.write_text(json.dumps({**sm, "outcome": "fallback:q35_4b_pxE"}))
    rc, log = _run(root, "teacher_switch_l4.sh", "vm-memo")
    assert rc == 0 and "(b) fails, the teacher stays 4B-E; memorisation read skipped" in log and not memo_pred.exists()
    sp.write_text(json.dumps({**sm, "teacher_switch_c_dev_select_diff_pp": 0.5}))
    rc, log = _run(root, "teacher_switch_l4.sh", "vm-memo")
    assert rc == 0 and "margin 0.500000 pp < +1.0" in log and not memo_pred.exists()
    # an explicit CAND always reads
    rc, log = _run(root, "teacher_switch_l4.sh", "vm-memo", "q35_4b_main500k")
    assert rc == 0 and "MEMO meta vs preds_dev/q35_4b_main500k: same settings" in log, log
    assert sum(1 for _ in open(memo_pred)) == 3209
    # the automatic path after a SHIP with (c) >= 1.0 reaches the read (already made: skipped, not repeated)
    sp.write_text(json.dumps({**sm, "teacher_switch_c_dev_select_diff_pp": 1.5}))
    rc, log = _run(root, "teacher_switch_l4.sh", "vm-memo")
    assert rc == 0 and "SHIP q35_4b_main500k and (c) margin 1.500000 pp >= +1.0" in log and "already complete, skipped" in log
    sp.write_text(keep)
    rc, log = _run(root, "teacher_switch_l4.sh", "check")
    print("\n===== L4-SEQUENCE SIMULATION (stub reads; SYNTHETIC memo probabilities) =====\n" + log)
    assert rc == 0, log
    res = json.loads((root / "logs/gate4b/teacher_switch.json").read_text())
    assert res["cand"] == "q35_4b_main500k" and res["ref"] == "q35_4b_pxE_fresh"
    assert res["b"]["pass"] is True and res["b"]["look"].endswith("look_ship1.json")
    assert res["c"]["diff"] == pytest.approx(c_sum)  # the same number as gate_4b_l4.sh's summary
    assert res["d"]["dev"]["n"] == 3209 and res["d"]["train"]["n"] == 3209
    assert res["final"] is True, res["not_final"]
