"""LoRA fine-tuning of a decoder LM as an OpenDecide decision model (runs on Modal, see modal_od.py).

Same recipes and losses as train.py, on the decoder readout (decoder_io.py):
  task:  CE over the candidate tokens (Yes/No, or option letters) with the same label smoothing as train.py
  cons:  complement (pA + pB - 1)^2 and equiv (pA - pB)^2 on P(yes), related rows in the same batch as
         SEPARATE sequences (no row ever sees another row)
Choice options are re-shuffled every time a row is drawn, so the model cannot learn a letter prior.
anchor (v0.6): rows with meta.anchor get + beta * KL(p_base || p_student) over the candidate tokens, where p_base is the
         frozen base model (adapter disabled, no grad). Breadth rows stay close to the base model's general behaviour
         (learning-without-forgetting / self-distillation); robustness rows are free to specialise.

v0.11 terms (all off by default; with the keys unset the loss is exactly the v0.10 loss). They work on the CANONICAL
distribution of a row (canon_logp: choice -> row["options"] order, yes/no -> [yes, no]), i.e. with the displayed option
permutation undone, so two views of the same question are comparable outcome by outcome.
  lam_inv   relation 'inv' (a = clean row, b = attacked twin, same call_id): + lam_inv * KL(stopgrad(p_a) || p_b) over the
            full distribution, yes/no and choice rows. With lam_inv = 0, 'inv' relations keep the old behaviour
            (treated like 'equiv', the pre-v0.11 fallback for any non-complement type).
  sym_cons  True: 'equiv' = Jensen-Shannon(p_a, p_b) over the full distribution (choice rows too, when both rows have the
            same option set); 'complement' = symmetric KL between p_a and p_b with yes/no swapped. Weight lam, as before.
  perm_twin that fraction of choice rows is scored a second time under another permutation in the SAME cand_logits call;
            + lam_p * JS(canonical view 1, canonical view 2). Twins are picked with their own RNG, so batches and first
            permutations are identical to a run without twins.
All consistency terms (cons, inv, perm) share the 20% warm-up ramp. Every term is logged; a non-finite term aborts the run.
Recipe v4 A4 (off by default; lam_ord 0 or unset leaves the loss, the data order and the log exactly as before):
  lam_ord   ordinal rows (choice rows with meta.option_level = {option text: level 0..K-1}): + lam_ord * ramp *
            ((E - y) * 4 / (K - 1))^2, E = sum over the displayed letters of p(letter) * level(option shown there), after
            the option re-shuffle (a permutation twin uses its own order; a row's term is the mean over its views),
            y = the gold option's level. Summed over ordinal rows and divided by the batch's row count, like the task CE
            it is added to (TRACT's per-example CE + lambda * squared error).
  expect_ord_rows  the mixer's ordinal row count: before the model loads it must equal the ordinal rows in the training
            file exactly (as expect_kd_targets), and a dry run of the data order must draw that many within 1% (at
            least batch - 1 rows: one pass drops its trailing partial batch).
kd: only a dict meta.teacher is a distillation target (a string teacher is provenance, e.g. on LAH rows, and is ignored).
Rows the loss cannot score (gold not an option, gold_probs with no mass, >255 options, ...) fail before the model loads.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import signal
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F

import decoder_io
import prism_x
from decoder_io import Readout, cand_logits, load

EPS = {"mnli": 0.08}
# v0.11 loss knobs; these defaults reproduce the v0.10 loss exactly.
LOSS_DEFAULTS = {"lam_inv": 0.0, "sym_cons": False, "perm_twin": 0.0, "lam_p": 0.5}
TERMS = ("loss", "task", "cons", "cons_comp", "cons_equiv", "inv", "perm", "kl")
ORD_TERM = "ord"  # logged (an extra TERMS entry) only when lam_ord > 0
ORD_TOL = 0.01    # allowed relative difference between the ordinal rows the run draws and those in the file


def read_jsonl(p):
    return [json.loads(l) for l in open(p)]


# ---------------------------------------------------------------- canonical order and divergences

def inverse_perm(perm):
    """perm[j] = canonical option shown at displayed position j  ->  inv[i] = displayed position of canonical option i."""
    inv = [0] * len(perm)
    for j, o in enumerate(perm):
        inv[o] = j
    return inv


def canon_logp(row, logits, perm, cyg=None):
    """Log-probs of one row in CANONICAL order: choice -> row["options"] order, yes/no -> [yes, no].
    `logits` are in displayed order (as cand_logits returns them for `perm`); this undoes the permutation.
    od-style yes/no rows are always read as [Yes, No] (perm None); cygnet-style ones carry a perm over [Yes, No]."""
    if cyg is None:
        cyg = decoder_io.STYLE == "cygnet"
    logp = F.log_softmax(logits.float(), -1)
    if perm is None or (row["qtype"] == "noul" and not cyg):
        return logp
    assert len(perm) == logp.shape[-1], (row.get("id"), len(perm), logp.shape)
    return logp[torch.tensor(inverse_perm(perm), device=logp.device)]


def kl_div(lp, lq):
    """KL(p || q) from log-probs over the same outcomes."""
    return F.kl_div(lq, lp, log_target=True, reduction="sum")


def js_div(lp, lq):
    """Jensen-Shannon divergence (natural log, in [0, ln 2]) from log-probs."""
    lm = torch.logsumexp(torch.stack([lp, lq]), 0) - math.log(2.0)
    return 0.5 * (kl_div(lp, lm) + kl_div(lq, lm))


def sym_kl(lp, lq):
    """Symmetric KL: (KL(p || q) + KL(q || p)) / 2."""
    return 0.5 * (kl_div(lp, lq) + kl_div(lq, lp))


def align(ra, la, rb, lb):
    """Canonical log-probs of two related rows over the SAME outcomes, or None when they are not comparable
    (yes/no vs choice, or different option sets). Same options in another order -> b is re-ordered to a's order."""
    if (ra["qtype"] == "noul") != (rb["qtype"] == "noul"):
        return None
    if ra["qtype"] == "noul":
        return la, lb
    oa, ob = ra["options"], rb["options"]
    if oa == ob:
        return la, lb
    if len(oa) != len(ob) or len(set(oa)) != len(oa) or set(oa) != set(ob):
        return None
    pos = {o: i for i, o in enumerate(ob)}
    return la, lb[torch.tensor([pos[o] for o in oa], device=lb.device)]


def _align_ok(ra, rb):
    """align() would return log-probs (not None) for these two rows (depends on the rows only)."""
    if (ra["qtype"] == "noul") != (rb["qtype"] == "noul"):
        return False
    if ra["qtype"] == "noul" or ra["options"] == rb["options"]:
        return True
    oa, ob = ra["options"], rb["options"]
    return len(oa) == len(ob) and len(set(oa)) == len(oa) and set(oa) == set(ob)


def aux_counts(c, batch, rel_by_row):
    """How many consistency (comp / equiv) and invariance terms compute_loss scores for this batch, from row metadata
    only, with exactly its enumeration rules. aux_norm "batch" divides each term's sum by these whole-batch counts."""
    n = Counter()
    if c["recipe"] == "A0":
        return n
    lam_inv, sym = float(c.get("lam_inv", 0.0) or 0.0), bool(c.get("sym_cons", False))
    pos = {r["id"]: i for i, r in enumerate(batch)}
    for r in batch:
        for x in rel_by_row.get(r["id"], []):
            a, b, kind = x["a"], x["b"], x["type"]
            if kind == "inv" and lam_inv > 0:
                if a in pos and b in pos and _align_ok(batch[pos[a]], batch[pos[b]]):
                    n["inv"] += 1
                continue
            if a not in pos or b not in pos:
                continue
            ra, rb = batch[pos[a]], batch[pos[b]]
            if sym:
                if kind == "complement":
                    ok = ra["qtype"] == "noul" and rb["qtype"] == "noul"
                else:
                    ok = _align_ok(ra, rb)
            else:
                ok = ra["qtype"] == "noul" and rb["qtype"] == "noul"
            if ok:
                n["cons"] += 1
                n["comp" if kind == "complement" else "equiv"] += 1
    return n


def second_perm(perm, rng):
    """A random permutation different from `perm` (len(perm) >= 2)."""
    n = len(perm)
    if n < 2:
        raise ValueError(f"second_perm needs >= 2 options, got {n}")
    while True:
        q = rng.sample(range(n), n)
        if q != list(perm):
            return q


def pick_twins(batch, perms, frac, rng):
    """[(i, perm2)] for the choice rows that get a second view (cfg perm_twin). frac 0 draws nothing from rng."""
    if not frac or frac <= 0:
        return []
    out = []
    for i, (r, p) in enumerate(zip(batch, perms)):
        if r["qtype"] == "choice" and len(r["options"]) > 1 and rng.random() < frac:
            out.append((i, second_perm(p, rng)))
    return out


# ---------------------------------------------------------------- batching

def make_units(rows, rels=()):
    """Rows grouped by call_id (one unit is never split across batches). 'inv' twins share call_id by construction;
    any 'inv' pair that does not is merged into one unit, so the invariance term always sees both rows.
    Returns (units, n_merged). Without such pairs the units are exactly the old call_id groups, in the same order."""
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r)
    cid = {r["id"]: r["call_id"] for r in rows}
    parent = {}

    def find(k):
        while parent.get(k, k) != k:
            k = parent[k]
        return k

    merged = 0
    for x in rels:
        if x.get("type") != "inv" or x["a"] not in cid or x["b"] not in cid:
            continue
        ka, kb = find(cid[x["a"]]), find(cid[x["b"]])
        if ka != kb:
            parent[kb] = ka
            merged += 1
    if merged:
        out = {}
        for k, u in units.items():
            out.setdefault(find(k), []).extend(u)
        units = out
    return list(units.values()), merged


def batches(units, batch_size):
    """Endless stream of batches of whole units (the global `random` stream, as before)."""
    while True:
        random.shuffle(units)
        cur = []
        for u in units:
            cur.extend(u)
            if len(cur) >= batch_size:
                yield cur
                cur = []


