"""grid_h100.gridbuild: the 18 candidates built from the saved C2 LoRA checkpoints exactly as c2_build/train/grid_plan.py (P6) defines them.

The construction is merge_avg.build_grid itself (stacked LoRA, rank 16 K, alpha/r unchanged), not a copy of it; the result is held to the
grid record written BEFORE any look (grid_plan.py record, A42-D 9.6): the rebuilt grid_sha256 and the adapter sha256 of every candidate
must equal GRID_RECORD.json's, and grid_plan.check_grid must find the frozen shape (3 bases x alpha 0.5..1.0, coefficients sum to 1,
the early checkpoint nearest 33%, final_a10 = the final adapter byte for byte, 6-10 checkpoints). A rebuild that differs from the record
in one byte is refused: the 18 are then not the recorded 18. (The tensor arithmetic is elementwise, so the bytes do not depend on the
machine; if a rebuild ever differs, the fallback is `grid_source: volume` with the locally built grid uploaded to the Volume, checked
the same way.)

merge_avg.py and grid_plan.py come from lean/c2_build/train (laptop) or /root/c2grid (container).
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

from . import common as C

SERVING_PIN = "S1_CONFIG_PIN.json"


class GridRefused(SystemExit):
    pass


def load_tools():
    """(merge_avg, grid_plan) from the first folder that has both."""
    for d in (os.environ.get("C2GRID_DIR"), "/root/c2grid", str(C.LEAN / "c2_build" / "train")):
        if d and (Path(d) / "merge_avg.py").exists() and (Path(d) / "grid_plan.py").exists():
            if d not in sys.path:
                sys.path.insert(0, d)
            import grid_plan
            import merge_avg
            return merge_avg, grid_plan
    raise GridRefused("gridbuild: merge_avg.py / grid_plan.py not found (set C2GRID_DIR)")


def locate_c1_adapter(candidates=C.C1_ADAPTER_DIR_CANDIDATES, expect_sha: str = C.C1_ADAPTER_SHA256) -> Path:
    """The first folder whose adapter_model.safetensors is C1's (sha256 507d1c29...)."""
    seen = []
    for d in candidates:
        f = Path(d) / "adapter_model.safetensors"
        if f.exists():
            sha = C.sha256_file(f)
            if sha == expect_sha:
                return Path(d)
            seen.append(f"{d}: {sha[:16]}")
    raise GridRefused(f"gridbuild: no C1 adapter (sha256 {expect_sha[:16]}) in {list(candidates)}; found {seen or 'none'}")


def check_run_dir(run_dir, tok_pins: dict) -> dict:
    """The C2 run folder: train_meta.json holds a cfg in C1's prompt layout / style, and the tokenizer files it saved (when it saved
    any) are byte-identical to C1's pinned ones (the gate renders prompts with the adapter folder's own tokenizer copy)."""
    run_dir = Path(run_dir)
    info = {"run_dir": str(run_dir), "problems": [], "notes": []}
    tm = run_dir / "train_meta.json"
    if not tm.exists():
        info["problems"].append("train_meta.json missing (training not finished)")
        return info
    meta = json.loads(tm.read_text())
    cfg = meta.get("cfg") or {}
    info["layout"], info["style"], info["steps"] = cfg.get("layout"), cfg.get("style"), meta.get("steps")
    info["base_revision"] = cfg.get("base_revision")
    for k, want in (("layout", C.LAYOUT), ("style", C.STYLE), ("base_revision", C.REVISION)):
        if cfg.get(k) != want:
            info["problems"].append(f"train_meta cfg {k} {cfg.get(k)!r} != {want!r}")
    for n in ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja"):
        p = run_dir / n
        if not p.exists():
            info["notes"].append(f"{n} not saved in the run folder")
        elif C.sha256_file(p) != tok_pins.get(n):
            info["problems"].append(f"{n} differs from C1's pinned tokenizer file")
    return info


