"""F10 bookkeeping: out/MANIFEST.json (files, parts, relations, parents, code) and qc/QC_REPORT.json (pool sha256s,
gate results). Reads only F10 outputs, gate reports and parent files' bytes (sha256). Run after every regeneration
and gate run: python qc/write_manifest.py"""
from __future__ import annotations

import collections as C
import datetime
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
F10 = HERE.parent
OUT = F10 / "out"
CSRC = F10.parent
LEAN = CSRC.parent
sys.path.insert(0, str(F10 / "gen"))
import common  # noqa: E402

PARTS = {"candidates": "candidates_r1", "qc_sample": "qc_sample", "mixdev": "mixdev_S5"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def lines(p):
    with open(p, "rb") as f:
        return sum(1 for _ in f)


def jl(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def rel(p):
    return str(Path(p).resolve().relative_to(LEAN))


def load_json(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return default


def main():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    files = {}
    for p in sorted(OUT.glob("*.json*")):
        if p.name in ("MANIFEST.json",) or p.name.endswith(".remote"):
            continue
        files[p.name] = {"sha256": sha(p), "lines": lines(p)}
    parts, packs_used, personas, s7_src = {}, set(), set(), C.Counter()
    for key, name in PARTS.items():
        rows = jl(OUT / f"{name}.jsonl")
        side = {m["id"]: m for m in jl(OUT / f"{name}.sidecar.jsonl")}
        fs = sum(1 for r in rows if r["meta"].get("format_style"))
        yn = sum(1 for r in rows if side[r["id"]]["form"] == "yn")
        ys = sum(1 for r in rows if side[r["id"]]["form"] == "yn" and r["gold"] in (1, "yes", "Yes", True))
        parts[key] = {"file": f"{name}.jsonl", "rows": len(rows), "yes_no_rows": yn, "choice_rows": len(rows) - yn,
                      "yes_rate_yes_no": round(ys / max(1, yn), 4),
                      "by_sampler": dict(sorted(C.Counter(r["meta"]["sampler"] for r in rows).items())),
                      "by_form": dict(C.Counter(side[r["id"]]["form"] for r in rows)),
                      "rows_with_format_style": fs, "cards": len({r["meta"]["card_id"] for r in rows})}
        for r in rows:
            packs_used.add((r["meta"].get("domain_pack"), key))
            ps = r["meta"].get("persona_seed")
            if isinstance(ps, dict):
                personas.add(ps.get("onet_code"))
            elif ps:
                personas.add(str(ps))
            if r["meta"]["sampler"] == "S7":
                ts = r["meta"].get("text_source")
                s7_src[((ts or {}).get("dataset") if isinstance(ts, dict) else ts, r["meta"].get("licence"), key)] += 1
    relations = {}
    for name in ("candidates_r1", "qc_sample"):
        p = OUT / f"{name}.relations.jsonl"
        if p.exists():
            rr = jl(p)
            relations[f"{name}.relations.jsonl"] = {"sha256": sha(p), "lines": len(rr),
                                                    "by_type": dict(C.Counter(x["type"] for x in rr))}
    # parents (spec 3.H / G1): every pack, codebook, wording set and real-text dataset the rows derive from
    packs = {}
    for src in ("packs-2", "packs-4"):
        for pk in jl(CSRC / "packs" / src / "packs.jsonl"):
            packs[pk["id"]] = (src, pk.get("parents"), pk.get("licence"))
    parents = []
    for src in ("packs-2", "packs-4"):
        for f in ("packs.jsonl", "manifest_packs2.json" if src == "packs-2" else "manifest.json"):
            p = CSRC / "packs" / src / f
            if p.exists():
                parents.append({"kind": "pack_file", "path": rel(p), "sha256": sha(p)})
    for pid in sorted({p for p, _ in packs_used if p}):
        src, par, lic = packs.get(pid, (None, None, None))
        parents.append({"kind": "domain_pack", "id": pid, "source": src, "parents": par, "licence": lic,
                        "used_in": sorted({k for p, k in packs_used if p == pid})})
    f1 = CSRC / "formats" / "formats-1"
    parents.append({"kind": "formats-1", "path": rel(f1 / "MANIFEST.json"), "sha256": sha(f1 / "MANIFEST.json")})
    for p in sorted((f1 / "data").glob("*.jsonl")):
        parents.append({"kind": "formats-1_pool", "path": rel(p), "sha256": sha(p)})
    f2 = CSRC / "formats" / "formats-2"
    for sub, kind in (("manifest.json", "formats-2"), ("codebooks/codebooks.jsonl", "codebooks"),
                      ("codebooks/lexicon.json", "codebook_lexicon"), ("wordings/family_pools.jsonl", "wordings")):
        parents.append({"kind": kind, "path": rel(f2 / sub), "sha256": sha(f2 / sub)})
    for ds in ("xed", "ghc", "mams_acsa", "mams_atsa"):
        p = f2 / "records" / f"{ds}.jsonl"
        parents.append({"kind": "real_text_records", "dataset": ds, "path": rel(p), "sha256": sha(p),
                        "rows": {k: sum(v for (t, _, kk), v in s7_src.items() if t == ds and kk == k)
                                 for k in PARTS}})
    p3 = CSRC / "public" / "public-3"
    for sub in ("out/public3_split_3e.jsonl", "out/public3_record_claims.jsonl", "manifest_public3.json"):
        if (p3 / sub).exists():
            parents.append({"kind": "public-3", "path": rel(p3 / sub), "sha256": sha(p3 / sub)})
    parents.append({"kind": "real_text_licences", "by_source": [{"dataset": t, "licence": l, "part": k, "rows": v}
                                                               for (t, l, k), v in sorted(s7_src.items(), key=str)]})
    parents.append({"kind": "persona_seeds", "source": "O*NET 31.0 Occupation Data (CC BY 4.0) via packs",
                    "n_distinct": len(personas)})
    mr = load_json(OUT / "merge_report.json", {})
    gates = {k: load_json(OUT / f"{n}.gates.json") for k, n in PARTS.items()}
    sealed = {}
    for k, n in PARTS.items():
        s = load_json(OUT / f"{n}.sealedqc.summary.json")
        if s:
            sealed[k] = {"rows": s.get("rows"), "rows_hit": s.get("rows_hit"), "input_sha256": s.get("input_sha256"),
                         "current": s.get("input_sha256") == files.get(f"{n}.jsonl", {}).get("sha256"),
                         "checker_sha256": s.get("checker_sha256")}
    g4 = load_json(HERE / "g4_report.json")
    tdr = load_json(HERE / "token_dryrun.json")
    problems = [
        "LENGTH: A22 ruling applied (tmp/repair/LENGTH_RULING.md; proof tmp/repair/INFEASIBLE_length.md, RESOLVED): "
        "every row <= 7,900 tokens (instructions twice), all shares and buckets kept, trim levers on; the mix-level "
        "cap (rows >= 2,000 tokens <= 9% of new rows and <= 30% of new-row tokens) is the mixer's (see per-part "
        "G15 share_rows_ge_2000 / share_tokens_in_rows_ge_2000).",
        "EDOS: formats-2 marks 0 EDOS records F10_S7-eligible -> 0 EDOS rows; candidates target 4,995 not 5,400.",
        "S5 mixdev: packs-4 held-out packs have no label_words -> no swapped-name mode on S5 (neutral / invented only).",
    ]
    if g4 and (g4.get("base") or {}).get("base_render_error"):
        problems.append("G4 (qc only, G4 seed range): base rows not rendered " + json.dumps(g4["base"]) +
                        "; skipped like build render drops (the emitted parts have 0 render_fail); every (sampler, MR) "
                        "cell still passes 100% on >= 1,000 rows. Card draws that failed on all salts: "
                        + str(len(g4.get("card_errors") or [])) + " (first 10 listed in qc/g4_report.json).")
    if not g4 or "S6|MR9" not in (g4.get("per_sampler_mr") or {}):
        problems.append("MR9 on S6 not run in the current G4 report.")
    if not g4 or g4.get("not_run"):
        problems.append("G4 incomplete: " + "; ".join((g4 or {}).get("not_run", ["not run"])))
    man = {"family": common.FAMILY, "spec_id": common.SPEC_ID, "g0_sha256": sha(F10 / "G0_SPEC.md"),
           "gen_version": common.GEN_VERSION, "written_utc": now,
           "binding": {"PREREG_FINAL": "A15, A16, A16.1, A16.2, A19, A20, A21", "C_DATA_SPEC": "v4",
                       "decoder_io": sha(LEAN / "decoder_io.py")[:8], "train_decoder": sha(LEAN / "train_decoder.py")[:8]},
           "files": files, "parts": parts, "relations": relations,
           "relation_unit_sizes": {k: v.get("unit_sizes") for k, v in mr.items() if isinstance(v, dict) and "unit_sizes" in v},
           "mixdev_separation": (mr.get("mixdev_S5") or {}).get("separation_overlaps"),
           "parents": parents,
           "length": {k: tdr.get(k) for k in ("training_parts_all", "counterfactual_instructions_once")} if tdr else None,
           "code": {p.name: sha(p) for p in sorted(list((F10 / "gen").glob("*.py")) + list(HERE.glob("*.py")))},
           "problems": problems}
    (OUT / "MANIFEST.json").write_text(json.dumps(man, indent=1))
    failed = []
    for k, g in gates.items():
        if not g:
            failed.append(f"{k}: no gate report")
            continue
        if g["G3"]["fail"]:
            failed.append(f"{k}: G3")
        if g["G2"]["mismatch"]:
            failed.append(f"{k}: G2")
        if g["G15"].get("loader_fail") or g["G15"].get("check_rows_whole_part") != "pass":
            failed.append(f"{k}: G15 loader")
        if g["G15"].get("units_bad") or g["G15"].get("rows_gt_7900"):
            failed.append(f"{k}: length (A22: <= 7,900 per row; 3-row units < 2,000): rows_gt_7900 "
                          f"{g['G15'].get('rows_gt_7900')}, units_bad {g['G15'].get('units_bad')}")
        if not (g.get("negcount") or {}).get("pass", True):
            failed.append(f"{k}: negcount")
    for k, s in sealed.items():
        if s["rows_hit"] or not s["current"]:
            failed.append(f"{k}: sealed_check {'hits' if s['rows_hit'] else 'stale'}")
    if not g4 or not g4.get("pass_all_run") or g4.get("not_run"):
        failed.append("G4: " + ("not run" if not g4 else f"pass_all_run {g4.get('pass_all_run')}, min rows "
                                f"{g4.get('min_rows_per_run_mr')}, not run {len(g4.get('not_run', []))}"))
    pool = {"candidates_r1.jsonl": files["candidates_r1.jsonl"]["sha256"],
            "candidates_r1.relations.jsonl": files["candidates_r1.relations.jsonl"]["sha256"],
            "qc_sample.jsonl": files["qc_sample.jsonl"]["sha256"], "mixdev_S5.jsonl": files["mixdev_S5.jsonl"]["sha256"]}
    qc = {"report": "F10 QC report (gen:F10, c-lanes-v3)", "written_utc": now, "gen_version": common.GEN_VERSION,
          "inputs_sha256": {"G0_SPEC.md": man["g0_sha256"]}, "rows": {k: v["rows"] for k, v in parts.items()},
          "pool_sha256": pool, "gates": {"per_part": gates, "sealed_check": sealed,
                                         "G4": {k: g4.get(k) for k in ("per_sampler_mr", "pass_all_run",
                                                                       "min_rows_per_run_mr", "not_run")} if g4 else None,
                                         "G18": "n/a (F10 has no ordinal row)",
                                         "length_dry_run": man["length"]},
          "failed_gates": failed, "pass": not failed, "problems": problems}
    (HERE / "QC_REPORT.json").write_text(json.dumps(qc, indent=1))
    print("MANIFEST", len(files), "files;", len(parents), "parents; failed:", failed)


if __name__ == "__main__":
    main()
