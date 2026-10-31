"""Renderer: structured Script -> command string through semantics-preserving operators (G0-lite T50 section 3).

Ten operator families (8 trained + 2 reserved for the dev-only held-out-operator slice):
  trained   : wrapper_insert, flag_reorder, git_C, quote_sub, abs_path, sh_c, var_held, b64_pipe
  held-out  : brace, ifs_split   (dev specs only; never rendered for a train spec)
b64_pipe renders `echo <b64> | base64 -d | sh` of a VISIBLE literal that decodes to a REGISTERED payload (K18).

Nothing here runs a command. Names for shell variables come from the namespace (slot ns.variable). Every
rendering reports the programs it introduced so the names guard can check them against the family's list.
"""
import base64
import re

from .shellmodel import (ABS_PATHS, Cmd, Glob, HARMLESS_ENV, Redir, Script, RawScript, TildeExpand, quote_word)

TRAINED_OPERATORS = ("wrapper_insert", "flag_reorder", "git_C", "quote_sub", "abs_path", "sh_c", "var_held",
                     "b64_pipe")
HELDOUT_OPERATORS = ("brace", "ifs_split")
ALL_OPERATORS = TRAINED_OPERATORS + HELDOUT_OPERATORS
OPERATOR_PROGRAMS = {            # programs an operator introduces (names guard)
    "wrapper_insert": {"timeout", "nohup", "command", "env"},
    "sh_c": {"sh", "bash"},
    "b64_pipe": {"echo", "base64", "sh", "bash"},
}
IFS_CHARS = (",", ":", "@")


def _arg_word(a):
    if isinstance(a, (Glob, TildeExpand)):
        return str(a)
    return quote_word(a)


def _redir_text(r):
    if r.op in ("2>&", "1>&"):
        return r.op + r.target
    return r.op + " " + (quote_word(r.target) if r.target else "")


class RItem:
    """Mutable per-command render state."""

    def __init__(self, cmd, sep):
        self.cmd = cmd
        self.sep = sep
        self.assigns = [f"{k}={quote_word(v)}" for k, v in cmd.env]          # semantic env
        self.wrappers = []                                                    # operator wrapper word lists
        self.prog = cmd.program
        self.prog_word = cmd.program
        self.glob_units = [list(u) for u in cmd.global_flags]
        self.sub_words = cmd.sub.split(" ") if cmd.sub else []
        self.flag_units = [list(u) for u in cmd.flags]
        self.args = list(cmd.args)
        self.redirs = list(cmd.redirs)
        self.sub_quoted = False
        self.var_args = {}             # arg index -> var name
        self.prog_var = None
        self.brace_args = None         # replacement arg words
        self.split_var = None          # (var, word) : whole flags+args held in one IFS-split var

    def sql_text(self):
        return self.cmd.sql.text() if self.cmd.sql is not None else None

    def words(self):
        w = list(self.assigns)
        for wr in self.wrappers:
            w.extend(wr)
        if self.cmd.sudo:
            w.append("sudo")
        w.append(self.prog_var and "$" + self.prog_var or self.prog_word)
        for u in self.glob_units:
            w.extend(quote_word(x) for x in u)
        for i, sw in enumerate(self.sub_words):
            w.append(quote_word(sw) if not (i == 0 and self.sub_quoted) else "'%s'" % sw)
        sql = self.sql_text()
        if self.split_var is not None:
            w.append("$" + self.split_var)
        else:
            for u in self.flag_units:
                # Q12.3: an unquoted `~` that begins a word is the registered home alias form wherever the word stands, including as a flag's argument
                w.extend(quote_word(sql) if x == "@SQL" else (str(x) if isinstance(x, TildeExpand) else quote_word(x)) for x in u)
            if self.brace_args is not None:
                w.extend(self.brace_args)
            else:
                for i, a in enumerate(self.args):
                    if i in self.var_args:
                        w.append("$" + self.var_args[i])
                    elif a == "@SQL":
                        w.append(quote_word(sql))
                    else:
                        w.append(_arg_word(a))
        for r in self.redirs:
            w.append(_redir_text(r))
        return w


