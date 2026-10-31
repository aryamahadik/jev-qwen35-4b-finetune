"""Row-start guard (C2.1 plan v3.1 section 2/8; L-0 output (h)).

Refuses to start any C2.1 ROW job unless ALL of these hold:
  1. the OHS-5 freeze record exists (os.path check; the file must be named OHS5_FREEZE.json, so the guard can
     never be pointed at any other sealed file), carries a well-formed sha field, and that sha equals the
     PINNED freeze sha the orchestrator supplies (an unpinned or hand-made record is refused). Only that one
     file is touched, only its sha field is kept; no other sealed file is ever opened or listed.
  2. the G13 target registry sha is pinned: a pinned sha is supplied AND the registry file's sha256 equals it.
  3. the frozen names-only allow-list is loaded (frozen:true) and equals its PINNED sha (an unpinned list
     could be edited to add the off-list name), and EVERY policy, tool, language, runner and carrier name in
     the job manifest is on it (exact match; any other category the manifest names must also exist in the
     allow-list; the job must declare all five categories, an empty list is allowed). One name off the list
     refuses the job. Duplicate JSON keys in any input are refused (two parsers could read different values).
  4. the job names a FAMILY ("family": "T50"...) and that family is on the allow-list's row_job_families_allowed
     (exact, case-sensitive match; the list is part of the pinned allow-list file, so it cannot be edited after
     the pin). A job without a family, with a non-string/empty family, with a family off the list, or an
     allow-list that carries no (or a malformed, duplicated or empty) families list, is refused. A per-row
     "family" field, when present, must equal the job's family (no mixed-family job).
  Every file the guard is told to read (manifest, allow-list, registry) is refused when ANY component of its
  absolute path contains ohs or sealed. The shas of all inputs are printed and exported to a --exec child as
  OD_ROWGUARD_* variables, so the child can detect a file changed after the check.
Exit codes: 0 = allowed to start, 1 = refused, 2 = usage error.

Job manifest (JSON):  {"job_id": "...", "family": "T50", "names": {"policy": [...], "tool": [...], "language": [...],
                       "runner": [...], "carrier": [...]},
                       "rows": [{"row_id": "...", "names": {...}}]   # optional per-row name sets
Allow-list (JSON):    {"frozen": true, "version": "...", "row_job_families_allowed": ["T50", ...],
                       "names": {"policy": [...], ...}}

Only names and shas are ever printed. Use `--exec -- CMD ARGS...` to run the row job only after the checks pass.
"""
import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathskip import is_skipped_path, safe_glob  # noqa: E402

DEFAULT_FREEZE = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/ohs5_sealed/OHS5_FREEZE.json"
FREEZE_BASENAME = "OHS5_FREEZE.json"
MAX_FREEZE_BYTES = 1 << 20
CATEGORIES = ("policy", "tool", "language", "runner", "carrier")
_SHA = re.compile(r"^[0-9a-f]{64}$")
MAX_SHOWN = 50


class GuardRefused(Exception):
    def __init__(self, reasons):
        super().__init__("; ".join(reasons))
        self.reasons = list(reasons)


def _no_dup_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError("duplicate key")
        d[k] = v
    return d


def load_json_strict(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=_no_dup_pairs)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_freeze_sha(path):
    """Existence via os.path; then read ONLY the sha field of that one record. Returns (sha | None, reason | None)."""
    if os.path.basename(path) != FREEZE_BASENAME:
        return None, "FREEZE_PATH_WRONG: the freeze record must be a file named %s" % FREEZE_BASENAME
    if not os.path.isfile(path):
        return None, "FREEZE_MISSING: OHS-5 freeze record does not exist"
    try:
        if os.path.getsize(path) > MAX_FREEZE_BYTES:
            return None, "FREEZE_UNREADABLE: freeze record is larger than %d bytes" % MAX_FREEZE_BYTES
        obj = load_json_strict(path)
    except (OSError, ValueError):
        return None, "FREEZE_UNREADABLE: freeze record is not valid JSON"
    sha = obj.get("sha") if isinstance(obj, dict) else None
    if sha is None and isinstance(obj, dict):
        sha = obj.get("sha256")
    if not isinstance(sha, str) or not _SHA.match(sha):
        return None, "FREEZE_NO_SHA: freeze record has no well-formed sha field"
    return sha, None


