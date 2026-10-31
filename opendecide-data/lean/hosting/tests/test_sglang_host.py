"""SGLang arm (S1/S2) on CPU: hosting/sglang_host.py (front end, /generate request + response, HTTP API v1, payer
guard, server args, container helpers) and hosting/export_c1_merged.py (merged checkpoint writer + every check), with
a tiny random Qwen3.5 hybrid model and the C1 tokenizer.

The fake SGLang computes what the real one returns for a prefill-only scoring request: per sequence, the fp32
log_softmax of h_last @ lm_head.T over the whole vocabulary, read at the requested candidate ids (returned in a
shuffled order). The front end's answers must then equal decoder_io.predict(tta_choice=True) on the same model.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_sglang_host.py -q
No GPU, no network, no Modal call; reads only the gate dev splits, the local C1 tokenizer backup and (if present) the
small files of the local Qwen3.5-4B HF cache snapshot.
"""
import json
import os
import random
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import httpx
import pytest
import torch

HOSTING = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HOSTING))
import export_c1_merged as E  # noqa: E402
import sglang_host as S  # noqa: E402
from fastcore import EngineClosed, RequestError, request_from_row  # noqa: E402
from fastcore import readout as R  # noqa: E402
from fastcore import testing as T  # noqa: E402

dio = R.dio
TOL = 1e-5
PY = sys.executable


# ------------------------------------------------------------------ fakes

class FakeSGLang:
    """In-process stand-in for SGLang's /generate (prefill-only scoring) on a tiny model: exact fp32 logprobs."""

    def __init__(self, model):
        self.model, self.calls, self.aborted, self.flushes = model, [], [], 0
        self.mutate, self.raise_exc, self.alive_ = None, None, True
        self.base_url = "fake://sglang"

    def logprobs(self, ids):
        body, head = dio._parts(self.model)
        with torch.no_grad():
            h = body(input_ids=torch.tensor([ids])).last_hidden_state[0, -1]
            return torch.log_softmax(h.float() @ head.weight.float().T, -1)

    def generate(self, body, timeout=None):
        self.calls.append(body)
        if self.raise_exc is not None:
            raise self.raise_exc
        out = []
        for i, (ids, cand) in enumerate(zip(body["input_ids"], body["token_ids_logprob"])):
            lp = self.logprobs(ids)
            trips = [[float(lp[t]), int(t), None] for t in cand]
            random.Random(i).shuffle(trips)  # SGLang's order need not be ours: the front end maps by token id
            out.append({"text": "", "meta_info": {"id": body["rid"][i], "prompt_tokens": len(ids), "completion_tokens": 0,
                                                  "cached_tokens": 0, "e2e_latency": 0.001,
                                                  "output_token_ids_logprobs": [trips]}})
        return self.mutate(out) if self.mutate else out

    def abort(self, rids):
        self.aborted += list(rids)

    def flush(self):
        self.flushes += 1
        return {"ok": True, "tries": 1}

    def alive(self, timeout=5.0):
        return self.alive_


def good_resolved(path="/vol/models/q35_4b_main500k_merged", fp8=False):
    return {"model_path": path, "dtype": "bfloat16", "quantization": "fp8" if fp8 else None, "enable_fp32_lm_head": True,
            "context_length": S.CONTEXT_LEN, "disable_radix_cache": False, "mamba_radix_cache_strategy": "extra_buffer",
            "mamba_ssm_dtype": "float32", "linear_attn_backend": "triton", "linear_attn_prefill_backend": "triton",
            "speculative_algorithm": None,
            "sampling_defaults": "openai", "random_seed": 0, "max_running_requests": 64, "max_mamba_cache_size": 400,
            "version": S.SGLANG_VERSION, "enable_lora": False, "lora_paths": None, "cuda_graph_max_bs_decode": 64,
            "disable_prefill_cuda_graph": False}


class FakeSGLangHTTP:
    """A local HTTP server speaking the SGLang routes the host uses: /generate, /flush_cache (400 while 'busy'),
    /abort_request, /health, /server_info."""

    def __init__(self, fake, flush_busy=0, delay=0.0):
        self.fake, self.flush_busy, self.delay = fake, flush_busy, delay
        self.flush_calls, self.aborts, self.generate_status = 0, [], 200
        me = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def _send(self, code, body, ctype="application/json"):
                b = body if isinstance(body, bytes) else (json.dumps(body).encode() if ctype == "application/json"
                                                          else body.encode())
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)

            def do_GET(self):
                if self.path == "/health":
                    self._send(200, b"", "text/plain")
                elif self.path == "/server_info":
                    self._send(200, good_resolved())
                else:
                    self._send(404, {"error": "nf"})

            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                if self.path == "/generate":
                    if me.delay:
                        time.sleep(me.delay)
                    if me.generate_status != 200:
                        self._send(me.generate_status, {"error": {"message": "input too long"}})
                        return
                    self._send(200, me.fake.generate(json.loads(raw)))
                elif self.path == "/flush_cache":
                    me.flush_calls += 1
                    if me.flush_busy > 0:
                        me.flush_busy -= 1
                        self._send(400, "Flush cache failed.\n", "text/plain")
                    else:
                        self._send(200, "Cache flushed.\nPlease check backend logs for more details.\n", "text/plain")
                elif self.path == "/abort_request":
                    me.aborts.append(json.loads(raw).get("rid"))
                    self._send(200, b"", "text/plain")
                else:
                    self._send(404, {"error": "nf"})

            def log_message(self, *a):
                pass

        class Srv(ThreadingHTTPServer):
            daemon_threads = True

        self.srv = Srv(("127.0.0.1", 0), H)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


# ------------------------------------------------------------------ fixtures

@pytest.fixture(scope="module")
def tok():
    return T.c1_tokenizer()


@pytest.fixture(scope="module")
def ro(tok):
    return T.readout()


@pytest.fixture(scope="module")
def model(tok):
    return T.tiny_model(seed=3)


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
def reference(model, tok, sample):
    two = dio.predict(model, tok, sample, dev="cpu", tta_choice=True)
    one = dio.predict(model, tok, sample, dev="cpu", tta_choice=False)
    return {r["id"]: {"served": a, "identity": b} for r, a, b in zip(sample, two, one)}


@pytest.fixture()
def fe(tok, ro, model):
    fake = FakeSGLang(model)
    return S.SGLangFrontEnd(fake, tok, ro, server_args=good_resolved(), log=lambda *a: None), fake


