"""T59 PRE-FREEZE KILL gates K1..K31 (CPU, data only) per G0-lite section 8.1 and the Opus batch-1b rulings (G2: data-audit gates are
pre-freeze; G5: ONE probe harness owned by L-0 -- this module supplies features and group keys and calls the harness through the
interface in tool_engine.gates_common). Orchestrator / program jobs, not computed here: K19 stamp drops beyond the pipeline summary,
K21 (A50 G6, A49c, G5-H, G3-H, A43(d)), K29 (C2 <= 70% on L4, od-l4b). POST-TRAINING lines (P1..P9) are never kill rules.

`run_all(records, harness, allowlist)` -> list of {id, ok, ...}. A probe gate is skipped (ok=None) when no harness is given.
"""
import collections
import io
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
import t59_oracle as orc  # noqa: E402
import t59_scene as sc  # noqa: E402
import t59_solver_a as sa  # noqa: E402

BLOCK_SHARES = {"A": 0.45, "B": 0.14, "C": 0.07, "D": 0.34}


def _clean(records):
    """Gates read the clean family rows (lever rows are checked by K26 / K27, dev-only rows are outside the 2,000)."""
    return [r for r in records if r.get("lever_tag", "lever.none") == "lever.none" and not r.get("dev_only")]


def _share(rows, pred):
    return sum(1 for r in rows if pred(r)) / len(rows) if rows else 0.0


# ---- K3 --------------------------------------------------------------------------------------------------------------------------
def k3_truth_table():
    """The plan rule (solver A) = the brute-force oracle = the pure formula, on the full cross product of (E empty, R-SAME, collapsed, R-COM,
    R-RES, any IRREV, mode) x the T6 3.3.1 sub-cases (Opus ruling Q2: none, the two forced-ASK cases, and the four PROCEED-side neighbours).
    The forced ASK is also checked against the spec sentence itself (the `forced` column of orc.T6_SUBCASES), on every card."""
    import itertools
    bad = []
    n = n_t6 = 0
    for name, (t6, forced) in orc.T6_SUBCASES.items():
        for fl in itertools.product([False, True], repeat=6):
            for mode in ("ON", "OFF"):
                e_empty, r_same, collapsed, r_com, r_res, any_irrev = fl
                case = orc.case_from_flags(e_empty, r_same, collapsed, r_com, r_res, any_irrev, mode, t6=t6)
                a, o = sa.gold_case(case), orc.oracle_label(case)
                f = sa.gold_formula(e_empty, r_same, collapsed, r_com, r_res, any_irrev, mode, t6_ask=forced)
                n += 1
                n_t6 += t6 is not None
                if not (a == o == f):
                    bad.append((name, fl, mode, a, o, f))
                robust = r_same or collapsed or r_com or r_res
                if forced and not e_empty and not robust and a != "ASK":       # 3.3.1: ASK on every card, undo path or not
                    bad.append((name, fl, mode, a, "3.3.1 says ASK"))
    for cid in list(sa.IMPORTED_KINDS) + ["card.t50.c03", "card.t51.c02"]:
        p = sa.imported_params(cid)
        assert p["mode"] == "OFF"
    return gc.result("K3", not bad, cases=n, cases_t6=n_t6, mismatches=bad[:5])


# ---- K4 ---------------------------------------------------------------------------------------------------------------------------
def k4_balance(records):
    rows = _clean(records)
    n = len(rows)
    ask = _share(rows, lambda r: r["gold"] == "ASK")
    probs = []
    if 1 - ask < 0.55 or ask < 0.35 or 1 - ask > 0.65:
        probs.append(("family", round(ask, 4)))
    for key in ("trigger", "form", "card", "world_kind", "view"):
        grp = collections.defaultdict(list)
        for r in rows:
            grp[r[key] if key != "card" else r["card"]].append(r)
        for k, rs in grp.items():
            sh = _share(rs, lambda r: r["gold"] == "ASK")
            if key == "trigger":
                if len(rs) >= 40 and not 0.39 <= sh <= 0.45:
                    probs.append((key, k, round(sh, 4)))
            elif key == "form":
                if len(rs) >= 40 and abs(sh - ask) > 0.05:
                    probs.append((key, k, round(sh, 4)))
            elif len(rs) >= 100 and not 0.36 <= sh <= 0.48:
                probs.append((key, k, round(sh, 4), len(rs)))
    blocks = collections.Counter(r["block"] for r in rows)
    for b, want in BLOCK_SHARES.items():
        if n and abs(blocks.get(b, 0) / n - want) > 0.02 + 0.5 / max(1, n) * 10:
            probs.append(("block", b, round(blocks.get(b, 0) / n, 4), want))
    return gc.result("K4", not probs, problems=probs, ask=round(ask, 4), n=n)


