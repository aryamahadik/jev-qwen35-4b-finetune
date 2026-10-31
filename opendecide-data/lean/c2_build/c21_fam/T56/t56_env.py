"""T56 done-claim half: the simulated environment (typed store, effect ledger, working tree, symbolic module graph),
the closed predicate library, and the check / ledger / tree / graph read operations. Everything here is a program; no
generated code is ever executed (the optional D3 execution check belongs to the signed-off sandbox, later).

Predicates (closed library): exists, absent, equals, count_eq, exactly_once, status_is, unchanged, reachable.
"""
from collections import deque

PREDICATES = ("exists", "absent", "equals", "count_eq", "exactly_once", "status_is", "unchanged", "reachable")
STORE_PREDS = ("exists", "absent", "equals", "count_eq", "status_is", "unchanged")
LEDGER_PREDS = ("exactly_once",)
GRAPH_PREDS = ("reachable",)


class Env:
    """Typed key-value store with a global revision clock. Every call ticks the clock; `last_mut[item]` is the clock value
    of the last call that targeted the item (an effect may have been silently dropped by a fault, the call still happened)."""

    def __init__(self, items, init_field, field_name):
        self.store = {i: {"status": "open", field_name: init_field, "rev": 0} for i in items}
        self.initial = {i: dict(v) for i, v in self.store.items()}
        self.field_name = field_name
        self.rev = 0
        self.last_mut = {}
        self.ledger = []                 # {"recipient","key","rev"}
        self.tree = {}                   # path -> state in {"modified","untracked","staged"}
        self.last_edit_rev = 0

    def tick(self):
        self.rev += 1
        return self.rev

    # ---- mutations -----------------------------------------------------------------------------------
    def set_status(self, item, value, drop=False):
        r = self.tick()
        self.last_mut[item] = r
        if not drop:
            self.store[item]["status"] = value
            self.store[item]["rev"] = r
        return r

    def set_field(self, item, value, drop=False):
        r = self.tick()
        self.last_mut[item] = r
        if not drop:
            self.store[item][self.field_name] = value
            self.store[item]["rev"] = r
        return r

    def create(self, item, drop=False):
        r = self.tick()
        self.last_mut[item] = r
        if not drop:
            self.store[item] = {"status": "open", self.field_name: "", "rev": r}
        return r

    def remove(self, item, drop=False):
        r = self.tick()
        self.last_mut[item] = r
        if not drop:
            self.store.pop(item, None)
        return r

    def send(self, recipient, key, mode="normal"):
        """mode normal: one ledger entry; dup: the effect lands twice; drop: it never lands."""
        r = self.tick()
        self.last_mut["send:" + recipient] = r
        if mode in ("normal", "dup"):
            self.ledger.append({"recipient": recipient, "key": key, "rev": r})
        if mode == "dup":
            self.ledger.append({"recipient": recipient, "key": key, "rev": r})
        return r

    def edit_tree(self, path, state="modified"):
        r = self.tick()
        self.tree[path] = state
        self.last_edit_rev = r
        return r

    # ---- predicate evaluation (hidden truth) -----------------------------------------------------------
    def eval_pred(self, c, graph=None):
        p = c["pred"]
        if p == "exists":
            return c["item"] in self.store
        if p == "absent":
            return c["item"] not in self.store
        if p == "status_is":
            return c["item"] in self.store and self.store[c["item"]]["status"] == c["value"]
        if p == "equals":
            return c["item"] in self.store and self.store[c["item"]].get(self.field_name) == c["value"]
        if p == "count_eq":
            return len(self.store) == c["value"]
        if p == "unchanged":
            return c["item"] in self.store and self.store[c["item"]] == self.initial.get(c["item"])
        if p == "exactly_once":
            return sum(1 for e in self.ledger if e["recipient"] == c["item"]) == 1
        if p == "reachable":
            return graph is not None and reachable(graph, c["item"])
        raise ValueError(p)


