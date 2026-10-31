"""CPU tests of the round-2 H100 window code: arm commands, the opt-in sitecustomize patches (real import hook against a fake
sglang package), the r2measure steps against the fake SGLang (generate and score readouts), and the R2Session decision tree
(boot failure with the chunked-prefix assertion -> dcpc variant -> nofull fallback; score refused; GC follow-up; budget gate)."""
import json
import os
import subprocess
import sys
import textwrap
import threading
import time
from collections import deque
from pathlib import Path

import pytest

from oc1 import common as C
from oc1 import configs as K
from oc1 import r2 as R2
from oc1 import runner as RU
from oc1 import session as S

from fastcore import testing as T          # noqa: E402
from fakes import FakeSGLangServer, good_info  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
C1_DIR = str(T.ADAPTER)


# ------------------------------------------------------------------ commands
def test_arm_commands():
    m = "/m"
    base = K.s1_cmd(m, "python3")
    a = R2.R2_CONFIGS["r2_a"].cmd(m, "python3")
    assert a == base
    b = R2.R2_CONFIGS["r2_b"].cmd(m, "python3")
    assert b[:len(base)] == base
    tail = b[len(base):]
    assert tail == ["--cuda-graph-backend-prefill", "full", "--skip-tokenizer-init", "--enable-metrics",
                    "--gc-warning-threshold-secs", "0.005"]
    assert "--cuda-graph-backend-prefill" not in R2.R2_CONFIGS["r2_b_nofull"].cmd(m)
    assert "--disable-chunked-prefix-cache" in R2.R2_CONFIGS["r2_b_dcpc"].cmd(m)
    e1 = R2.R2_CONFIGS["r2_e1"].cmd(m)
    assert e1.count("--mamba-ssm-dtype") == 1 and e1[e1.index("--mamba-ssm-dtype") + 1] == "bfloat16"
    assert R2.R2_CONFIGS["r2_e2"].cmd(m)[-2:] == ["--mamba-track-interval", "64"]
    assert R2.R2_CONFIGS["r2_c"].cmd(m)[-2:] == ["--quantization", "fp8"]
    assert R2.R2_CONFIGS["r2_d1"].cmd(m)[-1] == "--keep-mm-feature-on-device"
    assert R2.R2_CONFIGS["r2_d2"].cmd(m)[-2:] == ["--mm-processor-worker-num", "4"]
    # nothing but the intended flags differs from S1
    for name, cfg in R2.R2_CONFIGS.items():
        assert "--speculative-algorithm" not in cfg.cmd(m)
    w = R2.want_args_r2(R2.R2_CONFIGS["r2_e1"], m)
    assert w["mamba_ssm_dtype"] == "bfloat16"
    w = R2.want_args_r2(R2.R2_CONFIGS["r2_c"], "/fp8")
    assert w["quantization"] == "fp8" and w["model_path"] == "/fp8"
    w = R2.want_args_r2(R2.R2_CONFIGS["r2_b"], m)
    assert w["skip_tokenizer_init"] is True and w["gc_warning_threshold_secs"] == 0.005


def test_check_args_marks_critical_and_warns():
    info = {**good_info("/m"), "mamba_ssm_dtype": "float32"}
    bad, warn = R2.check_args_r2(info, R2.want_args_r2(R2.R2_CONFIGS["r2_a"], "/m"))
    assert not bad
    bad, warn = R2.check_args_r2(info, R2.want_args_r2(R2.R2_CONFIGS["r2_e1"], "/m"))
    assert any("mamba_ssm_dtype" in x for x in bad)             # the flag did not take effect: the block refuses to measure
    info2 = {**info, "quantization": "fp8"}
    bad, _ = R2.check_args_r2(info2, R2.want_args_r2(R2.R2_CONFIGS["r2_a"], "/m"))
    assert any("quantization" in x for x in bad)


def test_graph_prefill_backend():
    assert R2.graph_prefill_backend({"cuda_graph_config": {"decode": {"backend": "full"}, "prefill": {"backend": "breakable"}}}) == "breakable"
    assert R2.graph_prefill_backend({"cuda_graph_config": {"prefill": {"backend": "full"}}}) == "full"
    assert R2.graph_prefill_backend({}) is None


