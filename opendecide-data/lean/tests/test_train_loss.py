"""CPU tests for the v0.11 loss terms in train_decoder.py (synthetic logits, no model download, no GPU).

Run:  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -m pytest -q tests/test_train_loss.py
"""
from __future__ import annotations

import contextlib
import json
import math
import random
import sys
import types
import zlib
from collections import defaultdict
from pathlib import Path

import pytest
import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import decoder_io  # noqa: E402
import train_decoder as td  # noqa: E402

DEV = "cpu"


# ---------------------------------------------------------------- frozen copy of the v0.10 loss (train_decoder.py @ 91b32a9)

def old_loss(c, batch, perms, lg, rel_by_row, step, n_steps, dev, kl, cyg):
    """Verbatim body of the v0.10 training step's loss (lines 100-140), wrapped as a function."""
    EPS = {"mnli": 0.08}
    task, cons, pidx = [], [], {}
    for r, perm, l in zip(batch, perms, lg):
        teach = (r.get("meta") or {}).get("teacher") if c.get("kd", 0) > 0 else None  # distillation target
        if r["qtype"] == "noul":
            eps = EPS.get(r["source"], 0.05)
            y = r["gold"] * (1 - 2 * eps) + eps
            if teach:
                y = (1 - c["kd"]) * y + c["kd"] * float(teach["yes"])
            logp = F.log_softmax(l, -1)
            iy, in_ = (perm.index(0), perm.index(1)) if cyg else (0, 1)  # displayed letter of Yes / No
            task.append(-(y * logp[iy] + (1 - y) * logp[in_]))
            pidx[r["id"]] = logp[iy].exp()
        else:
            gp = (r.get("meta") or {}).get("gold_probs")
            if gp:  # exact probabilistic target (e.g. Bayes posterior): soft cross-entropy on the displayed order
                q = torch.tensor([float(gp.get(r["options"][i], 0.0)) for i in perm], device=dev)
                q = 0.97 * q / q.sum() + 0.03 / len(perm)
                task.append(-(q * F.log_softmax(l, -1)).sum())
            elif teach:  # soft target = (1 - kd) * smoothed gold + kd * teacher, in the displayed order
                gi = perm.index(r["options"].index(r["gold"]))
                q = torch.full((len(perm),), 0.05 / len(perm), device=dev)
                q[gi] += 0.95
                tq = torch.tensor([float(teach.get(r["options"][i], 0.0)) for i in perm], device=dev)
                q = (1 - c["kd"]) * q + c["kd"] * tq / tq.sum().clamp_min(1e-9)
                task.append(-(q * F.log_softmax(l, -1)).sum())
            else:
                gi = perm.index(r["options"].index(r["gold"]))
                task.append(F.cross_entropy(l.unsqueeze(0), torch.tensor([gi], device=dev), label_smoothing=0.05))
    loss_task = torch.stack(task).mean()
    loss = loss_task
    if c["recipe"] != "A0":
        for r in batch:
            for x in rel_by_row.get(r["id"], []):
                if x["a"] in pidx and x["b"] in pidx:
                    pa, pb = pidx[x["a"]], pidx[x["b"]]
                    cons.append((pa + pb - 1) ** 2 if x["type"] == "complement" else (pa - pb) ** 2)
        if cons:
            ramp = min(1.0, step / max(1, 0.2 * n_steps))
            loss = loss + c["lam"] * ramp * torch.stack(cons).mean()
    if kl is not None:
        loss = loss + c["beta"] * kl
    return loss


# ---------------------------------------------------------------- synthetic rows

def noul(rid, call, gold=1, source="boolq", meta=None, role="aff"):
    return {"id": rid, "group_id": "g_" + call, "call_id": call, "split": "train", "track": "L1", "source": source,
            "state": "text", "qtype": "noul", "instructions": "Is it so?", "options": None, "gold": gold, "role": role,
            "meta": meta or {}}


def choice(rid, call, options, gold, meta=None, source="clinc150"):
    return {"id": rid, "group_id": "g_" + call, "call_id": call, "split": "train", "track": "L0", "source": source,
            "state": "text", "qtype": "choice", "instructions": "Which one?", "options": list(options), "gold": gold,
            "role": "choice", "meta": meta or {}}


def opts(n, tag="o"):
    return [f"{tag}{i}" for i in range(n)]


def rel(t, a, b):
    return {"type": t, "a": a, "b": b, "track": "train"}


def by_row(rels):
    d = defaultdict(list)
    for x in rels:
        d[x["a"]].append(x)
    return d


def perm_for(r, rng, cyg):
    if r["qtype"] == "choice":
        return rng.sample(range(len(r["options"])), len(r["options"]))
    return rng.sample([0, 1], 2) if cyg else None


def displayed(z, perm):
    """Candidate logits in displayed order when canonical option i has logit z[i]: position j shows option perm[j]."""
    return z if perm is None else z[torch.tensor(perm)]


