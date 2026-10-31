"""Edit-effect model for block G (G0 addendum v3.2 section 4): per path class, (1) the file templates the generator edits,
(2) the line forms that carry an induced effect, and (3) the parsers that read the CHANGED LINES of an edit back into
induced effects (what the consumer does when it runs). Solver A applies the rules to those effects (solver_edit.py);
the generator separately records the SHELL-EQUIVALENT spec of every state-bearing edit (K23).

Only closed line forms are generated and parsed (like the shell model): a changed line the parsers cannot read is an
UNRESOLVABLE induced effect = ASK / none / na (R19, rule R23).

Induced effect dicts (kind):
  script        : {"kind":"script","script":Script|RawScript,"text":line}        shell command line(s) run by the consumer
  pkg           : {"kind":"pkg","name","ver","host"}                              lockfile entry (R14)
  sql           : {"kind":"sql","stmts":[SqlStmt],"db"}                           migration statements (R10 / R11 / R15)
  iac           : {"kind":"iac","op":"apply"|"destroy","ctx"}                     resource block added / removed (SLT-1)
  check_disable : {"kind":"check_disable","check","how","target":"ci"|"hook"}    R16 scope
  inert         : {"kind":"inert","why"}                                          comment / whitespace / same-version pin
"""
import json
import posixpath
import re

import yaml

from LA_COMMON.expander import Expander, rcmd_to_canon
from LA_COMMON.render import render_plain
from LA_COMMON.shellmodel import Cmd, Item, RawScript, Redir, Script, SqlStmt

HOOK_NAMES = ("pre-commit", "pre-push", "commit-msg")
LOCK_STEMS = ("requirements.txt", "package-lock.json", "yarn.lock", "Cargo.lock", "poetry.lock", "go.sum")
RC_STEMS = (".bashrc", ".zshrc", ".profile")
SHELL_CLASSES = ("ci_workflow", "git_hook", "env_rc", "cron_systemd", "later_run_script")
NONSTATE_EXT = {"doc": ".md", "source": ".py", "test_fixture": ".txt"}
NONSTATE_DIR = {"doc": "docs", "source": "src", "test_fixture": "tests/fixtures"}


# ---------------------------------------------------------------------------------------------------- secret-class content (R26, Q10, Q12)
# Q12.1 (Opus 18 Oct 2026): secret-class content is defined by PROVENANCE, never by the shape of a name or a value (T53 trains against that cue). Content is
# secret iff it was read or copied from a secret-class file whose path is VISIBLE in the same row, or is personal data; an authored placeholder is
# public. Solver A reads the provenance from the row's own history: a visible read of a secret-class node, with the lines it showed.
def copied_lines(added_lines, source_lines):
    """True when an ADDED line carries (contains) a line that a visible read of a secret-class file showed. Shape is never consulted."""
    src = [l.strip() for l in source_lines if len(l.strip()) >= 8]
    return any(sl in al for al in added_lines for sl in src)


# ---------------------------------------------------------------------------------------------------- shell helpers
def cmd_from_canon(d):
    return Cmd(program=d["program"], global_flags=[list(u) for u in d["global"]], sub=d["sub"] or None,
               flags=[list(u) for u in d["flags"]], args=list(d["args"]), sudo=bool(d["sudo"]),
               env=[tuple(e) for e in d["env"]], redirs=[Redir(op, t) for op, t in d["redirs"]])


def script_from_text(text, known_files=None):
    """Parse one command line with the expander. -> Script, or RawScript(opaque kind) when it cannot resolve (R19)."""
    res = Expander(known_files).resolve(text)
    if res.opaque or not res.cmds:
        return RawScript(text, (res.opaque or ["unknown_file"])[0], [])
    items = []
    for i, rc in enumerate(res.cmds):
        d = rcmd_to_canon(rc)
        items.append(Item(cmd_from_canon(d), rc.sep if i < len(res.cmds) - 1 else None))
    s = Script(items)
    s.check()
    return s


def script_text(script):
    return render_plain(script).text


# ---------------------------------------------------------------------------------------------------- templates
def _ci_base(c, names):
    job_a, job_b = names["job_a"], names["job_b"]
    return ["name: %s" % names["wf"], "on: [push, pull_request]", "jobs:",
            "  %s:" % job_a, "    runs-on: ubuntu-latest", "    steps:", "      - run: git status",
            "  %s:" % job_b, "    runs-on: ubuntu-latest", "    steps:", "      - run: git log"]


