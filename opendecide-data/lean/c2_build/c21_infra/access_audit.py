"""Access audit for workflow agent transcripts (C2.1 plan v3.1 skeptic 7c; L-0 output (g)).

Reads transcripts (JSONL or JSON; path arg = file or directory), extracts every file path an agent
read or wrote through its tool calls, and reports PER AGENT LABEL PREFIX every path outside the
agent's declared scope. Scopes come from a JSON config (see audit_scopes.json): training lanes,
the sealed lane, L-E and L-D, as in LANE_L-0.md READ SCOPES.

Output is basenames and counts only. Transcript text, commands, file content and full paths are never
printed. Agents must not open transcripts themselves; only the orchestrator runs this tool.

How accesses are found
  Read -> read; Write/Edit/MultiEdit/NotebookEdit -> write; Glob/Grep -> search of the root joined with the
  pattern/glob; any tool with a "command" string -> Bash scan; any other tool -> its path-like input keys.
  Bash scan: tokens of every command (cat/sed/grep/head/python/..., redirections, tee, cp/mv, sed -i,
  rm/mkdir/touch, dd of=, find/ls/rg/grep -r search roots, the command word itself, `cd` tracking,
  backslash continuations, `bash -c`/`eval`/`$(...)`/backtick bodies, quoted paths with spaces, globs and
  brace lists, file:// URLs). Inline interpreter code (python -c, node -e, heredocs fed to an interpreter) is
  scanned for quoted path literals. Paths are compared case-INSENSITIVELY (APFS), `..` is collapsed and the
  real path of non-denied absolute paths is checked too (symlink escape).
  NOT visible: paths built at run time inside a script file, `xargs`/pipe input, paths read from files.
  Treat the report as a floor, not a proof.

Verdicts per access:
  ok | deny (matches a deny pattern, including a glob that could expand onto one) | out (not in allow list) |
  unresolved (relative path, cwd unknown or not in scope either way) | broad (search root that is an ancestor of
  the allow region: it can read or list files outside it) | dynamic (path with a shell variable/inline literal
  that could not be resolved and did not hit a deny pattern).
Result: FINDINGS (deny, out, broad or unmapped labels), INCOMPLETE (unparsed transcript lines) or CLEAN.
Exit codes: 0 clean, 1 findings/incomplete, 2 usage/config error.
Pattern syntax in the config: "glob:..." (** crosses '/'), "contains:..." (case-insensitive substring
of the normalised or raw path), "prefix:...". Variables {ROOT} {C21} {TI} {LANE} {OTHER} are expanded;
`--var NAME=VALUE` overrides a config variable (for example SCRATCH, the session's own scratch directory).
"""
import argparse
import functools
import json
import os
import re
import shlex
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathskip import glob_to_regex, is_skipped_name, safe_walk  # noqa: E402

LABEL_KEYS = ("agentLabel", "agent_label", "label", "agentName", "agent_name")
READ_TOOLS = {"Read": ("file_path",)}
WRITE_TOOLS = {"Write": ("file_path",), "Edit": ("file_path",), "MultiEdit": ("file_path",),
               "NotebookEdit": ("notebook_path", "file_path")}
SEARCH_TOOLS = {"Glob": ("path",), "Grep": ("path",)}
GENERIC_FILE_KEYS = ("file_path", "notebook_path", "path", "root", "directory", "dir")
GENERIC_DIR_KEYS = ("path", "root", "directory", "dir")
GENERIC_LIST_KEYS = ("paths", "file_paths")
MAX_DEPTH = 3
_SAFE_BASE = re.compile(r"[^\w.\-@+=,]")
_META = "*?[{"
_PATHCHARS = re.compile(r"^[\w.\-@+=,:%~/*?\[\]{}]+$")
_PATHCHARS_SP = re.compile(r"^[\w.\-@+=,:%~/ *?\[\]{}]+$")
_BARE = re.compile(r"^[\w.\-]+\.[A-Za-z][A-Za-z0-9]{0,5}$")
_HEREDOC = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_]\w*)\1")
_SUBST = re.compile(r"\$\(([^()]*)\)|`([^`]*)`")
_STR_LIT = re.compile(r"\"((?:[^\"\\\n]|\\.)*)\"|'((?:[^'\\\n]|\\.)*)'")
_VAR = re.compile(r"\$\{?[A-Za-z_]\w*\}?|\$\(|`")
_ASSIGN = re.compile(r"^[A-Za-z_]\w*=")
_INTERP = re.compile(r"^(python[\d.]*|pypy[\d.]*|node(js)?|deno|bun|ruby|perl|php|rscript|lua|osascript|tsx|ts-node)$", re.I)
_SHELLS = {"sh", "bash", "zsh", "dash", "ksh"}
_CODE_FLAG = re.compile(r"^-[A-Za-z]*[ceEp]$|^--(eval|print|command)$")
_SHELL_C = re.compile(r"^-[A-Za-z]*c$")
_WRAPPERS = {"sudo", "env", "command", "exec", "time", "nohup", "nice", "xargs", "then", "do", "else", "elif",
             "if", "while", "until", "!", "{", "}", "builtin", "stdbuf", "caffeinate", "timeout"}
