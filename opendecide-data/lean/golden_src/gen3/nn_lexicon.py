"""nn_lexicon (F7 v2): the curated, Claude-written data lexicon of family F7 'nested negation'.

The builder (golden_src/gen3/gen3_nested_negation.py) draws every negation cue, frame, claim wording, definition and
distractor from this file; no model picks a word. This file holds wording only: no gold is computed here.

Sections
  LEXICON       every negation cue lexeme: class (syntactic / affixal / lexical / truth_frame / cross_sentence /
                answer_mapping), split (train or holdout), inflected surface forms, whether it can serve as a distractor.
                Checklist rule 2.8: >= 60 train lexemes over the 5 classes; >= 15 held-out lexemes (>= 1 per class).
  LOOKALIKES    words that look like negations but are not (checklist item 20).
  FRAMES        outer question frames in families (rule 2.9: >= 12 train families x >= 4 frames; 3 held-out families).
  CARD_SOURCES  card-format sources (real texts with human gold): authored label definitions, document nouns, label
                sets, ordinal poles (item 21) and the dev text pools. Definitions are written here (not copied from the
                golden cards) so they carry no golden_dev 12-gram and read the same in train, iid and holdout.
  MULTI_SOURCES multi-text (quantifier) sources: per-text property wording.
  PACKS         program-written record packs: per-predicate claim wording for every lexeme the pack supports.
  DISTRACTORS   provably non-scoping negations (side clauses, separate sentences, card lines).
  BANS          the v1 bans (dev frame, 'non-hateful', nothing about hate, judge words) plus the EXCLUDE list X1-X12.

Slots in templates: {S} claim subject, {L} quoted label, {doc} document noun, {ev} evaluator NP, {c} declarative
claim, {cp} declarative claim with a pronoun subject, {cq} interrogative claim, {N} an item name, {k}/{n} numbers.
"""
from __future__ import annotations

import re

# ============================================================================================ 1. lexicon
# cls: syntactic | affixal | lexical | truth_frame | cross_sentence | answer_mapping. split: train | holdout.
# forms: the surface words the lexeme takes (inflections listed, rule 2.8). distract: the lexeme can serve as a
# non-scoping distractor, so it must do so in >= 10% of its train uses (CL:351). Every syntactic lexeme can (a side
# clause or a card line that decides nothing: F7_OBJECTIONS.md A1), and so can the content verbs that describe the
# document (fail, lack, omit, miss, skip, avoid, decline, refuse, leave out, withhold, absent, forbid). Not flagged:
# the claim-evaluation verbs (deny, refute, reject, dispute, dismiss, contradict, exclude, rule out) and the truth-value
# frames, which in a side clause would evaluate a claim next to the claim under test, and the cross-sentence /
# answer-mapping cues, which only exist to scope.
def _L(cls, split, forms, distract=False, note=""):
    return {"cls": cls, "split": split, "forms": list(forms), "can_distract": distract, "note": note}


LEXICON = {
    # ---- syntactic (train)
    "not": _L("syntactic", "train", ["not"], True, "clausal negation; also the 'or not' of a 'whether or not' side clause"),
    "n't": _L("syntactic", "train", ["n't", "doesn't", "isn't", "hasn't", "didn't", "wasn't", "aren't", "don't"], True),
    "no": _L("syntactic", "train", ["no"], True),
    "never": _L("syntactic", "train", ["never"], True),
    "none": _L("syntactic", "train", ["none"], True),
    "nothing": _L("syntactic", "train", ["nothing"], True),
    "nobody": _L("syntactic", "train", ["nobody"], True),
    "no one": _L("syntactic", "train", ["no one"], True),
    "without": _L("syntactic", "train", ["without"], True),
    "cannot": _L("syntactic", "train", ["cannot", "can't"], True),
    "neither": _L("syntactic", "train", ["neither", "nor"], True, note="'neither A nor B' is one negation over 'A or B'"),
    "not a single": _L("syntactic", "train", ["not a single"], True),
    "not every": _L("syntactic", "train", ["not every"], True, note="needs the card's logic line (X10)"),
    "not all": _L("syntactic", "train", ["not all"], True, note="needs the card's logic line (X10)"),
    "no more than": _L("syntactic", "train", ["no more than"], True),
    "few": _L("syntactic", "train", ["few"], True, note="approximate negator; the card fixes 'few' = at most one (item 29)"),
    "unless": _L("syntactic", "train", ["unless"], True, note="'X unless Y' = X when not Y (item 34)"),
    "need not": _L("syntactic", "train", ["need not"], True, note="deontic: 'need not' = not required (item 33)"),
    "must not": _L("syntactic", "train", ["must not"], True, note="deontic: 'must not' = forbidden (item 33)"),
    # ---- affixal (train)
    "non-": _L("affixal", "train", ["non-"], True),
    "un-": _L("affixal", "train", ["un-"], True),
    "in-": _L("affixal", "train", ["in-"], True),
    "im-": _L("affixal", "train", ["im-"], True),
    "il-": _L("affixal", "train", ["il-"], True),
    "dis-": _L("affixal", "train", ["dis-"], True),
    "-less": _L("affixal", "train", ["-less"], True),
    "-free": _L("affixal", "train", ["-free"], True),
    # ---- lexical (train)
    "fail": _L("lexical", "train", ["fail", "fails", "failed", "failing"], True),
    "lack": _L("lexical", "train", ["lack", "lacks", "lacked", "lacking"], True),
    "deny": _L("lexical", "train", ["deny", "denies", "denied", "denying"]),
    "refute": _L("lexical", "train", ["refute", "refutes", "refuted", "refuting"]),
    "reject": _L("lexical", "train", ["reject", "rejects", "rejected", "rejecting"]),
    "dispute": _L("lexical", "train", ["dispute", "disputes", "disputed", "disputing"]),
    "dismiss": _L("lexical", "train", ["dismiss", "dismisses", "dismissed", "dismissing"]),
    "contradict": _L("lexical", "train", ["contradict", "contradicts", "contradicted", "contradicting"]),
    "omit": _L("lexical", "train", ["omit", "omits", "omitted", "omitting"], True),
    "exclude": _L("lexical", "train", ["exclude", "excludes", "excluded", "excluding"]),
    "refuse": _L("lexical", "train", ["refuse", "refuses", "refused", "refusing"], True),
    "decline": _L("lexical", "train", ["decline", "declines", "declined", "declining"], True),
    "avoid": _L("lexical", "train", ["avoid", "avoids", "avoided", "avoiding"], True),
    "miss": _L("lexical", "train", ["miss", "misses", "missed", "missing"], True),
    "rule out": _L("lexical", "train", ["rule out", "rules out", "ruled out", "ruling out"]),
    "withhold": _L("lexical", "train", ["withhold", "withholds", "withheld", "withholding"], True),
    "absent": _L("lexical", "train", ["absent"], True),
    "skip": _L("lexical", "train", ["skip", "skips", "skipped", "skipping"], True),
    "forbid": _L("lexical", "train", ["forbid", "forbids", "forbade", "forbidden"], True),
    "leave out": _L("lexical", "train", ["leave out", "leaves out", "left out", "leaving out"], True),
    # ---- truth-value frames (train)
    "false": _L("truth_frame", "train", ["false"]),
    "untrue": _L("truth_frame", "train", ["untrue"]),
    "not the case": _L("truth_frame", "train", ["not the case"]),
    "unsupported": _L("truth_frame", "train", ["unsupported"]),
    "unfounded": _L("truth_frame", "train", ["unfounded"]),
    "baseless": _L("truth_frame", "train", ["baseless"]),
    # ---- cross-sentence negators (train)
    "reverse": _L("cross_sentence", "train", ["reverse"]),
    "opposite": _L("cross_sentence", "train", ["opposite"]),
    "negation": _L("cross_sentence", "train", ["negation"]),
    # ---- answer mapping (train): in the instruction (answer_map) or in the card's yes/no key (yn_key)
    "answer no if": _L("answer_mapping", "train", ["answer no if"]),
    "say no when": _L("answer_mapping", "train", ["say no when"]),
    "no exactly when": _L("answer_mapping", "train", ["no exactly when"]),
    "fails to hold": _L("answer_mapping", "train", ["fails to hold"], note="inverted yes/no key (item 14)"),
    "is false of": _L("answer_mapping", "train", ["is false of"], note="inverted yes/no key (item 14)"),
    # ---- HELD OUT (dev_holdout only; never in a train row, inflections included)
    "not one": _L("syntactic", "holdout", ["not one"], True),
    "at no point": _L("syntactic", "holdout", ["at no point"], True),
    "no longer": _L("syntactic", "holdout", ["no longer"], True),
    "ir-": _L("affixal", "holdout", ["ir-"]),
    "a-": _L("affixal", "holdout", ["a-"]),
    "overturn": _L("lexical", "holdout", ["overturn", "overturns", "overturned", "overturning"]),
    "rebut": _L("lexical", "holdout", ["rebut", "rebuts", "rebutted", "rebutting"]),
    "veto": _L("lexical", "holdout", ["veto", "vetoes", "vetoed", "vetoing"]),
    "forgo": _L("lexical", "holdout", ["forgo", "forgoes", "forwent", "forgone"]),
    "abstain": _L("lexical", "holdout", ["abstain", "abstains", "abstained", "abstaining"]),
    "turn down": _L("lexical", "holdout", ["turn down", "turns down", "turned down", "turning down"]),
    "groundless": _L("truth_frame", "holdout", ["groundless"]),
    "erroneous": _L("truth_frame", "holdout", ["erroneous"]),
    "far from true": _L("truth_frame", "holdout", ["far from true"]),
    "contrary": _L("cross_sentence", "holdout", ["contrary"]),
    "mark no if": _L("answer_mapping", "holdout", ["mark no if"]),
    "enter no if": _L("answer_mapping", "holdout", ["enter no if"]),
}
CLASSES5 = {"syntactic": "syntactic", "affixal": "affixal", "lexical": "lexical", "truth_frame": "truth_frame",
            "cross_sentence": "cross+answer", "answer_mapping": "cross+answer"}

# look-alikes (item 20): never negations; they are recorded as cues of class 'lookalike' (non-scoping, no LF node)
LOOKALIKES = {
    "under": {"text": "Under the card's definitions, ", "kind": "prefix"},
    "displayed": {"text": "Going by the displayed {doc}, ", "kind": "prefix"},
    "uniform": {"text": "Read the definitions as one uniform set. ", "kind": "sentence"},
    "unit": {"text": "Treat the {doc} as a single unit. ", "kind": "sentence"},
    "notably": {"text": "Notably, the card defines every term used here. ", "kind": "sentence"},
    "nonetheless": {"text": "The {doc} may be short; nonetheless, ", "kind": "prefix"},
}
for _k in LOOKALIKES:
    LEXICON[_k] = _L("lookalike", "train", [_k])
LEXICON["displayed"]["forms"] = ["displayed"]


def lexemes(split="train", cls=None):
    return sorted(k for k, v in LEXICON.items() if v["split"] == split and v["cls"] != "lookalike"
                  and (cls is None or v["cls"] == cls))


def cls_of(lex):
    return LEXICON[lex]["cls"]


# ============================================================================================ 2. bans
BANNED_PATTERNS = [re.compile(p, re.I) for p in (
    r"\bbe\s+rejected\b", r"\bthe\s+statement\s+that\b", r"\bshould\s+the\s+statement\b", r"non-?hateful",
    r"\bhat(e|eful|red|ing)\b", r"\bhate\s+speech\b", r"\bthe\s+idea\s+that\b", r"\bwould\s+it\s+be\s+an\s+error\b",
    r"\bcontains\s+only\s+non\b")]
JUDGE_BANNED = re.compile(r"\b(right|wrong|correct|incorrect|accurate|inaccurate|mistaken|mistake|reply|replies|"
                          r"agreed|disagree|undercut|debate|commenter|back)\b|two notes", re.I)


def banned_hits(*texts):
    out = []
    for t in texts:
        if not t:
            continue
        for p in BANNED_PATTERNS:
            if p.search(t):
                out.append(p.pattern)
        if JUDGE_BANNED.search(t):
            out.append("judge:" + JUDGE_BANNED.search(t).group(0).lower())
    return out


def art(word):
    return "an" if word[:1].lower() in "aeiou" else "a"


# ============================================================================================ 3. frames
# One frame = one outer question template. cues: the frame's own negation cues, outermost first, as (lexeme, surface).
# pos: where those cues sit (outer_frame / separate_sentence / answer_map); dist: their distance to the claim.
# subj: 'full' -> the claim keeps its full subject ({c}); 'pron' -> a pronoun subject when the frame already names the
# document ({cp}); needs 'cq' -> the claim as a polar question. y / n: the card's yes / no lines (statement form, the
# same cues as the question for y; n states the outer polarity flipped). yn False: never with yes/no lines.
# embed: clause embeddings the frame adds (checklist rule 2.7).
def _F(fid, fam, q, y, n, cues=(), pos="outer_frame", dist="same_sentence", subj="full", embed=1, split="train",
       yn=True, kinds=None, needs="c", bival=False):
    return {"id": fid, "family": fam, "q": q, "y": y, "n": n, "cues": list(cues), "pos": pos, "dist": dist,
            "subj": subj, "embed": embed, "split": split, "yn": yn, "kinds": kinds, "needs": needs, "bival": bival}


