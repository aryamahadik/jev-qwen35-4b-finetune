"""Item 10 (I10) in the mixer registry (FINAL_PLAN item 10, PREREG A47) and the plain-string meta.text_source of the
real-text blocks (GB, GW, MD, I10). In memory only. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_mix_c2_i10.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
import mix_c2 as m  # noqa: E402
from test_mix_c2_a42d import mk  # noqa: E402


def test_i10_is_a_registered_block_first_in_the_trim_order():
    assert c2io.BLOCK_TARGETS["I10"] == 5000 == c2io.BLOCK_CAPS["I10"] == m.BLOCK_CAPS["I10"]
    assert c2io.tier("I10") == "block" and "I10" in c2io.ALL_TARGETS and "I10" in m.TARGETS
    assert m.ITEM10_BLOCKS == ("I10",) and m.TRIM_ORDER[0] == "item10"
    assert "I10" in m.GENERAL_BLOCKS and "I10" in m.RULE_BLOCKS
    assert "I10" not in c2io.TARGETS                             # the generators iterate TARGETS: I10 is not generated


def rows_of(n_cards, per_card, doms=10):
    out = []
    for c in range(n_cards):
        for i in range(per_card):
            out.append(mk(f"i{c}_{i}", "I10", source="c2_i10", qtype="choice", gold="a", call_id=f"u{c}_{i}",
                          meta={"domain": f"d{c % doms}", "card_id": f"k{c}", "text_source": "c2_gblock"}))
    return out


def test_block_rules_i10_card_and_domain_and_size_caps():
    ok = rows_of(20, 50)
    rep, p = m.block_rules("I10", ok)
    assert p == [] and rep["max_rows_per_card"] == 50 and rep["max_domain_share"] <= 0.2 + 1e-9
    _, p = m.block_rules("I10", rows_of(10, 151))
    assert any("a card holds 151 rows > 150" in x for x in p)
    _, p = m.block_rules("I10", rows_of(5, 20, doms=2))
    assert any("domain" in x for x in p)
    _, p = m.block_rules("I10", rows_of(40, 130))
    assert any("rows > 5,000" in x for x in p)


def test_fit_block_i10_trims_by_whole_units_to_the_domain_cap_and_relabels_nothing():
    rows = rows_of(20, 50)
    for r in rows:
        if r["meta"]["card_id"] in ("k0", "k10", "k2", "k12", "k4", "k14"):
            r["meta"]["domain"] = "d0"                           # d0 would hold 30% of the block
    out, rels, info = m.fit_block("I10", rows, [])
    dc = Counter(m.dom_of(r) for r in out)
    assert max(dc.values()) <= 0.2 * len(out) + 1e-9 and len(out) < len(rows) and "unfixable" not in info
    byid = {r["id"]: r["gold"] for r in rows}
    assert all(byid[r["id"]] == r["gold"] for r in out)


def test_plain_string_text_source_does_not_crash_the_anchor_check():
    rows = rows_of(2, 3) + [mk("g1", "GB", source="c2_gblock", meta={"text_source": "c2_gblock", "domain": "x"}),
                            mk("m1", "MD", source="c2_md_x", meta={"text_source": "api.ror.org", "domain": "y"}),
                            mk("d1", "T28", source="s", meta={"text_source": {"dataset": "anchor_ds"}, "domain": "z"})]
    assert m.anchor_row_problems(rows, {"nothing"}) == []
    bad = m.anchor_row_problems(rows, {"anchor_ds"})
    assert bad and "anchor_ds" in bad[0] and "1" in bad[0]
