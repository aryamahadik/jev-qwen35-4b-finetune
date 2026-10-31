"""Build-skeptic tests (Sun 18 Oct): EX-A1 position cue, undeclared export / table shas, K2 provenance and the K10 axis-reading share, the opaque B-view id."""
import copy

import pytest

from T63 import dryrun, exists, gates, generator as G, lic, schema


@pytest.fixture(scope="module")
def dry():
    return dryrun.dry_rows(900, seed=13)[0]


def test_ex_a1_query_is_strictly_inside_the_shown_range_for_both_labels(dry):
    sel = [r for r in dry if r["sub_block"] == "EX-A1"]
    assert len(sel) > 100 and {r["gold"] for r in sel} == {"YES", "NO"}
    for r in sel:
        lst, q = r["spec"]["listing"], r["spec"]["query_name"]
        assert lst[0] < q < lst[-1], (r["row_id"], r["gold"])


def test_ex_a1_single_rows_list_a_one_edit_neighbour_of_the_query(dry):
    for r in dry:
        s = r["spec"]
        if r["sub_block"] == "EX-A1" and not r["meta"].get("pair_id"):
            assert any(exists._edit1(s["query_name"], n) for n in s["listing"] if n != s["query_name"]), r["row_id"]


def test_edge_free_refuses_a_query_at_the_edge():
    sp = {"listing": ["aa", "bb", "cc"], "query_name": "aa"}
    with pytest.raises(exists.Reject):
        exists._edge_free([sp])
    exists._edge_free([{"listing": ["aa", "bb", "cc"], "query_name": "bb"}])


def test_real_export_and_table_must_declare_their_sha():
    ex = dryrun.fixture_exports()
    data = copy.deepcopy(ex.data)
    data.pop("fixture")
    with pytest.raises(ValueError):
        exists.ExportSet(data).require_real()                        # no declared sha
    data["sha256"] = exists.ExportSet(data).sha
    exists.ExportSet(data).require_real()
    data["sha256"] = "0" * 64
    with pytest.raises(ValueError):
        exists.ExportSet(data)                                       # declared sha does not match the content
    tb = lic.fixture_table()
    d = copy.deepcopy(tb.data)
    d.pop("fixture")
    with pytest.raises(ValueError):
        lic.LicTable(d).require_real()
    d["sha256"] = lic.LicTable(d).sha
    lic.LicTable(d).require_real()


def test_k2_provenance_gate(dry):
    assert gates.k2_provenance(dry)["ok"]
    bad = [dict(r, spec=dict(r["spec"], image_id=None)) if r["sub_block"] in ("EX-B1", "EX-B2") else r for r in dry]
    assert not gates.k2_provenance(bad)["ok"]
    other = [dict(r, spec=dict(r["spec"], table_sha="f" * 64)) if r["head"] == "LIC" and i % 2 else r for i, r in enumerate(dry)]
    assert not gates.k2_provenance(other)["ok"]


def test_k10_requires_the_mixed_pair_share(dry):
    lic_rows = [r for r in dry if r["head"] == "LIC"]
    res = gates.k10_lic(lic_rows)
    assert res["ok"] and res["mixed_pair_share"] >= 0.40
    flat = [dict(r, spec=dict(r["spec"], mixed_pair=False)) for r in lic_rows]
    assert not gates.k10_lic(flat)["ok"]


def test_b_view_id_is_opaque_and_the_pair_letter_is_hidden(dry):
    pairs = [r for r in dry if r["meta"].get("pair_id")]
    assert pairs
    for r in dry:
        bv = schema.b_view(r)
        assert bv["row_id"] != r["row_id"] and not bv["row_id"].endswith(("-a", "-b"))
    # why: in the NEAR pair builders the first member (-a) is always the YES row, so a B that saw the real id could read the label off it
    near_pairs = [r for r in pairs if r["head"] == "NEAR"]
    assert near_pairs and all((r["gold"] == "YES") == r["row_id"].endswith("-a") for r in near_pairs)


def _pool_with(near_texts):
    import json
    pool = json.load(open(os.path.join(FAMDIR, "pools", "wording_pool.json")))
    pool["forms"]["T63-Q-NEAR"] = [{"id": "w%03d" % k, "text": t} for k, t in enumerate(near_texts)]
    return pool


import os      # noqa: E402

FAMDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_the_shipped_pool_passes_the_pool_guard():
    import json
    pool = json.load(open(os.path.join(FAMDIR, "pools", "wording_pool.json")))
    assert G.pool_problems(pool) == []
    assert len(pool["forms"]["T63-Q-NEAR"]) >= 50


def test_near_frames_that_ask_for_a_near_name_are_refused():
    good = ["Under the definitions, is {pkg} on {registry} a lookalike or a confusion? #%d" % k for k in range(60)]
    assert G.pool_problems(_pool_with(good)) == []
    bad = good[:55] + ["Is there a package on {registry} whose name sits close to {pkg}?"] * 5
    probs = G.pool_problems(_pool_with(bad))
    assert probs and any("lacks" in p for p in probs)
    one_sided = good[:55] + ["Is {pkg} on {registry} a lookalike?"] * 5
    assert any("confusion" in p for p in G.pool_problems(_pool_with(one_sided)))


def test_production_context_refuses_a_bad_pool():
    from LP_COMMON import wording
    bad = _pool_with(["Is there a package on {registry} whose name sits close to {pkg}? #%d" % k for k in range(60)])
    with pytest.raises(wording.PoolError):
        G.Ctx(seed=1, standin=False, pool=bad)


def test_row_schema_pins_the_keyboard_map_that_solver_a_uses():
    from T63 import near
    schema_md = open(os.path.join(FAMDIR, "ROW_SCHEMA.md")).read()
    adj = " ".join("%s:%s" % (k, "".join(sorted(v))) for k, v in sorted(near.KEYBOARD.items()))
    assert adj in schema_md