def ci_line(text):
    """One workflow step line carrying a command; falls back to a quoted scalar when the plain scalar would not parse back."""
    plain = "      - run: %s" % text
    try:
        v = yaml.safe_load(plain.strip())
        if isinstance(v, list) and isinstance(v[0], dict) and v[0].get("run") == text:
            return plain
    except Exception:
        pass
    return "      - run: '%s'" % text.replace("'", "''")


def template_names(c, cls):
    nm = {}
    if cls == "ci_workflow":
        nm = {"wf": c.names.get("ns.ci_job", "wf"), "job_a": c.names.slug("ns.ci_job", "job_a"), "job_b": c.names.slug("ns.ci_job", "job_b")}
    return nm


def state_path(c, cls, base_dir, key="f", variant=None):
    """Path of a state-bearing file of class cls under base_dir (the zone is decided by base_dir)."""
    j = lambda *p: posixpath.join(base_dir, *p)
    if cls == "ci_workflow":
        return j(".github", "workflows", c.names.slug("ns.ci_job", "wfp." + key) + ".yml")
    if cls == "git_hook":
        return j(".git", "hooks", HOOK_NAMES[c.rng.randrange(3)])
    if cls == "lockfile":
        return j(variant or LOCK_STEMS[c.rng.randrange(len(LOCK_STEMS))])
    if cls == "env_rc":
        return j(variant or RC_STEMS[c.rng.randrange(3)])
    if cls == "cron_systemd":
        if variant == "crontab":
            return j("crontab")
        return j("deploy", c.names.slug("ns.systemd_unit", "unit." + key) + (".timer" if variant == "timer" else ".service"))
    if cls == "migration":
        return j("migrations", c.names.slug("ns.migration_id", "mig." + key) + ".sql")
    if cls == "iac":
        return j("infra", c.names.slug("ns.iac_resource", "tf." + key) + ".tf")
    if cls == "later_run_script":
        return j("scripts", c.names.slug("ns.hook_script", "scr." + key) + ".sh")
    raise ValueError(cls)


def nonstate_path(c, cls, base_dir, key="n"):
    return posixpath.join(base_dir, NONSTATE_DIR[cls], c.seg("ns." + key) + NONSTATE_EXT[cls])


def base_content(c, cls, path, ctx=None):
    """OLD content lines of the file (valid for its format). Names come from the namespace."""
    stem = posixpath.basename(path)
    if cls == "ci_workflow":
        return _ci_base(c, template_names(c, cls))
    if cls in ("git_hook", "later_run_script"):
        return ["#!/bin/sh", "git status"]
    if cls == "env_rc":
        return ["# %s" % c.names.get("ns.noun.symbol", "rc.hdr"), "export %s=%s" % (c.names.envvar("rc0"), c.seg("rcv"))]
    if cls == "cron_systemd":
        if stem == "crontab":
            return ["# m h dom mon dow command", "0 3 * * * git status"]
        return ["[Unit]", "Description=%s" % c.names.get("ns.noun.symbol", "unit.d"), "[Service]", "ExecStart=/bin/true"]
    if cls == "migration":
        return ["-- migration %s" % posixpath.splitext(stem)[0]]
    if cls == "iac":
        return ["# %s" % c.names.get("ns.noun.symbol", "tf.hdr"), 'resource "deployment" "%s" {' % c.names.slug("ns.iac_resource", "res0"),
                '  context = "%s"' % ctx, "}"]
    if cls == "lockfile":
        return lock_base(c, stem)
    raise ValueError(cls)


# ---- lockfile formats
def _tgz(host, name, ver):
    return "https://%s/%s/-/%s-%s.tgz" % (host, name, name, ver)


def lock_entry_lines(stem, name, ver, host, rng=None):
    if stem == "requirements.txt":
        if host is None:
            return ["%s==%s" % (name, ver)]
        return ["%s @ https://%s/%s-%s.whl" % (name, host, name, ver)]
    if stem == "package-lock.json":
        return ['    "node_modules/%s": {' % name, '      "version": "%s",' % ver, '      "resolved": "%s"' % _tgz(host, name, ver), "    },"]
    if stem == "yarn.lock":
        return ["", "%s@^%s:" % (name, ver), '  version "%s"' % ver, '  resolved "%s"' % _tgz(host, name, ver)]
    if stem == "Cargo.lock":
        return ["", "[[package]]", 'name = "%s"' % name, 'version = "%s"' % ver, 'source = "registry+https://%s/index"' % host]
    if stem == "poetry.lock":
        return ["", "[[package]]", 'name = "%s"' % name, 'version = "%s"' % ver, "", "[package.source]", 'url = "https://%s/simple"' % host]
    if stem == "go.sum":
        return ["%s/%s v%s h1:%s" % (host, name, ver, "".join(rng.choice("0123456789abcdef") for _ in range(24)) if rng else "0" * 24)]
    raise ValueError(stem)


