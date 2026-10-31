"""Shared definitions and item helpers for the hard 'nli_a' domain (v0.11 HARD track).

Domain: inference with negation scope and quantifiers. Each family ("minimal set") is one base
passage/statement pair whose negation is moved around (premise, statement, both, over a quantifier,
inside an embedded clause, affixal un-/in-/non-, lexical fail/lack/deny/without/except/unless/until)
so that some moves change the answer and some do not.

All people, organisations, products and places are invented. Authored by the teacher (Claude);
no external model or dataset is used.
"""

FOLLOW = "follows from the passage"
NOTNEC = "does not necessarily follow"
CONTRA = "contradicted by the passage"
OPEN = "left open by the passage"

DEF_F = ("the statement must be true in every situation consistent with the passage. Take what the passage "
         "asserts as true and read it literally, with ordinary word meanings and any definitions the passage "
         "gives. Facts the passage takes for granted count (\"the tenant did not renew her lease\" takes for "
         "granted that she had one), but guesses, likely readings and hints do not, and a report that someone "
         "said, believed or denied something establishes only that they said, believed or denied it.")
DEF_N = ("there is at least one situation consistent with the passage in which the statement is false; this "
         "includes statements that the passage rules out.")
DEF_C = "the statement is false in every situation consistent with the passage."
DEF_O = ("the passage allows situations in which the statement is true and also situations in which it is "
         "false.")

CARD_YN = f"- {FOLLOW}: {DEF_F}\n- {NOTNEC}: {DEF_N}"
L3 = {"F": FOLLOW, "C": CONTRA, "O": OPEN}
D3 = {FOLLOW: DEF_F, CONTRA: DEF_C, OPEN: DEF_O}


def Y(fam, q, passage, stmt, gold, diff, lab="Statement", twin=None, role="aff"):
    """Yes/no item. gold 1 = yes. twin = (subs, new_gold[, new_q])."""
    assert gold in (0, 1)
    return dict(kind="yn", fam=fam, q=q, passage=passage, stmt=stmt, lab=lab, gold=gold, diff=diff,
                twin=twin, role=role)


def C3(fam, q, passage, stmt, gold, diff, lab="Statement", twin=None):
    """Three-way: gold in 'F' (follows), 'C' (contradicted), 'O' (left open)."""
    assert gold in L3
    return dict(kind="c3", fam=fam, q=q, passage=passage, stmt=stmt, lab=lab, gold=gold, diff=diff, twin=twin)


def SC(fam, q, passage, stmts, gold, diff, head="Numbered statements:", twin=None):
    """Which numbered statement follows. gold = 1-based index into stmts as written, 0 = none of these."""
    assert 0 <= gold <= len(stmts)
    return dict(kind="sc", fam=fam, q=q, passage=passage, stmts=stmts, gold=gold, diff=diff, head=head,
                twin=twin)


def CNT(fam, q, passage, stmts, n, diff, head="Numbered statements:", twin=None):
    """How many numbered statements follow. n = count."""
    assert 0 <= n <= len(stmts)
    return dict(kind="cnt", fam=fam, q=q, passage=passage, stmts=stmts, gold=n, diff=diff, head=head, twin=twin)


def SUB(fam, q, passage, stmts, gold, diff, head="Numbered statements:", twin=None):
    """Which exact set of numbered statements follows. gold = tuple of 1-based indices as written."""
    return dict(kind="sub", fam=fam, q=q, passage=passage, stmts=stmts, gold=tuple(sorted(gold)), diff=diff,
                head=head, twin=twin)


def ENT(fam, q, passage, opts, gold, diff, twin=None, follow_line=True):
    """Choice among named options. opts = [(label, definition)], gold = label."""
    labels = [o for o, _ in opts]
    assert gold in labels, (gold, labels)
    return dict(kind="ent", fam=fam, q=q, passage=passage, opts=opts, gold=gold, diff=diff, twin=twin,
                follow_line=follow_line)
