"""Regression: apply_targets / fit_block_in_mix measure a general block's caps against THAT block's rows only (a dry run
emptied GW / I10 because fit_block saw every new row of the mix). In memory only. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_mix_c2_fitblock.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mix_c2 as m  # noqa: E402
from test_mix_c2_a42d import mk  # noqa: E402


def block_rows(block, n, doms=10, per_card=50, source=None):
    return [mk(f"{block}_{i}", block, source=source or f"c2_{block.lower()}", qtype="choice", gold="a",
               meta={"domain": f"d{(i // per_card) % doms}", "card_id": f"{block}k{i // per_card}"})
            for i in range(n)]


def mix(sizes):
    rows = []
    for b, n in sizes.items():
        rows += block_rows(b, n)
    return rows


def counts(rows):
    return dict(Counter(r["_block"] for r in rows))


def test_multi_block_mix_each_below_its_own_cap_loses_nothing():
    sizes = {"GB": 14000, "GW": 9000, "I10": 4800, "T1": 3000}
    assert sizes["GB"] + sizes["GW"] + sizes["I10"] > max(m.BLOCK_CAPS[b] for b in m.GENERAL_BLOCKS)
    assert all(sizes[b] <= m.BLOCK_CAPS[b] for b in m.GENERAL_BLOCKS)
    rows = mix(sizes)
    out, rels, info = m.apply_targets(rows, [], dict(sizes), {})
    assert counts(out) == sizes and [r["id"] for r in out] == [r["id"] for r in rows]
    for b in m.GENERAL_BLOCKS:
        assert "unfixable" not in info[b]["fit"] and info[b]["fit"]["steps"] == []
        assert info[b]["fit"]["before"] == info[b]["fit"]["after"] == sizes[b]


def test_block_over_its_own_cap_is_trimmed_exactly_as_fit_block_on_that_block_alone():
    sizes = {"GB": 14000, "GW": 9000, "I10": 5600, "T1": 3000}
    rows = mix(sizes)
    alone, _, ai = m.fit_block("I10", [r for r in rows if r["_block"] == "I10"], [])
    assert len(alone) <= m.BLOCK_CAPS["I10"] and ai["steps"][0]["rule"] == "size"
    out, rels, info = m.apply_targets(rows, [], dict(sizes), {})
    assert {r["id"] for r in out if r["_block"] == "I10"} == {r["id"] for r in alone}
    c = counts(out)
    assert c["GB"] == 14000 and c["GW"] == 9000 and c["T1"] == 3000 and c["I10"] == len(alone)
    assert info["I10"]["fit"]["steps"] == ai["steps"] and info["I10"]["fit"]["before"] == 5600


def test_gw_over_cap_trimmed_to_its_cap_while_others_untouched_and_relations_kept():
    sizes = {"GB": 14000, "GW": 9600, "I10": 4800}
    rows = mix(sizes)
    pairs = [(f"GW_{i}", f"GW_{i + 1}") for i in range(0, 9600, 2)]          # whole units of two rows
    rels = [{"a": a, "b": b} for a, b in pairs] + [{"a": "GB_0", "b": "GB_1"}, {"a": "I10_0", "b": "I10_1"}]
    out, orels, info = m.apply_targets(rows, rels, dict(sizes), {})
    c = counts(out)
    assert c["GB"] == 14000 and c["I10"] == 4800 and m.BLOCK_CAPS["GW"] - 2 <= c["GW"] <= m.BLOCK_CAPS["GW"]
    kept = {r["id"] for r in out}
    assert all(x["a"] in kept and x["b"] in kept for x in orels)                  # no dangling relation
    assert {"a": "GB_0", "b": "GB_1"} in orels and {"a": "I10_0", "b": "I10_1"} in orels
    gw = {r["id"] for r in out if r["_block"] == "GW"}
    assert all((a in gw) == (b in gw) for a, b in pairs)                            # whole units only


def test_fit_block_in_mix_leaves_other_blocks_in_place_and_order():
    rows = mix({"GW": 9600, "GB": 100, "I10": 100})
    out, _, info = m.fit_block_in_mix("GW", rows, [])
    assert counts(out)["GB"] == 100 and counts(out)["I10"] == 100 and counts(out)["GW"] <= m.BLOCK_CAPS["GW"]
    other = lambda xs: [r["id"] for r in xs if r["_block"] != "GW"]
    assert other(out) == other(rows) and info["before"] == 9600