def verify_against_record(grid: dict, record: dict) -> list:
    """Problems (empty = the grid is the recorded one)."""
    probs = []
    if grid.get("grid_sha256") != record.get("grid_sha256"):
        probs.append(f"grid_sha256 {str(grid.get('grid_sha256'))[:16]} != recorded {str(record.get('grid_sha256'))[:16]}")
    if grid.get("c1_adapter_sha256") != record.get("c1_adapter_sha256"):
        probs.append("C1 adapter sha256 differs from the record")
    got = {c["name"]: c["adapter_sha256"] for c in grid.get("candidates", [])}
    want = record.get("candidates") or {}
    if got != want:
        bad = sorted(k for k in set(got) | set(want) if got.get(k) != want.get(k))
        probs.append(f"{len(bad)} candidate adapter sha256 differ from the record (first: {bad[:3]})")
    return probs


def rebuild(c1_dir, run_dir, out_dir, record: dict, n_steps: int | None = None) -> dict:
    ma, gp = load_tools()
    if not record or not record.get("grid_sha256"):
        raise GridRefused("gridbuild: no grid record (grid_plan.py record must be written before any look, A42-D 9.6)")
    if Path(out_dir).exists() and any(Path(out_dir).iterdir()):
        shutil.rmtree(out_dir)
    grid = ma.build_grid(Path(c1_dir), Path(run_dir), Path(out_dir), n_steps)
    probs = gp.check_grid(grid, Path(out_dir)) + verify_against_record(grid, record)
    if probs:
        raise GridRefused("gridbuild: the rebuilt grid is not the recorded frozen grid: " + "; ".join(probs[:5]))
    return grid


def load_existing(grid_dir, record: dict) -> dict:
    ma, gp = load_tools()
    grid = json.loads((Path(grid_dir) / "grid.json").read_text())
    probs = gp.check_grid(grid, Path(grid_dir)) + verify_against_record(grid, record)
    if probs:
        raise GridRefused("gridbuild: the grid on the Volume is not the recorded frozen grid: " + "; ".join(probs[:5]))
    return grid


def build_one(c1_dir, run_dir, cand: str, out_dir, record: dict, n_steps: int | None = None) -> dict:
    """One candidate, built the way merge_avg.build_grid builds it (same functions, same bytes), held to the record's sha256."""
    ma, gp = load_tools()
    from safetensors.torch import load_file, save_file
    c1_dir, run_dir, out_dir = Path(c1_dir), Path(run_dir), Path(out_dir)
    ckpts = ma.list_checkpoints(run_dir, n_steps)
    bases = ma.base_coefs(ckpts)
    base_name, alpha = None, None
    for b in ma.BASES:
        for a in ma.ALPHAS:
            if ma.cand_name(b, a) == cand:
                base_name, alpha = b, a
    if base_name is None:
        raise GridRefused(f"gridbuild: {cand!r} is not one of the 18 candidates")
    co = ma.candidate_coefs(bases[base_name], alpha)
    cfg1 = json.loads((c1_dir / "adapter_config.json").read_text())
    r, la = int(cfg1["r"]), float(cfg1["lora_alpha"])
    scale = la / r
    files = {"c1": c1_dir / "adapter_model.safetensors", **{c["name"]: c["dir"] / "adapter_model.safetensors" for c in ckpts}}
    out_dir.mkdir(parents=True, exist_ok=True)
    if len(co) == 1 and abs(list(co.values())[0] - 1.0) < 1e-12:
        shutil.copyfile(files[next(iter(co))], out_dir / "adapter_model.safetensors")
        rank = r
    else:
        src = {k: ma.pairs(load_file(str(files[k]))) for k in co}
        st = ma.stack(src, co)
        save_file(st, str(out_dir / "adapter_model.safetensors"))
        rank = r * len(co)
    (out_dir / "adapter_config.json").write_text(json.dumps({**cfg1, "r": rank, "lora_alpha": scale * rank}, indent=2))
    for extra in ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja"):
        if (c1_dir / extra).exists():
            shutil.copyfile(c1_dir / extra, out_dir / extra)
    sha = C.sha256_file(out_dir / "adapter_model.safetensors")
    want = (record.get("candidates") or {}).get(cand)
    if want and sha != want:
        raise GridRefused(f"gridbuild: {cand} rebuilt with sha256 {sha[:16]}, the record says {want[:16]}")
    return {"name": cand, "base": base_name, "alpha": alpha, "coefs": co, "rank": rank, "adapter_sha256": sha}
