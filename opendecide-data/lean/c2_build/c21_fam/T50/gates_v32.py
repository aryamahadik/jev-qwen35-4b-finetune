"""Gates ADDED OR CHANGED by addendum v3.2 section 12 (K14s, K23-K33) plus the K6-within-carrier run (K10 NOTE, O-A1). Coded as written:
every bar is the addendum's. Each function takes the in-memory specs of a family build (family.Family.specs) and returns a dict like
T50/gates._res. Nothing here reads a file of rows or calls a model. The G13 stamp (K14s) and the model-based L4 read (K31) are not CPU
gates and are reported as `not run`.
"""
import dataclasses
from collections import Counter, defaultdict

from LA_COMMON import perturb, probe
from LA_COMMON.edits import EditAction, apply_parsed, parse_edit
from LA_COMMON.shellmodel import Script
from LA_COMMON.state import Consumer, NONSTATE_CLASSES, PATH_CLASSES, STATE_CLASSES

from . import dialects, edit_model as em
from .gates import _res, fmt_features, iter_rows, est_tokens
from .solver_a import label_spec

CLASS_STATE_Q = (0.05, 0.08)            # each state class 5-8% of block G
CLASS_NONSTATE_Q = (0.14, 0.19)         # each non-state class 14-19%
CLASS_ALLOW_BAND = (0.50, 0.72)
PARITY_TOL = 0.05


def _bin_probe(rows, feat, y_fn, group_fn=None):
    if len(rows) < 40:
        return {"pass": False, "why": "too few rows", "n": len(rows)}
    X = [feat(s, r) for s, r in rows]
    y = [y_fn(s) for s, r in rows]
    if len(set(y)) < 2:
        return {"pass": False, "why": "single class", "n": len(rows)}
    return probe.run_valid(probe.binary_probe, X, y, [(group_fn or (lambda s: s.group))(s) for s, r in rows])


# ================================================================================================ K23
def _canon_effects(effs):
    out = []
    for e in effs:
        k = e["kind"]
        if k == "script":
            out.append(("script", tuple(repr(s.canon()) for s in e["scripts"])))
        elif k == "pkg":
            out.append(("pkg", e["name"], e["ver"], e["host"]))
        elif k == "sql":
            out.append(("sql", tuple((x.kind, x.table, x.has_predicate) for x in e["stmts"]), e["db"]))
        elif k == "iac":
            out.append(("iac", e["op"], e["ctx"]))
        elif k == "check_disable":
            out.append(("dis", e["check"], e["how"]))
    return sorted(out, key=repr)


def rendered_effects(spec):
    """Induced effects recomputed from the RENDERED edit (parse of the call text + the recorded old content + the consumer record)."""
    parsed = parse_edit(spec.renderings[0]["text"])
    if parsed is None:
        return None
    new = apply_parsed(spec.action.old_lines, parsed)
    if new is None:
        return None
    cons = Consumer(**spec.consumer)
    return em.induced_effects(cons.kind, spec.action.path, list(spec.action.old_lines), new, cons)


def spec_effects(spec):
    cons = Consumer(**spec.consumer)
    return em.induced_effects(cons.kind, spec.action.path, list(spec.action.old_lines), list(spec.action.new_lines), cons)


def shell_equiv_result(spec):
    eq = spec.meta.get("shell_equiv")
    if eq is None:
        return None
    st = spec.state.clone()
    patch = spec.meta.get("shell_equiv_patch") or {}
    if "git_last_hook" in patch:
        st.git.last_hook_result = patch["git_last_hook"]
    sp = dataclasses.replace(spec, action=Script.from_dict(eq), state=st)
    return label_spec(sp)


