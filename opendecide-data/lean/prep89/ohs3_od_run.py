"""(b) Run one OpenDecide model on OHS-3 ONCE, blind, with the pre-registered A5 readout. Meant for the L4 VM
(backend real); the CPU dry run uses --backend tiny / oracle on the synthetic root.

  REAL, on the L4 (after the owner's GO and after the PREREG_OHS3 model amendment is committed):
    cd ~/lean && python prep89/ohs3_od_run.py --config prep89/ohs3_config.json --model-key 4b \\
        --config-sha256 <sha256 printed by ohs3_preflight.py and written in the amendment> --go
  DRY RUN:
    ../.venv/bin/python prep89/ohs3_od_run.py --root prep89/dryrun/root --config prep89/dryrun/config_dryrun.json \\
        --model-key 4b --backend tiny

Writes preds_ohs3/ (the score_ohs3.py inputs), every file one record per row in data order, as od_gcp.py writes them:
  <name>.jsonl            the A5 readout before T (2-view averaged on the choice rows A5 names)
  <name>_cal.jsonl        PRIMARY configuration (PREREG_OHS3 rule 4): the readout with the pre-registered T
  <name>_cal_bc.jsonl     SECONDARY configuration: batchcal.py (unchanged) on <name>_cal
  <name>_1v.jsonl         the identity view alone (by-product of the same reads; A5 item 1 "single read" secondary)
  <name>_1v_cal.jsonl     the identity view with the single-read T
  + .meta.json for each (config sha256, adapter sha256, code sha256, GPU, readout, T, timings, run id, and the
    run's input-token counts: identity read and all reads, from the encodes cand_logits made; counts only)
The identity view is saved next to the 2-view average from the SAME reads (a5_read keeps it); the dry run checks
<name>_1v equals decoder_io.predict() and <name> equals decoder_io.predict(tta_choice=True) on the same rows.
Real-mode guards before any row is read: config sha256 = the amendment's, frozen OHS-3 hashes, the Mac's code manifest
(which also lists the model's T fit log), and T_primary / T_single = that dev-only t_rule_check.py log
(ohs3_lib.require_fit_logs); for a PRISM-X model the loader checks prism_x.safetensors' sha256 too.
Rule 4 (one run per model): a completed run in logs/ohs3_runs.jsonl or an existing preds file stops the script. A
run interrupted part-way (pre-emption) resumes from preds_ohs3/<name>.partial.jsonl, only with the same run id
(config sha256 + adapter sha256 + backend); the reads are deterministic, so a resume is the same single run.
Blind: prints counts and timings only; it never reads gold (except the synthetic oracle backend) and never prints text.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_backends as B  # noqa: E402
import ohs3_lib as L  # noqa: E402

CODE_FILES = ("decoder_io.py", "prism_x.py", "writeblock.py", "calibrate.py", "batchcal.py")


def check_code(manifest_path, cfg):
    """Every file in the Mac's manifest has the same sha256 here, and the manifest names this config."""
    man = json.loads(Path(manifest_path).read_text())
    bad = {rel: "missing" if not (L.LEAN / rel).exists() else "differs" for rel, sha in man["files"].items()
           if not (L.LEAN / rel).exists() or L.sha256_file(L.LEAN / rel) != sha}
    if man.get("config_sha256") not in (None, cfg["_sha256"]):
        bad["config"] = "manifest made for another config"
    if bad:
        raise SystemExit(f"STOP: code here differs from the Mac manifest: {bad}")
    L.blind_print(f"code manifest: {len(man['files'])} files match the Mac's sha256")


def out_files(pd, name):
    return {k: pd / f"{name}{k}.jsonl" for k in ("", "_cal", "_cal_bc", "_1v", "_1v_cal")}


