"""T56 (done-claim half) PRE-FREEZE KILL gates (CPU, data only) per G0-lite 5.1 and the Opus rulings of 18 Oct (G2, G5, G6,
G7, T56 ruling 4: P-8 is a PRE-FREEZE KILL gate with bars AUC <= 0.65 and upper bound <= 0.70).
Orchestrator-run, not computed here: P-17 (200-row G13 pilot) and P-18 (collisions with the frozen evaluation set). POST-TRAINING lines R-1..R-6 are
never kill rules and are not here. Probes call L-0's harness through tool_engine.gates_common."""
import collections
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import gates_common as gc  # noqa: E402
from tool_engine import perturb, render, util  # noqa: E402
import t56_env as E  # noqa: E402
import t56_generator as gen  # noqa: E402
import t56_solver_a as sa  # noqa: E402

POSITIVE = ("DONE", "READY")


def _pos(r):
    return int(r["gold"] in POSITIVE)


def expected_mix():
    return {sb: dict(m) for sb, m in gen.LABEL_MIX.items()}


def p2_sizes_mixes(records):
    res = [gc.size_mix_gate("P-2", records, gen.SIZES, expected_mix(), fam_tol=0.02, mix_tol=0.03)]
    probs = []
    for sb in gen.SUB_BLOCKS:
        rs = [r for r in records if r["sub_block"] == sb and not r.get("head")]
        if not rs:
            continue
        pos = sum(_pos(r) for r in rs) / len(rs)
        if not 0.45 <= pos <= 0.55:
            probs.append((sb, round(pos, 4)))
        neg = [r for r in rs if not _pos(r)]
        rm = collections.Counter(r["gold_reason"] for r in neg)
        for reason, nominal in gen.REASON_MIX[sb].items():
            want = nominal / float(sum(gen.REASON_MIX[sb].values()))
            got = rm.get(reason, 0) / max(1, len(neg))
            if abs(got - want) > 0.03:
                probs.append((sb, reason, round(got, 4), round(want, 4)))
    res.append(gc.result("P-2:reasons_done_share", not probs, problems=probs))
    return res


def p3_pair_identity(records):
    """Byte-identical closing claim, task statement and call skeleton in 100% of pairs (D5: claim and task only)."""
    by = collections.defaultdict(dict)
    for r in records:
        if r["pair_role"] in ("a", "b") and not r.get("head"):
            by[r["group_id"]][r["pair_role"]] = r
    bad = []
    for gid, d in by.items():
        if set(d) != {"a", "b"}:
            bad.append((gid, "incomplete"))
            continue
        a, b = d["a"], d["b"]
        ok = a["claim"] == b["claim"] and a["task_text"] == b["task_text"]
        if a["sub_block"] != "d5_unverified":
            ok = ok and a["skeleton"] == b["skeleton"]
        if not ok:
            bad.append(gid)
    return gc.result("P-3", not bad, n_pairs=len(by), bad=bad[:5])


def p4_claim_only(records, harness):
    rs = [r for r in records if not r.get("head")]
    out = [gc.probe_binary_gate("P-4:pooled", harness, [r["claim"] for r in rs], [_pos(r) for r in rs], [r["group_id"] for r in rs])]
    for sb in gen.SUB_BLOCKS:
        x = [r for r in rs if r["sub_block"] == sb]
        if len(x) >= 60 and len({_pos(r) for r in x}) > 1:
            out.append(gc.probe_binary_gate("P-4:%s" % sb, harness, [r["claim"] for r in x], [_pos(r) for r in x], [r["group_id"] for r in x]))
    return out


def p5_task_only(records, harness):
    rs = [r for r in records if not r.get("head")]
    return gc.probe_binary_gate("P-5", harness, [r["task_text"] for r in rs], [_pos(r) for r in rs], [r["group_id"] for r in rs])


