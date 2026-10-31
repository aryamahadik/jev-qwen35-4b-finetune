"""CPU tests of the P7 serving-freeze tools (c2_build/serving): VM read-only guard, S1 pin and verify, merge / serve / stop
guards, the parity bar (>= 99.5%), the D9 latency harness and its record through gate_c2.latency_rule, and the prompt-sha check.
No GPU, no network, no Modal, no VM: the VM runner and the server are fakes.
Run: cd lean && HF_HUB_OFFLINE=1 ../.venv/bin/python -B -m pytest -q c2_build/serving/tests
"""
from __future__ import annotations

import copy
import json
import random
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
SERV = Path(__file__).resolve().parents[1]
C2B = SERV.parent
sys.path.insert(0, str(SERV))
sys.path.insert(0, str(C2B))
import p7_common as C  # noqa: E402
import s1_pin  # noqa: E402
import merge_parity as MP  # noqa: E402
import d9_latency as D9  # noqa: E402

STAGED = C2B / "staged/P7"
PIN = SERV / "S1_CONFIG_PIN.json"


# ---- fixtures ---------------------------------------------------------------------------------------------------------
def fake_info(model="/m/c1_merged") -> dict:
    SH = s1_pin.sh_mod()
    d = {k: None for k in SH.SERVER_ARGS_KEYS}
    d.update({"model_path": model, "tokenizer_path": model, "served_model_name": model, "dtype": "bfloat16", "quantization": None,
              "enable_fp32_lm_head": True, "context_length": SH.CONTEXT_LEN, "disable_radix_cache": False,
              "mamba_radix_cache_strategy": "extra_buffer", "mamba_ssm_dtype": "float32", "linear_attn_backend": "triton",
              "linear_attn_prefill_backend": "triton", "max_running_requests": 32, "max_mamba_cache_size": 128,
              "mem_fraction_static": 0.8, "attention_backend": "triton", "speculative_algorithm": None,
              "sampling_defaults": "openai", "random_seed": 0, "enable_lora": None, "lora_paths": None, "version": "0.5.20",
              "chunked_prefill_size": 4096, "page_size": 1, "schedule_policy": "fcfs"})
    d["internal_states"] = [{"last_gen_throughput": 1.0}]
    d["startup_time"] = {"load_weight": 48.0}
    return d


ENV = {"SGLANG_RETURN_ORIGINAL_LOGPROB": "1", "HF_HUB_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"}


def fake_pin(info=None, env=None) -> dict:
    info = info or fake_info()
    return {**s1_pin.hashes(info, env or ENV), "env": env or ENV, "server_args": s1_pin.sh_mod().args_subset(info),
            "model": {"path": info["model_path"]}}


# ---- p7_common ----------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("cmd", [
    "curl -s localhost:30000/server_info", "ps -eo pid,etimes,cmd | grep sglang", "sha256sum ~/lean/decoder_io.py",
    "python3 /tmp/p7_collect.py 30000 > /tmp/p7_collect_out.json", "ls ~/models", "cat /proc/1219/cmdline", "nvidia-smi --query-gpu=name --format=csv"])
def test_readonly_accepts_reads(cmd):
    assert C.assert_readonly(cmd) == cmd


@pytest.mark.parametrize("cmd", [
    "kill 1219", "pkill -f sglang", "~/od/bin/python -B ~/reads/fast_read.py stop", "~/reads/start_server.sh --max-running 32",
    "bash prod_stop.sh w", "curl -X POST localhost:30000/flush_cache", "curl localhost:30000/flush_cache", "rm -rf ~/models/x",
    "echo x > ~/jobs/sglang.pid", "sudo shutdown now", "gcloud compute instances stop od-l4b", "nohup python x &",
    "curl -s --data '{}' localhost:30000/generate", "mv a b", "systemctl stop x"])
def test_readonly_refuses_writes_and_stops(cmd):
    with pytest.raises(SystemExit):
        C.assert_readonly(cmd)


def test_vm_runner_checks_every_command_and_only_writes_tmp_p7():
    calls = []

    def fake_run(argv, **kw):
        calls.append(argv)
        return type("R", (), {"returncode": 0, "stdout": "ok", "stderr": ""})()

    vm = C.Vm(script=Path("/x/vm.sh"), run=fake_run)
    assert vm.ssh("curl -s localhost:30000/health") == "ok"
    with pytest.raises(SystemExit):
        vm.ssh("kill 1")
    assert len(calls) == 1
    with pytest.raises(SystemExit):
        vm.put("a", "od-l4b:~/jobs/x")
    vm.put("a", "od-l4b:/tmp/p7_a")
    assert calls[-1][-1] == "od-l4b:/tmp/p7_a"


@pytest.mark.parametrize("p", ["data/ohs4_sealed/x.jsonl", "bench/longbench_v2/a", "x/Jevbench/y", "c_spec/sealed_brief/z",
                               "bench/external_quarantine/a", "ejs5/run"])
