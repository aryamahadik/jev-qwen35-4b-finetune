"""GEN solver B, ARITH sub-block (AR-F1, AR-F2, AR-F3).

Method (G0-lite section 2, solver B column): exact rational evaluation with fractions.Fraction, written from the schema alone,
plus a unit-dimension checker; any non-terminating or negative intermediate = Reject. Standard library only.

Wording: B's lexicon (PATTERNS below) holds the sentence frames B knows. A sentence it does not know raises ParseFail; B never guesses.
When the wording pool changes, `lexicon_templates()` lists what must stay readable (see tests/test_pool_conformance in the harness).
"""
import re
from fractions import Fraction

from b_questions import read_question
from bcommon import (ParseFail, Reject, statements, name_list, fnum, is_terminating, numstr, round_half_up, floor_fr, ceil_fr,
                     pick_unique, norm_text, scene_and_body, split_sentences, strip_item_markers, is_filler)

NAME = r"[A-Za-z][A-Za-z0-9_]*"
NUM = r"\d+(?:\.\d+)?"
WORD = r"[A-Za-z]+"

# ---------------------------------------------------------------------------------------------------------------------
# units

UNIT_FACTOR = {   # (family, factor to the family base)
    "gram": ("mass", 1), "kilogram": ("mass", 1000),
    "metre": ("length", 1), "kilometre": ("length", 1000),
    "second": ("time", 1), "minute": ("time", 60), "hour": ("time", 3600), "day": ("time", 86400), "week": ("time", 604800),
    "litre": ("volume", 1),
}


class Unit(object):
    """('known', name) or ('count', noun)."""
    __slots__ = ("kind", "name")

    def __init__(self, kind, name):
        self.kind = kind
        self.name = name

    def __eq__(self, o):
        return isinstance(o, Unit) and self.kind == o.kind and self.name == o.name

    def __ne__(self, o):
        return not self == o

    def __hash__(self):
        return hash((self.kind, self.name))

    def __repr__(self):
        return "Unit(%s:%s)" % (self.kind, self.name)

    def code(self):
        return self.name if self.kind == "known" else "count"


def read_unit(word, qty=None, noun_hint=None):
    w = word.lower()
    if w in UNIT_FACTOR:
        return Unit("known", w)
    if w.endswith("s") and w[:-1] in UNIT_FACTOR:
        return Unit("known", w[:-1])
    if noun_hint and (w == noun_hint or w == noun_hint + "s"):
        return Unit("count", noun_hint)
    if w.endswith("s") and (qty is None or qty != 1):
        return Unit("count", w[:-1])
    return Unit("count", w)


def convert(value, src, dst):
    if src == dst:
        return value
    if src.kind != "known" or dst.kind != "known":
        raise Reject("unit_conversion_not_allowed", "%r->%r" % (src, dst))
    fs, ks = UNIT_FACTOR[src.name]
    fd, kd = UNIT_FACTOR[dst.name]
    if fs != fd:
        raise Reject("unit_family_mismatch", "%s->%s" % (src.name, dst.name))
    return value * Fraction(ks, kd)


# ---------------------------------------------------------------------------------------------------------------------
# sentence lexicon

ROUND_CODES = (("nearest whole number", "nearest_int"), ("one decimal place", "one_dp"), ("down to a whole number", "floor_int"),
               ("up to a whole number", "ceil_int"))


def round_code(text):
    t = text.lower()
    for key, code in ROUND_CODES:
        if key in t:
            return code
    raise ParseFail("unknown_round_rule", text)


def apply_round(code, x):
    if code == "nearest_int":
        return round_half_up(x, 0)
    if code == "one_dp":
        return round_half_up(x, 1)
    if code == "floor_int":
        return Fraction(floor_fr(x))
    if code == "ceil_int":
        return Fraction(ceil_fr(x))
    raise ParseFail("unknown_round_code", code)


def _args(s):
    names = name_list(s)
    for n in names:
        if not re.match("^" + NAME + "$", n):
            raise ParseFail("bad_arg_list", s)
    return names


def _difference(m):
    a, b, first, out = m.group(1), m.group(2), m.group(3), m.group(4)
    if first not in (a, b):
        raise ParseFail("difference_first_operand", m.group(0))
    return _mk("sub", out, [first, b if first == a else a])


def _mk(op, out, args, param=None):
    return {"op": op, "out": out, "args": args, "param": param}


def _pn(x):
    f = fnum(x)
    return int(f) if f.denominator == 1 else f


