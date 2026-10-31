"""Option lists from named-error hooks (3.4): exactly one hook per distractor, gold rank uniform over ordered options,
abstain options (NEI / None of the listed) shown only at k >= 3 and gold with probability 1/k (XF01)."""
from __future__ import annotations

import random
from collections import Counter

BUCKETS = [(2, 4, 0.35), (5, 9, 0.35), (10, 19, 0.15), (20, 60, 0.15)]

# Repair r2: XF01 / SC12 check the abstain-gold rate against 1/k within +/- 2 pp per k bucket and per abstain option,
# on cells as small as 12-60 rows, where independent 1/k draws miss by 4-8 pp at random (v1.2: none|2-4 6 / 33 vs
# 29.8% expected). Each draw is 1/k nudged by its cell's running deficit over the rows already written in this part
# (expected minus observed abstain-gold rows), so cells end within about one row of expectation. The nudge depends
# only on earlier rows, never on the row being built.
ABST_DEF = Counter()


# Repair r2: case-list case counts are drawn by option bucket (section 6: 2-4 35 / 5-9 35 / 10-19 15 / 20-60 15 of
# choice rows; large buckets come from case lists, 3.4). Non-case choice rows sit at k 2-9, so case lists carry the
# 10-19 and 20-60 buckets: weights 0.46 / 0.27 / 0.27 over the buckets a card offers, uniform inside a bucket
# (v1.2 drew uniformly over each card's list and then lost large counts to the token cap: 10-19 8.3%, 20-60 1.7%).
CASE_BUCKET_W = ((5, 9, 0.46), (10, 19, 0.27), (20, 60, 0.27))


def draw_ncases(rng, choices):
    avail = [(a, b, w) for a, b, w in CASE_BUCKET_W if any(a <= x <= b for x in choices)]
    if not avail:
        return rng.choice(choices)
    r = rng.random() * sum(w for _, _, w in avail)
    acc = 0.0
    for a, b, w in avail:
        acc += w
        if r < acc:
            return rng.choice([x for x in choices if a <= x <= b])
    a, b, _ = avail[-1]
    return rng.choice([x for x in choices if a <= x <= b])


def abst_bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def abst_p(kind, k):
    return min(1.0, max(0.0, 1.0 / k + 0.5 * ABST_DEF[(kind, abst_bucket(k))]))


def abst_note(row):
    tg = [t for t in row["meta"]["edge"] if t.startswith("abst:")]
    if tg and row.get("options"):
        k = len(row["options"])
        ABST_DEF[(tg[0][5:], abst_bucket(k))] += 1.0 / k - float(row["gold"] == row["options"][-1])


def draw_k(rng, lo=2, hi=9, weights=None):
    """Option count for a hook-built row: 2-4 or 5-9 (larger buckets come from case lists)."""
    if weights is None:
        return rng.randint(lo, hi)
    r = rng.random()
    acc = 0.0
    for (a, b), w in weights:
        acc += w
        if r < acc:
            return rng.randint(a, b)
    return rng.randint(lo, hi)


def single_hook_values(hk: dict) -> dict:
    """{value: hook id} for values that exactly one hook gives (SC3)."""
    out = {}
    for v, ids in hk.items():
        u = sorted(set(ids))
        if len(u) == 1:
            out[v] = u[0]
    return out


def pick_ranked(rng, gold, cands: dict, k_ord: int, r: int):
    """Choose k_ord - 1 distractors from cands {value: hook} with exactly r of them below gold (the caller draws r
    uniformly and resamples the structure when infeasible, so gold's rank stays uniform; R2-17).
    Returns (ordered values incl. gold, {value: hook}) or None."""
    below = sorted([v for v in cands if v < gold])
    above = sorted([v for v in cands if v > gold])
    nb, na = r, k_ord - 1 - r
    if nb > len(below) or na > len(above):
        return None
    b = rng.sample(below, nb)
    a = rng.sample(above, na)
    return sorted(b + [gold] + a), {v: cands[v] for v in b + a}


def kmax_all_ranks(gold, cands):
    """Largest ordered-option count at which EVERY gold rank is feasible (k_ord - 1 single-hook values on each side of
    gold). Repair r2: v1.2 rejected a structure only when the held rank was infeasible, and the 4-dead-try redraw then
    moved end ranks to the middle on k_ord >= 4 (val rows: first 8 / last 17 vs 24 expected of 96). Accepting a
    structure on this count (never on the drawn rank) keeps gold's rank uniform given k (R2-17; 3.4 resample)."""
    below = sum(1 for v in cands if v < gold)
    above = sum(1 for v in cands if v > gold)
    return 1 + min(below, above)


