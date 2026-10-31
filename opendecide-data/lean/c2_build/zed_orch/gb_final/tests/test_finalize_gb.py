"""Tests for zed_orch/gb_final/finalize_gb.py (Ruling A66): the GB QC-record writer. Pure-function checks on small synthetic fixtures and
an integration run on a symlink copy of the live GB files (the live files are never modified: a test that changes a file first replaces
its symlink with a private copy). Run from c2_build:
  ../../.venv/bin/python -B -m pytest -q -p no:cacheprovider zed_orch/gb_final/tests/test_finalize_gb.py
"""
from __future__ import annotations

import datetime
import json
import os
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import finalize_gb as F  # noqa: E402

BUILD = F.BUILD
LIVE = F.Paths()
UTC = datetime.timezone.utc
NOW = datetime.datetime(2026, 10, 17, 10, 0, 0, tzinfo=UTC)


# ------------------------------------------------------------------ synthetic fixtures for the pure checks

def base_row(i, qtype="noul", label="yes", card="gb_x_1_c0"):
    gold = (1 if label == "yes" else 0) if qtype == "noul" else label
    return {"id": f"c2_gblock:t{i}:{card}", "qtype": qtype, "gold": gold, "meta": {"card_id": card}}


def routed(r, source="haiku_agree_low", conf=0.9, label=None):
    lab = label or (("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"])
    return {"id": r["id"], "label": lab, "conf": conf, "source": source, "card_id": r["meta"]["card_id"], "qtype": r["qtype"], "domain": "d"}


def popu(ids_kept, ids_mix=(), n_drop=0, audit=()):
    pop = [{"id": i, "status": "haiku_accepted", "mixdev": False, "domain": "d", "label": "yes"} for i in ids_kept]
    pop += [{"id": i, "status": "opus_kept", "mixdev": True, "domain": "d", "label": "yes"} for i in ids_mix]
    pop += [{"id": f"drop{k}", "status": "a39_dropped", "mixdev": False, "domain": "d", "label": "yes"} for k in range(n_drop)]
    for r in pop:
        if r["id"] in audit:
            r["opus_audit_label"] = "yes" if audit[r["id"]] else "no"
    return pop


def qc_labels(h, o, d):
    return {"haiku_accepted_conf_ge_0.80": h, "opus_kept_conf_ge_0.85": o, "a39_dropped_low_conf": d, "labelled_pool": h + o}


def label_case(**kw):
    base = [base_row(i) for i in range(4)]
    rt = [routed(r) for r in base]
    pop = popu([r["id"] for r in base], ["m1"], n_drop=2, audit={base[0]["id"]: True, base[1]["id"]: True})
    args = dict(base=base, routed=rt, pop=pop, accepted_n=4, opus_kept_n=1, mixdev_ids={"m1"},
                qc_labels=qc_labels(4, 1, 2), qc_audit={"audit_items_read": 2, "disagreements": 0})
    args.update(kw)
    return args


def test_labels_pass():
    rep, p = F.label_problems(**label_case())
    assert p == [] and rep["audit"] == {"read": 2, "disagreements": 0, "worst_domain_rate": 0.0}


def test_labels_gold_differs_from_routed_label():
    a = label_case()
    a["routed"][0]["label"] = "no"
    _, p = F.label_problems(**a)
    assert any("gold differs from the routed label" in x for x in p)


def test_labels_choice_gold_is_the_label_string():
    base = [base_row(0, "choice", "money", "gb_x_2_c1")]
    a = label_case(base=base, routed=[routed(base[0])], pop=popu([base[0]["id"]], ["m1"]), accepted_n=1, opus_kept_n=1,
                   qc_labels=qc_labels(1, 1, 0), qc_audit={"audit_items_read": 0, "disagreements": 0})
    assert F.label_problems(**a)[1] == []
    a["routed"][0]["label"] = "rules"
    assert any("gold differs" in x for x in F.label_problems(**a)[1])


@pytest.mark.parametrize("source,conf,bad", [("haiku_agree_low", 0.80, False), ("haiku_agree_low", 0.79, True),
                                             ("opus_a39", 0.85, False), ("opus_a39", 0.80, True)])
def test_labels_confidence_floors(source, conf, bad):
    a = label_case()
    a["routed"][0]["source"], a["routed"][0]["conf"] = source, conf
    assert any("under its A39 floor" in x for x in F.label_problems(**a)[1]) is bad


def test_labels_row_not_routed_and_routed_in_mixdev():
    a = label_case()
    a["routed"] = a["routed"][1:]
    assert any("base rows != routed block" in x for x in F.label_problems(**a)[1])
    a = label_case(mixdev_ids={"m1", label_case()["base"][0]["id"]})
    assert any("in the mixdev" in x for x in F.label_problems(**a)[1])


def test_labels_counts_must_equal_the_qc_record_and_files():
    assert any("accepted_haiku.jsonl rows" in x for x in F.label_problems(**label_case(accepted_n=5))[1])
    assert any("opus_finalize_A39" in x for x in F.label_problems(**label_case(opus_kept_n=2))[1])
    assert any("A39_labels.a39_dropped_low_conf" in x for x in F.label_problems(**label_case(qc_labels=qc_labels(4, 1, 3)))[1])


def test_labels_audit_disagreement_over_six_percent_and_record_mismatch():
    base = label_case()["base"]
    pop = popu([r["id"] for r in base], ["m1"], n_drop=2, audit={base[0]["id"]: False, base[1]["id"]: True})
    _, p = F.label_problems(**label_case(pop=pop, qc_audit={"audit_items_read": 2, "disagreements": 1}))
    assert any("disagrees" in x and "0.5" in x for x in p) and not any("QC A39_5pct" in x for x in p)
    _, p = F.label_problems(**label_case(qc_audit={"audit_items_read": 2, "disagreements": 1}))
    assert any("QC A39_5pct_opus_audit" in x for x in p)


