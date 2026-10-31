"""Pool planning, selection, caps, drift, and the V-D decision rules."""
import collections
import random

import pool as PL
import vcommon as V
import vgates as G


def mk(n, seed=0):
    r = random.Random(seed)
    out = []
    for i in range(n):
        fam = r.choice(["T50", "T51", "T53", "T54", "T55", "GEN", "T41c"])
        out.append({"variant_id": "v%d" % i, "source_row_id": "s%d" % (i // 2 + r.randint(0, 3000)), "source_family": fam, "source_label": r.choice(["A", "B", "C"]),
                    "generator": "A" if r.random() < 0.55 else "B", "stratum": r.choices(V.STRATA, weights=[75, 10, 10, 5])[0], "band": r.choices([0, 1, 2, 3], weights=[30, 35, 25, 10])[0],
                    "voice": r.choice(["af_heart", "af_bella", "am_michael", "bf_emma", "bm_fable", "af_nova", "am_puck", "af_kore", "af_sarah", "bf_isabella", "bm_george", "af_alloy", "am_fenrir", "af_aoede", "af_nicole"]),
                    "fallback_spans": r.random() < 0.1, "kept_by_checker": r.random() < 0.8, "raw_asr_text": "Delete the cache.", "chunk_mode": "LOCKED-560-FLUSH"})
    return out


def test_pool_plan_formula():
    p = PL.pool_plan([0.9, 0.7, 0.5, 0.3])
    assert p["per_band"][0] == 1100 and p["per_band"][1] == 1650 and p["per_band"][3] == 1100
    assert p["total"] == sum(p["per_band"]) and not p["capped"]
    big = PL.pool_plan([0.1, 0.1, 0.1, 0.1])
    assert big["capped"] and big["total"] <= V.POOL_CAP


def test_selection_honours_every_cap_and_share():
    kept, rep = PL.select_kept(mk(20000), random.Random(3), n_target=3000)
    assert len(kept) == 3000 and not rep["below_floor"]
    ok, det = PL.shares_within_tolerance(rep)
    assert ok, det
    per = collections.Counter(v["source_row_id"] for v in kept)
    assert max(per.values()) <= 2
    fam = collections.Counter(v["source_family"] for v in kept)
    assert fam["GEN"] <= 0.05 * 3000 + 1 and max(fam.values()) <= 0.25 * 3000 + 1
    assert sum(1 for v in kept if v["fallback_spans"]) <= 0.30 * 3000
    voice = collections.Counter(v["voice"] for v in kept if v["generator"] == "A")
    assert max(voice.values()) <= 0.10 * 1650 + 2


def test_selection_ships_at_achieved_size_and_flags_floor():
    kept, rep = PL.select_kept(mk(900), random.Random(1), n_target=3000)
    assert rep["ships_at_achieved_size"] and rep["below_floor"] and len(kept) < 1500


def test_selection_only_takes_variants_that_passed_the_checker_and_have_a_band():
    vs = mk(5000)
    for v in vs[:2000]:
        v["band"] = None
    kept, _ = PL.select_kept(vs, random.Random(2), n_target=800)
    assert all(v["kept_by_checker"] and v["band"] in (0, 1, 2, 3) for v in kept)


def test_gate_c8_sizes_and_twin_rule():
    kept, _ = PL.select_kept(mk(20000, 4), random.Random(3), n_target=3000)
    twins = {v["source_row_id"] for v in kept}
    res = G.gate_c8_sizes(kept, 40000, twins)
    assert res["passed"], res["detail"]["checks"]
    assert not G.gate_c8_sizes(kept, 20000, twins)["detail"]["checks"]["voice_share_of_new_rows"]
    assert not G.gate_c8_sizes(kept, 40000, twins - {kept[0]["source_row_id"]})["detail"]["checks"]["clean_twin_100pct"]
    assert not G.gate_c8_sizes(kept, 40000, twins, human_label_sources={kept[1]["source_row_id"]})["detail"]["checks"]["zero_human_label_sources"]
    bad = [dict(v) for v in kept]
    bad[0]["chunk_mode"] = "CHUNK-160"
    assert not G.gate_c8_sizes(bad, 40000, twins)["detail"]["checks"]["chunk_mode_locked"]


def test_label_drift_and_drop_only_rebalance():
    pool = mk(8000, 7)
    kept = [v for v in pool if v["source_family"] == "T50"][:900]
    for v in kept[:400]:
        v["source_label"] = "A"
    ok, det = PL.label_drift(pool, kept)
    assert not ok
    new = PL.rebalance_family(kept, pool, "T50")
    assert len(new) < len(kept) and set(id(v) for v in new) <= set(id(v) for v in kept)       # drop-only
    ok2, _ = PL.label_drift(pool, new)
    assert ok2


def test_number_form_decision():
    assert PL.number_form_decision(70, 30)["decision"] == "digits"
    assert PL.number_form_decision(20, 80)["decision"] == "words"
    assert PL.number_form_decision(55, 45)["decision"] == "mixed"


def test_padding_decision():
    m = {0: 0.80, 160: 0.93, 320: 0.985, 560: 0.995, 1120: 1.0}
    assert PL.padding_decision(m, 1120)["padding_ms"] == 560
    assert PL.padding_decision({0: 0.5, 560: 0.9, 1120: 1.0}, 1120)["padding_ms"] is None


def test_pilot_reach_and_condition_filter_and_short_rule():
    ok, need = PL.pilot_reach([80, 90, 70, 30])
    assert ok and need == [75, 88, 63, 25]
    assert not PL.pilot_reach([80, 90, 70, 10])[0]
    names, over = PL.condition_filter({"snr5": [None, None, 1, None], "clean": [0, 0, 1, None]})
    assert names == ["snr5"]
    assert PL.clean_condition_median_ok([0.0, 0.01, 0.02]) and not PL.clean_condition_median_ok([0.05, 0.06, 0.07])
    assert PL.short_utterance_rule([0.1, 0.12])["exclude_short_from_A"] is True
    assert PL.consistency_ok([0.1, 0.2, 0.3], [0.105, 0.2, 0.31])[0]


def test_survival_report_counts_roles():
    r = [{"kept": True, "spans": [], "global_negation_ok": True, "wer": 0.02, "band": 0}, {"kept": False, "spans": [{"status": "altered", "role": "negation", "kind": "negation"}], "global_negation_ok": False, "wer": 0.1, "band": 2}]
    rep = PL.survival_report(r)
    assert rep["kept_pct"] == 0.5 and rep["altered_rows_by_role"]["negation/negation"] == 1 and rep["altered_rows_by_role"]["negation/global"] == 1


def test_number_form_minority_and_stress_set():
    assert PL.number_form_minority({"digits": 850, "words": 150}, {"decision": "digits"})[0]
    assert not PL.number_form_minority({"digits": 990, "words": 10}, {"decision": "digits"})[0]
    assert PL.number_form_minority({"digits": 50, "words": 50}, {"decision": "mixed"})[0]
    s = PL.stress_set([{"variant_id": "a", "kept_by_checker": True}, {"variant_id": "b", "kept_by_checker": False, "reasons": ["negation:negation:deleted"]}])
    assert [x["variant_id"] for x in s] == ["b"]
