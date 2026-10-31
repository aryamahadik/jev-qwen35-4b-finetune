"""Pool planning, selection and the pure-computation decision rules of the VOICE data-production gates. CPU only.

Variants are plain dicts with at least: variant_id, source_row_id, source_family, source_label, generator ('A'|'B'),
stratum, band (0..3 or None), voice (A only), fallback_spans (bool), kept_by_checker (bool).
No audio, no TTS and no ASR run here: the GPU jobs (od-l4b) produce the measurements these functions consume.
"""
import collections
import math

from vcommon import (BAND_NAMES, BAND_SHARE, BAND_TOL, FALLBACK_SPAN_CAP, FAMILY_SOURCE_CAP, GEN_SOURCE_CAP, GENERATOR_SHARE, GENERATOR_TOL,
                     KEPT_FLOOR, KEPT_TARGET, MAX_VARIANTS_PER_SOURCE, MAX_VOICE_SHARE_OF_A, POOL_CAP, STRATA, STRATA_SHARE, STRATA_TOL,
                     VOICE_SHARE_OF_NEW_MAX)


def wilson_lower(k, n, z=1.96):
    if n == 0:
        return 0.0
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - r) / d


def wilson_upper(k, n, z=1.96):
    if n == 0:
        return 1.0
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c + r) / d


# ------------------------------------------------------------------------------------------------
# Pool sizing:   pool_b = target_b / survival_b * 1.1   (survival from the 500-row pilot), capped at 12,000
# ------------------------------------------------------------------------------------------------
def pool_plan(survival_by_band, kept_target=KEPT_TARGET, shares=BAND_SHARE, cap=POOL_CAP, margin=1.1):
    """survival_by_band: fraction of pilot variants that end up KEPT in band b (after band and span filters), in (0,1].
    Returns {'per_band': [...], 'total': n, 'capped': bool, 'expected_kept': n}"""
    per = []
    for sh, s in zip(shares, survival_by_band):
        if s <= 0:
            raise ValueError("a band with zero survival cannot be planned")
        per.append(math.ceil(round(kept_target * sh / s * margin, 6)))
    total = sum(per)
    capped = total > cap
    if capped:
        scale = cap / total
        per = [int(x * scale) for x in per]
        total = sum(per)
    exp = sum(int(p * s / margin) for p, s in zip(per, survival_by_band))
    return {"per_band": per, "total": total, "capped": capped, "expected_kept": exp}


def voice_share_ok(n_voice, n_new_rows):
    return n_voice <= VOICE_SHARE_OF_NEW_MAX * n_new_rows


# ------------------------------------------------------------------------------------------------
# Selection
# ------------------------------------------------------------------------------------------------
def select_kept(variants, rng, n_target=KEPT_TARGET, gen_family="GEN", shares=None):
    """Greedy randomised selection that honours every share and cap. Only variants that passed the span checker and have a band
    in 0..3 are eligible. Returns (kept list, report)."""
    elig = [v for v in variants if v.get("kept_by_checker") and v.get("band") in (0, 1, 2, 3)]
    rng.shuffle(elig)
    band_cap = [math.ceil(n_target * (s + 0.0)) for s in BAND_SHARE]
    strat_cap = {s: math.ceil(n_target * (STRATA_SHARE[s] + STRATA_TOL)) for s in STRATA}
    shares = shares or GENERATOR_SHARE
    gen_cap = {g: math.ceil(n_target * (shares[g] + GENERATOR_TOL)) for g in shares}
    cnt_band, cnt_strat, cnt_gen = collections.Counter(), collections.Counter(), collections.Counter()
    cnt_src, cnt_fam, cnt_voice = collections.Counter(), collections.Counter(), collections.Counter()
    n_fallback = 0
    kept = []
    skipped = collections.Counter()
    for v in elig:
        if len(kept) >= n_target:
            break
        if cnt_band[v["band"]] >= band_cap[v["band"]]:
            skipped["band_cap"] += 1
            continue
        if cnt_strat[v["stratum"]] >= strat_cap[v["stratum"]]:
            skipped["stratum_cap"] += 1
            continue
        if v["generator"] not in gen_cap:
            skipped["generator_off"] += 1                    # e.g. generator C while its dictionary licence record is missing
            continue
        if cnt_gen[v["generator"]] >= gen_cap[v["generator"]]:
            skipped["generator_cap"] += 1
            continue
        if cnt_src[v["source_row_id"]] >= MAX_VARIANTS_PER_SOURCE:
            skipped["per_source"] += 1
            continue
        fam_limit = GEN_SOURCE_CAP if v["source_family"] == gen_family else FAMILY_SOURCE_CAP
        if cnt_fam[v["source_family"]] >= math.ceil(n_target * fam_limit):
            skipped["family_cap"] += 1
            continue
        if v["generator"] == "A" and v.get("voice") is not None and cnt_voice[v["voice"]] >= math.ceil(MAX_VOICE_SHARE_OF_A * max(1, math.ceil(n_target * shares["A"]))):
            skipped["voice_cap"] += 1
            continue
        if v.get("fallback_spans") and n_fallback >= math.ceil(FALLBACK_SPAN_CAP * n_target):
            skipped["fallback_cap"] += 1
            continue
        kept.append(v)
        cnt_band[v["band"]] += 1
        cnt_strat[v["stratum"]] += 1
        cnt_gen[v["generator"]] += 1
        cnt_src[v["source_row_id"]] += 1
        cnt_fam[v["source_family"]] += 1
        if v["generator"] == "A" and v.get("voice") is not None:
            cnt_voice[v["voice"]] += 1
        n_fallback += int(bool(v.get("fallback_spans")))
    rep = shares_report(kept, shares)
    rep["skipped"] = dict(skipped)
    rep["achieved"] = len(kept)
    rep["ships_at_achieved_size"] = len(kept) < n_target
    rep["below_floor"] = len(kept) < KEPT_FLOOR
    return kept, rep


