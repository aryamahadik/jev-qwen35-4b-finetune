"""Solver B string-side shell reader (T50 / T51 / T53).

Written by the solver-B session from the G0-lite text and the row schema ONLY. It shares no code with solver A, the
LA_COMMON expander, the LA_COMMON renderer or the LA_COMMON shell model. It never executes anything: it only
turns a rendered command string into a list of resolved simple commands (argv words), and it says when the string
is NOT resolvable (the opaque rule R19).

Method (deliberately different from a structured-spec solver): a character-level lexer builds words out of
segments (literal / single-quoted / double-quoted / parameter / command substitution), then a small
interpreter walks the statements in order, keeping a shell-variable environment, doing brace expansion,
parameter expansion, IFS field splitting and glob expansion against a caller-supplied filename list, resolving
only the substitution forms the G0-lite resolver list allows (base64 decode of a VISIBLE literal), and
recursing into `sh -c`, decoded payloads and write-then-run files whose content is known.

Public API:
    read_script(text, known_files=None, glob_fn=None, depth=0) -> Reading
    Reading.units : list[Unit]    resolved simple commands in order (pipelines flattened, `sep` = separator after)
    Reading.opaque : list[str]    opaque kinds met (cmdsub | redirect_exec | control_flow | unknown_file |
                                  b64_invisible | xargs_dynamic | background)
    Reading.notes : list[str]     decode / write-then-run events (names only)
"""
import base64
import binascii
import re
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

MAX_DEPTH = 4

# programs written with an absolute path in a rendering (basename is the program)
_ABS_BASE = re.compile(r"^/(?:usr/local/bin|usr/bin|bin|sbin|usr/sbin)/([A-Za-z0-9_+.-]+)$")
WRAPPERS_NOARG = ("nohup", "command")
SHELLS = ("sh", "bash")
KEYWORDS = ("if", "then", "else", "elif", "fi", "for", "while", "until", "do", "done", "case", "esac", "select",
            "function", "{", "}", "(", ")", "!", "time")


class Opaque(Exception):
    def __init__(self, kind):
        super().__init__(kind)
        self.kind = kind


# ------------------------------------------------------------------------------------------------ data
@dataclass
class Seg:
    kind: str            # lit | sq | dq | param | cmdsub
    text: str            # lit/sq/dq literal text, param name+operator, cmdsub inner text
    quoted: bool = False  # for param / cmdsub: inside double quotes


@dataclass
class Unit:
    argv: List[str]                       # program word first (wrappers, sudo and abs path already normalised away)
    assigns: List[Tuple[str, str]] = field(default_factory=list)
    redirs: List[Tuple[str, str]] = field(default_factory=list)
    sudo: bool = False
    wrappers: List[str] = field(default_factory=list)
    sep: Optional[str] = None            # separator AFTER this unit: ; && || | or None
    raw_program: str = ""
    glob_words: List[str] = field(default_factory=list)   # words that were unquoted glob patterns (before expansion)
    origin: str = "direct"               # direct | decoded | script | shc

    @property
    def prog(self):
        return self.argv[0] if self.argv else ""

    @property
    def rest(self):
        return self.argv[1:]


@dataclass
class Reading:
    units: List[Unit] = field(default_factory=list)
    opaque: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    fetch_exec: List[str] = field(default_factory=list)   # urls fetched into a shell (curl|sh, wget -qO-|sh)
    ok: bool = True
    tilde_unresolved: bool = False                        # an unquoted word-initial ~ was met and no home path is shown


# ------------------------------------------------------------------------------------------------ lexer
_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_PARAM_OPS = (":-", ":=", ":+", ":?", "-", "+")


