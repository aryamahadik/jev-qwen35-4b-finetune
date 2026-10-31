"""Self-test fixtures: source text only. They are staged into a container by selftest.py and NEVER run on the host.
Each fixture is {relative_path: source}. Several are deliberately hostile (fork bomb, memory bomb); that is the point.
"""

# ---------------------------------------------------------------- containment (ST-2, ST-3, ST-4)
PY = "python"

# SKEPTIC 18 Oct (S2 generalised): a probe that CRASHES for an unrelated reason (SyntaxError, missing module, container never started)
# used to count as "blocked". Every "must fail" probe now catches OSError and prints an explicit BLOCKED marker; the self-test requires
# the marker, so only a real OS-level refusal passes.
def _blocked(body: str) -> str:
    """Wrap `body` (python source) so that an OSError prints BLOCKED <errno> and anything else is a crash (= check fails)."""
    ind = "".join("    " + ln + "\n" for ln in body.strip("\n").split("\n"))
    return "import errno\ntry:\n" + ind + "except OSError as e:\n    print('BLOCKED', e.errno)\n"


NET_TCP_PUBLIC = {"t.py": "import socket\n" + _blocked("s=socket.socket(); s.settimeout(3)\ns.connect(('1.1.1.1',443)); print('CONNECTED')")}
NET_TCP_METADATA = {"t.py": "import socket\n" + _blocked("s=socket.socket(); s.settimeout(3)\ns.connect(('169.254.169.254',80)); print('CONNECTED')")}
NET_UDP_DNS = {"t.py": "import socket\n" + _blocked(
    "s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.settimeout(3)\n"
    "s.sendto(b'\\x12\\x34\\x01\\x00\\x00\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x07example\\x03com\\x00\\x00\\x01\\x00\\x01',('8.8.8.8',53))\n"
    "print('REPLY', s.recvfrom(512)[0][:2])")}
NET_DOCKER_SOCK = {"t.py": "import socket\n" + _blocked("s=socket.socket(socket.AF_UNIX); s.connect('/var/run/docker.sock'); print('CONNECTED')")}
# S2 (Opus 10.1): socket.if_nameindex() instead of listing /sys/class/net (a crashed probe printed nothing and "passed").
NET_IFACES = {"t.py": "import socket\nprint('IFACES', ','.join(sorted(n for _, n in socket.if_nameindex())))\n"}

WRITE_OUTSIDE = {"t.py": _blocked("open('/etc/od_sbx_probe','w').write('x'); print('WROTE')")}
WRITE_PROC_SYS = {"t.py": _blocked("open('/proc/sys/kernel/hostname','w').write('x'); print('WROTE')")}
WRITE_IN_RO = {"t.py": _blocked("open('/in/probe','w').write('x'); print('WROTE')")}
WRITE_WORK_OK = {"t.py": "open('/work/probe','w').write('x'); open('/out/probe','w').write('x'); print('WORK_AND_OUT_OK')\n"}
# ctypes probes: libc returns -1 (errno set) when refused; the check requires the literal `_RC -1`, so a crash does not pass.
PRIV_MOUNT = {"t.py": ("import ctypes\nl=ctypes.CDLL(None, use_errno=True)\n"
                       "r=l.mount(b'none',b'/work',b'tmpfs',0,None); print('MOUNT_RC',r, ctypes.get_errno())\n")}
# ST-3.5 was VACUOUS: the old probe attached to PID 1, which is the probe itself (the command is exec'd as the container's init), and
# ptrace(ATTACH) on yourself is always EPERM. The probe now attaches to a forked CHILD of the same uid. gVisor implements ptrace
# inside the sandbox, so SUCCESS here is plausible and harmless (the sandbox boundary is what matters): ST-3.5i records the result only.
PRIV_PTRACE = {"t.py": ("import ctypes, os, time\nl=ctypes.CDLL(None, use_errno=True)\n"
                        "pid=os.fork()\n"
                        "if pid==0:\n    time.sleep(5); os._exit(0)\n"
                        "r=l.ptrace(16,pid,0,0); print('PTRACE_CHILD_RC',r, ctypes.get_errno())\n"
                        "os.kill(pid,9)\n")}
PRIV_UNSHARE = {"t.py": "import os\n" + _blocked("os.unshare(os.CLONE_NEWNS)\nprint('UNSHARED')")}
ID_AND_CAPS = {"t.py": ("import os\nprint('UID',os.getuid(),os.getgid())\n"
                        "print([l for l in open('/proc/self/status') if l.startswith(('CapEff','CapBnd','NoNewPrivs'))])\n")}
