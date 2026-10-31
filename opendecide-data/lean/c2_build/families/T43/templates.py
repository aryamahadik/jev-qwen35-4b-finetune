"""families/T43/templates.py: the correct originals of T43 (program text only; no model writes any of it).

Two program kinds, both printed through one printer (ast.unparse):
  line    one function with a docstring `Equals <expr>.` and EXACTLY 6 body lines (16 templates; the numbered-line head)
  module  5-8 functions: 3-6 list stages, one reducer and the entry `run`; every function carries its own
          `Equals <expr>.` docstring; the entry's expression is the inline composition of the stages (the numbered-function head)
The docstring expression is the reference semantics of the function (solver B's oracle); the original body is an
independent loop-style implementation, checked equal to the expression on the G0 grid by the tests.

  build_line(R, tpl, style)            -> program dict
  build_module(R, n_fn, reducer, style)-> program dict
  LINE_TEMPLATES, STAGES, REDUCERS     the pools
Program dict: {kind, template, style, file, fns: [{name, src, ref, types}], entry, src}
"""
from __future__ import annotations

import ast
import re

STYLES = (
    {"xs": "xs", "k": "k", "t": "t", "x": "x", "n": "n", "i": "i", "out": "out", "s": "s", "c": "c"},
    {"xs": "values", "k": "limit", "t": "total", "x": "v", "n": "count", "i": "idx", "out": "kept", "s": "text", "c": "ch"},
    {"xs": "readings", "k": "cutoff", "t": "acc", "x": "r", "n": "size", "i": "pos", "out": "rows", "s": "line", "c": "sym"},
)
FILES = ("stats.py", "utils.py", "calc.py", "metrics.py", "scores.py", "helpers.py")
TYPES = {"int": "int", "list[int]": "ints", "str": "str"}


def fill(text: str, names: dict, consts: dict) -> str:
    def sub(m):
        k = m.group(1)
        return str(consts[k]) if k in consts else names[k]
    return re.sub(r"@(\w+)@", sub, text)


def norm(src: str) -> str:
    return ast.unparse(ast.parse(src))


def _fn_info(src: str) -> list:
    out = []
    for n in ast.parse(src).body:
        if isinstance(n, ast.FunctionDef):
            doc = ast.get_docstring(n)
            m = re.fullmatch(r"Equals (.+)\.", doc or "")
            if not m:
                raise ValueError(f"function {n.name}: no 'Equals <expr>.' docstring")
            types = [TYPES[ast.unparse(a.annotation)] for a in n.args.args]
            out.append({"name": n.name, "ref": m.group(1), "types": types,
                        "params": [a.arg for a in n.args.args]})
    return out


# ------------------------------------------------------------------------------------------------ line templates
# (id, function names per style, params, body lines, reference, constants drawn from R)
def _c(R, **rng):
    return {k: R.randint(a, b) for k, (a, b) in rng.items()}


