"""Writes solver_b/question_templates.json: the QUESTION wording templates solver B reads the question sentence with.

Why this exists (skeptic finding, 18 Oct): B was written against the TEST-ONLY wording pool and could not read a single row built from the real
Haiku pool (every row failed with question_not_found). A question sentence cannot be read by a wording-free rule for the forms whose slots
swap roles between wordings (CA-C3 pair vs z, CA-C4 t/o, TM-T1 start/offset ...), so B compiles each question template to a regular
expression and recovers the SLOT VALUES from the stem. The facts in front of the question are still read by B's own hand-written frames.
Only slot PLACEMENT is shared with the wording pool; what the facts MEAN is still B's own reading.

    python3 export_question_templates.py          # rewrites solver_b/question_templates.json (the test asserts it is current)
Sets: "real" = pools/q_*.json (the Haiku pool); "testonly" = gen_common.make_testonly_pool() (unit tests and the dry run).
Hashes only are exported to HASH_EXPORT.json; this file holds wording text and stays inside solver_b/.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

from gen_common import make_testonly_pool  # noqa: E402

OUT = os.path.join(HERE, "solver_b", "question_templates.json")
POOL_FILES = ("q_arith.json", "q_logic.json", "q_causal.json", "q_temporal.json", "q_table.json")


def build():
    real = {}
    for fn in POOL_FILES:
        with open(os.path.join(HERE, "pools", fn), "r", encoding="utf-8") as f:
            for k, v in json.load(f)["entries"].items():
                if k.startswith("q."):
                    real[k] = list(v)
    test = {k: list(v) for k, v in make_testonly_pool().entries.items() if k.startswith("q.")}
    return {"note": "question wording templates for solver B (slot placement only); regenerate with export_question_templates.py",
            "sets": {"real": real, "testonly": test}}


def main():
    obj = build()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True, ensure_ascii=True)
        f.write("\n")
    print("wrote", OUT, {k: sum(len(x) for x in v.values()) for k, v in obj["sets"].items()})


if __name__ == "__main__":
    main()
