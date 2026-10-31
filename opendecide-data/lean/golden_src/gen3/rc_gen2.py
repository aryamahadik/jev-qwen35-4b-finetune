"""rc_gen2: the gen2_long_policy reuse inside yn2b F1a (yn2b/SPEC.md section 5 F1, "Reuse of gen2_long_policy").

About 1,000 F1 rows use the six gen2_long_policy domain classes (Home, Travel, Lease, Benefits, Grant, Compliance)
with new seeds and the new key. Per the SPEC (and red-team D2) this module imports ONLY the domain classes, the
keyed-variant helper class `V`, the `Reject` class, `evaluate` and `build_state`; it never calls `main()`,
`make_pair()`, `fit_state()` or `append_manifest()`, never imports lean/pg/*, and never writes anything.

Labels: gen2's `evaluate()` runs the class's primary `decide()` and asserts it equals the class's own independent
`decide2()`; every parameter and fact the evaluator reads must be stated in the rendered text (gen2's grounding log),
and every chain clause must survive the length fit. The person names of a sampled case are replaced by yn2b pool
names (SPEC 4.11: invented names, disjoint pools) before anything is rendered. gen2 rows are train-only (the frozen
gen2 organisation lists are not split-disjoint).
"""
from __future__ import annotations

import copy
import difflib
import re
import sys
from pathlib import Path

import mv_core as mv

_GEN = Path(__file__).resolve().parents[1] / "gen"
if str(_GEN) not in sys.path:
    sys.path.append(str(_GEN))
from gen2_long_policy import (Benefits, Compliance, Grant, Home, Lease, Travel, V, Reject as G2Reject,  # noqa: E402
                              build_state, evaluate)

DOMS = {"home": Home(), "travel": Travel(), "lease": Lease(), "benefits": Benefits(), "grant": Grant(),
        "compliance": Compliance()}
DOCNAME = {"home": "policy", "travel": "certificate", "lease": "lease", "benefits": "handbook",
           "grant": "grant agreement", "compliance": "manual"}
AMOUNT_WORD = {"home": "the amount payable on this claim", "travel": "the amount payable on this claim",
               "lease": "the amount returned from the deposit", "benefits": "the amount reimbursed",
               "grant": "the amount reimbursed"}
NAME_KEYS = ("insured", "tenant", "pi", "emp")
MIN_LEN, MAX_LEN = 3000, 12000


def rename(P: dict, C: dict, pool: mv.NamePool, rng) -> dict:
    """Replace the case's person names with pool names (in place). Returns {old: new}."""
    main = pool.person(rng)
    other = pool.person(rng)
    while other.split()[0] == main.split()[0] or other.split()[-1] == main.split()[-1]:
        other = pool.person(rng)
    mp = {}
    for d in (P, C):
        for k in NAME_KEYS:
            if k in d and isinstance(d[k], str):
                mp[d[k]] = main
                d[k] = main
        if "rec" in d and isinstance(d["rec"], str):
            mp[d["rec"]] = other
            d["rec"] = other
        if "first" in d:
            mp[d["first"]] = main.split()[0]
            d["first"] = main.split()[0]
    return mp


def render(dom, P, C, Vx, drop):
    """(state, stated keys, kept paragraph ids, document length) via gen2's build_state."""
    return build_state(dom, P, C, Vx, drop)


def fit_drop(dom, P, C, Vx, lo: int, hi: int, rng) -> set:
    """Drop distractor paragraphs (never one that a kept paragraph references, never one whose section would empty
    out under a section reference) until the state is inside [lo, hi]."""
    doc = dom.doc(P, Vx)
    refs = doc.refs()
    order = list(doc.distractors())
    rng.shuffle(order)
    drop = set()
    s = render(dom, P, C, Vx, drop)[0]
    for pid in order:
        if len(s) <= hi:
            break
        if any(r not in drop for r in refs.get(pid, ())):
            continue
        try:
            s2 = render(dom, P, C, Vx, drop | {pid})[0]
        except KeyError:
            continue
        if len(s2) < lo:
            continue
        drop.add(pid)
        s = s2
    if not (lo <= len(s) <= hi):
        raise mv.Reject("g2_length", f"{len(s)} not in [{lo}, {hi}]")
    return drop


def changed_lines(a: str, b: str) -> int:
    dl = [ln for ln in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
          if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]
    return max(sum(1 for ln in dl if ln.startswith("-")), sum(1 for ln in dl if ln.startswith("+")))


