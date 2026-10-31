"""T55 PRE-FREEZE KILL gates (CPU, data only) per G0-lite 5.1 and the Opus rulings of 18 Oct (G2, G5, C3).
Orchestrator-run, not computed here: P-17 (200-row G13 pilot) and P-18 (collisions with the frozen evaluation set). POST-TRAINING lines (R-1..R-7)
are never kill rules and are not here. Probes call L-0's harness through tool_engine.gates_common."""
import collections
import itertools
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import gates_common as gc  # noqa: E402
from tool_engine import invariants, perturb, render, state, util  # noqa: E402
import t55_generator as gen  # noqa: E402
import t55_solver_a as sa  # noqa: E402

K_EFF = {"b1_classic": 5, "b4_blind_retry": 3, "b2_ambig_write": 5, "b3_implicit": 5, "b5_deny_escalate": 3,
         "b6_loop_poll": 4}


def kway_bars(k):
    return gc.kway_bars(k)


def expected_mix():
    return {sb: dict(m) for sb, m in gen.LABEL_MIX.items()}


def p2_sizes_mix(records):
    return gc.size_mix_gate("P-2", records, gen.SIZES, expected_mix())


def p3_perturbation_coverage(records):
    n = len(records)
    cells = collections.Counter(r["cell"] for r in records)
    probs = [(c, round(cells.get(c, 0) / n, 4)) for c in perturb.T55_CELLS if cells.get(c, 0) / n < 0.08]
    viol = [r for r in records if r["sub_block"] == "b3_implicit" and r["gold"] != "ACCEPT"]
    tcount = collections.Counter(r["b3"]["vtype"] for r in viol)
    tprobs = [(t, round(tcount.get(t, 0) / max(1, len(viol)), 4)) for t in perturb.TRAIN_TYPES
              if tcount.get(t, 0) / max(1, len(viol)) < 0.05]
    leaked = [t for t in tcount if t in perturb.HELDOUT_TYPES]
    return gc.result("P-3", not probs and not tprobs and not leaked, cells={c: round(cells.get(c, 0) / n, 4) for c in perturb.T55_CELLS},
                     cell_problems=probs, type_problems=tprobs, heldout_in_training=leaked, heldout=list(perturb.HELDOUT_TYPES))


# ---- P-4 / C3: exhaustive truth tables ---------------------------------------------------------------------
def p4_b2_truth_table(replay_fn=None):
    """Rule table vs five-option two-world simulation (and B's event-sourced replay when supplied) on EVERY cell of
    (I, kf, rp, committed, step)."""
    bad = []
    n = 0
    for I, kf, rp, c, st in itertools.product((False, True), (False, True), (False, True), (False, True), (1, 2)):
        n += 1
        a = sa.b2_rule(I, kf, rp, c, st)
        s = sa.b2_simulated(I, kf, rp, c, st)
        r = replay_fn(I, kf, rp, c, st) if replay_fn else a
        if not (a == s == r):
            bad.append((I, kf, rp, c, st, a, s, r))
    return gc.result("P-4:b2", not bad, cells=n, three_way=bool(replay_fn), mismatches=bad[:5])


def synth_b1(cls, a, cap, kind, eq, v, esc_q, esc_u):
    t0 = {"tid": "t0", "rw": "read" if kind == "read" else "write", "idempotent": kind in ("read", "idem"), "group": "g:x",
          "entity": "e", "verb": "v", "name": "v_e", "params": []}
    tools = [t0] + ([{"tid": "te", "rw": t0["rw"], "idempotent": t0["idempotent"], "group": "g:x", "entity": "e",
                      "verb": "w", "name": "w_e", "params": []}] if eq else [])
    args = [("idempotency_key", "k")] if kind == "key" else []
    return dict(error={"class": cls, "field": "f" if cls == "invalid_named_arg" else None}, attempt=a, R_cap=cap, tools=tools,
                call=dict(tool_tid="t0", args=args), user_values=[("f", "1")] if v else [],
                escalation={"quota_exhausted": esc_q, "unsupported_op": esc_u})


