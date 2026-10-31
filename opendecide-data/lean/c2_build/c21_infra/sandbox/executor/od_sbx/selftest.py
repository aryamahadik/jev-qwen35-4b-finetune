"""Executor self-test: ST-1 .. ST-7, run at EVERY VM start (od-sbx-selftest.service) and logged.

ANY failure leaves status FAIL in selftest.json and `run-batch` refuses to start. The IDs here are exactly the list in
IMAGE_RECIPE.md section 7; the Sonnet skeptic reviews exactly this list and Opus signs off before first use.
Checks whose id ends in `i` are INFORMATIONAL (recorded, never fail the batch): ST-3.5i (in-sandbox ptrace) and ST-5.5i (known gap).

FAIL-CLOSED RULE (skeptic 18 Oct): a "must be blocked" check passes only on an explicit, specific signal (a BLOCKED marker printed by
the probe's own `except OSError`, a specific curl/getent exit code, a named errno). A probe that crashed, never started, or
printed nothing is a FAILURE, never a pass.
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import time
from dataclasses import dataclass
from typing import Callable

from . import fixtures as F
from . import verdict as V
from .config import LIMITS, MANIFEST, ROOT, STAGE_ROOT, WORK_TMP
from .treehash import tree_hash
from .runner import BatchCounters, load_manifest, run_once, run_repeated

PY, NODE, GO, SH = "python", "node", "go", "sh"
PYRUN = ["python", "t.py"]
NET_FAIL_RC = {6, 7, 28}        # curl: could not resolve / could not connect (EPERM from an OUTPUT drop) / timed out. 127 (missing) is NOT here.


@dataclass
class Ctx:
    manifest: dict
    counters: BatchCounters
    batch: str = "selftest"


@dataclass
class Check:
    id: str
    desc: str
    fn: Callable[[Ctx], tuple[bool, str]]


def sh(args, timeout=30, user=None):
    a = list(args)
    if user is not None:
        a = ["setpriv", f"--reuid={user}", f"--regid={user}", "--clear-groups", *a]
    try:
        p = subprocess.run(a, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def ctr(ctx: Ctx, tool: str, files: dict, argv: list[str], key: str, kind: str = "run"):
    return run_once(tool, {k: v.encode() for k, v in files.items()}, argv, kind=kind,
                    name=f"od-sbx-{ctx.batch}-{key}", manifest=ctx.manifest)


# ------------------------------------------------------------------ ST-1 host network
def st1_1(c): rc, o = sh(["curl", "-sS", "-m", "5", "https://1.1.1.1"]); return rc in NET_FAIL_RC, f"rc={rc} {o.strip()[:60]!r}"
def st1_2(c): rc, o = sh(["curl", "-sS", "-m", "5", "http://169.254.169.254/"], user=65534); return rc in NET_FAIL_RC, f"rc={rc} {o.strip()[:60]!r}"
def st1_3(c):
    rc, o = sh(["curl", "-sS", "-m", "5", "-H", "Metadata-Flavor: Google",
                "http://169.254.169.254/computeMetadata/v1/instance/name"])
    return rc == 0 and o.strip().startswith("od-sbx"), f"root metadata path (guest agent) rc={rc} name={o.strip()[:40]!r}"
def st1_4(c): rc, o = sh(["getent", "hosts", "example.com"], user=65534, timeout=90); return rc == 2, f"rc={rc} (2 = lookup failed; 126/127 = tool missing)"
def st1_5(c): rc, o = sh(["nft", "list", "chain", "inet", "od_sbx", "output"]); return rc == 0 and "policy drop" in o, o[:120]
def st1_6(c):
    # An instance without a service account answers the listing with an EMPTY 200 (or a 404). `curl -sS` without -f used to compare the
    # body of a 404 page to "" and fail; now the status code is read explicitly and a non-empty listing (e.g. "default/") fails.
    rc, o = sh(["curl", "-sS", "-m", "5", "-H", "Metadata-Flavor: Google", "-w", "\n%{http_code}",
                "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/"])
    body, _, code = o.rpartition("\n")
    ok = rc == 0 and ((code == "200" and body.strip() == "") or code == "404")
    return ok, f"service-accounts listing: http={code!r} body={body.strip()[:60]!r}"
def st1_7(c):
    rc, o = sh(["getent", "group", "docker"])
    if rc == 2: return True, "no docker group"
    members = o.strip().split(":")[-1] if rc == 0 else None
    return members == "", f"docker group members={members!r}"


def host_guards() -> list[str]:
    """M5 (Opus 10.1): the cheap host checks, re-run by `run-batch` at batch start (an SSH login can change group membership after boot).
    Returns the ids that failed (empty = all good). ST-4.7's mount check is included: a missing tmpfs would let /out fill the boot disk."""
    bad = []
    for cid, fn in (("ST-1.5", st1_5), ("ST-1.6", st1_6), ("ST-1.7", st1_7), ("ST-4.7m", stage_mount_ok)):
        try:
            ok, _ = fn(None)
        except Exception:
            ok = False
        if not ok:
            bad.append(cid)
    return bad