FRAMES_LIST = [
    # ---- direct: the claim itself as a polar question (no outer cue)
    _F("dir1", "direct", "{cq}?", "{c}", "{cneg}", embed=0, needs="cq"),
    _F("dir2", "direct", "Based on the {doc}, {cql}?", "{c}", "{cneg}", embed=0, needs="cq"),
    _F("dir3", "direct", "{cq}? Answer from the {doc} and the card alone.", "{c}", "{cneg}", embed=0, needs="cq"),
    _F("dir4", "direct", "Judging only by the {doc}, {cql}?", "{c}", "{cneg}", embed=0, needs="cq"),
    _F("dir5", "direct", "Going by the card's definitions, {cql}?", "{c}", "{cneg}", embed=0, needs="cq"),
    # ---- truth: an affirmative statement-evaluation frame (no outer cue)
    _F("tru1", "truth", "Is it true that {c}?", "it is true that {c}", "it is untrue that {c}"),
    _F("tru2", "truth", "Is this true of the {doc}: {c}?", "this is true of the {doc}: {c}",
       "this is untrue of the {doc}: {c}"),
    _F("tru3", "truth", "Is it a fair summary of the {doc} that {c}?", "it is a fair summary of the {doc} that {c}",
       "it is an unfair summary of the {doc} that {c}"),
    _F("tru4", "truth", "Does it hold that {c}?", "it holds that {c}", "it fails to hold that {c}"),
    _F("tru5", "truth", "Can one say, from the {doc}, that {c}?", "one can say, from the {doc}, that {c}",
       "one cannot say, from the {doc}, that {c}"),
    # ---- falsity: one truth-value cue over the claim
    _F("fal1", "falsity", "Is it false that {c}?", "it is false that {c}", "it is true that {c}", [("false", "false")]),
    _F("fal2", "falsity", "Is it untrue that {c}?", "it is untrue that {c}", "it is true that {c}",
       [("untrue", "untrue")]),
    _F("fal3", "falsity", "Would it be false to say that {c}?", "it would be false to say that {c}",
       "it would be true to say that {c}", [("false", "false")]),
    _F("fal4", "falsity", "Is the claim that {c} false?", "the claim that {c} is false", "the claim that {c} is true",
       [("false", "false")]),
    _F("fal5", "falsity", "Does the {doc} show that the following is not the case: {c}?",
       "the {doc} shows that the following is not the case: {c}", "the {doc} shows that the following holds: {c}",
       [("not the case", "not the case")], embed=2, bival=True),
    _F("fal6", "falsity", "Is it untrue, going by the {doc}, that {c}?", "it is untrue, going by the {doc}, that {c}",
       "it is true, going by the {doc}, that {c}", [("untrue", "untrue")]),
    _F("fal7", "falsity", "Would a careful reader judge that the following is not the case: {c}?",
       "a careful reader would judge that the following is not the case: {c}",
       "a careful reader would judge that the following holds: {c}",
       [("not the case", "not the case")], embed=2, bival=True),
    # ---- support: affirmative evidence frames (no outer cue)
    _F("sup1", "support", "Does the {doc} support the claim that {cp}?", "the {doc} supports the claim that {cp}",
       "the {doc} gives the claim that {cp} no support", subj="pron", bival=True),
    _F("sup2", "support", "Is the claim that {c} borne out by the {doc}?", "the claim that {c} is borne out by the {doc}",
       "the claim that {c} is left unproven by the {doc}", bival=True),
    _F("sup3", "support", "Does the {doc} confirm that {cp}?", "the {doc} confirms that {cp}",
       "the {doc} leaves it unconfirmed that {cp}", subj="pron", bival=True),
    _F("sup4", "support", "Does the {doc} bear out the claim that {cp}?", "the {doc} bears out the claim that {cp}",
       "the {doc} leaves the claim that {cp} unproven", subj="pron", bival=True),
    _F("sup5", "support", "Is there clear support in the {doc} for the claim that {cp}?",
       "there is clear support in the {doc} for the claim that {cp}",
       "the {doc} holds no clear support for the claim that {cp}", subj="pron", bival=True),
    # ---- refutation: one lexical cue
    _F("ref1", "refute", "Does the {doc} refute the claim that {cp}?", "the {doc} refutes the claim that {cp}",
       "the {doc} leaves the claim that {cp} standing", [("refute", "refute")], subj="pron", bival=True),
    _F("ref2", "refute", "Does the {doc} contradict the claim that {cp}?", "the {doc} contradicts the claim that {cp}",
       "the {doc} is consistent with the claim that {cp}", [("contradict", "contradict")], subj="pron", bival=True),
    _F("ref3", "refute", "Is the claim that {c} refuted by the {doc}?", "the claim that {c} is refuted by the {doc}",
       "the claim that {c} stands, given the {doc}", [("refute", "refuted")], bival=True),
    _F("ref4", "refute", "Do the details of the {doc} contradict the claim that {cp}?",
       "the details of the {doc} contradict the claim that {cp}",
       "the details of the {doc} are consistent with the claim that {cp}", [("contradict", "contradict")],
       subj="pron", bival=True),
    _F("ref5", "refute", "Is the claim that {c} contradicted by the {doc}?",
       "the claim that {c} is contradicted by the {doc}", "the claim that {c} is consistent with the {doc}",
       [("contradict", "contradicted")], bival=True),
    # ---- unfounded: one truth-value cue that assumes the material settles the claim (bivalence line)
    _F("unf1", "unfounded", "Is the claim that {c} unsupported by the {doc}?",
       "the claim that {c} is unsupported by the {doc}", "the claim that {c} is supported by the {doc}",
       [("unsupported", "unsupported")], bival=True),
    _F("unf2", "unfounded", "Is the claim that {c} unfounded?", "the claim that {c} is unfounded",
       "the claim that {c} is well founded", [("unfounded", "unfounded")], bival=True),
    _F("unf3", "unfounded", "Is it baseless to claim that {c}?", "it is baseless to claim that {c}",
       "it is well grounded to claim that {c}", [("baseless", "baseless")], bival=True),
    _F("unf4", "unfounded", "Would the claim that {c} be unfounded, judging by the {doc}?",
       "the claim that {c} would be unfounded, judging by the {doc}",
       "the claim that {c} would be well founded, judging by the {doc}", [("unfounded", "unfounded")], bival=True),
    _F("unf5", "unfounded", "Does the {doc} leave the claim that {cp} unsupported?",
       "the {doc} leaves the claim that {cp} unsupported", "the {doc} supports the claim that {cp}",
       [("unsupported", "unsupported")], subj="pron", bival=True),
    _F("unf6", "unfounded", "Is the claim that {c} baseless?", "the claim that {c} is baseless",
       "the claim that {c} is well grounded", [("baseless", "baseless")], bival=True),
    # ---- reader: what a careful reader should do with the claim (0 or 1 lexical cue)
    _F("rea1", "reader", "Should a careful reader accept the claim that {c}?",
       "a careful reader should accept the claim that {c}", "a careful reader should set the claim that {c} aside",
       bival=True),
    _F("rea2", "reader", "Should a careful reader reject the claim that {c}?",
       "a careful reader should reject the claim that {c}", "a careful reader should accept the claim that {c}",
       [("reject", "reject")], bival=True),
    _F("rea3", "reader", "Should a careful reader dismiss the claim that {c}?",
       "a careful reader should dismiss the claim that {c}", "a careful reader should accept the claim that {c}",
       [("dismiss", "dismiss")], bival=True),
    _F("rea4", "reader", "Would a careful reader dispute the claim that {c}?",
       "a careful reader would dispute the claim that {c}", "a careful reader would accept the claim that {c}",
       [("dispute", "dispute")], bival=True),
    _F("rea5", "reader", "Would a careful reader deny that {c}?", "a careful reader would deny that {c}",
       "a careful reader would grant that {c}", [("deny", "deny")], bival=True),
    _F("rea6", "reader", "Would a careful reader sign off on the claim that {c}?",
       "a careful reader would sign off on the claim that {c}",
       "a careful reader would hold off on the claim that {c}", bival=True),
    # ---- failshow: one lexical 'fail' cue over an evidence verb
    _F("fsh1", "failshow", "Does the {doc} fail to show that {cp}?", "the {doc} fails to show that {cp}",
       "the {doc} shows that {cp}", [("fail", "fail")], subj="pron", bival=True),
    _F("fsh2", "failshow", "Does the {doc} fail to support the claim that {cp}?",
       "the {doc} fails to support the claim that {cp}", "the {doc} supports the claim that {cp}",
       [("fail", "fail")], subj="pron", bival=True),
    _F("fsh3", "failshow", "Does the {doc} fail to establish that {cp}?", "the {doc} fails to establish that {cp}",
       "the {doc} establishes that {cp}", [("fail", "fail")], subj="pron", bival=True),
    _F("fsh4", "failshow", "Does the {doc} fail to bear out the claim that {cp}?",
       "the {doc} fails to bear out the claim that {cp}", "the {doc} bears out the claim that {cp}",
       [("fail", "fail")], subj="pron", bival=True),
    # ---- nosupport: one syntactic cue in the outer frame
    _F("nos1", "nosupport", "Does the {doc} give no support to the claim that {cp}?",
       "the {doc} gives no support to the claim that {cp}", "the {doc} gives support to the claim that {cp}",
       [("no", "no")], subj="pron", bival=True),
    _F("nos2", "nosupport", "Does nothing in the {doc} support the claim that {cp}?",
       "nothing in the {doc} supports the claim that {cp}", "something in the {doc} supports the claim that {cp}",
       [("nothing", "nothing")], subj="pron", bival=True),
    _F("nos3", "nosupport", "Is there no sign in the {doc} that {cp}?", "there is no sign in the {doc} that {cp}",
       "there is a clear sign in the {doc} that {cp}", [("no", "no")], subj="pron", bival=True),
    _F("nos4", "nosupport", "Does the {doc} offer no grounds for the claim that {cp}?",
       "the {doc} offers no grounds for the claim that {cp}", "the {doc} offers grounds for the claim that {cp}",
       [("no", "no")], subj="pron", bival=True),
    # nos5 ('Does the {doc} never state that {cp}?') was retired in r4 (yn2b/F7_BLIND_READ.md 4.D): no record, batch or
    # text ever literally states a label claim, so the literal reading answers yes whatever the text shows
    _F("nos6", "nosupport", "Does the {doc} say nothing in favour of the claim that {cp}?",
       "the {doc} says nothing in favour of the claim that {cp}",
       "the {doc} says something in favour of the claim that {cp}", [("nothing", "nothing")], subj="pron",
       bival=True),
    # ---- note: an attributed claim in its own sentence, the outer cue in the next sentence (items 10, 12)
    _F("not1", "note", "A note says that {c}. Does the {doc} bear out that note?",
       "the {doc} bears out the note that {c}", "the {doc} leaves the note that {c} unproven", dist="next_sentence",
       bival=True),
    _F("not2", "note", "A note says that {c}. Does the {doc} contradict that note?",
       "the {doc} contradicts the note that {c}", "the {doc} is consistent with the note that {c}",
       [("contradict", "contradict")], dist="next_sentence", bival=True),
    _F("not3", "note", "A note says that {c}. Is that note false?", "the note that {c} is false",
       "the note that {c} is true", [("false", "false")], dist="next_sentence"),
    _F("not4", "note", "A log entry states that {c}. Should that entry be dismissed?",
       "the log entry that {c} should be dismissed", "the log entry that {c} should be kept",
       [("dismiss", "dismissed")], dist="next_sentence", bival=True),
    _F("not5", "note", "A log entry states that {c}. Does the {doc} refute that entry?",
       "the {doc} refutes the log entry that {c}", "the {doc} leaves the log entry that {c} standing",
       [("refute", "refute")], dist="next_sentence", bival=True),
    _F("not6", "note", "A log entry states that {c}. Is that entry untrue?", "the log entry that {c} is untrue",
       "the log entry that {c} is true", [("untrue", "untrue")], dist="next_sentence"),
    _F("not7", "note", "A clerk wrote that {c}. Is that entry borne out by the {doc}?",
       "the clerk's entry that {c} is borne out by the {doc}",
       "the clerk's entry that {c} is left unproven by the {doc}", dist="next_sentence", bival=True),
    _F("not8", "note", "A clerk wrote that {c}. Is that entry unfounded?", "the clerk's entry that {c} is unfounded",
       "the clerk's entry that {c} is well founded", [("unfounded", "unfounded")], dist="next_sentence", bival=True),
    # ---- reverse: a cross-sentence negator; the claim follows in a later sentence (item 12)
    _F("rev1", "reverse", "Consider the reverse of the claim that follows. Claim: {c}. Does the {doc} support that "
       "reverse?", "the {doc} supports the reverse of the claim that {c}",
       "the {doc} gives the reverse of the claim that {c} no support", [("reverse", "reverse")],
       pos="separate_sentence", dist="next_sentence", embed=1, bival=True),
    _F("rev2", "reverse", "Think about the opposite of the claim below. Claim: {c}. Is that opposite true of the "
       "{doc}?", "the opposite of this claim is true of the {doc}: {c}",
       "the opposite of this claim is untrue of the {doc}: {c}", [("opposite", "opposite")],
       pos="separate_sentence", dist="next_sentence", embed=1),
    _F("rev3", "reverse", "Take the negation of the claim given below. The claim was written by an intake clerk. "
       "Claim: {c}. Does the {doc} bear out that negation?", "the {doc} bears out the negation of the claim that {c}",
       "the {doc} leaves the negation of the claim that {c} unproven", [("negation", "negation")],
       pos="separate_sentence", dist="far", embed=1, bival=True),
    _F("rev4", "reverse", "We need the opposite of a claim. The claim comes from an intake form. Claim: {c}. Is that "
       "opposite borne out by the {doc}?", "the {doc} bears out the opposite of this claim: {c}",
       "the {doc} leaves the opposite of this claim unproven: {c}", [("opposite", "opposite")],
       pos="separate_sentence", dist="far", embed=1, bival=True),
    _F("rev5", "reverse", "Form the negation of the next claim. Claim: {c}. Is that negation true of the {doc}?",
       "the negation of the claim that {c} is true of the {doc}",
       "the negation of the claim that {c} is untrue of the {doc}", [("negation", "negation")],
       pos="separate_sentence", dist="next_sentence", embed=1),
    _F("rev6", "reverse", "Work with the reverse of a claim. That claim was copied from a tracking sheet. Claim: {c}. "
       "Is the reverse true of the {doc}?", "the reverse of the claim that {c} is true of the {doc}",
       "the reverse of the claim that {c} is untrue of the {doc}", [("reverse", "reverse")],
       pos="separate_sentence", dist="far", embed=1),
    # ---- answer mapping (item 13): negation in the answer mapping itself; never with yes/no lines
    _F("amp1", "answermap", "Answer yes if {c}; otherwise answer no.", "", "", embed=0, yn=False),
    _F("amp2", "answermap", "Answer no if {c}; otherwise answer yes.", "", "", [("answer no if", "answer no if")],
       pos="answer_map", embed=0, yn=False),
    _F("amp3", "answermap", "Say yes when {c}, and say no in every other case.", "", "", embed=0, yn=False),
    _F("amp4", "answermap", "Say no when {c}, and say yes in every other case.", "", "",
       [("say no when", "say no when")], pos="answer_map", embed=0, yn=False),
    _F("amp5", "answermap", "The answer is yes exactly when {c}.", "", "", embed=0, yn=False),
    _F("amp6", "answermap", "The answer is no exactly when {c}.", "", "", [("no exactly when", "no exactly when")],
       pos="answer_map", embed=0, yn=False),
    # ---- key: the claim is stated; the card's yes/no key carries the mapping (item 14 when inverted)
    _F("key1", "key", "Claim: {c}. Answer with the yes/no key in the card.", "", "", embed=0),
    _F("key2", "key", "The claim to check is this: {c}. Give the answer the card's key assigns.", "", "", embed=0),
    _F("key3", "key", "Check this claim against the {doc}: {c}. Answer by the card's key.", "", "", embed=0),
    _F("key4", "key", "Read the claim and use the key in the card. Claim: {c}.", "", "", embed=0),
    # ---- double: two outer cues (depth 3-4 with inner cues; item 10)
    _F("dbl1", "double", "Is it false that the {doc} fails to show that {cp}?",
       "it is false that the {doc} fails to show that {cp}", "it is true that the {doc} fails to show that {cp}",
       [("false", "false"), ("fail", "fails")], subj="pron", embed=2, bival=True),
    _F("dbl2", "double", "Is the claim that the {doc} refutes the note that {cp} unfounded?",
       "the claim that the {doc} refutes the note that {cp} is unfounded",
       "the claim that the {doc} refutes the note that {cp} is well founded",
       [("unfounded", "unfounded"), ("refute", "refutes")], subj="pron", embed=2, bival=True),
    _F("dbl3", "double", "Would a careful reader reject the claim that the {doc} fails to show that {cp}?",
       "a careful reader would reject the claim that the {doc} fails to show that {cp}",
       "a careful reader would accept the claim that the {doc} fails to show that {cp}",
       [("reject", "reject"), ("fail", "fails")], subj="pron", embed=2, bival=True),
    _F("dbl4", "double", "Is it untrue that nothing in the {doc} supports the claim that {cp}?",
       "it is untrue that nothing in the {doc} supports the claim that {cp}",
       "it is true that nothing in the {doc} supports the claim that {cp}",
       [("untrue", "untrue"), ("nothing", "nothing")], subj="pron", embed=2, bival=True),
    _F("dbl5", "double", "Is it false that the {doc} gives no support to the claim that {cp}?",
       "it is false that the {doc} gives no support to the claim that {cp}",
       "it is true that the {doc} gives no support to the claim that {cp}", [("false", "false"), ("no", "no")],
       subj="pron", embed=2, bival=True),
    _F("dbl6", "double", "Would a careful reader dispute that the {doc} fails to support the claim that {cp}?",
       "a careful reader would dispute that the {doc} fails to support the claim that {cp}",
       "a careful reader would grant that the {doc} fails to support the claim that {cp}",
       [("dispute", "dispute"), ("fail", "fails")], subj="pron", embed=2, bival=True),
    _F("dbl7", "double", "Is the claim that the {doc} contradicts the note that {cp} baseless?",
       "the claim that the {doc} contradicts the note that {cp} is baseless",
       "the claim that the {doc} contradicts the note that {cp} is well grounded",
       [("baseless", "baseless"), ("contradict", "contradicts")], subj="pron", embed=2, bival=True),
    # ---- inner-negative polar questions (item 38; always with full yes/no lines, <= 5% of rows)
    _F("pin1", "polar_inner", "{cq}?", "{c}", "{cneg}", embed=0, needs="cqn"),
    _F("pin2", "polar_inner", "Going by the {doc}, {cql}?", "{c}", "{cneg}", embed=0, needs="cqn"),
    _F("pin3", "polar_inner", "{cq}? Use the card's yes/no lines.", "{c}", "{cneg}", embed=0, needs="cqn"),
    _F("pin4", "polar_inner", "Reading the card first, {cql}?", "{c}", "{cneg}", embed=0, needs="cqn"),
    # ================================================= HELD-OUT families (dev_holdout only)
    _F("hv1", "verdict", "Would a verdict that {c} stand?", "a verdict that {c} would stand",
       "a verdict that {c} would fall", split="holdout", bival=True),
    _F("hv2", "verdict", "Would a review panel overturn the finding that {c}?",
       "a review panel would overturn the finding that {c}", "a review panel would uphold the finding that {c}",
       [("overturn", "overturn")], split="holdout", bival=True),
    _F("hv3", "verdict", "Would an appeals clerk rebut the finding that {c}?",
       "an appeals clerk would rebut the finding that {c}", "an appeals clerk would uphold the finding that {c}",
       [("rebut", "rebut")], split="holdout", bival=True),
    _F("hv4", "verdict", "Would the panel veto a ruling that {c}?", "the panel would veto a ruling that {c}",
       "the panel would endorse a ruling that {c}", [("veto", "veto")], split="holdout", bival=True),
    _F("hv5", "verdict", "Is the finding that {c} groundless?", "the finding that {c} is groundless",
       "the finding that {c} is well grounded", [("groundless", "groundless")], split="holdout", bival=True),
    _F("ha1", "audit", "An auditor checks the entry that {c}. Would the auditor call that entry erroneous?",
       "the auditor would call the entry that {c} erroneous", "the auditor would call the entry that {c} sound",
       [("erroneous", "erroneous")], dist="next_sentence", split="holdout"),
    _F("ha2", "audit", "An auditor checks the entry that {c}. Is that entry far from true?",
       "the entry that {c} is far from true", "the entry that {c} is true", [("far from true", "far from true")],
       dist="next_sentence", split="holdout"),
    _F("ha3", "audit", "An auditor checks the entry that {c}. Would the auditor sign it off as sound?",
       "the auditor would sign off the entry that {c} as sound", "the auditor would return the entry that {c} for rework",
       dist="next_sentence", split="holdout"),
    _F("ha4", "audit", "An auditor checks the entry that {c}. Is the entry groundless?",
       "the entry that {c} is groundless", "the entry that {c} is well grounded", [("groundless", "groundless")],
       dist="next_sentence", split="holdout", bival=True),
    _F("hc1", "contrary", "Consider the contrary of the claim that follows. Claim: {c}. Does the {doc} bear out that "
       "contrary?", "the {doc} bears out the contrary of the claim that {c}",
       "the {doc} leaves the contrary of the claim that {c} unproven", [("contrary", "contrary")],
       pos="separate_sentence", dist="next_sentence", split="holdout", bival=True),
    _F("hc2", "contrary", "Mark no if {c}; otherwise mark yes.", "", "", [("mark no if", "mark no if")],
       pos="answer_map", embed=0, split="holdout", yn=False),
    _F("hc3", "contrary", "Enter no if {c}; otherwise enter yes.", "", "", [("enter no if", "enter no if")],
       pos="answer_map", embed=0, split="holdout", yn=False),
    _F("hc4", "contrary", "Take the contrary of this claim. The claim was logged by a desk clerk. Claim: {c}. Is the "
       "contrary true of the {doc}?", "the contrary of the claim that {c} is true of the {doc}",
       "the contrary of the claim that {c} is untrue of the {doc}", [("contrary", "contrary")],
       pos="separate_sentence", dist="far", split="holdout"),
    # two held-out frames that put a truth-value cue together with a cross-sentence / answer-mapping cue: the held-out
    # depth-3 cue-class combinations (checklist rule 2.10) come from these alone
    _F("hc5", "contrary", "Take the contrary of the claim that follows. Claim: {c}. Is that contrary groundless?",
       "the contrary of the claim that {c} is groundless", "the contrary of the claim that {c} is well grounded",
       [("contrary", "contrary", "separate_sentence", "next_sentence"),
        ("groundless", "groundless", "outer_frame", "same_sentence")], split="holdout", bival=True),
    _F("hc6", "contrary", "Mark no if it is far from true that {c}; otherwise mark yes.", "", "",
       [("mark no if", "mark no if", "answer_map", "same_sentence"),
        ("far from true", "far from true", "outer_frame", "same_sentence")], embed=1, split="holdout", yn=False),
]
FRAMES = {f["id"]: f for f in FRAMES_LIST}
FAMILIES = sorted({f["family"] for f in FRAMES_LIST})
# the yes/no key of the key family: (inverted?, lexeme, yes line, no line); the claim is quoted in both lines
KEYS = [
    (False, None, 'the claim "{c}" holds for this {doc}', 'the claim "{c}" fails for this {doc}'),
    (False, None, 'the claim "{c}" is borne out by the {doc}', 'the claim "{c}" is left unproven by the {doc}'),
    (True, "fails to hold", 'the claim "{c}" fails to hold for this {doc}', 'the claim "{c}" holds for this {doc}'),
    (True, "is false of", 'the claim "{c}" is false of this {doc}', 'the claim "{c}" is true of this {doc}'),
]
# choice-row frames (instruction of a choice row). select: 'true' or 'false'; cue: the negated-selection cue.
CHOICE_FRAMES = [
    {"id": "chs1", "family": "choice", "q": "Which statement about the {doc} is true?", "select": "true", "cue": None},
    {"id": "chs2", "family": "choice", "q": "Which statement about the {doc} is false?", "select": "false",
     "cue": ("false", "false")},
    {"id": "chs3", "family": "choice", "q": "Which of these statements is untrue of the {doc}?", "select": "false",
     "cue": ("untrue", "untrue")},
    {"id": "chs4", "family": "choice", "q": "Which statement about the {doc} does hold?", "select": "true",
     "cue": None},
    {"id": "chs5", "family": "choice", "q": "Exactly one statement below is false. Which one is it?",
     "select": "false", "cue": ("false", "false")},
    {"id": "chs6", "family": "choice", "q": "Exactly one statement below does hold for the {doc}. Which one is it?",
     "select": "true", "cue": None},
    {"id": "chs7", "family": "choice", "q": "Which statement about the {doc} does not hold?", "select": "false",
     "cue": ("not", "not")},
    {"id": "chs8", "family": "choice", "q": "Exactly one statement below doesn't hold for the {doc}. Which one is it?",
     "select": "false", "cue": ("n't", "doesn't")},
]
FALSE_CHOICE_CUE = {f["id"]: f["cue"][0] for f in CHOICE_FRAMES if f["select"] == "false"}


