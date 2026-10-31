"""Selection helpers: yes/no pair balance and 'longest option is gold' balance for choice rows (G10)."""
from __future__ import annotations

from collections import defaultdict

from common import stable_shuffle


def longest_is_gold(options, gold) -> bool:
    lens = [len(o) for o in options]
    m = max(lens)
    return len(gold) == m and lens.count(m) == 1


def take_choice_balanced(units, n, key, k_of, lg_of):
    """Pick n units so that, within each option-count k, the share whose gold option is strictly the longest is about
    1/k (never above). units are opaque; k_of(u) and lg_of(u) read them. Returns (picked, leftover)."""
    by_k = defaultdict(lambda: {True: [], False: []})
    for u in stable_shuffle(units, "choice-bal", key):
        by_k[k_of(u)][bool(lg_of(u))].append(u)
    total = sum(len(v[True]) + len(v[False]) for v in by_k.values())
    picked, left = [], []
    ks = sorted(by_k)
    # proportional allocation of n over k buckets by availability
    alloc = {}
    rem = n
    for i, k in enumerate(ks):
        avail = len(by_k[k][True]) + len(by_k[k][False])
        alloc[k] = rem if i == len(ks) - 1 else min(avail, round(n * avail / max(total, 1)))
        rem -= alloc[k]
    for k in ks:
        want = alloc[k]
        n_lg = min(len(by_k[k][True]), round(want / k))       # about 1/k
        n_ot = want - n_lg
        if n_ot > len(by_k[k][False]):
            n_ot = len(by_k[k][False])
        picked += by_k[k][True][:n_lg] + by_k[k][False][:n_ot]
        left += by_k[k][True][n_lg:] + by_k[k][False][n_ot:]
    if len(picked) < n:  # top up from leftovers that are not longest-gold first
        extra = [u for u in left if not lg_of(u)][: n - len(picked)]
        ids = {id(u) for u in extra}
        picked += extra
        left = [u for u in left if id(u) not in ids]
    return picked[:n], left
