"""END-TO-END DRY RUN of the L1 look and of the J step on a SYNTHETIC suite: the real runner code, the real guards, the real frozen-scorer code (copied
into a temp tree), the real C1 tokenizer / readout / prompt-sha check, real tiny merges, a fake SGLang HTTP server and a fake GPU host.
No real item, no real answer, no Modal, no network (a loopback fake for OpenRouter), no money. The real looks.jsonl is never touched.
  cd lean/c2_build/train && HF_HUB_OFFLINE=1 ../../../.venv/bin/python -B -m pytest -q l1_look/tests/test_l1_dryrun.py
"""
from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
TESTS = Path(__file__).resolve().parent
PKG = TESTS.parent
TRAIN = PKG.parent
C2B = TRAIN.parent
LEAN = C2B.parent
GRID_TESTS = TRAIN / "grid_h100" / "tests"
for p in (str(TRAIN), str(C2B), str(LEAN), str(TESTS), str(GRID_TESTS), str(C2B / "serving")):
    sys.path.insert(0, p)

import fakes as F  # noqa: E402  (grid_h100/tests/fakes.py: tiny base + adapters, fake SGLang)
import synth as SY  # noqa: E402
from grid_h100 import common as C  # noqa: E402
from grid_h100 import gridbuild as GB  # noqa: E402
from grid_h100 import merge_direct as MD  # noqa: E402
from grid_h100 import servers as SV  # noqa: E402
from l1_look import j_run as J  # noqa: E402
from l1_look import l1_cli as CLI  # noqa: E402
from l1_look import l1common as L  # noqa: E402
from l1_look import l1reader as LR  # noqa: E402
from l1_look import l1session as LS  # noqa: E402
from l1_look import l1verdict as LV  # noqa: E402

HAVE_C1 = F.C1_BACKUP.exists() and (F.C1_BACKUP / "tokenizer.json").exists()
pytestmark = [pytest.mark.skipif(not HAVE_C1, reason="the C1 backup tokenizer is not on this machine"),
              pytest.mark.skipif(not SY.have_scorer_code(), reason="the sealed scorer CODE is not on this machine")]
P_REF = {"rows": 8143, "seq": 11957, "chars": 17175428}
GPU = "NVIDIA H100 80GB HBM3, 81559 MiB, 580.1"


# ------------------------------------------------------------------ doubles
def fake_info(model="/m/x"):
    SH = SV.sh()
    d = {k: None for k in SH.SERVER_ARGS_KEYS}
    d.update({"model_path": model, "tokenizer_path": model, "served_model_name": model, "dtype": "bfloat16", "quantization": None,
              "enable_fp32_lm_head": True, "context_length": SH.CONTEXT_LEN, "disable_radix_cache": False, "mamba_radix_cache_strategy": "extra_buffer",
              "mamba_ssm_dtype": "float32", "linear_attn_backend": "triton", "linear_attn_prefill_backend": "triton", "max_running_requests": 64,
              "max_mamba_cache_size": 400, "mem_fraction_static": 0.88, "attention_backend": "fa3", "speculative_algorithm": None,
              "sampling_defaults": "openai", "random_seed": 0, "enable_lora": None, "lora_paths": None, "version": "0.5.20",
              "chunked_prefill_size": 8192, "page_size": 1, "schedule_policy": "fcfs"})
    d["internal_states"], d["startup_time"] = [{"x": 1}], {"a": 1}
    return d


class FakeServer:
    """SglServer double: 'boots' instantly, serves the shared FakeSGL, reports the merged folder as its model_path."""
    boots, problems, info_patch = [], {}, {}

    def __init__(self, model_dir, python=None, port=None, log=print, log_file=None, server=None, extra_env=None):
        self.model_dir, self.tail = Path(model_dir), []
        self.env = {**SV.sh().server_env(), "TRITON_CACHE_DIR": "/tmp/x"}
        self.name, self.up, self.stopped = self.model_dir.name, False, False

    def start(self):
        self.up = True
        FakeServer.boots.append(self.name)
        return self

    def alive(self):
        return self.up and not self.stopped

    def wait_ready(self, timeout_s=900.0):
        return 0.1

    def server_info(self):
        info = fake_info(str(self.model_dir))
        info["context_length"] = SV.load_pin()["server_args"]["context_length"]
        info.update(FakeServer.info_patch.get(self.name, {}))
        return info

    def check(self, info, pin):
        return list(FakeServer.problems.get(self.name, [])), []

    def flush(self):
        return {"ok": True}

    def stop(self, grace=30.0):
        self.stopped = True
        return {"stop_s": 0.0, "gpu": {"free": True}}


class InProcL1Reader:
    """ReaderProc double: the real L1Reader in this process, same ready / run / quit interface (errors sanitised as the daemon does)."""

    def __init__(self, spec, log, port):
        self.gr = LR.L1Reader(spec["c1_dir"], spec["data_dir"], spec["sets"], spec["manifest"], spec["recorded_check"], port=port, workers=3, chunk=4,
                              log=lambda s: None)
        self.quit_called = False

    def wait_ready(self, timeout_s=900.0):
        return {"ok": True, "info": self.gr.init()}

    def run(self, cmd, timeout_s):
        try:
            r = self.gr.run_model(cmd)
            r["ok"] = True
            return r
        except BaseException as e:  # noqa: BLE001
            return {"ok": False, "error": LR._safe(e), "read_name": cmd.get("read_name")}

    def quit(self):
        self.quit_called = True


@pytest.fixture(scope="module")
def tokmemo():
    from grid_h100 import reader as RD
    orig = RD.SH.load_c1_tokenizer
    cache = {}

    def memo(c1_dir, *a, **k):
        key = str(c1_dir)
        if key not in cache:
            cache[key] = orig(c1_dir, *a, **k)
        return cache[key]
    RD.SH.load_c1_tokenizer = memo
    yield RD
    RD.SH.load_c1_tokenizer = orig


def build_world(tmp_path, monkeypatch):
    """A whole tiny job: base, C1 adapter, a C2 run with checkpoints, the grid record, CANDIDATE_C2.json, the pre-gate (PASS), the owner's GO #2,
    a synthetic suite + request file, a synthetic mixdev, a fake SGLang."""
    import grid_plan as gp
    fake = F.FakeSGL()
    FakeServer.boots, FakeServer.problems, FakeServer.info_patch = [], {}, {}
    suite = SY.make_suite(seed=7, n_g=40, n_r=30, n_u=8, n_x=10, n_comp=8, n_edit=6, n_ord=6)
    p, pins = SY.write_tree(tmp_path, suite, SY.make_mixdev(n_fam=6, per=30))
    vol = tmp_path / "vol"
    (vol / "models").mkdir(parents=True)
    c1, run = F.make_run(tmp_path / "src")
    shutil.copytree(run, vol / "models" / "q35_4b_c2")
    ma, _ = GB.load_tools()
    grid = ma.build_grid(c1, run, tmp_path / "gridref")
    monkeypatch.setattr(gp, "C1_SHA_PREFIX", grid["c1_adapter_sha256"][:8])
    monkeypatch.setattr(C, "C1_ADAPTER_SHA256", grid["c1_adapter_sha256"])
    monkeypatch.setattr(L, "C1_ADAPTER_SHA256", grid["c1_adapter_sha256"])
    monkeypatch.setattr(GB, "locate_c1_adapter", lambda *a, **k: c1)
    cands = {c["name"]: c["adapter_sha256"] for c in grid["candidates"]}
    cand = "last3_a07"
    SY.write_gate_files(p, cand, cands[cand], grid["grid_sha256"], candidates=cands)
    SY.write_parity(p, cand, cands[cand])
    base = F.make_tiny_base(tmp_path / "tbase")
    hooks = {"gpu_name": lambda: GPU, "sglang_version": lambda: "0.5.20", "torch_versions": lambda: {"torch": "2.13.0+cu130", "cuda": "13.0"},
             "load_pin": SV.load_pin, "prepare_base": lambda hf, dest, log: {"base_dir": str(base), "source": "test", "fetched": [], "pins_ok": True},
             "prepare_c1_tok": lambda src, pins_: F.C1_BACKUP, "merge": MD.merge_adapter, "server_cls": FakeServer}
    readers = []

    def mk_reader(spec, log):
        r = InProcL1Reader(spec, log, fake.port)
        readers.append(r)
        return r
    hooks["reader"] = mk_reader
    w = type("W", (), {})()
    w.tmp, w.p, w.pins, w.suite, w.vol, w.hooks, w.fake, w.readers, w.cand, w.cands, w.grid = tmp_path, p, pins, suite, vol, hooks, fake, readers, cand, cands, grid
    w.events, w.run_dir = [], vol / "models" / "q35_4b_c2"
    w.monkeypatch = monkeypatch

    real_prepare = L.prepare_plan                       # captured now: the glue tests replace L.prepare_plan on the shared module

    def plan(run_id="dry1"):
        return real_prepare(p, run_id, pins=pins, p_ref=P_REF, spent_usd=0.0, c2_run_dir=str(w.run_dir), trained_families=SY.trained_fn)

    def session(pl, rows, **kw):
        return LS.L1Session(pl, rows, emit=w.events.append, hooks=hooks, work_root=tmp_path / "work", vol=vol, data_dir=p.lean / "data",
                            c1tok_dir=F.C1_BACKUP, log=lambda s: None, **kw)
    w.plan, w.session = plan, session
    return w