_BATCHES = batches  # the real batch stream: the A4 dry run uses it even while a pilot probe wraps td.batches


# ---------------------------------------------------------------- loss

def kd_target(r):
    """meta.teacher as a distillation target, or None. Only a dict of probabilities is a target ({"yes": p} for yes/no,
    {option: p} for choice). LAH rows (train_v07..v10s4, lah_train) carry meta.teacher = "<model id>" as provenance;
    that string is not a target, and used as one it crashed kd > 0 runs ('str' object has no attribute 'get')."""
    t = (r.get("meta") or {}).get("teacher")
    return t if isinstance(t, dict) and t else None


def check_rows(rows, kd=0.0, max_options=decoder_io.MAX_OPTIONS):
    """Fail fast (before loading a model) on rows the loss cannot score; otherwise they crash or NaN mid-run."""
    bad = []
    for r in rows:
        rid, meta = r.get("id"), (r.get("meta") or {})
        if r["qtype"] == "noul":
            g = r.get("gold")
            if not isinstance(g, (int, float)) or not 0 <= g <= 1:
                bad.append((rid, f"noul gold {g!r} not in [0, 1]"))
            if meta.get("option_level") is not None:
                bad.append((rid, ordinal_problem(r)))
            t = kd_target(r) if kd > 0 else None
            if t is not None and "yes" not in t:
                bad.append((rid, "noul meta.teacher has no 'yes'"))
            elif t is not None and not 0 <= float(t["yes"]) <= 1:
                bad.append((rid, f"noul meta.teacher yes={t['yes']!r} not in [0, 1]"))
            continue
        o = r.get("options") or []
        if not 1 <= len(o) <= max_options:
            bad.append((rid, f"{len(o)} options (allowed 1..{max_options})"))
            continue
        if meta.get("option_level") is not None:  # A4 ordinal row (recipe v4)
            why = ordinal_problem(r)
            if why:
                bad.append((rid, why))
                continue
        gp = meta.get("gold_probs")
        if gp:
            if not sum(float(gp.get(x, 0.0)) for x in o) > 0:
                bad.append((rid, "meta.gold_probs has no mass on the row's options"))
        elif r.get("gold") not in o:
            bad.append((rid, f"gold {r.get('gold')!r} not among the options"))
        t = kd_target(r) if kd > 0 else None
        if t is not None and not gp:  # a choice teacher is a distribution over exactly the row's options
            if set(t) != set(o) or len(set(o)) != len(o):
                bad.append((rid, "meta.teacher keys differ from the options (or options repeat)"))
            elif abs(sum(float(v) for v in t.values()) - 1) > 0.01 or min(float(v) for v in t.values()) < 0:
                bad.append((rid, "meta.teacher is not a probability distribution (sum 1 +- 0.01)"))
    if bad:
        raise ValueError(f"train_decoder: {len(bad)} unusable training row(s), e.g. {bad[:5]}")


def check_finite(terms, step, batch):
    live = {k: v for k, v in terms.items() if v is not None}
    vals = torch.stack([v.detach().float().reshape(()) for v in live.values()])
    if bool(torch.isfinite(vals).all()):
        return
    got = dict(zip(live, vals.tolist()))
    bad = [k for k, v in got.items() if not math.isfinite(v)]
    raise FloatingPointError(
        f"train_decoder: non-finite loss term(s) {bad} at step {step}; terms={ {k: round(v, 6) for k, v in got.items()} }; "
        f"batch row ids (first 8): {[r.get('id') for r in batch[:8]]}. Aborting instead of training on NaN.")


def sharpen(p, T):
    """Teacher temperature on a probability vector (T < 1 sharpens): p^(1/T), renormalised. T = 1 returns p."""
    if T is None or T == 1:
        return p
    q = p.clamp_min(1e-9) ** (1.0 / T)
    return q / q.sum()


# ---------------------------------------------------------------- A4 ordinal mean term (recipe v4)

def is_ordinal(r) -> bool:
    """An ordinal row: a choice row whose options are the levels of one ordered scale (meta.option_level set)."""
    ol = (r.get("meta") or {}).get("option_level")
    return r.get("qtype") == "choice" and isinstance(ol, dict) and bool(ol)


def ordinal_problem(r):
    """Why an ordinal row cannot be scored by the A4 term (None if it can). option_level keys the canonical option text
    and must give the row's K options the levels 0..K-1 exactly once; the gold must be one of the options."""
    ol = (r.get("meta") or {}).get("option_level")
    if r.get("qtype") != "choice":
        return f"meta.option_level on a {r.get('qtype')!r} row (ordinal rows are choice rows)"
    if not isinstance(ol, dict) or not ol:
        return "meta.option_level is not a non-empty dict"
    o = r.get("options") or []
    if len(o) < 2 or len(set(o)) != len(o):
        return f"{len(o)} options (or repeated options); an ordinal row needs >= 2 distinct levels"
    if set(ol) != set(o):
        return f"meta.option_level keys {sorted(ol)[:6]} differ from the options {o[:6]}"
    lv = [ol[x] for x in o]
    if any(isinstance(v, bool) or not isinstance(v, int) for v in lv) or sorted(lv) != list(range(len(o))):
        return f"meta.option_level values {lv} are not the levels 0..{len(o) - 1}, each once"
    if r.get("gold") not in o:
        return f"gold {r.get('gold')!r} is not among the options (y = the gold level)"
    return None


def ord_term(r, logits, perm=None):
    """((E - y) * 4 / (K - 1))^2 for one view of an ordinal row. `logits` are over the displayed letters, in the order
    `perm` (perm[j] = canonical option shown at position j; None = as given); E = sum_j softmax(logits)_j *
    level(options[perm[j]]). E and y are on 0..K-1, so the term is in [0, 16] (TRACT's 1-5 range for every K)."""
    ol, o = r["meta"]["option_level"], r["options"]
    k = len(o)
    perm = list(range(k)) if perm is None else perm
    if len(perm) != k or logits.shape[-1] != k:
        raise ValueError(f"ord_term: row {r.get('id')} has {k} options, perm {len(perm)}, logits {tuple(logits.shape)}")
    lev = torch.tensor([float(ol[o[i]]) for i in perm], device=logits.device)
    e = (torch.softmax(logits.float(), -1) * lev).sum()
    return ((e - float(ol[r["gold"]])) * (4.0 / (k - 1))) ** 2


def ord_rows_drawn(units, batch_size, n_steps, cyg):
    """Ordinal rows the run will draw in n_steps, by a dry run of train()'s exact data order (batches() on a copy of the
    units, the same option and Yes/No draws per step; twins use their own RNG and are not drawn here). The global random
    state is restored afterwards, so the run's batches and permutations are unchanged."""
    st = random.getstate()
    try:
        gen, n = _BATCHES(list(units), batch_size), 0
        for _ in range(n_steps):
            b = next(gen)
            for r in b:  # same draws, same order as the training loop
                if r["qtype"] == "choice":
                    random.sample(range(len(r["options"])), len(r["options"]))
                elif cyg:
                    random.sample([0, 1], 2)
            n += sum(1 for r in b if is_ordinal(r))
        return n
    finally:
        random.setstate(st)


def check_ord_count(in_file: int, drawn, expect, tol: float = ORD_TOL, tail: int = 0):
    """expect_ord_rows (the mixer's count) must equal the ordinal rows in the training file exactly, as expect_kd_targets
    does: one row that lost meta.option_level (a mixer or format-augmentation bug) fails the run. Separately, the
    ordinal rows the run draws (the dry run of the data order; None = not computed) must cover the file: within
    max(tol x the file's count, tail) rows, where tail = batch - 1 (one pass of batches() drops its trailing partial
    batch, fewer than `batch` rows; at C's size, about 4,350 ordinal rows and batch 16, the 1% bound is the larger)."""
    if expect is None:
        return
    if in_file != int(expect):
        raise ValueError(f"expect_ord_rows: expected {int(expect)}, the training file has {in_file} ordinal rows")
    allowed = max(tol * in_file, tail)
    if drawn is not None and abs(drawn - in_file) > allowed:
        raise ValueError(f"expect_ord_rows: the run draws {drawn} ordinal rows, the file has {in_file} "
                         f"(allowed +-{allowed:g})")


def ord_finite_check(rows, perms=None, twins=(), probes=None) -> dict:
    """CPU check for the memory pre-flight dry run (recipe v4 pre-flight 11): on every ordinal row view (perms: the
    displayed order of each row, e.g. one step of replay_steps.stream; None = given order; twins: that step's
    [(i, perm2)] second views), the term and its gradient are finite and the term is in [0, 16] for fixed probe logits
    (flat, steep toward either end, +-1e4 one-hot, a seeded random draw). Raises on the first failure; returns counts."""
    gen = torch.Generator().manual_seed(20261003)
    n_rows = n_eval = 0
    views = [(r, None if perms is None else perms[i]) for i, r in enumerate(rows)] + [(rows[i], p2) for i, p2 in twins]
    for r, perm in views:
        if not is_ordinal(r):
            continue
        why = ordinal_problem(r)
        if why:
            raise ValueError(f"ord_finite_check: row {r.get('id')}: {why}")
        k = len(r["options"])
        zs = probes(k) if probes else [torch.zeros(k), torch.linspace(-30, 30, k), torch.linspace(30, -30, k),
                                       1e4 * F.one_hot(torch.tensor(0), k).float(), 1e4 * F.one_hot(torch.tensor(k - 1), k).float(),
                                       torch.randn(k, generator=gen) * 8]
        for z in zs:
            z = z.detach().clone().requires_grad_(True)
            t = ord_term(r, z, perm)
            t.backward()
            tv = float(t.detach())
            if not (math.isfinite(tv) and 0.0 <= tv <= 16.0 + 1e-4 and bool(torch.isfinite(z.grad).all())):
                raise FloatingPointError(f"ord_finite_check: row {r.get('id')} perm {perm}: term {tv}, "
                                         f"grad finite {bool(torch.isfinite(z.grad).all())}")
            n_eval += 1
        n_rows += 1
    return {"ordinal_views": n_rows, "evaluations": n_eval}


