"""transfer/T36/double_neg.py: the Haiku wording round for the double-negation form yn_double (G0_SPEC.md v2.2 section 6;
Stage B pilot fix F5; C2_DATA_SPEC 3.0 "double negation on at least 2% of yes/no rows").

Why. The pilot had 0% double negation: no question form had two syntactic negations (G10 bar 2%, k_syn >= 2). v2.2 adds
the form yn_double (positive polarity: a yes answer means the version meets the range). Its wordings must be written by
Haiku (this file builds the task, it never runs Haiku and writes nothing unless --write is given; A37 f: only after A38)
and then admitted by G-LEX (2/2 blind extractions of the meaning plugin.QUESTION_MEANINGS_V22["yn_double"]).

The failure to avoid (T35 pilot G5-H: 3 confirmed wrong golds in 100 rows, all double negation). A wording such as "is it
not the case that they do not bar the crawler ...?" has two syntactic negations (negcount k_syn = 2) and a negative
predicate ("bar") that negcount does not list; read literally it means the OPPOSITE of the form. c2_kit.polarity decides it
(rule P1-P3, plugin.NEGATIVE_PREDICATES), and so does the brief below:
  * exactly two plain negations: the outer frame "is it not the case / true / so / correct that ..." and a "not" on the verb
    "meet" ("... does not meet ..."): "Is it not the case that version X does not meet the range declared for P?"
  * no contracted negative anywhere (rule P3), no negative predicate (outside, beyond, exceed, fall short, violate, break,
    conflict, incompatible, reject, exclude, miss, block, bar, forbid ...), no implicit cue (fail to, lack, without, unless,
    false ...), and still no gold-label word the card defines as a verdict (outside, inside, within ...).

  python3 double_neg.py [--dry-run | --write]    # builds and checks the batch; --write needs A38 (paths.write_files)
  wording_problems(plugin, text)                   # the admission check of one returned wording (before G-LEX)
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths, polarity  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths; read-only reuse)
from c2_kit.skin import make_skin  # noqa: E402
from transfer.T36 import authoring as A  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402

FORM = "yn_double"
ROOT = P.HERE / "haiku" / "author_dn"
VERSION = "v2.2"
WORDING_COUNT = 16                 # authored; the plan needs >= 6 admitted (each wording <= 2% of rows), the rest is margin
MEANING = ("asks whether the version under review meets the declared range of the package (a yes answer means it meets "
           "the range), worded with two negations that cancel each other")
FRAMES = ("the case", "true", "so", "correct", "accurate", "right", "fair")      # polarity.EXPLICIT_FRAME (minus "false")

EXTRA = "\n".join([
    "DOUBLE NEGATION (this task only; it overrides any earlier line that names a different number of negation words or suggests "
    "the word outside): every question has EXACTLY TWO negation words, both the plain word \"not\", placed like this:",
    "- the first \"not\" is part of the opening frame: \"Is it not " + ", ".join(FRAMES[:3]) + " or " + FRAMES[3] + " that ...\" "
    "(other frames, such as \"Would it not be the case that ...\", are NOT allowed), optionally after a short phrase such as "
    "\"Under these rules,\";",
    "- the second \"not\" negates the verb meet: \"... version {CAND} does not meet the range declared for {PKG}?\" (or \"... "
    "{CAND} does not meet the declared range of {PKG}?\").",
    "Together they cancel: the question asks whether the version meets the range (a yes answer means it meets it).",
    "Never write a contracted negative (isn't, doesn't, aren't, wouldn't ...), never the words outside, beyond, exceed, short, "
    "violate, break, conflict, incompatible, reject, exclude, miss, block, bar, forbid, fail, lack, deny, refuse, without, "
    "unless, except, false, untrue, wrong, never, no, none, nothing or nobody, and never a third negation. Vary the rest of the "
    "sentence (framing phrase, word order, \"version {CAND}\" or \"{CAND}\", where {PKG} sits) but keep the meaning exact.",
])

ITEM = ("yes/no question", MEANING, ["{CAND}", "{PKG}"], 2,
        ["exactly two negation words, both \"not\": the frame \"Is it not <the case | true | so | correct> that\" and \"does not "
         "meet\"",
         "no contracted negative, no negative word other than those two \"not\"s",
         "never use the words outside, inside, within or fail"])


def prompt() -> str:
    """The base wording prompt (authoring.wording_prompt) with the double-negation paragraph."""
    return A.wording_prompt() + "\n" + EXTRA


def items(rng: random.Random) -> list:
    typ, meaning, slots, k, rules = ITEM
    styles = rng.sample(A.WORDING_STYLES, len(A.WORDING_STYLES))
    out = []
    for i in range(WORDING_COUNT):
        out.append((f"t36|wording|{FORM}|{i:03d}",
                    {"brief": f"Type: {typ}. Meaning (keep exactly): {meaning}. Placeholders: {', '.join(slots)}, each exactly "
                              f"once. Negation words: exactly {k}. Style: {styles[i % len(styles)]}.",
                     "slots": list(slots), "rules": list(rules)}))
    return out


def build() -> chunker.TaskBatch:
    """The task batch (deterministic, seeded); forbidden strings as authoring.FORBID_FREE (the question texts and the None
    option)."""
    rng = random.Random(f"T36|author_dn|{VERSION}")
    b = chunker.make_batch("author_wording", P.FAMILY, items(rng), seed=f"t36-author-dn-{VERSION}", prompt=prompt(),
                           max_items=WORDING_COUNT, forbid_strings=A.FORBID_FREE)
    for i, c in enumerate(b.chunks):
        answer = str(ROOT / b.answer_path(c["task_id"]))
        if paths.never_open(answer) or paths.never_open(ROOT / b.chunk_path(c["task_id"])):
            raise chunker.ChunkError(f"never-open path for {c['task_id']}")
        b.chunks[i] = {"task_id": c["task_id"], "kind": c["kind"], "pool": "wording_dn", "prompt_sha": c["prompt_sha"],
                       "answer_file": answer, "instructions": prompt().split("\n"), "items": c["items"]}
    return b


def wording_problems(plugin, text: str) -> list:
    """Why a returned yn_double wording must not enter the pool (empty list: it may go to G-LEX): the authoring lint of a
    wording, one line ending in "?", exactly two syntactic negations and nothing else negative, and the polarity rule
    (c2_kit.polarity P1-P3) with the family's negative predicates."""
    probs = []
    text = (text or "").strip()
    if not text.endswith("?") or "\n" in text:
        probs.append("one line ending with ?")
    try:
        sk = make_skin("T36-dn-check", P.FAMILY, text, {"CAND": "id", "PKG": "id"}, kind="wording", register="question",
                       qform=FORM)
    except Exception as e:  # noqa: BLE001  (a bad placeholder layout)
        return probs + [f"template: {e}"]
    probs += [f"{v.rule}: {v.detail}" for v in gsl.lint_template(sk)]
    nc = negcount.count(text.replace("{CAND}", "X").replace("{PKG}", "Y"))
    if nc.k_syn != 2 or nc.k_all != 2:
        probs.append(f"negation count k_syn {nc.k_syn}, k_all {nc.k_all}: exactly two plain negations")
    probs += polarity.form_problems(plugin, FORM, text)
    return probs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="build and check the batch, write nothing (default)")
    g.add_argument("--write", action="store_true", help="write the task files (refused before A38)")
    a = ap.parse_args(argv)
    b = build()
    if a.write:
        paths.write_files(ROOT, b.files())
    print(json.dumps({"form": FORM, "n_items": len(b.key), "n_tasks": len(b.chunks), "prompt_sha": b.prompt_sha,
                      "written": bool(a.write)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
