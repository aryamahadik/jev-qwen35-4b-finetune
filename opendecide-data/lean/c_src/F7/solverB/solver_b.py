#!/usr/bin/env python3
"""F7 solver B (independent; G2).

Written from c_src/F7/G0_SPEC.md (frozen, sha256 in G0_FROZEN.json) sections 2-4 and 3.5 and from the rendered
row fields only. Never reads c_src/F7/gen/ or any solver A code, and never uses the row's generator meta
(structure, edge, case_features) to derive a label: meta.option_level and gold are only COMPARED at the end.

Paradigm (different from solver A's forward evaluator): parse the rendered card / instructions / state /
options back into facts and an atom-tree rubric, then a table-driven constraint enumeration: every pair
(mode level M, final level F) in K x K is tested against the declarative constraints of the mode rule
(2.4), the overrides and C13 (2.5); exactly one F must be satisfiable (block-and-recheck in table form).
"""
import csv
import io
import json
import re
import sys
from datetime import date
from fractions import Fraction

# ---------------------------------------------------------------- lexicon (spec 3.1 only)
NUM = r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?"
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
          "october", "november", "december"]
DATE_RE = (r"\d{4}-\d{2}-\d{2}|\d{1,2} (?:" + "|".join(m.capitalize() for m in MONTHS) + r") \d{4}|(?:"
           + "|".join(m.capitalize() for m in MONTHS) + r") \d{1,2}, \d{4}")
CODE = r"[A-Z]{2,4}-[A-Z0-9]{3,6}"

# comparator words -> op (C8 inclusive, C9 exclusive)
PRE_CMP = [("no fewer than", "ge"), ("no less than", "ge"), ("no more than", "le"), ("at least", "ge"),
           ("at most", "le"), ("more than", "gt"), ("fewer than", "lt"), ("less than", "lt"),
           ("exceeds", "gt"), ("above", "gt"), ("over", "gt"), ("below", "lt"), ("under", "lt"),
           ("within", "le")]
POST_CMP = [("or more", "ge"), ("or fewer", "le"), ("or less", "le")]
DATE_CMP = [("on or before", "le"), ("on or after", "ge"), ("before", "lt"), ("after", "gt")]
RANK_CMP = [("at or above", "ge"), ("at or below", "le"), ("above", "gt"), ("below", "lt")]
PRESENT_MARK = {"yes", "y", "present", "x", "true"}
ABSENT_MARK = {"no", "n", "absent", "false"}


class ParseFail(Exception):
    pass


def fnum(s):
    return Fraction(s.replace(",", ""))


def parse_date(s):
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3))).toordinal()
    m = re.fullmatch(r"(\d{1,2}) ([A-Za-z]+) (\d{4})", s)
    if m and m.group(2).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS.index(m.group(2).lower()) + 1, int(m.group(1))).toordinal()
    m = re.fullmatch(r"([A-Za-z]+) (\d{1,2}), (\d{4})", s)
    if m and m.group(1).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS.index(m.group(1).lower()) + 1, int(m.group(2))).toordinal()
    return None


def norm(s):
    """Name normal form for matching keys / terms: lower case, '_' and '-' as spaces, single spaces."""
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s.strip().strip('"').strip("'"))
    s = s.lower().replace("_", " ").replace("-", " ")
    return " ".join(s.split())


def num_unit(s):
    """'39620 dollars' -> (Fraction, 'dollars'); None if not a number(+unit)."""
    m = re.fullmatch(r"(?:(?P<cur>[$£€])\s?)?(?P<n>" + NUM + r")(?:\s*(?P<u>[^\d].*))?", s.strip())
    if not m:
        return None
    return fnum(m.group("n")), (m.group("u") or m.group("cur") or "").strip()


# ---------------------------------------------------------------- criterion grammar (2.3) -> atom tree
# node: ("and", [..]) | ("or", [..]) | ("not", node) | ("true",) | atom
# atom: ("bool", name) | ("num", name, op, Fraction, unit) | ("date", name, op, ordinal[, N])
#       | ("rank", name, op, rankname)

def parse_value_cmp(name, rest):
    """rest is what follows '<name> is ' (or the GRID cell). Returns an atom."""
    rest = rest.strip()
    for w, op in DATE_CMP:
        m = re.fullmatch(re.escape(w) + r" (" + DATE_RE + r")", rest)
        if m:
            return ("date", name, op, parse_date(m.group(1)))
    m = re.fullmatch(r"within (" + NUM + r") days of (" + DATE_RE + r")", rest)
    if m:
        return ("date", name, "within", parse_date(m.group(2)), fnum(m.group(1)))
    for w, op in PRE_CMP:
        if rest.startswith(w + " "):
            nu = num_unit(rest[len(w) + 1:])
            if nu:
                return ("num", name, op, nu[0], nu[1])
    for w, op in POST_CMP:
        if rest.endswith(" " + w):
            nu = num_unit(rest[: -len(w) - 1])
            if nu:
                return ("num", name, op, nu[0], nu[1])
    for w, op in RANK_CMP:
        if rest.startswith(w + " "):
            return ("rank", name, op, rest[len(w) + 1:].strip())
    raise ParseFail("comparator: " + rest[:40])