def k23_equivalent(specs):
    """100% of block-G state-bearing rows: edit label (induced part) = shell-equivalent label (or ASK by R19); the induced effects
    recomputed from the RENDERED edit equal those of the spec."""
    n = bad_label = bad_eff = 0
    ex = []
    for s in specs:
        if s.block != "G" or not s.meta.get("state_bearing") or s.naming.get("ops"):
            continue
        n += 1
        res = label_spec(s)
        ind = res.induced
        eq = shell_equiv_result(s)
        if eq is not None:
            got = (ind.label, ind.reason, ind.tier) if ind is not None else ("ALLOW", "none", "na")
            want = (eq.label, eq.reason, eq.tier)
            r19 = ind is not None and any(m.rule == "R19" for m in res.members)
            if got != want and not (r19 and got[0] == "ASK"):
                bad_label += 1
                if len(ex) < 8:
                    ex.append((s.spec_id, got, want))
        elif ind is not None and ind.label != "ALLOW":
            bad_label += 1
            ex.append((s.spec_id, (ind.label,), "no shell equivalent"))
        re_ = rendered_effects(s)
        if re_ is None or _canon_effects(re_) != _canon_effects(spec_effects(s)):
            bad_eff += 1
            if len(ex) < 8:
                ex.append((s.spec_id, "rendered effects differ"))
    return _res("K23", "equivalent-effect check", "100% of block-G state-bearing rows: edit label = shell-equivalent label (or ASK by R19)",
                n > 0 and bad_label == 0 and bad_eff == 0, checked=n, label_mismatch=bad_label, effect_mismatch=bad_eff, examples=ex)


# ================================================================================================ K24
def k24_pathclass(specs):
    rows = [(s, r) for s, r in iter_rows(specs) if s.block == "G"]
    nG = len(rows)
    if not nG:
        return _res("K24", "path-class probe", "AUC <= 0.55", False, why="no block-G rows")
    st = [(s, r) for s, r in rows if s.meta.get("state_bearing")]
    ns = [(s, r) for s, r in rows if not s.meta.get("state_bearing")]
    a_st = sum(1 for s, r in st if s.gold.label == "ALLOW") / max(1, len(st))
    a_ns = sum(1 for s, r in ns if s.gold.label == "ALLOW") / max(1, len(ns))
    cls_rows = Counter(s.path_class for s, r in rows)
    cls_allow = Counter(s.path_class for s, r in rows if s.gold.label == "ALLOW")
    quota_ok = True
    quota = {}
    for c in PATH_CLASSES:
        sh = cls_rows[c] / nG
        lo, hi = CLASS_STATE_Q if c in STATE_CLASSES else CLASS_NONSTATE_Q
        al = cls_allow[c] / max(1, cls_rows[c])
        okc = lo <= sh <= hi and CLASS_ALLOW_BAND[0] <= al <= CLASS_ALLOW_BAND[1]
        quota[c] = {"share": round(sh, 4), "allow": round(al, 4), "ok": okc}
        quota_ok &= okc
    p_path = _bin_probe(rows, lambda s, r: {"pc_" + s.path_class: 1.0}, lambda s: int(s.gold.label == "ALLOW"))
    p_state = _bin_probe(rows, lambda s, r: {"state": float(bool(s.meta.get("state_bearing")))}, lambda s: int(s.gold.label == "ALLOW"))
    p_zone = _bin_probe(rows, lambda s, r: {"zone_" + s.zone: 1.0}, lambda s: int(s.gold.label == "ALLOW"))    # report line (risk 3)
    # pair integrity: members identical in diff bytes, different only in path, consumer record and zone
    by_g = defaultdict(list)
    for s, r in rows:
        by_g[s.group].append(s)
    bad_pairs = 0
    n_pairs = 0
    for gid, ss in by_g.items():
        n_pairs += 1
        h = {tuple(map(tuple, s.action.hunk())) for s in ss}
        if len(h) != 1:
            bad_pairs += 1
            continue
        if ss[0].meta.get("tag") != "g3q" and len({bool(s.consumer) for s in ss}) != 2:
            bad_pairs += 1
    ok = (p_path.get("pass") and p_state.get("pass") and abs(a_st - a_ns) <= PARITY_TOL and quota_ok and bad_pairs == 0)
    return _res("K24", "path-class-only probe on block G + parity quota", "both AUC <= 0.55 ub <= 0.60; ALLOW share state vs non-state within +-5 pp; "
                "class quotas; pair integrity 100%", bool(ok), rows=nG, allow_state=a_st, allow_nonstate=a_ns, quotas=quota,
                probe_path_class=p_path, probe_state_flag=p_state, zone_only_report=p_zone, pairs=n_pairs, bad_pairs=bad_pairs)


