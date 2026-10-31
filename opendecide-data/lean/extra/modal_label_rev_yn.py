"""Reversed-view 4B-E teacher labels for the CHOICE rows of the label shards (FINETUNE_PLAN.md 3.2 step 3: 2 views,
averaged in probability space, if the view flip rate is >= 3%; the dev test measured 8% on choice rows).

The first read (od_gcp.py label, modal_od.py::label) scored every row once in a seeded random view:
view = decoder_io.view_perms(rows, 20260930), stored as "view" in each label record. A perm lists ORIGINAL option
indices in DISPLAYED order: position k (letter A, B, ...) shows options[perm[k]]; predict() returns probabilities keyed
by option text. This job reads each choice row once more with perm = view[::-1] (exactly what predict's own TTA does),
so view + reversed view is order-invariant. merge_rev.py averages the two on the laptop.

Same model load as od_gcp.cmd_label: q35_4b_pxE on Qwen/Qwen3.5-4B @ 851bf6e8..., layout schema_branch_mark, style
cygnet, merged (merge_and_unload), HF_HUB_OFFLINE=1, H100 ("!" = never an H200), no TTA.

  MODAL_PROFILE=aryamhd ../.venv/bin/modal run --detach extra/modal_label_rev.py::main --groups "0,1;2,3;4,5;6-19"

Writes (Volume "opendecide" of that account) /vol/label_shards/labels_q35_4b_pxE_rev/shard_XXX.jsonl (choice rows
only, shard order) + shard_XXX.meta.json (written last); a shard is skipped when its meta vouches for it (resumable),
and the Volume is committed after every shard. Its own app name: never the live 4B run's app or model paths.
Fetch: MODAL_PROFILE=aryamhd ../.venv/bin/modal volume get opendecide label_shards/labels_q35_4b_pxE_rev extra/
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
if str(LEAN) not in sys.path:  # decoder_io, prism_x, shard_golden, writeblock live one level up
    sys.path.insert(0, str(LEAN))

# Copied EXACTLY from modal_od.PINNED35 (tests: extra/test_label_rev.py checks equality), so these image layers are the
# same as image35's and each account reuses its cached build. modal_od is not imported: it would also have to import
# inside the container.
PINNED35 = """accelerate==1.15.0 aiohappyeyeballs==2.7.1 aiohttp==3.14.3 aiosignal==1.4.0 annotated-doc==0.0.5 anyio==4.15.1
attrs==26.1.0 certifi==2026.7.22 charset_normalizer==3.5.1 click==8.5.0 cloudpickle==3.1.2 cuda-bindings==13.4.3
cuda-pathfinder==1.8.2 cuda-toolkit==13.0.3.0 datasets==5.0.1 dill==0.4.1 einops==0.8.2 filelock==4.0.3 fla-core==0.5.2
flash-linear-attention==0.5.2 frozenlist==1.8.0 fsspec==2026.6.0 h11==0.16.0 hf-xet==1.6.0 hf_transfer==0.1.9
httpcore==1.0.9 httpx==0.28.1 huggingface-hub==1.33.0 idna==3.20 jinja2==3.1.6 joblib==1.6.0 markdown-it-py==4.2.0
MarkupSafe==3.0.3 mdurl==0.1.2 mpmath==1.3.0 multidict==6.9.1 multiprocess==0.70.19 narwhals==2.26.0 networkx==3.7
numpy==2.5.3 nvidia-cublas==13.1.1.3 nvidia-cuda-cupti==13.0.85 nvidia-cuda-nvrtc==13.0.88 nvidia-cuda-runtime==13.0.96
nvidia-cudnn-cu13==9.24.0.43 nvidia-cufft==12.0.0.61 nvidia-cufile==1.15.1.6 nvidia-curand==10.4.0.35
nvidia-cusolver==12.0.4.66 nvidia-cusparse==12.6.3.3 nvidia-cusparselt-cu13==0.8.1 nvidia-nccl-cu13==2.30.7
nvidia-nvjitlink==13.4.92 nvidia-nvshmem-cu13==3.4.5 nvidia-nvtx==13.0.85 packaging==26.3 pandas==3.0.6 peft==0.21.0
propcache==0.5.4 protobuf==7.36.2 psutil==7.2.2 pyarrow==25.0.1 pygments==2.21.0 python-dateutil==2.9.0.post0
pyyaml==6.0.3 regex==2026.9.10 requests==2.34.2 rich==15.0.0 safetensors==0.8.0 scikit-learn==1.9.1 scipy==1.18.1
sentence-transformers==6.1.0 sentencepiece==0.2.2 setuptools==84.0.0 shellingham==1.5.4 six==1.17.0 sympy==1.14.0
threadpoolctl==3.7.0 tokenizers==0.23.2 torch==2.14.0 tqdm==4.70.1 transformers==5.17.0 triton==3.8.0 typer==0.27.2
typing-extensions==4.16.0 urllib3==2.8.0 xxhash==4.0.1 yarl==1.25.1""".split()
ENV35 = {"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false",
         "TRITON_CACHE_DIR": "/vol/triton_cache"}  # = modal_od.image35's env

APP_NAME = "opendecide-labelrevyn"  # NOT "opendecide" (the live 4B run's app)
NAME, BASE = "q35_4b_pxE", "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
LAYOUT, STYLE, PERM_SEED = "schema_branch_mark", "cygnet", 20260930
SHARDS = "/vol/label_shards"
ORIG = f"{SHARDS}/labels_{NAME}"
OUT = f"{SHARDS}/labels_{NAME}_revyn"
LOCAL_SHARDS = LEAN / "data/v14_label_shards"
EST_ROWS_PER_SEC = 25.0  # conservative choice-only H100 rate for the deadline check (measured about 24 on shards 0-5)

# the settings every rev shard records and is checked against (one label set never mixes settings)
SETTINGS = {"name": NAME, "base": BASE, "revision": REVISION, "layout": LAYOUT, "perm_seed": PERM_SEED,
            "view": "reverse_of_seeded_view", "rows": "noul_only", "tta": False, "tta_choice": False,
            "tta_noul": False, "merged": True}

app = modal.App(APP_NAME)
vol = modal.Volume.from_name("opendecide")  # the account's existing volume (never created here)
image = (
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*PINNED35)
    .env(ENV35)
    .add_local_python_source("decoder_io", "prism_x", "shard_golden", "writeblock")
)


# ---------------------------------------------------------------- pure helpers (CPU-testable, no model)

def reverse_views(views):
    """The reversed view of each seeded view: the options shown in the opposite order (still original indices)."""
    return [list(v)[::-1] for v in views]


def choice_rows(rows):
    return [r for r in rows if r["qtype"] == "noul"]


def ids_sha(ids):
    return hashlib.sha256("\n".join(ids).encode()).hexdigest()


def seeded_views(rows, seed=PERM_SEED):
    """The views the first read used (decoder_io.view_perms is per row: sha256(seed:id), so a choice-only subset gets
    exactly the views the full shard got)."""
    import decoder_io
    decoder_io.STYLE = STYLE  # yes/no views exist only in the cygnet style (the first read's style)
    return decoder_io.view_perms(rows, seed)


def check_stored_views(rows, views, orig_label_path):
    """If the first read's label file is present, every choice row's stored "view" must equal the recomputed one.
    Returns the number checked (0 when the file is absent on this account's volume)."""
    p = Path(orig_label_path)
    if not p.exists():
        return 0
    stored = {}
    with open(p) as f:
        for l in f:
            if l.strip():
                x = json.loads(l)
                stored[x["id"]] = x.get("view")
    bad = [r["id"] for r, v in zip(rows, views) if stored.get(r["id"]) != v]
    if bad:
        raise RuntimeError(f"{p}: {len(bad)} choice rows whose stored view differs from view_perms, e.g. {bad[:3]}")
    return len(rows)


def rev_done(shard_path, out_path, meta_path, settings) -> bool:
    """Done only if the meta exists (written last), its settings are these, its shard_sha256 is the shard file's, and
    the label file holds exactly the shard's choice-row ids in shard order."""
    import shard_golden as sg
    if not (Path(meta_path).exists() and Path(out_path).exists()):
        return False
    try:
        meta = json.loads(Path(meta_path).read_text())
        got = sg.read_ids(out_path)
    except (json.JSONDecodeError, KeyError):
        return False
    if meta.get("settings") != settings:
        raise SystemExit(f"{meta_path} was made with other settings: {meta.get('settings')} vs now {settings}")
    want = [r["id"] for r in choice_rows(sg.read_jsonl(shard_path))]
    return got == want and meta.get("rows") == len(want) and meta.get("shard_sha256") == sg._sha_file(shard_path)


def label_rev_shards(shard_ids, shards_dir, orig_dir, out_dir, predict_fn, expected_sha=None, commit=lambda: None,
                     settings=SETTINGS, load_info=None, stop_at_unix=0.0, rows_per_sec=EST_ROWS_PER_SEC):
    """For each shard id: skip if done; else read the choice rows, rebuild each row's seeded view, check it against the
    stored label file when present, predict with the reversed view, write the labels atomically, then the meta, then
    commit. predict_fn(rows, perms) -> list of {option: p}. Returns a per-shard summary."""
    import shard_golden as sg
    shards_dir, out_dir = Path(shards_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = []
    for i in shard_ids:
        sp = shards_dir / sg.shard_name(i)
        lp, mp = sg.label_paths(out_dir, sp)
        sha = sg._sha_file(sp)
        if expected_sha is not None and expected_sha.get(i) not in (None, sha):
            raise RuntimeError(f"{sp}: sha256 {sha} != the laptop's shards.json {expected_sha[i]} (other shard set)")
        if rev_done(sp, lp, mp, settings):
            print(f"{sp.name}: done, skipped", flush=True)
            summary.append({"shard": sp.name, "skipped": "done"})
            continue
        rs = choice_rows(sg.read_jsonl(sp))
        if stop_at_unix and time.time() + len(rs) / rows_per_sec + 60 > stop_at_unix:
            print(f"{sp.name}: {len(rs)} rows cannot finish before stop_at_unix; not started", flush=True)
            summary.append({"shard": sp.name, "skipped": "deadline"})
            continue
        Path(mp).unlink(missing_ok=True)  # a stale meta must never vouch for a new label file
        t = time.time()
        views = seeded_views(rs, settings["perm_seed"])
        checked = check_stored_views(rs, views, sg.label_paths(orig_dir, sp)[0])
        rev = reverse_views(views)
        preds = predict_fn(rs, rev)
        if len(preds) != len(rs):
            raise RuntimeError(f"{sp.name}: {len(preds)} predictions for {len(rs)} rows")
        for r, p in zip(rs, preds):
            if set(p) != {"yes", "no"}:  # yes/no rows have options null; predict keys them yes/no
                raise RuntimeError(f"{sp.name} {r['id']}: predicted keys {sorted(p)} != yes/no")
        sg.write_atomic(lp, [json.dumps({"id": r["id"], "model": settings["name"], "probs": p, "view": v})
                             for r, p, v in zip(rs, preds, rev)])
        sec = time.time() - t
        sg.write_json_atomic(mp, {"shard": sp.name, "rows": len(rs), "shard_sha256": sha,
                                  "choice_ids_sha256": ids_sha([r["id"] for r in rs]), "settings": settings,
                                  "style": STYLE, "views_checked_against_stored": checked, "sec": round(sec, 1),
                                  "rows_per_sec": round(len(rs) / max(sec, 1e-9), 3), "load": load_info or {},
                                  "finished_unix": time.time()})
        commit()
        print(f"{sp.name}: {len(rs)} choice rows in {sec:.0f}s ({len(rs) / max(sec, 1e-9):.1f}/s), "
              f"views checked {checked}", flush=True)
        summary.append({"shard": sp.name, "rows": len(rs), "sec": round(sec, 1), "views_checked": checked})
    return summary


# ---------------------------------------------------------------- Modal

@app.function(image=image, gpu="H100!", volumes={"/vol": vol}, timeout=3600)
def label_rev_remote(shard_ids: list, expected_sha: dict, stop_at_unix: float = 0.0) -> dict:
    os.environ["HF_HUB_OFFLINE"] = "1"  # the pinned base comes from /vol/hf only, as od_gcp label (--offline default)
    import torch
    import decoder_io
    vol.reload()
    expected_sha = {int(k): v for k, v in expected_sha.items()}
    import shard_golden as sg
    sd = Path(SHARDS)
    missing = [i for i in shard_ids if not (sd / sg.shard_name(i)).exists()]
    if missing:
        raise SystemExit(f"shards {missing} are not on this account's volume under {sd}")
    todo = [i for i in shard_ids if not rev_done(sd / sg.shard_name(i), *sg.label_paths(OUT, sd / sg.shard_name(i)),
                                                  SETTINGS)]
    if not todo:
        return {"shards": shard_ids, "todo": [], "note": "all done"}
    t0 = time.time()
    decoder_io.STYLE = STYLE
    model, tok = decoder_io.load(BASE, "cuda", adapter=f"/vol/models/{NAME}", revision=REVISION, layout=LAYOUT,
                                 style=None, force=False)
    commit_hash = getattr(getattr(model, "config", None), "_commit_hash", None)
    if commit_hash is not None and commit_hash != REVISION:
        raise RuntimeError(f"loaded base commit {commit_hash}, asked for {REVISION}")
    model = model.merge_and_unload()
    model.eval()
    if decoder_io.LAYOUT != LAYOUT or decoder_io.STYLE != STYLE:
        raise RuntimeError(f"loaded layout/style {(decoder_io.LAYOUT, decoder_io.STYLE)}, asked {(LAYOUT, STYLE)}")
    load_info = {**decoder_io.LOAD_INFO, "base_commit": commit_hash, "gpu": torch.cuda.get_device_name(0),
                 "torch": torch.__version__, "load_sec": round(time.time() - t0, 1)}
    print(json.dumps({"label_rev": SETTINGS, "load": load_info, "todo": todo}), flush=True)

    def predict_fn(rows, perms):
        if decoder_io.LAYOUT != LAYOUT or decoder_io.STYLE != STYLE:
            raise RuntimeError("layout/style changed")
        return decoder_io.predict(model, tok, rows, dev="cuda", tta=False, tta_noul=False, perms=perms)

    summ = label_rev_shards(todo, sd, ORIG, OUT, predict_fn, expected_sha, vol.commit, SETTINGS, load_info,
                            stop_at_unix)
    vol.commit()
    return {"shards": shard_ids, "summary": summ, "wall_sec": round(time.time() - t0, 1), "out": OUT}


def parse_groups(groups: str) -> list:
    """"0,1;2,3;6-19" -> [[0, 1], [2, 3], [6, ..., 19]] (one container per group)."""
    out = []
    for g in groups.split(";"):
        ids = []
        for part in g.split(","):
            if part.strip():
                lo, _, hi = part.strip().partition("-")
                ids += list(range(int(lo), int(hi or lo) + 1))
        if ids:
            out.append(ids)
    flat = [i for g in out for i in g]
    if len(flat) != len(set(flat)):
        raise SystemExit(f"a shard is in two groups: {groups}")
    return out


def local_shas(shards_json=LOCAL_SHARDS / "shards.json") -> dict:
    man = json.loads(Path(shards_json).read_text())
    return {int(s["file"][6:9]): s["sha256"] for s in man["shards"]}


@app.local_entrypoint()
def main(groups: str = "0,1;2,3;4,5;6-19", stop_at_utc: str = "23:55"):
    """One H100 container per group. stop_at_utc (today, UTC): a container does not START a shard it cannot finish by
    then (at EST_ROWS_PER_SEC); the function timeout (60 min) is the hard stop."""
    import datetime as dt
    hh, mm = (int(x) for x in stop_at_utc.split(":"))
    now = dt.datetime.now(dt.timezone.utc)
    stop = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if stop <= now:
        raise SystemExit(f"stop_at_utc {stop_at_utc} is already past ({now:%H:%M} UTC)")
    gs = parse_groups(groups)
    shas = local_shas()
    print(json.dumps({"groups": gs, "stop_at_unix": stop.timestamp(), "out": OUT}), flush=True)
    calls = [label_rev_remote.spawn(g, {str(i): shas[i] for i in g}, stop.timestamp()) for g in gs]
    for g, c in zip(gs, calls):
        try:
            print(json.dumps({"group": g, "result": c.get()}), flush=True)
        except Exception as e:  # one failed group never hides the others' results
            print(json.dumps({"group": g, "error": repr(e)[:500]}), flush=True)
