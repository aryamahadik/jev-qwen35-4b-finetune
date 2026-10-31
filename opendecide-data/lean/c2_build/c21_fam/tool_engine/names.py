"""Names for L-T generators: frozen allow-list check and the namespace-backed noun source.

Two separate things (see NAMES_MANIFEST_V1.json id_scheme.display_vs_id_rule):
  * IDS (card.*, verb.*, param.*, carrier ids, canonical language names, runner ids) are checked against the frozen
    allow-list, per family. `AllowList.check_names` refuses any id that is not listed for that family.
  * DISPLAY names (entity nouns, field nouns, policy-card titles, module/symbol/path nouns) are drawn from
    c21_infra/namespace.py with the TRAINING salt. Nothing is hand-picked. namespace.py v1 has no `noun_*` kinds
    (the manifest maps ns.noun.* to null until L-0 adds them), so `NameSource` fails closed: it raises unless
    `standin=True`, which maps every noun slot onto the existing 'user' kind (still a namespace.py output with the
    training salt, three-syllable stem). Stand-in mode is for unit tests and the 20-example dry run ONLY;
    `assert_production_ready()` is what a row job must call and it refuses stand-in names.
"""
import importlib.util
import json
import os

from . import util

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))          # .../opendecide-data/lean
C2_BUILD = os.path.join(LEAN, "c2_build")
INFRA_DIR = os.path.join(C2_BUILD, "c21_infra")
MANIFEST_DEFAULT = os.path.join(C2_BUILD, "zed_orch", "c21", "l0", "NAMES_MANIFEST_V1.json")
MANIFEST_SHA_FILE = os.path.join(C2_BUILD, "zed_orch", "c21", "l0", "NAMES_MANIFEST_V1.sha256")

CATEGORIES = ("policy", "tool", "language", "runner", "carrier")


class NameGuardError(ValueError):
    pass