class RenderResult:
    def __init__(self, text, ops, programs, features):
        self.text = text
        self.ops = ops
        self.programs = programs
        self.features = features

    def to_dict(self):
        return {"text": self.text, "ops": self.ops, "programs": sorted(self.programs), "features": self.features}


def _plain_safe_for_var(word):
    return bool(word) and re.fullmatch(r"[A-Za-z0-9_./@%+:=,-]+", word) is not None


def plan_items(script):
    return [RItem(it.cmd, it.sep) for it in script.items]


def assemble(items, pre_stmts):
    out = "".join(p + "; " for p in pre_stmts)
    for it in items:
        out += " ".join(it.words())
        if it.sep == ";":
            out += "; "
        elif it.sep:
            out += " " + it.sep + " "
    return out.rstrip()


def render_plain(script, rng=None):
    items = plan_items(script)
    return RenderResult(assemble(items, []), [], {it.cmd.program for it in items}, base_features(items, [], []))


def base_features(items, ops, pre):
    txt = " ".join(" ".join(i.words()) for i in items)
    return {
        "n_ops": len(ops), "chain_len": len(items), "n_pre": len(pre),
        "wrapper_count": sum(len(i.wrappers) for i in items),
        "quote_count": txt.count("'") + txt.count('"'),
        "brace_count": txt.count("{"),
        "ifs_count": sum(1 for p in pre if p.startswith("IFS=")),
        "var_count": sum(1 for p in pre if not p.startswith("IFS=")),
    }


class RenderError(Exception):
    pass


def _is_simple_path_arg(a):
    return isinstance(a, str) and not isinstance(a, Glob) and a != "@SQL" and _plain_safe_for_var(a) \
        and not a.startswith("-")


