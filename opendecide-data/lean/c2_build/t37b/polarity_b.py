"""t37b/polarity_b.py: T37b polarity program B, an independent word-level edit-script reader (G0 S7).

classify_b(base_q, partner_q, kind, entry, frames) -> ("opposite" | "same" | None, problems)

Written from G0_LITE_T37B.md, not from polarity.py, and sharing no code with it: B does not import negcount or
polarity.py. It has its own tokenizer (contractions expanded: isn't -> is not, can't / cannot -> can not, won't ->
will not; quoted spans kept as one token), its own word lists and its own subject reader, and it compares TOKEN
SEQUENCES (expected token templates and difflib opcodes) instead of counting cues:

  syntactic       partner tokens = frame tokens + the base with its first auxiliary moved right after the subject
                  (the entry's subject rule, coded here: a regex, or for hotpotqa the words up to the one "both"; G0
                  amendment A1-2) and "not" right after it; nothing scope-bearing (quantifier, modal, negation, subordinator) before the "not", only
                  wide-scope-safe quantifiers after it
  implicit        a do-question whose subject is followed by the entry's main verb: partner tokens = the base with
                  ["fail", "to"] inserted right before that verb, or the verb (have / contain / include) -> "lack"; the
                  base has no negation, quantifier, modal, collective or comparative word
  antonym         the base with exactly one occurrence of a closed phrase replaced by its antonym (token level)
  option_framing  exactly one replace opcode "1" <-> "2" right after "statement" (the comve rule, coded here)
  equiv           the same negation words, quantifiers and modals (as multisets), the same quoted spans, digit runs
                  and capitalised names, no frame or implicit cue added, no closed antonym introduced
"""
from __future__ import annotations

import difflib
import re
from collections import Counter

NEG_B = frozenset({"not", "no", "never", "none", "nobody", "nothing", "nowhere", "neither", "nor", "without",
                   "lack", "lacks", "lacked", "lacking", "fail", "fails", "failed", "failing", "refuse", "refuses",
                   "refused", "deny", "denies", "denied", "unless", "except", "hardly", "scarcely", "barely", "few",
                   "false", "neglect", "omit", "decline", "prevent"})
AUX_FIRST = frozenset({"do", "does", "did", "is", "are", "was", "were", "am", "be", "been", "has", "have", "had", "can",
                       "could", "will", "would", "shall", "should", "may", "might", "must"})
AUX_NEG_OK = frozenset({"do", "does", "did", "is", "are", "was", "were", "has", "have", "had", "can"})
QUANT_B = frozenset({"all", "every", "each", "both", "any", "some", "either", "neither", "only", "most", "many",
                     "much", "few", "several", "least", "more", "less", "fewer", "always", "sometimes", "usually",
                     "often", "everything", "everyone", "everybody", "anything", "anyone", "anybody", "something",
                     "someone", "somebody", "none", "nobody", "nothing", "never", "just", "exactly", "half",
                     "majority"})
SAFE_AFTER_B = frozenset({"any", "anything", "anyone", "anybody", "either", "both", "always"})   # G0 H28: no all / every /
#                                                                       each family after "not" (all-not reading)
MODAL_B = frozenset({"must", "may", "might", "should", "shall", "could", "would", "will", "ought", "need", "needs"})
SUB_B = frozenset({"that", "which", "who", "whom", "whose", "whether", "if", "because", "when", "where", "while",
                   "unless", "although", "though", "since", "until", "before", "after", "than"})
SHAPE_B = frozenset({"same", "different", "both", "together", "each", "other", "than", "either", "neither", "between",
                     "more", "less", "older", "younger", "larger", "smaller", "longer", "shorter", "higher", "lower",
                     "earlier", "later", "first", "last"})
FUNCTION_B = frozenset({"the", "a", "an", "this", "that", "these", "those", "its", "their", "his", "her", "our",
                        "your", "my", "of", "in", "on", "at", "to", "for", "by", "with", "from", "into", "and", "or",
                        "it", "they", "he", "she", "we", "you", "i"} | AUX_FIRST)
HAVE_LIKE = ("have", "contain", "include")
_TOKEN = re.compile(r"\"[^\"\n]*\"|“[^”\n]*”|[A-Za-z0-9]+(?:['’][A-Za-z]+)?")
_SPLIT_NT = {"can't": ["can", "not"], "won't": ["will", "not"], "shan't": ["shall", "not"], "cannot": ["can", "not"]}


