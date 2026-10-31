"""oc1.export_driver: C1 (Qwen3.5-4B @ 851bf6e8 + LoRA q35_4b_main500k) merged in BF16 on CPU, written to a Volume.

Runs under /opt/fastpath/bin/python (C1's PINNED35 stack) inside the export container:
    python -m oc1.export_driver --old /old --out /out --name q35_4b_main500k_merged [--fresh]

The merge is hosting/export_c1_merged.py's OWN code (oc1/export_pure.py = verbatim ast copy of its pure functions, so the
Modal-free copy cannot drift): decoder_io.load + merge_and_unload, checks listed in that file's docstring (adapter sha256,
base pins, written == in-memory, formula check, base copies, config). What this driver adds:
  * a writable HF cache in /tmp whose snapshot is symlinks into the READ-ONLY base cache of the `opendecide` Volume
  * the three pinned files that the Volume's snapshot lacks (LICENSE, preprocessor_config.json, video_preprocessor_config.json)
    fetched from the Hub (they carry the image-processor settings the vision phase needs)
  * after the export: a comparison of every written file's sha256 with SPEED-2's merged checkpoint manifest (if shipped)
    -> "identical to the S1 checkpoint" or the list of differing files
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def build_hf_cache(old_root: Path, tmp_hf: Path, base: str, revision: str) -> Path:
    """tmp_hf/hub/models--X--Y/{refs/main, snapshots/<rev>/<symlinks>} -> returns the snapshot dir."""
    src = old_root / "hf" / "hub" / ("models--" + base.replace("/", "--")) / "snapshots" / revision
    if not src.exists():
        raise SystemExit(f"base snapshot missing on the Volume: {src}")
    root = tmp_hf / "hub" / ("models--" + base.replace("/", "--"))
    snap = root / "snapshots" / revision
    snap.mkdir(parents=True, exist_ok=True)
    (root / "refs").mkdir(parents=True, exist_ok=True)
    (root / "refs" / "main").write_text(revision)
    for p in sorted(src.iterdir()):
        dst = snap / p.name
        if not dst.exists():
            os.symlink(os.path.realpath(p), dst)
    return snap


def fetch_missing(snap: Path, names: list, base: str, revision: str) -> dict:
    """Download the pinned files the snapshot lacks (Hub, online, in a subprocess so this process stays offline)."""
    miss = [n for n in names if not (snap / n).exists()]
    if not miss:
        return {}
    env = {**os.environ, "HF_HOME": "/tmp/hf_meta", "HF_HUB_OFFLINE": "0"}
    code = ("import json; from huggingface_hub import hf_hub_download; "
            f"print(json.dumps({{n: hf_hub_download({base!r}, n, revision={revision!r}) for n in {miss!r}}}))")
    r = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"could not fetch {miss} from the Hub: {r.stderr[-500:]}")
    got = json.loads(r.stdout.strip().splitlines()[-1])
    return {n: Path(p) for n, p in got.items()}


def compare_with_reference(out_dir: Path, ref_manifest: dict | None) -> dict:
    if not ref_manifest:
        return {"reference": None}
    ref_files = (ref_manifest.get("files") or {})
    mine = json.loads((out_dir / "merge_manifest.json").read_text()).get("files") or {}
    diff = sorted(k for k in set(ref_files) | set(mine) if (ref_files.get(k) or {}).get("sha256") != (mine.get(k) or {}).get("sha256"))
    return {"reference": "SPEED-2 merged checkpoint manifest (mahadikarya3)", "n_files": len(mine), "n_ref_files": len(ref_files),
            "identical": not diff, "differing": diff[:20]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", default="/old")
    ap.add_argument("--out", default="/out")
    ap.add_argument("--name", default="q35_4b_main500k_merged")
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--sample", type=int, default=32)
    ap.add_argument("--ref-manifest", default="/root/work/ref_speed2_merge_manifest.json")
    ap.add_argument("--result", default="/tmp/export_result.json")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from oc1 import export_pure as E
    t0 = time.time()
    old, out_root = Path(a.old), Path(a.out)
    final, partial = out_root / "models" / a.name, out_root / "models" / (a.name + ".partial")
    if final.exists() and (final / E.MANIFEST).exists() and not a.overwrite:
        man = json.loads((final / E.MANIFEST).read_text())
        probs = E.verify_manifest_files(final, man)
        res = {"status": "exists", "verified": not probs, "problems": probs[:10], "n_files": len(man.get("files") or {}),
               "adapter_sha256": man.get("adapter_sha256"), "wall_s": round(time.time() - t0, 1)}
        Path(a.result).write_text(json.dumps(res))
        return 0 if not probs else 1
    adapter = old / "models" / E.C1_MODEL
    tmp_hf = Path("/tmp/hf")
    snap = build_hf_cache(old, tmp_hf, E.BASE, E.REVISION)
    extra = fetch_missing(snap, list(E.BASE_PINS), E.BASE, E.REVISION)
    os.environ.update(HF_HOME=str(tmp_hf), HF_HUB_OFFLINE="1")
    if partial.exists():
        shutil.rmtree(partial)
    try:
        man = E.export_local(E.BASE, snap, adapter, partial, layout="base", dev="cpu", revision=E.REVISION, fresh=a.fresh,
                             sample=a.sample, extra_files=extra, base_pins=E.BASE_PINS)
    except BaseException:
        shutil.rmtree(partial, ignore_errors=True)
        raise
    if final.exists():
        shutil.rmtree(final)
    os.rename(partial, final)
    ref = None
    try:
        ref = json.loads(Path(a.ref_manifest).read_text())
    except (OSError, ValueError):
        pass
    cmp = compare_with_reference(final, ref)
    res = {"status": "exported", "wall_s": round(time.time() - t0, 1), "n_files": len(man["files"]),
           "adapter_sha256": man["adapter_sha256"], "checks_passed": man["checks"]["passed"],
           "fetched_extra": sorted(extra), "compare_with_speed2": cmp,
           "files_sha256": {k: v["sha256"] for k, v in man["files"].items()}, "merge": man["merge"]}
    Path(a.result).write_text(json.dumps(res))
    print(json.dumps({k: res[k] for k in ("status", "wall_s", "n_files", "checks_passed", "compare_with_speed2")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