# ============================================================================================ 4. card sources
# Card-format sources: real texts with their human gold labels. 'labels' maps the label name F7 shows to its
# Claude-written definition; 'gold' maps the source's gold label to that name (identity when absent). 'ordinal':
# the scale order (item 21: poles = ends, middle = the rest). 'golden': the golden_train source and the choice
# instruction prefix whose rows are eligible; 'raw': the data/v14_parts/raw file whose unused texts feed the dev.
# split 'train' sources feed train + dev_iid; 'holdout' sources feed dev_holdout only (whole held-out sources).
# r4 (yn2b/F7_BLIND_READ.md, the blind-read repair):
#   rule_open  the rule line of a residual card (item 22): the text's label is ONE label, listed below or not, so the
#              rule never claims that a listed line fits when the text's label is left off the card (4.A);
#   near       label pairs a careful reader can mistake for each other; a residual card never lists a label that is
#              near the left-off label (inhibitor next to a missing antagonist, 3.3 / 9.5);
#   tnoun      the noun a derived card term is defined over: the kind of thing the claim's subject is ('a name whose
#              label ...' for 'the marked name'), never the document noun (7, minor wording note);
#   evidence   texts are kept only when the text itself shows its human label as the card defines it (label-evidence
#              rules in section 4b and LABEL_EVIDENCE below, applied by the builder to train and dev pools alike).
# Retired sources (RETIRED_SOURCES): a careful reader cannot recover their human labels from the text and the card.
CARD_SOURCES = {
    "storm": dict(
        split="train", golden="gd_storm_ef", raw="storm_ef", doc="report", subj="the report",
        instr="Based on this National Weather Service storm-survey narrative",
        labels={
            "EF0": "the survey's estimated peak wind is 65 to 85 mph (light damage: shingles or siding peeled, "
                   "gutters bent, branches broken and shallow-rooted trees pushed over)",
            "EF1": "the survey's estimated peak wind is 86 to 110 mph (moderate damage: roofs badly stripped, mobile "
                   "homes rolled over, windows broken and many trees snapped or uprooted)",
            "EF2": "the survey's estimated peak wind is 111 to 135 mph (considerable damage: roofs torn off sturdy "
                   "houses, frame houses shifted, mobile homes destroyed and cars lifted)",
            "EF3": "the survey's estimated peak wind is 136 to 165 mph (severe damage: whole stories of sturdy houses "
                   "destroyed, large buildings badly damaged and heavy cars thrown)",
        },
        ordinal=["EF0", "EF1", "EF2", "EF3"],
        rule="the survey assigned exactly one of the ratings below, by the peak wind it estimated",
        rule_open="the survey assigned exactly one EF rating, by the peak wind it estimated: one of the ratings below "
                  "or another rating",
        wind={"EF0": (65, 85), "EF1": (86, 110), "EF2": (111, 135), "EF3": (136, 165)}, near=[]),
    "ncbi": dict(
        split="train", golden="gd_ncbi_disease", raw="ncbi_disease", doc="sentence", subj="the marked mention",
        pron="it", instr="According to the NCBI disease-mention categories",
        labels={
            "specific disease": "the marked words, used as a noun phrase, name one particular disease or syndrome, "
                                "often by a proper name or an abbreviation, such as Friedreich ataxia or PKU",
            "disease class": "the marked words, used as a noun phrase, name a broad family of diseases: a general "
                             "head word such as disorder, tumour, cancer or anomaly, or a plural",
            "modifier": "the marked disease name describes another word that follows it, such as gene, protein, "
                        "patients or family, instead of standing as a disease noun phrase",
        },
        rule="the marked mention belongs to exactly one of the categories below",
        rule_open="the marked mention belongs to exactly one category: one of the categories below or another category",
        tnoun="mention", near=[("specific disease", "disease class"), ("specific disease", "modifier")]),
    "medquad": dict(
        split="train", golden="gd_medquad_qtype", raw="medquad_qtype", doc="passage", subj="the passage",
        instr="Which consumer-health question", gold={"treatment": "treatment options", "prevention": "prevention steps"},
        labels={
            "causes": "explains why the condition arises: the mechanism, gene change or infectious or environmental "
                      "agent behind it",
            "treatment options": "explains how the condition is treated or managed: therapies, drugs, surgery and other care",
            "signs and symptoms": "lists the complaints, findings and visible changes a person with the "
                                  "disorder tends to have",
            "diagnosis and tests": "covers the checks doctors run to find or confirm the disorder, such as "
                                   "blood work, scans or gene panels",
            "inheritance pattern": "states how the condition passes down in families and the chance that relatives "
                                   "are affected",
            "prevention steps": "describes steps that lower the chance of getting the condition or of spreading it",
        },
        rule="the passage answers exactly one of the question types below",
        rule_open="the passage answers exactly one question type: one of the types below or another type",
        near=[("causes", "inheritance pattern"), ("signs and symptoms", "diagnosis and tests"),
              ("treatment options", "prevention steps")]),
    "edgar": dict(
        split="train", golden="gd_edgar_10k_item", raw="edgar_10k_item", doc="passage", subj="the passage",
        instr="Which item of a company's Form 10-K",
        labels={
            "Item 1 - Business": "describes what the company does: its history, products, segments, customers, "
                                 "markets, competition and the rules it works under",
            "Item 1A - Risk Factors": "lists material risks, phrased as what could happen and how that could hurt "
                                      "the business, its results or its stock",
            "Item 2 - Properties": "describes the offices, plants, stores, land or other physical sites the company "
                                   "owns or leases",
            "Item 3 - Legal Proceedings": "describes lawsuits, investigations or regulatory proceedings that involve "
                                          "the company, and where they stand",
            "Item 7 - MD&A": "management's discussion of the period's results, why they changed, liquidity, cash "
                             "flows and outlook",
            "Item 8 - Financial Statements and Notes": "the audited statements and the notes on accounting "
                                                       "policies, balances, debt, leases, taxes and equity",
        },
        rule="the passage comes from exactly one of the report items below",
        rule_open="the passage comes from exactly one report item: one of the items below or another item",
        near=[("Item 1 - Business", "Item 1A - Risk Factors"), ("Item 7 - MD&A", "Item 8 - Financial Statements and Notes"),
              ("Item 1 - Business", "Item 2 - Properties"), ("Item 1 - Business", "Item 7 - MD&A"),
              ("Item 2 - Properties", "Item 7 - MD&A"), ("Item 2 - Properties", "Item 8 - Financial Statements and Notes")]),
    "sd311": dict(
        split="train", golden="gd_sd311_routing", raw="sd311_routing", doc="request", subj="the request",
        instr="Which City of San Diego 311 request type", gold={"illegal dumping": "dumped debris"},
        labels={
            "pothole repair": "a distinct hole in the asphalt of a street or alley that needs patching",
            "street light repair": "a street light that is out, flickering, lit during the day or on a damaged pole",
            "dumped debris": "trash, furniture, appliances or debris that someone left on a public street, "
                               "sidewalk, alley or lot",
            "parking violation": "a vehicle parked in a restricted spot, blocking a driveway, stored on the street "
                                 "for days or abandoned",
            "sidewalk repair": "public sidewalk slabs that are cracked, lifted or broken and create a trip hazard",
            "tree trimming or fallen tree": "a street tree that needs trimming, has fallen or hanging limbs, or has "
                                            "died",
        },
        rule="the request goes to exactly one of the request types below",
        rule_open="the request goes to exactly one request type: one of the types below or another type",
        near=[("pothole repair", "sidewalk repair"), ("dumped debris", "tree trimming or fallen tree"),
              ("dumped debris", "parking violation")]),
    "smcal": dict(
        split="train", golden="gd_smcalflow_action", raw="smcalflow_action", doc="dialogue",
        subj="the user's latest message", pron="it", instr="How should the calendar assistant handle", excl_unit="message",
        labels={
            "create a new event": "the user asks to put one new, fully specified event on the calendar",
            "delete an event": "the user asks to cancel or remove one specific event that is already on the calendar",
            "change an existing event": "the user asks to move, extend, rename or otherwise edit an event already "
                                        "saved on the calendar",
            "answer a weather question": "the user asks about current or forecast weather for a place and time the "
                                         "forecast covers",
            "answer a question about a place": "the user asks for facts about a named business or place, such as "
                                               "its address, hours, rating or phone number",
            "answer a question about the calendar": "the user wants facts about their own schedule, such as "
                                                    "what is booked, when a saved meeting starts or who is invited",
        },
        rule="the latest message calls for exactly one of the actions below",
        rule_open="the latest message calls for exactly one action: one of the actions below or another action",
        tnoun="message", near=[("create a new event", "change an existing event"),
                               ("delete an event", "change an existing event"),
                               ("change an existing event", "answer a question about the calendar")]),
    "drugprot": dict(
        split="train", golden="gd_drugprot", raw="drugprot", doc="sentence",
        subj="the marked chemical-gene pair", pron="it", instr="Which chemical-protein relation",
        labels={
            "inhibitor": "the sentence says the compound inhibits, blocks or lowers what the protein does (a compound "
                         "the sentence calls an antagonist gets that label instead)",
            "activator": "the sentence says the compound activates, induces or raises what the protein does (a "
                         "compound the sentence calls an agonist gets that label instead)",
            "substrate": "the protein, working as an enzyme or carrier, processes the compound by breaking it "
                         "down, changing it or moving it across a membrane",
            "antagonist": "the sentence calls the chemical an antagonist of the gene product, usually a receptor: it "
                          "binds the receptor and blocks its response",
            "agonist": "the sentence calls the chemical an agonist of the gene product, usually a receptor: it "
                       "binds the receptor and triggers its response",
            "part of": "the compound is a building block inside the protein itself, for instance one residue or "
                       "an attached sugar group",
        },
        rule="the sentence states exactly one of the relations below for the marked pair",
        rule_open="the sentence states exactly one relation for the marked pair: one of the relations below or "
                  "another relation",
        tnoun="pair", near=[("inhibitor", "antagonist"), ("activator", "agonist"), ("agonist", "antagonist"),
                            ("inhibitor", "activator")]),
    # ---------------------------------------------------------------- HELD-OUT sources (dev_holdout only)
    "safer": dict(
        split="holdout", golden="gd_saferproducts_severity", raw="saferproducts_severity", doc="report",
        subj="the report", instr="Based on this consumer product incident report",
        gold={"no incident, no injury": "slight", "incident, but no injury": "slight",
              "injury, no first aid or medical care": "slight", "injury, first aid by a non-medical person": "middling",
              "injury, seen by a medical professional": "middling", "injury, emergency department treatment": "grave",
              "injury, hospital admission": "grave", "death": "grave"},
        labels={
            "slight": "the report shows at most a small injury to the primary victim, one that got neither first "
                      "aid nor medical care",
            "middling": "the primary victim got first aid from a lay person or was seen by a doctor, nurse or clinic "
                        "outside an emergency room",
            "grave": "the primary victim was treated in an emergency room, admitted to hospital or died",
        },
        ordinal=["slight", "middling", "grave"], rule="the report falls into exactly one of the outcome tiers below",
        rule_open="the report falls into exactly one outcome tier: one of the tiers below or another tier",
        near=[("slight", "middling"), ("middling", "grave")]),
    "wiki": dict(
        split="holdout", golden="gd_wiki_help_routing", raw="wiki_help_routing", doc="post", subj="the post", excl_unit="post",
        instr="Which Wikipedia",
        labels={
            "Computing reference desk": "questions about computers, software, programming, the internet and device "
                                        "problems",
            "Language reference desk": "asks how a word or phrase is used, spelled, said, translated or where it "
                                       "came from",
            "Science reference desk": "questions about the natural and applied sciences, medicine, astronomy and "
                                      "engineering, software aside",
            "Humanities reference desk": "asks about past events, government, faith, ideas, money matters, "
                                         "literature or the arts",
            "Help desk": "asks how to work the encyclopedia itself, for instance starting a page, adding a "
                         "citation, laying out a table or fixing a login",
            "Reliable sources noticeboard": "whether a given outlet, book, website or paper is reliable enough to "
                                            "cite for a statement in an article",
        },
        rule="the post belongs at exactly one of the places below",
        rule_open="the post belongs at exactly one place: one of the places below or another place",
        near=[("Computing reference desk", "Science reference desk"),
              ("Science reference desk", "Humanities reference desk"),
              ("Humanities reference desk", "Language reference desk"),
              ("Help desk", "Reliable sources noticeboard"), ("Help desk", "Computing reference desk")]),
}
# binary property sources (card format, two labels): P = the property holds. pos/neg: the two label names and their
# definitions. 'forms': the property's own claim wordings by lexeme tuple (outermost first): (decl, interrogative or
# None, surfaces). {S} is the subject.
PROP_SOURCES = {
    "injury": dict(
        split="train", golden="gd_nhtsa_complaints", raw="nhtsa_complaints", doc="complaint", subj="the complaint",
        pron="it", instr="Does this vehicle safety complaint report that at least one person was actually injured?",
        gold1=True, pos=("injury case", "the complaint says that at least one person was actually hurt in the "
                                        "incident, with any injury at all, burns and airbag injuries included"),
        neg=("intact case", "the complaint says everyone came through the incident physically intact, or it "
                            "describes only a risk of harm"),
        forms={
            (): [("{S} reports that someone was actually hurt", "Does {S} report that someone was actually hurt"),
                 ("{S} describes an injury case", "Does {S} describe an injury case")],
            ("not",): [("{S} does not report that anyone was actually hurt", None),
                       ("{S} does not describe an injury case", None)],
            ("n't",): [("{S} doesn't report that anyone was actually hurt", None)],
            ("no",): [("{S} reports no injury to anyone", "Does {S} report no injury to anyone")],
            ("nobody",): [("{S} reports that nobody was actually hurt", "Does {S} report that nobody was actually hurt")],
            ("never",): [("{S} never says that someone was actually hurt", "Does {S} never say that someone was actually hurt")],
            ("-free",): [("{S} describes an injury-free incident", "Does {S} describe an injury-free incident")],
            ("non-",): [("{S} describes a non-injury incident", "Does {S} describe a non-injury incident")],
            ("fail",): [("{S} fails to report that anyone was actually hurt", "Does {S} fail to report that anyone was actually hurt")],
            ("omit",): [("{S} omits any report of an injury", "Does {S} omit any report of an injury")],
            ("not", "-free"): [("{S} does not describe an injury-free incident", None)],
            ("not", "non-"): [("{S} does not describe a non-injury incident", None)],
            ("not", "fail"): [("{S} does not fail to report that someone was actually hurt", None)],
        },
        ar=("{S} describes an intact case", "Does {S} describe an intact case")),
    "fire": dict(
        split="train", golden="gd_nhtsa_complaints", raw="nhtsa_complaints", doc="complaint", subj="the complaint",
        pron="it", instr="Does this vehicle safety complaint report that the vehicle actually caught fire?", gold1=True,
        pos=("fire case", "according to the complaint, flames actually broke out on or in the vehicle"),
        neg=("smoke-only case", "the complaint describes at most smoke, a burning smell, overheating, melting or a "
                                "fire that could happen"),
        forms={
            (): [("{S} reports that the vehicle actually caught fire", "Does {S} report that the vehicle actually caught fire")],
            ("not",): [("{S} does not report that the vehicle actually caught fire", None)],
            ("n't",): [("{S} doesn't report that the vehicle actually caught fire", None)],
            ("no",): [("{S} reports no actual fire in the vehicle", "Does {S} report no actual fire in the vehicle")],
            ("never",): [("{S} never says that the vehicle actually caught fire", None)],
            ("fail",): [("{S} fails to report that the vehicle actually caught fire", "Does {S} fail to report that the vehicle actually caught fire")],
            ("-free",): [("{S} describes a fire-free incident", "Does {S} describe a fire-free incident")],
            ("not", "fail"): [("{S} does not fail to report an actual fire", None)],
            ("not", "-free"): [("{S} does not describe a fire-free incident", None)],
        },
        ar=("{S} describes a smoke-only case", "Does {S} describe a smoke-only case")),
    "crash": dict(
        split="train", golden="gd_nhtsa_complaints", raw="nhtsa_complaints", doc="complaint", subj="the complaint",
        pron="it", instr="Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
        gold1=True, pos=("crash case", "according to the complaint, the vehicle really collided with something: a car, "
                                       "a pole, a wall, a person or any other object"),
        neg=("defect-only case", "the complaint describes a defect, a near miss or a crash that could happen, and "
                                 "the vehicle itself stayed clear of any collision"),
        forms={
            (): [("{S} reports an actual crash of the vehicle", "Does {S} report an actual crash of the vehicle")],
            ("not",): [("{S} does not report an actual crash of the vehicle", None)],
            ("no",): [("{S} reports no actual crash of the vehicle", "Does {S} report no actual crash of the vehicle")],
            ("never",): [("{S} never reports an actual crash of the vehicle", None)],
            ("fail",): [("{S} fails to report an actual crash of the vehicle", "Does {S} fail to report an actual crash of the vehicle")],
            ("-free",): [("{S} describes a crash-free incident", "Does {S} describe a crash-free incident")],
            ("lack",): [("{S} lacks any report of an actual crash", "Does {S} lack any report of an actual crash")],
            ("not", "-free"): [("{S} does not describe a crash-free incident", None)],
            ("not", "lack"): [("{S} does not lack a report of an actual crash", None)],
        },
        ar=("{S} describes a defect-only case", "Does {S} describe a defect-only case")),
    "faithful": dict(
        split="train", golden="gd_faithdial", raw="faithdial", doc="dialogue", subj="the wizard's response",
        tnoun="response", pron="it", instr="Is everything the wizard's response asserts supported by the knowledge snippet?", gold1=True,
        pos=("grounded response", "every factual claim in the response is stated in or follows directly from the knowledge "
                         "snippet; questions, greetings and hedges are fine"),
        neg=("embellished response", "the response asserts at least one thing beyond the snippet, such as an extra fact, a "
                            "contradiction or a personal feeling given as its own"),
        forms={
            (): [("{S} is faithful to the snippet", "Is {S} faithful to the snippet")],
            ("not",): [("{S} is not faithful to the snippet", "Is {S} not faithful to the snippet")],
            ("un-",): [("{S} is unfaithful to the snippet", "Is {S} unfaithful to the snippet")],
            ("fail",): [("{S} fails to stay faithful to the snippet", "Does {S} fail to stay faithful to the snippet")],
            ("not", "un-"): [("{S} is not unfaithful to the snippet", None)],
            ("not", "fail"): [("{S} does not fail to stay faithful to the snippet", None)],
        },
        ar=("{S} is an embellished response", "Is {S} an embellished response")),
    "found": dict(
        split="train", golden="gd_multiwoz21_sysacts", raw="multiwoz21_sysacts", doc="dialogue",
        subj="the assistant's last turn", tnoun="turn", pron="it",
        instr="In its reply, did the assistant find at least one option that meets everything the customer asked "
              "for?", gold1=True,
        pos=("match found", "the assistant names, offers or says there is at least one hotel, venue or train that "
                            "satisfies every need the customer has stated so far, even if it then asks for more details"),
        neg=("dead end", "the assistant says that every candidate misses at least one of the customer's needs, "
                         "even if it then offers to relax one of them"),
        forms={
            (): [("{S} offers an option that meets every stated need", "Does {S} offer an option that meets every stated need")],
            ("not",): [("{S} does not offer an option that meets every stated need", None)],
            ("no",): [("{S} offers no option that meets every stated need", "Does {S} offer no option that meets every stated need")],
            ("fail",): [("{S} fails to offer an option that meets every stated need", "Does {S} fail to offer an option that meets every stated need")],
            ("nothing",): [("{S} finds nothing that meets every stated need", "Does {S} find nothing that meets every stated need")],
            ("not", "fail"): [("{S} does not fail to offer an option that meets every stated need", None)],
        },
        ar=("{S} reaches a dead end", "Does {S} reach a dead end")),
    # ---------------------------------------------------------------- HELD-OUT property source
    "toxic": dict(
        split="holdout", golden=None, raw=None, doc="comment", subj="the comment", pron="it", instr=None, gold1=True,
        pos=("toxic", "the comment is rude, insulting, threatening or demeaning toward someone"),
        neg=("civil", "the comment treats everyone it mentions with ordinary respect, even when it disagrees"),
        forms={
            (): [("{S} is toxic", "Is {S} toxic")],
            ("not",): [("{S} is not toxic", "Is {S} not toxic")],
            ("non-",): [("{S} is non-toxic", "Is {S} non-toxic")],
            ("not one",): [("not one word of {S} is toxic", None)],
            ("fail",): [("{S} fails to be toxic", None)],
            ("not", "non-"): [("{S} is not non-toxic", None)],
            ("no",): [("{S} contains no toxic language", "Does {S} contain no toxic language")],
        },
        ar=("{S} is civil", "Is {S} civil")),
}