def _ord_hand(levels_shown, z, y):
    """Hand computation (plain floats) of the term and its gradient over the displayed logits z:
    T = ((E - y) s)^2, s = 4 / (K - 1), dT/dz_j = 2 (E - y) s^2 p_j (level_j - E)."""
    k, m = len(z), max(z)
    ex = [math.exp(v - m) for v in z]
    p = [v / sum(ex) for v in ex]
    e = sum(pj * lj for pj, lj in zip(p, levels_shown))
    s = 4.0 / (k - 1)
    return ((e - y) * s) ** 2, [2 * (e - y) * s * s * pj * (lj - e) for pj, lj in zip(p, levels_shown)], e


def a4_selftest(n_random: int = 50, seed: int = 20261003) -> dict:
    """Recipe v4 pre-flight 10 (CPU): ord_term and its gradient match a hand computation on fixed logits for K = 3, 4, 5,
    under a shuffled option order and on a permutation twin, plus the recipe's example (K = 4, uniform p, y = 0:
    E = 1.5, term 4.0) and a random-logit gradient check against central finite differences. Raises AssertionError on
    any mismatch (then the A4 fallback applies: lam_ord 0); returns what was checked."""
    def row(k, gold_level, scramble):
        names = [f"level{j}" for j in range(k)]
        opts = [names[j] for j in scramble]  # canonical option order differs from the level order
        return {"id": f"selftest_k{k}", "qtype": "choice", "options": opts, "gold": names[gold_level],
                "meta": {"option_level": {n: j for j, n in enumerate(names)}}}

    # the recipe's example
    r4 = row(4, 0, [2, 0, 3, 1])
    for perm in (None, [3, 1, 0, 2]):
        t = float(ord_term(r4, torch.zeros(4), perm))
        assert abs(t - 4.0) < 1e-6, f"K=4 uniform y=0: term {t} != 4.0"
    checked = ["K4 uniform y0 -> 4.0"]
    fixed = {3: ([0.7, -1.1, 0.2], [2, 0, 1], 2, [1, 2, 0], [2, 1, 0]),
             4: ([0.3, -1.2, 2.0, 0.5], [2, 0, 3, 1], 1, [3, 1, 0, 2], [1, 3, 2, 0]),
             5: ([1.5, -0.4, 0.0, -2.2, 0.9], [4, 1, 0, 3, 2], 3, [2, 4, 1, 0, 3], [0, 3, 4, 2, 1])}
    for k, (zc, scramble, gold, perm, perm2) in fixed.items():
        r = row(k, gold, scramble)
        ol = r["meta"]["option_level"]
        vals = []
        for p in (perm, perm2):  # first view and its permutation twin: displayed logits = canonical logits reordered
            zd = torch.tensor([zc[i] for i in p], dtype=torch.float64, requires_grad=True)
            tt = ord_term(r, zd, p)
            tt.backward()
            t = float(tt.detach())
            th, gh, _ = _ord_hand([ol[r["options"][i]] for i in p], [zc[i] for i in p], gold)
            assert abs(t - th) < 1e-5 * max(1.0, th), f"K={k} perm {p}: term {t} vs hand {th}"
            assert all(abs(a - b) < 1e-5 for a, b in zip(zd.grad.tolist(), gh)), f"K={k} perm {p}: grad {zd.grad.tolist()} vs hand {gh}"
            vals.append(t)
        assert abs(vals[0] - vals[1]) < 1e-6, f"K={k}: the twin's term {vals[1]} differs from the first view's {vals[0]}"
        checked.append(f"K{k} shuffled + twin")
    g = torch.Generator().manual_seed(seed)
    rng = random.Random(seed)
    for _ in range(n_random):
        k = rng.choice([2, 3, 4, 5, 7])
        r = row(k, rng.randrange(k), rng.sample(range(k), k))
        p = rng.sample(range(k), k)
        z = (torch.randn(k, generator=g, dtype=torch.float64) * 3).requires_grad_(True)
        ord_term(r, z, p).backward()
        h = 1e-3
        for j in range(k):
            zp, zm = z.detach().clone(), z.detach().clone()
            zp[j] += h
            zm[j] -= h
            fd = (float(ord_term(r, zp, p)) - float(ord_term(r, zm, p))) / (2 * h)
            assert abs(fd - float(z.grad[j])) < 2e-3 * max(1.0, abs(fd)), f"K={k}: finite difference {fd} vs grad {float(z.grad[j])}"
    checked.append(f"{n_random} random-logit gradient checks")
    return {"ok": True, "checked": checked}


def compute_loss(c, batch, perms, lg, rel_by_row, step, n_steps, dev, kl=None, twins=(), cyg=None, norm=None):
    """Loss of one step. lg[i] = candidate logits of batch[i] in its displayed order perms[i]; kl = anchor KL (or None);
    twins = [(i, perm2, logits2)]: second views of choice rows (perm_twin).
    norm (aux_norm "batch"): whole-batch counts {"rows", "cons", "comp", "equiv", "inv", "twin"}; every term is then its
    sum over this micro-batch divided by the whole-batch count, so the micro-batch losses add up to the full-batch loss.
    Returns (loss, terms, counts): terms maps every name in TERMS to a 0-d tensor, or None when absent this step."""
    if cyg is None:
        cyg = decoder_io.STYLE == "cygnet"
    lam_inv, sym = float(c.get("lam_inv", 0.0) or 0.0), bool(c.get("sym_cons", False))
    lam_ord = float(c.get("lam_ord", 0.0) or 0.0)
    ls = c.get("label_smooth")        # None: the old per-source smoothing (0.05, MNLI 0.08); a number overrides it
    tT = c.get("teacher_T") or {}     # {"noul": T, "choice": T}: sharpen (T < 1) the teacher's KD targets
    full = set(c.get("kd_full_src") or ())  # yes/no sources whose teacher value is the exact probability (no smoothing)
    red = (lambda xs, k: torch.stack(xs).sum() / norm[k]) if norm else (lambda xs, k: torch.stack(xs).mean())
    task, cons, pidx = [], [], {}
    for r, perm, l in zip(batch, perms, lg):
        teach = kd_target(r) if c.get("kd", 0) > 0 else None  # distillation target
        if r["qtype"] == "noul":
            eps = EPS.get(r["source"], 0.05) if ls is None else float(ls)
            y = r["gold"] * (1 - 2 * eps) + eps
            if teach and r["source"] in full:
                y = float(teach["yes"])
            elif teach:
                ty = float(teach["yes"])
                if tT.get("noul") not in (None, 1):
                    ty = float(sharpen(torch.tensor([ty, 1 - ty]), float(tT["noul"]))[0])
                y = (1 - c["kd"]) * y + c["kd"] * ty
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
                e = 0.05 if ls is None else float(ls)
                q = torch.full((len(perm),), e / len(perm), device=dev)
                q[gi] += 1 - e
                tq = torch.tensor([float(teach.get(r["options"][i], 0.0)) for i in perm], device=dev)
                if tT.get("choice") not in (None, 1):
                    tq = sharpen(tq / tq.sum().clamp_min(1e-9), float(tT["choice"]))
                q = (1 - c["kd"]) * q + c["kd"] * tq / tq.sum().clamp_min(1e-9)
                task.append(-(q * F.log_softmax(l, -1)).sum())
            else:
                gi = perm.index(r["options"].index(r["gold"]))
                task.append(F.cross_entropy(l.unsqueeze(0), torch.tensor([gi], device=dev),
                                            label_smoothing=0.05 if ls is None else float(ls)))
    loss_task = red(task, "rows")
    loss = loss_task
    terms = dict.fromkeys(TERMS + ((ORD_TERM,) if lam_ord > 0 else ()))
    terms["task"] = loss_task
    counts = {"cons": 0, "inv": 0, "twin": len(twins), "rel_skipped": 0}
    ramp = min(1.0, step / max(1, 0.2 * n_steps))

    pos = {r["id"]: i for i, r in enumerate(batch)}
    canon = {}

    def ci(i):  # canonical log-probs of batch[i], by position (twins never go through an id lookup)
        if i not in canon:
            canon[i] = canon_logp(batch[i], lg[i], perms[i], cyg)
        return canon[i]

    def cl(rid):
        return ci(pos[rid])

    inv, comp, equiv = [], [], []
    if c["recipe"] != "A0":
        for r in batch:
            for x in rel_by_row.get(r["id"], []):
                kind = x["type"]
                if kind == "inv" and lam_inv > 0:
                    if x["a"] in pos and x["b"] in pos:
                        ab = align(batch[pos[x["a"]]], cl(x["a"]), batch[pos[x["b"]]], cl(x["b"]))
                        if ab is None:
                            counts["rel_skipped"] += 1
                        else:
                            inv.append(kl_div(ab[0].detach(), ab[1]))  # teacher = clean view, no gradient through it
                    continue
                if sym:
                    if x["a"] not in pos or x["b"] not in pos:
                        continue
                    ra, rb = batch[pos[x["a"]]], batch[pos[x["b"]]]
                    if kind == "complement":
                        if ra["qtype"] != "noul" or rb["qtype"] != "noul":
                            counts["rel_skipped"] += 1
                            continue
                        t = sym_kl(cl(x["a"]), cl(x["b"]).flip(0))  # [yes, no] of b -> [no, yes]
                        comp.append(t)
                    else:
                        ab = align(ra, cl(x["a"]), rb, cl(x["b"]))
                        if ab is None:
                            counts["rel_skipped"] += 1
                            continue
                        t = js_div(*ab)
                        equiv.append(t)
                    cons.append(t)
                elif x["a"] in pidx and x["b"] in pidx:
                    pa, pb = pidx[x["a"]], pidx[x["b"]]
                    t = (pa + pb - 1) ** 2 if kind == "complement" else (pa - pb) ** 2
                    cons.append(t)
                    (comp if kind == "complement" else equiv).append(t)
        if cons:
            terms["cons"] = red(cons, "cons")
            loss = loss + c["lam"] * ramp * terms["cons"]
    if comp:
        terms["cons_comp"] = red(comp, "comp").detach()
    if equiv:
        terms["cons_equiv"] = red(equiv, "equiv").detach()
    counts["cons"], counts["inv"] = len(cons), len(inv)
    if kl is not None:
        terms["kl"] = kl
        loss = loss + c["beta"] * kl
    if inv:
        terms["inv"] = red(inv, "inv")
        loss = loss + lam_inv * ramp * terms["inv"]
    if twins:
        pt = [js_div(ci(i), canon_logp(batch[i], l2, p2, cyg)) for i, p2, l2 in twins]
        terms["perm"] = red(pt, "twin")
        loss = loss + float(c.get("lam_p", 0.5)) * ramp * terms["perm"]
    if lam_ord > 0:  # A4 ordinal mean term (recipe v4): per ordinal row, the mean over its views; normalised like the CE
        tw_by = defaultdict(list)
        for i, p2, l2 in twins:
            if is_ordinal(batch[i]):
                tw_by[i].append(ord_term(batch[i], l2, p2))
        ords = [torch.stack([ord_term(r, l, perm)] + tw_by.get(i, [])).mean()
                for i, (r, perm, l) in enumerate(zip(batch, perms, lg)) if is_ordinal(r)]
        counts["ord"] = len(ords)
        if ords:
            terms[ORD_TERM] = torch.stack(ords).sum() / (norm["rows"] if norm else len(batch))
            loss = loss + lam_ord * ramp * terms[ORD_TERM]
    terms["loss"] = loss
    check_finite(terms, step, batch)
    return loss, terms, counts


