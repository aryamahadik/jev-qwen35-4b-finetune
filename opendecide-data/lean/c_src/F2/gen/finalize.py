"""Sealed check (id-only program run; never reads sealed_nd), side files, statistics and out/MANIFEST.json.

Run: .venv/bin/python -m gen.finalize [--sealed-only]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict

from . import packs, stats
from .common import (F2, GEN_VERSION, LEAN, OUT, SEED, SPEC_ID, SPEC_SHA256, TMP, progress, read_jsonl, sha_file,
                     write_json, write_jsonl)

PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
CHECKER = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
SUITE = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"
ROW_FILES = ["candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl"]
SIDE_FILES = ["candidates_r1.relations.jsonl", "qc_sample.relations.jsonl", "ordinal_side.jsonl"]


NOTES = [
    "v1.0 (interrupted run): 80 cards, candidates and QC sample written; mixdev never written (build.py called main() "
    "before run_mixdev was defined).",
    "v1.1 (resume): (1) abstain / NEI statuses (k, needed, case count, abstain uniform) are drawn once and held across "
    "every retry until a base row is written; v1.0 re-drew them on retries, which left S4 open-world rows at about 52% "
    "NEI gold against 1/k = 33%. (2) Two more S1 cards are open-world (10 open cards, G0 1 'r1 10-12'; v1.0 had 8). "
    "(3) The S4 open date-window card uses a calendar-day deadline (its business-day card text left ~99% of rows at "
    ">= 1,900 tokens). Rows of all 10 open-world cards were dropped and rebuilt in both files (gen_version v1.1).",
    "v1.1: candidates and QC sample topped up to their targets on fresh RNG streams (ids from 20500); the S4 "
    "plantation CL card stays below its card target (rows per call are slow: fmt1 masked case refs), and its "
    "shortfall went to other S4 cards.",
    "v1.1: QC-sample ids use the prefix F2q. (v1.0 wrote them with the candidates' F2c. prefix, so the files shared "
    "ids; ids never appear in row text, so this is a relabel of id, group_id, call_id, twin_of and relation ends).",
    "v1.1: S5 choice cards (CH-V, CH-D) carry no deduction lines and no B4 split, for the 1,900-token cap; S5 YN-T "
    "cards keep both. S3 sweep level-1 cards state the banding amount (computed=False). Short S5 cards and sweep "
    "cells are filled from extra held-out cards.",
    "Not changed (reported): every open-world row has k = 3; no premise_removed twins are generated; median tokens "
    "about 1,000 (G0 1 says median 500-900 on the doubled-instructions count); option buckets and per-adjustment "
    "bind / dec rates are off the section 6 targets before selection (see stats); one-line + examples cards are 20 of "
    "80 (G0 3.7 says about 50%); the QC sample's deep share is 10.1% (candidates 9.8%; the <= 10% cap binds on "
    "selected training rows). G10, G6-G8 and selection run later.",
    "G4 reading: every sampler is tested on >= 1,000 rows (S5: 460 dev items + 1,007 extra S5 rows in tmp/) with >= 3 "
    "relations, all at 100%; per-relation counts are in gates.g4_*. MR5 shifts years inside the U4 date forms only "
    "(a bare 20xx amount is not a year).",
]


def run_sealed(path, rows_like=True):
    """Run the checker as a program; return (exit code, hit ids, summary)."""
    sd = TMP / "sealed"
    sd.mkdir(parents=True, exist_ok=True)
    tag = path.name.replace(".jsonl", "").replace(".json", "")
    out = sd / f"{tag}.sealedqc.jsonl"
    summ = sd / f"{tag}.summary.json"
    cmd = [PY, str(CHECKER), str(path), "--id-field", "id", "--out", str(out), "--summary", str(summ), "--workers", "4"]
    if rows_like:
        cmd += ["--structure-fields", "state,card,instructions,options"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 3):
        raise SystemExit(f"sealed checker failed on {path.name}: rc {p.returncode} {p.stderr[-300:]}")
    s = json.load(open(summ))
    if s.get("suite_sha256") != SUITE:
        raise SystemExit("sealed checker suite sha mismatch")
    hits = []
    for line in open(out):
        r = json.loads(line)
        if r.get("hit"):
            hits.append(r.get("id"))
    return p.returncode, hits, {k: v for k, v in s.items() if k in ("rows", "rows_hit", "rows_report_only",
                                                                   "kinds_nonzero", "parse_errors", "checker_sha256")}


def wrap_json(path):
    """A JSON document as one JSONL object {"id": name, "doc": ...} for the checker."""
    sd = TMP / "sealed"
    sd.mkdir(parents=True, exist_ok=True)
    p = sd / (path.stem + ".wrap.jsonl")
    with open(p, "w") as f:
        f.write(json.dumps({"id": path.stem, "doc": json.load(open(path))}) + "\n")
    return p


def ordinal_side(rows):
    """SC4a fallback: per band / named-outcome / date-window row, the option text -> edge rank (outside meta), read
    back by the parser from the row's own table (band table, outcome table, window table)."""
    from .parse import parse_row
    out = []
    for r in rows:
        sch = r["meta"]["card_id"].split(".")[-2]
        if sch in ("CH-B", "CH-O") and r["qtype"] == "choice":
            LP = parse_row(r)
            names = [o["name"] for o in LP["q"]["outs"]] if LP["q"].get("kind") == "outcome" else LP.get("_names")
            if names:
                out.append({"id": r["id"], "option_rank": {o: names.index(o) for o in r["options"] if o in names}})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sealed-only", action="store_true")
    a = ap.parse_args(argv)
    rows = {f: read_jsonl(OUT / f) for f in ROW_FILES}
    side = []
    for f in ("candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl"):
        side += ordinal_side(rows[f])
    write_jsonl(OUT / "ordinal_side.jsonl", side)
    sealed = {}
    for f in ROW_FILES:
        rc, hits, s = run_sealed(OUT / f)
        sealed[f] = {"exit": rc, "hit_ids": hits, **s}
        progress(f"sealed_check {f}: rows {s.get('rows')} hits {len(hits)}")
    for f in SIDE_FILES + ["cards_r1.json"]:
        p = OUT / f
        if not p.exists():
            continue
        q = wrap_json(p) if f.endswith(".json") else p
        rc, hits, s = run_sealed(q, rows_like=False)
        sealed[f] = {"exit": rc, "hit_ids": hits, **s}
    write_json(TMP / "sealed_report.json", sealed)
    if a.sealed_only:
        return 0
    manifest(rows, sealed)
    return 0


