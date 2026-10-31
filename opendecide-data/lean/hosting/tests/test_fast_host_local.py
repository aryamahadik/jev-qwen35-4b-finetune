"""CPU tests of hosting/fast_host.py (od-fast-host) and hosting/upload_c1_adapter.sh. No GPU, no Modal call, no network
beyond 127.0.0.1, no paid call, no protected file.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_fast_host_local.py -q

The REAL server code (fast_host.boot_engine -> FastHost -> make_fast_server) runs in-process on a tiny random Qwen3.5
hybrid model with the C1 tokenizer (fastcore.testing; CUDA graphs EMULATED on CPU, reduced plan), and is hit over HTTP
with httpx: /health, /decide (noul, choice, cards, > 26 options, 16 questions; answers == decoder_io.predict(
tta_choice=True) <= 1e-5), 16 concurrent clients with cross-request batching on vs off (identical answers <= 1e-5),
/admin/config switching (canonical names, aliases, all-or-nothing errors; speed_bench's own client and arm checks),
/admin/flush, auth failures, error mapping (400/404/411/413/500/503/504), /shutdown. Also: the payer guard (called
directly; at import under a `modal` argv in a subprocess; run_main refusing before any Modal object is touched), the
launcher end to end with Modal FAKED (spawn -> device-side assert -> one private-pool reboot -> session file -> smoke /
hold / bad health -> POST /shutdown), the startup parity self-test (passes, and catches a corrupted graph path), the FP8
boot on CPU, adapter pinning, the upload script's refusals (a fake modal binary that must never be called), and the
Modal function's declared limits (read locally, nothing deployed).
"""
import concurrent.futures
import contextlib
import inspect
import json
import os
import queue
import re
import socket
import stat
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

