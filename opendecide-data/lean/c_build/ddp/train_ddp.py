"""Multi-GPU (DDP) training for OpenDecide, opt-in (PREREG_FINAL A20 c). The pinned trainer is NOT modified.

train_decoder.py is pinned by sha256 (c2c2d1d623cc..., the A16 trainer that fmt1 loader_check checks), so this module
imports it unchanged and builds the DDP train loop FROM ITS SOURCE: inspect.getsource(train_decoder.train) plus the
DDP hunks in HUNKS below (exact string replacements, each anchor must occur exactly once), compiled with the pinned
module's own globals. So every helper the loop calls (check_rows, make_units, batches, pick_twins, aux_counts,
_micro_groups, compute_loss, cand_logits, _save_ckpt, _fingerprint, ...) is the pinned function, called, not copied,
and every line of train() outside the hunks is the pinned line. train_decoder.train itself stays exactly as it was
(the single-GPU default path). `python c_build/ddp/train_ddp.py show` prints the hunks as a diff.

What a DDP run does (every rank runs train() below; launch_ddp starts them, or torchrun + `train_ddp.py train`):
- Every rank draws the SAME global batch (16 rows), option permutations and permutation twins: same seed, same Python
  RNG streams; after the model set-up every rank takes rank 0's Python RNG state; checked every step by an
  all-reduce of a hash). Same steps, warm-up and cosine LR schedule.
- The batch's whole units (a record's related rows) are dealt to the ranks (rank_split: heaviest first, to the
  least-loaded rank), so relation terms never cross ranks; each rank packs its share under the same micro_tokens.
- Every loss term is divided by the WHOLE-batch counts (aux_norm "batch", required): each rank computes them from the
  full batch, so the rank losses add up to the one-GPU batch loss. Gradients are summed over the ranks (one flat
  all-reduce), then clipped at 1.0 and stepped exactly as on one GPU. Logged terms and counts are summed too.
- Rank 0 alone logs, snapshots, checkpoints and saves; the checkpoint adds every rank's RNG state (dropout streams)
  after a check that all ranks hold identical weights. Resume works on the same GPU count, and across GPU counts with
  allow_env_change (env records world_size). Rank > 0 has its own LoRA-dropout stream (the only intended difference
  from one GPU, pure noise; zero when dropout is 0).
Adoption tests: c_build/ddp/adoption_cpu.py (test 1, CPU) and c_build/ddp/PARITY_PLAN.md (test 2, GPU)."""
from __future__ import annotations

import __future__
import functools
import hashlib
import inspect
import json
import linecache
import os
import signal
import sys
import time
import types
from collections import Counter, defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve()
for _d in (_HERE.parent, *_HERE.parents):  # the folder holding the pinned trainer (lean/ locally, /root on Modal)
    if (_d / "train_decoder.py").exists():
        if str(_d) not in sys.path:
            sys.path.insert(0, str(_d))
        break

import torch  # noqa: E402

import decoder_io  # noqa: E402
import train_decoder as td  # noqa: E402

PINNED_TRAINER_SHA = "c2c2d1d623ccd53f64254fb41400f5c952b4e1324d11550a01f170ab25ba04ef"  # train_decoder.py (A16)
CODE_SHA = hashlib.sha256(_HERE.read_bytes()).hexdigest()  # this file: recorded in DDP checkpoints and train_meta


class Dist:
    """The torch.distributed process group a rank runs in (nccl on GPU, gloo on CPU)."""

    def __init__(self):
        import torch.distributed as tdist
        if not tdist.is_initialized():  # torchrun sets RANK / WORLD_SIZE / MASTER_ADDR / MASTER_PORT
            tdist.init_process_group("nccl" if torch.cuda.is_available() else "gloo")
        self.d = tdist
        self.rank, self.world = tdist.get_rank(), tdist.get_world_size()
        self.dev = "cuda" if tdist.get_backend() == "nccl" else "cpu"

    def sum_(self, t):
        self.d.all_reduce(t, op=self.d.ReduceOp.SUM)
        return t

    def max_(self, t):
        self.d.all_reduce(t, op=self.d.ReduceOp.MAX)
        return t

    def barrier(self):
        self.d.barrier()

    def bcast_obj(self, obj):
        box = [obj]
        self.d.broadcast_object_list(box, src=0)
        return box[0]

    def gather_obj(self, obj) -> list:
        out = [None] * self.world
        self.d.all_gather_object(out, obj)
        return out


