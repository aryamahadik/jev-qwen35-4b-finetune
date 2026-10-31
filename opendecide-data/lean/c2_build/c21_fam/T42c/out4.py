"""OUT4 head: which of four listed outcomes (an output value or an exception class) does this call produce?

Spec expectation = IR interpreter in the target language's dialect; the sandbox witness decides the label.
Distractor kinds (G0-lite section 1): EXEC-NEARMISS (executed output of a one-token mutant), ARITH-PERTURB (gold shifted by
a small rule), EXC-SIBLING (another class from the closed per-language list).
"""
from LC_COMMON import codeview as V
from LC_COMMON import ir as I
from LC_COMMON import irmut, modgen
from LC_COMMON import render as R
from LC_COMMON import sampler as SM
from LC_COMMON import transforms as T
from LC_COMMON.interp import Interp

from . import config as C
from .base import Skip, new_base, lower, render_ok, mk_rng, variant, custom_error_flag

KINDS = ("EXEC-NEARMISS", "ARITH-PERTURB", "EXC-SIBLING")
EXTRA_KIND_WEIGHTS = (("EXEC-NEARMISS", 0.25), ("ARITH-PERTURB", 0.40), ("EXC-SIBLING", 0.35))


def _wchoice(rng, pairs):
    r, acc = rng.random(), 0.0
    for k, w in pairs:
        acc += w
        if r < acc:
            return k
    return pairs[-1][0]


def pick_call_plan(lo, lang, rng, want_exc, want_bin, tries=120):
    """-> (calls, outcomes, interp) or None. Prefix calls must succeed; only explicit outcomes; portable runs only."""
    fns = lo["funcs"]
    pure = [f for f in fns if f["scope"] == "free"]
    seq_dom = (lo["meta"].get("seq") or {}).get("domain")
    for t in range(tries):
        lo_s, hi_s = SM.TIER_SCALE[want_bin]
        scale = rng.randint(lo_s, hi_s)
        if seq_dom and (not pure or rng.random() < 0.6):
            n = rng.randint(1, 2 + scale)
            calls = SM.sample_sequence(seq_dom, rng, n, scale)
        else:
            f = rng.choice(pure) if pure else None
            if f is None:
                continue
            dom = lo["meta"]["fns"][f["name"]]["domain"]
            calls = [{"fn": f["name"], "args": SM.sample_args(dom, rng, scale)}]
        outs, it = SM.run_calls(lo, lang, calls)
        if any(o[0] == "exc" for o in outs[:-1]):
            continue
        final = outs[-1]
        if not SM.portable(it) or not SM.explicit_outcome(final):
            continue
        if want_exc != (final[0] == "exc"):
            continue
        ty = I.functions(lo)[calls[-1]["fn"]]["ret"]
        if final[0] == "ok" and ty not in (I.INT, I.STR, I.INTS, I.STRS):
            continue
        if SM.step_bin(it.steps) != want_bin:
            continue
        return calls, outs, it
    return None


# ----------------------------------------------------------------------------------------------- distractors
def _obs_key(obs):
    return I.canon(obs)


def nearmiss_pool(base, ids, lo, lang, calls, gold_obs, rng, want=6):
    """Executed (interpreter-predicted) outputs of one-token mutants of the module for the same calls."""
    out, seen = [], {_obs_key(gold_obs)}
    for site, mm in irmut.mutants(base, irmut.ALL_OPS, rng=rng, limit=60):
        try:
            mlo = lower(mm, lang, ids)
        except Skip:
            continue
        outs, it = SM.run_calls(mlo, lang, calls)
        o = outs[-1]
        if not SM.portable(it) or not SM.explicit_outcome(o):
            continue
        obs = R.observable_of(mlo, lang, o)
        k = _obs_key(obs)
        if k in seen:
            continue
        seen.add(k)
        out.append({"obs": obs, "site": site, "steps": it.steps})
        if len(out) >= want:
            break
    return out


