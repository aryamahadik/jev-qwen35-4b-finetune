"""families/T42/gen_out.py: the typed program grammar of the output head (T42 head 1).

Programs are generated from typed templates over ints, strings, lists, dicts, sets, slicing, comprehensions, loops,
closures, default arguments, exceptions, string formatting and sorting with keys, plus classes for the MRO bucket. A
template returns (setup, final): the plugin ends the program with print(final) or result = final. Difficulty bin d:
1 = one construct and a short trace, 2 = two constructs / one nesting level, 3 = three constructs / nesting 2.
Names come from a naming style ("short" or "long"); the style is a card dimension, never a label.

  IDIOMS           idiom bucket -> [template functions]
  HELD_OUT_IDIOMS  ("closure", "mro"): used only by the held-out sampler S5
  EXC_CAPABLE      templates that can end in an uncaught exception (the plugin steers them by the planned gold kind)
  make(rng, idiom, d, style, fail) -> (setup, final, template name)
Nothing here executes code or reads an output: gold comes from executor.py only.
"""
from __future__ import annotations

import textwrap

WORDS = ["apple", "kiwi", "banana", "fig", "plum", "cherry", "melon", "lime", "pear", "grape", "mango", "peach",
         "lemon", "olive", "berry", "guava"]
POOLS = {
    "short": {"xs": ["xs", "a", "v", "ns"], "acc": ["t", "s", "r", "z"], "i": ["i", "j", "k"], "w": ["s", "w", "u"],
              "d": ["d", "m", "c"], "f": ["f", "g", "h"], "p": ["p", "q"], "n": ["n", "m", "k"]},
    "long": {"xs": ["items", "numbers", "values", "readings"], "acc": ["total", "running", "score", "tally"],
             "i": ["index", "pos", "step", "idx"], "w": ["word", "text", "label", "line"],
             "d": ["counts", "table", "lookup", "groups"], "f": ["apply", "convert", "compute", "shift"],
             "p": ["pair", "entry", "record"], "n": ["limit", "size", "count", "width"]},
}


class Names:
    """Unique names per role, drawn from the style's pool (never 'result': it is the answer variable)."""

    def __init__(self, rng, style):
        self.rng, self.pool, self.used = rng, POOLS[style], set()

    def __call__(self, role):
        c = [x for x in self.pool[role] if x not in self.used] or [self.pool[role][0] + "2"]
        n = self.rng.choice(c)
        self.used.add(n)
        return n


def _d(s):
    return textwrap.dedent(s).strip("\n")


def ints(R, n, lo=1, hi=9):
    return [R.randint(lo, hi) for _ in range(n)]


def distinct(R, n, lo=1, hi=20):
    return R.sample(range(lo, hi + 1), n)


# ------------------------------------------------------------------------------------------------ arithmetic loops
def arith_acc(R, d, nm):
    acc, i, n = nm("acc"), nm("i"), nm("n")
    a, b, k, m = R.randint(0, 7), R.randint(5, 8 + 2 * d), R.randint(2, 9), R.randint(2, 9)
    body = [f"{acc} = {acc} + {i} * {k}" if d == 1 else f"{acc} = ({acc} * {k} + {i}) % {R.choice([17, 23, 29])}"]
    if d >= 2:
        body.insert(0, f"if {i} % {m} == {R.randint(0, m - 1)}:\n    continue")
    if d >= 3:
        body.append(f"if {acc} > {R.randint(20, 40)}:\n    {acc} -= {R.randint(3, 9)}")
    step = f", {R.choice([2, 3, 4, 5, 6])}" if R.random() < 0.4 else ""
    code = f"{acc} = {R.randint(0, 2)}\nfor {i} in range({a}, {b}{step}):\n" + textwrap.indent("\n".join(body), "    ")
    return code, acc