def test_mixdev_rules(monkeypatch):
    monkeypatch.setattr(F, "MIXDEV_ROWS", 4)
    monkeypatch.setattr(F, "MIXDEV_PER_DOMAIN", 2)
    dev = [{"id": f"m{i}", "meta": {"sampler": "S5", "dev_only": True}} for i in range(4)]
    pop = {f"m{i}": {"domain": "a" if i < 2 else "b", "mixdev": True} for i in range(4)} | {"c1": {"domain": "a", "mixdev": False}}
    mj = {"ids": {"a": ["m0", "m1"], "b": ["m2", "m3"]}}
    assert F.mixdev_problems(dev, {"c1"}, pop, mj, {"rows": 4})[1] == []
    assert any("among the candidates" in x for x in F.mixdev_problems(dev, {"m0"}, pop, mj, {"rows": 4})[1])
    assert any("mixdev_ids.json" in x for x in F.mixdev_problems(dev, {"c1"}, pop, {"ids": {"a": ["m0"]}}, {"rows": 4})[1])
    pop["m3"]["mixdev"] = False
    assert any("population's mixdev flags" in x for x in F.mixdev_problems(dev, {"c1"}, pop, mj, {"rows": 4})[1])
    pop["m3"]["mixdev"] = True
    pop["m3"]["domain"] = "a"
    assert any("per domain" in x for x in F.mixdev_problems(dev, {"c1"}, pop, mj, {"rows": 4})[1])
    dev[0]["meta"]["dev_only"] = False
    assert any("S5 / dev_only" in x for x in F.mixdev_problems(dev, {"c1"}, pop, mj, {"rows": 4})[1])
    assert any("row count" in x for x in F.mixdev_problems(dev, {"c1"}, pop, mj, {"rows": 3})[1])


def twin_rows(n=3):
    rows = [{"id": f"b{i}", "meta": {}} for i in range(n)]
    rows += [{"id": f"t{i}", "meta": {"twin_of": f"b{i}", "negtwin": {"pattern": f"P{i}"}}} for i in range(n)]
    rels = [{"a": f"b{i}", "b": f"t{i}", "type": "equiv"} for i in range(n)]
    return rows, rels


def test_twins_checks(monkeypatch):
    monkeypatch.setattr(F.K, "g_tw", lambda pairs: {"n_pairs": len(pairs), "violations": 0, "pass": True})
    rows, rels = twin_rows()
    assert F.twin_problems(rows, rels, {"P0", "P1", "P2"}, [])[1] == []
    assert any("outside the frozen trained catalogue" in x for x in F.twin_problems(rows, rels, {"P0", "P1"}, [])[1])
    assert any("pooled audit dropped" in x for x in F.twin_problems(rows, rels, {"P0", "P1", "P2"}, ["P2"])[1])
    assert any("relations" in x for x in F.twin_problems(rows, rels[:2], {"P0", "P1", "P2"}, [])[1])
    bad = [dict(rels[0], a="b1")] + rels[1:]
    assert any("base" in x for x in F.twin_problems(rows, bad, {"P0", "P1", "P2"}, [])[1])
    rows[3]["meta"]["twin_of"] = "gone"
    assert any("twins with a base" in x for x in F.twin_problems(rows, rels, {"P0", "P1", "P2"}, [])[1])
    monkeypatch.setattr(F.K, "g_tw", lambda pairs: {"n_pairs": len(pairs), "violations": 2, "pass": False})
    rows, rels = twin_rows()
    assert any("G-TW" in x for x in F.twin_problems(rows, rels, {"P0", "P1", "P2"}, [])[1])


def comp(block, kind, i):
    return {"id": f"{block}{kind}{i}", "role": "complement", "meta": {"twin_of": f"x{i}", "negtwin": {"kind": kind, "pattern": f"p{kind}{i}"}}}


def a60_case(counts=(("syntactic", 3), ("implicit", 3), ("antonym", 4)), **kw):
    rows = [comp("GB", k, i) for k, n in counts for i in range(n)]
    parts = {"GB": rows, "MD": [], "RTW": []}
    hold = [comp("H", "syntactic", i) for i in range(2)]
    rec = {"pooled_after": {"by_kind": {k: n for k, n in counts}, "problems": []}, "block_rule_problems": [],
           "hold": {"rows": 2, "relations": 2, "rows_sha256": "a", "relations_sha256": "b"},
           "block": {"rows_before": len(rows) + 2, "rows_after": len(rows)}, "equiv_twins_untouched": True}
    args = dict(parts=parts, rec=rec, hold_rows=hold, hold_rels=[{}, {}], hold_sha=("a", "b"))
    args.update(kw)
    return args


def test_a60_pass_and_share_failures():
    rep, p = F.a60_problems(**a60_case())
    assert p == [] and rep["by_kind"] == {"syntactic": 3, "implicit": 3, "antonym": 4}
    _, p = F.a60_problems(**a60_case(counts=(("syntactic", 6), ("implicit", 3), ("antonym", 1))))
    assert any("antonym" in x for x in p) and any("syntactic" in x for x in p)      # shares recomputed from the rows, not the record


def test_a60_record_vs_files():
    a = a60_case()
    a["rec"]["pooled_after"]["by_kind"]["antonym"] = 5
    assert any("recomputed pooled complement counts" in x for x in F.a60_problems(**a)[1])
    assert any("hold rows file differs" in x for x in F.a60_problems(**a60_case(hold_sha=("z", "b")))[1])
    assert any("hold relations file differs" in x for x in F.a60_problems(**a60_case(hold_sha=("a", "z")))[1])
    assert any("held row is not a complement" in x for x in F.a60_problems(**a60_case(hold_rows=[{"id": "h", "role": "equiv", "meta": {}}] * 2))[1])
    a = a60_case()
    a["hold_rows"] = [dict(a["hold_rows"][0], id=a["parts"]["GB"][0]["id"]), a["hold_rows"][1]]
    assert any("also a candidate" in x for x in F.a60_problems(**a)[1])
    a = a60_case()
    a["rec"]["block"]["rows_before"] += 1
    assert any("rows_before" in x for x in F.a60_problems(**a)[1])
    a = a60_case()
    a["rec"]["equiv_twins_untouched"] = False
    assert any("equiv_twins_untouched" in x for x in F.a60_problems(**a)[1])


def test_a60_pools_over_md_and_rtw_files():
    a = a60_case(counts=(("syntactic", 1), ("implicit", 1), ("antonym", 1)))
    a["parts"]["MD"] = [comp("MD", "syntactic", i) for i in range(30)]       # the pool is GB + MD + RTW: this breaks antonym / implicit
    a["rec"]["pooled_after"]["by_kind"] = {"syntactic": 31, "implicit": 1, "antonym": 1}
    a["rec"]["block"]["rows_before"] = 5
    assert any("implicit" in x for x in F.a60_problems(**a)[1])


