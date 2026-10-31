"""Static + pure-function tests for the od-sbx sandbox tree (skeptic pass, 18 Oct 2026).

Nothing here starts docker, executes a fixture or touches the network. The fixtures are only parsed (ast), never run.
Run from c21_infra:  python3 -m pytest -c pytest.ini -p no:cacheprovider sandbox/executor/tests
"""
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXEC = os.path.dirname(HERE)                       # sandbox/executor
SBX = os.path.dirname(EXEC)                        # sandbox
sys.path.insert(0, EXEC)

from od_sbx import fixtures as F, selftest as T, verdict as V          # noqa: E402
from od_sbx.cli import _suite_argv_ok                                   # noqa: E402
from od_sbx.dockercmd import RunPlan, build_run_argv                    # noqa: E402
from od_sbx.runner import safe_name, sanitize, sanitize_report          # noqa: E402


def read(*p):
    return open(os.path.join(SBX, *p), encoding="utf-8").read()


# ------------------------------------------------------------------ M1 launcher
def test_launcher_works_under_isolated_mode_and_the_old_wrapper_does_not():
    with tempfile.TemporaryDirectory() as td:
        ex = os.path.join(td, "executor")
        shutil.copytree(EXEC, ex, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        ok = subprocess.run([sys.executable, "-I", os.path.join(ex, "od_sbx_launcher.py"), "treehash", ex],
                            capture_output=True, text=True, cwd=td)
        assert ok.returncode == 0 and re.fullmatch(r"[0-9a-f]{64}", ok.stdout.strip()), ok.stderr
        # the pre-fix invocation: -I ignores PYTHONPATH, so the module is not found (this is the M1 blocker)
        old = subprocess.run([sys.executable, "-I", "-m", "od_sbx", "treehash", ex], capture_output=True, text=True,
                             cwd=td, env={**os.environ, "PYTHONPATH": ex})
        assert old.returncode != 0 and "No module named od_sbx" in old.stderr


def test_no_script_or_unit_uses_pythonpath_with_dash_I():
    for rel in ["build/50_install_executor.sh", "build/60_finalize_image.sh", "host/od-sbx-selftest.service"]:
        txt = read(rel)
        assert "PYTHONPATH" not in re.sub(r"#.*", "", txt), rel
        assert "-I -m od_sbx" not in txt and "-I -m od_sbx" not in txt.replace("python3 -I", "python3 -I"), rel
        assert "od_sbx_launcher.py" in txt, rel


# ------------------------------------------------------------------ M2 manifest values
def test_step60_assigns_before_jq_and_asserts_nonempty():
    s = read("build/60_finalize_image.sh")
    jq_part = s[s.index("jq -n"):s.index("chmod 0644")]
    assert "$(" not in jq_part.split("'{")[0], "a command substitution inside jq --arg would hide failures (M2)"
    for name in ["exech", "runsc_line", "pyid", "ndid", "goid", "shid", "dockerv", "stor"]:
        assert re.search(rf"\bneed \S+ \"\${{{name}}}\"", s), name


# ------------------------------------------------------------------ M3 go cache
def test_go_cache_is_prewarmed_and_seeded_and_gotmpdir_is_gone():
    d = read("images/Dockerfile.go")
    assert "/opt/gocache-seed" in d and "go test" in d and "GOTMPDIR" not in re.sub(r"#.*", "", d)
    a = build_run_argv(RunPlan("n", "sha256:x", "/i", "/o", ["go", "run", "."], seed=("/opt/gocache-seed", "/work/.gocache"), tmpfs_work="512m"))
    assert "size=512m" in " ".join(a) and "cp -R /opt/gocache-seed/. /work/.gocache/" in a[a.index("-c") + 1]
    from od_sbx.config import SEEDS
    assert set(SEEDS) == {"go"}
    assert os.path.exists(os.path.join(SBX, "images/gowarm/go.mod")) and os.path.exists(os.path.join(SBX, "images/gowarm/warm_test.go"))


# ------------------------------------------------------------------ M4 /out cap
def test_stage_root_is_a_capped_tmpfs_and_st47_exists():
    s = read("build/50_install_executor.sh")
    assert "/srv/od-sbx/stage tmpfs" in s and "size=512M" in s and "nofail" in s
    assert "ST-4.7" in [c.id for c in T.CHECKS]
    assert "OUT_STOPPED" in F.OUT_FILL["t.py"]


# ------------------------------------------------------------------ M5 docker group
def test_guest_agent_groups_override_and_runtime_regate():
    s10, s60 = read("build/10_install_base.sh"), read("build/60_finalize_image.sh")
    assert "groups = adm,dip,lxd,plugdev,video" in s10 and "docker" not in "adm,dip,lxd,plugdev,video".split(",")
    assert "docker_group_members" in s60
    assert callable(T.host_guards)
    assert "host_guards" in open(os.path.join(EXEC, "od_sbx", "cli.py")).read()


# ------------------------------------------------------------------ M6 / F-2 / F-3 / F-6
def test_runsc_guard_precedes_dpkg_and_nft_check_precedes_install():
    s20 = read("build/20_install_runsc.sh")
    assert s20.index("/etc/docker/daemon.json ] || die") < s20.index("dpkg -i")
    s50 = read("build/50_install_executor.sh")
    assert s50.index("nft -c -f") < s50.index("install -m 0644 \"${SBX_SRC}/host/hostfw.nft\"")
    dj = json.loads(read("host/docker-daemon.json"))
    assert dj["storage-driver"] == "overlay2" and dj["features"] == {"containerd-snapshotter": False}
    assert "docker_storage_driver" in read("build/60_finalize_image.sh")


# ------------------------------------------------------------------ S1 TMPDIR (+ F-GO1: /work/.tmp, never /work itself)
def test_tmpdir_is_a_subdirectory_of_work_everywhere():
    from od_sbx.config import BASE_ENV, WORK_TMP
    import posixpath
    assert WORK_TMP == "/work/.tmp" and BASE_ENV["TMPDIR"] == WORK_TMP
    # F-GO1: cmd/go ignores a go.mod whose directory IS os.TempDir(); every run has its sources at the /work root, so TMPDIR must differ
    assert posixpath.normpath(BASE_ENV["TMPDIR"]) != "/work" and posixpath.dirname(BASE_ENV["TMPDIR"]) == "/work"
    a = build_run_argv(RunPlan("n", "sha256:x", "/i", "/o", ["python", "t.py"]))
    assert "TMPDIR=/work/.tmp" in a and "TMPDIR=/work" not in a
    # S1 properties kept: the temp dir lives on the existing /work tmpfs, no new mount, root stays read-only, no network
    assert a.count("--mount") == 2 and a.count("--tmpfs") == 1 and "--read-only" in a and a[a.index("--network") + 1] == "none"
    for f in ["Dockerfile.python", "Dockerfile.node", "Dockerfile.go", "Dockerfile.sh"]:
        assert "stale" in read("images", f).lower(), f      # the baked TMPDIR=/work is documented as overridden by the executor


def test_prelude_creates_the_temp_dir_before_the_command_for_every_toolchain():
    for seed in (None, ("/opt/gocache-seed", "/work/.gocache")):
        a = build_run_argv(RunPlan("n", "sha256:x", "/i", "/o", ["go", "version"], seed=seed))
        script = a[a.index("-c") + 1]
        assert script.startswith("cp -R /in/. /work/ && mkdir /work/.tmp") and script.endswith('exec "$@"')
        assert a[-2:] == ["go", "version"] and a[a.index("-c") + 2] == "sh"


def _guarded_run_once(monkeypatch, tool, files, kind, overlay=None):
    """Call the REAL runner.run_once with stage() replaced by a recorder. Returns ("staged", tree) if the row got past the executor-owned-name
    check, or the StageError. Nothing reaches docker (stage raises a sentinel right after recording the tree)."""
    import od_sbx.runner as R

    class Reached(Exception):
        pass
    seen = {}

    def fake_stage(tree):
        seen["tree"] = dict(tree)
        raise Reached()
    monkeypatch.setattr(R, "stage", fake_stage)
    try:
        R.run_once(tool, files, [tool, "x"], kind=kind, name="n", manifest={"toolchains": {tool: {"image_id": "sha256:x"}}}, overlay=overlay)
    except R.StageError as e:
        return e
    except Reached:
        return ("staged", seen["tree"])
    raise AssertionError("run_once returned without staging or rejecting")


RESERVED_KEYS = [".tmp", ".tmp/x", "./.tmp/x", "d/../.tmp/e", ".tmp/a/b"]


def test_reserved_tmp_key_makes_the_row_unstageable_for_both_kinds_every_toolchain_patch_and_overlay(monkeypatch):
    import od_sbx.runner as R
    for tool in ("python", "node", "go", "sh"):
        for kind in ("run", "suite"):
            for key in RESERVED_KEYS:
                e = _guarded_run_once(monkeypatch, tool, {"m.py": b"1", key: b"x"}, kind)
                assert isinstance(e, R.StageError) and "'.tmp'" in str(e), (tool, kind, key, e)
                e = _guarded_run_once(monkeypatch, tool, {"m.py": b"1"}, kind, overlay={"t_test.py": b"2", key: b"x"})
                assert isinstance(e, R.StageError) and "overlay" in str(e), (tool, kind, key, e)


def test_names_that_merely_look_like_the_reserved_one_are_not_rejected(monkeypatch):
    ok = {"m.go": b"1", "a/.tmp/keep": b"2", ".tmpx": b"3", "tmp/y": b"4", ".tmp.py": b"5"}
    for kind in ("run", "suite"):
        r = _guarded_run_once(monkeypatch, "python", dict(ok), kind)
        assert isinstance(r, tuple) and r[0] == "staged", (kind, r)
        assert {"a/.tmp/keep", ".tmpx", "tmp/y", ".tmp.py"} <= set(r[1]), (kind, sorted(r[1]))     # nothing is stripped or altered


def test_go_executor_dirs_are_rejected_for_run_rows_and_overlays_but_stripped_for_suite_patches(monkeypatch):
    import od_sbx.runner as R
    for key in (".gocache/ab/x", ".gopath/pkg/m", "./.gocache"):
        assert isinstance(_guarded_run_once(monkeypatch, "go", {"main.go": b"1", key: b"x"}, "run"), R.StageError), key
        for kind in ("run", "suite"):
            assert isinstance(_guarded_run_once(monkeypatch, "go", {"main.go": b"1"}, kind, overlay={key: b"x"}), R.StageError), (kind, key)
        r = _guarded_run_once(monkeypatch, "go", {"main.go": b"1", key: b"x"}, "suite")           # K6: stripped and recorded (10.4 (a)), not rejected
        assert isinstance(r, tuple) and sorted(r[1]) == ["main.go"], r
    for tool in ("python", "node", "sh"):                                                          # the names mean nothing outside Go
        r = _guarded_run_once(monkeypatch, tool, {"x.py": b"1", ".gocache/a": b"x"}, "run")
        assert isinstance(r, tuple) and ".gocache/a" in r[1], (tool, r)
    r = _guarded_run_once(monkeypatch, "go", {"main.go": b"1", "sub/.gocache/z": b"x"}, "run")      # only the TOP-level names are executor-owned
    assert isinstance(r, tuple) and "sub/.gocache/z" in r[1]


def test_the_reserved_name_check_is_load_bearing(monkeypatch):
    """Mutation guard: with the check removed the very rows the tests above reject reach stage() and would run on a tree that contains `.tmp`.
    If someone reintroduces a silent drop or deletes `_reject_reserved`, the tests above fail and this one documents why."""
    import od_sbx.runner as R
    monkeypatch.setattr(R, "_reject_reserved", lambda *a, **k: None)
    r = _guarded_run_once(monkeypatch, "python", {"m.py": b"1", ".tmp/x": b"x"}, "run")
    assert isinstance(r, tuple) and ".tmp/x" in r[1]
    r = _guarded_run_once(monkeypatch, "go", {"main.go": b"1", ".gocache/x": b"x"}, "run")
    assert isinstance(r, tuple) and ".gocache/x" in r[1]


def test_run_batch_writes_rejected_and_the_counter_for_reserved_rows_of_both_kinds_and_keeps_going(tmp_path, monkeypatch):
    """Through the REAL cli.run_batch and the REAL run_repeated/run_once: a reserved key in a run row and in a suite row is rejected (no run, no
    execution counted), the counter is bumped once per row, and the batch goes on to the next row."""
    import base64
    from od_sbx import cli, runner, selftest
    b64 = lambda b: base64.b64encode(b).decode()
    mf = tmp_path / "IMAGE_MANIFEST.json"
    mf.write_text("{}")
    monkeypatch.setattr(cli, "MANIFEST", mf)
    monkeypatch.setattr(cli, "_selftest_ok", lambda: (True, "ok"))
    monkeypatch.setattr(selftest, "host_guards", lambda: [])
    monkeypatch.setattr(cli, "cleanup_containers", lambda: None)
    monkeypatch.setattr(cli, "load_manifest", lambda: {"runsc_version_line": "x", "toolchains": {"python": {"image_id": "sha256:x"}}})

    def no_stage(tree):
        raise AssertionError("a rejected row must never be staged")
    monkeypatch.setattr(runner, "stage", no_stage)
    monkeypatch.setattr(runner.subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(AssertionError("a rejected row must never reach docker")))
    real = runner.run_repeated

    def routed(tool, files, argv, **kw):
        if kw["row"] == "good":
            res = runner.RunResult("OK", 0, None, 0.1, b"", b"", "h", 0, 0, False, False)
            return runner.RepeatedResult([res, res], True)
        return real(tool, files, argv, **kw)
    monkeypatch.setattr(cli, "run_repeated", routed)
    rows = [
        {"row_id": "bad_run", "toolchain": "python", "kind": "run", "argv": ["python", "t.py"], "files": {"t.py": b64(b"1"), ".tmp/x": b64(b"2")}},
        {"row_id": "bad_suite", "toolchain": "python", "kind": "suite", "argv": ["python", "-s", "-P", "-m", "pytest"],
         "files": {"s.py": b64(b"1")}, "suite_files": {"./.tmp/y": b64(b"2")}},
        {"row_id": "bad_go_run", "toolchain": "go", "kind": "run", "argv": ["go", "run", "."], "files": {"m.go": b64(b"1"), ".gocache/z": b64(b"2")}},
        {"row_id": "good", "toolchain": "python", "kind": "run", "argv": ["python", "t.py"], "files": {"t.py": b64(b"1")}},
    ]
    jobs = tmp_path / "jobs.jsonl"
    jobs.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    out = tmp_path / "out.jsonl"
    assert cli.run_batch(str(jobs), str(out)) == 0
    got = [json.loads(x) for x in out.read_text().splitlines()]
    assert [g["row_id"] for g in got] == ["bad_run", "bad_suite", "bad_go_run", "good"]
    for g in got[:3]:
        assert "rejected" in g and "executor-owned name" in g["rejected"] and "runs" not in g, g
    assert got[3]["deterministic"] is True and "rejected" not in got[3]
    m = json.loads((tmp_path / "out.jsonl.manifest.json").read_text())
    assert m["counters"] == {"rejected_unstageable_tree": 3} and m["executions"] == 2     # only the good row's 2 runs were counted


def test_selftest_requires_the_temp_dir_as_the_exact_last_line_in_every_determinism_fixture():
    from od_sbx.config import WORK_TMP
    assert T.last_line(b"6 ok\n/work/.tmp\n") == WORK_TMP and T.last_line(b"/work/.tmp") == WORK_TMP
    for bad in (b"/work/.tmpx\n", b"x /work/.tmp\n", b"/work/.tmp\nmore\n", b"/work\n", b"", b"/work/.tmp\n\n"):
        assert T.last_line(bad) != WORK_TMP, bad
    src = inspect_source(T.st6)
    assert "last_line(r0.stdout) == WORK_TMP" in src and "in r0.stdout" not in src
    # each fixture prints the temp dir ALONE as its last statement (parse only, never run), and puts a file in it where it can
    assert F.DETERMINISTIC["python"]["t.py"].endswith("print(tempfile.gettempdir())\n") and "mkdtemp()" in F.DETERMINISTIC["python"]["t.py"]
    assert F.DETERMINISTIC["node"]["t.js"].endswith("console.log(os.tmpdir());\n") and "mkdtempSync" in F.DETERMINISTIC["node"]["t.js"]
    assert "fmt.Println(os.TempDir()) }" in F.DETERMINISTIC["go"]["m.go"]
    assert F.DETERMINISTIC["sh"]["t.sh"].endswith('printf \'%s\\n\' "$TMPDIR"\n') and 'touch "$TMPDIR/x"' in F.DETERMINISTIC["sh"]["t.sh"]
    # the Go fixtures keep go.mod at the /work root (the layout that broke with TMPDIR=/work); WORK_TMP must never equal that directory
    assert "go.mod" in F.DETERMINISTIC["go"] and "go.mod" in F.GO_TEST and WORK_TMP != "/work"


def inspect_source(fn):
    import inspect
    return inspect.getsource(fn)


# ------------------------------------------------------------------ S2 interfaces probe
def test_iface_probe_is_not_vacuous():
    assert "if_nameindex" in F.NET_IFACES["t.py"] and "IFACES" in F.NET_IFACES["t.py"]


# ------------------------------------------------------------------ S3 shadow modules
def test_sanitize_strips_shadow_modules_and_hooks_but_keeps_ordinary_files():
    files = {k: b"" for k in ["solution.py", "test_hidden.py", "helpers/util.py", "pytest_helpers.py", "conftest.py", "sub/conftest.py",
                              "pytest.py", "_pytest/__init__.py", "pluggy/x.py", "py.py", ".local/lib/python3.12/site-packages/a.py",
                              "x.pth", "m.pyc", "__pycache__/a.cpython-312.pyc", "sitecustomize.py", "go.work", "package.json"]}
    kept, removed = sanitize_report(files)
    assert sorted(kept) == ["helpers/util.py", "pytest_helpers.py", "solution.py", "test_hidden.py"]
    assert len(removed) == len(files) - 4 and sanitize(files) == kept
    # shadow/user-site/bytecode rules are python-only; hook files (conftest, package.json, go.work ...) are stripped for every toolchain
    nk, nr = sanitize_report({"py/a.js": b"", "packaging/x.js": b"", "package.json": b"", "go.work": b"", "main.go": b""}, "node")
    assert sorted(nk) == ["main.go", "packaging/x.js", "py/a.js"] and sorted(nr) == ["go.work", "package.json"]


def test_suite_prefix_requires_dash_s_dash_P():
    assert T.PYTEST_HIDDEN[:3] == ["python", "-s", "-P"]
    assert _suite_argv_ok("python", "suite", ["python", "-s", "-P", "-m", "pytest"])
    assert not _suite_argv_ok("python", "suite", ["python", "-m", "pytest"])
    assert _suite_argv_ok("python", "run", ["python", "t.py"]) and _suite_argv_ok("go", "suite", ["go", "test"])
    assert "PYTHONNOUSERSITE=1" in read("images/Dockerfile.python")


# ------------------------------------------------------------------ S4 report encoding
def test_junit_must_be_plain_utf8():
    ok = '<?xml version="1.0" encoding="utf-8"?><testsuites><testsuite><testcase classname="a" name="b"/></testsuite></testsuites>'
    assert V.parse_junit(ok.encode()) == {"a::b": "passed"}
    dtd = '<?xml version="1.0"?><!DOCTYPE x [<!ENTITY e "v">]><testsuites><testsuite><testcase classname="a" name="b"/></testsuite></testsuites>'
    for bad in [ok.replace("utf-8", "utf-16").encode("utf-16"), dtd.encode("utf-16-le"), dtd.encode("utf-16-be"),
                dtd.replace("1.0\"?", "1.0\" encoding=\"utf-16\"?").encode("utf-16"), ok.replace("utf-8", "iso-8859-1").encode("latin-1"),
                dtd.encode(), b"\xff\xfe<a/>", b"<a>\xff</a>"]:
        try:
            V.parse_junit(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad[:40]!r}")


def test_verdict_forged_cases():
    ids = {"a::t1", "a::t2"}
    assert V.compute(0, "OK", {"a::t1": "passed", "a::t2": "passed"}, ids).verdict == V.PASS
    assert V.compute(0, "OK", {"a::t1": "passed"}, ids).verdict == V.TAMPERED
    assert V.compute(0, "OK", {"a::t1": "passed", "a::t2": "failed"}, ids).verdict == V.TAMPERED
    assert V.compute(1, "NONZERO", {"a::t1": "passed", "a::t2": "failed"}, ids).verdict == V.FAIL
    assert V.compute(0, "OK", None, ids).verdict == V.NO_REPORT
    assert V.compute(None, "TIMEOUT", None, ids).verdict == V.TIMEOUT


# ------------------------------------------------------------------ S5 / S6
def test_s5_s6():
    s10 = read("build/10_install_base.sh")
    assert "unattended-upgrades" in s10 and "apt-daily" in s10 and "mask" in s10
    assert "host_python3" in read("build/60_finalize_image.sh")
    assert "Wants=network-online.target" in read("host/od-sbx-selftest.service")


# ------------------------------------------------------------------ misc found by the skeptic
def test_container_names_are_docker_safe():
    for raw in ["T56:abc/1", "-x", "ok_name.1", "a b", "é"]:
        n = safe_name(raw)
        assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", n), (raw, n)


def test_every_blocked_probe_requires_a_marker():
    for fx in [F.NET_TCP_PUBLIC, F.NET_TCP_METADATA, F.NET_UDP_DNS, F.NET_DOCKER_SOCK, F.WRITE_OUTSIDE, F.WRITE_PROC_SYS, F.WRITE_IN_RO,
               F.PRIV_UNSHARE]:
        assert "except OSError" in fx["t.py"] and "BLOCKED" in fx["t.py"]


def test_all_fixture_python_sources_parse_without_running_them():
    n = 0
    for name in dir(F):
        v = getattr(F, name)
        if name.isupper() and isinstance(v, dict):
            for fn, src in v.items():
                if fn.endswith(".py"):
                    ast.parse(src, fn)
                    n += 1
    assert n > 20


def test_selftest_ids_match_recipe_section7():
    txt = read("IMAGE_RECIPE.md")
    sec = txt[txt.index("## 7. Executor self-test list"):txt.index("## 8. Image creation")]
    ids = []
    for line in sec.splitlines():
        m = re.match(r"\| (ST-[\d.]+i?)(?: to (?:ST-)?([\d.]+))? \|", line)
        if not m:
            continue
        a, b = m.group(1), m.group(2)
        if b:
            pre, lo = a.rsplit(".", 1)
            ids += [f"{pre}.{i}" for i in range(int(lo), int(b.split('.')[-1]) + 1)]
        else:
            ids.append(a)
    assert sorted(ids) == sorted(c.id for c in T.CHECKS), (set(ids) ^ {c.id for c in T.CHECKS})


def test_hostfw_and_units_basics():
    nft = read("host/hostfw.nft")
    assert nft.count("policy drop;") == 3 and "meta skuid 0 ip daddr 169.254.169.254 accept" in nft
    assert "ip saddr 169.254.169.254 udp sport 67 udp dport 68 accept" in nft
    assert "ExecStartPre=/usr/bin/rm -f /var/lib/od-sbx/selftest.json" in read("host/od-sbx-selftest.service")


def test_all_shell_scripts_parse():
    bash = shutil.which("bash")
    for f in sorted(os.listdir(os.path.join(SBX, "build"))):
        if f.endswith(".sh"):
            r = subprocess.run([bash, "-n", os.path.join(SBX, "build", f)], capture_output=True, text=True)
            assert r.returncode == 0, (f, r.stderr)


def test_manifest_keys_used_by_the_executor_are_written_by_step60():
    s60 = read("build/60_finalize_image.sh")
    for key in ["runsc_version_line", "executor_py_tree_sha256", "docker_storage_driver", "pytest", "toolchains"]:
        assert key in s60, key


# ------------------------------------------------------------------ plumbing test with a FAKE docker (no container, nothing generated runs)
def test_run_once_plumbing_with_fake_docker(tmp_path, monkeypatch):
    from od_sbx import runner
    seen = tmp_path / "seen"
    seen.mkdir()
    fake = tmp_path / "bin" / "docker"
    fake.parent.mkdir()
    fake.write_text(f'''#!{sys.executable}
import os, sys, shutil, json
a = sys.argv[1:]
seen = {str(seen)!r}
if a[0] == "run":
    ins = [x for x in a if x.startswith("type=bind")]
    d = dict(kv.split("=", 1) for kv in ins[0].split(",") if "=" in kv); o = dict(kv.split("=", 1) for kv in ins[1].split(",") if "=" in kv)
    shutil.copytree(d["src"], os.path.join(seen, "in"), dirs_exist_ok=True)
    open(os.path.join(seen, "argv.json"), "w").write(json.dumps(a))
    open(os.path.join(o["src"], "junit.xml"), "w").write('<testsuites><testsuite><testcase classname="test_hidden" name="test_add"/></testsuite></testsuites>')
    print("hello")
elif a[0] == "inspect":
    print("0 false")
sys.exit(0)
''')
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", str(fake.parent) + os.pathsep + os.environ["PATH"])
    monkeypatch.setattr(runner, "STAGE_ROOT", tmp_path / "stage")
    monkeypatch.setattr(runner.os, "chown", lambda *a, **k: None)
    man = {"toolchains": {"python": {"image_id": "sha256:abc"}}}
    patch = {"solution.py": b"PATCH", "conftest.py": b"EVIL", "test_hidden.py": b"PATCH_VERSION_OF_HIDDEN", "pytest.py": b"EVIL"}
    suite = {"test_hidden.py": b"PRISTINE", "conftest.py": b"LEGIT_SUITE_FIXTURE"}
    r = runner.run_once("python", patch, ["python", "-s", "-P", "-m", "pytest"], kind="suite", name="od-sbx-b-T56:row/1-0",
                        manifest=man, read_back=["junit.xml"], overlay=suite)
    got = {p.relative_to(seen / "in").as_posix(): p.read_bytes() for p in (seen / "in").rglob("*") if p.is_file()}
    assert got == {"solution.py": b"PATCH", "test_hidden.py": b"PRISTINE", "conftest.py": b"LEGIT_SUITE_FIXTURE"}
    assert sorted(r.stripped) == ["conftest.py", "pytest.py"] and r.outcome == "OK" and r.stdout == b"hello\n"
    assert "junit.xml" in r.out_files
    argv = json.loads((seen / "argv.json").read_text())
    assert "od-sbx-b-T56_row_1-0" in argv and "sha256:abc" in argv       # docker-safe name, image by id
    assert not list((tmp_path / "stage").iterdir()), "stage dir must be removed after the run"


# ------------------------------------------------------------------ second-read additions (skeptic 2, 18 Oct 2026)
def test_overlay_wins_over_clashing_patch_paths_and_nothing_is_fatal(tmp_path, monkeypatch):
    from od_sbx import runner
    monkeypatch.setattr(runner, "STAGE_ROOT", tmp_path / "stage")
    monkeypatch.setattr(runner.os, "chown", lambda *a, **k: None)
    tree = {"solution.py": b"S", "test_hidden.py": b"PATCH", "./test_hidden.py": b"PATCH2", "test_hidden.py/x": b"CLASH",
            "tests": b"FILE-WHERE-DIR-NEEDED", "tests/../tests2.py": b"ok"}
    overlay = {"test_hidden.py": b"PRISTINE", "tests/test_a.py": b"PRISTINE_A"}
    removed = runner._drop_overlay_conflicts(tree, overlay)
    assert sorted(removed) == ["./test_hidden.py", "test_hidden.py/x", "tests"]   # an exact same-key entry is replaced silently, aliases are dropped
    tree.update(overlay)
    root, din, _ = runner.stage(tree)
    assert (din / "test_hidden.py").read_bytes() == b"PRISTINE" and (din / "tests" / "test_a.py").read_bytes() == b"PRISTINE_A"
    assert (din / "solution.py").read_bytes() == b"S"


def test_stage_failures_raise_stageerror_and_leave_no_run_dir(tmp_path, monkeypatch):
    import pytest
    from od_sbx import runner
    monkeypatch.setattr(runner, "STAGE_ROOT", tmp_path / "stage")
    monkeypatch.setattr(runner.os, "chown", lambda *a, **k: None)
    for bad in ({"../escape.py": b"x"}, {"/abs.py": b"x"}, {"a": b"x", "a/b": b"y"}, {"a/b": b"y", "a": b"x"}):
        with pytest.raises(runner.StageError):
            runner.stage(bad)
        assert not list((tmp_path / "stage").iterdir()), bad
    assert issubclass(runner.StageError, ValueError)


def test_run_dir_is_removed_even_when_the_launch_fails(tmp_path, monkeypatch):
    import pytest
    from od_sbx import runner
    monkeypatch.setattr(runner, "STAGE_ROOT", tmp_path / "stage")
    monkeypatch.setattr(runner.os, "chown", lambda *a, **k: None)
    monkeypatch.setattr(runner.subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(OSError("docker missing")))
    man = {"toolchains": {"python": {"image_id": "sha256:abc"}}}
    with pytest.raises(OSError):
        runner.run_once("python", {"solution.py": b"S"}, ["python", "t.py"], name="n", manifest=man)
    assert not list((tmp_path / "stage").iterdir()), "an exception must not leak a run dir onto the 512 MiB tmpfs"


def test_run_batch_rejects_an_unstageable_row_and_keeps_going(tmp_path, monkeypatch):
    import base64
    from od_sbx import cli, runner, selftest
    b64 = lambda b: base64.b64encode(b).decode()
    mf = tmp_path / "IMAGE_MANIFEST.json"
    mf.write_text("{}")
    monkeypatch.setattr(cli, "MANIFEST", mf)
    monkeypatch.setattr(cli, "_selftest_ok", lambda: (True, "ok"))
    monkeypatch.setattr(selftest, "host_guards", lambda: [])
    monkeypatch.setattr(cli, "cleanup_containers", lambda: None)
    monkeypatch.setattr(cli, "load_manifest", lambda: {"runsc_version_line": "x", "toolchains": {}})
    calls = []

    def fake_repeated(tool, files, argv, **kw):
        calls.append(kw["row"])
        if kw["row"] == "bad":
            raise runner.StageError("path escapes staging dir: '../x'")
        res = runner.RunResult("OK", 0, None, 0.1, b"", b"", "h", 0, 0, False, False)
        return runner.RepeatedResult([res, res], True)
    monkeypatch.setattr(cli, "run_repeated", fake_repeated)
    jobs = tmp_path / "jobs.jsonl"
    jobs.write_text("\n".join(json.dumps({"row_id": r, "toolchain": "sh", "argv": ["sh", "t.sh"], "files": {"t.sh": b64(b"echo")}})
                              for r in ("bad", "good")) + "\n")
    out = tmp_path / "out.jsonl"
    assert cli.run_batch(str(jobs), str(out)) == 0
    rows = [json.loads(x) for x in out.read_text().splitlines()]
    assert calls == ["bad", "good"] and "rejected" in rows[0] and rows[1]["deterministic"] is True
    assert json.loads((tmp_path / "out.jsonl.manifest.json").read_text())["counters"] == {"rejected_unstageable_tree": 1}


def test_classic_store_helper_creates_the_docker_dir_first():
    s = read("build/common.sh")
    body = s[s.index("ensure_classic_store() {"):]
    assert body.index("install -d -m 0755 /etc/docker") < body.index('>/etc/docker/daemon.json')


def test_alias_spellings_cannot_bypass_the_strip_rules_or_the_overlay(tmp_path, monkeypatch):
    """`conftest.py/x/..` has the textual name `..` but stage() resolves it to the file conftest.py: the strip rules must judge the real path."""
    from od_sbx import runner
    seen = tmp_path / "seen"
    seen.mkdir()
    fake = tmp_path / "bin" / "docker"
    fake.parent.mkdir()
    fake.write_text(f'''#!{sys.executable}
import os, sys, shutil
a = sys.argv[1:]
if a[0] == "run":
    ins = [x for x in a if x.startswith("type=bind")]
    d = dict(kv.split("=", 1) for kv in ins[0].split(",") if "=" in kv)
    shutil.copytree(d["src"], os.path.join({str(seen)!r}, "in"), dirs_exist_ok=True)
elif a[0] == "inspect":
    print("0 false")
sys.exit(0)
''')
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", str(fake.parent) + os.pathsep + os.environ["PATH"])
    monkeypatch.setattr(runner, "STAGE_ROOT", tmp_path / "stage")
    monkeypatch.setattr(runner.os, "chown", lambda *a, **k: None)
    man = {"toolchains": {"python": {"image_id": "sha256:abc"}}}
    patch = {"solution.py": b"S", "conftest.py/x/..": b"EVIL", "pytest.py/x/..": b"EVIL", "a/../_pytest/__init__.py": b"EVIL",
             ".local/x/../y.py": b"EVIL", "./test_hidden.py": b"ALIAS", "t//test_hidden.py/.": b"NEST"}
    r = runner.run_once("python", patch, ["python", "-s", "-P", "-m", "pytest"], kind="suite", name="n", manifest=man,
                        overlay={"test_hidden.py": b"PRISTINE"})
    got = {p.relative_to(seen / "in").as_posix(): p.read_bytes() for p in (seen / "in").rglob("*") if p.is_file()}
    assert got == {"solution.py": b"S", "test_hidden.py": b"PRISTINE", "t/test_hidden.py": b"NEST"}, got
    assert sorted(r.stripped) == [".local/y.py", "_pytest/__init__.py", "conftest.py", "pytest.py"], r.stripped
    import pytest
    for bad in ("..", ".", "../x.py", "a/../../x.py", "/etc/x", "x\0y"):
        with pytest.raises(runner.StageError):
            runner.norm_key(bad)


def test_go_scratch_dirs_are_not_taken_from_the_patch():
    from od_sbx.runner import sanitize_report
    kept, removed = sanitize_report({"main.go": b"", "go.mod": b"", "vendor/modules.txt": b"", ".gocache/ab/x-a": b"", ".gopath/pkg/mod/y": b"",
                                     "sub/.gocache/z": b""}, "go")
    assert sorted(kept) == ["go.mod", "main.go", "sub/.gocache/z", "vendor/modules.txt"] and sorted(removed) == [".gocache/ab/x-a", ".gopath/pkg/mod/y"]
    assert sanitize_report({".gocache/a": b""}, "node")[1] == [] and sanitize_report({".gocache/a": b""})[1] == []


def test_daemon_json_can_start_dockerd_and_keeps_the_isolation_keys():
    """Opus sign-off 18 Oct (O1): dockerd refuses to start with iptables=false AND icc=false ("ICC=false uses iptables to function"),
    which would have stopped step 50 at `systemctl restart docker`. ICC is moot here (bridge none, every run --network none), so the key
    is gone; the isolation keys must stay."""
    d = json.loads(read("host/docker-daemon.json"))
    assert not (d.get("iptables") is False and d.get("icc") is False)
    assert d["default-runtime"] == "runsc" and "--network=none" in d["runtimes"]["runsc"]["runtimeArgs"]
    assert d["bridge"] == "none" and d["no-new-privileges"] is True and d["iptables"] is False
    assert d["storage-driver"] == "overlay2" and d["features"]["containerd-snapshotter"] is False
