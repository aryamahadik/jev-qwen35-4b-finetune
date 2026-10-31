"""Builder context for T50 intents: the simulated environment of ONE spec family plus helpers that add the state
a rule needs AND the visible evidence for it (history calls, user-turn notes). Every NAME comes from the training
namespace through LA_COMMON.names.Names; fixed words (main, origin, .env, credentials, pre-commit ...) are the
manifest's generic words.
"""
import posixpath

from LA_COMMON.canon import rng_for
from LA_COMMON.names import Names
from LA_COMMON.shellmodel import Cmd, Glob, Redir, Script
from LA_COMMON.spec import HistCall
from LA_COMMON.state import (FsNode, GitRemote, InfraResource, SimState, SqlDb, SqlTable)

from . import cards as cards_mod

SECRET_KINDS = ("env", "creds", "key", "token")


class BCtx:
    def __init__(self, group, card_id, seed_tag="b", provisional=True):
        self.group = group
        self.names = Names(group, provisional=provisional)
        self.rng = rng_for("t50", group, seed_tag)
        self.card = cards_mod.make_card(card_id, self.names)
        self.st = SimState()
        self.hist = []
        self.payloads = {}
        self.shown = {}                          # fact id -> how it is visible
        self.naming = {"ops": [], "targets": [], "named_paths": []}
        self.user_notes = []                     # (form, slots) extra user turns that show facts
        self.meta = {"languages": ["bash"], "operators_ok": True}
        self.egress = None
        self.payload_kind = None
        self.k = 0
        self._base()

    # ---------------------------------------------------------------------------------- names / paths
    def nm(self, slot, key):
        return self.names.get(slot, key)

    def seg(self, key):
        return self.names.get("ns.noun.path_segment", "seg." + key)

    @property
    def root(self):
        return self.card["workspace_root"]

    def p(self, key, ext=".txt", sub=None):
        base = self.root if sub is None else posixpath.join(self.root, sub)
        return posixpath.join(base, self.seg(key) + ext)

    def uniq(self, tag):
        self.k += 1
        return "%s.%d" % (tag, self.k)

    # ---------------------------------------------------------------------------------- base environment
    def _base(self):
        st, card = self.st, self.card
        st.add(FsNode(self.root, "dir", tracked=True))
        st.add(FsNode(posixpath.join(self.root, "src"), "dir", tracked=True))
        st.add(FsNode(card["allowed_roots"][1], "dir"))
        for i in range(3):
            st.add(FsNode(self.p("base%d" % i, ".txt", "src"), "file", tracked=True, dirty=False))
        g = st.git
        g.branch = "feature/" + self.names.slug("ns.branch", "cur")
        g.own_branches = [g.branch]
        g.protected = []                         # protected branches live in the CARD (swap members must share the state)
        vis = "public" if self.rng.random() < 0.3 else "private"
        g.remotes = {"origin": GitRemote("origin", card["trusted_remotes"]["origin"], vis, True),
                     "upstream": GitRemote("upstream", card["trusted_remotes"]["upstream"], "private", True)}
        g.hooks = ["pre-commit", "pre-push", "commit-msg"]
        g.last_hook_result = "ok"
        n = st.net
        n.trusted_hosts = list(card["trusted_hosts"])
        n.trusted_registries = list(card["trusted_registries"])
        n.default_registry = card["trusted_registries"][0]
        n.gist_host = self.names.get("ns.host", "gist")
        for i in range(3):
            n.lockfile[self.names.get("ns.package", "lock%d" % i)] = "%d.%d.%d" % (1 + i, self.rng.randrange(0, 9), self.rng.randrange(0, 9))
        for lane in ("contained", "shared", "production"):
            for c in card["context_lists"][lane]:
                st.infra.contexts[c] = lane
        for lane, dbs in card["database_lists"].items():
            for d in dbs:
                st.sql.dbs[d] = SqlDb(d, lane, {})
        homes = self.names.get("ns.handle", "other.home")
        st.other_homes = ["/home/" + homes]
        st.env.vars = {self.names.envvar("env0"): False, self.names.envvar("env1") + "_TOKEN": True}

    # ---------------------------------------------------------------------------------- files
    def show_call(self, script, fact, author="agent", approved=False, how="history_call", output=""):
        self.hist.append(HistCall(author=author, carrier="shell_exec", script=script, approved_by_user=approved, shows=[fact], output=output))
        self.shown[fact] = how

    def file(self, kind, key, ext=".txt", sub=None, show=True, path=None, **kw):
        """kinds: agent | clean | dirty | untracked | backup_dirty | outside | system | secret | conf | public."""
        path = path or self.p(key, ext, sub)
        f = {}
        if kind == "agent":
            f = dict(tracked=False, dirty=False, created_by_agent=True)
        elif kind == "clean":
            f = dict(tracked=True, dirty=False)
        elif kind == "dirty":
            f = dict(tracked=True, dirty=True)
        elif kind == "untracked":
            f = dict(tracked=False, dirty=False)
        elif kind == "backup_dirty":
            f = dict(tracked=True, dirty=True, backup=True)
        elif kind == "outside":
            f = dict(tracked=False)
        elif kind == "system":
            f = dict(system_path=True)
        elif kind == "secret":
            f = dict(tracked=False, data_class="secret")
        elif kind == "conf":
            f = dict(tracked=True, dirty=False, data_class="confidential")
        elif kind == "public":
            f = dict(tracked=True, dirty=False)
        f.update(kw)
        n = FsNode(path, "file", **f)
        self.st.add(n)
        if show:
            self._evidence(n, kind)
        return n.path

    def _evidence(self, n, kind):
        path = n.path
        if kind == "agent":
            self.show_call(Script.of(Cmd("touch", args=[path])), "fs.created_by_agent:" + path)
            self.shown["fs.tracked:" + path] = "history_call"
            self.shown["fs.dirty:" + path] = "history_call"
        elif kind in ("dirty", "backup_dirty"):
            self.show_call(Script.of(Cmd("tee", flags=[["-a"]], args=[path])), "fs.dirty:" + path)
            self.shown["fs.tracked:" + path] = "history_call"
            self.shown["fs.created_by_agent:" + path] = "history_call"
            if kind == "backup_dirty":
                self.show_call(Script.of(Cmd("cp", args=[path, path + ".bak"])), "fs.backup:" + path)
        elif kind in ("clean", "untracked", "public", "conf"):
            how = "user_turn"
            self.shown["fs.tracked:" + path] = how
            self.shown["fs.dirty:" + path] = how
            self.shown["fs.created_by_agent:" + path] = how
            self.user_notes.append(("T50.U.note_file_state", {"path": path, "state": kind}))
        elif kind == "secret":
            self.shown["fs.data_class:" + path] = "path"
            for f in ("fs.tracked:", "fs.dirty:", "fs.created_by_agent:"):
                self.shown[f + path] = "path"
        elif kind in ("outside", "system"):
            for f in ("fs.tracked:", "fs.dirty:", "fs.created_by_agent:"):
                self.shown[f + path] = "path"

    def secret_path(self, key, outside=False):
        """A credential-store node whose conventional stem makes the class visible (.env, credentials, id_*)."""
        stem = self.rng.choice(["env", "creds", "key", "token"])
        if stem == "env":
            path = posixpath.join(self.root, ".env")
        elif stem == "creds":
            d = "." + self.names.get("ns.path_stem", "cred.dir")
            path = posixpath.join("/home/" + self.names.get("ns.handle", "me"), d, "credentials")
        elif stem == "key":
            path = posixpath.join("/home/" + self.names.get("ns.handle", "me"), ".ssh", "id_" + self.names.get("ns.path_stem", "idk"))
        else:
            path = posixpath.join(self.root, self.names.get("ns.path_stem", "tk." + key) + "_token")
        return self.file("secret", key, path=path)

    def conf_path(self, key):
        return self.file("conf", key, ".csv", "data")

    # ---------------------------------------------------------------------------------- infra
    def resource(self, lane, kind="deployment", creator="other", key="r", name=None):
        ctxs = self.card["context_lists"][lane]
        ctx = ctxs[0] if lane != "contained" else ctxs[self.rng.randrange(len(ctxs))]
        name = name or self.names.get("ns.service", "res." + key)
        if creator == "agent" and lane != "contained":
            raise ValueError("agent-created resource outside the contained lane")
        self.st.infra.resources.append(InfraResource(ctx, kind, name, creator))
        if creator == "agent":
            self.show_call(Script.of(Cmd("kubectl", sub="create", flags=[["--context", ctx]], args=[kind, name])),
                           "infra.creator:%s/%s/%s" % (ctx, kind, name))
        else:
            self.shown["infra.creator:%s/%s/%s" % (ctx, kind, name)] = "user_turn"
            self.user_notes.append(("T50.U.note_resource_owner", {"resource": name, "ctx": ctx, "owner": "other"}))
        return ctx, kind, name

    # ---------------------------------------------------------------------------------- sql
    def table(self, lane, backup=False, key="t"):
        dbs = self.card["database_lists"][lane]
        db = dbs[0]
        t = self.names.get("ns.table", "tbl." + key)
        self.st.sql.dbs[db].tables[t] = SqlTable(t, backup, "small")
        if backup:
            self.show_call(Script.of(Cmd("psql", flags=[["-c", "@SQL"], ["-d", db]],
                                         sql=_ctas(t, self.names))), "sql.backup:%s.%s" % (db, t))
        else:
            self.shown["sql.backup:%s.%s" % (db, t)] = "output"
        return db, t

    # ---------------------------------------------------------------------------------- naming
    def want_naming(self, op_ref, target_ref):
        """Record the default full naming (used by consent twins / named variants)."""
        if op_ref not in self.naming["ops"]:
            self.naming["ops"].append(op_ref)
        if target_ref not in self.naming["targets"]:
            self.naming["targets"].append(target_ref)


def _ctas(t, names):
    from LA_COMMON.shellmodel import SqlStmt
    return SqlStmt("ctas", t, has_predicate=False, column=names.get("ns.column", "bak"))


class Built:
    """What an intent returns."""

    def __init__(self, c, script, intent, payload_kind=None, egress=None, extra_programs=()):
        self.c = c
        self.script = script
        self.intent = intent
        self.payload_kind = payload_kind
        self.egress = egress
        self.extra_programs = set(extra_programs)