# ---- claim wordings for a card label L (multi-class and ordinal sources), by inner lexeme tuple (outermost first).
# Each entry: (declarative, interrogative or None, inner-negative interrogative or None). {S} subject, {L} label.
LABEL_FORMS = {
    (): [("{S} fits '{L}'", "Does {S} fit '{L}'", None), ("'{L}' applies to {S}", "Does '{L}' apply to {S}", None),
         ("{S} falls under '{L}'", "Does {S} fall under '{L}'", None),
         ("'{L}' is the label that fits {S}", "Is '{L}' the label that fits {S}", None)],
    ("not",): [("{S} does not fit '{L}'", None, "Does {S} not fit '{L}'"),
               ("'{L}' does not apply to {S}", None, "Does '{L}' not apply to {S}"),
               ("{S} does not fall under '{L}'", None, "Does {S} not fall under '{L}'"),
               ("'{L}' is not the label that fits {S}", None, None)],
    ("n't",): [("{S} doesn't fit '{L}'", None, None), ("'{L}' doesn't apply to {S}", None, None),
               ("'{L}' isn't the label that fits {S}", None, None)],
    ("cannot",): [("'{L}' cannot be the label that fits {S}", None, None), ("{S} cannot fall under '{L}'", None, None)],
    ("fail",): [("{S} fails to fit '{L}'", "Does {S} fail to fit '{L}'", None),
                ("'{L}' fails to apply to {S}", "Does '{L}' fail to apply to {S}", None)],
    ("exclude",): [("the definitions exclude {S} from '{L}'", "Do the definitions exclude {S} from '{L}'", None)],
    ("rule out",): [("the definitions rule out '{L}' for {S}", "Do the definitions rule out '{L}' for {S}", None)],
    ("miss",): [("{S} misses the mark for '{L}'", "Does {S} miss the mark for '{L}'", None)],
    ("lack",): [("{S} lacks what '{L}' requires", "Does {S} lack what '{L}' requires", None)],
    ("in-",): [("'{L}' is inapplicable to {S}", "Is '{L}' inapplicable to {S}", None)],
    ("not", "in-"): [("'{L}' is not inapplicable to {S}", None, "Is '{L}' not inapplicable to {S}")],
    ("non-",): [("'non-{L}' fits {S}", "Does 'non-{L}' fit {S}", None),
                ("{S} falls under 'non-{L}'", "Does {S} fall under 'non-{L}'", None)],
    ("not", "fail"): [("{S} does not fail to fit '{L}'", None, None),
                      ("'{L}' does not fail to apply to {S}", None, None)],
    ("n't", "fail"): [("{S} doesn't fail to fit '{L}'", None, None)],
    ("not", "non-"): [("'non-{L}' does not fit {S}", None, None), ("{S} does not fall under 'non-{L}'", None, None)],
    ("fail", "non-"): [("{S} fails to fit 'non-{L}'", "Does {S} fail to fit 'non-{L}'", None)],
    ("not", "exclude"): [("the definitions do not exclude {S} from '{L}'", None, None)],
    ("not", "rule out"): [("the definitions do not rule out '{L}' for {S}", None, None)],
    ("not", "lack"): [("{S} does not lack what '{L}' requires", None, None)],
    ("not", "miss"): [("{S} does not miss the mark for '{L}'", None, None)],
}
# item 24 ('only' with negation): the card says exactly one listed label fits, so 'L is the only label that fits' = fit(L)
ONLY_FORMS = {
    (): [("'{L}' is the only listed label that fits {S}", "Is '{L}' the only listed label that fits {S}", None)],
    ("not",): [("'{L}' is not the only listed label that fits {S}", None, None)],
    ("n't",): [("'{L}' isn't the only listed label that fits {S}", None, None)],
}
# item 32 (contrastive): 'the label that fits S is not X but Y' = (not fit X) and fit Y
CONTRAST_FORMS = {
    ("not",): [("the label that fits {S} is not '{L}' but '{Y}'", None, None),
               ("{S} fits not '{L}' but '{Y}'", None, None)],
}
# derived card terms (card_def negation, item 11): the term's definition carries one negation of fit(L)
TERM_NAMES = ["tag K", "code M", "mark R", "flag V", "badge Z", "stamp P", "token W", "sticker J"]
TERM_DEFS = {
    "not": "a {doc} whose label is not '{L}'",
    "n't": "a {doc} whose label isn't '{L}'",
    "fail": "a {doc} that fails to fit '{L}'",
    "lack": "a {doc} that lacks what '{L}' requires",
    "exclude": "a {doc} that the definitions exclude from '{L}'",
    "rule out": "a {doc} for which the definitions rule out '{L}'",
    "non-": "a non-{L} {doc}",
    "unless": "applies to every {doc} unless its label is '{L}'",
    "never": "a {doc} that '{L}' never covers",
    "without": "a {doc} without the features of '{L}'",
    "no": "a {doc} with no claim to '{L}'",
}
# claims about a derived term T (generic for every kind; {S} subject)
TERM_FORMS = {
    (): [("'{T}' applies to {S}", "Does '{T}' apply to {S}", None), ("{S} counts as '{T}'", "Does {S} count as '{T}'", None)],
    ("not",): [("'{T}' does not apply to {S}", None, "Does '{T}' not apply to {S}"),
               ("{S} does not count as '{T}'", None, "Does {S} not count as '{T}'")],
    ("n't",): [("'{T}' doesn't apply to {S}", None, None), ("{S} doesn't count as '{T}'", None, None)],
    ("fail",): [("'{T}' fails to apply to {S}", "Does '{T}' fail to apply to {S}", None),
                ("{S} fails to count as '{T}'", "Does {S} fail to count as '{T}'", None)],
    ("cannot",): [("{S} cannot count as '{T}'", None, None)],
    ("not", "fail"): [("'{T}' does not fail to apply to {S}", None, None)],
}
# residual label (item 22): the card lists some labels plus 'something else'; P = S fits one of the listed lines
RESIDUAL_NAME = "something else"
RESIDUAL_DEF = {"none": "the {noun} fits none of the label lines above", "no": "no label line above fits the {noun}",
                "not": "the {noun} does not fit any label line above"}
RESIDUAL_FORMS = {
    (): [("{S} fits one of the card's first {n} label lines", "Does {S} fit one of the card's first {n} label lines",
          None)],
    ("none",): [("{S} fits none of the card's first {n} label lines", None, None)],
    ("not",): [("{S} does not fit any of the card's first {n} label lines", None, None)],
    ("no",): [("no label line among the card's first {n} fits {S}", None, None)],
    ("fail",): [("{S} fails to fit any of the card's first {n} label lines",
                 "Does {S} fail to fit any of the card's first {n} label lines", None)],
}
# item 23 (exclusion clause): a term whose definition excludes texts that contain a question mark. The exclusion is
# part of the term's meaning (the core atom), so the questions about the term carry the negations F7 counts. {unit} is
# the unit the question asks about (the source's excl_unit: 'message' for the user's latest message, 'post' for the
# post), and the question mark is looked for in that unit only; the builder also keeps only texts where that unit and
# the whole state agree on a question mark, so no reading of the definition changes a gold (decide2 finding #2).
EXCLUSION_DEF = "a {unit} that fits '{L}', except one that contains a question mark"
EXCL_SOURCES = ("smcal", "wiki")
# item 25 (broader term spelled out as a list): group names per source (members are label names)
GROUPS = {
    "storm": [("strong-tornado rating", ["EF2", "EF3"]), ("weak-tornado rating", ["EF0", "EF1"])],
    "medquad": [("care question", ["treatment options", "prevention steps"]),
                ("origin question", ["causes", "inheritance pattern"])],
    "sd311": [("street-surface problem", ["pothole repair", "sidewalk repair"]),
              ("street-side clutter", ["dumped debris", "parking violation"])],
    "smcal": [("calendar edit", ["create a new event", "delete an event", "change an existing event"]),
              ("lookup question", ["answer a weather question", "answer a question about a place"])],
    "drugprot": [("receptor binding", ["antagonist", "agonist"]), ("activity change", ["inhibitor", "activator"])],
    "wiki": [("reference question", ["Computing reference desk", "Language reference desk", "Science reference desk",
                                     "Humanities reference desk"])],
}


