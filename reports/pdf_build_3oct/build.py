#!/usr/bin/env python3
"""Build /Users/aryamahadik/Documents/jev/reports/OpenDecide_Full_Status_3Oct.pdf

Copy of the 1 Oct builder (reports/pdf_build_1oct/build.py), rewritten for 3 Oct 2026 (evening EDT): a one-page
plain-language summary for the founder, the 3 Oct status, the CURRENT owner goal (4B only, plan C), a compact history
of 28 Sep - 2 Oct, what happened on 2-3 Oct (fix2 outcome, A10 C1 ship, step B, A12, ejs-5, JevBench public, the
Decision Index sample, the deep research, spec/recipe v4, the sealed suite, A13-A16.1, the data build, the replay read),
every comparison with Jev, the projections after C round 1 (EST), the knowledge-gap plan, the dated roadmap and money,
risks and open issues, and how to verify. Superseded plans are marked SUPERSEDED.

Inputs: reports/pdf_build_3oct/FACTS_3oct.md and MAP.md (read by the writer, not by this builder), the allowed
aggregate files listed in section 11.5, git, and the orchestrator facts (tag ORCH, typed in here).

SAFETY GUARDS (kept from the 1 Oct builder, plus new ones):
  1. Read-only on the project. Every open() (builtins and io) is wrapped: a write anywhere under the project root other
     than reports/pdf_build_3oct/ or the output PDF stops the build.
  2. Forbidden-path guard: any path matching sealed_nd, sealed_brief, ohs3 (any case), prep89, external_quarantine,
     longbench_v2, ejs-5 gold, .env, session folders (/tmp/claude-*, ~/.claude/projects) stops the build. Every open,
     stat, glob and sha goes through it. The sealed suite appears only as the counts and domain IDS in PREREG A15.
  3. Git only, read-only subcommands only (rev-parse, log, show, diff, status, worktree list, ls-files), with
     GIT_OPTIONAL_LOCKS=0. No other process is started. No Modal, gcloud, ssh, OpenRouter, network or paid call
     (logs/budget_tracker.py is NOT run: it calls `modal billing`). Billing figures are typed in with a sum assert.
  4. gate_dev.py is imported read-only (sys.dont_write_bytecode = True; SystemExit caught; import failure tolerated).
  5. Fault-tolerant readers: a missing input is skipped with a note and listed (MISSING_INPUTS) in section 11; the build
     never crashes on a moved file.
  6. Embedded Arial / Courier New TrueType fonts; BAD_GLYPHS (characters missing from Arial) and SPLIT_WORDS (a word
     wider than its table cell) are reported at the end; long-cell warning.
  7. md() escapes & < > and colours the tags ORCH / LIVE-ORCH / LIVE / EST.
  8. Two-pass build for "Page N of M" with a page-count equality check; TOC and PDF outline via afterFlowable.
  9. Report-only tests stay aggregates only (no per-item file of the Decision Index or ejs-5 is opened). No new lineage
     line and no absolute data claims (owner, 3 Oct about 03:10 UTC). No secrets (account names only).
Temporary files and the matplotlib cache live in reports/pdf_build_3oct/ (TMPDIR and MPLCONFIGDIR are set there).

Run:  python3 /Users/aryamahadik/Documents/jev/reports/pdf_build_3oct/build.py
"""
import builtins
import copy
import datetime as dt
import glob
import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/aryamahadik/Documents/jev")
L = ROOT / "opendecide-data/lean"
BENCH = ROOT / "bench"
REP = ROOT / "reports"
SCR = REP / "pdf_build_3oct"
OUT = REP / "OpenDecide_Full_Status_3Oct.pdf"
OLD_PDF = REP / "OpenDecide_Full_Status_1Oct.pdf"
OLDER_PDF = REP / "OpenDecide_Full_Status_30Sep.pdf"
UTC = dt.timezone.utc
assert SCR.name == "pdf_build_3oct" and OUT.name == "OpenDecide_Full_Status_3Oct.pdf", (SCR, OUT)
assert OUT not in (OLD_PDF, OLDER_PDF) and OUT.parent == REP

# temporary files and the matplotlib cache stay inside the build folder (never in session folders)
(SCR / "tmp").mkdir(exist_ok=True)
os.environ["TMPDIR"] = str(SCR / "tmp")
tempfile.tempdir = str(SCR / "tmp")
os.environ["MPLCONFIGDIR"] = str(SCR / "mplconfig")

# ----------------------------------------------------------------------------------------------- safety guards
FORBIDDEN = re.compile(r"sealed_nd|sealed_brief|ohs3|/prep89(/|$)|external_quarantine|longbench_v2|ejs5/.*gold|"
                       r"(^|/)\.env($|[./])|/tmp/claude-|/\.claude/projects", re.I)
GUARD = {"opens": 0}


def _abs(p):
    s = os.path.abspath(os.fspath(p))
    return s.decode(errors="replace") if isinstance(s, bytes) else s


def safe(p):
    """Every path the builder touches passes here; a forbidden path stops the build."""
    s = _abs(p)
    if FORBIDDEN.search(s):
        raise SystemExit(f"SAFETY STOP: the builder tried to touch a forbidden path: {s}")
    return Path(s)


def _check_write(s, mode):
    if any(c in str(mode) for c in "wax+"):
        if (s + "/").startswith(str(ROOT) + "/") and not (s.startswith(str(SCR) + "/") or s == str(OUT)):
            raise SystemExit(f"SAFETY STOP: write outside reports/pdf_build_3oct/ and the output PDF: {s}")


_ORIG_OPEN = builtins.open


def _guarded_open(file, mode="r", *a, **k):
    if not isinstance(file, int):
        s = _abs(file)
        if FORBIDDEN.search(s):
            raise SystemExit(f"SAFETY STOP: open() of a forbidden path: {s}")
        _check_write(s, mode)
        GUARD["opens"] += 1
    return _ORIG_OPEN(file, mode, *a, **k)


builtins.open = _guarded_open
io.open = _guarded_open

ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
GIT_OK = {"rev-parse", "log", "show", "diff", "status", "worktree", "ls-files"}


def _git_run(args):
    if not args or args[0] not in GIT_OK or (args[0] == "worktree" and list(args[1:]) != ["list"]):
        raise SystemExit(f"SAFETY STOP: git subcommand not allowed: {args}")
    for a in args:
        if FORBIDDEN.search(str(a)):
            raise SystemExit(f"SAFETY STOP: git argument names a forbidden path: {a}")
    try:
        return subprocess.run(["git", "-C", str(ROOT), "--no-pager", *args], capture_output=True, env=ENV, timeout=90)
    except Exception as e:  # noqa
        return None


def git(*args):
    r = _git_run(list(args))
    return r.stdout.decode(errors="replace").strip() if r is not None else "(git failed)"


def git_bytes(*args):
    r = _git_run(list(args))
    return r.stdout if (r is not None and r.returncode == 0) else None


def git_rc(*args):
    r = _git_run(list(args))
    return r.returncode if r is not None else -1


# ----------------------------------------------------------------------------------------------- fonts
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_LEFT  # noqa: E402
from reportlab.lib.fonts import addMapping  # noqa: E402
from reportlab.lib.pagesizes import landscape, letter  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, NextPageTemplate, PageBreak,  # noqa: E402
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents  # noqa: E402

FD = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Arial", FD + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", FD + "Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", FD + "Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", FD + "Arial Bold Italic.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD + "Courier New.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", FD + "Courier New Bold.ttf"))
for fam, n, b, i, bi in (("Arial", "Arial", "Arial-Bold", "Arial-Italic", "Arial-BoldItalic"),
                         ("Mono", "Mono", "Mono-Bold", "Mono", "Mono-Bold")):
    addMapping(fam, 0, 0, n); addMapping(fam, 1, 0, b); addMapping(fam, 0, 1, i); addMapping(fam, 1, 1, bi)

try:
    from fontTools.ttLib import TTFont as _FT
    CMAP = set(_FT(FD + "Arial.ttf").getBestCmap().keys())
except Exception:  # fontTools missing: skip the glyph check
    CMAP = None
BAD_GLYPHS = set()
SPLIT_WORDS = []  # (table, word) pairs where a word is wider than its table cell
MISSING_INPUTS = []  # inputs that were not found (skipped gracefully)

# ----------------------------------------------------------------------------------------------- readers (guarded)


def exists(p):
    return safe(p).exists()


def mtime(p):
    try:
        return dt.datetime.fromtimestamp(os.stat(safe(p)).st_mtime, UTC)
    except FileNotFoundError:
        return None


def birth(p):
    try:
        return dt.datetime.fromtimestamp(os.stat(safe(p)).st_birthtime, UTC)
    except Exception:
        return None


def sha256(p):
    h = hashlib.sha256()
    with open(safe(p), "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def sha_or_none(p):
    try:
        return sha256(p)
    except FileNotFoundError:
        MISSING_INPUTS.append(str(p))
        return None


def nlines(p):
    n = 0
    with open(safe(p), "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            n += b.count(b"\n")
    return n


def jload(p, note=True):
    try:
        return json.loads(safe(p).read_text())
    except FileNotFoundError:
        if note:
            MISSING_INPUTS.append(str(p))
        return None
    except Exception as e:  # noqa
        MISSING_INPUTS.append(f"{p} (unreadable: {e})")
        return None


def txt(p, note=True):
    try:
        return safe(p).read_text(errors="replace")
    except FileNotFoundError:
        if note:
            MISSING_INPUTS.append(str(p))
        return ""


def gl(pattern):
    safe(pattern.split("*")[0])
    return sorted(str(safe(x)) for x in glob.glob(pattern))


def hm(t):
    return t.strftime("%d %b %H:%M UTC") if t else "missing"


def hmu(t):
    return t.strftime("%-d %b %H:%M") if t else "?"


def edt(t):
    return (t - dt.timedelta(hours=4)).strftime("%a %-d %b %-I:%M %p") if t else "?"


def fmt(n):
    return f"{n:,}"


def pct(x, d=1):
    return f"{100 * x:.{d}f}"


from decimal import Decimal, ROUND_HALF_UP  # noqa: E402


def r1(x, sign=False):
    """One decimal, half away from zero (so -17.65 -> -17.7, 55.95 -> 56.0, as the source files print them)."""
    d_ = Decimal(repr(round(float(x), 6))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{d_:+}" if sign else f"{d_}"


# ----------------------------------------------------------------------------------------------- live checks: git
LIVE = {"build": dt.datetime.now(UTC)}
LIVE["branch"] = git("rev-parse", "--abbrev-ref", "HEAD")
LIVE["head"] = git("rev-parse", "HEAD")
LIVE["tag"] = git("rev-parse", "final-frozen")
LIVE["gitlog"] = git("log", "--format=%h %ad %s", "--date=iso", "-3").splitlines()
LIVE["worktrees"] = [x for x in git("worktree", "list").splitlines() if x.strip()]
FROZEN_FILES = ["train_decoder.py", "decoder_io.py", "prism_x.py", "writeblock.py"]
LIVE["frozen_diff"] = git("diff", "--no-ext-diff", "--stat", "final-frozen", "--",
                          *[f"opendecide-data/lean/{f}" for f in FROZEN_FILES], "opendecide-data/lean/runs/q35_4b_main.json")
EXPECT_TAG = {  # the code C1 was trained with (tag final-frozen 82b07d4; = C1's train_meta)
    "train_decoder.py": "ebdf046d1a9b517ec78969de70d1ebaa4200f4e00e7eb911b79a142841403f3c",
    "decoder_io.py": "8ba8ff4fb35389c76bb2d0851f66ef4822059d43fe4bef1ca582fcf21c5755cc",
    "prism_x.py": "3c4425bfde62182c997960ef68d43232df65ba28031608acde0b9dc8ba87b4fe",
    "writeblock.py": "ccc154a171bb20b5b6b8301f42bc9d36e70e2120bff88dbe89580d340bb4c94c",
}
LIVE["sha"] = {f: sha_or_none(L / f) for f in FROZEN_FILES}
LIVE["tag_sha"] = {}
for f in FROZEN_FILES:
    b_ = git_bytes("show", f"final-frozen:opendecide-data/lean/{f}")
    LIVE["tag_sha"][f] = hashlib.sha256(b_).hexdigest() if b_ is not None else None
for extra in ("runs/q35_4b_main.json", "runs/q35_4b_c_r1.json", "modal_od.py", "od_gcp.py", "gate_dev.py"):
    LIVE["sha"][extra] = sha_or_none(L / extra)
_b = git_bytes("show", "HEAD:opendecide-data/lean/modal_od.py")
LIVE["modal_head_sha"] = hashlib.sha256(_b).hexdigest() if _b is not None else None
LIVE["modal_status"] = git("status", "--porcelain", "--", "opendecide-data/lean/modal_od.py")[:2].strip()
LIVE["modal_diffstat"] = (git("diff", "--no-ext-diff", "--stat", "HEAD", "--", "opendecide-data/lean/modal_od.py").splitlines()
                          or [""])[-1].strip()
LIVE["modal_mtime"] = mtime(L / "modal_od.py")
LIVE["prereg_status"] = git("status", "--porcelain", "--", "opendecide-data/lean/PREREG_FINAL.md")
try:
    _du = shutil.disk_usage(str(ROOT))
    LIVE["disk_free_gib"], LIVE["disk_used_pct"] = _du.free / 2 ** 30, 100 * _du.used / _du.total
except Exception:  # noqa
    LIVE["disk_free_gib"], LIVE["disk_used_pct"] = None, None

# amendments and result commits: commit time (git) and text in HEAD's PREREG_FINAL.md
PREREG = txt(L / "PREREG_FINAL.md")
PREREG_HEAD = git("show", "HEAD:opendecide-data/lean/PREREG_FINAL.md")
PREREG_DRAFT = "DRAFT" in "\n".join(PREREG.splitlines()[:5])
AMEND = [("A8′", "c35de00", "Amendment A8-prime (A8′) (", "C4 = fix2 top-up, pre-checks, one ship look"),
         ("A10", "132cd2a", "Amendment A10 (", "owner override: C1 is the shipped 4B"),
         ("A11", "c11e4a9", "Amendment A11 (", "step B, weight softening of C1"),
         ("A12", "86f59dd", "Amendment A12 (", "OHS-1 + OHS-2 Jev yardstick; they become practice sets"),
         ("A13", "8f1a9eb", "Amendment A13 (", "Decision Index sample on C1, report-only"),
         ("A14", "a79e5d4", "Amendment A14 (", "sealed new-domains suite build rules"),
         ("A15", "3abd721", "Amendment A15 (", "sealed suite v2 frozen (sha256, counts, adjacency by id)"),
         ("A16", "27d8b0a", "Amendment A16 (", "C round-1 plan (spec, recipe, config, seed, sizes, gate)"),
         ("A16.1", "18c024c", "Amendment A16.1 (", "tool versions for A16's rulings; EDOS and choice-row rules"),
         ("A16.2", "6d79bf2", "Amendment A16.2 (", "round-1 Modal launcher pinned; plan files, tools and tests committed")]


def ctime(commit):
    out = git("show", "-s", "--format=%h %ct", commit).split()
    if len(out) >= 2 and out[-1].isdigit():
        return out[0], dt.datetime.fromtimestamp(int(out[-1]), UTC)
    return commit, None


AM = {}
for name, cid, marker, what in AMEND:
    h_, t_ = ctime(cid)
    m_ = re.search(re.escape(marker) + r"(\d+ Oct 2026), (\d\d:\d\d) UTC", PREREG)
    stated = None
    if m_:
        try:
            stated = dt.datetime.strptime(f"{m_.group(1)} {m_.group(2)}", "%d %b %Y %H:%M").replace(tzinfo=UTC)
        except Exception:  # noqa
            stated = None
    AM[name] = {"commit": h_, "time": t_, "in_head": marker in PREREG_HEAD, "stated": stated, "what": what}
RESULT_COMMITS = [("9a04df1", "ejs-5 pre-registration + kit (convert, run, score, 15 tests)"),
                  ("065191c", "ejs-5 note: runs on the backup L4 od-l4b (od-l4 out of stock)"),
                  ("32ee1f9", "ejs-5 results: C1 54.1%, 4B-E 54.5% vs Jev 58.5%"),
                  ("599c513", "step B result: no softened C1 passes; keep C1"),
                  ("629a9f4", "A12 result: C1 vs Jev OHS-1 −1.2, OHS-2 −0.6 (ties)")]
RC = {cid: ctime(cid) for cid, _ in RESULT_COMMITS}


def _block(start, end=None):
    i = PREREG.find(start)
    if i < 0:
        return ""
    j = PREREG.find(end, i + 1) if end else -1
    return PREREG[i:j] if j > 0 else PREREG[i:]


A15B = _block("**Amendment A15 (", "**Amendment A16 (")
A16B = _block("**Amendment A16 (", "**Amendment A16.1 (")
A161B = _block("**Amendment A16.1 (", "**Amendment A16.2 (")
A162B = _block("**Amendment A16.2 (")
A10B = _block("**Amendment A10 (", "**Amendment A11 (")
A15_CHECKS = {k: (k in A15B) for k in ("7,302 items", "2,988 select and 4,314 confirm", "6,205 items in 8 domains",
                                      "2,542 select / 3,663 confirm", "3,446 items (55.5%)", "2,759 items",
                                      "16.1%", "P 600", "B1 298", "B2 199")}
A15_OK = all(A15_CHECKS.values())
A10_OK = all(k in A10B for k in ("87 of 252 pairs (34.52%)", "+0.40 pp [−5.86, +6.75]", "8.86% vs REF 5.68%",
                                 "7 golden_train units"))

# A16 / A16.1 pins (working copy vs the committed text)
PINS = [("c_spec/C_DATA_SPEC.md", "4ca129963bef3e0a", "data spec v4", "A16"),
        ("c_spec/C_TRAIN_RECIPE.md", "f4b7915088942f9b", "training recipe v4", "A16"),
        ("c_spec/ADDENDUM_research.md", "0da2e8341929597e", "research addendum", "A16"),
        ("runs/q35_4b_c_r1.json", "f3bb379e", "round-1 config", "A16"),
        ("train_decoder.py", "c2c2d1d6", "trainer (A4/F2 changes, default-off)", "A16"),
        ("decoder_io.py", "908c08d7", "readout (default-off changes)", "A16"),
        ("c_build/replay_sample.py", "5735ca3eb673895d", "replay sampler", "A16.1"),
        ("c_src/common/denylist.py", "e268d5667f181bba", "deny-list v1.2", "A16.1"),
        ("c_src/common/deny_aliases.json", "40eeb47e2f379ea8", "deny aliases v1.1", "A16.1"),
        ("c_src/common/negcount.py", "79368f465d438617", "negation counter v1.1", "A16.1")]
PIN = []
for rel, pref, what, am in PINS:
    s_ = sha_or_none(L / rel)
    blk = A16B if am == "A16" else A161B
    tracked = git_rc("ls-files", "--error-unmatch", f"opendecide-data/lean/{rel}") == 0
    st_ = git("status", "--porcelain", "--", f"opendecide-data/lean/{rel}")[:2].strip()
    PIN.append({"rel": rel, "pref": pref, "what": what, "am": am, "sha": s_,
                "match": bool(s_) and s_.startswith(pref), "in_text": pref in blk,
                "git": ("tracked, unchanged" if tracked and not st_ else ("tracked, CHANGED (uncommitted)" if tracked
                                                                          else "UNTRACKED"))})
PINS_OK = all(p["match"] and p["in_text"] for p in PIN)
N_UNTRACKED = sum(1 for p in PIN if p["git"] == "UNTRACKED")
N_UNCOMMITTED = sum(1 for p in PIN if "CHANGED" in p["git"])
# the Modal launcher that will run round 1: changed vs HEAD? pinned anywhere in A16 / A16.1? (LIVE)
_msha = LIVE["sha"].get("modal_od.py") or ""
MODAL_CHANGED = bool(_msha) and _msha != (LIVE["modal_head_sha"] or "")
MODAL_PINNED = bool(_msha) and (_msha[:8] in A16B or _msha[:8] in A161B or _msha[:8] in A162B)
N_CODE_UNCOMMITTED = N_UNCOMMITTED + (1 if MODAL_CHANGED and LIVE["modal_status"] else 0)
# state before A16.2 (6d79bf2): 3 code files changed but uncommitted (train_decoder.py, decoder_io.py, modal_od.py) and
# 8 pinned plan files untracked; A16.2 committed them all and pinned the launcher. LIVE decides which wording prints.
_ns = {}
for _ln in git("diff", "--name-status", "6d79bf2^", "6d79bf2", "--", "opendecide-data/lean/").splitlines():
    _pp = _ln.split("\t")
    if len(_pp) == 2 and _pp[1].startswith("opendecide-data/lean/"):
        _ns[_pp[1][len("opendecide-data/lean/"):]] = _pp[0]
PRE_A162 = (sum(1 for f in ("train_decoder.py", "decoder_io.py", "modal_od.py") if _ns.get(f) == "M"),
            sum(1 for p in PIN if _ns.get(p["rel"]) == "A")) if _ns else (3, 8)  # LIVE from git; (3, 8) if git fails
PLAN_COMMITTED = (N_UNTRACKED == 0 and N_CODE_UNCOMMITTED == 0 and MODAL_PINNED and AM["A16.2"]["in_head"])
A162_REF = f"`{AM['A16.2']['commit']}`, A16.2, {hm(AM['A16.2']['time'])}"

# data (golden v14 = C1's training set and C's replay pool)
DATA_FILES = [("data/v14_parts/golden_train.jsonl", "ff7a395bc9b501ac", 501732),
              ("data/v14_parts/golden_relations.jsonl", "072ee6c4", 74094)]
LIVE["data"] = {}
for rel, pref, rows in DATA_FILES:
    p = L / rel
    if exists(p):
        LIVE["data"][rel] = {"sha": sha256(p), "lines": nlines(p), "expect_pref": pref, "expect_rows": rows,
                             "mode": oct(os.stat(safe(p)).st_mode)[-3:]}
    else:
        MISSING_INPUTS.append(str(p))
CFG4 = jload(L / "runs/q35_4b_main.json") or {}
GC_TXT = txt(L / "data/v14_parts/GOLDEN_CARD.md")
_m = re.search(r"\| replay \(v13 clean pool\) \| ([\d,]+) \|", GC_TXT)
GC_REPLAY = _m.group(1) if _m else "41,918"
GC_SOFT_LATER = "4B teacher soft labels" in GC_TXT
CFGC = jload(L / "runs/q35_4b_c_r1.json") or {}

# ----------------------------------------------------------------------------------------------- the 4B main run (C1)
SEGS = []
for lp in sorted((p for p in gl(str(L / "logs/main4b_seg*.log")) if re.fullmatch(r"main4b_seg\d+\.log", os.path.basename(p))),
                 key=lambda p: int(re.search(r"seg(\d+)\.log", p).group(1))):
    recs, ckpts, stopped, alerts, errs = [], [], None, 0, 0
    resumed, checks, account, completed, cancelled = None, None, None, False, None
    for line in open(lp, errors="replace"):
        if "Received a cancellation signal" in line and not cancelled:
            m = re.search(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)", line)
            cancelled = m.group(1).replace("T", " ") + " UTC" if m else "yes"
        if "app no longer running" in line or "App completed" in line:
            completed = True
        if "ALERT" in line:
            alerts += 1
        if re.search(r"Traceback|\bNaN\b|\bnan\b|Error", line):
            errs += 1
        m = re.search(r"modal\.com/apps/([^/\s]+)/", line)
        if m and not account:
            account = m.group(1)
        s = line.strip()
        if not s.startswith("{"):
            continue
        try:
            d = json.loads(s)
        except Exception:
            continue
        if "loss" in d and "step" in d:
            recs.append(d)
        elif "checkpoint" in d:
            ckpts.append(d)
        elif "stopped_at_step" in d:
            stopped = d["stopped_at_step"]
        elif "resumed_at_step" in d:
            resumed, checks = d["resumed_at_step"], d.get("checks")
    SEGS.append({"path": lp, "name": os.path.basename(lp), "recs": recs, "ckpts": ckpts, "stopped": stopped,
                 "alerts": alerts, "errs": errs, "mtime": mtime(lp), "birth": birth(lp), "resumed": resumed,
                 "checks": checks, "account": account, "completed": completed, "cancelled": cancelled})
_l5 = L / "logs/main4b_seg5_launch.log"
for sg in SEGS:
    if sg["account"] is None and sg["name"] == "main4b_seg5.log" and exists(_l5):
        m = re.search(r"modal\.com/apps/([^/\s]+)/", txt(_l5))
        if m:
            sg["account"] = "atmosphor" if m.group(1) == "admin-22544" else m.group(1)
ALLREC = {}
for sg in SEGS:
    for r in sg["recs"]:
        ALLREC[r["step"]] = r
REC = [ALLREC[k] for k in sorted(ALLREC)]
LAST = REC[-1] if REC else {"step": 0, "of": 30457, "lr": 0, "gn_med": 0}
TOTAL_STEPS = LAST.get("of", 30457)
for sg in SEGS:
    r = sg["recs"]
    sg["sps"] = ((r[-1]["min"] - r[0]["min"]) * 60 / (r[-1]["step"] - r[0]["step"])) if len(r) > 5 else None
if not SEGS:
    MISSING_INPUTS.append(str(L / "logs/main4b_seg*.log"))


def seg_state(sg):
    if sg.get("cancelled"):
        last_ck = max((c["next_step"] for c in sg["ckpts"]), default=0)
        return f"cancelled at {sg['cancelled']} (laptop lost network); signal save next_step {fmt(last_ck)}"
    if sg["stopped"] is not None:
        return f"stopped (planned) at step {fmt(sg['stopped'])}"
    if sg["completed"]:
        return ("finished the run (last logged step " + fmt(sg["recs"][-1]["step"]) + " of " + fmt(sg["recs"][-1]["of"]) + ")"
                if sg["recs"] and sg["recs"][-1]["step"] + 50 > sg["recs"][-1]["of"] else "app completed")
    return f"last logged step {fmt(sg['recs'][-1]['step']) if sg['recs'] else '–'}"


ALERTS = sum(sg["alerts"] for sg in SEGS)

# gate job 1 (1 Oct): look files
G4 = L / "logs/gate4b"
GSUM = jload(G4 / "summary.json") or {}
GSHIP = jload(G4 / "look_ship1.json") or {}
GPAR = jload(G4 / "look_refparity1.json") or {}
_prim = GSHIP.get("primary", {})
_eq = GSHIP.get("equiv_flip", {})

# Mac backup of C1 (one copy per model)
BK = ROOT / "backups/modal_models/q35_4b_main500k"
BK_EXPECT = {".": "507d1c29", "snaps/s025888": "a16f4b08", "snaps/s027411": "5433a908", "snaps/s028934": "9fed952c"}
BKSHA = {}
for sub, pref in BK_EXPECT.items():
    f = BK / sub / "adapter_model.safetensors"
    BKSHA[sub] = (sha256(f), pref) if exists(f) else (None, pref)
    if not exists(f):
        MISSING_INPUTS.append(str(f))
BKMETA = jload(BK / "train_meta.json") or {}
BK_CODE_OK = bool(BKMETA) and all(BKMETA.get("code", {}).get(f[:-3]) == EXPECT_TAG[f] for f in FROZEN_FILES)
BK_DATA_OK = bool(BKMETA) and [x[:16] for x in BKMETA.get("data", [])] == ["ff7a395bc9b501ac", "072ee6c45f3f246c"]
BK_OK = all(v[0] and v[0].startswith(v[1]) for v in BKSHA.values())


# definition-overwrite (redef) ASR, recomputed with score_redef.py's rule from the gate job's reads
def redef(name):
    try:
        rows_ = {json.loads(l)["id"]: json.loads(l) for l in open(safe(L / "data/eval_redef.jsonl"))}
        P_ = {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(safe(L / f"preds_eval_redef/{name}.jsonl"))}
    except Exception:
        return None
    top = lambda i: max(P_[i], key=P_[i].get)  # noqa: E731
    items = sorted({r["group_id"] for r in rows_.values()})
    k = lambda g, t: f"redef_{g.split(':')[-1]}_{t}"  # noqa: E731
    ok = [g for g in items if top(k(g, "clean")) == rows_[k(g, "clean")]["gold"]]
    asr = sum(top(k(g, "atk")) == rows_[k(g, "atk")]["meta"]["attack_target"] for g in ok)
    return {"clean": 100 * len(ok) / len(items), "asr": 100 * asr / max(1, len(ok)), "k": asr, "n": len(ok)}


REDEF = {n: redef(n) for n in ("q35_4b_main500k", "q35_4b_pxE_fresh")}

# ----------------------------------------------------------------------------------------------- security vs Jev (LIVE)
sys.dont_write_bytecode = True
sys.path.insert(0, str(L))
try:
    import gate_dev as GD  # read-only import; no bytecode written
except BaseException as e:  # noqa
    GD = None
    print("WARNING: gate_dev import failed:", e)


def wilson(k, n, z=1.959964):
    if not n:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (100 * (c - h) / d, 100 * (c + h) / d)


SEC_NAMES = [("q35_4b_main500k", "**C1** `q35_4b_main500k` (shipped; gate job 1 read)"),
             ("q35_4b_pxE_fresh", "4B-E `q35_4b_pxE_fresh` (gate job 1 read; reference)"),
             ("jev_guard", "**Jev with our guard prompt** (`jev_guard`)"),
             ("jev", "Jev, no guard (`jev`)")]
SEC, SEC_CMP = {}, {}
if GD is not None:
    for kind, fn in (("jagged", GD.jagged_units), ("opi", GD.opi_units)):
        SEC[kind] = {}
        for n_, _lbl in SEC_NAMES:
            try:
                u = fn(n_)
            except SystemExit as e:
                print("WARNING:", e)
                u = None
            if u:
                k_ = int(sum(a for a, b in u.values()))
                e_ = int(sum(b for a, b in u.values()))
                SEC[kind][n_] = {"units": u, "k": k_, "n": e_, "asr": 100 * k_ / e_ if e_ else math.nan,
                                 "ci": wilson(k_, e_), "items": len(u)}
        for c_ in ("q35_4b_main500k", "q35_4b_pxE_fresh"):
            if c_ in SEC[kind] and "jev_guard" in SEC[kind]:
                SEC_CMP[(kind, c_)] = GD.asr_compare(SEC[kind][c_]["units"], SEC[kind]["jev_guard"]["units"], "4b")


def _asr(kind, n_):
    x = (SEC.get(kind) or {}).get(n_)
    return f"{x['asr']:.1f}% ({x['k']}/{x['n']})" if x else "–"


def _asr_cmp(kind, n_):
    c = SEC_CMP.get((kind, n_))
    return f"{100 * c['diff']:+.1f} pp [{100 * c['lo']:+.1f}, {100 * c['hi']:+.1f}]" if c else "–"


# ----------------------------------------------------------------------------------------------- 3 Oct results (LIVE)
# A12: C1 vs Jev on OHS-1 + OHS-2 (aggregate result file only)
A12_TXT = txt(L / "logs/A12_ohs12_result.md")
A12 = {}
for m in re.finditer(r"\| (OHS-[12]) \(([\d,]+) base rows\) \| ([\d.]+) \| ([\d.]+) \| ([^|]+?) \| ([\d.]+) \| ([\d.]+) \| "
                     r"([\d.]+) / ([\d.]+) \|", A12_TXT):
    A12[m.group(1)] = {"n": m.group(2), "c1": m.group(3), "jev": m.group(4), "diff": m.group(5).strip(),
                       "mac_c1": m.group(6), "mac_jev": m.group(7), "br_c1": m.group(8), "br_jev": m.group(9)}
A12_OK = set(A12) == {"OHS-1", "OHS-2"}


def a12(t, k, dflt):
    return A12.get(t, {}).get(k, dflt)


def a12d(t):
    """C1 − Jev with its 95% CI, without the trailing verdict word."""
    return re.sub(r",\s*(tie|better|worse|loss)\s*$", "", a12(t, "diff", "?"))


# step B
BW = jload(L / "logs/b_wiseft_result.json") or {}
BW_C = BW.get("cands") or {}
BW_CHECKS = BW.get("checks") or []

# ejs-5 (aggregates only; the gold file is never opened)
EJ = jload(BENCH / "ejs5/runs/scores_c1_4be.json") or {}
EJ_C1 = (EJ.get("runs") or {}).get("c1_main500k") or {}
EJ_E = (EJ.get("runs") or {}).get("e4b_pxE") or {}
EJ_PUB = EJ_C1.get("published_on_same_rows") or {}


def ej_diff(run, key="PRIMARY_overall_pooled", sub=None):
    v = (run.get("vs_jev") or {}).get(key) or {}
    if sub:
        v = v.get(sub) or {}
    if "diff" not in v:
        return "–"
    return f"{100 * v['diff']:+.1f} [{100 * v['ci95'][0]:+.1f}, {100 * v['ci95'][1]:+.1f}]"


EJ_OK = bool(EJ_C1) and abs(EJ_C1.get("overall_pooled", 0) - 0.5415) < 0.001

# JevBench v1.5.4 public items, C1 (aggregates)
JB = (jload(BENCH / "runs/scores_v154_c1.json") or {}).get("runs") or {}
JB_ROWS = [("v154_q35_4b_main500k", "C1, as trained (T = 1)"),
           ("v154_whatif/v154_q35_4b_main500k_T0", "C1, committed yes/no"),
           ("v154_whatif/v154_q35_4b_main500k_band", "**C1, band edge (pre-registered readout)**"),
           ("v154_q35_4b_pxE", "4B-E, as trained"),
           ("v154_whatif/v154_q35_4b_pxE_T0", "4B-E, committed yes/no"),
           ("v154_whatif/v154_q35_4b_pxE_band", "4B-E, band edge"),
           ("jev_p1", "**Jev p1** (as returned)"), ("jev_p2", "Jev p2 (as returned)")]
JBC = JB.get("v154_whatif/v154_q35_4b_main500k_band") or {}
JBJ = JB.get("jev_p1") or {}


def jbv(k, *path):
    x = JB.get(k) or {}
    for p in path:
        x = (x or {}).get(p) if isinstance(x, dict) else None
    return x


JB_OK = bool(JBC) and abs((JBC.get("scores") or {}).get("A", 0) - 74.34) < 0.01


# JevBench v1.5.4 official board (snapshot 30 Sep): Score A = equal-weight HARMONIC mean of the 4 axes (LIVE check)
def hmean(v):
    return len(v) / sum(1.0 / x for x in v) if v and all(x > 0 for x in v) else math.nan


LB = jload(BENCH / "v154/leaderboard_v154.json") or {}
LBS = {s.get("key"): s for s in (LB.get("systems") or [])}


def lb_axes(key):
    a = (LBS.get(key) or {}).get("axes") or {}
    return [a.get(k) for k in ("intelligence", "calibration", "speed", "cost")] if a else None


_lbj = lb_axes("jev-1.13.0") or [71.99974990450261, 88.02903108992821, 83.8140999985063, 54.72500234484654]
LB_JEV_HM, LB_JEV_AM = hmean(_lbj), sum(_lbj) / 4
LB_JEV_A = ((LBS.get("jev-1.13.0") or {}).get("scores") or {}).get("A", 72.13292897895896)
_jbc_ax = JBC.get("axes") or {}
_c1v = [_jbc_ax.get(k) for k in ("intelligence", "calibration", "speed", "cost")]
C1_HM = hmean(_c1v) if all(_c1v) else math.nan
LB_HM_OK = abs(LB_JEV_HM - LB_JEV_A) < 0.01 and abs(C1_HM - (JBC.get("scores") or {}).get("A", 0)) < 0.01
LB_SC = {}
for k_, lbl_ in (("jevk5-v0.3-4b", "jevk5"), ("plumb-4b", "Plumb"), ("decider-4b-v2", "decider"), ("jev-1.13.0", "Jev")):
    v_ = lb_axes(k_)
    if v_:
        LB_SC[lbl_] = v_[2] + v_[3]
LB_DROP = {}
for k_, lbl_ in (("jevk5-v0.3-4b", "jevk5"), ("plumb-4b", "Plumb"), ("decider-4b-v2", "decider")):
    i_ = (LBS.get(k_) or {}).get("intelligence") or {}
    if "I_open" in i_ and "I_sealed" in i_:
        LB_DROP[lbl_] = i_["I_open"] - i_["I_sealed"]
# re-check of the "about 74.5 (71-77)" projection with board-like 4B speed/cost (about 93/63), calibration 83-88, I 61-75
PROJ_LO = hmean([61, min(83.1, _c1v[1] or 83.1), 93, 63])
PROJ_HI = hmean([75, 88, 93, 63])

# Decision Index sample (report-only, aggregates)
DI = jload(BENCH / "decision_index/report_sample10k.json") or {}
DI_OURS = (DI.get("ours") or {})
DI_JEV = (DI.get("jev_published_v01_full_suite") or {})
DI_AREAS = DI.get("areas") or []
DI_BENCH = [b for b in (DI.get("index_benchmarks") or []) if b.get("dataset")]
DI_UNNAMED = len([b for b in (DI.get("index_benchmarks") or []) if not b.get("dataset")])
DI_OK = abs(DI_OURS.get("index", 0) - 54.83) < 0.005 and abs(DI_JEV.get("index", 0) - 59.51) < 0.005
_board = [("Jev (v0.1, full suite)", DI_JEV.get("index", 59.51))] + [(n, s) for n, s in (DI.get("board_v01_top5") or [])]
_board.append(("**C1 (our 10K sample; not paired)**", DI_OURS.get("index", 54.83)))
DI_BOARD = sorted(_board, key=lambda x: -x[1])
DI_RANK = [i for i, (n, s) in enumerate(DI_BOARD, 1) if n.startswith("**C1")][0] if DI_BOARD else None

# replay draw (counts only) and the F2 rendered-prompt check
RW = jload(L / "c_build/replay_r1_write.json") or {}
RW1 = RW.get("round1_draw") or {}
RW2 = RW.get("round2_draw") or {}
RWD = RW.get("drops") or {}
RW_OK = RW1.get("rows") == 99069
F2L4 = jload(L / "c_build/f2_l4.json") or {}
F2MAC = jload(L / "c_build/f2_local_mac.json") or {}
F2_EQ = sum(1 for k, v in (F2L4.get("sha") or {}).items() if (F2MAC.get("sha") or {}).get(k) == v)
F2_N = len(F2L4.get("sha") or {})

# phase 1 (packs: LIVE line counts) and phase 2 (family rule sheets and generators; counts and family ids only)
PACK_FILES = ["c_src/packs/packs-1/packs.jsonl", "c_src/packs/packs-2/packs.jsonl", "c_src/packs/packs-3/packs-3.jsonl",
              "c_src/packs/packs-4/packs.jsonl"]
PACKS = {rel.split("/")[2]: (nlines(L / rel) if exists(L / rel) else None) for rel in PACK_FILES}
PACKS_N = sum(v for v in PACKS.values() if v)
FAMS = [f"F{i}" for i in range(1, 14)] + ["COMMIT"]
G0F = {f: exists(L / f"c_src/{f}/G0_FROZEN.json") for f in FAMS}
GEN = {f: exists(L / f"c_src/{f}/gen") for f in FAMS}
OUTF, OUTT = {}, {}  # production files vs test / smoke files (names marked _t, _t3, smoke, test) in c_src/<fam>/out/
for f in FAMS:
    o = safe(L / f"c_src/{f}/out")
    names = [n for _, _, fs in os.walk(o) for n in fs] if o.exists() else []
    OUTT[f] = sum(1 for n in names if re.search(r"smoke|test|_t\d*[._]", n))
    OUTF[f] = len(names) - OUTT[f]
OUT_TEST_S = ", ".join(f"{f} {n}" for f, n in OUTT.items() if n) or "none"
P2LOG = txt(L / "c_build/progress_phase2.log")
P2_GENSTART = {}
for m in re.finditer(r"(?m)^(?:\[(\w+)\] )?(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) (?:\[(\w+)\] )?(?:phase2 )?generator (?:build|phase)"
                     r"[^\n]*?start", P2LOG):
    fam = m.group(1) or m.group(3)
    P2_GENSTART.setdefault(fam, m.group(2)[11:16])
P2_TESTS = [(m.group(1), int(m.group(2))) for m in re.finditer(r"(?m)^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) \[\w+\] build test: wrote "
                                                                 r"(\d+) rows", P2LOG)]
P2_TESTS_S = (f"{len(P2_TESTS)} generator test builds (largest {max(n for _, n in P2_TESTS):,} rows, last at "
              f"{P2_TESTS[-1][0][11:16]} UTC)" if P2_TESTS else "no generator test build yet")
P2_LAST = (re.findall(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)", P2LOG) or ["?"])[-1]
F6_WORDINGS = "29 pass < 30 floor" in P2LOG
F13_LEN = "~6.0-6.5K" in P2LOG
F10_LEN = "card printed twice on choice rows" in P2LOG

# knowledge-gap research (plan file, if it exists)
KG = REP / "knowledge_gap/PLAN_knowledge_gap.md"
KG_TXT = txt(KG, note=False)
KG_T = mtime(KG)
KG_CHECKS = {k: (k in KG_TXT) for k in ("64.1 (58.0-69.9)", "57.4 (56.2-58.6)", "57.4 (55.0-59.0)", "74.6", "10-15%",
                                       "20-55", "DI-informed design", "A17")}
KG_SKEPTIC = "R_skeptic" in KG_TXT
KG_R = [os.path.basename(p) for p in gl(str(REP / "knowledge_gap/R_*.md"))]

# other status files
ROADMAP = txt(REP / "ROADMAP_2oct.md")
HANDOFF = txt(ROOT / "HANDOFF.md")
HANDOFF_3OCT = "HANDOFF 3 Oct 2026, 17:25 EDT" in HANDOFF

# real Modal billing, last read by the orchestrator at 23:40 UTC 1 Oct (LIVE-ORCH); nothing on Modal since (ORCH)
BILL_T = "23:40 UTC 1 Oct"
BILL = [("jaypatil-duke", 30.00), ("arya-mahadik-ai", 2.55), ("aryamhd", 3.69), ("atmosphor", 15.22),
        ("mahadikarya2", 30.00), ("mahadikarya3", 30.00), ("mahadikarya44", 30.00)]
BILL_LEFT = round(sum(v for _, v in BILL), 2)
BILL_USED = round(30.0 * len(BILL) - BILL_LEFT, 2)
assert abs(BILL_LEFT - 141.46) < 0.005 and abs(BILL_USED - 68.54) < 0.005, (BILL_LEFT, BILL_USED)

SNAP_FILES = [L / "PREREG_FINAL.md", BENCH / "decision_index/report_sample10k.json", L / "logs/b_wiseft_result.json",
              L / "logs/A12_ohs12_result.md", BENCH / "ejs5/runs/scores_c1_4be.json", BENCH / "v154/RESULTS_30sep.md",
              L / "c_build/progress_phase2.log", L / "c_build/replay_r1_write.json", KG]
SNAPSHOT = max([t for t in (mtime(p) for p in SNAP_FILES) if t] or [LIVE["build"]])

# ----------------------------------------------------------------------------------------------- styles
INK = colors.HexColor("#1d1d1b")
GREY = colors.HexColor("#5f5e5a")
LINE = colors.HexColor("#c9c8c2")
HEAD = colors.HexColor("#e9e8e2")
C_WIN, C_TIE, C_LOSS, C_NA = (colors.HexColor("#dcefe2"), colors.HexColor("#fbf0cf"), colors.HexColor("#f8dede"),
                              colors.HexColor("#ececec"))
TITLE = ParagraphStyle("TITLE", fontName="Arial-Bold", fontSize=19, leading=23, textColor=INK, spaceAfter=3)
SUB = ParagraphStyle("SUB", fontName="Arial", fontSize=9, leading=11.8, textColor=GREY, spaceAfter=3)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15, leading=19, textColor=INK, spaceBefore=2, spaceAfter=6,
                    keepWithNext=1)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3,
                    keepWithNext=1)
H3 = ParagraphStyle("H3", fontName="Arial-Bold", fontSize=9.2, leading=12, textColor=INK, spaceBefore=5, spaceAfter=2,
                    keepWithNext=1)
BODY = ParagraphStyle("BODY", fontName="Arial", fontSize=8.8, leading=11.6, textColor=INK, spaceAfter=3,
                      alignment=TA_LEFT)
SMALL = ParagraphStyle("SMALL", parent=BODY, fontSize=8, leading=10.2, spaceAfter=2)
BUL = ParagraphStyle("BUL", parent=BODY, leftIndent=11, bulletIndent=2, spaceAfter=1.5, bulletFontName="Arial")
BUL2 = ParagraphStyle("BUL2", parent=BODY, fontSize=8.4, leading=11, leftIndent=23, bulletIndent=13, spaceAfter=1,
                      bulletFontName="Arial")
SBUL = ParagraphStyle("SBUL", parent=SMALL, leftIndent=10, bulletIndent=2, spaceAfter=1, bulletFontName="Arial")
PBUL = ParagraphStyle("PBUL", parent=BODY, fontSize=8.6, leading=11, leftIndent=10, bulletIndent=2, spaceAfter=1,
                      bulletFontName="Arial")
SRC = ParagraphStyle("SRC", fontName="Arial-Italic", fontSize=7, leading=8.8, textColor=GREY, spaceBefore=1.5,
                     spaceAfter=5)
NOTE = ParagraphStyle("NOTE", parent=BODY, backColor=colors.HexColor("#fff4d8"), borderColor=colors.HexColor("#e8d49a"),
                      borderWidth=0.5, borderPadding=5, spaceBefore=4, spaceAfter=8)
GOOD = ParagraphStyle("GOOD", parent=NOTE, backColor=colors.HexColor("#e6f3ea"), borderColor=colors.HexColor("#a8cfb4"))
OLDS = ParagraphStyle("OLDS", parent=NOTE, backColor=colors.HexColor("#efefef"), borderColor=colors.HexColor("#bdbdbd"),
                      fontSize=8, leading=10.4)
PLAIN = ParagraphStyle("PLAIN", parent=GOOD, fontSize=9.2, leading=12.4, spaceAfter=7)
CODE = ParagraphStyle("CODE", fontName="Mono", fontSize=7.2, leading=9, textColor=INK, leftIndent=6, spaceAfter=1.5)
CODEC = ParagraphStyle("CODEC", parent=CODE, fontName="Arial-Italic", textColor=GREY, fontSize=7.2, spaceAfter=4)

PAGE_P = letter
PAGE_L = landscape(letter)
MX, MT, MB = 38, 50, 42
PW = PAGE_P[0] - 2 * MX
LW = PAGE_L[0] - 2 * MX


def md(s):
    """Plain text -> safe mini-markup. **bold**, `mono`, and the tags EST / ORCH / LIVE are highlighted."""
    s = str(s)
    if CMAP is not None:
        for ch in s:
            if ord(ch) > 126 and ord(ch) not in CMAP:
                BAD_GLYPHS.add(ch)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"(?<![\w.\-])-(?=\d)", "−", s)  # a minus sign, not a hyphen, before numbers
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r'<font face="Mono">\1</font>', s)
    s = re.sub(r"\bEST\b", '<font color="#a04b00"><b>EST</b></font>', s)
    s = re.sub(r"\bLIVE-ORCH\b", '<font color="#6a3d9a"><b>LIVE-ORCH</b></font>', s)
    s = re.sub(r"(?<!LIVE-)\bORCH\b", '<font color="#2f5597"><b>ORCH</b></font>', s)
    s = re.sub(r"\bLIVE\b(?!-ORCH)", '<font color="#1f7a3a"><b>LIVE</b></font>', s)
    return s


