"""Name source for L-A: every display name comes from namespace.py with the TRAINING salt (v3.1 skeptic 3);
every policy / tool / language / runner / carrier ID must be on the frozen allow-list NAMES_MANIFEST_V1.

Two separate things (manifest id_scheme.display_vs_id_rule):
  * DISPLAY names (repo, host, user, branch suffix, table ...) -> Names.get(slot, key), from namespace.py.
  * IDs (prog.git, carrier.shell_exec, card.t50.c01, language bash ...) -> AllowList.check(...), refused if off-list.

Null-kind slots. The manifest maps some slots (ns.package, ns.branch, ns.path_stem, ...) to NO namespace.py
kind yet, and says no row job may fill them until L-0 adds the kind. Names(provisional=False) therefore RAISES
NameSlotUnavailable for those slots. Names(provisional=True) (unit tests and the 20-example dry run ONLY) maps
them onto existing namespace.py kinds with a slot-qualified key, marks the result `provisional`, and
assert_row_ready() refuses any spec that used a provisional name. This is open item OI-1 in the report.
"""
import json
import os

from . import MANIFEST_PATH, MANIFEST_SHA_PATH
from .canon import sha_file

import namespace as _ns  # c21_infra/namespace.py (put on sys.path by LA_COMMON/__init__)

CATEGORIES = ("policy", "tool", "language", "runner", "carrier")
FAMILIES = ("T50", "T51", "T53")

# Provisional (tests / dry run only) aliases for slots whose own kind does not exist yet.
PROVISIONAL_KIND = {
    "ns.package": "repo", "ns.path_stem": "user", "ns.branch": "repo", "ns.envvar": "user", "ns.ticket": "user",
    "ns.project": "repo", "ns.endpoint": "service", "ns.mcp_server": "service", "ns.mcp_tool": "tool",
    "ns.context": "service", "ns.table": "user", "ns.database": "repo", "ns.prefix": "user", "ns.object": "user",
    "ns.job_id": "user", "ns.brand": "company", "ns.remote_name": "user", "ns.column": "user",
    "ns.noun.entity": "user", "ns.noun.field": "user", "ns.noun.path_segment": "user",
    "ns.variable": "user", "ns.event": "user", "ns.category": "user", "ns.noun.module": "user",
    "ns.noun.symbol": "user",
    # v3.2 addendum section 13 slots (manifest v1.1 namespace_slot_kinds_added): namespace.py has NO kind for them yet, so
    # no row job may fill them (NameSlotUnavailable under provisional=False); dry runs and tests alias them here.
    "ns.ci_job": "service", "ns.hook_script": "service", "ns.migration_id": "user", "ns.cron_job": "service",
    "ns.systemd_unit": "service", "ns.iac_resource": "service", "ns.lockfile_package": "repo", "ns.alias_dir": "repo",
    "ns.consumer_path_component": "user", "ns.crontab_entry": "service", "ns.manifest_object": "service",
    "ns.lifecycle_rule": "service",
}
# Slots with a real namespace.py kind today (manifest namespace.namespace_py.slot_to_kind).
DIRECT_KIND = {
    "ns.org": "company", "ns.repo": "repo", "ns.host": "host", "ns.registry_host": "host", "ns.service": "service",
    "ns.handle": "user", "ns.policy_card": "policy", "ns.storage_bucket": "bucket", "ns.mcp_tool": "tool",
}


class NameSlotUnavailable(Exception):
    pass


class AllowListError(Exception):
    pass


