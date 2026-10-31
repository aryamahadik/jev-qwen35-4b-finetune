"""families/T42/gen_eq.py: function-pair skeletons of the equivalence head (T42 head 2).

A skeleton is a small typed function with named CHOICE POINTS. Every point has variants in classes:
  "A"     forms of the reference behaviour (mutually interchangeable, so swapping them changes the text, not the meaning)
  "typ"   a near-miss expected to differ on ordinary inputs
  "edge"  a near-miss expected to differ only on an edge input (empty, zero, negative, single, repeated items ...)
The class is a HINT for the sampler; the label of a pair always comes from executing it (executor.py). Both functions of
a pair are assembled from the same skeleton and printed by the same printer (ast.unparse), so the formatting of f and g
is identical by construction.

  SKELETONS            name -> builder(R) -> {"sig", "head", "tpl", "points": {P: {"A": [...], "typ": [...], "edge": [...]}}}
  pair_source(sk, f_choice, g_choice)   -> (f source, g source)
  rename_locals(src, R)                 alpha-renames params and locals (a pure surface change)
"""
from __future__ import annotations

import ast
import re

TYPE_OF = {"int": "int", "ints": "list[int]", "str": "str"}


def _sk(sig, tpl, points, head="", params=None):
    return {"sig": tuple(sig), "tpl": tpl, "points": points, "head": head, "params": params}


def filter_sum(R):
    thr = R.choice(["k", "k + 1"]) if False else "k"
    return _sk(("ints", "int"), "def @N@(xs: list[int], k: int):\n    @P0@\n    @P1@\n    return t", {
        "P0": {"A": ["ys = list(xs)", "ys = xs[:]", "ys = [v for v in xs]"], "typ": [], "edge": []},
        "P1": {"A": ["t = 0\nfor x in ys:\n    if x > k:\n        t += x", "t = sum(x for x in ys if x > k)",
                     "t = sum([x for x in ys if x > k])", "t = sum(filter(lambda x: x > k, ys))"],
               "typ": ["t = sum(x for x in ys if x >= k)", "t = 0\nfor x in ys:\n    if x > k:\n        t += 1"],
               "edge": ["t = sum(x for x in ys if abs(x) > k)", "t = 0\nfor x in ys[1:]:\n    if x > k and x != 0:\n        t += x"
                        if False else "t = sum(x for x in ys if x > k and x != 0 and x != 1)"]}})


def vowels_tail(R):
    return _sk(("str", "int"), "def @N@(s: str, k: int):\n    @P0@\n    @P1@\n    return n", {
        "P0": {"A": ["tail = s[k:]", "tail = s[k:len(s)]"], "typ": [],
               "edge": ["tail = ''.join(s[i] for i in range(k, len(s)))"]},
        "P1": {"A": ["n = 0\nfor ch in tail:\n    if ch in 'aeiou':\n        n += 1", "n = sum(ch in 'aeiou' for ch in tail)",
                     "n = len([c for c in tail if c in 'aeiou'])", "n = sum(1 for c in tail if c in ('a', 'e', 'i', 'o', 'u'))"],
               "typ": ["n = sum(ch in 'aeio' for ch in tail)", "n = len(set(c for c in tail if c in 'aeiou'))"],
               "edge": ["n = sum(ch.lower() in 'aeiou' for ch in tail)", "n = len([c for c in tail if c in 'aeiouA'])"]}})


def abs_gap(R):
    return _sk(("int", "int"), "def @N@(a: int, b: int):\n    @P0@", {
        "P0": {"A": ["return abs(a - b)", "return max(a, b) - min(a, b)", "return a - b if a >= b else b - a",
                     "return a - b if a > b else b - a"],
               "typ": ["return a - b", "return abs(a) - abs(b)", "return max(a - b, 0)"],
               "edge": ["return abs(a - b) if a != 0 else b" if False else "return abs(a - b) if b >= 0 else a - b"]}})


def halve(R):
    return _sk(("int",), "def @N@(n: int):\n    @P0@\n    @P1@\n    return h, r", {
        "P0": {"A": ["h = n // 2", "h = n >> 1", "h = (n - n % 2) // 2", "h = int(n // 2)"], "typ": ["h = (n + 1) // 2"],
               "edge": ["h = int(n / 2)"]},
        "P1": {"A": ["r = n - 2 * h", "r = n % 2", "r = n & 1", "r = 1 if n % 2 else 0"], "typ": ["r = n % 3"], "edge": []}})


def first_last(R):
    return _sk(("ints",), "def @N@(xs: list[int]):\n    @P0@", {
        "P0": {"A": ["return xs[0] + xs[-1]", "return xs[0] + xs[len(xs) - 1]", "return sum((xs[0], xs[-1]))",
                     "first, last = xs[0], xs[-1]\nreturn first + last"],
               "typ": ["return xs[0] + xs[-2]", "return xs[1] + xs[-1]"],
               "edge": ["return sum(xs[:1] + xs[-1:])", "return xs[0] + xs[-1] if len(xs) > 1 else 0"]}})