def parse_atom(s):
    s = " ".join(s.strip().rstrip(".").split())
    m = re.fullmatch(r"no (.+) (?:occurred|is in place)", s)
    if m:
        return ("not", ("bool", m.group(1)))
    m = re.fullmatch(r"(.+) (?:did not occur|never occurred|is not in place)", s)
    if m:
        return ("not", ("bool", m.group(1)))
    m = re.fullmatch(r"(.+) (?:occurred|is in place)", s)
    if m:
        return ("bool", m.group(1))
    m = re.fullmatch(r"(.+?) exceeds (.+)", s)
    if m:
        nu = num_unit(m.group(2))
        if nu:
            return ("num", m.group(1), "gt", nu[0], nu[1])
    m = re.match(r"(.+?) is (.+)", s)
    if m:
        return parse_value_cmp(m.group(1), m.group(2))
    raise ParseFail("atom: " + s[:50])


def split_top(s, sep=";"):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [p.strip() for p in out if p.strip()]


def partition(s, op):
    """Split an inline 'and'/'or' criterion into atoms; the partition with the most parseable parts wins."""
    pieces = s.split(" %s " % op)
    best = None

    def rec(i, acc):
        nonlocal best
        if i == len(pieces):
            if best is None or len(acc) > len(best):
                best = list(acc)
            return
        for j in range(i + 1, len(pieces) + 1):
            txt = (" %s " % op).join(pieces[i:j])
            try:
                a = parse_atom(txt)
            except ParseFail:
                continue
            acc.append(a)
            rec(j, acc)
            acc.pop()

    rec(0, [])
    return best


def parse_inline(s):
    s = s.strip()
    cands = []
    for op in ("and", "or"):
        if " %s " % op in s:
            p = partition(s, op)
            if p and len(p) > 1:
                cands.append((len(p), op, p))
    if cands:
        cands.sort(key=lambda t: -t[0])
        if len(cands) > 1 and cands[0][0] == cands[1][0]:
            raise ParseFail("ambiguous inline and/or")
        _, op, p = cands[0]
        return (op, p)
    return parse_atom(s)


def parse_part(p):
    p = p.strip()
    m = re.fullmatch(r"(all|any) of \((.*)\)", p)
    if m:
        return ("and" if m.group(1) == "all" else "or", [parse_part(x) for x in split_top(m.group(2))])
    return parse_atom(p)


def parse_crit(s):
    s = " ".join(s.strip().split())
    s = s.rstrip(".").strip()
    m = re.fullmatch(r"(all|any) of: (.*)", s)
    if m:
        parts = split_top(m.group(2))
        return ("and" if m.group(1) == "all" else "or", [parse_part(x) for x in parts])
    if " unless " in s:
        left, b = s.rsplit(" unless ", 1)
        return ("and", [parse_inline(left), ("not", parse_atom(b))])
    return parse_inline(s)


def parse_def(s, word):
    """A level's own definition text; HIGHEST 'only if' sentence is folded in as an 'and' part (C5)."""
    s = " ".join(s.strip().split())
    m = re.fullmatch(r"(.*?)\.? %s (-?\d+) applies only if (.+?)\.?" % re.escape(word), s)
    if m:
        return ("and", [parse_crit(m.group(1)), parse_atom(m.group(3))]), int(m.group(2))
    return parse_crit(s), None


def parse_range(s):
    """Band / range text (C11) -> list of (op, Fraction). Units dropped (checked elsewhere)."""
    s = " ".join(s.strip().rstrip(".").split())
    m = re.fullmatch(r"(" + NUM + r")\s?-\s?(" + NUM + r")(?: (.+))?", s)
    if m:
        return [("ge", fnum(m.group(1))), ("le", fnum(m.group(2)))], (m.group(3) or "")
    out, unit = [], ""
    for piece in s.split(" and "):
        piece = piece.strip()
        got = None
        for w, op in PRE_CMP:
            if piece.startswith(w + " "):
                nu = num_unit(piece[len(w) + 1:])
                if nu:
                    got = (op, nu[0]); unit = nu[1] or unit
                    break
        if not got:
            for w, op in POST_CMP:
                if piece.endswith(" " + w):
                    nu = num_unit(piece[: -len(w) - 1])
                    if nu:
                        got = (op, nu[0]); unit = nu[1] or unit
                        break
        if not got:
            raise ParseFail("range: " + s[:40])
        out.append(got)
    return out, unit


def in_range(bounds, v):
    for op, t in bounds:
        if not cmp(op, v, t):
            return False
    return True


def cmp(op, v, t):
    return {"ge": v >= t, "gt": v > t, "le": v <= t, "lt": v < t}[op]


# ---------------------------------------------------------------- card side (3.2 lines, 3.5 fields)
BULLET = r"^(?:[-*•|]\s*)"
LABELS = r"^\s*(?:Rule|Condition|Criterion|When it applies)\s*:\s*(.+)$"
MODE_LINES = [("Each level adds one condition.", "ladder"),
              ("Assign the highest level on this scale whose own condition is met", "highest"),
              ("Check the levels from ", "highest"),
              ("Count the listed factors present", "count"),
              ("Add the points of the listed factors present", "points"),
              ("Sum the point values of all listed factors that are present", "points"),  # C16 paraphrase (Z01)
              ("The level is the range that contains", "cut"),
              ("whose filled cells all hold", "grid")]


def unquote_lines(text):
    out = []
    for ln in (text or "").split("\n"):
        ln = ln.rstrip()
        if ln.startswith("> "):
            ln = ln[2:]
        elif ln == ">":
            ln = ""
        out.append(ln)
    return out


