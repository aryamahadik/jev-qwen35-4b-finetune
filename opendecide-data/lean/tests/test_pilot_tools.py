"""CPU tests for the pilot tooling (FINETUNE_PLAN.md 2.4 / 4.2): replay_steps.py, rank_microbatches.py, the pilot parts
of modal_od.py (smoke_heavy, speed, relay --name-suffix) and pilot/compare_relay.py. Fake model, no GPU, no Modal call.

Run:  ../.venv/bin/python -m pytest -q tests/test_pilot_tools.py
(OD_GOLDEN_TESTS=1 also replays the real 501,732-row golden file: about 10 s and 3 GB of RAM.)
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
from pathlib import Path

import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pilot"))
import compare_relay as cr  # noqa: E402
import decoder_io  # noqa: E402
import modal_od  # noqa: E402
import rank_microbatches as rm  # noqa: E402
import replay_steps as rs  # noqa: E402
import train_decoder as td  # noqa: E402
from test_train_loss import _write_data, choice, fake_env, noul, opts, rel  # noqa: E402,F401

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")  # torch.autocast("cuda") on a CPU-only box

CFG = {"base": "fake", "grad_ckpt": False, "batch": 8, "epochs": 2.0, "beta": 0.1, "log_every": 1,
       "train_file": "train.jsonl", "rel_file": "rels.jsonl", "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.5,
       "style": "cygnet", "ckpt_every_min": 0}


@pytest.fixture(autouse=True)
def _keep_globals(monkeypatch):
    """train() and PromptLengths set decoder_io's layout/style/labels; restore them after each test."""
    for k in ("LAYOUT", "STYLE", "WIDE"):
        monkeypatch.setattr(decoder_io, k, getattr(decoder_io, k))


def _replayed_calls(units, c, n):
    """What the trainer's gradient forward sees per step (micro_tokens 0): batch rows then twins, with permutations."""
    out = []
    for step, b, p, tw in rs.stream(units, c):
        if step == n:
            return out
        out.append(([r["id"] for r in b] + [b[i]["id"] for i, _ in tw], p + [q for _, q in tw]))


# ---------------------------------------------------------------- replay_steps.py

def test_replay_stream_equals_train(fake_env, tmp_path):
    _write_data(tmp_path)
    res = td.train(dict(CFG), tmp_path, tmp_path / "out", dev="cpu")
    grad = [(ids, pp) for ids, pp, g in res["model"].calls if g]
    assert len(grad) == res["meta"]["steps"]
    c = rs.stream_cfg(CFG)
    _, _, _, units, _ = rs.load_data(c, tmp_path)
    assert _replayed_calls(units, c, len(grad)) == grad
    assert _replayed_calls(units, c, len(grad)) == grad  # the caller's units keep their order: replayable


@pytest.mark.parametrize("at", [1, 5, 9])
def test_replay_matches_checkpoint_state(fake_env, tmp_path, at):
    _write_data(tmp_path)
    td.train({**CFG, "stop_at_step": at}, tmp_path, tmp_path / "run", dev="cpu")
    st = torch.load(tmp_path / "run" / "_ckpt" / "state.pt", weights_only=False)
    c = rs.stream_cfg(CFG)
    _, _, _, units, _ = rs.load_data(c, tmp_path)
    assert rs.last_batch_hashes(units, c, [at]) == {at: st["last_batch"]}
    for step, *_ in rs.stream(units, c):
        if step == at - 1:
            break
    assert random.getstate() == st["py_rng"]


def _brute_pass(units, seed, bs):
    random.seed(seed)
    us = list(units)
    random.shuffle(us)
    n, cur, rows = 0, [], 0
    for u in us:
        cur += u
        if len(cur) >= bs:
            n, rows, cur = n + 1, rows + len(cur), []
    return n, rows, len(cur)


@pytest.mark.parametrize("seed", [0, 1, 20260925])
def test_first_pass_counts(seed):
    rng = random.Random(seed)
    units, k = [], 0
    for _ in range(300):
        u = []
        for _ in range(rng.choice([1, 1, 2, 3, 5])):
            u.append(noul(f"r{k}", f"c{len(units)}") if k % 3 else choice(f"r{k}", f"c{len(units)}", opts(3), "o0"))
            k += 1
        units.append(u)
    c = rs.stream_cfg({"seed": seed, "batch": 16, "style": "cygnet", "perm_twin": 0.3})
    p = rs.first_pass(units, c)
    n, rows, left = _brute_pass(units, seed, 16)
    assert (p["batches"], p["rows"], p["dropped_rows"]) == (n, rows, left)
    assert p["complete"] and p["rows"] + p["dropped_rows"] == k
    seen = []
    rs.first_pass(units, c, on_step=lambda s, b, pp, tw: seen.append(s), limit=7)
    assert seen == list(range(7))


@pytest.mark.parametrize("rows,bs,n", [(41, 4, 7), (501732, 16, 30457), (100, 16, 6), (48, 16, 3)])
def test_epochs_for_gives_exactly_n_steps(rows, bs, n):
    e = rs.epochs_for(n, rows, bs)
    assert rs.n_steps(rows, bs, e) == n == math.ceil(rows / bs * e)  # train()'s own expression
    assert e <= n / (rows / bs)
    if (rows, bs, n) == (41, 4, 7):  # the plain ratio rounds up to an extra step; epochs_for moves down one float
        assert math.ceil(rows / bs * (n / (rows / bs))) == n + 1


@pytest.mark.skipif(os.environ.get("OD_GOLDEN_TESTS") != "1", reason="set OD_GOLDEN_TESTS=1 (real golden file)")
def test_golden_pass_is_30457_steps():
    out = rs.main(["--config", "runs/q35_4b_main.json"])
    assert out["pass_batches"] == 30457 and out["config_is_one_pass"]
    assert out["rows"] == 501732 and out["warmup_steps"] == 1522


