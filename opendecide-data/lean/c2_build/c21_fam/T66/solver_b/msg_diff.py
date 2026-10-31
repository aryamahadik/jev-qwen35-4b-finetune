"""Diff side of the MSG head: which kind of change does the (single) behavioural hunk of a unified diff make?

Method (no execution, no model): parse the diff into hunks and change blocks; align the removed and added lines of a block by their comment-stripped token tuples
(a pair of lines whose tokens are equal differs by layout only: formatting hunk); lines inside docstrings and comment-only lines are TRIVIAL; what remains are
behavioural units, and each unit is classified by token-level rules into the registered change kinds CH-1..CH-10. The enclosing function is read from the
`def` lines shown in the hunk. `analyse` returns a dict with the kind, ambiguity alternatives and a reason when it cannot decide."""
import difflib
import keyword
import re

from . import textparse as tp

_TOK = (r"""\s*(?:(?P<c>\#.*$)|(?P<s>[rRuUbBfF]{0,2}(?:\"\"\"|''').*?(?:\"\"\"|''')|[rRuUbBfF]{0,2}"(?:\\.|[^"\\])*"|[rRuUbBfF]{0,2}'(?:\\.|[^'\\])*')|"""
                  r"""(?P<i>[A-Za-z_]\w*)|(?P<n>\d+(?:\.\d+)?)|(?P<o>==|!=|<=|>=|//|\*\*|->|\+=|-=|\*=|/=|%=|[-+*/%<>=()\[\]{}:,.@&|^~!;]))""")
_TRIPLE = r'"""|\'\'\''
_CMP = {"<", ">", "<=", ">=", "==", "!="}


def tokens(line):
    """[(kind, text)] with kind in s (string) i (identifier) n (number) o (operator); comments are dropped."""
    out, pos = [], 0
    s = line
    while pos < len(s):
        m = re.match(_TOK, s[pos:])
        if not m or m.end() == 0:
            if s[pos:].strip() == "":
                break
            out.append(("x", s[pos]))
            pos += 1
            continue
        pos += m.end()
        for k in ("s", "i", "n", "o"):
            if m.group(k) is not None:
                out.append((k, m.group(k)))
                break
    return out


def _strip(line):
    return line.strip()


def _doc_flags(hunk):
    """Per line of the hunk: True when a CHANGED line belongs to a docstring-like string (inside a triple-quoted string, opening or closing one, or a lone string
    statement), computed on the line's own side (old side = context + removed lines, new side = context + added lines)."""
    flags = [False] * len(hunk.lines)
    lone = r"""^[rRuUbB]?("([^"\\]|\\.)*"|'([^'\\]|\\.)*')$"""
    opener = r"""^[rRuUbB]?(\"\"\"|\'\'\')"""
    for side in ("-", "+"):
        inside = False
        for idx, (tag, text) in enumerate(hunk.lines):
            if tag not in (" ", side):
                continue
            st = text.strip()
            n = len(re.findall(_TRIPLE, st))
            was = inside
            if n % 2 == 1:
                inside = not inside
            if tag != " " and (was or re.match(opener, st) or re.match(lone, st)):
                flags[idx] = True
    return flags


def _blocks(hunk, flags):
    """Maximal runs of changed lines -> [(removed [(text, is_doc)], added [(text, is_doc)])]."""
    out, cur = [], None
    for (tag, text), fl in zip(hunk.lines, flags):
        if tag == " ":
            cur = None
            continue
        if cur is None:
            cur = ([], [])
            out.append(cur)
        (cur[0] if tag == "-" else cur[1]).append((text, fl))
    return out


def _is_comment_only(text):
    return text.strip().startswith("#")