story = []
A = story.append


class _Ctx:
    land = False


CTX = _Ctx()


def width():
    return LW if CTX.land else PW


def page(land=False):
    CTX.land = land
    A(NextPageTemplate("land" if land else "port"))
    A(PageBreak())


def h1(t):
    A(Paragraph(md(t), H1))


def h2(t):
    A(Paragraph(md(t), H2))


def h3(t):
    A(Paragraph(md(t), H3))


def para(t, st=BODY):
    A(Paragraph(md(t), st))


def bullets(items, st=BUL):
    for it in items:
        if isinstance(it, (list, tuple)):
            for sub in it:
                A(Paragraph(md(sub), BUL2, bulletText="-"))
        else:
            A(Paragraph(md(it), st, bulletText="•"))


def src(t):
    A(Paragraph(md("Source: " + t), SRC))


def note(t, st=NOTE):
    A(Paragraph(md(t), st))


def superseded(t):
    A(Paragraph(md("**SUPERSEDED (kept for the record):** " + t), OLDS))


def sp(h=4):
    A(Spacer(1, h))


def md_code(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def code(lines):
    for ln in lines:
        if ln.startswith("#"):
            A(Paragraph(md(ln[1:].strip()), CODEC))
        else:
            A(Paragraph(md_code(ln), CODE))


def status_color(txt_):
    t = str(txt_).upper().replace("*", "")
    for key, col in (("WIN", C_WIN), ("PASS", C_WIN), ("DONE", C_WIN), ("MATCH", C_WIN), ("SHIPPED", C_WIN),
                     ("FROZEN", C_WIN), ("COMMITTED", C_WIN), ("WRITTEN", C_WIN), ("BETTER", C_WIN), ("LOSS", C_LOSS),
                     ("FAIL", C_LOSS), ("MISMATCH", C_LOSS), ("OPEN", C_LOSS), ("MISSING", C_LOSS), ("NO GO", C_LOSS),
                     ("CHECK", C_LOSS), ("BEHIND", C_LOSS), ("TIE", C_TIE), ("PARTLY", C_TIE), ("RUNNING", C_TIE),
                     ("MIXED", C_TIE), ("CLOSE", C_TIE), ("OWNER", C_TIE), ("NEEDS", C_TIE), ("PENDING", C_NA),
                     ("UNMEASURED", C_NA), ("UNKNOWN", C_NA), ("NOT ", C_NA), ("N/A", C_NA), ("CLOSED", C_NA),
                     ("PAUSED", C_NA), ("SUPERSEDED", C_NA), ("PLANNED", C_NA), ("KEEP", C_NA), ("REPORT", C_NA),
                     ("UNTRACKED", C_TIE), ("CHANGED", C_TIE), ("AHEAD", C_TIE), ("UNPROVEN", C_NA),
                     ("POSSIBLE", C_NA)):
        if t.startswith(key):
            return col
    return None


def T(rows, fr, fs=7.3, head=True, status_col=None, mono_cols=(), bold_col0=False, hl_rows=(), keep=False):
    tot = float(sum(fr))
    ws = [width() * f / tot for f in fr]
    cs = ParagraphStyle("c", fontName="Arial", fontSize=fs, leading=fs * 1.24, textColor=INK)
    cb = ParagraphStyle("cb", parent=cs, fontName="Arial-Bold")
    cm = ParagraphStyle("cm", parent=cs, fontName="Mono", fontSize=fs - 0.3)
    data = []
    for i, r in enumerate(rows):
        row = []
        for j, c in enumerate(r):
            if len(str(c)) > 1500:
                print("WARNING: very long table cell", str(rows[0][0])[:30], i, j, len(str(c)), str(c)[:200])
            if head and i == 0:
                stl = cb
            elif j in mono_cols:
                stl = cm
            elif bold_col0 and j == 0:
                stl = cb
            else:
                stl = cs
            row.append(Paragraph(md_code(str(c)) if j in mono_cols and not (head and i == 0) else md(c), stl))
        data.append(row)
    for i, r in enumerate(rows):  # verification aid: a word wider than its cell would be split mid-word
        for j, c in enumerate(r):
            avail = ws[j] - 6.5
            for mono, chunk in ((k % 2 == 1, x) for k, x in enumerate(re.split(r"`", str(c)))):
                for w_ in chunk.replace("**", "").split():
                    fn = "Mono" if (mono or j in mono_cols) else ("Arial-Bold" if (head and i == 0) else "Arial")
                    fsz = fs - 0.3 if (j in mono_cols and not (head and i == 0)) else fs
                    if pdfmetrics.stringWidth(w_, fn, fsz) > avail:
                        SPLIT_WORDS.append((str(rows[0][0])[:30], w_[:50]))
    t = Table(data, colWidths=ws, repeatRows=1 if head else 0, hAlign="LEFT")
    sty = [("FONT", (0, 0), (-1, -1), "Arial", fs), ("GRID", (0, 0), (-1, -1), 0.35, LINE),
           ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    if head:
        sty.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    for i in hl_rows:
        sty.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#eef4fb")))
    if status_col is not None:
        for i, r in enumerate(rows):
            if head and i == 0:
                continue
            col = status_color(r[status_col])
            if col is not None:
                sty.append(("BACKGROUND", (status_col, i), (status_col, i), col))
    t.setStyle(TableStyle(sty))
    A(KeepTogether([t]) if keep else t)


# handy numbers
C1_JAG, C1_OPI = _asr("jagged", "q35_4b_main500k"), _asr("opi", "q35_4b_main500k")
JEV_JAG, JEV_OPI = _asr("jagged", "jev_guard"), _asr("opi", "jev_guard")
EJ_C1P = 100 * EJ_C1.get("overall_pooled", 0.5415)
EJ_JEVP = 100 * (EJ_PUB.get("jev") or {}).get("overall_pooled", 0.5853)
EJ_LATE = EJ_C1.get("late") or {}
DI_K = next((a for a in DI_AREAS if a["area"] == "knowledge"), {"ours_raw": 0.5123, "jev_raw": 0.6888, "diff_pp": -17.65})
KNOW6 = ["GPQA Diamond", "GSM8K", "CRUXEval", "MMLU", "CLadder", "ChessBench"]  # the v0.1 knowledge area (plan §1)
_DIB = {b["dataset"]: b for b in DI_BENCH}


def dib(name):
    b = _DIB.get(name)
    return r1(b['diff_pp'], True) if b else "?"


def dibraw(name, key, dflt):
    b = _DIB.get(name)
    return r1(100 * b[key]) if b and key in b else dflt


snap_s = hm(SNAPSHOT)
BUILD_EDT = edt(LIVE["build"])

# ======================================================================================= page 1: in plain words
A(Paragraph("OpenDecide vs Jev: status record, 3 Oct 2026 (evening)", TITLE))
A(Paragraph(md(f"Saturday 3 October 2026, evening EDT. Built {hm(LIVE['build'])} ({BUILD_EDT} EDT) from "
               f"`{LIVE['branch']}` (HEAD {LIVE['head'][:7]}); newest input {snap_s}. Replaces the 1 Oct record (kept). "
               "Page 1 is for the founder; the rest is for checking."), SUB))
A(Paragraph(md("Tags: **ORCH** = from the orchestrator's session log; **LIVE-ORCH** = its live reading; **LIVE** = "
               "recomputed at build time; **EST** = estimate, never a measurement. Gaps are ours minus Jev in points; "
               "brackets are 95% ranges. Times UTC unless marked EDT (UTC − 4)."), SMALL))
h1("In plain words (for the founder)")
_spd_c1 = (JBC.get("axes") or {}).get("speed", 88.4)
_spd_jev = (JBJ.get("axes") or {}).get("speed", 91.4)
note("**Our shipped model is C1**, the 4B trained on 30 Sep - 1 Oct. You shipped it on 3 Oct even though it failed one "
     "consistency check (double negatives); that is disclosed. The planned repair (fix2) never trained, because a quick "
     "test beforehand showed it would not help ($0). Against Jev, C1 "
     f"**wins** on hijack attacks (our own test set, {C1_JAG.split(' ')[0]} vs {JEV_JAG.split(' ')[0]}) and on cost (by the "
     f"JevBench formula, not measured); it **ties** on injection attacks ({C1_OPI.split(' ')[0]} vs "
     f"{JEV_OPI.split(' ')[0]}) and on the two practice tests (about 1 point behind); it is **ahead** on our unofficial "
     "run of the public JevBench items (our practice items, so not a win claim). It **loses** on the ejs-5 commit test "
     f"({EJ_C1P - EJ_JEVP:+.1f} points), on how well its confidence matches reality, and on the Decision Index, a broad "
     f"skills test ({DI_OURS.get('index', 54.83):.1f} vs {DI_JEV.get('index', 59.51):.1f}): most of that gap is in its "
     f"knowledge part (maths and science questions), where we trail by about {abs(round(DI_K['diff_pp'])):.0f} points. "
     "**No outside win can be claimed yet:** our fair-test rule needs JevBench sealed and ejs-5 to agree, and ejs-5 is a "
     "loss. Now: **plan C**, one careful extra training round (150,000 rows) aimed at new kinds of tasks. Odds (EST): "
     "about **1 in 5** that the new model beats C1 and ships; about **1 in 3** that our final model matches or beats Jev "
     "on the final exam (OHS-3). Modal money left: **$141.46** (nothing spent since 1 Oct).",
     PLAIN)
T([["Test (C1 = our shipped 4B)", "C1", "Jev", "Result"],
   ["Practice test OHS-1 (accuracy)", a12("OHS-1", "c1", "80.4"), a12("OHS-1", "jev", "81.7"),
    f"TIE ({a12d('OHS-1')})"],
   ["Practice test OHS-2 (accuracy)", a12("OHS-2", "c1", "81.0"), a12("OHS-2", "jev", "81.5"),
    f"TIE ({a12d('OHS-2')})"],
   ["ejs-5: 868 software-commit decisions", f"{EJ_C1P:.1f}%", f"{EJ_JEVP:.1f}%",
    f"LOSS ({ej_diff(EJ_C1)}); newest rows tie"],
   ["JevBench public items (our own run, unofficial)", f"{(JBC.get('scores') or {}).get('A', 74.34):.2f}",
    f"{(JBJ.get('scores') or {}).get('A', 68.80):.2f}", "AHEAD (unofficial, our practice items; not a win claim)"],
   ["JevBench official board", "not submitted", "#3 (72.13)", "NOT SUBMITTED (your call, $49)"],
   ["Decision Index sample (broad skills test)", f"{DI_OURS.get('index', 54.83):.2f}", f"{DI_JEV.get('index', 59.51):.2f}",
    f"LOSS: mostly knowledge (maths, science), about {abs(round(DI_K['diff_pp'])):.0f} points behind there"],
   ["Hijack attacks that succeed (lower is better)", C1_JAG.split(" ")[0], JEV_JAG.split(" ")[0], "WIN (our own attack set)"],
   ["Injection attacks that succeed", C1_OPI.split(" ")[0], JEV_OPI.split(" ")[0], "TIE (our own attack set)"],
   ["Confidence matches reality, OHS-1/2 (lower = better)",
    f"{a12('OHS-1', 'br_c1', '0.140')} / {a12('OHS-2', 'br_c1', '0.057')}",
    f"{a12('OHS-1', 'br_jev', '0.114')} / {a12('OHS-2', 'br_jev', '0.038')}", "LOSS (allowed by the goal)"],
   ["Cost per 1,000 decisions (JevBench formula)", "$0.0245", "$0.0384", "WIN (formula; real cost not measured)"],
   ["Speed (JevBench speed score)", f"{_spd_c1:.1f} on our L4 (no fast kernels); never timed on an H100",
    f"{_spd_jev:.1f} via its hosted API (OpenRouter)", "UNPROVEN: H100 test pending (different setups, not comparable yet)"],
   ["Sealed new-domains test", "not run yet", "–", "PENDING: first look after round 1 (about Tue 6 Oct); Jev read once "
    "after the ship verdict"],
   ["Final exam OHS-3", "not run yet", "–", "PENDING (once, at the end)"]],
  [2.6, 1.3, 1.3, 2.6], fs=7.1, status_col=3)
h3("Now and next (dates in EDT; future dates are estimates)")
bullets([
    "**Running:** the free Google L4 reads 99,069 old training rows with C1 (to mix old and new data), **slower than "
    f"planned** (ORCH). Agents build the new data: the rules for {sum(G0F.values())} of 14 new data types are fixed; "
    + ("no new training rows yet (LIVE). " if sum(OUTF.values()) == 0 else "the first candidate files exist, not yet checked (LIVE). ")
    + "A knowledge-gap plan is written (LIVE); nothing in it has run.",
    "**Next:** data ready **Sun 4 - Mon 5 Oct**; training **Mon 5 Oct** (your GO, about $30, about 7 h); verdict (ship the "
    "new model or keep C1) **Tue 6 Oct**; final results with OHS-3 **Wed 7 - Thu 8 Oct** (**Sat 10 - Mon 12** if a second "
    "round is earned, about 13%). Each date may slip by about a day.",
], st=PBUL)
h3("What you must decide")
bullets([
    "**Mon 5 Oct:** GO for a 50-cent test run on Modal, then training round 1 (about $30; hard stop $35).",
    "**Knowledge-gap plan (section 8):** 5 questions, mainly an optional slow \"think\" mode (free L4, about 7-10 days of "
    "agent work) and a label saying we designed it after seeing the Index scores. It would close about half of the Index "
    "gap, not all of it (EST).",
    (f"**Save the plan files in git: DONE** (LIVE; {A162_REF}): the {PRE_A162[0]} changed code files and the "
     f"{PRE_A162[1]} pinned plan files that were untracked (not in git at all) are now committed, and the round-1 Modal "
     "launcher is pinned. Nothing left to decide here." if PLAN_COMMITTED else
     f"**Save the plan files in git** (LIVE; open issue 3): {N_CODE_UNCOMMITTED} code files are changed but not committed, "
     f"and {N_UNTRACKED} pinned plan files are untracked (not in git at all)"
     + ("; the Modal launcher for round 1 is not pinned." if not MODAL_PINNED else ".")),
    "**Can Claude be the teacher?** (your question; ORCH): now Claude writes the questions and programs compute the "
    "answers (allowed); as teacher, Claude would give the answers itself, which breaks our \"no teacher bigger than the "
    "4B\" rule and the claim built on it (Claude's terms may also restrict it). If yes: only as a separate, disclosed "
    "test, locked in writing before running.",
    "**Later GO points:** Jev's one read of the sealed test and OHS-3 (OpenRouter; $6.58 may be short), the H100 "
    "speed/cost test (about $5-8), JevBench sealed ($49 real money).",
    "**Please note:** the earlier OHS-3 forecast (\"+0.8, tie-or-better about 60%\") is replaced: most likely about 1 point "
    "behind Jev, about **1 in 3** to match or beat it (EST, section 7).",
], st=PBUL)

# ======================================================================================= 1. status snapshot
page(False)
h1("1. Status snapshot: 3 October 2026, evening")
note(f"**Where we stand (verifier view).** (1) **Shipped 4B = C1** `q35_4b_main500k` by owner override, amendment A10 "
     f"(`{AM['A10']['commit']}`, {hm(AM['A10']['time'])}, LIVE git). The failed conditions are disclosed: ship look 1 "
     f"(e) {_eq.get('cand', 8.86):.2f}% vs {_eq.get('ref', 5.68):.2f}% (limit 7.68%), and A8′ step 0b NO GO (C1 34.52% vs 4B-E "
     "34.13% flips on the F7 probe, +0.40 pp [−5.86, +6.75], needed ≥ +3 with LB > 0), so **no C4 was trained ($0)**. "
     "(2) 3 Oct tests of C1 vs Jev: OHS-1 / OHS-2 ties (practice sets since A12), ejs-5 LOSS, JevBench public AHEAD (our dev "
     "items; unofficial, not a win claim), Decision Index sample behind (report-only). Step B (weight softening) adopted nothing. (3) **Owner direction "
     "(3 Oct 04:45-06:30 UTC, ORCH): 4B only, the 2B is paused;** beat or match Jev; plan C = research → sealed new-domains "
     f"test → expert data → training round 1 (round 2 only on a clear win); up to about $100 Modal, $25 reserve. (4) Plan C "
     f"so far, $0 Modal: research, spec/recipe v4, sealed suite v2 frozen (A15, 7,302 items), C plan pre-registered "
     f"(A16, A16.1), replay draw {fmt(RW1.get('rows', 0))} rows (LIVE), phase-1 blocks, {sum(G0F.values())} of 14 family "
     f"rule sheets frozen (LIVE). (5) Running: the C1 replay read on the free L4 (ORCH), family generators (LIVE log), "
     f"knowledge-gap plan written (LIVE file). Modal: **${BILL_LEFT:.2f}** left at the last reading ({BILL_T}); no Modal "
     "job since (ORCH).")
h2("1.1 What is where (machines, jobs, files)")
T([["What", "Where", "State", "Next"],
   ["**Shipped 4B: C1** `q35_4b_main500k`", "Mac backup + Modal volume",
    f"SHIPPED by override (A10). Adapter sha256 {BKSHA['.'][0][:8] if BKSHA['.'][0] else 'missing'} "
    f"({'MATCH' if BK_OK else 'CHECK'} vs 507d1c29; 3 snapshots too; LIVE)", "carried to OHS-3 with its disclosures"],
   ["fix2 top-up C4", "–", "NOT TRAINED: step 0b NO GO (02:10 UTC 3 Oct, on od-l4); $0 (A10 §A)",
    "none: A10 allows no further top-up, merge or ensemble without a new amendment"],
   ["Step B: weight softening of C1 (A11)", "Google L4 od-l4b", f"DONE: {BW.get('verdict', 'keep C1')} (LIVE file)", "–"],
   ["OHS-1 + OHS-2 read of C1 (A12)", "od-l4b", "DONE: ties; both are now practice sets", "never used to choose"],
   ["ejs-5 on C1 and 4B-E", "od-l4b", "DONE: LOSS for both (LIVE file)", "report again after C ships"],
   ["JevBench v1.5.4 public on C1", "Google L4 (eager)", "DONE: Score A 74.34 vs 68.80 (LIVE file)", "report-only"],
   ["Decision Index 10K sample on C1 (A13)", "od-l4b (about 8 h)", f"DONE (scored about 23:52 UTC; committed with A16.1): "
    f"{DI_OURS.get('index', 54.83):.2f} vs {DI_JEV.get('index', 59.51):.2f} (LIVE file)", "report-only (never chooses)"],
   ["Deep research + spec / recipe v4", "Mac, CPU agents", "DONE; frozen by sha256 in A16", "–"],
   ["Sealed new-domains suite v2", "isolated agents; `sealed_nd/` (git-ignored)", f"FROZEN (A15): 7,302 items; text checks "
    f"{'MATCH' if A15_OK else 'CHECK'} (LIVE); no model has read it", "first look S1 after round 1"],
   ["C plan round 1", "PREREG A16 + A16.1" + (" + A16.2" if AM["A16.2"]["in_head"] else ""), f"COMMITTED; pinned files {sum(p['match'] for p in PIN)}/{len(PIN)} sha MATCH "
    f"(LIVE); {N_UNTRACKED} untracked + {N_UNCOMMITTED} uncommitted" + (f"; all committed and launcher pinned ({A162_REF})"
                                                                       if PLAN_COMMITTED else ""),
    "–" if PLAN_COMMITTED else "commit the files to git (open issue 3)"],
   ["Replay draw", "Mac", f"DONE 20:50 UTC: {fmt(RW1.get('rows', 0))} rows, {fmt(RW1.get('reads_A5', 0))} reads (LIVE)", "–"],
   ["Replay read (C1 reads the draw)", "od-l4b (free L4)", "RUNNING since about 00:00 UTC 4 Oct; planned 10.7-11.8 h; "
    "shard 1 took over 55 min, slower (ORCH)", "then G9 crowd scoring on the same L4"],
   ["Phase 1 building blocks", "Mac CPU", f"DONE v1.1: {PACKS_N} packs (LIVE), 400 format styles, 8,575 public rows", "–"],
   ["Phase 2: 14 data families", "Mac CPU (workflow w9cr58a3r)", f"RUNNING: {sum(G0F.values())}/14 rule sheets FROZEN; "
    f"generator code for {sum(GEN.values())} families; {sum(OUTF.values())} production files; test/smoke files: {OUT_TEST_S} (LIVE)",
    "solver B (G2) → blind reads (G5) → QC"],
   ["Knowledge-gap research", "Mac agents (whl9uhvgk)", (f"WRITTEN: plan file {hm(KG_T)} (LIVE); nothing run" if KG_TXT else
                                                        "RUNNING (no plan file yet)"), "5 owner decisions (section 8)"],
   ["2B (PRISM-X I) and the cascade", "worktree `jev-2b`", "PAUSED (owner, 3 Oct 04:45 UTC)", "–"],
   ["Modal (7 accounts)", "–", f"no job since 1 Oct (ORCH); ${BILL_LEFT:.2f} at {BILL_T} (LIVE-ORCH)", "smoke + round 1 at GO"],
   ["Google GPU", "project quota: 1 GPU", "od-l4b busy; increase to 2 auto-denied 3 Oct 17:15 UTC (ORCH)", "free L4 only (owner)"],
   ["OpenRouter (Jev calls)", "–", "$6.58 left, key $7.60 of $10 (1 Oct reading); no Jev call since (ORCH)",
    "sealed-suite read + OHS-3 at GO"]],
  [1.75, 1.45, 3.6, 1.7], fs=6.8, status_col=2)
src("LIVE values from the files named in section 11.5; machine states and owner decisions: ORCH (orchestrator log, 3 Oct "
    "entries up to 00:51 UTC 4 Oct); billing: LIVE-ORCH reading of 1 Oct (no newer reading; `budget_tracker.py` not run).")
h2("1.2 Modal credit (last real reading) and account roles")
_role = {"jaypatil-duke": "planned round-1 account ($30.00 left; ORCH)",
         "arya-mahadik-ai": "nearly empty (main run segments 2-3)", "aryamhd": "nearly empty (segment 4)",
         "atmosphor": "segment 5 of the main run", "mahadikarya2": "unused",
         "mahadikarya3": "unused", "mahadikarya44": "unused"}
T([["Modal account", "October credit left", "October used = $30 − left", "Role now"]]
  + [[a, f"${v:.2f}", f"${30 - v:.2f}", _role.get(a, "–")] for a, v in BILL]
  + [["**Total (7 accounts)**", f"**${BILL_LEFT:.2f}**", f"**${BILL_USED:.2f}**", "no Modal spend since this reading (ORCH)"]],
  [1.6, 1.3, 1.5, 4.6], fs=7)
src(f"Modal billing pages read by the orchestrator at {BILL_T} (LIVE-ORCH; sum asserted by the builder). Since then: step 0b "
    "said NO GO, so no C4; every 3 Oct read (B, A12, ejs-5, JevBench, Decision Index, replay read) ran on the free Google "
    "L4 (ORCH; `L/logs/budget_ledger.md` has no Modal row after the gate).")
h2("1.3 Assessment (EST unless a number is cited)")
T([["Area", "Assessment"],
   ["Execution", "**Strong.** Every 3 Oct step was pre-registered and committed before it ran (A10-A16.1, LIVE git). No "
    "Modal spend. The sealed-text spill was caught, cleaned and disclosed (A15). Weak points: one GPU, slow replay read, "
    "rule sheets that did not converge by review (frozen anyway; label checks G2/G5 still to come)."],
   ["Shipped C1", "Better than 4B-E on dev sources neither saw (+2.47 [+1.31, +3.70]) and on most dev checks. Weak on "
    "nested negation (both C1 and 4B-E flip about 34% on the F7 probe); failed (e) and 0b, disclosed."],
   ["Ahead of Jev (measured, with caveats)", f"Hijack {C1_JAG.split(' ')[0]} vs {JEV_JAG.split(' ')[0]} (our own attack "
    "set, used for selection); cost $0.0245 vs $0.0384 (a formula, not a measured cost); JevBench public Score A 74.34 vs "
    "68.80 (our former dev items, no CI: AHEAD, not a win claim). Ties: OHS-1/2 accuracy, injection. **No outside win can "
    "be claimed yet:** the fair-test rule (6.6) needs JevBench sealed and ejs-5 to agree, and ejs-5 is a loss."],
   ["Behind Jev", "ejs-5 −4.4 [−7.8, −0.9]; Decision Index knowledge area −17.7 points (GPQA −38.8, GSM8K −23.1); "
    "calibration (Brier); JevBench sealed Intelligence likely lower (EST)."],
   ["Open", "C round 1 (P(ship) about 22% EST); OHS-3 once (P(≥ Jev) about 31% EST); the sealed-suite Jev read; the H100 "
    "speed/cost test; the knowledge-gap route (section 8)."],
   ["Money", f"Modal ${BILL_LEFT:.2f} (last reading); C capped at about $100 with an expected about $37; speed test about "
    "$5-8; the $25 reserve is kept in every case (section 9.3)."]],
  [1.4, 7.6], fs=7.2)
h2("1.4 Right now and the next GO points")
bullets([
    "**Running:** replay read on od-l4b (ORCH); phase-2 family builds on the Mac CPU (LIVE log, last line "
    f"{P2_LAST[11:16]} UTC); knowledge-gap plan written, waiting for the owner. **Modal:** nothing running.",
    "**Next, no money:** finish the replay read → family generators, solver B (G2), blind reads (G5), QC → G9 crowd "
    "scoring on the free L4 (C1, 4B-E, base 4B; about 16-20 h EST) → mixer + counts-only decontamination.",
    "**GO points in order:** Modal smoke ≤ $0.5 → round 1 about $29.5 (hard stop $35) → look S1 → (round 2 about $57, only "
    "if select ≥ +2.0 with LB > 0) → C look → Jev's sealed read (OpenRouter) → H100 speed + cost test (about $5-8) → "
    "OHS-3 once → report. JevBench sealed ($49 real money) is the owner's separate call.",
], st=SBUL)

# ======================================================================================= reading guide + contents
page(False)
A(Paragraph("Reading guide and contents", TITLE))
h3("What is new in this edition (vs the 1 Oct record)")
bullets([
    "Page 1 (plain words) and section 1 are new. **Section 2** holds the CURRENT owner goal (3 Oct): the 30 Sep goal "
    "(4B + 2B + cascade) is marked SUPERSEDED.",
    "**Section 4** condenses 28 Sep - 2 Oct (the 1 Oct record has the full detail). **Section 5 is new:** what happened "
    "on 2-3 Oct. **Section 6** now compares the shipped C1 with Jev on every test, including ejs-5 and the Decision Index. "
    "**Sections 7-10** (projections, knowledge-gap plan, roadmap and money, risks) are rewritten. Section 11 checks the "
    "A16/A16.1 pins and the amendment commits LIVE.",
    "Dropped: the fix2 build detail (§6.8-6.14 of 1 Oct; fix2 never trained), the 2 Oct 26-row roadmap and its "
    "$113-117 budget, the 30 Sep / 1 Oct odds, and the 2B material (short appendix A).",
    "**Review fixes (3 Oct evening):** page 1 in plainer words; JevBench public shown as AHEAD, not a win; Score A "
    "method corrected (harmonic mean, 6.6); 6.8 on the gate set; 7.3 restated against the goal; modal_od.py marked "
    "unpinned (3.3" + ("; since then pinned by A16.2" if PLAN_COMMITTED else "") + "); two owner questions added; isolation disclosure (11.7). Later review "
    "(3 Oct night): speed restated (Jev's 91.4 is from its hosted API, not our L4); C1's training data stated plainly.",
], st=SBUL)
h3("What \"held out\" means now")
bullets([
    "**Clean exams, still sealed:** OHS-3 (once, at the end), the sealed new-domains suite (its part-A confirm set is the "
    "ship test of plan C; no model has read it) and LongBench v2 (needs its own owner GO).",
    "**Practice sets (read once by C1, never used to choose):** OHS-1 and OHS-2, since A12.",
    "**Report-only (never choose anything):** the Decision Index sample (A13), ejs-5 (counted as in-domain once C trains "
    "commit data from other repos), the JevBench public items (our former dev set).",
    "**Selection sets (not held out):** dev (9 splits), the jagged and OPI attack sets.",
], st=SBUL)
h3("How to check")
bullets([
    "Each table ends with its source. `L/` = `/Users/aryamahadik/Documents/jev/opendecide-data/lean/`, `B/` = "
    "`/Users/aryamahadik/Documents/jev/bench/`, `R/` = `/Users/aryamahadik/Documents/jev/reports/`. Section 11 lists every "
    "file, hash and command.",
    "**LIVE** values were recomputed by this builder at build time; a missing input is skipped with a note and listed in "
    "section 11.5. The builder refuses to open sealed or OHS-3 files, session folders and secrets (section 11.7).",
], st=SBUL)
sp(4)
A(Paragraph("Contents", ParagraphStyle("H3nk", parent=H3, keepWithNext=0)))
toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle("toc0", fontName="Arial-Bold", fontSize=8.8, leading=11, leftIndent=8, firstLineIndent=-8,
                   spaceBefore=2.5),
    ParagraphStyle("toc1", fontName="Arial", fontSize=7.4, leading=8.9, leftIndent=20, firstLineIndent=-8),
]
toc.dotsMinLevel = 0
toc.tableStyle = TableStyle([("FONT", (0, 0), (-1, -1), "Arial", 8), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                             ("TOPPADDING", (0, 0), (-1, -1), 0.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6)])
A(toc)

# ======================================================================================= 2. goal
page(False)
h1("2. Goal, win conditions and rules (current: 3 October)")
h2("2.1 The owner's goal now (3 Oct about 06:00 UTC; ORCH, the authoritative record)")
note("**Beat or match Jev with the 4B** on unseen-domain accuracy and OHS-3 accuracy (at least Jev; −1 point is "
     "acceptable; the target is +1 to +2), and **beat Jev** on hijack and injection resistance, consistency, speed, cost "
     "and JevBench. **The 2B is paused** (owner, 04:45 UTC). Flow: step B → OHS-1/2 check → plan C no matter what (deep "
     "research → sealed new-domains suite → expert golden dataset → round 1 → gate → round 2 only on a clear win) → ship "
     "the best model that passes the gate → OHS-3 once. Stress (14:35 UTC): this run is for generalization to unseen "
     "domains, not for tuning to any test.", GOOD)
superseded("the 30 Sep goal: beat Jev with the final 4B, the final 2B (PRISM-X I) and a 2B→4B cascade (1 Oct record "
           "§2.1). The 2B and the cascade are paused, not cancelled; the 2B keeps 4B-E as its teacher (A10 §D).")
h2("2.2 Win conditions and where each stands")
T([["Axis", "Owner's condition (3 Oct)", "How it is measured", "Status now"],
   ["Unseen-domain accuracy", "≥ Jev (−1 ok; +1-2 target)", "Sealed new-domains suite part A (6,205 items, 8 domains); "
    "Jev read once at the C look, after the ship verdict (A15)", "PENDING: no model has read it"],
   ["OHS-3 accuracy", "≥ Jev (−1 ok)", "PREREG_OHS3: micro over 1,852 base rows, macro over 13 tasks; run once",
    "PENDING (sealed); practice proxy −1.0 pooled"],
   ["Hijack", "beat Jev", "Jagged planted-authority attack rate (our set; used for selection)", f"WIN: {C1_JAG} vs {JEV_JAG} (LIVE)"],
   ["Injection", "beat Jev", "OPI attack rate (our set; used for selection)", f"TIE: {C1_OPI} vs {JEV_OPI} (LIVE)"],
   ["Consistency", "beat Jev", "OHS-3 complement (300 `_neg` pairs) and option order (304 `_perm` pairs)",
    "UNMEASURED vs Jev for C1 (dev: complement 3.30%, option-order flips 2.43%)"],
   ["Speed", "beat Jev", "Not yet defined for OHS-3 (draft); H100 direct-hosting test planned (GO)",
    f"UNPROVEN: Jev {_spd_jev:.1f} via its hosted API (OpenRouter); C1 {_spd_c1:.1f} on our L4 (no fast kernels); C1 "
    "never timed on an H100: H100 test pending (6.11)"],
   ["Cost", "beat Jev", "JevBench formula; real serving cost never measured", "WIN on the formula"],
   ["JevBench", "beat Jev", "Public items (unofficial) now; sealed board only with the owner's OK", "AHEAD (public practice items; not a win claim)"],
   ["Calibration", "may lose", "Yes/no Brier (OHS-1/2 practice; OHS-3 endpoint)", "LOSS (allowed)"],
   ["ejs-5", "no claim (in-domain after C)", "Pooled accuracy, paired over 622 commits (PREREG_ejs5)", "LOSS −4.4"]],
  [1.2, 1.5, 3.6, 2.5], fs=7, status_col=3)
src("ORCH (owner, 3 Oct 06:00 UTC); `L/PREREG_FINAL.md` A15; `L/PREREG_OHS3.md` (cited by name; the builder does not open "
    "OHS-3 files); security LIVE (section 6.10). \"≥ Jev\" is the owner's 3 Oct wording, recorded in the orchestrator log, "
    "not in a committed file (open issue 8).")
h2("2.3 How a model is chosen now (A16; recipe v4 §6.2-6.4)")
bullets([
    "**One candidate per round** (the final-step adapter). It replaces C1 only if the sealed part-A **confirm** gain over C1 "
    "is **≥ +1.0 pp with a 95% lower bound > 0**, no sealed domain drops clearly (P2), part B is not worse (P3), and the "
    "guards D1-D6 and D9 pass (dev non-inferiority, yes/no and choice, Brier, flips, attacks, latency).",
    "**Round 2 runs only** if round 1's **select** gain is ≥ +2.0 pp with LB > 0 and the guards pass (owner, 3 Oct 06:30 UTC).",
    "**Looks:** S1, (S2), C once; Jev is read once, after the ship verdict. The sealed scorer logs every look and refuses "
    "any other (A15). ejs-5, OHS-1/2/3, JevBench, the Decision Index and LongBench **never choose anything**.",
], st=SBUL)
h2("2.4 OHS-3 facts (no OHS-3 file opened)")
bullets([
    "1,852 base rows (1,136 choice, 716 yes/no), 13 tasks; 300 complement and 304 permutation pairs; Jev pinned to "
    "`typesafe/jev-1.13-20260917`, run twice; each OpenDecide model runs once (`L/PREREG_OHS3.md`, 1 Oct record §2.3).",
    "**A10 overlap disclosure:** the owner's counts-only check found 7 golden_train units (gd_redocred 6, "
    "gd_helpsteer3_pref 1) sharing 12-grams with OHS-3; C1 trained on them. OHS-3 is reported with and without those "
    f"items (A10 §D; LIVE text check {'MATCH' if A10_OK else 'CHECK'}). Plan C drops both sources whole (A16 (d)).",
    "The PREREG_OHS3 model amendment at the OHS-3 step must name C1 (sha256 507d1c29...) and its A5 readout; the runbook "
    "and config template still name 4B-E (open issue 4).",
], st=SBUL)
h2("2.5 Rules the project follows now")
bullets([
    "GO from the owner before any Modal spend; prompts only at GO points. Training GO up to about $100 in total, keeping "
    "the $25 reserve; **free Google L4 only** for scoring (owner, 17:25 UTC); no paid Modal L4.",
    "No teacher bigger than our 4B; Claude authors the data; **no Jev output is ever an input** (training, selection, "
    "thresholds or temperatures). Pre-register every step before it runs; never use test items.",
    "**Sealed:** OHS-3, the sealed new-domains suite and LongBench v2. Builders never open sealed folders or session "
    "folders (A15 incident). Nothing is chosen on ejs-5, OHS-1/2/3, JevBench, the Decision Index or LongBench.",
    "**Data policy (3 Oct 05:40-06:00 UTC, ORCH):** commercial-licence public TRAIN splits only (private sources file); "
    "non-commercial data is study-only; our own program-labelled families; commit data from OTHER repos (never n8n, never "
    "ejs-5 items), disclosed, so ejs-5 counts as in-domain. Data stays private.",
    "No JevBench submission without the owner's word. One Mac backup per model. Honest numbers; no absolute public "
    "claims about data sources (owner, 3 Oct about 03:10 UTC). Code: C1 = tag `final-frozen`; plan C = the A16 pins (3.3).",
], st=SBUL)

# ======================================================================================= 3. the shipped model
page(False)
h1("3. The shipped 4B (C1): architecture, configs, code state, data")
h2("3.1 Layout E (`schema_branch_mark`): the layout of C1 and of plan C")
bullets([
    "**Prompt order** (`L/decoder_io.py`): (1) trusted schema: a definitions card (yes/no rows), the instructions, the "
    "options with definitions; (2) the untrusted text between `<<<UNTRUSTED TEXT START>>>` and `<<<UNTRUSTED TEXT END>>>` "
    "with a note that it is data; (3) a trusted question branch that repeats the question and short options; (4) "
    "\"Answer with the letter of exactly one option\": one forward pass, letter logits.",
    "Chosen on 29-30 Sep: X14 (layout E +1.36 [+0.25, +2.45] on dev-confirm, PASS); X15 (PRISM-X on the 4B ≈ 0, FAIL); "
    "X19 (read twice at serving ≈ 0, FAIL) (`L/logs/budget_ledger.md`).",
    "LoRA r 16 / alpha 32 on all `QWEN35` targets: 32,464,896 trainable parameters of 4,238,216,192 (0.766%).",
    "**A5 readout (shipped):** choice rows read twice (given order + exact reversal, averaged), yes/no read once, T = 1.00 "
    "/ 1.00; JevBench uses band edge on yes/no (pre-registered; `prep89/READOUT_DEV.md`, cited by name). Plan C adds a "
    "per-type temperature by leave-one-group-out within [0.8, 1.3] (addendum C1-C3).",
], st=SBUL)
h2("3.2 Run configs: C1 vs plan C round 1 (LIVE)")
keys = list(dict.fromkeys(list(CFG4) + list(CFGC)))


def cv(v):
    if v is None:
        return "–"
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    s_ = str(v)
    return ("placeholder (" + s_[5:].replace("_", " ").lower() + ")") if s_.startswith("FILL") else s_


rows = [["Key", "C1: `runs/q35_4b_main.json`", "Round 1: `runs/q35_4b_c_r1.json`"]]
for k in keys:
    a_, b_ = cv(CFG4.get(k)), cv(CFGC.get(k))
    rows.append([k, a_, b_ if b_ != a_ else "same"])
T(rows, [1.3, 2.8, 2.9], fs=6.6)
src(f"LIVE: C1 config sha256 {(LIVE['sha']['runs/q35_4b_main.json'] or '')[:16]} (unchanged since the tag; expected "
    f"e686d444); round-1 config sha256 {(LIVE['sha']['runs/q35_4b_c_r1.json'] or '')[:16]} (A16 pin f3bb379e; tracked, committed in 6d79bf2). "
    "Placeholders \"FILL_...\" are filled mechanically from the mixer and the batch dry run (A16); the seed is fixed at "
    "**20261003** by A16, while the file still holds a placeholder (discrepancy 10.3 #12).")
bullets([
    "What changes for round 1: init from C1's adapter (`init_adapter`); peak LR 5e-5 (C1 7e-5); base-model anchor off "
    "(`beta` 0); the A4 ordinal term `lam_ord` 1.0 (the only new loss); monitor snapshots at 25/50/75%; data `c_parts/`.",
    "One pass: about 8,880 steps for 150,000 rows (recipe v4 §4); C1 ran 30,457 steps on 501,732 rows.",
], st=SBUL)
h2("3.3 Code state (LIVE)")
rows = [["File (L/)", "Working copy sha256 (LIVE)", "At tag final-frozen (C1's code)", "A16 / A16.1 / A16.2 pin", "Check"]]
for f in FROZEN_FILES:
    pin = next((p for p in PIN if p["rel"] == f), None)
    wc, tg = LIVE["sha"][f] or "missing", LIVE["tag_sha"][f] or "missing"
    ok_tag = tg == EXPECT_TAG[f]
    if pin:
        chk = "MATCH (pin; tag = C1)" if pin["match"] and ok_tag else "MISMATCH"
        pin_s = pin["pref"]
    else:
        chk = "MATCH (unchanged)" if wc == EXPECT_TAG[f] and ok_tag else "MISMATCH"
        pin_s = "– (unchanged)"
    rows.append([f, wc[:24] + "...", tg[:16] + "...", pin_s, chk])
for f, exp in (("modal_od.py", "8f4bef05"), ("od_gcp.py", "9253209d"), ("gate_dev.py", "78975445")):
    wc = LIVE["sha"][f] or "missing"
    if f == "modal_od.py":
        hd = (LIVE["modal_head_sha"] or "missing")
        if MODAL_CHANGED:
            chk = ("CHANGED vs HEAD, uncommitted, " + ("pinned" if MODAL_PINNED else "NOT pinned (A16/A16.1)")
                   + (f"; HEAD = the 1 Oct value" if hd.startswith(exp) else "; HEAD ≠ 1 Oct value"))
        elif MODAL_PINNED and hd == wc:
            chk = "MATCH (HEAD = working copy = pin" + (", A16.2)" if wc[:8] in A162B else ")")
        else:
            chk = "MATCH (HEAD = working copy)" if hd.startswith(exp) else "CHECK"
        rows.append([f, wc[:24] + "...", f"HEAD {hd[:8]}", "– (not pinned)" if not MODAL_PINNED else wc[:8], chk])
    else:
        rows.append([f, wc[:24] + "...", "–", "–", "MATCH (unchanged)" if wc.startswith(exp) else "MISMATCH"])
T(rows, [1.2, 2.3, 2.0, 1.1, 1.9], mono_cols=(1, 2, 3), status_col=4, fs=6.6)
sp(4)
bullets([
    f"`git diff --stat final-frozen` on the 4 frozen files + C1's config (LIVE): "
    f"{(LIVE['frozen_diff'].splitlines()[-1].strip() if LIVE['frozen_diff'] else 'no difference')}. **Expected:** the "
    "A16 default-off changes (A4 ordinal term, F2 rendered-prompt assert); "
    + (f"they are **committed** ({A162_REF}). " if N_UNCOMMITTED == 0 and AM["A16.2"]["in_head"] else
       "they are **not committed** (HEAD still holds the tag versions). ")
    + "C1 reproduces bit for bit with them (ORCH, train prep 19:00 UTC; 297 + 55 tests pass, 1 failure "
    "that was there before).",
    (f"**The Modal launcher `modal_od.py` is changed and not pinned (LIVE):** working copy {_msha[:8]} (modified "
     f"{hm(LIVE['modal_mtime'])}) vs HEAD {(LIVE['modal_head_sha'] or '?')[:8]}: {LIVE['modal_diffstat'] or 'diff unavailable'}. "
     "It adds the C-round upload rules (`C_KEEP` for `c_train_r1` / `c_rel_r1`) and launch checks. This launcher will run "
     "round 1, but it is neither committed nor pinned in A16/A16.1 (open issue 3; owner decision on page 1)."
     if MODAL_CHANGED else ("`modal_od.py`: working copy = HEAD = " + _msha[:8] + " (LIVE)"
                            + (f", pinned in A16.2 ({A162_REF}); it adds the C-round upload rules and launch checks."
                               if MODAL_PINNED and _msha[:8] in A162B else "."))),
    f"C1's own record (backup `train_meta.json`): code = the 4 tag hashes {'MATCH' if BK_CODE_OK else 'MISMATCH'}; data = "
    f"golden_train / relations {'MATCH' if BK_DATA_OK else 'MISMATCH'} (LIVE).",
    "Pinned environment of the main run: python 3.12.10, torch 2.14.0, transformers 5.17.0, peft 0.21.0; Qwen3.5-4B "
    "revision `851bf6e8`. The L4 replay read renders prompts byte-identical to the Mac despite transformers 5.17.0 vs "
    f"4.57.6 (F2 check, LIVE: {F2_EQ}/{F2_N} views equal).",
], st=SBUL)
h2("3.4 Data: golden set v14 (C1's training set; plan C's replay pool)")
d_ = LIVE["data"]
_gt = d_.get("data/v14_parts/golden_train.jsonl") or {}
_gr = d_.get("data/v14_parts/golden_relations.jsonl") or {}
T([["Quantity", "Value", "Check"],
   ["Train rows / dev rows / sources", f"501,732 (LIVE {fmt(_gt.get('lines', 0))}) / 22,587 / 204",
    "MATCH" if _gt.get("lines") == 501732 and _gt.get("sha", "").startswith("ff7a395bc9b501ac") else "CHECK"],
   ["Relations", f"74,094 (LIVE {fmt(_gr.get('lines', 0))}): complement 36,958, equiv 1,922, inv 35,214",
    "MATCH" if _gr.get("lines") == 74094 and _gr.get("sha", "").startswith("072ee6c4") else "CHECK"],
   ["Yes/no share; roles", "64.5%; choice 163,008, aff 263,684, neg 37,552, attacked 31,936, dneg 1,107", "SRC golden_summary"],
   ["Rules", "**intended** rules (GOLDEN_CARD): human text with human labels, or exact program labels; permissive "
    "licences; train splits only; decontamination against OHS-1/2/3, eval sets and JevBench public items. Also in C1's "
    f"training: soft targets at config kd {CFG4.get('kd', 0.5)} on {fmt(CFG4.get('expect_kd_targets', 43363))} rows "
    f"(annotator vote shares plus {fmt(CFG4.get('expect_kd_full', 238))} exact program probabilities; not 4B-E labels), "
    f"a legacy v13 replay pool ({GC_REPLAY} rows), and 45,103 rows whose old model-teacher soft labels the run switched "
    "off (`kd_skip_src` blend50; see 10.2). **Later checks found exceptions:** see 2.4 (7 units overlap "
    "OHS-3), 5.6 (non-commercial sources; MuSR items that are Decision Index test items) and 5.10 "
    f"({fmt(RWD.get('rows_dropped', 83807))} rows dropped by licence/deny rules).", "PARTLY (exceptions found)"],
   ["Audits", "label audit 442 rows: 91.0% correct, 6.3% ambiguous, 2.7% wrong; priority families 94.2% correct "
    "(ledger D5-D6)", "–"],
   ["OHS-3 overlap (A10 §D)", "7 units share 12-grams with OHS-3 (counts-only check); an earlier 13-gram + exact check "
    "had found 0 (different n-gram size and scope; discrepancy 10.3 #2)", "DISCLOSED"],
   ["Use in plan C", f"replay pool after licence/deny drops: {fmt((RW.get('eligible') or {}).get('rows', 0))} rows from "
    f"{(RW.get('eligible') or {}).get('sources', '?')} sources (LIVE, section 5.10)", "–"]],
  [1.6, 5.6, 1.0], fs=7, status_col=2)
src("`L/data/v14_parts/` (sha256 and line counts LIVE), `GOLDEN_CARD.md`, `golden_summary.json`; `L/logs/budget_ledger.md` "
    "D1-D8; `L/c_build/replay_r1_write.json`.")

# ======================================================================================= 4. history (compact)
page(True)
h1("4. History, 28 September - 2 October (compact)")
para("A short record of how C1 came to be. The 1 Oct record (`reports/OpenDecide_Full_Status_1Oct.pdf`, 62 pages) has "
     "every detail; numbers here are copied from it or re-read LIVE. Times UTC.", SMALL)
h2("4.1 Log")
T([["When (UTC)", "What", "Result", "Source"],
   ["27 Sep", "Layout test M5 and protected memory M6 (2B arms)", "layout E passes; protected memory fails (−5.89 pp)",
    "ledger M5-M6"],
   ["28-29 Sep", "PRISM-X 2B arms on the Google L4 (X4-X13)", "arm I best; every add-on on top of I lost", "ledger X4-X13"],
   ["29 Sep", "Golden dataset v14 (D1-D7) and the 4B-E control (X14)", "501,732 rows / 204 sources; 4B-E 81.49 "
    "dev-confirm (+1.36 vs v13t), best 4B", "ledger D1-D7, X14"],
   ["29 Sep 18:50", "PRISM-X on the 4B (X15)", "about 0 → the 4B uses plain layout E", "ledger X15"],
   ["30 Sep 10:35-12:30", "2B matched pair X18; owner override", "accuracy −0.27, hijack 1.1% vs 10.0% → final 2B = "
    "PRISM-X I (now paused)", "ledger X18"],
   ["30 Sep 17:45", "**Owner GO: the 4B main run** (one pass over 501,732 rows)", "segment 1 on jaypatil-duke",
    "overnight plan"],
   ["30 Sep 19:06-22:24", "JevBench v1.5.4 public on 4B-E; option-order drift; H100 speed", "Score A 71.03 raw / 75.27 "
    "committed vs Jev 68.80; drift 7.79% → 1.90% with 2 views; p50 16.6 ms, speed axis 94.7 vs 83.8",
    "`B/v154/RESULTS_30sep.md`; drift and speed results"],
   ["30 Sep 19:17", "Code freeze", "commit 82b07d4, tag `final-frozen` (C1's code)", "git"],
   ["1 Oct 13:16", "Laptop lost its network; Modal cancelled segment 4", "signal save at 25,682; a spawn launcher "
    "finished the run", "`L/logs/main4b_seg4.log`, relay log"],
   ["1 Oct 15:28", "Amendments A0 + A7", "PREREG_FINAL adopted; 4B parity REF fixed", "git 9759d31"],
   ["1 Oct about 17:16", "**4B training finished**", f"{fmt(TOTAL_STEPS)} steps; Mac backup {'MATCH' if BK_OK else 'CHECK'} "
    "(LIVE)", "relay log; train_meta"],
   ["1 Oct 17:58-21:12", "**Ship gate, job 1** (L4 od-l4)", f"parity PASS; C1 +{_prim.get('diff', 2.47):.2f} on unseen dev "
    f"sources; **DO NOT SHIP** on (e) {_eq.get('cand', 8.86):.2f}% vs {_eq.get('ref', 5.68):.2f}%", "`L/logs/gate4b/` (LIVE)"],
   ["1 Oct evening", "Fix research; owner decisions", "C1 is our model; fix A = fix2 (a short top-up); fallback C = ship "
    "C1 by override", "ORCH; RESUME_NOTE_1oct"],
   ["1 Oct 23:40", "Real Modal billing read", f"${BILL_LEFT:.2f} left on 7 accounts", "LIVE-ORCH"],
   ["2 Oct", "F7 v2 + fix2 data built on CPU; 3 blind reads failed and were repaired; read 4 passed on r6; 3 skeptic "
    "reviews + a fixer", "fix2 = 42,566 rows, 2,512 steps, about $9 planned", "1 Oct record §6.8-6.14"],
   ["3 Oct 01:47", "A8′ committed (the fix2 rules)", "its only executed step was 0b: NO GO (section 5.1)", "git c35de00"]],
  [1.3, 3.0, 3.6, 2.0], fs=6.8)
h2("4.2 The 4B main run that produced C1 (LIVE from the 5 segment logs)")
_seg_rows = []
for sg in SEGS:
    r = sg["recs"]
    st_ = seg_state(sg)
    _seg_rows.append([sg["name"], sg["account"] or "–", hm(sg["birth"]), fmt(sg["resumed"]) if sg["resumed"] else "0",
                      fmt(r[-1]["step"]) if r else "–",
                      ("DONE: " + st_) if not st_.startswith("cancelled") else "PARTLY: " + st_,
                      f"{sg['sps']:.2f}" if sg["sps"] else "–", str(sg["alerts"])])
T([["Log", "Account", "Log created", "Resumed at", "Last logged step", "State (LIVE)", "s/step", "ALERT"]] + _seg_rows,
  [1.0, 1.0, 1.0, 0.65, 0.7, 3.6, 0.5, 0.5], status_col=5, fs=6.6)
CHART = SCR / "loss_main500k.png"
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    if not REC:
        raise RuntimeError("no loss records")
    xs = [r["step"] for r in REC]
    ys = [r["loss"] for r in REC]
    roll = []
    for i in range(len(ys)):
        w = ys[max(0, i - 19): i + 1]
        roll.append(sum(w) / len(w))
    fig, ax = plt.subplots(figsize=(10.0, 2.3), dpi=200)
    ax.plot(xs, ys, color="#b9c7d9", lw=0.8, label="loss (logged every 50 steps)")
    ax.plot(xs, roll, color="#2f5597", lw=1.6, label="rolling mean (1,000 steps)")
    ax.set_xlabel("step")
    ax.set_ylabel("training loss")
    ax.set_xlim(0, TOTAL_STEPS * 1.02)
    ax2 = ax.twinx()
    ax2.plot(xs, [r["lr"] * 1e5 for r in REC], color="#a04b00", lw=1.0, ls="--", label="learning rate (x1e-5)")
    ax2.set_ylabel("lr (x1e-5)", color="#a04b00")
    for sg in SEGS[1:]:
        if sg["resumed"]:
            ax.axvline(sg["resumed"], color="#999999", lw=0.6, ls=":")
    ax.spines[["top"]].set_visible(False)
    ax2.spines[["top"]].set_visible(False)
    h_a, l_a = ax.get_legend_handles_labels()
    h_b, l_b = ax2.get_legend_handles_labels()
    ax.legend(h_a + h_b, l_a + l_b, fontsize=7, frameon=False, loc="lower center", ncol=3, bbox_to_anchor=(0.5, 1.0))
    ax.tick_params(labelsize=7)
    ax2.tick_params(labelsize=7)
    ax.set_title(f"C1 = q35_4b_main500k: {len(SEGS)} segments, steps 0-{max(xs):,} of {TOTAL_STEPS:,} (LIVE; dotted = relay)",
                 fontsize=8, pad=16)
    fig.tight_layout()
    fig.savefig(str(CHART))
    plt.close(fig)
    A(Image(str(CHART), width=LW * 0.82, height=LW * 0.82 * 2.3 / 10.0))
except Exception as e:  # noqa
    if exists(CHART):
        A(Image(str(CHART), width=LW * 0.7, height=LW * 0.7 * 2.6 / 7.6))
        para(f"(Chart re-render skipped: {e}; the copy from the 1 Oct build folder is shown.)", SMALL)
    else:
        para(f"(Chart skipped: {e})", SMALL)
para(f"{fmt(TOTAL_STEPS)} steps = one pass; {BKMETA.get('minutes', 1380.98):,.0f} training minutes on Modal H100s; every "
     f"relay resumed at the exact step with all checks matching; {ALERTS} ALERT lines (LIVE). Cost about $100 (ORCH).",
     SMALL)
h2("4.3 Ship gate job 1 (1 Oct; the condition A10 overrides)")
T([["Test (C1 vs REF = 4B-E read fresh)", "C1", "REF", "Difference [95% CI]", "Status"],
   ["**Primary: dev sources neither model trained on**", f"{_prim.get('cand', 83.99):.2f}", f"{_prim.get('ref', 81.52):.2f}",
    f"{_prim.get('diff', 2.47):+.2f} [{_prim.get('lo', 1.31):+.2f}, {_prim.get('hi', 3.70):+.2f}]",
    "PASS" if _prim.get("pass", True) else "FAIL"]]
  + [[f"({c['id']}) {c['name']}", "", "", c["detail"], c["status"]] for c in GSHIP.get("constraints", [])],
  [3.0, 0.6, 0.6, 4.4, 0.7], status_col=4, fs=6.6)
para(f"Verdict (LIVE, `L/logs/gate4b/look_ship1.json`): **{GSHIP.get('verdict', '?')}** (final {GSHIP.get('final')}). "
     f"Reference parity {'PASS' if GPAR.get('pass') else 'CHECK'}: agreement {GPAR.get('agree', '?')}% over "
     f"{fmt(GPAR.get('n', 0))} rows (bit-identical reads). **Overridden by A10** on 3 Oct 03:10 UTC (section 5.2).", SMALL)
h2("4.4 Why (e) failed: one wording (dev diagnosis, kept short)")
bullets([
    "29 of C1's 64 flipped pairs come from one hate-speech frame (\"the tweet contains only non-hateful content\" inside "
    "\"Should the statement that ... be rejected?\"): C1 flips 29 of 30 there, 4B-E 0 of 30 (4B-E mostly answers \"no\").",
    "Without those 30 pairs C1 flips less than 4B-E: 35 of 692 (5.06%) vs 41 of 692 (5.92%). C1 is more accurate on both "
    "rows of the 722 pairs (affirmative 84.90 vs 83.93; double negation 84.35 vs 82.96) (A10 §C).",
    "On held-out nested negation (the F7 probe, 252 pairs) C1 and 4B-E are equally weak: 34.52% vs 34.13% flips (A10 §A).",
    "Cause: golden_train has about 16 times less double negation than 4B-E's lineage (0.34% of yes/no rows).",
], st=SBUL)
h2("4.5 From the fix research to fix2 (1-2 Oct)")
bullets([
    "Six research agents ranked fixes; the owner chose **fix A = fix2**: a short top-up from C1 with a new nested-negation "
    "family F7, one-way `inv` consistency pairs and ≥ 70% replay (about 2,500 steps, about $9-11), guarded by A8′ "
    "(step 0b probe pre-check, non-inferiority vs C1, one ship look). Fallback C = ship C1 by a disclosed override.",
    "2 Oct: F7 v2 and fix2 were built and audited on the Mac CPU (final file 42,566 rows, 2,512 steps). A8′ was committed "
    "3 Oct 01:47 UTC. **Step 0b said NO GO, so fix2 never trained** (section 5.1).",
], st=SBUL)

# ======================================================================================= 5. 2-3 October
page(True)
h1("5. What happened on 2-3 October")
para("Git times are the authority (LIVE). EDT = UTC − 4. \"ORCH\" rows come from the orchestrator's log; nothing here "
     "comes from a sealed file.", SMALL)
h2("5.0 Timeline of 3 October (and early 4 October UTC)")


def _gt(cid):
    t_ = (RC.get(cid) or (None, None))[1]
    if t_ is None:
        for a_ in AM.values():
            if a_["commit"].startswith(cid):
                t_ = a_["time"]
    return t_


def _ts(t_):
    return (hmu(t_), edt(t_)) if t_ else ("?", "?")


TL = []


def tl(t_, what, result, srcs, approx=False, key=None):
    if isinstance(t_, dt.datetime):
        u, e = _ts(t_)
        key = key or t_
    else:
        u, e = t_
    TL.append((key or dt.datetime(2026, 10, 5, tzinfo=UTC), [("about " if approx else "") + u, e, what, result, srcs]))


_d = lambda s: dt.datetime.strptime("2026-10-03 " + s, "%Y-%m-%d %H:%M").replace(tzinfo=UTC)  # noqa: E731
_d4 = lambda s: dt.datetime.strptime("2026-10-04 " + s, "%Y-%m-%d %H:%M").replace(tzinfo=UTC)  # noqa: E731
tl(AM["A8′"]["time"], "**A8′ committed** (fix2 rules)", "C4 = fix2 top-up; steps 0a/0b, R, P, N, one look", f"git {AM['A8′']['commit']}")
tl(_d("02:10"), "**Step 0b (F7 probe pre-check) on od-l4**", "**NO GO**: C1 34.52% vs 4B-E 34.13% flips (+0.40 [−5.86, +6.75]; "
   "needed ≥ +3, LB > 0) → no C4, $0", "A10 §A; ORCH", approx=True)
tl(_d("02:30"), "Option D (amend the stop rule and train anyway)", "blocked by the session's safety check; edit reverted; "
   "nothing trained; no A9 exists", "ORCH", approx=True)
tl(AM["A10"]["time"], "**A10: owner override, C1 is the shipped 4B**", "failed conditions disclosed; 2B keeps 4B-E labels; OHS-3 "
   "overlap disclosed", f"git {AM['A10']['commit']}")
tl(_d("03:40"), "JevBench v1.5.4 public on C1 (L4)", "band edge: Intelligence 75.1 vs 63.2; Score A 74.34 vs 68.80", "`B/v154/RESULTS_30sep.md`", approx=True)
tl(_gt("9a04df1"), "ejs-5 pre-registered (+ a note on the backup L4)", "kit: convert, run, score, 15 tests", "git 9a04df1, 065191c")
tl(_gt("32ee1f9"), "**ejs-5 result**", f"C1 {EJ_C1P:.1f}% vs Jev {EJ_JEVP:.1f}%: LOSS; newest rows tie", "git 32ee1f9")
tl(_d("04:45"), "**Owner: 4B only; the 2B is paused;** up to about $100 Modal", "plan C defined (research → sealed test → data → rounds)", "ORCH", approx=True)
tl(AM["A11"]["time"], "A11: step B (weight softening) pre-registered", "candidates a = 0.6-0.9; fixed select/confirm rule", f"git {AM['A11']['commit']}")
tl(AM["A12"]["time"], "A12: OHS-1 + OHS-2 as the Jev yardstick", "stop if ≥ Jev + 1 pp, else continue with C", f"git {AM['A12']['commit']}")
tl(_d("05:50"), "Deep research launched (CPU)", "7 web angles + local gaps + 2 skeptics + licence checks", "ORCH", approx=True)
tl(_d("06:00"), "**Owner restates the CURRENT GOAL**; 06:30: round 2 only on a clear win", "section 2.1", "ORCH", approx=True)
tl(_gt("599c513"), "**Step B result**", f"{BW.get('verdict', 'keep C1')}", "git 599c513")
tl(_gt("629a9f4"), "**A12 result**", f"OHS-1 {a12d('OHS-1')}; OHS-2 {a12d('OHS-2')}", "git 629a9f4")
tl(AM["A13"]["time"], "A13: Decision Index sample on C1, report-only", "never used to choose anything", f"git {AM['A13']['commit']}")
tl(AM["A14"]["time"], "A14: sealed-suite build rules", "isolated builders; counts by domain id only", f"git {AM['A14']['commit']}")
tl(_d("15:00"), "Research completeness pass done", "6 extra studies + addendum (14 ADOPT rows)", "ORCH", approx=True)
tl(_d("15:13"), "Decision Index sample run starts on od-l4b", "10,001 requests; about 8 h", "ORCH; `B/decision_index/README.md`", approx=True)
tl(_d("16:30"), "Spec + recipe **v4 final**", "equal commit shares (20% each); 150K-row round 1", "ORCH; `L/c_spec/`", approx=True)
tl(_d("17:15"), "GPU quota 1 → 2 requested (owner OK)", "auto-denied by Google in seconds; 17:25 owner: free L4 only", "ORCH", approx=True)
tl(_d("18:30"), "Sealed suite v1 **NOT READY**", "spread rule failed; sealed text had spilled into session folders → "
   "cleanup, no waiver", "ORCH; A15", approx=True)
tl(AM["A15"]["time"], "**A15: sealed suite v2 frozen**", "7,302 items; part A 6,205 in 8 domains", f"git {AM['A15']['commit']}")
tl(AM["A16"]["time"], "**A16: C round-1 plan**", "150,000 rows; seed 20261003; one candidate", f"git {AM['A16']['commit']}")
tl(mtime(L / "c_build/replay_r1_write.json") or _d("20:50"), "Replay draw written", f"{fmt(RW1.get('rows', 0))} rows + 2,000-row old slice (LIVE)",
   "replay_r1_write.json")
tl(_d("22:36"), "Phase 1 (packs, formats, public rows) reviewed and fixed (v1.1)", f"{PACKS_N} packs (LIVE), 400 styles, "
   "8,575 public rows", "progress_phase1.log", approx=True)
tl(_d("23:52"), "**Decision Index scored**", f"{DI_OURS.get('index', 54.83):.2f} vs Jev {DI_JEV.get('index', 59.51):.2f}", "`B/decision_index/`", approx=True)
tl(AM["A16.1"]["time"], "**A16.1** + the Decision Index report", "tool versions; EDOS and choice-row rules", f"git {AM['A16.1']['commit']}")
tl(_d4("00:00"), "Replay read starts on od-l4b", "F2 prompt check passes on the L4; ETA 11-12 h, running slower", "ORCH; `L/c_build/f2_l4.json`", approx=True)
tl(("4 Oct 00:12-00:50", "Sat 3 Oct 8:12-8:50 PM"), f"{sum(G0F.values())} of 14 family rule sheets FROZEN", "each with sha256, 0 open "
   "label-flip items", "progress_phase2.log (LIVE)", key=_d4("00:12"))
_gs = sorted(P2_GENSTART.items(), key=lambda kv: kv[1])
_gst = [dt.datetime.strptime("2026-10-04 " + v, "%Y-%m-%d %H:%M").replace(tzinfo=UTC) for _, v in _gs]
tl((f"4 Oct {_gs[0][1]}-{_gs[-1][1]}" if _gs else "4 Oct", (f"{edt(_gst[0])}-{(_gst[-1] - dt.timedelta(hours=4)).strftime('%-I:%M %p')}"
                                                          if _gst else "Sat 3 Oct evening")),
   "Generator code started for " + (", ".join(k for k, _ in _gs) or "no family yet"),
   f"{P2_TESTS_S}; production (round-1) files: {sum(OUTF.values())}", "same (LIVE)", key=_d4("00:28"))
tl(_d4("00:45"), "Knowledge-gap research launched (owner request)", "5 researchers → plan", "ORCH", approx=True)
if AM["A16.2"]["time"] and AM["A16.2"]["in_head"]:
    tl(AM["A16.2"]["time"], "**A16.2**: round-1 Modal launcher pinned; plan files committed",
       f"`modal_od.py` {_msha[:8]}; the {PRE_A162[0]} changed code files and the {PRE_A162[1]} untracked pinned files are "
       "now in git; review "
       "and licence-check files stay out (they name sealed-suite candidates)", f"git {AM['A16.2']['commit']}")
if KG_T:
    tl(KG_T, "Knowledge-gap plan written (revised after a skeptic review)", "think-mode route; Index EST 57.4 (56.2-58.6) vs "
       "59.51", "PLAN_knowledge_gap.md (LIVE)")
TL.sort(key=lambda r: r[0])
T([["When (UTC)", "When (EDT)", "What", "Result", "Source"]] + [r for _, r in TL], [1.1, 1.35, 3.0, 3.6, 1.8], fs=6.6)

h2("5.1 The fix2 outcome (A8′ step 0b): never trained, $0")
note("**What fix2 was:** a short top-up (C4) of C1 with a nested-negation family (F7), to repair the (e) failure. **A8′** "
     f"(`{AM['A8′']['commit']}`, {hm(AM['A8′']['time'])}) required a pre-check first: step 0b had to show, on 252 held-out F7 "
     "probe pairs, that C1 flips at least 3 points more than 4B-E (lower bound > 0) — otherwise there is nothing for fix2 "
     "to fix. **Result (02:10 UTC, od-l4): C1 87 of 252 (34.52%), 4B-E 86 (34.13%), +0.40 pp [−5.86, +6.75] → NO GO.** "
     "Probe accuracy (report only): C1 74.54, 4B-E 74.05. By A8′ D no C4 was trained and **$0** was spent. Meaning: C1's "
     "(e) failure is narrow (one dev frame); on general nested negation C1 = 4B-E, and both are weak (about 34% flips).",
     NOTE)
bullets([
    "After the NO GO, an attempt to change the stop rule and train anyway (option D) was blocked by the session's safety "
    "check; the edit was reverted and nothing was trained or committed (ORCH). **There is no amendment A9.**",
    "Flip research (CPU, ORCH): a weight merge of C1 + 4B-E (P about 0.10-0.15, dev-picked) and a 2-adapter ensemble "
    "(about −9 JevBench cost points) were both rejected; a gated \"Fix3\" (P pass about 0.15-0.27, about $12) stays "
    "optional and would need a new amendment (A10 §D).",
], st=SBUL)
h2("5.2 A10: the owner ships C1 (03:10 UTC), in plain words")
T([["Part", "What A10 says (committed text; LIVE check " + ("MATCH" if A10_OK else "CHECK") + ")"],
   ["A. What failed", "Ship look 1: (e) 8.86% vs 5.68% (limit 7.68%; 64 vs 41 of 722 pairs). Step 0b: NO GO. C1 is "
    "never described as having passed the ship rule."],
   ["B. What passed", "Primary +2.47 pp [+1.31, +3.70] (83.99 vs 81.52); yes/no +1.40; choice +0.94; Brier 0.1099 vs "
    "0.1184; permutation flips 2.43% vs 3.78%; jagged 0.0% vs 0.6%; OPI 1.3% vs 1.8%; parity 100%."],
   ["C. Why the override", "The failure sits in one dev frame (29 of 30 flips); elsewhere C1 flips less; C1 = 4B-E on "
    "held-out nested negation; OHS-3 has no double-negation twins and C1 is better on its consistency axes on dev "
    "(complement 3.30% vs 4.63%, option order 2.43% vs 3.78%)."],
   ["D. Consequences", "C1 may not teach the 2B (the 2B keeps 4B-E's 2-view labels; no relabel). OHS-3 amendment names "
    "C1 + the A5 readout. OHS-3 reported with and without the 7 overlapping units. No further top-up, merge or ensemble "
    "without a new amendment."]],
  [1.4, 8.4], fs=7)
src(f"`L/PREREG_FINAL.md` Amendment A10 (git {AM['A10']['commit']}); `L/prereg_drafts/A10_override_C1.md`. Owner instruction "
    "(ORCH, 3 Oct about 03:10 UTC): no new lineage line in reports; no absolute public data claims.")
h2("5.3 Owner decisions, 1-3 October")
T([["When (UTC)", "Decision", "Source"],
   ["1 Oct after 21:12", "C1 (the new 4B) is our model; keep the 4B-E files", "RESUME_NOTE_1oct; ORCH"],
   ["1 Oct evening", "Fix A = fix2 with the A8′ safeguards; fallback C = ship C1 by a disclosed override", "ORCH"],
   ["2 Oct about 04:00", "GO through fix2 training only if every check passes (cap $13) → re-test → pause", "RESUME_NOTE_2oct"],
   ["3 Oct about 02:10-03:10", "After the NO GO: **ship C1** (option B, disclosed override → A10)", "ORCH; A10"],
   ["3 Oct about 04:00-04:20", "Run ejs-5 (C1 + 4B-E) and the LongBench v2 kit on the free L4; ejs-5 first, then B, then C; "
    "arm D (2B + F7) not added", "ORCH"],
   ["3 Oct 04:45", "**Forget the 2B for now; focus on the 4B.** Up to about $100 of the $141 Modal may be spent; target: "
    "comparable to Jev, ideally +1-2", "ORCH"],
   ["3 Oct 05:00", "Overnight GO: finish B; OHS-1 + OHS-2 as a secondary yardstick (they become practice sets); stop if ≥ "
    "Jev + 1, else research → sealed suite → C data → rounds; keep the $25 reserve", "ORCH; A12"],
   ["3 Oct 05:40-06:00", "Commit data from OTHER repos allowed (never n8n or ejs-5 items); training splits of public "
    "evals only (never test items); commercial licences only; data private", "ORCH"],
   ["3 Oct 05:45-06:10", "Run B, then C \"no matter what\"; if B adopts a winner, C builds on it; run on the agent loop "
    "overnight; no regression of the shipped model", "ORCH"],
   ["3 Oct 06:20-06:30", "Codex review adopted (skill-based C, selective anchor, sealed suite first, RL only after SFT); "
    "**round 2 only on a clear round-1 win**; keep the owner's commit-data version", "ORCH"],
   ["3 Oct 14:35-14:50", "This run is for generalization; Decision Index ~10K sample on C1, report-only", "ORCH; A13"],
   ["3 Oct 17:15-17:25", "OK to ask Google for 2 GPUs (auto-denied); then **free L4 only**, no paid Modal L4", "ORCH"],
   ["3 Oct 18:05-18:30", "Do not pause the Decision Index run; sealed v1: no waiver, rebuild; OK to delete the 31 spilled "
    "files", "ORCH; A15"],
   ["4 Oct about 00:45 (8:45 pm EDT)", "Small deep research on closing the knowledge gap; validate on separate dev sets; "
    "the Decision Index stays report-only; round 1 (A16) untouched", "ORCH; section 8"],
   ["4 Oct, after the facts pass (about 01:15 UTC or later)", "**PENDING, owner's call:** the owner asked \"can Claude be the "
    "teacher?\" Answer given: possible, but it **breaks the no-bigger-teacher rule** (2.5) and the claim built on it, "
    "and may be restricted by Claude's terms. If yes, "
    "only as a separate, disclosed, pre-registered experiment; not part of round 1 (A16).", "ORCH"],
   ([f"{hm(AM['A16.2']['time'])}", f"**DONE:** the plan files are in git ({A162_REF}): the {PRE_A162[0]} changed code files "
     f"(including the Modal launcher `modal_od.py`, now pinned) and the {PRE_A162[1]} untracked pinned plan files were "
     "committed (LIVE)", "LIVE git"] if PLAN_COMMITTED else
    ["Open (no date)", "**PENDING, owner's call:** commit the plan files to git: " + f"{N_UNTRACKED} pinned files untracked, "
     f"{N_CODE_UNCOMMITTED} code files changed but uncommitted, including the unpinned Modal launcher `modal_od.py` "
     "(LIVE; open issue 3)", "ORCH; LIVE git"]),
   ["Standing", "No teacher bigger than 4B; no Jev outputs as inputs; OHS-3, LongBench and the sealed suite stay sealed; "
    "JevBench submission only on the owner's word; one backup per model", "memory rules; ORCH"]],
  [1.6, 6.4, 1.8], fs=6.8)
h2("5.4 Step B: softening C1's weights (A11; dev only)")
rows = [["Candidate (W = base + a × C1's change)", "Dev-select unseen", "Both halves, unseen vs C1 [95% CI] (n 3,847)", "Read"]]
for nm, c in sorted(BW_C.items(), key=lambda kv: -kv[1].get("a", 0)):
    b_ = c.get("all_unseen_boot") or {}
    rows.append([f"a = {c.get('a')} (`{nm.split('_')[-1]}`)", f"{c.get('select_unseen', 0):.2f} vs C1 {c.get('select_unseen_ref', 0):.2f}",
                 f"{b_.get('diff', 0):+.2f} [{b_.get('lo', 0):+.2f}, {b_.get('hi', 0):+.2f}]",
                 "picked (a*)" if c.get("a") == BW.get("a_star") else ("LOSS" if b_.get("hi", 1) < 0 else "TIE")])
T(rows, [2.6, 2.0, 3.0, 1.2], fs=7, status_col=3)
sp(5)
rows = [["Confirm check for a* = " + str(BW.get("a_star", "?")) + " vs C1 (dev-confirm half)", "Detail", "Result"]]
for c in BW_CHECKS:
    rows.append([c.get("check"), c.get("detail"), "PASS" if c.get("pass") else "FAIL"])
T(rows, [4.0, 3.0, 1.0], fs=7, status_col=2)
para(f"**Verdict (LIVE): {BW.get('verdict', '?')}.** Plan C starts from C1. Parity: the od-l4b re-read of C1 equals the "
     "od-l4 read (100%, max |dp| 0; ORCH). Source: `L/logs/b_wiseft_result.json` (git 599c513).", SMALL)
h2("5.5 Outside tests of C1 on 3 October (details in section 6)")
T([["Test", "C1", "Jev", "C1 − Jev [95% CI]", "Status", "Can it choose a model?"],
   ["OHS-1 (A12; practice since)", a12("OHS-1", "c1", "80.4"), a12("OHS-1", "jev", "81.7"), a12d("OHS-1"), "TIE", "no"],
   ["OHS-2 (A12; practice since)", a12("OHS-2", "c1", "81.0"), a12("OHS-2", "jev", "81.5"), a12d("OHS-2"), "TIE", "no"],
   ["ejs-5 (868 rows, 622 commits)", f"{EJ_C1P:.2f}%", f"{EJ_JEVP:.2f}%", ej_diff(EJ_C1), "LOSS", "no (report)"],
   ["JevBench v1.5.4 public, band edge", f"I {(JBC.get('axes') or {}).get('intelligence', 75.1):.1f}; A "
    f"{(JBC.get('scores') or {}).get('A', 74.34):.2f}", f"I {(JBJ.get('axes') or {}).get('intelligence', 63.2):.1f}; A "
    f"{(JBJ.get('scores') or {}).get('A', 68.80):.2f}",
    (f"I {(JBC.get('paired_vs_jev_p1') or {}).get('diff', 11.9):+.1f} [{((JBC.get('paired_vs_jev_p1') or {}).get('ci95') or [3.0, 21.3])[0]:+.1f}, "
     f"{((JBC.get('paired_vs_jev_p1') or {}).get('ci95') or [3.0, 21.3])[1]:+.1f}]"), "AHEAD (dev items)", "no (practice)"],
   ["Decision Index 10K sample", f"{DI_OURS.get('index', 54.83):.2f}", f"{DI_JEV.get('index', 59.51):.2f} (full suite)",
    f"{DI_OURS.get('index', 54.83) - DI_JEV.get('index', 59.51):+.2f} (not paired; about ±1-2)", "LOSS", "never (A13)"],
   ["Security: jagged / OPI (LIVE)", f"{C1_JAG} / {C1_OPI}", f"{JEV_JAG} / {JEV_OPI}",
    f"{_asr_cmp('jagged', 'q35_4b_main500k')} / {_asr_cmp('opi', 'q35_4b_main500k')}", "WIN / TIE", "selection sets"]],
  [2.2, 1.5, 1.5, 2.5, 1.0, 1.1], fs=6.9, status_col=4)

h2("5.6 Deep research for plan C (3 Oct, CPU only, $0)")
T([["Study (in `L/c_spec/`)", "Key finding (plain words)"],
   ["Competitor lessons", "No open 4B matches Jev on broad unseen tasks; most big 4B wins over Jev are on tasks like their "
    "training. Jev leads most on new task families and on knowledge."],
   ["Cross-domain generalization; small-model intelligence", "**Breadth beats volume:** count distinct task cards, not "
    "rows; gains flatten near 64 rows per task; under 300 distinct instructions never generalized, ≥ 1,000 did; many "
    "wordings per task help small models most."],
   ["Expert question design", "Labels must be exact (program labels, two different solvers; a model never sets a label); "
    "LLM-written text has shortcuts; decontamination must go beyond n-grams."],
   ["RL for decisions", "**RL does not help a one-token readout** (no GRPO/PPO); keep cross-entropy and KD."],
   ["Weight preservation", "Keep C1's skills with 50-60% replay and a selective C1 anchor; expected old-skill change −0.5 to "
    "+0.5; preservation does not create far-domain gains."],
   ["Licensed data (+ 3 licence checks, private register)", "50 usable commercial datasets; Hugging Face licence tags are "
    "often wrong (5 mismatches); C1's replay had licence and contamination problems (e.g. non-commercial sources; MuSR "
    "items are Decision Index test items)."],
   ["Local gaps; 2 skeptic reviews (4 blockers each)", "Where C1 fails on dev; blockers fixed in v3/v4 (rejected datasets, a "
    "weak round-2 rule, a gate that rarely ships, a sealed suite too close to the families)."],
   ["Completeness pass: 6 extra studies + addendum", "Adopted A1-A4 (ordinal targets; **A4 mean-E term = the only new "
    "loss**), B1-B4 (30% message-only commit rows; yes rate 20-80% per rule; yes-share alarm; no test-time prior fix), "
    "C1-C3 (per-type T, leave-one-group-out, within [0.8, 1.3]), D1 (no influence-based selection), E1-E3, F2-F4 "
    "(rendered-prompt sha assert; O*NET personas). B6 (decomposing ejs-5 gold) NOT run, to keep ejs-5 clean."]],
  [2.6, 7.2], fs=6.9)
src("the facts pass's short summaries of the plan-C research in `L/c_spec/` (13 studies: 7 web angles + 6 extra, plus "
    "local gaps, 2 skeptic reviews and 3 licence checks); every data rule from them is carried in `C_DATA_SPEC.md` v4 and "
    "PREREG A16. **Isolation note:** those inputs included research and review files that C_DATA_SPEC v4 (\"Who may read "
    "what\") bars C builders from because they name sealed-suite candidates; this table names none, this builder opens "
    "none of them, and they are no longer read or cited as report inputs (disclosure in 11.7). Never `L/c_spec/sealed_brief/`.")
h2("5.7 Spec and recipe v4: the round-1 design (pinned in A16)")
T([["Part", "Round 1 (A16)", "Notes"],
   ["Replay of C1's data", "90,000 rows (60%)", f"drawn from the eligible pool; draw = {fmt(RW1.get('rows', 0))} rows (90,000 + "
    "10% margin) for crowd and anchor selection (LIVE)"],
   ["Own program-labelled families", "45,250 rows", "13 families F1-F13 (rule sheets frozen; ids only here)"],
   ["Licensed public train splits", "8,750 rows", "14 datasets, human labels, commercial licences"],
   ["Commit decisions from other repos", "6,000 rows", "**equal shares** route / triage / score / gate / match, 1,200 each; "
    "30% of gate/triage/route message-only (1,080); never n8n or ejs-5 items"],
   ["**Total**", "**150,000 rows**; ≥ 1,050 task cards", "median about 40 rows per card, max 128; round 2 = 300,000 "
    "(superset), only on a clear win"],
   ["Training", "init C1; same LoRA; LR 5e-5; one pass (about 8,880 steps)", "C1's losses + `lam_ord` 1.0; base anchor off; "
    "C1 anchor only where C1 is right and confident (p ≥ 0.8) or on a protected skill; seed 20261003; RL not in the plan"],
   ["Gate", "confirm ≥ +1.0, LB > 0 + guards", "round 2 needs select ≥ +2.0, LB > 0 (section 2.3)"],
   ["Kept out", "ShARC, Measuring Hate Speech, CAD-SNLI, Social IQa, CosmosQA, e-CARE, EmoBank, ConvAbuse, NewsMTSC, "
    "DocFinQA, MultiHiertt, ConvFinQA, CodeReviewer", "licence, label or contamination reasons (spec §0.1)"],
   ["Equal commit shares (fix)", "v3 had set shares 10/20/25/35/10 from the ejs-5 per-task gaps", "that broke the rule "
    "\"ejs-5 never chooses anything\"; v4 uses 20% each (verifier blocker, 16:10 UTC)"]],
  [2.0, 2.6, 5.2], fs=6.9)
src("`L/c_spec/C_DATA_SPEC.md` v4 §0-§0.2 (sha 4ca12996), `C_TRAIN_RECIPE.md` v4 §0, §4 (sha f4b79150); `L/PREREG_FINAL.md` "
    "A16; LIVE sha checks in section 11.2.")
h2("5.8 The sealed new-domains test suite: v1 failed, v2 frozen (counts by domain id only)")
T([["Part", "Items", "Notes (A15 text; LIVE text check " + ("MATCH" if A15_OK else "CHECK") + ")"],
   ["**A (headline, real text)**", "**6,205** in 8 domains", "select 2,542 / confirm 3,663; largest domain 16.1%"],
   ["- non-adjacent domains", "D1, D10, D11, D12: 3,446 (55.5%)", "rule met: ≥ 4 non-adjacent domains holding ≥ 50%"],
   ["- adjacent domains", "D2, D3, D4, D5: 2,759", "labels fixed at pick time, before any model read"],
   ["P (program-built)", "600 (3 × 200)", "report-only"],
   ["B1 (commit decisions)", "298", "repos outside CommitChronicle / CommitPackFT, never n8n; 2 near-duplicate groups dropped"],
   ["B2 (long documents)", "199", "4,148-7,718 tokens; 1 decontamination drop"],
   ["**Total**", "**7,302**", "select 2,988 / confirm 4,314; yes/no 46.5% of items (gold yes 50.0%); 58.2% card-free; 2-8 options"]],
  [2.0, 2.6, 5.2], fs=7)
bullets([
    "**v1 (about 18:30 UTC): NOT READY.** 7,221 items, part A over 9 domains, but only 1 non-adjacent domain (rule: ≥ 4 "
    "holding ≥ 50%); B2 had 199 items; 2 B1 near-duplicate pairs. No waiver (owner: \"no compromise\"); v1 was never read "
    "by a model. 3 new non-adjacent domains were built and whole adjacent domains dropped.",
    "**Isolation incident (disclosed in A15):** sealed item text had spilled into shared session temp folders (tool "
    "results, task outputs, scratchpad). With the owner's OK the 31 flagged files were deleted and the sealed transcripts "
    "moved into `sealed_nd/`; a 12-gram re-scan found 0 files with ≥ 3 hits outside. C builders may not open session "
    "folders; this builder refuses them too (section 11.7).",
    "Decontamination (counts only, 12-grams vs C1's 501,732 training rows) dropped 43 v1 items and 18 new items (whole "
    "groups). Noise-floor reads: at most 1.5% clearly wrong per domain; none dropped.",
    "Frozen files (git-ignored, never opened here): suite sha256 `f4ae8637...`, scorer sha256 `953a3363...`. The scorer "
    "prints aggregates only, logs every look and refuses looks not in the plan; Jev is read once, after the ship verdict.",
], st=SBUL)
_A_LAST = "A16.2" if AM["A16.2"]["in_head"] else "A16.1"
h2(f"5.9 Amendments A13-{_A_LAST} (all committed before the step they govern)")
rows = [["Amendment", "Commit (LIVE)", "Git time (UTC / EDT)", "Header says", "In HEAD", "What it fixes in advance"]]
for name in ("A13", "A14", "A15", "A16", "A16.1") + (("A16.2",) if AM["A16.2"]["in_head"] else ()):
    a_ = AM[name]
    gap = (a_["stated"] - a_["time"]).total_seconds() / 60 if (a_["stated"] and a_["time"]) else None
    rows.append([name, a_["commit"], f"{hmu(a_['time'])} / {edt(a_['time'])}",
                 (a_["stated"].strftime("%-d %b %H:%M") + (f" ({gap:+.0f} min)" if gap is not None and abs(gap) > 2 else "")
                  if a_["stated"] else "?"), "MATCH" if a_["in_head"] else "MISSING", a_["what"]])
T(rows, [0.8, 0.9, 1.9, 1.4, 0.7, 4.1], fs=6.9, status_col=4)
bullets([
    "**A16 rulings on the deny-list:** (a) bare platform words (Wikipedia, Reddit, GitHub...) never match alone; real "
    "overlap is caught by counts-only n-gram decontamination; (b) entries rejected only for label quality are "
    "`no_new_rows`, not `taint` (T-REx; MuSiQue passes); (c) \"locked\" = \"avoid\"; (d) the A10 overlap is handled by "
    "dropping gd_redocred and gd_helpsteer3_pref whole; (e) attacked replay rows with C1 p_g < 0.2 count as successful "
    "attacks, not dropped. \"neither ... nor\" = one negation. Addendum D2 (facility-location selection) NOT adopted.",
    "**A16.1:** pinned tool versions (deny-list v1.2, aliases v1.1, negcount v1.1, replay sampler); 17 sub-entries moved "
    "to `no_new_rows`; the replay writer refuses stale verdicts and needs the A15 sha; (f) the 2-of-3-annotator filter on "
    "every EDOS row; (g) on choice rows everything goes in instructions, state or \"- option: definition\" lines.",
    "Order by git time: A15 and A16 were committed before the replay draw was written; A16.1 before the first generator "
    f"start (4 Oct 00:28 UTC, LIVE log). The headers of A14-{_A_LAST} carry times 11-25 minutes after their commits; git is "
    "the authority (discrepancy 10.3 #1).",
], st=SBUL)
h2("5.10 Data build: replay draw, phase 1, phase 2 (counts only)")
_rb = RWD.get("rows_dropped_by_rule") or {}
T([["Step", "Result (LIVE unless marked)", "Source"],
   ["Replay pool", f"C1's {fmt(RW.get('pool_rows', 0))} rows / {RW.get('pool_sources', '?')} sources", "replay_r1_write.json"],
   ["Dropped by licence / deny rules", f"**{fmt(RWD.get('rows_dropped', 0))} rows**: " + "; ".join(f"{k} {fmt(v)}" for k, v in _rb.items()),
    "same"],
   ["Eligible after the 2,000-row old slice", f"{fmt((RW.get('eligible') or {}).get('rows', 0))} rows / "
    f"{fmt((RW.get('eligible') or {}).get('units', 0))} units / {(RW.get('eligible') or {}).get('sources', '?')} sources "
    f"(old slice held out for forgetting checks: {fmt((RW.get('old_slice') or {}).get('rows', 0))} rows + "
    f"{fmt((RW.get('old_slice') or {}).get('replay_rows_held_out_with_it', 0))} with it)", "same"],
   ["**Round-1 draw**", f"**{fmt(RW1.get('rows', 0))} rows**, {fmt(RW1.get('units', 0))} units, {RW1.get('sources', '?')} sources; "
    f"choice {fmt(RW1.get('choice_rows', 0))}, yes/no {fmt(RW1.get('yesno_rows', 0))} (hard {fmt(RW1.get('hard_yesno_rows', 0))} at "
    f"{pct(RW1.get('hard_yesno_yes_rate', 0), 2)}% yes); attacked {fmt(RW1.get('attacked_rows', 0))}; **{fmt(RW1.get('reads_A5', 0))} "
    "C1 reads** (A5 readout)", "same"],
   ["Round-2 superset draw", f"{fmt(RW2.get('rows', 0))} rows ({fmt(RW2.get('reads_A5', 0))} reads), used only if round 2 runs", "same"],
   ["L4 time for the round-1 read", f"EST {(RW.get('l4_estimate_round1_read') or {}).get('est_hours_rows_scaled', '?')}-"
    f"{(RW.get('l4_estimate_round1_read') or {}).get('est_hours_char_scaled', '?')} h; running slower (ORCH)", "same; ORCH"],
   ["F2 prompt check (L4 vs Mac)", f"{F2_EQ} of {F2_N} rendered views byte-identical", "`f2_l4.json`, `f2_local_mac.json`"],
   ["Phase 1: packs", f"{PACKS_N} packs (" + ", ".join(f"{k} {v}" for k, v in PACKS.items()) + "); O*NET persona seeds; lint "
    "clean; sealed check 0 blocking", "packs files (LIVE line counts)"],
   ["Phase 1: formats, public rows", "400 format styles (350 training, 50 held out for dev), 77 skins, 12 card styles, 14 "
    "containers; 672 family wordings, 98 public wordings, 62 codebooks; public round-1 rows 8,575 (+175 moved to F13 = "
    "8,750 planned); 0 taint", "phase-1 manifests (facts pass, 4 Oct 01:00 UTC)"],
   ["Phase 2: rule sheets (G0)", f"**{sum(G0F.values())} of 14 FROZEN** ({', '.join(f for f in FAMS if G0F[f])}), each with sha256 "
    "and 0 open label-flip items; review did not converge, so the real label checks are G2 (an independent solver B), "
    "G3/G4 and G5 blind reads", "`c_src/*/G0_FROZEN.json`; ORCH"],
   ["Phase 2: generators", f"code for {sum(GEN.values())} families ({', '.join(f for f in FAMS if GEN[f])}); starts logged: "
    + ", ".join(f"{k} {v}" for k, v in sorted(P2_GENSTART.items(), key=lambda kv: kv[1])) + f"; {P2_TESTS_S}; "
    f"test/smoke output files: {OUT_TEST_S}; **production (round-1) files: {sum(OUTF.values())}**",
    "`progress_phase2.log`; `c_src/*/out/` (LIVE)"],
   ["Flags from the log", ("F13 served length about 6.0-6.5K tokens (v4 assumed about 4.6K); " if F13_LEN else "")
    + ("F10: card printed twice on choice rows may exceed the length budget (stop-and-report rule); " if F10_LEN else "")
    + ("F6: 7 of 36 formats-2 wordings fail a new F6 rule (29 < 30 floor), to be replaced before pool approval" if F6_WORDINGS else ""),
    "`progress_phase2.log` (LIVE)"]],
  [1.8, 6.4, 1.6], fs=6.8)
h2("5.11 The replay read on the L4 (running)")
bullets([
    "C1 reads every replay row once (choice rows twice) on the free L4 od-l4b, so the mixer can pick anchor targets and "
    "drop rows C1 already gets confidently right. Started about 00:00 UTC 4 Oct (8 pm EDT Sat) after the Decision Index "
    "run; the F2 check passed on the L4 (ORCH; LIVE file).",
    f"Planned {(RW.get('l4_estimate_round1_read') or {}).get('est_hours_rows_scaled', 10.7)}-"
    f"{(RW.get('l4_estimate_round1_read') or {}).get('est_hours_char_scaled', 11.8)} h. At about 00:50 UTC shard 1 of 20 was not "
    "done after 55 minutes and a memory hiccup had been recovered (ORCH). **EST finish: Sunday 4 Oct between about 8 am "
    "and 8 pm EDT** (on plan: about 7-8 am; at the first shard's pace for all 20 shards: about 6-8 pm). Progress lives on "
    "the VM; this builder makes no ssh call, so it cannot check it.",
    "After it: G9 crowd scoring of each family as it passes QC (C1, 4B-E and the base 4B; about 16-20 L4-hours EST), on "
    "the same single GPU (Google quota 1; the increase was denied).",
], st=SBUL)

# ======================================================================================= 6. benchmarks
page(True)
h1("6. Benchmarks: every comparison with Jev (the shipped C1)")
h2("6.1 Scoreboard")
T([["Axis", "Jev", "C1 (shipped)", "Difference [95% CI]", "Status", "Held out?", "Source"],
   ["Accuracy, OHS-1 (1,847 rows)", a12("OHS-1", "jev", "81.7"), a12("OHS-1", "c1", "80.4"), a12d("OHS-1"), "TIE",
    "practice since A12", "A12 result"],
   ["Accuracy, OHS-2 (1,320 rows)", a12("OHS-2", "jev", "81.5"), a12("OHS-2", "c1", "81.0"), a12d("OHS-2"), "TIE",
    "practice since A12", "A12 result"],
   ["Macro accuracy, OHS-1 / OHS-2", f"{a12('OHS-1', 'mac_jev', '81.5')} / {a12('OHS-2', 'mac_jev', '82.0')}",
    f"{a12('OHS-1', 'mac_c1', '80.1')} / {a12('OHS-2', 'mac_c1', '81.3')}", "–", "TIE (behind)", "practice", "A12 result"],
   ["Yes/no Brier, OHS-1 / OHS-2", f"{a12('OHS-1', 'br_jev', '0.114')} / {a12('OHS-2', 'br_jev', '0.038')}",
    f"{a12('OHS-1', 'br_c1', '0.140')} / {a12('OHS-2', 'br_c1', '0.057')}", "ours worse", "LOSS", "practice", "A12 result"],
   ["ejs-5 pooled (868 rows)", f"{EJ_JEVP:.2f}%", f"{EJ_C1P:.2f}%", ej_diff(EJ_C1), "LOSS", "yes until C trains commit data",
    "scores_c1_4be.json"],
   ["ejs-5, rows from 1 Jun 2026 (268)", f"{100 * EJ_LATE.get('jev', 0.459):.1f}%", f"{100 * EJ_LATE.get('ours', 0.463):.1f}%",
    ej_diff(EJ_C1, "late_overall_pooled"), "TIE", "same", "same"],
   ["JevBench v1.5.4 public, Score A", f"{(JBJ.get('scores') or {}).get('A', 68.80):.2f}",
    f"{(JBC.get('scores') or {}).get('A', 74.34):.2f} (band edge)", "–", "AHEAD (dev items; no win claim)", "no", "scores_v154_c1.json"],
   ["JevBench public, Intelligence", f"{(JBJ.get('axes') or {}).get('intelligence', 63.2):.1f}",
    f"{(JBC.get('axes') or {}).get('intelligence', 75.1):.1f}",
    f"{(JBC.get('paired_vs_jev_p1') or {}).get('diff', 11.9):+.1f} [{((JBC.get('paired_vs_jev_p1') or {}).get('ci95') or [3.0, 21.3])[0]:+.1f}, "
    f"{((JBC.get('paired_vs_jev_p1') or {}).get('ci95') or [3.0, 21.3])[1]:+.1f}]", "AHEAD (dev items; no win claim)", "no", "same"],
   ["JevBench official board", "#3, Score A 72.13", "not submitted", "–", "NOT SUBMITTED", "sealed half", "board 30 Sep"],
   ["Decision Index sample, index", f"{DI_JEV.get('index', 59.51):.2f} (full suite)", f"{DI_OURS.get('index', 54.83):.2f} (10K sample)",
    f"{DI_OURS.get('index', 54.83) - DI_JEV.get('index', 59.51):+.2f} (not paired; ±1-2)", "LOSS", "yes (report-only)",
    "report_sample10k.json"],
   ["Decision Index, knowledge area", r1(100 * DI_K['jev_raw']), r1(100 * DI_K['ours_raw']), f"{DI_K['diff_pp']:+.2f}",
    "LOSS", "same", "same"],
   ["Hijack, jagged attack rate", f"{JEV_JAG} (LIVE)", f"{C1_JAG} (LIVE)", _asr_cmp("jagged", "q35_4b_main500k"), "WIN",
    "no (selection set)", "section 6.10"],
   ["Injection, OPI attack rate", f"{JEV_OPI} (LIVE)", f"{C1_OPI} (LIVE)", _asr_cmp("opi", "q35_4b_main500k"), "TIE",
    "no (selection set)", "section 6.10"],
   ["Definition overwrite (redef)", "never run", (f"{REDEF['q35_4b_main500k']['asr']:.1f}% (LIVE)" if REDEF.get("q35_4b_main500k") else "–"),
    "–", "UNMEASURED for Jev", "no", "section 6.10"],
   ["Speed, JevBench axis", f"{_spd_jev:.1f} via its hosted API (OpenRouter, our run); board 83.8",
    f"{_spd_c1:.1f} on our L4 (no fast kernels); never timed on an H100", "– (reference only, a different model: 4B-E "
    "94.7 on an H100 with CUDA graphs)", "UNPROVEN", "public items", "6.11"],
   ["Cost, JevBench formula", "$0.0384 / 1K (axis 52.5)", "$0.0245 / 1K (axis 58.3)", "−36%", "WIN", "–", "6.11"],
   ["Dev unseen sources (vs 4B-E, not Jev)", "never run", f"+{_prim.get('diff', 2.47):.2f} vs 4B-E", "–", "PASS (vs 4B-E)", "no",
    "gate job 1"],
   ["OHS-3; sealed new-domains suite; LongBench v2", "–", "not run", "–", "PENDING", "yes (sealed)", "–"]],
  [1.9, 1.5, 1.8, 1.9, 1.0, 1.1, 1.2], fs=6.7, status_col=4)
src("A12 = `L/logs/A12_ohs12_result.md` (git 629a9f4); ejs-5 = `B/ejs5/runs/scores_c1_4be.json` (aggregates; git 32ee1f9); "
    "JevBench = `B/runs/scores_v154_c1.json`, `B/v154/RESULTS_30sep.md`; Decision Index = `B/decision_index/report_sample10k.json` "
    "(git 18c024c). All parsed LIVE: A12 " + ("MATCH" if A12_OK else "CHECK") + ", ejs-5 " + ("MATCH" if EJ_OK else "CHECK")
    + ", JevBench " + ("MATCH" if JB_OK else "CHECK") + ", Decision Index " + ("MATCH" if DI_OK else "CHECK") + ".")
h2("6.2 Which system was measured where")
T([["System", "Dev (9 splits)", "OHS-1 / OHS-2", "ejs-5", "JevBench v1.5.4 public", "Decision Index", "Jagged / OPI / redef",
    "OHS-3 / sealed suite"],
   ["**C1** `q35_4b_main500k` (shipped)", "yes (gate job 1; B re-read)", "yes / yes (A12)", "yes", "yes", "yes (10K sample)",
    "yes / yes / yes", "no / no"],
   ["4B-E `q35_4b_pxE` (reference; 2B teacher)", "yes", "never", "yes (report-only)", "yes", "no", "yes / yes / yes", "no / no"],
   ["Step B candidates (a = 0.6-0.9)", "yes (dev only)", "no", "no", "no", "no", "no", "no"],
   ["Older 4Bs (v10, v11b, v11c)", "yes", "yes (preds)", "no", "v1.4.2 only", "no", "v10, v11c", "no"],
   ["Jev (jev-1.13-20260917)", "never", "yes, 2 runs", "published answers", "yes (p1, p2)", "published full suite",
    "yes / yes / never", "planned once / once"],
   ["2B (paused)", "yes", "no", "no", "pilot only", "no", "pilot", "no"]],
  [2.2, 1.3, 1.1, 1.0, 1.1, 1.1, 1.2, 1.1], fs=6.8)
h2("6.3 OHS-1 and OHS-2 (practice sets since A12)")
T([["System", "OHS-1 micro", "Δ vs Jev [95% CI]", "OHS-1 macro", "OHS-1 Brier", "OHS-2 micro", "Δ vs Jev [95% CI]",
    "OHS-2 macro", "OHS-2 Brier"],
   ["**Jev** (mean of 2 runs)", a12("OHS-1", "jev", "81.7"), "–", a12("OHS-1", "mac_jev", "81.5"), a12("OHS-1", "br_jev", "0.114"),
    a12("OHS-2", "jev", "81.5"), "–", a12("OHS-2", "mac_jev", "82.0"), a12("OHS-2", "br_jev", "0.038")],
   ["**C1** (A12; A5 readout)", a12("OHS-1", "c1", "80.4"), a12d("OHS-1"), a12("OHS-1", "mac_c1", "80.1"),
    a12("OHS-1", "br_c1", "0.140"), a12("OHS-2", "c1", "81.0"), a12d("OHS-2"), a12("OHS-2", "mac_c1", "81.3"),
    a12("OHS-2", "br_c1", "0.057")],
   ["4B v11c (best earlier 4B; 1 Oct record)", "78.02 (_cal)", "−3.63 [−5.26, −2.00]", "–", "0.1450", "79.92",
    "−1.63 [−3.30, +0.11]", "80.64", "0.0831"],
   ["4B v10", "76.12", "−5.52 [−7.29, −3.77]", "–", "0.1613", "78.26", "−3.30 [−5.04, −1.52]", "78.91", "0.0904"],
   ["Frozen Qwen3.5-4B (no fine-tune)", "75.85", "−5.79 [−7.51, −4.10]", "–", "0.1705", "–", "–", "–", "–"]],
  [2.4, 0.9, 1.6, 0.8, 0.8, 0.9, 1.6, 0.8, 0.8], fs=6.8)
bullets([
    "Pooled by rows C1 ≈ 80.65 vs Jev ≈ 81.61, about **−1.0**: below the A12 stop bar (+1), so plan C continues from C1.",
    "Readouts differ: the older rows are the 1 Oct record's readouts (single read, some calibrated); the A12 file quotes "
    "v11b −3.1 on OHS-1 and v11c −1.0 on OHS-2 on its own readout. The C1 row is the shipped A5 readout.",
    "On all 2,972 OHS-1 yes/no rows (variant layer included) the same reads give Brier 0.133 (Jev) vs 0.152 (C1); the "
    "registered endpoint uses base rows only (recipe v4 §10.3). OHS-1 and OHS-2 are never used for training or choosing.",
], st=SBUL)
h2("6.4 ejs-5: 868 software-commit decisions (pre-registered 9a04df1; run once on od-l4b)")
_pt = (EJ_C1.get("vs_jev") or {}).get("per_task") or {}
_lt = (EJ_C1.get("vs_jev") or {}).get("late_per_task") or {}
_pj = (EJ_PUB.get("jev") or {}).get("per_task") or {}
rows = [["Task (rows)", "C1", "4B-E", "Jev", "C1 − Jev [95% CI]", "Late rows: C1 − Jev"]]
for tk in ("route", "triage", "score", "gate"):
    c1t = (EJ_C1.get("per_task") or {}).get(tk) or {}
    et = (EJ_E.get("per_task") or {}).get(tk) or {}
    v = _pt.get(tk) or {}
    lv = _lt.get(tk) or {}
    rows.append([f"{tk} ({c1t.get('n', '?')})", f"{100 * c1t.get('accuracy', 0):.1f}", f"{100 * et.get('accuracy', 0):.1f}",
                 f"{100 * _pj.get(tk, 0):.1f}",
                 f"{100 * v.get('diff', 0):+.1f} [{100 * (v.get('ci95') or [0, 0])[0]:+.1f}, {100 * (v.get('ci95') or [0, 0])[1]:+.1f}]",
                 f"{100 * lv.get('diff', 0):+.1f} (n {lv.get('n_rows', '?')})"])
rows.append(["**Pooled (868)**", f"**{EJ_C1P:.2f}**", f"{100 * EJ_E.get('overall_pooled', 0):.2f}", f"{EJ_JEVP:.2f}",
             f"**{ej_diff(EJ_C1)}** (4B-E {ej_diff(EJ_E)})", f"{ej_diff(EJ_C1, 'late_overall_pooled')} (n 268): tie"])
rows.append(["Macro (4 tasks)", f"{100 * EJ_C1.get('overall_macro', 0):.2f}", f"{100 * EJ_E.get('overall_macro', 0):.2f}", "64.40",
             "–", "–"])
T(rows, [1.4, 0.8, 0.8, 0.8, 2.6, 2.2], fs=7)
sp(5)
T([["Reference systems on the same 868 rows (published answers; context only)", "Pooled", "Macro", "From 1 Jun 2026 (268)"],
   ["Claude Opus 5", f"{100 * (EJ_PUB.get('opus') or {}).get('overall_pooled', 0.6809):.2f}%", "74.20%", "61.57%"],
   ["GPT-5.6 Terra", f"{100 * (EJ_PUB.get('gpt') or {}).get('overall_pooled', 0.6106):.2f}%", "66.85%", "50.75%"],
   ["**Jev 1.13**", f"**{EJ_JEVP:.2f}%**", "64.40%", "45.90%"],
   ["**C1** (ours)", f"**{EJ_C1P:.2f}%**", f"{100 * EJ_C1.get('overall_macro', 0):.2f}%", f"{100 * EJ_LATE.get('ours', 0):.2f}%"],
   ["Keyword-regex baseline", "43.4% (ORCH)", "–", "–"]],
  [3.6, 1.2, 1.2, 1.6], fs=7)
bullets([
    "**C1 ranks 4th of 5** (above only the keyword regex). The verdict rule is a paired bootstrap over the 622 commits; "
    "both C1 and 4B-E are clear losses; the newest rows (after Jev's likely data cutoff) are a tie.",
    f"Speed on the L4 (2 views, batch 1): p50 {(EJ_C1.get('timing') or {}).get('latency_ms', {}).get('p50', 230):.0f} ms, p95 "
    f"{(EJ_C1.get('timing') or {}).get('latency_ms', {}).get('p95', 242):.0f} ms, {(EJ_C1.get('timing') or {}).get('errors', 0)} errors (LIVE). "
    "Jev's medians in the author's run were 411-432 ms end to end (PREREG_ejs5).",
    "**My pre-run estimate was 59.6 (80%: 55.4-64.1); the result (54.1) fell below that range: the estimate was too "
    "optimistic** (ORCH). Later analysis: about 20-41 of the 38 missing items likely come from Jev's edge on older "
    "(pre-cutoff) rows, so a tie on the full set is the realistic best case (plan-C extra study 2; see 11.7).",
    "From plan C on, commit data from other repos is trained, so ejs-5 is **in-domain**: no \"unseen\" claim on it. Its "
    "gold file is never opened by this builder; only `scores_c1_4be.json` aggregates are read.",
], st=SBUL)
h2("6.5 JevBench v1.5.4: our run of the 231 public items (unofficial)")
rows = [["Run", "Intelligence", "Calib", "Speed", "Cost", "**Score A**", "Yes/no abstain", "Intelligence vs Jev p1 [95% CI]"]]
for k, lbl in JB_ROWS:
    x = JB.get(k)
    if not x:
        rows.append([lbl, "missing", "", "", "", "", "", ""])
        continue
    ax_ = x.get("axes") or {}
    pv = x.get("paired_vs_jev_p1") or {}
    rows.append([lbl, f"{ax_.get('intelligence', 0):.1f}", f"{ax_.get('calibration', 0):.1f}", f"{ax_.get('speed', 0):.1f}",
                 f"{ax_.get('cost', 0):.1f}", f"**{(x.get('scores') or {}).get('A', 0):.2f}**",
                 f"{100 * (x.get('diagnostics') or {}).get('noul_abstention_rate', 0):.1f}%",
                 (f"{pv['diff']:+.1f} [{pv['ci95'][0]:+.1f}, {pv['ci95'][1]:+.1f}]" if pv.get("ci95") else "–")])
T(rows, [2.6, 0.9, 0.7, 0.7, 0.7, 0.8, 0.9, 2.0], fs=7, hl_rows=(3,))
bullets([
    "C1 vs 4B-E on these items (`B/v154/RESULTS_30sep.md`): choice 81.8 vs 80.6; yes/no committed 65.2 vs 75.9 (hard tier "
    "47.4 vs 57.9); score 78.4 vs 79.5. 4B-E is stronger on hard yes/no here.",
    "**Caveats:** official v1.5 formulas but no sealed half and no judge tier; the public items were the dev set of "
    "4B-E's lineage, so these numbers flatter us; the L4 run is eager mode without CUDA graphs (speed axis 88.4 vs Jev's "
    "91.4 from our OpenRouter run). Band edge is the pre-registered readout (only yes/no answers between 0.2 and 0.8 are "
    "moved to 0.2 / 0.8).",
], st=SBUL)
h2("6.6 The official JevBench v1.5.4 board (snapshot 30 Sep, not re-fetched) and where we would land")
T([["#", "System", "Size", "Score A", "I", "I open / sealed", "Calib.", "Speed", "Cost"],
   ["1", "Cygnet (frozen Gemma-4-12B + shim)", "12B", "73.70", "71.1", "72.5 / 69.7", "87.0", "91.0", "56.4"],
   ["2", "Winnow-12B Q8", "12B", "73.23", "74.4", "72.5 / 76.4", "84.1", "86.1", "56.6"],
   ["**3**", "**Jev 1.13.0**", "closed", "**72.13**", "**72.0**", "71.5 / 72.5", "88.0", "83.8", "54.7"],
   ["4", "jevk5-v0.3-4b (best 4B)", "4B", "71.90", "56.3", "61.6 / 50.9", "88.3", "93.6", "63.1"],
   ["5", "Plumb-4B", "4B", "71.56", "55.8", "60.9 / 50.8", "87.4", "93.5", "63.1"],
   ["6", "Jev-Omni (12B)", "12B", "71.50", "70.5", "70.5 / 70.5", "82.6", "84.7", "56.1"],
   ["7", "decider-4b v2", "4B", "71.28", "55.8", "61.7 / 49.8", "85.6", "90.9", "64.5"],
   ["EST", "**C1, if submitted** (band edge; ROADMAP 3 Oct)", "4B", "**about 74.5 (71-77)**", "about 69 (61-75)", "–", "–", "–", "–"],
   ["EST", "C1, if submitted (orchestrator 3 Oct 05:40 UTC)", "4B", "about 72-75 (beat Jev about 65%)",
    "about 66-72 (beat Jev about 30%)", "–", "–", "–", "–"]],
  [0.4, 3.0, 0.6, 1.6, 1.4, 1.0, 0.6, 0.6, 0.6], fs=6.9, hl_rows=(3,))
src("`B/v154/leaderboard_v154.json` (fetched 30 Sep; 106 ranked systems); projections: `R/ROADMAP_2oct.md` final timeline "
    "(EST) and ORCH 05:40 UTC (EST). **Method (LIVE check of the board file):** Score A = the **harmonic mean** of "
    f"Intelligence, Calibration, Speed and Cost, equal weights. Jev {' / '.join(f'{x:.1f}' for x in _lbj)} gives "
    f"{LB_JEV_HM:.2f} (board {LB_JEV_A:.2f}; a plain average would give {LB_JEV_AM:.1f}); C1's band-edge axes give "
    f"{C1_HM:.2f} (file {(JBC.get('scores') or {}).get('A', 74.34):.2f}) ({'MATCH' if LB_HM_OK else 'CHECK'}). Board Speed + "
    "Cost: " + ", ".join(f"{k} {v:.1f}" for k, v in LB_SC.items()) + ". Re-check of the EST row: with board-like 4B Speed / "
    f"Cost (about 93 / 63), Calibration 83-88 and Intelligence 61-75, the harmonic mean is about {PROJ_LO:.1f}-{PROJ_HI:.1f}, "
    "so \"about 74.5 (71-77)\" roughly holds (EST). 4B entries drop about 10 points from open to sealed Intelligence ("
    + ", ".join(f"{k} −{v:.1f}" for k, v in LB_DROP.items()) + "). **Never submitted**; the $49 fast lane is the owner's "
    "call. Claim rule: an outside win is claimed only if JevBench sealed and ejs-5 agree (memory `fair-test-pick`); ejs-5 "
    "is now a loss.")
h2("6.7 Decision Index: C1 on a 10K sample (A13, report-only)")
rows = [["Area", "C1 (sample)", "Jev (full suite)", "Difference (pp)", "Status"]]
for a_ in DI_AREAS:
    rows.append([a_["area"] + (" (MMLU, GPQA Diamond, GSM8K, ChessBench, CRUXEval, CLadder)" if a_["area"] == "knowledge" else ""),
                 r1(100 * a_['ours_raw']), r1(100 * a_['jev_raw']), f"{a_['diff_pp']:+.2f}",
                 "LOSS" if a_["diff_pp"] < -5 else ("TIE" if a_["diff_pp"] > -1 else "BEHIND (small)")])
rows.append(["**Index** (balanced raw)", f"**{DI_OURS.get('index', 0):.2f}**", f"**{DI_JEV.get('index', 0):.2f}**",
             f"**{DI_OURS.get('index', 0) - DI_JEV.get('index', 0):+.2f}**", "LOSS"])
rows.append(["Balanced skill / breadth skill", f"{(DI_OURS.get('scores') or {}).get('balanced_skill', 0):.2f} / "
             f"{(DI_OURS.get('scores') or {}).get('breadth_skill', 0):.2f}", f"{(DI_JEV.get('scores') or {}).get('balanced_skill', 0):.2f} / "
             f"{(DI_JEV.get('scores') or {}).get('breadth_skill', 0):.2f}", "–", "LOSS"])
T(rows, [3.8, 1.1, 1.1, 1.1, 1.1], fs=7, status_col=4)
sp(5)
rows = [["Benchmark (in the index)", "C1", "Jev", "Δ pp", "Sample n", "Benchmark", "C1", "Jev", "Δ pp", "Sample n"]]
_bs = sorted(DI_BENCH, key=lambda b: b["diff_pp"])
_half = (len(_bs) + 1) // 2
for i in range(_half):
    a_ = _bs[i]
    b_ = _bs[_half + i] if _half + i < len(_bs) else None
    row = [a_["dataset"], r1(100 * a_['ours_raw']), r1(100 * a_['jev_raw']), r1(a_['diff_pp'], True), str(a_.get("sample_requests", "–"))]
    row += ([b_["dataset"], r1(100 * b_['ours_raw']), r1(100 * b_['jev_raw']), r1(b_['diff_pp'], True),
             str(b_.get("sample_requests", "–"))] if b_ else ["", "", "", "", ""])
    rows.append(row)
T(rows, [1.9, 0.6, 0.6, 0.6, 0.7, 1.9, 0.6, 0.6, 0.6, 0.7], fs=6.8)
sp(5)
rows = [["v0.1 board (index)", "Score", "Note"]]
for i, (n, s) in enumerate(DI_BOARD, 1):
    rows.append([f"#{i} {n}", f"{s:.2f}", "our sample, not the full suite (about ±1-2)" if n.startswith("**C1") else
                 ("published full suite" if n.startswith("Jev") else "published")])
T(rows, [4.6, 1.0, 3.2], fs=7, hl_rows=(DI_RANK,) if DI_RANK else ())
bullets([
    f"**Where the gap is:** the knowledge area holds {DI_K['diff_pp']:+.2f} of the area gaps (GPQA Diamond {dib('GPQA Diamond')}, "
    f"GSM8K {dib('GSM8K')}, CRUXEval {dib('CRUXEval')}, MMLU {dib('MMLU')}); language, retrieval, tools and arts are within "
    "about 3 points. C1 would sit about **#" + str(DI_RANK or 4) + "** on the v0.1 board (sample vs full suite; not "
    "paired). On the newer v0.2.1 board Jev is 57.91 and the best 4B 43.04 (competitor research).",
    f"**Set-up (A13):** harness `decision-index` pinned at 52a69892; sample seed {(DI.get('sample') or {}).get('seed', 20260919)} "
    f"({fmt((DI.get('sample') or {}).get('requests', 10001))} requests, {fmt((DI.get('sample') or {}).get('questions', 82939))} "
    f"questions); {fmt((DI_OURS.get('counts') or {}).get('ok', 9999))} ok, {(DI_OURS.get('counts') or {}).get('unsupported', 2)} "
    "unsupported (over 16,384 tokens, scored wrong). Checks: the harness reproduces Jev's 59.51; the scorer reproduces a "
    f"published full run; 0 oracle mismatches. The file also lists {DI_UNNAMED} index entries with no sample (coverage 0).",
    "**Disclosures:** 285 of 10,001 sample requests share a 12-gram with C1's training file (MuSR 160/230 = 69.6%, "
    "display-only; BRIGHT 57/230; ToolRet 23/230); BANKING77 and CLINC150 are C1 training sources (train splits; the Index "
    "uses test splits). **Report-only:** never used to choose data, families, weights or models; C's data is "
    "decontaminated against every Index test item. Per-item results are never opened (`bench/external_quarantine/` is "
    "refused by this builder).",
], st=SBUL)
h2("6.8 Dev (Jev never run on dev): C1 vs 4B-E and step B")
_gf = GSHIP.get("full") or {}
_gty = GSHIP.get("types") or {}
_gfx = (GSHIP.get("report") or {}).get("full_with_excluded") or {}
_bchk = {c.get("check", ""): c.get("detail", "") for c in BW_CHECKS}


def _bdet(prefix, side):
    """Step B confirm-half detail 'X vs Y' -> X (a*) or Y (C1)."""
    d_ = next((v for k, v in _bchk.items() if k.startswith(prefix)), "")
    m_ = re.match(r"\s*([\d.]+%?) vs ([\d.]+%?)", d_)
    return (m_.group(1) if side == 0 else m_.group(2)) if m_ else "?"


T([["Model (dev, 9 splits)", "Unseen sources (3,847 rows)", f"Full gate set ({fmt(_gf.get('n', 7056))} rows)",
    f"Yes/no ({fmt((_gty.get('noul') or {}).get('n', 3867))})", f"Choice ({fmt((_gty.get('choice') or {}).get('n', 3189))})",
    "Equivalence flips", "Complement / permutation flips"],
   ["**C1** (gate job 1)", f"{_prim.get('cand', 83.99):.2f}", f"{_gf.get('cand', 81.07):.2f}",
    f"{(_gty.get('noul') or {}).get('cand', 85.21):.2f}", f"{(_gty.get('choice') or {}).get('cand', 76.04):.2f}", "8.86%",
    "3.30% / 2.43%"],
   ["4B-E fresh read (REF)", f"{_prim.get('ref', 81.52):.2f}", f"{_gf.get('ref', 79.88):.2f}",
    f"{(_gty.get('noul') or {}).get('ref', 83.81):.2f}", f"{(_gty.get('choice') or {}).get('ref', 75.10):.2f}", "5.68%",
    "4.63% / 3.78%"],
   ["C1 re-read on od-l4b (step B REF; columns 3-7: dev-confirm half)",
    f"{(BW_C.get('q35_4b_main500k_wise090') or {}).get('all_unseen_boot', {}).get('ref', 83.99):.2f}",
    f"{_bdet('full set', 1)} (confirm half)", _bdet("yes/no", 1), _bdet("choice", 1), f"{_bdet('equivalence', 1)} (n 353)",
    f"{_bdet('complement', 1)} (n 559) / –"],
   ["Step B a* = 0.9 (columns 3-7: dev-confirm half)",
    f"{(BW_C.get('q35_4b_main500k_wise090') or {}).get('all_unseen_boot', {}).get('cand', 84.04):.2f}",
    f"{_bdet('full set', 0)} (confirm half)", _bdet("yes/no", 0), _bdet("choice", 0), _bdet("equivalence", 0),
    f"{_bdet('complement', 0)} / –"]],
  [2.4, 1.3, 1.3, 0.8, 0.8, 1.1, 1.7], fs=7)
_gex = (GSHIP.get("report") or {}).get("excluded") or {}
_gexl = list(GSHIP.get("constraint_exclude") or ["tb_mixtral"])
_gexn = ", ".join(_gexl)
_tbd_n, _tbd_x = 0, 0  # where the excluded rows sit (LIVE: count them in the dev split that holds them)
try:
    for _l in open(safe(L / "data/taskbank_dev.jsonl"), errors="replace"):
        _tbd_n += 1
        _tbd_x += json.loads(_l).get("source") in _gexl
except FileNotFoundError:
    MISSING_INPUTS.append(str(L / "data/taskbank_dev.jsonl"))
_where = (f"{fmt(_tbd_x)} of the {fmt(_tbd_n)} rows of the `taskbank_dev` split (LIVE count; the other "
          f"{fmt(_tbd_n - _tbd_x)} taskbank_dev rows and the other 8 splits stay in)"
          if _tbd_x and _tbd_x == _gex.get("n", 1087) else f"{fmt(_gex.get('n', 1087))} rows (split not re-counted)")
src("`L/logs/gate4b/look_ship1.json` (LIVE: `full` and `types` = the gate set), A10 §B-C, `L/logs/b_wiseft_result.json` "
    f"(LIVE). **What the gate set leaves out (look_ship1.json `constraint_exclude`):** the `{_gexn}` source family, "
    f"{_where}; `gate_dev.py` calls it "
    "the REF-lineage family the new model is barred from, so it is report-only (C1 "
    f"{_gex.get('cand', 83.72):.2f} vs 4B-E {_gex.get('ref', 86.20):.2f} on those rows, `report.excluded`). With them, on "
    f"all {fmt(_gfx.get('n', 8143))} dev rows: C1 {_gfx.get('cand', 81.42):.2f} vs 4B-E {_gfx.get('ref', 80.72):.2f} "
    "(`report.full_with_excluded`); the 1 Oct record §7.5 (\"Dev and dev-confirm\", the Pooled 8,143 column) gives the "
    "same pooled figures, and on the yes/no and choice rows of that wider set yes/no 85.19 / 84.52 and choice 77.14 / "
    "76.40 (C1 / 4B-E); those are not gate-set figures. Step B's checks use the "
    "dev-confirm half and their own subsets (n shown), so its complement figure (3.58%) differs from the gate's (3.30%).")
h2("6.9 Consistency")
bullets([
    "**C1 vs 4B-E on dev (A10):** complement violations 3.30% vs 4.63%; option-order (permutation) flips 2.43% vs 3.78%; "
    "equivalence flips (e) 8.86% vs 5.68% (FAIL, one frame); held-out nested negation (F7 probe) 34.52% vs 34.13%.",
    "**vs Jev:** no paired C1 data. The best earlier evidence: OHS-1 complement, v11c 11.31% vs Jev about 10.8% (tie). "
    "Jev's option-order drift was never measured (its run-to-run disagreement is 1.14-1.98%). OHS-3's consistency "
    "endpoints (complement, option order) are where C1 is stronger than 4B-E on dev.",
], st=SBUL)
h2("6.10 Security (LIVE: recomputed from the saved reads with gate_dev)")
_sec_rows = [["System (pred file)", "Jagged hijack rate k/n", "Wilson 95%", "Diff vs Jev guard [95%]", "OPI injection rate k/n",
              "Wilson 95%", "Diff vs Jev guard [95%]"]]
for n_, lbl in SEC_NAMES:
    cells = [lbl]
    for kind in ("jagged", "opi"):
        x = (SEC.get(kind) or {}).get(n_)
        if x:
            cells += [f"**{x['asr']:.1f}%** ({x['k']}/{x['n']})", f"[{x['ci'][0]:.1f}, {x['ci'][1]:.1f}]", _asr_cmp(kind, n_)]
        else:
            cells += ["missing", "–", "–"]
    _sec_rows.append(cells)
T(_sec_rows, [3.0, 1.2, 0.9, 1.6, 1.2, 0.9, 1.6], fs=6.8, hl_rows=(1,))
para(f"Definition overwrite (redef): C1 {REDEF['q35_4b_main500k']['asr']:.1f}% ({REDEF['q35_4b_main500k']['k']}/"
     f"{REDEF['q35_4b_main500k']['n']}) vs 4B-E {REDEF['q35_4b_pxE_fresh']['asr']:.1f}% (LIVE, `score_redef.py` rule); Jev "
     "never run on redef." if all(REDEF.values()) else "Redef: not available (input missing).", SMALL)
src("`L/preds_eval_jagged/`, `L/preds_eval_opi/` scored with `gate_dev.jagged_units` / `opi_units` / `asr_compare` (paired "
    "bootstrap, 10,000 resamples, seed 0). These are our own attack sets and were used for selection: not held out. No "
    "adaptive attack has been run. Jev outputs are scored here, never trained on.")
h2("6.11 Speed and cost")
T([["System", "Setup", "Latency", "JevBench speed axis", "Source"],
   ["4B-E (reference only: a different model, same size and layout as C1)", "H100, CUDA graphs, 1 read", "p50 16.6 ms (compute)", "94.7", "`L/extra/SPEED_RESULT_30sep.md`"],
   ["**C1**", "Google L4, eager, no CUDA graphs (JevBench)", f"p50 {1000 * (jbv('v154_q35_4b_main500k', 'speed', 'p50_s_raw') or 0.1137):.0f} ms raw",
    f"{(JBC.get('axes') or {}).get('speed', 88.4):.1f}", "`B/runs/scores_v154_c1.json`"],
   ["**C1**", "Google L4, 2 views, batch 1 (ejs-5)", f"p50 {(EJ_C1.get('timing') or {}).get('latency_ms', {}).get('p50', 230):.0f} ms", "–",
    "`scores_c1_4be.json`"],
   ["**C1**", "Google L4, Decision Index knowledge items (harness)", "median 242-262 ms (ChessBench 625 ms)", "–",
    "knowledge-gap plan §1"],
   ["**Jev**", "its hosted API via OpenRouter (our JevBench run `jev_p1`; never run on our L4)",
    f"p50 {1000 * (jbv('jev_p1', 'speed', 'p50_s_raw') or 0.238):.0f} ms, network included",
    f"{(JBJ.get('axes') or {}).get('speed', 91.4):.1f}", "`B/v154/RESULTS_30sep.md`; `scores_v154_all.json`"],
   ["**Jev**", "official board / published / third party", "616 ms (board); 70-500 ms end to end (official); OpenRouter "
    "p50 168 ms (a reviewer's figure, not re-checked)", "83.8 (board)", "board; market notes; 168 ms: knowledge-gap "
    "plan §1"]],
  [2.0, 2.6, 2.2, 1.1, 1.9], fs=7)
bullets([
    "**Cost per 1,000 decisions (JevBench formula):** ours $0.0245 (axis 58.3) vs Jev $0.0384 (axis 52.5), about −36%. "
    "Real serving cost was never measured (EST $0.014-0.12 per 1K depending on hardware and load).",
    f"**Speed is UNPROVEN.** Jev {_spd_jev:.1f} comes from its hosted API (our OpenRouter run `jev_p1`; Jev was never run "
    f"on our L4); C1 {_spd_c1:.1f} comes from our L4 with no fast kernels (eager mode, no CUDA graphs). C1 was never "
    "timed on an H100: the **H100 direct-hosting speed + cost test** is pending (after the ship decision; GO, about "
    "$5-8). The 4B-E H100 row is a reference for a different model, not a C1 result.",
], st=SBUL)
h2("6.12 Never measured (honest list)")
bullets([
    "OHS-3 (sealed), the sealed new-domains suite (no model has read it), LongBench v2 (kit built, never run; Jev's "
    "52.8% LongBench result was withdrawn, and the longjev repo cites TypeSafe terms that forbid publishing Jev "
    "benchmark results: **check before any public claim about Jev**).",
    "Jev on dev and on redef; Jev's option-order drift; C1's end-to-end hosted speed; real serving cost; the adaptive "
    "attack; JevBench sealed for any of our models; the round-1 model (does not exist yet).",
], st=SBUL)

# ======================================================================================= 7. projections
page(True)
h1("7. Projections after C round 1 (every number here is EST)")
note("**Current best estimate (recipe v4 §10, after A12):** plan C is a careful, low-risk step, not a jump. P(round-1 "
     "candidate ships) **about 22% (14-33%)**; P(round 2 runs) **about 13% (8-22%)**; if it ships, its true sealed gain "
     "averages about +2.1 pp; expected shipped gain about +0.5 pp. Against Jev on OHS-like domains (OHS-3) the median gap "
     "after C is **−0.8**, P(≥ Jev − 1) **56%**, P(≥ Jev) **31%**, P(≥ Jev + 1) **14%**. **This replaces the earlier "
     "\"+0.8 median, tie-or-better about 60%\" told to the owner on 3 Oct (05:40 and 14:35 UTC), which the recipe itself "
     "says is not supported after A12.** If C is truly worse than C1, the gate keeps C1: the downside is money, not a worse "
     "model.", NOTE)
h2("7.1 What was told to the owner vs the current best estimate")
T([["Target", "Told to the owner (when)", "Current best estimate (source)", "Use"],
   ["OHS-3 vs Jev", "+0.8 median; tie-or-better about 60%; ≥ +1 about 45% (05:40, repeated 14:35 UTC)",
    "**median −0.8; P(≥ Jev − 1) 56%; P(≥ Jev) 31%; P(≥ Jev + 1) 14%** (recipe v4 §10.3)", "**the lower one is current**"],
   ["Sealed new-domains suite vs C1", "+1.5 over C1 (05:40)", "round-2 candidate median +1.0 (80%: −1 to +3); round 1 about "
    "0.7 of that; P(C ships) about 22% (recipe §10.1-10.2)", "current"],
   ["ejs-5", "about 58-62, in-domain now (05:40)", "if C ships about 55 (80%: 52-58); P(≥ Jev) about 2%; P(within 2 pp) "
    "about 7%; a tie is the realistic best case", "current"],
   ["JevBench sealed (if submitted)", "Score A about 72-75 (beat Jev about 65%); Intelligence about 66-72 (beat about 30%) "
    "(05:40)", "Score A about 74.5 (71-77) vs Jev 72.13; Intelligence about 69 (61-75) vs 72.0 (ROADMAP 13:30 EDT)",
    "both shown (6.6)"],
   ["Decision Index", "top-5 on several decision tasks; about #10-20 overall (05:40)", "measured on the sample: 54.83 vs "
    "59.51, about #4 on the v0.1 board; knowledge −17.7", "measured"],
   ["LongBench v2", "a loss (05:40)", "not run (sealed)", "–"],
   ["Honesty line", "\"Not guaranteed to beat Jev on everything\" (14:35)", "\"C is a careful, low-risk step, not a jump\"; "
    "about +0.5 pp shipped gain on average (+2 when it ships)", "current"]],
  [1.6, 3.2, 3.8, 1.2], fs=6.9)
src("ORCH (orchestrator log 3 Oct 05:40, 14:35, 17:30 UTC); `L/c_spec/C_TRAIN_RECIPE.md` v4 §10 (simulation "
    "`L/c_spec/sim/gate_sim_c.py`); `R/ROADMAP_2oct.md` final timeline.")
h2("7.2 What the C plan does (recipe v4 §10.2, prior-averaged)")
T([["Scenario", "P(round 2 runs)", "P(C ships)", "P(ships, true ≥ +2)", "P(ships, true ≤ 0)", "True gain if shipped",
    "Expected shipped gain"],
   ["**Base** (part A 5,000+, 40/60 split)", "**13%**", "**22%**", "66%", "0.3%", "+2.1", "**+0.47**"],
   ["Pessimistic gain (median +0.3)", "8%", "14%", "65%", "0.3%", "+1.8", "+0.26"],
   ["Optimistic gain (median +1.8)", "22%", "33%", "66%", "0.4%", "+2.5", "+0.82"],
   ["Dev neutral (mean 0.0)", "11%", "19%", "56%", "0.3%", "+2.1", "+0.40"]],
  [2.8, 1.0, 0.9, 1.2, 1.2, 1.2, 1.3], fs=7)
para("Ship-gate power: about 77% at a true +2.0 pp sealed gain (88% at +2.5); about 2% false ship at a true 0. Round 2 "
     "power: 1% at a true round-1 gain of 0, 11% at +1.0, 47% at +2.0, 82% at +3.0. Without C, P(OHS-3 ≥ Jev) would be "
     "about 24%; C adds about 7 points, all from the 22% of runs where it ships.", SMALL)
superseded("the 30 Sep FINAL_PROJECTION (headline 4B −0.3 [−3.6, +3.2], P(4B ≥ Jev) 0.45, owner success 0.21) and the 1 "
           "Oct mixture odds (P(OHS-3 ≥ Jev) about 0.45; JevBench Score A > Jev about 0.92, rank about #1; P(I > Jev) about "
           "0.26) were made for the 4B + 2B + cascade plan before C1 shipped and before A12. They are kept in the 1 Oct "
           "record §8 and not used here.")
h2("7.3 Scorecard after C round 1: 10 axes (8 owner goal axes + 2 report-only)")
SC = [
    ["1", "Unseen-domain accuracy (sealed suite)", "≥ Jev (−1 ok)", "not measured", "OHS-like proxy median −0.8; P(≥ Jev − 1) about 56%",
     "TIE (close call)"],
    ["2", "OHS-3 accuracy", "≥ Jev (−1 ok)", "practice proxy −1.0 (ties)", "median −0.8; P(≥ Jev − 1) 56%, P(≥ Jev) 31%, "
     "P(≥ Jev + 1) 14%",
     "TIE (close call, at the −1 edge)"],
    ["3", "Hijack (jagged)", "beat", f"{C1_JAG.split(' ')[0]} vs {JEV_JAG.split(' ')[0]}", "guard D6 keeps it (fails only above "
     "max(C1 + 2 pp, 3%)); 30 Sep odds superseded, no current estimate", "WIN (own attack set; measured)"],
    ["4", "Injection (OPI)", "beat", f"{C1_OPI.split(' ')[0]} vs {JEV_OPI.split(' ')[0]}", "no planned change",
     "TIE; goal is beat (win unlikely)"],
    ["5", "Consistency", "beat", "no paired C1 data vs Jev", "guards D5; C1 better than 4B-E on OHS-3-type axes",
     "TIE / UNKNOWN; goal is beat"],
    ["6", "Speed", "beat", f"Jev {_spd_jev:.1f} via its hosted API (OpenRouter); C1 {_spd_c1:.1f} on our L4 (no fast "
     "kernels); C1 never timed on an H100",
     "H100 direct-hosting test (GO) after the ship verdict; 30 Sep odds superseded, no current estimate",
     "UNPROVEN: H100 test pending"],
    ["7", "Cost", "beat", "$0.0245 vs $0.0384 (formula)", "unchanged (same size)", "WIN (formula, not a measured cost)"],
    ["8", "JevBench (official, if submitted)", "beat", "public A 74.34 vs 68.80 (practice items; no CI)",
     "Score A about 74.5 (71-77) vs 72.13; 4B entries lose about 10 Intelligence points open → sealed; never submitted",
     "POSSIBLE, UNMEASURED (Intelligence likely below)"],
    ["9", "Calibration (allowed to lose)", "may lose", "Brier 0.140 vs 0.114", "T refit within [0.8, 1.3]", "LOSS"],
    ["10", "ejs-5 (in-domain; report-only)", "no claim", "−4.4 [−7.8, −0.9]", "P(≥ Jev) about 2%", "LOSS"]]
T([["#", "Axis", "Goal", "Now (C1, measured)", "After C round 1 (EST)", "Call (EST)"]] + SC,
  [0.3, 1.9, 0.8, 2.2, 3.5, 1.9], fs=6.9, status_col=5)
note("**Central call (EST range: at least match Jev on about 4-8 of the 10 axes).** Against the owner's goal wording: "
     "**\"beat\" is met only on hijack (measured, our own attack set) and cost (by formula)**; **ties where \"beat\" is "
     "required** on injection (win unlikely) and consistency (no paired data); **speed and JevBench are possible but "
     f"unmeasured** (speed: Jev {_spd_jev:.1f} via its hosted API, C1 {_spd_c1:.1f} on our L4 with no fast kernels, C1 "
     "never timed on an H100; JevBench never submitted, our public run used "
     "practice items, and the claim rule needs ejs-5 to agree); OHS-3 and unseen domains are close calls, **P(OHS-3 ≥ "
     "Jev) about 31%** (56% if −1 counts). Calibration and ejs-5 lose, which the goal allows. **All 8 owner goal axes at "
     "once: at most about 31% (56% if −1 counts), and likely far lower,** since injection and consistency would also "
     "have to turn from ties into wins. The Decision Index (report-only) stays a loss: even the think mode of section 8 "
     "projects 57.4 (56.2-58.6) vs 59.51.", NOTE)
h2("7.4 Track record: projections vs results (for honesty)")
T([["Projection", "Made (when)", "Projected", "Result", "Verdict"],
   ["ejs-5, C1", "3 Oct 04:35 UTC (ORCH)", "59.6 (80%: 55.4-64.1)", f"{EJ_C1P:.1f}", "MISS: too optimistic"],
   ["fix2 passes all checks", "1 Oct (agents)", "45-65%", "step 0b NO GO; never trained", "MISS"],
   ["P(OHS-3 ≥ Jev)", "30 Sep 0.45; 3 Oct 05:40 \"tie-or-better about 60%\"", "about coin flip or better",
    "practice ties −1.2 / −0.6; recipe now 31%", "REVISED DOWN"],
   ["Decision Index rank", "3 Oct 05:40 UTC", "about #10-20 overall", "about #4 on v0.1 (sample), but −4.7 vs Jev",
    "MIXED: rank better, gap real"],
   ["JevBench public Score A > Jev", "1 Oct (mixture)", "about 0.92", "74.34 vs 68.80 (public)", "MATCH (public only)"],
   ["Decision Index run time", "3 Oct 14:30 UTC", "about 1 h, then 6-9 h", "about 8 h", "slower"],
   ["Replay read", "3 Oct 19:00 UTC", "10.7-11.8 h", "running slower (shard 1 > 55 min)", "slower"],
   ["Rule sheets converge by review", "3 Oct 18:45 UTC", "2-3 rounds", "did not converge; frozen after a resolve-only pass", "MISS"],
   ["Training start", "13:30 EDT Mon morning → 17:55 UTC Sun 6 pm → 18:05 UTC Sun 11 pm → 19:00 UTC Mon early",
    "–", "not started", "slipping"]],
  [2.0, 3.0, 1.8, 2.6, 1.4], fs=6.8, status_col=4)
h2("7.5 What moves these odds most, and when we learn it")
bullets([
    "Round 1's sealed **select** result (look S1, about Tue 6 Oct): near 0 means breadth is not transferring to real text; "
    "re-plan before spending more.",
    "Sealed part B1 (commit items) and the held-out commit repos show whether the commit family transfers, before the "
    "single ejs-5 read. The hard-negation probe (report) shows whether the negation work helps.",
    "Jev's single read of the sealed suite (after the ship verdict; report-only) shows the real gap on new domains "
    "before OHS-3.",
    "The knowledge-gap route (section 8) can move the Decision Index and GPQA/GSM8K-type items, but not OHS-3 or the "
    "sealed suite as planned (it is a separate, opt-in mode).",
], st=SBUL)

# ======================================================================================= 8. knowledge gap
page(False)
h1("8. Closing the knowledge gap (research done; plan written; nothing run)")
if KG_TXT:
    note(f"**Status (LIVE):** `reports/knowledge_gap/PLAN_knowledge_gap.md`, last written {hm(KG_T)} ({edt(KG_T)} EDT), "
         f"{'revised after a skeptic review (`R_skeptic.md`)' if KG_SKEPTIC else 'before the skeptic review'}; built from "
         f"{len(KG_R)} research reports ({', '.join(KG_R)}). Launched at the owner's request (\"there has to be a way a 4B can "
         "surpass Jev\", ORCH 4 Oct about 00:45 UTC). No run, no paid call, no held-out file. **It does not change the frozen "
         "C round-1 plan (A16)**; the L4 is shared and C's crowd scoring goes first. Numbers checked in the file: "
         + ", ".join(f"{k} {'MATCH' if v else 'CHECK'}" for k, v in KG_CHECKS.items()) + ".", GOOD)
else:
    note("**Status:** research RUNNING (whl9uhvgk); no plan file yet (LIVE). Rules: any knowledge change is validated on "
         "separate dev sets with no Decision Index test overlap; the Index stays report-only; round 1 (A16) is untouched.")
h2("8.1 The finding in plain words")
bullets([
    "**The gap is mostly \"no thinking time\", not \"missing facts\".** C1 must answer in one quick read. Our own base "
    "model (Qwen3.5-4B) scores 76.2 on GPQA Diamond when allowed to think for 32K-82K tokens (model card, cited in the "
    "plan); Jev scores 78.6 and C1 39.8. With short thinking caps the score is much lower; the exact value is unknown "
    "until measured.",
    "**Best route:** keep today's fast one-pass answer as the default and add an optional \"auto\" mode: a small learned "
    "gate sends hard items to the **same 4B with thinking on and our LoRA off**, with one generic think prompt for every "
    "routed item (no per-benchmark branches; the Decision Index rules forbid prompt tuning). No new teacher, no training, "
    "C1 unchanged.",
    "**Honest limit:** this closes about **half** of the Index gap (55%, range 29-80%). Knowledge alone cannot win the "
    "Index: the other four areas trail Jev by 1.15 index points, so knowledge would need about 74.6 (6 points above Jev). "
    "MMLU (Jev 92.0) cannot be matched at 4B; GPQA only with long, slow thinking. Chance that auto mode matches Jev's "
    "knowledge area: **about 10-15%** (EST).",
    "**Tools add almost nothing to honest claims:** running CRUXEval's own code copies its answer key (as a chess engine "
    "copies ChessBench's), so both are reference-only; a 4B-written maths program adds about +1 on GSM8K.",
    "**Speed:** fast mode is unchanged, but the plan notes that our L4 numbers do not yet show fast mode beating Jev "
    "(Index knowledge items 242-262 ms on the L4 vs a Jev OpenRouter p50 of 168 ms reported by a reviewer, not "
    "re-checked; plan §1); routed items take seconds. C1 was never timed on an H100 (test pending).",
], st=SBUL)
h2("8.2 Projected effect (EST; the plan's corrected numbers)")
T([["Area", "Jev", "C1 fast (now)", "Auto, pure 4B", "Auto + model-driven tools (disclosed)", "Reference only (item code + chess engine)"],
   ["Knowledge", "68.88", "51.23", "**64.1 (58.0-69.9)**", "64.3 (58.1-70.0)", "79.8 (71.2-86.8)"],
   ["Language / retrieval / tools / arts", "62.28 / 37.01 / 73.43 / 55.95", "60.49 / 34.16 / 73.38 / 54.88",
    "same (each −1.5 to +0.5 from spill-over)", "same", "same"],
   ["**Index, other areas unchanged**", "**59.51**", "**54.83**", "**57.4 (56.2-58.6)**", "**57.4 (56.2-58.6)**", "60.5 (58.8-62.0)"],
   ["Index with the spill-over range", "–", "–", "57.4 (55.0-59.0)", "57.4 (55.0-59.0)", "60.5 (57.6-62.4)"],
   ["Share of the 4.68 gap closed", "–", "0%", "55% (29-80%)", "56% (29-80%)", "above Jev at mid (not a 4B skill)"]],
  [2.0, 1.5, 1.5, 1.5, 1.6, 1.7], fs=6.9)
T([["Benchmark", "Jev", "C1", "Auto, pure 4B (EST)", "Can a 4B beat Jev here? (plan §5)"],
   ["GSM8K", "79.9", "56.7", "88 (82-92)", "**yes, medium confidence**"],
   ["CRUXEval", "73.0", "51.5", "73 (65-82)", "tie at best"],
   ["CLadder", "72.6", "65.1", "70 (62-78)", "tie at best"],
   ["GPQA Diamond", "78.6", "39.8", "57 (45-68)", "no at short caps (a tie needs minutes of thinking)"],
   ["MMLU", "92.0", "82.5", "85 (82-87.5)", "no (capacity)"],
   ["ChessBench", "17.2", "11.7", "11.7 (not routed: > 10 options)", "maybe with a later chess fine-tune (unknown)"]],
  [1.6, 0.8, 0.8, 2.2, 4.0], fs=6.9)
T([["Option (ranked in the plan)", "Index gain EST", "Cost", "Verdict"],
   ["1. Gated think route on the same 4B (adapter off, one generic prompt, learned gate)", "+1.3 to +3.7 (mid +2.6)",
    "$0 (free L4)", "**Do first**"],
   ["2. Forgetting check + LoRA-scale probe (report-only)", "0 to +0.4", "$0", "Do (free diagnostic)"],
   ["3. Run the item's own code (CRUXEval)", "+0.4 to +1.2", "$0", "**Reference only, no claims** (copies the key)"],
   ["4. Program-of-thought for numeric word problems", "about 0", "$0", "Optional, later (tools row only)"],
   ["5. Self-distill thinking answers into the one-pass model", "+0.2 to +0.6", "$10-30 + 3-6 L4-h", "Later (after C)"],
   ["6-7. Chess fine-tune; causal-question parser", "+0.2 to +0.6 each", "later rounds", "Later, optional"],
   ["8. Retrieval (BM25 over Wikipedia)", "+0.1 to +0.3", "$0-3", "Skip for now"],
   ["9. Chess engine as a tool", "+1.6 to +2.8", "$0", "**Reference only, no claims**"],
   ["10. RL or a fact-injection LoRA", "about 0", "$40+", "Skip"]],
  [4.2, 1.6, 1.4, 2.4], fs=6.9)
h2("8.3 How it would be validated, what it costs, what the owner must decide")
bullets([
    "**Clean dev sets only** (never Decision Index test items, OHS, ejs-5, JevBench, the sealed suite or LongBench): "
    "program-made maths, code and causal sets (the only clean absolute measures), SuperGPQA and MMLU-Pro samples for "
    "paired comparisons, MMLU val/dev + ARC train/dev as no-harm guards, and a K-Skip set so the gate learns when not to "
    "route. Split 60/40 fit/confirm; sha256 frozen in a draft **amendment A17** before any read.",
    "**Ship rule for auto mode (draft A17), on 2 seeds:** every reasoning set gain LB ≥ 0 and macro gain ≥ +5 vs C1; the "
    "long-thinking level only if the science set gains ≥ +5 with LB > 0; pooled MMLU/ARC guard LB > −1.0; product-mix and "
    "K-Skip LB > −0.5; p95 latency under fixed limits; unrouted outputs bit-identical to C1; routing ignores task and "
    "benchmark names; no option-pattern tricks (a distractor re-draw test).",
    "**Honesty label:** the auto columns are labelled **\"DI-informed design\"** (the owner saw the Index gaps, which "
    "shaped the dev sets), so they do **not** fully keep A13's \"the Index never chooses\" rule; one Index look per shipped "
    "adapter, report-only.",
    "**Cost and time:** steps 0-7 about **7-10 days** of agent work and about **20-55 free L4-hours**, **$0**; optional "
    "Modal runs for steps 3 and 7 about $10-25 (GO); an H100 speed check $1-2 (GO). Later self-distill training $15-35 "
    "with its own amendment.",
    "**Owner decisions (plan §7):** (1) add a \"K-route\" step to the goal flow; (2) tools policy: executing the item's own "
    "code and the chess engine reference-only, never in claims (recommended), and build the model-driven Python tool later "
    "(recommended); (3) Decision-Index-adjacent dev splits for evaluation only; (4) approve A17 (the \"DI-informed design\" "
    "label, one Index look per shipped adapter, the certified file list); (5) accept that `effort=auto` takes seconds on "
    "routed items, with fast mode as the default.",
], st=SBUL)
src("`R/knowledge_gap/PLAN_knowledge_gap.md` §0-§7 and its corrections log (EST throughout; web sources are cited inside "
    "the plan). The plan uses only Decision Index aggregates (`report_sample10k.json`, `check_index_math.json`).")

# ======================================================================================= 9. roadmap + money
page(True)
h1("9. Roadmap, dated timeline and money")
h2("9.1 Roadmap (steps in order; dates in EDT; costs and future dates are estimates; today is Saturday 3 Oct)")
RM = [
    ["1", "A10: ship C1 by override", "DONE", "$0", "Fri 2 Oct 11:10 pm (3 Oct 03:10 UTC)", "owner (done)"],
    ["2", "JevBench public, ejs-5, step B, A12, Decision Index sample on C1", "DONE", "$0 Modal (free L4)", "Sat 3 Oct", "done"],
    ["3", "Deep research; spec + recipe v4", "DONE", "$0", "Sat 3 Oct", "–"],
    ["4", "Sealed suite v2 frozen (A15); C plan (A16, A16.1)", "DONE", "$0", "Sat 3 Oct 4:34-7:57 pm", "–"],
    ["5", "Replay draw; phase 1 (packs, formats, public rows)", "DONE", "$0", "Sat 3 Oct", "–"],
    ["6", "Replay read: C1 reads 99,069 rows (134,025 reads) on the free L4", "RUNNING", "$0", "ends Sun 4 Oct about 8 am-8 pm", "no"],
    ["7", "Phase 2: 14 families (generator → solver B → blind reads → QC)", "RUNNING", "$0", "Sun 4 Oct (may run into Mon)", "no"],
    ["8", "G9 crowd scoring (C1, 4B-E, base 4B) on the free L4, family by family", "PLANNED", "$0 (16-20 L4-h)", "Sun 4 - Mon 5 Oct", "no"],
    ["9", "Mixer + counts-only decontamination (OHS-1/2/3, Index test items, JevBench, sealed exports)", "PLANNED", "$0",
     "Mon 5 Oct", "no"],
    ["10", "Pre-flights + Modal smoke run", "PLANNED", "≤ $0.5", "Mon 5 Oct", "**GO**"],
    ["11", "**Round 1 training** (about 8,880 steps, about 6.7 h)", "PLANNED", "about $29.5 (hard stop $35)",
     "Mon 5 Oct, start early morning to evening", "**GO**"],
    ["12", "Gate reads on the L4 + look S1 → round-1 verdict", "PLANNED", "$0", "Mon night - Tue 6 Oct", "no"],
    ["13", "Round 2 (only if select ≥ +2.0, LB > 0; P about 13%)", "PLANNED", "about $57 (trimmed to the cap)",
     "data Wed 7, train Thu 8, verdict Fri 9", "**GO**"],
    ["14", "C look (confirm, once) → ship verdict", "PLANNED", "$0", "Tue 6 - Wed 7 Oct", "no"],
    ["15", "Jev's single read of the sealed suite (report-only)", "PLANNED", "OpenRouter EST $2.5-5.5", "Wed 7 Oct", "**GO**"],
    ["16", "After SHIP, report-only: ejs-5, OHS-1/2, JevBench public", "PLANNED", "$0", "Wed 7 Oct", "no"],
    ["17", "H100 speed + cost test vs Jev (direct hosting)", "PLANNED", "about $5-8", "Wed 7 - Thu 8 Oct", "**GO**"],
    ["18", "OHS-3 once (C1 or the C winner; with and without the 7 overlap units)", "PLANNED", "OpenRouter EST $1.2-2.7",
     "Wed 7 - Thu 8 Oct", "**GO**"],
    ["19", "Final report + model card (A10 disclosures)", "PLANNED", "$0", "Wed 7 - Thu 8 Oct (Sat 10 - Mon 12 with round 2)", "–"],
    ["20", "JevBench sealed submission", "OWNER DECISION", "$49 real money", "owner's call", "**owner**"],
    ["21", "Knowledge-gap route (A17; dev sets, serving stack, route code, measure)", "OWNER DECISION",
     "$0 (about 20-55 L4-h)", "7-10 days after the owner's OK; L4 after G9", "owner OK"],
    ["22", "2B and the cascade", "PAUSED", "–", "–", "owner"]]
T([["#", "Step", "Status", "Cost (EST)", "When (EDT, EST)", "GO needed?"]] + RM, [0.3, 4.2, 1.2, 1.7, 2.4, 0.9],
  fs=6.8, status_col=2)
src("`R/ROADMAP_2oct.md` (3 Oct updates and final timeline), `HANDOFF.md` (3 Oct 17:25 EDT NEXT list), `L/c_spec/C_TRAIN_RECIPE.md` "
    "v4 §4, §6, §11, A15-A16.1, ORCH (19:00 UTC: replay about 11.5 h + crowd about 16-20 h → training start about Mon 5 Oct "
    "early morning EDT). The replay read is slower than planned, so every date after it may slip by about a day.")
h2("9.2 Dated timeline (EDT; EST unless done)")
T([["Day", "What happens", "State"],
   ["**Sat 3 Oct** (today)", "A15 (4:34 pm), A16 (4:35 pm), replay draw (4:50 pm), Decision Index result (about 7:52 pm), "
    "A16.1 (7:57 pm), replay read start (about 8 pm), 14 rule sheets frozen (8:12-8:50 pm), generators start (from 8:28 "
    "pm), knowledge-gap plan (9:10 pm)", "DONE"],
   ["**Sun 4 Oct**", "replay read ends (about 8 am-8 pm); family generators, solver B, blind reads and QC; first crowd "
    "scoring as families pass QC", "RUNNING / PLANNED"],
   ["**Mon 5 Oct**", "crowd scoring ends; mixer; decontamination; smoke; **owner GO**; round 1 trains (about 7 h; start "
    "early morning to evening)", "PLANNED"],
   ["**Tue 6 Oct**", "gate reads; look S1 → **round-1 verdict** (ship decision needs the C look)", "PLANNED"],
   ["**Wed 7 - Thu 8 Oct**", "C look → ship verdict → Jev's sealed read → reports → H100 speed/cost → OHS-3 once → "
    "report (no round 2)", "PLANNED"],
   ["Wed 7 - Mon 12 Oct", "only if round 2 runs (about 13%): data Wed 7, train Thu 8, verdict Fri 9, finish Sat 10 - Mon "
    "12 Oct", "PLANNED"],
   ["Up to about 10 days", "if repairs are needed (ORCH 06:10 UTC)", "–"]],
  [1.6, 6.8, 1.4], fs=7, status_col=2)
h2("9.3 Money")
T([["Item", "Amount", "Notes"],
   ["Modal credit left (7 accounts)", f"**${BILL_LEFT:.2f}**", f"last real reading {BILL_T} (LIVE-ORCH); **$0 spent since** "
    "(no C4; every 3 Oct read on the free L4; ORCH); not re-checked (`budget_tracker.py` calls Modal billing)"],
   ["Owner cap for C (training GO)", "up to about $100", "and keep the $25 reserve: $141.46 − $100 = $41.46 ≥ $25"],
   ["C plan: smoke + round 1", "≤ $0.5 + about $29.5", "hard stop if round 1 projects over $35 (+12% s/step → about $33)"],
   ["C plan: round 2 (only on a clear win)", "about $57", "trimmed so all C spend stays ≤ $100; P(runs) about 13%"],
   ["**C plan, expected**", "**about $37**", "= $30 + 13% × $57 (recipe v4 §4)"],
   ["H100 speed + cost test", "about $5-8", "GO; after the ship decision"],
   ["**Modal total**", "**about $36-39 without round 2 (likely); about $93-96 with it; at most about $108**",
    "the worst case leaves about $33, above the $25 reserve"],
   ["OpenRouter (Jev calls)", "$6.58 left (key $7.60 of $10)", "no Jev call since 1 Oct (A12 used saved Jev reads; the Index "
    "and ejs-5 used published numbers) (ORCH)"],
   ["Planned OpenRouter", "EST $3.7-8.2", "sealed-suite read once (EST $2.5-5.5, by proportion to OHS-3) + OHS-3 (EST "
    "$1.2-2.7): **may exceed the balance; check before the GO**"],
   ["Google L4", "free credit", "used for 0b, JevBench, ejs-5, B, A12, the Index (about 8 h), the replay read (about 11-12 h+); "
    "crowd scoring next; balance not in an allowed file"],
   ["Real money (not Modal)", "$49 (+ per model)", "JevBench sealed fast lane: the owner's decision"],
   ["Knowledge-gap route", "$0 on the free L4", "or about $10-25 on Modal for steps 3 and 7 (GO); H100 speed check $1-2 "
    "(GO); later self-distill $15-35 (GO)"]],
  [2.4, 2.4, 5.0], fs=6.9)
superseded("the 2 Oct roadmap (26 rows: fix2 C4 about $8-9, relabel about $23, 2B main about $74, cascade, ejs-5 on the "
           "2B) and its budget (plan about $113-117, about $24-28 spare). fix2 never trained; the relabel and \"C4 as "
           "teacher\" are dead (A10 §D); the 2B is paused.")
h2("9.4 Plan rules (C)")
T([["Rule", "Content", "Source"],
   ["Ship gate", "confirm gain ≥ +1.0 pp with LB > 0; no domain clearly worse (P2); part B not worse (P3); guards D1-D6, D9",
    "recipe §6.4; A16"],
   ["Round-2 rule", "select gain ≥ +2.0 pp with LB > 0 + guards; otherwise the owner reviews a diagnosis first", "§6.3; owner 06:30"],
   ["Looks", "S1, (S2), C once; Jev once after the ship verdict; the sealed scorer refuses any other look", "A15; §6.2"],
   ["Candidates", "one per round (the final-step adapter); no snapshots, no blends; C replaces C1 only through the gate", "A16"],
   ["Training", "init C1; 60% replay + selective C1 anchor; LR 5e-5; one pass; `lam_ord` 1.0; seed 20261003; RL not in the plan",
    "recipe §0-§3, §8"],
   ["Data", "deny-list rulings (a)-(g); rule sheets frozen per family before its generator; G2 independent solver; G5 blind "
    "reads; counts-only decontamination before every freeze; no Jev output ever an input", "A16, A16.1; spec v4"],
   ["Never chooses", "ejs-5, OHS-1/2/3, JevBench, the Decision Index, LongBench (and no temperature fitted on them)", "A16"],
   ["Disclosures", "A10's failed conditions on the model card; OHS-3 with and without the 7 overlap units", "A10"]],
  [1.4, 6.8, 1.6], fs=6.9)

# ======================================================================================= 10. risks
page(False)
h1("10. Risks and open issues")
h2("10.1 Open issues")
_unt = [p["rel"] for p in PIN if p["git"] == "UNTRACKED"]
_unc = [p["rel"] for p in PIN if "CHANGED" in p["git"]]
T([["#", "Issue", "Why it matters", "Next step"],
   ["1", "Round 1 needs the owner's GO (about $30)", "nothing trains without it", "ask at the smoke run (Mon 5 Oct)"],
   ["2", "Projection mismatch: the owner holds \"+0.8 / about 60%\" for OHS-3", "the plan's own model says median −0.8 / "
    "31% (EST)", "this report corrects it (section 7)"],
   (["3", f"**RESOLVED** ({A162_REF}): the plan files were not in git ({PRE_A162[1]} pinned files untracked, "
     f"{PRE_A162[0]} code files changed but uncommitted, launcher unpinned); all are now committed and `modal_od.py` "
     f"`{_msha[:16]}` is pinned (LIVE)", "the audit trail no longer rests on one disk", "none; keep committing before "
     "each launch"] if PLAN_COMMITTED else
   ["3", f"Plan files not in git (LIVE): {N_UNTRACKED} pinned files untracked; **{N_CODE_UNCOMMITTED} code files changed but "
    f"uncommitted** ({', '.join(_unc + (['modal_od.py'] if MODAL_CHANGED else []))}); **the Modal launcher `modal_od.py` "
    "is unpinned** (not in A16/A16.1) although it will run round 1",
    ("the pinned files are fixed only by sha256 in A16/A16.1, and the launcher not at all; a disk failure would break the "
     f"audit trail; disk {LIVE['disk_used_pct']:.0f}% full, {LIVE['disk_free_gib']:.0f} GiB free (LIVE)")
    if LIVE["disk_free_gib"] else "pinned only by sha256; launcher unpinned",
    "**owner decision (page 1):** commit them, and record the launcher's sha256 before launch; or back them up"]),
   ["4", "OHS-3 config template and runbook still name 4B-E", "since A10 the shipped model is C1", "amend at the OHS-3 step "
    "(C1 sha 507d1c29..., A5 readout)"],
   ["5", "PREREG_OHS3 rule 4 vs the A5 readout and the timing pass; speed/cost definition not committed",
    "speed is a goal axis", "amend before OHS-3; commit the definition"],
   ["6", "Untracked OHS-3 tools (scorer, hosting, harness)", "the run must use committed code", "commit before the run"],
   ["7", "OpenRouter balance ($6.58) may not cover the sealed read + OHS-3 (EST $3.7-8.2)", "a Jev read cannot be redone",
    "check the balance before the GO"],
   ["8", "\"≥ Jev\" exists only as the owner's 3 Oct wording (ORCH)", "a win must be judged by a written rule",
    "write it into the OHS-3 amendment"],
   ["9", "LongBench / TypeSafe terms (longjev cites terms that forbid publishing Jev results)", "legal risk of public claims",
    "check before any public claim about Jev"],
   ["10", "Replay read slower than planned; one GPU (quota 1; increase denied twice)", "every later date may slip",
    "re-estimate after shard 1; free L4 only (owner)"],
   ["11", "Rule sheets did not converge by review (frozen anyway)", "label errors would hurt the new families",
    "rely on G2 solver B, G3/G4 and G5 blind reads"],
   ["12", ("Family length flags: " + ("F13 about 6.0-6.5K tokens served (v4 assumed 4.6K); " if F13_LEN else "")
           + ("F10 card printed twice; " if F10_LEN else "") + ("F6 7/36 wordings fail" if F6_WORDINGS else "")),
    "longer rows raise cost (+12% s/step → about $33)", "stop-and-report rule; replace F6 wordings"],
   ["13", "The round-1 config still holds `FILL_NEW_SEED`", "A16 fixes seed 20261003; the file's sha will change when filled",
    "fill mechanically; note the new sha at launch"],
   ["14", "Knowledge-gap plan: 5 owner decisions", "it cannot start without them", "owner (section 8.3)"],
   ["15", "Agents repeatedly globbed OHS-3 file names on 2-3 Oct (names/counts only, disclosed)", "isolation risk with many "
    "agents", "keep the never-open lists in every prompt; this builder refuses those paths"],
   ["16", "Jev never run on redef", "an injection-type claim is incomplete", "decide before OHS-3"],
   ["17", "**Isolation hygiene (report inputs):** the facts pass for this report read plan-C research and review files that "
    "C_DATA_SPEC v4 says name sealed-suite candidates (disclosed in 11.7)", "A15 says the orchestrator never saw source "
    "names; that may no longer hold. This PDF names none", "stop reading or citing those files as report inputs; keep "
    "FACTS_3oct.md and MAP.md out of every C-builder allow-list"],
   ["18", "The 1 Oct record said C1's data had \"no model labels\"; that was wrong as written. The 10.2 lineage bullet "
    "now states C1's data plainly (vote-share and exact soft targets at kd 0.5, a legacy replay pool, switched-off "
    "old model-teacher labels) and keeps the 4B-E lineage line", "a shared version must not repeat the 1 Oct wording",
    "use the 10.2 wording in any shared version; **owner question:** keep or shorten the 4B-E lineage line"],
   ["19", "Owner question \"can Claude be the teacher?\" (ORCH)", "it breaks the no-bigger-teacher rule (2.5) and the claim; "
    "terms may restrict it", "**owner's call** (page 1); if yes, a separate, disclosed, pre-registered experiment"]],
  [0.3, 3.4, 3.0, 2.3], fs=6.7)
h2("10.2 Risks")
bullets([
    "**C will most likely not ship** (P about 22% EST). The likely outcome is that C1 stays, at about −1 vs Jev on "
    "OHS-like tests. The downside is money (about $37 expected), not a worse model: the gate keeps C1.",
    f"**The knowledge gap has two parts** (Index knowledge {r1(DI_K['diff_pp'], True)} points; section 8): the reasoning "
    f"items (GPQA Diamond {dib('GPQA Diamond')}, GSM8K {dib('GSM8K')}, CRUXEval {dib('CRUXEval')}) are mostly a "
    "**thinking-time gap** that an optional think mode could narrow (EST: about half of the Index gap); MMLU (Jev "
    f"{dibraw('MMLU', 'jev_raw', '92.0')} vs C1 {dibraw('MMLU', 'ours_raw', '82.5')}) is a **capacity limit** that a LoRA "
    "cannot fix.",
    "**One GPU** for the replay read, crowd scoring, gate reads and the knowledge-gap work; the replay read is already "
    "slower than planned.",
    "**Label quality vs time:** the family rule sheets were frozen without converging by review; new families can carry "
    "label errors until G2/G5 pass.",
    "**Isolation:** a sealed-text spill happened (cleaned, disclosed); many agents mean continuing risk.",
    "**OHS-3 overlap:** 7 training units share 12-grams with OHS-3; report with and without them.",
    "**C1 shipped by override** with a failed consistency check and a failed fix pre-check (both C1 and 4B-E are weak on "
    "nested negation, about 34% flips): on the model card; C1 cannot teach the 2B.",
    "**ejs-5 is no longer unseen** once commit data trains; closing its gap is unlikely (P about 2% EST).",
    "**Calibration:** Jev's Brier is better on OHS-1/2; plan C refits temperature only by leave-one-group-out within "
    "[0.8, 1.3].",
    f"**Speed claim UNPROVEN:** Jev {_spd_jev:.1f} via its hosted API (OpenRouter); C1 {_spd_c1:.1f} on our L4 (no fast "
    "kernels); C1 never timed on an H100: H100 test pending. Raw latency (sourced): C1 median about 242-262 ms on the L4 "
    "on Decision Index knowledge items vs a Jev OpenRouter p50 of about 168 ms reported by a reviewer (knowledge-gap plan "
    f"§1, not re-checked; our own JevBench OpenRouter run measured Jev at p50 "
    f"{1000 * (jbv('jev_p1', 'speed', 'p50_s_raw') or 0.238):.0f} ms).",
    "**Security claims are not held out:** jagged and OPI were used for selection; no adaptive attack.",
    "**Session interruptions:** the app quit once (about 14:30 UTC) and the usage limit was hit (17:25 EDT); long "
    "workflows may need a relaunch.",
    "**Public JevBench items are a dev set** and do not predict the sealed board.",
    "**Lineage must be disclosed:** 4B-E descends from v13t ← v11c ← v11b ← (0.3 v10 + 0.7 v11); v10 includes "
    "Qwen3-235B-authored items and the v0.11 task-bank texts are by Mixtral (FINETUNE_PLAN §3.8). **C1** trained on "
    "golden set v14 (`golden_train.jsonl`, sha256 ff7a395b..., = C1's `train_meta.json`) with soft-label distillation at "
    f"kd {CFG4.get('kd', 0.5)} on {fmt(CFG4.get('expect_kd_targets', 43363))} targets: annotator vote shares from "
    f"human-labelled sources plus {fmt(CFG4.get('expect_kd_full', 238))} exact program probabilities (`runs/README.md`, "
    "`logs/label_check_30sep.md`, `logs/overnight_plan_28sep.md`; re-counted in the file 3 Oct). These targets are not "
    "4B-E labels (4B-E's labels were made for the 2B file). The file also holds a legacy replay pool (v13 clean pool, "
    f"{GC_REPLAY} rows) from older training sets, and 45,103 rows that carry old model-teacher soft labels, which the "
    "run switched off (`kd_skip_src` blend50, the \"no old-teacher kd\" rule; those rows train on their gold labels). "
    "**Correction:** the 1 Oct record's "
    "\"no model labels\" was wrong as written (the training file carries those switched-off model-teacher labels and "
    "the legacy replay pool) and is corrected here (open issue 18).",
], st=SBUL)
h2("10.3 Discrepancies between documents (for verifiers)")
_gaps = []
for nm in ("A14", "A15", "A16", "A16.1") + (("A16.2",) if AM["A16.2"]["in_head"] else ()):
    a_ = AM[nm]
    if a_["stated"] and a_["time"]:
        _gaps.append(f"{nm} header {a_['stated'].strftime('%-d %b %H:%M')} vs git {hmu(a_['time'])}")
bullets([
    "**#1 Amendment times:** " + "; ".join(_gaps) + " (UTC, LIVE). The texts are dated 10-25 minutes after their commits; "
    "A8′ and A10-A13 match within minutes. Git time is the authority; the required order holds by git.",
    "**#2 OHS-3 overlap:** golden v14's D4 check found 0 exact and 0 13-gram overlaps; the owner's counts-only 12-gram check "
    "found 7 units (A10 §D). Different n-gram sizes and scopes; both are reported.",
    "**#3 Spec v4 sha:** the orchestrator noted `6b4f39ba` at 16:30 UTC; A16 pins `4ca12996` (the file on disk, LIVE MATCH). "
    "A polish pass changed it after the note; A16 is authoritative.",
    f"**#4 Replay draw:** the 19:00 UTC note says 99,073 rows / 134,582 reads; the written draw has "
    f"{fmt(RW1.get('rows', 0))} rows / {fmt(RW1.get('reads_A5', 0))} reads (LIVE). Round 1 uses 90,000 of the drawn rows; "
    "the margin serves crowd and anchor selection.",
    "**#5 Training-start ETA:** \"Mon 5 Oct morning\" (final timeline 13:30 EDT) → \"Sun 6 pm\" (17:55 UTC) → \"Sun 11 pm "
    "EDT\" (18:05 UTC) → \"Mon early morning\" (19:00 UTC); the replay read is now slower. This report gives a range (Mon 5 "
    "Oct, early morning to evening, EST).",
    "**#6 JevBench sealed projection:** ROADMAP says Score A about 74.5 (71-77), I about 69 (61-75); the 05:40 UTC note "
    "says A about 72-75, I about 66-72. Both are shown (6.6); both are EST.",
    "**#7 Decision Index rank:** projected about #10-20 overall (05:40 UTC) vs about #4 on the v0.1 board (sample, not "
    "paired; about ±1-2).",
    "**#8 OHS-3 runbook / config template** name 4B-E as the shipped 4B; since A10 it is C1 (amend at the OHS-3 step).",
    f"**#9 PREREG_FINAL header** still says DRAFT (LIVE: {'yes' if PREREG_DRAFT else 'no'}); A0 adopted the file. §1 still says "
    "the 2B has no PRISM-X (the 2B is paused).",
    "**#10 OpenRouter:** the balance ($6.58) vs the planned Jev reads (EST $3.7-8.2) (open issue 7).",
    "**#11 No A9:** option D was blocked and never committed; the PREREG goes A8′ → A10.",
    "**#12 Seed:** A16 fixes seed 20261003 but `runs/q35_4b_c_r1.json` (pinned f3bb379e) holds `FILL_NEW_SEED`; filling it "
    "changes the file's sha (A16 lists the mechanical fills).",
    "**#13 Complement figures:** A10 gives C1 3.30% vs 4B-E 4.63% (gate set); step B's check gives C1 3.58% (its own subset, "
    "n 559). Both are right for their sets.",
    "**#14 OHS older rows:** the 1 Oct record's scoreboard had v11c_cal −3.63 on OHS-1 and v11c −1.63 on OHS-2; the A12 file "
    "quotes v11b −3.1 and v11c −1.0 (different readouts).",
], st=SBUL)

# ======================================================================================= 11. verify
page(True)
h1("11. How to verify")
h2("11.1 Identity and amendments (LIVE at build time)")
T([["Check", "Value (LIVE)", "Expected"],
   ["`git rev-parse --abbrev-ref HEAD`", LIVE["branch"], "freeze/4b-main500k"],
   ["`git rev-parse HEAD`", LIVE["head"], "18c024c... (A16.1) or later"],
   ["`git rev-parse final-frozen`", LIVE["tag"], "82b07d4baddd2b8e53b3f3f4b479379e23b132c9 (C1's code)"],
   ["`git log -3`", " | ".join(LIVE["gitlog"]), "18c024c, 27d8b0a, 3abd721 (or newer)"],
   ["`git worktree list`", " | ".join(LIVE["worktrees"]), "2: this one and the paused 2B worktree jev-2b"],
   ["`git status -- PREREG_FINAL.md`", LIVE["prereg_status"] or "(clean)", "(clean)"]],
  [2.6, 4.8, 2.4], mono_cols=(1,), fs=6.8)
rows = [["Amendment", "Commit (LIVE)", "Git time UTC", "EDT", "Text in HEAD", "What"]]
for name, cid, marker, what in AMEND:
    a_ = AM[name]
    rows.append([name, a_["commit"], hm(a_["time"]), edt(a_["time"]), "MATCH" if a_["in_head"] else "MISSING", what])
for cid, what in RESULT_COMMITS:
    h_, t_ = RC[cid]
    rows.append(["result", h_, hm(t_), edt(t_), "–", what])
T(rows, [0.8, 0.8, 1.5, 1.6, 0.8, 4.3], fs=6.8, status_col=4)
h2("11.2 Hashes (LIVE)")
rows = [["File (L/)", "What", "sha256 (LIVE)", "Pin", "Pin in the A16/A16.1 text", "Git"]]
for p in PIN:
    rows.append([p["rel"], p["what"], (p["sha"] or "missing")[:32] + "...", f"{p['pref']} ({p['am']})",
                 "MATCH" if (p["match"] and p["in_text"]) else "MISMATCH", p["git"]])
T(rows, [2.2, 1.7, 2.6, 1.5, 1.0, 1.5], mono_cols=(0, 2), status_col=4, fs=6.5)
rows = [["File", "sha256 (LIVE)", "Lines (LIVE)", "Expected", "Check"]]
for rel, pref, nrow in DATA_FILES:
    dd = LIVE["data"].get(rel)
    if dd:
        ok = dd["sha"].startswith(pref) and dd["lines"] == nrow
        rows.append([f"L/{rel}", dd["sha"], fmt(dd["lines"]), f"{pref}... / {fmt(nrow)}", "MATCH" if ok else "MISMATCH"])
    else:
        rows.append([f"L/{rel}", "missing", "–", pref, "MISSING"])
for sub, (sh, pref) in BKSHA.items():
    rows.append([f"C1 backup {'final' if sub == '.' else sub.split('/')[-1]} adapter", sh or "missing", "–", pref,
                 "MATCH" if sh and sh.startswith(pref) else "MISMATCH"])
T(rows, [2.6, 4.2, 0.8, 1.4, 0.8], mono_cols=(1,), status_col=4, fs=6.6)
src("Adapters: `/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k/` (one local copy per model). Code at "
    "the tag and in the working copy: section 3.3.")
h2("11.3 Commands to re-run the checks (all read-only, CPU, no network)")
code([
    "# Identity, amendments, pins",
    "cd /Users/aryamahadik/Documents/jev && git log --oneline -12 && git rev-parse final-frozen",
    "git show -s --format='%h %ci %s' c35de00 132cd2a c11e4a9 86f59dd 8f1a9eb a79e5d4 3abd721 27d8b0a 18c024c",
    "cd opendecide-data/lean && shasum -a 256 c_spec/C_DATA_SPEC.md c_spec/C_TRAIN_RECIPE.md c_spec/ADDENDUM_research.md runs/q35_4b_c_r1.json train_decoder.py decoder_io.py",
    "shasum -a 256 c_build/replay_sample.py c_src/common/denylist.py c_src/common/deny_aliases.json c_src/common/negcount.py",
    "git -C /Users/aryamahadik/Documents/jev show final-frozen:opendecide-data/lean/train_decoder.py | shasum -a 256   # ebdf046d... = C1's code",
    "# 3 Oct results (aggregate files only)",
    "cat logs/A12_ohs12_result.md; python3 -m json.tool logs/b_wiseft_result.json | head -80",
    "python3 -c \"import json;d=json.load(open('../../bench/ejs5/runs/scores_c1_4be.json'))['runs']['c1_main500k'];print(d['overall_pooled'],d['vs_jev']['PRIMARY_overall_pooled'],d['late'])\"",
    "python3 -c \"import json;d=json.load(open('../../bench/decision_index/report_sample10k.json'));print(d['ours'],d['jev_published_v01_full_suite'],d['areas'])\"",
    "python3 -c \"import json;r=json.load(open('../../bench/runs/scores_v154_c1.json'))['runs'];[print(k,v['axes'],v['scores']['A']) for k,v in r.items()]\"",
    "python3 -c \"import json;d=json.load(open('c_build/replay_r1_write.json'));print(d['round1_draw']['rows'],d['round1_draw']['reads_A5'],d['drops']['rows_dropped'])\"",
    "ls c_src/*/G0_FROZEN.json | wc -l; tail -20 c_build/progress_phase2.log",
    "# A15 counts: read the A15 block of PREREG_FINAL.md (domain ids only). NEVER open sealed_nd/ or c_spec/sealed_brief/",
    "sed -n '/Amendment A15 (/,/Amendment A16 (/p' PREREG_FINAL.md",
    "# Security vs Jev (rows of 6.10)",
    "PYTHONDONTWRITEBYTECODE=1 python3 -c \"import gate_dev as g;[print(k,n,sum(a for a,b in f(n).values()),sum(b for a,b in f(n).values())) for k,f in (('jagged',g.jagged_units),('opi',g.opi_units)) for n in ('q35_4b_main500k','q35_4b_pxE_fresh','jev_guard')]\"",
    "# C1 backup and the gate",
    "shasum -a 256 /Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k/adapter_model.safetensors",
    "cat logs/gate4b/look_ship1.txt; python3 -m json.tool logs/gate4b/summary.json",
    "# Rebuild this PDF (re-runs every LIVE check; refuses forbidden paths)",
    "python3 /Users/aryamahadik/Documents/jev/reports/pdf_build_3oct/build.py",
])
para("Never open: `L/sealed_nd/`, `L/c_spec/sealed_brief/`, any `*ohs3*` path, `L/prep89/`, `B/external_quarantine/`, "
     "`B/longbench_v2/` data, the ejs-5 gold, `.env` or secrets, session folders. Do not start Modal, gcloud or OpenRouter "
     "jobs (GO points).", SMALL)
h2("11.4 Verification checklist (claim → file → how)")
T([["Claim", "File(s)", "How to check"],
   ["C1 shipped by override; failed conditions disclosed", "L/PREREG_FINAL.md A10; git 132cd2a", "read the A10 block"],
   ["Step 0b NO GO; no C4; $0", "A10 §A (committed text); `logs/gate4b_fix2/` stayed on od-l4", "read; no Modal ledger row"],
   ["Step B: keep C1", "L/logs/b_wiseft_result.json; git 599c513", "verdict and checks"],
   ["OHS-1 −1.2, OHS-2 −0.6 (ties)", "L/logs/A12_ohs12_result.md; git 629a9f4", "read the table"],
   ["ejs-5 54.1 vs 58.5 (loss)", "B/ejs5/runs/scores_c1_4be.json; PREREG_ejs5.md §5-6", "aggregate keys only"],
   ["JevBench public C1 74.34 vs 68.80", "B/runs/scores_v154_c1.json; B/v154/RESULTS_30sep.md", "runs → axes, scores"],
   ["Decision Index 54.83 vs 59.51", "B/decision_index/report_sample10k.json; git 18c024c", "ours, jev, areas"],
   ["Sealed suite 7,302 items (ids only)", "L/PREREG_FINAL.md A15", "the A15 block; never the suite"],
   ["Round-1 plan and pins", "A16, A16.1; the pinned files", "shasum vs the prefixes (11.2)"],
   ["Replay draw 99,069 rows", "L/c_build/replay_r1_write.json", "round1_draw"],
   [f"{sum(G0F.values())} rule sheets frozen; {sum(OUTF.values())} non-test output files (candidates, before QC)",
    "L/c_src/*/G0_FROZEN.json; c_src/*/out/", "ls; file names only"],
   ["Security: jagged and OPI vs Jev", "L/preds_eval_jagged/, preds_eval_opi/; gate_dev.py", "the 11.3 one-liner"],
   ["C1 = the main run; backup intact", "logs/main4b_seg*.log; backup train_meta.json; adapter sha", "section 4.2 and 11.2"],
   ["Knowledge-gap projections", "R/knowledge_gap/PLAN_knowledge_gap.md", "EST only; §0, §3"]],
  [3.0, 4.2, 2.6], fs=6.8)
h2("11.5 File index (LIVE: existence, size, modification time) and missing inputs")
FILES = [
    ("Rules and plan", [L / "PREREG_FINAL.md", L / "prereg_drafts/A10_override_C1.md", L / "c_spec/C_DATA_SPEC.md",
                        L / "c_spec/C_TRAIN_RECIPE.md", L / "c_spec/ADDENDUM_research.md", L / "c_spec/LICENCE_REGISTER.md",
                        L / "runs/q35_4b_main.json", L / "runs/q35_4b_c_r1.json", BENCH / "ejs5/PREREG_ejs5.md"]),
    ("3 Oct results", [L / "logs/A12_ohs12_result.md", L / "logs/b_wiseft_result.json", BENCH / "ejs5/runs/scores_c1_4be.json",
                       BENCH / "ejs5/README.md", BENCH / "v154/RESULTS_30sep.md", BENCH / "runs/scores_v154_c1.json",
                       BENCH / "v154/leaderboard_v154.json", BENCH / "decision_index/report_sample10k.json",
                       BENCH / "decision_index/README.md"]),
    ("Plan C build", [L / "c_build/replay_r1_write.json", L / "c_build/replay_counts_dryrun.json", L / "c_build/f2_l4.json",
                      L / "c_build/f2_local_mac.json", L / "c_build/RUNBOOK_replay_reads.md", L / "c_build/L4_REPLAY_READ.sh",
                      L / "c_build/progress_phase1.log", L / "c_build/progress_phase2.log", L / "c_build/replay_sample.py",
                      L / "c_src/common/denylist.py", L / "c_src/common/negcount.py"]),
    ("Code and data", [L / "train_decoder.py", L / "decoder_io.py", L / "gate_dev.py", L / "modal_od.py", L / "od_gcp.py",
                       L / "data/v14_parts/golden_train.jsonl", L / "data/v14_parts/golden_relations.jsonl"]),
    ("C1 and the gate", [ROOT / "backups/modal_models/q35_4b_main500k", G4 / "look_ship1.json", G4 / "summary.json",
                         L / "logs/main4b_relays.md", L / "logs/budget_ledger.md"]),
    ("Status notes", [REP / "ROADMAP_2oct.md", ROOT / "HANDOFF.md", REP / "RESUME_NOTE_2oct.md", KG, OLD_PDF,
                      SCR / "FACTS_3oct.md", SCR / "MAP.md"]),
]
rows = [["Group", "Path (relative to /Users/aryamahadik/Documents/jev/)", "Size", "Modified (UTC)"]]
for grp, items in FILES:
    for p in items:
        rel = str(p).replace(str(ROOT) + "/", "")
        if exists(p):
            pp = safe(p)
            size = "dir" if pp.is_dir() else (f"{pp.stat().st_size / 1e6:,.1f} MB" if pp.stat().st_size > 1e6 else
                                               f"{pp.stat().st_size / 1e3:,.1f} KB")
            rows.append([grp, rel, size, hm(mtime(p))])
        else:
            rows.append([grp, rel, "MISSING", "–"])
            MISSING_INPUTS.append(str(p))
T(rows, [1.2, 6.2, 0.9, 1.5], mono_cols=(1,), fs=6.4)
sp(4)
_mi = sorted(set(MISSING_INPUTS))
para("**Missing inputs at build time (skipped gracefully):** " + ("; ".join(f"`{x.replace(str(ROOT) + '/', '')}`" for x in _mi)
                                                                 if _mi else "none.") + " Files moved or not on the Mac "
     "since the 1 Oct build, by design: `logs/gate4b_fix2/` (step 0b stayed on od-l4), the fix2 C4 backup (never "
     "existed), session task files (session folders are off-limits since the A15 incident). The memory folder is not "
     "opened by the builder; ORCH facts were typed in by the writer.", SMALL)
h2("11.6 Facts that come only from the live session (ORCH) and what corroborates them")
T([["ORCH fact", "Corroborating file (if any)"],
   ["Owner goal, rules and decisions of 1-3 Oct (section 5.3)", "A10-A16.1 (where committed); ROADMAP_2oct 3 Oct updates; HANDOFF 3 Oct"],
   ["0b ran at 02:10 UTC on od-l4; option D blocked; flip research", "A10 §A (numbers); none for D and the flip research"],
   ["Modal: nothing spent since 1 Oct 23:40 UTC", "budget_ledger has no Modal row after the gate; no billing file"],
   ["GPU quota request auto-denied (17:15 UTC); free L4 only (17:25 UTC)", "none (Google console)"],
   ["Replay read start (about 00:00 UTC 4 Oct), slower than planned", "`L/c_build/f2_l4.json` (the L4 check before it); progress on the VM"],
   ["Projections told to the owner (05:40, 14:35, 17:30 UTC); ejs-5 pre-run estimate", "recipe v4 §10.3 quotes the 60% figure"],
   ["ejs-5 rank (4th of 5) and the keyword-regex baseline 43.4", "PREREG_ejs5 §5 (published table; the regex row is not in it)"],
   ["Isolation incident handling (31 files)", "A15 (committed text)"],
   ["Knowledge-gap research launch and its rules", "PLAN_knowledge_gap.md §0, §6"]],
  [5.0, 4.8], fs=6.9)
h2("11.7 How this PDF was built (and its safety guards)")
bullets([
    "Builder: `/Users/aryamahadik/Documents/jev/reports/pdf_build_3oct/build.py` (reportlab, embedded Arial and Courier "
    "New TrueType), a copy of the 1 Oct builder rewritten for 3 Oct. Inputs: `FACTS_3oct.md` and `MAP.md` (written by the "
    "facts and mapper passes on 4 Oct about 01:00-01:15 UTC, read by the writer), the aggregate files in 11.5, git, and "
    "the ORCH facts. One chart (`reports/pdf_build_3oct/loss_main500k.png`) is rendered from the 5 segment logs.",
    "**Guards kept:** read-only on the project (every open() is wrapped; a write outside `reports/pdf_build_3oct/` and the "
    "output PDF stops the build); git without index locks and with read-only subcommands only; no Modal, gcloud, ssh, "
    "OpenRouter or paid call (billing typed in with a sum assert); `gate_dev.py` imported without bytecode; fault-tolerant "
    "readers; embedded fonts with the glyph and split-word checks; tag colouring; two-pass page numbering.",
    "**Guards added:** a forbidden-path guard on every open, stat, glob and sha (sealed folders, any OHS-3 path, prep89, "
    "the Decision Index quarantine, LongBench data, ejs-5 gold, .env, session folders); the sealed suite appears only as "
    "A15's counts and domain ids; report-only tests are read as aggregates only; no new lineage line; account names only.",
    "**Isolation disclosure (review, 3 Oct evening):** the facts pass that fed this report read `REVIEW_methods.md`, "
    "`REVIEW_rules.md` and `RESEARCH_*.md` in `L/c_spec/`, and `FACTS_3oct.md` cites `RESEARCH_licensed-data.md`. "
    "C_DATA_SPEC v4 (\"Who may read what\") bars C builders from some of these files because they name sealed-suite "
    "candidates. The PDF text names no sealed-suite domain, source or theme. The Decision Index benchmark names it uses "
    "(MMLU, GPQA Diamond, GSM8K, CRUXEval, CLadder, ChessBench and the others in 6.7) are the public Decision Index "
    "board's own names, read from `B/decision_index/report_sample10k.json`: public information, not sealed-suite "
    "names. This builder opens none of the barred files. But the report's inputs did "
    "touch candidate-naming files, so A15's statement that the orchestrator never saw source names may no longer hold. "
    "From now on these files are not read or cited as report inputs, and `FACTS_3oct.md` and `MAP.md` stay out of every "
    "C-builder allow-list (open issue 17).",
    f"Build stats: {GUARD['opens']} guarded opens so far at this point of the build; missing inputs: {len(_mi)}.",
])

# ======================================================================================= appendix
page(False)
h1("Appendix A. Paused: the 2B and the cascade")
para("The owner paused the 2B on 3 Oct 04:45 UTC (\"forget the 2B for now; focus on the 4B\"). Nothing below is being "
     "worked on; it is kept so the work can resume.", SMALL)
T([["Item", "State when paused"],
   ["Architecture", "Final 2B = layout E + PRISM-X I (owner override 30 Sep 12:30 UTC, for security: jagged 1.1% vs 10.0% "
    "at tied accuracy, matched pair X18)"],
   ["Teacher", "4B-E 2-view labels (`train_2b_golden_kd_2view.jsonl`, 450,170 KD targets); A10 §D: C1 is not eligible, "
    "no relabel (the 2 Oct relabel plan, about $23, is dead)"],
   ["Hard yes/no data (yn2b)", "6 families built and checked on 1 Oct: 18,359 train rows; arm files A/B/C ready"],
   ["Worktree", (next((x for x in LIVE["worktrees"] if "jev-2b" in x), "jev-2b (not listed)") + " (LIVE)")],
   ["Cost not spent", "2B A/B pilot + main run about $74 (2 Oct plan), cascade readouts, 2B ejs-5"],
   ["To resume", "an owner decision; the 2B would follow C's outcome (teacher stays 4B-E unless a new amendment)"]],
  [1.6, 7.4], fs=7)
sp(10)
h1("Appendix B. What this edition supersedes")
T([["In the 1 Oct record", "Now"],
   ["4B-E stays the shipped 4B / pre-registered fallback", "**C1 is shipped** (A10 owner override)"],
   ["fix2 / C4 top-up next (about $9-11), job 3 re-test", "step 0b NO GO; C4 never trained; $0"],
   ["2 Oct roadmap: 2B teacher, 2B A/B, 2B main, cascade, ejs-5 on the 2B", "replaced by the 4B-only plan C; 2B paused"],
   ["Scoreboard OHS rows from older 4Bs (v11c: −3.63 / −1.63)", "C1: −1.2 / −0.6 (A12); OHS-1/2 are practice sets"],
   ["JevBench public row showed 4B-E", "C1 band edge 75.1 / 74.34"],
   ["Projections (30 Sep FINAL_PROJECTION; 1 Oct mixture)", "recipe v4 §10 after A12 (section 7)"],
   ["Budget: about $113-117 planned, about $24-28 spare", "about $141 left; C cap about $100; expected about $37"],
   ["Goal: 4B + 2B + cascade", "4B only; beat or match Jev (section 2.1)"]],
  [4.6, 4.4], fs=7)


# ======================================================================================= document
PAGE_TOTAL = ["?"]


class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, **kw)
        fp = Frame(MX, MB, PW, PAGE_P[1] - MT - MB, id="fp", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        fl = Frame(MX, MB, LW, PAGE_L[1] - MT - MB, id="fl", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="port", frames=[fp], onPage=self.header, pagesize=PAGE_P),
                               PageTemplate(id="land", frames=[fl], onPage=self.header, pagesize=PAGE_L)])

    @staticmethod
    def header(c, doc):
        w, h = c._pagesize
        c.saveState()
        c.setFont("Arial", 7.2)
        c.setFillColor(GREY)
        c.drawString(MX, h - 30, "OpenDecide vs Jev: status record, 3 Oct 2026 (evening)")
        c.drawRightString(w - MX, h - 30, f"newest input {snap_s}; built {hm(LIVE['build'])}")
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(MX, h - 34, w - MX, h - 34)
        c.drawRightString(w - MX, 22, f"Page {c.getPageNumber()} of {PAGE_TOTAL[0]}")
        c.drawString(MX, 22, "Tags: ORCH = live-session fact; LIVE-ORCH = orchestrator's live reading; LIVE = recomputed "
                              "at build; EST = estimate")
        c.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ("H1", "H2"):
            txt_ = f.getPlainText()
            lvl = 0 if f.style.name == "H1" else 1
            key = "h" + hashlib.md5(txt_.encode()).hexdigest()[:12]
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(txt_, key, level=lvl, closed=lvl > 0)
            self.notify("TOCEntry", (lvl, txt_, self.page, key))


