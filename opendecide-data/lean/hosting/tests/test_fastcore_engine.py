"""fastcore.engine end to end on CPU: FastEngine (tiny random Qwen3.5 hybrid, C1 tokenizer, CUDA graphs EMULATED)
answers API v1 requests exactly like decoder_io.predict(tta_choice=True) under every HF arm's flags (A0 legacy, A1, A2),
with concurrent callers, multi-question requests, identity-only reads (choice_views=1), errors, flags and /health.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_fastcore_engine.py -q
No GPU, no network, no Modal.
"""
import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastcore import ARM_FLAGS, EngineClosed, FastEngine, RequestError, request_from_row  # noqa: E402
from fastcore import graphs as G  # noqa: E402
from fastcore import testing as T  # noqa: E402
from fastcore.readout import dio  # noqa: E402

TOL = 1e-5


@pytest.fixture(scope="module")
def setup():
    tok, ro, model = T.c1_tokenizer(), T.readout(), T.tiny_model()
    eng = FastEngine(model, tok, ro=ro, log=lambda *a: None)
    # a reduced plan (CPU time) that still covers the legacy B1/B2 <= 1024 shapes A0 uses for these rows
    rep = eng.boot(coverage={1: 2048, 2: 1024, 4: 512, 8: 512}, legacy_shapes=False, eager_warmup={}, warm_requests=1)
    yield tok, ro, model, eng, rep
    eng.close()


