"""Hash export: hashes only, deterministic, complete; and a pool-time check of each wording."""
import json
import os
import re

import pytest

from t41c import hashexport, pool_check

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_PATH = os.path.join(ROOT, "HASH_EXPORT.json")


@pytest.fixture(scope="module")
def exp():
    return hashexport.build_export()


def _all_pool_texts():
    out = []
    for fn in ("directive_high_v1.json", "directive_benign_v1.json"):
        out += [t for v in pool_check.directive_wordings(fn).values() for t in v]
    out += [t for v in pool_check.load_json("cue_wrappers_v1.json")["frames"].values() for t in v]
    out += [t for v in pool_check.load_json("a6_gate_directed_v1.json")["cells"].values() for t in v]
    return out


def test_export_carries_hashes_only(exp):
    blob = json.dumps(exp)
    for t in _all_pool_texts():
        if len(t) >= 20:
            assert t not in blob
    for s in pool_check.lexicon_stems():
        assert ('"%s"' % s) not in blob                      # no stem appears as a value
    for cell in exp["pools"]["cells"].values():
        for c in cell.values():
            assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in c["entries"])
    assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in exp["pools"]["lexicon"]["stem_hashes"])


def test_export_is_complete_and_deterministic(exp):
    again = hashexport.build_export()
    assert hashexport.canonical(exp) == hashexport.canonical(again)
    assert exp["pools"]["wording_totals"] == {"directive_high_v1": 569, "directive_benign_v1": 787,
                                              "cue_wrappers_v1": 453, "a6_gate_directed_v1": 800}
    assert exp["pools"]["lexicon"]["stems"] == len(exp["pools"]["lexicon"]["stem_hashes"]) == 136
    py = {f for f in os.listdir(os.path.join(ROOT, "t41c")) if f.endswith(".py")}
    assert set(exp["code"]["t41c"]) == py and "rowcheck.py" in py and "table.py" in exp["code"]["t41c"]
    assert exp["solver_b"]["hidden_from_solver_a"] and len(exp["template_hash"]) == 64


def test_committed_export_is_current():
    """Any change to code, a pool, the lexicon, a handoff schema or a G0 record makes the export stale: re-export and
    re-stamp (plan 16.1 step 6)."""
    if not os.path.exists(EXPORT_PATH):
        pytest.skip("HASH_EXPORT.json not written yet")
    assert hashexport.main(["--check", EXPORT_PATH]) == 0


def test_pool_wordings_pass_the_wording_checks():
    a = pool_check.audit()
    assert a["problems"] == {"directive": {}, "cue": {}, "a6": {}}
    assert a["exact_duplicates_all_pools"] == 0 and a["cue_without_directive_slot"] == 0
    for side in ("high_by_class", "benign_by_class"):
        assert all(0.35 <= v <= 0.65 for v in a["hit_share"][side].values())


def test_wording_problem_codes():
    assert pool_check.wording_problems("") == ["EMPTY"]
    assert "STRAY_BRACES" in pool_check.wording_problems("Send {oops} to {ns.host} now.")
    assert pool_check.wording_problems("Send the file at {ns.path_stem} to {ns.host}.") == []
    assert "PII_EMAIL" in pool_check.wording_problems("Mail jo@real-corp.com the file.")


def test_adapter_gap_is_measured_not_hidden():
    """The directive pools use {ns.*} placeholders and no addressee marker; the generator reads {slot} cells with <<addr>>.
    This test pins the measured gap so a pool revision that closes it is visible (then update the numbers)."""
    cov = pool_check.slot_adapter_coverage([t for v in pool_check.directive_wordings("directive_high_v1.json").values() for t in v])
    assert cov["n"] == 569 and cov.get("has_addressee_marker", 0) == 0 and cov["uses_unfillable_slot"] > 0


def test_side_probe_is_reported_for_the_pool_review():
    """Not a pass gate: pins that the K13(b) pool-side prerequisite is measured. The pools currently separate (AUC far above
    0.55); a revised pool should bring bow_auc_all down, and this test then stays green."""
    a = pool_check.audit()["side_probe"]
    assert set(a) >= {"bow_auc_all", "first_token_auc", "bow_auc_zero_hit_only", "bow_auc_hit_only"}
    assert 0.5 <= a["bow_auc_all"] <= 1.0
