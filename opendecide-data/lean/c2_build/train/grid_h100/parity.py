"""grid_h100.parity: the merged-vs-HF-adapter parity check (>= 99.5%) for the CHOSEN candidate, in its own H100 container.

The grid reads are served from merge_direct merges (fast, CPU); the production model will be the chosen candidate merged and served on the
S1 path. This check ties the two together exactly as P7 / A49 (f) tie C1's merge to its adapter (c2_build/serving/merge_parity.py parity):
  * the candidate's adapter is rebuilt from the checkpoints and must have the sha256 CANDIDATE_C2.json records;
  * reference: the PEFT adapter on the pinned base, merge_and_unload, decoder_io.predict(tta_choice) = od_gcp.py predict --tta-choice
    (hf_ref.py, C1's pinned stack) on a seeded sample of >= 2,000 rows of a NON-dev, non-sealed split (default: the G-block, data/
    gblock_a42d_c1read.jsonl; its rows carry no gold, so the label is the reference's argmax);
  * served: the merge on the frozen S1 command (same boot checks as the grid), choice rows in both orders (A5 readout), the same rows;
  * bar (merge_parity.verdict): argmax agreement >= 99.5% AND |d p(label)| <= 0.02 on >= 99% of rows, n >= 2000; the record names the
    served model path, merge manifest sha, config / path hashes and the split / reference shas.
The comparison functions are merge_parity's own (compare, accuracy_diff, check_ref_meta, verdict, sample_rows).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

from . import common as C
from . import gridbuild as GB
from . import hostops as HO
from . import merge_direct as MD
from . import servers as SV
from .session import ReaderProc, SessionRefused


def run_hf_ref(spec: dict, out_json: str, python: str = C.FASTPATH_PY, root: str = "/root", timeout_s: float = 3000.0, log=print) -> dict:
    import os
    sp = Path(out_json).with_suffix(".spec.json")
    C.write_json(sp, spec)
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "VIRTUAL_ENV")}
    env.update({"PYTHONPATH": root, "TOKENIZERS_PARALLELISM": "false", "HF_HUB_OFFLINE": "1", "OD_LEAN": str(C.LEAN)})
    r = subprocess.run([python, "-m", "grid_h100.hf_ref", "--spec", str(sp), "--out", out_json], cwd=root, env=env,
                       capture_output=True, text=True, timeout=timeout_s)
    log((r.stdout or "")[-1500:])
    try:
        return json.loads(Path(out_json).read_text())
    except (OSError, ValueError):
        return {"ok": False, "error": f"hf_ref produced no result (rc {r.returncode}): {(r.stderr or '')[-600:]}"}


def parity_record(sample: list, ref: list, got: list, ref_meta: dict | None, views: int, n: int, seed: int, min_n: int,
                  mp=None) -> dict:
    """merge_parity.run_parity's body on files already read (identical fields and the same bar)."""
    mp = mp or SV.serving_mod("merge_parity")
    import hashlib
    bad = [r["id"] for r, g, rf in zip(sample, got, ref) if set(rf) != set(g)]
    if bad:
        raise SystemExit(f"parity: option keys differ from the reference on {len(bad)} rows, e.g. {bad[:3]}")
    out = {"seed": seed, "n": n, "views": views,
           "sample_ids_sha256": hashlib.sha256("\n".join(r["id"] for r in sample).encode()).hexdigest(),
           "label_definition": "the HF adapter reference's argmax answer", "all": mp.compare(ref, got),
           "ref_meta_problems": mp.check_ref_meta(ref_meta, views)}
    for t_ in ("choice", "noul"):
        idx = [i for i, r in enumerate(sample) if r["qtype"] == t_]
        out[t_] = mp.compare([ref[i] for i in idx], [got[i] for i in idx])
    out["accuracy"] = mp.accuracy_diff(sample, ref, got)
    out["disagreements"] = [{"id": r["id"], "qtype": r["qtype"],
                             "ref_margin": round(sorted(rf.values(), reverse=True)[0] - sorted(rf.values(), reverse=True)[1], 4),
                             "served_margin": round(sorted(g.values(), reverse=True)[0] - sorted(g.values(), reverse=True)[1], 4)}
                            for r, rf, g in zip(sample, ref, got) if mp.argmax(rf) != mp.argmax(g)][:60]
    out["bar"] = mp.verdict(out["all"], n, out["accuracy"], min_n)
    if out["ref_meta_problems"]:
        out["bar"]["PASS"] = out["bar"]["PASS_strict"] = out["bar"]["PASS_gate"] = False
    return out