def _find_close_paren(s, i):
    """s[i] is just after '$('. Return index of the matching ')' (quote aware) or -1."""
    depth = 1
    n = len(s)
    while i < n:
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "'":
            j = s.find("'", i + 1)
            if j < 0:
                return -1
            i = j + 1
            continue
        if c == '"':
            i += 1
            while i < n and s[i] != '"':
                if s[i] == "\\":
                    i += 1
                elif s[i] == "$" and i + 1 < n and s[i + 1] == "(":
                    k = _find_close_paren(s, i + 2)
                    if k < 0:
                        return -1
                    i = k
                i += 1
            i += 1
            continue
        if c == "$" and i + 1 < n and s[i + 1] == "(":
            k = _find_close_paren(s, i + 2)
            if k < 0:
                return -1
            i = k + 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _lex_param(s, i):
    """s[i] == '$'. Returns (Seg or None, next_index). None = a literal '$'."""
    n = len(s)
    if i + 1 >= n:
        return None, i + 1
    c = s[i + 1]
    if c == "(":
        k = _find_close_paren(s, i + 2)
        if k < 0:
            raise Opaque("cmdsub")
        return Seg("cmdsub", s[i + 2:k]), k + 1
    if c == "{":
        k = s.find("}", i + 2)
        if k < 0:
            raise Opaque("cmdsub")
        return Seg("param", s[i + 2:k]), k + 1
    m = _NAME.match(s, i + 1)
    if m:
        return Seg("param", m.group(0)), m.end()
    return None, i + 1


def lex(s):
    """-> list of tokens: ('word', [Seg...]) | ('op', str) | ('redir', op, fdprefix). Raises Opaque."""
    toks = []
    i, n = 0, len(s)
    segs: List[Seg] = []

    def flush():
        nonlocal segs
        if segs:
            toks.append(("word", segs))
            segs = []

    def add_lit(t):
        if segs and segs[-1].kind == "lit" and not segs[-1].quoted:
            segs[-1].text += t
        else:
            segs.append(Seg("lit", t))

    while i < n:
        c = s[i]
        if c in " \t":
            flush()
            i += 1
        elif c == "\n":
            flush()
            toks.append(("op", ";"))
            i += 1
        elif c == "#" and not segs:
            while i < n and s[i] != "\n":
                i += 1
        elif c == "\\":
            if i + 1 < n:
                if s[i + 1] == "\n":
                    i += 2
                    continue
                segs.append(Seg("sq", s[i + 1]))
                i += 2
            else:
                i += 1
        elif c == "'":
            j = s.find("'", i + 1)
            if j < 0:
                raise Opaque("control_flow")
            segs.append(Seg("sq", s[i + 1:j]))
            i = j + 1
        elif c == '"':
            i += 1
            buf = []
            parts: List[Seg] = []
            while True:
                if i >= n:
                    raise Opaque("control_flow")
                d = s[i]
                if d == '"':
                    i += 1
                    break
                if d == "\\" and i + 1 < n and s[i + 1] in '$"\\`\n':
                    if s[i + 1] != "\n":
                        buf.append(s[i + 1])
                    i += 2
                elif d == "$":
                    seg, j = _lex_param(s, i)
                    if seg is None:
                        buf.append("$")
                        i = j
                    else:
                        if buf:
                            parts.append(Seg("dq", "".join(buf)))
                            buf = []
                        seg.quoted = True
                        parts.append(seg)
                        i = j
                elif d == "`":
                    raise Opaque("cmdsub")
                else:
                    buf.append(d)
                    i += 1
            if buf:
                parts.append(Seg("dq", "".join(buf)))
            if not parts:
                parts.append(Seg("dq", ""))
            segs.extend(parts)
        elif c == "$":
            seg, j = _lex_param(s, i)
            if seg is None:
                add_lit("$")
                i = j
            else:
                segs.append(seg)
                i = j
        elif c == "`":
            raise Opaque("cmdsub")
        elif c in ";|&":
            flush()
            two = s[i:i + 2]
            if two in ("&&", "||"):
                toks.append(("op", two))
                i += 2
            elif c == "&":
                toks.append(("op", "&"))
                i += 1
            else:
                toks.append(("op", c))
                i += 1
        elif c in "<>":
            # an adjacent fd prefix (digits, entire current word) belongs to the redirection
            fd = ""
            if segs and len(segs) == 1 and segs[0].kind == "lit" and segs[0].text.isdigit():
                fd = segs[0].text
                segs = []
            else:
                flush()
            for op in ("<<<", "<<", ">>", ">&", "<&", ">", "<"):
                if s.startswith(op, i):
                    break
            toks.append(("redir", op, fd))
            i += len(op)
        elif c in "()":
            flush()
            toks.append(("op", c))
            i += 1
        else:
            add_lit(c)
            i += 1
    flush()
    return toks


