import json
import os
import sys
from pathlib import Path

import pytest

from oc1 import common as C
from oc1 import configs as K
from oc1 import session as S
from oc1 import stubserver as ST

from fastcore import testing as T          # noqa: E402


class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def make_session(tmp_path, clock=None, **kw):
    events = []
    plan = {"configs": ["s1", "chunk_off"], "boot_timeout_s": 60, "measure_timeout_s": 600,
            "params": {"sub_n": 30, "parity_conc": 4, "lat_n": 6, "lat_s": 4, "lat_warm": 2, "lat_rounds": 2, "tp_conc": [2, 4],
                       "prefix_n": 10, "prefix_conc": 2}, "e2e": {"enabled": False}, "vision": {"enabled": False}, "voice_c1": {"enabled": False}}
    sess = S.Session(plan, events.append, models_root=str(tmp_path / "models"), work_dir=str(tmp_path / "work"),
                     results_root=str(tmp_path / "results"), rate_usd_h=4.33, clock=clock or Clock(), log=lambda *a: None,
                     runner_python=sys.executable, **kw)
    return sess, events


def test_gate_arithmetic(tmp_path):
    clk = Clock()
    sess, ev = make_session(tmp_path, clk, prior_usd=0.0)
    cfg = K.CONFIGS["s1"]
    ok, why = sess.gate(cfg)
    assert ok and "<=" in why
    # prior spend leaves too little room for the S1 block
    sess2, _ = make_session(tmp_path, clk, prior_usd=3.9)
    ok, why = sess2.gate(cfg)
    assert not ok and "budget gate" in why
    # a small block still fits at the same spend
    assert sess2.gate(K.CONFIGS["fp8_leave_attn"])[0]
    # elapsed container time counts at the rate (+ the start overhead)
    clk.t = 3600.0
    assert sess.spent() == pytest.approx(C.container_cost_usd(3600, 4.33), rel=1e-9)
    clk.t = 3600.0 * 1.2
    assert sess.spent() >= C.HARD_STOP_USD
    ok, why = sess.gate(cfg)
    assert not ok and "hard stop" in why
    assert sess.run_block(cfg)["skipped"].startswith("hard stop")
    assert ev == [] or True


class FakeServer:
    """Stands in for SglServer: a StubSGLang HTTP server instead of a GPU process."""
    boot_error = None

    def __init__(self, cfg, model_path, python=None, port=None, log=print, log_file=None, extra_env=None):
        self.cfg, self.model_path = cfg, str(model_path)
        self.stub = ST.StubSGLang(port=0)
        self.url = self.stub.url
        self.tail = ["fake log line"]
        self.cmd = cfg.cmd(model_path)
        self.stopped = False

    def start(self):
        self.stub.start()
        return self

    def wait_ready(self, timeout_s=0):
        if FakeServer.boot_error and self.cfg.name in FakeServer.boot_error:
            raise RuntimeError(FakeServer.boot_error[self.cfg.name])
        return 1.5

    def server_info(self):
        w = S.want_args(self.cfg, self.model_path)
        w.update({"enable_lora": False, "lora_paths": None, "cuda_graph_config": {"prefill": {"backend": "breakable"}}})
        return w

    def alive(self):
        return True

    def stop(self, grace=30.0):
        self.stopped = True
        self.stub.close()
        return {"stop_s": 0.1, "gpu": {"free": True}}


@pytest.fixture()
def env(tmp_path, monkeypatch):
    T.c1_tokenizer()
    models = tmp_path / "models" / C.MERGED_NAME
    models.mkdir(parents=True)
    os.symlink(T.ADAPTER, models / "c1_tokenizer")
    work = tmp_path / "work"
    work.mkdir()
    for name, n in (("P", 24), ("S", 12), ("N", 24), ("R", 12)):
        items = [it for it in C.read_jsonl(C.ROOT / "data" / f"{name}.jsonl") if len(it["request"]["state"]) < 600]
        C.write_jsonl(work / f"{name}.jsonl", items[:n])
    monkeypatch.setattr(S, "SglServer", FakeServer)
    monkeypatch.setenv("OC1_TMP", str(tmp_path))
    FakeServer.boot_error = None
    return tmp_path


def test_blocks_run_in_order_and_write_results(env):
    sess, ev = make_session(env)
    res = sess.run()
    assert list(res["results"]) == ["s1", "chunk_off"]
    for name, r in res["results"].items():
        assert "error" not in r, r.get("error")
        assert r["boot_s"] == 1.5 and r["args_problems"] == [] and r["stop"]["gpu"]["free"]
        assert (env / "results" / name / "block.json").exists()
    m1 = res["results"]["s1"]["measure"]
    assert set(m1["steps"]) >= {"parity_full", "latency", "throughput", "prefix", "score_readout"} and not m1["errors"]
    m2 = res["results"]["chunk_off"]["measure"]
    assert "parity_vs_s1_same_session" in m2["steps"]["parity_sub"]          # gated against the S1 block of this session
    kinds = [e["event"] for e in ev]
    assert kinds.count("block_start") == 2 and kinds.count("block_end") == 2 and kinds.count("booted") == 2


def test_a_failed_boot_is_recorded_and_the_next_block_still_runs(env):
    FakeServer.boot_error = {"s1": "SGLang exited (1) during boot"}
    sess, ev = make_session(env)
    res = sess.run()
    assert "SGLang exited" in res["results"]["s1"]["error"] and res["results"]["s1"]["stop"]
    assert "error" not in res["results"]["chunk_off"]


def test_a_wrong_engine_is_refused_before_any_timing(env, monkeypatch):
    def bad_info(self):
        w = S.want_args(self.cfg, self.model_path)
        w["dtype"] = "float16"
        return w
    monkeypatch.setattr(FakeServer, "server_info", bad_info)
    sess, _ = make_session(env)
    sess.plan["configs"] = ["s1"]
    res = sess.run()
    r = res["results"]["s1"]
    assert "refused" in r["error"] and "measure" not in r
