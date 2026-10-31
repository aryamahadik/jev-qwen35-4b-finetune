"""T66 / T65 program model: small application-style Python modules as STRUCTURES (blocks of stages) with two views of the same thing:

  render(module) -> the source text a row shows (deterministic style, 4-space indent);
  ref(module, fn, *args) -> the REFERENCE SEMANTICS computed on the structure with plain host arithmetic (no exec, no eval, no interpretation of text).

The reference semantics is the generator's own claim about what the rendered text means; the executor (PyEval in the dry run, od-sbx1 in production) must
agree with it on every witnessed call: a disagreement is a renderer bug and drops the row. Edits (change a stage parameter, add / delete / swap stages,
rename a function, change a signature, add a table row) are functions on the structure, so base / ours / theirs / reference-merge modules are built, not
guessed. Every identifier is supplied by the caller from the seeded namespace.
Block types: pipe (numeric stages on one value), build (an ordered list built by appends and a loop), table (a dict constant + lookup), wrap (calls a
function and adds a constant), call2 (calls a function with extra arguments). Module = {"blocks": [...]} .
"""
import copy

# ---- stages ---------------------------------------------------------------------------------------------------------------------------
PIPE_OPS = ("scale", "offset", "affine", "cap", "floor", "guard", "mod", "round")


def stage(op, **p):
    return dict(op=op, **p)


def _stage_lines(st, v):
    op = st["op"]
    if op == "scale":
        return ["%s = %s * %d" % (v, v, st["k"])]
    if op == "offset":
        return ["%s = %s + %d" % (v, v, st["c"])]
    if op == "affine":
        return ["%s = %s * %d + %d" % (v, v, st["k"], st["c"])]
    if op == "cap":
        return ["if %s > %d:" % (v, st["cap"]), "    %s = %d" % (v, st["cap"])]
    if op == "floor":
        return ["if %s < %d:" % (v, st["lo"]), "    %s = %d" % (v, st["lo"])]
    if op == "guard":
        return ["if %s < 0:" % v, '    raise ValueError("%s")' % st["msg"]]
    if op == "mod":
        return ["%s = %s %% %d" % (v, v, st["m"])]
    if op == "round":
        return ["%s = (%s // %d) * %d" % (v, v, st["s"], st["s"])]
    raise ValueError(op)


