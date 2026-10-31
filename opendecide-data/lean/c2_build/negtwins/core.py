"""negtwins/core.py: A42-D item 7 negation-twin framework, core: parser, rewrite engine, pattern catalogue.

A PATTERN is a deterministic program rewrite of a yes/no question core:

    pattern = (operator, frame or cue, predicate class, contraction / verb / lexical pair, relation)

The engine never reads a gold and never calls a model. Lexicon entries (extra truth frames, negative frames, lexical
complement pairs) are Haiku-drafted and enter the catalogue only after G-LEX 2/2 (lexicon.py of this folder); the
programmatic seeds below are the T37b frames that G0-lite already closed.

  instruction   = preamble + core        the core is the LAST sentence, a single polar question ending in "?"
  parse(core)   -> Q(aux, subj, rest, cls, verb, tail)   two independent parsers (A regex, B token scan) must agree
  rewrite(q, p) -> twin core | None      None = the pattern does not apply to this question (never a guess)

Operators (relation: complement = the twin's gold is 1 - the base gold, equiv = the same gold):
  FRAME_NOT   complement  positive frame + the proposition with one "not" / "n't" after the subject's auxiliary
  NEG_FRAME   complement  negative frame ("Is it false that ...") over the POSITIVE proposition (declarative order)
  FAIL_TO     complement  "fail to" before the main verb (do-questions), frame optional
  LACK        complement  have / contain / include -> lack, frame optional
  LEX_PAIR    complement  the main predicate word replaced by its exact lexical complement (allowed -> prohibited)
  POS_FRAME   equiv       positive frame over the unchanged proposition
  DNEG_PAIR   equiv       positive frame + "not" + the pair's complement word (does not omit == mentions)
  DNEG_FAIL   equiv       positive frame + "does not fail to"
A43 (f): no negated interrogative frame over a negated proposition. Every operator here puts at most ONE negation
layer into the frame OR the proposition for complements; the double-negation equivs keep the frame positive.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import paths  # noqa: E402,F401  (puts c_src/common on sys.path)
import negcount  # noqa: E402
from t37b import sources as SRC  # noqa: E402

HERE = Path(__file__).resolve().parent
COMPLEMENT_OPS = ("FRAME_NOT", "NEG_FRAME", "FAIL_TO", "LACK", "LEX_PAIR")
EQUIV_OPS = ("POS_FRAME", "DNEG_PAIR", "DNEG_FAIL")
OPS = COMPLEMENT_OPS + EQUIV_OPS
IMPLICIT_OPS = ("NEG_FRAME", "FAIL_TO", "LACK")          # spec spec 3.18 "implicit negation" share (fail to, lack, false)
ANTONYM_OPS = ("LEX_PAIR",)                             # spec 3.18 "closed antonym list" share
SYNTACTIC_OPS = ("FRAME_NOT",)

SEED_POS_FRAMES = tuple(SRC.FRAMES_TRAIN)               # 6, closed by G0-lite T37b
SEED_NEG_FRAMES = ("Is it false that", "Is it not the case that")
DEV_FRAMES = tuple(SRC.FRAMES_DEV)                      # T37b-dev frames: never trained, reused as held-out
LACK_VERBS = ("have", "contain", "include")

# closed verb table: base -> (3rd person singular, past). A do-question parses only with a verb listed here.
VERB_FORMS = {
    "ask": ("asks", "asked"), "say": ("says", "said"), "mention": ("mentions", "mentioned"),
    "use": ("uses", "used"), "involve": ("involves", "involved"), "make": ("makes", "made"),
    "name": ("names", "named"), "send": ("sends", "sent"), "give": ("gives", "gave"),
    "try": ("tries", "tried"), "contain": ("contains", "contained"), "require": ("requires", "required"),
    "include": ("includes", "included"), "have": ("has", "had"), "show": ("shows", "showed"),
    "state": ("states", "stated"), "describe": ("describes", "described"), "refer": ("refers", "referred"),
    "list": ("lists", "listed"), "provide": ("provides", "provided"), "allow": ("allows", "allowed"),
    "permit": ("permits", "permitted"), "support": ("supports", "supported"), "cover": ("covers", "covered"),
    "offer": ("offers", "offered"), "report": ("reports", "reported"), "confirm": ("confirms", "confirmed"),
    "mean": ("means", "meant"), "need": ("needs", "needed"), "apply": ("applies", "applied"),
    "reveal": ("reveals", "revealed"), "request": ("requests", "requested"), "explain": ("explains", "explained"),
    "identify": ("identifies", "identified"), "cite": ("cites", "cited"), "quote": ("quotes", "quoted"),
    "address": ("addresses", "addressed"), "involve": ("involves", "involved"), "invite": ("invites", "invited"),
    "announce": ("announces", "announced"), "recommend": ("recommends", "recommended"),
    "specify": ("specifies", "specified"), "indicate": ("indicates", "indicated"), "suggest": ("suggests", "suggested"),
    "include": ("includes", "included"), "demand": ("demands", "demanded"), "accept": ("accepts", "accepted"),
    "approve": ("approves", "approved"), "grant": ("grants", "granted"), "match": ("matches", "matched"),
    "cause": ("causes", "caused"), "change": ("changes", "changed"), "ignore": ("ignores", "ignored"),
    "bypass": ("bypasses", "bypassed"), "follow": ("follows", "followed"), "reach": ("reaches", "reached"),
    "fail": ("fails", "failed"), "do": ("does", "did"), "take": ("takes", "took"), "get": ("gets", "got"),
    "cost": ("costs", "cost"), "occur": ("occurs", "occurred"), "appear": ("appears", "appeared"),
}
def register_verbs(pairs) -> None:
    """Admitted verb pairs extend the closed verb table (so 'Does the notice omit the fee?' parses). Idempotent."""
    for pr in pairs or []:
        if pr.get("pos") == "verb":
            for side in ("a", "b"):
                f = pr[side]
                VERB_FORMS.setdefault(f["base"], (f["s3"], f["past"]))


DETS = frozenset({"the", "this", "that", "these", "those", "a", "an", "its", "their", "his", "her", "our", "your"})
AUX_DO = ("does", "do", "did")
AUX_COP = ("is", "are", "was", "were")
AUX_HAVE = ("has", "have", "had")
AUX_MOD = ("can", "could", "should", "would", "may", "might", "must", "will", "shall")
NT = {"does": "doesn't", "do": "don't", "did": "didn't", "is": "isn't", "are": "aren't", "was": "wasn't",
      "were": "weren't", "has": "hasn't", "have": "haven't", "had": "hadn't", "can": "can't"}
# words that may open the predicate after a copular subject (closed; adjectives / participles / adverbs / articles)
PRED_START = frozenset({
    "a", "an", "limited", "free", "given", "mainly", "primarily", "faithful", "worth", "supported", "off-topic",
    "required", "allowed", "permitted", "prohibited", "forbidden", "available", "open", "closed", "valid", "true",
    "correct", "accurate", "based", "written", "stated", "mentioned", "listed", "included", "covered", "named",
    "shown", "published", "complete", "current", "relevant", "clear", "specific", "eligible", "ready", "public",
    "private", "optional", "mandatory", "provided", "offered", "intended", "designed", "meant", "about",
    "outside", "inside", "within", "located", "held", "scheduled", "planned", "approved", "accepted", "recommended"})
CLAUSE_WORDS = frozenset({"so", "because", "rather", "than", "while", "although", "though", "since", "unless",
                          "whereas", "and", "if", "whether"})
QUANT = frozenset({"all", "every", "each", "some", "most", "many", "much", "few", "several", "none", "nobody",
                   "nothing", "never", "always", "sometimes", "usually", "often", "only", "just", "exactly",
                   "half", "majority", "neither", "either", "everyone", "everything", "everybody", "anyone",
                   "anything", "anybody", "someone", "something", "somebody", "least", "more", "less", "fewer"})
MODALS = frozenset(AUX_MOD) | {"ought", "need"}
_TOK = re.compile(r"\"[^\"\n]*\"|“[^”\n]*”|[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")


def tokens(text: str) -> list:
    """Lower-case word tokens; quoted spans whole; n't split off; cannot -> can not. Punctuation dropped."""
    out = []
    for m in _TOK.finditer(text or ""):
        t = m.group().replace("’", "'")
        if t[0] in "\"“":
            out.append(t)
            continue
        low = t.lower()
        if low == "cannot":
            out += ["can", "not"]
        elif low == "can't":
            out += ["can", "not"]
        elif low == "won't":
            out += ["will", "not"]
        elif low.endswith("n't") and len(low) > 3:
            out += [low[:-3], "not"]
        else:
            out.append(low)
    return out


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------------------------------------ instruction split

