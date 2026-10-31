"""families/T43/plugin.py: T43 PATCH-VERDICT (coding), a C2 family plugin (A42-D; FINAL_PLAN section 3, row 4).

Semantics: G0_SPEC.md. Three heads over Python programs whose every function carries a docstring `Equals <expr>.`:
  ll   localisation, line: which of the 6 numbered lines of one function holds the injected bug ("none" shown on some rows)
  lf   localisation, function: which of 5-8 functions of a module holds the bug ("none" shown on some rows)
  pv   patch verdict: A fixes / B does not fix / C passes the target test but is wrong (D does not apply, shown on some rows)
Gold is program execution only (executor.py: hermetic CPython 3.12 subprocess, two runs agree; patching.py: the strict diff
applier). Bugs are AST mutants of a correct original (families/T42/mutate.py operators; HELD_OUT_OPS = swap_args and
wrong_slice_bound appear only in the held-out sampler S5).

  solver A   execution of tests, grid and seeded differential cases against the ORIGINAL        paradigm simulator
  solver B   solver_b.py: its own parser, diff applier, AST interpreter and docstring-reference oracle     independent_interpreter
  samplers   S1 pv on 6-line functions; S2 ll; S3 lf; S4 pv on modules; S5 held out (bug operators swap_args and wrong_slice_bound,
             layouts boxed and tabs, all four heads); sealed entry point: sealed_rows(n, start_seed)
"""
from __future__ import annotations

import ast
import difflib
import functools
import random
import re
from pathlib import Path

from c2_kit import plugin as KP
from c2_kit.choiceplan import plan_choice
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row
from c2_kit.skin import RenderError, make_skin
from families.T42 import mutate as M

from . import executor as E
from . import patching as PT
from . import repairs as RP
from . import templates as TP
from . import texts as TX

HERE = Path(__file__).resolve().parent
FAMILY = "T43"
KP.FAMILIES.setdefault(FAMILY, "agent")

SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
HELD_OUT_SAMPLERS = ("S5",)
REGISTERS = ("banner", "md", "bracket", "xml", "dashes", "quote", "boxed", "tabs")
HELD_OUT_REGISTERS = ("boxed", "tabs")
HELD_OUT_OPS = tuple(M.HELD_OUT_OPS)                       # swap_args, wrong_slice_bound (the SAME two as T42)
LINE_OPS = ("off_by_one", "wrong_operator", "flip_sort", "wrong_method", "int_float_div")
MOD_OPS = LINE_OPS + ("reorder_stmts",)
TRAIN_ALL = tuple(o for o in M.OPERATORS if o not in M.HELD_OUT_OPS and o not in M.BUCKET_OPS
                  and o not in ("repair_failure", "revert_edit"))
SHOW_D = 0.16                                               # share of patch rows that show option D (gold D = 1/4 of those = 4%)
LABELS = ("A", "B", "C")
LABEL_WORDS = ("fixes", "fix", "wrong", "apply", "applies", "none", "fail")
DIAG: dict = {}
LINE_WIDTH = 64                                             # ll code lines are right-padded to this width (w4): a mutation changes
#                                                             the printed length of its line by 0..14 characters, which told the line


def pad_lines(src: str) -> str:
    """Every non-empty line right-padded with spaces to LINE_WIDTH (Python ignores trailing blanks): the printed length of the
    program and of every line is then the same whatever the mutation did (the delta of a mutation is op- and line-specific)."""
    return "\n".join(ln.ljust(LINE_WIDTH) if ln else ln for ln in src.split("\n"))
ATTEMPTS, ATTEMPTS_HELD = 200, 240
WORDS = ("tea", "banana", "Level", "ab c", "  hi", "queue", "noon", "sky", "Aa bb", "stone", "x1y", "radar")

register_name("neighbour_line", "blames the line next to the one that deviates")
register_name("trust_target_test", "calls a patch correct because the target test passes")
register_name("blame_caller", "blames the entry function that calls the deviating one")
register_name("ignore_tests", "calls a patch that leaves a listed test failing correct")


def bump(k: str) -> None:
    DIAG[k] = DIAG.get(k, 0) + 1