HOSTING = Path(__file__).resolve().parents[1]
LEAN = HOSTING.parent
for _p in (str(HOSTING), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import fast_host as FH  # noqa: E402
import modal  # noqa: E402
import torch  # noqa: E402
from fastcore import EngineClosed, RequestError, request_from_row  # noqa: E402
from fastcore import testing as T  # noqa: E402
from fastcore.readout import dio  # noqa: E402

if not (T.ADAPTER / "tokenizer.json").exists():
    pytest.skip("C1 tokenizer backup missing", allow_module_level=True)

TOKEN = "test-token-0123456789abcdef"
TOL = 1e-5
COVERAGE = {1: 1024, 2: 1024, 4: 512, 8: 256, 16: 256}  # reduced plan (CPU time); B1/B2 <= 1024 keep A0's legacy rule
TEST_BOOT = {"coverage": COVERAGE, "legacy_shapes": False, "eager_warmup": {}, "warm_requests": 1}
EAGER_BOOT = {"graphs": False, "eager_warmup": {}, "warm_requests": 0}
ARMS = json.loads(FH.ARMS_FILE.read_text())["arms"]


def quiet(*a, **k):
    pass


def _info(rep, **kw):
    return {**FH.base_info(kw.pop("fp8", False), "shared"), "adapter_sha256": FH.ADAPTER_SHA256, "gpu": "cpu (test)",
            "boot_s": 0.0, "boot": rep, **kw}


def _serve(host, **kw):
    stop = threading.Event()
    srv, st = FH.make_fast_server(0, TOKEN, host, stop.set, bind="127.0.0.1", **kw)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, st, stop, f"http://127.0.0.1:{srv.server_address[1]}"


def _client(url, token=TOKEN, **kw):
    h = {"Authorization": f"Bearer {token}"} if token is not None else {}
    return httpx.Client(base_url=url, headers=h, timeout=120.0, trust_env=False, **kw)


def _probs(a):
    p = a["probabilities"]
    return {"yes": p["yes"], "no": p["no"]} if a["type"] == "noul" else p


def _diff(ans, r, p_ref):
    """Max |p| difference of an API v1 answer vs decoder_io.predict's probabilities for row r (+ shape checks)."""
    if r["qtype"] == "noul":
        assert ans["type"] == "noul" and set(ans) == {"type", "noul", "probabilities", "usage"}
        assert ans["noul"] == ans["probabilities"]["yes"]
        return max(abs(ans["noul"] - p_ref["yes"]), abs(ans["probabilities"]["no"] - p_ref["no"]))
    assert ans["type"] == "choice" and list(ans["probabilities"]) == r["options"]
    assert ans["confidence"] == ans["probabilities"][ans["choice"]] == max(ans["probabilities"].values())
    return max(abs(ans["probabilities"][o] - p_ref[o]) for o in r["options"])


def _adiff(a, b):
    pa, pb = _probs(a), _probs(b)
    assert list(pa) == list(pb)
    return max(abs(pa[k] - pb[k]) for k in pa)


# ------------------------------------------------------------------ fixtures

@pytest.fixture(scope="module")
def stack():
    tok, ro, model = T.c1_tokenizer(), T.readout(), T.tiny_model()
    eng, rep = FH.boot_engine(model, tok, flags=ARMS["A2"]["flags"], boot_cfg=TEST_BOOT, ro=ro, log=quiet)
    host = FH.FastHost(eng, _info(rep))
    srv, st, stop, url = _serve(host)
    yield SimpleNamespace(tok=tok, ro=ro, model=model, eng=eng, rep=rep, host=host, srv=srv, st=st, stop=stop, url=url)
    srv.shutdown()
    srv.server_close()
    eng.close()


@pytest.fixture(scope="module")
def client(stack):
    with _client(stack.url) as c:
        yield c


@pytest.fixture(scope="module")
def rows(stack):
    """Dev rows (gate dev splits only), spread over ids, short enough for the reduced graph plan."""
    tok, ro = stack.tok, stack.ro
    every = T.dev_rows()

    def ntok(r):
        return len(tok(ro.prompt(r), add_special_tokens=False)["input_ids"])

    def pick(f, n, hi=900):
        pool = sorted((r for r in every if f(r)), key=lambda r: r["id"])
        out = []
        for r in pool[:: max(1, len(pool) // 60)]:
            if len(out) == n:
                break
            if len(r["state"]) + len(r.get("card") or "") < 6000 and ntok(r) <= hi:
                out.append(r)
        assert len(out) == n, (n, len(out))
        return out
    return {"noul": pick(lambda r: r["qtype"] == "noul" and not r.get("card"), 5),
            "noul_card": pick(lambda r: r["qtype"] == "noul" and r.get("card"), 4),
            "choice": pick(lambda r: r["qtype"] == "choice" and not r.get("card") and len(r["options"]) <= 26, 5),
            "choice_card": pick(lambda r: r["qtype"] == "choice" and r.get("card") and len(r["options"]) <= 26, 3),
            "wide": pick(lambda r: r["qtype"] == "choice" and len(r["options"]) > 26, 2, hi=1000)}


@pytest.fixture(scope="module")
def refs(stack, rows):
    """decoder_io.predict(tta_choice=True) probabilities per row id (computed before any concurrent HTTP traffic)."""
    allr = [r for v in rows.values() for r in v]
    ps = dio.predict(stack.model, stack.tok, allr, dev="cpu", tta_choice=True)
    return {r["id"]: p for r, p in zip(allr, ps)}


def _config(c, flags):
    r = c.post("/admin/config", json={"flags": flags})
    assert r.status_code == 200, r.text
    return r.json()


# ------------------------------------------------------------------ Modal objects, payer guard, launcher (no Modal)

def test_modal_objects_and_limits():
    assert FH.app.name == "od-fast-host" and FH.APP_NAME == "od-fast-host"
    assert isinstance(FH.serve, modal.Function) and type(FH.main).__name__ == "LocalEntrypoint"
    spec = FH.serve._spec_
    assert spec.gpus == "H100!" and spec.cpu == 2.0 and spec.memory == 16384 and "/vol" in spec.volumes
    src = Path(FH.__file__).read_text()
    deco = re.search(r"@app\.function\((.*?)\)\s*(?:#[^\n]*)?\ndef serve", src, re.S).group(1)
    for want in ("gpu=GPU", "max_containers=1", "single_use_containers=True", "timeout=FUNCTION_TIMEOUT_S",
                 'volumes={"/vol": vol}'):
        assert want in deco, want
    assert 'with_mount_options(read_only=True)' in src
    assert 'add_local_python_source("modal_direct_host", "fastcore")' in src
    assert FH.FUNCTION_TIMEOUT_S <= 60 * 60
    assert FH.MAX_SECONDS + FH.BOOT_BUDGET_S + FH.SHUTDOWN_MARGIN_S <= FH.FUNCTION_TIMEOUT_S
    assert FH.MAX_SECONDS >= 40 * 60  # A0 + A2 + A1 at a conservative 40 ms/call (~35.5 min) fits one hold window
    assert FH.ADAPTER_SHA256 == "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
    assert (FH.BASE, FH.REVISION) == ("Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    sig = inspect.signature(FH.main.info.raw_f).parameters
    assert sig["region"].default == "any" and sig["fp8"].default is False and sig["hold"].default is False
    assert sig["seconds"].default == 0 and sig["max_usd"].default == FH.DEFAULT_MAX_USD == 6.0
    assert sig["idle"].default == FH.DEFAULT_IDLE_S == 120
    assert {"seconds", "idle", "arm", "pool", "boot_cfg", "boot_wait", "max_usd"} <= set(sig)
    ps = list(inspect.signature(FH.serve._raw_f_).parameters)  # q is a modal.Queue: `modal run ::serve` cannot pass it
    assert ps == ["q", "token", "seconds", "idle_s", "fp8", "flags", "pool", "boot_cfg", "timeout_s"]
    assert FH.SESSION_FILE == LEAN / "speed" / "session_url.json"


@pytest.mark.parametrize("profile", ["mahadikarya3", "mahadikarya2"])
def test_payer_guard_accepts_free_credit(profile):
    assert FH.payer_guard({"MODAL_PROFILE": profile}) == profile
    assert FH.payer_guard({"MODAL_PROFILE": profile}, resolved=profile) == profile


@pytest.mark.parametrize("env", [{}, {"MODAL_PROFILE": ""}, {"MODAL_PROFILE": "  "}, {"MODAL_PROFILE": "aryamhd"},
                                 {"MODAL_PROFILE": "jaypatil-duke"}, {"MODAL_PROFILE": "mahadikarya33"},
                                 {"MODAL_PROFILE": "MAHADIKARYA3"}, {"MODAL_PROFILE": "mahadikarya3 "},
                                 {"MODAL_PROFILE": "mahadikarya44"}, {"MODAL_PROFILE": "default"},
                                 {"MODAL_PROFILE": "mahadikarya3", "MODAL_TOKEN_ID": "ak-x"},
                                 {"MODAL_PROFILE": "mahadikarya2", "MODAL_TOKEN_SECRET": "as-x"}])
def test_payer_guard_refuses(env):
    with pytest.raises(SystemExit, match="REFUSED"):
        FH.payer_guard(env)


def test_payer_guard_resolved_mismatch_and_cli_detection():
    with pytest.raises(SystemExit, match="resolved profile 'aryamhd'"):
        FH.payer_guard({"MODAL_PROFILE": "mahadikarya3"}, resolved="aryamhd")
    assert FH._cli_launch("/Users/x/opendecide-data/.venv/bin/modal")
    assert FH._cli_launch("/x/site-packages/modal/__main__.py")
    assert not FH._cli_launch("/x/.venv/bin/pytest") and not FH._cli_launch("hosting/fast_host.py")


@pytest.mark.parametrize("profile,ok", [("aryamhd", False), ("jaypatil-duke", False), (None, False),
                                        ("mahadikarya3", True)])
def test_import_guard_under_the_modal_cli(profile, ok):
    """Loading the module as the `modal` CLI does (run / deploy / ::serve) runs the payer guard at import."""
    env = {k: v for k, v in os.environ.items() if k not in ("MODAL_PROFILE", "MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET")}
    if profile:
        env["MODAL_PROFILE"] = profile
    code = ("import sys; sys.argv = ['/x/.venv/bin/modal', 'run', 'hosting/fast_host.py::serve']; "
            "sys.path.insert(0, 'hosting'); import fast_host")
    r = subprocess.run([sys.executable, "-c", code], cwd=LEAN, env=env, capture_output=True, text=True, timeout=300)
    assert (r.returncode == 0) == ok, (profile, r.stderr[-600:])
    if not ok:
        assert "REFUSED" in r.stderr


class _Boom:
    """Stands in for serve / modal.Queue: any use fails the test (nothing may reach Modal on a refused launch)."""

    def __getattr__(self, name):
        raise AssertionError(f"Modal object touched on a refused launch ({name})")


@pytest.mark.parametrize("env,kw,match", [
    ({"MODAL_PROFILE": "aryamhd"}, {}, "REFUSED"),
    ({"MODAL_PROFILE": "jaypatil-duke"}, {"hold": True}, "REFUSED"),
    ({}, {}, "REFUSED"),
    ({"MODAL_PROFILE": "mahadikarya3", "MODAL_TOKEN_ID": "ak-1"}, {}, "REFUSED"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"seconds": 5000}, "--seconds"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"hold": True, "seconds": FH.MAX_SECONDS + 1}, "--seconds"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"idle": 5}, "--idle"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"idle": 400}, "--idle"),  # a smoke serves SMOKE_SECONDS (300)
    ({"MODAL_PROFILE": "mahadikarya3"}, {"hold": True, "region": "us-east"}, "--max-usd"),  # worst ~$9.6 > $6
    ({"MODAL_PROFILE": "mahadikarya3"}, {"max_usd": 1.0}, "--max-usd"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"fp8": True, "arm": "A0"}, "BF16 boot"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"arm": "A3"}, "--fp8"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"arm": "S1"}, "not on this HF host"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"pool": "huge"}, "--pool"),
    ({"MODAL_PROFILE": "mahadikarya3"}, {"boot_cfg": '{"bogus": 1}'}, "--boot-cfg"),
])
def test_run_main_refuses_before_any_modal_call(monkeypatch, tmp_path, env, kw, match):
    monkeypatch.setattr(FH, "serve", _Boom())
    monkeypatch.setattr(FH.modal, "Queue", _Boom())
    sf, tf = tmp_path / "session_url.json", tmp_path / "session_token.txt"
    with pytest.raises(SystemExit, match=match):
        FH.run_main(env=env, session_file=sf, token_file=tf, **kw)
    assert not sf.exists() and not tf.exists()


