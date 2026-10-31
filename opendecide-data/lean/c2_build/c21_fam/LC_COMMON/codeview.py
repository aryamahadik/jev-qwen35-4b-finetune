"""What the model SEES of a module: pruned sub-modules, call text, option text, similarity features.

Everything here is text assembled from the IR; no code is executed.
"""
import difflib
import re

from . import ir as I
from . import render as R
from . import render_base as B
from .render_base import EXT


# ----------------------------------------------------------------------------------------------- pruning
def prune_module(mod, keep):
    """Smallest module that still contains functions `keep` (a set of names) and everything they use."""
    fns = I.functions(mod)
    need, stack = set(), list(keep)
    while stack:
        n = stack.pop()
        if n in need:
            continue
        need.add(n)
        for _, x in I.walk(fns[n]["body"]):
            if x[0] in ("fcall", "mcall"):
                stack.append(x[1])
    new = I.clone(mod)
    new["funcs"] = [f for f in new["funcs"] if f["name"] in need]
    used_consts = {x[1] for f in new["funcs"] for _, x in I.walk(f["body"]) if x[0] == "const"}
    new["consts"] = [c for c in new["consts"] if c["name"] in used_consts]
    if new["cls"] and not any(f["scope"] == "method" for f in new["funcs"]):
        new["cls"] = None
    files_used = {f["file"] for f in new["funcs"]} | {c.get("file", 0) for c in new["consts"]}
    if new["cls"]:
        files_used.add(new["cls"]["file"])
    errs = {x[1] for f in new["funcs"] for _, x in I.walk(f["body"]) if x[0] == "raise"}
    new["errors"] = {e: v for e, v in new["errors"].items() if e in errs}
    # custom error classes live in the dependency-first file; keep that file when any custom class is used
    keep_files = sorted(files_used)
    if not keep_files:
        keep_files = [0]
    remap = {old: k for k, old in enumerate(keep_files)}
    new["files"] = [mod["files"][k] for k in keep_files]
    for f in new["funcs"]:
        f["file"] = remap[f["file"]]
    for c in new["consts"]:
        c["file"] = remap[c.get("file", 0)]
    if new["cls"]:
        new["cls"]["file"] = remap[new["cls"]["file"]]
    new["public"] = [f["name"] for f in new["funcs"]]
    try:
        B.dep_order(new)
    except ValueError:
        pass
    return new


# ----------------------------------------------------------------------------------------------- source blocks
def src_blocks(mod, lang):
    """SRC_FILE carriers: [{"path", "lang", "text"}] for the module's files in dependency order (dependencies first)."""
    files = R.render_module(mod, lang)
    order = B.dep_order(mod)
    out = []
    for k in order:
        path = mod["files"][k] + EXT[lang]
        if path in files:
            out.append({"path": path, "lang": lang, "text": files[path]})
    if lang == "go":
        out.append({"path": "go.mod", "lang": "go", "text": files["go.mod"]})
    return out


def src_text(blocks):
    return "\n".join("### %s (%s)\n%s" % (b["path"], b["lang"], b["text"]) for b in blocks)


# ----------------------------------------------------------------------------------------------- values and options
def value_text(v, ty, lang):
    if lang == "bash":
        if isinstance(v, bool):
            return "1" if v else "0"
        return str(v)
    return R.value_lit(v, ty, lang)


def exc_text(mod, err, lang):
    if err == "IMP_INDEX":
        return "raises IndexError" if lang == "python" else "fails with an index error"
    info = mod["errors"][err]
    if lang == "python":
        return "raises %s" % info["python"]
    if lang in ("javascript", "typescript"):
        return "throws %s" % info["javascript"]
    if lang == "go":
        return "panics with %s" % info["go"]
    return "exits with status %d" % info["bash"]


def exc_name(mod, err, lang):
    """The observable exception token (matches the driver's {"exc": name})."""
    if err == "IMP_INDEX":
        return "IndexError"
    info = mod["errors"][err]
    if lang == "bash":
        return "exit:%d" % info["bash"]
    return info["python"] if lang == "python" else info["javascript"] if lang in ("javascript", "typescript") else info["go"]


def option_text(obs, ty, mod, lang):
    """Human text of one observable ({"ok": v} | {"exc": name})."""
    if "ok" in obs:
        return value_text(obs["ok"], ty, lang)
    name = obs["exc"]
    if lang == "python":
        return "raises %s" % name
    if lang in ("javascript", "typescript"):
        return "throws %s" % name
    if lang == "go":
        return "panics with %s" % name
    return "exits with status %s" % name.split(":")[-1]


def call_text(mod, lang, calls, ret_type):
    """CALL_SPEC: setup calls then the asked (last) call, in the language's own syntax."""
    fns = I.functions(mod)
    uses_obj = mod["cls"] is not None and any(fns[c["fn"]]["scope"] == "method" for c in calls)
    lines = []

    def args_of(c):
        f = fns[c["fn"]]
        if lang == "bash":
            return " ".join(("'%s'" % a) if p[1] == I.STR else str(1 if a is True else 0 if a is False else a)
                            for a, p in zip(c["args"], f["params"]))
        return ", ".join(R.value_lit(a, p[1], lang) for a, p in zip(c["args"], f["params"]))

    def pre(c):
        return "obj." if fns[c["fn"]]["scope"] == "method" else ""

    if lang == "python":
        if uses_obj:
            lines.append("obj = %s()" % mod["cls"]["name"])
        for c in calls[:-1]:
            lines.append("%s%s(%s)" % (pre(c), c["fn"], args_of(c)))
        c = calls[-1]
        lines.append("result = %s%s(%s)" % (pre(c), c["fn"], args_of(c)))
    elif lang in ("javascript", "typescript"):
        if uses_obj:
            lines.append("const obj = new %s();" % mod["cls"]["name"])
        for c in calls[:-1]:
            lines.append("%s%s(%s);" % (pre(c), c["fn"], args_of(c)))
        c = calls[-1]
        lines.append("const result = %s%s(%s);" % (pre(c), c["fn"], args_of(c)))
    elif lang == "go":
        if uses_obj:
            lines.append("obj := mk%s()" % mod["cls"]["name"])
        for c in calls[:-1]:
            lines.append("%s%s(%s)" % (pre(c), c["fn"], args_of(c)))
        c = calls[-1]
        lines.append("result := %s%s(%s)" % (pre(c), c["fn"], args_of(c)))
    else:
        for c in calls[:-1]:
            lines.append("%s %s" % (c["fn"], args_of(c)) if c["args"] else c["fn"])
        c = calls[-1]
        lines.append(("%s %s" % (c["fn"], args_of(c))) if c["args"] else c["fn"])
        lines.append('echo "$RET"')
    return "\n".join(lines)


# ----------------------------------------------------------------------------------------------- similarity
_TOK = re.compile(r"[A-Za-z_][A-Za-z_0-9]*|\d+|\S")


def tokens_of(text):
    return _TOK.findall(text)


def token_jaccard(a, b):
    sa, sb = set(tokens_of(a)), set(tokens_of(b))
    return len(sa & sb) / max(1, len(sa | sb))


def edit_ratio(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def changed_lines(a, b):
    la, lb = a.splitlines(), b.splitlines()
    return sum(1 for d in difflib.ndiff(la, lb) if d[:2] in ("+ ", "- "))
