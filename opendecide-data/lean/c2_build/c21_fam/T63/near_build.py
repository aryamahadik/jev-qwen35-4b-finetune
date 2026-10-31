"""T63 NEAR spec builder: squat mutations (NM-T1..NM-T7), snapshot groups (pair A, flip pair, T8 flip pair, singles), ladder
mechanism flags. Every name comes from the seeded namespace (TRAINING salt); the builder checks that the label computed by SOLVER A
equals the label the cell intends (a mismatch is a Reject: a builder defect or an accidental relation, never kept)."""
import re

from LP_COMMON import plan as plan_mod
from LP_COMMON.ns import Names

from . import config as C
from . import near as N

_VALID = re.compile(r"^[a-z0-9]+(?:[-_.][a-z0-9]+)*$")
_ALPHA = "bdfgklmnprstvzaeiou"


class Reject(Exception):
    """The cell cannot be realised with this seed (the pipeline redraws with a new seed)."""


def valid_name(s):
    bare = s.split("/", 1)[1] if "/" in s else s
    scope_ok = True if "/" not in s else bool(_VALID.match(s.split("/", 1)[0]))
    return bool(_VALID.match(bare)) and scope_ok and len(s) <= 40


def mutate(name, op, rng, scope_factory=None):
    """Return p with p = op(name) (rel(p, name) contains `op`) or None when the op does not apply."""
    n = len(name)
    idx_alpha = [i for i, ch in enumerate(name) if ch.isalnum()]
    if op == "NM-T1":
        cands = [name[:i] + name[i + 1:] for i in idx_alpha]
    elif op == "NM-T2":
        cands = [name[:i] + ch + name[i:] for i in range(1, n) for ch in rng.sample(_ALPHA, 4) if name[i - 1].isalnum() and name[i].isalnum()]
    elif op == "NM-T3":
        cands = []
        for i in idx_alpha:
            for ch in sorted(N.KEYBOARD.get(name[i], ())):
                cands.append(name[:i] + ch + name[i + 1:])
    elif op == "NM-T4":
        cands = [name[:i] + name[i + 1] + name[i] + name[i + 2:] for i in range(n - 1)
                 if name[i].isalnum() and name[i + 1].isalnum() and name[i] != name[i + 1]]
    elif op == "NM-T5":
        seps = [i for i, ch in enumerate(name) if ch in N.SEPS]
        cands = []
        for i in seps:
            for rep in ("-", "_", ".", ""):
                if rep != name[i]:
                    cands.append(name[:i] + rep + name[i + 1:])
    elif op == "NM-T6":
        cands = []
        for a, b in N.LOOKALIKES:
            k = name.find(a)
            while k >= 0:
                cands.append(name[:k] + b + name[k + len(a):])
                k = name.find(a, k + 1)
    elif op == "NM-T7":
        if "/" in name:
            cands = [name.split("/", 1)[1]]
        else:
            cands = ["%s/%s" % (scope_factory(), name)] if scope_factory else []
    else:
        return None
    cands = [c for c in dict.fromkeys(cands) if c != name and valid_name(c) and op in N.near_relations(c, name)]
    return rng.choice(cands) if cands else None


def pair_names(snap, rng, op):
    """(legit, squat) names of a near pair. The squat is op(legit) in a random half of the cells and the legit side is the mutated-looking name in the
    other half (the union of NM-T1..T7 is symmetric), so the name shape of the QUERIED package carries no label (K4)."""
    base = snap.package()
    other = mutate(base, op, rng, scope_factory=snap.scope)
    if other is None:
        raise Reject("op not applicable")
    if rng.random() < 0.5:
        return base, other
    if not N.near_relations(base, other):
        raise Reject("asymmetric relation")
    return other, base


# ---- entries and snapshots ------------------------------------------------------------------------------------------------------
def entry(name, registry, publisher, age, dl, fork_of=None):
    return {"name": name, "registry": registry, "publisher": publisher, "age": age, "dl": dl, "fork_of": fork_of}


class Snap(object):
    """Name factory for one snapshot group."""

    def __init__(self, ctx, gid, seed):
        self.names = Names("T63", "%s/%s" % (ctx.seed, seed), deny_check=ctx.deny_check)
        self.k = 0
        self.used = set()

    def _next(self, slot, tag, bare=False):
        for _ in range(40):
            self.k += 1
            nm = self.names.get(slot, "%s%d" % (tag, self.k))
            if bare:
                nm = nm.lower().replace(" ", "")
            if nm not in self.used:
                self.used.add(nm)
                return nm
        raise Reject("name pool")

    def package(self):
        return self._next("ns.package", "pkg")

    def handle(self):
        return self._next("ns.handle", "h")

    def host(self):
        return self._next("ns.registry_host", "host")

    def scope(self):
        return self._next("ns.handle", "scope")


