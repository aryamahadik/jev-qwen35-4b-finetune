"""families/T46/plugin.py: T46 DISPOSITION-GATE, a C2 family plugin (Ruling A59; semantics in G0_SPEC.md).

A request record (JSON / YAML / key-value / ticket / TOML / XML) is judged under a disposition vocabulary. Four
semantic classes (permit P, hold H, deny D, human E) are shown under >= 8 label sets in snake_case or spelled-out
form or as codes; the row is a yes/no question about ONE proposed action (45-55% yes) or a choice among 3 shown
labels. Gold is program gold: solver A is an ordered first-match rule engine over a policy card (plain card: the
intrinsic meaning of the state flags; stated card: printed priority lines); solver B (solver_b.py) is a decision-table
evaluator over the RENDERED text.

  samplers   S1 mixed; S2 boundary-heavy; S3 conflict-heavy (printed priority); S4 alarming-but-permitted-heavy;
             S5 held out (dev only: dev names, dev limits, the dev workflow skin `purchase`, layouts toml / xml, dev
             wordings, dev glosses, dev Arabic items)
  questions  yn_is, yn_not (syntactic complement), yn_ruledout (antonym complement), yn_dneg (two negations);
             ch_disp (closed set: 3 of the 4 labels shown, gold uniform in the shown set)
  relations  complement (yes/no), minimal-edit twin (one flag or one number), equiv (another layout), G4 metamorphic
             (rename, new id, scale the numbers, reorder the fields, swap the vocabulary, re-phrase one flag)
"""
from __future__ import annotations

import random
from pathlib import Path

from c2_kit import cards as CD
from c2_kit import polarity as POL
from c2_kit import slots as S
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import (C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms)
from c2_kit.rows import TextBuilder, assemble_row
from c2_kit.skin import Filled, make_skin

from . import policy as PO
from . import tables as T
from . import vocab as TX

HERE = Path(__file__).resolve().parent
FAMILY = T.FAMILY
G0_SPEC = HERE / "G0_SPEC.md"
SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
HELD_OUT_SAMPLERS = ("S5",)

# ------------------------------------------------------------------------------------------------ targets (G0 section 4)
P_YN = 0.44                                         # yes/no share of the base rows (G10 45-55% of all rows)
QF_YN = (("yn_is", 0.38), ("yn_not", 0.24), ("yn_ruledout", 0.26), ("yn_dneg", 0.12))
CLASS_SHARE = {"P": 0.30, "H": 0.25, "D": 0.25, "E": 0.20}
OMIT_W = (("P", 0.10), ("H", 0.25), ("D", 0.25), ("E", 0.40))     # the omitted class of a choice row: shares 30/25/25/20
P_STATED = 0.55
P_DEFS, P_CODED = 0.60, 0.25
BOUNDARY = {"S1": 0.15, "S2": 0.35, "S3": 0.15, "S4": 0.15, "S5": 0.20}          # P(boundary | gold) (P and not-P)
ALARM_P = {"S1": 0.45, "S2": 0.40, "S3": 0.45, "S4": 0.70, "S5": 0.50}          # P(alarming-but-permitted | gold P)
CONFLICT_N = {"S1": 0.85, "S2": 0.70, "S3": 1.00, "S4": 0.85, "S5": 0.85}        # P(conflict | gold not P, stated arm)
P_DECOY = 0.12                                      # an uncovered flag active on a not-P row
P_AR = {"S1": 0.10, "S2": 0.10, "S3": 0.10, "S4": 0.10, "S5": 0.16}              # Arabic share among eligible workflows
P_NOTE_DECIDES = 0.65                               # plain Arabic not-P row whose deciding fact is the Arabic note
AR_WORKFLOWS = ("support", "access", "hr", "purchase")
P_DEV_WF = 0.46                                     # S5 rows on the dev-only workflow skin
P_TWIN_P, P_TWIN_N, P_COMPLEMENT, P_EQUIV = 0.95, 0.30, 0.48, 0.13   # twins of P rows give not-P rows and vice versa
MAX_ATTEMPTS = 40

POLARITY_NEGS = (r"\bwrong\b", r"\bmistake\b", r"\bunwise\b", r"\binappropriate\b", r"\bincorrect\b",
                 r"\bunjustified\b", r"\bimproper\b", r"\binadvisable\b")

register_name("any_problem_means_stop", "treats any active problem flag as a reason to refuse")
register_name("any_problem_means_wait", "treats any active problem flag as a reason to hold the request")
register_name("alarm_means_human", "sends every request with an alarming-looking flag to a person")
register_name("unprinted_priority", "ignores the printed line order and uses the usual priority (deny, person, hold)")
register_name("trust_flag_name", "reads a flag by its name and ignores the printed policy")


def _norm(t: str) -> str:
    return " ".join(str(t).casefold().split())


def _joint() -> list:
    """Zero-diagonal coupling J[c][a] with row sums = column sums = CLASS_SHARE (iterative proportional fitting): a
    'no' yes/no row draws (class c, asked a != c) from it, so every class and every asked label is 50% yes."""
    p = [CLASS_SHARE[c] for c in T.CLASSES]
    J = [[0.0 if i == j else p[i] * p[j] for j in range(4)] for i in range(4)]
    for _ in range(2000):
        for i in range(4):
            s = sum(J[i])
            J[i] = [x * p[i] / s for x in J[i]]
        for j in range(4):
            s = sum(J[i][j] for i in range(4))
            for i in range(4):
                J[i][j] *= p[j] / s
    return J


JOINT = _joint()


def wpick(u: float, items) -> object:
    acc = 0.0
    for v, w in items:
        acc += w
        if u < acc:
            return v
    return items[-1][0]