def kmax_all_ranks_list(below, above):
    """kmax_all_ranks for listing options (bands / named outcomes): below / above = eligible names on each side."""
    return 1 + min(len(below), len(above))


def rank_feasible(gold, cands, k_ord):
    below = sum(1 for v in cands if v < gold)
    above = sum(1 for v in cands if v > gold)
    return [r for r in range(k_ord) if r <= below and k_ord - 1 - r <= above]


def held_rank(want, k: int, rng=None):
    """Gold's rank among k ordered options from the uniform `u_rank` drawn once per base row (predraw) and held
    across every structure retry, so the retries that reject infeasible (structure, rank) pairs never pull the rank
    toward the middle (R2-17; repair r1.1: v1.0 re-drew the rank on each retry)."""
    if want is None:
        want = {}
    u = want.get("u_rank")
    if u is None:
        u = (rng.random() if rng is not None else 0.5)
        want["u_rank"] = u
    return min(int(u * k), k - 1)


CASE_STRICT_ATTEMPTS = 40


def case_target(want, n):
    """Target count of distractor cases whose visible primary scalar lies below the gold case's (0..n-1), from the
    held uniform `u_crank` (repair r1.1: v1.0 gold cases sat at the extreme of the case list on 77% of rows)."""
    u = want.get("u_crank")
    if u is None:
        u = 0.5
    return min(int(u * n), n - 1)


def case_strict(want):
    return want.get("_attempt", 0) < CASE_STRICT_ATTEMPTS


def round_robin(items, need, rng):
    """items: [(payload, kind)] -> `need` payloads spread over kinds (round robin, random order), or None."""
    by = {}
    for p, kd in items:
        by.setdefault(kd, []).append(p)
    for lst in by.values():
        rng.shuffle(lst)
    order = sorted(by)
    rng.shuffle(order)
    out = []
    while len(out) < need:
        moved = False
        for kd in order:
            if by[kd] and len(out) < need:
                out.append((by[kd].pop(), kd))
                moved = True
        if not moved:
            return None
    return out


def pick_cases_ranked(rng, golds, errs, n_err, t, prim):
    """Gold case + n_err single-error cases with exactly t of them strictly below gold on prim() and n_err - t
    strictly above (ties excluded). golds: [payload]; errs: [(payload, kind)]. Returns (gold, [(payload, kind)])."""
    gl = list(golds)
    rng.shuffle(gl)
    for g in gl[:40]:
        pg = prim(g)
        if pg is None:
            continue
        below = [(p, kd) for p, kd in errs if prim(p) is not None and prim(p) < pg]
        above = [(p, kd) for p, kd in errs if prim(p) is not None and prim(p) > pg]
        if len(below) < t or len(above) < n_err - t:
            continue
        b = round_robin(below, t, rng) if t else []
        a = round_robin(above, n_err - t, rng) if n_err - t else []
        if b is None or a is None:
            continue
        return g, b + a
    return None


def one_group(rng, pool_g, pool_e, need_err, gold_needed, grp):
    """Restrict both pools to one depth group (a case list never mixes groups): a random group among those that can
    fill the list. grp(payload) -> group key or None (None = not allowed)."""
    gs = {}
    for p in pool_g:
        g = grp(p)
        if g is not None:
            gs.setdefault(g, [[], []])[0].append(p)
    for p, kd in pool_e:
        g = grp(p)
        if g is not None:
            gs.setdefault(g, [[], []])[1].append((p, kd))
    ok = [g for g, (a, b) in gs.items() if len(b) >= need_err and (a or not gold_needed)]
    if not ok:
        return None
    g = rng.choice(sorted(ok))
    return gs[g][0], gs[g][1]


K_FALLBACK_ATTEMPTS = 150


def held_k(want, choices, kmax, rng=None):
    """Option count from the uniform `u_k` drawn once per base row and held across retries (repair r1.1: v1.0 drew k
    per attempt as min(draw, 1 + hooks), so the accepted k depended on the gold rank). A structure with too few
    single-hook values for the held k is resampled; after K_FALLBACK_ATTEMPTS the k is taken among the feasible
    counts (same uniform), so a hook-poor card cannot stall."""
    if want is None:
        want = {}
    u = want.get("u_k")
    if u is None:
        u = rng.random() if rng is not None else 0.5
        want["u_k"] = u
    k = choices[min(int(u * len(choices)), len(choices) - 1)]
    if k <= kmax:
        return k
    if want.get("_attempt", 0) < K_FALLBACK_ATTEMPTS:
        return None
    feas = [x for x in choices if x <= kmax]
    if not feas:
        return None
    return feas[min(int(u * len(feas)), len(feas) - 1)]
