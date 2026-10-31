"""ab_readout.py (SPEC 11.5-11.6) on a synthetic fixture tree with gate_dev's layout (data/, preds_*/)."""
from __future__ import annotations

import json

import pytest

import ab_readout as ar
import gate_dev as gd
from conftest import write_jsonl

A, B, C = "armA", "armB", "armC"


def _p_noul(gold, right, conf=0.9):
    p = conf if right else 1 - conf
    py = p if gold == 1 else 1 - p
    return {"yes": py, "no": 1 - py}


def _p_choice(opts, gold, right, conf=0.8):
    tgt = gold if right else next(o for o in opts if o != gold)
    return {o: (conf if o == tgt else (1 - conf) / (len(opts) - 1)) for o in opts}


def _write_preds(root, split, name, rows, fn, perm=False):
    d = root / (f"preds_{split}" if split != "eval" else "preds")
    write_jsonl(d / f"{name}.jsonl", [{"id": r["id"], "probs": fn(r)} for r in rows])
    if perm:
        write_jsonl(d / f"{name}_perm.jsonl", [{"id": r["id"], "probs": {k: min(1.0, v + 1e-3) for k, v in fn(r).items()}}
                                               for r in rows])
        (d / f"{name}_perm.meta.json").write_text(json.dumps({"perm_seed": 1}))


def build(root, b_worse=0.0, c_sharper=False, with_yn2b=True, jag_b_hijack=1):
    splits = gd.SPLITS.split(",")
    for sp in splits:
        rows = []
        for i in range(60):
            src = "ag_news" if sp == "dev" else "src_" + sp
            if i < 40:
                rows.append({"id": f"{sp}{i}", "group_id": f"{sp}g{i}", "source": src, "qtype": "noul", "gold": i % 2,
                             "options": None, "state": "s"})
            else:
                rows.append({"id": f"{sp}{i}", "group_id": f"{sp}g{i}", "source": src, "qtype": "choice", "gold": "a",
                             "options": ["a", "b", "c"], "state": "s"})
        write_jsonl(root / f"data/{sp}.jsonl", rows)
        write_jsonl(root / f"data/{sp}_relations.jsonl", [{"type": "equiv", "a": f"{sp}0", "b": f"{sp}2"}])

        def base(r, conf_yes=0.9):
            k = int(r["id"][len(sp):])
            right = k % 5 != 0
            return _p_noul(r["gold"], right, conf_yes if k % 2 else 0.75) if r["qtype"] == "noul" else \
                _p_choice(r["options"], r["gold"], right)

        def worse(r):
            k = int(r["id"][len(sp):])
            if b_worse and k % 5 != 0 and k % int(1 / b_worse) == 1:
                return _p_noul(r["gold"], False) if r["qtype"] == "noul" else _p_choice(r["options"], r["gold"], False)
            return base(r)

        def sharper(r):
            k = int(r["id"][len(sp):])
            if r["qtype"] == "noul" and k % 5 != 0:
                return _p_noul(r["gold"], True, 0.97)
            return worse(r)

        _write_preds(root, sp, A, rows, base, perm=True)
        _write_preds(root, sp, B, rows, worse, perm=True)
        _write_preds(root, sp, C, rows, sharper if c_sharper else worse, perm=True)
    # attacks: jagged (20 items), opi (10 clean texts x 2 attacks), redef (30 rows)
    jag = []
    for i in range(20):
        jag += [{"id": f"jb{i}", "gold": 1, "meta": {"item_id": f"i{i}", "arm": "baseline"}},
                {"id": f"ja{i}", "gold": 1, "meta": {"item_id": f"i{i}", "arm": "adversarial"}}]
    write_jsonl(root / "data/eval_jagged.jsonl", jag)
    for name, hij in ((A, 1), (B, jag_b_hijack), (C, jag_b_hijack)):
        write_jsonl(root / f"preds_eval_jagged/{name}.jsonl",
                    [{"id": r["id"], "probs": {"yes": 0.2 if (r["id"].startswith("ja") and int(r["id"][2:]) < hij) else 0.9}}
                     for r in jag])
    opi = []
    for i in range(10):
        opi.append({"id": f"c{i}", "track": "CLEAN", "options": ["x", "y"], "gold": "x", "meta": {}})
        opi += [{"id": f"o{i}_{k}", "track": "OPI", "options": ["x", "y"], "gold": "x",
                 "meta": {"clean_id": f"c{i}", "attack_target": "y"}} for k in range(2)]
    write_jsonl(root / "data/eval_opi.jsonl", opi)
    for name in (A, B, C):
        write_jsonl(root / f"preds_eval_opi/{name}.jsonl", [{"id": r["id"], "probs": {"x": 0.9, "y": 0.1}} for r in opi])
    red = [{"id": f"rd{i}", "qtype": "choice", "options": ["p", "q"], "gold": "p"} for i in range(30)]
    write_jsonl(root / "data/eval_redef.jsonl", red)
    for name in (A, B, C):
        write_jsonl(root / f"preds_eval_redef/{name}.jsonl", [{"id": r["id"], "probs": {"p": 0.8, "q": 0.2}} for r in red])
    if with_yn2b:
        fams = ar.WAVE1
        dev = []
        for i in range(120):
            kind = "holdout" if i < 60 else "iid"
            dev.append({"id": f"y{i}", "source": fams[i % len(fams)], "qtype": "noul", "gold": i % 2, "options": None,
                        "meta": {"latent_id": f"L{i // 2}", "dev_kind": kind, "view": "base"}})
        devx = [{"id": f"x{i}", "source": fams[i % 5], "qtype": "noul", "gold": i % 2, "options": None,
                 "meta": {"latent_id": f"X{i}", "dev_kind": "devx"}} for i in range(60)]
        write_jsonl(root / "data/yn2b_dev.jsonl", dev)
        write_jsonl(root / "data/yn2b_devx.jsonl", devx)
        for split, rows in (("yn2b_dev", dev), ("yn2b_devx", devx)):
            _write_preds(root, split, A, rows, lambda r: _p_noul(r["gold"], int(r["id"][1:]) % 5 < 2, 0.6))
            for n in (B, C):
                _write_preds(root, split, n, rows, lambda r: _p_noul(r["gold"], int(r["id"][1:]) % 7 != 3, 0.95))
    return root