# ------------------------------------------------------------------------------------------------ layouts
def _tabs(line: str) -> str:
    m = re.match(r"^([ +\-]?)((?:    )+)", line)
    if not m or (m.group(1) == "" and line.startswith("---")):
        return line
    return m.group(1) + "\t" * (len(m.group(2)) // 4) + line[m.end():]


def decorate(reg: str, sid: str, body: str) -> str:
    title = TX.TITLES[sid]
    if reg == "banner":
        return f"=== {title} ===\n{body}"
    if reg == "md":
        return f"## {title}\n```\n{body}\n```"
    if reg == "bracket":
        return f"[{title}]\n{body}"
    if reg == "xml":
        return f"<{sid}>\n{body}\n</{sid}>"
    if reg == "dashes":
        return f"--- {title} ---\n{body}"
    if reg == "quote":
        return "\n".join("> " + ln for ln in (title + ":\n" + body).split("\n"))
    if reg == "boxed":
        return f"+- {title}\n" + "\n".join("| " + ln for ln in body.split("\n")) + "\n+-"
    if reg == "tabs":
        b = "\n".join(_tabs(ln) for ln in body.split("\n")) if sid in ("code", "patch") else body
        return f"=== {title} ===\n{b}"
    raise ContractError(f"register {reg}")


def make_ctx() -> KitCtx:
    reg = LexiconRegistry(FAMILY)
    for qf, meaning in TX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    form_of = {}
    for qf, ws in TX.WORDINGS.items():
        for w in ws:
            form_of[(qf, w)] = reg.add(w, question_sem(FAMILY, qf), family=FAMILY).form_id
    reg.unit_test_all()
    for fid, f in reg.forms.items():
        for e in range(f.required):
            reg.record_extraction(fid, f"program:stand-in-{e + 1}", f.sem_id)
    skins = {}
    for r in REGISTERS:
        sk = make_skin(f"T43-SK-{r}", FAMILY, f"{r} layout", {}, kind="skin", register=r, held_out=r in HELD_OUT_REGISTERS)
        skins[sk.skin_id] = sk
    for qf, ws in TX.WORDINGS.items():
        for i, w in enumerate(ws):
            sk = make_skin(f"T43-W-{qf}-{i}", FAMILY, w, {}, kind="wording", register="question", qform=qf,
                           lexicon_ids=(form_of[(qf, w)],))
            skins[sk.skin_id] = sk
    return KitCtx(skins=skins, lexicon=reg)


def make_plugin() -> tuple:
    ctx = make_ctx()
    return T43Plugin(lexicon=ctx.lexicon), ctx


# ------------------------------------------------------------------------------------------------ code helpers
def row_key(seed: int, sampler: str, head: str) -> str:
    return f"{FAMILY}|{seed}|{sampler}|{head}"


def fn_segments(src: str) -> dict:
    return {n.name: ast.get_source_segment(src, n) for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}


def fn_spans(src: str) -> dict:
    return {n.name: (n.lineno, n.end_lineno) for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}


def changed_lines(a: str, b: str) -> list:
    la, lb = a.split("\n"), b.split("\n")
    if len(la) != len(lb):
        return []
    return [i + 1 for i, (x, y) in enumerate(zip(la, lb)) if x != y]


def gen_args(R: random.Random, types: list) -> list:
    out = []
    for pos, t in enumerate(types):
        if t == "int":
            out.append(R.randint(0, 6) if pos else R.randint(-2, 12))
        elif t == "ints":
            out.append([R.randint(-2, 9) for _ in range(R.choice([0, 1, 2, 3, 3, 4, 4, 5, 5, 6]))])
        else:
            out.append(R.choice(WORDS))
    return out


def head_ll_single(prog: dict) -> bool:
    """Only one-argument entries can run out of distinct differing calls (the empty list / zero / empty text are single calls)."""
    return prog["kind"] == "line" and len([f for f in prog["fns"] if f["name"] == prog["entry"]][0]["types"]) == 1


def call_text(entry: str, args: list) -> str:
    return f"{entry}({', '.join(repr(a) for a in args)})"


@functools.lru_cache(maxsize=4096)
def _eq_sites(src: str) -> tuple:
    """[(node index, kind, file line)] places where a harmless-looking local rewrite exists."""
    out = []
    for idx, n in enumerate(ast.walk(ast.parse(src))):
        ln = getattr(n, "lineno", None)
        if ln is None:
            continue
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Mult)) and ast.unparse(n.left) != ast.unparse(n.right):
            out.append((idx, "bin", ln))
        elif isinstance(n, ast.Compare) and len(n.ops) == 1 and type(n.ops[0]) in (ast.Lt, ast.Gt, ast.LtE, ast.GtE):
            out.append((idx, "cmp", ln))
        elif isinstance(n, ast.AugAssign) and isinstance(n.op, (ast.Add, ast.Sub)) and isinstance(n.target, ast.Name):
            out.append((idx, "aug", ln))
    return tuple(out)


def _apply_eq(src: str, idx: int, kind: str):
    t = ast.parse(src)
    nodes = list(ast.walk(t))
    m = nodes[idx]
    if kind == "bin":
        m.left, m.right = m.right, m.left
    elif kind == "cmp":
        flip = {ast.Lt: ast.Gt, ast.Gt: ast.Lt, ast.LtE: ast.GtE, ast.GtE: ast.LtE}
        m.left, m.comparators[0] = m.comparators[0], m.left
        m.ops = [flip[type(m.ops[0])]()]
    else:
        new = ast.Assign(targets=[ast.Name(m.target.id, ast.Store())],
                         value=ast.BinOp(ast.Name(m.target.id, ast.Load()), type(m.op)(), m.value), lineno=m.lineno)
        for p in nodes:
            for fld in ("body", "orelse", "finalbody"):
                seq = getattr(p, fld, None)
                if isinstance(seq, list) and m in seq:
                    seq[seq.index(m)] = new
    text = ast.unparse(ast.fix_missing_locations(t))
    return text if text != src and len(text.split("\n")) == len(src.split("\n")) else None


def _eq_rewrites(src: str, avoid: set) -> list:
    out = []
    for idx, kind, ln in _eq_sites(src):
        if ln not in avoid:
            t = _apply_eq(src, idx, kind)
            if t:
                out.append((t, ln))
    return out


def _one_rewrite(src: str, avoid: set, R):
    sites = [s for s in _eq_sites(src) if s[2] not in avoid]
    R.shuffle(sites)
    for idx, kind, ln in sites[:4]:
        t = _apply_eq(src, idx, kind)
        if t:
            return t, ln
    return None


@functools.lru_cache(maxsize=4096)
def _sites_c(src: str, ops: tuple) -> tuple:
    tree = ast.parse(src)
    nodes = list(ast.walk(tree))
    return tuple(s for s in M.sites(src, ops)
                 if not (s[0] == "reorder_stmts" and isinstance(nodes[s[1]], ast.FunctionDef) and s[2] == "body:0"))