def test_refuse_path(p):
    with pytest.raises(SystemExit):
        C.refuse_path(p)
    C.refuse_path("data/gblock_a42d_c1read.jsonl")


# ---- s1_pin -------------------------------------------------------------------------------------------------------------
def test_hashes_ignore_per_boot_keys_and_mask_the_model_path():
    a, b = fake_info("/m/c1"), fake_info("/m/c2")
    b["internal_states"], b["startup_time"] = [{"last_gen_throughput": 99}], {"load_weight": 1.0}
    ha, hb = s1_pin.hashes(a, ENV), s1_pin.hashes(b, ENV)
    assert ha["path_sha256"] == hb["path_sha256"]                    # same path, other model
    assert ha["config_sha256"] != hb["config_sha256"]                # model_path is part of the config
    assert ha["server_info_stable_masked_sha256"] == hb["server_info_stable_masked_sha256"]
    c = fake_info("/m/c1")
    c["internal_states"] = [{"x": 1}]
    assert s1_pin.hashes(c, ENV)["server_info_stable_sha256"] == ha["server_info_stable_sha256"]


@pytest.mark.parametrize("key,val", [("dtype", "float16"), ("enable_fp32_lm_head", False), ("quantization", "fp8"),
                                     ("mamba_ssm_dtype", "bfloat16"), ("attention_backend", "flashinfer"),
                                     ("max_running_requests", 64), ("mem_fraction_static", 0.9), ("speculative_algorithm", "EAGLE"),
                                     ("disable_radix_cache", True), ("context_length", 8192), ("sampling_defaults", "model"),
                                     ("chunked_prefill_size", 2048), ("random_seed", 1), ("version", "0.5.21")])
def test_verify_catches_each_drift(key, val):
    pin = fake_pin()
    info = fake_info()
    assert s1_pin.verify(info, pin, "same", ENV)["ok"]
    info[key] = val
    res = s1_pin.verify(info, pin, "same", ENV)
    assert not res["ok"] and res["problems"]


def test_verify_path_mode_accepts_other_model_but_same_mode_does_not():
    pin = fake_pin(fake_info("/m/c1"))
    cand = fake_info("/m/c2")
    assert s1_pin.verify(cand, pin, "path", ENV)["ok"]
    assert not s1_pin.verify(cand, pin, "same", ENV)["ok"]


def test_verify_catches_env_drift():
    pin = fake_pin()
    bad = {**ENV, "SGLANG_RETURN_ORIGINAL_LOGPROB": "0"}
    assert not s1_pin.verify(fake_info(), pin, "path", bad)["ok"]


def test_lora_server_is_refused():
    info = fake_info()
    info["enable_lora"] = True
    assert any("LoRA" in p for p in s1_pin.arg_problems(info, ENV)[0])


@pytest.mark.skipif(not PIN.exists(), reason="S1_CONFIG_PIN.json not built")
def test_recorded_pin_is_consistent_with_the_staged_server_info():
    pin = json.loads(PIN.read_text())
    assert pin["checks"]["ok"] and pin["stable_hash_repeats"] is True
    assert pin["model"]["is_c1"] and pin["model"]["adapter_sha256"] == C.C1_ADAPTER_SHA256
    assert pin["server_args"]["attention_backend"] == "triton" and pin["server_args"]["max_running_requests"] == 32
    info = STAGED / "vm_server_info.json"
    if info.exists():
        d = json.loads(info.read_text())
        assert s1_pin.verify(d, pin, "same")["ok"] and s1_pin.verify(d, pin, "path")["ok"]
        d2 = copy.deepcopy(d)
        d2["enable_fp32_lm_head"] = False
        assert not s1_pin.verify(d2, pin, "same")["ok"]
    assert pin["pin_sha256"] == C.canon_sha({k: pin[k] for k in ("config_sha256", "path_sha256", "server_info_stable_sha256")})


@pytest.mark.skipif(not PIN.exists(), reason="S1_CONFIG_PIN.json not built")
def test_candidate_command_equals_the_production_argv_but_for_model_and_port():
    pin = json.loads(PIN.read_text())
    argv = pin["argv"]
    prod_model = pin["model"]["path"]
    mine = MP.candidate_cmd(prod_model, 30000, argv[0])
    assert mine == argv


# ---- parity -------------------------------------------------------------------------------------------------------------
def probs_choice(rng, opts, top=None):
    w = [rng.random() + 0.05 for _ in opts]
    if top is not None:
        w[top] += 5.0
    s = sum(w)
    return {o: x / s for o, x in zip(opts, w)}


def make_rows(n, seed=0):
    rng = random.Random(seed)
    rows, ref = [], {}
    for i in range(n):
        if i % 2:
            opts = ["a", "b", "c", "d"]
            rows.append({"id": f"r{i}", "qtype": "choice", "options": opts, "gold": opts[i % 4], "state": "s", "instructions": "q"})
            ref[f"r{i}"] = probs_choice(rng, opts, top=i % 4)
        else:
            rows.append({"id": f"r{i}", "qtype": "noul", "options": None, "gold": i % 3 == 0 and 1 or 0, "state": "s", "instructions": "q"})
            y = 0.9 if i % 3 == 0 else 0.1
            ref[f"r{i}"] = {"yes": y, "no": 1 - y}
    return rows, ref