def test_arm_flags_and_boot_cfg():
    for a in ("A0", "A1", "A2"):
        assert FH.arm_flags(a, fp8=False) == ARMS[a]["flags"]
    assert FH.arm_flags("A3", fp8=True) == ARMS["A3"]["flags"]
    with pytest.raises(SystemExit):
        FH.arm_flags("A9", fp8=False)
    assert FH.parse_boot_cfg("") == {}
    cfg = FH.parse_boot_cfg('{"coverage": {"1": 2048, "2": 1024}, "reserve_gb": 8}')
    assert FH.normalize_boot_cfg(cfg)["coverage"] == {1: 2048, 2: 1024}
    for bad in ("[1]", "{", '{"coverage": 3}'):
        with pytest.raises(SystemExit):
            FH.parse_boot_cfg(bad)


def test_check_adapter(tmp_path):
    assert FH.check_adapter(T.ADAPTER) == FH.ADAPTER_SHA256  # the local backup = the pinned C1 adapter
    with pytest.raises(SystemExit, match="missing"):
        FH.check_adapter(tmp_path)
    (tmp_path / "adapter_model.safetensors").write_bytes(b"not C1")
    with pytest.raises(SystemExit, match="refusing to boot"):
        FH.check_adapter(tmp_path)
    (tmp_path / "prism_x.json").write_text("{}")
    with pytest.raises(SystemExit, match="PRISM-X"):
        FH.check_adapter(tmp_path)


def test_session_file(tmp_path):
    sf, tf = tmp_path / "speed" / "session_url.json", tmp_path / "speed" / "session_token.txt"
    rec = FH.write_session(sf, "https://x.modal.host", "tok-123", {"legacy": False}, extra={"payer": "mahadikarya3"},
                           token_path=tf)
    got = json.loads(sf.read_text())
    assert got == rec and {"url", "token", "started_at", "flags"} <= set(got) and got["payer"] == "mahadikarya3"
    assert tf.read_text().strip() == "tok-123"
    for p in (sf, tf):
        assert stat.S_IMODE(p.stat().st_mode) == 0o600
    import speed_bench as sb
    assert sb.read_token(tf) == "tok-123"  # what `speed_bench ab --token-file` reads


def test_small_helpers():
    fc = FH.fastcore_import()
    for e, fatal in ((RuntimeError("CUDA error: device-side assert triggered"), True),
                     (RuntimeError("an illegal memory access was encountered"), True),
                     (ValueError("bad"), False), (torch.cuda.OutOfMemoryError("CUDA out of memory"), False),
                     (RuntimeError("CUDA error: out of memory"), False)):
        assert FH.is_cuda_fatal(e) is fatal and fc.is_cuda_fatal(e) is fatal, e  # one rule: boot and serving
    assert FH.serve_budget(1800, 600) == 1800 and FH.serve_budget(1800, 1200, 2700) == 2700 - 1200 - 90
    assert FH.serve_budget(1800, 2700, 2700) == 0
    assert FH.launch_timeout(FH.MAX_SECONDS) == FH.FUNCTION_TIMEOUT_S
    assert FH.launch_timeout(300) == FH.BOOT_BUDGET_S + 300 + FH.SHUTDOWN_MARGIN_S < FH.FUNCTION_TIMEOUT_S
    assert FH.serve_budget(300, 600, FH.launch_timeout(300)) == 300  # a boot inside its budget keeps the window
    c = FH.cost_estimate(60, 1.75)
    assert c["rate_usd_h"] == round((3.95 + 0.22) * 1.75, 2) and c["usd"] == c["rate_usd_h"]
    w_any, w_east = FH.worst_case(FH.MAX_SECONDS, 1.0), FH.worst_case(FH.MAX_SECONDS, 1.75)
    assert w_any["minutes"] == (3600 + 120 + 900 + 120) / 60 and w_any["usd"] <= FH.DEFAULT_MAX_USD < w_east["usd"]
    assert FH.worst_case(FH.MAX_SECONDS, 1.0, "private")["minutes"] == (3600 + 120) / 60
    assert FH.worst_case(300, 1.75)["usd"] <= FH.DEFAULT_MAX_USD  # a us-east smoke stays under the default cap
    a = FH.config_sha256({"legacy": True}, FH.ADAPTER_SHA256, {"f": "1"}, "e")
    assert a != FH.config_sha256({"legacy": False}, FH.ADAPTER_SHA256, {"f": "1"}, "e")
    assert a != FH.config_sha256({"legacy": True}, "0" * 64, {"f": "1"}, "e")
    assert a != FH.config_sha256({"legacy": True}, FH.ADAPTER_SHA256, {"f": "2"}, "e")
    code = FH.code_shas()
    assert {"fastcore/engine.py", "fastcore/batcher.py", "fast_host.py", "decoder_io.py"} <= set(code)


# ------------------------------------------------------------------ boot + startup parity self-test

def test_boot_report_and_parity_selftest(stack):
    g = stack.rep["engine"]["graphs"]
    assert g["mode"] == "shared" and g["selfcheck"]["ok"] and g["n_graphs"] > 0 and stack.eng.runner.frozen
    st = stack.rep["parity_selftest"]
    assert st["ok"] and st["worst_max_prob_diff"] <= TOL and st["argmax_flips"] == 0 and st["requests"] == 5
    assert st["graph_forwards"] > 0 and set(st["forwards_by_arm"]) == {"A0", "A1", "A2"}
    assert stack.eng.batcher.flags == FH.fastcore_import().batcher.normalize_flags(ARMS["A2"]["flags"])  # restored
    for r in FH.SELFTEST_REQUESTS:  # the built-in requests are valid API v1
        FH.fastcore_import().parse_v1(r)


def test_parity_selftest_catches_a_corrupted_graph_path(stack):
    eng = stack.eng
    real, before = eng.batcher.runner, eng.batcher.flags

    class Corrupt:  # graph replays return shifted logits; the eager path is untouched
        def select(self, *a, **k):
            return real.select(*a, **k)

        def run(self, seqs, cands, shape=None, readout="exact"):
            lg, path = real.run(seqs, cands, shape, readout=readout)
            if shape is not None:
                lg = [x + torch.linspace(0.0, 4.0, x.numel()) for x in lg]
            return lg, path
    eng.batcher.runner = Corrupt()
    try:
        rep = FH.parity_selftest(eng, log=quiet)
    finally:
        eng.batcher.runner = real
    assert not rep["ok"] and rep["n_failures"] > 0 and rep["worst_max_prob_diff"] > FH.SELFTEST_TOL
    assert eng.batcher.flags == before
    bad = FH.FastHost(eng, _info({"parity_selftest": rep}), code=stack.host.code)
    h = bad.health()
    assert h["ok"] is False and any("parity" in p for p in h["problems"])
    no_test = FH.FastHost(eng, _info({}), code=stack.host.code)  # fail closed: no self-test, no ok
    assert no_test.health()["ok"] is False


