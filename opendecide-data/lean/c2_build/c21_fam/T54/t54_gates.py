"""T54 PRE-FREEZE KILL gates (CPU, data only) per G0-lite 5.1 and the Opus rulings of 18 Oct (G2: data-audit gates are
pre-freeze; G5: ONE probe harness owned by L-0 -- this module supplies features and group keys and calls the harness
through the interface in tool_engine.gates_common).

Gates P-15 (200-row G13 pilot) and P-16 (collisions with the frozen evaluation set) are ORCHESTRATOR/program jobs, not computed here.
POST-TRAINING lines (R-1..R-7, incl. the call/no-call recall and logit offset) are never kill rules and are not here.
"""
import collections
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import gates_common as gc  # noqa: E402
from tool_engine import render, util  # noqa: E402
import t54_generator as gen  # noqa: E402
import t54_solver_a as sa  # noqa: E402

CALL_SBS = ("s1_need4", "s3_limit", "s4_precond")
NBIN_EDGES = ((2, 3), (4, 6), (7, 10), (11, 16), (17, 25))


def _nbin(n):
    for i, (lo, hi) in enumerate(NBIN_EDGES):
        if lo <= n <= hi:
            return i
    return 4 if n > 25 else 0


def expected_mix():
    """Label mix per sub-block derived from the entries (P-2 reference)."""
    out = {}
    for sb, mix in gen.LABEL_MIX.items():
        out[sb] = dict(mix)
    return out


def p2_sizes_mix(records):
    return gc.size_mix_gate("P-2", records, gen.SIZES, expected_mix())


def p3_call_nocall(records):
    """Call/no-call share 40-60% per sub-block (S1, S3, S4) and, for every (sub-block x card x N-bin) cell with
    >= 100 rows, 35-65%."""
    probs, rows = [], []
    for sb in CALL_SBS:
        rs = [r for r in records if r["sub_block"] == sb]
        if not rs:
            continue
        sh = sum(r["call_bearing"] for r in rs) / len(rs)
        rows.append((sb, round(sh, 4), len(rs)))
        if not 0.40 <= sh <= 0.60:
            probs.append(("sub_block", sb, round(sh, 4)))
        cells = collections.defaultdict(list)
        for r in rs:
            cells[(r["card"], _nbin(len(r["tools"])))].append(r["call_bearing"])
        for k, v in cells.items():
            if len(v) >= 100 and not 0.35 <= sum(v) / len(v) <= 0.65:
                probs.append(("cell", sb, k, round(sum(v) / len(v), 4), len(v)))
    return gc.result("P-3", not probs, problems=probs, shares=rows)


def p4_limit_awareness(records):
    s3 = [r for r in records if r["sub_block"] == "s3_limit"]
    n = len(records)
    probs = []
    share = len(s3) / n if n else 0
    if abs(share - 0.20) > 0.02:
        probs.append(("s3_share", round(share, 4)))
    kinds = collections.Counter(r["perturb"] for r in s3)
    dele = {k: kinds.get(k, 0) for k in ("perturb.del_tool", "perturb.del_param", "perturb.del_result")}
    nd = sum(dele.values())
    for k, v in dele.items():
        if nd and abs(v / nd - 1 / 3.0) > 0.03:
            probs.append((k, round(v / nd, 4)))
    nul = kinds.get("perturb.null_del", 0)
    if s3 and abs(nul / len(s3) - 0.15) > 0.03:
        probs.append(("null_share", round(nul / len(s3), 4)))
    # each deleted row has an intact twin (same group_id, pair_role b, gold CALL) in >= 85% of cases
    twins = {r["group_id"] for r in s3 if r["perturb"] == "perturb.none" and r["pair_role"] == "b"}
    with_twin = sum(1 for r in s3 if r["perturb"] in dele and r["group_id"] in twins)
    if nd and with_twin / nd < 0.85:
        probs.append(("twin_rate", round(with_twin / nd, 4)))
    return gc.result("P-4", not probs, problems=probs, deleted=dele, null=nul, twin_rate=round(with_twin / nd, 4) if nd else None)