def rank_split(batch: list, uid: dict, tw: list, world: int) -> list:
    """Whole units of one batch dealt to `world` ranks: heaviest unit first (cost = the pinned _est_tokens of its rows
    and their permutation twins), each to the least-loaded rank (ties: the lower rank). Depends on the batch only, so
    every rank computes the same split. Returns one sorted list of batch indices per rank (a rank may get none)."""
    twin_n = Counter(i for i, _ in tw)
    order, members = [], defaultdict(list)
    for i, r in enumerate(batch):
        u = uid.get(r["id"], ("row", i))
        if u not in members:
            order.append(u)
        members[u].append(i)
    cost = [(sum((1 + twin_n[i]) * td._est_tokens(batch[i]) for i in members[u]), k) for k, u in enumerate(order)]
    load, share = [0] * world, [[] for _ in range(world)]
    for cst, k in sorted(cost, key=lambda x: (-x[0], x[1])):
        j = min(range(world), key=lambda q: (load[q], q))
        load[j] += cst
        share[j] += members[order[k]]
    return [sorted(s) for s in share]


def rank_groups(batch: list, uid: dict, tw: list, micro_tok: int, dist: Dist) -> list:
    """This rank's micro-batches (lists of batch indices): its whole units, packed by the pinned _micro_groups under
    the same micro_tokens budget (all of them in one group when micro_tokens is 0)."""
    mine = rank_split(batch, uid, tw, dist.world)[dist.rank]
    if not mine:
        return []
    if micro_tok <= 0:
        return [mine]
    loc = {i: j for j, i in enumerate(mine)}
    sub = td._micro_groups([batch[i] for i in mine], uid, [(loc[i], p2) for i, p2 in tw if i in loc], micro_tok)
    return [[mine[j] for j in g] for g in sub]


def rank_seed(seed: int, rank: int, step: int = 0) -> int:
    """Seed of rank > 0's torch RNG (LoRA dropout masks): its own stream, so ranks never share masks."""
    return (int(seed) * 1000003 + 7919 * int(rank) + 104729 * int(step)) % (2**63 - 1)


def same_draws(dist: Dist, step: int, last_hash, perms, tw):
    """Stops before any update if the ranks drew different batches, permutations or twins (their sums would mix
    batches): min == max over the ranks of a 48-bit hash (exact in float64)."""
    hv = float(int(hashlib.sha256(json.dumps([last_hash, perms, tw]).encode()).hexdigest()[:12], 16))
    hx = dist.max_(torch.tensor([hv, -hv], dtype=torch.float64, device=dist.dev)).tolist()
    if hx[0] != -hx[1]:
        raise RuntimeError(f"DDP: the ranks drew different batches at step {step} (Python RNG streams differ); "
                           "stopping before any update")


def sum_grads(params: list, dist: Dist):
    """Sum every trained gradient over the ranks (one flat all-reduce). A tensor that got no gradient on any rank stays
    None, as on one GPU (AdamW then skips it); on a rank without it, it counts as zeros."""
    has = torch.tensor([float(p.grad is not None) for p in params], device=dist.dev)
    dist.sum_(has)
    live = [p for p, h in zip(params, has.tolist()) if h > 0]
    if not live:
        return
    flat = torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).reshape(-1).to(dist.dev) for p in live])
    dist.sum_(flat)
    off = 0
    for p in live:
        g = flat[off:off + p.numel()].view_as(p).to(p.device)
        off += p.numel()
        if p.grad is None:
            p.grad = g.clone()
        else:
            p.grad.copy_(g)


COUNT_KEYS = ("cons", "inv", "twin", "rel_skipped", "ord")  # the counts compute_loss returns