def scale_of(instr, options):
    m = re.search(r"Levels run from (\S+) (-?\d+) \(lowest\) to (\S+) (-?\d+) \(highest\)", instr)
    if not m:
        raise ParseFail("C17 missing")
    word, n0, ntop = m.group(1), int(m.group(2)), int(m.group(4))
    K = len(options)
    lvl = {}
    for o in options:
        mm = re.fullmatch(re.escape(word) + r" (-?\d+) - (.+)", o)
        if not mm:
            raise ParseFail("option text")
        n = int(mm.group(1))
        lvl[o] = (n - n0) if ntop > n0 else (n0 - n)
    if sorted(lvl.values()) != list(range(K)) or abs(ntop - n0) != K - 1:
        raise ParseFail("numbering")
    return word, n0, ntop, lvl


def num_to_idx(n, n0, ntop):
    return (n - n0) if ntop > n0 else (n0 - n)


def find_defs(lines, options):
    """Level definitions by option text at line start (card lines, rubric table, decision list, short card)."""
    defs = {}
    opts = sorted(options, key=len, reverse=True)
    for i, raw in enumerate(lines):
        s = raw.strip()
        s1 = re.sub(BULLET, "", s)
        s2 = re.sub(r"^\d+[.)]\s+", "", s1)
        for cand, numbered in ((s1, False), (s2, True)):
            hit = None
            for o in opts:
                if cand.startswith(o):
                    rem = cand[len(o):]
                    if rem and (rem[0].isalnum() or rem[0] in "_-"):
                        continue
                    hit = (o, rem)
                    break
            if not hit:
                continue
            o, rem = hit
            rem = rem.strip()
            rem = re.sub(r"^[:|]\s*", "", rem).strip()
            rem = rem.rstrip("|").strip()
            if not rem and not numbered:
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    mm = re.match(LABELS, lines[j])
                    if mm:
                        rem = mm.group(1).strip()
            if rem:
                if o in defs and defs[o] != rem:
                    raise ParseFail("two definitions for one level")
                defs[o] = rem
            break
    return defs


def find_grid(lines, options, word):
    """S5 levels x criteria table (fixed width with '=' rule, or pipes). -> {option: [(attr, cell)]}."""
    for i in range(len(lines) - 1):
        h, rule = lines[i], lines[i + 1]
        if re.fullmatch(r"=+(?:\s+=+)+\s*", rule or "") and h.strip().startswith(word):
            spans = [(m.start(), m.end()) for m in re.finditer(r"=+", rule)]
            starts = [a for a, _ in spans]

            def cells(ln):
                out = []
                for k, a in enumerate(starts):
                    b = starts[k + 1] if k + 1 < len(starts) else None
                    out.append((ln[a:b] if b else ln[a:]).strip())
                return out
            head = cells(h)
            grid = {}
            j = i + 2
            while j < len(lines) and lines[j].strip():
                c = cells(lines[j])
                if c[0] not in options:
                    raise ParseFail("grid row option")
                grid[c[0]] = list(zip(head[1:], c[1:]))
                j += 1
            return grid
        if h.strip().startswith("|"):
            head = [x.strip() for x in h.strip().strip("|").split("|")]
            if not head or head[0] != word:
                continue
            grid = {}
            j = i + 1
            while j < len(lines) and lines[j].strip()[:1] in ("|", "+"):
                t = lines[j].strip()
                if t.startswith("+") or re.fullmatch(r"\|?(?:\s*:?[-=]{3,}:?\s*\|)+\s*", t):
                    j += 1
                    continue
                c = [x.strip() for x in t.strip("|").split("|")]
                if c[0] not in options or len(c) != len(head):
                    raise ParseFail("grid row option")
                grid[c[0]] = list(zip(head[1:], c[1:]))
                j += 1
            return grid
    raise ParseFail("grid table missing")


def grid_atom(attr, cell):
    cell = " ".join(cell.split())
    if cell == "not required":
        return ("true",)
    if cell in ("occurred", "is in place"):
        return ("bool", attr)
    if cell in ("did not occur", "never occurred", "is not in place"):
        return ("not", ("bool", attr))
    if cell.startswith("exceeds "):
        nu = num_unit(cell[8:])
        if nu:
            return ("num", attr, "gt", nu[0], nu[1])
    return parse_value_cmp(attr, cell)


def collect_list(lines, header_re):
    """Items listed under a header line ('Listed factors:' / 'Points per listed factor:')."""
    for i, raw in enumerate(lines):
        m = re.match(header_re, raw.strip())
        if not m:
            continue
        inline = (m.group(1) or "").strip()
        if inline:
            return [x.strip() for x in re.split(r";|,(?![^()]*\))", inline) if x.strip()]
        out, mark = [], None
        j = i + 1
        while j < len(lines):
            s = lines[j].strip()
            mm = re.match(r"^([-*+\u2022]|\d+[.)])\s+(.+)$", s)
            mk = None
            if mm:
                mk = "num" if mm.group(1)[0].isdigit() else mm.group(1)
            if mm and (mark is None or mk == mark):
                mark = mk
                out.append(mm.group(2).strip())
            elif s:
                break
            elif out:
                k = j + 1
                if k < len(lines):
                    m2 = re.match(r"^\s*([-*+\u2022]|\d+[.)])\s+", lines[k])
                    if m2 and ("num" if m2.group(1)[0].isdigit() else m2.group(1)) == mark:
                        j += 1
                        continue
                break
            j += 1
        return out
    return None


