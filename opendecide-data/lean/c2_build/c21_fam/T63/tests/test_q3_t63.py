"""Opus ruling Q3 (18 Oct 2026), recorded before any pool rows. 3a: EX-B (B1 and B2) rows only from the sha-bound L-0 image-record export, LIC rows only from the
hashed Opus table; the pool writer refuses fixture shas and standin != False, and says exactly which production file is missing. 3b: the NEAR 'age >= A2, low
downloads' corner is NOT built (no NM-R5 in C2.1); disclosure line and C2.2 item are in the README.

Every source used below is a TEST-ONLY synthetic one (image id 'unit-test-image', a table with one cell changed): it is not the L-0 export and not the Opus table.
Nothing here is evidence for production; it only exercises the refusals."""
import copy
import json
import os

import pytest

from LP_COMMON import pipeline as pl
from T63 import checked, config as C, dryrun, exists, generator as G, lic, near, pool_writer as PW, solver_a

FAMDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = "a" * 64


def _unit_export():
    d = copy.deepcopy(dryrun.fixture_exports().data)
    d["fixture"] = False
    d["image_id"] = "unit-test-image"
    d["sha256"] = exists.ExportSet(d).sha
    return exists.ExportSet(d)


def _unit_table():
    d = copy.deepcopy(lic.fixture_table().data)
    d["fixture"] = False
    k = sorted(d["cells"])[0]
    d["cells"][k] = dict(d["cells"][k], label="REVIEW" if d["cells"][k]["label"] != "REVIEW" else "COMPATIBLE")
    d["sha256"] = lic.LicTable(d).sha
    return lic.LicTable(d)


def _hook():
    h = pl.TestDoubleHook(registry_sha=REG)
    h.method_set_version = "unit-test-ms"
    return h


@pytest.fixture(scope="module")
def src():
    ex, tb = _unit_export(), _unit_table()
    return {"exports": ex, "image_record": {"image_id": ex.image_id, "stdlib_export_sha256": ex.sha},
            "table": tb, "table_record": {"table_id": "T63-LIC-TABLE", "sha256": tb.sha}}


@pytest.fixture(scope="module")
def good(src):
    """Rows built from the (test-only) non-fixture sources with a non-test-double stamp."""
    rows = checked.run(300, 5, _hook(), standin=True, exports=src["exports"], table=src["table"])[0]
    assert {r["sub_block"] for r in rows} >= {"EX-B1", "EX-B2", "LIC", "NEAR", "EX-A1"}
    return rows


@pytest.fixture(scope="module")
def fixture_rows():
    return dryrun.dry_rows(300, seed=5)[0]


def _by(rows, pred):
    return [copy.deepcopy(r) for r in rows if pred(r)]


EXB = lambda r: r["sub_block"] in ("EX-B1", "EX-B2")     # noqa: E731
LIC = lambda r: r["head"] == "LIC"                       # noqa: E731
OTHER = lambda r: r["head"] == "NEAR" or r["sub_block"] in ("EX-A1", "EX-A2")   # noqa: E731


# ------------------------------------------------------------------------------------------------ 3a: the writer's refusals
@pytest.mark.parametrize("standin", [True, None, 0, "", "no"])
def test_writer_requires_the_literal_standin_false(good, src, tmp_path, standin):
    out = str(tmp_path / "b.jsonl")
    with pytest.raises(PW.PoolRefused):
        PW.write_pool(_by(good, OTHER)[:5], out, standin=standin, sources=src)
    assert not os.path.exists(out)


def test_writer_happy_path_is_write_once_and_records_the_shas(good, src, tmp_path):
    out = str(tmp_path / "b.jsonl")
    rows = _by(good, lambda r: True)
    res = PW.write_pool(rows, out, standin=False, sources=src)
    assert res["rows"] == len(rows) == len(open(out).read().splitlines())
    assert res["export_sha"] == src["exports"].sha and res["image_id"] == "unit-test-image" and res["table_sha"] == src["table"].sha
    assert res["ex_b_rows"] > 0 and res["lic_rows"] > 0
    with pytest.raises(PW.PoolRefused):                                   # write-once
        PW.write_pool(rows, out, standin=False, sources=src)


def test_missing_production_sources_are_named_with_their_producer(fixture_rows, tmp_path):
    out = str(tmp_path / "b.jsonl")
    for pred, roles, who in ((EXB, {"stdlib_export", "image_record"}, "L-0"), (LIC, {"lic_table", "lic_table_record"}, "Opus"),
                             (lambda r: EXB(r) or LIC(r), {"stdlib_export", "image_record", "lic_table", "lic_table_record"}, "L-0")):
        with pytest.raises(PW.SourceMissing) as ei:
            PW.write_pool(_by(fixture_rows, pred), out, standin=False, base_dir=str(tmp_path))
        e = ei.value
        assert {m[0] for m in e.missing} == roles
        for role, path, producer in e.missing:
            assert path.startswith(str(tmp_path)) and os.path.basename(path) == PW.SOURCES[role][0] and path in str(e) and who in str(e)
        assert not os.path.exists(out)
    assert os.path.basename(PW.source_paths()["lic_table"]) == "T63_LIC_TABLE.json"


