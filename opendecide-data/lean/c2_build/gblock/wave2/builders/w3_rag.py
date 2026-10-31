#!/usr/bin/env python3
"""W3: RAG faithfulness (PREREG_FINAL A40 b). Gold = CONSTRUCTION from Haiku-authored pieces on REAL G-block passages.

Input: author/answers/W3_tNN.json (brief: make_tasks.W3_BRIEF) + author/tasks_key.json (passage_id -> G-block
text_id; the passage text is re-read from texts/, never from the answer). Per passage Haiku wrote two questions and
four answers in fixed slots: supported_1, unsupported_1 (adds a claim the passage does not state), supported_2,
contradicting_2 (states something that conflicts with the passage). Row: yes/no "is every claim in the answer
supported by the passage?"; state = "Passage:\\n<passage>\\n\\nQuestion: <q>\\nAnswer: <a>"; card = yes/no
definitions. Gold = 1 for a supported_* slot, 0 for unsupported_1 / contradicting_2 (recorded, never chosen).
A passage marked skip, or with a missing / malformed / repeated piece, loses only the pairs that piece belongs to.
group_id = the G-block text_id (shared with wave 1, so any split keeps one passage's rows together).

  ../../../../../.venv/bin/python -I builders/w3_rag.py [--dry-run]
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders import common as C  # noqa: E402

T = "W3"
PAIRS = (("question_1", "supported_1", 1, "supported"), ("question_1", "unsupported_1", 0, "unsupported"),
         ("question_2", "supported_2", 1, "supported"), ("question_2", "contradicting_2", 0, "contradicting"))
QUESTIONS = ("Is every claim in the answer supported by the passage?",
             "Is the answer faithful to the passage, with nothing added or contradicted?")
YES = ("everything the answer states is said in the passage or follows directly from it (wording may differ, and the "
       "answer may leave things out).")
NO = ("the answer states at least one thing the passage does not say, or something that conflicts with the passage, "
      "even if the rest is right or the claim is true in the real world.")
CARD = C.yesno_card(YES, NO)


def state_of(passage: str, q: str, a: str) -> str:
    return f"Passage:\n{passage}\n\nQuestion: {q}\nAnswer: {a}"


def build(key: dict | None = None, answers: dict | None = None, texts: dict | None = None, checker=None) -> tuple:
    texts = texts if texts is not None else C.load_texts()
    rows, drops, tasks_seen, dd = [], Counter(), {}, C.Dedup()
    for tid, kk, obj, probs, prov in C.iter_answers(T, key, answers):
        tasks_seen[tid] = {"answered": obj is not None, "problems": probs}
        if obj is None:
            continue
        pmap = kk["passages"]
        items = obj.get("items")
        if not isinstance(items, list):
            tasks_seen[tid]["problems"].append("items is not a list")
            continue
        seen = set()
        for it in items:
            pid = it.get("passage_id") if isinstance(it, dict) else None
            if pid not in pmap or pid in seen:
                drops["unknown_or_repeated_passage_id"] += 1
                continue
            seen.add(pid)
            if it.get("skip") is True:
                drops["skipped_by_author"] += 1
                continue
            host = texts[pmap[pid]]
            f = {}
            for k in ("question_1", "question_2"):
                f[k], why = C.text_field(it.get(k), min_w=2, max_w=40, single_line=True)
                if why:
                    drops[f"{k}_{why.split(' ')[0]}"] += 1
            for k in ("supported_1", "unsupported_1", "supported_2", "contradicting_2"):
                f[k], why = C.text_field(it.get(k), min_w=1, max_w=90, single_line=True)
                if why:
                    drops[f"{k}_{why.split(' ')[0]}"] += 1
            for qk, ak in (("question_1", ("supported_1", "unsupported_1")),
                           ("question_2", ("supported_2", "contradicting_2"))):
                if f[ak[0]] and f[ak[1]] and f[ak[0]].lower() == f[ak[1]].lower():
                    drops[f"{ak[1]}_same_as_{ak[0]}"] += 1
                    f[ak[0]] = f[ak[1]] = None
            for qk, ak, gold, kind in PAIRS:
                if not f[qk] or not f[ak]:
                    continue
                if not dd.new(host["text_id"], f[qk], f[ak]):
                    drops["duplicate_pair"] += 1
                    continue
                qi = C.pick_wording(QUESTIONS, T, host["text_id"], ak)
                note = it.get({"unsupported": "unsupported_note", "contradicting": "contradicting_note"}.get(kind, ""))
                rows.append(C.make_row(
                    T, f"{host['text_id']}:{ak}", host["text_id"], state_of(host["text"], f[qk], f[ak]),
                    QUESTIONS[qi], qtype="noul", gold=gold, card=CARD, gold_method="construction",
                    construction={"slot": ak, "answer_kind": kind, "question_slot": qk,
                                  "author_note": C.one_line(note) if isinstance(note, str) else None},
                    extra_meta={"wording_id": f"W3.q{qi}", **C.text_meta(host),
                                "licence": f"passage: {host.get('licence_url')}; question and answer: "
                                           f"{C.LICENCE_AUTHORED}", **prov}))
    kept, rdrops, toks = C.check_all(rows, checker)
    bal = C.balance(kept, seed_tag="W3.balance")
    stats = C.authored_stats(T, tasks_seen, drops, rows, bal, rdrops, toks, {
        "before_balance": C.label_stats(kept),
        "answer_kinds": dict(Counter(r["meta"]["construction"]["answer_kind"] for r in bal)),
        "domains": dict(Counter(r["meta"]["domain"] for r in bal))})
    return bal, stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    rows, stats = build()
    return C.finish_authored(T, rows, stats, argv)


if __name__ == "__main__":
    main()
