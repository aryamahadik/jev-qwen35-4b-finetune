"""COMMIT core: path classes (solver A: Python sets + fnmatch; solver B: sqlite folder join + GLOB), diff views and
the 1.3 shortening rule, numstat block, message words / code names (6.1), M hits with words (1.4), mention-state and
reader-agreement filters, and the independent state parser used by G3 (written from the spec, not from the renderer).
"""
from __future__ import annotations

import fnmatch
import html
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import lex2 as L  # noqa: E402

CUT = "[... {n} lines not shown ...]"
CUT_RE = re.compile(r"^\[\.\.\. (\d+) lines not shown \.\.\.\]$")
ROUTE_SEP = "~~~~~~~~"
CHARS_PER_TOK = 3.0


def triage_classes() -> dict:
    import records as RC
    return RC.lex()["triage_classes"]


# ---------------------------------------------------------------------------------------------------------------
# path classes

def lint_class(cls: dict) -> list[str]:
    bad = []
    for f in cls.get("folders", []):
        if not re.fullmatch(r"[A-Za-z0-9._-]+", f) or f in (".", ".."):
            bad.append("folder:" + f)
    for p in cls.get("patterns", []):
        if not re.fullmatch(r"[A-Za-z0-9.*?_-]+", p):
            bad.append("pattern:" + p)
    return bad


def in_class_A(path: str, cls: dict) -> bool:
    segs = path.split("/")
    folders = {s.lower() for s in segs[:-1]}
    name = segs[-1].lower()
    if folders & {f.lower() for f in cls.get("folders", [])}:
        return True
    return any(fnmatch.fnmatchcase(name, p.lower()) for p in cls.get("patterns", []))


def file_in_A(f: dict, cls: dict) -> bool:
    return any(in_class_A(p, cls) for p in {f.get("old"), f.get("new"), f.get("path")} if p)


class ClassDB:
    """Solver B path classes: folder-segment equality join + GLOB of the lower-cased file name (3.4 B)."""

    def __init__(self, classes: dict):
        self.db = sqlite3.connect(":memory:")
        cur = self.db.cursor()
        cur.execute("create table cf(cls text, name text)")
        cur.execute("create table cp(cls text, pat text)")
        for cname, cls in classes.items():
            for f in cls.get("folders", []):
                cur.execute("insert into cf values (?, ?)", (cname, f.lower()))
            for p in cls.get("patterns", []):
                cur.execute("insert into cp values (?, ?)", (cname, p.lower()))
        self.db.commit()

    def classes_of(self, paths: list[str]) -> list[set]:
        cur = self.db.cursor()
        cur.execute("create temp table if not exists fs(fid int, fname text)")
        cur.execute("create temp table if not exists sg(fid int, seg text)")
        cur.execute("delete from fs")
        cur.execute("delete from sg")
        for i, p in enumerate(paths):
            parts = p.split("/")
            cur.execute("insert into fs values (?, ?)", (i, parts[-1].lower()))
            for s in parts[:-1]:
                cur.execute("insert into sg values (?, ?)", (i, s.lower()))
        out = [set() for _ in paths]
        for fid, c in cur.execute("select fs.fid, cp.cls from fs join cp on fs.fname glob cp.pat "
                                  "union select sg.fid, cf.cls from sg join cf on sg.seg = cf.name"):
            out[fid].add(c)
        return out


# ---------------------------------------------------------------------------------------------------------------
# eligibility helpers (record-level, gold-blind)

def plain_files(rec: dict) -> bool:
    """No rename, binary or mode-only file (COMMIT builder tightening: these rows are left out of every type)."""
    return all(f["ct"] in ("ADD", "DELETE", "MODIFY") and not f["binary"] and not f["mode_only"] and f["hunks"]
               for f in rec["files"])


def changed_lines(rec: dict) -> int:
    return rec["added"] + rec["removed"]


# ---------------------------------------------------------------------------------------------------------------
# diff views and the 1.3 shortening rule

def header_lines(f: dict) -> list[str]:
    a = "--- /dev/null" if f["ct"] == "ADD" else f"--- a/{f['old'] or f['path']}"
    b = "+++ /dev/null" if f["ct"] == "DELETE" else f"+++ b/{f['new'] or f['path']}"
    return [a, b]


def _line(k: str, t: str) -> str:
    return k + t


