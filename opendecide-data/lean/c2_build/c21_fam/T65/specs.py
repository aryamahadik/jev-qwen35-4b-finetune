"""T65 spec building (twin pairs), canary witnesses and ladder flags.

A twin pair has the same scenario, names and layout; the YES member carries the flaw (no neutralising step, or a DECOY DS-1..DS-6), the NO member differs by the one
token, argument, position or line that repairs it (or is a NO-HARD kind NS-1..NS-4). The execution witness (dynamic classes only; the label is NOT taken from it
alone) runs the function with a REGISTERED canary payload and a benign input through the executor (3 identical runs): YES iff the canary effect is observed,
NO iff it is not, anything else is dropped. Static-only classes (295 / 327 / 377) have no witness: their independent engine is solver B (an AST pattern engine).
"""
import copy
import difflib
import json

from LP_COMMON import plan as plan_mod
from LP_COMMON import sandbox_iface as S
from LP_COMMON.ns import Names

from . import config as C
from . import templates as T


class Reject(Exception):
    pass


class Pool(object):
    def __init__(self, names):
        self.names, self.k = names, 0

    def _u(self, slot):
        self.k += 1
        return self.names.unique(slot, "id%d" % self.k)

    def fn(self):
        return self._u("ns.mcp_tool")

    def var(self):
        return self._u("ns.variable")

    def const(self):
        return self._u("ns.envvar")

    def word(self):
        return self._u("ns.noun.entity").lower()

    def stem(self):
        return self._u("ns.noun.module")

    def alt_of(self, name):
        """A name differing from `name` by exactly one character (DS-1: the wrong variable)."""
        for i in range(len(name) - 1, 0, -1):
            for ch in "aeioulnrst":
                cand = name[:i] + ch + name[i + 1:]
                if cand != name:
                    return cand
        raise Reject("alt name")


def after_transforms(cls, value, transforms):
    """The benign value as the sink sees it (host-side mirror of the rendered transforms): the allow-list must contain it."""
    for t in transforms:
        if t == "strip":
            value = value.strip()
        elif t == "lower":
            value = value.lower()
        elif t == "fmt":
            value = {"CWEC-22": "./" + value, "CWEC-601": value + "#top"}.get(cls, "item " + value)
    return value


NOISE = {"CWEC-22": ("html", 'html.escape("{w}")'), "CWEC-78": ("html", 'html.escape("{w}")'), "CWEC-79": ("shlex", 'shlex.quote("{w}")'),
         "CWEC-89": ("html", 'html.escape("{w}")'), "CWEC-117": ("shlex", 'shlex.quote("{w}")'), "CWEC-601": ("html", 'html.escape("{w}")')}


def base_spec(cls, pool, rng, transforms, noise):
    nm = {"fn": pool.fn(), "param": pool.var(), "box": pool.var(), "msg": pool.word(), "h1": pool.fn(), "h2": pool.fn(), "noisevar": pool.var()}
    nm["chain"] = [pool.var() for _ in range(len(transforms) + 1)]
    nm["alt"] = pool.alt_of(nm["chain"][-1])
    spec = {"cls": cls, "source": "param", "transforms": list(transforms), "names": nm, "neut": None, "consts": {"root": pool.const(), "allowed": pool.const(), "config": pool.const()},
            "w": [pool.var() for _ in range(3)], "allowed": [], "config_value": C.BENIGN[cls], "noise": None, "lang": "python"}
    if noise:
        mod, expr = NOISE[cls]
        spec["noise"] = {"mod": mod, "expr": expr.format(w=pool.word())}
    if cls in C.DYNAMIC:
        spec["allowed"] = [after_transforms(cls, C.BENIGN[cls], transforms), pool.word()]
    return spec


def static_spec(cls, pool, rng):
    nm = {"fn": pool.fn(), "param": "password" if cls == "CWEC-327" else pool.var(), "ctx": pool.var(), "alt": None, "h1": pool.fn(), "h2": pool.fn(), "salt": pool.const(),
          "salt_word": pool.word(), "h": pool.var(), "path": pool.var(), "fd": pool.var(), "dir": pool.var(), "fixed": pool.word()}
    nm["alt"] = pool.alt_of(nm["ctx"] if cls == "CWEC-295" else nm["h"] if cls == "CWEC-327" else nm["path"])
    return {"cls": cls, "role": "password" if cls == "CWEC-327" else "other", "flagged": True, "neut": None, "names": nm, "lang": "python", "source": "param"}