# ------------------------------------------------------------------ HTTP: health, auth, decide

def test_health(stack, client):
    h = client.get("/health").json()
    for k in ("ok", "engine", "api", "readout", "flags", "config_sha256", "quantization", "graphs", "batcher", "queue",
              "model", "adapter_sha256", "base", "revision", "gpu", "region", "boot_s", "boot", "served", "errors",
              "engine_config_sha256", "code_sha256", "problems"):
        assert k in h, k
    assert h["ok"] is True and h["problems"] == [] and h["engine"] == "hf" and h["api"] == "v1"
    assert h["adapter_sha256"] == FH.ADAPTER_SHA256 and h["model"] == "q35_4b_main500k" and h["quantization"] is None
    assert h["readout"]["max_options"] == 255 and h["readout"]["layout"] == "schema_branch_mark"
    assert len(h["config_sha256"]) == 64 and h["config_sha256"] != h["engine_config_sha256"]
    assert h["boot"]["parity_selftest"]["ok"] and h["graphs"]["n_graphs"] == stack.rep["engine"]["graphs"]["n_graphs"]
    f = h["flags"]
    assert f["cross_batch"] is True and f["batching"] is True and f["effective"]["cross_batch"] is True
    assert client.get("/ping").json() == {"ok": True}


@pytest.mark.parametrize("auth", [None, "Bearer wrong-token-0123456789", TOKEN, f"bearer {TOKEN}", f"Bearer {TOKEN}x",
                                  f"Basic {TOKEN}"])
def test_auth_failures(stack, auth):
    before = stack.eng.batcher.flags
    h = {} if auth is None else {"Authorization": auth}
    with httpx.Client(base_url=stack.url, headers=h, timeout=60, trust_env=False) as c:
        for method, path, body in (("GET", "/health", None), ("GET", "/ping", None),
                                   ("POST", "/decide", FH.core.EXAMPLE), ("POST", "/admin/flush", {}),
                                   ("POST", "/admin/config", {"flags": {"legacy": True}}),
                                   ("POST", "/shutdown", {}), ("GET", "/nope", None)):
            r = c.request(method, path, json=body)
            assert r.status_code == 401 and r.json() == {"error": "unauthorized"}, (auth, path)
    assert not stack.stop.is_set() and stack.eng.batcher.flags == before


def test_decide_matches_decoder_io(stack, client, rows, refs):
    _config(client, ARMS["A2"]["flags"])
    for kind in ("noul", "noul_card", "choice", "choice_card", "wide"):
        for r in rows[kind]:
            r_ = client.post("/decide", json=request_from_row(r, "q"))
            assert r_.status_code == 200, r_.text
            out = r_.json()
            assert out["id"] == r["id"] and out["engine"] == "hf" and set(out["answers"]) == {"q"}
            assert set(out["timing"]) == {"tokenize_ms", "queue_ms", "model_ms", "total_ms"}
            assert out["server_ms"] > 0 and out["path"] in ("graph", "eager", "mixed") and out["batch_rows"] >= 1
            a = out["answers"]["q"]
            assert _diff(a, r, refs[r["id"]]) <= TOL, (kind, r["id"])
            views = 2 if r["qtype"] == "choice" else 1
            assert a["usage"]["views"] == views and out["usage"] == {"input_tokens": a["usage"]["input_tokens"],
                                                                      "routed_rows": 0}
            n_first = len(stack.tok(stack.ro.prompt(r), add_special_tokens=False)["input_ids"])
            assert a["usage"]["input_tokens_first_view"] == n_first
    wide = rows["wide"][0]
    assert len(wide["options"]) > 26 and "AA" in stack.ro.prompt(wide)  # two-letter labels after Z
    out = client.post("/decide", json={**request_from_row(wide), "return_views": True}).json()
    a = out["answers"]["q0"]
    assert len(a["view_probabilities"]) == 2
    avg = {o: (a["view_probabilities"][0][o] + a["view_probabilities"][1][o]) / 2 for o in wide["options"]}
    assert max(abs(avg[o] - a["probabilities"][o]) for o in wide["options"]) <= 1e-12
    out = client.post("/decide", json=request_from_row(rows["noul"][0])).json()
    assert out["path"] == "graph" and out["shapes"][0][0] == 1  # a short row replays a captured B1 graph


@pytest.mark.parametrize("arm", ["A2", "A0"])
def test_sixteen_questions(stack, client, rows, arm):
    qs = rows["noul"][:4] + rows["noul_card"][:3] + rows["choice"][:5] + rows["choice_card"][:3] + rows["wide"][:1]
    assert len(qs) == 16
    state = qs[0]["state"]
    req = {"id": "sixteen", "state": state,
           "questions": {f"q{i:02d}": request_from_row(r)["questions"]["q0"] for i, r in enumerate(qs)}}
    rows16 = [{**r, "state": state} for r in qs]
    ref = dio.predict(stack.model, stack.tok, rows16, dev="cpu", tta_choice=True)
    _config(client, ARMS[arm]["flags"])
    try:
        out = client.post("/decide", json=req).json()
    finally:
        _config(client, ARMS["A2"]["flags"])
    assert list(out["answers"]) == list(req["questions"])
    worst = max(_diff(out["answers"][f"q{i:02d}"], r, p) for i, (r, p) in enumerate(zip(rows16, ref)))
    assert worst <= TOL, worst
    assert out["usage"]["input_tokens"] == sum(a["usage"]["input_tokens"] for a in out["answers"].values())
    if arm == "A0":
        assert len(out["shapes"]) == 1 and out["batch_rows"] == 16 + sum(r["qtype"] == "choice" for r in qs)
    big = {**req, "questions": {**req["questions"], "q16": {"type": "noul", "instructions": "One too many?"}}}
    r = client.post("/decide", json=big)
    assert r.status_code == 400 and "at most 16 questions" in r.json()["error"]


def test_bad_requests(client):
    ok_q = {"type": "choice", "instructions": "Pick one.", "options": ["a", "b"]}
    bad = [({"state": "x", "questions": {"q": {**ok_q, "criteria": {"a": "first"}}}}, "criteria"),
           ({"state": "x", "questions": {"q": ok_q}, "extra": 1}, "unknown request field"),
           ({"state": "x", "questions": {}}, "non-empty"), ({"questions": {"q": ok_q}}, "state"),
           ({"state": "x", "questions": {"q": {**ok_q, "options": ["a", "a"]}}}, "duplicate"),
           ({"state": "x", "questions": {"q": {**ok_q, "options": ["a"]}}}, "options"),
           ({"state": "x", "questions": {"q": {**ok_q, "options": [str(i) for i in range(256)]}}}, "options"),
           ({"state": "x", "questions": {"q": {**ok_q, "options": ["a", ""]}}}, "non-empty"),
           ({"state": "x", "questions": {"q": {"type": "noul", "instructions": "?", "options": ["a", "b"]}}}, "noul"),
           ({"state": "x", "questions": {"q": {"type": "score", "instructions": "?"}}}, "type"),
           ({"state": "x", "questions": {"q": {"type": "noul", "instructions": " "}}}, "instructions"),
           ({"state": "x", "questions": {"q": {"type": "noul", "instructions": "?", "card": 3}}}, "card"),
           ({"state": "x", "return_views": "yes", "questions": {"q": ok_q}}, "return_views"),
           ({"id": 7, "state": "x", "questions": {"q": ok_q}}, "id"), (["state"], "object")]
    for body, word in bad:
        r = client.post("/decide", json=body)
        assert r.status_code == 400 and word in r.json()["error"], (body, r.text)
    for raw in (b"not json", b"\xff\xfe{", b""):
        r = client.post("/decide", content=raw, headers={"Content-Type": "application/json"})
        assert r.status_code == 400 and "bad JSON" in r.json()["error"]
    assert client.post("/nope", json={}).status_code == 404 and client.get("/decide").status_code == 404
    many = {**ok_q, "options": [f"o{i}" for i in range(255)]}
    r = client.post("/decide", json={"state": "x", "questions": {"q": many}})
    assert r.status_code == 200 and len(r.json()["answers"]["q"]["probabilities"]) == 255  # the 255-option ceiling
    assert client.get("/ping").status_code == 200  # the connection and the server survived every error


