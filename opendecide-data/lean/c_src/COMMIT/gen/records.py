"""COMMIT commit records (G0 1.1 steps 2, 4-7; 1.2): diff parse, two count derivations, path classes, repo groups,
held-out repo groups, language, bot flag, normalised message.

Record (in memory, after build_records):
  {rid, ds, repo, group, date, licence, lang, msg (normalised), msg_raw_sha, bot, files: [F], n_files, added, removed}
  F = {ct, old, new, path (new or old), binary, mode_only, hunks: [{"header": str|None, "lines": [[kind, text], ...]}],
       added, removed}       kind: "+", "-", " " (context; CommitChronicle context lines carry no marker)
CLI: python gen/records.py stats   -> counts only.
"""
from __future__ import annotations

import collections
import fnmatch
import glob
import gzip
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
N_FORK = 3          # shared commit keys that join two repos into one group (A51)
N_MIN_HELDOUT = 40  # eligible commits a held-out group needs (1.1 step 4)
HELDOUT_SEED = "commit-heldout-v1"


@lru_cache(maxsize=1)
def lex() -> dict:
    d = json.load(open(C.HERE / "lexicon.json"))
    d["_bot"] = [re.compile(p.replace("(?i)", ""), re.I) for p in d["bot_regex"]]
    return d


# ---------------------------------------------------------------------------------------------------------------
# path classes (SEM-08): any folder segment equal to a folder name, or the file name matching a pattern; case ignored

def lint_class(cls: dict) -> list[str]:
    bad = []
    for f in cls.get("folders", []):
        if f in (".", "..") or not re.fullmatch(r"[A-Za-z0-9._\-]+", f):
            bad.append(f"folder:{f}")
    for p in cls.get("patterns", []):
        if not re.fullmatch(r"[A-Za-z0-9._\-*?]+", p):
            bad.append(f"pattern:{p}")
    return bad


def in_class(path: str | None, cls: dict) -> bool:
    if not path:
        return False
    segs = path.split("/")
    folders = {f.lower() for f in cls.get("folders", [])}
    if any(s.lower() in folders for s in segs[:-1]):
        return True
    name = segs[-1].lower()
    return any(fnmatch.fnmatchcase(name, p.lower()) for p in cls.get("patterns", []))


def file_in_class(f: dict, cls: dict) -> bool:
    """SEM-05: a renamed file is in a class if its old or its new path is."""
    return in_class(f.get("old"), cls) or in_class(f.get("new"), cls)


def pat_class(name: str) -> dict:
    L = lex()
    if name in L["triage_classes"]:
        return L["triage_classes"][name]
    m = {"lockfile": {"folders": [], "patterns": L["lockfile_patterns"]},
         "generated": {"folders": [], "patterns": L["generated_patterns"]},
         "vendored": {"folders": L["vendored_folders"], "patterns": []},
         "manifest": {"folders": [], "patterns": L["manifest_patterns"]},
         "changelog": {"folders": [], "patterns": L["changelog_patterns"]}}
    return m[name]


# ---------------------------------------------------------------------------------------------------------------
# diff parse + two count derivations (A50)

def parse_cc(diff: str):
    """CommitChronicle per-file diff: hunks split at '@@' header lines; context lines have no marker (the dataset
    collapses whitespace). Returns (hunks, countsA, countsB, flags)."""
    lines = diff.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    hunks, cur = [], None
    for ln in lines:
        if HUNK.match(ln):
            cur = {"header": ln, "lines": []}
            hunks.append(cur)
            continue
        if ln.startswith("\\ No newline"):
            continue
        if cur is None:
            cur = {"header": None, "lines": []}
            hunks.append(cur)
        k = ln[:1]
        cur["lines"].append(["+", ln[1:]] if k == "+" else ["-", ln[1:]] if k == "-" else [" ", ln])
    # derivation A: count markers
    a_add = sum(1 for h in hunks for k, _ in h["lines"] if k == "+")
    a_rem = sum(1 for h in hunks for k, _ in h["lines"] if k == "-")
    # derivation B: header state machine (character scan, no regex) on raw lines
    b_add = b_rem = 0
    ok, headerless_changes = True, False
    state = None  # [old_left, new_left] while inside a headered hunk
    for ln in lines:
        if ln.startswith("\\ No newline"):
            continue
        if ln[:3] == "@@ ":
            if state is not None and not _cc_end_ok(state):
                ok = False
            nums = _scan_header(ln)
            if nums is None:
                ok = False
                state = None
                continue
            state = [nums[1], nums[3]]
            continue
        c = ln[:1]
        if state is None:
            if c == "+":
                b_add += 1
                headerless_changes = True
            elif c == "-":
                b_rem += 1
                headerless_changes = True
            continue
        if c == "+":
            b_add += 1
            state[1] -= 1
        elif c == "-":
            b_rem += 1
            state[0] -= 1
        else:
            state[0] -= 1
            state[1] -= 1
    if state is not None and not _cc_end_ok(state):
        ok = False
    return hunks, (a_add, a_rem), (b_add, b_rem), {"b_header_ok": ok, "headerless_changes": headerless_changes}


