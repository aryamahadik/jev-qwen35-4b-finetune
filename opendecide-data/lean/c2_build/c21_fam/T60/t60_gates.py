"""T60 PRE-FREEZE KILL gates K1..K28 (CPU, data only) per G0-lite section 8.1 and the Opus batch-1b rulings. Probes go through the injected
L-0 harness (G5). Orchestrator / program jobs, not computed here: K18 stamp drops beyond the pipeline summary, K20 (A50 G6, A49c, G5-H, G3-H,
A43(d)), K23 (C2 <= 70% on L4, od-l4b). POST-TRAINING lines (P1..P8) are never kill rules.
`run_all(records, harness, allowlist)` -> list of {id, ok, ...}; a probe gate is skipped (ok=None) without a harness.
"""
import collections
import io
import itertools
import os
import re
import sys
import tokenize

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import gates_common as gc  # noqa: E402
from tool_engine import render, util  # noqa: E402
import t60_levels as lv  # noqa: E402
import t60_model as M  # noqa: E402
import t60_oracle as orc  # noqa: E402
import t60_rule as rule  # noqa: E402

LABEL_A = {"h1": "DELEGATE", "h2": "KEEP", "h3": "PLAN"}


def _clean(records):
    return [r for r in records if r.get("lever_tag", "lever.none") == "lever.none" and not r.get("dev_only")]


def _share(rows, pred):
    return sum(1 for r in rows if pred(r)) / len(rows) if rows else 0.0


def _skip(gid):
    return dict(id=gid, ok=None, skipped="no probe harness")


def _probe(gid, rows, harness, X, **extra):
    if harness is None:
        return _skip(gid)
    y = [int(r["gold"] == LABEL_A[r["hd"]]) for r in rows]
    return gc.probe_binary_gate(gid, harness, X, y, [r["group_id"] for r in rows], **extra)


# ---- K3 truth tables (code level) ------------------------------------------------------------------------------------------------------
def k3_truth_tables(records):
    bad = []
    n = 0
    base_brief = dict(steps=[], files=[], result_tokens=0, needs=[], writes=[], incoming=[])
    for cid in M.CARDS_BY_HEAD["h1"]:
        c = M.CARDS[cid]
        for steps, vol, needs, res, shared, inc in itertools.product((1, c["S_min"] - 1, c["S_min"], c["S_min"] + 2), (100, c["V"] - 1, c["V"]),
                                                                    (0, c["B_max"], c["B_max"] + 1), (50, c["R_max"], c["R_max"] + 1),
                                                                    (False, True), (False, True)):
            steps = max(1, steps)
            sc = dict(head="h1", card=c, brief=dict(steps=["x"] * steps, files=[dict(path="p", tokens=vol)], result_tokens=res,
                                                    needs=["h%d" % i for i in range(needs)], writes=["w"], incoming=["m2"] if inc else []),
                      main=dict(facts=[], pending=[dict(id="m1", reads=["w"] if shared else ["z"], writes=[])]))
            n += 1
            if rule.h1_label(sc) != orc.h1_oracle(sc):
                bad.append(("h1", cid, steps, vol, needs, res, shared, inc))
    for cid in M.CARDS_BY_HEAD["h3"]:
        c = M.CARDS[cid]
        for nst, irr, ordered in itertools.product(range(2, 8), (False, True), (False, True)):
            eff = dict(kind="delete", backup=False, undo=None if irr else dict(tool="restore", remaining=9), external=False, magnitude=1,
                       created_by_agent=False)
            steps = [dict(sid="s%d" % i, verb="delete", entity="e", target="t", effect=dict(eff)) for i in range(nst)]
            edges = [["s%d" % i, "s%d" % (i + 1)] for i in range(nst - 1)]
            sc = dict(head="h3", card=c, steps=steps, edges=edges, stated_edges=edges if ordered else [])
            n += 1
            if rule.h3_label(sc) != orc.h3_oracle(sc):
                bad.append(("h3", cid, nst, irr, ordered))
    for r in records:
        if r["hd"] in ("h1", "h2", "h3"):
            n += 1
            if rule.gold_label(r) != orc.oracle_label(r["scene"]) or rule.gold_label(r) != r["gold"]:
                bad.append(("row", r["row_id"]))
    return gc.result("K3", not bad, cases=n, mismatches=bad[:5])


