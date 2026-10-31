"""families/T45/plugin.py: T45 TRACE-VERIFY (real-tool step verification), a C2 family plugin (A42-D, A47).

Semantics: G0_SPEC.md. Two choice heads over ONE executed step of an agent run (git push to a local bare remote, an sqlite
loader, a localhost HTTP batch endpoint, make, unittest):
  ch_outcome  SUCCESS / NEUTRAL / SILENT_PARTIAL / SILENT_WRONG / LOUD_RETRYABLE / LOUD_PERMANENT
  ch_move     ADVANCE / RETRY / REPAIR_ARGS / ESCALATE
Each row shows k = 2 or 3 of the labels (the anchor SUCCESS / ADVANCE is always one of them; the gold is uniform inside the
shown set, so the options alone say nothing about the gold; shown sets are confusable-aware).

  solver A   hermetic execution of the real step (executor.py + exec_child.py: venv CPython 3.12, PYTHONHASHSEED=0, fresh
             subprocess, 5 s cap, temp dir, localhost only; two independent runs must agree) + the executed retry and
             repair; label = the diff between the post-state and the intended effect.        paradigm simulator
  solver B   solver_b.py: own parser of the rendered row (layouts, legend, item lists) + set algebra over (key, value)
             pairs and the legend's tag groups.                                              paradigm set_algebra
  samplers   S1 outcome head only; S2 mostly move head; S3 / S4 mixed; S5 held out (fault type `stale_noop`, registers
             memo and journal; all rows dev only)
  relations  G4 metamorphic only (rename surfaces, change legend, re-pad, re-order options): choice rows, no input slots.
"""
from __future__ import annotations

import hashlib
import random
from pathlib import Path

from c2_kit import plugin as KP
from c2_kit.choiceplan import plan_choice
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row
from c2_kit.skin import RenderError, make_skin

from . import executor as E
from . import scenarios as SC
from . import texts as TX

HERE = Path(__file__).resolve().parent
FAMILY = "T45"
KP.FAMILIES.setdefault(FAMILY, "agent")           # kit candidate: add T40-T45 to plugin.FAMILIES (runtime registration)

SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
HELD_OUT_SAMPLERS = ("S5",)
REGISTERS = TX.REGISTERS
HELD_OUT_REGISTERS = TX.HELD_OUT_REGISTERS
HEAD1_P = {"S1": 1.0, "S2": 0.30, "S3": 0.70, "S4": 0.60, "S5": 0.65}     # P(outcome head); training mean 0.65
P_K2 = 0.30                                            # P(2 shown options); else 3
P_ADVANCE_OK = 0.85                                    # ch_move gold ADVANCE: the step is `ok` w.p. .85, else `already_done`
P_CONFUSABLE = 0.60                                    # ch_outcome k = 3: the two distractors are a confusable pair w.p. .6
CONFUSABLE = (("LOUD_RETRYABLE", "LOUD_PERMANENT"), ("SILENT_PARTIAL", "SILENT_WRONG"))
ATTEMPTS = 12
DIAG = {"exec_error": 0, "label_miss": 0, "inconsistent": 0, "attempts": 0}
G0_SPEC = HERE / "G0_SPEC.md"

register_name("trust_exit_code", "reads exit 0 as success without comparing the states")
register_name("ignore_before", "does not compare the state before the step with the intended effect")
register_name("partial_vs_wrong", "mixes up a partly applied effect with an effect that is missing or has another value")
register_name("loud_class_swap", "reads the runner tag of a failed step as the other kind of failure")
register_name("advance_on_exit_zero", "advances because the exit status is 0")
register_name("retry_everything", "repeats the step whatever the runner tag says")
register_name("escalate_everything", "hands every problem to a person")
register_name("repair_blocked", "tries other arguments when the step is blocked")


def row_key(seed: int, sampler: str, qform: str) -> str:
    return f"{FAMILY}|{seed}|{sampler}|{qform}"