def tokens(text: str) -> list:
    """Lower-case word tokens; quoted spans whole; n't contractions and 'cannot' split; other punctuation dropped."""
    out = []
    for m in _TOKEN.finditer(text or ""):
        t = m.group().replace("’", "'")
        if t[0] in "\"“":
            out.append(t.replace("“", '"').replace("”", '"'))
            continue
        low = t.lower()
        if low in _SPLIT_NT:
            out += _SPLIT_NT[low]
        elif low.endswith("n't"):
            out += [low[:-3], "not"]
        else:
            out.append(low)
    return out


_AUX_RAW = re.compile(r"\b(" + "|".join(sorted(AUX_FIRST, key=len, reverse=True)) + r")\b", re.I)


def _raw_words(text: str) -> list:
    """Case-kept word tokens (quoted spans whole), aligned with tokens() for a text without n't contractions."""
    return [m.group() for m in _TOKEN.finditer(text or "")]


def _aux_and_subject(base_q: str, q: list, entry):
    """(index of the first auxiliary in q, number of subject tokens) by the entry's subject rule, or None."""
    if not entry.subject:
        return None
    pq = next((i for i, w in enumerate(q) if w in AUX_FIRST), None)
    if pq is None:
        return None
    if entry.subject == "BOTH":
        # G0 amendment A1-2 (fix F2), coded here from the page: the subject runs from the word after the first
        # auxiliary to the question's ONE word "both" (exact lower case, a whole word); a question with no "both", two
        # of them, an empty subject or nothing after "both" is refused. B counts words, A counts " both " in the text.
        raw = _raw_words(base_q)
        if len(raw) != len(q):
            return None
        at = [i for i in range(pq + 1, len(raw)) if raw[i] == "both"]
        if len(at) != 1 or at[0] <= pq + 1 or at[0] + 1 >= len(q):
            return None
        return pq, at[0] - pq - 1
    m = _AUX_RAW.search(base_q)
    if not m or not base_q[m.end():].startswith(" "):
        return None
    sm = re.match(entry.subject, base_q[m.end() + 1:])
    if not sm:
        return None
    n = len(tokens(sm.group()))
    if n == 0 or pq + 1 + n >= len(q):
        return None
    return pq, n


def _caps(text: str) -> list:
    words = re.findall(r"[A-Za-z][\w'-]*", re.sub(r"\"[^\"\n]*\"|“[^”\n]*”", " ", text or ""))
    return sorted(w for w in words[1:] if w[0].isupper())


def _ops(a: list, b: list) -> list:
    return [op for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op[0] != "equal"]


def _strip_frame(p: list, frames: tuple):
    for f in sorted(frames, key=len, reverse=True):
        ft = tokens(f)
        if p[:len(ft)] == ft:
            return p[len(ft):]
    return None


def base_feasible_b(kind: str, base_q: str, entry) -> bool:
    """B's own static check on the base question alone: can this kind be written and certified at all?"""
    if kind not in entry.kinds:
        return False
    q = tokens(base_q)
    if kind in ("equiv", "antonym", "option_framing"):
        return True
    if set(q) & NEG_B:
        return False
    pos = _aux_and_subject(base_q, q, entry)
    if pos is None:
        return False
    pq, n = pos
    cut = pq + 1 + n
    if kind == "syntactic":
        front, back = set(q[:pq] + q[pq + 1:cut]), set(q[cut:])
        return q[pq] in AUX_NEG_OK and not front & (QUANT_B | MODAL_B | SUB_B) and \
            not ((back & QUANT_B) - SAFE_AFTER_B) and not back & MODAL_B
    if kind == "implicit":
        return q[pq] in ("do", "does", "did") and bool(entry.verb) and q[cut] == entry.verb and \
            not set(q) & (QUANT_B | MODAL_B | SHAPE_B)
    return False


