"""families/T44/plugin.py: T44 SEQ-CHECK (workflow routing), a C2 family plugin (A42, wave 2).

Semantics: G0_SPEC.md (sha in T44Plugin.G0_SHA256). Two heads over a tool algebra (typed predicates, preconditions with
negation, add / delete effects):
  ch_verdict  a plan (<= 6 steps in training, 7-8 held out): INVALID | STEP_k_NOT_APPLICABLE | GOAL_NOT_REACHED | VALID
  ch_next     the calls made so far + a goal: which of 4 calls can start a shortest sequence that makes the goal true
  solver A    forward state simulation (world.verdict) / layered BFS with first-move sets (world.explore)  paradigm simulator
  solver B    solver_b.py: its own parser of the rendered row + BACKWARD REGRESSION (weakest preconditions)   paradigm rule_engine
  samplers    S1 verdict (2-4 steps), S2 next (2-4 total calls), S3 verdict (4-6), S4 next (4-6),
              S5 held out (sealed split only): held-out domains (predicate / tool / type / object vocabularies), plan
              lengths 7-8, held-out layouts (hoare, colon); both heads
  relations   G4 metamorphic only (rename objects, rename tools and predicates, reorder the tool block, add an
              unusable tool); no twin / complement / equiv partners (choice-only family, like T42)
Gold is program-only; the label of a verdict row is drawn first (stratified over the seed) and the structure is searched
until solver A returns it (drops are redraws, never relabels).
"""
from __future__ import annotations

import itertools
import random
from pathlib import Path

from c2_kit import plugin as KP
from c2_kit.choiceplan import plan_choice
from c2_kit.distractors import build_closed, build_options, error_model, register_name, uhash
from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row
from c2_kit.skin import RenderError, make_skin

from . import texts as TX
from . import world as W

HERE = Path(__file__).resolve().parent
FAMILY = "T44"
KP.FAMILIES.setdefault(FAMILY, "agent")

SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
HELD_OUT_SAMPLERS = ("S5",)
REGISTERS = TX.TRAIN_REGISTERS + TX.HELD_OUT_REGISTERS
HELD_OUT_REGISTERS = TX.HELD_OUT_REGISTERS
LEN_RANGE = {"S1": (2, 4), "S2": (2, 4), "S3": (4, 6), "S4": (4, 6), "S5": (7, 8)}      # plan length / total calls
MAX_TRAIN_LEN = 6
HEAD_OF = {"S1": TX.HEAD_VERDICT, "S2": TX.HEAD_NEXT, "S3": TX.HEAD_VERDICT, "S4": TX.HEAD_NEXT}
GOAL_W = (0.4, 0.4, 0.2)                           # goal of 1 / 2 / 3 literals
CLASSES = ("inapp", "stuck")
CLASS_W = (0.5, 0.5)
ATTEMPTS = 300
DIAG = {}


def _diag(k):
    DIAG[k] = DIAG.get(k, 0) + 1


# error-model names (described for the G0 spec)
register_name("t44_skips_needs", "runs every step as if its needs always held, then checks the goal")
register_name("t44_ignores_deletes", "never removes facts, so earlier facts stay true")
register_name("t44_skips_malformed", "treats a malformed step as a step that does nothing")
register_name("t44_goal_unchecked", "calls a plan that runs to the end valid without looking at the goal")
for _c, _d in (("inapp", "a call whose needs do not hold in the current state"),
               ("stuck", "an applicable call that is on no shortest route: the goal is no nearer, or out of reach")):
    for _j in range(3):
        register_name(f"t44_{_c}" if _j == 0 else f"t44_{_c}@{_j + 1}", _d + ("" if _j == 0 else f" (variant {_j + 1})"))


def row_key(seed: int, sampler: str, qform: str) -> str:
    return f"{FAMILY}|{seed}|{sampler}|{qform}"


