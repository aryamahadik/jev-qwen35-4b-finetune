"""PREREG A28 (b), fix round r6 (new file; test_mixer.py and test_mixer_a28.py are unchanged): the spec 2.1 attack-twin
quota ('about 5% of own rows, `inv` relation') counts the inv relation's twins and every family's attack marker (F12
twin_kind 'T-ATTACK', F7 twin_kind 'inv'); 'short or no card' counts defs_style no_card (F12) and the sidecar's short
field (F10); an A26 (b) refill never takes a family past 12% of the realised own rows. CPU only, synthetic rows (the
relation / sidecar reader test writes its own files under pytest's tmp_path)."""
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import crowd_select as cs  # noqa: E402
import mixer as mx  # noqa: E402
import test_mixer_a28 as t28  # noqa: E402
from mixio import InputLog  # noqa: E402


@pytest.fixture(autouse=True)
def quiet(monkeypatch):
    monkeypatch.setattr(mx, "log", lambda msg: None)
    monkeypatch.setattr(mx, "A28_TRACE", [])
    monkeypatch.setattr(mx, "OWN_MAX", 1.0)          # as test_mixer_a28: synthetic families are far above 12%


def old_is_attack(r, sd=None):
    """The pre-r6 rule (meta.attack_target, role attacked / attack, twin_kind == 'attack')."""
    m = r.get("meta") or {}
    return bool(m.get("attack_target")) or r.get("role") in ("attacked", "attack") or m.get("twin_kind") == "attack"


def row(i, **kw):
    meta = kw.pop("meta", {})
    return {"id": i, "role": kw.pop("role", "base"), "meta": meta, **kw}


def test_attack_rule_counts_every_family_marking():
    assert mx.is_attack(row("a", role="own", meta={"twin_kind": "T-ATTACK"}))          # F12
    assert mx.is_attack(row("b", role="train", meta={"twin_kind": "inv"}))             # F7
    assert mx.is_attack(row("c", role="attacked"))                                      # F1 (no twin_kind)
    assert mx.is_attack(row("d", role="twin", meta={"twin_kind": "attack"}))           # F6 / F11
    assert mx.is_attack(row("e"), {mx.INV_TWIN: True})                                  # relation file's inv twin
    assert mx.is_attack(row("f"), {"attack": {"form": "x"}})                            # F10 sidecar
    assert not mx.is_attack(row("g"), {"attack": False})
    assert not mx.is_attack(row("h", role="own", meta={"twin_kind": "T-NEG"}))
    assert not mx.is_attack(row("i", role="twin", meta={"twin_kind": "fact_flip"}))
    assert not old_is_attack(row("a", role="own", meta={"twin_kind": "T-ATTACK"}))     # the reviewed defect
    assert not old_is_attack(row("b", role="train", meta={"twin_kind": "inv"}))
    assert mx.short_card(row("j", meta={"defs_style": "no_card"}))                     # F12
    assert mx.short_card(row("k", meta={"defs_style": "codebook"}), {"short": True})   # F10 sidecar
    assert mx.short_card(row("l", meta={"defs_style": "none"}))
    assert not mx.short_card(row("m", meta={"defs_style": "one_line"}), {"short": False})