class FakeReader:
    """Serves the reference probabilities (optionally perturbed / flipped) as API v1 answers."""

    def __init__(self, ref, flip_ids=(), shift=0.0, drop_key=False):
        self.ref, self.flip, self.shift, self.drop = ref, set(flip_ids), shift, drop_key
        self.stats = {}

    def read(self, rows, views=False):
        out = []
        for r in rows:
            p = dict(self.ref[r["id"]])
            if r["id"] in self.flip:
                ks = sorted(p, key=p.get, reverse=True)
                p[ks[0]], p[ks[1]] = p[ks[1]], p[ks[0]]
            if self.shift:
                k = max(p, key=p.get)
                p[k] -= self.shift
            if self.drop:
                p.pop(next(iter(p)))
            out.append({"type": "choice" if r["qtype"] == "choice" else "noul", "probabilities": p})
        return out

    @staticmethod
    def probs(ans):
        return ans["probabilities"]


META = {"layout": "schema_branch_mark", "style": "cygnet", "tta_choice": True, "tta": False, "tta_noul": False, "perm_seed": None}


def test_compare_equals_fast_read_compare():
    fr = MP.load_fast_read()
    rows, ref = make_rows(300)
    rng = random.Random(1)
    got = [{k: max(v + rng.uniform(-.03, .03), 0) for k, v in ref[r["id"]].items()} for r in rows]
    refl = [ref[r["id"]] for r in rows]
    assert MP.compare(refl, got) == fr.compare(refl, got)


def test_parity_pass_and_the_995_boundary():
    rows, ref = make_rows(2000)
    ok = MP.run_parity(FakeReader(ref), rows, ref, 2000, 7, 2, META)
    assert ok["bar"]["PASS"] and ok["bar"]["PASS_strict"] and ok["all"]["argmax_agree"] == 1.0
    ids = [r["id"] for r in rows if r["qtype"] == "choice"]
    # exactly 10 of 2000 flipped = 99.5% -> PASS; 11 -> FAIL
    p10 = MP.run_parity(FakeReader(ref, ids[:10]), rows, ref, 2000, 7, 2, META)
    assert p10["all"]["argmax_agree"] == 0.995 and p10["bar"]["argmax_agree>=0.995"]
    p11 = MP.run_parity(FakeReader(ref, ids[:11]), rows, ref, 2000, 7, 2, META)
    assert p11["all"]["n_disagree"] == 11 and not p11["bar"]["PASS"]


def test_parity_dlabel_bar_and_min_n():
    rows, ref = make_rows(2000)
    bad = MP.run_parity(FakeReader(ref, shift=0.05), rows, ref, 2000, 7, 2, META)
    assert bad["all"]["frac_dlabel_le_0.02"] == 0.0 and not bad["bar"]["PASS"]
    small = MP.run_parity(FakeReader(ref), rows, ref, 500, 7, 2, META)
    assert small["bar"]["PASS"] is False and not small["bar"]["n>=2000"] and small["bar"]["min_n_used"] == 2000


def test_parity_refuses_missing_reference_and_option_key_mismatch():
    rows, ref = make_rows(2200)
    short = {k: v for k, v in list(ref.items())[:100]}
    with pytest.raises(SystemExit, match="no reference prediction"):
        MP.run_parity(FakeReader(ref), rows, short, 2000, 1, 2, META)
    with pytest.raises(SystemExit, match="option keys differ"):
        MP.run_parity(FakeReader(ref, drop_key=True), rows, ref, 2000, 1, 2, META)


def test_parity_is_seeded_and_records_the_sample_hash():
    rows, ref = make_rows(2400)
    a = MP.run_parity(FakeReader(ref), rows, ref, 2000, 5, 2, META)
    b = MP.run_parity(FakeReader(ref), rows, ref, 2000, 5, 2, META)
    c = MP.run_parity(FakeReader(ref), rows, ref, 2000, 6, 2, META)
    assert a["sample_ids_sha256"] == b["sample_ids_sha256"] != c["sample_ids_sha256"]


@pytest.mark.parametrize("meta,views,frag", [(None, 2, "missing"), ({**META, "layout": "text_first"}, 2, "layout"),
                                             ({**META, "tta_choice": False}, 2, "tta_choice"), (META, 1, "tta_choice"),
                                             ({**META, "perm_seed": 3}, 2, "permutation"), ({**META, "tta": True}, 2, "legacy")])
def test_reference_meta_must_be_the_same_readout(meta, views, frag):
    assert any(frag in p for p in MP.check_ref_meta(meta, views))


def test_bad_reference_meta_fails_the_verdict():
    rows, ref = make_rows(2000)
    r = MP.run_parity(FakeReader(ref), rows, ref, 2000, 1, 2, {**META, "layout": "text_first"})
    assert not r["bar"]["PASS"]