def stage_mount_ok(c) -> tuple[bool, str]:
    rc, o = sh(["findmnt", "-no", "FSTYPE,TARGET,SIZE", "-T", str(STAGE_ROOT)])
    parts = o.split()
    return rc == 0 and len(parts) >= 2 and parts[0] == "tmpfs" and parts[1] == str(STAGE_ROOT), f"findmnt -T {STAGE_ROOT}: {o.strip()[:80]!r}"


# ------------------------------------------------------------------ ST-2 container network
def _blocked_ok(r, token):
    """Fail-closed: the probe must have printed BLOCKED (its own `except OSError`) and must NOT have printed the success token."""
    out = r.stdout.decode("utf-8", "replace")
    return ("BLOCKED" in out) and (token not in out)
def st2(fx, key, token):
    def f(c):
        r = ctr(c, PY, fx, PYRUN, key)
        return _blocked_ok(r, token), f"outcome={r.outcome} rc={r.exit_code} out={r.stdout[:60]!r} err={r.stderr[-120:]!r}"
    return f
def st2_5(c):
    r = ctr(c, PY, F.NET_IFACES, PYRUN, "ifaces")
    out = r.stdout.decode("utf-8", "replace").strip()
    return out == "IFACES lo", f"{out!r} (must be exactly 'IFACES lo'; empty or missing = crashed probe = FAIL)"


# ------------------------------------------------------------------ ST-3 isolation
def st3(fx, key, token):
    def f(c):
        r = ctr(c, PY, fx, PYRUN, key)
        return _blocked_ok(r, token), f"outcome={r.outcome} rc={r.exit_code} out={r.stdout[:80]!r} err={r.stderr[-100:]!r}"
    return f
def st3_mount(c):
    r = ctr(c, PY, F.PRIV_MOUNT, PYRUN, "mount"); o = r.stdout.decode("utf-8", "replace")
    return o.startswith("MOUNT_RC -1 "), f"out={o[:60]!r} rc={r.exit_code}"     # libc returned -1 with an errno; 0 or a crash fails
def st3_ptrace_info(c):
    r = ctr(c, PY, F.PRIV_PTRACE, PYRUN, "ptrace"); o = r.stdout.decode("utf-8", "replace")
    return True, f"INFO ptrace(ATTACH) of an own child: {o.strip()[:60]!r} (gVisor may allow this inside the sandbox; the old PID-1 probe was vacuous)"
def st3_ids(c):
    r = ctr(c, PY, F.ID_AND_CAPS, PYRUN, "ids"); o = r.stdout.decode()
    ok = "UID 65534 65534" in o and "'CapEff:\\t0000000000000000\\n'" in o and "NoNewPrivs:\\t1" in o
    return ok, o[:200]
def st3_work(c):
    r = ctr(c, PY, F.WRITE_WORK_OK, PYRUN, "workok")
    return "WORK_AND_OUT_OK" in r.stdout.decode(), f"rc={r.exit_code} err={r.stderr[-100:]!r}"


# ------------------------------------------------------------------ ST-4 resource limits
def host_responsive() -> tuple[bool, str]:
    rc, o = sh(["docker", "info", "--format", "{{.ServerVersion}}"], timeout=20)
    rc2, left = sh(["docker", "ps", "-aq", "--filter", "label=od-sbx=1"], timeout=20)
    return rc == 0 and left.strip() == "", f"docker info rc={rc}; leftover containers={left.strip()[:60]!r}"
def st4_1(c):
    r = ctr(c, PY, F.FORK_BOMB, PYRUN, "fork")
    ok, d = host_responsive()
    return ok and ("PIDS_LIMIT_HIT" in r.stdout.decode() or r.outcome == "TIMEOUT"), f"outcome={r.outcome} {d}"