def structural_features(r, token_fn=util.approx_tokens):
    return {"tokens": token_fn(r["rendered"]["text"]), "n_calls": len(r["calls"]) - sum(1 for c in r["calls"] if c["kind"] == "check" and r["fault"] == "f_no_check"),
            "n_output_lines": sum(o.count("\n") + 1 for o in r["parts"]["outputs"]), "output_chars": sum(len(o) for o in r["parts"]["outputs"]),
            "stage": r["stage"], "wording_id": r["wording"]["idx"], "template_id": r["template_id"], "gold_letter": r["gold_letter"]}


def p6_structure(records, harness):
    rs = [r for r in records if not r.get("head")]
    return gc.probe_binary_gate("P-6", harness, [structural_features(r) for r in rs], [_pos(r) for r in rs], [r["group_id"] for r in rs])


def p7_reason_head(records, harness):
    rs = [r for r in records if not r.get("head") and not _pos(r)]
    X = [r["claim"] + " " + r["task_text"] for r in rs]
    res = harness.kway(X, [r["gold_reason"] for r in rs], [r["group_id"] for r in rs], 8)
    lo, hi = gc.kway_bars(8)
    return gc.result("P-7", res.get("valid", True) and res["bacc"] <= lo and res["upper"] <= hi, bacc=round(res["bacc"], 4),
                     upper=round(res["upper"], 4), bars=[round(lo, 4), round(hi, 4)])


def p8_hard_bin_outputs(records, harness, auc_bar=0.65, upper_bar=0.70):
    """KILL gate (ruling 4): outputs-only probe on the HARD BIN -- CONTINUE rows whose fault is a relation, against their
    matched DONE partners. A sanity bar that relation faults are not keyword-readable, not a near-chance bar."""
    by = collections.defaultdict(dict)
    for r in records:
        if r["pair_role"] in ("a", "b") and not r.get("head"):
            by[r["group_id"]][r["pair_role"]] = r
    rows = []
    for gid, d in by.items():
        if len(d) == 2 and d["b"]["fault"] in perturb.HARD_FAULTS:
            rows += [d["a"], d["b"]]
    if len(rows) < 40:
        return gc.result("P-8", True, note="too few hard-bin pairs (%d rows) for a probe at this size" % len(rows))
    X = ["\n".join(r["parts"]["outputs"]) for r in rows]
    return gc.probe_binary_gate("P-8", harness, X, [_pos(r) for r in rows], [r["group_id"] for r in rows], auc_bar=auc_bar,
                                upper_bar=upper_bar, hard_bin_rows=len(rows))


def p9_claims(records, min_forms=50):
    by = collections.defaultdict(list)
    for r in records:
        if not r.get("head"):
            by[r["claim_wording"]].append(_pos(r))
    probs = [(c[:40], len(v), round(sum(v) / len(v), 3)) for c, v in by.items() if len(v) >= 20 and not 0.40 <= sum(v) / len(v) <= 0.60]
    return gc.result("P-9:claim_done_share", not probs, problems=probs[:5], n_claims=len(by), min_forms=min_forms,
                     enough_wordings=len(by) >= min_forms)


def p10_stages(records):
    probs = []
    for sb in gen.SUB_BLOCKS:
        rs = [r for r in records if r["sub_block"] == sb and not r.get("head")]
        if len(rs) < 30:
            continue
        c = collections.Counter(r["stage"] for r in rs)
        for st in gen.STAGES:
            sh = c.get(st, 0) / len(rs)
            if not 0.30 <= sh <= 0.37:
                probs.append((sb, st, round(sh, 4)))
            xs = [r for r in rs if r["stage"] == st]
            if len(xs) >= 20 and not 0.40 <= sum(_pos(r) for r in xs) / len(xs) <= 0.60:
                probs.append((sb, st, "done_share", round(sum(_pos(r) for r in xs) / len(xs), 4)))
    return gc.result("P-10", not probs, problems=probs)


def p11_sufficiency(records):
    bad = []
    for r in records:
        if r.get("head"):
            continue
        p = sa.evidence_sufficiency(r)
        if p:
            bad.append((r["row_id"], p[0]))
    return gc.result("P-11", not bad, n_bad=len(bad), bad=bad[:5], note="structural check; solver B's recovery of every predicate status is the full test")