def _pick(u: float, weights) -> int:
    tot, acc = float(sum(weights)), 0.0
    for i, w in enumerate(weights):
        acc += w / tot
        if u < acc:
            return i
    return len(weights) - 1


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
        sk = make_skin(f"T44-SK-{r}", FAMILY, f"{r} layout", {}, kind="skin", register=r, held_out=r in HELD_OUT_REGISTERS)
        skins[sk.skin_id] = sk
    for qf, ws in TX.WORDINGS.items():
        for i, w in enumerate(ws):
            sk = make_skin(f"T44-W-{qf}-{i}", FAMILY, w, {}, kind="wording", register="question", qform=qf,
                           lexicon_ids=(form_of[(qf, w)],))
            skins[sk.skin_id] = sk
    return KitCtx(skins=skins, lexicon=reg)


def make_plugin() -> tuple:
    ctx = make_ctx()
    return T44Plugin(lexicon=ctx.lexicon), ctx


# ------------------------------------------------------------------------------------------------ text of a row
def tool_entry(t: dict, reg: str, i: int) -> str:
    R = TX.REGISTERS[reg]
    sig = f"{t['name']}({', '.join(f'{v}: {ty}' for v, ty in t['params'])})"
    clauses = []
    needs = [("not " if n else "") + f"{p}({', '.join(a)})" for n, p, a in t["needs"]]
    adds = [f"{p}({', '.join(a)})" for p, a in t["adds"]]
    dels = [f"{p}({', '.join(a)})" for p, a in t["dels"]]
    for lab, items in zip(R["labels"], (needs, adds, dels)):
        if items:
            clauses.append(f"{lab} {R['item_sep'].join(items)}")
    body = R["clause_sep"].join(clauses)
    if "\n" in R["clause_sep"]:
        body = R["clause_sep"] + body
    return R["prefix"].replace("{i}", str(i)) + sig + R["sig_sep"] + body + R["suffix"]


def state_text(st: dict, reg: str) -> str:
    out = [TX.H_TOOLS] + [tool_entry(t, reg, i + 1) for i, t in enumerate(st["alg"]["tools"])]
    objs = "; ".join(f"{', '.join(v)} ({ty})" for ty, v in st["objects"].items())
    start = ", ".join(f"{p}({', '.join(a)})" for p, a in st["start"]) or TX.NOTHING
    goal = ", ".join(("not " if n else "") + f"{p}({', '.join(a)})" for n, p, a in st["goal"])
    out += [f"{TX.H_OBJECTS} {objs}", f"{TX.H_START} {start}", f"{TX.H_GOAL} {goal}"]
    if st["qform"] == TX.HEAD_VERDICT:
        out.append(TX.H_PLAN)
        out += [f"{i}. {W.call_text(n, a)}" for i, (n, a) in enumerate(st["plan"], 1)]
    else:
        out.append(TX.H_CALLS)
        out += [f"{i}. {W.call_text(n, a)}" for i, (n, a) in enumerate(st["prefix"], 1)] or [TX.NONE_YET]
    return "\n".join(out)