# ---- probes -------------------------------------------------------------------------------------------------------------------------
def _probe(gid, rows, harness, X, **extra):
    if harness is None:
        return dict(id=gid, ok=None, skipped="no probe harness")
    y = [int(r["gold"] == "ASK") for r in rows]
    groups = [r["group_id"] for r in rows]
    return gc.probe_binary_gate(gid, harness, X, y, groups, **extra)


def structural_features(r, token_fn=util.approx_tokens):
    kinds = [k for k, _ in r["lines"]]
    case = sc.derive_case(r["scene"])
    return {"tokens": token_fn(r["rendered"]["text"]), "n_tools": sum(1 for k in kinds if k.startswith("tool_") and k != "tools_header"),
            "n_user": sum(1 for k in kinds if k.startswith("user_")), "n_slots": len(case["slots"]), "gold_letter": r["gold_letter"],
            "wording_id": r["wording"]["idx"], "template_id": r["template_id"], "form": r["form"], "view": r["view"],
            "n_hist": sum(1 for k in kinds if k == "hist_call")}


def k_vis(r):
    s = r["scene"]
    if s["trigger"] == "T1":
        return len(s["t"]["cands"])
    if s["trigger"] in ("T2", "T4", "T8"):
        return sum(1 for k, _ in r["lines"] if k == "cand" and not _.startswith(("     count", "count")) and ("(" in _ or "=" in _))
    return 0


def k5_trigger_only(records, harness):
    rows = _clean(records)
    X = [{"trigger": r["trigger"], "form": r["form"], "view": r["view"], "world": r["world_kind"], "card": r["card"]} for r in rows]
    return _probe("K5", rows, harness, X)


def k6_request_only(records, harness):
    rows = _clean(records)
    return _probe("K6", rows, harness, [r["parts"]["user"] for r in rows])


def k7_value_span_parity(records):
    rows = _clean(records)
    dist = {lab: collections.Counter() for lab in ("ASK", "PROCEED")}
    for r in rows:
        dist[r["gold"]][min(render.count_value_spans(r["parts"]["user"]), 12)] += 1
    d = util.tv_distance(dist["ASK"], dist["PROCEED"])
    return gc.result("K7", d <= 0.05, tv=round(d, 4), bar=0.05, reference_rows=0, note="no reference-phrased rows are generated")


def k8_structure(records, harness):
    rows = _clean(records)
    return _probe("K8", rows, harness, [structural_features(r) for r in rows])


def k9_card(records, harness):
    rows = _clean(records)
    body = [r for r in rows if r["block"] != "C"]
    res = _probe("K9", body, harness, [{"card": r["card"]} for r in body]) if body else dict(id="K9", ok=None)
    by = collections.defaultdict(list)
    for r in rows:
        if r["block"] == "C":
            by[r["group_id"]].append(r)
    bad = []
    for gid, rs in by.items():
        if len(rs) != 2 or rs[0]["gold"] == rs[1]["gold"]:
            bad.append(gid)
            continue
        ca, cb = collections.Counter(rs[0]["lines"]), collections.Counter(rs[1]["lines"])
        if any(not k.startswith("card_") for (k, _t), _n in ((ca - cb) + (cb - ca)).items()):
            bad.append(gid)
    res["swap_pairs"] = len(by)
    res["swap_bad"] = bad[:10]
    if bad:
        res["ok"] = False
    return res