def _cc_end_ok(state) -> bool:
    """CommitChronicle drops blank context lines (O14 re-plan at G1, read from the data): a headered hunk is consistent
    when the lines left unseen are the same number on the old and the new side (context lines only), never negative.
    A context line read as a changed line makes the two sides differ, so the commit is dropped."""
    return state[0] == state[1] and state[0] >= 0


def _scan_header(ln: str):
    """'@@ -a,b +c,d @@' by character scan; omitted counts are 1."""
    i, n, out = 3, len(ln), []
    for sign in "-+":
        if i >= n or ln[i] != sign:
            return None
        i += 1
        j = i
        while j < n and ln[j].isdigit():
            j += 1
        if j == i:
            return None
        start = int(ln[i:j])
        cnt = 1
        if j < n and ln[j] == ",":
            k = j + 1
            while k < n and ln[k].isdigit():
                k += 1
            if k == j + 1:
                return None
            cnt = int(ln[j + 1:k])
            j = k
        out += [start, cnt]
        i = j + 1
    return out


def parse_pf(diff: str):
    """CommitPackFT git diff text (from the first '@@'): context lines start with ' '."""
    lines = diff.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    hunks, cur = [], None
    for ln in lines:
        if HUNK.match(ln):
            cur = {"header": ln, "lines": []}
            hunks.append(cur)
            continue
        if ln.startswith("\\ No newline") or cur is None:
            continue
        k = ln[:1]
        cur["lines"].append([k if k in "+-" else " ", ln[1:]])
    hs, (b_add, b_rem, ok) = hunks, _b_pf(lines)
    a = (sum(1 for h in hs for k, _ in h["lines"] if k == "+"), sum(1 for h in hs for k, _ in h["lines"] if k == "-"))
    return hunks, a, (b_add, b_rem), {"b_header_ok": ok, "headerless_changes": False}


def _b_pf(lines):
    b_add = b_rem = 0
    ok, state = True, None
    for ln in lines:
        if ln.startswith("\\ No newline"):
            continue
        if ln[:3] == "@@ ":
            if state is not None and state != [0, 0]:
                ok = False
            nums = _scan_header(ln)
            state = [nums[1], nums[3]] if nums else None
            ok = ok and nums is not None
            continue
        if state is None:
            continue
        c = ln[:1]
        if c == "+":
            b_add += 1
            state[1] -= 1
        elif c == "-":
            b_rem += 1
            state[0] -= 1
        else:
            state[0] -= 1
            state[1] -= 1
    if state is not None and state != [0, 0]:
        ok = False
    return b_add, b_rem, ok


# ---------------------------------------------------------------------------------------------------------------

def iter_raw():
    for fn in sorted(glob.glob(str(C.DATA / "cc_records_*.jsonl.gz"))) + \
            sorted(glob.glob(str(C.DATA / "pf_records_*.jsonl.gz"))):
        with gzip.open(fn, "rt") as f:
            for line in f:
                yield json.loads(line)


