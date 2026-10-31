"""NM-T1..NM-T7 predicates: hand cases per relation + a brute-force cross product against an independent op ENUMERATOR (B's predicates compare
two strings; this test generates the one-operation neighbours of a name and checks the predicates against them in both directions)."""
import random

import pytest

from T63.solver_b import rel

ROWS = "a:qswz b:ghnv c:dfvx d:cefrsx e:drsw f:cdgrtv g:bfhtvy h:bgjnuy i:jkou j:hikmnu k:ijlmo l:kop m:jkn n:bhjm o:iklp p:lo q:aw r:deft s:adewxz t:fgry u:hijy v:bcfg w:aeqs x:cdsz y:ghtu z:asx"
NB = {kv.split(":")[0]: set(kv.split(":")[1]) for kv in ROWS.split()}
ALPH = "abmnrlo01s-_./x"


@pytest.mark.parametrize("p,q,which", [
    ("abc-df-core", "abc-def-core", "NM-T1/2"), ("abc-def-core", "abc-df-core", "NM-T1/2"), ("abcdef", "abcde", "NM-T1/2"), ("xabc", "abc", "NM-T1/2"),
    ("abc-dsf-core", "abc-def-core", "NM-T3"), ("abc-dwf-core", "abc-def-core", "NM-T3"),
    ("abc-edf-core", "abc-def-core", "NM-T4"), ("ab", "ba", "NM-T4"),
    ("abc_def_core", "abc-def-core", "NM-T5"), ("abcdef-core", "abc-def-core", "NM-T5"), ("abc.def.core", "abc-def-core", "NM-T5"),
    ("abc-def-core", "abcdefcore", "NM-T5"), ("a-b_c", "abc", "NM-T5"),
    ("abc-rnem-core", "abc-mem-core", "NM-T6"), ("abc-mem-core", "abc-rnem-core", "NM-T6"), ("abc-1em-core", "abc-lem-core", "NM-T6"),
    ("abc-l0w", "abc-low", "NM-T6"), ("abc-low", "abc-l0w", "NM-T6"),
    ("scope/abc-def-core", "abc-def-core", "NM-T7"), ("abc-def-core", "@scope/abc-def-core", "NM-T7")])
def test_relations_positive(p, q, which):
    assert which in rel.relations(p, q)
    assert rel.near(p, q) and rel.near(q, p)


@pytest.mark.parametrize("p,q", [
    ("abc-def-core", "abc-def-core"),                    # identical
    ("abc-def-core", "xyz-uvw-kit"),                     # unrelated
    ("abc-def-cxxe", "abc-def-core"),                    # two substitutions
    ("abc-def-corm", "abc-def-core"),                    # e -> m is not a keyboard neighbour
    ("abc-d1f-core", "abc-def-core"),                    # digits have no keyboard neighbours
    ("abc-def-core", "abc-def-corea"),                   # 'a' appended is an insertion: this IS near (checked below), so use a 2-char insert here
    ("ab-cd", "ab-cdxx"),                                # two characters added
    ("abc-edf-cxre", "abc-def-core"),                    # swap plus a change
    ("abcdef", "abcdfe-"),                               # swap plus an insertion
    ("a/b/c", "b/c"),                                    # two slashes
    ("/abc", "abd"),                                     # empty scope is no scope prefix, plus a substitution
    ("sc/abc", "abd"),                                   # scope plus an edit
    ("abc-rnx", "abc-mxx"),                              # rn -> m plus another change
])
def test_relations_negative_or_not_single_op(p, q):
    if (p, q) == ("abc-def-core", "abc-def-corea"):
        assert rel.near(p, q)                            # a single insertion of any character is near (T1/T2)
    else:
        assert not rel.near(p, q), rel.relations(p, q)


def test_empty_scope_is_not_t7_but_is_one_inserted_character():
    assert not rel.t7("/abc", "abc") and "NM-T1/2" in rel.relations("/abc", "abc")


def test_t5_not_for_scoped_names():
    assert not rel.t5("sc/a-b", "sc/ab")
    assert rel.near("sc/a-b", "sc/ab")                    # still near through T1 (one character deleted)


def test_t3_letters_only():
    assert not rel.t3("a-c", "a_c")
    assert rel.t3("qa", "qs") and not rel.t3("qa", "qp")


def _neighbours(q):
    out = set()
    for i in range(len(q)):
        out.add(q[:i] + q[i + 1:])                                                     # T1
    for i in range(len(q) + 1):
        for ch in ALPH:
            out.add(q[:i] + ch + q[i:])                                                # T2
    for i, c in enumerate(q):
        for nb in NB.get(c, ()):
            out.add(q[:i] + nb + q[i + 1:])                                            # T3
    for i in range(len(q) - 1):
        if q[i] != q[i + 1]:
            out.add(q[:i] + q[i + 1] + q[i] + q[i + 2:])                               # T4
    for old, new in (("rn", "m"), ("m", "rn"), ("l", "1"), ("1", "l"), ("o", "0"), ("0", "o")):
        for i in range(len(q) - len(old) + 1):
            if q[i:i + len(old)] == old:
                out.add(q[:i] + new + q[i + len(old):])                                # T6
    if "/" not in q:
        for scope in ("s", "@x", "ab"):
            out.add(scope + "/" + q)                                                   # T7 added
    elif q.count("/") == 1 and q.split("/", 1)[0]:
        out.add(q.split("/", 1)[1])                                                    # T7 removed
    out.discard(q)
    return out


def _t5_pin(p, q):
    strip = lambda s: "".join(c for c in s if c not in "-_.")
    return p != q and "/" not in p and "/" not in q and strip(p) == strip(q)


def _expected(p, q):
    return p in _neighbours(q) or q in _neighbours(p) or _t5_pin(p, q)


def test_predicates_match_enumerated_neighbours():
    rng = random.Random(63)
    checked = pos = 0
    for _ in range(3000):
        q = "".join(rng.choice(ALPH) for _ in range(rng.randint(1, 6)))
        mode = rng.random()
        if mode < 0.6:
            p = rng.choice(sorted(_neighbours(q)))
        elif mode < 0.8:
            p = q
            for _k in range(rng.randint(1, 3)):                                        # two or three chained edits
                p = rng.choice(sorted(_neighbours(p)))
        else:
            p = "".join(rng.choice(ALPH) for _ in range(rng.randint(1, 6)))
        e = _expected(p, q)
        assert rel.near(p, q) == e, (p, q)
        assert rel.near(q, p) == e, (q, p)
        checked += 1
        pos += e
    assert checked == 3000 and pos > 1500