def parse_card(row):
    options = row["options"]
    instr = row["instructions"] or ""
    ilines = unquote_lines(instr)
    clines = unquote_lines(row.get("card") or "")
    itext = "\n".join(ilines)
    word, n0, ntop, lvl = scale_of(itext, options)
    K = len(options)
    modes = set()
    for key, md in MODE_LINES:
        if key in itext:
            modes.add(md)
    if len(modes) != 1:
        raise ParseFail("mode lines: %s" % sorted(modes))
    mode = modes.pop()
    card = {"K": K, "word": word, "n0": n0, "ntop": ntop, "lvl": lvl, "mode": mode,
            "decision_list": "Check the levels from " in itext}
    # level definitions
    conds = {}
    if mode == "grid":
        grid = find_grid(ilines, options, word)
        for o, cells in grid.items():
            conds[lvl[o]] = ("and", [grid_atom(a, c) for a, c in cells])
    else:
        defs = find_defs(clines + [""] + ilines, options)
        for o, txt in defs.items():
            if mode in ("ladder", "highest"):
                node, oi = parse_def(txt, word)
                if oi is not None and num_to_idx(oi, n0, ntop) != lvl[o]:
                    raise ParseFail("only-if level number")
                if oi is not None and mode != "highest":
                    raise ParseFail("only-if on non-HIGHEST card")
                conds[lvl[o]] = node
            else:
                conds[lvl[o]] = parse_range(txt)
    need = set(range(K)) if mode in ("count", "points", "cut") else set(range(1, K))
    if set(conds) != need:
        raise ParseFail("definitions found for %d of %d levels" % (len(set(conds) & need), len(need)))
    card["conds"] = conds
    # overrides (C13)
    ovr = []
    for raw in ilines:
        s = re.sub(BULLET, "", raw.strip())
        m = re.fullmatch(r"If (.+), the level is at (least|most) (\S+) (-?\d+)\.", s)
        if m:
            if m.group(3) != word:
                raise ParseFail("override level word")
            ovr.append(("floor" if m.group(2) == "least" else "cap", parse_crit(m.group(1)),
                        num_to_idx(int(m.group(4)), n0, ntop)))
        m = re.fullmatch(r"When (.+), (\S+) (-?\d+) or a lower level applies\.", s)  # C13 cap paraphrase (Z01)
        if m:
            if m.group(2) != word:
                raise ParseFail("override level word")
            ovr.append(("cap", parse_crit(m.group(1)), num_to_idx(int(m.group(3)), n0, ntop)))
    kinds = sorted(k for k, _, _ in ovr)
    if kinds not in ([], ["floor"], ["cap"], ["cap", "floor"]):
        raise ParseFail("override set %s" % kinds)
    card["overrides"] = ovr
    m = re.search(r"the (minimum|maximum) wins: the level is exactly (\S+) (-?\d+)", itext)
    card["winner"] = None
    if m:
        card["winner"] = ("floor" if m.group(1) == "minimum" else "cap", num_to_idx(int(m.group(3)), n0, ntop))
    if kinds == ["cap", "floor"]:
        if not card["winner"]:
            raise ParseFail("floor+cap card without precedence line")
        mf = [x for k, _, x in ovr if k == "floor"][0]
        mc = [x for k, _, x in ovr if k == "cap"][0]
        if not mf > mc:
            raise ParseFail("floor+cap with m_f <= m_c")
        wl = mf if card["winner"][0] == "floor" else mc
        if wl != card["winner"][1]:
            raise ParseFail("precedence level differs from the winner's override level")
    # COUNT / POINTS lists
    card["listed"], card["weights"] = None, None
    if mode == "count":
        card["listed"] = collect_list(ilines, r"^Listed factors\s*:?\s*(.*)$")
        if not card["listed"]:
            raise ParseFail("listed factors missing")
    if mode == "points":
        items = collect_list(ilines, r"^Points per listed factor\s*:?\s*(.*)$")
        if not items:
            raise ParseFail("points list missing")
        w = {}
        for it in items:
            mm = re.fullmatch(r"(.+?)\s*[:=\-]\s*(\d+) points?", it) or re.fullmatch(r"(.+?) \((\d+) points?\)", it)
            if not mm:
                raise ParseFail("points item")
            w[mm.group(1).strip()] = int(mm.group(2))
        card["weights"] = w
        card["listed"] = list(w)
    card["quantity"] = None
    if mode == "cut":
        m = re.search(r"The level is the range that contains (?:the )?(.+?)\.(?:\s|$)", itext)
        card["quantity"] = m.group(1).strip()
    # aliases, ranks, second units, subject
    alias = {}
    for raw in ilines:
        m = re.fullmatch(r"(.+?) \(also written (.+?)\)", re.sub(BULLET, "", raw.strip()))
        if m:
            for a in re.split(r", | or ", m.group(2)):
                alias.setdefault(m.group(1).strip(), []).append(a.strip())
    card["alias"] = alias
    card["ranks"] = [[x.strip() for x in m.group(1).split(",")]
                     for m in re.finditer(r"Ranks from lowest to highest: (.+?)\. 'Above'", itext)]
    card["units"] = []
    for raw in ilines:
        m = re.fullmatch(r"1 (.+?) = (" + NUM + r") (.+?)\.?", raw.strip())
        if m:
            card["units"].append((m.group(1).strip(), fnum(m.group(2)), m.group(3).strip()))
    m = re.search(r"Rate only (.+?)\. Facts about other", itext)
    card["c21"] = m.group(1) if m else None
    return card