def _raw(url, head: bytes) -> bytes:
    host, port = url.split("//")[1].split(":")
    with socket.create_connection((host, int(port)), timeout=30) as s:
        s.sendall(head)
        out = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                return out
            out += chunk


def test_body_limits(stack):
    a = f"Authorization: Bearer {TOKEN}\r\n".encode()
    r = _raw(stack.url, b"POST /decide HTTP/1.1\r\nHost: x\r\n" + a + b"Content-Length: 999999999\r\n\r\n")
    assert r.startswith(b"HTTP/1.1 413") and b"body too large" in r
    r = _raw(stack.url, b"POST /decide HTTP/1.1\r\nHost: x\r\n" + a + b"Transfer-Encoding: chunked\r\n\r\n0\r\n\r\n")
    assert r.startswith(b"HTTP/1.1 411")
    r = _raw(stack.url, b"POST /decide HTTP/1.1\r\nHost: x\r\n" + a + b"Content-Length: abc\r\n\r\n")
    assert r.startswith(b"HTTP/1.1 400") and b"Content-Length" in r


# ------------------------------------------------------------------ concurrency: batching on vs off

def test_concurrency_16_batching_on_vs_off(stack, client, rows, refs):
    pool = rows["noul"] + rows["noul_card"] + rows["choice"] + rows["choice_card"]
    reqs = [request_from_row(r, "q") for r in pool]

    def run(flags):
        _config(client, flags)
        bar, out, errs = threading.Barrier(16), [None] * 16, []

        def worker(t):
            try:
                with _client(stack.url) as c:
                    bar.wait(30)
                    res = []
                    for j in range(2):
                        i = (t + 7 * j) % len(reqs)
                        r = c.post("/decide", json=reqs[i])
                        assert r.status_code == 200, r.text
                        res.append((i, r.json()))
                    out[t] = res
            except BaseException as e:  # noqa: BLE001
                errs.append(e)
        ts = [threading.Thread(target=worker, args=(t,)) for t in range(16)]
        for t in ts:
            t.start()
        for t in ts:
            t.join(300)
        assert not errs, errs[:2]
        return [x for res in out for x in res]

    on = run({**ARMS["A2"]["flags"], "batch_wait_ms": 20, "max_rows": 16})
    off = run(ARMS["A1"]["flags"])
    legacy = run(ARMS["A0"]["flags"])
    _config(client, ARMS["A2"]["flags"])
    assert len(on) == len(off) == len(legacy) == 32
    worst = 0.0
    for (i, a), (i2, b), (i3, c) in zip(on, off, legacy):
        assert i == i2 == i3
        r = pool[i]
        worst = max(worst, _adiff(a["answers"]["q"], b["answers"]["q"]), _adiff(a["answers"]["q"], c["answers"]["q"]),
                    _diff(a["answers"]["q"], r, refs[r["id"]]))
    assert worst <= TOL, worst
    assert max(x["batch_rows"] for _, x in on) > 2  # forwards carried rows of several requests (one has <= 2)
    assert max(x["batch_rows"] for _, x in off) == 1  # A1: every view its own batch-1 forward
    # A0: one request at a time, both views of a choice in one batch
    assert all(x["batch_rows"] == (2 if pool[i]["qtype"] == "choice" else 1) for i, x in legacy)
    b = client.get("/health").json()["batcher"]
    assert b.get("request_errors", 0) == 0 and b.get("forward_errors", 0) == 0 and b["alive"]


# ------------------------------------------------------------------ admin routes

def test_admin_config(stack, client):
    h0 = _config(client, ARMS["A2"]["flags"])
    h = _config(client, {"legacy": True})
    assert h["flags"]["legacy"] is True and h["flags"]["effective"]["graph_plan"] == "legacy"
    assert h["flags"]["effective"]["cross_batch"] is False and h["config_sha256"] != h0["config_sha256"]
    assert "served" in h and h["ok"] is True
    h = _config(client, {"legacy": False, "batching": False, "two_pass_2view": True, "max_wait_ms": 5, "max_rows": 8,
                         "token_budget": 4096, "legacy_graphs": False, "tokenize_in_worker": False})
    f = h["flags"]
    assert f["cross_batch"] is False and f["batching"] is False
    assert f["batch_wait_ms"] == 5.0 and f["max_wait_ms"] == 5.0 and f["max_rows"] == 8 and f["token_budget"] == 4096
    assert f["graph_plan"] == "speed1" and f["legacy_graphs"] is False
    assert f["tokenize_outside_lock"] is True and f["tokenize_in_worker"] is False
    before = stack.eng.batcher.flags
    for body, word in (({"flags": {"legacy": True, "bogus": 1}}, "unknown flag"),
                       ({"flags": {"cross_batch": "yes"}}, "true"),
                       ({"flags": {"max_rows": 0}}, "max_rows"), ({"flags": ["legacy"]}, "object"),
                       ({"flags": {"legacy": True}, "extra": 1}, "flags"), ({}, "flags"), ([1], "flags")):
        r = client.post("/admin/config", json=body)
        assert r.status_code == 400 and word in r.json()["error"], (body, r.text)
    assert stack.eng.batcher.flags == before  # all or nothing
    assert client.post("/admin/config", content=b"{", headers={"Content-Type": "application/json"}).status_code == 400
    h = _config(client, {"choice_views": 1})
    try:
        r = next(x for x in FH.SELFTEST_REQUESTS if x["id"] == "selftest-card")
        a = client.post("/decide", json=r).json()["answers"]["intent"]
        assert a["usage"]["views"] == 1
    finally:
        _config(client, ARMS["A2"]["flags"])
    assert client.post("/admin/flush").json()["ok"] is True
    assert client.post("/admin/flush", json={}).status_code == 200