_WRITE_HEADS = {"rm", "mkdir", "touch", "rmdir", "chmod", "truncate", "tee", "unlink", "shred", "patch", "chown", "dd"}
_COPY_HEADS = {"cp", "mv", "install", "ln", "rsync"}
_SEARCH_HEADS = {"grep", "egrep", "fgrep", "rg", "ag", "ack", "find", "fd", "ls", "tree", "du", "dir", "git-grep"}
_PATTERN_HEADS = {"grep", "egrep", "fgrep", "rg", "ag", "ack"}
_SEV = {"ok": 1, "unresolved": 2, "dynamic": 2, "broad": 3, "out": 4, "deny": 5}


class ConfigError(ValueError):
    pass


# ---------------------------------------------------------------- glob tokens
def has_meta(s):
    return any(c in s for c in _META)


def expand_braces(tok, limit=64):
    """Expand simple (non-nested) brace lists a{b,c}d -> [abd, acd]; capped."""
    m = re.search(r"\{([^{}]*,[^{}]*)\}", tok)
    if not m:
        return [tok]
    out = []
    for alt in m.group(1).split(","):
        out += expand_braces(tok[:m.start()] + alt + tok[m.end():], limit)
        if len(out) >= limit:
            break
    return out[:limit]


@functools.lru_cache(maxsize=8192)
def _comp_regex(comp):
    out, i, n = [], 0, len(comp)
    while i < n:
        c = comp[i]
        if c == "*":
            out.append(".*" if comp[i:i + 2] == "**" else "[^/]*")
            i += 2 if comp[i:i + 2] == "**" else 1
            continue
        if c == "?":
            out.append("[^/]")
        elif c == "[" and "]" in comp[i + 2:]:
            j = comp.index("]", i + 2)
            body = comp[i + 1:j]
            neg = body.startswith(("!", "^"))
            body = body[1:] if neg else body
            body = re.sub(r"([\\\[\]^&~|])", r"\\\1", body).replace("--", "-\\-")
            out.append("[" + ("^" if neg else "") + body + "]")
            i = j + 1
            continue
        else:
            out.append(re.escape(c))
        i += 1
    try:
        return re.compile("".join(out), re.I)
    except re.error:
        return re.compile(re.escape(comp), re.I)


@functools.lru_cache(maxsize=8192)
def token_regex(token):
    """Regex for a whole path token with shell wildcards (** crosses '/', * and ? do not)."""
    parts = token.split("/")
    out = []
    for k, p in enumerate(parts):
        if p == "**":
            out.append("(?:.*)")
        else:
            out.append(_comp_regex(p).pattern)
    # 'a/**/b' -> a/(?:.*)/b would demand two slashes; allow zero directories
    rx = "/".join(out).replace("/(?:.*)/", "/(?:.*/)?")
    try:
        return re.compile("^" + rx + "$", re.I)
    except re.error:
        return re.compile("^" + re.escape(token) + "$", re.I)


def comps(path):
    return [c for c in path.split("/") if c]


