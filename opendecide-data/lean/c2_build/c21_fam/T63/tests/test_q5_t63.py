"""Opus rulings Q5 and Q7 (18 Oct 2026), recorded before any pool rows. Q5: the hashed Opus table has only 40 INCOMPATIBLE cells and a cell is used once, so LIC = 110 kept rows
(COMPATIBLE 38 / REVIEW 38 / INCOMPATIBLE 34; at most 44 / 44 / 40 cells drawn), the freed 90 rows go to NEAR (550) and EX-A (290: EX-A1 160, EX-A2 130), EX-B stays 250,
the family stays 1,200, the pilot is 600 = NEAR 275 / EX-A 145 / EX-B 125 / LIC 55. No bar changes.

The dry run below uses the REAL hashed table (zed_orch/c21/l0/T63_LIC_TABLE.json) with stand-in plumbing (fixture export, test-double stamp, test wording pool): it proves the
LIC rows build; it is not a production row set."""
import collections
import copy
import json
import os
import random

import pytest

from LP_COMMON import pipeline as pl
from LP_COMMON import gates as LG
from LP_COMMON import wording
from T63 import checked, config as C, dryrun, gates, generator as G, lic, lic_format as LF, near_plan, pool_writer as PW, roundtrip as RT, rows as ROWS

REAL_SHA = "81fe96f7c803da485fa26d1f1664dac626d0b53ed09755249daa5603113228eb"
FAMDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_P = PW.source_paths()
HAVE_REAL = os.path.isfile(_P["lic_table"]) and os.path.isfile(_P["lic_table_record"])
real_only = pytest.mark.skipif(not HAVE_REAL, reason="the real hashed licence table is not in the L-0 folder")


# ------------------------------------------------------------------------------------------------------------ design values
def test_design_values_are_the_ruling_and_the_family_stays_1200():
    assert C.BLOCK_ROWS == {"NEAR": 550, "EX-A1": 160, "EX-A2": 130, "EX-B": 250, "LIC": 110}
    assert sum(C.BLOCK_ROWS.values()) == C.GENERATED_ROWS == 1200
    assert C.LIC_ROWS == {"COMPATIBLE": 38, "REVIEW": 38, "INCOMPATIBLE": 34} and sum(C.LIC_ROWS.values()) == C.BLOCK_ROWS["LIC"]
    assert C.LIC_DRAW == {"COMPATIBLE": 44, "REVIEW": 44, "INCOMPATIBLE": 40}
    assert C.PILOT_ROWS == {"NEAR": 275, "EX-A": 145, "EX-B": 125, "LIC": 55} and sum(C.PILOT_ROWS.values()) == 600
    sh = {k: v / 110.0 for k, v in C.LIC_ROWS.items()}
    assert all(0.30 <= v <= 0.40 for v in sh.values())                   # K10 label shares (30.9 / 34.5 / 34.5%)
    assert (C.LIC_ROWS["INCOMPATIBLE"] - 1) / (110 - 1) >= 0.30          # one INCOMPATIBLE shortfall beyond the spare cells still passes K10 (33/109)


def _sizes(plan):
    out = collections.Counter()
    for g in plan:
        if g["head"] == "EXISTS":
            out[g["cell"]["sub"]] += g["size"]
        else:
            out[g["head"]] += g["size"]
    return out


def test_plan_sizes_full_and_pilot():
    full = _sizes(G.build_plan(total=1200, seed=2, oversample=False))
    assert (full["NEAR"], full["EX-A1"], full["EX-A2"], full["EX-B1"] + full["EX-B2"], full["LIC"]) == (550, 160, 130, 250, 110)
    pil = _sizes(G.build_plan(total=600, seed=2, oversample=False))
    assert (pil["NEAR"], pil["EX-A1"] + pil["EX-A2"], pil["EX-B1"] + pil["EX-B2"], pil["LIC"]) == (275, 145, 125, 55)


