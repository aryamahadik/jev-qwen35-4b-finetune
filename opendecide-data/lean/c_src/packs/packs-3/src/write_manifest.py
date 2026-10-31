"""Write packs-3.manifest.json: counts, licences, parents, check results and sha256 of every output and source file.
No row or pack text is copied into the manifest. Usage (from packs-3/): python src/write_manifest.py"""
import datetime
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT.parents[2]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).resolve().relative_to(LEAN.parent.parent))


packs = [json.loads(l) for l in open(ROOT / "packs-3.jsonl")]
lint = json.load(open(ROOT / "packs-3.lint.json"))
sq = json.load(open(ROOT / "packs-3.sealedqc.summary.json"))
dv = json.load(open(ROOT / "denylist_verdicts_packs3.json"))
xq = json.load(open(ROOT / "cross_quarter_check.json"))
CANON_DENYLIST = LEAN / "c_build" / "denylist.json"
NOTICE = ("This dataset includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment "
          "and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET\u00ae is a trademark of "
          "USDOL/ETA. OpenDecide has modified all or some of this information. USDOL/ETA has not approved, endorsed, "
          "or tested these modifications.")
large = [p for p in packs if p["large_tool_set"]]
draws = json.load(open(ROOT / "src" / "persona_draws.json"))
fam = Counter(k for p in packs for k, v in p["family_ready"].items() if v)
outputs = ["packs-3.jsonl", "packs-3.lint.json", "packs-3.sealedqc.jsonl", "packs-3.sealedqc.summary.json",
           "denylist_query_packs3.json", "denylist_verdicts_packs3.json", "denylist_packs3.json",
           "persona_draws.sealedqc.summary.json", "seed_banks.sealedqc.summary.json", "cross_quarter_check.json"]