# ============================================================================================ 5. multi-text sources
# State = 2-5 real labelled texts in one numbered list. Each text's property x_i comes from its human gold label.
# sg / base: the property as a singular verb phrase and its base form; adj / negadj / comp: adjective, its affixal
# negation and an affirmative complement (each optional). prop: how x_i is read from the base row.
MULTI_SOURCES = {
    "sd311_pothole": dict(split="train", src="sd311", label="pothole repair", item="request", items="requests",
                          Item="Request", sg="asks for pothole repair", base="ask for pothole repair",
                          negadj="non-pothole", negadj_aff="non-",
                          comp_sg="concerns some other kind of repair or problem",
                          comp_base="concern some other kind of repair or problem",
                          define="a request asks for pothole repair when it reports a distinct hole in the asphalt of a "
                                 "street or alley that needs patching"),
    "sd311_light": dict(split="train", src="sd311", label="street light repair", item="request", items="requests",
                        Item="Request", sg="concerns a street light", base="concern a street light",
                        negadj="non-lighting", negadj_aff="non-",
                        comp_sg="concerns something other than street lighting",
                        comp_base="concern something other than street lighting",
                        define="a request concerns a street light when it reports a street light that is out, "
                               "flickering, lit during the day or on a damaged pole"),
    "nhtsa_injury": dict(split="train", src="injury", item="complaint", items="complaints", Item="Complaint",
                         sg="reports an injury", base="report an injury", negadj="injury-free", negadj_aff="-free",
                         comp_sg="describes an intact case", comp_base="describe an intact case",
                         define="a complaint reports an injury when it says that at least one person was actually "
                                "hurt in the incident; it describes an intact case when everyone came through "
                                "physically intact or it describes only a risk of harm"),
    "nhtsa_crash": dict(split="train", src="crash", item="complaint", items="complaints", Item="Complaint",
                        sg="reports an actual crash", base="report an actual crash", negadj="crash-free",
                        negadj_aff="-free", comp_sg="describes a defect-only case", comp_base="describe a defect-only case",
                        define="a complaint reports an actual crash when, by its account, the vehicle really "
                               "collided with something, a car, a pole, a wall or a person included; it describes a "
                               "defect-only case when the vehicle itself stayed clear of any collision"),
    "oiics_fall": dict(split="train", src="oiics", label="fall to lower level", item="narrative", items="narratives",
                       Item="Narrative", sg="describes a fall to a lower level", base="describe a fall to a lower level",
                       negadj="non-fall", negadj_aff="non-",
                       comp_sg="describes some other kind of event", comp_base="describe some other kind of event",
                       define="a narrative describes a fall to a lower level when the worker fell from a higher place "
                              "to a lower one, such as off a ladder, roof, vehicle or stairs; a fall on the same "
                              "level and a deliberate jump are other kinds of event",
                       # r4 label evidence (yn2b/F7_BLIND_READ.md 6): a fall text names the height it fell from; the
                       # other texts come from event types far from a fall and never mention a height
                       pos_need=r"\b(?:off|from|down|through|thru)\b|\b\d+\s*(?:ft|feet|foot|fth)\b",
                       pos_drop=r"\bjump\w*",
                       neg_block=["jump to lower level", "fall on same level", "slip or trip without a fall",
                                  "fall stopped by personal fall arrest system",
                                  "struck, caught or crushed in collapsing structure or material"],
                       neg_drop=r"\b(?:fell|falls?|falling|slipped|tripped)\b[^.]{0,60}\b(?:off|from|down|ladder|"
                                r"roof|stairs?|steps?|curb|dock|scaffold\w*|platform|stool|chair|truck|trailer)\b"),
    "oiics_struck": dict(split="train", src="oiics", label="struck by object or equipment", item="narrative",
                         items="narratives", Item="Narrative", sg="describes a worker struck by a moving object",
                         base="describe a worker struck by a moving object", negadj="non-impact", negadj_aff="non-",
                         comp_sg="describes some other kind of event", comp_base="describe some other kind of event",
                         define="a narrative describes a worker struck by a moving object when an object or a piece "
                                "of equipment fell, swung, rolled, slid or flew into the worker; being hit by a "
                                "vehicle of any kind or by another person, and walking or bumping into something, are "
                                "other kinds of event",
                         # r4 label evidence (yn2b/F7_BLIND_READ.md 3.2 / 6): OIICS codes a worker hit by a car,
                         # forklift or person as a transport or person event, so a struck text never involves a
                         # vehicle or a person, and the other texts come only from event types far from an impact
                         pos_drop=r"\b(?:cars?|trucks?|vehicles?|fork ?lifts?|vans?|bus|pickup|suv|motorcycle|tractor|"
                                  r"golf cart|carts?|loader|backed|backing|ran over|run over|pallet jack|hi-?lo|"
                                  r"lift truck|train|trolley|bike|bicycle|mva|mvc|someone|somebody|co-?workers?|"
                                  r"patients?|person|customers?|students?|inmates?|clients?|residents?|child|"
                                  r"punched|kicked|assault\w*|fight|altercation|combative|attacked|threw|thrown)\b",
                         neg_block=["pedestrian struck by vehicle", "injury by person, unintentional or intent unknown",
                                    "intentional injury by person", "struck against object or equipment",
                                    "contact with object or equipment, mechanism unspecified",
                                    "struck, caught or crushed in collapsing structure or material",
                                    "caught in or compressed by equipment or objects", "roadway motor vehicle incident",
                                    "non-roadway motorized land vehicle incident", "rail vehicle incident",
                                    "water vehicle incident", "aircraft incident",
                                    "animal-ridden or non-motorized vehicle incident", "animal or insect related incident",
                                    "explosion", "rubbed or abraded by friction, pressure or foreign matter",
                                    "rubbed, abraded or jarred by vibration",
                                    "needlestick without exposure to a harmful substance"],
                         neg_drop=r"\b(?:hit|hits|hitting|struck|strikes?|striking|knocked|ran over|run over|bumped|"
                                  r"collided|pinned|crushed|flew|flying|swung|swinging|rolled|landed on|fell on|"
                                  r"fell onto|dropped on|came down on)\b"),
    "nhtsa_fire": dict(split="train", src="fire", item="complaint", items="complaints", Item="Complaint",
                       sg="reports an actual vehicle fire", base="report an actual vehicle fire", negadj="fire-free",
                       negadj_aff="-free", comp_sg=None, comp_base=None,
                       define="a complaint reports an actual vehicle fire when, by its account, flames really broke out "
                              "on or in the vehicle; smoke, a burning smell, overheating or a fire that could happen "
                              "by itself makes a smoke-only case"),
    # ---- held out
    "toxic_batch": dict(split="holdout", src="toxic", item="comment", items="comments", Item="Comment", sg="is toxic",
                        base="be toxic", adj="toxic", negadj="non-toxic", negadj_aff="non-", comp_sg="is civil",
                        comp_base="be civil",
                        define="a comment is toxic when it is rude, insulting, threatening or demeaning toward "
                               "someone; it is civil when it treats everyone it mentions with ordinary respect"),
    "wiki_lang": dict(split="holdout", src="wiki", label="Language reference desk", item="post", items="posts",
                      Item="Post", sg="belongs at the Language reference desk",
                      base="belong at the Language reference desk", negadj="non-language", negadj_aff="non-",
                      comp_sg="belongs somewhere other than the Language reference desk",
                      comp_base="belong somewhere other than the Language reference desk",
                      define="a post belongs at the Language reference desk when it asks about words or languages: "
                             "meaning, grammar, spelling, pronunciation, origin or translation"),
}
MULTI_GOLDEN = {"oiics": ("gd_oiics_event", "oiics_event", "Which OIICS event category")}
LOGIC_LINE = "quantifiers are read logically: 'not all' means at least one is not, and 'few' means at most one"
NUMBER_WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


# ============================================================================================ 4b. label evidence (r4)
# The blind read (yn2b/F7_BLIND_READ.md) found no composition error: every wrong or ambiguous gold came from a card
# line that contradicted the state or from a human label the card's definition does not bear out. r4 therefore keeps
# a real text only when the text itself shows its human label the way the card defines it. These are template-level
# rules over whole sources (the builder applies them to every train and dev pool); no single row is dropped by hand.
#
# Retired sources: a careful reader cannot recover the human label from the text plus any card F7 can write.
RETIRED_SOURCES = {
    "gd_onestop_level": "the reading level of one excerpt (elementary / intermediate / advanced) is a relative "
                        "judgement; sentence length and word length overlap across the three levels (median sentence "
                        "length 17.7 / 20.4 / 24.3 words), and the blind reader missed 4 rows on it",
    "br_casino": "CaSiNo utterances often carry two strategies (empathy and coordination in one offer), so 'exactly one "
                 "strategy' is false for many texts (blind read 4.C)",
    "br_claimbuster": "check-worthiness is a judgement the card cannot pin down (blind read 4.B and 5)",
    "gd_wnut17": "a tweet gives too little context to tell the entity types apart (iTunes as a product or a company, "
                 "Halo as a product or a title, Forgotten Door labelled a place in 'June Fest 2010 ~ Forgotten Door "
                 "LIVE!'; blind read 5, low-confidence 'Steve Dave')",
    "gd_sc101": "the 'bad' label covers unwise or self-directed acts ('eating too many snacks before dinner') that "
                "no short definition marks as objectionable, and some 'OK' acts read as bad (blind read 4.B)",
}
# NHTSA complaint flags (fire / injury / crash) are component or count flags, not a reading of the narrative. A text is
# kept only when the narrative states the event for a yes label and never states it for a no label. A phrase does not
# state the event when one of NHTSA_HYPO sits in the 4 words before it, in the same sentence ('could catch fire',
# 'almost caused an accident', 'no injuries', 'to prevent fire').
NHTSA_HYPO = (r"\b(?:could|might|may|would|will|can|almost|nearly|narrowly|not|never|no|afraid|fear(?:ful|ing|s)?|"
              r"risk(?:ing|s)?|potential(?:ly)?|possibl[ey]|prevent(?:ing)?|avoid(?:ing|ed)?|if|like|worried|worry|"
              r"scared|before|lucky|luckily|thankfully|fortunately|cause|causing|chance|danger|dangerous|hazard)\b|"
              r"n't\b|\bcannot\b")
NHTSA_EVENT = {
    "fire": r"c[ao]ugh?t (?:on )?fire|catch(?:es|ing)? (?:on )?fire|went (?:up )?in flames|(?:was|were|is|went) on fire|"
            r"burst into flames?|flames?|engulfed|ablaze|fire (?:started|broke out|erupted|spread|developed|appeared|"
            r"began|ignited|damage)|(?:vehicle|car|truck|engine|electrical|engine compartment|interior|small|minor|"
            r"dash(?:board)?|wiring|battery|seat|debris|spontaneous|brake|under-?hood) fires?|fire department|fire dept|"
            r"firefighters?|firemen|fire truck|extinguish(?:ed|er|ers)?|burn(?:ed|t) (?:up|down|completely)|"
            r"(?:spontaneously )?combusted|(?:had|ignited|caused|causing|started) a fire|(?:smoke|sparks),? (?:and |then )?fire",
    "injury": r"injur(?:y|ies|ed|ing)|hurt|bruis(?:e|es|ed|ing)|burns|burned (?:my|his|her|their)|"
              r"broke (?:my|his|her|their) \w+|broken (?:arm|leg|wrist|hand|ankle|nose|rib|ribs|neck|back|finger|foot|"
              r"bone|bones)|fractur(?:e|ed|es)|concussion|whiplash|lacerations?|stitches|sprain(?:ed|s)?|"
              r"hospital(?:ized)?|emergency room|ambulance|medical (?:attention|treatment|care)|swollen|abrasions?|"
              r"killed|died|fatal(?:ly|ity|ities)?",
    "crash": r"crash(?:ed|es|ing)?|collision|collided|rear[- ]ended|hit (?:a|the|another|my|an|me|us|him|her)|struck|"
             r"ran into|slammed into|accident|wreck(?:ed)?|totaled|totalled",
}
# Storm surveys: the card rates by the survey's estimated peak wind, so a text is kept only when every wind speed it
# gives (a number + mph after 'wind' / 'gust' in the same sentence) lies in its rating's band (CARD_SOURCES storm wind).
STORM_WIND_NUM = r"\b(\d{2,3})(?:\s*(?:-|to|and)\s*(\d{2,3}))?\s*(?:mph|miles per hour)\b"
STORM_WIND_CTX = r"\b(?:winds?|gusts?|wind speeds?)\b"
# MedQuAD: one question type per passage. A passage is kept when it carries no section heading of another type and
# its own type's words outnumber every other type's words at least two to one (blind read 4.C: a symptoms passage with
# a full 'Tests for Cataract' section).
MEDQUAD_WORDS = {
    "causes": r"\bcaus(?:e|es|ed)\b|\bmutations?\b|\bdue to\b|\bresults? from\b|\brisk factors?\b",
    "inheritance pattern": r"\binherit\w*|\bautosomal\b|\brecessive\b|\bdominant\b|\bX-linked\b|\bcarriers?\b|"
                           r"\bpassed (?:down|from)\b",
    "treatment options": r"\btreat\w*|\btherap\w*|\bmedications?\b|\bdrugs?\b|\bsurgery\b|\bmanage\w*",
    "signs and symptoms": r"\bsymptoms?\b|\bsigns?\b|\bfeatures?\b|\bcharacterized\b",
    "diagnosis and tests": r"\bdiagnos\w*|\btests?\b|\btesting\b|\bexam\w*|\bdetect\w*|\bscreen\w*|\bbiops\w*",
    "prevention steps": r"\bprevent\w*|\bavoid\w*|\bvaccin\w*|\breduce (?:the|your) (?:risk|chance)",
}
MEDQUAD_HEADINGS = {   # matched case-sensitive (a heading starts with a capital)
    "causes": r"\b(?:What causes|Causes of|Causes? and Risk|Risk Factors)\b",
    "inheritance pattern": r"\b(?:Is .{0,40} inherited|Inheritance Pattern)\b",
    "treatment options": r"\b(?:Treatments? (?:for|of|Options)|How is .{0,40} treated|Treating )",
    "signs and symptoms": r"\b(?:(?:Common )?Symptoms(?: of)?|Signs and Symptoms|What are the symptoms)\b",
    "diagnosis and tests": r"\b(?:Tests? for|Diagnosis|Diagnosing|How is .{0,40} diagnosed|Screening for)\b",
    "prevention steps": r"\b(?:Prevention|Preventing|How can .{0,40} be prevented)\b",
}
# Form 10-K items: 'Risk Factors' is defined as risks phrased as what could happen, so a Risk Factors passage must use
# that phrasing and a passage of any other item must not (blind read 4.C: a Business passage on competition that
# 'may have the effect of reducing' demand).
EDGAR_RISK = (r"\b(?:may|could|might|cannot assure|no assurance|there can be no)\b[^.]{0,80}\b(?:adverse(?:ly)?|harm|"
              r"hurt|reduc\w*|declin\w*|loss(?:es)?|negative(?:ly)?|impair\w*|decreas\w*|fail\w*|disrupt\w*|lower|risk|"
              r"material(?:ly)?)\b|\brisks?\b")
EDGAR_RISK_LABEL = "Item 1A - Risk Factors"
# DrugProt: the sentence names the marked pair's relation in its own words. A sentence is kept when it uses no word of
# another relation (blind read 4.C: 'acts as an antagonist, but later functions as an ER agonist'), and a regulator
# relation (agonist, antagonist, inhibitor, activator) must also use its own word.
DRUGPROT_WORDS = {
    "agonist": r"\bagonis\w*", "antagonist": r"\bantagoni\w*",
    "inhibitor": r"\binhibit\w*|\bblock\w*|\bsuppress\w*",
    "activator": r"\bactivat\w*|\bstimulat\w*|\binduc\w*|\benhanc\w*|\bup-?regulat\w*",
    "substrate": r"\bsubstrates?\b|\bmetaboli[sz]\w*|\btransport\w*|\bhydroly\w*|\buptake\b",
    "part of": r"\bresidues?\b|\bmoiet\w*",
}
DRUGPROT_NEED_OWN = ("agonist", "antagonist", "inhibitor", "activator")
# NCBI disease mentions: the category is read off the mention's form, and a text is kept only when its form gives its
# human category. modifier: a disease name followed by a word it describes (gene, patients, family ...) or an adjective
# form (C6-deficient, diabetic); a mention that joins parts with and / or / a slash is dropped (composite mentions are
# retired); disease class: a general head word or a plural; specific disease: a proper name, an abbreviation or a
# single-disease ending (-itis, -oma, -osis, syndrome, ataxia ...).
NCBI_MOD_NEXT = (r"^\s*-?\s*(?:genes?|proteins?|locus|loci|regions?|kinases?|mutations?|mutants?|patients?|families|family|"
                 r"kindreds?|individuals?|carriers?|alleles?|cells?|serum|sera|mice|mouse|phenotypes?|susceptibility|"
                 r"specific|associated|linked|transcripts?|mrna|products?|homologues?|homologs?|deletions?|"
                 r"chromosomes?|cases|subjects|children|women|men|males|females|pedigrees?|probands?|lines?|"
                 r"tissues?|samples?|cohorts?|populations?|haplotypes?|repeats?|expansions?|antigens?|fibroblasts?|"
                 r"tumou?rs?|candidate|critical|research|status|types?|polypeptide|enzyme|activity|domain|sequences?|"
                 r"cdna|dna)\b")