def _diff(ans, r, p_ref):
    if r["qtype"] == "noul":
        assert set(ans) == {"type", "noul", "probabilities", "usage"}
        return max(abs(ans["noul"] - p_ref["yes"]), abs(ans["probabilities"]["no"] - p_ref["no"]))
    assert list(ans["probabilities"]) == r["options"]
    assert ans["confidence"] == ans["probabilities"][ans["choice"]] == max(ans["probabilities"].values())
    return max(abs(ans["probabilities"][o] - p_ref[o]) for o in r["options"])


# ------------------------------------------------------------------ request building

def test_generate_body_is_the_hf_path(tok, ro, sample):
    """input_ids = decoder_io's own tokenization of ro.prompt(row, perm); token_ids_logprob = Readout.cand(row) flat,
    group by group; sequences in (question, view) order with view 1 = the exact reversal; prefill-only params."""
    for r in sample:
        named = R.parse_v1(request_from_row(r))
        items = R.build_items(ro, named)
        R.tokenize_items(tok, items)
        body = S.build_generate_body(items, "abc")
        perms = [None] + ([list(range(len(r["options"])))[::-1]] if r["qtype"] == "choice" else [])
        assert len(body["input_ids"]) == len(perms) == len(body["token_ids_logprob"]) == len(body["rid"])
        for i, perm in enumerate(perms):
            want = tok(dio.prompt_texts(ro, [r], [perm])[0], add_special_tokens=False, truncation=True,
                       max_length=dio.MAX_LEN)["input_ids"]
            assert body["input_ids"][i] == list(want)
            assert body["token_ids_logprob"][i] == [t for g in ro.cand(r) for t in g]
        assert body["sampling_params"] == S.SAMPLING and body["sampling_params"]["max_new_tokens"] == 0
        assert body["return_logprob"] is True and body["logprob_start_len"] == -1 and body["stream"] is False
        assert body["rid"] == [f"abc-{i}" for i in range(len(perms))]
        json.dumps(body)  # plain JSON (ints, no tensors)
    with pytest.raises(ValueError):
        S.build_generate_body(R.build_items(ro, R.parse_v1(request_from_row(sample[0]))))  # not tokenized


def test_known_logits_round_trip(tok, ro, sample):
    """Mock /generate built from KNOWN full-vocabulary logits: the per-group values the front end derives from the
    logprobs give decoder_io.to_probs exactly what the raw logits give (shift invariance), for every view."""
    g = torch.Generator().manual_seed(0)
    for r in sample[:8]:
        items = R.build_items(ro, R.parse_v1(request_from_row(r)))
        R.tokenize_items(tok, items)
        raw = [torch.randn(len(tok), generator=g) * 4 for _ in items]
        resp = []
        for it, lg in zip(items, raw):
            lp = torch.log_softmax(lg, -1)
            resp.append({"meta_info": {"prompt_tokens": it.n_tokens, "output_token_ids_logprobs":
                                       [[[float(lp[t]), t, None] for t in reversed(it.flat)]]}})
        got, meta = S.parse_generate_response(items, resp)
        assert meta["prompt_tokens"] == sum(it.n_tokens for it in items) and meta["cached_tokens"] is None
        for it, lg, g_ in zip(items, raw, got):
            want = torch.stack([torch.logsumexp(lg[gr], 0) for gr in it.groups])
            p1, p2 = dio.to_probs(r, want, it.perm), dio.to_probs(r, g_, it.perm)
            assert max(abs(p1[k] - p2[k]) for k in p1) < 1e-6
        named = R.parse_v1(request_from_row(r))
        a1, _ = R.combine(named, items, got)
        a2, _ = R.combine(named, items, [torch.stack([torch.logsumexp(lg[gr], 0) for gr in it.groups])
                                         for it, lg in zip(items, raw)])
        p1, p2 = a1["q0"]["probabilities"], a2["q0"]["probabilities"]
        assert max(abs(p1[k] - p2[k]) for k in p1) < 1e-6


# ------------------------------------------------------------------ the front end vs decoder_io

def test_answers_equal_decoder_io_predict(fe, sample, reference):
    fe, fake = fe
    worst = 0.0
    for r in sample:
        n_calls = len(fake.calls)
        out = fe.decide({**request_from_row(r, "q"), "return_views": True})
        assert len(fake.calls) == n_calls + 1  # ONE /generate per API request
        assert out["id"] == r["id"] and out["engine"] == "sglang" and out["path"] == "sglang"
        assert set(out["timing"]) == {"tokenize_ms", "queue_ms", "model_ms", "readout_ms", "total_ms"}
        a = out["answers"]["q"]
        views = 2 if r["qtype"] == "choice" else 1
        assert out["batch_rows"] == views and a["usage"]["views"] == views
        assert out["usage"]["input_tokens"] == a["usage"]["input_tokens"] and out["usage"]["routed_rows"] == 0
        assert out["usage"]["cached_tokens"] == 0
        worst = max(worst, _diff({k: v for k, v in a.items() if k != "view_probabilities"}, r,
                                 reference[r["id"]]["served"]))
        if r["qtype"] == "choice":  # view 0 = the identity read (decoder_io.predict without TTA)
            v0 = a["view_probabilities"][0]
            worst = max(worst, max(abs(v0[o] - reference[r["id"]]["identity"][o]) for o in r["options"]))
            assert out["sglang"]["prompt_tokens"] == a["usage"]["input_tokens"]
    assert worst <= TOL, worst


def test_multi_question_one_generate_call(fe, sample):
    fe, fake = fe
    noul = next(r for r in sample if r["qtype"] == "noul")
    choice = next(r for r in sample if r["qtype"] == "choice" and len(r["options"]) <= 9)
    wide = next(r for r in sample if r["qtype"] == "choice" and len(r["options"]) > 26)
    state = noul["state"]
    req = {"id": "m", "state": state, "questions": {}}
    for name, r in (("a", noul), ("b", choice), ("c", wide)):
        q = request_from_row({**r, "state": state})["questions"]["q0"]
        req["questions"][name] = q
    n = len(fake.calls)
    out = fe.decide(req)
    assert len(fake.calls) == n + 1 and len(fake.calls[-1]["input_ids"]) == 1 + 2 + 2 == out["batch_rows"]
    for name, r in (("a", noul), ("b", choice), ("c", wide)):
        single = fe.decide({"state": state, "questions": {name: req["questions"][name]}})["answers"][name]
        a = out["answers"][name]
        key = "noul" if r["qtype"] == "noul" else "probabilities"
        if key == "noul":
            assert abs(a["noul"] - single["noul"]) < 1e-7
        else:
            assert max(abs(a[key][o] - single[key][o]) for o in r["options"]) < 1e-7


