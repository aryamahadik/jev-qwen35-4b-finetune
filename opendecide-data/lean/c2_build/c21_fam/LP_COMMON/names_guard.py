"""Names guard against the FROZEN names manifest v1.2 (NAMES_MANIFEST_V1_2.json, sha-pinned).

Every policy, tool, language, runner and carrier name a row declares must be on the frozen allow-list AND on the family's own
per-family list (a family may not borrow another family's carrier). The family must be on row_job_families_allowed.
Only names are handled; the guard never reads rows. Built on the L-0 guard's own loader (c21_infra/row_start_guard.py).
"""
import json

from . import paths  # noqa: F401
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
        self.file_sha = rsg.sha256_file(self.path)
        if verify_sha:
            with open(sha_path, "r", encoding="utf-8") as f:
                pinned = f.read().split()[0].lower()
            if pinned != self.file_sha:
                raise NamesViolation(["ALLOWLIST_SHA_MISMATCH: %s != pinned %s" % (self.file_sha[:12], pinned[:12])])
            pin = pinned
        else:
            pin = self.file_sha
        allow, sha, reasons, fams = rsg.load_allowlist_and_families(self.path, pin)
        if reasons:
            raise NamesViolation(reasons)
        self.allow = allow
        self.families = fams
        with open(self.path, "r", encoding="utf-8") as f:
            self._doc = json.load(f)
        self._per_family = self._doc["per_family_names"]

    def family_names(self, family):
        bad = rsg.check_family(family, self.families)
        if bad:
            raise NamesViolation(bad)
        return {c: frozenset(self._per_family.get(family, {}).get(c, [])) for c in CATEGORIES}

    def check(self, family, names):
        """names: {category: [name,...]}. Returns violation strings ([] = clean)."""
        try:
            fam = self.family_names(family)
        except NamesViolation as e:
            return list(e.items)
        bad = rsg.check_names(names, self.allow, family)
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
        full = {c: sorted(set(names.get(c, []))) for c in CATEGORIES}
        self.assert_ok(family, full)
        m = {"job_id": job_id, "family": family, "names": full}
        if rows is not None:
            m["rows"] = [{"row_id": r["row_id"], "names": {c: sorted(set(r["names"].get(c, []))) for c in CATEGORIES}} for r in rows]
        return m


_DEFAULT = None


def default_guard():
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = NamesGuard()
    return _DEFAULT
