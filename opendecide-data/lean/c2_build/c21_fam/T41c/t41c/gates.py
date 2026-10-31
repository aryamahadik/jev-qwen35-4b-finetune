"""PRE-FREEZE CPU gates (G0-lite 4.1) for T41c. Data only; no model, no network.

K1 format-only probe, K2 meta probe, K3 held-out-family probe, K4 composition (+ facts-absent stratum cells),
K5 delegation-cue balance, K6 solver A vs B (needs solver B; harness only), K7 probe power control (inside K1/K2 runs),
K8 token histogram, K9 names + faithfulness, K12 wording and dedupe. K10 (G13 pilot) is the orchestrator's;
K11 (A50 G6, A49c, G5-H, G3-H) is supplied by L-0 and not restated here.

Every gate returns {"id", "tag", "pass", ...numbers}. The probe harness is injected (probe.ProbeHarness is the local
stand-in for the one L-0 harness).
"""
import re
from collections import Counter, defaultdict

import numpy as np

from . import ids
from .ids import ALLOW, ALLOW_BENIGN, ASK, BLOCK
from .planner import FACTS_ABSENT_SHARE, SHARES
from .pools import approx_tokens
from .probe import ProbeHarness, dict_matrix
from .spec import label_of

PRE = "PRE-FREEZE KILL"
AUC_BAR, AUC_UB = 0.55, 0.60
BA4_BAR, BA4_UB = 0.28, 0.31
GAP_BAR = 0.05
PLACEHOLDER = "<SLOT>"
LEN_EDGES = (128, 256, 512, 1024)


def _res(gid, ok, **kw):
    return dict({"id": gid, "tag": PRE, "pass": bool(ok)}, **kw)


# ---------------------------------------------------------------------------------------------------------------
# masking and features
# ---------------------------------------------------------------------------------------------------------------
def masked_flat(rendered):
    """Flattened row with every slot region replaced by one fixed placeholder (K1: no payload tokens)."""
    regs = sorted(rendered.meta["slot_regions"], key=lambda r: (r[0], r[1]))
    texts = []
    for s in rendered.spans:
        t = s.text
        for (si, a, b) in sorted([r for r in regs if r[0] == s.idx], key=lambda r: -r[1]):
            t = t[:a] + PLACEHOLDER + t[b:]
        a = "".join(' %s="%s"' % (k, v) for k, v in sorted(s.attrs.items()) if k != "path")
        texts.append("<%s%s>\n%s\n</%s>" % (s.tag, a, t, s.tag))
    return "\n".join(texts)


_KEY_PATTERNS = [r'"([A-Za-z]+)_\d+":', r"^([A-Za-z]+)_\d+:", r"^([A-Za-z]+)_\d+ =", r"^## ([A-Za-z]+)$",
                 r"^([A-Za-z]+): ", r"<h2>([A-Za-z]+)</h2>", r"([A-Za-z]+)\[\d+\]:"]
_KEY_RE = [re.compile(p, re.M) for p in _KEY_PATTERNS]


def key_names(carrier_text):
    out = set()
    for r in _KEY_RE:
        out.update(r.findall(carrier_text))
    return sorted(out)


def len_bucket(n):
    return sum(n > e for e in LEN_EDGES)


def k1_features(spec, rendered):
    """Format-only features: carrier type, serialisation, length bucket (5), key names, facts flag; slot masked."""
    m = masked_flat(rendered)
    masked_carrier = _mask_span(rendered, rendered.carrier_span)
    # the source tag is NOT a K1 feature (G0-lite K1 lists carrier type, serialisation, length, keys, facts flag):
    # provenance decides nested/ASK labels by design, so it is reported separately by `provenance_probe`
    f = {"car=" + spec.carrier_type: 1, "fmt=" + spec.carrier_format: 1,
         "len=%d" % len_bucket(approx_tokens(m)): 1, "facts=" + ("p" if spec.facts.present else "a"): 1}
    for k in key_names(masked_carrier):
        f["key=" + k] = 1
    return f


