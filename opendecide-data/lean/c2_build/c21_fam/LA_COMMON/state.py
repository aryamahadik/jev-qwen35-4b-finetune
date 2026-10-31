"""Simulated filesystem / git / infra / SQL / network-package / env / session state (plain data; never executed).

Shared by T50, T51 (as its entity backdrop) and T53. G0-lite T50 section 2 is the spec. Nothing here touches
the real machine: paths are strings, "files" are records, a command only ever changes a copy of this state.
"""
import copy
import fnmatch
import posixpath
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

DATA_CLASSES = ("secret", "confidential", "public")
LANES = ("contained", "shared", "production")
AGENT_CONFIG_KINDS = ("permission", "hook", "gate", "instruction")
# spec_v2 (G0 addendum v3.2 section 4): the 11 path classes of block G, the 3 zones, the consumer kinds
STATE_CLASSES = ("ci_workflow", "git_hook", "lockfile", "env_rc", "cron_systemd", "migration", "iac", "later_run_script")
NONSTATE_CLASSES = ("doc", "source", "test_fixture")
PATH_CLASSES = STATE_CLASSES + NONSTATE_CLASSES
ZONES = ("inside_roots", "outside_roots", "system")
CONSUMER_EXECUTORS = {"ci_workflow": "ci_runner", "git_hook": "git", "lockfile": "package_manager", "env_rc": "login_shell",
                      "cron_systemd": "scheduler", "migration": "migration_runner", "iac": "apply_pipeline",
                      "later_run_script": "later_call"}
# OS and system config directories (generic words; they are real directory names, not entity names).
SYSTEM_PREFIXES = ("/etc", "/usr", "/bin", "/sbin", "/lib", "/boot", "/sys", "/proc", "/dev", "/opt", "/var/lib",
                   "/root")


def norm(path):
    return posixpath.normpath(path)


def under(path, root):
    path, root = norm(path), norm(root)
    return path == root or path.startswith(root.rstrip("/") + "/")


@dataclass
class FsNode:
    path: str
    kind: str = "file"                   # file | dir
    tracked: bool = False
    dirty: bool = False                  # tracked and modified, or untracked-with-content counts via tracked False
    created_by_agent: bool = False
    data_class: str = "public"           # secret | confidential | public (sensitive stems -> secret)
    system_path: bool = False
    backup: bool = False                 # a backup copy exists (visible through a history call)
    agent_config: Optional[str] = None   # permission | hook | gate | instruction : the agent's OWN config
    posture: Optional[str] = None        # login_keys | privilege : files that weaken host security when written
    path_class: Optional[str] = None     # spec_v2: one of PATH_CLASSES (block G); None for ordinary shell-block nodes
    link_target: Optional[str] = None    # alias tables (addendum section 5): a link node (symlink / junction) points at this path
    content: Optional[List[str]] = None  # spec_v2: current content lines of a file a block-G edit changes (None = not recorded)
    visibility: Optional[str] = None     # spec_v2: private | public | unknown (visibility record of the file; R26 secret content)

    def __post_init__(self):
        if self.data_class not in DATA_CLASSES:
            raise ValueError("bad data_class %r" % self.data_class)
        if self.agent_config is not None and self.agent_config not in AGENT_CONFIG_KINDS:
            raise ValueError("bad agent_config %r" % self.agent_config)
        if self.posture is not None and self.posture not in ("login_keys", "privilege"):
            raise ValueError("bad posture %r" % self.posture)


@dataclass
class Consumer:
    """spec_v2: the executor the simulated state records for a state-bearing file (addendum section 4: a file with no
    recorded consumer is non-state, whatever it contains)."""
    kind: str                                                    # one of STATE_CLASSES
    executor: str = ""                                           # ci_runner | git | package_manager | login_shell | ...
    context: str = ""                                            # iac: context the apply targets; migration: the database
    required_checks: List[str] = field(default_factory=list)     # ci_workflow / git_hook: checks this file defines (R16 scope)
    last_run: Dict[str, str] = field(default_factory=dict)       # check -> "failed" | "ok" (last recorded run)
    reviewed: bool = False                                       # content reviewed earlier in the history (edit after review)
    run_by: str = ""                                             # later_run_script: path of the call that runs it


@dataclass
class GitRemote:
    name: str
    host: str
    visibility: str = "private"          # private | public | unknown
    trusted: bool = True


@dataclass
class GitState:
    branch: str = "main"
    protected: List[str] = field(default_factory=list)
    own_branches: List[str] = field(default_factory=list)       # feature branches the user/agent owns
    remotes: Dict[str, GitRemote] = field(default_factory=dict)
    unpushed: List[dict] = field(default_factory=list)          # {"branch": b, "files": [paths]}
    hooks: List[str] = field(default_factory=list)              # pre-commit, pre-push, commit-msg
    last_hook_result: Optional[str] = None                      # None | ok | failed
    review_approved: List[str] = field(default_factory=list)    # branches with an approved review in the session


@dataclass
class InfraResource:
    ctx: str
    kind: str
    name: str
    creator: str = "other"               # agent | other
    label: str = ""


@dataclass
class InfraState:
    contexts: Dict[str, str] = field(default_factory=dict)      # context name -> lane
    resources: List[InfraResource] = field(default_factory=list)

    def lane(self, ctx):
        return self.contexts.get(ctx)

    def find(self, ctx, kind, name):
        for r in self.resources:
            if r.ctx == ctx and r.kind == kind and r.name == name:
                return r
        return None


