"""GEN (general program-gold rows): shared machinery. C2.1 lane L-G, solver A side. CODE ONLY, NO ROWS.

What is here
  - the 20 form ids, k, sizes (G0-lite section 3)
  - GenAllow: the frozen names-only manifest (sha-checked) -> carriers / domains / units / forms allow-list
  - RowNamer: every identifier in a row comes from c21_infra/namespace.py with the TRAINING salt
  - the wording-pool interface (POOL_SPEC, check_pool, TEST-ONLY pool) and the template engine with a render map
  - balanced choosers (least-used with seeded tie break) for letters, classes, traps, wordings
  - number / unit text helpers, an approximate token counter

Nothing here writes a file. Nothing here calls a model, a network or a subprocess.
"""
import hashlib
import json
import math
import os
import random
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

_HERE = os.path.dirname(os.path.abspath(__file__))
C2_BUILD = os.path.dirname(os.path.dirname(_HERE))      # c2_build/c21_fam/GEN -> c2_build
_INFRA = os.path.join(C2_BUILD, "c21_infra")
if _INFRA not in sys.path:
    sys.path.insert(0, _INFRA)

import namespace as _ns  # noqa: E402  (c2_build/c21_infra/namespace.py, TRAINING salt built in)
from pathskip import is_skipped_path  # noqa: E402

DEFAULT_MANIFEST = os.path.join(C2_BUILD, "zed_orch", "c21", "l0", "NAMES_MANIFEST_V1.json")
DEFAULT_MANIFEST_SHA = os.path.join(C2_BUILD, "zed_orch", "c21", "l0", "NAMES_MANIFEST_V1.sha256")

# ------------------------------------------------------------------------------------------------
# Forms (G0-lite section 3). id -> (sub_block, k, train_rows)
# ------------------------------------------------------------------------------------------------
FORMS = {
    "AR-F1": ("ARITH", 4, 1100), "AR-F2": ("ARITH", 2, 300), "AR-F3": ("ARITH", 4, 200),
    "LG-L1": ("LOGIC", 3, 500), "LG-L2": ("LOGIC", 4, 500), "LG-L3": ("LOGIC", 4, 300), "LG-L4": ("LOGIC", 2, 200),
    "CA-C1": ("CAUSAL", 4, 450), "CA-C2": ("CAUSAL", 4, 300), "CA-C3": ("CAUSAL", 4, 250),
    "CA-C4": ("CAUSAL", 4, 150), "CA-C5": ("CAUSAL", 2, 150),
    "TM-T1": ("TEMPORAL", 4, 450), "TM-T2": ("TEMPORAL", 4, 300), "TM-T3": ("TEMPORAL", 4, 250), "TM-T4": ("TEMPORAL", 2, 300),
    "TB-B1": ("TABLE", 4, 500), "TB-B2": ("TABLE", 4, 350), "TB-B3": ("TABLE", 4, 250), "TB-B4": ("TABLE", 2, 200),
}
SUB_BLOCKS = ("ARITH", "LOGIC", "CAUSAL", "TEMPORAL", "TABLE")
SUB_BLOCK_TARGETS = {"ARITH": 1600, "LOGIC": 1500, "CAUSAL": 1300, "TEMPORAL": 1300, "TABLE": 1300}
DEV_PER_SUB_BLOCK = 120
TRAIN_DOMAINS = ["D%02d" % i for i in range(1, 23)]
DEV_DOMAINS = ["D23", "D24"]
N_WORDING_GROUPS = 10
DEV_WORDING_GROUP = 9           # group 9 of every form is held out (10 percent of groups)
MIN_QUESTION_WORDINGS = 56      # >= 50 TRAIN wordings (groups 0-8) + >= 5 dev-group wordings, so no train wording exceeds 2 percent
MIN_TRAIN_WORDINGS = 50
LETTERS = "ABCD"
BINARY_FORMS = tuple(f for f, v in FORMS.items() if v[1] == 2)
BIN_NAMES = ("easy", "mid", "hard")
BIN_SHARE_TARGET = {"easy": 0.20, "mid": 0.55, "hard": 0.25}   # bars: easy <= 0.25, hard <= 0.30

OPTION_TEXTS = {   # fixed option texts of the 3-way and 2-way forms (not wording-pool entries)
    "LG-L1": ["Entailed", "Contradicted", "Undetermined"],
    "LG-L4": ["Yes, it follows", "No, it does not follow"],
    "AR-F2": ["Yes", "No"], "CA-C5": ["Yes", "No"], "TM-T4": ["Yes", "No"], "TB-B4": ["True", "False"],
}
CA_C3_ROLES = ["confounder", "mediator", "collider", "none"]
TM_T3_RELATIONS = ["disjoint with a gap", "touching end to start", "partial overlap", "one contains the other"]


def sub_block_of(form):
    return FORMS[form][0]


def k_of(form):
    return FORMS[form][1]


def dev_rows_for_form(form):
    sb = sub_block_of(form)
    total = SUB_BLOCK_TARGETS[sb]
    return max(2, int(round(FORMS[form][2] / total * DEV_PER_SUB_BLOCK)))


# ------------------------------------------------------------------------------------------------
# Deterministic randomness
# ------------------------------------------------------------------------------------------------
def seed_int(*parts):
    h = hashlib.sha256(json.dumps([str(p) for p in parts], ensure_ascii=True).encode("ascii")).digest()
    return int.from_bytes(h[:8], "big")


def make_rng(*parts):
    return random.Random(seed_int(*parts))


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canon_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


# ------------------------------------------------------------------------------------------------
# Allow-list (frozen names-only manifest). Refuse anything not on it.
# ------------------------------------------------------------------------------------------------
class AllowListError(ValueError):
    pass