LINE_TEMPLATES = {
    "above_sum": (("above_total", "limit_sum", "gate_sum"), "@xs@: list[int], @k@: int",
                  ["@t@ = 0", "for @i@ in range(0, len(@xs@)):", "    if @xs@[@i@] > @k@:", "        @t@ += @xs@[@i@] * @C@",
                   "@t@ = @t@ * @E@", "return @t@ + @D@"],
                  "sum(@xs@[@i@] * @C@ for @i@ in range(len(@xs@)) if @xs@[@i@] > @k@) * @E@ + @D@", dict(C=(2, 5), D=(1, 4), E=(2, 3))),
    "rise_count": (("count_rises", "steep_steps", "jump_count"), "@xs@: list[int], @k@: int",
                   ["@c@ = 0", "for @i@ in range(1, len(@xs@)):", "    @n@ = @xs@[@i@] - @xs@[@i@ - 1]", "    if @n@ > @k@:",
                    "        @c@ += 1", "return @c@ * @C@ + @D@"],
                   "sum(1 for @i@ in range(1, len(@xs@)) if @xs@[@i@] - @xs@[@i@ - 1] > @k@) * @C@ + @D@", dict(C=(2, 4), D=(1, 3))),
    "clip_sum": (("clipped_total", "capped_sum", "cap_total"), "@xs@: list[int], @k@: int",
                 ["@t@ = 0", "for @i@ in range(0, len(@xs@)):", "    @x@ = @xs@[@i@] + @D@", "    @t@ += min(@x@, @k@)",
                  "@t@ = @t@ * @C@", "return @t@ - @E@"],
                 "sum(min(@xs@[@i@] + @D@, @k@) for @i@ in range(len(@xs@))) * @C@ - @E@", dict(C=(2, 4), D=(1, 4), E=(1, 5))),
    "max_gap": (("widest_gap", "max_step", "top_gap"), "@xs@: list[int]",
                ["@t@ = 0", "for @i@ in range(len(@xs@) - 1):", "    @n@ = @xs@[@i@ + 1] - @xs@[@i@]", "    @t@ = max(@t@, @n@)",
                 "@t@ = @t@ * @C@", "return @t@ + @D@"],
                "max([0] + [@xs@[@i@ + 1] - @xs@[@i@] for @i@ in range(len(@xs@) - 1)]) * @C@ + @D@", dict(C=(2, 4), D=(1, 4))),
    "band_count": (("band_count", "window_hits", "in_band"), "@xs@: list[int], @k@: int",
                   ["@n@ = @k@ * @C@", "@c@ = 0", "for @i@ in range(0, len(@xs@)):",
                    "    if @xs@[@i@] > @k@ and @xs@[@i@] < @n@:", "        @c@ += 1", "return @c@ * @D@"],
                   "sum(1 for @i@ in range(len(@xs@)) if @xs@[@i@] > @k@ and @xs@[@i@] < @k@ * @C@) * @D@", dict(C=(2, 4), D=(2, 4))),
    "digit_total": (("digit_total", "digit_score", "digit_mass"), "@n@: int",
                    ["@n@ = abs(@n@) + @D@", "@t@ = 0", "while @n@ > 0:", "    @t@ += @n@ % 10", "    @n@ //= 10", "return @t@ * @C@"],
                    "sum(int(@c@) for @c@ in str(abs(@n@) + @D@)) * @C@", dict(C=(2, 5), D=(1, 4))),
    "best_prefix": (("best_prefix", "peak_prefix", "max_prefix"), "@xs@: list[int]",
                    ["@t@ = 0", "@n@ = 0", "for @i@ in range(0, len(@xs@)):", "    @n@ += @xs@[@i@]", "    @t@ = max(@t@, @n@)",
                     "return @t@ * @D@"], "max(sum(@xs@[:@i@]) for @i@ in range(len(@xs@) + 1)) * @D@", dict(D=(2, 5))),
    "first_over": (("first_over", "first_above", "find_over"), "@xs@: list[int], @k@: int",
                   ["@i@ = 0", "while @i@ < len(@xs@):", "    if @xs@[@i@] > @k@:", "        return @i@ + @D@", "    @i@ += 1",
                    "return 0 - @E@"],
                   "next((@i@ + @D@ for @i@, @x@ in enumerate(@xs@) if @x@ > @k@), 0 - @E@)", dict(D=(1, 4), E=(1, 3))),
    "mean_floor": (("mean_floor", "avg_floor", "level_mean"), "@xs@: list[int]",
                   ["if len(@xs@) == 0:", "    return 0", "@t@ = sum(@xs@) + @D@", "@n@ = len(@xs@) + @E@", "@c@ = @t@ // @n@",
                    "return @c@ * @C@"],
                   "(sum(@xs@) + @D@) // (len(@xs@) + @E@) * @C@ if len(@xs@) != 0 else 0", dict(C=(2, 4), D=(1, 6), E=(1, 3))),
    "pick_ranked": (("pick_ranked", "ranked_item", "nth_best"), "@xs@: list[int], @k@: int",
                    ["if len(@xs@) == 0:", "    return 0 - @E@", "@s@ = sorted(@xs@, reverse=True)", "@i@ = min(@k@, len(@xs@) - 1)",
                     "@i@ = max(@i@, 0)", "return @s@[@i@] + @D@"],
                    "sorted(@xs@, reverse=True)[max(min(@k@, len(@xs@) - 1), 0)] + @D@ if len(@xs@) != 0 else 0 - @E@",
                    dict(D=(1, 4), E=(1, 3))),
    "vowel_score": (("vowel_score", "vowel_points", "vowel_mass"), "@s@: str, @k@: int",
                    ["@n@ = 0", "for @i@ in range(0, len(@s@)):", "    if @s@[@i@] in 'aeiou':", "        @n@ += 1",
                     "@n@ = @n@ * @k@ + @D@", "return @n@ * @E@"],
                    "(sum(1 for @i@ in range(len(@s@)) if @s@[@i@] in 'aeiou') * @k@ + @D@) * @E@", dict(D=(1, 5), E=(2, 3))),
    "lead_trim": (("trimmed_len", "after_trim", "trim_width"), "@s@: str",
                  ["@i@ = 0", "while @i@ < len(@s@) and @s@[@i@] == ' ':", "    @i@ += 1", "@t@ = len(@s@) + @D@", "@n@ = @t@ - @i@",
                   "return @n@ * @C@"], "(len(@s@.lstrip(' ')) + @D@) * @C@", dict(C=(2, 4), D=(1, 4))),
    "alt_sum": (("alt_total", "swing_total", "alt_score"), "@xs@: list[int]",
                ["@t@ = 0", "for @i@ in range(0, len(@xs@)):", "    @n@ = 1 if @i@ % 2 == 0 else -1", "    @t@ += @n@ * @xs@[@i@]",
                 "@t@ = @t@ * @C@", "return @t@ + @D@"],
                "sum((1 if @i@ % 2 == 0 else -1) * @xs@[@i@] for @i@ in range(len(@xs@))) * @C@ + @D@", dict(C=(2, 4), D=(1, 4))),
    "distinct_score": (("distinct_score", "unique_score", "uniq_mass"), "@xs@: list[int]",
                       ["@n@ = 0", "for @i@ in range(0, len(@xs@)):", "    if @xs@[@i@] not in @xs@[:@i@]:", "        @n@ += 1",
                        "@n@ = @n@ * @C@", "return @n@ + @D@"], "len(set(@xs@)) * @C@ + @D@", dict(C=(2, 4), D=(1, 4))),
    "scaled_cap": (("scaled_cap", "capped_scale", "cap_scale"), "@n@: int, @k@: int",
                   ["if @n@ <= 0:", "    return @D@", "@t@ = @n@ * @C@", "if @t@ > @k@:", "    @t@ = @k@ + @E@", "return @t@ - @D@"],
                   "((@k@ + @E@ if @n@ * @C@ > @k@ else @n@ * @C@) - @D@) if @n@ > 0 else @D@", dict(C=(2, 5), D=(1, 4), E=(1, 3))),
    "pair_count": (("pair_count", "adjacent_hits", "pair_hits"), "@xs@: list[int], @k@: int",
                   ["@c@ = 0", "for @i@ in range(0, len(@xs@) - 1):", "    if @xs@[@i@] + @xs@[@i@ + 1] > @k@:", "        @c@ += 1",
                    "@c@ = @c@ * @C@", "return @c@ - @D@"],
                   "sum(1 for @i@ in range(len(@xs@) - 1) if @xs@[@i@] + @xs@[@i@ + 1] > @k@) * @C@ - @D@", dict(C=(2, 4), D=(1, 3))),
}
# S5 only: a slice idiom whose lines are not all mutable by the training operators
S5_TEMPLATES = {
    "tail_top": (("tail_top", "top_tail", "tail_rank"), "@xs@: list[int], @k@: int",
                 ["@out@ = []", "for @x@ in @xs@[1:]:", "    @out@.append(@x@ + @k@)", "@out@.sort(reverse=True)",
                  "@out@ = @out@[:@C@]", "return @out@"], "sorted([@x@ + @k@ for @x@ in @xs@[1:]], reverse=True)[:@C@]",
                 dict(C=(2, 4))),
}
# measured (feas run, 24 draws per template x line): these two have lines the ambiguity guard / observability rule out in most draws
# (digit_total lines 1-2: 0.5 / 0.29; lead_trim lines 2, 3, 5: 0.67 / 0.12 / 0.0), which would make the bug line depend on the template
for _t in ("digit_total", "lead_trim"):
    S5_TEMPLATES[_t] = LINE_TEMPLATES.pop(_t)
