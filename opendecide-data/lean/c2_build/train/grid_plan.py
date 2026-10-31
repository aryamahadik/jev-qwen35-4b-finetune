"""grid_plan.py: the pre-registered bookkeeping around the 18-candidate grid (PREREG A42-D 9.2, 9.5, 9.6). CPU only; it
reads small JSON records and file metadata, never a prediction value, and it starts no job.

  record          grid.json sha256 recorded BEFORE any look (9.6). Re-derives the grid sha256 the way merge_avg.py does, checks the
                  grid is exactly the frozen one (3 bases x alpha 0.5..1.0 = 18, coefficients sum to 1, the early checkpoint is the
                  one nearest 33%, final_a10 is the final adapter byte for byte, 6-10 checkpoints) and, when the adapter folders
                  are on disk, each adapter's sha256. Refuses if ANY grid candidate already has a pred file (a look came first)
                  or if the record exists. Prints the line for the PREREG addendum.
  verify          the record still matches grid.json and the adapters, and was written before the first grid read.
  plan            the read plan for the 18 candidates + the C1 reference on od-l4b (final / last-3 average / early+late average
                  x alpha 0.5..1.0): reads, row counts, split files, order, estimates, the commands (printed, never run) and the
                  open questions. Writes READ_PLAN.json and GRID_CFG.json (the config grid_elig.py takes).
  candidate-check CANDIDATE_C2.json timing (9.6, gate_c2.check_candidate): the record names the chosen grid candidate, its
                  adapter sha256 equals grid.json's, it was written after the grid reads and the grid record and BEFORE the first
                  official pre-gate read of q35_4b_c2, and the adapter file the gate will hash is that adapter.

  grid_plan.py record --grid models/q35_4b_c2_grid/grid.json [--adapters-dir models/q35_4b_c2_grid] --out c2_build/train/GRID_RECORD.json
  grid_plan.py verify --grid ... --record ...
  grid_plan.py plan --grid ... --out-dir c2_build/staged/P6-grid [--expected]      (--expected: the frozen shape, no grid.json yet)
  grid_plan.py candidate-check [--candidate c2_build/CANDIDATE_C2.json] [--chosen c2_build/train/CHOSEN.json] ...

Exit 0 = ok, 1 = a check failed, 2 = refused / bad input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
LEAN = C2B.parent
for _p in (str(C2B), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ALPHAS = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)                       # A42-D 9.2 (kept equal to merge_avg.ALPHAS by a test)
BASES = ("final", "last3", "earlylate")
EARLY_FRAC = 0.33
FINAL = "final_a10"
C1_SHA_PREFIX = "507d1c29"
RUN_NAME, REF_NAME = "q35_4b_c2", "q35_4b_main500k_c2"        # gate_c2.CAND / REF
READ_TPL = "q35_4b_c2grid_{cand}"                              # the pred-file name of a grid read ("4b" token: gate_dev sizes it)
SLACK = 1.0                                                    # seconds, as gate_c2.check_candidate
SPLITS9 = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev")
ATTACKS = ("eval_jagged", "eval_opi")
C2_DEV = ("c2_mixdev", "c2_transfer_dev", "c2_t37b_dev")
GPROXY_SPLIT = "pab_gproxy"
BASE, REVISION, LAYOUT = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "schema_branch_mark"
# measured / cited rates for the estimates (replace by the first candidate's measured wall time)
RATE_NO_TTA = 8143 / (25 * 60)         # rows/s, od_gcp predict on the L4, 9 dev splits in 25 min (l4_reads.sh header, logs/gate4b)
RATE_TTA = 2.5                         # rows/s, od_gcp predict --tta-choice on the L4 (reads/README.md section 2, A49 f parity run)
LOAD_MIN = 3.0                         # model load per od_gcp invocation (l4_reads.sh header)
RATE_SGL = 8.7                         # rows/s, fast path 2-view (reads/README.md): NOT usable by the gate as it stands, see open Q3


class Refused(Exception):
    pass


def sha_file(p) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def cand_name(base: str, alpha: float) -> str:
    return f"{base}_a{round(alpha * 10):02d}"                  # merge_avg.cand_name


def expected_names() -> list:
    return [cand_name(b, a) for b in BASES for a in ALPHAS]


def read_name(cand: str) -> str:
    return READ_TPL.format(cand=cand)


def canon_grid_sha(grid: dict) -> str:
    """merge_avg.build_grid's formula."""
    canon = json.dumps({k: grid[k] for k in ("c1_adapter_sha256", "checkpoints", "bases", "candidates")}, sort_keys=True)
    return hashlib.sha256(canon.encode()).hexdigest()