def sum_step(agg, wsum, counts, keys, dist: Dist):
    """Logged terms and counts of one step summed over the ranks (each rank holds its micro-batches' sums, already
    divided by the whole-batch counts). A term is present when any rank had it."""
    v = torch.tensor([agg[k] for k in keys] + [wsum[k] for k in keys] + [float(counts[k]) for k in COUNT_KEYS],
                     dtype=torch.float64, device=dist.dev)
    v = dist.sum_(v).tolist()
    n = len(keys)
    agg, wsum = defaultdict(float), defaultdict(float)
    for j, k in enumerate(keys):
        if v[n + j] > 0:
            agg[k], wsum[k] = v[j], 1.0
    return agg, wsum, Counter({k: int(round(v[2 * n + j])) for j, k in enumerate(COUNT_KEYS)})


def ckpt_extra(model, dist: Dist) -> dict:
    """Checkpoint additions (every rank calls this; rank 0 saves): every rank's RNG state (its dropout stream), after a
    check that all ranks hold the same weights. cuda_rng is rank 0's device only, so a one-GPU resume can restore it."""
    tr = td._trainable(model)
    h = hashlib.sha256("".join(td._sha_tensor(p) for p in tr.values()).encode()).hexdigest()
    cuda = torch.cuda.get_rng_state() if torch.cuda.is_available() else None
    got = dist.gather_obj({"h": h, "torch_rng": torch.get_rng_state(), "cuda_rng": cuda})
    if len({g["h"] for g in got}) != 1:
        raise RuntimeError(f"DDP: the ranks hold different weights ({[g['h'][:12] for g in got]}); not saving")
    return {"ddp": {"world_size": dist.world, "code": CODE_SHA,
                    "rank_rng": [{"torch_rng": g["torch_rng"], "cuda_rng": g["cuda_rng"]} for g in got]},
            "cuda_rng": [cuda] if cuda is not None else None}


def restore_rng(st: dict, c: dict, dist: Dist):
    """Resume: this rank's own RNG stream when the checkpoint has the same GPU count; rank 0 takes the one-GPU state
    of another count's checkpoint (or a one-GPU one) and every other rank then starts a fresh stream of its own."""
    sd = st.get("ddp") or {}
    if sd.get("code") not in (None, CODE_SHA) and not c.get("allow_code_change"):
        raise RuntimeError(f"train_ddp.py differs from the checkpoint's ({sd['code'][:12]} -> {CODE_SHA[:12]}); "
                           "set allow_code_change to resume anyway")
    if sd.get("world_size") == dist.world:
        rr = sd["rank_rng"][dist.rank]
        torch.set_rng_state(rr["torch_rng"])
        if torch.cuda.is_available() and rr.get("cuda_rng") is not None:
            torch.cuda.set_rng_state(rr["cuda_rng"])
    elif dist.rank == 0:
        torch.set_rng_state(st["torch_rng"])
        if torch.cuda.is_available() and st.get("cuda_rng"):
            torch.cuda.set_rng_state(st["cuda_rng"][0])
    else:
        torch.manual_seed(rank_seed(c["seed"], dist.rank, st["step"]))


def ckpt_decision(dist: Dist, got, stop: bool, due: bool) -> tuple:
    """One decision for all ranks: any rank's signal, stop point or checkpoint clock."""
    f = dist.max_(torch.tensor([float(got or 0), float(stop), float(due)], dtype=torch.float64, device=dist.dev))
    f = f.tolist()
    return (int(f[0]) or None), bool(f[1]), bool(f[2])