def test_choice_views_flag(fe, sample, reference):
    fe, fake = fe
    view = fe.set_flags({"choice_views": 1})
    assert view["choice_views"] == 1 and view["effective"]["choice_views"] == 1
    r = next(r for r in sample if r["qtype"] == "choice")
    out = fe.decide(request_from_row(r))
    assert out["batch_rows"] == 1 and len(fake.calls[-1]["input_ids"]) == 1
    assert _diff(out["answers"]["q0"], r, reference[r["id"]]["identity"]) <= TOL
    fe.set_flags({"choice_views": 2})
    assert fe.decide(request_from_row(r))["batch_rows"] == 2


def test_flag_errors_all_or_nothing(fe):
    fe, _ = fe
    before = fe.flags_view()
    for bad in ({"cross_batch": True}, {"legacy": True}, {"choice_views": 3}, {"choice_views": True},
                {"timeout_s": 0}, {"timeout_s": "5"}, {"choice_views": 1, "max_rows": 4}, "x"):
        with pytest.raises(RequestError):
            fe.set_flags(bad)
        assert fe.flags_view() == before
    assert fe.set_flags({"timeout_s": 30})["timeout_s"] == 30.0


def test_bad_requests_never_reach_sglang(fe, sample):
    fe, fake = fe
    r = next(r for r in sample if r["qtype"] == "choice")
    good = request_from_row(r)
    q = good["questions"]["q0"]
    bads = [{**good, "extra": 1}, {"questions": good["questions"]}, {**good, "questions": {}},
            {**good, "questions": {f"q{i}": q for i in range(17)}},
            {**good, "questions": {"q": {**q, "options": ["only"]}}},
            {**good, "questions": {"q": {**q, "options": ["a", "a"]}}},
            {**good, "questions": {"q": {**q, "criteria": {"a": None}}}},
            {**good, "questions": {"q": {"type": "noul", "instructions": "x", "options": ["a", "b"]}}},
            {**good, "return_views": "yes"}]
    n = len(fake.calls)
    for b in bads:
        with pytest.raises(RequestError):
            fe.decide(b)
        assert S.http_status(RequestError("x")) == 400
    assert len(fake.calls) == n


@pytest.mark.parametrize("case", ["drop", "prompt_tokens", "short", "nan", "order", "none", "no_meta", "pos_inf"])
def test_upstream_answer_errors(fe, sample, case):
    fe, fake = fe
    r = next(r for r in sample if r["qtype"] == "choice")

    def mutate(out):
        mi = out[0]["meta_info"]
        trips = mi["output_token_ids_logprobs"][0]
        if case == "drop":
            trips.pop()
        elif case == "prompt_tokens":
            mi["prompt_tokens"] += 1
        elif case == "short":
            out = out[:1]
        elif case == "nan":
            trips[0][0] = float("nan")
        elif case == "order":
            out[0]["meta_info"]["id"], out[1]["meta_info"]["id"] = out[1]["meta_info"]["id"], out[0]["meta_info"]["id"]
        elif case == "none":
            trips[0][0] = None
        elif case == "no_meta":
            del out[0]["meta_info"]
        elif case == "pos_inf":
            trips[0][0] = float("inf")
        return out
    fake.mutate = mutate
    with pytest.raises(S.UpstreamError) as ei:
        fe.decide(request_from_row(r))
    assert S.http_status(ei.value) == 502
    assert fe.stats()["upstream_errors"] >= 1


def test_neg_inf_candidate_is_a_zero_probability(fe, ro, sample):
    """A -inf logprob (probability 0) is legal: letter A's whole group at -inf in both views gives the first displayed
    option of each view probability 0, and the 2view average stays a distribution."""
    fe, fake = fe
    r = next(r for r in sample if r["qtype"] == "choice" and len(r["options"]) <= 9)
    a_ids = set(ro.cand(r)[0])

    def mutate(out):
        for o in out:
            for t in o["meta_info"]["output_token_ids_logprobs"][0]:
                if t[1] in a_ids:
                    t[0] = float("-inf")
        return out
    fake.mutate = mutate
    a = fe.decide({**request_from_row(r), "return_views": True})["answers"]["q0"]
    v0, v1 = a["view_probabilities"]
    assert v0[r["options"][0]] == 0.0 and v1[r["options"][-1]] == 0.0
    assert abs(sum(a["probabilities"].values()) - 1) < 1e-6


def test_timeout_unavailable_closed(fe, sample):
    fe, fake = fe
    r = sample[0]
    fake.raise_exc = S.UpstreamTimeout("slow")
    with pytest.raises(S.UpstreamTimeout) as ei:
        fe.decide(request_from_row(r))
    assert S.http_status(ei.value) == 504 and fake.aborted == fake.calls[-1]["rid"]
    fake.raise_exc = S.UpstreamUnavailable("down")
    with pytest.raises(S.UpstreamUnavailable) as ei:
        fe.decide(request_from_row(r))
    assert S.http_status(ei.value) == 503
    fake.raise_exc = None
    fake.alive_ = False
    assert fe.health()["ok"] is False
    fake.alive_ = True
    fe.close()
    with pytest.raises(EngineClosed) as ei:
        fe.decide(request_from_row(r))
    assert S.http_status(ei.value) == 503 and fe.health()["ok"] is False
    assert S.http_status(TimeoutError()) == 504 and S.http_status(KeyError("x")) == 500


def test_health_and_config_hash(fe):
    fe, _ = fe
    h = fe.health()
    for k in ("ok", "engine", "api", "readout", "flags", "config_sha256", "quantization", "graphs", "server_args",
              "sglang", "batcher", "queue"):
        assert k in h
    assert h["engine"] == "sglang" and h["quantization"] is None and h["readout"]["max_options"] == 255
    assert h["readout"]["layout"] == "schema_branch_mark" and h["readout"]["sampling"] == S.SAMPLING
    assert h["server_args"]["enable_fp32_lm_head"] is True and h["graphs"]["engine"] == "sglang"
    sha = h["config_sha256"]
    fe.set_flags({"choice_views": 1})
    assert fe.health()["config_sha256"] != sha
    fe.set_flags({"choice_views": 2})
    assert fe.health()["config_sha256"] == sha


def test_boot_probe_and_warm(fe, tok, ro):
    fe, fake = fe
    want = S.probe_digest(ro, tok)
    assert want == S.probe_digest(ro, tok) and want["items"] == 1 + 2 + 1 + 2 + 2  # EXAMPLE noul+choice, card, wide, utf8
    rep = fe.boot(warm_requests=3, probe_sha256=want["sha256"])
    assert rep["probe"]["match"] is True and len(rep["warm"]) == 3 and fake.flushes == 1
    assert fe.stats()["requests"] == 0  # warm-up not counted
    with pytest.raises(RuntimeError):
        fe.boot(warm_requests=0, probe_sha256="0" * 64)


