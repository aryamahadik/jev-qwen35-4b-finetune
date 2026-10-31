#!/usr/bin/env python3
"""G-proxy finalisation, A42-D 12.1 / 12.2 / 12.3 (CPU only, no model, never prints row text).

  check    dry run; nothing is written or recorded. Rebuilds the 150 twins in memory from the frozen held-out patterns,
           compares them with data/c2_gproxy/gproxy_pairs.jsonl, builds the combined file in memory and checks every
           12.1 bar plus the pilot-verdict cluster rule (pilot_ab/verdict.clusters). Prints counts only.
  record   needs meta_src/gproxy/noise/NOISE_FINAL.json with all_sources_ok true (written after the Haiku noise check and
           the Opus confirmations). Order, as the plan says: (1) record the rows hash, (2) run pairs.py --final,
           (3) write the combined file pab_gproxy.jsonl (= gproxy_rows.jsonl bytes + gproxy_pairs.jsonl bytes) and
           pab_gproxy_relations.jsonl ({a: base id, b: twin id, type: complement}), (4) write GPROXY_HASH.json (every sha256)
           and the .sha256 sidecars, (5) make the five data files read-only. Refuses to run twice.
  verify   recomputes every sha256 and compares with GPROXY_HASH.json (run before any read).

Run from lean/c2_build:  ../../.venv/bin/python -B meta_src/gproxy/finalize.py check|record|verify
The combined file is the file `pilot_ab/verdict.py --gproxy-rows` pins with --gproxy-sha256."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parents[1]
LEAN = BUILD.parent
sys.path.insert(0, str(BUILD))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / "pilot_ab"))

DATA = Path(os.environ.get("GPROXY_DATA_DIR") or LEAN / "data" / "c2_gproxy")   # env override is for tests only
ROWS, PAIRS, INDEX, PREP = (DATA / "gproxy_rows.jsonl", DATA / "gproxy_pairs.jsonl", DATA / "gproxy_pairs_index.json",
                            DATA / "gproxy_pairs_report.json")
COMB, REL = DATA / "pab_gproxy.jsonl", DATA / "pab_gproxy_relations.jsonl"
RECORD = DATA / "GPROXY_HASH.json"
NOISE_FINAL = Path(os.environ.get("GPROXY_NOISE_FINAL") or HERE / "noise" / "NOISE_FINAL.json")
FROZEN = [ROWS, PAIRS, INDEX, PREP, COMB, REL]
BARS = dict(min_rows=2000, min_sources=3, max_source_share=0.40, yes=(0.40, 0.50), card_free_min=0.30, pairs=150, per_pattern=5)


def sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def lines(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def relations(twins: list) -> str:
    return "".join(json.dumps({"a": t["meta"]["pair_base_id"], "b": t["id"], "type": "complement", "pair_id": t["meta"]["pair_id"],
                               "pattern": t["meta"]["heldout_pattern"]}, sort_keys=True) + "\n" for t in twins)


def checks(rows: list, twins: list, comb_text: str, rel_text: str) -> dict:
    """Every number the plan fixes (12.1) plus the pilot-verdict cluster rule. Counts only."""
    import verdict as V
    from negtwins import heldout as H
    comb = [json.loads(x) for x in comb_text.splitlines() if x.strip()]
    rels = [json.loads(x) for x in rel_text.splitlines() if x.strip()]
    n, per = len(comb), Counter(r["source"] for r in comb)
    base_rows = len(rows)
    ids = [r["id"] for r in comb]
    held = {s["hid"] for s in json.loads(H.SPECS_FILE.read_text())}        # the frozen, sha-checked specs file
    pats = Counter(t["meta"]["heldout_pattern"] for t in twins)
    hids = {p.split(":")[1] for p in pats if p.startswith("H:")}
    lab, cinfo = V.clusters(comb, rels)
    out = {
        "rows_base": base_rows, "rows_combined": n, "twins": len(twins),
        "sources": dict(per), "max_source_share": round(max(per.values()) / n, 4),
        "yes_share_base": round(sum(r["gold"] for r in rows) / base_rows, 4),
        "yes_share_combined": round(sum(r["gold"] for r in comb) / n, 4),
        "card_free_share_base": round(sum(1 for r in rows if not r.get("card")) / base_rows, 4),
        "card_free_share_combined": round(sum(1 for r in comb if not r.get("card")) / n, 4),
        "unique_ids": len(set(ids)) == n, "all_noul_yes_no": all(r["qtype"] == "noul" for r in comb),
        "patterns_used": len(pats), "max_per_pattern": max(pats.values()) if pats else 0,
        "all_patterns_held_out": bool(pats) and all(p.startswith("H:") for p in pats) and hids <= held, "frozen_specs_verified": H.verify_frozen(),
        "twin_gold_is_complement": all(t["gold"] == 1 - next(r for r in rows if r["id"] == t["meta"]["pair_base_id"])["gold"] for t in twins),
        "twins_never_train_dev_only": all(t["meta"].get("never_train") and t["meta"].get("dev_only") for t in twins),
        "rows_never_train": all(r["meta"].get("never_train") for r in rows),
        "verdict_clusters": cinfo["clusters"], "verdict_complement_pairs": cinfo["pairs"],
        "verdict_group_id_fallback_rows": cinfo["rows_with_group_id_fallback"],
        "twin_share_clusters_with_base": all(lab[t["id"]] == lab[t["meta"]["pair_base_id"]] for t in twins),
    }
    b = BARS
    out["bars"] = {
        "rows>=2000": n >= b["min_rows"], "sources>=3": len(per) >= b["min_sources"], "no source >40%": out["max_source_share"] <= b["max_source_share"],
        "yes 40-50% (base rows)": b["yes"][0] <= out["yes_share_base"] <= b["yes"][1],
        "card-free>=30%": out["card_free_share_base"] >= b["card_free_min"] and out["card_free_share_combined"] >= b["card_free_min"],
        "150 pairs": len(twins) == b["pairs"] and cinfo["pairs"] == b["pairs"], "<=5 per pattern": out["max_per_pattern"] <= b["per_pattern"],
        "held-out patterns only": out["all_patterns_held_out"] and out["frozen_specs_verified"],
        "twin gold = 1 - base gold": out["twin_gold_is_complement"], "ids unique": out["unique_ids"],
    }
    out["all_bars_pass"] = all(out["bars"].values())
    return out


def rebuild_twins(rows: list):
    import pairs as PA
    twins, _index, rep = PA.build(rows, PA.load_admitted(True), n_target=150)
    return twins, rep


def cmd_check(_a):
    rows = lines(ROWS)
    twins_new, rep = rebuild_twins(rows)
    new_text = "".join(json.dumps(t, ensure_ascii=False, sort_keys=True) + "\n" for t in twins_new)
    on_disk = PAIRS.read_text(encoding="utf-8")
    twins = lines(PAIRS)
    comb_text = ROWS.read_text(encoding="utf-8") + on_disk
    res = checks(rows, twins, comb_text, relations(twins))
    res["pairs_file_equals_rebuild"] = new_text == on_disk
    res["pairs_rebuild_complete"] = rep.get("complete")
    res["pairs_rebuild_problems"] = len(rep.get("problems", []))
    res["combined_sha256_dry"] = hashlib.sha256(comb_text.encode()).hexdigest()
    res["rows_sha256"] = sha_file(ROWS)
    print(json.dumps(res, indent=1))
    return 0 if res["all_bars_pass"] and res["pairs_file_equals_rebuild"] else 2


def cmd_record(_a):
    if RECORD.exists():
        raise SystemExit(f"{RECORD} exists: the hash is recorded once and the files are never edited afterwards")
    if not NOISE_FINAL.exists():
        raise SystemExit("noise/NOISE_FINAL.json is missing: the noise check (12.3) comes first")
    nf = json.loads(NOISE_FINAL.read_text())
    if not nf.get("all_sources_ok"):
        raise SystemExit("NOISE_FINAL.json: a source is dropped or unresolved; replace it and rebuild before the hash")
    rows_sha0 = sha_file(ROWS)
    pairs_sha0 = sha_file(PAIRS) if PAIRS.exists() else None
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(json.dumps({"step": "1 rows hash recorded", "utc": t0, "rows_sha256": rows_sha0}))
    r = subprocess.run([sys.executable, "-B", str(HERE / "pairs.py"), "--final", "--out-dir", str(DATA), "--rows", str(ROWS)], cwd=str(BUILD), capture_output=True, text=True)
    print(json.dumps({"step": "2 pairs.py --final", "rc": r.returncode, "tail": r.stdout[-600:]}))
    if r.returncode != 0:
        print(r.stderr[-1500:])
        raise SystemExit("pairs.py --final failed: nothing recorded")
    if sha_file(ROWS) != rows_sha0:
        raise SystemExit("rows file changed during the run")
    rows, twins = lines(ROWS), lines(PAIRS)
    comb_text = ROWS.read_text(encoding="utf-8") + PAIRS.read_text(encoding="utf-8")
    rel_text = relations(twins)
    res = checks(rows, twins, comb_text, rel_text)
    if not res["all_bars_pass"]:
        raise SystemExit("a 12.1 bar fails: " + json.dumps(res["bars"]))
    COMB.write_text(comb_text, encoding="utf-8")
    REL.write_text(rel_text, encoding="utf-8")
    shas = {p.name: sha_file(p) for p in FROZEN}
    for p in FROZEN:
        (DATA / (p.name + ".sha256")).write_text(f"{shas[p.name]}  {p.name}\n")
    ctx = {k: sha_file(v) for k, v in {
        "SOURCES.json": HERE / "SOURCES.json", "build_w8.py": HERE / "build_w8.py", "build.py": HERE / "build.py", "pairs.py": HERE / "pairs.py",
        "noise_tasks.py": HERE / "noise_tasks.py", "score_noise.py": HERE / "score_noise.py", "NOISE_FINAL.json": NOISE_FINAL,
        "negtwins/HELDOUT_FREEZE.json": BUILD / "negtwins" / "HELDOUT_FREEZE.json",
        "negtwins/HELDOUT_REALISED.json": BUILD / "negtwins" / "HELDOUT_REALISED.json"}.items()}
    rec = {"gate": "A42-D 12.2: hash recorded before C1's first read; the files are never edited afterwards",
           "recorded_utc": t0, "pairs_final_run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "seed": "gproxy-v2-16oct2026", "snapshot": "2026-10-16",
           "sha256": shas, "pairs_file_unchanged_by_final_run": pairs_sha0 == shas["gproxy_pairs.jsonl"],
           "rows_sha256_recorded_before_pairs_final": rows_sha0,
           "pin_for_verdict": {"--gproxy-rows": str(COMB), "--gproxy-rel": str(REL), "--gproxy-sha256": shas["pab_gproxy.jsonl"]},
           "counts": {k: res[k] for k in ("rows_base", "rows_combined", "twins", "sources", "max_source_share", "yes_share_base",
                                          "yes_share_combined", "card_free_share_base", "card_free_share_combined", "patterns_used",
                                          "max_per_pattern", "verdict_clusters", "verdict_complement_pairs")},
           "bars": res["bars"], "noise_check": nf, "context_sha256": ctx}
    RECORD.write_text(json.dumps(rec, indent=1) + "\n")
    (DATA / "GPROXY_HASH.json.sha256").write_text(f"{sha_file(RECORD)}  GPROXY_HASH.json\n")
    for p in FROZEN + [RECORD]:
        os.chmod(p, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    print(json.dumps({"step": "3-5 recorded", "sha256": shas, "counts": rec["counts"], "pairs_unchanged": rec["pairs_file_unchanged_by_final_run"]}, indent=1))
    return 0


def cmd_verify(_a):
    rec = json.loads(RECORD.read_text())
    bad = [n for n, s in rec["sha256"].items() if sha_file(DATA / n) != s]
    print(json.dumps({"verified_files": len(rec["sha256"]), "mismatches": bad, "rows_sha256": rec["sha256"]["gproxy_rows.jsonl"],
                      "pab_gproxy_sha256": rec["sha256"]["pab_gproxy.jsonl"]}))
    return 2 if bad else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["check", "record", "verify"])
    a = ap.parse_args()
    sys.exit({"check": cmd_check, "record": cmd_record, "verify": cmd_verify}[a.cmd](a))
