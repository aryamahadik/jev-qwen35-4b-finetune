"""Run OpenDecide jobs on a plain GPU machine (the Google Cloud L4 VM) with the same code paths as modal_od.py:
train_decoder.train for training and decoder_io.predict for predictions, the same config keys, the same LoRA targets,
and the same prediction file format (preds_<split>/<name>.jsonl plus a .meta.json). Paths are relative to this
directory: data/ holds the splits, models/<name>/ holds adapters.
  python od_gcp.py predict --name q35_2b_v11r --base Qwen/Qwen3.5-2B --splits dev,hard_dev [--tag suffix]
  python od_gcp.py train --name X --base Qwen/Qwen3.5-2B [same options as modal_od.py::train]
  python od_gcp.py smoke --base Qwen/Qwen3.5-2B --train-file train_2b_rest.jsonl --steps 20 [--batch 16]
  python od_gcp.py latency --name q35_2b_v11r --base Qwen/Qwen3.5-2B --split dev
  python od_gcp.py relay --config runs/q35_4b_main.json [--stop-at-step N] [--stop-after-min M]
  python od_gcp.py label --name q35_4b_pxE --base Qwen/Qwen3.5-4B --layout schema_branch_mark \\
      --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --shards-dir data/v14_label_shards [--shard i] [--perm-seed S]
PRISM-X arms (PRISM_X.md): train with --arm H|I|J (sets the control plane and the schema_branch_mark layout); with
"ablate_splits" in --extra, the same weights are also scored with the control plane off (<name>_nopx).
Adapter loads take the prompt layout, style and base revision from the adapter's train_meta.json (decoder_io.load);
a conflicting --layout/--style/--revision/--base raises unless --force (the override is written into the meta).
An adapter name with "/" (a snapshot, e.g. q35_4b_main500k/snaps/s002500) is written as one flat preds file, "/" -> "__".
"""
import argparse
import json
import os
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA, MODELS = HERE / "data", HERE / "models"
QWEN35_TARGETS = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"
# same tuple as modal_od.RELAY_REQUIRED (tests/test_labelling.py checks); modal_od cannot be imported without modal
RELAY_REQUIRED = ("name", "base", "base_revision", "train_file", "rel_file", "epochs", "lr", "batch", "r", "alpha", "seed",
                  "style", "layout", "micro_tokens", "targets", "ckpt_every_min")
RELAY_ENV_OK = ("gpu", "sm_count", "python", "cudnn", "torch_cuda")  # may differ between an H100 segment and the L4
QWEN35_4B_REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"  # runs/q35_4b_main.json base_revision


def rows(split):
    return [json.loads(l) for l in open(DATA / f"{split}.jsonl")]


def save(name, preds_by_split, extra=None):
    import decoder_io
    for s, preds in preds_by_split.items():
        rs = rows(s)
        pd = HERE / ("preds" if s == "eval" else f"preds_{s}")
        pd.mkdir(parents=True, exist_ok=True)
        with open(pd / f"{name}.jsonl", "w") as f:
            for r, p in zip(rs, preds):
                f.write(json.dumps({"id": r["id"], "model": name, "probs": p}) + "\n")
        meta = {"name": name, "rows": len(rs), "layout": decoder_io.LAYOUT, "style": decoder_io.STYLE, **(extra or {})}
        (pd / f"{name}.meta.json").write_text(json.dumps(meta, indent=2))
        print(f"wrote {pd.name}/{name}.jsonl ({len(preds)} rows)", flush=True)


def out_name(name, tag=""):
    """Preds file name for an adapter name: a snapshot path (run/snaps/s002500) becomes one flat file name, so save()
    never opens preds_<split>/run/snaps/... (and the "model" field stays a plain name)."""
    return (name + tag).replace("/", "__")


def gpu_info():
    import torch
    return {"gpu": torch.cuda.get_device_name(0), "torch": torch.__version__, "cuda": torch.version.cuda}