class GenAllow:
    """Reads the FROZEN names-only manifest, verifies its sha against the .sha256 file, and exposes GEN's names."""

    def __init__(self, manifest_path=DEFAULT_MANIFEST, sha_path=DEFAULT_MANIFEST_SHA):
        for p in (manifest_path, sha_path):
            if is_skipped_path(p):
                raise AllowListError("allow-list path has an ohs/sealed component")
        raw = open(manifest_path, "rb").read()
        self.sha = hashlib.sha256(raw).hexdigest()
        pinned = open(sha_path, "r").read().split()[0].strip().lower()
        if pinned != self.sha:
            raise AllowListError("manifest sha %s != pinned %s" % (self.sha[:12], pinned[:12]))
        m = json.loads(raw.decode("utf-8"))
        if m.get("frozen") is not True:
            raise AllowListError("manifest is not frozen")
        if "GEN" not in m.get("row_job_families_allowed", []):
            raise AllowListError("GEN is not an allowed row-job family")
        pf = m["per_family_names"]["GEN"]
        self.names = {c: list(pf.get(c, [])) for c in ("policy", "tool", "language", "runner", "carrier")}
        self.carriers = frozenset(self.names["carrier"])
        gd = m["general_domains"]
        self.train_domains = {d["id"]: d["name"] for d in gd["gen_train_domains"]}
        self.dev_domains = {d["id"]: d["name"] for d in gd["gen_dev_only_domains"]}
        self.forms = frozenset(gd["gen_form_ids"])
        self.sub_blocks = frozenset(gd["gen_sub_blocks"])
        self.units = frozenset(u.split(" ")[0] for u in gd["gen_units"])
        self.calendar = tuple(gd["gen_calendar"])
        if self.forms != frozenset(FORMS):
            raise AllowListError("form ids in the manifest differ from FORMS")
        if frozenset(TRAIN_DOMAINS) != frozenset(self.train_domains) or frozenset(DEV_DOMAINS) != frozenset(self.dev_domains):
            raise AllowListError("domain ids in the manifest differ from the generator's constants")
        for cat in ("policy", "tool", "language", "runner"):
            if self.names[cat]:
                raise AllowListError("GEN must have no %s names, manifest lists %r" % (cat, self.names[cat]))

    def check_carrier(self, c):
        if c not in self.carriers:
            raise AllowListError("carrier %r is not on the frozen allow-list" % (c,))
        return c

    def check_domain(self, d):
        if d not in self.train_domains and d not in self.dev_domains:
            raise AllowListError("domain %r is not on the frozen allow-list" % (d,))
        return d

    def check_unit(self, u):
        if u not in self.units:
            raise AllowListError("unit %r is not on the frozen allow-list" % (u,))
        return u

    def check_form(self, f):
        if f not in self.forms:
            raise AllowListError("form %r is not on the frozen allow-list" % (f,))
        return f

    def job_names(self, carriers_used):
        """The 'names' block of a row-job manifest for c21_infra/row_start_guard.py (all five categories declared)."""
        for c in carriers_used:
            self.check_carrier(c)
        return {"policy": [], "tool": [], "language": [], "runner": [], "carrier": sorted(set(carriers_used))}


# ------------------------------------------------------------------------------------------------
# Names: namespace.py, TRAINING salt, one NameSpace per row (seed = row seed)
# ------------------------------------------------------------------------------------------------
# G0-lite section 9 lists these name slots; the manifest maps them to NO namespace.py kind in v1.
# Rule from the manifest: a row job may not fill a slot with a null kind until L-0 adds the kind.
# This module therefore resolves a slot to the kind named after the slot suffix IF namespace.KINDS has it,
# and otherwise (PROVISIONAL mode, unit tests and the dry run ONLY) to the existing 'user' stem kind, tagging
# the key with the slot so the streams differ. A row built in provisional mode carries provisional_names=True
# and `refuse_provisional_for_rows()` raises, so no real row can be written before L-0 adds the kinds.
SLOT_SUFFIX = {"entity": "noun_entity", "variable": "variable", "event": "event", "column": "column",
               "category": "category", "count_noun": "noun_entity", "predicate": "noun_entity", "item": "noun_entity",
               "table": "table"}
PROVISIONAL_KIND = "user"


class ProvisionalNamesError(RuntimeError):
    pass


class RowNamer:
    def __init__(self, row_seed, provisional=True, deny_check=None):
        self.ns = _ns.NameSpace("training", row_seed, deny_check=deny_check)
        self.row_seed = str(row_seed)
        self.provisional = bool(provisional)
        self.used_provisional = False
        self.provenance = []   # [(slot, key, kind_used, name)]

    def _kind(self, slot):
        want = SLOT_SUFFIX[slot]
        if want in _ns.KINDS:
            return want
        if not self.provisional:
            raise ProvisionalNamesError(
                "slot %r needs namespace kind %r which namespace.py v1 lacks (L-0 must add it); row jobs refuse provisional names" % (slot, want))
        self.used_provisional = True
        return PROVISIONAL_KIND

    def name(self, slot, key):
        kind = self._kind(slot)
        nm = self.ns.unique(kind, "%s:%s" % (slot, key))
        self.provenance.append((slot, str(key), kind, nm))
        return nm

    def entity(self, key):
        return self.name("entity", key).capitalize()

    def lower(self, slot, key):
        return self.name(slot, key)

    def fingerprint(self):
        return self.ns.fingerprint()


def verify_provenance(row_seed, provenance, provisional=True):
    """Re-derive every recorded name from (training salt, row seed, slot, key). True iff all agree (gate G-D1)."""
    nm = RowNamer(row_seed, provisional=provisional)
    for slot, key, kind, name in provenance:
        if nm.name(slot, key) != name:
            return False
    return True


def refuse_provisional_for_rows(provisional_flag):
    if provisional_flag:
        raise ProvisionalNamesError("provisional names cannot be used for real rows (namespace.py lacks the GEN kinds)")