def arith_while(R, d, nm):
    n, acc = nm("n"), nm("acc")
    kind = R.choice(["digits", "collatz", "gcd"] if d >= 2 else ["digits", "halve"])
    if kind == "digits":
        v = R.randint(120, 99999)
        return f"{n} = {v}\n{acc} = 0\nwhile {n}:\n    {acc} += {n} % 10\n    {n} //= 10", acc
    if kind == "halve":
        v = R.randint(40, 900)
        return f"{n} = {v}\n{acc} = 0\nwhile {n} > 1:\n    {n} = {n} // {R.choice([2, 3, 4, 5, 6])}\n    {acc} += 1", acc
    if kind == "collatz":
        v = R.choice([6, 7, 9, 12, 15, 17, 19, 22, 25, 27][:6 + d])
        return (f"{n} = {v}\n{acc} = 0\nwhile {n} != 1:\n    {n} = {n} // 2 if {n} % 2 == 0 else 3 * {n} + 1\n"
                f"    {acc} += 1"), acc
    a, b = R.randint(12, 90), R.randint(12, 90)
    p = nm("p")
    return f"{n} = {a}\n{p} = {b}\nwhile {p}:\n    {n}, {p} = {p}, {n} % {p}", n


def arith_div(R, d, nm):
    a, b, c = R.randint(7, 60), R.randint(2, 9), R.randint(2, 9)
    x, y = nm("n"), nm("acc")
    ex = R.choice([f"{x} // {b} + {x} % {b}", f"{x} / {b}", f"({x} + {c}) // {b} * {c}", f"{x} - {x} // {b} * {b}",
                   f"-{x} // {b}", f"{x} // {b} - -{x} // {b}"])
    code = f"{x} = {a}\n{y} = {ex}"
    if d >= 2:
        code += f"\n{y} = {y} if {y} > {b} else {y} + {c}"
    return code, f"{y}"


# ------------------------------------------------------------------------------------------------ strings and slices
def slice_str(R, d, nm):
    s, t = nm("w"), nm("acc")
    w = R.choice(WORDS) + R.choice(WORDS)[:R.randint(2, 9)]
    n = len(w)
    parts = [f"{s}[{R.randint(0, 2)}:{R.randint(3, n)}]", f"{s}[::-1][{R.randint(0, 7)}:{R.randint(4, n)}]",
             f"{s}[-{R.randint(2, 9)}:]", f"{s}[::{R.randint(2, 7)}]", f"{s}[{R.randint(1, 7)}:-{R.randint(1, 7)}]"]
    R.shuffle(parts)
    code = f'{s} = "{w}"\n{t} = {parts[0]} + "-" + {parts[1]}'
    if d >= 2:
        code += f"\n{t} = {t}.replace({R.choice(w[:3])!r}, '#').upper()" if R.random() < 0.6 else \
            f"\n{t} = {t}.title()"
    if d >= 3:
        code += f"\n{t} = {t}[{R.randint(0, 2)}:] + {s}[{R.randint(0, 2)}]"
    return code, t


def slice_list(R, d, nm):
    xs, ys = nm("xs"), nm("acc")
    L = ints(R, R.randint(6, 9), 1, 30)
    a, b = R.randint(0, 2), R.randint(4, len(L))
    code = f"{xs} = {L}\n{ys} = {xs}[{a}:{b}:{R.choice([1, 2, 3])}]"
    if d >= 2:
        code += f"\n{ys} = {ys}[::-1] + {xs}[-{R.randint(1, 7)}:]"
    if d >= 3:
        code += f"\n{xs}[{R.randint(0, 2)}:{R.randint(3, 5)}] = {R.choice([[0], [7, 7], []])}\n{ys} = {ys} + {xs}"
    return code, ys


