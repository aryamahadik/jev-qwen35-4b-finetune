"""families/T44/world.py: tool algebras (STRIPS-style, typed predicates, negative preconditions), the forward-state
executor (solver A's core), the layered BFS planner, and the sampling helpers. No model, no network.

Data (all JSON-able, so Spec.structure stays hashable):
  tool   {"name", "params": [[var, type]], "needs": [[neg, pred, [vars]]], "adds": [[pred, [vars]]], "dels": [[pred, [vars]]]}
  alg    {"id", "domain", "tools": [tool]}
  fact   (pred, (obj, ...))    state: frozenset of facts      call: (tool name, (obj, ...))
Semantics (G0_SPEC S1-S3): a call is applicable iff every positive need is in the state and no `not` need is; the next
state is (state - dels) | adds. add and del sets of one tool are disjoint (asserted at generation).
Algebras: dev domains = a hand-written tool library, a random subset plus perturbations; fictional domains = a layered
random generator over a vocabulary. Training and held-out domains share no tool, predicate, type or object name.
"""
from __future__ import annotations

import itertools
import random
import re
from collections import deque

# ------------------------------------------------------------------------------------------------ DSL
LIT_RE = re.compile(r"(not )?(\w+)\(([^)]*)\)")


def parse_tool(s: str) -> dict:
    """'stage(f:file) :: needs modified(f), not x(f) :: add staged(f) :: del y(f)' -> tool dict."""
    parts = [p.strip() for p in s.split("::")]
    m = re.fullmatch(r"(\w+)\(([^)]*)\)", parts[0])
    params = [[a.split(":")[0].strip(), a.split(":")[1].strip()] for a in m.group(2).split(",") if a.strip()]
    t = {"name": m.group(1), "params": params, "needs": [], "adds": [], "dels": []}
    for p in parts[1:]:
        kind, _, rest = p.partition(" ")
        for lm in LIT_RE.finditer(rest):
            args = [a.strip() for a in lm.group(3).split(",")]
            if kind == "needs":
                t["needs"].append([bool(lm.group(1)), lm.group(2), args])
            else:
                t["adds" if kind == "add" else "dels"].append([lm.group(2), args])
    return t