def _registries(snap, eco):
    ids = ["R1", "R2", "R3"]
    return [{"id": rid, "host": snap.host(), "eco": eco} for rid in ids]


def _card(snap, regs, rng, reserved=(), internal=None, order=None, own_org=None):
    return {"display": snap.names.get("ns.policy_card", "card"), "reserved": list(reserved), "internal_registry": internal,
            "resolve_order": list(order) if order else rng.sample([r["id"] for r in regs], 3), "own_org": own_org or snap.handle()}


def _no_accidental(entries, protected):
    """Fillers must not be near any other entry (an accidental relation would change the label)."""
    for i, a in enumerate(entries):
        for b in entries[i + 1:]:
            if a["registry"] == b["registry"] and (N.near_relations(a["name"], b["name"]) or N.near_relations(b["name"], a["name"])):
                if (a["name"], b["name"]) not in protected and (b["name"], a["name"]) not in protected:
                    raise Reject("accidental relation")


def _fillers(snap, rng, regs, qreg, n_same, n_other, avoid_publishers=()):
    out = []
    ages = list(C.AGE)
    for _ in range(n_same):
        out.append(entry(snap.package(), qreg, snap.handle(), rng.choice(ages), rng.choice(C.DL)))
    for _ in range(n_other):
        rid = rng.choice([r["id"] for r in regs if r["id"] != qreg])
        out.append(entry(snap.package(), rid, snap.handle(), rng.choice(ages), rng.choice(C.DL)))
    return out


def _decorate(snap, rng, spec, mech, p, q):
    """Label-irrelevant difficulty decorations (M-SIB, M-XREG); sets spec['mech'] flags. LOW/HIGH per G0-lite section 5."""
    regs = spec["registries"]
    other = [r["id"] for r in regs if r["id"] != p["registry"]]
    sib = mech.get("sib")
    if sib == "low":      # P's publisher also publishes an unrelated entry (a known publisher)
        spec["entries"].append(entry(snap.package(), p["registry"], p["publisher"], rng.choice(C.AGE), rng.choice(C.DL)))
    elif sib == "high":   # a fork edge links P to an unrelated entry
        x = entry(snap.package(), p["registry"], snap.handle(), rng.choice(("A1", "A2", "A3")), rng.choice(C.DL))
        spec["entries"].append(x)
        p["fork_of"] = x["name"]
    xr = mech.get("xreg")
    if xr == "low":       # Q's name is mirrored in another registry by Q's publisher
        spec["entries"].append(entry(q["name"], rng.choice(other), q["publisher"], q["age"], q["dl"]))
    elif xr == "high":    # P's name is also on another registry under a different publisher
        spec["entries"].append(entry(p["name"], rng.choice(other), snap.handle(), rng.choice(("A0", "A1")), rng.choice(C.DL)))
    spec["mech"] = {"edit": mech.get("edit"), "sib": sib, "xreg": xr}


def _finish(spec, intended):
    if len(spec["entries"]) > C.MAX_TABLE_ENTRIES:
        raise Reject("table too long")
    got = N.gold_label(spec)
    if got != intended:
        raise Reject("label %s != intended %s (%s)" % (got, intended, spec.get("no_kind") or spec.get("relation")))
    m = spec["mech"]
    low = sum(1 for k in ("edit", "sib", "xreg") if m.get(k) == "low")
    high = sum(1 for k in ("edit", "sib", "xreg") if m.get(k) == "high")
    spec["level"] = plan_mod.ladder_level(low, high)
    spec["label"] = intended
    return spec


EDIT_MECH = {"NM-T1": "low", "NM-T2": "low", "NM-T6": "high", "NM-T7": "high"}


def _age_below(age, rng):
    lower = [a for a in C.AGE if N.AGE_ORDER[a] < N.AGE_ORDER[age]]
    return rng.choice(lower) if lower else None


# ---- non-T8 groups --------------------------------------------------------------------------------------------------------------
def _base(ctx, g, eco, own_org_shown=True):
    snap = Snap(ctx, g["gid"], g["seed"])
    rng = ctx.rng("near", g["seed"])
    regs = _registries(snap, eco)
    return snap, rng, regs