sources = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "src").rglob("*.py")) + ["src/persona_draws.json"]
m = {
    "id": "packs-3-manifest",
    "builder": "packs-3 (C_DATA_SPEC v4 section 11 step 3, domain-pack agent 3 of 4)",
    "quarter": "public sector and civic (municipal services, permits, transport authorities, parks, libraries, "
               "courts admin, standards bodies, procurement, civic records, civic programs)",
    "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "order_g14": "built after A15 (sealed suite sha f4ae8637...) and A16 (C plan) were committed",
    "schema": packs[0]["schema"],
    "counts": {
        "packs": len(packs),
        "packs_by_area": dict(Counter(p["area"] for p in packs)),
        "persona_major_groups": len({p["persona"]["major_group"] for p in packs}),
        "packs_by_major_group": dict(sorted(Counter(p["persona"]["major_group"] for p in packs).items())),
        "distinct_persona_codes": len({p["persona_seed"] for p in packs}),
        "heldout_hint_packs": sum(p["heldout_hint"] for p in packs),
        "large_tool_packs": sum(p["large_tool_set"] for p in packs),
        "tools_total": sum(len(p["tools"]) for p in packs),
        "tools_per_pack_min_max": [min(len(p["tools"]) for p in packs), max(len(p["tools"]) for p in packs)],
        "tools_per_pack_min_max_other": [min(len(p["tools"]) for p in packs if not p["large_tool_set"]),
                                         max(len(p["tools"]) for p in packs if not p["large_tool_set"])],
        "tools_per_large_pack": {p["id"]: len(p["tools"]) for p in large},
        "near_miss_clusters": {p["id"]: [{"capability": f"{c['capability']['action']} {c['capability']['object']}",
                                          "compact_members": c["n_compact_members"],
                                          "near_miss_supply_min": c["near_miss_supply_min"]}
                                         for c in p["tool_clusters"]] for p in large},
        "bool_label_words": sum(1 for p in packs for lw in p["label_words"] if isinstance(lw["value"], bool)),
        "entity_types_total": sum(len(p["entity_types"]) for p in packs),
        "fields_total": sum(len(e["fields"]) for p in packs for e in p["entity_types"]),
        "boolean_facts_total": sum(len(p["boolean_facts"]) for p in packs),
        "label_words_total": sum(len(p["label_words"]) for p in packs),
        "jargon_candidates_total": sum(len(p["jargon_candidates"]) for p in packs),
        "id_pool_sizes": "first entity type 64 IDs with 16 look-alike pairs (Damerau-Levenshtein 1, no I/L/O, no "
                         "confusable swaps); other entity types 24 IDs with 6 pairs",
        "family_ready_packs": dict(sorted(fam.items())),
        "lint_issues": sum(len(v["issues"]) for v in lint["per_pack"].values()),
        "setting_rouge_l_pairs_ge_0_5": len(lint["setting_rouge_l_ge_0.5"]),
    },
    "pack_fields": {
        "id / pack_id": "stable id pk3-<key>; tools carry <pack id>-tNN, boolean facts bNN",
        "setting, org, jurisdiction, decider_role, roles": "Claude-written, invented places and bodies",
        "persona_seed / persona": "O*NET 31.0 main occupation title code (who is deciding); title, major group, draw index",
        "money": "currency, places, decider side for F2 (pays | paid; must act | waits)",
        "entity_types": "name, plural, id_key, id_prefix, typed fields (int/dec/pct/amt with unit, places, draw range, "
                        "direction; enum <= 10 values; status values with good/bad/neutral polarity; date; bool; text)",
        "scope_dimension": "one dimension with 3-5 values (F12 scope, F13 scope dimension)",
        "document_types": "with current_is bad/not bad (F3)",
        "item_kind": "F3 plural item kind with holder roles and holding polarity",
        "boolean_facts": "event/state kind (F7 U02), presupposed fact id (F1 F1R4-A04), concept set (F7 U01)",
        "predicates, links, affixed_words": "F4 unary predicates with adverse pole and implicit cue; directional links "
                                            "(active/passive); F5 SEM-18 / F1 affixal pairs",
        "events, hypotheses, actions, consequences": "F8 polarity (adverse/favourable/neutral, protective), F10 consequences bad/not bad",
        "outcome_sets": ">= 2 distinct outcome sets (F1, F13 X7)",
        "label_words": ">= 12 familiar words with natural predicates over the pack's own fields (F10)",
        "jargon_candidates": "invented jargon (unique across packs-3)",
        "disjoint_fillers": "F7 disjointness list (8, unique across packs-3, no content word shared with the pack's rubric slots)",
        "level_names": "familiar ordered level names, usual rank = list order (F7)",
        "inert_fact_types": ">= 12 (F13 X7 >= 10)",
        "register, source_names": "F11 register prose and report kinds; F4 trusted/untrusted source names",
        "names": "program-made pools: 40 persons, 14 organisations, 14 places (pairwise edit distance >= 3)",
        "id_schemes": "per entity type: format, regex, fixed width, pool, look-alike pairs (F3, F13 SEM-31)",
        "tools, tool_clusters, param_lexicon": "F12 tool set derived by program from the lexicon (12-30 tools; on "
                                               "large_tool_set packs 30-60 tools with 2 near-miss clusters per F12 G0 "
                                               "R3-SC3: each cluster = one capability + >= 24 compact-profile tools, "
                                               "each one fit component (action, object, scope, precondition, role) or "
                                               "one needed parameter from the plain tool, tagged in member_components; "
                                               "near_miss_supply_min = members minus one possible fit per restricting "
                                               "group, >= 19); every param name maps to one entity type; no scope "
                                               "dimension is a param name",
        "family_ready": "program flags of which family pack needs the pack meets (each family still runs its own lint)",
        "heldout_hint": "10 packs (lowest sha256 rank of id) suggested for S5 / held-out use; the orchestrator decides",
    },
    "lints_applied": [
        "word slots: no connective, comparator word, time-lead word, number token, XF06 marker, F3 stem word, F3 "
        "mechanism stem, negcount entry or implicit-cue verb, affixal negation (F9-R2-13, F3 rule 5/R1-16/R3-07/R3-09, F1 R3-A08)",
        "boolean fact names: plus F7 U03 banned factor kinds",
        "phrase slots: negcount k_all = 0, no core negation, no implicit cue, no affixal negation",
        "ID prefixes: 2-4 letters, never I, L or O",
        "label words: field exists, threshold strictly inside the field range or value in the field's list; bool "
        "fields take a JSON boolean with == or != (never the string 'true')",
        "cross-pack: setting ROUGE-L < 0.5 for every pair (G11 asks < 0.7); title, jurisdiction, org and decider "
        "role ROUGE-L < 0.7 for every pair (lint issue otherwise); fillers and jargon unique",
        "cross-quarter (src/cross_quarter_check.py, read-only on packs-1/2/4 pack files): no exact jargon clash; "
        "setting / org / decider role / title ROUGE-L < 0.7 against the other quarters' matching fields",
        "F12_large flag = 30-60 tools, >= 2 clusters, each >= 24 compact one-component members and near-miss supply "
        ">= 19 (F12 G0 R3-SC3)",
    ],
    "licence": {
        "pack_content": "CC0 1.0 (Claude-written)",
        "persona_titles": "O*NET 31.0 Database, CC BY 4.0, titles only (main occupation titles)",
        "onet_record": "https://www.onetcenter.org/license_db.html (read 3 Oct 2026; page names the O*NET 31.0 Database "
                       "under CC BY 4.0)",
        "onet_record_page_sha256": "7e9d1d0185578cb8f6119afc69efa909904ed2e55727a7772d0cbe03febf53e6",
        "onet_source_file": "https://www.onetcenter.org/dl_files/database/db_31_0_csv/occupation_data.csv",
        "onet_source_sha256": draws["source_sha256"],
        "notices_credit": NOTICE,
        "notices_credit_form": "the 'If you make edits or additions to O*NET information' credit on "
                               "onetcenter.org/license_db.html (page sha256 above, re-read 3 Oct 2026), with "
                               "'This page' as 'This dataset' and the name filled as OpenDecide",
        "notices_changes": "Changes to O*NET information: only main occupation titles (occupation_data.csv) are used; "
                           "each pack takes one title as the seed of its invented deciding role and records the "
                           "O*NET code and title in persona_seed / persona; no other O*NET content is used. The "
                           "list of codes and titles used is src/persona_draws.json (draws 0-79).",
        "rows_licence_value": "CC0 1.0 (program-generated) per spec 2.4; meta.persona_seed carries the O*NET code",
    },
    "parents": [{"name": "O*NET 31.0 Database occupation titles", "alias": "gd_onet_occupation",
                 "deny_class": "no_new_rows (O*NET alternate titles / SOC direct match entry); persona-seed parent passes"}],
    "persona_draw": {"seed": draws["seed"], "rule": draws["rule"], "draws_made": len(draws["draws"]),
                     "draws_used": sorted(p["persona"]["draw"] for p in packs) == list(range(len(packs)))},
    "denylist_check": {"program_sha256": dv["program_sha256"], "aliases_sha256": dv["aliases_sha256"],
                       "denylist": dv["denylist"], "denylist_exists": (LEAN.parent / dv["denylist"]).exists(),
                       "denylist_sha256": dv["denylist_sha256"],
                       "canonical_denylist": str(CANON_DENYLIST.relative_to(LEAN.parent)),
                       "equals_canonical": sha(CANON_DENYLIST) == dv["denylist_sha256"],
                       "created_utc": dv["created_utc"], "query": "denylist_query_packs3.json",
                       "verdicts": "denylist_verdicts_packs3.json", "counts": dv["counts"],
                       "verdict_per_entry": {k: v["verdict"] for k, v in dv["verdicts"].items()}},
    "sealed_check": {"checker_sha256": sq["checker_sha256"], "suite_sha256": sq["suite_sha256"],
                     "packs": {"rows": sq["rows"], "rows_hit": sq["rows_hit"], "rows_report_only": sq["rows_report_only"]},
                     "input_sha256": sq["input_sha256"],
                     "keyword_soft_matches": sq["kinds"]["keyword_soft"]["matches"],
                     "also_checked": {
                         k: (lambda s: f"{s['rows']} rows, {s['rows_hit']} blocking hits, {s['rows_report_only']} "
                                       f"report-only (input sha256 {s['input_sha256'][:16]})")(
                             json.load(open(ROOT / f))) for k, f in (("persona_draws", "persona_draws.sealedqc.summary.json"),
                                                                    ("seed_banks", "seed_banks.sealedqc.summary.json"))},
                     "keys_all_rerun": "packs with --keys all: 80 rows, 0 blocking hits (report-only keyword_soft)",
                     "report_only_kind": "keyword_soft on every pack (report-only by the checker; not a blocking hit)"},
    "cross_quarter_check": {"output": "cross_quarter_check.json", "jargon_clashes": len(xq["jargon_clashes"]),
                            "seed_rouge_l_ge_0_7": len(xq["seed_rouge_l_ge_0_7"]),
                            "max_seed_rouge_l": xq["max_seed_rouge_l"],
                            "others_sha256": {k: v.get("sha256") for k, v in xq["others"].items()}},
    "review_fixes": [
        "1 bool label words: 10 values were the string 'true'; the parser now emits JSON booleans and the lint rejects "
        "a non-boolean value or an operator other than == / != on a bool field",
        "2 F12_large: clusters rebuilt to F12 G0 R3-SC3 (>= 24 compact one-component members, near-miss supply >= 19, "
        "30-60 tools); two-component members (other action AND other object) removed; the flag now tests the rule",
        "3 G11 seed ROUGE-L: 3 jurisdiction pairs at 0.75 fixed by renaming one city in each pair (Ellerholt, "
        "Torrinsby, Quillanmouth; org, setting and register follow); the lint now checks title, jurisdiction, org and "
        "decider role pairwise (< 0.7)",
        "4 cross-quarter jargon: 1 exact clash with packs-4 renamed; cross_quarter_check.py added (also found and fixed "
        "2 decider roles at ROUGE-L 0.8 against packs-1 / packs-2)",
        "5 O*NET notice: the 'modified' credit form from the O*NET licence page, plus a changes note",
        "6 deny-list verdict path: verdicts re-run against a kept deny-list file (denylist_packs3.json, sha256 equal "
        "to lean/c_build/denylist.json) instead of a deleted tmp file",
    ],
    "decontamination": "counts-only decontamination (spec 7.2, G13) of packs against dev/eval/OHS/sealed sets is run "
                       "by the orchestrator, not here",
    "outputs": {o: {"path": rel(ROOT / o), "sha256": sha(ROOT / o)} for o in outputs},
    "sources": {s: sha(ROOT / s) for s in sources},
    "raw_inputs_deleted": ["tmp/onet31_occupation_data.csv (sha256 above)", "tmp/onet_license_page.html (sha256 above)",
                           "tmp/fix/onet_license_page.html (re-read for the notice form, same sha256; deleted)"],
    "scratch_left_in_tmp": "tmp/ holds scratch copies only (test builds, JSONL views of persona draws and seed banks, "
                           "their sealed-check outputs; tmp/fix/ = review-fix backups of the pre-fix outputs and "
                           "sources, trial builds, the keys=all sealed check); nothing there is an output",
    "caveats": [
        "Each family's own pack lint still runs before a card uses a pack (F3 rule 5, F7 concept-set review by a "
        "second session, F9-R2-13, F12 near-miss supply, F13 X7); a pack that fails one family's lint is skipped by "
        "that family only.",
        "Tool sets are program-derived drafts from the pack lexicon; F12 may rebuild variants from param_lexicon.",
        "keyword_soft report-only flags appear on all 80 packs; no blocking sealed hit.",
        "near_miss_supply_min is a pack-level bound; F12's solver A still counts the near-misses of each 20-60 row.",
    ],
}
json.dump(m, open(ROOT / "packs-3.manifest.json", "w"), indent=1)
print(json.dumps(m["counts"], indent=1))