DEV = {
    "git": dict(types={"file": ["main.py", "util.py", "app.js", "README.md", "setup.cfg", "index.html", "notes.txt", "Makefile"],
                       "branch": ["main", "dev", "hotfix", "release", "feature-x", "staging"]},
                tools=["edit(f:file) :: needs not frozen(f) :: add modified(f) :: del committed(f)",
                       "stage(f:file) :: needs modified(f) :: add staged(f)",
                       "unstage(f:file) :: needs staged(f) :: del staged(f)",
                       "commit(f:file) :: needs staged(f) :: add committed(f) :: del staged(f), modified(f)",
                       "revert(f:file) :: needs modified(f) :: del modified(f), staged(f)",
                       "track(b:branch) :: needs not detached(b) :: add tracking(b)",
                       "detach(b:branch) :: add detached(b) :: del tracking(b)",
                       "push(f:file, b:branch) :: needs committed(f), tracking(b) :: add pushed(f)",
                       "freeze(f:file) :: add frozen(f) :: del modified(f)",
                       "thaw(f:file) :: needs frozen(f) :: del frozen(f)",
                       "tag(f:file) :: needs committed(f), not frozen(f) :: add tagged(f)"]),
    "build": dict(types={"module": ["core", "net", "ui", "auth", "parser", "storage"],
                         "target": ["linux", "macos", "wasm", "arm64"]},
                  tools=["fetch(m:module) :: add fetched(m)",
                         "configure(m:module) :: needs fetched(m) :: add configured(m)",
                         "compile(m:module) :: needs configured(m) :: add compiled(m)",
                         "link(m:module, t:target) :: needs compiled(m) :: add linked(m, t)",
                         "test(m:module) :: needs compiled(m), not dirty(m) :: add tested(m)",
                         "bundle(m:module, t:target) :: needs linked(m, t), tested(m) :: add bundled(t)",
                         "touch(m:module) :: add dirty(m) :: del tested(m)",
                         "clean(m:module) :: del compiled(m), tested(m), dirty(m)",
                         "lint(m:module) :: needs fetched(m) :: add linted(m)",
                         "patch(m:module) :: needs dirty(m) :: add patched(m) :: del dirty(m)"]),
    "deploy": dict(types={"service": ["api", "worker", "web", "billing", "search"],
                          "env": ["dev-env", "qa", "prod", "eu-prod"]},
                   tools=["build_image(s:service) :: add imaged(s)",
                          "scan(s:service) :: needs imaged(s) :: add scanned(s)",
                          "sign(s:service) :: needs scanned(s) :: add signed(s)",
                          "lock_env(e:env) :: add locked(e)",
                          "unlock_env(e:env) :: needs locked(e) :: del locked(e)",
                          "release(s:service, e:env) :: needs signed(s), not locked(e) :: add live(s, e)",
                          "rollback(s:service, e:env) :: needs live(s, e) :: del live(s, e)",
                          "retire(s:service) :: del imaged(s), scanned(s), signed(s)",
                          "canary(s:service, e:env) :: needs signed(s), not locked(e) :: add trial(s, e)",
                          "promote(s:service, e:env) :: needs trial(s, e) :: add live(s, e) :: del trial(s, e)"]),
    "db": dict(types={"table": ["users", "orders", "events", "invoices", "sessions"],
                      "node": ["db1", "db2", "db3"]},
               tools=["backup(t:table) :: add backed_up(t)",
                      "lock_table(t:table) :: add readonly(t)",
                      "unlock_table(t:table) :: needs readonly(t) :: del readonly(t)",
                      "migrate(t:table) :: needs backed_up(t), not readonly(t) :: add migrated(t)",
                      "index_table(t:table) :: needs migrated(t) :: add indexed(t)",
                      "vacuum(t:table) :: needs not readonly(t) :: add vacuumed(t) :: del indexed(t)",
                      "drop_table(t:table) :: needs backed_up(t) :: del migrated(t), indexed(t), vacuumed(t)",
                      "replicate(t:table, n:node) :: needs migrated(t) :: add replicated(t, n)",
                      "detach_node(n:node) :: add offline(n)",
                      "attach_node(n:node) :: needs offline(n) :: del offline(n)",
                      "promote_node(n:node) :: needs not offline(n) :: add primary(n)"]),
    # held out (sealed split only): its own tool, predicate, type and object names
    "registry": dict(types={"pkg": ["libfoo", "libbar", "cli-kit", "sdk-core", "plugin-a"],
                            "channel": ["stable", "beta", "nightly"]},
                     tools=["draft(p:pkg) :: add drafted(p)",
                            "bump(p:pkg) :: needs drafted(p) :: add bumped(p)",
                            "changelog(p:pkg) :: needs bumped(p) :: add logged(p)",
                            "wheel(p:pkg) :: needs bumped(p) :: add wheeled(p)",
                            "attest(p:pkg) :: needs wheeled(p) :: add attested(p)",
                            "publish(p:pkg, c:channel) :: needs wheeled(p), attested(p), not embargoed(c) :: add listed(p, c)",
                            "embargo(c:channel) :: add embargoed(c)",
                            "lift(c:channel) :: needs embargoed(c) :: del embargoed(c)",
                            "yank(p:pkg, c:channel) :: needs listed(p, c) :: del listed(p, c)",
                            "abandon(p:pkg) :: del drafted(p), bumped(p), wheeled(p), attested(p)"]),
}
# fictional vocabularies: predicates ordered by layer (earlier = more basic); (name, [arg types])
FICT = {
    "alchemy": dict(types={"vial": ["vial_amber", "vial_blue", "vial_cedar", "vial_dusk", "vial_ember"],
                           "rack": ["rack_oak", "rack_ash", "rack_elm"]},
                    preds=[("raw", ["vial"]), ("ground", ["vial"]), ("steeped", ["vial"]), ("distilled", ["vial"]),
                           ("sealed", ["vial"]), ("shelved", ["vial", "rack"]), ("clouded", ["vial"]), ("warded", ["rack"])],
                    verbs=["grind", "steep", "distill", "seal", "shelve", "cloud", "ward", "rinse", "mend", "brew", "filter", "stir"]),
    "harbor": dict(types={"crate": ["crate_17", "crate_22", "crate_31", "crate_40", "crate_58"],
                          "berth": ["berth_north", "berth_south", "berth_pier"]},
                   preds=[("afloat", ["crate"]), ("hoisted", ["crate"]), ("weighed", ["crate"]), ("cleared", ["crate"]),
                          ("stowed", ["crate", "berth"]), ("lashed", ["crate"]), ("quarantined", ["crate"]), ("fuelled", ["berth"])],
                   verbs=["hoist", "weigh", "clear", "stow", "lash", "quarantine", "refuel", "drain", "unlash", "haul", "chart", "signal"]),
    "theatre": dict(types={"prop": ["prop_crown", "prop_sword", "prop_lamp", "prop_chair", "prop_mask"],
                           "scene": ["scene_opening", "scene_duel", "scene_finale", "scene_chase"]},
                    preds=[("dusted", ["prop"]), ("painted", ["prop"]), ("rigged", ["prop"]), ("rehearsed", ["prop"]),
                           ("placed", ["prop", "scene"]), ("lit", ["scene"]), ("hushed", ["scene"]), ("struck", ["prop"])],
                    verbs=["dust", "paint", "rig", "rehearse", "place", "illuminate", "hush", "strike", "polish", "cue", "wax", "fold"]),
    # held out
    "observatory": dict(types={"lens": ["lens_alpha", "lens_beta", "lens_gamma", "lens_delta", "lens_epsilon"],
                               "dome": ["dome_east", "dome_west", "dome_polar"]},
                        preds=[("cased", ["lens"]), ("collimated", ["lens"]), ("aligned", ["lens"]), ("cooled", ["lens"]),
                               ("mounted", ["lens", "dome"]), ("slewed", ["dome"]), ("opened", ["dome"]), ("calibrated", ["lens"])],
                        verbs=["case", "collimate", "align", "cool", "mount", "slew", "open_dome", "calibrate", "uncase", "park", "defog", "retune"]),
    "bakery": dict(types={"dough": ["dough_rye", "dough_spelt", "dough_brioche", "dough_sour", "dough_pita"],
                          "oven": ["oven_stone", "oven_deck", "oven_brick"]},
                   preds=[("kneaded", ["dough"]), ("proofed", ["dough"]), ("shaped", ["dough"]), ("scored", ["dough"]),
                          ("baked", ["dough", "oven"]), ("glazed", ["dough"]), ("preheated", ["oven"]), ("rested", ["dough"])],
                   verbs=["knead", "proof", "shape", "score", "bake", "glaze", "preheat", "rest", "punch_down", "slice", "dust_flour", "chill"]),
}
TRAIN_DOMAINS = ("git", "build", "deploy", "db", "alchemy", "harbor", "theatre")
HELD_OUT_DOMAINS = ("registry", "observatory", "bakery")
ALGS_PER_DOMAIN = 40               # algebra index range per domain (7 training domains x 40 = 280 algebras)


