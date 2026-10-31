"""Question-side cue templates (G0 section 4) and the composition engine for A, N, D and V questions.

A question = OUTER(PREFIX*(CORE)):
  OUTER   "mq"  matrix interrogative of the core (only when the core has a matrix form with no L_core word and there is
                no prefix; SEM-01), a truth frame "F01".."F10" (closed list, SEM-01), or "C2m" ("Is it false that ...?",
                the matrix C2 frame, CF-5).
  PREFIX  embedded C2 operators: "it is not the case that " (C2n) or "it is false that " (C2f).
  CORE    one cue template on the base atom (identity, C1, C3, C5, C6, C8, C9, C10, C12, C13, C14, C15, C16 forms).
k (k_neg) = k(core) + number of C2 operators; families = the core's families + "C2" per C2 operator. LF = the core's LF
under one ["not", .] per C2 operator. Polarity of <P> = parity of down operators on the path when every operator on it
is up or down (section 4 table), else None.

Every template declares: id, family, side "q", LF signature, k, slot monotonicity, L_neg entries, N/D eligibility. The
bank lint (bank.py) renders every template on a probe atom, parses it with the independent question parser and checks
the declared LF, k and polarity (100%).
"""
from __future__ import annotations

FRAMES = {
    "F01": "Is it true that {c}?",
    "F02": "Is the following statement true: {c}?",
    "F03": "Is it the case that {c}?",
    "F04": "Does the record show that {c}?",
    "F05": "According to the record, is it true that {c}?",
    "F06": "Based on the text, is it the case that {c}?",
    "F07": "Is this assertion true: {c}?",
    "F08": "Do the facts given establish that {c}?",
    "F09": "Taking the record as given, is it true that {c}?",
    "F10": "Is the statement that {c} true?",
}
C2_PREFIX = {"C2n": "it is not the case that ", "C2f": "it is false that "}
C2M = "Is it false that {c}?"

# matrix tails (A / matrix rows only; no operator words): spread matrix question templates under G11's 2% rule
TAILS = ["", ", according to the record", ", on the facts given", ", going by the text", ", based on the record"]


class Core:
    """One cue template applied to an atom: clause text (embedded form), optional matrix question, LF, k, families,
    L_neg entries, polarity effect on <P> ('up' / 'down' / None = non-monotone or opaque), N/D eligibility."""

    __slots__ = ("tid", "fam", "clause", "matrix", "lf", "k", "pol", "nd", "lneg", "rel", "ptag")

    def __init__(self, tid, fam, clause, matrix, lf, k, pol, nd=False, lneg=(), rel="same", ptag=None):
        self.tid, self.fam, self.clause, self.matrix, self.lf = tid, tuple(fam), clause, matrix, lf
        self.k, self.pol, self.nd, self.lneg, self.rel, self.ptag = k, pol, nd, tuple(lneg), rel, ptag


def NOT(x):
    return ["not", x]


def compose(core: Core, outer: str, prefixes: tuple = (), tail: str = ""):
    """(question, lf, k, families, polarity flips or None, template key). Raises ValueError on an illegal combination."""
    c = core.clause
    for p in reversed(prefixes):
        c = C2_PREFIX[p] + c
    if outer == "mq":
        if prefixes or core.matrix is None:
            raise ValueError("matrix form needs a core with a matrix question and no prefix")
        q = core.matrix + tail + "?"
    elif outer == "C2m":
        q = C2M.format(c=c + tail)
    else:
        q = FRAMES[outer].format(c=c)
    lf = core.lf
    flips = 0 if core.pol == "up" else (1 if core.pol == "down" else None)
    nC2 = len(prefixes) + (1 if outer == "C2m" else 0)
    for _ in range(nC2):
        lf = NOT(lf)
    if flips is not None:
        flips += nC2
    fams = tuple(core.fam) + ("C2",) * nC2
    k = core.k + nC2
    key = "|".join([outer if outer in ("mq", "C2m") else "FR", *prefixes, core.tid, tail.strip(", ") or "-"])
    return q, lf, k, fams, flips, key


# ---------------------------------------------------------------------------------------------------------------------
# atom realizations (program-written English; every word outside pack nouns comes from the 3.4 lexicons)

def adj_cores(subj, word, neg=None):
    P = ["adj", subj, word]
    out = [Core("ADJ.pos", (), f"{subj} is {word}", f"Is {subj} {word}", P, 0, "up"),
           Core("C1.adj", ("C1",), f"{subj} is not {word}", None, NOT(P), 1, "down", nd=True, lneg=("not",))]
    if neg:
        out += [Core("C6.adj", ("C6",), f"{subj} is {neg}", f"Is {subj} {neg}", NOT(P), 1, "down", nd=True,
                     lneg=(neg,)),
                Core("C1C6.adj", ("C1", "C6"), f"{subj} is not {neg}", None, NOT(NOT(P)), 2, "up", nd=True,
                     lneg=("not", neg))]
    return out


def has_cores(subj, thing):
    P = ["has", subj, thing]
    return [Core("HAS.pos", (), f"{subj} has a {thing}", f"Does {subj} have a {thing}", P, 0, "up"),
            Core("C1.has", ("C1",), f"{subj} does not have a {thing}", None, NOT(P), 1, "down", nd=True, lneg=("not",)),
            Core("C5.lacks", ("C5",), f"{subj} lacks a {thing}", f"Does {subj} lack a {thing}", NOT(P), 1, "down",
                 nd=True, lneg=("lack",)),
            Core("C5.without", ("C5",), f"{subj} is without a {thing}", f"Is {subj} without a {thing}", NOT(P), 1,
                 "down", nd=True, lneg=("without",)),
            Core("C1C5.lacks", ("C1", "C5"), f"{subj} does not lack a {thing}", None, NOT(NOT(P)), 2, "up", nd=True,
                 lneg=("not", "lack"))]


