"""Multi-GPU (DDP) training on Modal: a separate app; the pinned modal_od.py and train_decoder.py are untouched.

It reuses modal_od's image (image35: same pinned packages and data mount), Volume, secrets, launch checks and target
regex, and adds c_build/ddp/train_ddp.py (+ modal_od.py, imported in the container) to the image. One container holds
2, 4 or 8 H100s ("H100!": never an H200, as the one-GPU relay); train_ddp.launch_ddp starts one NCCL rank per GPU.
Same frozen config, run identity and checkpoint folder as modal_od.py::relay, so a run can move between GPU counts
(1 <-> 4 <-> 8) with --allow-env-change. Not used for a real run until adoption tests 1 (c_build/ddp/ADOPTION_CPU.json)
and 2 (ddp_parity below; c_build/ddp/PARITY_PLAN.md) both pass (PREREG_FINAL A20 c).

  modal run c_build/ddp/modal_ddp.py::ddp_parity                       # adoption test 2 (<= $4; needs a GO)
  modal run --detach c_build/ddp/modal_ddp.py::relay_ddp --config runs/q35_4b_c_r1.json --gpus 4
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path

import modal

_HERE = Path(__file__).resolve()
LEAN = next((d for d in (_HERE.parent, *_HERE.parents) if (d / "modal_od.py").exists()), _HERE.parent)
if str(LEAN) not in sys.path:
    sys.path.insert(0, str(LEAN))
import modal_od as od  # noqa: E402  (pinned; only read from here)

app = modal.App("opendecide-ddp")
vol = od.vol
SECRETS = od.SECRETS
image_ddp = (od.image35
             .add_local_file(LEAN / "c_build/ddp/train_ddp.py", "/root/train_ddp.py")
             .add_local_file(LEAN / "modal_od.py", "/root/modal_od.py"))
USD_PER_GPU_H = 4.09  # C_TRAIN_RECIPE.md section 4 (H100 with its CPU and memory share)
GPU_FN_KW = {2: dict(gpu="H100!:2", cpu=4.0, memory=32768), 4: dict(gpu="H100!:4", cpu=8.0, memory=65536),
             8: dict(gpu="H100!:8", cpu=16.0, memory=131072)}  # memory: every rank > 0 loads the base model at once


def _ddp_impl(name: str, cfg: dict, nproc: int) -> dict:
    import decoder_io
    decoder_io.STYLE = cfg.get("style", "od")
    import torch
    import train_ddp
    if torch.cuda.device_count() != nproc:
        raise RuntimeError(f"expected {nproc} GPUs, the container has {torch.cuda.device_count()}")
    res = train_ddp.launch_ddp(cfg, Path("/root/data"), Path(f"/vol/models/{name}"), nproc, dev="cuda",
                               on_ckpt=vol.commit, style=decoder_io.STYLE, logdir=Path(f"/tmp/ddp_logs_{name}"))
    vol.commit()
    if res.get("stopped"):
        return {"stopped": True, "next_step": res["next_step"], "n_steps": res["n_steps"], "meta": res["meta"]}
    return {"stopped": False, "meta": res["meta"]}


@app.function(image=image_ddp, volumes={"/vol": vol}, secrets=SECRETS, timeout=10 * 3600, **GPU_FN_KW[2])
def train_relay35_x2(name: str, cfg: dict) -> dict:
    """modal_od.train_relay35 on 2 H100s (DDP): the cheapest speed-up (least idle GPU time per step)."""
    return _ddp_impl(name, cfg, 2)


@app.function(image=image_ddp, volumes={"/vol": vol}, secrets=SECRETS, timeout=10 * 3600, **GPU_FN_KW[4])
def train_relay35_x4(name: str, cfg: dict) -> dict:
    """modal_od.train_relay35 on 4 H100s (DDP): one segment of a relay run, same config, same checkpoint folder."""
    return _ddp_impl(name, cfg, 4)


@app.function(image=image_ddp, volumes={"/vol": vol}, secrets=SECRETS, timeout=10 * 3600, **GPU_FN_KW[8])
def train_relay35_x8(name: str, cfg: dict) -> dict:
    """modal_od.train_relay35 on 8 H100s (DDP)."""
    return _ddp_impl(name, cfg, 8)


DDP_FNS = {2: train_relay35_x2, 4: train_relay35_x4, 8: train_relay35_x8}


@app.local_entrypoint()
def relay_ddp(config: str, gpus: int = 4, expect_resume: bool = False, stop_after_min: float = 0.0,
              stop_at_step: int = 0, name_suffix: str = "", log_every: int = 0, allow_env_change: bool = False):
    """modal_od.py::relay on 2, 4 or 8 H100s of one container (DDP), built exactly as relay() builds its config:
      modal run --detach c_build/ddp/modal_ddp.py::relay_ddp --config runs/q35_4b_c_r1.json --gpus 4
    --allow-env-change lets a segment resume a checkpoint written on another GPU count (1 <-> 4 <-> 8)."""
    if gpus not in DDP_FNS:
        raise SystemExit(f"--gpus must be one of {sorted(DDP_FNS)}")
    cfg = json.loads((LEAN / config).read_text())
    missing = [k for k in od.RELAY_REQUIRED if k not in cfg]
    if missing:
        raise SystemExit(f"{config}: missing keys {missing} (every key must be written out)")
    od._launch_checks(config, cfg)
    if cfg.get("aux_norm") != "batch":
        raise SystemExit(f"{config}: DDP needs aux_norm 'batch'")
    name = cfg.pop("name")
    if name_suffix:
        if not re.fullmatch(r"_[A-Za-z0-9_]+", name_suffix):
            raise SystemExit(f"--name-suffix must look like _pA1 (underscore, letters, digits), not {name_suffix!r}")
        name += name_suffix
    if cfg["targets"] == "QWEN35":
        cfg["targets"] = od.QWEN35_TARGETS
    cfg.update({"no_overwrite": True, "expect_resume": expect_resume, "stop_at_step": stop_at_step,
                "stop_at_unix": time.time() + 60 * stop_after_min if stop_after_min > 0 else 0})
    if log_every > 0:
        cfg["log_every"] = log_every
    if allow_env_change:
        cfg["allow_env_change"] = True
    res = DDP_FNS[gpus].remote(name, cfg)
    (LEAN / "logs").mkdir(exist_ok=True)
    tag = f"stopped_at_{res['next_step']}" if res["stopped"] else "final"
    (LEAN / f"logs/relay_{name}_x{gpus}_{tag}.json").write_text(json.dumps(res["meta"], indent=2, default=str))
    print(json.dumps({"name": name, "gpus": gpus, "stopped": res["stopped"], "next_step": res.get("next_step"),
                      "of": res.get("n_steps")}))


# ---- adoption test 2 (c_build/ddp/PARITY_PLAN.md): 50 steps, 1 x H100 (arms A and B) vs 4 x H100 (arm C), <= $4
PARITY_DIR = "pilot_ddp_parity_"  # /vol/models/pilot_ddp_parity_<arm>: pilot names only, never a real run's folder
PARITY_OUT = LEAN / "c_build/ddp/parity_data"


def parity_sample(c1_cfg: dict, keep_1_in: int, out: Path = PARITY_OUT) -> dict:
    """On the laptop, before any container: a fixed sample of C1's training rows (every row whose call_id's sha1 falls
    in 1 of keep_1_in buckets, so whole units), and the relations among them. Both containers get these exact bytes."""
    out.mkdir(parents=True, exist_ok=True)
    pat, ids, n = re.compile(r'"call_id":\s*"((?:[^"\\]|\\.)*)"'), set(), 0
    with open(LEAN / "data" / c1_cfg["train_file"]) as f, open(out / "mini_train.jsonl", "w") as g:
        for line in f:
            m = pat.search(line)
            if m is None:
                raise RuntimeError("a training row without call_id")
            if int(hashlib.sha1(m.group(1).encode()).hexdigest()[:8], 16) % keep_1_in == 0:
                r = json.loads(line)
                if r["call_id"] != json.loads(f'"{m.group(1)}"'):  # the regex found the row's own call_id
                    raise RuntimeError(f"{r['id']}: call_id regex mismatch")
                g.write(line if line.endswith("\n") else line + "\n")
                ids.add(r["id"])
                n += 1
    k = 0
    with open(LEAN / "data" / c1_cfg["rel_file"]) as f, open(out / "mini_rel.jsonl", "w") as g:
        for line in f:
            x = json.loads(line)
            if x["a"] in ids and x["b"] in ids:
                g.write(line if line.endswith("\n") else line + "\n")
                k += 1
    files = {p: (out / p).read_bytes() for p in ("mini_train.jsonl", "mini_rel.jsonl")}
    return {"rows": n, "relations": k, "keep_1_in": keep_1_in, "files": files,
            "sha256": {p: hashlib.sha256(b).hexdigest() for p, b in files.items()}}


def _parity_setup(cfg: dict, files: dict, work: Path = Path("/tmp/parity")) -> tuple:
    """Inside a container: the sample files, and C1's adapter as init when this account's Volume has it."""
    import torch.distributed  # noqa: F401  (imported before the seed in every arm, as in a DDP rank)
    work.mkdir(parents=True, exist_ok=True)
    for p, b in files.items():
        (work / p).write_bytes(b)
    c = {**cfg, "train_file": "mini_train.jsonl", "rel_file": "mini_rel.jsonl"}
    init = c.get("init_adapter")
    if init and not Path(init).exists():
        c.pop("init_adapter")
        init = None
    return c, work, (init or "fresh LoRA")


@app.function(image=image_ddp, gpu="H100!", volumes={"/vol": vol}, secrets=SECRETS, timeout=12 * 60,
              single_use_containers=True)
def ddp_parity_x1(cfg: dict, files: dict, tag: str, micro_tokens: int) -> dict:
    """Arm A (micro_tokens 8192) or B (6144: the same objective under aux_norm "batch", other packing, so other bf16
    shapes and dropout masks: the noise control) on one H100, through the unchanged one-GPU train_decoder.train, in
    its own container (a fresh process, as a relay segment)."""
    t_start = time.time()
    vol.reload()
    import decoder_io
    decoder_io.STYLE = cfg.get("style", "od")
    import train_decoder as td
    c, work, init = _parity_setup({**cfg, "micro_tokens": int(micro_tokens)}, files)
    t = time.time()
    res = td.train(c, work, od._pilot_dir(PARITY_DIR + tag), on_ckpt=vol.commit)
    vol.commit()
    return {"init": init, "gpu": od._gpu_info().get("gpu"), "gpus": 1, "container_s": round(time.time() - t_start, 1),
            "s": round(time.time() - t, 1), "micro_tokens": int(micro_tokens), "stopped": res.get("stopped"),
            "n_steps": res.get("n_steps"), "log": res["meta"]["log"]}


def _parity_xn(cfg: dict, files: dict, tag: str, nproc: int) -> dict:
    t_start = time.time()
    vol.reload()
    import decoder_io
    decoder_io.STYLE = cfg.get("style", "od")
    import torch
    import train_ddp
    if torch.cuda.device_count() != nproc:
        raise RuntimeError(f"expected {nproc} GPUs, the container has {torch.cuda.device_count()}")
    c, work, init = _parity_setup(cfg, files)
    t = time.time()
    res = train_ddp.launch_ddp(c, work, od._pilot_dir(PARITY_DIR + tag), nproc, dev="cuda", on_ckpt=vol.commit,
                               style=decoder_io.STYLE, logdir=Path(f"/tmp/ddp_logs_{tag}"))
    vol.commit()
    return {"init": init, "gpu": od._gpu_info().get("gpu"), "gpus": nproc, "container_s": round(time.time() - t_start, 1),
            "s": round(time.time() - t, 1), "micro_tokens": c.get("micro_tokens"), "stopped": res.get("stopped"),
            "n_steps": res.get("n_steps"), "log": res["meta"]["log"]}


@app.function(image=image_ddp, volumes={"/vol": vol}, secrets=SECRETS, timeout=8 * 60, single_use_containers=True,
              **GPU_FN_KW[4])
def ddp_parity_x4(cfg: dict, files: dict, tag: str = "C") -> dict:
    """Arm C: the same config on 4 H100s through train_ddp.launch_ddp (4 NCCL ranks)."""
    return _parity_xn(cfg, files, tag, 4)


@app.function(image=image_ddp, volumes={"/vol": vol}, secrets=SECRETS, timeout=7 * 60, single_use_containers=True,
              **GPU_FN_KW[8])
def ddp_parity_x8(cfg: dict, files: dict, tag: str = "C8") -> dict:
    """Optional arm C8 (8 H100s), run on its own with --gpus 8 --reuse-x1 (arms A and B from an earlier result)."""
    return _parity_xn(cfg, files, tag, 8)


@app.function(image=image_ddp, volumes={"/vol": vol}, timeout=10 * 60)
def ddp_parity_state(tags: list) -> dict:
    """The arms' stop checkpoints (step 50): ||W_x - W_A|| / ||W_A|| of the trained tensors, and the data stream
    (last batch hash and Python RNG state at the stop step: equal = the arms trained on the same batches)."""
    import torch
    from safetensors.torch import load_file
    vol.reload()
    w, st = {}, {}
    for t in tags:
        d = Path(f"/vol/models/{PARITY_DIR}{t}/_ckpt")
        w[t] = load_file(str(d / "trainable.safetensors"))
        s = torch.load(d / "state.pt", map_location="cpu", weights_only=False)
        st[t] = {"step": s["step"], "last_batch": s["last_batch"],
                 "py_rng": hashlib.sha256(repr(s["py_rng"]).encode()).hexdigest()[:16],
                 "world_size": (s.get("ddp") or {}).get("world_size", 1)}
    ref = w[tags[0]]
    nr = sum(float(ref[k].double().pow(2).sum()) for k in ref) ** 0.5
    out = {"state": st, "weights": {}}
    for t in tags[1:]:
        if set(w[t]) != set(ref):
            out["weights"][t] = {"error": "different tensor names"}
            continue
        d = sum(float((w[t][k].double() - ref[k].double()).pow(2).sum()) for k in ref) ** 0.5
        out["weights"][t] = {"rel_l2_vs_" + tags[0]: d / max(nr, 1e-30)}
    return out


def parity_verdict(logs: dict, state: dict, cand: str = "C", k: float = 1.5, eps_mean: float = 1e-3,
                   eps_max: float = 2e-3, gross: float = 0.05) -> dict:
    """The PARITY_PLAN.md rule. Per step s, d_X(s) = |X(s) - A(s)| / |A(s)|. The candidate passes if: the data stream
    is the same (last batch and Python RNG state at step 50; lr, n_cons, n_inv, n_twin, n_ord, n_rel_skipped at every
    step); for loss, task, every consistency term present and gn: mean_s d_C <= k mean_s d_B + eps_mean and
    max_s d_C <= k max_s d_B + eps_max; no step has d_C(loss) > gross; and the step-50 weights: ||C - A|| <= k ||B - A||
    + 1e-4 ||A||. A different data stream makes the test INCONCLUSIVE (rerun after fixing it), not a fail."""
    A, B, C = ({r["step"]: r for r in logs[t]} for t in ("A", "B", cand))
    steps = sorted(A)
    sa, sb, sc = (state["state"].get(t, {}) for t in ("A", "B", cand))
    out = {"steps": len(steps), "same_steps": sorted(B) == steps == sorted(C), "metrics": {}}
    order_keys = ("lr", "n_cons", "n_inv", "n_twin", "n_ord", "n_rel_skipped")
    out["same_data_order"] = all(A[s].get(q) == X[s].get(q) for s in steps for X in (B, C) for q in order_keys
                                 if s in X)
    out["same_stream"] = bool(sa) and all(sa.get(q) == x.get(q) for x in (sb, sc) for q in ("step", "last_batch",
                                                                                         "py_rng"))
    ok = out["same_steps"] and out["same_data_order"]
    for m in ("loss", "task", "cons", "inv", "perm", "ord", "kl", "gn"):
        pts = [(A[s].get(m), B.get(s, {}).get(m), C.get(s, {}).get(m)) for s in steps]
        pts = [(a, b, c) for a, b, c in pts if None not in (a, b, c) and abs(a) > 1e-8]
        if not pts:
            continue
        dB = [abs(b - a) / abs(a) for a, b, _ in pts]
        dC = [abs(c - a) / abs(a) for a, _, c in pts]
        r = {"n": len(pts), "mean_dB": sum(dB) / len(dB), "mean_dC": sum(dC) / len(dC), "max_dB": max(dB),
             "max_dC": max(dC)}
        r["pass"] = r["mean_dC"] <= k * r["mean_dB"] + eps_mean and r["max_dC"] <= k * r["max_dB"] + eps_max
        if m == "loss":
            r["gross_ok"] = r["max_dC"] <= gross
            r["pass"] = r["pass"] and r["gross_ok"]
        out["metrics"][m] = r
        ok = ok and r["pass"]
    wb, wc = (state["weights"].get(t, {}).get("rel_l2_vs_A") for t in ("B", cand))
    out["weights"] = {"B": wb, cand: wc, "pass": wb is not None and wc is not None and wc <= k * wb + 1e-4}
    out["pass"] = bool(ok and out["weights"]["pass"] and out["same_stream"])
    out["verdict"] = "PASS" if out["pass"] else ("INCONCLUSIVE (data stream differs)" if not
                                                 (out["same_stream"] and out["same_data_order"]) else "FAIL")
    return out


def _sps(log: list, lo: int = 10) -> float | None:
    """Seconds per step from the log's cumulative minutes (steps lo .. last)."""
    m = {r["step"]: r["min"] for r in log}
    hi = max(m) if m else -1
    return None if hi <= lo or lo not in m else round((m[hi] - m[lo]) * 60 / (hi - lo), 3)


