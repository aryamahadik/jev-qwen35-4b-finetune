"""Planning helpers: quota cells oversampled by 15% at generation (G0-lites section 4: quotas are counted AFTER drops), the ladder level
function of the G0-lites (L1 none; L2 one LOW; L3 one HIGH or two LOW; L4 two or more HIGH), and the base `Ctx`."""
import math

from . import util

OVERSAMPLE = 1.15
LEVELS = ("L1", "L2", "L3", "L4")


def oversampled(n):
    return int(math.ceil(n * OVERSAMPLE - 1e-9))


def ladder_level(n_low, n_high):
    if n_high >= 2:
        return "L4"
    if n_high == 1 or n_low >= 2:
        return "L3"
    if n_low == 1:
        return "L2"
    return "L1"


def level_cycle(n, rng, weights=(0.20, 0.30, 0.30, 0.20)):
    """n level labels, exactly the target composition up to rounding, shuffled."""
    alloc = util.largest_remainder(n, dict(zip(LEVELS, weights)))
    out = [lv for lv in LEVELS for _ in range(alloc[lv])]
    rng.shuffle(out)
    return out


class Ctx(object):
    """Generation context: seed, stand-in flag, the wording picker. Families subclass or wrap it."""

    def __init__(self, seed, standin=False, pool_path=None, pool=None, picker=None, deny_check=None, **kw):
        from . import wording
        self.seed, self.standin, self.deny_check = seed, standin, deny_check
        self.pool_path = pool_path
        self.pool = pool
        if pool is None and pool_path:
            self.pool = wording.require_real(wording.load(pool_path)) if not standin else wording.load(pool_path)
        self.picker = picker
        self.extra = kw

    def rng(self, *parts):
        return util.rng_for(self.seed, *parts)
