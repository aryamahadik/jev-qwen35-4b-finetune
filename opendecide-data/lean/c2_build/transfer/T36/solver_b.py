"""transfer/T36/solver_b.py: T36 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the card (row.card on yes/no rows, the head of the instructions on choice rows: cards.split_rules) by full-text
    comparison with the card THIS module builds from its own copies of the items for the parsed range (the rules the
    range needs, the pre-release gate, "inside / outside" on yes/no rows or the resolver's pick on choice rows);
  - the declared range by this module's own readers, one per container (inline line, package.json via json.loads,
    pyproject.toml lines, lockfile lines); alternatives split at " || ", hyphen ranges at " - ", comparators at
    spaces (npm) or commas (Python style);
  - the published versions (list or table) and the version under review by regular expressions;
  - the narrative skin (Mode T) through skin.parse_skin, the question through its wording template;
  - on choice rows, every option text back to its key (a version, or "none").
solve_b(view) decides by INTERVAL SCAN: every alternative becomes one interval (lower and upper bound with inclusive
flags), plus "!=" exclusions, "==P.*" prefixes and the pre-release rule; versions are ordered by a pairwise compare
function written here (loops over numbers and tag parts, zero padding for Python style), never by sort keys; the
resolver pick sorts the listed versions newest first with that compare function and takes the first one inside.
Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import functools
import json
import re

from c2_kit import cards as C
from c2_kit import skin as K
from c2_kit import slots as S

NONE_TEXT = "None of the listed versions meets the range"
CLOSED = "The range, the listed versions and these rules are complete: nothing else changes the answer."
SCHEMA = {"PKG": ("id", ()), "PROJECT": ("name", ()), "PERSON": ("name", ()), "PROJECT_ID": ("id", ()),
          "CAND": ("id", ())}
ANSWER = {"yn_meets": lambda ok: 1 if ok else 0, "yn_double": lambda ok: 1 if ok else 0,
          "yn_outside": lambda ok: 0 if ok else 1,
          "yn_not_meets": lambda ok: 0 if ok else 1, "yn_fails": lambda ok: 0 if ok else 1}
HEAD = {"npm": "How to read this version range (npm style):",
        "pep": "How to read these version specifiers (Python packaging style):"}
ITEM = {  # solver B's own copy of the G0 v2.2 card items (section 1.2); a test checks them against the plugin's
    "npm": {
        "ver": 'A version is MAJOR.MINOR.PATCH, optionally followed by "-" and a pre-release tag such as "beta.2". '
               'Compare versions by MAJOR, then MINOR, then PATCH, each as a number.',
        "tags": 'A version with a pre-release tag comes before the same version without one. Two tags compare part by '
                'part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when '
                'all its parts match (tag parts are separated by ".").',
        "cmp": '">=V", ">V", "<=V", "<V" and "=V" compare with V; a bare "V" means "=V".',
        "caret": '"^V" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means '
                 '>=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.',
        "tilde": '"~V" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.',
        "hyphen": '"A - B" means >=A <=B.',
        "xr": '"1.4.x" means >=1.4.0 <1.5.0, and "1.x" means >=1.0.0 <2.0.0.',
        "parts": 'Parts separated by spaces must all hold.',
        "alts": '"||" separates alternatives: the range is met when one alternative is met.',
        "gate": 'A version with a pre-release tag meets an alternative only if that alternative itself writes a version '
                'with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that "^", "~" or "x" imply do not '
                'count).',
        "inout": 'A version is inside the range when it meets the range, and outside the range when it does not, even '
                 'when its numbers lie between the bounds.',
        "pick": 'The resolver installs the highest listed version that meets the range; when no listed version meets '
                'it, the resolver installs none of them.',
    },
    "pep": {
        "ver": 'A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release '
               '(aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by '
               'number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its '
               'release; a post-release comes after its release and before the next release.',
        "cmp": '">=V", ">V", "<=V", "<V", "==V" and "!=V" compare with V.',
        "wild": '"==1.4.*" holds for every version whose release starts with 1.4 (with zero padding), post-releases '
                'included; a pre-release among them still needs the pre-release rule below.',
        "compat": '"~=V" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means '
                  '>=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.',
        "comma": 'Specifiers separated by commas must all hold.',
        "gate": 'A version with a pre-release meets the specifiers only if one of them, other than a "!=" one, names a '
                'pre-release version; this holds for every set of specifiers.',
        "inout": 'The specifiers together form the range. A version is inside the range when it meets the specifiers, '
                 'and outside the range when it does not, even when its numbers lie between the bounds.',
        "pick": 'The resolver installs the highest listed version that meets the specifiers; when no listed version '
                'meets them, the resolver installs none of them.',
    },
}
ORDER = {"npm": ("ver", "tags", "cmp", "caret", "tilde", "hyphen", "xr", "parts", "alts", "gate", "inout", "pick"),
         "pep": ("ver", "cmp", "wild", "compat", "comma", "gate", "inout", "pick")}


def needed_items(eco: str, alts: list, hyphen: list, choice: bool) -> list:
    """The card items the parsed range and the question type call for (G0 v2.2 section 1.2), in card order."""
    comps = [c for alt in alts for c in alt]
    need = {"gate"}
    if eco == "npm":
        need.add("ver")
        if any(NPM_VERSION.fullmatch(c.lstrip("^~<>=")) and NPM_VERSION.fullmatch(c.lstrip("^~<>="))[4]
               for c in comps if not c.endswith("x")):
            need.add("tags")
        if any(not h and c[0] not in "^~" and not c.endswith("x") for alt, h in zip(alts, hyphen) for c in alt):
            need.add("cmp")
        if any(c.startswith("^") for c in comps):
            need.add("caret")
        if any(c.startswith("~") for c in comps):
            need.add("tilde")
        if any(hyphen):
            need.add("hyphen")
        if any(c.endswith("x") for c in comps):
            need.add("xr")
        if any(len(alt) > 1 and not h for alt, h in zip(alts, hyphen)):
            need.add("parts")
        if len(alts) > 1:
            need.add("alts")
    else:
        need.add("ver")
        if any(not c.startswith("~=") and not c.endswith(".*") for c in comps):
            need.add("cmp")
        if any(c.endswith(".*") or c.startswith("~=") for c in comps):
            need.add("wild")
        if any(c.startswith("~=") for c in comps):
            need.add("compat")
        if len(comps) > 1:
            need.add("comma")
    need.add("pick" if choice else "inout")
    return [i for i in ORDER[eco] if i in need]


def expected_card(eco: str, alts: list, hyphen: list, choice: bool) -> str:
    return "\n".join([HEAD[eco]] + ["- " + ITEM[eco][i] for i in needed_items(eco, alts, hyphen, choice)] + [CLOSED])


INLINE_RE = re.compile(r"Declared (?:range|specifiers) for (?P<pkg>\S+) in project (?P<pid>\S+) "
                       r"\((?P<style>npm style|Python packaging style)\): (?P<range>[^\n]+)")
JSON_RE = re.compile(r"package\.json of the project:\n(?P<body>\{[^\n]*\})")
TOML_RE = re.compile(r"pyproject\.toml of the project:\n\[project\]\nname = \"(?P<pid>[^\"\n]+)\"\ndependencies = \[\n"
                     r"  \"(?P<pkg>\S+) (?P<range>[^\"\n]+)\",\n\]")
LOCK_RE = re.compile(r"lockfile request for (?P<pid>\S+):\n  package: (?P<pkg>\S+)\n  wanted: (?P<range>[^\n]+)")
LIST_RE = re.compile(r"Published versions of (?P<pkg>\S+): (?P<vs>[^\n]+)")
TABLE_RE = re.compile(r"Published versions of (?P<pkg>\S+):\n\| version \|\n\|---\|\n(?P<rows>(?:\| [^\n|]+ \|\n?)+)")
CAND_RE = re.compile(r"\nVersion under review: (?P<v>\S+)")
NPM_VERSION = re.compile(r"(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*))?")
PEP_VERSION = re.compile(r"(\d+(?:\.\d+)*)(?:(a|b|rc)(\d+))?(?:\.post(\d+))?")
PHASE = {"a": 0, "b": 1, "rc": 2}


class ParseError(ValueError):
    pass


def _one(rx, text, what):
    ms = list(rx.finditer(text))
    if len(ms) != 1:
        raise ParseError(f"{len(ms)} {what}(s) in the row")
    return ms[0]


# ------------------------------------------------------------------------------------------------ parse

def _split_range(eco: str, text: str) -> tuple:
    alts, hyphen = [], []
    for part in text.split(" || ") if eco == "npm" else [text]:
        if eco == "npm" and " - " in part:
            a, b = part.split(" - ")
            alts.append([a, b])
            hyphen.append(True)
        else:
            alts.append(part.split(" ") if eco == "npm" else part.split(", "))
            hyphen.append(False)
    for alt in alts:
        for c in alt:
            S.parse("glob", c, (), "raw")
    return alts, hyphen


def parse(row: dict, ctx) -> dict:
    card, question = C.split_rules(row)
    if not card:
        raise ParseError("the row has no rules block")
    eco = {HEAD["npm"]: "npm", HEAD["pep"]: "pep"}.get(card.split("\n", 1)[0])
    if eco is None:
        raise ParseError("the card does not open with one of the two G0 headings")
    state = row["state"]
    narrative, sep, rest = state.partition("\n\n")
    if not sep:
        raise ParseError("no blank line after the narrative")
    m = INLINE_RE.match(rest)
    if m:
        if (m["style"] == "npm style") != (eco == "npm"):
            raise ParseError("range style and card disagree")
        pkg, pid, rtext = m["pkg"], m["pid"], m["range"]
    elif rest.startswith("package.json of the project:\n"):
        mm = JSON_RE.match(rest)
        obj = json.loads(mm["body"])
        (pkg, rtext), = obj["dependencies"].items()
        pid = obj["name"]
    elif rest.startswith("pyproject.toml of the project:\n"):
        mm = TOML_RE.match(rest)
        pkg, pid, rtext = mm["pkg"], mm["pid"], mm["range"]
    else:
        mm = LOCK_RE.match(rest)
        if not mm:
            raise ParseError("no range block")
        pkg, pid, rtext = mm["pkg"], mm["pid"], mm["range"]
    alts, hyphen = _split_range(eco, rtext)
    if card != expected_card(eco, alts, hyphen, row["qtype"] == "choice"):
        raise ParseError("the card is not the card of this range and question (G0 v2.2 section 1.2)")
    lm = list(LIST_RE.finditer(state))
    tm = list(TABLE_RE.finditer(state))
    if len(lm) + len(tm) != 1:
        raise ParseError("need exactly one published-version block")
    if lm:
        vs = lm[0]["vs"].split(", ")
        lpkg = lm[0]["pkg"]
    else:
        vs = [x[2:-2] for x in tm[0]["rows"].strip("\n").split("\n")]
        lpkg = tm[0]["pkg"]
    if lpkg != pkg:
        raise ParseError("the version list names another package")
    vrx = NPM_VERSION if eco == "npm" else PEP_VERSION
    if any(not vrx.fullmatch(v) for v in vs):
        raise ParseError("a listed version does not read as a version of the card's style")
    cm = list(CAND_RE.finditer(state))
    cand = cm[0]["v"] if len(cm) == 1 else None
    if len(cm) > 1:
        raise ParseError("two versions under review")
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        told = K.parse_skin(skin, narrative, SCHEMA)
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, SCHEMA)
    facts = {"PKG": pkg, "PROJECT_ID": pid, "CAND": cand}
    for k, v in list(told.items()) + list(asked.items()):
        if k in facts and facts[k] != v:
            raise ParseError(f"{k} reads {v!r} in the text but {facts[k]!r} in the blocks")
    view = {"eco": eco, "package": pkg, "project_id": pid, "alts": alts, "hyphen": hyphen, "published": vs,
            "candidate": cand, "qform": wording.qform}
    if skin.author_mode == "T":
        view.update(project=told["PROJECT"], person=told["PERSON"])
    if row["qtype"] == "choice":
        view["options"] = ["none" if t == NONE_TEXT else t for t in row["options"]]
    return view


# ------------------------------------------------------------------------------------------------ compare

def _npm(v: str):
    m = NPM_VERSION.fullmatch(v)
    if not m:
        raise ParseError(f"npm version {v!r}")
    return [int(m[1]), int(m[2]), int(m[3])], (m[4].split(".") if m[4] else [])


def _pep(v: str):
    m = PEP_VERSION.fullmatch(v)
    if not m:
        raise ParseError(f"Python version {v!r}")
    return [int(x) for x in m[1].split(".")], m[2], int(m[3] or 0), (int(m[4]) if m[4] is not None else None)


def compare(eco: str, a: str, b: str) -> int:
    """-1 / 0 / 1 by explicit loops (no sort keys)."""
    if eco == "npm":
        (ta, pa), (tb, pb) = _npm(a), _npm(b)
        for x, y in zip(ta, tb):
            if x != y:
                return -1 if x < y else 1
        if not pa and not pb:
            return 0
        if not pa or not pb:
            return 1 if not pa else -1
        for x, y in zip(pa, pb):
            if x == y:
                continue
            xd, yd = x.isdigit(), y.isdigit()
            if xd and yd:
                return -1 if int(x) < int(y) else 1
            if xd != yd:
                return -1 if xd else 1
            return -1 if x < y else 1
        return (len(pa) > len(pb)) - (len(pa) < len(pb))
    (ra, qa, na, sa), (rb, qb, nb, sb) = _pep(a), _pep(b)
    n = max(len(ra), len(rb))
    for i in range(n):
        x = ra[i] if i < len(ra) else 0
        y = rb[i] if i < len(rb) else 0
        if x != y:
            return -1 if x < y else 1

    def phase(q, s):
        if q:
            return PHASE[q]
        return 4 if s is not None else 3

    fa, fb = phase(qa, sa), phase(qb, sb)
    if fa != fb:
        return -1 if fa < fb else 1
    ea = na if qa else (sa if sa is not None else 0)
    eb = nb if qb else (sb if sb is not None else 0)
    return (ea > eb) - (ea < eb)


def _tagged(eco: str, v: str) -> bool:
    return bool(_npm(v)[1]) if eco == "npm" else _pep(v)[1] is not None


# ------------------------------------------------------------------------------------------------ intervals

def _next(trip: list, i: int) -> str:
    t = list(trip)
    t[i] += 1
    for j in range(i + 1, 3):
        t[j] = 0
    return ".".join(str(x) for x in t)


class Interval:
    def __init__(self, eco):
        self.eco = eco
        self.lo = self.hi = None
        self.lo_in = self.hi_in = True
        self.out = []            # != versions
        self.prefixes = []       # == P.* release prefixes
        self.tags = []           # npm: triples named with a tag; Python: any named pre-release

    def floor(self, v, inclusive):
        if self.lo is None or compare(self.eco, v, self.lo) > 0 or \
                (compare(self.eco, v, self.lo) == 0 and not inclusive):
            self.lo, self.lo_in = v, inclusive

    def ceil(self, v, inclusive):
        if self.hi is None or compare(self.eco, v, self.hi) < 0 or \
                (compare(self.eco, v, self.hi) == 0 and not inclusive):
            self.hi, self.hi_in = v, inclusive

    def holds(self, v) -> bool:
        if self.lo is not None:
            c = compare(self.eco, v, self.lo)
            if c < 0 or (c == 0 and not self.lo_in):
                return False
        if self.hi is not None:
            c = compare(self.eco, v, self.hi)
            if c > 0 or (c == 0 and not self.hi_in):
                return False
        if any(compare(self.eco, v, x) == 0 for x in self.out):
            return False
        for p in self.prefixes:
            rel = _pep(v)[0]
            pn = [int(x) for x in p.split(".")]
            if [rel[i] if i < len(rel) else 0 for i in range(len(pn))] != pn:
                return False
        if _tagged(self.eco, v):
            if self.eco == "npm":
                return _npm(v)[0] in self.tags
            return bool(self.tags)
        return True


def interval_of(eco: str, alt: list, hyphen: bool) -> Interval:
    iv = Interval(eco)
    if hyphen:
        iv.floor(alt[0], True)
        iv.ceil(alt[1], True)
        for v in alt:
            if _npm(v)[1]:
                iv.tags.append(_npm(v)[0])
        return iv
    for c in alt:
        if eco == "npm":
            xr = re.fullmatch(r"(\d+)\.(?:(\d+)\.)?x", c)
            if xr:
                major = int(xr[1])
                if xr[2] is None:
                    iv.floor(f"{major}.0.0", True)
                    iv.ceil(f"{major + 1}.0.0", False)
                else:
                    iv.floor(f"{major}.{xr[2]}.0", True)
                    iv.ceil(f"{major}.{int(xr[2]) + 1}.0", False)
                continue
            op = next((o for o in ("^", "~", ">=", "<=", ">", "<", "=") if c.startswith(o)), "")
            v = c[len(op):]
            trip, tag = _npm(v)
            if tag:
                iv.tags.append(trip)
            if op == "^":
                iv.floor(v, True)
                i = 0 if trip[0] else (1 if trip[1] else 2)
                iv.ceil(_next(trip, i), False)
            elif op == "~":
                iv.floor(v, True)
                iv.ceil(_next(trip, 1), False)
            elif op in ("", "="):
                iv.floor(v, True)
                iv.ceil(v, True)
            else:
                (iv.floor if op[0] == ">" else iv.ceil)(v, op.endswith("="))
            continue
        op = next(o for o in ("~=", "==", "!=", "<=", ">=", "<", ">") if c.startswith(o))
        v = c[len(op):]
        if op == "==" and v.endswith(".*"):
            iv.prefixes.append(v[:-2])
            continue
        if op != "!=" and _pep(v)[1] is not None:
            iv.tags.append(v)
        if op == "~=":
            iv.floor(v, True)
            iv.prefixes.append(".".join(str(x) for x in _pep(v)[0][:-1]))
        elif op == "==":
            iv.floor(v, True)
            iv.ceil(v, True)
        elif op == "!=":
            iv.out.append(v)
        else:
            (iv.floor if op[0] == ">" else iv.ceil)(v, op.endswith("="))
    return iv


def inside(view: dict, v: str) -> bool:
    return any(interval_of(view["eco"], alt, h).holds(v) for alt, h in zip(view["alts"], view["hyphen"]))


def solve_b(view: dict):
    if view["qform"] == "ch_pick":
        eco = view["eco"]
        order = sorted(view["published"], key=functools.cmp_to_key(lambda a, b: compare(eco, b, a)))
        for v in order:
            if inside(view, v):
                return v
        return "none"
    if view["candidate"] is None:
        raise ParseError("a yes/no row without a version under review")
    return ANSWER[view["qform"]](inside(view, view["candidate"]))