def parity_cfg(config: str, c1_config: str, steps: int, seed: int) -> dict:
    """Round 1's frozen draft with its FILL keys removed: every loss setting unchanged, C1's data files, epochs 1.0 on
    the sample, a fixed seed, stop at `steps`, log every step, no periodic checkpoints or snapshots."""
    cfg = json.loads((LEAN / config).read_text())
    c1 = json.loads((LEAN / c1_config).read_text())
    cfg.pop("name", None)
    drop = [k for k, v in cfg.items() if isinstance(v, str) and v.startswith("FILL")] + [
        "expect_ord_rows", "expect_kd_targets", "expect_kd_full", "snap_every", "snap_fracs"]
    for k in drop:
        cfg.pop(k, None)
    cfg.update({"train_file": c1["train_file"], "rel_file": c1["rel_file"], "seed": int(seed), "epochs": 1.0,
                "resume": False, "ckpt_every_min": 0, "stop_at_step": int(steps), "log_every": 1})
    if cfg.get("targets") == "QWEN35":
        cfg["targets"] = od.QWEN35_TARGETS
    return cfg


@app.local_entrypoint()
def ddp_parity(config: str = "runs/q35_4b_c_r1.json", c1_config: str = "runs/q35_4b_main.json", steps: int = 50,
               keep_1_in: int = 300, seed: int = 20261006, gpus: int = 4, reuse_x1: bool = False,
               r1_steps: int = 8880, cap_usd: float = 4.0):
    """Adoption test 2 (PREREG_FINAL A20 c; c_build/ddp/PARITY_PLAN.md). Round 1's loss settings on a fixed sample of
    C1's training rows (about 1/keep_1_in, whole units), `steps` steps each, logged every step, in parallel containers:
    A = 1 x H100 at micro_tokens 8192, B = 1 x H100 at 6144 (noise control), C = 4 x H100 DDP at 8192. Refuses to start
    if the timeouts allow more than cap_usd. Writes c_build/ddp/PARITY_RESULT.json (C8: PARITY_RESULT_x8.json).
    --gpus 8 --reuse-x1 runs only arm C8 and compares it with A and B of PARITY_RESULT.json (same sample, config)."""
    if gpus not in (4, 8) or (gpus == 8) != bool(reuse_x1):
        raise SystemExit("use --gpus 4, or --gpus 8 --reuse-x1 (after a --gpus 4 run)")
    cand, fn_n = ("C", ddp_parity_x4) if gpus == 4 else ("C8", ddp_parity_x8)
    worst = (0 if reuse_x1 else 2 * 12 / 60 * USD_PER_GPU_H) + (8 if gpus == 4 else 7) / 60 * USD_PER_GPU_H * gpus
    if worst > cap_usd:
        raise SystemExit(f"worst case ${worst:.2f} (every container to its timeout) is over the ${cap_usd} cap")
    cfg = parity_cfg(config, c1_config, steps, seed)
    if od._data_ignore(Path(cfg["train_file"])) or od._data_ignore(Path(cfg["rel_file"])):
        raise SystemExit("C1's data files are not in the image's data mount")
    sample = parity_sample(json.loads((LEAN / c1_config).read_text()), int(keep_1_in))
    files = sample.pop("files")
    print(json.dumps({"sample": sample, "n_steps": -(-sample["rows"] // cfg["batch"]), "worst_usd": round(worst, 2)}))
    prev = json.loads((LEAN / "c_build/ddp/PARITY_RESULT.json").read_text()) if reuse_x1 else None
    if prev is not None and (prev["data"]["sha256"] != sample["sha256"] or prev["cfg"] != json.loads(json.dumps(cfg))):
        raise SystemExit("--reuse-x1: PARITY_RESULT.json has another sample or config")
    t0 = time.time()
    fa = fb = None
    if prev is None:
        fa, fb = (ddp_parity_x1.spawn(cfg, files, t, mt) for t, mt in (("A", 8192), ("B", 6144)))
    fc = fn_n.spawn(cfg, files, cand)
    arms = dict(prev["arms"]) if prev else {"A": fa.get(), "B": fb.get()}
    arms[cand] = fc.get()
    logs = {t: a.pop("log") for t, a in arms.items() if "log" in a}
    if prev:
        logs.update({t: prev["logs"][t] for t in ("A", "B")})
    state = ddp_parity_state.remote(["A", "B", cand])
    v = parity_verdict(logs, state, cand)
    v["same_init"] = len({a.get("init") for a in arms.values()}) == 1
    v["pass"] = v["pass"] and v["same_init"]
    sps = {t: _sps(logs[t]) for t in logs}
    usd = {t: round(a["container_s"] / 3600 * USD_PER_GPU_H * a["gpus"], 2) for t, a in arms.items()
           if not (prev and t in ("A", "B"))}
    proj = None
    if sps.get("A") and sps.get(cand):
        g = arms[cand]["gpus"]
        proj = {"r1_steps": r1_steps, "speedup": round(sps["A"] / sps[cand], 2),
                "efficiency": round(sps["A"] / sps[cand] / g, 2),
                "hours_x1": round(r1_steps * sps["A"] / 3600, 2), f"hours_x{g}": round(r1_steps * sps[cand] / 3600, 2),
                "usd_x1": round(r1_steps * sps["A"] / 3600 * USD_PER_GPU_H, 1),
                f"usd_x{g}": round(r1_steps * sps[cand] / 3600 * USD_PER_GPU_H * g, 1),
                "note": "steps only (C1 rows; round 1's prompts are longer); add start-up, snapshots, checkpoints"}
    res = {"test": f"PREREG_FINAL A20 (c) adoption test 2: 1 x H100 vs {gpus} x H100, per-step loss within bf16 noise",
           "pass": v["pass"], "verdict": v, "s_per_step": sps, "projection_round1": proj, "usd": usd,
           "data": sample, "cfg": cfg, "arms": arms, "state": state, "logs": logs, "wall_s": round(time.time() - t0, 1)}
    out = LEAN / ("c_build/ddp/PARITY_RESULT.json" if gpus == 4 else "c_build/ddp/PARITY_RESULT_x8.json")
    out.write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({"pass": res["pass"], "verdict": v["verdict"], "s_per_step": sps, "projection_round1": proj,
                      "usd": usd, "wrote": str(out)}))
