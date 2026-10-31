"""Run one container (timeouts and caps enforced from OUTSIDE), or N times with a determinism comparison."""
from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path, PurePosixPath
from typing import Mapping, Sequence

from .config import (LIMITS, MANIFEST, NOBODY, REPEATS_DEFAULT, RESERVED_TOP, SEEDS, STAGE_ROOT, STRIP_DIRS, STRIP_GO_TOP_DIRS,
                     STRIP_MODULES, STRIP_NAMES, STRIP_SUFFIXES, TMPFS_WORK, TOOLCHAINS, Limits)
from .dockercmd import RunPlan, build_run_argv


@dataclass
class RunResult:
    outcome: str                      # OK | TIMEOUT | OOM | SIGNALED | NONZERO | ERROR
    exit_code: int | None
    signal: int | None
    wall_s: float
    stdout: bytes                     # capped
    stderr: bytes                     # capped
    stdout_sha256: str                # over ALL bytes seen, so truncation is still comparable
    stdout_total: int
    stderr_total: int
    stdout_truncated: bool
    stderr_truncated: bool
    out_files: dict[str, bytes] = field(default_factory=dict)   # report files read back after exit (size-capped)
    stripped: list[str] = field(default_factory=list)           # patch files removed by sanitize() before a verdict run (never silent)

    def brief(self) -> dict:
        d = asdict(self)
        d["stdout"] = self.stdout[:200].decode("utf-8", "replace")
        d["stderr"] = self.stderr[:200].decode("utf-8", "replace")
        d["out_files"] = {k: len(v) for k, v in self.out_files.items()}
        d["stripped"] = self.stripped[:20]
        return d


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text())


def image_id(toolchain: str, manifest: Mapping | None = None) -> str:
    m = manifest or load_manifest()
    return m["toolchains"][TOOLCHAINS[toolchain]["manifest_key"]]["image_id"]


class _Capped(threading.Thread):
    """Drain a pipe to EOF so the child never blocks; keep only the first `cap` bytes; hash everything."""

    def __init__(self, pipe, cap: int):
        super().__init__(daemon=True)
        self.pipe, self.cap = pipe, cap
        self.buf = bytearray()
        self.total = 0
        self.h = hashlib.sha256()

    def run(self):
        while True:
            chunk = self.pipe.read(65536)
            if not chunk:
                return
            self.total += len(chunk)
            self.h.update(chunk)
            if len(self.buf) < self.cap:
                self.buf += chunk[: self.cap - len(self.buf)]


def _sh(args: Sequence[str], timeout: float = 30.0) -> subprocess.CompletedProcess:
    return subprocess.run(list(args), capture_output=True, timeout=timeout, check=False)


class StageError(ValueError):
    """A patch tree that cannot be staged (unusable or escaping path, file/directory clash). The row is rejected and counted by the
    caller; it must never abort the batch."""


def norm_key(rel: str) -> str:
    """The path a tree entry will really occupy. Judging the RAW key is unsafe: `conftest.py/x/..` has the textual name `..` (so no strip
    rule matches it) but `stage()` resolves it to the file `conftest.py`. Everything (strip rules, overlay, staging) works on this form."""
    n = posixpath.normpath(rel)
    if "\x00" in rel or n in (".", "..") or n.startswith(("/", "../")):
        raise StageError(f"unusable path in tree: {rel!r}")
    return n


def _strip_reason(rel: str, toolchain: str = "python") -> str | None:
    n = posixpath.normpath(rel)
    parts = PurePosixPath(n).parts
    if not parts or n == "..":
        return "invalid"
    name = parts[-1]
    if name in STRIP_NAMES:
        return "name"
    if toolchain == "go":              # the executor's own cache/GOPATH dirs (config.STRIP_GO_TOP_DIRS)
        return "dir" if parts[0] in STRIP_GO_TOP_DIRS else None
    if toolchain != "python":          # module-shadowing / user-site / bytecode rules are about the python interpreter only
        return None
    if n.endswith(STRIP_SUFFIXES):
        return "suffix"
    if any(d in STRIP_DIRS for d in parts[:-1]):
        return "dir"
    stem = name[:-3] if name.endswith(".py") else None
    if (stem in STRIP_MODULES) or any(d in STRIP_MODULES for d in parts[:-1]):
        return "shadow-module"
    return None


def sanitize_report(files: Mapping[str, bytes], toolchain: str = "python") -> tuple[dict[str, bytes], list[str]]:
    """Drop report-rewriting / interpreter-hooking / module-shadowing files from a patch tree (verdict runs only).
    Returns (kept, removed_paths) so the caller can record what was removed (no silent drops)."""
    kept: dict[str, bytes] = {}
    removed: list[str] = []
    for k, v in files.items():
        if _strip_reason(k, toolchain):
            removed.append(k)
        else:
            kept[k] = v
    return kept, removed