def probe_inputs(records, sb, which):
    """Features/groups named by the G0-lite for the probes. Returns (X, y_binary, y_label, groups)."""
    rs = [r for r in records if r["sub_block"] == sb]
    if which == "request":
        X = [r["parts"]["request"] for r in rs]            # the final user request only
    elif which == "toollist_card":
        X = [r["parts"]["card"] + "\n" + r["parts"]["tools"] for r in rs]
    elif which == "structural":
        X = [structural_features(r) for r in rs]
    elif which == "context":
        X = [r["parts"]["user"] + "\n" + "\n".join(r["parts"]["outputs"]) + "\n" + r["parts"]["tail"] for r in rs]
    elif which == "options":
        X = [" || ".join(o["text"] for o in r["options"]) for r in rs]
    else:
        raise ValueError(which)
    yb = [int(r["call_bearing"]) for r in rs]
    yl = [r["gold"] if sb not in ("s2_pick", "s6_parseq") else r["gold_letter"] for r in rs]
    groups = [r["group_id"] for r in rs]
    return X, yb, yl, groups


def structural_features(r, token_fn=util.approx_tokens):
    t = r["tools"]
    return {"tokens": token_fn(r["rendered"]["text"]), "n_tools": len(t), "n_distractors": max(0, len(t) - 1),
            "n_params": sum(len(x["params"]) for x in t), "gold_letter": r["gold_letter"],
            "turn_count": r["parts"]["conversation"].count("User:"), "wording_id": r["wording"]["idx"],
            "template_id": r["template_id"], "view": r["view"], "n_cards": len(r["cards"])}


def p5a_request_only(records, harness):
    out = []
    for sb in CALL_SBS:
        X, yb, _yl, grp = probe_inputs(records, sb, "request")
        if len(set(yb)) > 1:
            out.append(gc.probe_binary_gate("P-5a:%s" % sb, harness, X, yb, grp, sub_block=sb))
    return out


def p5b_toollist_card(records, harness):
    out = []
    for sb in CALL_SBS:
        X, yb, _yl, grp = probe_inputs(records, sb, "toollist_card")
        if len(set(yb)) > 1:
            out.append(gc.probe_binary_gate("P-5b:%s" % sb, harness, X, yb, grp, sub_block=sb))
    return out


def p5c_structural(records, harness):
    out = []
    for sb in CALL_SBS:
        X, yb, yl, grp = probe_inputs(records, sb, "structural")
        if len(set(yb)) > 1:
            out.append(gc.probe_binary_gate("P-5c:%s:binary" % sb, harness, X, yb, grp, sub_block=sb))
        k = len(set(yl))
        if k > 1:
            lo, hi = 0.28, 0.31
            res = harness.kway(X, yl, grp, 4)
            ok = res.get("valid", True) and res["bacc"] <= lo and res["upper"] <= hi
            out.append(gc.result("P-5c:%s:4way" % sb, ok, bacc=round(res["bacc"], 4), upper=round(res["upper"], 4), bars=[lo, hi]))
    return out


def p5d_s5(records, harness):
    X, yb, _yl, grp = probe_inputs(records, "s5_argground", "context")
    ybin = [1 if r["gold"] == "GROUNDED" else 0 for r in records if r["sub_block"] == "s5_argground"]
    # length / span-count matching inside pairs is checked separately (pair_match_s5)
    return gc.probe_binary_gate("P-5d", harness, X, ybin, grp)


def pair_match_s5(records, token_fn=util.approx_tokens):
    """Pairs in S5 are length and span-count matched: token length within 3 tokens, value spans equal."""
    by = collections.defaultdict(dict)
    for r in records:
        if r["sub_block"] == "s5_argground" and r["pair_role"] in ("a", "b"):
            by[r["group_id"]][r["pair_role"]] = r
    bad = []
    for gid, d in by.items():
        if len(d) == 2:
            dl = abs(token_fn(d["a"]["rendered"]["text"]) - token_fn(d["b"]["rendered"]["text"]))
            ds = abs(d["a"]["user_spans"] - d["b"]["user_spans"])
            if dl > 6 or ds > 1:
                bad.append((gid, dl, ds))
    return gc.result("P-5d:pair_match", len(bad) <= 0.05 * max(1, len(by)), n_bad=len(bad), n_pairs=len(by), bad=bad[:5])