def write_outputs(root, name, rows, p1, pr, m, meta_extra):
    """The five preds files + metas of one OpenDecide OHS-3 run (batch or served): p1 / pr = {row id: identity view /
    A5 readout, both before T}. Returns {suffix: sha256}."""
    pd = Path(root) / f"preds_{L.SPLIT}"
    outs = out_files(pd, name)
    files = {
        "": [{"id": r["id"], "model": name, "probs": pr[r["id"]]} for r in rows],
        "_cal": [{"id": r["id"], "model": f"{name}_cal", "probs": L.apply_T(pr[r["id"]], r, m["T_primary"])} for r in rows],
        "_1v": [{"id": r["id"], "model": f"{name}_1v", "probs": p1[r["id"]]} for r in rows],
        "_1v_cal": [{"id": r["id"], "model": f"{name}_1v_cal", "probs": L.apply_T(p1[r["id"]], r, m["T_single"])}
                    for r in rows],
    }
    code = {fn: L.sha256_file(L.LEAN / fn) for fn in CODE_FILES if (L.LEAN / fn).exists()}
    code.update({f"prep89/{p.name}": L.sha256_file(p) for p in sorted(L.PREP.glob("ohs3_*.py"))})
    meta = {"name": name, "rows": len(rows), "split": L.SPLIT, "base": m["base"], "revision": m["revision"],
            "layout": m["layout"], "style": m["style"], "adapter_sha256_preregistered": m["adapter_sha256"],
            "readout_choice": m["readout_choice"], "readout_noul": "single", "T_primary": m["T_primary"],
            "T_single": m["T_single"], "code_sha256": code, "host": os.uname().nodename, "finished_utc": L.utc(),
            "prereg": "PREREG_OHS3.md rule 4 + amendment A5", **meta_extra}
    descr = {"": "A5 readout before T", "_cal": "PRIMARY: A5 readout + T_primary",
             "_1v": "identity view (single read) before T", "_1v_cal": "identity view + T_single"}
    for k, recs_out in files.items():
        L.write_jsonl_atomic(outs[k], recs_out)
        (pd / f"{name}{k}.meta.json").write_text(json.dumps({**meta, "file": outs[k].name, "what": descr[k]}, indent=2))
    # SECONDARY configuration: the unchanged batchcal.py on the primary preds (a byte-identical copy in a dry root)
    root = Path(root).resolve()
    bc = root / "batchcal.py"
    if root != L.LEAN.resolve():
        if not bc.exists() or L.sha256_file(bc) != L.sha256_file(L.LEAN / "batchcal.py"):
            shutil.copyfile(L.LEAN / "batchcal.py", bc)
    r = subprocess.run([str(L.PY) if L.PY.exists() else sys.executable, str(bc), L.SPLIT, f"{name}_cal"], cwd=str(root),
                       capture_output=True, text=True)
    if r.returncode != 0 or not outs["_cal_bc"].exists():
        raise SystemExit(f"batchcal.py failed (exit {r.returncode}); the primary files are written")
    L.blind_print("  " + r.stdout.strip()[:300])
    (pd / f"{name}_cal_bc.meta.json").write_text(json.dumps({**meta, "file": outs["_cal_bc"].name,
                                                            "what": "SECONDARY: batchcal.py on the primary",
                                                            "batchcal_sha256": L.sha256_file(bc)}, indent=2))
    return {k: L.sha256_file(p) for k, p in outs.items()}


