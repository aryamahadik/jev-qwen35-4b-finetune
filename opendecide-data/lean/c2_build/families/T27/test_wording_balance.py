"""Tests of the T27 G11 wording balance (wording_balance.py). Stub skins and a stub plugin: no pools, no model.
Run from lean/c2_build:  ../.venv/bin/python -B -m pytest zed_orch/t27_fix_r2/test_wording_balance.py -q -p no:cacheprovider
After install_code.py the same file is installed as families/T27/test_wording_balance.py."""
import random
import sys
from pathlib import Path
from types import SimpleNamespace as NS

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = next(p for p in HERE.parents if (p / "c2_kit").is_dir())
for p in (str(C2), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest  # noqa: E402

try:
    import wording_balance as WB  # staged location
except ImportError:  # installed location
    from families.T27 import wording_balance as WB  # type: ignore  # noqa: E402

from c2_kit.plugin import KitCtx  # noqa: E402

FAM = "T27"


def sk(sid, qform, held=False, kind="wording"):
    return NS(skin_id=sid, family=FAM, kind=kind, held_out=held, register="question", qform=qform)


def make_ctx(n_by_q, held=2, bal=True):
    skins = {}
    for q, n in n_by_q.items():
        for i in range(n):
            skins[f"w-{q}-{i}"] = sk(f"w-{q}-{i}", q)
        for i in range(held):
            skins[f"h-{q}-{i}"] = sk(f"h-{q}-{i}", q, held=True)
    return WB.BalancedKitCtx(skins=skins, lexicon=None, balancer=WB.WordingBalancer() if bal else None)


def key(seed, sampler="S1", q="ch_next"):
    return f"{FAM}|{seed}|{sampler}|{q}"


def test_stream_of():
    assert WB.stream_of("T27|72000123|S1|ch_next") == 72
    assert WB.stream_of("T27|900007|S2|yn_beyond") == 0
    assert WB.stream_of("garbage") == 0


def test_balance_bound_with_unit_weights():
    """max - min of the booked load stays within the heaviest unit, for any sequence of unit sizes."""
    rng = random.Random(7)
    ctx = make_ctx({"ch_next": 17})
    load = {}
    for i in range(1256 // 2):
        w = rng.choice([1, 1, 2, 2, 3, 4])
        ctx.balancer.weight = w
        s = ctx.pick(FAM, "wording", key(72_000_000 + i), qform="ch_next")
        ctx.balancer.weight = 1
        load[s.skin_id] = load.get(s.skin_id, 0) + w
    vals = [load.get(f"w-ch_next-{i}", 0) for i in range(17)]
    assert max(vals) - min(vals) <= 4, vals
    assert not any(k.startswith("h-") for k in load)             # held-out never drawn for a training pick


def test_pick_is_memoised_and_does_not_rebook():
    ctx = make_ctx({"yn_beyond": 5})
    a = ctx.pick(FAM, "wording", key(5, q="yn_beyond"), qform="yn_beyond")
    tot = sum(ctx.balancer.load[(0, "yn_beyond")].values())
    b = ctx.pick(FAM, "wording", key(5, q="yn_beyond"), qform="yn_beyond")
    assert a.skin_id == b.skin_id
    assert sum(ctx.balancer.load[(0, "yn_beyond")].values()) == tot


def test_strata_and_streams_are_independent():
    ctx = make_ctx({"yn_beyond": 4, "yn_within": 4})
    for i in range(40):
        ctx.pick(FAM, "wording", key(72_000_000 + i, q="yn_beyond"), qform="yn_beyond")
    ctx.pick(FAM, "wording", key(73_000_000, q="yn_beyond"), qform="yn_beyond")
    ld = ctx.balancer.load
    assert sum(ld[(72, "yn_beyond")].values()) == 40
    assert sum(ld[(73, "yn_beyond")].values()) == 1
    assert (72, "yn_within") not in ld


def test_deterministic_across_instances():
    seq = [key(72_000_000 + i, q="yn_beyond") for i in range(60)]
    a = [make_ctx({"yn_beyond": 9}).pick(FAM, "wording", k, qform="yn_beyond").skin_id for k in seq[:1]]
    c1, c2 = make_ctx({"yn_beyond": 9}), make_ctx({"yn_beyond": 9})
    p1 = [c1.pick(FAM, "wording", k, qform="yn_beyond").skin_id for k in seq]
    p2 = [c2.pick(FAM, "wording", k, qform="yn_beyond").skin_id for k in seq]
    assert p1 == p2 and a[0] == p1[0]


def test_empty_stratum_matches_legacy_hash_pick():
    """The first pick of a stratum (all loads 0) is the old min-uhash pick."""
    ctx = make_ctx({"ch_next": 12})
    legacy = KitCtx(skins=ctx.skins).pick(FAM, "wording", key(72_000_001), qform="ch_next")
    assert ctx.pick(FAM, "wording", key(72_000_001), qform="ch_next").skin_id == legacy.skin_id


def test_held_out_and_other_kinds_use_the_legacy_draw():
    ctx = make_ctx({"ch_next": 6}, held=3)
    ctx.skins["sk-1"] = sk("sk-1", None, kind="skin")
    ctx.skins["sk-2"] = sk("sk-2", None, kind="skin")
    plain = KitCtx(skins=dict(ctx.skins))
    for i in range(30):
        k = key(68_000_000 + i, "S5")
        assert ctx.pick(FAM, "wording", k, qform="ch_next", held_out=True).skin_id == \
            plain.pick(FAM, "wording", k, qform="ch_next", held_out=True).skin_id
        assert ctx.pick(FAM, "skin", k).skin_id == plain.pick(FAM, "skin", k).skin_id
    assert ctx.balancer.load == {}


def test_lookup_error_when_stratum_empty():
    ctx = make_ctx({"ch_next": 3})
    with pytest.raises(LookupError):
        ctx.pick(FAM, "wording", key(1), qform="yn_beyond")
    with pytest.raises(LookupError):
        ctx.pick(FAM, "wording", key(1), qform="ch_next", exclude=tuple(f"w-ch_next-{i}" for i in range(3)))


def test_exclude_is_honoured():
    ctx = make_ctx({"yn_within": 4})
    ex = ("w-yn_within-0", "w-yn_within-1")
    for i in range(30):
        assert ctx.pick(FAM, "wording", key(10 + i, q="yn_within"), qform="yn_within", exclude=ex).skin_id not in ex


class StubPlugin:
    FAMILY = FAM

    def __init__(self, kinds):
        self.kinds = kinds
        self.calls = 0

    def quarantined_wordings(self, ctx):
        return {sid: ["p"] for sid in ctx.skins if sid.endswith("-bad")}

    def fits(self, s, spec):
        return s.skin_id != "carrier-nofit"

    def relations(self, spec):
        self.calls += 1
        return [NS(kind=k) for k in self.kinds]


def test_ctx_for_drops_polarity_quarantined_and_unfitting_and_keeps_the_rest():
    base = make_ctx({"yn_beyond": 3}, bal=False)
    base.skins["w-yn_beyond-bad"] = sk("w-yn_beyond-bad", "yn_beyond")
    base.skins["carrier-nofit"] = sk("carrier-nofit", None, kind="skin")
    base.skins["carrier-ok"] = sk("carrier-ok", None, kind="skin")
    base.skins["atk"] = sk("atk", None, kind="attack")
    pl = StubPlugin([])
    out = WB.ctx_for(pl, NS(), base)
    assert isinstance(out, WB.BalancedKitCtx)
    assert "w-yn_beyond-bad" not in out.skins and "carrier-nofit" not in out.skins
    assert {"carrier-ok", "atk"} <= set(out.skins)
    assert WB.ctx_for(pl, NS(), out).balancer is out.balancer          # the second narrowing keeps one balancer


def test_pick_wording_books_unit_size_and_counts_only_emitting_relations():
    pl = StubPlugin(["complement", "twin", "metamorphic", "equiv"])    # 3 emitting + base = 4 rows
    ctx = WB.ctx_for(pl, NS(), make_ctx({"ch_next": 3}, bal=False))
    spec = NS(qform="ch_next")
    k = key(72_000_005)
    w = WB.pick_wording(pl, ctx, spec, k, held=False)
    assert ctx.balancer.load[(72, "ch_next")][w.skin_id] == 4
    n = pl.calls
    assert WB.pick_wording(pl, ctx, spec, k, held=False).skin_id == w.skin_id
    assert pl.calls == n                                               # the repeat does not recompute the unit size
    assert ctx.balancer.weight == 1


def test_pick_wording_held_out_falls_back_to_training_when_none_exists():
    pl = StubPlugin([])
    base = make_ctx({"ch_next": 3}, held=0, bal=False)
    ctx = WB.ctx_for(pl, NS(), base)
    w = WB.pick_wording(pl, ctx, NS(qform="ch_next"), key(9, "S5"), held=True)
    assert not w.held_out