def check_registry(path, pinned_sha):
    if not pinned_sha:
        return None, "REGISTRY_SHA_NOT_PINNED: no pinned G13 target registry sha supplied"
    if not _SHA.match(pinned_sha.lower()):
        return None, "REGISTRY_SHA_MALFORMED: pinned sha is not 64 hex characters"
    if not path or not os.path.isfile(path):
        return None, "REGISTRY_MISSING: G13 target registry file not found"
    if is_skipped_path(path):
        return None, "REGISTRY_PATH_BARRED: registry path has an ohs/sealed component"
    actual = sha256_file(path)
    if actual != pinned_sha.lower():
        return actual, "REGISTRY_SHA_MISMATCH: registry sha %s != pinned %s" % (actual[:12], pinned_sha.lower()[:12])
    return actual, None


def _load_allowlist_full(path, pinned_sha=None):
    """One read of the file: the sha is taken from the same bytes that are parsed (no sha/parse gap).
    Returns ({category: frozenset(names)}, sha, [reasons], frozenset(families) | None)."""
    reasons = []
    if not path or not os.path.isfile(path):
        return {}, None, ["ALLOWLIST_MISSING: names-only allow-list not found"], None
    if is_skipped_path(path):
        return {}, None, ["ALLOWLIST_PATH_BARRED: allow-list path has an ohs/sealed component"], None
    with open(path, "rb") as f:
        raw = f.read()
    sha = hashlib.sha256(raw).hexdigest()
    if not pinned_sha:
        reasons.append("ALLOWLIST_SHA_NOT_PINNED: no pinned allow-list sha supplied (an unpinned list can be edited)")
    elif not _SHA.match(pinned_sha.lower()):
        reasons.append("ALLOWLIST_SHA_MALFORMED: pinned allow-list sha is not 64 hex characters")
    elif sha != pinned_sha.lower():
        reasons.append("ALLOWLIST_SHA_MISMATCH: allow-list sha %s != pinned %s" % (sha[:12], pinned_sha.lower()[:12]))
    try:
        obj = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_dup_pairs)
    except (ValueError, RecursionError):
        return {}, sha, reasons + ["ALLOWLIST_UNREADABLE: not valid JSON (or has a duplicate key)"], None
    if not isinstance(obj, dict) or obj.get("frozen") is not True:
        reasons.append("ALLOWLIST_NOT_FROZEN: allow-list must carry frozen:true")
    fams, why = _parse_families(obj.get("row_job_families_allowed") if isinstance(obj, dict) else None)
    if why:
        reasons.append(why)
    names = obj.get("names") if isinstance(obj, dict) else None
    out = {}
    if not isinstance(names, dict):
        return {}, sha, reasons + ["ALLOWLIST_BAD_SHAPE: 'names' must be an object of lists"], fams
    for cat, lst in names.items():
        if not isinstance(lst, list) or not all(isinstance(x, str) for x in lst):
            reasons.append("ALLOWLIST_BAD_SHAPE: category %r must be a list of strings" % cat)
            continue
        out[cat] = frozenset(lst)
    for cat in CATEGORIES:
        if cat not in out:
            reasons.append("ALLOWLIST_INCOMPLETE: category %r missing" % cat)
    return out, sha, reasons, fams


def _parse_families(lst):
    """The allow-list's row_job_families_allowed -> (frozenset | None, reason | None). Fail closed on anything odd."""
    if lst is None:
        return None, "ALLOWLIST_FAMILIES_MISSING: allow-list has no row_job_families_allowed (family check cannot run)"
    if not isinstance(lst, list) or not lst or not all(isinstance(x, str) and x for x in lst):
        return None, "ALLOWLIST_FAMILIES_BAD_SHAPE: row_job_families_allowed must be a non-empty list of non-empty strings"
    if len(set(lst)) != len(lst):
        return None, "ALLOWLIST_FAMILIES_BAD_SHAPE: row_job_families_allowed has a duplicate entry"
    return frozenset(lst), None