def tta_kwargs(a):
    """decoder_io.predict TTA arguments: legacy --tta (choice reversal and Yes/No swap together), or the per-type
    --tta-choice / --tta-noul."""
    if a.tta and (a.tta_choice or a.tta_noul):
        raise SystemExit("pass --tta, or --tta-choice/--tta-noul, not both")
    if a.tta_choice or a.tta_noul:
        return {"tta_choice": a.tta_choice, "tta_noul": a.tta_noul}
    return {"tta": a.tta, "tta_noul": a.tta}


def tta_meta(kw):
    return {"tta": kw.get("tta", False), "tta_choice": kw.get("tta_choice", kw.get("tta", False)),
            "tta_noul": kw.get("tta_noul", False)}


def cmd_predict(a):
    import decoder_io
    decoder_io.STYLE = a.style or "cygnet"
    adapter = str(MODELS / a.name) if a.adapter else None
    kw = tta_kwargs(a)
    t0 = time.time()
    model, tok = decoder_io.load(a.base, "cuda", adapter=adapter, revision=a.revision or None, layout=a.layout or None,
                                 style=a.style, force=a.force)
    if adapter:
        model = model.merge_and_unload()
    model.eval()
    out = {}
    for s in a.splits.split(","):
        t = time.time()
        rs = rows(s)
        pk = {} if a.perm_seed is None else {"perms": decoder_io.view_perms(rs, a.perm_seed)}
        out[s] = decoder_io.predict(model, tok, rs, dev="cuda", **kw, **pk)
        print(f"{s}: {len(out[s])} rows in {time.time() - t:.0f}s", flush=True)
    save(out_name(a.name, a.tag), out, {"base": a.base, "host": "gcp", **gpu_info(), "sec": round(time.time() - t0),
                                        **tta_meta(kw), "perm_seed": a.perm_seed, "layout": decoder_io.LAYOUT,
                                        "load": decoder_io.LOAD_INFO})


def build_cfg(a):
    cfg = {"base": a.base, "recipe": a.recipe, "epochs": a.epochs, "lr": a.lr, "batch": a.batch, "lam": a.lam, "r": a.r,
           "alpha": 2 * a.r, "train_file": a.train_file, "rel_file": a.rel_file, "grad_ckpt": True, "beta": a.beta,
           "style": a.style, "log_every": a.log_every, "kd": a.kd,
           **({"init_adapter": str(MODELS / a.init)} if a.init else {}), **({"prism_x": a.arm} if a.arm else {}),
           **(json.loads(a.extra) if a.extra else {})}
    if "Qwen3.5" in a.base:
        cfg["targets"] = QWEN35_TARGETS
    return cfg


def cmd_train(a):
    import decoder_io
    import train_decoder
    decoder_io.STYLE = a.style
    cfg = build_cfg(a)
    res = train_decoder.train(cfg, DATA, MODELS / a.name)
    model, tok = res["model"], res["tok"]
    preds = {s: decoder_io.predict(model, tok, rows(s), dev="cuda") for s in a.splits.split(",") if s}
    # cfg["base"]: --extra may override --base (4B-E's meta recorded the 2B because of that)
    save(a.name, preds, {"base": cfg["base"], "host": "gcp", **gpu_info(), "train": {k: v for k, v in res["meta"].items() if k != "log"}})
    import prism_x
    if prism_x.PX is not None and cfg.get("ablate_splits"):  # reliance check: same weights, control plane off
        prism_x.STATE["enabled"] = False
        save(a.name + "_nopx", {s: decoder_io.predict(model, tok, rows(s), dev="cuda") for s in cfg["ablate_splits"]},
             {"base": cfg["base"], "host": "gcp", "ablation": "PRISM-X control plane off at inference"})
        prism_x.STATE["enabled"] = True
    (HERE / "logs").mkdir(exist_ok=True)
    (HERE / f"logs/{a.name}.json").write_text(json.dumps(res["meta"], indent=2))


