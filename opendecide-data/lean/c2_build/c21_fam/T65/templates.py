"""T65 program templates (spec -> Python source) and SOLVER A (the static-taint label function over the spec).

Spec (G0-lite 2.1): class, a SOURCE (the parameter the spec marks attacker-controlled, or a constant for NS-3), 0-2 benign TRANSFORMS (strip, lower, format into
a larger string, put in and read from a container), at most one NEUTRALISING step of kind san in {valid, allowlist, helper, param_api} (VALID) or a DECOY
{wrong_class DS-2, wrong_var DS-1, after_sink DS-3, branch DS-4, discarded DS-5, overwritten DS-6}, and a class-specific SINK.

LABEL FUNCTION (solver A): YES iff a SOURCE-to-SINK flow exists and no neutralising step VALID for that class and that flow lies on every path before the sink. A step
is valid only if (1) it is of the sink's own class, (2) applied to the value that reaches the sink, (3) executed before the sink on all paths, (4) its result used.
Static-only classes (295, 327, 377): YES iff the flagged API use is present at the point the value is used and no valid step undoes it.
Code is produced by program templates only (no model writes, labels or checks a row); every identifier is drawn from the seeded namespace by the caller.
"""
import copy

from . import config as C

# conditions of a neutralising step: (own class, applied to the flow value, before the sink on all paths, result used)
COND = {"valid": (1, 1, 1, 1), "allowlist": (1, 1, 1, 1), "helper": (1, 1, 1, 1), "param_api": (1, 1, 1, 1), "wrong_class": (0, 1, 1, 1), "wrong_var": (1, 0, 1, 1),
        "after_sink": (1, 1, 0, 1), "branch": (1, 1, 0, 1), "discarded": (1, 1, 1, 0), "overwritten": (1, 1, 1, 0)}
DS_OF = {"wrong_var": "DS-1", "wrong_class": "DS-2", "after_sink": "DS-3", "branch": "DS-4", "discarded": "DS-5", "overwritten": "DS-6"}
NS_OF = {"helper": "NS-1", "allowlist": "NS-2", "param_api": "NS-4"}
SAN = {"CWEC-22": 'os.path.basename({v})', "CWEC-78": "shlex.quote({v})", "CWEC-79": "html.escape({v})", "CWEC-89": '{v}.replace("\'", "\'\'")',
       "CWEC-117": '{v}.replace("\\n", " ")', "CWEC-601": '"/" + {v}.lstrip("/")'}
WRONG = {"CWEC-79": "shlex.quote({v})", "CWEC-117": "shlex.quote({v})"}
WRONG_DEFAULT = "html.escape({v}, quote=False)"
IMPORT_OF = {"os.path": "import os", "shlex": "import shlex", "html": "import html", "subprocess": "import subprocess", "sqlite3": "import sqlite3"}


def valid_step(neut):
    return bool(neut) and not neut.get("identity") and all(COND[neut["san"]])


def label_spec(spec):
    """SOLVER A. The spec carries the facts; the validity table above carries the rule."""
    if spec["cls"] in C.STATIC:
        return label_static(spec)
    if spec["source"] != "param":
        return "NO"                                          # NS-3: the value is not attacker-controlled
    n = spec.get("neut")
    return "NO" if valid_step(n) else "YES"


def label_static(spec):
    """Abstract run over the spec's state: the flagged state is present at the use unless a valid step undoes it."""
    if spec["cls"] == "CWEC-327":
        if spec["role"] != "password":
            return "NO"
    elif spec.get("flagged") is False:
        return "NO"
    n = spec.get("neut")
    if n is None:
        return "YES" if spec.get("flagged", True) else "NO"
    return "NO" if valid_step(n) else "YES"


# ---- rendering -------------------------------------------------------------------------------------------------------------------------
def _san(spec, v):
    return SAN[spec["cls"]].format(v=v)


def _wrong(spec, v):
    return WRONG.get(spec["cls"], WRONG_DEFAULT).format(v=v)


def _imports(text, extra=()):
    """Import lines for the stdlib modules the generated code actually uses (scanned from the code, so nothing is imported that is not used)."""
    import re
    mods = {m for m in ("os", "shlex", "html", "subprocess", "sqlite3") if re.search(r"\b%s\." % m, text)}
    return ["import " + m for m in sorted(mods | set(extra))]