LINE_ORDER = tuple(LINE_TEMPLATES)
S5_ORDER = LINE_ORDER + tuple(S5_TEMPLATES)
NAME_POOL = ("calm", "brisk", "tidy", "plain", "sharp", "swift", "quiet", "rough", "steady", "gentle", "bold", "clear", "dense",
             "eager", "fresh", "grand", "hardy", "ideal", "jolly", "keen", "lucid", "mild", "noble", "prime", "rapid", "solid",
             "tame", "vivid", "warm", "zesty", "amber", "birch", "cedar", "dune", "ember", "fjord", "grove", "haze", "isle", "jade")
NAME_POOL2 = ("pass", "step", "scan", "fold", "pack", "walk", "trim", "mark", "sift", "tally", "sweep", "shape")


def build_line(R, tpl: str, style: int) -> dict:
    names_, params, body, ref, crng = (LINE_TEMPLATES.get(tpl) or S5_TEMPLATES[tpl])
    consts = {k: R.randint(a, b) for k, (a, b) in sorted(crng.items())}
    nm = STYLES[style]
    fname = names_[style]
    lines = [fill(ln, nm, consts) for ln in body]
    head = f"def {fname}({fill(params, nm, consts)}):\n    \"\"\"Equals {fill(ref, nm, consts)}.\"\"\"\n"
    src = norm(head + "\n".join("    " + ln for ln in lines) + "\n")
    info = _fn_info(src)
    assert len(src.split("\n")) == 8, (tpl, src)
    for f in info:
        f["src"] = src
    return {"kind": "line", "template": tpl, "style": style, "file": FILES[(R.randrange(6) + 0) % 6], "fns": info,
            "entry": fname, "src": src}


