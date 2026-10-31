"""T55 tiny dry run: builds a handful of examples IN MEMORY for unit tests and eyeballing. It never writes a row to disk,
never calls a model, never executes generated code. Production row jobs use the real namespace kinds (standin=False) and are
refused until namespace.py has the noun kinds (see tool_engine/names.py)."""
import collections
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import t55_generator as gen  # noqa: E402
from tool_engine import util  # noqa: E402

MAX_DRY = 200


def run(n=20, seed="t55-dry"):
    """Returns (records, summary). n is capped: this is a dry run, not a pilot."""
    if n > MAX_DRY:
        raise ValueError("the dry run builds at most %d examples; row jobs go through the row-start guard" % MAX_DRY)
    recs = gen.generate_in_memory(total=n, seed=seed, standin=True)
    summary = dict(n=len(recs), by_sub_block=dict(collections.Counter(r["sub_block"] for r in recs)),
                   labels=dict(collections.Counter(r["gold"] for r in recs)),
                   tokens_mean=round(sum(util.approx_tokens(r["rendered"]["text"]) for r in recs) / max(1, len(recs)), 1),
                   standin_names=True, written_to_disk=False)
    return recs, summary


if __name__ == "__main__":
    _recs, _sum = run(int(sys.argv[1]) if len(sys.argv) > 1 else 20)
    print(json.dumps(_sum, sort_keys=True))