def _mask_span(rendered, idx):
    t = rendered.spans[idx].text
    for (si, a, b) in sorted([r for r in rendered.meta["slot_regions"] if r[0] == idx], key=lambda r: -r[1]):
        t = t[:a] + PLACEHOLDER + t[b:]
    return t


def k2_features(spec, rendered):
    """Meta features: placement bin, visibility, wrapper style, slot token-length bucket, slot count, facts flag
    (for each slot, in slot order)."""
    f = {"nslots=%d" % (len(spec.directives) + len(spec.fills)): 1, "facts=" + ("p" if spec.facts.present else "a"): 1}
    slots = [(d.placement, d.visibility, d.wrapper, d.slot_bucket) for d in spec.directives] + [
        (x.placement, x.visibility, x.wrapper, x.bucket) for x in spec.fills]
    for i, (pl, vis, wr, bk) in enumerate(slots):
        f["s%d.place=%s" % (i, pl)] = 1
        f["s%d.vis=%s" % (i, vis)] = 1
        f["s%d.wrap=%s" % (i, wr)] = 1
        f["s%d.bucket=%d" % (i, bk)] = 1
    return f


def _views(rows):
    """Row index sets for the three binary views and the 4-way."""
    labels = [label_of(s) for s, _ in rows]
    y4 = np.array([ids.LABELS.index(l) for l in labels])
    b1 = np.array([1 if l in (BLOCK, ASK) else 0 for l in labels])
    return labels, y4, b1


def _probe_views(feats, rows, harness, gid, boot):
    labels, y4, b1 = _views(rows)
    groups = [s.group_id for s, _ in rows]
    X, _ = dict_matrix(feats)
    out = {}
    lab = np.array(labels)
    # B1 attack vs benign
    out["B1"] = harness.binary(X, b1, groups, 0, boot)
    out["B1"]["power_auc"] = harness.power(X, b1, groups, 0)
    # B2 BLOCK vs ASK
    idx = np.where((lab == BLOCK) | (lab == ASK))[0]
    out["B2"] = harness.binary(X[idx], (lab[idx] == BLOCK).astype(int), [groups[i] for i in idx], 1, boot)
    # B3 ALLOW vs ALLOW_BENIGN
    idx = np.where((lab == ALLOW) | (lab == ALLOW_BENIGN))[0]
    out["B3"] = harness.binary(X[idx], (lab[idx] == ALLOW_BENIGN).astype(int), [groups[i] for i in idx], 2, boot)
    out["4way"] = harness.kway(X, y4, groups, 3, boot)
    return out


def _judge(views, binary_only=False):
    ok, bad = True, []
    for k, v in views.items():
        if k == "4way":
            if binary_only:
                continue
            good = v["bal_acc"] <= BA4_BAR and v["ub"] <= BA4_UB
        else:
            good = v["auc"] <= AUC_BAR and v["ub"] <= AUC_UB
        if not good:
            ok = False
            bad.append(k)
    return ok, bad


def _validity(views):
    """K7: label-permutation sanity (AUC 0.50 +- 0.03) and the injected-leak power check (>= 0.80)."""
    perm_ok = all(abs(v["perm_auc"] - 0.5) <= 0.03 for k, v in views.items() if k != "4way")
    power_ok = views["B1"].get("power_auc", 0) >= 0.80
    return perm_ok, power_ok


