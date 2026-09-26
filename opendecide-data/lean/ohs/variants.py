"""OHS-1 consistency layer: deterministic yes/no variants (no model calls, no LLM-written text, seed 20260927).

make_variants(rows) -> (new_rows, relations)

For every yes/no base row (qtype "noul", role "aff") and for every choice row turned into a yes/no row
("Is the correct answer '<X>'?", X = gold or a random distractor, exactly 50/50 per source), it adds:
  neg   gold flipped, relation "complement"  -- either a NEW negation frame over p (NEG_T), or a NEW affirmative
                                                frame over the clause-negated proposition n (AFF_T; clausal "not"
                                                or affixal "untrue / irrelevant / harmless ..." where that is the
                                                exact contradictory)
  dneg  gold same,    relation "equiv"       -- either a NEW double-negation frame over p (DNEG_T), or a NEW
                                                negation frame over n (NEG_T x clause negation)
  para  gold same,    relation "equiv"       -- a NEW affirmative paraphrase frame over p (PARA_T)
Choice-derived rows also add the yes/no base row itself (role "aff", id "<choice id>_yn").

The proposition p is built from the base question: "Is this message hateful?" -> "this message is hateful",
"Does the statement follow from the passage?" -> "the statement follows from the passage",
"Is the correct answer 'X'?" -> "the correct answer is 'X'". Questions the rule parser cannot read safely fall
back to the always-grammatical p = 'the correct reply to "<question>" is yes' (n: '... is no').

Every template is NEW: at import time this module collects every string literal of every builder / generator in
opendecide-data (lean/*.py incl. build_*.py, lean/pg/, build/, assets/, design/) and every string in the wording
banks assets/templates/**.jsonl, and asserts that no template here equals, or shares a 6-word run with, any of
them. `python ohs/variants.py` additionally audits the templates against every instruction string in lean/data/
(train, dev, eval files) and runs a self-test.
"""
import ast
import hashlib
import json
import random
import re
from pathlib import Path

SEED = 20260927
HERE = Path(__file__).resolve().parent            # lean/ohs
LEAN = HERE.parent                                # lean
ROOT = LEAN.parent                                # opendecide-data

# ============================================================================ templates
# {p} = proposition in running text ("that {p}"); {P} = the same proposition as a standalone sentence.
# Families: attributed belief, statement falsity, rule-out, affixal negation, betting, correction, exceptive
# conditional ("unless"), nominal denial, evaluative (well founded / tenable), verdict (fact-checker).
NEG_T = [  # negation: yes <=> p is false
    ("N1", "Would an auditor who reported that {p} have it wrong?"),            # attributed belief
    ("N2", "Consider the statement: {P}. Is this statement false?"),            # statement falsity
    ("N3", "Can it be ruled out that {p}?"),                                    # rule-out
    ("N4", "Is the idea that {p} baseless?"),                                   # affixal (-less)
    ("N5", "Would a bet that {p} be lost?"),                                    # betting
    ("N6", "Does the claim that {p} need to be corrected?"),                    # correction
    ("N7", "Is it untenable to hold that {p}?"),                                # affixal (un-)
    ("N8", "Answer yes unless {p}."),                                           # exceptive conditional
]
DNEG_T = [  # double negation: yes <=> p is true
    ("D1", "Is it unjustified to doubt that {p}?"),                             # affixal + negative verb
    ("D2", "Would an auditor who denied that {p} have it wrong?"),              # attributed denial
    ("D3", "Consider the statement: {P}. Is this statement not false?"),        # statement falsity + not
    ("D4", "Would a bet against the claim that {p} be lost?"),                  # betting against + lost
    ("D5", "Is the denial that {p} unfounded?"),                                # nominal denial + affixal
    ("D6", "Answer no unless {p}."),                                            # exceptive conditional
]
AFF_T = [  # affirmative frames; applied to the clause-negated proposition n they give a clause-negation "neg"
    ("A1", "Would an auditor who reported that {p} have it right?"),
    ("A2", "Would a bet that {p} pay off?"),
    ("A3", "Consider the statement: {P}. Is this statement true?"),
    ("A4", "Does the claim that {p} stand as written?"),
    ("A5", "Is the idea that {p} well founded?"),
    ("A6", "Is it tenable to hold that {p}?"),
    ("A7", "Would a fact-checker rate the assertion that {p} as true?"),
    ("A8", "Answer yes if {p}, and no otherwise."),
]
PARA_T = [  # paraphrase: yes <=> p is true
    ("P1", "Would an analyst who stated that {p} be right?"),                   # attributed belief
    ("P2", "Would a wager that {p} be won?"),                                   # betting
    ("P3", "Take the following statement: {P}. Does it hold up?"),              # statement verification
    ("P4", "Is the proposition that {p} correct?"),                             # nominal
    ("P5", "Can it be confirmed that {p}?"),                                    # confirm (mirror of rule-out)
    ("P6", "Suppose a colleague asserted that {p}. Would the colleague be correct?"),  # hypothetical attribution
    ("P7", "Reply yes when {p}; otherwise reply no."),                          # conditional
    ("P8", "Is the following true of the text: {p}?"),                          # predication over the text
]
ALL_T = {"neg": NEG_T, "dneg": DNEG_T, "aff": AFF_T, "para": PARA_T}