def p5e_s2_options(records, harness):
    rs = [r for r in records if r["sub_block"] == "s2_pick"]
    X = [" || ".join(o["text"] for o in r["options"]) for r in rs]
    y = [r["gold_letter"] for r in rs]
    grp = [r["group_id"] for r in rs]
    res = harness.kway(X, y, grp, 4)
    lo, hi = 0.28, 0.31
    return gc.result("P-5e", res.get("valid", True) and res["bacc"] <= lo and res["upper"] <= hi,
                     bacc=round(res["bacc"], 4), upper=round(res["upper"], 4), bars=[lo, hi])


def p6_value_spans(records, bar=0.05):
    cb = collections.Counter(r["user_spans"] for r in records if r["sub_block"] in CALL_SBS and r["call_bearing"])
    nc = collections.Counter(r["user_spans"] for r in records if r["sub_block"] in CALL_SBS and not r["call_bearing"])
    out = [gc.tv_gate("P-6:pooled", cb, nc, bar)]
    for sb in CALL_SBS:
        a = collections.Counter(r["user_spans"] for r in records if r["sub_block"] == sb and r["call_bearing"])
        b = collections.Counter(r["user_spans"] for r in records if r["sub_block"] == sb and not r["call_bearing"])
        if a and b:
            out.append(gc.tv_gate("P-6:%s" % sb, a, b, bar))
    return out


def p7_letters_positions(records):
    out = [gc.letter_share_gate("P-7:letters", [r for r in records if r["sub_block"] != "s5_argground"], 4, 0.02)]
    s5 = [r for r in records if r["sub_block"] == "s5_argground"]
    if s5:
        yes = sum(r["gold"] == "GROUNDED" for r in s5) / len(s5)
        out.append(gc.result("P-7:s5_yes_rate", 0.45 <= yes <= 0.55, yes=round(yes, 4)))
    s2 = [r for r in records if r["sub_block"] == "s2_pick"]
    probs = []
    byn = collections.defaultdict(list)
    for r in s2:
        byn[len(r["tools"])].append(r["lists"]["gold_pos"])
    for n, poss in byn.items():
        if n <= 8 and len(poss) >= 20:
            c = collections.Counter(poss)
            for i in range(n):
                if abs(c.get(i, 0) / len(poss) - 1.0 / n) > 0.05:
                    probs.append((n, i, round(c.get(i, 0) / len(poss), 3)))
    big = [(len(r["tools"]), r["lists"]["gold_pos"]) for r in s2 if len(r["tools"]) > 8]
    if len(big) >= 100:
        dec = collections.Counter(int(p * 10 / n) for n, p in big)
        for d in range(10):
            if abs(dec.get(d, 0) / len(big) - 0.10) > 0.03:
                probs.append(("decile", d, round(dec.get(d, 0) / len(big), 3)))
    out.append(gc.result("P-7:s2_gold_position", not probs, problems=probs[:8]))
    return out


def p8_reference_parity(records):
    rs = [r for r in records if r["flags"].get("ref_phrased")]
    if not rs:
        return gc.result("P-8", True, note="no reference-phrased rows")
    return gc.share_band("P-8", sum(r["gold"] == "CALL" for r in rs), len(rs), 0.45, 0.55)


def _target_info(r):
    """(target group, entity, verb, target param names) for a row, if it has a single target tool."""
    intent = r.get("intent", {})
    if r["sub_block"] in ("s1_need4", "s2_pick", "s3_limit", "s4_precond") and intent.get("target_group"):
        t = next((x for x in r["tools"] if x["group"] == intent["target_group"]), None)
        ent = intent.get("entity")
        verb = intent.get("verb") or (t["verb"] if t else None)
        pn = {p["name"] for p in t["params"]} if t else {a["param"] for a in intent.get("args", [])}
        return intent["target_group"], ent, verb, pn
    if r["sub_block"] == "s5_argground":
        t = next(x for x in r["tools"] if x["tid"] == "t0")
        return t["group"], t["entity"], t["verb"], {p["name"] for p in t["params"]}
    return None