def upick(u: float, seq):
    seq = list(seq)
    return seq[min(len(seq) - 1, int(u * len(seq)))]


def kron(i: int, phi: float, off: float) -> float:
    """A low-discrepancy draw: windows of consecutive indices hold the target shares almost exactly."""
    return (i * phi + off) % 1.0


def pair_index(pair: int, sampler: str) -> tuple:
    """(is_yes_no, index within its kind) of seed pair `pair`: a Sturmian pattern, so every window holds P_YN."""
    off = uhash(FAMILY, "hoff", sampler)
    ny = int(pair * P_YN + off)
    nxt = int((pair + 1) * P_YN + off)
    return (nxt > ny), (ny if nxt > ny else pair - ny)


def row_key(seed: int, sampler: str) -> str:
    return f"{FAMILY}|{seed}|{sampler}"


def fslot(b: bool) -> S.Slot:
    return S.category_slot("true" if b else "false", {"true": ["true"], "false": ["false"]})


# ------------------------------------------------------------------------------------------------ the lexicon view
class Lex:
    """What the plugin may draw: the admitted forms of the registry (labels, flag values, glosses, notes)."""

    def __init__(self, reg: LexiconRegistry):
        self.reg = reg
        self.fid = {_norm(f.text): i for i, f in reg.forms.items()}

    def ok(self, text: str) -> bool:
        i = self.fid.get(_norm(text))
        return i is not None and self.reg.status(i) == "admitted"

    def form_id(self, text: str) -> str | None:
        return self.fid.get(_norm(text))

    def vocab_styles(self, vocab: str) -> list:
        out = []
        for style in ("snake", "plain"):
            if all(self.ok(T.label_forms(vocab, c)[0 if style == "snake" else 1]) for c in T.CLASSES):
                out.append(style)
        return out

    def flag_phr(self, wf: str, fid: str) -> list:
        _f, _c, a, b = next(x for x in T.FLAGS[wf] if x[0] == fid)
        return [p for p, nm in ((0, a), (1, b)) if self.ok(f"{nm}: true") and self.ok(f"{nm}: false")]

    def flags(self, wf: str) -> list:
        return [x for x in T.FLAGS[wf] if self.flag_phr(wf, x[0])]

    def wf_ok(self, wf: str) -> bool:
        fl = self.flags(wf)
        cov = {c for _f, c, *_ in fl if c in ("H", "D", "E")} | {PO.num_class(wf)}
        return cov == {"H", "D", "E"} and any(c == "A" for _f, c, *_ in fl) and any(
            self.vocab_styles(v) for v in T.DOMAINS[wf])


class PairCtx(KitCtx):
    """A KitCtx whose wording draw is made once per seed PAIR and question form: the antithetic seeds (2m, 2m + 1) and a
    complement partner of the same pair read the same wording, so every wording cell holds exactly 50% yes."""

    def __init__(self, base: KitCtx):
        super().__init__(skins=base.skins, lexicon=base.lexicon)

    def pick(self, family, kind, row_key_, *, register=None, qform=None, exclude=(), held_out=False):
        if kind == "wording" and isinstance(row_key_, str) and row_key_.startswith(FAMILY + "|"):
            parts = row_key_.split("|")
            if len(parts) == 4 and parts[1].isdigit():                  # T46|seed|sampler|qform
                row_key_ = f"{FAMILY}|{parts[2]}|pair{int(parts[1]) // 2}|{qform or parts[3]}"
        return super().pick(family, kind, row_key_, register=register, qform=qform, exclude=exclude,
                            held_out=held_out)