def shares_report(kept, shares=None):
    n = max(1, len(kept))
    band = collections.Counter(v["band"] for v in kept)
    strat = collections.Counter(v["stratum"] for v in kept)
    gen = collections.Counter(v["generator"] for v in kept)
    return {"n": len(kept), "band_share": [band[b] / n for b in range(4)], "stratum_share": {s: strat[s] / n for s in STRATA},
            "generator_share": {g: gen[g] / n for g in (shares or GENERATOR_SHARE)}}


def shares_within_tolerance(rep, shares=None):
    """V-C8 / V-D5 share checks. Returns (ok, details)."""
    det, ok = {}, True
    for b, (sh, tgt) in enumerate(zip(rep["band_share"], BAND_SHARE)):
        det["band_" + BAND_NAMES[b]] = abs(sh - tgt) <= BAND_TOL
        ok &= det["band_" + BAND_NAMES[b]]
    for s in STRATA:
        det["stratum_" + s] = abs(rep["stratum_share"][s] - STRATA_SHARE[s]) <= STRATA_TOL
        ok &= det["stratum_" + s]
    for g, tgt in (shares or GENERATOR_SHARE).items():
        det["generator_" + g] = abs(rep["generator_share"][g] - tgt) <= GENERATOR_TOL
        ok &= det["generator_" + g]
    return ok, det


# ------------------------------------------------------------------------------------------------
# V-C6 label drift (kept vs pool, inside each source family) and drop-only rebalancing
# ------------------------------------------------------------------------------------------------
def label_drift(pool, kept, max_pp=0.03):
    """Per source family and class: |share in kept - share in pool| <= 3 pp. Returns (ok, {family: {class: diff}})."""
    out, ok = {}, True
    fams = {v["source_family"] for v in pool}
    for f in fams:
        p = [v for v in pool if v["source_family"] == f]
        k = [v for v in kept if v["source_family"] == f]
        if not k:
            continue
        pc, kc = collections.Counter(v["source_label"] for v in p), collections.Counter(v["source_label"] for v in k)
        d = {c: kc[c] / len(k) - pc[c] / len(p) for c in set(pc) | set(kc)}
        out[f] = d
        ok &= all(abs(x) <= max_pp for x in d.values())
    return ok, out


def rebalance_family(kept, pool, family, max_pp=0.03):
    """Drop kept rows of over-represented classes (never generates labels). Returns the new kept list."""
    p = [v for v in pool if v["source_family"] == family]
    pc = collections.Counter(v["source_label"] for v in p)
    k = [v for v in kept if v["source_family"] == family]
    rest = [v for v in kept if v["source_family"] != family]
    classes = list(pc)
    for _ in range(len(k)):
        kc = collections.Counter(v["source_label"] for v in k)
        if not k:
            break
        diffs = {c: kc[c] / len(k) - pc[c] / len(p) for c in classes}
        worst = max(diffs, key=diffs.get)
        if diffs[worst] <= max_pp:
            break
        for i, v in enumerate(k):
            if v["source_label"] == worst:
                del k[i]
                break
    return rest + k


# ------------------------------------------------------------------------------------------------
# V-D decision rules (pure functions of measurements)
# ------------------------------------------------------------------------------------------------
def number_form_decision(n_digits, n_words):
    """V-D1: the majority form is the one at 60 percent or more; otherwise MIXED and the observed mix replaces the 15 percent rule."""
    n = n_digits + n_words
    if n == 0:
        return {"decision": "NO_DATA"}
    d, w = n_digits / n, n_words / n
    if d >= 0.60:
        return {"decision": "digits", "majority_share": d, "minority_target": 0.15}
    if w >= 0.60:
        return {"decision": "words", "majority_share": w, "minority_target": 0.15}
    return {"decision": "mixed", "digits_share": d, "words_share": w, "minority_target": None}