def sanitize(files: Mapping[str, bytes]) -> dict[str, bytes]:
    return sanitize_report(files)[0]


_NAME_BAD = re.compile(r"[^A-Za-z0-9_.-]")


def safe_name(name: str) -> str:
    """Docker container names allow [A-Za-z0-9][A-Za-z0-9_.-]*; row ids from jobs may contain anything."""
    n = _NAME_BAD.sub("_", name)[:120]
    return n if n and n[0].isalnum() else "r" + n


def _drop_overlay_conflicts(tree: dict[str, bytes], overlay: Mapping[str, bytes]) -> list[str]:
    """Remove patch entries that cannot coexist with the pristine overlay: a patch FILE where the suite needs a directory, a patch path
    BELOW a suite file (`test_hidden.py/x`), and ALIAS spellings of a suite file (`./test_hidden.py`, which would be written after the
    suite's own entry and win). Without this the suite does not always win (T56-3) or staging raises. An entry with exactly the SAME key
    as an overlay file is not reported: the overlay simply replaces it. Returns the removed keys."""
    ov = {posixpath.normpath(k) for k in overlay}
    ov_dirs = {d for o in ov for d in _ancestors(o)}
    removed: list[str] = []
    for k in list(tree):
        n = posixpath.normpath(k)
        if n in ov:
            if k != n:                      # an ALIAS spelling of a suite file (`./test_hidden.py`) would be written after it and win
                del tree[k]
                removed.append(k)
            continue
        if n in ov_dirs or any(n.startswith(o + "/") for o in ov):
            del tree[k]
            removed.append(k)
    return removed


def _reject_reserved(files: Mapping[str, bytes], overlay: Mapping[str, bytes] | None, toolchain: str, kind: str) -> None:
    """F-GO1 / D1: raise StageError (-> cli: `rejected` + counter `rejected_unstageable_tree`, the row is DROPPED for every kind) when a tree key
    sits under a name the executor owns. Keys are already normalised (norm_key), so `./.tmp/x` and `a/../.tmp` are caught; `a/.tmp/x` is not
    top level and passes.
      - `.tmp` (config.RESERVED_TOP): the run's TMPDIR /work/.tmp, made by the prelude. Patch AND overlay, run AND suite, every toolchain.
      - Go `.gocache` / `.gopath` (config.STRIP_GO_TOP_DIRS): executor-owned and seeded. Overlay: always. Patch of a "run": rejected. Patch of a
        "suite": NOT rejected here, it is stripped and recorded by sanitize_report as signed off in K6 (10.3) / 10.4 (a), so a declared tamper
        row that ships a poisoned cache can still be executed and labelled by intent."""
    for src, tree in (("patch", files), ("overlay", overlay or {})):
        for k in tree:
            top = k.split("/", 1)[0]
            if top in RESERVED_TOP or (toolchain == "go" and top in STRIP_GO_TOP_DIRS and (src == "overlay" or kind != "suite")):
                raise StageError(f"{src} path {k!r} is under the executor-owned name {top!r}")


def _ancestors(path: str) -> list[str]:
    parts = path.split("/")
    return ["/".join(parts[:i]) for i in range(1, len(parts))]


def stage(files: Mapping[str, bytes]) -> tuple[Path, Path, Path]:
    """Create run dir with in/ (root-owned, read-only mount) and out/ (owned by 65534). Returns (root, in, out).
    On any failure the half-built run dir is removed (STAGE_ROOT is a 512 MiB tmpfs, M4: a leaked dir would eat the cap)."""
    STAGE_ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    root = Path(tempfile.mkdtemp(prefix="run-", dir=STAGE_ROOT))
    try:
        din, dout = root / "in", root / "out"
        din.mkdir(mode=0o755)
        dout.mkdir(mode=0o700)
        os.chown(dout, NOBODY, NOBODY)
        for rel, data in files.items():
            p = (din / rel).resolve()
            if din.resolve() not in p.parents:
                raise StageError(f"path escapes staging dir: {rel!r}")
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
            except (FileExistsError, IsADirectoryError, NotADirectoryError) as e:
                raise StageError(f"file/directory clash at {rel!r}: {type(e).__name__}") from e
            os.chmod(p, 0o755 if rel.endswith((".sh",)) else 0o644)
        for d, _, fs in os.walk(din):                     # world-readable tree
            os.chmod(d, 0o755)
    except BaseException:
        shutil.rmtree(root, ignore_errors=True)
        raise
    return root, din, dout


def cleanup_containers() -> None:
    """Remove every container labelled od-sbx=1 (aborted batch, crashed executor)."""
    ids = _sh(["docker", "ps", "-aq", "--filter", "label=od-sbx=1"]).stdout.decode().split()
    if ids:
        _sh(["docker", "rm", "-f", "-v", *ids], timeout=120)