def test_partial_sources_name_only_what_is_missing(good, src, tmp_path):
    only_export = {k: src[k] for k in ("exports", "image_record")}
    with pytest.raises(PW.SourceMissing) as ei:
        PW.write_pool(_by(good, lambda r: EXB(r) or LIC(r)), str(tmp_path / "b.jsonl"), standin=False, sources=only_export)
    assert {m[0] for m in ei.value.missing} == {"lic_table", "lic_table_record"}
    with pytest.raises(PW.SourceMissing) as ei:                            # an export with no image record cannot be checked against anything
        PW.write_pool(_by(good, EXB), str(tmp_path / "b2.jsonl"), standin=False, sources={"exports": src["exports"]})
    assert {m[0] for m in ei.value.missing} == {"image_record"}


def test_a_batch_without_ex_b_and_lic_rows_needs_no_source(good, tmp_path):
    out = str(tmp_path / "o.jsonl")
    assert PW.write_pool(_by(good, OTHER), out, standin=False, base_dir=str(tmp_path))["rows"] > 0


def test_fixture_flagged_sources_and_fixture_shas_are_refused(fixture_rows, src, tmp_path):
    fx_ex, fx_tb = dryrun.fixture_exports(), lic.fixture_table()
    exb, lc = _by(fixture_rows, EXB), _by(fixture_rows, LIC)
    rec_ex = {"image_id": fx_ex.image_id, "stdlib_export_sha256": fx_ex.sha}
    rec_tb = {"table_id": "T63-LIC-TABLE", "sha256": fx_tb.sha}
    with pytest.raises(PW.PoolRefused):                                    # flagged fixture, even with a matching record
        PW.write_pool(exb, str(tmp_path / "1"), standin=False, sources={"exports": fx_ex, "image_record": rec_ex})
    with pytest.raises(PW.PoolRefused):
        PW.write_pool(lc, str(tmp_path / "2"), standin=False, sources={"table": fx_tb, "table_record": rec_tb})
    # the same content with the `fixture` flag stripped and the sha declared (the K-skeptic trick) is still a fixture sha
    d = copy.deepcopy(fx_ex.data)
    d.pop("fixture")
    d["sha256"] = exists.ExportSet(d).sha
    stripped = exists.ExportSet(d)
    stripped.require_real()
    with pytest.raises(PW.PoolRefused) as ei:
        PW.write_pool(exb, str(tmp_path / "3"), standin=False, sources={"exports": stripped, "image_record": rec_ex})
    assert "FIXTURE sha" in str(ei.value)
    d = copy.deepcopy(fx_tb.data)
    d.pop("fixture")
    d["sha256"] = lic.LicTable(d).sha
    with pytest.raises(PW.PoolRefused) as ei:
        PW.write_pool(lc, str(tmp_path / "4"), standin=False, sources={"table": lic.LicTable(d), "table_record": rec_tb})
    assert "FIXTURE sha" in str(ei.value)
    for i in range(1, 5):
        assert not os.path.exists(str(tmp_path / str(i)))


def test_a_row_carrying_a_fixture_sha_is_refused_whatever_its_head(good, src, tmp_path):
    fx_ex, fx_tb = dryrun.fixture_exports(), lic.fixture_table()
    rows = _by(good, EXB)[:3]
    for r in rows:                                                          # every place a sha sits
        r["spec"]["export_sha"] = r["witness_inputs"]["export_sha"] = fx_ex.sha
        r["manifest"]["pins"] = "image:%s;export:%s" % (r["spec"]["image_id"], fx_ex.sha)
    with pytest.raises(PW.PoolRefused) as ei:
        PW.write_pool(rows, str(tmp_path / "a"), standin=False, sources=src)
    assert "fixture_sha" in str(ei.value)
    near_row = _by(good, OTHER)[0]
    near_row["manifest"]["pins"] = "image:x;export:%s" % fx_ex.sha        # a non-EX-B row must not carry one either
    with pytest.raises(PW.PoolRefused) as ei:
        PW.write_pool([near_row], str(tmp_path / "b"), standin=False, sources=src)
    assert "fixture_sha" in str(ei.value)
    lrow = _by(good, LIC)[0]
    lrow["spec"]["table_sha"] = lrow["witness_inputs"]["table_sha"] = fx_tb.sha
    with pytest.raises(PW.PoolRefused) as ei:
        PW.write_pool([lrow], str(tmp_path / "c"), standin=False, sources=src)
    assert "fixture_sha" in str(ei.value)


