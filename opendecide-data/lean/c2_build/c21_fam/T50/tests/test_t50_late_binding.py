"""LATE-BINDING rows (addendum v3.2 section 6, lever A5). T50/intents_late.py, T50/gates_alias.py (K26)."""
from LA_COMMON.expander import roundtrip_equal
from LA_COMMON.render import render_plain
from LA_COMMON.shellmodel import RawScript
from LA_COMMON.spec import Gold, Spec

from T50.build import BCtx
from T50.cards import CARD_IDS
from T50.gates_alias import k26_late, k26_late_fixtures
from T50.intents import REGISTRY, build_intent, expected_for
from T50.intents_late import (LATE_VARIANTS, LATE_A_PLAN, LATE_A_SPLIT, LATE_CONSTRUCTS, LATE_D_OPAQUE, LATE_D_OPAQUE_CONSTRUCT,
                              LATE_D_WTR_PLAN, LATE_D_WTR_SPLIT, LATE_FIXTURES, LATE_TABLE)
from T50.solver_a import label_spec


def _spec_of(built, card):
    sp = Spec(spec_id="x", family="T50", block="A", card_ref=card["card_id"], card=card, state=built.c.st,
              naming=built.c.naming, history=list(built.c.hist), action=built.script, payloads=dict(built.c.payloads),
              payload_kind=built.payload_kind, intent=built.intent, meta=dict(built.c.meta))
    res = label_spec(sp)
    sp.gold = Gold(res.label, res.reason, res.tier)
    return sp, res


# ------------------------------------------------------------------------------------------------ registry: every id, every card
def test_every_late_intent_builds_on_every_card_with_correct_label_and_roundtrip():
    ids = [i for i in REGISTRY if i.startswith("late.")]
    assert len(ids) == len(LATE_CONSTRUCTS) * (6 + 2 * len(LATE_VARIANTS)) + 1          # 4 constructs x ((3 + 3) + Q10 variants blockw / askp, direct and wtr) + 1 opaque
    for iid in ids:
        meta = REGISTRY[iid]
        for cid in CARD_IDS:
            for seed in range(2):
                c = BCtx("t-%s-%s-%d" % (iid, cid, seed), cid, seed_tag="t%d" % seed)
                built = build_intent(iid, c, {})
                sp, res = _spec_of(built, c.card)
                assert (res.label, res.reason, res.tier) == expected_for(meta, c.card), (iid, cid)
                if isinstance(built.script, RawScript):
                    assert res.label == "ASK" and res.reason == "none" and res.tier == "na"
                    continue
                if ".wtr_" in iid:
                    expect = c.payloads.get("payload.late_wtr")
                    known = {p: c.meta["late_text"] for p in c.st.session.written_files}
                    ok, why = roundtrip_equal(expect, render_plain(built.script).text, known)
                else:
                    ok, why = roundtrip_equal(built.script, c.meta["late_text"], {})
                assert ok, (iid, cid, why, c.meta.get("late_text"))


# ------------------------------------------------------------------------------------------------ constants (DONE WHEN)
def test_late_plan_tables_are_internally_consistent():
    assert sum(LATE_A_PLAN.values()) == 60 and LATE_A_PLAN == {"ALLOW": 30, "ASK": 10, "BLOCK": 20}
    assert sum(sum(v) for v in LATE_A_SPLIT.values()) == 60
    assert LATE_D_OPAQUE == 35 and LATE_D_OPAQUE_CONSTRUCT in LATE_CONSTRUCTS
    assert LATE_D_OPAQUE / 110 <= 0.35                        # K3 cap: <= 35% of the 110 opaque rows
    assert sum(LATE_D_WTR_PLAN.values()) == 55 and LATE_D_WTR_PLAN == {"ALLOW": 22, "ASK": 6, "BLOCK": 27}
    assert sum(sum(v) for v in LATE_D_WTR_SPLIT.values()) == 55
    assert len(LATE_TABLE.sha) == 64


# ------------------------------------------------------------------------------------------------ K26 fixtures + gate
def test_late_fixtures_pass_100pct_per_construct():
    ok, per_construct = k26_late_fixtures()
    assert ok, per_construct
    assert set(per_construct) == set(LATE_CONSTRUCTS)
    for construct, info in per_construct.items():
        assert info["pass"] and info["n"] >= 1, (construct, info)


def test_k26_late_gate_passes():
    r = k26_late()
    assert r["pass"], {k: v for k, v in r.items() if k != "fixtures_per_construct"}
    assert r["opaque_all_ask"] is True
    assert r["resolvable_share"] >= 0.40 and r["ask_share"] <= 0.60
