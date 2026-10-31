"""Tests for the review fixes: relation files from the MANIFEST (F8), selection checks in --final, refills after
drops, QC records tied to the files, declared parents only, S7 / held-out dev checks, strict styles, commit 4.2
sub-targets and counts, G10 yes-rate cells. Synthetic fixtures only; no real data is read."""
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import crowd_select as cs  # noqa: E402
import mixer as mx  # noqa: E402
import mixio  # noqa: E402


def wjl(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


def yn(i, cid, gold, w="wd.1", block="F1", **meta):
    return {"id": i, "call_id": cid, "group_id": "g" + i, "state": "s " + i, "qtype": "noul", "gold": gold,
            "role": "base", "source": "c_own_" + block, "instructions": "Is it allowed?", "_block": block,
            "meta": {"wording_id": w, "licence": "CC0", "format_style": "FS-0001", **meta}}


@pytest.fixture
def famdir(tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "fam_dir", lambda fam: tmp_path / fam)
    monkeypatch.setattr(cs, "OUT", tmp_path / "crowd")
    return tmp_path


def f8_family(root, n_rel_declared=2, sha=None):
    out = root / "F8" / "out"
    rows = [yn(f"r{i}", f"c{i // 2}", i % 2) for i in range(8)]
    wjl(out / "candidates_r1.jsonl", rows)
    rp = wjl(out / "relations_candidates_r1.jsonl", [{"a": "r0", "b": "r1", "type": "complement"},
                                                    {"a": "r2", "b": "r3", "type": "equiv"}])
    man = {"files": {"candidates_r1": {"rows": 8, "relations": n_rel_declared,
                                       "relations_sha256": sha or mixio.sha256_file(rp)}}}
    (out / "MANIFEST.json").write_text(json.dumps(man))
    return rows


def test_f8_relations_found_from_manifest(famdir):
    f8_family(famdir)
    assert cs.fam_files("F8")["rel"].name == "relations_candidates_r1.jsonl"
    rows, rels = cs.load_family(mixio.InputLog(), "F8")
    assert len(rels) == 2 and len(cs.units_of(rows, rels)) == 4


def test_relation_count_or_sha_mismatch_refused(famdir):
    f8_family(famdir, n_rel_declared=289)
    with pytest.raises(SystemExit, match="289"):
        cs.load_family(mixio.InputLog(), "F8")
    f8_family(famdir, sha="0" * 64)
    with pytest.raises(SystemExit, match="sha256"):
        cs.load_family(mixio.InputLog(), "F8")
    (famdir / "F8/out/relations_candidates_r1.jsonl").unlink()
    with pytest.raises(SystemExit, match="no relation file"):
        cs.load_family(mixio.InputLog(), "F8")


def test_rel_decl_layouts_and_check_records_skipped():
    m = {"files": [{"path": "out/candidates_r1.relations.jsonl", "rows": 5, "sha256": "a" * 64}],
         "sealed_check": {"candidates_r1.relations.jsonl": {"rows": 3}},
         "outputs": {"candidates_r1": {"relations": {"file": "out/candidates_r1.relations.jsonl", "n": 5}}}}
    d = cs.rel_decl(m)
    assert d == {"names": {"candidates_r1.relations.jsonl"}, "n": {5}, "sha256": {"a" * 64}}


def test_final_selection_checks_and_target(famdir):
    rows = f8_family(famdir)
    sha = mixio.sha256_file(famdir / "F8/out/candidates_r1.jsonl")
    sel = {"family": "F8", "target": 4, "candidates_sha256": sha, "selected_ids": ["r0", "r1", "r2", "r3"],
           "crowd_pg": {r["id"]: 0.5 for r in rows}, "difficulty_bin": {r["id"]: "medium" for r in rows},
           "report": {"pass": False, "checks": {"total_eq_target": True, "chi2_p_gt_0.01": False}}}
    (famdir / "crowd").mkdir()
    (famdir / "crowd/select_F8.json").write_text(json.dumps(sel))
    probs, rep = [], {}
    out, rels, par, pool = mx.family_block(mixio.InputLog(), "F8", 6, True, rep, probs)
    assert len(out) == 4 and len(rels) == 2
    assert any("chi2_p_gt_0.01" in p for p in probs)
    assert any("target 4 != mixer target 6" in p for p in probs)
    assert any("declares no parents" in p for p in probs)          # G1: no 'parents' in the MANIFEST
    assert {u for u in pool.cands[""]} and all(rows[0]["id"] not in pool.raw_of(u)[0]["id"] for u in pool.cands[""])


def test_relation_refusal_dry_run_leaves_family_out(famdir):
    f8_family(famdir, n_rel_declared=9)
    probs, rep = [], {}
    out, rels, par, pool = mx.family_block(mixio.InputLog(), "F8", 4, False, rep, probs)
    assert out == [] and pool is None and "refused" in probs[0]
    with pytest.raises(SystemExit):
        mx.family_block(mixio.InputLog(), "F8", 4, True, {}, [])


def own_pool_fixture(n=40):
    rows = [yn(f"x{i}", f"u{i}", i % 2, w="wd.A" if i < 20 else "wd.B") for i in range(n)]
    units = [[i] for i in range(n)]
    bins = {r["id"]: "na" for r in rows}
    pool = mx.own_pool("F1", rows, [], units, {"x0", "x1", "x20", "x21"}, bins, {})
    return rows, pool


def test_refill_same_stratum_and_class():
    rows, pool = own_pool_fixture()
    cur = [rows[i] | {"_block": "F1"} for i in (0, 1, 20, 21)]
    ever = {r["id"]: ("F1", r) for r in cur}
    kept = [r for r in cur if r["id"] != "x20"]                # x20: wd.B, gold 0 dropped
    seen = []

    def accept(p, u, tally):
        seen.append(u)
        return p.rows_of(u, tally)
    rep = {}
    add, rels = mx.refill({"F1": pool}, kept, ever, set(), accept, rep)
    assert len(add) == 1 and add[0]["meta"]["wording_id"] == "wd.B" and add[0]["gold"] == 0
    assert rep["F1"]["tiers"]["tier1"] == 1 and rep["F1"]["unfilled_rows"] == 0
    add2, _ = mx.refill({"F1": pool}, kept + add, ever, {"x20"}, accept, {})
    assert add2 == []                                         # nothing new lost: no refill


def test_refill_skips_refused_units_and_counts_unfilled():
    rows, pool = own_pool_fixture(24)                         # wd.B gold 0 rows: x20, x22 (x20 selected)
    cur = [rows[i] | {"_block": "F1"} for i in (0, 1, 20, 21)]
    ever = {r["id"]: ("F1", r) for r in cur}
    kept = [r for r in cur if r["id"] != "x20"]
    rep = {}
    add, _ = mx.refill({"F1": pool}, kept, ever, set(), lambda p, u, t: None, rep)
    assert add == [] and rep["F1"]["unfilled_rows"] == 1 and len(pool.tried) >= 1


def test_replay_style_pool_refills_same_source_by_size():
    lt = [{"id": f"p{i}", "source": "s1" if i < 6 else "s2", "qtype": "noul", "role": "base", "gold": i % 2,
           "meta": {}} for i in range(10)]
    units = {0: {"rows": [0, 1]}, 1: {"rows": [2]}, 2: {"rows": [3, 4]}, 3: {"rows": [6]}}
    pool = mx.Pool("replay", {lt[i]["id"]: u for u, x in units.items() for i in x["rows"]}, lambda r: r["source"],
                   {"s1": [1, 2], "s2": [3]}, lambda u: [lt[i] for i in units[u]["rows"]],
                   lambda u, t: [lt[i] | {"_block": "replay"} for i in units[u]["rows"]],
                   lambda r: ((r["qtype"], r["role"], r["gold"]), (r["qtype"], r["role"]), "*"), lambda ids: [])
    lost = [lt[0] | {"_block": "replay"}, lt[1] | {"_block": "replay"}]
    rep = {}
    add, _ = mx.refill({"replay": pool}, [], {r["id"]: ("replay", r) for r in lost}, set(),
                       lambda p, u, t: p.rows_of(u, t), rep)
    assert [r["id"] for r in add] == ["p3", "p4"] and rep["replay"]["tiers"]["tier1"] == 1


def test_qc_binding_full_sha_stale_and_prefix(tmp_path):
    c = wjl(tmp_path / "candidates_r1.jsonl", [{"id": "a"}])
    r = wjl(tmp_path / "candidates_r1.relations.jsonl", [])
    sc, sr = mixio.sha256_file(c), mixio.sha256_file(r)
    files = {"candidates_r1.jsonl": c, "candidates_r1.relations.jsonl": r}
    ok = {"inputs_sha256": {"candidates_r1.jsonl": sc, "candidates_r1.relations.jsonl": sr},
          "gates": {"sealed": {"candidates_r1.jsonl": {"input_sha256": sc[:16]}}},
          "previous_report": {"inputs_sha256": {"candidates_r1.jsonl": "0" * 64}}}     # history is skipped
    assert mx.qc_binding(ok, files) == []
    names_only = {"files": ["candidates_r1.jsonl", "candidates_r1.relations.jsonl"]}
    assert len(mx.qc_binding(names_only, files)) == 2                                  # F1 / F4 style: names only
    stale = {"inputs": {"candidates_r1.jsonl": {"sha256": "1" * 64}, "candidates_r1.relations.jsonl": {"sha256": sr}}}
    assert any("stale" in p for p in mx.qc_binding(stale, files))
    pre = ok | {"sealed": {"candidates_r1.jsonl": {"input_sha256": "abcdef012345"}}}
    assert any("stale" in p for p in mx.qc_binding(pre, files))


def test_heldout_dev_keys_global_packs_per_block():
    import replay_sample as rs
    dev = {"F1": [(yn("d1", "c", 1, structure_hash="h1", domain_pack="pk-held"), True),
                  (yn("d2", "c", 0) | {"state": "Shared state"}, False)],
           "public": [({"id": "pd", "group_id": "page:Foo", "state": "", "meta": {}}, False)]}
    ho = mx.HeldOut(dev, rs)
    a = yn("t1", "u", 1, block="F2", structure_hash="h1")
    b = yn("t2", "u", 1, block="F2", domain_pack="pk-held")               # another family's pack: allowed
    c = yn("t3", "u", 1, block="F1", domain_pack="pk-held")
    d = yn("t4", "u", 1, block="replay") | {"state": "shared  STATE ", "group_id": "page:Foo"}
    e = yn("t5", "u", 1, block="F3", family="F14")
    f = yn("t6", "u", 1, block="F3") | {"state": ""}
    assert ho.clash(a) == ["structure_hash"] and ho.clash(b) == [] and ho.clash(c) == ["domain_pack"]
    assert set(ho.clash(d)) == {"group_id", "state"} and ho.clash(e) == ["F14"] and ho.clash(f) == []
    rep = {}
    probs = ho.check([a, b, c, d, e, f], rep)
    assert probs and rep["s7_dev_overlap"]["training_rows_hit"]["F1"] == {"domain_pack": 1}


def test_refuse_held_out_strict_on_own_rows():
    sys.path.insert(0, str(mixio.LEAN / "c_src/formats/formats-1"))
    from fmt1 import pool
    known = sorted(pool._index("styles.jsonl"))[0]
    good = yn("o1", "u", 1, format_style=known)
    rep = {}
    assert mx.refuse_held_out(mixio.InputLog(), {"F1": [good]}, rep) == []
    assert mx.refuse_held_out(mixio.InputLog(), {"F1": [yn("o2", "u", 1, format_style="FS-typo")]}, rep) == ["F1"]
    nofs = yn("o3", "u", 1)
    nofs["meta"].pop("format_style")
    assert mx.refuse_held_out(mixio.InputLog(), {"F1": [nofs]}, rep) == ["F1"]
    pub = yn("p1", "u", 1, block="public", format_style="sq_s1")          # builder-local public style ids
    assert mx.refuse_held_out(mixio.InputLog(), {"public": [pub]}, rep) == []


def test_g10_cells_outside_2pp_are_problems():
    rows = [yn(f"a{i}", f"a{i}", int(i < 54), w="wd.A") for i in range(100)]          # n 100, 54% yes
    rows += [yn(f"b{i}", f"b{i}", int(i < 51), w="wd.B") for i in range(100)]         # n 100, 51% yes: fine
    rows += [yn(f"c{i}", f"c{i}", int(i < 18), w="wd.C") for i in range(20)]          # n 20, 90% yes: binomial
    rows += [yn(f"d{i}", f"d{i}", int(i < 25), w="wd.D") for i in range(52)]          # balancer for the aggregate
    rep = {}
    probs = mx.g10_checks(rows, rep, False)
    yr = rep["g10"]["yes_rate"]
    assert yr["cells_n_ge_50_outside_2pp"] == 1 and yr["cells_n_lt_50_binom_p_lt_0.01"] == 1   # wd.D 48.1%: inside
    cell = [p for p in probs if "outside 50 +/- 2 (family" in p]
    assert len(cell) == 1 and "wd.A" in cell[0] and "n=100 yes=0.540" in cell[0]
    assert any("small yes-rate cells" in p for p in probs)


def commit_row(i, typ, view, gold=1):
    r = yn(f"m{typ}{view}{i}", f"cm{typ}{view}{i}", gold, block="COMMIT", input_view=view)
    return r | {"source": f"commit_{typ}"}


def test_commit_subtargets_and_select_commit():
    st = cs.commit_subtargets(6000)
    assert st["route|message_only"] == 360 and st["route|message_diff"] == 840 and st["score|message_diff"] == 1200
    assert "score|message_only" not in st and sum(st.values()) == 6000
    small = cs.commit_subtargets(50)                 # 10 per type, 3 message-only of route / triage / gate
    rows = []
    for t in cs.COMMIT_TYPES:
        for v in ("message_diff", "message_only") if t in cs.COMMIT_MSG_ONLY else ("message_diff",):
            rows += [commit_row(i, t, v, gold=i % 2) for i in range(30)]
    units = [[i] for i in range(len(rows))]
    res = cs.select_commit(rows, units, None, 50)
    got = Counter(cs.commit_group(rows[i]) for u in res["sel"] for i in units[u])
    assert dict(got) == small and res["report"]["checks"]["commit_4.2_counts"]
    assert cs.stratum(rows[0], "na")[1].startswith("route|message_diff|") and cs.n_classes(cs.stratum(rows[0], "na")) == 2


def test_commit_counts_check():
    rows = [commit_row(i, t, "message_diff") for t in cs.COMMIT_TYPES for i in range(10)]
    probs = mx.commit_counts(rows, {}, target=50)
    assert probs and "route|message_only 0 vs 3" in probs[0]
    assert mx.commit_counts([], {}, target=50) == []


def test_commit_repo_check(famdir, monkeypatch):
    out = famdir / "COMMIT" / "out"
    wjl(out / "mixdev_S5.jsonl", [{"id": "dev1", "meta": {}}])
    side = wjl(famdir / "commit_meta.jsonl", [{"id": "dev1", "repo_group": "held/a"}, {"id": "t1", "repo_group": "ok/b"},
                                             {"id": "t2", "repo_group": "held/a"}])
    monkeypatch.setattr(mx, "COMMIT_SIDECARS", (side,))
    rows = [{"id": "t1", "_block": "COMMIT"}, {"id": "t2", "_block": "COMMIT"}, {"id": "t3", "_block": "COMMIT"}]
    probs = mx.commit_repo_check(mixio.InputLog(), rows, rep := {})
    assert rep["commit_held_out_repos"]["rows_in_held_out_repos"] == 1
    assert rep["commit_held_out_repos"]["rows_without_repo_group"] == 1 and len(probs) == 2
    assert mx.commit_repo_check(mixio.InputLog(), [{"id": "x", "_block": "F1"}], {}) == []


def test_final_blockers_qc_and_public(famdir, monkeypatch):
    f8_family(famdir)
    monkeypatch.setattr(mx, "LEAN", famdir)
    (famdir / "c_src/public/public-1/out").mkdir(parents=True)
    monkeypatch.setattr(mx, "PUBLIC_FILES", ("public-1/out/rows.jsonl",))
    monkeypatch.setattr(mx, "PUBLIC_RESERVE", ("public-1/out/reserve.jsonl",))
    monkeypatch.setattr(cs, "crowd_complete", lambda fam: [])
    b = mx.final_blockers(mixio.InputLog(), ["F8"])
    assert "F8: no QC_REPORT.json" in b and any(x.startswith("public-1: no QC record") for x in b)
    c = famdir / "F8/out/candidates_r1.jsonl"
    r = famdir / "F8/out/relations_candidates_r1.jsonl"
    (famdir / "F8/qc").mkdir()
    (famdir / "F8/qc/QC_REPORT.json").write_text(json.dumps({"pass": True, "inputs_sha256": {
        c.name: mixio.sha256_file(c), r.name: mixio.sha256_file(r)}}))
    assert not [x for x in mx.final_blockers(mixio.InputLog(), ["F8"]) if x.startswith("F8")]
    c.write_text(c.read_text() + "\n")                                       # regenerated after the QC pass
    assert any("stale" in x for x in mx.final_blockers(mixio.InputLog(), ["F8"]) if x.startswith("F8"))


def test_heldout_template_state_not_matched():
    import replay_sample as rs
    hdr = '{"task": "headline review"}'
    dev = {"public": [({"id": "d1", "group_id": "g1", "state": hdr, "meta": {}}, False),
                      ({"id": "d2", "group_id": "g2", "state": hdr, "meta": {}}, False),
                      ({"id": "d3", "group_id": "g3", "state": "one passage", "meta": {}}, False)]}
    ho = mx.HeldOut(dev, rs)
    t = {"id": "t", "group_id": "gt", "state": hdr, "_block": "public", "meta": {}}
    u = {"id": "u", "group_id": "gu", "state": "One  passage", "_block": "public", "meta": {}}
    assert ho.clash(t) == [] and ho.clash(u) == ["state"]
    rep = {}
    ho.check([t, u], rep)
    assert rep["s7_dev_overlap"]["training_rows_on_template_states"] == {"public": 1}


def test_parent_names_dicts_b3():
    import mixer
    par = ["gd_onet_occupation", {"kind": "pack_file", "path": "c_src/packs/p.jsonl", "sha256": "x"},
           {"kind": "domain_pack", "id": "ghc:cb.F10.s1", "source": "ghc", "parents": ["gab"]},
           {"kind": "domain_pack", "id": "mams:x", "source": None, "parents": None}]
    assert mixer.parent_names(par) == ["gd_onet_occupation", "c_src/packs/p.jsonl", "ghc:cb.F10.s1", "ghc", "gab",
                                       "mams:x"]
    q = mixer.denylist_query([{"source": "s1", "meta": {}}], {"s1": par})
    assert "ghc" in q["s1"]["parents"]