# (regex, builder). Builders receive the match object and return a step dict.
PATTERNS = [
    # percent
    (r"^(%s) equals (%s) percent of (%s)$" % (NAME, NUM, NAME), lambda m: _mk("pct", m.group(1), [m.group(3)], _pn(m.group(2)))),
    (r"^Take (%s) percent of (%s); call it (%s)$" % (NUM, NAME, NAME), lambda m: _mk("pct", m.group(3), [m.group(2)], _pn(m.group(1)))),
    (r"^(%s) is the (%s) percent share of (%s)$" % (NAME, NUM, NAME), lambda m: _mk("pct", m.group(1), [m.group(3)], _pn(m.group(2)))),
    (r"^(%s) is (%s) percent of (%s)$" % (NAME, NUM, NAME), lambda m: _mk("pct", m.group(1), [m.group(3)], _pn(m.group(2)))),
    # multiply
    (r"^(%s) equals (%s) times (%s)$" % (NAME, NUM, NAME), lambda m: _mk("mul", m.group(1), [m.group(3)], _pn(m.group(2)))),
    (r"^(%s) is (%s) repeated (%s) times$" % (NAME, NAME, NUM), lambda m: _mk("mul", m.group(1), [m.group(2)], _pn(m.group(3)))),
    (r"^Multiply (%s) by (%s) to get (%s)$" % (NAME, NUM, NAME), lambda m: _mk("mul", m.group(3), [m.group(1)], _pn(m.group(2)))),
    (r"^Take (%s) copies of (%s); call it (%s)$" % (NUM, NAME, NAME), lambda m: _mk("mul", m.group(3), [m.group(2)], _pn(m.group(1)))),
    # divide
    (r"^Divide (%s) by (%s) to get (%s)$" % (NAME, NUM, NAME), lambda m: _mk("div", m.group(3), [m.group(1)], _pn(m.group(2)))),
    (r"^(%s) equals (%s) split into (%s) equal parts, one part$" % (NAME, NAME, NUM), lambda m: _mk("div", m.group(1), [m.group(2)], _pn(m.group(3)))),
    (r"^One of (%s) equal parts of (%s) is (%s)$" % (NUM, NAME, NAME), lambda m: _mk("div", m.group(3), [m.group(2)], _pn(m.group(1)))),
    (r"^(%s) is (%s) shared equally among (%s)$" % (NAME, NAME, NUM), lambda m: _mk("div", m.group(1), [m.group(2)], _pn(m.group(3)))),
    # add
    (r"^Add (.+?)(?: together)? to get (%s)$" % NAME, lambda m: _mk("add", m.group(2), _args(m.group(1)))),
    (r"^Combine (.+); call the total (%s)$" % NAME, lambda m: _mk("add", m.group(2), _args(m.group(1)))),
    (r"^(%s) is the sum of (.+)$" % NAME, lambda m: _mk("add", m.group(1), _args(m.group(2)))),
    (r"^(%s) equals (.+) added together$" % NAME, lambda m: _mk("add", m.group(1), _args(m.group(2)))),
    # subtract (a minus b)
    (r"^Subtract (%s) from (%s); the result is (%s)$" % (NAME, NAME, NAME), lambda m: _mk("sub", m.group(3), [m.group(2), m.group(1)])),
    (r"^(%s) equals (%s) less (%s)$" % (NAME, NAME, NAME), lambda m: _mk("sub", m.group(1), [m.group(2), m.group(3)])),
    (r"^(%s) is (%s) minus (%s)$" % (NAME, NAME, NAME), lambda m: _mk("sub", m.group(1), [m.group(2), m.group(3)])),
    (r"^Take (%s) away from (%s) to get (%s)$" % (NAME, NAME, NAME), lambda m: _mk("sub", m.group(3), [m.group(2), m.group(1)])),
    # min / max
    (r"^Take the least of (.+); call it (%s)$" % NAME, lambda m: _mk("min", m.group(2), _args(m.group(1)))),
    (r"^(%s) equals the minimum of (.+)$" % NAME, lambda m: _mk("min", m.group(1), _args(m.group(2)))),
    (r"^(%s) is the lowest among (.+)$" % NAME, lambda m: _mk("min", m.group(1), _args(m.group(2)))),
    (r"^(%s) is the smaller of (.+)$" % NAME, lambda m: _mk("min", m.group(1), _args(m.group(2)))),
    (r"^Take the greatest of (.+); call it (%s)$" % NAME, lambda m: _mk("max", m.group(2), _args(m.group(1)))),
    (r"^(%s) equals the maximum of (.+)$" % NAME, lambda m: _mk("max", m.group(1), _args(m.group(2)))),
    (r"^(%s) is the highest among (.+)$" % NAME, lambda m: _mk("max", m.group(1), _args(m.group(2)))),
    (r"^(%s) is the larger of (.+)$" % NAME, lambda m: _mk("max", m.group(1), _args(m.group(2)))),
    # convert
    (r"^Convert (%s) to (%s); call it (%s)$" % (NAME, WORD, NAME), lambda m: _mk("conv", m.group(3), [m.group(1)], _unit_param(m.group(2)))),
    (r"^(%s) equals (%s) written in (%s)$" % (NAME, NAME, WORD), lambda m: _mk("conv", m.group(1), [m.group(2)], _unit_param(m.group(3)))),
    (r"^In (%s), (%s) becomes (%s)$" % (WORD, NAME, NAME), lambda m: _mk("conv", m.group(3), [m.group(2)], _unit_param(m.group(1)))),
    (r"^(%s) is (%s) expressed in (%s)$" % (NAME, NAME, WORD), lambda m: _mk("conv", m.group(1), [m.group(2)], _unit_param(m.group(3)))),
    # round
    (r"^Round (%s) (.+) to get (%s)$" % (NAME, NAME), lambda m: _mk("round", m.group(3), [m.group(1)], round_code(m.group(2)))),
    (r"^Rounding (%s) (.+) gives (%s)$" % (NAME, NAME), lambda m: _mk("round", m.group(3), [m.group(1)], round_code(m.group(2)))),
    (r"^(%s) equals (%s) after rounding (.+)$" % (NAME, NAME), lambda m: _mk("round", m.group(1), [m.group(2)], round_code(m.group(3)))),
    (r"^(%s) is (%s) rounded (.+)$" % (NAME, NAME), lambda m: _mk("round", m.group(1), [m.group(2)], round_code(m.group(3)))),
    # split in a ratio (single-sentence frames)
    (r"^Dividing (%s) by the ratio (\d+) to (\d+), the (first|second) part is (%s)$" % (NAME, NAME),
     lambda m: _mk("split", m.group(5), [m.group(1)], {"r": [int(m.group(2)), int(m.group(3))], "which": 0 if m.group(4) == "first" else 1})),
    (r"^(%s) is split in the ratio (\d+) to (\d+); (%s) is the (first|second) share$" % (NAME, NAME),
     lambda m: _mk("split", m.group(4), [m.group(1)], {"r": [int(m.group(2)), int(m.group(3))], "which": 0 if m.group(5) == "first" else 1})),
    (r"^(%s) is the (first|second) part when (%s) is divided (\d+) to (\d+)$" % (NAME, NAME),
     lambda m: _mk("split", m.group(1), [m.group(3)], {"r": [int(m.group(4)), int(m.group(5))], "which": 0 if m.group(2) == "first" else 1})),
    # ---- frames of the Haiku wording pool (skeptic extension 18 Oct; each one read from its English meaning) ----
    # percent
    (r"^Take (%s) percent of (%s) to get (%s)$" % (NUM, NAME, NAME), lambda m: _mk("pct", m.group(3), [m.group(2)], _pn(m.group(1)))),
    (r"^(%s) equals the (%s) percent part of (%s)$" % (NAME, NUM, NAME), lambda m: _mk("pct", m.group(1), [m.group(3)], _pn(m.group(2)))),
    (r"^Find (%s) percent of (%s); call the result (%s)$" % (NUM, NAME, NAME), lambda m: _mk("pct", m.group(3), [m.group(2)], _pn(m.group(1)))),
    (r"^Taking (%s) percent of (%s) gives (%s)$" % (NUM, NAME, NAME), lambda m: _mk("pct", m.group(3), [m.group(2)], _pn(m.group(1)))),
    (r"^The (%s) percent share of (%s) is (%s)$" % (NUM, NAME, NAME), lambda m: _mk("pct", m.group(3), [m.group(2)], _pn(m.group(1)))),
    # multiply
    (r"^(%s) is (%s) times (%s)$" % (NAME, NAME, NUM), lambda m: _mk("mul", m.group(1), [m.group(2)], _pn(m.group(3)))),
    (r"^Let (%s) be (%s) groups of (%s)$" % (NAME, NUM, NAME), lambda m: _mk("mul", m.group(1), [m.group(3)], _pn(m.group(2)))),
    (r"^(%s) equals (%s) copies of (%s)$" % (NAME, NUM, NAME), lambda m: _mk("mul", m.group(1), [m.group(3)], _pn(m.group(2)))),
    (r"^Scaling (%s) by (%s) gives (%s)$" % (NAME, NUM, NAME), lambda m: _mk("mul", m.group(3), [m.group(1)], _pn(m.group(2)))),
    (r"^Take (%s) and multiply it by (%s); the result is (%s)$" % (NAME, NUM, NAME), lambda m: _mk("mul", m.group(3), [m.group(1)], _pn(m.group(2)))),
    # divide
    (r"^(%s) is (%s) divided by (%s)$" % (NAME, NAME, NUM), lambda m: _mk("div", m.group(1), [m.group(2)], _pn(m.group(3)))),
    (r"^Share (%s) equally across (%s); each share is (%s)$" % (NAME, NUM, NAME), lambda m: _mk("div", m.group(3), [m.group(1)], _pn(m.group(2)))),
    (r"^(%s) equals (%s) over (%s)$" % (NAME, NAME, NUM), lambda m: _mk("div", m.group(1), [m.group(2)], _pn(m.group(3)))),
    (r"^Splitting (%s) into (%s) equal parts gives (%s) per part$" % (NAME, NUM, NAME), lambda m: _mk("div", m.group(3), [m.group(1)], _pn(m.group(2)))),
    (r"^One of (%s) equal shares of (%s) is (%s)$" % (NUM, NAME, NAME), lambda m: _mk("div", m.group(3), [m.group(2)], _pn(m.group(1)))),
    # add
    (r"^Let (%s) be the total of (.+)$" % NAME, lambda m: _mk("add", m.group(1), _args(m.group(2)))),
    (r"^(%s) comes from adding (.+)$" % NAME, lambda m: _mk("add", m.group(1), _args(m.group(2)))),
    (r"^Summing (.+) gives (%s)$" % NAME, lambda m: _mk("add", m.group(2), _args(m.group(1)))),
    (r"^Combine (.+) and call the total (%s)$" % NAME, lambda m: _mk("add", m.group(2), _args(m.group(1)))),
    # subtract (a minus b)
    (r"^Subtract (%s) from (%s) to get (%s)$" % (NAME, NAME, NAME), lambda m: _mk("sub", m.group(3), [m.group(2), m.group(1)])),
    (r"^Let (%s) be (%s) less (%s)$" % (NAME, NAME, NAME), lambda m: _mk("sub", m.group(1), [m.group(2), m.group(3)])),
    (r"^Taking (%s) away from (%s) leaves (%s)$" % (NAME, NAME, NAME), lambda m: _mk("sub", m.group(3), [m.group(2), m.group(1)])),
    (r"^(%s) is what remains of (%s) after (%s) is removed$" % (NAME, NAME, NAME), lambda m: _mk("sub", m.group(1), [m.group(2), m.group(3)])),
    (r"^The difference of (%s) and (%s), (%s) first, is (%s)$" % (NAME, NAME, NAME, NAME), lambda m: _difference(m)),
    # min / max
    (r"^(%s) is the smallest of (.+)$" % NAME, lambda m: _mk("min", m.group(1), _args(m.group(2)))),
    (r"^(%s) equals the least of (.+)$" % NAME, lambda m: _mk("min", m.group(1), _args(m.group(2)))),
    (r"^Take the minimum of (.+); call it (%s)$" % NAME, lambda m: _mk("min", m.group(2), _args(m.group(1)))),
    (r"^(%s) is the lowest value among (.+)$" % NAME, lambda m: _mk("min", m.group(1), _args(m.group(2)))),
    (r"^Of (.+), the smallest is (%s)$" % NAME, lambda m: _mk("min", m.group(2), _args(m.group(1)))),
    (r"^Pick the least of (.+) as (%s)$" % NAME, lambda m: _mk("min", m.group(2), _args(m.group(1)))),
    (r"^(%s) is the largest of (.+)$" % NAME, lambda m: _mk("max", m.group(1), _args(m.group(2)))),
    (r"^(%s) equals the greatest of (.+)$" % NAME, lambda m: _mk("max", m.group(1), _args(m.group(2)))),
    (r"^Take the maximum of (.+); call it (%s)$" % NAME, lambda m: _mk("max", m.group(2), _args(m.group(1)))),
    (r"^(%s) is the highest value among (.+)$" % NAME, lambda m: _mk("max", m.group(1), _args(m.group(2)))),
    (r"^Of (.+), the largest is (%s)$" % NAME, lambda m: _mk("max", m.group(2), _args(m.group(1)))),
    (r"^Pick the greatest of (.+) as (%s)$" % NAME, lambda m: _mk("max", m.group(2), _args(m.group(1)))),
    # convert
    (r"^Convert (%s) into (%s) to get (%s)$" % (NAME, WORD, NAME), lambda m: _mk("conv", m.group(3), [m.group(1)], _unit_param(m.group(2)))),
    (r"^(%s) is the same amount as (%s), written in (%s)$" % (NAME, NAME, WORD), lambda m: _mk("conv", m.group(1), [m.group(2)], _unit_param(m.group(3)))),
    (r"^Express (%s) in (%s); the figure is (%s)$" % (NAME, WORD, NAME), lambda m: _mk("conv", m.group(3), [m.group(1)], _unit_param(m.group(2)))),
    (r"^(%s) converts to (%s) (%s)$" % (NAME, NAME, WORD), lambda m: _mk("conv", m.group(2), [m.group(1)], _unit_param(m.group(3)))),
    # round
    (r"^(%s) is (%s) after rounding (.+)$" % (NAME, NAME), lambda m: _mk("round", m.group(1), [m.group(2)], round_code(m.group(3)))),
    (r"^Apply the rounding rule (.+) to (%s); the result is (%s)$" % (NAME, NAME), lambda m: _mk("round", m.group(3), [m.group(2)], round_code(m.group(1)))),
    (r"^(%s) comes from rounding (%s) (.+)$" % (NAME, NAME), lambda m: _mk("round", m.group(1), [m.group(2)], round_code(m.group(3)))),
    # split in a ratio (single-sentence frames; the ratio is "a to b" or "a:b")
    (r"^Divide (%s) in the ratio (\d+):(\d+); the (first|second) part is (%s)$" % (NAME, NAME),
     lambda m: _mk("split", m.group(5), [m.group(1)], {"r": [int(m.group(2)), int(m.group(3))], "which": 0 if m.group(4) == "first" else 1})),
    (r"^The (first|second) share of (%s), split (\d+) to (\d+), is (%s)$" % (NAME, NAME),
     lambda m: _mk("split", m.group(5), [m.group(2)], {"r": [int(m.group(3)), int(m.group(4))], "which": 0 if m.group(1) == "first" else 1})),
    (r"^(%s) is the (first|second) portion when (%s) is divided (\d+) to (\d+)$" % (NAME, NAME),
     lambda m: _mk("split", m.group(1), [m.group(3)], {"r": [int(m.group(4)), int(m.group(5))], "which": 0 if m.group(2) == "first" else 1})),
    (r"^Splitting (%s) by the ratio (\d+):(\d+) gives (%s) as the (first|second) share$" % (NAME, NAME),
     lambda m: _mk("split", m.group(4), [m.group(1)], {"r": [int(m.group(2)), int(m.group(3))], "which": 0 if m.group(5) == "first" else 1})),
    (r"^Use the ratio (\d+) to (\d+) on (%s); (%s) is the (first|second) part$" % (NAME, NAME),
     lambda m: _mk("split", m.group(4), [m.group(3)], {"r": [int(m.group(1)), int(m.group(2))], "which": 0 if m.group(5) == "first" else 1})),
]
_COMPILED = [(re.compile(p), b) for p, b in PATTERNS]