def null_reference(feats, rows, n=10, seed=0):
    """INFORMATIONAL (not a bar): AUC of the same probe when labels are permuted WITHIN carrier type, which keeps every
    carrier's label mix. With ~60 sparse features and n ~ 1,000, max(AUC, 1 - AUC) sits well above 0.5 on pure noise;
    the bars are read next to this reference by the skeptic and Opus."""
    labels, y4, b1 = _views(rows)
    lab = np.array(labels)
    groups = np.array([s.group_id for s, _ in rows])
    cars = np.array([s.carrier_type for s, _ in rows])
    X, _ = dict_matrix(feats)
    rng = np.random.default_rng(seed)
    out = {}
    for name, sel, pos in (("B1", np.arange(len(rows)), lambda l: l in (BLOCK, ASK)),
                           ("B2", np.where((lab == BLOCK) | (lab == ASK))[0], lambda l: l == BLOCK),
                           ("B3", np.where((lab == ALLOW) | (lab == ALLOW_BENIGN))[0], lambda l: l == ALLOW_BENIGN)):
        y = np.array([1 if pos(l) else 0 for l in lab[sel]])
        vals = []
        for t in range(n):
            yp = y.copy()
            for c in set(cars[sel].tolist()):
                m = np.where(cars[sel] == c)[0]
                yp[m] = y[m][rng.permutation(len(m))]
            from .probe import oof_scores, auc_max
            vals.append(auc_max(yp, oof_scores(X[sel], yp, list(groups[sel]), seed=t)))
        out[name] = {"null_mean": float(np.mean(vals)), "null_p95": float(np.percentile(vals, 95))}
    return out


def gate_k1(rows, harness=ProbeHarness, boot=2000, feature_fn=k1_features, with_null=False):
    feats = [feature_fn(s, r) for s, r in rows]
    views = _probe_views(feats, rows, harness, "K1", boot)
    ok, bad = _judge(views)
    perm_ok, power_ok = _validity(views)
    extra = {"null_reference": null_reference(feats, rows)} if with_null else {}
    return _res("K1", ok and perm_ok and power_ok, views=views, failing=bad, valid=perm_ok and power_ok,
                note="invalid run (K7) is repeated and is not a fix iteration" if not (perm_ok and power_ok) else "", **extra)


def provenance_probe(rows, harness=ProbeHarness, boot=300):
    """INFORMATIONAL: source-tag probe (src tag + carrier type). Provenance decides labels by design (nested -> ASK),
    so this is a report line, not a bar."""
    feats = [{"src=" + s.carrier_src: 1, "car=" + s.carrier_type: 1} for s, _ in rows]
    return _probe_views(feats, rows, harness, "PROV", boot)


def gate_k2(rows, harness=ProbeHarness, boot=2000):
    feats = [k2_features(s, r) for s, r in rows]
    views = _probe_views(feats, rows, harness, "K2", boot)
    ok, bad = _judge(views, binary_only=True)
    perm_ok, power_ok = _validity(views)
    # wrapper-style share among agent-directed benign vs attack rows within 5 pp per style
    ben, att = Counter(), Counter()
    for s, _ in rows:
        lab = label_of(s)
        for d in s.directives:
            if not d.agent_directed:
                continue
            (ben if lab in (ALLOW_BENIGN, ALLOW) else att)[d.wrapper] += 1
    nb, na = max(1, sum(ben.values())), max(1, sum(att.values()))
    worst = max(abs(ben[w] / nb - att[w] / na) for w in ids.WRAPPERS)
    return _res("K2", ok and perm_ok and power_ok and worst <= 0.05, views=views, failing=bad,
                wrapper_share_max_diff=worst, valid=perm_ok and power_ok)