def test_row_shas_must_equal_the_recorded_ones(good, src, tmp_path):
    def refused(rows, sources, needle):
        out = str(tmp_path / ("x%d" % len(os.listdir(str(tmp_path)))))
        with pytest.raises(PW.PoolRefused) as ei:
            PW.write_pool(rows, out, standin=False, sources=sources)
        assert needle in str(ei.value) and not os.path.exists(out)

    r = _by(good, lambda x: x["sub_block"] == "EX-B1")[:1]
    r[0]["witness_inputs"]["export_sha"] = "f" * 64                                         # EX-B1 carries the sha in the witness too
    refused(r, src, "export_sha_mismatch")
    r = _by(good, lambda x: x["sub_block"] == "EX-B2")[:1]
    r[0]["spec"]["image_id"] = "other-image"
    refused(r, src, "image_id_mismatch")
    r = _by(good, EXB)[:1]
    r[0]["manifest"]["pins"] = "n/a:no_toolchain"
    refused(r, src, "pins_mismatch")
    r = _by(good, LIC)[:1]
    r[0]["spec"]["table_sha"] = "f" * 64
    refused(r, src, "table_sha_mismatch")
    # a source that is not the recorded one
    bad_rec = dict(src["image_record"], stdlib_export_sha256="f" * 64)
    refused(_by(good, EXB)[:2], dict(src, image_record=bad_rec), "recorded by the L-0 image record")
    refused(_by(good, EXB)[:2], dict(src, image_record=dict(src["image_record"], image_id="x")), "image id")
    refused(_by(good, EXB)[:2], dict(src, image_record={}), "image_id")
    refused(_by(good, LIC)[:2], dict(src, table_record=dict(src["table_record"], sha256="f" * 64)), "recorded by the Opus table record")
    refused(_by(good, LIC)[:2], dict(src, table_record={"sha256": src["table"].sha}), "table_id")


def test_rows_are_re_read_against_the_real_sources(good, src, tmp_path):
    def refused(rows, needle):
        with pytest.raises(PW.PoolRefused) as ei:
            PW.write_pool(rows, str(tmp_path / ("y%d" % len(os.listdir(str(tmp_path))))), standin=False, sources=src)
        assert needle in str(ei.value)

    r = _by(good, EXB)[:1]
    r[0]["gold"] = "YES" if r[0]["gold"] == "NO" else "NO"
    refused(r, "gold_not_export_membership")
    r = _by(good, lambda x: x["sub_block"] == "EX-B1")[:1]
    r[0]["spec"]["shown"] = r[0]["spec"]["shown"][1:]
    refused(r, "b1_list_not_export_slice")
    r = _by(good, EXB)[:1]
    r[0]["spec"]["module"] = "no_such_module"
    refused(r, "module_not_in_export")
    r = _by(good, LIC)[:1]
    r[0]["gold"] = next(x for x in C.LIC_LABELS if x != r[0]["gold"])
    refused(r, "gold_not_table_label")
    r = _by(good, LIC)[:1]
    r[0]["meta"]["construction_id"] = "LC:other"
    refused(r, "cell_id_mismatch")
    r = _by(good, LIC)[:1]
    refused(r + copy.deepcopy(r), "cell_used_twice")
    r = _by(good, LIC)[:1]
    r[0]["spec"]["dep"] = "no-such-licence"
    refused(r, "cell_not_in_table")


def test_only_stamped_clean_non_test_double_rows_are_written(good, src, tmp_path, fixture_rows):
    r = _by(good, OTHER)[:1]
    r[0].pop("stamp")
    with pytest.raises(PW.PoolRefused) as ei:
        PW.write_pool(r, str(tmp_path / "s1"), standin=False, sources=src)
    assert "not_stamped_clean" in str(ei.value)
    with pytest.raises(PW.PoolRefused) as ei:                               # the dry run's TEST DOUBLE stamp
        PW.write_pool(_by(fixture_rows, OTHER)[:3], str(tmp_path / "s2"), standin=False, sources=src)
    assert "test_double_stamp" in str(ei.value)