def k10_candidate_count(records, harness):
    rows = _clean(records)
    res = _probe("K10", rows, harness, [{"k": min(k_vis(r), 4)} for r in rows])
    k2 = [r for r in rows if k_vis(r) >= 2]
    sh = _share(k2, lambda r: r["gold"] == "PROCEED")
    res["k2_proceed_share"] = round(sh, 4)
    if k2 and len(k2) >= 40 and not 0.35 <= sh <= 0.55:
        res["ok"] = False
    return res


def k11_alarm(records, harness):
    rows = _clean(records)
    probs = []
    for key in ("gold", "trigger"):
        grp = collections.defaultdict(list)
        for r in rows:
            grp[r[key]].append(r)
        for k, rs in grp.items():
            sh = _share(rs, lambda r: r["alarm"])
            if len(rs) >= 40 and not 0.25 <= sh <= 0.35:
                probs.append((key, k, round(sh, 4)))
    res = _probe("K11", rows, harness, [{"alarm": int(r["alarm"])} for r in rows])
    res["problems"] = probs
    if probs:
        res["ok"] = False
    return res


def k12_edit_coverage(records):
    rows = [r for r in _clean(records) if r["block"] in ("A", "B") and r.get("edit") and r["edit"] != "swap" and r.get("pair_role") == "a"]
    probs = []
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        by[r["trigger"]][r["edit"]] += 1
    for tr, c in by.items():
        n = sum(c.values())
        if len(c) < 3 and n >= 20:
            probs.append((tr, "fewer than 3 edit fields"))
        for e, k in c.items():
            if n >= 20 and (k / n > 0.40 or k / n < 0.02):
                probs.append((tr, e, round(k / n, 3)))
    for r in _clean(records):
        if r.get("edit") in sc.ON_ONLY_EDITS and r["card_mode"] != "ON":
            probs.append((r["row_id"], "ON-only edit on an OFF card"))
    return gc.result("K12", not probs, problems=probs[:10], by_trigger={t: dict(c) for t, c in by.items()})


def k13_pair_share(records):
    rows = _clean(records)
    sh = _share(rows, lambda r: r["block"] in ("A", "B", "C"))
    return gc.result("K13", sh >= 0.30, share=round(sh, 4), minimum=0.30)


def k14_pair_integrity(records):
    rows = _clean(records)
    g = collections.defaultdict(list)
    for r in rows:
        if r.get("pair_role") in ("a", "b"):
            g[r["group_id"]].append(r)
    bad = []
    for gid, rs in g.items():
        if len(rs) != 2 or rs[0]["gold"] == rs[1]["gold"]:
            bad.append(gid)
            continue
        e = rs[0].get("edit")
        ca, cb = collections.Counter(rs[0]["lines"]), collections.Counter(rs[1]["lines"])
        diff = (ca - cb) + (cb - ca)
        if not diff:
            bad.append(gid)
            continue
        for (k, _t), _n in diff.items():
            if (e == "swap" and not k.startswith("card_")) or (e != "swap" and k not in sc.EDIT_OWNS.get(e, ())):
                bad.append(gid)
                break
    return gc.result("K14", not bad, bad_groups=bad[:10], n_groups=len(g))


def k15_wording(records):
    rows = _clean(records)
    per = collections.defaultdict(set)
    c = collections.Counter()
    for r in rows:
        per[r["wording"]["form_id"]].add(r["wording"]["idx"].split(".")[0])
        c[(r["wording"]["form_id"], r["wording"]["idx"].split(".")[0])] += 1
    few = {f: len(v) for f, v in per.items() if len(v) < 50}
    n = len(rows) or 1
    top = max(c.values()) / n if c else 0.0
    return gc.result("K15", not few and top <= 0.02, forms=len(per), forms_below_50=few, top_share=round(top, 4),
                     note="until the expanded pool is plugged in the seed pool fails this gate by design")


def k16_tokens(records, token_fn=util.approx_tokens):
    return gc.token_gate("K16", _clean(records), token_fn)


def k17_names(records, allowlist):
    return gc.name_guard_gate("K17", records, allowlist, "T59")


_EXEC_NAMES = {"subprocess", "eval", "exec", "__import__", "shlex", "pty"}


