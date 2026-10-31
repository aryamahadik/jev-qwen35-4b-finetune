"""CPU tests for the item 4 pilot harness on FABRICATED predictions (no GPU, no network, no sealed path).
Run from lean/c2_build:  nice -n 10 ../../.venv/bin/python -B -m pytest -q -p no:cacheprovider pilot_ab/tests
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
PAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAB))
import common as C  # noqa: E402
import verdict as V  # noqa: E402

FAM = "T40"
C1N, PN = C.C1_NAME + C.READ_TAG, C.pilot_name(FAM) + C.READ_TAG


# ----------------------------------------------------------------------------------------------------------- fabricated world
def mk_rows(prefix, n, doc_every=1, source="srcA"):
    rows = []
    for i in range(n):
        if i % 2 == 0:
            rows.append({"id": f"{prefix}{i}", "group_id": f"g:{prefix}{i}", "source": source, "qtype": "noul", "gold": i % 4 // 2,
                         "options": None, "meta": {"source_doc": f"{prefix}doc{i // doc_every}"}})
        else:
            rows.append({"id": f"{prefix}{i}", "group_id": f"g:{prefix}{i}", "source": source, "qtype": "choice", "gold": "b",
                         "options": ["a", "b", "c"], "meta": {"source_doc": f"{prefix}doc{i // doc_every}"}})
    return rows


def probs(r, ok):
    if r["qtype"] == "noul":
        hi = (r["gold"] == 1) == ok
        return {"yes": 0.9 if hi else 0.1, "no": 0.1 if hi else 0.9}
    return {"a": 0.1, "b": 0.8, "c": 0.1} if ok else {"a": 0.8, "b": 0.1, "c": 0.1}


def write_split(reads, split, rows, c1_ok, pilot_ok, meta_over=None):
    for name, oks in ((C1N, c1_ok), (PN, pilot_ok)):
        d = Path(reads) / f"preds_{split}"
        d.mkdir(parents=True, exist_ok=True)
        with open(d / f"{name}.jsonl", "w") as f:
            for r, ok in zip(rows, oks):
                f.write(json.dumps({"id": r["id"], "model": name, "probs": probs(r, ok)}) + "\n")
        meta = {"name": name, "base": C.BASE, "host": "gcp", "gpu": "NVIDIA L4", "torch": "2.14.0", "cuda": "13.0",
                "tta": False, "tta_choice": True, "tta_noul": False, "perm_seed": None, "layout": C.LAYOUT,
                "load": {"revision": C.BASE_REV, "chat_template_sha": "abc", "forced": False, "layout": C.LAYOUT, "style": "cygnet"}}
        meta.update(meta_over or {})
        (d / f"{name}.meta.json").write_text(json.dumps(meta))


def outcomes(n, gain, loss, c1_right_every=2):
    """C1 right on every 2nd row; the pilot gains `gain` wrong->right rows and loses `loss` right->wrong rows."""
    c1 = [i % c1_right_every == 0 for i in range(n)]
    p = list(c1)
    g_, l_ = gain, loss
    for i in range(n):
        if not c1[i] and g_:
            p[i] = True; g_ -= 1
        elif c1[i] and l_:
            p[i] = False; l_ -= 1
    assert g_ == 0 and l_ == 0
    return c1, p


class World:
    """own dev, G-proxy (with complement pairs) and two small 'gate dev' splits, all fabricated."""
    def __init__(self, tmp, own=(6, 0), existing=(0, 0), gproxy=(0, 0), n_own=300, n_ex=(150, 150), n_gp=600, n_pairs=20,
                 docs_per_cluster=1, meta_over=None, adapter_ok=True):
        self.tmp, self.reads, self.dev = Path(tmp), Path(tmp) / "reads", Path(tmp) / "dev"
        self.dev.mkdir(parents=True, exist_ok=True)
        self.own_rows = mk_rows("o", n_own)
        c1, p = outcomes(n_own, *own)
        write_split(self.reads, C.own_split(FAM), self.own_rows, c1, p, meta_over)
        self.gp_rows = mk_rows("p", n_gp, doc_every=docs_per_cluster)
        self.gp_rels = [{"a": f"p{2 * k}", "b": f"p{2 * k + 1}", "type": "complement"} for k in range(n_pairs)]
        c1, p = outcomes(n_gp, *gproxy)
        write_split(self.reads, C.GPROXY_SPLIT, self.gp_rows, c1, p, meta_over)
        self.splits = ("sA", "sB")
        total_gain, total_loss = existing
        self.ex_rows_n = 0
        for k, (sp, n) in enumerate(zip(self.splits, n_ex)):
            rows = mk_rows(f"{sp}_", n)
            rows[-1]["source"] = "tb_mixtral" if sp == "sB" else rows[-1]["source"]   # one barred row in sB
            (self.dev / f"{sp}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
            gn, ls = (total_gain, total_loss) if k == 0 else (0, 0)
            c1, p = outcomes(n, gn, ls)
            write_split(self.reads, sp, rows, c1, p, meta_over)
            self.ex_rows_n += n - (1 if sp == "sB" else 0)
        (self.reads / "adapters.sha256").write_text(
            f"{C.C1_ADAPTER_SHA if adapter_ok else '0' * 64}  models/{C.C1_NAME}/adapter_model.safetensors\n"
            f"{'1' * 64}  models/{C.pilot_name(FAM)}/adapter_model.safetensors\n")

    def spec(self, **kw):
        base = dict(own_n=len(self.own_rows), existing_n=self.ex_rows_n, min_gproxy_rows=len(self.gp_rows),
                    min_gproxy_pairs=len(self.gp_rels), splits9=self.splits)
        base.update(kw)
        return V.Spec(**base)

    def run(self, **kw):
        return V.compute(FAM, self.reads, self.own_rows, self.gp_rows, self.gp_rels, self.dev, spec=self.spec(**kw))


# --------------------------------------------------------------------------------------------------------------- the three rules
def test_keep_when_all_three_hold(tmp_path):
    r = World(tmp_path, own=(9, 0), existing=(0, 1), gproxy=(5, 0)).run()
    assert r["verdict"] == "KEEP" and r["failed"] == []
    assert r["criteria"]["i_own_dev"]["value_pt"] == pytest.approx(3.0)


@pytest.mark.parametrize("gain,passes", [(5, False), (6, True), (7, True)])
def test_own_gain_bar_is_plus_2_point_inclusive(tmp_path, gain, passes):
    r = World(tmp_path, own=(gain, 0)).run()      # 300 rows: 6 rows = exactly +2.0 pt
    assert r["criteria"]["i_own_dev"]["pass"] is passes
    assert (r["verdict"] == "KEEP") is passes and (r["failed"] == [] if passes else r["failed"] == ["i_own_dev"])


@pytest.mark.parametrize("loss,passes", [(0, True), (1, True), (2, False)])
def test_existing_drop_bar_is_half_a_point_inclusive(tmp_path, loss, passes):
    # 299 pooled rows (the barred tb_mixtral row is excluded): losing 1 row = -0.334 pt, 2 rows = -0.669 pt
    r = World(tmp_path, existing=(0, loss)).run()
    assert r["existing_dev"]["n"] == 299
    assert r["criteria"]["ii_existing_dev"]["pass"] is passes


def test_existing_drop_exactly_half_a_point(tmp_path):
    # 200 pooled rows (sA 101 + sB 100 after the barred row): 1 row lost = -0.5 pt exactly passes; 2 rows = -1.0 fails
    w = World(tmp_path, n_ex=(101, 100), existing=(0, 1))
    assert w.ex_rows_n == 200
    r = w.run()
    assert r["existing_dev"]["diff_pt"] == pytest.approx(-0.5) and r["criteria"]["ii_existing_dev"]["pass"]
    assert World(tmp_path / "x", n_ex=(101, 100), existing=(0, 2)).run()["criteria"]["ii_existing_dev"]["pass"] is False


def test_excluded_source_is_not_pooled(tmp_path):
    w = World(tmp_path)
    assert w.run()["existing_dev"]["n"] == w.ex_rows_n == 299


def test_gproxy_rejected_only_by_ci_upper_bound(tmp_path):
    # large clear loss: point -4 pt on 600 rows, CI far below -0.5 -> rejected -> MOVE_TO_C3
    r = World(tmp_path / "a", own=(9, 0), gproxy=(0, 24)).run()
    g3 = r["criteria"]["iii_gproxy"]
    assert g3["value_pt"] == pytest.approx(-4.0) and g3["ci"][1] < -0.5 and not g3["pass"]
    assert r["verdict"] == "MOVE_TO_C3" and r["failed"] == ["iii_gproxy"]
    # same point on a tiny set: CI wide, upper bound > -0.5 -> NOT rejected (there is no point threshold)
    w = World(tmp_path / "b", own=(9, 0), n_gp=50, n_pairs=5, gproxy=(0, 2))
    g3 = w.run()["criteria"]["iii_gproxy"]
    assert g3["value_pt"] == pytest.approx(-4.0) and g3["ci"][1] > -0.5 and g3["pass"]


def test_gproxy_gain_is_not_rejected_and_small_loss_is_not_rejected(tmp_path):
    assert World(tmp_path / "a", gproxy=(10, 0)).run()["criteria"]["iii_gproxy"]["pass"]
    r = World(tmp_path / "b", gproxy=(0, 3)).run()           # -0.5 pt point on 600 rows
    assert r["criteria"]["iii_gproxy"]["value_pt"] == pytest.approx(-0.5) and r["criteria"]["iii_gproxy"]["pass"]


def test_gproxy_is_paired_pilot_minus_c1(tmp_path):
    r = World(tmp_path, gproxy=(12, 0)).run()
    g_ = r["gproxy"]
    assert g_["diff_pt"] == pytest.approx(2.0) and g_["pilot"] - g_["c1"] == pytest.approx(2.0)
    assert g_["resamples"] == 10000 and g_["seed"] == 0 and g_["ci95"][0] < 2.0 < g_["ci95"][1]


def test_bootstrap_is_reproducible(tmp_path):
    w = World(tmp_path, gproxy=(0, 9))
    assert w.run()["gproxy"]["ci95"] == w.run()["gproxy"]["ci95"]


# ------------------------------------------------------------------------------------------------------------------ clustering
def test_complement_pair_is_one_cluster_and_documents_merge():
    rows = mk_rows("p", 40)                                  # 40 distinct documents
    pairs = [{"a": "p0", "b": "p1", "type": "complement"}, {"a": "p2", "b": "p3", "type": "complement"}]
    lab, info = V.clusters(rows, pairs)
    assert info["clusters"] == 38 and lab["p0"] == lab["p1"] and lab["p2"] == lab["p3"] and lab["p0"] != lab["p2"]
    rows2 = mk_rows("p", 40, doc_every=4)                    # 10 documents of 4 rows
    lab2, info2 = V.clusters(rows2, [{"a": "p3", "b": "p4", "type": "complement"}])   # links doc0 and doc1
    assert info2["clusters"] == 9 and lab2["p0"] == lab2["p7"]


def test_cluster_by_document_widens_the_ci(tmp_path):
    a = World(tmp_path / "a", gproxy=(0, 12), docs_per_cluster=1).run()["gproxy"]
    b = World(tmp_path / "b", gproxy=(0, 12), docs_per_cluster=20).run()["gproxy"]
    assert b["clusters"] < a["clusters"] and (b["ci95"][1] - b["ci95"][0]) > (a["ci95"][1] - a["ci95"][0])


def test_fallback_to_group_id_is_reported(tmp_path):
    w = World(tmp_path)
    for r in w.gp_rows:
        r["meta"] = {}
    r = w.run()
    assert r["gproxy"]["rows_with_group_id_fallback"] == len(w.gp_rows) and r["warnings"]


# --------------------------------------------------------------------------------------------------------------------- refusals
def test_refuses_missing_prediction(tmp_path):
    w = World(tmp_path)
    f = w.reads / "preds_sA" / f"{PN}.jsonl"
    f.write_text("".join(f.read_text().splitlines(True)[:-1]))
    with pytest.raises(V.Refused, match="without a prediction"):
        w.run()


@pytest.mark.parametrize("over,msg", [({"tta_choice": False}, "tta-choice"), ({"tta": True}, "tta-choice"),
                                      ({"perm_seed": 1}, "perm_seed"), ({"layout": "text_first"}, "layout")])
def test_refuses_wrong_readout(tmp_path, over, msg):
    with pytest.raises(V.Refused, match=msg):
        World(tmp_path, meta_over=over).run()


def test_refuses_reads_from_different_machines(tmp_path):
    w = World(tmp_path)
    m = w.reads / "preds_sA" / f"{PN}.meta.json"
    d = json.loads(m.read_text()); d["gpu"] = "NVIDIA A100"; m.write_text(json.dumps(d))
    with pytest.raises(V.Refused, match="gpu"):
        w.run()


def test_refuses_wrong_c1_adapter_and_size_and_pairs(tmp_path):
    with pytest.raises(V.Refused, match="507d1c29"):
        World(tmp_path / "a", adapter_ok=False).run()
    w = World(tmp_path / "b")
    with pytest.raises(V.Refused, match="own dev has"):
        w.run(own_n=299)
    with pytest.raises(V.Refused, match="G-proxy has"):
        w.run(min_gproxy_rows=2000)
    with pytest.raises(V.Refused, match="complement pairs"):
        w.run(min_gproxy_pairs=150)
    with pytest.raises(V.Refused, match="existing dev has"):
        w.run(existing_n=7056)


def test_refuses_pair_endpoint_outside_gproxy(tmp_path):
    w = World(tmp_path)
    w.gp_rels.append({"a": "p0", "b": "zzz", "type": "complement"})
    with pytest.raises(V.Refused, match="endpoint"):
        w.run()


def test_never_open_paths_are_refused():
    for p in ("lean/ohs4_sealed/x.jsonl", "/a/OHS_AC/y", "bench/external_quarantine/z", "/private/tmp/claude-501/x"):
        with pytest.raises(SystemExit):
            C.refuse_path(p)
    C.refuse_path("/Users/x/jev/opendecide-data/lean/data/dev.jsonl")


# --------------------------------------------------------------------------------------- CLI end to end on the REAL dev splits
def test_cli_end_to_end_real_dev_splits_and_no_repilot(tmp_path):
    """Full default Spec: 300 own rows, 2,100 G-proxy rows with 150 complement pairs, the real 9 gate dev splits
    (8,143 rows; 7,056 pooled) with fabricated predictions. Writes the verdict, then refuses a second one."""
    reads = tmp_path / "reads"
    own = mk_rows("o", 300)
    c1, p = outcomes(300, 9, 0)
    write_split(reads, C.own_split(FAM), own, c1, p)
    gp = mk_rows("p", 2100, doc_every=2)
    rels = [{"a": f"p{2 * k}", "b": f"p{2 * k + 1}", "type": "complement"} for k in range(150)]
    c1, p = outcomes(2100, 20, 0)
    write_split(reads, C.GPROXY_SPLIT, gp, c1, p)
    for sp in C.SPLITS9:
        rows = C.read_jsonl(C.LEAN / "data" / f"{sp}.jsonl")
        c1 = [(i % 3 != 0) for i in range(len(rows))]
        write_split(reads, sp, rows, c1, list(c1))
    (reads / "adapters.sha256").write_text(f"{C.C1_ADAPTER_SHA}  models/{C.C1_NAME}/adapter_model.safetensors\n"
                                           f"{'2' * 64}  models/{C.pilot_name(FAM)}/adapter_model.safetensors\n")
    for name, rows in (("own.jsonl", own), ("gp.jsonl", gp)):
        (tmp_path / name).write_text("".join(json.dumps(r) + "\n" for r in rows))
    (tmp_path / "rel.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    gsha = C.sha256_file(tmp_path / "gp.jsonl")
    args = ["--family", FAM, "--reads-dir", str(reads), "--own-rows", str(tmp_path / "own.jsonl"),
            "--gproxy-rows", str(tmp_path / "gp.jsonl"), "--gproxy-rel", str(tmp_path / "rel.jsonl"),
            "--out-dir", str(tmp_path / "out"), "--gproxy-sha256", gsha]
    assert V.main(args) == 0
    v = json.loads((tmp_path / "out" / "PILOT_AB_VERDICT.json").read_text())
    assert v["existing_dev"]["n"] == 7056 and v["own_dev"]["n"] == 300 and v["verdict"] == "KEEP"
    assert v["gproxy"]["complement_pairs"] == 150 and v["inputs"]["gproxy_sha256_pinned"] == gsha
    assert V.main(args) == 2                                                   # no re-pilot
    assert V.main(args[:-2] + ["--gproxy-sha256", "0" * 64, "--no-write"]) == 2   # file changed since it was pinned


# ----------------------------------------------------------------------------------------------------- staging and configs
def test_stage_and_config_on_real_format_rows(tmp_path):
    import make_config as M
    import train_decoder as td
    rows = C.read_jsonl(C.LEAN / "data/c_parts/c_train_r1.jsonl")[:1500]
    ids = {r["id"] for r in rows}
    rels = [x for x in C.read_jsonl(C.LEAN / "data/c_parts/c_rel_r1.jsonl") if x["a"] in ids and x["b"] in ids]
    (tmp_path / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (tmp_path / "rels.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    info = M.stage(FAM, tmp_path / "rows.jsonl", tmp_path / "rels.jsonl", out_root=tmp_path / "o", quiet=True)
    cfg = json.loads((tmp_path / "o" / "configs" / f"{FAM}.json").read_text())
    assert cfg["seed"] == 20261013 and cfg["lr"] == 5e-05 and cfg["init_adapter"] == C.C1_INIT_VOL and cfg["name"] == "q35_4b_pab_T40"
    assert not set(cfg) - td.KNOWN_KEYS - {"name"} and cfg["snap_every"] == 0 and cfg["snap_fracs"] == []
    assert cfg["expect_ord_rows"] == info["ordinal_rows"] and cfg["expect_kd_targets"] == info["kd_targets"]
    assert info["steps"] == 94 or 90 <= info["steps"] <= 94
    assert 0.1 < info["est_h100"]["usd"] < 1.0
    assert sorted(p.name for p in (tmp_path / "o" / "stage" / FAM).iterdir()) == sorted([C.TRAIN_FILE, C.REL_FILE])
    # the L4 command rebuilds the same config through od_gcp's own parser (micro_tokens aside)
    import od_gcp
    a = od_gcp.parser().parse_args(M.l4_train_argv(cfg))
    got = od_gcp.build_cfg(a)
    for k, v in cfg.items():
        if k in ("name", "init_adapter", "micro_tokens", "targets", "no_overwrite") and k != "no_overwrite":
            continue
        assert got.get(k) == v, k
    assert got["micro_tokens"] == M.L4_MICRO_TOKENS and got["targets"] == od_gcp.QWEN35_TARGETS


@pytest.mark.parametrize("bad", ["short", "dup", "dev_overlap", "rel_outside"])
def test_stage_refusals(tmp_path, bad):
    import make_config as M
    rows = C.read_jsonl(C.LEAN / "data/c_parts/c_train_r1.jsonl")[:1500]
    rels, dev = [], []
    if bad == "short":
        rows = rows[:1499]
    elif bad == "dup":
        rows[1]["id"] = rows[0]["id"]
    elif bad == "dev_overlap":
        dev = [rows[3]]
    elif bad == "rel_outside":
        rels = [{"a": rows[0]["id"], "b": "not_a_row", "type": "complement"}]
    (tmp_path / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (tmp_path / "dev.jsonl").write_text("".join(json.dumps(r) + "\n" for r in dev))
    (tmp_path / "rels.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    with pytest.raises(SystemExit):
        M.stage(FAM, tmp_path / "rows.jsonl", tmp_path / "rels.jsonl", [tmp_path / "dev.jsonl"], out_root=tmp_path / "o", quiet=True)