def top_item(R):
    return _sk(("ints",), "def @N@(xs: list[int]):\n    @P0@", {
        "P0": {"A": ["return max(xs)", "return max(x for x in xs)", "return max(xs, key=lambda v: v)",
                     "return -min(-x for x in xs)"],
               "typ": ["return min(xs)", "return sorted(xs)[-2]" if False else "return max(xs[1:])" if False else
                       "return max(xs) - min(xs)"],
               "edge": ["return sorted(xs)[-1]", "m = xs[0]\nfor x in xs[1:]:\n    if x > m:\n        m = x\nreturn m"]}})


def distinct_count(R):
    return _sk(("ints",), "def @N@(xs: list[int]):\n    @P0@\n    @P1@\n    return n", {
        "P0": {"A": ["seen = set(xs)", "seen = {x for x in xs}", "seen = set()\nfor x in xs:\n    seen.add(x)"],
               "typ": ["seen = set(xs[1:])"], "edge": []},
        "P1": {"A": ["n = len(seen)", "n = sum(1 for _ in seen)", "n = len(list(seen))"], "typ": ["n = len(seen) - 1"],
               "edge": ["n = len(xs)"]}})


def clamp(R):
    return _sk(("int", "int"), "def @N@(x: int, hi: int):\n    @P0@", {
        "P0": {"A": ["return min(x, hi)", "return x if x < hi else hi", "return hi if x > hi else x",
                     "return x if x <= hi else hi", "return (x + hi - abs(x - hi)) // 2"],
               "typ": ["return max(x, hi)", "return min(x, hi - 1)"],
               "edge": ["return min(x, hi) if x > 0 else x", "return min(x, hi) if hi > 0 else x"]}})


def tidy(R):
    return _sk(("str",), "def @N@(s: str):\n    @P0@", {
        "P0": {"A": ["return s.strip().lower()", "return s.lower().strip()", "t = s.strip()\nreturn t.lower()",
                     "return ''.join(c.lower() for c in s).strip()"],
               "typ": ["return s.upper()", "return s.strip().title()"],
               "edge": ["return s.lstrip().lower()", "return s.strip().lower().replace('a b', 'ab')"
                        if False else "return s.rstrip().lower()"]}})


def repeat(R):
    return _sk(("str", "int"), "def @N@(s: str, n: int):\n    @P0@", {
        "P0": {"A": ["return s * n", "return ''.join(s for _ in range(n))", "return n * s", "out = ''\nfor _ in range(n):\n    out += s\nreturn out"],
               "typ": ["return s * (n - 1)", "return s * n + s"],
               "edge": ["return s * max(n, 1)", "return s * abs(n)"]}})


def index_of(R):
    return _sk(("ints", "int"), "def @N@(xs: list[int], k: int):\n    @P0@", {
        "P0": {"A": ["return xs.index(k) if k in xs else -1",
                     "for i, x in enumerate(xs):\n    if x == k:\n        return i\nreturn -1",
                     "return next((i for i, x in enumerate(xs) if x == k), -1)",
                     "for i in range(len(xs)):\n    if xs[i] == k:\n        return i\nreturn -1"],
               "typ": ["return xs.index(k) if k in xs else 0", "for i, x in enumerate(xs):\n    if x >= k:\n        return i\nreturn -1"],
               "edge": ["pos = -1\nfor i, x in enumerate(xs):\n    if x == k:\n        pos = i\nreturn pos",
                        "return len(xs) - 1 - xs[::-1].index(k) if k in xs else -1"]}})


def prefix(R):
    return _sk(("ints",), "def @N@(xs: list[int]):\n    @P0@", {
        "P0": {"A": ["out = []\nt = 0\nfor x in xs:\n    t += x\n    out.append(t)\nreturn out",
                     "return [sum(xs[:i + 1]) for i in range(len(xs))]",
                     "from itertools import accumulate\nreturn list(accumulate(xs))"],
               "typ": ["out = []\nt = 0\nfor x in xs:\n    out.append(t)\n    t += x\nreturn out",
                       "return [sum(xs[:i]) for i in range(len(xs))]"],
               "edge": ["out = [xs[0]]\nfor x in xs[1:]:\n    out.append(out[-1] + x)\nreturn out"]}})


def digit_sum(R):
    return _sk(("int",), "def @N@(n: int):\n    @P0@", {
        "P0": {"A": ["return sum(int(c) for c in str(abs(n)))",
                     "n = abs(n)\nt = 0\nwhile n:\n    t += n % 10\n    n //= 10\nreturn t",
                     "return sum(map(int, str(abs(n))))"],
               "typ": ["return sum(int(c) for c in str(n)[1:])" if False else "return len(str(abs(n)))"],
               "edge": ["return sum(int(c) for c in str(n))", "t = 0\nwhile n > 0:\n    t += n % 10\n    n //= 10\nreturn t"]}})


