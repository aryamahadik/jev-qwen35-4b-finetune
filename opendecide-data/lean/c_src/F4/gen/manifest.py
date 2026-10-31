"""out/MANIFEST.json: counts, sha256, sampler / pack / style / card / wording coverage, gate and check results.

  python manifest.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import pickle
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
F4 = HERE.parent
OUT = F4 / "out"
LOGS = F4 / "logs"
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE))
import f4lex as L  # noqa: E402

SETS = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jl(p):
    with open(p) as f:
        return [json.loads(x) for x in f]


def jload(p):
    try:
        with open(p) as f:
            t = f.read()
        return json.loads(t[t.index("{"):])
    except (OSError, ValueError):
        return None


def coverage(rows, side):
    sd = {s["id"]: s for s in side}
    c = collections.Counter
    cards = {r["meta"]["card_id"] for r in rows}
    wc = collections.defaultdict(set)
    for r in rows:
        wc[r["meta"]["card_id"]].add(r["meta"]["wording_id"])
    defs = {}
    for r in rows:
        defs.setdefault(r["meta"]["card_id"], r["meta"]["defs_style"])
    return {
        "rows": len(rows),
        "groups": len({r["group_id"] for r in rows}),
        "call_units": len({r["call_id"] for r in rows}),
        "cards": len(cards),
        "packs": len({r["meta"]["domain_pack"] for r in rows}),
        "persona_seeds": len({r["meta"].get("persona_seed") for r in rows if r["meta"].get("persona_seed")}),
        "rows_with_persona_seed": sum(1 for r in rows if r["meta"].get("persona_seed")),
        "samplers": dict(sorted(c(r["meta"]["sampler"] for r in rows).items())),
        "format_styles": len({r["meta"]["format_style"] for r in rows}),
        "wordings": len({r["meta"]["wording_id"] for r in rows}),
        "min_wordings_per_card": min(len(v) for v in wc.values()),
        "defs_style_cards": dict(c(defs.values())),
        "qtype": dict(c(r["qtype"] for r in rows)),
        "forms": dict(sorted(c(sd[r["id"]]["form"] for r in rows).items())),
        "units": dict(sorted(c(sd[r["id"]]["unit"] for r in rows).items())),
        "twin_kinds": dict(sorted(c(str(r["meta"]["twin_kind"]) for r in rows).items())),
        "depth": dict(sorted(c(r["meta"]["depth"] for r in rows).items())),
        "deep_rows": sum(1 for r in rows if r["meta"]["deep"]),
        "worlds": dict(sorted(c(next(e for e in r["meta"]["edge"] if e.startswith("world:"))
                                for r in rows).items())),
        "labels": dict(sorted(c(next(e for e in r["meta"]["edge"] if e.startswith("L:")) for r in rows).items())),
        "rows_per_card_min_median_max": (lambda v: [v[0], v[len(v) // 2], v[-1]])(
            sorted(c(r["meta"]["card_id"] for r in rows).values())),
    }


def main():
    pl = pickle.load(open(F4 / "tmp" / "cards_r1.pkl", "rb"))
    man = {
        "family": "F4", "spec_id": L.SPEC_ID, "gen_version": L.GEN_VERSION, "round": 1,
        "g0_spec_sha256": sha(F4 / "G0_SPEC.md"),
        "g0_frozen_sha256": json.load(open(F4 / "G0_FROZEN.json"))["sha256"],
        "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_sha": subprocess.run(["git", "-C", str(LEAN), "rev-parse", "HEAD"], capture_output=True,
                                  text=True).stdout.strip(),
        "determinism": "PYTHONHASHSEED=0 (build.py re-execs), fixed seeds, results sorted by card; re-runs give "
                       "byte-identical rows",
        "plan": {"training_cards": len(pl["cards"]), "dev_cards_S5": len(pl["dev"]),
                 "training_packs": len({c.pack["pack_id"] for c in pl["cards"]}),
                 "dev_packs_heldout": len({c.pack["pack_id"] for c in pl["dev"]}),
                 "card_classes": dict(collections.Counter(c.cls for c in pl["cards"])),
                 "inverted_cards": sum(1 for c in pl["cards"] if c.inverted),
                 "short_cards": sum(1 for c in pl["cards"] if c.short),
                 "fewshot_cards": sum(1 for c in pl["cards"] if getattr(c, "fewshot", False))},
        "files": {}, "sets": {}, "gates": {}, "g4": {}, "quota": {}, "sealed_check": {}, "gen_fails": {},
    }
    for k, name in SETS.items():
        for suf in ("jsonl", "sidecar.jsonl", "relations.jsonl"):
            p = OUT / f"{name}.{suf}"
            if p.exists():
                man["files"][p.name] = {"sha256": sha(p), "lines": sum(1 for _ in open(p)), "bytes": p.stat().st_size}
        rp = OUT / f"{name}.relations.jsonl"
        if rp.exists():
            rel = jl(rp)
            man.setdefault("relations", {})[rp.name] = {
                "count": len(rel), "sha256": sha(rp),
                "by_type": dict(collections.Counter(r.get("type") for r in rel))}
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        rows, side = jl(p), jl(OUT / f"{name}.sidecar.jsonl")
        man["sets"][k] = coverage(rows, side)
        man["gates"][k] = jload(LOGS / f"gates_{k}.json")
        g4 = jload(LOGS / f"g4_{k}.json")
        if g4:
            man["g4"][k] = {"rows_tested": g4["rows_tested"], "n_fail": g4["n_fail"],
                            "relations": g4["relations"], "non_pass_reasons": g4["non_pass_reasons"]}
        q = jload(LOGS / f"quota_{k}.json")
        if q:
            man["quota"][k] = q
        fz = jload(LOGS / f"finalize_{k}.log")
        if fz:
            man["gen_fails"][k] = fz
        for suf in ("jsonl", "sidecar.jsonl", "relations.jsonl"):
            s = jload(OUT.parent / "logs" / f"sealed_{name}.{suf}.summary.json")
            if s:
                man["sealed_check"][f"{name}.{suf}"] = {kk: s.get(kk) for kk in
                                                        ("checker_version", "suite_sha256", "rows", "rows_hit",
                                                         "rows_clean", "rows_report_only", "parse_errors")}
                man["sealed_check"][f"{name}.{suf}"]["input_sha256_matches_file"] = \
                    s.get("input_sha256") == sha(OUT / f"{name}.{suf}")
                man["sealed_check"][f"{name}.{suf}"]["blocking_kinds_hit"] = \
                    {k: v["rows"] for k, v in s.get("kinds", {}).items() if v.get("blocking") and v.get("rows")}
                man["sealed_check"][f"{name}.{suf}"]["report_only_kinds"] = \
                    {k: v["rows"] for k, v in s.get("kinds", {}).items() if not v.get("blocking") and v.get("rows")}
    cs = LEAN / "c_src"
    par = [("pack", "c_src/packs/packs-1/packs.jsonl"), ("pack", "c_src/packs/packs-2/packs.jsonl"),
           ("pack", "c_src/packs/packs-3/packs-3.jsonl"), ("pack", "c_src/packs/packs-4/packs.jsonl"),
           ("format_set", "c_src/formats/formats-1/MANIFEST.json"),
           ("format_set", "c_src/formats/formats-1/data/registers.jsonl"),
           ("wording_set", "c_src/formats/formats-2/wordings/family_pools.jsonl"),
           ("word_list", "c_src/F4/gen/words_web2.txt")]
    man["parents"] = [{"kind": k, "path": r, "sha256": sha(LEAN / r)} for k, r in par if (LEAN / r).exists()]
    man["parents"].append({"kind": "real_text_dataset", "path": "gd_onet_occupation (O*NET occupation titles, CC BY 4.0)",
                           "via": "packs-1..4 persona_seed", "sha256": None})
    man["parents_note"] = ("words_web2.txt = macOS /usr/share/dict/web2 (Webster's Second International, public "
                           "domain), used only to screen invented pack terms against real English words")
    man["notes"] = [
        "Training pools (cand, qc): S1-S4 only, formats-1 training styles only (fmt1 refuse_held_out clean); S5 and "
        "the held-out styles appear only in mixdev_S5. F14 is never trained or posed.",
        "G3 / G15 run on every row at generation (rows that fail are redrawn; counts in gen_fails) and again on the "
        "written files (gates). G18 does not apply (no ordinal rows).",
        "G4 uses a seeded random property driver: Hypothesis is not installed in the project venv (no installs made).",
        "Sidecar and relations sit next to each row file in out/ (spec 2.4 names data/c_parts/; that path is outside "
        "this builder's allow-list, so the mixer copies them).",
        "difficulty_bin and crowd_pg are null: the G9 crowd pass is a later step.",
        "O*NET (CC BY 4.0, gd_onet_occupation) is the persona-seed parent; credit belongs in the notices file.",
    ]
    with open(OUT / "MANIFEST.json", "w") as f:
        json.dump(man, f, indent=1, default=str)
    print(json.dumps({"files": {k: v["lines"] for k, v in man["files"].items()}}, indent=1))


if __name__ == "__main__":
    main()