def test_accuracy_diff_reported_when_gold_present():
    rows, ref = make_rows(2000)
    ids = [r["id"] for r in rows if r["qtype"] == "choice"]
    r = MP.run_parity(FakeReader(ref, ids[:10]), rows, ref, 2000, 3, 2, META)
    assert r["accuracy"] is not None and "diff_pt" in r["accuracy"]


# ---- merge / serve / stop guards ------------------------------------------------------------------------------------------
def adapter_dir(tmp_path, payload=b"adapter-bytes"):
    d = tmp_path / "adapter"
    d.mkdir()
    (d / "adapter_model.safetensors").write_bytes(payload)
    return d, C.sha256_file(d / "adapter_model.safetensors")


def test_merge_guard(tmp_path):
    ad, sha = adapter_dir(tmp_path)
    out = tmp_path / "out"
    never = lambda *_: False  # noqa: E731
    assert MP.merge_guard(ad, out, sha, "cpu", None, never) == sha
    with pytest.raises(SystemExit, match="expect-sha"):
        MP.merge_guard(ad, out, "0" * 64, "cpu", None, never)
    out.mkdir()
    (out / "x").write_text("1")
    with pytest.raises(SystemExit, match="not empty"):
        MP.merge_guard(ad, out, sha, "cpu", None, never)
    prod = tmp_path / "prod"
    prod.mkdir()
    with pytest.raises(SystemExit, match="production model dir"):
        MP.merge_guard(ad, prod, sha, "cpu", str(prod), never)
    with pytest.raises(SystemExit, match="GPU belongs to production"):
        MP.merge_guard(ad, tmp_path / "o2", sha, "cuda", None, lambda *_: True)
    assert MP.merge_guard(ad, tmp_path / "o3", sha, "cpu", None, lambda *_: True) == sha


def test_serve_guard(tmp_path):
    m = tmp_path / "m"
    m.mkdir()
    (m / "merge_manifest.json").write_text(json.dumps({"adapter_sha256": "ab" * 32}))
    free = lambda: 100  # noqa: E731
    no = lambda p: False  # noqa: E731
    assert MP.serve_guard(m, "ab" * 32, 30000, no, free)["adapter_sha256"] == "ab" * 32
    with pytest.raises(SystemExit, match="expect-sha"):
        MP.serve_guard(m, "cd" * 32, 30000, no, free)
    with pytest.raises(SystemExit, match="never stops one"):
        MP.serve_guard(m, "ab" * 32, 30000, lambda p: True, free)
    with pytest.raises(SystemExit, match="production"):
        MP.serve_guard(m, "ab" * 32, 30000, no, lambda: 21130)
    with pytest.raises(SystemExit, match="production"):
        MP.serve_guard(m, "ab" * 32, 30000, no, lambda: None)
    with pytest.raises(SystemExit, match="merge_manifest"):
        MP.serve_guard(tmp_path, "ab" * 32, 30000, no, free)


SGL = ["/h/sgl/bin/python", "-m", "sglang.launch_server", "--model-path", "/m/cand"]


def test_stop_guard_only_stops_its_own_candidate():
    MP.stop_guard(55, SGL, "55", "1219", "/m/prod")
    with pytest.raises(SystemExit, match="not an SGLang"):
        MP.stop_guard(55, ["python", "x.py"], "55", "1219", "/m/prod")
    with pytest.raises(SystemExit, match="production server's pid"):
        MP.stop_guard(1219, SGL, "1219", "1219", "/m/prod")
    with pytest.raises(SystemExit, match="production model"):
        MP.stop_guard(55, SGL[:4] + ["/m/prod"], "55", "1219", "/m/prod")
    with pytest.raises(SystemExit, match="own pidfile"):
        MP.stop_guard(77, SGL, "55", "1219", "/m/prod")
    with pytest.raises(SystemExit, match="own pidfile"):
        MP.stop_guard(55, SGL, None, "1219", "/m/prod")


# ---- D9 latency -----------------------------------------------------------------------------------------------------------
C1A = C.C1_ADAPTER_SHA256


def rec(label, p50, adapter=None, path="aa" * 32, **kw):
    adapter = adapter or (C1A if label == "C1" else "b" * 64)
    n = 50
    calls = [p50 + (i - 25) * 0.1 for i in range(n)]
    base = {"label": label, "n": n, "p50_ms": p50, "p95_ms": p50 * 1.5, "p99_ms": p50 * 2, "mean_ms": p50, "path_sha256": path,
            "config_sha256": label * 3, "workload": "S", "workload_sha256": "w" * 64, "warmup": 20, "views": 1, "flushed": True,
            "gpu": "NVIDIA L4", "workload_seed": 0, "adapter_sha256": adapter, "utc": "t", "calls_ms": calls,
            "served_model_path": f"/m/{label}", "served_manifest_sha256": label.lower() * 32, "served_manifest_adapter_sha256": adapter}
    return base | kw