# ---------------------------------------------------------------- case side (state = case record only; L01)
FRAMES = [  # (tag, regex on the text after the entity code); order matters
    ("partial", r"partly completed (?:an? )?(?P<x>.+)"),
    ("partial", r"partially completed (?:an? )?(?P<x>.+)"),
    ("partial", r"had (?:an? )?(?P<x>.+?) occur only in part"),
    ("partial", r"had (?:an? )?(?P<x>.+?) (?:only partly|partially|only partially|partly) in place"),
    ("plan", r"plans to have (?:an? )?(?P<x>.+?)(?: in place)?"),
    ("plan", r"plans to (?:get|hold|have|complete|obtain) (?:an? )?(?P<x>.+?)(?: in place)?"),
    ("plan", r"planned (?:an? )?(?P<x>.+)"),
    ("plan", r"expects to have (?:an? )?(?P<x>.+?)(?: in place)?"),
    ("plan", r"is expected to have (?:an? )?(?P<x>.+?)(?: in place)?"),
    ("plan", r"is at risk of (?:an? )?(?P<x>.+)"),
    ("plan", r"has a risk of (?:an? )?(?P<x>.+)"),
    ("plan", r"(?:may|might) have (?:an? )?(?P<x>.+?)(?: in place)?"),
    ("plan", r"(?:may|might) have had (?:an? )?(?P<x>.+)"),
    ("plan", r"possibly had (?:an? )?(?P<x>.+)"),
    ("plan", r"requested (?:an? )?(?P<x>.+)"),
    ("neg", r"has no (?P<x>.+?) in place"),
    ("neg", r"does not have (?:an? )?(?P<x>.+?) in place"),
    ("neg", r"had no (?P<x>.+)"),
    ("neg", r"did not have (?:an? )?(?P<x>.+)"),
    ("neg", r"never had (?:an? )?(?P<x>.+)"),
    ("neg", r"failed to have (?:an? )?(?P<x>.+?)(?: in place)?"),
    ("neg", r"lacked (?:an? )?(?P<x>.+?)(?: in place)?"),
    ("aff", r"has (?:an? )?(?P<x>.+?) in place"),
    ("aff", r"had (?:an? )?(?P<x>.+)"),
]
SENT = re.compile(r"(?<![A-Za-z0-9-])(" + CODE + r") ((?:[^.\n<\"|]|\.(?=\d))*)")


def strip_val(v):
    v = v.strip()
    for _ in range(3):
        v = v.strip().rstrip(",").strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        if v.startswith("[") and v.endswith("]"):
            v = v[1:-1]
        v = v.rstrip("|").strip()
    return v.strip()