def test_lic_plan_draws_at_most_44_44_40_cells_and_at_least_33_pair_rows():
    q = G.lic_quota(1200)
    assert q["kept"] == C.LIC_ROWS and q["draw"] == C.LIC_DRAW and q["pairs_kept"] == 17 and q["pairs"] == 20
    for over, want in ((True, C.LIC_DRAW), (False, C.LIC_ROWS)):
        plan = [g for g in G.build_plan(total=1200, seed=4, oversample=over) if g["head"] == "LIC"]
        lab, pair_rows = collections.Counter(), 0
        for g in plan:
            c = g["cell"]
            if c["type"] == "pair":
                lab.update(c["labels"])
                pair_rows += 2
            else:
                lab[c["label"]] += 1
        assert dict(lab) == dict(want)
        assert pair_rows >= 33                                                           # >= 30% of the 110 kept rows in one-axis-flip pairs
        assert sum(1 for g in plan if g["cell"]["type"] == "pair") >= 17
        assert [g["size"] for g in plan] == sorted((g["size"] for g in plan), reverse=True)     # pairs before singles (the last INCOMPATIBLE cells go to singles)
    # the mode-flip share of the planned pairs (K10 axis-reading >= 50%)
    pairs = [g["cell"] for g in G.build_plan(total=1200, seed=4) if g["head"] == "LIC" and g["cell"]["type"] == "pair"]
    assert sum(1 for c in pairs if c["axis"] == "mode") / len(pairs) >= 0.5


def test_lic_never_asks_for_more_cells_than_the_table_has():
    for seed in range(5):
        for total in (60, 300, 600, 1200):
            lab = collections.Counter()
            for g in G.build_plan(total=total, seed=seed):
                if g["head"] == "LIC":
                    c = g["cell"]
                    lab.update(c["labels"] if c["type"] == "pair" else [c["label"]])
            assert lab["INCOMPATIBLE"] <= 40 and lab["COMPATIBLE"] <= 44 and lab["REVIEW"] <= 44


def test_near_550_keeps_the_k13_shares():
    g = near_plan.GROUPS_550
    assert 2 * (g["pair_a"] + g["yes_flip"] + g["t8_flip"]) + g["single_yes"] + g["single_no"] == 550
    yes = g["pair_a"] + g["yes_flip"] + g["t8_flip"] + g["single_yes"]
    no = g["pair_a"] + g["yes_flip"] + g["t8_flip"] + g["single_no"]
    assert yes == no == 275
    t17 = g["pair_a"] + g["yes_flip"] + g["single_yes"]
    assert 0.05 <= t17 / 7.0 / yes <= 0.25 and 0.05 <= g["t8_flip"] / yes <= 0.25      # NM-T1..T7 at 12% each, NM-T8 at 16%
    assert (2 * (g["pair_a"] + g["yes_flip"] + g["t8_flip"])) / 550 >= C.PAIR_FLOOR["NEAR"]
    plan = [x for x in G.build_plan(total=1200, seed=3, oversample=False) if x["head"] == "NEAR"]
    r4 = sum(1 for x in plan if x["cell"].get("no_kind") == "NM-R4")
    assert r4 / 275.0 <= C.NM_R4_MAX and 1 - r4 / 275.0 >= C.NO_NEAR_MIN


def test_ex_a_is_160_130_balanced_with_n_kind_shares_inside_the_bars():
    plan = [g for g in G.build_plan(total=1200, seed=3, oversample=False) if g["head"] == "EXISTS" and g["cell"]["sub"] in ("EX-A1", "EX-A2")]
    for sub, n in (("EX-A1", 160), ("EX-A2", 130)):
        rows = [(g["cell"]["label"], g["cell"]["kind"], g["size"]) for g in plan if g["cell"]["sub"] == sub]
        assert sum(s for _l, _k, s in rows) == n
        yes = sum(1 for g in plan if g["cell"]["sub"] == sub and g["cell"]["label"] == "YES") + sum(1 for g in plan if g["cell"]["sub"] == sub and g["cell"].get("pair"))
        assert yes == n // 2                                                             # YES = NO (pairs hold one of each)
        kinds = collections.Counter()
        for g in plan:
            if g["cell"]["sub"] == sub and g["cell"]["label"] == "NO":
                kinds[g["cell"]["kind"]] += 1
        no = n // 2
        assert sum(kinds.values()) == no
        for k in C.EX_N_DEFINED[sub]:
            assert kinds[k] / no >= C.EX_N_MIN - 1e-9 and kinds[k] / no <= C.EX_N_MAX, (sub, k)
        assert kinds["EX-N4"] / no <= C.EX_N4_MAX


# ---------------------------------------------------------------------------------------- the REAL table: LIC rows must build
@pytest.fixture(scope="module")
def real_dry():
    tb = lic.LicTable.load(_P["lic_table"])
    rec = json.load(open(_P["lic_table_record"]))
    rows, summary, log, _r = checked.run(1200, 11, pl.TestDoubleHook(), standin=True, exports=dryrun.fixture_exports(), table=tb)
    return tb, rec, rows, summary


