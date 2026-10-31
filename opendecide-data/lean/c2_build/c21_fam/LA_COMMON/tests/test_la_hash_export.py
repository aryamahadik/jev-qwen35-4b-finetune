import json
import os

import pytest

from LA_COMMON import hash_export as H
from tool_engine import hash_export as hx

FAM = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.parametrize("family", H.FAMILIES)
def test_export_is_hashes_only_and_deterministic(family):
    a = H.build(family, created="2026-10-18T00:00:00Z")
    b = H.build(family, created="2026-10-18T00:00:00Z")
    assert a == b
    assert hx.assert_no_text(a)
    assert a["wording_pool"]["is_stub"] is False and a["wording_pool"]["n_templates"] >= 50 * a["wording_pool"]["n_forms"]
    assert a["tables"]["template_hash"] and a["names"]["training_fingerprint"] == "0844fd92219a"
    # no wording text leaks into the export: every template is present only as a sha256
    pool = json.load(open(os.path.join(FAM, family, "pools", "%s_wording_pool_v1.json" % family)))
    blob = json.dumps(a)
    for form, tpls in list(pool["forms"].items())[:3]:
        assert tpls[0] not in blob


@pytest.mark.parametrize("family", H.FAMILIES)
def test_checked_in_export_is_current(family):
    """Any change to a template, pool, table, rendering or solver file = a new export + re-stamp (plan 16.1 step 6)."""
    path = os.path.join(FAM, family, "HASH_EXPORT.json")
    if not os.path.exists(path):
        pytest.skip("HASH_EXPORT.json not written yet")
    on_disk = json.load(open(path))
    cur = H.build(family, created=on_disk["created_utc"])
    assert cur == on_disk, "HASH_EXPORT is stale: run python3 -I c21_fam/LA_COMMON/hash_export.py %s" % family
    sha = open(os.path.join(FAM, family, "HASH_EXPORT.sha256")).read().split()[0]
    assert sha == H._sha_file(path)
