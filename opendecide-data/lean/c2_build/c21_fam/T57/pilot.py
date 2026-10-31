"""The 50-module mutation PILOT that fixes the gate-b threshold T_s (G0-lite section 2; Opus ruling (c)). Rule, written before the
pilot: T_s = 0.90 if >= 70% of the pilot modules reach 0.90 at the planned suite recipe; otherwise the suite recipe gets ONE
revision (more boundary and pairwise cases from D) and the pilot is rerun on fresh modules; T_s never goes below 0.80. If a
non-Python language scores below 0.80 on its 4 modules, that language's pilot is extended to 20 modules before any row.
Composition: 38 Python, 4 JS/TS, 4 Go, 4 bash. `pilot_tasks` builds the modules (no row is made), `pilot_requests` are the sandbox
jobs, `pilot_scores` reads the results (kill share of non-equivalent mutants per module) and applies the rule.
"""
from LC_COMMON import sandbox_iface as S

from . import config as C
from . import solver_a as SA
from . import task as TK
from .base import Skip

LANG_SPLIT = (("python", 38), ("javascript", 2), ("typescript", 2), ("go", 4), ("bash", 4))


def pilot_tasks(seed0=7000, split=LANG_SPLIT, extension=None):
    out = []
    for lang, n in split:
        want = (extension or {}).get(lang, n)
        s = seed0
        got = 0
        while got < want and s < seed0 + 2000:
            s += 1
            try:
                out.append(TK.make_task("pilot%d" % s, lang, "A"))
                got += 1
            except Skip:
                continue
    return out


def pilot_requests(tasks):
    pool = {}
    for t in tasks:
        for rid, kv in SA.module_requests(t).items():
            pool.setdefault(rid, kv)
    return pool


def kill_share(task, results):
    """Kill share of the NON-EQUIVALENT mutants of one module (survivors proven by the differential count as non-equivalent;
    undecided survivors are excluded). Returns (share | None, record)."""
    names = SA.all_case_names(task)
    domR = results["%s#domR" % task["id"]]
    killed = decided = undecided = 0
    for k, m in enumerate(SA.strength_pool(task)):
        st = SA.states_of(results["%s#str%d" % (task["id"], k)], names)
        if any(v != "passed" for v in st.values()):
            killed += 1
            decided += 1
            continue
        d = results.get("%s#strd%d" % (task["id"], k))
        if d is not None and SA.S_out_id(d) != SA.S_out_id(domR):
            decided += 1
        else:
            undecided += 1
    return ((killed / decided) if decided else None), {"killed": killed, "decided": decided, "undecided": undecided}


def pilot_scores(tasks, executor):
    reqs = pilot_requests(tasks)
    order = list(reqs)
    res = dict(zip(order, executor.run([reqs[r][1] for r in order])))
    by_lang, allscores = {}, []
    for t in tasks:
        share, rec = kill_share(t, res)
        if share is None:
            continue
        by_lang.setdefault(t["lang"], []).append(share)
        allscores.append(share)
    ts, action = SA.pilot_threshold(allscores)
    ext = []
    for lang, sc in by_lang.items():
        if lang != "python" and sc and (sum(sc) / len(sc)) < C.TS_FLOOR:
            ext.append(lang)
    return {"T_s": ts, "action": action, "per_language_mean": {k: sum(v) / len(v) for k, v in by_lang.items()},
            "extend_to_20_modules": ext, "n_modules": len(allscores)}
