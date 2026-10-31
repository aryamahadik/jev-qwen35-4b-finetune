"""Names guard for the L-C families (K15 / K16 / K15-equivalent in each G0-lite).

Every policy, tool, language, runner and carrier name a row or a job manifest declares must be on the frozen,
names-only allow-list (zed_orch/c21/l0/NAMES_MANIFEST_V1.json). This module:
  * loads that file through the L-0 guard's own loader (frozen:true, five categories, no duplicate keys);
  * checks the file sha256 against NAMES_MANIFEST_V1.sha256 (a hand-edited list is refused);
  * refuses any family that is not in row_job_families_allowed;
  * refuses any name that is on the global list but not on the family's own per-family list (a family may not borrow
    another family's carrier or runner);
  * builds job manifests in the exact shape row_start_guard.py expects.
It only handles names. It never reads rows.
"""
import hashlib
import json
import os

from . import paths  # noqa: F401  (puts c21_infra on sys.path)
import row_start_guard as rsg  # noqa: E402

CATEGORIES = rsg.CATEGORIES


class NamesViolation(ValueError):
    def __init__(self, items):
        super().__init__("; ".join(items))
        self.items = list(items)


class NamesGuard:
    def __init__(self, manifest_path=None, sha_path=None, verify_sha=True):
        self.path = manifest_path or paths.NAMES_MANIFEST
        sha_path = sha_path or paths.NAMES_MANIFEST_SHA
        self.sha = rsg.sha256_file(self.path)
        if verify_sha:
            with open(sha_path, "r", encoding="utf-8") as f:
                pinned = f.read().split()[0].lower()
            if pinned != self.sha:
                raise NamesViolation(["ALLOWLIST_SHA_MISMATCH: %s != pinned %s" % (self.sha[:12], pinned[:12])])
            pin = pinned
        else:
            pin = self.sha
        allow, sha, reasons = rsg.load_allowlist(self.path, pin)
        if reasons:
            raise NamesViolation(reasons)
        self.allow = allow
        with open(self.path, "r", encoding="utf-8") as f:
            self._doc = json.load(f)
        self.families = tuple(self._doc["row_job_families_allowed"])
        self._per_family = self._doc["per_family_names"]

    # ------------------------------------------------------------------ queries
    def family_names(self, family):
        if family not in self.families:
            raise NamesViolation(["FAMILY_NOT_ALLOWED: %r" % family])
        return {c: frozenset(self._per_family.get(family, {}).get(c, [])) for c in CATEGORIES}

    def check(self, family, names):
        """names: {category: [name, ...]}. Returns a list of violation strings ([] = clean)."""
        bad = []
        try:
            fam = self.family_names(family)
        except NamesViolation as e:
            return list(e.items)
        bad += rsg.check_names(names, self.allow, family)
        for cat, lst in (names or {}).items():
            if cat in fam and isinstance(lst, list):
                for nm in sorted(set(lst)):
                    if nm in self.allow.get(cat, ()) and nm not in fam[cat]:
                        bad.append("NAME_NOT_IN_FAMILY_LIST(%s): %s=%r" % (family, cat, nm))
        return bad

    def assert_ok(self, family, names):
        bad = self.check(family, names)
        if bad:
            raise NamesViolation(bad)
        return True

    def job_manifest(self, job_id, family, names, rows=None):
        """Manifest dict in the shape row_start_guard.check_manifest reads. Declares all five categories."""
        full = {c: sorted(set(names.get(c, []))) for c in CATEGORIES}
        self.assert_ok(family, full)
        m = {"job_id": job_id, "family": family, "names": full}
        if rows is not None:
            m["rows"] = [{"row_id": r["row_id"], "names": {c: sorted(set(r["names"].get(c, []))) for c in CATEGORIES}}
                         for r in rows]
        return m


_DEFAULT = None


def default_guard():
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = NamesGuard()
    return _DEFAULT


def write_json(path, obj):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
    return hashlib.sha256(open(path, "rb").read()).hexdigest()
