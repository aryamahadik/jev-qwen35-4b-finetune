"""Structured command model (the spec side of generate-then-render) and the tables the renderer and the
expander share.

A command is NOT a string here. Cmd(program, global_flags, sub, flags, args, ...) is the spec; render.py turns
it into text through semantics-preserving operators; expander.py (our own, parse-only) turns text back into a
command list; K1 compares the two canonical forms. bashlex and shlex are never used (barred / not a labeller);
quoting below is our own.
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

SEPS = (";", "&&", "||", "|")

# Flags that take values, per program: flag -> number of following words. Anything not listed has arity 0.
# Every flag with a value that a builder emits MUST be listed (a CPU test checks the round trip).
FLAG_ARITY = {
    "git": {"-C": 1, "-c": 1, "-m": 1, "-n": 0, "--set-upstream": 0, "-u": 0},
    "kubectl": {"-n": 1, "--namespace": 1, "--context": 1, "-f": 1, "-o": 1, "--selector": 1, "-l": 1},
    "aws": {"--profile": 1, "--region": 1, "--exclude": 1, "--include": 1, "--instance-ids": 1},
    "gcloud": {"--project": 1, "--zone": 1, "--format": 1, "--source-ranges": 1, "--allow": 1},
    "terraform": {"-var": 1, "-target": 1},
    "docker": {"--context": 1, "-v": 1, "-e": 1, "-p": 1, "--name": 1, "-f": 0},
    "psql": {"-c": 1, "-d": 1, "-h": 1, "-U": 1, "-f": 1},
    "sqlite3": {},
    "mysql": {"-e": 1, "-h": 1, "-u": 1, "-D": 1},
    "pip": {"--index-url": 1, "-i": 1, "--extra-index-url": 1, "--trusted-host": 1, "-r": 1},
    "npm": {"--registry": 1, "--access": 1, "--prefix": 1},
    "yarn": {"--registry": 1},
    "cargo": {"--registry": 1},
    "apt-get": {},
    "brew": {},
    "go": {},
    "curl": {"-X": 1, "-d": 1, "--data": 1, "--data-binary": 1, "-F": 1, "-T": 1, "-H": 1, "-o": 1, "-u": 1,
             "--user": 1, "--url": 1},
    "wget": {"-O": 1, "--header": 1},
    "scp": {"-P": 1, "-i": 1},
    "rsync": {"-e": 1},
    "nc": {"-w": 1, "-q": 1},
    "twine": {"--repository-url": 1, "-r": 1},
    "gh": {"-d": 1, "--desc": 1, "-R": 1},
    "ssh": {"-p": 1, "-i": 1},
    "rm": {}, "rmdir": {}, "cp": {}, "mv": {}, "ln": {}, "mkdir": {}, "touch": {}, "chmod": {}, "chown": {},
    "cat": {}, "head": {"-n": 1}, "tail": {"-n": 1}, "sort": {"-k": 1, "-t": 1}, "wc": {}, "ls": {}, "du": {}, "df": {},
    "ps": {}, "kill": {}, "pkill": {}, "find": {"-name": 1, "-type": 1, "-mtime": 1, "-maxdepth": 1, "-newer": 1,
                                                 "-path": 1, "-iname": 1},
    "grep": {"-e": 1, "--include": 1, "-m": 1}, "sed": {"-e": 1}, "awk": {"-F": 1, "-f": 1}, "tee": {},
    "echo": {}, "printf": {}, "tar": {"-czf": 1, "-xzf": 1, "-cf": 1, "-xf": 1, "-C": 1, "-f": 1},
    "gzip": {}, "unzip": {"-d": 1},
    "base64": {}, "xargs": {"-n": 1, "-I": 1}, "sudo": {"-u": 1}, "timeout": {}, "nohup": {}, "env": {},
    "command": {}, "bash": {"-c": 1}, "sh": {"-c": 1},
    "squeue": {"-u": 1, "-M": 1}, "scancel": {"-M": 1, "-u": 1, "-n": 1},
}

# Programs that take a subcommand, and the multiword subcommands the model knows (longest match first).
SUBCOMMANDS = {
    "git": ("status", "log", "diff", "show", "add", "commit", "push", "pull", "fetch", "merge", "rebase", "reset",
            "clean", "checkout", "switch", "branch", "remote", "stash", "tag", "config", "restore", "init"),
    "kubectl": ("get", "describe", "logs", "apply", "delete", "scale", "rollout", "patch", "edit", "create",
                "exec", "top"),
    "aws": ("s3 ls", "s3 cp", "s3 rm", "s3 sync", "s3 mb", "s3 rb", "ec2 describe-instances",
            "ec2 terminate-instances", "ec2 stop-instances", "iam list-users", "sts get-caller-identity"),
    "gcloud": ("compute instances list", "compute instances delete", "compute firewall-rules create",
               "storage cp", "storage ls", "storage rm", "projects list"),
    "terraform": ("plan", "apply", "destroy", "show", "validate", "init", "state"),
    "docker": ("ps", "images", "run", "rm", "rmi", "stop", "build", "logs", "pull", "exec", "container prune",
               "system prune"),
    "gh": ("gist create", "pr merge", "pr view", "pr create", "pr list", "repo view"),
    "npm": ("install", "ci", "ls", "publish", "run", "test", "audit"),
    "yarn": ("install", "add", "publish"),
    "cargo": ("build", "test", "publish", "install", "add", "fetch"),
    "go": ("get", "build", "test", "mod"),
    "pip": ("install", "list", "download", "freeze", "uninstall"),
    "apt-get": ("install", "update", "remove"),
    "brew": ("install", "list", "update"),
    "twine": ("upload", "check"),
}

# Absolute-binary-path rendering is allowed only for these (registered) paths. Not entity names.
ABS_PATHS = {
    "git": "/usr/bin/git", "rm": "/bin/rm", "ls": "/bin/ls", "cat": "/bin/cat", "cp": "/bin/cp", "mv": "/bin/mv",
    "kubectl": "/usr/local/bin/kubectl", "curl": "/usr/bin/curl", "wget": "/usr/bin/wget", "find": "/usr/bin/find",
    "grep": "/usr/bin/grep", "docker": "/usr/bin/docker", "chmod": "/bin/chmod", "mkdir": "/bin/mkdir",
    "touch": "/usr/bin/touch", "echo": "/bin/echo", "tar": "/usr/bin/tar", "scp": "/usr/bin/scp",
    "psql": "/usr/bin/psql", "pip": "/usr/bin/pip", "npm": "/usr/bin/npm", "aws": "/usr/local/bin/aws",
}
ABS_TO_PROG = {v: k for k, v in ABS_PATHS.items()}

# Operator-added env assignments that are semantics-preserving (registered, harmless).
HARMLESS_ENV = (("LC_ALL", "C"), ("TZ", "UTC"), ("LANG", "C"))
OPERATOR_WRAPPERS = ("timeout", "nohup", "command", "env")      # dropped when comparing canonical command lists
SEMANTIC_WRAPPERS = ("sudo",)
SHELLS = ("sh", "bash")

_SAFE = re.compile(r"^[A-Za-z0-9_@%+=:,./~-]+$")


def quote_word(w):
    """Our own quoting (never shlex). Safe words stay bare; everything else is single-quoted."""
    if w == "":
        return "''"
    if _SAFE.match(w) and not w.startswith("~"):
        return w
    return "'" + w.replace("'", "'\"'\"'") + "'"


class Glob(str):
    """A shell glob pattern argument (rendered bare so the shell expands it; solvers expand it against the
    simulated filesystem). A plain str with the same characters is a LITERAL and is rendered quoted."""


class TildeExpand(str):
    """ALIAS task forms 3/5 (addendum section 5): a bare `~`, `~/...`, `$HOME` or `$HOME/...` argument rendered
    UNQUOTED so the shell would expand it to the home directory. A plain str holding the same characters is a
    LITERAL (quoted by quote_word, since it starts with `~` or `$`) and never expands -- the quoting is what
    "decides whether the shell would expand it" (addendum). Solvers resolve it via SolverA._alias_resolve."""


def is_flag_word(w):
    return len(w) > 1 and w.startswith("-")


@dataclass
class SqlStmt:
    kind: str                       # select | insert | update | delete | drop | truncate | alter | grant | ctas
    table: str
    db: str = ""
    has_predicate: bool = True
    column: str = "state"
    value: str = "1"
    predicate: str = "id = 7"
    grantee: str = "app_role"

    def text(self):
        t, c = self.table, self.column
        if self.kind == "select":
            return "SELECT %s FROM %s%s LIMIT 20" % (c, t, " WHERE %s" % self.predicate if self.has_predicate else "")
        if self.kind == "insert":
            return "INSERT INTO %s (%s) VALUES (%s)" % (t, c, self.value)
        if self.kind == "update":
            return "UPDATE %s SET %s = %s%s" % (t, c, self.value, " WHERE %s" % self.predicate if self.has_predicate else "")
        if self.kind == "delete":
            return "DELETE FROM %s%s" % (t, " WHERE %s" % self.predicate if self.has_predicate else "")
        if self.kind == "drop":
            return "DROP TABLE %s" % t
        if self.kind == "truncate":
            return "TRUNCATE TABLE %s" % t
        if self.kind == "alter":
            return "ALTER TABLE %s ADD COLUMN %s_x INTEGER" % (t, c)
        if self.kind == "grant":
            return "GRANT ALL ON %s TO %s" % (t, self.grantee)
        if self.kind == "ctas":
            return "CREATE TABLE %s_%s AS SELECT * FROM %s" % (t, self.column, t)
        raise ValueError("bad sql kind %r" % self.kind)


@dataclass
class Redir:
    op: str                         # > >> < 2> 2>> 2>&1 <<< <<
    target: str = ""


@dataclass
class Cmd:
    program: str
    global_flags: List[List[str]] = field(default_factory=list)
    sub: Optional[str] = None
    flags: List[List[str]] = field(default_factory=list)
    args: List[str] = field(default_factory=list)
    sudo: bool = False                              # semantic wrapper (R21)
    env: List[Tuple[str, str]] = field(default_factory=list)   # semantic env assignments (not operator-added)
    redirs: List[Redir] = field(default_factory=list)
    sql: Optional[SqlStmt] = None                   # when set, the word '@SQL' in flags/args is the statement text

    def to_dict(self):
        d = {"program": self.program, "global_flags": self.global_flags, "sub": self.sub, "flags": self.flags,
             "args": [{"glob": str(a)} if isinstance(a, Glob) else a for a in self.args], "sudo": self.sudo,
             "env": [list(e) for e in self.env], "redirs": [[r.op, r.target] for r in self.redirs],
             "sql": None if self.sql is None else dict(self.sql.__dict__)}
        return d

    @staticmethod
    def from_dict(d):
        return Cmd(program=d["program"], global_flags=[list(u) for u in d["global_flags"]], sub=d["sub"],
                   flags=[list(u) for u in d["flags"]],
                   args=[Glob(a["glob"]) if isinstance(a, dict) else a for a in d["args"]], sudo=d["sudo"],
                   env=[tuple(e) for e in d["env"]], redirs=[Redir(op, t) for op, t in d["redirs"]],
                   sql=None if d["sql"] is None else SqlStmt(**d["sql"]))

    def words(self):
        """Plain word list after the program: global flags, sub (split on spaces), flags, args. '@SQL' resolved."""
        w = []
        for u in self.global_flags:
            w.extend(u)
        if self.sub:
            w.extend(self.sub.split(" "))
        for u in self.flags:
            w.extend(u)
        w.extend(self.args)
        if self.sql is not None:
            t = self.sql.text()
            w = [t if x == "@SQL" else x for x in w]
        return w

    def canon(self):
        """Order-insensitive over flag units, order-sensitive over positional args (K1 comparison form)."""
        sqltext = self.sql.text() if self.sql is not None else None

        def fix(units):
            return sorted(tuple(sqltext if x == "@SQL" else x for x in u) for u in units)

        args = [sqltext if a == "@SQL" else a for a in self.args]
        return {
            "program": self.program, "global": fix(self.global_flags), "sub": self.sub or "",
            "flags": fix(self.flags), "args": args, "sudo": bool(self.sudo),
            "env": sorted(self.env), "redirs": [(r.op, r.target) for r in self.redirs],
        }


@dataclass
class Item:
    cmd: Cmd
    sep: Optional[str] = None       # separator AFTER this command


@dataclass
class Script:
    items: List[Item] = field(default_factory=list)

    @staticmethod
    def of(*cmds, seps=None):
        seps = list(seps or [])
        items = []
        for i, c in enumerate(cmds):
            items.append(Item(c, seps[i] if i < len(seps) else (";" if i < len(cmds) - 1 else None)))
        s = Script(items)
        s.check()
        return s

    def check(self):
        for i, it in enumerate(self.items):
            last = i == len(self.items) - 1
            if last and it.sep is not None:
                raise ValueError("last item has a separator")
            if not last and it.sep not in SEPS:
                raise ValueError("bad separator %r" % it.sep)

    def cmds(self):
        return [it.cmd for it in self.items]

    def to_dict(self):
        return {"items": [{"cmd": it.cmd.to_dict(), "sep": it.sep} for it in self.items]}

    @staticmethod
    def from_dict(d):
        return Script([Item(Cmd.from_dict(x["cmd"]), x["sep"]) for x in d["items"]])

    def canon(self):
        return [dict(it.cmd.canon(), sep=it.sep or "") for it in self.items]

    def programs(self):
        return sorted({it.cmd.program for it in self.items})


@dataclass
class RawScript:
    """A script that is deliberately NOT structured: an opaque construct (R19) the expander must refuse to
    resolve. `text` is built from namespace names by the generator; `opaque_kind` is what the expander must say."""
    text: str
    opaque_kind: str                # cmdsub | redirect_exec | control_flow | unknown_file | b64_invisible | xargs_dynamic | background
    programs: List[str] = field(default_factory=list)

    def canon(self):
        return [{"raw": self.text, "opaque": self.opaque_kind}]

    def cmds(self):
        return []


OPAQUE_KINDS = ("cmdsub", "redirect_exec", "control_flow", "unknown_file", "b64_invisible", "xargs_dynamic",
                "background", "late_binding")