SPLIT_OPEN = re.compile(r"^Split (%s) in the ratio (\d+):(\d+)$" % NAME)
SPLIT_CLOSE = re.compile(r"^(%s) is the (first|second) share$" % NAME)
BASE_PATTERNS = [re.compile(r"^(%s) (?:equals|is|stands at|begins at) (%s) (%s)$" % (NAME, NUM, WORD)),
                 re.compile(r"^The value of (%s) is (%s) (%s)$" % (NAME, NUM, WORD)),
                 re.compile(r"^The (?:starting amount|opening figure) for (%s) is (%s) (%s)$" % (NAME, NUM, WORD)),
                 re.compile(r"^Take (%s) as (%s) (%s) to begin with$" % (NAME, NUM, WORD))]


def _unit_param(word):
    u = read_unit(word)
    if u.kind != "known":
        raise ParseFail("conversion_target_not_a_unit", word)
    return u.name


def lexicon_templates():
    return [p for p, _ in PATTERNS] + [SPLIT_OPEN.pattern, SPLIT_CLOSE.pattern] + [b.pattern for b in BASE_PATTERNS]


# ---------------------------------------------------------------------------------------------------------------------
# question frames

Q_F1 = re.compile(r"^[A-Z][a-z]+(?: out)? the final quantity (%s)$" % NAME)
Q_F2 = re.compile(r"^[A-Z][a-z]+(?: out)? whether (%s) is (at least|at most|more than|less than) (%s) (%s)$" % (NAME, NUM, WORD))
Q_F3 = re.compile(r"^[A-Z][a-z]+(?: out)? the first line that contains a mistake$")
F3_HEAD = re.compile(r"^A worked solution with (\d+) lines is shown$")
LINE_LABELS = [re.compile(p) for p in (r"^(?:Step|Line) (\d+): (.+)$", r"^Line (\d+) -> (.+)$", r"^\((\d+)\) (.+)$", r"^\[(\d+)\] (.+)$", r"^(\d+)\) (.+)$")]
CMP_CODE = {"at least": "ge", "at most": "le", "more than": "gt", "less than": "lt"}