KERNEL_VERSION = {"t.py": "print(open('/proc/version').read().strip())\n"}

FORK_BOMB = {"t.py": ("import os\nn=0\nwhile True:\n    try:\n        if os.fork()==0:\n            while True: pass\n        n+=1\n"
                      "    except OSError:\n        print('PIDS_LIMIT_HIT',n); break\n")}
MEM_BOMB = {"t.py": "b=[]\nwhile True: b.append(bytearray(64*1024*1024))\n"}
DISK_FILL = {"t.py": ("import errno\nn=0\ntry:\n    while True:\n        with open(f'/work/fill{n}','wb') as f:\n"
                      "            f.write(b'x'*(32*1048576))\n        n+=1\n"
                      "except OSError as e:\n    print('DISK_STOPPED', e.errno == errno.ENOSPC, n)\n")}
FILE_SIZE_BOMB = {"t.py": ("try:\n    with open('/work/big','wb') as f:\n        f.write(b'x'*(80*1048576))\n    print('WROTE_80MB')\n"
                           "except OSError as e:\n    print('FSIZE_STOPPED', e.errno)\n")}
# ST-4.7 (M4, Opus 10.1): /out is a bind mount of the size-capped STAGE_ROOT tmpfs (512 MiB). 63 MiB files (just under the 64 MiB fsize
# ulimit) until the write is refused; 24 x 63 MiB = 1.5 GiB > cap, so reaching the end without ENOSPC means the cap does not exist.
OUT_FILL = {"t.py": ("import errno\nn=0\nchunk=b'x'*(63*1048576)\n"
                     "try:\n    while n < 24:\n        with open(f'/out/fill{n}','wb') as f:\n            f.write(chunk)\n        n+=1\n"
                     "    print('OUT_NOT_CAPPED', n)\n"
                     "except OSError as e:\n    print('OUT_STOPPED', e.errno == errno.ENOSPC, n)\n")}
INFINITE_LOOP = {"t.py": "while True: pass\n"}
BIG_STDOUT = {"t.py": "import sys\nb=b'a'*1048576\nfor _ in range(1024): sys.stdout.buffer.write(b)\nsys.stdout.flush(); print('DONE', file=sys.stderr)\n"}

# ---------------------------------------------------------------- determinism (ST-6)
# S1 + F-GO1: each prints its temp dir ALONE on the LAST stdout line, which must be exactly /work/.tmp (config.WORK_TMP; selftest.st6 compares the
# whole line, not a substring), and creates a file in it (python/node mkdtemp, sh touch; go writes via t.TempDir() in ST-6.6). The go fixture keeps
# go.mod AT the /work root on purpose: that is exactly the layout cmd/go refuses when TMPDIR is /work itself (it ignores a go.mod in the system
# temp root), so ST-6.3 / ST-6.6 are the regression guard.
DETERMINISTIC = {
    "python": {"t.py": ("import tempfile\nd = tempfile.mkdtemp()\n"
                        "print(sum(i*i for i in range(1000)), hash('abc'))\nprint(tempfile.gettempdir())\n")},   # hash() stable: PYTHONHASHSEED=0
    "node":   {"t.js": ("const os=require('os'),fs=require('fs'),path=require('path');\n"
                        "fs.mkdtempSync(path.join(os.tmpdir(),'x-'));\n"
                        "console.log([1,2,3].map(x=>x*x).join(','), (0.1+0.2).toFixed(3));\nconsole.log(os.tmpdir());\n")},
    "go":     {"go.mod": "module det\n\ngo 1.26\n", "vendor/modules.txt": "",
               "m.go": 'package main\nimport (\n\t"fmt"\n\t"os"\n)\nfunc main(){ fmt.Println(1+2, "ok"); fmt.Println(os.TempDir()) }\n'},
    "sh":     {"t.sh": "#!/bin/sh\nprintf '%s\\n' a b c | sort | tr a-z A-Z\ntouch \"$TMPDIR/x\"\nprintf '%s\\n' \"$TMPDIR\"\n"},
}
# ST-6.6 (M3): a vendored `go test` must finish inside the 60 s suite limit on the pre-warmed cache, and t.TempDir() must work (S1)
GO_TEST = {"go.mod": "module det\n\ngo 1.26\n", "vendor/modules.txt": "",
           "m.go": "package det\n\nfunc Add(a, b int) int { return a + b }\n",
           "m_test.go": ('package det\n\nimport (\n\t"os"\n\t"path/filepath"\n\t"testing"\n)\n\n'
                         'func TestAdd(t *testing.T) {\n\tif Add(1, 2) != 3 {\n\t\tt.Fatal("add")\n\t}\n'
                         '\tif err := os.WriteFile(filepath.Join(t.TempDir(), "x"), []byte("x"), 0o600); err != nil {\n\t\tt.Fatal(err)\n\t}\n}\n')}
