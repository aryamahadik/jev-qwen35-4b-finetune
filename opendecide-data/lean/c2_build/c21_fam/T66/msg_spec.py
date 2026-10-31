"""T66 MSG head (generated): change specs CH-1..CH-10 with exactly ONE substantive hunk plus 0-2 trivial hunks, unified diffs, behaviour probes, messages and the
swap (derangement within the group, diff-size neighbours).

"Substantive" is fixed by EXECUTION (G0-lite 2.3): each hunk is applied alone to the base and a program-made behaviour probe (3 identical runs through the
executor) must differ for the substantive hunk and be identical for every trivial hunk; a hunk that fails this is DROPPED from the spec. CH-4 (extract helper)
and CH-7 (remove dead branch) preserve behaviour, so the execution rule always drops them: they are registered but never realised (flagged in the README).
CH-6 is "make a parameter required (the default is REMOVED)": the diff drops `=<default>` from an existing parameter (fixed before any training row existed; it was
registered as "add parameter", which the rendered diff never showed). Messages come from the production pool (pools/msg_messages.json via msg_pool.py), never from
question frames.
Gold: YES = the diff with its own message; NO = the same diff with another change spec's message (derangement inside the group, token Jaccard < 0.5, >= 4
tokens, different (verb class, object)) or with the message of a TRIVIAL hunk of the same diff (CH-trivial, >= 25% of NO rows). Solver A = construction + probe.
"""
import copy
import difflib
import re

from LP_COMMON import sandbox_iface as S
from LP_COMMON import util
from LP_COMMON.ns import Names

from . import prog as P
from .merge import Pool, Reject

CH_IDS = tuple("CH-%d" % i for i in range(1, 11))
CH_REALISED = ("CH-1", "CH-2", "CH-3", "CH-5", "CH-6", "CH-8", "CH-9", "CH-10")
CH_NEVER = ("CH-4", "CH-7")                        # behaviour-preserving: dropped by the execution rule
TRIV_IDS = ("fmt", "comment", "doc")
NEUTRAL = ("kept for the next release", "reviewed with the data team", "see the runbook", "unchanged since the last release", "owner is the platform group")
VERB_CLASS = {"CH-1": "guard", "CH-2": "bound", "CH-3": "rename", "CH-5": "default", "CH-6": "required", "CH-8": "message", "CH-9": "log", "CH-10": "constant"}
# Two change kinds that are never put on the same base module: a CH-5 message on a CH-6 diff (same `def` line, same function and parameter) reads as a second description of the diff
# (Solver B "alternative reading", dev round 3); a CH-10 message on a CH-5 diff (both change a number: the same two numbers once re-bound, still a numeric edit verbatim) abstained on
# every one of its rows in both halves (dev round X1).
CONFUSABLE_PAIRS = (frozenset(("CH-5", "CH-6")), frozenset(("CH-5", "CH-10")))
# The function (base-module block) each realised kind changes. Kinds on the SAME function can be partners of the M-OVL hard stratum (Opus ruling Q8 R4): the partner's verbatim style-I
# message names identifiers (the function) that occur in this diff.
BLOCK_OF = {"CH-1": "p1", "CH-10": "p1", "CH-3": "p2", "CH-5": "p3", "CH-6": "p3", "CH-8": "p3", "CH-2": "b1", "CH-9": "b1"}
# Kind mix (an allowed lever, G0-lite 163): the p3 kinds (CH-5, CH-6, CH-8) are the ones Solver B abstains on most (6-18% per row in dev round X1), so they are drawn less often.
KIND_WEIGHT = {"CH-5": 0.7, "CH-6": 0.7, "CH-8": 0.7}
SAME_FN_WEIGHT = {("CH-1", "CH-10"): 0.35, ("CH-2", "CH-9"): 0.35, ("CH-5", "CH-8"): 0.25, ("CH-6", "CH-8"): 0.05}
ALWAYS_N = ("CH-8",)           # style N in a same-function pair (CH-8 style N: 0 abstains in 356 rows; style I: 7-8%)
SAME_FN_PAIRS = tuple(sorted(tuple(sorted((a_, b_))) for a_ in CH_REALISED for b_ in CH_REALISED if a_ < b_ and BLOCK_OF[a_] == BLOCK_OF[b_] and frozenset((a_, b_)) not in CONFUSABLE_PAIRS))
CH_NAMES = {"CH-1": "add an input guard (reject negative input)", "CH-2": "extend a loop bound by one", "CH-3": "rename a function", "CH-5": "change a parameter default",
            "CH-6": "make a parameter required (its default is removed)", "CH-8": "change an error message", "CH-9": "append a log entry to the result list",
            "CH-10": "change a numeric constant (scale factor)"}