@real_only
def test_the_real_table_is_the_recorded_one(real_dry):
    tb, rec, _rows, _s = real_dry
    assert tb.sha == rec["sha256"] == REAL_SHA and tb.fixture is False
    PW.check_table_binding(tb, rec)
    assert collections.Counter(tb.cells.values()) == {"COMPATIBLE": 1550, "REVIEW": 330, "INCOMPATIBLE": 40}


@real_only
def test_lic_rows_build_on_the_real_table_with_all_40_incompatible_cells_once(real_dry):
    tb, _rec, rows, summary = real_dry
    L = [r for r in rows if r["head"] == "LIC"]
    assert summary["dropped"] == {} and len(L) == 128
    assert collections.Counter(r["gold"] for r in L) == {"COMPATIBLE": 44, "REVIEW": 44, "INCOMPATIBLE": 40}
    cells = [(r["spec"]["dep"], r["spec"]["project"], r["spec"]["use"], r["spec"]["dist"]) for r in L]
    assert len(set(cells)) == len(cells)                                                 # each cell once
    assert {c for c, r in zip(cells, L) if r["gold"] == "INCOMPATIBLE"} == {tuple(k.split("|")) for k, v in tb.cells.items() if v == "INCOMPATIBLE"}
    for r, c in zip(L, cells):
        assert r["spec"]["table_sha"] == r["witness_inputs"]["table_sha"] == REAL_SHA
        assert r["meta"]["construction_id"] == "LC:" + lic.key(*c) and r["gold"] == tb.label(*c)


@real_only
def test_k10_on_the_real_table_dry_run(real_dry):
    _tb, _rec, rows, _s = real_dry
    k10 = gates.k10_lic(rows)
    assert k10["ok"] and k10["each_cell_once"] and k10["table_sha_unique"]
    assert all(0.30 <= v <= 0.40 for v in k10["label_shares"].values())
    assert k10["axis_flip_mode_share"] >= C.LIC_AXIS_FLIP_MIN and k10["mixed_pair_share"] >= C.LIC_MIXED_PAIR_MIN
    assert k10["pair_share"] >= C.LIC_PAIR_MIN
    assert gates.k7_pairs(rows)["heads"]["LIC"] >= C.PAIR_FLOOR["LIC"]
    # the format-only probe runs (wording id, option order, token count; no licence id). At n ~ 110-128 its 97.5th-percentile bar (<= 39.3%) is mostly beyond reach even with
    # shuffled labels (reported, not tuned): here we only check that it is computed and uses no licence axis.
    fp = gates.k10_format_probe(rows)
    assert fp["id"] == "T63-K10:format" and fp["n"] == 128 and 0.0 <= fp["bal_acc"] <= 1.0


@real_only
def test_real_lic_rows_pass_the_pool_writer_when_stamped_and_bound(real_dry, tmp_path):
    tb, rec, rows, _s = real_dry
    L = copy.deepcopy([r for r in rows if r["head"] == "LIC"])
    for r in L:
        r["stamp"]["registry_sha"], r["stamp"]["method_set_version"] = "a" * 64, "unit-test-ms"
    res = PW.write_pool(L, str(tmp_path / "lic.jsonl"), standin=False, sources={"table": tb, "table_record": rec})
    assert res["lic_rows"] == 128 and res["table_sha"] == REAL_SHA


# ------------------------------------------------------------------------------------------------------------------ README
def test_readme_records_ruling_q5():
    txt = open(os.path.join(FAMDIR, "README.md"), encoding="utf-8").read()
    assert "Opus ruling Q5, before any pool rows" in txt and "COMPATIBLE 38 / REVIEW 38 / INCOMPATIBLE 34" in txt and REAL_SHA in txt
    assert "NEAR 550" in txt and "EX-A1 160" in txt and "EX-A2 130" in txt and "NEAR 275 / EX-A 145 / EX-B 125 / LIC 55" in txt


# ============================================================================================ Q5: the downstream cut (drawn rows -> kept 110)
def _population(seed=0):
    """128 LIC rows as the plan draws them at 1,200: 20 pairs (7 C-R, 7 R-I, 6 C-I) + singles C 31 / R 30 / I 27."""
    rows, k = [], 0

    def add(label, pid=None):
        nonlocal k
        k += 1
        rows.append({"row_id": "T63-LIC-%04d-%s" % (k, "ab"[len([r for r in rows if r["meta"]["pair_id"] == pid and pid]) if pid else 0]), "gold": label,
                     "meta": {"pair_id": pid}, "rendered": {"text": "text %d" % k}, "spec": {"dep": "MIT"}})

    for i, (a, b) in enumerate([("COMPATIBLE", "REVIEW")] * 7 + [("REVIEW", "INCOMPATIBLE")] * 7 + [("COMPATIBLE", "INCOMPATIBLE")] * 6):
        add(a, "P%02d" % i)
        add(b, "P%02d" % i)
    for lab, n in (("COMPATIBLE", 31), ("REVIEW", 30), ("INCOMPATIBLE", 27)):
        for _ in range(n):
            add(lab)
    random.Random(seed).shuffle(rows)
    return rows