def mixed_batch():
    """Every row kind the v0.10 loss handles, plus relations of every type (incl. partners outside the batch)."""
    o4, o30 = opts(4), opts(30, "w")
    rows = [
        noul("n1", "c1", 1, source="mnli"), noul("n2", "c1", 0, role="neg"), noul("n3", "c1", 1, role="para"),
        noul("n4", "c1", 1, role="inj"), noul("n5", "c2", 0, meta={"teacher": {"yes": 0.7}}),
        noul("n6", "c3", 1, meta={"anchor": True}),
        choice("k1", "c4", o4, "o2"), choice("k1x", "c4", o4, "o2"), choice("k1p", "c4", o4[::-1], "o2"),
        choice("k2", "c5", o4, "o1", meta={"gold_probs": {"o0": 0.1, "o1": 0.6, "o3": 0.3}}),
        choice("k3", "c6", o4, "o3", meta={"teacher": {"o0": 0.2, "o3": 0.8}}),
        choice("k4", "c7", o30, "w17"),
    ]
    rels = [rel("complement", "n1", "n2"), rel("equiv", "n1", "n3"), rel("inv", "n1", "n4"),
            rel("complement", "n5", "n_missing"), rel("equiv", "k1", "k1p"), rel("inv", "k1", "k1x"),
            rel("complement", "k1", "k2"), rel("equiv", "n6", "k4")]
    return rows, rels


def rand_logits(rows, perms, gen, scale=2.0):
    return [(torch.randn(2 if r["qtype"] == "noul" else len(r["options"]), generator=gen) * scale).requires_grad_(True)
            for r, p in zip(rows, perms)]


# ---------------------------------------------------------------- 1. inverse mapping

def test_inverse_perm_random():
    rng = random.Random(20261001)
    for _ in range(300):
        n = rng.choice([1, 2, 3, 5, 26, 27, 100, 255])
        p = rng.sample(range(n), n)
        inv = td.inverse_perm(p)
        assert [p[inv[i]] for i in range(n)] == list(range(n))
        assert [inv[p[j]] for j in range(n)] == list(range(n))
        assert inv == [p.index(i) for i in range(n)]


@pytest.mark.parametrize("cyg", [False, True])
def test_canon_logp_undoes_perm(cyg, monkeypatch):
    monkeypatch.setattr(decoder_io, "STYLE", "cygnet" if cyg else "od")
    rng, gen = random.Random(7), torch.Generator().manual_seed(7)
    for n in [2, 3, 9, 26, 40, 255]:
        r = choice("x", "c", opts(n), "o0")
        z = torch.randn(n, generator=gen) * 3
        for _ in range(5):
            p = rng.sample(range(n), n)
            got = td.canon_logp(r, displayed(z, p), p, cyg)
            assert torch.allclose(got, F.log_softmax(z, -1), atol=1e-6)
            # agrees with the inference readout (decoder_io.to_probs maps displayed probs back to option names)
            tp = decoder_io.to_probs(r, displayed(z, p), p)
            assert torch.allclose(got.exp(), torch.tensor([tp[o] for o in r["options"]]), atol=1e-6)
    r = noul("y", "c")
    z = torch.tensor([1.3, -0.4])  # canonical [yes, no]
    perms = [[0, 1], [1, 0]] if cyg else [None]
    for p in perms:
        got = td.canon_logp(r, displayed(z, p), p, cyg)
        assert torch.allclose(got, F.log_softmax(z, -1), atol=1e-6)
        assert math.isclose(got.exp()[0].item(), decoder_io.to_probs(r, displayed(z, p), p)["yes"], abs_tol=1e-6)
        if p is not None:  # same Yes letter the v0.10 task loss uses: perm.index(0)
            assert got[0].item() == pytest.approx(F.log_softmax(displayed(z, p), -1)[p.index(0)].item())


# ---------------------------------------------------------------- 2. defaults reproduce the v0.10 loss exactly

CFGS = [{"recipe": "A3", "lam": 0.5, "beta": 0.0},
        {"recipe": "A3", "lam": 0.5, "beta": 0.2, "kd": 0.3},
        {"recipe": "A0", "lam": 0.5, "beta": 0.0},
        {"recipe": "A3", "lam": 1.3, "beta": 0.1, "kd": 0.5}]


@pytest.mark.parametrize("cyg", [False, True])
@pytest.mark.parametrize("ci", range(len(CFGS)))
@pytest.mark.parametrize("explicit", [False, True])
def test_defaults_equal_old_loss(cyg, ci, explicit):
    rows, rels = mixed_batch()
    rbr = by_row(rels)
    c = dict(CFGS[ci])
    if explicit:
        c.update(td.LOSS_DEFAULTS)
    for seed in range(4):
        rng, gen = random.Random(seed), torch.Generator().manual_seed(seed)
        order = rows[:]
        rng.shuffle(order)
        perms = [perm_for(r, rng, cyg) for r in order]
        for step, n_steps in [(0, 100), (7, 100), (19, 100), (60, 100), (99, 100)]:
            lg_old = rand_logits(order, perms, gen)
            lg_new = [l.detach().clone().requires_grad_(True) for l in lg_old]
            kl_old = (lg_old[0] ** 2).sum() * 0.01 if c["beta"] > 0 else None
            kl_new = (lg_new[0] ** 2).sum() * 0.01 if c["beta"] > 0 else None
            lo = old_loss(c, order, perms, lg_old, rbr, step, n_steps, DEV, kl_old, cyg)
            ln, terms, counts = td.compute_loss(c, order, perms, lg_new, rbr, step, n_steps, DEV, kl=kl_new, cyg=cyg)
            assert torch.equal(lo.detach(), ln.detach()), (lo.item(), ln.item())
            lo.backward()
            ln.backward()
            for a, b in zip(lg_old, lg_new):
                assert torch.equal(a.grad, b.grad)
            assert terms["inv"] is None and terms["perm"] is None and counts["twin"] == 0
            if c["recipe"] != "A0":  # old behaviour for noul pairs: complement, equiv and (fallback) inv -> 3 terms
                assert counts["cons"] == 3