class T44Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "356835aa072556d7eefac7253f3cc9808601e1f83dcae030d7220f4d03642e78"
    SAMPLERS = SAMPLERS
    HELD_OUT_SAMPLERS = HELD_OUT_SAMPLERS
    PARADIGM_A = "simulator"
    PARADIGM_B = "rule_engine"
    SOLVER_B_MODULE = "families.T44.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm(TX.HEAD_VERDICT, "choice", answer_set="closed"),
        QuestionForm(TX.HEAD_NEXT, "choice", answer_set="open"),
    )}
    LABEL_WORDS = TX.LABEL_WORDS
    CLOSED_WORLD_SENTENCE = "Only the listed tools, objects and facts exist; nothing else is true or can be called."
    REGISTERS = REGISTERS
    HELD_OUT_REGISTERS = HELD_OUT_REGISTERS
    NAME_ALLOW = ()
    YES_NO_ONLY = False

    # ------------------------------------------------------------------------------------------- sampling
    def _head(self, sampler: str, seed: int) -> str:
        if sampler in HEAD_OF:
            return HEAD_OF[sampler]
        return TX.HEAD_VERDICT if uhash(FAMILY, "head", sampler, seed) < 0.5 else TX.HEAD_NEXT

    def sample(self, seed: int, sampler: str, reseed: str = "") -> Spec:
        """One spec. `reseed` (default none) re-draws the structure of the SAME row cell (head, label, lengths, domain,
        algebra, gold rank, option classes) from an independent random stream: the 3% reseed audit (A42-D 3.3)."""
        if sampler not in SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        head = self._head(sampler, seed)
        if head == TX.HEAD_VERDICT:
            return self._sample_verdict(seed, sampler, reseed)
        return self._sample_next(seed, sampler, reseed)

    def _world(self, key: str, held: bool) -> tuple:
        doms = W.HELD_OUT_DOMAINS if held else W.TRAIN_DOMAINS
        dom = doms[min(len(doms) - 1, int(uhash(key, "dom") * len(doms)))]
        idx = min(W.ALGS_PER_DOMAIN - 1, int(uhash(key, "alg") * W.ALGS_PER_DOMAIN))
        return dom, idx, W.make_algebra(dom, idx)

    def _spec(self, seed, sampler, qform, dom, idx, structure, n) -> Spec:
        d = 1 if n <= 3 else (2 if n <= 5 else 3)
        return Spec(FAMILY, sampler, seed, f"{FAMILY}:{dom}:a{idx}", qform, {}, structure=structure, depth=d, deep=False,
                    tags=(f"dom:{dom}", f"len:{n}"), pack=dom)

    # ---- verdict head
    def _target(self, seed: int, sampler: str, n: int, kshow: int) -> str:
        perm = sorted(range(4), key=lambda i: uhash(FAMILY, "perm", sampler, seed // 4, i))
        lab = ("INVALID", "STEP", "GOAL_NOT_REACHED", "VALID")[perm[seed % 4]]
        return TX.V_STEP.format(k=kshow) if lab == "STEP" else lab

    def _bad_step(self, R, alg, objs, dom, step):
        name, args = step
        tools = {t["name"]: t for t in alg["tools"]}
        kinds = R.choices(("unknown", "arity", "type"), weights=(0.35, 0.15, 0.5))[0]
        if kinds == "unknown":
            absent = sorted(set(W.domain_tool_names(dom)) - set(tools))
            if absent:
                return [R.choice(absent), list(args)]
            kinds = "arity"
        if kinds == "type":
            t = tools[name]
            idxs = [i for i, (_, ty) in enumerate(t["params"]) if any(o != ty and objs[o] for o in objs)]
            if idxs:
                i = R.choice(idxs)
                other = [x for ty in sorted(objs) if ty != t["params"][i][1] for x in objs[ty]]
                a = list(args)
                a[i] = R.choice(other)
                return [name, a]
            kinds = "arity"
        a = list(args)
        if a and R.random() < 0.5:
            a.pop()
        else:
            a.append(R.choice([o for v in objs.values() for o in v]))
        return [name, a]

    @staticmethod
    def _counts(key: str, alg: dict) -> dict:
        """Objects per type, drawn from the row key (2 or 3), so the object list's length carries no label."""
        tys = sorted({ty for t in alg["tools"] for _, ty in t["params"]})
        return {ty: 2 + int(uhash(key, "nobj", ty) * 2) for ty in tys}

    @staticmethod
    def _tool_first(R, calls: list, arity: int | None = None):
        """A call picked tool-first: a uniform tool among the tools that have a candidate, then a uniform call of it (so
        binary tools, which have many more ground calls, are not over-represented in any label)."""
        by = {}
        for g in calls:
            if arity is None or len(g["call"][1]) == arity:
                by.setdefault(g["call"][0], []).append(g)
        if not by:
            return None
        return R.choice(by[R.choice(sorted(by))])

    def _label_plan(self, R, target, kshow, plan, goal, alg, objs, dom, s0, acts, states, sf):
        self._last_op = target
        n = len(plan)
        if target == "VALID":
            return plan, goal
        if target == "INVALID":
            self._last_op = "invalid"
            j = R.randrange(n)
            p2 = [list(x) for x in plan]
            p2[j] = self._bad_step(R, alg, objs, dom, plan[j])
            return p2, goal
        if target == "GOAL_NOT_REACHED":
            if R.random() < 0.5:
                gi = R.randrange(len(goal))
                old = goal[gi]
                pool = [(False, f) for f in sorted({f for g in acts for f in g["adds"]} - sf)]
                pool += [(True, f) for f in sorted(sf & {f for g in acts for f in g["dels"]})]
                pool = [(ng, f) for ng, f in pool if ng == old[0] and len(f[1]) == len(old[2])]     # same sign and arity
                if not pool:
                    return None
                neg, f = R.choice(pool)
                g2 = [list(x) for x in goal]
                g2[gi] = [neg, f[0], list(f[1])]
                if len({(x[0], x[1], tuple(x[2])) for x in g2}) < len(g2):
                    return None
                g2.sort(key=lambda x: (x[1], x[2], x[0]))
                self._last_op = "goal_swap"
                return plan, g2
            j = R.randrange(n)
            alt = [g for g in acts if W.applicable(g, states[j]) and list(g["call"][1]) != list(plan[j][1])
                   or (W.applicable(g, states[j]) and g["call"][0] != plan[j][0])]
            if not alt:
                return None
            g = self._tool_first(R, alt, len(plan[j][1]))
            if g is None:
                return None
            p2 = [list(x) for x in plan]
            p2[j] = [g["call"][0], list(g["call"][1])]
            self._last_op = "step_swap"
            return p2, goal
        # STEP_k
        k = kshow
        u = R.random()
        p2 = [list(x) for x in plan]
        if u < 0.25 and k < n:
            p2[k - 1], p2[k] = p2[k], p2[k - 1]
            self._last_op = "swap_adjacent"
            return p2, goal
        if u < 0.45 and k > 1:
            j = R.randrange(k - 1)
            alt = [g for g in acts if W.applicable(g, states[j]) and [g["call"][0], list(g["call"][1])] != plan[j]]
            if not alt:
                return None
            g = self._tool_first(R, alt, len(plan[j][1]))
            if g is None:
                return None
            p2[j] = [g["call"][0], list(g["call"][1])]
            self._last_op = "replace_earlier"
            return p2, goal
        bad = [g for g in acts if not W.applicable(g, states[k - 1])]
        if not bad:
            return None
        g = self._tool_first(R, bad, len(plan[k - 1][1]))
        if g is None:
            return None
        self._last_op = "replace_inapplicable"
        p2[k - 1] = [g["call"][0], list(g["call"][1])]
        return p2, goal

    def _sample_verdict(self, seed: int, sampler: str, reseed: str = "") -> Spec:
        qform = TX.HEAD_VERDICT
        key = row_key(seed, sampler, qform)
        held = sampler in HELD_OUT_SAMPLERS
        lo, hi = LEN_RANGE[sampler]
        n = lo + min(hi - lo, int(uhash(key, "n") * (hi - lo + 1)))
        ngoal = 1 + _pick(uhash(key, "ngoal"), GOAL_W)
        kshow = 1 + min(n - 1, int(uhash(key, "kshow") * n))
        target = self._target(seed, sampler, n, kshow)
        dom, idx, alg = self._world(key, held)
        for attempt in range(ATTEMPTS):
            R = random.Random(f"{key}|{reseed}|{attempt}" if reseed else f"{key}|{attempt}")
            objs = W.make_objects(R, alg, dom, counts=self._counts(key, alg))
            s0 = W.make_start(R, alg, objs, 2 + int(uhash(key, "nstart") * 4))
            acts = W.ground_actions(alg, objs)
            walk = W.random_walk(R, acts, s0, n)
            if walk is None:
                _diag("v:walk")
                continue
            calls, states = walk
            goal = W.make_goal(R, s0, states[n], ngoal)
            if goal is None:
                _diag("v:goal")
                continue
            plan = [[nm, list(a)] for nm, a in calls]
            built = self._label_plan(R, target, kshow, plan, goal, alg, objs, dom, s0, acts, states, states[n])
            if built is None:
                _diag("v:build")
                continue
            plan2, goal2 = built
            start = [[p, list(a)] for p, a in sorted(s0)]
            if W.verdict(alg, objs, start, plan2, goal2) != target:
                _diag(f"v:miss:{target.split('_')[0]}")
                continue
            st = {"qform": qform, "domain": dom, "alg_idx": idx, "alg": alg, "objects": objs, "start": start,
                  "goal": goal2, "plan": plan2, "n": n, "kshow": kshow, "attempt": attempt, "op": self._last_op}
            return self._spec(seed, sampler, qform, dom, idx, st, n)
        raise ContractError(f"no verdict structure for {target} after {ATTEMPTS} attempts ({key})")

    @staticmethod
    def _perm_names(R, alg: dict) -> dict:
        """Head 2: the tool names of the algebra are shuffled among its tools (per row), so a tool name carries no role
        (entry tools such as build_image would otherwise be the gold far more often than a late tool such as push)."""
        names = [t["name"] for t in alg["tools"]]
        new = list(names)
        R.shuffle(new)
        return {**alg, "tools": [{**t, "name": nn} for t, nn in zip(alg["tools"], new)]}

    # ---- next-call head
    def _sample_next(self, seed: int, sampler: str, reseed: str = "") -> Spec:
        qform = TX.HEAD_NEXT
        key = row_key(seed, sampler, qform)
        held = sampler in HELD_OUT_SAMPLERS
        plan = plan_choice(key, ks=(4,), abstain=False)
        lo, hi = LEN_RANGE[sampler]
        T = lo + min(hi - lo, int(uhash(key, "n") * (hi - lo + 1)))
        dmin, dmax = max(1, T - 5), min(5, T)
        d_t = dmin + min(dmax - dmin, int(uhash(key, "d") * (dmax - dmin + 1)))
        m_t = T - d_t
        ngoal = 1 + _pick(uhash(key, "ngoal"), GOAL_W)
        cls = [CLASSES[_pick(uhash(key, "cls", j), CLASS_W)] for j in range(3)]
        dom, idx, alg0 = self._world(key, held)
        for attempt in range(ATTEMPTS):
            R = random.Random(f"{key}|{reseed}|{attempt}" if reseed else f"{key}|{attempt}")
            alg = self._perm_names(R, alg0)
            objs = W.make_objects(R, alg, dom, counts=self._counts(key, alg))
            s0 = W.make_start(R, alg, objs, 2 + int(uhash(key, "nstart") * 4))
            acts = W.ground_actions(alg, objs)
            walk = W.random_walk(R, acts, s0, m_t) if m_t else ([], [s0])
            if walk is None:
                _diag("n:walk")
                continue
            calls, states = walk
            sm = states[m_t]
            try:
                depth = W.bfs_depths(acts, sm, d_t)
            except W.Cap:
                _diag("n:cap")
                continue
            tgt = sorted(s for s, dd in depth.items() if dd == d_t)
            if not tgt:
                _diag("n:depth")
                continue
            shallow = [s for s, dd in depth.items() if dd < d_t]
            goal = None
            for t_state in R.sample(tgt, min(len(tgt), 6)):
                pool_l = [(False, f) for f in sorted(t_state - sm)] + [(True, f) for f in sorted(sm - t_state)]
                masks = set()
                for s_ in shallow:
                    mk = 0
                    for i, (ng, f) in enumerate(pool_l):
                        if (f in s_) != ng:
                            mk |= 1 << i
                    masks.add(mk)
                for size in [x for x in (ngoal, ngoal - 1, ngoal - 2, 1, 2, 3) if 1 <= x <= min(3, len(pool_l))]:
                    combos = [c for c in itertools.combinations(range(len(pool_l)), size)
                              if not any((mk & sum(1 << i for i in c)) == sum(1 << i for i in c) for mk in masks)]
                    if combos:
                        c = R.choice(combos)
                        goal = sorted([[pool_l[i][0], pool_l[i][1][0], list(pool_l[i][1][1])] for i in c],
                                      key=lambda x: (x[1], x[2], x[0]))
                        break
                if goal is not None:
                    break
            if goal is None:
                _diag("n:goal")
                continue
            ex = W.explore(acts, sm, goal, max_depth=d_t)
            if ex["d"] != d_t:
                _diag("n:dist")
                continue
            seen_t = {W.call_text(*c) for c in calls[:m_t]}          # an option never repeats a call printed above
            opt = [c for c in sorted(ex["firsts"]) if W.call_text(*c) not in seen_t]
            pools = {"inapp": [g["call"] for g in acts if not W.applicable(g, sm) and W.call_text(*g["call"]) not in seen_t],
                     "stuck": [g["call"] for g in acts if W.applicable(g, sm) and g["call"] not in ex["firsts"]
                               and W.call_text(*g["call"]) not in seen_t]}
            if not opt or any(len(pools[c]) < cls.count(c) for c in CLASSES):
                _diag("n:pool")
                continue
            chosen = None
            tsig = {t["name"]: tuple(ty for _, ty in t["params"]) for t in alg["tools"]}
            for _ in range(400):
                gold = R.choice(opt)
                ds, used = [], {gold}
                for c in cls:
                    cand = [x for x in pools[c] if x not in used and tsig[x[0]] == tsig[gold[0]]]   # one parameter-type signature per row
                    if not cand:
                        break
                    x = R.choice(cand)
                    used.add(x)
                    ds.append((x, c))
                if len(ds) < 3:
                    continue
                texts = [W.call_text(*gold)] + [W.call_text(*x) for x, _ in ds]
                order = sorted(texts, key=lambda t: (len(t), t))      # the kit's visible-length order (ties by text)
                if order.index(texts[0]) == plan.rank and len({t.casefold() for t in texts}) == 4:
                    chosen = (gold, ds)
                    break
            if chosen is None:
                _diag("n:rank")
                continue
            gold, ds = chosen
            cands = sorted(W.call_text(*c) for c in [gold] + [x for x, _ in ds])
            prefix = [[nm, list(a)] for nm, a in calls[:m_t]]
            st = {"qform": qform, "domain": dom, "alg_idx": idx, "alg": alg, "objects": objs,
                  "start": [[p, list(a)] for p, a in sorted(s0)], "goal": goal, "prefix": prefix, "n": T, "d": d_t,
                  "m": m_t, "cands": cands, "attempt": attempt,
                  "distractors": [{"call": W.call_text(*x), "cls": c} for x, c in ds]}
            return self._spec(seed, sampler, qform, dom, idx, st, T)
        raise ContractError(f"no next-call structure after {ATTEMPTS} attempts ({key})")

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        st = spec.structure
        if st["qform"] == TX.HEAD_VERDICT:
            return W.verdict(st["alg"], st["objects"], st["start"], st["plan"], st["goal"])
        sm = W.run_prefix(st["alg"], st["objects"], st["start"], st["prefix"])
        if sm is None:
            raise ContractError("a prefix call is not applicable")
        acts = W.ground_actions(st["alg"], st["objects"])
        ex = W.explore(acts, sm, st["goal"], max_depth=10)
        if not ex["d"]:
            raise ContractError("goal already holds or is unreachable")
        opt = {W.call_text(*c) for c in ex["firsts"]}
        hit = [c for c in st["cands"] if c in opt]
        if len(hit) != 1:
            raise ContractError(f"{len(hit)} optimal calls among the options")
        return hit[0]

    def canonical(self, spec: Spec) -> dict:
        st = spec.structure
        out = {"qform": st["qform"],
               "tools": [[t["name"], t["params"], t["needs"], t["adds"], t["dels"]] for t in st["alg"]["tools"]],
               "objects": st["objects"], "start": st["start"], "goal": st["goal"]}
        out["plan" if st["qform"] == TX.HEAD_VERDICT else "prefix"] = st["plan" if st["qform"] == TX.HEAD_VERDICT else "prefix"]
        return out

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
        tb = TextBuilder()
        tb.add("state", state_text(st, skin.register), skin_id=skin.skin_id)
        tb.add("instructions", TX.RULES[spec.qform]).add("instructions", "\n\n")
        tb.add("instructions", wording.fill(spec.all_slots(), forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        if spec.qform == TX.HEAD_VERDICT:
            plan = plan_choice(key, closed=4)
            labels = [TX.V_INVALID, TX.V_STEP.format(k=st["kshow"]), TX.V_GOAL, TX.V_VALID]
            os_ = build_closed(spec, ans, labels, self.error_models(), row_key=key, render_key=str, plan=plan)
        else:
            if st.get("meta_check"):
                os_ = build_options(spec, ans, self.error_models(), k=len(st["distractors"]) + 1, row_key=key + "|g4",
                                    render_key=str)
            else:
                plan = plan_choice(key, ks=(4,), abstain=False)
                os_ = build_options(spec, ans, self.error_models(), row_key=key, render_key=str, plan=plan,
                                    length_balance=True)
            if os_ is None:
                raise RenderError("the planned option set cannot be built from the stored distractors")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack)

    # ------------------------------------------------------------------------------------------- relations (G4)
    @staticmethod
    def _call_mapper(om, tm):
        import re

        def cm(s):
            nm, args = re.fullmatch(r"(\w+)\((.*)\)", s).groups()
            return W.call_text(tm.get(nm, nm), [om.get(x.strip(), x.strip()) for x in args.split(",")] if args.strip() else [])
        return cm

    @classmethod
    def _rename(cls, st: dict, om=None, tm=None, pm=None) -> dict:
        om, tm, pm = om or {}, tm or {}, pm or {}
        o = lambda x: om.get(x, x)  # noqa: E731
        t = lambda x: tm.get(x, x)  # noqa: E731
        p = lambda x: pm.get(x, x)  # noqa: E731
        alg = {**st["alg"], "tools": [
            {"name": t(x["name"]), "params": x["params"],
             "needs": [[n, p(q), a] for n, q, a in x["needs"]], "adds": [[p(q), a] for q, a in x["adds"]],
             "dels": [[p(q), a] for q, a in x["dels"]]} for x in st["alg"]["tools"]]}
        out = {**st, "alg": alg, "meta_check": True,
               "objects": {ty: sorted(o(x) for x in v) for ty, v in st["objects"].items()},
               "start": sorted([[p(q), [o(x) for x in a]] for q, a in st["start"]]),
               "goal": sorted([[n, p(q), [o(x) for x in a]] for n, q, a in st["goal"]], key=lambda x: (x[1], x[2], x[0]))}
        for k in ("plan", "prefix"):
            if k in st:
                out[k] = [[t(nm), [o(x) for x in a]] for nm, a in st[k]]
        if "cands" in st:
            cm = cls._call_mapper(om, tm)
            out["cands"] = sorted(cm(c) for c in st["cands"])
            out["distractors"] = [{"call": cm(d["call"]), "cls": d["cls"]} for d in st["distractors"]]
        return out

    def relations(self, spec: Spec) -> list:
        st = spec.structure
        R = random.Random(f"{FAMILY}|g4|{spec.seed}|{spec.sampler}")
        out = []
        ans = self.solve_a(spec)

        def add(s2, note, om=None, tm=None):
            exp = "same" if st["qform"] == TX.HEAD_VERDICT else self._call_mapper(om or {}, tm or {})(ans)
            out.append(RelationProposal("metamorphic", spec=spec.replace(structure=s2), expect=exp, note=note))

        # (1) rename the objects (fresh names of the same domain pools, same type)
        ty = W.domain_types(st["domain"])
        om = {}
        for tname, objs in st["objects"].items():
            sh = [x for x in ty[tname] if x not in objs]
            R.shuffle(sh)
            om.update(dict(zip(objs, sh)))
        if om:
            add(self._rename(st, om=om), "rename the objects", om=om)
        # (2) rename the tools and the predicates (suffixes cannot collide with any pool name)
        tm = {t["name"]: t["name"] + "_x" for t in st["alg"]["tools"]}
        preds = sorted({q for t in st["alg"]["tools"] for _, q, _ in t["needs"]} |
                       {q for t in st["alg"]["tools"] for q, _ in t["adds"] + t["dels"]})
        add(self._rename(st, tm=tm, pm={q: q + "_p" for q in preds}), "rename the tools and predicates", tm=tm)
        # (3) reverse the tool block
        add({**st, "alg": {**st["alg"], "tools": list(reversed(st["alg"]["tools"]))}, "meta_check": True}, "reverse the tool block")
        # (4) add a tool that can never run (needs a fact nothing adds and the start lacks)
        p0 = st["alg"]["tools"][0]["params"]
        if p0:
            ghost = {"name": "zz_hold", "params": [list(p0[0])], "needs": [[False, "zz_ready", [p0[0][0]]]],
                     "adds": [["zz_done", [p0[0][0]]]], "dels": []}
            add({**st, "alg": {**st["alg"], "tools": st["alg"]["tools"] + [ghost]}, "meta_check": True},
                "add a tool that can never run")
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        out = {}

        def alt(spec, needs=True, dels=True, bad=True):
            st = spec.structure
            if st["qform"] != TX.HEAD_VERDICT:
                return None
            alg, objs = st["alg"], st["objects"]
            tools = {t["name"]: t for t in alg["tools"]}
            gm = {g["call"]: g for g in W.ground_actions(alg, objs)}
            state = frozenset((p, tuple(a)) for p, a in st["start"])
            for nm, args in st["plan"]:
                t = tools.get(nm)
                ok = t is not None and len(args) == len(t["params"]) and all(a in objs.get(ty, ()) for a, (_, ty) in zip(args, t["params"]))
                if not ok:
                    if bad:
                        return None
                    continue
                g = gm[(nm, tuple(args))]
                if needs and not W.applicable(g, state):
                    return None
                state = ((state - g["dels"]) if dels else state) | g["adds"]
            return TX.V_VALID if W.goal_holds(st["goal"], state) else TX.V_GOAL

        def skips_needs(spec):
            if self.solve_a(spec).startswith("STEP_"):
                return alt(spec, needs=False, dels=True, bad=True)
        def ignores_deletes(spec):
            if self.solve_a(spec) in (TX.V_VALID, TX.V_GOAL):
                r = alt(spec, needs=True, dels=False, bad=True)
                return r if r and r != self.solve_a(spec) else None
        def skips_malformed(spec):
            if self.solve_a(spec) == TX.V_INVALID:
                return alt(spec, needs=True, dels=True, bad=False)
        def goal_unchecked(spec):
            if self.solve_a(spec) == TX.V_GOAL:
                return TX.V_VALID
        out["t44_skips_needs"] = error_model("t44_skips_needs", skips_needs)
        out["t44_ignores_deletes"] = error_model("t44_ignores_deletes", ignores_deletes)
        out["t44_skips_malformed"] = error_model("t44_skips_malformed", skips_malformed)
        out["t44_goal_unchecked"] = error_model("t44_goal_unchecked", goal_unchecked)

        def nth(c, j):
            def fn(spec):
                if spec.structure["qform"] != TX.HEAD_NEXT:
                    return None
                hits = [d["call"] for d in spec.structure["distractors"] if d["cls"] == c]
                return hits[j] if len(hits) > j else None
            return fn
        for c in CLASSES:
            for j in range(3):
                name = f"t44_{c}" if j == 0 else f"t44_{c}@{j + 1}"
                out[name] = error_model(name, nth(c, j))
        return out

