import json
from pathlib import Path

import pytest

from oc1 import common as C
from oc1 import report as RP
from oc1 import costmodel as CM

S2 = C.LEAN / "speed" / "speed2_20261013"


@pytest.mark.skipif(not (S2 / "S1" / "answers_P.jsonl").exists(), reason="SPEED-2 files absent")
def test_report_with_real_answers_as_stand_ins(tmp_path):
    """S1 stored answers = the 'baseline block'; A0's stored answers play a 'candidate' (they differ from S1 on 19 near-tie rows)."""
    s1, cand = tmp_path / "s1", tmp_path / "chunk_off"
    s1.mkdir(), cand.mkdir()
    (s1 / "answers_P.jsonl").write_text((S2 / "S1" / "answers_P.jsonl").read_text())
    (cand / "answers_P_sub.jsonl").write_text((S2 / "A0" / "answers_P.jsonl").read_text())
    for d, boot in ((s1, 170.0), (cand, 150.0)):
        (d / "block.json").write_text(json.dumps({"config": d.name, "boot_s": boot, "desc": "x"}))
    meas = {"steps": {"latency": {"batch1_N": {"wall_ms": {"n": 300, "p50": 30.0, "p95": 60.0}},
                                  "batched_N": {"one_call": {"per_decision_ms": {"p50": 9.9}}}},
                      "throughput": {"S": {"c16": {"decisions_per_h": 120000.0, "failed": 0}, "c64": {"decisions_per_h": 200000.0, "failed": 0,
                                                                                                    "gpu": {"util_mean": 77.0}}}},
                      "prefix": {"cached_token_share": 0.575}}, "errors": {}}
    (s1 / "measure.json").write_text(json.dumps(meas))
    (cand / "measure.json").write_text(json.dumps({"steps": {}, "errors": {}}))
    out = RP.build(tmp_path)
    c = out["configs"]["chunk_off"]
    assert c["parity_vs_s1"]["n"] == 8143 and c["parity_vs_s1"]["n_flips"] == 19
    assert round(100 * c["parity_vs_s1"]["argmax_agree"], 2) == 99.77
    assert c["parity_vs_s1"]["flip_margin_max"] < 0.05
    assert c["accuracy_vs_s1"] and abs(c["accuracy_vs_s1"]["acc_diff_pt"]) < 0.1
    assert c["verdict"] == "PASS" and c["adopt"] is True
    s = out["configs"]["s1"]
    assert s["latency_ms"]["batch1_N"]["p50"] == 30.0 and s["prefix"]["R_cached_share"] == 0.575
    assert out["cost"]["s1"]["decisions_per_h"] == 200000.0
    text = RP.render(out)
    assert "chunk_off" in text and "USD per 1K" in text


def test_costmodel_numbers():
    # SPEED-2 S1: 124,305 decisions/h at USD 3.95/h -> 0.0318 per 1K at 100%, 0.0794 at 40% (REPORT.md)
    assert CM.usd_per_1k(3.95, 124305, 1.0) == pytest.approx(0.03178, abs=2e-5)
    assert CM.usd_per_1k(3.95, 124305, 0.4) == pytest.approx(0.07944, abs=2e-5)
    # compute floor: 14.1 ms per decision (B1a) at 3.95/h
    assert CM.compute_floor(3.95, 14.1) == pytest.approx(0.01547, abs=1e-4)
    assert CM.breakeven_util(3.95, 124305, 0.061) == pytest.approx(0.5209, abs=2e-3)
    assert CM.cost_at_qps(3.95, 10) == pytest.approx(0.10972, abs=1e-4)
    assert CM.utilisation_at_qps(10, 360000) == pytest.approx(0.1)
    t = CM.table({"x": {"dph": 124305, "ms_per_decision": 14.1}})
    row = next(r for r in t["x"]["tiers"] if r["price"].startswith("Modal H100 on-demand (any"))
    assert row["usd_per_1k"]["40%"] == pytest.approx(CM.usd_per_1k(3.95 + CM.CONTAINER_EXTRA_USD_H, 124305, 0.4), abs=1e-5)
    assert "Modal H100 on-demand (any region)" in t["x"]["compute_floor_usd_per_1k"]
    h = CM.hedge_estimate([20.0] * 95 + [400.0] * 5, hedge_after_ms=60.0)
    assert h["hedged"]["p99"] < h["plain"]["p99"] and 0 < h["extra_request_share"] < 0.2


def test_voice_breakdown_adds_asr_final_and_c1_decision():
    voice = {"modes": {"stream160": {"final_flush_ms": {"p50": 25.0, "p95": 40.0}, "wer_mean": 0.03},
                       "offline": {"total_ms": {"p50": 120.0, "p95": 150.0}, "wer_mean": 0.01}}}
    vc1 = {"modes": {"stream160": {"argmax_agree": 0.97}, "offline": {"argmax_agree": 0.99}},
           "c1_latency_ms": {"cold_flushed": {"p50": 30.0}, "prefix_warm": {"p50": 18.0}, "prefix_cached_share": 0.6}}
    b = RP.voice_breakdown(voice, vc1)
    assert b["modes"]["stream160"]["total_after_speech_ms_p50"] == {"cold": 55.0, "prefix_warm": 43.0}
    assert b["modes"]["offline"]["decision_agreement_vs_text"] == 0.99 and b["prefix_cached_share"] == 0.6
    assert RP.voice_breakdown(None, vc1) is None


def test_always_on_and_breakeven_qps():
    assert CM.always_on_monthly(4.4) == pytest.approx(3212.0)
    # one H100 at 4.4/h equals Jev's 0.061 per 1K calls at 4.4 / 0.000061 / 3600 = 20.0 requests/s
    assert CM.breakeven_qps(4.4, 0.061) == pytest.approx(20.04, abs=0.02)
    t = CM.table({"x": 100000})
    row = t["x"]["tiers"][0]
    assert row["always_on_usd_month"] > 3000 and row["breakeven_qps_vs_jev"]["research_finding"] > row["breakeven_qps_vs_jev"]["prereg_11.4_reference"]