def test_concurrent_decides(fe, sample, reference):
    fe, _ = fe
    errs, worst = [], [0.0]

    def worker(t):
        try:
            for j in range(3):
                r = sample[(t * 3 + j) % len(sample)]
                out = fe.decide(request_from_row(r))
                worst[0] = max(worst[0], _diff(out["answers"]["q0"], r, reference[r["id"]]["served"]))
        except BaseException as e:  # noqa: BLE001
            errs.append(e)
    ts = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert not errs and worst[0] <= TOL
    st = fe.stats()
    assert st["requests"] == 24 and st["inflight"] == 0 and 1 <= st["inflight_max"] <= 8


# ------------------------------------------------------------------ HTTP: front end served against a fake SGLang server

def test_http_frontend_against_fake_sglang(tok, ro, model, sample, reference):
    fake = FakeSGLang(model)
    up = FakeSGLangHTTP(fake, flush_busy=2)
    client = S.SGLangClient(up.url, timeout=30)
    fe = S.SGLangFrontEnd(client, tok, ro, server_args=client.server_info(), log=lambda *a: None)
    stop = threading.Event()
    host = {"model": "q35_4b_main500k", "adapter_sha256": S.C1_ADAPTER_SHA256, "base": S.BASE,
            "revision": S.REVISION, "gpu": "fake", "region": None, "boot_s": 1.0, "boot": {}}
    srv, st = S.make_frontend_server(0, "tok", fe, host, stop.set, host="127.0.0.1")
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}"
    try:
        with httpx.Client(base_url=url, timeout=60, headers={"Authorization": "Bearer tok"}) as c:
            assert httpx.get(url + "/health").status_code == 401
            assert httpx.post(url + "/decide", json={}).status_code == 401
            assert c.get("/ping").json() == {"ok": True}
            for r in sample[:6]:
                d = c.post("/decide", json=request_from_row(r)).json()
                assert _diff(d["answers"]["q0"], r, reference[r["id"]]["served"]) <= TOL
                assert d["server_ms"] >= d["timing"]["total_ms"] * 0.5 and d["engine"] == "sglang"
            bad = c.post("/decide", json={"state": 1})
            assert bad.status_code == 400 and "state" in bad.json()["error"]
            assert c.post("/decide", content=b"{not json").status_code == 400
            h = c.get("/health").json()
            assert h["engine"] == "sglang" and h["adapter_sha256"] == S.C1_ADAPTER_SHA256 and h["ok"] is True
            assert h["served"] == 6 and h["errors"] == 2 and h["batcher"]["requests"] == 6
            assert h["quantization"] is None and h["server_args"]["mamba_radix_cache_strategy"] == "extra_buffer"
            h2 = c.post("/admin/config", json={"flags": {"choice_views": 1}}).json()
            assert h2["flags"]["choice_views"] == 1 and h2["engine"] == "sglang"
            assert c.post("/admin/config", json={"flags": {"cross_batch": False}}).status_code == 400
            assert c.post("/admin/config", json={"choice_views": 2}).status_code == 400
            assert c.post("/admin/config", json={"flags": {"choice_views": 2}}).json()["flags"]["choice_views"] == 2
            f = c.post("/admin/flush").json()
            assert f["ok"] and f["tries"] == 3 and up.flush_calls == 3  # retried while SGLang said "busy"
            up.generate_status = 400
            e = c.post("/decide", json=request_from_row(sample[0]))
            assert e.status_code == 502 and "input too long" in e.json()["error"]
            up.generate_status = 200
            assert c.post("/nope").status_code == 404
            assert c.post("/shutdown").json()["ok"] and stop.is_set()
    finally:
        srv.shutdown()
        srv.server_close()
        client.close()
        up.close()


def _free_port():
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.mark.parametrize("case", ["timeout", "dead"])
def test_http_timeout_and_dead_sglang(tok, ro, model, sample, case):
    fake = FakeSGLang(model)
    up = FakeSGLangHTTP(fake, delay=2.5) if case == "timeout" else None
    client = S.SGLangClient(up.url if up else f"http://127.0.0.1:{_free_port()}")
    fe = S.SGLangFrontEnd(client, tok, ro, flags={"timeout_s": 1.0}, log=lambda *a: None)
    srv, _ = S.make_frontend_server(0, "t", fe, {}, lambda: None, host="127.0.0.1")
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}"
    r = next(r for r in sample if r["qtype"] == "choice")
    try:
        with httpx.Client(base_url=url, timeout=60, headers={"Authorization": "Bearer t"}) as c:
            resp = c.post("/decide", json=request_from_row(r))
            if case == "timeout":  # 504, and every sequence of the abandoned request is aborted in SGLang
                assert resp.status_code == 504 and "within the 1.0 s request timeout" in resp.json()["error"]
                assert len(up.aborts) == 2 and len({a.rsplit("-", 1)[0] for a in up.aborts}) == 1
                assert [a.rsplit("-", 1)[1] for a in up.aborts] == ["0", "1"]
            else:  # nothing listening: 503, and /health says not ok
                assert resp.status_code == 503 and "unreachable" in resp.json()["error"]
                assert c.get("/health").json()["ok"] is False
    finally:
        srv.shutdown()
        srv.server_close()
        client.close()
        if up:
            up.close()


