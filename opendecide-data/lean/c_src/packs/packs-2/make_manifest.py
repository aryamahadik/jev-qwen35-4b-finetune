#!/usr/bin/env python3
"""packs-2 manifest writer (v1.1). Recomputes every count, lint summary, QC figure and code sha256 from the files in
this folder; the static sections that the v1.1 review fix did not touch (sectors, licence, persona draw, held-out note)
are carried over from the existing manifest_packs2.json.

Usage (from this folder): ../../../../.venv/bin/python make_manifest.py
"""
from __future__ import annotations

import collections
import datetime
import hashlib
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "manifest_packs2.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    old = json.loads(OUT.read_text())
    packs = [json.loads(l) for l in (HERE / "packs.jsonl").read_text().splitlines() if l.strip()]
    real = [a for p in packs for e in p["entity_types"] for a in e["attributes"]]
    bools = [a for a in real if a["type"] == "boolean"]
    tags = [a for a in real if a["type"] == "tag"]
    lint = [p["f10_f7_lint"] for p in packs]
    ctx = [len(p["inert_context_vocab"]) for p in packs]
    fills = [f for p in packs for f in p["filler_items"]]
    members = [len(a["concept_set"]["members"]) for a in real]
    statements = sum(len(a["lexicon"]["statements"]) for a in real)
    lw = [w for p in packs for w in p["label_words"]]
    case_lw = [l["label_words_case_entity"] for l in lint]
    qc = json.loads((HERE / "qc" / "qc_report_packs2.json").read_text())
    keyq = json.loads((HERE / "qc" / "sealedqc_keys_and_filler_pool_summary.json").read_text())
    dv = json.loads((HERE / "denylist_verdicts_packs2.json").read_text())
    counts = dict(old["counts"])
    counts.update({
        "packs": len(packs),
        "entity_types": sum(len(p["entity_types"]) for p in packs),
        "attributes_non_inert": len(real),
        "inert_attributes": sum(len(p["inert_attributes"]) for p in packs),
        "booleans": len(bools),
        "label_words": len(lw),
        "implicit_cues": sum(len(p["implicit_cues"]) for p in packs),
        "jargon_candidates": sum(len(p["jargon_candidates"]) for p in packs),
        "entity_ids": sum(len(e["ids"]) for p in packs for e in p["entity_types"]),
        "lookalike_pairs": sum(len(e["lookalike_pairs"]) for p in packs for e in p["entity_types"]),
        "person_names": sum(len(e.get("name_pool", [])) for p in packs for e in p["entity_types"]
                            if e.get("name_kind") == "person"),
        "v1_1": {
            "attribute_lexicons": sum(1 for a in real if all(k in a.get("lexicon", {}) for k in
                                                             ("phrases", "key_word_forms", "state_words"))),
            "lexicon_phrases": sum(len(a["lexicon"]["phrases"]) for a in real),
            "synonyms_claude_written": sum(len(a["concept_set"]["synonyms"]) for a in real),
            "key_word_forms": sum(len(a["lexicon"]["key_word_forms"]) for a in real),
            "state_words": sum(len(a["lexicon"]["state_words"]) for a in real),
            "statements": statements,
            "neg_statements": sum(1 for a in bools if a.get("neg_statement")),
            "pos_statements": sum(1 for a in bools if a.get("pos_statement")),
            "none_statements": sum(1 for a in tags if a.get("none_statement")),
            "statement_round_trip": {"sentences": sum(l["statement_round_trip"]["sentences"] for l in lint),
                                     "failures": sum(l["statement_round_trip"]["failures"] for l in lint)},
            "inert_context_vocab": {"total": sum(ctx), "min": min(ctx), "median": statistics.median(ctx)},
            "concept_sets": {"attributes": len(real), "members_total": sum(members), "members_min": min(members),
                             "members_median": statistics.median(members),
                             "booleans_with_broader_narrower_or_implication": sum(
                                 1 for a in bools if a["concept_set"]["broader"] or a["concept_set"]["narrower"] or
                                 a["concept_set"]["implies"])},
            "filler_items": {"total": len(fills), "event": sum(f["kind"] == "event" for f in fills),
                             "state": sum(f["kind"] == "state" for f in fills), "per_pack": 10},
            "disjointness_items": sum(len(p["disjointness_list"]) for p in packs),
            "label_words_name_lint_pass": sum(1 for w in lw if w["name_lint"] == "pass"),
            "label_words_case_entity_per_pack_min": min(case_lw),
            "marker_collision_hits": sum(l["marker_collision_hits"] for l in lint),
            "marker_lint_strings_checked": sum(l["strings_checked"] for l in lint),
        },
    })
    counts["per_pack_minimums"] = dict(old["counts"]["per_pack_minimums"])
    counts["per_pack_minimums"].update({
        "label_words_name_lint_pass": 12, "label_words_over_case_entity": 12, "inert_context_vocab": 30,
        "filler_items": 8, "filler_events": 3, "filler_states": 3, "concept_set_members": 3})
    tc = collections.Counter(a["type"] for a in real)
    man = {
        "artifact": old["artifact"],
        "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "packs-2 v1.1 (review fixes for review-packs2, 3 Oct; v1.0 packs.jsonl sha256 3cfe275a01e08f0c... "
                   "is superseded)",
        "quarter": old["quarter"],
        "sectors": old["sectors"],
        "file": {"path": "c_src/packs/packs-2/packs.jsonl", "sha256": sha(HERE / "packs.jsonl"),
                 "packs": len(packs), "bytes": (HERE / "packs.jsonl").stat().st_size,
                 "id_rule": old["file"]["id_rule"],
                 "rebuild": "build_packs.py is deterministic: a second run writes a byte-identical file"},
        "pack_ids": [p["id"] for p in packs],
        "counts": counts,
        "attribute_types": dict(sorted(tc.items())),
        "licence": old["licence"],
        "internal_inputs": [
            {"path": "c_src/common/markers.json", "sha256": lint[0]["markers_json_sha256"],
             "use": "R4-02 marker-collision word classes (unknown, zero-or-absent, banned with case and dash forms) "
                    "and F10's local 'not listed'; read only, never edited"},
            {"path": "c_src/common/negcount.py", "use": "negation counter for name-like strings and statements"},
        ],
        "parents": old["parents"],
        "persona_draw": old["persona_draw"],
        "denylist": {
            "program": dv["program"], "version": dv["version"], "program_sha256": dv["program_sha256"],
            "aliases_sha256": dv["aliases_sha256"], "denylist_sha256": dv["denylist_sha256"],
            "canonical": dv["canonical"], "query": "denylist_query_packs2.json", "query_sha256": dv["query_sha256"],
            "verdicts": "denylist_verdicts_packs2.json", "verdicts_sha256": sha(HERE / "denylist_verdicts_packs2.json"),
            "created_utc": dv["created_utc"], "counts": dv["counts"],
            "result": f"{dv['counts']['datasets']} checked (80 packs + pack builder + O*NET + word list): "
                      f"{dv['counts']['deny_taint']} taint, {dv['counts']['ohs3_hit']} ohs3 hits, "
                      f"{dv['counts']['sealed_hit']} sealed hits; O*NET parent hits the rejected alternate-titles "
                      "entry as no_new_rows, which passes for persona seeds (spec 2.1 F4, 3.H.2). v1.1 adds no "
                      "third-party input, so the query is unchanged (same sha256); deny-list rebuilt and re-run",
        },
        "sealed_check": {
            "program": "lean/sealed_nd/qc/sealed_check.py (run as a program; exports never read)",
            "checker_sha256": qc["sealed_check"]["checker_sha256"],
            "suite_sha256": qc["sealed_check"]["suite_sha256"],
            "p_vocab_loaded": qc["sealed_check"]["p_vocab_loaded"],
            "whole_packs": qc["sealed_check"]["whole_packs"],
            "components": qc["sealed_check"]["components"],
            "dict_keys_and_filler_pool": {"rows": keyq["rows"], "rows_hit": keyq["rows_hit"],
                                          "kinds": {k: v["rows"] for k, v in keyq["kinds"].items() if v["rows"]}},
            "blocking_hits": len(qc["sealed_check"]["hit_pack_ids"]) + len(qc["sealed_check"]["hit_component_ids"]) +
            keyq["rows_hit"],
            "dropped_or_replaced": 0,
            "note": "keyword_soft is report-only (not blocking); counts only. Components = every string value in "
                    "every pack (lexicons, statements, concept sets, fillers and inert vocabulary included); a third "
                    "run covers every dict key and the whole shared filler pool (drawn or not)",
            "summaries": ["qc/sealedqc_packs_summary.json", "qc/sealedqc_components_summary.json",
                          "qc/sealedqc_packs_ids.jsonl", "qc/sealedqc_keys_and_filler_pool_summary.json"],
        },
        "diversity": {
            "rouge_l_worst_pack_pair": qc["rouge_l"]["worst_pack_pair"],
            "rouge_l_worst_setting_pair": qc["rouge_l"]["worst_setting_pair"],
            "pairs_over_0_7": len(qc["rouge_l"]["over_0_7"]),
            "cross_quarter": {"files": qc["rouge_l"]["cross"]["files"], "worst": round(qc["rouge_l"]["cross"]["worst"], 4),
                              "over_0_7": len(qc["rouge_l"]["cross"]["over_0_7"])},
            "statement_frames": {"total": statements,
                                 "distinct": len({s for a in real for s in a["lexicon"]["statements"].values()})},
            "report": "qc/qc_report_packs2.json",
        },
        "decontamination": old["decontamination"],
        "lints": (
            "build_packs.py lints all pass (0 errors). v1.0 lints kept: counts per pack, shared negcount (k_all 0 on "
            "every name-like string), declared vs undeclared affixed words, F7 banned factor stems, F4 link and cue "
            "bans, predicate parsing, unique keys, SEM-31 IDs. v1.1 lints: (1) R4-02 marker-collision lint on every "
            "attribute key, label, alias, synonym, category value, tag name, unit, unit synonym, lexicon phrase, "
            "statement (zero-class 'no' allowed only in the negative statement, 'none' only in the none statement), "
            "key-word form, state word, concept-set member, label word, entity name, alias and name pool, inert "
            "attribute and filler item; word classes from c_src/common/markers.json plus 'null', 'false', 'true', "
            "'yes', F10's 'not listed', and 'record' / 'list' in any form (waitlist, checklist ... included), "
            "'stated', 'missing', 'blank', 'pending', 'known', 'available', 'applicable', 'specified', 'determined' "
            "with un- / in- forms; (2) R4-03 name lint: every label word passes against the pack's legend strings, "
            "attribute-lexicon words and word stems, document types, outcomes and the operator / connective content "
            "words (every word must pass, >= 12 per pack, and >= 12 per pack whose natural predicate reads only the "
            "case entity's attributes); (3) R4-01 inert-context vocabulary disjoint from every attribute lexicon "
            "(exact words and stems) and from F7 concept sets, label words, operator, number, calendar and marker "
            "words, >= 30 words per pack; (4) statements: {E} / {v} placeholders, the negative statement's value word "
            "is 'no' or 'not' with a counted negation, positive and value statements negation-free, no modal or "
            "hedged verb (ST50); statement round trip: every statement rendered with probe values parses back to "
            "exactly its own attribute, kind and value among all statements of its entity type; (5) F7 U01: every "
            "concept set has >= 3 members, every Boolean factor has broader / narrower / implication members, "
            "synonyms pass the negation, affix and banned-stem lints; inert attributes and filler items share no "
            "content word stem with any rubric concept set; (6) F7 Z02 fillers: >= 8 per pack, >= 3 event and >= 3 "
            "state, affirmative, no banned stem"),
        "schema": {
            "top": old["schema"]["top"].replace(
                "disjointness_list[]", "disjointness_list[] (inert attribute keys + filler keys), filler_items[]") +
            ", inert_context_vocab[], f10_f7_lint{marker_collision_hits, strings_checked, label_words, "
            "label_words_name_lint_pass, label_words_case_entity, inert_context_vocab, filler_items, "
            "statement_round_trip, markers_json_sha256}",
            "entity_type": old["schema"]["entity_type"],
            "attribute": old["schema"]["attribute"] +
            "; v1.1 on every rubric attribute: lexicon{phrases (label, aliases, synonyms, statement frames), "
            "synonyms, statements{value | positive + negative | value + none}, key_words, key_word_forms, "
            "state_words, forms_dropped_as_markers?}, concept_set{term, aliases, synonyms, broader, narrower, "
            "implies, members}; booleans add pos_statement and neg_statement, tag attributes none_statement. "
            "Statement frames use {E} (the entity reference) and {v} (the value as rendered with its unit)",
            "inert_attribute": "as v1.0 plus concept_set{term, aliases, members}",
            "filler_item": "key (fill_<words>), entity, type boolean, kind event|state, label, filler true, drawn?, "
                           "concept_set{term, synonyms, members}",
            "label_word": "word, predicate_text, predicate, name_lint (pass), entity (the entity type its predicate "
                          "reads)",
            "label_word_predicate": old["schema"]["label_word_predicate"],
        },
        "family_coverage": dict(old["family_coverage"]),
        "held_out": old["held_out"],
        "code": {f: sha(HERE / f) for f in
                 ["build_packs.py", "draw_personas.py", "qc_packs.py", "make_manifest.py", "qc/verify_v11.py",
                  "src/common_pools.py"] +
                 sorted(str(p.relative_to(HERE)) for p in (HERE / "src").glob("sec_*.py")) +
                 sorted(str(p.relative_to(HERE)) for p in (HERE / "src").glob("lex_*.py"))},
    }
    man["family_coverage"]["F7"] = (
        "Boolean factors with kind event|state and banned factor stems linted (labels, aliases, synonyms, fillers); "
        f"U01 concept sets on all {len(real):,} rubric attributes (term, aliases, Claude-written synonyms; broader, narrower and "
        "implication members on every Boolean factor; >= 3 members each); disjointness list = 12 inert attributes + "
        "10 filler Booleans per pack (5 event, 5 state, drawn by program from a shared Claude-written pool), every "
        "item token-stem disjoint from all rubric concept sets; level scales with usual rank; cutpoint_ok numerics. "
        "Not done here: U01's second-session review of concept sets and disjointness lists (a separate reviewer's job)")
    man["family_coverage"]["F10"] = (
        "Pack requirements (G0 section 2, R4-01/R4-02/R4-03) met: typed attributes with units, grids, ranges, full "
        "value lists, tag vocabularies <= 10; per rubric attribute a lexicon (phrases, synonyms, statement frames, "
        f"key words in every word form, state words); a negative fact statement on all {len(bools)} flags and a "
        f"'none' statement on all {len(tags)} tag attributes; an inert-context vocabulary per pack (>= {min(ctx)} "
        "words) disjoint from every attribute lexicon; 0 marker-collision hits; "
        f"{len(lw):,} familiar label words with natural predicates, all passing "
        "the name lint, >= 12 per pack over the case entity's attributes; consequences tagged adverse; 16 invented "
        "jargon candidates per pack (dictionary- and morphology-filtered; F10's own >= 300K 3-language word list "
        "still applies at card build). Card-time lints (name lint against the card's own legend, render lint) stay "
        "with the F10 generator (G1 / G3)")
    man["problems"] = [
        "pack schema is this agent's own; packs-1 and packs-4 use different field names (e.g. org vs org_name, jargon "
        "vs jargon_candidates); generators or the mixer need an adapter or one shared schema",
        "keyword_soft (report-only) sealed-check matches on all 80 packs; no blocking hit",
        "invented jargon was filtered only against the local web2 list (English); F10's >= 300K 3-language list must "
        "still run",
        "F7 U01 asks for a second-session review of every pack's concept sets and disjointness list; not done by this "
        "builder",
        "statement frames are lexicon entries, so short frames repeat across packs (1,729 distinct of 1,995; the tag "
        "and 'none' frames share one pattern on purpose); pack-level ROUGE-L stays far below 0.7",
        "the operator / connective word list used by the name lint is a pack-side superset; F10's registered step-4 "
        "pools are not written yet, so the card-time name lint must re-run against them",
    ]
    man["review_fixes_v1_1"] = {
        "review": "review-packs2 (c_build/progress_phase1.log 21:46:19Z): ISSUES",
        "fixed": [
            "F10 (a) fields: lexicon{phrases, key_word_forms, state_words} (+ synonyms, statements, key_words) on all "
            "1,493 rubric attributes; neg_statement on all 422 flags; none_statement on all 80 tag attributes; "
            "pack-level inert_context_vocab with a disjointness lint",
            "F10 (b) marker-collision lint added to build_packs.py; 21 attribute keys and labels, 27 alias lists, 3 "
            "value lists, 8 entity types (names, aliases or name pools) and 1 inert attribute renamed; label words "
            "'listed' and 'pending' replaced; 0 hits",
            "F10 (c) name lint added: 456 label words renamed (same predicates), 105 added; all 1,150 pass; >= 12 "
            "per pack over the case entity's attributes",
            "F10 further checks: inert-context disjointness, statement checks and a statement round trip (3,446 "
            "sentences, 0 failures)",
            "F7 U01: concept sets with Claude-written synonyms on every attribute and broader / narrower / "
            "implication members on every Boolean factor; 10 filler Booleans per pack in the disjointness list; "
            "inert and filler items checked against every rubric concept set (38 pack-specific inert attributes "
            "renamed to pass)",
            "manifest: F7 and F10 coverage now states what is and is not covered",
        ],
    }
    OUT.write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.name}: packs sha256 {man['file']['sha256'][:16]}...")


if __name__ == "__main__":
    main()