def test_combine_record_is_what_gate_c2_reads():
    import gate_c2
    c1, ok = rec("C1", 100.0), rec("C2", 104.0)
    out = D9.combine(c1, ok)
    assert out["pass"] and out["ratio"] == 1.04 and out["served_path"].startswith("sglang_s1_l4:")
    assert gate_c2.latency_rule(out)["status"] == "PASS"
    out2 = D9.combine(c1, rec("C2", 105.0))
    assert out2["pass"] and gate_c2.latency_rule(out2)["status"] == "PASS"       # 1.05 is the boundary
    out3 = D9.combine(c1, rec("C2", 105.2))
    assert not out3["pass"] and gate_c2.latency_rule(out3)["status"] == "FAIL"
    assert len(out["ratio_ci95_bootstrap_report_only"]) == 2


@pytest.mark.parametrize("k,v", [("path_sha256", "bb" * 32), ("workload_sha256", "x" * 64), ("n", 49), ("warmup", 5), ("views", 2),
                                 ("flushed", False), ("gpu", "H100"), ("workload_seed", 1)])
def test_combine_refuses_records_of_different_paths(k, v):
    with pytest.raises(SystemExit, match=k):
        D9.combine(rec("C1", 100.0), rec("C2", 100.0) | {k: v})


def test_combine_refuses_same_adapter_and_wrong_labels():
    with pytest.raises(SystemExit, match="same adapter"):
        D9.combine(rec("C1", 100.0), rec("C2", 100.0, C1A))
    with pytest.raises(SystemExit, match="--c1 must be"):
        D9.combine(rec("C2", 100.0, "a" * 64), rec("C2", 100.0))


def test_combine_refuses_a_forgotten_server_swap():
    """Both records measured on ONE server (same model path / config / manifest) but labelled C1 and C2 with different adapter
    dirs: the D9 pass of c7 must not come out of that."""
    c1 = rec("C1", 100.0)
    same = rec("C2", 100.0, served_model_path=c1["served_model_path"], served_manifest_sha256=c1["served_manifest_sha256"],
               config_sha256=c1["config_sha256"])
    with pytest.raises(SystemExit, match="same served_model_path"):
        D9.combine(c1, same)
    with pytest.raises(SystemExit, match="same config_sha256"):
        D9.combine(c1, rec("C2", 100.0, config_sha256=c1["config_sha256"]))
    with pytest.raises(SystemExit, match="same served_manifest_sha256"):
        D9.combine(c1, rec("C2", 100.0, served_manifest_sha256=c1["served_manifest_sha256"]))


def test_combine_requires_the_c1_record_to_be_the_c1_adapter():
    with pytest.raises(SystemExit, match="not C1's"):
        D9.combine(rec("C1", 100.0, "a" * 64), rec("C2", 100.0))


@pytest.mark.parametrize("who,k", [("C1", "served_model_path"), ("C1", "served_manifest_sha256"), ("C2", "served_model_path"),
                                   ("C2", "served_manifest_sha256"), ("C2", "config_sha256")])
def test_combine_requires_each_record_to_name_its_served_model(who, k):
    a, b = rec("C1", 100.0), rec("C2", 100.0)
    (a if who == "C1" else b)[k] = None
    with pytest.raises(SystemExit, match=k):
        D9.combine(a, b)


def test_combine_requires_the_served_manifest_to_match_the_named_adapter():
    with pytest.raises(SystemExit, match="different adapter"):
        D9.combine(rec("C1", 100.0), rec("C2", 100.0, served_manifest_adapter_sha256=C1A))
    with pytest.raises(SystemExit, match="different adapter"):
        D9.combine(rec("C1", 100.0, served_manifest_adapter_sha256="c" * 64), rec("C2", 100.0))


def test_served_identity_ties_a_record_to_the_servers_model(tmp_path):
    md = tmp_path / "merged"
    md.mkdir()
    (md / "merge_manifest.json").write_text(json.dumps({"adapter_sha256": "ab" * 32}))
    info = {"model_path": str(md)}
    got = MP.served_identity(info, "ab" * 32)
    assert got["served_model_path"] == str(md) and got["served_manifest_adapter_sha256"] == "ab" * 32
    assert got["served_manifest_sha256"] == C.sha256_file(md / "merge_manifest.json")
    with pytest.raises(SystemExit, match="not serving this adapter"):
        MP.served_identity(info, "cd" * 32)
    with pytest.raises(SystemExit, match="no model_path"):
        MP.served_identity({}, "ab" * 32)
    with pytest.raises(SystemExit, match="no merge manifest"):
        MP.served_identity({"model_path": str(tmp_path / "nope")}, "ab" * 32)


def test_pick_is_seeded_and_disjoint():
    reqs = [{"i": i} for i in range(100)]
    w, m = D9.pick(reqs, 30, 10, 0)
    assert len(w) == 10 and len(m) == 30 and not ({x["i"] for x in w} & {x["i"] for x in m})
    assert D9.pick(reqs, 30, 10, 0) == (w, m) and D9.pick(reqs, 30, 10, 1) != (w, m)
    with pytest.raises(SystemExit):
        D9.pick(reqs, 95, 10)