def _sha(p):
    return sha_file(p) if p.exists() else None


def parents_list():
    """MIXER_NOTE 1 (spec 3.H, G1): every pack, codebook, wording set and format set the rows derive from (no real-text
    dataset: F2 rows are program-generated, CC0). Repair r2 adds this list."""
    from .common import CSRC, FMT1, FMT2, PACKS
    items = [("pack_file", PACKS / "packs-1" / "packs.jsonl"), ("pack_file", PACKS / "packs-1" / "manifest.json"),
             ("pack_file", PACKS / "packs-2" / "packs.jsonl"), ("pack_file", PACKS / "packs-3" / "packs-3.jsonl"),
             ("pack_file", PACKS / "packs-4" / "packs.jsonl"),
             ("wording_set", FMT2 / "wordings" / "family_pools.jsonl"),
             ("codebook", CSRC / "common" / "negcount.py"), ("codebook", CSRC / "common" / "markers.json"),
             ("format_loader", FMT1 / "fmt1" / "card.py")]
    items += [("format_set", q) for q in sorted((FMT1 / "data").glob("*.jsonl"))]
    return [{"kind": k, "path": str(q.relative_to(LEAN)), "sha256": sha_file(q)} for k, q in items if q.exists()]


def relations_block():
    """MIXER_NOTE 3: relation counts and sha256 that must equal the relation files on disk (repair r2)."""
    out = {}
    for name in ("candidates_r1.relations.jsonl", "qc_sample.relations.jsonl"):
        q = OUT / name
        if q.exists():
            rs = read_jsonl(q)
            out[name] = {"path": f"out/{name}", "sha256": sha_file(q), "lines": len(rs),
                         "by_type": dict(Counter(x["type"] for x in rs))}
    return out