def test_cut_takes_128_to_110_dropping_singles_only():
    pop = _population()
    assert len(pop) == 128
    kept, rep = lic.cut_to_quota(pop, seed=11)
    assert collections.Counter(r["gold"] for r in kept) == C.LIC_ROWS and len(kept) == 110
    gone = set(rep["dropped"])
    assert len(gone) == 18 and all(not r["meta"]["pair_id"] for r in pop if r["row_id"] in gone)         # singles first: every pair survives
    assert rep["pair_rows"] == 40 and rep["pair_ok"] and rep["pair_rows"] >= 33 and [r["row_id"] for r in kept] == [r["row_id"] for r in pop if r["row_id"] not in gone]


def test_cut_is_deterministic_per_seed_and_blind_to_everything_but_the_ids():
    pop = _population()
    a = lic.cut_to_quota(pop, 5)[1]["dropped"]
    assert a == lic.cut_to_quota(pop, 5)[1]["dropped"] and a != lic.cut_to_quota(pop, 6)[1]["dropped"]
    shuffled = copy.deepcopy(pop)
    random.Random(3).shuffle(shuffled)
    assert set(lic.cut_to_quota(shuffled, 5)[1]["dropped"]) == set(a)                                 # input order does not matter
    blind = copy.deepcopy(pop)
    for r in blind:                                                                                    # row text, spec, score-like fields: none is read
        r["rendered"] = {"text": "zzz"}
        r["spec"] = {"dep": "GPL-3.0-only", "score": random.random()}
        r["meta"]["tokens"], r["meta"]["wording_id"], r["score"] = 1, "w999", random.random()
    assert set(lic.cut_to_quota(blind, 5)[1]["dropped"]) == set(a)
    src = open(os.path.join(FAMDIR, "lic.py"), encoding="utf-8").read()
    body = src[src.index("def cut_to_quota"):]
    assert "rendered" not in body.split('"""')[2] and "spec" not in body.split('"""')[2] and "score" not in body.split('"""')[2]


def test_cut_leaves_a_label_under_quota_alone_and_falls_back_to_pair_members_only_when_it_must():
    pop = [r for r in _population() if not (r["gold"] == "INCOMPATIBLE" and not r["meta"]["pair_id"])]
    inc = sum(1 for r in pop if r["gold"] == "INCOMPATIBLE")
    kept, rep = lic.cut_to_quota(pop, 1)
    assert collections.Counter(r["gold"] for r in kept)["INCOMPATIBLE"] == inc <= 34                  # under quota: nothing cut
    # a label whose only surplus rows are paired: pair members go (their partner is then a single)
    pairs_only = [r for r in pop if r["meta"]["pair_id"]]
    q = {"COMPATIBLE": 8, "REVIEW": 8, "INCOMPATIBLE": 8}
    kept, rep = lic.cut_to_quota(pairs_only, 2, quota=q, min_pair_rows=33)
    cnt = collections.Counter(r["gold"] for r in kept)
    assert all(cnt[k] <= 8 for k in q) and len(rep["dropped"]) == len(pairs_only) - len(kept) and rep["pair_ok"] is False
    assert lic.cut_to_quota([], 1)[0] == []


def test_cut_lic_wrapper_keeps_other_heads_and_scales_to_the_pilot():
    pop = _population()
    other = [{"row_id": "N-1", "head": "NEAR", "gold": "YES", "meta": {"pair_id": None}}]
    full = [dict(r, head="LIC") for r in pop] + other
    out, rep = checked.cut_lic(full, seed=4, total=1200)
    assert sum(1 for r in out if r["head"] == "LIC") == 110 and other[0] in out
    out, rep = checked.cut_lic(full, seed=4, total=600)
    assert collections.Counter(r["gold"] for r in out if r["head"] == "LIC") == {"COMPATIBLE": 19, "REVIEW": 19, "INCOMPATIBLE": 17}