def str_methods(R, d, nm):
    s, t = nm("w"), nm("acc")
    words = R.sample(WORDS, 3 + d)
    code = f'{s} = "{" ".join(words)}"\n{t} = {s}.split()'
    ex = R.choice([f"[w[0].upper() + w[1:] for w in {t}]", f"[len(w) for w in {t}]", f"{t}[::-1]",
                   f'"-".join(w[:{R.randint(2, 7)}] for w in {t})', f'{s}.count("{R.choice("aeiou")}")',
                   f'{s}.find("{R.choice(words)[:2]}")'])
    if d >= 2:
        code += f'\n{t} = {ex}'
        ex = R.choice([f"{t}", f"len({t})"])
    return code, ex


# ------------------------------------------------------------------------------------------------ comprehensions
def comp_list(R, d, nm):
    xs, ys, i = nm("xs"), nm("acc"), nm("i")
    L = ints(R, R.randint(6, 9), 1, 15)
    m, r, k = R.randint(2, 9), R.randint(0, 1), R.randint(2, 9)
    code = f"{xs} = {L}\n{ys} = [{i} * {k} for {i} in {xs} if {i} % {m} == {r}]"
    final = ys
    if d >= 2:
        j = "j" if i != "j" else "k"
        code = (f"{xs} = {L[:5]}\n{ys} = [({i}, {j}) for {i} in range(len({xs})) for {j} in range({i}) "
                f"if ({xs}[{i}] + {xs}[{j}]) % {m} == {r}]")
        final = f"len({ys}), {ys}[:{R.randint(1, 2)}]" if d == 2 else f"sum(a * b for a, b in {ys})"
    return code, final


def comp_dict_set(R, d, nm):
    xs, dd = nm("xs"), nm("d")
    L = ints(R, R.randint(6, 9), 1, 12)
    m = R.randint(2, 9)
    kind = R.choice(["dict", "set", "inv"] if d >= 2 else ["dict", "set"])
    if kind == "dict":
        return f"{xs} = {L}\n{dd} = {{x: x * x % {m + 5} for x in {xs}}}", f"sorted({dd}.items())"
    if kind == "set":
        return f"{xs} = {L}\n{dd} = {{x % {m} for x in {xs}}}", f"sorted({dd}), len({dd})"
    w = R.sample(WORDS, 4)
    return (f"{dd} = {{w: len(w) for w in {w}}}\ninv = {{v: k for k, v in {dd}.items()}}"), f"sorted(inv.items())"


# ------------------------------------------------------------------------------------------------ dict, sort, set
def dict_count(R, d, nm):
    dd, w = nm("d"), nm("w")
    words = [R.choice(WORDS[:5 + d]) for _ in range(R.randint(6, 9))]
    code = f"{dd} = {{}}\nfor {w} in {words}:\n    {dd}[{w}] = {dd}.get({w}, 0) + 1"
    final = R.choice([dd, f"sorted({dd}.items(), key=lambda kv: (-kv[1], kv[0]))[:2]", f"max({dd}, key={dd}.get)",
                      f"len({dd}), max({dd}.values())"])
    return code, final


def dict_group(R, d, nm):
    dd, x, xs = nm("d"), nm("p"), nm("xs")
    L = ints(R, R.randint(6, 9), 1, 25)
    m = R.randint(2, 9)
    code = f"{xs} = {L}\n{dd} = {{}}\nfor {x} in {xs}:\n    {dd}.setdefault({x} % {m}, []).append({x})"
    final = R.choice([dd, f"[{dd}[k] for k in sorted({dd})]", f"{{k: sum(v) for k, v in {dd}.items()}}"])
    return code, final