# ---------------------------------------------------------------- the DDP hunks on the pinned train_decoder.train
# (why, old, new): `old` must occur exactly once in inspect.getsource(train_decoder.train). In the built function,
# `_dx` is this module (a keyword-only default), `dist` the process group and `lead` = rank 0.
HUNKS = [
    ("a keyword-only handle on this module", r'''
def train(cfg: dict, data_dir: Path, out_dir: Path, dev="cuda", on_ckpt=None) -> dict:
''', r'''
def train(cfg: dict, data_dir: Path, out_dir: Path, dev="cuda", on_ckpt=None, *, _dx=None) -> dict:
'''),
    ("DDP needs whole-batch normalisation; join the process group", r'''
        raise ValueError(f"aux_norm must be 'micro' or 'batch', got {aux_norm!r}")
''', r'''
        raise ValueError(f"aux_norm must be 'micro' or 'batch', got {aux_norm!r}")
    if aux_norm != "batch":  # DDP: "micro" weights each micro-batch's mean, which depends on the packing
        raise ValueError("ddp needs aux_norm 'batch' (losses normalised by whole-batch counts)")
    dist = _dx.Dist()  # the process group (launch_ddp or torchrun started it)
    lead = dist.rank == 0  # the rank that writes files and logs (snapshots, checkpoints, the model)
'''),
    ("rank 0 loads (and downloads) the base model first", r'''
    model, tok = load(c["base"], dev, **({"revision": c["base_revision"]} if c.get("base_revision") else {}))
''', r'''
    if dist.rank > 0:
        dist.barrier()  # rank 0 loads (and downloads) the base model first; the others then read the cache
    model, tok = load(c["base"], dev, **({"revision": c["base_revision"]} if c.get("base_revision") else {}))
    if dist.rank == 0:
        dist.barrier()
'''),
    ("same start weights on every rank; rank > 0 gets its own dropout stream", r'''
        opt, lambda s: (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm))))
''', r'''
        opt, lambda s: (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm))))
    with torch.no_grad():  # every rank starts from rank 0's weights
        for p in params:
            dist.d.broadcast(p.data, src=0)
    if dist.rank > 0:
        torch.manual_seed(_dx.rank_seed(c["seed"], dist.rank))
    # the model set-up may draw from Python's random (pilot P2: the GPU data stream differs from the CPU replay), so
    # every rank continues rank 0's stream (= a one-GPU run's); same_draws checks it at every step
    random.setstate(dist.bcast_obj(random.getstate()))
'''),
    ("env records the GPU count; rank 0 alone tidies the checkpoint folder", r'''
    env, code, last_hash = _env(), _code(), None
    old = ckpt.with_name(ckpt.name + ".old")
    if not (ckpt / "state.pt").exists() and (old / "state.pt").exists():  # stopped between the two renames
''', r'''
    env, code, last_hash = _env(), _code(), None
    env["world_size"] = dist.world  # a resume on another GPU count needs allow_env_change
    old = ckpt.with_name(ckpt.name + ".old")
    if lead and not (ckpt / "state.pt").exists() and (old / "state.pt").exists():  # stopped between the two renames
'''),
    ("rank 0 alone tidies the checkpoint folder", r'''
    elif (ckpt / "state.pt").exists() and old.exists():  # stopped after the swap, before the clean-up
''', r'''
    elif lead and (ckpt / "state.pt").exists() and old.exists():  # stopped after the swap, before the clean-up
'''),
    ("rank 0 alone tidies the checkpoint folder; the others wait for it", r'''
    if ckpt.with_name(ckpt.name + ".done").exists():  # stopped during the final clean-up (the model was saved)
        shutil.rmtree(ckpt.with_name(ckpt.name + ".done"))
''', r'''
    if lead and ckpt.with_name(ckpt.name + ".done").exists():  # stopped during the final clean-up (model saved)
        shutil.rmtree(ckpt.with_name(ckpt.name + ".done"))
    dist.barrier()  # the checkpoint folder is settled before any rank reads it
'''),
    ("resume: each rank's own RNG stream", r'''
            torch.set_rng_state(st["torch_rng"])
            if torch.cuda.is_available() and st.get("cuda_rng") is not None:
                torch.cuda.set_rng_state_all(st["cuda_rng"])
''', r'''
            _dx.restore_rng(st, c, dist)  # this rank's own dropout stream (a fresh one after a GPU-count change)
'''),
    ("rank 0 alone moves stale snapshots aside", r'''
    stale = sorted(q for q in snaps.glob("s[0-9]*") if q.is_dir() and int(q.name[1:]) > start) if snaps.exists() else []
''', r'''
    stale = (sorted(q for q in snaps.glob("s[0-9]*") if q.is_dir() and int(q.name[1:]) > start)
             if lead and snaps.exists() else [])
'''),
    ("all ranks start the loop together", r'''
    last_ckpt, t_seg = time.time(), time.time()
''', r'''
    dist.barrier()
    last_ckpt, t_seg = time.time(), time.time()
'''),
    ("every rank must hold the same batch, permutations and twins", r'''
            tw = pick_twins(batch, perms, c["perm_twin"], twin_rng)  # second views ride in the same forward call
''', r'''
            tw = pick_twins(batch, perms, c["perm_twin"], twin_rng)  # second views ride in the same forward call
            _dx.same_draws(dist, step, last_hash, perms, tw)  # else the sums below would mix batches
'''),
    ("this rank's whole units of the batch, packed under the same micro_tokens budget", r'''
            groups = _micro_groups(batch, uid, tw, micro_tok) if micro_tok > 0 else [list(range(len(batch)))]
''', r'''
            groups = _dx.rank_groups(batch, uid, tw, micro_tok, dist)
'''),
    ("sum gradients, logged terms and counts over the ranks (before clipping)", r'''
            if norm and (counts["cons"] != norm["cons"] or counts["inv"] != norm["inv"]):
''', r'''
            _dx.sum_grads(params, dist)  # the whole batch's gradient, terms and counts on every rank
            agg, wsum, counts = _dx.sum_step(agg, wsum, counts, TERMS + ((ORD_TERM,) if lam_ord > 0 else ()), dist)
            if norm and lead and (counts["cons"] != norm["cons"] or counts["inv"] != norm["inv"]):
'''),
    ("rank 0 alone prints the step log", r'''
                log.append(rec)
                print(json.dumps(rec), flush=True)
''', r'''
                log.append(rec)
                if lead:
                    print(json.dumps(rec), flush=True)
'''),
    ("rank 0 alone writes snapshots", r'''
            if done in snap_steps:
''', r'''
            if done in snap_steps and lead:
'''),
    ("one checkpoint decision for all ranks; rank 0 saves, with every rank's RNG state", r'''
                if got is not None or stop or (every > 0 and now - last_ckpt >= 60 * every):
                    _save_ckpt(ckpt, model, opt, sched, done, log, (time.time() - t0) / 60, fp, ckpt_extra(), on_ckpt,
                               tok=tok)
                    last_ckpt = time.time()
''', r'''
                got, stop, due = _dx.ckpt_decision(dist, got, stop, every > 0 and now - last_ckpt >= 60 * every)
                if got is not None or stop or due:
                    dx = _dx.ckpt_extra(model, dist)
                    if lead:
                        _save_ckpt(ckpt, model, opt, sched, done, log, (time.time() - t0) / 60, fp,
                                   {**ckpt_extra(), **dx}, on_ckpt, tok=tok)
                    dist.barrier()  # the checkpoint is complete before any rank goes on (or stops)
                    last_ckpt = time.time()
'''),
    ("rank 0 alone copies the good checkpoint", r'''
                        _copy_good(ckpt, on_ckpt)
                        mon["last_good"] = done
''', r'''
                        if lead:
                            _copy_good(ckpt, on_ckpt)
                        mon["last_good"] = done
'''),
    ("rank 0 alone saves the model", r'''
        out_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(out_dir)
        prism_x.save(out_dir)  # prism_x.json + prism_x.safetensors; decoder_io.load() re-installs them
        tok.save_pretrained(out_dir)
''', r'''
        if lead:
            out_dir.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(out_dir)
            prism_x.save(out_dir)  # prism_x.json + prism_x.safetensors; decoder_io.load() re-installs them
            tok.save_pretrained(out_dir)
'''),
    ("meta records the DDP run; the other ranks wait for rank 0's final save", r'''
        (out_dir / "train_meta.json").write_text(json.dumps(meta, indent=2))  # written last: marks a finished model
''', r'''
        meta["ddp"] = {"world_size": dist.world, "code": _dx.CODE_SHA}
        if not lead:
            dist.barrier()  # rank 0 saves the model and removes the checkpoint; the others wait for it
            model.eval()
            return {"model": model, "tok": tok, "meta": meta}
        (out_dir / "train_meta.json").write_text(json.dumps(meta, indent=2))  # written last: marks a finished model
'''),
    ("rank 0 releases the others after the final clean-up", r'''
            if on_ckpt is not None:
                on_ckpt()
    finally:
''', r'''
            if on_ckpt is not None:
                on_ckpt()
        dist.barrier()
    finally:
'''),
]


