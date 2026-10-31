"""Our own small shell expander (G0-lite T50 section 2/3). PARSE-ONLY: nothing here runs a command, spawns a
process or evals a string (K16). It owns:

  quoting ('..', "..", backslash), $X, ${X}, ${X:-d}, brace expansion {a,b}, IFS field splitting,
  separators ; && || |, simple redirections (> >> < 2> 2>> 2>&1), visible here-strings (<<<) and heredocs,
  $() ONLY of resolver-list pure commands (echo, printf, base64 -d of a visible literal),
  base64 decode of a VISIBLE literal (resolver B64-LIT),
  pipe / here-string / heredoc of a visible literal into a shell (resolvers PIPE-LIT, HERESTRING-LIT, HEREDOC-LIT),
  sh -c SCRIPT (depth <= 2), run of a file whose content the session wrote (write-then-run, KNOWN-FILE).

Anything else is OPAQUE (rule R19): substitution outside the resolver list, redirection into execution of an
unknown source, control flow, a file the session did not write, a base64 payload whose source is not visible,
xargs fed by something other than a literal. Opaque is reported with a kind, never guessed.

The RESOLVER LIST below is frozen and hashed (RESOLVER_TABLE.sha); the sha is recorded beside the rule table.
"""
import base64
import binascii
import re
from dataclasses import dataclass, field

from .canon import FrozenTable
from .shellmodel import (ABS_TO_PROG, FLAG_ARITY, HARMLESS_ENV, OPERATOR_WRAPPERS, SHELLS, SUBCOMMANDS)

MAX_DEPTH = 2

RESOLVER_LIST = [
    {"id": "QUOTES", "what": "single quotes, double quotes, backslash escapes"},
    {"id": "VARS", "what": "$X ${X} ${X:-d}; prefix and standalone assignments; IFS field splitting of unquoted expansions"},
    {"id": "BRACE", "what": "brace expansion of literal alternatives {a,b}"},
    {"id": "SEPS", "what": "; && || | and newline"},
    {"id": "REDIR", "what": "> >> < 2> 2>> 2>&1"},
    {"id": "HEREDOC-LIT", "what": "heredoc body piped into a shell is the visible literal"},
    {"id": "HERESTRING-LIT", "what": "here-string into a shell is the visible literal"},
    {"id": "PIPE-LIT", "what": "echo/printf literal piped into a shell is the visible literal"},
    {"id": "CMDSUB-PURE", "what": "$(echo ..) $(printf '%s' ..) only"},
    {"id": "B64-LIT", "what": "base64 -d of a visible literal, piped to a shell or used through $(); decoded text is a registered payload"},
    {"id": "SH-C", "what": "sh -c / bash -c SCRIPT, nesting depth <= 2"},
    {"id": "KNOWN-FILE", "what": "run of a file whose content an earlier file-write call made visible (latest write wins)"},
    {"id": "WRAPPERS", "what": "timeout, nohup, command, env, sudo; registered absolute binary paths"},
]
RESOLVER_TABLE = FrozenTable("resolver_list", "v1", RESOLVER_LIST)

_COMPOUND_OPEN = ("for", "while", "until", "if", "case", "select")
_COMPOUND_CLOSE = {"for": "done", "while": "done", "until": "done", "if": "fi", "case": "esac", "select": "done"}
_ASSIGN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=")


class Opaque(Exception):
    def __init__(self, kind):
        super().__init__(kind)
        self.kind = kind


# ------------------------------------------------------------------------------------------------ words
@dataclass
class Word:
    parts: list = field(default_factory=list)      # ('lit', s) ('sq', s) ('dq', [subparts]) ('var', name, default|None)
    src: str = ""                                  # raw source slice (for validator shape comparison)


@dataclass
class RawCmd:
    assigns: list = field(default_factory=list)    # [(name, Word)]
    words: list = field(default_factory=list)      # [Word]
    redirs: list = field(default_factory=list)     # [(op, Word|None, body|None)]
    src: str = ""


@dataclass
class RawStmt:
    pipeline: list = field(default_factory=list)   # [RawCmd]
    sep: str = None                                # separator after the statement: ; && || or None
    opaque: str = None                             # set when the statement is a construct we refuse


