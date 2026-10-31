"""grid_h100.plan: the read plan, the data manifest and the wall-time / cost estimate of the A42-D 9 grid reads. CPU only.

What is read, for each of the 19 models (C1 as the reference + the 18 candidates), every one on the SAME H100 in the SAME job:
  A  no TTA (views 1, perm None)   the 9 gate dev splits + eval_jagged + eval_opi + the 3 C2 dev sets (c2_mixdev merged, c2_transfer_dev,
                                   c2_t37b_dev)                      -> preds_<split>/<read name>.jsonl
  B  permuted view (perm seed 1)   the 9 gate dev splits             -> preds_<split>/<read name>_perm.jsonl   (D5)
  C  --tta-choice (choice 2 views) the G-proxy (data/c2_gproxy/pab_gproxy.jsonl) + any own dev split -> preds_pab_gproxy/<read name>.jsonl
These are exactly the jobs A, B, C of grid_plan.jobs_for (the L4 plan), on the S1 server instead of od_gcp.py predict.

Estimate. Measured: 17 Oct 2026 H100 window (HANDOFF; lean/speed/opt_c1_round2_20261017/h100): S1 reads the 8,143-row parity set P (the 9 gate
dev splits, A18.2 readout = 11,957 sequences) at 325,826 decisions/h at concurrency 64 = 89.97 s. Everything else here is scaled from that
by the work in the sequences (max of the sequence-count and the character-count scaling, so the heavier of the two is used). The boot time
(~2 min per model), merge, latency run and stop times are stated assumptions [E]; the three scenarios vary them. Nothing here was run.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import common as C

SPLITS9 = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev")
ATTACKS = ("eval_jagged", "eval_opi")
C2_DEV = ("c2_mixdev", "c2_transfer_dev", "c2_t37b_dev")            # gate_c2.MIXDEV / TRANSFER / T37B_DEV
GPROXY_SPLIT, GPROXY_FILE = "pab_gproxy", "c2_gproxy/pab_gproxy.jsonl"
EXTRA_FILES = ("c2_t37b_dev_relations.jsonl", "c2_gproxy/pab_gproxy_relations.jsonl")     # hashed into the manifest, not read
PERM_SEED, PERM_TAG = 1, "_perm"
FINAL = "final_a10"

# measured: 17 Oct 2026 H100, S1, parity set P (hosting/speed_bench workloads), c64
P_DEC_H = 325_826
P_ROWS = 8143
ASSUME = {   # [E] = assumption, not a measurement; low / likely / high
    "boot_s": (90, 120, 180),                 # "boot ~2 min per model" (owner's brief); 17 Oct B1a boots were 2-3 min with a warm Triton cache
    "read_factor": (0.85, 1.0, 1.4),          # x the scaled P time (cold radix cache each boot, heavier rows, 2 sets of tokenisation overlap)
    "latency_s": (20, 30, 45),                # flush + 20 warm-up + 400 batch-1 calls at ~30-40 ms (17 Oct: p50 29.9 ms)
    "stop_handoff_s": (10, 15, 30),
    "first_merge_s": (45, 75, 150),           # the first model's merge cannot be hidden behind a previous model's reads
    "base_setup_s": (60, 90, 180),            # base snapshot copy + 12-pin check (Volume -> local disk)
    "grid_rebuild_s": (60, 120, 240),         # merge_avg.build_grid on 8 checkpoints + C1 (CPU), sha check
}
PARITY_ASSUME = {"fixed_s": (420, 560, 900)}  # container, base, one candidate build + merge, HF load + 2,000-row HF read, S1 boot + read


# ------------------------------------------------------------------ data
def split_path(data_root: Path, split: str) -> Path:
    C.check_names(split)
    return Path(data_root) / (GPROXY_FILE if split == GPROXY_SPLIT else f"{split}.jsonl")


def set_specs(own_dev=()) -> list:
    """The read sets, in the order a model is read. views = choice views (1 = given order only, 2 = given + exact reversal)."""
    specs = []
    for sp in (*SPLITS9, *ATTACKS, *C2_DEV):
        specs.append({"split": sp, "tag": "", "views": 1, "perm_seed": None, "job": "A"})
    for sp in SPLITS9:
        specs.append({"split": sp, "tag": PERM_TAG, "views": 1, "perm_seed": PERM_SEED, "job": "B"})
    for sp in (GPROXY_SPLIT, *own_dev):
        specs.append({"split": sp, "tag": "", "views": 2, "perm_seed": None, "job": "C"})
    for s in specs:
        s["file"] = GPROXY_FILE if s["split"] == GPROXY_SPLIT else f"{s['split']}.jsonl"
        s["pred_dir"] = f"preds_{s['split']}"
        s["tta_choice"] = s["views"] == 2
    return specs


def row_work(r: dict, views: int) -> tuple:
    """(sequences, characters) of one row: choice rows are read twice when views == 2."""
    n = 2 if (views == 2 and r.get("qtype") == "choice") else 1
    chars = len(r.get("state") or "") + len(r.get("card") or "") + len(r.get("instructions") or "") + \
        sum(len(o) for o in (r.get("options") or []))
    return n, n * chars


def scan_split(path: Path, views: int) -> dict:
    rows = seq = chars = ch = 0
    with open(C.safe_path(path)) as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            n, c = row_work(r, views)
            rows += 1
            seq += n
            chars += c
            ch += r.get("qtype") == "choice"
    return {"rows": rows, "seq": seq, "chars": chars, "choice_rows": ch}


def data_manifest(data_root: Path, specs: list, extra=EXTRA_FILES) -> dict:
    """{relative file: {sha256, rows, bytes}} for every read file and the relation files (so a run record binds the exact data)."""
    out = {}
    for rel in sorted({s["file"] for s in specs} | set(extra)):
        p = C.safe_path(Path(data_root) / rel)
        if not p.exists():
            out[rel] = {"missing": True}
            continue
        out[rel] = {"sha256": C.sha256_file(p), "rows": sum(1 for x in open(p) if x.strip()), "bytes": p.stat().st_size}
    return out


def work_of(data_root: Path, specs: list) -> dict:
    """Per spec: rows / sequences / characters (from the files; a missing file counts 0 and is listed)."""
    per, missing = {}, []
    for s in specs:
        p = Path(data_root) / s["file"]
        if not p.exists():
            per[f"{s['split']}{s['tag']}"] = {"rows": 0, "seq": 0, "chars": 0, "choice_rows": 0}
            missing.append(s["file"])
            continue
        per[f"{s['split']}{s['tag']}"] = scan_split(p, s["views"])
    tot = {k: sum(v[k] for v in per.values()) for k in ("rows", "seq", "chars")}
    return {"per_set": per, "total": tot, "missing_files": sorted(set(missing))}


def p_reference(data_root: Path) -> dict:
    """The 17 Oct parity set P: the 9 gate dev splits read with the A18.2 readout (choice rows twice)."""
    t = {"rows": 0, "seq": 0, "chars": 0}
    for sp in SPLITS9:
        w = scan_split(Path(data_root) / f"{sp}.jsonl", 2)
        for k in t:
            t[k] += w[k]
    if t["rows"] != P_ROWS:
        raise ValueError(f"the parity set P has {t['rows']} rows now, the 17 Oct measurement had {P_ROWS}: the throughput basis is stale")
    return t


# ------------------------------------------------------------------ order
def candidate_order(grid_names: list) -> list:
    """P6 read order: the C1 reference, then the final step (the A42-D 9.5 reference), then the rest in grid order."""
    rest = [n for n in grid_names if n != FINAL]
    if FINAL not in grid_names:
        raise ValueError(f"{FINAL} is not in the grid")
    return [FINAL, *rest]


def model_list(grid_names: list, adapter_shas: dict | None = None) -> list:
    adapter_shas = adapter_shas or {}
    out = [{"order": 0, "kind": "ref", "cand": None, "read_name": C.REF_NAME, "adapter_sha256": C.C1_ADAPTER_SHA256}]
    for i, n in enumerate(candidate_order(grid_names), 1):
        out.append({"order": i, "kind": "cand", "cand": n, "read_name": C.read_name(n), "adapter_sha256": adapter_shas.get(n)})
    return out


# ------------------------------------------------------------------ estimate
def per_model_seconds(reads_s: float, scen: int, latency_calls: int = 420) -> dict:
    a = ASSUME
    lat = a["latency_s"][scen] * (latency_calls / 420.0)
    boot, rd = a["boot_s"][scen], reads_s * a["read_factor"][scen]
    return {"boot_s": boot, "latency_s": round(lat, 1), "reads_s": round(rd, 1), "stop_handoff_s": a["stop_handoff_s"][scen],
            "total_s": round(boot + lat + rd + a["stop_handoff_s"][scen], 1)}


def estimate(data_root: Path, specs: list, n_models: int = 19, spent_usd: float = 0.0, rate_h: float = C.FN_RATE_USD_H,
             stop_launch: float = C.STOP_LAUNCH_USD, latency_calls: int = 420, p_ref: dict | None = None) -> dict:
    w = work_of(data_root, specs)
    p = p_ref or p_reference(data_root)
    p_sec = P_ROWS / P_DEC_H * 3600
    t_seq = w["total"]["seq"] / p["seq"] * p_sec
    t_chars = w["total"]["chars"] / p["chars"] * p_sec
    reads_s = max(t_seq, t_chars)
    out = {"basis": {"P_decisions_per_h": P_DEC_H, "P_rows": P_ROWS, "P_seconds": round(p_sec, 2), "P_work": p,
                     "this_work_per_model": w["total"], "scaled_by_sequences_s": round(t_seq, 1),
                     "scaled_by_characters_s": round(t_chars, 1), "used_s": round(reads_s, 1),
                     "note": "17 Oct 2026 H100 S1 window, concurrency 64; scaled by the larger of the sequence and character ratios"},
           "assumptions_E": ASSUME, "rate_usd_h": rate_h, "overhead_s": C.CONTAINER_OVERHEAD_S, "scenarios": {}}
    for scen, name in enumerate(("low", "likely", "high")):
        a = ASSUME
        pm = per_model_seconds(reads_s, scen, latency_calls)
        fixed = a["base_setup_s"][scen] + a["grid_rebuild_s"][scen] + a["first_merge_s"][scen]
        total = fixed + n_models * pm["total_s"]
        cost = C.container_cost_usd(total, rate_h)
        budget = stop_launch - spent_usd
        k = 0
        while k < n_models and C.container_cost_usd(fixed + (k + 1) * pm["total_s"], rate_h) <= budget:
            k += 1
        par_s = PARITY_ASSUME["fixed_s"][scen]
        par_cost = C.container_cost_usd(par_s, rate_h)
        out["scenarios"][name] = {"per_model": pm, "fixed_s": fixed, "grid_total_s": round(total, 1), "grid_hours": round(total / 3600, 2),
                                  "grid_cost_usd": round(cost, 2), "parity_job_s": par_s, "parity_job_cost_usd": round(par_cost, 2),
                                  "all_in_cost_usd": round(cost + par_cost, 2),
                                  "fits_stop_launch": cost + par_cost + spent_usd <= stop_launch,
                                  "models_that_fit_before_stop_launch_without_parity": k}
    lk = out["scenarios"]["likely"]
    out["verdict"] = {"fits": lk["fits_stop_launch"], "likely_all_in_usd": lk["all_in_cost_usd"], "cap_usd": C.CAP_USD,
                      "stop_launch_usd": stop_launch, "spent_usd": spent_usd,
                      "shortfall_usd": round(max(0.0, lk["all_in_cost_usd"] + spent_usd - stop_launch), 2),
                      "models_of_19_that_fit": lk["models_that_fit_before_stop_launch_without_parity"],
                      "text": ("FITS" if lk["fits_stop_launch"] else
                               f"DOES NOT FIT: likely ${lk['all_in_cost_usd']:.2f} against stop-launch ${stop_launch:.2f} "
                               f"(about {lk['models_that_fit_before_stop_launch_without_parity']} of {n_models} models before the stop; "
                               f"the 18-candidate selection needs all of them)")}
    return out


def build_plan(data_root: Path, grid_record: dict | None, own_dev=(), spent_usd: float = 0.0, p_ref: dict | None = None) -> dict:
    specs = set_specs(own_dev)
    names = list((grid_record or {}).get("candidates", {})) or _expected_names()
    models = model_list(names, (grid_record or {}).get("candidates"))
    est = estimate(data_root, specs, len(models), spent_usd, p_ref=p_ref)
    return {"what": "A42-D 9 grid reads on ONE H100 (nothing here was run)", "app": C.APP_NAME, "set_specs": specs, "models": models,
            "own_dev": list(own_dev), "data_manifest": data_manifest(data_root, specs), "estimate": est,
            "limits": {"cap_usd": C.CAP_USD, "stop_launch_usd": C.STOP_LAUNCH_USD, "hard_stop_usd": C.HARD_STOP_USD,
                       "session_timeout_s": C.SESSION_TIMEOUT_S, "rate_usd_h": C.FN_RATE_USD_H, "region": C.REGION}}


ALPHAS = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)          # grid_plan.ALPHAS / BASES (a test keeps them equal)
BASES = ("final", "last3", "earlylate")


def _expected_names() -> list:
    return [f"{b}_a{round(a * 10):02d}" for b in BASES for a in ALPHAS]