NCBI_MOD_SELF = r"-(?:deficient|affected|specific|associated|linked|related|prone|causing)$|(?:ic|al|ed)$"
NCBI_CLASS_HEAD = (r"\b(?:disorders?|diseases?|tumou?rs?|cancers?|neoplasms?|neoplasias?|conditions?|malignanc(?:y|ies)|"
                   r"dystrophies|syndromes|anomalies|defects?|deficiencies|carcinomas|sarcomas|lymphomas|leuk(?:a)?emias|"
                   r"abnormalit(?:y|ies)|illness(?:es)?|ataxias|myopathies|neuropathies|dysplasias)$|"
                   r"(?:ias|oses|emias|aemias|pathies|trophies)$")
NCBI_JOIN = r"\b(?:and|or)\b|/"
NCBI_SPECIFIC_NAME = r"^[A-Z0-9][A-Za-z0-9\-' ]*$"          # matched case-sensitive: a proper name or an abbreviation
NCBI_SPECIFIC_END = (r"(?:syndrome|ataxia|dystrophy|an(?:a)?emia|emia|aemia|itis|oma|osis|opathy|trophy|plasia|uria|ism|ia|"
                     r"goiter|goitre|palsy|fever|sclerosis)$")

# SaferProducts (held out): the tier follows the care the primary victim got. Grave texts name an emergency room, a
# hospital stay or a death; middling texts name a doctor, clinic or first aid and no emergency care; slight texts name
# no care at all.
# (compiled case-sensitive: the words carry their own (?i:...) group, the abbreviations ER / ED / ICU stay capitals)
SAFER_GRAVE = (r"(?i:\b(?:emergency (?:room|department|dept)|hospital(?:ized|ised)?|admitted|died|death|passed away|"
               r"killed|fatal(?:ly)?|ambulance|intensive care|trauma (?:center|unit))\b)|\bE\.R\.|\b(?:ER|ED|ICU)\b")
SAFER_CARE = (r"\b(?:doctor|doctors|physician|pediatrician|paediatrician|clinic|urgent care|first aid|nurse|"
              r"dermatologist|dentist|orthodontist|ophthalmologist|optometrist|chiropractor|podiatrist|medical "
              r"(?:attention|care|treatment)|stitches|x-?rays?|prescri\w+|antibiotic\w*)\b")


# ============================================================================================ 6. record packs
# One record = a list of 3-6 invented items (names from the split's name pool) with one decisive field; P is about one
# named item. pos / neg: field values that make P true / false. forms: P's wordings by inner lexeme tuple
# (declarative, interrogative, inner-negative interrogative). dterms: derived card terms that carry one negation of P
# (card_def cue). ar: an affirmative complement (no cue word) with its card definition. choice: choice-row questions
# whose options are item names (key 'true' = select true; a lexeme = negated selection with that cue).
def _P(split, doc, title, item, items, field, pos, neg, noise, subj, pos_term, forms, dterms, choice, ar=None,
       people=False):
    return dict(split=split, doc=doc, title=title, item=item, items=items, field=field, pos=pos, neg=neg, noise=noise,
                subj=subj, pos_term=pos_term, forms=forms, dterms=dterms, choice=choice, ar=ar, people=people)