def test_audit_record_checks():
    qc = {"negtwin_audit": {"final_twins": 5, "sampled": 9, "opus_confirmed_errors": 1, "batch_id": "B"},
          "negtwin_gates": {"g_tw": {"pass": True}}}
    rep = {"final_twins": {"GB": 5}, "final_rows": {"GB": 50}, "dry_run": False, "sampled": 9, "opus_confirmed_errors": 1, "batch_id": "B",
           "pooled_spec_3_18_shares": {"by_kind": {"a": 1}}}
    assert F.audit_problems(qc, rep, 50, 5, {"by_kind": {"a": 1}}) == []
    assert any("final_twins" in x for x in F.audit_problems(qc, rep, 50, 6, {"by_kind": {"a": 1}}))
    assert any("final_rows" in x for x in F.audit_problems(qc, rep, 51, 5, {"by_kind": {"a": 1}}))
    assert any("dry run" in x for x in F.audit_problems(qc, dict(rep, dry_run=True), 50, 5, {"by_kind": {"a": 1}}))
    assert any("pooled shares" in x for x in F.audit_problems(qc, rep, 50, 5, {"by_kind": {"a": 2}}))
    assert any("g_tw" in x for x in F.audit_problems(dict(qc, negtwin_gates={}), rep, 50, 5, {"by_kind": {"a": 1}}))
    assert any("sampled" in x for x in F.audit_problems(qc, dict(rep, sampled=8), 50, 5, {"by_kind": {"a": 1}}))


def test_jl_does_not_split_on_unicode_line_separators(tmp_path):
    f = tmp_path / "x.jsonl"
    f.write_text(json.dumps({"t": "a b\x0bc\u0085d"}, ensure_ascii=False) + "\n" + json.dumps({"t": 2}) + "\n", encoding="utf-8")
    assert [r["t"] for r in F.jl(f)] == ["a b\x0bc\u0085d", 2]


# ------------------------------------------------------------------ integration on a symlink copy of the live GB files

