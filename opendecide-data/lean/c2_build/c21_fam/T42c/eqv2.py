"""EQV2 head: do two implementations give the same observable result on EVERY input of the declared finite domain?

YES = equivalent by a registered construction (EQ-YES-1..5) AND confirmed by an exhaustive run over the domain.
NO  = a concrete distinguishing input found by execution (mutator classes MUT-xx, including hard-NO: the programs differ
      on <= 2% of the declared domain points, so one random probe usually misses it).
The domain is finite, shown in the prompt, and has 25 to 5,000 points. Random testing alone never produces YES.
"""
from LC_COMMON import codeview as V
from LC_COMMON import domain as D
from LC_COMMON import ir as I
from LC_COMMON import irmut
from LC_COMMON import render as R
from LC_COMMON import sampler as SM
from LC_COMMON import transforms as T
from LC_COMMON.interp import Interp

from . import config as C
from .base import Skip, new_base, lower, render_ok, mk_rng, variant


def closure(lo, names):
    fns = I.functions(lo)
    out, stack = set(), list(names)
    while stack:
        n = stack.pop()
        if n in out:
            continue
        out.add(n)
        for _, x in I.walk(fns[n]["body"]):
            if x[0] in ("fcall", "mcall"):
                stack.append(x[1])
    return out


def widen(dom, target, limit=D.MAX_POINTS):
    """Extend contiguous int ranges (x2, x3, ...) until the domain has at least `target` points (never above `limit`)."""
    for k in range(1, 40):
        new = []
        for pd in dom:
            pd = dict(pd)
            if pd["t"] == "int" and len(pd["vals"]) >= 4 and pd["vals"] == list(range(pd["vals"][0], pd["vals"][-1] + 1)):
                lo, hi = pd["vals"][0], pd["vals"][-1]
                pd["vals"] = list(range(lo, lo + (hi - lo + 1) * k))
            new.append(pd)
        n = D.size(new)
        if n > limit:
            return dom
        if n >= target:
            return new
    return dom


def choose_target(lo, lang, rng, prefer_seq, min_size=0):
    """-> {"mode": "pure"|"seq", "fn", "domain" | "seq_domain", "kept": set(names)}"""
    pure = [f["name"] for f in lo["funcs"] if f["scope"] == "free" and lo["meta"]["fns"].get(f["name"], {}).get("domain")
            and D.size(widen(lo["meta"]["fns"][f["name"]]["domain"], min_size) if min_size else lo["meta"]["fns"][f["name"]]["domain"]) >= min_size]
    seq = lo["meta"].get("seq")
    if seq and min_size and D.size({"ops": seq["domain"]["ops"], "maxlen": 5}) < min_size:
        seq = None
    options = []
    if pure:
        options.append("pure")
    if seq:
        options.append("seq")
    if not options:
        raise Skip("no function to compare")
    mode = "seq" if (prefer_seq and "seq" in options) else rng.choice(options)
    if mode == "pure":
        fn = rng.choice(pure)
        dom = lo["meta"]["fns"][fn]["domain"]
        if min_size and D.size(dom) < min_size:
            dom = widen(dom, min_size)
        n = D.size(dom)
        if not D.MIN_POINTS <= n <= D.MAX_POINTS:
            raise Skip("domain size %d" % n)
        return {"mode": "pure", "fn": fn, "domain": dom, "kept": closure(lo, [fn])}
    sd = seq["domain"]
    ops = list(sd["ops"])
    target = rng.choice(ops)
    others = [o for o in ops if o["fn"] != target["fn"]]
    chosen = [target] + (rng.sample(others, 1) if others else [])
    for maxlen in (3, 4, 5, 2):
        dom = {"ops": chosen, "maxlen": maxlen}
        n = D.size(dom)
        if max(D.MIN_POINTS, min_size) <= n <= D.MAX_POINTS:
            kept = closure(lo, [o["fn"] for o in chosen] + [seq["snapshot"]])
            return {"mode": "seq", "fn": target["fn"], "seq_domain": dom, "snapshot": seq["snapshot"], "kept": kept}
    raise Skip("no sequence length gives 25..5000 points")


def point_stream(tgt):
    if tgt["mode"] == "pure":
        for pt in D.enumerate_points(tgt["domain"]):
            yield [{"fn": tgt["fn"], "args": pt}]
    else:
        for seq in D.enumerate_sequences(tgt["seq_domain"]):
            yield [{"fn": c["fn"], "args": c["args"]} for c in seq]


