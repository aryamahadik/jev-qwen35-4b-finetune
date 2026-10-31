"""out/MANIFEST.json: counts, sha256, sampler / pack / style / wording coverage, gate results, deviations.

  python -m gen.manifest
"""
from __future__ import annotations

import collections
import json

from .common import (CSRC, F5, G0, G0_SHA256, GEN_VERSION, LEAN, OUT, SPEC_ID, TMP, now_utc, read_jsonl, sha_file)

SETS = [("candidates_r1", "round-1 candidate pool (1.5 x 3,600 rows; training samplers S1-S4)"),
        ("qc_sample", "separate G6 QC sample (same generators, other seed tag)"),
        ("mixdev_S5", "mix-tuning dev items: S5 held-out sampler, held-out packs and styles (never training)"),
        ("probe_hardneg", "hard-negation probe (held-out cue templates; report-only, never training)")]


def g4_per_sampler(name, rows, counts):
    """G4 groups inverted-card rows as INV; every INV row is checked when INV:rows equals the eligible INV rows, so the
    per-sampler total is S:rows plus that sampler's eligible inverted rows (exact; None if not every INV row ran)."""
    bases = {b["base_id"]: b for b in read_jsonl(TMP / f"{name}.bases.jsonl")}
    side = {x["id"]: x["base_id"] for x in read_jsonl(OUT / f"{name}.F5_polarity.jsonl")}
    inv = collections.Counter(bases[side[r["id"]]]["sampler"] for r in rows
                              if r["role"] != "attack" and bases[side[r["id"]]].get("inverted"))
    if counts.get("INV:rows", 0) != sum(inv.values()):
        return None
    return {s: counts.get(f"{s}:rows", 0) + inv.get(s, 0) for s in ("S1", "S2", "S3", "S4")}


def gate_summary(name, rows, ent):
    """One pass/fail line per required gate (G3, G4, G15, G18, negcount quotas, length, held-out styles, S5)."""
    g = ent.get("gates", {})
    rep = ent.get("report", {})
    g4 = ent.get("G4")
    toks = g.get("G15", {}).get("served_tokens", {})
    ordinal = sum(1 for r in rows if r.get("qtype") not in ("noul",) or r.get("options") or "option_level" in r)
    out = {"G3_roundtrip": {"rows_ok": g.get("G3", {}).get("rows_ok"), "rows": len(rows),
                            "pass": g.get("G3", {}).get("pass") and g["G3"]["rows_ok"] == len(rows)},
           "G15_loader": {"ok": g.get("G15", {}).get("ok"), "pass": g.get("G15", {}).get("pass")},
           "G18_ordinal_lint": {"ordinal_or_choice_rows": ordinal, "pass": ordinal == 0,
                                "note": "F5 has no ordinal or choice rows (yes/no raw form only); lint = 0 such rows"},
           "length": {"max_served_tokens_instructions_twice": toks.get("max"), "cap_F5": 1900, "cap_spec": 7900,
                      "pass": (toks.get("max") or 10 ** 9) < 1900}}
    if g4 is not None:
        n = sum(v for k, v in g4["counts"].items() if k.endswith(":rows"))
        fails = sum(v for k, v in g4["counts"].items() if k.lower().endswith(":fail"))
        per = g4_per_sampler(name, rows, g4["counts"])
        out["G4_metamorphic"] = {"rows": n, "fails": fails, "errors": len(g4.get("errors", [])),
                                 "rows_per_sampler_incl_inverted": per,
                                 "relations": sorted({k.split(":")[1] for k in g4["counts"] if k.count(":") == 2}),
                                 "pass": (n >= 1000 and fails == 0 and not g4.get("errors")
                                          and bool(per) and all(v >= 1000 for v in per.values()))}
    if rep and name != "probe_hardneg":
        out["negcount_quotas"] = {"k_syn_ge1": rep.get("share_k_syn_ge1"), "k_syn_ge1_min": 0.10,
                                  "k_syn_ge2_aff_twin": rep.get("share_k_syn_ge2_with_aff_twin"),
                                  "k_syn_ge2_aff_twin_min": 0.02, "k_all_ge2": rep.get("share_k_all_ge2"),
                                  "k_all_ge2_min": 0.30, "k_all_ge_k_every_row": rep.get("k_all_ge_k_every_row"),
                                  "yes_by_k_all": {k: v["yes"] for k, v in rep.get("yes_by_k_all", {}).items()},
                                  "pass": (rep.get("share_k_syn_ge1", 0) >= 0.10
                                           and rep.get("share_k_syn_ge2_with_aff_twin", 0) >= 0.02
                                           and rep.get("share_k_all_ge2", 0) >= 0.30
                                           and bool(rep.get("k_all_ge_k_every_row"))
                                           and all(abs(v["yes"] - 0.5) <= 0.02 for v in rep["yes_by_k_all"].values()))}
    return out