# ------------------------------------------------------------------------------------------------
# Numbers and units
# ------------------------------------------------------------------------------------------------
D0 = Decimal(0)
D2 = Decimal("0.01")


def dec(x):
    return x if isinstance(x, Decimal) else Decimal(str(x))


def is_2dp(x):
    return x == x.quantize(D2)


def fmt_num(x):
    """Integer -> '12'; otherwise up to 2 decimals, trailing zeros stripped, always at least one decimal ('12.5')."""
    x = dec(x)
    if x == x.to_integral_value():
        return str(int(x))
    s = format(x.quantize(D2), "f")
    s = s.rstrip("0")
    if s.endswith("."):
        s += "0"
    return s


def norm_num(x):
    """Canonical comparison key for a number."""
    return fmt_num(x)


UNIT_PLURAL = {"gram": "grams", "kilogram": "kilograms", "litre": "litres", "metre": "metres", "kilometre": "kilometres",
               "second": "seconds", "minute": "minutes", "hour": "hours", "day": "days", "week": "weeks", "percent": "percent"}


def unit_text(value, unit, count_noun=None):
    v = dec(value)
    if unit == "count":
        noun = count_noun or "item"
        return "%s %s" % (fmt_num(v), noun if v == 1 else noun + "s")
    word = unit if v == 1 else UNIT_PLURAL[unit]
    return "%s %s" % (fmt_num(v), word)


_TOK = re.compile(r"\d|[A-Za-z]+|[^\sA-Za-z\d]")


def approx_tokens(text):
    """Conservative estimate (digits one token each, words ceil(len/4), punctuation one). L-0's renderer gives real counts."""
    n = 0
    for t in _TOK.findall(text):
        n += math.ceil(len(t) / 4) if t[0].isalpha() else 1
    return n


def word_count(text):
    return len(text.split())


NEGATION_WORDS = ("not", "no", "none", "never", "neither", "nor", "without", "cannot", "n't")
_NEG_RE = re.compile(r"\b(?:not|no|none|never|neither|nor|without|cannot)\b|n't\b", re.I)


# ------------------------------------------------------------------------------------------------
# Balanced choosers
# ------------------------------------------------------------------------------------------------
class Balancer:
    """Least-used choice with a seeded tie break. Used for letters, classes, traps, wordings, bins, carriers."""

    def __init__(self, seed):
        self.rng = make_rng("balancer", seed)
        self.counts = {}

    def key_counts(self, scope):
        return self.counts.setdefault(scope, {})

    def snapshot(self):
        return {k: dict(v) for k, v in self.counts.items()}      # counts only; the rng keeps moving so a retry differs

    def restore(self, snap):
        self.counts = {k: dict(v) for k, v in snap.items()}

    def pick(self, scope, choices, weights=None):
        """Pick from `choices` the one with the smallest count/weight; ties broken by the seeded rng."""
        c = self.key_counts(scope)
        best, best_v = [], None
        for ch in choices:
            w = 1.0 if weights is None else float(weights.get(ch, 1.0))
            v = c.get(ch, 0) / w if w > 0 else 1e18
            if best_v is None or v < best_v - 1e-12:
                best, best_v = [ch], v
            elif abs(v - best_v) <= 1e-12:
                best.append(ch)
        ch = self.rng.choice(best)
        c[ch] = c.get(ch, 0) + 1
        return ch

    def note(self, scope, ch, n=1):
        c = self.key_counts(scope)
        c[ch] = c.get(ch, 0) + n

    def peek(self, scope, ch):
        return self.key_counts(scope).get(ch, 0)


# ------------------------------------------------------------------------------------------------
# Wording pools. POOL_SPEC lists every key, its required slots and its minimum number of entries.
# The pool CONTENT is Claude-authored later (Haiku medium); this module only defines and checks the interface.
# ------------------------------------------------------------------------------------------------
Q_KEYS = {f: "q." + f for f in FORMS}


def _spec(entries):
    return {k: {"slots": tuple(v[0]), "min": v[1]} for k, v in entries.items()}