def test_defaults_ignore_new_keys_when_zero():
    """lam_inv=0 / sym_cons=False / perm_twin=0 set explicitly behave like the keys being absent."""
    rows, rels = mixed_batch()
    rbr, cyg = by_row(rels), True
    rng, gen = random.Random(3), torch.Generator().manual_seed(3)
    perms = [perm_for(r, rng, cyg) for r in rows]
    lg = rand_logits(rows, perms, gen)
    base = {"recipe": "A3", "lam": 0.5, "beta": 0.0}
    l1, _, _ = td.compute_loss(base, rows, perms, lg, rbr, 50, 100, DEV, cyg=cyg)
    l2, _, _ = td.compute_loss({**base, "lam_inv": 0.0, "sym_cons": False, "perm_twin": 0.0, "lam_p": 3.0},
                               rows, perms, lg, rbr, 50, 100, DEV, cyg=cyg)
    assert torch.equal(l1, l2)


# ---------------------------------------------------------------- 3. new terms: ~0 when identical, > 0 otherwise

def _pair_loss(c, ra, rb, za, zb, rels, cyg, seed=0, pa=None, pb=None):
    rng = random.Random(seed)
    pa = pa if pa is not None else perm_for(ra, rng, cyg)
    pb = pb if pb is not None else perm_for(rb, rng, cyg)
    la = displayed(za, pa).clone().requires_grad_(True)
    lb = displayed(zb, pb).clone().requires_grad_(True)
    loss, terms, counts = td.compute_loss(c, [ra, rb], [pa, pb], [la, lb], by_row(rels), 100, 100, DEV, cyg=cyg)
    return loss, terms, counts, la, lb


INV_C = {"recipe": "A3", "lam": 0.5, "beta": 0.0, "lam_inv": 1.0}


@pytest.mark.parametrize("cyg", [False, True])
def test_inv_noul(cyg):
    a, b = noul("a", "c1", 1), noul("b", "c1", 1, role="inj")
    rels = [rel("inv", "a", "b")]
    z = torch.tensor([0.9, -0.3])
    for pa, pb in ([[0, 1], [1, 0]], [[1, 0], [1, 0]]) if cyg else ([None, None],):
        _, t, n, _, _ = _pair_loss(INV_C, a, b, z, z.clone(), rels, cyg, pa=pa, pb=pb)
        assert n["inv"] == 1 and n["cons"] == 0 and t["inv"].item() == pytest.approx(0.0, abs=1e-7)
    _, t, _, la, lb = _pair_loss(INV_C, a, b, z, torch.tensor([-1.0, 0.5]), rels, cyg)
    assert t["inv"].item() > 1e-3
    lpa, lpb = F.log_softmax(z, -1), F.log_softmax(torch.tensor([-1.0, 0.5]), -1)
    assert t["inv"].item() == pytest.approx((lpa.exp() * (lpa - lpb)).sum().item(), rel=1e-5)
    # stop-gradient on the clean row: only the attacked twin moves
    t["inv"].backward()
    assert la.grad is None or torch.count_nonzero(la.grad) == 0
    assert torch.count_nonzero(lb.grad) > 0


def test_inv_choice_aligned_and_skipped():
    o = opts(6)
    a = choice("a", "c1", o, "o2")
    b = choice("b", "c1", o, "o2")
    rels = [rel("inv", "a", "b")]
    z = torch.randn(6, generator=torch.Generator().manual_seed(1))
    _, t, _, _, _ = _pair_loss(INV_C, a, b, z, z.clone(), rels, True, seed=5)  # different random perms, same beliefs
    assert t["inv"].item() == pytest.approx(0.0, abs=1e-6)
    _, t, _, _, _ = _pair_loss(INV_C, a, b, z, z.flip(0), rels, True, seed=5)
    assert t["inv"].item() > 1e-3
    # attacked twin lists the same options in another order: aligned by option string
    ob = [o[i] for i in [3, 0, 5, 1, 4, 2]]
    b2 = choice("b", "c1", ob, "o2")
    zb = z[torch.tensor([3, 0, 5, 1, 4, 2])]  # same belief per option name
    _, t, _, _, _ = _pair_loss(INV_C, a, b2, z, zb, rels, True, seed=9)
    assert t["inv"].item() == pytest.approx(0.0, abs=1e-6)
    # different option set -> not comparable, skipped (no silent misalignment)
    b3 = choice("b", "c1", o[:5] + ["other"], "o2")
    _, t, n, _, _ = _pair_loss(INV_C, a, b3, z, z.clone(), rels, True)
    assert t["inv"] is None and n["rel_skipped"] == 1


SYM_C = {"recipe": "A3", "lam": 0.5, "beta": 0.0, "sym_cons": True}