def conn_cores(subj, a, b, b_neg=None):
    """C13 / C16 on two adjectives of one subject (a = the base predicate). b is a determined second atom."""
    A, B = ["adj", subj, a], ["adj", subj, b]
    return [Core("C13.neither", ("C13",), f"{subj} is neither {a} nor {b}", None, ["and", NOT(A), NOT(B)], 1, "down",
                 lneg=("neither ... nor",), rel="conn"),
            Core("C13.notboth", ("C13",), f"{subj} is not both {a} and {b}", None, NOT(["and", A, B]), 1, "down",
                 lneg=("not both",), rel="conn"),
            Core("C16.decoy", ("C16",), f"{subj} is not only {a} but also {b}", None, ["and", A, B], 0, "up",
                 lneg=("not only",), rel="conn"),
            Core("C13.or", (), f"{subj} is {a} or {b}", f"Is {subj} {a} or {b}", ["or", A, B], 0, "up", rel="conn")]


def deon_cores(role, verb, obj, which):
    """which = 'perm' or 'req' (the base status). Positive modals are identity; negated modals are C12 (down)."""
    P = ["deon", which, role, verb, obj]
    r = f"the {role}"
    if which == "perm":
        return [Core("DEON.perm", (), f"{r} is permitted to {verb} {obj}", f"Is {r} permitted to {verb} {obj}", P, 0,
                     "up"),
                Core("DEON.may", (), f"{r} may {verb} {obj}", None, P, 0, "up"),
                Core("C12.mustnot", ("C12",), f"{r} must not {verb} {obj}", None, NOT(P), 1, "down",
                     lneg=("must not",)),
                Core("C12.maynot", ("C12",), f"{r} may not {verb} {obj}", None, NOT(P), 1, "down", lneg=("may not",)),
                Core("C12.notperm", ("C12",), f"{r} is not permitted to {verb} {obj}", None, NOT(P), 1, "down",
                     lneg=("is not permitted to",))]
    return [Core("DEON.req", (), f"{r} is required to {verb} {obj}", f"Is {r} required to {verb} {obj}", P, 0, "up"),
            Core("DEON.must", (), f"{r} must {verb} {obj}", None, P, 0, "up"),
            Core("C12.neednot", ("C12",), f"{r} need not {verb} {obj}", None, NOT(P), 1, "down", lneg=("need not",)),
            Core("C12.doesnothave", ("C12",), f"{r} does not have to {verb} {obj}", None, NOT(P), 1, "down",
                 lneg=("does not have to",)),
            Core("C12.notreq", ("C12",), f"{r} is not required to {verb} {obj}", None, NOT(P), 1, "down",
                 lneg=("is not required to",))]


# bound words (SEM-08): canonical op per phrase; "count" words only on counts, "amount" words only on amounts
BOUND_POS = {">=": ["at least {n}", "{n} or more"], ">": ["more than {n}", "over {n}", "above {n}"],
             "<=": ["at most {n}", "up to {n}"], "<": ["less than {n}", "under {n}", "below {n}"]}
BOUND_NEGCMP_AMT = {">=": "not less than {n}", "<=": "not more than {n}"}
BOUND_NEGCMP_CNT = {">=": "no fewer than {n}", "<=": "no more than {n}"}
COMPLEMENT = {">=": "<", ">": "<=", "<=": ">", "<": ">="}


def amt_cores(name, subj, op, n, unit, pick=0):
    """A bound claim on one single-valued amount. pick chooses among the synonymous phrases (MR3 swaps them)."""
    P = ["amt", name, subj, op, n]
    i1 = pick % len(BOUND_POS[op])
    ph = BOUND_POS[op][i1].format(n=f"{n} {unit}")
    base = f"the {name} of {subj} is {ph}"
    out = [Core(f"AMT{op}~{BOUND_POS[op][i1].split(' {')[0].replace(' ', '_')}", (), base,
                f"Is the {name} of {subj} {ph}", P, 0, "up")]
    cop = COMPLEMENT[op]
    i2 = pick % len(BOUND_POS[cop])
    cph = BOUND_POS[cop][i2].format(n=f"{n} {unit}")
    out.append(Core(f"C9.compl{cop}~{BOUND_POS[cop][i2].split(' {')[0].replace(' ', '_')}", ("C9",),
                    f"the {name} of {subj} is {cph}", f"Is the {name} of {subj} {cph}",
                    ["amt", name, subj, cop, n], 0, "down", rel="compl"))
    return out


def amt_negcmp_cores(name, subj, op, n, unit):
    """Negated comparison words (k = 1, C9): 'not less than n' (>=) and 'not more than n' (<=)."""
    out = []
    for o, t in BOUND_NEGCMP_AMT.items():
        out.append(Core(f"C9.neg{o}", ("C9",), f"the {name} of {subj} is {t.format(n=f'{n} {unit}')}", None,
                        ["amt", name, subj, o, n], 1, None, lneg=(t.split(" {")[0],), rel="other"))
    return out