def make_doc():
    return Doc(str(OUT), pagesize=PAGE_P, leftMargin=MX, rightMargin=MX, topMargin=MT, bottomMargin=MB,
               initialFontName="Arial", initialFontSize=9, initialLeading=11,
               title="OpenDecide vs Jev: status record (3 Oct 2026, evening)", author="OpenDecide (built by Claude)",
               subject="Plain-language summary, status, current goal, 2-3 Oct events, benchmarks vs Jev, projections, "
                       "knowledge-gap plan, roadmap and money, risks, verification index")


# pass 1 learns the page count, pass 2 writes "Page N of M" (a deferred-page canvas broke the PDF bookmarks)
_story_pass2 = copy.deepcopy(story)
doc = make_doc()
doc.multiBuild(story)
PAGE_TOTAL[0] = doc.page
doc = make_doc()
doc.multiBuild(_story_pass2)
if doc.page != PAGE_TOTAL[0]:
    print("WARNING: page count changed between passes", PAGE_TOTAL[0], doc.page)
print("wrote", OUT, "| pages", doc.page)
print("C1 backup sha ok", BK_OK, "| pins ok", PINS_OK, f"({N_UNTRACKED} untracked, {N_UNCOMMITTED} uncommitted)",
      "| A15 text ok", A15_OK, "| A10 text ok", A10_OK, "| amendments in HEAD", all(a["in_head"] for a in AM.values()))
print("A12", A12_OK, "| ejs-5", EJ_OK, "| JevBench", JB_OK, "| DI", DI_OK, "| replay draw", RW_OK, "| G0 frozen",
      sum(G0F.values()), "| production rows", sum(OUTF.values()), "| KG plan", bool(KG_TXT), KG_CHECKS)
print("security:", {k: {n: round(v["asr"], 1) for n, v in d.items()} for k, d in SEC.items()}, "| redef",
      {k: round(v["asr"], 1) for k, v in REDEF.items() if v})
print("guarded opens:", GUARD["opens"], "| missing inputs:", sorted(set(MISSING_INPUTS)))
if BAD_GLYPHS:
    print("WARNING: characters missing from Arial:", sorted(BAD_GLYPHS))
else:
    print("BAD_GLYPHS: none")
if SPLIT_WORDS:
    print("WARNING: words wider than their table cell (split mid-word):", SPLIT_WORDS)
else:
    print("SPLIT_WORDS: none")