@pytest.fixture()
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(gd, "ROOT", tmp_path)
    return tmp_path


def _status(res, prefix, key="B_vs_A"):
    part = res[key] if key == "B_vs_A" else res["C_rule"]
    return [x["status"] for x in part["constraints"] if x["name"].startswith(prefix)]


def test_pass_when_b_equals_a_outside_yn2b_and_learns_yn2b(root):
    build(root)
    res = ar.readout(A, B, C)
    assert res["verdict"] == "PASS", [x for x in res["B_vs_A"]["constraints"] if x["status"] != "PASS"]
    assert res["dropped_families"] == []
    assert res["C_rule"]["verdict"] == "FAIL"  # C == B: the committed-accuracy gain of +1.0 pp is missing
    assert "FAIL" in _status(res, "C-B committed", "C")


def test_arm_c_pass_when_sharper(root):
    build(root, c_sharper=True)
    res = ar.readout(A, B, C)
    assert res["C_rule"]["verdict"] == "PASS", [x for x in res["C_rule"]["constraints"] if x["status"] == "FAIL"]


def test_nr1_fails_on_a_full_set_loss(root):
    build(root, b_worse=1 / 10)
    res = ar.readout(A, B)
    assert res["verdict"] == "FAIL" and _status(res, "NR1") == ["FAIL"]


def test_incomplete_without_yn2b_reads(root):
    build(root, with_yn2b=False)
    res = ar.readout(A, B)
    assert res["verdict"] == "INCOMPLETE"
    assert "UNMEASURED" in _status(res, "G1")