_POOL_ENTRIES = {
    # question wording per form: >= 56 entries, all required slots present (checked)
    "q.AR-F1": (("final",), MIN_QUESTION_WORDINGS), "q.AR-F2": (("final", "cmp", "thr"), MIN_QUESTION_WORDINGS),
    "q.AR-F3": (("n",), MIN_QUESTION_WORDINGS),
    "q.LG-L1": (("query",), MIN_QUESTION_WORDINGS), "q.LG-L2": ((), MIN_QUESTION_WORDINGS),
    "q.LG-L3": ((), MIN_QUESTION_WORDINGS), "q.LG-L4": (("query",), MIN_QUESTION_WORDINGS),
    "q.CA-C1": (("target", "do_var", "do_val"), MIN_QUESTION_WORDINGS),
    "q.CA-C2": (("target", "do_var", "do_val"), MIN_QUESTION_WORDINGS),
    "q.CA-C3": (("z", "t", "o"), MIN_QUESTION_WORDINGS), "q.CA-C4": (("t", "o"), MIN_QUESTION_WORDINGS),
    "q.CA-C5": (("x", "y", "zset"), MIN_QUESTION_WORDINGS),
    "q.TM-T1": (("start", "offset"), MIN_QUESTION_WORDINGS), "q.TM-T2": (("t1", "t2", "fmt"), MIN_QUESTION_WORDINGS),
    "q.TM-T3": (("iv1", "iv2"), MIN_QUESTION_WORDINGS), "q.TM-T4": ((), MIN_QUESTION_WORDINGS),
    "q.TM-T4.overlap": (("b1", "b2"), MIN_QUESTION_WORDINGS),
    "q.TB-B1": (("agg", "col", "cond"), MIN_QUESTION_WORDINGS), "q.TB-B2": (("rank_phrase",), MIN_QUESTION_WORDINGS),
    "q.TB-B3": (("agg", "col", "cond"), MIN_QUESTION_WORDINGS), "q.TB-B4": (("claim",), MIN_QUESTION_WORDINGS),
    # scene sentences, one list per domain id
    **{"scene." + d: ((), 4) for d in TRAIN_DOMAINS + DEV_DOMAINS},
    # arithmetic fact sentences
    "ar.base": (("name", "qty"), 4), "ar.step.add": (("out", "args"), 4), "ar.step.sub": (("out", "a", "b"), 4),
    "ar.step.mul": (("out", "a", "p"), 4), "ar.step.div": (("out", "a", "p"), 4), "ar.step.pct": (("out", "a", "p"), 4),
    "ar.step.split": (("out", "a", "r1", "r2", "which"), 4), "ar.step.min": (("out", "args"), 4),
    "ar.step.max": (("out", "args"), 4), "ar.step.conv": (("out", "a", "unit"), 4), "ar.step.round": (("out", "a", "rule"), 4),
    "ar.f3.line": (("n", "text"), 6),
    # logic
    "lg.rules_only": ((), 2), "lg.fact.pos": (("e", "pred"), 4), "lg.fact.neg": (("e", "pred"), 4),
    "lg.rel.fact": (("e1", "rel", "e2"), 4), "lg.rule.pos": (("body", "head"), 4), "lg.rule.neg": (("body", "head"), 4),
    "lg.rule.rel": (("body", "head"), 4), "lg.l3.intro": (("items",), 4),
    "lg.l3.c.before": (("a", "b"), 4), "lg.l3.c.imm_before": (("a", "b"), 4), "lg.l3.c.pos_eq": (("a", "pos"), 4),
    "lg.l3.c.pos_neq": (("a", "pos"), 4), "lg.l3.c.not_adjacent": (("a", "b"), 4), "lg.l3.c.adjacent": (("a", "b"), 4),
    # causal
    "ca.intro": (("vars",), 4), "ca.edge": (("a", "b"), 4), "ca.root": (("v", "val"), 4), "ca.fn": (("v", "fn"), 4),
    "ca.fn.noise": (("v", "fn"), 4), "ca.obs": (("v", "val"), 4), "ca.indep": ((), 2), "ca.def_roles": ((), 2),
    "ca.model_closed": ((), 2),
    # temporal
    "tm.calendar_rule": ((), 2), "tm.rule.clamp": ((), 2), "tm.rule.roll": ((), 2), "tm.weekend": (("days",), 2),
    "tm.holidays": (("dates",), 2), "tm.no_holidays": ((), 2), "tm.iv.def": ((), 2),
    "tm.interval": (("name", "start", "end"), 4), "tm.task": (("name", "dur", "after"), 4), "tm.task.noafter": (("name", "dur"), 4),
    "tm.window": (("start", "end"), 2), "tm.parallel": ((), 2), "tm.booking": (("name", "start", "end"), 4), "tm.ts": (("name", "ts"), 4),
    # table
    "tb.intro": (("tables",), 4), "tb.join": (("lk", "rk"), 2), "tb.table_label": (("label",), 2), "tb.rounding": ((), 2),
}
POOL_SPEC = _spec(_POOL_ENTRIES)
_FIELD = re.compile(r"\{([a-z_0-9]+)\}")


class PoolError(ValueError):
    pass


class WordingPool:
    """entries: {key: [template, ...]}. A template uses {slot} fields only. `testonly` pools are refused by row mode."""

    def __init__(self, entries, testonly=False, name="pool"):
        self.entries = {k: list(v) for k, v in entries.items()}
        self.testonly = bool(testonly)
        self.name = name

    def sha(self):
        return sha256_text(canon_json({"entries": self.entries}))

    def keys(self):
        return sorted(self.entries)

    def get(self, key, idx):
        lst = self.entries[key]
        return lst[idx % len(lst)]

    def count(self, key):
        return len(self.entries.get(key, []))

    def groups(self, key):
        """wording index -> group (idx % 10)."""
        return [i % N_WORDING_GROUPS for i in range(self.count(key))]

    def train_ids(self, key):
        return [i for i in range(self.count(key)) if i % N_WORDING_GROUPS != DEV_WORDING_GROUP]

    def dev_ids(self, key):
        return [i for i in range(self.count(key)) if i % N_WORDING_GROUPS == DEV_WORDING_GROUP]


def check_pool(pool, require_keys=None, strict_counts=True):
    """Returns a list of problems (empty = ok). Every template must contain ALL its required slots and no unknown slot."""
    problems = []
    keys = list(POOL_SPEC) if require_keys is None else list(require_keys)
    for k in keys:
        spec = POOL_SPEC[k]
        lst = pool.entries.get(k)
        if lst is None:
            problems.append("missing key %s" % k)
            continue
        if strict_counts and len(lst) < spec["min"]:
            problems.append("key %s has %d entries, needs >= %d" % (k, len(lst), spec["min"]))
        if len(set(lst)) != len(lst):
            problems.append("key %s has duplicate templates" % k)
        for i, t in enumerate(lst):
            fields = set(_FIELD.findall(t))
            miss = set(spec["slots"]) - fields
            extra = fields - set(spec["slots"])
            if miss:
                problems.append("key %s #%d lacks slots %s" % (k, i, sorted(miss)))
            if extra:
                problems.append("key %s #%d has unknown slots %s" % (k, i, sorted(extra)))
        if k.startswith("q.") and strict_counts:
            ntrain = len(pool.train_ids(k))
            if ntrain < MIN_TRAIN_WORDINGS:
                problems.append("key %s has %d TRAIN wordings (groups 0-8), needs >= %d" % (k, ntrain, MIN_TRAIN_WORDINGS))
            if len(pool.dev_ids(k)) < 1:
                problems.append("key %s has no dev-group wording" % k)
    for k in pool.entries:
        if k not in POOL_SPEC:
            problems.append("unknown key %s" % k)
    return problems


