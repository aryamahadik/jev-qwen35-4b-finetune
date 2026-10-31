"""EXISTS head of solver B. EX-A1 / EX-A2 / EX-B1: membership recomputed from the RENDERED listing (complete lists; absence is provable only
inside the stated range). EX-B2: membership in the sha-bound stdlib export handed in as a plain dict {lang: {module: [names]}}.
EX-B1 and EX-B2 both REQUIRE that export and its sha (Opus ruling Q3a, 18 Oct): no export, no configured sha, a fixture, a witness without a sha or a
different sha -> abstain; for EX-B1 the label read off the shown list must also equal the export's membership, else abstain. Stdlib only."""
import re

from .common import Abstain, norm_ws, require_sha

LANG_WORD = {"python": "Python 3.12", "node": "Node 24", "go": "Go 1.26"}
REQUIRED_DEFS = (
    "a name exists in a module when attribute access on the module works, including names the module re-exports",
    "only public names (no leading underscore) count",
    "a list marked complete for a range names every entry in that range; a name inside the range that is not listed does not exist",
    "answer yes if the name exists, otherwise no",
)
_SHAPE_NAME = r"[a-z0-9]+(?:[-_.][a-z0-9]+)+"
_SHAPE_DOTTED = r"[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*"
_PUNCT = "\"'`.,;:?!()[]{}<>"
# words of the hand-written question frames (lower-case); used only as a last resort to drop frame words when picking the asked name
FRAME_WORDS = frozenset(
    "a about according above among an and appear appears are as at available based be been by can check complete confirm contain contains "
    "describe describes do does entries entry exist exists export exports file for found from given gives given has have hold holds in include "
    "includes is it its list listed listing lists look match matches name named names of on one only or other part present read record "
    "recorded records row rows shown shows snapshot table that the there this to under using view what whether which with within would you "
    "your anywhere carry contained decide define defined exported hit if looking lookup member mention occur provide queried reading return "
    "rules s say search set show up were when".split())


def check_definitions(context):
    flat = norm_ws(context).lower()
    for clause in REQUIRED_DEFS:
        if clause not in flat:
            raise Abstain("defs_mismatch")


def _inside(name, lo, hi):
    """Inside the alphabetical range [lo, hi]: code-point order, or case-folded order (lists sort either way)."""
    return (lo <= name <= hi) or (lo.casefold() <= name.casefold() <= hi.casefold())


def _strip_tok(t):
    return t.strip(_PUNCT)


def _quoted_pair(line):
    """'... from "lo" to "hi":' -> (lo, hi) or None."""
    a = line.find('from "')
    if a < 0:
        return None
    a += len('from "')
    b = line.find('"', a)
    c = line.find('to "', b)
    if b < 0 or c < 0:
        return None
    c += len('to "')
    d = line.find('"', c)
    if d < 0:
        return None
    return line[a:b], line[c:d]


def _bullets(lines, start):
    out, i = [], start
    while i < len(lines) and lines[i].startswith("- "):
        out.append(lines[i][2:].strip())
        i += 1
    return out, i


# ---- EX-A1 ----------------------------------------------------------------------------------------------------------------------
def parse_registry_blocks(context):
    lines = context.split("\n")
    blocks, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("Registry index for "):
            rest = ln[len("Registry index for "):]
            rid, _s, tail = rest.partition(" (")
            host, _s2, _t = tail.partition("), ")
            rng = _quoted_pair(ln)
            if not rid or not host or rng is None:
                raise Abstain("a1_header")
            names, i = _bullets(lines, i + 1)
            blocks.append({"id": rid.strip(), "host": host.strip(), "lo": rng[0], "hi": rng[1], "names": names})
            continue
        i += 1
    if not blocks:
        raise Abstain("a1_no_block")
    return blocks


def asked_registry(question, blocks):
    hit = [b for b in blocks if "%s (%s)" % (b["id"], b["host"]) in question]
    if len(hit) == 1:
        return hit[0]
    if not hit:
        hit = [b for b in blocks if re.search(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(b["id"]), question)]
        if len(hit) == 1:
            return hit[0]
    raise Abstain("a1_asked_registry")


def a1_name(question, blk, blocks):
    q = question
    for b in blocks:
        q = q.replace("%s (%s)" % (b["id"], b["host"]), " ")
    toks = [_strip_tok(t) for t in q.split()]
    toks = [t for t in toks if t]
    shaped = [t for t in toks if re.fullmatch(_SHAPE_NAME, t)]
    if len(set(shaped)) == 1:
        return shaped[0]
    pool = [t for t in toks if t.lower() not in FRAME_WORDS and _inside(t, blk["lo"], blk["hi"])]
    if len(set(pool)) == 1:
        return pool[0]
    raise Abstain("a1_name")


def solve_a1(bview):
    ctx, qtext = bview["rendered"]["context"], bview["rendered"]["question"]
    check_definitions(ctx)
    blocks = parse_registry_blocks(ctx)
    blk = asked_registry(qtext, blocks)
    name = a1_name(qtext, blk, blocks)
    if name in blk["names"]:
        return "YES", "a1_listed"
    if _inside(name, blk["lo"], blk["hi"]):
        return "NO", "a1_absent_in_range"
    raise Abstain("a1_outside_range")