def test_speed_bench_client_and_arm_checks(stack):
    """speed_bench's own client (V1) and refusal rules against this server: what SPEED-2 will run."""
    import speed_bench as sb
    cl = sb.V1(stack.url, TOKEN, 60)
    try:
        for a in ("A0", "A1", "A2"):
            acfg = ARMS[a]
            sb.check_boot(cl.health(), a, acfg)
            h = cl.config(acfg["flags"])
            sb.check_flags(h, a, acfg["flags"])
            assert cl.flush()["ok"] is True
            d, ms, st, err = cl.call({**request_from_row({"id": "x", "state": "s", "qtype": "choice",
                                                           "instructions": "Pick.", "options": ["a", "b", "c"]}),
                                      **acfg["p_request_extra"]})
            assert st == 200 and err is None and len(d["answers"]["q0"]["view_probabilities"]) == 2
        with pytest.raises(sb.ArmRefused, match="quantization"):
            sb.check_boot(cl.health(), "A3", ARMS["A3"])  # A3 needs the FP8 boot
        with pytest.raises(sb.ArmRefused, match="adapter_sha256"):
            sb.check_boot({**cl.health(), "adapter_sha256": "0" * 64}, "A1", ARMS["A1"])
    finally:
        cl.close()
        stack.host.admin_config({"flags": ARMS["A2"]["flags"]})


# ------------------------------------------------------------------ error mapping, shutdown, FP8

class _FakeHost:
    decide_timeout = 0.25

    def decide(self, req):
        fc = FH.fastcore_import()
        m = req.get("mode") if isinstance(req, dict) else None
        if m == "timeout":
            raise concurrent.futures.TimeoutError()
        if m == "closed":
            raise fc.EngineClosed("engine is shut down")
        if m == "bad":
            raise fc.RequestError("bad question")
        if m == "boom":
            raise RuntimeError("kaput")
        return {"answers": {}, "engine": "fake"}

    def admin_config(self, body):
        if body.get("flags") == "boom":
            raise RuntimeError("config kaput")
        return {"ok": True, "flags": body.get("flags")}

    def flush(self):
        return {"ok": True, "flushed": 0}

    def health(self):
        return {"ok": True, "engine": "fake"}


def test_error_mapping():
    srv, st, stop, url = _serve(_FakeHost())
    try:
        with _client(url) as c:
            for mode, code in (("timeout", 504), ("closed", 503), ("bad", 400), ("boom", 500), (None, 200)):
                r = c.post("/decide", json={"mode": mode})
                assert r.status_code == code, (mode, r.text)
            assert "server_ms" in c.post("/decide", json={}).json()
            assert c.post("/admin/config", json={"flags": "boom"}).status_code == 500
            h = c.get("/health").json()
            assert h["served"] == 2 and h["errors"] == 5 and st["status"][504] == 1 and st["status"][503] == 1
    finally:
        srv.shutdown()
        srv.server_close()
    with pytest.raises(ValueError):
        FH.make_fast_server(0, "short", _FakeHost(), lambda: None, bind="127.0.0.1")


def test_shutdown_timeout_and_closed_engine():
    tok, ro = T.c1_tokenizer(), T.readout()
    eng, rep = FH.boot_engine(T.tiny_model(seed=7), tok, flags=ARMS["A1"]["flags"], boot_cfg=EAGER_BOOT, ro=ro,
                              log=quiet)
    assert rep["engine"]["graphs"]["mode"] == "eager_only" and rep["parity_selftest"]["ok"]
    host = FH.FastHost(eng, _info(rep))
    srv, st, stop, url = _serve(host)
    try:
        with _client(url) as c:
            out = c.post("/decide", json=FH.core.EXAMPLE).json()
            assert out["path"] == "eager" and set(out["answers"]) == {"q0", "q1"}
            host.decide_timeout = 1e-6
            r = c.post("/decide", json=FH.core.EXAMPLE)
            assert r.status_code == 504, r.text
            host.decide_timeout = FH.DECIDE_TIMEOUT_S
            with _client(url, token="wrong-token-0123456789") as bad:
                assert bad.post("/shutdown").status_code == 401
            assert not stop.is_set()
            r = c.post("/shutdown")
            assert r.status_code == 200 and r.json() == {"ok": True, "served": 1} and stop.is_set()
            assert FH.wait_serving(stop, st, time.time() + 60, 60) == "shutdown request"  # what serve() does next
            assert eng.close()
            r = c.post("/decide", json=FH.core.EXAMPLE)
            assert r.status_code == 503 and "closed" in r.json()["error"]
            h = c.get("/health").json()
            assert h["ok"] is False and any("worker stopped" in p for p in h["problems"])
    finally:
        srv.shutdown()
        srv.server_close()
        eng.close()
    with pytest.raises(httpx.ConnectError):
        with _client(url) as c:
            c.get("/ping")
    with pytest.raises(EngineClosed):
        eng.decide(FH.core.EXAMPLE)


def test_fp8_boot_cpu():
    import speed_bench as sb
    tok, ro = T.c1_tokenizer(), T.readout()
    eng, rep = FH.boot_engine(T.tiny_model(seed=5), tok, fp8=True, flags=ARMS["A3"]["flags"], boot_cfg=EAGER_BOOT,
                              ro=ro, log=quiet)
    try:
        q = rep["fp8"]
        assert q["quantization"] == "fp8" and q["swapped"] > 0 and "kept_linear" not in q
        kept = q["kept_linear_text"]
        assert "lm_head" in kept and any(n.endswith("in_proj_a") for n in kept) and not q["skipped_not_16_aligned"]
        host = FH.FastHost(eng, _info(rep, fp8=True))
        h = host.health()
        assert h["ok"] and h["quantization"] == "fp8" and h["boot"]["fp8"]["swapped"] == q["swapped"]
        sb.check_boot(h, "A3", ARMS["A3"])
        with pytest.raises(sb.ArmRefused):
            sb.check_boot(h, "A2", ARMS["A2"])
        out = host.decide(FH.SELFTEST_REQUESTS[1])
        p = out["answers"]["intent"]["probabilities"]
        assert abs(sum(p.values()) - 1) < 1e-5 and out["answers"]["urgent"]["type"] == "noul"
        with pytest.raises(RequestError):
            host.admin_config({"flags": {"nope": 1}})
    finally:
        eng.close()


# ------------------------------------------------------------------ the launcher end to end, Modal faked

@pytest.fixture(scope="module")
def eager_engine():
    tok, ro = T.c1_tokenizer(), T.readout()
    eng, rep = FH.boot_engine(T.tiny_model(seed=9), tok, flags=ARMS["A2"]["flags"], boot_cfg=EAGER_BOOT, ro=ro,
                              log=quiet)
    yield eng, rep
    eng.close()


class _FakeQueue:
    def __init__(self):
        self.items = []

    def get(self, timeout=None):
        if self.items:
            return self.items.pop(0)
        raise queue.Empty


class _FakeCall:
    def __init__(self, result=None, stop=None):
        self.result, self.stop, self.cancelled = result, stop, False

    def get(self, timeout=None):
        if self.result is not None:
            return self.result
        if self.stop is not None and self.stop.wait(min(timeout or 0, 2)):
            return {"stop": "shutdown request", "served": -1}
        raise TimeoutError  # what Modal raises for a call that is still running

    def cancel(self):
        self.cancelled = True


