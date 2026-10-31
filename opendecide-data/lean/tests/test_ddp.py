"""DDP (PREREG_FINAL A20 c, c_build/ddp/train_ddp.py): the pinned trainer is untouched, the DDP hunks apply, the rank
split keeps units whole and covers the batch, and 1 or 2 gloo ranks train like one process (fake model, CPU). The full
adoption test (tiny real model, real prompts, resume) is c_build/ddp/adoption_cpu.py."""
from __future__ import annotations

import hashlib
import random
import sys
import types
from pathlib import Path

import pytest
import torch

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(LEAN / "c_build/ddp"))
import decoder_io  # noqa: E402
import train_ddp  # noqa: E402
import train_decoder as td  # noqa: E402
from test_train_loss import FakeModel, FakeTok, _write_data, fake_cand_logits, fake_env  # noqa: E402,F401

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")
CFG = {"base": "fake", "grad_ckpt": False, "batch": 8, "epochs": 2.0, "beta": 0.1, "log_every": 1,
       "train_file": "train.jsonl", "rel_file": "rels.jsonl", "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.5,
       "aux_norm": "batch", "micro_tokens": 1024, "ckpt_every_min": 0}


def test_pinned_trainer_untouched_and_hunks_apply():
    assert hashlib.sha256(Path(td.__file__).read_bytes()).hexdigest() == train_ddp.PINNED_TRAINER_SHA
    src, first, new = train_ddp.patched_source()
    assert src != new and first > 1
    fn = train_ddp._built()
    assert fn.__globals__ is vars(td)  # every helper it calls is the pinned module's
    assert td.train.__code__.co_filename == td.__file__  # the default path is the pinned function itself
    assert "ddp" not in td.train.__code__.co_varnames and "_dx" not in td.train.__code__.co_varnames


def _units(n=40, seed=3):
    rng = random.Random(seed)
    batch, uid = [], {}
    for u in range(n):
        for j in range(rng.randint(1, 3)):
            r = {"id": f"u{u}_{j}", "state": "x" * rng.choice([10, 500, 4000]), "options": ["a", "b"], "qtype": "choice"}
            batch.append(r)
            uid[r["id"]] = u
    return batch, uid


@pytest.mark.parametrize("world", [1, 2, 3, 4, 8])
def test_rank_split_whole_units_disjoint_cover(world):
    batch, uid = _units()
    tw = [(i, None) for i in range(0, len(batch), 3)]
    sh = train_ddp.rank_split(batch, uid, tw, world)
    assert sh == train_ddp.rank_split(batch, uid, tw, world)  # deterministic: every rank computes the same split
    flat = [i for s in sh for i in s]
    assert sorted(flat) == list(range(len(batch)))
    for a in range(world):
        for b in range(a + 1, world):
            assert not ({uid[batch[i]["id"]] for i in sh[a]} & {uid[batch[i]["id"]] for i in sh[b]})
    if world > 1:  # greedy balance: no rank above mean + the heaviest unit
        cost = lambda s: sum((1 + sum(1 for j, _ in tw if j == i)) * td._est_tokens(batch[i]) for i in s)  # noqa: E731
        loads = [cost(s) for s in sh]
        assert max(loads) <= sum(loads) / world + max(cost([i for i in range(len(batch)) if uid[batch[i]["id"]] == u])
                                                      for u in set(uid.values()))
    if world == 1:  # one rank: exactly the one-process micro-batches
        d = types.SimpleNamespace(rank=0, world=1)
        assert train_ddp.rank_groups(batch, uid, tw, 4096, d) == td._micro_groups(batch, uid, tw, 4096)


def test_ddp_needs_batch_norm(fake_env, tmp_path, monkeypatch):
    _write_data(tmp_path)
    monkeypatch.setattr(train_ddp, "Dist", lambda: (_ for _ in ()).throw(AssertionError("not reached")))
    with pytest.raises(ValueError, match="aux_norm"):
        train_ddp.train({**CFG, "aux_norm": "micro"}, tmp_path, tmp_path / "x", dev="cpu")


def child_fakes(rank):
    """fake_env's patches, in a spawned rank."""
    fake_peft = types.ModuleType("peft")
    fake_peft.LoraConfig = lambda **kw: kw
    fake_peft.get_peft_model = lambda model, cfg: model
    sys.modules["peft"] = fake_peft
    td.load = lambda base, dev: (FakeModel(), FakeTok())
    td.Readout = lambda tok: None
    td.cand_logits = fake_cand_logits
    decoder_io.STYLE = "cygnet"


def _log(meta):
    return [{k: v for k, v in r.items() if k != "min"} for r in meta["log"]]


@pytest.mark.parametrize("world", [1, 2])
def test_gloo_ranks_train_like_one_process(fake_env, tmp_path, world):
    _write_data(tmp_path)
    one = td.train(dict(CFG), tmp_path, tmp_path / "one", dev="cpu")
    two = train_ddp.launch_ddp(dict(CFG), tmp_path, tmp_path / "two", world, dev="cpu", style="cygnet",
                               logdir=tmp_path / "logs", setup=(child_fakes, ()))
    a = {k: v.detach() for k, v in one["model"].state_dict().items()}
    b = torch.load(tmp_path / "two" / "fake.pt")
    assert a.keys() == b.keys()
    for k in a:
        if world == 1:  # one rank: the same arithmetic as one process, bit for bit
            assert torch.equal(a[k], b[k]), k
        else:
            assert torch.allclose(a[k], b[k], rtol=1e-5, atol=1e-7), k
    la, lb = _log(one["meta"]), _log(two["meta"])
    assert [r["step"] for r in la] == [r["step"] for r in lb]
    if world == 1:
        assert la == lb
    for x, y in zip(la, lb):  # same data order and counts; terms equal to the 4 logged decimals (or 1e-4)
        assert {k: x[k] for k in ("n_cons", "n_inv", "n_twin", "n_rel_skipped", "lr")} == \
               {k: y[k] for k in ("n_cons", "n_inv", "n_twin", "n_rel_skipped", "lr")}
        for k in td.TERMS + ("gn",):
            assert (x[k] is None) == (y[k] is None) and (x[k] is None or abs(x[k] - y[k]) <= 1e-4), (x["step"], k)
    assert two["meta"]["ddp"] == {"world_size": world, "code": train_ddp.CODE_SHA}
    assert (tmp_path / "two" / "train_meta.json").exists()
