#!/usr/bin/env python3
"""W6: Conventional Commits type of a real commit message (PREREG_FINAL A40 b). Gold = PROGRAM (the stripped prefix).

Sources: 6 permissive GitHub repos that follow Conventional Commits (angular/angular and vitejs/vite are excluded by
A40 a; none of the A40 a never-train datasets is read). `fetch()` makes a bare, treeless clone (commits only, no file
contents) of each into wave2/raw/git/ (git-ignored) and records the licence the GitHub API reports.

Per commit (first-parent history of the default branch, merges excluded):
  - parse "type(scope)!: description"; gold = type; the type, scope and "!" are stripped;
  - drop: bot authors; merges and reverts; a type outside the 10 standard ones (feat fix docs style refactor perf test
    build ci chore); a scope that names another type (fix(ci):, chore(docs):, ...) or deps; dependency / version bumps and
    releases; a description under 3 or over 30 words; a description that itself starts with a prefix; a body that holds
    a prefixed line of a DIFFERENT type (squashed mixed commits); text with an email, phone, user path or IP left after
    cleaning; exact duplicate descriptions;
  - body cleaning: trailers (Co-authored-by, Signed-off-by, Fixes #, ...), "Notes: none", markdown headers, check
    lists, code fences, HTML comments, URLs, emails and @handles are removed; prefixed lines of the SAME type are
    removed (they would leak the gold); the body is cut to <= 80 words at a line boundary;
  - "(#1234)" PR suffixes are removed from the description.
Options of a row = the types present in its repo (types with >= MIN_TYPE clean commits, at most 8, most frequent);
commits of other types are dropped. Balance: an equal quota per type (target / number of types), water-filled across
repos so each type comes from as many repos as possible.

  ../../../../../.venv/bin/python -I builders/w6_commit.py [--fetch] [--target 1700] [--dry-run]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders import common as C  # noqa: E402

T = "W6"
TARGET = 1700
MIN_TYPE = 40
GIT_DIR = C.RAW / "git"
REPOS = {   # owner/repo: expected SPDX licence (verified via the GitHub API at fetch time)
    "electron/electron": "MIT",
    "denoland/deno": "MIT",
    "nuxt/nuxt": "MIT",
    "vuejs/core": "MIT",
    "open-telemetry/opentelemetry-js": "Apache-2.0",
    "googleapis/release-please": "Apache-2.0",
}
EXCLUDED = ("angular/angular", "vitejs/vite")        # A40 a never-train commit histories
PERMISSIVE = ("MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "0BSD", "Unlicense", "CC0-1.0")
STD = ("feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore")
TYPE_WORDS = set(STD) | {"doc", "tests", "deps", "dep", "release", "revert", "chores", "types", "lint"}

DEFS = {
    "feat": "the commit adds a new feature or capability for the project's users.",
    "fix": "the commit fixes a bug or other wrong behaviour.",
    "docs": "the commit changes documentation only (guides, API docs, READMEs or code comments).",
    "style": "the commit changes formatting only (whitespace, semicolons, code style) with no change in meaning.",
    "refactor": "the commit restructures code without changing its behaviour, fixing a bug or adding a feature.",
    "perf": "the commit makes something faster or use less memory, disk or bandwidth.",
    "test": "the commit adds, fixes or changes tests only.",
    "build": "the commit changes the build system, packaging, compilers or external build tooling.",
    "ci": "the commit changes continuous-integration configuration or scripts (pipelines, workflows, CI jobs).",
    "chore": "the commit is routine maintenance that changes no shipped behaviour, tests or docs (tooling, "
             "housekeeping, repository settings).",
}
QUESTIONS = ("Which Conventional Commits type fits this commit message? Its type prefix and scope were removed.",
             "This commit message had its Conventional Commits type prefix removed. Which type does it have?")

SUBJECT = re.compile(r"^(?P<type>[A-Za-z]+)(?:\((?P<scope>[^()]*)\))?(?P<bang>!)?: (?P<desc>\S.*)$")
BOT = re.compile(r"(?i)\[bot\]|\bbot\b|-bot\b|renovate|dependabot|github-actions|release-please|greenkeeper|"
                 r"semantic-release|snyk|copilot")
PREFIXED_LINE = re.compile(r"^\s*(?:[-*]\s*)?(?P<type>[a-z]+)(?:\([^()]*\))?!?: ", re.I)
TRAILER = re.compile(r"(?i)^\s*(co-authored-by|signed-off-by|reviewed-by|reviewed-on|acked-by|tested-by|reported-by|"
                     r"suggested-by|helped-by|cc|change-id|pr-url|backport-pr-url|refs?|fixes|closes|resolves|fix|close|"
                     r"resolve|see|related|part of|depends on|ref)\b\s*[:#]")
NOTES_NONE = re.compile(r"(?i)^\s*notes?\s*:\s*(none|no-notes|n/?a|no notes|-)?\s*\.?\s*$")
BUMP = re.compile(r"(?i)^(bump|upgrade|update|roll|pin|unpin|downgrade|lock|sync)\b.*(\d+\.\d+|\bto v?\d|dependenc|"
                  r"\bdeps?\b|lock ?file|\bversion|\bnode_modules|\bcrate|\bpackages?\b)")
RELEASE = re.compile(r"(?i)^(v?\d+\.\d+[\w.-]*|release\b|releasing\b|prepare (for )?(the )?release|publish\b|"
                     r"version packages|new version|cut release)|\brelease commit\b|\bforward\b.*\brelease\b")
URL = re.compile(r"https?://\S+|www\.\S+")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
HANDLE = re.compile(r"(?<![\w@])@[A-Za-z0-9_][A-Za-z0-9_.-]{0,38}")
PR_SUFFIX = re.compile(r"\s*\((?:#\d+(?:,\s*)?)+\)\s*$|\s+#\d+\s*$")


# ---------------------------------------------------------------------------------------------------------- fetch

def repo_dir(repo: str) -> Path:
    assert repo not in EXCLUDED
    return GIT_DIR / (repo.replace("/", "_") + ".git")


def fetch(repos=REPOS) -> dict:
    """Bare treeless clones (commits only) + the licence the GitHub API reports. Returns {repo: info}."""
    info = {}
    GIT_DIR.mkdir(parents=True, exist_ok=True)
    for repo, want in repos.items():
        assert repo not in EXCLUDED
        d = repo_dir(repo)
        if not d.exists():
            subprocess.run(["git", "clone", "-q", "--bare", "--filter=tree:0", "--single-branch",
                            f"https://github.com/{repo}.git", str(d)], check=True)
        meta = C._gb_tools_common().fetch_json(f"https://api.github.com/repos/{repo}")   # certifi TLS, low rate
        spdx = (meta.get("license") or {}).get("spdx_id")
        if spdx != want or spdx not in PERMISSIVE:
            raise SystemExit(f"{repo}: licence {spdx!r} (expected {want})")
        head = subprocess.run(["git", "--git-dir", str(d), "rev-parse", "HEAD"], check=True, capture_output=True,
                              text=True).stdout.strip()
        info[repo] = {"licence": spdx, "default_branch": meta.get("default_branch"), "head": head,
                      "clone": str(d), "fetched_from": f"https://github.com/{repo}.git"}
    C.kp.write_json(C.RAW / "repos.json", info)
    return info


def read_log(repo: str) -> list:
    """[{sha, author, email, date, subject, body}] first-parent, no merges (git log on the bare clone)."""
    d = repo_dir(repo)
    fmt = "%H%x1f%an%x1f%ae%x1f%aI%x1f%s%x1f%b%x1e"
    out = subprocess.run(["git", "--git-dir", str(d), "log", "--first-parent", "--no-merges", f"--format={fmt}",
                          "HEAD"], check=True, capture_output=True).stdout.decode("utf-8", "replace")
    rows = []
    for rec in out.split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        parts = rec.split("\x1f")
        if len(parts) != 6:
            continue
        sha, an, ae, date, subj, body = parts
        rows.append({"sha": sha, "author": an, "email": ae, "date": date, "subject": subj, "body": body})
    return rows


# ---------------------------------------------------------------------------------------------------------- parse

def clean_body(body: str, gold: str) -> tuple:
    """(cleaned body, problem or None). Removes trailers, templates, links and same-type prefixed lines."""
    body = re.sub(r"(?s)<!--.*?-->", " ", body or "")
    body = re.sub(r"(?s)```.*?```", " ", body)
    out = []
    for line in body.split("\n"):
        s = line.strip()
        if not s:
            out.append("")
            continue
        if TRAILER.match(s) or NOTES_NONE.match(s) or s.startswith("#") or re.match(r"^[-*]\s*\[[ xX]\]", s) \
                or re.fullmatch(r"[-*=_~`>|]+", s):
            continue
        m = PREFIXED_LINE.match(s)
        if m and m.group("type").lower() in TYPE_WORDS:
            if m.group("type").lower() != gold:
                return "", "mixed_types_in_body"
            continue                                   # restates the subject with its prefix: would leak the gold
        s2 = HANDLE.sub("", EMAIL.sub("", URL.sub("", s)))
        s2 = re.sub(r"\s+", " ", s2).strip(" -*")
        if s2 != re.sub(r"\s+", " ", s).strip(" -*") and C.nwords(s2) < 4:
            continue                                   # a line that was mostly a link or a handle
        if s2:
            out.append(s2)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    words, keep = 0, []
    for line in text.split("\n"):
        k = C.nwords(line)
        if words + k > 80:
            if not keep:
                keep.append(" ".join(line.split()[:80]))
            break
        keep.append(line)
        words += k
    return re.sub(r"\n{3,}", "\n\n", "\n".join(keep)).strip(), None


def parse_commit(c: dict) -> tuple:
    """(record or None, drop reason or None)."""
    if BOT.search(c["author"]) or BOT.search(c["email"]):
        return None, "bot"
    subj = c["subject"].strip()
    if subj.lower().startswith("merge ") or re.search(r"(?i)\brevert", subj):
        return None, "merge_or_revert"
    m = SUBJECT.match(subj)
    if not m:
        return None, "not_conventional"
    typ, scope, desc = m.group("type"), (m.group("scope") or "").strip().lower(), m.group("desc").strip()
    if typ != typ.lower() or typ not in STD:
        return None, "nonstandard_type"
    if re.search(r"(?i)\brevert", c["body"] or ""):
        return None, "merge_or_revert"
    scope_words = set(re.split(r"[\s,/|+-]+", scope)) if scope else set()
    if scope_words & (TYPE_WORDS - {typ}) or "deps" in scope or "release" in scope:
        return None, "scope_names_type"
    desc = PR_SUFFIX.sub("", desc).strip()
    if PREFIXED_LINE.match(desc) and PREFIXED_LINE.match(desc).group("type").lower() in TYPE_WORDS:
        return None, "double_prefix"
    if BUMP.search(desc) or RELEASE.search(desc):
        return None, "bump_or_release"
    if not 3 <= C.nwords(desc) <= 30:
        return None, "length"
    body, why = clean_body(c["body"], typ)
    if why:
        return None, why
    state = f"{desc}\n\n{body}" if body else desc
    if C.pii_reason(state):
        return None, "pii"
    return {"type": typ, "scope": scope or None, "breaking": bool(m.group("bang")), "desc": desc, "state": state,
            "sha": c["sha"], "date": c["date"]}, None


# ---------------------------------------------------------------------------------------------------------- build

def repo_options(recs: list) -> list:
    c = Counter(r["type"] for r in recs)
    top = [t for t, n in c.most_common() if n >= MIN_TYPE][:8]
    return [t for t in STD if t in top]


def build(logs: dict, info: dict, target: int = TARGET, checker=None) -> tuple:
    drops = Counter()
    pool, opts, seen_desc = {}, {}, set()
    for repo in sorted(logs):
        recs = []
        for c in logs[repo]:
            rec, why = parse_commit(c)
            if rec is None:
                drops[why] += 1
                continue
            k = re.sub(r"\W+", " ", rec["desc"].lower()).strip()
            if k in seen_desc:
                drops["duplicate_desc"] += 1
                continue
            seen_desc.add(k)
            recs.append(rec)
        opts[repo] = repo_options(recs)
        pool[repo] = [r for r in recs if r["type"] in opts[repo]]
        drops["type_not_in_repo_options"] += len(recs) - len(pool[repo])
    types = sorted({t for o in opts.values() for t in o}, key=STD.index)
    quota = target // max(1, len(types))
    picked = []
    for t in types:
        by_repo = {repo: sorted([r for r in pool[repo] if r["type"] == t],
                                key=lambda r: C.key_hash(C.SEED, T, "commit", r["sha"])) for repo in pool}
        sizes = {k: len(v) for k, v in by_repo.items() if v}
        lo, hi = 0, max(sizes.values()) if sizes else 0
        while lo < hi:
            mid = (lo + hi) // 2
            if sum(min(s, mid) for s in sizes.values()) >= quota:
                hi = mid
            else:
                lo = mid + 1
        take = []
        for repo in sorted(sizes):
            take += [(repo, r) for r in by_repo[repo][:min(sizes[repo], lo)]]
        take.sort(key=lambda x: C.key_hash(C.SEED, T, "take", x[1]["sha"]))
        picked += take[:quota]
    rows = []
    for repo, rec in picked:
        o = opts[repo]
        qi = C.pick_wording(QUESTIONS, T, rec["sha"])
        rows.append(C.make_row(
            T, f"{repo.replace('/', '_')}:{rec['sha'][:12]}", f"c2_wave2:W6:{repo}:{rec['sha'][:12]}", rec["state"],
            QUESTIONS[qi], qtype="choice", options=o, gold=rec["type"], card=C.card_lines([(t, DEFS[t]) for t in o]),
            gold_method="program",
            construction={"rule": "gold = the Conventional Commits type prefix, stripped with its scope",
                          "stripped_scope": rec["scope"], "breaking_bang": rec["breaking"]},
            extra_meta={"wording_id": f"W6.q{qi}", "repo": repo, "commit_sha": rec["sha"], "commit_date": rec["date"],
                        "repo_licence": info.get(repo, {}).get("licence", REPOS[repo]),
                        "licence": f"commit message from {repo} ({info.get(repo, {}).get('licence', REPOS[repo])})",
                        "repo_options": o}))
    kept, rdrops, toks = C.check_all(rows, checker)
    stats = {
        "type": T, "gold_method": "program", "repos": {r: {**info.get(r, {}), "options": opts[r],
                                                           "clean_pool": len(pool[r]),
                                                           "commits_read": len(logs[r])} for r in sorted(logs)},
        "types": types, "quota_per_type": quota, "drops": dict(drops), "candidates": len(rows),
        "kept_after_render": len(kept), "n_render_drops": len(rdrops), "render_drops": rdrops[:50],
        "labels": C.label_stats(kept), "tokens_min_med_max_mean": C.token_stats(toks),
        "per_repo": dict(Counter(r["meta"]["repo"] for r in kept)),
        "per_type_repo": {t: dict(Counter(r["meta"]["repo"] for r in kept if r["gold"] == t)) for t in types},
    }
    return kept, stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    target = int(argv[argv.index("--target") + 1]) if "--target" in argv else TARGET
    if "--fetch" in argv or not (C.RAW / "repos.json").exists():
        info = fetch()
    else:
        info = C.read_json(C.RAW / "repos.json")
    logs = {repo: read_log(repo) for repo in REPOS}
    rows, stats = build(logs, info, target)
    print(f"W6 rows {len(rows)} types {stats['types']} labels {stats['labels']['labels']} per repo "
          f"{stats['per_repo']} tokens {stats['tokens_min_med_max_mean']} render drops {stats['n_render_drops']}")
    if "--dry-run" not in argv:
        C.write_outputs(T, rows, stats)
    return rows, stats


if __name__ == "__main__":
    main()