def b1_rule_table(cls, a, cap, kind, eq, v, esc_q, esc_u):
    """The G0-lite 3.2 B1 table written as a flat decision list (independent of the record-based evaluator)."""
    safe = kind in ("read", "idem", "key")
    if cls in ("transient_unavailable", "rate_limited"):
        if a < cap and safe:
            return "RETRY"
        if a >= cap:
            return "SWITCH_TOOL" if eq else "ASK"
        return None                                                    # B2 territory
    if cls == "invalid_named_arg":
        return "FIX_ARGS" if v else "ASK"
    if cls == "invalid_unnamed":
        return "SWITCH_TOOL" if eq else "ASK"
    if cls == "auth_denied":
        return "ASK"
    if cls == "unsupported_op":
        return "SWITCH_TOOL" if eq else ("STOP" if esc_u == "STOP" else "ASK")
    if cls == "quota_exhausted":
        return "SWITCH_TOOL" if eq else esc_q
    if cls == "irrecoverable":
        return "STOP"
    raise ValueError(cls)


def p4_b1_truth_table(evaluator=None):
    evaluator = evaluator or sa.b1_label
    bad, n, skipped = [], 0, 0
    for cls in perturb.ERROR_CLASSES:
        for a, cap, kind, eq, v, eq_q, eq_u in itertools.product((1, 2, 3, 4), (2, 3), ("read", "idem", "key", "plain"),
                                                                 (False, True), (False, True), ("ASK", "STOP"), ("ASK", "STOP")):
            want = b1_rule_table(cls, a, cap, kind, eq, v, eq_q, eq_u)
            rec = synth_b1(cls, a, cap, kind, eq, v, eq_q, eq_u)
            if want is None:
                skipped += 1
                try:
                    evaluator(rec)
                    bad.append(("expected OutOfBlock", cls, a, cap, kind))
                except sa.OutOfBlock:
                    pass
                continue
            n += 1
            got = evaluator(rec)
            if got != want:
                bad.append((cls, a, cap, kind, eq, v, eq_q, eq_u, want, got))
    return gc.result("P-4:b1", not bad, cells=n, out_of_block=skipped, mismatches=bad[:5])


def b3_rule_table(violation, cause_arg, rw, a, eq):
    if not violation:
        return "ACCEPT"
    if cause_arg:
        return "FIX_ARGS"
    if rw == "write":
        return "ASK"
    if a == 1:
        return "RETRY"
    return "SWITCH_TOOL" if eq else "ASK"


def p4_b3_truth_table(evaluator=None):
    """Every violation type x cause x tool kind x attempt x equivalent-listed, against the C1 decision order."""
    bad, n = [], 0
    rng = util.rng_for("t55-tt")
    for vt in perturb.VIOLATION_TYPES:
        for cause in ("data", "arg"):
            if cause == "arg" and vt not in invariants.ARG_CAPABLE:
                continue
            for violating in (True, False):
                base = invariants.make_base(vt, rng, "kol", "qty", cause)
                result, ctx = invariants.materialise(base, violating)
                for rw, a, eq in itertools.product(("read", "write"), (1, 2, 3), (False, True)):
                    t0 = {"tid": "t0", "rw": rw, "idempotent": rw == "read", "group": "g:x", "entity": "e", "verb": "v", "params": []}
                    tools = [t0] + ([{"tid": "te", "rw": rw, "idempotent": rw == "read", "group": "g:x", "entity": "e",
                                      "verb": "w", "params": []}] if eq else [])
                    rec = dict(result=result, ctx=ctx, attempt=a, tools=tools, call=dict(tool_tid="t0", args=[]))
                    cause_arg = violating and invariants.cause(vt, result, ctx) == "arg"
                    want = b3_rule_table(violating, cause_arg, rw, a, eq)
                    got = (evaluator or sa.b3_label)(rec)
                    n += 1
                    if got != want:
                        bad.append((vt, cause, violating, rw, a, eq, want, got))
    return gc.result("P-4:b3", not bad, cells=n, mismatches=bad[:5])


def b5_rule_table(n_c, n_t, n_w, kc, kt, kw, window, alt, hard):
    if n_c >= kc or (kt is not None and n_t >= kt) or (window and n_w >= kw):
        return "ESCALATE"
    if hard:
        return "STOP"
    return "CONTINUE_ALT" if alt else "ESCALATE"


