"""Family-independent PRE-FREEZE CPU gate helpers (data only; no model).

Row conventions (all families): a record is a dict with at least
  family, row_id, sub_block, group_id, pair_role (None | "a" | "b"), gold (label), gold_letter,
  options [{"letter","label","text"}...] in DISPLAY order, rendered {"context","question","options_text","text"},
  slots {name: value}, wording {"form_id","idx"}, names {category: [ids]}, template_id.

Probes are NOT implemented here: G5 says L-0 owns ONE probe harness. A gate takes a `harness` object with
    harness.binary(texts_or_features, y, groups) -> {"auc": float, "upper": float, "valid": bool}
    harness.kway(texts_or_features, y, groups, k)  -> {"bacc": float, "upper": float, "valid": bool}
and this module supplies the feature extractors and group keys the G0-lites name. Tests use a stub harness.
"""
import collections
import re

from . import util

BINARY_AUC, BINARY_UPPER = 0.55, 0.60


def kway_bars(k):
    return 1.0 / k + 0.03, 1.0 / k + 0.06


def result(gid, ok, **detail):
    return dict(id=gid, ok=bool(ok), **detail)


# ---- counts, shares, bands -------------------------------------------------------------------------------
def share_band(gid, num, den, lo, hi, **extra):
    s = (num / den) if den else 0.0
    return result(gid, lo <= s <= hi, share=round(s, 4), num=num, den=den, band=[lo, hi], **extra)


def size_mix_gate(gid, records, expected_sizes, expected_mix, fam_tol=0.02, mix_tol=0.03, key="sub_block"):
    """expected_sizes: {sub_block: rows}; expected_mix: {sub_block: {label: share}} (shares sum to 1 per sub-block).
    Sizes are compared as shares of the family (+-fam_tol), label mixes as shares of the sub-block (+-mix_tol)."""
    n = len(records)
    tot = float(sum(expected_sizes.values()))
    by = collections.defaultdict(list)
    for r in records:
        by[r[key]].append(r)
    problems = []
    for sb, rows in expected_sizes.items():
        got = len(by.get(sb, []))
        if abs(got / n - rows / tot) > fam_tol:
            problems.append(("size", sb, round(got / n, 4), round(rows / tot, 4)))
        lab = collections.Counter(x["gold"] for x in by.get(sb, []))
        for l, sh in expected_mix.get(sb, {}).items():
            g = lab.get(l, 0) / max(1, len(by.get(sb, [])))
            if abs(g - sh) > mix_tol:
                problems.append(("mix", sb, l, round(g, 4), sh))
    return result(gid, not problems, problems=problems, n=n)


def pair_share(records):
    paired = sum(1 for r in records if r.get("pair_role") in ("a", "b"))
    return paired / len(records) if records else 0.0


def pair_share_gate(gid, records, minimum, per_sub_block=None):
    s = pair_share(records)
    probs = []
    if per_sub_block:
        by = collections.defaultdict(list)
        for r in records:
            by[r["sub_block"]].append(r)
        for sb, m in per_sub_block.items():
            if pair_share(by.get(sb, [])) < m - 0.02:
                probs.append((sb, round(pair_share(by.get(sb, [])), 4), m))
    return result(gid, s >= minimum and not probs, share=round(s, 4), minimum=minimum, problems=probs)


def pair_integrity(records):
    """Every group_id with pair_role a/b has exactly one a and one b."""
    g = collections.defaultdict(list)
    for r in records:
        if r.get("pair_role") in ("a", "b"):
            g[r["group_id"]].append(r["pair_role"])
    bad = [k for k, v in g.items() if sorted(v) != ["a", "b"]]
    return result("pair_integrity", not bad, bad_groups=bad[:10], n_groups=len(g))


# ---- gold-letter / position balance ----------------------------------------------------------------------
def letter_share_gate(gid, records, k, tol=0.02, key="sub_block"):
    by = collections.defaultdict(list)
    for r in records:
        by[r[key]].append(r)
    problems = []
    for sb, rows in by.items():
        if len(rows) < 10 * k:
            continue
        c = collections.Counter(x["gold_letter"] for x in rows)
        for i in range(k):
            sh = c.get(util.LETTERS[i], 0) / len(rows)
            if abs(sh - 1.0 / k) > tol:
                problems.append((sb, util.LETTERS[i], round(sh, 4)))
    return result(gid, not problems, problems=problems, k=k, tol=tol)


