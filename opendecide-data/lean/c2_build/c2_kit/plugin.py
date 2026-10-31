"""c2_kit/plugin.py: the plugin contract every C2 family implements (C2_DATA_SPEC 3.0, 4.1, 6.2-6.4).

A family plugin is a subclass of C2Plugin plus one separate solver-B module. The kit's pipeline (pipeline.py) runs
every program gate on it in memory: G2 (solver B = solver A on 100%), G3 (parse = generator facts), G4 (metamorphic
predictions), G-SL, G-LEX, G-TW and G15. See c2_build/README.md for the contract in one table and reference/r00.py
for a complete example.

Data flow for one row (spec 2.1 pipeline, C2 changes in 3.0):
  spec = plugin.sample(seed, sampler)                    hidden structure + typed slots + question form (label-blind)
  gold = plugin.solve_a(spec)                            solver A on the Spec object
  rr   = plugin.render(spec, ctx, skin=, wording=, forms=, attack=)   RenderedRow: row (spec 2.4 + meta.c2) + spans
  view = plugin.parse(rr.row, ctx)                       solver-B module: independent parser of the RENDERED row
  plugin.solve_b(view) == gold                           solver-B module: another paradigm on the parsed view
  view["options"][gold position] == gold                 choice rows: parse() also reads every option text back
                                                         to its key, so the key -> text mapping is checked too
  view minus "options" == plugin.canonical_for(spec, author_mode)   G3: the text carries the generator's facts
  plugin.relations(spec)                                 complement / twin / equiv / inv / metamorphic proposals

Answers: a yes/no ("noul") answer is 1 or 0; a choice answer is the option KEY (a canonical value such as an ISO date,
a rule id or a verdict id). render() maps keys to option texts; the row's gold is 1/0 or the gold option's text.
"""
from __future__ import annotations

import abc
import ast
import dataclasses
import hashlib
import importlib
import inspect
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import slots as S
from .distractors import ErrorModel, OptionSet, uhash

FAMILIES = {
    # agent tier (spec 2.1)
    "T28": "agent", "T35": "agent", "T33": "agent", "T29": "agent", "T30": "agent", "T27": "agent", "T26": "agent",
    "T31": "agent", "T32": "agent",
    # post-freeze agent-tier program block (Ruling A59; not one of the 10 program families, no OHS-AC split)
    "T46": "agent",
    # everyday tier
    "T01": "everyday", "T23": "everyday", "T24": "everyday", "T06": "everyday", "T15": "everyday", "T12": "everyday",
    "T07": "everyday", "T25": "everyday",
    # real-text complements (its own builder; not a C2Plugin family)
    "T37b": "real_text",
    # transfer dev only, never trained (spec 2.2)
    "T36": "transfer_dev", "T19": "transfer_dev", "T21": "transfer_dev", "T20": "transfer_dev",
}
REFERENCE_FAMILIES = {"R00": "reference"}       # kit examples: never written, never trained
TIERS = ("agent", "everyday", "real_text", "transfer_dev", "reference")
PARADIGMS = ("ast_interpreter", "rule_engine", "decision_table", "brute_force_enumeration", "day_bitmap",
             "interval_scan", "sql_sqlite", "regex_compile", "trie_longest_match", "sort_group", "state_machine",
             "event_sourcing", "simulator", "set_algebra", "integer_arithmetic", "independent_interpreter",
             "string_compare", "matrix_counter")
RELATION_KINDS = ("complement", "twin", "equiv", "inv", "metamorphic", "premise_removal")
COMPLEMENT_KINDS = ("syntactic", "antonym", "option_framing", "implicit")
QTYPES = ("noul", "choice")
B_FORBIDDEN_MODULES = ("c2_kit.rules", "c2_kit.glob_a")
B_FORBIDDEN_NAMES = ("solve_a", "fill", "fill_freeform", "render", "evaluate", "evaluate3", "resolve")


class ContractError(TypeError):
    pass


# ------------------------------------------------------------------------------------------------ data classes

