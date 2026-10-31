"""Seeded random name generator with a per-side salt (C2.1 plan v3.1, skeptic 3/4; L-0 output (l)).

Every company, repo, host, service, bucket, tool, policy and runner identifier in a TRAINING row comes from
this generator with the TRAINING salt. No hand-picked fake names. The SEALED salt is supplied only on the
sealed side (environment variable OD_SEALED_SALT or the `salt` argument) and is never stored in this file.

Design
  name = f(HMAC-SHA256(key=salt, msg=JSON[side, seed, kind, key, attempt])) -> syllables / digits / hex.
  Deterministic: the same (side, salt, seed, kind, key) always gives the same name.
  The side string is part of the message (domain separation) and the salt is the key, so the two sides
  produce unrelated name streams even for equal seeds and keys.
  Hosts use RFC 2606 reserved TLDs (.example, .test, .invalid), so a generated host never resolves.
  A caller-supplied deny_check(name)->bool (the deny-list program) makes the generator redraw.
Only names are produced; no rows, no text.

Kinds added in v2 (L-0 task of 18 Oct, PREREG A77/A79): one kind for every slot the frozen names manifest
(NAMES_MANIFEST_V1.json, namespace.slot_to_kind) maps to null, named after the slot suffix ("ns.package" ->
"package"; "ns.noun.entity" -> "noun_entity"). The v1 kinds render exactly as before (a kind is part of the
HMAC message, so adding kinds moves no existing name). SLOT_TO_KIND is the slot -> kind table; kind_for_slot()
refuses an unknown slot. Rules that apply to the NEW kinds only:
  * the same deny_check hook as the old kinds (a hit redraws);
  * a built-in barred-name check on top of it: the whole name may not be one of RESERVED_NAMES (real env vars,
    remotes, branches, directories, SQL words), because a row that uses a real name teaches the real name;
  * a name containing a LABEL_LEAK_SUBSTRINGS word (prod, dev, test, secret, token, ask, allow, block ...) is redrawn,
    so no generated word gives the label away.
Rule that applies to ALL kinds: a name containing "ohs" or "sealed" (any case) is redrawn, so a generated name can
never turn a path into a barred one (the letters cannot occur in the syllable alphabet, but base32/hex bodies of
the composed ids could produce "ohs").
"""
import argparse
import hashlib
import hmac
import json
import os
import sys

TRAINING_SALT = "od-c21-training-namespace-salt-v1"
SEALED_ENV = "OD_SEALED_SALT"
MIN_SEALED_SALT_LEN = 16

_CONS = "bdfgklmnprstvz"
_VOW = "aeiou"
_CODA = "lnrst"
_TLDS = ("example", "test", "invalid")
_COMPANY_WORDS = ("Labs", "Systems", "Group", "Works", "Cloud", "Dynamics")   # generic words, not names
_SERVICE_WORDS = ("api", "svc", "worker", "gateway", "proxy", "queue")         # generic words, not names

KINDS_V1 = ("company", "repo", "host", "service", "bucket", "tool", "policy", "runner", "user")
NEW_KINDS = ("package", "path_stem", "branch", "envvar", "ticket", "project", "endpoint", "mcp_server", "context",
             "table", "database", "prefix", "object", "job_id", "brand", "remote_name", "noun_entity", "noun_field",
             "noun_module", "noun_symbol", "noun_path_segment", "variable", "event", "column", "category")
KINDS = KINDS_V1 + NEW_KINDS