def st4_2(c):
    r = ctr(c, PY, F.MEM_BOMB, PYRUN, "mem"); ok, d = host_responsive()
    return ok and r.outcome in ("OOM", "SIGNALED") , f"outcome={r.outcome} rc={r.exit_code} {d}"
def st4_3(c):
    r = ctr(c, PY, F.DISK_FILL, PYRUN, "disk")
    return "DISK_STOPPED True" in r.stdout.decode(), f"outcome={r.outcome} out={r.stdout[:60]!r}"     # must be ENOSPC, not any kill
def st4_4(c):
    r = ctr(c, PY, F.INFINITE_LOOP, PYRUN, "loop"); ok, d = host_responsive()
    return ok and r.outcome == "TIMEOUT" and r.wall_s < LIMITS.timeout_run_s + LIMITS.kill_grace_s + 5, f"wall={r.wall_s:.1f}s {d}"
def st4_5(c):
    r = ctr(c, PY, F.BIG_STDOUT, PYRUN, "stdout")
    return r.stdout_truncated and len(r.stdout) == LIMITS.stdout_cap, f"outcome={r.outcome} kept={len(r.stdout)} total={r.stdout_total}"
def st4_6(c):
    r = ctr(c, PY, F.FILE_SIZE_BOMB, PYRUN, "fsize"); o = r.stdout.decode()
    return "FSIZE_STOPPED" in o and "WROTE_80MB" not in o, f"outcome={r.outcome} rc={r.exit_code} out={o[:60]!r}"
def st4_7(c):  # M4: /out lives on a 512 MiB tmpfs; filling it must stop at ENOSPC and the host must stay healthy
    mount_ok, md = stage_mount_ok(c)
    r = ctr(c, PY, F.OUT_FILL, PYRUN, "outfill", kind="suite")        # suite limits: writing ~0.5 GiB can take longer than 10 s under gVisor
    o = r.stdout.decode("utf-8", "replace"); ok, d = host_responsive()
    return mount_ok and ok and "OUT_STOPPED True" in o, f"{md}; out={o.strip()[:60]!r} outcome={r.outcome}; {d}"


# ------------------------------------------------------------------ ST-5 verdict integrity (python / pytest in v1)
# S3 (Opus 10.1): `-P` keeps the cwd off sys.path (a patch file /work/pytest.py cannot replace pytest) and `-s` drops the user site
# (HOME=/work, so /work/.local would be searched first). The same prefix is REQUIRED of python suite jobs by cli._suite_argv_ok.
PYTEST_PREFIX = ["python", "-s", "-P", "-m", "pytest", "-c", "/etc/od-sbx/pytest.ini", "--rootdir=/work", "--junitxml=/out/junit.xml"]
PYTEST_VISIBLE = [*PYTEST_PREFIX, "test_visible.py"]
PYTEST_HIDDEN = [*PYTEST_PREFIX, "test_hidden.py"]

def _suite_verdict(c, patch: dict, suite: dict, expected: set, key: str) -> tuple[V.Verdict, object]:
    # the patch is sanitized first and the PRISTINE suite is overlaid afterwards (T56-3); see runner.run_once
    r = run_once(PY, {k: v.encode() for k, v in patch.items()},
                 PYTEST_HIDDEN if "test_hidden.py" in suite else PYTEST_VISIBLE, kind="suite",
                 name=f"od-sbx-{c.batch}-{key}", manifest=c.manifest, read_back=["junit.xml"],
                 overlay={k: v.encode() for k, v in suite.items()})
    rep = None
    if "junit.xml" in r.out_files:
        try: rep = V.parse_junit(r.out_files["junit.xml"])
        except Exception: rep = None
    return V.compute(r.exit_code, r.outcome, rep, expected), r

def st5_0(c):  # control: a correct solution must PASS, or the other ST-5 results mean nothing
    v, _ = _suite_verdict(c, F.SOL_CORRECT, F.HIDDEN_SUITE, F.EXPECTED_HIDDEN_IDS, "t5ctl")
    return v.verdict == V.PASS, f"{v.verdict}: {v.detail}"
def st5_1(c):  # patch exits 0 early
    v, _ = _suite_verdict(c, F.SOL_EXIT0_AT_IMPORT, F.HIDDEN_SUITE, F.EXPECTED_HIDDEN_IDS, "t5exit")
    return v.verdict != V.PASS, f"{v.verdict}: {v.detail}"