def items_text(d: dict) -> str:
    return ", ".join(f"{k}={v}" for k, v in sorted(d.items()))


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
        sk = make_skin(f"T45-SK-{r}", FAMILY, f"{r} layout", {}, kind="skin", register=r, held_out=r in HELD_OUT_REGISTERS)
        skins[sk.skin_id] = sk
    for qf in TX.QFORMS:                       # the rules and legend block: a role "program" template (placeholder lint only)
        sk = make_skin(f"T45-RULES-{qf}", FAMILY, TX.rules_text(qf, 0), {}, kind="program", register="rules")
        skins[sk.skin_id] = sk
    for qf, ws in TX.WORDINGS.items():
        for i, w in enumerate(ws):
            sk = make_skin(f"T45-W-{qf}-{i}", FAMILY, w, {}, kind="wording", register="question", qform=qf,
                           lexicon_ids=(form_of[(qf, w)],))
            skins[sk.skin_id] = sk
    return KitCtx(skins=skins, lexicon=reg)


def make_plugin() -> tuple:
    ctx = make_ctx()
    return T45Plugin(lexicon=ctx.lexicon), ctx


def shown_set(key: str, qform: str) -> tuple:
    """(shown labels, gold): label-blind. The anchor is always shown; the gold is uniform inside the shown set."""
    universe = TX.LABELS if qform == "ch_outcome" else TX.MOVES
    anchor, others = universe[0], list(universe[1:])
    k = 2 if uhash(key, "k") < P_K2 else 3
    if k == 2:
        d = [others[min(len(others) - 1, int(uhash(key, "d1") * len(others)))]]
    elif qform == "ch_outcome" and uhash(key, "conf") < P_CONFUSABLE:
        d = list(CONFUSABLE[min(1, int(uhash(key, "confpair") * 2))])
    else:
        pairs = [(a, b) for i, a in enumerate(others) for b in others[i + 1:]]
        d = list(pairs[min(len(pairs) - 1, int(uhash(key, "pair") * len(pairs)))])
    shown = [anchor] + d
    gold = shown[min(len(shown) - 1, int(uhash(key, "gold") * len(shown)))]
    return tuple(shown), gold


def fault_candidates(kind: str, qform: str, gold: str, held: bool) -> list:
    """[(fault, variant or None)] that can reach `gold` for this kind. Training samplers never list the held-out fault."""
    pool = SC.KIND_FAULTS[kind] if held else SC.TRAIN_FAULTS[kind]
    out = []
    for f in pool:
        if qform == "ch_outcome":
            if SC.FAULT_LABEL[f] == gold:
                out.append((f, None))
        elif f == "error_body":
            if gold == "REPAIR_ARGS":
                out.append((f, 0))
            elif gold == "ESCALATE":
                out.append((f, 1))
        elif SC.target_move(f, 0) == gold:
            out.append((f, None))
    if held and qform == "ch_outcome" and gold == "SILENT_WRONG" and SC.HELD_OUT_FAULT in pool:
        out = [(SC.HELD_OUT_FAULT, None)]
    return out