def kv_pairs(state):
    """Generic key/value extraction over every structured container (json, yaml, csv, tables, forms, html)."""
    body = "\n".join(ln for ln in state.split("\n") if not ln.strip().startswith("```"))
    pairs = []
    b = body.strip()
    if b.startswith("{"):
        try:
            obj = json.loads(b)
        except ValueError:
            obj = None
        if isinstance(obj, dict):
            def walk(d):
                for k, v in d.items():
                    if isinstance(v, dict):
                        walk(v)
                    elif isinstance(v, list):
                        for x in v:
                            if isinstance(x, dict):
                                walk(x)
                    else:
                        pairs.append((k, v))
            walk(obj)
            return pairs, True
    t = re.sub(r"<tr>\s*<th>(.*?)</th>\s*<td>(.*?)</td>\s*</tr>", r"\n\1: \2\n", body, flags=re.S)
    t = re.sub(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", r"\n\1: \2\n", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    for raw in t.split("\n"):
        s = raw.strip()
        if not s:
            continue
        s = re.sub(r"^(?:[-*•>]\s+)", "", s)
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if len(cells) == 2 and not re.fullmatch(r":?-{3,}:?", cells[0]):
                pairs.append((cells[0], cells[1]))
            continue
        if s.startswith('"') and '","' in s:
            try:
                rec = next(csv.reader(io.StringIO(s)))
                if len(rec) == 2:
                    pairs.append((rec[0], rec[1]))
                    continue
            except Exception:
                pass
        m = re.match(r"^(?P<k>[A-Za-z][A-Za-z0-9 _\-/'&()]*?)\s*(?:\.{2,}\s*|:\s*|=\s*|\|\s*|;\s*|,\s*|\t+\s*|\s{2,})(?P<v>.*)$", s)
        if m:
            pairs.append((m.group("k"), m.group("v")))
    return pairs, False


def atoms_of(node, out):
    if node[0] in ("and", "or"):
        for x in node[1]:
            atoms_of(x, out)
    elif node[0] == "not":
        atoms_of(node[1], out)
    elif node[0] != "true":
        out.append(node)
    return out


def rubric_items(card):
    """Every factor / attribute the rubric reads -> kind; plus name lookup incl. declared aliases."""
    items = {}
    nodes = []
    if card["mode"] in ("ladder", "highest", "grid"):
        nodes += list(card["conds"].values())
    nodes += [c for _, c, _ in card["overrides"]]
    for n in nodes:
        for a in atoms_of(n, []):
            k = a[0]
            if items.get(a[1], k) != k:
                raise ParseFail("item read with two kinds")
            items[a[1]] = k
    for f in card["listed"] or []:
        items.setdefault(f, "bool")
    if card["quantity"]:
        items[card["quantity"]] = "num"
    names = {}
    for it in items:
        for nm in [it] + card["alias"].get(it, []):
            if names.get(norm(nm), it) != it:
                raise ParseFail("one name for two items")
            names[norm(nm)] = it
    return items, names


def subject_code(card, state, instr):
    if card["c21"]:
        m = re.search(CODE, card["c21"])
        if m:
            return m.group(0)
    codes = []
    for m in re.finditer(r"(?<![A-Za-z0-9-])" + CODE + r"(?![A-Za-z0-9])", state):
        if m.group(0) not in codes:
            codes.append(m.group(0))
    if len(codes) == 1:
        return codes[0]
    tail = [c for c in codes if c in instr]
    if len(tail) == 1:
        return tail[0]
    raise ParseFail("subject not determined (%d codes)" % len(codes))


def parse_case(state, card, items, names, subj):
    facts = {it: set() for it in items}
    vals = {it: [] for it in items}
    probs = []
    pairs, is_json = kv_pairs(state)
    for k, v in pairs:
        it = names.get(norm(str(k)))
        if it is None:
            continue
        if items[it] == "bool":
            if isinstance(v, bool):
                facts[it].add("aff" if v else "neg")
                continue
            sv = strip_val(str(v)).lower()
            if sv in PRESENT_MARK:
                facts[it].add("aff")
            elif sv in ABSENT_MARK:
                facts[it].add("neg")
            elif sv == "":
                facts[it].add("missing")
            else:
                raise ParseFail("marker word for a listed factor")
        else:
            sv = strip_val(str(v))
            if sv == "":
                raise ParseFail("blank value for a numeric/date/rank field (K02)")
            vals[it].append(sv)
    # sentences: one entity code as grammatical subject, frame after it (3.1 fact frames)
    for m in SENT.finditer(state):
        code, rest = m.group(1), " ".join(m.group(2).split()).strip()
        if not rest:
            continue
        hit = None
        for nm, it in names.items():
            if items[it] == "bool":
                continue
            mm = re.fullmatch(r"has an? (.+) of (.+)", rest)
            if mm:
                # choose the split whose name part is this item
                parts = rest[6:] if rest.startswith("has a ") else rest[7:]
                segs = parts.split(" of ")
                for cut in range(1, len(segs)):
                    if norm(" of ".join(segs[:cut])) == nm:
                        hit = ("val", it, " of ".join(segs[cut:]))
                        break
            if hit:
                break
        if not hit:
            for tag, rx in FRAMES:
                mm = re.fullmatch(rx, rest)
                if mm and norm(mm.group("x")) in names and items[names[norm(mm.group("x"))]] == "bool":
                    hit = (tag, names[norm(mm.group("x"))], None)
                    break
        if not hit:
            # not a rubric fact; it must not name a rubric item (else the frame is outside the lexicon)
            if not re.fullmatch(r"has an? .+ of .+", rest):
                for nm, it in names.items():
                    if re.search(r"(?<![a-z])" + re.escape(nm) + r"(?![a-z])", norm(rest)):
                        probs.append("unclassified sentence names a rubric item")
                        break
            continue
        if code != subj:
            continue  # other entity (C21): never counts
        tag, it, v = hit
        if tag == "val":
            vals[it].append(v.strip())
        else:
            facts[it].add(tag)
    return facts, vals, probs, is_json


# ---------------------------------------------------------------- evaluation of atoms on the parsed facts
def unit_eq(a, b):
    a, b = norm(a), norm(b)
    return a == b or a.rstrip("s") == b.rstrip("s")


class Facts:
    def __init__(self, card, items, facts, vals):
        self.card, self.items, self.facts, self.vals = card, items, facts, vals

    def present(self, it):
        return "aff" in self.facts[it]

    def value(self, it, kind, unit=None):
        vs = self.vals.get(it) or []
        if not vs:
            raise ParseFail("no stated value for a rubric attribute")
        out = set()
        for v in vs:
            if kind == "date":
                d = parse_date(v)
                if d is None:
                    raise ParseFail("date value")
                out.add(d)
            elif kind == "rank":
                out.add(v.strip())
            else:
                nu = num_unit(v)
                if not nu:
                    raise ParseFail("numeric value")
                x, u = nu
                if unit and u and not unit_eq(u, unit):
                    conv = [c for (u2, c, u1) in self.card["units"] if unit_eq(u2, u) and unit_eq(u1, unit)]
                    if not conv:
                        raise ParseFail("unit mismatch")
                    x = x * conv[0]
                out.add(x)
        if len(out) != 1:
            raise ParseFail("two different values for one attribute")
        return out.pop()

    def rank_index(self, r):
        hits = [lst.index(r) for lst in self.card["ranks"] if r in lst]
        if len(hits) != 1:
            raise ParseFail("rank not in exactly one C25 list")
        return hits[0]

    def truth(self, node):
        t = node[0]
        if t == "true":
            return True
        if t == "and":
            return all(self.truth(x) for x in node[1])
        if t == "or":
            return any(self.truth(x) for x in node[1])
        if t == "not":
            return not self.truth(node[1])
        if t == "bool":
            return self.present(self.canon(node[1]))
        it = self.canon(node[1])
        if t == "num":
            return cmp(node[2], self.value(it, "num", node[4]), node[3])
        if t == "date":
            v = self.value(it, "date")
            if node[2] == "within":
                return node[3] <= v <= node[3] + int(node[4])
            return cmp(node[2], v, node[3])
        if t == "rank":
            return cmp(node[2], self.rank_index(self.value(it, "rank")), self.rank_index(node[3]))
        raise ParseFail("node")

    def canon(self, name):
        if name in self.items:
            return name
        raise ParseFail("unknown item")


# ---------------------------------------------------------------- declarative solve (table-driven enumeration)
def solve(card, F):
    K, mode = card["K"], card["mode"]
    conds = card["conds"]
    if mode in ("ladder", "highest", "grid"):
        c = {k: F.truth(conds[k]) for k in range(1, K)}
    elif mode in ("count", "points"):
        if mode == "count":
            q = sum(1 for f in card["listed"] if F.present(f))
        else:
            q = sum(w for f, w in card["weights"].items() if F.present(f))
        member = {k: in_range(conds[k][0], q) for k in range(K)}
    else:
        q = F.value(card["quantity"], "num")
        member = {k: in_range(conds[k][0], q) for k in range(K)}

    def mode_ok(M):
        if mode == "ladder":
            return all(c[j] for j in range(1, M + 1)) and (M == K - 1 or not c[M + 1])
        if mode in ("highest", "grid"):
            return (M == 0 or c[M]) and not any(c[j] for j in range(M + 1, K))
        return member[M]

    fire = {k: F.truth(cond) for k, cond, _ in card["overrides"]}
    lv = {k: x for k, _, x in card["overrides"]}

    def final_ok(M, Fl):
        ff, cf = fire.get("floor", False), fire.get("cap", False)
        if ff and cf:
            return Fl == card["winner"][1]
        if ff:
            return Fl >= lv["floor"] and Fl >= M and Fl in (M, lv["floor"])
        if cf:
            return Fl <= lv["cap"] and Fl <= M and Fl in (M, lv["cap"])
        return Fl == M

    Ms = [M for M in range(K) if mode_ok(M)]
    sols = sorted({Fl for M in Ms for Fl in range(K) if final_ok(M, Fl)})
    return sols, Ms


# ---------------------------------------------------------------- per row
def solve_row(row):
    card = parse_card(row)
    items, names = rubric_items(card)
    subj = subject_code(card, row["state"], row["instructions"])
    facts, vals, probs, _ = parse_case(row["state"], card, items, names, subj)
    for it, tags in facts.items():
        if "aff" in tags and tags & {"neg", "missing", "plan", "partial"}:
            probs.append("factor both affirmed and denied")
        if "missing" in tags and len(tags) > 1:
            probs.append("missing marker with another mention (A15)")
        if ("plan" in tags or "partial" in tags) and len(tags) > 1:
            probs.append("plan/partial sentence not the only statement (W04/H01)")
    F = Facts(card, items, facts, vals)
    sols, Ms = solve(card, F)
    if len(Ms) != 1:
        raise ParseFail("mode rule gives %d levels (totality / single value)" % len(Ms))
    if len(sols) != 1:
        raise ParseFail("constraint table gives %d final levels" % len(sols))
    lvl = sols[0]
    inv = {v: k for k, v in card["lvl"].items()}
    fired = sorted(k for k, c, _ in card["overrides"] if F.truth(c))
    try:
        wc = worked_cases(row, card, items, names, subj)
    except ParseFail as e:
        wc = [("?", None, "unparsed: " + str(e))]
    return {"answer": inv[lvl], "level": lvl, "option_level": card["lvl"], "mode": card["mode"],
            "fired": fired, "M": Ms[0], "probs": probs, "worked": wc}


def worked_cases(row, card, items, names, subj):
    """W08 / 4.2: every worked case in instructions, parsed like a row case; its shown level must equal solver B."""
    lines = (row["instructions"] or "").split("\n")
    opts = sorted(row["options"], key=len, reverse=True)

    def opt_in(ln):
        for o in opts:
            if re.search(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])", ln):
                return o
        return None
    codes = []
    for ln in lines:
        for m in SENT.finditer(ln):
            if m.group(1) != subj and m.group(2).strip() and m.group(1) not in codes:
                codes.append(m.group(1))
    def is_def(i):
        t = re.sub(r"^\d+[.)]\s+", "", re.sub(BULLET, "", lines[i].strip().lstrip("> ")))
        for o in opts:
            if t.startswith(o):
                rem = re.sub(r"^[\s:|]+", "", t[len(o):]).rstrip("| ").strip()
                if rem:
                    return True
                j = i + 1
                while j < len(lines) and not lines[j].strip().lstrip("> ").strip():
                    j += 1
                # quoted layouts ("> " prefix) carry the label line quoted too
                return j < len(lines) and re.match(LABELS, lines[j].strip().lstrip("> ")) is not None
        return False
    case_line = {}
    for code in codes:
        case_line[code] = [i for i, ln in enumerate(lines)
                           if re.search(r"(?<![A-Za-z0-9-])" + re.escape(code) + r" ", ln)]
    all_case = sorted(i for v in case_line.values() for i in v)
    ans = [i for i, ln in enumerate(lines) if opt_in(ln) and i not in all_case and not is_def(i)]
    before = bool(ans and all_case and ans[0] < all_case[0])
    out = []
    for code in codes:
        idx = case_line[code]
        txt = "\n".join(lines[i] for i in idx)
        shown = None
        for i in idx:
            shown = shown or opt_in(lines[i])
        if not shown:
            if before:
                prev = [i for i in ans if i < idx[0]]
                shown = opt_in(lines[prev[-1]]) if prev else None
            else:
                nxt = [i for i in ans if i > idx[-1]]
                shown = opt_in(lines[nxt[0]]) if nxt else None
        facts, vals, probs, _ = parse_case(txt, card, items, names, code)
        sols, Ms = solve(card, Facts(card, items, facts, vals))
        if len(sols) != 1 or len(Ms) != 1:
            raise ParseFail("worked case: constraint table not single-valued")
        inv = {v: k for k, v in card["lvl"].items()}
        out.append((code, shown, inv[sols[0]]))
    return out