def _vars_for(types: list) -> list:
    """Fresh parameter variables for a list of types: first letter, then a digit when a type repeats."""
    out, seen = [], {}
    for t in types:
        seen[t] = seen.get(t, 0) + 1
        out.append(t[0] + ("" if seen[t] == 1 else str(seen[t])))
    return out


def _check_tool(t: dict) -> dict:
    ad = {(p, tuple(a)) for p, a in t["adds"]}
    dl = {(p, tuple(a)) for p, a in t["dels"]}
    assert not (ad & dl), f"tool {t['name']}: add and del overlap"
    pos = {(p, tuple(a)) for n, p, a in t["needs"] if not n}
    neg = {(p, tuple(a)) for n, p, a in t["needs"] if n}
    assert not (pos & neg), f"tool {t['name']}: contradictory needs"
    return t


def _dev_algebra(dom: str, idx: int) -> dict:
    R = random.Random(f"alg|{dom}|{idx}")
    lib = [parse_tool(s) for s in DEV[dom]["tools"]]
    k = R.randint(5, 7)
    prod = {}
    for t in lib:
        for p, _ in t["adds"]:
            prod.setdefault(p, []).append(t)
    chosen = [R.choice(lib)]
    grew = True
    while grew and len(chosen) < k:                    # dependency closure: every positive need has a producer
        grew = False
        for t in list(chosen):
            for n, p, _ in t["needs"]:
                if not n and p in prod and not any(p in [x for x, _ in c["adds"]] for c in chosen) and len(chosen) < k:
                    chosen.append(R.choice(prod[p]))
                    grew = True
    rest = [t for t in lib if t not in chosen]
    R.shuffle(rest)
    chosen += rest[:max(0, k - len(chosen))]
    tools = [dict(t) for t in chosen]
    for t in tools:                                   # perturbations (label-blind, per algebra)
        t["needs"] = [list(x) for x in t["needs"]]
        t["dels"] = [list(x) for x in t["dels"]]
        u = R.random()
        if u < 0.2 and len(t["needs"]) >= 2:
            t["needs"].pop(R.randrange(len(t["needs"])))
        elif u < 0.4 and t["params"]:
            # add a `not` need on a predicate over the same params that this tool does not add or need
            cands = []
            for o in tools:
                for lit in o["adds"] + o["dels"]:
                    p = lit[0]
                    ps = {(l[1]) for l in t["needs"]} | {l[0] for l in t["adds"]} | {l[0] for l in t["dels"]}
                    if p in ps:
                        continue
                    ptypes = [dict((v, ty) for v, ty in o["params"])[a] for a in lit[1]]
                    pv = [v for v, _ in t["params"]]
                    mapped = []
                    for ty in ptypes:
                        m = [v for v, tty in t["params"] if tty == ty]
                        if not m:
                            mapped = None
                            break
                        mapped.append(m[0])
                    if mapped is not None:
                        cands.append([True, p, mapped])
            if cands:
                t["needs"].append(R.choice(cands))
        _check_tool(t)
    tools.sort(key=lambda t: R.random())
    return {"id": f"{dom}:{idx}", "domain": dom, "tools": tools}