class AllowList:
    """The frozen names-only allow-list. Loads the manifest, verifies its whole-file sha against
    NAMES_MANIFEST_V1.sha256 (the value the row-start guard pins) and exposes per-family lists."""

    def __init__(self, path=MANIFEST_PATH, sha_path=MANIFEST_SHA_PATH):
        self.path = path
        with open(path, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
        self.file_sha = sha_file(path)
        with open(sha_path, "r", encoding="utf-8") as f:
            pinned = f.read().split()[0].strip().lower()
        if pinned != self.file_sha:
            raise AllowListError("allow-list file sha %s != pinned %s" % (self.file_sha[:12], pinned[:12]))
        if self.manifest.get("frozen") is not True:
            raise AllowListError("allow-list is not frozen")
        self.names = {c: frozenset(self.manifest["names"][c]) for c in CATEGORIES}
        self.per_family = {f: {c: frozenset(self.manifest["per_family_names"][f][c]) for c in CATEGORIES}
                           for f in FAMILIES}
        self.families_allowed = tuple(self.manifest["row_job_families_allowed"])
        self.training_fingerprint = self.manifest["namespace"]["namespace_py"]["training_fingerprint"]

    def check(self, family, used):
        """used: {category: iterable of ids}. Returns a list of violations (empty = ok). Stricter than the
        guard: ids must be on THIS FAMILY's list, not merely on the union."""
        bad = []
        if family not in self.families_allowed:
            bad.append("FAMILY_NOT_ALLOWED: %s" % family)
            return bad
        fam = self.per_family.get(family)
        if fam is None:
            return ["FAMILY_NOT_BUILT_BY_LA: %s" % family]
        for cat in CATEGORIES:
            for nm in sorted(set(used.get(cat, ()))):
                if nm not in self.names[cat]:
                    bad.append("OFF_ALLOWLIST: %s=%r" % (cat, nm))
                elif nm not in fam[cat]:
                    bad.append("OFF_FAMILY_LIST: %s=%r not in %s's list" % (cat, nm, family))
        for cat in used:
            if cat not in CATEGORIES:
                bad.append("UNKNOWN_CATEGORY: %r" % cat)
        return bad

    def require(self, family, used):
        bad = self.check(family, used)
        if bad:
            raise AllowListError("; ".join(bad[:10]))

    def programs(self, family):
        return frozenset(n[len("prog."):] for n in self.per_family[family]["tool"] if n.startswith("prog."))

    def policy_ids(self, family):
        return sorted(self.per_family[family]["policy"])


_ALLOW_CACHE = {}
ROW_MODE = {"on": False}


def set_row_mode(flag):
    """Row jobs call set_row_mode(True): any Names(provisional=True) then raises, so a spec can never be built from a
    provisional alias (open item OI-1: slots without a namespace.py kind)."""
    ROW_MODE["on"] = bool(flag)


def get_allowlist():
    if "al" not in _ALLOW_CACHE:
        _ALLOW_CACHE["al"] = AllowList()
    return _ALLOW_CACHE["al"]


class Names:
    """Per-spec name source. seed = the spec family id, so every rendering of a spec shares its names."""

    def __init__(self, seed, provisional=False, deny_check=None):
        if provisional and ROW_MODE["on"]:
            raise NameSlotUnavailable("row mode is on: provisional names are not allowed (OI-1)")
        # deny_check = the deny-list program hook (manifest: every kind redraws on a hit); None only in tests / dry runs
        self.ns = _ns.NameSpace("training", seed, deny_check=deny_check)
        if self.ns.fingerprint() != get_allowlist().training_fingerprint:
            raise AllowListError("namespace training fingerprint does not match the manifest")
        self.provisional = provisional
        self.used_provisional = False
        self.issued = []

    def kind_for(self, slot):
        if slot in DIRECT_KIND:
            return DIRECT_KIND[slot], False
        # L-0 namespace v2 closed OI-1: the real kind for a manifest slot is namespace.SLOT_TO_KIND (authoritative table,
        # includes ns.noun.path_segment -> noun_path_segment). Only a slot the manifest lists can resolve; a name that
        # merely equals some kind (ns.user, ns.company ...) is NOT a manifest slot and is refused (A64 skeptic T50/51/53).
        real = _ns.SLOT_TO_KIND.get(slot)
        if real is not None and real in _ns.KINDS:
            return real, False
        if not self.provisional:
            raise NameSlotUnavailable("slot %s has no namespace.py kind yet (OI-1); no row job may fill it" % slot)
        if slot not in PROVISIONAL_KIND:
            raise NameSlotUnavailable("slot %s is unknown" % slot)
        return PROVISIONAL_KIND[slot], True

    def get(self, slot, key):
        kind, prov = self.kind_for(slot)
        nm = self.ns.unique(kind, "%s:%s" % (slot, key))
        if prov:
            self.used_provisional = True
        self.issued.append((slot, key, nm))
        return nm

    # display forms (formatting only; the characters still come from namespace.py)
    def slug(self, slot, key):
        return self.get(slot, key).lower().replace(" ", "-")

    def stem(self, key):
        return self.get("ns.path_stem", key)

    def envvar(self, key):
        return self.get("ns.envvar", key).upper()

    def fingerprint(self):
        return self.ns.fingerprint()


def assert_row_ready(spec_meta):
    """Used by the row jobs (not by tests): refuse any spec built with provisional names."""
    if spec_meta.get("names_provisional"):
        raise NameSlotUnavailable("spec used provisional names (OI-1): not row-ready")


def build_job_manifest(job_id, family, specs_ids):
    """Names-only job manifest for row_start_guard.py. specs_ids: iterable of (row_id, {category: [ids]})."""
    al = get_allowlist()
    union = {c: set() for c in CATEGORIES}
    rows = []
    for rid, used in specs_ids:
        rows.append({"row_id": rid, "names": {c: sorted(set(used.get(c, ()))) for c in CATEGORIES}})
        for c in CATEGORIES:
            union[c].update(used.get(c, ()))
    bad = al.check(family, union)
    if bad:
        raise AllowListError("; ".join(bad[:10]))
    return {"job_id": job_id, "family": family, "names": {c: sorted(union[c]) for c in CATEGORIES}, "rows": rows}