def p12_fault_coverage(records):
    probs = []
    neg_all = [r for r in records if not _pos(r) and not r.get("head")]
    for sb in gen.SUB_BLOCKS:
        neg = [r for r in neg_all if r["sub_block"] == sb]
        c = collections.Counter(r["fault"] for r in neg)
        for f, n in c.items():
            if len(neg) >= 40 and n / len(neg) < 0.05:
                probs.append((sb, f, round(n / len(neg), 4)))
    hard = sum(1 for r in neg_all if r["fault"] in perturb.HARD_FAULTS)
    hshare = hard / len(neg_all) if neg_all else 0
    if hshare < 0.40:
        probs.append(("hard_bin", round(hshare, 4)))
    return gc.result("P-12", not probs, problems=probs, hard_bin_share=round(hshare, 4))


def p13_output_lint(records):
    bad = []
    for r in records:
        for o in r["parts"]["outputs"]:
            v = render.lint_output(o)
            if v:
                bad.append((r["row_id"], v[0]))
    return gc.result("P-13", not bad, violations=bad[:10], n=len(bad))


def p19_letters(records):
    rs = [r for r in records if not r.get("head")]
    out = []
    for sb in gen.SUB_BLOCKS:
        xs = [r for r in rs if r["sub_block"] == sb]
        if len(xs) >= 40:
            a = sum(r["gold_letter"] == "A" for r in xs) / len(xs)
            out.append(gc.result("P-19:%s" % sb, abs(a - 0.5) <= 0.03, share_A=round(a, 4)))
    return out


def p20_reachability(records):
    """D3: reachability gold equals an independent graph search (BFS vs DFS) on 100% of rows."""
    d3 = [r for r in records if r["sub_block"] == "d3_demo_only" and not r.get("head")]
    bad = []
    for r in d3:
        g = r["hidden"]["final"]["graph"]
        c = next(c for c in r["criteria"] if c["pred"] == "reachable")
        if E.reachable(g, c["item"]) != E.reachable_dfs(g, c["item"]):
            bad.append(r["row_id"])
    return gc.result("P-20", not bad, n=len(d3), bad=bad[:5], executed_slice="not run: needs the signed-off sandbox (symbolic gold only)")


def head_share(records, heads):
    """G7: head rows come from at most 25% of the family's specs."""
    specs = {r["group_id"] for r in records if not r.get("head")}
    hs = {h["group_id"] for h in heads}
    return gc.result("G7:head_share", len(hs) <= 0.25 * len(specs) + 1, share=round(len(hs) / max(1, len(specs)), 4))


def run_all(records, harness=None, allowlist=None, solver_b_fn=None, token_fn=util.approx_tokens, min_forms=50):
    res = p2_sizes_mixes(records) + [p3_pair_identity(records), gc.pair_integrity(records), p9_claims(records, min_forms),
                                    p10_stages(records), p11_sufficiency(records), p12_fault_coverage(records), p13_output_lint(records),
                                    gc.token_gate("P-14", [r for r in records if not r.get("head")], token_fn),
                                    gc.slot_survival_gate("P-15", records), gc.pair_share_gate("P-pairs", records, 0.60),
                                    p20_reachability(records)]
    res += p19_letters(records)
    res += [gc.wording_gate("P-9:wording", records, min_forms=min_forms), gc.template_share_gate("P-9:template", records)]
    if allowlist is not None:
        res.append(gc.name_guard_gate("P-16", [r for r in records], allowlist, "T56"))
    if harness is not None:
        res += p4_claim_only(records, harness) + [p5_task_only(records, harness), p6_structure(records, harness),
                                                  p7_reason_head(records, harness), p8_hard_bin_outputs(records, harness)]
    if solver_b_fn is not None:
        res.append(gc.agreement_gate("P-1", [r for r in records if not r.get("head")], solver_b_fn, 0.01))
    return res
