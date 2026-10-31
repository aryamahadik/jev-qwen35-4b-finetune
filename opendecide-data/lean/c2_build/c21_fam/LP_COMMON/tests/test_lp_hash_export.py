import json
import os

import pytest

from LP_COMMON import hash_export as H
from tool_engine import hash_export as hx

FAM = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.parametrize("family", H.FAMILIES)
def test_export_is_hashes_only_deterministic_and_covers_code_pool_tables_and_names(family):
    a = H.build(family, created="2026-10-18T00:00:00Z")
    b = H.build(family, created="2026-10-18T00:00:00Z")
    assert a == b
    assert hx.assert_no_text(a)
    wp = a["wording_pool"]
    assert wp["is_stub"] is False and wp["n_templates"] >= 50 * wp["n_forms"] - 100      # per-form counts are validated by the family pool guards
    assert a["names"]["training_fingerprint"] == "0844fd92219a" and len(a["tables"]) > 20
    assert any(k.startswith("LP_COMMON/") for k in a["code"]) and any(k.startswith(family + "/") for k in a["code"])
    assert a["solver_b_status"] in ("absent", "present") and (a["solver_b_status"] == "present") == bool(a["solver_b"])
    assert a["code_combined_sha256"] and a["export_sha256"]
    pool = json.load(open(os.path.join(FAM, family, "pools", "wording_pool.json")))
    blob = json.dumps(a)
    for form, ws in list(pool["forms"].items())[:4]:
        assert ws[0]["text"] not in blob                                              # a wording is present only as a sha256


@pytest.mark.parametrize("family", H.FAMILIES)
def test_checked_in_export_is_current(family):
    """Any change to a template, pool, table, rendering or test file = a new export + re-stamp of the affected rows (plan 16.1 step 6)."""
    path = os.path.join(FAM, family, "HASH_EXPORT.json")
    if not os.path.exists(path):
        pytest.skip("HASH_EXPORT.json not written yet")
    on_disk = json.load(open(path))
    cur = H.build(family, created=on_disk["created_utc"])
    assert cur == on_disk, "HASH_EXPORT is stale: run python3 -I c21_fam/LP_COMMON/hash_export.py %s" % family
    sha = open(os.path.join(FAM, family, "HASH_EXPORT.sha256")).read().split()[0]
    assert sha == H._sha_file(path)


def test_changing_a_pool_or_a_table_changes_the_export_sha(monkeypatch):
    base = H.build("T63", created="x")
    pool_path = os.path.join(FAM, "T63", "pools", "wording_pool.json")
    pool = json.load(open(pool_path))
    pool["forms"]["T63-Q-LIC"][0]["text"] += " "
    import LP_COMMON.hash_export as mod
    monkeypatch.setattr(mod.json, "load", lambda f, _orig=json.load: pool if getattr(f, "name", "") == pool_path else _orig(f))
    changed = H.build("T63", created="x")
    assert changed["wording_pool"]["forms"]["T63-Q-LIC"]["template_sha256"][0] != base["wording_pool"]["forms"]["T63-Q-LIC"]["template_sha256"][0]
    assert changed["export_sha256"] != base["export_sha256"]