def guard(*paths) -> None:
    import c2io
    for p in paths:
        if p is None:
            continue
        why = c2io.refusal(p)
        if why:
            raise Refused(f"{p} refused: {why}")


# ------------------------------------------------------------------------------------------------ the grid itself
def check_grid(grid: dict, grid_dir: Path | None = None) -> list:
    """Problems with grid.json against the frozen A42-D 9.2 shape (empty list = it is the frozen grid)."""
    p = []
    cands = grid.get("candidates") or []
    names = [c.get("name") for c in cands]
    if sorted(names) != sorted(expected_names()) or len(set(names)) != len(names):
        p.append(f"candidate names {names} are not the 18 of A42-D 9.2")
    if not str(grid.get("c1_adapter_sha256", "")).startswith(C1_SHA_PREFIX):
        p.append(f"C1 adapter sha256 does not start {C1_SHA_PREFIX}")
    try:
        if canon_grid_sha(grid) != grid.get("grid_sha256"):
            p.append("grid_sha256 does not match the grid's content (file edited after merge_avg wrote it)")
    except KeyError as e:
        p.append(f"grid.json lacks {e}")
        return p
    ck = grid.get("checkpoints") or []
    if not 6 <= len(ck) <= 10:
        p.append(f"{len(ck)} checkpoints (A42-D 9.1 says 6-10)")
    if ck and ck[-1].get("name") != "final":
        p.append("the final adapter is not the last checkpoint")
    bases = grid.get("bases") or {}
    if ck and len(ck) >= 4:
        early = min(ck[:-1], key=lambda c: (abs(c["frac"] - EARLY_FRAC), c["step"]))["name"]
        want = {"final": {"final": 1.0}, "last3": {c["name"]: 1 / 3 for c in ck[-3:]}, "earlylate": {early: 0.5, "final": 0.5}}
        for b in BASES:
            got = bases.get(b) or {}
            if set(got) != set(want[b]) or any(abs(got[k] - want[b][k]) > 1e-9 for k in want[b]):
                p.append(f"base {b}: weights {got} are not the frozen {want[b]}")
    byname = {c.get("name"): c for c in cands}
    for b in BASES:
        for a in ALPHAS:
            c = byname.get(cand_name(b, a))
            if c is None:
                continue
            if c.get("base") != b or abs(float(c.get("alpha", -1)) - a) > 1e-9:
                p.append(f"{c['name']}: base/alpha {c.get('base')}/{c.get('alpha')} disagree with its name")
            co = c.get("coefs") or {}
            if abs(sum(co.values()) - 1.0) > 1e-9:
                p.append(f"{c['name']}: coefficients sum to {sum(co.values())}")
            want_c1 = 1.0 - a
            if (a < 1.0 - 1e-12) != ("c1" in co) or ("c1" in co and abs(co["c1"] - want_c1) > 1e-9):
                p.append(f"{c['name']}: C1 weight {co.get('c1')} is not 1 - alpha")
            if not (isinstance(c.get("adapter_sha256"), str) and len(c["adapter_sha256"]) == 64):
                p.append(f"{c['name']}: no adapter sha256")
            if c.get("verify_max_abs_err", 0.0) > 1e-5:
                p.append(f"{c['name']}: stacked-vs-dense error {c['verify_max_abs_err']} > 1e-5")
    fin = byname.get(FINAL)
    if fin and ck and fin.get("adapter_sha256") != ck[-1].get("adapter_sha256"):
        p.append("final_a10 is not the final adapter byte for byte")
    if grid_dir is not None:
        for c in cands:
            f = Path(grid_dir) / str(c.get("name")) / "adapter_model.safetensors"
            if not f.exists():
                p.append(f"{f} missing")
            elif sha_file(f) != c.get("adapter_sha256"):
                p.append(f"{c['name']}: the adapter on disk is not the recorded one")
    return p


def grid_read_files(root: Path, names: list) -> list:
    """Every pred/meta file of the given read names under root/preds_*/ (all splits, _perm and tagged variants)."""
    out = []
    for d in sorted(Path(root).glob("preds_*")):
        for n in names:
            out += [f for f in d.glob(f"{n}*") if f.is_file()]
    return out