@pytest.mark.parametrize("cyg", [False, True])
def test_sym_equiv_noul(cyg):
    a, b = noul("a", "c1", 1), noul("b", "c1", 1, role="para")
    rels = [rel("equiv", "a", "b")]
    z = torch.tensor([0.4, -1.2])
    for s in range(4):
        _, t, _, _, _ = _pair_loss(SYM_C, a, b, z, z.clone(), rels, cyg, seed=s)
        assert t["cons"].item() == pytest.approx(0.0, abs=1e-7) and t["cons_equiv"] is not None
    z2 = torch.tensor([-0.7, 1.1])
    _, t, _, _, _ = _pair_loss(SYM_C, a, b, z, z2, rels, cyg)
    lp, lq = F.log_softmax(z, -1), F.log_softmax(z2, -1)
    m = 0.5 * (lp.exp() + lq.exp())
    js = 0.5 * ((lp.exp() * (lp - m.log())).sum() + (lq.exp() * (lq - m.log())).sum())
    assert t["cons"].item() > 1e-3 and t["cons"].item() == pytest.approx(js.item(), rel=1e-5)
    assert t["cons"].item() <= math.log(2) + 1e-6
    # symmetric in (a, b)
    _, t2, _, _, _ = _pair_loss(SYM_C, a, b, z2, z, rels, cyg)
    assert t2["cons"].item() == pytest.approx(t["cons"].item(), rel=1e-5)


def test_sym_equiv_choice():
    o = opts(5)
    a, b = choice("a", "c1", o, "o1"), choice("b", "c1", o[::-1], "o1")  # same option set, other canonical order
    rels = [rel("equiv", "a", "b")]
    z = torch.randn(5, generator=torch.Generator().manual_seed(2))
    _, t, _, _, _ = _pair_loss(SYM_C, a, b, z, z.flip(0), rels, True, seed=4)  # same belief per option name
    assert t["cons"].item() == pytest.approx(0.0, abs=1e-6)
    _, t, _, _, _ = _pair_loss(SYM_C, a, b, z, z.clone(), rels, True, seed=4)
    assert t["cons"].item() > 1e-3
    # without sym_cons, choice-row equiv is ignored (v0.10 behaviour)
    _, t, n, _, _ = _pair_loss({**SYM_C, "sym_cons": False}, a, b, z, z.clone(), rels, True, seed=4)
    assert t["cons"] is None and n["cons"] == 0
    # different option sets -> skipped
    c2 = choice("b", "c1", opts(5, "q"), "q1")
    _, t, n, _, _ = _pair_loss(SYM_C, a, c2, z, z.clone(), rels, True)
    assert t["cons"] is None and n["rel_skipped"] == 1


@pytest.mark.parametrize("cyg", [False, True])
def test_sym_complement(cyg):
    a, b = noul("a", "c1", 1), noul("b", "c1", 0, role="neg")
    rels = [rel("complement", "a", "b")]
    za = torch.log(torch.tensor([0.8, 0.2]))
    zb = torch.log(torch.tensor([0.2, 0.8]))  # P_b(yes) = P_a(no): perfectly complementary
    for s in range(4):
        _, t, _, _, _ = _pair_loss(SYM_C, a, b, za, zb, rels, cyg, seed=s)
        assert t["cons"].item() == pytest.approx(0.0, abs=1e-6) and t["cons_comp"] is not None
    _, t, _, _, _ = _pair_loss(SYM_C, a, b, za, za.clone(), rels, cyg)  # both say yes: contradiction
    p, q = torch.tensor([0.8, 0.2]), torch.tensor([0.2, 0.8])  # p_a vs swapped p_b
    want = 0.5 * ((p * (p / q).log()).sum() + (q * (q / p).log()).sum())
    assert t["cons"].item() == pytest.approx(want.item(), rel=1e-5) and t["cons"].item() > 0.1
    _, t2, _, _, _ = _pair_loss(SYM_C, b, a, za, za.clone(), [rel("complement", "b", "a")], cyg)
    assert t2["cons"].item() == pytest.approx(t["cons"].item(), rel=1e-5)


@pytest.mark.parametrize("n", [2, 4, 27])
def test_perm_twin_term(n):
    r = choice("a", "c1", opts(n), "o1")
    rng = random.Random(n)
    p1 = rng.sample(range(n), n)
    p2 = td.second_perm(p1, rng)
    assert p2 != p1 and sorted(p2) == list(range(n))
    z = torch.randn(n, generator=torch.Generator().manual_seed(n))
    c = {"recipe": "A3", "lam": 0.5, "beta": 0.0, "perm_twin": 1.0}
    l1 = displayed(z, p1).clone().requires_grad_(True)
    _, t, cnt = td.compute_loss(c, [r], [p1], [l1], {}, 100, 100, DEV, twins=[(0, p2, displayed(z, p2))], cyg=True)
    assert cnt["twin"] == 1 and t["perm"].item() == pytest.approx(0.0, abs=1e-6)
    z2 = z.clone()
    z2[0] += 2.0  # the second view believes something else
    _, t, _ = td.compute_loss(c, [r], [p1], [l1], {}, 100, 100, DEV, twins=[(0, p2, displayed(z2, p2))], cyg=True)
    assert t["perm"].item() > 1e-3
    # weight lam_p and ramp: total = task + lam_p * JS at full ramp
    loss, t, _ = td.compute_loss({**c, "lam_p": 2.0}, [r], [p1], [l1], {}, 100, 100, DEV,
                                 twins=[(0, p2, displayed(z2, p2))], cyg=True)
    assert loss.item() == pytest.approx(t["task"].item() + 2.0 * t["perm"].item(), rel=1e-6)