def token_summary(rows, recs):
    """Counts only (no text): the input tokens of this run's reads, from the tokenizer encodes cand_logits made.
    first_view = the identity read; total = every read (the reversed read on 2-view rows too); output tokens = 0."""
    by = {"noul": [0, 0, 0, 0], "choice": [0, 0, 0, 0]}  # rows, first-view tokens, all tokens, reads
    for r in rows:
        t = recs.get(r["id"], {}).get("tok")
        if t is None:
            continue
        b = by[r["qtype"]]
        b[0] += 1
        b[1] += t[0]
        b[2] += t[1]
        b[3] += t[2]
    n, f, tot, rd = (sum(b[i] for b in by.values()) for i in range(4))
    out = {"rows_counted": n, "rows": len(rows), "input_tokens_first_view": f, "input_tokens_all_reads": tot,
           "output_tokens": 0, "reads": rd, "all_reads_over_first_view": round(tot / f, 4) if f else None,
           "per_row_mean_all_reads": round(tot / n, 1) if n else None,
           "by_qtype": {q: {"rows": b[0], "first_view": b[1], "all_reads": b[2], "reads": b[3]} for q, b in by.items()},
           "note": "0 tokens = a backend without a tokenizer (synthetic oracle)"}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(L.LEAN))
    ap.add_argument("--config", required=True)
    ap.add_argument("--model-key", required=True, help="a key of config.models (e.g. 4b, 2b)")
    ap.add_argument("--backend", default="real", choices=["real", "tiny", "tiny_px", "oracle"])
    ap.add_argument("--config-sha256", default=None, help="real: the sha256 written in the PREREG_OHS3 amendment")
    ap.add_argument("--models-dir", default=None, help="default <lean>/models")
    ap.add_argument("--chunk", type=int, default=512)
    ap.add_argument("--stop-after-chunks", type=int, default=0, help="test only: simulate an interruption")
    ap.add_argument("--code-manifest", default=None,
                    help="real: prep89/ohs3_code_manifest.json from ohs3_preflight.py on the Mac; every listed file "
                         "here must have that sha256 (the L4 is not a git checkout)")
    ap.add_argument("--check-only", action="store_true",
                    help="pre-GO on the VM: config sha256, frozen files, code manifest, rule 4; loads no model, reads no row")
    ap.add_argument("--go", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    real = L.is_real_ohs3(root)
    cfg = L.load_config(a.config, require_complete=True, model_keys=[a.model_key])
    m = cfg["models"][a.model_key]
    name = m["name"]
    if real:
        if not a.go and not a.check_only:
            raise SystemExit("REAL OHS-3: needs --go (owner's GO, after the PREREG_OHS3 model amendment is committed)")
        if a.backend != "real":
            raise SystemExit("REAL OHS-3 runs only with --backend real")
        if a.config_sha256 != cfg["_sha256"]:
            raise SystemExit(f"config sha256 {cfg['_sha256'][:16]} != --config-sha256 (the amendment's value)")
        if cfg["decisions"]["od_scored_run"] != "L4_batch":
            raise SystemExit(f"STOP (rule 4): decisions.od_scored_run = {cfg['decisions']['od_scored_run']}: the scored "
                             "run is the served H100 pass, so an L4 batch run would be a second OHS-3 pass")
        L.require_frozen(root)
        if not a.code_manifest:
            raise SystemExit("REAL OHS-3: needs --code-manifest (prep89/ohs3_code_manifest.json from the Mac preflight)")
        check_code(a.code_manifest, cfg)
        # T == the dev-only t_rule_check log (its sha256 is in the manifest); the dev reads are re-hashed on the Mac
        L.require_fit_logs(cfg, [a.model_key], rehash=False)
    else:
        L.require_synthetic(root)
    pd = root / f"preds_{L.SPLIT}"
    outs = out_files(pd, name)
    if L.completed_runs(root, name) or any(p.exists() for p in outs.values()):
        raise SystemExit(f"STOP (PREREG_OHS3 rule 4): {name} already has a completed OHS-3 run or preds files")
    if a.check_only:
        part = pd / f"{name}.partial.jsonl"
        ad = Path(a.models_dir or L.LEAN / "models") / name / "adapter_model.safetensors"
        ad_ok = ad.exists() and L.sha256_file(ad) == m["adapter_sha256"]
        if a.backend == "real" and not ad_ok:
            raise SystemExit(f"CHECK FAILED: {ad} missing or its sha256 differs from the pre-registered one")
        L.blind_print(f"CHECK OK: {name}, config {cfg['_sha256'][:16]}, frozen files ok={real}, adapter sha256 ok="
                      f"{ad_ok}, partial run to resume: {part.exists()}")
        return {"check_only": True}
    pd.mkdir(parents=True, exist_ok=True)
    rows = L.read_jsonl(root / "data" / f"{L.SPLIT}.jsonl")
    if real or a.backend != "oracle":  # blind: the model never needs gold (only the synthetic oracle reads it)
        for r in rows:
            r.pop("gold", None)
    run_id = L.sha256_bytes(f"{cfg['_sha256']}:{name}:{m['adapter_sha256']}:{a.backend}".encode())[:16]
    partial = pd / f"{name}.partial.jsonl"
    done = {}
    if partial.exists():
        recs = L.read_jsonl(partial)
        if not recs or recs[0].get("run_id") != run_id:
            raise SystemExit(f"{partial.name} belongs to another run (run id differs): refusing to mix runs")
        done = {r["id"]: r for r in recs[1:]}
        L.blind_print(f"resuming run {run_id}: {len(done)}/{len(rows)} rows already read")
    else:
        with open(partial, "w") as f:
            f.write(json.dumps({"run_id": run_id, "name": name, "config_sha256": cfg["_sha256"], "utc": L.utc()}) + "\n")
    L.ledger_append(root, {"name": name, "status": "start" if not done else "resume", "run_id": run_id,
                           "config_sha256": cfg["_sha256"], "backend": a.backend, "rows_done": len(done)})
    t_load = time.time()
    be = B.load_backend(a.backend, m, root, a.models_dir)
    load_s = round(time.time() - t_load, 1)
    readout = m["readout_choice"]
    L.blind_print(f"{name}: backend {a.backend}, readout choice={readout} yes/no=single, T={m['T_primary']}, "
                  f"T_single={m['T_single']}, load {load_s}s, rows {len(rows)}")
    # predict()'s global order, cut into chunks: each chunk is batched exactly as decoder_io.predict batches it
    order = [i for b in L.predict_batches(rows) for i in b]
    todo = [i for i in order if rows[i]["id"] not in done]
    chunks = [todo[s:s + a.chunk] for s in range(0, len(todo), a.chunk)]
    t0 = time.time()
    for ci, ch in enumerate(chunks):
        part = [rows[i] for i in ch]
        tc = time.time()
        usage = L.new_usage(len(part))
        p1, pr = L.a5_read(be["dio"], be["model"], be["ro"], part, be["dev"], readout, usage=usage)
        with open(partial, "a") as f:
            for r, x, y, u in zip(part, p1, pr, usage["rows"]):
                f.write(json.dumps({"id": r["id"], "p1": x, "pr": y,
                                    "tok": [u["first_view"], u["total"], u["reads"]]}) + "\n")
            f.flush()
            os.fsync(f.fileno())
        L.blind_print(f"  chunk {ci + 1}/{len(chunks)}: {len(part)} rows in {time.time() - tc:.1f}s")
        if a.stop_after_chunks and ci + 1 >= a.stop_after_chunks:
            L.blind_print(f"  stopped after {ci + 1} chunks (--stop-after-chunks); re-run to resume")
            return {"stopped": True, "run_id": run_id}
    recs = {r["id"]: r for r in L.read_jsonl(partial)[1:]}
    missing = [r["id"] for r in rows if r["id"] not in recs]
    if missing:
        raise SystemExit(f"{len(missing)} rows have no read: re-run to resume")
    sec = round(time.time() - t0, 1)
    meta = {"run_id": run_id, "config": cfg["_path"], "config_sha256": cfg["_sha256"], "model_key": a.model_key,
            "backend": be["info"], "load_s": load_s, "read_s_this_session": sec, "resumed_rows": len(done),
            "path": "batch (decoder_io.predict batching, ohs3_lib.a5_read)", "tokens": token_summary(rows, recs)}
    shas = write_outputs(root, name, rows, {i: r["p1"] for i, r in recs.items()}, {i: r["pr"] for i, r in recs.items()},
                         m, meta)
    shutil.move(str(partial), str(pd / f"{name}.partial.done.jsonl"))
    L.ledger_append(root, {"name": name, "status": "complete", "run_id": run_id, "config_sha256": cfg["_sha256"],
                           "backend": a.backend, "files_sha256": shas})
    L.blind_print(f"{name}: wrote {', '.join(p.name for p in outs.values())}; reads {sec}s")
    return {"run_id": run_id, "files": {k: str(p) for k, p in outs.items()}, "sha256": shas}


if __name__ == "__main__":
    main()