def cov(rows):
    m = [r["meta"] for r in rows]
    return {"rows": len(rows), "by_sampler": dict(collections.Counter(x["sampler"] for x in m)),
            "by_role": dict(collections.Counter(r["role"] for r in rows)),
            "cards": len({x["card_id"] for x in m}), "packs": sorted({x["domain_pack"] for x in m}),
            "n_packs": len({x["domain_pack"] for x in m}), "n_styles": len({x["format_style"] for x in m}),
            "styles": sorted({x["format_style"] for x in m}), "n_wordings": len({x["wording_id"] for x in m}),
            "defs_styles": dict(collections.Counter(x["defs_style"] for x in m)),
            "persona_seeds": len({x["persona_seed"] for x in m}),
            "yes_rate": round(sum(r["gold"] for r in rows) / len(rows), 4)}


PARENTS = [  # spec 3.H / G1 (MIXER_NOTE 1): every pack, codebook, wording set and real-text dataset the rows derive from
    ("pack_file", "packs-4 domain packs (training cards S1-S4)", "packs/packs-4/packs.jsonl"),
    ("pack_manifest", "packs-4 manifest", "packs/packs-4/manifest.json"),
    ("pack_file", "packs-3 domain packs (S5 held-out packs, mixdev only)", "packs/packs-3/packs-3.jsonl"),
    ("pack_manifest", "packs-3 manifest", "packs/packs-3/packs-3.manifest.json"),
    ("wording_set", "formats-2 family wording pools (F5 rows)", "formats/formats-2/wordings/family_pools.jsonl"),
    ("wording_manifest", "formats-2 manifest", "formats/formats-2/manifest.json"),
    ("codebook", "formats-1 (fmt1) format style pool and label tools: MANIFEST", "formats/formats-1/MANIFEST.json"),
] + [("codebook", "formats-1 (fmt1) data: " + n, "formats/formats-1/data/" + n) for n in (
    "card_styles.jsonl", "containers.jsonl", "defs_styles.jsonl", "fences.jsonl", "fewshot_templates.jsonl",
    "instr_positions.jsonl", "inverted.jsonl", "label_masks.jsonl", "label_notices.jsonl", "label_rules.jsonl",
    "registers.jsonl", "skins.jsonl", "styles.jsonl", "swap_words.jsonl")] + [
    ("tool", "negation counter (shared)", "common/negcount.py"),
    ("family_cue_bank", "F5 cue-template bank (family-authored, CC0)", "F5/out/cue_bank.json")]


def parents():
    out = []
    for kind, name, rel in PARENTS:
        q = CSRC / rel
        if q.exists():
            out.append({"kind": kind, "name": name, "path": f"lean/c_src/{rel}", "sha256": sha_file(q)})
    out.append({"kind": "real_text_dataset", "name": "none: S6 public human-gold bases not built (see deviations)",
                "path": None, "sha256": None})
    return out


def relations_summary(names):
    res = {}
    for name in names:
        rel_p = OUT / f"{name}.relations.jsonl"
        if rel_p.exists():
            rr = read_jsonl(rel_p)
            res[name] = {"path": f"out/{name}.relations.jsonl", "sha256": sha_file(rel_p), "count": len(rr),
                         "lines": len(rr), "by_type": dict(collections.Counter(r["type"] for r in rr))}
    return res