def p4_b5_truth_table(evaluator=None):
    bad, n = [], 0
    for kc, kt, window, alt, hard in itertools.product((2, 3, 4), (None, 10, 20), (False, True), (False, True), (False, True)):
        kw = 10 if window else None
        for n_c in (0, kc - 1, kc, kc + 1):
            for n_t in (0, 9, 10, 19, 20, 25):
                for n_w in ((0, 9, 10, 11) if window else (None,)):
                    rec = dict(denials=dict(n_c=n_c, n_t=n_t, n_w=n_w, alt_exists=alt, goal_blocked_hard=hard),
                               card_b5=dict(K_c=kc, K_t=kt, K_w=kw, W=50 if window else None, window=window))
                    want = b5_rule_table(n_c, n_t, n_w, kc, kt, kw, window, alt, hard)
                    got = (evaluator or sa.b5_label)(rec)
                    n += 1
                    if got != want:
                        bad.append((kc, kt, window, alt, hard, n_c, n_t, n_w, want, got))
    return gc.result("P-4:b5", not bad, cells=n, mismatches=bad[:5])


def b6_rule_table(adv, calls_used, p_cap, lim, alt, non_waitable):
    changed = bool(adv) and adv[-1]
    stale = 0
    for x in reversed(adv):
        if x:
            break
        stale += 1
    if changed:
        return "KEEP_POLLING" if calls_used < p_cap else "ESCALATE"
    if stale < lim:
        return "KEEP_POLLING"
    if alt:
        return "BREAK_LOOP_ALT"
    return "STOP" if non_waitable else "ESCALATE"


def p4_b6_truth_table(evaluator=None):
    """Every advance pattern of up to 5 steps x budget position x loop limit x alt x non-waitable. Observations are built
    from progress only so the evaluator's predicate is exercised end to end."""
    bad, n = [], 0
    for steps in (2, 3, 4, 5):
        for adv in itertools.product((False, True), repeat=steps):
            prog = [10]
            for x in adv:
                prog.append(prog[-1] + (5 if x else 0))
            obs = [{"progress": v} for v in prog]
            for cu, pc, lim, alt, nw in itertools.product((3, 8, 12), (8, 12), (3, 4), (False, True), (False, True)):
                rec = dict(poll=dict(obs=obs, calls_used=cu, alt_exists=alt), card_b6=dict(P_cap=pc, L=lim, transitions=[],
                                                                                             non_waitable=nw))
                want = b6_rule_table(list(adv), cu, pc, lim, alt, nw)
                got = (evaluator or sa.b6_label)(rec)
                n += 1
                if got != want:
                    bad.append((adv, cu, pc, lim, alt, nw, want, got))
    return gc.result("P-4:b6", not bad, cells=n, mismatches=bad[:5])


def p4_all(evaluators=None):
    ev = evaluators or {}
    return [p4_b2_truth_table(ev.get("b2_replay")), p4_b1_truth_table(ev.get("b1")), p4_b3_truth_table(ev.get("b3")),
            p4_b5_truth_table(ev.get("b5")), p4_b6_truth_table(ev.get("b6"))]


# ---- probes -----------------------------------------------------------------------------------------------
def structural_features(r, token_fn=util.approx_tokens):
    return {"tokens": token_fn(r["rendered"]["text"]), "user_turns": r["parts"]["conversation"].count("User:"),
            "n_tools": len(r["tools"]), "gold_letter": r["gold_letter"], "wording_id": r["wording"]["idx"],
            "template_id": r["template_id"], "view": r["view"]}


def p5_structure(records, harness):
    out = []
    for sb, k in K_EFF.items():
        rs = [r for r in records if r["sub_block"] == sb]
        if len(rs) < 40:
            continue
        X = [structural_features(r) for r in rs]
        y = [r["gold"] for r in rs]
        grp = [r["group_id"] for r in rs]
        res = harness.kway(X, y, grp, k)
        lo, hi = kway_bars(k)
        out.append(gc.result("P-5:%s" % sb, res.get("valid", True) and res["bacc"] <= lo and res["upper"] <= hi,
                             bacc=round(res["bacc"], 4), upper=round(res["upper"], 4), bars=[round(lo, 4), round(hi, 4)], k_eff=k))
    return out