def split_instruction(instr: str):
    """(preamble, core) or None. The core is the last sentence; it holds the one '?' and no inner sentence stop."""
    if not instr or not instr.endswith("?") or instr.count("?") != 1:
        return None
    bounds = [0] + [m.end() for m in re.finditer(r"(?<=[.!?\"”)\]:])\s+", instr)]
    for b in reversed(bounds):
        t = instr[b:]
        if t[:1].isupper() and t.count("?") == 1 and not re.search(r"[.!;:]\s", t):
            return instr[:b], t
    return None


@dataclass(frozen=True)
class Q:
    aux: str                    # lower case: does / is / can ...
    subj: str                   # subject text exactly as written ("there" for existential questions)
    rest: str                   # everything after the subject, without the final "?"
    cls: str                    # DO | COP | HAVE | MOD | THERE
    verb: str = ""              # DO: the base verb that opens `rest`
    tail: str = ""              # DO: `rest` after the verb (starts with a space or is empty)

    def core_key(self) -> str:
        return f"{self.cls}|{self.aux}|{self.subj}|{self.rest}"


_AUX_ALL = AUX_DO + AUX_COP + AUX_HAVE + AUX_MOD
_HEAD = re.compile(r"^(?P<aux>" + "|".join(a.capitalize() for a in _AUX_ALL) + r") (?P<body>.+)\?$")
_NP = r"(?:(?:the|this|that|these|those|an?|its|their)\s+)?(?:[A-Za-z0-9'’-]+\s+){0,5}?[A-Za-z0-9'’-]+(?:\s+below)?"


