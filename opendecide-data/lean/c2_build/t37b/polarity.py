"""t37b/polarity.py: T37b polarity program A, built on negcount (XF02; C2_DATA_SPEC 3.18 "Checks"; G0 S6-S9).

classify_a(base_q, partner_q, kind, entry, frames) -> ("opposite" | "same" | None, problems)

Program A splits the base question into (fronted prefix, first auxiliary, subject, rest) with the entry's subject
rule (a regex; for hotpotqa "BOTH": the anchor rule, the subject is the text between the auxiliary and the one
" both "; G0 amendment A1-2), builds the EXACT partner strings a kind allows, and reads both questions with c_src/common/negcount.py (counts,
entry names, anchors). None means "not proven": the pair is dropped. A pair enters T37b only when program A and
program B (polarity_b.py, an independent token-level reading) both return the planned relation.

  syntactic       partner == "<frame>[, <prefix>,] <subject> <aux> not|n't <rest>?" ("can": can not / cannot / can't);
                  base k_all = 0; partner k_all = k_syn = base + 1; scope: no quantifier, modal, negation or
                  subordinator in the prefix or subject, the auxiliary is do / does / did / is / are / was / were /
                  has / have / had / can, and the rest holds no modal and only wide-scope-safe quantifiers (any,
                  anything, anyone, anybody, both, either, always; never all / every / each: G0 H28)
  implicit        a do-question whose rest starts with the entry's main verb; partner == "<Aux> <subject> fail to
                  <rest>?" or, for have / contain / include, "<Aux> <subject> lack <rest minus the verb>?"; partner
                  k_all = 1, k_syn = 0, entry fail to / lack; the base holds no negation, quantifier, modal,
                  collective or comparative word
  antonym         k_all and k_syn unchanged; the partner is the base with exactly one closed-list phrase replaced by
                  its antonym (string level)
  option_framing  k_all and k_syn unchanged; the partner is the base rewritten by the entry's closed rule (string level)
  equiv           the same negcount entries (so the same k_all and k_syn), the same quantifiers and modals, the same
                  anchors (quoted spans, numbers, capitalised names), no truth frame, no closed antonym introduced
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import paths  # noqa: E402,F401  (puts c_src/common on sys.path)
import negcount  # noqa: E402

from t37b import sources as SRC  # noqa: E402

AUX_ANY = ("does", "do", "did", "is", "are", "was", "were", "am", "has", "have", "had", "can", "could", "will", "would",
           "shall", "should", "may", "might", "must")
AUX_OK = frozenset({"do", "does", "did", "is", "are", "was", "were", "has", "have", "had", "can"})
DO_AUX = frozenset({"do", "does", "did"})
NT = {"does": "doesn't", "do": "don't", "did": "didn't", "is": "isn't", "are": "aren't", "was": "wasn't",
      "were": "weren't", "has": "hasn't", "have": "haven't", "had": "hadn't"}
QUANT = frozenset({"all", "every", "each", "both", "any", "some", "either", "neither", "only", "most", "many", "much",
                   "few", "several", "least", "more", "less", "fewer", "always", "sometimes", "usually", "often",
                   "everything", "everyone", "everybody", "anything", "anyone", "anybody", "something", "someone",
                   "somebody", "none", "nobody", "nothing", "never", "just", "exactly", "half", "majority"})
# Quantifiers allowed after the inserted "not": only those whose not(...) reading is the one natural reading (G0 H28).
# all / every / each (and everything / everyone / everybody) are refused: "does not support all X" also reads all-not.
AFTER_OK = frozenset({"any", "both", "either", "always", "anything", "anyone", "anybody"})
MODAL = frozenset({"must", "may", "might", "should", "shall", "could", "would", "will", "wo", "ought", "need",
                   "needs"})
SUBORD = frozenset({"that", "which", "who", "whom", "whose", "whether", "if", "because", "when", "where", "while",
                    "unless", "although", "though", "since", "until", "before", "after", "than"})
COLLECTIVE = frozenset({"same", "different", "both", "together", "each", "other", "than", "either", "neither",
                        "between", "more", "less", "older", "younger", "larger", "smaller", "longer", "shorter",
                        "higher", "lower", "earlier", "later", "first", "last"})
_FIRST_AUX = re.compile(r"\b(" + "|".join(AUX_ANY) + r")\b", re.I)
_QUOTED = re.compile(r"\"[^\"\n]*\"|“[^”\n]*”")
_DIGITS = re.compile(r"\d+(?:[.,:/]\d+)*")


def _words(text: str) -> list:
    """negcount tokens without punctuation, with "ca" read as "can" (can't) and "wo" as "will" (won't)."""
    out = []
    for t in negcount.tokenize(text):
        if re.match(r"[\w']", t.low):
            out.append({"ca": "can", "wo": "will"}.get(t.low, t.low))
    return out


def frame_of(partner_q: str, frames: tuple) -> str | None:
    """The truth frame the partner starts with (followed by a space or ", "), longest first; None if none."""
    for f in sorted(frames, key=len, reverse=True):
        if partner_q.startswith(f + " ") or partner_q.startswith(f + ", "):
            return f
    return None


def split_question(base_q: str, entry):
    """(prefix, aux as written, subject, rest) of a yes/no question by the entry's subject rule, or None.
    prefix is "" or a fronted phrase ending in ", "; rest is the text between the subject and the final "?"."""
    if not entry.subject or not base_q.endswith("?") or base_q.count("?") != 1:
        return None
    m = _FIRST_AUX.search(base_q)
    if not m:
        return None
    prefix, aux = base_q[:m.start()], m.group(0)
    if prefix and (not prefix.endswith(", ") or not prefix[0].isupper()):
        return None
    if not prefix and not aux[0].isupper():
        return None
    after = base_q[m.end():]
    if not after.startswith(" "):
        return None
    after = after[1:-1]
    if entry.subject == "BOTH":
        sp = _split_both(after)
        return None if sp is None else (prefix, aux) + sp
    sm = re.compile(entry.subject).match(after)
    if not sm or not after[sm.end():].startswith(" "):
        return None
    rest = after[sm.end() + 1:]
    if not rest:
        return None
    return prefix, aux, sm.group(0), rest


def _split_both(after: str):
    """(subject, rest) of the text after the first auxiliary for a "BOTH" entry (hotpotqa; G0 amendment A1-2, fix F2).
    The anchor rule: the question holds exactly one " both "; the subject is everything between the auxiliary and
    that " both " and the rest starts with "both" ("Are Hottonia and Delphinium both genera of plants?" -> subject
    "Hottonia and Delphinium", rest "both genera of plants"). Every other shape (no " both ", two of them, "the same",
    "Do X <verb>", "Is X a ...") is refused. The old capital-run rule cut titles with lowercase words or digits
    mid-name ("Are BLT cocktail and Tamango both ..." -> subject "BLT")."""
    if after.count(" both ") != 1:
        return None
    i = after.index(" both ")
    subj = after[:i]
    if not subj or subj != subj.strip() or after[i + 1:].strip() == "both":
        return None
    return subj, after[i + 1:]


def syntactic_targets(base_q: str, entry, frame: str) -> set:
    sp = split_question(base_q, entry)
    if sp is None:
        return set()
    prefix, aux, subj, rest = sp
    a = aux.lower()
    if a not in AUX_OK:
        return set()
    lead = f", {prefix[0].lower()}{prefix[1:-2]}," if prefix else ""
    negs = ["can not", "cannot", "can't"] if a == "can" else [f"{a} not", NT[a]]
    return {f"{frame}{lead} {subj} {n} {rest}?" for n in negs}


def implicit_targets(base_q: str, entry) -> set:
    sp = split_question(base_q, entry)
    if sp is None or not entry.verb:
        return set()
    prefix, aux, subj, rest = sp
    if aux.lower() not in DO_AUX or not re.match(re.escape(entry.verb) + r"\b", rest):
        return set()
    out = {f"{prefix}{aux} {subj} fail to {rest}?"}
    if entry.verb in SRC.LACK_VERBS:
        out.add(f"{prefix}{aux} {subj} lack{rest[len(entry.verb):]}?")
    return out


def anchors(text: str) -> dict:
    """Facts a paraphrase must keep: quoted spans, digit runs and capitalised words after the first word."""
    words = re.findall(r"[A-Za-z][\w'-]*", _QUOTED.sub(" ", text))
    caps = [w for w in words[1:] if w[0].isupper()]
    return {"quoted": sorted(_QUOTED.findall(text)), "digits": sorted(_DIGITS.findall(text)), "caps": sorted(caps)}


def _counts_equal(ka, kb) -> bool:
    return (ka.k_all, ka.k_syn) == (kb.k_all, kb.k_syn) and \
        sorted(m.entry for m in ka.matches) == sorted(m.entry for m in kb.matches)


def _one_replace(base_q: str, partner_q: str, old: str, new: str) -> bool:
    rx = re.compile(r"(?<![\w-])" + re.escape(old) + r"(?![\w-])")
    hits = list(rx.finditer(base_q))
    if len(hits) != 1:
        return False
    m = hits[0]
    return base_q[:m.start()] + new + base_q[m.end():] == partner_q


def _syntactic_scope(base_q: str, entry) -> list:
    sp = split_question(base_q, entry)
    if sp is None:
        return ["the base does not split into prefix, auxiliary, subject and rest"]
    prefix, aux, subj, rest = sp
    probs = []
    if aux.lower() not in AUX_OK:
        probs.append(f"auxiliary {aux!r} does not take an exact 'not'")
    front = set(_words(prefix + " " + subj)) & (QUANT | MODAL | SUBORD | set(negcount.L_CORE))
    if front:
        probs.append(f"scope: {sorted(front)} in the prefix or subject")
    back = set(_words(rest))
    if (back & QUANT) - AFTER_OK or back & MODAL:
        probs.append(f"scope: {sorted(((back & QUANT) - AFTER_OK) | (back & MODAL))} after the 'not'")
    return probs


# ------------------------------------------------------------------------------------------------ feasibility

def base_feasible_a(kind: str, base_q: str, entry) -> bool:
    """Static checks on the base question alone (before any partner exists): can this kind be written at all?"""
    if kind not in entry.kinds:
        return False
    if kind == "equiv":
        return True
    if kind == "antonym":
        return any(len(re.findall(r"(?<![\w-])" + re.escape(p) + r"(?![\w-])", base_q)) == 1 for p, _ in entry.antonyms)
    if kind == "option_framing":
        rx, _fn = SRC.OPTION_FRAMES[entry.option_frame]
        return len(re.findall(rx, base_q)) == 1
    if negcount.count(base_q).k_all:
        return False
    if kind == "syntactic":
        return bool(syntactic_targets(base_q, entry, "F")) and not _syntactic_scope(base_q, entry)
    if kind == "implicit":
        return bool(implicit_targets(base_q, entry)) and not (set(_words(base_q)) & (QUANT | MODAL | COLLECTIVE))
    return False


# ------------------------------------------------------------------------------------------------ classify

def classify_a(base_q: str, partner_q: str, kind: str, entry, frames: tuple = SRC.FRAMES_TRAIN) -> tuple:
    if kind not in SRC.KINDS:
        return None, [f"unknown kind {kind!r}"]
    if not partner_q or "\n" in partner_q or not partner_q.endswith("?") or partner_q.count("?") != 1:
        return None, ["the partner is not one question on one line ending in '?'"]
    if partner_q == base_q:
        return None, ["the partner equals the base"]
    ka, kb = negcount.count(base_q), negcount.count(partner_q)
    probs = []
    if kind == "syntactic":
        f = frame_of(partner_q, frames)
        if f is None:
            return None, ["no closed truth frame at the start"]
        if ka.k_all:
            probs.append("the base already holds a negation cue")
        if partner_q not in syntactic_targets(base_q, entry, f):
            probs.append("the partner is not '<frame> <prefix> <subject> <aux> not <rest>?' for this base")
        if (kb.k_all - ka.k_all, kb.k_syn - ka.k_syn) != (1, 1):
            probs.append(f"negcount: k_all {ka.k_all}->{kb.k_all}, k_syn {ka.k_syn}->{kb.k_syn} (need +1 / +1)")
        probs += _syntactic_scope(base_q, entry)
        return (None, probs) if probs else ("opposite", [])
    if kind == "implicit":
        if ka.k_all:
            probs.append("the base already holds a negation cue")
        if set(_words(base_q)) & (QUANT | MODAL | COLLECTIVE):
            probs.append(f"scope: the base holds {sorted(set(_words(base_q)) & (QUANT | MODAL | COLLECTIVE))}")
        if partner_q not in implicit_targets(base_q, entry):
            probs.append("the partner is not the base with 'fail to' before (or 'lack' for) the entry's main verb")
        if (kb.k_all - ka.k_all, kb.k_syn - ka.k_syn) != (1, 0) or \
                not any(m.entry in ("fail to", "lack") for m in kb.matches):
            probs.append(f"negcount: k_all {ka.k_all}->{kb.k_all}, k_syn {ka.k_syn}->{kb.k_syn} (need +1 / +0, an "
                         "implicit cue)")
        return (None, probs) if probs else ("opposite", [])
    if kind == "antonym":
        if not _counts_equal(ka, kb):
            return None, ["an antonym partner changes the negation cues"]
        if not any(_one_replace(base_q, partner_q, p, a) for p, a in entry.antonyms):
            return None, ["the partner is not the base with one closed-list antonym swapped in"]
        return "opposite", []
    if kind == "option_framing":
        if not _counts_equal(ka, kb):
            return None, ["an option-framing partner changes the negation cues"]
        rx, fn = SRC.OPTION_FRAMES[entry.option_frame]
        if len(re.findall(rx, base_q)) != 1 or re.sub(rx, fn, base_q) != partner_q:
            return None, ["the partner is not the base rewritten by the entry's option-framing rule"]
        return "opposite", []
    # equiv
    if not _counts_equal(ka, kb):
        probs.append("a paraphrase changes the negation cues")
    wa, wp = Counter(_words(base_q)), Counter(_words(partner_q))
    if Counter({w: c for w, c in wa.items() if w in QUANT}) != Counter({w: c for w, c in wp.items() if w in QUANT}):
        probs.append("a paraphrase changes the quantifiers")
    if Counter({w: c for w, c in wa.items() if w in MODAL}) != Counter({w: c for w, c in wp.items() if w in MODAL}):
        probs.append("a paraphrase changes the modals")
    if anchors(base_q) != anchors(partner_q):
        probs.append("a paraphrase changes a quoted span, number or name")
    all_frames = SRC.FRAMES_TRAIN + SRC.FRAMES_DEV
    if frame_of(partner_q, all_frames) and not frame_of(base_q, all_frames):
        probs.append("a paraphrase adds a truth frame")
    for _p, a in entry.antonyms:
        rx = re.compile(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", re.I)
        if len(rx.findall(partner_q)) > len(rx.findall(base_q)):
            probs.append(f"a paraphrase introduces the antonym {a!r}")
    return (None, probs) if probs else ("same", [])
