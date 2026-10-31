"""Shared helpers of the three agreement harnesses: sha logging, error-class sanitising, summary tables. No row text is stored."""
import collections
import hashlib
import json
import os
import re


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def sha_tree(root, exts=(".py",), skip=("__pycache__", "tests", "reports")):
    out = {}
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d not in skip)
        for f in sorted(fn):
            if f.endswith(exts):
                p = os.path.join(dp, f)
                out[os.path.relpath(p, root)] = sha256_file(p)
    return out


def why_class(why):
    """Reduce an Unsupported / Timeout message to a construct class (no identifiers, no item text)."""
    w = re.sub(r"'[^']*'|\"[^\"]*\"", "Q", why or "")
    w = re.sub(r"\b[a-z]{3,}_[a-z_]+\b", "ID", w)
    w = re.sub(r"\d+", "N", w)
    return w[:60]


class Tally:
    def __init__(self):
        self.n = collections.Counter()
        self.classes = collections.defaultdict(collections.Counter)
        self.notes = collections.defaultdict(collections.Counter)

    def add(self, key, outcome, cls=None):
        self.n[(key, "rows")] += 1
        self.n[(key, outcome)] += 1
        if cls:
            self.classes[key][cls] += 1

    def note(self, key, name, ok):
        self.notes[key][(name, bool(ok))] += 1

    def table(self):
        keys = sorted({k for k, _ in self.n})
        out = {}
        for k in keys:
            rows = self.n[(k, "rows")]
            agree = self.n[(k, "agree")]
            dis = self.n[(k, "disagree")]
            unsup = rows - agree - dis
            labelled = agree + dis
            out["/".join(map(str, k)) if isinstance(k, tuple) else str(k)] = {
                "rows": rows, "b_labelled": labelled, "agree": agree, "disagree": dis, "b_refused": unsup,
                "agreement_pct": round(100.0 * agree / labelled, 3) if labelled else None,
                "classes": dict(self.classes[k]), "notes": {"%s=%s" % nm: c for nm, c in self.notes[k].items()}}
        return out


def totals(table):
    r = sum(v["rows"] for v in table.values())
    a = sum(v["agree"] for v in table.values())
    d = sum(v["disagree"] for v in table.values())
    ref = sum(v["b_refused"] for v in table.values())
    return {"rows": r, "b_labelled": a + d, "agree": a, "disagree": d, "b_refused": ref,
            "agreement_pct": round(100.0 * a / (a + d), 3) if a + d else None}


def write_report(path, report):
    with open(path, "w") as f:
        json.dump(report, f, indent=1, sort_keys=True)


# ------------------------------------------------------------------------------------------------ G1 lint of the solver B package
FORBIDDEN_IMPORT_PREFIXES = ("LC_COMMON", "tool_engine", "T42c.solver_a", "T42c.out4", "T42c.eqv2", "T42c.tfail2", "T42c.planner",
                             "T42c.rows", "T42c.build", "T42c.gates", "T57.solver_a", "T57.task", "T57.heads", "T57.facts", "T57.build",
                             "T57.rows", "T56g.solver_a", "T56g.hacks", "T56g.task", "T56g.build", "T56g.natural", "T56g.rows",
                             "subprocess", "socket", "urllib", "requests", "http", "anthropic", "openai", "modal", "ctypes")
FORBIDDEN_CALLS = ("exec", "eval", "compile", "__import__", "open")


def lint_b_files(paths, allowed_local=("LC_SOLVER_B",)):
    """G1: a solver B module may import only the standard library, LC_SOLVER_B and its own package; it never calls exec / eval /
    compile / os.system / subprocess on generated text and reads no file. Returns a list of violations."""
    import ast
    import sys
    std = set(sys.stdlib_module_names)
    bad = []
    for p in paths:
        tree = ast.parse(open(p, encoding="utf-8").read())
        for n in ast.walk(tree):
            mods = []
            if isinstance(n, ast.Import):
                mods = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                if n.level:
                    continue                                # relative import inside the solver_b package itself
                mods = [n.module or ""]
            for m in mods:
                top = m.split(".")[0]
                if any(m == f or m.startswith(f + ".") for f in FORBIDDEN_IMPORT_PREFIXES):
                    bad.append("%s: forbidden import %s" % (p, m))
                elif top not in std and top not in allowed_local:
                    bad.append("%s: non-stdlib import %s" % (p, m))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FORBIDDEN_CALLS:
                bad.append("%s: call to %s" % (p, n.func.id))
            if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "os" and n.attr in ("system", "popen", "exec", "spawn"):
                bad.append("%s: os.%s" % (p, n.attr))
    return bad


# ------------------------------------------------------------------------------------------------ generation-time check hook (shared)
def batch_verdict(results, block_drop_limit):
    """results: list of {'row_id', 'keep': bool, 'reason': str|None}. Applies the G0-lite block rule (drop share above the family limit
    returns the block to the generator). Counts only."""
    n = len(results)
    dropped = [r for r in results if not r["keep"]]
    reasons = collections.Counter(r["reason"] for r in dropped)
    share = (len(dropped) / n) if n else 0.0
    return {"n": n, "kept": n - len(dropped), "dropped": len(dropped), "drop_share": round(share, 5), "reasons": dict(reasons),
            "block_returns_to_generator": share > block_drop_limit, "block_drop_limit": block_drop_limit}