def form_of(ch, style):
    return "T66-M-%s-%s" % (ch, style)


FORMS_MSG = ["T66-M-%s-%s" % (ch, st) for ch in CH_REALISED for st in ("I", "N")] + ["T66-M-TRIV-%s" % t for t in TRIV_IDS]
MSG_SLOTS = ["fn"]                                 # slots of a stand-in (test) pool; the production pool uses KIND_SLOTS
# Slots a message template of each kind may use (style N: only the NUMERIC_SLOTS among them). The generator fills EVERY slot of SLOT_NAMES on every spec: the kind's own slots from the facts of its change, the others
# with module-bound fillers (a swapped message keeps the neighbour's wording but is bound to THIS diff's names).
SLOT_NAMES = ("fn", "arg", "param", "new_fn", "tok", "word", "num_old", "num_new", "word_old", "word_new", "lv")
NUMERIC_SLOTS = ("num_old", "num_new")             # numbers are not identifiers: a style-N (identifier-free) message may carry them
KIND_SLOTS = {"CH-1": ("fn", "arg", "word"), "CH-2": ("fn", "arg", "lv"), "CH-3": ("fn", "new_fn"), "CH-5": ("fn", "arg", "param", "num_old", "num_new"),
              "CH-6": ("fn", "arg", "param", "num_old"), "CH-8": ("fn", "arg", "word_old", "word_new"), "CH-9": ("fn", "arg", "tok"), "CH-10": ("fn", "arg", "num_old", "num_new"),
              "fmt": ("fn",), "comment": ("fn",), "doc": ("fn",)}


def base_module(pool, rng):
    """P1 (scale, offset, cap) for CH-1 / CH-10, P2 for CH-3, P3 (guard + default bias) for CH-5 / CH-6 / CH-8, B1 (appends + loop) for CH-2 / CH-9, a table."""
    p1 = P.pipe(pool.fn(), pool.var(), pool.var(), [P.stage("scale", k=rng.randint(2, 6)), P.stage("offset", c=rng.randint(1, 9)), P.stage("cap", cap=rng.randint(150, 400))])
    p2 = P.pipe(pool.fn(), pool.var(), pool.var(), [P.stage("scale", k=rng.randint(2, 6)), P.stage("offset", c=rng.randint(1, 9))])
    p3 = P.pipe(pool.fn(), pool.var(), pool.var(), [P.stage("guard", msg=pool.word()), P.stage("scale", k=rng.randint(2, 6))], bias=pool.var())
    p3["bias_def"] = rng.randint(0, 3)
    b1 = P.build(pool.fn(), pool.var(), pool.var(), pool.var(), [P.stage("append", tok=pool.word()), P.stage("loop", k=rng.randint(2, 5))])
    return P.module(p1, p2, p3, b1), {"p1": p1["name"], "p2": p2["name"], "p3": p3["name"], "b1": b1["name"]}


def _blk(mod, name):
    return next(b for b in mod["blocks"] if b.get("name") == name)


def arg_of(mod, fn):
    """First parameter name of the function `fn` (a pipe's input or a build's count). Kinds whose hunk lines read another variable (CH-1, CH-8, CH-10) set `arg` themselves."""
    b = _blk(mod, fn)
    return b["x"] if b["t"] == "pipe" else b["n"]


def substantive(ch, mod, ids, pool, rng, facts=None):
    """-> (changed module, function name the hunk is about). `facts` (optional dict) receives the slot values of the change (the names / values the diff shows)."""
    f = facts if facts is not None else {}
    if ch == "CH-1":
        word = pool.word()
        f.update(word=word, arg=_blk(mod, ids["p1"])["v"])               # the variable the added guard tests (it is in the hunk lines)
        return P.insert_stage(mod, ids["p1"], 0, P.stage("guard", msg=word)), ids["p1"]
    if ch == "CH-2":
        b = _blk(mod, ids["b1"])
        f.update(arg=b["n"], lv=b["i"])                                  # the range argument and the loop variable of the changed `for` line
        return P.set_param(mod, ids["b1"], 1, plus=1), ids["b1"]
    if ch == "CH-3":
        new = pool.fn()
        f.update(new_fn=new)
        return P.rename_fn(mod, ids["p2"], new), ids["p2"]
    if ch == "CH-5":
        b3 = _blk(mod, ids["p3"])
        old = b3["bias_def"]
        new = old + rng.randint(1, 4)
        f.update(param=b3["bias"], num_old=old, num_new=new)
        return P.set_bias_default(mod, ids["p3"], new), ids["p3"]
    if ch == "CH-6":
        # make the parameter REQUIRED: its default is removed (`def f(x, b=2)` -> `def f(x, b)`); the old spec name "add parameter" did not match this diff
        m, b = P.edit(mod, ids["p3"])
        f.update(param=b["bias"], num_old=b["bias_def"])
        b["bias_def"] = None
        return m, ids["p3"]
    if ch == "CH-8":
        old, new = _blk(mod, ids["p3"])["stages"][0]["msg"], pool.word()
        f.update(word_old=old, word_new=new, arg=_blk(mod, ids["p3"])["v"])
        return P.set_param(mod, ids["p3"], 0, msg=new), ids["p3"]
    if ch == "CH-9":
        tok = pool.word()
        f.update(tok=tok)
        return P.insert_stage(mod, ids["b1"], 1, P.stage("append", tok=tok)), ids["b1"]
    if ch == "CH-10":
        old = _blk(mod, ids["p1"])["stages"][0]["k"]
        new = old + rng.randint(1, 3)
        f.update(num_old=old, num_new=new, arg=_blk(mod, ids["p1"])["v"])      # the variable the scaled line reads (it is in the hunk lines)
        return P.set_param(mod, ids["p1"], 0, k=new), ids["p1"]
    raise Reject("%s is behaviour-preserving (execution rule)" % ch)


