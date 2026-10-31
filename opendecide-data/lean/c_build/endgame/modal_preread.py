"""Model pre-reads on a Modal H100 (PREREG A21 (d): C1's reads pre-computed, kept sealed, sha256 only, no score).

Own app ("od-preread"); the same pinned Qwen3.5 image as c_build/modal_crowd.py (PINNED35 read from modal_od.py by ast;
modal_od.py and every lean/*.py stay unchanged). One model load, then every set through decoder_io.predict exactly as
`od_gcp.py predict` calls it (merged adapter, bf16, pinned base revision, layout asserted against train_meta, style from
train_meta, HF offline), written in od_gcp's pred format: preds_<set>/<out-name><tag>.jsonl + .meta.json (meta last =
done marker). The candidate's reads at gate time MUST use this same tool (same image, GPU type, host field "modal-h100").
NEEDS AMENDMENT: PREREG 4 fixes the gate scoring job to the Google L4 VM; this tool refuses to launch unless
PREREG_FINAL.md carries the owner line "OWNER-AMENDMENT gate-reads-h100" (RUNBOOK P2: use P2-L4).

Sets, in priority order. Each is committed to the Volume when it finishes; a re-run skips finished sets (resumable).
  1. sealed   the A15 suite (sha256 checked locally first), served 6.0 readout: choice/Score rows given + exact reversed
              order averaged (tta_choice), yes/no once  -> /vol/sealed_preread_c1/preds_nd_suite_v2/<out>.jsonl
  2. dev      the 9 gate splits, standard read (TTA off, perm_seed None)      -> /vol/preread_c1/preds_<split>/<out>.jsonl
  3. attack   eval_jagged, eval_opi, standard read
  4. perm     the 9 splits, seeded random view (perm_seed 1)                   -> <out>_perm
  5. rev      the 9 splits, choice rows only, exact reversed order             -> <out>_revchoice
              (6.0 served dev output = mean of 2. and 5. on choice rows; 2. alone on yes/no rows)
Prints set names, row counts, seconds and status only (never row text, never a score). A sealed error prints its type only.

  cd lean && MODAL_PROFILE=aryamhd ../.venv/bin/modal run --detach c_build/endgame/modal_preread.py::preread \
      --name q35_4b_main500k --out-name q35_4b_main500k_pre --minutes 36
Hard cost cap: the function timeout (TIMEOUT_MIN, 44 min of one H100 at $3.95/h = $2.90); --minutes = no new set starts
after that many minutes from launch.
"""
from __future__ import annotations

import ast
import hashlib
import json
import time
from pathlib import Path

import modal

LEAN = Path(__file__).resolve().parents[2]
BASE, REVISION, LAYOUT = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "schema_branch_mark"
A15_SUITE_SHA = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"
DEV_SPLITS = "dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev".split(",")
ATTACK = ["eval_jagged", "eval_opi"]
TIMEOUT_MIN = 44
DEV_ROOT, SEALED_ROOT = "/vol/preread_c1", "/vol/sealed_preread_c1"
SUITE_SET = "nd_suite_v2"
LOG = LEAN / "c_build/endgame/logs/preread_runs.jsonl"


def _pinned35() -> list[str]:
    tree = ast.parse((LEAN / "modal_od.py").read_text())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "PINNED35" for t in n.targets):
            v = n.value.func.value if isinstance(n.value, ast.Call) else n.value
            return ast.literal_eval(v).split()
    raise SystemExit("PINNED35 not found in modal_od.py")


app = modal.App("od-preread")
vol = modal.Volume.from_name("opendecide", create_if_missing=False)
image = (
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*_pinned35())
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false",
          "TRITON_CACHE_DIR": "/vol/triton_cache", "HF_HUB_OFFLINE": "1"})
    .add_local_file(LEAN / "decoder_io.py", "/root/decoder_io.py")
    .add_local_file(LEAN / "prism_x.py", "/root/prism_x.py")
    .add_local_file(LEAN / "od_gcp.py", "/root/od_gcp.py")
    .add_local_file(LEAN / "shard_golden.py", "/root/shard_golden.py")
    .add_local_file(LEAN / "writeblock.py", "/root/writeblock.py")
)


def _paths(job: dict, out_name: str):
    root = Path(SEALED_ROOT if job["sealed"] else DEV_ROOT) / f"preds_{job['set']}"
    nm = out_name + job["tag"]
    return root, root / f"{nm}.jsonl", root / f"{nm}.meta.json", nm


