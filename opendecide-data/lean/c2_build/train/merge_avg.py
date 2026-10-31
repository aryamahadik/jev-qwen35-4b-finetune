"""merge_avg.py: the C2 candidate grid of A42-D 9.1-9.2 (checkpoint average and C1 -> C2 interpolation), in MERGED-weight
space. CPU only, no network.

A LoRA adapter is the update dW = (alpha/r) B A per module. Averaging the A factors and the B factors separately is NOT
the average of the updates (mean(B) mean(A) != mean(B A)), so it is never done here. Everything is a weighted sum of
updates:   dW_candidate = sum_k c_k dW_k   with   sum_k c_k = 1  (C1 is one of the sources).
That sum is written EXACTLY as one stacked LoRA adapter: B_cat = [c_1 B_1 | c_2 B_2 | ...], A_cat = [A_1 ; A_2 ; ...]
(rank r' = sum r_k, lora_alpha' = (alpha/r) r', so alpha'/r' is unchanged): B_cat A_cat = sum_k c_k B_k A_k. The result
loads in PEFT like any adapter and merges to the same bf16 weights as the dense sum.

Grid (frozen in A42-D 9.2). Checkpoints = the trainer's snapshots out_dir/snaps/s<step>/ (cfg snap_fracs) + the final
adapter (out_dir/adapter_model.safetensors, step = n_steps), 6-10 in all. Three bases:
  final      the final-step adapter                                  (the A37 default)
  last3      mean of the last three checkpoints (incl. the final)
  earlylate  0.5 x early + 0.5 x final; early = the checkpoint nearest 33% of the steps
and theta(a) = C1 + a (base - C1) for a in {0.5, 0.6, 0.7, 0.8, 0.9, 1.0}: 18 candidates, named <base>_a<10 a> (final_a10 =
the final adapter, copied byte for byte).
Output: <out>/<candidate>/{adapter_model.safetensors, adapter_config.json} + <out>/grid.json (sources, coefficients,
adapter sha256 of every candidate, grid sha256). Record grid.json's sha256 BEFORE any look (A42-D 9.6).

  merge_avg.py grid --c1 <C1 adapter dir> --run <run dir> --out <dir> [--n-steps N] [--alphas 0.5,...] [--verify-modules 8]
  merge_avg.py show --run <run dir> [--n-steps N]      (checkpoints and the three bases; writes nothing)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file

ALPHAS = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
BASES = ("final", "last3", "earlylate")
EARLY_FRAC = 0.33
MIN_CKPT, MAX_CKPT = 6, 10


def sha_file(p) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------ checkpoints
def list_checkpoints(run: Path, n_steps: int | None = None) -> list:
    """[{name, step, frac, dir}] sorted by step: snaps/s<step>/ and the final adapter (step = n_steps)."""
    run = Path(run)
    n = n_steps
    snaps = sorted((q for q in (run / "snaps").glob("s[0-9]*") if q.is_dir() and (q / "adapter_model.safetensors").exists()),
                   key=lambda q: int(q.name[1:]))
    if n is None:
        for q in [run, *snaps]:
            try:
                n = int(json.loads((q / "train_meta.json").read_text())["steps"])
                break
            except (OSError, KeyError, ValueError):
                continue
    if not n:
        raise SystemExit("n_steps unknown: pass --n-steps or keep train_meta.json")
    out = [{"name": q.name, "step": int(q.name[1:]), "frac": round(int(q.name[1:]) / n, 4), "dir": q} for q in snaps]
    if (run / "adapter_model.safetensors").exists():
        out.append({"name": "final", "step": n, "frac": 1.0, "dir": run})
    else:
        raise SystemExit(f"{run}: no final adapter_model.safetensors (training not finished)")
    if not MIN_CKPT <= len(out) <= MAX_CKPT:
        raise SystemExit(f"{len(out)} checkpoints found; A42-D 9.1 says {MIN_CKPT}-{MAX_CKPT}")
    return out


def base_coefs(ckpts: list, early_frac: float = EARLY_FRAC) -> dict:
    """{base: {checkpoint name: weight}} (weights sum to 1)."""
    final, rest = ckpts[-1], ckpts[:-1]
    if final["name"] != "final" or len(ckpts) < 4:
        raise SystemExit("need the final adapter last and at least 4 checkpoints")
    early = min(rest, key=lambda c: (abs(c["frac"] - early_frac), c["step"]))
    last3 = ckpts[-3:]
    if early["name"] in {c["name"] for c in last3}:
        raise SystemExit(f"the early checkpoint {early['name']} is inside the last 3: the grid would degenerate")
    return {"final": {"final": 1.0}, "last3": {c["name"]: 1 / 3 for c in last3},
            "earlylate": {early["name"]: 0.5, "final": 0.5}}


def candidate_coefs(base: dict, alpha: float) -> dict:
    """theta(a) = C1 + a (base - C1): coefficient a * w on every base checkpoint and (1 - a) on C1."""
    out = {k: alpha * w for k, w in base.items()}
    if alpha < 1.0 - 1e-12:
        out["c1"] = 1.0 - alpha
    return {k: v for k, v in out.items() if abs(v) > 1e-12}


def cand_name(base: str, alpha: float) -> str:
    return f"{base}_a{round(alpha * 10):02d}"


# ------------------------------------------------------------------------------------------------ tensors
def pairs(sd: dict) -> dict:
    """{module: (A, B)} from lora_A / lora_B tensor names; anything else (prism_x etc.) is refused."""
    mods = {}
    for k in sd:
        m = re.fullmatch(r"(.*)\.lora_([AB])\.weight", k)
        if not m:
            raise SystemExit(f"unexpected tensor {k!r} in an adapter (only lora_A / lora_B weights are merged)")
        mods.setdefault(m.group(1), {})[m.group(2)] = sd[k].float()
    bad = [m for m, v in mods.items() if set(v) != {"A", "B"}]
    if bad:
        raise SystemExit(f"modules without both A and B: {bad[:3]}")
    return {m: (v["A"], v["B"]) for m, v in mods.items()}


def stack(sources: dict, coefs: dict) -> dict:
    """Exact stacked adapter tensors for sum_k coefs[k] * dW_k. sources = {name: {module: (A, B)}}."""
    names = [k for k in sources if k in coefs]
    if abs(sum(coefs.values()) - 1.0) > 1e-9:
        raise ValueError(f"coefficients sum to {sum(coefs.values())}, not 1")
    mods = list(sources[names[0]])
    for k in names:
        if list(sources[k]) != mods:
            raise SystemExit(f"adapter {k} has different modules than {names[0]}")
    out = {}
    for m in mods:
        out[f"{m}.lora_A.weight"] = torch.cat([sources[k][m][0] for k in names], dim=0).contiguous()
        out[f"{m}.lora_B.weight"] = torch.cat([coefs[k] * sources[k][m][1] for k in names], dim=1).contiguous()
    return out


def dense(sd: dict, module: str, scale: float) -> torch.Tensor:
    return scale * sd[f"{module}.lora_B.weight"].float() @ sd[f"{module}.lora_A.weight"].float()


def formula_dense(sources: dict, coefs: dict, module: str, scale: float) -> torch.Tensor:
    return sum(c * scale * (sources[k][module][1] @ sources[k][module][0]) for k, c in coefs.items())


def verify(stacked: dict, sources: dict, coefs: dict, scale: float, modules: list) -> float:
    """Max abs difference between the stacked adapter's merged update and the weighted sum of the sources' updates."""
    return max(float((dense(stacked, m, scale) - formula_dense(sources, coefs, m, scale)).abs().max()) for m in modules)


# ------------------------------------------------------------------------------------------------ the grid
def build_grid(c1: Path, run: Path, out: Path, n_steps: int | None = None, alphas=ALPHAS, verify_modules: int = 8) -> dict:
    c1, run, out = Path(c1), Path(run), Path(out)
    ckpts = list_checkpoints(run, n_steps)
    bases = base_coefs(ckpts)
    cfg1 = json.loads((c1 / "adapter_config.json").read_text())
    r, la = int(cfg1["r"]), float(cfg1["lora_alpha"])
    scale = la / r
    files = {"c1": c1 / "adapter_model.safetensors", **{c["name"]: c["dir"] / "adapter_model.safetensors" for c in ckpts}}
    for c in ckpts:
        cc = json.loads((c["dir"] / "adapter_config.json").read_text())
        if int(cc["r"]) != r or float(cc["lora_alpha"]) != la:
            raise SystemExit(f"{c['name']}: r/alpha {cc['r']}/{cc['lora_alpha']} differ from C1's {r}/{la}")
    sources = {k: pairs(load_file(str(p))) for k, p in files.items()}
    mods = list(sources["c1"])
    sample = mods[:: max(1, len(mods) // max(1, verify_modules))][:verify_modules]
    out.mkdir(parents=True, exist_ok=True)
    cands, worst = [], 0.0
    for b in BASES:
        for a in alphas:
            name, co = cand_name(b, a), candidate_coefs(bases[b], a)
            d = out / name
            if d.exists():
                raise SystemExit(f"{d} exists: the grid is written once")
            d.mkdir()
            if len(co) == 1 and abs(list(co.values())[0] - 1.0) < 1e-12:      # the final adapter itself: byte for byte
                src = files[next(iter(co))]
                shutil.copyfile(src, d / "adapter_model.safetensors")
                rank, err = r, 0.0
            else:
                st = stack({k: sources[k] for k in co}, co)
                err = verify(st, {k: sources[k] for k in co}, co, scale, sample)
                if err > 1e-5:
                    raise SystemExit(f"{name}: stacked adapter differs from the weighted sum of updates by {err}")
                save_file(st, str(d / "adapter_model.safetensors"))
                rank = r * len(co)
            worst = max(worst, err)
            cfg = {**cfg1, "r": rank, "lora_alpha": scale * rank}
            (d / "adapter_config.json").write_text(json.dumps(cfg, indent=2))
            for extra in ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja"):
                if (c1 / extra).exists():
                    shutil.copyfile(c1 / extra, d / extra)
            cands.append({"name": name, "base": b, "alpha": a, "coefs": co, "rank": rank,
                          "adapter_sha256": sha_file(d / "adapter_model.safetensors"), "verify_max_abs_err": err})
    grid = {"what": "A42-D 9.2 candidate grid (merged-weight space; stacked-LoRA exact form)", "early_frac": EARLY_FRAC,
            "alphas": list(alphas), "scale_alpha_over_r": scale, "c1_adapter_sha256": sha_file(files["c1"]),
            "checkpoints": [{"name": c["name"], "step": c["step"], "frac": c["frac"],
                             "adapter_sha256": sha_file(files[c["name"]])} for c in ckpts],
            "bases": bases, "candidates": cands, "worst_verify_err": worst}
    canon = json.dumps({k: grid[k] for k in ("c1_adapter_sha256", "checkpoints", "bases", "candidates")}, sort_keys=True)
    grid["grid_sha256"] = hashlib.sha256(canon.encode()).hexdigest()
    (out / "grid.json").write_text(json.dumps(grid, indent=2))
    return grid


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grid")
    g.add_argument("--c1", required=True)
    g.add_argument("--run", required=True)
    g.add_argument("--out", required=True)
    g.add_argument("--n-steps", type=int, default=None)
    g.add_argument("--alphas", default=",".join(str(a) for a in ALPHAS))
    g.add_argument("--verify-modules", type=int, default=8)
    s = sub.add_parser("show")
    s.add_argument("--run", required=True)
    s.add_argument("--n-steps", type=int, default=None)
    a = ap.parse_args(argv)
    if a.cmd == "show":
        ck = list_checkpoints(Path(a.run), a.n_steps)
        print(json.dumps({"checkpoints": [{k: v for k, v in c.items() if k != "dir"} for c in ck],
                          "bases": base_coefs(ck)}, indent=1))
        return 0
    al = tuple(float(x) for x in a.alphas.split(","))
    gr = build_grid(Path(a.c1), Path(a.run), Path(a.out), a.n_steps, al, a.verify_modules)
    print(json.dumps({"candidates": len(gr["candidates"]), "grid_sha256": gr["grid_sha256"],
                      "worst_verify_err": gr["worst_verify_err"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