# ---- K4 balance ---------------------------------------------------------------------------------------------------------------------------
def k4_balance(records):
    rows = _clean(records)
    probs = []
    for head in M.HEADS:
        rs = [r for r in rows if r["hd"] == head]
        if not rs:
            continue
        sh = _share(rs, lambda r: r["gold"] == LABEL_A[head])
        if not 0.40 <= sh <= 0.60:
            probs.append(("head", head, round(sh, 4)))
        for key, lo, hi in (("card", .40, .60), ("world_kind", .40, .60), ("view", .40, .60)):
            grp = collections.defaultdict(list)
            for r in rs:
                grp[r[key]].append(r)
            for k, g_ in grp.items():
                s2 = _share(g_, lambda r: r["gold"] == LABEL_A[head])
                if len(g_) >= 100 and not lo <= s2 <= hi:
                    probs.append((head, key, k, round(s2, 4), len(g_)))
        lv = collections.defaultdict(list)
        for r in rs:
            lv[r["levels"]["row"]].append(r)
        for k, g_ in lv.items():
            s2 = _share(g_, lambda r: r["gold"] == LABEL_A[head])
            if len(g_) >= 100 and not 0.35 <= s2 <= 0.65:
                probs.append((head, "ladder", k, round(s2, 4)))
    return gc.result("K4", not probs, problems=probs[:10])


# ---- probes ----------------------------------------------------------------------------------------------------------------------------------
def k5_important_looking(records, harness):
    rows = [r for r in _clean(records) if r["hd"] == "h2" and r.get("cell")]          # the QUAD rows (pooled; the cell pairs share every other field)
    X = []
    for r in rows:
        f = rule.fact_by_id(r["scene"], r["scene"]["quote"])
        X.append({m: int(m in f["markers"]) for m in M.MARKERS} | {"len": len(str(f["value"])), "pos": f["idx"]})
    res = _probe("K5", rows, harness, X)
    tv = util.tv_distance(collections.Counter(len([m for m in rule.fact_by_id(r["scene"], r["scene"]["quote"])["markers"] if m in M.QUAD_MARKERS])
                                              for r in rows if r["gold"] == "KEEP"),
                          collections.Counter(len([m for m in rule.fact_by_id(r["scene"], r["scene"]["quote"])["markers"] if m in M.QUAD_MARKERS])
                                              for r in rows if r["gold"] == "DROP")) if rows else 0.0
    res["marker_count_tv"] = round(tv, 4)
    if tv > 0.05:
        res["ok"] = False
    return res


def k6_plan_overlap(records, harness):
    rows = [r for r in _clean(records) if r["hd"] == "h2"]
    X, drop_in, keep_not = [], [], []
    for r in rows:
        sc = r["scene"]
        q = rule.fact_by_id(sc, sc["quote"])
        plan_txt = " ".join(t for k, t in r["lines"] if k in ("h2_plan", "h2_planref"))
        inplan = q["handle"] in plan_txt
        X.append({"in_plan": int(inplan), "count": plan_txt.count(q["handle"])})
        (drop_in if r["gold"] == "DROP" else keep_not).append(inplan)
    res = _probe("K6", rows, harness, X)
    if drop_in and keep_not:
        d = sum(drop_in) / len(drop_in)
        k = sum(1 for x in keep_not if not x) / len(keep_not)
        res["drop_mentions_noun"] = round(d, 3)
        res["keep_without_noun"] = round(k, 3)
        if len(rows) >= 200 and (d < 0.50 or k < 0.30):
            res["ok"] = False
    return res