# slot id (as in the frozen manifest, text after the first space dropped) -> kind. Mirrors namespace.slot_to_kind
# of NAMES_MANIFEST_V1 for the nine v1 slots and gives the 25 formerly-null slots their kind.
SLOT_TO_KIND = {
    "ns.org": "company", "ns.repo": "repo", "ns.package": "package", "ns.host": "host", "ns.registry_host": "host",
    "ns.service": "service", "ns.handle": "user", "ns.path_stem": "path_stem", "ns.branch": "branch",
    "ns.envvar": "envvar", "ns.ticket": "ticket", "ns.project": "project", "ns.endpoint": "endpoint",
    "ns.mcp_server": "mcp_server", "ns.mcp_tool": "tool", "ns.policy_card": "policy", "ns.context": "context",
    "ns.table": "table", "ns.database": "database", "ns.storage_bucket": "bucket", "ns.prefix": "prefix",
    "ns.object": "object", "ns.job_id": "job_id", "ns.brand": "brand", "ns.remote_name": "remote_name",
    "ns.noun.entity": "noun_entity", "ns.noun.field": "noun_field", "ns.noun.module": "noun_module",
    "ns.noun.symbol": "noun_symbol", "ns.noun.path_segment": "noun_path_segment", "ns.variable": "variable",
    "ns.event": "event", "ns.column": "column", "ns.category": "category",
}

# Whole-name matches refused for the NEW kinds (lower-case compare). Real identifiers a row must never present as
# a made-up one. Generic suffix words used inside the formats below (core, kit, lib, ...) are deliberately absent.
RESERVED_NAMES = frozenset("""
path home user users shell lang pwd term tmpdir editor pager hostname logname mail oldpwd display
origin upstream fork main master develop dev prod production stage staging test release hotfix
etc usr bin sbin var tmp opt root src lib proc sys boot mnt srv run dev home
data date time name id key value table index order group select insert update delete from where
default public private secret token password config env null true false none
node python java go ruby rust bash sh git npm pip
""".split())
_BARRED_SUBSTRINGS = ("ohs", "sealed")
# Substrings refused inside a NEW-kind name: environment / risk / label words that a syllable draw can spell by
# accident ("devil", "tokena", "baska"). A name carrying one would hand the model a shortcut to the label
# (prod vs dev, ask vs allow). Lower-case compare.
LABEL_LEAK_SUBSTRINGS = ("prod", "stag", "dev", "test", "live", "sandbox", "secret", "token", "passw", "admin", "root",
                         "cred", "priv", "tmp", "temp", "backup", "demo", "mock", "fake", "dummy", "sample", "real",
                         "safe", "danger", "delete", "drop", "kill", "sudo", "shadow", "main", "master", "base", "gold",
                         "label", "block", "allow", "deny", "ask", "stop", "halt")


def _message(side, seed, kind, key, attempt):
    """JSON array = injective encoding (a '|' inside seed/key cannot shift fields into each other)."""
    return json.dumps([side, str(seed), kind, str(key), attempt], ensure_ascii=True).encode("ascii")


class NamespaceError(ValueError):
    pass


class _Stream:
    """Deterministic byte stream from HMAC blocks."""

    def __init__(self, key, msg):
        self._key, self._msg, self._ctr, self._buf = key, msg, 0, b""

    def _more(self):
        self._buf += hmac.new(self._key, self._msg + b"|blk%d" % self._ctr, hashlib.sha256).digest()
        self._ctr += 1

    def below(self, n):
        while len(self._buf) < 4:
            self._more()
        v, self._buf = int.from_bytes(self._buf[:4], "big"), self._buf[4:]
        return v % n

    def pick(self, seq):
        return seq[self.below(len(seq))]


def _stem(st, syllables):
    out = []
    for i in range(syllables):
        s = st.pick(_CONS) + st.pick(_VOW)
        if st.below(3) == 0:
            s += st.pick(_CODA)
        out.append(s)
    return "".join(out)


def _hex(st, n):
    return "".join("0123456789abcdef"[st.below(16)] for _ in range(n))


def _digits(st, n):
    return "".join(str(st.below(10)) for _ in range(n))


_B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_CHARSETS = (("digits", "0123456789"), ("base32", _B32), ("hex", "0123456789abcdef"))
_SEPS = ("-", "_", "")
_PKG_WORDS = ("core", "kit", "lib", "sdk", "utils")        # generic words, not names
_PROJECT_WORDS = ("app", "core", "web", "data", "ops")      # generic words, not names