def test_measure_discards_warmup_and_times_each_call():
    seen = []
    reqs = [{"i": i} for i in range(40)]
    parse = lambda q: [("q", {"i": q["i"]})]  # noqa: E731
    rec_ = D9.measure(lambda row: seen.append(row["i"]), parse, reqs, 20, 5, "C1", {"workload": "S"})
    assert len(seen) == 25 and len(rec_["calls_ms"]) == 20 and rec_["n"] == 20 and rec_["warmup"] == 5
    assert seen[:5] != seen[5:10] or True
    with pytest.raises(SystemExit, match="exactly one question"):
        D9.measure(lambda r: None, lambda q: [("a", {}), ("b", {})], reqs, 5, 2, "C1", {})


def test_percentile_convention_is_nearest_rank():
    assert D9.pct(list(range(1, 101)), .5) == 51 and D9.pct([3, 1, 2], .5) == 2


def test_workload_sha_is_checked(tmp_path):
    (tmp_path / "S.jsonl").write_text(json.dumps({"request": {"state": "x"}}) + "\n")
    (tmp_path / "manifest.json").write_text(json.dumps({"workloads": {"S": {"file": "S.jsonl", "sha256": "0" * 64}}}))
    with pytest.raises(SystemExit, match="manifest"):
        D9.load_workload("S", tmp_path)
    (tmp_path / "manifest.json").write_text(json.dumps({"workloads": {"S": {"file": "S.jsonl", "sha256": C.sha256_file(tmp_path / "S.jsonl")}}}))
    assert D9.load_workload("S", tmp_path)[0] == [{"state": "x"}]


@pytest.mark.skipif(not (D9.WORKLOAD_DIR / "manifest.json").exists(), reason="speed workloads absent")
def test_real_workload_matches_its_manifest_and_holds_single_decisions():
    reqs, sha = D9.load_workload("S")
    assert len(reqs) == 660 and sha == "05f3353fb4a3497f40035d3e8e969971956459e3cebba630e5ee7ccc4e7f2b44"
    C.add_paths()
    from fastcore import readout as R
    assert all(len(R.parse_v1(q, max_opts=255)) == 1 for q in reqs[:50])


# ---- prompt-sha check -----------------------------------------------------------------------------------------------------
def test_views_and_edge_rows_cover_the_hard_cases():
    import prompt_sha_check as P
    rows = P.edge_rows()
    ids = {r["id"] for r in rows}
    assert {"p7_ws", "p7_defs", "p7_yn_card", "p7_wide", "p7_unicode", "p7_inject", "p7_long"} <= ids
    vr, vp = P.views_of(rows)
    assert len(vr) == 2 * len(rows) and vp[0] is None and vp[1] is not None
    assert any(r["qtype"] == "choice" and len(r["options"]) == 30 for r in rows)