# ------------------------------------------------------------------ the sitecustomize hook against a fake sglang
FAKE_LP = textwrap.dedent('''
    import torch
    class LogitsProcessor:
        def _get_logits(self, hidden_states, lm_head, logits_metadata, embedding_bias=None, use_logits_buffer=True):
            return self._compute_lm_head(hidden_states, lm_head, embedding_bias)
        def _compute_lm_head(self, hidden_states, lm_head, embedding_bias=None):
            return torch.matmul(hidden_states.to(torch.float32), lm_head.weight.to(torch.float32).T)
''')

HOOK_SCRIPT = textwrap.dedent('''
    import json, sys, types, torch
    import sglang.srt.layers.logits_processor as m
    torch.manual_seed(0)
    V, D = 300, 32
    W = torch.randn(V, D, dtype=torch.bfloat16)
    lm = types.SimpleNamespace(weight=W)
    h = torch.randn(3, D, dtype=torch.bfloat16)
    ids = json.load(open(sys.argv[1]))
    LP = m.LogitsProcessor()
    meta_ok = types.SimpleNamespace(token_ids_logprobs=[ids[:3], ids[1:5], ids[:2]], extend_return_logprob=True)
    meta_out = types.SimpleNamespace(token_ids_logprobs=[ids[:3], [299], ids[:2]], extend_return_logprob=True)
    meta_dec = types.SimpleNamespace(token_ids_logprobs=None, extend_return_logprob=False)
    full = torch.matmul(h.float(), W.float().T)
    a = LP._get_logits(h, lm, meta_ok)
    b = LP._get_logits(h, lm, meta_out)
    c = LP._get_logits(h, lm, meta_dec)
    idt = torch.tensor(ids)
    out = {"a_cols_equal": bool(torch.allclose(a[:, idt], full[:, idt], atol=1e-5)),
           "a_other_inf": bool(torch.isinf(a[:, [i for i in range(V) if i not in set(ids)]]).all()),
           "b_full": bool(torch.allclose(b, full, atol=1e-5)), "c_full": bool(torch.allclose(c, full, atol=1e-5)),
           "w_untouched": bool(torch.equal(W, lm.weight))}
    print(json.dumps(out))
''')


def test_lmhead_hook_installs_and_slices(tmp_path):
    pkg = tmp_path / "fake"
    d = pkg / "sglang" / "srt" / "layers"
    d.mkdir(parents=True)
    for p in (pkg / "sglang", pkg / "sglang" / "srt", d):
        (p / "__init__.py").write_text("")
    (d / "logits_processor.py").write_text(FAKE_LP)
    ids = [5, 17, 29, 41, 150, 151, 299 - 1]
    idf = tmp_path / "ids.json"
    idf.write_text(json.dumps(ids))
    rep = tmp_path / "rep.jsonl"
    env = {**os.environ, "PYTHONPATH": f"{HERE / 'r2pypatch'}{os.pathsep}{pkg}", "R2_LMHEAD_IDS": str(idf), "R2_REPORT": str(rep)}
    r = subprocess.run([sys.executable, "-c", HOOK_SCRIPT, str(idf)], env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr[-1500:]
    out = json.loads(r.stdout.strip().splitlines()[-1])
    assert out == {"a_cols_equal": True, "a_other_inf": True, "b_full": True, "c_full": True, "w_untouched": True}, out
    events = [json.loads(x) for x in rep.read_text().splitlines()]
    assert any(e.get("event") == "patched" for e in events) and any(e.get("event") == "rows_copied" and e["rows"] == len(ids) for e in events)
    diags = [e for e in events if e.get("event") == "diag"]
    assert diags and diags[-1]["calls"] >= 1 and any(d["example"]["why"] in ("ids_outside", "no_ids") for d in diags), diags     # every refusal is counted by reason
    # without the env var nothing is installed
    env2 = {k: v for k, v in env.items() if k != "R2_LMHEAD_IDS"}
    r2 = subprocess.run([sys.executable, "-c", HOOK_SCRIPT.replace("ids = json.load(open(sys.argv[1]))", "ids = [5, 17, 29, 41, 150, 151, 298]"),
                         str(idf)], env=env2, capture_output=True, text=True, timeout=120)
    assert r2.returncode == 0
    assert json.loads(r2.stdout.strip().splitlines()[-1])["a_other_inf"] is False


def test_gc_freeze_thread(tmp_path):
    flag = tmp_path / "flag"
    rep = tmp_path / "rep.jsonl"
    env = {**os.environ, "PYTHONPATH": str(HERE / "r2pypatch"), "R2_GC_FREEZE": "600", "R2_GC_FLAG": str(flag), "R2_REPORT": str(rep)}
    code = f"import time, gc; open({str(flag)!r}, 'w').write('go'); time.sleep(2.5); print(gc.get_freeze_count())"
    r = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout.strip().splitlines()[-1]) > 0
    assert any(json.loads(x).get("event") == "gc_frozen" for x in rep.read_text().splitlines())