# ============================================================================ novelty check
_SLOT = re.compile(r"\{[^{}]*\}|%[sd]")


def _words(s: str):
    s = _SLOT.sub(" slot ", s.lower())
    return re.sub(r"[^a-z0-9']+", " ", s).split()


def _grams(ws, k=6):
    return {tuple(ws[i:i + k]) for i in range(len(ws) - k + 1)}


def _fstring(node) -> str:
    out = []
    for v in node.values:
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            out.append(v.value)
        else:
            out.append("{}")
    return "".join(out)


def _py_strings(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return []
    out, inner = [], set()
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            out.append(_fstring(node))
            inner.update(id(v) for v in node.values)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in inner:
            out.append(node.value)
    return out


def _json_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _json_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _json_strings(v)


def collect_existing_templates():
    """Every string literal in the project's builders/generators + every string in the wording banks.
    Returns (all_strings, template_like) where template_like = strings with a slot ({p}, {P}, {q}, {}, %s)
    or a question mark, i.e. the TRAIN / DEV / EVAL wordings and question strings."""
    files = sorted(set(LEAN.glob("*.py")) | set(LEAN.glob("pg/*.py")) | set(ROOT.glob("build/**/*.py"))
                   | set(ROOT.glob("assets/**/*.py")) | set(ROOT.glob("design/**/*.py")) | set(ROOT.glob("*.py")))
    strings = []
    for f in files:
        if HERE in f.parents or ".venv" in f.parts:
            continue  # OHS itself (held-out side) is not a source of train/dev/eval wordings
        strings += _py_strings(f)
    for f in sorted(ROOT.glob("assets/templates/**/*.jsonl")):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                strings += list(_json_strings(json.loads(line)))
    strings = sorted({s for s in strings if len(_words(s)) >= 1})
    tl = [s for s in strings if ("?" in s or _SLOT.search(s)) and len(_words(s)) >= 3]
    return strings, tl


def check_novelty(templates, existing, k=6):
    """Assert no template equals, or shares a k-word run with, any existing string. Slots count as one word."""
    ex_norm = {tuple(_words(s)) for s in existing}
    ex_grams = set()
    for s in existing:
        ex_grams |= _grams(_words(s), k)
    bad = []
    for tid, t in templates:
        w = _words(t)
        if tuple(w) in ex_norm or t in existing:
            bad.append((tid, t, "equal"))
        hit = _grams(w, k) & ex_grams
        if hit:
            bad.append((tid, t, " ".join(sorted(hit)[0])))
    assert not bad, f"templates overlap existing wordings: {bad}"
    return True


_ALL_TEMPLATES = [x for v in ALL_T.values() for x in v]
assert len({t for _, t in _ALL_TEMPLATES}) == len(_ALL_TEMPLATES), "duplicate template"
EXISTING_STRINGS, COLLECTED_TEMPLATES = collect_existing_templates()
assert len(COLLECTED_TEMPLATES) > 100, "template collection looks broken"
for _must in ("Is it true that {p}?", "Would someone who says that {p} be mistaken?", "Can we conclude from the text that {p}?",
              "Would it be wrong to dispute that {p}?", "Is the assertion that {p} off the mark?"):
    assert _must in COLLECTED_TEMPLATES, f"collector missed a known template: {_must}"
check_novelty(_ALL_TEMPLATES, EXISTING_STRINGS)

# ============================================================================ question -> proposition
BE = {"is", "are", "was", "were"}
DO = {"does", "do", "did"}
HAVE = {"has", "have", "had"}
MODAL_NEG = {"can": "cannot", "could": "could not", "will": "will not", "would": "would not", "shall": "shall not"}
MODAL_UNSAFE = {"may", "might", "must", "should"}      # simple "not" is not the contradictory -> "it is not the case that"
AUX = BE | DO | HAVE | set(MODAL_NEG) | MODAL_UNSAFE
DETS = {"the", "this", "that", "these", "those", "a", "an", "its", "their", "his", "her", "my", "our", "your", "each",
        "every", "any", "some", "both", "all", "either", "neither", "one", "two", "three", "no"}
DEMONSTRATIVE = {"this", "that", "these", "those"}
PRONOUNS = {"it", "he", "she", "they", "we", "you", "i", "someone", "anyone", "something", "anything", "everyone",
            "everything", "somebody", "anybody", "there"}
HEADS = set("""text message statement sentence passage article tweet post comment review email e-mail sms abstract claim
answer question response reply headline title document paragraph hypothesis premise argument conclusion speaker author
writer user customer reviewer label story report excerpt snippet query request utterance summary translation code
program function product dialogue dialog conversation thread essay news item evidence context source citation
reference sentiment tone stance topic emotion intent word phrase term expression pair study paper finding result
trial patient drug treatment company firm person model system option choice entity event relation fact rule name
target mention instance example case caption description definition explanation rationale solution proof step output
input bug commit patch issue ticket transcript turn joke meme poem line span quote quotation number value date amount
price figure table instruction prompt task clause provision contract agreement policy term section decision court
judge party plaintiff defendant witness testimony opinion ruling law statute regulation filing complaint motion
record letter note memo notice lyric verse chapter book film movie show episode song album game app website page
link url tool api function method class variable file message's user's author's speaker's writer's""".split())
PREPS = {"of", "about", "from", "in", "on", "for", "to", "with", "by", "between", "regarding", "concerning", "under"}
PRED_WORDS = set("""true false correct incorrect right wrong accurate inaccurate valid invalid positive negative neutral
spam ham toxic hateful offensive sarcastic ironic relevant irrelevant supported unsupported consistent inconsistent
related unrelated possible impossible likely unlikely safe unsafe harmful harmless legal illegal fair unfair clear
unclear present absent real fake genuine literal grammatical ungrammatical acceptable unacceptable complete incomplete
answerable unanswerable faithful unfaithful biased neutral ambiguous unambiguous appropriate inappropriate more less
not also still already about a an the some any no""".split())
ADJ_SUFFIX = ("ful", "ous", "ive", "able", "ible", "ic", "al", "ent", "ant", "less", "ary", "ory", "ed", "en", "ish")
VERBS = set("""support entail contain mention express describe imply contradict answer follow include discuss show refer
suggest indicate state claim say report agree disagree use involve promote target attack violate reveal need require
provide make have get give match belong relate concern address affect cause increase decrease reduce improve convey
reflect present propose find conclude demonstrate prove confirm refute deny accept reject recommend praise criticize
criticise complain ask request want seek mean sound seem appear look read cite quote reference depend apply hold work
exist occur happen win lose succeed fail pass comply adhere conform satisfy meet fit represent count qualify
constitute encourage incite threaten insult harass mock endorse oppose favor favour like love hate enjoy solve compute
return produce output print raise crash compile run terminate handle check validate leak expose share disclose sell buy
own pay cost offer attempt try intend plan expect believe think know understand remember allow permit prohibit forbid
grant limit restrict waive release assign transfer terminate govern define establish create identify list specify
contain explain justify cover protect breach infringe infer derive originate come go lead result stem arise""".split())
IRREG_PAST = dict(x.split(":") for x in """make:made say:said go:went get:got give:gave take:took come:came win:won
lose:lost find:found leave:left keep:kept think:thought tell:told write:wrote speak:spoke break:broke choose:chose
buy:bought bring:brought hold:held feel:felt meet:met pay:paid run:ran see:saw send:sent set:set sell:sold put:put
read:read lead:led spend:spent stand:stood understand:understood begin:began become:became know:knew grow:grew
draw:drew drive:drove eat:ate fall:fell fight:fought fly:flew forget:forgot hit:hit hurt:hurt let:let ride:rode
rise:rose shoot:shot sing:sang sit:sat sleep:slept steal:stole strike:struck teach:taught throw:threw wear:wore
cut:cut cost:cost quit:quit beat:beat build:built catch:caught deal:dealt hide:hid lay:laid lend:lent mean:meant
seek:sought shake:shook shut:shut spread:spread swear:swore tear:tore wake:woke withdraw:withdrew have:had do:did
arise:arose bear:bore forbid:forbade undertake:undertook overcome:overcame""".split())
# exact contradictories only (binary predicates); graded antonyms (happy/unhappy, clear/unclear ...) are excluded
AFFIX = {"true": "untrue", "correct": "incorrect", "accurate": "inaccurate", "supported": "unsupported",
         "relevant": "irrelevant", "consistent": "inconsistent", "related": "unrelated", "valid": "invalid",
         "answerable": "unanswerable", "grammatical": "ungrammatical", "acceptable": "unacceptable",
         "complete": "incomplete", "possible": "impossible", "faithful": "unfaithful", "toxic": "non-toxic",
         "ambiguous": "unambiguous", "harmful": "harmless", "meaningful": "meaningless", "verifiable": "unverifiable",
         "sufficient": "insufficient", "safe": "unsafe", "ethical": "unethical", "legal": "illegal"}
SELF_REF = {"statement", "claim", "sentence", "assertion", "proposition"}  # heads that clash with statement frames
_TOK = re.compile(r"(?<!\S)(?:'[^']*'|\"[^\"]*\"|“[^”]*”|‘[^’]*’)(?!\S)|\S+")  # quoted spans stay one token
_SCOPE = re.compile(r"^((?:according to|based (?:only )?on|given|in light of|judging (?:only )?by|from|in) [^,?]{1,80}),\s*(.+)$", re.I)
_HEDGE = re.compile(r"^(?:is it (?:true|the case|correct|accurate) that|would you say that|do you think that|"
                    r"can we say that|is it true to say that)\s+(.+)$", re.I)
_YN_DIRECTIVE = re.compile(r"^\s*(?:please\s+)?(?:answer|respond|reply|say|output|return|choose|pick|select)\b[^.?!]*\b(?:yes|no)\b"
                           r"|^\s*\(?yes\s*(?:/|or)\s*no\)?\s*[.:]?\s*$", re.I)
_NPI = [(re.compile(r"\bany(?=\s)"), "some"), (re.compile(r"\banything\b"), "something"),
        (re.compile(r"\banyone\b"), "someone"), (re.compile(r"\banybody\b"), "somebody")]


def _depolarize(s):
    """Affirmative clause from a question: negative-polarity 'any' -> 'some' ('Are there any errors?' -> 'there are some errors')."""
    for rx, w in _NPI:
        s = rx.sub(w, s)
    return s


def _low(t):
    return t.replace("\u2019", "'").lower().strip(",;:")


def _quoted(t):
    return t[:1] in "'\"“‘" and len(t) > 1 and t[-1:] in "'\"”’"


def _head(w):
    return w in HEADS or (w.endswith("s") and w[:-1] in HEADS) or (w.endswith("es") and w[:-2] in HEADS)


def _pred_start(w):
    return w in PRED_WORDS or w in DETS or _quoted(w) or (len(w) > 4 and w.endswith(ADJ_SUFFIX)) or w.endswith("ly")


def _bare_np(toks):
    """Length of a bare noun sequence (object of a preposition without determiner): up to 3 non-predicate words."""
    k = 0
    while k < len(toks) and k < 3 and not _pred_start(_low(toks[k])) and _low(toks[k]) not in PREPS \
            and _low(toks[k]) not in VERBS:
        k += 1
    return k


def _scan_np(toks, mode):
    """Length of the subject noun phrase at the start of toks (mode 'be' | 'do' | 'aux'), or None."""
    if not toks:
        return None
    t0 = _low(toks[0])
    if _quoted(toks[0]) or t0 in PRONOUNS:
        return 1
    if toks[0][:1].isupper() and t0 not in DETS:  # proper noun run
        k = 1
        while k < len(toks) and toks[k][:1].isupper():
            k += 1
        return k
    if t0 not in DETS and not t0.endswith("'s"):
        return None
    k = 1
    while k < len(toks) and k <= 6:
        w = _low(toks[k])
        nxt = _low(toks[k + 1]) if k + 1 < len(toks) else ""
        obj_next = (not nxt) or nxt in DETS or nxt in PREPS or _quoted(toks[k + 1]) or nxt in PRONOUNS
        if k == 1 and t0 in DEMONSTRATIVE and not w.endswith("'s"):
            if mode == "do" and w in VERBS and obj_next:          # "Does this mention a price?"
                return 1
            if mode != "do" and _pred_start(w) and not _head(w):  # "Is this hateful?"
                return 1
        if k >= 2 and mode == "do" and w in VERBS and nxt not in VERBS:  # "Does the bank mention ..."
            return k
        if _head(w) and not w.endswith("'s") and not (nxt.endswith("'s") and nxt[:1] not in "'\"“‘"):
            end = k + 1
            while end < len(toks) - 1 and _head(_low(toks[end])) and not (
                    mode == "do" and _low(toks[end]) in VERBS and _low(toks[end + 1]) not in VERBS):
                end += 1
            return _extend_pp(toks, end, mode)
        if w.endswith("'s") or w.endswith("s'"):
            k += 1
            continue
        if k >= 2 and mode != "do" and _pred_start(w):
            return k
        k += 1
    if t0 in DEMONSTRATIVE:
        return 1
    if mode == "do" and len(toks) >= 3:
        return 2  # "Does the <noun> <verb> ..." (most common shape); marked as a guess by the caller
    return None


def _extend_pp(toks, end, mode):
    """Optionally extend a subject through a prepositional chain ('the sentiment of the review', 'the claim about X')
    when what remains still starts like a predicate (be) or a verb (do)."""
    best, cur = end, end
    for _ in range(3):
        if cur + 1 >= len(toks) or _low(toks[cur]) not in PREPS:
            break
        rest = toks[cur + 1:]
        sub = _scan_np(rest, mode) if (_low(rest[0]) in DETS or _low(rest[0]) in PRONOUNS or _quoted(rest[0])
                                        or rest[0][:1].isupper()) else _bare_np(rest)
        if not sub:
            break
        cur = cur + 1 + sub
        remaining = toks[cur:]
        if not remaining:
            break
        r0 = _low(remaining[0])
        if r0 in ("or", "and", "than"):
            break
        ok = (r0 in VERBS or r0 == "not") if mode == "do" else (_pred_start(r0) and r0 not in PREPS)
        if ok:
            best = cur
    return best


def _third_person(v):
    if v in ("have",):
        return "has"
    if v in ("do", "go"):
        return v + "es"
    if re.search(r"(s|x|z|ch|sh)$", v):
        return v + "es"
    if re.search(r"[^aeiou]y$", v):
        return v[:-1] + "ies"
    return v + "s"


def _past(v):
    """Simple past, or None when a regular form is unsafe (then emphatic 'did <v>' is used)."""
    if v in IRREG_PAST:
        return IRREG_PAST[v]
    if v.endswith("e"):
        return v + "d"
    if re.search(r"[^aeiou]y$", v):
        return v[:-1] + "ied"
    if re.search(r"[^aeiou][aeiou][^aeiouwxy]$", v):
        return None  # doubling is stress-dependent (stop/stopped vs happen/happened)
    return v + "ed"


def _is_plural_subj(subj):
    w = _low(subj.split()[0])
    return w in ("these", "those", "they", "we", "you", "both", "all", "two", "three") or \
        (w in ("the", "some", "any", "their", "its", "his", "her", "our", "my", "your") and
         _low(subj.split()[-1]).endswith("s") and not _low(subj.split()[-1]).endswith(("ss", "'s", "news")))


def _lower_first(s):
    w = s.split(" ", 1)[0]
    if w in ("I",) or (len(w) > 1 and (w.isupper() or w[1:].lower() != w[1:])):
        return s
    return s[:1].lower() + s[1:]


def _cap(s):
    for i, ch in enumerate(s):
        if ch.isalpha():
            return s[:i] + ch.upper() + s[i + 1:]
    return s


def negate_declarative(x):
    """Clause negation of a declarative sentence: insert 'not' after its first auxiliary, else 'it is not the case that'."""
    toks = x.split()
    for i, t in enumerate(toks[:12]):
        w = t.lower()
        if i == 0 or w in ("that", "which", "who", "if", "when", "whether", "because", "while", "although"):
            if w in ("that", "which", "who", "if", "when", "whether", "because", "while", "although"):
                break
            continue
        if i + 1 < len(toks) and toks[i + 1].lower() in ("not", "never"):
            break
        if w in BE or w in ("has", "have", "had", "will", "would", "could"):
            return " ".join(toks[:i + 1] + ["not"] + toks[i + 1:])
        if w == "can":
            return " ".join(toks[:i] + ["cannot"] + toks[i + 1:])
    return f"it is not the case that {x}"


def question_to_prop(q, rng=None):
    """'Is this message hateful?' -> ('this message is hateful', 'this message is not hateful', info).
    info = {'shape': ..., 'subj': ..., 'neg_form': 'clausal'|'affixal'|'case'|'reply'}."""
    rng = rng or random.Random(SEED)
    q0 = re.sub(r"\s+", " ", q).strip()
    body = q0[:-1].strip() if q0.endswith("?") else None
    fb = (f'the correct reply to "{q0}" is yes', f'the correct reply to "{q0}" is no',
          {"shape": "fallback", "subj": "", "neg_form": "reply"})
    if not body or "?" in body or "n't" in body.lower() or re.search(r"\bor (not|no)\b", body, re.I):
        return fb
    scope = ""
    m = _SCOPE.match(body)
    if m and m.group(2).split(" ", 1)[0].lower() in AUX:
        scope, body = _lower_first(m.group(1)) + ", ", _cap(m.group(2))
    m = _HEDGE.match(body)
    if m:
        x = _lower_first(m.group(1))
        return scope + x, scope + negate_declarative(x), {"shape": "that_clause", "subj": "", "neg_form": "case"}
    toks = _TOK.findall(body)
    if len(toks) < 2:
        return fb
    aux = toks[0].lower()
    if aux not in AUX:
        return fb
    rest = toks[1:]
    mode = "be" if aux in BE else "do" if aux in DO else "aux"
    k = _scan_np(rest, mode)
    if not k or k >= len(rest):
        if mode == "be" and _low(rest[0]) in DEMONSTRATIVE and len(rest) > 1:
            k = 1
        else:
            return fb
    subj_t, pred_t = rest[:k], rest[k:]
    subj = " ".join(subj_t)
    if _low(subj_t[0]) in DETS | PRONOUNS:
        subj = _lower_first(subj)
    shape = f"{mode}:{aux}"
    if mode == "do" and k == 2 and not _head(_low(subj_t[-1])) and _low(pred_t[0]) not in VERBS:
        shape += ":guess"
    pred = " ".join(pred_t)
    info = {"shape": shape, "subj": subj, "neg_form": "clausal"}
    head = _low(subj_t[-1]).rstrip("s")
    info["self_ref"] = head in SELF_REF or any(_low(t).rstrip("s") in SELF_REF for t in subj_t)
    if mode == "be":
        if subj.lower() == "there" and _low(pred_t[0]) != "not":
            p0 = _low(pred_t[0])
            p = f"there {aux} {_depolarize(pred)}"
            if p0 in ("a", "an", "any", "some"):
                n = f"there {aux} no {' '.join(pred_t[1:])}"
            elif p0 in DETS or _quoted(pred_t[0]):
                n = f"there {aux} not {pred}"
            else:
                n = f"there {aux} no {pred}"
        elif _low(pred_t[0]) == "not":
            p, n = f"{subj} {aux} {pred}", f"{subj} {aux} {' '.join(pred_t[1:])}"
        else:
            p = f"{subj} {aux} {_depolarize(pred)}"
            a = AFFIX.get(_low(pred_t[0]))
            if a and pred_t[0] == _low(pred_t[0]) and rng.random() < 0.5:
                n = f"{subj} {aux} {' '.join([a] + pred_t[1:])}"
                info["neg_form"] = "affixal"
            else:
                n = f"{subj} {aux} not {pred}"
    elif mode == "do":
        verb, vrest = _low(pred_t[0]), pred_t[1:]
        if verb in PREPS or verb in DETS or _quoted(pred_t[0]) or (verb not in VERBS and verb != "not" and _pred_start(verb)):
            return fb  # the subject was mis-segmented; never emit an ungrammatical clause
        tail = (" " + " ".join(vrest)) if vrest else ""
        if verb == "not":
            if not vrest:
                return fb
            v2, tail2 = _low(vrest[0]), (" " + " ".join(vrest[1:])) if len(vrest) > 1 else ""
            p = f"{subj} {aux} not {v2}{tail2}"
            n = f"{subj} {_decl_do(aux, v2, subj)}{_depolarize(tail2)}"
        else:
            if not re.fullmatch(r"[a-z]+", verb):
                return fb
            p = f"{subj} {_decl_do(aux, verb, subj)}{_depolarize(tail)}"
            n = f"{subj} {aux} not {verb}{tail}"
    else:
        if _low(pred_t[0]) == "not":
            p, n = f"{subj} {aux} {pred}", f"{subj} {aux} {' '.join(pred_t[1:])}"
        else:
            p = f"{subj} {aux} {_depolarize(pred)}"
            if aux in MODAL_NEG:
                n = f"{subj} {MODAL_NEG[aux]} {pred}"
            elif aux in HAVE:
                n = f"{subj} {aux} not {pred}"
            else:
                n = f"it is not the case that {p}"
                info["neg_form"] = "case"
    return scope + p, scope + n, info


def _decl_do(aux, verb, subj):
    if aux == "does":
        return _third_person(verb)
    if aux == "do":
        return verb
    pv = _past(verb)
    return pv if pv else f"did {verb}"


# ============================================================================ instruction splitting
_Q_START = re.compile(r"(?:(?<=[.!:;])\s+|^)(?=(?:%s)\b)" % "|".join(sorted((a.capitalize() for a in AUX), key=len, reverse=True)))


def split_instruction(ins):
    """-> (pre, question, post, dropped): question = the last polar question (a sentence starting with an auxiliary and
    ending with '?'); pre/post = surrounding text kept verbatim, except yes/no answer directives, which are dropped
    (a directive such as 'Answer yes if ...' would contradict a negated wording)."""
    s = ins.strip()
    dropped = []
    # sentence pieces with their separators
    pieces = re.split(r"(\n+|(?<=[.!?])\s+)", s)
    sents, seps = pieces[0::2], pieces[1::2] + [""]
    keep = []
    for sent, sep in zip(sents, seps):
        if _YN_DIRECTIVE.search(sent) and not sent.rstrip().endswith("?"):
            dropped.append(sent)
            continue
        m = re.match(r"^(answer (?:with )?(?:yes or no|yes/no)[^:]*:)\s*(.+)$", sent, re.I)
        if m:
            dropped.append(m.group(1))
            sent = _cap(m.group(2))
        keep.append((sent, sep))
    qi = None
    for i in range(len(keep) - 1, -1, -1):
        sent = keep[i][0].strip()
        if sent.endswith("?"):
            # the question may follow a colon/definition inside the same sentence piece
            mm = list(_Q_START.finditer(sent))
            sm = _SCOPE.match(sent[:-1])
            if mm or (sm and sm.group(2).split(" ", 1)[0].lower() in AUX):
                qi = i
                break
    if qi is None:
        pre = "".join(a + b for a, b in keep).strip()
        return "", pre, "", dropped
    sent = keep[qi][0].strip()
    mm = list(_Q_START.finditer(sent))
    sm = _SCOPE.match(sent[:-1])
    cut = 0 if (sm and sm.group(2).split(" ", 1)[0].lower() in AUX) or not mm else mm[-1].start()
    lead, qtxt = sent[:cut].rstrip(), sent[cut:].strip()
    pre = "".join(a + b for a, b in keep[:qi]) + lead
    post = "".join(a + b for a, b in keep[qi + 1:])
    return pre.rstrip(), qtxt, post.strip(), dropped


def _join(pre, mid, post):
    out = mid
    if pre:
        out = pre + ("\n" if "\n" in pre or len(pre) > 200 else " ") + out
    if post:
        out = out + " " + post
    return out


# ============================================================================ variants
def _rng(*parts):
    h = hashlib.sha256(":".join([str(SEED), *map(str, parts)]).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def _std(p):
    """Standalone-sentence form: demonstrative subject -> 'the' (avoids self-reference inside 'Consider the statement: ...')."""
    return re.sub(r"^(this|that)\b", "the", re.sub(r"^(these|those)\b", "the", p))


def _fill(tpl, x):
    return tpl.format(p=x, P=_cap(_std(x)))


def _end_weight(tpl):
    """True when the proposition slot closes its clause (standalone {P}, or '{p}' followed by ?/./,/;), i.e. a long
    proposition is not centre-embedded before the matrix verb ('Would a bet that <40 words> be lost?')."""
    if "{P}" in tpl:
        return True
    tail = tpl.split("{p}", 1)[1].strip()
    return tail in ("?", ".") or tail[:1] in ".,;"


LONG_PROP = 12  # words


def _pick(r, pool, info, x):
    ok = [t for t in pool if not ("{P}" in t[1] and info.get("self_ref"))]
    if len(x.split()) > LONG_PROP:
        ok = [t for t in ok if _end_weight(t[1])]
    return r.choice(ok or pool)


def _variant_rows(base, pre, post, p, n, info, dropped):
    """neg / dneg / para rows (+ relations) for one yes/no base row."""
    r = _rng("ohs-variants", base["id"])
    out, rels = [], []
    g = int(base["gold"])
    specs = []
    if r.random() < 0.5:
        tid, t = _pick(r, NEG_T, info, p)
        specs.append(("neg", 1 - g, tid, _fill(t, p), "template_neg"))
    else:
        tid, t = _pick(r, AFF_T, info, n)
        specs.append(("neg", 1 - g, tid, _fill(t, n), f"clause_neg:{info['neg_form']}"))
    if r.random() < 0.5:
        tid, t = _pick(r, DNEG_T, info, p)
        specs.append(("dneg", g, tid, _fill(t, p), "lexical_dneg"))
    else:
        tid, t = _pick(r, NEG_T, info, n)
        specs.append(("dneg", g, tid, _fill(t, n), f"template_neg_x_clause_neg:{info['neg_form']}"))
    tid, t = _pick(r, PARA_T, info, p)
    specs.append(("para", g, tid, _fill(t, p), "para"))
    for role, gold, tid, txt, kind in specs:
        row = {k: base[k] for k in ("group_id", "call_id", "split", "track", "source", "state")}
        row.update({"id": f"{base['id']}_{role}", "qtype": "noul", "instructions": _join(pre, txt, post),
                    "options": None, "gold": gold, "role": role})
        if base.get("card"):
            row["card"] = base["card"]
        row["meta"] = {**(base.get("meta") or {}), "variant_of": base["id"], "variant_kind": kind, "template_id": tid,
                       "prop_shape": info["shape"], "prop": p}
        if dropped:
            row["meta"]["dropped_directive"] = dropped
        out.append(row)
        rels.append({"type": "complement" if role == "neg" else "equiv", "a": base["id"], "b": row["id"], "track": "OHS"})
    return out, rels


def _yn_from_choice(row, target):
    opts = row["options"]
    listed = len(opts) <= 30
    pre = f"Question: {row['instructions'].strip()}"
    if listed:
        pre += "\nOptions: " + "; ".join(f"'{o}'" for o in opts)
    q = f"Is the correct answer '{target}'?"
    base = {k: row[k] for k in ("group_id", "call_id", "split", "track", "source", "state")}
    base.update({"id": f"{row['id']}_yn", "qtype": "noul", "instructions": pre + "\n" + q, "options": None,
                 "gold": int(target == row["gold"]), "role": "aff"})
    if row.get("card"):
        base["card"] = row["card"]
    base["meta"] = {**(row.get("meta") or {}), "from_choice": row["id"], "target": target,
                    "target_is_gold": target == row["gold"], "options_listed": listed, "n_options": len(opts)}
    p, n = f"the correct answer is '{target}'", f"the correct answer is not '{target}'"
    return base, pre, p, n, {"shape": "choice_yn", "subj": "the correct answer", "neg_form": "clausal", "self_ref": False}


def make_variants(rows):
    """rows: OHS rows (any mix). Returns (new_rows, relations); input rows are not repeated in new_rows."""
    new_rows, rels = [], []
    # choice rows -> yes/no base: exactly 50/50 gold vs distractor per source (seeded order), distractor seeded per row
    by_src = {}
    for x in rows:
        if x.get("qtype") == "choice" and x.get("options") and len(x["options"]) >= 2:
            by_src.setdefault(x["source"], []).append(x)
    for src in sorted(by_src):
        items = sorted(by_src[src], key=lambda x: hashlib.sha256(f"{SEED}:{x['id']}".encode()).hexdigest())
        for i, x in enumerate(items):
            rr = _rng("ohs-yn", x["id"])
            others = [o for o in x["options"] if o != x["gold"]]
            target = x["gold"] if (i % 2 == 0 or not others) else rr.choice(others)
            base, pre, p, n, info = _yn_from_choice(x, target)
            new_rows.append(base)
            vr, vl = _variant_rows(base, pre, "", p, n, info, [])
            new_rows += vr
            rels += vl
    for x in rows:
        if x.get("qtype") == "noul" and x.get("role") == "aff":
            pre, q, post, dropped = split_instruction(x["instructions"])
            p, n, info = question_to_prop(q, _rng("ohs-affix", x["id"]))
            vr, vl = _variant_rows(x, pre, post, p, n, info, dropped)
            new_rows += vr
            rels += vl
    ids = [r["id"] for r in rows] + [r["id"] for r in new_rows]
    assert len(ids) == len(set(ids)), "variant id collision"
    return new_rows, rels


# ============================================================================ audit + self-test
def audit_data(k=6):
    """6-word runs of every template's fixed fragments vs every instruction string in lean/data/*.jsonl."""
    ins = set()
    for f in sorted((LEAN / "data").glob("*.jsonl")):
        if "relations" in f.name:
            continue
        for line in open(f, encoding="utf-8"):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if isinstance(r, dict) and isinstance(r.get("instructions"), str):
                ins.add(r["instructions"])
    grams = set()
    for s in ins:
        grams |= _grams(_words(s), k)
    hits = []
    for tid, t in _ALL_TEMPLATES:
        for frag in _SLOT.split(t):
            h = _grams(_words(frag), k) & grams
            if h:
                hits.append((tid, " ".join(sorted(h)[0])))
    return len(ins), hits


if __name__ == "__main__":
    print(f"collected {len(COLLECTED_TEMPLATES)} existing template/question strings "
          f"({len(EXISTING_STRINGS)} string literals scanned); novelty check passed")
    n_ins, hits = audit_data()
    print(f"audit vs {n_ins} distinct train/dev/eval instruction strings in lean/data: {len(hits)} 6-word overlaps {hits}")
    assert not hits
    SHAPES = ["Is this statement true?", "Is this message hateful?", "Is the correct answer 'B'?",
              "Does the statement follow from the passage?", "Is this spam?", "Is the sentiment of the review positive?",
              "Are the two sentences paraphrases of each other?", "Does the text contain hate speech?",
              "Is the claim supported by the evidence?", "Did the author make a claim?", "Can the question be answered from the passage?",
              "Is there hearsay?", "Is it true that the court ruled for the plaintiff?", "Is the tweet about sports?",
              "Is the claim about vaccines true?", "Does the clause not limit liability?", "Should the ticket be escalated?",
              "Based on the abstract, does the study report a benefit?", "Is this review in English?",
              "Do the sentences mean the same thing?", "Is the hypothesis entailed by the premise?", "Classify the text.",
              "Are there any errors in the proof?", "Is the email from the bank spam?", "Is this post news?",
              "Is the review about the hotel positive?", "Does the email from the bank mention a password?",
              "Is the author\u2019s claim supported?", "Is the article about renewable energy?", "Does this mention a price?",
              "Is it sarcastic?", "Isn't this rude?", "Is this comment toxic or not?",
              "Is the correct answer 'Children's rights'?", "Is the label 'not spam'?", "Has the defendant waived the right?"]
    for q in SHAPES:
        p, n, info = question_to_prop(q)
        print(f"  {q!r:58} p={p!r}  n={n!r}  [{info['shape']}, {info['neg_form']}]")
    try:  # the checker must catch a known near-copy ("be right to say that {p}" is a train wording's 6-word run)
        check_novelty([("X", "Would you be right to say that {p}?")], EXISTING_STRINGS)
        raise SystemExit("novelty checker failed to flag a planted collision")
    except AssertionError:
        print("planted-collision check: flagged as expected")
    for q in ["Hearsay is an out-of-court statement. Is there hearsay?", "Answer yes or no: is this message hateful?",
              "Read the abstract. Based on the abstract, does the study report a benefit? Answer Yes or No."]:
        print("  split:", split_instruction(q))
    fake = [
        {"id": "r_ohs_test_0001", "group_id": "g:ohs:test:1", "call_id": "c_ohs_test_0001", "split": "ohs", "track": "T",
         "source": "fake_facts", "state": "Statement:\nWater boils at 100 degrees Celsius at sea level.", "qtype": "noul",
         "instructions": "Is this statement true?", "options": None, "gold": 1, "role": "aff", "meta": {}},
        {"id": "r_ohs_test_0002", "group_id": "g:ohs:test:2", "call_id": "c_ohs_test_0002", "split": "ohs", "track": "T",
         "source": "fake_hate", "state": "Message:\nI really enjoyed the concert last night.", "qtype": "noul",
         "instructions": "Hate speech is abusive language aimed at a protected group. Is this message hateful? Answer yes or no.",
         "options": None, "gold": 0, "role": "aff", "meta": {}},
        {"id": "r_ohs_test_0003", "group_id": "g:ohs:test:3", "call_id": "c_ohs_test_0003", "split": "ohs", "track": "T",
         "source": "fake_topic", "state": "Abstract:\nWe train a transformer to translate English into French.", "qtype": "choice",
         "instructions": "Which arXiv category is the primary subject of this paper?", "options": ["cs.CL", "cs.CV", "math.PR"],
         "gold": "cs.CL", "role": "choice", "card": "- cs.CL: Computation and Language", "meta": {}},
    ]
    new, rel = make_variants(fake)
    assert make_variants(fake) == (new, rel), "not deterministic"
    for x in new:
        print(json.dumps({k: x[k] for k in ("id", "role", "gold", "instructions")}, ensure_ascii=False))
    for x in rel:
        print(json.dumps(x))
    print({k: len(v) for k, v in ALL_T.items()})
