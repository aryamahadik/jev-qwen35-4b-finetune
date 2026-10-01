"""Write an exact `cat` average of LoRA adapters to disk as ONE ordinary PEFT adapter folder, so that it can be read with
`od_gcp.py predict` (PREREG_FINAL.md 4: every read of a candidate must be a predict read; `od_gcp.py blend` writes a
"blend" meta that the ship rule's pipeline check refuses, and it has no --perm-seed for the _perm read).

The math is PEFT 0.21.0's add_weighted_adapter(combination_type="cat") (peft/tuners/lora/model.py), the same call that
od_gcp.py blend makes:
  new r = sum of the ranks, new lora_alpha = new r (scaling 1.0),
  lora_A = cat([A_i * w_i * scaling_i], dim 0), lora_B = cat([B_i], dim 1), scaling_i = lora_alpha_i / r_i,
  target_modules = "|".join(f"({t_i})") for string target_modules.
So delta W = sum_i w_i * scaling_i * B_i @ A_i exactly (fp32), and the merged model equals od_gcp.py blend's.

The folder gets the first member's tokenizer files and a train_meta.json whose "cfg" is the first member's cfg (so
decoder_io.load resolves the same layout, style, base and base revision), plus a "blend" record (members, weights,
ranks, scalings, sha256 of each member's adapter_model.safetensors). It refuses members that disagree on layout,
style, base or base revision, that carry PRISM-X files, DoRA, rsLoRA, rank/alpha patterns or modules_to_save, or whose
tensor key sets differ.

  python gate/materialize_cat.py --out models/q35_4b_main500k_c2 --weights 0.25,0.25,0.25,0.25 \
      models/q35_4b_main500k/snaps/s025888 models/q35_4b_main500k/snaps/s027411 \
      models/q35_4b_main500k/snaps/s028934 models/q35_4b_main500k
  python gate/materialize_cat.py --out models/q35_4b_main500k_c3 --weights 0.75,0.25 models/q35_4b_main500k models/q35_4b_pxE
  python gate/materialize_cat.py --verify models/q35_4b_main500k_c2     (re-check delta W against the members)
CPU only; needs torch and safetensors (no peft, no GPU, no base model).
"""
import argparse
import datetime
import hashlib
import json
import shutil
import sys
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file

ADAPTER = "adapter_model.safetensors"
TOKENIZER_FILES = ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja", "special_tokens_map.json",
                   "vocab.json", "merges.txt", "added_tokens.json")
PROMPT_KEYS = (("layout", "text_first"), ("style", None), ("base", None), ("base_revision", None))


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_member(d):
    d = Path(d)
    cfg = json.loads((d / "adapter_config.json").read_text())
    bad = [k for k, ok in (("use_dora", not cfg.get("use_dora")), ("use_rslora", not cfg.get("use_rslora")),
                           ("rank_pattern", not cfg.get("rank_pattern")), ("alpha_pattern", not cfg.get("alpha_pattern")),
                           ("modules_to_save", not cfg.get("modules_to_save")),
                           ("fan_in_fan_out", not cfg.get("fan_in_fan_out")),
                           ("peft_type", cfg.get("peft_type") == "LORA"),
                           ("target_modules is a string", isinstance(cfg.get("target_modules"), str))) if not ok]
    if bad:
        sys.exit(f"{d}: unsupported adapter_config ({', '.join(bad)})")
    if any((d / f).exists() for f in ("prism_x.json", "prism_x.safetensors")):
        sys.exit(f"{d}: carries PRISM-X files; a cat average of a PRISM-X adapter is not defined here")
    tm = d / "train_meta.json"
    meta = json.loads(tm.read_text()) if tm.exists() else None
    if not (meta and isinstance(meta.get("cfg"), dict)):
        sys.exit(f"{d}: no train_meta.json with a cfg (the layout it was trained in would be unknown)")
    return {"dir": d, "cfg": cfg, "meta": meta, "r": int(cfg["r"]), "alpha": float(cfg["lora_alpha"]),
            "scaling": float(cfg["lora_alpha"]) / int(cfg["r"]), "sha256": sha256(d / ADAPTER)}


