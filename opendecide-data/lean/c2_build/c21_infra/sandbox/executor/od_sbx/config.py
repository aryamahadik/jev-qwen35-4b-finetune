"""Single source for limits, paths and the toolchain table. Values mirror codeexec.md 5.4."""
from dataclasses import dataclass
from pathlib import Path

ROOT = Path("/opt/od-sbx")
MANIFEST = ROOT / "IMAGE_MANIFEST.json"
STAGE_ROOT = Path("/srv/od-sbx/stage")        # root-owned 0700; per-run dirs below it
STATE_DIR = Path("/var/lib/od-sbx")
SELFTEST_JSON = STATE_DIR / "selftest.json"
NOBODY = 65534
LABEL = "od-sbx=1"


@dataclass(frozen=True)
class Limits:
    pids: int = 256
    memory: str = "1g"            # --memory and --memory-swap equal: no swap
    cpus: str = "1"
    nofile: int = 256
    fsize_bytes: int = 64 * 1024 * 1024
    tmpfs_work: str = "256m"
    timeout_run_s: float = 10.0
    timeout_suite_s: float = 60.0
    stdout_cap: int = 64 * 1024
    stderr_cap: int = 64 * 1024
    kill_grace_s: float = 5.0


LIMITS = Limits()
REPEATS_DEFAULT = 2
REPEATS_WILL_THIS_TEST_FAIL = 3

# toolchain key -> name used in IMAGE_MANIFEST["toolchains"]; the executor runs images BY IMAGE ID from the manifest,
# never by tag, so a retagged image cannot be picked up.
TOOLCHAINS = {
    "python": {"manifest_key": "python"},
    "node": {"manifest_key": "node"},
    "go": {"manifest_key": "go"},
    "sh": {"manifest_key": "sh"},
}

# F-GO1 (first boot of the image, ST-6.3 / ST-6.6): cmd/go treats a go.mod whose directory IS os.TempDir() as non-existent
# ("go: warning: ignoring go.mod in system temp root /work", then "go.mod file not found"). With TMPDIR=/work every Go row (go.mod at the
# /work root) failed. The temp dir is therefore /work/.tmp: still inside the size-capped /work tmpfs (no new mount, same cap, same read-only
# root), created fresh by the run prelude (dockercmd) for EVERY toolchain, and a reserved top-level name (RESERVED_TOP): a patch or overlay key
# under it makes the row unstageable (runner._reject_reserved -> StageError -> cli `rejected`, counted), so it is never run on an altered tree
# and can never make the prelude's mkdir fail.
WORK_TMP = "/work/.tmp"
RESERVED_TOP = frozenset({".tmp"})

# environment applied to EVERY run in addition to the image ENV (determinism block of the spec). The executor's --env wins over the image
# ENV, so the stale `TMPDIR=/work` still baked into the four Dockerfiles is never seen by an executor run.
BASE_ENV = {
    "TZ": "UTC",
    "TMPDIR": WORK_TMP,         # S1 (Opus 10.1): / is read-only and /tmp does not exist as a writable path; Go t.TempDir(), node os.tmpdir(),
                                # python tempfile and pytest tmp_path all need a writable temp dir. F-GO1 (first boot, 18 Oct): it must be a
                                # SUBDIRECTORY of /work, never /work itself (see WORK_TMP)
    "LANG": "C.UTF-8",
    "PYTHONHASHSEED": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
    "GOFLAGS": "-mod=vendor",
    "GOPROXY": "off",
    "GOTOOLCHAIN": "local",
    "GOCACHE": "/work/.gocache",
}

# Per-toolchain overrides (M3). The Go std build cache is pre-warmed into the image at /opt/gocache-seed and COPIED into the run's
# tmpfs before the command (a read-only GOCACHE does not work: go writes the user package's outputs to it). The go tmpfs is larger
# to hold the seed plus the user build; the seed size is printed by the Dockerfile build, and ST-6.3 / ST-6.6 are the timing controls.
# UNMEASURED: the first self-test run decides whether 512m fits inside the 1g memory limit; adjust here, not in the image.
SEEDS = {"go": ("/opt/gocache-seed", "/work/.gocache")}
TMPFS_WORK = {"go": "512m"}

# Files the patch may NOT carry into a verdict run (they can rewrite reports or hook the interpreter). The executor
# deletes them from the staged tree; the hidden suite is copied in AFTER the patch from a pristine copy (T56-3).
STRIP_NAMES = frozenset({"conftest.py", "pytest.ini", "tox.ini", "setup.cfg", "pyproject.toml",
                         "sitecustomize.py", "usercustomize.py", "go.work", ".npmrc", "package.json"})
STRIP_SUFFIXES = (".pth", ".pyc", ".pyo")
# S3 (Opus 10.1): `python -m pytest` puts the cwd on sys.path, so a patch file /work/pytest.py replaces pytest; pytest also inserts the
# test dir into sys.path while collecting, which exposes its lazily imported dependencies. These module names (as `X.py` or a path
# component) are removed from a patch tree before a verdict run. `.local` is the user-site (HOME=/work) and __pycache__ holds
# precompiled modules; both are removed too. Suites are run as `python -s -P -m pytest` (PYTEST_ARGV in selftest/cli).
STRIP_MODULES = frozenset({"pytest", "_pytest", "pluggy", "py", "iniconfig", "packaging", "pygments"})
STRIP_DIRS = frozenset({".local", "__pycache__"})
# Go: GOCACHE and GOPATH live at /work/.gocache and /work/.gopath, seeded/owned by the executor (M3). A patch has no reason to ship them, and a
# pre-poisoned cache entry for a std package outside the seed would be trusted by `go test`; the seed copy only overwrites what it contains.
STRIP_GO_TOP_DIRS = frozenset({".gocache", ".gopath"})
TRUSTED_PYTEST_INI = "/etc/od-sbx/pytest.ini"   # baked into the python image; the patch cannot replace it