# ---------------------------------------------------------------- F2 rendered-prompt identity (recipe v4 pre-flight 9)

def train_prompt_path(cfg: dict) -> dict:
    """The tokenizer, layout and style train() renders prompts with for this config, without loading the model:
    load(cfg base at base_revision) (an init_adapter is loaded on top, so the base tokenizer is used), LAYOUT = cfg
    layout (PRISM-X's when it is on and no layout is given, else text_first), STYLE = cfg style."""
    layout = cfg["layout"] if cfg.get("layout") else (prism_x.LAYOUT if prism_x.resolve(cfg.get("prism_x")) else "text_first")
    return {"tok": decoder_io.load_tokenizer(cfg["base"], revision=cfg.get("base_revision")), "layout": layout,
            "style": cfg.get("style") or decoder_io.STYLE, "src": f"{cfg['base']}@{cfg.get('base_revision')}"}


def f2_preflight(cfg: dict, adapter=None, gate_style=None) -> dict:
    """Recipe v4 F2 on THIS machine: the sha256 of the rendered prompt of the 3 fixed rows (decoder_io.F2_ROWS, given
    and reversed order: 6 views) is identical on every prompt path this machine can render. Paths:
      "train"      this config as train() renders it (base tokenizer at base_revision, cfg layout and style);
      "gate_serve" with an adapter: decoder_io.load(base, adapter=...) with STYLE cygnet. This is both the dev gate
                   read (od_gcp.py predict: STYLE preset to --style or cygnet) and serving (di_engine / serve_tunnel:
                   STYLE cygnet). Both make the same call, so they are one path, not two;
      "gate"       only with gate_style (od_gcp.py predict --style S): the gate read with that preset.
    Within one process this proves only that the tokenizer files, layout and style agree: every path renders with this
    machine's transformers / jinja2. A difference between the training image, the L4 gate VM and the serving host
    shows up only when their f2_record files are compared (f2_compare; `train_decoder.py f2 --out` on each machine).
    Raises RuntimeError on any difference; returns the per-path report."""
    saved = (decoder_io.LAYOUT, decoder_io.STYLE)
    try:
        paths = {"train": train_prompt_path(cfg)}
        if adapter:
            decoder_io.LAYOUT, decoder_io.STYLE = saved[0], "cygnet"
            paths["gate_serve"] = decoder_io.adapter_prompt_path(cfg["base"], str(adapter))
            if gate_style and gate_style != "cygnet":
                decoder_io.LAYOUT, decoder_io.STYLE = saved[0], gate_style
                paths["gate"] = decoder_io.adapter_prompt_path(cfg["base"], str(adapter), style=gate_style)
        return decoder_io.assert_prompt_identity(paths)
    finally:
        decoder_io.LAYOUT, decoder_io.STYLE = saved


def f2_record(rep: dict, where: str) -> dict:
    """One machine's F2 record (what `train_decoder.py f2 --out` writes): the 6 per-view sha256 (one set: f2_preflight
    has checked that every path of rep renders them identically), each path's layout, style, template sha and source,
    and the software that rendered them."""
    import importlib.metadata as md
    import platform
    env = {"python": platform.python_version(), "host": platform.node()}
    for pkg in ("transformers", "tokenizers", "jinja2"):
        try:
            env[pkg] = md.version(pkg)
        except md.PackageNotFoundError:
            env[pkg] = None
    first = next(iter(rep.values()))
    return {"f2_record": 1, "where": where, "env": env, "views": list(first["views"]),
            "sha": dict(zip(first["views"], first["sha"])),
            "paths": {k: {f: v[f] for f in ("layout", "style", "chat_template_sha", "src", "qwen35", "chat_kwargs")}
                      for k, v in rep.items()}}


def f2_compare(records: dict) -> dict:
    """Recipe v4 F2 across machines: every record ({label: f2_record}) has the same 6 views and the same sha256 per
    view as the first one (the reference), and every Qwen3.5 path renders with thinking off. Raises RuntimeError on
    any difference (before the GO); returns the summary to write to the look log."""
    names = list(records)
    if len(names) < 2:
        raise ValueError("f2_compare needs a reference record and at least one other")
    ref = records[names[0]]
    bad = []
    for n in names:
        rec = records[n]
        if rec.get("f2_record") != 1 or len(rec.get("sha") or {}) != 6:
            bad.append(f"{n}: not an F2 record with 6 views")
            continue
        for k, p in rec["paths"].items():
            if p["qwen35"] and (p.get("chat_kwargs") or {}).get("enable_thinking") is not False:
                bad.append(f"{n}/{k}: Qwen3.5 path without enable_thinking=False")
        if n == names[0]:
            continue
        if rec["views"] != ref["views"]:
            bad.append(f"{n}: views {rec['views']} != {ref['views']}")
            continue
        for v in ref["views"]:
            if rec["sha"][v] != ref["sha"][v]:
                bad.append(f"{n} {v}: {rec['sha'][v][:12]} != {names[0]} {ref['sha'][v][:12]} (transformers "
                           f"{rec['env'].get('transformers')} vs {ref['env'].get('transformers')}, jinja2 "
                           f"{rec['env'].get('jinja2')} vs {ref['env'].get('jinja2')})")
    if bad:
        raise RuntimeError("F2 cross-machine rendered-prompt identity failed: " + "; ".join(bad[:10]))
    return {"f2_cross": "pass", "reference": names[0], "records": {n: {"where": records[n]["where"],
            "env": records[n]["env"], "paths": sorted(records[n]["paths"])} for n in names}, "sha": ref["sha"]}


# ---------------------------------------------------------------- training

def _est_tokens(r: dict) -> int:
    """Rough prompt length in tokens (system prompt + text + question + options + card), for micro-batch packing."""
    n = len(r.get("state") or "") + len(r.get("card") or "") + len(r.get("instructions") or "")
    n += sum(len(o) + 4 for o in (r.get("options") or []))
    return int((n + 600) / 3.2)