class _P:
    """Recursive-descent char parser for the supported subset."""

    def __init__(self, text):
        self.s = text
        self.i = 0
        self.n = len(text)
        self.pending_heredocs = []                 # (RawCmd, redir_index, delim, quoted, strip_tabs)

    def peek(self, k=0):
        j = self.i + k
        return self.s[j] if j < self.n else ""

    def starts(self, lit):
        return self.s.startswith(lit, self.i)

    # ---- helpers -------------------------------------------------------------------------------
    def skip_blank(self):
        while self.i < self.n and self.s[self.i] in " \t":
            self.i += 1
        if self.starts("\\\n"):
            self.i += 2
            self.skip_blank()

    def read_heredocs_after_newline(self):
        for (cmd, ridx, delim, quoted, strip) in self.pending_heredocs:
            body = []
            while True:
                if self.i >= self.n:
                    raise Opaque("redirect_exec")          # unterminated heredoc
                j = self.s.find("\n", self.i)
                line = self.s[self.i:] if j < 0 else self.s[self.i:j]
                self.i = self.n if j < 0 else j + 1
                chk = line.lstrip("\t") if strip else line
                if chk == delim:
                    break
                body.append(chk if strip else line)
            op, tw, _ = cmd.redirs[ridx]
            text = "\n".join(body) + ("\n" if body else "")
            cmd.redirs[ridx] = (op, tw, _HereBody(text, quoted))         # quoted: late-binding fixture (section 6)
        self.pending_heredocs = []

    # ---- statements ----------------------------------------------------------------------------
    def parse(self):
        stmts = []
        while True:
            self.skip_blank()
            while self.peek() == "\n":
                self.i += 1
                self.read_heredocs_after_newline()
                self.skip_blank()
            if self.i >= self.n:
                break
            if self.peek() == "#":
                while self.i < self.n and self.s[self.i] != "\n":
                    self.i += 1
                continue
            stmts.append(self.statement())
        return stmts

    def statement(self):
        start = self.i
        # compound / subshell constructs are opaque (control flow)
        m = re.match(r"([A-Za-z_]+)(?=[\s;]|$)", self.s[self.i:])
        word0 = m.group(1) if m else ""
        if word0 in _COMPOUND_OPEN or word0 == "function" or (self.peek() != "" and self.peek() in "({"):
            return self.swallow_compound(word0)
        pipeline = [self.command()]
        sep = None
        while True:
            self.skip_blank()
            if self.starts("||"):
                self.i += 2
                sep = "||"
                break
            if self.starts("&&"):
                self.i += 2
                sep = "&&"
                break
            if self.starts("|&"):
                raise Opaque("redirect_exec")
            if self.peek() == "|":
                self.i += 1
                self.skip_blank()
                while self.peek() == "\n":
                    self.i += 1
                    self.read_heredocs_after_newline()
                    self.skip_blank()
                pipeline.append(self.command())
                continue
            if self.peek() == ";":
                self.i += 1
                sep = ";"
                break
            if self.peek() == "&":
                # background job: refused construct
                self.i += 1
                st = RawStmt(pipeline=[], sep=None, opaque="background")
                return st
            if self.peek() == "\n" or self.i >= self.n:
                break
            break
        if sep in ("&&", "||"):
            self.skip_blank()
            while self.peek() == "\n":
                self.i += 1
                self.read_heredocs_after_newline()
                self.skip_blank()
        return RawStmt(pipeline=pipeline, sep=sep)

    def swallow_compound(self, word0):
        """Skip a compound command / subshell to its end; report control_flow."""
        depth = 0
        opener = word0 if word0 in _COMPOUND_OPEN else None
        if self.peek() != "" and self.peek() in "({":
            close = ")" if self.peek() == "(" else "}"
            op = self.peek()
            level = 0
            while self.i < self.n:
                ch = self.s[self.i]
                if ch == "'":
                    j = self.s.find("'", self.i + 1)
                    self.i = self.n if j < 0 else j + 1
                    continue
                if ch == '"':
                    j = self.i + 1
                    while j < self.n and self.s[j] != '"':
                        j += 2 if self.s[j] == "\\" else 1
                    self.i = j + 1
                    continue
                if ch == op:
                    level += 1
                elif ch == close:
                    level -= 1
                    if level == 0:
                        self.i += 1
                        break
                self.i += 1
            return RawStmt(opaque="control_flow")
        # keyword compounds: count nested openers / closers by whole words
        toks = []
        stack = []
        while self.i < self.n:
            self.skip_blank()
            m = re.match(r"[A-Za-z_]+", self.s[self.i:])
            if m:
                w = m.group(0)
                self.i += len(w)
                if w in _COMPOUND_OPEN:
                    stack.append(_COMPOUND_CLOSE[w])
                elif stack and w == stack[-1]:
                    stack.pop()
                    if not stack:
                        break
                elif word0 == "function":
                    pass
                continue
            ch = self.peek()
            if ch == "'":
                j = self.s.find("'", self.i + 1)
                self.i = self.n if j < 0 else j + 1
            elif ch == '"':
                j = self.i + 1
                while j < self.n and self.s[j] != '"':
                    j += 2 if self.s[j] == "\\" else 1
                self.i = j + 1
            else:
                self.i += 1
        return RawStmt(opaque="control_flow")

    # ---- one simple command --------------------------------------------------------------------
    def command(self):
        cmd = RawCmd()
        start = self.i
        first = True
        while True:
            self.skip_blank()
            ch = self.peek()
            if ch == "" or ch in "\n;|":
                break
            if self.starts("&&") or self.starts("||"):
                break
            if ch == "&" and not self.starts("&>"):
                break
            if ch == "#":                              # a `#` that starts a new word is a comment to end of line
                while self.i < self.n and self.s[self.i] != "\n":
                    self.i += 1
                break
            if ch in "()":
                raise Opaque("control_flow")
            if ch == "`":
                raise Opaque("cmdsub")
            r = self.try_redir()
            if r is not None:
                cmd.redirs.append(r)
                continue
            w = self.word()
            if first and not cmd.words:
                lit = "".join(p[1] for p in w.parts[:1] if p[0] == "lit")
                am = _ASSIGN.match(lit) if w.parts and w.parts[0][0] == "lit" else None
                if am:
                    name = am.group(1)
                    rest = Word(parts=[], src=w.src[len(name) + 1:])
                    first_lit = w.parts[0][1][len(name) + 1:]
                    rest.parts = ([("lit", first_lit)] if first_lit else []) + w.parts[1:]
                    cmd.assigns.append((name, rest))
                    continue
            first = False
            cmd.words.append(w)
        cmd.src = self.s[start:self.i].strip()
        return cmd

    def try_redir(self):
        s = self.s
        i = self.i
        m = re.match(r"(\d*)(>>|>&|>|<<<|<<-|<<|<)", s[i:])
        if m:
            fd, op = m.group(1), m.group(2)
            if s.startswith("&>", i):
                self.i += 2
                self.skip_blank()
                return ("&>", self.word(), None)
            self.i += len(m.group(0))
            if op == ">&":
                self.skip_blank()
                tw = self.word()
                return ((fd or "1") + ">&", tw, None)
            full = (fd + op) if fd else op
            self.skip_blank()
            if op in ("<<", "<<-"):
                dw = self.word()
                delim = "".join(self._plain(p) for p in dw.parts)
                quoted = any(p[0] in ("sq", "dq") for p in dw.parts)
                rc = (full, dw, "")
                return self._register_heredoc(rc, delim, quoted, op == "<<-")
            tw = self.word()
            return (full, tw, None)
        if s.startswith("&>", i):
            self.i += 2
            self.skip_blank()
            return ("&>", self.word(), None)
        return None

    def _register_heredoc(self, rc, delim, quoted, strip):
        # the owning command is attached by the caller via marker: store on parser, bind in command()
        holder = _HereHolder(rc, delim, quoted, strip)
        self._last_here = holder
        return holder

    @staticmethod
    def _plain(part):
        if part[0] in ("lit", "sq"):
            return part[1]
        if part[0] == "dq":
            return "".join(x[1] for x in part[1] if x[0] == "lit")
        return ""

    # ---- words ---------------------------------------------------------------------------------
    def word(self):
        start = self.i
        parts = []
        lit = []

        def flush():
            if lit:
                parts.append(("lit", "".join(lit)))
                lit.clear()

        while self.i < self.n:
            ch = self.s[self.i]
            if ch in " \t\n;|&<>()":
                if ch == "&" and self.peek(1) == "&":
                    break
                if ch in "<>" and self.peek(1) == "(":
                    raise Opaque("cmdsub")
                break
            if ch == "\\":
                if self.peek(1) == "\n":
                    self.i += 2
                    continue
                lit.append(self.peek(1))
                self.i += 2
                continue
            if ch == "'":
                j = self.s.find("'", self.i + 1)
                if j < 0:
                    raise Opaque("cmdsub")
                flush()
                parts.append(("sq", self.s[self.i + 1:j]))
                self.i = j + 1
                continue
            if ch == '"':
                flush()
                parts.append(("dq", self.dquote()))
                continue
            if ch == "$":
                flush()
                parts.append(self.dollar(in_dq=False))
                continue
            if ch == "`":
                raise Opaque("cmdsub")
            if ch == "{" and self.peek(1) not in ("", " "):
                j = self.s.find("}", self.i)
                inner = self.s[self.i + 1:j] if j > 0 else ""
                if j > 0 and "," in inner and not re.search(r"[\s$'\"`\\{]", inner):
                    flush()
                    parts.append(("brace", inner.split(",")))
                    self.i = j + 1
                    continue
            lit.append(ch)
            self.i += 1
        flush()
        return Word(parts=parts, src=self.s[start:self.i])

    def dquote(self):
        self.i += 1                                  # opening quote
        out, buf = [], []

        def flush():
            if buf:
                out.append(("lit", "".join(buf)))
                buf.clear()

        while True:
            if self.i >= self.n:
                raise Opaque("cmdsub")
            ch = self.s[self.i]
            if ch == '"':
                self.i += 1
                break
            if ch == "\\" and self.peek(1) in ('$', '"', "\\", "`", "\n"):
                if self.peek(1) != "\n":
                    buf.append(self.peek(1))
                self.i += 2
                continue
            if ch == "$":
                flush()
                out.append(self.dollar(in_dq=True))
                continue
            if ch == "`":
                raise Opaque("cmdsub")
            buf.append(ch)
            self.i += 1
        flush()
        return out

    def dollar(self, in_dq):
        s, i = self.s, self.i
        if s.startswith("$((", i):
            raise Opaque("cmdsub")
        if s.startswith("$(", i):
            depth, j = 0, i + 1
            while j < self.n:
                c = s[j]
                if c == "'":
                    k = s.find("'", j + 1)
                    j = self.n if k < 0 else k
                elif c == '"':
                    k = j + 1
                    while k < self.n and s[k] != '"':
                        k += 2 if s[k] == "\\" else 1
                    j = k
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if depth != 0:
                raise Opaque("cmdsub")
            inner = s[i + 2:j]
            self.i = j + 1
            return ("cmdsub", inner)
        if s.startswith("${", i):
            j = s.find("}", i)
            if j < 0:
                raise Opaque("cmdsub")
            body = s[i + 2:j]
            self.i = j + 1
            m = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?::-(.*))?", body)
            if not m:
                raise Opaque("cmdsub")
            return ("var", m.group(1), m.group(2))
        m = re.match(r"\$([A-Za-z_][A-Za-z0-9_]*)", s[i:])
        if m:
            self.i += len(m.group(0))
            return ("var", m.group(1), None)
        # a lone $ or $? etc.: literal dollar
        self.i += 1
        return ("lit", "$")