def test_frontend_process_without_modal(tmp_path, model):
    """The container's front end: this file run as a script under a Python with NO modal client (as /opt/fastpath),
    against a fake SGLang server: boots (tokenizer from a c1_tokenizer dir, probe, warm-up, flush), writes the ready
    file, serves API v1, stops on POST /shutdown and writes the done file."""
    fake = FakeSGLang(model)
    up = FakeSGLangHTTP(fake)
    c1 = tmp_path / "c1_tokenizer"
    c1.mkdir()
    for n in ("tokenizer.json", "tokenizer_config.json", "train_meta.json", "chat_template.jinja"):
        shutil.copyfile(T.ADAPTER / n, c1 / n)
    probe = S.probe_digest(T.readout(), T.c1_tokenizer())["sha256"]
    cfg = {"sglang_url": up.url, "c1_tokenizer_dir": str(c1), "port": 0, "host": "127.0.0.1", "seconds": 300,
           "idle_s": 300, "quantization": None, "server_args": good_resolved(), "probe_sha256": probe,
           "host_info": {"model": "q35_4b_main500k", "adapter_sha256": S.C1_ADAPTER_SHA256, "gpu": "fake"},
           "ready_file": str(tmp_path / "ready.json"), "done_file": str(tmp_path / "done.json"), "t0": time.time()}
    (tmp_path / "cfg.json").write_text(json.dumps(cfg))
    code = ("import runpy, sys; sys.modules['modal'] = None; "  # `import modal` -> ImportError, as in /opt/fastpath
            f"sys.argv = [{str(HOSTING / 'sglang_host.py')!r}, 'frontend', '--config', {str(tmp_path / 'cfg.json')!r}]; "
            f"runpy.run_path({str(HOSTING / 'sglang_host.py')!r}, run_name='__main__')")
    env = {**os.environ, "OD_SGL_TOKEN": "tkn", "PYTHONPATH": ""}
    log = open(tmp_path / "frontend.log", "w")
    p = subprocess.Popen([PY, "-c", code], env=env, cwd=str(HOSTING), stdout=log, stderr=subprocess.STDOUT, text=True)
    try:
        t0 = time.time()
        while not (tmp_path / "ready.json").exists():
            assert p.poll() is None, (tmp_path / "frontend.log").read_text()[-3000:]
            assert time.time() - t0 < 240
            time.sleep(0.5)
        ready = json.loads((tmp_path / "ready.json").read_text())
        assert ready["ok"] and ready["health"]["engine"] == "sglang" and ready["health"]["gpu"] == "fake"
        assert 0 < ready["health"]["serve_remaining_s"] <= 300 and ready["health"]["serve_deadline_unix"] > 0
        boot = ready["health"]["boot"]["frontend"]
        assert boot["probe"]["match"] is True and boot["tokenizer"]["layout"] == "schema_branch_mark"
        url = f"http://127.0.0.1:{ready['port']}"
        with httpx.Client(base_url=url, timeout=60, headers={"Authorization": "Bearer tkn"}) as c:
            d = c.post("/decide", json=probe_req()).json()
            assert set(d["answers"]) == {"q0", "q1"} and d["batch_rows"] == 3
            h = c.get("/health").json()
            assert h["boot_s"] > 0 and 0 < h["serve_remaining_s"] <= 300  # speed_bench's fit check reads it
            assert c.post("/shutdown").json()["ok"]
        assert p.wait(timeout=60) == 0
        done = json.loads((tmp_path / "done.json").read_text())
        assert done["stop"] == "shutdown request" and done["served"] == 1 and done["stats"]["requests"] == 1
        assert "FRONTEND READY" in (tmp_path / "frontend.log").read_text()
    finally:
        if p.poll() is None:
            p.kill()
        log.close()
        up.close()


def probe_req():
    return {"state": "Customer message:\nMy card payment was declined at the shop this morning.",
            "questions": {"q0": {"type": "noul", "instructions": "Is the customer reporting a declined payment?"},
                          "q1": {"type": "choice", "instructions": "Which label describes this message?",
                                 "options": ["declined card payment", "card arrival", "refund request"]}}}


def test_frontend_main_boot_failure_writes_error(tmp_path, monkeypatch):
    cfg = {"sglang_url": "http://127.0.0.1:9", "c1_tokenizer_dir": str(tmp_path / "missing"), "port": 0,
           "ready_file": str(tmp_path / "ready.json")}
    (tmp_path / "cfg.json").write_text(json.dumps(cfg))
    monkeypatch.setenv("OD_SGL_TOKEN", "x")
    assert S.frontend_main(["frontend", "--config", str(tmp_path / "cfg.json")]) == 1
    r = json.loads((tmp_path / "ready.json").read_text())
    assert r["ok"] is False and r["error"]
    monkeypatch.delenv("OD_SGL_TOKEN")
    with pytest.raises(SystemExit):
        S.frontend_main(["frontend", "--config", str(tmp_path / "cfg.json")])


# ------------------------------------------------------------------ server args, payer guard, helpers

def test_server_cmd():
    cmd = S.server_cmd("/vol/models/m", python="py")
    s = " ".join(cmd)
    for need in ("-m sglang.launch_server", "--model-path /vol/models/m", "--dtype bfloat16", "--enable-fp32-lm-head",
                 f"--context-length {S.CONTEXT_LEN}", "--mamba-radix-cache-strategy extra_buffer",
                 "--mamba-ssm-dtype float32", "--linear-attn-backend triton", "--linear-attn-prefill-backend triton",
                 "--max-running-requests 64",
                 "--max-mamba-cache-size 400", "--host 127.0.0.1", "--sampling-defaults openai"):
        assert need in s, need
    assert cmd[0] == "py" and "--quantization" not in cmd and "speculative" not in s and "--disable-radix-cache" not in s
    assert "lora" not in s and "--mem-fraction-static" not in s
    f = S.server_cmd("/m", fp8=True, max_running_requests=32, max_mamba_cache_size=256, mem_fraction_static=0.8,
                     chunked_prefill_size=8192)
    assert f[f.index("--quantization") + 1] == "fp8" and f[f.index("--max-running-requests") + 1] == "32"
    assert f[f.index("--mem-fraction-static") + 1] == "0.8" and f[f.index("--chunked-prefill-size") + 1] == "8192"
    assert S.CONTEXT_LEN > dio.MAX_LEN == S.MAX_LEN
    env = S.server_env({"PATH": "/bin", "PYTHONPATH": "/x", "VIRTUAL_ENV": "/v"})
    assert env["SGLANG_RETURN_ORIGINAL_LOGPROB"] == "1" and "PYTHONPATH" not in env and env["PATH"] == "/bin"


def test_check_server_args():
    want = S.want_server_args("/vol/models/q35_4b_main500k_merged", False)
    bad, warn = S.check_server_args(good_resolved(), want)
    assert bad == [] and warn == []
    bad, _ = S.check_server_args(good_resolved(fp8=True), S.want_server_args("/vol/models/q35_4b_main500k_merged", True))
    assert bad == []
    for k, v in (("enable_fp32_lm_head", False), ("disable_radix_cache", True), ("speculative_algorithm", "EAGLE"),
                 ("quantization", "fp8"), ("dtype", "float16"), ("mamba_ssm_dtype", "bfloat16"),
                 ("linear_attn_prefill_backend", "flashinfer"), ("linear_attn_backend", "cutedsl"), ("version", "0.5.21"), ("enable_lora", True),
                 ("context_length", 8192), ("sampling_defaults", "model")):
        bad, _ = S.check_server_args({**good_resolved(), k: v}, want)
        assert bad, k
    bad, warn = S.check_server_args({**good_resolved(), "max_running_requests": 48}, want)
    assert bad == [] and warn
    res = good_resolved()
    del res["enable_fp32_lm_head"]
    assert S.check_server_args(res, want)[0]
    res = good_resolved()
    del res["random_seed"]
    bad, warn = S.check_server_args(res, want)
    assert bad == [] and warn
    assert S.check_server_args({**good_resolved(), "quantization": "none"}, want)[0] == []


