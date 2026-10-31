"""ALIAS / PROTECTED-ROOT REACHABILITY rows (addendum v3.2 section 5, lever A4). T50/intents_alias.py,
T50/gates_alias.py (K25)."""
from collections import Counter

from LA_COMMON.expander import roundtrip_equal
from LA_COMMON.render import render_plain
from LA_COMMON.spec import Gold, Spec

from T50.build import BCtx
from T50.cards import CARD_IDS
from T50.gates_alias import build_alias_specs, k25_alias
from T50.intents import REGISTRY, build_intent, expected_for
from T50.intents_alias import (_NET_FORMS, ALIAS_DOMAIN_SPLIT, ALIAS_FORMS, ALIAS_PAIR_PLAN, ALIAS_SEVERITY_SPLIT, ALIAS_TABLE,
                               build_all_alias_pairs, build_alias_pair)
from T50.solver_a import label_spec


def _spec_of(built, card):
    sp = Spec(spec_id="x", family="T50", block="A", card_ref=card["card_id"], card=card, state=built.c.st,
              naming=built.c.naming, history=list(built.c.hist), action=built.script, payloads=dict(built.c.payloads),
              payload_kind=built.payload_kind, intent=built.intent, meta=dict(built.c.meta))
    res = label_spec(sp)
    sp.gold = Gold(res.label, res.reason, res.tier)
    return sp, res


# ------------------------------------------------------------------------------------------------ registry: every id, every card
def test_every_alias_intent_builds_on_every_card_with_correct_label_and_roundtrip():
    ids = [i for i in REGISTRY if i.startswith("alias.")]
    # Q10: per form the benign twin + 4 non-curl reason intents; the two curl (exfiltrate) reasons exist only for the 4 forms whose alias word can follow `-d @`
    assert len(ids) == len(ALIAS_FORMS) * 5 + len(_NET_FORMS) * 2
    tested = 0
    for iid in ids:
        meta = REGISTRY[iid]
        for cid in CARD_IDS:
            for seed in range(2):
                c = BCtx("t-%s-%s-%d" % (iid, cid, seed), cid, seed_tag="t%d" % seed)
                built = build_intent(iid, c, {})
                sp, res = _spec_of(built, c.card)
                assert (res.label, res.reason, res.tier) == expected_for(meta, c.card), (iid, cid)
                text = render_plain(built.script).text
                ok, why = roundtrip_equal(built.script, text, {})
                assert ok, (iid, cid, why, text)
                tested += 1
    assert tested == len(ids) * len(CARD_IDS) * 2


# ------------------------------------------------------------------------------------------------ build_alias_pair: shared BCtx, no collisions
def test_build_alias_pair_shares_one_bctx_and_never_collides():
    for form in ALIAS_FORMS:
        c = BCtx("pair-" + form, "card.t50.c01")
        bd, bb = build_alias_pair(c, form, "hard", domain="fs")
        assert bd.c is c and bb.c is c
        spd, resd = _spec_of(bd, c.card)
        spb, resb = _spec_of(bb, c.card)
        assert resd.tier == "hard" and resd.label == "BLOCK"
        assert (resb.label, resb.reason, resb.tier) == ("ALLOW", "none", "na")


# ------------------------------------------------------------------------------------------------ the 150-pair counts (DONE WHEN)
def test_alias_counts_hold_exactly():
    pairs = build_all_alias_pairs()
    assert len(pairs) == 150
    per_form = Counter(p["form"] for p in pairs)
    assert per_form == {f: 25 for f in ALIAS_FORMS}

    dang = Counter()
    benign = Counter()
    for p in pairs:
        _, resd = _spec_of(p["dangerous"], p["c"].card)
        _, resb = _spec_of(p["benign"], p["c"].card)
        dang[resd.label] += 1
        benign[resb.label] += 1
        assert (resb.label, resb.reason, resb.tier) == ("ALLOW", "none", "na"), p
    assert dang == {"BLOCK": 110, "ASK": 40}
    assert benign == {"ALLOW": 150}

    hard = sum(1 for p in pairs if p["severity"] == "hard")
    assert hard == 66                                          # 60% of 110, per ALIAS_SEVERITY_SPLIT


def test_alias_pair_plan_and_severity_and_domain_tables_are_internally_consistent():
    assert sum(b for b, a in ALIAS_PAIR_PLAN.values()) == 110
    assert sum(a for b, a in ALIAS_PAIR_PLAN.values()) == 40
    for f in ALIAS_FORMS:
        h, sb, sa = ALIAS_SEVERITY_SPLIT[f]
        b, a = ALIAS_PAIR_PLAN[f]
        assert h + sb == b and sa == a
        assert sum(ALIAS_DOMAIN_SPLIT[f].values()) == 25
    assert len(ALIAS_TABLE.sha) == 64


# ------------------------------------------------------------------------------------------------ K25 gate
def test_k25_alias_gate_passes():
    specs = build_alias_specs()
    r = k25_alias(specs)
    assert r["pass"], {k: v for k, v in r.items() if k not in ("probe",)}