class _FakeServe:
    """serve.with_options(...).spawn(...) without Modal: the first spawn reports a device-side assert (shared pool),
    later spawns publish the in-process server's URL and health, as serve() does."""

    def __init__(self, q, url, health, stop, fail_first=True, fail_wall_s=None):
        self.q, self.url, self.health, self.stop, self.fail_first = q, url, health, stop, fail_first
        self.fail_wall_s = fail_wall_s
        self.spawns, self.opts = [], []

    def with_options(self, **o):
        self.opts.append(o)
        return self

    def spawn(self, *args):
        self.spawns.append(args)
        if self.fail_first and len(self.spawns) == 1:
            msg = {"boot_failed": "AcceleratorError: CUDA error: device-side assert triggered", "cuda_fatal": True,
                   "retry_private": True, "pool": args[6]}
            if self.fail_wall_s is not None:
                msg["wall_s"] = self.fail_wall_s
            self.q.items.append(msg)
            return _FakeCall(result=msg)
        self.q.items.append({"url": self.url, "health": self.health})
        return _FakeCall(stop=self.stop)


@pytest.mark.parametrize("mode", ["smoke", "hold", "bad_health"])
def test_run_main_flow_with_modal_faked(monkeypatch, tmp_path, eager_engine, mode, capsys):
    eng, rep = eager_engine
    host = FH.FastHost(eng, _info(rep, serve_s=600))
    srv, st, stop, url = _serve(host)
    try:
        health = host.health()
        if mode == "bad_health":
            health = {**health, "ok": False, "problems": ["startup parity self-test failed"]}
        q = _FakeQueue()
        fake = _FakeServe(q, url, health, stop)
        monkeypatch.setattr(FH, "serve", fake)
        monkeypatch.setattr(FH.modal, "Queue", SimpleNamespace(ephemeral=lambda: contextlib.nullcontext(q)))
        monkeypatch.setattr(FH.secrets, "token_urlsafe", lambda n=None: TOKEN)
        sf, tf = tmp_path / "session_url.json", tmp_path / "session_token.txt"
        if mode == "hold":  # the owner (or speed_bench) ends the session with POST /shutdown
            threading.Timer(2.0, lambda: httpx.post(url + "/shutdown", headers={"Authorization": f"Bearer {TOKEN}"},
                                                    timeout=30, trust_env=False)).start()
        kw = dict(env={"MODAL_PROFILE": "mahadikarya3"}, session_file=sf, token_file=tf, hold=(mode == "hold"))
        if mode == "bad_health":
            with pytest.raises(SystemExit, match="not ok"):
                FH.run_main(**kw)
        else:
            out = FH.run_main(**kw)
            assert out["server_stop"] == "shutdown request"
        secs = FH.MAX_SECONDS if mode == "hold" else FH.SMOKE_SECONDS
        assert len(fake.spawns) == 2 and fake.opts[0] == {"gpu": "H100!", "timeout": FH.launch_timeout(secs)}
        first, second = fake.spawns
        assert first[0] is q and first[1] == TOKEN and first[4] is False and first[5] == ARMS["A2"]["flags"]
        assert first[2] == secs and first[3] == FH.DEFAULT_IDLE_S and first[8] == FH.launch_timeout(secs)
        assert first[6] == "shared" and second[6] == "private"  # rebooted once with private pools
        out = capsys.readouterr().out
        assert '"worst_case"' in out and '"max_usd": 6.0' in out
        if mode == "hold":  # the printed bench command: main arm before A1, and the bench ends the session
            assert "--arms A0,A2,A1 --shutdown-after --go" in out
        assert stop.is_set()  # the launcher always sent POST /shutdown
        rec = json.loads(sf.read_text())
        assert rec["url"] == url and rec["token"] == TOKEN and rec["payer"] == "mahadikarya3"
        assert rec["pool"] == "private" and rec["region"] == "any" and rec["arm"] == "A2"
        assert rec["flags"]["effective"]["cross_batch"] is True and "ended_at" in rec and "started_at" in rec
        assert tf.read_text().strip() == TOKEN and stat.S_IMODE(sf.stat().st_mode) == 0o600
        if mode == "smoke":
            assert st["n"] == 3 * len(FH.SELFTEST_REQUESTS) and st["errors"] == 0
        else:
            assert st["n"] == 0
    finally:
        srv.shutdown()
        srv.server_close()


def test_no_private_reboot_after_a_slow_failed_boot(monkeypatch, tmp_path):
    """The single private-pool reboot is priced into --max-usd as one failed boot of <= BOOT_BUDGET_S: a shared-pool
    boot that died later is not rebooted (nothing more is spawned)."""
    q = _FakeQueue()
    fake = _FakeServe(q, "http://127.0.0.1:9", {}, threading.Event(), fail_wall_s=FH.BOOT_BUDGET_S + 1)
    monkeypatch.setattr(FH, "serve", fake)
    monkeypatch.setattr(FH.modal, "Queue", SimpleNamespace(ephemeral=lambda: contextlib.nullcontext(q)))
    with pytest.raises(SystemExit, match="not rebooting"):
        FH.run_main(env={"MODAL_PROFILE": "mahadikarya3"}, session_file=tmp_path / "s.json",
                    token_file=tmp_path / "t.txt", hold=True)
    assert len(fake.spawns) == 1 and not (tmp_path / "s.json").exists()


class _Sabotage:
    """Wraps the engine's runner: mode "hang" blocks every forward on `release`; mode "cuda" raises the error a
    poisoned CUDA context gives (what a shared-pool aliasing bug missed by the boot self-check would do)."""

    def __init__(self, real):
        self.real, self.mode, self.release, self.calls = real, None, threading.Event(), 0

    def select(self, *a, **k):
        return self.real.select(*a, **k)

    def run(self, seqs, cands, shape=None, readout="exact"):
        self.calls += 1
        if self.mode == "hang":
            assert self.release.wait(30)
        elif self.mode == "cuda":
            raise RuntimeError("CUDA error: device-side assert triggered")
        return self.real.run(seqs, cands, shape, readout=readout)