def sort_key(R, d, nm):
    xs = nm("xs")
    kind = R.choice(["len", "tuple", "abs", "rev"] if d >= 2 else ["len", "abs", "rev"])
    if kind == "len":
        w = R.sample(WORDS, 5 + d)
        return f"{xs} = {w}", R.choice([f"sorted({xs}, key=len)", f"sorted({xs}, key=len, reverse=True)",
                                         f"max({xs}, key=len)", f"min({xs}, key=lambda w: w[-1])"])
    if kind == "abs":
        L = [R.randint(-9, 9) for _ in range(6 + d)]
        return f"{xs} = {L}", R.choice([f"sorted({xs}, key=abs)", f"sorted({xs}, key=abs, reverse=True)",
                                        f"sorted({xs}, key=lambda v: -v % 5)"])
    if kind == "rev":
        L = ints(R, 6 + d, 1, 20)
        return f"{xs} = {L}\n{xs}.sort(key=lambda v: v % {R.randint(3, 5)})", xs
    P = [(R.choice("abc"), R.randint(1, 5)) for _ in range(5 + d)]
    return f"{xs} = {P}", R.choice([f"sorted({xs}, key=lambda p: p[1], reverse=True)[:3]",
                                     f"sorted({xs}, key=lambda p: (p[0], -p[1]))[:3]", f"max({xs}, key=lambda p: p[1])"])


def set_ops(R, d, nm):
    a, b = distinct(R, R.randint(4, 6), 1, 12), distinct(R, R.randint(4, 6), 4, 15)
    code = f"A = {set(a)!r}\nB = {set(b)!r}"
    if d >= 2:
        code += f"\nC = A | B if {R.randint(0, 1)} else A & B"
    final = R.choice(["sorted(A & B)", "sorted(A - B), sorted(B - A)", "sorted(A ^ B)", "len(A | B)",
                      "A <= B, A.isdisjoint(B)" if d == 1 else "sorted(C)"])
    return code, final


# ------------------------------------------------------------------------------------------------ defaults and aliasing
def default_arg(R, d, nm):
    f, p, xs = nm("f"), nm("p"), nm("xs")
    kind = R.choice(["shared", "guard", "defer"])
    items = ints(R, 3, 1, 9)
    if kind in ("shared", "guard"):
        head = (f"def {f}({p}, bucket=[]):\n    bucket.append({p})\n    return bucket" if kind == "shared" else
                f"def {f}({p}, bucket=None):\n    if bucket is None:\n        bucket = []\n    bucket.append({p})\n"
                f"    return bucket")
        calls = f"{f}({items[0]})\n{f}({items[1]}, [{items[2]}])\n{xs} = {f}({items[2]})"
        if d >= 2:
            calls += f"\n{f}({R.randint(1, 9)})"
        return head + "\n" + calls, f"{xs}, {f}({R.randint(1, 9)})" if d == 3 else xs
    b = R.randint(2, 9)
    code = f"base = {b}\ndef {f}({p}, step=base):\n    return {p} + step\nbase = {b + R.randint(1, 5)}"
    return code, f"{f}({R.randint(1, 9)}), {f}({R.randint(1, 9)}, {R.randint(1, 9)})"


def aliasing(R, d, nm):
    xs, ys = nm("xs"), nm("acc")
    kind = R.choice(["grid", "alias", "func"])
    if kind == "grid":
        n, r, c = R.randint(2, 9), R.randint(0, 1), R.randint(0, 1)
        code = f"{ys} = [[0] * {n}] * {n}\n{ys}[{r}][{c}] = {R.randint(1, 9)}"
        if d >= 2:
            code += f"\n{ys}[{n - 1}].append(1)"
        return code, ys
    if kind == "alias":
        L = ints(R, 3, 1, 9)
        code = f"{xs} = {L}\nb = {xs}\nb.append({R.randint(1, 9)})\nc = {xs}[:]\nc.append({R.randint(1, 9)})"
        if d >= 2:
            code += f"\nb = b + [0]\n{xs}.extend(c[-1:])"
        return code, f"{xs}, b, c"
    L = ints(R, 3, 1, 9)
    f = nm("f")
    code = f"def {f}(v):\n    v.append({R.randint(1, 9)})\n    v = v + [{R.randint(10, 19)}]\n    return v\n{xs} = {L}\n{ys} = {f}({xs})"
    return code, f"{xs}, {ys}"


