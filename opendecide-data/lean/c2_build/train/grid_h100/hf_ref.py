"""grid_h100.hf_ref: the HF-adapter reference read of the parity check (runs under /opt/fastpath, the HF path's own stack).

Exactly `od_gcp.py predict --name <cand> --base Qwen/Qwen3.5-4B --revision <pin> --layout schema_branch_mark --tta-choice` on a row file:
decoder_io.load (the base from the HF cache at the pinned revision, the PEFT adapter on top), merge_and_unload, decoder_io.predict with
tta_choice, writing preds + meta in od_gcp's format. The base snapshot is exposed to the HF cache by a directory symlink
(hub/models--Qwen--Qwen3.5-4B/snapshots/<revision> -> the local copy), so the call is the production one (hub id + revision, offline).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def expose_cache(base_dir, hf_home) -> Path:
    from . import common as C
    snap = Path(hf_home) / "hub" / ("models--" + C.BASE.replace("/", "--")) / "snapshots" / C.REVISION
    snap.parent.mkdir(parents=True, exist_ok=True)
    (snap.parent.parent / "refs").mkdir(parents=True, exist_ok=True)
    (snap.parent.parent / "refs" / "main").write_text(C.REVISION)
    if snap.exists() or snap.is_symlink():
        snap.unlink()
    snap.symlink_to(Path(base_dir).resolve(), target_is_directory=True)
    return snap


def run(spec: dict) -> dict:
    from . import common as C
    os.environ["HF_HOME"] = spec["hf_home"]
    os.environ["HF_HUB_OFFLINE"] = "1"
    for d in (C.LEAN,):
        if str(d) not in sys.path:
            sys.path.insert(0, str(d))
    expose_cache(spec["base_dir"], spec["hf_home"])
    import torch
    import decoder_io
    decoder_io.STYLE = C.STYLE
    t0 = time.time()
    rows = [json.loads(l) for l in open(C.safe_path(spec["rows_file"])) if l.strip()]
    model, tok = decoder_io.load(C.BASE, "cuda", adapter=spec["adapter_dir"], revision=C.REVISION, layout=C.LAYOUT, style=None, force=False)
    model = model.merge_and_unload()
    model.eval()
    t1 = time.time()
    preds = decoder_io.predict(model, tok, rows, dev="cuda", tta_choice=True, tta_noul=False)
    sec = time.time() - t0
    name = spec["name"]
    out = Path(spec["out_dir"])
    C.write_jsonl(out / f"{name}.jsonl", ({"id": r["id"], "model": name, "probs": p} for r, p in zip(rows, preds)))
    meta = {"name": name, "rows": len(rows), "layout": decoder_io.LAYOUT, "style": decoder_io.STYLE, "base": C.BASE, "host": C.HOST_TAG,
            "gpu": torch.cuda.get_device_name(0), "torch": torch.__version__, "cuda": torch.version.cuda, "sec": round(sec),
            "tta": False, "tta_choice": True, "tta_noul": False, "perm_seed": None, "load": decoder_io.LOAD_INFO,
            "load_s": round(t1 - t0, 1), "engine": "hf_adapter_merge_and_unload"}
    C.write_json(out / f"{name}.meta.json", meta)
    return {"ok": True, "rows": len(rows), "sec": round(sec, 1), "load_s": round(t1 - t0, 1), "preds_sha256": C.sha256_file(out / f"{name}.jsonl")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    from . import common as C
    try:
        res = run(json.loads(Path(a.spec).read_text()))
    except BaseException as e:  # noqa: BLE001
        res = {"ok": False, "error": f"{type(e).__name__}: {e}"[:3000]}
    C.write_json(a.out, res)
    return 0 if res.get("ok") else 3


if __name__ == "__main__":
    sys.exit(main())