# ================================================================================================ K33 / K6 within carriers
def k33_carrier(specs):
    rows = list(iter_rows(specs))
    p = _bin_probe(rows, lambda s, r: {"carrier_" + (s.carrier or "shell_exec"): 1.0}, lambda s: int(s.gold.label == "ALLOW"))
    sh = [r for s, r in rows if not s.carrier]
    ed = [r for s, r in rows if s.carrier]
    a_sh = sum(1 for s, r in rows if not s.carrier and s.gold.label == "ALLOW") / max(1, len(sh))
    a_ed = sum(1 for s, r in rows if s.carrier and s.gold.label == "ALLOW") / max(1, len(ed))
    out = _res("K33", "carrier-only probe", "REPORT line, advisory (O-A1 / T50-B1): number published, never a kill", True,
               report_only=True, auc=p.get("auc"), ub=p.get("ub"), allow_shell=a_sh, allow_edit=a_ed, probe=p)
    return out


def k6_within_carrier(specs):
    """K6 (format-only probe) run WITHIN each carrier: shell_exec rows alone, edit rows alone. Bars unchanged."""
    out = {}
    for name, pred in (("shell_exec", lambda s: not s.carrier), ("edit_carriers", lambda s: bool(s.carrier))):
        rows = [(s, r) for s, r in iter_rows(specs) if pred(s) and not (hasattr(s.action, "opaque_kind"))]
        out[name] = _bin_probe(rows, fmt_features, lambda s: int(s.gold.label == "ALLOW"))
    return _res("K6c", "format-only probe within each carrier", "AUC <= 0.55 ub <= 0.60 inside shell_exec and inside the edit carriers",
                all(v.get("pass") for v in out.values()), **{k: {kk: vv for kk, vv in v.items() if kk in ("auc", "ub", "pass", "n", "valid", "why")}
                                                            for k, v in out.items()})


# ================================================================================================ K27
def _a6_rows(specs):
    return [(s, r) for s, r in iter_rows(specs) if s.cue]


def _strip_label_same(spec):
    """Solver A label with the free text removed equals the label with it (solver B is checked by its own agent)."""
    if not spec.cue:
        return True
    if isinstance(spec.action, EditAction):
        txt = spec.cue["text"]
        keep = [l for l in spec.action.new_lines if txt not in l]
        sp = dataclasses.replace(spec, action=EditAction(spec.action.carrier, spec.action.path, list(spec.action.old_lines), keep))
        a, b = label_spec(spec), label_spec(sp)
        return (a.label, a.reason, a.tier) == (b.label, b.reason, b.tier)
    return True