def test_nr5_needs_cap_and_significance(root):
    build(root, jag_b_hijack=3)   # 15% > 6.9% cap, but 3 vs 1 of 20 items: the LB of the increase is not > 0
    res = ar.readout(A, B)
    assert _status(res, "NR5 jagged") == ["PASS"]
    build(root, jag_b_hijack=12)  # 60% vs 5%: over the cap and significant -> FAIL
    res = ar.readout(A, B)
    assert _status(res, "NR5 jagged") == ["FAIL"] and res["verdict"] == "FAIL"


def test_committed_accuracy_definition():
    x = {"qtype": "noul", "gold": 1, "options": None, "p_c": {"yes": 0.85, "no": 0.15}, "p_r": {"yes": 0.7, "no": 0.3}}
    assert [(r["ok_c"], r["ok_r"]) for r in ar.committed([x])] == [(1.0, 0.0)]
    y = {"qtype": "choice", "gold": "a", "options": ["a", "b"], "p_c": {"a": 0.4, "b": 0.1}, "p_r": {"a": 0.5, "b": 0.5}}
    assert [(r["ok_c"], r["ok_r"]) for r in ar.committed([y])] == [(1.0, 0.0)]  # renormalised: 0.4 / 0.5 = 0.8


def test_cli_writes_json_and_one_look(root, tmp_path):
    build(root)
    ar.main(["--root", str(root), "--a", A, "--b", B])
    assert json.loads((root / "logs/yn2b_ab.json").read_text())["verdict"] == "PASS"
    assert len((root / "logs/yn2b_ab_looks.jsonl").read_text().splitlines()) == 1
    assert not (root / "logs/ship_looks.jsonl").exists()


def test_family_with_negative_pooled_gain_is_dropped(root):
    build(root)
    fam = ar.WAVE1[1]
    for split in ("yn2b_dev", "yn2b_devx"):
        rows = [json.loads(l) for l in open(root / f"data/{split}.jsonl")]
        _write_preds(root, split, B, rows, lambda r: _p_noul(r["gold"], r["source"] != fam, 0.95))
    res = ar.readout(A, B)
    assert res["dropped_families"] == [fam]


def _split_dev_files(root):
    """data/yn2b_dev.jsonl -> data/yn2b_dev_iid.jsonl + data/yn2b_dev_holdout.jsonl, preds split the same way."""
    dev = [json.loads(l) for l in open(root / "data/yn2b_dev.jsonl")]
    kind = {r["id"]: r["meta"]["dev_kind"] for r in dev}
    for k in ("iid", "holdout"):
        write_jsonl(root / f"data/yn2b_dev_{k}.jsonl", [r for r in dev if r["meta"]["dev_kind"] == k])
        for name in (A, B, C):
            pr = [json.loads(l) for l in open(root / f"preds_yn2b_dev/{name}.jsonl")]
            write_jsonl(root / f"preds_yn2b_dev_{k}/{name}.jsonl", [x for x in pr if kind[x["id"]] == k])
    (root / "data/yn2b_dev.jsonl").unlink()


def test_split_dev_files_give_the_same_readout(root):
    """Owner decision (wave-1a issue 6): the dev rows may live in yn2b_dev_iid + yn2b_dev_holdout instead of yn2b_dev."""
    build(root)
    one = ar.readout(A, B)
    _split_dev_files(root)
    two = ar.readout(A, B)
    assert two["verdict"] == one["verdict"] == "PASS"
    for k in ("G1_holdout", "G1_committed", "G1x_devx", "dev_iid"):
        assert two["B_vs_A"]["numbers"][k]["diff"] == pytest.approx(one["B_vs_A"]["numbers"][k]["diff"])
        assert two["B_vs_A"]["numbers"][k]["n"] == one["B_vs_A"]["numbers"][k]["n"]


def test_split_dev_files_missing_one_half_is_unmeasured(root):
    build(root)
    _split_dev_files(root)
    (root / "preds_yn2b_dev_holdout" / f"{B}.jsonl").unlink()
    res = ar.readout(A, B)
    assert "UNMEASURED" in _status(res, "G1") and res["verdict"] != "PASS"