def _sink(spec, s):
    """(compute lines, return expr). `s` is the variable that reaches the sink."""
    cls, w = spec["cls"], spec["w"]
    n = spec.get("neut") or {}
    if cls == "CWEC-22":
        return ["%s = os.path.join(%s, %s)" % (w[0], spec["consts"]["root"], s), "%s = open(%s)" % (w[1], w[0]), "%s = %s.read()" % (w[2], w[1]), "%s.close()" % w[1]], w[2]
    if cls == "CWEC-78":
        if n.get("san") == "param_api":
            return ['%s = subprocess.run(["echo", %s], capture_output=True, text=True)' % (w[0], s)], "%s.stdout" % w[0]
        return ['%s = subprocess.run("echo " + %s, shell=True, capture_output=True, text=True)' % (w[0], s)], "%s.stdout" % w[0]
    if cls == "CWEC-79":
        return ['%s = "<p>" + %s + "</p>"' % (w[0], s)], w[0]
    if cls == "CWEC-89":
        # self-contained: a fresh in-memory database has no table, so the function creates and fills the two-row table itself (the real sqlite3 would raise
        # "no such table" otherwise); the setup lines are the same on every CWEC-89 row, whatever the label
        setup = ["%s = sqlite3.connect(\":memory:\")" % w[0], "%s = %s.cursor()" % (w[1], w[0]),
                 '%s.execute("CREATE TABLE users (id TEXT, name TEXT)")' % w[1],
                 '%s.execute("INSERT INTO users VALUES (\'1\', \'alice\'), (\'2\', \'bob\')")' % w[1]]
        if n.get("san") == "param_api":
            return setup + ['%s.execute("SELECT name FROM users WHERE id = ?", (%s,))' % (w[1], s)], "%s.fetchall()" % w[1]
        return setup + ['%s.execute("SELECT name FROM users WHERE id = \'" + %s + "\'")' % (w[1], s)], "%s.fetchall()" % w[1]
    if cls == "CWEC-117":
        return ['%s = "INFO user=" + %s' % (w[0], s)], w[0]
    if cls == "CWEC-601":
        return ["%s = %s" % (w[0], s)], w[0]
    raise ValueError(cls)


_TRANSFORM = {"strip": "{n} = {v}.strip()", "lower": "{n} = {v}.lower()"}


def _fmt(spec, v, n):
    return {"CWEC-22": '%s = "./" + %s', "CWEC-601": '%s = %s + "#top"'}.get(spec["cls"], '%s = "item " + %s') % (n, v)


def render_dynamic(spec):
    cls, nm = spec["cls"], spec["names"]
    p, neut = nm["param"], spec.get("neut")
    consts, helpers = [], []
    if cls == "CWEC-22":
        consts.append('%s = "srv/files"' % spec["consts"]["root"])             # relative to the job directory: the fixture files ship WITH the job (config.FIXTURES)
    if neut and neut["san"] == "allowlist":
        allowed = ", ".join('"%s"' % x for x in spec["allowed"])
        consts.append("%s = (%s%s)" % (spec["consts"]["allowed"], allowed, "," if len(spec["allowed"]) == 1 else ""))
    if spec["source"] != "param":
        consts.append('%s = "%s"' % (spec["consts"]["config"], spec["config_value"]))
    if neut and neut["san"] == "helper":
        h1, h2 = nm["h1"], nm["h2"]
        helpers = ["def %s(x):" % h2, "    return %s" % (_san(spec, "x") if valid_step(neut) and not neut.get("identity") else "x"), "", "",
                   "def %s(x):" % h1, "    return %s(x)" % h2]
    body = []
    if consts:
        body += [""] + consts
    if helpers:
        body += ["", ""] + helpers
    body += ["", ""]
    lines = ["def %s(%s):" % (nm["fn"], p)]
    chain = nm["chain"]
    cur = chain[0]
    lines.append("    %s = %s" % (cur, p if spec["source"] == "param" else spec["consts"]["config"]))
    for i, t in enumerate(spec["transforms"]):
        nxt = chain[i + 1]
        if t == "box":
            lines += ['    %s = {"k": %s}' % (nm["box"], cur), '    %s = %s["k"]' % (nxt, nm["box"])]
        elif t == "fmt":
            lines.append("    " + _fmt(spec, cur, nxt))
        else:
            lines.append("    " + _TRANSFORM[t].format(n=nxt, v=cur))
        cur = nxt
    vt, sv = cur, cur
    vs = nm.get("alt")
    pre, post = [], []
    kind, form = (neut["san"], neut.get("form", "direct")) if neut else (None, None)
    if kind == "valid":
        if form == "direct":
            pre.append("%s = %s" % (vt, _san(spec, vt)))
        elif form == "copy":
            pre += ["%s = %s" % (vs, vt), "%s = %s" % (vs, _san(spec, vs))]
            sv = vs
        else:                                                      # copy1
            pre.append("%s = %s" % (vs, _san(spec, vt)))
            sv = vs
    elif kind == "wrong_class":
        pre.append("%s = %s" % (vt, _wrong(spec, vt)))
    elif kind == "wrong_var":                                      # DS-1: the step runs on the copy, the sink reads the original
        pre += ["%s = %s" % (vs, vt), "%s = %s" % (vs, _san(spec, vs))]
    elif kind == "after_sink":
        post.append("%s = %s" % (vt, _san(spec, vt)))
    elif kind == "branch":
        pre += ["if len(%s) < %d:" % (vt, neut["n"]), "    %s = %s" % (vt, _san(spec, vt))]
    elif kind == "discarded":
        pre.append(_san(spec, vt))
    elif kind == "overwritten":                                    # DS-6: sanitised value replaced by the raw one
        pre += ["%s = %s" % (vs, _san(spec, vt)), "%s = %s" % (vs, vt)]
        sv = vs
    elif kind == "allowlist":
        pre += ["if %s not in %s:" % (vt, spec["consts"]["allowed"]), '    raise ValueError("%s")' % nm["msg"]]
    elif kind == "helper":
        pre.append("%s = %s(%s)" % (vt, nm["h1"], vt))
    if spec.get("noise"):
        pre.insert(0, "%s = %s" % (nm["noisevar"], spec["noise"]["expr"]))
    compute, ret = _sink(spec, sv)
    lines += ["    " + x for x in pre] + ["    " + x for x in compute] + ["    " + x for x in post] + ["    return %s" % ret]
    code = "\n".join(body + lines)
    return "\n".join(_imports(code) + body + lines) + "\n"


