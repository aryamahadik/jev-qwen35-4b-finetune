"""F5 build (small plan): structure, labels, views, held-out composition, determinism, writing.

The full-size SPEC gates (balance, tiers, shortcuts <= 60%, artefact correlations, ...) run on the written files in
test_gen3_lead_score_written.py; here the checks that hold at any size are asserted.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict

from f5_helpers import SMALL_PLAN, g, mv, rows_json, small_build


def _rows(part=None):
    fb, _ = small_build()
    return fb.rows if part is None else fb.rows_for(part)


def test_counts_follow_the_plan():
    fb, b = small_build()
    for split, plan in SMALL_PLAN.items():
        for grp, n in plan.items():
            assert b.made[(split, grp)] == n, (split, grp)
    rows = fb.rows
    kinds = Counter((g.kind_of_row(r), r["meta"]["view"] == "attack") for r in rows if r["meta"]["dev_kind"] is None)
    assert kinds[("score", False)] == 160 and kinds[("ready", False)] == 24 and kinds[("judge", False)] == 24
    assert kinds[("jb", False)] == 16


def test_structure_cards_keysets_and_self_check():
    fb, _ = small_build()
    for part in ("train", "dev"):
        rows = fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rels = [x for x in fb.rels if x["a"] in rids and x["b"] in rids]
        rep = mv.run_checks(rows, rels)
        for k in ("structure", "keysets", "cards", "plants"):
            assert rep[k]["ok"], (part, k, rep[k])
        assert g.self_check_all(rows)["ok"]


def test_labels_equal_decide_on_the_stored_facts():
    fb, b = small_build()
    for r in fb.rows:
        f = b.row_facts[r["rid"]]
        kind = g.kind_of_row(r)
        gold, _ = g.decide(f, {"kind": kind})
        if kind == "jb":
            gold = r["options"][0] if gold == "yes" else r["options"][1]
        assert gold == r["gold"], r["rid"]


def test_every_base_row_has_a_trap_and_hard_rows_two():
    fb, _ = small_build()
    for r in fb.rows:
        m = r["meta"]
        if m["view"] != "base":
            continue
        real = {k: v for k, v in m["shortcut_hits"].items() if k != "trust_record"}
        wrong = sum(1 for v in real.values() if v == 0)
        assert wrong >= 1, r["rid"]
        if m["tier"] == "hard":
            assert wrong >= 2
        if m["tier"] in ("easy", "standard"):
            assert wrong == 1


def test_yes_no_units_are_balanced_pairs():
    fb, _ = small_build()
    by = defaultdict(list)
    for r in fb.rows:
        if r["meta"]["qkind"] in ("yn", "jb"):
            by[r["meta"]["latent_id"]].append(r)
    for lid, rs in by.items():
        ys = [mv._yes(r) for r in rs]
        assert sum(ys) * 2 == len(ys), lid                     # every unit adds as many yes rows as no rows
        views = Counter(r["meta"]["view"] for r in rs)
        assert views["base"] == 1 and views["contrast"] == 1


def test_twins_flip_and_change_at_most_three_lines():
    fb, _ = small_build()
    by = {r["rid"]: r for r in fb.rows}
    n = 0
    for r in fb.rows:
        t = r["meta"]["twin_of"]
        if t:
            n += 1
            assert by[t]["gold"] != r["gold"] and by[t]["instructions"] == r["instructions"]
            assert by[t]["options"] == r["options"] and mv.diff_lines(by[t]["state"], r["state"]) <= 3
    assert n > 50


def test_attack_twins_keep_gold_and_plant_only_in_untrusted_fields():
    fb, _ = small_build()
    by = {r["rid"]: r for r in fb.rows}
    inv = [x for x in fb.rels if x["type"] == "inv"]
    assert inv
    for x in inv:
        a, b_ = by[x["a"]], by[x["b"]]
        assert a["gold"] == b_["gold"] and b_["meta"]["role"] == "attacked"
        assert b_["meta"]["plant_channel"] in ("rep_note", "email", "log_note", "tool_result")
        assert not b_["meta"]["plant_spoof"]
    fams = Counter(by[x["b"]]["meta"]["plant_dir"] for x in inv)
    assert abs(fams["for_gold"] - fams["against_gold"]) <= 2


def test_dev_holdout_is_held_out_everywhere():
    fb, b = small_build()
    ho = [r for r in fb.rows if r["meta"]["dev_kind"] == "holdout"]
    tr = [r for r in fb.rows if r["meta"]["dev_kind"] is None]
    assert ho
    assert {b.facts[r["meta"]["latent_id"]]["arch"] for r in ho} == {"weighted"}
    assert {r["meta"]["pack"] for r in ho} <= set(g.HOLDOUT_PACKS)
    assert not {r["meta"]["pack"] for r in tr} & set(g.HOLDOUT_PACKS)
    assert not {r["meta"]["tpl"] for r in ho} & {r["meta"]["tpl"] for r in tr}
    assert not {r["instructions"] for r in ho if r["meta"]["qkind"] != "yn" or not r["meta"]["judge"]} & {
        r["instructions"] for r in tr}
    tr_levels = {tuple(b.facts[r["meta"]["latent_id"]]["rub"]["levels"]) for r in tr}
    assert not {tuple(b.facts[r["meta"]["latent_id"]]["rub"]["levels"]) for r in ho} & tr_levels
    assert {b.facts[r["meta"]["latent_id"]]["arch"] for r in tr} == {"points", "bant", "gated"}


def test_name_pools_are_disjoint_across_splits():
    fb, b = small_build()
    names = defaultdict(set)
    for lid, f in b.facts.items():
        split = {"tr": "train", "di": "dev_iid", "dh": "dev_holdout"}[lid.split("-")[1]]
        L = f["lead"]
        for c in (L["primary"], L["secondary"]):
            if c:
                names[split] |= set(c["name"].split())
        names[split] |= set(L["owner"].split())
    for s1 in names:
        for s2 in names:
            if s1 < s2:
                assert not names[s1] & names[s2], (s1, s2)
    for s, ns in names.items():
        assert all(mv.name_split(n) == s for n in ns)


def test_raw_rows_meet_the_golden_raw_format():
    for r in _rows():
        assert set(r) == {"key", "rid", "state", "instructions", "options", "gold", "soft", "meta"}
        assert r["key"] == g.KEY and r["soft"] is None and r["meta"]["split"] == "train"
        assert r["meta"]["dataset"] == "program generator golden_src/gen3/gen3_lead_score.py"
        assert r["meta"]["licence"] == mv.LICENCE and "teacher" not in r["meta"]
        if r["meta"]["qkind"] == "yn":
            assert r["options"] == ["yes", "no"] and r["gold"] in ("yes", "no")
        if r["meta"]["qkind"] == "score":
            assert r["meta"]["levels"] == len(r["options"]) and 3 <= len(r["options"]) <= 6
        if r["meta"]["judge"]:
            assert not mv.judge_violations(r["instructions"])


def test_determinism_and_write(tmp_path):
    fb, _ = small_build("a")
    fb2, _ = small_build("b")                                  # a second, independent build
    assert rows_json(fb.rows) == rows_json(fb2.rows)
    assert json.dumps(fb.rels) == json.dumps(fb2.rels)
    old = (fb2.raw_dir, fb2.defs_dir, fb2.manifest)
    fb2.raw_dir, fb2.defs_dir, fb2.manifest = tmp_path / "raw", tmp_path / "defs", tmp_path / "MANIFEST_yn2b.jsonl"
    try:
        out = fb2.write(parts=("train", "dev"))
    finally:
        fb2.raw_dir, fb2.defs_dir, fb2.manifest = old
    rows, rels = mv.read_raw(g.KEY, "train", tmp_path / "raw")
    assert rows_json(rows) == rows_json(fb.rows_for("train"))
    man = [json.loads(x) for x in (tmp_path / "MANIFEST_yn2b.jsonl").read_text().splitlines()]
    assert {m["sha256"] for m in man} >= {v for k, v in out.items() if k.endswith(".jsonl")}
    assert (tmp_path / "raw" / "dev" / f"{g.KEY}.jsonl").exists()


def test_sample_latents_for_devx():
    xs = g.sample_latents("devx", plan={"score": 8, "ready": 2, "judge": 2, "jb": 2})
    assert xs and {x["facts"]["arch"] for x in xs} == {"weighted"}
    assert {x["facts"]["pack"] for x in xs} <= set(g.HOLDOUT_PACKS)
    for x in xs:
        assert x["latent_id"].startswith("f5-dx-")
        assert g.decide(x["facts"], x["query"])[0] == x["gold"]
        json.dumps(x["facts"])


def test_exception_group_tags_match_the_override_outcome():
    """SPEC 4.6 three equal exception groups: a base row carries exc:* only when its rubric has an override, and the
    tag names what the override did (lowered = allow_deny, raised = deny_allow, condition not met = near_miss)."""
    fb, b = small_build()
    for r in fb.rows:
        tags = [t for t in (r["meta"]["edge"] or "").split(",") if t.startswith("exc:")]
        if r["meta"]["view"] != "base":
            assert not tags
            continue
        f = b.row_facts[r["rid"]]
        o = f["rub"].get("override")
        if not tags:
            continue
        assert o is not None, r["rid"]
        res = g.evaluate(f)
        assert not res["dq"]
        ov = res["comps"]["override"]
        cond = (not res["counted"]["budget_met"]) if o["kind"] == "ceiling" else res["counted"]["demo"]
        want = g.EXC_GROUP[ov] if ov else ("exc:near_miss" if not cond else None)
        assert tags == [want], (r["rid"], tags, want)