def _fixed_subject(body: str):
    """'there ...' existential, or None."""
    return ("there", body[6:]) if body.lower().startswith("there ") else None


def parse_a(core: str):
    """Parser A: anchored regexes with a lazy noun phrase and the closed verb / predicate lists."""
    m = _HEAD.match(core or "")
    if not m:
        return None
    aux, body = m["aux"].lower(), m["body"]
    if aux in AUX_COP + AUX_HAVE and _fixed_subject(body):
        s, r = _fixed_subject(body)
        return Q(aux, s, r, "THERE", "", "") if aux in AUX_COP else None
    if aux in AUX_DO:
        vs = "|".join(sorted(VERB_FORMS, key=len, reverse=True))
        mm = re.match(r"^(?P<subj>" + _NP + r")\s+(?P<verb>" + vs + r")\b(?P<tail>.*)$", body)
        return Q(aux, mm["subj"], mm["verb"] + mm["tail"], "DO", mm["verb"], mm["tail"]) if mm else None
    if aux in AUX_COP + AUX_HAVE:
        ps = "|".join(sorted(PRED_START, key=len, reverse=True))
        mm = re.match(r"^(?P<subj>" + _NP + r")\s+(?P<rest>(?:" + ps + r"|[a-z]+ed|[a-z]+en)\b.*)$", body)
        if not mm or len(mm["subj"].split()) < 2:
            return None
        return Q(aux, mm["subj"], mm["rest"], "COP" if aux in AUX_COP else "HAVE")
    mm = re.match(r"^(?P<subj>" + _NP + r")\s+(?P<rest>[a-z]+\b.*)$", body)       # modal: subject + bare verb phrase
    return Q(aux, mm["subj"], mm["rest"], "MOD") if mm and len(mm["subj"].split()) >= 2 else None


def parse_b(core: str):
    """Parser B: token scan on the words after the auxiliary; the subject ends at the first closed-list word."""
    if not core or not core.endswith("?"):
        return None
    words = core[:-1].split(" ")
    aux = words[0].lower()
    if aux not in _AUX_ALL or words[0] != words[0].capitalize() or len(words) < 4:
        return None
    body = words[1:]
    if body[0].lower() == "there":
        return Q(aux, "there", " ".join(body[1:]), "THERE") if aux in AUX_COP and len(body) > 2 else None
    lows = [w.lower().strip(",") for w in body]
    if aux in AUX_DO:
        lo = 2 if lows[0] in DETS else 1
        idx = next((i for i in range(lo, len(lows)) if lows[i] in VERB_FORMS), None)
        if idx is None:
            return None
        return Q(aux, " ".join(body[:idx]), " ".join(body[idx:]), "DO", lows[idx], (" " + " ".join(body[idx + 1:])) if
                 idx + 1 < len(body) else "")
    if aux in AUX_COP + AUX_HAVE:
        idx = next((i for i in range(2, len(lows)) if lows[i] in PRED_START or re.fullmatch(r"[a-z]+(?:ed|en)", lows[i])),
                   None)
        if idx is None:
            return None
        return Q(aux, " ".join(body[:idx]), " ".join(body[idx:]), "COP" if aux in AUX_COP else "HAVE")
    idx = next((i for i in range(2, len(lows)) if re.fullmatch(r"[a-z]+", lows[i]) and lows[i - 1] not in DETS), None)
    return None if idx is None else Q(aux, " ".join(body[:idx]), " ".join(body[idx:]), "MOD")


