"""A72 (17 Oct 2026): the mix_c2 steps the Opus ruling names (removal only, nothing relabelled, no bar moved). In memory only. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_mix_c2_a72.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mix_c2 as m  # noqa: E402
from test_mix_c2_a42d import mk  # noqa: E402


# ---------------------------------------------------------------------------------------------- GB per-card yes band (A42-D 5.5)

def gb_card(card, yes, no, start=0):
    rows = []
    for i in range(yes):
        rows.append(mk(f"{card}_y{start + i}", "GB", gold=1, meta={"card_id": card, "domain": "d"}))
    for i in range(no):
        rows.append(mk(f"{card}_n{start + i}", "GB", gold=0, meta={"card_id": card, "domain": "d"}))
    return rows


def yes_share(rows):
    return sum(1 for r in rows if r["gold"] == 1) / len(rows)


def test_gb_band_down_samples_the_over_represented_label_inside_the_card_only():
    rows = gb_card("c1", 13, 7) + gb_card("c2", 10, 10) + gb_card("c3", 4, 12)        # 0.65 (too many yes), 0.5, 0.25 (too many no)
    out, rels, info = m.gb_band_step(rows, [])
    assert info["cards_fixed"] == 2 and not info["unfixed"]
    by = {c: [r for r in out if r["meta"]["card_id"] == c] for c in ("c1", "c2", "c3")}
    assert 0.4 <= yes_share(by["c1"]) <= 0.6 and 0.4 <= yes_share(by["c3"]) <= 0.6
    assert len(by["c2"]) == 20                                                         # a card inside the band is not touched
    assert all(r["gold"] == 1 for r in rows if r["id"] not in {x["id"] for x in out} and r["meta"]["card_id"] == "c1")    # only yes rows left c1
    assert all(r["gold"] == 0 for r in rows if r["id"] not in {x["id"] for x in out} and r["meta"]["card_id"] == "c3")    # only no rows left c3
    assert {r["id"] for r in out} <= {r["id"] for r in rows} and all(r["gold"] in (0, 1) for r in out)                   # nothing added, nothing relabelled


def test_gb_band_never_takes_a_card_under_its_checked_size_and_reports_what_it_cannot_fix():
    rows = gb_card("c1", 10, 0)                                                         # all yes: the band cannot be reached above 10 rows
    out, rels, info = m.gb_band_step(rows, [])
    assert len(out) == 10 and info["unfixed"] and info["removed"] == 0


def test_gb_band_takes_whole_units_only_and_skips_units_that_hold_both_labels():
    rows = gb_card("c1", 13, 7)
    rels = [{"a": "c1_y0", "b": "c1_n0", "kind": "complement"}, {"a": "c1_y1", "b": "c1_n1", "kind": "complement"}]      # twin pairs hold one yes and one no
    out, rels2, info = m.gb_band_step(rows, rels)
    ids = {r["id"] for r in out}
    assert ("c1_y0" in ids) == ("c1_n0" in ids) and ("c1_y1" in ids) == ("c1_n1" in ids)
    assert 0.4 <= yes_share(out) <= 0.6 and all(x["a"] in ids and x["b"] in ids for x in rels2)


def spread(rows, k=8):
    """Give GB rows k domains so the 20% domain cap does not fire (the cards' rows stay in order)."""
    for i, r in enumerate(rows):
        r["meta"] = {**r["meta"], "domain": f"d{i % k}"}
    return rows


def test_fit_block_runs_the_gb_band_after_the_caps_and_leaves_a_clean_block_alone():
    rows = spread(gb_card("c1", 13, 7) + gb_card("c2", 10, 10))
    out, rels, info = m.fit_block("GB", rows, [])
    assert any(s["rule"] == "gb_card_band" for s in info["steps"]) and not m.block_rules("GB", out)[1]
    clean = spread(gb_card("c2", 10, 10))
    out2, _, info2 = m.fit_block("GB", clean, [])
    assert len(out2) == 20 and info2["steps"] == []


# ---------------------------------------------------------------------------------------------- crowd_select's cap pass

def bins_rows(block, n_medium, n_hard, n_easy=0):
    rows = []
    for k, (b, n) in enumerate((("medium", n_medium), ("hard", n_hard), ("easy", n_easy))):
        rows += [mk(f"{block}_{b}{i}", block, meta={"difficulty_bin": b}) for i in range(n)]
    return rows


def test_diff_cap_pass_sheds_hard_only_units_until_hard_is_inside_30_percent():
    rows = bins_rows("F11", 70, 33)                                                    # hard 0.320
    out, rels, info = m.diff_cap_pass(rows, [])
    hard = sum(1 for r in out if r["meta"]["difficulty_bin"] == "hard")
    assert hard / len(out) <= 0.30 + 1e-9 and hard / len(out) > 0.29 and info == {"F11": 103 - len(out)}
    assert all(r["meta"]["difficulty_bin"] != "medium" or True for r in out) and sum(1 for r in out if r["meta"]["difficulty_bin"] == "medium") == 70


def test_diff_cap_pass_does_not_touch_a_unit_that_holds_a_medium_row():
    rows = bins_rows("F11", 70, 33)
    rels = [{"a": f"F11_hard{i}", "b": f"F11_medium{i}", "kind": "complement"} for i in range(33)]    # every hard row is tied to a medium row
    out, _, info = m.diff_cap_pass(rows, rels)
    assert len(out) == len(rows) and info == {}                                         # nothing can be shed: reported by the gate, not hidden


def test_diff_cap_pass_leaves_blocks_inside_their_caps():
    rows = bins_rows("T01", 70, 30)
    out, _, info = m.diff_cap_pass(rows, [])
    assert len(out) == 100 and info == {}


# ---------------------------------------------------------------------------------------------- pooled new yes/no (spec 5.2)

def yn_mix(spec):
    """spec: block -> (rows, yes_no_share); yes/no rows alternate gold; the rest are choice rows."""
    rows = []
    for b, (n, sh) in spec.items():
        k = round(n * sh)
        for i in range(n):
            rows.append(mk(f"{b}_{i}", b, qtype="noul" if i < k else "choice", gold=i % 2 if i < k else "a",
                           meta={"card_id": f"{b}c{i // 40}", "domain": f"d{i % 8}", "task_id": f"{b}t{i // 40}", "difficulty_bin": "medium"},
                           source="c2_md_x" if b == "MD" else f"c2_{b.lower()}"))
    return rows


def test_pooled_trim_takes_one_common_factor_from_blocks_above_55_percent_and_never_touches_a_program_family():
    rows = yn_mix({"T01": (2000, 0.50), "F5": (1000, 1.0), "F6": (1000, 0.60), "F4": (500, 0.40), "GW": (2000, 0.56)})
    n, y = m.yn_counts(rows)
    assert y / n > 0.55
    out, rels, info = m.yn_pooled_trim(rows, [])
    n2, y2 = m.yn_counts(out)
    assert y2 / n2 <= 0.55 + 1e-9 and y2 / n2 > 0.54                                   # the largest f: the share lands just under the cap
    by0, by1 = Counter(r["_block"] for r in rows), Counter(r["_block"] for r in out)
    assert by1["T01"] == by0["T01"] and by1["F4"] == by0["F4"]                         # program family and a block under 55% are untouched
    step = info["rounds"][0]
    assert set(step["B"]) == {"F5", "F6", "GW"} and 0 < step["common_factor_f"] < 1
    kept = {r["id"] for r in out}
    assert kept <= {r["id"] for r in rows} and all(r["gold"] in (0, 1, "a") for r in out)
    for b in ("F5", "F6", "GW"):                                                       # the removed yes/no rows keep the block's own yes:no ratio
        gone = [r for r in rows if r["_block"] == b and r["id"] not in kept and r["qtype"] == "noul"]
        assert abs(sum(r["gold"] for r in gone) - len(gone) / 2) <= 3


def test_pooled_trim_is_a_noop_inside_the_cap_and_deterministic():
    rows = yn_mix({"T01": (2000, 0.50), "F5": (100, 1.0)})
    out, _, info = m.yn_pooled_trim(rows, [])
    assert len(out) == len(rows) and info["rounds"] == []
    rows2 = yn_mix({"T01": (1000, 0.5), "F5": (1000, 1.0)})
    a, _, _ = m.yn_pooled_trim(rows2, [])
    b, _, _ = m.yn_pooled_trim(rows2, [])
    assert [r["id"] for r in a] == [r["id"] for r in b]


def test_pooled_trim_keeps_the_metadata_block_above_its_floor(monkeypatch):
    monkeypatch.setattr(m, "META_MIN_ROWS", 1000)
    rows = yn_mix({"T01": (4000, 0.5), "MD": (1400, 0.6), "F5": (2000, 1.0)})
    out, _, info = m.yn_pooled_trim(rows, [])
    md = sum(1 for r in out if r["_block"] == "MD")
    assert 1000 + 150 - 40 <= md < 1400                                                 # MD gave what its floor allows (a task may overshoot by its own size)
    n2, y2 = m.yn_counts(out)
    assert y2 / n2 <= 0.55 + 1e-9 and sum(1 for r in out if r["_block"] == "F5") < 2000     # F5 made up the difference


def test_pooled_trim_in_gb_keeps_each_cards_yes_share():
    rows = []
    for c in range(10):
        rows += gb_card(f"gc{c}", 15, 15, start=c * 100)
    rows += yn_mix({"T01": (300, 0.2)})
    out, _, info = m.yn_pooled_trim(rows, [])
    for c in range(10):
        card = [r for r in out if r["meta"].get("card_id") == f"gc{c}"]
        assert 0.4 <= yes_share(card) <= 0.6 and len(card) < 30


def test_pooled_trim_leaves_the_a60_complement_twins_for_last():
    rows = []
    for c in range(20):
        for i in range(10):
            rows.append(mk(f"gc{c}_{i}", "GB", gold=i % 2, meta={"card_id": f"gc{c}", "domain": f"d{c % 6}"}))
    for i in range(10):                                                                   # ten complement twins (an A60 selection) spread over the cards
        rows[i * 20]["role"] = "complement"
        rows[i * 20]["meta"] = {**rows[i * 20]["meta"], "negtwin": {"kind": "antonym", "pattern": f"p{i}"}, "twin_of": f"b{i}"}
    twins = {r["id"] for r in rows if m.a60_kind(r)}
    assert len(twins) == 10
    sub = list(rows)
    gone, got = m.yn_block_remove(sub, [], "GB", 60, m.SEED)
    assert got >= 60 and not (gone & twins)
    gone2, got2 = m.yn_block_remove(sub, [], "GB", 195, m.SEED)                           # nearly everything: only now may a twin go
    assert got2 >= 195 and (gone2 & twins)


# ---------------------------------------------------------------------------------------------- SB5 yes share (A58 step 8)

def test_label_band_fix_down_samples_the_majority_label_to_45_55():
    rows = [mk(f"S{i}", "SB5", gold=1 if i < 70 else 0) for i in range(100)]
    out, _, info = m.label_band_fix(rows, [], "SB5", 0.45, 0.55, "t")
    assert 0.45 <= yes_share(out) <= 0.55 and all(r["gold"] == 0 for r in rows if r["id"] not in {x["id"] for x in out}) is False
    assert all(r["gold"] == 1 for r in rows if r["id"] not in {x["id"] for x in out})
    ok = [mk(f"S{i}", "SB5", gold=i % 2) for i in range(100)]
    assert m.label_band_fix(ok, [], "SB5", 0.45, 0.55, "t")[0] == ok


# ---------------------------------------------------------------------------------------------- report-only routing (A69 a) and the G13 log of a block that is out

def test_g10_lines_of_a_carry_pool_or_block_are_report_only_and_a_program_families_still_bind():
    m._A72_RO.clear()
    lines = ["G10 aggregate yes rate outside 50 +/- 2: ['F11', 'T05']",
             "G10 yes-rate cell outside 50 +/- 2 (family|wording|bin|negation): MD|None|hard|0 n=72 yes=0.542",
             "G10 yes-rate cell outside 50 +/- 2 (family|wording|bin|negation): T01|w1|hard|0 n=72 yes=0.542",
             "G10 longest-option-is-gold off 1/k by > 2 pp in ['GB'] ({'GB': 7.58})",
             "G10 longest-option-is-gold off 1/k by > 2 pp in ['GB', 'T28'] ({'GB': 7.58, 'T28': 2.5})",
             "G10 abstain option is gold on > 50% of rows that show one"]
    out = m.a72_g10(lines)
    assert out == ["G10 aggregate yes rate outside 50 +/- 2: ['T05']",
                   "G10 yes-rate cell outside 50 +/- 2 (family|wording|bin|negation): T01|w1|hard|0 n=72 yes=0.542",
                   "G10 longest-option-is-gold off 1/k by > 2 pp in ['T28'] ({'GB': 7.58, 'T28': 2.5})",
                   "G10 abstain option is gold on > 50% of rows that show one"]
    assert len(m._A72_RO) == 4 and all(x.startswith("report-only (A72, A69 a)") for x in m._A72_RO)


def test_token_mean_of_a_carry_pool_is_report_only_but_the_pooled_mean_and_a_program_family_bind():
    m._A72_RO.clear()
    mkr = lambda i, b: mk(f"{b}{i}", b, meta={"difficulty_bin": "medium"})            # noqa: E731
    rows = [mkr(i, "F5") for i in range(10)] + [mkr(i, "T01") for i in range(10)]
    ntok = {r["id"]: (900 if r["_block"] == "F5" else 700) for r in rows}
    rep, probs = m.cap_checks(rows, ntok, final=False)
    assert not any("F5: mean" in p for p in probs) and rep["F5"]["tok_mean_report_only"] and any("F5: mean" in x for x in m._A72_RO)
    assert not any("pooled mean" in p for p in probs) and rep["_new_tok_mean"] == 800.0
    ntok2 = {r["id"]: (1200 if r["_block"] == "F5" else 900) for r in rows}
    rep2, probs2 = m.cap_checks(rows, ntok2, final=False)
    assert any("T01: mean 900" in p for p in probs2) and any("pooled mean of new rows 1050" in p for p in probs2)


def test_a_gateless_seed_log_is_report_only_everything_else_still_refuses(monkeypatch):
    m._A72_RO.clear()
    monkeypatch.setattr(m.c2_select, "g13_log_problems", lambda ilog, files, tool=None, exempt=(): [
        "c2_seed_T27: incomplete G13 log (complete False, 1 reasons): re-run before the mix",
        "c2_seed_T26: incomplete G13 log (complete False, 1 reasons): re-run before the mix"])
    out = m.g13_log_problems(None, [])
    assert out == ["c2_seed_T26: incomplete G13 log (complete False, 1 reasons): re-run before the mix"]
    assert len(m._A72_RO) == 1 and "c2_seed_T27" in m._A72_RO[0]


# ---------------------------------------------------------------------------------------------- held-out packs by pack ID (A54 a)

def test_held_out_pack_check_compares_pack_ids_not_domain_labels():
    class RS:                                   # the replay_sample module is only used by row_keys for the normalised state
        @staticmethod
        def norm_state(s):
            return s
    dev = {"T33": [({"id": "d1", "meta": {"domain_pack": "bunkaru"}}, True)],
           "T23": [({"id": "d2", "meta": {"domain_pack": "t23:travel"}}, True)],
           "T01": [({"id": "d3", "meta": {"domain_pack": "t01-rolling-p3"}}, True)]}
    ho = m.HeldOutA72(dev, RS)
    mk_ = lambda b, pack: {"id": f"{b}1", "_block": b, "meta": {"domain_pack": pack}}       # noqa: E731
    assert ho.clash(mk_("T33", "bunkaru")) == ["domain_pack"]                                  # a real pack id still binds
    assert ho.clash(mk_("T23", "t23:travel")) == [] and ho.clash(mk_("T01", "t01-rolling-p3")) == []     # a domain label / card-slot label does not
    assert ho.clash(mk_("T33", "other")) == []


# ---------------------------------------------------------------------------------------------- the 40-task floor is NOT loosened

def test_the_task_floor_stays_binding_after_a_quarantine_unless_a_ruling_turns_it_on(monkeypatch):
    rows = []
    for s in range(8):
        for t in range(40 if s else 39):
            for i in range(5):
                rows.append(mk(f"M{s}_{t}_{i}", "MD", source=f"src{s}", gold=i % 2, card="",
                               meta={"task_id": f"s{s}t{t}", "domain": f"d{s}"}))
    monkeypatch.setattr(m, "META_MIN_ROWS", 1)
    monkeypatch.setattr(m, "A72_TASK_QUARANTINE", {"src0": ("a", "b")})
    _, p = m.block_rules("MD", rows, loaded=True, deviations=[])
    assert any("tasks per source outside" in x for x in p)
    monkeypatch.setattr(m, "A72_TASK_FLOOR_A51C", True)
    _, p2 = m.block_rules("MD", rows, loaded=True, deviations=[])
    assert not any("tasks per source outside" in x for x in p2)


def test_metadata_card_free_rule_removes_whole_tasks_of_carded_rows_only():
    rows = []
    for s_ in range(8):                                                                 # 8 sources x 10 tasks x 10 rows, 8 domains: no source / domain cap fires
        for t in range(10):
            free = t < 2 if s_ == 0 else t % 2 == 0
            for i in range(10):
                rows.append(mk(f"M{s_}_{t}_{i}", "MD", source=f"src{s_}", gold=i % 2, card="" if free else "card",
                               meta={"task_id": f"s{s_}t{t}", "domain": f"d{s_}"}))
    s0 = [r for r in rows if r["source"] == "src0"]
    assert sum(1 for r in s0 if m.card_free(r)) / len(s0) < 0.30
    out, _, info = m.fit_block("MD", rows, [])
    assert any(s["rule"].startswith("card_free:") for s in info["steps"])
    s0o = [r for r in out if r["source"] == "src0"]
    assert sum(1 for r in s0o if m.card_free(r)) / len(s0o) >= 0.30 - 1e-9 and {r["meta"]["task_id"] for r in s0o} >= {"s0t0", "s0t1"}
    assert len([r for r in out if r["source"] != "src0"]) == 700 and len(s0o) % 10 == 0     # other sources untouched; whole tasks


# ---------------------------------------------------------------------------------------------- E2 stub safety

def test_e2_cell_fix_without_a_replay_context_is_a_noop():
    rows = [mk("a", "T01")]
    out, rels, log = m.e2_cell_fix(rows, [], {})
    assert out == rows and log["skipped"] == "no replay context"
    out2, _, n = m.e2_neutral_trim(rows, [], {}, 5)
    assert out2 == rows and n == 0
