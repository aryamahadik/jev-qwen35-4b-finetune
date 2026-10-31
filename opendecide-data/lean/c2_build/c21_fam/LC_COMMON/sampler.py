"""Call sampling over (scaled-up) declared domains. Used by T42c OUT4 (long traces) and by suite builders."""
from . import domain as D
from . import interp as X

TIER_SCALE = {"lt10": (1, 1), "mid": (1, 3), "gt40": (3, 8)}


def sample_param(pd, rng, scale=1, max_list=24):
    t = pd["t"]
    if t == "int":
        lo, hi = min(pd["vals"]), max(pd["vals"])
        if scale > 1 and hi - lo >= 3:
            hi = lo + (hi - lo + 1) * scale - 1
        return rng.randint(lo, hi)
    if t == "str":
        return rng.choice(pd["vals"])
    if t == "bool":
        return rng.choice([False, True])
    n = rng.randint(0, min(max_list, max(1, pd["maxlen"] * scale)))
    return [rng.choice(pd["elem"]) for _ in range(n)]


def sample_args(dom, rng, scale=1):
    return [sample_param(pd, rng, scale) for pd in dom]


def sample_sequence(seq_dom, rng, n_calls, scale=1):
    out = []
    for _ in range(n_calls):
        op = rng.choice(seq_dom["ops"])
        out.append({"fn": op["fn"], "args": sample_args(op["params"], rng, scale)})
    return out


def run_calls(mod, lang, calls):
    """Execute calls through the IR interpreter on a fresh instance. Returns (outcomes, interp)."""
    it = X.Interp(mod, lang)
    outs = [it.call(c["fn"], c["args"]) for c in calls]
    return outs, it


def step_bin(steps):
    if steps < 10:
        return "lt10"
    if steps <= 40:
        return "mid"
    return "gt40"


def portable(it):
    """No dialect event happened (no out-of-range index, no negative index, no big integers)."""
    return not it.events


def explicit_outcome(out):
    """True for ("ok", v) and for explicit ERR_* exceptions; False for implicit ones (IMP_*)."""
    return out[0] == "ok" or not str(out[1]).startswith("IMP_")