def _trainer_sha() -> str:
    return hashlib.sha256(Path(td.__file__).read_bytes()).hexdigest()


def patched_source() -> tuple:
    """(pinned source of train_decoder.train, its first line, the DDP source). Refuses a trainer other than the pinned
    one (the hunks and adoption test 1 were made against it) and any hunk whose anchor is not found exactly once."""
    sha = _trainer_sha()
    if sha != PINNED_TRAINER_SHA:
        raise RuntimeError(f"train_decoder.py is {sha[:12]}, not the pinned {PINNED_TRAINER_SHA[:12]}: re-check the DDP "
                           "hunks and re-run adoption test 1 before changing PINNED_TRAINER_SHA")
    lines, first = inspect.getsourcelines(td.train)
    src = new = "".join(lines)
    for why, old, rep in HUNKS:
        old, rep = old[1:], rep[1:]  # each literal starts with a newline
        n = new.count(old)
        if n != 1:
            raise RuntimeError(f"DDP hunk {why!r}: its anchor occurs {n} times in train_decoder.train (need exactly 1)")
        new = new.replace(old, rep)
    return src, first, new


@functools.lru_cache(maxsize=1)
def _built():
    """train_decoder.train with the DDP hunks, as a function of the pinned module (its globals are train_decoder's, so
    every name it calls is the pinned one, and a test's patch of train_decoder.X applies to it as to train())."""
    _, first, new = patched_source()
    fname = f"<train_ddp: train_decoder.train + {len(HUNKS)} DDP hunks>"
    full = "\n" * (first - 1) + new  # unhunked lines before the first hunk keep train_decoder.py's line numbers
    linecache.cache[fname] = (len(full), None, full.splitlines(True), fname)  # tracebacks show the built source
    code = compile(full, fname, "exec", flags=__future__.annotations.compiler_flag, dont_inherit=True)
    scratch = {"__name__": td.__name__}
    exec(code, scratch)  # noqa: S102 (only defines the function; annotations stay strings)
    f = scratch["train"]
    fn = types.FunctionType(f.__code__, vars(td), "train", f.__defaults__, f.__closure__)
    fn.__kwdefaults__ = {"_dx": sys.modules[__name__]}
    fn.__doc__, fn.__module__, fn.__qualname__ = td.train.__doc__, __name__, "train_ddp.train"
    return fn


