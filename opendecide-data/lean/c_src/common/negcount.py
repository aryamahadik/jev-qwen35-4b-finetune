"""c_src/common/negcount.py: the one cross-family negation counter (XF02). Orchestrator-owned; no family builder writes
or forks it. CPU, standard library only, deterministic.

Definitions (XF02, the same row in every c_src/*/G0_SPEC.md; lexicons from F5 G0_SPEC 3.4, C_DATA_SPEC v4 2.2 F5):
  k_syn  the number of F5 L_core tokens in the text: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor.
         Used for the 2.1 quotas (k_syn >= 1 on >= 10% of yes/no rows; k_syn >= 2 with an affirmative twin on >= 2%).
  k_all  the F5 L_neg surface count (F5's j_q): matched L_neg entries, longest match first, left to right, no overlap,
         1 per match whatever its length; comparator phrases ("no fewer than") and implicit cues ("fail to", "lack")
         included. Used for the G10 yes-rate negation-count cells.

What to pass: the question sentence (with its embedded claim, F4; with a quoted source question, F5). Card lines,
options, the answer instruction and record text are not part of the question (F5 3.4: card lines are not counted).
F7 passes criterion text; the counter does not care what the text is, the caller decides what it counts.

Rules fixed once here (XF02: "fixed once inside negcount, never per family"):
  R1 Tokens. Words are runs of letters/digits, hyphen- or apostrophe-joined ("non-compliant", "no-show" and "don't" are
     one word before R2). Each other non-space character is its own punctuation token; a newline is a token. Case is
     ignored; curly apostrophes count as "'".
  R2 Clitics, Penn Treebank style: "<x>n't" -> "<x>" + "n't" (don't, isn't, can't = "ca" + "n't", won't = "wo" + "n't");
     "cannot" -> "can" + "not"; "'s 're 'll 'd 've 'm" split off. So "cannot", "can not" and "can't" all give k_syn 1
     and k_all 1 (entry "cannot"). A word written without its apostrophe ("dont") is not a negation.
  R3 Comparators (the XF02 question). An L_core token inside a matched comparator entry does NOT count toward k_syn;
     the entry still counts 1 in k_all. Comparator entries = F5's negated comparison words (no fewer than, no more
     than, not less than, not more than, not before, not after) plus the comparator phrases the G0 specs name as
     comparators, never as negation (COMPARATOR_ALIASES: no less than, no later than, no earlier than, not exceeding,
     does not exceed, not equal to). The aliases are not new L_neg entries: each starts with an L_core token followed
     by words that are in no L_neg entry, so k_all is the same with or without them (tested); they change only k_syn.
     Reason: F6 (3.1 "clausal/lexical", G3 agreement with negcount), F8 (SEM-06), F9 (F9-R1-21) and F2 (CMP "negcmp")
     all read these phrases as comparators; F6's G3 check needs k_syn = 0 on them.
  R4 Every other L_core token counts toward k_syn, also inside a multiword entry: "need not", "no longer", "none of",
     "not only", "it is not the case that" give k_syn 1. One exception (PREREG_FINAL.md amendment A16, ruling on
     MARKERS.md N1; v1.1): a matched "neither ... nor" pair is ONE syntactic negation, k_syn 1 (its "neither" counts,
     its "nor" does not), so it cannot fill the k_syn >= 2 double-negation quota; k_all stays 1 (one entry). A "nor"
     or "neither" outside a matched pair (another sentence, R6) still counts 1 each.
  R5 Lemmas: every inflection of the F5 verbs counts (deny/denies/denied/denying; lack, fail, neglect, omit, refuse,
     decline, prevent, rule out likewise). "fewer"/"fewest" are not "few"; "a few" is not "few" (a different, positive
     quantifier that F5 bans by name).
  R6 Discontinuous entries consume only their anchor words; words in the gap stay countable. "neither ... nor": the
     first "nor" after "neither" in the same sentence; "prevent ... from": "from" within 6 words; "ruled/ruling ... out":
     "out" within 3 words (contiguous "rule(s) out" for every form). A gap never crosses . ? ! ; or a newline.
  R7 Longest match: at each position, left to right, the matching entry with the most anchor words wins (ties: the
     order of ENTRIES). Words already used by a match are skipped.
  R8 SEM-18 affixed words are pack-declared, so the caller passes them (affixed=...); each counts 1 in k_all, 0 in
     k_syn. Litotes "not non-<P>" is then k_all 2, k_syn 1.

Status: G0 lexicon code (XF17: closed operator lexicons are G0 semantics). Before any use on rows the lexicon passes the
7.2 Claude-seed decontamination and the counts-only sealed template compare (XF17). LEXICON_SHA256 identifies it.

  from c_src.common.negcount import count
  count("Is it true that the firm did not fail to file?")  # -> k_syn 1, k_all 2
  ../.venv/bin/python c_src/common/negcount.py "Is it true that no fewer than 3 seats were sold?"
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Iterable

VERSION = "1.1"

L_CORE = ("not", "n't", "no", "none", "nobody", "nothing", "nowhere", "never", "neither", "nor")
_L_CORE = frozenset(L_CORE)

# ------------------------------------------------------------------ lexicon (F5 G0_SPEC 3.4)
# An entry: (name, class, forms). A form is a tuple of slots: a frozenset of lower-case tokens, or an int g (the next
# slot may sit up to g words later, R6). Classes: "core" (an L_core word alone), "neg" (any other L_neg entry),
# "comparator" (R3; its L_core tokens are exempt from k_syn), "comparator_alias" (R3; not an L_neg entry, k_all-neutral).

_S = lambda *w: frozenset(w)                                    # noqa: E731
NEG = _S("not", "n't")
BE = _S("is", "are", "was", "were", "be", "been", "being", "am", "'s", "'re", "'m")
DO = _S("do", "does", "did")


def _verb(base, third, past, ing):
    return _S(base, third, past, ing)


LACK = _verb("lack", "lacks", "lacked", "lacking")
FAIL = _verb("fail", "fails", "failed", "failing")
NEGLECT = _verb("neglect", "neglects", "neglected", "neglecting")
OMIT = _verb("omit", "omits", "omitted", "omitting")
REFUSE = _verb("refuse", "refuses", "refused", "refusing")
DECLINE = _verb("decline", "declines", "declined", "declining")
PREVENT = _verb("prevent", "prevents", "prevented", "preventing")
DENY = _verb("deny", "denies", "denied", "denying")
RULE = _verb("rule", "rules", "ruled", "ruling")
EXCEED = _verb("exceed", "exceeds", "exceeded", "exceeding")

ENTRIES = (
    # multiword L_neg entries (F5 3.4)
    ("it is not the case that", "neg", [(_S("it"), BE, NEG, _S("the"), _S("case"), _S("that")),
                                        (BE, _S("it"), NEG, _S("the"), _S("case"), _S("that")),
                                        (BE, NEG, _S("it"), _S("the"), _S("case"), _S("that"))]),
    ("is not permitted to", "neg", [(BE, NEG, _S("permitted"), _S("to"))]),
    ("does not have to", "neg", [(DO, NEG, _S("have"), _S("to"))]),
    ("is not required to", "neg", [(BE, NEG, _S("required"), _S("to"))]),
    ("did not manage to", "neg", [(DO, NEG, _S("manage"), _S("to"))]),
    ("it is false that", "neg", [(_S("it"), BE, _S("false"), _S("that")), (BE, _S("it"), _S("false"), _S("that"))]),
    ("no fewer than", "comparator", [(_S("no"), _S("fewer"), _S("than"))]),
    ("no more than", "comparator", [(_S("no"), _S("more"), _S("than"))]),
    ("not less than", "comparator", [(NEG, _S("less"), _S("than"))]),
    ("not more than", "comparator", [(NEG, _S("more"), _S("than"))]),
    ("not before", "comparator", [(NEG, _S("before"))]),
    ("not after", "comparator", [(NEG, _S("after"))]),
    ("neither ... nor", "neg", [(_S("neither"), 40, _S("nor"))]),
    ("not only", "neg", [(_S("not"), _S("only"))]),
    ("no longer", "neg", [(_S("no"), _S("longer"))]),
    ("need not", "neg", [(_S("need"), NEG)]),
    ("must not", "neg", [(_S("must"), NEG)]),
    ("may not", "neg", [(_S("may"), _S("not"))]),
    ("not both", "neg", [(_S("not"), _S("both"))]),
    ("not every", "neg", [(_S("not"), _S("every"))]),
    ("not all", "neg", [(_S("not"), _S("all"))]),
    ("not any", "neg", [(_S("not"), _S("any"))]),
    ("none of", "neg", [(_S("none"), _S("of"))]),
    ("all except", "neg", [(_S("all"), _S("except"))]),
    ("except when", "neg", [(_S("except"), _S("when"))]),
    ("other than", "neg", [(_S("other"), _S("than"))]),
    # single L_neg entries (F5 3.4; "<verb> to" / "prevent from" / "rule out" carry their particle)
    ("fail to", "neg", [(FAIL, _S("to"))]),
    ("neglect to", "neg", [(NEGLECT, _S("to"))]),
    ("omit to", "neg", [(OMIT, _S("to"))]),
    ("refuse to", "neg", [(REFUSE, _S("to"))]),
    ("decline to", "neg", [(DECLINE, _S("to"))]),
    ("prevent from", "neg", [(PREVENT, 6, _S("from"))]),
    ("rule out", "neg", [(RULE, _S("out")), (_S("ruled", "ruling"), 3, _S("out"))]),
    ("free of", "neg", [(_S("free"), _S("of"))]),
    ("cannot", "neg", [(_S("can"), _S("not")), (_S("ca"), _S("n't"))]),
    ("without", "neg", [(_S("without"),)]),
    ("lack", "neg", [(LACK,)]),
    ("deny", "neg", [(DENY,)]),
    ("hardly", "neg", [(_S("hardly"),)]),
    ("scarcely", "neg", [(_S("scarcely"),)]),
    ("few", "neg", [(_S("few"),)]),
    ("barely", "neg", [(_S("barely"),)]),
    ("except", "neg", [(_S("except"),)]),
    ("unless", "neg", [(_S("unless"),)]),
    ("false", "neg", [(_S("false"),)]),
) + tuple((w, "core", [(_S(w),)]) for w in L_CORE)

# R3 aliases: comparator phrases named in the G0 specs (F1, F2, F4, F5 SEM-11, F6 3.1, F7, F8 SEM-06, F9 T10, F12
# SEM-12, F13 SEM-10). k_all-neutral by construction; they only exempt their L_core token from k_syn.
COMPARATOR_ALIASES = (
    ("no less than", "comparator_alias", [(_S("no"), _S("less"), _S("than"))]),
    ("no later than", "comparator_alias", [(_S("no"), _S("later"), _S("than"))]),
    ("no earlier than", "comparator_alias", [(_S("no"), _S("earlier"), _S("than"))]),
    ("not exceeding", "comparator_alias", [(NEG, _S("exceeding"))]),
    ("does not exceed", "comparator_alias", [(DO, NEG, EXCEED)]),
    ("not equal to", "comparator_alias", [(NEG, _S("equal"), _S("to"))]),
)

_EXEMPT = frozenset({"comparator", "comparator_alias"})
# R4 exception (A16): entries whose matched L_core anchors count ONCE toward k_syn (the first anchor only)
_SYN_ONCE = frozenset({"neither ... nor"})
_NOT_AFTER = {"few": _S("a")}        # R5: "a few" is not "few"
_STOP = frozenset({".", "?", "!", ";", "\n"})


def lexicon() -> dict:
    """The lexicon as plain JSON (sorted token lists), for audit and the sha."""
    def form(f):
        return [s if isinstance(s, int) else sorted(s) for s in f]
    return {"version": VERSION, "l_core": list(L_CORE),
            "entries": [{"name": n, "class": c, "forms": [form(f) for f in fs]} for n, c, fs in ENTRIES],
            "comparator_aliases": [{"name": n, "class": c, "forms": [form(f) for f in fs]}
                                   for n, c, fs in COMPARATOR_ALIASES],
            "not_after": {k: sorted(v) for k, v in _NOT_AFTER.items()}, "stop": sorted(_STOP),
            "syn_once": sorted(_SYN_ONCE)}


LEXICON_SHA256 = hashlib.sha256(json.dumps(lexicon(), sort_keys=True).encode()).hexdigest()

# ------------------------------------------------------------------ tokenizer (R1, R2)

_APOS = str.maketrans({"’": "'", "‘": "'", "ʼ": "'", "′": "'"})
_TOKEN = re.compile(r"\d+(?:[.,:/]\d+)*|[^\W_]+(?:[-'][^\W_]+)*|\n|[^\s]")
_CLITIC = re.compile(r"(.+?)('s|'re|'ll|'d|'ve|'m)")


@dataclass(frozen=True)
class Token:
    low: str
    start: int
    end: int


def tokenize(text: str) -> list[Token]:
    text = (text or "").translate(_APOS)
    out = []
    for m in _TOKEN.finditer(text):
        w, s, e = m.group().lower(), m.start(), m.end()
        if w == "cannot":
            out += [Token("can", s, s + 3), Token("not", s + 3, e)]
        elif len(w) > 3 and w.endswith("n't"):
            out += [Token(w[:-3], s, e - 3), Token("n't", e - 3, e)]
        elif "'" in w and _CLITIC.fullmatch(w):
            stem, cl = _CLITIC.fullmatch(w).groups()
            out += [Token(stem, s, s + len(stem)), Token(cl, s + len(stem), e)]
        else:
            out.append(Token(w, s, e))
    return out

# ------------------------------------------------------------------ matcher (R6, R7)


@dataclass(frozen=True)
class Match:
    entry: str
    cls: str
    anchors: tuple
    surface: str


@dataclass(frozen=True)
class NegCount:
    k_syn: int
    k_all: int
    matches: tuple
    syn_tokens: tuple            # the L_core tokens that counted toward k_syn, in order

    def as_dict(self):
        return {"k_syn": self.k_syn, "k_all": self.k_all, "syn_tokens": list(self.syn_tokens),
                "matches": [asdict(m) for m in self.matches]}


def _match_form(toks, i, form, used):
    anchors, prev, gap = [], None, 0
    for slot in form:
        if isinstance(slot, int):
            gap = slot
            continue
        if prev is None:
            if i in used or toks[i].low not in slot:
                return None
            hit = i
        else:
            hit = None
            for p in range(prev + 1, min(len(toks), prev + 2 + gap)):
                if toks[p].low in slot and p not in used:
                    hit = p
                    break
                if toks[p].low in _STOP or gap == 0:
                    break
            if hit is None:
                return None
        anchors.append(hit)
        prev, gap = hit, 0
    return anchors


@lru_cache(maxsize=256)
def _index(affixed: tuple, aliases: bool = True):
    """first-slot token -> [(order, name, cls, form)] over the entries in force (ENTRIES, the R3 aliases, R8 words)."""
    extra = tuple((w, "affixed", [tuple(_S(t.low) for t in tokenize(w))]) for w in affixed if tokenize(w))
    idx = defaultdict(list)
    for order, (name, cls, forms) in enumerate(ENTRIES + (COMPARATOR_ALIASES if aliases else ()) + extra):
        for f in forms:
            for t in f[0]:
                idx[t].append((order, name, cls, f))
    return dict(idx)


def _count(text: str, affixed: Iterable[str] = (), aliases: bool = True) -> NegCount:
    src = (text or "").translate(_APOS)
    toks = tokenize(src)
    idx = _index(tuple(affixed), aliases)
    used, matches = set(), []
    for i, tok in enumerate(toks):
        if i in used:
            continue
        best = None
        for order, name, cls, f in idx.get(tok.low, ()):
            if name in _NOT_AFTER and i > 0 and toks[i - 1].low in _NOT_AFTER[name]:
                continue
            a = _match_form(toks, i, f, used)
            if a is None:
                continue
            key = (len(a), -order)
            if best is None or key > best[0]:
                best = (key, name, cls, a)
        if best:
            _, name, cls, a = best
            used.update(a)
            if any(y - x > 1 for x, y in zip(a, a[1:])):
                surface = " ... ".join(src[toks[x].start:toks[x].end] for x in a)
            else:
                surface = src[toks[a[0]].start:toks[a[-1]].end]
            matches.append(Match(name, cls, tuple(a), surface))
    exempt = {x for m in matches if m.cls in _EXEMPT for x in m.anchors}
    exempt |= {x for m in matches if m.entry in _SYN_ONCE for x in m.anchors[1:]}     # R4 exception (A16)
    syn = tuple(t.low for j, t in enumerate(toks) if t.low in _L_CORE and j not in exempt)
    return NegCount(k_syn=len(syn), k_all=len(matches), matches=tuple(matches), syn_tokens=syn)


def count(text: str, affixed: Iterable[str] = ()) -> NegCount:
    """k_syn, k_all and the matches for one text. affixed: the pack's SEM-18 affixed words (R8)."""
    return _count(text, affixed)


def k_syn(text: str) -> int:
    return _count(text).k_syn


def k_all(text: str, affixed: Iterable[str] = ()) -> int:
    return _count(text, affixed).k_all


def main(argv=None):
    ap = argparse.ArgumentParser(description="XF02 negation counter: k_syn and k_all for one text")
    ap.add_argument("text")
    ap.add_argument("--affixed", default="", help="comma-separated SEM-18 affixed words of the pack")
    a = ap.parse_args(argv)
    aff = [w.strip() for w in a.affixed.split(",") if w.strip()]
    print(json.dumps({**count(a.text, aff).as_dict(), "version": VERSION, "lexicon_sha256": LEXICON_SHA256}))


if __name__ == "__main__":
    main()