@dataclass
class SqlTable:
    name: str
    backup_exists: bool = False
    rows: str = "small"                  # small | large


@dataclass
class SqlDb:
    name: str
    env: str = "contained"               # lane of the database (dev = contained)
    tables: Dict[str, SqlTable] = field(default_factory=dict)


@dataclass
class SqlState:
    dbs: Dict[str, SqlDb] = field(default_factory=dict)


@dataclass
class NetState:
    trusted_hosts: List[str] = field(default_factory=list)
    trusted_registries: List[str] = field(default_factory=list)
    lockfile: Dict[str, str] = field(default_factory=dict)      # package -> pinned version
    default_registry: str = ""
    gist_host: str = ""                                         # paste / gist service host (untrusted unless named)


@dataclass
class EnvState:
    vars: Dict[str, bool] = field(default_factory=dict)         # stem -> is_sensitive


@dataclass
class Session:
    written_files: Dict[str, str] = field(default_factory=dict)  # path -> payload id (content known)
    modified_files: List[str] = field(default_factory=list)     # written files edited since: content no longer known
    approvals: List[dict] = field(default_factory=list)


@dataclass
class ProcessState:
    procs: Dict[str, dict] = field(default_factory=dict)        # pid -> {"owner": agent|user|system, "name": str}


@dataclass
class SimState:
    fs: Dict[str, FsNode] = field(default_factory=dict)
    git: GitState = field(default_factory=GitState)
    infra: InfraState = field(default_factory=InfraState)
    sql: SqlState = field(default_factory=SqlState)
    net: NetState = field(default_factory=NetState)
    env: EnvState = field(default_factory=EnvState)
    session: Session = field(default_factory=Session)
    proc: ProcessState = field(default_factory=ProcessState)
    other_homes: List[str] = field(default_factory=list)       # other accounts' home directories (system class)
    consumers: Dict[str, Consumer] = field(default_factory=dict)   # spec_v2: path -> recorded consumer (state-bearing files)
    # ALIAS TABLES (addendum v3.2 section 5). All additive; empty/default values leave every older state unchanged.
    short_names: Dict[str, str] = field(default_factory=dict)      # 8.3 short path -> long path (derived by program)
    ci_roots: List[str] = field(default_factory=list)              # roots whose path resolution is case-insensitive
    cwd: str = ""                                                  # current working directory ("" = not recorded)
    home: str = ""                                                 # the user's home directory ("" = not recorded)

    # ---- helpers -------------------------------------------------------------------------------------
    def add(self, node):
        node.path = norm(node.path)
        self.fs[node.path] = node
        return node

    def node(self, path):
        return self.fs.get(norm(path))

    def remove(self, path):
        self.fs.pop(norm(path), None)

    def children(self, dirpath):
        d = norm(dirpath)
        return [n for p, n in sorted(self.fs.items()) if posixpath.dirname(p) == d]

    def glob(self, pattern):
        """fnmatch inside ONE directory; '*' never matches '/', and a leading '.' needs an explicit '.'."""
        pattern = norm(pattern) if not any(c in pattern for c in "*?[") else pattern
        d, base = posixpath.split(pattern)
        out = []
        for p, n in sorted(self.fs.items()):
            if posixpath.dirname(p) != d:
                continue
            b = posixpath.basename(p)
            if b.startswith(".") and not base.startswith("."):
                continue
            if fnmatch.fnmatchcase(b, base):
                out.append(p)
        return out

    def has_dirty_or_untracked(self):
        """git working-tree dirtiness: a tracked modified file or an untracked file."""
        return any(n.kind == "file" and ((n.tracked and n.dirty) or (not n.tracked)) for n in self.fs.values()
                   if not n.system_path and n.agent_config is None and not n.path.endswith(".bak"))

    def clone(self):
        return copy.deepcopy(self)

    def to_dict(self):
        return asdict(self)

    # ---- validation ----------------------------------------------------------------------------------
    def validate(self):
        """SLT-1 constraint (R2-T50-a / 11.3a): created_by_agent is true only in a contained lane."""
        problems = []
        for r in self.infra.resources:
            lane = self.infra.contexts.get(r.ctx)
            if lane is None:
                problems.append("resource %s/%s in unknown context" % (r.ctx, r.name))
            if r.creator == "agent" and lane != "contained":
                problems.append("agent-created resource %s/%s in %s lane (SLT-1 constraint)" % (r.ctx, r.name, lane))
        for p, n in self.fs.items():
            if p != n.path:
                problems.append("fs key/path mismatch %s" % p)
        # Q13.2: trust comes ONLY from the card's trusted_registries; a default registry that is not on that list is not trusted, so the generator keeps
        # the two equal in every generated state (an assert here), and a lock source pointing at an off-list default is a custom index (R14)
        if self.net.default_registry and self.net.default_registry not in self.net.trusted_registries:
            problems.append("net.default_registry %r is not on trusted_registries (Q13.2)" % self.net.default_registry)
        return problems


def inside_roots(path, roots):
    return any(under(path, r) for r in roots)


def zone_of(path, roots, state=None):
    """spec_v2 zone of a path: inside_roots | outside_roots | system (system wins)."""
    if is_system_path(path, state):
        return "system"
    return "inside_roots" if inside_roots(path, roots) else "outside_roots"


def is_system_path(path, state=None):
    p = norm(path)
    homes = ()
    if state is not None:
        n = state.fs.get(p)
        if n is not None and n.system_path:
            return True
        homes = state.other_homes
    if any(under(p, s) for s in SYSTEM_PREFIXES):
        return True
    return any(under(p, h) for h in homes)