def shorten(rec: dict, budget_tok: int, decisive=frozenset(), file_ids=None, view: str = "full"):
    """1.3 rule: file headers never dropped; decisive lines never cut; other lines cut from the end of the longest
    hunks first (water level over hunk lengths); each cut run becomes one marker. Returns shown structure or None
    when headers + decisive lines alone pass the budget."""
    fids = list(range(len(rec["files"]))) if file_ids is None else list(file_ids)
    hunks = []  # (fi, hi, [(li, k, t)])
    fixed = 0
    for fi in fids:
        f = rec["files"][fi]
        if view == "full":
            fixed += sum(len(x) + 1 for x in header_lines(f))
        else:
            fixed += len(ROUTE_SEP) + 1
        for hi, h in enumerate(f["hunks"]):
            if h["header"]:
                fixed += len(h["header"]) + 1
            hunks.append((fi, hi, [(li, k, t) for li, (k, t) in enumerate(h["lines"])]))
    budget = budget_tok * CHARS_PER_TOK

    def cost(level):
        tot = fixed
        keep = []
        for fi, hi, lines in hunks:
            nd = [x for x in lines if (fi, hi, x[0]) not in decisive]
            kept_nd = {x[0] for x in nd[:level]}
            kl = [x for x in lines if (fi, hi, x[0]) in decisive or x[0] in kept_nd]
            tot += sum(len(t) + 2 for _, _, t in kl)
            if len(kl) < len(lines):
                tot += 30 * (1 + sum(1 for a, b in zip(kl, kl[1:]) if b[0] != a[0] + 1))
            keep.append(kl)
        return tot, keep

    hi_lvl = max((len(x[2]) for x in hunks), default=0)
    tot, keep = cost(hi_lvl)
    if tot > budget:
        lo, hi_ = 0, hi_lvl
        while lo < hi_:
            mid = (lo + hi_ + 1) // 2
            if cost(mid)[0] <= budget:
                lo = mid
            else:
                hi_ = mid - 1
        tot, keep = cost(lo)
        if tot > budget:
            return None
    shown = {"view": view, "files": []}
    idx = 0
    for fi in fids:
        f = rec["files"][fi]
        sf = {"fi": fi, "path": f["path"], "old": f["old"], "new": f["new"], "ct": f["ct"], "hunks": []}
        for hi, h in enumerate(f["hunks"]):
            kl = keep[idx]
            idx += 1
            n = len(h["lines"])
            items, prev = [], -1
            for li, k, t in kl:
                if li != prev + 1:
                    items.append(("cut", li - prev - 1))
                items.append((k, t))
                prev = li
            if prev != n - 1:
                items.append(("cut", n - 1 - prev))
            sf["hunks"].append({"hi": hi, "header": h["header"], "items": items})
        shown["files"].append(sf)
    return shown


def render_shown(shown: dict) -> str:
    out = []
    for sf in shown["files"]:
        if shown["view"] == "full":
            out.extend(header_lines(sf))
        else:
            out.append(ROUTE_SEP)
        for h in sf["hunks"]:
            if h["header"]:
                out.append(h["header"])
            for k, t in h["items"]:
                out.append(CUT.format(n=t) if k == "cut" else _line(k, t))
    return "\n".join(out)


def shown_lines(shown: dict):
    """(file path, kind, text) of every shown changed or context line."""
    for sf in shown["files"]:
        for h in sf["hunks"]:
            for k, t in h["items"]:
                if k != "cut":
                    yield sf["path"], k, t


def numstat_block(rec: dict, file_ids=None) -> str:
    fids = list(range(len(rec["files"]))) if file_ids is None else list(file_ids)
    lines = ["Stats (added, removed, path):"]
    tot = 0
    for fi in fids:
        f = rec["files"][fi]
        lines.append(f"{f['added']}\t{f['removed']}\t{f['path']}")
        tot += f["added"] + f["removed"]
    lines.append(f"Total: {len(fids)} files changed, {tot} changed lines")
    return "\n".join(lines)


def fence(body: str, tag: str) -> str:
    return f"```{tag}\n{body}\n```"


# ---------------------------------------------------------------------------------------------------------------
# independent state parser (G3): reads fences from the rendered state only

FENCE_RE = re.compile(r"```([a-z]+)\n(.*?)\n```", re.S)


def parse_state(state: str) -> dict:
    out = {"stats": None, "total": None, "diffs": [], "pre": state, "fences": []}
    first = None
    for m in FENCE_RE.finditer(state):
        tag, body = m.group(1), m.group(2)
        out["fences"].append((m.start(), tag, body))
        if first is None:
            first = m.start()
        if tag == "stats":
            rows, total = [], None
            for ln in body.split("\n")[1:]:
                if ln.startswith("Total: "):
                    mm = re.fullmatch(r"Total: (\d+) files changed, (\d+) changed lines", ln)
                    total = (int(mm.group(1)), int(mm.group(2))) if mm else None
                else:
                    a, r, p = ln.split("\t", 2)
                    rows.append((int(a), int(r), p))
            out["stats"], out["total"] = rows, total
        elif tag == "diff":
            out["diffs"].append((m.start(), parse_diff_text(body)))
    return out