def spec_item(res):
    it = {"ladder": "2.4 LADDER", "highest": "2.4 HIGHEST", "count": "2.4 COUNT", "points": "2.4 POINTS",
          "cut": "2.4 CUT / C11", "grid": "2.4 GRID"}[res["mode"]]
    if res["fired"]:
        it += " + 2.5 overrides (%s) / C13" % "+".join(res["fired"])
    return "4.2 G2; " + it


def run_file(path):
    out = {"rows": 0, "agree": 0, "mismatch": [], "unparsed": [], "option_level_diff": [], "probs": {},
           "worked": {"checked": 0, "agree": 0, "no_shown_level": 0, "unparsed": 0, "disagree_ids": []}}
    seen_wc = set()
    by = {}
    with open(path) as fh:
        for line in fh:
            row = json.loads(line)
            out["rows"] += 1
            smp = (row.get("meta") or {}).get("sampler", "?")
            try:
                res = solve_row(row)
            except ParseFail as e:
                out["unparsed"].append({"id": row["id"], "reason": str(e), "spec_item": "4.4 G3 parse (fail closed)"})
                by[smp + ":unparsed"] = by.get(smp + ":unparsed", 0) + 1
                continue
            except Exception as e:  # a crash is reported, never hidden
                out["unparsed"].append({"id": row["id"], "reason": "crash: %s: %s" % (type(e).__name__, str(e)[:60]),
                                        "spec_item": "4.4 G3 parse"})
                by[smp + ":unparsed"] = by.get(smp + ":unparsed", 0) + 1
                continue
            ck = (row.get("meta") or {}).get("card_id"), row["instructions"]
            if ck not in seen_wc:
                seen_wc.add(ck)
                for code, shown, got in res["worked"]:
                    w = out["worked"]
                    if isinstance(got, str) and got.startswith("unparsed"):
                        w["unparsed"] += 1
                    elif shown is None:
                        w["no_shown_level"] += 1
                    else:
                        w["checked"] += 1
                        if shown == got:
                            w["agree"] += 1
                        else:
                            w["disagree_ids"].append(row["id"])
            for p in res["probs"]:
                out["probs"][p] = out["probs"].get(p, 0) + 1
            meta_ol = (row.get("meta") or {}).get("option_level")
            if meta_ol is not None and meta_ol != res["option_level"]:
                out["option_level_diff"].append({"id": row["id"], "spec_item": "4.4 item 5 option_level"})
            if res["answer"] == row["gold"]:
                out["agree"] += 1
                by[smp + ":agree"] = by.get(smp + ":agree", 0) + 1
            else:
                gl = res["option_level"].get(row["gold"])
                out["mismatch"].append({"id": row["id"], "solver_b_level": res["level"], "gold_level": gl,
                                        "solver_b_option_index": row["options"].index(res["answer"]),
                                        "gold_option_index": row["options"].index(row["gold"]) if row["gold"] in row["options"] else None,
                                        "spec_item": spec_item(res)})
                by[smp + ":mismatch"] = by.get(smp + ":mismatch", 0) + 1
    out["by_sampler"] = by
    return out