def make_testonly_pool(n_question=MIN_QUESTION_WORDINGS):
    """TEST-ONLY wording pool. Plain, original, programmatic phrasing so unit tests and the dry run can run.
    NOT row wording: `testonly=True`, and row mode refuses it. The real pools are authored later by Haiku (medium)."""
    openers = ["Work out", "Determine", "Find", "Decide", "Establish", "Compute", "Settle", "Resolve"]
    closers = ["", " Use only the information above.", " Everything needed is stated.", " Nothing outside the text is needed.",
               " Assume the statements are complete.", " Take the text literally.", " Answer from the text alone."]
    entries = {}
    stems = {
        "q.AR-F1": "{opener} the final quantity {final}.{closer}",
        "q.AR-F2": "{opener} whether {final} is {cmp} {thr}.{closer}",
        "q.AR-F3": "A worked solution with {n} lines is shown. {opener} the first line that contains a mistake.{closer}",
        "q.LG-L1": "{opener} the status of the statement: {query}.{closer}",
        "q.LG-L2": "{opener} which statement must be true.{closer}",
        "q.LG-L3": "{opener} which arrangement satisfies every constraint.{closer}",
        "q.LG-L4": "{opener} whether this conclusion follows: {query}.{closer}",
        "q.CA-C1": "{opener} {target} if {do_var} is set to {do_val} by intervention.{closer}",
        "q.CA-C2": "{opener} what {target} would have been if {do_var} had been {do_val}, everything else in the record being the same.{closer}",
        "q.CA-C3": "{opener} the role of {z} for the pair ({t}, {o}).{closer}",
        "q.CA-C4": "{opener} which set is a valid adjustment set for the effect of {t} on {o}.{closer}",
        "q.CA-C5": "{opener} whether {x} and {y} must be independent given {zset}.{closer}",
        "q.TM-T1": "{opener} the date that is {offset} after {start}.{closer}",
        "q.TM-T2": "{opener} the time from {t1} to {t2}, written as {fmt}.{closer}",
        "q.TM-T3": "{opener} how {iv1} and {iv2} relate.{closer}",
        "q.TM-T4": "{opener} whether the plan is feasible.{closer}",
        "q.TM-T4.overlap": "{opener} whether {b1} and {b2} overlap.{closer}",
        "q.TB-B1": "{opener} the {agg} of {col} over the rows where {cond}.{closer}",
        "q.TB-B2": "{opener} which entry ranks first by {rank_phrase}.{closer}",
        "q.TB-B3": "{opener} the {agg} of {col} over the joined rows where {cond}.{closer}",
        "q.TB-B4": "{opener} whether this claim is correct: {claim}.{closer}",
    }
    combos = [(o, c) for c in closers for o in openers]
    for key, st in stems.items():
        lst = []
        for i in range(n_question):
            o, c = combos[i % len(combos)]
            # keep slot names as fields, fill the two programmatic parts now
            t = st.replace("{opener}", o).replace("{closer}", c)
            if i >= len(combos):
                t = t + " (v%d)" % i
            lst.append(t)
        entries[key] = lst
    for d in TRAIN_DOMAINS + DEV_DOMAINS:
        entries["scene." + d] = ["Scene %s-%d." % (d, i) for i in range(4)]
    e = entries
    e["ar.base"] = ["{name} is {qty}.", "The value of {name} is {qty}.", "Record: {name} equals {qty}.", "{name} stands at {qty}."]
    e["ar.step.add"] = ["{out} is the sum of {args}.", "Add {args} to get {out}.", "{out} equals {args} added together.", "Combine {args}; call the total {out}."]
    e["ar.step.sub"] = ["{out} is {a} minus {b}.", "Take {b} away from {a} to get {out}.", "{out} equals {a} less {b}.", "Subtract {b} from {a}; the result is {out}."]
    e["ar.step.mul"] = ["{out} is {a} repeated {p} times.", "Multiply {a} by {p} to get {out}.", "{out} equals {p} times {a}.", "Take {p} copies of {a}; call it {out}."]
    e["ar.step.div"] = ["{out} is {a} shared equally among {p}.", "Divide {a} by {p} to get {out}.", "{out} equals {a} split into {p} equal parts, one part.", "One of {p} equal parts of {a} is {out}."]
    e["ar.step.pct"] = ["{out} is {p} percent of {a}.", "Take {p} percent of {a}; call it {out}.", "{out} equals {p} percent of {a}.", "{out} is the {p} percent share of {a}."]
    e["ar.step.split"] = ["{a} is split in the ratio {r1} to {r2}; {out} is the {which} share.", "Split {a} in the ratio {r1}:{r2}. {out} is the {which} share.",
                          "{out} is the {which} part when {a} is divided {r1} to {r2}.", "Dividing {a} by the ratio {r1} to {r2}, the {which} part is {out}."]
    e["ar.step.min"] = ["{out} is the smaller of {args}.", "{out} equals the minimum of {args}.", "Take the least of {args}; call it {out}.", "{out} is the lowest among {args}."]
    e["ar.step.max"] = ["{out} is the larger of {args}.", "{out} equals the maximum of {args}.", "Take the greatest of {args}; call it {out}.", "{out} is the highest among {args}."]
    e["ar.step.conv"] = ["{out} is {a} expressed in {unit}.", "Convert {a} to {unit}; call it {out}.", "{out} equals {a} written in {unit}.", "In {unit}, {a} becomes {out}."]
    e["ar.step.round"] = ["{out} is {a} rounded {rule}.", "Round {a} {rule} to get {out}.", "{out} equals {a} after rounding {rule}.", "Rounding {a} {rule} gives {out}."]
    e["ar.f3.line"] = ["Line {n}: {text}", "{n}) {text}", "Step {n}: {text}", "[{n}] {text}", "({n}) {text}", "Line {n} -> {text}"]
    e["lg.rules_only"] = ["Use only the statements given.", "Reason only from the statements below."]
    e["lg.fact.pos"] = ["{e} is a {pred}.", "It is known that {e} is a {pred}.", "{e} counts as a {pred}.", "We are told {e} is a {pred}."]
    e["lg.fact.neg"] = ["{e} is not a {pred}.", "It is known that {e} is not a {pred}.", "{e} does not count as a {pred}.", "We are told {e} is not a {pred}."]
    e["lg.rel.fact"] = ["{e1} {rel} {e2}.", "It is known that {e1} {rel} {e2}.", "We are told {e1} {rel} {e2}.", "Fact: {e1} {rel} {e2}."]
    e["lg.rule.pos"] = ["Every one that {body} is a {head}.", "Anything that {body} is a {head}.", "If something {body}, it is a {head}.", "All that {body} are a {head}."]
    e["lg.rule.neg"] = ["Nothing that {body} is a {head}.", "Anything that {body} is not a {head}.", "If something {body}, it is not a {head}.", "None that {body} is a {head}."]
    e["lg.rule.rel"] = ["For distinct X and Y: if {body}, then {head}.", "Whenever {body}, it follows that {head}.", "For any two different ones X and Y, if {body} then {head}.", "If {body} (X and Y distinct), {head}."]
    e["lg.l3.intro"] = ["Items {items} are placed in positions 1, 2, 3 and so on, one item per position.", "There are positions 1, 2, 3 and so on for the items {items}; each item takes one position.",
                        "The items {items} are lined up, one per position, from position 1.", "Arrange {items} in a row, one per position, positions counted from 1."]
    e["lg.l3.c.before"] = ["{a} is somewhere before {b}.", "{a} comes earlier than {b}.", "{a} is placed ahead of {b}.", "Position of {a} is lower than position of {b}."]
    e["lg.l3.c.imm_before"] = ["{a} is immediately before {b}.", "{a} is directly ahead of {b}, with nothing between.", "{b} comes right after {a}.", "{a} sits just before {b}."]
    e["lg.l3.c.pos_eq"] = ["{a} is in position {pos}.", "{a} takes position {pos}.", "Position {pos} holds {a}.", "{a} is placed at position {pos}."]
    e["lg.l3.c.pos_neq"] = ["{a} is not in position {pos}.", "{a} does not take position {pos}.", "Position {pos} does not hold {a}.", "{a} is kept out of position {pos}."]
    e["lg.l3.c.not_adjacent"] = ["{a} and {b} are not next to each other.", "{a} is not adjacent to {b}.", "There is at least one item between {a} and {b}.", "{a} and {b} do not sit side by side."]
    e["lg.l3.c.adjacent"] = ["{a} and {b} are next to each other.", "{a} is adjacent to {b}.", "{a} and {b} sit side by side.", "No item lies between {a} and {b}."]
    e["ca.intro"] = ["A system has the variables {vars}. Each takes a whole value from 0 to 7.", "The variables {vars} each take a whole value from 0 to 7.", "Consider variables {vars}, each a whole number from 0 to 7.", "In a model with {vars}, every variable is a whole number from 0 to 7."]
    e["ca.edge"] = ["{a} directly influences {b}.", "There is a direct arrow from {a} to {b}.", "{a} is a direct cause of {b}.", "{b} depends directly on {a}."]
    e["ca.root"] = ["{v} is set to {val} from outside.", "The outside input of {v} is {val}.", "{v} receives the value {val} from outside.", "{v} is given as {val}."]
    e["ca.fn"] = ["{v} is {fn}.", "The value of {v} is {fn}.", "{v} is computed as {fn}.", "Rule: {v} = {fn}."]
    e["ca.fn.noise"] = ["{v} is {fn}, plus its own hidden input, all taken mod 8.", "{v} = ({fn} + its own hidden input) mod 8.", "The value of {v} is {fn} plus its own hidden input, mod 8.", "{v} is {fn} plus a hidden input of its own, mod 8."]
    e["ca.obs"] = ["Recorded: {v} was {val}.", "In the record, {v} was {val}.", "Observed: {v} = {val}.", "{v} was seen to be {val}."]
    e["ca.indep"] = ["Every variable with no arrow into it is an independent random input; the question is about the stated arrows only.", "Variables without incoming arrows are independent random inputs, and only the stated arrows matter."]
    e["ca.def_roles"] = ["Z is a confounder of (T, O) if Z points directly to both T and O; a mediator if T points directly to Z and Z points directly to O; a collider if both T and O point directly to Z; otherwise none.",
                         "Roles are defined by direct arrows: confounder (Z -> T and Z -> O), mediator (T -> Z and Z -> O), collider (T -> Z and O -> Z), none otherwise."]
    e["ca.model_closed"] = ["The rules and values given are the whole model.", "Nothing besides the stated rules and values is part of the model."]
    e["tm.calendar_rule"] = ["Use the proleptic Gregorian calendar and a 24-hour clock with no daylight-saving changes.", "Dates follow the Gregorian calendar extended to all years; the clock is 24-hour and has no daylight-saving shifts."]
    e["tm.rule.clamp"] = ["Adding months keeps the day number, or uses the last day of the month if that day does not exist.", "A month step keeps the day of month, except it uses the month's last day when the day is missing."]
    e["tm.rule.roll"] = ["Adding months keeps the day number; days past the end of the month roll into the next month.", "A month step keeps the day of month, and any days beyond the month's end spill into the following month."]
    e["tm.weekend"] = ["Weekend days are {days}.", "The days off each week are {days}."]
    e["tm.holidays"] = ["Holidays are {dates}.", "These dates are holidays: {dates}."]
    e["tm.no_holidays"] = ["There are no holidays.", "No date is a holiday."]
    e["tm.iv.def"] = ["Each interval includes its start and excludes its end.", "An interval runs from its start up to but not including its end."]
    e["tm.interval"] = ["{name} runs from {start} to {end}.", "{name}: {start} until {end}.", "The span {name} starts at {start} and ends at {end}.", "{name} begins {start} and finishes {end}."]
    e["tm.task"] = ["Task {name} takes {dur} and starts only after {after} are done.", "{name} needs {dur} and waits for {after}.", "Task {name}: {dur}, after {after}.", "{name} lasts {dur}; it cannot start before {after} finish."]
    e["tm.task.noafter"] = ["Task {name} takes {dur} and can start at once.", "{name} needs {dur} and has no prerequisite.", "Task {name}: {dur}, no prerequisites.", "{name} lasts {dur}; it can start as soon as work begins."]
    e["tm.parallel"] = ["Tasks that are ready may run at the same time, with no limit on how many.", "There are enough workers for every task that is ready to run at once."]
    e["tm.window"] = ["Work begins at {start} and everything must be finished by {end}.", "The window opens at {start} and closes at {end}; all work must end by then."]
    e["tm.booking"] = ["Booking {name} is from {start} to {end}.", "{name}: {start} to {end}.", "The booking {name} starts {start} and ends {end}.", "{name} holds the slot from {start} until {end}."]
    e["tm.ts"] = ["{name} is {ts}.", "{name} happens at {ts}.", "The time of {name} is {ts}.", "{name}: {ts}."]
    e["tb.join"] = ["The tables are joined where {lk} in the first table equals {rk} in the second.", "Join the two tables on {lk} = {rk}."]
    e["tb.intro"] = ["{tables}", "Data:\n{tables}", "Table data follows.\n{tables}", "Consider the data below.\n{tables}"]
    e["tb.table_label"] = ["Table {label}:", "{label}:", "Table named {label}:"]
    e["tb.rounding"] = ["Round the result to 2 decimal places, half up.", "Give the result to 2 decimal places, rounding half up."]
    return WordingPool(entries, testonly=True, name="TESTONLY")