def _stage_ref(st, v):
    op = st["op"]
    if op == "scale":
        return v * st["k"]
    if op == "offset":
        return v + st["c"]
    if op == "affine":
        return v * st["k"] + st["c"]
    if op == "cap":
        return st["cap"] if v > st["cap"] else v
    if op == "floor":
        return st["lo"] if v < st["lo"] else v
    if op == "guard":
        if v < 0:
            raise ValueError(st["msg"])
        return v
    if op == "mod":
        return v % st["m"]
    if op == "round":
        return (v // st["s"]) * st["s"]
    raise ValueError(op)


def _build_lines(st, out, i, n):
    if st["op"] == "append":
        return ['%s.append("%s")' % (out, st["tok"])]
    if st["op"] == "loop":
        rng_ = n if not st.get("plus") else "%s + %d" % (n, st["plus"])
        return ["for %s in range(%s):" % (i, rng_), "    %s.append(%s * %d)" % (out, i, st["k"])]
    raise ValueError(st["op"])


# ---- blocks ---------------------------------------------------------------------------------------------------------------------------
def pipe(name, x, v, stages, doc=None, bias=None):
    return {"t": "pipe", "name": name, "x": x, "v": v, "stages": list(stages), "doc": doc, "bias": bias}


def build(name, n, out, i, stages):
    return {"t": "build", "name": name, "n": n, "out": out, "i": i, "stages": list(stages)}


def table(tab, fn, key, rows):
    return {"t": "table", "tab": tab, "fn": fn, "key": key, "rows": list(rows)}


def wrap(name, x, call, add, extra=()):
    return {"t": "wrap", "name": name, "x": x, "call": call, "add": add, "extra": list(extra)}


def module(*blocks):
    return {"blocks": list(blocks)}


def block_lines(b):
    if b["t"] == "pipe":
        sig = b["x"] + ((", " + b["bias"] + ("=%d" % b["bias_def"] if b.get("bias_def") is not None else "")) if b.get("bias") else "")
        lines = ["def %s(%s):" % (b["name"], sig)]
        if b.get("doc"):
            lines.append('    """%s"""' % b["doc"])
        lines.append("    %s = %s" % (b["v"], b["x"] + (" + " + b["bias"] if b.get("bias") else "")))
        for st in b["stages"]:
            lines += ["    " + ln for ln in _stage_lines(st, b["v"])]
        lines.append("    return %s" % b["v"])
        return lines
    if b["t"] == "build":
        lines = ["def %s(%s):" % (b["name"], b["n"]), "    %s = []" % b["out"]]
        for st in b["stages"]:
            lines += ["    " + ln for ln in _build_lines(st, b["out"], b["i"], b["n"])]
        lines.append("    return %s" % b["out"])
        return lines
    if b["t"] == "table":
        lines = ["%s = {" % b["tab"]]
        for k, v in b["rows"]:
            lines.append('    "%s": %d,' % (k, v))
        lines.append("}")
        lines += ["", "", "def %s(%s):" % (b["fn"], b["key"]), "    return %s[%s]" % (b["tab"], b["key"])]
        return lines
    if b["t"] == "wrap":
        args = ", ".join([b["x"]] + [str(e) for e in b["extra"]])
        return ["def %s(%s):" % (b["name"], b["x"]), "    return %s(%s) + %d" % (b["call"], args, b["add"])]
    raise ValueError(b["t"])


def render(mod):
    out = []
    for i, b in enumerate(mod["blocks"]):
        if i:
            out += ["", ""]
        out += block_lines(b)
    return "\n".join(out) + "\n"


def lines(mod):
    return render(mod).rstrip("\n").split("\n")


# ---- reference semantics ---------------------------------------------------------------------------------------------------------------
def _find(mod, name):
    for b in mod["blocks"]:
        if b["t"] in ("pipe", "build", "wrap") and b["name"] == name:
            return b
        if b["t"] == "table" and b["fn"] == name:
            return b
    return None


def ref(mod, fn, *args):
    """Reference value of fn(*args), or raises the exception the rendered text would raise (ValueError / KeyError / TypeError / NameError)."""
    b = _find(mod, fn)
    if b is None:
        raise NameError(fn)
    if b["t"] == "pipe":
        if b.get("bias") and b.get("bias_def") is not None and len(args) == 1:
            args = (args[0], b["bias_def"])
        if len(args) != (2 if b.get("bias") else 1):
            raise TypeError("arity")
        v = args[0] + (args[1] if b.get("bias") else 0)
        for st in b["stages"]:
            v = _stage_ref(st, v)
        return v
    if b["t"] == "build":
        if len(args) != 1:
            raise TypeError("arity")
        out = []
        for st in b["stages"]:
            if st["op"] == "append":
                out.append(st["tok"])
            else:
                out.extend(i * st["k"] for i in range(args[0] + st.get("plus", 0)))
        return out
    if b["t"] == "table":
        if len(args) != 1:
            raise TypeError("arity")
        return dict(b["rows"])[args[0]]
    if b["t"] == "wrap":
        if len(args) != 1:
            raise TypeError("arity")
        return ref(mod, b["call"], *([args[0]] + list(b["extra"]))) + b["add"]
    raise ValueError(b["t"])


def observe(mod, fn, args):
    try:
        return ("ok", ref(mod, fn, *args))
    except (ValueError, KeyError, TypeError, NameError) as e:
        return ("exc", type(e).__name__)


# ---- edits (all return a NEW module) ---------------------------------------------------------------------------------------------------
def edit(mod, fn):
    m = copy.deepcopy(mod)
    for b in m["blocks"]:
        if b["t"] in ("pipe", "build", "wrap") and b["name"] == fn:
            return m, b
        if b["t"] == "table" and b["fn"] == fn:
            return m, b
    raise KeyError(fn)


def set_param(mod, fn, idx, **p):
    m, b = edit(mod, fn)
    b["stages"][idx].update(p)
    return m


def insert_stage(mod, fn, idx, st):
    m, b = edit(mod, fn)
    b["stages"].insert(idx, st)
    return m


def delete_stage(mod, fn, idx):
    m, b = edit(mod, fn)
    del b["stages"][idx]
    return m


def swap_stages(mod, fn, i, j):
    m, b = edit(mod, fn)
    b["stages"][i], b["stages"][j] = b["stages"][j], b["stages"][i]
    return m


def rename_fn(mod, old, new):
    m = copy.deepcopy(mod)
    for b in m["blocks"]:
        if b["t"] in ("pipe", "build", "wrap") and b["name"] == old:
            b["name"] = new
        if b["t"] == "table" and b["fn"] == old:
            b["fn"] = new
        if b["t"] == "wrap" and b["call"] == old:
            b["call"] = new
    return m


def rename_var(mod, fn, new):
    m, b = edit(mod, fn)
    key = "v" if b["t"] == "pipe" else "out"
    b[key] = new
    return m


def add_block(mod, blk, idx=None):
    m = copy.deepcopy(mod)
    if idx is None:
        m["blocks"].append(blk)
    else:
        m["blocks"].insert(idx, blk)
    return m


def add_row(mod, fn, key, val, pos=None):
    m, b = edit(mod, fn)
    if pos is None:
        b["rows"].append((key, val))
    else:
        b["rows"].insert(pos, (key, val))
    return m


def add_bias(mod, fn, bias):
    m, b = edit(mod, fn)
    b["bias"] = bias
    return m


def set_wrap(mod, fn, **kw):
    m, b = edit(mod, fn)
    b.update(kw)
    return m


def set_bias_default(mod, fn, d):
    m, b = edit(mod, fn)
    b["bias_def"] = d
    return m