def test_pick_twins():
    rows = [choice("a", "c", opts(4), "o0"), noul("b", "c"), choice("d", "c", ["only"], "only"), choice("e", "c", opts(3), "o1")]
    rng = random.Random(1)
    perms = [perm_for(r, rng, True) for r in rows]
    r0 = random.Random(5)
    state = r0.getstate()
    assert td.pick_twins(rows, perms, 0.0, r0) == [] and r0.getstate() == state  # off -> no RNG draws
    tw = td.pick_twins(rows, perms, 1.0, random.Random(5))
    assert [i for i, _ in tw] == [0, 3]  # choice rows with >= 2 options only
    for i, p2 in tw:
        assert p2 != perms[i] and sorted(p2) == sorted(perms[i])
    assert td.pick_twins(rows, perms, 0.5, random.Random(5)) == td.pick_twins(rows, perms, 0.5, random.Random(5))


# ---------------------------------------------------------------- 5. NaN guard

def BAD(term):
    """regex: `term` is in the reported list of non-finite terms (not just somewhere in the message)."""
    return r"non-finite loss term\(s\) \[[^\]]*'" + term + "'"


def test_nan_guard_task():
    r = choice("a", "c1", opts(3), "o0")
    l = torch.tensor([0.1, float("nan"), 0.3], requires_grad=True)
    with pytest.raises(FloatingPointError, match=r"non-finite loss term\(s\) \['loss', 'task'\]"):
        td.compute_loss({"recipe": "A3", "lam": 0.5, "beta": 0.0}, [r], [[0, 1, 2]], [l], {}, 3, 10, DEV, cyg=True)


def test_nan_guard_new_terms():
    r = choice("a", "c1", opts(3), "o0")
    l = torch.tensor([0.1, 0.2, 0.3], requires_grad=True)
    c = {"recipe": "A3", "lam": 0.5, "beta": 0.1, "perm_twin": 1.0}
    with pytest.raises(FloatingPointError, match=BAD("perm")):
        td.compute_loss(c, [r], [[0, 1, 2]], [l], {}, 3, 10, DEV,
                        twins=[(0, [2, 1, 0], torch.tensor([0.0, float("nan"), 1.0]))], cyg=True)
    with pytest.raises(FloatingPointError, match=BAD("kl")):
        td.compute_loss(c, [r], [[0, 1, 2]], [l], {}, 3, 10, DEV, kl=torch.tensor(float("nan")), cyg=True)
    a, b = noul("a", "c1"), noul("b", "c1")
    with pytest.raises(FloatingPointError, match=BAD("inv")):
        td.compute_loss({**INV_C}, [a, b], [None, None], [torch.tensor([0.0, 1.0]), torch.tensor([float("inf"), 0.0])],
                        by_row([rel("inv", "a", "b")]), 3, 10, DEV, cyg=False)
    # finite everything -> no error
    td.compute_loss(c, [r], [[0, 1, 2]], [l], {}, 3, 10, DEV, kl=torch.tensor(0.5), cyg=True)


# ---------------------------------------------------------------- 6. batching keeps 'inv' twins together

def _old_units(rows):
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r)
    return list(units.values())


def _old_batches(units, bs):  # the v0.10 closure, with c["batch"] -> bs
    while True:
        random.shuffle(units)
        cur = []
        for u in units:
            cur.extend(u)
            if len(cur) >= bs:
                yield cur
                cur = []


def test_units_and_batches_unchanged_without_inv():
    rng = random.Random(0)
    rows = [noul(f"r{i}", f"c{rng.randrange(40)}") for i in range(200)]
    rels = [rel("complement", "r1", "r2"), rel("equiv", "r3", "r4")]
    units, merged = td.make_units(rows, rels)
    assert merged == 0 and [[r["id"] for r in u] for u in units] == [[r["id"] for r in u] for u in _old_units(rows)]
    random.seed(11)
    g_old = _old_batches(_old_units(rows), 16)
    seq_old = [[r["id"] for r in next(g_old)] for _ in range(50)]
    random.seed(11)
    g_new = td.batches(td.make_units(rows, rels)[0], 16)
    assert [[r["id"] for r in next(g_new)] for _ in range(50)] == seq_old


def test_inv_twins_always_batched_together():
    rng = random.Random(1)
    rows, rels = [], []
    for i in range(120):
        call = f"c{i}"
        rows.append(noul(f"a{i}", call))
        for j in range(rng.randrange(0, 3)):  # attacked twins share call_id
            rows.append(noul(f"a{i}_inj{j}", call, role="inj"))
            rels.append(rel("inv", f"a{i}", f"a{i}_inj{j}"))
    # malformed data: twin with its own call_id, and a chain across three calls -> merged into one unit
    rows += [noul("x0", "cx0"), noul("x1", "cx1"), noul("x2", "cx2")]
    rels += [rel("inv", "x0", "x1"), rel("inv", "x1", "x2"), rel("inv", "a0", "missing_row")]
    units, merged = td.make_units(rows, rels)
    assert merged == 2
    assert sum(len(u) for u in units) == len(rows) and len({r["id"] for u in units for r in u}) == len(rows)
    random.seed(20261001)
    gen = td.batches(units, 16)
    pairs = [(x["a"], x["b"]) for x in rels if x["b"] != "missing_row"]
    seen = set()
    for _ in range(300):
        ids = {r["id"] for r in next(gen)}
        seen |= ids
        for a, b in pairs:
            assert (a in ids) == (b in ids), (a, b)
    assert {"x0", "x1", "x2"} <= seen


# ---------------------------------------------------------------- 7. train() wiring with a fake model (no download)

class FakeModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.emb = torch.nn.Parameter(torch.randn(64, 8) * 0.5)
        self.head = torch.nn.Parameter(torch.randn(8, 32) * 0.5)
        self.calls = []

    def print_trainable_parameters(self):
        pass

    @contextlib.contextmanager
    def disable_adapter(self):
        yield

    def save_pretrained(self, out_dir):
        torch.save(self.state_dict(), Path(out_dir) / "fake.pt")


class FakeTok:
    def save_pretrained(self, out_dir):
        pass


def fake_cand_logits(model, ro, rows, dev, perms=None):
    perms = perms or [None] * len(rows)
    model.calls.append(([r["id"] for r in rows], [None if p is None else list(p) for p in perms], torch.is_grad_enabled()))
    out = []
    for r, p in zip(rows, perms):
        h = model.emb[zlib.crc32(r["id"].encode()) % 64]
        n = 2 if r["qtype"] == "noul" else len(r["options"])
        z = (h @ model.head)[:n]
        out.append(z if p is None else z[torch.tensor(p)])
    return out


@pytest.fixture
def fake_env(monkeypatch):
    fake_peft = types.ModuleType("peft")
    fake_peft.LoraConfig = lambda **kw: kw
    fake_peft.get_peft_model = lambda model, cfg: model
    monkeypatch.setitem(sys.modules, "peft", fake_peft)
    monkeypatch.setattr(td, "load", lambda base, dev: (FakeModel(), FakeTok()))
    monkeypatch.setattr(td, "Readout", lambda tok: None)
    monkeypatch.setattr(td, "cand_logits", fake_cand_logits)
    monkeypatch.setattr(decoder_io, "STYLE", "cygnet")


def _write_data(d: Path):
    rows, rels = [], []
    for i in range(24):
        rows += [noul(f"n{i}", f"c{i}", 1), noul(f"n{i}_neg", f"c{i}", 0, role="neg"),
                 noul(f"n{i}_inj", f"c{i}", 1, role="inj", meta={"anchor": i % 3 == 0})]
        rels += [rel("complement", f"n{i}", f"n{i}_neg"), rel("inv", f"n{i}", f"n{i}_inj")]
        o = opts(3 + i % 5)
        rows += [choice(f"k{i}", f"d{i}", o, o[i % len(o)]), choice(f"k{i}_inj", f"d{i}", o, o[i % len(o)])]
        rels += [rel("inv", f"k{i}", f"k{i}_inj"), rel("equiv", f"k{i}", f"k{i}_inj")]
    (d / "train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (d / "rels.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))


@pytest.mark.filterwarnings("ignore::UserWarning")  # torch.autocast("cuda") on a CPU-only box
def test_train_loop_wiring(fake_env, tmp_path):
    _write_data(tmp_path)
    cfg = {"base": "fake", "grad_ckpt": False, "batch": 8, "epochs": 2.0, "beta": 0.1, "log_every": 1,
           "train_file": "train.jsonl", "rel_file": "rels.jsonl", "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.5}
    res = td.train(cfg, tmp_path, tmp_path / "out", dev="cpu")
    log = res["meta"]["log"]
    assert len(log) == res["meta"]["steps"]
    for rec in log:
        assert set(td.TERMS) <= set(rec)
        assert all(rec[k] is None or math.isfinite(rec[k]) for k in td.TERMS)
    assert any(rec["inv"] is not None for rec in log) and any(rec["perm"] is not None for rec in log)
    assert any(rec["cons_comp"] is not None for rec in log) and any(rec["cons_equiv"] is not None for rec in log)
    assert res["meta"]["relation_types"] == {"complement": 24, "equiv": 24, "inv": 48}
    assert sum(rec["n_twin"] for rec in log) > 0
    # twins ride in the SAME forward call as their batch: exactly one grad-enabled call per step (+ no-grad anchor calls),
    # holding batch + twins; batch = whole units (2-3 rows) until >= 8 rows -> 8..10 rows
    grad_calls = [(ids, pp) for ids, pp, g in res["model"].calls if g]
    assert len(grad_calls) == len(log)
    for (ids, pp), rec in zip(grad_calls, log):
        nb = len(ids) - rec["n_twin"]
        assert 8 <= nb <= 10
        for k in range(nb, len(ids)):  # each twin repeats a batch row under a different permutation
            j = ids.index(ids[k])
            assert j < nb and pp[j] != pp[k] and sorted(pp[j]) == sorted(pp[k])
    # own RNG: turning twins on leaves the batches and first permutations of the run unchanged
    res0 = td.train({**cfg, "perm_twin": 0.0}, tmp_path, tmp_path / "out0", dev="cpu")
    grad0 = [(ids, pp) for ids, pp, g in res0["model"].calls if g]
    assert [(ids[:len(i0)], pp[:len(i0)]) for (ids, pp), (i0, _) in zip(grad_calls, grad0)] == grad0


def old_train(cfg, data_dir, dev="cpu"):
    """Frozen copy of the v0.10 train() loop (91b32a9), same fakes (model/readout/cand_logits via td.*), no saving.
    Returns (per-step losses, model)."""
    c = {"recipe": "A3", "epochs": 1.0, "lr": 1e-4, "batch": 16, "lam": 0.5, "r": 16, "alpha": 32, "dropout": 0.05, "beta": 0.0,
         "seed": 20260925, "train_file": "train.jsonl", "rel_file": "train_relations.jsonl", "grad_ckpt": True, **cfg}
    random.seed(c["seed"])
    torch.manual_seed(c["seed"])
    rows_all = td.read_jsonl(data_dir / c["train_file"])
    rels_all = td.read_jsonl(data_dir / c["rel_file"])
    rows = [r for r in rows_all if c["recipe"] != "A0" or r["track"] == "L0"]
    ids = {r["id"] for r in rows}
    rels = [x for x in rels_all if c["recipe"] != "A0" and x["a"] in ids and x["b"] in ids]
    n_steps = math.ceil(len(rows_all) / c["batch"] * c["epochs"])
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r)
    units = list(units.values())
    rel_by_row = defaultdict(list)
    for x in rels:
        rel_by_row[x["a"]].append(x)

    def batches():
        while True:
            random.shuffle(units)
            cur = []
            for u in units:
                cur.extend(u)
                if len(cur) >= c["batch"]:
                    yield cur
                    cur = []

    model, tok = td.load(c["base"], dev)
    model.train()
    ro = td.Readout(tok)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=c["lr"], weight_decay=0.0)
    warm = int(0.05 * n_steps)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm))))
    losses, gen = [], batches()
    for step in range(n_steps):
        batch = next(gen)
        cyg = decoder_io.STYLE == "cygnet"
        perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                 else (random.sample([0, 1], 2) if cyg else None) for r in batch]
        with torch.autocast("cuda", dtype=torch.bfloat16):
            lg = td.cand_logits(model, ro, batch, dev, perms=perms)
        anc = [i for i, r in enumerate(batch) if c["beta"] > 0 and (r.get("meta") or {}).get("anchor")]
        kl = None
        if anc:
            with torch.no_grad(), model.disable_adapter(), torch.autocast("cuda", dtype=torch.bfloat16):
                blg = td.cand_logits(model, ro, [batch[i] for i in anc], dev, perms=[perms[i] for i in anc])
            kl = torch.stack([F.kl_div(F.log_softmax(lg[i], -1), F.log_softmax(b, -1), log_target=True, reduction="sum")
                              for i, b in zip(anc, blg)]).mean()
        loss = old_loss(c, batch, perms, lg, rel_by_row, step, n_steps, dev, kl, cyg)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        sched.step()
        losses.append(round(loss.item(), 4))
    return losses, model