class T43Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "85bed6b2a4a3aad01cccc259e821b8af36c504fd0fbc339ee000d73d4926aea4"   # G0 v1.2 (16 Oct 2026, w8: label-blind patch size; w4: event budget, cell-first draw, exemption table)
    SAMPLERS = SAMPLERS
    HELD_OUT_SAMPLERS = HELD_OUT_SAMPLERS
    PARADIGM_A = "simulator"
    PARADIGM_B = "independent_interpreter"
    SOLVER_B_MODULE = "families.T43.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("loc_line", "choice", answer_set="closed"),
        QuestionForm("loc_line_n", "choice", answer_set="closed", abstain=True),
        QuestionForm("loc_func", "choice", answer_set="closed"),
        QuestionForm("loc_func_n", "choice", answer_set="closed", abstain=True),
        QuestionForm("pv", "choice", answer_set="closed"),
        QuestionForm("pv_d", "choice", answer_set="closed", abstain=True),
    )}
    LABEL_WORDS = LABEL_WORDS
    CLOSED_WORLD_SENTENCE = "Nothing outside the shown file and tests affects the result."
    REGISTERS = REGISTERS
    HELD_OUT_REGISTERS = HELD_OUT_REGISTERS
    NAME_ALLOW = ("Python",)
    YES_NO_ONLY = False
    _held = False
    _seed = 0
    _salt = ""                  # reseed audit only: an independent draw of the same row spec (sample_salted)

    # ------------------------------------------------------------------------------------------- sampling
    @staticmethod
    def head_of(sampler: str, seed: int) -> str:
        if sampler == "S1":
            return "pvl"
        if sampler == "S2":
            return "ll"
        if sampler == "S3":
            return "lf"
        if sampler == "S4":
            return "pvm"
        return ("ll", "lf", "pvl", "pvm")[min(3, int(uhash(FAMILY, "head5", seed) * 4))]

    @staticmethod
    def plan_for(head: str, key: str, n_fn: int = 6):
        if head == "ll":
            return plan_choice(key, closed=6, abstain=True, show_rate=0.35)
        if head == "lf":
            return plan_choice(key, closed=n_fn, abstain=True, show_rate=min(0.9, 0.05 * (n_fn + 1)))
        return plan_choice(key, closed=3, abstain=True, show_rate=SHOW_D)

    @staticmethod
    def qform_of(head: str, plan) -> str:
        if head == "ll":
            return "loc_line_n" if plan.show_abstain else "loc_line"
        if head == "lf":
            return "loc_func_n" if plan.show_abstain else "loc_func"
        return "pv_d" if plan.show_abstain else "pv"

    def sample_salted(self, seed: int, sampler: str, salt: str) -> Spec:
        """The same row spec (head, planned label / line / function, diff bin, none and D display) drawn again with an
        independent random stream: the reseed audit of A42-D 3.3."""
        self._salt = salt + "|"
        try:
            return self.sample(seed, sampler)
        finally:
            self._salt = ""

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        head = self.head_of(sampler, seed)
        key = row_key(seed, sampler, head)
        held = sampler in HELD_OUT_SAMPLERS
        self._held = held
        style = min(2, int(uhash(key, "style") * 3))
        u_fn = uhash(key, "nfn")
        n_fn = (4 + int(u_fn * 2)) if head == "pvm" else (5 if u_fn < 0.35 else 6 if u_fn < 0.65 else 7 if u_fn < 0.85 else 8)
        if head == "pvm" and not held:
            n_fn = 4 + (seed // 12) % 2                  # balanced with label (seed % 3) and reducer ((seed // 3) % 4)
        plan = self.plan_for(head, key, n_fn)
        qform = self.qform_of(head, plan)
        n_att = ATTEMPTS_HELD if held else ATTEMPTS
        self._seed = seed
        for attempt in range(n_att):
            R = random.Random(f"{key}|{self._salt}{attempt}")
            try:
                spec = self._attempt(R, seed, sampler, head, key, held, style, n_fn, plan, qform, attempt)
            except E.ExecTimeout:
                bump("timeout_drop")                     # a wall cap is never a label: the attempt is dropped
                continue
            except E.ExecError:
                bump("exec_error")
                continue
            if spec is not None:
                return spec
        raise ContractError(f"no structure after {n_att} attempts ({key})")

    # one attempt: program, bug, tests, then the head-specific part
    def _program(self, R, head: str, n_fn: int, style: int, tj: int):
        """Training samplers draw the CELL before the gold, by the seed counter (consecutive seeds of a sampler cycle exactly):
        ll: line = seed % 6, template = (seed // 6) % 14; pv lines: label = seed % 3, template = (seed // 3) % 14; pv modules:
        label = seed % 3, reducer = (seed // 3) % 4, size = 4 + (seed // 12) % 2; lf: function = seed % n, the TYPE of that function
        (stage or reducer) = (seed // n) % 9 (or % 4). An attempt that fails (no site, short tests, no patch of the label) redraws
        everything BUT the cell, so P(bug line | template), P(label | template) and P(function | type) are flat by construction
        and no feasibility rate moves them (w4: measured rates were .38 to 1)."""
        s = self._seed
        if head in ("ll", "pvl"):
            if self._held:
                return TP.build_line(R, TP.S5_ORDER[R.randrange(len(TP.S5_ORDER))], style)
            order = TP.LINE_ORDER
            return TP.build_line(R, order[((s // 6) if head == "ll" else (s // 3)) % len(order)], style)
        if self._held:
            return TP.build_module(R, n_fn, TP.REDUCER_ORDER[R.randrange(4)], style)
        if head == "pvm":
            return TP.build_module(R, n_fn, TP.REDUCER_ORDER[(s // 3) % 4], style)
        n_st = n_fn - 2                                                     # lf
        if tj < n_st:
            return TP.build_module(R, n_fn, TP.REDUCER_ORDER[R.randrange(4)], style,
                                   force=(tj, TP.STAGE_ORDER[(s // n_fn) % len(TP.STAGE_ORDER)]))
        red = TP.REDUCER_ORDER[(s // n_fn) % 4] if tj == n_st else TP.REDUCER_ORDER[R.randrange(4)]
        return TP.build_module(R, n_fn, red, style)

    def _inject(self, R, prog: dict, head: str, held: bool, tj: int):
        src = prog["src"]
        ops = HELD_OUT_OPS if held else (LINE_OPS if head == "ll" else MOD_OPS)
        sites = list(_sites_c(src, ops))
        nodes = list(ast.walk(ast.parse(src)))
        if head == "ll":
            sites = [s for s in sites if nodes[s[1]].lineno == tj + 3 and not s[2].endswith(":drop")]
        elif head == "lf":
            lo, hi = fn_spans(src)[prog["fns"][tj]["name"]]
            sites = [s for s in sites if lo <= nodes[s[1]].lineno <= hi]
        if not sites:
            bump("inject:no_site")
            return None
        s = sites[R.randrange(len(sites))]
        m = M.apply(src, s)
        if m is None or m == src:
            bump("inject:apply_none")
            return None
        if head == "ll" and changed_lines(src, m) != [tj + 3]:
            bump("inject:line_mismatch")
            return None
        if head == "lf":
            a, b = fn_segments(src), fn_segments(m)
            if [k for k in a if a[k] != b.get(k)] != [prog["fns"][tj]["name"]]:
                bump("inject:fn_mismatch")
                return None
        return m, s[0]

    def _tests(self, R, prog: dict, orig: str, mut: str, n_f2p: int, n_p2p: int, none: bool):
        entry = prog["entry"]
        types = [f for f in prog["fns"] if f["name"] == entry][0]["types"]
        calls, seen = [], set()
        for _ in range(30):
            c = call_text(entry, gen_args(R, types))
            if c not in seen:
                seen.add(c)
                calls.append(c)
        for edge in range(3):                       # edge calls (empty list / zero / empty text): a mutation that only shows there stays observable
            a = gen_args(R, types)
            for pos, t in enumerate(types):
                a[pos] = ([[], [0], [1]][edge] if t == "ints" else ((0 if edge != 2 else 1) if t == "int" and pos == 0 else (a[pos] if t != "str" else ["", "a", " "][edge])))
            c = call_text(entry, a)
            if c not in seen:
                seen.add(c)
                calls.append(c)
        R.shuffle(calls)
        res = E.run([E.pair_job(orig, mut, calls)])[0]
        f2p, p2p = [], []
        for c, (oa, ob) in zip(calls, res):
            if oa[0] != "v" or len(oa[1]) > 40:
                continue
            if ob == oa:
                p2p.append((c, oa[1]))
            elif not none:
                f2p.append((c, oa[1]))
        if none:
            tot = n_f2p + n_p2p                       # same count as a bug row (1-2 target + 2 other), so the count is label-blind
            if len(p2p) < tot:
                return None
            return {"f2p": [], "p2p": p2p[:tot], "spare": p2p[tot:tot + 2]}
        if len(f2p) < n_f2p and not (n_f2p == 2 and len(f2p) == 1 and len(calls) <= 36 and head_ll_single(prog)):
            bump("tests:short")                   # P2P tests are optional: a mutation that changes every output has none
            return None
        n_f2p = min(n_f2p, len(f2p))              # a cell whose mutation shows on ONE call only (mean_floor line 2: the empty list) shows one target test
        return {"f2p": f2p[:n_f2p], "p2p": p2p[:n_p2p], "spare": p2p[n_p2p:n_p2p + 2]}

    def _attempt(self, R, seed, sampler, head, key, held, style, n_fn, plan, qform, attempt):
        none = head in ("ll", "lf") and plan.gold_abstain
        if head in ("ll", "lf"):
            n_choices = 6 if head == "ll" else n_fn
            tj = seed % n_choices          # stratified: consecutive seeds cycle through the lines / functions (exact balance)
        else:
            tj = 0
        prog = self._program(R, head, n_fn, style, tj)
        orig = prog["src"]
        if held and head == "ll" and not none:       # sealed S5: the bug line is drawn among the lines that have a held-out site
            nodes = list(ast.walk(ast.parse(orig)))
            lines = sorted({nodes[s[1]].lineno - 2 for s in _sites_c(orig, HELD_OUT_OPS) if not s[2].endswith(":drop")} & set(range(1, 7)))
            if not lines:
                bump("inject:no_site")
                return None
            tj = lines[R.randrange(len(lines))] - 1
        if none:
            mut, op = orig, "none"
        else:
            got = self._inject(R, prog, head, held, tj)
            if got is None:
                return None
            mut, op = got
        n_f2p = 1 + int(uhash(key, "nf") < 0.4)
        n_p2p = 0 if head == "ll" else 2          # ll shows only the target tests: the number of agreeing calls told the line
        tests = self._tests(R, prog, orig, mut, n_f2p, n_p2p, none)
        if tests is None:
            return None
        fns = [{"name": f["name"], "types": f["types"], "entry": f["name"] == prog["entry"]} for f in prog["fns"]]
        allt = [(c, e) for c, e in tests["f2p"] + tests["p2p"]]
        seed_ex = int(uhash(key, "exseed" + self._salt) * 10 ** 6)
        if head in ("ll", "lf"):
            order = sorted(range(len(allt)), key=lambda i: uhash(key, "tord", i))
            disp = [allt[i] for i in order]
            groups = ["t"] * len(disp)
            if head == "ll" and not none:
                if not self._guard_line(prog, orig, mut, tj, fns, seed_ex):
                    return None
            if head == "lf" and not none:
                r = E.run([E.judge_job(orig, fns, [("m", mut)], [], seed_ex, 0)])[0][0]
                tname = prog["fns"][tj]["name"]
                if tname not in r["fn_diff"] or not set(r["fn_diff"]) <= {tname, prog["entry"]}:
                    bump("guard:fn_not_deviating")
                    return None
            patch, patched = None, None
        else:
            disp = [(c, e) for c, e in tests["f2p"]] + [(c, e) for c, e in tests["p2p"]]
            groups = ["f2p"] * len(tests["f2p"]) + ["p2p"] * len(tests["p2p"])
            built = self._patch(R, key, prog, orig, mut, op, disp, groups, fns, seed_ex, plan, held, attempt, seed)
            if built is None:
                return None
            patch, patched = built
        rep = E.run([E.judge_job(orig, fns, [("m", mut)], disp, seed_ex, 0)])[0][0]["tests"]
        spare = tests["spare"]
        if patched is not None and spare:
            res = E.run([E.pair_job(orig, patched, [c for c, _ in spare])])[0]
            spare = [sp for sp, (oa, ob) in zip(spare, res) if oa == ob]
        if head == "ll":
            orig, mut = pad_lines(orig), pad_lines(mut)
        structure = {"head": head[:2] if head != "pvl" and head != "pvm" else "pv", "qform": qform,
                     "kind": prog["kind"], "template": prog["template"], "style": style, "orig": orig, "code": mut,
                     "patch": patch, "patched": patched, "op": op, "entry": prog["entry"], "fns": fns,
                     "tests": [[c, e, g] for (c, e), g in zip(disp, groups)], "report": rep,
                     "spare": [list(x) for x in spare], "target": tj if head in ("ll", "lf") else None,
                     "n_choices": n_fn if head == "lf" else (6 if head == "ll" else 3), "exseed": seed_ex,
                     "attempt": attempt}
        E.run([E.pair_job(orig, mut, [c for c, _ in disp]),
               E.judge_job(orig, fns, [("m", mut)] + ([("p", patched)] if patched else []), disp, seed_ex, 0)], confirm=True)
        depth = len(prog["fns"]) if prog["kind"] == "module" else 1
        card = f"{FAMILY}:{structure['head']}:{prog['template']}:s{style}:v{min(2, int(uhash(key, 'cardv') * 3))}"
        tags = (f"head:{structure['head']}", f"kind:{prog['kind']}")      # no operator or template tag: metadata must not carry the bug
        return Spec(FAMILY, sampler, seed, card, qform, {}, structure=structure, depth=depth, deep=False, tags=tags,
                    pack=structure["head"])

    def _guard_line(self, prog, orig, mut, tj, fns, seed_ex) -> bool:
        gold_line = tj + 3
        if orig not in {v for _, v in RP.variants(mut, gold_line)}:
            bump("guard:gold_not_in_R*")
            return False
        cands = []
        for ln in range(3, 9):
            if ln != gold_line:
                cands += [(f"{ln}.{i}", v) for i, (_, v) in enumerate(RP.variants(mut, ln))]
        if not cands:
            return True
        for lo in range(0, len(cands), 12):               # chunks: a diverging variant costs 3 timeouts, the spawn cap is 5 s
            r = E.run([E.judge_job(orig, fns, cands[lo:lo + 12], [], seed_ex, 0)])[0]
            if any(c["load"] == "ok" and not c["slow"] and c["grid_diff"] == 0 for c in r):
                bump("guard:second_repair")
                return False
        return True

    # ---- patch construction
    def _candidates(self, R, orig, mut, op, disp, groups, held, entry_params):
        out = []
        ops = tuple(M.OPERATORS) if held else TRAIN_ALL
        gold = changed_lines(orig, mut)
        
        def one(src, r):
            ss = list(_sites_c(src, ops))
            while ss:
                s = ss.pop(r.randrange(len(ss)))
                m = M.apply(src, s)
                if m and m != src:
                    return m
            return None

        for _ in range(3):
            out.append(("revert", orig))
        for new, ln in _eq_rewrites(orig, {l for l in range(1, 400) if l not in gold}):
            out.append(("equiv", new))
        for _ in range(5):
            m = one(mut, R)
            if m:
                out.append(("edit1", m))
                m2 = one(m, R)
                if m2:
                    out.append(("edit2", m2))
            fp = one(orig, R)
            if fp:
                out.append(("fix_plus", fp))
        for good in (True, False):
            hc = self._hardcode(mut, disp, groups, entry_params, good)
            if hc:
                out.append(("hard_good" if good else "hard_bad", hc))
        return out

    @staticmethod
    def _hardcode(mut, disp, groups, params, good: bool):
        tree = ast.parse(mut)
        fn = [n for n in tree.body if isinstance(n, ast.FunctionDef)][-1] if params else None
        if fn is None:
            return None
        ins = []
        for (call, exp), g in zip(disp, groups):
            if g == "p2p":
                continue
            args = ast.literal_eval("(" + call[call.index("(") + 1:-1] + ",)")
            cond = " and ".join(f"{p} == {a!r}" for p, a in zip(params, args))
            val = exp if good else _perturb(exp)
            ins.append(ast.parse(f"if {cond}:\n    return {val}").body[0])
        fn.body[1:1] = ins
        return ast.unparse(ast.fix_missing_locations(tree))

    @staticmethod
    def size_sig(mut: str, src: str, diff: str) -> tuple:
        """(changed-lines bin, token-edit bin) of a patch: the two size classes the label-blind draw balances."""
        ta, tb = re.findall(r"\w+|[^\w\s]", mut), re.findall(r"\w+|[^\w\s]", src)
        tok = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in
                  difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes() if op != "equal")
        return PT.diff_bin(PT.stats(diff)["changed"]), (0 if tok <= 5 else (1 if tok <= 9 else 2))

    @staticmethod
    def _sig(mut: str, src: str) -> tuple:
        """Size signature of the patch mut -> src (the A42-D 3.2 diff-size features): hunks, added, removed, token edit, token hunks."""
        st = PT.stats(PT.make_diff(mut, src, TX.FILE))
        ops = [o for o in difflib.SequenceMatcher(None, re.findall(r"\w+|[^\w\s]", mut), re.findall(r"\w+|[^\w\s]", src),
                                                  autojunk=False).get_opcodes() if o[0] != "equal"]
        return (st["hunks"], st["added"], st["removed"], sum(max(i2 - i1, j2 - j1) for _, i1, i2, j1, j2 in ops), len(ops))

    def _patch(self, R, key, prog, orig, mut, op, disp, groups, fns, seed_ex, plan, held, attempt, seed=0):
        """Patch = one core edit + one hard-coded guard for the target test + 0-2 harmless-looking rewrites (the same skeleton for
        every label; the number of rewrites is drawn from the row key), so the diff-size features carry no label. The label of every
        candidate is its execution class (judged on the G0 grid, then re-judged with the seeded cases)."""
        entry = [f for f in prog["fns"] if f["name"] == prog["entry"]][0]
        params = entry["params"]
        want_d = plan.gold_abstain
        # stratified: consecutive seeds cycle A, B, C. A D row is built like any other row (the SAME skeleton: core edit + guard +
        # rewrites, label drawn from the row key) and then made inapplicable (shifted header or one stale line), so the size and the
        # shape of the patch cannot tell D (w4: D patches used to be short single-hunk diffs, +3.5 pp in G6 d_meta)
        target = LABELS[int(uhash(key, "dskel") * 3)] if want_d else LABELS[seed % 3]
        ops = tuple(M.OPERATORS) if held else TRAIN_ALL
        gold_lines = set(changed_lines(orig, mut))
        tests = [(c, e) for c, e in disp]
        # hunk count drawn from the row key (label-blind) among the counts the program kind can reach: an 8-line function cannot hold
        # 3 hunks (3 context lines merge them), so asking for 3 there forced the relaxed, label-dependent draw (diff-size probe +3 pp)
        # w8: the SIZE SIGNATURE is not drawn; it is the reference's. A's core edit is fixed by the bug (the original line, or an equivalent
        # rewrite of it drawn from the KEY, not from the label), so its size is a property of the program and the bug. The reference is A's own
        # core + guard (no rewrites); B and C must reproduce its (hunks, added, removed, token edit, token hunks) exactly, so
        # P(size signature | label) is equal by construction. Rewrites (n_pad, from the key) come after and add the same way for every label.
        R_ref = random.Random(f"{key}|{self._salt}ref")
        eqs_ref = _eq_rewrites(orig, {l for l in range(1, 400) if l not in gold_lines}) if R_ref.random() < 0.3 else []
        ref_core = R_ref.choice(eqs_ref)[0] if eqs_ref else orig
        ref_src = self._hardcode(ref_core, disp, groups, params, True)
        if ref_src is None:
            bump("patch:no_ref")
            return None
        sig_ref = self._sig(mut, ref_src)
        for batch in range(8):
            Rb = random.Random(f"{key}|{self._salt}{attempt}|b{batch}")
            n_pad = int(uhash(key, "pads") * 3)                 # 0-2 rewrites, drawn from the row key (the same for every label)

            def edit(src):
                ss = list(_sites_c(src, ops))
                while ss:
                    m = M.apply(src, ss.pop(Rb.randrange(len(ss))))
                    if m and m != src:
                        return m
                return None

            matched, seen = [], set()
            for _ in range(64):
                # every patch has the same skeleton: one core edit + one hard-coded guard for the target test + n_pad rewrites;
                # the label is decided by what the core edit and the guard value are (and by execution), never by the shape
                if target == "A":
                    core, good = ref_core, True
                elif target == "B":
                    core, good = edit(mut), Rb.random() < 0.5
                else:
                    core, good = edit(mut), True
                if core is None:
                    continue
                src = self._hardcode(core, disp, groups, params, good)
                if src is None:
                    continue
                if target != "A" and self._sig(mut, src) != sig_ref:
                    bump("patch:ref_sig_skip")
                    continue
                used = set(changed_lines(mut, src)) if len(src.split("\n")) == len(mut.split("\n")) else set()
                used |= gold_lines                         # w8: the bug line is closed to rewrites for every label (A's is already changed; B / C's was open)
                got_pads = 0
                for _p in range(n_pad):
                    rw = _one_rewrite(src, used, Rb)
                    if not rw:
                        break
                    src, ln = rw
                    used.add(ln)
                    got_pads += 1
                if got_pads < n_pad:                      # w8: a candidate with fewer rewrites than the key drew is rejected for every label
                    bump("patch:pad_short")               # (the realised count used to be 15% short for B, 19% for A, 20% for C)
                    continue
                if src == mut or src in seen:
                    continue
                seen.add(src)
                diff = PT.make_diff(mut, src, TX.FILE)
                if PT.apply_diff(mut, diff) == src:
                    matched.append(src)
                if len(matched) >= 40:
                    break
            if not matched:
                bump(f"patch:no_sig_{target}")
                continue
            res = E.run([E.judge_job(orig, fns, [(str(i), s) for i, s in enumerate(matched)], tests, seed_ex, 0)])[0]
            for src, r in zip(matched, res):
                lab = "B" if (r["load"] == "ok" and not r["slow"] and any(t != "p" for t in r["tests"])) else (
                    "C" if (r["load"] == "ok" and not r["slow"] and r["grid_diff"]) else (
                        "A" if r["load"] == "ok" and not r["slow"] else None))
                if lab != target:
                    continue
                full = E.run([E.judge_job(orig, fns, [("p", src)], tests, seed_ex)])[0][0]
                if E.label_of(full) != target:
                    bump("patch:seeded_disagrees")
                    continue
                diff = PT.make_diff(mut, src, TX.FILE)
                stt = PT.stats(diff)
                if want_d:
                    bad = self._inapplicable(diff, mut, Rb)
                    if bad is None:
                        bump("patch:d_no_corruption")
                        continue
                    return bad, None
                return diff, src
            bump(f"patch:no_{target}_in_sig")
        return None

    @staticmethod
    def _inapplicable(diff: str, mut: str, R):
        """The same diff made inapplicable: a patch for another version of the file (header shifted) or with one stale context /
        removed line. Same lines, same hunks, same size as an applying patch."""
        for _ in range(6):
            if R.random() < 0.5:
                d = PT.shift_header(diff, R.choice([-2, -1, 1, 2, 3]))
            else:
                ls = diff.split("\n")
                idx = [i for i, ln in enumerate(ls) if ln[:1] in (" ", "-") and not ln.startswith("---") and ln[1:].strip()]
                if not idx:
                    continue
                i = idx[R.randrange(len(idx))]
                body = ls[i][1:]
                m = re.search(r"\d", body)
                if m:
                    body = body[:m.start()] + str((int(m.group()) + 1 + R.randrange(8)) % 10) + body[m.end():]
                else:
                    m = re.search(r"[a-z]", body)
                    if not m:
                        continue
                    body = body[:m.start()] + chr((ord(m.group()) - 97 + 1 + R.randrange(24)) % 26 + 97) + body[m.end():]
                ls[i] = ls[i][0] + body
                d = "\n".join(ls)
            if d != diff and PT.parse_diff(d) and PT.apply_diff(mut, d) is None:
                return d
        return None

    def _d_patch(self, R, orig, mut, held):
        ops = tuple(M.OPERATORS) if held else TRAIN_ALL
        for _ in range(8):
            if R.random() < 0.5:
                ss = list(_sites_c(orig, ops))
                if not ss:
                    continue
                m2 = M.apply(orig, ss[R.randrange(len(ss))])
                if not m2 or m2 == mut:
                    continue
                d = PT.make_diff(m2, orig, TX.FILE)
            else:
                d = PT.make_diff(mut, orig, TX.FILE)
                d = PT.shift_header(d, R.choice([-2, -1, 1, 2, 3]))
            if PT.parse_diff(d) and PT.apply_diff(mut, d) is None:
                return d
        return None

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        st = spec.structure
        head = st["head"]
        orig, code, fns = st["orig"], st["code"], st["fns"]
        tests = [(c, e) for c, e, _ in st["tests"]]
        seed = st["exseed"]
        if head == "pv":
            if st["patch"] is None:
                raise ContractError("a patch row without a patch")
            patched = PT.apply_diff(code, st["patch"])
            if patched is None:
                return "D"
            if st.get("patched") is not None and patched != st["patched"]:
                raise ContractError("the stored patched source differs from the applied patch")
            r = E.run([E.judge_job(orig, fns, [("p", patched)], tests, seed)])[0][0]
            lab = E.label_of(r)
            if lab is None:
                raise ContractError("the patched code cannot be judged (load error, timeout or ambiguous seeded difference)")
            return lab
        if code == orig:
            r = E.run([E.judge_job(orig, fns, [("m", code)], tests, seed, 0)])[0][0]
            if any(t != "p" for t in r["tests"]):
                raise ContractError("none row with a failing test")
            return "none"
        if head == "ll":
            diff = changed_lines(orig, code)
            reverts = []
            for ln in diff:
                lines = code.split("\n")
                lines[ln - 1] = orig.split("\n")[ln - 1]
                reverts.append((ln - 2, "\n".join(lines)))
        else:
            a, b = fn_segments(orig), fn_segments(code)
            reverts = [(k, code.replace(b[k], a[k])) for k in a if a[k] != b[k]]
        r = E.run([E.judge_job(orig, fns, [("m", code)] + [(str(i), s) for i, (_, s) in enumerate(reverts)], tests, seed, 0)])[0]
        if all(t == "p" for t in r[0]["tests"]):
            raise ContractError("the shown code passes every test")
        good = [reverts[i][0] for i, x in enumerate(r[1:]) if all(t == "p" for t in x["tests"]) and x["grid_diff"] == 0]
        if len(good) != 1:
            raise ContractError(f"reverting the gold hunk must turn the failing tests green: {good}")
        return f"L{good[0]}" if head == "ll" else good[0]

    def canonical(self, spec: Spec) -> dict:
        st = spec.structure
        return {"qform": spec.qform, "code": st["code"], "tests": [list(t) for t in st["tests"]],
                "report": list(st["report"]), "patch": st["patch"]}

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def code_block(st: dict) -> str:
        lines = st["code"].split("\n")
        if st["head"] != "ll":
            return "\n".join(lines)
        out = []
        for i, ln in enumerate(lines):
            out.append(f"{i - 1:>2} | {ln}" if i >= 2 else f"   | {ln}")
        return "\n".join(out)

    @staticmethod
    def tests_block(st: dict) -> str:
        t = st["tests"]
        if st["head"] != "pv":
            pad = (lambda s: s.ljust(LINE_WIDTH + 8)) if st["head"] == "ll" else (lambda s: s)
            return "\n".join(pad(f"  t{i + 1}  {c} == {e}") for i, (c, e, _) in enumerate(t))
        a = [f"  t{i + 1}  {c} == {e}" for i, (c, e, g) in enumerate(t) if g == "f2p"]
        b = [f"  t{i + 1}  {c} == {e}" for i, (c, e, g) in enumerate(t) if g == "p2p"]
        return "Target test:\n" + "\n".join(a) + (("\nOther tests:\n" + "\n".join(b)) if b else "")

    @staticmethod
    def run_block(st: dict) -> str:
        lines, nf = [], 0
        for i, r in enumerate(st["report"]):
            if r == "p":
                lines.append(f"  t{i + 1} pass, got {st['tests'][i][1]}")
            elif r.startswith("f:"):
                nf += 1
                lines.append(f"  t{i + 1} FAIL, got {r[2:]}")
            else:
                nf += 1
                lines.append(f"  t{i + 1} ERROR, raised {r[2:]}")
        if st["head"] == "ll":                      # padded like the code: the length of the run (the got values) told the line
            lines = [ln.ljust(LINE_WIDTH + 8) for ln in lines]
        return "\n".join(lines)

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        st = spec.structure
        head = st["head"]
        hk = "pvl" if (head == "pv" and st["kind"] == "line") else ("pvm" if head == "pv" else head)
        key = row_key(spec.seed, spec.sampler, hk)
        held = spec.sampler in HELD_OUT_SAMPLERS
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        reg = skin.register
        tb = TextBuilder()
        secs = [("code", self.code_block(st)), ("tests", self.tests_block(st)), ("run", self.run_block(st))]
        if head == "pv":
            secs.append(("patch", st["patch"]))
        tb.add("state", "\n\n".join(decorate(reg, sid, body) for sid, body in secs), skin_id=skin.skin_id)
        tb.add("instructions", TX.RULES[spec.qform]).add("instructions", "\n\n")
        tb.add("instructions", wording.fill(spec.all_slots(), forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        plan = self.plan_for(hk, key, st["n_choices"])
        if plan.show_abstain != self.QFORMS[spec.qform].abstain:
            raise ContractError("plan and question form disagree about the abstain option")
        if head == "ll":
            closed, ab, rk = [f"L{i}" for i in range(1, 7)], ("none", TX.NONE_TEXT["ll"]), lambda k: "line " + k[1:]
        elif head == "lf":
            closed, ab, rk = [f["name"] for f in st["fns"]], ("none", TX.NONE_TEXT["lf"]), str
        else:
            closed, ab, rk = list(LABELS), ("D", TX.OPT["D"]), lambda k: TX.OPT[k]
        os_ = build_closed(spec, ans, closed, self.error_models(), row_key=key, render_key=rk, abstain=ab, plan=plan)
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms, attack=attack)

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        st = spec.structure
        out = []

        def meta(**kw):
            return spec.replace(structure={**st, **kw})

        t = [list(x) for x in st["tests"]]
        rep = list(st["report"])
        if len(t) >= 2:
            idx = list(range(len(t)))
            idx = idx[1:] + idx[:1] if st["head"] != "pv" else idx
            if st["head"] == "pv":
                # reorder the listing within each group: swap the first two tests of the larger group
                grp = [i for i, x in enumerate(t) if x[2] == "p2p"]
                if len(grp) >= 2:
                    idx[grp[0]], idx[grp[1]] = idx[grp[1]], idx[grp[0]]
            if idx != list(range(len(t))):
                out.append(RelationProposal("metamorphic", spec=meta(tests=[t[i] for i in idx], report=[rep[i] for i in idx]),
                                            expect="same", note="reorder the test listing"))
        if len(st["spare"]) >= 2:
            g2 = "p2p" if st["head"] == "pv" else "t"
            out.append(RelationProposal("metamorphic", spec=meta(tests=t + [[c, e, g2] for c, e in st["spare"][:2]],
                                                                 report=rep + ["p", "p"]), expect="same",
                                        note="add two tests that pass before and after"))
        if st["spare"]:
            c, e = st["spare"][0]
            g = "p2p" if st["head"] == "pv" else "t"
            out.append(RelationProposal("metamorphic", spec=meta(tests=t + [[c, e, g]], report=rep + ["p"]), expect="same",
                                        note="add a test that passes before and after"))
        if st["head"] == "pv":
            dead = "\n\ndef unused_helper(a: int) -> int:\n    \"\"\"Equals a + 1.\"\"\"\n    return a + 1"
            p2 = st["patch"]
            out.append(RelationProposal("metamorphic", spec=meta(code=st["code"] + dead, orig=st["orig"] + dead,
                                                                 patched=(st["patched"] + dead) if st["patched"] else None,
                                                                 fns=st["fns"] + [{"name": "unused_helper", "types": ["int"]}]),
                                        expect="same", note="append an unused function"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def neighbour(spec):
            st = spec.structure
            if st["head"] != "ll" or st["target"] is None or st["code"] == st["orig"]:
                return None
            j = st["target"] + 1
            return f"L{j + 1 if j < 6 else j - 1}"

        def blame_caller(spec):
            st = spec.structure
            if st["head"] != "lf" or st["code"] == st["orig"]:
                return None
            return st["entry"]

        def trust(spec):
            st = spec.structure
            return "A" if st["head"] == "pv" else None

        def ignore(spec):
            st = spec.structure
            return "A" if st["head"] == "pv" else None
        return {"neighbour_line": error_model("neighbour_line", neighbour),
                "blame_caller": error_model("blame_caller", blame_caller),
                "trust_target_test": error_model("trust_target_test", trust),
                "ignore_tests": error_model("ignore_tests", ignore)}


def _perturb(exp: str) -> str:
    """A wrong expected value of the same printed size (the guard of a B patch is as long as the guard of a C patch)."""
    try:
        v = ast.literal_eval(exp)
    except (ValueError, SyntaxError):
        return exp
    if isinstance(v, bool):
        return repr(not v)
    if isinstance(v, int):
        return repr(v + 1)
    if isinstance(v, list):
        return repr([v[0] + 1] + v[1:]) if v else "[1]"
    if isinstance(v, str):
        return repr(v[:-1] + ("x" if v[-1:] != "x" else "y")) if v else "'x'"
    return exp


def sealed_rows(n: int, start_seed: int = 0, samplers: tuple = ("S5",)) -> list:
    """The sealed entry point (A42-D 13.1): n held-out specs from HELD_OUT_SAMPLERS, as (spec, rendered row) pairs.
    Called by a sealed agent only, never by a training run:  sealed_rows(500, start_seed=SEALED_SEED)."""
    plugin, ctx = make_plugin()
    out, seed = [], start_seed
    while len(out) < n:
        spec = plugin.sample(seed, samplers[0])
        out.append((spec, plugin.render(spec, ctx)))
        seed += 1
    return out