def sign_name(R):
    return _sk(("int",), "def @N@(x: int):\n    @P0@", {
        "P0": {"A": ["if x < 0:\n    return 'neg'\nif x == 0:\n    return 'zero'\nreturn 'pos'",
                     "return ['neg', 'zero', 'pos'][(x > 0) - (x < 0) + 1]",
                     "return {-1: 'neg', 0: 'zero', 1: 'pos'}[(x > 0) - (x < 0)]",
                     "return 'neg' if x < 0 else 'zero' if x == 0 else 'pos'"],
               "typ": ["return 'pos' if x > 3 else 'neg'"],
               "edge": ["return 'pos' if x > 0 else 'neg'", "return 'neg' if x < 0 else 'pos'"]}})


def palin(R):
    return _sk(("str",), "def @N@(s: str):\n    @P0@", {
        "P0": {"A": ["return s == s[::-1]", "return list(s) == list(reversed(s))",
                     "return all(s[i] == s[-1 - i] for i in range(len(s) // 2))", "return s == ''.join(reversed(s))"],
               "typ": [],
               "edge": ["return s[0] == s[-1]", "return s[:1] == s[-1:]" if False else "return s.lower() == s.lower()[::-1]"]}})


def fizz_count(R):
    a, b = R.choice([(3, 5), (2, 7), (3, 4), (4, 6)])
    lcm = a * b // __import__("math").gcd(a, b)
    return _sk(("int",), "def @N@(n: int):\n    @P0@", {
        "P0": {"A": [f"return n // {a} + n // {b} - n // {lcm}",
                     f"return sum(1 for i in range(1, n + 1) if i % {a} == 0 or i % {b} == 0)",
                     f"return len([i for i in range(1, n + 1) if i % {a} == 0 or i % {b} == 0])"],
               "typ": [f"return n // {a} + n // {b}", f"return sum(1 for i in range(1, n) if i % {a} == 0 or i % {b} == 0)"],
               "edge": [f"return sum(1 for i in range(n + 1) if i % {a} == 0 or i % {b} == 0) - 1 if n > 0 else 0",
                        f"return len([i for i in range(1, abs(n) + 1) if i % {a} == 0 or i % {b} == 0])"]}})


def pair_sum_target(R):
    return _sk(("ints", "int"), "def @N@(xs: list[int], k: int):\n    @P0@", {
        "P0": {"A": ["return any(a + b == k for i, a in enumerate(xs) for b in xs[i + 1:])",
                     "for i in range(len(xs)):\n    for j in range(i + 1, len(xs)):\n        if xs[i] + xs[j] == k:\n            return True\nreturn False",
                     "seen = set()\nfor x in xs:\n    if k - x in seen:\n        return True\n    seen.add(x)\nreturn False"],
               "typ": ["return any(a + b == k for a in xs for b in xs)" if False else "return any(a + b <= k for i, a in enumerate(xs) for b in xs[i + 1:])"],
               "edge": ["return any(a + b == k for a in xs for b in xs)", "return k in {a + b for a in xs for b in xs}"]}})


SKELETONS = {f.__name__: f for f in (filter_sum, vowels_tail, abs_gap, halve, first_last, top_item, distinct_count, clamp,
                                     tidy, repeat, index_of, prefix, digit_sum, sign_name, palin, fizz_count,
                                     pair_sum_target)}


def _fill(tpl: str, name: str, choice: dict) -> str:
    out = tpl.replace("@N@", name)
    lines = []
    for ln in out.split("\n"):
        m = re.fullmatch(r"(\s*)@(P\d)@", ln)
        if m:
            ind = m.group(1)
            lines += [ind + x if x else x for x in choice[m.group(2)].split("\n")]
        else:
            lines.append(ln)
    return "\n".join(lines)


def pair_source(sk: dict, f_choice: dict, g_choice: dict) -> tuple:
    """(f source, g source), both through the one printer."""
    fs = ast.unparse(ast.parse(sk["head"] + _fill(sk["tpl"], "f", f_choice)))
    gs = ast.unparse(ast.parse(sk["head"] + _fill(sk["tpl"], "g", g_choice)))
    return fs, gs


class _Rename(ast.NodeTransformer):
    def __init__(self, mapping):
        self.m = mapping

    def visit_Name(self, n):
        if n.id in self.m:
            n.id = self.m[n.id]
        return n

    def visit_arg(self, n):
        if n.arg in self.m:
            n.arg = self.m[n.arg]
        return n


ALT = ["u", "v", "w", "q", "z", "val", "acc", "cur", "tmp", "buf", "arr", "seq", "num", "item", "ch", "pos"]


def rename_locals(src: str, R, skip=("f", "g")) -> str:
    """Alpha-rename parameters and locals (builtins and the function name stay)."""
    tree = ast.parse(src)
    bound = []
    for n in ast.walk(tree):
        if isinstance(n, ast.arg):
            bound.append(n.arg)
        elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            bound.append(n.id)
    bound = [b for i, b in enumerate(bound) if b not in bound[:i] and b not in skip]
    if not bound:
        return src
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | {n.arg for n in ast.walk(tree)
                                                                         if isinstance(n, ast.arg)}
    pool = [a for a in ALT if a not in used]
    R.shuffle(pool)
    mapping = dict(zip(bound, pool))
    return ast.unparse(_Rename(mapping).visit(tree))