def build_record(raw: dict, drops: collections.Counter, scrub: dict):
    """Normalise + parse one raw commit; returns a record or None (drop reason counted)."""
    files = []
    for f in raw["files"]:
        if raw["ds"] == "CommitChronicle":
            hunks, a, b, fl = parse_cc(f["diff"])
            if fl["headerless_changes"]:
                mk = {"ADD": "+", "DELETE": "-"}.get(f["ct"])
                body = [ln for ln in f["diff"].split("\n") if ln and not ln.startswith("\\ No newline")]
                # B for whole-file adds/deletes: every line carries the one marker the change kind allows
                if not (mk and len(hunks) == 1 and body and all(ln[:1] == mk for ln in body)):
                    drops["count_unverified_headerless"] += 1
                    return None
        else:
            hunks, a, b, fl = parse_pf(f["diff"])
            if (f["a_added"], f["a_removed"]) != a:
                drops["count_mismatch_lcs"] += 1
                return None
        if a != b or not fl["b_header_ok"]:
            drops["count_mismatch"] += 1
            return None
        binary = "Binary files" in f["diff"][:200] or "GIT binary patch" in f["diff"][:200]
        mode_only = not f["diff"].strip() and f["ct"] == "MODIFY"
        if not f["diff"].strip() and not mode_only and f["ct"] not in ("ADD", "DELETE", "RENAME"):
            drops["diff_unparsed"] += 1
            return None
        files.append({"ct": f["ct"], "old": f["old"], "new": f["new"], "path": f["new"] or f["old"],
                      "binary": binary, "mode_only": mode_only, "hunks": hunks, "added": a[0], "removed": a[1]})
    msg = C.normalise_message(raw["msg_raw"], scrub)
    if not msg.strip():
        drops["empty_message"] += 1
        return None
    langs = collections.Counter()
    for f in files:
        lg = C.lang_of(f["path"])
        if lg:
            langs[lg] += f["added"] + f["removed"]
    lang = sorted(langs.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if langs else "none"
    first = msg.split("\n", 1)[0]
    bot = any(p.search(first) for p in lex()["_bot"])
    return {"rid": raw["rid"], "ds": raw["ds"], "repo": raw["repo"], "repos": raw.get("repos") or [raw["repo"]],
            "date": raw.get("date"), "licence": raw["repo_licence"], "lang": lang, "msg": msg, "bot": bot,
            "files": files, "n_files": len(files), "added": sum(f["added"] for f in files),
            "removed": sum(f["removed"] for f in files)}


def commit_key(rec: dict) -> str:
    norm = re.sub(r"\s+", " ", rec["msg"].lower()).strip()
    fl = sorted((f["path"], f["added"], f["removed"]) for f in rec["files"])
    return C.sha256(norm + "\x1f" + json.dumps(fl))


def repo_groups(recs: list[dict]) -> dict:
    """Union-find over normalised lower-case owner/name and shared commit keys (>= N_FORK) across both datasets."""
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    keyrepos = collections.defaultdict(set)
    for r in recs:
        names = [x.strip().lower() for x in r["repos"]]
        for n in names:
            find(n)
        for n in names[1:]:
            union(names[0], n)
        keyrepos[commit_key(r)].add(names[0])
    pair = collections.Counter()
    for k, rs in keyrepos.items():
        rs = sorted(rs)
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                pair[(rs[i], rs[j])] += 1
    for (a, b), n in pair.items():
        if n >= N_FORK:
            union(a, b)
    return {n: "g_" + C.sha256(find(n))[:10] for n in list(parent)}


def load_records(drops=None, scrub=None) -> list[dict]:
    drops = drops if drops is not None else collections.Counter()
    scrub = scrub if scrub is not None else {}
    recs, seen = [], {}
    for raw in iter_raw():
        r = build_record(raw, drops, scrub)
        if r is None:
            continue
        k = commit_key(r)
        if k in seen:            # same commit in both datasets: keep the CommitChronicle copy (A51)
            j = seen[k]
            if recs[j]["ds"] != "CommitChronicle" and r["ds"] == "CommitChronicle":
                recs[j] = r
            drops["dup_commit_key"] += 1
            continue
        seen[k] = len(recs)
        recs.append(r)
    g = repo_groups(recs)
    for r in recs:
        r["group"] = g[r["repo"].strip().lower()]
    return recs


if __name__ == "__main__" and sys.argv[1:] == ["stats"]:
    drops, scrub = collections.Counter(), {}
    recs = load_records(drops, scrub)
    by = collections.Counter(r["ds"] for r in recs)
    groups = collections.Counter((r["ds"], r["group"]) for r in recs)
    print(json.dumps({"records": len(recs), "by_ds": by, "groups_cc": sum(1 for k in groups if k[0] == "CommitChronicle"),
                      "groups_pf": sum(1 for k in groups if k[0] == "CommitPackFT"), "bot": sum(r["bot"] for r in recs),
                      "drops": drops, "scrub": scrub,
                      "lint": {k: lint_class(v) for k, v in lex()["triage_classes"].items()}}, default=str)[:1500])
