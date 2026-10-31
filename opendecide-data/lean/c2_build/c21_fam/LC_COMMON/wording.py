"""Wording pools: question forms (>= 50 wording ids each, none above 2% of rows) and card/task phrasing.

Wording text is Claude-authored (Haiku medium) LATER and arrives as a JSON pool; this module only
  * validates a pool (>= 50 wordings per form, unique ids, every {slot} known),
  * picks a wording per row so that no wording exceeds ceil(N / W) uses (<= 2% when W >= 50),
  * hashes the pool for the template/wording-pool hash export,
  * builds a clearly flagged TEST-ONLY pool for unit tests and the dry run. A test-only pool is refused by `require_real`.
Pool JSON: {"version": 1, "test_only": false, "forms": {FORM_ID: [{"id": "w001", "text": "... {slot} ..."}, ...]}}
"""
import hashlib
import json
import math
import re

SLOT = re.compile(r"\{([a-z_]+)\}")
MIN_WORDINGS = 50


class PoolError(ValueError):
    pass


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pool_hash(pool):
    return hashlib.sha256(json.dumps(pool, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(pool, forms, slots_by_form, min_wordings=MIN_WORDINGS):
    """Returns a list of problems ([] = ok)."""
    bad = []
    for form in forms:
        ws = pool.get("forms", {}).get(form)
        if not ws:
            bad.append("missing form %s" % form)
            continue
        if len(ws) < min_wordings:
            bad.append("form %s has %d wordings (< %d)" % (form, len(ws), min_wordings))
        ids = [w["id"] for w in ws]
        if len(set(ids)) != len(ids):
            bad.append("form %s has duplicate ids" % form)
        texts = [w["text"] for w in ws]
        if len(set(texts)) != len(texts):
            bad.append("form %s has duplicate texts" % form)
        allowed = set(slots_by_form.get(form, ()))
        for w in ws:
            miss = set(SLOT.findall(w["text"])) - allowed
            if miss:
                bad.append("form %s wording %s uses unknown slots %s" % (form, w["id"], sorted(miss)))
            need = allowed - set(SLOT.findall(w["text"]))
            if need and slots_by_form.get(form + "#required", None):
                bad.append("form %s wording %s misses required slots %s" % (form, w["id"], sorted(need)))
    return bad


def require_real(pool):
    if pool.get("test_only"):
        raise PoolError("a TEST-ONLY wording pool cannot be used to build rows")
    return pool


class Picker:
    """Least-used-first wording choice: with W wordings and N picks no wording is used more than ceil(N / W) times."""

    def __init__(self, pool, rng):
        self.pool = pool
        self.rng = rng
        self.use = {}

    def pick(self, form):
        ws = self.pool["forms"][form]
        use = self.use.setdefault(form, {w["id"]: 0 for w in ws})
        m = min(use.values())
        cands = [w for w in ws if use[w["id"]] == m]
        w = self.rng.choice(cands)
        use[w["id"]] += 1
        return w

    def render(self, form, **slots):
        w = self.pick(form)
        return w["id"], w["text"].format(**slots)

    def max_share(self, form):
        use = self.use.get(form, {})
        n = sum(use.values())
        return (max(use.values()) / n) if n else 0.0


def make_test_pool(forms, n=MIN_WORDINGS, slot_of=None):
    """TEST-ONLY placeholders (not wording). Every text carries a visible tag so it can never pass for a real pool.
    `slot_of` maps a form to the slot name its text embeds (default 'ask')."""
    slot_of = slot_of or {}
    return {"version": 1, "test_only": True,
            "forms": {f: [{"id": "t%03d" % k, "text": "[TEST-ONLY %s #%d] {%s}" % (f, k, slot_of.get(f, "ask"))} for k in range(n)]
                      for f in forms}}
