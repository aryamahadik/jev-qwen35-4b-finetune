"""families/T01/haiku_dneg.py: the T01 double-negation WORDING round (G0_SPEC_v4.md section 12.1; pilot fix F1).

Why. The frozen pools_v2 hold no wording with two syntactic negations (G0 v3 section 7 asked for k_syn <= 1 everywhere),
so the pilot's double-negation share is 0% against the spec 3.0 bar of 2% of yes/no rows (G10). The generator now draws
six double-negation base forms (plugin.DNEG_FORMS) once a clean, admitted wording exists; this module is the authoring
task that supplies them. It changes nothing that exists: haiku_author.py, the frozen answers, plans and pools_v2/ stay
byte for byte as they are (freeze_v2 rebuilds them), and nothing here runs a model.

  build_batch()   the gold-free authoring batch (c2_kit.chunker.make_batch): 6 forms x 12 items = 72 wordings, <= 48 per
                  chunk, the same WORDING_PROMPT as the round-1 wordings, a brief that asks for the safe shape only
  check_wording() admission of ONE answer: the round-1 wording checks plus the exact profile (negcount k_all = k_syn = 2)
                  and the polarity rule (c2_kit.polarity P1-P4, strict frames), so a wording that reads the other way
                  round (T35's "is it not the case that they do not bar ...") never enters a pool
  write_tasks()   writes the chunks, key, manifest and one task file per chunk under haiku/redo4/ (guarded writers); the
                  orchestrator runs it, then one fresh Haiku agent per task file

Afterwards (not done here): 2/2 independent G-LEX extractions per admitted wording (sems q.t01.yn_dneg_*, meanings in
fixtures.DNEG_MEANINGS), a pool freeze that adds the admitted forms (freeze_v3; freeze_v2 keeps the 26 frozen forms), G13-seed
on the new texts, then a G5-H re-read with at least 10 double-negation rows.

Run (from lean/c2_build):  ../.venv/bin/python -B -m families.T01.haiku_dneg plan | write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T01 import fixtures as FX  # noqa: E402
from families.T01 import haiku_author as A  # noqa: E402
from families.T01 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

FAMILY = "T01"
ROOT = HERE / "haiku" / "redo4"
SEED = "t01-dneg-v1"
N_PER_FORM = 12
MAX_ITEMS = 48
FORMS = tuple(P.DNEG_FORMS.values())
NEG_PROFILE = (2, 2)                 # negcount (k_all, k_syn): two syntactic negations, nothing else
FORBID = A.QSTRINGS + tuple(t for _, _, t, _ in FX.DNEG_WORDINGS)

# the words a double negation must NOT hide a negative predicate in: lateness, blocking, denial, lack (polarity P1)
BLOCKING = ("late", "too late", "after the deadline", "bar", "block", "deny", "prevent", "refuse", "lack", "without",
            "fail to", "unless", "except", "forbid", "exclude", "stop", "skip")
CONTRACTED = ("isn't", "aren't", "wasn't", "weren't", "doesn't", "don't", "didn't", "hasn't", "haven't", "won't",
              "wouldn't", "can't", "couldn't", "shouldn't")

# the shape every item asks for (the polarity rule's safe shape: explicit outer frame, a second "not" on a positive word)
SHAPE = ("Use exactly TWO negations and no other negation word. The first is 'not' in an explicit outer frame: the "
         "clause opens with 'is it not the case that' or 'is it not true that' (a short opening phrase such as "
         "'Under the card's rule,' may come before it). The second is on the clause's own positive word, as the item "
         "says. Never use a contracted form (" + ", ".join(CONTRACTED[:6]) + " ...), never put 'not' straight after "
         "the subject of a question ('Is the person not ...?'), and never use a word of lateness, blocking, denial or "
         "lack (" + ", ".join(BLOCKING[:9]) + " ...) anywhere in the question.")

DNEG_BRIEF = {   # qform -> (meaning, [form rules]); the meanings repeat the round-1 meanings of the base forms
    "yn_dneg_over": ("A yes/no question with the same meaning as 'is the person over the stay limit, that is, are more "
                     "days present inside the checked window (the window that ends on the reference date) than the "
                     "limit?' (yes = over the limit), asked with two negations.",
                     [SHAPE, "The second 'not' goes on 'over the stay limit' (for example '... is it not the case that "
                             "{PERSON} is not over the stay limit ...'; do not copy it)."]),
    "yn_dneg_timely": ("A yes/no question with the same meaning as 'was the document filed in time, that is, on or "
                       "before the final day of the filing period?' (yes = filed in time), asked with two negations.",
                       [SHAPE, "The second 'not' goes on 'filed in time' or 'filed on or before the final day'."]),
    "yn_dneg_covered": ("A yes/no question with the same meaning as 'is the loss covered under the cover rule?' "
                        "(yes = covered), asked with two negations.",
                        [SHAPE, "The second 'not' goes on the word 'covered'."]),
    "yn_dneg_quotes": ("A yes/no question with the same meaning as 'does the purchase request need written quotes "
                       "under the purchase rule?' (yes = quotes are needed), asked with two negations.",
                       [SHAPE, "The second 'not' goes on 'need' or 'call for' written quotes ('... does not need "
                               "written quotes')."]),
    "yn_dneg_cash_report": ("A yes/no question with the same meaning as 'is a cash report required for the day under "
                            "review?' (yes = a report is required), asked with two negations.",
                            [SHAPE, "The second negation is the word 'no' before 'cash report' ('is it not true that "
                                    "no cash report is required ...')."]),
    "yn_dneg_on_time": ("A yes/no question with the same meaning as 'was the response to the notice on time under "
                        "the receipt rule?' (yes = on time), asked with two negations.",
                        [SHAPE, "The second 'not' goes on 'on time'. Say 'on time under the receipt rule' or "
                                "'counted as received on time'; never say the response was 'sent' or 'arrived' on "
                                "time (the rule decides on the day the office counts it as received)."]),
}


def _items():
    items, plan = [], {}
    for q in FORMS:
        kind = P.KIND_OF[q]
        meaning, rules = DNEG_BRIEF[q]
        for i in range(N_PER_FORM):
            slots = A.SLOT_SETS[kind][i % len(A.SLOT_SETS[kind])]
            style = A.STYLES[i % len(A.STYLES)].replace("{RULE}", A.RULE_NAME[kind])
            ph = ", ".join("{" + s + "}" for s in slots)
            refer = (f" Refer to the record as {A.KIND_NOUN[kind]} when you use {{REF}}." if "REF" in slots else "")
            iid = f"t01d.wording.{q}.{i:03d}"
            items.append((iid, {"brief": meaning, "slots": list(slots),
                                "rules": rules + [f"Placeholders: exactly {ph}, each once.{refer}",
                                                  f"Style hint: {style}."]}))
            plan[iid] = {"role": "wording", "qform": q, "kind": kind, "slots": list(slots), "held_out": False}
    return items, plan


def build_batch():
    """(TaskBatch, plan): in memory, nothing written."""
    items, plan = _items()
    b = chunker.make_batch("author_wording", FAMILY, items, seed=f"{SEED}|wordings", prompt=A.WORDING_PROMPT,
                           max_items=MAX_ITEMS, forbid_strings=FORBID)
    return b, plan


def check_wording(iid: str, text: str, meta: dict, tid: str = "", psha: str = "", seen=None) -> tuple:
    """Admission of one double-negation wording. -> ((qform, text, slots, task id, prompt sha) | None, [problem])."""
    seen = set() if seen is None else seen
    q = meta["qform"]
    if q not in FORMS:
        return None, [f"{q} is not a double-negation form"]
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip().endswith("?"):
        return None, ["not one question line"]
    text = " ".join(text.split())
    names = [p.name for p in K.placeholders(text)]
    v = []
    if sorted(names) != sorted(meta["slots"]) or K.malformed(text):
        v.append(f"placeholders {names} != {meta['slots']}")
    slots = {s: A.SLOT_KIND[s] for s in meta["slots"]}
    try:
        sk = K.make_skin("tmp", FAMILY, text, slots, kind="wording", register="question", qform=q)
        v += [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    except Exception as e:  # noqa: BLE001
        v.append(str(e)[:120])
    c = negcount.count(text)
    if (c.k_all, c.k_syn) != NEG_PROFILE:
        v.append(f"negcount {(c.k_all, c.k_syn)} != {NEG_PROFILE}")
    v += [f"polarity {p}" for p in POL.form_problems(P.T01, q, text)]
    lit = K.PH_RE.sub(" ", text)
    m = A.WORDING_BANNED.search(lit)
    if m:
        v.append(f"time or day-type word {m.group()!r} (H38)")
    if re.search(r"\boffices?\b", lit, re.I) and meta["kind"] not in ("addon", "cutoff"):
        v.append("'office' outside addon / cutoff forms (H38)")
    if A.LABEL_CHECK.search(lit):
        v.append("label-check form")
    if re.search(r"\b(?:sent|arrived|arrives|arriving)\b", lit, re.I) and q == "yn_dneg_on_time":
        v.append("the response is judged by the day counted as received, not by sending or arriving (G0 v4 12.4)")
    if text.count("?") != 1 or text.lower() in seen or text in FORBID:
        v.append("duplicate, fixture copy or two questions")
    if not v:
        seen.add(text.lower())
    return (q, text, slots, tid, psha), v


def write_tasks(root: Path = ROOT) -> list:
    """Chunks, key, manifest, plan and one self-contained task file per chunk (guarded writers; refuses before A38)."""
    b, plan = build_batch()
    files = dict(b.files())
    files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": "wordings_dneg", "kind": b.kind,
                                                   "plan": plan}, indent=1, sort_keys=True) + "\n"
    tasks = []
    for c in b.chunks:
        tid = c["task_id"]
        ans = str(root / b.answer_path(tid))
        tfile = f"tasks/{tid}.md"
        files[tfile] = A.task_file_text(b, c, ans)
        tasks.append({"task_file": str(root / tfile), "answer_file": ans, "kind": b.kind, "batch": "wordings_dneg",
                      "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                      "audit_allowed_read": [str(root / tfile)], "audit_allowed_write": [ans]})
    paths.write_files(root, files)
    paths.write_json(root / "TASKS.json", {"family": FAMILY, "seed": SEED, "n_tasks": len(tasks), "tasks": tasks,
                                           "g0_sha256": P.T01.G0_SHA256, "round": "redo4 (double-negation wordings)"})
    return tasks


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("plan", "write"))
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        b, plan = build_batch()
        print(json.dumps({"kind": b.kind, "n_items": len(plan), "chunks": [len(c["items"]) for c in b.chunks],
                          "prompt_sha": b.prompt_sha}, indent=1))
        return 0
    print(json.dumps(write_tasks(), indent=1)[:3000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