def _parse_qty(num, word, noun_hint=None):
    v = fnum(num)
    return v, read_unit(word, v, noun_hint)


def parse_world(stmts):
    """Return (bases, steps, rest) where rest are the statements that are neither a base nor a step (question, worked lines)."""
    bases = []   # [name, value, unit]
    steps = []
    rest = []
    i = 0
    pending = None
    while i < len(stmts):
        s = stmts[i]
        i += 1
        if pending is not None:
            m = SPLIT_CLOSE.match(s)
            if not m:
                raise ParseFail("split_not_closed", s)
            a, r1, r2 = pending
            steps.append(_mk("split", m.group(1), [a], {"r": [r1, r2], "which": 0 if m.group(2) == "first" else 1}))
            pending = None
            continue
        m = SPLIT_OPEN.match(s)
        if m:
            pending = (m.group(1), int(m.group(2)), int(m.group(3)))
            continue
        done = False
        for rx, build in _COMPILED:
            m = rx.match(s)
            if m:
                steps.append(build(m))
                done = True
                break
        if done:
            continue
        for rx in BASE_PATTERNS:
            m = rx.match(s)
            if m:
                bases.append([m.group(1), m.group(2), m.group(3)])
                done = True
                break
        if done:
            continue
        rest.append(s)
    if pending is not None:
        raise ParseFail("split_not_closed", "end of text")
    return bases, steps, rest