# ------------------------------------------------------------------------------------------------ module stages
# (id, name, params, body, ref with {P} = the previous list expression, the reference docstring with param names)
STAGES = {
    "keep_over": ("keep_over", "@xs@: list[int], @k@: int",
                  ["@out@ = []", "for @x@ in @xs@:", "    if @x@ > @k@:", "        @out@.append(@x@)", "return @out@"],
                  "[@x@ for @x@ in {P} if @x@ > {k}]", ("k", (1, 5))),
    "keep_even": ("keep_even", "@xs@: list[int]",
                  ["@out@ = []", "for @x@ in @xs@:", "    if @x@ % 2 == 0:", "        @out@.append(@x@)", "return @out@"],
                  "[@x@ for @x@ in {P} if @x@ % 2 == 0]", None),
    "scale_by": ("scale_by", "@xs@: list[int], @k@: int",
                 ["@out@ = []", "for @x@ in @xs@:", "    @out@.append(@x@ * @k@)", "return @out@"],
                 "[@x@ * {k} for @x@ in {P}]", ("k", (2, 4))),
    "shift_by": ("shift_by", "@xs@: list[int], @k@: int",
                 ["@out@ = []", "for @x@ in @xs@:", "    @out@.append(@x@ + @k@)", "return @out@"],
                 "[@x@ + {k} for @x@ in {P}]", ("k", (1, 5))),
    "cap_at": ("cap_at", "@xs@: list[int], @k@: int",
               ["@out@ = []", "for @x@ in @xs@:", "    @out@.append(min(@x@, @k@))", "return @out@"],
               "[min(@x@, {k}) for @x@ in {P}]", ("k", (3, 9))),
    "dedupe_sorted": ("dedupe_sorted", "@xs@: list[int]",
                      ["@out@ = []", "for @x@ in @xs@:", "    if @x@ not in @out@:", "        @out@.append(@x@)", "@out@.sort()",
                       "return @out@"], "sorted(set({P}))", None),
    "step_gaps": ("step_gaps", "@xs@: list[int]",
                  ["@out@ = []", "for @i@ in range(1, len(@xs@)):", "    @out@.append(@xs@[@i@] - @xs@[@i@ - 1])", "return @out@"],
                  "[@a@[@i@] - @a@[@i@ - 1] for @i@ in range(1, len(@a@))]", None),
    "running_sum": ("running_sum", "@xs@: list[int]",
                    ["@out@ = []", "@t@ = 0", "for @x@ in @xs@:", "    @t@ += @x@", "    @out@.append(@t@)", "return @out@"],
                    "[sum(@a@[:@i@ + 1]) for @i@ in range(len(@a@))]", None),
    "floor_zero": ("floor_zero", "@xs@: list[int]",
                   ["@out@ = []", "for @x@ in @xs@:", "    @out@.append(@x@ if @x@ > 0 else 0)", "return @out@"],
                   "[@x@ if @x@ > 0 else 0 for @x@ in {P}]", None),
    "head_sorted": ("head_sorted", "@xs@: list[int], @k@: int",
                    ["@out@ = @xs@[:@k@]", "@out@.sort()", "return @out@"], "sorted({P}[:{k}])", ("k", (2, 5))),
}
REDUCERS = {
    "total": ("total", "@xs@: list[int]", ["@t@ = 0", "for @x@ in @xs@:", "    @t@ += @x@", "return @t@"], "sum({P})", None),
    "spread": ("spread", "@xs@: list[int]", ["if not @xs@:", "    return 0", "return max(@xs@) - min(@xs@)"],
               "max({P}) - min({P}) if {P} else 0", None),
    "count_over": ("count_over", "@xs@: list[int], @k@: int",
                   ["@t@ = 0", "for @x@ in @xs@:", "    if @x@ > @k@:", "        @t@ += 1", "return @t@"],
                   "sum(1 for @x@ in {P} if @x@ > {k})", ("k", (1, 6))),
    "weighted": ("weighted", "@xs@: list[int]",
                 ["@t@ = 0", "for @i@ in range(len(@xs@)):", "    @t@ += @xs@[@i@] * (@i@ + 1)", "return @t@"],
                 "sum({P}[@i@] * (@i@ + 1) for @i@ in range(len(@xs@)))", None),
}
STAGE_ORDER = tuple(STAGES)
REDUCER_ORDER = tuple(REDUCERS)
MODULE_FILES = ("pipeline.py", "report.py", "feed.py", "batch.py")


