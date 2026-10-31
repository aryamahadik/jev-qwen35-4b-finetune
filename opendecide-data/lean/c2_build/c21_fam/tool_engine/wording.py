"""Wording pools: interface, slot round trip and hash export. Claude-authored SEED templates only live in the
family modules; the >= 50 wordings per question form come from the Haiku reword pass (reword-only, slot round trip,
drop-only on a miss). Templates use {slot} fields; slot values are recorded per row so the round trip is checkable."""
import re

from . import util

_SLOT = re.compile(r"\{([a-z_][a-z0-9_]*)\}")
_NUM = re.compile(r"\d+(?:\.\d+)?")
_NEG = re.compile(r"\b(?:not|no|never|none|without|neither|nor|cannot)\b|n't", re.I)


class WordingPool:
    """Wording pools by form. With `balanced=True` (the generators' setting) a pick that carries a `key` is drawn from a shuffled
    CYCLE over the form's wordings (cached per (form, key), so a matched twin asking again gets the same wording): every wording of a
    form is then used equally often (+-1), instead of the +-3 sigma spread of independent random picks that pushes the busiest
    wording of a heavily used form (an option text shown in 80% of the rows) over the 2%-of-the-family bar."""

    def __init__(self, pools=None, balanced=False):
        self.pools = {k: list(v) for k, v in (pools or {}).items()}
        self.balanced = balanced
        self._cyc = {}
        self._cache = {}

    def add(self, form_id, templates):
        self.pools.setdefault(form_id, [])
        for t in templates:
            if t not in self.pools[form_id]:
                self.pools[form_id].append(t)

    def forms(self):
        return sorted(self.pools)

    def count(self, form_id):
        return len(self.pools.get(form_id, []))

    def pick(self, form_id, rng, fallback=None, key=None):
        """Returns (form id, index, template). Falls back to `fallback` form (e.g. the sub-block level) when the form has none."""
        for fid in (form_id, fallback):
            if fid and self.pools.get(fid):
                pool = self.pools[fid]
                if self.balanced and key is not None:
                    ck = (fid, key)
                    if ck not in self._cache:
                        st = self._cyc.setdefault(fid, [[], 0])
                        if st[1] >= len(st[0]):
                            perm = list(range(len(pool)))
                            rng.shuffle(perm)
                            st[0], st[1] = perm, 0
                        self._cache[ck] = st[0][st[1]]
                        st[1] += 1
                    i = self._cache[ck]
                else:
                    i = rng.randrange(len(pool))
                return fid, i, pool[i]
        raise KeyError("no wording for form %r (fallback %r)" % (form_id, fallback))

    @classmethod
    def from_json(cls, path):
        """Load an expanded pool (pools/wording_pool_v1.json: {form id: [templates]}) written by the family's build_pools.py."""
        import json
        with open(path, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    def export_sha(self):
        """Hash of the whole pool (re-export at EVERY template change, plan v3.1)."""
        return util.sha256_text(util.canon_json({k: self.pools[k] for k in sorted(self.pools)}))


def fill(template, slots):
    """Strict fill: every {slot} must be given, and no extra literal braces are allowed."""
    names = _SLOT.findall(template)
    missing = [n for n in names if n not in slots]
    if missing:
        raise KeyError("template slots without values: %s" % missing)
    return _SLOT.sub(lambda m: str(slots[m.group(1)]), template)


def template_slots(template):
    return set(_SLOT.findall(template))


def reword_ok(original, reworded):
    """Haiku reword slot round trip: same {slot} set, same numbers (multiset), same count of negation words."""
    if template_slots(original) != template_slots(reworded):
        return False
    if sorted(_NUM.findall(original)) != sorted(_NUM.findall(reworded)):
        return False
    if len(_NEG.findall(original)) != len(_NEG.findall(reworded)):
        return False
    return True


def slots_survive(slots, text):
    """Rendered-text round trip: every recorded slot value appears verbatim. Returns the list of lost slot names."""
    return [k for k, v in slots.items() if str(v) not in text]