def st5_2(c):  # conftest forcing outcomes: the executor strips it, so the wrong solution FAILS
    v, _ = _suite_verdict(c, {**F.SOL_WRONG, **F.CONFTEST_FORCE_PASS}, F.HIDDEN_SUITE, F.EXPECTED_HIDDEN_IDS, "t5conf")
    return v.verdict == V.FAIL, f"{v.verdict}: {v.detail}"
def st5_3(c):  # __eq__ overload: visible suite is fooled, pristine hidden suite in a fresh container is not
    vv, _ = _suite_verdict(c, F.SOL_EQ_OVERLOAD, F.VISIBLE_SUITE, F.EXPECTED_VISIBLE_IDS, "t5eqv")
    vh, _ = _suite_verdict(c, F.SOL_EQ_OVERLOAD, F.HIDDEN_SUITE, F.EXPECTED_HIDDEN_IDS, "t5eqh")
    return vv.verdict == V.PASS and vh.verdict == V.FAIL, f"visible={vv.verdict} hidden={vh.verdict}"
def st5_4(c):  # forged report with only the visible ids
    v, _ = _suite_verdict(c, F.SOL_FORGE_PARTIAL, F.HIDDEN_SUITE, F.EXPECTED_HIDDEN_IDS, "t5forge")
    return v.verdict in (V.TAMPERED, V.NO_REPORT), f"{v.verdict}: {v.detail}"
def st5_6(c):  # S3: shadow modules (pytest.py, _pytest/, user-site pluggy) are stripped; the real pytest runs and the WRONG solution FAILS
    v, r = _suite_verdict(c, {**F.SOL_WRONG, **F.SHADOW_PYTEST}, F.HIDDEN_SUITE, F.EXPECTED_HIDDEN_IDS, "t5shadow")
    return v.verdict == V.FAIL and len(r.stripped) >= 3, f"{v.verdict}: {v.detail}; stripped={r.stripped[:5]}"
def st5_5i(c):  # INFORMATIONAL known gap: forged report that names exactly the hidden ids
    v, _ = _suite_verdict(c, F.SOL_FORGE_EXACT, F.HIDDEN_SUITE, F.EXPECTED_HIDDEN_IDS, "t5exact")
    return True, (f"INFO verdict={v.verdict} (PASS means the in-process forgery gap is open; Opus ruling 18 Oct: a per-run id nonce does "
                  "NOT close it and is dropped; T56 labels come from PASS on the pristine hidden suite + a clean static lint, see recipe 10.1)")


# ------------------------------------------------------------------ ST-6 determinism
def last_line(stdout: bytes) -> str:
    """The last stdout line, compared EXACTLY (a substring match would accept `/work/.tmpx` or a prefix)."""
    lines = stdout.decode("utf-8", "replace").splitlines()
    return lines[-1] if lines else ""


def st6(tool, argv):
    def f(c):
        fx = {k: v.encode() for k, v in F.DETERMINISTIC[tool].items()}
        rr = run_repeated(tool, fx, argv, batch=c.batch, row=f"det{tool}", manifest=c.manifest)
        r0 = rr.results[0]
        tmp_ok = last_line(r0.stdout) == WORK_TMP         # F-GO1: every toolchain must see TMPDIR=/work/.tmp (its fixture prints it as the LAST line)
        return rr.deterministic and r0.exit_code == 0 and tmp_ok, \
            f"exit={r0.exit_code} tmpdir={'ok' if tmp_ok else 'NOT ' + WORK_TMP} out={r0.stdout[-80:]!r} err={r0.stderr[-200:]!r}"
    return f
def st6_6(c):  # M3 control: a cold vendored `go test` finishes inside the 60 s suite limit on the pre-warmed cache; t.TempDir() works (S1)
    r = run_once(GO, {k: v.encode() for k, v in F.GO_TEST.items()}, ["go", "test", "-count=1", "./..."], kind="suite",
                 name=f"od-sbx-{c.batch}-gotest", manifest=c.manifest)
    return r.outcome == "OK" and r.wall_s < LIMITS.timeout_suite_s, f"outcome={r.outcome} wall={r.wall_s:.1f}s err={r.stderr[-100:]!r}"
