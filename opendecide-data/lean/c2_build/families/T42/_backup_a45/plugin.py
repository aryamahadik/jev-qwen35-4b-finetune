"""families/T42/plugin.py: T42 CODE-EXEC (code execution reasoning), a C2 family plugin (A42).

Semantics: G0_SPEC.md (frozen; sha in T42Plugin.G0_SHA256). Two heads:
  output head   ch_output / ch_return: "what does this Python snippet print / what does `result` hold, or which
                exception does it raise?" 4-5 options. Gold = the hermetic execution of the shown program; every wrong
                option is the real output of a MUTANT of the shown program (one named near-miss edit, or two).
  equivalence   ch_equiv: SAME / DIFFERS_TYPICAL / DIFFERS_EDGE for two functions printed through one printer. DIFFERS
                needs a witness found by execution; SAME needs the full grid, 10K fuzz and >= 95% branch coverage.

  solver A   hermetic execution (executor.py: venv CPython 3.12, PYTHONHASHSEED=0, subprocess, 5 s cap, temp dir, no
             network / writes; two runs must agree)                                            paradigm simulator
  solver B   solver_b.py: its own parser of the rendered row, a tree-walking interpreter of the shown AST, exhaustive
             enumeration of the G0 grids for equivalence                                 paradigm independent_interpreter
  samplers   S1 output (short programs); S2 return form; S3 equivalence; S4 output / return mix; S5 held out (idiom
             buckets closure / late binding and MRO, mutation operators swap_args and wrong_slice_bound, layouts numbered
             and tabs; equivalence rows 25%)
  relations  G4 metamorphic only (rename locals, add a dead statement, swap which function is f, swap in a mutant)
Surface text is program text only (rules, wordings); the wordings are admitted in the lexicon by program stand-ins, the
Haiku admission comes later (BUILD_NOTES.md).
"""
from __future__ import annotations

import ast
import collections
import difflib
import hashlib
import random
import re
from pathlib import Path

from c2_kit import plugin as KP
from c2_kit.choiceplan import plan_choice
from c2_kit.distractors import build_closed, build_options, error_model, register_name, uhash
from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row
from c2_kit.skin import RenderError, make_skin

from . import executor as E
from . import gen_eq as GE
from . import gen_out as GO
from . import mutate as M
from . import texts as TX

HERE = Path(__file__).resolve().parent
FAMILY = "T42"
KP.FAMILIES.setdefault(FAMILY, "agent")           # kit candidate: add T40-T42 to plugin.FAMILIES (runtime registration)

SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
HELD_OUT_SAMPLERS = ("S5",)
REGISTERS = ("fenced", "plain", "headed", "task_intro", "md_quote", "narrow", "numbered", "tabs")
HELD_OUT_REGISTERS = ("numbered", "tabs")
STYLES = ("short", "long")
TRAIN_OPS = tuple(o for o in M.OPERATORS if o not in M.HELD_OUT_OPS and o not in M.BUCKET_OPS)
S5_OPS = tuple(M.OPERATORS)
ALL_OPS = tuple(M.OPERATORS) + ("compound",)
EXC_OPS = ("repair_failure",)
STEP_RANGE = {1: (2, 40), 2: (2, 120), 3: (2, 300)}      # executed line events of the shown program: the trace cap, per bin
P_EXC_ROW = 0.20                                           # rows of the exception idiom
Q_EXC = 0.5                                                # in those rows one option is an exception w.p. Q_EXC
VALUE_MAX = 12                                             # exception rows: value options are shorter than any 'raises X' text
MUT_PER_OP, MUT_MAX, COMPOUND_N = 6, 64, 6
DIFF_EDGES = (7, 14, 24)                                    # token-diff bins of an equivalence pair: <=7, 8-14, 15-24, 25+
DIFF_W = (1, 1, 1, 1)
LABELS = TX.LABELS
EQ_ATTEMPTS, OUT_ATTEMPTS = 120, 160
# skeletons that cannot yield every label at a similar rate (measured, 24 tries per label): excluded, so each skeleton
# carries the label thirds and the skeleton's code says nothing about the label
EQ_EXCLUDED = ("fizz_count", "pair_sum_target", "palin", "vowels_tail")
EXC_ATTEMPTS, EXC_BLOCK = 320, 8
EXC_CLASSES = ("KeyError", "IndexError", "ZeroDivisionError")
DIAG = collections.Counter()                                # rejection reasons of the sampling loops (BUILD_NOTES)

