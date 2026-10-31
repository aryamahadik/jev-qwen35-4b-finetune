import json
import threading
import time
from pathlib import Path

import httpx
import pytest

from oc1 import common as C
from oc1 import items as I
from oc1 import runner as RU
from oc1 import front as F
from oc1 import loadgen as LG
from oc1 import backend as B

from fastcore import testing as T          # noqa: E402
from fakes import FakeSGLangServer           # noqa: E402

C1_DIR = str(T.ADAPTER)


def sample(items, n):
    out, seen = [], {}
    for it in items:                         # keep the bucket mix, small prompts only
        if len(it["request"]["state"]) > 700:
            continue
        seen[it["bucket"]] = seen.get(it["bucket"], 0) + 1
        if seen[it["bucket"]] <= max(1, n // 5):
            out.append(it)
    return out[:n]


@pytest.fixture(scope="module")
def world(tmp_path_factory):
    T.c1_tokenizer()
    model = T.tiny_model(seed=0)
    srv = FakeSGLangServer(model)
    work = tmp_path_factory.mktemp("work")
    for name, n in (("P", 40), ("S", 20), ("N", 40), ("R", 24)):
        C.write_jsonl(work / f"{name}.jsonl", sample(C.read_jsonl(C.ROOT / "data" / f"{name}.jsonl"), n))
    yield {"srv": srv, "work": work, "tmp": tmp_path_factory.mktemp("out")}
    srv.close()


PARAMS = {"sub_n": 20, "parity_conc": 4, "lat_n": 8, "lat_s": 5, "lat_warm": 2, "lat_rounds": 2, "tp_conc": [2, 4],
          "prefix_n": 12, "prefix_conc": 2}


def spec_for(w, config, out_dir, measures):
    return {"config": config, "sgl_url": w["srv"].url, "work_dir": str(w["work"]), "c1_dir": C1_DIR, "out_dir": str(out_dir),
            "measures": measures, "params": PARAMS, "out_path": str(out_dir / "measure.json"), "fp8": False}


def test_measure_end_to_end_and_parity_against_the_baseline(world, monkeypatch, tmp_path):
    monkeypatch.setenv("OC1_TMP", str(tmp_path))
    root = world["tmp"]
    s1 = root / "s1"
    s1.mkdir()
    res1 = RU.run_measure(spec_for(world, "s1", s1, ["parity_full", "latency", "throughput", "prefix", "score_readout"]),
                          log=lambda *a: None)
    assert not res1["errors"], res1["errors"]
    assert set(res1["steps"]) == {"parity_full", "latency", "throughput", "prefix", "score_readout"}
    pf = res1["steps"]["parity_full"]
    assert pf["n_missing"] == 0 and (s1 / "answers_P.jsonl").exists()
    n = len(C.read_jsonl(world["work"] / "P.jsonl"))
    assert len(C.read_jsonl(s1 / "answers_P.jsonl")) == n
    sr = res1["steps"]["score_readout"]
    cmp = sr["parity"]["parity_vs_generate_same_boot"]                  # score readout vs generate readout of the same boot
    assert cmp["n"] > 0 and cmp["argmax_agree"] == 1.0 and cmp["dp_max"] < 5e-5
    assert res1["steps"]["latency"]["batch1_N"]["wall_ms"]["n"] == 8
    assert res1["steps"]["throughput"]["S"]["c2"]["ok"] == len(C.read_jsonl(world["work"] / "S.jsonl"))
    assert res1["steps"]["prefix"]["rows"] == 12
    # a second config gated against the first (same session layout: sibling dir "s1")
    other = root / "chunk_off"
    other.mkdir()
    res2 = RU.run_measure(spec_for(world, "chunk_off", other, ["parity_sub", "latency"]), log=lambda *a: None)
    assert not res2["errors"], res2["errors"]
    ps = res2["steps"]["parity_sub"]
    rep = ps["parity_vs_s1_same_session"]
    assert rep["n"] == ps["n_requested"] and rep["argmax_agree"] == 1.0 and rep["dp_max"] < 1e-9
    assert (other / "answers_P_sub.jsonl").exists()
    # partial results are on disk after every step
    assert json.loads((other / "measure.json").read_text())["steps"].keys() >= {"parity_sub", "latency"}


def test_front_and_loadgen_end_to_end(world, tmp_path):
    cfg = {"sglang_url": world["srv"].url, "c1_tokenizer_dir": C1_DIR, "port": 0, "seconds": 120, "idle_s": 120,
           "wait_ms": 0.0, "shed_at": 10 ** 6, "ready_file": str(tmp_path / "ready.json"), "done_file": str(tmp_path / "done.json"),
           "warm_requests": 2, "host": "127.0.0.1", "max_inflight": 64}
    stop = threading.Event()
    th = threading.Thread(target=F.run_front, args=(cfg, "tok123", stop), kwargs={"log": lambda *a: None}, daemon=True)
    th.start()
    t0 = time.time()
    while not (tmp_path / "ready.json").exists():
        assert time.time() - t0 < 180 and th.is_alive(), "front did not come up"
        time.sleep(0.5)
    ready = json.loads((tmp_path / "ready.json").read_text())
    assert ready["ok"]
    url = f"http://127.0.0.1:{ready['port']}"
    reqs = [it["request"] for it in sample(C.read_jsonl(world["work"] / "P.jsonl"), 40)]
    # unauthorized
    assert httpx.post(url + "/decide", json=reqs[0]).status_code == 401
    levels = [{"name": "a", "qps": 6, "duration_s": 4, "warm_s": 1, "wait_ms": 0},
              {"name": "b", "qps": 6, "duration_s": 4, "warm_s": 1, "wait_ms": 5, "new_conn_frac": 0.5}]
    out = LG.e2e_levels(url, "tok123", reqs * 6, levels, log=lambda *a: None, workers=8)
    for lv in out:
        assert lv["ok"] >= 5 and lv["errors"] == 0 and lv["shed_503"] == 0, lv
        for k in ("total_ms", "wait_ms", "server_ms", "tokenize_ms", "queue_ms", "sglang_call_ms", "readout_ms", "network_ms",
                  "client_queue_ms", "decode_ms"):
            assert lv[k]["n"] > 0, k
        assert lv["server_mark"]["served"] >= lv["ok"] and "gpu" in lv["server_mark"]
        assert lv["total_ms"]["p50"] >= lv["server_ms"]["p50"] > 0
        assert lv["wait_ms"]["p50"] >= lv["server_ms"]["p50"] * 0.99
    assert out[1]["new_connections"] >= 1 and out[1]["connect_ms"]["n"] >= 1
    assert out[1]["settings"]["wait_ms"] == 5
    # the coalescing wait is part of the timing when the cap is on
    assert out[1]["coalesce_wait_ms"]["p50"] >= 4.0 and out[0]["coalesce_wait_ms"]["p50"] < 4.0
    health = httpx.get(url + "/health", headers={"Authorization": "Bearer tok123"}).json()
    assert health["coalescer"]["merged_calls"] > 0 and health["front"]["wait_ms"] == 5
    # answers equal the fake backend's directly (the front adds nothing to the numbers)
    ans = httpx.post(url + "/decide", json=reqs[1], headers={"Authorization": "Bearer tok123"}).json()
    assert "answers" in ans and ans["server_ms"] > 0 and ans["engine"] == "sglang"
    r = httpx.post(url + "/shutdown", headers={"Authorization": "Bearer tok123"})
    assert r.status_code == 200
    th.join(timeout=30)
    done = json.loads((tmp_path / "done.json").read_text())
    assert done["served"] >= 10 and done["errors"] == 0


def test_coalescer_merges_concurrent_requests_and_splits_the_answers(world):
    SH = I.sglang_host_mod()
    inner = SH.SGLangClient(world["srv"].url, timeout=30.0)
    co = F.CoalescingClient(inner, wait_ms=60.0, max_seqs=64)
    R = I.readout_mod()
    tok, ro = T.c1_tokenizer(), T.readout()
    preps = [I.prepare_one(it, R, ro, tok) for it in sample(C.read_jsonl(world["work"] / "N.jsonl"), 6)]
    be = B.GenerateBackend(co)
    solo = B.GenerateBackend(inner)
    out, errs = {}, []

    def one(p):
        try:
            out[p.id] = be.read(p)[0]
        except Exception as e:  # noqa: BLE001
            errs.append(e)

    base = world["srv"].calls["generate"]
    th = [threading.Thread(target=one, args=(p,)) for p in preps]
    [t.start() for t in th]
    [t.join() for t in th]
    assert not errs
    calls = world["srv"].calls["generate"] - base
    assert calls < len(preps), "a 60 ms wait cap should merge simultaneous requests"
    assert co.snapshot()["mean_seqs_per_call"] > 1.5
    for p in preps:                                    # merged-then-split answers are the solo answers
        a = B.answer_probs(out[p.id]["q0"], p.qtype)
        b = B.answer_probs(solo.read(p)[0]["q0"], p.qtype)
        assert max(abs(a[k] - b[k]) for k in a) < 1e-9
    co.close()


def test_coalescer_sheds_when_the_queue_is_full(world):
    SH = I.sglang_host_mod()
    inner = SH.SGLangClient(world["srv"].url, timeout=30.0)
    co = F.CoalescingClient(inner, wait_ms=200.0, max_seqs=1000, max_queue=1)
    body = {"input_ids": [[5, 6, 7]], "token_ids_logprob": [[10, 11]], "sampling_params": {}, "rid": ["x"], "stream": False,
            "return_logprob": True, "logprob_start_len": -1}
    results = []

    def go(i):
        try:
            co.generate({**body, "rid": [f"r{i}"]}, 20.0)
            results.append("ok")
        except SH.UpstreamUnavailable:
            results.append("shed")

    th = [threading.Thread(target=go, args=(i,)) for i in range(6)]
    [t.start() for t in th]
    [t.join() for t in th]
    assert "shed" in results and "ok" in results and co.snapshot()["shed"] >= 1
    co.close()