def outcomes(lo, lang, tgt, ref=None, max_diff=None):
    """Per-point canonical outcome list + executed steps per point + dialect events. With `ref` and `max_diff` the scan stops
    (returns None) as soon as more than `max_diff` points differ from `ref` (cheap rejection of hard-NO candidates)."""
    res, steps, events = [], [], set()
    it = Interp(lo, lang)
    snap = tgt.get("snapshot")
    diffs = 0
    for calls in point_stream(tgt):
        it.reset()
        outs = [it.call(c["fn"], c["args"]) for c in calls]
        if tgt["mode"] == "seq":
            outs.append(it.call(snap, []))
        obs = [R.observable_of(lo, lang, o) for o in outs]
        res.append(obs)
        steps.append(it.steps)
        events |= it.events
        if ref is not None and max_diff is not None and obs != ref[len(res) - 1]:
            diffs += 1
            if diffs > max_diff:
                return None
    return res, steps, events


def diff_points(a, b):
    return [k for k, (x, y) in enumerate(zip(a, b)) if x != y]


def _pick_transform_site(base, lo, names, rng, ids, lang, eq, tag):
    names = sorted(names)                 # a set arrives here: its iteration order depends on PYTHONHASHSEED, the shuffle must not
    rng.shuffle(names)
    for n in names:
        try:
            return variant(base, ids, lang, n, eq, rng, tag), n
        except Skip:
            continue
    raise Skip("transform %s applies nowhere in the kept functions" % eq)