def _prefix_raises(outs):
    """OUT4 shows the earlier calls as bare statements: if one of them raised, the script would end before the final call."""
    return any(o[0] == "exc" for o in outs[:-1])


def overlap_flag(obs, src_text):
    """K7 literal-overlap feature: does the option's value (or exception class name) occur in the shown source?"""
    lit = str(obs["ok"]) if "ok" in obs else obs.get("exc", "")
    return bool(lit) and lit in src_text


def _perturb_cands(obs, ty, rng):
    """ARITH-PERTURB candidates: the gold value shifted by a small rule (many rules, so gold is not always the middle)."""
    if "ok" not in obs:
        return []
    v = obs["ok"]
    if ty == I.INT:
        ks = [k for k in range(-12, 13) if k]
        c = [v + k for k in ks] + [v * 2, v * 3, v // 2, v + 100, -v if v else 7]
    elif ty == I.STR:
        c = [v[:-1] if len(v) > 1 else v + "x", v + "x", (v[:-1] + ("a" if not v.endswith("a") else "b")) if v else "x",
             "x" + v, v[1:] if len(v) > 1 else v + "y"]
    else:
        c = [v[:-1], v + [v[-1] + 1 if v else 1], [x + 1 for x in v] if v else [1], list(reversed(v)) if len(v) > 1 else v + [0],
             v[1:], [x + 2 for x in v] if v else [2]]
    out = []
    for x in c:
        if x != v and I.canon(x) not in {I.canon(y) for y in out}:
            out.append(x)
    rng.shuffle(out)
    return [{"ok": x} for x in out]


def _sibling_cands(lo, lang, ids, rng):
    """EXC-SIBLING candidates: other classes of the module itself (they occur in the source) and classes from the closed
    per-language list; the caller picks by the overlap flag it wants."""
    from LC_COMMON import modgen as M
    own = []
    for info in lo["errors"].values():
        own.append({"python": info["python"], "javascript": info["javascript"], "typescript": info["javascript"],
                    "go": info["go"], "bash": "exit:%d" % info["bash"]}[lang])
    if lang == "python":
        pool = list(M.PY_ERR_CLOSED)
    elif lang in ("javascript", "typescript"):
        pool = list(M.JS_ERR_CLOSED)
    elif lang == "go":
        pool = [ids.typename("sib.%d" % k) for k in range(4)]
    else:
        pool = ["exit:%d" % (64 + k) for k in range(0, 60)]
    rng.shuffle(own)
    rng.shuffle(pool)
    seen, out = set(), []
    for n in own + pool:
        if n not in seen:
            seen.add(n)
            out.append({"exc": n})
    return out


def _choose(cands, avoid, src_text, want_overlap, rng):
    ok = [c for c in cands if _obs_key(c) not in avoid]
    if not ok:
        return None
    pref = [c for c in ok if overlap_flag(c, src_text) == want_overlap]
    return (pref or ok)[0]


def build_options(lo, base, ids, lang, calls, gold_obs, ret_ty, rng, src_text="", want_kinds=None):
    """Gold + 3 distractors with kinds recorded. Returns list of option dicts (gold first, unshuffled).
    Literal overlap (K7) is decorrelated from the role: each distractor's overlap flag is drawn iid fair when possible."""
    avoid = {_obs_key(gold_obs)}
    pool = nearmiss_pool(base, ids, lo, lang, calls, gold_obs, rng)
    if not pool:
        raise Skip("no executable near-miss distractor")
    kinds = want_kinds or (["EXEC-NEARMISS"] + [_wchoice(rng, EXTRA_KIND_WEIGHTS) for _ in range(2)])
    opts = [{"obs": gold_obs, "kind": "GOLD", "mutant": None}]
    used_pool = 0
    for kind in kinds:
        o, mutant = None, None
        gold_flag = overlap_flag(gold_obs, src_text)
        want = gold_flag if rng.random() < 0.9 else (not gold_flag)         # keep the overlap flag uninformative
        order = [kind] + [k for k in rng.sample(KINDS, len(KINDS)) if k != kind]
        for alt in order:
            if alt == "EXEC-NEARMISS":
                rest = [p for p in pool[used_pool:] if _obs_key(p["obs"]) not in avoid]
                if rest:
                    pref = [p for p in rest if overlap_flag(p["obs"], src_text) == want]
                    pick = (pref or rest)[0]
                    pool.remove(pick)
                    o, mutant, kind = pick["obs"], pick["site"], alt
                    break
            elif alt == "ARITH-PERTURB":
                src = gold_obs if "ok" in gold_obs else next((p["obs"] for p in pool if "ok" in p["obs"]), None)
                if src is not None:
                    o = _choose(_perturb_cands(src, ret_ty if "ok" in gold_obs else I.INT, rng), avoid, src_text, want, rng)
                    if o is not None:
                        kind = alt
                        break
            else:
                o = _choose(_sibling_cands(lo, lang, ids, rng), avoid, src_text, want, rng)
                if o is not None:
                    kind = alt
                    break
        if o is None:
            raise Skip("could not build 3 distinct distractors")
        avoid.add(_obs_key(o))
        opts.append({"obs": o, "kind": kind, "mutant": mutant})
    return opts


def place_options(opts, gold_pos, rng, rows_seed=None):
    """Shuffle so that gold sits at `gold_pos` (0-3); other options in random order."""
    others = opts[1:]
    rng.shuffle(others)
    out = others[:gold_pos] + [opts[0]] + others[gold_pos:]
    return out


# ----------------------------------------------------------------------------------------------- the head
def gen_out4(cell, seed):
    """cell: {lang, exc(bool), bin, gold_pos(0..3), custom(bool)} -> spec dict. Raises Skip."""
    lang = cell["lang"]
    rng = mk_rng("OUT4", seed, lang)
    custom = bool(cell.get("custom"))
    def pred(m):
        if cell["exc"] and len(m["errors"]) < 2:
            return False                                   # a single raised class would give the answer away
        if cell["bin"] == "gt40" and not (m["cls"] or I.size_metrics(m)["loops"] > 0):
            return False                                   # a long trace needs a loop or state
        return True

    base, ids = new_base("o%s" % seed, lang, pred=pred, custom_errors=custom)
    lo = lower(base, lang, ids)
    render_ok(lo, lang)
    plan = pick_call_plan(lo, lang, rng, cell["exc"], cell["bin"])
    if plan is None:
        raise Skip("no call satisfies the cell")
    calls, outs, it = plan
    final = outs[-1]
    gold_obs = R.observable_of(lo, lang, final)
    ret_ty = I.functions(lo)[calls[-1]["fn"]]["ret"]
    shown_src = V.src_text(V.src_blocks(V.prune_module(lo, {c["fn"] for c in calls}), lang))
    opts = build_options(lo, base, ids, lang, calls, gold_obs, ret_ty, rng, src_text=shown_src)
    opts = place_options(opts, cell["gold_pos"], rng)
    for o in opts:
        o["text"] = V.option_text(o["obs"], ret_ty, lo, lang)
    if len({o["text"] for o in opts}) != 4:
        raise Skip("duplicate option text")
    spec = {
        "shown_src": shown_src,
        "head": "OUT4", "lang": lang, "seed": seed, "base": base, "ids": ids, "lo": lo, "origin_base": base, "origin_lo": lo,
        "calls": calls, "ret_type": ret_ty, "gold_obs": gold_obs, "options": opts,
        "gold_index": [i for i, o in enumerate(opts) if o["kind"] == "GOLD"][0],
        "steps_ir": it.steps, "bin_ir": SM.step_bin(it.steps),
        "meta": {"exc_gold": final[0] == "exc", "custom_exc": bool(custom and final[0] == "exc"
                                                                    and lo["errors"].get(final[1], {}).get("python_custom")),
                 "distractor_kinds": [o["kind"] for o in opts if o["kind"] != "GOLD"],
                 "stateful": lo["cls"] is not None, "n_calls": len(calls), "cdom": lo["meta"]["cdom"],
                 "n_files": len(lo["files"]), "pair_id": None, "pair_kind": None},
    }
    return spec


# ----------------------------------------------------------------------------------------------- pairs
def make_pair(spec, kind, seed):
    """Partner row for an OUT4 spec: 'invariant' (equivalent rewrite, same gold) or 'nearmiss' (mutant whose output is
    one of this row's own EXEC-NEARMISS distractors: the old gold becomes a distractor). Raises Skip."""
    lang, base, ids, lo = spec["lang"], spec["base"], spec["ids"], spec["lo"]
    rng = mk_rng("OUT4pair", seed, kind)
    if kind == "nearmiss":
        cands = [o for o in spec["options"] if o["kind"] == "EXEC-NEARMISS" and o["mutant"] is not None]
        if not cands:
            raise Skip("no near-miss distractor to pair with")
        pick = rng.choice(cands)
        mbase, mlo, info = variant(base, ids, lang, None, pick["mutant"], rng, "pm")
        outs, it = SM.run_calls(mlo, lang, spec["calls"])
        if _prefix_raises(outs):
            raise Skip("near-miss mutant makes an earlier call raise")      # the earlier calls run bare: the script would stop there
        o = R.observable_of(mlo, lang, outs[-1])
        if o != pick["obs"]:
            raise Skip("mutant prediction mismatch")
        new = dict(spec)
        new["base"], new["lo"] = mbase, mlo
        new["gold_obs"] = o
        opts = []
        for x in spec["options"]:
            y = dict(x)
            y["kind"] = "GOLD" if x is pick else ("PAIR-OLD-GOLD" if x["kind"] == "GOLD" else x["kind"])
            opts.append(y)
        new["options"] = opts
        new["gold_index"] = [i for i, x in enumerate(opts) if x["kind"] == "GOLD"][0]
        new["steps_ir"], new["bin_ir"] = it.steps, SM.step_bin(it.steps)
        new["meta"] = dict(spec["meta"], pair_kind="nearmiss", mutator_op=info["op"],
                           distractor_kinds=[x["kind"] for x in opts if x["kind"] != "GOLD"],
                           exc_gold="exc" in o, variant_info=info)
        return new
    # invariant: transform a function on the executed path
    path_fns = sorted({c["fn"] for c in spec["calls"]})
    rng.shuffle(path_fns)
    for fn_name in path_fns:
        for eq in rng.sample(list(T.IDS), len(T.IDS)):
            try:
                tb, tlo, info = variant(base, ids, lang, fn_name, eq, rng, "pi")
            except Skip:
                continue
            outs, it = SM.run_calls(tlo, lang, spec["calls"])
            if _prefix_raises(outs) or R.observable_of(tlo, lang, outs[-1]) != spec["gold_obs"] or not SM.portable(it):
                continue
            new = dict(spec)
            new["base"], new["lo"] = tb, tlo
            new["steps_ir"], new["bin_ir"] = it.steps, SM.step_bin(it.steps)
            new["meta"] = dict(spec["meta"], pair_kind="invariant", construction=eq, variant_info=info)
            return new
    raise Skip("no equivalent rewrite applies on the executed path")


def permuted_copy(spec, rng):
    """Order-invariance copy: same content, random NON-IDENTITY permutation of the options."""
    n = len(spec["options"])
    for _ in range(50):
        perm = list(range(n))
        rng.shuffle(perm)
        if perm != list(range(n)):
            break
    new = dict(spec)
    new["options"] = [spec["options"][k] for k in perm]
    new["gold_index"] = [i for i, o in enumerate(new["options"]) if o["kind"] == "GOLD"][0]
    new["meta"] = dict(spec["meta"], perm_copy=True, perm=perm)
    return new