def shape_text(r):
    """B3 shape-only text: field names and value SHAPES (digits and words masked), no values."""
    import re
    lines = []
    for o in r["parts"]["outputs"]:
        for ln in o.splitlines():
            k, _, v = ln.partition(":")
            lines.append(k.strip() + ":" + re.sub(r"[A-Za-z]+", "W", re.sub(r"\d+", "N", v)))
    return " ".join(lines)


def p6_b3_shape(records, harness):
    rs = [r for r in records if r["sub_block"] == "b3_implicit"]
    X = [shape_text(r) for r in rs]
    y = [int(r["gold"] != "ACCEPT") for r in rs]
    return gc.probe_binary_gate("P-6", harness, X, y, [r["group_id"] for r in rs])


def p7_b6_identical_fraction(records, harness):
    rs = [r for r in records if r["sub_block"] == "b6_loop_poll"]
    X = [{"identical_fraction": _identical_fraction(r)} for r in rs]
    y = [int(r["gold"] == "KEEP_POLLING") for r in rs]
    return gc.probe_binary_gate("P-7", harness, X, y, [r["group_id"] for r in rs])


def _identical_fraction(r):
    calls = [tuple(c) for c in r["poll"]["calls"]]
    return sum(1 for a, b in zip(calls, calls[1:]) if a == b) / max(1, len(calls) - 1)


# ---- non-probe gates ----------------------------------------------------------------------------------------
def p8_b4_pairs(records):
    by = collections.defaultdict(dict)
    for r in records:
        if r["sub_block"] == "b4_blind_retry":
            by[r["group_id"]][r["pair_role"]] = r
    bad = []
    for gid, d in by.items():
        if set(d) != {"a", "b"}:
            bad.append((gid, "incomplete"))
            continue
        ea, eb = d["a"]["error"], d["b"]["error"]
        same = all(ea[k] == eb[k] for k in ("group", "code", "phrase_idx", "channels")) and ea["class"] == "invalid_named_arg" \
            and eb["class"] == "invalid_unnamed" and eb.get("field") is None and ea.get("field")
        # only the detail (field) line may differ in the rendered output blocks
        oa, ob = d["a"]["parts"]["outputs"], d["b"]["parts"]["outputs"]
        diff = [(x, y) for x, y in zip(oa, ob) if x != y]
        only_field = all([ln for ln in x.splitlines() if ln not in y.splitlines()] and
                         all(ln.startswith("field:") for ln in x.splitlines() if ln not in y.splitlines()) and
                         not [ln for ln in y.splitlines() if ln not in x.splitlines()] for x, y in diff)
        if not (same and only_field):
            bad.append(gid)
    return gc.result("P-8", not bad, n_pairs=len(by), bad=bad[:5])


def p9_channels(records):
    rs = [r for r in records if r["sub_block"] in ("b1_classic", "b4_blind_retry")]
    n = len(rs)
    single = sum(1 for r in rs if len(r["error"]["channels"]) == 1)
    combos = collections.Counter(tuple(r["error"]["channels"]) for r in rs)
    ok = 0.28 <= single / n <= 0.32 and max(combos.values()) / n <= 0.40
    return gc.result("P-9", ok, single_share=round(single / n, 4), top_combo=round(max(combos.values()) / n, 4))


