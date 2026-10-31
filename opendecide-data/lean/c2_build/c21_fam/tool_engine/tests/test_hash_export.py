"""The template / wording-pool HASH EXPORTS (T54, T55, T56): hashes only, no text, and CURRENT. A change to any hashed file (generator,
renderer, solver A or B, wording seed, pool, engine file, names manifest) makes the committed export stale and this test fails: the
export is then rebuilt (python3 -I tNN_hash_export.py) and the affected rows are re-stamped (plan 16.1 step 6)."""
import hashlib
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))          # .../c21_fam
for fam in ("T54", "T55", "T56"):
    for p in (os.path.join(ROOT, fam),):
        if p not in sys.path:
            sys.path.insert(0, p)

import t54_hash_export  # noqa: E402
import t55_hash_export  # noqa: E402
import t56_hash_export  # noqa: E402
from tool_engine import hash_export as hx  # noqa: E402

MODS = {"T54": t54_hash_export, "T55": t55_hash_export, "T56": t56_hash_export}


def _exp(fam):
    with open(os.path.join(ROOT, fam, "HASH_EXPORT.json"), "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("fam", sorted(MODS))
def test_export_has_no_text_and_its_self_hash_holds(fam):
    exp = _exp(fam)
    assert hx.assert_no_text(exp)
    body = {k: v for k, v in exp.items() if k != "export_sha256"}
    assert hx._sha_obj(body) == exp["export_sha256"]
    with open(os.path.join(ROOT, fam, "HASH_EXPORT.json"), "rb") as f:
        line = open(os.path.join(ROOT, fam, "HASH_EXPORT.sha256")).read().split()
        assert line[0] == hashlib.sha256(f.read()).hexdigest() and line[1] == "HASH_EXPORT.json"
    assert exp["kind"] == "hashes_only_no_text" and exp["family"] == fam
    # every template of the expanded pool has its own digest, and no template text is stored
    wp = exp["wording_pool"]
    assert wp["n_templates"] == sum(f["count"] for f in wp["forms"].values()) == sum(len(f["template_sha256"]) for f in wp["forms"].values())


@pytest.mark.parametrize("fam", sorted(MODS))
def test_export_is_current_for_every_hashed_file(fam):
    exp = _exp(fam)
    fresh = MODS[fam].build(created=exp["created_utc"])
    assert fresh == exp, "stale export: rebuild it and re-stamp the affected rows"


def test_assert_no_text_refuses_text():
    with pytest.raises(ValueError):
        hx.assert_no_text({"tables": {"x": "Make the tool call now, all values are available"}})
    with pytest.raises(ValueError):
        hx.assert_no_text({"code": {"some text": "0" * 64}})
