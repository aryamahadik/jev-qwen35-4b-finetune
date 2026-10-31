"""transfer/T21/authoring_i1.py: wording authoring for fix iteration 1 (PILOT_VERDICT FIX-1 and FIX-6; G0_SPEC.md v1.3 section 6).

What this module is. The frozen v1 authoring (haiku_author.py: prompts, briefs, WORDING_PLAN, check_wording) is left byte for
byte as it was: freeze_v2 rebuilds pools/ and pools_v2/ from it and must reproduce both, and the Haiku task files the
agents read are sha-pinned. This module holds what a LATER wording round must use, and nothing here has run:
  - the polarity rule (c2_kit.polarity) in the wording admission check, so a wording that reads either way (the contracted
    "isn't this claim capped ...?" frame of PILOT_VERDICT FIX-1) or against its form (a negative predicate under a
    negation) never enters a pool;
  - the yn_not_capped brief WITHOUT the contractions the v1 brief offered as examples (the only n't wording of the 98 split
    both G5-H readers), allowed shape "Is/Does ... not ...?";
  - the yn_double_neg form (FIX-6): positive polarity (yes iff capped), two syntactic negations (negcount k_syn 2). The
    explicit outer frame "is it not the case that" plus one "not" on the cap, never a negative predicate, never a contraction.
A round is: author with these briefs (Haiku never sees a question's answer; the briefs are gold-free), load each answer with
check_wording_i1, add the survivors to the registry (kind question, sem q.t21.<form>), admit them 2/2 by G-LEX, then G13-seed.
That round is NOT run here (no Haiku, no model); until it is, plugin.T21Plugin never draws yn_double_neg (the fallback to
yn_capped keeps the rows label-blind) and G10 double_negation_share stays 0 against its >= 2% bar. Nothing is written here
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
from transfer.T21 import haiku_author as HA  # noqa: E402
from transfer.T21 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

DOUBLE_NEG = P.DOUBLE_NEG_FORM
# what a later round must still author: >= 8 admitted double-negation wordings (PILOT_VERDICT FIX-6) and the one
# yn_not_capped wording the quarantine of 10e86065 left short of the G0 minimum 14; candidates per missing wording as in redo2
NEED = {DOUBLE_NEG: 8, "yn_not_capped": 1}
CANDIDATES_PER_MISSING = 4
QUESTION_MEANING = {DOUBLE_NEG: "asks whether the cap clause limits the liability for the claim, with two negations"}
NEG_EXACT = {**HA.NEG_EXACT, DOUBLE_NEG: (2, 2)}                      # negcount (k_all, k_syn)
CAP_COUNT = {**HA.CAP_COUNT, DOUBLE_NEG: (1, 1)}                      # {CAP_ID} occurrences allowed
BRIEF = {
    DOUBLE_NEG: (
        "A yes/no question with the same meaning as asking whether the cap set by clause {CAP_ID} still limits the "
        "liability for this claim (yes exactly when it does), asked with two negations.",
        "Use exactly TWO negation cues, both the word 'not': the explicit frame 'is it not the case that' (or 'is it not "
        "true that') and one more 'not' on 'capped' or 'limit' (for example 'is it not the case that this claim is not "
        "capped by clause {CAP_ID}?'). Never n't or a contraction, never 'no', 'never' or 'without', and never a negative "
        "predicate (uncapped, unlimited, free of, lifted, removed, set aside). Write {CAP_ID} exactly once."),
    "yn_not_capped": (
        HA.WORDING_BRIEF["yn_not_capped"][0],
        "Use exactly ONE negation, the word 'not' on the main verb ('does ... not limit' or 'is ... not capped'). Never a "
        "contraction: no n't, so never 'isn't', 'doesn't' or 'aren't', and never an opening such as 'Isn't this claim ...?'. "
        "No other negation cue, and never 'uncapped' or 'free of'. Write {CAP_ID} exactly once."),
}


def polarity_problems(qform: str, text: str) -> list:
    """c2_kit.polarity on a wording of `qform` with T21's lexicon (P1-P3; P4 is off: 'Is/Does ... not ...?' is the allowed
    shape). [] when the wording reads with its form's declared polarity."""
    return polarity.form_problems(P.T21Plugin, qform, text)


