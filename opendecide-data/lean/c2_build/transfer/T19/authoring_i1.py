"""transfer/T19/authoring_i1.py: wording authoring for fix iteration 1 (pilot G10 double_negation_share; G0_SPEC.md v1.2 section 6).

What this module is. The frozen v1 authoring (haiku_author.py: prompts, briefs, WORDING_PLAN, check_wording) is left byte for
byte as it was: freeze.py / freeze_v2.py / redo2 / redo3 rebuild pools/ and pools_v2/ from it and must reproduce both, and the
Haiku task files the agents read are sha-pinned. This module holds what a LATER wording round must use, and nothing here has run:
  - the yn_dneg form (plugin.DNEG_FORM): positive polarity (yes iff compliant), two syntactic negations (negcount k_syn 2). It
    asks the compliance question behind the explicit outer frame "is it not the case that" plus one "not" on "compliant": never a
    negative predicate, never a contraction (the T35 pilot's three wrong golds were double negations over a negative predicate);
  - the polarity rule (c2_kit.polarity) in the wording admission check, so a wording that reads either way (a contracted frame)
    or against its form never enters a pool;
  - the yn_not_compliant brief WITHOUT the contractions the v1 brief offered as examples ("isn't ... in compliance").
A round is: author with these briefs (Haiku never sees a question's answer or a row; the briefs are gold-free), load each answer
with check_wording_i1, declare the sem (declare_forms) and add the survivors to the registry (kind question, sem
q.t19.yn_dneg), admit them 2/2 by G-LEX, then G13-seed; the admitted wordings join the context next to the frozen pools_v2 ones
(pilot_loaders._t19 builds one wording skin per admitted form). That round is NOT run here (no Haiku, no model); until it is,
plugin.T19Plugin never draws yn_dneg (dneg_ok is False: the form falls back to yn_compliant, label-blind: pool state only) and G10
double_negation_share stays 0 against its >= 2% bar. A yn_dneg row pairs with yn_not_compliant only (one negation cue more or
less: the syntactic complement). The G5-H re-read of this family needs >= 10 double-negation rows. Nothing is written here
(A37 f); no label is set.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, polarity  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

DNEG = P.DNEG_FORM
# what a later round must author: >= 8 admitted double-negation wordings (the frozen forms hold 14 of every other yes/no form;
# 2 wordings of 6 = 1 / 30 per 1,000 rows at most 2% each, spec 3.0), candidates per wording as in redo2
NEED = {DNEG: 10}
CANDIDATES_PER_MISSING = 4
QUESTION_MEANING = {DNEG: "asks whether the site is compliant with the checklist on the audit date, with two negations"}
NEG_EXACT = {**HA.NEG_EXACT, DNEG: (2, 2)}                      # negcount (k_all, k_syn)
EXPLICIT_FRAME = re.compile(r"\bit not (?:the case|true) that\b", re.I)
BRIEF = {
    DNEG: (
        "A yes/no question with the same meaning as asking whether the site is compliant with its checklist on the audit date "
        "(yes exactly when every applying control passes), asked with two negations that cancel.",
        "Use exactly TWO negation cues, both the word 'not': the explicit frame 'is it not the case that' (or 'is it not true "
        "that') and one more 'not' on 'compliant' (for example 'is it not the case that {SITE} is not compliant with its "
        "checklist on the audit date?'). Never n't or a contraction, never 'no', 'never' or 'without', and never a negative "
        "predicate (non-compliant, out of compliance, in breach, fail to, lack)."),
    "yn_not_compliant": (
        HA.WORDING_BRIEF["yn_not_compliant"][0],
        "Use exactly ONE negation, the word 'not' on the main verb or adjective ('is ... not compliant', 'does ... not meet'). "
        "Never a contraction: no n't, so never 'isn't', 'doesn't' or 'aren't', and never an opening such as 'Isn't the site "
        "compliant ...?'. No other negation cue."),
}


def declare_forms(reg) -> None:
    """Declare the yn_dneg question sem in a registry that does not hold it (the frozen pools_v2 lexicon predates the form)."""
    sem = question_sem(HA.FAMILY, DNEG)
    if sem not in getattr(reg, "sems", {}):
        reg.declare(sem, "question", QUESTION_MEANING[DNEG])


def polarity_problems(qform: str, text: str) -> list:
    """c2_kit.polarity on a wording of `qform` with T19's lexicon (P1-P3; P4 is off: 'Is ... not ...?' is the allowed shape of
    yn_not_compliant). [] when the wording reads with its form's declared polarity."""
    return polarity.form_problems(P.T19Plugin, qform, text)


def contraction_problems(text: str) -> list:
    """No n't anywhere (the v1 lint left it to negcount's count, which lets one contraction through)."""
    return ["contraction n't"] if re.search(r"n['’]t\b", text) else []


def check_wording_i1(iid, text, meta, tid, psha, seen) -> tuple:
    """haiku_author.check_wording plus the polarity rule, the contraction ban and the double-negation form. -> ((qform, text,
    task id, prompt sha), problems); an empty problem list admits the text to the G-LEX read."""
    q = meta["qform"]
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip().endswith("?"):
        return None, ["not one question line"]
    text = " ".join(text.split())
    v = []
    try:
        sk = K.make_skin("tmp", HA.FAMILY, text, {"SITE": "name"}, kind="wording", register="question", qform=q)
        v += [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    c = negcount.count(K.PH_RE.sub("the site", text))
    if (c.k_all, c.k_syn) != NEG_EXACT[q]:
        v.append(f"negcount {(c.k_all, c.k_syn)} != {NEG_EXACT[q]}")
    v += contraction_problems(text)
    v += [f"polarity {p}" for p in polarity_problems(q, text)]
    low = text.lower()
    if "checklist" not in low or "audit date" not in low:
        v.append("must name the checklist and the audit date")
    if q == DNEG and not EXPLICIT_FRAME.search(low):
        v.append("yn_dneg opens with the explicit frame 'it not the case that' / 'it not true that'")
    if q == DNEG and re.search(r"non-?compliant|out of compliance|in breach|fail(?:s|ed)? to|\black", low):
        v.append("yn_dneg never uses a negative predicate")
    if low in seen or text in HA.QSTRINGS:
        v.append("duplicate or fixture copy")
    if not 6 <= len(text.split()) <= 34:
        v.append("length")
    if not v:
        seen.add(low)
    return (q, text, tid, psha), v


def wording_items(need: dict | None = None, per_missing: int = CANDIDATES_PER_MISSING) -> tuple:
    """Authoring items for the round, in haiku_author._wording_items' shape: ([(item id, payload)], {item id: plan}). The payload
    is gold-free (a meaning, a placeholder rule and a style hint), exactly like v1."""
    items, plan = [], {}
    for q, n in sorted((need or NEED).items()):
        meaning, rule = BRIEF[q]
        for i in range(n * per_missing):
            iid = f"t19i1.wording.{q}.{i:03d}"
            items.append((iid, {"brief": meaning, "slots": {"SITE": "the site's name (exactly once)"},
                                "rules": [rule, f"Style hint: {HA.STYLES[i % len(HA.STYLES)]}."]}))
            plan[iid] = {"role": "wording", "qform": q, "held_out": False}
    return items, plan