@real_only
def test_real_table_dry_run_cut_gives_110_with_pairs_and_k10_inside_the_bars(real_dry):
    tb, rec, rows, _s = real_dry
    out, rep = checked.cut_lic(rows, 11, total=1200)
    L = [r for r in out if r["head"] == "LIC"]
    assert collections.Counter(r["gold"] for r in L) == C.LIC_ROWS and rep["pair_ok"] and rep["pair_rows"] >= 33
    k10 = gates.k10_lic(out)
    assert k10["ok"] and all(0.30 <= v <= 0.40 for v in k10["label_shares"].values()) and k10["pair_share"] >= 0.30


# ================================================================================ Q5: a dropped row's cell is released inside the run
def test_picker_releases_only_unkept_rows_of_earlier_rounds():
    import random as _r
    tb = lic.fixture_table()
    pk = lic.CellPicker(tb, _r.Random(1))
    c0, c1, c2 = (pk.single("INCOMPATIBLE") for _ in range(3))
    pk.register("r0", "g0", c0, 0)
    pk.register("r1", "g1", c1, 0)
    pk.register("r2", "g2", c2, 1)                                    # a row of the CURRENT round (pending, not stamped yet)
    assert pk.release_unkept({"r1"}, before_round=1) == 1             # r0 dropped (earlier round, not kept); r1 kept; r2 is pending
    assert c0 not in pk.used and c1 in pk.used and c2 in pk.used
    assert pk.release_unkept({"r1"}, before_round=2) == 1 and c2 not in pk.used
    freed = {c0, c2}
    drawn = {pk.single("INCOMPATIBLE") for _ in range(len(pk._by_label["INCOMPATIBLE"]) - 1)}      # draw every unused INCOMPATIBLE cell: the two freed ones are among them, once
    assert freed <= drawn and c1 not in drawn and len(pk.used) == len(pk._by_label["INCOMPATIBLE"])


def test_a_builder_error_after_the_draw_gives_the_cell_back():
    tb = lic.fixture_table()
    ctx = G.Ctx(seed=1, standin=True, table=tb)
    g = {"gid": "T63-LIC-9999", "seed": "lic-9999", "size": 1, "head": "LIC", "cell": {"type": "single", "label": "COMPATIBLE", "target_level": "L1", "mixed": False}}
    boom = ROWS.build_record
    try:
        ROWS.build_record = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom"))
        with pytest.raises(RuntimeError):
            G.generate_group(ctx, g)
    finally:
        ROWS.build_record = boom
    assert not ctx.cells.used


@real_only
def test_lost_incompatible_rows_get_their_cell_back_and_all_40_are_used_once(monkeypatch):
    tb = lic.LicTable.load(_P["lic_table"])
    seed = 11
    plan = G.build_plan(total=1200, seed=seed)
    singles = [g for g in plan if g["head"] == "LIC" and g["cell"]["type"] == "single" and g["cell"]["label"] == "INCOMPATIBLE"]
    answer_drop, g13_hit = singles[0]["gid"] + "-a", singles[1]["gid"] + "-a"
    real_check = RT.check
    monkeypatch.setattr(RT, "check", lambda rec: ["forced"] if rec["row_id"] == answer_drop else real_check(rec))

    def run():
        hook = pl.TestDoubleHook(hit_if=lambda it: it["row_id"] == g13_hit)
        return checked.run(1200, seed, hook, standin=True, exports=dryrun.fixture_exports(), table=tb)

    rows, summary, _l, _r = run()
    inc = [r for r in rows if r["head"] == "LIC" and r["gold"] == "INCOMPATIBLE"]
    cells = [(r["spec"]["dep"], r["spec"]["project"], r["spec"]["use"], r["spec"]["dist"]) for r in inc]
    assert answer_drop not in {r["row_id"] for r in rows} and g13_hit not in {r["row_id"] for r in rows}
    assert summary["retired_groups"] >= 1 and len(inc) == 40 and len(set(cells)) == 40                 # both lost groups were refilled with a released cell
    monkeypatch.setattr(lic.CellPicker, "release_unkept", lambda self, kept, before_round: 0)           # the old behaviour
    rows2 = run()[0]
    assert sum(1 for r in rows2 if r["head"] == "LIC" and r["gold"] == "INCOMPATIBLE") == 38


# ======================================================================================= Q7a: the K10 format-only probe and the format assignment
def _fam_lic(rows, total=1200):
    return [r for r in rows if r["head"] == "LIC"]