def build_yes_flip(ctx, g):
    """YES squat row and (optionally) its one-field-flip NO twin. cell: op, a_p, d_p, flip, mech, pair (bool)."""
    c = g["cell"]
    snap, rng, regs = _base(ctx, g, c["eco"])
    qreg = rng.choice(["R1", "R2", "R3"])
    qname, pname = pair_names(snap, rng, c["op"])
    pub_q, pub_p = snap.handle(), snap.handle()
    # Q established: age above a_p, at least A2, downloads D2
    a_p = c["a_p"]
    q_ages = [a for a in C.ESTABLISHED if N.AGE_ORDER[a] > N.AGE_ORDER[a_p]]
    if not q_ages:
        raise Reject("no older established age")
    Q = entry(qname, qreg, pub_q, rng.choice(q_ages), "D2")
    P = entry(pname, qreg, pub_p, a_p, c["d_p"])
    entries = [Q, P] + _fillers(snap, rng, regs, qreg, rng.randint(2, 6), rng.randint(0, 2))
    _no_accidental(entries, {(pname, qname)})
    card = _card(snap, regs, rng, reserved=[snap.package() for _ in range(rng.randint(0, 2))],
                 internal=rng.choice(["R1", "R2", "R3", None]))
    spec = {"head": "NEAR", "registries": regs, "entries": entries, "card": card,
            "query": {"name": pname, "registry": qreg, "explicit": rng.random() < 0.5},
            "relation": c["op"], "no_kind": None}
    mech = dict(c["mech"])
    mech["edit"] = EDIT_MECH.get(c["op"])
    _decorate(snap, rng, spec, mech, P, Q)
    yes = _finish(spec, "YES")
    out = [yes]
    if c.get("flip"):
        no = _flip(snap, rng, yes, c["flip"])
        out.append(no)
    return out


def _flip(snap, rng, yes, flip):
    import copy
    s = copy.deepcopy(yes)
    q = s["query"]
    P = next(e for e in s["entries"] if e["name"] == q["name"] and e["registry"] == q["registry"])
    Qn = next(e for e in s["entries"] if e["registry"] == q["registry"] and e is not P and N.near_relations(P["name"], e["name"])
              and N.established(e))
    if flip == "pub":
        P["publisher"] = Qn["publisher"]
        s["no_kind"] = "NM-R2"
        s["flip_field"] = "publisher"
    elif flip == "fork":
        P["fork_of"] = Qn["name"]
        s["no_kind"] = "NM-R2"
        s["flip_field"] = "fork_of"
    elif flip == "age":
        if not (N.established(P) and P["age"] in C.ESTABLISHED):
            raise Reject("age flip needs an established P")
        Qn["age"] = P["age"]
        s["no_kind"] = "NM-R3"
        s["flip_field"] = "age"
    else:
        raise Reject("unknown flip")
    s["relation"] = None
    # the mechanism flags stay (decorations unchanged); M-SIB high via fork flip counts for the NO row
    if flip == "fork":
        s["mech"] = dict(s["mech"], sib="high") if s["mech"].get("sib") in (None, "low") else s["mech"]
    return _finish(s, "NO")


def build_pair_a(ctx, g):
    """Pair A: one snapshot, two queries: the squat (YES) and the older legit package (NO, NM-R1). The queried legit package is NOT
    required to be established; it only has to be older than the squat."""
    c = g["cell"]
    snap, rng, regs = _base(ctx, g, c["eco"])
    qreg = rng.choice(["R1", "R2", "R3"])
    legit_name, sname = pair_names(snap, rng, c["op"])
    pub_l, pub_s = snap.handle(), snap.handle()
    a_leg = c["a_p"]                                   # the queried NO package: age class a_p (feasible: >= A1)
    a_sq = c.get("a_sq") or _age_below(a_leg, rng)
    if a_sq is None or N.AGE_ORDER[a_sq] >= N.AGE_ORDER[a_leg]:
        raise Reject("no younger squat age")
    # R1 legit side: the squat's partner must make the squat YES (so the squat needs an ESTABLISHED older Q): use a THIRD entry E
    # established and older than the squat which the squat also resembles? Simpler and exact: the legit package IS Q, so it must be
    # established; its age must be >= A2.
    if a_leg not in C.ESTABLISHED:
        raise Reject("pair A needs an established legit side")
    LEG = entry(legit_name, qreg, pub_l, a_leg, "D2")
    SQ = entry(sname, qreg, pub_s, a_sq, c["d_p"])
    entries = [LEG, SQ] + _fillers(snap, rng, regs, qreg, rng.randint(2, 6), rng.randint(0, 2))
    _no_accidental(entries, {(sname, legit_name)})
    card = _card(snap, regs, rng, reserved=[snap.package() for _ in range(rng.randint(0, 2))], internal=rng.choice(["R1", "R2", "R3", None]))
    base = {"head": "NEAR", "registries": regs, "entries": entries, "card": card, "no_kind": None}
    mech = dict(c["mech"])
    mech["edit"] = EDIT_MECH.get(c["op"])
    import copy
    y = copy.deepcopy(base)
    y["query"] = {"name": sname, "registry": qreg, "explicit": rng.random() < 0.5}
    y["relation"] = c["op"]
    _decorate(snap, rng, y, mech, next(e for e in y["entries"] if e["name"] == sname), next(e for e in y["entries"] if e["name"] == legit_name))
    n = copy.deepcopy(y)
    n["query"] = {"name": legit_name, "registry": qreg, "explicit": y["query"]["explicit"]}
    n["relation"] = None
    n["no_kind"] = "NM-R1"
    return [_finish(y, "YES"), _finish(n, "NO")]


