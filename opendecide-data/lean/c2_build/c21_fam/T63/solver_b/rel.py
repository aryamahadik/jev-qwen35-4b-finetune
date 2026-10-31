"""NM-T1..NM-T7 as PAIRWISE PREDICATES on two names (ROW_SCHEMA 2a conventions). B decides "is p near q" by comparing the two strings
directly; it never generates candidate edits of a name. The relation is symmetric: near(p, q) = rel(p, q) or rel(q, p) for one single operation."""

KEYBOARD = {
    "a": "qswz", "b": "ghnv", "c": "dfvx", "d": "cefrsx", "e": "drsw", "f": "cdgrtv", "g": "bfhtvy", "h": "bgjnuy", "i": "jkou", "j": "hikmnu",
    "k": "ijlmo", "l": "kop", "m": "jkn", "n": "bhjm", "o": "iklp", "p": "lo", "q": "aw", "r": "deft", "s": "adewxz", "t": "fgry", "u": "hijy",
    "v": "bcfg", "w": "aeqs", "x": "cdsz", "y": "ghtu", "z": "asx"}
SEPARATORS = "-_."
LOOKALIKE_SWAPS = (("rn", "m"), ("m", "rn"), ("l", "1"), ("1", "l"), ("o", "0"), ("0", "o"))


def _one_deleted(longer, shorter):
    """True iff `shorter` is `longer` with exactly one character removed."""
    if len(longer) != len(shorter) + 1:
        return False
    i = 0
    while i < len(shorter) and longer[i] == shorter[i]:
        i += 1
    return longer[i + 1:] == shorter[i:]


def t1_t2(p, q):
    """One character dropped or added (any character, anywhere; separators count)."""
    return _one_deleted(p, q) or _one_deleted(q, p)


def _diff_positions(p, q):
    return [i for i in range(len(p)) if p[i] != q[i]]


def t3(p, q):
    """Same length, exactly one position differs, and the two letters are neighbours on the QWERTY map (map is read in both directions)."""
    if len(p) != len(q):
        return False
    d = _diff_positions(p, q)
    if len(d) != 1:
        return False
    a, b = p[d[0]], q[d[0]]
    return b in KEYBOARD.get(a, "") or a in KEYBOARD.get(b, "")


def t4(p, q):
    """Same length, exactly two ADJACENT positions differ and they are swapped."""
    if len(p) != len(q):
        return False
    d = _diff_positions(p, q)
    return len(d) == 2 and d[1] == d[0] + 1 and p[d[0]] == q[d[1]] and p[d[1]] == q[d[0]]


def _strip_sep(s):
    return "".join(ch for ch in s if ch not in SEPARATORS)


def t5(p, q):
    """p != q, neither contains '/', and they are equal once every '-', '_' and '.' is deleted."""
    if p == q or "/" in p or "/" in q:
        return False
    return _strip_sep(p) == _strip_sep(q)


def _one_swap(src, dst, old, new):
    """True iff replacing ONE occurrence of `old` in src by `new` gives dst."""
    start = src.find(old)
    while start != -1:
        if src[:start] + new + src[start + len(old):] == dst:
            return True
        start = src.find(old, start + 1)
    return False


def t6(p, q):
    """ASCII look-alike swap: one occurrence rn->m, m->rn, l->1, 1->l, o->0 or 0->o (either direction)."""
    for old, new in LOOKALIKE_SWAPS:
        if _one_swap(p, q, old, new) or _one_swap(q, p, old, new):
            return True
    return False


def _scoped_of(scoped, bare):
    return scoped.count("/") == 1 and bare.count("/") == 0 and scoped.split("/", 1)[0] != "" and scoped.split("/", 1)[1] == bare


def t7(p, q):
    """Scope prefix added or removed: one name has exactly one '/', a non-empty scope before it, and the text after it equals the other name."""
    return _scoped_of(p, q) or _scoped_of(q, p)


TESTS = (("NM-T1/2", t1_t2), ("NM-T3", t3), ("NM-T4", t4), ("NM-T5", t5), ("NM-T6", t6), ("NM-T7", t7))


def relations(p, q):
    """Names of the T1..T7 relations that hold between p and q (empty for identical names)."""
    if p == q:
        return []
    return [name for name, fn in TESTS if fn(p, q)]


def near(p, q):
    return bool(relations(p, q))
