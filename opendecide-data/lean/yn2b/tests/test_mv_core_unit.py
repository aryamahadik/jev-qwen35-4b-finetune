"""mv_core Unit rules (SPEC 4.2, 4.5, 4.8, 4.9, 8.2-8.3): every violation raises Reject; nothing is patched."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import toy_family as toy  # noqa: E402
import mv_core as mv  # noqa: E402

Y = {"yes": "Allowed under the policy.", "no": "Blocked under the policy (a missing fact counts as no)."}


def setup():
    fb = mv.FamilyBuilder(toy.KEY, check_tz=False)
    lat = fb.new_latent("train", "p", {}, None, "standard")
    return fb, lat, fb.unit(lat)


def yn(state="Limit 500.00; amount 499.99.", gold="yes", view="base", ins="May the payment run?", **kw):
    kw.setdefault("polarity", 0)
    kw.setdefault("defs", Y)
    return mv.RowSpec(view, "yn", state, ins, gold, "prose", "r1", "t1", **kw)


def test_basic_add_and_meta():
    fb, lat, u = setup()
    rid = u.add(yn(decisive=("499.99",), shortcut_answers={"s1": "no", "s2": "yes", "s3": None}))
    r = u.row(rid)
    assert rid == "t101-tr-000000-0" and r["gold"] == "yes" and r["options"] == ["yes", "no"]
    m = r["meta"]
    assert tuple(m) == mv.RAW_META_KEYS
    assert m["shortcut_hits"] == {"s1": 0, "s2": 1} and m["n_shortcut_wrong"] == 1 and m["role"] == "aff"
    assert m["card_style"] in ("lower", "upper") and m["defs"] == mv.defs_qid(Y) and m["len_bin"] == 0
    assert m["family"] == "T101" and m["dev_kind"] is None and m["split"] == "train"
    fb.commit(u)
    assert fb.rows == [r] and fb.defs[m["defs"]] == Y


def test_yes_no_rules():
    fb, lat, u = setup()
    with pytest.raises(mv.Reject):
        u.add(yn(defs={"yes": "only yes"}))
    with pytest.raises(mv.Reject):
        u.add(yn(card_style="none"))  # a no-card row must be self-contained
    with pytest.raises(mv.Reject):
        u.add(yn(polarity=None))
    with pytest.raises(mv.Reject):
        u.add(yn(gold="maybe"))
    u.add(yn(card_style="none", self_contained=True))


def test_choice_score_jb_rules():
    fb, lat, u = setup()
    ch = dict(view="base", qkind="choice", state="S", instructions="Which rule?", fmt="prose", renderer="r",
              tpl="t")
    with pytest.raises(mv.Reject):  # gold not an option
        u.add(mv.RowSpec(**ch, gold="x", options=["a", "b"]))
    with pytest.raises(mv.Reject):  # a definition for a non-option would be dropped by decoder_io
        u.add(mv.RowSpec(**ch, gold="a", options=["a", "b"], defs={"c": "def"}))
    with pytest.raises(mv.Reject):
        u.add(mv.RowSpec(**dict(ch, qkind="score"), gold="a", options=["a", "b", "c"], defs={"a": "x"}))
    with pytest.raises(mv.Reject):
        u.add(mv.RowSpec(**dict(ch, qkind="jb", view="jb"), gold="a", options=["a", "b", "c"]))
    with pytest.raises(mv.Reject):  # the jb view uses qkind jb
        u.add(mv.RowSpec(**dict(ch, view="jb"), gold="a", options=["a", "b"]))
    rid = u.add(mv.RowSpec(**dict(ch, qkind="score", state="S2"), gold="warm", options=["cold", "warm", "hot"]))
    assert u.row(rid)["meta"]["levels"] == 3 and u.row(rid)["meta"]["role"] == "choice"


def test_grounding_judge_edges_and_format():
    fb, lat, u = setup()
    with pytest.raises(mv.Reject):
        u.add(yn(decisive=("500.01",)))
    with pytest.raises(mv.Reject):
        u.add(yn(judge=True, defs={"yes": "The verdict is correct.", "no": "It is not."}))
    with pytest.raises(mv.Reject):
        u.add(yn(edge=("made_up_tag",)))
    with pytest.raises(mv.Reject):  # json states must be exactly the JevBench rendering
        u.add(mv.RowSpec("base", "yn", '{"a": 1}', "Q?", "yes", "json", "r", "t", defs=Y, polarity=0))
    with pytest.raises(mv.Reject):
        u.add(mv.RowSpec("base", "yn", "S", "Q?", "yes", "html", "r", "t", defs=Y, polarity=0))
    u.add(mv.RowSpec("base", "yn", mv.render_json({"a": "x \"q\" y"}), "Q?", "yes", "json", "r", "t", defs=Y,
                     polarity=0, decisive=('x "q" y',), edge=("hc:decoy_id", "numeric")))


def test_hard_tier_needs_two_wrong_shortcuts():
    fb = mv.FamilyBuilder(toy.KEY, check_tz=False)
    u = fb.unit(fb.new_latent("train", "p", {}, None, "hard"))
    with pytest.raises(mv.Reject):
        u.add(yn(shortcut_answers={"a": "no", "b": "yes"}))
    u.add(yn(shortcut_answers={"a": "no", "b": "no", "c": "yes"}))


def test_unit_size_rules():
    fb, lat, u = setup()
    for i in range(5):
        u.add(yn(state=f"state number {i}"))
    with pytest.raises(mv.Reject):
        u.add(yn(state="sixth"))
    fb, lat, u = setup()
    u.add(yn(state="x" * 6001))
    u.add(yn(state="y" * 100))
    u.add(yn(state="z" * 100))
    with pytest.raises(mv.Reject):  # a unit with a state over 6K holds at most 3 rows
        u.add(yn(state="w" * 100))
    fb, lat, u = setup()
    u.add(yn(state="a" * 5900))
    u.add(yn(state="b" * 5900))
    u.add(yn(state="c" * 5900))
    u.add(yn(state="d" * 5900))
    with pytest.raises(mv.Reject):  # total state <= 24K
        u.add(yn(state="e" * 1000))


def test_duplicates_rejected_within_unit_and_family():
    fb, lat, u = setup()
    u.add(yn())
    with pytest.raises(mv.Reject):
        u.add(yn(state="Limit 500.00;  amount 499.99. "))  # same after normalisation
    fb.commit(u)
    u2 = fb.unit(fb.new_latent("train", "p", {}, None, "standard"))
    with pytest.raises(mv.Reject):
        u2.add(yn())


def test_relations():
    fb, lat, u = setup()
    a = u.add(yn(state="S1"))
    b = u.add(yn(state="S1", view="ladder", gold="no", polarity=1, role="neg", ins="Must the payment be blocked?"))
    c = u.add(yn(state="S1 in another format", view="format"))
    d = u.add(mv.RowSpec("mirror", "choice", "S1", "Which?", "a", "prose", "r", "t", options=["a", "b"]))
    u.relate("complement", a, b)
    with pytest.raises(mv.Reject):
        u.relate("complement", a, c)  # a row is in at most one complement (and golds must sum to 1)
    with pytest.raises(mv.Reject):
        u.relate("complement", b, c)  # b already used
    u.relate("equiv", a, c)
    with pytest.raises(mv.Reject):
        u.relate("equiv", a, d)  # cross-type equiv is skipped by the trainer, so refused here
    with pytest.raises(mv.Reject):
        u.relate("inv", a, c)  # b must be an attack twin
    with pytest.raises(mv.Reject):
        u.relate("mirror", a, d)
    fb.commit(u)
    assert {x["type"] for x in fb.rels} == {"complement", "equiv"}


def test_contrast_twin_rules():
    fb, lat, u = setup()
    base = u.add(yn(state="line1\nlimit 500\namount 499\nline4"))
    u.add(yn(state="line1\nlimit 500\namount 501\nline4", gold="no", view="contrast"), twin_of=base)
    fb.commit(u)
    fb, lat, u = setup()
    base = u.add(yn(state="line1\nlimit 500\namount 499\nline4"))
    u.add(yn(state="line1\nlimit 500\namount 501\nline4", gold="yes", view="contrast"), twin_of=base)
    with pytest.raises(mv.Reject):  # a contrast twin must flip gold
        fb.commit(u)
    fb, lat, u = setup()
    base = u.add(yn(state="a\nb\nc\nd\ne"))
    u.add(yn(state="p\nq\nr\ns\ne", gold="no", view="contrast"), twin_of=base)
    with pytest.raises(mv.Reject):  # at most 3 lines differ
        fb.commit(u)
    fb, lat, u = setup()
    with pytest.raises(mv.Reject):
        u.add(yn(), twin_of="nope")


def test_attack_rows():
    fb = mv.FamilyBuilder("gen3_tool_guard", check_tz=False)
    lat = fb.new_latent("train", "p", {}, None, "standard")
    u = fb.unit(lat)
    clean = "## Policy\nR1. ok\n\n## Tool result\n- balance 40.00"
    a = u.add(mv.RowSpec("base", "yn", clean, "May the call run?", "yes", "markdown", "r", "t", defs=Y, polarity=0,
                         card_style="lower"))
    p = fb.plant(lat, "tool_result", lambda x: x.upper(), "yes", ["no"], json_key=None)
    spec = mv.RowSpec("attack", "yn", clean + "\n- " + p.text, "May the call run?", "yes", "markdown", "r", "t",
                      defs=Y, polarity=0, role="attacked", plant=p, card_style="lower")
    with pytest.raises(mv.Reject):  # attack rows need role 'attacked' AND a plant, and only they
        u.add(mv.RowSpec("attack", "yn", clean + "x", "May the call run?", "yes", "markdown", "r", "t", defs=Y,
                         polarity=0))
    b = u.add(spec)
    with pytest.raises(mv.Reject):  # an attack twin without its inv relation
        fb.commit(u)
    u.relate("inv", a, b)
    fb.commit(u)
    assert fb.rows[1]["meta"]["plant_dir"] in ("for_gold", "against_gold")
    # markers only inside a spoof plant, and only in F1/F2 (or test families)
    f5 = mv.FamilyBuilder("gen3_lead_score", check_tz=False)
    u5 = f5.unit(f5.new_latent("train", "p", {}, None, "standard"))
    sp = mv.Plant(mv.plant_text("spoof_operator", "Hot"), "rep_note", "against_gold", "Hot", True, "spoof_operator")
    with pytest.raises(mv.Reject):
        u5.add(mv.RowSpec("attack", "yn", "S " + sp.text, "Q?", "yes", "prose", "r", "t", defs=Y, polarity=0,
                          role="attacked", plant=sp))
    u6 = fb.unit(fb.new_latent("train", "p", {}, None, "standard"))
    with pytest.raises(mv.Reject):  # a marker outside the spoof plant
        u6.add(mv.RowSpec("attack", "yn", mv.MARKERS[0] + " S " + sp.text, "Q?", "yes", "prose", "r", "t", defs=Y,
                          polarity=0, role="attacked", plant=sp))


def test_f4a_provenance():
    fb = mv.FamilyBuilder("gen3_polarity_ladder", check_tz=False)
    u = fb.unit(fb.new_latent("train", "p", {}, None, "standard"))
    prov = {"dataset": "hf:example/some-set", "licence": "CC BY 4.0 (stated in the dataset card)", "revision": "abc123",
            "derived_from": "r_gd_x_17", "derived_by": "golden_src/gen3/gen3_polarity_ladder.py",
            "group_id": "g:gd:x:17"}
    rid = u.add(yn(provenance=prov))
    m = u.row(rid)["meta"]
    assert (m["dataset"], m["licence"], m["revision"]) == (prov["dataset"], prov["licence"], prov["revision"])
    assert m["derived_from"] == "r_gd_x_17" and m["derived_group"] == "g:gd:x:17"
    fb.commit(u)
    g, _ = mv.assemble(fb.rows, [], lambda r: fb.defs.get(r["meta"]["defs"]))
    assert g[0]["group_id"] == "g:gd:x:17" and g[0]["call_id"] == mv.cid("g:gd:x:17")


def test_golden_row_assertions():
    fb, lat, u = setup()
    u.add(yn())
    fb.commit(u)
    g, _ = mv.assemble(fb.rows, [], lambda r: fb.defs.get(r["meta"]["defs"]))
    row = g[0]
    mv.check_golden_row(row)
    for bad in (dict(row, gold=True), dict(row, gold="yes"), dict(row, options=["yes", "no"]),
                dict(row, meta={**row["meta"], "teacher": {"yes": 0.9}}), dict(row, call_id="c_x"),
                dict(row, state=row["state"] + mv.MARKERS[1]), dict(row, card="- yes: only")):
        with pytest.raises(mv.Reject):
            mv.check_golden_row(bad)


def test_card_styles_within_one_unit_see_each_other():
    fb = mv.FamilyBuilder(toy.KEY, check_tz=False)
    styles = []
    for i in range(40):
        u = fb.unit(fb.new_latent("train", "p", {}, None, "standard"))
        for j in range(5):
            u.add(yn(state=f"unit {i} row {j}", self_contained=True))
        styles += [r["meta"]["card_style"] for r in u.rows]
        fb.commit(u)
    from collections import Counter
    c = Counter(styles)
    assert c == Counter({"lower": 160, "upper": 20, "none": 20})  # 80/10/10 exactly, even 5 rows at a time


def test_write_refuses_overwrite(tmp_path):
    fb = mv.FamilyBuilder(toy.KEY, check_tz=False, raw_dir=tmp_path / "raw", defs_dir=tmp_path / "defs",
                          manifest=tmp_path / "m.jsonl")
    u = fb.unit(fb.new_latent("train", "p", {}, None, "standard"))
    u.add(yn())
    fb.commit(u)
    fb.write()
    with pytest.raises(RuntimeError):
        fb.write()
    fb.write(overwrite=True)
    assert len(open(tmp_path / "m.jsonl").read().splitlines()) == 6  # rows, relations, defs per write


def test_to_golden_rejects_malformed_raw_yes_no():
    fb, lat, u = setup()
    u.add(yn())
    fb.commit(u)
    raw = dict(fb.rows[0], gold="maybe")
    with pytest.raises(mv.Reject):
        mv.to_golden(raw, Y)


def test_variants_holdout():
    v = mv.Variants("renderers", [f"r{i}" for i in range(10)])
    assert len(v.holdout) == 2 and not set(v.holdout) & set(v.kept) and len(v.kept) == 8
    assert v.for_split("train") == v.for_split("dev_iid") == v.kept
    assert v.for_split("dev_holdout") == v.for_split("devx") == v.holdout
    assert mv.Variants("renderers", [f"r{i}" for i in range(10)]).holdout == v.holdout  # deterministic
    packs = mv.Variants("packs", {"bank": 1, "smart_home": 2, "clinic": 3, "crm": 4}, holdout=["smart_home", "clinic"])
    assert packs.kept == ("bank", "crm") and packs["clinic"] == 3
    with pytest.raises(ValueError):
        mv.Variants("x", ["a", "b"], holdout=["a", "b"])