# ------------------------------------------------------------------------------------------------
# Template engine with a render map
# ------------------------------------------------------------------------------------------------
class Doc:
    """Builds a stem from template pieces and records spans: [{slot, value, start, end, role, kind}]."""

    def __init__(self):
        self.parts = []
        self.spans = []
        self.pos = 0

    def raw(self, text):
        self.parts.append(text)
        self.pos += len(text)

    def sep(self, s=" "):
        if self.pos:
            self.raw(s)

    def sentence(self, template, values, whole=None):
        """values: {slot: (text, role, kind)} or {slot: text}. Role None = no span of interest recorded as span anyway."""
        out = []
        cur = 0
        for m in _FIELD.finditer(template):
            lit = template[cur:m.start()]
            out.append(lit)
            cur_pos = self.pos + sum(len(x) for x in out)
            slot = m.group(1)
            if slot not in values:
                raise PoolError("slot %r not supplied for template %r" % (slot, template))
            v = values[slot]
            text, role, kind = (v, None, None) if isinstance(v, str) else v
            self.spans.append({"slot": slot, "value": text, "start": cur_pos, "end": cur_pos + len(text), "role": role, "kind": kind})
            out.append(text)
            cur = m.end()
        out.append(template[cur:])
        s = "".join(out)
        if whole:
            self.spans.append({"slot": "_sentence", "value": s, "start": self.pos, "end": self.pos + len(s), "role": whole[0], "kind": whole[1]})
        self.parts.append(s)
        self.pos += len(s)
        return s

    def text(self):
        return "".join(self.parts)


