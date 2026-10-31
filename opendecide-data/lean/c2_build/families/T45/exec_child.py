"""families/T45/exec_child.py: the hermetic child of T45 TRACE-VERIFY (solver A, execution side).

Run as `python -S -s -B -P exec_child.py` with PYTHONHASHSEED=0, a fresh temp dir as cwd and a JSON job on stdin; one JSON
result on stdout. It builds a REAL sandbox (a git work tree with local bare remotes, an sqlite file, a localhost HTTP
server started inside this process, a make tree, a unittest tree), runs the REAL step, reads the state back with REAL
inspectors, and then (for steps that did not work) runs the same step again ("retry") and a repaired step ("repair") in
fresh copies of the same sandbox. Nothing here decides a label: the parent (executor.classify) does, from the states.

Network: only 127.0.0.1 inside this process. No other host is contacted; the child has no proxy variables.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import stat
import subprocess
import sys
import tempfile
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PY = sys.executable
ROOT = None
FIXED_PORT = "8080"          # the port shown in command lines; the real one is ephemeral
GIT_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_TERMINAL_PROMPT": "0", "GIT_AUTHOR_NAME": "dev",
           "GIT_AUTHOR_EMAIL": "dev@example.test", "GIT_COMMITTER_NAME": "dev",
           "GIT_COMMITTER_EMAIL": "dev@example.test"}
BASE_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C", "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"}


class EnvError(RuntimeError):
    """A wall-clock timeout or an exit status no tool of the catalogue produces (killed, not found): never an outcome. The
    child exits 97 and the parent repeats the whole spec; after the last repeat the spec is dropped and counted."""


INNER_T = float(os.environ.get("T45_INNER_TIMEOUT") or 0)       # test knob: a tiny inner timeout must only cause drops
ALLOWED_RC = {"git": (0, 1, 128), "curl": (0, 22), "make": (0, 2)}


def run(args, cwd, env=None, timeout=3.0, input=None):
    e = dict(BASE_ENV)
    e["HOME"] = ROOT
    if env:
        e.update(env)
    try:
        p = subprocess.run(args, cwd=cwd, env=e, capture_output=True, text=True, timeout=INNER_T or timeout, input=input)
    except subprocess.TimeoutExpired:
        raise EnvError("inner timeout: " + " ".join(args)[:80])
    allowed = ALLOWED_RC.get(os.path.basename(args[0]), (0, 1, 5))
    if p.returncode not in allowed:
        raise EnvError(f"unexpected exit {p.returncode} from {os.path.basename(args[0])}")
    return p.returncode, p.stdout, p.stderr


def git(args, cwd, date=None):
    env = dict(GIT_ENV)
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    return run(["git"] + args, cwd, env)


def new_dir(name):
    d = os.path.join(ROOT, name)
    os.makedirs(d)
    return d


def sh_script(path, text):
    with open(path, "w") as f:
        f.write(text)
    os.chmod(path, 0o755)


# ===================================================================================================== git
def git_setup(p):
    """origin.git (bare), backup.git (bare), work/ with branches main < other < br (and feat for stale_noop). Plumbing
    (commit-tree on the empty tree + one update-ref --stdin per repo) keeps the number of git calls small."""
    wd = new_dir("work")
    o = os.path.join(ROOT, "origin.git")
    b = os.path.join(ROOT, "backup.git")
    git(["init", "-q", "-b", "main", wd], ROOT)
    for d in (o, b):
        git(["init", "-q", "--bare", "-b", "main", d], ROOT)
    with open(os.path.join(wd, ".git", "config"), "a") as f:
        f.write('[remote "origin"]\n\turl = ../origin.git\n\tfetch = +refs/heads/*:refs/remotes/origin/*\n'
                '[remote "backup"]\n\turl = ../backup.git\n\tfetch = +refs/heads/*:refs/remotes/backup/*\n')
    empty = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    day = [1]

    def commit(msg, parent=None):
        d = f"2026-02-{day[0]:02d}T10:00:00Z"
        day[0] += 1
        args = ["commit-tree", empty, "-m", msg] + (["-p", parent] if parent else [])
        return git(args, wd, date=d)[1].strip()
    fault, br, other, feat = p["fault"], p["br"], p["other"], p["feat"]
    c1 = commit("c1")
    c2 = commit("c2", c1)
    head_old = c2
    for i in range(2):
        head_old = commit(f"b{i}", head_old)
    head = commit("new", head_old) if fault == "stale_noop" else head_old
    refs = [f"update refs/heads/main {c1}", f"update refs/heads/{other} {c2}", f"update refs/heads/{br} {head_old}"]
    if fault == "stale_noop":
        refs.append(f"update refs/heads/{feat} {head}")
    for t in p["tags"]:
        refs.append(f"update refs/tags/{t} {head}")
    run(["git", "update-ref", "--stdin"], wd, GIT_ENV, input="\n".join(refs) + "\n")
    git(["push", "-q", "origin", "main"], wd)
    run(["git", "update-ref", "--stdin"], o, GIT_ENV, input="".join(f"create refs/heads/{nm} {c1}\n" for nm in p["noise"]))
    if fault == "already_done":
        git(["push", "-q", "origin", br] + tags_intended(p), wd)
    if fault == "stale_noop":
        git(["push", "-q", "origin", br], wd)         # origin br = old sha
    hook = os.path.join(o, "hooks", "pre-receive")
    if fault == "busy":
        sh_script(hook, '#!/bin/sh\nn=$(cat busy.count 2>/dev/null || echo 0)\nif [ "$n" -lt 1 ]; then echo $((n+1)) > busy.count; '
                        'echo "remote: error: ref lock busy, try again" >&2; exit 1; fi\nexit 0\n')
    if fault == "blocked":
        sh_script(hook, '#!/bin/sh\necho "remote: error: protected branch, ask the maintainers" >&2\nexit 1\n')
    intent = {f"heads/{br}": head[:7]}
    for t in tags_intended(p):
        intent[f"tags/{t}"] = head[:7]
    return {"wd": wd, "o": o, "head": head[:7], "c1": c1}, intent


def tags_intended(p):
    return list(p["tags"])                    # every git intent holds the branch and 1-2 tags: its size is label-blind


def git_read(ctx, p):
    rc, out, err = git(["ls-remote", "origin"], ctx["wd"])
    st = {}
    for ln in out.splitlines():
        sha, ref = ln.split("\t")
        if ref.startswith("refs/heads/"):
            st["heads/" + ref[11:]] = sha[:7]
        elif ref.startswith("refs/tags/"):
            st["tags/" + ref[10:]] = sha[:7]
    return st


def git_noise(ctx, p, n):
    return


def git_cmd(p, which):
    f, br, other, feat = p["fault"], p["br"], p["other"], p["feat"]
    if which in ("main", "retry"):
        if f == "wrong_target":
            return ["git", "push", "origin", other] if p["variant"] == 0 else ["git", "push", "backup", br, "--tags"]
        if f == "bad_arg":
            return ["git", "push", "orign", br] if p["variant"] == 0 else ["git", "push", "origin", br + "x"]
        if f == "swallowed":
            return ["git", "push", "origin", br]                # the branch only: the tags stay behind
        return ["git", "push", "origin", br, "--tags"]
    if f == "stale_noop":
        return ["git", "push", "origin", f"{feat}:{br}", "--tags"]
    if f == "blocked":
        return ["git", "push", "--force", "origin", br, "--tags"]
    return ["git", "push", "origin", br, "--tags"]


def git_step(ctx, p, which):
    cmd = git_cmd(p, which)
    rc, out, err = run(cmd, ctx["wd"], GIT_ENV)
    return cmd, rc, out, err


def git_classify(rc, out, err, p):
    t = (out + err).lower()
    if rc == 0:
        return "0"
    if re.search(r"busy|try again|lock", t):
        return "T"
    if re.search(r"does not appear to be a git repository|does not match any|unknown revision|no such", t):
        return "A"
    if re.search(r"protected|denied|forbidden|permission|read-only", t):
        return "H"
    return "?"


# ===================================================================================================== db
DBLOAD = r'''
import csv, sqlite3, sys
db, batch = sys.argv[1], sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else "--lenient"
rows = [(int(r[0]), r[1] or None, int(r[2])) for r in csv.reader(open(batch)) if r]
try:
    con = sqlite3.connect(db, timeout=0.0)
    if mode == "--script":
        con.isolation_level = None
        script = "\n".join("INSERT INTO __T__(id,sku,qty) VALUES(%d,%s,%d);" % (i, "NULL" if s is None else "'%s'" % s, q)
                           for i, s, q in rows)
        con.executescript(script)
        print("loaded %d rows" % len(rows)); sys.exit(0)
    if mode == "--strict":
        try:
            with con:
                for n, (i, s, q) in enumerate(rows, 1):
                    con.execute("INSERT INTO __T__(id,sku,qty) VALUES(?,?,?)", (i, s, q))
        except sqlite3.IntegrityError as e:
            print("error: constraint failed at row %d (%s)" % (n, e), file=sys.stderr); sys.exit(1)
        print("loaded %d rows" % len(rows)); sys.exit(0)
    done = skipped = kept = 0
    for i, s, q in rows:
        cur = con.execute("SELECT qty FROM __T__ WHERE id=?", (i,)).fetchone()
        if cur is not None:
            if mode == "--update":
                con.execute("UPDATE __T__ SET qty=? WHERE id=?", (q, i)); done += 1
            elif cur[0] != q:
                kept += 1
            continue
        try:
            con.execute("INSERT INTO __T__(id,sku,qty) VALUES(?,?,?)", (i, s, q)); done += 1
        except sqlite3.IntegrityError:
            skipped += 1
    con.commit()
    print("loaded %d rows" % done)
    if skipped:
        print("warning: skipped %d rows (constraint)" % skipped, file=sys.stderr)
    if kept:
        print("warning: kept %d existing rows" % kept, file=sys.stderr)
except sqlite3.OperationalError as e:
    print("error: %s" % e, file=sys.stderr); sys.exit(1)
except sqlite3.IntegrityError as e:
    print("error: %s" % e, file=sys.stderr); sys.exit(1)
'''


def db_setup(p):
    d = new_dir("data")
    path = os.path.join(d, "shop.db")
    decoy = os.path.join(ROOT, "shop.db")
    for q in {path, decoy} if p["fault"] == "wrong_target" else {path}:
        con = sqlite3.connect(q)
        con.execute("CREATE TABLE %s(id INTEGER PRIMARY KEY, sku TEXT NOT NULL, qty INTEGER NOT NULL CHECK(qty > 0))" % p["table"])
        for i in range(p["nb"]):
            con.execute("INSERT INTO %s VALUES(?,?,?)" % p["table"], (i + 1, "s%d" % (i + 1), 2 + i))
        if q == path and p["fault"] in ("already_done", "stale_noop"):
            for i, (iid, qty) in enumerate(p["items"]):
                old = qty if p["fault"] == "already_done" else qty + 1 + (i % 3)
                con.execute("INSERT INTO %s VALUES(?,?,?)" % p["table"], (iid, "s%d" % iid, old))
        con.commit()
        con.close()
    with open(os.path.join(ROOT, "dbload.py"), "w") as f:
        f.write(DBLOAD.replace("__T__", p["table"]))
    write_batch(p, p["bad_rows"] if p["fault"] in ("swallowed", "bad_arg") else [])
    if p["fault"] == "blocked":
        os.chmod(path, 0o444)
    holder = None
    intent = {f"{p['table']}.{iid}": str(q) for iid, q in p["items"]}
    return {"path": path, "holder": holder}, intent


def db_arm(ctx, p):
    if p["fault"] == "busy":
        h = sqlite3.connect(ctx["path"], timeout=0.0)
        h.isolation_level = None
        h.execute("BEGIN EXCLUSIVE")
        ctx["holder"] = h


def db_release(ctx, p):
    if ctx["holder"] is not None:
        ctx["holder"].execute("ROLLBACK")
        ctx["holder"].close()
        ctx["holder"] = None


def write_batch(p, bad):
    items = list(p["items"])
    lines = []
    for n, (iid, q) in enumerate(items):
        lines.append("%d,%s,%d" % (iid, "" if n in bad else "s%d" % iid, q))
    if p["fault"] == "fail_midway":
        j = p["dup_at"]
        lines.insert(j, lines[j - 1])
    with open(os.path.join(ROOT, "batch.csv"), "w") as f:
        f.write("\n".join(lines) + "\n")


def db_read(ctx, p):
    con = sqlite3.connect("file:%s?mode=ro" % ctx["path"], uri=True, timeout=0.0)
    try:
        rows = con.execute("SELECT id, qty FROM %s ORDER BY id" % p["table"]).fetchall()
    except sqlite3.OperationalError as e:
        raise EnvError(f"db readback: {e}")                   # never an empty state by accident
    con.close()
    return {f"{p['table']}.{i}": str(q) for i, q in rows}


def db_noise(ctx, p, n):
    if ctx["holder"] is not None:
        return
    try:
        os.chmod(ctx["path"], 0o644)
        con = sqlite3.connect(ctx["path"], timeout=0.0)
        for i in range(n):
            con.execute("INSERT OR IGNORE INTO %s VALUES(?,?,?)" % p["table"], (900 + i, "x", 1))
        con.commit()
        con.close()
        if p["fault"] == "blocked":
            os.chmod(ctx["path"], 0o444)
    except sqlite3.Error:
        pass


def db_cmd(p, which):
    f = p["fault"]
    db = "shop.db" if (f == "wrong_target" and which in ("main", "retry")) else "data/shop.db"
    mode = {"bad_arg": "--strict", "fail_midway": "--script"}.get(f)
    if which == "repair" and f == "stale_noop":
        mode = "--update"
    if which == "repair" and f == "fail_midway":
        mode = None
    if which == "repair" and f == "bad_arg":
        mode = "--strict"
    cmd = ["python", "dbload.py", db, "batch.csv"] + ([mode] if mode else [])
    return cmd


def db_step(ctx, p, which):
    if which == "repair" and p["fault"] in ("swallowed", "bad_arg", "fail_midway"):
        write_batch({**p, "fault": "ok"}, [])
    cmd = db_cmd(p, which)
    real = [PY if cmd[0] == "python" else cmd[0]] + cmd[1:]
    rc, out, err = run(real, ROOT, timeout=3.0)
    return cmd, rc, out, err


def db_classify(rc, out, err, p):
    t = (out + err).lower()
    if rc == 0 and not err.strip():
        return "0"
    if re.search(r"locked|busy", t):
        return "T"
    if re.search(r"readonly|read-only|permission", t):
        return "H"
    if re.search(r"skipped|kept|constraint|unique|failed at row", t):
        return "A"
    return "?" if rc else "0"


# ===================================================================================================== http
class Store:
    def __init__(self, p):
        self.p = p
        self.prod = {}
        self.staging = {}
        self.calls = 0
        self.last_status = 0
        self.lock = threading.Lock()


def make_handler(st):
    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def log_message(self, *a):
            pass

        def reply(self, code, body):
            data = json.dumps(body).encode()
            st.last_status = code
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/v1/" + st.p["res"]:
                self.reply(200, [{"id": k, "name": v} for k, v in sorted(st.prod.items())])
            else:
                self.reply(404, {})

        def do_POST(self):
            p = st.p
            f = p["fault"]
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n) or b"[]")
            path = self.path.split("?")[0]
            query = self.path.partition("?")[2]
            with st.lock:
                st.calls += 1
                call = st.calls
                if path not in ("/v1/%s/batch" % p["res"], "/v1/staging/%s/batch" % p["res"]):
                    return self.reply(404, {})
                key = self.headers.get("X-Key", "")
                if f == "blocked":
                    return self.reply(403, {})
                if f == "busy" and call == 1:
                    return self.reply(503, {})
                if f == "error_body" and p["variant"] == 1:
                    return self.reply(200, {"error": "forbidden"})
                if f == "error_body" and key != "k1":
                    return self.reply(200, {"error": "invalid_key"})
                store = st.staging if path.startswith("/v1/staging") else st.prod
                stored = rejected = skipped = deferred = 0
                limit = p["rate_q"] if (f == "deferred" and call == 1) else None
                for it in body:
                    iid, name = it["id"], it["name"]
                    if not name:
                        rejected += 1
                        continue
                    if iid in store:
                        if store[iid] == name:
                            continue
                        if f == "stale_noop" and "mode=upsert" not in query:
                            skipped += 1
                            continue
                    if limit is not None and stored >= limit:
                        deferred += 1
                        continue
                    store[iid] = name
                    stored += 1
                resp = {"stored": stored}
                for k, v in (("rejected", rejected), ("skipped", skipped), ("deferred", deferred)):
                    if v:
                        resp[k] = v
                return self.reply(200, resp)
    return H


def http_setup(p):
    st = Store(p)
    for i in range(p["nb"]):
        st.prod[i + 1] = p["noise"][i]
    if p["fault"] in ("already_done", "stale_noop"):
        for n, (iid, name) in enumerate(p["items"]):
            st.prod[iid] = name if p["fault"] == "already_done" else name + "_old"
    srv = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(st))
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    port = srv.server_address[1]
    write_http_batch(p, p["bad_rows"] if p["fault"] == "swallowed" else [])
    intent = {f"{p['res']}.{iid}": name for iid, name in p["items"]}
    return {"srv": srv, "st": st, "port": port}, intent


def write_http_batch(p, bad):
    body = [{"id": iid, "name": ("" if n in bad else name)} for n, (iid, name) in enumerate(p["items"])]
    with open(os.path.join(ROOT, "batch.json"), "w") as f:
        json.dump(body, f)


def http_read(ctx, p):
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with op.open("http://127.0.0.1:%d/v1/%s" % (ctx["port"], p["res"]), timeout=INNER_T or 2) as r:
            data = json.loads(r.read())
    except Exception as e:  # noqa: BLE001  (timeout, reset, refused: environment, never a state)
        raise EnvError(f"http readback: {type(e).__name__}")
    return {f"{p['res']}.{d['id']}": d["name"] for d in data}


def http_noise(ctx, p, n):
    for i in range(n):
        ctx["st"].prod[900 + i] = p["extra_names"][i]


def http_cmd(p, which):
    f = p["fault"]
    path = "/v1/%s/batch" % p["res"]
    key = "k1"
    flags = "-s"
    if f == "wrong_target" and which in ("main", "retry"):
        path = "/v1/staging/%s/batch" % p["res"]
    if f == "bad_arg" and which in ("main", "retry"):
        path = "/v1/%sx/batch" % p["res"]
    if f in ("bad_arg", "busy", "blocked"):
        flags = "-sf"
    if f == "error_body" and p["variant"] == 0 and which in ("main", "retry"):
        key = "k0"
    if f == "blocked" and which == "repair":
        key = "k2"
    if f == "stale_noop" and which == "repair":
        path += "?mode=upsert"
    return ["curl", flags, "-X", "POST", "-H", f"X-Key: {key}", "-d", "@batch.json", f"http://127.0.0.1:{FIXED_PORT}{path}"]


def http_step(ctx, p, which):
    if which == "repair" and p["fault"] == "swallowed":
        write_http_batch(p, [])
    cmd = http_cmd(p, which)
    real = [c.replace(":" + FIXED_PORT + "/", ":%d/" % ctx["port"]) for c in cmd]
    rc, out, err = run(real, ROOT, timeout=3.0)
    return cmd, rc, out, err + "|status=%d" % ctx["st"].last_status


def http_classify(rc, out, err, p):
    t = out.lower()
    m = re.search(r"\|status=(\d+)", err)
    status = int(m.group(1)) if m else 0
    if rc != 0:
        if status in (503, 429):
            return "T"
        if status in (400, 404, 422):
            return "A"
        if status in (401, 403):
            return "H"
        return "?"
    if "deferred" in t:
        return "T"
    if "forbidden" in t:
        return "H"
    if re.search(r"rejected|skipped|invalid_key", t):
        return "A"
    return "0"


# ===================================================================================================== build
GEN = r'''
import os, sys
src, out = sys.argv[1], sys.argv[2]
try:
    text = open(src).read().strip()
except OSError:
    print("gen: missing source %s" % src, file=sys.stderr); sys.exit(1)
if text == "BAD":
    print("gen: corrupt source %s" % src, file=sys.stderr); sys.exit(1)
tmp = out + ".tmp"
try:
    with open(tmp, "w") as f:
        f.write(text)
    os.replace(tmp, out)
except OSError:
    print("gen: permission denied for %s" % out, file=sys.stderr); sys.exit(1)
'''
MAKEFILE = '''PY = {py}
OUT = build
NAMES = {names}
all: $(addprefix $(OUT)/,$(addsuffix .bin,$(NAMES)))
$(OUT)/%.bin: src/%.src
\t@mkdir -p $(OUT)
{lock}\t{dash}$(PY) gen.py $< $@
'''
LOCK = '\t@test ! -f build.lock || (echo "make: build.lock held by another job, try again" >&2; exit 1)\n'


def build_setup(p):
    names, f = p["names"], p["fault"]
    os.makedirs(os.path.join(ROOT, "src"))
    os.makedirs(os.path.join(ROOT, "build"))
    with open(os.path.join(ROOT, "gen.py"), "w") as fh:
        fh.write(GEN)
    mk = MAKEFILE.format(py=PY, names=" ".join(names), lock=LOCK if f == "busy" else "",
                         dash="-" if f == "swallowed" else "")
    with open(os.path.join(ROOT, "Makefile"), "w") as fh:
        fh.write(mk)
    new, old = "r%d" % p["ver"], "r%d" % (p["ver"] - 1)
    new_old_noise = old          # the noise artifact carries the old version word, so that word is in every build row's before-state
    for n, name in enumerate(names):
        src = os.path.join(ROOT, "src", name + ".src")
        art = os.path.join(ROOT, "build", name + ".bin")
        bad = f in ("swallowed", "fail_midway") and n in p["bad_rows"]
        with open(src, "w") as fh:
            fh.write("BAD" if bad else new)
        os.utime(src, (2000, 2000))
        have = None
        if f == "already_done":
            have = new
        elif f == "stale_noop":
            have = old
        elif p["old_present"]:
            have = old
        if have:
            with open(art, "w") as fh:
                fh.write(have)
            os.utime(art, (3000, 3000) if f in ("already_done", "stale_noop") else (1000, 1000))
    for nm in p["noise"]:
        with open(os.path.join(ROOT, "build", nm + ".bin"), "w") as fh:
            fh.write(new_old_noise)
    if f == "busy":
        open(os.path.join(ROOT, "build.lock"), "w").close()
    if f == "blocked":
        os.chmod(os.path.join(ROOT, "build"), 0o555)
    intent = {f"build/{n}.bin": new for n in names}
    return {}, intent


def build_read(ctx, p):
    st = {}
    d = os.path.join(ROOT, "build")
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".bin"):
            st["build/" + fn] = open(os.path.join(d, fn)).read().strip()
    out = os.path.join(ROOT, "out")
    return st


def build_noise(ctx, p, n):
    d = os.path.join(ROOT, "build")
    if p["fault"] == "blocked":
        return
    for nm in p["extra_names"][:n]:
        with open(os.path.join(d, nm + ".bin"), "w") as fh:
            fh.write("r1")


def build_cmd(p, which):
    f = p["fault"]
    if which in ("main", "retry"):
        if f == "wrong_target":
            return ["make", "all", "OUT=out"]
        if f == "bad_arg":
            return ["make", "al"]
        if f == "fail_midway":
            return ["make", "-k", "all"]
        return ["make", "all"]
    if f == "stale_noop" or f == "blocked":
        return ["make", "-B", "all"]
    return ["make", "all"]


def build_step(ctx, p, which):
    if which == "repair" and p["fault"] in ("swallowed", "fail_midway"):
        for name in p["names"]:
            src = os.path.join(ROOT, "src", name + ".src")
            with open(src, "w") as fh:
                fh.write("r%d" % p["ver"])
            os.utime(src, (2000, 2000))
    cmd = build_cmd(p, which)
    rc, out, err = run(cmd, ROOT, timeout=3.0)
    return cmd, rc, out, err


def build_prepare_second(ctx, p, which):
    if p["fault"] == "busy":
        os.remove(os.path.join(ROOT, "build.lock"))


def build_classify(rc, out, err, p):
    t = (out + err).lower()
    if rc == 0 and not re.search(r"ignored", t):
        return "0"
    if re.search(r"try again|held by another", t):
        return "T"
    if re.search(r"permission denied", t):
        return "H"
    if re.search(r"no rule to make target|corrupt source|missing source|ignored", t):
        return "A"
    return "?" if rc else "0"


# ===================================================================================================== tests
TEST_TPL = "import os, unittest\nclass Suite(unittest.TestCase):\n{methods}\n"


def tests_setup(p):
    d_good, d_bad = p["dir"], p["bad_dir"]
    os.makedirs(os.path.join(ROOT, d_good))
    os.makedirs(os.path.join(ROOT, d_bad))
    f = p["fault"]
    mods = {}
    for n, (mod, t) in enumerate(p["names"]):
        body = "        self.assertEqual(%d, %d)" % (n + 2, n + 2)
        deco = ""
        if f == "swallowed" and n in p["bad_rows"]:
            deco = '    @unittest.skip("later")\n'
        if f == "blocked" and n == p["fail_at"]:
            body = "        self.assertEqual(%d, %d)" % (n + 2, n + 3)
        if f == "busy" and n == p["fail_at"]:
            body = ("        if not os.path.exists('flaky.flag'):\n            open('flaky.flag', 'w').close()\n"
                    "            self.fail('resource temporarily unavailable')")
        mods.setdefault(mod, []).append(f"{deco}    def {t}(self):\n{body}\n")
    for mod, ms in mods.items():
        with open(os.path.join(ROOT, d_good, f"{mod}.py"), "w") as fh:
            fh.write(TEST_TPL.format(methods="".join(ms)))
    mod2 = p["bad_mod"]
    with open(os.path.join(ROOT, d_bad, f"{mod2}.py"), "w") as fh:
        fh.write(TEST_TPL.format(methods="".join(f"    def {t}(self):\n        self.assertTrue(True)\n" for t in p["bad_tests"])))
    intent = {f"{d_good}/{m}.{t}": "pass" for m, t in p["names"]}
    ctx = {"last": {}}
    if f == "already_done":
        cmd = tests_cmd(p, "repair")
        rc, out, err = run([PY if c == "python" else c for c in cmd], ROOT, timeout=3.0)
        ctx["last"] = parse_tests(err, d_good)
    return ctx, intent


def parse_tests(err, dname):
    st = {}
    for m in re.finditer(r"^(\w+) \((\w+)\.\w+\.\w+\) \.\.\. ok$", err, re.M):
        st[f"{dname}/{m.group(2)}.{m.group(1)}"] = "pass"
    return st


def tests_read(ctx, p):
    return dict(ctx["last"])


def tests_noise(ctx, p, n):
    return


def tests_cmd(p, which):
    f = p["fault"]
    d, pat = p["dir"], "test_*.py"
    if which in ("main", "retry"):
        if f == "wrong_target":
            d = p["bad_dir"]
        if f == "bad_arg":
            pat = "tests_*.py"
        return ["python", "-m", "unittest", "discover", "-s", d, "-p", pat, "-v"]
    return ["python", "-m", "unittest", "discover", "-s", d, "-p", pat, "-v"] + (["-f"] if f == "blocked" else [])


def tests_step(ctx, p, which):
    if which == "repair" and p["fault"] == "swallowed":
        for mod in {m for m, _ in p["names"]}:
            fp = os.path.join(ROOT, p["dir"], f"{mod}.py")
            txt = open(fp).read().replace('    @unittest.skip("later")\n', "")
            with open(fp, "w") as fh:
                fh.write(txt)
    cmd = tests_cmd(p, which)
    rc, out, err = run([PY if c == "python" else c for c in cmd], ROOT, timeout=4.0)
    dname = cmd[cmd.index("-s") + 1]
    ctx["last"] = parse_tests(err, dname)
    return cmd, rc, out, err


def tests_classify(rc, out, err, p):
    t = err
    if rc == 0:
        return "A" if "skipped" in t else "0"
    if re.search(r"temporarily unavailable", t):
        return "T"
    if re.search(r"NO TESTS RAN|Ran 0 tests", t):
        return "A"
    if re.search(r"AssertionError|FAIL", t):
        return "H"
    return "?"


# ===================================================================================================== driver
KINDS = {
    "git": (git_setup, git_read, git_noise, git_step, None, git_classify),
    "db": (db_setup, db_read, db_noise, db_step, None, db_classify),
    "http": (http_setup, http_read, http_noise, http_step, None, http_classify),
    "build": (build_setup, build_read, build_noise, build_step, build_prepare_second, build_classify),
    "tests": (tests_setup, tests_read, tests_noise, tests_step, None, tests_classify),
}
ARM = {"db": db_arm}
RELEASE = {"db": db_release}


def run_plan(spec):
    """One fresh sandbox: setup, before-readback, the main step, after-readback. Unless the fault is ok / already_done,
    then the SAME step again (retry) and, if the retry did not make the intended effect hold, the repaired step (repair),
    each followed by a readback. (A retry that does not fix leaves the state as it was for every fault in the catalogue,
    so the repair starts from the post-main state; the tests check this.)"""
    global ROOT
    kind, p = spec["kind"], spec["params"]
    setup, read, noise, step, prep2, classify = KINDS[kind]
    ROOT = os.path.realpath(tempfile.mkdtemp(prefix="t45_"))
    try:
        ctx, intent = setup(p)
        out = {"intent": intent, "before": read(ctx, p)}
        if kind in ARM:
            ARM[kind](ctx, p)
        cmd, rc, o_, e_ = step(ctx, p, "main")
        if kind in RELEASE:
            RELEASE[kind](ctx, p)
        out["main"] = {"cmd": " ".join(cmd), "exit": rc, "cls": classify(rc, o_, e_, p), "after": read(ctx, p)}
        out["debug"] = {"out": o_[-300:], "err": e_[-300:]}
        if p["fault"] not in ("ok", "already_done"):
            for which in ("retry", "repair"):
                if which == "retry" and prep2:
                    prep2(ctx, p, which)
                cmd2, rc2, o2, e2 = step(ctx, p, which)
                st = read(ctx, p)
                out[which] = {"cmd": " ".join(cmd2), "exit": rc2, "after": st}
                if all(st.get(k) == v for k, v in intent.items()) and rc2 == 0:
                    break
        if kind == "http":
            ctx["srv"].shutdown()
            ctx["srv"].server_close()
    finally:
        for dp, dn, fn in os.walk(ROOT):
            try:
                os.chmod(dp, 0o755)
            except OSError:
                pass
        shutil.rmtree(ROOT, ignore_errors=True)
    return out


def main():
    spec = json.load(sys.stdin)
    try:
        out = run_plan(spec)
    except EnvError as e:
        sys.stderr.write(f"T45-ENV: {e}\n")
        sys.exit(97)
    json.dump(out, sys.stdout, sort_keys=True)


if __name__ == "__main__":
    main()