def _fict_algebra(dom: str, idx: int) -> dict:
    V = FICT[dom]
    R = random.Random(f"alg|{dom}|{idx}")
    P = V["preds"]
    chosen = sorted(R.sample(range(len(P)), R.randint(6, len(P))))
    preds = [P[i] for i in chosen]                    # layer order
    ntools = R.randint(5, 7)
    verbs = R.sample(V["verbs"], ntools)
    targets = [i for i in range(len(preds))]
    R.shuffle(targets)
    targets = (targets * 2)[:ntools - 1]
    tools = []
    for j, verb in enumerate(verbs[:-1]):
        ti = targets[j]
        pname, ptypes = preds[ti]
        vs = _vars_for(ptypes)
        params = [[v, ty] for v, ty in zip(vs, ptypes)]
        pmap = {}
        for v, ty in params:
            pmap.setdefault(ty, v)

        def lit_over(pi):
            nm, tys = preds[pi]
            if all(ty in pmap for ty in tys):
                return nm, [pmap[ty] for ty in tys]
            return None
        needs, dels = [], []
        low = [i for i in range(ti) if lit_over(i)]
        if low and (ti > 0 or R.random() < 0.3):
            for i in R.sample(low, min(len(low), R.choice([1, 1, 2]))):
                nm, a = lit_over(i)
                needs.append([False, nm, a])
        high = [i for i in range(ti + 1, len(preds)) if lit_over(i)]
        if high and R.random() < 0.3:
            nm, a = lit_over(R.choice(high))
            needs.append([True, nm, a])
        pool = [i for i in range(len(preds)) if i != ti and lit_over(i)]
        if pool and R.random() < 0.5:
            nm, a = lit_over(R.choice(pool))
            if not any(n == nm and ar == a for ng, n, ar in needs if not ng) or R.random() < 0.5:
                dels.append([nm, a])
        t = {"name": verb, "params": params, "needs": needs, "adds": [[pname, [pmap[ty] for ty in ptypes]]],
             "dels": dels}
        tools.append(t)
    # one undo tool: removes a mid-layer fact that it needs
    ui = R.randrange(len(preds))
    nm, tys = preds[ui]
    vs = _vars_for(tys)
    tools.append({"name": verbs[-1], "params": [[v, ty] for v, ty in zip(vs, tys)], "needs": [[False, nm, vs]],
                  "adds": [], "dels": [[nm, vs]]})
    for t in tools:
        _check_tool(t)
    return {"id": f"{dom}:{idx}", "domain": dom, "tools": tools}


def make_algebra(dom: str, idx: int) -> dict:
    return _dev_algebra(dom, idx) if dom in DEV else _fict_algebra(dom, idx)


def domain_types(dom: str) -> dict:
    return (DEV.get(dom) or FICT[dom])["types"]


def domain_tool_names(dom: str) -> list:
    if dom in DEV:
        return [parse_tool(s)["name"] for s in DEV[dom]["tools"]]
    return list(FICT[dom]["verbs"])


def vocab(dom: str) -> dict:
    """Every name the domain can put in a row: tools, predicates, types, objects."""
    if dom in DEV:
        tl = [parse_tool(s) for s in DEV[dom]["tools"]]
        preds = {p for t in tl for p, _ in t["adds"] + t["dels"]} | {p for t in tl for _, p, _ in t["needs"]}
        tools = {t["name"] for t in tl}
    else:
        preds = {p for p, _ in FICT[dom]["preds"]}
        tools = set(FICT[dom]["verbs"])
    ty = domain_types(dom)
    return {"tools": tools, "preds": preds, "types": set(ty), "objects": {o for v in ty.values() for o in v}}