@dataclass(frozen=True)
class QuestionForm:
    qform: str
    qtype: str                         # noul | choice
    predicate: str = ""                # noul: the predicate asked; complement forms share it
    polarity: int = 1                  # +1 asks the predicate, -1 asks its complement
    complement_kind: str | None = None  # polarity -1: syntactic | antonym | option_framing | implicit
    yes_is_bad: bool | None = None     # G10 "yes = bad outcome" balance
    answer_set: str = "closed"         # choice: closed (whole label set) | open (error-model distractors)
    abstain: bool = False              # the form can show an abstain option

    def __post_init__(self):
        if self.qtype not in QTYPES or self.polarity not in (1, -1) or self.answer_set not in ("closed", "open"):
            raise ContractError(f"question form {self.qform}: qtype / polarity / answer_set")
        if self.qtype == "noul" and not self.predicate:
            raise ContractError(f"yes/no form {self.qform} names its predicate")
        if self.polarity == -1 and self.complement_kind not in COMPLEMENT_KINDS:
            raise ContractError(f"complement form {self.qform} needs complement_kind in {COMPLEMENT_KINDS}")
        if self.qtype == "noul" and self.abstain:
            raise ContractError("yes/no rows never abstain (spec 3.0)")


@dataclass
class Spec:
    family: str
    sampler: str
    seed: int
    card_id: str
    qform: str
    slots: dict                                   # input facts: name -> Slot
    structure: dict = field(default_factory=dict)  # JSON-able hidden structure; refers to slots by name
    derived: dict = field(default_factory=dict)    # printed intermediates: name -> Slot (plugin.derive recomputes)
    derived_deps: dict = field(default_factory=dict)  # derived name -> tuple of input slot names
    closed_world: bool = True
    depth: int = 0
    deep: bool = False
    tags: tuple = ()                              # trap tags (spec 3.x trap tables)
    pack: str | None = None
    persona_seed: str | None = None

    def all_slots(self) -> dict:
        both = set(self.slots) & set(self.derived)
        if both:
            raise ContractError(f"slot names used twice: {sorted(both)}")
        return {**self.slots, **self.derived}

    def env(self) -> dict:
        """slot -> python value (a clause gives its sem id)."""
        return {k: (v.value[0] if v.kind == "clause" else v.value) for k, v in self.all_slots().items()}

    def schema(self) -> dict:
        return {k: v.schema for k, v in self.all_slots().items()}

    def facts(self) -> dict:
        return {"family": self.family, "sampler": self.sampler, "qform": self.qform,
                "slots": {k: [v.kind, S.canonical(v)] for k, v in sorted(self.slots.items())},
                "derived": {k: [v.kind, S.canonical(v)] for k, v in sorted(self.derived.items())},
                "structure": self.structure, "closed_world": self.closed_world}

    def structure_hash(self) -> str:
        return hashlib.sha256(json.dumps(self.facts(), sort_keys=True, default=str).encode()).hexdigest()

    def replace(self, **kw) -> "Spec":
        base = {f.name: getattr(self, f.name) for f in dataclasses.fields(self)}
        for k in ("slots", "structure", "derived", "derived_deps"):
            base[k] = dict(base[k])
        base.update(kw)
        return Spec(**base)

    def with_slot(self, name: str, slot) -> "Spec":
        """A copy with one input slot changed (slot None removes it: premise-removal twins)."""
        if name not in self.slots:
            raise ContractError(f"{name} is not an input slot")
        new = dict(self.slots)
        if slot is None:
            del new[name]
        else:
            if slot.kind != self.slots[name].kind:
                raise ContractError(f"{name}: kind {slot.kind} != {self.slots[name].kind}")
            new[name] = slot
        return self.replace(slots=new)


@dataclass
class RenderedRow:
    row: dict
    spans: list                       # skin.Span list over the row fields
    forms: dict                       # slot -> form used (twins and partners reuse it)
    option_set: OptionSet | None = None
    skin_id: str | None = None
    wording_id: str | None = None
    attack_id: str | None = None
    register: str | None = None
    regions: dict = field(default_factory=dict)   # skin id -> (field, start, end): where its text sits in the row

    def text(self, fld: str) -> str:
        v = self.row.get(fld)
        if fld == "options":
            return "\n".join(v or [])
        return v or ""

    @property
    def answer(self):
        """The gold KEY (noul: 1/0; choice: the gold option's key)."""
        if self.row["qtype"] == "noul":
            return self.row["gold"]
        return self.option_set.gold.key