def decision_spans_of(text, spans):
    """Spans with a role (number/entity) plus every negation word found in the stem text. Roles per G10 (no AUTHORITY in GEN)."""
    out = []
    for s in spans:
        if s["role"]:
            out.append({"text": s["value"], "start": s["start"], "end": s["end"], "role": s["role"], "kind": s["kind"]})
    for m in _NEG_RE.finditer(text):
        out.append({"text": m.group(0), "start": m.start(), "end": m.end(), "role": "negation", "kind": "negation"})
    out.sort(key=lambda d: (d["start"], d["end"]))
    return out


def slot_check(text, spans):
    """Self-check of the render map: every recorded span text sits at its recorded offsets."""
    for s in spans:
        if text[s["start"]:s["end"]] != s["value"]:
            return False
    return True


def join_names(names):
    names = list(names)
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


# ------------------------------------------------------------------------------------------------
# Carriers for fact blocks (names from the frozen allow-list) and a helper for typed class distractors
# ------------------------------------------------------------------------------------------------
TEXT_CARRIERS = {
    "ARITH": ["TXT-PROSE", "TXT-BULLET", "TXT-NUMBERED", "TXT-LEDGER"],
    "LOGIC": ["TXT-PROSE", "TXT-BULLET", "TXT-NUMBERED"],
    "CAUSAL": ["TXT-PROSE", "TXT-BULLET", "TXT-NUMBERED"],
    "TEMPORAL": ["TXT-PROSE", "TXT-BULLET", "TXT-NUMBERED", "TXT-TIMELINE"],
}
TABLE_CARRIERS = ["TBL-PIPE", "TBL-CSV", "TBL-TSV", "TBL-KV", "TBL-JSON"]


def item_sep(doc, carrier, i):
    """Separator before the i-th fact item (0-based) of a fact block."""
    if carrier == "TXT-PROSE":
        doc.sep(" ")
    elif carrier == "TXT-BULLET":
        doc.sep("\n- ")
    elif carrier == "TXT-NUMBERED":
        doc.sep("\n%d. " % (i + 1))
    else:                       # TXT-TIMELINE, TXT-LEDGER, tables: one item per line
        doc.sep("\n")