def resolve_units(bases_raw):
    """Fix the row's count noun, then give each base a Unit."""
    plural_nouns = set()
    singular_nouns = set()
    for name, num, word in bases_raw:
        w = word.lower()
        if w in UNIT_FACTOR or (w.endswith("s") and w[:-1] in UNIT_FACTOR):
            continue
        q = fnum(num)
        if q != 1 and w.endswith("s"):
            plural_nouns.add(w[:-1])
        else:
            singular_nouns.add(w)
    nouns = plural_nouns or singular_nouns
    if len(nouns) > 1:
        raise ParseFail("several_count_nouns", sorted(nouns))
    hint = next(iter(nouns)) if nouns else None
    out = []
    for name, num, word in bases_raw:
        v = fnum(num)
        out.append((name, v, read_unit(word, v, hint)))
    return out, hint


# ---------------------------------------------------------------------------------------------------------------------
# evaluation

def op_eval(op, args_vals, args_units, param, strict=True):
    """Return (value, unit). strict: reject negative / non-terminating results."""
    u0 = args_units[0]
    if op in ("add", "sub", "min", "max"):
        for u in args_units[1:]:
            if u != u0:
                raise Reject("unit_mismatch", "%r vs %r" % (u0, u))
    if op == "add":
        v = sum(args_vals, Fraction(0))
        u = u0
    elif op == "sub":
        if len(args_vals) != 2:
            raise ParseFail("sub_arity", str(len(args_vals)))
        v = args_vals[0] - args_vals[1]
        u = u0
    elif op == "min":
        v = min(args_vals)
        u = u0
    elif op == "max":
        v = max(args_vals)
        u = u0
    elif op == "mul":
        v = args_vals[0] * Fraction(param)
        u = u0
    elif op == "div":
        if Fraction(param) == 0:
            raise Reject("divide_by_zero", "")
        v = args_vals[0] / Fraction(param)
        u = u0
    elif op == "pct":
        v = args_vals[0] * Fraction(param) / 100
        u = u0
    elif op == "split":
        r1, r2 = param["r"]
        share = (r1, r2)[param["which"]]
        v = args_vals[0] * share / (r1 + r2)
        u = u0
    elif op == "conv":
        dst = Unit("known", param)
        if u0.kind != "known":
            raise Reject("convert_count_unit", "")
        v = convert(args_vals[0], u0, dst)
        u = dst
    elif op == "round":
        v = apply_round(param, args_vals[0])
        u = u0
    else:
        raise ParseFail("unknown_op", op)
    if strict:
        if v < 0:
            raise Reject("negative_intermediate", op)
        if not is_terminating(v):
            raise Reject("non_terminating", op)
    return v, u