def own_slots(ch, facts, fn, mod):
    """The slots of ONE change spec: exactly the slots its kind's templates use (KIND_SLOTS), from the facts of its own change. A message is never re-bound to another diff: a swapped
    NO message is the partner's true message verbatim (Opus ruling Q8 R1)."""
    s = dict(facts)
    s["fn"] = fn
    s.setdefault("arg", arg_of(mod, fn))
    return {k: s[k] for k in KIND_SLOTS[ch]}


def line_hunks(base_lines, new_lines):
    sm = difflib.SequenceMatcher(None, base_lines, new_lines, autojunk=False)
    return [(i1, i2, new_lines[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]


def apply_hunks(base_lines, hunks):
    out, pos = [], 0
    for i1, i2, new in sorted(hunks):
        out += base_lines[pos:i1] + list(new)
        pos = i2
    return out + base_lines[pos:]


def trivial_hunk(kind, base_lines, avoid, rng):
    """A behaviour-preserving text hunk away from the lines in `avoid` (indices). -> (i1, i2, new) or None."""
    cand = []
    if kind == "fmt":
        for i, ln in enumerate(base_lines):
            m = re.match(r"^(\s+)(\w+) = (\w+) ([*+]) (\d+)$", ln)
            if m and all(abs(i - a) > 2 for a in avoid):
                cand.append((i, i + 1, ["%s%s = %s%s%s" % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))]))
    elif kind == "comment":
        for i, ln in enumerate(base_lines):
            if ln.startswith("def ") and all(abs(i - a) > 2 for a in avoid):
                cand.append((i, i, ["# " + rng.choice(NEUTRAL)]))
    else:
        for i, ln in enumerate(base_lines):
            if ln.startswith("def ") and ln.endswith(":") and i + 1 < len(base_lines) and not base_lines[i + 1].strip().startswith('"""') \
                    and all(abs(i - a) > 3 for a in avoid) and "guard" not in "".join(base_lines[i:i + 3]):
                cand.append((i + 1, i + 1, ['    """%s"""' % rng.choice(NEUTRAL)]))
    return rng.choice(cand) if cand else None


def enclosing_fn(base_lines, hunk):
    """Name of the function a trivial hunk (i1, i2, new) sits in: the def on its first line (comment hunk) or the nearest def above it (docstring, formatting)."""
    for i in range(min(hunk[0], len(base_lines) - 1), -1, -1):
        m = re.match(r"^def (\w+)\(", base_lines[i])
        if m:
            return m.group(1)
    return None


def unified(stem, base_lines, new_lines, context=3):
    out = ["--- a/%s.py" % stem, "+++ b/%s.py" % stem]
    for grp in difflib.SequenceMatcher(None, base_lines, new_lines, autojunk=False).get_grouped_opcodes(context):
        i1, i2, j1, j2 = grp[0][1], grp[-1][2], grp[0][3], grp[-1][4]
        out.append("@@ -%d,%d +%d,%d @@" % (i1 + 1, i2 - i1, j1 + 1, j2 - j1))
        for tag, a1, a2, b1, b2 in grp:
            if tag == "equal":
                out += [" " + x for x in base_lines[a1:a2]]
            else:
                out += ["-" + x for x in base_lines[a1:a2]] + ["+" + x for x in new_lines[b1:b2]]
    return "\n".join(out) + "\n"