# ------------------------------------------------------------------ r2measure on the fake server
def sample(items, n):
    out, seen = [], {}
    for it in items:
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
    for name, n in (("P", 60), ("N", 70), ("R", 30), ("S", 10)):
        C.write_jsonl(work / f"{name}.jsonl", sample(C.read_jsonl(C.OLD_DATA / f"{name}.jsonl"), n))
    yield {"srv": srv, "work": work, "tmp": tmp_path_factory.mktemp("out")}
    srv.close()


PARAMS = {"parity_conc": 4, "lat_n": 20, "lat_warm": 3, "canary_n": 12}


def spec_for(w, name, backend, steps, out_dir, refs=None, canary_min=0.0):
    out_dir.mkdir(parents=True, exist_ok=True)
    return {"config": name, "backend": backend, "sgl_url": w["srv"].url, "work_dir": str(w["work"]), "c1_dir": C1_DIR,
            "out_dir": str(out_dir), "steps": steps, "params": PARAMS, "refs": refs or {}, "out_path": str(out_dir / "measure.json"),
            "canary_min": canary_min, "fp8": False}


def test_r2measure_generate_then_score_vs_reference(world, monkeypatch, tmp_path):
    monkeypatch.setenv("OC1_TMP", str(tmp_path))
    root = world["tmp"]
    a = root / "r2_a"
    ra = R2.run_r2measure(spec_for(world, "r2_a", "generate", ["parity", "latency", "throughput", "prefix", "parity_c64"], a), log=lambda *x: None)
    assert not ra["errors"], ra["errors"]
    assert set(ra["steps"]) == {"parity", "latency", "throughput", "prefix", "parity_c64"}
    n = len(C.read_jsonl(world["work"] / "P.jsonl"))
    assert len(C.read_jsonl(a / "answers_P.jsonl")) == n and len(C.read_jsonl(a / "answers_P_c64.jsonl")) == n
    c64 = ra["steps"]["parity_c64"]["parity_vs_same_boot_c32"]
    assert c64["argmax_agree"] == 1.0
    lat = ra["steps"]["latency"]
    assert lat["rep1"]["n"] == 20 and lat["rep2"]["wall_ms"]["p99"] is not None
    recs = json.loads((a / "latency_records.json").read_text())
    assert set(recs) == {"rep1", "rep2"} and recs["rep1"][0]["id"]
    thr = ra["steps"]["throughput"]
    assert thr["N_c64"]["ok"] == len(C.read_jsonl(world["work"] / "N.jsonl")) and thr["P_sat_c64"]["ok"] == n
    # B: the score readout, same model: canary + parity against A's answers
    b = root / "r2_b"
    refs = {"r2_a_same_session": str(a / "answers_P.jsonl")}
    rb = R2.run_r2measure(spec_for(world, "r2_b", "score", ["canary", "parity", "latency"], b, refs, canary_min=0.97), log=lambda *x: None)
    assert not rb["errors"] and "aborted" not in rb, (rb["errors"], rb.get("aborted"))
    assert rb["backend"] == "score"
    assert rb["steps"]["canary"]["agree_vs_reference"] == 1.0 and rb["steps"]["canary"]["stop"] is False
    pv = rb["steps"]["parity"]["parity_vs_r2_a_same_session"]
    assert pv["n"] == n and pv["argmax_agree"] == 1.0 and pv["dp_max"] < 5e-5