def main():
    from fmt1 import pool as fpool
    held_styles = fpool.held_out_style_ids()
    man = {"family": "F5", "builder": "F5 generator author (phase 2)", "gen_version": GEN_VERSION, "spec_id": SPEC_ID,
           "written_utc": now_utc()}
    man["binding"] = {
        "G0_SPEC.md": {"sha256": sha_file(G0), "frozen_sha256": G0_SHA256, "match": sha_file(G0) == G0_SHA256},
        "C_DATA_SPEC.md": sha_file(LEAN / "c_spec" / "C_DATA_SPEC.md"),
        "C_TRAIN_RECIPE.md": sha_file(LEAN / "c_spec" / "C_TRAIN_RECIPE.md"),
        "PREREG_FINAL.md": sha_file(LEAN / "PREREG_FINAL.md"),
        "negcount.py": sha_file(CSRC / "common" / "negcount.py"),
        "fmt1 MANIFEST": sha_file(CSRC / "formats" / "formats-1" / "MANIFEST.json"),
        "formats-2 manifest": sha_file(CSRC / "formats" / "formats-2" / "manifest.json"),
        "packs-3": sha_file(CSRC / "packs" / "packs-3" / "packs-3.jsonl"),
        "packs-4": sha_file(CSRC / "packs" / "packs-4" / "packs.jsonl"),
        "decoder_io.py": sha_file(LEAN / "decoder_io.py"), "train_decoder.py": sha_file(LEAN / "train_decoder.py"),
        "tokenizer": {"file": "c_src/public/public-3/tmp/tokenizer.json (Qwen3.5-4B tokenizer.json)",
                      "sha256": sha_file(CSRC / "public" / "public-3" / "tmp" / "tokenizer.json")}}
    man["parents"] = parents()
    man["code"] = {p.name: sha_file(p) for p in sorted((F5 / "gen").glob("*.py"))}
    bank = json.load(open(OUT / "cue_bank.json"))
    man["cue_bank"] = {"file": "out/cue_bank.json", "sha256": sha_file(OUT / "cue_bank.json"),
                       "n_templates": bank["n_templates"], "families": bank["families"],
                       "probe_holdout": bank["probe_holdout"],
                       "probe_holdout_sha256": bank["sha256_of_templates_and_holdout"]}
    man["outputs"] = {}
    for name, what in SETS:
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        rows = read_jsonl(p)
        c = cov(rows)
        side_p = OUT / f"{name}.F5_polarity.jsonl"
        rel_p = OUT / f"{name}.relations.jsonl"
        ent = {"what": what, "file": f"out/{name}.jsonl", "sha256": sha_file(p), **c,
               "held_out_style_rows": sum(1 for r in rows if r["meta"]["format_style"] in held_styles),
               "relations": {"file": f"out/{name}.relations.jsonl", "sha256": sha_file(rel_p),
                             "n": len(read_jsonl(rel_p))},
               "polarity_sidecar": {"file": f"out/{name}.F5_polarity.jsonl", "sha256": sha_file(side_p)},
               "cards_file": {"file": f"out/{name}.cards.jsonl", "sha256": sha_file(OUT / f"{name}.cards.jsonl")}}
        for extra in ("buildstats", "report", "gates", "G4"):
            q = OUT / f"{name}.{extra}.json"
            if q.exists():
                ent[extra] = json.load(open(q))
        ent["gate_summary"] = gate_summary(name, rows, ent)
        man["outputs"][name] = ent
    man["relations"] = relations_summary(list(man["outputs"]))
    q = OUT / "sealed_check_summary.json"
    if q.exists():
        man["sealed_check"] = json.load(open(q))
    q = TMP / "deviations.json"
    if q.exists():
        man["deviations_and_problems"] = json.load(open(q))
    json.dump(man, open(OUT / "MANIFEST.json", "w"), indent=1)
    print(json.dumps({k: (v if k not in ("outputs", "code") else list(v)) for k, v in man.items()}, indent=1)[:3000])


if __name__ == "__main__":
    main()