PACKS = {
    "invoices": _P(
        "train", "ledger", "Accounts ledger", "invoice", "invoices", "status", ["cleared"], ["open"], "amount in USD",
        "invoice {N}", ("paid", "an invoice whose status reads 'cleared'"),
        {(): [("{S} has been paid", "Has {S} been paid", None)],
         ("not",): [("{S} has not been paid", None, "Has {S} not been paid")],
         ("n't",): [("{S} hasn't been paid", None, None)],
         ("never",): [("{S} was never paid", "Was {S} never paid", None)],
         ("un-",): [("{S} is unpaid", "Is {S} unpaid", None), ("{S} remains unpaid", "Does {S} remain unpaid", None)],
         ("no",): [("no payment has been made on {S}", None, None)],
         ("fail",): [("the client failed to pay {S}", "Did the client fail to pay {S}", None)],
         ("lack",): [("{S} lacks a recorded payment", "Does {S} lack a recorded payment", None)],
         ("not", "un-"): [("{S} is not unpaid", None, "Is {S} not unpaid")],
         ("n't", "un-"): [("{S} isn't unpaid", None, None)],
         ("not", "fail"): [("the client did not fail to pay {S}", None, None)],
         ("not", "lack"): [("{S} does not lack a recorded payment", None, None)]},
        {"not": ("open item", "an invoice that has not been paid"), "un-": ("open item", "an unpaid invoice"),
         "lack": ("open item", "an invoice that lacks a recorded payment")},
        {"true": "Which invoice has been paid?", "un-": "Which invoice is unpaid?",
         "not": "Which invoice has not been paid?", "lack": "Which invoice lacks a recorded payment?"},
        ar=("{S} is still outstanding", "Is {S} still outstanding", ("outstanding", "an invoice whose status reads 'open'"))),
    "parcels": _P(
        "train", "delivery log", "Delivery log", "parcel", "parcels", "signature", ["collected"], ["refused"],
        "weight in kg", "parcel {N}", ("signed for", "a parcel whose signature field reads 'collected'"),
        {(): [("the recipient signed for {S}", "Did the recipient sign for {S}", None)],
         ("not",): [("the recipient did not sign for {S}", None, "Did the recipient not sign for {S}")],
         ("n't",): [("the recipient didn't sign for {S}", None, None)],
         ("refuse",): [("the recipient refused to sign for {S}", "Did the recipient refuse to sign for {S}", None)],
         ("decline",): [("the recipient declined to sign for {S}", "Did the recipient decline to sign for {S}", None)],
         ("un-",): [("{S} is unsigned", "Is {S} unsigned", None)],
         ("without",): [("{S} was left without a signature", "Was {S} left without a signature", None)],
         ("no",): [("{S} has no signature", None, None)],
         ("not", "un-"): [("{S} is not unsigned", None, None)],
         ("not", "refuse"): [("the recipient did not refuse to sign for {S}", None, None)],
         ("never", "refuse"): [("the recipient never refused to sign for {S}", None, None)],
         ("not", "decline"): [("the recipient did not decline to sign for {S}", None, None)]},
        {"not": ("unsigned item", "a parcel the recipient did not sign for"),
         "refuse": ("unsigned item", "a parcel the recipient refused to sign for"),
         "without": ("unsigned item", "a parcel left without a signature")},
        {"true": "Which parcel did the recipient sign for?", "un-": "Which parcel is unsigned?",
         "refuse": "Which parcel did the recipient refuse to sign for?",
         "not": "Which parcel did the recipient not sign for?"},
        ar=('{S} counts as returned', 'Does {S} count as returned', ('returned', "a parcel whose signature field reads 'refused'"))),
    "menu": _P(
        "train", "menu card", "Menu card", "dish", "dishes", "allergen tags", ["gluten", "gluten, egg", "gluten, dairy"],
        ["egg", "dairy", "sesame", "soy"], "price in USD", "the dish {N}",
        ("gluten dish", "a dish whose allergen tags include gluten"),
        {(): [("{S} contains gluten", "Does {S} contain gluten", None)],
         ("not",): [("{S} does not contain gluten", None, "Does {S} not contain gluten")],
         ("n't",): [("{S} doesn't contain gluten", None, None)],
         ("-free",): [("{S} is gluten-free", "Is {S} gluten-free", None)],
         ("no",): [("{S} contains no gluten", "Does {S} contain no gluten", None)],
         ("without",): [("{S} is made without gluten", "Is {S} made without gluten", None)],
         ("lack",): [("{S} lacks gluten", "Does {S} lack gluten", None)],
         ("omit",): [("the recipe for {S} omits gluten", "Does the recipe for {S} omit gluten", None)],
         ("exclude",): [("the recipe for {S} excludes gluten", "Does the recipe for {S} exclude gluten", None)],
         ("leave out",): [("the recipe for {S} leaves out gluten", "Does the recipe for {S} leave out gluten", None)],
         ("avoid",): [("the recipe for {S} avoids gluten", "Does the recipe for {S} avoid gluten", None)],
         ("not", "avoid"): [("the recipe for {S} does not avoid gluten", None, None)],
         ("not", "leave out"): [("the recipe for {S} does not leave out gluten", None, None)],
         ("not", "-free"): [("{S} is not gluten-free", None, "Is {S} not gluten-free")],
         ("n't", "-free"): [("{S} isn't gluten-free", None, None)],
         ("not", "without"): [("{S} is not made without gluten", None, None)],
         ("not", "omit"): [("the recipe for {S} does not omit gluten", None, None)],
         ("not", "lack"): [("{S} does not lack gluten", None, None)]},
        {"no": ("safe dish", "a dish with no gluten among its allergen tags"),
         "-free": ("safe dish", "a gluten-free dish"), "lack": ("safe dish", "a dish whose tags lack gluten")},
        {"true": "Which dish contains gluten?", "-free": "Which dish is gluten-free?",
         "not": "Which dish does not contain gluten?", "omit": "Which dish has a recipe that omits gluten?"},
        ar=('{S} counts as coeliac-safe', 'Does {S} count as coeliac-safe', ('coeliac-safe', "a dish whose allergen tags read 'egg', 'dairy', 'sesame' or 'soy'"))),
    "applications": _P(
        "train", "intake sheet", "Intake sheet", "application", "applications", "required fields", ["all filled"],
        ["one blank", "two blank"], "pages", "application {N}", ("complete", "an application whose required fields "
                                                                 "read 'all filled'"),
        {(): [("{S} is complete", "Is {S} complete", None)],
         ("not",): [("{S} is not complete", None, "Is {S} not complete")],
         ("n't",): [("{S} isn't complete", None, None)],
         ("in-",): [("{S} is incomplete", "Is {S} incomplete", None)],
         ("lack",): [("{S} lacks a required field", "Does {S} lack a required field", None)],
         ("miss",): [("{S} is missing a required field", "Is {S} missing a required field", None)],
         ("fail",): [("{S} fails to fill every required field", "Does {S} fail to fill every required field", None)],
         ("not", "in-"): [("{S} is not incomplete", None, "Is {S} not incomplete")],
         ("n't", "in-"): [("{S} isn't incomplete", None, None)],
         ("not", "lack"): [("{S} does not lack a required field", None, None)],
         ("not", "miss"): [("{S} is not missing a required field", None, None)]},
        {"not": ("held file", "an application that is not complete"), "in-": ("held file", "an incomplete application"),
         "miss": ("held file", "an application missing a required field")},
        {"true": "Which application is complete?", "in-": "Which application is incomplete?",
         "miss": "Which application is missing a required field?", "not": "Which application is not complete?"},
        ar=("{S} is on hold for blanks", "Is {S} on hold for blanks",
            ("on hold for blanks", "an application whose required fields read 'one blank' or 'two blank'"))),
    "tickets": _P(
        "train", "ticket list", "Ticket list", "ticket", "tickets", "status", ["valid"], ["expired"], "seat row",
        "ticket {N}", ("valid", "a ticket whose status reads 'valid'"),
        {(): [("{S} is valid", "Is {S} valid", None), ("{S} can be used", "Can {S} be used", None)],
         ("not",): [("{S} is not valid", None, "Is {S} not valid")],
         ("in-",): [("{S} is invalid", "Is {S} invalid", None)],
         ("cannot",): [("{S} cannot be used", None, None)],
         ("not", "in-"): [("{S} is not invalid", None, None)],
         ("n't", "in-"): [("{S} isn't invalid", None, None)],
},
        {"not": ("dead ticket", "a ticket that is not valid"), "in-": ("dead ticket", "an invalid ticket")},
        {"true": "Which ticket is valid?", "in-": "Which ticket is invalid?", "not": "Which ticket is not valid?"},
        ar=("{S} has expired", "Has {S} expired", ("expired", "a ticket whose status reads 'expired'"))),
    "guests": _P(
        "train", "guest list", "Guest list", "guest", "guests", "RSVP", ["accepted"], ["declined"], "table",
        "{N}", ("attending", "a guest whose RSVP reads 'accepted'"),
        {(): [("{S} accepted the invitation", "Did {S} accept the invitation", None)],
         ("not",): [("{S} did not accept the invitation", None, "Did {S} not accept the invitation")],
         ("n't",): [("{S} didn't accept the invitation", None, None)],
         ("never",): [("{S} never accepted the invitation", None, None)],
         ("decline",): [("{S} declined the invitation", "Did {S} decline the invitation", None)],
         ("refuse",): [("{S} refused the invitation", "Did {S} refuse the invitation", None)],
         ("not", "decline"): [("{S} did not decline the invitation", None, None)],
         ("n't", "decline"): [("{S} didn't decline the invitation", None, None)],
         ("not", "refuse"): [("{S} did not refuse the invitation", None, None)]},
        {"not": ("list C guest", "a guest who did not accept the invitation"),
         "decline": ("list C guest", "a guest who declined the invitation")},
        {"true": "Which guest accepted the invitation?", "decline": "Which guest declined the invitation?",
         "not": "Which guest did not accept the invitation?"}, people=True,
        ar=("{S} sent regrets", "Did {S} send regrets", ("sent regrets", "a guest whose RSVP reads 'declined'"))),
    "inspections": _P(
        "train", "inspection log", "Inspection log", "unit", "units", "result", ["pass"], ["fail"], "floor",
        "unit {N}", ("passed", "a unit whose result reads 'pass'"),
        {(): [("{S} passed the inspection", "Did {S} pass the inspection", None)],
         ("not",): [("{S} did not pass the inspection", None, "Did {S} not pass the inspection")],
         ("n't",): [("{S} didn't pass the inspection", None, None)],
         ("never",): [("{S} never passed the inspection", None, None)],
         ("fail",): [("{S} failed the inspection", "Did {S} fail the inspection", None)],
         ("not", "fail"): [("{S} did not fail the inspection", None, None)],
         ("n't", "fail"): [("{S} didn't fail the inspection", None, None)],
         ("never", "fail"): [("{S} never failed the inspection", None, None)]},
        {"not": ("repair job", "a unit that did not pass the inspection"),
         "fail": ("repair job", "a unit that failed the inspection")},
        {"true": "Which unit passed the inspection?", "fail": "Which unit failed the inspection?",
         "not": "Which unit did not pass the inspection?"},
        ar=("{S} was sent for repair", "Was {S} sent for repair", ("sent for repair", "a unit whose result reads 'fail'"))),
    "lines": _P(
        "train", "service sheet", "Service sheet", "line", "lines", "state", ["connected"], ["disconnected"],
        "monthly fee", "line {N}", ("live", "a line whose state reads 'connected'"),
        {(): [("{S} is connected", "Is {S} connected", None), ("{S} has a live connection", "Does {S} have a live connection", None)],
         ("not",): [("{S} is not connected", None, "Is {S} not connected")],
         ("n't",): [("{S} isn't connected", None, None)],
         ("dis-",): [("{S} is disconnected", "Is {S} disconnected", None)],
         ("no",): [("{S} has no live connection", None, None)],
         ("without",): [("{S} is without a live connection", "Is {S} without a live connection", None)],
         ("lack",): [("{S} lacks a live connection", "Does {S} lack a live connection", None)],
         ("not", "dis-"): [("{S} is not disconnected", None, "Is {S} not disconnected")],
         ("n't", "dis-"): [("{S} isn't disconnected", None, None)],
         ("not", "lack"): [("{S} does not lack a live connection", None, None)],
         ("not", "without"): [("{S} is not without a live connection", None, None)]},
        {"not": ("silent line", "a line that is not connected"), "dis-": ("silent line", "a disconnected line"),
         "lack": ("silent line", "a line that lacks a live connection")},
        {"true": "Which line is connected?", "dis-": "Which line is disconnected?", "not": "Which line is not connected?",
         "lack": "Which line lacks a live connection?"},
        ar=('{S} is a dead line', 'Is {S} a dead line', ('dead line', "a line whose state reads 'disconnected'"))),
    "devices": _P(
        "train", "equipment list", "Equipment list", "device", "devices", "power", ["mains cable"], ["battery"],
        "weight in grams", "device {N}", ("mains device", "a device whose power field reads 'mains cable'"),
        {(): [("{S} needs a power cable", "Does {S} need a power cable", None)],
         ("not",): [("{S} does not need a power cable", None, "Does {S} not need a power cable")],
         ("n't",): [("{S} doesn't need a power cable", None, None)],
         ("-less",): [("{S} is cordless", "Is {S} cordless", None)],
         ("no",): [("{S} needs no power cable", "Does {S} need no power cable", None)],
         ("without",): [("{S} runs without a power cable", "Does {S} run without a power cable", None)],
         ("not", "-less"): [("{S} is not cordless", None, "Is {S} not cordless")],
         ("n't", "-less"): [("{S} isn't cordless", None, None)],
         ("not", "without"): [("{S} does not run without a power cable", None, None)]},
        {"no": ("portable kit", "a device that needs no power cable"), "-less": ("portable kit", "a cordless device")},
        {"true": "Which device needs a power cable?", "-less": "Which device is cordless?",
         "not": "Which device does not need a power cable?"},
        ar=("{S} runs on a battery", "Does {S} run on a battery", ("battery-run", "a device whose power field reads 'battery'"))),
    "parking": _P(
        "train", "patrol sheet", "Patrol sheet", "car", "cars", "zone", ["permit bay"], ["red zone", "loading bay"],
        "minutes parked", "car {N}", ("parked legally", "a car whose zone reads 'permit bay'"),
        {(): [("{S} is parked legally", "Is {S} parked legally", None)],
         ("not",): [("{S} is not parked legally", None, "Is {S} not parked legally")],
         ("il-",): [("{S} is parked illegally", "Is {S} parked illegally", None)],
         ("not", "il-"): [("{S} is not parked illegally", None, None)],
         ("n't", "il-"): [("{S} isn't parked illegally", None, None)],
         ("n't",): [("{S} isn't parked legally", None, None)]},
        {"not": ("ticket case", "a car that is not parked legally"), "il-": ("ticket case", "an illegally parked car")},
        {"true": "Which car is parked legally?", "il-": "Which car is parked illegally?",
         "not": "Which car is not parked legally?"},
        ar=('{S} sits in a restricted spot', 'Does {S} sit in a restricted spot', ('restricted spot', "a car whose zone reads 'red zone' or 'loading bay'"))),
    "requests": _P(
        "train", "record", "Board minutes", "request", "requests", "decision", ["approved"], ["rejected"],
        "budget in USD", "request {N}", ("approved", "a request whose decision reads 'approved'"),
        {(): [("the board approved {S}", "Did the board approve {S}", None)],
         ("not",): [("the board did not approve {S}", None, "Did the board not approve {S}")],
         ("never",): [("the board never approved {S}", None, None)],
         ("reject",): [("the board rejected {S}", "Did the board reject {S}", None)],
         ("deny",): [("the board denied {S}", "Did the board deny {S}", None)],
         ("decline",): [("the board declined {S}", "Did the board decline {S}", None)],
         ("withhold",): [("the board withheld approval from {S}", "Did the board withhold approval from {S}", None)],
         ("refuse",): [("the board refused {S}", "Did the board refuse {S}", None)],
         ("not", "reject"): [("the board did not reject {S}", None, None)],
         ("not", "deny"): [("the board did not deny {S}", None, None)],
         ("not", "withhold"): [("the board did not withhold approval from {S}", None, None)],
         ("never", "reject"): [("the board never rejected {S}", None, None)]},
        {"not": ("dead request", "a request the board did not approve"),
         "reject": ("dead request", "a request the board rejected"),
         "withhold": ("dead request", "a request the board withheld approval from")},
        {"true": "Which request did the board approve?", "reject": "Which request did the board reject?",
         "deny": "Which request did the board deny?", "not": "Which request did the board not approve?"},
        ar=('{S} is in the red file', 'Is {S} in the red file', ('red file', "the file that holds every request whose decision reads 'rejected'"))),
    "bundles": _P(
        "train", "stock sheet", "Stock sheet", "bundle", "bundles", "box contents", ["phone, charger, cable"],
        ["phone, cable", "phone, case"], "units in stock", "bundle {N}", ("full bundle", "a bundle whose box "
                                                                         "contents list a charger"),
        {(): [("{S} includes a charger", "Does {S} include a charger", None)],
         ("not",): [("{S} does not include a charger", None, "Does {S} not include a charger")],
         ("n't",): [("{S} doesn't include a charger", None, None)],
         ("exclude",): [("{S} excludes the charger", "Does {S} exclude the charger", None)],
         ("omit",): [("{S} omits the charger", "Does {S} omit the charger", None)],
         ("leave out",): [("{S} has its charger left out", "Does {S} have its charger left out", None)],
         ("lack",): [("{S} lacks a charger", "Does {S} lack a charger", None)],
         ("without",): [("{S} ships without a charger", "Does {S} ship without a charger", None)],
         ("no",): [("{S} comes with no charger", None, None)],
         ("not", "exclude"): [("{S} does not exclude the charger", None, None)],
         ("not", "omit"): [("{S} does not omit the charger", None, None)],
         ("not", "without"): [("{S} does not ship without a charger", None, None)],
         ("n't", "lack"): [("{S} doesn't lack a charger", None, None)]},
        {"lack": ("bare bundle", "a bundle that lacks a charger"), "omit": ("bare bundle", "a bundle that omits the charger"),
         "without": ("bare bundle", "a bundle that ships without a charger")},
        {"true": "Which bundle includes a charger?", "omit": "Which bundle omits the charger?",
         "exclude": "Which bundle excludes the charger?", "without": "Which bundle ships without a charger?"},
        ar=('{S} is a cut-down box', 'Is {S} a cut-down box', ('cut-down box', "a bundle whose box contents read 'phone, cable' or 'phone, case'"))),
    "rooms": _P(
        "train", "housekeeping sheet", "Housekeeping sheet", "room", "rooms", "cleaning", ["done"], ["skipped"],
        "beds", "room {N}", ("cleaned", "a room whose cleaning field reads 'done'"),
        {(): [("the cleaner cleaned {S}", "Did the cleaner clean {S}", None)],
         ("not",): [("the cleaner did not clean {S}", None, "Did the cleaner not clean {S}")],
         ("n't",): [("the cleaner didn't clean {S}", None, None)],
         ("never",): [("the cleaner never cleaned {S}", None, None)],
         ("skip",): [("the cleaner skipped {S}", "Did the cleaner skip {S}", None)],
         ("miss",): [("the cleaner missed {S}", "Did the cleaner miss {S}", None)],
         ("fail",): [("the cleaner failed to clean {S}", "Did the cleaner fail to clean {S}", None)],
         ("not", "skip"): [("the cleaner did not skip {S}", None, None)],
         ("not", "miss"): [("the cleaner did not miss {S}", None, None)],
         ("never", "skip"): [("the cleaner never skipped {S}", None, None)],
         ("not", "fail"): [("the cleaner did not fail to clean {S}", None, None)]},
        {"not": ("open room", "a room the cleaner did not clean"), "skip": ("open room", "a room the cleaner skipped"),
         "miss": ("open room", "a room the cleaner missed")},
        {"true": "Which room did the cleaner clean?", "skip": "Which room did the cleaner skip?",
         "miss": "Which room did the cleaner miss?", "not": "Which room did the cleaner not clean?"},
        ar=('{S} is on the redo list', 'Is {S} on the redo list', ('redo list', "the list of every room whose cleaning field reads 'skipped'"))),
    "staff": _P(
        "train", "briefing sheet", "Briefing sheet", "staff member", "staff members", "attendance", ["present"],
        ["absent"], "shift hours", "{N}", ("present", "a staff member whose attendance reads 'present'"),
        {(): [("{S} was present at the briefing", "Was {S} present at the briefing", None)],
         ("not",): [("{S} was not present at the briefing", None, "Was {S} not present at the briefing")],
         ("n't",): [("{S} wasn't present at the briefing", None, None)],
         ("absent",): [("{S} was absent from the briefing", "Was {S} absent from the briefing", None)],
         ("miss",): [("{S} missed the briefing", "Did {S} miss the briefing", None)],
         ("skip",): [("{S} skipped the briefing", "Did {S} skip the briefing", None)],
         ("never",): [("{S} never attended the briefing", None, None)],
         ("not", "absent"): [("{S} was not absent from the briefing", None, "Was {S} not absent from the briefing")],
         ("n't", "absent"): [("{S} wasn't absent from the briefing", None, None)],
         ("not", "miss"): [("{S} did not miss the briefing", None, None)],
         ("not", "skip"): [("{S} did not skip the briefing", None, None)]},
        {"not": ("follow-up case", "a staff member who was not present at the briefing"),
         "absent": ("follow-up case", "a staff member absent from the briefing")},
        {"true": "Which staff member was present at the briefing?", "absent": "Which staff member was absent from the briefing?",
         "miss": "Which staff member missed the briefing?", "not": "Which staff member was not present at the briefing?"},
        people=True,
        ar=('{S} is marked away', 'Is {S} marked away', ('away', "a staff member whose attendance reads 'absent'"))),
    "routes": _P(
        "train", "route plan", "Route plan", "route", "routes", "road type", ["toll road"], ["open road", "side road"],
        "length in km", "route {N}", ("toll route", "a route whose road type reads 'toll road'"),
        {(): [("{S} uses a toll road", "Does {S} use a toll road", None)],
         ("not",): [("{S} does not use a toll road", None, "Does {S} not use a toll road")],
         ("n't",): [("{S} doesn't use a toll road", None, None)],
         ("avoid",): [("{S} avoids toll roads", "Does {S} avoid toll roads", None)],
         ("-free",): [("{S} is toll-free", "Is {S} toll-free", None)],
         ("no",): [("{S} has no toll roads", None, None)],
         ("without",): [("{S} runs without toll roads", "Does {S} run without toll roads", None)],
         ("not", "avoid"): [("{S} does not avoid toll roads", None, None)],
         ("not", "-free"): [("{S} is not toll-free", None, "Is {S} not toll-free")],
         ("n't", "-free"): [("{S} isn't toll-free", None, None)]},
        {"avoid": ("free route", "a route that avoids toll roads"), "-free": ("free route", "a toll-free route"),
         "no": ("free route", "a route with no toll roads")},
        {"true": "Which route uses a toll road?", "-free": "Which route is toll-free?",
         "avoid": "Which route avoids toll roads?", "not": "Which route does not use a toll road?"},
        ar=('{S} is a by-road route', 'Is {S} a by-road route', ('by-road route', "a route whose road type reads 'open road' or 'side road'"))),
    "accounts": _P(
        "train", "account review", "Account review", "account", "accounts", "identity check", ["verified"],
        ["pending"], "logins this month", "account {N}", ("verified", "an account whose identity check reads 'verified'"),
        {(): [("{S} is verified", "Is {S} verified", None)],
         ("not",): [("{S} is not verified", None, "Is {S} not verified")],
         ("n't",): [("{S} isn't verified", None, None)],
         ("un-",): [("{S} is unverified", "Is {S} unverified", None)],
         ("lack",): [("{S} lacks a completed identity check", "Does {S} lack a completed identity check", None)],
         ("not", "un-"): [("{S} is not unverified", None, "Is {S} not unverified")],
         ("n't", "un-"): [("{S} isn't unverified", None, None)],
         ("not", "lack"): [("{S} does not lack a completed identity check", None, None)]},
        {"not": ("watch item", "an account that is not verified"), "un-": ("watch item", "an unverified account")},
        {"true": "Which account is verified?", "un-": "Which account is unverified?", "not": "Which account is not verified?"},
        ar=("{S} is still pending review", "Is {S} still pending review",
            ("pending review", "an account whose identity check reads 'pending'"))),
    "orders": _P(
        "train", "order sheet", "Order sheet", "order", "orders", "refund terms", ["full refund"], ["final sale"],
        "items", "order {N}", ("refundable", "an order whose refund terms read 'full refund'"),
        {(): [("{S} is refundable", "Is {S} refundable", None), ("{S} can be refunded", "Can {S} be refunded", None)],
         ("not",): [("{S} is not refundable", None, "Is {S} not refundable")],
         ("non-",): [("{S} is non-refundable", "Is {S} non-refundable", None)],
         ("cannot",): [("{S} cannot be refunded", None, None)],
         ("not", "non-"): [("{S} is not non-refundable", None, "Is {S} not non-refundable")],
         ("n't", "non-"): [("{S} isn't non-refundable", None, None)]},
        {"not": ("locked sale", "an order that is not refundable"), "non-": ("locked sale", "a non-refundable order"),
         "cannot": ("locked sale", "an order that cannot be refunded")},
        {"true": "Which order is refundable?", "non-": "Which order is non-refundable?", "not": "Which order is not refundable?"},
        ar=("{S} is a final sale", "Is {S} a final sale", ("final sale", "an order whose refund terms read 'final sale'"))),
    "roads": _P(
        "train", "road report", "Road report", "road", "roads", "status", ["clear"], ["blocked"], "lanes",
        "road {N}", ("passable", "a road whose status reads 'clear'"),
        {(): [("{S} is passable", "Is {S} passable", None)],
         ("not",): [("{S} is not passable", None, "Is {S} not passable")],
         ("im-",): [("{S} is impassable", "Is {S} impassable", None)],
         ("cannot",): [("cars cannot get through on {S}", None, None)],
         ("not", "im-"): [("{S} is not impassable", None, "Is {S} not impassable")],
         ("n't", "im-"): [("{S} isn't impassable", None, None)],
},
        {"not": ("closed road", "a road that is not passable"), "im-": ("closed road", "an impassable road")},
        {"true": "Which road is passable?", "im-": "Which road is impassable?", "not": "Which road is not passable?"},
        ar=("{S} is blocked", "Is {S} blocked", ("blocked", "a road whose status reads 'blocked'"))),
    "lockers": _P(
        "train", "locker check", "Locker check", "locker", "lockers", "contents", ["1 bag", "2 boxes", "1 coat"],
        ["empty"], "floor", "locker {N}", ("in use", "a locker whose contents field lists at least one thing"),
        {(): [("{S} holds something", "Does {S} hold something", None)],
         ("nothing",): [("{S} holds nothing", "Does {S} hold nothing", None)],
         ("no",): [("{S} holds no items", None, None)],
         ("not",): [("{S} does not hold anything", None, "Does {S} not hold anything")],
         ("n't",): [("{S} doesn't hold anything", None, None)],
         ("without",): [("{S} is without contents", "Is {S} without contents", None)],
         ("not", "without"): [("{S} is not without contents", None, None)]},
        {"nothing": ("free locker", "a locker that holds nothing"), "no": ("free locker", "a locker with no items in it")},
        {"true": "Which locker holds something?", "nothing": "Which locker holds nothing?",
         "not": "Which locker does not hold anything?"},
        ar=("{S} is empty", "Is {S} empty", ("empty", "a locker whose contents field reads 'empty'"))),
    "sessions": _P(
        "train", "attendance sheet", "Attendance sheet", "session", "sessions", "attendees", ["3", "5", "8", "12"],
        ["0"], "room size", "session {N}", ("attended", "a session whose attendee count is above zero"),
        {(): [("someone attended {S}", "Did someone attend {S}", None)],
         ("nobody",): [("nobody attended {S}", "Did nobody attend {S}", None)],
         ("no one",): [("no one attended {S}", "Did no one attend {S}", None)],
         ("none",): [("none of the invitees attended {S}", "Did none of the invitees attend {S}", None)],
         ("not",): [("{S} was not attended", None, "Was {S} not attended")],
         ("un-",): [("{S} went unattended", "Did {S} go unattended", None)],
         ("not", "un-"): [("{S} did not go unattended", None, None)]},
        {"nobody": ("empty session", "a session that nobody attended"),
         "no one": ("empty session", "a session that no one attended")},
        {"true": "Which session did someone attend?", "nobody": "Which session did nobody attend?",
         "un-": "Which session went unattended?"},
        ar=("{S} stood empty", "Did {S} stand empty", ("stood empty", "a session whose attendee count is 0"))),
    # ---------------------------------------------------------------- HELD-OUT packs (dev_holdout only)
    "patients": _P(
        "holdout", "ward chart", "Ward chart", "patient", "patients", "symptoms", ["cough", "fever", "rash"],
        ["clear"], "age", "patient {N}", ("symptomatic", "a patient whose symptoms field names a symptom"),
        {(): [("{S} has symptoms", "Does {S} have symptoms", None)],
         ("a-",): [("{S} is asymptomatic", "Is {S} asymptomatic", None)],
         ("at no point",): [("at no point did {S} show symptoms", None, None)],
         ("not",): [("{S} does not have symptoms", None, "Does {S} not have symptoms")],
         ("no",): [("{S} has no symptoms", None, None)],
         ("not", "a-"): [("{S} is not asymptomatic", None, None)]},
        {"a-": ("quiet case", "an asymptomatic patient"), "no": ("quiet case", "a patient with no symptoms")},
        {"true": "Which patient has symptoms?", "a-": "Which patient is asymptomatic?",
         "not": "Which patient does not have symptoms?"},
        ar=('{S} is in the clear group', 'Is {S} in the clear group', ('clear group', "the patients whose symptoms field reads 'clear'"))),
    "licences": _P(
        "holdout", "licence register", "Licence register", "licence", "licences", "status", ["active"], ["lapsed"],
        "renewals", "licence {N}", ("active", "a licence whose status reads 'active'"),
        {(): [("{S} is valid", "Is {S} valid", None)],
         ("no longer",): [("{S} is no longer valid", "Is {S} no longer valid", None)],
         ("in-",): [("{S} is invalid", "Is {S} invalid", None)],
         ("not",): [("{S} is not valid", None, None)],
         ("not", "in-"): [("{S} is not invalid", None, None)]},
        {"no longer": ("lapsed file", "a licence that is no longer valid")},
        {"true": "Which licence is valid?", "no longer": "Which licence is no longer valid?"},
        ar=('{S} has lapsed', 'Has {S} lapsed', ('lapsed', "a licence whose status reads 'lapsed'"))),
    "grants": _P(
        "holdout", "council record", "Council record", "grant", "grants", "council vote", ["approved"], ["vetoed"],
        "amount in USD", "grant {N}", ("funded", "a grant whose council vote reads 'approved'"),
        {(): [("the council approved {S}", "Did the council approve {S}", None)],
         ("veto",): [("the council vetoed {S}", "Did the council veto {S}", None)],
         ("turn down",): [("the council turned down {S}", "Did the council turn down {S}", None)],
         ("not",): [("the council did not approve {S}", None, None)],
         ("not", "veto"): [("the council did not veto {S}", None, None)]},
        {"veto": ("stalled grant", "a grant the council vetoed")},
        {"true": "Which grant did the council approve?", "veto": "Which grant did the council veto?"},
        ar=('{S} is shelved', 'Is {S} shelved', ('shelved', "a grant whose council vote reads 'vetoed'"))),
    "plans": _P(
        "holdout", "payment ledger", "Payment ledger", "payment plan", "payment plans", "schedule", ["on time"],
        ["late twice"], "instalments", "payment plan {N}", ("regular", "a payment plan whose schedule reads 'on time'"),
        {(): [("{S} is regular", "Is {S} regular", None)],
         ("ir-",): [("{S} is irregular", "Is {S} irregular", None)],
         ("not",): [("{S} is not regular", None, None)],
         ("not", "ir-"): [("{S} is not irregular", None, None)]},
        {"ir-": ("review plan", "an irregular payment plan")},
        {"true": "Which payment plan is regular?", "ir-": "Which payment plan is irregular?"},
        ar=('{S} is on the watch list', 'Is {S} on the watch list', ('watch list', "the payment plans whose schedule reads 'late twice'"))),
    "ballots": _P(
        "holdout", "ballot record", "Ballot record", "member", "members", "vote", ["cast"], ["abstained"], "seat",
        "{N}", ("voted", "a member whose vote reads 'cast'"),
        {(): [("{S} voted in the ballot", "Did {S} vote in the ballot", None)],
         ("abstain",): [("{S} abstained from the ballot", "Did {S} abstain from the ballot", None)],
         ("forgo",): [("{S} forwent the ballot", "Did {S} forgo the ballot", None)],
         ("not",): [("{S} did not vote in the ballot", None, None)],
         ("not", "abstain"): [("{S} did not abstain from the ballot", None, None)]},
        {"abstain": ("silent member", "a member who abstained from the ballot")},
        {"true": "Which member voted in the ballot?", "abstain": "Which member abstained from the ballot?"},
        people=True,
        ar=('{S} is in the blank column', 'Is {S} in the blank column', ('blank column', "the members whose vote reads 'abstained'"))),
}

