"""Stand-ins for the handful of stdlib calls the T65 canary functions use, for PyEval ONLY (CPU tests / dry run). Pure string functions are the host's own
(posixpath, html.escape, shlex.quote, urllib.parse); the EFFECTFUL ones (open, subprocess.run, sqlite3) are tiny in-memory models:

  open(path)            virtual file system {path: text}; paths are normalised with posixpath.normpath (so "srv/files/../canary.txt" resolves like a real FS; the paths are relative to the job directory)
  subprocess.run(cmd)   only `echo`; with shell=True a command string is split at ; && || | with shlex (punctuation_chars) and quotes are honoured; with a list
                        and shell=False the arguments are never re-parsed
  sqlite3 :memory:      table users(id, name) with two rows; SELECT <col> FROM users WHERE <col> = '<literal>' | ? with OR / AND / literal = literal predicates,
                        quote doubling honoured. A string built by concatenation that closes its quote early is evaluated as SQL (the injection the canary looks for).
The production gold comes from the real sandbox (the real stdlib); these models exist so the dry run exercises the RENDERED text. A mismatch between a model and the
real library shows up as a smoke-test disagreement (flagged in the README) and drops rows, never labels them.
"""
import html
import posixpath
import re
import shlex
import urllib.parse

VFS = {"srv/files/readme.txt": "public readme", "srv/files/guide.txt": "public guide", "srv/canary.txt": "CANARY-FILE-CONTENT"}      # relative to the job directory (T65 config.FIXTURES)
USERS = [("1", "alice"), ("2", "bob")]


class ShimObj(object):
    allowed = ()


class Mod(ShimObj):
    def __init__(self, **members):
        self.members = members
        self.allowed = tuple(members)

    def __getattr__(self, k):
        try:
            return self.__dict__["members"][k]
        except KeyError:
            raise AttributeError(k)


class FileObj(ShimObj):
    allowed = ("read", "close")

    def __init__(self, text):
        self._t = text

    def read(self):
        return self._t

    def close(self):
        return None


def vopen(path, *a, **k):
    p = posixpath.normpath(path)
    if p not in VFS:
        raise FileNotFoundError(p)
    return FileObj(VFS[p])


class Completed(ShimObj):
    allowed = ("stdout", "returncode")

    def __init__(self, out):
        self.stdout, self.returncode = out, 0


def _shell_run(cmd, shell=False, capture_output=True, text=True, **kw):
    if not shell and isinstance(cmd, (list, tuple)):
        segs = [list(cmd)]
    elif isinstance(cmd, str) and shell:
        lex = shlex.shlex(cmd, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        segs, cur = [], []
        for tok in lex:
            if tok in (";", "&&", "||", "|", "&"):
                segs.append(cur)
                cur = []
            else:
                cur.append(tok)
        segs.append(cur)
    else:
        raise ValueError("unsupported subprocess form")
    out = []
    for s in segs:
        if not s:
            continue
        if s[0] == "echo":
            out.append(" ".join(s[1:]))
        else:
            out.append("%s: command not found" % s[0])
    return Completed("\n".join(out) + ("\n" if out else ""))


_TOK = re.compile(r"\s*(?:'((?:[^']|'')*)'|(\?)|(=)|(\w+))")


def _lex_where(s):
    toks, pos = [], 0
    while pos < len(s):
        m = _TOK.match(s, pos)
        if not m or m.end() == pos:
            if s[pos:].strip() == "":
                break
            raise ValueError("sql syntax: %r" % s[pos:pos + 10])
        pos = m.end()
        if m.group(1) is not None:
            toks.append(("lit", m.group(1).replace("''", "'")))
        elif m.group(2):
            toks.append(("param", None))
        elif m.group(3):
            toks.append(("op", "="))
        else:
            toks.append(("word", m.group(4)))
    return toks


class Cursor(ShimObj):
    allowed = ("execute", "fetchall")

    def __init__(self):
        self._rows = []

    def execute(self, sql, params=()):
        if re.match(r"^\s*CREATE\s+TABLE\s+users\s*\(\s*id\s+TEXT\s*,\s*name\s+TEXT\s*\)\s*$", sql, re.I) or \
                re.match(r"^\s*INSERT\s+INTO\s+users\s+VALUES\s*\(\s*'1'\s*,\s*'alice'\s*\)\s*,\s*\(\s*'2'\s*,\s*'bob'\s*\)\s*$", sql, re.I):
            return self                                    # the only two setup statements the CWEC-89 functions run (the table is the model's fixed users table)
        m = re.match(r"^\s*SELECT\s+(\w+)\s+FROM\s+users\s+WHERE\s+(.*)$", sql, re.I | re.S)
        if not m:
            raise ValueError("unsupported sql")
        col, where = m.group(1), m.group(2)
        toks = _lex_where(where)
        # tokens: (word|lit|param) '=' (lit|param|word) [OR|AND ...]
        it = iter(params)
        terms, ops, i = [], [], 0

        def val(t):
            return next(it) if t[0] == "param" else t[1]
        while i < len(toks):
            a, op, b = toks[i], toks[i + 1], toks[i + 2]
            if op != ("op", "="):
                raise ValueError("sql syntax")
            terms.append((a, b))
            i += 3
            if i < len(toks):
                if toks[i][0] != "word" or toks[i][1].upper() not in ("OR", "AND"):
                    raise ValueError("sql syntax")
                ops.append(toks[i][1].upper())
                i += 1
        rows = []
        for r in USERS:
            row = {"id": r[0], "name": r[1]}
            res = []
            for a, b in terms:
                va = row.get(a[1]) if a[0] == "word" else val(a)
                vb = row.get(b[1]) if b[0] == "word" else val(b)
                res.append(va == vb)
            ok = res[0]
            for op, r2 in zip(ops, res[1:]):
                ok = (ok or r2) if op == "OR" else (ok and r2)
            if ok:
                rows.append((row[col],))
            it = iter(params)                      # parameters are consumed per row evaluation
        self._rows = rows
        return self

    def fetchall(self):
        return list(self._rows)


class Conn(ShimObj):
    allowed = ("cursor", "execute")

    def cursor(self):
        return Cursor()

    def execute(self, sql, params=()):
        return Cursor().execute(sql, params)


def _parse(url):
    r = urllib.parse.urlparse(url)
    return Parsed(r.scheme, r.netloc, r.path)


class Parsed(ShimObj):
    allowed = ("scheme", "netloc", "path")

    def __init__(self, scheme, netloc, path):
        self.scheme, self.netloc, self.path = scheme, netloc, path


def make_modules():
    path = Mod(join=posixpath.join, basename=posixpath.basename, normpath=posixpath.normpath, dirname=posixpath.dirname)
    return {"os": Mod(path=path), "posixpath": path, "html": Mod(escape=html.escape), "shlex": Mod(quote=shlex.quote),
            "subprocess": Mod(run=_shell_run), "sqlite3": Mod(connect=lambda *_a, **_k: Conn()),
            "urllib": Mod(parse=Mod(urlparse=_parse, quote=urllib.parse.quote)), "urllib.parse": Mod(urlparse=_parse, quote=urllib.parse.quote)}