def p10_observability(records):
    """Every label's required facts are visible in the rendered row. Generator-side form (solver B's parser does the
    parse-based version): the facts that the rule reads must be present in the rendered text."""
    bad = []
    for r in records:
        t = r["rendered"]["text"]
        sb = r["sub_block"]
        if sb in ("b1_classic", "b4_blind_retry"):
            e = r["error"]
            ok = ("[read]" in t or "idempotent]" in t or "[write]" in t)
            ok = ok and (e["class"] != "invalid_named_arg" or ("field: %s" % e["field"]) in t)
            ok = ok and (("idempotency_key=" in t) == sa.key_offered(r)) and ("so far (including this one): %d." % r["attempt"]) in t
            ok = ok and ("quota" in r["slots"] and "unsupp" in r["slots"])        # the table's two values were slot-filled (and survive in the text: slot_survival gate); the card's wording varies by pool
            if e["class"] == "invalid_named_arg":
                f = e["field"]
                ok = ok and (any(("with %s " % f.replace("_", " ")) in t for _ in (0,)) == (f in {k for k, _v in r["user_values"]}))
        elif sb == "b2_ambig_write":
            ok = "status: timeout" in t and (r["step"] == 1 or ("committed: %s" % ("yes" if r["readback"]["committed"] else "no")) in t)
        elif sb == "b3_implicit":
            ok = "status: ok" in t
        elif sb == "b5_deny_escalate":
            d = r["denials"]
            ok = ("%d consecutive" % d["n_c"]) in t and ("%d in total" % d["n_t"]) in t and ("exists: %s" % ("yes" if d["alt_exists"] else "no")) in t
        else:
            ok = ("Calls used on this poll: %d" % r["poll"]["calls_used"]) in t and all(
                ("progress: %s" % o["progress"]) in t for o in r["poll"]["obs"] if "progress" in o)
        if not ok:
            bad.append(r["row_id"])
    return gc.result("P-10", not bad, n_bad=len(bad), bad=bad[:5], note="generator-side check; solver B's parser gives the parse-based version")


def p11_letters(records):
    return gc.letter_share_gate("P-11", records, 5, 0.02)


def p11_letters_by_k(records):
    out = []
    for k in (5, 4):
        rs = [r for r in records if len(r["options"]) == k]
        if rs:
            out.append(gc.letter_share_gate("P-11:k%d" % k, rs, k, 0.02))
    return out


def p19_b5_thresholds(records):
    rs = [r for r in records if r["sub_block"] == "b5_deny_escalate"]
    n = len(rs)
    cfg = collections.Counter((r["card_b5"]["K_c"], r["card_b5"]["K_t"], r["card_b5"]["window"]) for r in rs)
    top = max(cfg.values()) / n if n else 0
    pub1 = any(r["card_b5"]["K_c"] == 3 and r["card_b5"]["K_t"] == 20 and not r["card_b5"]["window"] for r in rs)
    pub2 = any(r["card_b5"]["K_c"] == 3 and r["card_b5"]["window"] and r["card_b5"]["K_w"] == 10 and r["card_b5"]["W"] == 50 for r in rs)
    return gc.result("P-19", top <= 0.25 and pub1 and pub2, top_config_share=round(top, 4), published_present=[pub1, pub2])


def p14_output_lint(records):
    """No imperative or second-person clause, and every line is a key: value data line. Keys are the closed output keys
    plus the row's own field nouns / argument names, so the key list itself is checked per row."""
    bad = []
    for r in records:
        extra = set()
        if r["sub_block"] == "b3_implicit":
            extra.add(r["b3"]["field"])
            extra.update(k for k, _v in r["call"]["args"])
        for t in r["parts"]["outputs"]:
            v = render.lint_output(t, render.OUTPUT_KEYS_T55 | extra | {"detail"})
            if v:
                bad.append((r["row_id"], v[0]))
    return gc.result("P-14", not bad, violations=bad[:10], n=len(bad))


def run_all(records, harness=None, allowlist=None, solver_b_fn=None, token_fn=util.approx_tokens, min_forms=50):
    res = [p2_sizes_mix(records), p3_perturbation_coverage(records), gc.pair_integrity(records)] + p4_all()
    res += [p8_b4_pairs(records), p9_channels(records), p10_observability(records), gc.token_gate("P-12", records, token_fn)]
    res += p11_letters_by_k(records)
    res += [gc.wording_gate("P-13:wording", records, min_forms=min_forms), gc.template_share_gate("P-13:template", records),
            gc.slot_survival_gate("P-13:slot_survival", records), p14_output_lint(records),
            gc.pair_share_gate("P-16", records, 0.30), p19_b5_thresholds(records)]
    if allowlist is not None:
        res.append(gc.name_guard_gate("P-15", records, allowlist, "T55"))
    if harness is not None:
        res += p5_structure(records, harness) + [p6_b3_shape(records, harness), p7_b6_identical_fraction(records, harness)]
    if solver_b_fn is not None:
        res.append(gc.agreement_gate("P-1", records, solver_b_fn, 0.01))
    return res