def test_payer_guard():
    ok = {"MODAL_PROFILE": "mahadikarya3"}
    run = ["/x/.venv/bin/modal", "run", "hosting/sglang_host.py", "--region", "us-east"]
    assert S.payer_guard(ok, active="mahadikarya3", argv=run) == "mahadikarya3"
    assert S.payer_guard({"MODAL_PROFILE": "mahadikarya2"}, active="mahadikarya2", argv=run) == "mahadikarya2"
    for env, active, argv in (({}, "mahadikarya3", run), ({"MODAL_PROFILE": "aryamhd"}, "aryamhd", run),
                              ({"MODAL_PROFILE": "jaypatil-duke"}, "jaypatil-duke", run),
                              ({**ok, "MODAL_TOKEN_ID": "ak-1"}, "mahadikarya3", run),
                              (ok, "aryamhd", run),
                              (ok, "mahadikarya3", ["/x/modal", "deploy", "hosting/sglang_host.py"]),
                              (ok, "mahadikarya3", ["/x/modal", "serve", "hosting/sglang_host.py"]),
                              (ok, "mahadikarya3", ["/x/modal", "run", "--detach", "hosting/sglang_host.py"]),
                              (ok, "mahadikarya3", ["/x/modal", "run", "-d", "hosting/export_c1_merged.py"])):
        with pytest.raises(SystemExit):
            S.payer_guard(env, active=active, argv=argv)
    assert E.payer_guard is S.payer_guard


def test_modal_cli_command():
    assert S.modal_cli_command(["/v/bin/modal", "run", "x.py"]) == "run"
    assert S.modal_cli_command(["/v/lib/modal/__main__.py", "--help", "deploy", "x.py"]) == "deploy"
    assert S.modal_cli_command(["/v/bin/pytest", "run"]) is None
    assert S.modal_cli_command(["sglang_host.py", "frontend"]) is None
    assert S.modal_cli_command([]) is None


def test_smoke_compare():
    pairs = [("noul", None, {"yes": 0.8, "no": 0.2}, {"noul": 0.7}),
             ("choice", ["a", "b"], {"a": 0.4, "b": 0.6}, {"probabilities": {"a": 0.45, "b": 0.55}}),
             ("choice", ["a", "b"], {"a": 0.6, "b": 0.4}, {"probabilities": {"a": 0.3, "b": 0.7}}),
             ("noul", None, {"yes": 0.5, "no": 0.5}, None)]
    out = S.smoke_compare(pairs)
    assert out["n"] == 4 and out["argmax_agree"] == 0.5 and out["max_abs_dp"] == 1.0


def test_session_files(tmp_path):
    """speed/session_url.json + session_token.txt: hosting/fast_host.py's files and keys, mode 0600; ended at stop."""
    f, t = tmp_path / "speed" / "session_url.json", tmp_path / "speed" / "session_token.txt"
    rec = S.write_session(f, "https://x.modal.host", "tok123", {"choice_views": 2}, token_path=t,
                          extra={"payer": "mahadikarya3", "arm": "S1", "engine": "sglang", "adapter_sha256": "a"})
    on_disk = json.loads(f.read_text())
    assert on_disk == rec and on_disk["url"] == "https://x.modal.host" and on_disk["token"] == "tok123"
    assert {"started_at", "flags", "payer", "arm"} <= set(on_disk) and t.read_text() == "tok123\n"
    assert (f.stat().st_mode & 0o777) == 0o600 and (t.stat().st_mode & 0o777) == 0o600
    ended = S.end_session(f, "shutdown request")
    again = json.loads(f.read_text())
    assert ended == again and again["stop"] == "shutdown request" and again["ended_at"]
    assert again["started_at"] == on_disk["started_at"] and again["arm"] == "S1" and again["token"] == "tok123"
    assert S.end_session(tmp_path / "missing.json", "x") is None


def test_launcher_defaults_and_bench_command():
    """Region any by default (us-east = x1.75 is opt-in), and the printed speed_bench command ends the session itself
    (--shutdown-after: no idle GPU tail)."""
    import inspect
    sig = inspect.signature(S.main.info.raw_f).parameters
    assert sig["region"].default == "any" and sig["max_usd"].default == 6.0
    src = Path(S.__file__).read_text()
    assert '--arms {arm} --shutdown-after --go' in src


def test_cost_and_timeouts():
    est = S.cost_estimate(1500, 1.75)
    assert est["worst_usd"] < 6.0 and est["rate_usd_h"] > S.RATE_USD_H
    assert 1500 + S.BOOT_BUDGET_S <= S.FUNCTION_TIMEOUT_S
    assert E.cost_estimate()["worst_usd"] < 1.0 and E.cost_estimate("H100!")["worst_usd"] < 4.0


