"""Wording pools: question forms (>= 50 wording ids each, none above 2% of rows).

Wording text is Claude-authored (Haiku) LATER and arrives as a JSON pool; this module only validates a pool, picks a wording
per row (least-used-first, so no wording exceeds ceil(N / W) uses), hashes the pool and builds a clearly flagged TEST-ONLY pool
for unit tests and the dry run. A test-only pool is refused by `require_real`.
Pool JSON: {"version": 1, "test_only": false, "forms": {FORM_ID: [{"id": "w001", "text": "... {slot} ..."}, ...]}}
Writers get the question forms and slots only, never the literal-ban list.
"""
import hashlib
import json
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


def validate(pool, slots_by_form, min_wordings=MIN_WORDINGS):
    """slots_by_form: {form: [required slot names]}. Returns a list of problems ([] = ok)."""
    bad = []
    for form, slots in slots_by_form.items():
        ws = pool.get("forms", {}).get(form)
        if not ws:
            bad.append("missing form %s" % form)
            continue
        if len(ws) < min_wordings:
            bad.append("form %s has %d wordings (< %d)" % (form, len(ws), min_wordings))
        ids = [w["id"] for w in ws]
        if len(set(ids)) != len(ids):
            bad.append("form %s has duplicate ids" % form)
        if len({w["text"] for w in ws}) != len(ws):
            bad.append("form %s has duplicate texts" % form)
        allowed = set(slots)
        for w in ws:
            miss = set(SLOT.findall(w["text"])) - allowed
            if miss:
                bad.append("form %s wording %s uses unknown slots %s" % (form, w["id"], sorted(miss)))
            need = allowed - set(SLOT.findall(w["text"]))
            if need:
                bad.append("form %s wording %s misses slots %s" % (form, w["id"], sorted(need)))
    return bad


def require_real(pool):
    if pool.get("test_only"):
        raise PoolError("a TEST-ONLY wording pool cannot be used to build rows")
    return pool


class Picker:
    """Least-used-first wording choice."""

    def __init__(self, pool, rng):
        self.pool, self.rng, self.use = pool, rng, {}

    def pick(self, form):
        ws = self.pool["forms"][form]
        use = self.use.setdefault(form, {w["id"]: 0 for w in ws})
        m = min(use.values())
        w = self.rng.choice([w for w in ws if use[w["id"]] == m])
        use[w["id"]] += 1
        return w

    def render(self, form, **slots):
        w = self.pick(form)
        return w["id"], w["text"].format(**slots)

    def max_share(self, form):
        use = self.use.get(form, {})
        n = sum(use.values())
        return (max(use.values()) / n) if n else 0.0


def make_test_pool(slots_by_form, n=MIN_WORDINGS):
    """TEST-ONLY placeholders (not wording): every text carries a visible tag so it can never pass for a real pool. Each text
    embeds every required slot as `{slot}` in a fixed order."""
    forms = {}
    for form, slots in slots_by_form.items():
        tail = " ".join("{%s}" % s for s in slots)
        forms[form] = [{"id": "t%03d" % k, "text": ("[TEST-ONLY %s #%d] %s" % (hashlib.sha256(form.encode()).hexdigest()[:4], k, tail)).rstrip()} for k in range(n)]
    return {"version": 1, "test_only": True, "forms": forms}


def texts_of(pool, form):
    return [w["text"] for w in pool.get("forms", {}).get(form, [])]


def frame_problems(pool, form, deny=(), require_all=(), deny_start=None):
    """Semantic guards for ONE question form (a frame that asks something other than the gold question, or the opposite of it, makes the label noise even
    though the frame passes every count / slot rule): `deny` regexes may match no text, `require_all` regexes must match every text, `deny_start` is a regex
    for the first words (e.g. a yes/no opener on a form whose options are not YES / NO). -> list of problem strings."""
    bad = []
    for t in texts_of(pool, form):
        for rx in deny:
            if re.search(rx, t, re.I):
                bad.append("%s: wording %r matches the denied pattern %r" % (form, t[:60], rx))
        for rx in require_all:
            if not re.search(rx, t, re.I):
                bad.append("%s: wording %r lacks %r" % (form, t[:60], rx))
        if deny_start and re.match(deny_start, t.strip(), re.I):
            bad.append("%s: wording %r opens as a yes/no question but the options are not YES / NO" % (form, t[:60]))
    return bad
