"""Token rule G6 / GV4: mean <= 800 per family, no row above 1,536, rows above 1,024 on <= 10%."""
from .util import approx_tokens

_counter = None


def set_counter(fn):
    global _counter
    _counter = fn


def count(text):
    return (_counter or approx_tokens)(text)


def token_gate(token_counts, mean_max=800, cap=1536, over_1024_max=0.10):
    n = len(token_counts)
    if n == 0:
        return {"pass": False, "reason": "no rows"}
    mean = sum(token_counts) / n
    over_cap = sum(1 for t in token_counts if t > cap)
    over_1k = sum(1 for t in token_counts if t > 1024) / n
    return {"mean": mean, "max": max(token_counts), "over_cap": over_cap, "share_over_1024": over_1k,
            "pass": bool(mean <= mean_max and over_cap == 0 and over_1k <= over_1024_max)}