def link(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.symlink_to(src.resolve())


def make_tree(tmp: Path) -> F.Paths:
    L = LIVE
    for f in (L.cand, L.rel, L.man, L.mixdev, L.parts / "GB" / "out" / "c3_hold_a60.jsonl", L.parts / "GB" / "out" / "c3_hold_a60.relations.jsonl"):
        link(f, tmp / "parts" / "GB" / "out" / f.name)
    (tmp / "parts" / "GB" / "qc").mkdir(parents=True)
    (tmp / "parts" / "GB" / "qc" / "QC_REPORT.json").write_bytes(L.qc.read_bytes())          # a real copy: the writer may write it
    for b in ("MD", "RTW"):
        link(L.parts / b / "out" / F.c2io.CAND, tmp / "parts" / b / "out" / F.c2io.CAND)
    sd = LIVE.shards / "GB"
    for f in list(sd.glob("*.json*")) + list((sd / "labels_q35_4b_main500k").glob("*")):
        link(f, tmp / "shards" / "GB" / f.relative_to(sd))
    for d in ("route_a42d", "label"):
        for f in (L.gblock / d).glob("*"):
            if f.is_file():
                link(f, tmp / "gblock" / d / f.name)
    for f in (L.gblock / "checks").glob("*.json"):
        link(f, tmp / "gblock" / "checks" / f.name)
    for f in L.stage3.glob("*.json"):
        link(f, tmp / "stage3" / f.name)
    link(L.denylist_program, tmp / "c_src" / "denylist.py")
    return F.Paths(parts=tmp / "parts", shards=tmp / "shards", gblock=tmp / "gblock", stage3=tmp / "stage3", backup=tmp / "backup",
                   denylist_program=tmp / "c_src" / "denylist.py")


def own(path: Path) -> Path:
    """Replace a symlink by a private copy so a test may change it."""
    if path.is_symlink():
        data = path.read_bytes()
        path.unlink()
        path.write_bytes(data)
    return path


@pytest.fixture()
def tree(tmp_path):
    return make_tree(tmp_path)


def run(P, **kw):
    return F.verdict(P, now=NOW, **kw)


def test_live_files_pass_in_the_symlink_copy(tree):
    v, p = run(tree)
    assert p == [] and v["would_pass"] and v["rows"] == 5537 and v["twins"] == 101 and v["g_tw"]["pass"]
    assert v["crowd"]["labels_for_candidates"] == 5537 and v["mixdev"]["rows"] == 1650
    assert v["gates_pending_after"] == F.PENDING and len(F.PENDING) == 2


def test_dry_run_changes_nothing(tree):
    before = F.sha(tree.qc)
    run(tree)
    assert F.sha(tree.qc) == before and not tree.backup.exists()


def test_changed_candidate_file_is_refused_by_manifest_and_qc_shas(tree):
    own(tree.cand).write_bytes(tree.cand.read_bytes() + b"\n")                  # same rows, other bytes
    _, p = run(tree)
    assert any("manifest:" in x and "sha256 differs" in x for x in p) and any("qc:" in x and "differs from the file on disk" in x for x in p)


def test_flipped_gold_is_caught_by_the_label_gate(tree):
    rows = F.jl(tree.cand)
    r = next(x for x in rows if x["qtype"] == "noul" and not x["meta"].get("twin_of"))
    r["gold"] = 1 - r["gold"]
    own(tree.cand).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n", encoding="utf-8")
    _, p = run(tree)
    assert any("gold differs from the routed label" in x for x in p)


def test_twin_gold_flip_breaks_g_tw(tree):
    rows = F.jl(tree.cand)
    r = next(x for x in rows if x["meta"].get("twin_of"))
    r["gold"] = 1 - r["gold"]
    own(tree.cand).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n", encoding="utf-8")
    _, p = run(tree)
    assert any("G-TW" in x for x in p)


def test_missing_crowd_label_is_refused(tree):
    lf = own(tree.shards / "GB" / "labels_q35_4b_main500k" / "shard_000.jsonl")
    lines = lf.read_text(encoding="utf-8").split("\n")
    lf.write_text("\n".join(lines[1:]), encoding="utf-8")
    _, p = run(tree)
    assert any(x.startswith("crowd:") for x in p)


def test_stale_hold_file_sha_and_qc_problems_are_refused(tree):
    qc = F.jf(tree.qc)
    qc["a60"]["hold"]["rows_sha256"] = "0" * 64
    qc["problems"] = ["x"]
    tree.qc.write_text(json.dumps(qc), encoding="utf-8")
    _, p = run(tree)
    assert any("hold rows file differs" in x for x in p) and any("QC record lists problems" in x for x in p)


def test_pooled_audit_record_mismatch_is_refused(tree):
    qc = F.jf(tree.qc)
    qc["negtwin_audit"]["final_twins"] = 102
    tree.qc.write_text(json.dumps(qc), encoding="utf-8")
    _, p = run(tree)
    assert any("final_twins" in x for x in p)


def test_after_the_data_cutoff_admission_refuses(tree):
    late = datetime.datetime(2026, 10, 22, 0, 0, 0, tzinfo=UTC)
    _, p = F.verdict(tree, now=late, crowd=False)
    assert any(x.startswith("admission:") and "after the data cutoff" in x for x in p)


def test_write_backs_up_and_records_a_record_the_mixer_admits(tree):
    v, p = run(tree)
    old = tree.qc.read_bytes()
    bdir = F.write(tree, v, now=NOW)
    assert (bdir / "QC_REPORT.json").read_bytes() == old
    qc = F.jf(tree.qc)
    assert qc["pass"] is True and qc["passed_utc"] == "2026-10-17T10:00:00Z" and qc["fix_iterations"] == 0
    assert qc["gates_pending"] == F.PENDING and "G13" in qc["gates_pending"][0] and "OHS-AC" in qc["gates_pending"][0] and "crowd selection" in qc["gates_pending"][1]
    assert qc["finalize"]["tool"].endswith("finalize_gb.py") and qc["finalize"]["ruling"] == "A66"
    assert qc["files"][F.c2io.CAND] == {"sha256": F.sha(tree.cand), "rows": 5537}
    assert qc["gates_run"] == json.loads(old)["gates_run"]                      # the earlier gate records are untouched
    files = {tree.cand.name: tree.cand, tree.rel.name: tree.rel}
    assert F.mix_c2.admission("GB", qc, F.mix_c2.mx.qc_binding(qc, files)) == []
    assert not list(tree.qc.parent.glob("*.tmp"))
    # only the QC record changed in the tree: every other file is still a symlink to the live file
    assert all(f.is_symlink() for f in (tree.cand, tree.rel, tree.man, tree.mixdev))
    again, p2 = run(tree)                                                         # the finalized record still verifies
    assert p2 == []


def test_write_never_overwrites_an_existing_backup(tree):
    v, _ = run(tree)
    F.write(tree, v, now=NOW)
    v2, p2 = run(tree)                                                            # a fresh verdict on the finalized record
    assert p2 == []
    before = F.sha(tree.qc)
    with pytest.raises(FileExistsError):
        F.write(tree, v2, now=NOW)
    assert F.sha(tree.qc) == before


def test_pass_is_not_written_when_a_gate_fails(tree, monkeypatch):
    own(tree.cand).write_bytes(tree.cand.read_bytes() + b"\n")
    monkeypatch.setattr(F, "Paths", lambda *a, **k: tree)
    before = F.sha(tree.qc)
    assert F.main(["--write"]) == 2 and F.sha(tree.qc) == before and not tree.backup.exists()


def test_main_dry_run_exit_codes_and_double_write_refusal(tree, monkeypatch, capsys):
    monkeypatch.setattr(F, "Paths", lambda *a, **k: tree)
    assert F.main([]) == 0
    assert F.main(["--write"]) == 0
    capsys.readouterr()
    assert F.main(["--write"]) == 3                                                # already finalized: not rewritten
    assert F.jf(tree.qc)["pass"] is True


# ================================================================== A66 skeptic round: the gates the first writer skipped

def route_case(n_high=40, **kw):
    """A small routed-block world: 40 AGREE-HIGH (2 cards x 2 labels), 6 AGREE-LOW, 4 OPUS_KEPT, 3 DISAGREE, 2 A39_DROPPED, 2 MIXDEV."""
    classes = []

    def add(i, cl, card="c0", label="yes", p=0.95, status="haiku_accepted", mixdev=False, conf=0.9):
        am = label if cl in ("AGREE-HIGH", "AGREE-LOW", "OPUS_KEPT", "A39_DROPPED", "MIXDEV") else ("no" if label == "yes" else "yes")
        classes.append({"id": i, "class": cl, "card_id": card, "label": label, "domain": "d", "qtype": "noul", "conf": conf, "status": status,
                        "mixdev": mixdev, "haiku_audit": False, "c1_argmax": am, "c1_p_argmax": p, "c1_p_label": p if am == label else 1 - p,
                        "anchor_kept": False, "disagree_read": False})
    for k in range(n_high):
        add(f"h{k}", "AGREE-HIGH", card=f"c{k % 2}", label="yes" if (k // 2) % 2 else "no")
    for k in range(6):
        add(f"l{k}", "AGREE-LOW", p=0.7)
    for k in range(4):
        add(f"o{k}", "OPUS_KEPT", status="opus_kept", conf=0.85)
    for k in range(3):
        add(f"d{k}", "DISAGREE", p=0.8)
    for k in range(2):
        add(f"x{k}", "A39_DROPPED", status="a39_dropped", conf=0.5)
    for k in range(2):
        add(f"m{k}", "MIXDEV", mixdev=True)
    anchors = F.keep_anchors([c for c in classes if c["class"] == "AGREE-HIGH"])
    for c in classes:
        c["anchor_kept"] = c["id"] in anchors
    pop = [{k: c[k] for k in ("id", "label", "card_id", "domain", "qtype", "conf", "status", "mixdev", "haiku_audit")} for c in classes]
    routed = []
    for c in classes:
        src = {"AGREE-HIGH": "haiku_agree_high_anchor", "AGREE-LOW": "haiku_agree_low", "OPUS_KEPT": "opus_a39", "DISAGREE": "opus_disagree"}.get(c["class"])
        if src and (c["class"] != "AGREE-HIGH" or c["anchor_kept"]):
            routed.append({"id": c["id"], "label": c["label"], "conf": 0.85 if src.startswith("opus") else c["conf"], "source": src, "card_id": c["card_id"],
                           "qtype": "noul", "domain": "d"})
    cnt = {c: sum(1 for x in classes if x["class"] == c) for c in {x["class"] for x in classes}}
    funnel = {"a39_dropped_stay_dropped": cnt["A39_DROPPED"], "agree_high_total": cnt["AGREE-HIGH"], "agree_high_anchor_kept": len(anchors),
              "agree_low_kept": cnt["AGREE-LOW"], "disagree_total": cnt["DISAGREE"], "mixdev_held_out": cnt["MIXDEV"], "opus_a39_kept": cnt["OPUS_KEPT"],
              "disagree_kept_opus_label": 2, "disagree_dropped_at_opus": {"low_confidence": 1}, "disagree_unread_dropped": 0,
              "disagree_kept_label_differs_from_haiku": 0}
    qcr = {"c1_read_population": len(classes), "mixdev_held_out": cnt["MIXDEV"]}
    a = dict(classes=classes, pop=pop, routed=routed, stats_funnel=funnel, qc_routing=qcr)
    a.update(kw)
    return a


def test_keep_anchors_is_the_documented_stratified_draw():
    a = route_case(400)
    high = [c for c in a["classes"] if c["class"] == "AGREE-HIGH"]
    k = F.keep_anchors(high)
    assert abs(len(k) / len(high) - 0.35) < 0.01
    assert F.keep_anchors(high) == k and F.keep_anchors(high, seed=1) != k              # seeded, and the seed matters
    for card in ("c0", "c1"):
        for lab in ("yes", "no"):
            n = sum(1 for c in high if c["card_id"] == card and c["label"] == lab)
            kept = sum(1 for c in high if c["card_id"] == card and c["label"] == lab and c["id"] in k)
            assert int(0.35 * n) <= kept <= int(0.35 * n) + 1


def test_routing_passes_and_each_fault_bites():
    rep, p = F.routing_problems(**route_case(2000))
    assert p == [] and rep["population"] == 2017 and rep["anchors_of"] == 2000
    a = route_case(2000)
    stored = next(c for c in a["classes"] if c["class"] == "AGREE-HIGH" and c["anchor_kept"])
    stored["anchor_kept"] = False                                                           # an anchor silently removed
    assert any("anchors differ from the seeded draw" in x for x in F.routing_problems(**a)[1])
    a = route_case(2000)
    next(c for c in a["classes"] if c["class"] == "AGREE-LOW")["class"] = "AGREE-HIGH"       # a class other than the C1 read gives
    assert any("carry a class other than" in x for x in F.routing_problems(**a)[1])
    a = route_case(2000)
    c = next(c for c in a["classes"] if c["class"] == "AGREE-HIGH")
    c["c1_p_label"] = 0.89                                                                    # p under 0.9 is not AGREE-HIGH
    assert any("carry a class other than" in x for x in F.routing_problems(**a)[1])
    a = route_case(2000)
    a["stats_funnel"]["agree_low_kept"] += 1
    assert any("funnel.agree_low_kept" in x for x in F.routing_problems(**a)[1])
    a = route_case(2000)
    a["stats_funnel"]["disagree_unread_dropped"] = 5
    assert any("DISAGREE rows" in x for x in F.routing_problems(**a)[1])
    a = route_case(2000)
    a["qc_routing"]["c1_read_population"] = 5
    assert any("QC A42D_5_1_5_2_routing" in x for x in F.routing_problems(**a)[1])
    a = route_case(2000)
    a["pop"] = a["pop"][1:]
    assert any("ids != population ids" in x for x in F.routing_problems(**a)[1])


def test_routing_routed_row_faults():
    base = route_case(2000)

    def case(mut):
        a = route_case(2000)
        mut(a)
        return F.routing_problems(**a)[1]
    drop = next(c for c in base["classes"] if c["class"] == "A39_DROPPED")
    assert any("class its source does not allow" in x for x in case(lambda a: a["routed"].append({"id": drop["id"], "label": "yes", "conf": 0.9, "source": "haiku_agree_low"})))
    mix = next(c for c in base["classes"] if c["class"] == "MIXDEV")
    assert any("class its source does not allow" in x for x in case(lambda a: a["routed"].append({"id": mix["id"], "label": "yes", "conf": 0.9, "source": "opus_a39"})))
    nonanchor = next(c for c in base["classes"] if c["class"] == "AGREE-HIGH" and not c["anchor_kept"])
    assert any("not an anchor" in x for x in case(lambda a: a["routed"].append({"id": nonanchor["id"], "label": nonanchor["label"], "conf": 0.9, "source": "haiku_agree_high_anchor"})))
    assert any("relabelled" in x for x in case(lambda a: a["routed"][0].update(label="maybe")))
    dis = next(r for r in base["routed"] if r["source"] == "opus_disagree")
    assert any("under Opus confidence 0.85" in x for x in case(lambda a: next(r for r in a["routed"] if r["id"] == dis["id"]).update(conf=0.84)))
    assert any("not in classes.jsonl" in x for x in case(lambda a: a["routed"].append({"id": "ghost", "label": "yes", "conf": 0.9, "source": "haiku_agree_low"})))


def test_anchor_rate_bar_bites_when_the_stored_set_is_the_drawn_set_but_the_rate_is_off(monkeypatch):
    a = route_case(2000)
    monkeypatch.setattr(F, "keep_anchors", lambda high, *x, **k: {c["id"] for c in high if c["anchor_kept"]})
    for c in a["classes"]:
        if c["class"] == "AGREE-HIGH":
            c["anchor_kept"] = True                                                         # 100% kept
    assert any("not 35%" in x for x in F.routing_problems(**a)[1])


def test_audit_disclosure():
    pop = [{"id": f"a{i}", "domain": "d", "status": "haiku_accepted", "mixdev": i == 0, "haiku_audit": i < 6, **({"opus_audit_label": "yes"} if i < 4 else {})} for i in range(20)]
    rep, p = F.audit_disclosure(pop, {"audit_rows": 6, "opus_audit_items_read": 4})
    assert p == [] and rep["sampled"] == 6 and rep["read"] == 4 and rep["never_answered"] == 2 and rep["sampled_rows_later_in_mixdev"] == 1
    assert rep["per_domain_sampled_read"] == {"d": [6, 4]} and rep["read_share"] == 0.2
    assert any("audit_rows" in x for x in F.audit_disclosure(pop, {"audit_rows": 7, "opus_audit_items_read": 4})[1])
    assert any("opus_audit_items_read" in x for x in F.audit_disclosure(pop, {"audit_rows": 6, "opus_audit_items_read": 5})[1])
    pop[10]["opus_audit_label"] = "yes"                                                     # an audit label outside the sample
    assert any("not in the audit sample" in x for x in F.audit_disclosure(pop, {"audit_rows": 6, "opus_audit_items_read": 4})[1])
    pop[10].pop("opus_audit_label")
    pop[1]["status"] = "opus_kept"
    assert any("not a Haiku-accepted row" in x for x in F.audit_disclosure(pop, {"audit_rows": 6, "opus_audit_items_read": 4})[1])


def test_mixdev_text_and_group_disjointness():
    dev = [{"id": "m1", "group_id": "g1", "call_id": "c1", "state": "text one"}]
    rows = [{"id": "r1", "group_id": "g2", "call_id": "c2", "state": "text two"}]
    assert F.mixdev_overlap_problems(dev, rows)[1] == []
    assert any("group_id" in x for x in F.mixdev_overlap_problems(dev, [dict(rows[0], group_id="g1")])[1])
    assert any("call_id" in x for x in F.mixdev_overlap_problems(dev, [dict(rows[0], call_id="c1")])[1])
    assert any("text" in x for x in F.mixdev_overlap_problems(dev, [dict(rows[0], state="text one")])[1])
    assert any("cannot be shown" in x for x in F.mixdev_overlap_problems([dict(dev[0], state="")], rows)[1])


class Pat:
    def __init__(self, pid):
        self.pid = pid


def prog_rows(n=3):
    rows = [{"id": f"b{i}", "instructions": "Does the text say that this item is red?", "meta": {}} for i in range(n)]
    rows += [{"id": f"t{i}", "instructions": "Is it correct that the text says that this item is red?", "meta": {"twin_of": f"b{i}", "negtwin": {"pattern": f"P{i}"}}} for i in range(n)]
    return rows


def test_program_checks_gate(monkeypatch):
    trained = [Pat(f"P{i}") for i in range(3)]
    ok = lambda b, t, p, pairs: []                                                           # noqa: E731
    rep, p = F.program_problems(prog_rows(), trained, {}, check=ok, min_patterns=3)
    assert p == [] and rep == {"twins_checked": 3, "failures": 0, "unparsed": 0, "catalogue_patterns": 3}
    seen = []
    F.program_problems(prog_rows(), trained, {"x": 1}, check=lambda b, t, pt, pairs: seen.append((b, t, pt.pid, pairs)) or [], min_patterns=3)
    assert seen[0] == ("Does the text say that this item is red?", "Is it correct that the text says that this item is red?", "P0", {"x": 1})   # cores, not whole rows
    bad = lambda b, t, pt, pairs: ["K: two predicates changed"] if pt.pid == "P1" else []   # noqa: E731
    rep, p = F.program_problems(prog_rows(), trained, {}, check=bad, min_patterns=3)
    assert rep["failures"] == 1 and any("fail the program checks" in x and "1 of 3" in x for x in p)
    assert any("trained catalogue has 3 patterns < 300" in x for x in F.program_problems(prog_rows(), trained, {}, check=ok)[1])      # the >= 300 bar
    assert any("no base row or no pattern" in x for x in F.program_problems(prog_rows(), trained[:2], {}, check=ok, min_patterns=2)[1])
    rows = prog_rows()
    rows[3]["instructions"] = "no question mark here"
    assert any("do not split" in x for x in F.program_problems(rows, trained, {}, check=ok, min_patterns=3)[1])
    rows = prog_rows()
    rows[3]["meta"]["twin_of"] = "gone"
    assert any("no base row" in x for x in F.program_problems(rows, trained, {}, check=ok, min_patterns=3)[1])


def src_case():
    doms = [f"d{i}" for i in range(8)]
    rows = [{"id": f"r{i}", "domain": d, "meta": {"licence": "CC BY-SA 4.0 (Wikibooks) (text); card, question and label wording: CC0 1.0"}} for i, d in enumerate(doms)]
    vd = {d: {"hit": False, "verdict": "pass", "class": None, "entry": None, "taint_hits": 0, "parent_no_new_rows_pass": [], "matches": []} for d in doms}
    verdicts = {"canonical": True, "provisional": [], "denylist_sha256": "A", "query_sha256": "B", "program_sha256": "C",
                "counts": {"datasets": 8, "hit": 0, "deny_taint": 0, "no_new_rows": 0, "pass": 8, "pass_with_parent_no_new_rows": 0, "ohs3_hit": 0, "sealed_hit": 0},
                "verdicts": vd}
    return dict(rows=rows, verdicts=verdicts, c1o={d: [] for d in doms}, final_sources={d: {} for d in doms}, summary={"problems": [], "per_domain": {d: {} for d in doms}},
                shas={"denylist_built": "A", "denylist_query_final": "B", "denylist_program": "C"})


def test_source_gates_pass_and_each_fault_bites():
    rep, p = F.source_problems(**src_case())
    assert p == [] and rep["domains"] == 8 and rep["c1_overlap_hits"] == 0

    def case(mut):
        a = src_case()
        mut(a)
        return F.source_problems(**a)[1]
    assert any("domains < 8" in x for x in case(lambda a: a["rows"].pop()))
    assert any("domains < 8" in x for x in case(lambda a: [r.update(domain="d0") for r in a["rows"]]))
    assert any("counts.hit is 1" in x for x in case(lambda a: a["verdicts"]["counts"].update(hit=1)))
    assert any("counts.sealed_hit" in x for x in case(lambda a: a["verdicts"]["counts"].pop("sealed_hit")))
    assert any("not a clean pass" in x for x in case(lambda a: a["verdicts"]["verdicts"]["d1"].update(verdict="deny", hit=True)))
    assert any("not a clean pass" in x for x in case(lambda a: a["verdicts"]["verdicts"]["d1"].update(taint_hits=1)))
    assert any("without a deny-list verdict" in x for x in case(lambda a: a["verdicts"]["verdicts"].pop("d2") and None))
    assert any("not canonical" in x for x in case(lambda a: a["verdicts"].update(canonical=False)))
    assert any("not canonical" in x for x in case(lambda a: a["verdicts"].update(provisional=["x"])))
    assert any("C1-overlap lists are not empty" in x for x in case(lambda a: a["c1o"].update(d3=["a source name"])))
    assert any("without a C1-overlap entry" in x for x in case(lambda a: a["c1o"].pop("d3")))
    assert any("denylist_sha256 differs" in x for x in case(lambda a: a["shas"].update(denylist_built="Z")))
    assert any("query_sha256 differs" in x for x in case(lambda a: a["shas"].update(denylist_query_final="Z")))
    assert any("program_sha256 differs" in x for x in case(lambda a: a["shas"].update(denylist_program="Z")))
    assert any("file missing" in x for x in case(lambda a: a["shas"].update(denylist_program=None)))
    assert any("summary.json lists problems" in x for x in case(lambda a: a["summary"].update(problems=["x"])))
    assert any("without a final_sources entry" in x for x in case(lambda a: a["final_sources"].pop("d0")))


@pytest.mark.parametrize("lic,bad", [("CC BY 4.0 (AIC) (text); wording: CC0", False), ("Public Domain (Delaware) (text); x", False), ("Nova Scotia Open Government Licence (x) (text); y", False),
                                     ("CC BY-NC 4.0 (x) (text); y", True), ("all rights reserved (x) (text); y", True), ("", True), (None, True), ("Some site terms (x) (text); CC0", True)])
def test_source_row_licences_must_be_recorded_and_permissive(lic, bad):
    a = src_case()
    a["rows"][0]["meta"]["licence"] = lic
    assert any("row licences" in x for x in F.source_problems(**a)[1]) is bad


def test_card_band_report():
    rows = [{"qtype": "noul", "gold": int(i < 5), "meta": {"card_id": "A"}} for i in range(10)] + [{"qtype": "noul", "gold": 1, "meta": {"card_id": "B"}}] * 3
    rep = F.card_band_report(rows)
    assert rep["yes_share_per_card"] == {"A": 0.5} and rep["cards_not_checked"] == 1 and rep["min"] == rep["max"] == 0.5


def test_refresh_check_only_applies_to_a_finalized_record():
    assert F.refresh_problems({}, 101, {"n_pairs": 101}) == []
    fin = {"finalize": {"tool": "x"}, "negtwin_gates": {"twins": 224, "g_tw": {"n_pairs": 224, "pass": True}}, "negtwin_gates_superseded": {}}
    assert any("!= the live recompute" in x for x in F.refresh_problems(fin, 101, {"n_pairs": 101}))
    fin["negtwin_gates"] = {"twins": 101, "g_tw": {"n_pairs": 101, "pass": True}}
    assert F.refresh_problems(fin, 101, {"n_pairs": 101}) == []
    fin.pop("negtwin_gates_superseded")
    assert any("no negtwin_gates_superseded" in x for x in F.refresh_problems(fin, 101, {"n_pairs": 101}))


# ------------------------------------------------------------------ integration: fault injection on the symlink tree

def write_jsonl(path: Path, rows):
    own(path).write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n", encoding="utf-8")


def edit_json(path: Path, fn):
    own(path)
    d = F.jf(path)
    fn(d)
    path.write_text(json.dumps(d), encoding="utf-8")


def test_live_tree_reports_the_new_gates(tree):
    v, p = run(tree)
    assert p == []
    assert v["program_checks"] == {"twins_checked": 101, "failures": 0, "unparsed": 0, "catalogue_patterns": 379}
    assert v["routing"]["population"] == 18773 and v["routing"]["anchors_kept"] == 2376 and v["routing"]["anchors_of"] == 6802
    assert v["routing"]["routed_by_source"]["opus_disagree"] == 96 and sum(v["routing"]["routed_by_source"].values()) == 5436
    assert v["audit_sample"]["sampled"] == 565 and v["audit_sample"]["read"] == 493 and v["audit_sample"]["never_answered"] == 72
    assert v["source_gates"]["domains"] == 11 and v["source_gates"]["deny_list_clean_passes"] == 11 and v["source_gates"]["c1_overlap_hits"] == 0
    assert v["mixdev"]["shared_with_candidates"] == {"group_id": 0, "call_id": 0, "text": 0}
    assert v["caps_ok"] is True and v["card_band"]["cards_checked"] == 21 and 0.4 <= v["card_band"]["min"] and v["card_band"]["max"] <= 0.6
    assert set(v["inputs_sha256"]) >= {"classes.jsonl", "denylist_verdicts_final.json", "c1_overlap.json", "denylist.py", "TRAINED_CATALOGUE.json"}
    assert all(len(h) == 64 for h in v["inputs_sha256"].values())


def test_a_twin_that_fails_the_program_checks_is_refused(tree):
    rows = F.jl(tree.cand)
    by = {r["id"]: r for r in rows}
    t = next(r for r in rows if r["meta"].get("twin_of"))
    t["instructions"] = by[t["meta"]["twin_of"]]["instructions"]                           # no predicate changed: check_pair must refuse it
    write_jsonl(tree.cand, rows)
    _, p = run(tree)
    assert any(x.startswith("programs:") and "fail the program checks" in x for x in p)


def test_a_bad_edit_site_twin_is_refused(tree):
    rows = F.jl(tree.cand)
    by = {r["id"]: r for r in rows}
    t = next(r for r in rows if r["meta"].get("twin_of"))
    pre, core = F.NC.split_instruction(t["instructions"])
    words = core.split(" ")
    t["instructions"] = pre + " ".join(words[:2] + ["the"] + words[2:])               # a word inserted right after a function word
    write_jsonl(tree.cand, rows)
    _, p = run(tree)
    assert any(x.startswith("programs:") for x in p)


def test_routing_fault_in_the_class_file_is_refused(tree):
    cls = F.jl(tree.route / "classes.jsonl")
    c = next(x for x in cls if x["class"] == "AGREE-HIGH" and x["anchor_kept"])
    c["anchor_kept"] = False
    write_jsonl(tree.route / "classes.jsonl", cls)
    _, p = run(tree)
    assert any(x.startswith("routing:") and "anchors differ" in x for x in p)


def test_routed_row_in_a_dropped_class_is_refused(tree):
    cls = F.jl(tree.route / "classes.jsonl")
    rid = F.jl(tree.route / "routed_block.jsonl")[0]["id"]
    next(x for x in cls if x["id"] == rid)["class"] = "A39_DROPPED"
    write_jsonl(tree.route / "classes.jsonl", cls)
    _, p = run(tree)
    assert any(x.startswith("routing:") for x in p)


def test_deny_list_hit_and_c1_overlap_are_refused(tree):
    edit_json(tree.checks / "denylist_verdicts_final.json", lambda d: d["counts"].update(hit=1))
    _, p = run(tree, crowd=False)
    assert any(x.startswith("source:") and "counts.hit" in x for x in p)


def test_c1_overlap_entry_is_refused(tree):
    edit_json(tree.checks / "c1_overlap.json", lambda d: d.update(news=["Wikinews"]))
    _, p = run(tree, crowd=False)
    assert any(x.startswith("source:") and "C1-overlap lists are not empty" in x for x in p)


def test_changed_deny_list_inputs_break_the_sha_binding(tree):
    own(tree.checks / "denylist_query_final.json").write_bytes((tree.checks / "denylist_query_final.json").read_bytes() + b" ")
    own(tree.denylist_program).write_bytes(tree.denylist_program.read_bytes() + b"\n# changed\n")
    _, p = run(tree, crowd=False)
    assert any("query_sha256 differs" in x for x in p) and any("program_sha256 differs" in x for x in p)


def test_missing_cached_gate_file_is_a_problem_not_a_crash(tree):
    (tree.checks / "c1_overlap.json").unlink()
    (tree.route / "classes.jsonl").unlink()
    _, p = run(tree, crowd=False)
    assert any("input c1_overlap.json: cannot be read" in x for x in p) and any("input classes.jsonl: cannot be read" in x for x in p)
    assert any(x.startswith("source:") for x in p) and any(x.startswith("routing:") for x in p)


def test_mixdev_sharing_a_text_with_a_candidate_is_refused(tree):
    dev = F.jl(tree.mixdev)
    cand = F.jl(tree.cand)
    dev[0]["state"] = cand[0]["state"]
    write_jsonl(tree.mixdev, dev)
    _, p = run(tree, crowd=False)
    assert any(x.startswith("mixdev:") and "text values are also in the candidates" in x for x in p)


def test_a_missing_md_or_rtw_candidates_file_is_an_explicit_problem(tree):
    (tree.parts / "MD" / "out" / F.c2io.CAND).unlink()
    _, p = run(tree, crowd=False)
    assert any("a60: MD candidates file is missing" in x for x in p)
    (tree.parts / "RTW" / "out" / F.c2io.CAND).unlink()
    _, p = run(tree, crowd=False)
    assert any("a60: RTW candidates file is missing" in x for x in p)


def test_audit_sample_counts_in_counts_json_must_match(tree):
    edit_json(tree.route / "counts.json", lambda d: d.update(opus_audit_items_read=500))
    _, p = run(tree, crowd=False)
    assert any(x.startswith("audit-sample:") for x in p)


def test_the_written_record_refreshes_negtwin_gates_and_keeps_the_old_block(tree):
    v, p = run(tree)
    old = F.jf(tree.qc)
    F.write(tree, v, now=NOW)
    qc = F.jf(tree.qc)
    ng, sup = qc["negtwin_gates"], qc["negtwin_gates_superseded"]
    assert ng["twins"] == 101 and ng["g_tw"]["n_pairs"] == 101 and ng["g_tw"]["pass"] and ng["program_checks"]["failures"] == 0
    assert ng["twin_count_history"] == {"tw1_packaged": 224, "after_pooled_audit": 197, "after_a60_selection": 101}
    assert "yes_share_rebalance" not in ng and ng["yes_share_band_live"]["cards_checked"] == 21
    assert sup["twins"] == 224 and sup["g_tw"]["n_pairs"] == 224 and sup["yes_share_rebalance"] == old["negtwin_gates"]["yes_share_rebalance"]
    assert "superseded_by" in sup and "re-derived from the files" not in qc["note"]
    fin = qc["finalize"]
    assert fin["tool_sha256"] == F.sha(Path(F.__file__)) and fin["inputs_sha256"] == v["inputs_sha256"]
    assert fin["verdict"]["audit_sample"]["never_answered"] == 72 and fin["verdict"]["program_checks"]["failures"] == 0
    assert qc["gates_pending"] == F.PENDING and not any("twin gates" in x or "Sonnet 3%" in x for x in qc["gates_pending"])
    v2, p2 = run(tree)                                                                      # the refreshed record verifies; the superseded block is not re-superseded
    assert p2 == []
    again = F.would_be(F.jf(tree.qc), v2, NOW)
    assert again["negtwin_gates_superseded"] == sup


def test_a_finalized_record_with_a_stale_negtwin_block_is_refused(tree):
    v, _ = run(tree)
    F.write(tree, v, now=NOW)
    edit_json(tree.qc, lambda d: d["negtwin_gates"].update(twins=224))
    _, p = run(tree, crowd=False)
    assert any("finalized QC negtwin_gates" in x for x in p)


def test_write_refuses_a_verdict_gone_stale(tree):
    v, _ = run(tree)
    own(tree.checks / "c1_overlap.json").write_text(json.dumps({"news": []}), encoding="utf-8")        # a gate file changed after the verdict
    before = F.sha(tree.qc)
    with pytest.raises(RuntimeError, match="changed since the verdict"):
        F.write(tree, v, now=NOW)
    assert F.sha(tree.qc) == before and not tree.backup.exists()


def test_write_refuses_when_the_record_or_candidates_changed_after_the_verdict(tree):
    v, _ = run(tree)
    own(tree.cand).write_bytes(tree.cand.read_bytes() + b"\n")
    with pytest.raises(RuntimeError, match="candidates_sha256"):
        F.write(tree, v, now=NOW)
    t2 = make_tree(tree.backup.parent / "second")
    v, _ = run(t2)
    t2.qc.write_text(t2.qc.read_text(encoding="utf-8") + " ", encoding="utf-8")
    with pytest.raises(RuntimeError, match="qc_sha256_before"):
        F.write(t2, v, now=NOW)
    assert not t2.backup.exists()


# ------------------------------------------------------------------ source hygiene

def test_jsonl_is_never_split_with_splitlines():
    src = Path(F.__file__).read_text(encoding="utf-8")
    code = "\n".join(l for l in src.split("\n") if not l.lstrip().startswith("#"))
    assert ".splitlines(" not in code.replace('"str.splitlines() also', "")        # only the explanatory comment mentions it


FORBIDDEN = ("ohs", "sealed", "preread", "external_quarantine", "longbench_v2", "/.claude", "c_spec/sealed_brief")
_WATCH = {"on": False, "blocked": []}


def _audit_hook(event, args):
    if _WATCH["on"] and event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        try:
            raw = os.fsdecode(args[0])
        except Exception:
            return
        for cand in {raw.lower(), os.path.realpath(raw).lower()}:
            if any(f in cand for f in FORBIDDEN):
                _WATCH["blocked"].append(raw)


sys.addaudithook(_audit_hook)


def test_the_dry_run_opens_no_forbidden_path(tree):
    _WATCH["on"], _WATCH["blocked"] = True, []
    try:
        v, p = run(tree)
    finally:
        _WATCH["on"] = False
    assert p == [] and _WATCH["blocked"] == []


def test_the_forbidden_path_watch_itself_bites(tmp_path):
    f = tmp_path / "x_sealed_y.txt"
    f.write_text("a", encoding="utf-8")
    _WATCH["on"], _WATCH["blocked"] = True, []
    try:
        f.read_text(encoding="utf-8")
    finally:
        _WATCH["on"] = False
    assert _WATCH["blocked"] and "sealed" in _WATCH["blocked"][0]
