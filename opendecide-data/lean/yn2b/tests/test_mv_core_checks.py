"""mv_core checks (SPEC 4.6-4.8, 8.3-8.4): each check passes on balanced synthetic rows and catches the defect it
is for."""
from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import toy_family as toy  # noqa: E402
import mv_core as mv  # noqa: E402


def row(i, gold="yes", qkind="yn", **meta):
    given = meta.pop("options", None)
    m = {k: None for k in mv.RAW_META_KEYS}
    m.update(family="F2", pack="bank", tier="standard", polarity=0 if qkind in ("yn", "jb") else None, fmt="json",
             len_bin=0, tpl="t1", renderer="r1", view="base", qkind=qkind, card_style="lower" if qkind == "yn" else None,
             latent_id=f"f2-tr-{i:06d}", shortcut_hits={}, n_shortcut_wrong=0, edge=None, role="aff")
    m.update(meta)
    opts = ["yes", "no"] if qkind == "yn" else given or ["A", "B", "C", "D"]
    return {"key": "gen3_tool_guard", "rid": f"f2-tr-{i:06d}-0", "state": "s" * (100 + i % 7), "instructions": "Q?",
            "options": opts, "gold": gold, "soft": None, "meta": m}


def test_share_rule():
    assert mv.share_ok(9, 20) and mv.share_ok(11, 20) and not mv.share_ok(12, 20) and not mv.share_ok(8, 20)
    assert mv.share_ok(45, 100) and not mv.share_ok(44, 100)
    assert mv.share_ok(2, 3) and mv.share_ok(1, 3) and not mv.share_ok(3, 3) and mv.share_ok(1, 1)


def test_balance_report():
    rows = [row(i, "yes" if i % 2 else "no") for i in range(200)]
    assert mv.balance_report(rows)["ok"]
    bad = [row(i, "yes" if i % 2 else "no", tpl="t2" if i % 2 else "t1") for i in range(200)]
    rep = mv.balance_report(bad)
    assert not rep["ok"] and {v["group"] for v in rep["violations"]} == {"tpl"}  # the template predicts gold
    skew = [row(i, "yes" if i % 3 else "no") for i in range(200)]
    assert not mv.balance_report(skew)["ok"]


def test_positions_levels_none():
    rows = [row(i, "ABCD"[i % 4], qkind="choice", view="mirror") for i in range(80)]
    assert mv.position_report(rows)["ok"]
    assert not mv.position_report([row(i, "A", qkind="choice") for i in range(80)])["ok"]
    lv = ["cold", "warm", "hot"]
    good = [row(i, lv[i % 3], qkind="score", options=lv) for i in range(60)]
    assert mv.level_report(good)["ok"]
    assert not mv.level_report([row(i, lv[i % 2], qkind="score", options=lv) for i in range(60)])["ok"]
    nn = ["A", "B", "C", mv.NONE_DEFAULT]
    m = [row(i, mv.NONE_DEFAULT if i % 4 == 0 else "A", qkind="choice", view="mirror", options=nn,
             none_option=mv.NONE_DEFAULT) for i in range(80)]
    assert mv.none_report(m)["ok"]
    m2 = [row(i, "A", qkind="choice", view="mirror", options=nn, none_option=mv.NONE_DEFAULT) for i in range(80)]
    assert not mv.none_report(m2)["ok"]  # a 'none' option that is never gold is an artefact


def test_tiers_and_shortcuts():
    tiers = ["easy"] * 15 + ["standard"] * 30 + ["judge"] * 20 + ["hard"] * 35
    rows = [row(i, tier=t, shortcut_hits={"a": 0, "b": 0, "c": 1} if t == "hard" else {"a": i % 2, "b": 1 - i % 2},
                n_shortcut_wrong=2 if t == "hard" else 1) for i, t in enumerate(tiers)]
    rep = mv.tier_report(rows)
    assert rep["ok"], rep
    rows[99]["meta"]["n_shortcut_wrong"] = 1
    assert not mv.tier_report(rows)["ok"]
    sc = mv.shortcut_report(rows)
    assert not sc["ok"] and "c" in sc["over_cap"]  # c is right on every hard row -> over 60%
    assert mv.shortcut_report([row(i, shortcut_hits={"a": i % 2}) for i in range(10)])["ok"]