def _units(removed, added):
    """Drop blank, comment-only and docstring lines; align the rest by token tuples; equal tuples are layout-only. -> [(R lines, A lines)] behavioural units."""
    r = [t for t, d in removed if t.strip() and not d and not _is_comment_only(t)]
    a = [t for t, d in added if t.strip() and not d and not _is_comment_only(t)]
    rt = [tuple(tokens(x)) for x in r]
    at = [tuple(tokens(x)) for x in a]
    sm = difflib.SequenceMatcher(None, rt, at, autojunk=False)
    units = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        units.append((r[i1:i2], a[j1:j2]))
    return units


# ---- unit classification --------------------------------------------------------------------------------------------------------------
_DEF = (r"^\s*def\s+([A-Za-z_]\w*)\s*\((.*)\)\s*(?:->\s*[^:]+)?:\s*$")


def _params(sig):
    """'a, b=2' -> [(name, default source or None)] using a token walk (no parsing of code into objects)."""
    out, depth, cur = [], 0, []
    for k, t in tokens(sig):
        if t in "([{" and k == "o":
            depth += 1
        elif t in ")]}" and k == "o":
            depth -= 1
        if t == "," and depth == 0 and k == "o":
            out.append(cur)
            cur = []
        else:
            cur.append((k, t))
    if cur:
        out.append(cur)
    res = []
    for p in out:
        if not p:
            continue
        name = p[0][1]
        eq = [i for i, x in enumerate(p) if x == ("o", "=")]
        res.append((name, " ".join(t for _, t in p[eq[0] + 1:]) if eq else None))
    return res


