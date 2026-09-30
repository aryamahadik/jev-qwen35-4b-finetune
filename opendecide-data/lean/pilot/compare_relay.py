"""Relay proof test verdict (FINETUNE_PLAN.md 4.2, logs/relay_protocol.md test C), on the laptop, CPU only.

  ../.venv/bin/python pilot/compare_relay.py --a1 handoff/pA1_300/_ckpt --a2 handoff/pA2_300/_ckpt \
      --b handoff/pB_300/_ckpt --b-resume-log logs/pilot/relay_pB_seg2.log --resume-step 150 \
      --a1-run-log logs/pilot/relay_pA1.log --a2-run-log logs/pilot/relay_pA2.log

A1 and A2 are straight runs to the same step on two accounts (their difference is the noise floor); B stopped half way,
was copied to another account and resumed. Each run is a checkpoint folder (trainable.safetensors, state.pt and
manifest.json) or a trainable.safetensors file; its log comes from --X-log (a relay JSON meta with "log", or a text
log of the trainer's JSON lines) or else from the folder's state.pt.

Exact checks (any difference fails): the logged steps, lr and "of" and every n_* count at every logged step; lr against
the schedule formula (when state.pt holds the config); the step, last-batch hash, fingerprint and random states in
state.pt (and the CPU replay's hash, --expect-last-batch); every folder's files against its manifest; B's resumed line;
A1 and A2 ran straight (no resumed_at_step line in their tee logs, --a1-run-log/--a2-run-log: a preemption restart
adds its own resume error to the noise floor and must be rerun, not compared).
Noise checks: d(X,Y) = ||θX - θY||2 / ||θA1||2 over all trainable tensors; g(X,Y) = mean |loss_X - loss_Y| over the
logged steps --lo..--hi (150-299). PASS if d(A1,B) <= 1.5 d(A1,A2) and g(A1,B) <= 1.5 g(A1,A2); if A1 and A2 are
bit-identical, B must be too. The report also gives A1's loss trend (mean of the first vs last 50 logged steps).

Handoff check of one copied checkpoint (manifest, step, optional CPU-replay batch hash):
  ../.venv/bin/python pilot/compare_relay.py --check handoff/pB_150/_ckpt --step 150 --expect-last-batch <hash>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

STATE_KEYS = ("step", "last_batch", "fingerprint", "py_rng", "twin_rng")


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def manifest_problems(folder: Path) -> list:
    """Files missing or changed against the folder's manifest.json (a bad copy between accounts)."""
    m = folder / "manifest.json"
    if not m.exists():
        return [f"{folder}: no manifest.json"]
    files = json.loads(m.read_text())["files"]
    return [f"{folder}/{f}: missing or changed" for f, h in files.items() if not (folder / f).exists() or _sha(folder / f) != h]


def load_run(path: str, log_path: str = "") -> dict:
    """{"tensors", "state" (or None), "log", "folder" (or None)} of one run."""
    import torch
    from safetensors.torch import load_file
    p = Path(path)
    folder = p if p.is_dir() else None
    st_file = (folder / "trainable.safetensors") if folder else p
    state = None
    if folder and (folder / "state.pt").exists():
        state = torch.load(folder / "state.pt", map_location="cpu", weights_only=False)
    log = load_log(log_path) if log_path else list((state or {}).get("log") or [])
    return {"tensors": load_file(str(st_file)), "state": state, "log": log, "folder": folder}


def load_log(path: str) -> list:
    """Log records from a relay JSON meta ({"log": [...]}) or from a text log of JSON lines."""
    text = Path(path).read_text()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and isinstance(obj.get("log"), list):
            return obj["log"]
    except json.JSONDecodeError:
        pass
    out = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{") and '"step"' in line and '"lr"' in line:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(rec, dict) and "step" in rec:
                out.append(rec)
    return out


def rel_dist(x: dict, y: dict, ref: dict) -> float:
    """||x - y||2 / ||ref||2 over all tensors (float64)."""
    if set(x) != set(y) or set(x) != set(ref):
        raise ValueError(f"trainable tensor names differ: {sorted(set(x) ^ set(y) | set(x) ^ set(ref))[:5]}")
    num = den = 0.0
    for k in ref:
        if x[k].shape != y[k].shape:
            raise ValueError(f"{k}: shapes differ {tuple(x[k].shape)} vs {tuple(y[k].shape)}")
        num += float(((x[k].double() - y[k].double()) ** 2).sum())
        den += float((ref[k].double() ** 2).sum())
    return math.sqrt(num) / math.sqrt(den)


def loss_gap(la: list, lb: list, lo: int, hi: int, key: str = "loss") -> tuple:
    """(mean |loss difference|, n steps) over the logged steps in [lo, hi] present in both logs."""
    a = {r["step"]: r.get(key) for r in la if lo <= r["step"] <= hi and r.get(key) is not None}
    b = {r["step"]: r.get(key) for r in lb if lo <= r["step"] <= hi and r.get(key) is not None}
    common = sorted(set(a) & set(b))
    if not common:
        return None, 0
    return sum(abs(a[s] - b[s]) for s in common) / len(common), len(common)


def lr_factor(s: int, n_steps: int) -> float:
    """train_decoder's LambdaLR factor at scheduler step s (5% linear warm-up, then cosine to 0)."""
    warm = int(0.05 * n_steps)
    return (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm)))