def parse_diff_text(body: str) -> dict:
    """Files (headers, lines) or route segments, by a line scan."""
    files, segs = [], []
    cur, seg = None, None
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("--- ") and i + 1 < len(lines) and lines[i + 1].startswith("+++ "):
            a, b = ln[4:], lines[i + 1][4:]
            old = None if a == "/dev/null" else a[2:]
            new = None if b == "/dev/null" else b[2:]
            cur = {"old": old, "new": new, "path": new or old, "lines": [], "segments": [[]]}
            files.append(cur)
            i += 2
            continue
        if ln == ROUTE_SEP:
            seg = {"lines": [], "segments": [[]]}
            segs.append(seg)
            i += 1
            continue
        tgt = cur if cur is not None else seg
        if tgt is None:
            i += 1
            continue
        if ln.startswith("@@ "):
            tgt["segments"].append([])
            tgt.setdefault("hunk_headers", []).append(ln)
        elif CUT_RE.match(ln):
            tgt["segments"].append([])
        else:
            k = ln[:1] if ln[:1] in "+-" else " "
            t = ln[1:]
            tgt["lines"].append((k, t))
            tgt["segments"][-1].append((k, t))
        i += 1
    return {"files": files, "route_files": segs}


# ---------------------------------------------------------------------------------------------------------------
# message words (6.1) and code names

OUTER = ",;:!?()[]{}\"'"


def msg_words(msg: str) -> list[tuple[str, int]]:
    """Whitespace-separated words with outer punctuation trimmed (one final '.'), with char start."""
    out = []
    for m in re.finditer(r"\S+", msg):
        w, s = m.group(0), m.start()
        while w and w[0] in OUTER:
            w, s = w[1:], s + 1
        while w and w[-1] in OUTER:
            w = w[:-1]
        if w.endswith("."):
            w = w[:-1]
        while w and w[-1] in OUTER:
            w = w[:-1]
        if w:
            out.append((w, s))
    return out


def code_shaped(w: str) -> bool:
    if len(w) >= 2 and w[0] == "`" and w[-1] == "`":
        return True
    if "/" in w or "_" in w:
        return True
    if re.search(r"[a-z][A-Z]", w):
        return True
    return bool(re.search(r"[A-Za-z0-9]\.[A-Za-z0-9]", w))


def code_names(msg: str) -> list[str]:
    return [w.strip("`") for w, _ in msg_words(msg) if code_shaped(w)]


def touched(name: str, lines: list[str]) -> bool:
    """Whole-name, case-insensitive occurrence: no letter, digit or _ directly before or after (6.1)."""
    pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])", re.I)
    return any(pat.search(x) for x in lines)


# ---------------------------------------------------------------------------------------------------------------
# M hits mapped to message words; mention-state filter (1.4)

def word_index(msg: str):
    """Words (lower-case, outer punctuation trimmed) and a char -> word index map."""
    ws = msg_words(msg)
    starts = [s for _, s in ws]
    ends = [s + len(w) for w, s in ws]
    return [w.lower() for w, _ in ws], starts, ends


def hit_word(pos: int, starts, ends) -> int | None:
    for i, (s, e) in enumerate(zip(starts, ends)):
        if s <= pos < e:
            return i
    return None


_CUES = [c.split() for c in L.CUES]


def cue_near(words: list[str], i: int, cues=None, w: int = L.CUE_WINDOW) -> bool:
    cues = _CUES if cues is None else cues
    lo, hi = i - w, i + w
    for ent in cues:
        n = len(ent)
        for j in range(max(0, lo), min(len(words), hi + 1) - n + 1):
            if j <= i < j + n:
                continue
            if words[j:j + n] == ent and j >= lo and j + n - 1 <= hi:
                return True
    return False


def mention_classes(msg: str, hits: dict) -> dict | None:
    """hits: entity -> [char positions of its M hits]. Returns entity -> 'changed' | 'not_changed', or None when an
    entity's hits get different classes (row dropped)."""
    words, starts, ends = word_index(msg)
    out = {}
    for ent, poss in hits.items():
        cls = set()
        for p in poss:
            wi = hit_word(p, starts, ends)
            if wi is None:
                return None
            cls.add("not_changed" if cue_near(words, wi) else "changed")
        if len(cls) != 1:
            return None
        out[ent] = cls.pop()
    return out


def m_hits(msg: str, token_sets: dict) -> dict:
    """entity -> list of (token, char pos) where an M token of the message equals a token of the entity set."""
    toks = C.m_tokens(msg, with_pos=True)
    out = {}
    for ent, ts in token_sets.items():
        hs = [(t, p) for t, p in toks if t in ts]
        if hs:
            out[ent] = hs
    return out


def reader_conflict(msg: str, printed: dict, hits: dict) -> bool:
    """Reader agreement filter (R4-04): True (drop) when a message part equals or nearly matches a part of an
    entity's printed words and that message part is not an M hit of that entity."""
    mparts = C.parts(msg, with_pos=True)
    for ent, words in printed.items():
        pw = set()
        for w in words:
            pw.update(C.parts(w))
        hit_pos = {p for _, p in hits.get(ent, [])}
        hit_tok = {t for t, _ in hits.get(ent, [])}
        for p, pos, ph in mparts:
            if ph:
                continue
            if any(p == q or C.near_miss(p, q) for q in pw):
                if not (p in hit_tok and pos in hit_pos):
                    return True
    return False


def unescape_state(s: str) -> str:
    return html.unescape(s)