def k18_no_exec(files):
    """No subprocess / exec / eval on a rendered string: scan the family's code for those names OUTSIDE comments and strings. `compile`
    is flagged only as a builtin call (not `re.compile`); `os.system` / `os.popen` / `os.exec*` are flagged."""
    bad = []
    for p in files:
        with open(p, "rb") as f:
            src = f.read()
        try:
            toks = [t for t in tokenize.tokenize(io.BytesIO(src).readline) if t.type in (tokenize.NAME, tokenize.OP)]
        except tokenize.TokenError:
            bad.append((os.path.basename(p), "untokenisable"))
            continue
        for i, t in enumerate(toks):
            if t.type != tokenize.NAME:
                continue
            prev = toks[i - 1].string if i else ""
            prev2 = toks[i - 2].string if i > 1 else ""
            if t.string in _EXEC_NAMES and prev != ".":
                bad.append((os.path.basename(p), t.string, t.start[0]))
            elif t.string == "compile" and prev != "." and i + 1 < len(toks) and toks[i + 1].string == "(":
                bad.append((os.path.basename(p), t.string, t.start[0]))
            elif prev == "." and prev2 == "os" and (t.string in ("system", "popen") or t.string.startswith("exec") or t.string.startswith("spawn")):
                bad.append((os.path.basename(p), "os." + t.string, t.start[0]))
    return gc.result("K18", not bad, violations=bad[:10])


def k20_split(records):
    rows = records
    bad = []
    by = collections.defaultdict(set)
    for r in rows:
        by[r["group_id"]].add(r["split"])
        if r.get("heldout_family") and r.get("split") != "dev":
            bad.append((r["row_id"], "heldout_family outside dev"))
    bad += [(g, "split mixed") for g, s in by.items() if len(s) > 1]
    return gc.result("K20", not bad, problems=bad[:10])


def k22_ladder(records):
    rows = _clean(records)
    n = len(rows)
    lv = collections.Counter(r["levels"]["row"] for r in rows)
    hi = (lv.get(3, 0) + lv.get(4, 0)) / n if n else 0
    l4 = lv.get(4, 0) / n if n else 0
    probs = []
    if hi < 0.25:
        probs.append(("L3-L4 share", round(hi, 4)))
    if n >= 500 and l4 < 0.08:
        probs.append(("L4 share", round(l4, 4)))
    l4rows = [r for r in rows if r["levels"]["row"] == 4]
    if l4rows:
        sh = _share(l4rows, lambda r: r["gold"] == "ASK")
        if max(sh, 1 - sh) > 0.55:
            probs.append(("L4 label share", round(sh, 4)))
    mech = {}
    for m in ("certainty", "intent", "slot", "undo", "stakes", "resolver", "length"):
        rs = [r for r in rows if r.get("prim") == m]
        c = collections.Counter(r["levels"][m] for r in rs)
        mech[m] = {k: round(c.get(k, 0) / len(rs), 3) if rs else None for k in (1, 2, 3, 4)}
        if len(rs) >= 80:
            for k in (1, 2, 3, 4):
                if c.get(k, 0) / len(rs) < 0.10:
                    probs.append((m, "level %d below 10%% of its rows" % k, round(c.get(k, 0) / len(rs), 3)))
    return gc.result("K22", not probs, problems=probs[:12], row_levels=dict(lv), l3_l4=round(hi, 4), l4=round(l4, 4), mech=mech)


def k24_k25(records):
    import t59_checked as ck
    bad24, bad25 = [], []
    import t59_repo as repo
    for r in _clean(records):
        if r["scene"]["world"] == "repo":
            p = repo.k24(r)
            if p:
                bad24.append((r["row_id"], p))
        p25 = ck.observability_problems(r)
        if p25:
            bad25.append((r["row_id"], p25))
    return [gc.result("K24", not bad24, violations=bad24[:5]), gc.result("K25", not bad25, violations=bad25[:5])]


def k26_wrappers(records, harness=None):
    from LK_COMMON import klevers
    wr = [r for r in records if r.get("lever_tag") == "lever.a10"]
    if not wr:
        return gc.result("K26", True, note="A10 not built")
    bad = []
    for r in wr:
        if r.get("heldout_family") is None and r["wrapper"]["family"] in klevers.WRAPPERS_HELD_OUT:
            bad.append((r["row_id"], "held-out wrapper in train"))
        if not r.get("twin_of"):
            bad.append((r["row_id"], "no clean twin"))
    return gc.result("K26", not bad, violations=bad[:5], n=len(wr))