def prompt_of(m):
    c = m["meta"]["cfg"]
    return {k: c.get(k, default) for k, default in PROMPT_KEYS}


def check_agree(members):
    """The members must agree on every prompt key that they set (decoder_io.resolve_prompt's rule)."""
    out = {}
    for k, _ in PROMPT_KEYS:
        vals = {prompt_of(m)[k] for m in members} - {None}
        if len(vals) > 1:
            sys.exit(f"members disagree on {k}: " + ", ".join(f"{m['dir']}={prompt_of(m)[k]!r}" for m in members))
        out[k] = next(iter(vals)) if vals else None
    return out


def keys_of(d):
    with safe_open(str(Path(d) / ADAPTER), "pt") as f:
        return sorted(f.keys())


def pairs(keys):
    """module prefix -> (A key, B key); every lora_A has its lora_B and nothing else is stored."""
    mods = {}
    for k in keys:
        if k.endswith(".lora_A.weight"):
            mods.setdefault(k[: -len(".lora_A.weight")], [None, None])[0] = k
        elif k.endswith(".lora_B.weight"):
            mods.setdefault(k[: -len(".lora_B.weight")], [None, None])[1] = k
        else:
            sys.exit(f"unexpected tensor {k} (only lora_A / lora_B weights are supported)")
    if any(a is None or b is None for a, b in mods.values()):
        sys.exit("a module has lora_A without lora_B or the reverse")
    return mods


def cat_tensors(members, weights):
    keys = keys_of(members[0]["dir"])
    for m in members[1:]:
        if keys_of(m["dir"]) != keys:
            sys.exit(f"{m['dir']}: tensor keys differ from {members[0]['dir']}")
    mods = pairs(keys)
    handles = [safe_open(str(m["dir"] / ADAPTER), "pt") for m in members]
    out = {}
    for mod, (ka, kb) in mods.items():
        As, Bs = [], []
        for m, w, f in zip(members, weights, handles):
            A, B = f.get_tensor(ka), f.get_tensor(kb)
            if A.dtype != torch.float32 or B.dtype != torch.float32:
                sys.exit(f"{m['dir']}: {mod} is {A.dtype}/{B.dtype}, expected float32 (as PEFT saves LoRA weights)")
            if A.shape[0] != m["r"] or B.shape[1] != m["r"]:
                sys.exit(f"{m['dir']}: {mod} rank {A.shape[0]}/{B.shape[1]} != r {m['r']}")
            As.append(A.data * w * m["scaling"])  # PEFT 0.21.0: current_adapter_lora_A.data * weight * target.scaling
            Bs.append(B.data)
        out[ka] = torch.cat(As, dim=0).contiguous()
        out[kb] = torch.cat(Bs, dim=1).contiguous()
    return out, mods