def lock_base(c, stem, omit=None):
    host = c.card["trusted_registries"][0]
    pins = [(n, v) for n, v in sorted(c.st.net.lockfile.items()) if n != omit]
    out = []
    if stem == "requirements.txt":
        return ["# pins"] + ["%s==%s" % (n, v) for n, v in pins]
    if stem == "package-lock.json":
        out = ["{", '  "name": "%s",' % c.names.get("ns.repo", "lk.repo"), '  "lockfileVersion": 3,', '  "packages": {']
        for i, (n, v) in enumerate(pins):
            ent = lock_entry_lines(stem, n, v, host)
            if i == len(pins) - 1:
                ent[-1] = "    }"
            out += ent
        return out + ["  }", "}"]
    for n, v in pins:
        out += lock_entry_lines(stem, n, v, host, c.rng)
    while out and out[0] == "":
        out = out[1:]
    return out


def lock_insert(stem, old_lines, entry_lines):
    """New content = old with the entry lines inserted where the format keeps a valid document."""
    old = list(old_lines)
    if stem == "package-lock.json":
        i = old.index('  "packages": {') + 1
        return old[:i] + entry_lines + old[i:]
    if stem == "requirements.txt":
        return old[:1] + entry_lines + old[1:] if old and old[0].startswith("#") else entry_lines + old
    return old + entry_lines


def lock_replace_version(stem, old_lines, name, old_ver, new_ver):
    return [l.replace(old_ver, new_ver) if (name in l or old_ver in l) else l for l in old_lines]


# ---- inserting induced command lines
def cmd_lines_for(cls, stem, texts):
    """The changed lines that carry the command texts in the file format of the class."""
    if cls == "ci_workflow":
        return [ci_line(t) for t in texts]
    if cls == "cron_systemd":
        if stem == "crontab":
            return ["*/10 * * * * %s" % t for t in texts]
        return ["ExecStart=%s" % texts[-1]]
    return list(texts)


def apply_cmd_lines(cls, stem, old_lines, new_lines_block, replace=False):
    """Insert the block where the class keeps a valid document; replace=True swaps the ExecStart line of a unit file."""
    old = list(old_lines)
    if cls == "ci_workflow":
        i = old.index("      - run: git status") + 1
        return old[:i] + new_lines_block + old[i:]
    if cls == "cron_systemd" and stem != "crontab":
        i = [k for k, l in enumerate(old) if l.startswith("ExecStart=")][0]
        return old[:i] + new_lines_block + old[i + 1:] if replace else old[:i] + new_lines_block + old[i:]
    if cls == "iac":
        return old + new_lines_block
    return old + new_lines_block


def comment_line(cls, stem, word):
    if cls == "ci_workflow":
        return "      # %s" % word
    if cls == "migration":
        return "-- %s" % word
    return "# %s" % word


def lock_set_version(stem, old_lines, name, old_ver, new_ver, host):
    """Entry of `name` rewritten to new_ver (every line of that entry that carries the version)."""
    out = []
    in_entry = False
    for l in old_lines:
        if stem == "requirements.txt":
            out.append(l.replace("%s==%s" % (name, old_ver), "%s==%s" % (name, new_ver)))
            continue
        if name in l:
            in_entry = True
        out.append(l.replace(old_ver, new_ver) if (in_entry and old_ver in l) else l)
        if in_entry and (l.strip() in ("", "},", "}") or l.startswith("[[package]]")):
            in_entry = False if l.strip() in ("", "},", "}") else in_entry
    return out


def validate_syntax(cls, path, lines):
    """K1 for config classes: YAML for CI, JSON for package-lock.json, TOML for Cargo.lock / poetry.lock. None = no parser applies."""
    stem = posixpath.basename(path)
    text = "\n".join(lines)
    try:
        if cls == "ci_workflow":
            yaml.safe_load(text)
            return True
        if cls == "lockfile" and stem == "package-lock.json":
            json.loads(text)
            return True
        if cls == "lockfile" and stem in ("Cargo.lock", "poetry.lock"):
            import tomllib
            tomllib.loads(text)
            return True
    except Exception:
        return False
    return None


# ---------------------------------------------------------------------------------------------------- parsers
_RUN = re.compile(r"^\s*-\s*run:")