# ------------------------------------------------------------------------------------------------ brace / glob / split
def _brace_expand(word):
    """Expand a{b,c}d (comma lists only). Returns list of strings."""
    k = word.find("{")
    if k < 0:
        return [word]
    depth = 0
    j = k
    commas = []
    while j < len(word):
        ch = word[j]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                break
        elif ch == "," and depth == 1:
            commas.append(j)
        j += 1
    if j >= len(word) or not commas:
        return [word]
    pre, post = word[:k], word[j + 1:]
    cuts = [k] + commas + [j]
    out = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        for tail in _brace_expand(post):
            for mid in _brace_expand(word[a + 1:b]):
                out.append(pre + mid + tail)
    return out


def glob_to_re(pat):
    out = ["^"]
    i = 0
    while i < len(pat):
        c = pat[i]
        if c == "*":
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        elif c == "[":
            j = pat.find("]", i + 1)
            if j < 0:
                out.append(re.escape(c))
            else:
                body = pat[i + 1:j]
                if body.startswith("!"):
                    body = "^" + body[1:]
                out.append("[" + body + "]")
                i = j
        else:
            out.append(re.escape(c))
        i += 1
    out.append("$")
    return re.compile("".join(out))


def default_glob(pattern, names):
    """Bash-like single-directory glob over an iterable of absolute names."""
    d, _, base = pattern.rpartition("/")
    rx = glob_to_re(base)
    out = []
    for nm in sorted(names):
        dd, _, bb = nm.rpartition("/")
        if dd != d:
            continue
        if bb.startswith(".") and not base.startswith("."):
            continue
        if rx.match(bb):
            out.append(nm)
    return out