COMPOUND_TEXT = "applies two different near-miss edits to the shown program"
register_name("compound", COMPOUND_TEXT)
for _op, _d in M.OPERATORS.items():
    register_name(_op, _d)
register_name("typical_only_check", "tests only ordinary inputs and calls two functions that differ on edge inputs the same")
register_name("edge_as_typical", "sees an edge-only difference and calls it a difference on ordinary inputs")
register_name("typical_as_edge", "sees a difference on ordinary inputs and thinks it needs an edge input")
register_name("same_as_differs", "calls two equivalent rewrites different because the text differs")


# ------------------------------------------------------------------------------------------------ layouts (registers)
def decorate(reg: str, code: str) -> str:
    if reg == "fenced":
        return f"```python\n{code}\n```"
    if reg == "plain":
        return code
    if reg == "headed":
        return "# snippet.py\n" + code
    if reg == "task_intro":
        return "Consider this Python program:\n" + code
    if reg == "md_quote":
        return "\n".join("> " + ln if ln else ">" for ln in code.split("\n"))
    if reg == "narrow":
        return "\n".join(re.sub(r"^((?:    )+)", lambda m: " " * (len(m.group(1)) // 2), ln) for ln in code.split("\n"))
    if reg == "numbered":
        return "\n".join(f"{i + 1:>2}  {ln}" for i, ln in enumerate(code.split("\n")))
    if reg == "tabs":
        return "\n".join(re.sub(r"^((?:    )+)", lambda m: "\t" * (len(m.group(1)) // 4), ln) for ln in code.split("\n"))
    raise ContractError(f"register {reg}")


def make_ctx() -> KitCtx:
    """Lexicon (program stand-ins admit the question wordings) + register skins + wording skins. In memory only."""
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
        sk = make_skin(f"T42-SK-{r}", FAMILY, f"{r.replace('_', ' ')} layout", {}, kind="skin", register=r,
                       held_out=r in HELD_OUT_REGISTERS)
        skins[sk.skin_id] = sk
    for qf, ws in TX.WORDINGS.items():
        for i, w in enumerate(ws):
            sk = make_skin(f"T42-W-{qf}-{i}", FAMILY, w, {}, kind="wording", register="question", qform=qf,
                           lexicon_ids=(form_of[(qf, w)],))
            skins[sk.skin_id] = sk
    return KitCtx(skins=skins, lexicon=reg)


def make_plugin() -> tuple:
    ctx = make_ctx()
    return T42Plugin(lexicon=ctx.lexicon), ctx


# ------------------------------------------------------------------------------------------------ helpers
def row_key(seed: int, sampler: str, qform: str) -> str:
    return f"{FAMILY}|{seed}|{sampler}|{qform}"


def norm(src: str) -> str:
    return ast.unparse(ast.parse(src))


def key_text(k: str) -> str:
    return "raises " + k[4:] if k.startswith("exc:") else k[4:]


def _num(text: str):
    return float(text) if re.fullmatch(r"-?\d+(?:\.\d+)?", text) else None


def shape_of(text: str) -> tuple:
    """Coarse shape of an option text: everything a reader can see without running the program (container, sign,
    decimal point, letters). The sampler keeps all value options of a row in ONE shape, so the shape of an option
    (a negative number, a float, None ...) carries no information about the gold."""
    if text in ("None", "True", "False"):
        return (text,)
    return (text[:1] if text[:1] in "[({'\"" else "x", bool(re.search(r"-\d", text)), bool(re.search(r"\d\.\d", text)),
            bool(re.search(r"[A-Za-z]", text)))


TOK_RE = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")          # the pilot's token pattern (G6 / G7 features)
LAYOUT_WORDS = {"snippet", "py", "consider", "this", "python", "program"}


def toks(text: str) -> set:
    return set(TOK_RE.findall(text.lower()))


def context_tokens(code: str, qform: str) -> set:
    """Tokens a reader sees around the options: the code, the rules, every wording of the form, the layout words."""
    out = toks(code) | toks(TX.RULES[qform]) | LAYOUT_WORDS
    for w in TX.WORDINGS[qform]:
        out |= toks(w)
    return out


def ov_class(text: str, ctx_toks: set) -> int:
    """0: no token of the option is in the visible text, 2: all of them are, 1: some. The pilot's overlap feature takes
    these extremes for the gold much more often than for a mutant's output, so every value option of a row shares the class."""
    t = toks(text)
    if not t:
        return 0
    f = len(t & ctx_toks) / len(t)
    return 0 if f == 0 else (2 if f == 1 else 1)


def sim_rank_ok(texts: list, gi: int, target: int) -> bool:
    """The gold's rank by total similarity to the other options (0 = least central) can be `target` under some tie
    break: the medoid cue (the option most like all the others) is then at chance."""
    sims = []
    for i, a in enumerate(texts):
        sims.append(sum(difflib.SequenceMatcher(None, a, b).ratio() for j, b in enumerate(texts) if j != i))
    less = sum(s < sims[gi] - 1e-9 for s in sims)
    ties = sum(abs(s - sims[gi]) <= 1e-9 for j, s in enumerate(sims) if j != gi)
    return less <= target <= less + ties


def tok_diff(f_src: str, g_src: str) -> tuple:
    """(token diff size, changed lines): both sources printed by the same printer, function name normalised."""
    g2 = re.sub(r"\bdef g\(", "def f(", g_src, count=1)
    tf, tg = re.findall(r"\w+|[^\w\s]", f_src), re.findall(r"\w+|[^\w\s]", g2)
    size = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, tf, tg, autojunk=False).get_opcodes():
        if op != "equal":
            size += max(i2 - i1, j2 - j1)
    lf, lg = f_src.split("\n"), g2.split("\n")
    lines = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in
                difflib.SequenceMatcher(None, lf, lg, autojunk=False).get_opcodes() if op != "equal")
    return size, lines


def diff_bin(size: int) -> int:
    return sum(size > e for e in DIFF_EDGES)


def _pick(u: float, weights) -> int:
    tot, acc = float(sum(weights)), 0.0
    for i, w in enumerate(weights):
        acc += w / tot
        if u < acc:
            return i
    return len(weights) - 1


def _fuzz_seed(f: str, g: str) -> int:
    return int(hashlib.sha256((f + "\x00" + g).encode()).hexdigest()[:8], 16)


class T42Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "6b3934f5e4715ee3251a46031f0754fc9f54614b89824bba6a09a88c570dcac7"   # G0 v1.0 (14 Oct 2026)
    SAMPLERS = SAMPLERS
    HELD_OUT_SAMPLERS = HELD_OUT_SAMPLERS
    PARADIGM_A = "simulator"
    PARADIGM_B = "independent_interpreter"
    SOLVER_B_MODULE = "families.T42.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("ch_output", "choice", answer_set="open"),
        QuestionForm("ch_return", "choice", answer_set="open"),
        QuestionForm("ch_equiv", "choice", answer_set="closed"),
    )}
    LABEL_WORDS = ("same", "differs", "typical", "edge")
    CLOSED_WORLD_SENTENCE = "No input is read and nothing outside the snippet affects the result."
    REGISTERS = REGISTERS
    HELD_OUT_REGISTERS = HELD_OUT_REGISTERS
    NAME_ALLOW = ("Python",)
    YES_NO_ONLY = False

    # ------------------------------------------------------------------------------------------- sampling
    def _qform(self, sampler: str, seed: int) -> str:
        u = uhash(FAMILY, "qform", sampler, seed)
        if sampler == "S1":
            return "ch_output"
        if sampler == "S2":
            return "ch_return"
        if sampler == "S3":
            return "ch_equiv"
        if sampler == "S4":
            return "ch_output" if u < 0.5 else "ch_return"
        return "ch_equiv" if u < 0.25 else ("ch_output" if u < 0.625 else "ch_return")

    def _bin(self, sampler: str, seed: int) -> int:
        u = uhash(FAMILY, "bin", sampler, seed)
        lo, hi = {"S1": (1, 2), "S2": (2, 3), "S3": (1, 3), "S4": (1, 3), "S5": (1, 3)}[sampler]
        return lo + min(hi - lo, int(u * (hi - lo + 1)))

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        qform = self._qform(sampler, seed)
        if qform == "ch_equiv":
            return self._sample_equiv(seed, sampler)
        return self._sample_output(seed, sampler, qform)

    # ---- output head
    def _mutants(self, code: str, R: random.Random, ops: tuple, per_op: int = MUT_PER_OP, n_comp: int = COMPOUND_N) -> list:
        sites = M.sites(code, ops)
        by_op: dict = {}
        for s in sites:
            by_op.setdefault(s[0], []).append(s)
        chosen = []
        for op in sorted(by_op):
            lst = by_op[op]
            R.shuffle(lst)
            chosen += lst[:per_op]
        R.shuffle(chosen)
        out, seen = [], {code}
        for s in chosen[:MUT_MAX if per_op <= MUT_PER_OP else 3 * MUT_MAX]:
            m = M.apply(code, s)
            if m is not None and m not in seen:
                seen.add(m)
                out.append(((s[0],), m))
        firsts = list(out)
        for _ in range(n_comp):
            if not firsts:
                break
            (op1,), m1 = R.choice(firsts)
            s2 = M.sites(m1, ops)
            s2 = [s for s in s2 if s[0] != op1]
            if not s2:
                continue
            s = R.choice(s2)
            m2 = M.apply(m1, s)
            if m2 is not None and m2 not in seen:
                seen.add(m2)
                out.append(((op1, s[0]), m2))
        return out

    def _select(self, pool: list, hub: dict, plan, m_exc: int, held: bool, R: random.Random, qform: str, key: str):
        """The k options of an output row: the HUB (the generated program's own output) plus k - 1 mutant outputs. The
        shown program is the member whose visible-length rank is the planned one (label-blind, from the row key), so it
        is the hub only 1 time in k: the hub is the centre of the star of mutants (the most central option, the one
        whose numbers sit inside the generator's prior), and the gold is that centre exactly as often as chance.
        Constraints: every value option has one shape and one overlap class; m_exc options are exceptions (every value
        text is shorter than any `raises X`); the gold's similarity rank among the values is drawn from the row key."""
        sig = shape_of
        klen = lambda e: (len(key_text(e["key"])), key_text(e["key"]))  # noqa: E731
        hub_exc = hub["key"].startswith("exc:")
        n_exc_d = m_exc - int(hub_exc)
        n_val_d = plan.k - 1 - n_exc_d
        if n_exc_d < 0 or n_val_d < 0:
            DIAG["sel:kind_infeasible"] += 1
            return None
        exc_pool = [e for e in pool if e["key"].startswith("exc:")]
        val_pool = [e for e in pool if not e["key"].startswith("exc:")]
        if not hub_exc:
            hs = sig(key_text(hub["key"]))
            val_pool = [e for e in val_pool if sig(key_text(e["key"])) == hs]
        elif n_val_d:
            groups: dict = {}
            for e in val_pool:
                groups.setdefault(sig(key_text(e["key"])), []).append(e)
            ok = [g for g in groups.values() if len(g) >= n_val_d]
            val_pool = R.choice(ok) if ok else []
        if len(exc_pool) < n_exc_d or len(val_pool) < n_val_d:
            DIAG["sel:kind_pool_short"] += 1
            return None
        for t in range(120):
            pick = R.sample(exc_pool, n_exc_d) + R.sample(val_pool, n_val_d)
            members = [hub] + pick
            texts = [key_text(e["key"]).casefold() for e in members]
            if len(set(texts)) != len(texts):
                DIAG["sel:try_dup_text"] += 1
                continue
            order = sorted(members, key=klen)
            gold = order[plan.rank]
            vals = [e for e in order if not e["key"].startswith("exc:")]
            ctx_toks = context_tokens(gold["code"], qform)        # what a reader of the SHOWN program sees
            if len({ov_class(key_text(e["key"]), ctx_toks) for e in vals}) > 1:
                DIAG["sel:try_ov_class"] += 1
                continue
            if not gold["key"].startswith("exc:") and len(vals) >= 3:    # centrality among the value options
                vt = [key_text(e["key"]) for e in vals]
                nv = len(vt)
                if not sim_rank_ok(vt, vals.index(gold), min(nv - 1, int(uhash(key, "simrank") * nv))):
                    DIAG["sel:try_sim_rank"] += 1
                    continue
            if held and t < 60 and not any(set(e["ops"]) & set(M.HELD_OUT_OPS) for e in members):
                continue
            return members, gold
        return None

    def _gen(self, key, attempt, exc_row, held, d, style, gold_exc, kind, ops, xcls="KeyError"):
        """One candidate program of the output head with its mutants: (R, idiom, template, code, muts, jobs) or None."""
        R = random.Random(f"{key}|{attempt}")
        if exc_row:
            idiom, tpl = "exceptions", "exc_fail"
        elif held:
            idiom, tpl = GO.HELD_OUT_IDIOMS[R.randrange(len(GO.HELD_OUT_IDIOMS))], None
        else:
            idiom = GO.TRAIN_IDIOMS[R.randrange(len(GO.TRAIN_IDIOMS))]
            tpl = "exc_flow" if idiom == "exceptions" else None
        info: dict = {}
        setup, final, tname = GO.make(R, idiom, d, style, fail=gold_exc, template=tpl, exc_class=xcls, info=info)
        last = f"print({final})" if kind == "print" else f"result = {final}"
        try:
            code = norm(setup + "\n" + last)
        except SyntaxError:
            return None
        muts = self._mutants(code, R, ops, 20 if exc_row else MUT_PER_OP, 16 if exc_row else COMPOUND_N)
        if exc_row and gold_exc and "fixed" in info:      # value options of a failing program: its repaired versions
            try:
                fixed = norm(info["fixed"] + "\n" + last)
            except SyntaxError:
                fixed = None
            if fixed:
                muts = [(("repair_failure",), fixed)] + [(("repair_failure",) + o, m) for o, m in
                                                         self._mutants(fixed, R, ops, 10)] + muts
        jobs = [{"id": "base", "code": code, "kind": kind}] + \
               [{"id": f"m{i}", "code": m, "kind": kind} for i, (_, m) in enumerate(muts)]
        return R, idiom, tname, code, muts, jobs

    def _sample_output(self, seed: int, sampler: str, qform: str) -> Spec:
        key = row_key(seed, sampler, qform)
        plan = plan_choice(key, ks=(4, 5), abstain=False)
        held = sampler in HELD_OUT_SAMPLERS
        d = self._bin(sampler, seed)
        style = STYLES[min(1, int(uhash(key, "style") * 2))]
        exc_row = (not held) and uhash(key, "excrow") < P_EXC_ROW
        # exception rows: m of the k options are exceptions (m = 1 with probability Q_EXC, else 0); every value option
        # is shorter than every exception text, so with m = 1 the member with the longest text is the exception and the
        # gold (the member at the planned length rank) is that exception exactly 1 time in k
        m_exc = 1 if exc_row and uhash(key, "dk", 0) < Q_EXC else 0
        hub_fail = m_exc == 1 and uhash(key, "hubfail") < 0.5       # the generated program itself ends in the exception
        ops = S5_OPS if held else TRAIN_OPS
        kind = "result" if qform == "ch_return" else "print"
        xcls = EXC_CLASSES[min(2, int(uhash(key, "xcls") * 3))]          # the one exception class of an exception row
        lo, hi = STEP_RANGE[d]
        block = EXC_BLOCK if exc_row else 1
        n_att = EXC_ATTEMPTS if (exc_row or held) else OUT_ATTEMPTS
        gen = lambda a: self._gen(key, a, exc_row, held, d, style, hub_fail, kind, ops, xcls)  # noqa: E731
        for attempt in range(n_att):
            if block > 1 and attempt % block == 0:      # exception rows: one subprocess runs a block of candidates
                batch = []
                for j in range(attempt, min(n_att, attempt + block)):
                    c = gen(j)
                    batch += [] if c is None else [{**x, "id": f"b{j}.{x['id']}"} for x in c[5]]
                try:
                    E.run_snippets(batch)
                except E.ExecError:
                    DIAG["out:exec_error"] += 1
            c = gen(attempt)
            if c is None:
                DIAG["out:syntax"] += 1
                continue
            R, idiom, tname, code, muts, jobs = c
            try:
                res = E.run_snippets(jobs)
            except E.ExecError:
                DIAG["out:exec_error"] += 1
                continue
            hub_key = E.answer_key(res["base"])
            if hub_key is None:
                DIAG[f"out:no_answer:{tname}"] += 1
                continue
            if hub_key.startswith("exc:") != hub_fail or (exc_row and not hub_fail and len(key_text(hub_key)) > VALUE_MAX):
                DIAG[f"out:kind_mismatch:{tname}"] += 1
                continue
            if not lo <= res["base"]["steps"] <= hi:
                DIAG[f"out:steps_bin{d}"] += 1
                continue
            hub = {"key": hub_key, "ops": ["revert_edit"], "code": code, "steps": res["base"]["steps"]}
            pool: dict = {}
            for i, (mops, m) in enumerate(muts):
                k = E.answer_key(res[f"m{i}"])
                st_i = res[f"m{i}"]["steps"]
                if k is None or k == hub_key or not lo <= st_i <= hi or \
                        (k.startswith("exc:") and not (exc_row and k == "exc:" + xcls)) or \
                        (exc_row and not k.startswith("exc:") and len(key_text(k)) > VALUE_MAX):
                    continue
                e = pool.setdefault(k, {"key": k, "ops": [], "code": m, "steps": st_i})
                e["ops"] = sorted(set(e["ops"]) | set(mops))
            got = self._select(list(pool.values()), hub, plan, m_exc, held, R, qform, key)
            if got is None:
                DIAG[f"out:no_selection:{tname}"] += 1
                continue
            members, gold_m = got
            try:                    # the shown program and the shown distractors: a second, fresh run must agree
                E.run_snippets([{"id": f"c{i}", "code": e["code"], "kind": kind} for i, e in enumerate(members)],
                               confirm=True)
            except E.ExecError:
                DIAG["out:confirm_error"] += 1
                continue
            others = [e for e in members if e is not gold_m]
            structure = {"qform": qform, "idiom": idiom, "template": tname, "bin": d, "style": style,
                         "code": gold_m["code"], "kind": kind, "steps": gold_m["steps"],
                         "gold_kind": "exc" if gold_m["key"].startswith("exc:") else "out", "shown_is_hub": gold_m is hub,
                         "hub_code": code, "pool": len(pool), "attempt": attempt,
                         "distractors": [{"key": e["key"], "ops": e["ops"], "code": e["code"]} for e in others]}
            tags = (f"idiom:{idiom}", f"bin:{d}", f"steps:{min(gold_m['steps'] // 25, 9)}") + \
                tuple(sorted({f"err:{o}" for e in others for o in e["ops"]}))
            card = f"{FAMILY}:{tname}:{xcls}:b{d}:{style}" if exc_row else f"{FAMILY}:{tname}:b{d}:{style}"
            card += f":v{min(2, int(uhash(key, 'cardv') * 3))}"
            return Spec(FAMILY, sampler, seed, card, qform, {}, structure=structure,
                        depth=d, deep=False, tags=tags, pack=idiom)
        raise ContractError(f"no output structure after {n_att} attempts ({key})")

    # ---- equivalence head
    def _build_pair(self, R: random.Random, sk_name: str, label: str, n_eq: int, rename: bool, ops: tuple) -> tuple:
        sk = GE.SKELETONS[sk_name](R)
        pts = sk["points"]
        base = {p: R.choice(v["A"]) for p, v in pts.items()}
        f_ch, g_ch = dict(base), dict(base)
        movable = [p for p, v in pts.items() if len(v["A"]) >= 2]
        for p in R.sample(movable, min(n_eq, len(movable))):
            g_ch[p] = R.choice([v for v in pts[p]["A"] if v != f_ch[p]])
        mode = "same"
        if label != "SAME":
            cls = "typ" if label == "DIFFERS_TYPICAL" else "edge"
            have = [p for p, v in pts.items() if v[cls]]
            mode = "point" if have and R.random() < 0.65 else "mutate"
            if mode == "point":
                p = R.choice(have)
                g_ch[p] = R.choice(pts[p][cls])
        if R.random() < 0.5:
            f_ch, g_ch = g_ch, f_ch
        f_src, g_src = GE.pair_source(sk, f_ch, g_ch)
        op = None
        if mode == "mutate":
            tgt_is_g = R.random() < 0.5
            src = g_src if tgt_is_g else f_src
            sites = M.sites(src, ops)
            if not sites:
                return None
            s = R.choice(sites)
            m = M.apply(src, s)
            if m is None:
                return None
            op = s[0]
            f_src, g_src = (f_src, m) if tgt_is_g else (m, g_src)
        if rename:
            if R.random() < 0.5:
                g_src = GE.rename_locals(g_src, R)
            else:
                f_src = GE.rename_locals(f_src, R)
        if f_src == re.sub(r"\bdef g\(", "def f(", g_src, count=1):
            return None
        return f_src, g_src, sk["sig"], mode, op

    def _sample_equiv(self, seed: int, sampler: str) -> Spec:
        qform = "ch_equiv"
        key = row_key(seed, sampler, qform)
        label = LABELS[min(2, int(uhash(key, "label") * 3))]
        dbin = _pick(uhash(key, "dbin"), DIFF_W)
        held = sampler in HELD_OUT_SAMPLERS
        ops = S5_OPS if held else TRAIN_OPS
        names = [n for n in sorted(GE.SKELETONS) if n not in EQ_EXCLUDED]
        for attempt in range(EQ_ATTEMPTS):
            R = random.Random(f"{key}|{attempt}")
            sk_name = names[R.randrange(len(names))]
            n_eq = R.choice([1, 2, 3, 4]) if label == "SAME" else R.choice([0, 1, 2, 3])
            rename = R.random() < 0.35
            built = self._build_pair(R, sk_name, label, n_eq, rename, ops)
            if built is None:
                DIAG["eq:build_none"] += 1
                continue
            f_src, g_src, sig, mode, op = built
            size, lines = tok_diff(f_src, g_src)
            if diff_bin(size) != dbin:
                DIAG[f"eq:dbin_miss:{label}"] += 1
                continue
            try:
                res = E.run_equiv(f_src, g_src, sig, seed=_fuzz_seed(f_src, g_src))
            except E.ExecError:
                DIAG["eq:exec_error"] += 1
                continue
            got, witness = E.equiv_label(res)
            if got != label:
                DIAG[f"eq:label_miss:{label}->{got or str(witness)[:22]}"] += 1
                continue
            try:
                E.run_equiv(f_src, g_src, sig, seed=_fuzz_seed(f_src, g_src), confirm=True)
            except E.ExecError:
                DIAG["eq:confirm_error"] += 1
                continue
            d = 1 + min(2, dbin // 2 + (1 if len(sig) == 2 and dbin >= 1 else 0))
            structure = {"qform": qform, "skeleton": sk_name, "sig": list(sig), "f": f_src, "g": g_src, "label": label,
                         "witness": witness, "mode": mode, "mut_op": op, "n_eq": n_eq, "rename": rename,
                         "tok_diff": size, "line_diff": lines, "diff_bin": dbin, "attempt": attempt,
                         "typ_frac": round(res["typ_diff"] / res["n_typ"], 4), "coverage": E.coverage_of(res),
                         "fuzz_n": res["fuzz_n"]}
            return Spec(FAMILY, sampler, seed, f"{FAMILY}:eq:{sk_name}:b{d}:v{int(uhash(key, 'cardv') * 2)}", qform, {}, structure=structure, depth=d,
                        deep=False, tags=(f"skeleton:{sk_name}", f"bin:{d}", f"dbin:{dbin}"), pack=f"eq:{sk_name}")
        raise ContractError(f"no equivalence pair for {label}/dbin {dbin} after {EQ_ATTEMPTS} attempts ({key})")

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        st = spec.structure
        if spec.qform == "ch_equiv":
            res = E.run_equiv(st["f"], st["g"], tuple(st["sig"]), seed=_fuzz_seed(st["f"], st["g"]))
            label, _ = E.equiv_label(res)
            if label is None:
                raise ContractError(f"equivalence pair has no label: {E.equiv_label(res)[1]}")
            return label
        k = E.answer_key(E.run_one(st["code"], st["kind"]))
        if k is None:
            raise ContractError("the program has no usable output")
        return k

    def canonical(self, spec: Spec) -> dict:
        st = spec.structure
        if spec.qform == "ch_equiv":
            return {"qform": spec.qform, "f": st["f"], "g": st["g"]}
        return {"qform": spec.qform, "code": st["code"]}

    # ------------------------------------------------------------------------------------------- render
    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = row_key(spec.seed, spec.sampler, spec.qform)
        held = spec.sampler in HELD_OUT_SAMPLERS
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        st = spec.structure
        reg = skin.register
        tb = TextBuilder()
        if spec.qform == "ch_equiv":
            state = decorate(reg, st["f"]) + "\n" + TX.SEPARATOR + "\n" + decorate(reg, st["g"])
        else:
            state = decorate(reg, st["code"])
        tb.add("state", state, skin_id=skin.skin_id)
        tb.add("instructions", TX.RULES[spec.qform]).add("instructions", "\n\n")
        tb.add("instructions", wording.fill(spec.all_slots(), forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        if spec.qform == "ch_equiv":
            plan = plan_choice(key, closed=3)
            os_ = build_closed(spec, ans, list(LABELS), self.error_models(), row_key=key, render_key=str, plan=plan)
        else:
            if st.get("meta_check"):          # a G4 partner: never emitted, so its options need no plan
                os_ = build_options(spec, ans, self.error_models(), k=len(st["distractors"]) + 1, row_key=key + "|g4",
                                    render_key=key_text)
            else:
                plan = plan_choice(key, ks=(4, 5), abstain=False)
                os_ = build_options(spec, ans, self.error_models(), row_key=key, render_key=key_text, plan=plan,
                                    length_balance=True)
            if os_ is None:
                raise RenderError("the planned option set cannot be built from the stored distractors")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack)

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        st = spec.structure
        out = []
        R = random.Random(f"{FAMILY}|g4|{spec.seed}|{spec.sampler}")

        def meta(**kw):
            return spec.replace(structure={**st, **kw, "meta_check": True})

        if spec.qform == "ch_equiv":
            f2, g2 = GE.rename_locals(st["f"], R), GE.rename_locals(st["g"], R)
            pairs = []
            if (f2, g2) != (st["f"], st["g"]):
                out.append(RelationProposal("metamorphic", spec=meta(f=f2, g=g2), expect="same",
                                            note="rename the parameters and locals"))
                pairs.append((f2, g2))
            sw_f = re.sub(r"\bdef g\(", "def f(", st["g"], count=1)
            sw_g = re.sub(r"\bdef f\(", "def g(", st["f"], count=1)
            out.append(RelationProposal("metamorphic", spec=meta(f=sw_f, g=sw_g), expect="same",
                                        note="swap which function is f"))
            pairs.append((sw_f, sw_g))
            E.prefetch_equiv([(a, b, tuple(st["sig"]), _fuzz_seed(a, b)) for a, b in pairs])
            return out
        code = st["code"]
        tree = ast.parse(code)
        unsafe = any(isinstance(n, (ast.ClassDef, ast.Nonlocal, ast.Global)) for n in ast.walk(tree))
        if not unsafe:
            c2 = GE.rename_locals(code, R, skip=("result", "f", "g"))
            if c2 != code:
                out.append(RelationProposal("metamorphic", spec=meta(code=c2), expect="same",
                                            note="rename the variables"))
        out.append(RelationProposal("metamorphic", spec=meta(code=norm("_pad = 0\n" + code)), expect="same",
                                    note="add a dead statement"))
        if st["distractors"]:
            e = st["distractors"][0]
            rest = [{"key": self.solve_a(spec), "ops": e["ops"], "code": code}] + st["distractors"][1:]
            out.append(RelationProposal("metamorphic", spec=meta(code=e["code"], distractors=rest), expect=e["key"],
                                        note="swap in the first distractor's mutant"))
        E.run_snippets([{"id": f"p{i}", "code": o.spec.structure["code"], "kind": st["kind"]}
                        for i, o in enumerate(out)])             # the partners' gold: one spawn for all of them
        return out

    @staticmethod
    def _pad_fn(src: str) -> str:
        tree = ast.parse(src)
        for n in ast.walk(tree):
            if isinstance(n, ast.FunctionDef):
                n.body.insert(0, ast.parse("_pad = 0").body[0])
        return ast.unparse(tree)

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def nth(op, j):
            def fn(spec):
                if spec.qform == "ch_equiv":
                    return None
                hits = [e["key"] for e in spec.structure["distractors"] if op in e["ops"]]
                return hits[j] if len(hits) > j else None
            return fn
        out = {}
        for op in ALL_OPS:
            for j in range(4):
                name = op if j == 0 else f"{op}@{j + 1}"
                if j:
                    register_name(name, M.OPERATORS.get(op, COMPOUND_TEXT) + f" (variant {j + 1})")
                out[name] = error_model(name, nth(op, j))

        def eq(table):
            def fn(spec):
                if spec.qform != "ch_equiv":
                    return None
                return table.get(spec.structure["label"])
            return fn
        out["typical_only_check"] = error_model("typical_only_check", eq({"DIFFERS_EDGE": "SAME"}))
        out["edge_as_typical"] = error_model("edge_as_typical", eq({"DIFFERS_EDGE": "DIFFERS_TYPICAL"}))
        out["typical_as_edge"] = error_model("typical_as_edge", eq({"DIFFERS_TYPICAL": "DIFFERS_EDGE"}))
        out["same_as_differs"] = error_model("same_as_differs", eq({"SAME": "DIFFERS_TYPICAL"}))
        return out