def probe_calls(mod):
    calls = []
    for b in mod["blocks"]:
        if b["t"] == "pipe":
            for x in (-3, -1, 0, 1, 2, 5, 9, 30, 80, 400):
                calls.append((b["name"], [x], {}))
                if b.get("bias"):
                    calls.append((b["name"], [x, 3], {}))
        elif b["t"] == "build":
            for n in (0, 1, 2, 5):
                calls.append((b["name"], [n], {}))
        elif b["t"] == "table":
            for k, _v in b["rows"]:
                calls.append((b["fn"], [k], {}))
        elif b["t"] == "wrap":
            for x in (0, 3):
                calls.append((b["name"], [x], {}))
    return calls


def run_probe(executor, rid, stem, text, calls):
    res = executor.run([S.calls_request(rid, {stem + ".py": text}, stem, calls)])[0]
    return S.parse_marker(res["stdout"]), S.witness_ok(res)


def jaccard(a, b):
    ta, tb = set(a.lower().split()), set(b.lower().split())
    return len(ta & tb) / float(len(ta | tb)) if ta | tb else 1.0


def build_group(ctx, g, cell):
    """cell: {chs: [change kinds], trivial: [n trivial hunks per spec], styles: [I|N per spec] (optional)} -> specs (a YES and a NO row for every change spec)."""
    rng = ctx.rng("msg", g["seed"])
    names = Names("T66", "%s/%s" % (ctx.seed, g["seed"]), deny_check=ctx.deny_check)
    pool = Pool(names, rng)
    mod, ids = base_module(pool, rng)
    stem = pool.stem()
    base_text = P.render(mod)
    base_lines = base_text.rstrip("\n").split("\n")
    calls = probe_calls(mod)
    base_obs, ok0 = run_probe(ctx.executor, "%s:base" % g["gid"], stem, base_text, calls)
    if not ok0:
        raise Reject("base probe not deterministic")
    chs = list(cell["chs"])
    specs = []
    for j, ch in enumerate(chs):
        facts = {}
        new_mod, fn = substantive(ch, mod, ids, pool, rng, facts)
        sub_hunks = line_hunks(base_lines, P.render(new_mod).rstrip("\n").split("\n"))
        if len(sub_hunks) < 1 or len(sub_hunks) > 3:
            raise Reject("%s produced %d line hunks" % (ch, len(sub_hunks)))
        obs, ok = run_probe(ctx.executor, "%s:%s:sub" % (g["gid"], ch), stem, P.render(new_mod), calls)
        if not ok or obs == base_obs:
            raise Reject("%s does not change behaviour (execution rule)" % ch)
        avoid = [x for h in sub_hunks for x in range(h[0], h[1] + 1)]
        trivs = []
        for t in rng.sample(TRIV_IDS, cell["trivial"][j % len(cell["trivial"])]):
            h = trivial_hunk(t, base_lines, avoid, rng)
            if h is None:
                continue
            tl = apply_hunks(base_lines, [h])
            tobs, tok = run_probe(ctx.executor, "%s:%s:triv:%s" % (g["gid"], ch, t), stem, "\n".join(tl) + "\n", calls)
            if not tok or tobs != base_obs:
                continue                                        # a trivial hunk that fails the rule is dropped from the spec
            trivs.append((t, h, enclosing_fn(base_lines, h)))
            avoid += list(range(h[0], h[1] + 1))
        all_h = list(sub_hunks) + [h for _t, h, _f in trivs]
        new_lines = apply_hunks(base_lines, all_h)
        full_obs, ok = run_probe(ctx.executor, "%s:%s:full" % (g["gid"], ch), stem, "\n".join(new_lines) + "\n", calls)
        if not ok or full_obs != obs:
            raise Reject("trivial hunks changed the behaviour")
        style = rng.choice(("I", "N"))
        if cell.get("styles"):
            style = cell["styles"][j % len(cell["styles"])]                 # planned (the M-OVL hard stratum fixes the styles of a same-function pair)
        slots = own_slots(ch, facts, fn, mod)
        specs.append({"ch": ch, "fn": fn, "stem": stem, "diff": unified(stem, base_lines, new_lines), "diff_size": sum(1 for ln in unified(stem, base_lines, new_lines).split("\n") if ln[:1] in "+-" and ln[:3] not in ("+++", "---")),
                      "trivials": [t for t, _h, _f in trivs], "triv_fns": [f for _t, _h, f in trivs], "slots": slots, "style": style, "probe": {"base": util.sha_obj(base_obs), "sub": util.sha_obj(obs), "sub_differs": True, "trivials_identical": True, "runs": S.WITNESS_RUNS},
                      "verb": VERB_CLASS[ch]})
    return specs
