"""Round-1 card and row plan for the program samplers (G0 section 1 sizes and option buckets; section 8 shares)."""
from __future__ import annotations

from common import rng

# candidate rows (about 1.5x the round-1 rows): S1-S4 810, S6 540
ROWS = {"S1": 810, "S2": 810, "S3": 810, "S4": 810, "S6": 540}
NCARDS = {"S1": 14, "S2": 14, "S3": 14, "S4": 14, "S6": 9}
# option-bucket shares per sampler (section 1, AR14)
KSHARE = {"S1": {"2-4": .45, "5-9": .35, "10-19": .20}, "S2": {"2-4": .55, "5-9": .45},
          "S3": {"5-9": .10, "10-19": .40, "20-60": .50}, "S4": {"2-4": .55, "5-9": .45},
          "S6": {"2-4": .575, "5-9": .425}}
KR = {"2-4": (2, 4), "5-9": (5, 9), "10-19": (10, 19), "20-60": (20, 60)}


def program_plan(seed_tag="r1"):
    r = rng("plan", seed_tag)
    cards = []
    for s in ("S1", "S2", "S3", "S4", "S6"):
        n = NCARDS[s]
        for i in range(n):
            if s == "S3":
                ctype = "partition" if i % 2 == 0 else "dlist"
                k = [22, 21, 22, 20, 22, 22, 22, 21, 23, 20, 22, 22, 12, 12][i]   # R2-25 lever 3: low end per bucket;
                # repair r1 (G10 buckets): AR14 puts 20-60 only on all-codes rows (60% of forward rows), so 50% of S3
                # choice rows in 20-60 needs about 6 / 7 of the cards at >= 20 codes
                # (partition cards are drawn 2 codes above 20: their split step can end up to 2 leaves short)
            elif s == "S6":
                ctype, k = "desc", [4, 5, 6, 7, 8, 9, 9, 6, 8][i]
            else:
                ctype = "amo" if i < round(n * 0.7) else "first"
                ks = {"S1": [10, 11, 10, 5, 6, 7, 4, 8, 9, 5, 6, 7, 10, 8], "S2": [4, 5, 6, 7, 8, 4, 5, 6, 7, 8, 5, 6, 7, 4],
                      "S4": [4, 5, 6, 7, 8, 4, 5, 6, 7, 8, 5, 6, 7, 6]}[s]   # R2-25 lever 3: low end per bucket
                k = ks[i]
            cards.append({"sampler": s, "ctype": ctype, "k": k, "idx": i})
    r.shuffle(cards)
    # name modes (G0 8: neutral 40 / swapped 30 / other 30 of choice ROWS; repair r1): cards differ in their expected
    # choice-row counts, so the modes are assigned by expected choice rows, not by card count. Swapped needs a pack
    # label word per term, so it is drawn only on cards with k <= 9 terms (as before).
    assign_modes(cards, r)
    prog = [c for c in cards if c["sampler"] != "S6"]
    opens = r.sample([c for c in prog if c["sampler"] != "S3" or c["ctype"] == "dlist"], round(0.20 * len(prog)))
    for c in cards:
        c["world"] = "open" if c in opens else "closed"
    inv_cands = [c for c in prog if c["world"] == "closed" and (c["ctype"] == "amo" or c["ctype"] == "partition")]
    for c in r.sample(inv_cands, 11):
        c["inverted"] = True
    fs_cands = [c for c in prog if not c.get("inverted")]
    for c in r.sample(fs_cands, 6):
        c["fewshot"] = True
    for c in cards:
        c["examples_on"] = r.random() < 0.5
        c["lookalike"] = c["mode"] == "invented" and r.random() < 0.35
        c["sectioned"] = c["sampler"] == "S4" and r.random() < 0.3
        c["prose_record"] = c["sampler"] == "S4" or (c["sampler"] in ("S1", "S2") and r.random() < 0.25)
        c["conv"] = c["sampler"] in ("S1", "S2", "S4", "S6") and r.random() < 0.5
        c["n_split"] = 2 if c["ctype"] == "partition" else 0
        c["n_rows"] = round(ROWS[c["sampler"]] / NCARDS[c["sampler"]])
    # consequence lines on 50% of program cards (G0 8: 50 +/- 5; repair r1: an exact half, not a per-card coin)
    cq = set(id(c) for c in r.sample(cards, round(0.5 * len(cards))))
    for c in cards:
        c["conseq_on"] = id(c) in cq
    # per-card option-bucket shares so that each sampler meets its section-1 allocation (AR14) although cards differ
    # in how many terms they hold (repair r1, G10 option buckets)
    set_kshares(cards)
    for o, c in enumerate(cards):
        c["ordinal"] = o
    return cards


def exp_choice_rows(c):
    n = ROWS[c["sampler"]] / NCARDS[c["sampler"]]
    return n * (0.60 if c.get("inverted") else 0.50)     # the per-card choice-row controller's shares