# --------------------------------------------------------------------------------- 3a: generator side (no silent fallback)
def test_no_export_or_table_means_an_error_not_a_fallback(good):
    r = _by(good, EXB)[0]
    with pytest.raises(ValueError):
        solver_a.make_gold_a(None, None)(r)
    with pytest.raises(ValueError):
        solver_a.make_gold_a(dryrun.fixture_exports(), None)(r)               # a different export than the row's: sha differs
    w = copy.deepcopy(r)
    w["witness_inputs"]["export_sha"] = "f" * 64                              # EX-B1 and EX-B2 alike: the witness sha must be the bound one
    with pytest.raises(ValueError):
        solver_a.make_gold_a(_unit_export(), None)(w)
    lr = _by(good, LIC)[0]
    with pytest.raises(ValueError):
        solver_a.make_gold_a(None, None)(lr)
    lw = copy.deepcopy(lr)
    lw["witness_inputs"]["table_sha"] = "f" * 64
    with pytest.raises(ValueError):
        solver_a.make_gold_a(None, _unit_table())(lw)
    ok = solver_a.make_gold_a(_unit_export(), _unit_table())
    assert ok(r) == r["gold"] and ok(lr) == lr["gold"]


def test_builders_raise_without_their_source():
    ctx = G.Ctx(seed=1, standin=True)                                          # no exports, no table
    with pytest.raises(ValueError):
        exists.gen_b(ctx, {"seed": "s", "gid": "g", "cell": {"lang": "python", "view": "B2", "kind": None, "label": "YES"}})
    with pytest.raises(ValueError):
        G._generate_lic(ctx, {"seed": "s", "gid": "g", "cell": {"type": "single", "label": "COMPATIBLE", "target_level": "L1", "mixed": True}})
    assert not any(c.get("view") for c in G.build_plan(total=300, seed=1, with_b=False))      # and a plan without an export plans no EX-B cell


def test_production_context_refuses_a_fixture_sha_even_when_the_flag_is_stripped():
    pool = os.path.join(FAMDIR, "pools", "wording_pool.json")
    d = copy.deepcopy(dryrun.fixture_exports().data)
    d.pop("fixture")
    d["sha256"] = exists.ExportSet(d).sha
    with pytest.raises(PW.PoolRefused):
        G.Ctx(seed=1, standin=False, pool_path=pool, exports=exists.ExportSet(d))
    d = copy.deepcopy(lic.fixture_table().data)
    d.pop("fixture")
    d["sha256"] = lic.LicTable(d).sha
    with pytest.raises(PW.PoolRefused):
        G.Ctx(seed=1, standin=False, pool_path=pool, table=lic.LicTable(d))
    G.Ctx(seed=1, standin=False, pool_path=pool, exports=_unit_export(), table=_unit_table())      # a non-fixture source is accepted by the context


def test_ex_b1_and_b2_rows_both_carry_the_export_sha_and_image_id(good):
    for sub in ("EX-B1", "EX-B2"):
        rs = [r for r in good if r["sub_block"] == sub]
        assert rs
        for r in rs:
            assert r["witness_inputs"]["export_sha"] == r["spec"]["export_sha"] and r["spec"]["image_id"] == "unit-test-image"
            assert r["manifest"]["pins"] == "image:unit-test-image;export:%s" % r["spec"]["export_sha"]


# -------------------------------------------------------------------------------------------------------------- 3b: NEAR corner
def test_no_near_row_builds_the_old_but_not_popular_corner(good):
    """NM-R5 'old but not popular' (Q with age >= A2 and downloads below D2, everything else as for a squat) is NOT a C2.1 NO kind: no registered id, no quota."""
    assert "NM-R5" not in C.NM_R and set(C.NM_R) == {"NM-R1", "NM-R2", "NM-R3", "NM-R4"}
    near_rows = [r for r in good if r["head"] == "NEAR"]
    assert len(near_rows) > 100
    for r in near_rows:
        s = r["spec"]
        q = s["query"]
        p = next(e for e in s["entries"] if e["name"] == q["name"] and e["registry"] == q["registry"])
        for e in s["entries"]:
            if e is p or e["registry"] != q["registry"]:
                continue
            corner = (e["age"] in C.ESTABLISHED and e["dl"] != "D2" and near.near_relations(p["name"], e["name"]) and not near.linked(p, e) and near.newer(p, e))
            assert not corner, r["row_id"]
        if r["gold"] == "NO" and not s.get("t8_variant"):
            assert r["meta"]["no_kind"] in (None,) + C.NM_R


def test_downloads_stays_a_conjunct_of_established_in_the_gold_function():
    assert near.established({"age": "A3", "dl": "D2"}) and not near.established({"age": "A3", "dl": "D1"}) and not near.established({"age": "A2", "dl": "D0"})


def test_readme_records_the_disclosure_line_and_the_c2_2_item():
    txt = open(os.path.join(FAMDIR, "README.md"), encoding="utf-8").read()
    assert "downloads is never the deciding conjunct of 'established' in a C2.1 NEAR row" in txt
    assert "NM-R5" in txt and "old but not popular" in txt and "C2.2" in txt
    assert "Opus ruling Q3" in txt and "T63_STDLIB_EXPORT.json" in txt and "T63_LIC_TABLE.json" in txt