def _composed(st, upper):
    """Composed id (ns prefix, length 4-10, charset in {digits, base32, hex}, separator in {-, _, none}) =
    126 formats, each equally likely. Returns (prefix, sep, charset_name, length, body, rendered)."""
    prefix = _stem(st, 1 + st.below(2))
    sep = st.pick(_SEPS)
    cs_name, cs = st.pick(_CHARSETS)
    n = 4 + st.below(7)
    body = "".join(st.pick(cs) for _ in range(n))
    if upper:
        prefix, body = prefix.upper(), body.upper()
    else:
        body = body.lower()
    return prefix, sep, cs_name, n, body, prefix + sep + body


def _render(kind, st):
    if kind == "company":
        return _stem(st, 3).capitalize() + " " + st.pick(_COMPANY_WORDS)
    if kind == "repo":
        return _stem(st, 2) + "-" + _stem(st, 2)
    if kind == "host":
        return _stem(st, 2) + "-" + _digits(st, 2) + "." + _stem(st, 2) + "." + st.pick(_TLDS)
    if kind == "service":
        return _stem(st, 3) + "-" + st.pick(_SERVICE_WORDS)
    if kind == "bucket":
        return _stem(st, 2) + "-" + _stem(st, 2) + "-" + _hex(st, 4)
    if kind == "tool":
        return _stem(st, 2) + "_" + _stem(st, 2)
    if kind == "policy":
        return _stem(st, 2) + "_" + _stem(st, 3)
    if kind == "runner":
        return _stem(st, 3) + "-" + _digits(st, 2)
    if kind == "user":
        return _stem(st, 3)
    # ---- v2 kinds (the formerly-null manifest slots) ----
    if kind == "package":
        return _stem(st, 2) + "-" + _stem(st, 2) + "-" + st.pick(_PKG_WORDS)
    # The slots the family lanes fill with a bare word (noun.*, variable, event, column, category, table, path_stem)
    # render one lower-case 3-syllable stem, exactly the shape the lanes' stand-in ('user') had; the lane adds any
    # joining, casing or suffix itself.
    if kind == "path_stem":
        return _stem(st, 3)
    if kind == "branch":                       # a branch SUFFIX; the family adds any fixed prefix
        return _stem(st, 2) + "-" + _digits(st, 3)
    if kind == "envvar":                       # an env-var STEM, upper snake
        return (_stem(st, 2) + "_" + _stem(st, 2)).upper()
    if kind == "ticket":
        return _composed(st, True)[5]
    if kind == "project":
        return _stem(st, 3) + "-" + st.pick(_PROJECT_WORDS)
    if kind == "endpoint":
        return "/v%d/" % (1 + st.below(3)) + _stem(st, 3) + "/" + _stem(st, 2)
    if kind == "mcp_server":
        return _stem(st, 2) + "-" + _stem(st, 2) + "-mcp"
    if kind == "context":                      # cluster context / namespace; no env word (would leak a label)
        return _stem(st, 3) + "-" + _hex(st, 3)
    if kind == "table":
        return _stem(st, 3)
    if kind == "database":
        return _stem(st, 3) + "_db"
    if kind == "prefix":                       # object-store key prefix, trailing slash
        return _stem(st, 3) + "/" + _stem(st, 2) + "/"
    if kind == "object":                       # object key; no extension (a fixed extension can carry a meaning)
        return _stem(st, 2) + "-" + _hex(st, 6)
    if kind == "job_id":
        return _composed(st, False)[5]
    if kind == "brand":
        return _stem(st, 3).capitalize()
    if kind == "remote_name":
        return _stem(st, 2)
    if kind == "noun_entity":
        return _stem(st, 3)
    if kind == "noun_field":
        return _stem(st, 3)
    if kind == "noun_module":
        return _stem(st, 3)
    if kind == "noun_symbol":
        return _stem(st, 3)
    if kind == "noun_path_segment":
        return _stem(st, 3)
    if kind == "variable":
        return _stem(st, 3)
    if kind == "event":
        return _stem(st, 3)
    if kind == "column":
        return _stem(st, 3)
    if kind == "category":
        return _stem(st, 3)
    raise NamespaceError("unknown kind %r (known: %s)" % (kind, ", ".join(KINDS)))


