"""F7 devx v2 (blind, round-2 rebuild): hand-written nested-negation dev rows (checklist section 2 rule 10, SPEC 6).

Written blind: the author never opened the F7 generator (golden_src/gen3/gen3_nested_negation.py), its lexicon
(nn_lexicon.py, f7_lexicon.json) or any F7 train / probe row text. Every instruction, card line and option below is
hand-written for this file. States are
  (a) real human-labelled texts, copied byte-exact: civil_comments / toxic_conv comments from data/train_v05.jsonl and
      data/train_v06.jsonl (plain base rows only, every copy of the comment carries the same human label; symbol-label
      copies are read through their own card), gd_saferproducts_severity and gd_wiki_help_routing reports and posts
      from data/v14_parts/raw/*.jsonl. Every chosen text has 0 word 8-grams in common with any golden_train state and
      with any F7 train / probe state (count-only scan, yn2b/f7_devx_pool_scan.py), or
  (b) records invented here (names from the devx name pool of golden_src/gen3/mv_core.py, reserved .example domains).

Design (round 2):
  * TWIN LADDERS. The 44 ladders come in 22 twin pairs. Both ladders of a pair ask the SAME yes/no questions (same
    instruction, same card) over two states whose core claim P has opposite truth values, so every yes/no question
    appears once with gold yes and once with gold no. Every yes/no stratum that depends only on the question (depth,
    cue count, rung, frame, template, cue class / position / lexeme / distance, card style, length, quoted label) is
    therefore exactly 50% yes, and so is every stratum that depends on the state, because twins share source, ladder
    kind, state format and state negation. Each ladder also has one choice row of its own.
  * LF CONTRACT (yn2b/F7_OBJECTIONS.md rulings): choice rows have CHOICE at the root with the negated-selection cue
    on the CHOICE node, exactly one CORE per option, sidecar gold = option index, depth = NOT nodes on the gold
    option's path + 1 for a negated selection. Look-alikes are cues on no node (class lookalike). AR rows are NOT
    nodes with "cue": null and no cue word. Negations inside the reported content of a non-factive verb are not cues:
    they are listed in the information field 'content_negations'. Rule words ('must not', 'unless', 'need not') are
    NOT nodes on the claim path. Item-21 rows carry 'antonym_gold'.
Gold is written by hand per twin (gold2 = gold of twin a + gold of twin b) AND computed from the logical form; the
build asserts they agree and that twins differ on every yes/no row. No model is used anywhere. CPU only, no network.

Run (from opendecide-data/lean):  ../.venv/bin/python yn2b/f7_devx_build.py
Outputs: data/v14_parts/f7_devx.jsonl, f7_devx_meta.jsonl, f7_devx_relations.jsonl,
         yn2b/f7_devx_blind_packet.jsonl (gold-free rows for the blind decide2 LF author and the 11.1 blind reader)
Audit:   ../.venv/bin/python yn2b/f7_devx_audit.py   (writes yn2b/f7_devx_audit.json)
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
OUT_ROWS = LEAN / "data/v14_parts/f7_devx.jsonl"
OUT_REL = LEAN / "data/v14_parts/f7_devx_relations.jsonl"
OUT_META = LEAN / "data/v14_parts/f7_devx_meta.jsonl"
OUT_PACKET = LEAN / "yn2b/f7_devx_blind_packet.jsonl"
VERSION = "f7x2"
# Round 3 (arbiter round 3, yn2b/F7_OBJECTIONS.md A3 / A4): the rows rewritten in round 3 get the id prefix r_f7x3_
# (ladder ids stay f7x2_L..), so decide2's round-2 parse table, which still holds the old wording under r_f7x2_ ids,
# cannot silently match a rewritten row. Their LFs must be written again by an agent who has not seen devx golds.
VERSION_R3 = "f7x3"

# ------------------------------------------------------------------------------------------------ cue vocabulary
SYN, AFF, LEX, TF, CS, AM, LK = ("syntactic", "affixal", "lexical", "truth_frame", "cross_sentence",
                                 "answer_mapping", "lookalike")
OF, IC, CD, YK, AMP, SSP, CO, ST = ("outer_frame", "inner_claim", "card_def", "yn_key", "answer_map",
                                    "separate_sentence", "choice_option", "state")
SC, SS, NS, FAR, OFD = "same_clause", "same_sentence", "next_sentence", "far", "other_field"


def cid(gid: str) -> str:
    return "c_" + hashlib.sha1(gid.encode()).hexdigest()[:12]


# ------------------------------------------------------------------------------------------------ sources
def _symbol_label(r):
    """A symbol-labelled copy ('Label-W' ...) read through the row's own card; None when the card does not say."""
    card = r.get("card") or ""
    tox = set(re.findall(r"^- (Label-[A-Z]): A comment is toxic\b", card, re.M))
    non = set(re.findall(r"^- (Label-[A-Z]): A comment is (?:not toxic|non-toxic)\b", card, re.M))
    if r["gold"] in tox:
        return "toxic"
    if r["gold"] in non:
        return "not toxic"
    if tox and len(r.get("options") or []) == 2 and r["gold"] not in tox:
        return "not toxic"
    return None