def build_single_no(ctx, g):
    """Single NO rows: NM-R2 (sibling), NM-R3 (two long-lived), NM-R4 (unrelated)."""
    c = g["cell"]
    snap, rng, regs = _base(ctx, g, c["eco"])
    kind = c["no_kind"]
    qreg = rng.choice(["R1", "R2", "R3"])
    qname, pname = None, None
    pub_q, pub_p = snap.handle(), snap.handle()
    a_p, d_p = c["a_p"], c["d_p"]
    card = _card(snap, regs, rng, reserved=[snap.package() for _ in range(rng.randint(0, 2))], internal=rng.choice(["R1", "R2", "R3", None]))
    if kind == "NM-R4":
        pn = pair_names(snap, rng, rng.choice(("NM-T1", "NM-T2", "NM-T3", "NM-T4", "NM-T5", "NM-T6", "NM-T7")))[rng.randrange(2)]
        P = entry(pn, qreg, pub_p, a_p, d_p)
        entries = [P] + _fillers(snap, rng, regs, qreg, rng.randint(3, 7), rng.randint(0, 2))
        _no_accidental(entries, set())
        spec = {"head": "NEAR", "registries": regs, "entries": entries, "card": card,
                "query": {"name": P["name"], "registry": qreg, "explicit": rng.random() < 0.5}, "relation": None, "no_kind": kind}
        _decorate(snap, rng, spec, {"edit": None, **c["mech"]}, P, P)
        return [_finish(spec, "NO")]
    if kind == "NM-R3":
        if a_p not in C.ESTABLISHED or d_p != "D2":
            raise Reject("R3 needs an established P")
        a_q = "A2" if a_p == "A2" else rng.choice(("A2", "A3"))
        qname, pname = pair_names(snap, rng, c["op"])
        Q = entry(qname, qreg, pub_q, a_q, "D2")
    else:                                              # NM-R2: Q established and older than P; P linked to Q
        q_ages = [a for a in C.ESTABLISHED if N.AGE_ORDER[a] > N.AGE_ORDER[a_p]]
        if not q_ages:
            raise Reject("no older established age")
        qname, pname = pair_names(snap, rng, c["op"])
        Q = entry(qname, qreg, pub_q, rng.choice(q_ages), "D2")
    op = c["op"]
    P = entry(pname, qreg, pub_p, a_p, d_p)
    if kind == "NM-R2":
        if c.get("sib") == "high":
            P["fork_of"] = qname
        else:
            P["publisher"] = pub_q
    entries = [Q, P] + _fillers(snap, rng, regs, qreg, rng.randint(2, 6), rng.randint(0, 2))
    _no_accidental(entries, {(pname, qname)})
    spec = {"head": "NEAR", "registries": regs, "entries": entries, "card": card,
            "query": {"name": pname, "registry": qreg, "explicit": rng.random() < 0.5}, "relation": None, "no_kind": kind}
    mech = dict(c["mech"])
    mech["edit"] = EDIT_MECH.get(op)
    r2_sib = None
    if kind == "NM-R2":                       # the sibling relation IS the M-SIB mechanism; no extra sib decoration (it would move fork_of)
        r2_sib = "high" if c.get("sib") == "high" else "low"
        mech["sib"] = None
    _decorate(snap, rng, spec, mech, P, Q)
    if r2_sib:
        spec["mech"]["sib"] = r2_sib
    return [_finish(spec, "NO")]


