"""F7 finalize: held-out guard, sealed_check on every output (and replacement of any blocking hit), gates, G4 summary
and out/MANIFEST.json. Counts only (no row text) in every log.

  python f7finalize.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f7build as B  # noqa: E402
import f7case as CS  # noqa: E402
import f7cards as CD  # noqa: E402
import f7lex as LX  # noqa: E402
import f7main as MN  # noqa: E402
import f7model as M  # noqa: E402
import f7packs as PK  # noqa: E402
from fmt1 import pool  # noqa: E402

LEAN = B.LEAN
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
SEALED = LEAN / "sealed_nd/qc/sealed_check.py"
FILES = {"candidates": "candidates_r1", "qc": "qc_sample", "mixdev": "mixdev_S5"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_jsonl(p: Path) -> list:
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def sealed(path: Path) -> dict:
    out = path.with_suffix(".sealedqc.jsonl")
    summ = path.with_suffix(".sealedqc.summary.json")
    subprocess.run([PY, str(SEALED), str(path), "--out", str(out), "--summary", str(summ), "--structure-fields",
                    "state,card,instructions,options", "--skip-fields", "meta", "--workers", "4"],
                   check=True, capture_output=True)
    s = json.load(open(summ))
    hits = [json.loads(l)["id"] for l in open(out) if json.loads(l).get("hit")]
    return {"rows": s["rows"], "rows_hit": s["rows_hit"], "rows_report_only": s["rows_report_only"],
            "kinds_blocking_rows": {k: v["rows"] for k, v in s["kinds"].items() if v["blocking"] and v["rows"]},
            "keyword_soft_rows": s["kinds"].get("keyword_soft", {}).get("rows"), "hit_ids": hits,
            "checker_sha256": s["checker_sha256"], "suite_sha256": s["suite_sha256"]}


def replace_hits(kind: str, hit_ids: list) -> int:
    """Regenerate every unit (group_id) that holds a blocking hit, on the same card, with a fresh row stream."""
    name = FILES[kind]
    path = B.OUT / f"{name}.jsonl"
    rows = read_jsonl(path)
    rels = read_jsonl(B.OUT / f"{name}.relations.jsonl")
    bad_groups = {r["group_id"] for r in rows if r["id"] in set(hit_ids)}
    if not bad_groups:
        return 0
    by_card = collections.defaultdict(list)
    for r in rows:
        if r["group_id"] in bad_groups:
            by_card[r["meta"]["card_id"]].append(r)
    packs = list(PK.training_packs()) if kind != "mixdev" else list(PK.heldout_packs())
    if kind == "mixdev":
        plans = CD.s5_plan(packs, B.SEED, n_cards=10)
    else:  # r2: the same plans as the build (f7main.train_plans: R1B card counts, packs-3 S6 cards, qc row target)
        packs, plans = MN.train_plans(kind)
    report = {"card_attempts": {}, "card_fail_reasons": collections.Counter(), "row_fail_reasons": collections.Counter(),
              "unit_fail": collections.Counter(), "flip_fallback": 0}
    new_rows, new_rels = [], []
    for cid, rs in by_card.items():
        plan = next(p for p in plans if p["card_id"] == cid)
        card, fs, used = MN.setup_card(plan, kind == "mixdev", report)
        used |= {r["meta"]["case_features"].get("subject") for r in rows if False}
        n = len(rs)
        rr, rl = MN.card_rows(card, plan, fs, used, max(n, 2 * card["K"]), 0, report,
                              "dev" if kind == "mixdev" else ("train" if kind == "candidates" else "qc"))
        # keep the same per-level counts as the dropped rows
        want = collections.Counter(r["gold"] for r in rs)
        keep = []
        for r in rr:
            if want[r["gold"]] > 0 and r["meta"]["twin_kind"] is None:
                want[r["gold"]] -= 1
                r["id"] = r["id"].replace(cid, cid + "-rep")
                r["group_id"] = r["group_id"].replace(cid, cid + "-rep")
                r["call_id"] = r["call_id"].replace(cid, cid + "-rep")
                keep.append(r)
        new_rows += keep
    rows = [r for r in rows if r["group_id"] not in bad_groups] + [MN.strip_private(r) for r in new_rows]
    ids = {r["id"] for r in rows}
    rels = [x for x in rels if x["a"] in ids and x["b"] in ids]
    MN.write_jsonl(path, rows)
    MN.write_jsonl(B.OUT / f"{name}.relations.jsonl", rels)
    return len(bad_groups)


def main():
    t0 = time.time()
    man = {"family": "F7", "builder": "F7 generator (c_src/F7/gen)", "gen_version": LX.GEN_VERSION,
           "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "seed": B.SEED, "git_sha": B.GIT_SHA}
    man["binding"] = {
        "PREREG_FINAL.md": sha(LEAN / "PREREG_FINAL.md"), "A15_suite_sha256": "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68",
        "C_DATA_SPEC.md": sha(LEAN / "c_spec/C_DATA_SPEC.md"), "C_TRAIN_RECIPE.md": sha(LEAN / "c_spec/C_TRAIN_RECIPE.md"),
        "F7_G0_SPEC.md": sha(LEAN / "c_src/F7/G0_SPEC.md"), "F7_G0_frozen_sha256": LX.SPEC_SHA256}
    man["tools"] = {"decoder_io.py": sha(LEAN / "decoder_io.py"), "train_decoder.py": sha(LEAN / "train_decoder.py"),
                    "negcount.py": sha(LEAN / "c_src/common/negcount.py"),
                    "fmt1/card.py": sha(LEAN / "c_src/formats/formats-1/fmt1/card.py"),
                    "formats-1 MANIFEST": sha(LEAN / "c_src/formats/formats-1/MANIFEST.json"),
                    "formats-2 wordings": sha(LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl"),
                    "packs-2": sha(LEAN / "c_src/packs/packs-2/packs.jsonl"),
                    "packs-3": sha(LEAN / "c_src/packs/packs-3/packs-3.jsonl"),
                    "sealed_check.py": sha(SEALED)}
    man["generator_files"] = {p.name: sha(p) for p in sorted(HERE.glob("*.py"))}
    # held-out guard on training files; dev file uses held-out styles only
    guard = {}
    for kind in ("candidates", "qc"):
        rows = read_jsonl(B.OUT / f"{FILES[kind]}.jsonl")
        try:
            guard[kind] = pool.refuse_held_out(rows, strict_unknown=True)
        except pool.HeldOutStyleError as e:
            guard[kind] = {"refused": str(e)[:200]}
    dev = read_jsonl(B.OUT / f"{FILES['mixdev']}.jsonl")
    guard["mixdev_all_held_out_styles"] = all(pool.style(r["meta"]["format_style"])["held_out"] for r in dev)
    guard["mixdev_sampler_S5_only"] = all(r["meta"]["sampler"] == "S5" for r in dev)
    tp = {p["id"] for p in PK.training_packs()}
    guard["mixdev_packs_disjoint_from_training_packs"] = all(r["meta"]["domain_pack"] not in tp for r in dev)
    man["held_out_guard"] = guard
    # sealed check (replace blocking hits, then re-check)
    sc = {}
    for kind, name in FILES.items():
        p = B.OUT / f"{name}.jsonl"
        s = sealed(p)
        rounds = 0
        while s["rows_hit"] and rounds < 3:
            replace_hits(kind, s["hit_ids"])
            s = sealed(p)
            rounds += 1
        s["replacement_rounds"] = rounds
        s.pop("hit_ids", None)
        sc[name] = s
    for name in FILES.values():
        cp = B.OUT / f"{name}.cards.jsonl"
        s = sealed(cp)
        s.pop("hit_ids", None)
        sc[f"{name}.cards"] = s
    man["sealed_check"] = sc
    # gates
    gates = {}
    for kind, name in FILES.items():
        p = B.OUT / f"{name}.jsonl"
        out = B.OUT / f"gates_{name}.json"
        subprocess.run([PY, str(HERE / "f7gates.py"), str(p), "--relations", str(B.OUT / f"{name}.relations.jsonl"),
                        "--out", str(out)], check=True, capture_output=True)
        gates[name] = json.load(open(out))
    man["gates"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("by_sampler", "median_tokens_by_sampler_defs")}
                    for k, v in gates.items()}
    man["gates_by_sampler"] = {k: v.get("by_sampler") for k, v in gates.items()}
    g4p = B.OUT / "G4_metamorphic.json"
    man["G4"] = json.load(open(g4p)) if g4p.exists() else None
    # files, counts, coverage
    files = {}
    for kind, name in FILES.items():
        for suf in (".jsonl", ".relations.jsonl", ".cards.jsonl"):
            p = B.OUT / f"{name}{suf}"
            if p.exists():
                files[p.name] = {"sha256": sha(p), "lines": sum(1 for _ in open(p))}
    man["files"] = files
    # MIXER_NOTE (6 Oct): parents (spec 3.H / G1) and relation counts / sha of the training relation file
    man["parents"] = [
        {"name": "packs-2 domain packs (training cards)", "path": "lean/c_src/packs/packs-2/packs.jsonl",
         "sha256": sha(LEAN / "c_src/packs/packs-2/packs.jsonl")},
        {"name": "packs-3 domain packs (S5 held-out packs, mixdev only)", "path": "lean/c_src/packs/packs-3/packs-3.jsonl",
         "sha256": sha(LEAN / "c_src/packs/packs-3/packs-3.jsonl")},
        {"name": "formats-1 format style pool and label tools (fmt1)", "path": "lean/c_src/formats/formats-1/MANIFEST.json",
         "sha256": sha(LEAN / "c_src/formats/formats-1/MANIFEST.json")},
        {"name": "formats-2 instruction wording pool (F7 families)",
         "path": "lean/c_src/formats/formats-2/wordings/family_pools.jsonl",
         "sha256": sha(LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl")},
        {"name": "O*NET 31.0 Database occupation titles (persona seeds inside the packs)", "alias": "gd_onet_occupation",
         "deny_class": "no_new_rows (persona-seed parent passes)"}]
    rel = {}
    for kind, name in FILES.items():
        p = B.OUT / f"{name}.relations.jsonl"
        if p.exists():
            rr = read_jsonl(p)
            rel[name] = {"path": f"out/{p.name}", "sha256": sha(p), "count": len(rr),
                         "by_type": dict(collections.Counter(x["type"] for x in rr))}
    man["relations"] = rel
    cov = {}
    for kind, name in FILES.items():
        rows = read_jsonl(B.OUT / f"{name}.jsonl")
        cov[name] = {
            "rows": len(rows),
            "rows_by_sampler": dict(collections.Counter(r["meta"]["sampler"] for r in rows)),
            "cards": len({r["meta"]["card_id"] for r in rows}),
            "cards_by_sampler": {s: len({r["meta"]["card_id"] for r in rows if r["meta"]["sampler"] == s})
                                 for s in sorted({r["meta"]["sampler"] for r in rows})},
            "packs": len({r["meta"]["domain_pack"] for r in rows}),
            "pack_ids": sorted({r["meta"]["domain_pack"] for r in rows}),
            "persona_seeds": len({r["meta"]["persona_seed"] for r in rows if r["meta"]["persona_seed"]}),
            "format_styles": len({r["meta"]["format_style"] for r in rows}),
            "skins": len({pool.style(r["meta"]["format_style"])["skin"] for r in rows}),
            "containers": dict(collections.Counter(r["meta"]["container"] for r in rows)),
            "wording_ids": len({r["meta"]["wording_id"] for r in rows}),
            "wording_families": sorted({r["meta"]["wording_id"].split(".wd.")[0] for r in rows}),
            "K": dict(collections.Counter(r["meta"]["K"] for r in rows)),
            "modes": dict(collections.Counter(r["meta"]["mode"] for r in rows)),
            "defs_styles": dict(collections.Counter(r["meta"]["defs_style"] for r in rows)),
            "label_forms": dict(collections.Counter(r["meta"]["label_form"] for r in rows)),
            "twin_kinds": dict(collections.Counter(str(r["meta"]["twin_kind"]) for r in rows)),
            "deep_rows": sum(1 for r in rows if r["meta"]["deep"]),
            "inverted_cards": 0,
            "option_buckets": {"2-4": sum(1 for r in rows if len(r["options"]) <= 4),
                               "5-9": sum(1 for r in rows if 5 <= len(r["options"]) <= 9)},
        }
    man["coverage"] = cov
    rep = {}
    for name in FILES.values():
        p = B.TMP / f"report_{name}.json"
        if p.exists():
            rep[name] = json.load(open(p))
            rep[name].pop("card_attempts", None)
    man["build_reports"] = rep
    json.dump(man, open(B.OUT / "MANIFEST.json", "w"), indent=1, default=str)
    B.log(f"finalize: MANIFEST written, {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