def _micro_groups(batch: list, uid: dict, tw: list, budget: int) -> list:
    """Split a batch into micro-batches of whole units (a unit holds a record's related rows, so relation terms stay
    inside one micro-batch). Cost of a micro-batch = sequences x padded max length (twins count as extra sequences).
    Units are packed longest first; a unit over the budget on its own becomes its own micro-batch."""
    pad = max(1, decoder_io.PAD_MULTIPLE)
    padded = lambda n: -(-n // pad) * pad
    twin_n = Counter(i for i, _ in tw)
    order, members = [], defaultdict(list)
    for i, r in enumerate(batch):
        u = uid.get(r["id"], ("row", i))
        if u not in members:
            order.append(u)
        members[u].append(i)
    info = []
    for u in order:
        idx = members[u]
        info.append((max(_est_tokens(batch[i]) for i in idx), sum(1 + twin_n[i] for i in idx), idx))
    info.sort(key=lambda x: -x[0])
    groups, cur, cur_len, cur_seq = [], [], 0, 0
    for ln, nseq, idx in info:
        if cur and (cur_seq + nseq) * padded(max(cur_len, ln)) > budget:
            groups.append(sorted(cur))
            cur, cur_len, cur_seq = [], 0, 0
        cur += idx
        cur_len, cur_seq = max(cur_len, ln), cur_seq + nseq
    if cur:
        groups.append(sorted(cur))
    return groups


# Per-segment knobs of a run (resume, stop points, logging): never part of its identity, so a run split across machines
# or Modal accounts (a relay) resumes although these differ between segments.
RUN_KEYS = ("resume", "ckpt_every_min", "log_every", "expect_resume", "stop_after_min", "stop_at_step",
            "allow_code_change", "allow_env_change", "fresh_start", "stop_at_unix", "snap_every", "snap_fracs",
            "expect_trainable", "expect_kd_targets", "expect_kd_full", "expect_ord_rows")
# Every config key the trainer (or its launchers) reads; train() refuses any other key, so a key whose code is missing
# fails loudly instead of being silently ignored.
GOOD_EVERY, GOOD_QUIET = 2000, 400  # _ckpt_good refresh: every ~2,000 steps, only if no alert in the last 400 steps
KNOWN_KEYS = frozenset(RUN_KEYS) | {
    "base", "base_revision", "recipe", "epochs", "lr", "batch", "lam", "r", "alpha", "dropout", "beta", "seed",
    "train_file", "rel_file", "grad_ckpt", "lam_inv", "sym_cons", "perm_twin", "lam_p", "style", "layout", "targets",
    "kd", "kd_skip_src", "kd_full_src", "label_smooth", "teacher_T", "micro_tokens", "aux_norm", "init_adapter",
    "prism_x", "px_selfcheck", "writeblock_frac", "ablate_splits", "no_overwrite", "lam_ord"}
CODE_MODULES = ("train_decoder", "decoder_io", "prism_x", "writeblock")
ENV_PACKAGES = ("torch", "transformers", "peft", "accelerate", "triton", "fla-core", "flash-linear-attention",
                "tokenizers", "safetensors", "huggingface-hub", "numpy")


def _sha_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def _sha_tensor(t: torch.Tensor) -> str:
    """Exact content hash of a tensor (bytes + shape + dtype)."""
    t = t.detach().contiguous().cpu().reshape(-1)
    return hashlib.sha256(t.view(torch.uint8).numpy().tobytes()).hexdigest() + f"|{tuple(t.shape)}|{t.dtype}"


def _batch_hash(batch: list) -> str:
    return hashlib.sha256("\n".join(r["id"] for r in batch).encode()).hexdigest()


def _env() -> dict:
    """Software and GPU a segment runs on. A resumed segment must match (Modal accounts build their own images)."""
    import sys
    from importlib import metadata
    e = {"python": sys.version.split()[0], "torch_cuda": torch.version.cuda,
         "cudnn": torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None}
    for p in ENV_PACKAGES:
        try:
            e[p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            e[p] = None
    if torch.cuda.is_available():  # the dropout grid (so the random masks) depends on the SM count
        pr = torch.cuda.get_device_properties(0)
        e["gpu"], e["sm_count"] = pr.name, pr.multi_processor_count
    return e


def _code() -> dict:
    import importlib.util
    out = {}
    for m in CODE_MODULES:
        spec = importlib.util.find_spec(m)
        out[m] = _sha_file(spec.origin) if spec and spec.origin else None
    return out


def _trainable(model) -> dict:
    """Every trained tensor by name: the LoRA adapter, plus PRISM-X (its own module, not a submodule of the model)."""
    out = {n: p for n, p in model.named_parameters() if p.requires_grad}
    if prism_x.PX is not None:
        out.update({"__px__." + n: p for n, p in prism_x.PX.named_parameters()})
    return out


def _opt_names(opt, tr: dict) -> list:
    """The optimizer's parameters in order, by name (load_state_dict pairs saved state with parameters by position)."""
    by_id = {id(p): n for n, p in tr.items()}
    return [(by_id.get(id(p), "?"), tuple(p.shape), str(p.dtype)) for g in opt.param_groups for p in g["params"]]


def _diff(saved: dict, now: dict) -> dict:
    keys = sorted(set(saved or {}) | set(now or {}), key=str)
    return {k: [(saved or {}).get(k), (now or {}).get(k)] for k in keys if (saved or {}).get(k) != (now or {}).get(k)}


def _identity(c: dict) -> dict:
    """The config keys that define a run. Under aux_norm "batch" the loss does not depend on micro_tokens, so a relay
    segment may pack differently (e.g. the L4 tail at a smaller budget)."""
    batch_norm = c.get("aux_norm") == "batch"
    return {k: v for k, v in c.items() if k not in RUN_KEYS and not (batch_norm and k == "micro_tokens")}


def _fingerprint(c: dict, rows: list, n_steps: int, data_hashes=()) -> str:
    """Identifies a run for resume: the config (minus per-segment knobs), the step count, the training rows and the
    exact bytes of the data and relations files."""
    cfg = _identity(c)
    h = hashlib.sha256(json.dumps(cfg, sort_keys=True, default=str).encode())
    h.update(str(n_steps).encode())
    for r in rows:
        h.update(r["id"].encode())
    for d in data_hashes:
        h.update(d.encode())
    return h.hexdigest()


def _save_ckpt(ckpt: Path, model, opt, sched, next_step: int, log: list, minutes: float, fp: str, extra: dict,
               on_ckpt=None, tok=None):
    """Atomic checkpoint: write to _ckpt.tmp, then swap it in, so a machine stopped mid-write leaves the old one intact.
    Holds every trained tensor by name (trainable.safetensors), a usable adapter copy, the optimizer, scheduler, RNG
    states and a manifest of file hashes (checked on resume, so a checkpoint copied between accounts is verified)."""
    from safetensors.torch import save_file
    tmp, old = ckpt.with_name(ckpt.name + ".tmp"), ckpt.with_name(ckpt.name + ".old")
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "adapter").mkdir(parents=True)
    model.save_pretrained(tmp / "adapter")
    prism_x.save(tmp / "adapter")  # no-op without PRISM-X
    if tok is not None:  # the adapter copy is loadable on its own (the emergency fallback model)
        tok.save_pretrained(tmp / "adapter")
    (tmp / "adapter" / "snap.json").write_text(json.dumps({"cfg": extra.get("cfg"), "step": next_step,
                                                           "fingerprint": fp}, default=str))
    tr = _trainable(model)
    save_file({n: p.detach().contiguous().cpu() for n, p in tr.items()}, str(tmp / "trainable.safetensors"))
    torch.save({"step": next_step, "opt": opt.state_dict(), "sched": sched.state_dict(), "log": log, "minutes": minutes,
                "fingerprint": fp, "torch_rng": torch.get_rng_state(),
                "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
                "tensors": {n: _sha_tensor(p) for n, p in tr.items()}, "opt_params": _opt_names(opt, tr), **extra},
               tmp / "state.pt")
    files = sorted(p for p in tmp.rglob("*") if p.is_file())
    (tmp / "manifest.json").write_text(json.dumps(
        {"step": next_step, "fingerprint": fp, "files": {str(p.relative_to(tmp)): _sha_file(p) for p in files}}, indent=1))
    if old.exists():  # left over from a stop between the two renames below
        shutil.rmtree(old)
    if ckpt.exists():
        ckpt.rename(old)
    tmp.rename(ckpt)
    if old.exists():
        shutil.rmtree(old)
    if on_ckpt is not None:
        on_ckpt()  # e.g. Modal: vol.commit(), so the checkpoint is durable before it is reported
    print(json.dumps({"checkpoint": str(ckpt), "next_step": next_step}), flush=True)


def _verify_manifest(ckpt: Path):
    m = ckpt / "manifest.json"
    if not m.exists():
        raise RuntimeError(f"{ckpt} has no manifest.json (incomplete copy, or saved by older code)")
    files = json.loads(m.read_text())["files"]
    bad = [f for f, h in files.items() if not (ckpt / f).exists() or _sha_file(ckpt / f) != h]
    if bad:
        raise RuntimeError(f"checkpoint files missing or changed (bad copy?): {bad[:5]}")


def _snapshot(snaps: Path, done: int, model, tok, meta: dict, on_ckpt=None):
    """A kept (never overwritten) adapter at step `done`: fallback model and averaging candidate. A failed save is
    logged and never stops training."""
    dst, tmp = snaps / f"s{done:06d}", snaps / f".s{done:06d}.tmp"
    if dst.exists():
        return
    try:
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        model.save_pretrained(tmp)
        prism_x.save(tmp)
        tok.save_pretrained(tmp)
        (tmp / "train_meta.json").write_text(json.dumps({**meta, "snapshot_step": done}, indent=2, default=str))
        tmp.rename(dst)
        if on_ckpt is not None:
            on_ckpt()
        print(json.dumps({"snapshot": str(dst)}), flush=True)
    except Exception as e:  # noqa: BLE001 (insurance only)
        print(json.dumps({"snapshot_failed": done, "error": repr(e)[:300]}), flush=True)


def _copy_good(ckpt: Path, on_ckpt=None):
    """_ckpt -> _ckpt_good (a rollback point taken only while no alert fired recently); swap via a temp folder."""
    good, tmp = ckpt.with_name(ckpt.name + "_good"), ckpt.with_name(ckpt.name + "_good.tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    shutil.copytree(ckpt, tmp)
    if good.exists():
        shutil.rmtree(good)
    tmp.rename(good)
    if on_ckpt is not None:
        on_ckpt()


def _px_selfcheck(model, ro, rows, perms, dev, tol=1e-3):
    """PRISM-X starts as the arm-E model: with every new part at its zero init, the candidate logits must equal the
    logits with PRISM-X switched off. Runs once before step 0, in eval mode (no dropout), without gradients; it draws
    no random numbers, so the run's data order is unchanged."""
    was = model.training
    model.eval()
    try:
        with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
            a = cand_logits(model, ro, rows, dev, perms=perms)
            prism_x.check_fired()
            prism_x.STATE["enabled"] = False
            b = cand_logits(model, ro, rows, dev, perms=perms)
    finally:
        prism_x.STATE["enabled"] = True
        model.train(was)
    diff = max(float((F.log_softmax(x.float(), -1) - F.log_softmax(y.float(), -1)).abs().max()) for x, y in zip(a, b))
    print(json.dumps({"prism_x_selfcheck": {"rows": len(rows), "max_abs_logprob_diff": diff}}), flush=True)
    if not diff <= tol:
        raise RuntimeError(f"PRISM-X self-check failed: at init the logits differ from arm E by {diff} (> {tol})")


def train(cfg: dict, data_dir: Path, out_dir: Path, dev="cuda", on_ckpt=None) -> dict:
    """Trains and saves the adapter to out_dir. With cfg stop_at_step / stop_after_min it stops early at a step boundary
    after a checkpoint and returns {"stopped": True, ...} (a relay segment); a rerun of the same config resumes there.
    on_ckpt() runs after every checkpoint and after the final save (Modal: vol.commit)."""
    c = {"recipe": "A3", "epochs": 1.0, "lr": 1e-4, "batch": 16, "lam": 0.5, "r": 16, "alpha": 32, "dropout": 0.05, "beta": 0.0,
         "seed": 20260925, "train_file": "train.jsonl", "rel_file": "train_relations.jsonl", "grad_ckpt": True,
         **LOSS_DEFAULTS, **cfg}
    if not (c["lam_inv"] >= 0 and 0 <= c["perm_twin"] <= 1 and c["lam_p"] >= 0):
        raise ValueError(f"bad v0.11 loss cfg: lam_inv={c['lam_inv']} perm_twin={c['perm_twin']} lam_p={c['lam_p']}")
    unknown = sorted(set(cfg) - KNOWN_KEYS)
    if unknown:
        raise ValueError(f"train_decoder: unknown config key(s) {unknown} (nothing reads them; typo or missing code?)")
    lam_ord, expect_ord = c.get("lam_ord", 0.0), c.get("expect_ord_rows")
    if lam_ord is not None and (isinstance(lam_ord, bool) or not isinstance(lam_ord, (int, float))
                                or not math.isfinite(lam_ord) or lam_ord < 0):
        raise ValueError(f"lam_ord must be a finite number >= 0 (0 = off, the A4 fallback), got {lam_ord!r}")
    if expect_ord is not None and (isinstance(expect_ord, bool) or not isinstance(expect_ord, int) or expect_ord < 0):
        raise ValueError(f"expect_ord_rows must be an integer >= 0, got {expect_ord!r}")
    lam_ord = float(lam_ord or 0.0)
    ord_track = lam_ord > 0 or expect_ord is not None  # off: nothing below runs, the run is exactly as before
    aux_norm = c.get("aux_norm", "micro")
    if aux_norm not in ("micro", "batch"):
        raise ValueError(f"aux_norm must be 'micro' or 'batch', got {aux_norm!r}")
    if c.get("style") and decoder_io.STYLE != c["style"]:
        raise ValueError(f"decoder_io.STYLE is {decoder_io.STYLE!r} but the config says {c['style']!r}")
    px_cfg = prism_x.resolve(c.get("prism_x"))  # PRISM-X arms H/I/J (None = off; the run is then unchanged)
    if px_cfg:
        c.setdefault("layout", prism_x.LAYOUT)
    decoder_io.LAYOUT = c.get("layout", "text_first")  # PRISM layout test (prompt order); predictions after training reuse it
    if px_cfg and (decoder_io.LAYOUT != prism_x.LAYOUT or decoder_io.STYLE != "cygnet"):
        raise ValueError(f"PRISM-X needs style 'cygnet' and layout '{prism_x.LAYOUT}' "
                         f"(got {decoder_io.STYLE!r}, {decoder_io.LAYOUT!r})")
    random.seed(c["seed"])
    torch.manual_seed(c["seed"])
    twin_rng = random.Random(c["seed"] + 1)  # own stream: perm_twin never changes batches or first permutations
    rows_all = read_jsonl(data_dir / c["train_file"])
    rels_all = read_jsonl(data_dir / c["rel_file"])
    rows = [r for r in rows_all if c["recipe"] != "A0" or r["track"] == "L0"]
    skip = set(c.get("kd_skip_src") or [])  # e.g. ["blend50"]: drop old model-teacher soft labels, keep human vote shares
    if skip:
        for r in rows:
            m = r.get("meta") or {}
            if isinstance(m.get("teacher"), dict) and m.get("teacher_src") in skip:
                r["meta"] = {k: v for k, v in m.items() if k != "teacher"}
    ids = {r["id"] for r in rows}
    rels = [x for x in rels_all if c["recipe"] != "A0" and x["a"] in ids and x["b"] in ids]
    n_steps = math.ceil(len(rows_all) / c["batch"] * c["epochs"])  # step-matched across recipes
    check_rows(rows, c.get("kd", 0) or 0)

    units, inv_merged = make_units(rows, rels)
    if inv_merged:
        print(f"make_units: merged {inv_merged} 'inv' pair(s) with different call_ids into one unit", flush=True)
    rel_by_row = defaultdict(list)
    for x in rels:
        rel_by_row[x["a"]].append(x)
    rel_types = dict(sorted(Counter(x["type"] for x in rels).items()))
    n_kd = sum(kd_target(r) is not None for r in rows) if c.get("kd", 0) else 0
    full = set(c.get("kd_full_src") or ())
    n_full = sum(1 for r in rows if r["source"] in full and r["qtype"] == "noul" and kd_target(r) is not None) \
        if c.get("kd", 0) else 0
    print(json.dumps({"rows": len(rows), "relations": rel_types, "units": len(units), "kd_targets": n_kd,
                      **({"kd_full_rows": n_full} if full else {}), "aux_norm": aux_norm,
                      **{k: c[k] for k in LOSS_DEFAULTS}}), flush=True)
    for key, got in (("expect_kd_targets", n_kd), ("expect_kd_full", n_full)):
        if c.get(key) is not None and int(c[key]) != got:
            raise ValueError(f"{key}: expected {c[key]}, the data gives {got}")
    ord_info = None
    if ord_track:  # A4 (recipe v4): counted before the model loads
        ord_info = {"lam_ord": lam_ord, "rows_in_file": sum(1 for r in rows if is_ordinal(r)),
                    "rows_drawn_planned": None, "expect_ord_rows": expect_ord, "tol": ORD_TOL}
        if expect_ord is not None:  # the dry run leaves the random state exactly as it found it
            ord_info["rows_drawn_planned"] = ord_rows_drawn(units, c["batch"], n_steps, decoder_io.STYLE == "cygnet")
        print(json.dumps({"ordinal": ord_info}), flush=True)
        if expect_ord is not None:
            check_ord_count(ord_info["rows_in_file"], ord_info["rows_drawn_planned"], expect_ord, tail=c["batch"] - 1)
        elif lam_ord > 0:
            print(json.dumps({"warning": "lam_ord > 0 without expect_ord_rows: the ordinal row count is not checked"}),
                  flush=True)

    from peft import LoraConfig, get_peft_model
    # base_revision pins the exact Hugging Face commit of the base model (every Modal account downloads its own copy)
    want = (decoder_io.LAYOUT, decoder_io.STYLE)
    model, tok = load(c["base"], dev, **({"revision": c["base_revision"]} if c.get("base_revision") else {}))
    if (decoder_io.LAYOUT, decoder_io.STYLE) != want:  # e.g. prism_x.uninstall() restored an earlier adapter's layout
        raise RuntimeError(f"prompt layout/style changed during the model load: {want} -> "
                           f"{(decoder_io.LAYOUT, decoder_io.STYLE)}")
    if c["grad_ckpt"]:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        model.enable_input_require_grads()
    targets = c.get("targets") or ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    if c.get("init_adapter"):  # continue training an existing adapter (stage 2); the KL anchor still uses the frozen base
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, c["init_adapter"], is_trainable=True)
    else:
        model = get_peft_model(model, LoraConfig(r=c["r"], lora_alpha=c["alpha"], lora_dropout=c["dropout"],
                                                 task_type="CAUSAL_LM", target_modules=targets))
    model.print_trainable_parameters()
    if float(c.get("writeblock_frac", 0) or 0) > 0:  # PRISM test F: protected recurrent memory, trained end to end
        print(json.dumps({"writeblock": {"frac": c["writeblock_frac"], "deltanet_layers": decoder_io.install_writeblock(model, float(c["writeblock_frac"]))}}), flush=True)
    px_loaded = False
    if px_cfg:  # installed after PEFT, so PEFT never wraps or saves the control plane (prism_x.save does)
        print(json.dumps({"prism_x": prism_x.install(model, px_cfg, dev)}), flush=True)
        if c.get("init_adapter") and (Path(c["init_adapter"]) / "prism_x.safetensors").exists():
            prism_x.load_weights(c["init_adapter"])  # continue a PRISM-X model (no longer at its zero init)
            px_loaded = True
    model.train()
    ro = Readout(tok)
    n_max = max((len(r["options"]) for r in rows if r["qtype"] == "choice"), default=0)
    if n_max > 26 and getattr(ro, "wide", None) is not None and len(ro.wide) < n_max:
        raise ValueError(f"train_decoder: a row has {n_max} options but this tokenizer has only {len(ro.wide)} labels")
    n_tr = sum(p.numel() for p in model.parameters() if p.requires_grad)
    px_params = [q for g in prism_x.param_groups() for q in g["params"]]
    print(json.dumps({"trainable": n_tr, "trainable_px": sum(q.numel() for q in px_params)}), flush=True)
    if c.get("expect_trainable") is not None and int(c["expect_trainable"]) != n_tr:
        raise ValueError(f"expect_trainable: expected {c['expect_trainable']}, the model has {n_tr} (r/alpha/targets?)")
    low = sorted({str(q.dtype) for q in [*(p for p in model.parameters() if p.requires_grad), *px_params]} - {"torch.float32"})
    if low:  # bf16 masters silently drop small updates (Adam steps below the bf16 spacing)
        raise ValueError(f"trainable parameters must be float32, found {low}")
    params = [p for p in model.parameters() if p.requires_grad]
    px_groups = prism_x.param_groups()  # own learning rates per part; the cosine schedule below scales every group
    opt = torch.optim.AdamW([{"params": params, "lr": c["lr"]}] + px_groups, lr=c["lr"], weight_decay=0.0)
    params = params + [p for g in px_groups for p in g["params"]]  # gradient clipping covers everything trained
    warm = int(0.05 * n_steps)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm))))

    log, t0, gen = [], time.time(), batches(units, c["batch"])
    # training monitor (gradient norm, loss trend, alerts); saved in checkpoints so a resumed run logs identically
    mon = {"gn": [], "task": [], "streak": 0, "best": None, "last_alert": None, "last_good": 0, "good_frozen": False}
    if ord_track:
        mon["ord_seen"] = 0  # ordinal rows drawn so far (checked against the dry run at the end)
    # Save-and-resume (Spot VMs, auto-stop timers): every ckpt_every_min minutes the adapter, optimizer, scheduler,
    # step, log and RNG states go to out_dir/_ckpt. A rerun of the same config resumes exactly: the finished steps'
    # random-number use (batch order, option permutations, twin picks) is replayed without GPU work, then the torch
    # RNG states are restored.
    ckpt, start, every = out_dir / "_ckpt", 0, float(c.get("ckpt_every_min", 15))
    data_hashes = (_sha_file(data_dir / c["train_file"]), _sha_file(data_dir / c["rel_file"]))
    fp = _fingerprint(c, rows, n_steps, data_hashes)
    env, code, last_hash = _env(), _code(), None
    old = ckpt.with_name(ckpt.name + ".old")
    if not (ckpt / "state.pt").exists() and (old / "state.pt").exists():  # stopped between the two renames
        if ckpt.exists():
            shutil.rmtree(ckpt)
        old.rename(ckpt)
    elif (ckpt / "state.pt").exists() and old.exists():  # stopped after the swap, before the clean-up
        shutil.rmtree(old)
    if ckpt.with_name(ckpt.name + ".done").exists():  # stopped during the final clean-up (the model was saved)
        shutil.rmtree(ckpt.with_name(ckpt.name + ".done"))
    if c.get("no_overwrite") and (out_dir / "train_meta.json").exists() and not (ckpt / "state.pt").exists():
        raise RuntimeError(f"{out_dir} already holds a finished model (train_meta.json) and no checkpoint")
    if c.get("resume", True) and (ckpt / "state.pt").exists():
        st = torch.load(ckpt / "state.pt", map_location="cpu", weights_only=False)
        if st.get("fingerprint") != fp and not c.get("fresh_start"):
            # never silently start over: that would burn the budget and, at the next save, replace the checkpoint
            raise RuntimeError(f"checkpoint in {ckpt} is for a different run (config diff saved->now: "
                               f"{_diff(st.get('cfg'), _identity(c))}; "
                               f"data {st.get('data')} -> {list(data_hashes)}). Set fresh_start to discard it.")
        if st.get("fingerprint") != fp:
            print("fresh_start: ignoring the checkpoint in", ckpt, flush=True)
        else:
            _verify_manifest(ckpt)  # every file as saved (a copy between accounts is checked here)
            if st.get("env") != env and not c.get("allow_env_change"):
                raise RuntimeError(f"software/GPU differs from the checkpoint's (saved->now): {_diff(st.get('env'), env)}")
            if st.get("code") != code and not c.get("allow_code_change"):
                raise RuntimeError(f"code differs from the checkpoint's (saved->now): {_diff(st.get('code'), code)}")
            from safetensors.torch import load_file
            if px_cfg:
                prism_x.load_weights(ckpt / "adapter")  # buffers too; parameters are then set by name below
            tr, sd = _trainable(model), load_file(str(ckpt / "trainable.safetensors"))
            if set(sd) != set(tr):
                raise RuntimeError(f"trained tensors differ: missing {sorted(set(tr) - set(sd))[:5]}, "
                                   f"unexpected {sorted(set(sd) - set(tr))[:5]}")
            with torch.no_grad():
                for n, p in tr.items():
                    if sd[n].shape != p.shape or sd[n].dtype != p.dtype:
                        raise RuntimeError(f"{n}: saved {tuple(sd[n].shape)} {sd[n].dtype}, model {tuple(p.shape)} {p.dtype}")
                    p.copy_(sd[n].to(p.device))
            bad = [n for n, p in tr.items() if _sha_tensor(p) != st["tensors"][n]]
            if bad:
                raise RuntimeError(f"restored tensors do not match the saved hashes: {bad[:5]}")
            if _opt_names(opt, tr) != st["opt_params"]:
                raise RuntimeError("optimizer parameter order/shapes differ from the checkpoint's")
            opt.load_state_dict(st["opt"])
            sched.load_state_dict(st["sched"])
            cyg0 = decoder_io.STYLE == "cygnet"
            for _ in range(st["step"]):
                b = next(gen)
                ps = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                      else (random.sample([0, 1], 2) if cyg0 else None) for r in b]
                pick_twins(b, ps, c["perm_twin"], twin_rng)
                last_hash = _batch_hash(b)
            # the replay must land exactly where the saved run was: same random streams, same last batch
            if (random.getstate() != st["py_rng"] or twin_rng.getstate() != st["twin_rng"]
                    or last_hash != st["last_batch"]):
                raise RuntimeError("data-order replay does not match the checkpoint (random state or last batch differ)")
            torch.set_rng_state(st["torch_rng"])
            if torch.cuda.is_available() and st.get("cuda_rng") is not None:
                torch.cuda.set_rng_state_all(st["cuda_rng"])
            start, log, t0 = st["step"], st["log"], time.time() - 60 * st["minutes"]
            mon.update(st.get("mon") or {})
            if ord_track and "ord_seen" not in (st.get("mon") or {}):
                mon["ord_seen"] = None  # a checkpoint from before the count existed: the end-of-run check is skipped
            print(json.dumps({"resumed_at_step": start, "of": n_steps, "checks": "manifest, config, data, env, code, "
                              "tensors, optimizer order, data order: all match"}), flush=True)
    elif c.get("expect_resume"):
        raise RuntimeError(f"expect_resume: no checkpoint at {ckpt / 'state.pt'} (wrong --name, or the copy is missing)")
    snaps = out_dir / "snaps"
    stale = sorted(q for q in snaps.glob("s[0-9]*") if q.is_dir() and int(q.name[1:]) > start) if snaps.exists() else []
    if stale:  # written by a run we rolled back from: keep them, but out of the way
        aside = snaps / f"_abandoned_from_{start:06d}_{int(time.time())}"
        aside.mkdir()
        for q in stale:
            q.rename(aside / q.name)
        print(json.dumps({"snapshots_moved_aside": [q.name for q in stale], "to": str(aside)}), flush=True)
        if on_ckpt is not None:
            on_ckpt()
    last_ckpt, t_seg = time.time(), time.time()
    snap_steps = {int(f * n_steps) for f in (c.get("snap_fracs") or [])}
    if c.get("snap_every"):
        snap_steps |= set(range(int(c["snap_every"]), n_steps, int(c["snap_every"])))
    stop_step, stop_min = int(c.get("stop_at_step", 0) or 0), float(c.get("stop_after_min", 0) or 0)
    # stop_at_unix: an absolute end time (relay launches set it), so a Modal restart after a preemption keeps the
    # segment's original end instead of getting a fresh stop_after_min
    deadline = float(c.get("stop_at_unix", 0) or 0)
    # Preemption (Modal sends SIGINT; a VM shutdown sends SIGTERM): finish the current step, checkpoint, then raise.
    sig = {"n": None}
    prev = {}
    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            prev[s] = signal.signal(s, lambda num, frame: sig.__setitem__("n", num))
        except ValueError:  # not the main thread: keep the default handlers
            pass

    def ckpt_extra():
        return {"cfg": _identity(c), "data": list(data_hashes), "env": env, "mon": dict(mon, gn=list(mon["gn"]),
                task=list(mon["task"])),
                "code": code, "py_rng": random.getstate(), "twin_rng": twin_rng.getstate(), "last_batch": last_hash}
    try:
        uid = {r["id"]: k for k, u in enumerate(units) for r in u}
        micro_tok = int(c.get("micro_tokens", 0) or 0)
        for step in range(start, n_steps):
            batch = next(gen)
            last_hash = _batch_hash(batch)
            cyg = decoder_io.STYLE == "cygnet"
            perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                     else (random.sample([0, 1], 2) if cyg else None) for r in batch]
            tw = pick_twins(batch, perms, c["perm_twin"], twin_rng)  # second views ride in the same forward call
            if px_cfg and px_cfg["loop_steps"]:  # J: loop depth for this step, seeded by the step (resume stays exact)
                prism_x.STATE["train_T"] = random.Random(c["seed"] * 1000003 + step).randint(1, int(px_cfg["loop_steps"]))
            # Gradient accumulation (cfg micro_tokens > 0, for small GPUs): the batch is split into micro-batches of whole
            # units under a padded-token budget; each micro-batch's loss is weighted by its share of the batch's rows. The
            # random draws above are made for the whole batch, so data order and resume are unchanged.
            groups = _micro_groups(batch, uid, tw, micro_tok) if micro_tok > 0 else [list(range(len(batch)))]
            norm = None
            if aux_norm == "batch":  # whole-batch counts: the same objective whatever the micro-batching
                ac = aux_counts(c, batch, rel_by_row)
                norm = {"rows": len(batch), "cons": ac["cons"], "comp": ac["comp"], "equiv": ac["equiv"],
                        "inv": ac["inv"], "twin": len(tw),
                        "anc": sum(1 for r in batch if c["beta"] > 0 and (r.get("meta") or {}).get("anchor"))}
            opt.zero_grad(set_to_none=True)
            agg, wsum, counts = defaultdict(float), defaultdict(float), Counter()
            for idx in groups:
                mb, mp = [batch[i] for i in idx], [perms[i] for i in idx]
                local = {i: j for j, i in enumerate(idx)}
                mtw = [(local[i], p2) for i, p2 in tw if i in local]
                anc = [i for i, r in enumerate(mb) if c["beta"] > 0 and (r.get("meta") or {}).get("anchor")]
                blg = None
                if anc:  # base-model anchor targets first, without write protection (the base never learned it); the
                    # training forward then comes last, so checkpoint recomputation in backward sees its own block mask
                    wb_on = decoder_io.WRITEBLOCK
                    decoder_io.WRITEBLOCK = False
                    if wb_on:
                        import writeblock as _wb
                        _wb.STATE["enabled"] = False
                    prism_x.STATE["enabled"] = False  # the anchor is the frozen base model: no control plane either
                    try:
                        with torch.no_grad(), model.disable_adapter(), torch.autocast("cuda", dtype=torch.bfloat16):
                            blg = cand_logits(model, ro, [mb[i] for i in anc], dev, perms=[mp[i] for i in anc])
                    finally:
                        prism_x.STATE["enabled"] = True
                    if wb_on:
                        decoder_io.WRITEBLOCK = True
                        _wb.STATE["enabled"] = True
                if px_cfg and not px_loaded and step == 0 and idx is groups[0] and c.get("px_selfcheck", True):
                    _px_selfcheck(model, ro, mb[:4], mp[:4], dev)  # before any update: PRISM-X must equal arm E
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    lg_all = cand_logits(model, ro, mb + [mb[i] for i, _ in mtw], dev, perms=mp + [p for _, p in mtw])
                if px_cfg and step == start:
                    prism_x.check_fired()  # every authority / shadow hook ran in this forward
                if decoder_io.WRITEBLOCK and step == start:
                    import writeblock as _wb
                    if _wb.STATE["applied"] < (_wb.STATE["n_layers"] or 1):
                        raise RuntimeError(f"write-block did not fire: applied {_wb.STATE['applied']} of {_wb.STATE['n_layers']} layers")
                lg = lg_all[:len(mb)]
                twins = [(i, p2, l2) for (i, p2), l2 in zip(mtw, lg_all[len(mb):])]
                kl = None
                if anc:
                    kls = torch.stack([F.kl_div(F.log_softmax(lg[i], -1), F.log_softmax(b, -1), log_target=True,
                                                reduction="sum") for i, b in zip(anc, blg)])
                    kl = kls.sum() / norm["anc"] if norm else kls.mean()
                loss, mterms, mcounts = compute_loss(c, mb, mp, lg, rel_by_row, step, n_steps, dev, kl=kl, twins=twins,
                                                     cyg=cyg, norm=norm)
                w = len(mb) / len(batch)
                if norm:  # the micro-batch losses already add up to the batch loss
                    loss.backward()
                else:
                    (loss * w if len(groups) > 1 else loss).backward()
                for k, v in mterms.items():
                    if v is not None:
                        agg[k] += float(v.detach()) if norm else w * float(v.detach())
                        wsum[k] = 1.0 if norm else wsum[k] + w
                counts.update(mcounts)
            if norm and (counts["cons"] != norm["cons"] or counts["inv"] != norm["inv"]):
                print(json.dumps({"warning": "a relation spans micro-batches", "step": step, "cons": [counts["cons"],
                                  norm["cons"]], "inv": [counts["inv"], norm["inv"]]}), flush=True)
            terms = {k: (torch.tensor(agg[k] / wsum[k]) if wsum[k] > 0 else None)
                     for k in TERMS + ((ORD_TERM,) if lam_ord > 0 else ())}
            if ord_track:
                n_ord_b = sum(1 for r in batch if is_ordinal(r))
                if mon["ord_seen"] is not None:
                    mon["ord_seen"] += n_ord_b
            gn_px = float(torch.norm(torch.stack([q.grad.detach().float().norm() for q in px_params
                                                  if q.grad is not None]))) if px_params else None
            gn = float(torch.nn.utils.clip_grad_norm_(params, 1.0))
            if not math.isfinite(gn):  # one NaN step would turn every weight into NaN (and could reach _ckpt)
                raise FloatingPointError(f"non-finite gradient norm {gn} at step {step}; stopped before the update")
            opt.step()
            sched.step()
            mon["gn"] = (mon["gn"] + [gn])[-200:]
            if terms["task"] is not None:
                mon["task"] = (mon["task"] + [float(terms["task"])])[-200:]
            gn_med = statistics.median(mon["gn"])
            mon["streak"] = mon["streak"] + 1 if gn > 5 * gn_med else 0
            alerts = ["gradient norm above 5x its 200-step median for 20 steps"] if mon["streak"] == 20 else []
            if step >= warm and len(mon["task"]) == 200:
                m = sum(mon["task"]) / 200
                mon["best"] = m if mon["best"] is None else min(mon["best"], m)
                if m > 1.2 * mon["best"] and (mon["last_alert"] is None or step - mon["last_alert"] >= 200):
                    alerts.append(f"200-step task loss {m:.4f} is above 1.2x its best {mon['best']:.4f}")
            for a in alerts:  # logged only; any rollback is a manual rename of _ckpt_good
                mon["last_alert"] = step
                mon["good_frozen"] = True  # _ckpt_good keeps the last pre-alert state for the rest of the run
                print(json.dumps({"ALERT": a, "step": step, "gn": round(gn, 4), "gn_med": round(gn_med, 4)}), flush=True)
            if step % c.get("log_every", 25) == 0 or step == n_steps - 1:
                rec = {"step": step, "of": n_steps,
                       **{k: (round(v.item(), 4) if v is not None else None) for k, v in terms.items()},
                       "n_cons": counts["cons"], "n_inv": counts["inv"], "n_twin": counts["twin"],
                       "n_rel_skipped": counts["rel_skipped"], **({"n_ord": n_ord_b} if ord_track else {}),
                       "lr": sched.get_last_lr()[0], "gn": round(gn, 4), "gn_med": round(gn_med, 4),
                       "clip_frac": round(sum(g > 1.0 for g in mon["gn"]) / len(mon["gn"]), 3),
                       **({"gn_px": round(gn_px, 4)} if gn_px is not None else {}),
                       "min": round((time.time() - t0) / 60, 2)}
                if px_cfg:
                    rec["px"] = prism_x.stats()  # are the new parts switching on (gates, authority size, head weight)?
                log.append(rec)
                print(json.dumps(rec), flush=True)
            done = step + 1
            if done in snap_steps:
                _snapshot(out_dir / "snaps", done, model, tok, {"cfg": c, "steps": n_steps, "fingerprint": fp}, on_ckpt)
            if done < n_steps:
                got = sig["n"]  # read once: a signal landing between two reads could skip the save below
                now = time.time()
                stop = ((stop_step > 0 and done >= stop_step) or (stop_min > 0 and now - t_seg >= 60 * stop_min)
                        or (deadline > 0 and now >= deadline))
                if got is not None or stop or (every > 0 and now - last_ckpt >= 60 * every):
                    _save_ckpt(ckpt, model, opt, sched, done, log, (time.time() - t0) / 60, fp, ckpt_extra(), on_ckpt,
                               tok=tok)
                    last_ckpt = time.time()
                    if (got is None and not mon["good_frozen"] and done - mon["last_good"] >= GOOD_EVERY
                            and (mon["last_alert"] is None or done - mon["last_alert"] > GOOD_QUIET)):
                        _copy_good(ckpt, on_ckpt)
                        mon["last_good"] = done
                if got is not None:  # Modal restarts a preempted input; it resumes from this checkpoint
                    raise KeyboardInterrupt(f"signal {got}: checkpoint saved, next step {done}")
                if stop:  # a planned end of this segment (relay): the next one resumes at `done`
                    print(json.dumps({"stopped_at_step": done, "of": n_steps}), flush=True)
                    return {"stopped": True, "next_step": done, "n_steps": n_steps,
                            "meta": {"cfg": c, "steps": n_steps, "stopped_at_step": done, "log": log}}
        out_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(out_dir)
        prism_x.save(out_dir)  # prism_x.json + prism_x.safetensors; decoder_io.load() re-installs them
        tok.save_pretrained(out_dir)
        meta = {"cfg": c, "rows": len(rows), "relations": len(rels), "relation_types": rel_types, "inv_merged": inv_merged,
                "steps": n_steps, "minutes": round((time.time() - t0) / 60, 2), "log": log, "env": env, "code": code,
                "data": list(data_hashes), **({"prism_x": {**prism_x.PX.meta(), "final": prism_x.stats()}} if px_cfg else {})}
        if ord_track:
            meta["ordinal"] = {**ord_info, "rows_drawn": mon["ord_seen"]}
            if (mon["ord_seen"] is not None and ord_info["rows_drawn_planned"] is not None
                    and mon["ord_seen"] != ord_info["rows_drawn_planned"]):
                print(json.dumps({"ALERT": "ordinal rows drawn differ from the dry run", "drawn": mon["ord_seen"],
                                  "planned": ord_info["rows_drawn_planned"]}), flush=True)
        (out_dir / "train_meta.json").write_text(json.dumps(meta, indent=2))  # written last: marks a finished model
        if on_ckpt is not None:
            on_ckpt()  # the final adapter is durable before the checkpoint goes
        if ckpt.exists():  # the finished adapter supersedes the checkpoint; renamed first, so the delete is all-or-nothing
            gone = ckpt.with_name(ckpt.name + ".done")
            if gone.exists():
                shutil.rmtree(gone)
            ckpt.rename(gone)
            if on_ckpt is not None:
                on_ckpt()
            shutil.rmtree(gone)
            if on_ckpt is not None:
                on_ckpt()
        good = ckpt.with_name(ckpt.name + "_good")
        if good.exists():
            shutil.rmtree(good)
            if on_ckpt is not None:
                on_ckpt()
    finally:
        for s_, h in prev.items():
            signal.signal(s_, h)
    model.eval()
    return {"model": model, "tok": tok, "meta": meta}


