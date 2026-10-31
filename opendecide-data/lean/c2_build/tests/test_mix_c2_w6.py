"""W6 task B tests: GW registration, A49 (c) checks, GB mixdev never-train, GB twin yes-share rebalance, g13 block list."""
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import a49c  # noqa: E402
import c2io  # noqa: E402
import mix_c2 as m  # noqa: E402
from negtwins import block_twins as BT  # noqa: E402


def yn(i, gold, block="TX", **meta):
    return {"id": f"{block}:{i}", "call_id": f"{block}:{i}", "qtype": "noul", "gold": gold, "options": None, "_block": block,
            "meta": {"twin_kind": None, **meta}}


def ch(i, k, gold_idx, block="TX", opts=None, call=None):
    o = opts or [f"opt{j}" + "x" * j for j in range(k)]
    return {"id": f"{block}:c{i}", "call_id": call or f"{block}:c{i}", "qtype": "choice", "gold": o[gold_idx], "options": o,
            "_block": block, "meta": {"twin_kind": None}}


def test_gw_registered():
    assert c2io.ALL_TARGETS["GW"] == 9200 and m.BLOCK_CAPS["GW"] == 9200 and "GW" in m.TARGETS
    assert c2io.tier("GW") == "block" and "GW" in m.GENERAL_BLOCKS
    from g13_c2 import default_blocks
    assert {"GB", "GW", "MD", "RTW", "T40", "T45"} <= set(default_blocks("candidates"))


def test_gw_block_rules():
    rows = [{"id": f"x{i}", "_block": "GW", "qtype": "noul", "gold": i % 2, "source": "c2_wave2", "domain": f"W{i % 5}",
             "meta": {"domain": f"W{i % 5}"}} for i in range(3000)]
    rep, p = m.block_rules("GW", rows)
    assert not p and rep["max_rows_per_type"] == 600
    rows += [dict(rows[0], id=f"y{i}", domain="W0", meta={"domain": "W0"}) for i in range(700)]       # W0 > 1,200 and > 20%
    _, p = m.block_rules("GW", rows)
    assert any("wave-2 type" in x for x in p) and any("domain" in x for x in p)


def test_a49c_yes_rate_share_and_cells():
    good = [yn(i, i % 2) for i in range(100)] + [ch(i, 3, i % 3) for i in range(100)]
    ck = a49c.family_checks("TX", good, [], {r["id"]: 100 for r in good})
    assert not a49c.failing(ck) or a49c.failing(ck) == ["twin_share"] or set(a49c.failing(ck)) <= {"twin_share", "equiv_share", "complement_share_of_yes_no"}
    assert ck["yes_no_share"]["verdict"] == "pass" and ck["yes_rate"]["verdict"] == "pass"
    bad = [yn(i, 1 if i % 10 else 0) for i in range(100)] + [ch(i, 3, 0) for i in range(100)]
    ck = a49c.family_checks("TX", bad, [], {r["id"]: 900 for r in bad})
    assert {"yes_rate", "gold_position_cells", "token_mean"} <= set(a49c.failing(ck))


def test_a49c_position_counts_one_per_cell():
    # 90 partner rows share 30 cells (3 rows each, same gold position 0): per-cell counting sees 30 cells, not 90 rows
    rows = [ch(i, 3, 0, call=f"u{i // 3}") for i in range(90)]
    ck = a49c.family_checks("TX", rows, [])
    assert ck["gold_position_cells"]["value"]["cells"]["3"] == 30


def test_a49c_abstain_and_longest():
    rows = [ch(i, 3, 0, opts=["a", "bb", "none of these"]) for i in range(40)]            # gold is shortest, abstain never gold
    ck = a49c.family_checks("TX", rows, [])
    assert ck["abstain_wrong_share"]["verdict"] == "pass" and ck["abstain_wrong_share"]["value"] == 1.0
    rows = [ch(i, 3, 0, opts=["a", "bb", "none of these"]) for i in range(20)] + \
           [ch(i + 100, 3, 2, opts=["a", "bb", "none of these"]) for i in range(40)]      # abstain gold on 2/3
    assert a49c.family_checks("TX", rows, [])["abstain_wrong_share"]["verdict"] == "fail"


def test_a49c_assert_scope():
    rows = [yn(i, i % 2, block="GB") for i in range(60)] + [yn(i, 1, block="T28") for i in range(60)]
    rep, probs = m.a49c_assert(rows, [], {})
    assert rep["GB"]["binding"] is False and rep["T28"]["binding"] is True
    assert any("T28" in x and "yes_rate" in x for x in probs) and not any(" GB:" in x for x in probs)


def test_swap_balance_keeps_bins_and_sizes():
    rows, units, bins = [], [], {}
    for u in range(200):
        gold = 1 if u < 120 else 0                        # 60% yes units
        r = yn(u, gold)
        rows.append(r)
        units.append([u])
        bins[r["id"]] = "medium"
    sel = list(range(0, 100)) + []                        # selected: all yes -> rate 1.0
    new, info = a49c.swap_balance('TX', rows, units, sel, bins, 20261013)
    y = sum(rows[u]["gold"] for u in new) / len(new)
    assert len(new) == len(set(new)) == 100 and abs(y - 0.5) <= 0.0200001 and info["swaps"] > 0


def test_mixdev_id_never_train():
    rep = {}
    rows = [{"id": "a"}, {"id": "b"}]
    assert m.mixdev_id_problems(rows, {"GB": {"z"}}, rep) == []
    p = m.mixdev_id_problems(rows, {"GB": {"b", "z"}}, rep)
    assert p and rep["block_mixdev_never_train"]["training_rows_hit"] == {"GB": 1}


def test_dev_items_reads_block_mixdev(tmp_path):
    class L:
        def jsonl(self, p):
            return [{"id": "gb_dev", "group_id": "g_dev", "state": "some state", "meta": {}}]
    out, _ = m.dev_items(L(), ["GB"], dev_sets={})
    assert [r["id"] for r, _ in out["GB"]] == ["gb_dev"]


def test_rebalance_cards_removes_fewest_twins():
    base = [{"id": f"b{i}", "qtype": "noul", "gold": 1 if i < 21 else 0, "meta": {"card_id": "c"}} for i in range(52)]
    tw = [{"id": f"t{i}", "qtype": "noul", "gold": 0, "meta": {"card_id": "c", "twin_of": f"b{i}"}} for i in range(5)]
    kept, rep = BT.rebalance_cards(base, tw)
    yes = 21 / (52 + len(kept))
    assert yes >= 0.40 - 1e-9 and 21 / (52 + len(kept) + 1) < 0.40 - 1e-9 and rep["cards_adjusted"]["c"]["twins_removed"] == 5 - len(kept)
    again, _ = BT.rebalance_cards(base, tw)
    assert [t["id"] for t in again] == [t["id"] for t in kept]                       # seeded, repeatable
    assert all(b["gold"] in (0, 1) for b in base) and sum(b["gold"] for b in base) == 21   # base rows untouched