# ------------------------------------------------------------------------------------------------ grounding / execution
def tool_types(alg: dict) -> dict:
    return {t["name"]: [ty for _, ty in t["params"]] for t in alg["tools"]}


def ground_actions(alg: dict, objs: dict) -> list:
    """All ground calls in a fixed order: [{call, name, args, pos, neg, adds, dels}]."""
    out = []
    for t in alg["tools"]:
        pools = [objs.get(ty, []) for _, ty in t["params"]]
        for combo in itertools.product(*pools):
            b = {v: o for (v, _), o in zip(t["params"], combo)}
            out.append({"call": (t["name"], tuple(combo)), "name": t["name"], "args": tuple(combo),
                        "pos": frozenset((p, tuple(b[v] for v in a)) for n, p, a in t["needs"] if not n),
                        "neg": frozenset((p, tuple(b[v] for v in a)) for n, p, a in t["needs"] if n),
                        "adds": frozenset((p, tuple(b[v] for v in a)) for p, a in t["adds"]),
                        "dels": frozenset((p, tuple(b[v] for v in a)) for p, a in t["dels"])})
    return out


def applicable(g: dict, state: frozenset) -> bool:
    return g["pos"] <= state and not (g["neg"] & state)


def step(g: dict, state: frozenset) -> frozenset:
    return (state - g["dels"]) | g["adds"]


def call_text(name: str, args) -> str:
    return f"{name}({', '.join(args)})"


def fact_text(f) -> str:
    return f"{f[0]}({', '.join(f[1])})"


def lit_text(neg: bool, f) -> str:
    return ("not " if neg else "") + fact_text(f)


def goal_holds(goal: list, state: frozenset) -> bool:
    return all(((p, tuple(a)) in state) != bool(n) for n, p, a in goal)


def verdict(alg: dict, objs: dict, start: list, plan: list, goal: list) -> str:
    """Solver A (forward state simulation). Returns INVALID | STEP_k_NOT_APPLICABLE | GOAL_NOT_REACHED | VALID."""
    tools = {t["name"]: t for t in alg["tools"]}
    for name, args in plan:
        t = tools.get(name)
        if t is None or len(args) != len(t["params"]) or any(a not in objs.get(ty, ()) for a, (_, ty) in zip(args, t["params"])):
            return "INVALID"
    gmap = {g["call"]: g for g in ground_actions(alg, objs)}
    state = frozenset((p, tuple(a)) for p, a in start)
    for k, (name, args) in enumerate(plan, 1):
        g = gmap[(name, tuple(args))]
        if not applicable(g, state):
            return f"STEP_{k}_NOT_APPLICABLE"
        state = step(g, state)
    return "VALID" if goal_holds(goal, state) else "GOAL_NOT_REACHED"


def run_prefix(alg: dict, objs: dict, start: list, prefix: list):
    """The state after the prefix calls, or None when a call is not applicable / unknown."""
    gmap = {g["call"]: g for g in ground_actions(alg, objs)}
    state = frozenset((p, tuple(a)) for p, a in start)
    for name, args in prefix:
        g = gmap.get((name, tuple(args)))
        if g is None or not applicable(g, state):
            return None
        state = step(g, state)
    return state


class Cap(Exception):
    pass


def explore(actions: list, state: frozenset, goal: list, *, max_depth: int = 10, cap: int = 40000) -> dict:
    """Layered BFS from `state`. {d, firsts (set of calls that start some shortest plan), complete (search exhausted)}.
    d None: goal not reached within max_depth (complete: the whole reachable space was searched)."""
    if goal_holds(goal, state):
        return {"d": 0, "firsts": set(), "complete": True}
    seen = {state: (0, frozenset())}
    frontier = [state]
    depth = 0
    while frontier and depth < max_depth:
        depth += 1
        nxt = {}
        for s in frontier:
            f0 = seen[s][1]
            for g in actions:
                if not applicable(g, s):
                    continue
                ns = step(g, s)
                fs = frozenset([g["call"]]) if depth == 1 else f0
                if ns in seen:
                    if seen[ns][0] == depth:
                        seen[ns] = (depth, seen[ns][1] | fs)
                    continue
                seen[ns] = (depth, fs)
                nxt[ns] = True
                if len(seen) > cap:
                    raise Cap()
        hit = [s for s in nxt if goal_holds(goal, s)]
        if hit:
            firsts = set()
            for s in hit:
                firsts |= seen[s][1]
            return {"d": depth, "firsts": firsts, "complete": True}
        frontier = list(nxt)
    return {"d": None, "firsts": set(), "complete": not frontier}


