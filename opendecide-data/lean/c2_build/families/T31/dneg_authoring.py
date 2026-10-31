"""families/T31/dneg_authoring.py: the F07 top-up brief and admission check for the two double-negation question forms
(PILOT_VERDICT F07; C2_DATA_SPEC 3.0 "double negation on at least 2% of yes/no rows"; G0 v1.2 M9 / M12 / section 7).

Why. The frozen wordings (pools_v2) have k_syn 0 or 1 only, so the pilot's double_negation_share was 0.0% (bar >= 2%).
G0 v1.2 adds the forms
  yn_holder_dneg  "does CANDIDATE hold the accountable (A) role?", worded with two cancelling negations (yes = holds)
  yn_agent_dneg   "may REQ_AGENT use REQ_SCOPE?", worded with two cancelling negations (yes = may)
The plugin draws them (4% of base specs each) only while the lexicon admits at least one polarity-clean wording of
them (T31.available); until then they fall back to yn_holder / yn_agent_ok and the double-negation share is 0%.

What is here (nothing runs Haiku; nothing is written):
  * prompt(track), items(...)    the gold-free authoring brief in the shape of haiku_author's wording tasks
  * wording_problems(q, text)    the admission check of an answer: shape (one question, 6-30 words, one {CANDIDATE} /
                                 {REQ_AGENT} + {REQ_SCOPE}, optional {REQ_ID}), the negation profile (k_syn 2), the
                                 c2_kit.polarity rule (P1-P4: a syntactic negation over a negative predicate such as
                                 "bar" or "block" reads with the REVERSE meaning, the T35 pilot's 3 wrong golds; a
                                 contracted frame reads either way), G-SL (wording role), no escalate word
  * build_batches()              the chunker batches, in memory (guards run inside make_batch)
OPEN (needs Haiku, after this iteration): author them from this brief, run the G-LEX 2/2 extraction on the admitted
texts (sem q.t31.yn_holder_dneg / q.t31.yn_agent_dneg), G13-seed on the new pieces, add them to a pool freeze
(freeze_v2 pattern), then re-pilot. Accept a wording only if wording_problems() is empty.
"""
from __future__ import annotations

import sys
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import gsl, paths  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
import negcount  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402
from families.T31 import plugin as P  # noqa: E402

F = "T31"
FORMS = ("yn_holder_dneg", "yn_agent_dneg")
PER_FORM = 10                                  # candidates per form (>= 6 admitted are needed; spare for the lint)
NEG_PROFILE = (2, 2)                           # (k_syn, k_all): exactly two syntactic negations, no other cue
SEED = "t31-dneg-r3"
EXPLICIT_OUTER = ("Is it not the case that", "Is it not true that", "Is it not correct that", "Is it not so that")

MEANING = {
    "yn_holder_dneg": (
        "Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = "
        "{CANDIDATE} holds it). Word it with exactly two negations that cancel: start with one of the explicit outer "
        "frames 'Is it not the case that', 'Is it not true that' or 'Is it not correct that', and put a second 'not' "
        "inside the embedded statement, directly on the verb or on 'the accountable approver', for example 'Is it not "
        "the case that {CANDIDATE} was not the accountable approver?'. The second 'not' negates the plain statement "
        "that {CANDIDATE} holds the role; the question as a whole asks whether that is so.",
        ("{CANDIDATE}",)),
    "yn_agent_dneg": (
        "Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request (yes = it may). Word it with exactly "
        "two negations that cancel: start with one of the explicit outer frames 'Is it not the case that', 'Is it not "
        "true that' or 'Is it not correct that', and put a second 'not' inside the embedded statement on a permission "
        "word, for example 'Is it not the case that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the "
        "request?'. The second 'not' negates the plain statement that {REQ_AGENT} may use the scope.",
        ("{REQ_AGENT}", "{REQ_SCOPE}")),
}
RULES = ["exactly two 'not': the outer frame 'Is it not the case/true/correct that' and one 'not' inside the statement",
         "the second 'not' sits on a PERMISSION or ROLE word (permitted, allowed, entitled, the holder, the approver)",
         "never a blocking, excluding or lacking word (bar, block, deny, lack, forbid, prevent, exclude, skip, "
         "withhold, refuse), never a contracted negative (isn't, doesn't, wasn't, aren't)"]
QUESTION_SEM_MEANING = {
    "yn_holder_dneg": "asks, with two cancelling negations, whether the named person holds the accountable (A) role for "
                      "the request at its time (yes = the person holds it)",
    "yn_agent_dneg": "asks, with two cancelling negations, whether the agent is permitted to use the scope at the time "
                     "of the request (yes = it is permitted)",
}


