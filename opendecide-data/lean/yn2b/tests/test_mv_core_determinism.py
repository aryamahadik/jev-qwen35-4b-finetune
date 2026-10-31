"""mv_core determinism (SPEC 4.11): seeds, streams, the tz pin, disjoint invented name pools, identical rebuilds."""
from __future__ import annotations

import hashlib
import json
import random
import sys
from datetime import date, datetime
from fractions import Fraction
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import toy_family as toy  # noqa: E402
import mv_core as mv  # noqa: E402


def test_seed_formula():
    assert mv.split_seed("gen3_rule_chain", "train") == 20261001 + 1
    assert mv.split_seed("gen3_tool_guard", "train") == 20261001 + 2
    assert mv.split_seed("gen3_tool_guard", "dev_iid") == 20261003 + 10 ** 9
    assert mv.split_seed("gen3_tool_guard", "dev_holdout") == 20261003 + 2 * 10 ** 9
    assert mv.split_seed("gen3_table_layouts", "devx") == 20261001 + 8 + 3 * 10 ** 9
    assert mv.rng_for("gen3_lead_score", "train").random() == random.Random(20261006).random()
    assert mv.rng_for("gen3_lead_score", "train", "x").random() == mv.rng_for("gen3_lead_score", "train", "x").random()
    assert len(mv.FAMILIES) == 8 and sorted(mv.FAMILIES.values()) == list(range(1, 9))
    with pytest.raises(KeyError):
        mv.split_seed("gen3_nope", "train")
    with pytest.raises(ValueError):
        mv.register_test_family("gen3_tool_guard", 150)


def test_tz_pin():
    info = mv.assert_tz()
    assert info["version"] == mv.TZ_PIN["version"] and info["fingerprint"] == mv.TZ_PIN["fingerprint"]
    with pytest.raises(RuntimeError):
        mv.assert_tz({"version": "1999a", "fingerprint": mv.TZ_PIN["fingerprint"]})
    mv.assert_tz_year(date(2026, 5, 1))
    with pytest.raises(ValueError):
        mv.assert_tz_year(date(2031, 1, 1))


def test_dst_and_business_days():
    assert not mv.local_time_ok(datetime(2026, 3, 8, 2, 30), "America/New_York")    # spring-forward gap
    assert not mv.local_time_ok(datetime(2026, 11, 1, 1, 30), "America/New_York")   # fall-back fold
    assert mv.local_time_ok(datetime(2026, 3, 8, 3, 30), "America/New_York")
    assert mv.to_utc(datetime(2026, 7, 1, 9, 0), "Europe/Berlin").hour == 7
    with pytest.raises(ValueError):
        mv.to_utc(datetime(2026, 3, 29, 2, 30), "Europe/Berlin")
    fri, hol = date(2026, 4, 3), [date(2026, 4, 6)]
    assert mv.add_business_days(fri, 1) == date(2026, 4, 6)
    assert mv.add_business_days(fri, 1, hol) == date(2026, 4, 7)
    assert mv.business_days_between(fri, date(2026, 4, 7), hol) == 1


def test_numbers_and_lookalikes():
    t = mv.boundary_triple(500)
    assert (t["below"], t["at"], t["above"]) == (499, 500, 501)
    assert mv.pct_off(200)["above"] == Fraction(202)
    assert mv.compare(500, "<=", 500) and not mv.compare(500, "<", 500)
    assert mv.convert(Fraction("123.45"), Fraction("0.9215")) == Fraction("113.76")  # 113.759175 half-up
    assert mv.round_half_up(Fraction("0.125"), 2) == Fraction("0.13")
    assert mv.fmt_amount(Fraction("1234.5")) == "1,234.50"
    rng = random.Random(0)
    d = mv.decoy_id("W3319027", rng)
    assert d != "W3319027" and sorted(d) == sorted("W3319027") and len(d) == 8
    for kind in ("tld", "hyphen", "double", "rn", "suffix"):
        la, k = mv.lookalike_domain("mardova.com", rng, kind)
        assert k == kind and la != "mardova.com"
    assert mv.lookalike_domain("acme.com", rng, "tld")[0] == "acme.co"


