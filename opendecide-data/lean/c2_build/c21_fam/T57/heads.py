"""Row specs for the four T57 heads, built from a task and its candidate pool (spec level; execution decides the labels).

VERDICT   one patch; CORRECT / INCORRECT, reason head over INCORRECT rows (PARTIAL / REGRESSION / NOFIX).
BEST4     four patches, exactly one CORRECT (>= 30% of the correct options are CAND-ALTFIX).
TESTSEL   four hidden-suite tests: the one that fails before the fix and passes after; three pass both. (Opus C1: the
          module of a TESTSEL row is never used by any other head, nor by T42c / T56g.)
LOCALISE  four functions: the one holding the injected bug (>= 1 traversed by the killing test but unmutated, >= 1 from
          the same file, the rest from other files).
"""
from LC_COMMON import ir as I
from LC_COMMON import render as R
from LC_COMMON import suites

from . import config as C
from .base import Skip
from . import task as TK

LETTERS = "ABCD"


def correct_cands(task):
    return [c for c in task["cands"] if c["cls"] == "CORRECT"]


def incorrect_cands(task):
    return [c for c in task["cands"] if c["cls"] != "CORRECT"]


def pick(cands, rng, kinds=None, avoid=(), ref=None):
    """Random candidate of the cell; with `ref` (a style vector, see _vec) the candidate nearest to it, so VERDICT rows of the two
    labels share one style distribution by construction (matched sampling; K5 / K7 / K8 close at the source)."""
    pool = [c for c in cands if (kinds is None or c["kind"] in kinds) and c["diff"] not in {a["diff"] for a in avoid}]
    if not pool:
        return None
    if ref is None:
        return rng.choice(pool)
    return min(pool, key=lambda c: _dist(_vec(c), ref, _SCALE) + rng.random() * 0.35)


# ----------------------------------------------------------------------------------------------- VERDICT
def verdict_spec_of(task, c):
    return {"head": "VERDICT", "task": task, "cands": [c], "gold_index": None, "label_exp": "CORRECT" if c["cls"] == "CORRECT" else "INCORRECT",
            "reason_exp": None if c["cls"] == "CORRECT" else c["cls"], "options": None}


def verdict_spec(task, rng, want_label, want_reason=None, kinds=None, avoid=(), ref=None):
    """want_label 'CORRECT' | 'INCORRECT'; want_reason in PARTIAL / REGRESSION / NOFIX for INCORRECT."""
    if want_label == "CORRECT":
        c = pick(correct_cands(task), rng, kinds, avoid, ref)
    else:
        pool = incorrect_cands(task)
        if want_reason:
            pool = [c for c in pool if c["cls"] == want_reason]
        c = pick(pool, rng, kinds, avoid, ref)
    if c is None:
        raise Skip("no candidate for the VERDICT cell")
    return {"head": "VERDICT", "task": task, "cands": [c], "gold_index": None, "label_exp": "CORRECT" if c["cls"] == "CORRECT" else "INCORRECT",
            "reason_exp": None if c["cls"] == "CORRECT" else c["cls"], "options": None}


# ----------------------------------------------------------------------------------------------- BEST4
def _short(cands, limit=520):
    """Prefer small diffs: BEST4 shows four of them and the family has a token budget (mean <= 800, <= 10% above 1,024)."""
    s = [c for c in cands if len(c["diff"]) <= limit]
    return s if len(s) >= 1 else cands


_FEAT_KEYS = ("chars", "added", "removed", "hunks", "files", "n_idents", "mean_ident_len", "digits")
_SCALE = [200.0, 2.0, 2.0, 1.0, 1.0, 10.0, 3.0, 3.0]


def _vec(c):
    from .rows import style_feats
    s = style_feats(c)
    return [float(s[k]) for k in _FEAT_KEYS]


def _dist(a, b, scale):
    return sum(abs(x - y) / sc for x, y, sc in zip(a, b, scale))


def best4_spec(task, rng, gold_pos, want_altfix):
    good = _short(correct_cands(task))
    alt = [c for c in good if c["kind"] == "CAND-ALTFIX"]
    inv = [c for c in good if c["kind"] != "CAND-ALTFIX"]
    pool = alt if (want_altfix and alt) else (inv or alt)
    if not pool:
        raise Skip("no correct candidate")
    gold = rng.choice(pool)
    bad = incorrect_cands(task)
    bad = _short(bad) if len(_short(bad)) >= 3 else bad
    if len(bad) < 3:
        raise Skip("not enough incorrect candidates")
    # feature-matched distractors: the three incorrect patches whose style vector is nearest to the gold patch (K6 closes the
    # shortcut at the source; the gap balancer in the planner removes what is left), kinds diversified when there is a tie
    g = _vec(gold)
    vs = [_vec(c) for c in bad]
    scale = [max(1.0, max([abs(v[k] - g[k]) for v in vs] + [1.0])) for k in range(len(g))]
    order = sorted(range(len(bad)), key=lambda i: _dist(g, vs[i], scale) + rng.random() * 1.6)
    picked, kinds_seen = [], set()
    for i in order:
        if bad[i]["kind"] not in kinds_seen or len(order) - order.index(i) <= 3 - len(picked):
            picked.append(bad[i])
            kinds_seen.add(bad[i]["kind"])
        if len(picked) == 3:
            break
    for i in order:
        if len(picked) == 3:
            break
        if bad[i] not in picked:
            picked.append(bad[i])
    others = picked[:]
    rng.shuffle(others)
    opts = others[:gold_pos] + [gold] + others[gold_pos:]
    return {"head": "BEST4", "task": task, "cands": opts, "gold_index": gold_pos, "label_exp": LETTERS[gold_pos],
            "reason_exp": None, "options": None, "altfix": gold["kind"] == "CAND-ALTFIX"}


