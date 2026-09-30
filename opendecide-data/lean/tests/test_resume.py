"""Relay safety: a run stopped, copied to another machine/account and resumed must end bit-identical to a straight run
(on CPU, where the maths is deterministic), and every kind of mismatch must stop loudly instead of starting over."""
from __future__ import annotations

import json
import os
import shutil
import signal
import sys
from pathlib import Path

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import train_decoder as td  # noqa: E402
from test_train_loss import _write_data, fake_cand_logits, fake_env  # noqa: E402,F401

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")  # torch.autocast("cuda") on a CPU-only box

CFG = {"base": "fake", "grad_ckpt": False, "batch": 8, "epochs": 2.0, "beta": 0.1, "log_every": 1,
       "train_file": "train.jsonl", "rel_file": "rels.jsonl", "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.5,
       "ckpt_every_min": 0}


@pytest.fixture
def noisy(monkeypatch):
    """The fake forward also draws from the torch RNG (like LoRA dropout), so a wrong RNG restore shows up."""
    state = {"calls": 0, "kill_at": None}

    def cand(model, ro, rows, dev, perms=None):
        out = fake_cand_logits(model, ro, rows, dev, perms)
        if torch.is_grad_enabled():
            state["calls"] += 1
            if state["kill_at"] is not None and state["calls"] == state["kill_at"]:
                os.kill(os.getpid(), signal.SIGINT)  # like a Modal preemption, mid-step
            out = [z + 0.05 * torch.randn(z.shape) for z in out]
        return out
    monkeypatch.setattr(td, "cand_logits", cand)
    return state


def _params(res):
    return {n: p.detach().clone() for n, p in res["model"].named_parameters()}


def _log(res):
    return [{k: v for k, v in r.items() if k != "min"} for r in res["meta"]["log"]]


def _straight(tmp_path):
    _write_data(tmp_path)
    return td.train(dict(CFG), tmp_path, tmp_path / "straight", dev="cpu")


def test_relay_is_bit_identical_to_a_straight_run(fake_env, noisy, tmp_path):
    ref = _straight(tmp_path)
    n = ref["meta"]["steps"]
    r1 = td.train({**CFG, "stop_at_step": 11}, tmp_path, tmp_path / "acct1", dev="cpu")
    assert r1["stopped"] and r1["next_step"] == 11 and r1["n_steps"] == n
    ck = tmp_path / "acct1" / "_ckpt"
    assert json.loads((ck / "manifest.json").read_text())["step"] == 11
    shutil.copytree(ck, tmp_path / "acct2" / "_ckpt")  # the account switch
    r2 = td.train({**CFG, "expect_resume": True, "stop_at_step": 23}, tmp_path, tmp_path / "acct2", dev="cpu")
    assert r2["stopped"] and r2["next_step"] == 23
    shutil.copytree(tmp_path / "acct2" / "_ckpt", tmp_path / "acct3" / "_ckpt")
    r3 = td.train({**CFG, "expect_resume": True}, tmp_path, tmp_path / "acct3", dev="cpu")
    a, b = _params(ref), _params(r3)
    assert a.keys() == b.keys() and all(torch.equal(a[k], b[k]) for k in a)
    assert _log(ref) == _log(r3)  # every step: the same losses, counts and learning rate
    assert not (tmp_path / "acct3" / "_ckpt").exists() and (tmp_path / "acct3" / "train_meta.json").exists()


def test_preemption_signal_saves_and_resumes_exactly(fake_env, noisy, tmp_path):
    ref = _straight(tmp_path)
    noisy["calls"], noisy["kill_at"] = 0, 7
    with pytest.raises(KeyboardInterrupt):
        td.train(dict(CFG), tmp_path, tmp_path / "run", dev="cpu")
    st = torch.load(tmp_path / "run" / "_ckpt" / "state.pt", weights_only=False)
    assert st["step"] == 7  # the interrupted step finished, then the checkpoint
    assert signal.getsignal(signal.SIGINT) is signal.default_int_handler  # handler restored
    noisy["kill_at"] = None
    res = td.train(dict(CFG), tmp_path, tmp_path / "run", dev="cpu")
    a, b = _params(ref), _params(res)
    assert all(torch.equal(a[k], b[k]) for k in a) and _log(ref) == _log(res)


def _stopped(tmp_path, at=5):
    _write_data(tmp_path)
    td.train({**CFG, "stop_at_step": at}, tmp_path, tmp_path / "run", dev="cpu")
    return tmp_path / "run" / "_ckpt"


def test_config_change_raises_instead_of_starting_over(fake_env, noisy, tmp_path):
    ck = _stopped(tmp_path)
    with pytest.raises(RuntimeError, match="different run"):
        td.train({**CFG, "lr": 2e-4}, tmp_path, tmp_path / "run", dev="cpu")
    assert (ck / "state.pt").exists()  # the checkpoint is kept
    res = td.train({**CFG, "lr": 2e-4, "fresh_start": True}, tmp_path, tmp_path / "run", dev="cpu")
    assert res["meta"]["log"][0]["step"] == 0


