"""Names for lane L-K.

  * IDS (card.*, defs_card.*, verb.*, param.*, prog.*, carrier.*) are checked against the FROZEN allow-list, manifest v1.2
    (NAMES_MANIFEST_V1_2.json, pinned by its .sha256 file), per family. `load_allowlist()` returns a tool_engine AllowList.
  * DISPLAY names (entity / field / unit nouns, policy-card titles, paths, handles, tickets, contexts) are drawn from
    c21_infra/namespace.py with the TRAINING salt, per-family hash bucket bucket.t59 / bucket.t60. Nothing is hand-picked.
    namespace.py now has the noun kinds, so production mode works; `standin=True` (tests / dry run) is kept for the case that a
    future namespace.py drops a kind.
"""
import hashlib

from . import MANIFEST_V12, MANIFEST_V12_SHA
from tool_engine import names as tn

BUCKETS = {"T59": "bucket.t59", "T60": "bucket.t60"}


def load_allowlist(path=MANIFEST_V12, sha_file=MANIFEST_V12_SHA):
    """The v1.2 allow-list, verified against its pinned file sha and against names_block_sha256."""
    with open(sha_file, "r", encoding="utf-8") as f:
        pinned = f.read().split()[0]
    return tn.AllowList.load(path, expect_sha=pinned)


def allowlist_file_sha(path=MANIFEST_V12):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class KNameSource(tn.NameSource):
    """tn.NameSource for the L-K families (the L-T class refuses families outside its BUCKETS table, which is not ours to edit)."""

    def __init__(self, family, seed="v1", standin=False, deny_check=None, reserved=()):
        if family not in BUCKETS:
            raise tn.NameGuardError("unknown L-K family %r" % family)
        self.family = family
        self.bucket = BUCKETS[family]
        self.standin = standin
        self.ns = tn.ns_mod.NameSpace("training", "%s|%s" % (self.bucket, seed), deny_check=deny_check)
        self.reserved = set(reserved)
        self._noun_cache = {}
        self._issued_names = set()
        self._uses = {}
        self._scenario_nouns = {}
        self._drawn = {}
        self._other = {}

    def other(self, kind, key):
        """A display name of a non-noun namespace kind (handle='user', path_stem, ticket, job_id, context, service, host ...),
        stable per (kind, key) and distinct from every other name issued by this source."""
        k = (kind, key)
        if k not in self._other:
            kd = kind
            if kd not in tn.ns_mod.KINDS:
                if not self.standin:
                    raise tn.NamespaceError("namespace.py has no kind %r" % kind)
                kd = tn.STANDIN_KIND
            nm = self.ns.unique(kd, "%s|%s" % (kind, key))
            self._other[k] = nm
            self._issued_names.add(nm)
        return self._other[k]

    @property
    def is_production_ready(self):
        return all(k in tn.ns_mod.KINDS for k in tn.NOUN_KINDS) and all(
            k in tn.ns_mod.KINDS for k in ("path_stem", "ticket", "job_id", "context", "service", "user"))