def _load_namespace_module():
    spec = importlib.util.spec_from_file_location("od_c21_namespace", os.path.join(INFRA_DIR, "namespace.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ns_mod = _load_namespace_module()
NamespaceError = ns_mod.NamespaceError


class AllowList:
    """The frozen names-only allow-list (NAMES_MANIFEST_V1.json)."""

    def __init__(self, data, file_sha):
        if data.get("frozen") is not True:
            raise NameGuardError("allow-list is not frozen")
        self.data = data
        self.file_sha = file_sha
        self.union = {c: set(data["names"][c]) for c in CATEGORIES}
        self.per_family = {f: {c: set(v.get(c, [])) for c in CATEGORIES} for f, v in data["per_family_names"].items()}

    @classmethod
    def load(cls, path=MANIFEST_DEFAULT, expect_sha=None, sha_file=MANIFEST_SHA_FILE):
        with open(path, "rb") as f:
            raw = f.read()
        import hashlib
        file_sha = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw.decode("utf-8"))
        pinned = expect_sha
        if pinned is None and os.path.isfile(sha_file) and os.path.abspath(path) == os.path.abspath(MANIFEST_DEFAULT):
            with open(sha_file, "r", encoding="utf-8") as f:
                pinned = f.read().split()[0]
        if pinned is not None and pinned != file_sha:
            raise NameGuardError("allow-list sha %s does not match the pinned sha %s" % (file_sha, pinned))
        block = json.dumps(data["names"], sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
        if hashlib.sha256(block).hexdigest() != data.get("names_block_sha256"):
            raise NameGuardError("names block sha does not match names_block_sha256")
        return cls(data, file_sha)

    def family_names(self, family):
        if family not in self.per_family:
            raise NameGuardError("family %r is not in the allow-list" % family)
        return self.per_family[family]

    def check_names(self, family, names):
        """names: {category: iterable of ids}. Returns the list of (category, id) NOT allowed for the family
        (and not in the union). Empty list = pass. Unknown categories are violations."""
        fam = self.family_names(family)
        bad = []
        for cat, ids in names.items():
            if cat not in CATEGORIES:
                bad.extend((cat, i) for i in ids)
                continue
            for i in ids:
                if i not in fam[cat] or i not in self.union[cat]:
                    bad.append((cat, i))
        return bad

    def assert_names(self, family, names):
        bad = self.check_names(family, names)
        if bad:
            raise NameGuardError("names off the frozen allow-list for %s: %s" % (family, bad[:10]))


# slot kind -> namespace.py kind it needs in production
NOUN_KINDS = ("noun_entity", "noun_field", "noun_module", "noun_symbol", "noun_path_segment")
STANDIN_KIND = "user"          # an existing namespace.py kind: a three-syllable stem
BUCKETS = {"T54": "bucket.t54", "T55": "bucket.t55", "T56": "bucket.t56"}
MAX_NOUN_REUSE = 3


class NameSource:
    """Display names for one family from namespace.py (TRAINING salt). Per-family hash bucket = the namespace
    seed, so two families can never share a stream. Each noun may be used in at most 3 scenarios."""

    def __init__(self, family, seed="v1", standin=False, deny_check=None, reserved=()):
        if family not in BUCKETS:
            raise NameGuardError("unknown family %r" % family)
        self.family = family
        self.bucket = BUCKETS[family]
        self.standin = standin
        self.ns = ns_mod.NameSpace("training", "%s|%s" % (self.bucket, seed), deny_check=deny_check)
        self.reserved = set(reserved)
        self._noun_cache = {}
        self._issued_names = set()
        self._uses = {}                      # noun -> number of scenarios that used it
        self._scenario_nouns = {}            # scenario key -> set of nouns
        self._drawn = {}                     # (slot kind, scenario key) -> the nouns drawn (idempotent per scenario)

    # -- kinds ----------------------------------------------------------------------------------
    def kind_for(self, slot_kind):
        if slot_kind not in NOUN_KINDS:
            raise NameGuardError("unknown noun slot %r" % slot_kind)
        if slot_kind in ns_mod.KINDS:
            return slot_kind
        if self.standin:
            return STANDIN_KIND
        raise NamespaceError("namespace.py has no kind %r yet (manifest slot is null); row jobs must wait for L-0 "
                             "to add it; stand-in is for tests and the dry run only" % slot_kind)

    @property
    def is_production_ready(self):
        return all(k in ns_mod.KINDS for k in NOUN_KINDS)

    def assert_production_ready(self):
        if self.standin or not self.is_production_ready:
            raise NamespaceError("not production ready: stand-in nouns or missing namespace.py kinds")

    # -- nouns ----------------------------------------------------------------------------------
    def noun(self, slot_kind, index):
        """The index-th noun of a slot kind in this family's bucket (stable)."""
        k = (slot_kind, index)
        if k not in self._noun_cache:
            kind = self.kind_for(slot_kind)
            for bump in range(64):
                nm = self.ns.name(kind, "%s#%d#%d" % (slot_kind, index, bump))
                if nm not in self.reserved and nm not in self._issued_names:
                    break
            else:
                raise NamespaceError("could not draw a distinct noun")
            self._noun_cache[k] = nm
            self._issued_names.add(nm)
        return self._noun_cache[k]

    def draw_nouns(self, slot_kind, n, scenario_key, rng, pool_size=60000):
        """n distinct nouns for one scenario; each noun is used by at most MAX_NOUN_REUSE scenarios. Idempotent per
        (slot kind, scenario key, n): a second call for the same scenario (a matched twin, a retry) returns the same nouns
        and does not count as another use."""
        ck = (slot_kind, scenario_key, n)
        if ck in self._drawn:
            return list(self._drawn[ck])
        got = []
        tries = 0
        # selection uses its OWN stream keyed by (family seed, slot kind, scenario key): the caller's rng is never
        # consumed, so a matched twin or a retry sees exactly the same draws as the first build
        own = util.rng_for(self.ns.seed, "draw", slot_kind, scenario_key, n)
        while len(got) < n:
            tries += 1
            if tries > 10000:
                raise NamespaceError("noun pool exhausted")
            idx = own.randrange(pool_size)
            nm = self.noun(slot_kind, idx)
            if nm in got or self._uses.get(nm, 0) >= MAX_NOUN_REUSE:
                continue
            got.append(nm)
        for nm in got:
            self._uses[nm] = self._uses.get(nm, 0) + 1
        self._scenario_nouns[scenario_key] = set(got)
        self._drawn[ck] = list(got)
        return list(got)

    def card_title(self, card_id):
        """Display title of a policy card (ns.policy_card -> 'policy' kind), never hand-picked."""
        return self.ns.name("policy", "title|" + card_id)

    def fingerprint(self):
        return self.ns.fingerprint()


def assert_buckets_disjoint(sources):
    """P-13 helper: no noun appears in two different families' streams."""
    seen = {}
    for src in sources:
        for nm in src._noun_cache.values():
            if nm in seen and seen[nm] != src.family:
                raise NameGuardError("noun %r appears in %s and %s" % (nm, seen[nm], src.family))
            seen[nm] = src.family
    return True


def job_manifest(family, records, job_id=None):
    """A row-start-guard job manifest (names only) for a batch of records: the union of the ids the rows use, per category,
    plus the per-row name sets. Every category is declared (an empty list is allowed), as the guard requires."""
    union = {c: set() for c in CATEGORIES}
    rows = []
    for r in records:
        for c in CATEGORIES:
            union[c].update(r["names"].get(c, []))
        rows.append({"row_id": r["row_id"], "names": {c: sorted(r["names"].get(c, [])) for c in CATEGORIES}})
    return {"job_id": job_id or "%s-names" % family.lower(), "names": {c: sorted(v) for c, v in union.items()}, "rows": rows}