def st6_5(c):
    fx = {k: v.encode() for k, v in F.NONDETERMINISTIC.items()}
    rr = run_repeated(PY, fx, PYRUN, batch=c.batch, row="nondet", manifest=c.manifest)
    if not rr.deterministic:
        c.counters.bump("dropped_nondeterministic")
    return (not rr.deterministic), rr.reason or "NOT DETECTED"


# ------------------------------------------------------------------ ST-7 pins
def st7_1(c):
    bad = []
    for k, v in c.manifest["toolchains"].items():
        rc, o = sh(["docker", "image", "inspect", "--format", "{{.Id}}", v["image_id"]])
        if rc != 0 or o.strip() != v["image_id"]: bad.append(k)
    return not bad, f"mismatched images: {bad}"
def st7_2(c):
    rc, o = sh(["runsc", "--version"]); line = o.splitlines()[0] if o else ""
    return rc == 0 and line == c.manifest["runsc_version_line"], f"{line!r} vs manifest {c.manifest['runsc_version_line']!r}"
def st7_3(c):
    m = c.manifest; res = []
    for tool, argv, want in [(PY, ["python", "-V"], "Python " + m["toolchains"]["python"]["version"]),
                             (PY, ["python", "-m", "pytest", "--version"], "pytest " + m["pytest"]),
                             (NODE, ["node", "-v"], "v" + m["toolchains"]["node"]["version"]),
                             (GO, ["go", "version"], "go" + m["toolchains"]["go"]["version"]),
                             (SH, ["bash", "--version"], "version 5.2")]:
        r = run_once(tool, {}, argv, name=f"od-sbx-{c.batch}-ver-{tool}-{len(res)}", manifest=m)
        txt = (r.stdout + r.stderr).decode("utf-8", "replace")
        res.append((want in txt, want))
    return all(ok for ok, _ in res), "; ".join(f"{w}:{'ok' if ok else 'BAD'}" for ok, w in res)
def st7_4(c):
    got = tree_hash(ROOT / "executor")
    return got == c.manifest["executor_py_tree_sha256"], f"computed={got[:16]} manifest={c.manifest['executor_py_tree_sha256'][:16]}"
def st7_5(c):
    r = ctr(c, PY, F.KERNEL_VERSION, PYRUN, "kver"); inside = r.stdout.decode().strip()
    host = platform.release()
    return host not in inside and "Linux version" in inside, f"container /proc/version={inside[:60]!r} host={host}"


def st7_6(c):  # F-3 / M6: the docker storage driver equals the manifest (classic overlay2 store, not the containerd image store)
    rc, o = sh(["docker", "info", "--format", "{{.Driver}}"])
    return rc == 0 and o.strip() == c.manifest.get("docker_storage_driver", "?"), f"driver={o.strip()!r} manifest={c.manifest.get('docker_storage_driver')!r}"