# ---- EX-A2 ----------------------------------------------------------------------------------------------------------------------
def parse_library(context):
    lines = context.split("\n")
    lib = ver = None
    mods = {}
    for ln in lines:
        if ln.startswith("Library ") and "complete export list" in ln:
            body = ln[len("Library "):]
            lib, _s, rest = body.partition(" version ")
            ver = rest.split(",")[0].strip()
            lib = lib.strip()
        elif ln.startswith("module "):
            head, sep, tail = ln[len("module "):].partition(": ")
            if not sep:
                raise Abstain("a2_module_line")
            if head.strip() in mods:
                raise Abstain("a2_dup_module")
            mods[head.strip()] = [s.strip() for s in tail.split(",") if s.strip()]
    if not lib or not ver or not mods:
        raise Abstain("a2_no_library")
    return lib, ver, mods


def solve_a2(bview):
    ctx, qtext = bview["rendered"]["context"], bview["rendered"]["question"]
    check_definitions(ctx)
    lib, ver, mods = parse_library(ctx)
    scope = "%s version %s" % (lib, ver)
    if scope not in qtext:
        raise Abstain("a2_scope_mismatch")
    toks = [_strip_tok(t) for t in qtext.replace(scope, " ").split()]
    dotted = [t for t in toks if re.fullmatch(_SHAPE_DOTTED, t)]
    if len(set(dotted)) != 1:
        raise Abstain("a2_name")
    full = dotted[0]
    mod, _d, sym = full.partition(".")
    if mod not in mods:
        return "NO", "a2_module_absent"
    return ("YES" if sym in mods[mod] else "NO"), "a2_listed" if sym in mods[mod] else "a2_not_listed"


# ---- EX-B ----------------------------------------------------------------------------------------------------------------------
def parse_module_listing(context):
    lines = context.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("Exports of ") and "module" in ln:
            head = ln[len("Exports of "):]
            lang_word, _s, rest = head.partition(" module ")
            module, _s2, tail = rest.partition(" in the pinned toolchain image")
            rng = _quoted_pair(tail)
            complete = tail.strip().startswith(", complete")
            if not complete:
                raise Abstain("b1_header")
            names, _end = _bullets(lines, i + 1)
            return {"lang_word": lang_word.strip(), "module": module.strip(), "range": rng, "names": names}
    return None


def _witness(bview, keys):
    w = bview.get("witness_inputs") or {}
    if any(w.get(k) in (None, "") for k in keys):
        raise Abstain("witness_missing")
    return w


def _name_in_question(name, qtext):
    return re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(name), qtext) is not None


def _require_export(w, exports, export_sha, fixture, allow_fixture):
    """The sha-bound L-0 image-record export is MANDATORY for EX-B1 and EX-B2 (Opus ruling Q3a): source present, sha configured, not a fixture
    (unless explicitly allowed for the build-stage harness) and equal to the sha in the row's witness."""
    if exports is None:
        raise Abstain("no_export_source")
    require_sha("export", export_sha, w.get("export_sha"), fixture, allow_fixture)


def solve_b1(bview, exports=None, export_sha=None, fixture=False, allow_fixture=False):
    ctx, qtext = bview["rendered"]["context"], bview["rendered"]["question"]
    check_definitions(ctx)
    w = _witness(bview, ("lang", "module", "name"))
    _require_export(w, exports, export_sha, fixture, allow_fixture)
    lst = parse_module_listing(ctx)
    if lst is None:
        raise Abstain("b1_no_listing")
    if lst["module"] != w["module"] or lst["lang_word"] != LANG_WORD.get(w["lang"]):
        raise Abstain("b1_scope_mismatch")
    if not _name_in_question(w["name"], qtext):
        raise Abstain("b1_name_not_in_question")
    name = w["name"]
    if name in lst["names"]:
        label, reason = "YES", "b1_listed"
    elif lst["range"] is None or _inside(name, lst["range"][0], lst["range"][1]):
        label, reason = "NO", "b1_absent"
    else:
        raise Abstain("b1_outside_range")
    # the shown list is a rendering of the sha-bound export: a list that disagrees with the real export is a defect, not a label
    agree = b1_export_crosscheck(bview, label, exports)
    if agree is None:
        raise Abstain("b1_export_module_unknown")
    if not agree:
        raise Abstain("b1_export_mismatch")
    return label, reason


def solve_b2(bview, exports, export_sha, fixture=False, allow_fixture=False):
    ctx, qtext = bview["rendered"]["context"], bview["rendered"]["question"]
    check_definitions(ctx)
    w = _witness(bview, ("lang", "module", "name"))
    _require_export(w, exports, export_sha, fixture, allow_fixture)
    if not _name_in_question(w["name"], qtext):
        raise Abstain("b2_name_not_in_question")
    scope = "%s module %s in the pinned toolchain image" % (LANG_WORD.get(w["lang"], "?"), w["module"])
    if scope not in qtext:
        raise Abstain("b2_scope_mismatch")
    mods = exports.get(w["lang"])
    if mods is None or w["module"] not in mods:
        raise Abstain("b2_module_unknown")
    return ("YES" if w["name"] in set(mods[w["module"]]) else "NO"), "b2_export_lookup"


def b1_export_crosscheck(bview, label, exports):
    """True/False when the shown list and the export file agree/differ on the asked name; None when not checkable (reported by the harness)."""
    if exports is None:
        return None
    w = bview.get("witness_inputs") or {}
    mods = (exports.get(w.get("lang")) or {})
    if w.get("module") not in mods:
        return None
    return (w["name"] in set(mods[w["module"]])) == (label == "YES")