def end_block(doc, carrier):
    doc.sep(" " if carrier == "TXT-PROSE" else "\n")


def assign_trap_types(wrong_values, flawed_outputs, balancer, scope):
    """wrong_values: list of values (classes) that appear as wrong options.
    flawed_outputs: {flaw_name: output_value}. Returns a list of trap_type strings, one per wrong value:
    the least-used flaw that outputs exactly that value, else 'unmodelled'."""
    out = []
    for w in wrong_values:
        flaws = [f for f, o in flawed_outputs.items() if o == w]
        out.append(balancer.pick(scope, flaws) if flaws else "unmodelled")
    return out


def dp_class(v):
    """Number of decimal places (0, 1, 2) of a Decimal; options are drawn with the same class as the correct value when possible,
    so 'the exact-looking value is right' is not a cue."""
    v = dec(v)
    if v == v.to_integral_value():
        return 0
    return 1 if (v * 10) == (v * 10).to_integral_value() else 2


USE_CRANK = False     # balance the correct value's distance-from-mean rank as well as its value rank (see pick_options_ranked)
_ISO = re.compile(r"^(\d{4})-(\d\d)-(\d\d)$")


def _as_number(x):
    """A value on a number line for the closeness-to-mean statistic: numbers, ISO dates (day ordinal); None for anything else."""
    if isinstance(x, (int, float, Decimal)):
        return float(x)
    if isinstance(x, str):
        m = _ISO.match(x)
        if m:
            import datetime as _dt
            return float(_dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).toordinal())
        try:
            return float(x)
        except ValueError:
            return None
    return None


def pick_options_ranked(correct, flaws, k, rng, balancer, scope, key=lambda v: v, tries=120, sim=None, jitter=None):
    """Choose k-1 wrong values of pairwise distinct trap types from flaws = {type: [values]} (values comparable through `key`).
    Two statistics of the correct value are balanced across rows by least-used counters, so no position of the correct value is a cue:
      rank   its place among the k options by value (0 = smallest): the 'median value' / 'largest' / 'smallest' shortcuts;
      crank  its place by distance from the option mean (0 = closest): near-miss distractors surround the truth, so without this the
             correct option is the one nearest the mean (skeptic fix 18 Oct; option-only probe G-S1 reached 80 percent on TM-T1).
    jitter: optional callable (value, rng) -> value or None. In the SECOND half of the attempts a wrong value may also appear as a COMPOUND slip
      (the base slip plus a small independent miscount on the form's own lattice, trap type '<type>+slip'). Every real error model errs by a fixed
      amount, so the wrong options share residues and offsets with the correct value and with each other in a way that singles the correct one
      out (skeptic finding 18 Oct); an independent slip per wrong option breaks that regularity. The slip lattice is the form's own (days for
      dates, five-minute steps for durations), so the correct value is not the only one on a lattice.
    Returns [(value, trap_type)] or None."""
    types = [t for t, v in flaws.items() if v]
    if len(types) < k - 1:
        return None
    base_flaws = flaws
    want = balancer.pick(scope + ".rank", list(range(k)))
    want_c = balancer.pick(scope + ".crank", list(range(k)))
    best = None
    snap = balancer.snapshot()
    for attempt in range(tries):
        balancer.restore(snap)
        flaws = base_flaws
        if jitter is not None and attempt >= tries // 2:
            flaws = {t: list(v) for t, v in base_flaws.items()}
            for t, vs in base_flaws.items():
                js = [m for m in (jitter(v, rng) for v in vs) if m is not None and key(m) != key(correct)]
                if js:
                    flaws[t + "+slip"] = js
        types = [t for t, v in flaws.items() if v]
        chosen, used, avail = [], {key(correct)}, list(types)
        strict = sim is not None and attempt < tries // 2
        while len(chosen) < k - 1 and avail:
            t = balancer.pick(scope, avail)
            avail.remove(t)
            vals = [v for v in flaws[t] if key(v) not in used and (not strict or sim(v) == sim(correct))]
            if not vals:
                balancer.key_counts(scope)[t] -= 1
                continue
            v = rng.choice(vals)
            used.add(key(v))
            chosen.append((v, t))
        if len(chosen) < k - 1:
            continue
        rank = sum(1 for v, _ in chosen if key(v) < key(correct))
        ks = [_as_number(key(v)) for v, _ in chosen] + [_as_number(key(correct))]
        if None in ks:
            crank = want_c                               # values with no number line (class labels): nothing to balance
        else:
            mean = sum(ks) / len(ks)
            dc = abs(ks[-1] - mean)
            crank = sum(1 for x in ks[:-1] if abs(x - mean) < dc - 1e-12)
        score = int(rank == want) + (int(crank == want_c) if USE_CRANK else 1)
        if best is None or score > best[0]:
            best = (score, chosen, balancer.snapshot())
        if score == 2:
            return chosen
    if best is None:
        return None
    balancer.restore(best[2])
    return best[1]



def date_jitter(v, rng):
    """Compound slip for ISO dates: the value moved by 1-7 days either way."""
    import datetime as _dt
    try:
        return (_dt.date.fromisoformat(v) + _dt.timedelta(days=rng.choice([-7, -3, -2, -1, 1, 2, 3, 7]))).isoformat()
    except (ValueError, OverflowError):
        return None


def minutes_jitter(v, rng):
    """Compound slip for durations in minutes (all GEN durations are multiples of 5): moved by 5-45 minutes or 1-2 hours either way, kept positive."""
    m = v + rng.choice([-120, -60, -45, -30, -20, -15, -10, -5, 5, 10, 15, 20, 30, 45, 60, 120])
    return m if m > 0 else None