def ds_pair(spec, ds, rng):
    """(yes_spec, no_spec) for a decoy kind. The NO member is the repaired twin."""
    yes, no = copy.deepcopy(spec), copy.deepcopy(spec)
    n = rng.randint(5, 9)                                  # the branch sanitises SHORT values only: a canary payload (>= 11 characters) takes the other branch
    yes["neut"] = {"san": {"DS-1": "wrong_var", "DS-2": "wrong_class", "DS-3": "after_sink", "DS-4": "branch", "DS-5": "discarded", "DS-6": "overwritten"}[ds], "n": n}
    if ds == "DS-1":
        no["neut"] = {"san": "valid", "form": "copy" if spec["cls"] in C.DYNAMIC else "alt"}
    elif ds == "DS-6":
        no["neut"] = {"san": "valid", "form": "copy1" if spec["cls"] in C.DYNAMIC else "direct"}
    else:
        no["neut"] = {"san": "valid", "form": "direct"}
    return yes, no


def ns_pair(spec, ns, rng):
    yes, no = copy.deepcopy(spec), copy.deepcopy(spec)
    cls = spec["cls"]
    if ns == "NS-1":
        yes["neut"] = {"san": "helper", "identity": True}
        no["neut"] = {"san": "helper"}
    elif ns == "NS-2":
        no["neut"] = {"san": "allowlist"}
    elif ns == "NS-3":
        if cls in C.DYNAMIC:
            no["source"] = "const"
        elif cls == "CWEC-327":
            no["role"] = "other"
            no["names"]["param"] = "filename"
        else:
            no["flagged"] = False
    elif ns == "NS-4":
        no["neut"] = {"san": "param_api"}
    else:
        raise Reject(ns)
    return yes, no


def build_pair(cls, cell, pool, rng):
    transforms = cell["transforms"]
    spec = static_spec(cls, pool, rng) if cls in C.STATIC else base_spec(cls, pool, rng, transforms, cell.get("noise", False))
    kind = cell["pair_kind"]
    if kind == "plain":
        yes, no = copy.deepcopy(spec), copy.deepcopy(spec)
        no["neut"] = {"san": "valid", "form": "direct"}
    elif kind.startswith("decoy:"):
        yes, no = ds_pair(spec, kind.split(":")[1], rng)
    else:
        ns = kind.split(":")[1]
        if ns in ("NS-2", "NS-4") and cls in C.STATIC:
            raise Reject("%s not defined for %s" % (ns, cls))
        if ns == "NS-4" and cls not in ("CWEC-78", "CWEC-89"):
            raise Reject("NS-4 is defined for 78 and 89 only")
        if ns == "NS-2" and cls == "CWEC-601" and False:
            raise Reject("n/a")
        yes, no = ns_pair(spec, ns, rng)
    return yes, no


# ---- witness ------------------------------------------------------------------------------------------------------------------------------
def effect(cls, obs):
    """Did the registered canary effect occur? obs = the observable of the payload call (JSON form)."""
    if obs[0] != "ok":
        return False
    v = obs[1]
    if cls == "CWEC-22":
        return v == "CANARY-FILE-CONTENT"
    if cls == "CWEC-78":
        return isinstance(v, str) and "canarytoken" in [ln.strip() for ln in v.splitlines()]
    if cls == "CWEC-79":
        return isinstance(v, str) and "<b>canarytoken</b>" in v
    if cls == "CWEC-89":
        return isinstance(v, list) and len(v) >= 2
    if cls == "CWEC-117":
        return isinstance(v, str) and "\n" in v
    if cls == "CWEC-601":
        import urllib.parse
        return isinstance(v, str) and urllib.parse.urlparse(v).netloc == "canary.example"
    raise ValueError(cls)