def build_single_yes(ctx, g):
    c = dict(g["cell"], flip=None)
    return build_yes_flip(ctx, dict(g, cell=c))[:1]


# ---- T8 groups --------------------------------------------------------------------------------------------------------------------
def _t8_base(ctx, g):
    c = g["cell"]
    snap, rng, regs = _base(ctx, g, c["eco"])
    ids = [r["id"] for r in regs]
    rng.shuffle(ids)
    internal, pub, third = ids
    pname = snap.package()
    own = snap.handle()
    other_pub = snap.handle()
    explicit = bool(c.get("explicit"))
    high = c["mech"].get("xreg") == "high"
    qreg = third if high else pub
    entries = [entry(pname, internal, own, "A2" if rng.random() < 0.9 else "A3", "D2"), entry(pname, qreg, other_pub, c["a_p"], c["d_p"])]
    if high:                                           # the name also lives on a second public registry that bare installs hit first
        entries.append(entry(pname, pub, snap.handle(), rng.choice(("A0", "A1")), rng.choice(C.DL)))
        order = [pub, qreg, internal]
        explicit = True                                # YES only by naming the registry explicitly
    else:
        order = [qreg, internal, third] if rng.random() < 0.5 else [qreg, third, internal]
    reserved = [pname] + [snap.package() for _ in range(rng.randint(0, 2))]
    rng.shuffle(reserved)
    entries += _fillers(snap, rng, regs, qreg, rng.randint(1, 4), rng.randint(0, 2))
    _no_accidental(entries, set())
    card = {"display": snap.names.get("ns.policy_card", "card"), "reserved": reserved, "internal_registry": internal,
            "resolve_order": order, "own_org": own}
    spec = {"head": "NEAR", "registries": regs, "entries": entries, "card": card,
            "query": {"name": pname, "registry": qreg, "explicit": explicit}, "relation": "NM-T8", "no_kind": None}
    xr = "high" if high else ("low" if c["mech"].get("xreg") == "low" else None)
    sib = c["mech"].get("sib")
    p = next(e for e in entries if e["name"] == pname and e["registry"] == qreg)
    qd = entries[0]
    if sib == "low":
        spec["entries"].append(entry(snap.package(), qreg, p["publisher"], rng.choice(C.AGE), rng.choice(C.DL)))
    elif sib == "high":
        x = entry(snap.package(), qreg, snap.handle(), "A2", rng.choice(C.DL))
        spec["entries"].append(x)
        p["fork_of"] = x["name"]
    spec["mech"] = {"edit": None, "sib": sib, "xreg": xr or ("low" if c["mech"].get("xreg") == "low" else None)}
    return snap, rng, spec, p, qd


def build_t8_yes_flip(ctx, g):
    import copy
    c = g["cell"]
    snap, rng, spec, p, qd = _t8_base(ctx, g)
    yes = _finish(spec, "YES")
    out = [yes]
    flip = c.get("flip")
    if flip:
        s = copy.deepcopy(yes)
        q = s["query"]
        pe = next(e for e in s["entries"] if e["name"] == q["name"] and e["registry"] == q["registry"])
        card = s["card"]
        if flip == "t8_own_org":
            pe["publisher"] = card["own_org"]
            s["no_kind"] = "NM-R2"
        elif flip == "t8_not_reserved":
            card["reserved"] = [r for r in card["reserved"] if r != q["name"]] or [snap.package()]
            s["no_kind"] = "NM-R3"
        elif flip == "t8_internal_first":
            if q["explicit"]:
                q["explicit"] = False
            card["resolve_order"] = [card["internal_registry"]] + [r for r in card["resolve_order"] if r != card["internal_registry"]]
            s["no_kind"] = "NM-R1"
        elif flip == "t8_internal_query":
            q["registry"] = card["internal_registry"]
            s["no_kind"] = "NM-R1"
        else:
            raise Reject("unknown t8 flip")
        s["relation"] = "NM-T8"
        s["t8_variant"] = flip
        out.append(_finish(s, "NO"))
    return out


# ---- dispatch ------------------------------------------------------------------------------------------------------------------------
def build_group(ctx, g):
    t = g["cell"]["type"]
    return {"yes_flip": build_yes_flip, "pair_a": build_pair_a, "single_no": build_single_no, "single_yes": build_single_yes,
            "t8_flip": build_t8_yes_flip}[t](ctx, g)