@pytest.mark.filterwarnings("ignore::UserWarning")
@pytest.mark.parametrize("style", ["cygnet", "od"])
@pytest.mark.parametrize("explicit", [False, True])
def test_train_loop_default_matches_old(fake_env, tmp_path, monkeypatch, style, explicit):
    """New keys unset (or at their defaults): train() follows the v0.10 trajectory exactly - same batches, permutations,
    losses and final weights - on data that also contains 'inv' relations (legacy fallback: treated like 'equiv')."""
    monkeypatch.setattr(decoder_io, "STYLE", style)
    _write_data(tmp_path)
    base = {"base": "fake", "grad_ckpt": False, "batch": 8, "epochs": 2.0, "beta": 0.1, "log_every": 1,
            "train_file": "train.jsonl", "rel_file": "rels.jsonl"}
    old_losses, old_model = old_train(base, tmp_path)
    res = td.train({**base, **(td.LOSS_DEFAULTS if explicit else {})}, tmp_path, tmp_path / "out", dev="cpu")
    assert [rec["loss"] for rec in res["meta"]["log"]] == old_losses
    for pa, pb in zip(old_model.parameters(), res["model"].parameters()):
        assert torch.equal(pa, pb)
    assert all(rec["n_twin"] == 0 and rec["inv"] is None and rec["perm"] is None for rec in res["meta"]["log"])


# ---------------------------------------------------------------- 8. review fixes (real-data shapes)

LAH_TEACHER = "qwen/qwen3-235b-a22b-2507"  # provenance string on LAH rows in train_v07..v10s4 / lah_train


@pytest.mark.parametrize("cyg", [False, True])
def test_kd_ignores_provenance_teacher_string(cyg):
    """kd > 0 on a mix that contains LAH rows (meta.teacher = model id string) used to crash with
    AttributeError: 'str' object has no attribute 'get'. A string teacher is provenance, not a target."""
    o = opts(3)
    lah = choice("lah", "c1", o, "o1", meta={"teacher": LAH_TEACHER, "anchor": False})
    lah_n = noul("lahn", "c2", 1, meta={"teacher": LAH_TEACHER})
    plain = choice("lah", "c1", o, "o1")
    plain_n = noul("lahn", "c2", 1)
    rng, gen = random.Random(2), torch.Generator().manual_seed(2)
    perms = [perm_for(lah, rng, cyg), perm_for(lah_n, rng, cyg)]
    lg = rand_logits([lah, lah_n], perms, gen)
    c = {"recipe": "A3", "lam": 0.5, "beta": 0.0, "kd": 0.3}
    got, _, _ = td.compute_loss(c, [lah, lah_n], perms, lg, {}, 5, 10, DEV, cyg=cyg)
    want = old_loss({**c, "kd": 0.0}, [plain, plain_n], perms, lg, {}, 5, 10, DEV, None, cyg)
    assert torch.equal(got, want)
    # a real (dict) teacher is still used exactly as in v0.10
    kd_rows = [choice("k", "c3", o, "o1", meta={"teacher": {"o0": 0.1, "o1": 0.7, "o2": 0.2}}),
               noul("kn", "c4", 0, meta={"teacher": {"yes": 0.3, "no": 0.7}})]
    perms = [perm_for(r, rng, cyg) for r in kd_rows]
    lg = rand_logits(kd_rows, perms, gen)
    got, _, _ = td.compute_loss(c, kd_rows, perms, lg, {}, 5, 10, DEV, cyg=cyg)
    assert torch.equal(got, old_loss(c, kd_rows, perms, lg, {}, 5, 10, DEV, None, cyg))
    assert not torch.equal(got, old_loss({**c, "kd": 0.0}, kd_rows, perms, lg, {}, 5, 10, DEV, None, cyg))
    assert td.kd_target(lah) is None and td.kd_target(kd_rows[0]) is not None and td.kd_target(noul("z", "c")) is None