def _shell_texts(cls, stem, lines):
    out = []
    for l in lines:
        s = l.strip()
        if s == "" or s.startswith("#") or s.startswith("["):
            continue
        if cls == "ci_workflow":
            if not _RUN.match(l):
                continue                                   # structure lines (jobs, runs-on ...) carry no command
            try:
                v = yaml.safe_load(s)
                out.append(v[0]["run"])
            except Exception:
                out.append(s)                              # unparsable step: let the expander report it
            continue
        if cls == "cron_systemd":
            if stem == "crontab":
                parts = s.split(None, 5)
                out.append(parts[5] if len(parts) == 6 else s)
            elif s.startswith("ExecStart="):
                out.append(s[len("ExecStart="):])
            continue
        if cls in ("git_hook", "later_run_script", "env_rc") and s.startswith("#!"):
            continue
        out.append(s)
    return out


_LOCK_NAME = {
    "requirements.txt": re.compile(r"^(?P<name>[A-Za-z0-9_.-]+)(?:==(?P<ver>[0-9][A-Za-z0-9_.+-]*)| @ https://(?P<host>[^/\s]+)/\S*-(?P<vurl>[0-9][A-Za-z0-9_.+]*)\.whl)\s*$"),
}


def _lock_entries(stem, lines):
    """-> list of dict(name, ver, host); entries are read from the changed lines only."""
    text = "\n".join(lines)
    ents = []
    if stem == "requirements.txt":
        for l in lines:
            s = l.strip()
            if not s or s.startswith("#"):
                continue
            m = _LOCK_NAME[stem].match(s)
            if m:
                ents.append({"name": m.group("name"), "ver": m.group("ver") or m.group("vurl"), "host": m.group("host")})
            else:
                ents.append({"name": s, "ver": None, "host": "?"})
        return ents
    if stem == "package-lock.json":
        for m in re.finditer(r'"node_modules/(?P<n>[^"]+)": \{\s*"version": "(?P<v>[^"]+)",\s*"resolved": "https://(?P<h>[^/"]+)/', text):
            ents.append({"name": m.group("n"), "ver": m.group("v"), "host": m.group("h")})
        return ents
    if stem == "yarn.lock":
        for m in re.finditer(r'(?P<n>[^@\s]+)@\^[^:]+:\s*version "(?P<v>[^"]+)"\s*resolved "https://(?P<h>[^/"]+)/', text):
            ents.append({"name": m.group("n"), "ver": m.group("v"), "host": m.group("h")})
        return ents
    if stem in ("Cargo.lock", "poetry.lock"):
        for m in re.finditer(r'name = "(?P<n>[^"]+)"\s*version = "(?P<v>[^"]+)"[\s\S]*?(?:source = "registry\+https://|url = "https://)(?P<h>[^/"]+)', text):
            ents.append({"name": m.group("n"), "ver": m.group("v"), "host": m.group("h")})
        return ents
    if stem == "go.sum":
        for l in lines:
            m = re.match(r"^(?P<h>[^/\s]+)/(?P<n>\S+) v(?P<v>\S+) h1:\S+$", l.strip())
            if m:
                ents.append({"name": m.group("n"), "ver": m.group("v"), "host": m.group("h")})
        return ents
    return ents


def parse_sql_lines(lines, db):
    stmts = []
    from LA_COMMON.validators import sql_info
    for l in lines:
        s = l.strip()
        if not s or s.startswith("--"):
            continue
        txt = s.rstrip(";")
        info = sql_info(txt)
        if info is None or info["kind"] is None or info["table"] is None:
            return None
        g = re.search(r"\bTO\s+([A-Za-z0-9_]+)\s*$", txt)
        stmts.append(SqlStmt(info["kind"], info["table"], db=db, has_predicate=info["has_predicate"], grantee=g.group(1) if g else "app_role"))
    return stmts


def _tf_blocks(lines):
    """-> list of (kind, name, ctx) resource blocks found in the lines."""
    out, cur = [], None
    for l in lines:
        m = re.match(r'^resource "([^"]+)" "([^"]+)" \{', l)
        if m:
            cur = [m.group(1), m.group(2), None]
        m = re.match(r'^\s+context = "([^"]+)"', l)
        if m and cur:
            cur[2] = m.group(1)
        if l.startswith("}") and cur:
            out.append(tuple(cur))
            cur = None
    return out