def parse(core: str):
    """The question both parsers read identically, else None (dropped: never a guess)."""
    a, b = parse_a(core), parse_b(core)
    return a if a is not None and a == b else None


def _lower_first(s: str) -> str:
    w = s.split(" ", 1)[0]
    return s[0].lower() + s[1:] if w.lower() in DETS or w.lower() in {"someone's", "anyone's", "there"} else s


def declarative(q: Q) -> str:
    """The proposition in declarative order (no negation, no question mark)."""
    s = _lower_first(q.subj)
    if q.cls == "DO":
        f3, past = VERB_FORMS[q.verb]
        v = {"does": f3, "did": past, "do": q.verb}[q.aux]
        return f"{s} {v}{q.tail}"
    if q.cls == "THERE":
        return f"there {q.aux} {q.rest}"
    return f"{s} {q.aux} {q.rest}"


# ------------------------------------------------------------------------------------------------ eligibility guards

def has_negation(core: str) -> bool:
    return negcount.count(core).k_all > 0


def not_insertion_ok(q: Q, core: str) -> bool:
    """Scope guard for operators that put 'not' / 'fail to' / 'lack' into the proposition (T37b scope rule)."""
    if has_negation(core):
        return False
    front = set(tokens(q.subj))
    back = set(tokens(q.rest))
    if front & (QUANT | MODALS | CLAUSE_WORDS) or back & (MODALS | CLAUSE_WORDS):
        return False
    return not ((back & QUANT) - {"any", "anyone", "anything", "anybody", "either", "always"})


# ------------------------------------------------------------------------------------------------ patterns

@dataclass(frozen=True)
class Pattern:
    pid: str
    op: str
    relation: str                 # complement | equiv
    cls: str                      # predicate class the pattern applies to: DO | COP | HAVE | MOD | THERE
    frame: str = ""               # truth / negative frame, "" = none
    contr: str = ""               # "" | "not" | "nt"  (FRAME_NOT, DNEG_*)
    verb: str = ""                # LACK: have | contain | include
    pair: str = ""                # LEX_PAIR / DNEG_PAIR: pair_id
    direction: str = ""           # LEX_PAIR: "a>b" | "b>a"
    source: str = "prog"          # prog (seed list) | lex (Haiku-drafted, G-LEX 2/2) | heldout
    held_out: bool = False

    @property
    def kind(self) -> str:          # spec 3.18 share bucket
        return ("syntactic" if self.op in SYNTACTIC_OPS else "implicit" if self.op in IMPLICIT_OPS else
                "antonym" if self.op in ANTONYM_OPS else "equiv")

    def surfaces(self) -> list:
        return [s for s in (self.frame, {"FAIL_TO": "fail to", "LACK": "lack"}.get(self.op, ""), self.pair) if s]


def _pid(op, cls, frame, contr, verb, pair, direction):
    return "|".join([op, cls, sha(frame)[:6] if frame else "-", contr or "-", verb or "-", pair or "-", direction or "-"])


def make_pattern(op, cls, *, frame="", contr="", verb="", pair="", direction="", source="prog", held_out=False):
    rel = "complement" if op in COMPLEMENT_OPS else "equiv"
    return Pattern(_pid(op, cls, frame, contr, verb, pair, direction), op, rel, cls, frame, contr, verb, pair,
                   direction, source, held_out)


# lexical complement pairs: {"pair_id", "pos": "verb"|"adj", "a": {forms}, "b": {forms}} ; forms: base, s3, past, pp, adj
def pair_words(pr: dict, side: str) -> set:
    return {v for v in pr[side].values() if v}