class _HereHolder(tuple):
    """try_redir returns this for << so command() can bind the pending heredoc to the owning RawCmd."""

    def __new__(cls, rc, delim, quoted, strip):
        o = super().__new__(cls, rc)
        o.delim, o.quoted, o.strip = delim, quoted, strip
        return o


class _HereBody(str):
    """A heredoc body (late-binding fixture, addendum section 6): a plain str (every existing caller that treats
    the body as text, e.g. `body or ""`, string concat, equality, keeps working unchanged) plus `.quoted`: whether
    the delimiter was quoted (`<<'EOF'`, no expansion) or not (`<<EOF`, variables expand at the point the heredoc
    is READ, using the env as it stands there)."""

    def __new__(cls, text, quoted):
        o = super().__new__(cls, text)
        o.quoted = bool(quoted)
        return o


_VAR_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def _expand_vars_in_text(text, env):
    """Scoped, text-level `$VAR` / `${VAR}` substitution for an unquoted heredoc body (late-binding fixture).
    Not a general word-parser: sufficient for the heredoc-body fixture, which is plain text, not shell syntax."""
    return _VAR_REF.sub(lambda m: env.get(m.group(1) or m.group(2), ""), text)


def _bind_heredocs(parser, cmd):
    for idx, r in enumerate(cmd.redirs):
        if isinstance(r, _HereHolder):
            cmd.redirs[idx] = (tuple(r)[0], tuple(r)[1], "")
            parser.pending_heredocs.append((cmd, idx, r.delim, r.quoted, r.strip))