def run_once(toolchain: str, files: Mapping[str, bytes], argv: Sequence[str], *, kind: str = "run",
             name: str, lim: Limits = LIMITS, manifest: Mapping | None = None,
             read_back: Sequence[str] = (), overlay: Mapping[str, bytes] | None = None) -> RunResult:
    """`files` is the (untrusted) patch tree. On a verdict run (kind="suite") it is sanitized FIRST and `overlay` (the PRISTINE hidden
    suite and its support files) is copied in AFTERWARDS, so the suite always wins over the patch and its own conftest.py/package.json/
    go.work are not stripped (T56-3). Without an overlay, kind="suite" sanitizes the whole tree as before."""
    timeout = lim.timeout_suite_s if kind == "suite" else lim.timeout_run_s
    name = safe_name(name)
    stripped: list[str] = []
    files = {norm_key(k): v for k, v in files.items()}          # alias spellings (`./x`, `a/../x`, `x/y/..`) collapse BEFORE any rule runs
    overlay = {norm_key(k): v for k, v in overlay.items()} if overlay else None
    _reject_reserved(files, overlay, toolchain, kind)           # F-GO1 / D1: executor-owned names make the row unstageable (dropped), never silently altered
    tree = dict(files)
    if kind == "suite":
        tree, stripped = sanitize_report(files, toolchain)
    if overlay:
        stripped = stripped + _drop_overlay_conflicts(tree, overlay)     # suite wins: clashing patch paths are dropped, never fatal
        tree.update(overlay)
    root, din, dout = stage(tree)
    try:           # the run dir lives on a 512 MiB tmpfs (M4): it is removed on EVERY exit path, or leaks would eat the cap
        plan = RunPlan(name=name, image_id=image_id(toolchain, manifest), in_dir=str(din), out_dir=str(dout), argv=argv,
                       tmpfs_work=TMPFS_WORK.get(toolchain), seed=SEEDS.get(toolchain))
        t0 = time.monotonic()
        p = subprocess.Popen(build_run_argv(plan, lim), stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        so, se = _Capped(p.stdout, lim.stdout_cap), _Capped(p.stderr, lim.stderr_cap)
        so.start(); se.start()
        timed_out = False
        try:
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            _sh(["docker", "kill", name])                       # killed from OUTSIDE the container
            try:
                p.wait(timeout=lim.kill_grace_s)
            except subprocess.TimeoutExpired:
                p.kill()
        so.join(5); se.join(5)
        wall = time.monotonic() - t0
        oom = False
        code: int | None = p.returncode
        try:
            ins = _sh(["docker", "inspect", "--format", "{{.State.ExitCode}} {{.State.OOMKilled}}", name])
            if ins.returncode == 0:
                c, o = ins.stdout.decode().split()
                code, oom = int(c), (o == "true")
        finally:
            _sh(["docker", "rm", "-f", "-v", name])
        out_files: dict[str, bytes] = {}
        for rel in read_back:                                   # re-read AFTER exit, size-capped, regular files only
            f = dout / rel
            if f.is_file() and not f.is_symlink() and f.stat().st_size <= 8 * 1024 * 1024:
                out_files[rel] = f.read_bytes()
    finally:
        shutil.rmtree(root, ignore_errors=True)
    sig = code - 128 if code is not None and code > 128 else None
    outcome = ("TIMEOUT" if timed_out else "OOM" if oom else "SIGNALED" if sig else
               "OK" if code == 0 else "NONZERO" if code is not None else "ERROR")
    return RunResult(outcome, code, sig, wall, bytes(so.buf), bytes(se.buf), so.h.hexdigest(), so.total, se.total,
                     so.total > lim.stdout_cap, se.total > lim.stderr_cap, out_files, stripped)


@dataclass
class RepeatedResult:
    results: list[RunResult]
    deterministic: bool
    reason: str = ""


def run_repeated(toolchain: str, files: Mapping[str, bytes], argv: Sequence[str], *, kind: str = "run",
                 batch: str, row: str, repeats: int = REPEATS_DEFAULT, **kw) -> RepeatedResult:
    """Run `repeats` times in fresh containers. A mismatch in exit code or stdout hash means the ROW IS DROPPED by the
    caller and a counter is incremented in the batch manifest (no silent drops)."""
    rs = [run_once(toolchain, files, argv, kind=kind, name=f"od-sbx-{batch}-{row}-{i}", **kw) for i in range(repeats)]
    ok = len({(r.exit_code, r.stdout_sha256) for r in rs}) == 1
    return RepeatedResult(rs, ok, "" if ok else "exit code or stdout hash differs between runs")


class BatchCounters:
    """Counts every drop and abort by reason; written into the batch manifest."""

    def __init__(self):
        self.c: dict[str, int] = {}

    def bump(self, reason: str):
        self.c[reason] = self.c.get(reason, 0) + 1