def contraction_problems(text: str) -> list:
    """No n't anywhere (the v1 lint left it to negcount's count, which lets one contraction through)."""
    return ["contraction n't"] if re.search(r"n['’]t\b", text) else []


def check_wording_i1(iid, text, meta, tid, psha, seen) -> tuple:
    """haiku_author.check_wording plus the polarity rule, the contraction ban and the double-negation form. -> ((qform,
    text, task id, prompt sha), problems); an empty problem list admits the text to the G-LEX read."""
    q = meta["qform"]
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip().endswith("?"):
        return None, ["not one question line"]
    text = " ".join(text.split())
    v = []
    phs = [p.name for p in K.placeholders(text)]
    if set(phs) - {"CAP_ID"}:
        v.append(f"placeholders {sorted(set(phs) - {'CAP_ID'})}")
    lo, hi = CAP_COUNT[q]
    if not lo <= phs.count("CAP_ID") <= hi:
        v.append(f"{{CAP_ID}} {phs.count('CAP_ID')}x, allowed {lo}-{hi}")
    if "CAP_ID" in phs and not re.search(r"\bclause \{CAP_ID\}", text):
        v.append("{CAP_ID} not right after 'clause'")
    slots = {"CAP_ID": "id"} if "CAP_ID" in phs else {}
    try:
        sk = K.make_skin("tmp", HA.FAMILY, text, slots, kind="wording", register="question", qform=q)
        v += [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    c = negcount.count(K.PH_RE.sub("9.1", text))
    if (c.k_all, c.k_syn) != NEG_EXACT[q]:
        v.append(f"negcount {(c.k_all, c.k_syn)} != {NEG_EXACT[q]}")
    v += contraction_problems(text)
    v += [f"polarity {p}" for p in polarity_problems(q, text)]
    ws = HA._words(text)
    low = text.lower()
    v += [f"banned word {w!r}" for w in HA._label_hits(text, HA.WORDING_BANNED)]
    tc = sorted(ws & HA.TYPE_CAUSE_WORDS)
    if tc:
        v.append(f"type or cause words {tc}")
    if "claim" not in ws:
        v.append("must ask about this claim")
    if ws & {"cover", "covers", "covered", "describe", "describes", "described"}:
        v.append("asks whether a clause covers the claim")
    if q in (DOUBLE_NEG, "yn_capped", "yn_not_capped") and ("uncapped" in ws or "free of" in low):
        v.append("'uncapped' / 'free of' belong to the complement forms")
    if q == "yn_uncapped" and "uncapped" not in ws:
        v.append("yn_uncapped says 'uncapped'")
    if q == "yn_free_of" and "free of" not in low:
        v.append("yn_free_of says 'free of'")
    if q in (DOUBLE_NEG, "yn_capped", "yn_not_capped") and not ws & {"cap", "capped", "limit", "limits", "limited"}:
        v.append("names the cap or its limit")
    if q == DOUBLE_NEG and not re.search(r"\bit not (?:the case|true) that\b", low):
        v.append("yn_double_neg opens with the explicit frame 'it not the case that' / 'it not true that'")
    if ws & {"decides", "deciding", "decide"}:
        v.append("a yes/no wording asks about the deciding clause")
    if low in seen or text in HA.QSTRINGS:
        v.append("duplicate or fixture copy")
    if not 6 <= len(text.split()) <= 34:
        v.append("length")
    if not v:
        seen.add(low)
    return (q, text, tid, psha), v


def wording_items(need: dict | None = None, per_missing: int = CANDIDATES_PER_MISSING) -> tuple:
    """Authoring items for the round, in haiku_author._wording_items' shape: ([(item id, payload)], {item id: plan}). The
    payload is gold-free (a meaning, a placeholder rule and a style hint), exactly like v1."""
    items, plan = [], {}
    for q, n in sorted((need or NEED).items()):
        meaning, rule = BRIEF[q]
        lo, _hi = CAP_COUNT[q]
        for i in range(n * per_missing):
            iid = f"t21i1.wording.{q}.{i:03d}"
            items.append((iid, {"brief": meaning,
                                "slots": {"CAP_ID": "the cap clause's number (exactly once)" if lo else
                                          "the cap clause's number (at most once)"},
                                "rules": [rule, f"Style hint: {HA.STYLES[i % len(HA.STYLES)]}."]}))
            plan[iid] = {"role": "wording", "qform": q, "held_out": False}
    return items, plan