@pytest.fixture
def world(tmp_path, monkeypatch, tokmemo):
    w = build_world(tmp_path, monkeypatch)
    yield w
    w.fake.close()


def a100(w, failed=("b",)):
    """The A100 situation on the fake world: candidate final_a10, pre-gate failed on (b) only, waiver, A98 record kept, new CHOSEN.json, parity record."""
    w.cand = "final_a10"
    sha = w.cands["final_a10"]
    SY.write_gate_files(w.p, "final_a10", sha, w.grid["grid_sha256"], pass_=False, decision="PRE-GATE FAIL (b)", candidates=w.cands, rules=SY.rules_with(list(failed)))
    SY.write_parity(w.p, "final_a10", sha)
    w.monkeypatch.setattr(L, "A98_CHOSEN_SHA_PREFIX", SY.write_chosen(w.p, "final_a10", sha))
    w.monkeypatch.setattr(L, "A100_ADAPTER_SHA256", sha)
    SY.write_waiver(w.p, b_numbers_at_waiver={"final_a10": "-4.83 pp [-8.59, -1.02] (n 600)"})


def run_gpu_job(w, run_id="dry1"):
    pl, rows = w.plan(run_id)
    res = w.session(pl, rows).run()
    return pl, rows, res


# ------------------------------------------------------------------ the GPU job, on fakes
def test_the_job_reads_c1_then_c2_on_one_path_and_returns_what_the_scorer_needs(world):
    w = world
    pl, rows, res = run_gpu_job(w)
    assert res["ok"] and res["errors"] == [] and set(res["reads"]) == {"q35_4b_main500k_l1", "q35_4b_c2_l1"}
    assert FakeServer.boots == ["q35_4b_main500k_l1", "q35_4b_c2_l1"]                         # C1 first, then C2: one container, one job
    blocks = res["models"]
    assert {b["path_sha256"] for b in blocks.values()} == {res["path_sha256"]} and len(res["path_sha256"]) == 64      # ONE served path
    assert blocks["q35_4b_c2_l1"]["adapter_sha256"] == w.cands[w.cand] and blocks["q35_4b_main500k_l1"]["adapter_sha256"] == w.grid["c1_adapter_sha256"]
    for n, sets in res["reads"].items():
        assert [r["id"] for r in sets[L.FINAL_SPLIT]] == [r["id"] for r in rows]             # every call, in order
        assert len(sets[L.MIXDEV_SPLIT]) == pl["mixdev"]["rows"]
        for r, x in zip(rows, sets[L.FINAL_SPLIT]):
            keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
            assert set(x["probs"]) == set(keys) and abs(sum(x["probs"].values()) - 1) < 1e-6
    assert w.readers[0].quit_called
    kinds = [e["event"] for e in w.events]
    assert kinds[:3] == ["container_up", "base_ready", "candidate_built"] and kinds[-1] == "session_done"
    assert SY.MARK not in json.dumps({k: v for k, v in res.items() if k != "reads"}) and SY.MARK not in json.dumps(w.events)      # no text in status / events
    assert not (w.tmp / "work" / "merged" / "q35_4b_c2_l1").exists()                          # merged folders are deleted after use


def test_the_in_memory_reads_equal_an_independent_recomputation(world, tokmemo):
    w = world
    pl, rows, res = run_gpu_job(w)
    RD = tokmemo
    tok, ro, _ = RD.SH.load_c1_tokenizer(F.C1_BACKUP)
    # the C1 read and the C2 read go through different weights, so the recomputation is the readout arithmetic on the fake logprobs only for the shape:
    # the fake SGLang's logprobs depend on the token ids, which are identical for both models -> both reads equal the independent value.
    for r, x in list(zip(rows, res["reads"]["q35_4b_main500k_l1"][L.FINAL_SPLIT]))[::7]:
        want = F.expected_probs(RD.R, RD.SH, tok, ro, r, 2)
        assert x["probs"] == pytest.approx(want, abs=1e-6)
    mix = [json.loads(l) for l in open(w.p.mixdev)]
    for r, x in list(zip(mix, res["reads"]["q35_4b_c2_l1"][L.MIXDEV_SPLIT]))[::11]:
        assert x["id"] == r["id"] and x["probs"] == pytest.approx(F.expected_probs(RD.R, RD.SH, tok, ro, r, 2), abs=1e-6)


def test_a_failed_model_returns_no_sealed_read_and_a_content_free_error(world):
    w = world
    FakeServer.problems["q35_4b_c2_l1"] = ["dtype: 'float16' (pin 'bfloat16')"]
    pl, rows, res = run_gpu_job(w)
    assert not res["ok"] and res["reads"] == {} and res["errors"]
    assert SY.MARK not in json.dumps(res)
    rec = L.write_raw(w.p, pl, res)
    assert not rec["ok"] and not w.p.raw_dir.exists()                                         # nothing sealed was written, the look is not taken
    assert (w.p.out_root / "dry1" / "run_record.json").exists()
    L.guard_gpu_fresh(w.p)                                                                    # so the job may be run again


def test_an_unexpected_exception_is_reported_by_class_name_only(world):
    w = world

    def bad_reader(spec, log):
        r = InProcL1Reader(spec, log, w.fake.port)
        orig = r.gr.run_model

        def boom(cmd):
            raise RuntimeError("leaky message " + SY.MARK + " state text")
        r.gr.run_model = boom
        return r
    w.hooks["reader"] = bad_reader
    pl, rows, res = run_gpu_job(w)
    assert not res["ok"] and res["reads"] == {}
    assert "RuntimeError" in json.dumps(res["errors"]) and "leaky" not in json.dumps(res) and SY.MARK not in json.dumps(res)


def test_server_on_another_path_is_refused(world):
    w = world
    FakeServer.info_patch["q35_4b_c2_l1"] = {"attention_backend": "flashinfer"}
    pl, rows, res = run_gpu_job(w)
    assert not res["ok"] and "served path differs" in json.dumps(res["errors"]) and res["reads"] == {}


def test_budget_gate_stops_before_a_second_model(world):
    w = world
    pl, rows = w.plan()
    res = w.session(pl, rows, prior_usd=13.45).run()
    assert not res["ok"] and res["reads"] == {} and any("budget gate" in e["error"] or "hard stop" in e["error"] for e in res["errors"])


def test_setup_refuses_wrong_host_wrong_candidate_and_changed_rows(world):
    w = world
    pl, rows = w.plan()
    w.hooks["gpu_name"] = lambda: "NVIDIA L4, 23034 MiB"
    r = w.session(pl, rows).run()
    assert not r["ok"] and "H100" in json.dumps(r["errors"])
    w.hooks["gpu_name"] = lambda: GPU
    r = w.session(pl, rows[:-1]).run()
    assert not r["ok"] and "rows of the look differ" in json.dumps(r["errors"])
    bad = json.loads(json.dumps(pl))
    bad["models"][1]["adapter_sha256"] = "f" * 64
    r = w.session(bad, rows).run()
    assert not r["ok"] and "not the one CANDIDATE_C2.json records" in json.dumps(r["errors"])