def test_process_helpers(tmp_path):
    p = subprocess.Popen([PY, "-c", "import time; print('hello', flush=True); time.sleep(120)"], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, start_new_session=True)
    tail = S.deque(maxlen=10)
    S.pump(p, tail, "[t]")
    t0 = time.time()
    while not tail and time.time() - t0 < 20:
        time.sleep(0.05)
    assert list(tail) == ["hello"]
    with pytest.raises(RuntimeError):
        S.wait_http_ready("http://127.0.0.1:9", p, timeout_s=0.5)  # alive but never ready
    t0 = time.time()
    S.stop_process(p, grace=5)
    assert p.poll() is not None and time.time() - t0 < 10
    q = subprocess.Popen([PY, "-c", "print('boom')"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         start_new_session=True)
    q.wait()
    with pytest.raises(RuntimeError, match="exited"):
        S.wait_http_ready("http://127.0.0.1:9", q, timeout_s=30, tail=["boom"])
    assert S.stop_process(None) is None


# ------------------------------------------------------------------ export_c1_merged on a tiny fake Qwen3.5 base

C1_REGEX = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"


@pytest.fixture(scope="module")
def fake_c1(tmp_path_factory):
    """A tiny Qwen3_5ForConditionalGeneration checkpoint laid out like the real base (BF16, A_log and the gated norm
    in F32, a vision tower, an MTP tensor, several shards + index, README) and a LoRA on it with C1's target regex,
    train_meta (C1's layout/style) and the C1 tokenizer files."""
    from peft import LoraConfig, get_peft_model
    from safetensors import safe_open
    from safetensors.torch import save_file
    from transformers import AutoModelForCausalLM, Qwen3_5Config, Qwen3_5ForConditionalGeneration
    root = tmp_path_factory.mktemp("fake_c1")
    tc = dict(vocab_size=512, hidden_size=64, intermediate_size=128, num_hidden_layers=4,
              layer_types=["linear_attention", "full_attention", "linear_attention", "full_attention"],
              num_attention_heads=4, num_key_value_heads=2, head_dim=16, linear_num_key_heads=2,
              linear_num_value_heads=4, linear_key_head_dim=16, linear_value_head_dim=16, linear_conv_kernel_dim=4,
              tie_word_embeddings=True, pad_token_id=0, mamba_ssm_dtype="float32")
    vc = dict(depth=1, hidden_size=32, intermediate_size=64, num_heads=2, out_hidden_size=64, patch_size=4,
              spatial_merge_size=2, temporal_patch_size=2, num_position_embeddings=16)
    torch.manual_seed(0)
    vl = Qwen3_5ForConditionalGeneration(Qwen3_5Config(text_config=tc, vision_config=vc, tie_word_embeddings=True))
    vl = vl.to(torch.bfloat16)
    with torch.no_grad():
        for n, p in vl.named_parameters():
            if n.endswith("linear_attn.A_log") or n.endswith("linear_attn.norm.weight"):
                p.data = (p.data.float() + torch.rand_like(p.data.float()) * 1e-3)  # F32 values bf16 cannot hold
    base = root / "base"
    vl.save_pretrained(base, max_shard_size="300KB")
    idx = json.loads((base / "model.safetensors.index.json").read_text())
    last = sorted(set(idx["weight_map"].values()))[-1]
    with safe_open(str(base / last), "pt") as f:
        ts, meta = {k: f.get_tensor(k) for k in f.keys()}, f.metadata()
    ts["mtp.fc.weight"] = torch.randn(64, 128).to(torch.bfloat16)
    save_file(ts, str(base / last), metadata=meta)
    idx["weight_map"]["mtp.fc.weight"] = last
    (base / "model.safetensors.index.json").write_text(json.dumps(idx))
    (base / "README.md").write_text("not copied")
    (base / "preprocessor_config.json").write_text("{}")
    m = AutoModelForCausalLM.from_pretrained(base, dtype=torch.bfloat16)
    pm = get_peft_model(m, LoraConfig(r=4, lora_alpha=8, lora_dropout=0.0, target_modules=C1_REGEX))
    with torch.no_grad():
        for n, p in pm.named_parameters():
            if "lora_B" in n:
                p.normal_(0, 0.05)
    ad = root / "adapter"
    pm.save_pretrained(ad)
    for n in ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja"):
        shutil.copyfile(T.ADAPTER / n, ad / n)
    (ad / "train_meta.json").write_text(json.dumps({"cfg": {"layout": "schema_branch_mark", "style": "cygnet"}}))
    return {"root": root, "base": base, "adapter": ad, "sha": E.sha256_file(ad / "adapter_model.safetensors")}


@pytest.fixture(scope="module")
def exported(fake_c1):
    out = fake_c1["root"] / "out_base"
    man = E.export_local(fake_c1["base"], fake_c1["base"], fake_c1["adapter"], out, layout="base", revision=None,
                         adapter_sha=fake_c1["sha"], sample=12, log=lambda *a: None)
    return out, man


def test_ckpt_to_mem():
    assert E.ckpt_to_mem("model.language_model.layers.3.self_attn.q_proj.weight") == "model.layers.3.self_attn.q_proj.weight"
    assert E.ckpt_to_mem("model.layers.3.mlp.up_proj.weight") == "model.layers.3.mlp.up_proj.weight"
    assert E.ckpt_to_mem("model.visual.blocks.0.attn.qkv.weight") is None and E.ckpt_to_mem("mtp.fc.weight") is None
    assert E.ckpt_to_mem("lm_head.weight") == "lm_head.weight" and E.ckpt_to_mem("other.x") is None
    assert (E.MERGED_NAME, E.C1_ADAPTER_SHA256, E.MANIFEST, E.C1_TOKENIZER_SUBDIR) == \
        (S.MERGED_NAME, S.C1_ADAPTER_SHA256, S.MANIFEST, S.C1_TOKENIZER_SUBDIR)


def test_export_base_layout(fake_c1, exported):
    from safetensors import safe_open
    from transformers import AutoModelForCausalLM
    out, man = exported
    base = fake_c1["base"]
    c = man["checks"]
    assert c["passed"] and not c["problems"] and man["layout"] == "base" and man["adapter_sha256"] == fake_c1["sha"]
    assert c["write"]["n_merged"] == 30 and c["write"]["tied_lm_head"] is True and c["write"]["n_copied_base"] >= 2
    assert len(c["write"]["rounded_like_hf"]) == 4  # 2 GDN layers x (A_log, norm.weight)
    assert c["verify_in_memory"]["ok"] and c["verify_fresh_merge"]["ok"] and c["verify_fresh_merge"]["same_targets"]
    assert c["formula"]["ok"] and c["formula"]["bitwise_all"] and c["formula"]["n"] == 12 and c["base_copies"]["ok"]
    assert man["config"]["architectures"] == ["Qwen3_5ForConditionalGeneration"]
    assert man["config"]["mamba_ssm_dtype"] == "float32" and man["config"]["tie_word_embeddings"] is True
    assert (out / "config.json").read_bytes() == (base / "config.json").read_bytes()
    assert (out / "model.safetensors.index.json").read_bytes() == (base / "model.safetensors.index.json").read_bytes()
    assert not (out / "README.md").exists() and (out / "preprocessor_config.json").exists()
    assert set(man["c1_tokenizer"]) == {"tokenizer.json", "tokenizer_config.json", "train_meta.json",
                                         "chat_template.jinja", "adapter_config.json"}
    files = E.file_manifest(out)
    assert files == man["files"] and S.MANIFEST not in files and "c1_tokenizer/train_meta.json" in files
    for sh in E.shard_names(base):  # same keys, dtypes, shapes as the base
        with safe_open(str(base / sh), "pt") as fb, safe_open(str(out / sh), "pt") as fo:
            assert list(fb.keys()) == list(fo.keys())
            for k in fb.keys():
                assert fb.get_slice(k).get_dtype() == fo.get_slice(k).get_dtype()
    # The exported folder, loaded the way decoder_io loads the base, IS the merged model (bitwise, every tensor)
    merged, _, _, _ = E.merge_c1(base, fake_c1["adapter"], "cpu", None, log=lambda *a: None)
    re = AutoModelForCausalLM.from_pretrained(out, dtype=torch.bfloat16)
    a, b = merged.state_dict(), re.state_dict()
    assert set(a) == set(b) and all(torch.equal(a[k], b[k]) for k in a)
    x = torch.randint(0, 512, (1, 17))
    with torch.no_grad():
        assert torch.equal(merged(input_ids=x).logits, re(input_ids=x).logits)


def test_export_save_pretrained_layout(fake_c1):
    from transformers import AutoModelForCausalLM
    out = fake_c1["root"] / "out_sp"
    man = E.export_local(fake_c1["base"], fake_c1["base"], fake_c1["adapter"], out, layout="save_pretrained",
                         revision=None, adapter_sha=fake_c1["sha"], sample=6, fresh=False, log=lambda *a: None)
    assert man["checks"]["passed"] and man["config"]["architectures"] == ["Qwen3_5ForCausalLM"]
    assert man["config"]["mamba_ssm_dtype"] == "float32" and man["checks"]["verify_fresh_merge"] is None
    merged, _, _, _ = E.merge_c1(fake_c1["base"], fake_c1["adapter"], "cpu", None, log=lambda *a: None)
    re = AutoModelForCausalLM.from_pretrained(out, dtype=torch.bfloat16)
    a, b = merged.state_dict(), re.state_dict()
    assert set(a) == set(b) and all(torch.equal(a[k], b[k]) for k in a)


def test_export_refusals(fake_c1, tmp_path):
    kw = dict(revision=None, sample=2, fresh=False, log=lambda *a: None)
    (tmp_path / "busy").mkdir()
    (tmp_path / "busy" / "x").write_text("x")
    with pytest.raises(E.ExportFailed, match="not empty"):
        E.export_local(fake_c1["base"], fake_c1["base"], fake_c1["adapter"], tmp_path / "busy",
                       adapter_sha=fake_c1["sha"], **kw)
    with pytest.raises(E.ExportFailed, match="adapter sha256"):
        E.export_local(fake_c1["base"], fake_c1["base"], fake_c1["adapter"], tmp_path / "o1", **kw)  # C1's real pin
    with pytest.raises(E.ExportFailed, match="layout"):
        E.export_local(fake_c1["base"], fake_c1["base"], fake_c1["adapter"], tmp_path / "o2", layout="pretty",
                       adapter_sha=fake_c1["sha"], **kw)
    with pytest.raises(E.ExportFailed, match="config.json"):  # base pins: a wrong base is refused before any merge
        E.export_local(fake_c1["base"], fake_c1["base"], fake_c1["adapter"], tmp_path / "o3",
                       adapter_sha=fake_c1["sha"], base_pins={"config.json": ("git_sha1", "0" * 40)}, **kw)
    ad2 = tmp_path / "ad2"
    shutil.copytree(fake_c1["adapter"], ad2)
    (ad2 / "train_meta.json").write_text(json.dumps({"cfg": {"layout": "text_first", "style": "od"}}))
    try:
        with pytest.raises(E.ExportFailed, match="layout/style"):
            E.export_local(fake_c1["base"], fake_c1["base"], ad2, tmp_path / "o4", adapter_sha=fake_c1["sha"], **kw)
    finally:  # decoder_io.load set text_first/od for that adapter: give the module back C1's layout
        dio.LAYOUT, dio.STYLE = "schema_branch_mark", "cygnet"


def test_export_checks_catch_tampering(fake_c1, exported, tmp_path):
    from safetensors import safe_open
    from safetensors.torch import save_file
    out, man = exported
    bad = tmp_path / "bad"
    shutil.copytree(out, bad)
    wmap = json.loads((bad / "model.safetensors.index.json").read_text())["weight_map"]
    lm = next(k for k in sorted(wmap) if E.ckpt_to_mem(k) and k.endswith("q_proj.weight"))
    vis = next(k for k in sorted(wmap) if k.startswith("model.visual."))
    touched = sorted({wmap[lm], wmap[vis]})
    for sh in touched:  # one language-model tensor and one vision tensor, +1 on their first element
        with safe_open(str(bad / sh), "pt") as f:
            ts, meta = {k: f.get_tensor(k) for k in f.keys()}, f.metadata()
        for k in (lm, vis):
            if k in ts:
                ts[k] = ts[k].clone()
                ts[k].view(-1)[0] += 1
        save_file(ts, str(bad / sh), metadata=meta)
    merged, _, _, targets = E.merge_c1(fake_c1["base"], fake_c1["adapter"], "cpu", None, log=lambda *a: None)
    v = E.verify_written(merged, bad)
    assert not v["ok"] and v["n_mismatched"] == 1 and v["mismatched"] == [lm]
    bc = E.verify_base_copies(bad, fake_c1["base"])
    assert not bc["ok"] and bc["problems"] == [f"{vis}: differs from the base"]
    wrong = {k: s * 1.5 for k, s in targets.items()}
    assert not E.formula_check(out, fake_c1["base"], fake_c1["adapter"], wrong, n=4)["ok"]
    assert E.formula_check(out, fake_c1["base"], fake_c1["adapter"], targets, n=4)["ok"]
    # the SGLang host's boot checks on the same folders
    m, probs = S.check_manifest(out, adapter_sha=fake_c1["sha"])
    assert probs == [] and S.verify_files(out, m) == []
    assert S.check_manifest(out)[1]  # not C1's real adapter sha
    assert S.verify_files(bad, m) == [f"{sh}: sha256 differs from the manifest" for sh in touched]
    assert S.check_manifest(tmp_path)[0] is None


def test_base_pins_against_local_hf_cache():
    snap = (Path.home() / ".cache" / "huggingface" / "hub" / "models--Qwen--Qwen3.5-4B" / "snapshots" / E.REVISION)
    if not (snap / "config.json").exists():
        pytest.skip("no local Qwen3.5-4B snapshot")
    small = {k: v for k, v in E.BASE_PINS.items() if not k.endswith(".safetensors")}  # the 9 GB shards: in the container
    files = {p.name: p for p in snap.iterdir()}
    assert E.check_pins(files, small) == []
    assert E.check_pins({**files, "config.json": snap / "vocab.json"}, small) == [
        f"config.json: git_sha1 {E.git_blob_sha1(snap / 'vocab.json')[:16]} != pinned {small['config.json'][1][:16]}"]
    assert set(E.BASE_PINS) == {p.name for p in snap.iterdir()} - E.SKIP_BASE_FILES