def render(script, rng, names, ops, split="train", allowed_programs=None, registered_payload=True):
    """Apply `ops` (a list of operator names, in order) to a Script. Returns RenderResult.

    Operators that do not apply to this script are skipped and not listed in `ops_applied`.
    split: 'train' specs may not use held-out operators (RenderError). allowed_programs: the family's program
    set; an operator that would introduce a program outside it is refused (T53 has no wrappers/sh/base64)."""
    if isinstance(script, RawScript):
        raise RenderError("RawScript is rendered verbatim by the generator, not by operators")
    if split == "train":
        for o in ops:
            if o in HELDOUT_OPERATORS:
                raise RenderError("held-out operator %s on a train spec" % o)
    for o in ops:
        if o not in ALL_OPERATORS:
            raise RenderError("unknown operator %s" % o)
        if allowed_programs is not None:
            need = OPERATOR_PROGRAMS.get(o, set())
            if not need <= set(allowed_programs):
                raise RenderError("operator %s needs programs %s not in the family list" % (o, sorted(need - set(allowed_programs))))
    items = plan_items(script)
    applied, pre, used = [], [], set(i.cmd.program for i in items)
    text_ops = [o for o in ops if o in ("sh_c", "b64_pipe")]
    token_ops = [o for o in ops if o not in ("sh_c", "b64_pipe")]
    vcount = [0]

    def newvar():
        vcount[0] += 1
        return names.get("ns.variable", "v%d" % vcount[0]).upper()

    for o in token_ops:
        if o == "wrapper_insert":
            n = 0
            for it in items:
                if rng.random() < 0.6 or n == 0:
                    kind = rng.choice(("timeout", "nohup", "command", "env"))
                    if kind == "timeout":
                        it.wrappers.append(["timeout", str(rng.choice((5, 10, 30, 60)))])
                    elif kind == "env":
                        k, v = rng.choice(HARMLESS_ENV)
                        it.wrappers.append(["env", f"{k}={v}"])
                    else:
                        it.wrappers.append([kind])
                    used.add(kind)
                    n += 1
            applied.append(o)
        elif o == "flag_reorder":
            ok = False
            for it in items:
                if len(it.flag_units) >= 2:
                    before = [tuple(u) for u in it.flag_units]
                    for _ in range(6):
                        rng.shuffle(it.flag_units)
                        if [tuple(u) for u in it.flag_units] != before:
                            ok = True
                            break
            if ok:
                applied.append(o)
        elif o == "git_C":
            ok = False
            for it in items:
                if it.prog == "git" and not any(u and u[0] == "-C" for u in it.glob_units):
                    it.glob_units.insert(0, ["-C", "."])
                    ok = True
            if ok:
                applied.append(o)
        elif o == "quote_sub":
            ok = False
            for it in items:
                if it.sub_words:
                    it.sub_quoted = True
                    ok = True
            if ok:
                applied.append(o)
        elif o == "abs_path":
            ok = False
            for it in items:
                if it.prog in ABS_PATHS and not it.prog_var:
                    it.prog_word = ABS_PATHS[it.prog]
                    ok = True
            if ok:
                applied.append(o)
        elif o == "var_held":
            ok = False
            for it in items:
                cands = [i for i, a in enumerate(it.args) if _is_simple_path_arg(a)]
                if cands and not it.var_args:
                    i = rng.choice(cands)
                    v = newvar()
                    pre.append(f"{v}={quote_word(it.args[i])}")
                    it.var_args[i] = v
                    ok = True
                    break
            if not ok:
                for it in items:
                    if it.prog in ("git", "rm", "kubectl", "curl", "cat", "ls") and not it.prog_var:
                        v = newvar()
                        pre.append(f"{v}={it.prog}")
                        it.prog_var = v
                        ok = True
                        break
            if ok:
                applied.append(o)
        elif o == "brace":
            ok = False
            for it in items:
                if it.brace_args is None and len(it.args) >= 2 and all(_is_simple_path_arg(a) for a in it.args):
                    pre_p = _common_prefix(it.args)
                    rest = [a[len(pre_p):] for a in it.args]
                    suf = _common_suffix(rest)
                    mids = [r[:len(r) - len(suf)] if suf else r for r in rest]
                    if (pre_p or suf) and all(m and "," not in m and "/" not in m for m in mids) and len(set(mids)) == len(mids):
                        it.brace_args = [pre_p + "{" + ",".join(mids) + "}" + suf]
                        ok = True
            if ok:
                applied.append(o)
        elif o == "ifs_split":
            ok = False
            for it in items:
                words = [x for u in it.flag_units for x in u] + [a for a in it.args]
                if len(words) >= 2 and all(isinstance(w, str) and not isinstance(w, Glob) and w != "@SQL"
                                           and _plain_safe_for_var(w) for w in words) and it.cmd.sql is None:
                    d = rng.choice([c for c in IFS_CHARS if not any(c in w for w in words)] or [None])
                    if d is None:
                        continue
                    v = newvar()
                    pre.append("IFS=%s" % d)
                    pre.append('%s="%s"' % (v, d.join(words)))
                    it.split_var = v
                    ok = True
                    break
            if ok:
                applied.append(o)
    text = assemble(items, pre)
    feats_items = items
    for o in text_ops:
        if o == "sh_c":
            sh = rng.choice(("sh", "bash"))
            used.add(sh)
            text = "%s -c %s" % (sh, quote_word(text))
            applied.append(o)
        elif o == "b64_pipe":
            if not registered_payload:
                raise RenderError("b64_pipe needs a registered payload (K18)")
            sh = rng.choice(("sh", "bash"))
            lit = base64.b64encode(text.encode("utf-8")).decode("ascii")
            used.update({"echo", "base64", sh})
            if rng.random() < 0.7:
                text = "echo %s | base64 -d | %s" % (lit, sh)
            else:
                text = '%s -c "$(echo %s | base64 -d)"' % (sh, lit)
            applied.append(o)
    feats = base_features(feats_items, applied, pre)
    feats["text_wrap_depth"] = sum(1 for o in applied if o == "sh_c")
    feats["b64"] = int("b64_pipe" in applied)
    return RenderResult(text, applied, used, feats)


def _common_prefix(strs):
    import os.path
    return os.path.commonprefix(list(strs))


def _common_suffix(strs):
    import os.path
    rev = os.path.commonprefix([x[::-1] for x in strs])
    return rev[::-1]