class World(object):
    def __init__(self, bases, steps):
        self.bases = bases           # list of (name, Fraction, Unit)
        self.steps = steps
        self.base_map = dict((b[0], b) for b in bases)
        if len(self.base_map) != len(bases):
            raise ParseFail("duplicate_base", "")
        self.step_map = {}
        for s in steps:
            if s["out"] in self.step_map or s["out"] in self.base_map:
                raise ParseFail("duplicate_name", s["out"])
            self.step_map[s["out"]] = s
        self.memo = {}

    def value(self, name, stack=()):
        if name in self.memo:
            return self.memo[name]
        if name in self.base_map:
            b = self.base_map[name]
            r = (b[1], b[2])
        elif name in self.step_map:
            if name in stack:
                raise ParseFail("cyclic_definition", name)
            s = self.step_map[name]
            vals, units = [], []
            for a in s["args"]:
                v, u = self.value(a, stack + (name,))
                vals.append(v)
                units.append(u)
            r = op_eval(s["op"], vals, units, s["param"])
        else:
            raise ParseFail("undefined_name", name)
        self.memo[name] = r
        return r


# ---------------------------------------------------------------------------------------------------------------------
# options

OPT_QTY = re.compile(r"^(-?\d+(?:\.\d+)?) ([A-Za-z]+)$")