def _pair_replace(q: Q, pr: dict, direction: str):
    """(new rest) with the main predicate word replaced, or None. DO: the verb; COP / HAVE: the first word of rest."""
    src, dst = ("a", "b") if direction == "a>b" else ("b", "a")
    if pr["pos"] == "verb" and q.cls == "DO":
        if q.verb != pr[src].get("base"):
            return None
        return f"{pr[dst]['base']}{q.tail}"
    if pr["pos"] == "adj" and q.cls in ("COP", "HAVE"):
        first, _, tail = q.rest.partition(" ")
        if first.lower() != pr[src].get("adj", "").lower():
            return None
        return pr[dst]["adj"] + (" " + tail if tail else "")
    return None


def rewrite(q: Q, core: str, p: Pattern, pairs: dict | None = None):
    """The twin core for pattern p on the parsed question q, or None when p does not apply. Deterministic."""
    if q.cls != p.cls and not (p.op in ("NEG_FRAME", "POS_FRAME") and p.cls == "ANY"):
        return None
    op = p.op
    if op in ("NEG_FRAME", "POS_FRAME"):
        if op == "NEG_FRAME" and has_negation(core):
            return None
        if q.cls == "DO" and q.verb not in VERB_FORMS:
            return None
        return f"{p.frame} {declarative(q)}?"
    if op == "LEX_PAIR":
        pr = (pairs or {}).get(p.pair)
        if pr is None or has_negation(core) or not not_insertion_ok(q, core):
            return None
        new = _pair_replace(q, pr, p.direction)
        if new is None:
            return None
        return f"{q.aux.capitalize()} {q.subj} {new}?" if q.cls != "THERE" else None
    if not not_insertion_ok(q, core):
        return None
    if op == "FRAME_NOT":
        if q.cls == "MOD" and q.aux != "can":
            return None
        if q.aux == "can":
            neg = "can't" if p.contr == "nt" else "cannot"
        else:
            neg = NT[q.aux] if p.contr == "nt" else f"{q.aux} not"
        rest = f"{q.verb}{q.tail}" if q.cls == "DO" else q.rest
        s = "there" if q.cls == "THERE" else _lower_first(q.subj)
        return f"{p.frame} {s} {neg} {rest}?"
    if q.cls != "DO":
        return None
    if op in ("FAIL_TO", "DNEG_FAIL"):
        if op == "DNEG_FAIL":
            return f"{p.frame} {_lower_first(q.subj)} {q.aux} not fail to {q.verb}{q.tail}?"
        if not p.frame:
            return f"{q.aux.capitalize()} {q.subj} fail to {q.verb}{q.tail}?"
        v = {"does": "fails", "did": "failed", "do": "fail"}[q.aux]
        return f"{p.frame} {_lower_first(q.subj)} {v} to {q.verb}{q.tail}?"
    if op == "LACK":
        if q.verb != p.verb or q.verb not in LACK_VERBS:
            return None
        if not p.frame:
            return f"{q.aux.capitalize()} {q.subj} lack{q.tail}?"
        v = {"does": "lacks", "did": "lacked", "do": "lack"}[q.aux]
        return f"{p.frame} {_lower_first(q.subj)} {v}{q.tail}?"
    if op == "DNEG_PAIR":
        pr = (pairs or {}).get(p.pair)
        new = _pair_replace(q, pr, "a>b") if pr else None
        return None if new is None else f"{p.frame} {_lower_first(q.subj)} {q.aux} not {new}?"
    return None


def rewrite_cop_dneg(q: Q, core: str, p: Pattern, pairs: dict):
    """DNEG_PAIR on a copular question: 'Is it true that S is not <complement word> ...?'."""
    pr = pairs.get(p.pair)
    new = _pair_replace(q, pr, "a>b") if pr else None
    if new is None or not not_insertion_ok(q, core):
        return None
    return f"{p.frame} {_lower_first(q.subj)} {q.aux} not {new}?"


def apply(core: str, p: Pattern, pairs: dict | None = None):
    """parse + rewrite in one call: (twin core, Q) or (None, None)."""
    if p.pair and pairs:
        register_verbs(pairs.values())
    q = parse(core)
    if q is None:
        return None, None
    if p.op == "DNEG_PAIR" and q.cls in ("COP", "HAVE"):
        return rewrite_cop_dneg(q, core, p, pairs or {}), q
    return rewrite(q, core, p, pairs), q


# ------------------------------------------------------------------------------------------------ catalogue

PROG_CLASSES_NOT = ("DO", "COP", "HAVE", "THERE", "MOD")        # MOD is `can` only for FRAME_NOT
CLASSES_WRAP = ("DO", "COP", "HAVE", "MOD", "THERE")