def render_static(spec):
    cls, nm, neut = spec["cls"], spec["names"], spec.get("neut")
    kind, form = (neut["san"], neut.get("form", "direct")) if neut else (None, None)
    flagged = spec.get("flagged", True)
    P = nm["param"]
    if cls == "CWEC-295":
        c, a = nm["ctx"], nm["alt"]
        head = ["import ssl", "", ""]
        if kind == "helper":
            if neut.get("identity"):                       # NS-1 YES member: the helper two calls away does NOT re-enable verification (identity)
                head += ["def %s(x):" % nm["h2"], "    return x", "", "", "def %s(x):" % nm["h1"], "    return %s(x)" % nm["h2"], "", ""]
            else:
                head += ["def %s(x):" % nm["h2"], "    x.verify_mode = ssl.CERT_REQUIRED", "    x.check_hostname = True", "    return x", "", "", "def %s(x):" % nm["h1"],
                         "    return %s(x)" % nm["h2"], "", ""]
        lines = ["def %s(%s):" % (nm["fn"], P), "    %s = ssl.create_default_context()" % c]
        if flagged:
            lines += ["    %s.check_hostname = False" % c, "    %s.verify_mode = ssl.CERT_NONE" % c]
        reen = ["    %s.verify_mode = ssl.CERT_REQUIRED" % c, "    %s.check_hostname = True" % c]
        tail = []
        if kind == "valid":
            lines += (["    %s = ssl.create_default_context()" % a] if form == "alt" else []) + reen
        elif kind == "wrong_var":
            lines += ["    %s = ssl.create_default_context()" % a, "    %s.verify_mode = ssl.CERT_REQUIRED" % a, "    %s.check_hostname = True" % a]
        elif kind == "wrong_class":
            lines.append("    %s.minimum_version = ssl.TLSVersion.TLSv1_2" % c)
        elif kind == "branch":
            lines += ['    if %s == "":' % P, "        %s.verify_mode = ssl.CERT_REQUIRED" % c]
        elif kind == "discarded":
            lines.append("    ssl.CERT_REQUIRED")
        elif kind == "overwritten":
            lines += [reen[0], "    %s.verify_mode = ssl.CERT_NONE" % c]
        elif kind == "helper":
            lines.append("    %s = %s(%s)" % (c, nm["h1"], c))
        elif kind == "after_sink":
            tail = reen
        return "\n".join(head + lines + ["    return %s" % c] + tail) + "\n"
    if cls == "CWEC-327":
        h, a, salt = nm["h"], nm["alt"], nm["salt"]
        weak = "hashlib.md5(%s.encode()).hexdigest()" % P
        kdf = 'hashlib.pbkdf2_hmac("sha256", %s.encode(), %s, 100000).hex()' % (P, salt)
        head = ["import hashlib", "", "", '%s = b"%s"' % (salt, nm["salt_word"]), "", ""]
        if kind == "helper":
            body = weak.replace(P + ".encode()", "x.encode()") if neut.get("identity") else kdf.replace(P + ".encode()", "x.encode()")   # identity = the weak hash stays
            head += ["def %s(x):" % nm["h2"], "    return %s" % body, "", "", "def %s(x):" % nm["h1"], "    return %s(x)" % nm["h2"], "", ""]
        L = ["def %s(%s):" % (nm["fn"], P)]
        if kind is None:
            L += ["    %s = %s" % (h, weak), "    return %s" % h]
        elif kind == "valid":
            L += (["    %s = %s" % (h, kdf), "    %s = %s" % (a, weak)] if form == "alt" else ["    %s = %s" % (h, kdf)]) + ["    return %s" % h]
        elif kind == "wrong_var":
            L += ["    %s = %s" % (a, kdf), "    %s = %s" % (h, weak), "    return %s" % h]
        elif kind == "wrong_class":
            L += ["    %s = hashlib.sha256(%s + %s.encode()).hexdigest()" % (h, salt, P), "    return %s" % h]
        elif kind == "after_sink":
            L += ["    %s = %s" % (h, weak), "    return %s" % h, "    %s = %s" % (h, kdf)]
        elif kind == "branch":
            L += ["    %s = %s" % (h, weak), "    if len(%s) < %d:" % (P, neut["n"]), "        %s = %s" % (h, kdf), "    return %s" % h]
        elif kind == "discarded":
            L += ["    %s" % kdf, "    %s = %s" % (h, weak), "    return %s" % h]
        elif kind == "overwritten":
            L += ["    %s = %s" % (h, kdf), "    %s = %s" % (h, weak), "    return %s" % h]
        elif kind == "helper":
            L += ["    %s = %s(%s)" % (h, nm["h1"], P), "    return %s" % h]
        return "\n".join(head + L) + "\n"
    p, fd, a = nm["path"], nm["fd"], nm["alt"]
    weak = '%s = tempfile.mktemp(suffix=".log")' % p
    good = '%s, %s = tempfile.mkstemp(suffix=".log")' % (fd, p)
    head = ["import tempfile", "", ""]
    if kind == "helper":
        inner = '    return None, tempfile.mktemp(suffix=".log")' if neut.get("identity") else '    return tempfile.mkstemp(suffix=".log")'   # identity = predictable name stays
        head += ["def %s():" % nm["h2"], inner, "", "", "def %s():" % nm["h1"], "    return %s()" % nm["h2"], "", ""]
    L = ["def %s(%s):" % (nm["fn"], P)]
    if not flagged:
        L += ["    %s = tempfile.mkdtemp()" % nm["dir"], '    %s = %s + "/" + "%s"' % (p, nm["dir"], nm["fixed"]), "    return %s" % p]
    elif kind is None:
        L += ["    " + weak, "    return %s" % p]
    elif kind == "valid":
        L += (["    " + weak.replace(p, a), "    " + good] if form == "alt" else ["    " + good]) + ["    return %s" % p]
    elif kind == "helper":
        L += ["    %s, %s = %s()" % (fd, p, nm["h1"]), "    return %s" % p]
    elif kind == "wrong_class":
        L += ["    " + weak, "    %s = tempfile.gettempdir()" % nm["dir"], "    return %s" % p]
    elif kind == "wrong_var":
        L += ["    " + weak, '    %s, %s = tempfile.mkstemp(suffix=".log")' % (fd, a), "    return %s" % p]
    elif kind == "after_sink":
        L += ["    " + weak, "    return %s" % p, "    " + good]
    elif kind == "branch":
        L += ["    " + weak, "    if %s:" % P, "        " + good, "    return %s" % p]
    elif kind == "discarded":
        L += ['    tempfile.mkstemp(suffix=".log")', "    " + weak, "    return %s" % p]
    elif kind == "overwritten":
        L += ["    " + good, "    " + weak, "    return %s" % p]
    return "\n".join(head + L) + "\n"


def render(spec):
    return render_static(spec) if spec["cls"] in C.STATIC else render_dynamic(spec)