if __name__ == "__main__":  # CPU pre-flights of recipe v4: item 10 (A4 unit test) and item 9 (F2 rendered-prompt identity)
    import argparse
    ap = argparse.ArgumentParser(description="python train_decoder.py a4 | f2 --config runs/<c>.json [--adapter <C1 dir>] "
                                 "[--where L --out f2_L.json] [--ref f2_ref.json] | f2cmp REF.json OTHER.json ...")
    ap.add_argument("check", choices=["a4", "f2", "f2cmp"])
    ap.add_argument("records", nargs="*", help="f2cmp: F2 record files; the first is the reference")
    ap.add_argument("--config")
    ap.add_argument("--adapter", default="", help="adds the gate/serve adapter-load path (od_gcp.py predict, di_engine)")
    ap.add_argument("--gate-style", default="", help="od_gcp.py predict --style, when the gate read presets one")
    ap.add_argument("--where", default="", help="label of this machine in the record (e.g. modal-image35, l4-gate)")
    ap.add_argument("--out", default="", help="write this machine's F2 record (6 per-view sha256 + software) here")
    ap.add_argument("--ref", default="", help="an F2 record to compare this machine's record with")
    a = ap.parse_args()
    if a.check == "a4":
        print(json.dumps(a4_selftest()))
    elif a.check == "f2":
        import platform
        rec = f2_record(f2_preflight(json.loads(Path(a.config).read_text()), a.adapter or None, a.gate_style or None),
                        a.where or platform.node())
        if a.out:
            Path(a.out).write_text(json.dumps(rec, indent=1))
        print(json.dumps({"f2": "pass", **rec}))
        if a.ref:
            print(json.dumps(f2_compare({a.ref: json.loads(Path(a.ref).read_text()), a.out or "this machine": rec})))
    else:
        print(json.dumps(f2_compare({p: json.loads(Path(p).read_text()) for p in a.records})))