def gen_eqv2(cell, seed):
    """cell: {lang, label 'YES'|'NO', eq (EQ-YES id, for YES), op (MUT id) | None, hard(bool), restructured(bool)}"""
    lang, label = cell["lang"], cell["label"]
    rng = mk_rng("EQV2", seed, lang)
    pred = None
    if label == "NO" and cell.get("hard"):
        def pred(m):                                   # hard-NO needs a domain of >= 200 points (widened ranges)
            sizes = [D.size(s["domain"]) for s in m["meta"]["fns"].values() if s.get("domain")]
            seq = m["meta"].get("seq")
            if seq:
                sizes.append(D.size(seq["domain"]))
            return bool(sizes)
    base, ids = new_base("e%s" % seed, lang, pred=pred)
    lo = lower(base, lang, ids)
    render_ok(lo, lang)
    tgt = choose_target(lo, lang, rng, cell.get("seq", False), 200 if (label == "NO" and cell.get("hard")) else 0)
    ref, steps_a, ev = outcomes(lo, lang, tgt)
    if ev:
        raise Skip("non-portable domain run: %s" % sorted(ev))
    n_points = len(ref)
    info = {}
    if label == "YES":
        chain = [cell["eq"]]
        cur_base, cur_lo = base, lo
        for k, eq in enumerate(chain + ([rng.choice(T.IDS)] if rng.random() < 0.3 else [])):
            (cur_base, cur_lo, vi), where = _pick_transform_site(cur_base, cur_lo, tgt["kept"], rng, ids, lang, eq, "ty%d" % k)
            info.setdefault("chain", []).append({"id": eq, "fn": where})
        got, steps_b, ev2 = outcomes(cur_lo, lang, tgt)
        if ev2 or got != ref:
            raise Skip("YES construction disagrees with the interpreter")
        mod_b, lo_b = cur_base, cur_lo
        info.update({"label_kind": "YES", "construction": cell["eq"], "distinguishing": None, "diff_fraction": 0.0})
    else:
        cur_base, cur_lo = base, lo
        if cell.get("restructured"):
            eq = rng.choice(T.IDS)
            try:
                (cur_base, cur_lo, vi), where = _pick_transform_site(base, lo, tgt["kept"], rng, ids, lang, eq, "tr")
                info["pre_transform"] = {"id": eq, "fn": where}
            except Skip:
                pass
        ops = list(irmut.ALL_OPS)
        rng.shuffle(ops)
        if cell.get("hard"):                          # tiny-difference mutants come from boundary/constant edits first
            first = [o for o in ("MUT-02", "MUT-04", "MUT-09", "MUT-13", "MUT-12", "MUT-11") if o in ops]
            ops = first + [o for o in ops if o not in first]
        if cell.get("op") in ops and (not cell.get("hard") or cell["op"] in ("MUT-02", "MUT-04")):
            ops.remove(cell["op"])                     # the planner's class is a preference, not a requirement
            ops.insert(0, cell["op"])
        budget = 90                                    # mutants evaluated per candidate (cost bound)
        found = None
        for op in ops:
            sites = irmut.enumerate_sites(cur_base, [op], tgt["kept"])
            rng.shuffle(sites)
            for site in sites[:30]:
                if budget <= 0:
                    break
                budget -= 1
                try:
                    mb, mlo, vi = variant(cur_base, ids, lang, None, site, rng, "tm")
                except Skip:
                    continue
                scan = outcomes(mlo, lang, tgt, ref, int(C.HARD_NO_MAX_DIFF * n_points) if cell.get("hard") else None)
                if scan is None:
                    continue                                   # already above the hard-NO difference budget
                got, steps_b, ev2 = scan
                if ev2:
                    continue
                d = diff_points(ref, got)
                frac = len(d) / n_points
                if not d:
                    continue                                   # equivalent mutant: never labelled NO
                if cell.get("hard") and (frac > C.HARD_NO_MAX_DIFF or n_points < 50):
                    continue
                if not cell.get("hard") and frac <= C.HARD_NO_MAX_DIFF:
                    continue
                found = (site, mb, mlo, vi, d, frac, steps_b)
                break
            if found or budget <= 0:
                break
        if not found:
            raise Skip("no mutant satisfies the NO cell")
        site, mod_b, lo_b, vi, d, frac, steps_b = found
        first = d[0]
        pts = list(point_stream(tgt))
        info.update({"label_kind": "NO", "mutator_op": site["op"], "site": {"fn": site["fn"], "path": site["path"], "variant": site["variant"]},
                     "distinguishing": pts[first], "diff_fraction": frac, "hard_no": frac <= C.HARD_NO_MAX_DIFF})
    pts_all = list(point_stream(tgt))
    k_rep = max(range(len(steps_a)), key=lambda k: steps_a[k])
    rep_point = pts_all[k_rep]
    rep_steps = (steps_a[k_rep] + steps_b[k_rep]) / 2.0
    swap = rng.random() < 0.5
    progs = [("A", lo), ("B", lo_b)] if not swap else [("A", lo_b), ("B", lo)]
    shown = []
    for name, m in progs:
        pr = V.prune_module(m, tgt["kept"])
        blocks = V.src_blocks(pr, lang)
        shown.append({"name": name, "blocks": blocks, "text": V.src_text(blocks)})
    if shown[0]["blocks"] == shown[1]["blocks"]:
        # build-review fix 18 Oct: a transform that only touched code outside the shown slice leaves two identical programs;
        # "identical text" would then be a pure YES cue (no NO row can have identical programs)
        raise Skip("the two shown programs are textually identical")
    sim = V.token_jaccard(shown[0]["text"], shown[1]["text"])
    spec = {
        "head": "EQV2", "lang": lang, "seed": seed, "cell_seq": bool(cell.get("seq", False)), "base": base, "ids": ids, "lo": lo, "lo_b": lo_b, "swap": swap,
        "target": tgt, "domain_text": D.describe(tgt["domain"] if tgt["mode"] == "pure" else tgt["seq_domain"]),
        "domain_size": n_points, "gold_label": label, "shown": shown, "info": info,
        "steps_ir": rep_steps, "rep_point": rep_point, "points": pts_all,
        "meta": {"similarity": sim, "stateful": tgt["mode"] == "seq", "cdom": lo["meta"]["cdom"], "n_files": len(lo["files"]),
                 "pair_id": None, "pair_kind": None, "construction": info.get("construction"),
                 "shown_chars": len(shown[0]["text"]) + len(shown[1]["text"]),
                 "mutator_op": info.get("mutator_op"), "hard_no": info.get("hard_no", False),
                 "ast_nodes_a": I.size_metrics(progs[0][1])["nodes"], "ast_nodes_b": I.size_metrics(progs[1][1])["nodes"],
                 "changed_lines": V.changed_lines(shown[0]["text"], shown[1]["text"]),
                 "edit_ratio": V.edit_ratio(shown[0]["text"], shown[1]["text"]), "len_ratio": len(shown[0]["text"]) / max(1, len(shown[1]["text"]))},
    }
    spec["bin_ir"] = SM.step_bin(spec["steps_ir"])
    return spec


def make_pair(spec, kind, seed):
    """Partner EQV2 row from the same base program: 'invariant' = a second YES with another transform of the same
    function; 'nearmiss' = a NO row whose B is a one-token mutant of the same A."""
    cell_lang = spec["lang"]
    cseq = spec["cell_seq"]
    rng = mk_rng("EQV2pair", seed, kind)
    if spec["gold_label"] == "YES" and kind == "nearmiss":
        cell = {"lang": cell_lang, "label": "NO", "op": None, "hard": False, "seq": cseq}
    elif spec["gold_label"] == "YES":
        cell = {"lang": cell_lang, "label": "YES", "seq": cseq,
                "eq": rng.choice([e for e in T.IDS if e != spec["meta"]["construction"]] or list(T.IDS))}
    elif kind == "nearmiss":
        cell = {"lang": cell_lang, "label": "YES", "eq": rng.choice(T.IDS), "seq": cseq}
    else:
        raise Skip("invariant pair needs a YES row")
    # same base module seed => same A program; the partner differs only in B
    new = gen_eqv2(cell, seed)
    return new