MODAL_SPLIT = re.compile(r"\b(?:couldn't|won't|wouldn't|shouldn't|mustn't|mightn't|shan't|mayn't)\b|"
                         r"\b(?:can|could|would|should|may|might|must|will|shall)\s+not\b", re.I)


def a48h_class(p) -> str:
    """Ruling A48 (h), pattern level. '' = admitted. (i) a frame that negates the interrogative ("Is it not the case that",
    "Isn't ...") even over a positive proposition. (ii) is a twin-level guard (MODAL_SPLIT): a split or ambiguous modal negation
    ("can not", "could not", "couldn't" ...) is refused; "cannot" and its contraction "can't" (the modal negated as a unit,
    orchestrator decision 15 Oct) stay. Frame wording rules (iii)/(iv) live in lexicon.lint_frame."""
    if p.frame and "not" in tokens(p.frame):
        return "i_negated_interrogative_frame"
    return ""


def build_catalogue(lex: dict | None = None, a48h: bool = True) -> list:
    """All trained patterns (a48h=False rebuilds the pre-A48(h) 116-pattern seed set, for the exact_prog batch id only). lex = admitted lexicon (lexicon.load_admitted()): pos_frames, neg_frames, pairs.
    Programmatic = seed frames and cues (source 'prog'); every pattern that needs an admitted entry is source 'lex'."""
    lex = lex or {"pos_frames": [], "neg_frames": [], "pairs": []}
    register_verbs(lex.get("pairs"))
    pos = [(f, "prog") for f in SEED_POS_FRAMES] + [(f, "lex") for f in lex.get("pos_frames", [])]
    neg = [(f, "prog") for f in SEED_NEG_FRAMES] + [(f, "lex") for f in lex.get("neg_frames", [])]
    out = []
    for f, src in pos:
        for cls in ("DO", "COP", "HAVE", "MOD"):
            if cls == "MOD":
                out.append(make_pattern("FRAME_NOT", "MOD", frame=f, contr="not", source=src))   # `can` questions
                out.append(make_pattern("FRAME_NOT", "MOD", frame=f, contr="nt", source=src))
                continue
            for c in ("not", "nt"):
                out.append(make_pattern("FRAME_NOT", cls, frame=f, contr=c, source=src))
        out.append(make_pattern("FRAME_NOT", "THERE", frame=f, contr="not", source=src))
        out.append(make_pattern("FRAME_NOT", "THERE", frame=f, contr="nt", source=src))
        out.append(make_pattern("POS_FRAME", "DO", frame=f, source=src))
        out.append(make_pattern("POS_FRAME", "COP", frame=f, source=src))
        out.append(make_pattern("DNEG_FAIL", "DO", frame=f, source=src))
        out.append(make_pattern("FAIL_TO", "DO", frame=f, source=src))
        for v in LACK_VERBS:
            out.append(make_pattern("LACK", "DO", frame=f, verb=v, source=src))
    out.append(make_pattern("FAIL_TO", "DO", source="prog"))
    for v in LACK_VERBS:
        out.append(make_pattern("LACK", "DO", verb=v, source="prog"))
    for f, src in neg:
        for cls in CLASSES_WRAP:
            out.append(make_pattern("NEG_FRAME", cls, frame=f, source=src))
    dframes = [f for f, _ in pos[:6]]                       # DNEG_PAIR uses the seed frames, one per pair (hash order)
    for pr in lex.get("pairs", []):
        f = dframes[int(sha(pr["pair_id"])[:4], 16) % len(dframes)]
        for d in ("a>b", "b>a"):
            cls = "DO" if pr["pos"] == "verb" else "COP"
            out.append(make_pattern("LEX_PAIR", cls, pair=pr["pair_id"], direction=d, source="lex"))
        out.append(make_pattern("DNEG_PAIR", "DO" if pr["pos"] == "verb" else "COP", frame=f, pair=pr["pair_id"],
                                source="lex"))
    seen, uniq = set(), []
    for p in out:
        if p.pid not in seen:
            seen.add(p.pid)
            if not (a48h and a48h_class(p)):
                uniq.append(p)
    return uniq


def catalogue_report(cat: list) -> dict:
    from collections import Counter
    return {"n": len(cat), "by_op": dict(Counter(p.op for p in cat)), "by_source": dict(Counter(p.source for p in cat)),
            "by_kind": dict(Counter(p.kind for p in cat)), "by_relation": dict(Counter(p.relation for p in cat))}