class T46Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = G0_SPEC
    G0_SHA256 = "77c3b241c65634093f37756376912730d5e92aa1a6cdd74aed1e5ed9d0eb569d"   # frozen G0_SPEC.md (pin_g0.py)
    SAMPLERS = SAMPLERS
    HELD_OUT_SAMPLERS = HELD_OUT_SAMPLERS
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "decision_table"
    SOLVER_B_MODULE = "families.T46.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("yn_is", "noul", T.PREDICATE, 1),
        QuestionForm("yn_dneg", "noul", T.PREDICATE, 1),
        QuestionForm("yn_not", "noul", T.PREDICATE, -1, "syntactic"),
        QuestionForm("yn_ruledout", "noul", T.PREDICATE, -1, "implicit"),
        QuestionForm("ch_disp", "choice", answer_set="closed"),
    )}
    LABEL_WORDS = tuple(sorted({w for v in T.VOCABS.values() for s in v.values() for w in s.split("_")}))
    CLOSED_WORLD_SENTENCE = T.CLOSED_WORLD
    REGISTERS = T.LAYOUTS_TRAIN + T.LAYOUTS_DEV
    HELD_OUT_REGISTERS = T.LAYOUTS_DEV
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = POLARITY_NEGS
    POLARITY_STRICT_FRAMES = False

    def __init__(self, lexicon=None, pools=None):
        super().__init__(lexicon)
        self.pools = pools or {}
        self._lex = None

    # ------------------------------------------------------------------------------------------- views
    @property
    def lex(self) -> Lex:
        if self._lex is None or self._lex.reg is not self.lexicon:
            if self.lexicon is None:
                raise ContractError("T46 needs its lexicon registry (T46Plugin(lexicon=...))")
            self._lex = Lex(self.lexicon)
        return self._lex

    def ctx_for(self, spec, ctx):
        return PairCtx(POL.screen(ctx, self)[0])

    def _pool_texts(self, group: str, dev: bool, *path) -> list:
        node = self.pools.get(group, {})
        for p in path:
            node = node.get(p, {}) if isinstance(node, dict) else {}
        lst = node.get("dev" if dev else "train", []) if isinstance(node, dict) else []
        return [t for t in lst if self.lex.ok(t)]

    def _glosses(self, cls: str, dev: bool) -> list:
        return self._pool_texts("glosses", dev, cls)

    def _notes(self, wf: str, cls: str, dev: bool) -> list:
        return self._pool_texts("notes_ar", dev, wf, cls)

    def _names_ar(self, dev: bool) -> list:
        lst = self.pools.get("names_ar", {}).get("dev" if dev else "train", [])
        return list(lst)

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in SAMPLERS:
            raise ContractError(f"sampler {sampler!r}")
        held = sampler in HELD_OUT_SAMPLERS
        pair = seed // 2
        key = row_key(seed, sampler)
        is_yn, j = pair_index(pair, sampler)
        qform = T.QFORM_CH
        want_yes = None
        if is_yn:
            qform = wpick(kron(j, 0.7548776662466927, uhash(FAMILY, "qoff", sampler)), QF_YN)
            want_yes = (seed % 2 == 0) != (uhash(FAMILY, "flip", sampler, pair) < 0.5)
        lex = self.lex
        wfs = [w for w in T.TRAIN_WORKFLOWS if lex.wf_ok(w)]
        if held and lex.wf_ok("purchase") and uhash(key, "devwf") < P_DEV_WF:
            wf = "purchase"
        elif wfs:
            wf = upick(uhash(key, "wf"), wfs)
        else:
            raise ContractError("no usable workflow in the lexicon")
        arm = "stated" if uhash(key, "arm") < P_STATED else "plain"
        flags = lex.flags(wf)
        vocabs = [v for v in T.DOMAINS[wf] if lex.vocab_styles(v)]
        vocab = upick(uhash(key, "vocab"), vocabs)
        coded = uhash(key, "coded") < P_CODED
        defs = coded or uhash(key, "defs") < (P_DEFS - P_CODED) / (1 - P_CODED)
        styles = lex.vocab_styles(vocab)
        lstyle = upick(uhash(key, "lstyle"), styles)
        cstyle = "alpha" if uhash(key, "cstyle") < 0.5 else "num"
        if defs and not all(self._glosses(c, held) for c in T.CLASSES):
            if coded:
                raise ContractError("coded labels need admitted glosses")
            defs = False
        variant = int(uhash(key, "variant") * PO.N_VARIANTS) if arm == "stated" else 0
        # the class(es) first (label-first); the display is drawn before the gold
        ask, shown = None, None
        if is_yn:
            if want_yes:
                cls = wpick(kron(j, 0.6180339887498949, uhash(FAMILY, "yoff", sampler)),
                            [(c, CLASS_SHARE[c]) for c in T.CLASSES])
                ask = cls
            else:
                cells = [((T.CLASSES[i], T.CLASSES[k]), JOINT[i][k]) for i in range(4) for k in range(4) if i != k]
                cls, ask = wpick(kron(j, 0.5698402909980532, uhash(FAMILY, "noff", sampler)), cells)
        else:
            m = 2 * j + (seed % 2)
            omit = wpick(kron(m, 0.6180339887498949, uhash(FAMILY, "omit", sampler)), OMIT_W)
            shown = [c for c in T.CLASSES if c != omit]
            # the gold is uniform inside the shown set, drawn by LENGTH RANK of its printed label (round 8, G10 longest_option_gold):
            # the quasi-random draw picks a rank 0..2 and the rank names the class, so the gold-is-longest share is 1/3 up to
            # O(1/n) while every class keeps probability 1/3 inside any shown set (options alone still say nothing).
            if coded:
                lab_len = {c: len(t) for c, t in TX.code_map(f"{key}|codes", cstyle).items()}
            else:
                lab_len = {c: len(T.label_forms(vocab, c)[0 if lstyle == "snake" else 1]) for c in T.CLASSES}
            by_len = sorted(shown, key=lambda c: (-lab_len[c], c))
            cls = upick(kron(m, 0.7548776662466927, uhash(FAMILY, "gold", sampler)), by_len)
        # the special type of the row (label-blind given the class)
        st_b = BOUNDARY[sampler]
        u = uhash(key, "typ")
        if cls == "P":
            typ = "boundary" if u < st_b else ("alarm" if u < st_b + (1 - st_b) * ALARM_P[sampler] else "ordinary")
        else:
            c_n = CONFLICT_N[sampler] if arm == "stated" else 0.0
            typ = "boundary" if u < st_b else ("conflict" if u < st_b + (1 - st_b) * c_n else "ordinary")
        # Arabic
        lang = "en"
        note_decides = False
        if wf in AR_WORKFLOWS and uhash(key, "ar") < P_AR[sampler] and self._names_ar(held) \
                and all(self._notes(wf, c, held) for c in T.CLASSES):
            lang = "ar"
            if arm == "plain" and cls != "P" and uhash(key, "note") < P_NOTE_DECIDES:
                note_decides = True
                typ = "note"
        structure = {"wf": wf, "arm": arm, "variant": variant, "vocab": vocab, "cls": cls, "ask": ask, "shown": shown,
                     "defs": bool(defs), "coded": bool(coded), "lstyle": lstyle, "cstyle": cstyle, "typ": typ,
                     "lang": lang, "dev": held, "flags": [f[0] for f in flags], "ord": 0, "yes": want_yes,
                     "note_decides": note_decides}
        card = PO.card_for(wf, arm, variant, flags)
        if typ == "conflict" and not any(card["lines"][c]["flags"] or card["lines"][c]["num"]
                                         for c in card["order"][card["order"].index(cls) + 1:]):
            typ = structure["typ"] = "ordinary"        # the lowest-priority line has nothing below it (card-only rule)
        for attempt in range(MAX_ATTEMPTS):
            rng = random.Random(f"{key}|build|{attempt}")
            built = self._construct(rng, wf, card, flags, lex, held, cls, typ, lang, note_decides)
            if built is None:
                continue
            slots, vals, phr, note = built
            structure["phr"] = phr
            spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{wf}:" + (f"s{variant}" if arm == "stated" else f"p:{vocab}"),
                        qform, slots, structure=dict(structure), depth=2, deep=False,
                        tags=tuple(sorted({typ, arm, f"lang_{lang}", f"gold_{cls}"})), pack=wf)
            if PO.decide(card, wf, vals) == cls:
                return spec
        raise ContractError(f"no structure reached class {cls} ({key}, {typ}, {arm})")

    def reseed(self, spec: Spec, salt: int):
        """A fresh draw of the facts for the SAME plan (A42-D 3.3 reseed audit): same workflow, arm, card, display, class
        and special type; new phrasing, flags, numbers, names, note and field order. None when no draw reaches the class."""
        st = spec.structure
        card, flags = self.card(spec), self._flags(spec)
        for attempt in range(MAX_ATTEMPTS):
            rng = random.Random(f"{row_key(spec.seed, spec.sampler)}|reseed|{salt}|{attempt}")
            built = self._construct(rng, st["wf"], card, flags, self.lex, st["dev"], st["cls"], st["typ"], st["lang"],
                                    st["note_decides"])
            if built is None:
                continue
            slots, vals, phr, _note = built
            if PO.decide(card, st["wf"], vals) == st["cls"]:
                return spec.replace(slots=slots, structure={**st, "phr": phr, "ord": 1000 + salt})
        return None

    def _construct(self, rng, wf, card, flags, lex, held, cls, typ, lang, note_decides):
        """One label-first draw of the facts (flags, numbers, names, note). None = this draw cannot reach the plan."""
        fids = [f[0] for f in flags]
        phr = {}
        for f in flags:
            ok = lex.flag_phr(wf, f[0])
            phr[f[0]] = ok[int(rng.random() * len(ok))]
        printed = {f: not PO.problem_value(phr[f]) for f in fids}                # all inactive
        nkind, lims = T.NUMERIC[wf][2], T.NUMERIC[wf][3]
        lim = rng.choice(lims)
        if held:
            lim = lim * 3 if nkind == "money" else lim + 3
        delta = 1
        lines = card["lines"]
        decided_by = []          # [("flag", fid) | ("num", None)]
        trigger_num = False
        if cls != "P" and not note_decides:
            ln = lines[cls]
            if typ == "boundary" and ln["num"]:
                decided_by = [("num", None)]
            else:
                pool = [("flag", f) for f in ln["flags"]]
                if ln["num"] and (not pool or rng.random() < 0.35):
                    pool.append(("num", None))
                if not pool:
                    return None
                decided_by = [rng.choice(pool)]
            if typ == "conflict":
                lower = [c for c in card["order"][card["order"].index(cls) + 1:]
                         if lines[c]["flags"] or lines[c]["num"]]
                if not lower:
                    return None
                c2 = rng.choice(lower)
                pool2 = [("flag", f) for f in lines[c2]["flags"]] + ([("num", None)] if lines[c2]["num"] else [])
                decided_by.append(rng.choice(pool2))
        for kind, f in decided_by:
            if kind == "flag":
                printed[f] = PO.problem_value(phr[f])
            else:
                trigger_num = True
        unc = PO.uncovered_flags(card, flags)
        if cls == "P" and typ == "alarm":
            if not unc:
                return None
            k = 1 + int(rng.random() < 0.35 and len(unc) > 1)
            for f in rng.sample(unc, k):
                printed[f] = PO.problem_value(phr[f])
        elif cls != "P" and not note_decides:
            for f in unc:
                if rng.random() < P_DECOY:
                    printed[f] = PO.problem_value(phr[f])
        inclusive = card["inclusive"]
        if nkind == "money":
            lo = max(1, lim // 10)
            clean = rng.randint(lo, max(lo, lim - 100))
            over = lim + max(delta, int(lim * rng.uniform(0.05, 0.9)))
        else:
            clean = rng.randint(1, max(1, lim - 1))
            over = lim + rng.randint(1, max(1, lim // 2))
        if trigger_num:
            if typ == "boundary":
                num = lim if (inclusive and rng.random() < 0.5) else lim + delta
            else:
                num = over
        elif typ == "boundary":
            num = lim - delta if inclusive else lim                     # equal to the limit (strict: not above) / just below
        else:
            num = clean
        # names, ids, note
        pkey, pkind = T.PERSON_KEY[wf]
        if lang == "ar":
            person = rng.choice(self._names_ar(held))
        else:
            person = rng.choice(T.names_for(pkind, held))
        idkey, prefix = T.ID_KEY[wf]
        ident = f"{prefix}-{rng.randint(10000, 99999) if held else rng.randint(1000, 9999)}"
        note_cls = None
        slots = {"ID": S.id_slot(ident), "PERSON": S.name_slot(person)}
        if lang == "ar":
            note_cls = cls if note_decides else "P"
            notes = self._notes(wf, note_cls, held)
            slots["NOTE"] = S.name_slot(rng.choice(notes))
        mk = (lambda n: S.cents_slot(n)) if nkind == "money" else (lambda n: S.count_slot(n))
        slots["NUM"] = mk(num)
        slots["LIM"] = mk(lim)
        for f in fids:
            slots[f"F_{f}"] = fslot(printed[f])
        vals = {"phr": phr, "flags": printed, "num": num, "lim": lim, "note_cls": note_cls}
        return slots, vals, phr, note_cls

    # ------------------------------------------------------------------------------------------- spec -> facts
    def _flags(self, spec: Spec) -> list:
        wf = spec.structure["wf"]
        return [x for x in T.FLAGS[wf] if x[0] in set(spec.structure["flags"])]

    def card(self, spec: Spec) -> dict:
        st = spec.structure
        return PO.card_for(st["wf"], st["arm"], st["variant"], self._flags(spec))

    def vals(self, spec: Spec) -> dict:
        st = spec.structure
        sl = spec.slots
        note_cls = None
        if "NOTE" in sl:
            note_cls = self._note_class(st["wf"], sl["NOTE"].value, st["dev"])
        return {"phr": {k: int(v) for k, v in st["phr"].items()},
                "flags": {f: sl[f"F_{f}"].value == "true" for f in st["flags"]},
                "num": sl["NUM"].value, "lim": sl["LIM"].value, "note_cls": note_cls}

    def _note_class(self, wf: str, text: str, dev: bool) -> str:
        for c in T.CLASSES:
            if text in self.pools.get("notes_ar", {}).get(wf, {}).get(c, {}).get("dev" if dev else "train", []):
                return c
        raise ContractError("a note that is not in the pool")

    def solve_class(self, spec: Spec) -> str:
        return PO.decide(self.card(spec), spec.structure["wf"], self.vals(spec))

    def solve_a(self, spec: Spec):
        c = self.solve_class(spec)
        a = spec.structure["ask"]
        q = spec.qform
        if q == "ch_disp":
            return c
        if q in ("yn_is", "yn_dneg"):
            return int(c == a)
        return int(c != a)

    # ------------------------------------------------------------------------------------------- the row plan
    def _plan(self, spec: Spec, layout: str | None = None, variant: int = 0) -> dict:
        """Everything the text prints, as data (render and canonical share it, so G3 compares text with intent)."""
        st = spec.structure
        wf, key = st["wf"], row_key(spec.seed, spec.sampler)
        card = self.card(spec)
        vals = self.vals(spec)
        flags = self._flags(spec)
        idkey, _ = T.ID_KEY[wf]
        pkey, _ = T.PERSON_KEY[wf]
        nval, lval, nkind = T.NUMERIC[wf][0], T.NUMERIC[wf][1], T.NUMERIC[wf][2]
        sl = spec.slots

        def numtxt(slot):
            return TX.money_text(slot.value) if nkind == "money" else str(slot.value)

        items = [{"key": idkey, "group": "request", "kind": "str", "slot": "ID", "val": sl["ID"].value,
                  "s": sl["ID"].value},
                 {"key": pkey, "group": "request", "kind": "str", "slot": "PERSON", "val": sl["PERSON"].value,
                  "s": sl["PERSON"].value}]
        if "NOTE" in sl:
            items.append({"key": T.NOTE_KEY, "group": "request", "kind": "str", "slot": "NOTE",
                          "val": sl["NOTE"].value, "s": sl["NOTE"].value})
        body = [{"key": nval, "group": "figures", "kind": nkind if nkind == "money" else "count", "slot": "NUM",
                 "val": sl["NUM"].value, "s": numtxt(sl["NUM"])},
                {"key": lval, "group": "figures", "kind": nkind if nkind == "money" else "count", "slot": "LIM",
                 "val": sl["LIM"].value, "s": numtxt(sl["LIM"])}]
        for f, c, a, b in flags:
            nm = a if st["phr"][f] == 0 else b
            body.append({"key": nm, "group": "checks", "kind": "flag", "slot": f"F_{f}",
                         "val": vals["flags"][f], "s": TX.printed_flag(layout or "json", vals["flags"][f]), "fid": f})
        body.sort(key=lambda it: uhash(key, "ord", st["ord"], variant, it["key"]))
        items += body
        # labels
        if st["coded"]:
            labels = TX.code_map(f"{key}|codes", st["cstyle"])
        else:
            labels = {c: T.label_forms(st["vocab"], c)[0 if st["lstyle"] == "snake" else 1] for c in T.CLASSES}
        defs = None
        order_keys = sorted(T.CLASSES, key=lambda c: uhash(key, "defs_order", c))
        if st["defs"]:
            defs = {c: upick(uhash(key, "gloss", c), self._glosses(c, st["dev"])) for c in T.CLASSES}
        policy = None
        if st["arm"] == "stated":
            names = {f: (a if st["phr"][f] == 0 else b) for f, _c, a, b in flags}
            lines = []
            for cls in card["order"]:
                ln = card["lines"][cls]
                conds = [TX.cond_text("flag", names[f], active_value=PO.problem_value(st["phr"][f]))
                         for f in ln["flags"]]
                if ln["num"]:
                    conds.append(TX.cond_text("num", nval, limit=lval, inclusive=card["inclusive"]))
                if conds:
                    lines.append((cls, conds))
            policy = {"lines": lines, "default_cls": "P",
                      "ignore": [names[f] for f in PO.uncovered_flags(card, flags)]}
        rules = TX.rules_block(policy=policy, labels=labels, defs=defs, order_keys=order_keys)
        printed_cls = set()
        if policy:
            printed_cls |= {c for c, _ in policy["lines"]} | {"P"}
        if defs:
            printed_cls |= set(T.CLASSES)
        if st["ask"]:
            printed_cls.add(st["ask"])
        if st["shown"]:
            printed_cls |= set(st["shown"])
        return {"items": items, "labels": labels, "defs": defs, "policy": policy, "rules": rules, "card": card,
                "vals": vals, "printed_cls": printed_cls, "order_keys": order_keys, "flags": flags}

    def _class_of_flag(self, wf: str, fid: str, phr: int, printed: bool) -> str:
        if not PO.is_active(phr, printed):
            return "P"
        c = PO.problem_class(wf, fid)
        return "P" if c == "A" else c

    def canonical(self, spec: Spec) -> dict:
        st = spec.structure
        plan = self._plan(spec)
        vals = plan["vals"]
        fields = {it["key"]: (it["val"] if it["kind"] != "flag" else bool(it["val"])) for it in plan["items"]}
        labels = plan["labels"]
        pol = None
        if plan["policy"]:
            p = plan["policy"]
            pol = {"lines": [[labels[c], list(conds)] for c, conds in p["lines"]], "default": labels[p["default_cls"]],
                   "ignore": list(p["ignore"])}
        meanings = {labels[c]: g for c, g in plan["defs"].items()} if plan["defs"] else {}
        label_class = {labels[c]: c for c in sorted(plan["printed_cls"])}
        flag_class = {}
        for it in plan["items"]:
            if it["kind"] == "flag":
                flag_class[it["key"]] = self._class_of_flag(st["wf"], it["fid"], st["phr"][it["fid"]], it["val"])
        return {"qform": spec.qform, "fields": fields,
                "proposed": labels[st["ask"]] if st["ask"] else None, "policy": pol, "meanings": meanings,
                "label_class": label_class, "flag_class": flag_class, "note_class": vals["note_cls"]}

    # ------------------------------------------------------------------------------------------- render
    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        st = spec.structure
        held = spec.sampler in HELD_OUT_SAMPLERS
        okey = f"{row_key(spec.seed, spec.sampler)}|{spec.qform}"
        skin = skin or ctx.pick(FAMILY, "skin", okey, held_out=held)
        pkey = f"{FAMILY}|{spec.sampler}|pair{spec.seed // 2}|{spec.qform}"
        wording = wording or ctx.pick(FAMILY, "wording", pkey, qform=spec.qform, held_out=held)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, okey)
        layout = skin.register
        variant = int(skin.skin_id.rsplit("-", 1)[1])
        plan = self._plan(spec, layout, variant)
        text, spans = TX.state_text(layout, plan["items"], variant)
        tb = TextBuilder()
        tb.add("state", Filled(text, spans), skin_id=skin.skin_id)
        q = self.QFORMS[spec.qform]
        field_used = CD.place_rules(tb, plan["rules"], q.qtype)
        labels = plan["labels"]
        if q.qtype == "noul":
            tb.add("instructions", TX.question_line(labels[st["ask"]]) + "\n")
        tb.add("instructions", wording.fill({}, {}), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if q.qtype == "choice":
            os_ = build_closed(spec, ans, list(st["shown"]), self.error_models(), row_key=okey,
                               render_key=lambda c: labels[c])
        extra = {"t46": {"wf": st["wf"], "arm": st["arm"], "cls": self.solve_class(spec), "ask": st["ask"], "typ": st["typ"],
                         "coded": st["coded"], "defs": st["defs"], "vocab": st["vocab"], "lstyle": st["lstyle"],
                         "layout": layout, "shown": st["shown"]},
                 "lang_state": st["lang"]}
        rr = assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                          defs_style=CD.defs_style(field_used, "full"), format_style=f"{layout}", extra_meta=extra)
        # the lexicon forms the row uses (G-LEX: every one must be admitted)
        ids = set(rr.row["meta"]["c2"]["lexicon_ids"])
        lex = self.lex
        texts = []
        if not st["coded"]:
            texts += [labels[c] for c in plan["printed_cls"]]
        if plan["defs"]:
            texts += list(plan["defs"].values())
        for it in plan["items"]:
            if it["kind"] == "flag":
                texts.append(f'{it["key"]}: {"true" if it["val"] else "false"}')
            elif it["key"] == T.NOTE_KEY:
                texts.append(it["val"])
        for t in texts:
            fid = lex.form_id(t)
            if fid is None:
                raise ContractError(f"printed text without a lexicon form: {t!r}")
            ids.add(fid)
        rr.row["meta"]["c2"]["lexicon_ids"] = sorted(ids)
        return rr

    def layout_of(self, spec: Spec) -> str:
        """The layout render() draws for the base row (ctx.pick's label-blind rule, replayed)."""
        okey = f"{row_key(spec.seed, spec.sampler)}|{spec.qform}"
        held = spec.sampler in HELD_OUT_SAMPLERS
        lay = T.LAYOUTS_DEV if held else T.LAYOUTS_TRAIN
        ids = [f"T46-SK-{r}-{v:02d}" for r in lay for v in range(TX.N_VARIANTS)]
        return min(ids, key=lambda i: uhash(okey, "skin", i)).split("-")[2]

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        st = spec.structure
        q = spec.qform
        out = []
        seed = spec.seed
        pr = seed // 2                                  # relation draws are per seed PAIR (keeps the wording cells balanced)
        if q in T.COMPLEMENT_PAIRS and uhash(FAMILY, "comp", pr, spec.sampler) < P_COMPLEMENT:
            partners = T.COMPLEMENT_PAIRS[q]
            if q == "yn_is":
                p2 = partners[1] if uhash(FAMILY, "cp", pr, spec.sampler) < 0.7 else partners[0]
            else:
                p2 = upick(uhash(FAMILY, "cp", pr, spec.sampler), partners)
            out.append(RelationProposal("complement", qform=p2))
        if uhash(FAMILY, "equiv", pr, spec.sampler) < P_EQUIV:
            held = spec.sampler in HELD_OUT_SAMPLERS
            lay = [r for r in (T.LAYOUTS_DEV if held else T.LAYOUTS_TRAIN) if r != self.layout_of(spec)]
            out.append(RelationProposal("equiv", register=upick(uhash(FAMILY, "eqreg", pr, spec.sampler), lay)))
        if uhash(FAMILY, "twin", pr, spec.sampler) < (P_TWIN_P if self.solve_class(spec) == "P" else P_TWIN_N):
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        out += self._metamorphic(spec)
        return out

    def _cond_slot_edit(self, spec: Spec, kind: str, fid, *, active: bool):
        """The slot edit that makes one covered condition active (or inactive)."""
        st = spec.structure
        card = self.card(spec)
        if kind == "flag":
            pv = PO.problem_value(st["phr"][fid])
            return f"F_{fid}", fslot(pv if active else not pv)
        lim = spec.slots["LIM"].value
        mk = S.cents_slot if T.NUMERIC[st["wf"]][2] == "money" else S.count_slot
        if active:
            return "NUM", mk(lim + 1)
        return "NUM", mk(max(0, lim - 1) if card["inclusive"] else lim)

    def _twin(self, spec: Spec):
        """Exactly one covered condition toggled; the predicted class comes from the construction (never solve_a)."""
        st = spec.structure
        if st["lang"] == "ar" and st["note_decides"]:
            return None
        card = self.card(spec)
        vals = self.vals(spec)
        wf = st["wf"]
        hits = PO.covered_hits(card, wf, vals)
        n_hits = sum(len(h) for h in hits.values())
        if n_hits > 1:
            return None
        g = st["cls"]
        a = st["ask"]
        shown = st["shown"]
        options = []                                    # (target class, kind, fid, active)
        if n_hits == 1:
            (cls_, [(kind, fid)]), = hits.items()
            if kind == "note":
                return None
            options.append(("P", kind, fid, False))     # remove the single deciding condition -> permit
        else:
            ln = card["lines"]
            for c in ("H", "D", "E"):
                for f in ln[c]["flags"]:
                    options.append((c, "flag", f, True))
                if ln[c]["num"]:
                    options.append((c, "num", None, True))
        if spec.qform == "ch_disp":
            options = [o for o in options if o[0] in shown and o[0] != g]
        else:
            flips = (lambda t: (t == a) != (g == a)) if spec.qform in ("yn_is", "yn_dneg") else \
                (lambda t: (t != a) != (g != a))
            options = [o for o in options if flips(o[0])]
        if not options:
            return None
        tcls = sorted({o[0] for o in options})                       # the target class first (uniform), then a condition of it:
        t0 = upick(uhash(FAMILY, "twinclass", spec.seed, spec.sampler), tcls)      # no workflow / card prior on the twin's class
        options = [o for o in options if o[0] == t0]
        o = upick(uhash(FAMILY, "twinpick", spec.seed, spec.sampler), options)
        name, slot = self._cond_slot_edit(spec, o[1], o[2], active=o[3])
        twin = spec.with_slot(name, slot)
        t = o[0]
        if spec.qform == "ch_disp":
            exp = t
        elif spec.qform in ("yn_is", "yn_dneg"):
            exp = int(t == a)
        else:
            exp = int(t != a)
        return RelationProposal("twin", spec=twin, changed_slot=name, expect=exp)

    def _metamorphic(self, spec: Spec) -> list:
        st = spec.structure
        sl = spec.slots
        wf = st["wf"]
        out = []
        pkey, pkind = T.PERSON_KEY[wf]
        if st["lang"] == "en":
            pool = T.names_for(pkind, st["dev"])
            i0 = int(uhash(FAMILY, "mm1", spec.seed) * len(pool))
            other = next(n for n in pool[i0:] + pool[:i0] if n != sl["PERSON"].value)
            out.append(RelationProposal("metamorphic", spec=spec.with_slot("PERSON", S.name_slot(other)),
                                        expect="same", note="rename the person"))
        prefix = T.ID_KEY[wf][1]
        new_id = f"{prefix}-{(int(sl['ID'].value.split('-')[1]) * 7 + 13) % 9000 + 1000}"
        if new_id != sl["ID"].value:
            out.append(RelationProposal("metamorphic", spec=spec.with_slot("ID", S.id_slot(new_id)), expect="same",
                                        note="another record id"))
        mk = S.cents_slot if T.NUMERIC[wf][2] == "money" else S.count_slot
        scaled = spec.replace(slots={**sl, "NUM": mk(sl["NUM"].value * 2), "LIM": mk(sl["LIM"].value * 2)})
        out.append(RelationProposal("metamorphic", spec=scaled, expect="same", note="double both numbers"))
        out.append(RelationProposal("metamorphic", spec=spec.replace(structure={**st, "ord": st["ord"] + 1}),
                                    expect="same", note="reorder the fields"))
        vocs = [v for v in T.DOMAINS[wf] if v != st["vocab"] and self.lex.vocab_styles(v)
                and st["lstyle"] in self.lex.vocab_styles(v)]
        if vocs:
            out.append(RelationProposal("metamorphic", spec=spec.replace(structure={**st, "vocab": vocs[0]}),
                                        expect="same", note="another label vocabulary"))
        fl = [f for f in st["flags"] if len(self.lex.flag_phr(wf, f)) == 2]
        if fl:
            f = upick(uhash(FAMILY, "mm2", spec.seed, spec.sampler), fl)
            new_phr = {**st["phr"], f: 1 - st["phr"][f]}
            val = sl[f"F_{f}"].value == "true"
            sl2 = {**sl, f"F_{f}": fslot(not val)}                  # same activity under the other phrasing
            out.append(RelationProposal("metamorphic", spec=spec.replace(structure={**st, "phr": new_phr}, slots=sl2),
                                        expect="same", note="re-phrase one flag"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def card_vals(spec):
            return self.card(spec), self.vals(spec), spec.structure["wf"]

        def any_problem(target):
            def fn(spec):
                card, vals, wf = card_vals(spec)
                st = spec.structure
                active = any(PO.is_active(vals["phr"][f], vals["flags"][f]) and PO.problem_class(wf, f) != "A"
                             for f in st["flags"])
                return target if active else "P"
            return fn

        def alarm_human(spec):
            card, vals, wf = card_vals(spec)
            alarm = any(PO.is_active(vals["phr"][f], vals["flags"][f]) for f in PO.uncovered_flags(card, self._flags(spec)))
            return "E" if alarm else None

        def unprinted(spec):
            card, vals, wf = card_vals(spec)
            return PO.decide({**card, "order": list(PO.PRIORITY_PLAIN)}, wf, vals)

        def trust_name(spec):
            card, vals, wf = card_vals(spec)
            return PO.decide(PO.plain_card(wf, self._flags(spec)), wf, vals)

        return {"any_problem_means_stop": error_model("any_problem_means_stop", any_problem("D")),
                "any_problem_means_wait": error_model("any_problem_means_wait", any_problem("H")),
                "alarm_means_human": error_model("alarm_means_human", alarm_human),
                "unprinted_priority": error_model("unprinted_priority", unprinted),
                "trust_flag_name": error_model("trust_flag_name", trust_name)}


# ------------------------------------------------------------------------------------------------ the kit context
def build_registry(pools: dict, *, standin: bool) -> LexiconRegistry:
    """The T46 lexicon: label forms, flag-value forms, gloss forms, Arabic note forms, question wordings. standin=True
    admits every form by a program stand-in extraction (tests only); otherwise forms stay pending until haiku_author
    records the 2/2 reads."""
    reg = LexiconRegistry(FAMILY)
    for c in T.CLASSES:
        reg.declare(T.SEM_OF[c], "status", T.MEANING[c])
    reg.declare("x.notify", "status", "tell someone about it but still carry on")             # decoys: no forms
    reg.declare("x.partial", "status", "carry out only part of it")
    for qf, meaning in T.QFORM_MEANING.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    reg.declare("x.q_why", "question", "asks why the record looks the way it does")
    reg.declare("x.q_who", "question", "asks who filed the request")
    add = []
    for v in T.VOCABS:
        for c in T.CLASSES:
            for t in dict.fromkeys(T.label_forms(v, c)):
                add.append((t, T.SEM_OF[c], False))
    for wf, fl in T.FLAGS.items():
        for _f, c, a, b in fl:
            cls = "P" if c == "A" else c
            add.append((f"{a}: true", T.SEM_OF[cls], wf == "purchase"))
            add.append((f"{a}: false", T.SEM_OF["P"], wf == "purchase"))
            add.append((f"{b}: false", T.SEM_OF[cls], wf == "purchase"))
            add.append((f"{b}: true", T.SEM_OF["P"], wf == "purchase"))
    for c, parts in pools.get("glosses", {}).items():
        for part, held in (("train", False), ("dev", True)):
            for t in parts.get(part, []):
                add.append((t, T.SEM_OF[c], held))
    for wf, byc in pools.get("notes_ar", {}).items():
        for c, parts in byc.items():
            for part, held in (("train", False), ("dev", True)):
                for t in parts.get(part, []):
                    add.append((t, T.SEM_OF[c], held))
    seen = set()
    for text, sem, held in add:
        if _norm(text) in seen:
            continue
        seen.add(_norm(text))
        reg.add(text, sem, family=FAMILY, held_out=held)
    for qf, parts in pools.get("wordings", {}).items():
        for part, held in (("train", False), ("dev", True)):
            for t in parts.get(part, []):
                if _norm(t) in seen:
                    continue
                seen.add(_norm(t))
                reg.add(t, question_sem(FAMILY, qf), family=FAMILY, held_out=held)
    return reg


def make_ctx(pools: dict | None = None, *, standin: bool = True, registry: LexiconRegistry | None = None) -> KitCtx:
    from . import fixtures as FX
    pools = FX.POOLS if pools is None else pools
    reg = registry or build_registry(pools, standin=standin)
    if registry is None:
        reg.unit_test_all()
        if standin:
            for fid, f in reg.forms.items():
                for e in range(f.required):
                    reg.record_extraction(fid, f"program:stand-in-{e + 1}", f.sem_id)
    skins = {}
    for r in T.LAYOUTS_TRAIN + T.LAYOUTS_DEV:
        for v in range(TX.N_VARIANTS):
            sk = make_skin(f"T46-SK-{r}-{v:02d}", FAMILY, f"{r} layout {TX.WORDS[v]}", {}, kind="skin", register=r,
                           held_out=r in T.LAYOUTS_DEV)
            skins[sk.skin_id] = sk
    for qf, parts in pools.get("wordings", {}).items():
        for part, held in (("train", False), ("dev", True)):
            for i, t in enumerate(parts.get(part, [])):
                fid = next((i2 for i2, f in reg.forms.items() if f.text == t), None)
                if fid is None:
                    continue
                sk = make_skin(f"T46-W-{qf}-{part[0]}{i}", FAMILY, t, {}, kind="wording", register="question",
                               qform=qf, lexicon_ids=(fid,), held_out=held)
                skins[sk.skin_id] = sk
    return KitCtx(skins=skins, lexicon=reg)


def make_plugin(pools: dict | None = None, *, standin: bool = True) -> tuple:
    from . import fixtures as FX
    pools = FX.POOLS if pools is None else pools
    ctx = make_ctx(pools, standin=standin)
    return T46Plugin(lexicon=ctx.lexicon, pools=pools), ctx