# ------------------------------------------------------------------------------------------------ exceptions
def exc_flow(R, d, nm):
    f, v, acc = nm("f"), nm("p"), nm("acc")
    vals = [R.choice(["4", "x", "7", "12", "", "3.5", "9"]) for _ in range(3 + d)]
    handler = R.choice(["ValueError", "(ValueError, TypeError)"])
    code = (f"log = []\ndef {f}({v}):\n    try:\n        n = int({v})\n    except {handler}:\n        log.append('bad')\n"
            f"        return -1\n    else:\n        log.append('ok')\n        return n * {R.randint(2, 9)}\n"
            f"    finally:\n        log.append({R.choice(['v', 'z'])!r})\n{acc} = [{f}(s) for s in {vals}]")
    return code, R.choice([f"{acc}, len(log)", f"{acc}", f"len(log), {acc}[0]"])


def exc_fail(R, d, nm, fail=True, cls="KeyError", info=None):
    """3-4 risky steps of ONE exception class (KeyError: dictionary lookups; IndexError: list indexing;
    ZeroDivisionError: integer divisions), summed. With fail exactly one step is wrong and the program ends in an
    uncaught `cls`; without it every step is fine. The class is the same for the shown program and for the mutants
    that raise (the plugin keeps only exc:cls as an exception option), so the class never tells gold from distractor."""
    dd, acc, xs = nm("d"), nm("acc"), nm("xs")
    n_steps = 3 if d == 1 else 4
    bad = R.randrange(n_steps) if fail else -1
    lines, terms, fixed = [], [], []
    if cls == "KeyError":
        ks = R.sample(WORDS[:6], 4)
        lines.append(f"{dd} = {{{', '.join(f'{k!r}: {R.randint(1, 9)}' for k in ks)}}}")
        for i in range(n_steps):
            good = R.choice(ks)
            terms.append(f"{dd}[{(R.choice(WORDS[6:]) if i == bad else good)!r}]")
            fixed.append(f"{dd}[{good!r}]")
    elif cls == "IndexError":
        L = ints(R, 5, 1, 9)
        lines.append(f"{xs} = {L}")
        for i in range(n_steps):
            good = R.randint(0, 4)
            terms.append(f"{xs}[{R.randint(5, 7) if i == bad else good}]")
            fixed.append(f"{xs}[{good}]")
    else:
        for i in range(n_steps):
            n, num, step = R.randint(2, 9), R.randint(10, 90), R.choice([1, 2])
            terms.append(f"{num} // ({n} - {n if i == bad else n - step})")
            fixed.append(f"{num} // ({n} - {n - step})")
    if info is not None:           # the program with the one wrong step repaired (the 'repair_failure' near-miss)
        info["fixed"] = "\n".join(lines + [f"{acc} = 0"] + [f"{acc} += {t}" for t in fixed])
    return "\n".join(lines + [f"{acc} = 0"] + [f"{acc} += {t}" for t in terms]), acc


# ------------------------------------------------------------------------------------------------ formatting
def fmt_f(R, d, nm):
    x, y = R.randint(3, 140), R.randint(1, 30)
    kind = R.choice(["int", "float", "str"])
    if kind == "int":
        spec = R.choice([">6", "<5", "05d", "^7", "+d", ",", "x", "b", "o"])
        if spec in (",",):
            x = x * 1000
        out = f'f"[{{x:{spec}}}]"'
    elif kind == "float":
        a, b = R.randint(2, 40), R.randint(3, 9)
        return f"a = {a}\nb = {b}", f'f"{{a / b:.{R.randint(1, 7)}f}}|{{a // b}}|{{a % b:>3}}"'
    else:
        w = R.choice(WORDS)
        return f'w = "{w}"', R.choice([f'f"{{w:>8}}|{{w!r}}"', f'f"{{w:*^{R.randint(8, 11)}}}"', f'f"{{w[:3]:<5}}|{{len(w):02d}}"'])
    if d >= 2:
        return f"x = {x}\ny = {y}", f'f"{{x:>5}}-{{y:<3}}-{{x + y:03d}}"' if kind == "int" else out
    return f"x = {x}", out


