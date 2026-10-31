#!/usr/bin/env python3
"""packs-1: write manifest.json (counts, licences, parents, sha256, checks, schema). Counts only; no pack text."""
import collections
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    packs = [json.loads(l) for l in open(HERE / "packs.jsonl")]
    draw = json.loads((HERE / "persona_draw.json").read_text())
    lint = json.loads((HERE / "lint_report.json").read_text())
    sq = json.loads((HERE / "packs.sealedqc.summary.json").read_text())
    ps = json.loads((HERE / "tmp" / "persona_seeds.sealedqc.summary.json").read_text())
    dv = json.loads((HERE / "packs1_denylist_verdicts.json").read_text())
    n = lambda k: [len(p[k]) for p in packs]  # noqa: E731
    tot = collections.Counter()
    for p in packs:
        tot["attributes"] += len(p["attributes"])
        tot["entity_types"] += len(p["entity_types"])
        tot["entity_names"] += sum(len(e["names"]) for e in p["entity_types"])
        tot["jargon_terms"] += len(p["jargon"])
        tot["document_types"] += len(p["document_types"])
        tot["label_words"] += len(p["label_words"])
        tot["outcome_sets"] += len(p["outcome_sets"])
        tot["consequences"] += len(p["consequences"])
        tot["inert_fact_types"] += len(p["inert_fact_types"])
        tot["ordered_scales"] += len(p["ordered_scales"])
        tot["people_names"] += len(p["people"])
        tot["id_pool_ids"] += sum(len(r["ids"]) for r in p["id_pool"])
        tot["lookalike_pairs"] += sum(len(r["lookalike_pairs"]) for r in p["id_pool"])
        for a in p["attributes"]:
            tot["attr_" + a["type"]] += 1
    # Held-out proposal (orchestrator decides): sha256(id) mod 8 == 0, never used by a training card if adopted.
    held = sorted(p["id"] for p in packs if int(hashlib.sha256(p["id"].encode()).hexdigest(), 16) % 8 == 0)
    files = {}
    for rel in ["packs.jsonl", "persona_draw.json", "lint_report.json", "packs.sealedqc.jsonl",
                "packs.sealedqc.summary.json", "packs1_denylist_query.json", "packs1_denylist_verdicts.json",
                "build_packs.py", "draw_personas.py", "make_manifest.py"] + \
               sorted(str(p.relative_to(HERE)) for p in (HERE / "src").glob("*.pack.txt")):
        files[rel] = sha(HERE / rel)
    ver = dv.get("verdicts") or dv.get("datasets") or {}
    man = {
        "name": "packs-1 domain packs (C_DATA_SPEC v4 2.1, step 3)",
        "agent": "packs-1",
        "pack_version": packs[0]["pack_version"],
        "fix_v1_1": {"review": "review-packs1 (3 Oct, verdict ISSUES)",
                     "boolean_aliases_rewritten": 13, "packs_with_alias_changes": 10,
                     "record_status_words_removed": {"names": 3, "free_text": 8},
                     "inert_items_replaced": 559, "inert_second_pass_rewrites": 23, "inert_items_distinct": len({s.lower() for p in packs for s in p["inert_fact_types"]}),
                     "jargon_renamed_cross_agent_clash": 3, "scripts": ["tmp/fix/apply_fix.py", "tmp/fix/apply_fix2.py", "tmp/fix/apply_fix3.py", "tmp/fix/apply_fix4.py"],
                     "originals": "tmp/fix/orig/ (v1.0 src, packs.jsonl 62b36964..., checks)"},
        "quarter": "industry and operations (manufacturing, logistics, utilities, construction, agriculture as a business, retail operations, plus transport and field-service operations)",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plan_refs": {"PREREG_FINAL": "A15 (sealed suite f4ae8637...), A16 (C round-1 plan)",
                      "C_DATA_SPEC.md": sha(LEAN / "c_spec" / "C_DATA_SPEC.md"),
                      "C_TRAIN_RECIPE.md": sha(LEAN / "c_spec" / "C_TRAIN_RECIPE.md")},
        "counts": {"packs": len(packs), "target_min": 75, "per_sector": dict(collections.Counter(p["sector"] for p in packs)),
                   "per_onet_group": dict(collections.Counter(p["persona_seed"]["onet_group"] for p in packs)),
                   "distinct_persona_seeds": len({p["persona_seed"]["onet_code"] for p in packs}),
                   "totals": dict(tot),
                   "per_pack_min": {k: min(n(k)) for k in ["roles", "sites", "partner_orgs", "entity_types", "attributes",
                                                             "jargon", "document_types", "status_values", "outcome_sets",
                                                             "consequences", "label_words", "actions", "objects",
                                                             "source_names", "inert_fact_types", "affixed_negatives",
                                                             "ordered_scales", "people"]},
                   "per_pack_min_id_pool": min(sum(len(r["ids"]) for r in p["id_pool"]) for p in packs)},
        "licences": {
            "packs": "CC0 1.0 (Claude-written; meta.licence of rows built from them stays 'CC0 1.0 (program-generated)')",
            "persona_titles": "O*NET 31.0 Database, CC BY 4.0 (titles only, main occupation file)",
            "notices_credit": "This work uses information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA), used under the CC BY 4.0 licence. Titles were used as persona seeds; USDOL/ETA has not approved, endorsed, or tested these modifications."},
        "parents": [{"name": "gd_onet_occupation", "what": "O*NET 31.0 Occupation Data, main occupation titles (persona seeds)",
                     "url": draw["source"]["url"], "licence_record": draw["source"]["licence_record"],
                     "sha256": draw["source"]["sha256"], "rows": draw["source"]["rows"],
                     "rule": "titles only, drawn by program (draw_personas.py, seed 20261003, 11 group prefixes and quotas fixed before the draw); never the alternate-titles or SOC direct-match file; PersonaHub never used",
                     "raw_file": "deleted after the build (re-fetch by url and check sha256)"}],
        "persona_draw": {"seed": draw["seed"], "drawn": len(draw["drawn"]), "used": len(packs),
                         "spares_kept": sum(len(g["spares"]) for g in draw["groups"])},
        "checks": {
            "lint": {"errors": len(lint["errors"]), "warnings": len(lint["warnings"]),
                     "warnings_note": "affix review only: words such as disposition, stainless, discharger, near miss, missed; every real affixed negative was removed from names (v1.1: 3 more in Boolean aliases) or declared",
                     "rules": ["minimum counts per field", "marker-collision and record-status words (MARKERS.md v1.1, F10 R4-02, F8)",
                               "negcount k_syn = k_all = 0 on every name, value, unit, status, outcome, level, label word, jargon term, Boolean alias, source name, inert fact type, org name and deciding role (v1.1 adds the last five)",
                               "negative-implicative stems and declared affixed words never in names", "F7 U03 banned factor stems in any form (risk, possib-, request, schedul-, plan/plans/planned/planning, expect-) on Boolean names and every alias (v1.1)",
                               "F8-R4-06 record-status words ('record' and 'log' in any form, 'on file', 'documented', 'registered', 'reported') nowhere in pack text, names or free text (v1.1)",
                               "inert fact types: each unique across packs-1, sharing no word with the pack's own attributes, values, aliases, statuses, outcomes, label words, levels, jargon, entity names, scope values or actions; no number or date word (v1.1; F7 U01/M4, F13 SEM-62)",
                               "SEM-31 ID pools (no I/L/O, Damerau-Levenshtein-1 look-alike pairs, no confusable swaps, fixed width, >= 60 IDs)",
                               "label natural predicates read only the pack's own attributes, values, tags and ranges",
                               "jargon: one coined lower-case 5-10 letter word, unique across packs-1",
                               "no placeholder text"]},
            "diversity_G11": {"metric": "ROUGE-L F (word LCS) between every pair of packs' flattened value text",
                              "pairs": len(packs) * (len(packs) - 1) // 2, "max": lint["rouge_l_max"],
                              "max_pair": lint["rouge_l_max_pair"], "limit": 0.7},
            "sealed_check": {"checker_sha256": sq["checker_sha256"], "suite_sha256": sq["suite_sha256"],
                             "input_sha256": sq["input_sha256"], "rows": sq["rows"], "rows_hit": sq["rows_hit"],
                             "rows_report_only": sq["rows_report_only"],
                             "report_only_kinds": {k: v["rows"] for k, v in sq["kinds"].items() if v["rows"] and not v["blocking"]},
                             "persona_titles": {"rows": ps["rows"], "rows_hit": ps["rows_hit"], "rows_report_only": ps["rows_report_only"]},
                             "dropped_or_replaced": 0},
            "denylist": {"program_sha256": dv.get("program_sha256"), "aliases_sha256": dv.get("aliases_sha256"),
                         "denylist_sha256": dv.get("denylist_sha256"), "canonical": dv.get("canonical"),
                         "counts": dv.get("counts"), "query_sha256": dv.get("query_sha256"), "verdicts": ver},
            "decontam_7_2": "not run here: the orchestrator runs the counts-only checks on these Claude seeds (spec 7.2) before any freeze"},
        "heldout_proposal": {"rule": "sha256(pack id) mod 8 == 0 (proposal only; the orchestrator rules the held-out pack set)",
                             "ids": held, "count": len(held)},
        "schema": {
            "id": "stable 'p1-<slug>'; every sub-object has a stable id '<pack id>:<a|e|j|d|o|c|l|s><nn>'",
            "fields": ["sector", "sub_sector", "setting", "org{name,kind}", "persona_seed{onet_code,onet_title,onet_group,source}",
                       "deciding_role", "roles", "sites", "partner_orgs", "item_kind{singular,plural}",
                       "entity_types[{eid,type,plural,id_prefix,names}]",
                       "attributes[{aid,name,type: num|int|cat|ord|bool|date|tags, unit, decimals, grid, range, nonneg, signed, values, ordered, kind: event|state, aliases, presupposes}]",
                       "unit_conversions", "units", "jargon[{jid,term,meaning}]", "document_types[{did,type,sections}]",
                       "status_values", "outcome_sets[{oid,outcomes}]", "consequences[{cid,tag: bad|not_bad,text}]",
                       "label_words[{lid,word,natural_predicate}]", "actions", "objects", "source_names",
                       "scope_dimension{name,values}", "inert_fact_types", "affixed_negatives", "ordered_scales[{sid,name,levels,order}]",
                       "people (program-drawn)", "id_pool[{eid,register,width,ids,lookalike_pairs}] (program-made)",
                       "provenance{author,licence,parents,program_parts,source_file,seed}", "pack_sha256"],
            "natural_predicate_grammar": "<attribute> above|under <number or attribute> | <attribute> is <v> [or <v>] | <attribute> include <tag> [or <tag>] | <event attribute> occurred | <state attribute> is in place"},
        "handoffs": [
            "F7 U01 concept sets: packs give Boolean aliases and inert fact types only; F7 builds full concept sets and disjointness lists from them and has them reviewed (F7 4.4)",
            "F1 R8 presupposition: every Boolean declares presupposes = null; F1 phrasings that presuppose a field must stay within that",
            "F10 invented names: jargon terms are candidates; F10's word-list, morphology, edit-distance and profanity filters still run",
            "Cross-agent G11 (ROUGE-L against packs-2..4) and the pack pool merge are the mixer's / orchestrator's"],
        "files_sha256": files,
    }
    (HERE / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"packs": len(packs), "heldout_proposal": len(held), "manifest": "manifest.json"}))


if __name__ == "__main__":
    main()