def p9_distractors(records):
    out = []
    n = len(records)
    obs = collections.Counter(_nbin(len(r["tools"])) for r in records)
    probs = [(i, round(obs.get(i, 0) / n, 4), gen.FAMILY_NBIN_SHARES[i]) for i in range(5)
             if abs(obs.get(i, 0) / n - gen.FAMILY_NBIN_SHARES[i]) > 0.02]
    out.append(gc.result("P-9:nbin_shares", not probs, problems=probs, observed={i: round(obs.get(i, 0) / n, 4) for i in range(5)}))
    big = [r for r in records if len(r["tools"]) >= 4 and _target_info(r)]
    ns = sv = ov = 0
    for r in big:
        g_, ent, verb, pn = _target_info(r)
        others = [t for t in r["tools"] if t["group"] != g_]
        ns += any(t["entity"] == ent and t["verb"] != verb for t in others)
        sv += any(t["verb"] == verb and t["entity"] != ent for t in others)
        generic = {x for x in pn if not x.endswith("_id")}
        ov += any(generic & {p["name"] for p in t["params"]} for t in others)
    d = max(1, len(big))
    out.append(gc.result("P-9:hard_negatives", ns / d >= 0.40 and sv / d >= 0.20 and ov / d >= 0.15,
                         same_namespace=round(ns / d, 4), same_verb=round(sv / d, 4), param_overlap=round(ov / d, 4),
                         bars=[0.40, 0.20, 0.15], n=len(big)))
    return out


def p10_tokens(records, token_fn=util.approx_tokens):
    return gc.token_gate("P-10", records, token_fn)


def p11_wording(records, min_forms=50):
    return [gc.wording_gate("P-11:wording", records, min_forms=min_forms), gc.template_share_gate("P-11:template", records),
            gc.slot_survival_gate("P-11:slot_survival", records)]


def p12_pairs(records):
    return gc.pair_share_gate("P-12", records, 0.30, per_sub_block={"s1_need4": 0.50, "s3_limit": 0.80, "s4_precond": 0.60,
                                                                    "s5_argground": 0.70, "s6_parseq": 0.30, "s2_pick": 0.40})


def p13_names(records, allowlist):
    return gc.name_guard_gate("P-13", records, allowlist, "T54")


def p14_output_lint(records):
    return gc.lint_gate("P-14", records, render.lint_output, lambda r: r["parts"]["outputs"])


def p1_agreement(records, solver_b_fn):
    """Solver A vs B (B is a separate session's module): rows with A != B are dropped; > 1.0% = spec ambiguity."""
    return gc.agreement_gate("P-1", records, solver_b_fn, 0.01)


def solver_a_self_consistency(records):
    """Recompute gold from the structured record for every row (guards the export round trip)."""
    bad = [r["row_id"] for r in records if sa.gold_label(r) != r["gold"]]
    return gc.result("A-self", not bad, bad=bad[:10])


def run_all(records, harness=None, allowlist=None, solver_b_fn=None, token_fn=util.approx_tokens, min_forms=50):
    res = [p2_sizes_mix(records), p3_call_nocall(records), p4_limit_awareness(records), gc.pair_integrity(records)]
    res += p6_value_spans(records) + p7_letters_positions(records) + [p8_reference_parity(records)]
    res += p9_distractors(records) + [p10_tokens(records, token_fn)] + p11_wording(records, min_forms)
    res += [p12_pairs(records), p14_output_lint(records), solver_a_self_consistency(records), pair_match_s5(records)]
    if allowlist is not None:
        res.append(p13_names(records, allowlist))
    if harness is not None:
        res += p5a_request_only(records, harness) + p5b_toollist_card(records, harness) + p5c_structural(records, harness)
        res += [p5d_s5(records, harness), p5e_s2_options(records, harness)]
    if solver_b_fn is not None:
        res.append(p1_agreement(records, solver_b_fn))
    return res