def test_canary_stops_a_broken_arm(world, monkeypatch, tmp_path):
    monkeypatch.setenv("OC1_TMP", str(tmp_path))
    a = world["tmp"] / "canary_a"
    R2.run_r2measure(spec_for(world, "r2_a", "generate", ["parity"], a), log=lambda *x: None)
    ref = {"r2_a_same_session": str(a / "answers_P.jsonl")}
    # corrupt the reference so that the arm "disagrees" on every decision
    rows = C.read_jsonl(a / "answers_P.jsonl")
    for r in rows:
        p = r["probs"]
        if "yes" in p:
            r["probs"] = {"yes": 1.0 - p["yes"], "no": 1.0 - p["no"]}
        else:
            ks = sorted(p, key=p.get)
            r["probs"] = {k: p[ks[len(ks) - 1 - i]] for i, k in enumerate(ks)}
    C.write_jsonl(a / "ref_flipped.jsonl", rows)
    ref = {"r2_a_same_session": str(a / "ref_flipped.jsonl")}
    out = world["tmp"] / "canary_b"
    rb = R2.run_r2measure(spec_for(world, "r2_b", "generate", ["canary", "parity", "latency"], out, ref, canary_min=0.97), log=lambda *x: None)
    assert rb.get("aborted", "").startswith("canary")
    assert "parity" not in rb["steps"] and "latency" not in rb["steps"]


# ------------------------------------------------------------------ the session decision tree
class FakeHandle:
    """Stands in for SglServer: the url of the shared fake server, scripted boot behaviour."""

    def __init__(self, cfg, url, behaviour, log):
        self.cfg, self.url, self.behaviour = cfg, url, behaviour
        self.cmd = ["fake-sglang"] + cfg.extra
        self.tail = deque(maxlen=50)
        self.log = log

    def start(self):
        return self

    def wait_ready(self, timeout_s=0):
        if self.behaviour == "chunked_assert":
            self.tail.append("AssertionError: HybridLinearAttnBackend does not support chunked-prefix Full prefill CUDA graphs")
            raise RuntimeError("SGLang exited (1) during boot")
        if self.behaviour == "other_boot_fail":
            raise RuntimeError("SGLang exited (1) during boot: CUDA out of memory")
        return 1.0

    def server_info(self):
        info = good_info("/m")
        flags = R2.parse_flag_values(self.cfg.cmd("/m"))
        info["model_path"] = self.cfg.model_dir_for_test
        info["mamba_ssm_dtype"] = flags.get("mamba_ssm_dtype", "float32")
        info["quantization"] = flags.get("quantization")
        info["cuda_graph_config"] = {"prefill": {"backend": flags.get("cuda_graph_backend_prefill", "breakable")}}
        return info

    def alive(self):
        return True

    def stop(self, grace=0):
        return {"stop_s": 0.0}


class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def make_session(world, tmp_path, behaviours, plan_configs, monkeypatch, rate=4.4, prior=0.0):
    (tmp_path / "tmp").mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("OC1_TMP", str(tmp_path / "tmp"))
    models = tmp_path / "models"
    (models / C.MERGED_NAME).mkdir(parents=True)
    os.symlink(C1_DIR, models / C.MERGED_NAME / "c1_tokenizer")
    events = []
    started = []

    def factory(cfg, mdir, python, log, log_file):
        cfg = R2._replace_cfg(cfg)
        object.__setattr__(cfg, "model_dir_for_test", mdir)
        started.append(cfg.name)
        return FakeHandle(cfg, world["srv"].url, behaviours.get(cfg.name, "ok"), log)

    plan = {"configs": plan_configs, "params": {**PARAMS}, "measure_timeout_s": 300, "boot_timeout_s": 10}
    sess = R2.R2Session(plan, events.append, models_root=str(models), work_dir=str(world["work"]), results_root=str(tmp_path / "res"),
                        rate_usd_h=rate, prior_usd=prior, python=sys.executable, runner_python=sys.executable, log=lambda *a: None,
                        server_factory=factory)
    return sess, events, started