# ----------------------------------------------------------------------------------------------- LOCALISE
def localise_spec(task, rng, gold_pos):
    lo = task["buggy_lo"]
    bug = task["bug_fn"]
    fns = I.functions(lo)
    allf = [f["name"] for f in lo["funcs"]]
    if len(allf) < 4:
        raise Skip("module has fewer than 4 functions")
    vis = task["visible"]["name"]
    trace = task["trace"][vis]
    traversed = [n for n in trace if n != bug and n in fns]
    same_file = [n for n in allf if n != bug and fns[n]["file"] == fns[bug]["file"]]
    if not traversed or not same_file:
        raise Skip("LOCALISE needs a traversed and a same-file distractor")
    # the gold function is traversed AND in its own file; distractors are drawn to look the same where the module allows it:
    # rank by (traversed and same-file) > traversed > same-file > other, so the flags carry no label information
    rest = [n for n in allf if n != bug]
    rng.shuffle(rest)
    rest.sort(key=lambda n: -((n in trace) + (n in same_file)))
    chosen = rest[:3]
    if not any(n in trace for n in chosen):
        chosen = [traversed[0]] + [n for n in chosen if n != traversed[0]][:2]
    if not any(n in same_file for n in chosen):
        chosen = [same_file[0]] + [n for n in chosen if n != same_file[0]][:2]
    chosen = list(dict.fromkeys(chosen))
    for n in rest:
        if len(chosen) >= 3:
            break
        if n not in chosen:
            chosen.append(n)
    chosen = chosen[:3]
    rng.shuffle(chosen)
    opts = chosen[:gold_pos] + [bug] + chosen[gold_pos:]
    flags = {n: {"traversed": n in trace, "same_file": (n == bug) or n in same_file} for n in opts}
    return {"head": "LOCALISE", "task": task, "cands": [], "gold_index": gold_pos, "label_exp": LETTERS[gold_pos],
            "reason_exp": None, "options": opts,
            "opt_roles": {n: ("GOLD" if n == bug else "TRAVERSED" if n in trace else "SAME_FILE" if n in same_file else "OTHER_FILE") for n in opts},
            "opt_flags": flags}


# ----------------------------------------------------------------------------------------------- TESTSEL
def testsel_spec(task, rng, gold_pos):
    lo, lang = task["ref_lo"], task["lang"]
    fns = I.functions(lo)
    hidden = {c["name"]: c for c in task["hidden"]["cases"]}
    if not task["target"] or len(task["p2p"]) < 3:
        raise Skip("not enough tagged tests")
    gold = rng.choice(task["target"])
    bug = task["bug_fn"]
    p2p = list(task["p2p"])
    rng.shuffle(p2p)
    runs_bug = [n for n in p2p if bug in task["trace"][n]]
    same_file = [n for n in p2p if suites.home_file(lo, hidden[n]) == fns[bug]["file"]]
    # rendered blocks of the gold test and of every pass-to-pass test: distractors are matched to the gold test on what a reader (or a
    # probe) can see without running anything: whether the block names the bug function, its length and line count, and the flags
    allb = {}
    R.render_tests(lo, lang, {"cases": [hidden[n] for n in [gold] + p2p]}, "tmp", blocks=allb)

    def vec(n):
        blk = allb[n]
        return [1.0 if bug in blk else 0.0, len(blk) / 120.0, blk.count("\n") / 3.0, 1.0 if suites.home_file(lo, hidden[n]) == fns[bug]["file"] else 0.0,
                1.0 if bug in task["trace"][n] else 0.0]
    g = vec(gold)
    order = sorted(p2p, key=lambda n: sum(abs(x - y) for x, y in zip(vec(n), g)) + rng.random() * 0.6)
    chosen = order[:3]
    if len(chosen) < 3:
        raise Skip("cannot fill three distractor tests")
    rng.shuffle(chosen)
    opts = chosen[:gold_pos] + [gold] + chosen[gold_pos:]
    fix = [c for c in correct_cands(task)] or []
    if not fix:
        raise Skip("no correct patch to show")
    # which correct patch to show: the plain inverse when available
    fixc = next((c for c in fix if c["kind"] == "CAND-INVERSE"), fix[0])
    blocks = {}
    R.render_tests(lo, lang, {"cases": [hidden[n] for n in opts]}, "tmp", blocks=blocks)
    return {"head": "TESTSEL", "task": task, "cands": [fixc], "gold_index": gold_pos, "label_exp": LETTERS[gold_pos],
            "reason_exp": None, "options": opts, "test_blocks": [blocks[n] for n in opts],
            "opt_roles": {n: ("GOLD" if n == gold else "RUNS_BUG_FN" if n in runs_bug else "SAME_FILE" if n in same_file else "OTHER") for n in opts},
            "opt_flags": {n: {"runs_bug_fn": bug in task["trace"][n], "same_file": suites.home_file(lo, hidden[n]) == fns[bug]["file"]}
                          for n in opts}}
