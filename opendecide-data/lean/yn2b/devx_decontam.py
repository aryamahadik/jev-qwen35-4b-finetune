"""devx_decontam.py: SPEC section 7 checks on reviewer R's 500 devx rows, before they are assembled (programs only).

Runs check_yn2b's own functions on the devx rows in the golden format (built in memory by build_devx), never on other
rows:
  7.1  12-word runs against held-out text (OHS-1/2, eval*, JevBench public) and OHS-3 by check_yn2b.ohs3_blind,
       which reads OHS-3 inside one function and returns COUNTS ONLY (no OHS-3 text, id or row is printed or kept);
  7.2  12-word runs against every dev / eval split;
  7.3  6-word runs of the devx instructions against the reference template sets, the banned judge words, cue shares
       and the marker rule;
  7.5  exact dedupe against golden_train and inside devx;
  7.6  every devx state shares at most 20% of its 12-grams with any single train state of the five families;
  7.7  the devx names (people and organisations shown in the rows) against JevBench public and OHS-1/2 text, and
       against OHS-3 by hash only (counts).
Writes yn2b/devx_decontam.json (counts and the devx row ids of non-OHS-3 hits only) and a MANIFEST_yn2b record.

  ../.venv/bin/python yn2b/devx_decontam.py [--write] [--overwrite]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN / "yn2b"))
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import yn2b_common as yc  # noqa: E402
import check_yn2b as ck  # noqa: E402
import mv_core as mv  # noqa: E402
import build_devx as bd  # noqa: E402

OUT = LEAN / "yn2b" / "devx_decontam.json"


def devx_names(built: dict) -> list:
    """(family source, name) for the people and organisations that devx rows show (from the latents)."""
    out = set()
    for key, b in built.items():
        src = f"gd_{key}"
        mod = bd.module(key)
        items = {it.lid: it for it in mod.load()} if key != "gen3_lead_score" else None
        for g in b.golden:
            lid = g["meta"]["latent_id"]
            if key == "gen3_lead_score":
                continue
            it = items[lid]
            f = it.facts
            if key == "gen3_rule_chain":
                out |= {(src, f["doc"]["org"]), (src, f["case"]["name"])}
                if f["case"].get("decoy"):
                    out.add((src, f["case"]["decoy"]["name"]))
            elif key == "gen3_tool_guard":
                out.add((src, f.user_name))
                for c in getattr(f, "confs", []):
                    out.add((src, c.by_name))
            elif key == "gen3_state_track":
                P = f["params"]
                for k in ("users", "eng", "editors", "approvers"):
                    out |= {(src, x) for x in P.get(k, [])}
            elif key == "gen3_def_literal":
                for k in ("item", "org", "officer", "bg_from"):
                    if isinstance(f.get(k), str) and f[k][:1].isupper():
                        out.add((src, f[k]))
    if "gen3_lead_score" in built:
        src = "gd_gen3_lead_score"
        for g in built["gen3_lead_score"].golden:
            st = g["state"]
            for ln in st.replace('"', "\n").split("\n"):
                for tag in ("Company: ", "Owner (sales rep): ", "Primary contact: ", "Other contact: "):
                    if tag in ln:
                        v = ln.split(tag, 1)[1]
                        v = v.split(" (")[0].split(", ")[0]
                        out.add((src, v.strip()))
    return sorted(out)


def run(built: dict) -> dict:
    root = LEAN
    devx = [g for b in built.values() for g in b.golden]
    rep = {"rows": len(devx), "families": sorted({r["source"] for r in devx})}
    held, miss_h = ck.held_sets(root)
    h12, hunits = ck.check_12(devx, held)
    rep["7.1_heldout_12gram_units"] = h12
    rep["7.1_heldout_hit_units"] = hunits
    names = devx_names(built)
    o3_units, _o3_hashes, o3_names, o3_loaded = ck.ohs3_blind(root, devx, names)
    rep["7.1_ohs3_hit_units_per_family"] = dict(o3_units)          # COUNTS ONLY
    rep["7.1_ohs3_loaded"] = o3_loaded
    dvs, miss_d = ck.dev_sets(root)
    d12, dunits = ck.check_12(devx, dvs)
    rep["7.2_dev_12gram_units"] = d12
    rep["7.2_dev_hit_units"] = dunits
    rep["missing_reference_files"] = miss_h + miss_d
    items = ck.template_items(devx, None)
    items = [x for x in items if x[0] != "mv_core_plants"]          # devx has no attack plants
    refs = ck.template_refs(root)
    tcount, texamples = ck.check_templates(items, refs)
    rep["7.3_template_clashes"] = tcount
    rep["7.3_template_clash_examples"] = texamples
    bw = ck.banned_words(devx)
    rep["7.3_banned_words"] = {f: len(v) for f, v in bw.items()}
    rep["7.3_cue_shares"] = ck.cue_shares(items)
    rep["7.3_marker_violations"] = len(ck.marker_rule(devx))
    drop, drep = ck.dedupe(devx, root / "data" / "v14_parts" / "golden_train.jsonl")
    rep["7.5_dedupe"] = {**drep, "units": len(drop)}
    train = []
    for key in built:
        raw, _ = mv.read_raw(key, "train")
        train += raw
    _fails, dtrep = ck.dev_vs_train(train, devx)
    rep["7.6_devx_vs_train"] = dtrep
    nm = ck.name_check(root, names)
    rep["7.7_names"] = {"checked": len(names), "found_in_jevbench_or_ohs12": {f: len(v) for f, v in nm.items()},
                        "examples": {f: v[:5] for f, v in nm.items()}, "ohs3_hash_hits_per_family": dict(o3_names)}
    rep["ok"] = (not hunits and not dunits and not any(tcount.values()) and not bw and not rep["7.3_marker_violations"]
                 and not drop and not dtrep["failing_units"] and not nm and not o3_names and not sum(o3_units.values())
                 and all(v["pass"] for v in rep["7.3_cue_shares"].values()))
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)
    built = bd.build(list(bd.MODULES))
    rep = run(built)
    print(json.dumps({k: v for k, v in rep.items() if not k.endswith("_hit_units")}, indent=1, default=str))
    if a.write:
        if OUT.exists() and not a.overwrite:
            raise SystemExit(f"{OUT} exists; pass --overwrite")
        OUT.write_text(json.dumps(rep, indent=1, default=str) + "\n")
        mv.manifest_append({"tool": "yn2b/devx_decontam.py", "key": "devx", "part": "devx_decontam",
                            "path": mv._rel(OUT), "rows": rep["rows"],
                            "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(), "ok": rep["ok"]})
        print("wrote", mv._rel(OUT))
    return rep


if __name__ == "__main__":
    main()