def test_data_change_raises(fake_env, noisy, tmp_path):
    _stopped(tmp_path)
    f = tmp_path / "train.jsonl"
    rows = [json.loads(l) for l in f.read_text().splitlines()]
    rows[0]["gold"] = 1 - rows[0]["gold"]  # same ids, one label changed
    f.write_text("".join(json.dumps(r) + "\n" for r in rows))
    with pytest.raises(RuntimeError, match="different run"):
        td.train(dict(CFG), tmp_path, tmp_path / "run", dev="cpu")


def test_code_and_env_changes_raise(fake_env, noisy, tmp_path, monkeypatch):
    _stopped(tmp_path)
    real_code, real_env = td._code, td._env
    monkeypatch.setattr(td, "_code", lambda: {**real_code(), "train_decoder": "edited"})
    with pytest.raises(RuntimeError, match="code differs"):
        td.train(dict(CFG), tmp_path, tmp_path / "run", dev="cpu")
    monkeypatch.setattr(td, "_code", real_code)
    monkeypatch.setattr(td, "_env", lambda: {**real_env(), "peft": "0.21.1"})
    with pytest.raises(RuntimeError, match="software/GPU differs"):
        td.train(dict(CFG), tmp_path, tmp_path / "run", dev="cpu")


def test_expect_resume_without_checkpoint_raises(fake_env, noisy, tmp_path):
    _write_data(tmp_path)
    with pytest.raises(RuntimeError, match="expect_resume"):
        td.train({**CFG, "expect_resume": True}, tmp_path, tmp_path / "wrong_name", dev="cpu")


def test_corrupted_copy_raises(fake_env, noisy, tmp_path):
    ck = _stopped(tmp_path)
    p = ck / "trainable.safetensors"
    b = bytearray(p.read_bytes())
    b[-1] ^= 1
    p.write_bytes(bytes(b))
    with pytest.raises(RuntimeError, match="missing or changed"):
        td.train(dict(CFG), tmp_path, tmp_path / "run", dev="cpu")


def test_leftover_old_checkpoint_is_cleaned(fake_env, noisy, tmp_path):
    ref = _straight(tmp_path)
    ck = _stopped(tmp_path, at=9)
    shutil.copytree(ck, ck.with_name("_ckpt.old"))  # a stop between the swap and the clean-up
    res = td.train(dict(CFG), tmp_path, tmp_path / "run", dev="cpu")
    assert not ck.with_name("_ckpt.old").exists()
    a, b = _params(ref), _params(res)
    assert all(torch.equal(a[k], b[k]) for k in a)


def test_no_overwrite_protects_a_finished_model(fake_env, noisy, tmp_path):
    _write_data(tmp_path)
    td.train({**CFG, "no_overwrite": True}, tmp_path, tmp_path / "run", dev="cpu")
    with pytest.raises(RuntimeError, match="finished model"):
        td.train({**CFG, "no_overwrite": True}, tmp_path, tmp_path / "run", dev="cpu")


def test_absolute_deadline_stops_and_resumes_exactly(fake_env, noisy, tmp_path):
    ref = _straight(tmp_path)
    r1 = td.train({**CFG, "stop_at_unix": 1.0}, tmp_path, tmp_path / "run", dev="cpu")  # a deadline long past
    assert r1["stopped"] and r1["next_step"] == 1
    r2 = td.train({**CFG, "expect_resume": True}, tmp_path, tmp_path / "run", dev="cpu")
    a, b = _params(ref), _params(r2)
    assert all(torch.equal(a[k], b[k]) for k in a) and _log(ref) == _log(r2)


def test_final_cleanup_is_all_or_nothing(fake_env, noisy, tmp_path):
    ck = _stopped(tmp_path, at=9)
    shutil.copytree(ck, ck.with_name("_ckpt.done"))  # a stop during a previous final clean-up
    td.train(dict(CFG), tmp_path, tmp_path / "run", dev="cpu")
    assert not ck.exists() and not ck.with_name("_ckpt.done").exists()
    assert (tmp_path / "run" / "train_meta.json").exists()


def test_kd_skip_src_drops_only_the_named_teacher(fake_env, noisy, tmp_path):
    _write_data(tmp_path)
    f = tmp_path / "train.jsonl"
    rows = [json.loads(l) for l in f.read_text().splitlines()]
    for i, r in enumerate(rows[:10]):
        t = {"yes": 0.7} if r["qtype"] == "noul" else {o: 1 / len(r["options"]) for o in r["options"]}
        r["meta"] = {**(r.get("meta") or {}), "teacher": t, **({"teacher_src": "blend50"} if i % 2 else {})}
    f.write_text("".join(json.dumps(r) + "\n" for r in rows))
    res = td.train({**CFG, "kd": 0.5, "kd_skip_src": ["blend50"], "epochs": 0.2}, tmp_path, tmp_path / "run", dev="cpu")
    assert res["meta"]["steps"] > 0
    kept = [r for r in td.read_jsonl(f) if isinstance((r.get("meta") or {}).get("teacher"), dict)]
    assert len(kept) == 10  # the file itself is untouched