# ------------------------------------------------------------------------------------------------ interpreter
class _Interp:
    def __init__(self, known_files, glob_fn, depth, rd):
        self.known = known_files or {}
        self.glob_fn = glob_fn
        self.depth = depth
        self.env: Dict[str, str] = {}
        self.rd = rd
        self.fetched: Dict[str, str] = {}      # path -> url written by an earlier curl -o / wget -O in this string
        self.aliases: Dict[str, str] = {}      # alias name -> body (the LAST definition decides: late binding)
        self.traps: List[str] = []             # EXIT trap bodies, run after the last statement with the FINAL environment
        self.heredocs: Dict[str, Tuple[str, bool]] = {}   # placeholder -> (body, delimiter quoted?)
        self.unset_hit = False                 # a parameter expansion met an unset variable

    # ---- expansion -------------------------------------------------------------------------------
    def _param(self, name):
        if _NAME.fullmatch(name) and name not in self.env:
            self.unset_hit = True
            if name == "HOME":
                raise Opaque("unresolved_binding")           # $HOME is not in the resolver list (Opus Q11)
        for op in _PARAM_OPS:
            k = name.find(op)
            if k > 0 and _NAME.fullmatch(name[:k]):
                var, default = name[:k], name[k + len(op):]
                val = self.env.get(var)
                if op in (":-", "-"):
                    return val if (val not in (None, "") or (op == "-" and val is not None)) else default
                if op in (":+", "+"):
                    return default if val else ""
                if op == ":=":
                    if not val:
                        self.env[var] = default
                        return default
                    return val
                return val or ""
        return self.env.get(name, "")

    def _cmdsub(self, inner):
        """Resolver list: only `echo LIT | base64 -d` (visible literal). Anything else is opaque."""
        try:
            toks = lex(inner)
        except Opaque:
            raise Opaque("cmdsub")
        stages, cur = [], []
        for t in toks:
            if t[0] == "op" and t[1] == "|":
                stages.append(cur)
                cur = []
            elif t[0] == "word":
                cur.append(t[1])
            else:
                raise Opaque("cmdsub")
        stages.append(cur)
        if len(stages) != 2:
            raise Opaque("cmdsub")
        a = [self._join_plain(w) for w in stages[0]]
        b = [self._join_plain(w) for w in stages[1]]
        if len(a) == 2 and a[0] == "echo" and b[:1] == ["base64"] and set(b[1:]) <= {"-d", "--decode", "-D"} and len(b) >= 2:
            try:
                txt = base64.b64decode(a[1], validate=True).decode("utf-8")
            except (binascii.Error, ValueError, UnicodeDecodeError):
                raise Opaque("b64_invisible")
            self.rd.notes.append("b64_cmdsub")
            return txt.rstrip("\n")
        raise Opaque("cmdsub")

    def _join_plain(self, segs):
        """Literal-only join (used for the resolver-list check); a param in there reads the env."""
        out = []
        for sg in segs:
            if sg.kind in ("lit", "sq", "dq"):
                out.append(sg.text)
            elif sg.kind == "param":
                out.append(self._param(sg.text))
            else:
                raise Opaque("cmdsub")
        return "".join(out)

    def expand_word(self, segs):
        """-> (fields: list[str], globbed: bool, pattern_words: list[str]).

        Unquoted literal text is subject to brace expansion; unquoted parameter / substitution results are
        subject to IFS field splitting; any resulting field with an unquoted glob character is matched
        against the supplied name list."""
        # build a list of (text, splittable, globbable) pieces
        pieces = []
        for k, sg in enumerate(segs):
            if sg.kind == "lit":
                text = sg.text
                if k == 0 and text.startswith("~") and (len(text) == 1 or text[1] == "/"):
                    # Opus Q12.2: an UNQUOTED ~ that begins a word (also after a flag) is the registered home alias form: it resolves
                    # through the SHOWN home path; without one it does not resolve (R19). A quoted ~ and an attached / mid-word ~
                    # stay literal.
                    if self.env.get("HOME"):
                        text = self.env["HOME"].rstrip("/") + text[1:]
                    else:
                        self.rd.tilde_unresolved = True
                pieces.append((text, False, True))
            elif sg.kind in ("sq", "dq"):
                pieces.append((sg.text, False, False))
            elif sg.kind == "param":
                pieces.append((self._param(sg.text), not sg.quoted, not sg.quoted))
            elif sg.kind == "cmdsub":
                pieces.append((self._cmdsub(sg.text), not sg.quoted, not sg.quoted))
        # brace expansion only when the word is a single unquoted literal run
        if len(pieces) == 1 and pieces[0][2] and not pieces[0][1] and "{" in pieces[0][0] and "," in pieces[0][0]:
            alts = _brace_expand(pieces[0][0])
            fields, glob_words = [], []
            for a in alts:
                f, gw = self._finish_fields([(a, False, True)])
                fields += f
                glob_words += gw
            return fields, glob_words
        return self._finish_fields(pieces)

    def _finish_fields(self, pieces):
        ifs = self.env.get("IFS", " \t\n")
        fields = [[]]
        forced = [False]
        for text, splittable, globbable in pieces:
            if not splittable:
                if not globbable:
                    forced[-1] = True
                for ch in text:
                    fields[-1].append((ch, globbable))
            else:
                for ch in text:
                    if ch in ifs:
                        if not fields[-1] and not forced[-1]:
                            continue
                        fields.append([])
                        forced.append(False)
                    else:
                        fields[-1].append((ch, globbable))
        out, glob_words = [], []
        for f, fz in zip(fields, forced):
            if not f and not fz:
                continue
            word = "".join(c for c, _ in f)
            if any(g and c in "*?[" for c, g in f):
                glob_words.append(word)
                matches = self.glob_fn(word) if self.glob_fn else []
                out.extend(matches if matches else [word])
            else:
                out.append(word)
        return out, glob_words

    # ---- statements ------------------------------------------------------------------------------
    def _extract_heredocs(self, text):
        """`CMD <<[-]DELIM` + body lines + DELIM line -> `CMD <<< __HDn__`; the body is expanded where the command runs
        (unquoted DELIM: the parent shell expands $VAR at that point; quoted DELIM: the body stays literal)."""
        lines = text.split("\n")
        out, i, n = [], 0, 0
        while i < len(lines):
            ln = lines[i]
            m = re.search(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", ln)
            if m and "<<<" not in ln:
                delim, quoted = m.group(2), bool(m.group(1))
                body, j = [], i + 1
                while j < len(lines) and lines[j].strip() != delim:
                    body.append(lines[j])
                    j += 1
                if j >= len(lines):
                    raise Opaque("control_flow")             # unterminated heredoc
                key = "__HD%d__" % n
                n += 1
                self.heredocs[key] = ("\n".join(body), quoted)
                out.append(ln[:m.start()] + "<<< " + key + ln[m.end():])
                i = j + 1
                continue
            out.append(ln)
            i += 1
        return "\n".join(out)

    def _expand_text(self, body):
        return re.sub(r"\$(?:\{(\w+)\}|(\w+))", lambda m: self.env.get(m.group(1) or m.group(2), ""), body)

    def evaluate(self, text):
        if "<<" in text:
            text = self._extract_heredocs(text)
        toks = lex(text)
        # split into simple commands with the operator that FOLLOWS each one
        cmds = []          # (words(list of segs), redirs(list), sep)
        cur_words, cur_redirs = [], []
        i = 0
        while i < len(toks):
            t = toks[i]
            if t[0] == "word":
                cur_words.append(t[1])
            elif t[0] == "redir":
                if i + 1 >= len(toks) or toks[i + 1][0] != "word":
                    # `2>&1` style: the target digit lexes as a word, so a missing word means malformed
                    raise Opaque("control_flow")
                cur_redirs.append((t[2] + t[1], toks[i + 1][1]))
                i += 1
            else:
                op = t[1]
                if op in ("(", ")"):
                    raise Opaque("control_flow")
                if op == "&":
                    raise Opaque("background")
                if cur_words or cur_redirs:
                    cmds.append((cur_words, cur_redirs, op))
                    cur_words, cur_redirs = [], []
                elif op != ";":
                    raise Opaque("control_flow")
            i += 1
        if cur_words or cur_redirs:
            cmds.append((cur_words, cur_redirs, None))
        return self._interpret(cmds)

    def _is_assign(self, segs):
        if not segs or segs[0].kind != "lit":
            return None
        m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)=", segs[0].text)
        if not m:
            return None
        return m.group(1), len(m.group(0))

    def _assign_value(self, segs, skip):
        """Value of NAME=value (no field splitting, no globbing)."""
        out = []
        first = True
        for sg in segs:
            if first and sg.kind == "lit":
                out.append(sg.text[skip:])
                first = False
                continue
            first = False
            if sg.kind in ("lit", "sq", "dq"):
                out.append(sg.text)
            elif sg.kind == "param":
                out.append(self._param(sg.text))
            else:
                out.append(self._cmdsub(sg.text))
        return "".join(out)

    def _interpret(self, cmds):
        rd = self.rd
        # first pass: expand each command into (argv, assigns, redirs, sep)
        resolved = []
        for words, redirs, sep in cmds:
            assigns = []
            idx = 0
            while idx < len(words):
                a = self._is_assign(words[idx])
                if a is None:
                    break
                name, skip = a
                val = self._assign_value(words[idx], skip)
                assigns.append((name, val))
                idx += 1
            body = words[idx:]
            red_out = []
            for op, tw in redirs:
                f, _ = self.expand_word(tw)
                tgt = f[0] if f else ""
                if op == "<<<" and tgt in self.heredocs:
                    hb, quoted = self.heredocs[tgt]
                    tgt = hb if quoted else self._expand_text(hb)
                red_out.append((op, tgt))
            if not body:
                for k, v in assigns:
                    self.env[k] = v
                resolved.append(("assign", sep))
                continue
            self.unset_hit = False
            argv, gw = [], []
            for w in body:
                f, g = self.expand_word(w)
                argv.extend(f)
                gw.extend(g)
            if argv and argv[0] in KEYWORDS:
                raise Opaque("control_flow")
            if argv and argv[0] == "trap" and len(argv) >= 3:
                # `trap 'BODY' EXIT`: BODY (single-quoted) is read at exit with the FINAL environment; a double-quoted BODY
                # was expanded now, and an unset variable in it cannot be resolved (R19)
                if self.unset_hit or any(x not in ("EXIT", "0") for x in argv[2:]):
                    raise Opaque("unresolved_binding")
                self.traps.append(argv[1])
                resolved.append(("assign", sep))
                continue
            if argv and argv[0] == "alias" and len(argv) >= 2 and all("=" in x for x in argv[1:]):
                for x in argv[1:]:
                    k, _, v = x.partition("=")
                    self.aliases[k] = v
                resolved.append(("assign", sep))
                continue
            if argv and argv[0] in self.aliases:
                # alias call: the definition in force NOW (the last one) replaces the word
                toks_a = lex(self.aliases[argv[0]])
                if any(t[0] != "word" for t in toks_a):
                    raise Opaque("control_flow")
                new = []
                for t in toks_a:
                    f, g = self.expand_word(t[1])
                    new.extend(f)
                    gw.extend(g)
                argv = new + argv[1:]
            resolved.append((argv, assigns, red_out, sep, gw))
        # second pass: build pipelines / units
        units: List[Unit] = []
        i = 0
        while i < len(resolved):
            r = resolved[i]
            if r[0] == "assign":
                if units and r[1] is not None:
                    # propagate the separator of the bare assignment to the previous unit when it had none
                    if units[-1].sep is None:
                        units[-1].sep = r[1]
                i += 1
                continue
            # gather a pipeline [i .. j]
            j = i
            while j < len(resolved) and resolved[j][0] != "assign" and resolved[j][3] == "|":
                j += 1
            if j >= len(resolved) or resolved[j][0] == "assign":
                j = min(j, len(resolved) - 1)
            pipe = [x for x in resolved[i:j + 1] if x[0] != "assign"]
            self._emit_pipeline(pipe, units)
            i = j + 1
        for body in self.traps:
            tu = self._recurse_units(body, None, origin="trap", env=dict(self.env))
            if units and units[-1].sep is None:
                units[-1].sep = ";"
            units.extend(tu)
        return units

    def _norm(self, argv, assigns, redirs, sep, gw):
        """Strip operator wrappers / sudo / absolute binary path / git -C . ; return Unit."""
        u = Unit(argv=list(argv), assigns=list(assigns), redirs=list(redirs), sep=sep, glob_words=list(gw))
        a = u.argv
        changed = True
        while changed and a:
            changed = False
            m = _ABS_BASE.match(a[0])
            if m:
                u.raw_program = a[0]
                a[0] = m.group(1)
                changed = True
            if a[0] in WRAPPERS_NOARG and len(a) > 1:
                u.wrappers.append(a.pop(0))
                changed = True
            elif a[0] == "timeout" and len(a) > 2 and re.fullmatch(r"\d+[smhd]?", a[1]):
                u.wrappers.append("timeout")
                del a[0:2]
                changed = True
            elif a[0] == "env" and len(a) > 1:
                u.wrappers.append("env")
                a.pop(0)
                while a and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", a[0]):
                    k, _, v = a.pop(0).partition("=")
                    u.assigns.append((k, v))
                changed = True
            elif a[0] == "sudo" and len(a) > 1:
                u.sudo = True
                a.pop(0)
                while a and a[0].startswith("-"):
                    if a[0] == "-u" and len(a) > 1:
                        del a[0:2]
                    else:
                        a.pop(0)
                changed = True
        if a and a[0] == "git":
            # `git -C <dir>` is a no-op wrapper in this corpus only for `.`
            k = 1
            while k + 1 < len(a) and a[k] == "-C" and a[k + 1] == ".":
                del a[k:k + 2]
        return u

    def _emit_pipeline(self, pipe, units):
        # pipeline of normalised units
        nus = []
        for argv, assigns, redirs, sep, gw in pipe:
            if not argv:
                continue
            nus.append(self._norm(argv, assigns, redirs, sep, gw))
        if not nus:
            return
        for x in nus:
            if x.prog in ("curl", "wget"):
                flag = "-o" if x.prog == "curl" else "-O"
                if flag in x.rest and x.rest.index(flag) + 1 < len(x.rest):
                    urls = [w for w in x.rest if re.match(r"^[a-z]+://", w)]
                    self.fetched[x.rest[x.rest.index(flag) + 1]] = urls[0] if urls else ""
        last_sep = pipe[-1][3]
        # shell at the end of a pipeline: payload comes from the previous stage
        if len(nus) >= 2 and nus[-1].prog in SHELLS and not nus[-1].rest:
            src = nus[:-1]
            if any(x.prog == "xargs" for x in src):
                raise Opaque("xargs_dynamic")
            if len(src) == 2 and src[0].prog == "echo" and len(src[0].rest) == 1 and src[1].prog == "base64" \
                    and set(src[1].rest) <= {"-d", "--decode", "-D"} and src[1].rest:
                try:
                    dec = base64.b64decode(src[0].rest[0], validate=True).decode("utf-8")
                except (binascii.Error, ValueError, UnicodeDecodeError):
                    raise Opaque("b64_invisible")
                self.rd.notes.append("b64_pipe")
                us = self._recurse_units(dec, last_sep, origin="decoded")
                if us and us[-1].sep is None:
                    us[-1].sep = last_sep
                units.extend(us)
                return
            if len(src) == 1 and src[0].prog in ("curl", "wget"):
                url = [w for w in src[0].rest if re.match(r"^[a-z]+://", w)]
                self.rd.fetch_exec.extend(url or [""])
                src[0].origin = "fetch_exec"
                src[0].sep = None
                units.append(src[0])
                nus[-1].sep = last_sep
                units.append(nus[-1])
                nus[-1].origin = "fetch_exec_shell"
                return
            # payload not visible
            raise Opaque("b64_invisible" if any(x.prog == "base64" for x in src) else "cmdsub")
        for x in nus:
            if x.prog == "xargs":
                raise Opaque("xargs_dynamic")
        for k, x in enumerate(nus):
            x.sep = "|" if k < len(nus) - 1 else last_sep
        # shell invocations in the middle are resolved individually
        out_units = []
        for x in nus:
            if x.prog in SHELLS:
                sub = self._run_shell(x)
                if sub is None:
                    out_units.append(x)
                else:
                    sub_units, tail_sep = sub
                    if sub_units:
                        sub_units[-1].sep = x.sep if sub_units[-1].sep is None else sub_units[-1].sep
                    out_units.extend(sub_units)
            else:
                # running a script by path
                if "/" in x.prog and re.search(r"\.(sh|bash)$", x.prog):
                    sh = Unit(argv=["sh", x.prog] + x.rest, sep=x.sep)
                    sub = self._run_shell(sh)
                    out_units.extend(sub[0] if sub else [x])
                else:
                    out_units.append(x)
        units.extend(out_units)

    def _run_shell(self, x):
        """Resolve `sh -c STR`, `sh FILE`, `sh < FILE`. Returns (units, sep) or None when the unit stays as is."""
        if x.redirs:
            ops = [op for op, _ in x.redirs]
            if any(op in ("<", "<<") for op in ops):
                raise Opaque("redirect_exec")
            if "<<<" in ops:
                lit = [t for op, t in x.redirs if op == "<<<"][0]
                return self._recurse_units(lit, x.sep), x.sep
        rest = x.rest
        if rest and rest[0] == "-c" and len(rest) >= 2:
            return self._recurse_units(rest[1], x.sep), x.sep
        files = [w for w in rest if not w.startswith("-")]
        if files:
            path = files[0]
            if path in self.fetched:
                self.rd.fetch_exec.append(self.fetched[path])
                self.rd.notes.append("fetched_then_run")
                return [], x.sep
            if path in self.known:
                self.rd.notes.append("script_known")
                return self._recurse_units(self.known[path], x.sep, origin="script"), x.sep
            raise Opaque("unknown_file")
        raise Opaque("unknown_file")

    def _recurse_units(self, text, sep, origin="shc", env=None):
        if self.depth >= MAX_DEPTH:
            raise Opaque("control_flow")
        sub_rd = Reading()
        child = _Interp(self.known, self.glob_fn, self.depth + 1, sub_rd)
        if "HOME" in self.env:
            child.env["HOME"] = self.env["HOME"]               # the login environment's HOME reaches `sh -c` / scripts
        if env:
            child.env.update(env)
        us = child.evaluate(text)
        self.rd.notes.extend(sub_rd.notes)
        self.rd.tilde_unresolved = self.rd.tilde_unresolved or sub_rd.tilde_unresolved
        self.rd.fetch_exec.extend(sub_rd.fetch_exec)
        for u in us:
            if u.origin == "direct":
                u.origin = origin
        return us


def read_script(text, known_files=None, glob_fn=None, env=None):
    """Read one rendered command string. Never raises: opacity is reported in Reading.opaque. `env` seeds the shell variables
    (HOME from the simulated state: an unquoted leading ~ and $HOME expand to it)."""
    rd = Reading()
    it = _Interp(known_files, glob_fn, 0, rd)
    if env:
        it.env.update(env)
    try:
        rd.units = it.evaluate(text)
    except Opaque as e:
        rd.opaque.append(e.kind)
        rd.ok = False
        rd.units = []
    return rd