# ---------------------------------------------------------------------------------------------------------------
# K3 held-out-family probe
# ---------------------------------------------------------------------------------------------------------------
def gate_k3(train_rows, ho_rows, harness=ProbeHarness, boot=2000):
    """TF-IDF + LR on in-family train rows; (a) held-out in-family groups (5-fold group CV), (b) the HO block."""
    from .probe import auc_max, balanced_accuracy, group_folds
    texts = [r.flat() for _, r in train_rows]
    labels = np.array([ids.LABELS.index(label_of(s)) for s, _ in train_rows])
    groups = [s.group_id for s, _ in train_rows]
    b1 = (labels >= 2).astype(int)
    folds = group_folds(groups, 5, 0)
    pred_a = np.zeros(len(labels), dtype=int)
    score_a = np.zeros(len(labels))
    for f in range(5):
        tr, te = np.where(folds != f)[0], np.where(folds == f)[0]
        pred_a[te] = harness.tfidf([texts[i] for i in tr], labels[tr], [texts[i] for i in te], multi=True)
        score_a[te] = harness.tfidf([texts[i] for i in tr], b1[tr], [texts[i] for i in te])
    ho_texts = [r.flat() for _, r in ho_rows]
    ho_lab = np.array([ids.LABELS.index(label_of(s)) for s, _ in ho_rows])
    ho_b1 = (ho_lab >= 2).astype(int)
    pred_b = harness.tfidf(texts, labels, ho_texts, multi=True)
    score_b = harness.tfidf(texts, b1, ho_texts)
    a_ba, b_ba = balanced_accuracy(labels, pred_a), balanced_accuracy(ho_lab, pred_b)
    a_auc, b_auc = auc_max(b1, score_a), auc_max(ho_b1, score_b)
    ho_groups = [s.group_id for s, _ in ho_rows]
    ci_b = _ci(lambda y, p: balanced_accuracy(y, p), ho_lab, pred_b, ho_groups, boot)
    gap_ba, gap_auc = a_ba - b_ba, a_auc - b_auc
    return _res("K3", gap_ba <= GAP_BAR and gap_auc <= GAP_BAR, in_family_ba=a_ba, held_out_ba=b_ba, gap_ba=gap_ba,
                in_family_auc=a_auc, held_out_auc=b_auc, gap_auc=gap_auc, held_out_ba_ci95=ci_b,
                n_train=len(labels), n_ho=len(ho_lab),
                note="two rotations of the held-out draw are report-only")


def _ci(metric, y, p, groups, boot=2000):
    groups = np.asarray(groups)
    idx_by = defaultdict(list)
    for i, g in enumerate(groups):
        idx_by[g].append(i)
    arrs = [np.array(v) for v in idx_by.values()]
    rng = np.random.default_rng(5)
    vals = []
    for _ in range(boot):
        pick = rng.integers(0, len(arrs), len(arrs))
        idx = np.concatenate([arrs[j] for j in pick])
        vals.append(metric(y[idx], p[idx]))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


