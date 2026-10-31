"""Write out/MANIFEST.json (files, counts, sha256, relation counts/sha, parents, held-out groups, deviations, pending
orchestrator items), out/notices_commits.json (G1: one entry per repo used) and qc/QC_REPORT.json (gate results from
qc/gates_summary.json + tmp/sealed/hits.json, pool sha256s, candidates/relation sha256s)."""
from __future__ import annotations

import collections
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen"))
import common as C  # noqa: E402

FILES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}


def sha(p: Path) -> str | None:
    if not p.exists():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read(p: Path):
    return [json.loads(l) for l in open(p)] if p.exists() else []


PARENTS = [
    {"name": "CommitChronicle", "id": "JetBrains-Research/commit-chronicle", "kind": "real_text_dataset",
     "licence": "per-repo permissive licences (compilation record kept per row)",
     "parents": ["public GitHub repositories (each repo name checked against the deny-list)"]},
    {"name": "CommitPackFT", "id": "bigcode/commitpackft", "kind": "real_text_dataset",
     "licence": "per-repo permissive licences (dataset `license` field kept per row)",
     "parents": ["CommitPack (bigcode/commitpack)", "public GitHub repositories (each repo name checked)"]},
    {"name": "O*NET occupation titles (persona seeds)", "id": "gd_onet_occupation", "kind": "persona_seed",
     "class": "no_new_rows", "via": ["c_src/packs/packs-1", "c_src/packs/packs-2", "c_src/packs/packs-4"]},
    {"name": "packs", "id": "c_src/packs/packs-{1,2,4}/packs.jsonl", "kind": "pack"},
    {"name": "formats-1", "id": "c_src/formats/formats-1 (fmt1 styles, render_row_text, loader_check)",
     "kind": "format_codebook"},
    {"name": "formats-2", "id": "c_src/formats/formats-2/wordings/family_pools.jsonl (COMMIT pools)",
     "kind": "wording_set"},
    {"name": "COMMIT lexicon", "id": "c_src/COMMIT/gen/lexicon.json + gen/lex2.py (program lists, area/type defs)",
     "kind": "codebook"},
    {"name": "common tools", "id": "c_src/common (negcount.py, markers.json, denylist.py)", "kind": "tool"},
]

DEVIATIONS = [
    "GT1L / GT4 / GT6 gate rule templates not built (GT1/GT2/GT3/GT5 only).",
    "Renames, binary and mode-only files excluded from every row (SEM-05/SEM-07 inactive, left off cards).",
    "Pool size caps: <= 400 records per repo group; files <= 5,000 lines; CommitPackFT triage-eligible groups: none "
    "(triage is CommitChronicle only, X10).",
    "No short card forms, no definition examples or few-shot cards for route/triage/match in this build; gate few-shot "
    "flag only as set in gate.build_cards.",
    "Score and triage samplers are label-first in practice; inverted gate distractors size-matched by file count only.",
    "rho fixed at 0.68 for gate and match polarity frames.",
    "Route area token sets (nearest-area option fill, symmetric dominance filter) are built from the group's pooled "
    "commits' paths, not the dated tree proxy at each commit; area non-emptiness at the commit is not re-checked.",
    "Route view shows a bare '@@' line between two hunks of one file (no line numbers, no context text) so that each "
    "shown hunk is separable for the G3 substring check.",
    "Route S5 dev cards use the list card form (no tree rendering of the area list).",
    "Route one card = one repo group (the area list is per group); domain_pack = card id + group.",
    "Top-up rounds: when a card's units go unfilled (e.g. message-only supply), the builder draws extra diff-view "
    "units on the same cards to reach the per-type candidate count.",
    "Yes/no rows whose question is negated (k_syn odd), double-negated or in an inverted frame (gate 'merge without "
    "review', match 'written for a different change') draw only formats-2 wordings without a question mark: a polar "
    "wording question there would ask the opposite thing (found by G2 on qc row CMM016; checked in run_gates).",
    "mixdev_S5 is cut to 80 rows per type by whole units in emission order (400 items).",
]

REPAIRS = [
    "fixA G2 pass 1 (6 Oct): solver B found 112/15,082 route mismatches on monorepo-shift cards (CMR007/015/018/022): "
    "the card said 'Every area below is a folder inside the folder P' but 2.1 areas include other top-level folders. "
    "Generator fix (gen/route.py folder_path + shifted-card sentence 'Most of this project's files are inside the "
    "folder P. Each folder below is given from the project root.'); definitions print folders from the project root. "
    "Full rebuild, same seeds: only the 491 shifted-card route rows changed text (303 cand, 188 qc); solver B 0/15,082. "
    "Note: tmp/repair/g2fix1/NOTE.md.",
]

PENDING = [
    "X9 rows per card, X12 card forms, X15 card distinctness: no recorded ruling; built under the spec's default plan.",
    "X13 route message-only name-hit quota: the eligible pool gives far fewer message-only route rows than 30% "
    "(see build_report mo_* counts); the slice is not frozen before the ruling.",
    "Gate message-only GT2 supply ~0 (spec 5.5 fallback: GT2 cards leave the slice).",
    "QC message-only minimums (>= 334 per route/triage/gate in qc_sample) not met for route (supply).",
    "G8 / G5 / G6 / G7 / G9 / G10 run in later steps (not part of gen:COMMIT).",
]


