"""F1 canonical structure (G0 F1 v7 section 2): attributes, literals, items, rules, notices, inert elements, policy, case.

Plain data only. Solver A (solver_a.py) and solver B (solver_b.py) each evaluate it with their own code; the parser
(parse_f1.py) builds the same classes from text. Dates are day ordinals (int); numbers are Decimal on the field's step.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from decimal import Decimal

NUM_OPS = ("ge", "gt", "le", "lt", "between", "within")
DATE_OPS = ("before", "onbefore", "after", "onafter", "fromto")
CAT_OPS = ("in", "notin")


@dataclass(frozen=True)
class Attr:
    key: str                 # row-local id ("f1".."f14"); also the stable sort key
    name: str                # display name (pack vocabulary)
    type: str                # bool | num | date | cat
    unit: str = ""
    places: int = 0
    step: Decimal = Decimal(1)
    lo: object = None        # Decimal (num) | int ordinal (date domain, open-world unknown dates)
    hi: object = None
    values: tuple = ()
    daycount: bool = False
    anchor: str | None = None
    true: str = ""           # bool: true-phrasing template ({S} = subject reference)
    false: str | None = None  # bool: explicit-negative phrasing (row-4 cue) or None
    presup: str | None = None  # bool: row key of the presupposed Boolean field, if on the row
    role: str = "normal"     # normal | gov | distractor | listed
    money: bool = False
    pack_key: str = ""


@dataclass(frozen=True)
class Lit:
    attr: str
    op: str
    args: tuple

    def canon(self, attrs: dict):
        """Canonical (attr, op, args): strict -> inclusive on the grid (the only merge, F1R2-A04)."""
        a = attrs[self.attr]
        op, args = self.op, self.args
        if a.type == "num":
            s = a.step
            if op == "gt":
                return (self.attr, "ge", (args[0] + s,))
            if op == "lt":
                return (self.attr, "le", (args[0] - s,))
            if op == "within":
                return (self.attr, "le", (args[0],))
            return (self.attr, op, tuple(args))
        if a.type == "date":
            if op == "before":
                return (self.attr, "le", (args[0] - 1,))
            if op == "onbefore":
                return (self.attr, "le", (args[0],))
            if op == "after":
                return (self.attr, "ge", (args[0] + 1,))
            if op == "onafter":
                return (self.attr, "ge", (args[0],))
            if op == "fromto":
                return (self.attr, "between", tuple(args))
        if a.type == "cat":
            return (self.attr, op, tuple(sorted(args)))
        return (self.attr, op, tuple(args))


@dataclass(frozen=True)
class Item:
    kind: str                # lit | or | xor | all | any | kofn | not   ("not" = the unless item, not-B)
    mem: tuple               # tuple[Lit]
    k: int = 0

    def canon(self, attrs: dict):
        return (self.kind, tuple(sorted((m.canon(attrs) for m in self.mem), key=repr)), self.k)


@dataclass
class Rule:
    rid: int
    kind: str                # gen | pexc | oexc | onlyif
    items: tuple             # tuple[Item] (condition items; the unless part is separate)
    unless: Lit | None = None
    out: str | None = None   # outcome (gen / oexc) or Y (onlyif)
    target: int | None = None
    tier: int | None = None  # PRIORITY tier index, 0 = highest
    date: int | None = None  # printed in-force-from date (LATER cards); None -> B
    last: int | None = None  # last-applicable date (inclusive), governing-date field

    def all_items(self):
        """Condition items including the unless item ('not', B)."""
        its = list(self.items)
        if self.unless is not None:
            its.append(Item("not", (self.unless,)))
        return tuple(its)

    def copy(self, **kw):
        return replace(self, **kw)


@dataclass
class Notice:
    num: int
    ntype: str               # replace | repeal | insert
    target: int | None       # replace / repeal target id
    rule: Rule | None        # whole new text (replace: rid = target; insert: the new id)
    ndate: int
    edate: int
    pos: tuple | None = None  # S3 insert position: ("top",) | ("bottom",) | ("after", k)

    def copy(self, **kw):
        return replace(self, **kw)


@dataclass
class Inert:
    cls: str                 # draft | other_scope | comment | other_body
    num: int | None = None   # other_body: notice number (never equal to an operative id / number)
    notice: Notice | None = None   # draft / other_body content (applied only by error model E15)
    rule: Rule | None = None       # other_scope rule (never in force)
    scope_value: str | None = None
    body: str | None = None        # other_body issuing body
    text: str | None = None        # comment text
    where: str = "policy"          # policy | after_rules | notices


@dataclass
class Policy:
    world: str               # closed | open | missing
    prim: str                # SPEC | LATER | PRIORITY | ORDER
    sec: str | None
    tie: str                 # esc | strict
    strict: tuple            # strictness order, strictest first (tie == strict)
    outcomes: tuple          # card outcomes (display names; masking happens at render time)
    roles: dict              # outcome -> escalate | default | fallback | M | other
    valence: dict            # outcome -> bad | good
    default: str
    escalate: str
    fallback: str | None
    M: str | None
    gov: str                 # attr key of the governing-date field
    body: str                # issuing body
    B: int                   # base effective date
    listed: tuple = ()       # missing-field listed attr keys
    tiers: tuple = ()        # tier display names, highest first
    scope_name: str | None = None
    scope_value: str | None = None


@dataclass
class Case:
    vals: dict               # attr key -> value (bool | Decimal | int ordinal | str); unknown / not-recorded keys absent
    unknown: frozenset = frozenset()
    notrec: frozenset = frozenset()
    ref: str = ""            # case id text (subject reference)

    def g(self, policy: Policy) -> int:
        return self.vals[policy.gov]

    def copy(self, **kw):
        return replace(self, **kw)


@dataclass
class Struct:
    attrs: dict              # key -> Attr (row fields: Fields block order = sorted keys)
    rules: list              # base rules (Rule), in reading order of the base text
    notices: list            # operative notices (Notice)
    inert: list              # Inert elements
    policy: Policy
    order: list = field(default_factory=list)  # reading order of operative rule-bearing elements: ("r", rid)/("n", num)
    s3_rows: list | None = None                # S3: base display order of rule ids (ORDER rank before notices)

    def copy(self):
        import copy as _c
        return _c.deepcopy(self)