def test_wording_is_a_seeded_random_draw_that_ignores_the_label_within_the_k14_cap():
    """Opus ruling Q7a follow-up: 'label-blind' = a seeded random draw of the wording id that never sees the label (a cycle or Latin square builds an anti-correlation)."""
    src = open(os.path.join(FAMDIR, "rows.py"), encoding="utf-8").read()
    assert "render_cycle" not in src and "StratPicker" not in src
    ctx = G.Ctx(seed=1, standin=True, table=lic.fixture_table())
    assert type(ctx.picker) is wording.Picker
    plan = [g for g in G.build_plan(total=600, seed=3, oversample=False) if g["head"] == "LIC" and g["cell"]["type"] == "single"]
    rot = {"COMPATIBLE": "REVIEW", "REVIEW": "INCOMPATIBLE", "INCOMPATIBLE": "COMPATIBLE"}

    def wids(groups):
        c = G.Ctx(seed=1, standin=True, table=lic.fixture_table())
        return [r["meta"]["wording_id"] for g in groups for r in G.generate_group(c, g)]

    same = wids(plan)
    rotated = wids([dict(g, cell=dict(g["cell"], label=rot[g["cell"]["label"]])) for g in plan])
    assert same == rotated and len(same) == len(plan) > 20                               # permute the labels: the wording ids do not move
    assert wids(plan) == same                                                            # seeded: reproducible
    other = G.Ctx(seed=2, standin=True, table=lic.fixture_table())
    assert [r["meta"]["wording_id"] for g in plan for r in G.generate_group(other, g)] != same        # and the seed does change the draw
    # K14 cap: with W wordings each round of the draw uses every wording once, so a wording is used at most ceil(n / W) times; the cap on the KEPT rows is ceil(n_kept / 50)
    for W, n_draw, n_kept in ((57, 128, 110), (57, 64, 55), (50, 128, 110), (50, 64, 55)):
        use = collections.Counter(LF.draw(5, i, W, C.LIC_LABELS)["word_index"] for i in range(n_draw))
        assert max(use.values()) == -(-n_draw // W) <= -(-n_kept // 50)


@real_only
def test_family_lic_rows_meet_the_k14_wording_cap_and_carry_the_constant_format_fields(real_dry):
    _tb, _rec, rows, _s = real_dry
    out, _rep = checked.cut_lic(rows, 11, total=1200)
    for sel in (_fam_lic(rows), _fam_lic(out)):
        assert LG.wording_variety(sel)["ok"]
        assert all(r["meta"]["card_layout"] == C.LIC_CARD_LAYOUT and r["meta"]["field_order"] == C.LIC_FIELD_ORDER for r in sel)


@real_only
def test_k10_format_probe_is_report_only_with_exactly_the_k10_features_and_the_noise_ub(real_dry):
    _tb, _rec, rows, _s = real_dry
    out, _rep = checked.cut_lic(rows, 11, total=1200)
    res = gates.k10_format_probe(out, B=200)
    assert res["features"] == ["wording_id", "card_layout", "field_order"] and res["n"] == 110 and res["report_only"] is True and res["ok"] is True      # never a kill
    assert res["status"] in ("PASS", "FAIL", "INVALID") and res["valid"] == (res["status"] != "INVALID") and res["harness_pass"] == (res["status"] == "PASS")
    assert {"perm_bal_acc", "leak_bal_acc", "bal_acc", "upper"} <= set(res) and res["noise"]["n"] == 110 and res["noise"]["ub_median"] > 0.39      # the noise ub sits above the 39.3% bar
    if res["valid"]:
        assert res["leak_bal_acc"] >= 0.80 and abs(res["perm_bal_acc"] - 1 / 3.0) <= 0.03
    # token count, option order, gold letter, licence ids, usage and distribution are not features: changing them changes nothing
    L = [r for r in out if r["head"] == "LIC"]
    alt = copy.deepcopy(L)
    for r in alt:
        r["meta"]["tokens"] = random.randint(1, 999)
        r["options"] = list(reversed(r["options"]))
        r["gold_letter"] = "Z"
        r["spec"].update(dep="GPL-3.0-only", project="MIT", use="LC-USE-1", dist="LC-DIST-3")
        r["rendered"] = {"text": "licence ids differ"}
    assert gates.k10_format_probe(alt, B=200) == gates.k10_format_probe(L, B=200)


def test_k10_format_probe_still_sees_a_planted_format_leak_but_never_kills():
    rows = []
    for i in range(120):
        lab = C.LIC_LABELS[i % 3]
        rows.append({"head": "LIC", "gold": lab, "group_id": "G%03d" % i, "meta": {"wording_id": "w%02d" % (i % 3 * 5 + (i // 3) % 5), "card_layout": "L", "field_order": "O"}})
    res = gates.k10_format_probe(rows, B=100)
    assert res["harness_pass"] is False and res["bal_acc"] > 0.9 and res["ok"] is True and res["report_only"] is True
    assert gates.k10_format_probe(rows[:10])["skipped"] == 10


# ==================================================================================================================== Q7b: K10-F construction assert
def _fingerprint(recs):
    return {r["row_id"]: json.dumps([r["meta"]["lic_format"], r["meta"]["wording_id"], r["meta"]["template_id"], r["meta"]["card_layout"], r["meta"]["field_order"],
                                      [o["label"] for o in r["options"]], r["rendered"]["question"].split(" ")[0]], sort_keys=True) for r in recs}


def test_lic_format_draw_is_a_pure_function_of_seed_and_index_and_the_static_check_bites(monkeypatch):
    assert LF.static_problems() == [] and tuple(LF.inspect.signature(LF.draw).parameters) == LF.DRAW_PARAMS
    a = LF.draw(7, 31, 57, C.LIC_LABELS)
    assert a == LF.draw(7, 31, 57, C.LIC_LABELS) and a != LF.draw(8, 31, 57, C.LIC_LABELS) and sorted(a["option_order"]) == sorted(C.LIC_LABELS)
    assert a["template_id"] == C.LIC_TEMPLATE_ID == "t63.lic.v1" and a["card_layout"] == C.LIC_CARD_LAYOUT and a["field_order"] == C.LIC_FIELD_ORDER
    src = LF.inspect.getsource(LF)
    for bad_src in (src.replace("n_wordings, vocab):", "n_wordings, vocab, label):"), src.replace('order = list(vocab)', 'order = list(vocab); gold = spec'),
                    src.replace('"option-order", index)', '"option-order", index, cell)')):
        monkeypatch.setattr(LF.inspect, "getsource", lambda _m, _s=bad_src: _s)
        assert LF.static_problems(), "the static check missed a label / cell input"
    monkeypatch.undo()
    assert LF.static_problems() == []
    # row index = a place in the block: each wording once per round, so the K14 cap is built in
    assert sorted(LF.draw(3, i, 57, C.LIC_LABELS)["word_index"] for i in range(57)) == list(range(57))


def test_formats_are_byte_identical_when_labels_are_permuted_or_cells_swapped():
    plan = [g for g in G.build_plan(total=600, seed=3, oversample=False) if g["head"] == "LIC"]
    rot = {"COMPATIBLE": "REVIEW", "REVIEW": "INCOMPATIBLE", "INCOMPATIBLE": "COMPATIBLE"}

    def build(groups, table):
        ctx = G.Ctx(seed=3, standin=True, table=table)
        return [r for g in groups for r in G.generate_group(ctx, g)]

    def permuted(g):
        c = dict(g["cell"])
        if c["type"] == "pair":
            c["labels"] = [rot[x] for x in c["labels"]]
        else:
            c["label"] = rot[c["label"]]
        return dict(g, cell=c)

    base = build(plan, lic.fixture_table())
    perm = build([permuted(g) for g in plan], lic.fixture_table())
    swap = build(plan, lic.fixture_table("another-table"))
    fb = _fingerprint(base)
    assert len(fb) == len(base) == len(perm) == len(swap) and len(fb) > 40
    assert _fingerprint(perm) == fb and _fingerprint(swap) == fb                         # byte-identical formats
    # while the labels and the licence cells really did change
    assert [r["gold"] for r in perm] != [r["gold"] for r in base]
    assert [(r["spec"]["dep"], r["spec"]["project"], r["spec"]["use"], r["spec"]["dist"]) for r in swap] != [(r["spec"]["dep"], r["spec"]["project"], r["spec"]["use"], r["spec"]["dist"]) for r in base]


@real_only
def test_k10_f_replays_exactly_on_100_percent_of_the_built_rows(real_dry):
    _tb, _rec, rows, _s = real_dry
    out, _rep = checked.cut_lic(rows, 11, total=1200)
    for sel in (rows, out):
        res = gates.k10_f_construction(sel)
        assert res["ok"] and res["rows"] in (128, 110) and res["replay_failures"] == 0 and res["layout_order_single_valued"] and res["k14_cap_ok"] and res["static_problems"] == []
    L = [r for r in out if r["head"] == "LIC"]

    def tamper(fn):
        t = copy.deepcopy(L)
        fn(t)
        return gates.k10_f_construction(t)

    assert not tamper(lambda t: t[0]["meta"]["lic_format"].update(word_index=(t[0]["meta"]["lic_format"]["word_index"] + 1) % 50))["ok"]
    assert not tamper(lambda t: t[0].update(options=list(reversed(t[0]["options"]))))["ok"]
    assert not tamper(lambda t: t[0]["meta"].update(card_layout="lic.card.v2"))["ok"]
    assert not tamper(lambda t: t[1]["meta"].update(field_order="project,dep,use,dist"))["ok"]
    assert not tamper(lambda t: t[2]["meta"].update(template_id="t63.lic.v2"))["ok"]
    assert not tamper(lambda t: t[3]["meta"]["lic_format"].update(index=t[4]["meta"]["lic_format"]["index"]))["ok"]
    assert not tamper(lambda t: t[5]["meta"].pop("lic_format"))["ok"]
    assert gates.k10_f_construction([]) ["ok"] and "T63-K10-F" in {g["id"] for g in gates.run_all(out)}


@real_only
def test_k10_f_holds_on_the_pilot_size_dry_run_too():
    tb = lic.LicTable.load(_P["lic_table"])
    rows, summary, _l, _r = checked.run(600, 3, pl.TestDoubleHook(), standin=True, exports=dryrun.fixture_exports(), table=tb)
    out, rep = checked.cut_lic(rows, 3, total=600)
    res = gates.k10_f_construction(out)
    assert res["ok"] and res["rows"] == 55 and gates.k10_lic(out)["ok"] and rep["pair_ok"]


def test_noise_simulation_record_is_seeded_and_reproducible():
    rec = json.load(open(os.path.join(FAMDIR, "K10_NOISE_SIM.json"), encoding="utf-8"))
    assert rec["k"] == 3 and [r["n"] for r in rec["runs"]] == [55, 110] and all(r["sims"] == 200 and r["seed"] == 20261018 for r in rec["runs"])
    for r in rec["runs"]:
        again = gates.k10_noise_simulation(r["n"], sims=3)
        assert again["per_sim"] == r["per_sim"][:3]                                      # same seed, same numbers
        assert r["ub_bar"] == 0.3933 and {"ub_median", "ub_p97_5", "perm_pass_rate", "status_counts"} <= set(r)
    r110 = rec["runs"][1]
    assert r110["ub_median"] > r110["ub_bar"] and r110["n"] == 110                       # correct data cannot pass the 39.3% bar at n=110


# ================================================================================================================ Q7b: K12, LIC is single-level
def test_non_lic_level_weights_keep_the_family_composition_with_lic_all_l3():
    lam, w = C.LIC_SHARE, C.NON_LIC_LEVEL_WEIGHTS
    assert abs(lam - 110 / 1200.0) < 1e-12 and abs(sum(w) - 1.0) < 1e-12
    fam = [(1 - lam) * w[i] + (lam if lv == "L3" else 0.0) for i, lv in enumerate(("L1", "L2", "L3", "L4"))]
    assert all(abs(a - b) < 1e-9 for a, b in zip(fam, (0.20, 0.30, 0.30, 0.20)))
    cells = [g["cell"]["target_level"] for g in G.build_plan(total=1200, seed=6, oversample=False) if g["head"] == "EXISTS"]
    sh = collections.Counter(cells)
    for lv, want in zip(("L1", "L2", "L3", "L4"), w):
        assert abs(sh[lv] / len(cells) - want) <= 0.03


@real_only
def test_every_lic_row_is_l3_and_no_narrower_measure_exists(real_dry):
    _tb, _rec, rows, _s = real_dry
    L = _fam_lic(rows)
    assert {r["meta"]["ladder"] for r in L} == {"L3"} and {r["spec"]["mech"]["cell"] for r in L} == {"high"}
    src = open(os.path.join(FAMDIR, "lic.py"), encoding="utf-8").read()
    assert 'return "high"' in src and "def m_cell_flag" in src and "distance" not in src.lower()
    txt = open(os.path.join(FAMDIR, "README.md"), encoding="utf-8").read()
    assert "LIC rows are single-level (L3, M-CELL HIGH) on the hashed table" in txt


def test_readme_records_q5_cut_and_release_and_q7():
    txt = open(os.path.join(FAMDIR, "README.md"), encoding="utf-8").read()
    for needle in ("Opus ruling Q7", "cut_to_quota", "release_unkept", "seeded permutation", "K10-F", "K10_NOISE_SIM", "report-only"):
        assert needle.lower() in txt.lower(), needle