# ---------------------------------------------------------------- patterns
class Pattern:
    def __init__(self, text):
        self.text = text
        self.static = None
        self.exact = False
        self.comps = []
        if text.startswith("contains:"):
            self.kind, self.arg = "contains", text[9:].lower()
        elif text.startswith("prefix:"):
            self.kind, self.arg = "prefix", text[7:].lower()
            self.static = text[7:]
        else:
            body = text[5:] if text.startswith("glob:") else text
            self.kind = "glob"
            self.arg = re.compile(glob_to_regex(body).pattern, re.I)
            m = re.search(r"[*?\[{]", body)
            self.static = body if not m else body[:m.start()]
            self.exact = m is None
            self.comps = [c.lower() for c in body.split("/") if c]

    # exact path / string match
    def match(self, path):
        if self.kind == "contains":
            return self.arg in path.lower()
        if self.kind == "prefix":
            return path.lower().startswith(self.arg)
        return bool(self.arg.match(path))

    def is_ancestor_region(self, d):
        """True if directory d contains (part of) this pattern's region."""
        if not self.static:
            return False
        dd = d.rstrip("/") + "/"
        return self.static.lower().startswith(dd.lower())

    # could the wildcard token (absolute) expand onto this pattern's region?
    def reaches(self, token):
        if self.kind == "contains":
            return self.arg in token.lower()
        if self.kind == "prefix":
            cut = [i for i in (token.find(c) for c in "*?[") if i >= 0]
            p = token[:min(cut)].lower() if cut else token.lower()
            return bool(p) and (p.startswith(self.arg) or self.arg.startswith(p))
        if self.exact:
            return bool(token_regex(token).match("/" + "/".join(self.comps)))
        tcs = comps(token)
        for i, pc in enumerate(self.comps):
            if pc == "**":
                return True
            if i >= len(tcs):
                return False
            tc = tcs[i]
            if "**" in tc:
                return True
            if has_meta(pc):
                return True
            if not _comp_regex(tc).fullmatch(pc):
                return False
        return True

    # relative (cwd unknown) tokens: does the token look like a tail of a denied path?
    @staticmethod
    def _distinctive(rc):
        return len(rc) >= 2 or (len(rc) == 1 and len(rc[0]) >= 8 and not has_meta(rc[0]))

    def hit_rel(self, rcomps, inclusive=False):
        """rcomps: components of a relative token; leading '**' (an unknown prefix, e.g. a shell variable) is dropped.
        inclusive: the token is a search root, so the region directory itself counts."""
        if self.kind != "glob":
            return False
        rc = [c.lower() for c in rcomps]
        while rc and rc[0] == "**":
            rc = rc[1:]
        if not rc:
            return False
        D = self.comps
        if self.exact:
            n = len(rc)
            if n > len(D) or not self._distinctive(rc):
                return False
            tail = D[-n:]
            return all(_comp_regex(a).fullmatch(b) for a, b in zip(rc, tail))
        # region pattern: literal head L then '**' (or a wildcard component)
        L = []
        for c in D:
            if has_meta(c):
                break
            L.append(c)
        for m in range(1, min(len(L), len(rc)) + 1):
            if len(rc) <= m and not inclusive and "**" not in "".join(rc):
                continue
            if not all(_comp_regex(a).fullmatch(b) for a, b in zip(rc[:m], L[-m:])):
                continue
            if m >= 2 or len(L[-1]) >= 8:
                return True
        return False


def _expand(tpl, variables):
    out = tpl
    for _ in range(4):
        out = re.sub(r"\{(\w+)\}", lambda m: variables.get(m.group(1), m.group(0)), out)
    return out


class Scope:
    def __init__(self, name, spec, variables, common_read, common_write, lanes, own_lane):
        self.name = name
        self.unconfirmed = bool(spec.get("unconfirmed"))
        self.write_unconfirmed = bool(spec.get("write_unconfirmed"))
        v = dict(variables)
        v["LANE"] = own_lane or ""

        def pats(key, extra=()):
            return [Pattern(_expand(t, v)) for t in list(spec.get(key, [])) + list(extra)]
        self.allow_write = pats("allow_write", spec.get("_extra_allow_write", []))
        self.allow_read = pats("allow_read") + self.allow_write + [Pattern(_expand(t, v)) for t in common_read]
        self.deny_read = pats("deny_read")
        for tpl in spec.get("deny_read_per_other_lane", []):
            for other in lanes:
                if other != own_lane:
                    self.deny_read.append(Pattern(_expand(tpl.replace("{OTHER}", other), v)))
        self.allow_write_full = self.allow_write + [Pattern(_expand(t, v)) for t in common_write]
        self.deny_write = pats("deny_write") + self.deny_read


class Config:
    def __init__(self, obj, overrides=None):
        try:
            self.variables = dict(obj.get("vars", {}))
            self.variables.update(overrides or {})
            for k in list(self.variables):
                self.variables[k] = _expand(self.variables[k], self.variables)
            self.lanes = list(obj.get("lanes", []))
            self.common_read = obj.get("common_allow_read", [])
            self.common_write = obj.get("common_allow_write", [])
            self.scope_specs = obj["scopes"]
            self.agents = obj["agents"]
            self.label_map = obj.get("label_map", {})
        except (KeyError, TypeError) as e:
            raise ConfigError("config missing %s" % e)
        self.agents = sorted(self.agents, key=lambda a: -len(a["prefix"]))
        for a in self.agents:
            if a.get("scope") != "unrestricted" and a.get("scope") not in self.scope_specs:
                raise ConfigError("agent prefix %r names unknown scope %r" % (a["prefix"], a.get("scope")))
        self._cache = {}

    def agent_for(self, label):
        low = (label or "").lower()
        for a in self.agents:
            if low.startswith(a["prefix"].lower()):
                return a
        return None

    def scope_for(self, agent):
        key = agent["prefix"]
        if key not in self._cache:
            spec = dict(self.scope_specs[agent["scope"]])
            spec["_extra_allow_write"] = agent.get("allow_write", [])
            spec["allow_read"] = list(spec.get("allow_read", [])) + list(agent.get("allow_read", []))
            self._cache[key] = Scope(agent["scope"], spec, self.variables, self.common_read, self.common_write,
                                     self.lanes, agent.get("lane"))
        return self._cache[key]