def exact_log_problems(logs: dict, hi: int, base_lr=None) -> list:
    """Logged steps, lr, "of" and n_* counts identical across runs (up to step hi); lr equal to the schedule."""
    probs = []
    by = {name: {r["step"]: r for r in log if r["step"] <= hi} for name, log in logs.items()}
    names = list(by)
    ref = names[0]
    for name in names[1:]:
        if set(by[name]) != set(by[ref]):
            diff = sorted(set(by[name]) ^ set(by[ref]))
            probs.append(f"logged steps differ {ref} vs {name}: {diff[:10]}")
    for s in sorted(set.intersection(*(set(v) for v in by.values()))):
        recs = {n: by[n][s] for n in names}
        keys = {"lr", "of"} | {k for r in recs.values() for k in r if k.startswith("n_")}
        for k in sorted(keys):
            vals = {n: r.get(k) for n, r in recs.items()}
            if len(set(map(repr, vals.values()))) > 1:
                probs.append(f"step {s} {k}: {vals}")
        r0 = recs[ref]
        if base_lr is not None and r0.get("of") and r0.get("lr") is not None:
            want = base_lr * lr_factor(s + 1, int(r0["of"]))  # logged after sched.step(): the next step's lr
            if not math.isclose(r0["lr"], want, rel_tol=1e-9, abs_tol=0.0):
                probs.append(f"step {s} lr {r0['lr']!r} != schedule {want!r}")
    return probs


def state_problems(states: dict, expect_last_batch: str = "") -> list:
    """step, last batch hash, fingerprint and random states identical across the runs that have a state.pt."""
    probs = []
    have = {n: s for n, s in states.items() if s is not None}
    if not have:
        return probs
    names = list(have)
    for k in STATE_KEYS:
        vals = {n: have[n].get(k) for n in names}
        if len({repr(v) for v in vals.values()}) > 1:
            shown = {n: (v if k in ("step", "last_batch") else hashlib.sha256(repr(v).encode()).hexdigest()[:12])
                     for n, v in vals.items()}
            probs.append(f"state.pt {k} differs: {shown}")
    if expect_last_batch:
        for n in names:
            if have[n].get("last_batch") != expect_last_batch:
                probs.append(f"{n}: last_batch {have[n].get('last_batch')} != CPU replay {expect_last_batch}")
    return probs


