"""F11 hidden taxonomies and solver A (G0 sections 2-3).

Attributes (nominal, presence, numeric banded, date cut-off), cells = the product of value indices (numeric and date
attributes as bands), and four taxonomy shapes:
  BoxTax   S1, S2, S4 (and short cards): codes are boxes from a random splitting tree, plus 'unless' / 'only if'
           redirects and precedence notes; solver A = the cell -> code table built from the resolved rules.
  GroupTax S3: group tree (top groups by one nominal group attribute), leaves by leaf attributes, residual codes,
           scope notes; solver A = a top-down walk.
  ListTax  S6: ordered entries, first match wins, catch-all last; solver A = first-match scan.
  KeyTax   S5: numbered couplets; solver A = the key walk.
Every taxonomy runs its card validity check at build; a failing card is discarded (raise), never patched.
"""
from __future__ import annotations

import datetime as dt
import itertools
from fractions import Fraction

PRES, ABS = 0, 1


class CardInvalid(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ attributes
class Attr:
    """kind: nom | pres | num | date. Values are indices; num/date indices are bands over the cut list."""

    def __init__(self, aid, kind, name, *, values=None, terms=None, unit=None, cuts=None, lo=None, hi=None,
                 step=1, event=None):
        self.aid, self.kind, self.name = aid, kind, name
        self.values = list(values or [])       # nom: value names; pres: ['present', 'absent']
        self.terms = terms or {}                # nom: {idx: [terms]}; pres/num/date: {'attr': [terms]}
        self.unit = unit                        # num: (singular, plural)
        self.cuts = list(cuts or [])            # num: Fractions; date: dt.date
        self.lo, self.hi, self.step = lo, hi, step
        self.event = event                      # date: the event it dates

    @property
    def n(self) -> int:
        if self.kind == "nom":
            return len(self.values)
        if self.kind == "pres":
            return 2
        return len(self.cuts) + 1

    def band_of(self, x) -> int:
        b = 0
        for c in self.cuts:
            if x >= c:
                b += 1
        return b

    def band_range(self, b):
        """(lo inclusive, hi exclusive or None) of band b."""
        lo = self.cuts[b - 1] if b > 0 else None
        hi = self.cuts[b] if b < len(self.cuts) else None
        return lo, hi

    def grid_values(self, b):
        """Every grid value inside band b (num: multiples of step within [lo, hi]; date: days within the window)."""
        lo, hi = self.band_range(b)
        if self.kind == "num":
            a = self.lo if lo is None else lo
            z = self.hi if hi is None else hi - self.step
            out, x = [], Fraction(a)
            while x <= z:
                out.append(x)
                x += self.step
            return out
        a = self.lo if lo is None else lo
        z = self.hi if hi is None else hi - dt.timedelta(days=1)
        return [a + dt.timedelta(days=i) for i in range((z - a).days + 1)]

    def label(self, i) -> str:
        if self.kind in ("nom", "pres"):
            return self.values[i]
        return f"band{i}"

    def to_spec(self) -> dict:
        d = {"kind": self.kind, "n": self.n}
        if self.kind in ("num", "date"):
            d["cuts"] = [str(c) for c in self.cuts]
        return d


def all_cells(attrs):
    return list(itertools.product(*[range(a.n) for a in attrs]))


def neighbours_of_cell(attrs, cell, *, fixed=None):
    """Cells one neighbour step from cell (F11-R2-06): change one nominal value, toggle presence, move one band.
    fixed: an attribute index that never changes (the unstated attribute, R04)."""
    out = []
    for i, a in enumerate(attrs):
        if i == fixed:
            continue
        if a.kind in ("nom", "pres"):
            for j in range(a.n):
                if j != cell[i]:
                    out.append((i, cell[:i] + (j,) + cell[i + 1:]))
        else:
            for j in (cell[i] - 1, cell[i] + 1):
                if 0 <= j < a.n:
                    out.append((i, cell[:i] + (j,) + cell[i + 1:]))
    return out


def cond_holds(cond, cell, attrs_index):
    aid, allowed = cond
    return cell[attrs_index[aid]] in allowed


def contiguous(s) -> bool:
    s = sorted(s)
    return s == list(range(s[0], s[-1] + 1))


# ------------------------------------------------------------------------------------------------ code object
class Code:
    def __init__(self, k, box):
        self.k = k                      # index
        self.box = box                  # {aid: frozenset(allowed)}; missing aid = any
        self.rule = None                # {'kind': 'unless'|'onlyif', 'cond': (aid, frozenset), 'target': k2}
        self.mark = False
        self.residual_of = None         # S3: group index when residual
        self.group = None               # S3: lowest group index
        self.id = None
        self.name = None

    def parts(self, attrs):
        """Definition parts in attribute order: [(aid, frozenset)] (num/date ranges kept as one cond)."""
        return [(a.aid, self.box[a.aid]) for a in attrs if a.aid in self.box and len(self.box[a.aid]) < a.n]


# ------------------------------------------------------------------------------------------------ BoxTax
class BoxTax:
    shape = "box"

    def __init__(self, attrs, codes, notes, default=None, sampler="S1"):
        self.attrs = attrs
        self.ai = {a.aid: i for i, a in enumerate(attrs)}
        self.codes = codes
        self.notes = notes              # list of (winner, loser) code indices
        self.default = default          # (aid, value idx) SEM-03, or None
        self.sampler = sampler
        self.table = {}
        self.fits = {}
        self._build_table()

    def in_box(self, k, cell):
        return all(cell[self.ai[aid]] in s for aid, s in self.codes[k].box.items())

    def fit_set(self, cell):
        F, by_redirect = set(), set()
        for c in self.codes:
            if not self.in_box(c.k, cell):
                continue
            if c.rule is None:
                F.add(c.k)
                continue
            b = cond_holds(c.rule["cond"], cell, self.ai)
            ruled_out = b if c.rule["kind"] == "unless" else not b
            if ruled_out:
                F.add(c.rule["target"])
                by_redirect.add(c.rule["target"])
            else:
                F.add(c.k)
        return F, by_redirect

    def decide(self, F):
        if len(F) == 1:
            return next(iter(F))
        if len(F) == 2:
            a, b = sorted(F)
            ws = [w for (w, l) in self.notes if {w, l} == {a, b}]
            if len(ws) == 1:
                return ws[0]
        return None

    def _build_table(self):
        for cell in all_cells(self.attrs):
            F, red = self.fit_set(cell)
            self.fits[cell] = (F, red)
            self.table[cell] = self.decide(F)

    def resolve_cell(self, cell, missing=None):
        """The cell Assign reads: SEM-03 default for an unstated attribute."""
        if missing is None:
            return cell
        if self.default is None or self.default[0] != self.attrs[missing].aid:
            raise CardInvalid("unstated attribute without a missing rule")
        return cell[:missing] + (self.default[1],) + cell[missing + 1:]

    def assign(self, cell, missing=None):
        return self.table[self.resolve_cell(cell, missing)]

    def validate(self):
        pairs = set()
        for cell, (F, red) in self.fits.items():
            if not 1 <= len(F) <= 2:
                raise CardInvalid(f"|F|={len(F)} at {cell}")
            if red and len(F) != 1:
                raise CardInvalid("redirect cell with |F| > 1 (F11-R5-11)")
            if len(F) == 2:
                pairs.add(frozenset(F))
            if self.table[cell] is None:
                raise CardInvalid("undecided cell")
        named = [frozenset((w, l)) for w, l in self.notes]
        if sorted(map(sorted, pairs)) != sorted(map(sorted, set(named))) or len(set(named)) != len(named):
            raise CardInvalid("fitting pairs and notes differ")
        targets = {c.rule["target"] for c in self.codes if c.rule}
        for c in self.codes:
            if c.rule:
                t = c.rule["target"]
                if self.codes[t].rule is not None or t == c.k:
                    raise CardInvalid("redirect chain")
                if not c.parts(self.attrs):
                    raise CardInvalid("empty definition")
        for w, l in self.notes:
            if self.codes[w].rule or self.codes[l].rule:
                raise CardInvalid("note on a redirect code")
        got = set(self.table.values())
        if got != set(range(len(self.codes))):
            raise CardInvalid("code with no cell")
        nb = self.code_neighbours()
        if any(not nb[k] for k in range(len(self.codes))):
            raise CardInvalid("code without a neighbour")
        _ = targets
        return True

    def code_neighbours(self):
        nb = {k: set() for k in range(len(self.codes))}
        for cell, k in self.table.items():
            for _, c2 in neighbours_of_cell(self.attrs, cell):
                k2 = self.table[c2]
                if k2 != k:
                    nb[k].add(k2)
        return nb

    def to_spec(self) -> dict:
        return {"shape": "box", "attrs": [a.to_spec() for a in self.attrs],
                "codes": [{"box": {self.ai[aid]: sorted(s) for aid, s in c.parts(self.attrs)},
                           "rule": None if not c.rule else {"kind": c.rule["kind"],
                                                            "cond": [self.ai[c.rule["cond"][0]],
                                                                     sorted(c.rule["cond"][1])],
                                                            "target": c.rule["target"]},
                           "mark": c.mark} for c in self.codes],
                "notes": sorted([list(x) for x in self.notes]),
                "default": None if self.default is None else [self.ai[self.default[0]], self.default[1]]}


def _split_set(a, s, r):
    s = sorted(s)
    if a.kind in ("num", "date"):
        cut = r.randint(1, len(s) - 1)
        return [frozenset(s[:cut]), frozenset(s[cut:])]
    if a.kind == "pres":
        return [frozenset([x]) for x in s]
    k = 2 if len(s) < 4 or r.random() < 0.7 else 3
    r.shuffle(s)
    cuts = sorted(r.sample(range(1, len(s)), k - 1))
    parts, prev = [], 0
    for c in cuts + [len(s)]:
        parts.append(frozenset(s[prev:c]))
        prev = c
    return parts


def split_tree(attrs, n_codes, r, *, base=None, prefer=None):
    """A random splitting tree with n_codes leaf boxes. Returns (leaves [box], sibling_groups [[leaf idx]])."""
    full = {a.aid: frozenset(range(a.n)) for a in attrs}
    if base:
        full.update(base)
    nodes = [{"box": full, "kids": None, "parent": None}]
    leaves = [0]

    def size(b):
        p = 1
        for s in b.values():
            p *= len(s)
        return p
    guard = 0
    while len(leaves) < n_codes:
        guard += 1
        if guard > 5000:
            raise CardInvalid("tree split stalled")
        cand = [i for i in leaves if size(nodes[i]["box"]) > 1]
        if not cand:
            raise CardInvalid("space too small")
        w = [size(nodes[i]["box"]) ** 1.3 for i in cand]
        li = r.choices(cand, weights=w)[0]
        box = nodes[li]["box"]
        sa = [a for a in attrs if len(box[a.aid]) >= 2]
        if prefer:
            sa2 = [a for a in sa if a.aid in prefer]
            if sa2 and r.random() < 0.5:
                sa = sa2
        a = r.choice(sa)
        parts = _split_set(a, box[a.aid], r)
        if len(leaves) - 1 + len(parts) > n_codes:
            parts = [parts[0], frozenset().union(*parts[1:])]
        kids = []
        for p in parts:
            nb = dict(box)
            nb[a.aid] = p
            nodes.append({"box": nb, "kids": None, "parent": li, "split": a.aid})
            kids.append(len(nodes) - 1)
        nodes[li]["kids"] = kids
        leaves.remove(li)
        leaves.extend(kids)
    leaf_pos = {n: i for i, n in enumerate(leaves)}
    groups = []
    for i, nd in enumerate(nodes):
        if nd["kids"] and all(nodes[k]["kids"] is None for k in nd["kids"]):
            groups.append([leaf_pos[k] for k in nd["kids"]])
    grouped = {x for g in groups for x in g}
    lone = [leaf_pos[n] for n in leaves if leaf_pos[n] not in grouped]
    return [nodes[n]["box"] for n in leaves], groups, lone


def build_box(attrs, n_codes, r, *, n_unless=0, n_onlyif=0, n_notes=0, default=None, sampler="S1",
              mark_share=None, prefer=None):
    """S1 / S2 / S4 taxonomy (and short cards with no rules). Raises CardInvalid when the draw fails."""
    boxes, groups, lone = split_tree(attrs, n_codes, r, prefer=prefer)
    codes = [Code(i, dict(b)) for i, b in enumerate(boxes)]
    # strip full-range constraints
    for c in codes:
        c.box = {aid: s for aid, s in c.box.items() if len(s) < attrs[[a.aid for a in attrs].index(aid)].n}
    tax = BoxTax(attrs, codes, [], default=default, sampler=sampler)
    ai = tax.ai
    nb = tax.code_neighbours()
    used = set()
    # precedence notes: sibling leaf pairs; extend the loser's box into part of the winner's region
    notes = []
    sib_pairs = [g for g in groups if len(g) >= 2]
    r.shuffle(sib_pairs)
    for g in sib_pairs:
        if len(notes) >= n_notes:
            break
        k1, k2 = r.sample(g, 2)
        if k1 in used or k2 in used:
            continue
        b1, b2 = codes[k1].box, codes[k2].box
        diff = [aid for aid in set(b1) | set(b2) if b1.get(aid) != b2.get(aid)]
        if len(diff) != 1:
            continue
        aid = diff[0]
        a = attrs[ai[aid]]
        s1, s2 = b1.get(aid, frozenset(range(a.n))), b2.get(aid, frozenset(range(a.n)))
        if len(s1) < 2:
            continue
        if a.kind in ("num", "date"):
            # take the band(s) of s1 adjacent to s2
            if max(s2) < min(s1):
                ext = frozenset([min(s1)])
            elif min(s2) > max(s1):
                ext = frozenset([max(s1)])
            else:
                continue
        else:
            ext = frozenset(r.sample(sorted(s1), r.randint(1, len(s1) - 1)))
        newbox = dict(b2)
        news = s2 | ext
        if len(news) == a.n:
            newbox.pop(aid, None)
        else:
            newbox[aid] = news
        if not newbox:
            continue
        winner = r.choice([k1, k2])
        codes[k2].box = newbox
        notes.append((winner, k2 if winner == k1 else k1))
        used |= {k1, k2}
    # redirects: unless / only if
    order = list(range(len(codes)))
    r.shuffle(order)
    want = ["unless"] * n_unless + ["onlyif"] * n_onlyif
    targets = set()
    for kind in want:
        for k in order:
            if k in used or k in targets:
                continue
            c = codes[k]
            # condition attribute: free or partly constrained inside the box, with >= 2 allowed values
            opts = []
            for a in attrs:
                s = c.box.get(a.aid, frozenset(range(a.n)))
                if len(s) >= 2 and (default is None or a.aid != default[0]):
                    opts.append((a, s))
            if not opts:
                continue
            a, s = r.choice(opts)
            ss = sorted(s)
            if a.kind in ("num", "date"):
                cut = r.randint(1, len(ss) - 1)
                cond = frozenset(ss[cut:]) if r.random() < 0.5 else frozenset(ss[:cut])
                # a single CMP must express it: the set must reach an end of the attribute's band range
                if not (min(cond) == 0 or max(cond) == a.n - 1):
                    continue
            elif a.kind == "pres":
                cond = frozenset([r.choice(ss)])
            else:
                cond = frozenset(r.sample(ss, r.randint(1, len(ss) - 1)))
            # the redirected region: box & cond (unless) or box & not cond (only if)
            red = cond if kind == "unless" else frozenset(s) - cond
            if not red or red == frozenset(s):
                continue
            # target: a neighbour code of k with no rule, not already a rule holder
            cands = [t for t in nb[k] if t not in used and codes[t].rule is None and t != k]
            if not cands:
                continue
            t = r.choice(sorted(cands))
            c.rule = {"kind": kind, "cond": (a.aid, cond), "target": t}
            used.add(k)
            targets.add(t)
            used.add(t)
            break
    if mark_share is None:
        mark_share = r.uniform(0.3, 0.6)
    idx = list(range(len(codes)))
    r.shuffle(idx)
    for k in idx[:max(1, round(mark_share * len(codes)))]:
        codes[k].mark = True
    tax = BoxTax(attrs, codes, notes, default=default, sampler=sampler)
    tax.validate()
    tax.sibling_groups = groups
    tax.lone = lone
    return tax


# ------------------------------------------------------------------------------------------------ S3 GroupTax
class GroupTax:
    shape = "group"

    def __init__(self, attrs, gattr, groups, codes, scope_notes, default=None):
        """attrs[0] is the group attribute (nominal). groups: [{'vals': frozenset, 'name', 'residual': k|None,
        'leaves': [k]}]; codes: leaves (box over leaf attributes) and residuals; scope_notes: [{'src': g, 'dst': h,
        'cond': (aid, frozenset)}]. One level of groups (2-level tree: top groups -> leaves)."""
        self.attrs, self.gattr = attrs, gattr
        self.ai = {a.aid: i for i, a in enumerate(attrs)}
        self.groups, self.codes, self.scope_notes = groups, codes, scope_notes
        self.default = default
        self.notes = []
        self.table = {}
        self.ingroup = {}
        for cell in all_cells(attrs):
            g = self.group_of(cell)
            self.ingroup[cell] = g
            self.table[cell] = self.leaf_of(cell, g)

    def group_of(self, cell):
        gv = cell[self.ai[self.gattr]]
        home = [i for i, g in enumerate(self.groups) if gv in g["vals"]]
        if len(home) != 1:
            raise CardInvalid("group values do not partition")
        g = home[0]
        for sn in self.scope_notes:
            if sn["src"] == g and cond_holds(sn["cond"], cell, self.ai):
                return sn["dst"]
        return g

    def in_group(self, cell, g):
        return self.group_of(cell) == g

    def leaf_fits(self, k, cell):
        c = self.codes[k]
        return all(cell[self.ai[aid]] in s for aid, s in c.box.items())

    def leaf_of(self, cell, g):
        grp = self.groups[g]
        fit = [k for k in grp["leaves"] if self.leaf_fits(k, cell)]
        if len(fit) == 1:
            return fit[0]
        if not fit and grp["residual"] is not None:
            return grp["residual"]
        raise CardInvalid(f"group {g}: {len(fit)} leaves fit at {cell}")

    def resolve_cell(self, cell, missing=None):
        if missing is None:
            return cell
        if self.default is None or self.default[0] != self.attrs[missing].aid:
            raise CardInvalid("unstated attribute without a missing rule")
        return cell[:missing] + (self.default[1],) + cell[missing + 1:]

    def assign(self, cell, missing=None):
        return self.table[self.resolve_cell(cell, missing)]

    def group_assign(self, cell, missing=None):
        return self.ingroup[self.resolve_cell(cell, missing)]

    def validate(self):
        if set(self.table.values()) != set(range(len(self.codes))):
            raise CardInvalid("S3 code with no cell")
        srcs = {s["src"] for s in self.scope_notes}
        dsts = {s["dst"] for s in self.scope_notes}
        if srcs & dsts or len(srcs) != len(self.scope_notes):
            raise CardInvalid("scope note chain")
        if any(not v for v in self.code_neighbours().values()):
            raise CardInvalid("S3 code without a neighbour")
        return True

    def code_neighbours(self):
        nb = {k: set() for k in range(len(self.codes))}
        for cell, k in self.table.items():
            for _, c2 in neighbours_of_cell(self.attrs, cell):
                if self.table[c2] != k:
                    nb[k].add(self.table[c2])
        return nb

    def to_spec(self) -> dict:
        return {"shape": "group", "attrs": [a.to_spec() for a in self.attrs], "gattr": self.ai[self.gattr],
                "groups": [{"vals": sorted(g["vals"]), "leaves": list(g["leaves"]), "residual": g["residual"]}
                           for g in self.groups],
                "codes": [{"box": {self.ai[aid]: sorted(s) for aid, s in c.box.items()}, "mark": c.mark,
                           "residual_of": c.residual_of} for c in self.codes],
                "scope": [[s["src"], s["dst"], self.ai[s["cond"][0]], sorted(s["cond"][1])]
                          for s in self.scope_notes],
                "default": None if self.default is None else [self.ai[self.default[0]], self.default[1]]}


def build_group(attrs, r, *, n_top, leaves_per, residual_share=0.6, n_scope=1, default=None):
    """attrs[0] = group attribute (nominal, >= n_top values); attrs[1:] = leaf attributes."""
    g_attr = attrs[0]
    if g_attr.kind != "nom" or n_top > g_attr.n or n_top < 3:
        raise CardInvalid("group attribute too small")
    vals = list(range(g_attr.n))
    r.shuffle(vals)
    # partition the group attribute's values into n_top groups
    cuts = sorted(r.sample(range(1, len(vals)), n_top - 1))
    parts, prev = [], 0
    for c in cuts + [len(vals)]:
        parts.append(frozenset(vals[prev:c]))
        prev = c
    leaf_attrs = attrs[1:]
    codes, groups = [], []
    for gi, vs in enumerate(parts):
        nl = leaves_per[gi]
        has_res = r.random() < residual_share
        boxes, sg, lone = split_tree(leaf_attrs, nl + (1 if has_res else 0), r)
        leaves = []
        res_k = None
        if has_res:
            # the residual takes the cells of one leaf box (that box is left uncovered by leaves)
            drop = r.randrange(len(boxes))
            boxes = [b for i, b in enumerate(boxes) if i != drop]
        for b in boxes:
            c = Code(len(codes), {aid: s for aid, s in b.items() if len(s) < leaf_attrs[[a.aid for a in leaf_attrs].index(aid)].n})
            c.group = gi
            codes.append(c)
            leaves.append(c.k)
        if has_res:
            c = Code(len(codes), {})
            c.residual_of = gi
            c.group = gi
            codes.append(c)
            res_k = c.k
        groups.append({"vals": vs, "leaves": leaves, "residual": res_k, "sib": sg})
    for c in codes:
        c.mark = False
    for gi, g in enumerate(groups):
        if r.random() < 0.45:
            for k in g["leaves"] + ([g["residual"]] if g["residual"] is not None else []):
                codes[k].mark = True
    scope = []
    gidx = list(range(len(groups)))
    r.shuffle(gidx)
    for _ in range(n_scope):
        free = [g for g in gidx if g not in {s["src"] for s in scope} | {s["dst"] for s in scope}]
        if len(free) < 2:
            break
        for _try in range(30):
            src, dst = r.sample(free, 2)
            la = r.choice([a for a in leaf_attrs if a.n >= 2])
            ss = list(range(la.n))
            if la.kind in ("num", "date"):
                cut = r.randint(1, la.n - 1)
                cond = frozenset(ss[cut:]) if r.random() < 0.5 else frozenset(ss[:cut])
            else:
                cond = frozenset(r.sample(ss, r.randint(1, max(1, la.n - 1))))
            trial = scope + [{"src": src, "dst": dst, "cond": (la.aid, cond)}]
            try:
                GroupTax(attrs, g_attr.aid, groups, codes, trial, default=default).validate()
            except CardInvalid:
                continue
            scope = trial
            break
    gt = GroupTax(attrs, g_attr.aid, groups, codes, scope, default=default)
    gt.validate()
    gt.sibling = [g["sib"] for g in groups]
    return gt


# ------------------------------------------------------------------------------------------------ S6 ListTax
class ListTax:
    shape = "list"

    def __init__(self, attrs, entries, catch, n_codes):
        """entries: [(conds [(aid, frozenset)], k)] in order; catch: code of the catch-all (last entry)."""
        self.attrs = attrs
        self.ai = {a.aid: i for i, a in enumerate(attrs)}
        self.entries, self.catch, self.n_codes = entries, catch, n_codes
        self.default = None
        self.notes = []
        self.codes = [Code(k, {}) for k in range(n_codes)]
        self.table, self.first = {}, {}
        for cell in all_cells(attrs):
            m = self.matches(cell)
            self.first[cell] = m[0] if m else len(entries)
            self.table[cell] = entries[m[0]][1] if m else catch

    def entry_meets(self, j, cell):
        return all(cond_holds(c, cell, self.ai) for c in self.entries[j][0])

    def matches(self, cell):
        return [j for j in range(len(self.entries)) if self.entry_meets(j, cell)]

    def resolve_cell(self, cell, missing=None):
        if missing is not None:
            raise CardInvalid("S6 has no missing rule")
        return cell

    def assign(self, cell, missing=None):
        return self.table[cell]

    def code_neighbours(self):
        nb = {k: set() for k in range(self.n_codes)}
        for cell, k in self.table.items():
            for _, c2 in neighbours_of_cell(self.attrs, cell):
                if self.table[c2] != k:
                    nb[k].add(self.table[c2])
        return nb

    def validate(self):
        if set(self.table.values()) != set(range(self.n_codes)):
            raise CardInvalid("S6 code never reached")
        firsts = set(self.first.values())
        if firsts != set(range(len(self.entries) + 1)):
            raise CardInvalid("S6 entry never decides")
        if any(not v for v in self.code_neighbours().values()):
            raise CardInvalid("S6 code without a neighbour")
        return True

    def to_spec(self) -> dict:
        return {"shape": "list", "attrs": [a.to_spec() for a in self.attrs],
                "entries": [[[self.ai[aid], sorted(s)] for aid, s in conds] + [k] for conds, k in self.entries],
                "catch": self.catch, "marks": [c.mark for c in self.codes]}


def build_list(attrs, n_codes, r, *, max_repeat_share=0.3):
    cells = all_cells(attrs)
    ai = {a.aid: i for i, a in enumerate(attrs)}
    n_rep = r.randint(0, int(max_repeat_share * n_codes))
    entries = []
    claimed = set()
    code_order = list(range(n_codes))
    catch = code_order.pop()            # the catch-all code
    seq = code_order + r.sample(code_order, n_rep)
    r.shuffle(seq)
    for ei, k in enumerate(seq):
        remaining = len(seq) - ei
        for _ in range(200):
            free = [c for c in cells if c not in claimed]
            if len(free) < 2:
                raise CardInvalid("S6 space used up")
            budget = max(1, (len(free) - 2) // remaining)
            c0 = r.choice(free)
            na = r.choice((2, 3, 3, 4, 4, 5))
            ats = r.sample(range(len(attrs)), min(na, len(attrs)))
            conds = []
            for i in sorted(ats):
                a = attrs[i]
                if a.kind in ("num", "date"):
                    b = c0[i]
                    if r.random() < 0.5 and b > 0:
                        conds.append((a.aid, frozenset(range(b, a.n))))
                    elif b < a.n - 1:
                        conds.append((a.aid, frozenset(range(0, b + 1))))
                    else:
                        conds.append((a.aid, frozenset(range(b, a.n))))
                elif a.kind == "pres":
                    conds.append((a.aid, frozenset([c0[i]])))
                else:
                    extra = [x for x in range(a.n) if x != c0[i]]
                    s = {c0[i]} | set(r.sample(extra, 1 if r.random() < 0.25 else 0))
                    conds.append((a.aid, frozenset(s)))
            if all(len(s) == attrs[ai[aid]].n for aid, s in conds):
                continue
            reg = [c for c in cells if all(c[ai[aid]] in s for aid, s in conds)]
            new = [c for c in reg if c not in claimed]
            if not new or len(claimed) + len(new) >= len(cells) or len(new) > 2 * budget:
                continue
            entries.append((conds, k))
            claimed |= set(reg)
            break
        else:
            raise CardInvalid("S6 entry draw failed")
    lt = ListTax(attrs, entries, catch, n_codes)
    for c in lt.codes:
        c.mark = r.random() < 0.45
    lt.validate()
    return lt


# ------------------------------------------------------------------------------------------------ S5 KeyTax
class KeyTax:
    shape = "key"

    def __init__(self, attrs, couplets, n_codes, default=None):
        """couplets: {n: {'cond': (aid, frozenset), 'a': ('n', m) | ('k', code), 'b': ..., 'group': name idx|None}}"""
        self.attrs, self.couplets, self.n_codes = attrs, couplets, n_codes
        self.ai = {a.aid: i for i, a in enumerate(attrs)}
        self.default = default
        self.notes = []
        self.codes = [Code(k, {}) for k in range(n_codes)]
        self.table, self.paths = {}, {}
        for cell in all_cells(attrs):
            k, path = self.walk(cell)
            self.table[cell], self.paths[cell] = k, path
        # named couplets' groups (group index -> couplet and the codes reached through it)
        self.groups = {}
        for n, cp in couplets.items():
            if cp.get("group") is not None:
                self.groups[cp["group"]] = {"couplet": n, "leaves": sorted({k for cl, k in self.table.items()
                                                                            if n in self.paths[cl]})}

        gs = [{self.couplets[n]["group"] for n in p if self.couplets[n].get("group") is not None}
              for p in self.paths.values()]
        self.partition = bool(self.groups) and sorted(self.groups) == list(range(len(self.groups))) and \
            all(len(x) == 1 for x in gs)

    def group_assign(self, cell, missing=None):
        gs = {self.couplets[n]["group"] for n in self.groups_of(cell, missing)}
        if len(gs) != 1:
            raise CardInvalid("key groups do not partition")
        return gs.pop()

    def walk(self, cell):
        n, path = 1, []
        while True:
            path.append(n)
            cp = self.couplets[n]
            nxt = cp["a"] if cond_holds(cp["cond"], cell, self.ai) else cp["b"]
            if nxt[0] == "k":
                return nxt[1], tuple(path)
            n = nxt[1]

    def resolve_cell(self, cell, missing=None):
        if missing is None:
            return cell
        if self.default is None or self.default[0] != self.attrs[missing].aid:
            raise CardInvalid("unstated attribute without a missing rule")
        return cell[:missing] + (self.default[1],) + cell[missing + 1:]

    def assign(self, cell, missing=None):
        return self.table[self.resolve_cell(cell, missing)]

    def groups_of(self, cell, missing=None):
        p = self.paths[self.resolve_cell(cell, missing)]
        return [n for n in p if self.couplets[n].get("group") is not None]

    def code_neighbours(self):
        nb = {k: set() for k in range(self.n_codes)}
        for cell, k in self.table.items():
            for _, c2 in neighbours_of_cell(self.attrs, cell):
                if self.table[c2] != k:
                    nb[k].add(self.table[c2])
        return nb

    def validate(self):
        if set(self.table.values()) != set(range(self.n_codes)):
            raise CardInvalid("S5 code never reached")
        if any(not v for v in self.code_neighbours().values()):
            raise CardInvalid("S5 code without a neighbour")
        return True

    def to_spec(self):
        return {"shape": "key", "attrs": [a.to_spec() for a in self.attrs],
                "couplets": {str(n): [self.ai[c["cond"][0]], sorted(c["cond"][1]), list(c["a"]), list(c["b"]),
                                      c.get("group")] for n, c in sorted(self.couplets.items())}}


def build_key(attrs, n_codes, r, *, n_named=3):
    """Binary key over the cell space: each couplet tests one condition; leaves are distinct codes."""
    full = {a.aid: frozenset(range(a.n)) for a in attrs}
    # build a binary tree by splitting boxes with one condition each
    nodes = [{"box": full, "cond": None, "kids": None}]
    leaves = [0]
    guard = 0
    while len(leaves) < n_codes:
        guard += 1
        if guard > 5000:
            raise CardInvalid("key split stalled")
        li = r.choice([i for i in leaves if any(len(s) >= 2 for s in nodes[i]["box"].values())])
        box = nodes[li]["box"]
        a = r.choice([a for a in attrs if len(box[a.aid]) >= 2])
        s = sorted(box[a.aid])
        if a.kind in ("num", "date"):
            cut = r.randint(1, len(s) - 1)
            yes = frozenset(s[cut:])
            cond_set = frozenset(range(s[cut], a.n))      # "at least <cut>" over the whole range
        elif a.kind == "pres":
            yes = frozenset([s[0]])
            cond_set = yes
        else:
            yes = frozenset(r.sample(s, r.randint(1, len(s) - 1)))
            cond_set = yes
        no = frozenset(s) - yes
        kids = []
        for part in (yes, no):
            nb = dict(box)
            nb[a.aid] = part
            nodes.append({"box": nb, "cond": None, "kids": None})
            kids.append(len(nodes) - 1)
        nodes[li]["cond"] = (a.aid, cond_set)
        nodes[li]["kids"] = kids
        leaves.remove(li)
        leaves.extend(kids)
    # number couplets breadth-first; codes in leaf order shuffled
    codes = list(range(n_codes))
    r.shuffle(codes)
    leaf_code = {n: codes[i] for i, n in enumerate(leaves)}
    num, q = {}, [0]
    while q:
        x = q.pop(0)
        if nodes[x]["kids"]:
            num[x] = len(num) + 1
            q.extend(nodes[x]["kids"])
    couplets = {}
    for x, n in num.items():
        a_k, b_k = nodes[x]["kids"]
        ref = lambda y: ("n", num[y]) if y in num else ("k", leaf_code[y])  # noqa: E731
        couplets[n] = {"cond": nodes[x]["cond"], "a": ref(a_k), "b": ref(b_k), "group": None}
    # named couplets (groups): pick couplets at depth 1 (children of the root) as one level
    kt = KeyTax(attrs, couplets, n_codes)
    lvl = [c[1] for c in (couplets[1]["a"], couplets[1]["b"]) if c[0] == "n"]
    if len(lvl) == 2:
        for gi, n in enumerate(lvl):
            couplets[n]["group"] = gi
    kt = KeyTax(attrs, couplets, n_codes)
    for c in kt.codes:
        c.mark = r.random() < 0.45
    kt.validate()
    return kt