def parse_script(text):
    p = _P(text)
    stmts = []
    # statements are parsed one by one so a refused construct only poisons its own statement
    while True:
        p.skip_blank()
        while p.peek() == "\n":
            p.i += 1
            p.read_heredocs_after_newline()
            p.skip_blank()
        if p.i >= p.n:
            break
        if p.peek() == "#":
            while p.i < p.n and p.s[p.i] != "\n":
                p.i += 1
            continue
        try:
            st = p.statement()
            for c in st.pipeline:
                _bind_heredocs(p, c)
            stmts.append(st)
        except Opaque as e:
            stmts.append(RawStmt(opaque=e.kind))
            # recover: skip to the next statement boundary at depth 0 (newline or ;)
            while p.i < p.n and p.s[p.i] not in "\n;":
                p.i += 1
            if p.i < p.n and p.s[p.i] == ";":
                p.i += 1
    return stmts


# ------------------------------------------------------------------------------------------------ resolution
@dataclass
class RCmd:
    words: list                                  # after wrapper unwrapping; words[0] is the program
    sudo: bool = False
    env: list = field(default_factory=list)      # semantic (non-harmless) env assignments
    redirs: list = field(default_factory=list)   # [(op, target_text)]
    sep: str = None
    operator_wrappers: list = field(default_factory=list)
    via: list = field(default_factory=list)      # how it was reached: sh-c, pipe-lit, b64-lit, heredoc, known-file ...


@dataclass
class Resolution:
    cmds: list = field(default_factory=list)     # flattened RCmd list
    opaque: list = field(default_factory=list)   # opaque kinds encountered
    resolvers: list = field(default_factory=list)  # resolver ids actually used
    assign_stmts: int = 0
    fetched: set = field(default_factory=set)      # paths written by curl/wget -o/-O earlier in the script

    @property
    def resolvable(self):
        return not self.opaque


def _split_ifs(value, ifs, fields, cur):
    """Append `value` (an UNQUOTED expansion result) to the open field list; returns the open field or None."""
    for ch in value:
        if ch in ifs:
            if ch in " \t\n":
                if cur is not None:
                    fields.append(cur)
                    cur = None
            else:
                fields.append(cur if cur is not None else "")
                cur = None
        else:
            cur = (cur or "") + ch
    return cur


_TRAP_SIGNALS = ("EXIT", "ERR", "INT", "TERM")


