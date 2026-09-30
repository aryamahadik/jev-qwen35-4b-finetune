"""FINETUNE_PLAN.md changes C1-C5: packing-invariant loss (aux_norm "batch"), startup checks, the NaN-gradient guard and
monitor, snapshots, exact-probability rows."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parent))
import train_decoder as td  # noqa: E402
from test_train_loss import FakeModel, FakeTok, _write_data, fake_env, noul  # noqa: E402,F401

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")

CFG = {"base": "fake", "grad_ckpt": False, "batch": 8, "epochs": 1.0, "beta": 0.1, "log_every": 1,
       "train_file": "train.jsonl", "rel_file": "rels.jsonl", "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.5,
       "ckpt_every_min": 0}


def _params(res):
    return {n: p.detach().clone() for n, p in res["model"].named_parameters()}


def _close(a, b, atol=1e-5):
    return all(torch.allclose(a[k], b[k], atol=atol) for k in a)


def test_aux_norm_batch_is_packing_invariant(fake_env, tmp_path, monkeypatch, capsys):
    _write_data(tmp_path)
    n_groups = []
    real = td._micro_groups
    monkeypatch.setattr(td, "_micro_groups", lambda *a: n_groups.append(len(g := real(*a))) or g)
    whole = td.train({**CFG, "aux_norm": "batch"}, tmp_path, tmp_path / "w", dev="cpu")
    packed = td.train({**CFG, "aux_norm": "batch", "micro_tokens": 512}, tmp_path, tmp_path / "p", dev="cpu")
    assert max(n_groups) > 1  # the batch really was split
    assert _close(_params(whole), _params(packed))  # same objective, only float order differs
    assert "spans micro-batches" not in capsys.readouterr().out
    micro = td.train({**CFG, "micro_tokens": 512}, tmp_path, tmp_path / "m", dev="cpu")
    assert not _close(_params(whole), _params(micro))  # today's path weights aux terms by micro-batch share


def test_aux_norm_batch_equals_micro_without_packing(fake_env, tmp_path):
    _write_data(tmp_path)
    a = td.train({**CFG, "aux_norm": "batch"}, tmp_path, tmp_path / "a", dev="cpu")
    b = td.train(dict(CFG), tmp_path, tmp_path / "b", dev="cpu")
    assert _close(_params(a), _params(b), atol=1e-6)


def test_aux_counts_match_compute_loss(fake_env, tmp_path):
    _write_data(tmp_path)
    rows = td.read_jsonl(tmp_path / "train.jsonl")
    rels = td.read_jsonl(tmp_path / "rels.jsonl")
    by = {}
    for x in rels:
        by.setdefault(x["a"], []).append(x)
    c = {**CFG, "recipe": "A3", "lam": 1.0, "lam_p": 0.5}
    batch = rows[:30]
    perms = [list(range(len(r["options"]))) if r["qtype"] == "choice" else [0, 1] for r in batch]
    lg = [torch.randn(len(p)) for p in perms]
    _, _, counts = td.compute_loss(c, batch, perms, lg, by, 5, 10, "cpu", cyg=True)
    n = td.aux_counts(c, batch, by)
    assert (n["cons"], n["inv"]) == (counts["cons"], counts["inv"]) and n["cons"] > 0 and n["inv"] > 0


@pytest.mark.parametrize("extra,match", [({"lr_typo": 1}, "unknown config key"), ({"expect_trainable": 7}, "expect_trainable"),
                                         ({"expect_kd_targets": 3}, "expect_kd_targets"), ({"aux_norm": "x"}, "aux_norm"),
                                         ({"style": "od"}, "STYLE")])
def test_startup_checks_raise(fake_env, tmp_path, extra, match):
    _write_data(tmp_path)
    with pytest.raises(ValueError, match=match):
        td.train({**CFG, **extra}, tmp_path, tmp_path / "x", dev="cpu")


def test_bf16_trainable_params_are_refused(fake_env, tmp_path, monkeypatch):
    _write_data(tmp_path)

    def load(base, dev):
        m = FakeModel()
        m.head = torch.nn.Parameter(m.head.detach().bfloat16())
        return m, FakeTok()
    monkeypatch.setattr(td, "load", load)
    with pytest.raises(ValueError, match="float32"):
        td.train(dict(CFG), tmp_path, tmp_path / "x", dev="cpu")


def test_trainable_count_passes_when_right(fake_env, tmp_path):
    _write_data(tmp_path)
    n = sum(p.numel() for p in FakeModel().parameters())
    td.train({**CFG, "expect_trainable": n, "epochs": 0.2}, tmp_path, tmp_path / "x", dev="cpu")


def test_nan_gradient_stops_before_the_update(fake_env, tmp_path, monkeypatch):
    _write_data(tmp_path)
    monkeypatch.setattr(td.torch.nn.utils, "clip_grad_norm_", lambda *a, **k: torch.tensor(float("nan")))
    with pytest.raises(FloatingPointError, match="non-finite gradient norm"):
        td.train(dict(CFG), tmp_path, tmp_path / "x", dev="cpu")


def test_monitor_logs_and_good_copy(fake_env, tmp_path, monkeypatch):
    _write_data(tmp_path)
    monkeypatch.setattr(td, "GOOD_EVERY", 4)
    res = td.train({**CFG, "stop_at_step": 9, "ckpt_every_min": 1e-9}, tmp_path, tmp_path / "x", dev="cpu")
    assert res["stopped"]
    rec = res["meta"]["log"][-1]
    assert {"gn", "gn_med", "clip_frac"} <= set(rec) and rec["gn"] > 0
    assert (tmp_path / "x" / "_ckpt_good" / "state.pt").exists()


def test_snapshots_fire_at_the_planned_steps_and_change_nothing(fake_env, tmp_path):
    _write_data(tmp_path)
    ref = td.train(dict(CFG), tmp_path, tmp_path / "ref", dev="cpu")
    n = ref["meta"]["steps"]
    res = td.train({**CFG, "snap_every": 5, "snap_fracs": [0.5]}, tmp_path, tmp_path / "s", dev="cpu")
    want = {f"s{k:06d}" for k in set(range(5, n, 5)) | {int(0.5 * n)}}
    got = {p.name for p in (tmp_path / "s" / "snaps").iterdir() if not p.name.startswith(".")}
    assert got == want
    meta = json.loads((tmp_path / "s" / "snaps" / "s000005" / "train_meta.json").read_text())
    assert meta["snapshot_step"] == 5 and meta["cfg"]["train_file"] == "train.jsonl"
    a, b = _params(ref), _params(res)
    assert all(torch.equal(a[k], b[k]) for k in a)


def test_kd_full_src_uses_the_exact_probability():
    c = {"kd": 0.5, "label_smooth": 0.05, "recipe": "A3", "lam": 1.0, "kd_full_src": ["gd_gen2_probability"]}
    lg = [torch.tensor([0.3, -0.2])]
    lp = F.log_softmax(lg[0], -1)
    listed = noul("a", "c", 1, source="gd_gen2_probability", meta={"teacher": {"yes": 0.3}})
    loss, _, _ = td.compute_loss(c, [listed], [[0, 1]], lg, {}, 1, 10, "cpu", cyg=True)
    assert torch.allclose(loss, -(0.3 * lp[0] + 0.7 * lp[1]))
    other = noul("b", "c", 1, source="boolq", meta={"teacher": {"yes": 0.3}})
    loss2, _, _ = td.compute_loss(c, [other], [[0, 1]], lg, {}, 1, 10, "cpu", cyg=True)
    y = 0.5 * (1 * 0.9 + 0.05) + 0.5 * 0.3
    assert torch.allclose(loss2, -(y * lp[0] + (1 - y) * lp[1]))


def test_good_copy_freezes_after_an_alert(fake_env, tmp_path, monkeypatch, capsys):
    _write_data(tmp_path)
    monkeypatch.setattr(td, "GOOD_EVERY", 2)
    monkeypatch.setattr(td, "GOOD_QUIET", 1)
    monkeypatch.setattr(td.statistics, "median", lambda xs: 1.0)  # so a gn of 1000 counts as a spike every step
    copied = []
    real_copy = td._copy_good
    monkeypatch.setattr(td, "_copy_good", lambda ck, oc=None: copied.append(
        torch.load(ck / "state.pt", weights_only=False)["step"]) or real_copy(ck, oc))
    real_clip = td.torch.nn.utils.clip_grad_norm_
    calls = {"n": 0}

    def clip(params, mx):
        calls["n"] += 1
        g = real_clip(params, mx)
        return torch.tensor(1000.0) if calls["n"] > 10 else g  # steps 10+ spike; the ALERT fires at step 29
    monkeypatch.setattr(td.torch.nn.utils, "clip_grad_norm_", clip)
    td.train({**CFG, "epochs": 4.0, "ckpt_every_min": 1e-9, "stop_at_step": 50}, tmp_path, tmp_path / "x", dev="cpu")
    alerts = [json.loads(l)["step"] for l in capsys.readouterr().out.splitlines() if l.startswith('{"ALERT"')]
    assert alerts and copied and max(copied) <= alerts[0] + 1  # nothing copied after the first alert
    good = torch.load(tmp_path / "x" / "_ckpt_good" / "state.pt", weights_only=False)
    assert good["step"] == max(copied) <= alerts[0] + 1


def test_stale_snapshots_are_moved_aside_on_rollback(fake_env, tmp_path):
    _write_data(tmp_path)
    td.train({**CFG, "stop_at_step": 12, "snap_every": 5}, tmp_path, tmp_path / "x", dev="cpu")
    snaps = tmp_path / "x" / "snaps"
    (snaps / "s000020").mkdir()  # as if a later, abandoned run had written it
    td.train({**CFG, "snap_every": 5, "epochs": 1.0}, tmp_path, tmp_path / "x", dev="cpu")
    aside = [q for q in snaps.iterdir() if q.name.startswith("_abandoned_from_000012")]
    assert aside and (aside[0] / "s000020").exists()


def test_checkpoint_adapter_is_loadable_on_its_own(fake_env, tmp_path):
    _write_data(tmp_path)
    td.train({**CFG, "stop_at_step": 4}, tmp_path, tmp_path / "x", dev="cpu")
    snap = json.loads((tmp_path / "x" / "_ckpt" / "adapter" / "snap.json").read_text())
    assert snap["step"] == 4 and snap["cfg"]["train_file"] == "train.jsonl"
    man = json.loads((tmp_path / "x" / "_ckpt" / "manifest.json").read_text())
    assert "adapter/snap.json" in man["files"]


def test_fresh_start_passes_an_old_format_checkpoint(fake_env, tmp_path):
    _write_data(tmp_path)
    ck = tmp_path / "x" / "_ckpt"
    ck.mkdir(parents=True)
    torch.save({"step": 3, "fingerprint": "old-code"}, ck / "state.pt")  # no manifest (saved by older code)
    with pytest.raises(RuntimeError, match="different run"):
        td.train(dict(CFG), tmp_path, tmp_path / "x", dev="cpu")
    res = td.train({**CFG, "fresh_start": True}, tmp_path, tmp_path / "x", dev="cpu")
    assert res["meta"]["log"][0]["step"] == 0