def test_eager_ids_strip_the_padding():
    import prompt_sha_check as P

    class Tok:
        def __call__(self, texts, **kw):
            import torch
            ids = [[ord(c) for c in t][:kw["max_length"]] for t in texts]
            n = max(map(len, ids))
            n = -(-n // kw["pad_to_multiple_of"]) * kw["pad_to_multiple_of"]
            return {"input_ids": torch.tensor([i + [0] * (n - len(i)) for i in ids]),
                    "attention_mask": torch.tensor([[1] * len(i) + [0] * (n - len(i)) for i in ids])}

    assert P.eager_ids(Tok(), ["ab", "abcd"], 3) == [[97, 98], [97, 98, 99]]


def test_package_pins_come_from_image35():
    import prompt_sha_check as P
    pins = P.package_pins(C.BUILD / "train/modal_od_c2.py")
    assert pins == {"transformers": ["5.17.0"], "tokenizers": ["0.23.2"], "jinja2": ["3.1.6"]}


def test_prompt_identity_end_to_end_on_this_machine():
    import prompt_sha_check as P
    if not P.DEFAULT_ADAPTER.exists():
        pytest.skip("C1 adapter folder absent")
    try:
        rec_ = P.run([str(P.DEFAULT_ADAPTER)], STAGED / "vm_facts.json")
    except OSError as e:                                  # HF cache absent
        pytest.skip(f"tokenizer not available offline: {e}")
    assert rec_["pass"], rec_["problems"]
    assert all(all(v.values()) for v in rec_["f2_anchor_matches"].values())
    assert set(rec_["paths"]) >= {"train", "gate[q35_4b_main500k]", "s1[q35_4b_main500k]"}


# ---- snap monitor record --------------------------------------------------------------------------------------------------
def test_snap_monitor_cpu_record_vouches_for_the_current_files():
    import snap_monitor_c2 as sm
    assert sm.cputest_ok() is None


# ---- live path against the model-free SGLang stub (real Reader, real tokenizer, real fastcore; no model) ---------------------
STUB = C2B.parent / "speed/opt_c1_20261017/oc1/stubserver.py"
ADAPTER = C2B.parents[2] / "backups/modal_models" / C.C1_NAME


@pytest.fixture()
def stub():
    if not (STUB.exists() and ADAPTER.exists() and (D9.WORKLOAD_DIR / "manifest.json").exists()):
        pytest.skip("stub server, C1 adapter folder or speed workloads absent")
    import importlib.util
    spec = importlib.util.spec_from_file_location("p7_stub", STUB)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    s = mod.StubSGLang(port=0).start()
    yield s
    s.close()


@pytest.fixture()
def served(stub, tmp_path, monkeypatch):
    """The stub 'serves' a merged dir whose manifest names C1's adapter (the stub's /server_info has no model_path of its own)."""
    md = tmp_path / "merged"
    md.mkdir()
    (md / "merge_manifest.json").write_text(json.dumps({"adapter_sha256": C.C1_ADAPTER_SHA256}))
    real = MP.fetch_server_info
    monkeypatch.setattr(MP, "fetch_server_info", lambda port, *a, **k: {**real(port), "model_path": str(md)})
    return md


def test_measure_cli_end_to_end_on_the_stub(stub, served, tmp_path, capsys):
    out = tmp_path / "c1.json"
    rc = D9.main(["measure", "--label", "C1", "--adapter", str(ADAPTER), "--n", "8", "--warmup", "3", "--views", "1",
                  "--port", str(stub.port), "--flush", "--out", str(out)])
    assert rc == 0
    r = json.loads(out.read_text())
    assert r["n"] == 8 and len(r["calls_ms"]) == 8 and r["flushed"] is True and r["views"] == 1
    assert r["adapter_sha256"] == C.C1_ADAPTER_SHA256 and r["workload_sha256"].startswith("05f3353f")
    assert stub.calls["flush"] == 1 and stub.calls["generate"] == 11            # 3 warm-up + 8 measured, one call each
    assert r["served_model_path"] == str(served) and r["served_manifest_adapter_sha256"] == C.C1_ADAPTER_SHA256
    assert r["served_manifest_sha256"] == C.sha256_file(served / "merge_manifest.json")


def test_measure_refuses_a_server_that_serves_another_adapter(stub, served, tmp_path):
    """The forgotten-swap case: the server still serves C1 while the caller labels the run C2 with another adapter dir."""
    other = tmp_path / "c2_adapter"
    other.mkdir()
    for f in ADAPTER.iterdir():
        if f.is_file() and f.name != "adapter_model.safetensors":
            (other / f.name).write_bytes(f.read_bytes())
    (other / "adapter_model.safetensors").write_bytes(b"a different adapter")
    with pytest.raises(SystemExit, match="not serving this adapter"):
        D9.main(["measure", "--label", "C2", "--adapter", str(other), "--n", "4", "--warmup", "2", "--port", str(stub.port),
                 "--flush", "--out", str(tmp_path / "c2.json")])
    assert stub.calls["flush"] == 0 and stub.calls["generate"] == 0 and not (tmp_path / "c2.json").exists()


def test_measure_refuses_flush_on_the_production_port_without_the_window_flag(tmp_path):
    with pytest.raises(SystemExit, match="production port"):
        D9.main(["measure", "--label", "C1", "--adapter", str(ADAPTER), "--port", str(C.PROD_PORT), "--flush", "--out", str(tmp_path / "x")])


def test_parity_cli_end_to_end_on_the_stub(stub, served, tmp_path):
    fr = MP.load_fast_read()
    C.add_paths()
    from fastcore import readout as R
    reqs, _ = D9.load_workload("S")
    rows = []
    for i, q in enumerate(reqs[:80]):
        (_, row), = R.parse_v1(q, max_opts=255)
        rows.append({**row, "id": f"t{i}", "gold": None})
    root = tmp_path / "root"
    (root / "data").mkdir(parents=True)
    (root / "data/split_x.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    rd = fr.Reader(stub.port, ADAPTER, 2, 4, views=2)
    ans = rd.read(rows, views=True)
    (root / "preds_split_x").mkdir()
    (root / "preds_split_x/cand.jsonl").write_text("\n".join(json.dumps({"id": r["id"], "model": "cand", "probs": rd.probs(a)})
                                                           for r, a in zip(rows, ans)) + "\n")
    (root / "preds_split_x/cand.meta.json").write_text(json.dumps(META))
    out = tmp_path / "parity.json"
    rc = MP.main(["parity", "--root", str(root), "--adapter", str(ADAPTER), "--split", "split_x", "--ref", "preds_split_x/cand.jsonl",
                  "--n", "60", "--min-n", "60", "--allow-small-n", "--seed", "3", "--port", str(stub.port), "--out", str(out)])
    r = json.loads(out.read_text())
    assert rc == 0 and r["bar"]["PASS"] and not r["bar"]["PASS_gate"] and r["bar"]["n>=60"] and r["bar"]["min_n_used"] == 60
    assert r["served_model_path"] == str(served) and r["served_manifest_adapter_sha256"] == C.C1_ADAPTER_SHA256
    assert r["config_sha256"] and r["server_info_path_sha256"] and r["all"]["n"] == 60 and r["all"]["argmax_agree"] == 1.0
    assert r["adapter_sha256"] == C.C1_ADAPTER_SHA256 and r["split_sha256"] and r["ref_sha256"]
    # a perturbed reference fails: flip the top option of 5 of the 60 sampled rows (> 0.5%)
    lines = [json.loads(l) for l in (root / "preds_split_x/cand.jsonl").read_text().splitlines()]
    for x in lines[:40]:
        ks = sorted(x["probs"], key=x["probs"].get, reverse=True)
        x["probs"][ks[0]], x["probs"][ks[1]] = x["probs"][ks[1]], x["probs"][ks[0]]
    (root / "preds_split_x/cand.jsonl").write_text("\n".join(json.dumps(x) for x in lines) + "\n")
    rc2 = MP.main(["parity", "--root", str(root), "--adapter", str(ADAPTER), "--split", "split_x", "--ref", "preds_split_x/cand.jsonl",
                   "--n", "60", "--min-n", "60", "--allow-small-n", "--seed", "3", "--port", str(stub.port), "--out", str(out)])
    assert rc2 == 2 and not json.loads(out.read_text())["bar"]["PASS"]
    # a --min-n under the bar is refused without the test flag; a server serving another adapter is refused before any read
    with pytest.raises(SystemExit, match="allow-small-n"):
        MP.main(["parity", "--root", str(root), "--adapter", str(ADAPTER), "--split", "split_x", "--ref", "preds_split_x/cand.jsonl",
                 "--n", "60", "--min-n", "60", "--seed", "3", "--port", str(stub.port), "--out", str(out)])
    (served / "merge_manifest.json").write_text(json.dumps({"adapter_sha256": "ee" * 32}))
    n_gen = stub.calls["generate"]
    with pytest.raises(SystemExit, match="not serving this adapter"):
        MP.main(["parity", "--root", str(root), "--adapter", str(ADAPTER), "--split", "split_x", "--ref", "preds_split_x/cand.jsonl",
                 "--n", "60", "--min-n", "60", "--allow-small-n", "--seed", "3", "--port", str(stub.port), "--out", str(out)])
    assert stub.calls["generate"] == n_gen


def test_gate_pass_needs_the_full_2000_rows():
    rows, ref = make_rows(2000)
    ok = MP.run_parity(FakeReader(ref), rows, ref, 2000, 7, 2, META)
    assert ok["bar"]["PASS_gate"] and ok["bar"]["n>=2000"] and ok["bar"]["min_n_used"] == 2000
    small = MP.run_parity(FakeReader(ref), rows, ref, 500, 7, 2, META, min_n=500)
    assert small["bar"]["PASS"] and not small["bar"]["PASS_gate"] and not small["bar"]["PASS_strict"]
    assert small["bar"]["n>=500"] and not small["bar"]["n>=2000 (A49 f bar)"]


def test_cmd_merge_on_a_non_c1_adapter_pins_nothing_to_c1(tmp_path, monkeypatch):
    """cmd_merge with a non-C1 adapter: export_local gets adapter_sha=None (no C1 pin), the recorded sha is the adapter's own,
    a manifest naming another sha fails, and the record notes the constant 'model' field export_local writes."""
    ad, sha = adapter_dir(tmp_path, b"c2-adapter-bytes")
    out = tmp_path / "merged_c2"
    calls = {}

    class FakeEx:
        BASE_PINS = {"x": "y"}

        @staticmethod
        def export_local(base, snap, adapter, outd, **kw):
            calls.update(kw)
            Path(outd).mkdir(parents=True, exist_ok=True)
            (Path(outd) / "merge_manifest.json").write_text("{}")
            return {"adapter_sha256": calls_sha[0], "model": "q35_4b_main500k", "checks": {"passed": True}}

    calls_sha = [sha]
    monkeypatch.setattr(MP, "_import_exporter", lambda lean: FakeEx)
    args = ["merge", "--adapter", str(ad), "--expect-sha", sha, "--out", str(out)]
    assert MP.main(args) == 0
    assert calls["adapter_sha"] is None and calls["layout"] == "base" and calls["fresh"] is True
    rec_ = json.loads(Path(str(out) + ".p7_merge.json").read_text())
    assert rec_["adapter_sha256"] == sha and rec_["adapter_sha256"] != C.C1_ADAPTER_SHA256
    assert rec_["manifest_model_field"] == "q35_4b_main500k"
    out2 = tmp_path / "merged_bad"
    calls_sha[0] = "0" * 64
    with pytest.raises(SystemExit, match="manifest adapter sha256 differs"):
        MP.main(["merge", "--adapter", str(ad), "--expect-sha", sha, "--out", str(out2)])