def candidate_reads(root: Path, cands: list) -> list:
    return grid_read_files(root, [read_name(c) for c in cands])


# ------------------------------------------------------------------------------------------------ record / verify
def record(grid_path: Path, out: Path, adapters_dir: Path | None, root: Path = LEAN, now: float | None = None) -> dict:
    guard(grid_path, out, root)
    grid = json.loads(Path(grid_path).read_text())
    probs = check_grid(grid, adapters_dir)
    if probs:
        raise Refused("grid.json is not the frozen grid: " + "; ".join(probs[:6]))
    if Path(out).exists():
        raise Refused(f"{out} exists: the grid sha256 is recorded once, before any look")
    seen = candidate_reads(root, [c["name"] for c in grid["candidates"]])
    if seen:
        raise Refused(f"{len(seen)} grid read file(s) exist already (first: {seen[0].name}): the sha256 must be recorded before any look")
    t = time.time() if now is None else now
    rec = {"rule": "PREREG A42-D 9.6: the grid is recorded before any look", "grid_sha256": grid["grid_sha256"],
           "grid_file_sha256": sha_file(grid_path), "grid_file": str(grid_path), "c1_adapter_sha256": grid["c1_adapter_sha256"],
           "candidates": {c["name"]: c["adapter_sha256"] for c in grid["candidates"]},
           "adapters_checked_on_disk": adapters_dir is not None, "written_unix": t,
           "written_utc": datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n")
    rec["addendum_line"] = (f"Grid record (A42-D 9.6, {rec['written_utc']}): grid_sha256 {rec['grid_sha256']}, grid.json sha256 "
                            f"{rec['grid_file_sha256']}; 18 candidates; recorded before any grid read.")
    return rec


def verify_record(rec_path: Path, grid_path: Path, root: Path = LEAN, adapters_dir: Path | None = None) -> dict:
    """{ok, problems, first_read_unix}. Read-only."""
    guard(rec_path, grid_path, root)
    probs = []
    try:
        rec = json.loads(Path(rec_path).read_text())
        grid = json.loads(Path(grid_path).read_text())
    except (OSError, ValueError) as e:
        return {"ok": False, "problems": [f"cannot load the record or grid.json ({type(e).__name__})"], "first_read_unix": None}
    if sha_file(grid_path) != rec.get("grid_file_sha256"):
        probs.append("grid.json changed after it was recorded")
    probs += check_grid(grid, adapters_dir)
    if rec.get("grid_sha256") != grid.get("grid_sha256"):
        probs.append("the recorded grid_sha256 is not grid.json's")
    if rec.get("candidates") != {c["name"]: c["adapter_sha256"] for c in grid.get("candidates", [])}:
        probs.append("the recorded adapter shas differ from grid.json's")
    reads = candidate_reads(root, [c["name"] for c in grid.get("candidates", [])])
    first = min((f.stat().st_mtime for f in reads), default=None)
    if first is not None and float(rec.get("written_unix", 1e18)) > first + SLACK:
        probs.append("the grid record was written after the first grid read")
    return {"ok": not probs, "problems": probs, "first_read_unix": first, "grid_sha256": rec.get("grid_sha256")}


# ------------------------------------------------------------------------------------------------ the read plan
def count_rows(path: Path) -> int | None:
    try:
        with open(path) as f:
            return sum(1 for line in f if line.strip())
    except OSError:
        return None


def split_rows_in(root: Path) -> dict:
    """Row counts of the split files that exist (None = the file is not written yet)."""
    d = Path(root) / "data"
    out = {s: count_rows(d / f"{s}.jsonl") for s in (*SPLITS9, *ATTACKS, *C2_DEV)}
    out[GPROXY_SPLIT] = count_rows(d / "c2_gproxy" / "pab_gproxy.jsonl")
    return out


def per_read_minutes(rows: dict, own: dict | None = None) -> dict:
    """Minutes of one candidate's reads on the HF path (od_gcp.py predict) from the cited rates; None rows count as 0 and are listed."""
    own = own or {}
    n9 = sum(rows[s] or 0 for s in SPLITS9)
    att = sum(rows[s] or 0 for s in ATTACKS)
    c2d = sum(rows[s] or 0 for s in C2_DEV)
    gp = (rows[GPROXY_SPLIT] or 0) + sum(own.values())
    job_a = (n9 + att + c2d) / RATE_NO_TTA / 60 + LOAD_MIN        # no TTA: 9 dev + 2 attack sets + 3 C2 dev sets
    job_b = n9 / RATE_NO_TTA / 60 + LOAD_MIN                      # _perm reads (perm seed 1) of the 9 dev splits
    job_c = gp / RATE_TTA / 60 + LOAD_MIN                         # G-proxy (+ own dev): --tta-choice, as C1's G-proxy read
    return {"A_dev_attacks_c2dev": round(job_a, 1), "B_perm": round(job_b, 1), "C_gproxy_owndev": round(job_c, 1),
            "total": round(job_a + job_b + job_c, 1), "unknown_row_counts": sorted(k for k, v in rows.items() if v is None)}


def jobs_for(name: str, adapter_dir: str | None, own_splits: list) -> list:
    pre = (f"cd ~/lean && ~/od/bin/python od_gcp.py predict --name {name} --base {BASE} --revision {REVISION} "
           f"--layout {LAYOUT} ")
    s_a = ",".join((*SPLITS9, *ATTACKS, *C2_DEV))
    s_c = ",".join((GPROXY_SPLIT, *own_splits))
    return [
        {"job": "A", "what": "9 dev splits + eval_jagged + eval_opi + the 3 C2 dev sets, no TTA (gate_dev.pipeline_check)",
         "cmd": pre + f"--splits {s_a}", "writes": f"preds_<split>/{name}.jsonl"},
        {"job": "B", "what": "permuted-view reads of the 9 dev splits, perm seed 1 (D5)",
         "cmd": pre + f"--splits {','.join(SPLITS9)} --perm-seed 1 --tag _perm", "writes": f"preds_<split>/{name}_perm.jsonl"},
        {"job": "C", "what": "G-proxy (+ own dev splits when new families entered C2), choice rows two views like C1's G-proxy read (A18.2)",
         "cmd": pre + f"--splits {s_c} --tta-choice", "writes": f"preds_{GPROXY_SPLIT}/{name}.jsonl"},
    ]


OPEN_QUESTIONS = [
    "Q1 GPU: od-l4b holds the project's one L4 and the production C1 SGLang server (port 30000, --mem-fraction-static 0.8). An "
    "od_gcp.py predict job loads a 4B model on the same GPU, so the 19 reads (18 candidates + the C1 reference) cannot run "
    "beside the server. This lane never stops or restarts it: the orchestrator decides the window (about the plan's total hours) "
    "and who swaps the server back afterwards. Modal and a second GPU VM are not options under the standing rules.",
    "Q2 Adapters on the VM: the 18 candidate folders (stacked LoRA, rank 16 K) must be copied to ~/lean/models/<read name>/ "
    "(adapter_model.safetensors, adapter_config.json, tokenizer files; merge_avg writes no train_meta.json, so the commands pass "
    "--layout schema_branch_mark --revision <pin> as l4_reads.sh does: no forced override is recorded). Their sha256 must be "
    "re-checked on the VM against GRID_RECORD.json before each read.",
    "Q3 Fast path: reads/fast_read.py predict writes metas without gpu/torch/cuda, with tta_choice true by default and serves only "
    "C1 (the merged export is pinned to C1's adapter sha). gate_dev.pipeline_check rejects such metas for the dev reads. The plan "
    "therefore uses the HF path (od_gcp.py predict, about 4 times slower). Using SGLang for the grid needs a ruling plus P7's "
    "parameterised merge export, and 'same served path' for D9 then applies to every candidate.",
    "Q4 REF: the C1 reference is read once (name q35_4b_main500k_c2) in the same session, then "
    "gate_dev.py q35_4b_main500k_c2 q35_4b_main500k --mode refparity must PASS before grid_elig.py runs; the same REF preds then "
    "serve the official pre-gate (gate_c2 requires the preds not to change after the refparity look).",
    "Q5 Official pre-gate reads: gate_c2.check_candidate refuses CANDIDATE_C2.json written after the first read of q35_4b_c2, and "
    "pred_files() looks only at that name. The plan therefore reads the chosen candidate AGAIN under q35_4b_c2 after "
    "CANDIDATE_C2.json is written (one more candidate read, about the plan's per-candidate hours). Reusing a grid read as the "
    "official read would need a ruling.",
    "Q6 D9 latency: each of the 18 eligibility records needs its own latency record (gate_c2.latency_rule: cand_p50_ms, ref_p50_ms, one "
    "served_path). Merged candidates share the C1 architecture; whether one measured p50 per candidate (18 server restarts) or a "
    "shared measurement is allowed is a ruling. grid_elig.py refuses a missing record; it never fills one.",
    "Q7 Row counts of c2_mixdev, c2_t37b_dev and the own dev splits are unknown until the dev files are written (P5); the plan's "
    "hours exclude them and say so.",
]


def build_plan(root: Path, grid: dict | None, own_splits: list | None = None, own_rows: dict | None = None) -> dict:
    own_splits, own_rows = own_splits or [], own_rows or {}
    rows = split_rows_in(root)
    mins = per_read_minutes(rows, own_rows)
    names = [c["name"] for c in grid["candidates"]] if grid else expected_names()
    adapters = {c["name"]: c["adapter_sha256"] for c in grid["candidates"]} if grid else {}
    order = [FINAL] + [n for n in names if n != FINAL]            # the final step first: the A42-D 9.5 reference
    reads = [{"order": 0, "kind": "ref", "name": REF_NAME, "adapter_sha256_prefix": C1_SHA_PREFIX, "jobs": jobs_for(REF_NAME, None, own_splits)}]
    for i, n in enumerate(order, 1):
        reads.append({"order": i, "kind": "candidate", "candidate": n, "name": read_name(n), "adapter_sha256": adapters.get(n),
                      "adapter_dir_on_vm": f"~/lean/models/{read_name(n)}", "jobs": jobs_for(read_name(n), None, own_splits)})
    total_min = mins["total"] * len(reads)
    return {
        "what": "P6 read plan: the 18 grid candidates and the C1 reference on od-l4b (A42-D 9.2, 9.6). NOTHING here was run.",
        "grid_sha256": grid["grid_sha256"] if grid else None, "grid_shape": "frozen A42-D 9.2" if not grid else "from grid.json",
        "candidates": names, "n_candidates": len(names),
        "read_order": [r.get("candidate") or "REF" for r in reads],
        "split_rows": rows, "own_dev_splits": own_splits, "own_dev_rows": own_rows,
        "minutes_per_read": mins,
        "estimate_hours": {"reads": round(total_min / 60, 1), "n_reads": len(reads),
                           "basis": {"no_tta_rows_per_s": round(RATE_NO_TTA, 2), "tta_choice_rows_per_s": RATE_TTA,
                                     "load_min_per_invocation": LOAD_MIN},
                           "note": "from cited L4 rates; excludes the unknown C2 dev row counts, the per-candidate latency run (Q6), "
                                   "adapter copies and the refparity look; replace by the first candidate's wall time"},
        "sglang_alternative_hours": round((sum((rows[s] or 0) for s in SPLITS9) * 2 + sum((rows[s] or 0) for s in (*ATTACKS, *C2_DEV, GPROXY_SPLIT)))
                                          / RATE_SGL / 3600 * len(reads), 1),
        "reads": reads,
        "sequence": [
            "0. grid_plan.py record --grid <grid.json> --adapters-dir <grid dir> --out c2_build/train/GRID_RECORD.json  (sha before any look)",
            "1. orchestrator: GPU window on od-l4b (Q1); scp the 18 adapter folders + data/<split>.jsonl for the C2 dev sets; sha256 -c on the VM",
            "2. REF read (order 0), then gate_dev.py q35_4b_main500k_c2 q35_4b_main500k --mode refparity (must PASS, Q4)",
            "3. candidates in read_order, jobs A, B, C each (one session, one torch/CUDA stack: pipeline_check demands one value)",
            "4. latency record per candidate (Q6): logs/grid/latency_<cand>.json",
            "5. per candidate: gate_dev.py <read name> q35_4b_main500k_c2 --mode ship --size 4b --json c2_build/logs/grid/ship_<cand>.json --no-log",
            "6. grid_elig.py all --cfg GRID_CFG.json --out-dir c2_build/train/grid_reads   (writes reads/<cand>.json with the 11 booleans)",
            "7. select_candidate.py --reads <dir> --grid <grid.json> --out CHOSEN.json --candidate-out c2_build/CANDIDATE_C2.json",
            "8. grid_plan.py candidate-check (before ANY official read of q35_4b_c2), then the official pre-gate reads (Q5)",
        ],
        "open_questions": OPEN_QUESTIONS,
    }


def default_cfg(root: Path = LEAN) -> dict:
    """The config grid_elig.py takes. Paths are relative to `root` (lean/)."""
    return {"root": str(root), "run_name": RUN_NAME, "ref": REF_NAME, "name_tpl": READ_TPL,
            "grid": "models/q35_4b_c2_grid/grid.json", "grid_record": "c2_build/train/GRID_RECORD.json",
            "ship_tpl": "c2_build/logs/grid/ship_{cand}.json", "latency_tpl": "c2_build/logs/grid/latency_{cand}.json",
            "d2_set": "c2_build/logs/d2_set_c2.json",
            "gproxy": {"split": GPROXY_SPLIT, "rows": "data/c2_gproxy/pab_gproxy.jsonl",
                       "rel": "data/c2_gproxy/pab_gproxy_relations.jsonl", "sha256": None},
            "own_dev": [], "tta_choice_splits": [GPROXY_SPLIT]}


# ------------------------------------------------------------------------------------------------ CANDIDATE_C2 timing
def candidate_check(cand_path: Path, grid_path: Path, rec_path: Path, chosen_path: Path | None, adapter: Path | None,
                    root: Path = LEAN, run_name: str = RUN_NAME) -> dict:
    """The CANDIDATE_C2.json timing and identity checks (read-only). `status`: NOT_WRITTEN | OK_BEFORE_READS | OK_READS_AFTER | FAIL."""
    guard(cand_path, grid_path, rec_path, adapter, chosen_path)
    out = {"problems": [], "notes": []}
    pr = out["problems"]
    if not Path(cand_path).exists():
        return {**out, "status": "NOT_WRITTEN", "ok": False, "notes": ["CANDIDATE_C2.json does not exist yet (select_candidate.py --candidate-out writes it)"]}
    c = json.loads(Path(cand_path).read_text())
    v = verify_record(rec_path, grid_path, root)
    pr += [f"grid: {x}" for x in v["problems"]]
    grid = json.loads(Path(grid_path).read_text())
    shas = {x["name"]: x["adapter_sha256"] for x in grid.get("candidates", [])}
    gc_ = c.get("grid_candidate")
    if c.get("name") != run_name:
        pr.append(f"record names {c.get('name')!r}, not {run_name!r}")
    if gc_ not in shas:
        pr.append(f"grid_candidate {gc_!r} is not a grid candidate")
    elif c.get("adapter_sha256") != shas[gc_]:
        pr.append("adapter_sha256 is not grid.json's sha for the named candidate")
    if c.get("grid_sha256") != grid.get("grid_sha256"):
        pr.append("grid_sha256 in the record is not the recorded grid's")
    if chosen_path is not None:
        if not Path(chosen_path).exists():
            pr.append("CHOSEN.json missing")
        else:
            ch = json.loads(Path(chosen_path).read_text())
            if ch.get("chosen") != gc_ or ch.get("chosen_adapter_sha256") != c.get("adapter_sha256") or ch.get("grid_sha256") != grid.get("grid_sha256"):
                pr.append("CHOSEN.json and CANDIDATE_C2.json name different candidates / shas")
    w = c.get("written_unix")
    if not isinstance(w, (int, float)):
        pr.append("written_unix missing (gate_c2 would fall back to the file mtime)")
        w = Path(cand_path).stat().st_mtime
    mt = Path(cand_path).stat().st_mtime
    if abs(mt - w) > 5:
        out["notes"].append(f"file mtime and written_unix differ by {abs(mt - w):.0f} s")
    rec = json.loads(Path(rec_path).read_text()) if Path(rec_path).exists() else {}
    if rec and w < float(rec.get("written_unix", 0)):
        pr.append("CANDIDATE_C2.json is older than the grid record")
    gr = candidate_reads(root, list(shas))
    last_grid = max((f.stat().st_mtime for f in gr), default=None)
    if last_grid is not None and w < last_grid - SLACK:
        pr.append("CANDIDATE_C2.json was written before the last grid read (the choice cannot have used all 18)")
    off = official_reads(root, run_name)
    first_off = min((f.stat().st_mtime for f in off), default=None)
    if first_off is not None and w > first_off + SLACK:
        pr.append("CANDIDATE_C2.json was written after the first official read of " + run_name + " (gate_c2.check_candidate refuses)")
    if adapter is not None:
        if not Path(adapter).exists():
            out["notes"].append(f"the gate adapter path {adapter} is empty: copy the chosen candidate's adapter_model.safetensors there")
        elif sha_file(adapter) != c.get("adapter_sha256"):
            pr.append("the adapter file at the gate's path is not the chosen candidate's")
    out["written_unix"], out["first_official_read_unix"], out["last_grid_read_unix"] = w, first_off, last_grid
    out["official_read_files"] = len(off)
    out["ok"] = not pr
    out["status"] = "FAIL" if pr else ("OK_BEFORE_READS" if first_off is None else "OK_READS_AFTER")
    return out


def official_reads(root: Path, run_name: str = RUN_NAME) -> list:
    """Pred files named exactly run_name[_perm] (what gate_c2.pred_files() looks at), over every preds_* folder."""
    out = []
    for d in sorted(Path(root).glob("preds_*")):
        for suf in ("", "_perm"):
            f = d / f"{run_name}{suf}.jsonl"
            if f.exists():
                out.append(f)
    return out


# ------------------------------------------------------------------------------------------------ CLI
def _p(root: Path, x: str | None) -> Path | None:
    if x is None:
        return None
    q = Path(x)
    return q if q.is_absolute() else Path(root) / q


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(LEAN), help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("--grid", required=True)
    r.add_argument("--adapters-dir", default=None)
    r.add_argument("--out", default="c2_build/train/GRID_RECORD.json")
    v = sub.add_parser("verify")
    v.add_argument("--grid", required=True)
    v.add_argument("--record", default="c2_build/train/GRID_RECORD.json")
    v.add_argument("--adapters-dir", default=None)
    p = sub.add_parser("plan")
    p.add_argument("--grid", default=None)
    p.add_argument("--expected", action="store_true")
    p.add_argument("--out-dir", default="c2_build/staged/P6-grid")
    p.add_argument("--own-dev", default="", help="comma list of own dev split names (new families that entered C2)")
    k = sub.add_parser("candidate-check")
    k.add_argument("--candidate", default="c2_build/CANDIDATE_C2.json")
    k.add_argument("--grid", default="models/q35_4b_c2_grid/grid.json")
    k.add_argument("--record", default="c2_build/train/GRID_RECORD.json")
    k.add_argument("--chosen", default="c2_build/train/CHOSEN.json")
    k.add_argument("--adapter", default=str(LEAN.parents[1] / "backups/modal_models/q35_4b_c2/adapter_model.safetensors"))
    a = ap.parse_args(argv)
    root = Path(a.root)
    try:
        if a.cmd == "record":
            res = record(_p(root, a.grid), _p(root, a.out), _p(root, a.adapters_dir), root)
            print(json.dumps({k_: res[k_] for k_ in ("grid_sha256", "grid_file_sha256", "written_utc", "addendum_line")}, indent=1))
            return 0
        if a.cmd == "verify":
            res = verify_record(_p(root, a.record), _p(root, a.grid), root, _p(root, a.adapters_dir))
            print(json.dumps(res, indent=1))
            return 0 if res["ok"] else 1
        if a.cmd == "plan":
            out = _p(root, a.out_dir)
            guard(out)
            grid = None
            if a.grid and not a.expected:
                grid = json.loads(_p(root, a.grid).read_text())
                probs = check_grid(grid)
                if probs:
                    raise Refused("grid.json is not the frozen grid: " + "; ".join(probs[:5]))
            elif not a.expected:
                raise Refused("pass --grid grid.json, or --expected for the frozen shape before grid.json exists")
            own = [s for s in a.own_dev.split(",") if s]
            plan = build_plan(root, grid, own, {s: count_rows(root / "data" / f"{s}.jsonl") or 0 for s in own})
            out.mkdir(parents=True, exist_ok=True)
            (out / "READ_PLAN.json").write_text(json.dumps(plan, indent=1) + "\n")
            cfg = default_cfg(root)
            cfg["own_dev"] = [{"split": s, "rows": f"data/{s}.jsonl"} for s in own]
            cfg["tta_choice_splits"] = [GPROXY_SPLIT, *own]
            (out / "GRID_CFG.json").write_text(json.dumps(cfg, indent=1) + "\n")
            print(json.dumps({"reads": len(plan["reads"]), "hours": plan["estimate_hours"]["reads"], "out": str(out)}))
            return 0
        res = candidate_check(_p(root, a.candidate), _p(root, a.grid), _p(root, a.record), _p(root, a.chosen), Path(a.adapter), root)
        print(json.dumps(res, indent=1))
        return 0 if res["ok"] else 1
    except Refused as e:
        print(f"REFUSED: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
