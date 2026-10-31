"""GEN solver B: shared helpers. Python 3 standard library only. Imports NOTHING from solver A (CT-G1-B-blind).

Solver B is written from GEN/G0_LITE.md (+ the Opus addendum) and GEN/SCHEMA.md only. It is a PROGRAM (G1): it reads a row's
`stem`, `options`, `form`, `k`, `carrier` and returns (1) the answer option, (2) a parse-back object.
It never reads a row's `spec`, `label`, `answer_text`, `option_meta` or `render_map`.

Failure vocabulary (kept apart so the agreement harness can count classes):
    ParseFail   the stem text could not be read back into a world state (wording not in B's lexicon, ambiguity, broken table).
    Reject      the text parsed, but the world state breaks a G0-lite answer-uniqueness / exactness rule
                (non-terminating or negative intermediate, tie, no unique option, inconsistent logic base ...).
"""
import re
from fractions import Fraction


class ParseFail(Exception):
    def __init__(self, code, detail=""):
        Exception.__init__(self, "%s: %s" % (code, detail))
        self.code = code
        self.detail = detail


class Reject(Exception):
    def __init__(self, code, detail=""):
        Exception.__init__(self, "%s: %s" % (code, detail))
        self.code = code
        self.detail = detail


# ---------------------------------------------------------------------------------------------------------------------
# text helpers

FILLERS = [
    r"take the text literally",
    r"answer from the text alone",
    r"nothing outside the text is needed",
    r"use only the information above",
    r"assume the statements are complete",
    r"everything needed is stated",
]
_FILLER_RE = re.compile(r"^(?:" + "|".join(FILLERS) + r")$", re.I)

_SCENE_RE = re.compile(r"^Scene D(\d\d)-(\d+)\.?\s*")
_FIRST_SENTENCE_RE = re.compile(r"^([^\n]*?[.])(?:\s+|$)", re.S)
_NUM_PREFIX_RE = re.compile(r"^\s*\d+\.\s+")
_BULLET_RE = re.compile(r"^\s*-\s+")
_LEAD_LABEL_RE = re.compile(r"^(?:Record|Fact|Recorded|Observed):\s*", re.I)


def is_filler(sentence):
    return bool(_FILLER_RE.match(sentence.strip().rstrip(".").strip()))


def split_sentences(text):
    """Split on a full stop that is followed by white space or the end. Decimal points have no white space after them."""
    out = []
    for part in re.split(r"(?<=\.)\s+", text.strip()):
        part = part.strip()
        if part:
            out.append(part)
    return out


def strip_item_markers(line):
    line = _BULLET_RE.sub("", line)
    line = _NUM_PREFIX_RE.sub("", line)
    return line.strip()


def scene_and_body(stem):
    """Return (domain_id or None, remaining text). Every stem starts with ONE scene sentence that carries no data (a stem contract: scene
    sentences have no digits, braces or inner full stops). The legacy test tag "Scene D07-3." is read as the same thing. A first sentence
    with a digit or an '=' is data, not a scene: ParseFail (B never drops data silently)."""
    s = stem.lstrip()
    m = _SCENE_RE.match(s)
    if m:
        return "D" + m.group(1), s[m.end():]
    m = _FIRST_SENTENCE_RE.match(s)
    if not m:
        raise ParseFail("no_scene_sentence", s[:60])
    first = m.group(1)
    if re.search(r"[0-9=]", first):
        raise ParseFail("scene_sentence_has_data", first[:60])
    return None, s[m.end():]


def statements(stem, keep_lines=False, scene=True):
    """List of statement strings: scene tag removed, item markers (bullet / "N.") removed, leading Record:/Fact: labels removed,
    one string per sentence. Filler sentences are dropped. A trailing '.' is removed."""
    body = scene_and_body(stem)[1] if scene else stem
    out = []
    for line in body.split("\n"):
        line = line.strip()
        if not line:
            continue
        line = strip_item_markers(line)
        line = _LEAD_LABEL_RE.sub("", line)
        for sent in split_sentences(line):
            sent = _LEAD_LABEL_RE.sub("", sent).strip()
            if not sent or is_filler(sent):
                continue
            if sent.endswith("."):
                sent = sent[:-1].rstrip()
            if sent:
                out.append(sent)
    return out


# ---------------------------------------------------------------------------------------------------------------------
# numbers

_NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")


def fnum(s):
    s = s.strip()
    if not _NUM_RE.match(s):
        raise ParseFail("bad_number", s)
    return Fraction(s)


def is_terminating(fr):
    d = fr.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def numstr(fr):
    """Own canonical text of an exact number: integer, else decimal digits with trailing zeros stripped. Raises on non-terminating."""
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    if not is_terminating(fr):
        raise Reject("non_terminating", str(fr))
    neg = fr < 0
    fr = abs(fr)
    k = 0
    while (fr * 10 ** k).denominator != 1:
        k += 1
    digits = str(int(fr * 10 ** k)).rjust(k + 1, "0")
    s = digits[:-k] + "." + digits[-k:]
    s = s.rstrip("0")
    if s.endswith("."):
        s = s[:-1]
    return ("-" if neg else "") + s


def round_half_up(fr, ndigits):
    """Round a Fraction half up (away from -inf for ties on positives) to ndigits decimal places; exact."""
    scale = 10 ** ndigits
    x = Fraction(fr) * scale
    fl = x.numerator // x.denominator
    if x - fl >= Fraction(1, 2):
        fl += 1
    return Fraction(fl, scale)


def floor_fr(fr):
    return fr.numerator // fr.denominator


def ceil_fr(fr):
    return -((-fr.numerator) // fr.denominator)


# ---------------------------------------------------------------------------------------------------------------------
# option helpers

def norm_text(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def letter_of(i):
    return "ABCD"[i]


def pick_unique(indices, what):
    if len(indices) == 1:
        return indices[0]
    if not indices:
        raise Reject("no_option_matches_answer", what)
    raise Reject("several_options_match_answer", "%s: %s" % (what, indices))


def name_list(s):
    """'a', 'a and b', 'a, b and c' -> ['a','b','c']  (also accepts 'a, b, c and d')."""
    s = s.strip()
    parts = []
    for chunk in re.split(r",\s*", s):
        for p in re.split(r"\s+and\s+", chunk):
            p = p.strip()
            if p:
                parts.append(p)
    return parts


def tokens_alpha(s):
    return re.findall(r"[A-Za-z0-9_]+", s)