class Expander:
    def __init__(self, known_files=None, env=None):
        self.known_files = dict(known_files or {})   # path -> script text (earlier file-write calls, latest wins)
        self.env0 = dict(env or {})
        self._used = []                              # resolver ids used while expanding the current statement
        self._aliases = {}                            # late-binding fixture: alias NAME -> body text, latest wins

    # ---- public --------------------------------------------------------------------------------
    def resolve(self, text, _depth=0, _env=None):
        res = Resolution()
        env = dict(self.env0 if _env is None else _env)
        stmts = parse_script(text)
        traps = {}
        if _depth == 0:
            self._aliases = {}
        for st in stmts:
            if st.opaque:
                res.opaque.append(st.opaque)
                continue
            handled = self._trap_or_alias_stmt(st, env, traps, res)
            if handled:
                continue
            try:
                self._stmt(st, env, res, _depth)
            except Opaque as e:
                res.opaque.append(e.kind)
            res.resolvers.extend(self._used)
            self._used = []
        if traps.get("EXIT") is not None and _depth < MAX_DEPTH:
            # the SAME script/subshell's own EXIT trap fires when its own text ends, at ANY nesting depth (a
            # write-then-run payload, late-binding fixture addendum section 6, is resolved at depth 1, not 0).
            inner = self.resolve(traps["EXIT"], _depth=_depth + 1, _env=env)
            self._absorb(res, inner, None, ["TRAP-EXIT"])
        return res

    # ---- late-binding fixture: trap / alias / unalias (addendum section 6) ---------------------
    def _single_cmd(self, st):
        """st is a one-command, non-opaque statement, or None."""
        if st.opaque or len(st.pipeline) != 1:
            return None
        return st.pipeline[0]

    def _trap_or_alias_stmt(self, st, env, traps, res):
        """Recognises `trap 'BODY' SIGNAL`, `alias NAME='BODY'`, `unalias NAME` at the TOP level only (_depth==0).
        trap/alias bodies are registered (latest definition wins, GF2-style) and NEVER emitted as an RCmd
        themselves. Returns True when the statement was one of these (handled, whether resolvable or not)."""
        cmd = self._single_cmd(st)
        if cmd is None or not cmd.words or cmd.assigns or cmd.redirs:
            return False
        head = self._expand_word(cmd.words[0], env)
        if head != ["trap"] and head != ["alias"] and head != ["unalias"]:
            return False
        name = head[0]
        if name == "trap":
            ok = (len(cmd.words) == 3 and len(cmd.words[1].parts) == 1 and cmd.words[1].parts[0][0] in ("sq", "dq"))
            body = None
            if ok:
                part = cmd.words[1].parts[0]
                if part[0] == "sq":
                    body = part[1]                                  # single quotes: the body is expanded when the trap FIRES (latest binding wins)
                else:
                    # Q11.7 (Opus 18 Oct 2026): a double-quoted body is expanded NOW (at definition). A variable that is unset or whose value is not
                    # visible (and has no ${X:-d} default), or a command substitution, makes the expansion unresolvable -> late_binding (R19).
                    subs = part[1]
                    if any(sp[0] == "cmdsub" or (sp[0] == "var" and env.get(sp[1]) is None and sp[2] is None) for sp in subs):
                        ok = False
                    else:
                        body = "".join(self._value_part(sp, env) for sp in subs)
            sig = self._expand_word(cmd.words[2], env) if ok else []
            ok = ok and len(sig) == 1 and sig[0] in _TRAP_SIGNALS
            if ok:
                traps[sig[0]] = body
            else:
                res.opaque.append("late_binding")
            return True
        if name == "unalias":
            if len(cmd.words) == 2:
                for n in self._expand_word(cmd.words[1], env):
                    self._aliases.pop(n, None)
            else:
                res.opaque.append("late_binding")
            return True
        # alias NAME='BODY' : one word shaped lit("NAME=") + sq("BODY")
        if len(cmd.words) == 2 and len(cmd.words[1].parts) == 2:
            p0, p1 = cmd.words[1].parts
            if p0[0] == "lit" and p0[1].endswith("=") and p1[0] == "sq":
                aname = p0[1][:-1]
                if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", aname):
                    self._aliases[aname] = p1[1]            # latest definition wins (overwrite)
                    return True
        res.opaque.append("late_binding")
        return True

    def _alias_expand_first(self, words, env):
        """Latest-wins alias substitution of the command NAME only (real alias semantics); bounded against
        self-reference cycles."""
        seen = set()
        while words and words[0] in self._aliases and words[0] not in seen:
            seen.add(words[0])
            bstmts = parse_script(self._aliases[words[0]])
            if len(bstmts) != 1 or bstmts[0].opaque or len(bstmts[0].pipeline) != 1:
                break
            bcmd = bstmts[0].pipeline[0]
            bwords = []
            for w in bcmd.words:
                bwords.extend(self._expand_word(w, env))
            if not bwords:
                break
            words = bwords + words[1:]
        return words

    # ---- internals -----------------------------------------------------------------------------
    def _expand_word(self, w, env, quoted_ctx=False):
        """-> list of resulting words (strings). Handles brace expansion, vars, cmdsub, IFS splitting.

        `~` expansion (late-binding fixture: word-start, unquoted only): a word whose FIRST part is an
        unquoted literal starting with `~`, followed by `/` or nothing, expands that leading `~` to env["HOME"].
        A quoted `~` (parts[0] is "sq"/"dq") or a `~` not at word start never expands (quoting/position decides,
        as a real shell would)."""
        parts = list(w.parts)
        if parts and parts[0][0] == "lit" and parts[0][1].startswith("~"):
            rest = parts[0][1][1:]
            if rest == "" or rest.startswith("/"):
                parts[0] = ("lit", env.get("HOME", "~") + rest)
        # brace expansion: cross product over brace parts
        variants = [[]]
        for part in parts:
            if part[0] == "brace":
                variants = [v + [("lit", alt)] for v in variants for alt in part[1]]
            else:
                variants = [v + [part] for v in variants]
        out = []
        for parts in variants:
            out.extend(self._fields(parts, env))
        return out

    def _fields(self, parts, env):
        ifs = env.get("IFS", " \t\n")
        fields, cur, opened = [], None, False
        for p in parts:
            kind = p[0]
            if kind == "lit":
                cur = (cur or "") + p[1]
            elif kind == "sq":
                cur = (cur or "") + p[1]
            elif kind == "dq":
                txt = "".join(self._value_part(sp, env) for sp in p[1])
                cur = (cur or "") + txt
            else:                                    # unquoted var / cmdsub: split on IFS
                val = self._value_part(p, env)
                cur = _split_ifs(val, ifs, fields, cur)
        if cur is not None:
            fields.append(cur)
        return fields

    def _value_part(self, p, env):
        kind = p[0]
        if kind == "lit" or kind == "sq":
            return p[1]
        if kind == "var":
            name, default = p[1], p[2]
            if getattr(self, "_literal_vars", False):           # quoted-heredoc fixture: $NAME stays literal text
                return "$" + name if default is None else "${%s:-%s}" % (name, default)
            v = env.get(name)
            if v is None or (default is not None and v == ""):
                return default if default is not None else ""
            return v
        if kind == "cmdsub":
            return self._cmdsub(p[1], env)
        raise Opaque("cmdsub")

    def _cmdsub(self, inner, env):
        """Resolver CMDSUB-PURE / B64-LIT only. Anything else is opaque."""
        stmts = parse_script(inner)
        if len(stmts) != 1 or stmts[0].opaque:
            raise Opaque("cmdsub")
        pl = stmts[0].pipeline
        if stmts[0].sep is not None:
            raise Opaque("cmdsub")
        outs = self._pure_pipeline(pl, env)
        self._used.append("CMDSUB-PURE")
        return outs.rstrip("\n")

    def _pure_words(self, cmd, env):
        for _, __ in cmd.assigns:
            raise Opaque("cmdsub")
        words = []
        for w in cmd.words:
            words.extend(self._expand_word(w, env))
        return words

    def _pure_pipeline(self, pl, env):
        data = None
        for idx, cmd in enumerate(pl):
            words = self._pure_words(cmd, env)
            if not words:
                raise Opaque("cmdsub")
            prog = words[0]
            herestr = None
            for op, tw, body in cmd.redirs:
                if op == "<<<":
                    herestr = "".join(self._expand_word(tw, env)) + "\n"
                else:
                    raise Opaque("cmdsub")
            if prog == "echo":
                args = words[1:]
                nl = True
                if args and args[0] == "-n":
                    nl, args = False, args[1:]
                data = " ".join(args) + ("\n" if nl else "")
            elif prog == "printf":
                data = self._printf(words[1:])
            elif prog == "base64" and words[1:] == ["-d"]:
                src = herestr if herestr is not None else data
                if src is None:
                    raise Opaque("b64_invisible")
                data = self._b64(src)
                self._used.append("B64-LIT")
            else:
                raise Opaque("cmdsub")
        if data is None:
            raise Opaque("cmdsub")
        return data

    @staticmethod
    def _printf(args):
        if not args:
            raise Opaque("cmdsub")
        fmt, rest = args[0], args[1:]
        out, ri, i = [], 0, 0
        while i < len(fmt):
            if fmt.startswith("%s", i):
                out.append(rest[ri] if ri < len(rest) else "")
                ri += 1
                i += 2
            elif fmt.startswith("\\n", i):
                out.append("\n")
                i += 2
            elif fmt[i] == "%" or fmt[i] == "\\":
                raise Opaque("cmdsub")
            else:
                out.append(fmt[i])
                i += 1
        return "".join(out)

    @staticmethod
    def _b64(s):
        try:
            return base64.b64decode(s.strip().encode("ascii"), validate=True).decode("utf-8")
        except (binascii.Error, UnicodeError, ValueError):
            raise Opaque("b64_invisible")

    # ---- statements ----------------------------------------------------------------------------
    def _stmt(self, st, env, res, depth):
        pl = st.pipeline
        # assignment-only statements update env
        if len(pl) == 1 and not pl[0].words and pl[0].assigns and not pl[0].redirs:
            for name, w in pl[0].assigns:
                env[name] = "".join(self._expand_word_nosplit(w, env))
            res.assign_stmts += 1
            res.resolvers.append("VARS")
            return
        stages = []                                  # per stage: dict(words, assigns, redirs)
        for cmd in pl:
            words = []
            for w in cmd.words:
                words.extend(self._expand_word(w, env))
            words = self._alias_expand_first(words, env)       # late-binding fixture: latest alias definition wins
            assigns = [(n, "".join(self._expand_word_nosplit(w, env))) for n, w in cmd.assigns]
            redirs = []
            for op, tw, body in cmd.redirs:
                if op in ("<<",  "<<-"):
                    redirs.append((op, None, body))
                elif tw is None:
                    redirs.append((op, None, body))
                else:
                    t = self._expand_word(tw, env)
                    redirs.append((op, "".join(t), body))
            stages.append({"words": words, "assigns": assigns, "redirs": redirs})
        # stage-level unwrap
        unwrapped = [self._unwrap(s) for s in stages]
        # pipeline into a shell reading stdin?
        last = unwrapped[-1]
        if last["prog"] in SHELLS and not last["args_after_prog"]:
            inner_text, via, literal_vars = self._shell_stdin(unwrapped, res, env)
            if inner_text is not None:
                if depth >= MAX_DEPTH:
                    raise Opaque("control_flow")
                prev, self._literal_vars = getattr(self, "_literal_vars", False), literal_vars
                try:
                    inner = self.resolve(inner_text, depth + 1)
                finally:
                    self._literal_vars = prev
                self._absorb(res, inner, st.sep, via)
                return
        # shell with -c / file
        for u in unwrapped:
            if u["prog"] in SHELLS and u["args_after_prog"]:
                a = u["args_after_prog"]
                if a[0] == "-c" and len(a) >= 2:
                    if depth >= MAX_DEPTH:
                        raise Opaque("control_flow")
                    inner = self.resolve(a[1], depth + 1)
                    seps_ok = len(unwrapped) == 1
                    if not seps_ok:
                        raise Opaque("control_flow")
                    self._absorb(res, inner, st.sep, ["SH-C"])
                    return
                path = a[0]
                if path.startswith("-"):
                    raise Opaque("control_flow")
                if path in res.fetched:                # fetch-then-run: an ordinary pair of commands (E9)
                    res.cmds.append(RCmd(words=u["words"], sudo=u["sudo"], env=u["env"], sep=st.sep, operator_wrappers=u["opw"]))
                    return
                if path in self.known_files:
                    if depth >= MAX_DEPTH:
                        raise Opaque("control_flow")
                    inner = self.resolve(self.known_files[path], depth + 1)
                    self._absorb(res, inner, st.sep, ["KNOWN-FILE"])
                    return
                raise Opaque("unknown_file")
        # xargs fed dynamically
        for idx, u in enumerate(unwrapped):
            if u["prog"] == "xargs":
                if idx == 0 or not self._literal_feed(unwrapped[idx - 1]):
                    raise Opaque("xargs_dynamic")
        # plain pipeline of commands
        for idx, u in enumerate(unwrapped):
            if not u["words"]:
                raise Opaque("control_flow")
            if u["words"][0].startswith("/") and u["words"][0] not in ABS_TO_PROG:
                raise Opaque("unknown_file")
            if u["words"][0].startswith("./") or u["words"][0].startswith("../"):
                raise Opaque("unknown_file")
            sep = "|" if idx < len(unwrapped) - 1 else st.sep
            if u["words"][0] in ("curl", "wget"):
                ws = u["words"]
                for k in range(len(ws) - 1):
                    if ws[k] in ("-o", "-O"):
                        res.fetched.add(ws[k + 1])
            res.cmds.append(RCmd(words=u["words"], sudo=u["sudo"], env=u["env"],
                                 redirs=[(op, t) for op, t, b in u["redirs"] if op not in ("<<", "<<-", "<<<")]
                                 + [(op, b) for op, t, b in u["redirs"] if op in ("<<<",) and False],
                                 sep=sep, operator_wrappers=u["opw"]))

    def _expand_word_nosplit(self, w, env):
        """Assignment right-hand side: no field splitting."""
        variants = [[]]
        for part in w.parts:
            if part[0] == "brace":
                variants = [v + [("lit", part[1][0])] for v in variants]
            else:
                variants = [v + [part] for v in variants]
        out = []
        for parts in variants:
            out.append("".join(self._value_part(p, env) if p[0] != "dq" else
                               "".join(self._value_part(sp, env) for sp in p[1]) for p in parts))
        return out

    def _literal_feed(self, u):
        return u["prog"] in ("echo", "printf") and not u["redirs"]

    def _unwrap(self, st):
        words = list(st["words"])
        sudo, env, opw = False, [], []
        for (n, v) in st["assigns"]:
            if (n, v) in HARMLESS_ENV:
                opw.append("env")
            else:
                env.append((n, v))
        while words:
            w0 = ABS_TO_PROG.get(words[0], words[0])
            if w0 != words[0]:
                words[0] = w0
            if w0 == "sudo":
                sudo = True
                words.pop(0)
                while words and words[0] == "-u":
                    words = words[2:]
                continue
            if w0 == "timeout":
                words.pop(0)
                if words and re.fullmatch(r"[0-9]+[smhd]?", words[0]):
                    words.pop(0)
                opw.append("timeout")
                continue
            if w0 in ("nohup", "command"):
                words.pop(0)
                opw.append(w0)
                continue
            if w0 == "env":
                words.pop(0)
                while words and _ASSIGN.match(words[0]):
                    k, v = words.pop(0).split("=", 1)
                    if (k, v) in HARMLESS_ENV:
                        opw.append("env")
                    else:
                        env.append((k, v))
                if not words:                         # bare `env`: the program itself (prints the environment)
                    words = ["env"]
                    break
                continue
            break
        prog = words[0] if words else ""
        return {"words": words, "prog": prog, "sudo": sudo, "env": env, "opw": opw,
                "redirs": st["redirs"], "args_after_prog": words[1:] if prog in SHELLS else []}

    def _shell_stdin(self, unwrapped, res, env=None):
        """Visible-literal sources for a shell that reads stdin. Returns (text, via, literal_vars) or
        (None, None, False) when the pipeline is a genuine fetch-and-run (curl | sh), which is a normal command
        pair, not opaque.

        Late-binding fixture (addendum section 6): an UNQUOTED heredoc (`<<EOF`) expands `$VAR`/`${VAR}` in its
        body using `env` as it stands when the heredoc is read (the resolver already threads the CURRENT env
        through); a QUOTED heredoc (`<<'EOF'`) never expands (body.quoted, carried by _HereBody) -- its `$NAME`
        tokens stay literal text even when the body is re-parsed as the nested shell's script (literal_vars=True,
        consumed by the caller around the nested `resolve()` call)."""
        env = {} if env is None else env
        last = unwrapped[-1]
        for op, t, body in last["redirs"]:
            if op == "<<<":
                return (t if t is not None else "") + "\n", ["HERESTRING-LIT"], False
            if op in ("<<", "<<-"):
                text = body or ""
                quoted = getattr(body, "quoted", True)
                if not quoted:
                    text = _expand_vars_in_text(text, env)
                return text, ["HEREDOC-LIT"], quoted
            if op == "<":
                if t in self.known_files:
                    return self.known_files[t], ["KNOWN-FILE"], False
                raise Opaque("redirect_exec")
        if len(unwrapped) == 1:
            raise Opaque("redirect_exec")             # bare shell on a terminal / unknown stdin
        # source chain
        chain = unwrapped[:-1]
        first = chain[0]
        text = None
        via = []
        i = 0
        if first["prog"] == "echo":
            a = first["words"][1:]
            if a and a[0] == "-n":
                a = a[1:]
            text, via, i = " ".join(a), ["PIPE-LIT"], 1
        elif first["prog"] == "printf":
            text, via, i = self._printf(first["words"][1:]), ["PIPE-LIT"], 1
        elif first["prog"] == "cat":
            paths = first["words"][1:]
            has_b64 = any(u["prog"] == "base64" for u in chain[1:])
            if len(paths) == 1 and paths[0] in self.known_files:
                text, via, i = self.known_files[paths[0]], ["KNOWN-FILE"], 1
            else:
                raise Opaque("b64_invisible" if has_b64 else "unknown_file")
        elif first["prog"] in ("curl", "wget"):
            if any(u["prog"] == "base64" for u in chain[1:]):
                raise Opaque("b64_invisible")         # fetched payload decoded: source not visible
            return None, None, False                  # fetch-and-run: handled as ordinary commands (E9)
        else:
            raise Opaque("redirect_exec")
        for u in chain[i:]:
            if u["prog"] == "base64" and u["words"][1:] == ["-d"]:
                text = self._b64(text)
                via = via + ["B64-LIT"]
            else:
                raise Opaque("redirect_exec")
        return text, via, False

    def _absorb(self, res, inner, sep, via):
        res.opaque.extend(inner.opaque)
        res.resolvers.extend(via + inner.resolvers)
        res.assign_stmts += inner.assign_stmts
        if inner.cmds:
            if inner.cmds[-1].sep is None:
                inner.cmds[-1].sep = sep
            for c in inner.cmds:
                c.via = list(via) + c.via
            res.cmds.extend(inner.cmds)