def test_session_full_prefill_refused_goes_dcpc_then_nofull(world, tmp_path, monkeypatch):
    sess, events, started = make_session(world, tmp_path, {"r2_b": "chunked_assert", "r2_b_dcpc": "other_boot_fail"}, ["r2_a", "r2_b", "r2_c"], monkeypatch)
    # shrink the plan: skip the vision / prefix steps of the real configs for speed
    for n in ("r2_a",):
        sess.configs[n] = R2._replace_cfg(sess.configs[n], vision=[], steps=["parity", "latency"])
    sess.configs["r2_c"] = R2._replace_cfg(sess.configs["r2_c"], fp8=False, model="merged", steps=["canary", "parity"])
    for n in ("r2_b_dcpc", "r2_b_nofull"):
        sess.configs[n] = R2._replace_cfg(sess.configs[n], steps=["canary", "parity"])
    res = sess.run()
    assert started == ["r2_a", "r2_b", "r2_b_dcpc", "r2_b_nofull", "r2_c"], started
    assert "chunked-prefix" in res["results"]["r2_b"]["error"] or "SGLang exited" in res["results"]["r2_b"]["error"]
    assert res["results"]["r2_b"]["server_tail"]
    nof = res["results"]["r2_b_nofull"]
    assert not nof.get("error"), nof.get("error")
    assert "steps" in nof["measure"], nof["measure"]
    pv = nof["measure"]["steps"]["parity"]["parity_vs_r2_a_same_session"]
    assert pv["argmax_agree"] == 1.0
    assert any("r2_b: full-graph prefill not usable" in n or "r2_b_dcpc" in n for n in res["notes"])
    assert nof["prefill_graph_backend_resolved"] == "breakable"


def test_session_ok_bundle_keeps_full_and_gate_skips_when_budget_runs_out(world, tmp_path, monkeypatch):
    sess, events, started = make_session(world, tmp_path, {}, ["r2_a", "r2_b", "r2_c", "r2_d1"], monkeypatch, rate=4.4, prior=4.45)
    # spent so far 4.45 + 45 s overhead = 4.505: nothing fits under the 4.50 stop-launch
    for n in ("r2_a", "r2_b", "r2_c", "r2_d1"):
        sess.configs[n] = R2._replace_cfg(sess.configs[n], est_s=30, vision=[], steps=["parity"])
    res = sess.run()
    assert all("skipped" in r for r in res["results"].values()), res["results"]
    assert started == []


def test_session_bundle_with_full_in_effect_runs_gc_variant_only_when_pauses_show(world, tmp_path, monkeypatch):
    sess, events, started = make_session(world, tmp_path, {}, ["r2_a", "r2_b"], monkeypatch)
    sess.configs["r2_a"] = R2._replace_cfg(sess.configs["r2_a"], vision=[], steps=["parity"])
    sess.configs["r2_b"] = R2._replace_cfg(sess.configs["r2_b"], steps=["canary", "parity"])
    res = sess.run()
    assert started == ["r2_a", "r2_b"], started          # no GC lines in the (fake) log: no gc variant
    assert res["results"]["r2_b"]["prefill_graph_backend_resolved"] == "full"
    assert res["results"]["r2_b"]["measure"]["steps"]["parity"]["parity_vs_r2_a_same_session"]["argmax_agree"] == 1.0
    # now with GC lines in the log of r2_b
    sess2, _, started2 = make_session(world, tmp_path / "again", {}, ["r2_a", "r2_b"], monkeypatch)
    sess2.configs["r2_a"] = R2._replace_cfg(sess2.configs["r2_a"], vision=[], steps=["parity"])
    sess2.configs["r2_b"] = R2._replace_cfg(sess2.configs["r2_b"], steps=["canary", "parity"])
    orig = sess2.run_block

    def with_gc(cfg):
        r = orig(cfg)
        if cfg.name == "r2_b":
            r["log_scan"] = {"gc": {"n": 3, "first": ["GC took 0.2 s"]}}
        return r
    sess2.run_block = with_gc
    res2 = sess2.run()
    assert started2 == ["r2_a", "r2_b", "r2_b_gc"], started2
    gc = sess2.configs["r2_b_gc"]
    assert gc.gc_flag and gc.env["R2_GC_FREEZE"] and "--cuda-graph-backend-prefill" in gc.extra      # the passing variant + the freeze


def test_scan_log(tmp_path):
    p = tmp_path / "log"
    p.write_text("a\nWARNING: GC took 0.01 s\ncapture graph begin\nfalling back to eager\nTraceback x\nok\n")
    s = R2.scan_log(p)
    assert s["gc"]["n"] == 1 and s["graph"]["n"] == 1 and s["fallback"]["n"] == 1 and s["error"]["n"] == 1


def test_session_stops_when_the_reference_arm_fails(world, tmp_path, monkeypatch):
    sess, events, started = make_session(world, tmp_path, {"r2_a": "other_boot_fail"}, ["r2_a", "r2_b", "r2_c"], monkeypatch)
    res = sess.run()
    assert started == ["r2_a"], started
    assert any("reference" in n and "window stopped" in n for n in res["notes"])
    assert any(e.get("event") == "reference_failed" for e in events)