def test_sidecar_flags_reads_inv_twins_from_relation_files(tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "fam_dir", lambda fam: tmp_path / fam)
    (tmp_path / "F12/out").mkdir(parents=True)
    (tmp_path / "F3/out").mkdir(parents=True)
    rels = [{"a": "a1", "b": "b1", "type": "inv"}, {"a": "a2", "b": "b2", "type": "equiv"},
            {"a": "a3", "b": "b3", "type": "complement"}, {"a": "a4", "b": "b4", "type": "inv"}]
    (tmp_path / "F12/out/relations_candidates_r1.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    side = [{"id": "s1", "vocab": "masked", "attack": True, "short": True, "other": 1}, {"id": "b4", "attack": True}]
    (tmp_path / "F3/out/candidates_r1.sidecar.jsonl").write_text("".join(json.dumps(x) + "\n" for x in side))
    out = mx.sidecar_flags(InputLog(), ["F12", "F3"])
    assert out == {"b1": {mx.INV_TWIN: True}, "b4": {"attack": True, mx.INV_TWIN: True},
                   "s1": {"vocab": "masked", "attack": True, "short": True}}
    assert mx.inv_twin_ids(InputLog(), ["F12", "F3"]) == {"b1", "b4"}


def attack_block(fam="F12", kind="T-ATTACK", n_pairs=12, p="z"):
    """150 yes/no + 150 choice rows; n_pairs attack twins (label unchanged, twin_of the base) among the yes/no rows."""
    rr = t28.plain_rows(fam, p, 150, 150, k=4, card=p)
    yn = [r for r in rr if r["qtype"] == "noul"]
    for j in range(n_pairs):
        base, tw = yn[4 * j], yn[4 * j + 2]                     # same gold (j % 2 pattern: 4j and 4j + 2)
        assert base["gold"] == tw["gold"]
        tw["role"] = "own"
        tw["meta"] |= {"twin_kind": kind, "twin_of": base["id"]}
    return rr


@pytest.mark.parametrize("fam,kind", [("F12", "T-ATTACK"), ("F7", "inv")])
def test_attack_share_guard_sees_f12_and_f7(fam, kind, monkeypatch):
    rows = attack_block(fam, kind)
    nt = {r["id"]: 600 for r in rows}
    st = mx.A28State(rows, nt)
    assert st.c[("blk", fam)]["attack_rows"] == 12                 # 4% of 300
    tw = next(r for r in rows if (r["meta"].get("twin_kind") == kind))
    base = next(r for r in rows if r["id"] == tw["meta"]["twin_of"])
    st.move(out=[tw, base])                                         # 11 / 298 = 3.69%: further from 5%
    assert not st.passes() and any("attack_rows" in m for m in st.broken(st.dirty))
    st.rollback()
    other = [r for r in rows if r["qtype"] == "noul" and not r["meta"].get("twin_kind")
             and r["id"] not in {x["meta"].get("twin_of") for x in rows}]
    st.move(out=[next(r for r in other if r["gold"] == 1), next(r for r in other if r["gold"] == 0)])
    assert st.passes(), st.broken(st.dirty)                         # 12 / 298 = 4.03%: closer to 5%
    st.rollback()
    monkeypatch.setattr(mx, "is_attack", old_is_attack)            # power: the pre-r6 rule saw no attack twin here
    st2 = mx.A28State(rows, nt)
    assert st2.c[("blk", fam)]["attack_rows"] == 0
    st2.move(out=[tw, base])
    assert st2.passes()


def test_attack_twin_from_relation_file_only():
    """A family whose relation file is the only attack marker (side INV_TWIN) is guarded as well."""
    rows = t28.plain_rows("F9", "q", 150, 150, k=4, card="q")
    side = {}
    yn =[r for r in rows if r["qtype"] == "noul"]
    for r in yn[:15]:
        side[r["id"]] = {mx.INV_TWIN: True}
    st = mx.A28State(rows, {r["id"]: 600 for r in rows}, side)
    assert st.c[("blk", "F9")]["attack_rows"] == 15                 # 5%
    st.move(out=[yn[0]])
    assert any("attack_rows" in m for m in st.broken(st.dirty))


def test_short_card_counts_no_card_and_sidecar_short():
    rows = t28.plain_rows("F12", "w", 50, 50, k=4, card="w")
    for i, r in enumerate(rows):
        r["meta"]["defs_style"] = "no_card" if i % 10 == 0 else "one_line"
    f10 = t28.plain_rows("F10", "v", 50, 50, k=4, card="v")
    side = {}
    for i, r in enumerate(f10):
        r["meta"]["defs_style"] = "codebook"
        side[r["id"]] = {"short": i % 5 == 0}
    st = mx.A28State(rows + f10, {r["id"]: 600 for r in rows + f10}, side)
    assert st.c[("blk", "F12")]["short_or_no_card"] == 10
    assert st.c[("blk", "F10")]["short_or_no_card"] == 20


def attack_world():
    """F12: 300 rows, 69% long (104 of the 150 yes/no rows, incl. the 12 attack twins (T-ATTACK, 4%), and 103 of the
    150 choice rows); F3: 800 short rows with a deep short pool (refills)."""
    nt, rows, pools = {}, [], {}
    rows_r, ctx, pools["replay"] = t28.replay_ctx()
    pools["replay"].ctx = ctx
    rows += rows_r
    for r in rows_r:
        nt[r["id"]] = 500
    f12 = attack_block()
    att = {r["id"] for r in f12 if r["meta"].get("twin_kind")}
    yn = [r for r in f12 if r["qtype"] == "noul"]
    long_yn = set(att) | set([r["id"] for r in yn if r["id"] not in att][:104 - len(att)])
    long_ch = {r["id"] for r in f12 if r["qtype"] == "choice"}
    long_ch = set(sorted(long_ch, key=t28.idx)[:103])
    for r in f12:
        nt[r["id"]] = 2600 if r["id"] in long_yn | long_ch else 600
    f12x = t28.plain_rows("F12", "zx", 30, 30, k=4, card="z")
    f3 = t28.plain_rows("F3", "b", 400, 400, card="b")
    f3x = t28.plain_rows("F3", "bx", 200, 200, card="b")
    for r in f12x + f3 + f3x:
        nt[r["id"]] = 600
    for fam, sel, ext in (("F12", f12, f12x), ("F3", f3, f3x)):
        mr, pools[fam] = t28.fam_pool(fam, sel, ext)
        rows += mr
    targets = dict(cs.TARGET_R1) | {"F12": 300, "F3": 800}
    return rows, pools, targets, nt


def true_attack_share(rows_f):
    return sum(1 for r in rows_f if r["meta"].get("twin_kind") == "T-ATTACK") / len(rows_f)


def test_cap_trim_keeps_true_attack_share():
    rows, pools, targets, nt = attack_world()
    f12 = [r for r in rows if r["_block"] == "F12"]
    s0 = true_attack_share(f12)
    assert abs(s0 - 0.04) < 1e-9 and sum(nt[r["id"]] >= 2000 for r in f12) == 207
    out, probs, info, ntok, tr = t28.run(rows, pools, targets, nt)
    f12b = [r for r in out if r["_block"] == "F12"]
    s1 = true_attack_share(f12b)
    assert info["after"]["cap_met"] and not probs, probs
    assert info["guard_audit_break_count"] == 0
    assert info["trims_by_block"]["F12"]["long_rows_removed"] > 0
    assert abs(s1 - 0.05) <= abs(s0 - 0.05) + 1e-12, (s0, s1)       # not further from 5% (independent count)
    ct = info["composition_touched"]["F12"]
    assert ct["before"]["attack_rows"] == 0.04 and ct["after"]["attack_rows"] == round(s1, 4)
    assert info["guard"]["attack_twins_before"]["F12"]["counted"] == 12
    t28.check_rules_kept(rows, out, ntok)


def test_cap_trim_old_rule_lost_attack_share(monkeypatch):
    """Power check for the test above: with the pre-r6 rule the same trim moves F12's attack share away from 5%."""
    monkeypatch.setattr(mx, "is_attack", old_is_attack)
    rows, pools, targets, nt = attack_world()
    s0 = true_attack_share([r for r in rows if r["_block"] == "F12"])
    out, probs, info, ntok, tr = t28.run(rows, pools, targets, nt)
    s1 = true_attack_share([r for r in out if r["_block"] == "F12"])
    assert info["after"]["cap_met"]
    assert abs(s1 - 0.05) > abs(s0 - 0.05), (s0, s1)


def share_world_over12():
    """F3 holds 15.6% of the 960 own rows before the trim and has the lowest rows / target and a deep short pool;
    F4-F10 (100 rows each, F4 with a short pool); F13 (110 rows, all long) is trimmed."""
    nt, rows, pools = {}, [], {}
    rows_r, ctx, pools["replay"] = t28.replay_ctx()
    pools["replay"].ctx = ctx
    rows += rows_r
    for r in rows_r:
        nt[r["id"]] = 500
    for f in ("F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"):
        n = 75 if f == "F3" else 50
        sel = t28.plain_rows(f, f.lower() + "s", n, n, k=4, card=f.lower())
        extra = t28.plain_rows(f, f.lower() + "x", 60, 60, k=4, card=f.lower()) if f in ("F3", "F4") else []
        for r in sel + extra:
            nt[r["id"]] = 600
        mr, pools[f] = t28.fam_pool(f, sel, extra)
        rows += mr
    f13 = t28.f13_rows("t", yn_n=40, ch=((4, 28), (5, 30), (12, 6), (25, 6)))
    for i, r in enumerate(f13):
        nt[r["id"]] = 6500 if i % 3 == 0 else 3000
    mr, pools["F13"] = t28.fam_pool("F13", f13, [])
    rows += mr
    targets = dict(cs.TARGET_R1) | {f: 100 for f in ("F4", "F5", "F6", "F7", "F8", "F9", "F10")} | \
        {"F3": 300, "F13": 110}
    return rows, pools, targets, nt


def test_refill_never_past_12pct_of_realised_own_rows(monkeypatch):
    monkeypatch.setattr(mx, "OWN_MAX", 0.12)
    rows, pools, targets, nt = share_world_over12()
    own0 = sum(1 for r in rows if r["_block"] in cs.FAMS)
    assert own0 == 960 and 150 / own0 > 0.12
    out, probs, info, ntok, tr = t28.run(rows, pools, targets, nt)
    cnt = Counter(r["_block"] for r in out)
    own1 = sum(cnt[f] for f in cs.FAMS)
    assert info["after"]["cap_met"] and not probs, probs
    ref = info["refilled_rows_by_family"]
    assert ref.get("F3", 0) == 0 and ref.get("F4", 0) > 0              # F3 (lowest rows / target) is over 12%
    for f, n in ref.items():
        assert n <= 0 or cnt[f] / own1 <= 0.12 + 1e-12, f            # every refilled family ends <= 12%
    assert cnt["F3"] / own1 <= 150 / own0 + 1e-12                      # no refill: no worse than before the trim
    assert info["family_share_limit"]["F3"] == round(150 / own0, 4) and info["family_share_limit"]["F4"] == 0.12


def test_g10_attack_label_check_sees_f12(monkeypatch):
    rows = []
    for j in range(40):
        r = t28.yn(f"g{j}", f"gu{j}", 1 if j < 20 else 0, "F12", w=f"wd.{j % 4}")
        if j < 20:
            r["role"], r["meta"]["twin_kind"] = "own", "T-ATTACK"
        rows.append(r)
    probs = mx.g10_checks(rows, {}, False, {})
    assert "G10 attack presence correlates with the label" in probs
    monkeypatch.setattr(mx, "is_attack", old_is_attack)
    assert "G10 attack presence correlates with the label" not in mx.g10_checks(rows, {}, False, {})