def _pick_by_qty(options, value, unit, noun_hint):
    hits = []
    for i, o in enumerate(options):
        m = OPT_QTY.match(o.strip())
        if not m:
            raise ParseFail("option_not_a_quantity", o)
        if Fraction(m.group(1)) == value and read_unit(m.group(2), Fraction(m.group(1)), noun_hint) == unit:
            hits.append(i)
    return pick_unique(hits, "value %s %r" % (value, unit))


def _fmt_qty(value, unit, noun_hint):
    return "%s %s" % (numstr(value), unit.name if unit.kind == "known" else (noun_hint or unit.name))


# ---------------------------------------------------------------------------------------------------------------------
# main entry

def solve(form, stem, options):
    key, slots, remainder = read_question("q." + form, stem)
    stmts = statements(remainder)
    if form == "AR-F3":
        pre, lines, tail = _line_blocks(stmts)
        bases_raw, steps, rest = parse_world(pre)
    else:
        bases_raw, steps, rest = parse_world(stmts)
    if rest:
        raise ParseFail("unread_sentences", str(rest))
    bases, noun = resolve_units(bases_raw)
    if form == "AR-F1":
        return _solve_f1(bases, noun, steps, slots, options)
    if form == "AR-F2":
        return _solve_f2(bases, noun, steps, slots, options)
    if form == "AR-F3":
        return _solve_f3(bases, noun, steps, lines, tail, slots, options)
    raise ParseFail("not_an_arith_form", form)


def _parse_back_core(form, bases, noun, steps, final):
    pb = {"form": form, "count_noun": noun,
          "bases": [{"name": n, "value": numstr(v), "unit": u.code()} for n, v, u in bases],
          "steps": [{"out": s["out"], "op": s["op"], "args": list(s["args"]), "param": s["param"]} for s in steps],
          "final": final}
    return pb


def _solve_f1(bases, noun, steps, slots, options):
    final = slots["final"]
    w = World(bases, steps)
    for s in steps:   # every step must be well formed, not only the ones the final quantity needs
        w.value(s["out"])
    v, u = w.value(final)
    idx = _pick_by_qty(options, v, u, noun)
    return {"answer_index": idx, "answer_text": _fmt_qty(v, u, noun), "parse": _parse_back_core("AR-F1", bases, noun, steps, final)}


def _solve_f2(bases, noun, steps, slots, options):
    final, cmpw = slots["final"], slots["cmp"]
    thr_n, thr_u = slots["thr"].split(" ", 1)
    w = World(bases, steps)
    for s in steps:
        w.value(s["out"])
    v, u = w.value(final)
    thr = fnum(thr_n)
    tu = read_unit(thr_u, thr, noun)
    thr_in_u = convert(thr, tu, u)
    res = {"at least": v >= thr_in_u, "at most": v <= thr_in_u, "more than": v > thr_in_u, "less than": v < thr_in_u}[cmpw]
    want = "yes" if res else "no"
    idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == want], want)
    pb = _parse_back_core("AR-F2", bases, noun, steps, final)
    pb["f2"] = {"cmp": CMP_CODE[cmpw], "thr": numstr(thr)}
    return {"answer_index": idx, "answer_text": "Yes" if res else "No", "parse": pb}


# --- AR-F3 -----------------------------------------------------------------------------------------------------------

_SHARE = re.compile(r"^share (1|2) of (%s) split (\d+):(\d+)$" % NAME)
_LINE_EXPR = [
    (re.compile(r"^(%s) \* (%s)$" % (NAME, NUM)), lambda m: ("mul", [m.group(1)], _pn(m.group(2)))),
    (re.compile(r"^(%s) / (%s)$" % (NAME, NUM)), lambda m: ("div", [m.group(1)], _pn(m.group(2)))),
    (re.compile(r"^(%s)((?: \+ %s)+)$" % (NAME, NAME)), lambda m: ("add", [m.group(1)] + [x.strip() for x in m.group(2).split("+") if x.strip()], None)),
    (re.compile(r"^(%s) - (%s)$" % (NAME, NAME)), lambda m: ("sub", [m.group(1), m.group(2)], None)),
    (re.compile(r"^(%s)%% of (%s)$" % (NUM, NAME)), lambda m: ("pct", [m.group(2)], _pn(m.group(1)))),
    (re.compile(r"^min\((.+)\)$"), lambda m: ("min", [x.strip() for x in m.group(1).split(",")], None)),
    (re.compile(r"^max\((.+)\)$"), lambda m: ("max", [x.strip() for x in m.group(1).split(",")], None)),
    (re.compile(r"^(%s) in (%s)$" % (NAME, WORD)), lambda m: ("conv", [m.group(1)], _unit_param(m.group(2)))),
    (re.compile(r"^(%s) rounded (.+)$" % NAME), lambda m: ("round", [m.group(1)], round_code(m.group(2)))),
    (_SHARE, lambda m: ("split", [m.group(2)], {"r": [int(m.group(3)), int(m.group(4))], "which": int(m.group(1)) - 1})),
    (re.compile(r"^(%s)$" % NAME), lambda m: ("identity", [m.group(1)], None)),
]