def load_allowlist(path, pinned_sha=None):
    """Returns ({category: frozenset(names)}, sha, [reasons]). Families: see load_allowlist_and_families."""
    out, sha, reasons, _ = _load_allowlist_full(path, pinned_sha)
    return out, sha, reasons


def load_allowlist_and_families(path, pinned_sha=None):
    """Returns (names, sha, [reasons], families | None). The reasons include any family-list problem."""
    return _load_allowlist_full(path, pinned_sha)


def check_family(family, families, where="job"):
    """Violation list for one declared family against the allow-list's families (None = list unusable -> refuse)."""
    if families is None:
        return ["FAMILY_LIST_UNAVAILABLE(%s): no usable row_job_families_allowed, family %r cannot be verified" % (where, family if isinstance(family, str) else None)]
    if family is None:
        return ["FAMILY_MISSING(%s): the job must declare its family" % where]
    if not isinstance(family, str) or not family:
        return ["FAMILY_BAD_SHAPE(%s): family must be a non-empty string" % where]
    if family not in families:
        return ["FAMILY_OFF_ALLOWLIST(%s): family=%r" % (where, family[:40])]
    return []


def check_names(names, allow, where="job"):
    """names: {category: [name,...]}. Returns a list of violation strings (names only, never row content)."""
    bad = []
    if not isinstance(names, dict) or not names:
        return ["NAMES_MISSING(%s): no names declared, nothing to verify" % where]
    for cat, lst in names.items():
        if cat not in allow:
            bad.append("UNKNOWN_CATEGORY(%s): %r is not an allow-list category" % (where, cat))
            continue
        if not isinstance(lst, list) or not all(isinstance(x, str) for x in lst):
            bad.append("BAD_SHAPE(%s): category %r must be a list of strings" % (where, cat))
            continue
        off = sorted(set(x for x in lst if x not in allow[cat]))
        for nm in off[:MAX_SHOWN]:
            bad.append("NAME_OFF_ALLOWLIST(%s): %s=%r" % (where, cat, nm))
        if len(off) > MAX_SHOWN:
            bad.append("NAME_OFF_ALLOWLIST(%s): %s +%d more" % (where, cat, len(off) - MAX_SHOWN))
    return bad


def check_manifest(path, allow, families=None):
    if is_skipped_path(path):
        return ["MANIFEST_PATH_BARRED: job manifest path has an ohs/sealed component: %s" % os.path.basename(path)]
    try:
        m = load_json_strict(path)
    except (OSError, ValueError):
        return ["MANIFEST_UNREADABLE: %s is not valid JSON (or has a duplicate key)" % os.path.basename(path)]
    if not isinstance(m, dict):
        return ["MANIFEST_BAD_SHAPE: %s must be a JSON object" % os.path.basename(path)]
    label = str(m.get("job_id", os.path.basename(path)))[:60]
    jn = m.get("names")
    jfam = m.get("family")
    bad = check_family(jfam, families, label)
    bad += check_names(jn, allow, label)
    if isinstance(jn, dict) and jn:
        for cat in CATEGORIES:
            if cat not in jn:
                bad.append("NAMES_INCOMPLETE(%s): category %r not declared (declare an empty list if unused)" % (label, cat))
        if not any(isinstance(v, list) and v for v in jn.values()):
            bad.append("NAMES_EMPTY(%s): every category is empty, nothing to verify" % label)
    rows = m.get("rows")
    if rows is not None:
        if not isinstance(rows, list):
            bad.append("BAD_SHAPE(%s): rows must be a list" % label)
        else:
            for i, r in enumerate(rows):
                rid = str(r.get("row_id", i))[:40] if isinstance(r, dict) else str(i)
                if isinstance(r, dict) and "family" in r and r["family"] != jfam:
                    bad.append("FAMILY_ROW_MISMATCH(%s/row %s): row family %r != job family %r" % (
                        label, rid, str(r["family"])[:40], str(jfam)[:40]))
                bad += check_names(r.get("names") if isinstance(r, dict) else None, allow, "%s/row %s" % (label, rid))
                if len(bad) > 4 * MAX_SHOWN:
                    bad.append("TRUNCATED: further row violations not listed")
                    break
    return bad


