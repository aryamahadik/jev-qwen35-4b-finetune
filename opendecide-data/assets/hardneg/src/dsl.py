"""Tiny authoring DSL for the train hard-negative draft (authored_by llm:claude:hardneg_author).

L(...) = state whose author gives a legitimate in-content instruction or correction that
         changes the correct answer (kind "legit_instruction").
Q(...) = state that quotes a third-party claim which must NOT change the answer
         (kind "quoted_claim").
N(instructions, gold, true_desc, false_desc) = Noul question (gold 1 = yes, 0 = no).
C(instructions, [(key, desc), ...], gold_key) = Choice question.
"""
import textwrap


def _state(s):
    return textwrap.dedent(s).strip("\n").strip()


def L(state, *questions):
    return {"kind": "legit_instruction", "state": _state(state), "questions": list(questions)}


def Q(state, *questions):
    return {"kind": "quoted_claim", "state": _state(state), "questions": list(questions)}


def N(instructions, gold, true_desc, false_desc):
    assert gold in (0, 1)
    return {"type": "noul", "instructions": instructions, "gold": gold,
            "criteria": {"true": true_desc, "false": false_desc}}


def C(instructions, options, gold):
    keys = [k for k, _ in options]
    assert gold in keys, (instructions, gold)
    assert len(set(keys)) == len(keys)
    return {"type": "choice", "instructions": instructions, "gold": gold,
            "options": [list(o) for o in options]}