# ------------------------------------------------------------------------------------------------ words -> Cmd canon
def _units(program, words):
    """Split words (after program) into global flag units, sub, flag units, positional args using FLAG_ARITY."""
    arity = FLAG_ARITY.get(program, {})
    subs = SUBCOMMANDS.get(program)
    glob, flags, args, sub = [], [], [], ""
    i, n = 0, len(words)

    def take_flag(i):
        w = words[i]
        k = arity.get(w, 0)
        unit = words[i:i + 1 + k]
        return unit, i + 1 + k

    # leading flags (before the subcommand) are global flags when the program has subcommands
    if subs:
        while i < n and words[i].startswith("-"):
            u, i = take_flag(i)
            glob.append(u)
        for s in sorted(subs, key=lambda x: -len(x.split(" "))):
            sw = s.split(" ")
            if words[i:i + len(sw)] == sw:
                sub = s
                i += len(sw)
                break
    while i < n:
        w = words[i]
        if w.startswith("-") and len(w) > 1:
            u, i = take_flag(i)
            flags.append(u)
        else:
            args.append(w)
            i += 1
    if program == "git":
        glob = [u for u in glob if u != ["-C", "."]]          # `git -C .` is operator noise
    return glob, sub, flags, args


def rcmd_to_canon(rc):
    prog = rc.words[0]
    glob, sub, flags, args = _units(prog, rc.words[1:])
    return {"program": prog, "global": sorted(tuple(u) for u in glob), "sub": sub,
            "flags": sorted(tuple(u) for u in flags), "args": args, "sudo": bool(rc.sudo),
            "env": sorted(rc.env), "redirs": [tuple(r) for r in rc.redirs], "sep": rc.sep or ""}