# ---- tokens ----------------------------------------------------------------------------------------------
def token_gate(gid, records, token_fn=util.approx_tokens, mean_max=800, hard_cap=1536, over1024=0.10):
    toks = [token_fn(r["rendered"]["text"]) for r in records]
    n = len(toks) or 1
    mean = sum(toks) / n
    over_cap = sum(1 for t in toks if t > hard_cap)
    over_1024 = sum(1 for t in toks if t > 1024)
    ok = mean <= mean_max and over_cap == 0 and (over_1024 / n) <= over1024
    return result(gid, ok, mean=round(mean, 1), max=max(toks) if toks else 0, over_cap=over_cap,
                  share_over_1024=round(over_1024 / n, 4), token_fn=getattr(token_fn, "__name__", "token_fn"))


# ---- wording ---------------------------------------------------------------------------------------------
def wording_gate(gid, records, min_forms=50, max_share=0.02, min_per_form=None):
    """>= min_forms distinct wordings per question form, no wording above max_share of the family. With the SEED
    pool (a handful of templates) this fails by design until the Haiku reword export is plugged in."""
    n = len(records)
    per_form = collections.defaultdict(set)
    c = collections.Counter()
    for r in records:
        w = r["wording"]
        per_form[w["form_id"]].add(w["idx"])
        c[(w["form_id"], w["idx"])] += 1
    few = {f: len(s) for f, s in per_form.items() if len(s) < (min_per_form or min_forms)}
    top = max(c.values()) / n if n else 0.0
    return result(gid, not few and top <= max_share, forms=len(per_form), forms_below_min=len(few),
                  top_share=round(top, 4), min_forms=min_per_form or min_forms)


def template_share_gate(gid, records, max_share=0.02):
    c = collections.Counter(r["template_id"] for r in records)
    n = len(records) or 1
    top = max(c.values()) / n if c else 0.0
    return result(gid, top <= max_share, top_share=round(top, 4), n_templates=len(c))


def slot_survival_gate(gid, records):
    lost = []
    for r in records:
        t = r["rendered"]["text"]
        miss = [k for k, v in r.get("slots", {}).items() if str(v) not in t]
        if miss:
            lost.append((r["row_id"], miss))
    return result(gid, not lost, lost=lost[:10], n_lost=len(lost))


# ---- names / lint ----------------------------------------------------------------------------------------
def name_guard_gate(gid, records, allowlist, family, extra_forbidden=()):
    bad = []
    for r in records:
        for cat, ident in allowlist.check_names(family, r["names"]):
            bad.append((r["row_id"], cat, ident))
        for lit in extra_forbidden:
            if lit and lit in r["rendered"]["text"]:
                bad.append((r["row_id"], "literal", "<hidden>"))
    return result(gid, not bad, violations=bad[:10], n=len(bad))


def lint_gate(gid, records, lint_fn, text_getter):
    bad = []
    for r in records:
        for t in text_getter(r):
            v = lint_fn(t)
            if v:
                bad.append((r["row_id"], v[0]))
    return result(gid, not bad, violations=bad[:10], n=len(bad))


# ---- probes (interface only) -----------------------------------------------------------------------------
def probe_binary_gate(gid, harness, X, y, groups, auc_bar=BINARY_AUC, upper_bar=BINARY_UPPER, **extra):
    out = harness.binary(X, y, groups)
    ok = out.get("valid", True) and out["auc"] <= auc_bar and out["upper"] <= upper_bar
    return result(gid, ok, auc=round(out["auc"], 4), upper=round(out["upper"], 4), bars=[auc_bar, upper_bar],
                  valid=out.get("valid", True), n=len(y), **extra)


def probe_kway_gate(gid, harness, X, y, groups, k, **extra):
    bacc_bar, up_bar = kway_bars(k)
    out = harness.kway(X, y, groups, k)
    ok = out.get("valid", True) and out["bacc"] <= bacc_bar and out["upper"] <= up_bar
    return result(gid, ok, bacc=round(out["bacc"], 4), upper=round(out["upper"], 4), bars=[round(bacc_bar, 4), round(up_bar, 4)],
                  valid=out.get("valid", True), n=len(y), k=k, **extra)


def tv_gate(gid, dist_a, dist_b, bar):
    d = util.tv_distance(dist_a, dist_b)
    return result(gid, d <= bar, tv=round(d, 4), bar=bar)


# ---- solver agreement ------------------------------------------------------------------------------------
def agreement_gate(gid, records, solver_b_fn, drop_bar=0.01):
    """P-1. solver_b_fn(record) -> label (written by the separate solver-B session). Rows with A != B are returned for
    dropping; disagreement above drop_bar means spec ambiguity (the fix iteration)."""
    bad = [r["row_id"] for r in records if solver_b_fn(r) != r["gold"]]
    rate = len(bad) / len(records) if records else 0.0
    return result(gid, rate <= drop_bar, disagreement=round(rate, 5), dropped_ids=bad)


def ngram_texts(records, getter):
    return [getter(r) for r in records]