def h1_features(r):
    b = r["scene"]["brief"]
    return {"steps": len(b["steps"]), "vol": min(sum(f["tokens"] for f in b["files"]) // 500, 40), "needs": len(b["needs"]),
            "result": b["result_tokens"] // 100}


def k7_size_probes(records, harness):
    out = []
    for head, fn in (("h1", h1_features), ("h3", lambda r: {"n": len(r["scene"]["steps"])})):
        rows = [r for r in _clean(records) if r["hd"] == head]
        res = _probe("K7-" + head, rows, harness, [fn(r) for r in rows]) if rows else _skip("K7-" + head)
        out.append(res)
    return out


def structural_features(r, token_fn=util.approx_tokens):
    kinds = [k for k, _ in r["lines"]]
    return {"tokens": token_fn(r["rendered"]["text"]), "n_lines": len(kinds), "gold_letter": r["gold_letter"], "wording_id": r["wording"]["idx"],
            "template_id": r["template_id"], "view": r["view"], "n_event": sum(1 for k in kinds if k.startswith("h2_event"))}


def k8_structure(records, harness):
    out = []
    for head in M.HEADS:
        rows = [r for r in _clean(records) if r["hd"] == head]
        out.append(_probe("K8-" + head, rows, harness, [structural_features(r) for r in rows]) if rows else _skip("K8-" + head))
    return out


def k9_card(records, harness):
    rows = _clean(records)
    out = []
    for head in M.HEADS:
        rs = [r for r in rows if r["hd"] == head and r["edit"] not in ("card_swap", "card_swap_recovery")]
        out.append(_probe("K9-" + head, rs, harness, [{"card": r["card"]} for r in rs]) if rs else _skip("K9-" + head))
    by = collections.defaultdict(list)
    for r in rows:
        if r["edit"] in ("card_swap", "card_swap_recovery"):
            by[r["group_id"]].append(r)
    bad = []
    for gid, rs in by.items():
        if len(rs) != 2 or rs[0]["gold"] == rs[1]["gold"]:
            bad.append(gid)
            continue
        ca, cb = collections.Counter(rs[0]["lines"]), collections.Counter(rs[1]["lines"])
        if any(not k.startswith("card_") for (k, _t), _n in ((ca - cb) + (cb - ca)).items()):
            bad.append(gid)
    out.append(gc.result("K9-swaps", not bad, bad=bad[:5], n=len(by)))
    return out


def k10_quad(records):
    by = collections.defaultdict(list)
    for r in _clean(records):
        if r.get("cell"):
            by[r["group_id"]].append(r)
    bad = []
    for gid, rs in by.items():
        if sorted(r["cell"] for r in rs) != sorted(M.QUAD_CELLS.values()):
            bad.append(gid)
            continue
        base = collections.Counter(rs[0]["lines"])
        for r in rs[1:]:
            diff = (base - collections.Counter(r["lines"])) + (collections.Counter(r["lines"]) - base)
            if any(k not in ("h2_fact", "h2_quote", "h2_planref") for (k, _t), _n in diff.items()):
                bad.append(gid)
                break
        facts = {(rule.fact_by_id(r["scene"], r["scene"]["quote"])["type"], rule.fact_by_id(r["scene"], r["scene"]["quote"])["idx"]) for r in rs}
        if len(facts) != 1:
            bad.append(gid)
    return gc.result("K10", not bad, bad_groups=bad[:5], n_quads=len(by))


def k11_pair_integrity(records):
    rows = _clean(records)
    g = collections.defaultdict(list)
    for r in rows:
        if r.get("pair_role") in ("a", "b") and not r.get("cell"):
            g[r["group_id"]].append(r)
    bad = []
    for gid, rs in g.items():
        if len(rs) != 2 or rs[0]["gold"] == rs[1]["gold"]:
            bad.append(gid)
            continue
        e = rs[0]["edit"]
        ca, cb = collections.Counter(rs[0]["lines"]), collections.Counter(rs[1]["lines"])
        diff = (ca - cb) + (cb - ca)
        if not diff:
            bad.append(gid)
            continue
        for (k, _t), _n in diff.items():
            owns = M.EDIT_OWNS.get({"pointer_content": "pointer_content"}.get(e, e), set())
            if e in ("card_swap", "card_swap_recovery"):
                if not k.startswith("card_"):
                    bad.append(gid)
                    break
            elif k not in owns:
                bad.append(gid)
                break
    return gc.result("K11", not bad, bad_groups=bad[:10], n_groups=len(g))


def k12_share(records):
    rows = _clean(records)
    sh = _share(rows, lambda r: r.get("edit") is not None)
    return gc.result("K12", sh >= 0.30, share=round(sh, 4), minimum=0.30)


def k13_h2_coverage(records):
    rows = [r for r in _clean(records) if r["hd"] == "h2"]
    probs = []
    cnt = collections.Counter()
    for r in rows:
        for f in r["scene"]["facts"]:
            cnt[f["type"]] += 1
    n = sum(cnt.values()) or 1
    for t in ("V", "R", "D", "S", "P"):
        if t == "P":
            continue
        if cnt[t] / n < 0.10 and n > 300:
            probs.append(("fact type", t, round(cnt[t] / n, 3)))
    sup = collections.Counter()
    for r in rows:
        if r.get("h2kind") == "supersede" and r["gold"] == "KEEP":
            sup[len(r["scene"]["revs"]) - 1] += 1
    tot = sum(sup.values())
    if tot >= 40:
        for d, want in ((1, .5), (2, .3), (3, .2)):
            if abs(sup[d] / tot - want) > 0.05:
                probs.append(("supersession depth", d, round(sup[d] / tot, 3)))
    return gc.result("K13", not probs, problems=probs, fact_types=dict(cnt), supersession=dict(sup))


def k14_wording(records, min_forms=50):
    rows = _clean(records)
    per = collections.defaultdict(set)
    c = collections.Counter()
    for r in rows:
        q = [p for p in r["wording"]["idx"].split(".") if p.startswith("q.")]
        key = q[0] if q else r["wording"]["idx"]
        per[r["wording"]["form_id"]].add(key)
        c[(r["wording"]["form_id"], key)] += 1
    few = {f: len(v) for f, v in per.items() if len(v) < min_forms}
    n = len(rows) or 1
    top = max(c.values()) / n if c else 0.0
    return gc.result("K14", not few and top <= 0.02, forms=len(per), forms_below_min=few, top_share=round(top, 4))


def k15_tokens(records):
    return gc.token_gate("K15", _clean(records))


def k16_names(records, allowlist):
    return gc.name_guard_gate("K16", records, allowlist, "T60")


_EXEC_NAMES = {"subprocess", "eval", "exec", "__import__", "shlex", "pty"}


def k17_no_exec(files):
    bad = []
    for p in files:
        with open(p, "rb") as f:
            src = f.read()
        toks = [t for t in tokenize.tokenize(io.BytesIO(src).readline) if t.type in (tokenize.NAME, tokenize.OP)]
        for i, t in enumerate(toks):
            if t.type != tokenize.NAME:
                continue
            prev = toks[i - 1].string if i else ""
            prev2 = toks[i - 2].string if i > 1 else ""
            if t.string in _EXEC_NAMES and prev != ".":
                bad.append((os.path.basename(p), t.string, t.start[0]))
            elif t.string == "compile" and prev != "." and i + 1 < len(toks) and toks[i + 1].string == "(":
                bad.append((os.path.basename(p), t.string, t.start[0]))
            elif prev == "." and prev2 == "os" and (t.string in ("system", "popen") or t.string.startswith(("exec", "spawn"))):
                bad.append((os.path.basename(p), "os." + t.string, t.start[0]))
    return gc.result("K17", not bad, violations=bad[:10])


def k19_split(records):
    by = collections.defaultdict(set)
    bad = []
    for r in records:
        by[r["group_id"]].add(r["split"])
        by[r.get("scenario_id", r["group_id"]) + "#scn"].add(r["split"])
        if r.get("heldout_family") and r["split"] != "dev":
            bad.append((r["row_id"], "heldout outside dev"))
    bad += [(g, "split mixed") for g, s in by.items() if len(s) > 1]
    return gc.result("K19", not bad, problems=bad[:10])


TWIN_TOKEN_TOL = 0.15
FILL_MIN = 0.10
TWIN_MIN = 0.80


def marker_count(r):
    """Salience-marker count of the row (the quad markers on the quoted fact; 0 for H1 / H3 rows)."""
    if r["hd"] != "h2":
        return 0
    return len([m for m in rule.fact_by_id(r["scene"], r["scene"]["quote"])["markers"] if m in M.QUAD_MARKERS])


def k21_mechanism_fill(rows):
    """G0-lite section 5: every mechanism populates all four levels, each >= 10% of its rows (head mechanisms over the rows of the head, length over
    all rows). -> (problems, fill table)."""
    fill, probs = {}, []
    for head in M.HEADS:
        rs = [r for r in rows if r["hd"] == head]
        if not rs:
            continue
        for mech in lv.MECHS[head]:
            c = collections.Counter(r["levels"][mech] for r in rs)
            sh = [c.get(k, 0) / float(len(rs)) for k in (1, 2, 3, 4)]
            fill["%s.%s" % (head, mech)] = [round(x, 3) for x in sh]
            if mech != "length":
                probs += [("fill", head, mech, k + 1, round(x, 3)) for k, x in enumerate(sh) if x < FILL_MIN]
    if rows:
        c = collections.Counter(r["levels"]["length"] for r in rows)
        sh = [c.get(k, 0) / float(len(rows)) for k in (1, 2, 3, 4)]
        fill["all.length"] = [round(x, 3) for x in sh]
        probs += [("fill", "all", "length", k + 1, round(x, 3)) for k, x in enumerate(sh) if x < FILL_MIN]
    return probs, fill


def k21_twin_rule(rows, token_fn=util.approx_tokens):
    """K21 twin rule as amended by OWNER Record A102 (Opus Q6 follow-up): it applies only to rows whose DECISIVE mechanism (the one tied to the predicate the
    row's edit or control flips; registered in t60_levels.DECISIVE, part of the hash export) is at L3-L4. Such a row needs a twin with the OPPOSITE label, the
    same scenario-id prefix, tokens within +-15%, the same marker count and that mechanism at L2 or below; required for >= 80% of these rows.
    -> (rate, ids of the rows without a twin, rate by head, number of rows the rule applies to)."""
    by = collections.defaultdict(list)
    for r in rows:
        by[r.get("scenario_id", r["group_id"])].append(r)
    toks = {r["row_id"]: token_fn(r["rendered"]["text"]) for r in rows}
    subject = [r for r in rows if r.get("decisive", "-") != "-" and r["levels"][r["decisive"]] >= 3]
    miss, per = [], collections.defaultdict(lambda: [0, 0])
    for r in subject:
        t, mech = toks[r["row_id"]], r["decisive"]
        ok = any(s is not r and s["gold"] != r["gold"] and s["levels"][mech] <= 2 and abs(toks[s["row_id"]] - t) <= TWIN_TOKEN_TOL * t
                 and marker_count(s) == marker_count(r) for s in by[r.get("scenario_id", r["group_id"])])
        per[r["hd"]][1] += 1
        if ok:
            per[r["hd"]][0] += 1
        else:
            miss.append(r["row_id"])
    rate = 1 - len(miss) / float(len(subject)) if subject else 1.0
    return rate, miss, {h: round(a / float(b), 3) for h, (a, b) in per.items() if b}, len(subject)


def k21_ladder(records):
    rows = _clean(records)
    probs = []
    n = len(rows)
    lvl = collections.Counter(r["levels"]["row"] for r in rows)
    hi = (lvl.get(3, 0) + lvl.get(4, 0)) / n if n else 0
    l4 = lvl.get(4, 0) / n if n else 0
    if hi < 0.25:
        probs.append(("L3-L4 share", round(hi, 3)))
    if n >= 500 and l4 < 0.08:
        probs.append(("L4 share", round(l4, 3)))
    for head in M.HEADS:
        rs = [r for r in rows if r["hd"] == head]
        if len(rs) >= 200:
            h_ = _share(rs, lambda r: r["levels"]["row"] >= 3)
            l4h = _share(rs, lambda r: r["levels"]["row"] == 4)
            if h_ < 0.25:
                probs.append((head, "L3-L4", round(h_, 3)))
            if l4h < 0.05:
                probs.append((head, "L4", round(l4h, 3)))
    l4rows = [r for r in rows if r["levels"]["row"] == 4]
    if l4rows:
        sh = _share(l4rows, lambda r: r["gold"] == LABEL_A[r["hd"]])
        if max(sh, 1 - sh) > 0.55:
            probs.append(("L4 label share", round(sh, 3)))
    fill_probs, fill = k21_mechanism_fill(rows) if n >= 200 else ([], {})
    probs += fill_probs
    twin_rate, twinless, twin_by_head, n_subject = k21_twin_rule(rows) if n >= 200 else (1.0, [], {}, 0)
    if twin_rate < TWIN_MIN:
        probs.append(("twin rule", round(twin_rate, 3)))
    return gc.result("K21", not probs, problems=probs[:40], row_levels=dict(lvl), l3_l4=round(hi, 3), l4=round(l4, 3), fill=fill,
                     twin_rate=round(twin_rate, 3), twinless=len(twinless), twin_by_head=twin_by_head, twin_subject_rows=n_subject)


def k24_wrappers(records):
    from LK_COMMON import klevers
    wr = [r for r in records if r.get("lever_tag") == "lever.a10"]
    if not wr:
        return gc.result("K24", True, note="A10 not built")
    bad = [(r["row_id"], "held-out wrapper in train") for r in wr if r.get("heldout_family") is None and r["wrapper"]["family"] in klevers.WRAPPERS_HELD_OUT]
    bad += [(r["row_id"], "no clean twin") for r in wr if not r.get("twin_of")]
    return gc.result("K24", not bad, violations=bad[:5], n=len(wr))


def k25_perturbation(records):
    from LK_COMMON import klevers
    ids = {r["row_id"]: r for r in records}
    bad = []
    pr = [r for r in records if r.get("lever_tag") == "lever.a12" and r.get("a12")]
    for r in pr:
        c = ids.get(r.get("twin_of"))
        if c is None:
            bad.append((r["row_id"], "no clean twin"))
            continue
        if klevers.invert(r["rendered"]["context"], [tuple(o) for o in r["a12"]["ops"]]) != c["rendered"]["context"]:
            bad.append((r["row_id"], "inverse does not restore"))
        if r.get("heldout_family") is None and r["a12"]["transform"] in klevers.HELD_OUT:
            bad.append((r["row_id"], "held-out transform in train"))
    return gc.result("K25", not bad, violations=bad[:5], n=len(pr))


MEMORY_INSTR = re.compile(r"\b(remember|keep this|do not forget|don't forget|memori[sz]e)\b", re.I)


def k27_lints(records):
    bad = []
    for r in records:
        text = r["rendered"]["context"]
        if MEMORY_INSTR.search(text):
            bad.append((r["row_id"], "memory instruction"))
        for o in r["parts"]["outputs"]:
            if render.lint_output(o):
                bad.append((r["row_id"], "output lint"))
        if r["hd"] == "h2" and any(re.search(r"\b(only|nothing else|except|exclude)\b", t, re.I) for k, t in r["lines"] if k.startswith("h2_event")):
            bad.append((r["row_id"], "boundary-type fact"))
    return gc.result("K27", not bad, violations=bad[:5])


def k28_reference_grammar(records):
    rows = [r for r in _clean(records) if r["hd"] == "h2" and r["gold"] == "KEEP"]
    c = collections.Counter()
    unresolved = 0
    for r in rows:
        sc = r["scene"]
        star = next(s for s in sc["plan"] if s["sid"] == sc["star"])
        lv = max([ref["level"] for ref in star["refs"]] or [1])
        c[lv] += 1
        if not (rule.needs(sc) & {rule.fact_by_id(sc, sc["quote"])["id"]}):
            unresolved += 1
    n = len(rows) or 1
    probs = [("level %d" % k, round(c[k] / n, 3)) for k in (1, 2, 3, 4) if n >= 100 and c[k] / n < 0.10]
    return gc.result("K28", not probs and unresolved == 0, problems=probs, levels=dict(c), unresolved=unresolved)


def run_all(records, harness=None, allowlist=None, code_files=None):
    out = [k3_truth_tables(records), k4_balance(records), k5_important_looking(records, harness), k6_plan_overlap(records, harness)]
    out += k7_size_probes(records, harness) + k8_structure(records, harness) + k9_card(records, harness)
    out += [k10_quad(records), k11_pair_integrity(records), k12_share(records), k13_h2_coverage(records), k14_wording(records), k15_tokens(records)]
    if allowlist is not None:
        out.append(k16_names(records, allowlist))
    if code_files:
        out.append(k17_no_exec(code_files))
    out += [k19_split(records), k21_ladder(records), k24_wrappers(records), k25_perturbation(records), k27_lints(records),
            k28_reference_grammar(records)]
    return out