def train(cfg: dict, data_dir: Path, out_dir: Path, dev="cuda", on_ckpt=None) -> dict:
    """One rank of a DDP run: train_decoder.train's run (same config, batches, steps, schedule, seed and losses; needs
    aux_norm "batch") with the DDP hunks. The process group must be up or its env vars set (launch_ddp / torchrun).
    Rank 0 returns what train_decoder.train returns; the other ranks return their (identical) model and the meta."""
    return _built()(cfg, Path(data_dir), Path(out_dir), dev=dev, on_ckpt=on_ckpt)


def show() -> str:
    """The DDP hunks as a unified diff against the pinned train_decoder.train."""
    import difflib
    src, first, new = patched_source()
    return "".join(difflib.unified_diff(src.splitlines(True), new.splitlines(True), "train_decoder.train (pinned)",
                                        "train_ddp.train (built)", n=1))


# ---------------------------------------------------------------- launcher: N local ranks (one container / machine)

def _ddp_worker(rank, world, port, cfg, data_dir, out_dir, dev, style, req_q, ack_q, res_q, logdir, setup, commit):
    """One rank (a spawned process): joins the process group, runs train(), reports to the launcher. Rank > 0 writes
    its stdout to logdir/rank<r>.log; rank 0 asks the launcher to run on_ckpt (e.g. Modal vol.commit)."""
    import traceback
    from datetime import timedelta
    os.environ.update({"MASTER_ADDR": "127.0.0.1", "MASTER_PORT": str(port), "RANK": str(rank),
                       "WORLD_SIZE": str(world), "LOCAL_RANK": str(rank)})
    if rank > 0:
        sys.stdout = open(Path(logdir) / f"rank{rank}.log", "a", buffering=1)  # noqa: SIM115
    try:
        import torch.distributed as tdist
        cuda = str(dev).startswith("cuda")
        if cuda:
            torch.cuda.set_device(rank)
        # long timeout: the other ranks wait in a collective while rank 0 writes a snapshot or checkpoint
        tdist.init_process_group("nccl" if cuda else "gloo", rank=rank, world_size=world, timeout=timedelta(minutes=60))
        decoder_io.STYLE = style
        if setup is not None:  # tests: install fakes / probes in this process
            setup[0](rank, *setup[1])

        def on_ckpt():
            req_q.put(rank)
            err = ack_q.get()
            if err:
                raise RuntimeError(f"on_ckpt failed in the launcher: {err}")
        res = train(cfg, Path(data_dir), Path(out_dir), dev=dev, on_ckpt=on_ckpt if (commit and rank == 0) else None)
        if rank == 0:
            res_q.put(("ok", {k: v for k, v in res.items() if k not in ("model", "tok")}))
        tdist.barrier()
        tdist.destroy_process_group()
    except KeyboardInterrupt as e:  # a forwarded preemption signal: checkpoint saved, stop like one GPU does
        res_q.put(("signal", f"rank {rank}: {e}"))
        raise SystemExit(3) from None
    except BaseException as e:  # noqa: BLE001
        res_q.put(("error", f"rank {rank}: {type(e).__name__}: {e}\n{traceback.format_exc()[-3000:]}"))
        raise SystemExit(1) from None


