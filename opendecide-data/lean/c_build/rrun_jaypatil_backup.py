#!/usr/bin/env python3
"""rrun: run one family command unchanged in a Modal CPU container, then copy its outputs back (PREREG_FINAL A20 a).

  .venv/bin/python lean/c_build/rrun.py --fam F5 [--cpu 16] [--mem 32] [--timeout 3h] [--sync-back REL ...]
        [--exclude REL ...] [--in LEANREL ...] [--out LEANREL ...] [--all-fams] [--sync-on-fail] [--sync-to DIR]
        [--plan] -- <command>

The command runs with cwd = lean/c_src/<FAM>, at the SAME absolute paths as on the Mac, with the venv's exact package
versions (Python 3.12.10, CPU torch) and MiniLM-L6 + the Qwen3.5-4B tokenizer baked into an offline HF cache.
One argument after `--` = a shell string (bash -c); several = an argv list.
Uploaded (Modal content-hashed mounts): c_src/<FAM> + c_src/{common,formats,packs,public,COMMIT} + c_src top-level
files (all families with --all-fams), INCLUDING */tmp/** (minus --exclude paths), minus caches, __pycache__ and
*.npz; lean/{decoder_io,train_decoder,prism_x,writeblock}.py, PREREG_FINAL.md, three c_spec files; --in and existing
--out paths. Every uploaded path is checked against the never-open list and symlinks are refused (fail closed).
rrun's own stdout/stderr file is never uploaded; a *.log/*.out/*.err another job writes during the upload is skipped
and the upload retried (WARN); any other file changing during the upload aborts the launch ($0).
Nothing under lean/sealed_nd is uploaded: each sealed_nd/qc/*.py is replaced by a stub that exits 97 and marks the run
FAILED, so a sealed check can never pass remotely (run sealed checks on the Mac).
Sync back (three-way): files the job created or changed under c_src/<FAM> (filtered by --sync-back) and under --out.
A local file is overwritten only if it still equals the copy that was uploaded (sha256); a file the job created is
written only if no local file appeared meanwhile; every other case lands as <name>.remote (warned). If the job failed
(rc != 0, budget kill, sealed stub hit, stdout held by an orphan), everything lands as .remote unless --sync-on-fail.
Changes outside the synced roots are listed as WARN. Local mtimes are the sync time (never backdated).
Cost guard: c_build/rrun_ledger.jsonl. The container gets HARD limits equal to the request (cpu=(c, c),
memory=(m, m)), so Modal bills exactly the request (a job above --mem is OOM-killed, not billed more). Each launch
first writes a locked reservation for its worst case (request rate x (container timeout + 60 s), the timeout being
min(--timeout, what is left under $15)); open reservations count in the total; the row is settled with the estimate
at the end. No launch once max(ledger, billing report + open reservations) would pass $15. logs/budget_ledger.md gets
one fixed-width 'rrun running total' row, rewritten in place on every settle (never duplicated, so not additive), plus
one marker row at $5 and at $10. `rrun.py --budget-row` refreshes that row alone. Profile jaypatil-duke, app od-rrun.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import io
import json
import os
import re
import shlex
import signal
import sys
import tarfile
import time
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
REPO = LEAN.parent
HOME = Path("/Users/aryamahadik")
CSRC, CBUILD = LEAN / "c_src", LEAN / "c_build"
PROGRESS = CBUILD / "progress_phase2.log"
LEDGER = CBUILD / "rrun_ledger.jsonl"
LOCK = CBUILD / ".rrun_ledger.lock"
BUDGET_MD = LEAN / "logs/budget_ledger.md"
LOGDIR = CBUILD / "rrun_logs"
PROFILE, APP_NAME = "jaypatil-duke", "od-rrun"
CAP_USD, MILESTONES = 15.0, (5.0, 10.0)
CPU_RATE, MEM_RATE = 0.0000131, 0.00000222   # $/physical core/s, $/GiB/s (Modal list prices, CPU containers)
# Modal bills max(request, usage); without a limit a container may use request + 16 cores (seen: 2->18 ... 16->32) and
# memory above the request. rrun sets hard limits = request, so billing = request and the reservation is the worst case.
CPU_BURST = 1.0
BUDGET_TAG, BUDGET_ROW_W = "| rrun running total |", 400   # fixed-width row in logs/budget_ledger.md
BILLING_CACHE = CBUILD / "rrun_billing.json"
STAGE = "/rrun_stage"                         # mounts land here; copied to the real absolute paths at start
PYVER = "3.12.10"
QWEN = ("Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
MINILM = ("sentence-transformers/all-MiniLM-L6-v2", "1110a243fdf4706b3f48f1d95db1a4f5529b4d41")
HF_LOCAL = Path.home() / ".cache/huggingface/hub"
ROOT_PKGS = ["numpy", "scipy", "scikit-learn", "pandas", "sentence-transformers", "transformers", "tokenizers",
             "huggingface-hub", "hf-xet", "safetensors", "PyYAML", "datasketch", "requests", "xxhash", "pytest",
             "beautifulsoup4", "joblib", "threadpoolctl", "regex", "tqdm", "Jinja2", "filelock", "packaging"]
SKIP_PKGS = re.compile(r"^(torch|triton|nvidia-.*|modal|pip|setuptools|wheel)$", re.I)
SHARED = ["common", "formats", "packs", "public", "COMMIT"]
LEAN_FILES = ["decoder_io.py", "train_decoder.py", "prism_x.py", "writeblock.py", "PREREG_FINAL.md",
              "c_spec/C_DATA_SPEC.md", "c_spec/C_TRAIN_RECIPE.md", "c_spec/LICENCE_REGISTER.md"]
SEALED_QC = LEAN / "sealed_nd/qc"             # names of its *.py files are listed (never opened) to place stubs
SEALED_RC, SEALED_MARK = 97, "/rrun_sealed_called"
# never-open / never-upload (lean-relative): checked on every uploaded file and every --in/--out/--exclude path
# (RESEARCH_/REVIEW_/LICENCE_CHECK_ are upper-case names in the never-open list: matched case-sensitively, so family
# files such as public-1/tmp/fix/review_check_rows_v11.json are not refused; everything else is case-insensitive)
# ('ohs3', 'preds_ohs' and 'jev' match ANYWHERE in the path, e.g. tmp/check_ohs3.json, x.OHS3, my_preds_ohs.json)
_DENY_I = re.compile(r"(^|/)(sealed_brief|prep89|bench)(/|$)|ohs3|preds_ohs|"
                     r"ADDENDUM_research\.md$|jev|^sealed_nd(/|$)|(^|/)\.\.(/|$)", re.I)
_DENY_C = re.compile(r"(^|/)(RESEARCH_|REVIEW_|LICENCE_CHECK_)[^/]*$")


def denied(rel: str) -> bool:
    return bool(_DENY_I.search(rel) or _DENY_C.search(rel))
IGN_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache", "cache", ".git", ".venv"}
IGN_SUFFIX = (".npz", ".pyc", ".pyo", ".rrun_tmp")


def log(m):
    print(f"[rrun {dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%SZ')}] {m}", flush=True)


def parse_secs(s):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([smhd]?)", s.strip())
    if not m:
        raise SystemExit(f"bad --timeout {s!r} (e.g. 90m, 3h)")
    return int(float(m[1]) * {"": 1, "s": 1, "m": 60, "h": 3600, "d": 86400}[m[2]])


def pins():
    """Exact local versions of ROOT_PKGS and their (linux, no-extra) dependency closure; torch handled apart."""
    import importlib.metadata as md
    from packaging.markers import default_environment
    from packaging.requirements import Requirement
    env = dict(default_environment(), sys_platform="linux", platform_system="Linux", platform_machine="x86_64",
               os_name="posix", platform_release="", platform_version="", extra="")
    seen, todo, out = set(), list(ROOT_PKGS), {}
    while todo:
        n = re.sub(r"[-_.]+", "-", todo.pop()).lower()
        if n in seen:
            continue
        seen.add(n)
        try:
            dist = md.distribution(n)
        except md.PackageNotFoundError:
            continue
        if not SKIP_PKGS.match(n):
            out[n] = dist.version
        for r in dist.requires or []:
            req = Requirement(r)
            if req.marker is None or req.marker.evaluate(env):
                todo.append(req.name)
    return [f"{k}=={v}" for k, v in sorted(out.items())], md.version("torch")


def hf_files(repo, rev):
    """Relative file list + sha256 of the local HF snapshot (the image must hold the same bytes)."""
    snap = HF_LOCAL / f"models--{repo.replace('/', '--')}" / "snapshots" / rev
    if not snap.is_dir():
        raise SystemExit(f"local HF snapshot missing: {repo}@{rev}")
    files = sorted(str(p.relative_to(snap)) for p in snap.rglob("*") if p.is_file())
    return {f: cached_sha256((snap / f).resolve()) for f in files}


def bake_cmd():
    spec = {repo: [rev, hf_files(repo, rev)] for repo, rev in (QWEN, MINILM)}
    code = (
        "import json,hashlib,pathlib\n"
        "from huggingface_hub import snapshot_download as s\n"
        f"S=json.loads({json.dumps(json.dumps(spec))})\n"
        "for repo,(rev,files) in S.items():\n"
        "    p=pathlib.Path(s(repo,revision=rev,allow_patterns=sorted(files)))\n"
        "    for f,h in files.items():\n"
        "        assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h,(repo,f)\n"
        "    r=p.parent.parent/'refs'; r.mkdir(exist_ok=True); (r/'main').write_text(rev)\n"
        "print('baked',list(S))\n")
    import base64
    b64 = base64.b64encode(code.encode()).decode()
    return f"python -c \"import base64; exec(base64.b64decode('{b64}'))\""


STUB_CODE = ("import sys\n"
             f"open({SEALED_MARK!r}, 'a').write(' '.join(sys.argv) + '\\n')\n"
             "sys.stderr.write('rrun: lean/sealed_nd programs never run in the cloud (A20 a review); run this step on "
             "the Mac\\n')\n"
             f"sys.exit({SEALED_RC})\n")


def _remote(spec):
    """Runs in the container (stdlib only): stage -> real paths, snapshot (+sha of sync roots), run, diff, tar."""
    import hashlib, io, os, signal, subprocess, tarfile, threading, time  # noqa: E401
    from concurrent.futures import ThreadPoolExecutor
    t0 = time.time()
    subprocess.run(["cp", "-a", f"{spec['stage']}/.", "/"], check=True)
    for d in spec["mkdirs"]:
        os.makedirs(d, exist_ok=True)
    for p in spec["stubs"]:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(spec["stub_code"])
    os.makedirs(os.path.dirname(spec["progress"]), exist_ok=True)
    open(spec["progress"], "w").close()

    def under(p, roots):
        return any(p == r or p.startswith(r.rstrip("/") + "/") for r in roots)

    def walk(top):
        out = {}
        for dp, dn, fn in os.walk(top):
            dn[:] = [d for d in dn if d not in ("__pycache__", ".pytest_cache")]
            for f in fn:
                p = os.path.join(dp, f)
                if not os.path.islink(p) and not f.endswith((".pyc", ".pyo")):
                    st = os.stat(p)
                    out[p] = (st.st_size, st.st_mtime_ns)
        return out

    def sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        return h.hexdigest()

    def shas(paths):
        with ThreadPoolExecutor(16) as ex:
            return dict(zip(paths, ex.map(sha, paths)))
    roots = [spec["famdir"]] + spec["outs"]
    before = walk(spec["home"])
    base = shas([p for p in before if under(p, roots)])     # = the uploaded copy of every file in the sync roots
    t_copy = time.time() - t0
    t_run0 = time.time()
    proc = subprocess.Popen(["bash", "-c", spec["cmd"]], cwd=spec["famdir"], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, start_new_session=True)
    tail = []

    def reader():
        for raw in iter(proc.stdout.readline, b""):
            line = raw.decode("utf-8", "replace")
            print(line, end="", flush=True)
            tail.append(line)
            if len(tail) > 20000:
                del tail[:5000]
    th = threading.Thread(target=reader, daemon=True)
    th.start()
    killed = False
    try:
        cmd_rc = proc.wait(timeout=spec["budget_s"])
    except subprocess.TimeoutExpired:
        killed = True
        os.killpg(proc.pid, signal.SIGKILL)
        cmd_rc = proc.wait()
    leftover = False
    try:
        os.killpg(proc.pid, signal.SIGKILL)       # background children the command left in its process group
        leftover = True
    except (ProcessLookupError, PermissionError):
        pass
    th.join(30)
    orphan = th.is_alive()                        # something outside the group (setsid) still holds stdout
    t_run = time.time() - t_run0
    time.sleep(0.5)
    sealed = os.path.exists(spec["sealed_mark"])
    after = walk(spec["home"])
    skip = {spec["progress"]} | set(spec["stubs"])
    changed = sorted(p for p, v in after.items() if before.get(p) != v and p not in skip)
    deleted = sorted(p for p in before if p not in after and p not in skip)
    keep = spec["sync_back"]
    synced = [p for p in changed if under(p, spec["outs"]) or (under(p, [spec["famdir"]]) and (not keep or
                                                                                                 under(p, keep)))]
    unsynced = [p for p in changed if p not in set(synced)]
    new = shas(synced)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz", compresslevel=3) as tf:
        for p in synced:
            tf.add(p, arcname=p.lstrip("/"), recursive=False)
    prog = open(spec["progress"], errors="replace").read()
    rc = spec["sealed_rc"] if sealed else cmd_rc
    return {"rc": rc, "cmd_rc": cmd_rc, "killed_at_budget": killed, "sealed_called": sealed, "orphan_stdout": orphan,
            "leftover_group": leftover, "t_copy": round(t_copy, 1), "t_run": round(t_run, 1),
            "t_total": round(time.time() - t0, 1),
            "files": {p: [after[p][0], base.get(p), new[p]] for p in synced},
            "unsynced": unsynced[:200], "n_unsynced": len(unsynced), "deleted": deleted[:200], "n_deleted": len(deleted),
            "tar": buf.getvalue(), "progress": prog, "log_tail": "".join(tail[-4000:]),
            "cpu_count": os.cpu_count(), "uname": " ".join(os.uname())}


def lean_rel(p):
    """Validate a lean-relative path (no never-open / OHS-3 / bench / jev / sealed / '..')."""
    p = p.strip().lstrip("./") if not p.startswith("/") else str(Path(p).resolve().relative_to(LEAN))
    if not p or denied(p):
        raise SystemExit(f"refused path (never-open or outside the allowed set): {p!r}")
    return p


def make_skip(excl=()):
    """Plain upload filter (True = skip): caches, bytecode, *.npz, --exclude paths. tmp/** IS uploaded."""
    excl = [tuple(Path(e).parts) for e in excl]

    def skip(rel: Path):
        parts = rel.parts
        return (any(x in IGN_DIRS for x in parts) or rel.name.endswith(IGN_SUFFIX)
                or any(parts[:len(e)] == e for e in excl))
    return skip


LIVE_SKIP: set = set()   # absolute paths never uploaded because they are being written: rrun's own stdout/stderr
LIVE_SUFFIX = (".log", ".out", ".err")   # and log files another job was writing during the upload (retried once each)


def own_logs():
    """(dev, inode) of this process's stdout/stderr when they are regular files (nohup ... > log 2>&1)."""
    out = set()
    for fd in (1, 2):
        try:
            st = os.fstat(fd)
            if (st.st_mode & 0o170000) == 0o100000:
                out.add((st.st_dev, st.st_ino))
        except OSError:
            pass
    return out


OWN_LOGS = own_logs()


def guarded(base: Path, skip):
    """The ignore Modal uses: skip() plus never-open names, symlinks (defence in depth; preflight refuses them) and
    LIVE_SKIP log files."""
    brel = base.relative_to(LEAN)

    def ign(rel: Path):
        return (skip(rel) or (denied((brel / rel).as_posix())) or (base / rel).is_symlink()
                or str(base / rel) in LIVE_SKIP)
    return ign


def plan_mounts(a):
    """[(local, kind, skip)] for every upload; kind = dir | file. Nothing under sealed_nd. tmp/** included."""
    lean_ex = [e for e in a.exclude if e.startswith("c_src/")]

    def ex_for(sub):
        pre = f"c_src/{sub}/"
        return [e[len(pre):] for e in lean_ex if e.startswith(pre)]
    m = [(CSRC / a.fam, "dir", make_skip([e for e in a.exclude if not e.startswith("c_src/")] + ex_for(a.fam)))]
    subs = SHARED + ([p.name for p in sorted(CSRC.glob("F*")) if p.is_dir() and p.name != a.fam] if a.all_fams else [])
    m += [(CSRC / s, "dir", make_skip(ex_for(s))) for s in subs if (CSRC / s).is_dir()]
    m += [(p, "file", None) for p in sorted(CSRC.iterdir()) if p.is_file() and not p.name.startswith(".")]
    m += [(LEAN / f, "file", None) for f in LEAN_FILES if (LEAN / f).is_file()]
    for p in a.inp + a.out:
        q = LEAN / lean_rel(p)
        if not q.exists():
            if p in a.inp:
                raise SystemExit(f"--in {p}: not found")
            continue                                   # a new --out path: nothing to upload
        if any(k == "dir" and (q == loc or loc in q.parents) for loc, k, _ in m):
            continue                                   # already inside an uploaded dir
        m.append((q, "dir" if q.is_dir() else "file", make_skip()))
    return m


def preflight(m):
    """Walk exactly what Modal will upload: count, bytes, dirs; collect never-open names and symlinks (fail closed)."""
    n = b = 0
    bad, dirs = [], []
    for local, kind, skip in m:
        brel = local.relative_to(LEAN)
        if local.is_symlink() or denied(brel.as_posix()):
            bad.append(brel.as_posix())
            continue
        if kind == "file":
            n, b = n + 1, b + local.stat().st_size
            continue
        for dp, dn, fn in os.walk(local):
            rd = Path(dp).relative_to(local)
            keep = []
            for d in dn:
                if skip(rd / d):
                    continue
                if (Path(dp) / d).is_symlink() or denied((brel / rd / d).as_posix()):
                    bad.append((brel / rd / d).as_posix())
                else:
                    keep.append(d)
            dn[:] = keep
            dirs.append(dp)
            for f in fn:
                if skip(rd / f):
                    continue
                if (Path(dp) / f).is_symlink() or denied((brel / rd / f).as_posix()):
                    bad.append((brel / rd / f).as_posix())
                else:
                    st = os.stat(os.path.join(dp, f))
                    if (st.st_dev, st.st_ino) in OWN_LOGS:          # our own log: being written, never uploaded
                        LIVE_SKIP.add(os.path.join(dp, f))
                        continue
                    n, b = n + 1, b + st.st_size
    return n, b, bad, dirs


def sealed_stubs():
    """Real paths of the sealed_nd/qc programs (names only, never opened) -> fail-closed stubs in the container."""
    try:
        names = {e.name for e in os.scandir(SEALED_QC) if e.name.endswith(".py")}
    except OSError:
        names = set()
    return [str(SEALED_QC / x) for x in sorted(names | {"sealed_check.py"})]


def est_usd(secs, cpu, mem_gib):
    return round(secs * (cpu * CPU_RATE * CPU_BURST + mem_gib * MEM_RATE), 4)


# ---- upload hash cache (speed only): Modal re-hashes every mounted file on every launch (~60 s for 560 MB on the
# loaded Mac). A file's sha256/md5 is reused only when (size, mtime_ns, ctime_ns, inode) are unchanged; ctime moves on
# every write and cannot be set by tools, and files touched < 2 s before hashing are never cached (racy-git rule), so
# a cached hash always belongs to the bytes on disk. The remote base sha (three-way sync) is computed in the container.
HASH_CACHE, HASH_LOCK = CBUILD / ".rrun_hash_cache.json", CBUILD / ".rrun_hash_cache.lock"
_HC: dict | None = None
_HC_NEW: dict = {}


def _sig(st):
    return [st.st_size, st.st_mtime_ns, st.st_ctime_ns, st.st_ino]


def _hc_get(p, st):
    global _HC
    if _HC is None:
        try:
            _HC = json.loads(HASH_CACHE.read_text())
        except (OSError, ValueError):
            _HC = {}
    v = _HC.get(str(p))
    return v[1] if v and v[0] == _sig(st) else None


def _hc_put(p, st0, val, t0):
    st = os.stat(p)
    old = (t0 - 2) * 1e9
    if _sig(st) == _sig(st0) and st.st_ctime_ns < old and st.st_mtime_ns < old:
        _HC_NEW[str(p)] = [_sig(st), val]


def _hc_save():
    if not _HC_NEW:
        return
    with open(HASH_LOCK, "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            cur = json.loads(HASH_CACHE.read_text())
        except (OSError, ValueError):
            cur = {}
        cur.update(_HC_NEW)
        if len(cur) > 60000:
            cur = {k: v for k, v in cur.items() if os.path.exists(k)}
        tmp = HASH_CACHE.with_name(HASH_CACHE.name + ".tmp")
        tmp.write_text(json.dumps(cur))
        os.replace(tmp, HASH_CACHE)


def cached_sha256(p: Path):
    t0, st = time.time(), os.stat(p)
    hit = _hc_get(p, st)
    if hit:
        return hit[0]
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    _hc_put(p, st, [h, None], t0)
    return h


def patch_modal_hashing(modal):
    """Wrap Modal 1.5.5's per-file spec builder with the cache; any other Modal version hashes as usual."""
    import modal.mount as mm
    from modal._utils import blob_utils as bu
    if modal.__version__ != "1.5.5" or not hasattr(mm, "get_file_upload_spec_from_path"):
        log(f"note: modal {modal.__version__}: upload hash cache off")
        return
    orig = bu.get_file_upload_spec_from_path

    def spec(filename, mount_filename, mode=None):
        t0, st = time.time(), os.stat(filename)
        mode = mode or (st.st_mode & 0o7777)
        hit = _hc_get(filename, st)
        if hit and hit[1] is not None:
            return bu.FileUploadSpec(source=lambda: open(filename, "rb"), source_description=filename,
                                     source_is_path=True, mount_filename=mount_filename.as_posix(),
                                     use_blob=st.st_size >= bu.LARGE_FILE_LIMIT, sha256_hex=hit[0], md5_hex=hit[1],
                                     mode=mode & 0o7777, size=st.st_size, content=None)
        s = orig(filename, mount_filename, mode)
        if s.size == st.st_size:
            _hc_put(filename, st, [s.sha256_hex, s.md5_hex], t0)
        return s
    mm.get_file_upload_spec_from_path = spec


def _rows():
    out = []
    if LEDGER.exists():
        for x in LEDGER.read_text().splitlines():
            try:
                out.append(json.loads(x)) if x.strip() else None
            except ValueError:
                pass
    return out


def ledger_total(rows=None):
    """(total incl. open reservations, settled, open reservations $, settled runs, open reservations)."""
    rows = _rows() if rows is None else rows
    runs = [r for r in rows if r.get("kind", "run") == "run"]
    done = {r.get("run_id") for r in runs}
    opn = [r for r in rows if r.get("kind") == "reserve" and r.get("run_id") not in done]
    settled = sum(r.get("est_usd") or 0.0 for r in runs)
    res = sum(r.get("reserve_usd") or 0.0 for r in opn)
    return round(settled + res, 4), round(settled, 4), round(res, 4), len(runs), len(opn)


def billing_actual():
    """Real od-rrun spend this month from `modal billing report` (best effort; None if unavailable)."""
    import subprocess
    try:
        r = subprocess.run([str(REPO / ".venv/bin/modal"), "billing", "report", "--for", "this month",
                            "--show-resources", "--json", "--profile", PROFILE], capture_output=True, text=True,
                           timeout=90)
        rows = json.loads(r.stdout)
        usd = round(sum(float(x["cost"]) for x in rows if x.get("description") == APP_NAME), 4)
        apps = sorted({x["object_id"] for x in rows if x.get("description") == APP_NAME})
        BILLING_CACHE.write_text(json.dumps({"ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                                             "od_rrun_usd_this_month": usd, "apps": len(apps)}, indent=1))
        return usd
    except Exception:  # noqa: BLE001
        return None


def budget_for(a, rate, total, res, actual, timeout_s):
    """Worst case under the cap: guard = max(ledger incl. open reservations, billing + open reservations)."""
    guard = max(total, (actual or 0.0) + res)
    fn_timeout = min(timeout_s, int((CAP_USD - guard) / rate) - 60)
    budget_s = fn_timeout - min(300, max(60, fn_timeout // 5))   # in-container kill; the rest is for tar + return
    return guard, fn_timeout, budget_s


def reserve(run_id, a, rate, actual):
    """Locked: check the cap against settled runs + every open reservation, then write this run's reservation."""
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        total, settled, res, nruns, nopen = ledger_total()
        guard, fn_timeout, budget_s = budget_for(a, rate, total, res, actual, a.timeout_s)
        if guard >= CAP_USD or budget_s < 60:
            raise SystemExit(f"REFUSED: rrun spend ${guard:.2f} (settled ${settled:.2f} + {nopen} open reservations "
                             f"${res:.2f}) leaves no room under the ${CAP_USD:.0f} cap (A20 a)")
        row = {"kind": "reserve", "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
               "run_id": run_id, "fam": a.fam, "pid": os.getpid(), "cpu": a.cpu, "mem_gib": a.mem,
               "fn_timeout_s": fn_timeout, "budget_s": budget_s, "reserve_usd": est_usd(fn_timeout + 60, a.cpu, a.mem),
               "guard_before_usd": round(guard, 4)}
        with open(LEDGER, "a") as f:
            f.write(json.dumps(row) + "\n")
    return row, nruns, nopen


def write_budget_row(text):
    """Write the one fixed-width 'rrun running total' row of logs/budget_ledger.md. An existing row of the same width
    is overwritten in place (seek + write, no truncation), so lines other writers append (>>) are never lost."""
    if len(text) > BUDGET_ROW_W:                                  # keep the amount column, cut the description
        head, tail = text.rsplit(" | ", 1)
        text = head[:BUDGET_ROW_W - len(tail) - 3] + " | " + tail
    line = text.encode("ascii", "replace").ljust(BUDGET_ROW_W) + b"\n"
    data = BUDGET_MD.read_bytes() if BUDGET_MD.exists() else b""
    i = 0 if data.startswith(BUDGET_TAG.encode()) else data.find(b"\n" + BUDGET_TAG.encode())
    if i < 0:
        with open(BUDGET_MD, "ab") as f:
            f.write((b"" if not data or data.endswith(b"\n") else b"\n") + line)
        return "appended"
    i += 0 if data.startswith(BUDGET_TAG.encode()) else 1
    j = data.find(b"\n", i)
    if j - i == BUDGET_ROW_W:
        with open(BUDGET_MD, "r+b") as f:
            f.seek(i)
            f.write(line[:-1])
        return "rewritten"
    tmp = BUDGET_MD.with_name(BUDGET_MD.name + ".rrun_tmp")      # row was hand-edited: replace the file once
    tmp.write_bytes(data[:i] + line + (data[j + 1:] if j >= 0 else b""))
    os.replace(tmp, BUDGET_MD)
    return "replaced"


def budget_text(n, settled, nopen, res, actual, cached=None):
    now = dt.datetime.now(dt.timezone.utc).strftime("%-d %b %H:%M UTC")
    bill = (f"modal billing report ${actual:.2f} this month" if actual is not None else
            f"billing report unavailable (last cached {cached})")
    return (f"{BUDGET_TAG} {PROFILE} CPU (app {APP_NAME}, A20 a), updated {now}: {n} runs in "
            f"c_build/rrun_ledger.jsonl est ${settled:.2f} + {nopen} open reservations ${res:.2f}; {bill}; hard "
            f"CPU/mem limits = request; auto-stop $15. Running total, rewritten in place on every run (the milestone "
            f"rows are not additive) | ~${max(settled, actual or 0):.2f} [E] |")


def settle(rec, actual=None):
    """Locked: write the run row (closes its reservation), rewrite the running-total row, write milestone markers."""
    with open(LOCK, "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        with open(LEDGER, "a") as f:
            f.write(json.dumps(rec) + "\n")
        total, settled, res, n, nopen = ledger_total()
        spent = max(settled, actual or 0.0)
        try:
            write_budget_row(budget_text(n, settled, nopen, res, actual))
            done = BUDGET_MD.read_text() if BUDGET_MD.exists() else ""
            for m in MILESTONES:
                tag = f"| rrun milestone ${m:.0f} |"
                if spent >= m and tag not in done:
                    with open(BUDGET_MD, "a") as f:
                        f.write(f"{tag} {dt.datetime.now(dt.timezone.utc).strftime('%-d %b %H:%M UTC')}: "
                                f"{PROFILE} od-rrun spend passed ${m:.0f} (~${spent:.2f} at {n} runs); auto-stop at "
                                f"${CAP_USD:.0f} | marker only: amount is in the rrun running total row |\n")
                    log(f"budget milestone ${m:.0f} written to logs/budget_ledger.md")
        except OSError as e:
            log(f"WARN logs/budget_ledger.md not updated ({e!r}); the rrun ledger row is written")
    return settled, res


def append_progress(text, dest):
    if not text.strip():
        return 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(text if text.endswith("\n") else text + "\n")
    return len(text.splitlines())


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def decide(dst: Path, base, new):
    """Three-way rule. 'same' = local already equals the remote result; None = write in place; else the reason the
    remote copy goes to <name>.remote."""
    if dst.is_symlink() or (dst.exists() and not dst.is_file()):
        return "local path is not a regular file"
    if not dst.exists():
        return None if base is None else "local file was deleted after the upload"
    cur = sha_file(dst)
    if cur == new:
        return "same"
    if base is None:
        return "local file exists but was not uploaded (excluded, or created during the job)"
    return None if cur == base else "local file changed after the upload"


def unpack(tar_bytes, files, allowed, failed, sync_to=None):
    """Write synced files by the three-way rule; a failed job writes everything as .remote. Mtime = sync time.
    With sync_to the rule is still judged on the real local file, but everything is written under sync_to."""
    wrote, conflicts, same = [], [], 0
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tf:
        for mem in tf.getmembers():
            src = "/" + mem.name
            if (not mem.isfile() or ".." in Path(mem.name).parts or src not in files
                    or not any(src == r or src.startswith(r.rstrip("/") + "/") for r in allowed)):
                log(f"WARN skipped unexpected tar member {mem.name!r}")
                continue
            _, base, new = files[src]
            with tf.extractfile(mem) as r:
                data = r.read()
            reason = decide(Path(src), base, new)       # always judged against the real local file
            if hashlib.sha256(data).hexdigest() != new:
                reason = "remote file changed while it was being packed"
            elif reason == "same":
                same += 1
                if not sync_to:
                    continue
                reason = None
            dst = Path(sync_to) / mem.name if sync_to else Path(src)
            if failed and reason is None:
                reason = "job failed (" + failed + "); rerun with --sync-on-fail to sync in place"
            if reason:
                dst = dst.with_name(dst.name + ".remote")
                conflicts.append([str(dst), reason])
            dst.parent.mkdir(parents=True, exist_ok=True)
            tmp = dst.with_name(f".{dst.name}.rrun_tmp")
            with open(tmp, "wb") as w:
                w.write(data)
            os.chmod(tmp, mem.mode & 0o777 or 0o644)
            os.replace(tmp, dst)
            wrote.append(str(dst))
    if conflicts:
        kinds = {}
        for _, why in conflicts:
            kinds[why] = kinds.get(why, 0) + 1
        log(f"WARN {len(conflicts)} file(s) written as <name>.remote, local copy untouched: {kinds}; first: "
            f"{conflicts[0][0]}")
    return wrote, conflicts, same


def build_image(modal, mounts):
    p, torch_v = pins()
    img = (modal.Image.debian_slim(python_version=PYVER)
           .pip_install(f"torch=={torch_v}", index_url="https://download.pytorch.org/whl/cpu")
           .pip_install(*p)
           .env({"HF_HOME": "/root/.cache/huggingface", "TOKENIZERS_PARALLELISM": "false"})
           .run_commands(bake_cmd())
           .env({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"})
           .run_commands(f"mkdir -p {REPO}/.venv/bin && for b in python python3 pytest; do "
                         f"ln -sf $(command -v $b) {REPO}/.venv/bin/$b; done"))
    for local, kind, ign in mounts:
        remote = STAGE + str(local)
        img = img.add_local_file(local, remote) if kind == "file" else img.add_local_dir(
            local, remote, ignore=guarded(local, ign))
    return img



def parse(argv):
    if "--" not in argv:
        raise SystemExit("usage: rrun.py --fam F5 [opts] -- <command>   (see --help)" if "-h" not in argv and
                         "--help" not in argv else __doc__)
    i = argv.index("--")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fam", required=True)
    ap.add_argument("--cpu", type=float, default=16)
    ap.add_argument("--mem", type=float, default=32, help="GiB")
    ap.add_argument("--timeout", default="3h")
    ap.add_argument("--sync-back", nargs="*", default=[], help="relpaths under c_src/<FAM> (default: all changes)")
    ap.add_argument("--exclude", nargs="*", default=[], help="skip big inputs the job does not read: relpaths under "
                    "c_src/<FAM>, or lean-relative c_src/<shared>/... paths (absent remotely!)")
    ap.add_argument("--need", nargs="*", default=[], help="obsolete (tmp/** is uploaded by default); accepted")
    ap.add_argument("--in", dest="inp", nargs="*", default=[], help="extra lean-relative inputs")
    ap.add_argument("--out", nargs="*", default=[], help="extra lean-relative outputs to sync back (uploaded first "
                    "if they exist, so the three-way rule can apply)")
    ap.add_argument("--all-fams", action="store_true", help="also upload the other families' folders")
    ap.add_argument("--sync-on-fail", action="store_true", help="sync a failed job's files by the normal rule")
    ap.add_argument("--sync-to", default=None, help="unpack under this dir instead of in place (tests)")
    ap.add_argument("--plan", action="store_true", help="print the upload plan and cost bound; run nothing")
    a = ap.parse_args(argv[:i])
    cmdv = argv[i + 1:]
    if not cmdv:
        raise SystemExit("no command after --")
    if not re.fullmatch(r"F\d{1,2}", a.fam) or not (CSRC / a.fam).is_dir():
        raise SystemExit(f"--fam {a.fam}: not a family folder under c_src/")
    for r in a.sync_back + a.need + a.exclude:
        if r.startswith("/") or ".." in Path(r).parts:
            raise SystemExit(f"{r!r}: must be a relpath under c_src/{a.fam} (or c_src/<shared>/...)")
        lean_rel(r if r.startswith("c_src/") and r not in a.sync_back else f"c_src/{a.fam}/{r}")
    a.cmd = cmdv[0] if len(cmdv) == 1 else shlex.join(cmdv)
    a.timeout_s = parse_secs(a.timeout)
    return a


def under(p, roots):
    return any(str(p) == str(r) or str(p).startswith(str(r).rstrip("/") + "/") for r in roots)


def _on_term(*_):
    raise SystemExit("SIGTERM: run settled in the ledger")


def refresh_budget_row():
    """`rrun.py --budget-row`: refresh the billing cache and the running-total row of logs/budget_ledger.md."""
    actual = billing_actual()
    with open(LOCK, "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        total, settled, res, n, nopen = ledger_total()
        cached = json.loads(BILLING_CACHE.read_text()).get("ts") if BILLING_CACHE.exists() else None
        how = write_budget_row(budget_text(n, settled, nopen, res, actual, cached))
    log(f"budget row {how}: {n} runs, ledger ${settled:.4f} + open ${res:.4f}, billing report {actual}")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv == ["--budget-row"]:
        return refresh_budget_row()
    a = parse(argv)
    famdir = CSRC / a.fam
    outs = [str(LEAN / lean_rel(o)) for o in a.out]
    mounts = plan_mounts(a)
    n_up, b_up, bad, dirs = preflight(mounts)
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} upload path(s) are never-open names or symlinks; first: {bad[0]} "
                         f"(remove it or pass --exclude)")
    if a.need:
        log("note: --need is obsolete; tmp/** is uploaded by default")
    if LIVE_SKIP:
        log(f"note: own log file(s) inside the upload are not uploaded: {sorted(LIVE_SKIP)}")
    total, settled, res, nruns, nopen = ledger_total()
    actual = None if a.plan else billing_actual()
    rate = a.cpu * CPU_RATE * CPU_BURST + a.mem * MEM_RATE
    guard, fn_timeout, budget_s = budget_for(a, rate, total, res, actual, a.timeout_s)
    cmd_sha = hashlib.sha256(a.cmd.encode()).hexdigest()
    stubs = sealed_stubs()
    log(f"{a.fam}: cmd sha {cmd_sha[:12]}; upload {n_up} files {b_up / 1e6:.1f} MB (content-hashed; 0 never-open, "
        f"0 symlinks); cpu {a.cpu} mem {a.mem} GiB; ${rate * 3600:.3f}/h; container timeout {fn_timeout}s, job "
        f"budget {budget_s}s (worst ${est_usd(fn_timeout + 60, a.cpu, a.mem)}); spend ${guard:.3f} of "
        f"${CAP_USD:.0f} ({nruns} settled runs, {nopen} open reservations ${res:.3f}); {len(stubs)} sealed stub(s)")
    if a.plan:
        for local, kind, _ in mounts:
            print(f"  {kind:4s} {local}")
        return 0
    run_id = f"{time.strftime('%Y%m%dT%H%M%S')}_{a.fam}_{cmd_sha[:8]}_{os.getpid()}"
    row, _, _ = reserve(run_id, a, rate, actual)
    fn_timeout, budget_s = row["fn_timeout_s"], row["budget_s"]
    log(f"reserved ${row['reserve_usd']:.3f} (worst case, container timeout {fn_timeout}s) as {run_id}")
    signal.signal(signal.SIGTERM, _on_term)
    t_launch, tc0, res, err, app_id = time.time(), None, None, None, None
    mk = [d for d in dirs if under(d, [famdir])][:20000]
    mk += [o if Path(o).is_dir() else str(Path(o).parent) for o in outs]
    spec = {"stage": STAGE, "famdir": str(famdir), "outs": outs, "cmd": a.cmd, "progress": str(PROGRESS),
            "mkdirs": mk, "budget_s": budget_s, "home": str(HOME), "stubs": stubs, "stub_code": STUB_CODE,
            "sealed_mark": SEALED_MARK, "sealed_rc": SEALED_RC, "sync_back": [str(famdir / r) for r in a.sync_back]}
    try:
        os.environ["MODAL_PROFILE"] = PROFILE
        import modal
        patch_modal_hashing(modal)
        mem_mb = int(a.mem * 1024)
        for attempt in range(4):
            app = modal.App(APP_NAME)
            img = build_image(modal, mounts)
            fn = app.function(image=img, cpu=(float(a.cpu), float(a.cpu)), memory=(mem_mb, mem_mb),
                              timeout=fn_timeout, serialized=True, name="rrun", retries=0)(_remote)  # hard limits
            try:
                with modal.enable_output():
                    with app.run():
                        tc0 = time.time()
                        app_id = getattr(app, "app_id", None)
                        res = fn.remote(spec)
                break
            except modal.exception.ExecutionError as e:
                m = re.match(r"(/.+?) was modified during build process", str(e))
                if not (m and tc0 is None and attempt < 3 and m[1].endswith(LIVE_SUFFIX) and m[1] not in LIVE_SKIP
                        and any(k == "dir" and under(m[1], [loc]) for loc, k, _ in mounts)):
                    raise
                LIVE_SKIP.add(m[1])                     # a log another job is writing: skip it and retry the upload
                log(f"WARN {m[1]} was being written during the upload: not uploaded (retry {attempt + 1}); keep "
                    f"nohup logs outside c_src/")
    except BaseException as e:  # noqa: BLE001 (settled in the ledger, then re-raised below)
        err = e
    try:
        _hc_save()
    except Exception as e:  # noqa: BLE001 (cache is optional)
        log(f"note: hash cache not saved ({e!r})")
    t_call = time.time() - tc0 if tc0 else 0.0
    wall = time.time() - t_launch
    cost = est_usd(t_call, a.cpu, a.mem)
    rec = {"kind": "run", "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "run_id": run_id,
           "fam": a.fam, "cmd_sha256": cmd_sha, "cmd": a.cmd[:300], "cpu": a.cpu, "mem_gib": a.mem,
           "timeout_s": a.timeout_s, "fn_timeout_s": fn_timeout, "budget_s": budget_s, "billed_s_est": round(t_call, 1),
           "wall_s": round(wall, 1), "build_s": round((tc0 or time.time()) - t_launch, 1), "est_usd": cost,
           "rc": res["rc"] if res else None, "error": repr(err)[:300] if err else None, "profile": PROFILE,
           "app": APP_NAME, "app_id": app_id, "not_uploaded_live_logs": sorted(LIVE_SKIP)[:20], "cpu_limit": a.cpu, "mem_limit_gib": a.mem, "upload_files": n_up, "upload_mb": round(b_up / 1e6, 1)}
    if res:
        rec.update({k: res[k] for k in ("cmd_rc", "t_copy", "t_run", "t_total", "killed_at_budget", "sealed_called",
                                        "orphan_stdout", "leftover_group", "cpu_count", "n_unsynced", "n_deleted")})
    total, open_res = settle(rec, actual)
    if err is not None:
        log(f"FAILED before a result ({type(err).__name__}); est ${cost} settled; spend ${total:.3f}")
        raise err
    why = [w for w, c in (("rc=%s" % res["cmd_rc"], res["cmd_rc"] != 0), ("killed at budget", res["killed_at_budget"]),
                          ("sealed stub called", res["sealed_called"]), ("orphan held stdout", res["orphan_stdout"]))
           if c]
    failed = "; ".join(why) if why and not a.sync_on_fail else ""
    rc = res["rc"] or (98 if why else 0)          # a failed run never exits 0 (orphan stdout -> 98)
    LOGDIR.mkdir(parents=True, exist_ok=True)
    wrote, conflicts, same = unpack(res["tar"], res["files"], [str(famdir)] + outs, failed, a.sync_to)
    pdest = Path(a.sync_to) / "progress_phase2.log" if a.sync_to else PROGRESS
    n_prog = 0 if failed else append_progress(res["progress"], pdest)
    if res["sealed_called"]:
        log("WARN the job called a lean/sealed_nd program; it never runs in the cloud (stub rc 97): run that step on "
            "the Mac. The run counts as FAILED.")
    if failed and res["progress"].strip():
        log(f"WARN job failed ({failed}): its {len(res['progress'].splitlines())} progress line(s) are only in the "
            f"run log, not in progress_phase2.log")
    if res["n_unsynced"]:
        log(f"WARN {res['n_unsynced']} file(s) changed remotely outside the synced roots (not copied back; add --out "
            f"or drop --sync-back filters): " + ", ".join(res["unsynced"][:10]))
    if res["n_deleted"]:
        log(f"WARN {res['n_deleted']} file(s) deleted remotely (deletions are not mirrored): "
            + ", ".join(res["deleted"][:5]))
    if res["leftover_group"]:
        log("note: the command left processes in its group at exit; they were killed before the diff")
    rec.update({"failed": failed or None, "synced": len(wrote), "same": same, "conflicts": conflicts,
                "progress_lines": n_prog, "tar_mb": round(len(res["tar"]) / 1e6, 2), "uname": res["uname"],
                "unsynced": res["unsynced"][:50], "deleted": res["deleted"][:50], "spend_usd": total,
                "open_reservations_usd": open_res, "exit_rc": rc, "why_failed": "; ".join(why) or None})
    (LOGDIR / f"{run_id}.log").write_text(json.dumps(rec, indent=1) + "\n----- progress lines -----\n"
                                          + res["progress"] + "\n----- log tail -----\n" + res["log_tail"])
    log(f"done rc={rc}{' FAILED: ' + '; '.join(why) if why else ''}; run {res['t_run']}s (container "
        f"{res['t_total']}s, call {t_call:.0f}s, wall {wall:.0f}s); synced {len(wrote) - len(conflicts)} in place, "
        f"{len(conflicts)} as .remote, {same} already equal; {n_prog} progress lines; est ${cost}; spend "
        f"${total:.3f} settled (+${open_res:.3f} open reservations); log {LOGDIR / (run_id + '.log')}")
    out = {k: rec.get(k) for k in ("run_id", "exit_rc", "why_failed", "t_run", "t_total", "wall_s", "est_usd", "synced",
                                   "same", "n_unsynced", "spend_usd")}
    out["conflicts"] = len(conflicts)
    print("RRUN_RESULT " + json.dumps(out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