def padding_decision(match_by_padding, reference_key, min_match=0.99, within_pp=0.005):
    """V-D2: smallest trailing-silence padding (ms) whose last-three-words match rate vs the long-padding reference is >= 99 percent
    and within 0.5 pp of the reference. match_by_padding: {ms: fraction of utterances whose last 3 words equal the reference's}."""
    ref = match_by_padding[reference_key]
    for ms in sorted(k for k in match_by_padding if k != reference_key):     # the reference padding is not a candidate
        v = match_by_padding[ms]
        if v >= min_match and ref - v <= within_pp + 1e-9:
            return {"padding_ms": ms, "rate": v}
    return {"padding_ms": None, "reason": "no padding reaches 99 percent: voice rows wait; question goes to Opus and the owner"}


def pilot_reach(band_counts, n_pilot=500, shares=BAND_SHARE, min_frac=0.5):
    """V-D3: every kept band must be reached by at least 50 percent of its designed count (>= 75, 87, 62, 25 of 500)."""
    need = [math.ceil(n_pilot * s * min_frac) for s in shares]
    ok = all(c >= nd for c, nd in zip(band_counts, need))
    return ok, need


def condition_filter(rows_by_condition, max_over=0.5):
    """V-D3: remove any condition with more than 50 percent of its rows over 25 percent WER. rows_by_condition: {cond: [band or None]}."""
    removed = {c: sum(1 for b in bs if b is None) / len(bs) for c, bs in rows_by_condition.items() if bs and sum(1 for b in bs if b is None) / len(bs) > max_over}
    return sorted(removed), removed


def clean_condition_median_ok(wers, max_median=0.03):
    s = sorted(wers)
    return (s[len(s) // 2] if s else 1.0) <= max_median


def short_utterance_rule(wers_clean_short, max_wer=0.08):
    """V-D4: if clean-condition WER of the under-20-token utterances exceeds 8 percent they are excluded from generator A."""
    if not wers_clean_short:
        return {"exclude_short_from_A": None}
    m = sum(wers_clean_short) / len(wers_clean_short)
    return {"exclude_short_from_A": m > max_wer, "mean_wer": m}


def consistency_ok(wer_a, wer_b, max_median_abs_diff=0.01):
    d = sorted(abs(a - b) for a, b in zip(wer_a, wer_b))
    return (d[len(d) // 2] if d else 0.0) <= max_median_abs_diff, (d[len(d) // 2] if d else None)


def survival_report(results):
    """V-D6. results: list of check_doc outputs (+ band). Returns kept %, altered % by role, mean/median WER per band."""
    n = len(results)
    kept = sum(1 for r in results if r["kept"])
    alt = collections.Counter()
    for r in results:
        for s in r["spans"]:
            if s["status"] not in ("survived", "recovered"):
                alt[s["role"] + ("/" + s["kind"] if s["kind"] else "")] += 1
        if not r["global_negation_ok"]:
            alt["negation/global"] += 1
    by_band = collections.defaultdict(list)
    for r in results:
        by_band[r.get("band")].append(r["wer"])
    stats = {str(b): {"n": len(w), "mean": sum(w) / len(w), "median": sorted(w)[len(w) // 2]} for b, w in by_band.items() if w}
    return {"n": n, "kept_pct": kept / n if n else 0.0, "altered_rows_by_role": dict(alt), "wer_by_band": stats,
            "kept_ge_floor": kept >= KEPT_FLOOR}


def number_form_minority(forms_counts, decision, target=0.15, tol=0.05):
    """Gate input for the number-form rule. forms_counts = {'digits': n, 'words': n} over the numeric spans of the KEPT rows' raw ASR.
    With a majority form (V-D1) the minority form must be 15 +- 5 pp; with MIXED the observed mix stands and nothing is checked."""
    n = sum(forms_counts.values())
    if decision.get("decision") == "mixed" or n == 0:
        return True, None
    minority = forms_counts["words" if decision["decision"] == "digits" else "digits"] / n
    return abs(minority - target) <= tol + 1e-9, minority


def stress_set(variants):
    """Altered variants (dropped by the span checker, drop-only) form the dev-only stress set: training-pool sources, so they are
    labelled 'training-pool stress, not generalisation'. Returns their ids and reasons."""
    return [{"variant_id": v["variant_id"], "reasons": v.get("reasons", []), "label": "training-pool stress, not generalisation"} for v in variants if not v.get("kept_by_checker")]