def assign_modes(cards, r):
    tgt = {"neutral": 0.40, "swapped": 0.30, "invented": 0.30}
    tot = sum(exp_choice_rows(c) for c in cards)
    got = {m: 0.0 for m in tgt}
    order = sorted(cards, key=lambda c: (-exp_choice_rows(c), c["k"] > 9, r.random()))
    # cards that cannot be swapped first, so the swapped share lands on the cards that can carry it
    order = [c for c in order if c["k"] > 9] + [c for c in order if c["k"] <= 9]
    for c in order:
        allowed = ["neutral", "invented"] + (["swapped"] if c["k"] <= 9 else [])
        m = max(allowed, key=lambda m: (tgt[m] * tot - got[m], r.random()))
        c["mode"] = m
        got[m] += exp_choice_rows(c)

    def loss():
        return sum((got[m] / tot - tgt[m]) ** 2 for m in tgt)
    # pairwise swaps (allowed modes only) while they bring the weighted shares closer to 40 / 30 / 30
    improved = True
    while improved:
        improved = False
        for a in cards:
            for b in cards:
                ma, mb = a["mode"], b["mode"]
                if ma == mb or (mb == "swapped" and a["k"] > 9) or (ma == "swapped" and b["k"] > 9):
                    continue
                l0 = loss()
                wa, wb = exp_choice_rows(a), exp_choice_rows(b)
                got[ma] += wb - wa
                got[mb] += wa - wb
                if loss() < l0 - 1e-12:
                    a["mode"], b["mode"] = mb, ma
                    improved = True
                else:
                    got[ma] -= wb - wa
                    got[mb] -= wa - wb


def card_kmax(c):
    if c.get("kmax_real") is not None:      # probed: terms on the drawn card (+ the open-world abstain slot)
        return c["kmax_real"]
    if c["sampler"] == "S6":
        return c["k"]
    return c["k"] + (1 if c.get("world") == "open" else 0)


def set_kshares(cards):
    for s in ("S1", "S2", "S4", "S6"):
        card_kshares([c for c in cards if c["sampler"] == s], KSHARE[s])


def card_kshares(cs, target):
    """Water-filling: the largest bucket first, spread evenly over the cards that can reach it (capacity 1 per card)."""
    if not cs:
        return
    cap = {id(c): 1.0 for c in cs}
    sh = {id(c): {b: 0.0 for b in target} for c in cs}
    for b in sorted(target, key=lambda b: -KR[b][0]):
        need = target[b] * len(cs)
        elig = [c for c in cs if KR[b][0] <= card_kmax(c) and cap[id(c)] > 1e-9]
        while need > 1e-9 and elig:
            per = need / len(elig)
            nxt = []
            for c in elig:
                give = min(per, cap[id(c)])
                sh[id(c)][b] += give
                cap[id(c)] -= give
                need -= give
                if cap[id(c)] > 1e-9:
                    nxt.append(c)
            elig = nxt
    for c in cs:
        if cap[id(c)] > 1e-9:     # left-over capacity goes to the smallest bucket the card can reach
            b = min((b for b in target if KR[b][0] <= card_kmax(c)), key=lambda b: KR[b][0])
            sh[id(c)][b] += cap[id(c)]
        c["kshare"] = {b: round(v, 4) for b, v in sh[id(c)].items() if v > 1e-6}


def k_drawer(sampler, r, kmax_terms, has_abstain_slots=0, kshare=None):
    """Draw (k, s3_subset). The bucket is the one furthest below the card's share (the sampler's section-1 shares,
    spread over cards by card_kshares; a stratified draw, repair r1), k uniform inside the bucket over feasible values.
    draw.note(k, subset) records an emitted choice row; draw.k_in(bucket) redraws k inside one bucket."""
    sh = kshare or KSHARE[sampler]
    cnt = {b: 0 for b in sh}
    s3 = [0, 0]          # S3: rows, all-codes rows (AR14: 60% all-codes)

    def k_in(b):
        lo, hi = KR[b]
        hi = min(hi, kmax_terms + has_abstain_slots)
        lo = min(lo, hi)
        return r.randint(lo, hi)

    def draw():
        if sampler == "S3":
            n = kmax_terms
            if s3[1] < 0.6 * (s3[0] + 1) - 0.5 + r.random() * 0.5:
                return None, False          # all-codes row
            return min(n, r.randint(8, 15)), True
        tot = sum(cnt.values()) + 1
        b = max(sh, key=lambda b: (sh[b] * tot - cnt[b], r.random()))
        return k_in(b), False

    def note(k, subset=False):
        if sampler == "S3":
            s3[0] += 1
            s3[1] += int(k is None or not subset)
            return
        from samplers import bucket_of
        b = bucket_of(k)
        if b in cnt:
            cnt[b] += 1
    draw.k_in = k_in
    draw.note = note
    return draw