# ---------------------------------------------------------------------------------------------------------------
# K4 composition (+ R2-T41c-d stratum cells), K5 delegation-cue balance
# ---------------------------------------------------------------------------------------------------------------
def gate_k4(specs, N=None, tol=0.015):
    N = N or len(specs)
    labs = [label_of(s) for s in specs]
    n = len(specs)
    share = lambda c: c / n
    lab_c = Counter(labs)
    fails = []
    benign = lab_c[ALLOW] + lab_c[ALLOW_BENIGN]
    if abs(share(benign) - 0.50) > 0.01:
        fails.append("benign share %.3f" % share(benign))
    da = sum(1 for s in specs if s.subtype in ("sub.delegated", "sub.ambient"))
    if benign and da / benign < 0.30:
        fails.append("delegated+ambient of benign %.3f" % (da / benign))
    sub_c = Counter(s.subtype for s in specs)
    for b, sh in SHARES.items():
        if abs(share(sub_c[b]) - sh) > tol:
            fails.append("subtype %s %.3f vs %.3f" % (b, share(sub_c[b]), sh))
    exp_lab = {ALLOW: 0.15, ALLOW_BENIGN: 0.35, BLOCK: 0.35, ASK: 0.15}
    for l, sh in exp_lab.items():
        if abs(share(lab_c[l]) - sh) > tol:
            fails.append("label %s %.3f vs %.3f" % (l, share(lab_c[l]), sh))
    if share(lab_c[ASK]) < 0.12:
        fails.append("ASK < 12%")
    # per-carrier-type label mix within 8 pp of global
    by_car = defaultdict(Counter)
    for s, l in zip(specs, labs):
        by_car[s.carrier_type][l] += 1
    worst_car = 0.0
    for c, cnt in by_car.items():
        tot = sum(cnt.values())
        for l in ids.LABELS:
            worst_car = max(worst_car, abs(cnt[l] / tot - share(lab_c[l])))
    if worst_car > 0.08:
        fails.append("carrier label mix %.3f" % worst_car)
    pair = sum(1 for s in specs if s.pair_kind != "single")
    if share(pair) < 0.30:
        fails.append("pair share %.3f" % share(pair))
    multi = sum(1 for s in specs if len(s.directives) >= 2)
    if not 0.10 <= share(multi) <= 0.14:
        fails.append("multi-directive %.3f" % share(multi))
    pol = sum(1 for s in specs if s.declared_policy_file)
    # R2-T41c-d: facts-absent share per label, carrier type and subtype cell
    cells = defaultdict(lambda: [0, 0])
    for s, l in zip(specs, labs):
        for key in (("label", l), ("carrier", s.carrier_type), ("subtype", s.subtype)):
            cells[key][0] += 1
            cells[key][1] += 0 if s.facts.present else 1
    worst_cell, worst_key = 0.0, None
    for key, (cn, ca) in cells.items():
        dev = abs(ca / cn - FACTS_ABSENT_SHARE)
        slack = 1.0 / cn                                   # one row of rounding
        if dev - slack > worst_cell:
            worst_cell, worst_key = dev - slack, key
        if ca / cn < 0.25 - slack:
            fails.append("facts-absent floor %s %.3f" % (key, ca / cn))
    if worst_cell > 0.02:
        fails.append("facts-absent cell %s off by %.3f" % (worst_key, worst_cell))
    ab_all = sum(1 for s in specs if not s.facts.present) / n
    return _res("K4", not fails, fails=fails, n=n, benign_share=share(benign), delegated_ambient_of_benign=da / max(1, benign),
                label_shares={l: share(lab_c[l]) for l in ids.LABELS}, subtype_shares={b: share(sub_c[b]) for b in SHARES},
                worst_carrier_label_diff=worst_car, pair_share=share(pair), multi_directive_share=share(multi),
                declared_policy_share=share(pol), facts_absent_share=ab_all, worst_stratum_cell_dev=worst_cell)


def gate_k5(specs):
    """P(ALLOW_BENIGN | delegation clause) in [0.40, 0.70]; delegated + HARD rows >= 8% of N (labelled by table)."""
    from .table import HARD, risk
    clause = [s for s in specs if s.pointer.mode != "deleg.none"]
    ab = sum(1 for s in clause if label_of(s) == ALLOW_BENIGN)
    p = ab / max(1, len(clause))
    dh = 0
    for s in specs:
        env = s.env()
        for d in s.directives:
            if d.agent_directed and s.pointer.covers(d.did) and risk(d.action, env) == HARD:
                dh += 1
                break
    share = dh / len(specs)
    return _res("K5", 0.40 <= p <= 0.70 and share >= 0.08, p_allow_benign_given_clause=p, n_clause=len(clause),
                delegated_hard_share=share)