def cmd_smoke(a):
    """A few training steps on the first rows of a train file: loss finite, seconds per step, peak GPU memory."""
    import torch
    import decoder_io
    import train_decoder
    decoder_io.STYLE = a.style
    src = [json.loads(l) for l in open(DATA / a.train_file)]
    n = a.steps * a.batch + 64
    tmp = DATA / "_smoke_train.jsonl"
    tmp.write_text("".join(json.dumps(r) + "\n" for r in src[:n]))
    a.train_file, a.rel_file, a.epochs, a.log_every = tmp.name, "_none_relations.jsonl", a.steps * a.batch / n, 5
    (DATA / a.rel_file).write_text("")
    torch.cuda.reset_peak_memory_stats()
    t0 = time.time()
    res = train_decoder.train({**build_cfg(a), "resume": False}, DATA, HERE / "models/_smoke")  # a smoke never resumes
    log = res["meta"].get("log", [])
    print(json.dumps({"steps": a.steps, "batch": a.batch, "sec_total": round(time.time() - t0),
                      "min_per_step_logged": [x.get("min") for x in log][-3:], "last_losses": [x.get("loss") for x in log][-3:],
                      "peak_mem_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2), **gpu_info()}), flush=True)


def cmd_blend(a):
    """Exact weighted blend of LoRA adapters (PEFT add_weighted_adapter, combination 'cat'), merged, then predictions.
    The layout, style and base revision are resolved per adapter; adapters that disagree raise."""
    import decoder_io
    from peft import PeftModel
    decoder_io.STYLE = a.style or "cygnet"
    names, ws = a.adapters.split(","), [float(x) for x in a.weights.split(",")]
    info = decoder_io.resolve_prompt([str(MODELS / n) for n in names], a.base, layout=a.layout or None, style=a.style,
                                     revision=a.revision or None, force=a.force)
    t0 = time.time()
    base, tok = decoder_io.load(a.base, "cuda", revision=info["revision"], layout=info["layout"], style=info["style"])
    model = PeftModel.from_pretrained(base, str(MODELS / names[0]), adapter_name="a0")
    for i, n in enumerate(names[1:], 1):
        model.load_adapter(str(MODELS / n), adapter_name=f"a{i}")
    model.add_weighted_adapter([f"a{i}" for i in range(len(names))], ws, adapter_name="blend", combination_type="cat")
    model.set_adapter("blend")
    model = model.merge_and_unload(adapter_names=["blend"])
    model.eval()
    out = {}
    for s in a.splits.split(","):
        t = time.time()
        out[s] = decoder_io.predict(model, tok, rows(s), dev="cuda")
        print(f"{s}: {len(out[s])} rows in {time.time() - t:.0f}s", flush=True)
    save(out_name(a.name, a.tag), out, {"base": a.base, "blend": dict(zip(names, ws)), "host": "gcp", **gpu_info(),
                                        "sec": round(time.time() - t0), "load": {
                                            **info, "layout": decoder_io.LAYOUT, "style": decoder_io.STYLE,
                                            "chat_template_sha": decoder_io.LOAD_INFO.get("chat_template_sha")}})


def cmd_latency(a):
    import decoder_io
    decoder_io.STYLE = a.style or "cygnet"
    model, tok = decoder_io.load(a.base, "cuda", adapter=str(MODELS / a.name), layout=a.layout or None, style=a.style,
                                 force=a.force)
    model = model.merge_and_unload()
    model.eval()
    print(json.dumps({"latency": decoder_io.latency(model, tok, rows(a.split), dev="cuda"), **gpu_info(),
                      "layout": decoder_io.LAYOUT, "style": decoder_io.STYLE}), flush=True)


# ---------------------------------------------------------------- relay tail on the L4 (FINETUNE_PLAN.md C9)

def relay_cfg(config_path, stop_at_step=0, stop_after_min=0.0):
    """(name, cfg) for one relay segment from a frozen config file, as modal_od.py::relay builds it, but always
    expecting a checkpoint (a missing one must fail, not restart at step 0 on a slower GPU) and allowing the
    GPU-bound part of the environment to change (checked separately by relay_env_diff)."""
    cfg = json.loads(Path(config_path).read_text())
    missing = [k for k in RELAY_REQUIRED if k not in cfg]
    if missing:
        raise SystemExit(f"{config_path}: missing keys {missing} (every key must be written out)")
    name = cfg.pop("name")
    if cfg["targets"] == "QWEN35":
        cfg["targets"] = QWEN35_TARGETS
    cfg.update({"no_overwrite": True, "expect_resume": True, "allow_env_change": True, "stop_at_step": stop_at_step,
                "stop_at_unix": time.time() + 60 * stop_after_min if stop_after_min > 0 else 0})
    return name, cfg


def relay_env_diff(saved, now):
    """Environment differences (saved -> now) outside RELAY_ENV_OK: any of them refuses the resume."""
    saved, now = saved or {}, now or {}
    return {k: [saved.get(k), now.get(k)] for k in sorted(set(saved) | set(now), key=str)
            if k not in RELAY_ENV_OK and saved.get(k) != now.get(k)}


def check_relay_env(ckpt_dir, env_now):
    """Refuses (SystemExit) unless a checkpoint exists and its saved env matches env_now outside RELAY_ENV_OK. Returns
    the allowed differences. A checkpoint left at _ckpt.old (stopped between two renames) counts; the trainer
    restores it."""
    import torch
    ckpt_dir = Path(ckpt_dir)
    st_path = ckpt_dir / "state.pt"
    if not st_path.exists() and (ckpt_dir.with_name(ckpt_dir.name + ".old") / "state.pt").exists():
        st_path = ckpt_dir.with_name(ckpt_dir.name + ".old") / "state.pt"
    if not st_path.exists():
        raise SystemExit(f"relay: no checkpoint at {ckpt_dir / 'state.pt'} (wrong name, or the copy is missing)")
    saved = torch.load(st_path, map_location="cpu", weights_only=False).get("env")
    if saved is None:
        raise SystemExit(f"relay: {st_path} has no saved env; refusing to resume blind")
    bad = relay_env_diff(saved, env_now)
    if bad:
        raise SystemExit(f"relay: software differs from the checkpoint's (saved -> now): {bad}")
    return {k: [saved.get(k), env_now.get(k)] for k in RELAY_ENV_OK if saved.get(k) != env_now.get(k)}


def cmd_relay(a):
    import decoder_io
    import train_decoder
    cfg_path = Path(a.config) if Path(a.config).is_absolute() else HERE / a.config
    name, cfg = relay_cfg(cfg_path, a.stop_at_step, a.stop_after_min)
    decoder_io.STYLE = cfg["style"]
    allowed = check_relay_env(MODELS / name / "_ckpt", train_decoder._env())
    print(json.dumps({"relay": name, "env_changes_allowed": allowed}), flush=True)
    if not (a.stop_after_min > 0 or a.stop_at_step > 0):
        print("note: no stop point set; this segment runs to the end")
    res = train_decoder.train(cfg, DATA, MODELS / name)
    (HERE / "logs").mkdir(exist_ok=True)
    tag = f"stopped_at_{res['next_step']}" if res.get("stopped") else "final"
    (HERE / f"logs/relay_{name}_{tag}.json").write_text(json.dumps(res["meta"], indent=2, default=str))
    print(json.dumps({"name": name, "stopped": bool(res.get("stopped")), "next_step": res.get("next_step"),
                      "of": res.get("n_steps")}), flush=True)
    return res


# ---------------------------------------------------------------- sharded teacher labels (FINETUNE_PLAN.md C10, 3.2)

def label_shards(model, tok, shards, out_dir, settings, predict_kw, style, load_info=None):
    """Labels each shard that is not done: the label file goes to .tmp then os.replace, the meta is written last. A shard
    is done only if its meta exists, the ids and line count match and its shard_sha256 is the shard file's
    (shard_golden.shard_done); a done shard labelled with other settings stops the job (one label set never mixes
    views, layouts or models). The layout (and the style the load resolved) is asserted before every shard. load_info
    (default decoder_io.LOAD_INFO) goes into every meta."""
    import decoder_io
    import shard_golden as sg
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    check_done_settings(shards, out_dir, settings)
    done = []
    for sp in shards:
        lp, mp = sg.label_paths(out_dir, sp)
        if sg.shard_done(sp, lp, mp):
            print(f"{sp.name}: done, skipped", flush=True)
            done.append(sp.name)
            continue
        if decoder_io.LAYOUT != settings["layout"] or decoder_io.STYLE != style:
            raise RuntimeError(f"layout/style changed before {sp.name}: {(decoder_io.LAYOUT, decoder_io.STYLE)} vs "
                               f"{(settings['layout'], style)}")
        mp.unlink(missing_ok=True)  # a stale meta must never vouch for a new label file
        t = time.time()
        rs = sg.read_jsonl(sp)
        perms = decoder_io.view_perms(rs, settings["perm_seed"]) if settings["perm_seed"] is not None else None
        preds = decoder_io.predict(model, tok, rs, dev="cuda", **predict_kw, **({} if perms is None else {"perms": perms}))
        if len(preds) != len(rs):
            raise RuntimeError(f"{sp.name}: {len(preds)} predictions for {len(rs)} rows")
        sg.write_atomic(lp, [json.dumps({"id": r["id"], "model": settings["name"], "probs": p,
                                         **({} if perms is None else {"view": perms[i]})})
                             for i, (r, p) in enumerate(zip(rs, preds))])
        sec = time.time() - t
        sg.write_json_atomic(mp, {"shard": sp.name, "rows": len(rs), "shard_sha256": sg._sha_file(sp),
                                  "settings": settings, "style": style,
                                  "sec": round(sec, 1), "rows_per_sec": round(len(rs) / max(sec, 1e-9), 3),
                                  "load": decoder_io.LOAD_INFO if load_info is None else load_info,
                                  "finished_unix": time.time()})
        print(f"{sp.name}: {len(rs)} rows in {sec:.0f}s", flush=True)
        done.append(sp.name)
    return done


def check_done_settings(shards, out_dir, settings):
    """Every finished shard in out_dir must have been labelled with these settings."""
    import shard_golden as sg
    for sp in shards:
        lp, mp = sg.label_paths(out_dir, sp)
        if sg.shard_done(sp, lp, mp):
            old = json.loads(Path(mp).read_text()).get("settings")
            if old != settings:
                raise SystemExit(f"{mp} was labelled with other settings: {old} vs now {settings}")


def label_revision(a):
    """The exact base commit a label job loads: --revision, else the adapter's train_meta base_revision. Must be a
    40-character commit hash, so every (re)start of the ~33 L4-hour job reads the same base (it is part of the settings
    every done shard is checked against)."""
    import decoder_io
    found = decoder_io.adapter_cfg(MODELS / a.name)
    rev = a.revision or ((found[0] if found else {}).get("base_revision") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", rev):
        raise SystemExit(f"label needs --revision <40-character base commit> ({a.name}'s train_meta has "
                         f"{rev or 'no base_revision'!r}); for Qwen/Qwen3.5-4B: {QWEN35_4B_REVISION}")
    return rev


def cmd_label(a):
    if a.offline:  # the default: the base must come from the local cache (pinned snapshot), never the Hub
        os.environ["HF_HUB_OFFLINE"] = "1"
    import decoder_io
    import shard_golden as sg
    sd = Path(a.shards_dir) if Path(a.shards_dir).is_absolute() else HERE / a.shards_dir
    shards = sg.shard_files(sd)
    if not shards:
        raise SystemExit(f"no shards in {sd}")
    rev = label_revision(a)
    out_dir = Path(a.out) if a.out else sd / f"labels_{a.name}{a.tag}"
    kw = tta_kwargs(a)
    settings = {"name": a.name, "base": a.base, "revision": rev, "layout": a.layout,
                "perm_seed": a.perm_seed, **tta_meta(kw), "merged": a.merge}
    # every shard, before --shard narrows the list and before the model load: a per-shard job with other settings
    # fails in seconds instead of mixing views into one label set
    check_done_settings(shards, out_dir, settings)
    if a.shard is not None:
        if not 0 <= a.shard < len(shards):
            raise SystemExit(f"--shard {a.shard}: {len(shards)} shards in {sd}")
        shards = [shards[a.shard]]
    todo = [s for s in shards if not sg.shard_done(s, *sg.label_paths(out_dir, s))]
    if not todo:
        print(f"all {len(shards)} shard(s) already labelled in {out_dir}")
        return
    decoder_io.STYLE = a.style or "cygnet"
    model, tok = decoder_io.load(a.base, "cuda", adapter=str(MODELS / a.name), revision=rev,
                                 layout=a.layout, style=a.style, force=a.force)
    commit = getattr(getattr(model, "config", None), "_commit_hash", None)  # the snapshot actually loaded
    if commit is not None and commit != rev:
        raise RuntimeError(f"loaded base commit {commit}, asked for {rev}")
    if a.merge:
        model = model.merge_and_unload()
    model.eval()
    if decoder_io.LAYOUT != a.layout:
        raise RuntimeError(f"loaded layout {decoder_io.LAYOUT!r}, asked for {a.layout!r}")
    load_info = {**decoder_io.LOAD_INFO, "base_commit": commit}
    print(json.dumps({"label": settings, "style": decoder_io.STYLE, "load": load_info, "shards": len(shards),
                      "todo": len(todo), "out": str(out_dir), **gpu_info()}), flush=True)
    label_shards(model, tok, shards, out_dir, settings, kw, decoder_io.STYLE, load_info)


def parser():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("predict")
    p.add_argument("--name", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--splits", required=True)
    p.add_argument("--style", default=None, help="default: the adapter's train_meta style (cygnet without an adapter)")
    p.add_argument("--tag", default="")
    p.add_argument("--no-adapter", dest="adapter", action="store_false")
    p.add_argument("--layout", default="", help="prompt layout, e.g. schema_branch_mark (layout E); must match train_meta")
    p.add_argument("--revision", default="", help="exact Hugging Face commit of the base (default: train_meta's)")
    p.add_argument("--force", action="store_true", help="override a train_meta conflict (recorded in the meta)")
    p.add_argument("--tta", action="store_true", help="average over the reversed option order (and swapped Yes/No letters)")
    p.add_argument("--tta-choice", dest="tta_choice", action="store_true", help="choice rows: add the reversed order")
    p.add_argument("--tta-noul", dest="tta_noul", action="store_true", help="yes/no rows: add the swapped Yes/No letters")
    p.add_argument("--perm-seed", dest="perm_seed", type=int, default=None,
                   help="read each row in its seeded random view (decoder_io.view_perms)")
    for nm in ("train", "smoke"):
        t = sub.add_parser(nm)
        t.add_argument("--name", default="_smoke")
        t.add_argument("--base", required=True)
        t.add_argument("--recipe", default="A3")
        t.add_argument("--splits", default="")
        t.add_argument("--epochs", type=float, default=1.0)
        t.add_argument("--lr", type=float, default=1e-4)
        t.add_argument("--batch", type=int, default=16)
        t.add_argument("--lam", type=float, default=1.0)
        t.add_argument("--r", type=int, default=16)
        t.add_argument("--beta", type=float, default=1.0)
        t.add_argument("--kd", type=float, default=0.0)
        t.add_argument("--style", default="cygnet")
        t.add_argument("--train-file", dest="train_file", default="train.jsonl")
        t.add_argument("--rel-file", dest="rel_file", default="train_relations.jsonl")
        t.add_argument("--init", default="")
        t.add_argument("--extra", default='{"lam_inv": 1.0, "sym_cons": true, "perm_twin": 0.3, "lam_p": 0.5}')
        t.add_argument("--log-every", dest="log_every", type=int, default=50)
        t.add_argument("--steps", type=int, default=20)
        t.add_argument("--arm", default="", choices=["", "H", "I", "J"], help="PRISM-X preset (prism_x.PRESETS)")
    b = sub.add_parser("blend")
    b.add_argument("--name", required=True)
    b.add_argument("--base", required=True)
    b.add_argument("--adapters", required=True)
    b.add_argument("--weights", required=True)
    b.add_argument("--splits", required=True)
    b.add_argument("--style", default=None)
    b.add_argument("--tag", default="")
    b.add_argument("--layout", default="")
    b.add_argument("--revision", default="")
    b.add_argument("--force", action="store_true")
    l = sub.add_parser("latency")
    l.add_argument("--name", required=True)
    l.add_argument("--base", required=True)
    l.add_argument("--split", default="dev")
    l.add_argument("--style", default=None)
    l.add_argument("--layout", default="")
    l.add_argument("--force", action="store_true")
    r = sub.add_parser("relay", help="resume a relay run's checkpoint on this machine (the L4 tail)")
    r.add_argument("--config", required=True, help="runs/<x>.json, the frozen config")
    r.add_argument("--stop-at-step", dest="stop_at_step", type=int, default=0)
    r.add_argument("--stop-after-min", dest="stop_after_min", type=float, default=0.0)
    lb = sub.add_parser("label", help="sharded, resumable teacher labels (shard_golden.py makes the shards)")
    lb.add_argument("--name", required=True, help="adapter under models/")
    lb.add_argument("--base", required=True)
    lb.add_argument("--layout", required=True, help="asserted against train_meta and before every shard")
    lb.add_argument("--shards-dir", dest="shards_dir", required=True)
    lb.add_argument("--shard", type=int, default=None, help="only this shard index (default: every shard not done)")
    lb.add_argument("--out", default="", help="default: <shards-dir>/labels_<name><tag>")
    lb.add_argument("--tag", default="")
    lb.add_argument("--style", default=None)
    lb.add_argument("--revision", default="", help="40-character base commit (default: the adapter's base_revision)")
    lb.add_argument("--force", action="store_true")
    lb.add_argument("--perm-seed", dest="perm_seed", type=int, default=None,
                    help="one seeded random view per row (plan 3.2 step 3); default: the given order")
    lb.add_argument("--tta", action="store_true")
    lb.add_argument("--tta-choice", dest="tta_choice", action="store_true")
    lb.add_argument("--tta-noul", dest="tta_noul", action="store_true")
    lb.add_argument("--no-merge", dest="merge", action="store_false", help="score the unmerged PEFT model")
    lb.add_argument("--offline", action="store_true", default=True,
                    help="HF_HUB_OFFLINE=1: load the base from the local cache only (the default)")
    lb.add_argument("--online", dest="offline", action="store_false", help="allow Hub downloads (a first download)")
    return ap


COMMANDS = {"predict": cmd_predict, "train": cmd_train, "smoke": cmd_smoke, "latency": cmd_latency, "blend": cmd_blend,
            "relay": cmd_relay, "label": cmd_label}

if __name__ == "__main__":
    a = parser().parse_args()
    COMMANDS[a.cmd](a)