CHECKS: list[Check] = [
    Check("ST-1.1", "host: TCP to a public IP fails", st1_1),
    Check("ST-1.2", "host: metadata server unreachable for a non-root uid", st1_2),
    Check("ST-1.3", "host: metadata reachable for root only (guest agent path stays alive)", st1_3),
    Check("ST-1.4", "host: DNS lookup as non-root fails", st1_4),
    Check("ST-1.5", "host: nftables output chain is policy drop", st1_5),
    Check("ST-1.6", "host: no service account on the instance", st1_6),
    Check("ST-1.7", "host: docker group is empty", st1_7),
    Check("ST-2.1", "container: TCP to 1.1.1.1:443 fails", st2(F.NET_TCP_PUBLIC, "tcp", "CONNECTED")),
    Check("ST-2.2", "container: TCP to 169.254.169.254:80 fails", st2(F.NET_TCP_METADATA, "tcpmd", "CONNECTED")),
    Check("ST-2.3", "container: UDP DNS to 8.8.8.8:53 fails", st2(F.NET_UDP_DNS, "udp", "REPLY")),
    Check("ST-2.4", "container: unix socket to docker.sock fails", st2(F.NET_DOCKER_SOCK, "dsock", "CONNECTED")),
    Check("ST-2.5", "container: only loopback exists", st2_5),
    Check("ST-3.1", "container: write outside /work fails", st3(F.WRITE_OUTSIDE, "wout", "WROTE")),
    Check("ST-3.2", "container: write to /proc/sys fails", st3(F.WRITE_PROC_SYS, "wproc", "WROTE")),
    Check("ST-3.3", "container: /in is read-only", st3(F.WRITE_IN_RO, "win", "WROTE")),
    Check("ST-3.4", "container: mount fails", st3_mount),
    Check("ST-3.5i", "INFO container: ptrace of an own child (the old PID-1 probe was vacuous)", st3_ptrace_info),
    Check("ST-3.6", "container: unshare fails", st3(F.PRIV_UNSHARE, "unshare", "UNSHARED")),
    Check("ST-3.7", "container: uid 65534, no capabilities, no_new_privs", st3_ids),
    Check("ST-3.8", "container: /work and /out are writable (control)", st3_work),
    Check("ST-4.1", "fork bomb dies at the pids limit; host stays responsive; no leftovers", st4_1),
    Check("ST-4.2", "memory bomb is OOM-killed; host stays responsive", st4_2),
    Check("ST-4.3", "disk fill stops at the tmpfs size", st4_3),
    Check("ST-4.4", "infinite loop is killed from outside at the timeout", st4_4),
    Check("ST-4.5", "1 GB stdout is truncated to the 64 KB cap", st4_5),
    Check("ST-4.6", "single file over the fsize limit cannot be written", st4_6),
    Check("ST-4.7", "/out fill stops at the 512 MiB tmpfs cap; stage mount is a tmpfs; host responsive", st4_7),
    Check("ST-5.0", "control: correct patch + pristine hidden suite = PASS", st5_0),
    Check("ST-5.1", "tamper: patch exits 0 at import -> not PASS", st5_1),
    Check("ST-5.2", "tamper: conftest forcing pass is stripped -> FAIL", st5_2),
    Check("ST-5.3", "tamper: __eq__ overload fools visible tests, fails the pristine hidden suite", st5_3),
    Check("ST-5.4", "tamper: forged report with wrong id set -> TAMPERED/NO_REPORT", st5_4),
    Check("ST-5.5i", "INFO known gap: forged report with the exact hidden ids", st5_5i),
    Check("ST-5.6", "tamper: shadow modules pytest.py / _pytest / user-site pluggy are stripped -> FAIL", st5_6),
    Check("ST-6.1", "determinism python x2 identical", st6(PY, PYRUN)),
    Check("ST-6.2", "determinism node x2 identical", st6(NODE, ["node", "t.js"])),
    Check("ST-6.3", "determinism go x2 identical", st6(GO, ["go", "run", "."])),
    Check("ST-6.4", "determinism sh x2 identical", st6(SH, ["sh", "t.sh"])),
    Check("ST-6.5", "nondeterministic fixture is detected, row dropped, counter incremented", st6_5),
    Check("ST-6.6", "go test (vendored, t.TempDir) finishes inside the 60 s suite limit on the pre-warmed cache", st6_6),
    Check("ST-7.1", "four toolchain image ids equal the manifest", st7_1),
    Check("ST-7.2", "runsc version line equals the manifest", st7_2),
    Check("ST-7.3", "python/pytest/node/go/bash versions equal the manifest pins", st7_3),
    Check("ST-7.4", "executor .py tree hash equals the manifest", st7_4),
    Check("ST-7.5", "workload runs under gVisor (container /proc/version is not the host kernel)", st7_5),
    Check("ST-7.6", "docker storage driver equals the manifest", st7_6),
]


def run_selftest(out_path: str) -> int:
    t0 = time.time()
    ctx = Ctx(load_manifest(), BatchCounters())
    rows, failed = [], 0
    for ck in CHECKS:
        try:
            ok, detail = ck.fn(ctx)
        except Exception as e:                       # a crashing check is a failure, never a skip
            ok, detail = False, f"EXC {type(e).__name__}: {e}"
        info = ck.id.endswith("i")
        failed += (not ok) and (not info)
        rows.append({"id": ck.id, "desc": ck.desc, "ok": ok, "info": info, "detail": detail[:300]})
    doc = {"status": "FAIL" if failed else "PASS", "failed": failed, "n": len(rows), "elapsed_s": round(time.time() - t0, 1),
           "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(), "kernel": platform.release(),
           "counters": ctx.counters.c, "checks": rows}
    with open(out_path, "w") as f:
        json.dump(doc, f, indent=1)
    print(json.dumps({k: doc[k] for k in ("status", "failed", "n", "elapsed_s")}))
    return 1 if failed else 0