@dataclass
class RelationProposal:
    kind: str                          # complement | twin | equiv | inv | metamorphic | premise_removal
    spec: Spec | None = None           # partner spec (twin, metamorphic, premise_removal); None = the same spec
    qform: str | None = None           # complement: the partner question form
    changed_slot: str | None = None    # twin / premise_removal: the one input slot that changes
    expect: Any = None                 # predicted partner answer, from the construction (never from solve_a)
    register: str | None = None        # equiv: another register or container
    attack: str | None = None          # inv: attack skin id (None: ctx picks one)
    note: str = ""

    def __post_init__(self):
        if self.kind not in RELATION_KINDS:
            raise ContractError(f"relation kind {self.kind!r}")


@dataclass
class KitCtx:
    """What render() and parse() may use: the skin pools (skins, wordings, program templates, attack lines) and the
    lexicon registry. pick() is label-blind: a seeded draw from the row key."""
    skins: dict = field(default_factory=dict)
    lexicon: Any = None

    def skin(self, skin_id: str):
        return self.skins[skin_id]

    def pick(self, family: str, kind: str, row_key: str, *, register: str | None = None, qform: str | None = None,
             exclude: tuple = (), held_out: bool = False):
        c = [s for s in self.skins.values() if s.family == family and s.kind == kind and s.held_out == held_out
             and (register is None or s.register == register) and (qform is None or s.qform == qform)
             and s.skin_id not in exclude]
        if not c:
            raise LookupError(f"no {kind} for {family} (register={register}, qform={qform}, held_out={held_out})")
        return min(c, key=lambda s: uhash(row_key, kind, s.skin_id))


# ------------------------------------------------------------------------------------------------ the contract

class C2Plugin(abc.ABC):
    """Subclass, fill the class attributes, implement the six abstract methods, and put parse(row, ctx) and
    solve_b(view) in the module named by SOLVER_B_MODULE. validate_plugin(plugin) checks the whole contract."""

    FAMILY: str = ""
    TIER: str = ""
    G0_LITE: Path | None = None          # the frozen one-page G0-lite spec (spec 6.2 item 3)
    G0_SHA256: str | None = None         # its sha256, set when frozen
    SAMPLERS: tuple = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS: tuple = ("S5",)   # mixdev only, never a training row
    PARADIGM_A: str = ""
    PARADIGM_B: str = ""
    SOLVER_B_MODULE: str = ""            # dotted module path: parse(row, ctx) -> view; solve_b(view) -> answer
    QFORMS: dict = {}                    # qform id -> QuestionForm
    LABEL_WORDS: tuple = ()              # gold-label words (G-SL: never in skin text)
    CLOSED_WORLD_SENTENCE: str = ""      # printed on every card whose rows carry complements (spec 4.1)
    REGISTERS: tuple = ()                # >= 8 per family (spec 3.0)
    HELD_OUT_REGISTERS: tuple = ()       # >= 2, mixdev / transfer dev only
    GSL_EXCEPTIONS: dict = {}            # extended-lint word -> reason (must be listed in the G0-lite spec)
    NAME_ALLOW: tuple = ()               # capitalised words skins may use that are not names (pack glossary)
    # wording polarity (c2_kit.polarity; opt in): a yes/no wording must read with its form's declared polarity
    POLARITY_CHECK: bool = False         # True: authoring, ctx screening and the pipeline's G-LEX check apply the rule
    POLARITY_NEGATIVES: tuple = ()       # regexes: the family's negative / antonym predicates (bar, skip, ...)
    POLARITY_BASE: dict = {}             # predicate -> negations its positive phrasing itself carries (default 0)
    POLARITY_STRICT_FRAMES: bool = False  # also refuse the "aux + subject + not" negative question frame
    POLARITY_SKIP: tuple = ()            # yes/no forms exempt (option-framing complements are always exempt)

    def __init__(self, lexicon=None):
        self.lexicon = lexicon           # the family's frozen LexiconRegistry (sample() draws admitted forms)

    @abc.abstractmethod
    def sample(self, seed: int, sampler: str) -> Spec:
        """Draw one spec (structure, slots, question form) from a sampler. Label-blind display choices only."""

    @abc.abstractmethod
    def solve_a(self, spec: Spec) -> Any:
        """Solver A: the answer key for spec.qform (1/0 or an option key)."""

    @abc.abstractmethod
    def canonical(self, spec: Spec) -> dict:
        """The JSON-able facts a correct parse of the rendered row must return (G3 target; parse() returns this)."""

    @abc.abstractmethod
    def render(self, spec: Spec, ctx: KitCtx, *, skin=None, wording=None, forms: dict | None = None,
               attack=None) -> RenderedRow:
        """Row text + spans. skin / wording None: pick label-blind from ctx. forms None: kit.choose_forms()."""

    @abc.abstractmethod
    def relations(self, spec: Spec) -> list:
        """RelationProposals for the overlay (spec 4.1) and the G4 metamorphic checks (spec 6.3)."""

    @abc.abstractmethod
    def error_models(self) -> dict:
        """{name: ErrorModel}: every wrong option comes from one of these (spec 3.0)."""

    # ---------------------------------------------------------------------------------- defaults
    def derive(self, spec: Spec) -> Spec:
        """Recompute derived (printed) slots after an input changed. Default: none."""
        return spec

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        """G3 target for a row whose skin is in `author_mode`. Mode F narrative facts are checked by G3-H, so a
        family returns here only the facts its program parser reads from program-rendered text. Default: all."""
        return self.canonical(spec)

    def extract_view(self, spec: Spec) -> dict:
        """G3-H: the facts a Haiku extractor must recover from a Mode F text (default: canonical)."""
        return self.canonical(spec)

    def extract_fields(self, spec: Spec) -> list:
        """G3-H: [g3h.Field] describing extract_view (Mode F families implement it)."""
        raise NotImplementedError(f"{self.FAMILY}: Mode F needs extract_fields()")

    def solver_b_module(self):
        return importlib.import_module(self.SOLVER_B_MODULE)

    def parse(self, row: dict, ctx: KitCtx) -> dict:
        return self.solver_b_module().parse(row, ctx)

    def solve_b(self, view: dict) -> Any:
        return self.solver_b_module().solve_b(view)


