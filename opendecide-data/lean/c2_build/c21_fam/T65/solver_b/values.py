"""Abstract values for solver B's dataflow (stdlib only).

An AVal summarises every concrete value a variable can hold at a program point, over all paths that reach it:
  atk    some path gives an attacker-controlled value        neut  classes neutralised on EVERY attacker-controlled path (intersection)
  pw     some path gives a password-role value               weak  some path gives a fast unsalted digest of a password-role value
  pred   some path gives a predictable temporary path         shared  the shared temp directory (a name inside it is predictable)
  lits   constant text fragments that went into the value    const  the exact string when the value is one constant
  items  container members (tuple / list / dict)             handle  heap object id (TLS context)       kind  coarse type tag
Join is "may": flags are OR-ed, neut is intersected (a path with a raw value defeats the neutraliser on the other path).
"""
from .rules import ALL_NEUT


class AVal(object):
    __slots__ = ("atk", "pw", "neut", "weak", "pred", "shared", "lits", "const", "items", "handle", "kind", "bound")

    def __init__(self, atk=False, pw=False, neut=ALL_NEUT, weak=False, pred=False, shared=False, lits=(), const=None, items=None, handle=None, kind="val", bound=None):
        self.atk, self.pw, self.weak, self.pred, self.shared = atk, pw, weak, pred, shared
        self.neut = neut if atk else ALL_NEUT
        self.lits, self.const, self.items, self.handle, self.kind, self.bound = tuple(lits), const, items, handle, kind, bound

    def replace(self, **kw):
        d = dict(atk=self.atk, pw=self.pw, neut=self.neut, weak=self.weak, pred=self.pred, shared=self.shared, lits=self.lits, const=self.const,
                 items=self.items, handle=self.handle, kind=self.kind, bound=self.bound)
        d.update(kw)
        return AVal(**d)

    def sensitive(self):
        """True when the value carries state a call we do not model could hide or act on."""
        return self.atk or self.pw or self.weak or self.pred or self.shared or self.handle is not None or bool(self.items and any(i.sensitive() for i in _members(self)))


def _members(v):
    if v.items is None:
        return []
    return list(v.items.values()) if isinstance(v.items, dict) else list(v.items)


CLEAN = AVal()
NONE = AVal(kind="none")


def const(s):
    return AVal(const=s, lits=(s,) if isinstance(s, str) else (), kind="str" if isinstance(s, str) else "val")


def tainted(pw=False):
    return AVal(atk=True, pw=pw, neut=frozenset())


def join(a, b):
    """May-join of two values reaching the same point by different paths."""
    if a is b:
        return a
    atk = a.atk or b.atk
    items = None
    if a.items is not None and b.items is not None:
        if isinstance(a.items, dict) and isinstance(b.items, dict):
            keys = list(a.items) + [k for k in b.items if k not in a.items]
            items = {}
            for k in keys:
                items[k] = join(a.items[k], b.items[k]) if (k in a.items and k in b.items) else (a.items.get(k) or b.items.get(k))
        elif not isinstance(a.items, dict) and not isinstance(b.items, dict) and len(a.items) == len(b.items):
            items = tuple(join(x, y) for x, y in zip(a.items, b.items))
    handle = a.handle if a.handle == b.handle else (a.handle if b.handle is None else b.handle)
    return AVal(atk=atk, pw=a.pw or b.pw, neut=(a.neut & b.neut), weak=a.weak or b.weak, pred=a.pred or b.pred, shared=a.shared or b.shared,
                lits=_merge_lits(a.lits, b.lits), const=a.const if a.const == b.const else None, items=items, handle=handle,
                kind=a.kind if a.kind == b.kind else "val", bound=a.bound if a.bound == b.bound else None)


def _merge_lits(x, y):
    out = list(x)
    out.extend(t for t in y if t not in x)
    return tuple(out)


def combine(parts):
    """Value built from several operands (concatenation, formatting, container summary): flags OR-ed, neut intersected, fragments kept in order."""
    parts = list(parts)
    if not parts:
        return CLEAN
    atk = any(p.atk for p in parts)
    neut = ALL_NEUT
    for p in parts:
        neut = neut & p.neut
    lits = []
    for p in parts:
        lits.extend(p.lits)
    return AVal(atk=atk, pw=any(p.pw for p in parts), neut=neut, weak=any(p.weak for p in parts), pred=any(p.pred for p in parts),
                shared=any(p.shared for p in parts), lits=lits)


def summary(v):
    """A container used as a plain value: the combination of its members and itself."""
    mem = _members(v)
    if not mem:
        return v
    return combine([v.replace(items=None, kind="val")] + [summary(m) for m in mem])
