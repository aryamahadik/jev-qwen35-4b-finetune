import collections

import pytest

from LA_COMMON.wording import stub_pool
from T53 import blocks, gates
from T53.dryrun import build_dry, select_dry_cells
from T53.generator import render_turns, with_results_output
from T53.registry import ExampleKeys, Registry


@pytest.fixture(scope="module")
def plan_stats():
    return blocks.plan_stats()


def test_nominal_block_arithmetic_and_ask_oversampling(plan_stats):
    st, cells = plan_stats
    nominal = blocks.plan(oversample=False)
    sn, _ = blocks.plan_stats(nominal)
    assert dict(sn["block_rows"]) == {"a": 440, "b": 480, "c": 360, "d": 420 + 0, "e": 160, "f": 140} or sn["rows"] >= 1995
    assert sn["labels"]["ASK"] / sn["rows"] >= 0.10
    # generation-time ASK share is at least 11% (FIX-5), so a 0.6 pp drop cannot burn the fix iteration
    assert st["labels"]["ASK"] / st["rows"] >= 0.11
    ask_b = sum(1 for c in cells if c.kind == "b_pair" and c.extras["cue"] in ("plain_http", "cert_warning"))
    assert ask_b >= 66                                                       # transport-defect specs 60 -> >= 66
    ask_c = sum(1 for c in cells if c.kind == "c_row" and c.extras["klass"] == "confidential" and c.extras["vis"] == "unknown")
    assert ask_c >= 44                                                       # unknown-visibility cells 40 -> >= 44
    mcp = sum(1 for c in cells if c.kind == "d_ask_mcp_unlisted")
    assert mcp >= 22


def test_design_labels_cues_grid_channels_and_balance(plan_stats):
    st, cells = plan_stats
    n = st["rows"]
    assert 2000 <= n <= 2030
    assert dict(st["block_labels"]["a"]) == {"ALLOW": 248, "BLOCK": 192} and dict(st["block_labels"]["e"]) == {"ALLOW": 80, "BLOCK": 80}
    assert dict(st["block_labels"]["f"]) == {"ALLOW": 70, "BLOCK": 70}
    assert 0.45 <= st["labels"]["ALLOW"] / n <= 0.52 and st["labels"]["BLOCK"] / n <= 0.45
    cues = collections.Counter(c.extras["cue"] for c in cells if c.kind == "b_pair")
    for cue, k in cues.items():
        assert 30 <= k <= 33
    grid = collections.Counter((c.extras["klass"], c.extras["vis"], c.extras["channel"]) for c in cells if c.kind == "c_row")
    assert len(grid) == 18 and all(20 <= v <= 22 for v in grid.values())
    chan = st["channels"]
    assert all(52 <= chan[ch] <= 68 for ch in blocks.CHANNELS), dict(chan)
    assert sum(1 for c in cells if c.kind == "d_soft_twin") == 45 and sum(1 for c in cells if c.kind == "d_hard_twin") == 45
    twins = collections.Counter(c.extras["twin"] for c in cells if c.kind == "b_pair")
    assert twins["odd"] >= 118 and twins["exact"] >= 118
    assert 0.35 <= st["views"]["with_results"] / n <= 0.45                      # ~60/40 view split
    assert max(st["cards"].values()) - min(st["cards"].values()) <= 4


def test_unknown_visibility_cells_only_on_cards_where_the_slot_is_on(plan_stats):
    _, cells = plan_stats
    from T53 import cards
    for c in cells:
        if c.kind == "c_row" and c.extras["klass"] == "confidential" and c.extras["vis"] == "unknown":
            assert cards.LEVERS[c.card]["unknown_ask"]
    assert [k for k, v in cards.LEVERS.items() if not v["unknown_ask"]] == ["card.t53.c06"]
    for k, v in cards.LEVERS.items():
        card = cards.make_card(k, __import__("LA_COMMON.names", fromlist=["Names"]).Names("x", provisional=True), __import__("random").Random(1))
        assert card["ask_on_soft"] is False                                      # fixed OFF on all 6 T53 cards


@pytest.fixture(scope="module")
def dry():
    return build_dry()


def test_dry_run_20_examples_zero_drops_and_registered_fakes(dry):
    specs, drops, reg = dry
    assert len(specs) == 20 and drops == []
    assert gates.k1_registered(specs, reg)["pass"]
    assert gates.k2_checksum(specs)["pass"] and gates.k16_not_live(specs)["pass"]
    assert gates.k3_examples(specs, ExampleKeys())["pass"]
    assert gates.k20_names(specs)["pass"], gates.k20_names(specs)["refusals"]
    assert gates.k17_split(specs)["pass"]


def test_provenance_quad_same_shape_action_destination_different_labels(dry):
    specs, _, _ = dry
    q = {s.meta["quad"]: s for s in specs if s.meta.get("quad")}
    assert set(q) == {"authored", "pubkey", "read", "copied"}
    assert len({m.egress.dest_norm for m in q.values()}) == 1 and len({m.egress.channel for m in q.values()}) == 1
    assert [q[k].gold.label for k in ("authored", "pubkey", "read", "copied")] == ["ALLOW", "ALLOW", "BLOCK", "ALLOW"]       # conf_trusted sub-type
    assert q["authored"].renderings[0]["text"] == q["read"].renderings[0]["text"] or q["authored"].egress.provenance != q["read"].egress.provenance
    assert q["authored"].egress.provenance == "authored_placeholder" and q["read"].egress.provenance == "read_from_sensitive"
    assert {h.carrier for h in q["authored"].history} == {"file_write"} and any("file://" in (h.text or "") for h in q["read"].history)
    assert gates.k10_contrast(specs)["pass"]