def _classify_pair_tokens(rl, al):
    """One removed line and one added line -> (kind, alt) or None."""
    rt, at = tokens(rl), tokens(al)
    sm = difflib.SequenceMatcher(None, rt, at, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    if not ops:
        return None
    # all differences are one numeric / string / identifier replacement
    if len(ops) == 1 and ops[0][0] == "replace" and ops[0][2] - ops[0][1] == 1 and ops[0][4] - ops[0][3] == 1:
        _, i1, _, j1, _ = ops[0]
        (rk, rv), (ak, av) = rt[i1], at[j1]
        if rk == "n" and ak == "n":
            try:
                delta = abs(float(av) - float(rv))
            except ValueError:
                return None
            prev = rt[i1 - 1][1] if i1 > 0 else ""
            nxt = rt[i1 + 1][1] if i1 + 1 < len(rt) else ""
            in_cmp = prev in _CMP or nxt in _CMP
            in_range = any(x == ("i", "range") for x in rt[:i1])
            if (in_cmp or in_range) and delta == 1:
                return "CH-2", ()
            return "CH-10", ()
        if rk == "s" and ak == "s":
            return "CH-8", ()
        if rk == "i" and ak == "i" and not keyword.iskeyword(rv) and not keyword.iskeyword(av):
            return "CH-3", ()
        if rk == "o" and ak == "o" and {rv, av} in ({"<", "<="}, {">", ">="}):
            return "CH-2", ()
        return None
    # a "+ 1" / "- 1" inserted into a bound
    if len(ops) == 1 and ops[0][0] == "insert":
        ins = [t for _, t in at[ops[0][3]:ops[0][4]]]
        if ins in (["+", "1"], ["-", "1"]) and (any(x == ("i", "range") for x in rt) or any(t in _CMP for _, t in rt)):
            return "CH-2", ()
    if len(ops) == 1 and ops[0][0] == "delete":
        dele = [t for _, t in rt[ops[0][1]:ops[0][2]]]
        if dele in (["+", "1"], ["-", "1"]) and (any(x == ("i", "range") for x in at) or any(t in _CMP for _, t in at)):
            return "CH-2", ()
    return None


def _classify_unit(R, A):
    """-> (kind, alt tuple) or ("unknown", reason)."""
    if not R and A:
        first = A[0].strip()
        body = [x.strip() for x in A[1:]]
        if first.startswith("if ") and first.endswith(":") and body and (body[0].startswith("raise") or body[0].startswith("return")):
            return "CH-1", ()
        if all(re.match(r"^[A-Za-z_][\w.]*\(.*\)$", x.strip()) and not x.strip().startswith(("raise", "return")) for x in A):
            return "CH-9", ()
        return "unknown", "pure addition"
    if R and not A:
        first = R[0].strip()
        if first.startswith(("if ", "elif ", "else")):
            return "CH-7", ()
        return "unknown", "pure deletion"
    dr = [re.match(_DEF, x) for x in R]
    da = [re.match(_DEF, x) for x in A]
    if len(R) == 1 and len(A) == 1 and dr[0] and da[0]:
        n1, p1 = dr[0].group(1), _params(dr[0].group(2))
        n2, p2 = da[0].group(1), _params(da[0].group(2))
        if n1 != n2:
            return ("CH-3", ()) if p1 == p2 else ("unknown", "rename plus signature")
        if p1 == p2:
            return "unknown", "def line differs only outside the parameters"
        if [p[0] for p in p1] != [p[0] for p in p2]:
            return "CH-6", ()
        # same names; defaults differ
        added = [n for (n, d1), (_, d2) in zip(p1, p2) if d1 is None and d2 is not None]
        removed = [n for (n, d1), (_, d2) in zip(p1, p2) if d1 is not None and d2 is None]
        changed = [n for (n, d1), (_, d2) in zip(p1, p2) if d1 is not None and d2 is not None and d1 != d2]
        if changed and not added and not removed:
            return "CH-5", ()
        if removed and not added and not changed:
            return "CH-6", ("CH-5",)            # a parameter that had a default is now required: parameter list reading, default reading as alternative
        if added and not removed and not changed:
            return "CH-5", ("CH-6",)
        return "unknown", "mixed default change"
    if len(R) == len(A):
        if len(R) > 1:                                  # adjacent changes with no context line between them: judge each line pair on its own
            parts = [_classify_unit([rl], [al]) for rl, al in zip(R, A)]
            if any(k == "unknown" for k, _ in parts):
                return "unknown", "line pair"
            if len({k for k, _ in parts}) != 1:
                return "unknown", "mixed pair kinds"
            return parts[0][0], tuple(sorted({x for _, al in parts for x in al}))
        c = _classify_pair_tokens(R[0], A[0])
        return c if c is not None else ("unknown", "line pair")
    return "unknown", "unequal blocks"


def analyse(diff_text):
    """-> {"ok": bool, "kind": str|None, "alt": tuple, "why": str, "n_units": int, "idents": set}"""
    try:
        hunks = tp.parse_diff(diff_text)
    except tp.ParseError as e:
        return {"ok": False, "kind": None, "alt": (), "why": "diff parse: %s" % e, "n_units": 0, "idents": set()}
    idents = set()
    kinds, alts, n_units = [], [], 0
    for h in hunks:
        for _tag, text in h.lines:
            for k, t in tokens(text):
                if k == "i" and not keyword.iskeyword(t):
                    idents.add(t)
        flags = _doc_flags(h)
        for removed, added in _blocks(h, flags):
            for R, A in _units(removed, added):
                n_units += 1
                k, extra = _classify_unit(R, A)
                if k == "unknown":
                    return {"ok": False, "kind": None, "alt": (), "why": "unit: %s" % extra, "n_units": n_units, "idents": idents}
                kinds.append(k)
                alts.append(tuple(extra))
    if not kinds:
        return {"ok": False, "kind": None, "alt": (), "why": "no behavioural unit", "n_units": 0, "idents": idents}
    ks = set(kinds)
    if len(ks) != 1:
        return {"ok": False, "kind": None, "alt": (), "why": "several behavioural kinds", "n_units": n_units, "idents": idents}
    alt = tuple(sorted(set(a for al in alts for a in al)))
    return {"ok": True, "kind": kinds[0], "alt": alt, "why": "", "n_units": n_units, "idents": idents}