def k27_perturbation(records):
    from LK_COMMON import klevers
    pr = [r for r in records if r.get("lever_tag") == "lever.a12" and r.get("a12")]
    bad = []
    clean_ids = {r["row_id"] for r in records}
    for r in pr:
        if not r.get("twin_of") or r["twin_of"] not in clean_ids:
            bad.append((r["row_id"], "no clean twin"))
            continue
        back = klevers.invert(r["rendered"]["context"], [tuple(o) for o in r["a12"]["ops"]])
        clean = next(c for c in records if c["row_id"] == r["twin_of"])
        if back != clean["rendered"]["context"]:
            bad.append((r["row_id"], "inverse does not restore"))
        if r.get("heldout_family") is None and r["a12"]["transform"] in klevers.HELD_OUT:
            bad.append((r["row_id"], "held-out transform in train"))
    return gc.result("K27", not bad, violations=bad[:5], n=len(pr))


def k30_resolver_default(records):
    rows = [r for r in _clean(records) if r["gold"] == "PROCEED"]
    n = len(rows) or 1
    settled = sum(1 for r in rows if r["trace"]["rule"] == "robust" and (r["trace"]["r_res"] or any(
        sa.collapse(s, sc.derive_case(r["scene"])["defaults_count"])[1] in ("default", "precedence") for s in sc.derive_case(r["scene"])["slots"])))
    com = sum(1 for r in rows if r["trace"]["rule"] == "robust" and r["trace"]["r_com"] and not r["trace"]["r_def"] and not r["trace"]["r_same"])
    rev = sum(1 for r in rows if r["trace"]["rule"] == "on_reversible")
    probs = []
    if not 0.15 <= settled / n <= 0.25:
        probs.append(("settled", round(settled / n, 3)))
    if com / n < 0.08:
        probs.append(("common_step", round(com / n, 3)))
    if not 0.25 <= rev / n <= 0.40:
        probs.append(("reversibility", round(rev / n, 3)))
    return gc.result("K30", not probs, problems=probs, settled=round(settled / n, 3), common=round(com / n, 3), reversible=round(rev / n, 3))


def k31_delegation(records, harness):
    rows = _clean(records)
    real = [r for r in rows if any(k == "user_delegation" for k, _ in r["lines"])]
    decoy = [r for r in rows if any(k == "user_decoy" for k, _ in r["lines"])]
    carrying = real + decoy
    probs = []
    if carrying:
        sh = _share(carrying, lambda r: r["gold"] == "PROCEED")
        if len(carrying) >= 40 and not 0.45 <= sh <= 0.60:
            probs.append(("proceed_share", round(sh, 3)))
        if len(carrying) >= 40 and len(decoy) / len(carrying) < 0.30:
            probs.append(("decoy_share", round(len(decoy) / len(carrying), 3)))
    res = _probe("K31", rows, harness, [{"deleg": int(any(k in ("user_delegation", "user_decoy") for k, _ in r["lines"]))} for r in rows])
    res["problems"] = probs
    res["n_real"], res["n_decoy"] = len(real), len(decoy)
    if probs:
        res["ok"] = False
    return res


def run_all(records, harness=None, allowlist=None, code_files=None):
    out = [k3_truth_table(), k4_balance(records), k5_trigger_only(records, harness), k6_request_only(records, harness),
           k7_value_span_parity(records), k8_structure(records, harness), k9_card(records, harness),
           k10_candidate_count(records, harness), k11_alarm(records, harness), k12_edit_coverage(records), k13_pair_share(records),
           k14_pair_integrity(records), k15_wording(records), k16_tokens(records)]
    if allowlist is not None:
        out.append(k17_names(records, allowlist))
    if code_files:
        out.append(k18_no_exec(code_files))
    out += [k20_split(records), k22_ladder(records)] + k24_k25(records) + [k26_wrappers(records), k27_perturbation(records),
                                                                         k30_resolver_default(records), k31_delegation(records, harness)]
    return out