# ---- module graph (D3) -------------------------------------------------------------------------------------
def reachable(graph, sym):
    """BFS from the entrypoint over CALL edges that are usable: the guard holds (none, or a flag whose default is on) and,
    for a call across modules, an import edge exists. Solver A uses BFS; the P-20 gate cross-checks with DFS."""
    mod = graph["module_of"]
    imports = {(a, b) for a, b in graph["imports"]}
    flags = graph["flags"]
    seen = {graph["entry"]}
    q = deque([graph["entry"]])
    while q:
        u = q.popleft()
        for (a, b, guard) in graph["calls"]:
            if a != u or b in seen:
                continue
            if guard == "never":
                continue
            if guard.startswith("flag:") and not flags.get(guard[5:], False):
                continue
            if mod[a] != mod[b] and (mod[a], mod[b]) not in imports:
                continue
            seen.add(b)
            q.append(b)
    return sym in seen


def reachable_dfs(graph, sym):
    """Independent implementation (iterative DFS, recursion-free) for the P-20 cross-check."""
    mod = graph["module_of"]
    imports = {(a, b) for a, b in graph["imports"]}
    flags = graph["flags"]
    stack, seen = [graph["entry"]], set()
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        for (a, b, guard) in graph["calls"]:
            ok = a == u and guard != "never" and not (guard.startswith("flag:") and not flags.get(guard[5:], False)) \
                and (mod[a] == mod[b] or (mod[a], mod[b]) in imports)
            if ok:
                stack.append(b)
    return sym in seen


def build_graph(rng, entry_mod, feat_mod, feat_sym, other_mods, variant):
    """Symbolic graph with the requested defect (variant None = correctly wired). Symbols are <module>.<name>.
    Every graph, defective or not, carries DECOYS that look like defects but are irrelevant (a guard that is never true, a
    flag that is off, both on unrelated branches) and a RANDOM number of unrelated modules, so neither a keyword nor a count
    of imports / calls / flags is a cue for the defect."""
    entry = "%s.run" % entry_mod
    target = "%s.%s" % (feat_mod, feat_sym)
    mods = [entry_mod, feat_mod] + list(other_mods)
    module_of = {entry: entry_mod, target: feat_mod}
    calls = [(entry, target, "none")]
    imports = [(entry_mod, feat_mod)]
    flags = {}
    for om in other_mods:                                      # unrelated utility modules
        util_s = "%s.util" % om
        module_of[util_s] = om
        calls.append((entry, util_s, "none"))
        imports.append((entry_mod, om))
        if rng.random() < 0.55:                                # decoy: a flag that is off
            beta_s = "%s.beta" % om
            module_of[beta_s] = om
            calls.append((entry, beta_s, "flag:%s_beta" % om))
            flags["%s_beta" % om] = False
        if rng.random() < 0.55:                                # decoy: a guard that is never true
            dead_s = "%s.dead" % om
            module_of[dead_s] = om
            calls.append((util_s, dead_s, "never"))
    guarded = rng.random() < 0.5                               # the live path may sit behind a flag that is ON
    if guarded:
        flags["%s_enabled" % feat_mod] = True
        calls[0] = (entry, target, "flag:%s_enabled" % feat_mod)
    if variant == "import_not_wired":
        imports = [(a, b) for a, b in imports if (a, b) != (entry_mod, feat_mod)]
    elif variant == "flag_default_off":
        fl = "%s_enabled" % feat_mod
        flags[fl] = False
        calls[0] = (entry, target, "flag:%s" % fl)
    elif variant == "unreachable_branch":
        calls[0] = (entry, target, "never")
    elif variant == "helper_never_called":
        calls = [c for c in calls if not (c[0] == entry and c[1] == target)]            # imported but never called
    elif variant is not None:
        raise ValueError(variant)
    rng.shuffle(calls)
    rng.shuffle(imports)
    return dict(entry=entry, module_of=module_of, calls=[list(c) for c in calls], imports=[list(i) for i in imports],
                flags=flags, modules=mods, target=target)