def test_edges_plants_cards():
    ex = [row(i, "yes" if i % 2 else "no", edge=["exc:deny_allow", "exc:allow_deny", "exc:near_miss"][i % 3])
          for i in range(90)]
    assert mv.edge_report(ex)["exception_ok"]
    ex2 = [row(i, edge="exc:deny_allow") for i in range(30)] + ex[:30]
    assert not mv.edge_report(ex2)["exception_ok"]
    mi = [row(i, "no", edge="missing_info") for i in range(20)]
    assert not mv.edge_report(mi)["missing_info_ok"]  # 'missing -> no' would be a shortcut
    mp = [row(i, edge="mixed_provenance" if i < 10 else None) for i in range(100)]
    assert not mv.edge_report(mp)["mixed_provenance_ok"]
    at = [row(i, view="attack", role="attacked", plant_dir=["for_gold", "against_gold"][i // 4 % 2],
              plant_tpl=f"t{i % 4}", plant_spoof=i % 4 == 0) for i in range(80)]
    assert mv.plant_report(at)["ok"]
    at2 = [dict(r, meta={**r["meta"], "plant_dir": "against_gold"}) for r in at]
    assert not mv.plant_report(at2)["ok"]  # 'answer against the plant' would be learnable
    cs = [row(i, "yes" if i % 2 else "no", card_style=["lower", "upper", "none", "lower", "lower"][i // 2 % 5])
          for i in range(200)]
    assert mv.card_report(cs)["ok"]
    cs2 = [row(i, "yes" if i % 2 else "no", card_style="none" if i % 2 else "lower") for i in range(200)]
    assert not mv.card_report(cs2)["ok"] and not mv.artefact_corr(cs2)["ok"]


def test_artefacts_keysets_structure():
    rows = [row(i, "yes" if i % 2 else "no") for i in range(200)]
    for r in rows:
        r["state"] = "x" * 300
    assert mv.artefact_corr(rows)["ok"]
    long_yes = [dict(r, state="x" * (300 + 200 * (r["gold"] == "yes"))) for r in rows]
    rep = mv.artefact_corr(long_yes)
    assert not rep["ok"] and "yn:length" in rep["over"]
    js = [dict(row(i), state=mv.render_json({"a": 1, "b": []} if i % 2 else {"a": 1})) for i in range(10)]
    assert not mv.keyset_report(js)["ok"]  # key presence could give the answer away
    a, b = row(1, "yes"), row(1, "no")
    b = dict(b, rid="f2-tr-000001-1", meta={**b["meta"], "view": "ladder"})
    assert mv.structure_report([a, b], [{"type": "complement", "a": a["rid"], "b": b["rid"]}])["ok"]
    assert not mv.structure_report([a, b], [{"type": "equiv", "a": a["rid"], "b": b["rid"]}])["ok"]
    c = dict(row(1, "yes"), rid="f2-tr-000001-2", meta={**a["meta"], "twin_of": a["rid"]})
    assert not mv.structure_report([a, c], [])["ok"]  # a twin that keeps gold


def test_run_checks_on_toy_and_label_verification(tmp_path):
    fb = mv.FamilyBuilder(toy.KEY, generator_file=toy.__file__, raw_dir=tmp_path / "raw", defs_dir=tmp_path / "defs",
                          manifest=tmp_path / "m.jsonl", tier_shares={"easy": 0.3, "standard": 0.4, "hard": 0.3})
    toy.build(fb, "train", 200)
    rep = mv.run_checks(fb.rows, fb.rels, fb.tier_shares)
    for k in ("structure", "positions", "none", "tiers", "plants", "cards", "keysets", "edges"):
        assert rep[k]["ok"], (k, rep[k])
    # the toy's shortcuts are deliberately weak solvers: the family rule flags them (> 60%)
    assert not rep["shortcuts"]["ok"] and not rep["ok"]
    assert mv.verify_labels(fb.rows, toy.decide2_row)["ok"]
    flipped = lambda r: ({"yes": "no", "no": "yes"}.get(r["gold"], r["gold"]) if r["meta"]["qkind"] == "yn"
                         else r["gold"])
    v = mv.verify_labels(fb.rows, flipped)
    assert not v["ok"] and v["disagree"] == sum(r["meta"]["qkind"] == "yn" for r in fb.rows)
    und = mv.verify_labels(fb.rows[:5], lambda r: mv.UNDEFINED)
    assert und["undefined"] == 5 and not und["ok"]


def test_hard_case_report():
    rows = [row(i, edge="hc:decoy_id,numeric" if i % 2 else "hc:dst") for i in range(10)]
    rep = mv.hard_case_report(rows)
    assert rep["by_area"]["look_alikes"] == {"hc:decoy_id": 5} and rep["by_area"]["numbers_time"] == {"hc:dst": 5}
    assert "hc:env_alias" in rep["absent"]["look_alikes"] and "hc:dst" not in rep["absent"]["numbers_time"]