# ------------------------------------------------------------------ the CPU finish: T, answers, THE look, the verdict
def finish(w, run_id="dry1"):
    pl, rows, res = run_gpu_job(w, run_id)
    assert res["ok"]
    L.write_raw(w.p, pl, res)
    return pl, CLI.finish(w.p, pins=w.pins, out=lambda *a: None)


def test_end_to_end_l1_synthetic(world):
    w = world
    pl, out = finish(w)
    p = w.p
    assert out["look"] == "L1" and out["mode"] == "c1c2" and set(out["verdict"]) >= {"S1", "S2", "S3", "S4", "S5", "S6", "overall"}
    assert p.result.exists() and p.result.stat().st_mode & 0o222 == 0                         # read-only result
    looks = [json.loads(l) for l in open(p.looks)]
    assert [(x["look"], x["status"]) for x in looks] == [("L1", "granted")]                  # exactly one look, in the synthetic tree's own log
    assert set(looks[0]["sha256"]) == {"c1", "c2"} and looks[0]["sha256"]["c2"] == L.sha256_file(p.c2_answers)
    for f in (p.c1_answers, p.c2_answers, p.tfrozen, p.scorer_out, p.sums):
        assert f.exists() and f.stat().st_mode & 0o222 == 0, f.name
    sums = json.loads(p.sums.read_text())
    assert sums["c2_ohs4.jsonl"] == L.sha256_file(p.c2_answers) and sums["c1_ohs4.jsonl"] == L.sha256_file(p.c1_answers)
    t = json.loads(p.tfrozen.read_text())
    assert t["frozen_before_any_sealed_read"] and 0.8 <= t["T"]["c1"]["noul"] <= 1.3 and 0.8 <= t["T"]["c2"]["choice"] <= 1.3 and t["group_kind"].startswith("sampler + pack + register")
    assert out["T_frozen"]["sha256"] == L.sha256_file(p.tfrozen) and out["rules_sha256"] == LV.RULES_SHA
    # the answer files are the raw reads with T applied per type (calibrate.scaled on the aggregated probabilities)
    raw = {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(p.raw_dir / "q35_4b_c2_l1_raw.jsonl")}
    ans = {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(p.c2_answers)}
    from l1_look import l1temp as LT
    for it in w.suite[:25]:
        assert ans[it["id"]] == pytest.approx(LT.apply_T(raw[it["id"]], it["qtype"], t["T"]["c2"]), abs=1e-12)
    # the scorer's aggregates are in the result; nothing per item
    so = out["scorer_output"]
    assert so["look"] == "L1" and so["reports"][0]["model"] == "c1" and so["reports"][1]["model"] == "c2" and so["comparisons"][0]["comparison"] == "C2 - C1"
    rj = json.loads(p.result.read_text())
    rj.pop("rules")
    blob = json.dumps(rj) + p.sums.read_text() + p.tfrozen.read_text()
    assert SY.MARK not in blob and "syn-G-" not in blob and "syn-R-" not in blob and "gold" not in blob.lower().replace("gold option", "")
    assert out["report_only"]["scorer_crosscheck"]["ok"]
    assert out["answer_files_sha256"] == {"c1": L.sha256_file(p.c1_answers), "c2": L.sha256_file(p.c2_answers)}


def test_one_look_only_after_the_first(world):
    w = world
    finish(w)
    p = w.p
    with pytest.raises(L.Refused, match="one look only"):
        CLI.finish(p, pins=w.pins, out=lambda *a: None)
    with pytest.raises(L.Refused, match="one look only"):
        w.plan("again")
    with pytest.raises(L.Refused, match="one look only"):
        L.guard_one_look(p)
    S = LV.load_scorer(p.scorer, SY.sha(p.scorer), name="score_ohs4_again")
    buf = []
    assert S.run_look("L1", {"c1": str(p.c1_answers), "c2": str(p.c2_answers)}, suite_path=str(p.suite), looks_path=str(p.looks), out=buf.append) == 3
    assert "L1 already used" in buf[0]                                                         # the frozen scorer refuses a second L1 itself
    assert [x["status"] for x in map(json.loads, open(p.looks))] == ["granted", "refused"]


def retarget_raw(w, name, text):
    """Replace a raw read AND record its new sha in run_record.json / RAW_RUN.json, so only the content (not the integrity check) is under test."""
    raw = w.p.raw_dir / f"{name}_raw.jsonl"
    os.chmod(raw, 0o644)
    raw.write_text(text)
    sha = L.sha256_file(raw)
    for f in (w.p.out_root / "dry1" / "run_record.json", w.p.raw_dir / "RAW_RUN.json"):
        rec = json.loads(f.read_text())
        rec["files"][f"sealed raw {name}"] = sha
        os.chmod(f, 0o644)
        f.write_text(json.dumps(rec))


