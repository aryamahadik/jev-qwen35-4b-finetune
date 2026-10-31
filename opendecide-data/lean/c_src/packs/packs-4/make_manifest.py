#!/usr/bin/env python3
"""packs-4: write manifest.json (counts, licences, parents, sha256 of every input and output; no pack text)."""
import collections
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
# O*NET licence record re-read by this builder in fix round 1 (same sha as the reviewer's read)
ONET_RECORD_SHA = "7e9d1d0185578cb8f6119afc69efa909904ed2e55727a7772d0cbe03febf53e6"
ONET_RECORD_READ_UTC = "2026-10-03T21:58:12Z"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rel(p: Path) -> str:
    return str(p.relative_to(LEAN.parent.parent)) if str(p).startswith(str(LEAN.parent.parent)) else str(p)


def main():
    packs = [json.loads(l) for l in (HERE / "packs.jsonl").read_text().splitlines() if l.strip()]
    draw = json.loads((HERE / "persona_draw.json").read_text())
    qc = json.loads((HERE / "tmp" / "qc_report.json").read_text())
    dv = json.loads((HERE / "denylist_verdicts_packs4.json").read_text())
    sc = {}
    for name, f in (("packs.jsonl", "sc_packs"), ("packs.jsonl (--keys all)", "sc_packs_keysall"),
                    ("packs_index.jsonl", "sc_packs_index"),
                    ("persona_draw.json (draws as rows)", "sc_persona_draw_rows")):
        s = json.loads((HERE / "tmp" / f"{f}.summary.json").read_text())
        sc[name] = {"input_sha256": s["input_sha256"], "rows": s["rows"], "rows_hit_blocking": s["rows_hit"],
                    "rows_report_only": s["rows_report_only"],
                    "report_only_kinds": {k: v["rows"] for k, v in s["kinds"].items() if v["rows"] and not v["blocking"]},
                    "blocking_kinds_hit": {k: v["rows"] for k, v in s["kinds"].items() if v["rows"] and v["blocking"]}}
        sc["_checker"] = {"path": "lean/sealed_nd/qc/sealed_check.py", "sha256": s["checker_sha256"],
                          "version": s["checker_version"], "suite_sha256": s["suite_sha256"],
                          "run_as": "program only (id/kind counts read; exports never opened)"}
    sections = ["roles", "entity_types", "items", "documents", "units", "quantities", "bool_fields", "cat_fields",
                "statuses", "outcomes", "predicates", "links", "actions", "risk_events", "taxonomy_dims", "jargon",
                "neg_affix_pairs", "inert_facts"]
    man = {
        "id": "packs-4.manifest",
        "builder": "packs-4 (domain-pack agent, C_DATA_SPEC v4 section 11 step 3; quarter: invented and fictional settings)",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plan": {"prereg": "PREREG_FINAL.md A15 (sealed suite f4ae8637...) and A16 (C round-1 plan)",
                 "spec": "c_spec/C_DATA_SPEC.md v4 (2.1 domain packs, F4 persona seeds, 3.H, 7.2)",
                 "spec_sha256": sha(LEAN / "c_spec" / "C_DATA_SPEC.md"),
                 "recipe_sha256": sha(LEAN / "c_spec" / "C_TRAIN_RECIPE.md")},
        "outputs": {
            "packs.jsonl": {"sha256": sha(HERE / "packs.jsonl"), "packs": len(packs), "schema": "c_pack.v1",
                            "objects_with_id": qc["objects_with_id"], "duplicate_ids": qc["duplicate_ids"]},
            "packs_index.jsonl": {"sha256": sha(HERE / "packs_index.jsonl"), "rows": len(packs)},
            "persona_draw.json": {"sha256": sha(HERE / "persona_draw.json"), "draws": len(draw["draws"])},
            "denylist_query_packs4.json": {"sha256": sha(HERE / "denylist_query_packs4.json")},
            "denylist_verdicts_packs4.json": {"sha256": sha(HERE / "denylist_verdicts_packs4.json")},
        },
        "code": {f.name: sha(f) for f in sorted(HERE.glob("*.py"))},
        "authoring_sources": {f"src/{f.name}": sha(f) for f in sorted((HERE / "src").glob("batch_*.py"))},
        "counts": {
            "packs": len(packs),
            "themes": dict(collections.Counter(p["theme"] for p in packs)),
            "onet_major_groups": len({p["persona"]["major_group"] for p in packs}),
            "distinct_persona_seeds": len({p["persona_seed"] for p in packs}),
            "split_hint": dict(collections.Counter(p["split_hint"] for p in packs)),
            "section_totals": {s: sum(len(p[s]) for p in packs) for s in sections},
            "people_names": sum(len(p["names"]["people"]) for p in packs),
            "date_windows_within": [min(p["date_window"]["start"] for p in packs), max(p["date_window"]["end"] for p in packs)],
        },
        "licence": {
            "packs": packs[0]["licence"],
            "row_licence_for_families": "CC0 1.0 (program-generated) (C_DATA_SPEC 2.4); persona_seed recorded in meta",
            "third_party": [{"name": "O*NET 31.0 Database, occupation_data.csv (titles only)",
                             "licence": "CC BY 4.0", "record": "https://www.onetcenter.org/license_db.html",
                             "url": draw["source_url"], "sha256": draw["source_sha256"],
                             "use": "persona seed titles, drawn by program (draw_personas.py, seed string "
                                    f"'{draw['seed_string']}', round-robin over {qc['major_groups']} major groups); "
                                    "descriptions never read; raw file deleted after the draw (re-download by URL)",
                             "notice_form": "modified (the record's form 'If you make edits or additions to O*NET "
                                            "information'; fix round 1, review of 3 Oct)",
                             "record_read": {"url": "https://www.onetcenter.org/license_db.html",
                                             "sha256": ONET_RECORD_SHA, "read_utc": ONET_RECORD_READ_UTC},
                             "notice": "This product includes information from the O*NET 31.0 Database by the U.S. "
                                       "Department of Labor, Employment and Training Administration (USDOL/ETA). Used "
                                       "under the CC BY 4.0 license. O*NET\u00ae is a trademark of USDOL/ETA. The "
                                       "OpenDecide project has modified all or some of this information. USDOL/ETA "
                                       "has not approved, endorsed, or tested these modifications.",
                             "changes": "Only main occupation titles (occupation_data.csv, Title column) were used, as "
                                        "persona seeds. Each pack keeps the title verbatim in persona.onet_title with its "
                                        "O*NET-SOC code in persona_seed, and adds an invented deciding role written "
                                        "from it (persona.deciding_role) inside an invented setting. No O*NET "
                                        "description, task, alternate title or other field is used; the list of "
                                        "changes is this manifest and packs_index.jsonl (code, title, deciding role "
                                        "per pack)."},
                            {"name": "/usr/share/dict/web2 (Webster's Second International, 1934; public domain)",
                             "use": "filter-only: rejects jargon candidates that are dictionary words; never emitted",
                             "sha256": sha(Path("/usr/share/dict/web2"))}],
            "personahub": "never used",
        },
        "parents": {"declared": packs[0]["parents"],
                    "denylist_run": {"program": "c_src/common/denylist.py", "program_sha256": dv["program_sha256"],
                                     "aliases_sha256": dv["aliases_sha256"], "denylist_sha256": dv["denylist_sha256"],
                                     "canonical": dv["canonical"], "counts": dv["counts"],
                                     "verdicts": {k: {"verdict": v["verdict"], "class": v["class"]}
                                                  for k, v in dv["verdicts"].items()},
                                     "note": "O*NET hit is class no_new_rows (alternate-titles / SOC direct-match "
                                             "entry); persona seeds use main titles only and emit no O*NET rows, "
                                             "so it passes (C_DATA_SPEC 2.1 F4)"}},
        "sealed_check": sc,
        "lint": {"program": "build_packs.py", "result": "84/84 packs pass, 0 errors",
                 "checks": ["section minimums", "unique names and ids", "negcount k_all = 0 on every name-like string",
                            "negating-affix words only as declared neg_affix_pairs (never in names)",
                            "XF06 marker words and family-banned value words never a value",
                            "jargon: not a web2 word, no morphology hint, unique across packs",
                            "quantities on their step grid", "date windows inside 1901-2099",
                            "presupposition, predicate and link types resolve",
                            "negcount k_all = 0 on inert facts",
                            "(fix round 1) inert facts name no own-pack decision word: whole words with simple "
                            "inflections against statuses, outcomes, risk events, Boolean names and aliases, category "
                            "field names and all values, taxonomy dimension names and values, quantity names, jargon "
                            "terms and predicate phrases (entries >= 3 characters)",
                            "G11 ROUGE-L < 0.7: settings, and (fix round 1) all pairs of inert facts, unit definitions "
                            "and jargon definitions, under both word splits ([a-z]+ hyphen-kept and [a-z0-9']+)"]},
        "qc": {k: qc[k] for k in ("person_names_in_2plus_packs", "inert_facts_reusing_own_vocab",
                                   "inert_vocab_hit_kinds", "max_rouge_l_setting",
                                   "max_rouge_l_jargon_definition_cross_pack", "max_rouge_l_inert_fact_all_pairs",
                                   "inert_fact_pairs_rouge_l_ge_0.7", "max_rouge_l_unit_definition_all_pairs",
                                   "unit_definition_pairs_rouge_l_ge_0.7", "max_rouge_l_jargon_definition_all_pairs",
                                   "jargon_definition_pairs_rouge_l_ge_0.7")},
        "g11_cross_set": json.loads((HERE / "tmp" / "fix1" / "cross_set_g11.json").read_text()),
        "g15_smoke": json.loads((HERE / "tmp" / "fix1" / "g15_smoke.json").read_text()),
        "fix_round_1": {
            "trigger": "review of packs-4 (3 Oct, verdict ISSUES; c_build/tmp/review_packs4/)",
            "issues": ["inert facts reused their own pack's decision words (review: 67 of 504 in 42 packs; the old "
                       "qc_packs.py check covered only statuses, outcomes, Boolean fields and category values > 3 "
                       "letters)",
                       "G11 ROUGE-L >= 0.7 on 32 inert-fact pairs and 11 unit-definition pairs (cross-pack)",
                       "O*NET notice used the unmodified credit form"],
            "fixes": {"inert_facts_rewritten": 125, "unit_definitions_rewritten": 15, "packs_touched": 71,
                      "inert_reasons": {"own_vocab_exact_phrase": 68, "own_vocab_inflection_only": 40,
                                        "g11_pair_side": 17},
                      "unit_reasons": {"review_g11_pairs": 9, "g11_pairs_under_hyphen_kept_split": 3,
                                       "margin_below_0.7 (max now 0.667)": 3},
                      "lint": "the two checks above are now lint errors in build_packs.py (a failing pack is not "
                              "written); qc_packs.py uses the same functions",
                      "notice": "O*NET credit now uses the record's 'modified' form, with a changes note"},
            "unchanged": "every id, persona seed, theme, title, setting, name, vocabulary entry and count; only "
                         "inert_facts[].text and units[].definition changed; packs_index.jsonl is byte-identical "
                         "(now written by make_index.py)",
            "packs_jsonl_sha256_before": "7cfbd38e24f1092f5f288cc015ac8ed48fa172b539665cebb66f673b614afa42",
            "authoring_record": {"tmp/fix1/replacements.py": sha(HERE / "tmp" / "fix1" / "replacements.py"),
                                 "tmp/fix1/apply.py": sha(HERE / "tmp" / "fix1" / "apply.py")},
            "denylist_rerun": "verdicts identical to the first run (query sha unchanged)",
        },
        "replacements": ["p4-077: first version had 1 blocking sealed keyword hit (keyword_hard); the pack was "
                         "rewritten whole with a new setting (same id, same program-drawn persona seed) and re-checked: "
                         "0 hits. The hit was never bisected, so no sealed keyword was learned."],
        "not_done_here": ["counts-only 10/12-gram, MinHash and cosine decontamination against OHS-1/2/3, the sealed "
                          "exports, DI and JevBench (orchestrator, C_DATA_SPEC 7.2; Claude-written seeds included)",
                          "F10's own >= 300K 3-language word-list check of invented words",
                          "family-specific pack lints (F7 concept sets and disjointness review, F12 tool catalog, "
                          "F1 presupposition review) run by each generator per card",
                          "held-out pack choice (split_hint is only a hint)"],
    }
    (HERE / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
    print("manifest written:", man["outputs"]["packs.jsonl"])


if __name__ == "__main__":
    main()