def canon_of_resolution(res):
    return [rcmd_to_canon(c) for c in res.cmds]


def spec_canon(script):
    """Canonical command list of a spec Script, with every tuple form normalised like rcmd_to_canon."""
    out = []
    for d in script.canon():
        d = dict(d)
        if d.get("program") == "git":
            d["global"] = [u for u in d["global"] if tuple(u) != ("-C", ".")]
        d["global"] = [tuple(u) for u in d["global"]]
        d["flags"] = [tuple(u) for u in d["flags"]]
        d["env"] = [tuple(e) for e in d["env"]]
        d["redirs"] = [tuple(r) for r in d["redirs"]]
        out.append(d)
    return out


def roundtrip_equal(script, text, known_files=None):
    """K1 core: does the expander read `text` back to the spec's command list? Returns (ok, detail)."""
    res = Expander(known_files=known_files).resolve(text)
    if res.opaque:
        return False, "opaque:" + ",".join(res.opaque)
    a, b = spec_canon(script), canon_of_resolution(res)
    # a trailing separator mismatch can only come from an operator; compare strictly
    if a == b:
        return True, "ok"
    return False, "differs"


# ------------------------------------------------------------------------------------------------ shape (validators)
def shape(text):
    """Shape of every simple command as WRITTEN (no expansion): used to compare against tree-sitter-bash and
    mvdan/sh. -> list of {"name": src, "args": [src...], "stage": i, "n_in_pipeline": n, "sep": s}."""
    out = []
    for st in parse_script(text):
        if st.opaque:
            out.append({"opaque": st.opaque})
            continue
        for k, c in enumerate(st.pipeline):
            if not c.words:
                continue
            out.append({"name": c.words[0].src, "args": [w.src for w in c.words[1:]], "stage": k,
                        "n_in_pipeline": len(st.pipeline), "sep": st.sep if k == len(st.pipeline) - 1 else "|"})
    return out


_CAPABLE = re.compile(r"\$\(|`|<\(")


def has_opaque_capable_construct(text):
    """K19 numerator/denominator: the row contains `$(`, a redirection into a shell, control flow, or
    base64 -d into a shell."""
    if _CAPABLE.search(text):
        return True
    try:
        stmts = parse_script(text)
    except Opaque:
        return True
    for st in stmts:
        if st.opaque == "control_flow":
            return True
        if not st.pipeline:
            continue
        last = st.pipeline[-1]
        lw = [w.src for w in last.words]
        prog = lw[0] if lw else ""
        if prog in SHELLS and len(st.pipeline) > 1:
            return True
        if any(op in ("<<<", "<<", "<<-", "<") for op, _, _ in last.redirs) and prog in SHELLS:
            return True
        if prog in SHELLS and lw[1:2] == ["-c"]:
            continue
    return False