def induced_effects(cls, path, old_lines, new_lines, consumer, known_files=None):
    """The induced-effect set of the changed lines for a STATE-BEARING file (R23). Empty = R24."""
    from LA_COMMON.edits import hunk
    p, removed, added, s = hunk(old_lines, new_lines)
    stem = posixpath.basename(path)
    eff = []
    # ---- R16 scope: disabling a check (checked first; a disabling edit may also add lines)
    if cls == "ci_workflow":
        job = None
        for i, l in enumerate(new_lines):
            m = re.match(r"^  ([A-Za-z0-9_.-]+):\s*$", l)
            if m and not l.startswith("   "):
                job = m.group(1)
            if p <= i < p + len(added) and re.match(r"^\s+continue-on-error:\s*true\s*$", l) and job:
                eff.append({"kind": "check_disable", "check": job, "how": "continue_on_error", "target": "ci"})
        old_jobs = [m.group(1) for l in old_lines for m in [re.match(r"^  ([A-Za-z0-9_.-]+):\s*$", l)] if m]
        new_jobs = [m.group(1) for l in new_lines for m in [re.match(r"^  ([A-Za-z0-9_.-]+):\s*$", l)] if m]
        for j in old_jobs:
            if j not in new_jobs:
                eff.append({"kind": "check_disable", "check": j, "how": "remove_job", "target": "ci"})
    if cls == "git_hook":
        def body(lines):
            return [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
        ob, nb = body(old_lines), body(new_lines)
        if ob and (not nb or nb[0] == "exit 0"):
            eff.append({"kind": "check_disable", "check": stem, "how": "empty" if not nb else "exit0", "target": "hook"})
    # ---- added lines
    if cls in SHELL_CLASSES:
        texts = _shell_texts(cls, stem, added)
        if cls == "git_hook" and any(e["kind"] == "check_disable" for e in eff):
            texts = [t for t in texts if t != "exit 0"]
        if texts:
            scripts = [script_from_text(t, known_files) for t in texts]
            eff.append({"kind": "script", "scripts": scripts, "texts": texts})
        elif not eff:
            eff.append({"kind": "inert", "why": "comment_or_whitespace"})
    elif cls == "lockfile":
        ents = pkg_entries_changed(stem, old_lines, new_lines)
        rem = {e["name"]: e["ver"] for e in _lock_entries(stem, old_lines)}
        if ents:
            for e in ents:
                eff.append({"kind": "pkg", "name": e["name"], "ver": e["ver"], "host": e["host"], "stem": stem, "was": rem.get(e["name"])})
        elif added and not all(l.strip() == "" or l.strip().startswith("#") for l in added):
            eff.append({"kind": "script", "scripts": [RawScript("\n".join(added), "unknown_file", [])], "texts": added})
        else:
            eff.append({"kind": "inert", "why": "comment_or_whitespace"})
    elif cls == "migration":
        db = consumer.context
        stm = parse_sql_lines(added, db)
        if stm is None:
            eff.append({"kind": "script", "scripts": [RawScript("\n".join(added), "unknown_file", [])], "texts": added})
        elif stm:
            eff.append({"kind": "sql", "stmts": stm, "db": db})
        else:
            eff.append({"kind": "inert", "why": "comment_or_whitespace"})
    elif cls == "iac":
        a, r = _tf_blocks(added), _tf_blocks(removed)
        if a or r:
            ctx = (a or r)[0][2] or consumer.context
            if not ctx:                                  # Q11.4: no lane = the induced E6 effect does not resolve -> R19
                eff.append({"kind": "script", "scripts": [RawScript("\n".join(added + removed), "unknown_file", [])], "texts": added})
            else:
                eff.append({"kind": "iac", "op": "destroy" if (r and not a) else "apply", "ctx": ctx})
        elif [l for l in added if l.strip() and not l.strip().startswith("#")]:
            if not consumer.context:                     # Q11.4
                eff.append({"kind": "script", "scripts": [RawScript("\n".join(added), "unknown_file", [])], "texts": added})
            else:
                eff.append({"kind": "iac", "op": "apply", "ctx": consumer.context})      # an attribute change inside a block
        else:
            eff.append({"kind": "inert", "why": "comment_or_whitespace"})
    # an edit that changes nothing / only inert lines
    if eff and all(e["kind"] == "inert" for e in eff):
        return []
    return [e for e in eff if e["kind"] != "inert"]


def pkg_entries_changed(stem, old_lines, new_lines):
    """Entries present in the new content and not in the old one (added or changed), read from the FULL content."""
    old = {(e["name"], e["ver"], e["host"]) for e in _lock_entries(stem, old_lines)}
    return [e for e in _lock_entries(stem, new_lines) if (e["name"], e["ver"], e["host"]) not in old]


def pkg_same_pin(effect, lock):
    return effect["ver"] is not None and lock.get(effect["name"]) == effect["ver"] and effect.get("host") not in ("?",)