# ---------------------------------------------------------------------------------------------------------------
# K8 token histogram, K9 names and faithfulness, K12 wording and dedupe
# ---------------------------------------------------------------------------------------------------------------
def gate_k8(rows, token_fn=approx_tokens):
    toks = [token_fn(r.flat()) for _, r in rows]
    mean, mx = float(np.mean(toks)), max(toks)
    above = sum(t > 1024 for t in toks) / len(toks)
    return _res("K8", mean <= 800 and mx <= 1536 and above <= 0.10, mean=mean, max=mx, share_above_1024=above,
                tokenizer="approx_tokens proxy; L-0's K8 re-measures with C2's tokenizer",
                hist=dict(Counter(min(t // 128, 12) * 128 for t in toks)))


def gate_k9(specs, build_report, allow=None, heldout=None, block="train"):
    """Names + faithfulness: guard refusals <= 2%, anchor drops <= 3%, zero accepted rows off the allow-list,
    training rows carry no held-out value."""
    allow = allow or ids.load_manifest_names()
    off = 0
    for s in specs:
        off += len(ids.check_ids_on_manifest(ids.spec_guard_names(s), allow))
    ho_hits = 0
    if heldout and block != "ho":
        for s in specs:
            vals = [d.wrapper for d in s.directives] + [f.wrapper for f in s.fills]
            ho_hits += any(v in heldout["wrappers"] for v in vals)
            ho_hits += s.carrier_format in heldout["formats"]
            ho_hits += any(d.cls in heldout["goals"] for d in s.directives)
            ho_hits += any(p in heldout["placements"] for p in [d.placement for d in s.directives] + [f.placement for f in s.fills])
    ok = (build_report["guard_refusal_rate"] <= 0.02 and build_report["anchor_drop_rate"] <= 0.03 and off == 0
          and ho_hits == 0)
    return _res("K9", ok, guard_refusal_rate=build_report["guard_refusal_rate"], anchor_drop_rate=build_report["anchor_drop_rate"],
                off_list_ids=off, heldout_value_rows=ho_hits, other_drops=build_report["drops"])


def gate_k12(rows):
    """No wording > 2%; >= 50 wordings per task class and delegation mode; exact-duplicate directive text <= 2%."""
    n = len(rows)
    core = Counter()
    task_words = defaultdict(set)
    texts = Counter()
    seen_in_group = set()
    for s, r in rows:
        w = r.meta["wording"]
        for e in w["core"]:
            if e:
                core[e] += 1
        task_words[(s.task_class, s.pointer.mode)].add(w["task"])
        for d, t in zip(s.directives, r.slot_texts):
            # a task-edit pair carries the identical directive text in both members BY DESIGN: count it once per group
            if d.agent_directed and (s.group_id, t) not in seen_in_group:
                seen_in_group.add((s.group_id, t))
                texts[t] += 1
    top = max(core.values()) / n if core else 0.0
    dup = sum(c - 1 for c in texts.values() if c > 1) / max(1, sum(texts.values()))
    thin = sorted((k for k, v in task_words.items() if len(v) < 50))
    # no group in both train and dev: group ids carry the block prefix; verify no cross-block reuse
    by_block = defaultdict(set)
    for s, _ in rows:
        by_block[s.group_id].add(s.block)
    mixed = sum(1 for v in by_block.values() if len(v) > 1)
    return _res("K12", top <= 0.02 and not thin and dup <= 0.02 and mixed == 0, top_wording_share=top,
                task_cells_below_50=len(thin), n_task_cells=len(task_words), exact_dup_directive_share=dup,
                groups_in_two_blocks=mixed)


# ---------------------------------------------------------------------------------------------------------------
# K6 solver A vs solver B (harness only; B is written by a separate session)
# ---------------------------------------------------------------------------------------------------------------
def gate_k6_rows(rows, solve_b, strata=True):
    """(ii) full-set agreement of A (spec) and program B (rendered row + anchors only). solve_b(export) must return
    {"label": ...}. Disagreeing rows are dropped by the caller and counted here; > 2% fails, overall and per stratum."""
    from .render import export_for_b
    from .spec import label_of
    tot, dis = Counter(), Counter()
    bad_ids = []
    for s, r in rows:
        key = "present" if s.facts.present else "absent"
        tot[key] += 1
        tot["all"] += 1
        try:
            lb = solve_b(export_for_b(r))["label"]
        except Exception as e:                 # a crash in B is a disagreement
            lb = "ERROR:%s" % type(e).__name__
        if lb != label_of(s):
            dis[key] += 1
            dis["all"] += 1
            bad_ids.append(s.row_id)
    rates = {k: dis[k] / max(1, tot[k]) for k in tot}
    return _res("K6ii", all(v <= 0.02 for v in rates.values()), disagreement_rate=rates, disagreeing_rows=len(bad_ids),
                row_ids=bad_ids[:50])
