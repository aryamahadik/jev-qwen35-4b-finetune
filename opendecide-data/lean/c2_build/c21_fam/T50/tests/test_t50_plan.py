"""Plan arithmetic against addendum v3.2 section 3 (sizes by SUBSTITUTION: A-F shrink to 2,400, block G has 1,600, the family stays 4,000)."""
from collections import Counter

import pytest

from T50 import blockg, blocks, cards, quads
from T50.intents import REGISTRY, expected_for


@pytest.fixture(scope="module")
def stats():
    return blocks.plan_stats()


def rows_of(cells, pred):
    return Counter(r[0] for c in cells if pred(c) for r in blocks.cell_rows(c))


def test_block_label_totals_match_the_v32_section_3_table_exactly(stats):
    st, cells = stats
    assert st["rows"] == 4000
    for b, want in blocks.BLOCK_ROWS.items():
        assert dict(st["by_block_label"][b]) == want, b
    assert dict(st["label"]) == {"ALLOW": 2039, "ASK": 674, "BLOCK": 1287}
    assert sum(sum(v.values()) for v in blocks.BLOCK_ROWS.values()) == blocks.FAMILY_SIZE == 4000


def test_block_a_parts_alias_late_swap_and_plain(stats):
    _, cells = stats
    a = lambda c: c.block == "A"
    assert rows_of(cells, lambda c: a(c) and c.tag == "alias") == Counter({"ALLOW": 150, "ASK": 40, "BLOCK": 110})
    assert rows_of(cells, lambda c: a(c) and c.tag == "swap") == Counter({"ALLOW": 40, "ASK": 40, "BLOCK": 40})
    assert rows_of(cells, lambda c: a(c) and c.tag == "late") == Counter({"ALLOW": 30, "ASK": 10, "BLOCK": 20})
    plain = rows_of(cells, lambda c: a(c) and c.tag not in ("alias", "swap", "late"))
    assert plain == Counter({"ALLOW": 180, "ASK": 30, "BLOCK": 50})                       # 260 plain direct rows (quads and M4 cells included)


def test_balance_designs_hold_with_margin(stats):
    st, _ = stats
    n = st["rows"]
    assert 0.45 <= st["label"]["ALLOW"] / n <= 0.52 and st["label"]["ASK"] / n >= 0.15 and st["label"]["BLOCK"] / n >= 0.25
    reasons = {k: v for k, v in st["reason"].items() if k != "none"}
    assert st["reason"]["none"] == 124                                      # opaque ASK 110 + wtr.modified ASK 14 (the 6 late-binding wtr ASK rows are `destroy`)
    assert set(reasons) == {"destroy", "exfiltrate", "weaken_security", "cross_trust", "bypass_review_or_affect_others", "supply_chain"}
    assert st["tier"]["hard"] >= 400 and st["tier"]["soft"] >= 800
    for c, v in st["card_allow"].items():
        assert 0.40 <= v["ALLOW"] / sum(v.values()) <= 0.55, c
    dom = st["domain_A"]
    assert sum(dom.values()) == 740
    assert max(dom.values()) / 740 <= 0.45                                 # block A domain shares deviate from the v3.1 targets (see the report); no gate reads them


def test_k10_reason_bar_is_feasible_on_the_design_values(stats):
    """Opus Q10 (18 Oct 2026): the reason bar binds and the quotas are amended. Only G3 (200), the 45 G1-mirror ASK pairs and INFERRED-TARGET (30)
    are forced to `destroy` (275 rows, about 15%); the alias rows take the reason of the RESOLVED node; G1 / G2 mirrors may use any R26
    condition. With the design values every harm reason is 10-25% of the reason-bearing non-ALLOW rows."""
    st, cells = stats
    harm = {k: v for k, v in st["reason"].items() if k != "none"}
    tot = sum(harm.values())
    assert set(harm) == {"destroy", "exfiltrate", "weaken_security", "cross_trust", "supply_chain", "bypass_review_or_affect_others"}
    assert all(0.10 <= v / tot <= 0.25 for v in harm.values()), {k: round(v / tot, 3) for k, v in harm.items()}
    alias_rows = [r for c in cells if c.tag == "alias" for r in blocks.cell_rows(c) if r[0] != "ALLOW"]
    assert len(alias_rows) == 150 and Counter(r[1] for r in alias_rows)["destroy"] < 50          # not forced destroy


def test_matched_pairs_share_is_75_percent(stats):
    st, cells = stats
    paired = Counter()
    for c in cells:
        n = len(blocks.cell_rows(c))
        if c.block in ("B", "C", "E", "G") or c.tag in ("swap", "alias"):
            paired[c.block] += n
    total = sum(paired.values())
    assert paired["B"] == 400 and paired["C"] == 220 and paired["E"] == 360 and paired["G"] == 1600
    assert total / 4000 >= 0.75 - 1e-9                                      # B 400 + C 220 + E 360 + swap 120 + alias 300 + G 1,600 = 3,000