def test_check_rows():
    ok = [noul("a", "c"), noul("b", "c", 0), choice("k", "c", opts(4), "o2"),
          choice("g", "c", opts(3), None, meta={"gold_probs": {"o1": 1.0}}),
          choice("w", "c", opts(255), "o254"), choice("l", "c", opts(3), "o0", meta={"teacher": LAH_TEACHER}),
          noul("t", "c", 1, meta={"teacher": {"yes": 0.8}})]
    td.check_rows(ok, kd=0.3)
    for bad in [choice("x", "c", opts(3), "zz"), choice("x", "c", opts(256), "o0"), choice("x", "c", [], None),
                choice("x", "c", opts(3), "o0", meta={"gold_probs": {"nope": 1.0}}), noul("x", "c", 2),
                noul("x", "c", None)]:
        with pytest.raises(ValueError, match="unusable training row"):
            td.check_rows(ok + [bad])
    with pytest.raises(ValueError, match="no 'yes'"):
        td.check_rows([noul("x", "c", 1, meta={"teacher": {"o1": 1.0}})], kd=0.3)
    td.check_rows([noul("x", "c", 1, meta={"teacher": {"o1": 1.0}})], kd=0.0)  # teacher unused without kd


def test_perm_twin_uses_position_not_id():
    """Twins are matched to their row by batch position; a duplicated id elsewhere in the batch cannot redirect them."""
    o = opts(4)
    r0, r1 = choice("dup", "c1", o, "o1"), choice("dup", "c1", o, "o2")
    z0 = torch.tensor([2.0, -1.0, 0.5, 0.0])
    z1 = torch.tensor([-3.0, 1.0, 0.0, 4.0])
    p0, p1, p2 = [0, 1, 2, 3], [3, 2, 1, 0], [1, 0, 3, 2]
    c = {"recipe": "A3", "lam": 0.5, "beta": 0.0, "perm_twin": 1.0}
    _, t, _ = td.compute_loss(c, [r0, r1], [p0, p1], [displayed(z0, p0), displayed(z1, p1)], {}, 10, 10, DEV,
                              twins=[(0, p2, displayed(z0, p2))], cyg=True)
    assert t["perm"].item() == pytest.approx(0.0, abs=1e-6)


def test_second_perm_needs_two():
    with pytest.raises(ValueError):
        td.second_perm([0], random.Random(0))


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_train_kd_with_lah_rows(fake_env, tmp_path):
    """End to end: kd > 0 on data that mixes dict teachers with LAH provenance strings trains without crashing."""
    _write_data(tmp_path)
    rows = td.read_jsonl(tmp_path / "train.jsonl")
    for i, r in enumerate(rows):
        if r["qtype"] == "choice" and i % 2:
            r["meta"]["teacher"] = LAH_TEACHER
        elif r["qtype"] == "noul" and i % 3 == 0:
            r["meta"]["teacher"] = {"yes": 0.9 if r["gold"] else 0.1}
    (tmp_path / "train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    cfg = {"base": "fake", "grad_ckpt": False, "batch": 8, "epochs": 1.0, "beta": 0.1, "log_every": 1, "kd": 0.3,
           "train_file": "train.jsonl", "rel_file": "rels.jsonl", "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.5}
    res = td.train(cfg, tmp_path, tmp_path / "out", dev="cpu")
    assert all(math.isfinite(rec["loss"]) for rec in res["meta"]["log"])


def test_label_smooth_and_teacher_T_default_off_and_sharpen():
    import train_decoder as td
    p = torch.tensor([0.7, 0.2, 0.1])
    assert torch.equal(td.sharpen(p, None), p) and torch.equal(td.sharpen(p, 1), p)
    q = td.sharpen(p, 0.5)
    assert abs(float(q.sum()) - 1) < 1e-6 and float(q[0]) > 0.7  # sharper
    r = {"id": "a", "qtype": "noul", "source": "x", "gold": 1, "meta": {"teacher": {"yes": 0.8}}}
    lg = [torch.tensor([0.4, -0.4])]
    base = {"recipe": "A3", "kd": 0.5, "lam": 1.0, "beta": 0.0}
    l0, _, _ = td.compute_loss(dict(base), [r], [[0, 1]], lg, {}, 0, 10, "cpu", cyg=True)
    l1, _, _ = td.compute_loss(dict(base, label_smooth=None, teacher_T={}), [r], [[0, 1]], lg, {}, 0, 10, "cpu", cyg=True)
    assert torch.equal(l0, l1)  # unset knobs = old loss exactly
    l2, _, _ = td.compute_loss(dict(base, label_smooth=0.0, teacher_T={"noul": 0.6}), [r], [[0, 1]], lg, {}, 0, 10, "cpu", cyg=True)
    assert float(l2) != float(l0)