class ParitySession:
    def __init__(self, pplan: dict, emit=lambda ev: None, hooks: dict | None = None, clock=time.time, rate_usd_h: float = C.FN_RATE_USD_H,
                 prior_usd: float = 0.0, out_root="/out/runs", work_root="/tmp/parity_work", vol="/vol", data_dir="/root/data",
                 c1tok_dir="/root/c1tok", commit=lambda: None, log=print, stop_launch: float = C.STOP_LAUNCH_USD,
                 hard_stop: float = C.HARD_STOP_USD):
        from .session import real_hooks
        self.p, self.emit, self.h = pplan, emit, {**real_hooks(), "hf_ref": run_hf_ref, **(hooks or {})}
        self.clock, self.rate, self.prior = clock, rate_usd_h, prior_usd
        self.out = Path(out_root) / pplan["run_id"] / "parity" / pplan["cand"]
        self.work, self.vol = Path(work_root), Path(vol)
        self.data_dir, self.c1tok_dir = Path(data_dir), Path(c1tok_dir)
        self.commit, self.log = commit, log
        self.stop_launch, self.hard_stop = stop_launch, hard_stop
        self.t0 = clock()

    def spent(self) -> float:
        return self.prior + C.container_cost_usd(self.clock() - self.t0, self.rate)

    def ev(self, kind, **kw):
        self.emit({"event": kind, "t": round(self.clock() - self.t0, 1), "spent_usd": round(self.spent(), 3), **kw})

    def run(self) -> dict:
        p, h = self.p, self.h
        C.check_names(p["cand"], p["split"])
        gpu = h["gpu_name"]()
        HO.check_gpu(gpu)
        ver = h["sglang_version"]()
        if ver != C.SGLANG_VERSION:
            raise SessionRefused(f"sglang {ver!r} != pinned {C.SGLANG_VERSION}")
        tv = h["torch_versions"]()
        pin = h["load_pin"]()
        self.ev("container_up", gpu=gpu, **tv)
        split_path = self.data_dir / p["split_file"]
        if C.sha256_file(split_path) != p["split_sha256"]:
            raise SessionRefused(f"{p['split_file']} differs from the plan's sha256")
        base = h["prepare_base"](str(self.vol / "hf"), str(self.work / "base"), self.log)
        c1_tok = h["prepare_c1_tok"](self.c1tok_dir, (pin.get("model") or {}).get("tokenizer_pins") or {})
        c1_dir = GB.locate_c1_adapter()
        run_dir = Path(p["c2_run_dir"])
        ri = GB.check_run_dir(run_dir, (pin.get("model") or {}).get("tokenizer_pins") or {})
        if ri["problems"]:
            raise SessionRefused("the C2 run folder is not usable: " + "; ".join(ri["problems"]))
        cand_dir = self.work / "cand"
        if cand_dir.exists():
            shutil.rmtree(cand_dir)
        built = GB.build_one(c1_dir, run_dir, p["cand"], cand_dir, p["grid_record"])
        if built["adapter_sha256"] != p["expect_adapter_sha256"]:
            raise SessionRefused(f"{p['cand']} rebuilt with sha256 {built['adapter_sha256'][:16]}, CANDIDATE_C2.json says "
                                 f"{p['expect_adapter_sha256'][:16]}")
        self.ev("candidate_built", **built)
        mdir = self.work / "merged" / p["read_name"]
        man = h["merge"](base["base_dir"], str(cand_dir), str(mdir), str(c1_tok), label=p["read_name"], dev="cpu",
                         expect_adapter_sha=p["expect_adapter_sha256"], log=self.log)
        man_sha = C.sha256_file(mdir / MD.MANIFEST)
        # sample, HF reference
        mp = SV.serving_mod("merge_parity")
        rows_all = [json.loads(l) for l in open(C.safe_path(split_path)) if l.strip()]
        sample = mp.sample_rows(rows_all, p["n"], p["seed"])
        rows_file = self.work / "sample.jsonl"
        C.write_jsonl(rows_file, sample)
        ref_dir = self.out / "ref"
        ref_dir.mkdir(parents=True, exist_ok=True)
        ref_name = p["read_name"] + "_hfref"
        ok, why = self.gate(float(p.get("est_hf_usd", 0.3)))
        if not ok:
            raise SessionRefused(why)
        res = h["hf_ref"]({"hf_home": str(self.work / "hf_home"), "base_dir": base["base_dir"], "adapter_dir": str(cand_dir),
                           "rows_file": str(rows_file), "name": ref_name, "out_dir": str(ref_dir)}, str(self.out / "hf_ref_result.json"))
        if not res.get("ok"):
            raise SessionRefused("HF reference failed: " + str(res.get("error")))
        self.ev("hf_ref_done", **{k: res.get(k) for k in ("rows", "sec", "load_s")})
        refp = {x["id"]: x["probs"] for x in (json.loads(l) for l in open(ref_dir / f"{ref_name}.jsonl") if l.strip())}
        ref_meta = json.loads((ref_dir / f"{ref_name}.meta.json").read_text())
        # served
        ok, why = self.gate(float(p.get("est_served_usd", 0.25)))
        if not ok:
            raise SessionRefused(why)
        spec = {"c1_dir": str(c1_tok), "data_dir": str(self.data_dir), "sets": [], "manifest": {}, "recorded_check": p["prompt_check_record"],
                "ctl_dir": str(self.work / "reader_ctl"), "port": C.PORT}
        reader = h["reader"](spec, self.log)
        srv = h["server_cls"](mdir, log=self.log, log_file=str(self.out / "sglang.log"))
        hashed = {}
        th = threading.Thread(target=lambda: hashed.update(problems=MD.verify_files(mdir, man)), daemon=True)
        try:
            th.start()
            srv.start()
            reader.wait_ready(900.0)
            boot_s = srv.wait_ready(900.0)
            info = srv.server_info()
            bad, warn = srv.check(info, pin)
            if bad:
                raise SessionRefused("resolved server args refused: " + "; ".join(bad))
            th.join(timeout=600)
            if th.is_alive() or hashed.get("problems"):
                raise SessionRefused(f"merged checkpoint differs from its manifest: {hashed.get('problems') or 'timeout'}")
            s1 = SV.serving_mod("s1_pin")
            hs = s1.hashes(info, srv.env)
            ident = mp.served_identity(info, p["expect_adapter_sha256"])
            srv.flush()
            served_file = self.out / "served.jsonl"
            r = reader.run({"op": "read_rows", "rows_file": str(rows_file), "views": int(p["views"]), "out": str(served_file),
                            "name": p["read_name"]}, timeout_s=1800.0)
            if not r.get("ok"):
                raise SessionRefused("served read failed: " + str(r.get("error")))
            info_after = srv.server_info()
            after = s1.hashes(info_after, srv.env)["config_sha256"]
            gotp = {x["id"]: x["probs"] for x in (json.loads(l) for l in open(served_file) if l.strip())}
        finally:
            try:
                reader.quit()
            except Exception:  # noqa: BLE001
                pass
            srv.stop()
            shutil.rmtree(mdir, ignore_errors=True)
        rec = parity_record(sample, [refp[x["id"]] for x in sample], [gotp[x["id"]] for x in sample], ref_meta, int(p["views"]),
                            p["n"], p["seed"], p["min_n"], mp)
        rec.update({"cand": p["cand"], "read_name": p["read_name"], "adapter_sha256": p["expect_adapter_sha256"],
                    "split": p["split"], "split_file": p["split_file"], "split_sha256": p["split_sha256"],
                    "ref_sha256": C.sha256_file(ref_dir / f"{ref_name}.jsonl"), "served_sha256": C.sha256_file(served_file),
                    "merge_manifest_sha256": man_sha, "merge_s": man.get("merge_s"),
                    **ident, "server_info_path_sha256": hs["path_sha256"], "config_sha256": hs["config_sha256"], "boot_s": boot_s,
                    "gpu": gpu, **tv, "run_id": p["run_id"], "utc": C.utc(), "spent_usd": round(self.spent(), 3)})
        if after != hs["config_sha256"]:
            rec["bar"]["PASS"] = rec["bar"]["PASS_strict"] = rec["bar"]["PASS_gate"] = False
            rec["served_problems"] = ["server config changed during the parity read"]
        C.write_json(self.out / f"PARITY_{p['cand']}.json", rec)
        self.commit()
        self.ev("parity_done", PASS=rec["bar"]["PASS"], PASS_gate=rec["bar"]["PASS_gate"], argmax=rec["all"].get("argmax_agree"))
        return rec

    def gate(self, extra_usd: float) -> tuple:
        s = self.spent()
        if s >= self.hard_stop:
            return False, f"hard stop: spent ${s:.2f} >= ${self.hard_stop:.2f}"
        if s + extra_usd > self.stop_launch:
            return False, f"budget gate: spent ${s:.2f} + estimate ${extra_usd:.2f} > stop-launch ${self.stop_launch:.2f}"
        return True, "ok"