def main():
    import hashlib
    import os
    import time
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sys.argv[1:] or [os.path.join(base, "out", f) for f in
                             ("candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl")]
    report = {"solver": "F7 solver B (parse rendered fields -> atom trees + facts; table-driven constraint "
                        "enumeration over (M, F) in K x K; exactly one F required)",
              "spec": "c_src/F7/G0_SPEC.md sha256 " + hashlib.sha256(
                  open(os.path.join(base, "G0_SPEC.md"), "rb").read()).hexdigest(),
              "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "independence": "Written from the frozen G0 spec (2-4, 3.5) and the rendered row fields only; never "
                              "read c_src/F7/gen/ or solver A code. Gold and meta.option_level are only compared.",
              "per_file": {}, "mismatch_rows": [], "unparsed_rows": [], "option_level_diff_rows": []}
    tot = agree = 0
    for p in files:
        r = run_file(p)
        name = os.path.basename(p)
        report["per_file"][name] = {"rows": r["rows"], "agree": r["agree"], "mismatches": len(r["mismatch"]),
                                    "unparsed": len(r["unparsed"]), "option_level_diff": len(r["option_level_diff"]),
                                    "by_sampler": r["by_sampler"], "problems": r["probs"],
                                    "worked_cases": r["worked"]}
        for k, lst in (("mismatch_rows", r["mismatch"]), ("unparsed_rows", r["unparsed"]),
                       ("option_level_diff_rows", r["option_level_diff"])):
            for x in lst:
                x["file"] = name
                report[k].append(x)
        tot += r["rows"]
        agree += r["agree"]
    report["rows_checked"] = tot
    report["agree"] = agree
    report["agree_pct"] = round(100.0 * agree / tot, 3) if tot else 0.0
    report["mismatches"] = len(report["mismatch_rows"])
    report["unparsed"] = len(report["unparsed_rows"])
    outp = os.environ.get("SB_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "mismatch.json")
    with open(outp, "w") as fh:
        json.dump(report, fh, indent=1)
    print(json.dumps({k: report[k] for k in ("rows_checked", "agree", "agree_pct", "mismatches", "unparsed")}))


if __name__ == "__main__":
    main()