def test_answer_files_must_be_complete_and_valid_before_the_look_is_taken(world):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    raw = w.p.raw_dir / "q35_4b_c2_l1_raw.jsonl"
    lines = open(raw).read().splitlines()
    retarget_raw(w, "q35_4b_c2_l1", "\n".join(lines[:-1]) + "\n")                              # one call missing
    with pytest.raises(L.Refused, match="cover exactly the suite"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert not w.p.looks.exists() and not w.p.result.exists()                                  # the look was NOT consumed
    assert not w.p.c1_answers.exists() and not w.p.c2_answers.exists()                          # (b) C1 is valid, C2 is not: NEITHER file is written
    bad = json.loads(lines[0])
    bad["probs"] = {k: float("nan") if i == 0 else v for i, (k, v) in enumerate(bad["probs"].items())}
    retarget_raw(w, "q35_4b_c2_l1", json.dumps(bad) + "\n" + "\n".join(lines[1:]) + "\n")
    with pytest.raises(L.Refused, match="valid probability vector"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert not w.p.looks.exists() and not w.p.c1_answers.exists() and not w.p.c2_answers.exists()


def test_raw_reads_must_be_the_bytes_the_gpu_job_returned(world):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    raw = w.p.raw_dir / "q35_4b_main500k_l1_raw.jsonl"
    os.chmod(raw, 0o644)
    raw.write_text(raw.read_text().replace("0.", "0.0", 1))                                      # any change at all
    with pytest.raises(L.Refused, match="differs from the sha256 in the GPU job's run record"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    raw.unlink()
    with pytest.raises(L.Refused, match="differs from the sha256 in the GPU job's run record"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert not w.p.looks.exists() and not w.p.tfrozen.exists()                                  # refused before T is frozen and before any answer exists


def test_a_crash_after_the_look_is_resumed_without_a_second_look(world, monkeypatch):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    orig = LV.l1_rules

    def boom(*a, **k):
        raise RuntimeError("simulated crash after the scorer granted L1")
    monkeypatch.setattr(LV, "l1_rules", boom)
    with pytest.raises(RuntimeError):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert not w.p.result.exists() and w.p.scorer_out.exists()
    assert [x["status"] for x in map(json.loads, open(w.p.looks))] == ["granted"]
    monkeypatch.setattr(LV, "l1_rules", orig)
    out = CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert w.p.result.exists() and out["verdict"]["overall"]["text"]
    assert [x["status"] for x in map(json.loads, open(w.p.looks))] == ["granted"]              # still ONE look
    # a changed answer file after the granted look is refused (the scorer would refuse it at J too)
    os.chmod(w.p.c2_answers, 0o644)
    w.p.c2_answers.write_text(w.p.c2_answers.read_text() + "\n")
    w.p.result.chmod(0o644)
    w.p.result.unlink()
    with pytest.raises(L.Refused):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)


def test_pre_gate_fail_reads_c1_alone_end_to_end(world):
    w = world
    SY.write_gate_files(w.p, w.cand, w.cands[w.cand], w.grid["grid_sha256"], pass_=False, decision="FAIL", candidates=w.cands)
    pl, rows, res = run_gpu_job(w)
    assert pl["mode"] == "c1" and res["ok"] and set(res["reads"]) == {"q35_4b_main500k_l1"} and FakeServer.boots == ["q35_4b_main500k_l1"]
    L.write_raw(w.p, pl, res)
    out = CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert out["mode"] == "c1" and "gets no OHS-4 look" in out["verdict"]["overall"]["text"] and not w.p.c2_answers.exists()
    assert out["disclosure"] == [L.SPEED3_LINE] and out["parity"] is None
    looks = [json.loads(l) for l in open(w.p.looks)]
    assert set(looks[0]["sha256"]) == {"c1"} and looks[0]["look"] == "L1"
    assert "comparisons" not in out["scorer_output"]
    # the pre-gate flipping between the GPU job and the finish is refused
    w.p.result.chmod(0o644)


def test_the_temperature_is_frozen_once_and_never_refitted(world):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    rr = CLI.raw_run(w.p)
    t1 = CLI.freeze_t(w.p, rr["run_id"], rr["mode"])
    assert CLI.freeze_t(w.p, rr["run_id"], rr["mode"]) == t1                                    # same record
    dev = w.p.out_root / "dry1" / "dev" / "q35_4b_c2_l1.jsonl"
    dev.write_text(dev.read_text() + " ")
    with pytest.raises(L.Refused, match="never re-fitted"):
        CLI.freeze_t(w.p, rr["run_id"], rr["mode"])
    assert not w.p.looks.exists()                                                               # freezing T opens no sealed file and takes no look


def test_a_pre_gate_result_that_changed_after_the_gpu_job_is_refused(world):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    SY.write_gate_files(w.p, w.cand, w.cands[w.cand], w.grid["grid_sha256"], pass_=False, decision="FAIL", candidates=w.cands)
    with pytest.raises(L.Refused, match="changed since the GPU job"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)


def test_check_command_prints_go_and_stop_without_changing_anything(world, capsys):
    w = world
    lines = []
    assert CLI.check(w.p, pins=w.pins, out=lines.append, p_ref=P_REF, spent_usd=0.0, trained_families=SY.trained_fn) == 0
    blob = "\n".join(lines)
    assert "hash pins" in blob and SY.MARK not in blob and blob.strip().splitlines()[-1] in ("GO", "STOP")
    w.p.owner_go.unlink()
    lines.clear()
    assert CLI.check(w.p, pins=w.pins, out=lines.append, p_ref=P_REF, spent_usd=0.0, trained_families=SY.trained_fn) == 2 and lines[-1] == "STOP" and any("L1_OWNER_GO2.json missing" in l for l in lines)
    assert not w.p.looks.exists() and not w.p.raw_dir.exists()


# ------------------------------------------------------------------ the real subprocess reader (what runs in the container)
def test_reader_daemon_runs_in_memory_rows_and_prints_only_counts(world, tokmemo, tmp_path):
    w = world
    pl, rows = w.plan()
    rd = LS.L1Session(pl, rows, hooks=w.hooks, data_dir=w.p.lean / "data", c1tok_dir=F.C1_BACKUP, work_root=tmp_path / "wk", log=lambda s: None)
    rd.c1_tok = F.C1_BACKUP
    spec = rd.reader_spec()
    spec.update({"port": w.fake.port, "workers": 2, "chunk": 4, "ctl_dir": str(tmp_path / "ctl")})
    lines = []
    rp = LS.L1ReaderProc(spec, python=sys.executable, root=str(TRAIN), log=lines.append).start()
    try:
        ready = rp.wait_ready(180)
        assert ready["ok"] and ready["info"]["sets"] == 2 and ready["info"]["prompt_check"]["ok"]
        cmd = {"read_name": "q35_x_l1", "out_dir": str(tmp_path / "o"), "env_meta": {"gpu": "H100", "torch": "t", "cuda": "c", "sglang_version": "0.5.20",
                                                                                        "server_args": {}}, "progress_every": 0, "provenance": {"run_id": "t"}}
        res = rp.run(cmd, 180)
        assert res["ok"] and res["sets"][L.FINAL_SPLIT]["rows"] == len(rows) and res["sets"][L.MIXDEV_SPLIT]["rows"] == pl["mixdev"]["rows"]
        got = [json.loads(l) for l in open(tmp_path / "o" / f"preds_{L.FINAL_SPLIT}" / "q35_x_l1.jsonl")]
        assert [g["id"] for g in got] == [r["id"] for r in rows]
        meta = json.loads((tmp_path / "o" / f"preds_{L.FINAL_SPLIT}" / "q35_x_l1.meta.json").read_text())
        assert meta["tta_choice"] is True and meta["host"] == "modal" and meta["grid_h100"]["data_sha256"] == pl["final"]["rows_sha256"]
        bad = rp.run({"read_name": "ohs_x", "out_dir": str(tmp_path / "o2"), "env_meta": cmd["env_meta"]}, 60)
        assert bad["ok"] is False and "refused" in bad["error"]                                 # an authored refusal keeps its text (no item in it)
        w.fake.close()                                                                          # the server dies: the HTTP error must not travel
        gone = rp.run({**cmd, "read_name": "q35_y_l1", "out_dir": str(tmp_path / "o3")}, 180)
        assert gone["ok"] is False and gone["error"] == "RuntimeError"
    finally:
        rp.quit()
    assert all(SY.MARK not in l for l in lines) and not rp.alive()
    assert all(l[len("[reader] "):].startswith(("ready", "model", "init")) for l in lines), lines


def test_in_memory_set_equals_the_file_set_of_the_grid_reader(world, tokmemo, tmp_path):
    RD = tokmemo
    rows = F.make_rows("gb", 9)
    f = tmp_path / "data" / "gb.jsonl"
    f.parent.mkdir()
    f.write_text("".join(json.dumps(r) + "\n" for r in rows))
    base = {"split": "gb", "tag": "", "views": 2, "perm_seed": None, "job": "L1", "pred_dir": "preds_gb", "tta_choice": True}
    rec = json.loads((C2B / "logs/p7_prompt_sha_check.json").read_text())
    outs = []
    for k, spec in enumerate(({**base, "file": "gb.jsonl"}, {**base, "file": "(memory)", "rows": rows, "rows_sha256": L.canon_sha(rows)})):
        fake = F.FakeSGL()
        try:
            Cls = RD.GridReader if k == 0 else LR.L1Reader
            man = {"gb.jsonl": {"sha256": L.sha256_file(f), "rows": 9}} if k == 0 else {}
            rd = Cls(F.C1_BACKUP, tmp_path / "data", [spec], man, rec, port=fake.port, workers=2, chunk=4)
            rd.init()
            rd.run_model({"read_name": "q35_m", "out_dir": str(tmp_path / f"o{k}"), "env_meta": {"gpu": "H", "torch": "t", "cuda": "c"}})
            outs.append([json.loads(l) for l in open(tmp_path / f"o{k}" / "preds_gb" / "q35_m.jsonl")])
        finally:
            fake.close()
    assert outs[0] == outs[1]
    # a tampered in-memory set is refused by its hash
    fake = F.FakeSGL()
    try:
        bad = LR.L1Reader(F.C1_BACKUP, tmp_path / "data", [{**base, "file": "(memory)", "rows": rows[:-1], "rows_sha256": L.canon_sha(rows)}], {}, rec, port=fake.port)
        with pytest.raises(SystemExit, match="differs from its hash"):
            bad.init()
    finally:
        fake.close()


# ------------------------------------------------------------------ J
class FakeJev:
    """A loopback fake of OpenRouter: POST /v1/systemone answers q0, GET /api/v1/key reports usage / limit."""

    def __init__(self, usage=1.0, limit=10.0, rise_per_call=0.0, model="typesafe/jev-1.13-20260917", fail_status=None, fail_first=0, persist_mod=0, model_cycle=None):
        outer = self
        self.usage, self.limit, self.rise, self.n = usage, limit, rise_per_call, 0
        self.model, self.fail_status, self.fail_first, self.persist_mod, self.model_cycle = model, fail_status, fail_first, persist_mod, model_cycle

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _send(self, obj, code=200):
                data = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                self._send({"data": {"usage": outer.usage, "limit": outer.limit, "limit_remaining": None if outer.limit is None else outer.limit - outer.usage}})

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                q = body["questions"]["q0"]
                outer.n += 1
                outer.usage += outer.rise
                import zlib
                if outer.persist_mod and zlib.crc32(body["state"].encode()) % outer.persist_mod == 0:       # the same calls fail on every pass
                    return self._send({"error": {"message": "SYNTHETIC-ERROR-TEXT"}}, 503)
                if outer.fail_status and (outer.fail_first == 0 or outer.n <= outer.fail_first):
                    return self._send({"error": {"message": "SYNTHETIC-ERROR-TEXT"}}, outer.fail_status)
                if q["type"] == "noul":
                    ans = {"noul": 0.3 + 0.4 * ((outer.n % 7) / 7.0)}
                else:
                    keys = list(q["criteria"])
                    w = [1.0 + ((outer.n + i) % 3) for i in range(len(keys))]
                    ans = {"probabilities": {k: x / sum(w) for k, x in zip(keys, w)}}
                served = outer.model_cycle[outer.n % len(outer.model_cycle)] if outer.model_cycle else outer.model
                body_out = {"usage": {"input_tokens": 10, "output_tokens": 2}, "answers": {"q0": ans}}
                if served is not None:                                   # None = the response carries no model field at all
                    body_out["model"] = served
                self._send(body_out)

        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


def test_j_guards_balance_run_look_and_result(world):
    w = world
    p = w.p
    jev = FakeJev(usage=1.0, limit=10.0)
    try:
        kw = dict(pins=w.pins, balance_url=jev.url + "/api/v1/key", key="DRYRUN-NOT-A-KEY", poll_s=0.2, out=lambda *a: None)
        with pytest.raises(L.Refused, match="L1_RESULT.json missing"):                          # J before the L1 verdict is logged
            J.go(p, **kw)
        finish(w)
        runner_args = ["--dry-run", "--base-url", jev.url, "--out-dir", str(p.answers)]
        # the live balance must be known and large enough
        low = FakeJev(usage=9.5, limit=10.0)
        unknown = FakeJev(usage=1.0, limit=None)
        try:
            with pytest.raises(L.Refused, match="left on the OpenRouter key"):
                J.go(p, **{**kw, "balance_url": low.url + "/api/v1/key"}, runner_args=runner_args)
            with pytest.raises(L.Refused, match="remaining balance is unknown"):
                J.go(p, **{**kw, "balance_url": unknown.url + "/api/v1/key"}, runner_args=runner_args)
            with pytest.raises(L.Refused, match="could not be read live"):
                J.go(p, **{**kw, "balance_url": "http://127.0.0.1:1/api/v1/key"}, runner_args=runner_args)
        finally:
            low.close()
            unknown.close()
        assert not p.jev_answers.exists() and not p.j_result.exists()                          # no call was made, no J look was taken
        # the paid path, on the loopback fake
        res = J.go(p, **kw, runner_args=runner_args)
        assert res["look"] == "J" and res["answered_calls"] == len(w.suite) and res["unanswered_calls"] == 0 and p.j_result.stat().st_mode & 0o222 == 0
        assert res["openrouter"]["before"]["usage"] == 1.0 and res["jev_model"] == "jev-1.13"
        assert set(res["claims_report_only"]) == {"c2", "c1"} and "both pinned Jev runs" in res["note"]
        assert res["jev_usage_totals"]["calls"] == len(w.suite) and res["jev_usage_totals"]["errors"] == 0
        looks = [json.loads(l) for l in open(p.looks)]
        assert [(x["look"], x["status"]) for x in looks] == [("L1", "granted"), ("J", "granted")]
        # the scorer re-verified the L1 answer files (it refuses a J if they changed) and J is once
        with pytest.raises(L.Refused, match="already taken"):
            J.go(p, **kw, runner_args=runner_args)
        with pytest.raises(L.Refused, match="already taken"):
            J.score_j(p, pins=w.pins, out=lambda *a: None)
        S = LV.load_scorer(p.scorer, SY.sha(p.scorer), name="score_ohs4_j_again")
        buf = []
        assert S.run_look("J", {"jev": str(p.jev_answers)}, suite_path=str(p.suite), looks_path=str(p.looks), out=buf.append) == 3 and "J already used" in buf[0]
        blob = p.j_result.read_text()
        assert SY.MARK not in blob and "syn-G-" not in blob
    finally:
        jev.close()


def test_j_refuses_when_an_l1_answer_file_changed_and_check_never_spends(world):
    w = world
    p = w.p
    finish(w)
    jev = FakeJev()
    try:
        lines = []
        assert J.check(p, pins=w.pins, balance_url=jev.url + "/api/v1/key", key="DRYRUN-NOT-A-KEY", out=lines.append) == 0
        assert lines[-1].endswith("GO") and "OpenRouter live" in "\n".join(lines) and jev.n == 0     # check made no Jev call
        os.chmod(p.c1_answers, 0o644)
        p.c1_answers.write_text(p.c1_answers.read_text() + " ")
        with pytest.raises(L.Refused, match="differs from the file the L1 look scored"):
            J.guards(p, w.pins)
    finally:
        jev.close()


def test_j_watchdog_stops_the_runner_above_the_cap(tmp_path):
    slow = tmp_path / "slow_runner.py"
    slow.write_text("import time\nprint('started', flush=True)\ntime.sleep(60)\n")
    p = L.L1Paths(tmp_path / "lean", tmp_path / "synthetic_suite")
    p.jev_runner.parent.mkdir(parents=True)
    shutil.copyfile(slow, p.jev_runner)
    usage = {"v": 1.0}

    def opener(req, timeout=0):
        usage["v"] += 1.0                                                                       # +1.00 USD per poll
        return io.BytesIO(json.dumps({"data": {"usage": usage["v"], "limit": 10.0, "limit_remaining": 10.0 - usage["v"]}}).encode())
    t0 = time.time()
    run = J.run_runner(p, "k", [], "http://x", {"usage": 1.0, "limit": 10.0, "limit_remaining": 9.0}, cap_usd=1.5, poll_s=0.2, opener=opener)
    assert run["stopped_at_cap"] and time.time() - t0 < 20 and run["returncode"] != 0


def test_j_balance_helpers_never_return_the_key(tmp_path):
    env = tmp_path / ".env"
    env.write_text("# c\nOTHER=1\nOPENROUTER_API_KEY=\"sk-test-key-123\"\n")
    key = J.read_key(env)
    assert key == "sk-test-key-123"
    out = J.balance(key, "http://x", opener=lambda req, timeout=0: io.BytesIO(b'{"data":{"usage":2.5,"limit":10,"limit_remaining":7.5,"label":"sk-test-key-123"}}'))
    assert out == {"usage": 2.5, "limit": 10, "limit_remaining": 7.5} and "sk-test" not in json.dumps(out)
    assert J.balance_ok(out) is None and J.balance_ok({"limit_remaining": 1.0}) and J.balance_ok({"limit_remaining": None})
    env.write_text("NOPE=1\n")
    with pytest.raises(L.Refused, match="OPENROUTER_API_KEY is missing"):
        J.read_key(env)


def test_end_to_end_l1_with_b_waived_under_a100(world):
    """The A100 path: the pre-gate failed on (b) only, the owner's record is on file -> C1 + final_a10 in ONE job; the disclosure lines come first."""
    w = world
    a100(w)
    pl, out = finish(w)
    assert pl["mode"] == "c1c2" and out["mode"] == "c1c2" and FakeServer.boots == ["q35_4b_main500k_l1", "q35_4b_c2_l1"] and out["candidate"]["grid_candidate"] == "final_a10"
    assert out["pregate"]["pass"] is False and out["pregate"]["effective_pass"] and out["pregate"]["waived"] == ["b"]
    assert list(out)[0] == "disclosure" and out["disclosure"][0].startswith("OWNER OVERRIDE (PREREG A100, 18 Oct 2026 ~19:20 UTC / 3:20 PM ET, after the result)")
    assert "final_a10 C2 \u2212 C1 = \u22124.83 pp" in out["disclosure"][0] and out["disclosure"][1] == L.SPEED3_LINE
    assert out["verdict"]["S6"]["pass"] and out["verdict"]["S6"]["pregate_checks_failed_and_waived_by_the_owner"] == {"b": "A100"}
    assert out["parity"]["argmax_agree"] == 0.9985 and out["parity"]["n"] == 2000
    if out["verdict"]["overall"]["all_pass"]:
        assert "passing H100 parity record is logged" in out["verdict"]["overall"]["text"]
    assert out["carried_rulings"] and any(x.startswith("A68") for x in out["carried_rulings"])
    assert w.p.c2_answers.exists() and json.loads(w.p.raw_dir.joinpath("RAW_RUN.json").read_text())["pregate"]["waived"] == ["b"]
    assert [x["status"] for x in map(json.loads, open(w.p.looks))] == ["granted"]


def test_a_waiver_that_changed_between_the_gpu_job_and_the_finish_is_refused(world):
    w = world
    a100(w)
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    SY.write_waiver(w.p, b_numbers_at_waiver={"final_a10": "-9.99 pp (edited after the job)"})        # still a valid A100 record, different bytes
    with pytest.raises(L.Refused, match="waiver record changed"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert not w.p.looks.exists()


# ------------------------------------------------------------------ RULING item 1: the temperature, on the fake world
def test_the_t_record_follows_the_ruling(world):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    rr = CLI.raw_run(w.p)
    t = CLI.freeze_t(w.p, rr["run_id"], rr["mode"])
    from l1_look import l1temp as LT
    from test_l1_temp import reference_fit
    mix = [json.loads(l) for l in open(w.p.mixdev)]
    fit_rows = [r for r in mix if r["meta"]["family"] in SY.TRAINED]
    assert t["trained_families"] == SY.TRAINED and t["fit_rows"] == len(fit_rows) < len(mix)           # the untrained family (T05) is out
    assert t["group_kind"] == "sampler + pack + register (union)" and t["ruling"].endswith("RULING_L1_PRELOOK.md item 1") and t["clip"] == [0.8, 1.3]
    assert t["frozen_before_any_sealed_read"] and t["c1_shipped_A5_T_report_only"] == {"noul": 1.0, "choice": 1.0, "source": LT.SHIPPED_C1_A5["source"]}
    for key, name in (("c1", L.C1_READ), ("c2", L.C2_READ)):
        preds = {d["id"]: d["probs"] for d in map(json.loads, open(w.p.out_root / "dry1" / "dev" / f"{name}.jsonl"))}
        for qt in ("noul", "choice"):
            raw, clipped, n = reference_fit(fit_rows, preds, qt, LT.group_ids)
            f = t["fits"][key][qt]
            assert f["T_raw"] == raw and f["T"] == clipped == t["T"][key][qt] and f["n_groups"] == n and 0.8 <= f["T"] <= 1.3
            assert set(f["groups_per_kind"]) == {"sampler", "pack", "register"} and f["groups_per_kind"]["sampler"] == 1
            assert "M_at_1.0" in f and "M_at_T_raw" in f
        assert set(t["report_only_fits"][key]) == {"family", "pack_only", "register_only"}                # the family-keyed fits are report-only
    assert t["mixdev_sha256"] == SY.sha(w.p.mixdev) and t["inputs"]["c2"]["sha256"] == SY.sha(w.p.out_root / "dry1" / "dev" / "q35_4b_c2_l1.jsonl")


def test_the_t_fit_stops_without_a_fallback_when_a_type_has_fewer_than_two_groups(world):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    rr = CLI.raw_run(w.p)
    with pytest.raises(L.Refused, match="no fallback"):
        CLI.freeze_t(w.p, rr["run_id"], rr["mode"], trained=["no-such-family"])
    assert not w.p.tfrozen.exists() and not w.p.looks.exists()


def test_the_trained_family_list_of_the_job_is_what_the_finish_uses(world):
    w = world
    pl, out = finish(w)
    assert out["T_frozen"]["trained_families"] == SY.TRAINED == pl["trained_families"]
    assert json.loads(w.p.raw_dir.joinpath("RAW_RUN.json").read_text())["trained_families"] == SY.TRAINED


# ------------------------------------------------------------------ RULING item 8: parity guard at the finish
def test_a_parity_record_that_changed_after_the_gpu_job_is_refused(world):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    SY.write_parity(w.p, w.cand, w.cands[w.cand], agree=0.9991)
    with pytest.raises(L.Refused, match="parity record changed"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    (w.p.train / f"PARITY_{w.cand}.json").unlink()
    with pytest.raises(L.Refused, match="PARITY_last3_a07.json missing"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert not w.p.looks.exists() and not w.p.result.exists()


def test_the_gpu_job_is_not_launched_without_a_parity_record(world):
    w = world
    (w.p.train / f"PARITY_{w.cand}.json").unlink()
    with pytest.raises(L.Refused, match="PARITY_last3_a07.json missing"):
        w.plan()
    assert FakeServer.boots == []                                                        # nothing was asked of the GPU


# ------------------------------------------------------------------ RULING item 6: the pinned Jev model must be what answered
def j_world(w, **jev_kw):
    finish(w)
    jev = FakeJev(**jev_kw)
    kw = dict(pins=w.pins, balance_url=jev.url + "/api/v1/key", key="DRYRUN-NOT-A-KEY", poll_s=0.2, out=lambda *a: None,
              runner_args=["--dry-run", "--base-url", jev.url, "--out-dir", str(w.p.answers)])
    return jev, kw


@pytest.mark.parametrize("fail_status", [404, 410])
def test_j_model_gone_takes_no_look_and_records_not_run(world, fail_status):
    w = world
    jev, kw = j_world(w, fail_status=fail_status)
    try:
        with pytest.raises(L.Refused, match="no J look was taken"):
            J.go(w.p, **kw)
        looks = [json.loads(l) for l in open(w.p.looks)]
        assert [(x["look"], x["status"]) for x in looks] == [("L1", "granted")]               # the J look was NOT spent
        rec = json.loads(w.p.j_result.read_text())
        assert rec["status"] == "not_run" and rec["reason"] == "J not run: pinned jev-1.13 not served (accepted served id typesafe/jev-1.13-20260917)" and "not evaluable" in rec["claims"]
        assert rec["served_check"]["model_not_served"] and rec["disclosure"][0] == J.ONE_READ_LINE and J.JEV_VERSION_LINE in rec["disclosure"]
        assert w.p.j_result.stat().st_mode & 0o222 == 0 and not w.p.jev_answers.exists()
        assert "SYNTHETIC-ERROR-TEXT" not in w.p.j_result.read_text()                         # no response text is stored
    finally:
        jev.close()


def test_j_all_bad_requests_is_an_all_error_run_and_is_not_scored(world):
    w = world
    jev, kw = j_world(w, fail_status=400)
    try:
        with pytest.raises(L.Refused, match="no J look was taken"):
            J.go(w.p, **kw)
        rec = json.loads(w.p.j_result.read_text())
        assert rec["status"] == "not_run" and rec["served_check"]["answered"] == 0 and any("400/422" in r or "no call was answered" in r for r in rec["served_check"]["reasons"])
        assert not any(x["look"] == "J" for x in map(json.loads, open(w.p.looks)))
    finally:
        jev.close()


def test_j_a_served_model_other_than_the_pin_takes_no_look(world):
    w = world
    jev, kw = j_world(w, model="jev-1.14")
    try:
        with pytest.raises(L.Refused, match="no J look was taken"):
            J.go(w.p, **kw)
        rec = json.loads(w.p.j_result.read_text())
        assert rec["status"] == "not_run" and rec["served_check"]["served_models"] == {"jev-1.14": len(w.suite)}
        assert not any(x["look"] == "J" for x in map(json.loads, open(w.p.looks)))
    finally:
        jev.close()


def test_j_a_not_run_record_does_not_use_up_the_look_and_a_later_good_run_replaces_it(world):
    w = world
    jev, kw = j_world(w, fail_status=404)
    try:
        with pytest.raises(L.Refused):
            J.go(w.p, **kw)
    finally:
        jev.close()
    assert json.loads(w.p.j_result.read_text())["status"] == "not_run"
    good = FakeJev()
    try:
        res = J.go(w.p, **{**kw, "balance_url": good.url + "/api/v1/key", "runner_args": ["--dry-run", "--base-url", good.url, "--out-dir", str(w.p.answers)]})
        assert res["status"] == "taken" and res["served_check"]["ok"] and res["served_check"]["served_models"] == {J.SERVED_ID: len(w.suite)}
        assert res["disclosure"][0] == J.ONE_READ_LINE and res["disclosure"][2] == L.SPEED3_LINE and res["disclosure"][1].startswith("OHS-4 Jev comparator: Jev 1.13, requested as 'jev-1.13'")
        assert f"All {len(w.suite):,} responses reported the served id 'typesafe/jev-1.13-20260917'" in res["disclosure"][1]
        assert all(c["comparator"].startswith("Jev 1.13") for c in res["claims_report_only"].values())
        assert [(x["look"], x["status"]) for x in map(json.loads, open(w.p.looks))] == [("L1", "granted"), ("J", "granted")]
    finally:
        good.close()


def test_j_transient_failures_are_retried_by_the_runners_resume_before_scoring(world):
    w = world
    jev, kw = j_world(w, fail_status=503, fail_first=12)
    try:
        res = J.go(w.p, **kw)
        assert res["runner_passes"] == 2 and res["unanswered_calls"] == 0 and res["answered_calls"] == len(w.suite)
        assert res["served_check"]["ok"] and jev.n == len(w.suite) + 12
    finally:
        jev.close()


def test_j_an_all_error_transient_run_is_not_scored(world):
    w = world
    jev, kw = j_world(w, fail_status=503)
    try:
        with pytest.raises(L.Refused, match="no J look was taken"):
            J.go(w.p, **kw)                                                  # nothing was answered at all: an all-error run is not scored
        assert not any(x["look"] == "J" for x in map(json.loads, open(w.p.looks)))
        assert not w.p.j_result.exists() or json.loads(w.p.j_result.read_text())["status"] == "not_run"
    finally:
        jev.close()


def test_j_calls_that_stay_unanswered_after_the_resumes_count_wrong_and_are_disclosed(world):
    w = world
    jev, kw = j_world(w, persist_mod=11)
    try:
        res = J.go(w.p, **kw)
        assert res["status"] == "taken" and res["runner_passes"] == J.MAX_PASSES and res["unanswered_calls"] > 0
        assert res["answered_calls"] + res["unanswered_calls"] == len(w.suite) and res["served_check"]["ok"]
        assert res["scorer_output"]["reports"][0]["headline_G+R+X"]["coverage"] < 1.0                 # the frozen scorer prints the coverage
    finally:
        jev.close()


def test_j_refuses_a_runner_whose_model_id_is_not_the_pin(world, monkeypatch):
    w = world
    jev, kw = j_world(w)
    try:
        monkeypatch.setattr(J, "PINNED_MODEL", "jev-9.9")
        with pytest.raises(L.Refused, match="not the A38 pin jev-9.9"):
            J.go(w.p, **kw)
        assert J.served_matches("typesafe/jev-1.13-20260917") and not J.served_matches("jev-1.13") and not J.served_matches("openrouter/jev-1.13")
        assert not any(x["look"] == "J" for x in map(json.loads, open(w.p.looks)))
    finally:
        jev.close()


# ------------------------------------------------------------------ BLOCKING 1: a crash after the scorer logged L1 but before its output was saved
def test_a_crash_between_the_granted_look_and_the_saved_scorer_output_is_resumed_without_a_second_look(world, monkeypatch):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    captured = {}

    def crash_after_the_look(p, S, files):
        buf = []
        rc = S.run_look("L1", {k: str(v) for k, v in files.items()}, suite_path=str(p.suite), looks_path=str(p.looks), out=buf.append)
        assert rc == 0
        captured["printed"] = json.loads(buf[0])
        raise RuntimeError("synthetic crash: the look is logged granted, its output is not saved")
    real_take = CLI.take_look
    monkeypatch.setattr(CLI, "take_look", crash_after_the_look)
    with pytest.raises(RuntimeError, match="synthetic crash"):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert [x["status"] for x in map(json.loads, open(w.p.looks))] == ["granted"] and not w.p.scorer_out.exists() and not w.p.result.exists()
    monkeypatch.setattr(CLI, "take_look", real_take)
    monkeypatch.setattr(CLI, "take_look", lambda *a, **k: pytest.fail("a second look must never be taken"))
    out = CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert [x["status"] for x in map(json.loads, open(w.p.looks))] == ["granted"]              # still ONE look
    assert w.p.result.exists() and out["verdict"]["overall"]["text"]
    assert any("was not saved (a crash after the look was granted)" in x for x in out["disclosure"]) and "No second look was taken" in " ".join(out["disclosure"])
    so = out["scorer_output"]
    assert so["recomputed_without_a_second_look"] is True
    assert so["reports"] == captured["printed"]["reports"] and so["comparisons"] == captured["printed"]["comparisons"] and so["suite_sha256"] == captured["printed"]["suite_sha256"]
    assert w.p.scorer_out.stat().st_mode & 0o222 == 0


def test_the_resume_still_refuses_an_answer_file_that_changed(world, monkeypatch):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    real = CLI.take_look

    def crash(p, S, files):
        real(p, S, files)
        raise RuntimeError("synthetic crash after the look and its saved output")
    monkeypatch.setattr(CLI, "take_look", crash)
    with pytest.raises(RuntimeError):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    os.chmod(w.p.scorer_out, 0o644)
    w.p.scorer_out.unlink()                                                                      # the crash lost the output as well
    os.chmod(w.p.c2_answers, 0o644)
    w.p.c2_answers.write_text(w.p.c2_answers.read_text() + " ")
    with pytest.raises(L.Refused):
        CLI.finish(w.p, pins=w.pins, out=lambda *a: None)
    assert [x["status"] for x in map(json.loads, open(w.p.looks))] == ["granted"]


# ------------------------------------------------------------------ freeze-t end to end (the CLI command)
def test_freeze_t_command_runs_end_to_end(world, monkeypatch, capsys):
    w = world
    pl, rows, res = run_gpu_job(w)
    L.write_raw(w.p, pl, res)
    monkeypatch.setattr(CLI.L, "L1Paths", lambda *a, **k: w.p)
    monkeypatch.setattr(CLI.L, "A38_PINS", w.pins)
    assert CLI.main(["freeze-t"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert set(printed) == {"T", "report_only_fits", "trained_families", "fit_rows", "sha256"} and printed["sha256"] == L.sha256_file(w.p.tfrozen)
    assert printed["trained_families"] == SY.TRAINED and set(printed["T"]) == {"c1", "c2"} and set(printed["report_only_fits"]["c2"]) == {"family", "pack_only", "register_only"}
    assert not w.p.looks.exists() and not w.p.c1_answers.exists()                              # freezing T opens no sealed read and takes no look
    assert CLI.main(["freeze-t"]) == 0                                                          # idempotent: the same record
    assert json.loads(capsys.readouterr().out)["sha256"] == printed["sha256"]


# ------------------------------------------------------------------ (d) J: a crash after the J look was granted
def test_j_crash_after_the_look_is_resumed_without_a_second_read(world, monkeypatch):
    w = world
    jev, kw = j_world(w)
    try:
        orig = J.LV.j_claims
        monkeypatch.setattr(J.LV, "j_claims", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("synthetic crash after the J look")))
        with pytest.raises(RuntimeError, match="synthetic crash"):
            J.go(w.p, **kw)
        n_calls = jev.n
        assert [x["status"] for x in map(json.loads, open(w.p.looks))] == ["granted", "granted"] and not w.p.j_result.exists()
        monkeypatch.setattr(J.LV, "j_claims", orig)
        res = J.go(w.p, **{**kw, "balance_url": "http://127.0.0.1:1/api/v1/key", "key": None, "env_file": w.tmp / "no-such-env"})   # no runner, no balance call, no key read
        assert res["status"] == "taken" and jev.n == n_calls                                         # NO second Jev read
        assert [(x["look"], x["status"]) for x in map(json.loads, open(w.p.looks))] == [("L1", "granted"), ("J", "granted")]
        assert w.p.j_result.stat().st_mode & 0o222 == 0 and res["claims_report_only"]
    finally:
        jev.close()


def test_j_crash_before_the_scorer_output_was_saved_is_recomputed_not_re_looked(world, monkeypatch):
    w = world
    jev, kw = j_world(w)
    try:
        real_write = L.write_json

        def flaky(path, obj, mode=None):
            if str(path).endswith("J_scorer_output.json"):
                raise RuntimeError("synthetic crash before the J scorer output was saved")
            return real_write(path, obj, mode)
        monkeypatch.setattr(L, "write_json", flaky)
        with pytest.raises(RuntimeError, match="before the J scorer output"):
            J.go(w.p, **kw)
        monkeypatch.setattr(L, "write_json", real_write)
        n_calls = jev.n
        assert not w.p.j_scorer_out.exists() and [x["look"] for x in map(json.loads, open(w.p.looks))] == ["L1", "J"]
        res = J.score_j(w.p, pins=w.pins, out=lambda *a: None)
        assert res["status"] == "taken" and jev.n == n_calls and res["scorer_output"]["recomputed_without_a_second_look"] is True
        assert any("was not saved (a crash after the look was granted)" in x for x in res["disclosure"])
        assert [x["look"] for x in map(json.loads, open(w.p.looks))] == ["L1", "J"]
    finally:
        jev.close()


def test_j_resume_refuses_a_changed_jev_answer_file(world, monkeypatch):
    w = world
    jev, kw = j_world(w)
    try:
        monkeypatch.setattr(J.LV, "j_claims", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("synthetic crash")))
        with pytest.raises(RuntimeError):
            J.go(w.p, **kw)
        w.p.jev_answers.write_text(w.p.jev_answers.read_text() + " ")
        monkeypatch.undo()
        with pytest.raises(L.Refused, match="differs from the one the granted J look scored"):
            J.score_j(w.p, pins=w.pins, out=lambda *a: None)
    finally:
        jev.close()


# ------------------------------------------------------------------ RULING 6b: exactly one accepted SERVED id
def test_the_accepted_served_id_is_hard_coded_exactly():
    assert J.SERVED_ID == "typesafe/jev-1.13-20260917" and J.PINNED_MODEL == "jev-1.13"
    for ok, bad in (("typesafe/jev-1.13-20260917", ("jev-1.13", "typesafe/jev-1.13", "typesafe/jev-1.13-20260918", "typesafe/jev-1.13-20260917 ", "Typesafe/jev-1.13-20260917",
                                                     "typesafe/jev-1.14-20261014", "typesafe/jev-1.14", "typesafe/jev-router", "x/typesafe/jev-1.13-20260917", "", None, 5)),):
        assert J.served_matches(ok)
        assert not any(J.served_matches(b) for b in bad)


@pytest.mark.parametrize("served,why", [
    ("typesafe/jev-1.14-20261014", "not the accepted typesafe/jev-1.13-20260917"),
    ("typesafe/jev-router", "not the accepted typesafe/jev-1.13-20260917"),
    ("typesafe/jev-1.13-20260918", "not the accepted typesafe/jev-1.13-20260917"),
    ("jev-1.13", "not the accepted typesafe/jev-1.13-20260917"),
    (None, "report no served model id"),
])
def test_j_any_other_served_id_is_refused_before_the_look(world, served, why):
    w = world
    jev, kw = j_world(w, model=served)
    try:
        with pytest.raises(L.Refused, match="no J look was taken") as e:
            J.go(w.p, **kw)
        assert why in str(e.value)
        assert not any(x["look"] == "J" for x in map(json.loads, open(w.p.looks)))                 # the look is NOT spent
        rec = json.loads(w.p.j_result.read_text())
        assert rec["status"] == "not_run" and "not evaluable" in rec["claims"] and rec["served_check"]["accepted_served_id"] == J.SERVED_ID
    finally:
        jev.close()


def test_j_more_than_one_distinct_served_id_is_refused_even_if_one_is_the_accepted_one(world):
    w = world
    jev, kw = j_world(w, model_cycle=[J.SERVED_ID, J.SERVED_ID, "typesafe/jev-1.13-20260918"])
    try:
        with pytest.raises(L.Refused, match="no J look was taken") as e:
            J.go(w.p, **kw)
        assert "more than one distinct served model id (2)" in str(e.value) or "not the accepted" in str(e.value)
        rec = json.loads(w.p.j_result.read_text())
        assert rec["status"] == "not_run" and len(rec["served_check"]["served_models"]) == 2
        assert not any(x["look"] == "J" for x in map(json.loads, open(w.p.looks)))
    finally:
        jev.close()


def test_j_a_response_without_an_id_among_good_ones_is_refused(world):
    w = world
    jev, kw = j_world(w, model_cycle=[J.SERVED_ID, None])
    try:
        with pytest.raises(L.Refused, match="no J look was taken") as e:
            J.go(w.p, **kw)
        assert "report no served model id" in str(e.value)
    finally:
        jev.close()


def test_j_the_look_is_taken_on_the_complete_pass_with_no_new_call_and_the_not_run_record_is_kept(world, monkeypatch):
    """The 6b situation: a first guard refused after a complete, paid pass; the corrected check scores that same pass once, sending nothing."""
    w = world
    jev, kw = j_world(w, rise_per_call=0.00003)
    try:
        monkeypatch.setattr(J, "SERVED_ID", "typesafe/jev-1.13-20990101")                          # the 'first guard': a wrong accepted id
        with pytest.raises(L.Refused, match="no J look was taken"):
            J.go(w.p, **kw)
        first = w.p.j_result.read_bytes()
        n_calls = jev.n
        assert json.loads(first)["status"] == "not_run" and n_calls == len(w.suite) and not any(x["look"] == "J" for x in map(json.loads, open(w.p.looks)))
        spent_first = json.loads(first)["openrouter"]["spent_usd"]
        monkeypatch.undo()                                                                           # the corrected guard
        archived = J.archive_not_run(w.p)
        assert archived.name.startswith("J_RESULT_NOTRUN_") and archived.name.endswith("Z.json") and archived.read_bytes() == first and not w.p.j_result.exists()
        assert archived.stat().st_mode & 0o222 == 0
        res = J.score_j(w.p, pins=w.pins, out=lambda *a: None)                                       # `score`: no runner, no key, no balance call, no Jev call
        assert jev.n == n_calls and res["status"] == "taken" and res["served_check"]["ok"]
        assert [(x["look"], x["status"]) for x in map(json.loads, open(w.p.looks))] == [("L1", "granted"), ("J", "granted")]
        line = res["disclosure"][1]
        assert f"All {len(w.suite):,} responses reported the served id 'typesafe/jev-1.13-20260917' (a 17 Sep 2026 snapshot" in line
        assert "Jev 1.14 (14 Oct) is not the comparator" in line and "corrected by ruling 6b" in line and "scored once (Jev spend $" in line
        assert f"${spent_first:.2f}" in line
        assert w.p.j_result.stat().st_mode & 0o222 == 0 and sorted(f.name for f in w.p.train.glob("J_RESULT_NOTRUN_*.json")) == [archived.name]
        assert all(c["comparator"] == "Jev 1.13 (requested jev-1.13; served typesafe/jev-1.13-20260917)" for c in res["claims_report_only"].values())
    finally:
        jev.close()


def test_j_a_not_run_record_is_renamed_never_overwritten_or_deleted(world):
    w = world
    jev, kw = j_world(w, model="typesafe/jev-router")
    try:
        with pytest.raises(L.Refused):
            J.go(w.p, **kw)
        first = w.p.j_result.read_bytes()
        with pytest.raises(L.Refused):
            J.score_j(w.p, pins=w.pins, out=lambda *a: None)                                         # a second refusal: the first record must survive
        kept = sorted(w.p.train.glob("J_RESULT_NOTRUN_*.json"))
        assert len(kept) == 1 and kept[0].read_bytes() == first and json.loads(w.p.j_result.read_text())["status"] == "not_run"
        with pytest.raises(L.Refused):
            J.score_j(w.p, pins=w.pins, out=lambda *a: None)
        assert len(sorted(w.p.train.glob("J_RESULT_NOTRUN_*.json"))) == 2                              # suffixed, never overwritten
    finally:
        jev.close()


def test_j_a_taken_result_is_never_archived_or_replaced(world):
    w = world
    jev, kw = j_world(w)
    try:
        res = J.go(w.p, **kw)
        assert res["status"] == "taken"
        with pytest.raises(L.Refused, match="not a not-run record"):
            J.archive_not_run(w.p)
        assert not list(w.p.train.glob("J_RESULT_NOTRUN_*.json"))
    finally:
        jev.close()