def build_module(R, n_fn: int, reducer: str, style: int, force: tuple | None = None) -> dict:
    """force = (position, stage id): the stage at that position is that type (the others are a uniform draw of the remaining types in
    random order), so the type of the gold function is drawn BEFORE the gold and independent of its position (T43 w4)."""
    nm = STYLES[style]
    n_st = n_fn - 2
    if force is not None and force[0] < n_st:
        rest = R.sample([s for s in STAGE_ORDER if s != force[1]], n_st - 1)
        chosen = rest[:force[0]] + [force[1]] + rest[force[0]:]
    else:
        chosen = R.sample(STAGE_ORDER, n_st)
    pool = [f"{a}_{b}" for a in NAME_POOL for b in NAME_POOL2]
    fnames = R.sample(pool, n_st + 2)             # function names carry no stage identity (the gold function is uniform over names)
    fns, calls, comp = [], [], nm["xs"]
    cur = nm["xs"]
    letters = "abcdefgh"
    entry_lines = []
    ks = {}
    for idx, sid in enumerate(chosen):
        name, params, body, ref, kspec = STAGES[sid]
        name = fnames[idx]
        k = R.randint(*kspec[1]) if kspec else None
        ks[sid] = k
        # standalone function (own docstring over its own parameters)
        own = ref.replace("{P}", "@xs@").replace("{k}", "@k@").replace("@a@", "@xs@")
        if "(lambda" in own:
            raise AssertionError
        fn_src = (f"def {name}({fill(params, nm, {})}):\n    \"\"\"Equals {fill(own, nm, {})}.\"\"\"\n" +
                  "\n".join("    " + fill(ln, nm, {}) for ln in body) + "\n")
        fns.append(fn_src)
        arg = f"{cur}, {k}" if k is not None else cur
        var = letters[idx]
        entry_lines.append(f"    {var} = {name}({arg})")
        cur = var
        comp = f"{name}({comp}, {k})" if k is not None else f"{name}({comp})"
    rname, rparams, rbody, rref, rk = REDUCERS[reducer]
    rname = fnames[-1]
    k = R.randint(*rk[1]) if rk else None
    own = rref.replace("{P}", "@xs@").replace("{k}", "@k@")
    fns.append(f"def {rname}({fill(rparams, nm, {})}):\n    \"\"\"Equals {fill(own, nm, {})}.\"\"\"\n" +
               "\n".join("    " + fill(ln, nm, {}) for ln in rbody) + "\n")
    arg = f"{cur}, {k}" if k is not None else cur
    entry_lines.append(f"    return {rname}({arg})")
    comp_r = f"{rname}({comp}, {k})" if k is not None else f"{rname}({comp})"
    ename = fnames[-2]
    entry = (f"def {ename}({nm['xs']}: list[int]) -> int:\n    \"\"\"Equals {comp_r}.\"\"\"\n" + "\n".join(entry_lines) + "\n")
    order = fns + [entry]
    src = norm("\n\n".join(order))
    info = _fn_info(src)
    assert len(info) == n_fn, (len(info), n_fn)
    return {"kind": "module", "template": f"mod{n_fn}_{reducer}", "style": style, "file": MODULE_FILES[R.randrange(4)],
            "fns": info, "entry": ename, "src": src}