def kind_for_slot(slot):
    """Namespace kind for a manifest slot id such as 'ns.noun.entity' (text after the first space is ignored)."""
    key = str(slot).split(" ", 1)[0]
    if key not in SLOT_TO_KIND:
        raise NamespaceError("unknown slot %r (known: %s)" % (slot, ", ".join(sorted(SLOT_TO_KIND))))
    return SLOT_TO_KIND[key]


def _barred(name, kind):
    """True when the built-in rules refuse this draw (applies on top of the caller's deny_check)."""
    low = name.lower()
    if any(b in low for b in _BARRED_SUBSTRINGS):
        return True
    if kind in NEW_KINDS:
        return low in RESERVED_NAMES or any(w in low for w in LABEL_LEAK_SUBSTRINGS)
    return False


class NameSpace:
    def __init__(self, side, seed, salt=None, deny_check=None):
        if side not in ("training", "sealed"):
            raise NamespaceError("side must be 'training' or 'sealed'")
        if side == "training":
            if salt is not None and salt != TRAINING_SALT:
                raise NamespaceError("a training namespace uses only the built-in training salt")
            salt = TRAINING_SALT
        else:
            if salt is None:
                salt = os.environ.get(SEALED_ENV)
            if not salt:
                raise NamespaceError("sealed side: the salt must be supplied (argument or %s)" % SEALED_ENV)
            if salt == TRAINING_SALT:
                raise NamespaceError("the sealed salt must differ from the training salt")
            if len(salt) < MIN_SEALED_SALT_LEN:
                raise NamespaceError("sealed salt shorter than %d characters" % MIN_SEALED_SALT_LEN)
        self.side = side
        self.seed = str(seed)
        self._salt = salt.encode("utf-8")
        self._deny = deny_check
        self._issued = {}

    def fingerprint(self):
        """Short public id of (side, salt); does not reveal the salt."""
        return hmac.new(self._salt, b"fingerprint|" + self.side.encode(), hashlib.sha256).hexdigest()[:12]

    def name(self, kind, key, max_tries=64):
        """Pure function of (side, salt, seed, kind, key); redraws only on a deny hit."""
        if kind not in KINDS:
            raise NamespaceError("unknown kind %r (known: %s)" % (kind, ", ".join(KINDS)))
        for attempt in range(max_tries):
            msg = _message(self.side, self.seed, kind, key, attempt)
            nm = _render(kind, _Stream(self._salt, msg))
            if _barred(nm, kind):
                continue
            if self._deny is None or not self._deny(nm):
                return nm
        raise NamespaceError("deny_check rejected %d draws for %s/%s" % (max_tries, kind, key))

    def unique(self, kind, key):
        """Stateful variant: a different key never returns a name already issued in this namespace."""
        seen = self._issued.setdefault(kind, {})
        if key in seen:
            return seen[key]
        used = set(seen.values())
        for bump in range(256):
            nm = self.name(kind, key if bump == 0 else "%s#%d" % (key, bump))
            if nm not in used:
                seen[key] = nm
                return nm
        raise NamespaceError("could not draw a unique %s name" % kind)

    def catalogue(self, kind, n, tag="cat"):
        """n distinct names for a names-only manifest (stable for the same tag)."""
        return [self.unique(kind, "%s-%d" % (tag, i)) for i in range(n)]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Print generated names (names only).")
    ap.add_argument("--side", choices=("training", "sealed"), default="training")
    ap.add_argument("--seed", required=True)
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--tag", default="cat")
    a = ap.parse_args(argv)
    try:
        ns = NameSpace(a.side, a.seed)          # sealed salt only from the environment, never argv
    except NamespaceError as e:
        print("namespace: %s" % e, file=sys.stderr)
        return 2
    print("# side=%s fingerprint=%s" % (ns.side, ns.fingerprint()))
    for nm in ns.catalogue(a.kind, a.count, a.tag):
        print(nm)
    return 0


if __name__ == "__main__":
    sys.exit(main())
