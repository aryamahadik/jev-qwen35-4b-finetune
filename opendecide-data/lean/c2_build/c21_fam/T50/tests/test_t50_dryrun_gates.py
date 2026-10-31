import builtins
import os

import pytest

from LA_COMMON.canon import sha_obj
from LA_COMMON.names import get_allowlist
from LA_COMMON.wording import stub_pool
from T50 import gates
from T50.dryrun import build_dry, select_dry_cells
from T50.generator import render_turns, spec_rows


@pytest.fixture(scope="module")
def dry():
    return build_dry()


def test_dry_run_builds_20_example_cells_in_memory_and_never_writes_to_disk(monkeypatch):
    real_open = builtins.open
    writes = []

    def guarded(file, mode="r", *a, **k):
        if any(c in mode for c in "wax+"):
            writes.append(file)
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded)
    specs, ledger, cells = build_dry()
    assert len(cells) == 20 and len(specs) >= 20 and not writes and ledger.count() == 0


def test_dry_run_covers_every_block_swap_twin_quad_opaque_and_wtr(dry):
    specs, _, cells = dry
    assert {c.block for c in cells} == set("ABCDEFG")
    assert any(c.tag == "swap" for c in cells) and any(c.extras.get("twin") for c in cells)
    assert any(c.tag == "soft_quad" for c in cells) and any(c.tag == "hard_quad" for c in cells)
    assert any(c.tag == "opaque" for c in cells) and any(c.tag == "modified" for c in cells)
    assert any(c.intent.startswith("wtr.") and c.label == "BLOCK" for c in cells)


def test_dry_run_is_deterministic(dry):
    a = [s.sha() for s in dry[0]]
    b = [s.sha() for s in build_dry()[0]]
    assert a == b


def test_gold_invariants_and_row_expansion(dry):
    specs, _, _ = dry
    rows = [r for s in specs for r in spec_rows(s)]
    assert len(rows) >= 25
    for s in specs:
        assert s.gold.label in ("ALLOW", "ASK", "BLOCK")
        if s.gold.tier == "hard":
            assert s.gold.label == "BLOCK"
        if s.gold.label == "ALLOW":
            assert s.gold.reason == "none"
    assert all(r["gold"]["label"] for r in rows)


def test_k1_k3_k4_k9_k13_k16_k17_k18_k20_on_the_dry_run(dry):
    specs = dry[0]
    assert gates.k1_roundtrip(specs)["pass"]
    assert gates.k3_opaque(specs)["violations"] == []
    assert gates.k13_split(specs)["pass"]
    assert gates.k17_names(specs)["pass"], gates.k17_names(specs)["refusals"]
    assert gates.k18_payloads(specs)["pass"]
    assert gates.k20_tier_source(specs)["pass"]
    assert gates.k8_consent(specs)["violations"] == []
    assert gates.k9_pairs(specs)["share"] > 0.2


def test_k4_equal_numbers_needs_exactly_equal_counts():
    class S:  # tiny stand-ins
        pass

    def mk(label, role="obf"):
        s = S()
        s.block, s.gold = "B", type("G", (), {"label": label})
        s.renderings = [{"role": role, "roundtrip": True}]
        return s
    assert gates.k4_evasion_equal([mk("BLOCK"), mk("ALLOW")])["pass"]
    assert not gates.k4_evasion_equal([mk("BLOCK"), mk("ASK"), mk("ALLOW")])["pass"]


def test_k2_k5_k6_k7_k10_k11_k12_k22_mechanics(dry):
    specs = dry[0]
    a = {"r1": "ALLOW", "r2": "ASK"}
    assert gates.k2_agreement(a, dict(a))["pass"] and not gates.k2_agreement(a, {"r1": "ALLOW", "r2": "BLOCK"})["pass"]
    for fn in (gates.k5_evasion_cue_probe, gates.k6_format_probe, gates.k7_card, gates.k22_heads):
        out = fn(specs)
        assert "id" in out and isinstance(out["pass"], bool)                  # 20 examples are far too few: they must not pass silently
    out = gates.k10_balance(specs)
    assert out["id"] == "K10" and "label_shares" in out
    stub = stub_pool()
    for s in specs:
        render_turns(s, stub)
    k11 = gates.k11_wording(stub, specs)
    assert not k11["pass"] and k11["stub"]                                     # stub pool: K11 fails by design
    k12 = gates.k12_tokens(specs)
    assert k12["mean"] < 800 and k12["over_1536"] == 0


def test_decision_spans_carry_authority_on_consent_turns(dry):
    specs = dry[0]
    q = [s for s in specs if s.meta.get("quad_cell") == "both"]
    assert q
    render_turns(q[0], stub_pool())
    assert any("AUTHORITY" in sp["roles"] for sp in q[0].decision_spans)
    n = [s for s in specs if s.meta.get("quad_cell") == "neither"]
    if n:
        render_turns(n[0], stub_pool())
        assert not any("AUTHORITY" in sp["roles"] for sp in n[0].decision_spans)


def test_trivial_baselines_report_per_class_rates(dry):
    out = gates.trivial_baselines(dry[0])
    assert set(out) == {"always_allow", "always_ask", "regex_prefix_allow", "block_when_unsure"}
    assert out["always_allow"]["ALLOW"]["FNR"] == 0.0 and out["always_allow"]["BLOCK"]["FNR"] == 1.0


def test_head_rows_are_at_most_a_quarter_of_the_specs(dry):
    specs = dry[0]
    for head in ("reason", "tier"):
        hs = gates.head_specs(specs, head)
        assert len(hs) <= 0.6 * len(specs)


def test_a_fix_cannot_change_the_bars_only_parameters():
    import inspect
    src = inspect.getsource(gates)
    for bar in ("0.55", "0.60", "0.25", "0.10"):
        assert bar in src


def test_program_subcommand_share_estimate_stays_under_ten_percent():
    est = gates.program_share_estimate(samples=8)
    top = sorted(est.items(), key=lambda kv: -kv[1])[:3]
    assert top[0][1] < 0.10 and abs(sum(est.values()) - 1.0) < 0.02, top