@pytest.fixture(scope="module")
def sample():
    rows = T.dev_rows()
    pick = []
    for f, n in ((lambda r: r["qtype"] == "noul" and r.get("card"), 3), (lambda r: r["qtype"] == "noul" and not r.get("card"), 3),
                 (lambda r: r["qtype"] == "choice" and len(r["options"]) <= 9, 4),
                 (lambda r: r["qtype"] == "choice" and 10 <= len(r["options"]) <= 26, 2),
                 (lambda r: r["qtype"] == "choice" and len(r["options"]) > 26, 2)):
        pool = sorted([r for r in rows if f(r)], key=lambda r: (len(r["state"]) + len(r.get("card") or ""), r["id"]))
        pick += pool[:: max(1, len(pool) // (4 * n))][:n]
    return pick


@pytest.fixture(scope="module")
def reference(setup, sample):
    tok, ro, model, eng, rep = setup
    return {r["id"]: p for r, p in zip(sample, dio.predict(model, tok, sample, dev="cpu", tta_choice=True))}


def _diff(ans, r, p_ref):
    if r["qtype"] == "noul":
        assert set(ans) == {"type", "noul", "probabilities", "usage"}
        return max(abs(ans["noul"] - p_ref["yes"]), abs(ans["probabilities"]["no"] - p_ref["no"]))
    assert set(ans) >= {"type", "choice", "confidence", "probabilities", "usage"} and list(ans["probabilities"]) == r["options"]
    assert ans["confidence"] == ans["probabilities"][ans["choice"]] == max(ans["probabilities"].values())
    return max(abs(ans["probabilities"][o] - p_ref[o]) for o in r["options"])


def test_boot_report(setup):
    *_, eng, rep = setup
    g = rep["graphs"]
    assert g["mode"] == "shared" and g["selfcheck"]["ok"] and g["n_graphs"] == len(G.coverage_plan(
        {1: 2048, 2: 1024, 4: 512, 8: 512})) and eng.runner.frozen
    h = eng.health()
    for k in ("ok", "engine", "api", "readout", "flags", "config_sha256", "quantization", "graphs", "batcher", "queue"):
        assert k in h
    assert h["engine"] == "hf" and h["readout"]["max_options"] == 255 and h["readout"]["layout"] == "schema_branch_mark"


@pytest.mark.parametrize("arm", ["A0", "A1", "A2"])
def test_decide_equals_predict_per_arm(setup, sample, reference, arm):
    *_, eng, _ = setup
    v = eng.set_flags(ARM_FLAGS[arm])
    assert all(v[k] == x for k, x in ARM_FLAGS[arm].items())
    worst, paths = 0.0, set()
    for r in sample:
        out = eng.decide(request_from_row(r, "q"))
        assert out["id"] == r["id"] and out["engine"] == "hf" and set(out["answers"]) == {"q"}
        assert set(out["timing"]) == {"tokenize_ms", "queue_ms", "model_ms", "total_ms"}
        a = out["answers"]["q"]
        worst = max(worst, _diff(a, r, reference[r["id"]]))
        views = 2 if r["qtype"] == "choice" else 1
        assert a["usage"]["views"] == views and out["usage"]["input_tokens"] == a["usage"]["input_tokens"]
        assert out["usage"]["routed_rows"] == 0
        paths.add(out["path"])
        if arm == "A1":
            assert out["batch_rows"] == 1 and len(out["shapes"]) == views
        if arm == "A0":
            assert out["batch_rows"] == views and len(out["shapes"]) == 1
    assert worst <= TOL, (arm, worst)
    assert "graph" in paths


def test_identity_tokens_match_decoder_io(setup, sample):
    tok, ro, model, eng, _ = setup
    eng.set_flags(ARM_FLAGS["A2"])
    for r in sample[:6]:
        out = eng.decide(request_from_row(r))
        n = len(tok(ro.prompt(r), add_special_tokens=False)["input_ids"])
        assert out["answers"]["q0"]["usage"]["input_tokens_first_view"] == n


def test_concurrent_a2_equals_reference(setup, sample, reference):
    *_, eng, _ = setup
    eng.set_flags(ARM_FLAGS["A2"])
    errs, worst, rows_seen = [], [0.0], []

    def worker(t):
        try:
            for j in range(3):
                r = sample[(t * 3 + j) % len(sample)]
                out = eng.decide(request_from_row(r))
                worst[0] = max(worst[0], _diff(out["answers"]["q0"], r, reference[r["id"]]))
                rows_seen.append(out["batch_rows"])
        except BaseException as e:  # noqa: BLE001
            errs.append(e)
    ts = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
    for t in ts:
        t.start()
    for t in ts:
        t.join(120)
    assert not errs, errs[:2]
    assert worst[0] <= TOL and len(rows_seen) == 24


def test_multi_question_request(setup, sample, reference):
    *_, eng, _ = setup
    eng.set_flags(ARM_FLAGS["A2"])
    rs = [r for r in sample if len(r["options"] or []) <= 26][:5]
    req = {"state": rs[0]["state"], "questions": {}}
    for i, r in enumerate(rs):
        q = request_from_row(r)["questions"]["q0"]
        req["questions"][f"q{i}"] = q
    out = eng.decide(req)
    rows2 = [{**r, "state": rs[0]["state"]} for r in rs]
    ref = dio.predict(eng.model, eng.tok, rows2, dev="cpu", tta_choice=True)
    for i, (r, p) in enumerate(zip(rows2, ref)):
        assert _diff(out["answers"][f"q{i}"], r, p) <= TOL
    assert out["usage"]["input_tokens"] == sum(a["usage"]["input_tokens"] for a in out["answers"].values())
    for arm in ("A0", "A1"):
        eng.set_flags(ARM_FLAGS[arm])
        o2 = eng.decide(req)
        assert max(abs(o2["answers"][k].get("noul", 0) - out["answers"][k].get("noul", 0)) for k in out["answers"]) <= TOL


def test_identity_only_reads(setup, sample):
    *_, eng, _ = setup
    eng.set_flags({**ARM_FLAGS["A2"], "choice_views": 1})
    try:
        ch = [r for r in sample if r["qtype"] == "choice"][:4]
        ref = dio.predict(eng.model, eng.tok, ch, dev="cpu")  # one read in the given order (the _pre.jsonl view)
        for r, p in zip(ch, ref):
            a = eng.decide(request_from_row(r))["answers"]["q0"]
            assert a["usage"]["views"] == 1 and _diff(a, r, p) <= TOL
    finally:
        eng.set_flags({"choice_views": 2})
    r = ch[0]
    a = eng.decide({**request_from_row(r), "return_views": True})["answers"]["q0"]
    assert len(a["view_probabilities"]) == 2
    avg = {o: (a["view_probabilities"][0][o] + a["view_probabilities"][1][o]) / 2 for o in r["options"]}
    assert avg == a["probabilities"]


def test_layout_guard(monkeypatch):
    tok, ro = T.c1_tokenizer(), T.readout()
    monkeypatch.setattr(dio, "LAYOUT", "text_first")  # a host that forgot decoder_io.load's layout would serve wrong prompts
    with pytest.raises(RuntimeError, match="layout"):
        FastEngine(T.tiny_model(), tok, ro=ro)


def test_errors_flags_and_close(sample):
    tok, ro = T.c1_tokenizer(), T.readout()
    eng = FastEngine(T.tiny_model(seed=3), tok, ro=ro, log=lambda *a: None)
    eng.boot(graphs=False, eager_warmup={}, warm_requests=0)
    with pytest.raises(RequestError):
        eng.decide({"state": "x", "questions": {}})
    with pytest.raises(RequestError):
        eng.set_flags({"cross_batch": "yes"})
    with pytest.raises(RequestError):
        eng.set_flags(["legacy"])
    sha = eng.config_sha256()
    eng.set_flags({"legacy": True})
    assert eng.config_sha256() != sha and eng.health()["flags"]["effective"]["graph_plan"] == "legacy"
    out = eng.decide(request_from_row(sample[0]))
    assert out["path"] == "eager" and eng.flush()["ok"]
    assert eng.close()
    with pytest.raises(EngineClosed):
        eng.decide(request_from_row(sample[0]))
