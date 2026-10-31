"""T63 LIC format draw (K10-F, Opus ruling Q7b, before the pilot). Every format choice of a LIC row is a pure function of (seed, row index): card layout, field order, wording
id, template id and option order. `draw` takes NO label, no licence cell and no row: only the run seed, the row's index in the LIC block, the number of wordings in the pool and
the (fixed) option vocabulary. So the format is independent of the label by construction, and any row's format replays exactly from the seed and index recorded on it
(`gates.k10_f_construction`). `static_problems()` is the static check that the draw reads no label or cell input; it runs with the gate at every code sha."""
import ast
import hashlib
import inspect
import random
import sys

from . import config as C

FORMAT_FUNCTIONS = ("draw", "_rng")
DRAW_PARAMS = ("seed", "index", "n_wordings", "vocab")
FORBIDDEN_NAMES = frozenset(("label", "labels", "gold", "spec", "cell", "dep", "project", "use", "dist", "row", "rec", "options", "text", "table"))


def _rng(*parts):
    return random.Random(int.from_bytes(hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).digest()[:16], "big"))


def draw(seed, index, n_wordings, vocab):
    """-> the format choices of LIC row number `index` of the run `seed`. The wording is least-used-first by construction (round r = index div n_wordings is a seeded permutation
    of the pool, each wording once per round), so the K14 cap ceil(n / W) holds; the option order is a seeded permutation of the fixed vocabulary."""
    perm = list(range(n_wordings))
    _rng(seed, "wording-round", index // n_wordings).shuffle(perm)
    order = list(vocab)
    _rng(seed, "option-order", index).shuffle(order)
    return {"word_index": perm[index % n_wordings], "option_order": order, "template_id": C.LIC_TEMPLATE_ID, "card_layout": C.LIC_CARD_LAYOUT,
            "field_order": C.LIC_FIELD_ORDER}


def static_problems():
    """Static check: `draw` has exactly the parameters (seed, index, n_wordings, vocab) and neither it nor `_rng` mentions a label, licence cell, spec, row or table."""
    tree = ast.parse(inspect.getsource(sys.modules[__name__]))
    bad = []
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in FORMAT_FUNCTIONS]:
        if fn.name == "draw" and tuple(a.arg for a in fn.args.args) != DRAW_PARAMS:
            bad.append("draw has parameters %r" % (tuple(a.arg for a in fn.args.args),))
        for node in ast.walk(fn):
            names = {getattr(node, "id", None), getattr(node, "arg", None), getattr(node, "attr", None)} - {None}
            for nm in names & FORBIDDEN_NAMES:
                bad.append("%s reads %r" % (fn.name, nm))
    return bad