def evaluate(manifests, allowlist, registry, registry_sha, freeze=DEFAULT_FREEZE, allowlist_sha=None, freeze_sha=None):
    """Returns (ok, reasons, facts). facts holds shas only."""
    reasons, facts = [], {}
    fsha, why = read_freeze_sha(freeze)
    if why:
        reasons.append(why)
    else:
        facts["freeze_sha"] = fsha
        if not freeze_sha:
            reasons.append("FREEZE_SHA_NOT_PINNED: no pinned freeze sha supplied (a hand-made record could pass)")
        elif not _SHA.match(freeze_sha.lower()):
            reasons.append("FREEZE_SHA_MALFORMED: pinned freeze sha is not 64 hex characters")
        elif fsha != freeze_sha.lower():
            reasons.append("FREEZE_SHA_MISMATCH: freeze sha %s != pinned %s" % (fsha[:12], freeze_sha.lower()[:12]))
    rsha, why = check_registry(registry, registry_sha)
    if why:
        reasons.append(why)
    else:
        facts["registry_sha"] = rsha
    allow, asha, why_list, families = _load_allowlist_full(allowlist, allowlist_sha)
    reasons += why_list
    if asha:
        facts["allowlist_sha"] = asha
    if not manifests:
        reasons.append("MANIFEST_MISSING: no job manifest given")
    elif allow:
        for mp in manifests:
            reasons += check_manifest(mp, allow, families)
        if not any(r.startswith("MANIFEST_PATH_BARRED") for r in reasons):
            for i, mp in enumerate(manifests):
                try:
                    facts["manifest_%d_sha" % i] = sha256_file(mp)
                except OSError:
                    pass
    return (not reasons), reasons, facts


def require_start(*args, **kw):
    ok, reasons, facts = evaluate(*args, **kw)
    if not ok:
        raise GuardRefused(reasons)
    return facts


def main(argv=None):
    ap = argparse.ArgumentParser(description="Refuse to start a C2.1 row job unless the freeze, registry pin and allow-list checks pass.")
    ap.add_argument("--manifest", action="append", default=[], help="job manifest JSON (repeatable)")
    ap.add_argument("--manifest-glob", help="glob relative to --root, e.g. 'data/**/job_*.json' (ohs/sealed paths are skipped)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--allowlist", required=True, help="frozen names-only allow-list JSON")
    ap.add_argument("--allowlist-sha", help="pinned sha256 of the allow-list file (required to start)")
    ap.add_argument("--registry", required=True, help="G13 target registry file")
    ap.add_argument("--registry-sha", help="pinned sha256 of the registry (required to start)")
    ap.add_argument("--freeze", default=DEFAULT_FREEZE, help="OHS-5 freeze record path (existence + sha field only)")
    ap.add_argument("--freeze-sha", help="pinned sha in the freeze record (required to start)")
    ap.add_argument("--exec", dest="exec_", action="store_true", help="after a pass, exec the command following '--'")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)
    manifests = list(a.manifest)
    if a.manifest_glob:
        manifests += safe_glob(a.root, a.manifest_glob)
    ok, reasons, facts = evaluate(manifests, a.allowlist, a.registry, a.registry_sha, a.freeze,
                                  a.allowlist_sha, a.freeze_sha)
    if not ok:
        print("ROW START REFUSED (%d reason%s)" % (len(reasons), "" if len(reasons) == 1 else "s"))
        for r in reasons[: 4 * MAX_SHOWN]:
            print("  - " + r)
        return 1
    print("ROW START ALLOWED manifests=%d " % len(manifests) + " ".join("%s=%s" % (k, v[:16]) for k, v in sorted(facts.items())))
    if a.exec_:
        cmd = [c for c in a.cmd if c != "--"] if a.cmd and a.cmd[0] == "--" else a.cmd
        if not cmd:
            print("--exec given without a command", file=sys.stderr)
            return 2
        sys.stdout.flush()
        for k, v in facts.items():
            os.environ["OD_ROWGUARD_" + k.upper()] = v
        os.execvp(cmd[0], cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