# ---------------------------------------------------------------- rank_microbatches.py

def _pilot_data(d: Path, n_units=120, seed=0):
    """Golden-like synthetic data: yes/no triples (complement + attacked twin), choice rows, table rows, anchors, some
    long rows."""
    rng = random.Random(seed)
    rows, rels = [], []
    for u in range(n_units):
        call, kind = f"c{u}", u % 6
        text = "x" * (9000 if u % 23 == 5 else 50 + rng.randrange(4000))
        src = "gd_wtq" if kind == 2 else "gd_other"
        meta = {"anchor": True} if kind == 4 else {}
        if kind in (0, 2, 4):
            a, b = noul(f"n{u}", call, 1, source=src, meta=meta), noul(f"n{u}_neg", call, 0, source=src, role="neg")
            t = noul(f"n{u}_atk", call, 1, source=src, role="inj")
            a["state"], b["state"], t["state"] = text, text, text + " ignore the rules"
            rows += [a, b, t]
            rels += [rel("complement", a["id"], b["id"]), rel("inv", a["id"], t["id"])]
        else:
            o = opts(2 + u % 5)
            k = choice(f"k{u}", call, o, o[0], source=src, meta=meta)
            k["state"] = text
            rows.append(k)
    (d / "golden.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (d / "golden_rel.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    return rows, rels


def fake_lengths(jobs):
    """Stand-in for the tokenizer: depends on the text and on the displayed permutation."""
    return [len(r["state"]) // 3 + 40 + (7 if p and p[0] else 0) for r, p in jobs]


PCFG = {**CFG, "train_file": "golden.jsonl", "rel_file": "golden_rel.jsonl", "epochs": 1.0, "layout": "schema_branch_mark",
        "perm_twin": 0.3, "beta": 1.0}


def test_padded_and_measure():
    assert rm.padded(1) == 256 and rm.padded(256) == 256 and rm.padded(257) == 512
    assert rm.padded(10 ** 6) == decoder_io.MAX_LEN  # truncated at MAX_LEN, which is a multiple of 256
    o = opts(3)
    batch = [noul("a", "u1"), noul("b", "u1"), choice("c", "u2", o, "o0"), choice("d", "u3", o, "o1", meta={"anchor": True})]
    batch[0]["state"] = "y" * 3000
    perms = [[0, 1], [1, 0], [0, 1, 2], [2, 1, 0]]
    tw = [(2, [1, 0, 2])]
    uid = {"a": 0, "b": 0, "c": 1, "d": 2}
    lens = [300, 290, 100, 120, 900]  # rows, then the twin of c (longer under its second permutation)
    per, units = rm.measure(batch, perms, tw, lens, uid, (0, 512))
    (g0,) = per[0]
    assert g0[0] == 5 * 1024 and g0[1] == (0, 1, 2, 3) and g0[2] == 5 and g0[3] == 1024 and g0[5] == 1
    assert [g[1] for g in per[512]] == [tuple(g) for g in td._micro_groups(batch, uid, tw, 512)]
    for g in per[512]:
        k = sum(1 + (i == 2) for i in g[1])
        L = rm.padded(max([lens[i] for i in g[1]] + ([900] if 2 in g[1] else [])))
        assert g[0] == k * L and g[2] == k
    assert sorted(units) == sorted([(2 * 512, (0, 1), 2, 512), (2 * 1024, (2,), 2, 1024), (256, (3,), 1, 256)])


def test_rank_end_to_end(tmp_path, monkeypatch):
    _pilot_data(tmp_path)
    (tmp_path / "cfg.json").write_text(json.dumps({"name": "x", **PCFG}))
    monkeypatch.setattr(rm, "PromptLengths", lambda *a, **k: fake_lengths)
    out = rm.main(["--config", str(tmp_path / "cfg.json"), "--data-dir", str(tmp_path), "--out", str(tmp_path / "hb.json"),
                   "--micro-tokens", "0,1024,2048", "--top", "4"])
    assert json.loads((tmp_path / "hb.json").read_text()) == json.loads(json.dumps(out))
    c = rs.stream_cfg(PCFG)
    _, _, _, units, _ = rs.load_data(c, tmp_path)
    n_pass = rs.first_pass(units, c)["batches"]
    assert out["pass_steps_replayed"] == out["steps_measured"] == n_pass > 20
    assert out["ordinary_steps"] == list(range(20))
    steps = {s: (b, p, tw) for s, b, p, tw in _stream_n(units, c, n_pass)}
    uid = rs.unit_ids(units)
    for mt in (0, 1024, 2048):
        s = out["settings"][str(mt)]
        allg = sorted((g[0] for st, (b, p, tw) in steps.items()
                       for g in rm.measure(b, p, tw, fake_lengths(rm.jobs_of(b, p, tw)), uid, (mt,))[0][mt]), reverse=True)
        assert [g["tokens"] for g in s["top"]] == allg[:4]  # brute force over the whole pass
        for g in s["top"]:
            rec = out["batches"][str(g["step"])]
            assert set(g["rows"]) <= set(rec["ids"]) and max(rec["group_tokens"][str(mt)]) >= g["tokens"]
        assert s["heaviest_anchor"]["n_anchor"] > 0 and s["heaviest_table"]["n_table"] > 0
        assert s["groups"] == len(allg) and s["over_budget"] == sum(t > mt for t in allg if mt)
    assert out["heaviest_unit"]["tokens"] == max(u["tokens"] for u in out["top_units"])
    assert out["settings"]["0"]["max_groups_per_step"] == 1 and out["settings"]["1024"]["max_groups_per_step"] > 1
    smp = rm.main(["--config", str(tmp_path / "cfg.json"), "--data-dir", str(tmp_path), "--out", str(tmp_path / "s.json"),
                   "--micro-tokens", "1024", "--sample", "3"])
    assert 20 <= smp["steps_measured"] <= 23 and smp["pass_steps_replayed"] == n_pass


def _stream_n(units, c, n):
    for s, b, p, tw in rs.stream(units, c):
        if s == n:
            return
        yield s, b, p, tw


def test_prompt_lengths_match_cand_logits_tensor(monkeypatch):
    """The cost model equals the tensor cand_logits builds (real pinned tokenizer; skipped when not cached)."""
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    try:
        pl = rm.PromptLengths("cygnet", "schema_branch_mark")
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"tokenizer not available offline: {e!r}")
    o = opts(30)  # past 26 options: two-letter labels (decoder_io.WIDE, set by Readout)
    rows = [noul("a", "c1"), choice("b", "c2", o, "o3"), noul("c", "c3")]
    rows[0]["state"], rows[2]["card"] = "a long text " * 400, "- Yes: it holds\n- No: it does not"
    perms = [[1, 0], list(reversed(range(30))), [0, 1]]
    lens = pl(list(zip(rows, perms)))
    texts = [pl.ro.prompt(r, p) for r, p in zip(rows, perms)]
    enc = pl.tok(texts, add_special_tokens=False, truncation=True, max_length=decoder_io.MAX_LEN, padding="longest",
                 pad_to_multiple_of=decoder_io.PAD_MULTIPLE, return_tensors="pt")
    assert tuple(enc["input_ids"].shape) == (3, rm.padded(max(lens)))
    assert enc["attention_mask"].sum(1).tolist() == lens


# ---------------------------------------------------------------- modal_od.py: relay --name-suffix, pilot guards

FROZEN = {"name": "q35_4b_main500k", "base": "Qwen/Qwen3.5-4B", "base_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
          "recipe": "A3", "train_file": "v14_parts/golden_train.jsonl", "rel_file": "v14_parts/golden_relations.jsonl",
          "epochs": 0.9712363276890207, "lr": 7e-05, "batch": 16, "r": 16, "alpha": 32, "seed": 20260925,
          "style": "cygnet", "layout": "schema_branch_mark", "micro_tokens": 10240, "targets": "QWEN35",
          "ckpt_every_min": 10, "log_every": 50, "aux_norm": "batch"}


class _FakeRemote:
    def __init__(self):
        self.calls = []

    def remote(self, name, cfg):
        self.calls.append((name, json.loads(json.dumps(cfg))))
        return {"stopped": True, "next_step": 7, "n_steps": 30457, "meta": {"log": []}}


def _old_relay_cfg(cfg, expect_resume=False, stop_at_step=0):
    """The relay config as the code before --name-suffix built it (stop_after_min 0)."""
    cfg = dict(cfg)
    name = cfg.pop("name")
    cfg["targets"] = modal_od.QWEN35_TARGETS
    cfg.update({"no_overwrite": True, "expect_resume": expect_resume, "stop_at_step": stop_at_step, "stop_at_unix": 0})
    return name, cfg


@pytest.fixture
def relay_env(tmp_path, monkeypatch):
    (tmp_path / "runs").mkdir()
    (tmp_path / "runs/x.json").write_text(json.dumps(FROZEN))
    monkeypatch.setattr(modal_od, "HERE", tmp_path)
    fake = _FakeRemote()
    monkeypatch.setattr(modal_od, "train_relay35", fake)
    return fake


def test_relay_default_is_unchanged(relay_env, tmp_path):
    relay = modal_od.relay.info.raw_f
    relay(config="runs/x.json", stop_at_step=7)
    relay(config="runs/x.json", expect_resume=True, stop_at_step=7, name_suffix="", log_every=0)
    assert relay_env.calls == [_old_relay_cfg(FROZEN, False, 7), _old_relay_cfg(FROZEN, True, 7)]
    assert (tmp_path / "logs/relay_q35_4b_main500k_stopped_at_7.json").exists()


def test_relay_name_suffix_and_log_every(relay_env, tmp_path):
    relay = modal_od.relay.info.raw_f
    relay(config="runs/x.json", stop_at_step=7, name_suffix="_pA1")
    relay(config="runs/x.json", stop_at_step=7, name_suffix="_pB", log_every=1)
    (n1, c1), (n2, c2) = relay_env.calls
    name0, cfg0 = _old_relay_cfg(FROZEN, False, 7)
    assert (n1, c1) == (name0 + "_pA1", cfg0)  # same run identity, another folder
    assert n2 == name0 + "_pB" and c2 == {**cfg0, "log_every": 1}
    assert (tmp_path / "logs/relay_q35_4b_main500k_pA1_stopped_at_7.json").exists()
    for bad in ("pA1", "_p/../x", "_", "_p A"):
        with pytest.raises(SystemExit):
            relay(config="runs/x.json", stop_at_step=7, name_suffix=bad)
    assert len(relay_env.calls) == 2


def test_frozen_matches_relay_and_pilot_dir(relay_env):
    name, cfg = modal_od._frozen("runs/x.json")
    old_name, old = _old_relay_cfg(FROZEN)
    assert name == old_name and cfg == {k: v for k, v in old.items() if k in FROZEN}
    assert modal_od._pilot_dir("pilot_speed_h100_mt10240") == Path("/vol/models/pilot_speed_h100_mt10240")
    for bad in ("q35_4b_main500k", "pilot_", "pilot_a/../../q35_4b_main500k", "x_pilot_a", "", None):
        with pytest.raises(ValueError):
            modal_od._pilot_dir(bad)
    assert modal_od._pilot_tag("H100!", 10240, "") == "h100_mt10240"
    assert modal_od._pilot_tag("L4", 0, "expandable_segments:True") == "l4_mt0_exp"


# ---------------------------------------------------------------- modal_od.py: smoke_heavy and speed on CPU

def _heavy_json(tmp_path, monkeypatch, mts="0,1024,2048"):
    _pilot_data(tmp_path)
    (tmp_path / "cfg.json").write_text(json.dumps({"name": "x", **PCFG}))
    monkeypatch.setattr(rm, "PromptLengths", lambda *a, **k: fake_lengths)
    rm.main(["--config", str(tmp_path / "cfg.json"), "--data-dir", str(tmp_path), "--out", str(tmp_path / "hb.json"),
             "--micro-tokens", mts, "--top", "3"])
    return json.loads((tmp_path / "hb.json").read_text())


def test_smoke_spec(tmp_path, monkeypatch):
    hv = _heavy_json(tmp_path, monkeypatch)
    modal_od._check_heavy(hv, PCFG)
    with pytest.raises(SystemExit):
        modal_od._check_heavy(hv, {**PCFG, "seed": 1})
    with pytest.raises(SystemExit):
        modal_od._smoke_spec(hv, 4096)
    sp = modal_od._smoke_spec(hv, 1024)
    assert [b["step"] for b in sp["ordinary"]] == list(range(20))
    preds = [b["pred_max_tokens"] for b in sp["heavy"]]
    assert preds == sorted(preds) and len({b["step"] for b in sp["heavy"]}) == len(sp["heavy"])
    tags = "+".join(b["tag"] for b in sp["heavy"])
    for t in ("top1", "top2", "top3", "anchor", "table", "unit"):
        assert t in tags
    top1 = next(b for b in sp["heavy"] if "top1" in b["tag"].split("+"))
    assert top1["pred_max_tokens"] == hv["settings"]["1024"]["top"][0]["tokens"] == max(preds)


@pytest.mark.parametrize("mt", [0, 1024])
def test_smoke_heavy_runs_the_exact_batches(fake_env, tmp_path, monkeypatch, mt):
    hv = _heavy_json(tmp_path, monkeypatch)
    spec = modal_od._smoke_spec(hv, mt)
    cfg = {**PCFG, "expect_kd_targets": 12345, "micro_tokens": 99}  # full-file checks are dropped; spec wins
    res = modal_od._smoke_heavy_impl(cfg, spec, tmp_path, tmp_path / "work", dev="cpu")
    script = spec["ordinary"] + spec["heavy"]
    assert res["steps_run"] == res["steps_planned"] == len(script) and res["oom"] is None and res["pass_memory"]
    assert [s["tag"] for s in res["steps"]] == [b["tag"] for b in script]
    assert all(s["loss"] is not None and math.isfinite(s["loss"]) for s in res["steps"])
    # every step trained exactly its scripted rows, plus one twin per recorded twin position
    for s, b in zip(res["steps"], script):
        assert sum(f[0] for f in s["forwards"]) == len(b["ids"]) + len(b["twins"])
        if mt == 0:
            assert len(s["forwards"]) == 1
        else:
            assert len(s["forwards"]) == len(hv["batches"][str(b["step"])]["groups"][str(mt)])
    mini = [json.loads(x)["id"] for x in (tmp_path / "work/mini_train.jsonl").read_text().splitlines()]
    assert set(mini) == {i for b in script for i in b["ids"]} and len(mini) == len(set(mini))
    assert not (tmp_path / "work/out/_ckpt").exists()


def test_smoke_heavy_reports_oom(fake_env, tmp_path, monkeypatch):
    hv = _heavy_json(tmp_path, monkeypatch)
    spec = modal_od._smoke_spec(hv, 0)
    real, n, batches0 = td.cand_logits, {"grad": 0}, td.batches

    def boom(model, ro, rows, dev, perms=None):
        if torch.is_grad_enabled():
            n["grad"] += 1
            if n["grad"] == 23:
                raise torch.cuda.OutOfMemoryError("CUDA out of memory. Tried to allocate 9.00 GiB")
        return real(model, ro, rows, dev, perms)
    monkeypatch.setattr(td, "cand_logits", boom)
    res = modal_od._smoke_heavy_impl(PCFG, spec, tmp_path, tmp_path / "work", dev="cpu")
    assert res["oom"].startswith("OutOfMemoryError") and not res["pass_memory"]
    assert res["steps_run"] == 23 and res["oom_step"]["k"] == 22 and res["oom_step"]["tag"] == spec["heavy"][2]["tag"]
    assert td.cand_logits is boom and td.batches is batches0  # the probe put everything back

    def other(model, ro, rows, dev, perms=None):
        raise ValueError("not a memory error")
    monkeypatch.setattr(td, "cand_logits", other)
    with pytest.raises(ValueError):
        modal_od._smoke_heavy_impl(PCFG, spec, tmp_path, tmp_path / "work2", dev="cpu")


def test_speed_probe_changes_nothing(fake_env, tmp_path):
    """speed: s/step over steps skip..n-2, batch hashes equal the CPU replay, and the run is identical to one without
    the probe (same log, same checkpoint)."""
    _pilot_data(tmp_path)
    cfg = {**PCFG, "micro_tokens": 1024}
    res = modal_od._speed_impl(cfg, 12, tmp_path, tmp_path / "pilot_speed", dev="cpu", skip=2)
    assert res["stopped"] and res["steps_run"] == 12 and res["probe_ok"] and res["oom"] is None
    assert res["timed_steps"] == 9 and res["s_per_step"] > 0 and len(res["step_s"]) == 12
    c = rs.stream_cfg(cfg)
    _, _, _, units, _ = rs.load_data(c, tmp_path)
    assert res["first_batch"] == rs.last_batch_hashes(units, c, [1])[1]
    assert res["last_batch"] == rs.last_batch_hashes(units, c, [12])[12]
    ref = td.train({**cfg, "resume": False, "stop_at_step": 12}, tmp_path, tmp_path / "plain", dev="cpu")
    strip = lambda log: [{k: v for k, v in r.items() if k != "min"} for r in log]  # noqa: E731
    assert strip(res["log"]) == strip(ref["meta"]["log"])
    a = torch.load(tmp_path / "pilot_speed/_ckpt/state.pt", weights_only=False)
    b = torch.load(tmp_path / "plain/_ckpt/state.pt", weights_only=False)
    assert a["tensors"] == b["tensors"] and a["py_rng"] == b["py_rng"] and a["last_batch"] == b["last_batch"]


# ---------------------------------------------------------------- pilot/compare_relay.py

def _ckpt(folder: Path, tensors: dict, log: list, step=300, last="h300", lr=7e-5):
    from safetensors.torch import save_file
    folder.mkdir(parents=True)
    save_file(tensors, str(folder / "trainable.safetensors"))
    rng = random.Random(7)
    torch.save({"step": step, "log": log, "last_batch": last, "fingerprint": "fp", "py_rng": rng.getstate(),
                "twin_rng": random.Random(8).getstate(), "cfg": {"lr": lr}}, folder / "state.pt")
    files = sorted(p for p in folder.rglob("*") if p.is_file())
    (folder / "manifest.json").write_text(json.dumps({"step": step, "fingerprint": "fp",
                                                      "files": {p.name: cr._sha(p) for p in files}}))
    return folder


def _log(noise, seed, lr=7e-5, of=1000, n=300):
    g = random.Random(seed)
    return [{"step": s, "of": of, "loss": 2.0 - s / 300 + (noise * g.random() if noise else 0.0), "n_cons": s % 5,
             "n_inv": 3, "n_twin": s % 2, "n_rel_skipped": 0, "lr": lr * cr.lr_factor(s + 1, of)} for s in range(n)]


def _runs(tmp_path, d2=1e-3, db=1.2e-3, g2=0.01, gb=0.012, same=False):
    gen = torch.Generator().manual_seed(0)
    base = {"a.lora_A": torch.randn(16, 64, generator=gen), "a.lora_B": torch.randn(64, 16, generator=gen)}
    noise = {k: torch.randn(v.shape, generator=gen) for k, v in base.items()}
    unit = math.sqrt(sum(float((v ** 2).sum()) for v in base.values()) / sum(float((v ** 2).sum()) for v in noise.values()))
    mk = lambda d: {k: base[k] + d * unit * noise[k] for k in base}  # noqa: E731  (d = relative distance to A1)
    a1 = _ckpt(tmp_path / "A1", base, _log(0, 0))
    a2 = _ckpt(tmp_path / "A2", dict(base) if same else mk(d2), _log(0, 0) if same else _log(g2 * 2, 1))
    b = _ckpt(tmp_path / "B", dict(base) if same else mk(db), _log(0, 0) if same else _log(gb * 2, 2))
    return {"A1": cr.load_run(str(a1)), "A2": cr.load_run(str(a2)), "B": cr.load_run(str(b))}


def test_compare_relay_pass_and_noise_fails(tmp_path):
    rep = cr.verdict(_runs(tmp_path / "ok"))
    assert rep["verdict"] == "PASS", rep
    assert rep["d_A1_A2"] == pytest.approx(1e-3, rel=1e-4) and rep["d_A1_B"] == pytest.approx(1.2e-3, rel=1e-4)
    assert rep["loss_steps"] == [150, 150]
    rep = cr.verdict(_runs(tmp_path / "w", db=2e-3))
    assert rep["verdict"] == "FAIL" and "weights" in rep["noise_problems"][0]
    rep = cr.verdict(_runs(tmp_path / "l", gb=0.03))
    assert rep["verdict"] == "FAIL" and "loss" in rep["noise_problems"][0]


def test_compare_relay_bit_identical_rule(tmp_path):
    assert cr.verdict(_runs(tmp_path / "same", same=True))["verdict"] == "PASS"
    runs = _runs(tmp_path / "b", same=True)
    runs["B"]["tensors"] = {k: v + 1e-6 for k, v in runs["B"]["tensors"].items()}
    rep = cr.verdict(runs)
    assert rep["verdict"] == "FAIL" and "bit-identical" in rep["noise_problems"][0]


def test_compare_relay_exact_checks(tmp_path):
    runs = _runs(tmp_path / "lr")
    runs["B"]["log"][200]["lr"] *= 1.0000001
    rep = cr.verdict(runs)
    assert rep["verdict"] == "FAIL" and any("step 200 lr" in p for p in rep["exact_problems"])
    runs = _runs(tmp_path / "cnt")
    runs["A2"]["log"][17]["n_inv"] = 4
    assert any("step 17 n_inv" in p for p in cr.verdict(runs)["exact_problems"])
    runs = _runs(tmp_path / "steps")
    del runs["B"]["log"][250]
    assert any("logged steps differ" in p for p in cr.verdict(runs)["exact_problems"])
    runs = _runs(tmp_path / "hash")
    runs["B"]["state"]["last_batch"] = "other"
    assert any("last_batch differs" in p for p in cr.verdict(runs)["exact_problems"])
    assert any("CPU replay" in p for p in cr.verdict(_runs(tmp_path / "rp"), expect_last_batch="nope")["exact_problems"])
    runs = _runs(tmp_path / "man")
    (tmp_path / "man/B/trainable.safetensors").write_bytes(b"corrupt")
    assert any("missing or changed" in p for p in cr.verdict(runs)["exact_problems"])
    ok = '{"resumed_at_step": 150, "of": 30457, "checks": "manifest, config, ...: all match"}\n'
    assert cr.resume_problems("noise\n" + ok, 150) == []
    assert cr.resume_problems(ok, 151) and cr.resume_problems("no line", 150)


def test_compare_relay_cli_and_log_formats(tmp_path, capsys):
    _runs(tmp_path)
    meta = tmp_path / "b_meta.json"
    meta.write_text(json.dumps({"cfg": {}, "log": _log(0.024, 2)}))
    text = tmp_path / "a2.log"
    text.write_text("container started\n" + "".join(json.dumps(r) + "\n" for r in _log(0.02, 1)) + "done\n")
    assert cr.load_log(str(meta)) == _log(0.024, 2) and cr.load_log(str(text)) == _log(0.02, 1)
    run_log = tmp_path / "a_run.log"
    run_log.write_text("container started\n" + json.dumps(_log(0, 0)[-1]) + "\n")
    args = ["--a1", str(tmp_path / "A1"), "--a2", str(tmp_path / "A2"), "--a2-log", str(text),
            "--b", str(tmp_path / "B/trainable.safetensors"), "--b-log", str(meta),
            "--a1-run-log", str(run_log), "--a2-run-log", str(run_log)]
    assert cr.main(args) == 1  # a bare .safetensors has no batch hash: not a full proof
    assert capsys.readouterr().out.strip().endswith("FAIL")
    assert cr.main(args + ["--no-state-ok"]) == 0
    out = capsys.readouterr().out
    assert out.strip().endswith("PASS") and "no state.pt for ['B']" in out


def test_compare_relay_fails_when_a1_or_a2_resumed(tmp_path, capsys):
    """A preempted A1/A2 is re-run by Modal and resumes silently (only a resumed_at_step line in its tee log): its own
    resume error would widen the noise floor and hide a resume defect in B, so it fails the verdict (review item 15)."""
    straight = "container started\n" + "".join(json.dumps(r) + "\n" for r in _log(0, 0)[:3])
    resumed = straight + '{"resumed_at_step": 5, "of": 30457, "checks": "manifest, config, ...: all match"}\n'
    assert cr.straight_problems(straight, "A1") == []
    assert "A2 was resumed" in cr.straight_problems(resumed, "A2")[0]
    rep = cr.verdict(_runs(tmp_path / "ok"), straight_texts={"A1": straight, "A2": straight})
    assert rep["verdict"] == "PASS", rep
    rep = cr.verdict(_runs(tmp_path / "res"), straight_texts={"A1": straight, "A2": resumed})
    assert rep["verdict"] == "FAIL" and any("A2 was resumed" in p for p in rep["exact_problems"])
    _runs(tmp_path / "cli")
    (tmp_path / "a1.log").write_text(straight)
    (tmp_path / "a2.log").write_text(resumed)
    args = ["--a1", str(tmp_path / "cli/A1"), "--a2", str(tmp_path / "cli/A2"), "--b", str(tmp_path / "cli/B")]
    with pytest.raises(SystemExit):  # the run logs are required
        cr.main(args)
    capsys.readouterr()
    assert cr.main(args + ["--a1-run-log", str(tmp_path / "a1.log"), "--a2-run-log", str(tmp_path / "a1.log")]) == 0
    assert cr.main(args + ["--a1-run-log", str(tmp_path / "a1.log"), "--a2-run-log", str(tmp_path / "a2.log")]) == 1
    assert "A2 was resumed" in capsys.readouterr().out


def test_compare_relay_lr_formula_matches_trainer(fake_env, tmp_path):
    _write_data(tmp_path)
    res = td.train(dict(CFG), tmp_path, tmp_path / "out", dev="cpu")
    log = res["meta"]["log"]
    assert cr.exact_log_problems({"a": log, "b": log}, 10 ** 9, base_lr=res["meta"]["cfg"]["lr"]) == []
    assert cr.exact_log_problems({"a": log}, 10 ** 9, base_lr=res["meta"]["cfg"]["lr"] * 1.01)


# ---------------------------------------------------------------- modal_od.py: local entrypoints (no Modal call)

class _FakeFn:
    """Stands in for a Modal Function: with_options / remote / starmap, recording every call."""

    def __init__(self, fail_first=False):
        self.gpu, self.env, self.calls, self.fail_first = None, None, [], fail_first

    def with_options(self, gpu=None, env=None):
        self.gpu, self.env = gpu, env
        return self

    def remote(self, *a):
        self.calls.append(("remote", a))
        if self.fail_first:
            raise RuntimeError("container failed")
        return {"ok": True, "n": len(self.calls)}

    def starmap(self, args, return_exceptions=False):
        for a in args:
            self.calls.append(("starmap", a))
            yield {"ok": True, "n": len(self.calls)}


def test_run_all_first_alone_then_parallel():
    fn = _FakeFn()
    assert list(modal_od._run_all(fn, [(1,), (2,), (3,)])) == [{"ok": True, "n": 1}, {"ok": True, "n": 2}, {"ok": True, "n": 3}]
    assert [k for k, _ in fn.calls] == ["remote", "starmap", "starmap"]
    out = list(modal_od._run_all(_FakeFn(fail_first=True), [(1,), (2,)]))
    assert isinstance(out[0], RuntimeError) and out[1]["ok"]
    assert list(modal_od._run_all(fn, [])) == []


def test_pilot_entrypoints(tmp_path, monkeypatch):
    d = tmp_path / "data" / "v14_parts"
    d.mkdir(parents=True)
    _pilot_data(d, n_units=300)  # batch 16: more than 20 steps in the pass
    (d / "golden.jsonl").rename(d / "golden_train.jsonl")
    (d / "golden_rel.jsonl").rename(d / "golden_relations.jsonl")
    (tmp_path / "runs").mkdir()
    (tmp_path / "runs/x.json").write_text(json.dumps(FROZEN))
    monkeypatch.setattr(rm, "PromptLengths", lambda *a, **k: fake_lengths)
    rm.main(["--config", str(tmp_path / "runs/x.json"), "--data-dir", str(tmp_path / "data"), "--micro-tokens", "0,10240",
             "--out", str(tmp_path / "pilot/heavy_batches.json"), "--top", "2"])
    monkeypatch.setattr(modal_od, "HERE", tmp_path)
    smoke, speed = _FakeFn(), _FakeFn()
    monkeypatch.setattr(modal_od, "smoke_heavy_remote", smoke)
    monkeypatch.setattr(modal_od, "speed_remote", speed)
    _, cfg = modal_od._frozen("runs/x.json")
    modal_od.smoke_heavy.info.raw_f(micro_tokens="0,10240", config="runs/x.json")
    assert smoke.gpu == "H100!" and smoke.env is None and [k for k, _ in smoke.calls] == ["remote", "starmap"]
    assert [a[0] for _, a in smoke.calls] == [cfg, cfg] and [a[1]["micro_tokens"] for _, a in smoke.calls] == [0, 10240]
    assert all(len(a[1]["ordinary"]) == 20 and a[1]["heavy"] and a[2] == "" for _, a in smoke.calls)
    assert json.loads((tmp_path / "logs/pilot/smoke_heavy_h100_mt10240.json").read_text())["ok"]
    modal_od.speed.info.raw_f(micro_tokens="0,10240", gpu="L4", config="runs/x.json", alloc_conf="expandable_segments:True")
    names = [a[0] for _, a in speed.calls]
    assert names == ["pilot_speed_l4_mt0_exp", "pilot_speed_l4_mt10240_exp"] and speed.gpu == "L4"
    assert speed.env == {"PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
    assert [a[1] for _, a in speed.calls] == [{**cfg, "micro_tokens": 0}, {**cfg, "micro_tokens": 10240}]
    assert [a[2:] for _, a in speed.calls] == [(100, 10, "expandable_segments:True")] * 2
    assert (tmp_path / "logs/pilot/speed_l4_mt0_exp.json").exists()
    with pytest.raises(SystemExit):  # heavy_batches.json ranked for another config
        (tmp_path / "runs/y.json").write_text(json.dumps({**FROZEN, "seed": 1}))
        modal_od.smoke_heavy.info.raw_f(micro_tokens="0", config="runs/y.json")


def test_pilot_values_run_once():
    """'10240,10240' (RUNBOOK step 4 when step 3 kept 10240) is one container, not two writing one result file."""
    assert modal_od._mt_values("10240,0,10240,16384,0") == [10240, 0, 16384]
    assert modal_od._mt_values("24576") == [24576]


def test_pilot_entrypoints_dedupe_values(tmp_path, monkeypatch):
    d = tmp_path / "data" / "v14_parts"
    d.mkdir(parents=True)
    _pilot_data(d, n_units=300)
    (d / "golden.jsonl").rename(d / "golden_train.jsonl")
    (d / "golden_rel.jsonl").rename(d / "golden_relations.jsonl")
    (tmp_path / "runs").mkdir()
    (tmp_path / "runs/x.json").write_text(json.dumps(FROZEN))
    monkeypatch.setattr(rm, "PromptLengths", lambda *a, **k: fake_lengths)
    rm.main(["--config", str(tmp_path / "runs/x.json"), "--data-dir", str(tmp_path / "data"), "--micro-tokens", "10240",
             "--out", str(tmp_path / "pilot/heavy_batches.json"), "--top", "2"])
    monkeypatch.setattr(modal_od, "HERE", tmp_path)
    smoke, speed = _FakeFn(), _FakeFn()
    monkeypatch.setattr(modal_od, "smoke_heavy_remote", smoke)
    monkeypatch.setattr(modal_od, "speed_remote", speed)
    modal_od.smoke_heavy.info.raw_f(micro_tokens="10240,10240", gpu="L4", config="runs/x.json")
    modal_od.speed.info.raw_f(micro_tokens="10240,10240", config="runs/x.json")
    assert [k for k, _ in smoke.calls] == ["remote"] and [k for k, _ in speed.calls] == ["remote"]


def _decorator_kwargs(fn_name):
    import ast
    tree = ast.parse((ROOT / "modal_od.py").read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == fn_name)
    (dec,) = [d for d in fn.decorator_list if isinstance(d, ast.Call) and getattr(d.func, "attr", "") == "function"]
    return {k.arg: ast.literal_eval(k.value) for k in dec.keywords if k.arg in ("gpu", "single_use_containers")}


@pytest.mark.parametrize("fn_name", ["smoke_heavy_remote", "speed_remote"])
def test_pilot_functions_use_fresh_containers(fn_name):
    """Each pilot input runs in a fresh process: in a reused container the previous input's CUDA cache inflates the
    peak memory (a false memory FAIL) and PYTORCH_CUDA_ALLOC_CONF cannot be set again (review item 14). The flag is
    only visible on the decorator (Modal sends it at deploy time)."""
    import inspect
    import modal
    assert "single_use_containers" in inspect.signature(modal.App.function).parameters
    assert _decorator_kwargs(fn_name) == {"gpu": "H100!", "single_use_containers": True}


def test_data_ignore_uploads_run_files_and_skips_label_shards():
    """The image's data/ upload keeps every file a run config trains on (including the 2B's KD file) and never the
    ~1 GB label-shard directory (review item 13). Paths are relative to data/, as Modal passes them."""
    wanted = {"v14_parts/train_2b_golden_kd.jsonl", "v14_parts/golden_dev.jsonl", "v14_parts/golden_dev_relations.jsonl",
              "dev.jsonl", "train_2b_kd.jsonl",
              # C rounds (C_TRAIN_RECIPE.md v4 config sketch), checked even before a round's config exists
              "c_parts/c_train_r1.jsonl", "c_parts/c_rel_r1.jsonl", "c_parts/c_train_r2.jsonl", "c_parts/c_rel_r2.jsonl"}
    # configs the default image never launches (runs/README.md): each must be refused on the laptop by _launch_checks
    not_default = {**modal_od.SPAWN_LAUNCHED,
                   "runs/q35_2b_main.json": "2B paused; add its train file to V14_KEEP when it resumes"}
    runs = sorted((ROOT / "runs").glob("*.json"))
    assert runs and "runs/q35_4b_c_r1.json" in {f"runs/{p.name}" for p in runs}  # the C config is checked here
    for p in runs:
        cfg = json.loads(p.read_text())
        files = {cfg[k] for k in ("train_file", "rel_file") if cfg.get(k)}
        if f"runs/{p.name}" in not_default:
            if all(not modal_od._data_ignore(Path(f)) for f in files):
                continue  # the file was allow-listed since; nothing to refuse
            with pytest.raises(SystemExit, match="not uploaded"):
                modal_od._launch_checks(f"runs/{p.name}", {k: cfg[k] for k in ("train_file", "rel_file")})
            continue
        wanted |= files
    for name, script in modal_od.SPAWN_LAUNCHED.items():  # the spawn script exists and uploads that run's files
        cfg, src = json.loads((ROOT / name).read_text()), (ROOT / script).read_text()
        assert all(Path(cfg[k]).name in src for k in ("train_file", "rel_file")), name
    for f in sorted(wanted):
        assert not modal_od._data_ignore(Path(f)), f
    for f in ("v14_label_shards", "v14_label_shards/shard_000.jsonl", "v14_label_shards/shards.json",
              "v14_label_shards/labels_q35_4b_pxE/shard_000.jsonl", "x_label_shards/shard_001.meta.json",
              "v14_parts/raw/gd_x.jsonl", "v14_parts/golden_train_pregap.jsonl", "v13_parts/golden_train.jsonl",
              "c_parts/c_mix_report.json", "c_parts/f7/rows.jsonl", "c_parts/c_train_r1_pre_lint.jsonl",
              "c_replay_r1_shards/shard_000.jsonl", "c_old_slice_shards/labels_q35_4b_main500k/shard_000.jsonl",
              "ohs3_parts/x.jsonl", "ohs3_x.jsonl"):
        assert modal_od._data_ignore(Path(f)), f
    for d in ("v14_parts", "c_parts", ""):
        assert not modal_od._data_ignore(Path(d)), d


def test_launch_checks_refuse_fill_and_unmounted_files():
    ok = {"train_file": "c_parts/c_train_r1.jsonl", "rel_file": "c_parts/c_rel_r1.jsonl", "epochs": 0.97}
    modal_od._launch_checks("runs/x.json", ok)
    with pytest.raises(SystemExit, match="FILL"):
        modal_od._launch_checks("runs/x.json", {**ok, "epochs": "FILL_FROM_dry_run"})
    with pytest.raises(SystemExit, match="PARTS_KEEP"):
        modal_od._launch_checks("runs/x.json", {**ok, "train_file": "c_parts/c_train_r3.jsonl"})
    with pytest.raises(SystemExit, match="fix2_spawn"):
        modal_od._launch_checks("runs/q35_4b_fix2.json", {"train_file": "v14_parts/fix2_train.jsonl"})
    with pytest.raises(SystemExit, match="FILL"):  # the C draft cannot launch until the build fills it
        modal_od._launch_checks("runs/q35_4b_c_r1.json", json.loads((ROOT / "runs/q35_4b_c_r1.json").read_text()))


def test_compare_relay_check_mode_and_trend(tmp_path, capsys):
    runs = _runs(tmp_path)
    assert cr.verdict(runs)["a1_loss_trend"][0] > cr.verdict(runs)["a1_loss_trend"][1]
    assert cr.main(["--check", str(tmp_path / "A1"), "--step", "300", "--expect-last-batch", "h300"]) == 0
    assert capsys.readouterr().out.strip().endswith("OK")
    assert cr.check_ckpt(str(tmp_path / "A1"), 150) and cr.check_ckpt(str(tmp_path / "A1"), 300, "other")
    (tmp_path / "A2/state.pt").write_bytes((tmp_path / "A2/state.pt").read_bytes() + b"x")
    assert any("missing or changed" in p for p in cr.check_ckpt(str(tmp_path / "A2"), 300))
    with pytest.raises(SystemExit):
        cr.main(["--a1", str(tmp_path / "A1")])


def test_smoke_f2_ride_along_record_and_compare(tmp_path, monkeypatch):
    """The Modal smoke's F2 record (recipe v4 pre-flight 9) is written next to the smoke result and compared with the
    reference record from another machine (e.g. the L4 gate VM)."""
    from test_ordinal_a4 import Q35_TMPL, TemplTok, _f2_rec
    monkeypatch.setattr(modal_od, "HERE", tmp_path)
    rec = _f2_rec("modal-image35")
    (tmp_path / "f2_l4.json").write_text(json.dumps({**rec, "where": "l4-gate"}))
    out = tmp_path / "logs"
    out.mkdir()
    v = modal_od._f2_check({"ok": True, "f2": rec}, "smoke_heavy_h100_mt8192", "f2_l4.json", out)
    assert v["f2_cross"] == "pass" and json.loads((out / "f2_smoke_heavy_h100_mt8192.json").read_text()) == rec
    other = {**rec, "sha": {**rec["sha"], rec["views"][1]: "f" * 64}}
    assert modal_od._f2_check({"f2": other}, "t2", "f2_l4.json", out)["f2"] == "FAIL"
    assert modal_od._f2_check({"f2": {"error": "OSError: x"}}, "t3", "f2_l4.json", out)["f2"] == "ERROR"
    assert modal_od._f2_check({"f2": rec}, "t4", "", out)["f2"].startswith("recorded")
    assert modal_od._f2_check({"ok": True}, "t5", "f2_l4.json", out) is None
    # inside the container: the training path of a config (no adapter); an error is returned, never raised
    monkeypatch.setattr(td, "train_prompt_path", lambda cfg: {"tok": TemplTok("Qwen/Qwen3.5-4B", Q35_TMPL),
                                                             "layout": cfg["layout"], "style": cfg["style"], "src": "x"})
    here = modal_od._f2_here({"base": "Qwen/Qwen3.5-4B", "layout": "schema_branch_mark", "style": "cygnet"}, "", "m")
    assert here["sha"] == rec["sha"] and set(here["paths"]) == {"train"}
    assert "error" in modal_od._f2_here({}, "", "m")