def manifest(rows, sealed):
    import time
    from .rowkit import git_sha
    gates = json.load(open(OUT / "gates_report.json")) if (OUT / "gates_report.json").exists() else {}
    tr, he = packs.split()
    cand, qc, dev = rows["candidates_r1.jsonl"], rows["qc_sample.jsonl"], rows["mixdev_S5.jsonl"]
    rels_c = read_jsonl(OUT / "candidates_r1.relations.jsonl")
    rels_q = read_jsonl(OUT / "qc_sample.relations.jsonl")
    cards = json.load(open(OUT / "cards_r1.json"))
    fails = {k: json.load(open(TMP / f"{k}_fail.json")) for k in ("cand", "qc", "dev") if (TMP / f"{k}_fail.json").exists()}
    held = set(packs.heldout_ids())
    train_styles = {r["meta"]["format_style"] for r in cand + qc}
    dev_styles = {r["meta"]["format_style"] for r in dev}
    from .render import fpool
    ho = fpool.held_out_style_ids()
    M = {
        "family": "F2", "what": "C round-1 F2 generator outputs: candidate pool (1.5x), G6 QC sample, S5 mix-tuning dev "
                                "items and the F2 depth sweep. No crowd scores yet (G9 runs on the free L4).",
        "gen_version": GEN_VERSION, "spec_id": SPEC_ID, "g0_spec_sha256": SPEC_SHA256, "seed": SEED, "git_sha": git_sha(),
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "binding_sha256": {k: _sha(LEAN / p) for k, p in (("C_DATA_SPEC.md", "c_spec/C_DATA_SPEC.md"),
                                                          ("C_TRAIN_RECIPE.md", "c_spec/C_TRAIN_RECIPE.md"),
                                                          ("PREREG_FINAL.md", "PREREG_FINAL.md"),
                                                          ("G0_SPEC.md", "c_src/F2/G0_SPEC.md"),
                                                          ("decoder_io.py", "decoder_io.py"),
                                                          ("train_decoder.py", "train_decoder.py"),
                                                          ("negcount.py", "c_src/common/negcount.py"),
                                                          ("fmt1/card.py", "c_src/formats/formats-1/fmt1/card.py"))},
        "sealed_suite_sha256_A15": SUITE,
        "parents": parents_list(),
        "relations": relations_block(),
        "files": [{"path": f"out/{p.name}", "rows": sum(1 for _ in open(p)) if p.suffix == ".jsonl" else None,
                   "sha256": sha_file(p)} for p in sorted(OUT.glob("*")) if p.name != "MANIFEST.json"],
        "code": [{"path": f"gen/{p.name}", "sha256": sha_file(p)} for p in sorted((F2 / "gen").glob("*.py"))],
        "counts": {"candidates_r1": len(cand), "qc_sample": len(qc), "mixdev_S5": len(dev),
                   "mixdev_parts": dict(Counter(r["meta"].get("mixdev") for r in dev)),
                   "sweep_by_level_sampler": dict(Counter(f"L{r['meta']['sweep_level']}:{r['meta']['sampler']}"
                                                          for r in dev if r["meta"].get("mixdev") == "sweep")),
                   "round1_target_rows": 3150, "candidate_target_rows": 4725,
                   "relations_candidates": dict(Counter(x["type"] for x in rels_c)),
                   "relations_qc": dict(Counter(x["type"] for x in rels_q))},
        "cards": {"n": len(cards), "by_sampler": dict(Counter(c["sampler"] for c in cards)),
                  "by_schema": dict(Counter(c["schema"] for c in cards)),
                  "open_world": sum(1 for c in cards if c["world"] == "open"),
                  "fewshot": sum(1 for c in cards if c["instr"] == "fewshot"),
                  "inverted": sum(1 for c in cards if c["instr"] == "inverted"),
                  "short": sum(1 for c in cards if c.get("short")),
                  "with_flip_variants": sum(1 for c in cards if c.get("variants")),
                  "one_card_per_pack": len({c["pack"] for c in cards}) == len(cards),
                  "defs_styles": dict(Counter(c["defs_style"] for c in cards))},
        "packs": {"training_packs_used": len({r["meta"]["domain_pack"] for r in cand + qc}),
                  "heldout_packs_used_by_dev": len({r["meta"]["domain_pack"] for r in dev}),
                  "training_rows_on_heldout_packs": sum(1 for r in cand + qc if r["meta"]["domain_pack"] in held),
                  "dev_rows_on_training_packs": sum(1 for r in dev if r["meta"]["domain_pack"] not in held),
                  "heldout_rule": "union of the pack agents' proposals (packs-1 heldout_proposal, packs-3 heldout_hint, "
                                  "packs-4 split_hint heldout; packs-2: sha256(id) mod 8 == 0); orchestrator to confirm",
                  "pool_split": {"training": len(tr), "heldout": len(he)}},
        "styles": {"training_styles_used": len(train_styles), "heldout_styles_in_training_rows": len(train_styles & ho),
                   "dev_styles_used": len(dev_styles), "dev_rows_on_training_styles": sum(1 for r in dev if r["meta"]["format_style"] not in ho),
                   "containers_training": dict(Counter(fpool.style(r["meta"]["format_style"])["container"] for r in cand))},
        "s5_in_training_files": sum(1 for r in cand + qc if r["meta"]["sampler"] == "S5"),
        "option_level_rows": sum(1 for r in cand + qc + dev if r["meta"].get("option_level") is not None),
        "stats": {"candidates_r1": stats.stats(cand, rels_c), "qc_sample": stats.stats(qc, rels_q), "mixdev_S5": stats.stats(dev)},
        "gates": gates, "generation_fails": fails, "sealed_check": sealed,
        "gen_version_rows": {f: dict(Counter(r["meta"]["gen_version"] for r in rows[f])) for f in ROW_FILES},
        "resume_notes": NOTES,
    }
    write_json(OUT / "MANIFEST.json", M)
    rc, hits, s = run_sealed(wrap_json(OUT / "MANIFEST.json"), rows_like=False)
    progress(f"manifest written; sealed_check on MANIFEST: hits {len(hits)}")
    return M


if __name__ == "__main__":
    sys.exit(main())