def main():
    out = {"family": "COMMIT", "spec_id": C.SPEC_ID, "g0_sha256": json.load(open(C.FAM / "G0_FROZEN.json"))["sha256"],
           "gen_version": C.GEN_VERSION, "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "files": {}, "relations": {}, "parents": PARENTS, "deviations": DEVIATIONS, "repairs": REPAIRS,
           "pending_orchestrator": PENDING}
    repos = {}
    all_rows = {}
    for s, nm in FILES.items():
        p = C.OUT / f"{nm}.jsonl"
        rows = read(p)
        all_rows[s] = rows
        side = C.OUT / f"{nm}.sidecar.jsonl"
        out["files"][nm] = {
            "path": f"out/{nm}.jsonl", "rows": len(rows), "sha256": sha(p), "sidecar_sha256": sha(side),
            "by_type": dict(collections.Counter(r["source"] for r in rows)),
            "by_view": dict(collections.Counter(r["meta"]["input_view"] for r in rows)),
            "by_qtype": dict(collections.Counter(r["qtype"] for r in rows)),
            "cards": len({r["meta"]["card_id"] for r in rows}),
            "domain_packs": len({r["meta"]["domain_pack"] for r in rows}),
            "persona_rows": sum(1 for r in rows if r["meta"].get("persona_seed")),
            "format_styles": len({r["meta"]["format_style"] for r in rows})}
        rp = C.OUT / f"{nm}.rel.jsonl"
        if rp.exists():
            rels = read(rp)
            out["relations"][nm] = {"path": f"out/{nm}.rel.jsonl", "n": len(rels), "sha256": sha(rp),
                                    "by_type": dict(collections.Counter(x["type"] for x in rels))}
        for x in read(side):
            for e in x.get("extra_records", []):
                repos.setdefault(e["repo"], e["repo_licence"])
    # repos of base records
    sys.path.insert(0, str(C.HERE))
    import frame as FR
    for rows in all_rows.values():
        for r in rows:
            rec = FR.rec(r["meta"]["text_source"]["record_id"])
            repos.setdefault(rec["repo"], rec["licence"])
    notices = [{"repo": k, "licence": v, "needs_notice_text": "apache" in str(v).lower()} for k, v in sorted(repos.items())]
    with open(C.OUT / "notices_commits.json", "w") as f:
        json.dump(notices, f, indent=0)
    g = json.load(open(C.DATA / "groups.json"))
    out["held_out_repo_groups"] = g["heldout"]
    out["repos_used"] = len(repos)
    out["apache_repos"] = sum(1 for n in notices if n["needs_notice_text"])
    br = C.OUT / "build_report.json"
    if br.exists():
        b = json.load(open(br))
        out["build"] = {"counts": b.get("counts"), "lengths": b.get("lengths"), "drops": b.get("drops"),
                        "seconds": b.get("seconds")}
    with open(C.OUT / "MANIFEST.json", "w") as f:
        json.dump(out, f, indent=1)
    # QC report
    gs = json.load(open(HERE / "gates_summary.json")) if (HERE / "gates_summary.json").exists() else {}
    sealed = json.load(open(C.TMP / "sealed" / "hits.json")) if (C.TMP / "sealed" / "hits.json").exists() else {}
    qr = {"family": "COMMIT", "utc": out["built_utc"],
          "candidates_r1_sha256": out["files"]["candidates_r1"]["sha256"],
          "relation_file": "out/candidates_r1.rel.jsonl",
          "relation_sha256": out["relations"].get("candidates_r1", {}).get("sha256"),
          "pool_sha256": {"gen/data/pool.jsonl.gz": sha(C.DATA / "pool.jsonl.gz"),
                          "gen/data/groups.json": sha(C.DATA / "groups.json"),
                          "gen/lexicon.json": sha(C.HERE / "lexicon.json")},
          "file_sha256": {nm: v["sha256"] for nm, v in out["files"].items()},
          "gates": {}, "sealed_check": {k: {kk: vv for kk, vv in v.items() if kk != "blocking_ids"}
                                         for k, v in sealed.items()}}
    for s in FILES:
        if s in gs:
            x = gs[s]
            qr["gates"][s] = {"rows": x["rows"], "pass": x["pass"], "fail": x["fail"], "G2G3": x["G2G3"],
                              "negation": x["negation"], "check_rows": x["check_rows"],
                              "counted_len": x["counted_len"], "max_unit_rows": x["max_unit_rows"],
                              "G18": x["G18"], "G4": {t: {k: v for k, v in y.items() if k != "detail"}
                                                      for t, y in x.get("G4", {}).items()}}
    qr["cross"] = gs.get("cross")
    qr["repairs"] = REPAIRS
    mb = HERE.parent / "solverB" / "mismatch.json"
    if mb.exists():
        m = json.load(open(mb))
        qr["G2_solverB"] = {k: m.get(k) for k in ("solver", "solver_sha256", "spec", "inputs", "utc", "rows_checked",
                                                 "mismatches_n", "parse_fail_n", "eligibility_flag_n", "by_type",
                                                 "mismatch_by_card")}
        qr["G2_solverB"]["inputs_match_files"] = all(qr["file_sha256"].get(k) == v for k, v in m["inputs"].items())
    with open(HERE / "QC_REPORT.json", "w") as f:
        json.dump(qr, f, indent=1)
    print("MANIFEST", {nm: v["rows"] for nm, v in out["files"].items()}, "repos", len(repos))


if __name__ == "__main__":
    main()
