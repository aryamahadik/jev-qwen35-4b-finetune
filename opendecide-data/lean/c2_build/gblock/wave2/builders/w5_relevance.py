#!/usr/bin/env python3
"""W5: search relevance (PREREG_FINAL A40 b). Gold = CONSTRUCTION from Haiku-authored queries on REAL G-block documents.

Input: author/answers/W5_tNN.json (brief: make_tasks.W5_BRIEF) + author/tasks_key.json (doc_id -> G-block text_id;
the document is re-read from texts/, never from the answer). Per document Haiku wrote one query in each graded slot:
exact / substitute / complement / irrelevant. Row: choice over the 4 grades (fixed order, card = the grade
definitions); state = the document; instructions = the question with the query quoted (one line). Gold = the slot
(recorded, never chosen). A document marked skip loses all 4 rows; a malformed or repeated query loses only its row.
Labels are balanced to equal counts. group_id = the G-block text_id (shared with wave 1).

  ../../../../../.venv/bin/python -I builders/w5_relevance.py [--dry-run]
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders import common as C  # noqa: E402

T = "W5"
GRADES = ("exact", "substitute", "complement", "irrelevant")
DEFS = {
    "exact": "the document is what the searcher wants: it directly covers the thing the query asks for, with all "
             "the details the query states.",
    "substitute": "the document is about a close alternative to what the query asks for (a similar item, place, "
                  "activity, method or topic with at least one stated detail different), so it could serve instead "
                  "but is not an exact match.",
    "complement": "the document is not what the query asks for, but covers something a person with that need would "
                  "use together with it or need next.",
    "irrelevant": "the document does not help with the query's need at all, even if it shares some words with the "
                  "query.",
}
QUESTIONS = ('A user typed this search query: "{q}" How relevant is the document below to that search?',
             'Search query: "{q}" Which relevance grade fits the document below for this query?')
CARD = C.card_lines([(g, DEFS[g]) for g in GRADES])


def build(key: dict | None = None, answers: dict | None = None, texts: dict | None = None, checker=None) -> tuple:
    texts = texts if texts is not None else C.load_texts()
    rows, drops, tasks_seen, dd = [], Counter(), {}, C.Dedup()
    for tid, kk, obj, probs, prov in C.iter_answers(T, key, answers):
        tasks_seen[tid] = {"answered": obj is not None, "problems": probs}
        if obj is None:
            continue
        dmap = kk["documents"]
        items = obj.get("items")
        if not isinstance(items, list):
            tasks_seen[tid]["problems"].append("items is not a list")
            continue
        seen = set()
        for it in items:
            did = it.get("doc_id") if isinstance(it, dict) else None
            if did not in dmap or did in seen:
                drops["unknown_or_repeated_doc_id"] += 1
                continue
            seen.add(did)
            if it.get("skip") is True:
                drops["skipped_by_author"] += 1
                continue
            host = texts[dmap[did]]
            qs = {}
            for g in GRADES:
                q, why = C.text_field(it.get(g), min_w=1, max_w=20, single_line=True)
                if why:
                    drops[f"{g}_{why.split(' ')[0]}"] += 1
                    continue
                qs[g] = q
            low = Counter(q.lower() for q in qs.values())
            for g, q in qs.items():
                if low[q.lower()] > 1:
                    drops["same_query_in_two_grades"] += 1
                    continue
                if not dd.new(host["text_id"], q):
                    drops["duplicate_query"] += 1
                    continue
                qi = C.pick_wording(QUESTIONS, T, host["text_id"], g)
                rows.append(C.make_row(
                    T, f"{host['text_id']}:{g}", host["text_id"], host["text"], QUESTIONS[qi].format(q=q),
                    qtype="choice", options=list(GRADES), gold=g, card=CARD, gold_method="construction",
                    construction={"slot": g, "query": q},
                    extra_meta={"wording_id": f"W5.q{qi}", **C.text_meta(host),
                                "licence": f"document: {host.get('licence_url')}; query: {C.LICENCE_AUTHORED}",
                                **prov}))
    kept, rdrops, toks = C.check_all(rows, checker)
    bal = C.balance(kept, seed_tag="W5.balance")
    stats = C.authored_stats(T, tasks_seen, drops, rows, bal, rdrops, toks, {
        "before_balance": C.label_stats(kept), "domains": dict(Counter(r["meta"]["domain"] for r in bal))})
    return bal, stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    rows, stats = build()
    return C.finish_authored(T, rows, stats, argv)


if __name__ == "__main__":
    main()