def test_name_pools_disjoint_and_invented():
    pools = {s: mv.NamePool(s) for s in mv.SPLITS}
    for a in mv.SPLITS:
        for b in mv.SPLITS:
            if a < b:
                assert not set(pools[a].first) & set(pools[b].first)
                assert not set(pools[a].last) & set(pools[b].last)
                assert not set(pools[a].stems) & set(pools[b].stems)
    tr = pools["train"]
    assert len(tr.first) > 5000 and len(tr.last) > 5000 and len(tr.stems) > 3000
    for s in mv.SPLITS[1:]:
        assert len(pools[s].first) > 500 and len(pools[s].stems) > 400
    rng = random.Random(1)
    p = tr.person(rng)
    assert mv.name_split(p.split()[0]) == "train" and mv.name_split(p.split()[1]) == "train"
    assert tr.domain(rng).endswith((".example", ".test")) and tr.domain(rng, reserved=False).endswith(mv._PUBLIC_TLDS)
    assert "@" in tr.email(rng)


def _build(tmp):
    fb = mv.FamilyBuilder(toy.KEY, generator_file=toy.__file__, raw_dir=tmp / "raw", defs_dir=tmp / "defs",
                          manifest=tmp / "m.jsonl", tier_shares={"easy": 0.3, "standard": 0.4, "hard": 0.3})
    toy.build(fb, "train", 120)
    toy.build(fb, "dev_holdout", 20)
    fb.write()
    return fb


def test_rebuild_is_identical(tmp_path):
    a, b = _build(tmp_path / "a"), _build(tmp_path / "b")
    assert json.dumps(a.rows) == json.dumps(b.rows) and a.rels == b.rels
    for part in ("train", "dev"):
        pa, pb = mv.raw_paths(toy.KEY, part, tmp_path / "a" / "raw")[0], mv.raw_paths(toy.KEY, part, tmp_path / "b" / "raw")[0]
        assert hashlib.sha256(pa.read_bytes()).digest() == hashlib.sha256(pb.read_bytes()).digest()
    ids = [r["meta"]["latent_id"] for r in a.rows]
    assert ids[0] == "t101-tr-000000" and any(x.startswith("t101-dh-") for x in ids)


def test_latent_streams_do_not_depend_on_order():
    fb = mv.FamilyBuilder(toy.KEY, check_tz=False)
    l0 = fb.new_latent("train", "p", {}, None, "easy")
    l1 = fb.new_latent("train", "p", {}, None, "easy")
    fb2 = mv.FamilyBuilder(toy.KEY, check_tz=False)
    m0 = fb2.new_latent("train", "p", {}, None, "easy")
    assert l0.seed == m0.seed and l0.seed != l1.seed and l0.rng("x").random() == m0.rng("x").random()
    assert l0.dev_kind is None and fb.new_latent("devx", "p", {}, None, "easy").dev_kind == "devx"


def test_guard_refuses_frozen_locations():
    for rel in ("data/v14_parts/raw/gen3_x.jsonl", "data/v14_parts/defs/gen3_x.json", "data/yn2b_dev.jsonl",
                "data/v14_parts/golden_train.jsonl", "train_decoder.py"):
        with pytest.raises(RuntimeError):
            mv._guard(mv.LEAN / rel)
    mv._guard(mv.LEAN / "data/v14_parts/yn2b_raw/gen3_x.jsonl")
    mv._guard(mv.LEAN / "data/v14_parts/yn2b_defs/gen3_x__q1.json")
    assert mv.raw_paths("gen3_tool_guard", "train")[0] == mv.LEAN / "data/v14_parts/yn2b_raw/gen3_tool_guard.jsonl"
    assert mv.raw_paths("gen3_tool_guard", "dev")[1] == mv.LEAN / "data/v14_parts/yn2b_raw/dev/relations/gen3_tool_guard.jsonl"
    assert mv.raw_paths("gen3_tool_guard", "devx")[0].name == "gen3_tool_guard__devx.jsonl"