class T45Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = G0_SPEC
    G0_SHA256 = "fe1694bb1be6d94ebb6b3e21b9ac099756b6b3239c5c1946b31bd4b0c97acda8"   # frozen G0_SPEC.md (see BUILD_NOTES.md)
    SAMPLERS = SAMPLERS
    HELD_OUT_SAMPLERS = HELD_OUT_SAMPLERS
    PARADIGM_A = "simulator"
    PARADIGM_B = "set_algebra"
    SOLVER_B_MODULE = "families.T45.solver_b"
    QFORMS = {"ch_outcome": QuestionForm("ch_outcome", "choice", answer_set="closed"),
              "ch_move": QuestionForm("ch_move", "choice", answer_set="closed")}
    LABEL_WORDS = ("success", "neutral", "silent", "loud", "retryable", "permanent", "advance", "retry", "repair",
                   "escalate", "partial", "wrong")
    CLOSED_WORLD_SENTENCE = ("The intended effect, the two states and the tag legend are the only evidence: no other write, "
                             "retry or log applies.")
    REGISTERS = REGISTERS
    HELD_OUT_REGISTERS = HELD_OUT_REGISTERS
    YES_NO_ONLY = False

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in SAMPLERS:
            raise ContractError(f"sampler {sampler!r}")
        held = sampler in HELD_OUT_SAMPLERS
        key0 = f"{FAMILY}|{seed}|{sampler}"
        qform = "ch_outcome" if uhash(key0, "head") < HEAD1_P[sampler] else "ch_move"
        key = row_key(seed, sampler, qform)
        shown, gold = shown_set(key, qform)
        kind = SC.KINDS[min(len(SC.KINDS) - 1, int(uhash(key, "kind") * len(SC.KINDS)))]
        pack = SC.PACK_NAMES[min(len(SC.PACK_NAMES) - 1, int(uhash(key, "pack") * len(SC.PACK_NAMES)))]
        legend = min(TX.N_LEGENDS - 1, int(uhash(key, "legend") * TX.N_LEGENDS))
        cands = fault_candidates(kind, qform, gold, held)
        if not cands:
            raise ContractError(f"no fault reaches {gold} for kind {kind}")
        if qform == "ch_move" and gold == "ADVANCE":
            cands = [("ok", None)] if uhash(key, "adv") < P_ADVANCE_OK else [("already_done", None)]
        for attempt in range(ATTEMPTS):
            DIAG["attempts"] += 1
            fault, var = cands[min(len(cands) - 1, int(uhash(key, "fault", attempt) * len(cands)))]
            R = random.Random(f"{key}|exec|{attempt}")
            params = SC.exec_params(R, kind, fault)
            if var is not None:
                params["variant"] = var
            try:
                res = E.run_exec(kind, params)
                c = E.classify(res)
            except E.Inconsistent:
                DIAG["inconsistent"] += 1
                continue
            except E.ExecTimeout:
                DIAG["timeout_drops"] = DIAG.get("timeout_drops", 0) + 1       # redrawn with other parameters of the same fault
                continue
            except E.ExecError:
                DIAG["exec_error"] += 1
                continue
            got = c["label"] if qform == "ch_outcome" else c["move"]
            if got != gold or c["label"] != SC.FAULT_LABEL[fault] or c["move"] != SC.target_move(fault, params["variant"]):
                DIAG["label_miss"] += 1
                continue
            st = {"seed": seed, "qform": qform, "kind": kind, "fault": fault, "params": params, "shown": list(shown), "gold": gold,
                  "pack": pack, "legend": legend, "surf": 0, "pad": 0, "opt": 0, "attempt": attempt,
                  "exec_key": E.exec_key(kind, params)}
            return Spec(FAMILY, sampler, seed, f"{FAMILY}:{kind}:L{legend}:{pack}", qform, {}, structure=st, depth=2,
                        deep=False, tags=(f"kind:{kind}",), pack=f"{kind}:{pack}")
        raise ContractError(f"no executed structure reached {gold} ({key}): {DIAG}")

    # ------------------------------------------------------------------------------------------- solver A
    def _classified(self, spec: Spec) -> dict:
        st = spec.structure
        try:
            return E.classify(E.run_exec(st["kind"], st["params"]))
        except E.ExecError as e:
            raise ContractError(f"execution gold unavailable: {e}") from e

    def solve_a(self, spec: Spec):
        c = self._classified(spec)
        return c["label"] if spec.qform == "ch_outcome" else c["move"]

    # ------------------------------------------------------------------------------------------- the surface view
    def view(self, spec: Spec) -> dict:
        """Everything the text shows, as plain data: the generator's facts (G3 target) and the input of render().
        Each state line shows: the keys that were there before (real), ONE disguised item per intent key that is not set in that
        state, and 2 padding items. Disguised and padding items are built ONLY from the row's 6 rare pseudo-words V (keys
        `a-b`; values repeat values already in the row), and the 4 padding items cover all of V in every row. So the number of
        distinct rare tokens of a row is intent tokens + 6 whatever the step did (found by ablation: the number of distinct rare
        tokens leaked the label through the L2 scale of the G6 cross features), while item counts, lengths and digit counts
        stay label-blind. New non-intent keys written by the step are not shown (other keys never matter)."""
        st = spec.structure
        kind, p = st["kind"], st["params"]
        res = E.run_exec(kind, p)
        key = row_key(spec.seed, spec.sampler, spec.qform)
        R = random.Random(f"{key}|surf|{st['surf']}")
        sm = SC.surface(R, kind, st["pack"], p)
        mp = SC.Mapper(R, sm, kind)
        intent, before = mp.state(res["intent"]), mp.state(res["before"])
        after = {k: v for k, v in mp.state(res["main"]["after"]).items() if k in intent or k in before}
        RP = random.Random(f"{key}|pad|{st['pad']}")
        V = []
        while len(V) < 6:
            w = SC.pseudo(RP, RP.randrange(4, 8))
            if w not in V:
                V.append(w)
        vals = sorted(set(intent.values()) | set(before.values()))
        used = set(intent) | set(before) | set(after)

        def mk(kind_of, a, b):
            if kind == "git":
                return f"tags/release-{a}-{b}" if kind_of == "tags" else f"heads/{a}-{b}"
            if kind == "db":
                return f"{sm['names']['QTBL']}.{a}-{b}"
            if kind == "http":
                return f"{sm['names']['QRES']}.{a}-{b}"
            if kind == "build":
                return f"build/{a}-{b}.bin" if RP.random() < 0.5 else f"build/{a}.bin"
            return f"{sm['names']['QD0']}/test_{a}.test_{b}"

        def item(kind_of, ab=None):
            for _ in range(200):
                a, b = ab if ab else RP.sample(V, 2)
                k = mk(kind_of, a, b)
                if k not in used:
                    used.add(k)
                    return k, ("pass" if kind == "tests" else RP.choice(vals))
                ab = None
            raise ContractError("no disguised item found")

        def disguise(state):
            out = dict(state)
            for k in intent:
                if k not in out:
                    pk, pv = item("tags" if k.startswith("tags/") else "heads")
                    out[pk] = pv
            return out
        before, after = disguise(before), disguise(after)
        pb = [item("heads", (V[0], V[1])), item("heads", (V[2], V[3]))]        # padding covers every pseudo-word in every row
        pa = [item("heads", (V[4], V[5])), item("heads", (V[0], V[2]))]
        before = {**before, **dict(pb)}
        after = {**after, **dict(pb), **dict(pa)}
        legend = TX.legend_of(st["legend"])
        cls = res["main"]["cls"]
        return {"qform": spec.qform, "legend": {legend["codes"][g]: g for g in "TAH0"}, "intent": intent,
                "before": before, "after": after, "command": mp.text(TX.PLANNED[kind]),
                "exit": legend["ok_exit"] if int(res["main"]["exit"]) == 0 else legend["fail_exit"], "ok_exit": legend["ok_exit"],
                "tag": legend["codes"][cls]}

    def canonical(self, spec: Spec) -> dict:
        return self.view(spec)

    # ------------------------------------------------------------------------------------------- render
    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        st = spec.structure
        held = spec.sampler in HELD_OUT_SAMPLERS
        key = row_key(spec.seed, spec.sampler, spec.qform)
        okey = key + (f"|opt{st['opt']}" if st["opt"] else "")
        skin = skin or ctx.pick(FAMILY, "skin", okey, held_out=held)
        wording = wording or ctx.pick(FAMILY, "wording", okey, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, okey)
        v = self.view(spec)
        lay = TX.LAYOUTS[skin.register]
        lines = [lay[0] + items_text(v["intent"]), lay[1] + items_text(v["before"]), lay[2] + v["command"],
                 lay[3].format(n=v["exit"], t=v["tag"]), lay[4] + items_text(v["after"])]
        tb = TextBuilder()
        tb.add("state", "\n".join(lines), skin_id=skin.skin_id)
        tb.add("instructions", TX.rules_text(spec.qform, st["legend"]), skin_id=f"T45-RULES-{spec.qform}").add("instructions", "\n\n")
        tb.add("instructions", wording.fill(spec.all_slots(), forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        shown = list(st["shown"])
        if ans not in shown:
            raise ContractError(f"gold {ans} is not in the shown set {shown}")
        plan = plan_choice(okey, closed=len(shown))
        os_ = build_closed(spec, ans, shown, self.error_models(), row_key=okey, render_key=lambda a: TX.DISPLAY[a], plan=plan)
        tb.add("card", "\n".join(f"- {o.text}: {TX.DEFS[o.key]}" for o in os_.options))
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack)

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        st = spec.structure

        def meta(**kw):
            return spec.replace(structure={**st, **kw, "meta_check": True})
        pack2 = SC.PACK_NAMES[(SC.PACK_NAMES.index(st["pack"]) + 1) % len(SC.PACK_NAMES)]
        return [
            RelationProposal("metamorphic", spec=meta(surf=st["surf"] + 1, pack=pack2), expect="same",
                             note="rename every name, id, value and sha (another pack)"),
            RelationProposal("metamorphic", spec=meta(legend=(st["legend"] + 1) % TX.N_LEGENDS), expect="same",
                             note="another runner legend (codes, wording, order)"),
            RelationProposal("metamorphic", spec=meta(pad=st["pad"] + 1), expect="same", note="other padding items"),
            RelationProposal("metamorphic", spec=meta(opt=st["opt"] + 1), expect="same",
                             note="another option order and layout draw"),
        ]

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def table(m):
            def fn(spec):
                g = self.solve_a(spec)
                return m.get(g)
            return fn
        out = {}
        for name, mapping in (
                ("trust_exit_code", {"SILENT_PARTIAL": "SUCCESS", "SILENT_WRONG": "SUCCESS"}),
                ("ignore_before", {"SUCCESS": "NEUTRAL", "NEUTRAL": "SUCCESS"}),
                ("partial_vs_wrong", {"SILENT_PARTIAL": "SILENT_WRONG", "SILENT_WRONG": "SILENT_PARTIAL"}),
                ("loud_class_swap", {"LOUD_RETRYABLE": "LOUD_PERMANENT", "LOUD_PERMANENT": "LOUD_RETRYABLE"}),
                ("advance_on_exit_zero", {"RETRY": "ADVANCE", "REPAIR_ARGS": "ADVANCE", "ESCALATE": "ADVANCE"}),
                ("retry_everything", {"REPAIR_ARGS": "RETRY", "ESCALATE": "RETRY"}),
                ("escalate_everything", {"REPAIR_ARGS": "ESCALATE", "RETRY": "ESCALATE"}),
                ("repair_blocked", {"ESCALATE": "REPAIR_ARGS"})):
            out[name] = error_model(name, table(mapping))
        return out


def warm_cache(workers: int = 4, draws: int = 300, held: bool = True, kinds=None) -> int:
    """Execute (in parallel, each spec still two fresh processes) every canonical structure the samplers can reach, so
    sampling afterwards is a cache hit. Returns the number of distinct executions."""
    jobs, seen = [], set()
    for kind in (kinds or SC.KINDS):
        for fault in (SC.KIND_FAULTS[kind] if held else SC.TRAIN_FAULTS[kind]):
            for i in range(draws):
                for var in ((0, 1) if (kind == "http" and fault == "error_body") else (None,)):
                    p = SC.exec_params(random.Random(f"warm|{kind}|{fault}|{i}"), kind, fault)
                    if var is not None:
                        p["variant"] = var
                    k = E.exec_key(kind, p)
                    if k not in seen:
                        seen.add(k)
                        jobs.append((kind, p))
    E.prefetch(jobs, workers=workers)
    return len(jobs)