def materialize(member_dirs, weights, out_dir, force=False):
    if len(member_dirs) != len(weights):
        sys.exit(f"{len(member_dirs)} adapters but {len(weights)} weights")
    members = [read_member(d) for d in member_dirs]
    prompt = check_agree(members)
    out_dir = Path(out_dir)
    if out_dir.exists():
        if not force:
            sys.exit(f"{out_dir} exists; pass --force to replace it")
        shutil.rmtree(out_dir)
    tmp = out_dir.with_name(out_dir.name + ".tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    tensors, mods = cat_tensors(members, weights)
    save_file(tensors, str(tmp / ADAPTER), metadata={"format": "pt"})
    new_r = sum(m["r"] for m in members)
    cfg = {**members[0]["cfg"], "r": new_r, "lora_alpha": new_r, "alpha_pattern": {}, "rank_pattern": {},
           "target_modules": "|".join(f"({m['cfg']['target_modules']})" for m in members), "inference_mode": True}
    (tmp / "adapter_config.json").write_text(json.dumps(cfg, indent=2) + "\n")
    tpl = {m["dir"]: sha256(m["dir"] / "chat_template.jinja") if (m["dir"] / "chat_template.jinja").exists() else None
           for m in members}
    if len(set(tpl.values())) > 1:
        sys.exit(f"members have different chat templates: {tpl}")
    for fn in TOKENIZER_FILES:
        if (members[0]["dir"] / fn).exists():
            shutil.copy2(members[0]["dir"] / fn, tmp / fn)
    meta = {"cfg": {**members[0]["meta"]["cfg"], **{k: v for k, v in prompt.items() if v is not None}},
            "blend": {"combination": "cat", "tool": "gate/materialize_cat.py", "peft_equivalent": "0.21.0",
                      "created": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                      "members": [{"dir": str(m["dir"]), "weight": w, "r": m["r"], "lora_alpha": m["alpha"],
                                   "scaling": m["scaling"], "adapter_sha256": m["sha256"],
                                   "train_steps": m["meta"].get("steps"), "snapshot_step": m["meta"].get("snapshot_step")}
                                  for m, w in zip(members, weights)],
                      "modules": len(mods), "new_r": new_r}}
    if "base_revision" in meta["cfg"] and meta["cfg"]["base_revision"] is None:
        del meta["cfg"]["base_revision"]
    (tmp / "train_meta.json").write_text(json.dumps(meta, indent=2, default=str) + "\n")
    tmp.rename(out_dir)
    return out_dir


def verify(out_dir, n_modules=None, tol=1e-5):
    """Recompute delta W = B @ A (scaling 1) of the written folder and compare it, module by module, with
    sum_i w_i * scaling_i * B_i @ A_i of the members named in its train_meta. Returns (modules checked, max relative
    error, max absolute error)."""
    out_dir = Path(out_dir)
    meta = json.loads((out_dir / "train_meta.json").read_text())["blend"]
    cfg = json.loads((out_dir / "adapter_config.json").read_text())
    assert cfg["r"] == cfg["lora_alpha"] == meta["new_r"], "new adapter must have lora_alpha == r (scaling 1)"
    mems = meta["members"]
    for m in mems:
        if sha256(Path(m["dir"]) / ADAPTER) != m["adapter_sha256"]:
            sys.exit(f"{m['dir']}: adapter changed since the blend was written")
    mods = pairs(keys_of(out_dir))
    names = sorted(mods)[: n_modules] if n_modules else sorted(mods)
    fo = safe_open(str(out_dir / ADAPTER), "pt")
    fm = [safe_open(str(Path(m["dir"]) / ADAPTER), "pt") for m in mems]
    worst_rel = worst_abs = 0.0
    for mod in names:
        ka, kb = mods[mod]
        got = fo.get_tensor(kb).double() @ fo.get_tensor(ka).double()
        want = sum(m["weight"] * m["scaling"] * (f.get_tensor(kb).double() @ f.get_tensor(ka).double())
                   for m, f in zip(mems, fm))
        err = (got - want).abs().max().item()
        rel = err / max(want.abs().max().item(), 1e-30)
        worst_abs, worst_rel = max(worst_abs, err), max(worst_rel, rel)
    if worst_rel > tol:
        sys.exit(f"verify FAILED: max relative error {worst_rel:.3e} > {tol}")
    return len(names), worst_rel, worst_abs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("adapters", nargs="*", help="member adapter folders, in order (the first gives cfg and tokenizer)")
    ap.add_argument("--weights", default="", help="comma list, one per adapter")
    ap.add_argument("--out", default="", help="output adapter folder (written via <out>.tmp then renamed)")
    ap.add_argument("--force", action="store_true", help="replace an existing --out folder")
    ap.add_argument("--verify", default="", help="only verify an existing materialized folder")
    ap.add_argument("--verify-modules", type=int, default=0, help="verify only the first N modules (0 = all)")
    a = ap.parse_args(argv)
    if a.verify:
        n, rel, ab = verify(a.verify, a.verify_modules or None)
        print(json.dumps({"verify": a.verify, "modules": n, "max_rel_err": rel, "max_abs_err": ab, "ok": True}))
        return
    if not (a.adapters and a.weights and a.out):
        ap.error("adapters, --weights and --out are required")
    out = materialize(a.adapters, [float(x) for x in a.weights.split(",")], a.out, a.force)
    n, rel, ab = verify(out, a.verify_modules or None)
    print(json.dumps({"wrote": str(out), "adapter_sha256": sha256(out / ADAPTER), "modules": n, "max_rel_err": rel,
                      "max_abs_err": ab}))


if __name__ == "__main__":
    main()