def choose_forms(spec: Spec, row_key: str, allowed: dict | None = None) -> dict:
    """Label-blind slot forms for one row. One seeded form order per kind, so a row writes all its dates (amounts,
    counts ...) the same way; each slot takes the first form in that order that is free and valid for its value
    (slots.free_forms; `allowed[slot]` narrows it). Templates pin context forms themselves ({X:int_cents})."""
    out = {}
    for name, slot in sorted(spec.all_slots().items()):
        free = S.free_forms(slot)
        opts = [f for f in ((allowed or {}).get(name) or free) if f in S.forms(slot)]
        if not opts:
            raise ContractError(f"no valid form for slot {name}")
        group = slot.kind if slot.kind != "category" else f"category:{name}"
        order = sorted(S.form_names(slot.kind, slot.params), key=lambda f: uhash(row_key, "form", group, f))
        out[name] = next((f for f in order if f in opts), opts[0])
    return out


# ------------------------------------------------------------------------------------------------ validation

def _imports_and_names(module) -> tuple:
    src = inspect.getsource(module)
    tree = ast.parse(src)
    pkg = module.__package__ or ""
    mods, names = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                mods.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                parts = pkg.split(".")
                parts = parts[: len(parts) - node.level + 1] if node.level > 1 else parts
                base = ".".join(p for p in parts + ([base] if base else []) if p)
            mods.add(base)
            for a in node.names:
                mods.add(f"{base}.{a.name}")
                names.add(a.name)
        elif isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
    return mods, names


def check_independence(plugin: C2Plugin) -> list:
    """Solver B shares no code path with solver A or the renderer (direct imports and names of the solver-B module)."""
    probs = []
    try:
        mod_b = plugin.solver_b_module()
    except Exception as e:  # noqa: BLE001
        return [f"solver-B module {plugin.SOLVER_B_MODULE!r} does not import: {e}"]
    for fn in ("parse", "solve_b"):
        if not callable(getattr(mod_b, fn, None)):
            probs.append(f"solver-B module lacks {fn}()")
    mod_a = type(plugin).__module__
    if mod_b.__name__ == mod_a:
        probs.append("solver B lives in the solver-A module")
    mods, names = _imports_and_names(mod_b)
    forbid = set(B_FORBIDDEN_MODULES) | {mod_a}
    for m in sorted(mods):
        for f in forbid:
            short = f.split(".", 1)[1] if f.startswith("c2_kit.") else None
            if m == f or m.startswith(f + ".") or (short and m.endswith("c2_kit." + short)):
                probs.append(f"solver B imports {m} (solver-A side)")
    for n in sorted(set(B_FORBIDDEN_NAMES) & names):
        probs.append(f"solver B uses the name {n!r} (solver-A or renderer code)")
    return probs