# ---------------------------------------------------------------- bash extraction
def token_kind(tok):
    """'path' | 'dyn' | None for one shell word."""
    if not tok or len(tok) > 400:
        return None
    if tok.startswith("file://"):
        tok = tok[7:]
    if "://" in tok:
        return None
    if "$" in tok or "`" in tok:
        return "dyn" if ("/" in tok or tok.startswith("~")) else None
    if " " in tok:
        return "path" if tok.startswith(("/", "~/", "./", "../")) and _PATHCHARS_SP.match(tok) else None
    if tok.startswith(("/", "~/", "./", "../")) and _PATHCHARS.match(tok):
        return "path"
    if "/" in tok and _PATHCHARS.match(tok) and not tok.startswith("-"):
        return "path"
    return "path" if _BARE.match(tok) else None


def inline_literals(code):
    out = []
    for a, b in _STR_LIT.findall(code):
        s = a or b
        if 2 < len(s) <= 400 and "\n" not in s and ("/" in s or s.startswith("~") or _BARE.match(s)):
            out.append(s)
    return out


def _tokenize(line):
    try:
        lex = shlex.shlex(line, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        lex.commenters = ""
        return list(lex)
    except ValueError:
        return line.split()


def _heredoc_consumer(prefix_text):
    """Head word of the command a heredoc feeds: 'interp' | 'shell' | None."""
    chunk = re.split(r"[|;&]", prefix_text)[-1]
    toks = [t for t in _tokenize(chunk) if t]
    i = 0
    while i < len(toks) and (_ASSIGN.match(toks[i]) or toks[i] in _WRAPPERS):
        i += 1
    if i >= len(toks):
        return None
    head = os.path.basename(toks[i])
    if head in _SHELLS:
        return "shell"
    if _INTERP.match(head):
        return "interp"
    return None


def bash_accesses(cmd, cwd, depth=0, state=None):
    """-> list of (kind, token, cwd_at_that_point, search, mode). mode: path | dyn | inline. Best effort.
    state (dict, optional) receives the shell's cwd after the command ('cwd'), because the Bash tool keeps it."""
    res = []
    if depth > MAX_DEPTH:
        return res
    cmd = re.sub(r"\\\r?\n", " ", cmd)
    lines = cmd.split("\n")
    pending = []          # heredocs waiting for their body: [term, consumer, [lines]]
    kept = []
    for ln in lines:
        if pending:
            term, consumer, body = pending[0]
            if ln.strip() == term:
                pending.pop(0)
                text = "\n".join(body)
                if consumer == "interp":
                    for lit in inline_literals(text):
                        res.append(("read", lit, False, cwd, "inline"))
                elif consumer == "shell":
                    res += bash_accesses(text, cwd, depth + 1)
            else:
                body.append(ln)
            continue
        kept.append(ln)
        for m in _HEREDOC.finditer(ln):
            pending.append([m.group(2), _heredoc_consumer(ln[:m.start()]), []])
    for term, consumer, body in pending:           # unterminated heredoc: scan what is there, as code too
        text = "\n".join(body)
        if consumer == "interp":
            for lit in inline_literals(text):
                res.append(("read", lit, False, cwd, "inline"))
        elif consumer == "shell":
            res += bash_accesses(text, cwd, depth + 1)
        else:
            kept.extend(body)
    for line in kept:
        for m in _SUBST.finditer(line):
            res += bash_accesses(m.group(1) or m.group(2) or "", cwd, depth + 1)
        toks = _tokenize(line)
        segs, cur = [], []
        for t in toks:
            if t and set(t) <= set(";|&()"):
                if cur:
                    segs.append(cur)
                cur = []
            else:
                cur.append(t)
        if cur:
            segs.append(cur)
        for seg in segs:
            cwd = _scan_segment(seg, cwd, res, depth)
    if state is not None and depth == 0:
        state["cwd"] = cwd
    return list(dict.fromkeys(res)) if depth == 0 else res


def _scan_segment(seg, cwd, res, depth):
    i = 0
    while i < len(seg):
        t = seg[i]
        if _ASSIGN.match(t) or t in _WRAPPERS:
            if _ASSIGN.match(t):                          # CONFIG=/some/path cmd: the value is read by cmd
                val = t.split("=", 1)[1]
                if token_kind(val):
                    res.append(("read", val, False, cwd, token_kind(val)))
            i += 2 if (t == "timeout" and i + 1 < len(seg)) else 1
            continue
        break
    seg = seg[i:]
    if not seg:
        return cwd
    head_tok = seg[0]
    head = os.path.basename(head_tok)
    args = seg[1:]
    if head in ("cd", "pushd"):
        tgt = args[0] if args else "~"
        if tgt.startswith(("/", "~")):
            cwd = os.path.normpath(os.path.expanduser(tgt))
        elif cwd and "$" not in tgt:
            cwd = os.path.normpath(os.path.join(cwd, tgt))
        else:
            cwd = None if "$" in tgt else cwd
        return cwd
    if token_kind(head_tok) and ("/" in head_tok):          # a script or binary being executed
        res.append(("read", head_tok, False, cwd, "dyn" if token_kind(head_tok) == "dyn" else "path"))
    if head == "eval" and args:
        res += bash_accesses(" ".join(args), cwd, depth + 1)
    if head in _SHELLS:
        for k, a in enumerate(args[:-1]):
            if _SHELL_C.match(a):
                res += bash_accesses(args[k + 1], cwd, depth + 1)
                break
    if _INTERP.match(head):
        for k, a in enumerate(args[:-1]):
            if _CODE_FLAG.match(a):
                for lit in inline_literals(args[k + 1]):
                    res.append(("read", lit, False, cwd, "inline"))
    searchy = head in _SEARCH_HEADS or (head == "git" and "grep" in args[:3])
    pat_flag = head in _PATTERN_HEADS and any(a in ("-e", "--regexp", "-f", "--file") for a in args)
    recursive = head in ("rg", "ag", "ack") or head == "git"
    nonflag = []
    k = 0
    while k < len(args):
        a = args[k]
        if a in (">", ">>", ">|", "&>", "&>>") and k + 1 < len(args):
            res.append(("write", args[k + 1], False, cwd, token_kind(args[k + 1]) or "path"))
            k += 2
            continue
        if a == "<" and k + 1 < len(args):
            res.append(("read", args[k + 1], False, cwd, token_kind(args[k + 1]) or "path"))
            k += 2
            continue
        if a.startswith("-") and "=" in a:
            nonflag.append(a.split("=", 1)[1])
        elif a.startswith("-") and len(a) > 2 and a[1] != "-" and a[2] in "/~":
            nonflag.append(a[2:])                         # -I/path style
        elif a.startswith("-"):
            if head in ("grep", "egrep", "fgrep") and (re.match(r"^-[A-Za-z]*[rR][A-Za-z]*$", a) or a == "--recursive"):
                recursive = True
        else:
            nonflag.append(a)
        k += 1
    if head in _PATTERN_HEADS and nonflag and not pat_flag:
        nonflag = nonflag[1:]                             # the first operand is the pattern, not a path
    sed_inplace = head == "sed" and any(a == "--in-place" or a.startswith("-i") for a in args)
    found_path = False
    for idx, tok in enumerate(nonflag):
        kind = "read"
        if head in _WRITE_HEADS or sed_inplace:
            kind = "write"
        elif head in _COPY_HEADS:
            kind = "write" if (idx == len(nonflag) - 1 or head == "mv") else "read"
        if "=" in tok and not tok.startswith(("/", "~", ".")) and token_kind(tok.split("=", 1)[1]):
            key, tok = tok.split("=", 1)                  # dd of=/x if=/y
            if head == "dd":
                kind = "write" if key == "of" else "read"
        if head == "git" and ":" in tok and not tok.startswith(("/", "~", ".", "-")):
            tok = tok.split(":", 1)[1]                    # git show REV:path
        mode = token_kind(tok)
        if mode is None and searchy and tok in (".", "..", "~"):
            mode = "path"
        if mode:
            found_path = True
            res.append((kind, tok, searchy, cwd, mode))
    if searchy and not found_path and (recursive or head not in ("grep", "egrep", "fgrep")):
        res.append(("read", ".", True, cwd, "path"))      # no operand: the search root is the cwd
    return cwd


def bash_paths(cmd, cwd):
    """Compatibility view: list of (kind, token, cwd) for path-mode accesses."""
    return [(k, t, c) for k, t, _s, c, m in bash_accesses(cmd, cwd) if m == "path"]


# ---------------------------------------------------------------- tool uses
def iter_tool_uses(obj):
    stack = [obj]
    while stack:
        o = stack.pop()
        if isinstance(o, dict):
            if o.get("type") in ("tool_use", "server_tool_use") and isinstance(o.get("input"), dict) and isinstance(o.get("name"), str):
                yield o
            else:
                stack.extend(o.values())
        elif isinstance(o, list):
            stack.extend(o)


def _generic_accesses(inp, cwd):
    out = []
    for k in GENERIC_FILE_KEYS:
        v = inp.get(k)
        if isinstance(v, str) and v:
            out.append(("read", v, k in GENERIC_DIR_KEYS, cwd, "path"))
    for k in GENERIC_LIST_KEYS:
        v = inp.get(k)
        if isinstance(v, list):
            out += [("read", x, False, cwd, "path") for x in v if isinstance(x, str) and x]
    files = inp.get("files")
    vals = []
    if isinstance(files, dict):
        vals = list(files.values())
    elif isinstance(files, list):
        vals = files
    for x in vals:
        if isinstance(x, str) and x:
            out.append(("read", x, False, cwd, "path"))
        elif isinstance(x, dict):
            for kk in ("from", "path"):
                if isinstance(x.get(kk), str) and x[kk]:
                    out.append(("read", x[kk], False, cwd, "path"))
    u = inp.get("url")
    if isinstance(u, str) and u.startswith("file://"):
        out.append(("read", u, False, cwd, "path"))
    return out


def accesses_of(tool, inp, cwd, state=None):
    """-> list of (kind, raw_path, search_flag, cwd, mode)."""
    out = []
    if tool in READ_TOOLS or tool in WRITE_TOOLS:
        keys = READ_TOOLS.get(tool) or WRITE_TOOLS[tool]
        kind = "read" if tool in READ_TOOLS else "write"
        for k in keys:
            if isinstance(inp.get(k), str):
                out.append((kind, inp[k], False, cwd, "path"))
                break
    elif tool in SEARCH_TOOLS:
        base = inp.get("path") if isinstance(inp.get("path"), str) and inp.get("path") else (cwd or ".")
        extra = inp.get("pattern") if tool == "Glob" else inp.get("glob")
        if isinstance(extra, str) and extra:
            if extra.startswith(("/", "~")):
                target = extra
            elif tool == "Grep" and "/" not in extra:       # rg globs without a slash match at any depth
                target = base.rstrip("/") + "/**/" + extra
            else:
                target = base.rstrip("/") + "/" + extra
            out.append(("read", target, True, cwd, "path"))
        else:
            out.append(("read", base, True, cwd, "path"))
    elif isinstance(inp.get("command"), str):
        for kind, tok, search, c, mode in bash_accesses(inp["command"], cwd, 0, state):
            out.append((kind, tok, search, c, mode))
    else:
        out = _generic_accesses(inp, cwd)
    return out


def normalise(raw, cwd):
    """-> (path, resolved?)"""
    p = raw[7:] if raw.startswith("file://") else raw
    p = os.path.expanduser(p) if p.startswith("~") else p
    if os.path.isabs(p):
        return re.sub(r"^/{2,}", "/", os.path.normpath(p)), True
    if cwd and (p.startswith(("./", "../")) or p in (".", "..")):
        return os.path.normpath(os.path.join(cwd, p)), True
    return (p[2:] if p.startswith("./") else p), False


# ---------------------------------------------------------------- judging
def _deny_hit(patterns, s, wild):
    for p in patterns:
        if p.match(s) or (wild and p.reaches(s)):
            return True
    return False


def _search_root(v):
    cs = []
    for c in v.split("/"):
        if has_meta(c):
            break
        cs.append(c)
    return "/".join(cs) or "/"


def _variants(raw):
    out = []
    for v in expand_braces(raw):
        out.append(v)
    return out or [raw]


def _var_to_glob(text):
    t = re.sub(r"\$\{[^}]*\}|\$[A-Za-z_]\w*", "**", text)
    return re.sub(r"\$\([^)]*\)|`[^`]*`", "**", t)


def judge_one(scope, kind, raw, cwd, search, mode):
    deny = scope.deny_write if kind == "write" else scope.deny_read
    allow = scope.allow_write_full if kind == "write" else scope.allow_read
    if mode in ("dyn", "inline"):
        txt = raw[7:] if raw.startswith("file://") else raw
        g = _var_to_glob(txt) if mode == "dyn" else txt
        g = os.path.expanduser(g) if g.startswith("~") else g
        for v in _variants(g):
            if any(p.kind == "contains" and (p.arg in txt.lower() or p.arg in v.lower()) for p in deny):
                return "deny"
            if v.startswith("/"):
                nv = re.sub(r"^/{2,}", "/", os.path.normpath(v)) if "**" not in v else v
                if _deny_hit(deny, nv, has_meta(nv)):
                    return "deny"
            if any(p.hit_rel(comps(v)) for p in deny):
                return "deny"
        return "dynamic"
    path, resolved = normalise(raw, cwd)
    worst = "ok"
    for v in _variants(path):
        wild = has_meta(v)
        r = _judge_path(deny, allow, raw, v, resolved, cwd, search, wild)
        if _SEV[r] > _SEV[worst]:
            worst = r
    return worst


def _judge_path(deny, allow, raw, v, resolved, cwd, search, wild):
    if any(p.kind == "contains" and (p.arg in raw.lower() or p.arg in v.lower()) for p in deny):
        return "deny"
    if resolved:
        if _deny_hit(deny, v, wild):
            return "deny"
        rp = _real(v) if not wild else v
        if rp != v and _deny_hit(deny, rp, False):
            return "deny"                                   # symlink escape onto a denied path
        if allow_hit(allow, v):
            return "ok"
        if rp != v and allow_hit(allow, rp):
            return "ok"
        if search:
            root = _search_root(v)
            if any(p.is_ancestor_region(root) for p in allow):
                return "broad"
        return "out"
    # relative path, cwd unknown (or token not clearly a path): look for a denied tail, then give up
    if _deny_hit(deny, v, wild):
        return "deny"
    if any(p.hit_rel(comps(v), inclusive=search) for p in deny):
        return "deny"
    if search and not cwd and v in (".", ".."):
        return "broad"                                      # search root unknown: it can reach anything
    if cwd:
        joined = os.path.normpath(os.path.join(cwd, v))
        if _deny_hit(deny, joined, wild):
            return "deny"
        if allow_hit(allow, joined):
            return "ok"
        if search:
            root = _search_root(joined)
            if any(p.is_ancestor_region(root) for p in allow) and not allow_hit(allow, joined):
                return "broad"
    return "unresolved"


def _real(v):
    """Real path of a non-denied absolute path (lstat only, never for ohs/sealed-named paths)."""
    if not v.startswith("/") or is_skipped_name(v):
        return v
    try:
        return os.path.realpath(v)
    except OSError:
        return v


def allow_hit(allow, v):
    return any(p.match(v) for p in allow)


def judge(scope, kind, raw, cwd, search, mode):
    return judge_one(scope, kind, raw, cwd, search, mode)


def safe_base(path):
    b = os.path.basename(path.rstrip("/")) or "/"
    b = _SAFE_BASE.sub("?", b)
    return b[:80]


# ---------------------------------------------------------------- transcripts
def find_transcripts(path):
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        return [p for p in safe_walk(path, only_below_data=True)
                if p.endswith((".jsonl", ".json")) and not p.endswith(".meta.json")]
    raise ConfigError("transcript path not found: %s" % os.path.basename(path))


def read_entries(path):
    """-> (entries, bad_line_count). JSONL, a (pretty-printed) JSON array, or one JSON object."""
    bad = 0
    objs = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            first = f.readline()
            try:
                json.loads(first) if first.strip() else None
                jsonl = True
            except ValueError:
                jsonl = False
            f.seek(0)
            if not jsonl:
                try:
                    data = json.load(f)
                    return (data if isinstance(data, list) else [data]), 0
                except ValueError:
                    f.seek(0)
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    objs.append(json.loads(ln))
                except ValueError:
                    bad += 1
    except OSError:
        return [], 1
    return objs, bad


def audit(transcripts, cfg, label_override=None):
    """-> (stats, unmapped, unrestricted, bad_lines, n_tool_uses, no_tool_use_files)"""
    stats = defaultdict(lambda: {"agents": set(), "verdict": Counter(), "findings": Counter(), "tools": 0})
    unmapped = Counter()
    unrestricted = Counter()
    bad_lines = 0
    n_tool_uses = 0
    no_tool_use_files = 0
    for tp in transcripts:
        stem = os.path.splitext(os.path.basename(tp))[0]
        entries, bad = read_entries(tp)
        bad_lines += bad
        seen_ids = set()
        file_label = label_override or cfg.label_map.get(stem) or stem
        cwd = None
        before = n_tool_uses
        for ent in entries:
            if isinstance(ent, dict):
                if isinstance(ent.get("cwd"), str):
                    cwd = ent["cwd"]
                lab = label_override
                if not lab:
                    for k in LABEL_KEYS:
                        if isinstance(ent.get(k), str) and ent[k]:
                            lab = ent[k]
                            break
                    if not lab and isinstance(ent.get("agentId"), str):
                        lab = cfg.label_map.get(ent["agentId"])
                lab = lab or file_label
            else:
                lab = file_label
            for tu in iter_tool_uses(ent):
                tid = tu.get("id")
                if tid:
                    if (tp, tid) in seen_ids:
                        continue
                    seen_ids.add((tp, tid))
                n_tool_uses += 1
                agent = cfg.agent_for(lab)
                if agent is None:
                    unmapped[lab[:40]] += 1
                    continue
                if agent["scope"] == "unrestricted":
                    unrestricted[agent["prefix"]] += 1
                    continue
                st = stats[agent["prefix"]]
                st["agents"].add((tp, lab))
                st["tools"] += 1
                scope = cfg.scope_for(agent)
                state = {"cwd": cwd}
                for kind, raw, search, c, mode in accesses_of(tu["name"], tu["input"], cwd, state):
                    v = judge(scope, kind, raw, c, search, mode)
                    st["verdict"][v] += 1
                    if v in ("deny", "out", "broad"):
                        st["findings"][(v, kind, safe_base(raw if mode != "path" else normalise(raw, c)[0]))] += 1
                cwd = state["cwd"]            # the Bash tool's shell keeps its cwd between calls
        if entries and n_tool_uses == before:
            no_tool_use_files += 1
    return stats, unmapped, unrestricted, bad_lines, n_tool_uses, no_tool_use_files


def summarise(stats, unmapped, unrestricted, bad_lines, n_tool_uses, no_tool_use_files, n_files, cfg):
    rep = {"transcripts": n_files, "tool_uses": n_tool_uses, "unparsed_lines": bad_lines,
           "transcripts_without_tool_use": no_tool_use_files,
           "unmapped_labels": dict(unmapped), "unrestricted_tool_uses": dict(unrestricted), "prefixes": {}}
    bad = bool(unmapped)
    for prefix in sorted(stats):
        st = stats[prefix]
        agent = next(a for a in cfg.agents if a["prefix"] == prefix)
        v = st["verdict"]
        sc = cfg.scope_for(agent)
        rep["prefixes"][prefix] = {
            "scope": agent["scope"],
            "scope_unconfirmed": sc.unconfirmed,
            "write_allow_unconfirmed": sc.write_unconfirmed,
            "agents": len(st["agents"]), "tool_uses": st["tools"],
            "ok": v["ok"], "deny": v["deny"], "out": v["out"], "unresolved": v["unresolved"], "broad": v["broad"],
            "dynamic": v["dynamic"],
            "findings": [{"verdict": k[0], "kind": k[1], "basename": k[2], "count": n}
                         for k, n in sorted(st["findings"].items(), key=lambda kv: (-kv[1], kv[0]))],
        }
        bad = bad or v["deny"] > 0 or v["out"] > 0 or v["broad"] > 0
    rep["findings_present"] = bad
    rep["incomplete"] = bad_lines > 0
    return rep


def render(rep, limit=40):
    lines = ["ACCESS AUDIT transcripts=%d tool_uses=%d unparsed_lines=%d transcripts_without_tool_use=%d" % (
        rep["transcripts"], rep["tool_uses"], rep["unparsed_lines"], rep.get("transcripts_without_tool_use", 0))]
    for prefix, p in rep["prefixes"].items():
        lines.append("== %s scope=%s%s%s agents=%d tool_uses=%d ok=%d deny=%d out=%d broad=%d unresolved=%d dynamic=%d" % (
            prefix, p["scope"], " (UNCONFIRMED scope)" if p["scope_unconfirmed"] else "",
            " (write allow-list UNCONFIRMED)" if p.get("write_allow_unconfirmed") else "", p["agents"], p["tool_uses"],
            p["ok"], p["deny"], p["out"], p["broad"], p["unresolved"], p.get("dynamic", 0)))
        for f in p["findings"][:limit]:
            lines.append("   %-5s %-5s %s x%d" % (f["verdict"].upper(), f["kind"], f["basename"], f["count"]))
        if len(p["findings"]) > limit:
            lines.append("   (+%d more basenames)" % (len(p["findings"]) - limit))
    if rep["unmapped_labels"]:
        lines.append("UNMAPPED labels (no scope, cannot verify): " + ", ".join(
            "%s x%d" % (_SAFE_BASE.sub("?", k), n) for k, n in sorted(rep["unmapped_labels"].items())))
    if rep["unrestricted_tool_uses"]:
        lines.append("UNRESTRICTED (not audited): " + ", ".join("%s x%d" % kv for kv in sorted(rep["unrestricted_tool_uses"].items())))
    if rep.get("incomplete"):
        lines.append("INCOMPLETE: %d transcript line(s) could not be parsed; accesses on them were not audited" % rep["unparsed_lines"])
    lines.append("RESULT: " + ("FINDINGS" if rep["findings_present"] else "INCOMPLETE" if rep.get("incomplete") else "CLEAN"))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Audit workflow agent transcripts against declared read/write scopes (basenames and counts only).")
    ap.add_argument("transcripts", help="transcript file or directory")
    ap.add_argument("--config", required=True, help="scope config JSON (audit_scopes.json)")
    ap.add_argument("--label", help="force one agent label for every transcript (single-agent files)")
    ap.add_argument("--var", action="append", default=[], metavar="NAME=VALUE",
                    help="override a config variable, e.g. SCRATCH=/private/tmp/claude-501/<proj>/<session>/scratchpad")
    ap.add_argument("--json", action="store_true", help="print the report as JSON (same fields, no content)")
    ap.add_argument("--limit", type=int, default=40)
    a = ap.parse_args(argv)
    try:
        over = {}
        for kv in a.var:
            if "=" not in kv:
                raise ConfigError("--var needs NAME=VALUE")
            k, v = kv.split("=", 1)
            over[k] = v
        with open(a.config, "r", encoding="utf-8") as f:
            cfg = Config(json.load(f), over)
        files = find_transcripts(a.transcripts)
    except (OSError, ValueError) as e:
        print("access_audit: %s" % (e if isinstance(e, ConfigError) else "cannot read config/transcripts"), file=sys.stderr)
        return 2
    res = audit(files, cfg, a.label)
    rep = summarise(*res, len(files), cfg)
    print(json.dumps(rep, indent=1, sort_keys=True) if a.json else render(rep, a.limit))
    return 1 if (rep["findings_present"] or rep["incomplete"]) else 0


if __name__ == "__main__":
    sys.exit(main())