def fmt_pct(R, d, nm):
    n, p = R.randint(2, 40), R.randint(2, 9) * 5 + R.choice([0, 0.5, 0.25])
    kind = R.choice(["pct", "join", "format"])
    if kind == "pct":
        return f"n = {n}\np = {p}", R.choice(['"%d items at %5.1f" % (n, p)', '"%s/%s" % (n, p)', '"%03d|%-4d|" % (n, n + 1)'])
    if kind == "join":
        dd = {w: R.randint(1, 9) for w in R.sample(WORDS[:6], 3)}
        return f"d = {dd!r}", R.choice(['",".join(f"{k}={v}" for k, v in d.items())',
                                        '" ".join("%s:%d" % (k[:2], v) for k, v in sorted(d.items()))'])
    return f"n = {n}", R.choice(['"{:>4}|{:<4}|".format(n, n * 2)', '"{0}-{1}-{0}".format(n, n + 1)',
                                 '"{:.1f}".format(n / 7)', '"{:08.3f}".format(n / 3)'])


# ------------------------------------------------------------------------------------------------ iteration and control
def iter_gen(R, d, nm):
    xs, i = nm("xs"), nm("i")
    kind = R.choice(["iter", "gen", "zip"] if d >= 2 else ["iter", "zip"])
    L = ints(R, R.randint(5, 8), 1, 20)
    if kind == "iter":
        return f"{xs} = {L}\nit = iter({xs})\na = next(it)\nb = next(it)\nrest = list(it)", R.choice(
            ["a, b, rest", "a + b, len(rest)", f"a, list(it), rest[{R.randint(0, 2)}:]"])
    if kind == "zip":
        return f"{xs} = {L}", R.choice([f"list(zip({xs}, {xs}[1:]))[:3]", f"[a - b for a, b in zip({xs}, {xs}[1:])]",
                                        f"list(enumerate({xs}, start={R.randint(1, 7)}))[:3]",
                                        f"dict(zip({xs}[::2], {xs}[1::2]))"])
    m, k = R.randint(2, 9), R.randint(2, 9)
    return (f"def gen(n):\n    for {i} in range(n):\n        if {i} % {m}:\n            yield {i} * {k}\n"
            f"g = gen({R.randint(7, 10)})\nfirst = next(g)"), R.choice(["first, sum(g)", "first, list(g)", "first, next(g)"])


def while_control(R, d, nm):
    xs, x, acc = nm("xs"), nm("i"), nm("acc")
    L = ints(R, R.randint(6, 9), 1, 15)
    m, lim = R.randint(2, 9), R.randint(8, 13)
    code = (f"{xs} = {L}\n{acc} = 0\nfor {x} in {xs}:\n    if {x} % {m} == 0:\n        continue\n    if {x} > {lim}:\n"
            f"        break\n    {acc} += {x}")
    if d >= 2:
        code += f"\nelse:\n    {acc} = -{acc}"
    if d >= 3:
        code += f"\nn = 0\nwhile n < {acc} % 7 + 2:\n    n += 1\n    if n == {R.randint(2, 9)}:\n        break"
    return code, acc if d < 3 else f"{acc}, n"


# ------------------------------------------------------------------------------------------------ held-out buckets
def closure_late(R, d, nm):
    f = nm("f")
    k = R.randint(2, 9)
    kind = R.choice(["loop", "default", "counter", "listcomp"] if d >= 2 else ["loop", "listcomp", "default"])
    arg = R.randint(1, 9)
    if kind == "loop":
        return (f"fns = []\nfor i in range({k}):\n    fns.append(lambda x: x + i)\n"), f"[fn({arg}) for fn in fns]"
    if kind == "default":
        return f"fns = []\nfor i in range({k}):\n    fns.append(lambda x, i=i: x * i)\n", f"[fn({arg}) for fn in fns]"
    if kind == "listcomp":
        return f"fns = [lambda: i * {R.randint(2, 7)} for i in range({k + 1})]", "[fn() for fn in fns]"
    step = R.randint(1, 9)
    return (f"def make(start):\n    c = start\n    def inc():\n        nonlocal c\n        c += {step}\n        return c\n"
            f"    return inc\na = make({R.randint(0, 5)})\nb = make({R.randint(0, 5)})\na()\nb()"), f"a(), b(), a()"


