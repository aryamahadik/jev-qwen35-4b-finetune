#!/usr/bin/env python3
"""W4: off-topic vs a stated assistant scope (PREREG_FINAL A40 b). Gold = CONSTRUCTION from Haiku-authored pieces.

Input: author/answers/W4_tNN.json (brief: make_tasks.W4_BRIEF). Per setting Haiku wrote a scope statement, 10 messages
in the "in_scope" slot and 10 in the "off_topic" slot. Row: yes/no "is the message off-topic for this assistant?";
state = the user message; instructions = the question with the scope quoted (one line); card = yes/no definitions.
Gold = 1 for "off_topic", 0 for "in_scope" (recorded, never chosen). Malformed items are dropped, never repaired;
exact duplicate messages are dropped; labels are balanced to equal counts.

  ../../../../../.venv/bin/python -I builders/w4_offtopic.py [--dry-run]
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders import common as C  # noqa: E402

T = "W4"
SLOTS = {"off_topic": 1, "in_scope": 0}
IN_KINDS = ("core", "unusual_but_covered", "short_or_vague", "small_talk_or_meta", "messy_or_misspelled",
            "long_detailed")
OFF_KINDS = ("near_miss", "far_away", "starts_on_topic_then_switches", "personal_or_general_knowledge",
             "other_business")
QUESTIONS = (
    'An assistant has this scope: "{scope}" Is the user message below off-topic for this assistant?',
    'Assistant scope: "{scope}" Does the user message below ask for something outside this scope?',
)
YES = ("the message's main request falls outside what the scope covers, including requests that sound close to the "
       "assistant's subject but are not covered.")
NO = ("the main request is covered by the scope; greetings, thanks, short follow-ups and questions about what the "
      "assistant can do also count as in scope.")
CARD = C.yesno_card(YES, NO)


def build(key: dict | None = None, answers: dict | None = None, checker=None) -> tuple:
    rows, drops, tasks_seen, dd = [], Counter(), {}, C.Dedup()
    for tid, kk, obj, probs, prov in C.iter_answers(T, key, answers):
        tasks_seen[tid] = {"answered": obj is not None, "problems": probs}
        if obj is None:
            continue
        want = kk["settings"]
        ass = obj.get("assistants")
        if not isinstance(ass, list):
            tasks_seen[tid]["problems"].append("assistants is not a list")
            continue
        seen = set()
        for a in ass:
            aid = a.get("a_id") if isinstance(a, dict) else None
            if aid not in want or aid in seen:
                drops["unknown_or_repeated_a_id"] += 1
                continue
            seen.add(aid)
            scope, why = C.text_field(a.get("scope"), min_w=8, max_w=140, single_line=True)
            if why:
                drops["scope_" + why.split(" ")[0]] += 1
                continue
            for slot, gold in SLOTS.items():
                items = a.get(slot)
                if not isinstance(items, list):
                    drops[f"{slot}_not_a_list"] += 1
                    continue
                if len(items) != 10:
                    drops[f"{slot}_count_{len(items)}_not_10"] += 1
                for j, it in enumerate(items):
                    if not isinstance(it, dict):
                        drops["item_not_object"] += 1
                        continue
                    msg, why = C.text_field(it.get("text"), min_w=1, max_w=160)
                    if why:
                        drops[f"message_{why.split(' ')[0]}"] += 1
                        continue
                    if not dd.new(scope, msg):
                        drops["duplicate_message"] += 1
                        continue
                    kind = it.get("kind") if it.get("kind") in (OFF_KINDS if gold else IN_KINDS) else "other"
                    qi = C.pick_wording(QUESTIONS, T, tid, aid, slot, j)
                    rows.append(C.make_row(
                        T, f"{tid}:{aid}:{slot}{j + 1:02d}", f"c2_wave2:W4:{tid}:{aid}", msg,
                        QUESTIONS[qi].format(scope=scope), qtype="noul", gold=gold, card=CARD,
                        gold_method="construction",
                        construction={"slot": slot, "kind": kind, "setting": want[aid]["setting"]},
                        extra_meta={"wording_id": f"W4.q{qi}", "licence": C.LICENCE_AUTHORED, **prov}))
    kept, rdrops, toks = C.check_all(rows, checker)
    bal = C.balance(kept, seed_tag="W4.balance")
    stats = C.authored_stats(T, tasks_seen, drops, rows, bal, rdrops, toks, {
        "before_balance": C.label_stats(kept),
        "kinds": dict(Counter(f"{r['meta']['construction']['slot']}/{r['meta']['construction']['kind']}"
                              for r in bal))})
    return bal, stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    rows, stats = build()
    return C.finish_authored(T, rows, stats, argv)


if __name__ == "__main__":
    main()