def _free_text_feats(s, r):
    c = s.cue
    t = r["text"]
    return {"has_free_text": float(bool(c)), "len_b": float(min(len(c["text"]) // 12, 8)) if c else 0.0,
            "pos_inline": float(bool(c) and c["position"] == "trailing_comment"), "pos_diff": float(bool(c) and c["position"] == "diff_comment"),
            "count": float(c["count"]) if c else 0.0}


def k27_injection(specs):
    rows = list(iter_rows(specs))
    a6 = _a6_rows(specs)
    n_a6 = len(a6)
    p_all = _bin_probe(rows, _free_text_feats, lambda s: int(s.gold.label == "ALLOW"))
    p_in = _bin_probe(a6, _free_text_feats, lambda s: int(s.gold.label == "ALLOW"))
    honest = sum(1 for s, r in a6 if s.cue["kind"] == "honest")
    types = defaultdict(lambda: [0, 0])
    for s, r in a6:
        if s.cue["kind"] == "cue":
            types[s.cue["type"]][0] += 1
            types[s.cue["type"]][1] += s.gold.label == "ALLOW"
    bal = {t: (a / n if n else None) for t, (n, a) in types.items()}
    bal_ok = bool(bal) and all(v is not None and abs(v - 0.5) <= PARITY_TOL for v in bal.values())
    same = sum(1 for s, r in a6 if _strip_label_same(s))
    ok = (p_all.get("pass") and p_in.get("pass") and n_a6 > 0 and honest / n_a6 >= 0.45 and bal_ok and same == n_a6)
    return _res("K27", "gate-directed injection", "comment-presence probe whole family and inside A6: AUC <= 0.55 ub <= 0.60; benign explanatory >= 45%; "
                "cue type x label within +-5 pp of 50%; label unchanged without the free text: 100%", bool(ok), a6_rows=n_a6, honest_share=honest / max(1, n_a6),
                cue_type_allow_share=bal, label_unchanged_without_text=same, probe_whole=p_all, probe_inside=p_in,
                by_block=dict(Counter(s.block for s, r in a6)))


# ================================================================================================ K28
def k28_perturbation(specs):
    pert = [s for s in specs if s.perturbation]
    by_g = defaultdict(list)
    for s in specs:
        by_g[s.group].append(s)
    no_twin = [s.spec_id for s in pert if all(m.perturbation for m in by_g[s.group])]
    held_in_train = [s.spec_id for s in pert if s.perturbation["transform"] in perturb.HELDOUT_TRANSFORMS and s.split != "dev"]
    rows = [(s, r) for s, r in iter_rows(specs)]
    p = _bin_probe(rows, lambda s, r: {"perturbed": float(bool(s.perturbation))}, lambda s: int(s.gold.label == "ALLOW"))
    n_rows_p = sum(len(s.renderings) for s in pert)
    fam_allow = sum(1 for s, r in rows if s.gold.label == "ALLOW") / max(1, len(rows))
    p_allow = sum(len(s.renderings) for s in pert if s.gold.label == "ALLOW") / max(1, n_rows_p)
    surv_bad = 0
    for s in pert:
        for i, (otext, ospans) in enumerate(s.meta.get("pert_orig", [])):
            nsp = [sp for sp in s.decision_spans if sp["turn"] == i]
            ok_, _ = perturb.spans_survive(otext, ospans, s.user_turns[i].text, nsp)
            surv_bad += (not ok_)
    ok = (not no_twin and not held_in_train and surv_bad == 0 and p.get("pass") and abs(p_allow - fam_allow) <= PARITY_TOL and n_rows_p > 0)
    return _res("K28", "character perturbation", "spans survive + clean twin 100%; 0 held-out transform rows in train; perturbation-presence probe AUC <= 0.55 ub <= 0.60; "
                "ALLOW share within +-5 pp", bool(ok), perturbed_rows=n_rows_p, by_transform=dict(Counter(s.perturbation["transform"] for s in pert)),
                missing_clean_twin=no_twin[:10], heldout_in_train=held_in_train[:10], span_survival_failures=surv_bad, allow_share_perturbed=p_allow, allow_share_family=fam_allow, probe=p)


# ================================================================================================ K29
def k29_dialects(specs):
    rows = list(iter_rows(specs))
    n = len(rows)
    sc_ok = 0
    for s, r in rows:
        body = dialects.render_card_body(s.dialect, s.card) if s.dialect else ""
        sc_ok += bool(s.dialect) and dialects.scaffold_sha_ok(dialects.wrap_in_scaffold(body))
    held_in_train = sum(1 for s, r in rows if s.dialect in dialects.HELDOUT_DIALECTS and s.split != "dev")
    share = Counter(s.dialect for s, r in rows if s.dialect in dialects.TRAINED_DIALECTS and s.split == "train")
    tot_train = sum(share.values()) or 1
    shares = {d: share[d] / tot_train for d in dialects.TRAINED_DIALECTS}
    share_ok = all(0.12 <= v <= 0.25 for v in shares.values())
    within = {}
    for d in dialects.TRAINED_DIALECTS:
        rr = [(s, r) for s, r in rows if s.dialect == d and not hasattr(s.action, "opaque_kind")]
        within[d] = _bin_probe(rr, fmt_features, lambda s: int(s.gold.label == "ALLOW"))
    p_id = _bin_probe(rows, lambda s, r: {"dialect_" + s.dialect: 1.0}, lambda s: int(s.gold.label == "ALLOW"))
    ok = (sc_ok == n and held_in_train == 0 and share_ok and all(v.get("pass") for v in within.values()) and p_id.get("pass"))
    cost = {}
    for d in dialects.ALL_DIALECTS:
        toks = [est_tokens(dialects.render_card_body(d, s.card)) for s, r in rows[:200]]
        cost[d] = sum(toks) / max(1, len(toks))
    return _res("K29", "dialects", "scaffold-sha assert 100%; 0 held-out dialect rows in train; each trained dialect 12-25%; K6 within each dialect and dialect-id-only "
                "AUC <= 0.55 ub <= 0.60", bool(ok), rows=n, scaffold_ok=sc_ok, heldout_in_train=held_in_train, trained_shares=shares,
                k6_within={d: {k: v.get(k) for k in ("auc", "ub", "pass", "valid")} for d, v in within.items()},
                dialect_id_probe={k: p_id.get(k) for k in ("auc", "ub", "pass", "valid")}, card_body_tokens_by_dialect=cost,
                scaffold="STUB (the real scaffold is L-0's; scaffold_sha_ok must be called with it)")


# ================================================================================================ K30 / K31 / K32
def row_levels(specs):
    out = []
    for s, r in iter_rows(specs):
        lad = r.get("ladder") or s.ladder
        if lad:
            out.append((lad["mechanism"], lad["level"], s.gold.label, s))
    return out


def k30_ladder(specs, n_quads=120, quad_cells=4):
    rl = row_levels(specs)
    total = len(list(iter_rows(specs)))
    l34 = sum(1 for m, l, lab, s in rl if l >= 3)
    mech = defaultdict(Counter)
    for m, l, lab, s in rl:
        mech[m][l] += 1
    mech_ok = {}
    for m, c in mech.items():
        tot = sum(c.values())
        mech_ok[m] = all(c[l] / tot >= 0.10 for l in (1, 2, 3, 4))
    l4 = Counter(lab for m, l, lab, s in rl if l == 4)
    l4_share = max(l4.values()) / sum(l4.values()) if l4 else 1.0
    quads = defaultdict(dict)
    for s, r in iter_rows(specs):
        if s.quad_id:
            quads[s.quad_id][(s.quad_axes["surface"], s.quad_axes["risk"])] = s.gold.label
    quad_ok = len(quads) == n_quads and all(len(q) == quad_cells for q in quads.values())
    twin_ok = all((q[("alarming", "present")] != "ALLOW" and q[("calm", "present")] != "ALLOW" and q[("alarming", "resolved")] == "ALLOW"
                   and q[("calm", "resolved")] == "ALLOW") for q in quads.values() if len(q) == quad_cells)
    ok = (l34 / max(1, total) >= 0.25 and bool(mech_ok) and all(mech_ok.values()) and len(mech) == 5 and l4_share <= 0.55 and quad_ok and twin_ok)
    return _res("K30", "ladder structure", ">= 25% of rows L3-L4; every mechanism has all four levels (each >= 10%); 120 quad specs x 4 cells; every hard cell has "
                "its opposite-label twin; <= 55% of L4 rows share one label", bool(ok), share_l34=l34 / max(1, total), mechanisms={m: dict(c) for m, c in mech.items()},
                mechanism_levels_ok=mech_ok, l4_max_label_share=l4_share, quads=len(quads), quad_cells_ok=quad_ok, twin_ok=twin_ok)


def k31_note():
    return _res("K31", "C2 (or C1) <= 70% on L4 rows", "PRE-FREEZE FIX-TRIGGER, NOT A KILL", True, not_run=True,
                why="needs the od-l4b read of our own model on the 1,000-row pilot (not a CPU gate)")


def k32_wrappers(specs, built=False):
    if not built:
        return _res("K32", "cue wrappers", "only if A10 is built", True, built=False, why="GV1: no Fri 23 probe result; A10 is not built, its quotas revert to plain rows")
    raise NotImplementedError("A10 not built")


# ================================================================================================ K14s (CPU part)
def k14s_report(family):
    gen = family.report.get("generated_rows") or 1
    by = Counter(w.split(":")[0] for _, w in family.ledger.drops)
    return _res("K14s", "stamp on ALL rows", "<= 1% non-exempt drops (G13 stamp); OHS-5 collisions <= 5%", True, g13_stamp_run=False,
                answer_check_drops=dict(by), generated_rows=gen, answer_check_drop_rate=family.ledger.count() / gen,
                why="the G13 stamp and the manifest stamp are the L-0b wrapper's; only the CPU answer-check drops are counted here")


def run_set_level(family, fast=False):
    """All v3.2 set-level gates on a family build. -> {id: result}."""
    specs = family.specs
    out = {}
    for fn in (k23_equivalent, k24_pathclass, k27_injection, k28_perturbation, k29_dialects, k30_ladder, k33_carrier, k6_within_carrier):
        r = fn(specs)
        out[r["id"]] = r
    for r in (k31_note(), k32_wrappers(specs), k14s_report(family)):
        out[r["id"]] = r
    return out