def witness(executor, rid, stem, text, spec):
    cls = spec["cls"]
    fn = spec["names"]["fn"]
    calls = [(fn, [C.PAYLOADS[C.PAY_OF[cls]]], {}), (fn, [C.BENIGN[cls]], {})]
    files = {stem + ".py": text}
    files.update(C.FIXTURES.get(cls, {}))
    res = executor.run([S.calls_request(rid, files, stem, calls)])[0]
    obs = S.parse_marker(res["stdout"]) or []
    ok = S.witness_ok(res) and len(obs) == 2
    eff = bool(ok and effect(cls, obs[0]))
    benign_ok = bool(ok and obs[1][0] == "ok")
    return {"ok": ok, "effect": eff, "benign_ok": benign_ok, "runs": res.get("runs"), "image": res.get("image"), "payload_id": C.PAY_OF[cls], "obs_sha": __import__("LP_COMMON.util", fromlist=["x"]).sha_obj(obs)}


def label_from_witness(w):
    """SOLVER-A recomputation from the stored witness: YES iff the canary effect is observed (and the benign call works), NO iff it is not (benign works)."""
    if not (w["ok"] and w["benign_ok"]):
        return None
    return "YES" if w["effect"] else "NO"


def ladder_flags(spec, kind):
    n = spec.get("neut") or {}
    tr = spec.get("transforms") or []
    flow = "high" if (len(tr) >= 2 or "fmt" in tr or "box" in tr) else ("low" if tr else None)
    helper = "high" if n.get("san") == "helper" else None
    decoy = {"wrong_class": "low", "wrong_var": "high", "branch": "high"}.get(n.get("san"))
    look = "high" if (kind.startswith("ns:NS-3")) else None
    return {"flow": flow, "help": helper, "decoy": decoy, "look": look}


def level_of(flags):
    vals = [v for v in flags.values() if v in ("low", "high")]
    return plan_mod.ladder_level(sum(1 for v in vals if v == "low"), sum(1 for v in vals if v == "high"))


def edit_distance_lines(a, b):
    return sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a.split("\n"), b.split("\n"), autojunk=False).get_opcodes() if t != "equal")


def make_pair_specs(ctx, g, cell):
    from LP_COMMON import util
    rng = ctx.rng("t65", g["seed"])
    banned = lambda n: any(w in n.lower() for w in C.BANNED_WORDS) or bool(ctx.deny_check and ctx.deny_check(n))        # K5: no label word in OUR identifiers
    names = Names("T65", "%s/%s" % (ctx.seed, g["seed"]), deny_check=banned)
    pool = Pool(names)
    cls = cell["cls"]
    yes, no = build_pair(cls, cell, pool, rng)
    stem = pool.stem()
    out = []
    for member, spec in (("yes", yes), ("no", no)):
        text = T.render(spec)
        expect = T.label_spec(spec)
        if expect != ("YES" if member == "yes" else "NO"):
            raise Reject("spec engine says %s for the %s member" % (expect, member))
        w = None
        if cls in C.DYNAMIC:
            w = witness(ctx.executor, "%s:%s" % (g["gid"], member), stem, text, spec)
            lab = label_from_witness(w)
            if lab != expect:
                raise Reject("witness %s vs spec engine %s (%s)" % (lab, expect, member))
        kind = cell["pair_kind"]
        flags = ladder_flags(spec, kind)
        out.append({"head": "VULN", "cls": cls, "lang": "python", "stem": stem, "label": expect, "source_text": text, "member": member, "pair_kind": kind, "witness": w,
                    "spec_summary": {"neut": spec.get("neut"), "source": spec.get("source"), "transforms": spec.get("transforms"), "noise": bool(spec.get("noise"))},
                    "fn": spec["names"]["fn"], "mech": flags, "pair_id": g["gid"], "module_group": g["gid"], "spec": spec})
    d = edit_distance_lines(out[0]["source_text"], out[1]["source_text"])
    if out[0]["source_text"] == out[1]["source_text"] or d < 1:
        raise Reject("twin members render the same code (K2: a pair differs by exactly the registered edit)")     # opposite labels on identical text is a gold bug
    for s in out:
        s["edit_lines"] = d
    return out