NONDETERMINISTIC = {"t.py": "import os\nprint(os.urandom(8).hex())\n"}

# ---------------------------------------------------------------- tamper (ST-5): python / pytest only in v1
HIDDEN_SUITE = {"test_hidden.py": ("from solution import add, sub\n"
                                   "def test_add():\n    r = add(1, 2)\n    assert type(r) is int and r == 3\n"
                                   "def test_sub():\n    r = sub(3, 1)\n    assert type(r) is int and r == 2\n")}
VISIBLE_SUITE = {"test_visible.py": "from solution import add\ndef test_add():\n    assert add(1, 2) == 3\n"}
EXPECTED_HIDDEN_IDS = {"test_hidden::test_add", "test_hidden::test_sub"}
EXPECTED_VISIBLE_IDS = {"test_visible::test_add"}

SOL_CORRECT = {"solution.py": "def add(a, b):\n    return a + b\ndef sub(a, b):\n    return a - b\n"}
SOL_EXIT0_AT_IMPORT = {"solution.py": "import os\nos._exit(0)\n"}
SOL_EQ_OVERLOAD = {"solution.py": ("class Always(int):\n    def __eq__(self, o): return True\n    def __hash__(self): return 0\n"
                                   "def add(a, b): return Always(0)\n"
                                   "def sub(a, b): return Always(0)\n")}
SOL_FORGE_PARTIAL = {"solution.py": (
    "import os\n"
    "x = ('<testsuites><testsuite name=\"od\" tests=\"1\"><testcase classname=\"test_hidden\" name=\"test_add\"/>'\n"
    "     '</testsuite></testsuites>')\n"
    "open('/out/junit.xml','w').write(x)\nos._exit(0)\n")}
SOL_FORGE_EXACT = {"solution.py": (            # KNOWN GAP probe (ST-5.5, informational): author knows the hidden ids
    "import os\n"
    "x = ('<testsuites><testsuite name=\"od\" tests=\"2\"><testcase classname=\"test_hidden\" name=\"test_add\"/>'\n"
    "     '<testcase classname=\"test_hidden\" name=\"test_sub\"/></testsuite></testsuites>')\n"
    "open('/out/junit.xml','w').write(x)\nos._exit(0)\n")}
CONFTEST_FORCE_PASS = {"conftest.py": (
    "import pytest\n"
    "@pytest.hookimpl(hookwrapper=True)\n"
    "def pytest_runtest_makereport(item, call):\n"
    "    out = yield\n    rep = out.get_result()\n    rep.outcome = 'passed'\n"
    "def pytest_sessionfinish(session, exitstatus):\n    session.exitstatus = 0\n")}
# ST-5.6 (S3): shadow modules. `pytest.py` replaces pytest when the cwd is on sys.path (`python -m pytest`), and the user-site copy
# under HOME=/work (.local/...) is searched before site-packages. Both forge the EXACT hidden ids and exit 0, so if either survives the
# run the verdict is PASS for a WRONG solution; the executor must strip them (and run `python -s -P`) so the real pytest reports FAIL.
_FORGED = ("import os, sys\n"
           "open('/out/junit.xml','w').write('<testsuites><testsuite name=\"od\" tests=\"2\"><testcase classname=\"test_hidden\" name=\"test_add\"/>'\n"
           "    '<testcase classname=\"test_hidden\" name=\"test_sub\"/></testsuite></testsuites>')\n"
           "os._exit(0)\n")
SHADOW_PYTEST = {"pytest.py": _FORGED,
                 ".local/lib/python3.12/site-packages/pluggy/__init__.py": _FORGED,
                 "_pytest/__init__.py": _FORGED}
SOL_WRONG = {"solution.py": "def add(a, b):\n    return 0\ndef sub(a, b):\n    return 0\n"}