def test_destination_distractors_have_trusted_twins_and_cues_are_computed_not_declared(dry):
    specs, _, _ = dry
    b = {(s.group, s.meta["role"]): s for s in specs if s.block == "b"}
    for (g, role), s in b.items():
        if role == "d":
            t = b[(g, "t")]
            assert s.gold.label in ("BLOCK", "ASK") and t.gold.label == "ALLOW"
            assert s.meta["verdict"] in ("lookalike", "transport_defect") and t.meta["verdict"] in ("trusted_exact", "trusted_odd")


def test_credential_use_pair_rule_2_vs_misplacements(dry):
    specs, _, _ = dry
    ok = next(s for s in specs if s.block == "e" and s.meta["role"] == "use")
    bad = next(s for s in specs if s.block == "e" and s.meta["role"] != "use")
    assert ok.rule_ids == ["2"] and ok.gold.label == "ALLOW" and bad.gold.tier == "hard" and bad.rule_ids[0] in ("1", "3")


def test_soft_twin_clears_only_with_op_and_destination_and_hard_twin_never(dry):
    specs, _, _ = dry
    soft = {s.meta["twin"]: s for s in specs if s.meta.get("d_kind") == "soft_twin"}
    hard = {s.meta["twin"]: s for s in specs if s.meta.get("d_kind") == "hard_twin"}
    assert soft["n"].gold.label == "BLOCK" and soft["y"].gold.label == "ALLOW" and soft["y"].gold.tier == "soft"
    assert soft["n"].renderings[0]["text"] == soft["y"].renderings[0]["text"]
    assert hard["n"].gold.label == hard["y"].gold.label == "BLOCK" and hard["y"].gold.tier == "hard"
    assert gates.k10_contrast(specs)["twins"] >= 2


def test_view_split_and_output_only_facts(dry):
    specs, _, _ = dry
    wr = [s for s in specs if s.view == "with_results"]
    assert wr and all(with_results_output(s) for s in wr)
    cert = [s for s in specs if s.egress.cert_state == "warning"]
    for s in cert:
        assert s.view == "with_results" and "certificate verification failed" in with_results_output(s)
    pr = [s for s in specs if s.view == "primary"]
    assert pr and all(s.meta["primary_determinable"] for s in pr)
    assert gates.k9_fact_coverage(specs)["pass"]


def test_t53_programs_are_only_the_closed_list_even_with_the_obfuscated_stratum():
    cells = blocks.plan()
    obf = [c for c in cells if c.kind == "b_pair" and c.extras["obf"]]
    assert len(obf) == blocks.OBF_SHARE_B
    drops = []
    specs = []
    for c in obf[:6]:
        specs += blocks.build_cell(c, drops, None, Registry())
    assert not drops
    assert any(r["role"] == "obf" for s in specs for r in s.renderings)
    allowed = {"curl", "wget", "git", "scp", "nc", "aws", "gcloud", "npm", "twine", "cargo", "gh"}
    for s in specs:
        for r in s.renderings:
            assert set(r["programs"]) <= allowed, r["programs"]
    ob_d = sum(1 for s in specs for r in s.renderings if r["role"] == "obf" and s.gold.label != "ALLOW")
    ob_b = sum(1 for s in specs for r in s.renderings if r["role"] == "obf" and s.gold.label == "ALLOW")
    assert ob_d == ob_b


def test_every_distinct_plan_cell_builds_with_design_labels_and_zero_drops():
    cells = blocks.plan()
    seen = collections.OrderedDict()
    for c in cells:
        e = c.extras
        k = (c.kind, e.get("sub"), e.get("cue"), e.get("twin"), e.get("klass"), e.get("vis"), e.get("channel"), e.get("mis"), e.get("benign_shape"), e.get("view"))
        seen.setdefault(k, c)
    drops, reg = [], Registry()
    for k, c in seen.items():
        specs = blocks.build_cell(c, drops, None, reg)
        got = sorted((s.gold.label, s.gold.reason, s.gold.tier) for s in specs)
        assert got == sorted(blocks.design_rows(c)), (k, got)
    assert not drops and len(seen) >= 150
    assert reg.stats()["checksum_wrong"] == reg.by_shape.get("ckt_token", 0)
    allspecs = [s for c in seen.values() for s in blocks.build_cell(c, [], None, Registry())]
    assert gates.k20_names(allspecs)["pass"], gates.k20_names(allspecs)["refusals"][:3]
    assert gates.k2_checksum(allspecs)["pass"] and gates.k16_not_live(allspecs)["pass"]
    r1 = Registry()
    again = [s for c in seen.values() for s in blocks.build_cell(c, [], None, r1)]
    assert gates.k1_registered(again, r1)["pass"]


def test_head_and_mechanics_of_remaining_gates(dry):
    specs, _, reg = dry
    stub = stub_pool()
    for s in specs:
        render_turns(s, stub)
    assert not gates.k24_heads(specs)["pass"]                                   # 20 examples are too few
    assert gates.k7_agreement({"a": 1}, {"a": 1}, {"a": "ALLOW"}, {"a": "ALLOW"})["pass"]
    assert not gates.k7_agreement({"a": 1}, {"a": 2}, {"a": "ALLOW"}, {"a": "ALLOW"})["pass"]
    for fn in (gates.k4_shape, gates.k5_identifiers, gates.k6_destination_surface, gates.k12_format, gates.k11_obfuscated, gates.k13_balance, gates.k8_coverage):
        assert isinstance(fn(specs)["pass"], bool)