def prompt(track: str) -> str:
    """The authoring prompt: haiku_author's wording prompt with its negation rule (6) replaced by the two-negation rule."""
    base = HA._wording_prompt(track)
    lines = base.split("\n")
    i = next(k for k, ln in enumerate(lines) if ln.startswith("6. Negation only where the item asks for it"))
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith("7. "))
    new = ["6. Negation exactly as the item asks (two cancelling 'not' words with the explicit outer frame the item "
           "names). No other negation word anywhere: none of " + ", ".join(
               x for x in HA.NEGATIONS if x not in ("not",)) + "; no contracted negatives."]
    return "\n".join(lines[:i] + new + lines[j:])


def items(qforms=FORMS, per_form: int = PER_FORM) -> list:
    out = []
    for q in qforms:
        meaning, required = MEANING[q]
        for i in range(per_form):
            slots = {r.strip("{}"): "required, exactly once" for r in required}
            slots["REQ_ID"] = "optional, at most once" if i % 2 == 0 else "leave it out"
            out.append((f"wording|{q}|{i:03d}", {
                "brief": f"Meaning: {meaning} Style: {HA.WORDING_STYLES[(i * 3 + len(q)) % len(HA.WORDING_STYLES)]}.",
                "slots": slots, "rules": list(RULES)}))
    return out


def wording_problems(qform: str, text: str, *, need_req_id: bool | None = None) -> list:
    """Problems of one candidate wording ([] = admissible; G-LEX 2/2 and G13-seed still follow)."""
    if qform not in FORMS:
        return [f"{qform} is not a double-negation form"]
    if not isinstance(text, str) or not text.strip():
        return ["empty"]
    probs = []
    text = text.strip()
    if "\n" in text or not text.endswith("?") or text.count("?") != 1:
        probs.append("one question on one line, ending with '?'")
    n = len(text.split())
    if not 6 <= n <= 30:
        probs.append(f"{n} words (6-30)")
    counts = HA._phs(text)
    need = [r.strip("{}") for r in MEANING[qform][1]]
    if any(counts.get(k) != 1 for k in need) or counts.get("REQ_ID", 0) > 1 or set(counts) - set(need) - {"REQ_ID"}:
        probs.append(f"placeholders {counts} (need {need} once, REQ_ID at most once)")
    if any(p.mod for p in K.placeholders(text)):
        probs.append("grammar helper inside a question")
    if not any(text.startswith(f) for f in EXPLICIT_OUTER):
        probs.append(f"must open with an explicit outer frame {EXPLICIT_OUTER}")
    low = text.lower()
    if any(w in low for w in P.T31.LABEL_WORDS):
        probs.append("names the abstain option or a gold label")
    c = negcount.count(K.PH_RE.sub("X", text))
    if (c.k_syn, c.k_all) != NEG_PROFILE:
        probs.append(f"negation counts (k_syn {c.k_syn}, k_all {c.k_all}), need {NEG_PROFILE}")
    probs += [f"polarity: {p}" for p in POL.form_problems(P.T31, qform, text)]
    if probs:
        return probs
    decl = {k: ("name" if k == "CANDIDATE" else "id") for k in counts}
    try:
        sk = K.make_skin("T31-DNEG-CAND", F, text, decl, kind="wording", register="question", qform=qform)
    except K.RenderError as e:
        return [f"wording: {e}"]
    return [f"{v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=P.T31.LABEL_WORDS,
                                                                exceptions=P.T31.GSL_EXCEPTIONS,
                                                                name_allow=P.T31.NAME_ALLOW)]


def build_batches() -> list:
    """[(info, TaskBatch)] in memory: one task per track (appr: yn_holder_dneg; agent: yn_agent_dneg)."""
    out = []
    for track, q in (("appr", "yn_holder_dneg"), ("agent", "yn_agent_dneg")):
        b = CH.make_batch("author_wording", F, items((q,)), seed=f"{SEED}|{track}", prompt=prompt(track),
                          forbid_strings=HA.FORBID_WORDING)
        out.append(({"task": f"wording-dneg-{track}", "qform": q, "track": track}, b))
    return out


if __name__ == "__main__":
    for info, b in build_batches():
        print(info, b.batch_id, len(b.chunks), sum(len(c["items"]) for c in b.chunks), "items;",
              "nothing written" if not paths.a38_frozen() else "check only")