# ------------------------------------------------------------------------------------------------ instance helpers
def make_objects(R: random.Random, alg: dict, dom: str, *, n_range=(2, 3), counts: dict | None = None) -> dict:
    ty = domain_types(dom)
    used = []
    for t in alg["tools"]:
        for _, tt in t["params"]:
            if tt not in used:
                used.append(tt)
    out = {}
    for tt in [t for t in ty if t in used]:
        out[tt] = sorted(R.sample(ty[tt], min(len(ty[tt]), (counts or {}).get(tt) or R.randint(*n_range))))
    return out


def entry_preds(alg: dict) -> list:
    """Predicates some tool needs positively but no tool adds (inputs of the world), in tool order."""
    added = {p for t in alg["tools"] for p, _ in t["adds"]}
    out = []
    for t in alg["tools"]:
        for n, p, _ in t["needs"]:
            if not n and p not in added and p not in out:
                out.append(p)
    return out


def all_facts(alg: dict, objs: dict) -> list:
    """Every ground fact the algebra can mention (sorted)."""
    sig = {}
    for t in alg["tools"]:
        tm = dict((v, ty) for v, ty in t["params"])
        for p, a in t["adds"] + t["dels"]:
            sig[p] = [tm[v] for v in a]
        for _, p, a in t["needs"]:
            sig[p] = [tm[v] for v in a]
    out = []
    for p in sorted(sig):
        for combo in itertools.product(*[objs.get(ty, []) for ty in sig[p]]):
            out.append((p, tuple(combo)))
    return out


def make_start(R: random.Random, alg: dict, objs: dict, n: int | None = None) -> frozenset:
    """The start facts: `n` of them when given (drawn from the row key, so a label cannot move it), else 1-5. Entry
    predicates first (at least one when the world has any), then any fact."""
    facts = all_facts(alg, objs)
    ent = set(entry_preds(alg))
    pri = [f for f in facts if f[0] in ent]
    oth = [f for f in facts if f[0] not in ent]
    if n is None:
        n = R.randint(1, 3) + (R.randint(1, 2) if oth and R.random() < 0.6 else 0)
    k1 = min(len(pri), max(1, n - 1) if oth else n) if pri else 0
    s = set(R.sample(pri, k1)) if k1 else set()
    rest = [f for f in facts if f not in s]
    s |= set(R.sample(rest, min(len(rest), n - len(s))))
    return frozenset(s)


def random_walk(R: random.Random, actions: list, state: frozenset, n: int):
    """n applicable calls from `state` (each changes the state, none repeats the previous call); biased to calls that add
    a new fact. Returns ([call...], [state after each]) or None."""
    calls, states = [], [state]
    for _ in range(n):
        opts = [g for g in actions if applicable(g, state) and step(g, state) != state
                and (not calls or g["call"] != calls[-1])]
        if not opts:
            return None
        w = [3 if (g["adds"] - state) else 1 for g in opts]
        g = R.choices(opts, weights=w)[0]
        calls.append(g["call"])
        state = step(g, state)
        states.append(state)
    return calls, states


def make_goal(R: random.Random, s_from: frozenset, s_to: frozenset, n_goal: int):
    """A goal of n_goal literals true in s_to and false in s_from (positive: gained fact; negative: lost fact)."""
    gained = sorted(s_to - s_from)
    lost = sorted(s_from - s_to)
    pool = [(False, f) for f in gained] + [(True, f) for f in lost if R.random() < 0.5]
    if len(pool) < 1:
        return None
    R.shuffle(pool)
    pick = pool[:min(n_goal, len(pool))]
    pick.sort(key=lambda x: (x[1], x[0]))
    return [[neg, f[0], list(f[1])] for neg, f in pick]


def bfs_depths(actions: list, state: frozenset, max_depth: int, cap: int = 40000) -> dict:
    """{state: shortest depth} for every state reachable from `state` in <= max_depth calls."""
    depth = {state: 0}
    frontier = [state]
    for d in range(1, max_depth + 1):
        nxt = []
        for s in frontier:
            for g in actions:
                if applicable(g, s):
                    ns = step(g, s)
                    if ns not in depth:
                        depth[ns] = d
                        nxt.append(ns)
                        if len(depth) > cap:
                            raise Cap()
        frontier = nxt
    return depth