def resume_problems(text: str, step: int) -> list:
    """B's second segment must print {"resumed_at_step": step, ..., "checks": "...: all match"}."""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{") and "resumed_at_step" in line:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("resumed_at_step") == step and "all match" in str(rec.get("checks", "")):
                return []
            return [f"resume line says {rec}, expected resumed_at_step {step} with all checks matching"]
    return [f"no resumed_at_step line in B's resume log (expected {step})"]


def straight_problems(text: str, name: str) -> list:
    """A1/A2 must run 0-300 straight: after a preemption Modal re-runs the input, train() resumes silently and prints
    resumed_at_step (the only trace)."""
    hits = [line.strip() for line in text.splitlines() if '"resumed_at_step"' in line]
    return [f"{name} was resumed mid-run (preempted?): {hits[0]} - rerun it straight"] if hits else []


def check_ckpt(folder: str, step: int = 0, expect_last_batch: str = "") -> list:
    """Problems of one copied checkpoint folder: files vs manifest, state.pt step and last batch hash."""
    import torch
    f = Path(folder)
    probs = manifest_problems(f)
    if not (f / "state.pt").exists():
        return probs + [f"{f}: no state.pt"]
    st = torch.load(f / "state.pt", map_location="cpu", weights_only=False)
    man = json.loads((f / "manifest.json").read_text()) if (f / "manifest.json").exists() else {}
    if step and (st.get("step") != step or man.get("step", step) != step):
        probs.append(f"{f}: state.pt step {st.get('step')}, manifest step {man.get('step')}, expected {step}")
    if man and man.get("fingerprint") != st.get("fingerprint"):
        probs.append(f"{f}: manifest fingerprint != state.pt fingerprint")
    if expect_last_batch and st.get("last_batch") != expect_last_batch:
        probs.append(f"{f}: last_batch {st.get('last_batch')} != CPU replay {expect_last_batch}")
    return probs


def loss_trend(log: list, n: int = 50):
    """(mean loss of the first n logged steps, of the last n): does the loss fall?"""
    ls = [r["loss"] for r in sorted(log, key=lambda r: r["step"]) if r.get("loss") is not None]
    if len(ls) < 2 * n:
        return None
    return sum(ls[:n]) / n, sum(ls[-n:]) / n


def verdict(runs: dict, lo=150, hi=299, factor=1.5, expect_last_batch="", resume_text=None, resume_step=150,
            require_state=True, straight_texts=None) -> dict:
    """runs = {"A1": run, "A2": run, "B": run} (load_run). Returns the full report with "verdict" PASS / FAIL.
    A run without state.pt fails (its batch hash cannot be checked) unless require_state is False (then a warning).
    straight_texts = {"A1": tee log text, "A2": ...}: a resumed_at_step line in any of them fails."""
    a1, a2, b = runs["A1"], runs["A2"], runs["B"]
    exact, warnings = [], []
    missing = [n for n, r in runs.items() if r["state"] is None]
    if missing:
        (exact if require_state else warnings).append(
            f"no state.pt for {missing}: step, batch hash and random-state checks not possible")
    for n, r in runs.items():
        if r["folder"] is not None:
            exact += manifest_problems(r["folder"])
    cfgs = [(r["state"] or {}).get("cfg") for r in runs.values()]
    base_lr = cfgs[0].get("lr") if cfgs[0] else None
    exact += exact_log_problems({n: r["log"] for n, r in runs.items()}, hi, base_lr)
    exact += state_problems({n: r["state"] for n, r in runs.items()}, expect_last_batch)
    if resume_text is not None:
        exact += resume_problems(resume_text, resume_step)
    for n, t in (straight_texts or {}).items():
        exact += straight_problems(t, n)
    d12 = rel_dist(a1["tensors"], a2["tensors"], a1["tensors"])
    d1b = rel_dist(a1["tensors"], b["tensors"], a1["tensors"])
    g12, n12 = loss_gap(a1["log"], a2["log"], lo, hi)
    g1b, n1b = loss_gap(a1["log"], b["log"], lo, hi)
    noise = []
    if g12 is None or g1b is None:
        noise.append(f"no common logged loss in steps {lo}-{hi} (relaunch with --log-every 1?)")
    identical = d12 == 0.0 and g12 == 0.0
    if identical:
        if not (d1b == 0.0 and g1b == 0.0):
            noise.append(f"A1 and A2 are bit-identical, B is not (d={d1b:.3e}, g={g1b})")
    elif not noise:
        if d1b > factor * d12:
            noise.append(f"weights: d(A1,B) {d1b:.4e} > {factor} x d(A1,A2) {d12:.4e}")
        if g1b > factor * g12:
            noise.append(f"loss: g(A1,B) {g1b:.4e} > {factor} x g(A1,A2) {g12:.4e}")
    return {"verdict": "PASS" if not exact and not noise else "FAIL",
            "d_A1_A2": d12, "d_A1_B": d1b, "g_A1_A2": g12, "g_A1_B": g1b, "loss_steps": [n12, n1b],
            "a1_a2_bit_identical": identical, "factor": factor, "window": [lo, hi], "a1_loss_trend": loss_trend(a1["log"]),
            "exact_problems": exact, "noise_problems": noise, "warnings": warnings}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for x in ("a1", "a2", "b"):
        ap.add_argument(f"--{x}", help="checkpoint folder or trainable.safetensors")
        ap.add_argument(f"--{x}-log", default="", help="relay JSON meta or text log (default: the folder's state.pt)")
    ap.add_argument("--lo", type=int, default=150)
    ap.add_argument("--hi", type=int, default=299)
    ap.add_argument("--factor", type=float, default=1.5)
    ap.add_argument("--expect-last-batch", default="", help="replay_steps.py --last-batch-at <step> hash")
    ap.add_argument("--b-resume-log", default="", help="stdout of B's resumed segment (checks the resumed_at_step line)")
    for x in ("a1", "a2"):
        ap.add_argument(f"--{x}-run-log", default="",
                        help=f"tee log of {x.upper()}'s run (5.1): fails if it shows a resumed_at_step line")
    ap.add_argument("--resume-step", type=int, default=150)
    ap.add_argument("--no-state-ok", action="store_true", help="a run given as a bare .safetensors only warns")
    ap.add_argument("--check", default="", help="only check one copied checkpoint folder (with --step)")
    ap.add_argument("--step", type=int, default=0)
    a = ap.parse_args(argv)
    if a.check:
        probs = check_ckpt(a.check, a.step, a.expect_last_batch)
        print(json.dumps({"checkpoint": a.check, "problems": probs}, indent=1))
        print("OK" if not probs else "BAD COPY")
        return 0 if not probs else 1
    if not (a.a1 and a.a2 and a.b):
        ap.error("--a1, --a2 and --b are required (or --check)")
    if not (a.a1_run_log and a.a2_run_log) and not a.no_state_ok:
        ap.error("--a1-run-log and --a2-run-log are required (the tee logs of A1 and A2): a preempted, resumed A1 or A2 "
                 "must be rerun, not compared")
    straight = {n: Path(f).read_text() for n, f in (("A1", a.a1_run_log), ("A2", a.a2_run_log)) if f}
    runs = {"A1": load_run(a.a1, a.a1_log), "A2": load_run(a.a2, a.a2_log), "B": load_run(a.b, a.b_log)}
    rep = verdict(runs, a.lo, a.hi, a.factor, a.expect_last_batch,
                  Path(a.b_resume_log).read_text() if a.b_resume_log else None, a.resume_step, not a.no_state_ok,
                  straight)
    print(json.dumps(rep, indent=1))
    print(rep["verdict"])
    return 0 if rep["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