def test_serving_watchdog_hang_then_cuda_fatal():
    """While serving: a hung forward reads ok=false (and past the stop threshold ends the session); a CUDA-fatal
    error stops the engine worker at once: that request and every later one get 503, /health reads ok=false with the
    problem, and the serving loop's watchdog ends the container (no more H100 time spent serving errors)."""
    tok, ro = T.c1_tokenizer(), T.readout()
    eng, rep = FH.boot_engine(T.tiny_model(seed=11), tok, flags=ARMS["A1"]["flags"], boot_cfg=EAGER_BOOT, ro=ro,
                              log=quiet)
    host = FH.FastHost(eng, _info(rep))
    sab = _Sabotage(eng.batcher.runner)
    eng.batcher.runner = sab
    srv, st, stop, url = _serve(host)
    try:
        with _client(url) as c:
            h = c.get("/health").json()
            assert h["ok"] and h["serve_remaining_s"] is None and h["serve_deadline_unix"] is None
            dl = host.open_window(600)
            h = c.get("/health").json()
            assert 590 < h["serve_remaining_s"] <= 600 and h["serve_deadline_unix"] == pytest.approx(dl, abs=1e-3)
            assert h["serve_deadline_utc"].endswith("Z") and h["serve_s"] == 600
            assert c.post("/decide", json=FH.core.EXAMPLE).status_code == 200
            assert FH.engine_watchdog(host) is None

            eng.batcher.stall_s = 0.3  # ---- hung GPU
            sab.mode = "hang"
            th = threading.Thread(target=lambda: c.post("/decide", json=FH.core.EXAMPLE), daemon=True)
            th.start()
            t0 = time.time()
            while eng.batcher.inflight_s() is None or eng.batcher.inflight_s() < 0.5:
                assert time.time() - t0 < 20
                time.sleep(0.05)
            with _client(url) as c2:
                h = c2.get("/health").json()
            assert h["ok"] is False and any("GPU looks hung" in p for p in h["problems"]), h["problems"]
            assert FH.engine_watchdog(host) is None  # below STALL_STOP_S: reported, not yet stopped
            why = FH.engine_watchdog(host, stall_stop_s=0.4)
            assert why and "GPU hung" in why
            sab.mode = None
            sab.release.set()
            th.join(20)
            assert not th.is_alive() and eng.batcher.inflight_s() is None and c.get("/health").json()["ok"]

            sab.mode = "cuda"  # ---- poisoned CUDA context
            n0 = sab.calls
            r = c.post("/decide", json=FH.SELFTEST_REQUESTS[4])  # 4 questions: several forwards, no retry
            assert r.status_code == 503 and "died" in r.json()["error"] and "device-side assert" in r.json()["error"]
            assert sab.calls == n0 + 1  # the fatal forward is not retried per request
            eng.batcher._thread.join(10)
            h = c.get("/health").json()
            assert h["ok"] is False and any("CUDA context lost" in p for p in h["problems"]), h["problems"]
            b = h["batcher"]
            assert b["alive"] is False and b["cuda_fatal"] is True and b["cuda_fatal_errors"] == 1
            r = c.post("/decide", json=FH.core.EXAMPLE)
            assert r.status_code == 503 and "died" in r.json()["error"]
            assert sab.calls == n0 + 1  # nothing more reached the GPU
            why = FH.engine_watchdog(host)
            assert why and "CUDA context lost" in why
            t0 = time.time()
            reason = FH.wait_serving(stop, st, dl, 600, watchdog=lambda: FH.engine_watchdog(host), poll_s=0.05)
            assert reason.startswith("watchdog: engine worker stopped (CUDA context lost") and time.time() - t0 < 5
            import speed_bench as sb
            with pytest.raises(sb.ArmRefused, match="ok=false"):  # the bench refuses / aborts on it
                sb.check_boot(h, "A1", ARMS["A1"])
    finally:
        sab.release.set()
        srv.shutdown()
        srv.server_close()
        eng.close()


def test_wait_serving_reasons():
    def st(posts, idle_for):
        return {**FH.new_state(), "posts": posts, "last": time.time() - idle_for}

    now, ev = time.time(), threading.Event()
    assert FH.wait_serving(ev, st(0, 0), now - 1, 60, poll_s=0.01) == "serving window (--seconds) reached"
    # before the first POST the grace (first_idle_s) applies, not idle_s: the window ends first here
    t0 = time.time()
    assert FH.wait_serving(ev, st(0, 10), time.time() + 0.3, 1, 100, poll_s=0.01).startswith("serving window")
    assert time.time() - t0 >= 0.25
    assert FH.wait_serving(ev, st(0, 10), now + 60, 1, 5, poll_s=0.01) == \
        "idle for 5 s (no POST since the tunnel opened)"
    assert FH.wait_serving(ev, st(3, 10), now + 60, 1, 100, poll_s=0.01) == "idle for 1 s"
    assert FH.wait_serving(ev, st(3, 0), now + 60, 60, watchdog=lambda: "dead", poll_s=0.01) == "watchdog: dead"

    def broken():
        raise RuntimeError("watchdog bug")

    assert FH.wait_serving(ev, st(3, 0), time.time() + 0.2, 60, watchdog=broken, poll_s=0.01).startswith(
        "serving window")  # a broken watchdog never ends a healthy session
    ev.set()
    assert FH.wait_serving(ev, st(3, 0), now + 60, 60, poll_s=0.01) == "shutdown request"
    s = FH.new_state()
    srv, st2, stop, url = _serve(_FakeHost(), state=s)
    try:
        with _client(url) as c:
            c.get("/health")
            assert st2["posts"] == 0  # GETs do not count
            c.post("/decide", json={})
            c.post("/admin/flush")
            assert st2["posts"] == 2
    finally:
        srv.shutdown()
        srv.server_close()


def test_smoke_against_the_real_server(stack):
    s = FH.smoke(stack.url, TOKEN, rounds=1)
    assert s["calls"] == len(FH.SELFTEST_REQUESTS) and s["errors"] == 0 and s["first_error"] is None
    assert s["client_ms"]["n"] == s["calls"] and set(s["paths"]) <= {"graph", "eager", "mixed"}


# ------------------------------------------------------------------ upload script, pinned files

def test_upload_script_refusals(tmp_path):
    script = HOSTING / "upload_c1_adapter.sh"
    txt = script.read_text()
    assert FH.ADAPTER_SHA256 in txt and "DST=/models/q35_4b_main500k" in txt and "volume put" in txt
    assert "--force" not in txt.split("set -uo pipefail", 1)[1]
    calls = tmp_path / "calls"
    fake = tmp_path / "modal"
    fake.write_text(f'#!/bin/bash\necho "$@" >> "{calls}"\nexit 0\n')
    fake.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if k not in ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET", "MODAL_PROFILE")}
    env["FAST_HOST_MODAL_BIN"] = str(fake)  # belt and braces: the refusals below exit before any modal call
    cases = [(p, {}) for p in ("aryamhd", "jaypatil-duke", "", "mahadikarya33", "MAHADIKARYA3", "mahadikarya44")]
    cases += [("mahadikarya3", {"MODAL_TOKEN_ID": "ak-1"}), ("mahadikarya2", {"MODAL_TOKEN_SECRET": "as-1"})]
    for prof, extra in cases:
        r = subprocess.run(["bash", str(script), prof], env={**env, **extra}, capture_output=True, text=True,
                           timeout=60)
        last = (r.stdout.strip().splitlines() or [""])[-1]
        assert r.returncode == 1 and last.startswith("UPLOAD_FAIL"), (prof, r.stdout, r.stderr)
    assert not calls.exists()  # the modal binary was never invoked
    r = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_pinned_files_untouched():
    """The pinned lean files and the core host files this host imports read-only are unchanged vs HEAD."""
    pinned = ["decoder_io.py", "prism_x.py", "writeblock.py", "gate_dev.py", "hosting/modal_direct_host.py",
              "hosting/client_bench.py"]
    try:
        tracked = subprocess.run(["git", "ls-files", "--", *pinned], cwd=LEAN, capture_output=True, text=True,
                                 timeout=60)
        r = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", *pinned], cwd=LEAN, capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        pytest.skip("git unavailable")
    assert sorted(tracked.stdout.split()) == sorted(pinned), tracked.stdout  # all tracked: the diff below has teeth
    assert r.returncode == 0, "a pinned / core file differs from HEAD"