# item 33 (must not / need not / cannot): a rule pack. The card states the rule; P = the item must be signed for
# (true exactly for 'fragile' parcels). Every 'need not' wording is paired with a 'must not' wording.
DEONTIC = dict(
    split="train", doc="dispatch sheet", title="Dispatch sheet", item="parcel", items="parcels", field="handling",
    pos=["fragile"], neg=["standard"], noise="weight in kg", subj="parcel {N}",
    rule=("rule", "a parcel marked 'fragile' must be signed for; other parcels need not be"),
    pos_term=("fragile", "a parcel whose handling field reads 'fragile'"), dterms={}, ar=None, people=False,
    forms={(): [("{S} must be signed for", "Must {S} be signed for", None)],
           ("need not",): [("{S} need not be signed for", None, None)],
           ("not",): [("{S} does not have to be signed for", None, None)],
           ("must not", "un-"): [("{S} must not be left unsigned", None, None)],
           ("cannot", "un-"): [("the courier cannot leave {S} unsigned", None, None)],
           ("forbid", "un-"): [("the rule forbids leaving {S} unsigned", None, None)],
           ("forbid", "skip"): [("the rule forbids skipping the signature for {S}", None, None)],
           ("must not", "without"): [("{S} must not go out without a signature", None, None)],
           ("must not", "skip"): [("the courier must not skip the signature for {S}", None, None)],
           ("not", "need not"): [("it is not so that {S} need not be signed for", None, None)]},
    choice={"true": "Which parcel must be signed for?", "need not": "Which parcel need not be signed for?"})
DEONTIC_H = dict(
    split="holdout", doc="cargo manifest", title="Cargo manifest", item="crate", items="crates", field="label",
    pos=["hazmat"], neg=["general"], noise="volume in litres", subj="crate {N}",
    rule=("rule", "a crate labelled 'hazmat' must be inspected before loading; other crates need not be"),
    pos_term=("hazmat", "a crate whose label field reads 'hazmat'"), dterms={}, ar=None, people=False,
    forms={(): [("{S} must be inspected before loading", "Must {S} be inspected before loading", None)],
           ("need not",): [("{S} need not be inspected before loading", None, None)],
           ("not",): [("{S} does not have to be inspected before loading", None, None)],
           ("must not", "un-"): [("{S} must not be loaded uninspected", None, None)],
           ("cannot", "un-"): [("the crew cannot load {S} uninspected", None, None)],
           ("at no point",): [("at no point does {S} have to be inspected", None, None)]},
    choice={"true": "Which crate must be inspected before loading?",
            "need not": "Which crate need not be inspected before loading?"})
# item 35 (non-factive scope edit): a ticket record with a triage field 'refund requested' = yes / no / blank.
# P = the triage note claims that the customer asks for a refund (field 'yes'). 'Makes no claim that P' and 'claims
# that not-P' come apart when the field is blank; the choice rows contrast all three.
TRIAGE = dict(
    split="train", doc="ticket", title="Support ticket", subj="the triage note",
    forms={(): [("the triage note claims that the customer is asking for a refund",
                 "Does the triage note claim that the customer is asking for a refund", None)],
           ("no",): [("the triage note makes no claim that the customer is asking for a refund", None, None)],
           ("not",): [("the triage note does not claim that the customer is asking for a refund", None,
                       "Does the triage note not claim that the customer is asking for a refund")],
           ("fail",): [("the triage note fails to claim that the customer is asking for a refund",
                        "Does the triage note fail to claim that the customer is asking for a refund", None)],
           ("not", "fail"): [("the triage note does not fail to claim that the customer is asking for a refund",
                              None, None)]},
    options=["the note claims: 'the customer is asking for a refund'",
             "the note claims: 'the customer is not asking for a refund'",
             "the note says nothing about a refund"])
TRIAGE_H_MESSAGES = [
    "The blender stopped after two uses and I don't have the box any more. Can someone look at this?",
    "I was charged twice for one parcel and I haven't heard back yet. Please check my account.",
    "The rug arrived the wrong size; it isn't what I picked on the site. What happens now?",
    "My tablet case never closes properly and I can't use the stand. I'd like help with it.",
]


# ============================================================================================ 7. distractors
# Provably non-scoping negations (rule 2.5): conditional or vacuous side clauses ('whether or not', 'even if',
# 'regardless of whether'), format instructions in their own sentence, and card lines that decide nothing. None of
# them presupposes a fact about the text. (lexeme, surface, text); {doc} = the document noun.
DIST_SIDE = [
    ("not", "not", "whether or not the {doc} is long"),
    ("not", "not", "whether or not the {doc} is easy to read"),
    ("no", "no", "even if the {doc} names no place"),
    ("never", "never", "even if the {doc} never gives a date"),
    ("nothing", "nothing", "even if nothing in the {doc} is in capital letters"),
    ("nobody", "nobody", "even if nobody signed the {doc}"),
    ("without", "without", "even if the {doc} comes without a title"),
    ("none", "none", "even if none of the sentences in the {doc} is long"),
    ("un-", "unsigned", "regardless of whether the {doc} is unsigned"),
    ("un-", "undated", "even if the {doc} is undated"),
    ("in-", "informal", "even if the {doc} is informal in tone"),
    ("dis-", "disorganised", "even if the {doc} is disorganised"),
    ("im-", "impersonal", "even if the {doc} sounds impersonal"),
    ("il-", "illogical", "even if parts of the {doc} read as illogical"),
    ("-less", "careless", "even if the {doc} looks careless in places"),
    ("-free", "jargon-free", "even if the {doc} is jargon-free"),
    ("non-", "non-standard", "regardless of whether the {doc} uses non-standard spelling"),
    ("lack", "lacks", "even if the {doc} lacks a heading"),
    ("fail", "fails", "even if the {doc} fails to name its writer"),
    ("omit", "omits", "even if the {doc} omits the writer's name"),
    ("miss", "missing", "even if the {doc} is missing a date"),
    # every syntactic lexeme and the document-content verbs (A1); one cue word per clause, no comma inside (the clause
    # is cut at its comma), nothing presupposed about the text
    ("n't", "doesn't", "even if the {doc} doesn't name its writer"),
    ("n't", "isn't", "even if the {doc} isn't signed at the end"),
    ("n't", "doesn't", "even if the {doc} doesn't give a date"),
    ("n't", "wasn't", "even if the {doc} wasn't proofread before it was sent"),
    ("n't", "hasn't", "even if the {doc} hasn't got a title"),
    ("cannot", "cannot", "even if the writer of the {doc} cannot be identified"),
    ("cannot", "cannot", "even if the {doc} cannot be dated"),
    ("cannot", "cannot", "even if the {doc} cannot be traced to a source"),
    ("not a single", "not a single", "even if not a single word in the {doc} is in bold"),
    ("no more than", "no more than", "even if the {doc} runs to no more than a few lines"),
    ("few", "few", "even if few words in the {doc} are capitalised"),
    ("neither", "neither", "even if the {doc} names neither a date nor a place"),
    ("no one", "no one", "even if no one is named as the writer of the {doc}"),
    ("not every", "not every", "even if not every sentence in the {doc} is complete"),     # logic-line cards only (X10)
    ("not all", "not all", "even if not all of the {doc} is easy to read"),                  # logic-line cards only (X10)
    ("skip", "skips", "even if the {doc} skips the usual heading"),
    ("avoid", "avoids", "even if the {doc} avoids technical terms"),
    ("decline", "declined", "even if the writer of the {doc} declined to give a name"),
    ("refuse", "refused", "even if the writer of the {doc} refused to give a name"),
    ("leave out", "leaves out", "even if the {doc} leaves out the date"),
    ("withhold", "withheld", "even if the writer of the {doc} withheld their name"),
    ("absent", "absent", "even if a title is absent from the {doc}"),
]
# side clauses with 'not all' / 'not every' need the card's logic line (EXCLUDE X10): multi-text ladders only
DIST_SIDE_LOGIC_ONLY = ("not every", "not all")
DIST_SEP = [
    ("fail", "fails", "A {doc} that fails to name its writer can still be judged.",
     "even when a {doc} fails to name its writer"),
    ("lack", "lacks", "A {doc} that lacks a heading can still be judged.", "even when a {doc} lacks a heading"),
    ("non-", "non-standard", "Non-standard spelling is fine.", "whatever its non-standard spelling"),
    ("in-", "informal", "An informal tone is fine.", "whatever its informal tone"),
    ("-free", "jargon-free", "Jargon-free wording is fine.", "with jargon-free wording being fine"),
    ("-less", "careless", "Careless typing is fine.", "with careless typing being fine"),
    ("not", "not", "Do not use outside knowledge.", "not using outside knowledge"),
    ("no", "no", "Use no outside knowledge.", "using no outside knowledge"),
    ("never", "never", "Never rely on facts from outside the {doc}.", "never relying on outside facts"),
    ("nothing", "nothing", "Nothing outside the {doc} and the card counts.", "with nothing outside the {doc} counting"),
    ("without", "without", "Answer without outside facts.", "without outside facts"),
    ("dis-", "disregard", "Disregard anything outside the {doc}.", "if you disregard anything outside the {doc}"),
    ("un-", "unrelated", "Set unrelated details aside.", "with unrelated details set aside"),
]
DIST_CARD = [
    ("non-", "non-standard", "spelling", "non-standard spelling in the {doc} is fine"),
    ("in-", "informal", "tone", "an informal tone in the {doc} is fine"),
    ("dis-", "disorganised", "layout", "a disorganised layout in the {doc} is fine"),
    ("-less", "careless", "typing", "careless typing in the {doc} is fine"),
    ("-free", "jargon-free", "wording", "jargon-free wording and heavy jargon are both fine"),
    ("im-", "impersonal", "voice", "an impersonal voice in the {doc} is fine"),
    ("lack", "lacks", "heading", "a {doc} that lacks a heading can still be judged"),
    ("fail", "fails", "writer", "a {doc} that fails to name its writer can still be judged"),
    ("omit", "omits", "date", "a {doc} that omits its date can still be judged"),
    ("no", "no", "scope", "no outside knowledge is needed for this question"),
    ("never", "never", "note", "the answer never depends on the writer's tone"),
    ("nothing", "nothing", "note", "nothing outside the {doc} and this card counts"),
    ("un-", "unrelated", "note", "unrelated details in the {doc} can be set aside"),
    ("without", "without", "note", "read each line of the {doc} without outside facts"),
    ("none", "none", "something else", "the {doc} fits none of the label lines above"),
    # A1: card lines that decide nothing, for the syntactic lexemes and content verbs; every key is a card key that
    # names a format matter (never 'definition' / 'reading', which the multi-text card already uses, and never
    # 'wording' next to a 'contrary' frame, whose card defines that word under that key)
    ("unless", "unless", "typing", "typing slips in the {doc} are fine unless they change a word's meaning"),
    ("unless", "unless", "spelling", "spelling in the {doc} is ignored unless it changes a word"),
    ("need not", "need not", "tone", "the {doc} need not sound formal"),
    ("need not", "need not", "voice", "the {doc} need not be written in the first person"),
    ("must not", "must not", "scope", "facts from outside the {doc} must not be used"),
    ("must not", "must not", "writer", "the writer's identity must not sway the answer"),
    ("n't", "doesn't", "heading", "a {doc} that doesn't have a heading can still be judged"),
    ("n't", "isn't", "date", "a {doc} that isn't dated can still be judged"),
    ("cannot", "cannot", "writer", "a {doc} whose writer cannot be identified can still be judged"),
    ("cannot", "cannot", "date", "a {doc} that cannot be dated can still be judged"),
    ("no one", "no one", "writer", "a {doc} that no one signed can still be judged"),
    ("not a single", "not a single", "layout", "a {doc} in which not a single line is indented is fine"),
    ("forbid", "forbids", "scope", "the card forbids the use of outside facts"),
    ("skip", "skips", "layout", "a {doc} that skips the usual heading can still be judged"),
    # 'not every' / 'not all' in a card line (X10 reads the question, options and yes / no lines, never card lines)
    ("not every", "not every", "layout", "not every {doc} follows the same layout"),
    ("not all", "not all", "spelling", "not all words in the {doc} need standard spelling"),
]
BIVALENCE_LINE = "the {doc} settles every claim asked about here: each one either holds or fails"
# held-out 'contrary' frames: the card states that the contrary of a claim is its plain denial (not a stronger opposite
# claim, not the antonym label), so the logical-contrary and antonym readings are ruled out (decide2 finding #6)
CONTRARY_KEY = "wording"
CONTRARY_DEF = ("here 'the contrary of a claim' means its plain denial: the contrary holds exactly when the claim "
                "itself fails")
# round 3 (yn2b/F7_OBJECTIONS.md, arbiter round 3 A4): 'the opposite / reverse of a claim' has the same two readings
# as 'contrary' (plain denial vs a stronger opposite claim: 'the opposite of none is all'; on ordinal label sets also
# the antonym label). Every row whose frame uses one of these words carries the line for that word.
FRAME_WORDS = ("contrary", "opposite", "reverse")


def frame_word_def(word):
    """The card's 'wording' line for a frame word (for 'contrary' it is CONTRARY_DEF byte for byte)."""
    assert word in FRAME_WORDS, word
    return CONTRARY_DEF.replace("contrary", word)