def _parse_line_expr(expr):
    for rx, b in _LINE_EXPR:
        m = rx.match(expr)
        if m:
            op, args, param = b(m)
            return op, args, param
    raise ParseFail("unknown_line_expression", expr)


def _line_blocks(stmts):
    """Return (preamble statements, worked lines [(n, text)], tail statements)."""
    pre, lines, tail = [], [], []
    state = 0
    for s in stmts:
        if state == 0:
            if s.startswith("Worked solution:"):
                state = 1
                s = s[len("Worked solution:"):].strip()
                if not s:
                    continue
            else:
                pre.append(s)
                continue
        if state == 1:
            hit = None
            for rx in LINE_LABELS:
                m = rx.match(s)
                if m:
                    hit = (int(m.group(1)), m.group(2))
                    break
            if hit:
                lines.append(hit)
                continue
            state = 2
        tail.append(s)
    return pre, lines, tail


def _solve_f3(bases, noun, steps, lines, tail, slots, options):
    if not lines:
        raise ParseFail("no_worked_lines", "")
    if tail:
        raise ParseFail("unread_sentences", str(tail))
    if int(slots["n"]) != len(lines):
        raise ParseFail("line_count_differs", "%s vs %d" % (slots["n"], len(lines)))
    w = World(bases, steps)
    for s in steps:
        w.value(s["out"])
    # shown values
    shown = {}
    for name, v, u in bases:
        shown[name] = (v, u)
    parsed_lines = []
    wrong = []
    for n, text in lines:
        parts = text.split(" = ")
        if len(parts) != 3:
            raise ParseFail("line_shape", text)
        out, expr, valtxt = [p.strip() for p in parts]
        mv = re.match(r"^(%s) (%s)$" % (NUM, WORD), valtxt)
        if not mv:
            raise ParseFail("line_value_shape", valtxt)
        sval = Fraction(mv.group(1))
        sunit = read_unit(mv.group(2), sval, noun)
        op, args, param = _parse_line_expr(expr)
        if out not in w.step_map:
            raise ParseFail("line_out_not_a_step", out)
        st = w.step_map[out]
        # Only the FIRST wrong line is needed: once one is found the later lines are parsed (for the parse-back) but not evaluated, because they
        # follow through from the wrong value and may mix units.
        if not wrong:
            # 1. expression against the stated step
            same_expr = _same_expr(st, op, args, param)
            # 2. value against the stated inputs as SHOWN
            vals, units = [], []
            for a in args:
                if a not in shown:
                    raise ParseFail("line_arg_not_known_yet", a)
                vals.append(shown[a][0])
                units.append(shown[a][1])
            if op == "identity":
                ev, eu = vals[0], units[0]
            else:
                ev, eu = op_eval(op, vals, units, param, strict=False)
            same_val = (sval == ev) or ((not _two_dp(ev)) and sval == round_half_up(ev, 2))
            same_unit = (eu == sunit)
            if not (same_expr and same_val and same_unit):
                wrong.append(n)
        else:
            for a in args:
                if a not in shown:
                    raise ParseFail("line_arg_not_known_yet", a)
        shown[out] = (sval, sunit)
        # A line that shows only one operand is a SKIPPED step: its parse-back op is "skip" and its operands are the stated step's
        # operands (the line itself shows only the first one).
        parsed_lines.append({"out": out, "op": "skip" if op == "identity" else op, "args": list(st["args"]) if op == "identity" else args,
                             "param": param, "value": numstr(sval), "unit": sunit.code()})
    if not wrong:
        raise Reject("no_wrong_line", "")
    first = wrong[0]
    target = "line %d" % first
    idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == target], target)
    final = steps[-1]["out"] if steps else None
    pb = _parse_back_core("AR-F3", bases, noun, steps, final)
    pb["f3_lines"] = parsed_lines
    return {"answer_index": idx, "answer_text": "Line %d" % first, "parse": pb, "info": {"wrong_lines": wrong}}


def _two_dp(x):
    return (x * 100).denominator == 1


def _same_expr(step, op, args, param):
    if op == "identity":
        return False
    if step["op"] != op:
        return False
    if op in ("add", "min", "max"):
        if sorted(step["args"]) != sorted(args):
            return False
    else:
        if step["args"] != args:
            return False
    if op in ("mul", "div", "pct"):
        return Fraction(step["param"]) == Fraction(param)
    if op in ("conv", "round", "split"):
        return step["param"] == param
    return True