def validate_plugin(plugin: C2Plugin, *, strict: bool = True) -> list:
    """Every contract problem (empty list = the plugin may enter the pilot). strict=False for kit examples."""
    probs = []
    fam = plugin.FAMILY
    tier = FAMILIES.get(fam) or REFERENCE_FAMILIES.get(fam)
    if tier is None:
        probs.append(f"family {fam!r} is not in the C2 family registry")
    elif plugin.TIER != tier:
        probs.append(f"TIER {plugin.TIER!r} != registry tier {tier!r}")
    if strict and fam in REFERENCE_FAMILIES:
        probs.append(f"{fam} is a kit reference family (strict validation is for C2 families)")
    train = [s for s in plugin.SAMPLERS if s not in plugin.HELD_OUT_SAMPLERS]
    if len(train) < 4 or "S5" not in plugin.SAMPLERS or "S5" not in plugin.HELD_OUT_SAMPLERS:
        probs.append("samplers: >= 4 training samplers and the held-out S5 (spec 3.0)")
    if plugin.PARADIGM_A not in PARADIGMS or plugin.PARADIGM_B not in PARADIGMS:
        probs.append(f"paradigms must come from {PARADIGMS}")
    if plugin.PARADIGM_A == plugin.PARADIGM_B:
        probs.append("solver B must use a different paradigm from solver A")
    probs += check_independence(plugin)
    g0 = Path(plugin.G0_LITE) if plugin.G0_LITE else None
    if g0 is None or not g0.is_file():
        probs.append("G0-lite spec file missing")
    else:
        n = len(g0.read_text(encoding="utf-8").splitlines())
        if n > 200:
            probs.append(f"G0-lite spec has {n} lines (one page: <= 200, semantics table <= ~150)")
        sha = hashlib.sha256(g0.read_bytes()).hexdigest()
        if plugin.G0_SHA256 and plugin.G0_SHA256 != sha:
            probs.append(f"G0-lite spec changed since it was frozen ({sha[:12]} != {plugin.G0_SHA256[:12]})")
        if strict and not plugin.G0_SHA256:
            probs.append("G0-lite spec is not frozen (G0_SHA256 unset)")
    qf = plugin.QFORMS
    if not qf or any(k != v.qform for k, v in qf.items()):
        probs.append("QFORMS: {qform id: QuestionForm} with matching ids")
    else:
        for q in qf.values():
            if q.qtype == "noul" and q.polarity == -1 and not any(
                    p.qtype == "noul" and p.predicate == q.predicate and p.polarity == 1 for p in qf.values()):
                probs.append(f"complement form {q.qform} has no positive form for {q.predicate}")
        pairs = [q for q in qf.values() if q.qtype == "noul" and q.polarity == -1]
        if strict and not pairs:
            probs.append("no complement question form (overlay: >= 20% of yes/no rows in complement pairs)")
        if strict and not any(q.complement_kind in ("antonym", "option_framing", "implicit") for q in pairs):
            probs.append("no non-syntactic complement form (overlay: >= 30% of complement pairs)")
    try:
        ems = plugin.error_models()
        if not ems:
            probs.append("error_models() is empty")
        for k, m in ems.items():
            if not isinstance(m, ErrorModel) or m.name != k:
                probs.append(f"error model {k!r} is not an ErrorModel named {k!r}")
    except Exception as e:  # noqa: BLE001
        probs.append(f"error_models() raised {e}")
    if not plugin.LABEL_WORDS:
        probs.append("LABEL_WORDS is empty (G-SL needs the gold-label words)")
    if not plugin.CLOSED_WORLD_SENTENCE:
        probs.append("CLOSED_WORLD_SENTENCE is empty (complements are exact only under it)")
    if strict and (len(plugin.REGISTERS) < 8 or len(plugin.HELD_OUT_REGISTERS) < 2
                   or not set(plugin.HELD_OUT_REGISTERS) <= set(plugin.REGISTERS)):
        probs.append("registers: >= 8, of which >= 2 held out (spec 3.0)")
    from . import gsl, polarity
    probs += gsl.check_exceptions(plugin.GSL_EXCEPTIONS)
    probs += polarity.config_problems(plugin)
    return probs