def load_sources():
    """Comments by group id: (source, human label, text). A comment is kept only if every plain choice copy and every
    symbol copy (read through its card) gives the same label, and only plain base rows (id r_ + 12 hex) are used."""
    copies = collections.defaultdict(list)
    for f in ["data/train_v05.jsonl", "data/train_v06.jsonl"]:
        for line in open(LEAN / f, encoding="utf-8"):
            r = json.loads(line)
            if r["source"] in ("civil_comments", "toxic_conv") and re.fullmatch(r"r_[0-9a-f]{12}", r["id"]):
                copies[r["group_id"]].append(r)
    tox = {}
    for gid, rs in copies.items():
        texts = {r["state"].split("\n", 1)[1] for r in rs}
        labels, bad = set(), False
        for r in rs:
            if r["qtype"] != "choice":
                continue
            if set(r.get("options") or []) == {"toxic", "not toxic"}:
                labels.add(r["gold"])
            else:
                lab = _symbol_label(r)
                bad |= lab is None
                labels.add(lab)
        if len(texts) == 1 and not bad and len(labels) == 1:
            tox[gid] = (rs[0]["source"], labels.pop(), texts.pop())
    raw = {}
    for key in ["saferproducts_severity", "wiki_help_routing"]:
        for line in open(LEAN / f"data/v14_parts/raw/{key}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            raw[r["rid"]] = ("gd_" + key, r["gold"], r["state"])
    return tox, raw


TOX, RAW = load_sources()
HEAD = {"civil_comments": "Comment:\n", "toxic_conv": "Online comment:\n"}


def tox_text(gid, want_gold):
    src, gold, text = TOX[gid]
    assert gold == want_gold, (gid, gold, want_gold)
    return src, text


def tox_state(gid, want_gold):
    src, text = tox_text(gid, want_gold)
    return src, HEAD[src] + text


def raw_text(rid, want_gold):
    src, gold, text = RAW[rid]
    assert gold == want_gold, (rid, gold, want_gold)
    return src, text


# ------------------------------------------------------------------------------------------------ LF builder
class B:
    """Collects the cues of one row while its logical form is written. ATOM values come from the ladder's atoms."""

    def __init__(self, atoms):
        self.atoms = atoms
        self.cues = []
        self.pending_dists = []   # instruction-level distractors of a choice row (wrapped onto the gold option)

    def _cue(self, spec, scoping, **kw):
        lex, cls, pos, dist, word = spec
        cue = dict(lexeme=lex, cls=cls, position=pos, scoping=scoping, distance=dist)
        if word:
            cue["word"] = word
        cue.update(kw)
        self.cues.append(cue)
        return len(self.cues) - 1

    def N(self, spec, child):          # a negation node; the precheck decides path / off-path from the tree
        return {"op": "NOT", "cue": self._cue(spec, True), "child": child}

    def NX(self, spec, child):         # an off-path negation (exception clause): scoping False, still a NOT node
        return {"op": "NOT", "cue": self._cue(spec, False), "child": child}

    def NN(self, child):               # AR: an implicit flip with no cue word
        return {"op": "NOT", "cue": None, "child": child}

    def D(self, spec, child):          # a distractor: evaluates to its child
        return {"op": "DIST", "cue": self._cue(spec, False), "child": child}

    def look(self, spec):              # a look-alike: a cue on no node
        assert spec[1] == LK
        self._cue(spec, False)

    def DI(self, spec):                # a choice row's instruction-level distractor
        self.pending_dists.append(self._cue(spec, False))

    def A(self, i):
        return {"op": "ATOM", "id": i, "val": bool(self.atoms[i])}

    def C(self, x):
        return {"op": "CORE", "child": x}

    def CA(self, i):                   # CORE(ATOM)
        return self.C(self.A(i))

    def AND(self, *xs):
        return {"op": "AND", "children": list(xs)}

    def OR(self, *xs):
        return {"op": "OR", "children": list(xs)}

    def ATLEAST(self, k, *xs):
        return {"op": "ATLEAST", "k": k, "children": list(xs)}

    def ATMOST(self, k, *xs):
        return {"op": "ATMOST", "k": k, "children": list(xs)}

    def EXACTLY(self, k, *xs):
        return {"op": "EXACTLY", "k": k, "children": list(xs)}

    def CH(self, opts, select, sel=None):
        n = {"op": "CHOICE", "options": list(opts), "select": select}
        if sel is not None:
            n["cue"] = self._cue(sel, True)
        assert (select == "false") == (sel is not None), "a negated selection carries its cue, a plain one none"
        return n


def c(lex, cls, pos, dist, word=None):
    """A cue: lexeme, class, position, distance to the core claim, and (optional) the surface word."""
    return (lex, cls, pos, dist, word)


def ev(n):
    op = n["op"]
    if op == "ATOM":
        return n["val"]
    if op == "NOT":
        return not ev(n["child"])
    if op in ("DIST", "CORE"):
        return ev(n["child"])
    vals = [ev(x) for x in n["children"]]
    if op == "AND":
        return all(vals)
    if op == "OR":
        return any(vals)
    s = sum(vals)
    return s >= n["k"] if op == "ATLEAST" else s <= n["k"] if op == "ATMOST" else s == n["k"]


def choice_hits(ch):
    want = ch["select"] == "true"
    return [i for i, o in enumerate(ch["options"]) if ev(o) == want]


def core_paths(n, nots=0, out=None):
    """[(core node, NOT count on its path)] for every CORE under n."""
    out = [] if out is None else out
    if n.get("op") == "CORE":
        out.append((n, nots))
        return out
    kids = [n["child"]] if "child" in n else n.get("children", []) + n.get("options", [])
    for k in kids:
        core_paths(k, nots + (1 if n.get("op") == "NOT" else 0), out)
    return out


def strip_dists(n):
    if n["op"] == "DIST":
        return strip_dists(n["child"])
    out = dict(n)
    if "child" in n:
        out["child"] = strip_dists(n["child"])
    for key in ("children", "options"):
        if key in n:
            out[key] = [strip_dists(x) for x in n[key]]
    return out


def dist_deletions(n):
    """Every variant of n with exactly one DIST node removed."""
    outs = []
    if n["op"] == "DIST":
        outs.append(n["child"])
    if "child" in n:
        outs += [{**n, "child": v} for v in dist_deletions(n["child"])]
    for key in ("children", "options"):
        for i, x in enumerate(n.get(key, [])):
            for v in dist_deletions(x):
                lst = list(n[key])
                lst[i] = v
                outs.append({**n, key: lst})
    return outs


def pure_chain(n):
    """If n (after removing DIST) is NOT^k(CORE(x)): return (k, x); else None."""
    n = strip_dists(n)
    k = 0
    while n["op"] == "NOT":
        k += 1
        n = n["child"]
    if n["op"] == "CORE":
        return k, n["child"]
    return None


def n_not(n):
    return (1 if n.get("op") == "NOT" else 0) + sum(n_not(k) for k in ([n["child"]] if "child" in n else [])
                                                   + n.get("children", []) + n.get("options", []))


# ------------------------------------------------------------------------------------------------ cards
_NO = ["any other case.", "every other case.", "all other cases."]
_no_i = [0]


def no_line():
    s = _NO[_no_i[0] % 3]
    _no_i[0] += 1
    return s


def Y(defs, yes, style="g"):
    """A yes/no card: definition lines, then a yes line that restates the question in full (same cues)."""
    lines = list(defs)
    if style == "g":
        lines += [f"- yes: {yes}", f"- no: {no_line()}"]
    elif style == "Y":
        lines += [f"- Yes: {yes}", f"- No: {no_line()}"]
    else:
        raise ValueError(style)
    return "\n".join(lines)


def DEFS(defs):
    """A definitions card with no yes/no lines (the answer is fixed by the instruction itself)."""
    assert defs
    return "\n".join(defs)


def YN(rung, ins, card, gold2, lf, phen, ff, fid, ant=None, looks=(), content=(), note=None, idv=None):
    """A yes/no question shared by both twins. gold2: gold of twin a + gold of twin b ('yn' or 'ny').
    idv: the id prefix of a row rewritten after round 2 (VERSION_R3); None keeps the round-2 id."""
    assert gold2 in ("yn", "ny"), gold2
    assert idv in (None, VERSION_R3), idv
    return dict(kind="yn", rung=rung, ins=ins, card=card, gold2=gold2, lf=lf, phen=phen, ff=ff, fid=fid, ant=ant,
                looks=list(looks), content=list(content), note=note, idv=idv)


def CHR(ins, card, gold, lf, opts, phen, ff, fid, looks=(), content=(), note=None):
    """A choice row of one ladder. card: None or {option: definition} (rendered in the final option order)."""
    return dict(kind="ch", rung="CH", ins=ins, card=card, gold=gold, lf=lf, opts=list(opts), phen=phen, ff=ff,
                fid=fid, looks=list(looks), content=list(content), note=note)


NOTE_C = "- note: the comment settles every claim asked about here."
NOTE_R = "- note: the report settles every claim asked about here."
NOTE_RS = "- note: the reports settle every claim asked about here."
NOTE_P = "- note: the post settles every claim asked about here."
NOTE_PS = "- note: the posts settle every claim asked about here."
NOTE_B = "- note: the comments settle every claim asked about here."
NOTE_REC = "- note: the record settles every claim asked about here."
NOTE_L = "- note: the log settles every claim asked about here."
NOTE_T = "- note: the thread settles every claim asked about here."
NOTE_CH = "- note: the chat settles every claim asked about here."
NOTE_TK = "- note: the ticket settles every claim asked about here."
# Round 3 (arbiter A4): 'the opposite' of a universal claim over a mixed batch has two readings (plain denial: some
# comment is toxic; contrary: every comment is toxic). The card now fixes the plain-denial reading.
NOTE_OPP = "- note: here 'the opposite' of a claim means its plain negation."

PAIRS = []


def PAIR(n, kind, source, a, b, rows, ch_a, ch_b):
    """a / b: dict(orig=[...], state=str, atoms={...}). rows: shared yes/no questions (first one is R0)."""
    assert rows[0]["rung"] == "R0"
    PAIRS.append(dict(n=n, kind=kind, source=source, twins={"a": a, "b": b}, rows=rows, ch={"a": ch_a, "b": ch_b}))


# common distractor and look-alike cues
def WON(pos=OF, dist=SS):
    return c("whether or not", SYN, pos, dist)


UNDER = c("under", LK, OF, SS)
NOTABLE = c("notable", LK, OF, SS)
NOTONLY = c("not only ... but also", LK, SSP, NS)
INFORMAL = c("in-", AFF, SSP, NS, "informal")
UNUSUAL = c("un-", AFF, SSP, NS, "unusual")
UNCLEAR = c("un-", AFF, SSP, NS, "unclear")
WITHOUT = c("without", SYN, SSP, NS)
DISREGARD = c("disregard", LEX, SSP, NS)
DONOT = c("not", SYN, SSP, NS, "do not")
IRREG = c("ir-", AFF, SSP, NS, "irregular")
INV_KEY = ["- yes: the claim fails for this {x}.", "- no: the claim holds for this {x}."]


def inv_key(x):
    return [ln.format(x=x) for ln in INV_KEY]


def CDN(lex, word=None):
    """A card-line distractor (a negation in a card line that does not decide the answer)."""
    return c(lex, SYN, CD, OFD, word)


# ================================================================================================ the twin ladders
# ---------------------------------------------------------------- P01 civil_comments: 'toxic' / 'non-toxic'
TOXD = ("- toxic: the comment insults, mocks, curses at or threatens a person or a group, for example by calling "
        "someone a name.")
NONTOXD = "the comment insults, mocks, curses at and threatens no one."
D01 = [TOXD, "- non-toxic: the comment does none of the things in the 'toxic' line."]
_sa, _ta = tox_state("g:civil:106", "toxic")
_sb, _tb = tox_state("g:civil:313", "not toxic")
PAIR(1, "card", "civil_comments",
     dict(orig=["g:civil:106"], state=_ta, atoms=dict(toxic=True, personal=True)),
     dict(orig=["g:civil:313"], state=_tb, atoms=dict(toxic=False, question=True)), [
         YN("R0", "Does the label 'toxic' fit this comment?",
            Y(D01 + ["- note: spelling and capital letters do not matter here."], "the label 'toxic' fits this comment."),
            "yn", lambda b: b.D(CDN("not", "do not"), b.CA("toxic")), [1, 18], "label_fit", "label_fit.does_fit"),
         YN("N1", "Does the label 'non-toxic' fit this comment?",
            Y(D01, "the label 'non-toxic' fits this comment."), "ny",
            lambda b: b.N(c("non-", AFF, CD, OFD, "non-toxic"), b.CA("toxic")), [5, 12], "label_fit",
            "label_fit.does_fit"),
         YN("N2", "Whether or not the comment uses capital letters, does it fail to fit the label 'non-toxic'?",
            Y(D01, "whether or not the comment uses capital letters, it fails to fit the label 'non-toxic'."), "yn",
            lambda b: b.D(WON(), b.N(c("fail", LEX, IC, SC), b.N(c("non-", AFF, CD, OFD, "non-toxic"),
                                                                  b.CA("toxic")))),
            [6, 11, 12, 15, 16], "side_clause", "side_clause.whether_or_not"),
         YN("N3", "Answer no if the reverse of the next sentence holds; otherwise answer yes. The label 'non-toxic' "
                  "fits this comment.",
            DEFS(D01), "ny",
            lambda b: b.N(c("answer no if", AM, AMP, SS), b.N(c("reverse", CS, SSP, NS), b.N(
                c("non-", AFF, CD, OFD, "non-toxic"), b.CA("toxic")))), [8, 12, 13], "answer_map",
            "answer_map.no_if_reverse_holds"),
     ],
     CHR("Which label is inapplicable to this comment?",
         {"toxic": TOXD[len("- toxic: "):], "non-toxic": NONTOXD,
          "personal": "the comment speaks to the reader directly as 'you'."}, "non-toxic",
         lambda b: b.CH([b.CA("toxic"), b.N(c("non-", AFF, CD, OFD, "non-toxic"), b.CA("toxic")), b.CA("personal")],
                        "false", c("in-", AFF, OF, SS, "inapplicable")),
         ["toxic", "non-toxic", "personal"], [36], "choice_neg", "choice_neg.label_fail_to_match"),
     CHR("Which label does this comment fail to match?",
         {"non-toxic": NONTOXD, "flagged": "the 'non-toxic' line excludes the comment.",
          "question": "the comment asks at least one question."}, "flagged",
         lambda b: b.CH([b.N(c("non-", AFF, CD, OFD, "non-toxic"), b.CA("toxic")),
                         b.N(c("exclude", LEX, CD, OFD, "excludes"), b.N(c("non-", AFF, CD, OFD, "non-toxic"),
                                                                          b.CA("toxic"))),
                         b.CA("question")], "false", c("fail", LEX, OF, SS)),
         ["non-toxic", "flagged", "question"], [8, 36], "choice_neg", "choice_neg.label_fail_to_match"))

# ---------------------------------------------------------------- P02 civil_comments: 'abusive' / 'civil' ('Yes' cards)
ABUSD = "the comment attacks a person or a group with insults, slurs, threats or crude name-calling."
CIVD = "the comment contains none of what the 'abusive' line lists."
D02 = [f"- abusive: {ABUSD}", f"- civil: {CIVD}"]
D02R = D02 + ["- rule: each comment gets exactly one of these two labels."]
_sa, _ta = tox_state("g:civil:59", "toxic")
_sb, _tb = tox_state("g:civil:342", "not toxic")
PAIR(2, "card", "civil_comments",
     dict(orig=["g:civil:59"], state=_ta, atoms=dict(toxic=True, insults=True)),
     dict(orig=["g:civil:342"], state=_tb, atoms=dict(toxic=False, ads=False)), [
         YN("R0", "Is 'abusive' the label that fits this comment?",
            Y(D02, "'abusive' is the label that fits this comment.", "Y"), "yn",
            lambda b: b.CA("toxic"), [1], "label_fit", "label_fit.is_the_label"),
         YN("N1", "Is 'civil' the only one of the two labels that fits this comment?",
            Y(D02R, "'civil' is the only one of the two labels that fits this comment.", "Y"), "ny",
            lambda b: b.N(c("none", SYN, CD, OFD), b.CA("toxic")), [12, 22, 24], "label_fit", "label_fit.only_label"),
         YN("N2", "A moderator tagged this comment 'civil'. Does the comment's wording contradict that tag?",
            Y(D02 + [NOTE_C], "the comment's wording contradicts the moderator's tag 'civil'.", "Y"), "yn",
            lambda b: b.N(c("contradict", LEX, OF, NS), b.N(c("none", SYN, CD, OFD), b.CA("toxic"))),
            [6, 10, 11, 12, 22], "verb_eval", "verb_eval.contradict_tag"),
         YN("N3", "Respond without quoting the comment. Is it false that the comment fails to fit the label 'civil'?",
            Y(D02, "responding without quoting the comment, it is false that the comment fails to fit the label "
                   "'civil'."), "ny",
            lambda b: b.D(WITHOUT, b.N(c("false", TF, OF, SS), b.N(c("fail", LEX, IC, SC, "fails"), b.N(
                c("none", SYN, CD, OFD), b.CA("toxic"))))), [8, 11, 12, 16, 22], "truth_q", "truth_q.false_that"),
     ],
     CHR("Disregard the comment's length. Which label is unsuitable for this comment?",
         {"abusive": ABUSD, "civil": CIVD, "insulting": "the comment calls someone a name or mocks someone."},
         "civil",
         lambda b: (b.DI(DISREGARD), b.CH([b.CA("toxic"), b.N(c("none", SYN, CD, OFD), b.CA("toxic")),
                                           b.CA("insults")], "false", c("un-", AFF, OF, SS, "unsuitable")))[1],
         ["abusive", "civil", "insulting"], [16, 36], "choice_neg", "choice_neg.label_fail_to_match"),
     CHR("Which label fits this comment best?",
         {"abusive": ABUSD, "civil": CIVD, "advertising": "the comment promotes a product or a sales link."},
         "civil",
         lambda b: b.CH([b.CA("toxic"), b.N(c("none", SYN, CD, OFD), b.CA("toxic")), b.CA("ads")], "true"),
         ["abusive", "civil", "advertising"], [22], "choice_pick", "choice_pick.label_best"))

# ---------------------------------------------------------------- P03 civil_comments: 'hostile' / 'harmless'
D03 = ["- hostile: the comment demeans, insults or threatens a person or a group.",
       "- harmless: the comment is not hostile."]
HARMLESS = "the comment demeans, insults and threatens no one."
_sa, _ta = tox_state("g:civil:52", "toxic")
_sb, _tb = tox_state("g:civil:363", "not toxic")
PAIR(3, "card", "civil_comments",
     dict(orig=["g:civil:52"], state=_ta, atoms=dict(toxic=True, praises=False, sunset=False, question=False)),
     dict(orig=["g:civil:363"], state=_tb, atoms=dict(toxic=False, home=False, red=False, says_nobody=False)), [
         YN("R0", "Is it true that this comment demeans, insults or threatens someone?", None, "yn",
            lambda b: b.CA("toxic"), [1], "truth_q", "truth_q.true_that"),
         YN("N1", "A triage summary says: 'the comment is hostile.' Does the comment refute that summary?",
            Y(D03 + [NOTE_C], "the comment refutes the triage summary 'the comment is hostile'."), "ny",
            lambda b: b.N(c("refute", LEX, OF, NS), b.CA("toxic")), [4, 12], "verb_eval", "verb_eval.refute_summary"),
         YN("N2", "Whether or not the comment names anyone, does it refute a triage summary saying that the comment is "
                  "harmless?",
            Y(D03 + [NOTE_C], "whether or not the comment names anyone, it refutes a triage summary saying that the "
                              "comment is harmless."), "yn",
            lambda b: b.D(WON(), b.N(c("refute", LEX, OF, SS), b.N(c("-less", AFF, CD, OFD, "harmless"),
                                                                    b.CA("toxic")))),
            [6, 10, 11, 12, 15, 16], "side_clause", "side_clause.whether_or_not"),
         YN("N3", "Is it false that this comment is not free of insults and threats?", None, "ny",
            lambda b: b.N(c("false", TF, OF, SS), b.N(c("not", SYN, IC, SC), b.N(c("free of", LEX, IC, SC),
                                                                                   b.CA("toxic")))),
            [8], "truth_q", "truth_q.false_that"),
     ],
     CHR("Which statement about this comment is true?", None, "It isn't free of insults.",
         lambda b: b.CH([b.CA("praises"), b.N(c("n't", SYN, CO, SC, "isn't"), b.N(c("free of", LEX, CO, SC),
                                                                                  b.CA("toxic"))),
                         b.CA("sunset"), b.CA("question")], "true"),
         ["It praises Jeff Dunham.", "It isn't free of insults.", "It describes a sunset.", "It asks a question."], [],
         "choice_true", "choice_true.which_statement"),
     CHR("Which statement about this comment is true?", None, "It does not insult or threaten anyone.",
         lambda b: b.CH([b.CA("home"), b.N(c("not", SYN, CO, SC, "does not"), b.CA("toxic")), b.CA("red"),
                         b.CA("says_nobody")], "true"),
         ["It says the writer stayed home on Thursday.", "It does not insult or threaten anyone.",
          "It mentions a red marker.", "It says nobody saw the bus."], [], "choice_true",
         "choice_true.which_statement", content=["nobody (option 4: reported content)"]))

# ---------------------------------------------------------------- P04 civil_comments: 'insulting' / 'insult-free'
INSD = "the comment calls a person or a group a name, mocks them, swears at them or threatens them."
INSFREE = "the comment calls no one a name and mocks no one."
D04 = [f"- insulting: {INSD}", "- insult-free: the comment does none of that."]
_sa, _ta = tox_state("g:civil:120", "toxic")
_sb, _tb = tox_state("g:civil:369", "not toxic")
PAIR(4, "card", "civil_comments",
     dict(orig=["g:civil:120"], state=_ta, atoms=dict(toxic=True, popular_anywhere=False, governor=False,
                                                      praises=False)),
     dict(orig=["g:civil:369"], state=_tb, atoms=dict(toxic=False, doctors=True)), [
         YN("R0", "Under the card's definitions, does 'insulting' describe this comment?",
            Y(D04, "under the card's definitions, 'insulting' describes this comment."), "yn",
            lambda b: b.CA("toxic"), [1, 20], "label_fit", "label_fit.describes", looks=[UNDER]),
         YN("N1", "Does the comment not insult, mock, swear at or threaten anyone?",
            "\n".join(D04 + ["- note: spelling and capital letters do not matter here.",
                             "- yes: the comment does not insult, mock, swear at or threaten anyone.",
                             "- no: the comment insults, mocks, swears at or threatens someone."]), "ny",
            lambda b: b.D(CDN("not", "do not"), b.N(c("not", SYN, IC, SC, "does not"), b.CA("toxic"))),
            [16, 18, 38], "polar_inner", "polar_inner.does_not"),
         YN("N2", "Claim: the comment is insult-free as the card defines it. Give the answer that the key in the card "
                  "assigns to this claim.",
            "\n".join(D04 + inv_key("comment")), "yn",
            lambda b: b.N(c("fails", AM, YK, OFD), b.N(c("-free", AFF, CD, OFD, "insult-free"),
                                                                 b.CA("toxic"))),
            [6, 12, 14], "key_card", "key_card.inverted_key"),
         YN("N3", "Even if the comment has no greeting, take the reverse of the claim below and judge that reverse. "
                  "Claim: the comment is insult-free. Is that reverse unsupported by the comment?",
            Y(D04 + [NOTE_C], "even if the comment has no greeting, the reverse of the claim 'the comment is "
                              "insult-free' is unsupported by the comment."), "ny",
            lambda b: b.D(c("no", SYN, SSP, NS), b.N(c("unsupported", TF, OF, NS), b.N(c("reverse", CS, SSP, NS), b.N(
                c("-free", AFF, CD, OFD, "insult-free"), b.CA("toxic"))))), [8, 12, 16], "reverse_claim",
            "reverse_claim.take_reverse"),
     ],
     CHR(f"Here 'insult-free' means {INSFREE[:-1]}. Which statement about the comment is true?", None,
         "It is not insult-free.",
         lambda b: b.CH([b.CA("popular_anywhere"), b.N(c("not", SYN, CO, SC), b.N(c("-free", AFF, CO, SC,
                                                                                     "insult-free"), b.CA("toxic"))),
                         b.CA("governor"), b.CA("praises")], "true"),
         ["It says Trump is not popular anywhere.", "It is not insult-free.", "It names Alaska's governor.",
          "It praises George W."], [], "choice_true", "choice_true.which_statement",
         content=["not (option 1: reported content)"]),
     CHR("Which label does this comment fail to match?",
         {"insult-free": INSFREE, "needs review": "the 'insult-free' line leaves the comment out.",
          "about doctors": "the comment talks about doctors."}, "needs review",
         lambda b: b.CH([b.N(c("-free", AFF, CD, OFD, "insult-free"), b.CA("toxic")),
                         b.N(c("leave out", LEX, CD, OFD, "leaves ... out"), b.N(c("-free", AFF, CD, OFD, "insult-free"),
                                                                                  b.CA("toxic"))),
                         b.CA("doctors")], "false", c("fail", LEX, OF, SS)),
         ["insult-free", "needs review", "about doctors"], [8, 36], "choice_neg", "choice_neg.label_fail_to_match"))

# ---------------------------------------------------------------- P05 toxic_conv: 'offensive' / 'inoffensive'
OFFD = "the comment insults, mocks, curses at or threatens a person or a group."
INOFFD = "the comment insults, mocks, curses at and threatens no one."
D05 = [f"- offensive: {OFFD}", "- inoffensive: the comment is not offensive."]
_sa, _ta = tox_state("g:toxconv:6", "toxic")
_sb, _tb = tox_state("g:toxconv:249", "not toxic")
PAIR(5, "card", "toxic_conv",
     dict(orig=["g:toxconv:6"], state=_ta, atoms=dict(toxic=True, praise=False)),
     dict(orig=["g:toxconv:249"], state=_tb, atoms=dict(toxic=False, friendly=True)), [
         YN("R0", "Going by the card, is the comment offensive?",
            Y(D05 + ["- note: the comment's length does not matter.", "- note: no label depends on the topic alone."],
              "going by the card, the comment is offensive."), "yn",
            lambda b: b.D(CDN("not", "does not"), b.D(CDN("no"), b.CA("toxic"))),
            [1, 17, 18], "direct_q", "direct_q.going_by_card"),
         YN("N1", "Is the comment inoffensive, going by the card?",
            Y(D05, "the comment is inoffensive, going by the card."), "ny",
            lambda b: b.N(c("in-", AFF, CD, OFD, "inoffensive"), b.CA("toxic")), [5, 12], "direct_q",
            "direct_q.going_by_card"),
         YN("D", "Ignore informal spelling. Is the comment inoffensive, going by the card?",
            Y(D05, "ignoring informal spelling, the comment is inoffensive, going by the card."), "ny",
            lambda b: b.D(INFORMAL, b.N(c("in-", AFF, CD, OFD, "inoffensive"), b.CA("toxic"))), [5, 12, 16],
            "direct_q", "direct_q.going_by_card_format"),
         YN("N3", "Answer no if the comment refutes the tag 'inoffensive'; otherwise answer yes.",
            DEFS(D05 + [NOTE_C]), "ny",
            lambda b: b.N(c("answer no if", AM, AMP, SS), b.N(c("refute", LEX, OF, SC, "refutes"), b.N(
                c("in-", AFF, CD, OFD, "inoffensive"), b.CA("toxic")))), [8, 10, 12, 13], "answer_map",
            "answer_map.no_if_otherwise_yes"),
     ],
     CHR("Which label fits this comment?",
         {"inoffensive": INOFFD, "escalated": "the 'inoffensive' line excludes the comment.",
          "praise": "the comment praises someone."}, "escalated",
         lambda b: b.CH([b.N(c("in-", AFF, CD, OFD, "inoffensive"), b.CA("toxic")),
                         b.N(c("exclude", LEX, CD, OFD, "excludes"), b.N(c("in-", AFF, CD, OFD, "inoffensive"),
                                                                          b.CA("toxic"))),
                         b.CA("praise")], "true"),
         ["inoffensive", "escalated", "praise"], [], "choice_pick", "choice_pick.label_fits"),
     CHR("Which label is inapplicable to this comment?",
         {"inoffensive": INOFFD, "escalated": "the 'inoffensive' line excludes the comment.",
          "friendly": "the comment speaks to someone warmly, for example as 'my friend'."}, "escalated",
         lambda b: b.CH([b.N(c("in-", AFF, CD, OFD, "inoffensive"), b.CA("toxic")),
                         b.N(c("exclude", LEX, CD, OFD, "excludes"), b.N(c("in-", AFF, CD, OFD, "inoffensive"),
                                                                          b.CA("toxic"))),
                         b.CA("friendly")], "false", c("in-", AFF, OF, SS, "inapplicable")),
         ["inoffensive", "escalated", "friendly"], [8, 36], "choice_neg", "choice_neg.label_fail_to_match"))

# ---------------------------------------------------------------- P06 toxic_conv: 'attack' / 'no attack'
ATKD = "the comment insults, mocks, threatens or calls names at a person or a group."
NOATKD = "the comment contains nothing listed for 'attack'."
D06 = [f"- attack: {ATKD}", "- no attack: the comment contains nothing listed in the 'attack' line."]
_sa, _ta = tox_state("g:toxconv:135", "toxic")
_sb, _tb = tox_state("g:toxconv:244", "not toxic")
PAIR(6, "card", "toxic_conv",
     dict(orig=["g:toxconv:135"], state=_ta, atoms=dict(toxic=True, exclaims=True)),
     dict(orig=["g:toxconv:244"], state=_tb, atoms=dict(toxic=False, hope=True)), [
         YN("R0", "Answer yes if the label 'attack' fits this comment, and no otherwise.", DEFS(D06), "yn",
            lambda b: b.CA("toxic"), [1], "answer_map", "answer_map.yes_if_otherwise_no"),
         YN("N1", "Answer no if the label 'attack' fits this comment; otherwise answer yes.", DEFS(D06), "ny",
            lambda b: b.N(c("answer no if", AM, AMP, SS), b.CA("toxic")), [13], "answer_map",
            "answer_map.no_if_otherwise_yes"),
         YN("N2", "Under the card, is the claim that this comment fits 'no attack' unfounded?",
            Y(D06 + [NOTE_C, "- note: punctuation is irrelevant to every label."],
              "under the card, the claim that this comment fits 'no attack' is unfounded."), "yn",
            lambda b: b.D(c("ir-", AFF, CD, OFD, "irrelevant"), b.N(c("unfounded", TF, OF, SS), b.N(c("no", SYN, CD, OFD, "no attack"),
                                                                         b.CA("toxic")))),
            [6, 10, 11, 12, 16, 18, 20], "attributed", "attributed.claim_unfounded", looks=[UNDER]),
         YN("N3", "Whether or not the comment is sarcastic, is it untrue that the comment fails to match the label "
                  "'no attack'?",
            Y(D06, "whether or not the comment is sarcastic, it is untrue that the comment fails to match the label "
                   "'no attack'."), "ny",
            lambda b: b.D(WON(), b.N(c("untrue", TF, OF, SS), b.N(c("fail", LEX, IC, SC, "fails"), b.N(
                c("no", SYN, CD, OFD, "no attack"), b.CA("toxic"))))), [8, 11, 12, 15, 16], "side_clause",
            "side_clause.whether_or_not"),
     ],
     CHR("Disregard the capital letters. Which label does this comment fail to match?",
         {"attack": ATKD, "no attack": NOATKD, "exclamation": "the comment ends with an exclamation mark."},
         "no attack",
         lambda b: (b.DI(DISREGARD), b.CH([b.CA("toxic"), b.N(c("no", SYN, CD, OFD, "no attack"), b.CA("toxic")),
                                           b.CA("exclaims")], "false", c("fail", LEX, OF, SS)))[1],
         ["attack", "no attack", "exclamation"], [16, 36], "choice_neg", "choice_neg.label_fail_to_match"),
     CHR("Which label is unsuitable for this comment?",
         {"no attack": NOATKD, "hope": "the comment expresses a hope.",
          "held": "the comment fails to fit the 'no attack' line."}, "held",
         lambda b: b.CH([b.N(c("no", SYN, CD, OFD, "no attack"), b.CA("toxic")), b.CA("hope"),
                         b.N(c("fail", LEX, CD, OFD, "fails"), b.N(c("no", SYN, CD, OFD, "no attack"),
                                                                    b.CA("toxic")))],
                        "false", c("un-", AFF, OF, SS, "unsuitable")),
         ["no attack", "hope", "held"], [8, 36], "choice_neg", "choice_neg.label_fail_to_match"))

# ---------------------------------------------------------------- P07 toxic_conv: 'rude' / 'respectful' (AR)
D07 = ["- rude: the comment insults, mocks or threatens someone, for example by calling the reader a name.",
       "- respectful: every other comment."]
_sa, _ta = tox_state("g:toxconv:45", "toxic")
_sb, _tb = tox_state("g:toxconv:272", "not toxic")
PAIR(7, "card", "toxic_conv",
     dict(orig=["g:toxconv:45"], state=_ta, atoms=dict(toxic=True, thanks=False, praises=False, question=False,
                                                     judge=False)),
     dict(orig=["g:toxconv:272"], state=_tb, atoms=dict(toxic=False, forecast=True, timeframe=True, eu=True)), [
         YN("R0", "Does the label 'rude' apply to this comment?",
            Y(D07 + ["- note: a label never depends on spelling."], "the label 'rude' applies to this comment."), "yn",
            lambda b: b.D(CDN("never"), b.CA("toxic")), [1, 18], "label_fit", "label_fit.applies"),
         YN("AR", "Does the label 'respectful' apply to this comment?",
            Y(D07, "the label 'respectful' applies to this comment."), "ny",
            lambda b: b.NN(b.CA("toxic")), [22], "label_fit", "label_fit.applies"),
         YN("N2", "A moderator wrote that the comment is not rude. Does the comment's wording refute what the "
                  "moderator wrote?",
            Y(D07 + [NOTE_C], "the comment's wording refutes what the moderator wrote, namely that the comment is not "
                              "rude."), "yn",
            lambda b: b.N(c("refute", LEX, OF, SC), b.N(c("not", SYN, IC, SC), b.CA("toxic"))), [6, 10],
            "verb_eval", "verb_eval.refute_claim"),
         YN("N3", "A note says the comment isn't rude. Is it untrue that the comment contradicts that note?",
            Y(D07 + [NOTE_C], "it is untrue that the comment contradicts the note saying that the comment isn't rude."),
            "ny",
            lambda b: b.N(c("untrue", TF, OF, NS), b.N(c("contradict", LEX, OF, NS, "contradicts"), b.N(
                c("n't", SYN, IC, SC, "isn't"), b.CA("toxic")))), [8, 10, 12], "attributed",
            "attributed.untrue_contradicts"),
     ],
     CHR("Which statement about the comment is true?", None, "It lacks praise for the person it addresses.",
         lambda b: b.CH([b.CA("thanks"), b.N(c("lack", LEX, CO, SC, "lacks"), b.CA("praises")), b.CA("question"),
                         b.CA("judge")], "true"),
         ["It thanks Ms. Flowers.", "It lacks praise for the person it addresses.", "It asks a question.",
          "It names a judge."], [4], "choice_true", "choice_true.which_statement"),
     CHR("Which statement about this comment is untrue?", None,
         "It is false that the comment is free of insults.",
         lambda b: b.CH([b.CA("forecast"), b.N(c("false", TF, CO, SC), b.N(c("free of", LEX, CO, SC), b.CA("toxic"))),
                         b.CA("timeframe"), b.CA("eu")], "false", c("untrue", TF, OF, SS)),
         ["It predicts the end of the European Union.", "It is false that the comment is free of insults.",
          "It gives a time frame of a year or two.", "It mentions the European Union."], [8, 36], "choice_neg",
         "choice_neg.untrue"))

# ---------------------------------------------------------------- severity cards (my own coarse levels)
SEVL = {"mild": "any injury was left alone or treated only by the victim or another layperson.",
        "moderate": "the most serious care was from a doctor, nurse, clinic or emergency department.",
        "severe": "the main victim was admitted to hospital, had surgery or died."}
SEV = [f"- {k}: {v}" for k, v in SEVL.items()] + \
    ["- rule: go by the care the report states; exactly one level fits each report."]
SEV_INS = ("Levels: 'mild' means at most first aid by the victim or a layperson; 'moderate' means the most serious "
           "care was from a doctor, nurse, clinic or emergency department; 'severe' means a hospital stay, surgery or "
           "death.")

# ---------------------------------------------------------------- P08 saferproducts: P = 'severe'
_sa, _ta = raw_text("spdb-20141026-C470F-2147439613", "injury, hospital admission")
_sb, _tb = raw_text("spdb-20170418-CF8ED-2147404282", "injury, emergency department treatment")
PAIR(8, "card", "gd_saferproducts_severity",
     dict(orig=["spdb-20141026-C470F-2147439613"], state=_ta, atoms=dict(severe=True, mild=False, moderate=False)),
     dict(orig=["spdb-20170418-CF8ED-2147404282"], state=_tb, atoms=dict(severe=False, mild=False, moderate=True)), [
         YN("R0", "Does the level 'severe' fit this report?", Y(SEV, "the level 'severe' fits this report."), "yn",
            lambda b: b.CA("severe"), [1], "label_fit", "label_fit.does_fit"),
         YN("AR", "Is the level for this report either 'mild' or 'moderate'?",
            Y(SEV, "the level for this report is either 'mild' or 'moderate'."), "ny",
            lambda b: b.NN(b.CA("severe")), [], "label_fit", "label_fit.either_or"),
         YN("N2", "Disregard the product name. A triage note says the level for this report isn't 'severe'. Does the "
                  "report contradict that note?",
            Y(SEV + [NOTE_R], "disregarding the product name, the report contradicts the triage note saying that the "
                              "level for this report isn't 'severe'."), "yn",
            lambda b: b.D(DISREGARD, b.N(c("contradict", LEX, OF, NS), b.N(c("n't", SYN, IC, SC, "isn't"),
                                                                          b.CA("severe")))),
            [6, 10, 12, 16, 21], "verb_eval", "verb_eval.refute_note", ant=lambda at: not at["mild"]),
         YN("N3", "Is it unfounded to say that the report cannot rule out the level 'severe'?",
            Y(SEV + [NOTE_R], "it is unfounded to say that the report cannot rule out the level 'severe'."), "ny",
            lambda b: b.N(c("unfounded", TF, OF, SS), b.N(c("cannot", SYN, IC, SC), b.N(
                c("rule out", LEX, IC, SC), b.CA("severe")))), [8, 10], "attributed", "attributed.unfounded_to_say"),
     ],
     CHR("Which label fits this report?",
         {"non-severe": "the report's level is anything other than 'severe'.",
          "top": "the report fails to fit the 'non-severe' line.", "mild": SEVL["mild"]}, "top",
         lambda b: b.CH([b.N(c("non-", AFF, CD, OFD, "non-severe"), b.CA("severe")),
                         b.N(c("fail", LEX, CD, OFD, "fails"), b.N(c("non-", AFF, CD, OFD, "non-severe"),
                                                                    b.CA("severe"))),
                         b.CA("mild")], "true"),
         ["non-severe", "top", "mild"], [37], "choice_pick", "choice_pick.level_label"),
     CHR(SEV_INS + " Which statement about this report is true?", None, "Its level is not 'severe'.",
         lambda b: b.CH([b.CA("mild"), b.N(c("not", SYN, CO, SC), b.CA("severe")), b.CA("severe")], "true"),
         ["Its level is 'mild'.", "Its level is not 'severe'.", "Its level is 'severe'."], [37], "choice_true",
         "choice_true.level_statement"))

# ---------------------------------------------------------------- P09 saferproducts: P = 'mild'
_sa, _ta = raw_text("spdb-20240618-7C1F7-2147338536", "injury, no first aid or medical care")
_sb, _tb = raw_text("spdb-20191007-4CBBC-2147377264", "injury, seen by a medical professional")
PAIR(9, "card", "gd_saferproducts_severity",
     dict(orig=["spdb-20240618-7C1F7-2147338536"], state=_ta, atoms=dict(mild=True, severe=False, moderate=False)),
     dict(orig=["spdb-20191007-4CBBC-2147377264"], state=_tb,
          atoms=dict(mild=False, severe=False, moderate=True, folded=True, stitches=True, urgent=True)), [
         YN("R0", "Is 'mild' the level that fits this report?",
            Y(SEV + ["- note: a report need not name the store."], "'mild' is the level that fits this report."), "yn",
            lambda b: b.D(CDN("need not"), b.CA("mild")), [1, 18], "label_fit", "label_fit.is_the_label"),
         YN("N1", "Disregard the brand name. Say no if the level 'mild' fits this report, and yes in every other case.",
            DEFS(SEV), "ny",
            lambda b: b.D(DISREGARD, b.N(c("say no if", AM, AMP, SS), b.CA("mild"))), [13, 16], "answer_map",
            "answer_map.say_no_if"),
         YN("N2", "A triage note says the level for this report isn't 'mild'. Does the report give grounds to reject "
                  "that note?",
            Y(SEV + [NOTE_R], "the report gives grounds to reject the triage note saying that the level for this "
                              "report isn't 'mild'."), "yn",
            lambda b: b.N(c("reject", LEX, OF, NS), b.N(c("n't", SYN, IC, SC, "isn't"), b.CA("mild"))), [6, 10, 12, 21],
            "verb_eval", "verb_eval.grounds_to_reject", ant=lambda at: not at["severe"]),
         YN("N3", "Is it false that the report doesn't rule out the level 'mild'?",
            Y(SEV + [NOTE_R], "it is false that the report doesn't rule out the level 'mild'."), "ny",
            lambda b: b.N(c("false", TF, OF, SS), b.N(c("n't", SYN, IC, SC, "doesn't"), b.N(
                c("rule out", LEX, IC, SC), b.CA("mild")))), [8], "truth_q", "truth_q.false_that"),
     ],
     CHR("Which label fits this report?",
         {"non-mild": "the report's level is anything other than 'mild'.",
          "low": "the report fails to fit the 'non-mild' line.", "severe": SEVL["severe"]}, "low",
         lambda b: b.CH([b.N(c("non-", AFF, CD, OFD, "non-mild"), b.CA("mild")),
                         b.N(c("fail", LEX, CD, OFD, "fails"), b.N(c("non-", AFF, CD, OFD, "non-mild"),
                                                                    b.CA("mild"))),
                         b.CA("severe")], "true"),
         ["non-mild", "low", "severe"], [37], "choice_pick", "choice_pick.level_label"),
     CHR("Disregard the dollar amount. " + SEV_INS + " Exactly one level fits each report. Which statement about this "
         "report is untrue?", None, "It is false that 'moderate' is the only level that fits it.",
         lambda b: (b.DI(DISREGARD), b.CH([b.CA("folded"), b.CA("stitches"), b.N(c("false", TF, CO, SC),
                                                                                b.CA("moderate")),
                                           b.CA("urgent")], "false", c("untrue", TF, OF, SS)))[1],
         ["The knife folded onto the writer's finger.", "The writer needed 3 stitches.",
          "It is false that 'moderate' is the only level that fits it.",
          "The writer went to an urgent care clinic."], [16, 24, 36], "choice_neg", "choice_neg.untrue"))

# ---------------------------------------------------------------- P10 saferproducts: P = someone hurt (items 23, 25)
HURT = ["- hurt: a person was physically injured, however slightly.",
        "- medical care: first aid by a layperson, a visit to a doctor or nurse, emergency treatment, or a hospital "
        "stay."]
HOMEH = ["- home-handled: any incident, except one where a doctor, nurse, clinic or emergency department treated "
         "someone."]
_sa, _ta = raw_text("spdb-20210826-C7385-2147360887", "incident, but no injury")
_sb, _tb = raw_text("spdb-20140320-3CB2C-2147446196", "injury, seen by a medical professional")
PAIR(10, "card", "gd_saferproducts_severity",
     dict(orig=["spdb-20210826-C7385-2147360887"], state=_ta,
          atoms=dict(hurt=False, care=False, treated=False, appliance=True)),
     dict(orig=["spdb-20140320-3CB2C-2147446196"], state=_tb,
          atoms=dict(hurt=True, care=True, treated=True, blue=False, thumb=False, admitted=False)), [
         YN("R0", "Setting aside any notable typos, does the report describe someone getting hurt?",
            Y(HURT, "setting aside any notable typos, the report describes someone getting hurt."), "ny",
            lambda b: b.CA("hurt"), [1, 20], "direct_q", "direct_q.describes", looks=[NOTABLE]),
         YN("N1", "Is it true that the report describes no medical care for anyone?",
            Y(HURT, "it is true that the report describes no medical care for anyone."), "yn",
            lambda b: b.N(c("no", SYN, IC, SC), b.CA("care")), [2, 25], "truth_q", "truth_q.true_that"),
         YN("N2", "Is it false that the label 'home-handled' fits this report?",
            Y(HOMEH + ["- note: the store's name is irrelevant."],
              "it is false that the label 'home-handled' fits this report."), "ny",
            lambda b: b.D(c("ir-", AFF, CD, OFD, "irrelevant"), b.N(c("false", TF, OF, SS), b.N(c("except", LEX, CD, OFD),
                                                                                   b.CA("treated")))),
            [6, 11, 12, 16, 18, 23], "truth_q", "truth_q.false_that_label"),
         YN("N3", "Is it unjustified to say that the report does not show that not a single person was hurt?",
            Y(HURT + [NOTE_R], "it is unjustified to say that the report does not show that not a single person was "
                               "hurt.", "Y"), "yn",
            lambda b: b.N(c("unjustified", TF, OF, SS), b.N(c("not", SYN, IC, SC, "does not"), b.N(
                c("not a single", SYN, IC, SC), b.CA("hurt")))), [8, 10], "attributed", "attributed.unjustified_to_say"),
     ],
     CHR("Which label is inapplicable to this report?",
         {"unhurt": "nobody was physically injured.", "injury report": "the report fails to fit the 'unhurt' line.",
          "appliance": "the report is about a household appliance."}, "injury report",
         lambda b: b.CH([b.N(c("un-", AFF, CD, OFD, "unhurt"), b.CA("hurt")),
                         b.N(c("fail", LEX, CD, OFD, "fails"), b.N(c("un-", AFF, CD, OFD, "unhurt"), b.CA("hurt"))),
                         b.CA("appliance")], "false", c("in-", AFF, OF, SS, "inapplicable")),
         ["unhurt", "injury report", "appliance"], [8, 36], "choice_neg", "choice_neg.label_fail_to_match"),
     CHR("Which statement about this report is true?", None, "It is untrue that the writer was unhurt.",
         lambda b: b.CH([b.CA("blue"), b.N(c("untrue", TF, CO, SC), b.N(c("un-", AFF, CO, SC, "unhurt"),
                                                                        b.CA("hurt"))),
                         b.CA("thumb"), b.CA("admitted")], "true"),
         ["The stroller is blue.", "It is untrue that the writer was unhurt.", "The writer's thumb was crushed.",
          "The writer was admitted to hospital."], [], "choice_true", "choice_true.which_statement"))

# ---------------------------------------------------------------- wiki desk cards (my own wording)
DESK = {
    "Computing desk": "questions about computers, software, devices and the internet.",
    "Mathematics desk": "questions about numbers, proofs, puzzles and calculations.",
    "Language desk": "questions about words, grammar, meanings and usage.",
    "Science desk": "questions about nature, the human body, physics, chemistry and biology.",
    "Entertainment desk": "questions about songs, films, television, celebrities and popular culture.",
    "Humanities desk": "questions about history, religion, society, people and the arts.",
}


def desk_lines(names):
    return [f"- {n}: {DESK[n]}" for n in names]


# ---------------------------------------------------------------- P11 wiki: P = Computing desk (AR)
WD11 = desk_lines(["Computing desk", "Mathematics desk", "Language desk", "Science desk"]) + \
    ["- rule: exactly one listed desk is the best place for each post."]
WD11S = desk_lines(["Computing desk", "Mathematics desk", "Language desk", "Science desk"]) + \
    ["- rule: exactly one listed desk suits each post."]
DESK11_INS = ("Each post belongs at exactly one of these desks: Computing (computers and software), Mathematics "
              "(numbers and proofs), Language (words and grammar) and Science (nature and the human body).")
_sa, _ta = raw_text("4f6b0dbd763e162b", "Computing reference desk")
_sb, _tb = raw_text("2546ae117747c6f1", "Science reference desk")
PAIR(11, "card", "gd_wiki_help_routing",
     dict(orig=["4f6b0dbd763e162b"], state=_ta, atoms=dict(comp=True, sci=False, printer=False, lang=False,
                                                           wiki_head=False)),
     dict(orig=["2546ae117747c6f1"], state=_tb, atoms=dict(comp=False, math=False)), [
         YN("R0", "Is the Computing desk the best listed place for this post?",
            Y(desk_lines(["Computing desk", "Mathematics desk", "Language desk", "Science desk"])
              + ["- other: the post fits none of the desks above.",
                 "- rule: exactly one of these lines is the best place for each post."],
              "the Computing desk is the best listed place for this post."), "yn",
            lambda b: b.D(CDN("none"), b.CA("comp")), [1, 18], "route_q", "route_q.best_listed_place"),
         YN("AR", "Does this post belong at the Mathematics, Language or Science desk?",
            Y(WD11, "this post belongs at the Mathematics, Language or Science desk."), "ny",
            lambda b: b.NN(b.CA("comp")), [], "route_q", "route_q.belong_at"),
         YN("N2", "Even if the post names no book, does it give grounds to reject the claim that the Computing desk "
                  "fails to suit it?",
            Y(WD11 + [NOTE_P], "even if the post names no book, it gives grounds to reject the claim that the "
                               "Computing desk fails to suit it."), "yn",
            lambda b: b.D(c("no", SYN, OF, SS), b.N(c("reject", LEX, OF, SS), b.N(c("fail", LEX, IC, SC, "fails"),
                                                                                  b.CA("comp")))),
            [7, 10, 15, 16], "verb_eval", "verb_eval.grounds_to_reject"),
         YN("N3", "Setting aside any notable typos, consider the opposite of the next sentence. The Computing desk "
                  "isn't the only listed desk that suits this post. Is that opposite unsupported by the post?",
            Y(WD11S + [NOTE_P], "setting aside any notable typos, the opposite of the sentence 'the Computing desk "
                                "isn't the only listed desk that suits this post' is unsupported by the post."), "ny",
            lambda b: b.N(c("unsupported", TF, OF, NS), b.N(c("opposite", CS, SSP, NS), b.N(c("n't", SYN, IC, SC,
                                                                                              "isn't"),
                                                                                           b.CA("comp")))),
            [8, 12, 20, 24], "reverse_claim", "reverse_claim.opposite_next_sentence", looks=[NOTABLE]),
     ],
     CHR(DESK11_INS + " Which statement about this post is true?", None, "It does not belong at the Science desk.",
         lambda b: b.CH([b.CA("printer"), b.N(c("not", SYN, CO, SC, "does not"), b.CA("sci")), b.CA("lang"),
                         b.CA("wiki_head")], "true"),
         ["It asks about a printer.", "It does not belong at the Science desk.", "It belongs at the Language desk.",
          "Its heading mentions Wikipedia."], [], "choice_true", "choice_true.which_statement"),
     CHR("Which line describes the best place for this post?",
         {"Computing desk": DESK["Computing desk"], "Mathematics desk": DESK["Mathematics desk"],
          "elsewhere": "any listed desk other than the Computing desk."}, "elsewhere",
         lambda b: b.CH([b.CA("comp"), b.CA("math"), b.N(c("other than", LEX, CD, OFD), b.CA("comp"))], "true"),
         ["Computing desk", "Mathematics desk", "elsewhere"], [], "choice_pick", "choice_pick.desk_line"))

# ---------------------------------------------------------------- P12 wiki: P = Language desk ('Yes' cards)
OFFTOP = "the post is about something other than words, grammar, meanings or usage."
WD12 = desk_lines(["Language desk", "Entertainment desk", "Humanities desk", "Science desk"]) + \
    [f"- off-topic for Language: {OFFTOP}", "- rule: exactly one listed desk is the best place for each post."]
DESK12_INS = ("Each post belongs at exactly one of these desks: Language (words and grammar), Entertainment (films, "
              "music and television), Humanities (history and society) and Science (nature and the human body).")
_sa, _ta = raw_text("be1b61142a961661", "Language reference desk")
_sb, _tb = raw_text("2e4f0a66890a3f9b", "Entertainment reference desk")
PAIR(12, "card", "gd_wiki_help_routing",
     dict(orig=["be1b61142a961661"], state=_ta, atoms=dict(lang=True, question=True)),
     dict(orig=["2e4f0a66890a3f9b"], state=_tb, atoms=dict(lang=False, finale=True, crane=True, passions=True)), [
         YN("R0", "Should this post go to the Language desk, as the card describes it?",
            Y(WD12, "this post should go to the Language desk, as the card describes it.", "Y"), "yn",
            lambda b: b.CA("lang"), [1], "route_q", "route_q.should_go"),
         YN("N1", "Does this post ask about something other than words, grammar, meanings or usage?",
            Y(WD12 + ["- note: greetings alone decide nothing here."],
              "this post asks about something other than words, grammar, meanings or usage.", "Y"), "ny",
            lambda b: b.D(CDN("nothing"), b.N(c("other than", LEX, IC, SC), b.CA("lang"))), [4, 16, 18],
            "direct_q", "direct_q.asks_about"),
         YN("N2", "Does the post fail to fit the label 'off-topic for Language'?",
            Y(WD12, "the post fails to fit the label 'off-topic for Language'.", "Y"), "yn",
            lambda b: b.N(c("fail", LEX, IC, SC), b.N(c("other than", LEX, CD, OFD), b.CA("lang"))), [7, 11, 12],
            "verb_eval", "verb_eval.fail_to_fit"),
         YN("N3", "Respond without quoting the post. A helper wrote: 'This post is unsuited to the Language desk.' Does "
                  "the post fail to refute the helper's note?",
            Y(WD12 + [NOTE_P], "responding without quoting the post, the post fails to refute the helper's note 'this "
                               "post is unsuited to the Language desk'."), "ny",
            lambda b: b.D(WITHOUT, b.N(c("fail", LEX, OF, NS), b.N(c("refute", LEX, OF, NS), b.N(
                c("un-", AFF, IC, SC, "unsuited"), b.CA("lang"))))), [8, 10, 12, 16], "verb_eval",
            "verb_eval.fail_to_refute"),
     ],
     CHR("Which of these lines does the post fail to fit?",
         {"Language desk": DESK["Language desk"], "off-topic for Language": OFFTOP,
          "question": "the post asks a question."}, "off-topic for Language",
         lambda b: b.CH([b.CA("lang"), b.N(c("other than", LEX, CD, OFD), b.CA("lang")), b.CA("question")],
                        "false", c("fail", LEX, OF, SS)),
         ["Language desk", "off-topic for Language", "question"], [22, 36], "choice_neg",
         "choice_neg.line_fail_to_fit"),
     CHR(DESK12_INS + f" Here 'off-topic for Language' means {OFFTOP[:-1]}. Which statement about this post is untrue?",
         None, "It is false that the label 'off-topic for Language' fits it.",
         lambda b: b.CH([b.CA("finale"), b.CA("crane"),
                         b.N(c("false", TF, CO, SC), b.N(c("other than", LEX, SSP, FAR), b.CA("lang"))),
                         b.CA("passions")], "false", c("untrue", TF, OF, SS)),
         ["It asks about the final episode of a TV series.", "It names a character called Alistair Crane.",
          "It is false that the label 'off-topic for Language' fits it.", "It names the series Passions."],
         [8, 36], "choice_neg", "choice_neg.untrue"))

# ---------------------------------------------------------------- P13 wiki noticeboards: P = Sources board
BOARD = {"COI board": "an editor writing about themselves, their employer or their clients, or asking for a review "
                      "of such edits.",
         "Sources board": "whether a given website, book or study can be cited.",
         "Technical board": "bugs, broken templates, scripts and other technical faults.",
         "Fringe board": "articles that push or describe fringe ideas."}
WB13 = [f"- {k}: {v}" for k, v in BOARD.items()] + ["- rule: exactly one listed board is the best place for each post."]
ELSE13 = "- elsewhere: any listed board other than the Sources board."
BOARD_INS = ("The listed boards are the COI, Sources, Technical and Fringe boards; the Sources board handles questions "
             "about whether a given website, book or study can be cited, and exactly one listed board is the best "
             "place for a post.")
_sa, _ta = raw_text("885f2eb6f02a79d8", "Reliable sources noticeboard")
_sb, _tb = raw_text("107ad93003a5dbe7", "Conflict of interest noticeboard")
PAIR(13, "card", "gd_wiki_help_routing",
     dict(orig=["885f2eb6f02a79d8"], state=_ta,
          atoms=dict(src=True, coi=False, asks_cite=True, sikhiwiki=True, historian=True, discussion=True)),
     dict(orig=["107ad93003a5dbe7"], state=_tb,
          atoms=dict(src=False, coi=True, asks_cite=False, template=False, fringe=False)), [
         YN("R0", "Is the Sources board the best listed place for this post?",
            Y(WB13 + [ELSE13], "the Sources board is the best listed place for this post."), "yn",
            lambda b: b.D(c("other than", LEX, CD, OFD), b.CA("src")), [1, 18], "route_q",
            "route_q.best_listed_place"),
         YN("N1", "Ignore irregular spacing. Is it false that this post asks whether a website can be cited as a "
                  "source?", None, "ny",
            lambda b: b.D(IRREG, b.N(c("false", TF, OF, SS), b.CA("asks_cite"))), [3, 16], "truth_q",
            "truth_q.false_that"),
         YN("N2", "Whether or not the poster gives a link, does the post fail to fit the label 'elsewhere'?",
            Y(WB13 + [ELSE13], "whether or not the poster gives a link, the post fails to fit the label 'elsewhere'."),
            "yn",
            lambda b: b.D(WON(), b.N(c("fail", LEX, IC, SC), b.N(c("other than", LEX, CD, OFD), b.CA("src")))),
            [7, 11, 12, 15, 16, 22], "side_clause", "side_clause.whether_or_not"),
         YN("N3", "A helper wrote: 'This post is unsuited to the Sources board.' Take the denial of the helper's "
                  "note. Does the post give grounds to dismiss that denial?",
            Y(WB13 + [NOTE_P], "the post gives grounds to dismiss the denial of the helper's note 'this post is "
                               "unsuited to the Sources board'."), "ny",
            lambda b: b.N(c("dismiss", LEX, OF, NS), b.N(c("denial", CS, SSP, NS), b.N(
                c("un-", AFF, IC, SC, "unsuited"), b.CA("src")))), [8, 10, 12], "reverse_claim",
            "reverse_claim.dismiss_denial"),
     ],
     CHR("Disregard the poster's sign-off. " + BOARD_INS + " Which statement about this post is untrue?", None,
         "The best listed place for it is not the Sources board but the COI board.",
         lambda b: (b.DI(DISREGARD), b.CH([b.CA("sikhiwiki"), b.AND(b.N(c("not ... but", SYN, CO, SC), b.CA("src")),
                                                                    b.A("coi")),
                                           b.CA("historian"), b.CA("discussion")], "false",
                                          c("untrue", TF, OF, SS)))[1],
         ["It asks about sikhiwiki.org.", "The best listed place for it is not the Sources board but the COI board.",
          "It mentions a historian.", "The poster wants to point an editor to a discussion."], [16, 32, 36],
         "choice_neg", "choice_neg.untrue"),
     CHR(BOARD_INS + " Which statement about this post is true?", None,
         "The best listed place for it is not the Sources board but the COI board.",
         lambda b: b.CH([b.CA("asks_cite"), b.AND(b.N(c("not ... but", SYN, CO, SC), b.CA("src")), b.A("coi")),
                         b.CA("template"), b.CA("fringe")], "true"),
         ["It asks whether a website can be cited.",
          "The best listed place for it is not the Sources board but the COI board.", "It reports a broken template.",
          "It names a fringe theory."], [32], "choice_true", "choice_true.which_statement"))

# ================================================================================================ multi-text ladders
MT = ["- toxic: a comment that insults, mocks, curses at or threatens a person or a group, for example by calling "
      "people names.",
      "- non-toxic: a comment that does none of the things in the 'toxic' line.",
      "- logic: words such as 'all', 'only', 'none' and number words are read literally; 'not all' means at least "
      "one is not."]
TOX_INS = "Here 'toxic' means a comment insults, mocks, curses at or threatens someone."


def batch(gids_golds):
    parts, srcs = [], []
    for i, (g, gold) in enumerate(gids_golds, 1):
        s, t = tox_text(g, gold)
        srcs.append(s)
        parts.append(f"Comment {i}:\n{t}")
    return "\n\n".join(parts), "+".join(sorted(set(srcs)))


def T(b, k):
    return [b.A(f"t{i}") for i in range(1, k + 1)]


# ---------------------------------------------------------------- P14 four comments: P = at least one toxic
_A14 = [("g:civil:258", "not toxic"), ("g:toxconv:251", "not toxic"), ("g:civil:114", "toxic"),
        ("g:civil:208", "not toxic")]
_B14 = [("g:civil:243", "not toxic"), ("g:toxconv:202", "not toxic"), ("g:civil:302", "not toxic"),
        ("g:toxconv:276", "not toxic")]
_ta, _sa = batch(_A14)
_tb, _sb = batch(_B14)
assert _sa == _sb
PAIR(14, "multitext", _sa,
     dict(orig=[g for g, _ in _A14], state=_ta, atoms=dict(t1=False, t2=False, t3=True, t4=False)),
     dict(orig=[g for g, _ in _B14], state=_tb,
          atoms=dict(t1=False, t2=False, t3=False, t4=False, alaskans=True, uber=True, fuel=True)), [
         YN("R0", "Answer yes if at least one of the four comments is toxic, and no otherwise.", DEFS(MT), "yn",
            lambda b: b.C(b.OR(*T(b, 4))), [1], "answer_map", "answer_map.yes_if_otherwise_no"),
         YN("N1", "Claim: at least one of the four comments is toxic. Give the answer that the key in the card assigns "
                  "to this claim.",
            "\n".join(MT + inv_key("batch")), "ny",
            lambda b: b.N(c("fails", AM, YK, OFD), b.C(b.OR(*T(b, 4)))), [12, 14], "key_card",
            "key_card.inverted_key"),
         YN("N2", "Even if a comment looks unusual, is it false that the batch is made up only of non-toxic "
                  "comments?",
            Y(MT, "even if a comment looks unusual, it is false that the batch is made up only of non-toxic "
                  "comments."), "yn",
            lambda b: b.D(c("un-", AFF, OF, SS, "unusual"), b.N(c("false", TF, OF, SS), b.N(c("non-", AFF, CD, OFD, "non-toxic"),
                                                                  b.C(b.OR(*T(b, 4)))))),
            [6, 11, 12, 15, 16, 27], "truth_q", "truth_q.false_that"),
         YN("N3", "Overlook unclear symbols. Consider the opposite of the next claim. Claim: not a single comment is "
                  "toxic. Does the batch give grounds to dismiss that opposite?",
            Y(MT + [NOTE_B, NOTE_OPP], "overlooking unclear symbols, the batch gives grounds to dismiss the opposite of "
                                       "the claim 'not a single comment is toxic'."), "ny",
            lambda b: b.D(UNCLEAR, b.N(c("dismiss", LEX, OF, NS), b.N(c("opposite", CS, SSP, NS), b.N(
                c("not a single", SYN, IC, SC), b.C(b.OR(*T(b, 4))))))), [8, 12, 16, 26], "reverse_claim",
            "reverse_claim.dismiss_opposite", idv=VERSION_R3),
     ],
     CHR(TOX_INS + " Which statement about the four comments is true?", None,
         "Apart from Comment 3, no comment is toxic.",
         lambda b: b.CH([b.C(b.AND(*T(b, 4))), b.N(c("none", SYN, CO, SC), b.C(b.OR(*T(b, 4)))),
                         b.N(c("no", SYN, CO, SC), b.C(b.OR(b.A("t1"), b.A("t2"), b.A("t4")))), b.CA("t1")], "true"),
         ["Every comment is toxic.", "None of the comments is toxic.", "Apart from Comment 3, no comment is toxic.",
          "Comment 1 is toxic."], [26, 31], "choice_true", "choice_true.which_statement"),
     CHR("Here 'non-toxic' means a comment insults, mocks, curses at and threatens no one. Which statement about the "
         "four comments is false?", None, "It is untrue that every comment is non-toxic.",
         lambda b: b.CH([b.CA("alaskans"), b.CA("uber"),
                         b.N(c("untrue", TF, CO, SC), b.N(c("non-", AFF, CO, SC, "non-toxic"), b.C(b.OR(*T(b, 4))))),
                         b.CA("fuel")], "false", c("false", TF, OF, SS)),
         ["Comment 2 mentions Alaskans.", "Comment 3 mentions über.", "It is untrue that every comment is non-toxic.",
          "Comment 4 mentions fuel cells."], [8, 26, 27, 36], "choice_neg", "choice_neg.false"))

# ---------------------------------------------------------------- P15 five comments: P = at least three toxic
MT2 = MT + ["- few: at most one."]
_A15 = [("g:toxconv:13", "toxic"), ("g:civil:298", "not toxic"), ("g:civil:163", "toxic"),
        ("g:toxconv:285", "not toxic"), ("g:civil:119", "toxic")]
_B15 = [("g:toxconv:128", "toxic"), ("g:toxconv:257", "not toxic"), ("g:civil:91", "toxic"),
        ("g:civil:259", "not toxic"), ("g:toxconv:312", "not toxic")]
_ta, _sa = batch(_A15)
_tb, _sb = batch(_B15)
assert _sa == _sb
PAIR(15, "multitext", _sa,
     dict(orig=[g for g, _ in _A15], state=_ta, atoms=dict(t1=True, t2=False, t3=True, t4=False, t5=True)),
     dict(orig=[g for g, _ in _B15], state=_tb, atoms=dict(t1=True, t2=False, t3=True, t4=False, t5=False)), [
         YN("R0", "Are at least three of the five comments toxic?",
            Y(MT2, "at least three of the five comments are toxic."), "yn",
            lambda b: b.C(b.ATLEAST(3, *T(b, 5))), [1], "quant", "quant.at_least_k"),
         YN("N2", "Even if some comments are unedited, is it false that no more than two of the five comments are "
                  "toxic?",
            Y(MT2, "even if some comments are unedited, it is false that no more than two of the five comments are "
                   "toxic."), "yn",
            lambda b: b.D(c("un-", AFF, OF, SS, "unedited"), b.N(c("false", TF, OF, SS), b.N(c("no more than", SYN, IC, SC),
                                                                  b.C(b.ATLEAST(3, *T(b, 5)))))),
            [6, 15, 16, 28], "side_clause", "side_clause.whether_or_not"),
         YN("N2", "Answer no if no more than two of the five comments are toxic; otherwise answer yes.", DEFS(MT2), "yn",
            lambda b: b.N(c("answer no if", AM, AMP, SS), b.N(c("no more than", SYN, IC, SC),
                                                               b.C(b.ATLEAST(3, *T(b, 5))))),
            [6, 13, 28], "answer_map", "answer_map.no_if_otherwise_yes"),
         YN("N3", "Consider the reverse of the claim at the end. The batch has five comments. Claim: the number of "
                  "toxic comments is not fewer than three. Is that reverse borne out by the comments?",
            Y(MT2 + [NOTE_B, "- note: links are irrelevant here."],
              "the reverse of the claim 'the number of toxic comments is not fewer than three' is borne out by the "
              "comments."), "ny",
            lambda b: b.D(c("ir-", AFF, CD, OFD, "irrelevant"), b.N(c("reverse", CS, SSP, FAR), b.N(c("not", SYN, IC, SC), b.N(
                c("fewer than", LEX, IC, SC), b.C(b.ATLEAST(3, *T(b, 5))))))),
            [8, 12, 16, 18, 28], "reverse_claim", "reverse_claim.consider_reverse"),
     ],
     CHR("Disregard links. " + TOX_INS[:-1] + ", and 'few' means at most one. Which statement about the five comments "
         "is true?", None, "It is untrue that every comment is free of insults.",
         lambda b: (b.DI(DISREGARD), b.CH([b.C(b.EXACTLY(2, *T(b, 5))), b.C(b.ATMOST(1, *T(b, 5))),
                                           b.N(c("untrue", TF, CO, SC), b.N(c("free of", LEX, CO, SC),
                                                                            b.C(b.OR(*T(b, 5))))),
                                           b.C(b.AND(*T(b, 5)))], "true"))[1],
         ["Exactly two of the comments are toxic.", "Few of the comments are toxic.",
          "It is untrue that every comment is free of insults.", "Every comment is toxic."], [16, 26, 29],
         "choice_true", "choice_true.which_statement"),
     CHR(TOX_INS + " Which statement about the five comments is true?", None,
         "It is untrue that no more than one comment is toxic.",
         lambda b: b.CH([b.CA("t2"), b.C(b.ATLEAST(3, *T(b, 5))),
                         b.N(c("untrue", TF, CO, SC), b.N(c("no more than", SYN, CO, SC), b.C(b.ATLEAST(2, *T(b, 5))))),
                         b.C(b.ATMOST(1, *T(b, 5)))], "true"),
         ["Comment 2 is toxic.", "At least three of the comments are toxic.",
          "It is untrue that no more than one comment is toxic.", "At most one comment is toxic."], [28],
         "choice_true", "choice_true.which_statement"))

# ---------------------------------------------------------------- P16 two reports: P = both describe someone hurt
H16 = ["- hurt: a person was physically injured, however slightly."]
_s1, _t1 = raw_text("spdb-20240802-A7C36-2147337542", "no incident, no injury")
_s2, _t2 = raw_text("spdb-20200722-625C6-2147370926", "injury, no first aid or medical care")
_s3, _t3 = raw_text("spdb-20120626-924E0-2147466260", "injury, no first aid or medical care")
_s4, _t4 = raw_text("spdb-20200905-27128-2147369992", "injury, no first aid or medical care")
PAIR(16, "multitext", "gd_saferproducts_severity",
     dict(orig=["spdb-20240802-A7C36-2147337542", "spdb-20200722-625C6-2147370926"],
          state=f"Report 1:\n{_t1}\n\nReport 2:\n{_t2}",
          atoms=dict(h1=False, h2=True, cart=True, rash=True, sports=True)),
     dict(orig=["spdb-20120626-924E0-2147466260", "spdb-20200905-27128-2147369992"],
          state=f"Report 1:\n{_t3}\n\nReport 2:\n{_t4}",
          atoms=dict(h1=True, h2=True, upright=False, doctor=False, store=False)), [
         YN("R0", "Do both reports describe someone getting hurt?",
            Y(H16, "both reports describe someone getting hurt."), "ny",
            lambda b: b.C(b.AND(b.A("h1"), b.A("h2"))), [1], "quant", "quant.both"),
         YN("N1", "Ignore irregular spacing. Is it true that not both reports describe someone getting hurt?", None,
            "yn",
            lambda b: b.D(IRREG, b.N(c("not both", SYN, IC, SC), b.C(b.AND(b.A("h1"), b.A("h2"))))),
            [2, 16, 30], "truth_q", "truth_q.true_that"),
         YN("N2", "Is it false that not both reports describe someone getting hurt?", None, "ny",
            lambda b: b.N(c("false", TF, OF, SS), b.N(c("not both", SYN, IC, SC), b.C(b.AND(b.A("h1"), b.A("h2"))))),
            [6, 30], "truth_q", "truth_q.false_that"),
         YN("N3", "Whether or not either report names a store, is it unjustified to say that the reports do not show "
                  "that not both of them describe someone getting hurt?",
            Y(H16 + [NOTE_RS], "whether or not either report names a store, it is unjustified to say that the reports "
                               "do not show that not both of them describe someone getting hurt."), "yn",
            lambda b: b.D(WON(), b.N(c("unjustified", TF, OF, SS), b.N(c("not", SYN, IC, SC, "do not"), b.N(
                c("not both", SYN, IC, SC), b.C(b.AND(b.A("h1"), b.A("h2"))))))), [8, 10, 15, 16, 30], "attributed",
            "attributed.unjustified_to_say"),
     ],
     CHR("Which statement about the two reports does not hold?", None,
         "Neither report describes someone getting hurt.",
         lambda b: b.CH([b.CA("cart"), b.CA("rash"), b.N(c("neither", SYN, CO, SC), b.C(b.OR(b.A("h1"), b.A("h2")))),
                         b.CA("sports")], "false", c("not", SYN, OF, SS, "does not")),
         ["Report 1 describes a golf cart stopping suddenly.", "Report 2 describes a rash on the writer's neck.",
          "Neither report describes someone getting hurt.", "Report 2 mentions playing sports."], [30, 36],
         "choice_neg", "choice_neg.does_not_hold"),
     CHR("Here 'hurt' means a person was physically injured, however slightly. Which statement about the two reports "
         "is true?", None, "It is untrue that neither report describes someone getting hurt.",
         lambda b: b.CH([b.CA("upright"), b.CA("doctor"),
                         b.N(c("untrue", TF, CO, SC), b.N(c("neither", SYN, CO, SC),
                                                          b.C(b.OR(b.A("h1"), b.A("h2"))))),
                         b.CA("store")], "true"),
         ["Report 1 describes a toy that stayed upright.", "Report 2 says a doctor treated the writer's hand.",
          "It is untrue that neither report describes someone getting hurt.",
          "Report 1 names the store that sold the rocker."], [30], "choice_true", "choice_true.which_statement"))

# ---------------------------------------------------------------- P17 three wiki posts: P = some post at Language
WD17 = desk_lines(["Language desk", "Science desk", "Mathematics desk", "Humanities desk"]) + \
    ["- rule: each post belongs at exactly one listed desk."]
DESK17_INS = ("Each post belongs at exactly one of these desks: Language (words and grammar), Science (nature and the "
              "body), Mathematics (numbers and proofs) and Humanities (history and society).")
_ra = [("0e83a9ff2818a56d", "Science reference desk"), ("5d3a5cbe7291ffad", "Language reference desk"),
       ("f6b4794fcfb7a864", "Mathematics reference desk")]
_rb = [("bde2e01bfaca4fe2", "Science reference desk"), ("f215a5dfdff36ad5", "Humanities reference desk"),
       ("32dfdbe06dcce327", "Mathematics reference desk")]
_ta = "\n\n".join(f"Post {i}:\n{raw_text(r, g)[1]}" for i, (r, g) in enumerate(_ra, 1))
_tb = "\n\n".join(f"Post {i}:\n{raw_text(r, g)[1]}" for i, (r, g) in enumerate(_rb, 1))
# Round 3 (arbiter A3): row N1 excepts Post 3, so Post 3 must have the asked property (Language or Mathematics desk)
# in BOTH twins, by its human label
assert _ra[2][1] == _rb[2][1] == "Mathematics reference desk"
PAIR(17, "multitext", "gd_wiki_help_routing",
     dict(orig=[r for r, _ in _ra], state=_ta,
          atoms=dict(l1=False, l2=True, l3=False, m1=False, m2=False, m3=True, h1=False)),
     dict(orig=[r for r, _ in _rb], state=_tb,
          atoms=dict(l1=False, l2=False, l3=False, m1=False, m2=False, s1=True, s2=False, s3=False, colorblind=True,
                     calendar=True, formula=True)), [
         YN("R0", "Does at least one of the three posts belong at the Language desk?",
            Y(WD17, "at least one of the three posts belongs at the Language desk."), "yn",
            lambda b: b.C(b.OR(b.A("l1"), b.A("l2"), b.A("l3"))), [1], "quant", "quant.at_least_one"),
         # Round 3 (arbiter A3): 'no post apart from Post 3 ...' also says that Post 3 has the property (inclusion).
         # The property is now one that Post 3 (a Mathematics post) has in both twins, so the literal and the
         # exceptive readings agree on both states; the twins still differ only through Post 2.
         YN("N1", "Is it true that no post apart from Post 3 belongs at either of the Language and Mathematics "
                  "desks?",
            Y(WD17, "it is true that no post apart from Post 3 belongs at either of the Language and Mathematics "
                    "desks."), "ny",
            lambda b: b.N(c("no", SYN, IC, SC), b.C(b.OR(b.A("l1"), b.A("m1"), b.A("l2"), b.A("m2")))), [2, 31],
            "truth_q", "truth_q.true_that", idv=VERSION_R3),
         YN("N2", "Answer no if no post here belongs at the Language desk; otherwise answer yes.", DEFS(WD17), "yn",
            lambda b: b.N(c("answer no if", AM, AMP, SS), b.N(c("no", SYN, IC, SC),
                                                               b.C(b.OR(b.A("l1"), b.A("l2"), b.A("l3"))))),
            [6, 13, 26], "answer_map", "answer_map.no_if_otherwise_yes"),
         YN("N3", "Disregard the post headings. A sorting note says no post here belongs at the Language desk. Going by "
                  "the posts, is it unfounded to dispute that note?",
            Y(WD17 + [NOTE_PS], "disregarding the post headings, going by the posts, it is unfounded to dispute the "
                                "sorting note saying that no post here belongs at the Language desk.", "Y"), "ny",
            lambda b: b.D(DISREGARD, b.N(c("unfounded", TF, OF, NS), b.N(c("dispute", LEX, OF, NS), b.N(
                c("no", SYN, IC, SC), b.C(b.OR(b.A("l1"), b.A("l2"), b.A("l3")))))))
            , [8, 10, 12, 16, 26], "attributed", "attributed.unfounded_to_dispute"),
     ],
     CHR("Overlook unclear symbols. " + DESK17_INS + " Which statement about the three posts is true?", None,
         "Besides Post 3, no post belongs at the Mathematics desk.",
         lambda b: (b.DI(UNCLEAR), b.CH([b.C(b.AND(b.A("m1"), b.A("m2"), b.A("m3"))), b.CA("h1"),
                                         b.N(c("no", SYN, CO, SC), b.C(b.OR(b.A("m1"), b.A("m2")))),
                                         b.N(c("not", SYN, CO, SC, "does not"), b.CA("l2"))], "true"))[1],
         ["Every post belongs at the Mathematics desk.", "Post 1 belongs at the Humanities desk.",
          "Besides Post 3, no post belongs at the Mathematics desk.", "Post 2 does not belong at the Language desk."],
         [16, 31], "choice_true", "choice_true.which_statement"),
     CHR(DESK17_INS + " Which statement about the three posts fails to hold?", None,
         "No post belongs at the Science desk.",
         lambda b: b.CH([b.CA("colorblind"), b.CA("calendar"), b.N(c("no", SYN, CO, SC), b.C(b.OR(
             b.A("s1"), b.A("s2"), b.A("s3")))), b.CA("formula")], "false", c("fail", LEX, OF, SS, "fails")),
         ["Post 1 asks how scientists know that some animals are color-blind.",
          "Post 2 asks when the Hebrew calendar was created.", "No post belongs at the Science desk.",
          "Post 3 asks about a formula."], [26, 36], "choice_neg",
         "choice_neg.fails_to_hold"))

# ================================================================================================ invented records
# ---------------------------------------------------------------- P18 email thread: P = customer asks for a refund
EMAIL = """From: Beira Bainton <beira.bainton@mailbox.example>
To: help@kettleworks.example
Subject: Order KW-48213
Date: 14 Mar 2026 09:12

Hello, the travel kettle from order KW-48213 arrived on Tuesday with a cracked lid. {ask}

From: help@kettleworks.example
To: Beira Bainton <beira.bainton@mailbox.example>
Date: 14 Mar 2026 11:40

Thanks for writing. Could you send us a photo of the lid?"""
REQ = {"other request": "the customer asks for something other than her money back.",
       "billing": "the 'other request' line leaves the thread out.",
       "praise": "the customer thanks the shop for a good order.",
       "complaint": "the customer reports a problem with an order."}
PAIR(18, "record", "f7x_record",
     dict(orig=["invented:email_kettle_refund"],
          state=EMAIL.format(ask="Please send my money back to the card I paid with."),
          atoms=dict(refund=True, praise=False)),
     dict(orig=["invented:email_kettle_replace"], state=EMAIL.format(ask="Please send me a new kettle in its place."),
          atoms=dict(refund=False, complaint=True)), [
         YN("R0", "Answer yes if the customer asks for a refund in this thread, and no otherwise.", DEFS([NOTE_T]),
            "yn", lambda b: b.CA("refund"), [1], "answer_map", "answer_map.yes_if_otherwise_no"),
         YN("N1", "A ticket summary reads: 'Customer asks for a refund.' Does the thread give grounds to dispute that "
                  "summary?",
            Y([NOTE_T], "the thread gives grounds to dispute the ticket summary 'Customer asks for a refund'."), "ny",
            lambda b: b.N(c("dispute", LEX, OF, NS), b.CA("refund")), [4, 12], "verb_eval",
            "verb_eval.grounds_to_dispute"),
         YN("N2", "Answer no if the customer doesn't ask for a refund; otherwise answer yes.", DEFS([NOTE_T]), "yn",
            lambda b: b.N(c("answer no if", AM, AMP, SS), b.N(c("n't", SYN, IC, SC, "doesn't"), b.CA("refund"))),
            [6, 13], "answer_map", "answer_map.no_if_otherwise_yes"),
         YN("N3", "Do not explain your answer. Is it false that the thread is not free of a refund request?", None,
            "ny",
            lambda b: b.D(DONOT, b.N(c("false", TF, OF, SS), b.N(c("not", SYN, IC, SC), b.N(
                c("free of", LEX, IC, SC), b.CA("refund"))))), [8, 16], "truth_q", "truth_q.false_that"),
     ],
     CHR("Which label fits this thread?", {k: REQ[k] for k in ("other request", "billing", "praise")}, "billing",
         lambda b: b.CH([b.N(c("other than", LEX, CD, OFD), b.CA("refund")),
                         b.N(c("leave out", LEX, CD, OFD, "leaves ... out"), b.N(c("other than", LEX, CD, OFD),
                                                                                  b.CA("refund"))),
                         b.CA("praise")], "true"),
         ["other request", "billing", "praise"], [], "choice_pick", "choice_pick.label_fits"),
     CHR("Which label does this thread fail to match?", {k: REQ[k] for k in ("other request", "billing", "complaint")},
         "billing",
         lambda b: b.CH([b.N(c("other than", LEX, CD, OFD), b.CA("refund")),
                         b.N(c("leave out", LEX, CD, OFD, "leaves ... out"), b.N(c("other than", LEX, CD, OFD),
                                                                                  b.CA("refund"))),
                         b.CA("complaint")], "false", c("fail", LEX, OF, SS)),
         ["other request", "billing", "complaint"], [36], "choice_neg", "choice_neg.label_fail_to_match"))

# ---------------------------------------------------------------- P19 key: value ticket + rules (items 33, 34, 35)
TICKET = """Ticket: 55-2190
Channel: chat
Customer: Beilin Barford
Message: Hi, my parcel arrived crushed {msg}
Triage note: {note}"""
RULES19 = ["- rule 1: an agent must not issue a refund unless the customer has asked for one.",
           "- rule 2: a ticket must be escalated exactly when it asks for a refund."]
RULES19_INS = ("Rule 1: an agent must not issue a refund unless the customer has asked for one. Rule 2: a ticket must "
               "be escalated exactly when it asks for a refund.")
PAIR(19, "record", "f7x_record",
     dict(orig=["invented:ticket_lamp_refund"],
          state=TICKET.format(msg="and the lamp inside is broken. I would like my money back, please.",
                              note="topic = refund request; photo attached = no"),
          atoms=dict(refund=True, note_refund=True, chat=True, lamp_broken=True, number=True)),
     dict(orig=["invented:ticket_lamp_courier"],
          state=TICKET.format(msg="but the lamp inside works. Could you pass this on to the courier?",
                              note="topic = packaging; refund wanted = no"),
          atoms=dict(refund=False, note_refund=False, lamp_broken=False)), [
         YN("R0", "Does the customer ask for a refund in this ticket?",
            Y([NOTE_TK], "the customer asks for a refund in this ticket."), "yn",
            lambda b: b.CA("refund"), [1], "direct_q", "direct_q.in_this_record"),
         YN("N2", "Under rule 1, is the agent allowed to issue a refund on this ticket?",
            Y(RULES19 + ["- note: the channel does not affect any rule."],
              "under rule 1, the agent is allowed to issue a refund on this ticket."), "yn",
            lambda b: b.D(CDN("not", "does not"), b.N(c("must not", SYN, CD, OFD), b.N(c("unless", SYN, CD, OFD),
                                                                             b.CA("refund")))),
            [12, 16, 18, 20, 33, 34], "policy_modal", "policy_modal.allowed_under_rule", looks=[UNDER]),
         YN("N2", "A note says this ticket need not be escalated under rule 2. Does the ticket refute that note?",
            Y(RULES19 + [NOTE_TK], "the ticket refutes the note saying that this ticket need not be escalated under "
                                   "rule 2."), "yn",
            lambda b: b.N(c("refute", LEX, OF, NS), b.N(c("need not", SYN, IC, SC), b.CA("refund"))),
            [6, 10, 12, 33], "verb_eval", "verb_eval.refute_note"),
         YN("N1", "Does the triage note make no claim that the customer is asking for a refund?",
            Y(["- reading: a note claims only what it states outright."],
              "the triage note makes no claim that the customer is asking for a refund."), "ny",
            lambda b: b.N(c("no", SYN, IC, SC), b.CA("note_refund")), [35], "direct_q", "direct_q.note_makes_no_claim",
            note="core = what the triage note claims (non-factive), not what the customer asks"),
     ],
     CHR(RULES19_INS + " Which statement about this ticket is untrue?", None, "Rule 1 forbids a refund on this ticket.",
         lambda b: b.CH([b.CA("chat"), b.CA("lamp_broken"), b.N(c("unless", SYN, SSP, FAR), b.CA("refund")),
                         b.CA("number")], "false", c("untrue", TF, OF, SS)),
         ["The ticket came in by chat.", "The lamp inside the parcel is broken.",
          "Rule 1 forbids a refund on this ticket.", "The ticket number is 55-2190."], [34, 36], "choice_neg",
         "choice_neg.untrue"),
     CHR(RULES19_INS + " Which statement about this ticket is true?", None,
         "It is untrue that rule 1 allows a refund on this ticket.",
         lambda b: b.CH([b.CA("refund"),
                         b.N(c("untrue", TF, CO, SC), b.N(c("must not", SYN, SSP, FAR), b.N(
                             c("unless", SYN, SSP, FAR), b.CA("refund")))),
                         b.CA("refund"), b.CA("lamp_broken")], "true"),
         ["Rule 2 requires this ticket to be escalated.", "It is untrue that rule 1 allows a refund on this ticket.",
          "The customer asks for a refund.", "The lamp inside the parcel is broken."], [8, 33, 34], "choice_true",
         "choice_true.which_statement"))

# ---------------------------------------------------------------- P20 JSON expense claim: P = receipt attached
def _claim(receipt):
    return json.dumps({"claim_id": "EXP-30771", "employee": "Bolan Barmere", "date": "2026-02-19",
                       "category": "uniform cleaning", "amount_eur": 42.5, "receipt": receipt,
                       "approver_note": "Policy 4.2: payment once a receipt is attached."}, indent=1,
                      ensure_ascii=False)


DOCL = {"documented": "a receipt file is attached to the claim.",
        "undocumented": "no receipt file is attached to the claim.",
        "payable": "the claim fails to fit the 'undocumented' line.",
        "expense": "the record is an expense claim."}
DOC = [f"- {k}: {DOCL[k]}" for k in ("documented", "undocumented")]
PAIR(20, "record", "f7x_record",
     dict(orig=["invented:expense_json_receipt"], state=_claim("scan_0412.pdf"), atoms=dict(receipt=True,
                                                                                         expense=True)),
     dict(orig=["invented:expense_json_none"], state=_claim(None), atoms=dict(receipt=False, expense=True)), [
         YN("R0", "Is it true that a receipt is attached to this claim?", None, "yn",
            lambda b: b.CA("receipt"), [1], "truth_q", "truth_q.true_that"),
         YN("N1", "Disregard the claim's date. Answer no if the label 'documented' fits this claim; otherwise answer "
                  "yes.", DEFS(DOC), "ny",
            lambda b: b.D(DISREGARD, b.N(c("answer no if", AM, AMP, SS), b.CA("receipt"))), [13, 16], "answer_map",
            "answer_map.no_if_otherwise_yes"),
         YN("N2", "Under the card's definitions, and even if the amount looks unusual, does the label 'undocumented' "
                  "fail to fit this claim?",
            Y(DOC, "under the card's definitions, and even if the amount looks unusual, the label 'undocumented' "
                   "fails to fit this claim."), "yn",
            lambda b: b.D(c("un-", AFF, OF, SS, "unusual"), b.N(c("fail", LEX, IC, SC), b.N(c("un-", AFF, CD, OFD,
                                                                                      "undocumented"),
                                                                  b.CA("receipt")))),
            [11, 12, 15, 16, 20], "label_fit", "label_fit.fail_to_fit", looks=[UNDER]),
         YN("N3", "Take the reverse of the following label claim. Claim: 'undocumented' fits this expense claim. Does "
                  "the record fail to bear out that reverse?",
            Y(DOC + [NOTE_REC], "the record fails to bear out the reverse of the label claim \"'undocumented' fits "
                                "this expense claim\"."), "ny",
            lambda b: b.N(c("fail", LEX, OF, NS), b.N(c("reverse", CS, SSP, NS), b.N(
                c("un-", AFF, CD, OFD, "undocumented"), b.CA("receipt")))), [8, 12], "reverse_claim",
            "reverse_claim.take_reverse"),
     ],
     CHR("Which label is unsuitable for this claim?", {k: DOCL[k] for k in ("documented", "undocumented", "expense")},
         "undocumented",
         lambda b: b.CH([b.CA("receipt"), b.N(c("un-", AFF, CD, OFD, "undocumented"), b.CA("receipt")),
                         b.CA("expense")], "false", c("un-", AFF, OF, SS, "unsuitable")),
         ["documented", "undocumented", "expense"], [36], "choice_neg", "choice_neg.label_fail_to_match"),
     CHR("Which label does this claim fail to match?", {k: DOCL[k] for k in ("undocumented", "payable", "expense")},
         "payable",
         lambda b: b.CH([b.N(c("un-", AFF, CD, OFD, "undocumented"), b.CA("receipt")),
                         b.N(c("fail", LEX, CD, OFD, "fails"), b.N(c("un-", AFF, CD, OFD, "undocumented"),
                                                                    b.CA("receipt"))),
                         b.CA("expense")], "false", c("fail", LEX, OF, SS)),
         ["undocumented", "payable", "expense"], [8, 36], "choice_neg", "choice_neg.label_fail_to_match"))

# ---------------------------------------------------------------- P21 parcel log: P = delivered (AR, depth 4)
LOG = """2026-05-03 08:14  label printed for parcel PX-7781
2026-05-03 17:02  parcel scanned at Hollins depot
2026-05-04 06:55  out for delivery
2026-05-04 13:31  {event}
2026-05-04 13:40  note: customer had asked for a call before delivery"""
STAT = ["- status: each parcel has exactly one status, 'delivered' or 'with the carrier'."]
PARL = {"undelivered": "the parcel has not reached the customer.",
        "closed": "the 'undelivered' line excludes the parcel.",
        "lost": "the carrier reports the parcel missing.", "scanned": "the parcel was scanned at a depot."}
PAIR(21, "record", "f7x_record",
     dict(orig=["invented:parcel_log_delivered"], state=LOG.format(event="delivered; signed by R. Binley"),
          atoms=dict(delivered=True, signed=True, with_carrier=False, label5=False, text_msg=False)),
     dict(orig=["invented:parcel_log_returned"],
          state=LOG.format(event="delivery attempt failed; parcel taken back to Hollins depot"),
          atoms=dict(delivered=False, scanned=True)), [
         YN("R0", "According to the log, was parcel PX-7781 delivered?",
            Y(["- note: the log's times are irrelevant here."], "according to the log, parcel PX-7781 was delivered."),
            "yn", lambda b: b.D(c("ir-", AFF, CD, OFD, "irrelevant"), b.CA("delivered")), [1, 18], "direct_q",
            "direct_q.according_to"),
         YN("AR", "According to the log, is the status of parcel PX-7781 'with the carrier'?",
            Y(STAT, "according to the log, the status of parcel PX-7781 is 'with the carrier'."), "ny",
            lambda b: b.NN(b.CA("delivered")), [], "direct_q", "direct_q.status_is"),
         YN("N1", "Read the claim at the end, then answer about its denial. The log covers two days. Claim: parcel "
                  "PX-7781 was delivered. Is that denial borne out by the log?",
            Y([NOTE_L], "the denial of the claim 'parcel PX-7781 was delivered' is borne out by the log."), "ny",
            lambda b: b.N(c("denial", CS, SSP, FAR), b.CA("delivered")), [12], "reverse_claim",
            "reverse_claim.denial_far"),
         YN("N4", "Disregard the timestamps. Take the opposite of the note below. Note: 'Parcel PX-7781 was never "
                  "delivered.' Is it untrue that the log fails to bear out that opposite?",
            Y([NOTE_L], "disregarding the timestamps, it is untrue that the log fails to bear out the opposite of the "
                        "note 'Parcel PX-7781 was never delivered'."), "yn",
            lambda b: b.D(DISREGARD, b.N(c("untrue", TF, OF, SS), b.N(c("fail", LEX, OF, SS, "fails"), b.N(
                c("opposite", CS, SSP, NS), b.N(c("never", SYN, IC, SC), b.CA("delivered")))))), [9, 10, 12, 16],
            "attributed", "attributed.untrue_fails_opposite"),
     ],
     CHR("Which statement about the log is true?", None, "It is false that nobody signed for the parcel.",
         lambda b: b.CH([b.CA("with_carrier"), b.N(c("false", TF, CO, SC), b.N(c("nobody", SYN, CO, SC),
                                                                              b.CA("signed"))),
                         b.CA("label5"), b.CA("text_msg")], "true"),
         ["The parcel is still with the carrier.", "It is false that nobody signed for the parcel.",
          "A label was printed on 5 May.", "The customer asked for a text message."], [], "choice_true",
         "choice_true.which_statement"),
     CHR("Which label is inapplicable to parcel PX-7781?",
         {k: PARL[k] for k in ("undelivered", "closed", "scanned")}, "closed",
         lambda b: b.CH([b.N(c("un-", AFF, CD, OFD, "undelivered"), b.CA("delivered")),
                         b.N(c("exclude", LEX, CD, OFD, "excludes"), b.N(c("un-", AFF, CD, OFD, "undelivered"),
                                                                          b.CA("delivered"))),
                         b.CA("scanned")], "false", c("in-", AFF, OF, SS, "inapplicable")),
         ["undelivered", "closed", "scanned"], [8, 36], "choice_neg", "choice_neg.label_fail_to_match"))

# ---------------------------------------------------------------- P22 chat: P = manager approved (item 35)
CHAT = """[09:02] Bodetta Bansko: Hi, I need edit access to the Q3 budget sheet.
[09:05] IT bot: Request logged as ACC-6620. Waiting for manager approval.
[09:41] IT bot: Reminder sent to manager Bemis Belov.
[11:15] Bemis Belov: {mgr}
[11:16] IT bot: {bot}"""
REQL = {"unapproved": "the request is still waiting for the manager.",
        "cleared": "the request fails to fit the 'unapproved' line.",
        "refused": "the manager turned the request down.", "logged": "the request has a ticket number."}
PAIR(22, "record", "f7x_record",
     dict(orig=["invented:access_chat_approved"],
          state=CHAT.format(mgr="Approved, go ahead.", bot="Status changed: approved."),
          atoms=dict(approved=True, bot_claims_not=False, out=False, wrong_id=False, payroll=False)),
     dict(orig=["invented:access_chat_waiting"],
          state=CHAT.format(mgr="I'm out today, I'll look at it tomorrow.",
                            bot="Status unchanged: unapproved."),
          atoms=dict(approved=False, bot_claims_not=True, logged=True)), [
         YN("R0", "Has the manager approved Bodetta's access request in this chat?",
            Y([NOTE_CH], "the manager has approved Bodetta's access request in this chat."), "yn",
            lambda b: b.CA("approved"), [1], "direct_q", "direct_q.in_this_record"),
         YN("N1", "Treat the bot's first message as irrelevant. Is it false that the IT bot's 11:16 message claims "
                  "that the request is unapproved?",
            Y(["- reading: a message claims only what it states outright."],
              "treating the bot's first message as irrelevant, it is false that the IT bot's 11:16 message claims "
              "that the request is unapproved."), "yn",
            lambda b: b.D(c("ir-", AFF, SSP, NS, "irrelevant"), b.N(c("false", TF, OF, SS), b.CA("bot_claims_not"))), [3, 16, 35], "truth_q",
            "truth_q.false_that_claims", content=["un- (inside what the message is said to claim)"],
            note="core = what the bot's 11:16 message claims (non-factive); the 'un-' sits inside the claimed content"),
         YN("N2", "Ignore informal wording. Is it false that the access request in this chat is unapproved?", None,
            "yn",
            lambda b: b.D(INFORMAL, b.N(c("false", TF, OF, SS), b.N(c("un-", AFF, IC, SC, "unapproved"),
                                                                    b.CA("approved")))),
            [6, 16], "truth_q", "truth_q.false_that"),
         YN("N3", "Overlook the bot's unusual wording. Is it false that the chat doesn't show that the request is "
                  "unapproved?",
            Y([NOTE_CH], "overlooking the bot's unusual wording, it is false that the chat doesn't show that the "
                         "request is unapproved."), "ny",
            lambda b: b.D(UNUSUAL, b.N(c("false", TF, OF, SS), b.N(c("n't", SYN, IC, SC, "doesn't"), b.N(
                c("un-", AFF, IC, SC, "unapproved"), b.CA("approved"))))), [8, 16], "truth_q", "truth_q.false_that"),
     ],
     CHR("Which statement about the chat is true?", None, "It is false that the request is still unapproved.",
         lambda b: b.CH([b.CA("out"), b.N(c("false", TF, CO, SC), b.N(c("un-", AFF, CO, SC, "unapproved"),
                                                                      b.CA("approved"))),
                         b.CA("wrong_id"), b.CA("payroll")], "true"),
         ["The manager says he is out today.", "It is false that the request is still unapproved.",
          "The request was logged as ACC-6602.", "Bodetta asks for access to a payroll sheet."], [],
         "choice_true", "choice_true.which_statement"),
     CHR("Which label is unsuitable for the request?", {k: REQL[k] for k in ("unapproved", "cleared", "logged")},
         "cleared",
         lambda b: b.CH([b.N(c("un-", AFF, CD, OFD, "unapproved"), b.CA("approved")),
                         b.N(c("fail", LEX, CD, OFD, "fails"), b.N(c("un-", AFF, CD, OFD, "unapproved"),
                                                                    b.CA("approved"))),
                         b.CA("logged")], "false", c("un-", AFF, OF, SS, "unsuitable")),
         ["unapproved", "cleared", "logged"], [8, 36], "choice_neg", "choice_neg.label_fail_to_match"))


# ================================================================================================ assembly
STATE_NEG_RE = re.compile(r"\b(?:not|no|never|none|nothing|nobody|nowhere|neither|nor|without|cannot)\b|n't\b", re.I)


def card_style_of(card):
    if not card:
        return "none"
    lines = card.split("\n")
    if any(ln.startswith("- yes: ") for ln in lines):
        return "golden"
    if any(ln.startswith("- Yes: ") for ln in lines):
        return "Yes"
    return "defs"


def refs_of(n, acc=None):
    """{cue index: [node op, ...]} over the tree (NOT / DIST / CHOICE nodes)."""
    acc = collections.defaultdict(list) if acc is None else acc
    if isinstance(n.get("cue"), int):
        acc[n["cue"]].append(n["op"])
    for k in ([n["child"]] if "child" in n else []) + n.get("children", []) + n.get("options", []):
        refs_of(k, acc)
    return acc


def has_null_not(n):
    if n.get("op") == "NOT" and n.get("cue") is None:
        return True
    return any(has_null_not(k) for k in ([n["child"]] if "child" in n else []) + n.get("children", [])
               + n.get("options", []))


QUESTION_POS = (OF, IC, SSP, AMP, CO)


def gold_positions(metas):
    """Gold position of every choice row, stratified so that the position is unrelated to the option count, the
    negated selection, the depth and the cue count (5.k): within each option count k the rows are sorted by
    (selection, depth, cue count, id) and take positions 0, 1, ..., k-1 in turn."""
    pos = {}
    by_k = collections.defaultdict(list)
    for m in metas:
        if m["qtype"] == "choice":
            by_k[m["n_options"]].append(m)
    import itertools
    feats = (lambda m: m["select"] == "false", lambda m: m["depth"], lambda m: m["n_cues"], lambda m: m["n_options"])

    def corr(xs, ys):
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        vx, vy = sum((x - mx) ** 2 for x in xs), sum((y - my) ** 2 for y in ys)
        return 0.0 if not vx or not vy else sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (vx * vy) ** 0.5

    best = None
    keys = [("select", "depth", "n_cues"), ("depth", "select", "n_cues"), ("n_cues", "select", "depth"),
            ("select", "n_cues", "depth"), ("depth", "n_cues", "select"), ("n_cues", "depth", "select")]
    for key in keys:
        for offs in itertools.product(range(3), range(4), range(5)):
            cand = {}
            for k, ms in by_k.items():
                ms = sorted(ms, key=lambda m: tuple(m[x] for x in key) + (m["id"],))
                off = offs[k - 3]
                for i, m in enumerate(ms):
                    cand[m["id"]] = (i + off) % k
            allm = [m for ms in by_k.values() for m in ms]
            gp = [cand[m["id"]] / (m["n_options"] - 1) for m in allm]
            score = max(abs(corr([float(f(m)) for m in allm], gp)) for f in feats)
            if best is None or score < best[0] - 1e-12:
                best = (score, cand)
    return best[1]


def build(positions=None):
    rows, metas, rels, packet = [], [], [], []
    pos_ctr = collections.Counter()
    for P in PAIRS:
        tw_states = {k: v["state"] for k, v in P["twins"].items()}
        assert bool(STATE_NEG_RE.search(tw_states["a"])) == bool(STATE_NEG_RE.search(tw_states["b"])), P["n"]
        assert tw_states["a"] != tw_states["b"]
        for tw in ("a", "b"):
            T_ = P["twins"][tw]
            other = "b" if tw == "a" else "a"
            lid = f"{VERSION}_L{P['n']:02d}{tw}"
            gid = f"g:{VERSION}:{lid}"
            call = cid(gid)
            specs = P["rows"] + [P["ch"][tw]]
            built = []
            for k, spec in enumerate(specs):
                b = B(T_["atoms"])
                for lk in spec["looks"]:
                    b.look(lk)
                lf = spec["lf"](b)
                rid = f"r_{spec.get('idv') or VERSION}_{P['n']:02d}{tw}_{k}"
                if spec["kind"] == "ch":
                    assert lf["op"] == "CHOICE", rid
                    for o in lf["options"]:
                        assert len(core_paths(o)) == 1, (rid, "every option needs exactly one CORE")
                    hits = choice_hits(lf)
                    assert len(hits) == 1, (rid, hits)
                    gi = hits[0]
                    opts = list(spec["opts"])
                    assert len(opts) == len(lf["options"]) and opts[gi] == spec["gold"], (rid, opts[gi], spec["gold"])
                    opt = lf["options"][gi]
                    for ci in reversed(b.pending_dists):   # instruction-level distractors sit on the gold option
                        opt = {"op": "DIST", "cue": ci, "child": opt}
                    lf["options"][gi] = opt
                    kk = len(opts)
                    target = positions[rid] if positions else pos_ctr[kk] % kk
                    pos_ctr[kk] += 1
                    order = [i for i in range(kk) if i != gi]
                    order.insert(target, gi)
                    opts = [opts[i] for i in order]
                    lf = {**lf, "options": [lf["options"][i] for i in order]}
                    assert choice_hits(lf) == [target] and opts[target] == spec["gold"]
                    core, nots = core_paths(lf["options"][target])[0]
                    depth = nots + (1 if lf["select"] == "false" else 0)
                    truth_p = ev(core["child"])
                    assert truth_p == (depth % 2 == 0), (rid, "choice identity")
                    for v in dist_deletions(lf):
                        assert choice_hits(v) == [target], (rid, "distractor test")
                    card = None
                    if spec["card"]:
                        assert set(spec["card"]) == set(opts), rid
                        card = "\n".join(f"- {o}: {spec['card'][o]}" for o in opts)
                    gold_row, gold_meta, qtype = opts[target], target, "choice"
                    card_style = "options" if card else "none"
                else:
                    assert not b.pending_dists, rid
                    cps = core_paths(lf)
                    assert len(cps) == 1, (rid, "exactly one CORE")
                    core, depth = cps[0]
                    truth_p = ev(core["child"])
                    g = ev(lf)
                    want = spec["gold2"][0 if tw == "a" else 1] == "y"
                    assert g == want, (rid, spec["ins"], g, want)
                    for v in dist_deletions(lf):
                        assert ev(v) == g, (rid, "distractor test")
                    gold_row = gold_meta = int(g)
                    qtype, opts, card = "noul", None, spec["card"]
                    card_style = card_style_of(card)
                    if card_style == "none":
                        assert re.search(r"\bis it (?:true|false) that\b", spec["ins"], re.I), (rid, "card-less frame")
                # cue <-> node consistency
                refs = refs_of(lf)
                for i, cu in enumerate(b.cues):
                    if cu["cls"] == LK:
                        assert i not in refs and not cu["scoping"], (rid, i)
                    else:
                        assert len(refs.get(i, [])) == 1, (rid, i, cu, "every cue sits on exactly one node")
                n_dist = sum(1 for i, cu in enumerate(b.cues) if refs.get(i) == ["DIST"])
                built.append(dict(spec=spec, rid=rid, lf=lf, depth=depth, truth_p=truth_p, cues=b.cues,
                                  n_dist=n_dist, gold_row=gold_row, gold_meta=gold_meta, qtype=qtype, opts=opts,
                                  card=card, card_style=card_style))
            # rungs: R0 / AR / CH / D as written; N<k> must equal the computed depth; a D row needs its twin
            for x in built:
                r = x["spec"]["rung"]
                x["rung"] = r
                if r == "D":
                    twin = [y for y in built if y is not x and y["qtype"] == "noul" and y["depth"] == x["depth"]
                            and y["gold_row"] == x["gold_row"] and y["n_dist"] < x["n_dist"]]
                    assert x["n_dist"] >= 1 and twin, (x["rid"], "D needs a distractor and its twin")
                elif r.startswith("N"):
                    assert int(r[1]) == x["depth"], (x["rid"], r, x["depth"])
            for x in built:
                negq = [cu for cu in x["cues"] if cu["cls"] != LK and cu["position"] in QUESTION_POS]
                if x["rung"] == "R0":
                    assert x["depth"] == 0 and not negq, x["rid"]
                if x["rung"] == "AR":
                    assert x["depth"] == 1 and has_null_not(x["lf"]) and not negq and \
                        not any(cu["scoping"] for cu in x["cues"]), x["rid"]
                    assert any(y["qtype"] == "noul" and y["depth"] % 2 == 1 and y["rung"] != "AR"
                               and y["gold_row"] == x["gold_row"] for y in built), (x["rid"], "AR needs an odd sibling")
            golds = {x["gold_row"] for x in built if x["qtype"] == "noul"}
            assert golds == {0, 1}, lid
            # relations among pure yes/no rows that share the R0 core
            pcs = {x["rid"]: (pure_chain(x["lf"]) if x["qtype"] == "noul" else None) for x in built}
            r0 = [x for x in built if x["rung"] == "R0"][0]
            core0 = json.dumps(pcs[r0["rid"]][1], sort_keys=True)
            pure = [x for x in built if pcs[x["rid"]] is not None and json.dumps(pcs[x["rid"]][1], sort_keys=True)
                    == core0]
            evens = [x for x in pure if pcs[x["rid"]][0] % 2 == 0 and x is not r0]
            odds = [x for x in pure if pcs[x["rid"]][0] % 2 == 1]
            ncomp = collections.Counter()
            for x in evens:
                rels.append({"type": "equiv", "a": r0["rid"], "b": x["rid"], "track": "dev"})
            if odds:
                rels.append({"type": "complement", "a": r0["rid"], "b": odds[0]["rid"], "track": "dev"})
                ncomp[r0["rid"]] += 1
                ncomp[odds[0]["rid"]] += 1
                for x in odds[1:]:
                    rels.append({"type": "equiv", "a": odds[0]["rid"], "b": x["rid"], "track": "dev"})
                free_even = [x for x in evens if ncomp[x["rid"]] == 0]
                for x in odds[1:]:
                    if free_even:
                        e = free_even.pop(0)
                        rels.append({"type": "complement", "a": e["rid"], "b": x["rid"], "track": "dev"})
                        ncomp[e["rid"]] += 1
                        ncomp[x["rid"]] += 1
            state_neg = bool(STATE_NEG_RE.search(T_["state"]))
            for x in built:
                spec = x["spec"]
                role = "choice" if x["qtype"] == "choice" else ("aff" if x["depth"] == 0 else
                                                                ("neg" if x["depth"] % 2 else "dneg"))
                row = {"id": x["rid"], "group_id": gid, "call_id": call, "split": "dev", "track": "F7X",
                       "source": P["source"], "state": T_["state"], "qtype": x["qtype"],
                       "instructions": spec["ins"], "options": x["opts"], "gold": x["gold_row"], "role": role,
                       "card": x["card"],
                       "meta": {"family": "f7_devx", "version": VERSION, "ladder_id": lid, "rung": x["rung"],
                                "dev_kind": "devx", "orig": T_["orig"], "pair": f"{VERSION}_P{P['n']:02d}",
                                "twin_ladder": f"{VERSION}_L{P['n']:02d}{other}"}}
                meta = {"id": x["rid"], "ladder_id": lid, "rung": x["rung"], "lf": x["lf"],
                        "truth_P": bool(x["truth_p"]), "depth": x["depth"], "n_cues": len(x["cues"]),
                        "n_distractor": x["n_dist"], "cues": x["cues"], "phen": sorted(set(spec["phen"])),
                        "frame_family": spec["ff"], "frame_id": spec["fid"], "ladder_kind": P["kind"],
                        "source": P["source"], "dev_kind": "devx", "card_style": x["card_style"],
                        "gold": x["gold_meta"], "qtype": x["qtype"], "state_neg": state_neg, "orig": T_["orig"],
                        "pair": f"{VERSION}_P{P['n']:02d}", "twin_ladder": f"{VERSION}_L{P['n']:02d}{other}"}
                if 21 in meta["phen"]:
                    assert x["qtype"] == "noul" and spec["ant"] is not None, x["rid"]
                    meta["antonym_gold"] = int(bool(spec["ant"](T_["atoms"])))
                if spec["content"]:
                    meta["content_negations"] = list(spec["content"])
                if spec["note"]:
                    meta["note"] = spec["note"]
                if x["qtype"] == "choice":
                    meta["select"] = x["lf"]["select"]
                    meta["n_options"] = len(x["opts"])
                    meta["gold_pos"] = x["gold_meta"]
                rows.append(row)
                metas.append(meta)
                packet.append({"id": x["rid"], "ladder_id": lid, "orig": T_["orig"], "qtype": x["qtype"],
                               "state": T_["state"], "instructions": spec["ins"], "card": x["card"],
                               "options": x["opts"]})
    # twins: every yes/no question appears once per twin, with opposite golds
    byq = collections.defaultdict(list)
    for r in rows:
        if r["qtype"] == "noul":
            byq[(r["meta"]["pair"], r["instructions"], r["card"])].append(r["gold"])
    assert all(sorted(v) == [0, 1] for v in byq.values()), [k for k, v in byq.items() if sorted(v) != [0, 1]][:3]
    assert len({r["id"] for r in rows}) == len(rows)
    return rows, metas, rels, packet


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--outdir":  # dry runs write elsewhere
        _d = Path(sys.argv[2])
        _d.mkdir(parents=True, exist_ok=True)
        OUT_ROWS, OUT_META, OUT_REL, OUT_PACKET = (_d / OUT_ROWS.name, _d / OUT_META.name, _d / OUT_REL.name,
                                                   _d / OUT_PACKET.name)
    rows, metas, rels, packet = build(gold_positions(build()[1]))
    sys.path.insert(0, str(LEAN))
    try:  # the trainer's own row check (read-only import)
        import train_decoder
        train_decoder.check_rows(rows)
        chk = "train_decoder.check_rows: pass"
    except ImportError as e:  # pragma: no cover
        chk = f"train_decoder import failed ({e}); not checked"
    OUT_ROWS.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    OUT_META.write_text("".join(json.dumps(m, ensure_ascii=False) + "\n" for m in metas))
    OUT_REL.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rels))
    OUT_PACKET.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in packet))
    print(chk)
    print(len(rows), "rows,", len({m["ladder_id"] for m in metas}), "ladders,", len(rels), "relations")