@app.function(image=image, gpu="H100!", volumes={"/vol": vol}, timeout=TIMEOUT_MIN * 60)
def preread_remote(name: str, out_name: str, sets: dict, jobs: list, deadline_unix: float) -> list:
    import os
    import sys
    sys.path.insert(0, "/root")
    import decoder_io
    import od_gcp
    t0 = time.time()
    res, todo = [], []
    for j in jobs:
        if _paths(j, out_name)[2].exists():
            res.append({"set": j["set"], "tag": j["tag"], "status": "already_done"})
        else:
            todo.append(j)
    if not todo:
        return res
    decoder_io.STYLE = "cygnet"   # = od_gcp cmd_predict with no --style; load() then takes the style from train_meta
    model, tok = decoder_io.load(BASE, "cuda", adapter=f"/vol/models/{name}", revision=REVISION, layout=LAYOUT,
                                 style=None, force=False)
    model = model.merge_and_unload()
    model.eval()
    gi = od_gcp.gpu_info()
    res.append({"set": "_load", "sec": round(time.time() - t0)})
    for j in todo:
        if time.time() > deadline_unix:
            res.append({"set": j["set"], "tag": j["tag"], "status": "skipped_deadline"})
            continue
        rows = sets[j["set"]]
        kw, pk = {}, {}
        if j["mode"] == "served":
            kw = {"tta_choice": True, "tta_noul": False}
        elif j["mode"] == "perm":
            pk = {"perms": decoder_io.view_perms(rows, 1)}
        elif j["mode"] == "rev":
            rows = [r for r in rows if r["qtype"] == "choice"]
            pk = {"perms": [list(range(len(r["options"])))[::-1] for r in rows]}
        t = time.time()
        try:
            preds = decoder_io.predict(model, tok, rows, dev="cuda", **kw, **pk)
        except Exception as e:  # noqa: BLE001 - a sealed error never carries its message (it could hold item text)
            res.append({"set": j["set"], "tag": j["tag"], "status": "error",
                        "error": type(e).__name__ + ("" if j["sealed"] else f": {str(e)[:160]}")})
            continue
        root, pf, mf, nm = _paths(j, out_name)
        root.mkdir(parents=True, exist_ok=True)
        tmp = pf.with_suffix(".jsonl.tmp")
        with open(tmp, "w") as f:
            for r, p in zip(rows, preds):
                f.write(json.dumps({"id": r["id"], "model": nm, "probs": p}) + "\n")
        os.replace(tmp, pf)
        meta = {"name": nm, "rows": len(rows), "layout": decoder_io.LAYOUT, "style": decoder_io.STYLE, "base": BASE,
                "host": "modal-h100", **gi, "sec": round(time.time() - t), **od_gcp.tta_meta(kw),
                "perm_seed": 1 if j["mode"] == "perm" else None, "load": decoder_io.LOAD_INFO,
                "view": {"served": "6.0 served: choice given+reversed mean, yes/no once", "std": "given order",
                         "perm": "view_perms seed 1", "rev": "choice rows only, exact reversed order"}[j["mode"]],
                "preread": "PREREG A21 (d), c_build/endgame/modal_preread.py", "adapter": name}
        mf.write_text(json.dumps(meta, indent=2))
        vol.commit()
        res.append({"set": j["set"], "tag": j["tag"], "status": "ok", "rows": len(rows), "sec": meta["sec"]})
    return res


def _rows(path: Path) -> list:
    return [json.loads(x) for x in path.open() if x.strip()]


@app.local_entrypoint()
def preread(name: str = "q35_4b_main500k", out_name: str = "q35_4b_main500k_pre", minutes: float = 36.0,
            parts: str = "sealed,dev,attack,perm,rev"):
    # PREREG 4 fixes the scoring job to ONE GPU type, the Google L4 VM, and refparity is against the stored L4 C1 read.
    # A Modal H100 gate/pre-read changes the platform: refused until the owner commits an amendment that says so.
    import re
    if not re.search(r"^[>\s*-]*OWNER-AMENDMENT gate-reads-h100:", (LEAN / "PREREG_FINAL.md").read_text(), re.M):
        raise SystemExit("REFUSED: NEEDS AMENDMENT. PREREG 4 puts gate reads on the L4 VM; an H100 pre-read needs the "
                         "line 'OWNER-AMENDMENT gate-reads-h100' in PREREG_FINAL.md (owner only). Use RUNBOOK P2-L4.")
    want = [p for p in parts.split(",") if p]
    sets, jobs = {}, []
    if "sealed" in want:
        suite = LEAN / "sealed_nd" / "suite_v2.jsonl"          # read by program only; never printed
        h = hashlib.sha256(suite.read_bytes()).hexdigest()
        if h != A15_SUITE_SHA:
            raise SystemExit("sealed suite sha256 is not A15's: refused")
        sets[SUITE_SET] = _rows(suite)
        jobs.append({"set": SUITE_SET, "mode": "served", "tag": "", "sealed": True})
    if any(p in want for p in ("dev", "perm", "rev")):
        for s in DEV_SPLITS:
            sets[s] = _rows(LEAN / "data" / f"{s}.jsonl")
    if "attack" in want:
        for s in ATTACK:
            sets[s] = _rows(LEAN / "data" / f"{s}.jsonl")
    for part, mode, tag, names in (("dev", "std", "", DEV_SPLITS), ("attack", "std", "", ATTACK),
                                   ("perm", "perm", "_perm", DEV_SPLITS), ("rev", "rev", "_revchoice", DEV_SPLITS)):
        if part in want:
            jobs += [{"set": s, "mode": mode, "tag": tag, "sealed": False} for s in names]
    deadline = time.time() + 60 * minutes
    print(json.dumps({"launch": name, "out": out_name, "sets": {k: len(v) for k, v in sets.items()},
                      "jobs": len(jobs), "minutes": minutes, "timeout_min": TIMEOUT_MIN}))
    t = time.time()
    try:
        res = preread_remote.remote(name, out_name, sets, jobs, deadline)
    except Exception as e:  # noqa: BLE001 (timeout: the sets committed so far stay on the Volume)
        res = [{"status": "remote_failed", "error": type(e).__name__}]
    rec = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "name": name, "out": out_name,
           "wall_s": round(time.time() - t), "results": res}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    for r in res:
        print(json.dumps(r))