def _drain(q, out: list, timeout: float = 0.0):
    import queue
    while True:
        try:
            out.append(q.get(timeout=timeout) if timeout else q.get_nowait())
        except queue.Empty:
            return


def launch_ddp(cfg: dict, data_dir, out_dir, nproc: int, dev: str = "cuda", on_ckpt=None, style=None, logdir=None,
               setup=None, grace_s: float = 30.0) -> dict:
    """Runs train(cfg, ...) on nproc local ranks (spawned processes; nccl on GPU, gloo on CPU) and returns rank 0's
    result without the model ({"stopped", "next_step", "n_steps", "meta"} or {"meta"}). on_ckpt runs HERE, in the
    launcher, whenever rank 0 asks (after each checkpoint, snapshot and the final save). SIGINT / SIGTERM to the launcher
    are forwarded to every rank: they finish the step, rank 0 checkpoints, and the launcher raises KeyboardInterrupt, as
    a one-GPU run does. A rank that fails stops the others (after grace_s) and the launcher raises."""
    import multiprocessing as mp
    import queue
    import socket
    import tempfile
    style = style or decoder_io.STYLE
    logdir = Path(logdir or tempfile.mkdtemp(prefix="od_ddp_"))
    logdir.mkdir(parents=True, exist_ok=True)
    with socket.socket() as sk:
        sk.bind(("127.0.0.1", 0))
        port = sk.getsockname()[1]
    ctx = mp.get_context("spawn")
    req_q, ack_q, res_q = ctx.Queue(), ctx.Queue(), ctx.Queue()
    procs = [ctx.Process(target=_ddp_worker, args=(r, nproc, port, cfg, str(data_dir), str(out_dir), dev, style,
                                                   req_q, ack_q, res_q, str(logdir), setup, on_ckpt is not None),
                         daemon=False) for r in range(nproc)]
    got_sig = {"n": None}

    def fwd(num, frame):
        got_sig["n"] = num
        for q in procs:
            if q.pid and q.is_alive():
                os.kill(q.pid, signal.SIGINT)
    prev = {}
    for sg in (signal.SIGINT, signal.SIGTERM):
        try:
            prev[sg] = signal.signal(sg, fwd)
        except ValueError:  # not the main thread
            pass
    results, failed_at = [], None
    try:
        for q in procs:
            q.start()
        while True:
            try:
                req_q.get(timeout=0.5)
                err = ""
                try:
                    if on_ckpt is not None:
                        on_ckpt()
                except Exception as e:  # noqa: BLE001
                    err = f"{type(e).__name__}: {e}"
                ack_q.put(err)
            except queue.Empty:
                pass
            _drain(res_q, results)
            codes = [q.exitcode for q in procs]
            if all(x is not None for x in codes):
                break
            if failed_at is None and any(x not in (None, 0) for x in codes):
                failed_at = time.time()
            if failed_at is not None and time.time() - failed_at > grace_s:
                for q in procs:
                    if q.is_alive():
                        q.kill()
        for q in procs:
            q.join()
        _drain(res_q, results, timeout=0.2)
    finally:
        for sg, h in prev.items():
            signal.signal(sg, h)
        for q in procs:
            if q.is_alive():
                q.kill()
    codes = [q.exitcode for q in procs]
    ok = [p for kind, p in results if kind == "ok"]
    if all(x == 0 for x in codes) and ok:
        return ok[0]
    msgs = [p for kind, p in results if kind != "ok"]
    if got_sig["n"] is not None or (msgs and all(kind == "signal" for kind, _ in results if kind != "ok")):
        raise KeyboardInterrupt(f"signal {got_sig['n']}: ranks stopped after a checkpoint ({msgs[:2]})")
    raise RuntimeError(f"launch_ddp: rank exit codes {codes}; logs in {logdir}; {' | '.join(msgs)[:6000]}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=(
        "show: print the DDP hunks as a diff against the pinned train_decoder.train | "
        "train: one rank, under torchrun --standalone --nproc_per_node N c_build/ddp/train_ddp.py train --config C "
        "--data-dir D --out-dir O | launch: N local ranks from one process (--nproc N)"))
    ap.add_argument("cmd", choices=["show", "train", "launch"])
    ap.add_argument("--config", default="")
    ap.add_argument("--data-dir", default="data", help="folder holding the config's train_file and rel_file")
    ap.add_argument("--out-dir", default="", help="the model folder")
    ap.add_argument("--dev", default="cuda")
    ap.add_argument("--nproc", type=int, default=0, help="launch: number of ranks (default: every visible GPU)")
    a = ap.parse_args()
    if a.cmd == "show":
        print(show(), end="")
        print(json.dumps({"hunks": len(HUNKS), "trainer_sha256": _trainer_sha(), "train_ddp_sha256": CODE_SHA}))
        raise SystemExit(0)
    if not (a.config and a.out_dir):
        raise SystemExit("--config and --out-dir are required")
    cfg_t = json.loads(Path(a.config).read_text())
    decoder_io.STYLE = cfg_t.get("style") or decoder_io.STYLE
    if a.cmd == "launch":
        n = a.nproc or (torch.cuda.device_count() if a.dev.startswith("cuda") else 2)
        out = launch_ddp(cfg_t, Path(a.data_dir), Path(a.out_dir), n, dev=a.dev, style=decoder_io.STYLE)
    else:
        import torch.distributed as tdist
        if a.dev.startswith("cuda"):
            torch.cuda.set_device(int(os.environ.get("LOCAL_RANK", 0)))
        tdist.init_process_group("nccl" if a.dev.startswith("cuda") else "gloo")
        if tdist.get_rank() > 0:
            sys.stdout = open(os.devnull, "w")  # noqa: SIM115 (rank 0 logs)
        out = train(cfg_t, Path(a.data_dir), Path(a.out_dir), dev=a.dev)
        tdist.barrier()
        tdist.destroy_process_group()
    print(json.dumps({k: v for k, v in out.items() if k in ("stopped", "next_step", "n_steps")}))