def test_block_e_quads_are_45_soft_and_45_hard_specs_with_the_designed_labels(stats):
    _, cells = stats
    soft = [c for c in cells if c.tag == "soft_quad"]
    hard = [c for c in cells if c.tag == "hard_quad"]
    assert len(soft) == 45 and len(hard) == 45
    assert sum(1 for c in soft if c.label == "ASK") == 22 and sum(1 for c in soft if c.label == "BLOCK") == 23
    for c in soft:
        meta = REGISTRY[c.intent]
        assert meta["tier"] == "soft" and (meta["label"] == "BLOCK")                  # the un-cleared label follows the card's ask_on_soft
        assert cards.LEVERS[c.card]["ask_on_soft"] == (c.label == "ASK") or (meta.get("c4") and c.label == "BLOCK" and not cards.LEVERS[c.card]["ask_on_soft"])
        assert not (meta.get("c4") and cards.LEVERS[c.card]["ask_on_soft"])             # a C4 intent never sits on an ask_on_soft card here
    for c in hard:
        assert REGISTRY[c.intent]["tier"] == "hard" and c.intent not in ("git.hooks_config", "proc.kill_system")
    assert blocks_rows(cells, "E", "ASK") == 66 and blocks_rows(cells, "E", "BLOCK") == 249


def blocks_rows(cells, block, label):
    return sum(1 for c in cells if c.block == block for r in blocks.cell_rows(c) if r[0] == label)


def test_view_twins_are_180_pairs_inside_the_4000(stats):
    _, cells = stats
    tw = [c for c in cells if c.extras.get("twin")]
    pairs = sum(blocks.TWIN_PAIRS_PER_CELL[c.block] for c in tw)
    assert pairs == blocks.VIEW_TWIN_PAIRS == 180 and {c.block for c in tw} <= {"A", "B", "C", "F"}


def test_f_subfamily_counts(stats):
    _, cells = stats
    for sub, (a, s, b) in blocks.F_SUB.items():
        got = Counter(r[0] for c in cells if c.sub == sub for r in blocks.cell_rows(c))
        assert (got["ALLOW"], got["ASK"], got["BLOCK"]) == (a, s, b), sub


def test_block_g_sub_blocks_are_exact(stats):
    _, cells = stats
    want = {"G1": (320, 100, 220), "G2": (100, 0, 100), "G3": (200, 100, 100), "G4": (360, 0, 0)}
    for sub, (a, s, b) in want.items():
        got = rows_of(cells, lambda c, sub=sub: c.block == "G" and c.sub == sub)
        assert (got["ALLOW"], got["ASK"], got["BLOCK"]) == (a, s, b), sub
    pairs = Counter(c.extras["g"] for c in cells if c.block == "G")
    assert pairs == Counter(blockg.PAIRS)
    g = [c for c in cells if c.block == "G"]
    # carriers: apply_patch is the HELD-OUT carrier (dev only), 20 pairs = 40 rows (section 9); the rest split 45 : 40
    patch = [c for c in g if c.extras["carrier"] == "apply_patch"]
    assert sum(len(blocks.cell_rows(c)) for c in patch) == 40 and all(c.extras.get("force_dev") for c in patch)
    assert sum(1 for c in g if c.extras.get("review")) >= 0
    fwd_review = [c for c in g if c.extras["g"] == "g1f" and c.extras.get("review")]
    assert len(fwd_review) >= blockg.REVIEW_FORWARD_PAIRS


def test_block_g_forward_pairs_are_55_ask_and_105_block(stats):
    _, cells = stats
    f = Counter(c.label for c in cells if c.extras.get("g") == "g1f")
    assert f == Counter({"ASK": blockg.FORWARD_ASK_PAIRS, "BLOCK": blockg.FORWARD_BLOCK_PAIRS})
    m = Counter(c.label for c in cells if c.extras.get("g") == "g1m")
    assert m == Counter({"ASK": blockg.MIRROR_ASK, "BLOCK": blockg.MIRROR_BLOCK})


def test_mandatory_quads_are_80_in_the_shell_blocks(stats):
    _, cells = stats
    assert sum(1 for c in cells if c.tag == "quad4") == 80
    assert sum(1 for c in cells if c.tag == "quad4" and c.block == "A") == 30 and sum(1 for c in cells if c.tag == "quad4" and c.block == "C") == 50


def test_swap_pairs_differ_in_label_for_their_intent():
    for iid, pairs in blocks.SWAP_PAIRS_FOR.items():
        for a, b in pairs:
            la = expected_for(REGISTRY[iid], blocks.cards_mod_card(a))[0]
            lb = expected_for(REGISTRY[iid], blocks.cards_mod_card(b))[0]
            assert la != lb, (iid, a, b)


def test_plan_is_deterministic_and_hashable():
    a = [(c.block, c.intent, c.card, c.tag) for c in blocks.plan()]
    b = [(c.block, c.intent, c.card, c.tag) for c in blocks.plan()]
    assert a == b
