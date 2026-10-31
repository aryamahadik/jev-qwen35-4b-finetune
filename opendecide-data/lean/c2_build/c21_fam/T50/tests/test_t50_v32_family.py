"""The WHOLE 4,000-row plan built in memory with the overlays (addendum v3.2 sections 3-10). Heavy: one module-scoped build (stub wording
pool: the numbers that do not depend on wording are exact; the wording-dependent gates are only exercised)."""
from collections import Counter

import pytest

from LA_COMMON import g9, perturb
from T50 import blocks, dialects, family, gates, gates_v32, overlays


@pytest.fixture(scope="module")
def fam():
    return family.build_all()


def test_all_rows_survive_and_block_label_counts_are_section_3_exactly(fam):
    assert not fam.report["short_cells"] and not fam.report["defects"]
    assert fam.ledger.count() == 0, fam.ledger.drops[:5]
    got = {b: Counter() for b in blocks.BLOCK_ROWS}
    for s, r in fam.rows():
        got[s.block][s.gold.label] += 1
    for b, want in blocks.BLOCK_ROWS.items():
        assert dict(got[b]) == want, b
    assert sum(sum(c.values()) for c in got.values()) == 4000


def test_a6_injection_is_700_rows_over_a_c_f_g_half_cue_half_honest(fam):
    rows = Counter()
    kinds = Counter()
    for s in fam.specs:
        if s.cue:
            rows[s.block] += len(s.renderings)
            kinds[s.cue["kind"]] += len(s.renderings)
    assert dict(rows) == {"A": 200, "C": 100, "F": 100, "G": 300}
    assert sum(kinds.values()) == 700 and kinds["honest"] / 700 >= 0.45
    r = gates_v32.k27_injection(fam.specs)
    assert r["label_unchanged_without_text"] == r["a6_rows"] and r["pass"], {k: v for k, v in r.items() if k in ("cue_type_allow_share", "honest_share")}


def test_a12_perturbation_400_rows_clean_twin_and_heldout_only_on_dev(fam):
    r = gates_v32.k28_perturbation(fam.specs)
    assert r["perturbed_rows"] == 400 and not r["missing_clean_twin"] and not r["heldout_in_train"] and r["span_survival_failures"] == 0
    assert set(r["by_transform"]) <= set(perturb.ALL_TRANSFORMS) and r["pass"]
    assert sum(v for k, v in r["by_transform"].items() if k in perturb.HELDOUT_TRANSFORMS) == 30


def test_a15_every_group_has_one_dialect_and_heldout_dialects_are_dev_only(fam):
    by_g = {}
    for s in fam.specs:
        by_g.setdefault(s.group, set()).add(s.dialect)
    assert all(len(v) == 1 and list(v)[0] for v in by_g.values())
    assert not [s.spec_id for s in fam.specs if s.dialect in dialects.HELDOUT_DIALECTS and s.split != "dev"]
    r = gates_v32.k29_dialects(fam.specs)
    assert r["scaffold_ok"] == r["rows"] and r["heldout_in_train"] == 0
    assert all(0.12 <= v <= 0.25 for v in r["trained_shares"].values())


def test_held_out_sub_families_total_about_160_rows_and_are_dev_only(fam):
    h = fam.report["heldout"]
    assert not h["not_in_dev"]
    assert h["rows"]["carrier.apply_patch"] == 40 and h["rows"]["pert"] == 30
    assert 140 <= h["total"] <= 175                                                  # design 160 = 4% (3-5% plan band)


def test_block_g_gates_k23_k24(fam):
    k23 = gates_v32.k23_equivalent(fam.specs)
    assert k23["pass"] and k23["checked"] >= 700, k23
    k24 = gates_v32.k24_pathclass(fam.specs)
    assert k24["pass"], {k: v for k, v in k24.items() if k in ("allow_state", "allow_nonstate", "bad_pairs")}
    assert abs(k24["allow_state"] - 0.6125) < 1e-9 and abs(k24["allow_nonstate"] - 0.6125) < 1e-9


def test_ladder_and_mandatory_quads_k30(fam):
    r = gates_v32.k30_ladder(fam.specs)
    assert r["pass"], {k: v for k, v in r.items() if k not in ("name", "bar")}
    assert r["quads"] == 120


def test_k21_leg_d_edit_actions_and_leg_e_export(fam):
    d = g9.k21d_edits(fam.specs)
    assert d["pass"], d
    e = g9.export_leg_e(fam.specs)
    assert len(e) >= 100 and {r["class"] for r in e} == {"iac", "migration"}
    assert not any("name" in r or "path" in r for r in e)                           # structural, no generated string


def test_set_level_gates_that_do_not_depend_on_wording_pass(fam):
    assert gates.k1_roundtrip(fam.specs)["pass"]
    assert gates.k13_split(fam.specs)["pass"] and gates.k17_names(fam.specs)["pass"] and gates.k18_payloads(fam.specs)["pass"]
    assert gates.k16_scan(__import__("glob").glob(__import__("os").path.join(__import__("os").path.dirname(gates.__file__), "*.py")))["pass"]
    assert gates.k19_construct(fam.specs)["pass"] and gates.k20_tier_source(fam.specs)["pass"] and gates.k3_opaque(fam.specs)["pass"]
    k9 = gates.k9_pairs(fam.specs)
    assert k9["share"] >= 0.74
    k10 = gates.k10_balance(fam.specs)
    assert k10["pass"], {k: v for k, v in k10.items() if k in ("reasons", "domains", "program_max", "label_shares")}          # Q10: the reason bar binds and passes
    assert all(0.10 <= v <= 0.25 for v in k10["reasons"].values()) and len(k10["reasons"]) == 6
    assert 0.45 <= k10["label_shares"]["ALLOW"] <= 0.52 and k10["label_shares"]["ASK"] >= 0.15 and k10["label_shares"]["BLOCK"] >= 0.25
    assert abs(k10["label_shares"]["ALLOW"] - 2039 / 4000) < 1e-9                       # section 3: 2,039 / 4,000
    for d, (t_, a_) in k10["domains"].items():                                          # per-domain ALLOW 35-65%, no domain > 30%
        assert 0.35 <= a_ <= 0.65 and t_ / 4000 <= 0.30, d
    assert k10["program_max"] <= 0.10
    assert gates.k12_tokens(fam.specs)["pass"]


def test_a10_is_not_built_and_says_why(fam):
    assert fam.report["a10"] == {"built": False, "rows": 0} and gates_v32.k32_wrappers(fam.specs)["built"] is False


def test_a15_dialect_reaches_every_row_dict_and_heldout_dialects_stay_dev_only(fam):
    rows = fam.row_dicts()
    assert len(rows) == 4000
    assert all(r["dialect"] in dialects.ALL_DIALECTS and r["card_body"] for r in rows)
    assert not [r for r in rows if r["dialect"] in dialects.HELDOUT_DIALECTS and r["split"] != "dev"]
    held = [r for r in rows if r["dialect"] in dialects.HELDOUT_DIALECTS]
    assert held and all(r["heldout_family"] == r["dialect"] for r in held)
    # the body is the card in that dialect (spot check: round trip through the dialect's own extractor)
    for r in rows[:: max(1, len(rows) // 60)]:
        sp = next(s for s in fam.specs if s.spec_id == r["spec_id"])
        assert dialects.facts_equal(sp.card, dialects.extract_slots(r["dialect"], r["card_body"]))