def mro_dispatch(R, d, nm):
    names = R.sample("ABCDEFG", 4)
    a, b, c, e = names
    tags = [R.choice("xyzuvw") for _ in range(4)]
    kind = R.choice(["diamond", "mro", "attr", "init", "init"] if d >= 2 else ["diamond", "attr", "init"])
    if kind == "init":
        t = R.sample("abcdefgh", 4)
        code = (f"log = []\nclass {a}:\n    def __init__(self):\n        log.append('{t[0]}')\n"
                f"class {b}({a}):\n    def __init__(self):\n        log.append('{t[1]}')\n        super().__init__()\n"
                f"class {c}({a}):\n    def __init__(self):\n        log.append('{t[2]}')\n        super().__init__()\n"
                f"class {e}({b}, {c}):\n    def __init__(self):\n        super().__init__()\n        log.append('{t[3]}')\n"
                f"{e}()")
        return code, R.choice(["log", "''.join(log)", f"log, len({e}.__mro__)"])
    if kind == "attr":
        return (f"class {a}:\n    tag = '{tags[0]}'\n    def name(self):\n        return self.tag\n"
                f"class {b}({a}):\n    tag = '{tags[1]}'\nclass {c}({a}):\n    def name(self):\n        return '{tags[2]}' + super().name()\n"
                f"class {e}({c}, {b}):\n    pass"), f"{e}().name(), {b}().name(), {c}().tag"
    code = (f"class {a}:\n    def who(self):\n        return '{tags[0]}'\n"
            f"class {b}({a}):\n    def who(self):\n        return '{tags[1]}' + super().who()\n"
            f"class {c}({a}):\n    def who(self):\n        return '{tags[2]}' + super().who()\n"
            f"class {e}({b}, {c}):\n    def who(self):\n        return '{tags[3]}' + super().who()\n")
    if kind == "mro":
        return code, f"[k.__name__ for k in {e}.__mro__], {e}().who()"
    return code, f"{e}().who(), {c}().who()"


IDIOMS = {
    "arith_loop": [arith_acc, arith_while, arith_div],
    "slice_str": [slice_str, slice_list, str_methods],
    "comprehension": [comp_list, comp_dict_set],
    "dict_ops": [dict_count, dict_group],
    "sort_key": [sort_key],
    "set_ops": [set_ops],
    "default_arg": [default_arg],
    "aliasing": [aliasing],
    "exceptions": [exc_flow, exc_fail],
    "formatting": [fmt_f, fmt_pct],
    "iteration": [iter_gen, while_control],
    "closure": [closure_late],
    "mro": [mro_dispatch],
}
HELD_OUT_IDIOMS = ("closure", "mro")
TRAIN_IDIOMS = tuple(k for k in IDIOMS if k not in HELD_OUT_IDIOMS)
EXC_CAPABLE = {"exc_fail"}


def make(R, idiom: str, d: int, style: str, fail: bool = False, template: str | None = None,
         exc_class: str = "KeyError", info: dict | None = None):
    """(setup, final, template name). `fail` steers exc_fail templates toward an uncaught exception; `template`
    pins one template of the idiom by name."""
    nm = Names(R, style)
    fn = R.choice(IDIOMS[idiom]) if template is None else next(f for f in IDIOMS[idiom] if f.__name__ == template)
    if fn is exc_fail:
        setup, final = exc_fail(R, d, nm, fail=fail, cls=exc_class, info=info)
    else:
        setup, final = fn(R, d, nm)
    return setup, final, fn.__name__