def sample_pair(dom_name: str, rng, pool: mv.NamePool, want_q: str, lo: int, hi: int, seed_tag: str) -> dict:
    """A base case and a fact-flip twin of one gen2 domain (the flip changes the answer of question type want_q:
    outcome | amount | permitted | choice). Raises mv.Reject when the draw does not work."""
    dom = DOMS[dom_name]
    scen = rng.choice(sorted(dom.SCEN))
    try:
        P, C, flips = dom.sample(rng, scen)
    except G2Reject as e:
        raise mv.Reject("g2_sample", str(e)[:40])
    names = rename(P, C, pool, rng)
    try:
        c1, a1, ch1, log1 = evaluate(dom, P, C)
    except G2Reject as e:
        raise mv.Reject("g2_eval", str(e)[:40])
    cands = []
    for fname, ffn in [flips[i] for i in rng.sample(range(len(flips)), len(flips))]:
        P2, C2 = copy.deepcopy(P), copy.deepcopy(C)
        ffn(P2, C2)
        try:
            c2, a2, ch2, log2 = evaluate(dom, P2, C2)
        except G2Reject:
            continue
        if c2 == c1:
            continue
        if want_q == "amount" and a1 == a2:
            continue
        if want_q == "permitted" and (c1 in dom.PERMITTED) == (c2 in dom.PERMITTED):
            continue
        cands.append((fname, P2, C2, c2, a2, ch2, log2))
    if not cands:
        raise mv.Reject("g2_flip", "no flip changes the answer")
    fname, P2, C2, c2, a2, ch2, log2 = cands[0]
    Vx = V(f"yn2b|{seed_tag}")
    drop = fit_drop(dom, P, C, Vx, lo, hi, rng)
    s1, st1, pids1, dl1 = render(dom, P, C, Vx, drop)
    s2, st2, pids2, dl2 = render(dom, P2, C2, Vx, drop)
    for s, st, pids, log, ch in ((s1, st1, pids1, log1, ch1), (s2, st2, pids2, log2, ch2)):
        if log - st:
            raise mv.Reject("g2_grounding", ",".join(sorted(log - st))[:60])
        if not set(ch) <= pids:
            raise mv.Reject("g2_chain", "a chain paragraph was dropped")
        if "[[" in s or "]]" in s:
            raise mv.Reject("g2_ref", "unresolved cross reference")
        if not (MIN_LEN <= len(s) <= MAX_LEN):
            raise mv.Reject("g2_length", str(len(s)))
    if s1 == s2:
        raise mv.Reject("g2_flip", "flip not visible")
    if not 1 <= changed_lines(s1, s2) <= 3:
        raise mv.Reject("g2_flip", "flip changes more than 3 lines")
    for old in names:
        for s in (s1, s2):
            if re.search(r"\b" + re.escape(old) + r"\b", s) and old not in names.values():
                raise mv.Reject("g2_names", "an original name survived")
    return {"dom": dom_name, "scen": scen, "flip": fname, "P": P, "C": C, "P2": P2, "C2": C2,
            "c1": c1, "a1": a1, "c2": c2, "a2": a2, "s1": s1, "s2": s2, "dl1": dl1, "dl2": dl2,
            "names": sorted(set(names.values())), "seed_tag": seed_tag}


def split_doc_file(state: str, dlen: int) -> tuple[str, str]:
    """(document text, claim-file text) of a gen2 state (build_state joins them with one blank line)."""
    return state[:dlen].rstrip("\n"), state[dlen:].lstrip("\n")


def as_json(state: str, dlen: int) -> str:
    d, f = split_doc_file(state, dlen)
    return mv.render_json({"document": [ln for ln in d.split("\n") if ln.strip()],
                           "file": [ln for ln in f.split("\n") if ln.strip()]})


def pick_threshold(rng, lo: int, hi: int):
    """A dollar threshold t with lo <= t < hi (lo is then 'not more than t', hi 'more than t')."""
    lo2 = max(lo, 50)
    if lo2 >= hi:
        return None
    if lo >= 50 and rng.random() < 0.15:
        return lo
    for step in (1000, 500, 250, 100, 50, 10, 1):
        c = [x for x in range(-(-lo2 // step) * step, hi, step) if lo2 <= x < hi]
        if c:
            return rng.choice(c)
    return None