def classify_b(base_q: str, partner_q: str, kind: str, entry, frames: tuple) -> tuple:
    q, p = tokens(base_q), tokens(partner_q)
    if not p or (partner_q or "").count("?") != 1 or not partner_q.rstrip().endswith("?") or "\n" in partner_q:
        return None, ["B: the partner is not one question on one line"]
    if q == p:
        return None, ["B: the partner has the base's words"]
    if kind == "syntactic":
        d1 = _strip_frame(p, frames)
        if d1 is None:
            return None, ["B: no closed frame"]
        if set(q) & NEG_B:
            return None, ["B: the base already holds a negation word"]
        pos = _aux_and_subject(base_q, q, entry)
        if pos is None:
            return None, ["B: the base does not read as auxiliary + the entry's subject + rest"]
        pq, n_subj = pos
        cut = pq + 1 + n_subj
        if d1 != q[:pq] + q[pq + 1:cut] + [q[pq], "not"] + q[cut:]:
            return None, ["B: the statement is not the base with its auxiliary + 'not' moved right after the subject"]
        if q[pq] not in AUX_NEG_OK:
            return None, [f"B: auxiliary {q[pq]!r} does not take an exact 'not'"]
        front, back = set(q[:pq] + q[pq + 1:cut]), set(q[cut:])
        if front & (QUANT_B | MODAL_B | SUB_B | NEG_B):
            return None, [f"B: scope: {sorted(front & (QUANT_B | MODAL_B | SUB_B | NEG_B))} before the 'not'"]
        bad = ((back & QUANT_B) - SAFE_AFTER_B) | (back & MODAL_B)
        if bad:
            return None, [f"B: scope: {sorted(bad)} after the 'not'"]
        return "opposite", []
    if kind == "implicit":
        if set(q) & (NEG_B | QUANT_B | MODAL_B | SHAPE_B):
            return None, ["B: the base holds a negation, quantifier, modal or comparison word"]
        pos = _aux_and_subject(base_q, q, entry)
        if pos is None or not entry.verb:
            return None, ["B: no auxiliary + subject reading, or no main verb for the entry"]
        pq, n_subj = pos
        v = pq + 1 + n_subj
        if q[pq] not in ("do", "does", "did") or v >= len(q) or q[v] != entry.verb:
            return None, ["B: not a do-question whose subject is followed by the entry's main verb"]
        if p == q[:v] + ["fail", "to"] + q[v:]:
            return "opposite", []
        if entry.verb in HAVE_LIKE and p == q[:v] + ["lack"] + q[v + 1:]:
            return "opposite", []
        return None, ["B: the edit is not 'fail to' right before the main verb (or the verb -> 'lack')"]
    if kind == "antonym":
        if Counter(w for w in q if w in NEG_B) != Counter(w for w in p if w in NEG_B):
            return None, ["B: an antonym partner changes the negation words"]
        for x, y in entry.antonyms:
            xt, yt = tokens(x), tokens(y)
            at = [s for s in range(len(q) - len(xt) + 1) if q[s:s + len(xt)] == xt]
            if len(at) == 1 and q[:at[0]] + yt + q[at[0] + len(xt):] == p:
                return "opposite", []
        return None, ["B: the edit is not one closed antonym swap"]
    if kind == "option_framing":
        if entry.option_frame != "comve_other_statement":
            return None, ["B: no coded rule for this option frame"]
        ops = _ops(q, p)
        if len(ops) == 1 and ops[0][0] == "replace":
            _t, a1, a2, b1, b2 = ops[0]
            pair = (q[a1:a2], p[b1:b2])
            if pair in ((["1"], ["2"]), (["2"], ["1"])) and a1 > 0 and q[a1 - 1] == "statement" \
                    and q[a1 + 1:a1 + 4] == ["go", "against", "common"]:
                return "opposite", []
        return None, ["B: the edit is not the other-statement swap"]
    # equiv
    probs = []
    for name, vocab in (("negation", NEG_B), ("quantifier", QUANT_B), ("modal", MODAL_B)):
        if Counter(w for w in q if w in vocab) != Counter(w for w in p if w in vocab):
            probs.append(f"B: a paraphrase changes the {name} words")
    if sorted(w for w in q if w[0] == '"') != sorted(w for w in p if w[0] == '"'):
        probs.append("B: a paraphrase changes a quoted span")
    if sorted(re.findall(r"\d+", base_q)) != sorted(re.findall(r"\d+", partner_q)):
        probs.append("B: a paraphrase changes a number")
    if _caps(base_q) != _caps(partner_q):
        probs.append("B: a paraphrase changes a capitalised name")
    if _strip_frame(p, frames) is not None and _strip_frame(q, frames) is None:
        probs.append("B: a paraphrase adds a truth frame")
    for _x, y in entry.antonyms:
        yt = tokens(y)
        cnt = lambda s: sum(1 for i in range(len(s) - len(yt) + 1) if s[i:i + len(yt)] == yt)   # noqa: E731
        if cnt(p) > cnt(q):
            probs.append(f"B: a paraphrase introduces the antonym {y!r}")
    return (None, probs) if probs else ("same", [])
