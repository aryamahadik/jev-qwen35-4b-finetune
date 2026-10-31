"""GATE generator (G0 section 5): rules GT1, GT2, GT3, GT5 (GT1L, GT4 and GT6 are not built in round 1: their row
shares have no floor; see MANIFEST deviations), yes/no rows in two polarity frames with negated forms, message-only
slice (1.4, 5.5), threshold / class-edit / negation / attack twins (1.6), inverted gate cards (5.9).
Solver A: Python evaluator over the record. Parser + solver B: the rule re-parsed from the rendered card text into an
AST, files from the rendered diff headers and numstat, classes and atoms in sqlite (5.6, 5.7)."""
from __future__ import annotations

import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import core as K  # noqa: E402
import frame as FR  # noqa: E402
import lex2 as L  # noqa: E402
import texts as T  # noqa: E402

sys.path.insert(0, str(C.CSRC / "common"))
import negcount  # noqa: E402

CLS = L.GATE_CLASSES
CMPS = ("more than", "at least")
T_LINES = [20, 40, 80, 150, 300, 600]
T_FILES = [2, 3, 4, 6, 9]
T_CLINES = [10, 25, 60, 120]
T_CFILES = [1, 2, 3, 5]

# ---------------------------------------------------------------------------------------------------------------
# rule model: atom = ("any", A) | ("without", A, B) | ("count", q, cmp, T, A|None)
# rule = {"tpl", "op": None|"all"|"any", "atoms": [...], "exc": atom|None, "guard": atom|None}


def atom_text(a) -> str:
    if a[0] == "any":
        return f"any {a[1]} file changes"
    if a[0] == "without":
        return f"any {a[1]} file changes without any {a[2]} file changing"
    _, q, cmp, t, c = a
    if q == "lines":
        return f"the number of changed lines is {cmp} {t}"
    if q == "files":
        return f"the number of changed files is {cmp} {t}"
    if q == "clines":
        return f"the number of changed lines in {c} files is {cmp} {t}"
    return f"the number of changed {c} files is {cmp} {t}"


def rule_lines(rule: dict) -> list[str]:
    if rule["op"] is None:
        out = [f"Hold rule: the rule holds a change if {atom_text(rule['atoms'][0])}."]
    else:
        items = "; ".join(f"[{i + 1}] {atom_text(a)}" for i, a in enumerate(rule["atoms"]))
        out = [f"Hold rule: the rule holds a change if {rule['op']} of these are true: {items}."]
    if rule.get("exc"):
        out.append(f"Exception: this rule does not hold the change if {atom_text(rule['exc'])}.")
    if rule.get("guard"):
        out.append(f"This rule applies only if {atom_text(rule['guard'])}.")
    return out


def atoms_of(rule: dict) -> list:
    return list(rule["atoms"]) + [x for x in (rule.get("exc"), rule.get("guard")) if x]


def classes_of(rule: dict) -> list[str]:
    out = []
    for a in atoms_of(rule):
        cs = [a[1]] if a[0] == "any" else [a[1], a[2]] if a[0] == "without" else ([a[4]] if a[4] else [])
        for c in cs:
            if c not in out:
                out.append(c)
    return out


def has_count(rule: dict) -> bool:
    return any(a[0] == "count" for a in atoms_of(rule))


def slice_ok(rule: dict) -> bool:
    return not has_count(rule)


def clauses(rule: dict, view: str, inverted: bool = False) -> list[str]:
    ids = ["SEM-08", "SEM-09", "SEM-30", "SEM-32", "SEM-33", "SEM-34", "SEM-41"]
    if view == "message_only":
        ids = ["SEM-04", "SEM-46"] + ids + ["SEM-31m", "SEM-48"]
    else:
        # SEM-05 / SEM-07 left out: their rivals (renames, binary and mode-only files) cannot occur, because the builder
        # keeps no such file on any row (plain_files); both are boundary clauses, inactive on every row (1.5)
        ids = ["SEM-01", "SEM-02", "SEM-22", "SEM-23", "SEM-36", "SEM-37"] + ids + ["SEM-31d"]
    kinds = {a[0] for a in atoms_of(rule)}
    if "count" in kinds:
        ids += ["SEM-06", "SEM-10"]
    if "any" in kinds:
        ids.append("SEM-35")
    if "without" in kinds:
        ids.append("SEM-14")
    if rule["op"]:
        ids += ["SEM-12", "SEM-13", "SEM-39"]
    if rule.get("exc"):
        ids.append("SEM-15")
    if rule.get("guard"):
        ids.append("SEM-16")
    if inverted:
        ids.append("SEM-44")
    else:
        ids.append("SEM-38")
    return [i for i in dict.fromkeys(ids) if i != "SEM-48"] + (["SEM-48"] if "SEM-48" in ids else [])


# ---------------------------------------------------------------------------------------------------------------
# solver A (Python over the record)

def file_classes_A(rec: dict, names) -> list[set]:
    return [{c for c in names if K.file_in_A(f, CLS[c])} for f in rec["files"]]


def eval_atom_A(a, rec, fc) -> bool:
    if a[0] == "any":
        return any(a[1] in s for s in fc)
    if a[0] == "without":
        return any(a[1] in s for s in fc) and not any(a[2] in s for s in fc)
    _, q, cmp, t, c = a
    if q == "lines":
        v = rec["added"] + rec["removed"]
    elif q == "files":
        v = len(rec["files"])
    elif q == "clines":
        v = sum(f["added"] + f["removed"] for f, s in zip(rec["files"], fc) if c in s)
    else:
        v = sum(1 for s in fc if c in s)
    return v > t if cmp == "more than" else v >= t


def qvalue_A(a, rec, fc) -> int:
    _, q, cmp, t, c = a
    if q == "lines":
        return rec["added"] + rec["removed"]
    if q == "files":
        return len(rec["files"])
    if q == "clines":
        return sum(f["added"] + f["removed"] for f, s in zip(rec["files"], fc) if c in s)
    return sum(1 for s in fc if c in s)


def holds_A(rule: dict, rec: dict, cls_override: dict | None = None) -> bool:
    global CLS
    saved = CLS
    if cls_override:
        CLS = {**CLS, **cls_override}
    try:
        fc = file_classes_A(rec, classes_of(rule))
        vals = [eval_atom_A(a, rec, fc) for a in rule["atoms"]]
        cond = vals[0] if rule["op"] is None else (all(vals) if rule["op"] == "all" else any(vals))
        if rule.get("guard") and not eval_atom_A(rule["guard"], rec, fc):
            return False
        if rule.get("exc") and eval_atom_A(rule["exc"], rec, fc):
            return False
        return cond
    finally:
        CLS = saved


def shown_gold(hold: bool, frame: str, k: int) -> int:
    v = hold if frame == "hold" else (not hold)
    return int(v) ^ (k % 2)


# ---------------------------------------------------------------------------------------------------------------
# parser + solver B (reads only the rendered row text; message-only rows: the parsed rule + the record, 5.7)

B_ATOMS = [
    ("without", re.compile(r"^any (.+?) file changes without any (.+?) file changing$")),
    ("any", re.compile(r"^any (.+?) file changes$")),
    ("lines", re.compile(r"^the number of changed lines is (more than|at least) (\d+)$")),
    ("files", re.compile(r"^the number of changed files is (more than|at least) (\d+)$")),
    ("clines", re.compile(r"^the number of changed lines in (.+?) files is (more than|at least) (\d+)$")),
    ("cfiles", re.compile(r"^the number of changed (.+?) files is (more than|at least) (\d+)$")),
]
B_JOIN_BAD = re.compile(r"\b(and|or)\b")


class ParseError(Exception):
    pass


def B_atom(s: str):
    s = s.strip()
    for kind, rx in B_ATOMS:
        m = rx.match(s)
        if m:
            g = m.groups()
            if kind == "without":
                return ("without", g[0], g[1])
            if kind == "any":
                return ("any", g[0])
            if kind in ("lines", "files"):
                return ("count", kind, g[0], int(g[1]), None)
            return ("count", kind, g[1], int(g[2]), g[0])
    raise ParseError("atom: " + s)


def B_parse_rule(text: str) -> dict:
    lines = [ln.strip() for ln in text.split("\n")]
    rule = {"op": None, "atoms": None, "exc": None, "guard": None}
    classes = {}
    for ln in lines:
        m = re.search(r"(?<!['\w])Hold rule: the rule holds a change if (all|any) of these are true: (.+)\.$", ln)
        if m:
            items = re.split(r";? ?\[\d+\] ", " " + m.group(2))
            rule["op"] = m.group(1)
            rule["atoms"] = [B_atom(x.rstrip(";")) for x in items if x.strip()]
            continue
        m = re.search(r"(?<!['\w])Hold rule: the rule holds a change if (.+)\.$", ln)
        if m:
            body = m.group(1)
            a = B_atom(body)
            rule["atoms"] = [a]
            continue
        m = re.search(r"(?<!['\w])Exception: this rule does not hold the change if (.+)\.$", ln)
        if m:
            rule["exc"] = B_atom(m.group(1))
            continue
        m = re.search(r"(?<!['\w])This rule applies only if (.+)\.$", ln)
        if m:
            rule["guard"] = B_atom(m.group(1))
            continue
        m = re.search(r"(?:^|\W)([A-Za-z][A-Za-z ]*?) files: (.+)\.$", ln)
        if m and "Hold rule" not in ln:
            name, body = m.group(1).strip(), m.group(2)
            folders, pats = [], []
            for part in body.split("; or "):
                mm = re.match(r"any file in a folder named (.+)$", part)
                if mm:
                    folders = _B_split_or(mm.group(1))
                mm = re.match(r"any file whose file name matches (.+)$", part)
                if mm:
                    pats = _B_split_or(mm.group(1))
            classes[name] = {"folders": folders, "patterns": pats}
    if not rule["atoms"]:
        raise ParseError("no rule")
    # join-rule and shape checks (R4-01, R5-07)
    if rule["op"] is None and (rule["exc"] or rule["guard"]):
        raise ParseError("single-atom rule with exception or guard")
    for a in rule["atoms"] + [x for x in (rule["exc"], rule["guard"]) if x]:
        for c in ([a[1]] if a[0] == "any" else [a[1], a[2]] if a[0] == "without" else [a[4]] if a[4] else []):
            if B_JOIN_BAD.search(c):
                raise ParseError("class name with and/or")
            if c not in classes:
                raise ParseError("class list missing: " + c)
            bad = K.lint_class(classes[c])
            if bad:
                raise ParseError("class lint: " + ",".join(bad))
    return {"rule": rule, "classes": classes}


def _B_split_or(s: str) -> list[str]:
    if " or " in s:
        head, last = s.rsplit(" or ", 1)
        return [x.strip() for x in head.split(", ")] + [last.strip()]
    return [s.strip()]


def B_eval(parsed: dict, files: list[tuple]) -> bool:
    """files: [(path, added, removed)] ; atoms compiled to sqlite EXISTS / COUNT queries."""
    rule, classes = parsed["rule"], parsed["classes"]
    db = K.ClassDB(classes)
    fcls = db.classes_of([p for p, _, _ in files])
    con = sqlite3.connect(":memory:")
    con.execute("create table f(fid int, added int, removed int)")
    con.execute("create table fc(fid int, cls text)")
    for i, (p, a, r) in enumerate(files):
        con.execute("insert into f values (?,?,?)", (i, a, r))
        for c in fcls[i]:
            con.execute("insert into fc values (?,?)", (i, c))

    def ex(c):
        return con.execute("select exists(select 1 from fc where cls = ?)", (c,)).fetchone()[0] == 1

    def atom(a):
        if a[0] == "any":
            return ex(a[1])
        if a[0] == "without":
            return ex(a[1]) and not ex(a[2])
        _, q, cmp, t, c = a
        if q == "lines":
            v = con.execute("select coalesce(sum(added + removed), 0) from f").fetchone()[0]
        elif q == "files":
            v = con.execute("select count(*) from f").fetchone()[0]
        elif q == "clines":
            v = con.execute("select coalesce(sum(added + removed), 0) from f where fid in "
                            "(select fid from fc where cls = ?)", (c,)).fetchone()[0]
        else:
            v = con.execute("select count(distinct fid) from fc where cls = ?", (c,)).fetchone()[0]
        return v > t if cmp == "more than" else v >= t

    if rule["guard"] and not atom(rule["guard"]):
        return False
    if rule["exc"] and atom(rule["exc"]):
        return False
    vals = [atom(a) for a in rule["atoms"]]
    return vals[0] if rule["op"] is None else (all(vals) if rule["op"] == "all" else any(vals))


QFRAME = re.compile(r"([^\n?]*\b(?:hold|holds|held|merge without review)\b[^\n?]*\?)")


def B_question(instr: str) -> tuple[str, int]:
    qs = QFRAME.findall(instr)
    if not qs:
        raise ParseError("no question")
    q = qs[-1].strip()
    if re.search(r"(?i)\b(is it not true|isn't it|is it not the case|is it false that)\b", q):
        raise ParseError("negated frame")
    frame = "pass" if "merge without review" in q else "hold"
    return frame, negcount.k_syn(q)


def B_files_from_state(state: str, need_stats: bool):
    st = K.parse_state(state)
    if not st["diffs"]:
        raise ParseError("no diff")
    files = st["diffs"][0][1]["files"]
    if need_stats:
        if st["stats"] is None:
            raise ParseError("stats missing")
        tot = st["total"]
        if tot is None or tot[0] != len(st["stats"]) or tot[1] != sum(a + r for a, r, _ in st["stats"]):
            raise ParseError("total mismatch")
        if sorted(p for _, _, p in st["stats"]) != sorted(f["path"] for f in files):
            raise ParseError("stats and headers differ")
        return [(p, a, r) for a, r, p in st["stats"]], files
    return [(f["path"], 0, 0) for f in files], files


def B_solve(row: dict, rec: dict | None = None) -> int:
    """Shown gold of a gate yes/no row from its rendered text (message-only rows: parsed rule + record)."""
    parsed = B_parse_rule(row["card"])
    frame, k = B_question(row["instructions"])
    rule = parsed["rule"]
    need = any(a[0] == "count" for a in rule["atoms"] + [x for x in (rule["exc"], rule["guard"]) if x])
    if row["meta"]["input_view"] == "message_only":
        files = [(f["path"], f["added"], f["removed"]) for f in rec["files"]]
    else:
        files, _ = B_files_from_state(row["state"], need)
    hold = B_eval(parsed, files)
    v = hold if frame == "hold" else (not hold)
    return int(v) ^ (k % 2)


def B_solve_inverted(row: dict) -> str:
    parsed = B_parse_rule(row["instructions"])
    st = K.parse_state(row["state"])
    held = []
    for ref in row["options"]:
        body = _B_case_diff(row["state"], ref)
        files = K.parse_diff_text(body)["files"]
        if B_eval(parsed, [(f["path"], 0, 0) for f in files]):
            held.append(ref)
    if len(held) != 1:
        raise ParseError(f"inverted: {len(held)} held cases")
    return held[0]


def _B_case_diff(state: str, ref: str) -> str:
    m = re.search(re.escape(ref) + r" diff:\n```diff\n(.*?)\n```", state, re.S)
    if not m:
        raise ParseError("case diff missing: " + ref)
    return m.group(1)


# ---------------------------------------------------------------------------------------------------------------
# rules (step 6; fixed seed)

def _cls_pool():
    return sorted(CLS)


def make_rules(n_by_tpl: dict, seed: str = "gate-rules-v1") -> list[dict]:
    rng = FR.rng(seed)
    names = _cls_pool()
    common_cls = ["test", "documentation", "CI", "build script", "manifest", "config", "migration", "script",
                  "lockfile", "container", "template", "stylesheet", "example", "security"]
    out, seen = [], set()

    def cnt_atom():
        q = rng.choice(["lines", "files", "clines", "cfiles"])
        cmp = rng.choice(CMPS)
        if q == "lines":
            return ("count", q, cmp, rng.choice(T_LINES), None)
        if q == "files":
            return ("count", q, cmp, rng.choice(T_FILES), None)
        c = rng.choice(common_cls[:8])
        return ("count", q, cmp, rng.choice(T_CLINES if q == "clines" else T_CFILES), c)

    def atom(kinds):
        k = rng.choice(kinds)
        if k == "any":
            return ("any", rng.choice(common_cls))
        if k == "without":
            a, b = rng.sample(common_cls, 2)
            return ("without", a, b)
        return cnt_atom()

    for tpl, n in n_by_tpl.items():
        made = 0
        tries = 0
        while made < n and tries < 5000:
            tries += 1
            if tpl == "GT1":
                r = {"tpl": tpl, "op": None, "atoms": [atom(["any"])], "exc": None, "guard": None}
            elif tpl == "GT2":
                r = {"tpl": tpl, "op": None, "atoms": [atom(["without"])], "exc": None, "guard": None}
            elif tpl == "GT3":
                r = {"tpl": tpl, "op": None, "atoms": [cnt_atom()], "exc": None, "guard": None}
            else:
                na = rng.choice([2, 2, 3])
                kinds = ["any", "without", "count"] if made % 3 else ["any", "without"]
                r = {"tpl": tpl, "op": rng.choice(["all", "any"]), "atoms": [atom(kinds) for _ in range(na)],
                     "exc": atom(["any", "without"] if made % 3 == 0 else ["any", "without", "count"])
                     if rng.random() < 0.5 else None,
                     "guard": atom(["any", "count"] if made % 3 else ["any"]) if rng.random() < 0.3 else None}
            cs = classes_of(r)
            if len(set(map(str, atoms_of(r)))) != len(atoms_of(r)):
                continue
            if r["op"] == "all" and len(cs) < len(r["atoms"]) and any(a[0] == "without" for a in r["atoms"]):
                pass
            key = json.dumps(r, sort_keys=True)
            if key in seen:
                continue
            # a rule must be satisfiable both ways on plausible commits: no 'without' of a class with itself
            if any(a[0] == "without" and a[1] == a[2] for a in atoms_of(r)):
                continue
            seen.add(key)
            r["rule_id"] = f"GR{len(out) + 1:03d}"
            out.append(r)
            made += 1
    return out


def alias_lint(rule: dict) -> bool:
    """R4-05: each alias word is one part and one M token; entity alias lists disjoint; no alias word of one entity
    equal to / near miss of a part of another entity's alias words, class name or folder names."""
    ents = classes_of(rule)
    for e in ents:
        for w in CLS[e]["aliases"]:
            ps = C.parts(w)
            if len(ps) != 1 or C.m_tokens(w) != ps:
                return False
    for e in ents:
        mine = {p for w in CLS[e]["aliases"] for p in C.parts(w)}
        for o in ents:
            if o == e:
                continue
            theirs = {p for w in CLS[o]["aliases"] + [o] + CLS[o]["folders"] for p in C.parts(w)}
            for a in mine:
                if any(a == b or C.near_miss(a, b) for b in theirs):
                    return False
    return True


# ---------------------------------------------------------------------------------------------------------------
# message-only filters (1.4, 5.5) -- one symmetric program, record-based, gold-blind

def mo_check(rule: dict, rec: dict):
    """Returns (ok, reason, trigger_entities)."""
    ents = classes_of(rule)
    fc = file_classes_A(rec, ents)
    alias_tok = {e: {p for w in CLS[e]["aliases"] for p in C.m_tokens(w)} for e in ents}
    full = {}
    for e in ents:
        s = set(alias_tok[e])
        for f, cs in zip(rec["files"], fc):
            if e in cs:
                s.update(C.m_tokens(f["path"]))
                s.update(t for x in C.identifiers([t for h in f["hunks"] for k, t in h["lines"] if k in "+-"])
                         for t in C.m_tokens(x))
        full[e] = s
    shared = collections.Counter(t for s in full.values() for t in s)
    full = {e: {t for t in s if shared[t] == 1} for e, s in full.items()}
    alias_tok = {e: alias_tok[e] & full[e] for e in ents}
    if any(not alias_tok[e] for e in ents):
        return False, "alias_emptied", None
    msg = rec["msg"]
    hits = K.m_hits(msg, full)
    for e in ents:
        if not any(t in alias_tok[e] for t, _ in hits.get(e, [])):
            return False, "no_alias_hit", None
    printed = {e: CLS[e]["aliases"] + [e] + CLS[e]["folders"] for e in ents}
    if K.reader_conflict(msg, printed, {e: [(t, p) for t, p in hits.get(e, [])] for e in ents}):
        return False, "reader_agreement", None
    # file-name words (R5-04)
    import fnmatch
    for w, s in K.msg_words(msg):
        segs = [w] + w.split("/")
        for e in ents:
            for sg in segs:
                low = sg.lower()
                if any(fnmatch.fnmatchcase(low, p.lower()) for p in CLS[e]["patterns"]) or \
                        low in {f.lower() for f in CLS[e]["folders"]}:
                    ok = any(s <= p < s + len(w) and t in alias_tok[e] for t, p in hits.get(e, []))
                    if not ok:
                        return False, "file_name_word", None
    cls = K.mention_classes(msg, {e: [p for _, p in hits[e]] for e in ents})
    if cls is None:
        return False, "mixed_mention", None
    truth = {e: any(e in s for s in fc) for e in ents}
    if any((cls[e] == "changed") != truth[e] for e in ents):
        return False, "mention_vs_record", None
    # re-solve from said-changed classes (R2-03): must equal the record's gold
    def atom_cls(a):
        if a[0] == "any":
            return cls[a[1]] == "changed"
        return cls[a[1]] == "changed" and cls[a[2]] != "changed"
    vals = [atom_cls(a) for a in rule["atoms"]]
    cond = vals[0] if rule["op"] is None else (all(vals) if rule["op"] == "all" else any(vals))
    if rule.get("guard") and not atom_cls(rule["guard"]):
        cond = False
    if rule.get("exc") and atom_cls(rule["exc"]):
        cond = False
    if cond != holds_A(rule, rec):
        raise FR.FrameError("message-only re-solve differs from the record gold (generator bug)")
    trig = [{"entity": e, "token": t, "position": p, "alias": t in alias_tok[e]} for e in ents
            for t, p in hits.get(e, [])]
    return True, None, trig


# ---------------------------------------------------------------------------------------------------------------
# card text

def card_ir(rule: dict, view: str, cls_override: dict | None = None, fewshot: list | None = None,
            inverted: bool = False) -> dict:
    cl = {**CLS, **(cls_override or {})}
    blocks = [{"type": "para", "text": x} for x in rule_lines(rule)]
    for c in classes_of(rule):
        blocks.append({"type": "para", "text": T.class_line(c, cl[c])})
    ids = clauses(rule, view, inverted)
    blocks.append({"type": "section", "heading": "How to read the rule",
                   "blocks": [{"type": "items", "items": [T.SEM[i] for i in ids if i != "SEM-48"]}]})
    if view == "message_only":
        blocks.append({"type": "section", "heading": "Words the message uses for each class",
                       "blocks": [{"type": "para", "text": T.SEM["SEM-48"]},
                                  {"type": "items", "items": [T.alias_line(c, cl[c]) for c in classes_of(rule)]}]})
    if inverted:
        blocks.insert(0, {"type": "para", "text": T.INV_FRAME_GATE})
    if fewshot:
        blocks.append({"type": "fewshot", "template": fewshot[0], "heading": None, "examples": fewshot[1]})
    return {"title": "Review rule", "blocks": blocks}


def decisive_lines(rec: dict, rule: dict) -> set:
    fc = file_classes_A(rec, classes_of(rule))
    out = set()
    for fi, (f, cs) in enumerate(zip(rec["files"], fc)):
        if cs:
            for hi, h in enumerate(f["hunks"]):
                for li in range(len(h["lines"])):
                    out.add((fi, hi, li))
    return out


DECISIVE_MAX = 2400   # chars of never-cut lines a row may carry (else the 1,999-token row cap cannot hold)


def decisive_chars(rec: dict, rule: dict) -> int:
    fc = file_classes_A(rec, classes_of(rule))
    return sum(len(t) + 2 for f, cs in zip(rec["files"], fc) if cs for h in f["hunks"] for _, t in h["lines"])


def diff_extra(rec: dict, rule: dict, budget: int):
    shown = K.shorten(rec, budget, decisive_lines(rec, rule))
    if shown is None:
        return None
    parts = []
    if has_count(rule):
        parts.append(K.fence(K.numstat_block(rec), "stats"))
    parts.append(K.fence(K.render_shown(shown), "diff"))
    return "\n\n".join(parts), {}


# ---------------------------------------------------------------------------------------------------------------
# cards and rows

import yn  # noqa: E402

N_BY_TPL = {"GT1": 12, "GT2": 18, "GT3": 8, "GT5": 22}
SAMPLERS = {"GT1": ["S1", "S2", "S4"], "GT2": ["S1", "S2", "S3", "S4"], "GT3": ["S1", "S2", "S3"],
            "GT5": ["S6", "S1", "S2", "S4", "S6", "S3"]}
CC, PF = "CommitChronicle", "CommitPackFT"


def build_cards(split_kind: str = "train") -> list[dict]:
    """60 yes/no rule cards + 4 inverted cards (train); S5 dev cards reuse 8 slice rules on held-out groups."""
    rules = make_rules(N_BY_TPL)
    cards = []
    rates = {}
    by_tpl = collections.defaultdict(list)
    for i, r in enumerate(rules):
        cid = f"CMG{i + 1:03d}"
        by_tpl[r["tpl"]].append(cid)
    for tpl, ids in by_tpl.items():
        rates.update(FR.antithetic_rates(ids, 28, "gate-" + tpl))
    for i, r in enumerate(rules):
        cid = f"CMG{i + 1:03d}"
        smp = SAMPLERS[r["tpl"]][i % len(SAMPLERS[r["tpl"]])]
        if smp == "S3" and not (r["tpl"] in ("GT2", "GT3") or any(a[0] in ("without", "count") for a in r["atoms"])):
            smp = "S1"
        ds = CC if C.h01("gate-ds", cid) < 7 / 12 else PF
        cards.append({"card_id": cid, "type": "gate", "sampler": smp, "ds": ds, "rule": r, "rule_id": r["rule_id"],
                      "r": rates[cid], "slice": slice_ok(r) and alias_lint(r), "inverted": False,
                      "defs_style": "one_line", "fewshot": i % 15 == 7})
    inv_src = [c for c in cards if c["rule"]["tpl"] in ("GT1", "GT2") or
               (c["rule"]["tpl"] == "GT5" and not has_count(c["rule"]))]
    for j in range(4):
        src = inv_src[(j * 5) % len(inv_src)]
        cid = f"CMGI{j + 1:02d}"
        cards.append({"card_id": cid, "type": "gate", "sampler": ["S1", "S2", "S4", "S6"][j], "rule": src["rule"],
                      "rule_id": src["rule_id"], "r": None, "slice": False, "inverted": True,
                      "ds": CC if j % 3 else PF, "defs_style": "one_line", "fewshot": False})
    return cards


def dev_cards() -> list[dict]:
    rules = make_rules(N_BY_TPL)
    pick = [r for r in rules if r["tpl"] in ("GT1", "GT2", "GT5") and not has_count(r)][:6] + \
        [r for r in rules if r["tpl"] == "GT3"][:2]
    rates = FR.antithetic_rates([f"CMGD{i + 1:02d}" for i in range(len(pick))], 10, "gate-dev")
    return [{"card_id": f"CMGD{i + 1:02d}", "type": "gate", "sampler": "S5", "ds": CC, "rule": r,
             "rule_id": r["rule_id"], "r": rates[f"CMGD{i + 1:02d}"], "slice": slice_ok(r) and alias_lint(r),
             "inverted": False, "defs_style": "one_line", "fewshot": False} for i, r in enumerate(pick)]


def _eligible(rid: str) -> bool:
    x = FR.index()[rid]
    return x["n_files"] <= 20 and not x["bot"]


_GC = {}


def _cands(card: dict, split: str, gsplit: str, cap: int = 2500):
    k = ("c", card["card_id"], split, gsplit, cap)
    if k not in _GC:
        _GC[k] = _cands0(card, split, gsplit, cap)
    else:
        card["pack_id"] = _GC[("pk", card["card_id"], gsplit)]
    return list(_GC[k])


def _cands0(card: dict, split: str, gsplit: str, cap: int = 2500):
    pk, gs = FR.pack(card["card_id"], gsplit, card["ds"], frac=0.4 if gsplit == "train" else 1.0)
    card["pack_id"] = pk
    _GC[("pk", card["card_id"], gsplit)] = pk
    ix = FR.index()
    gset = set(gs)
    rids = sorted((rid for rid, x in ix.items() if x["group"] in gset and x["split"] == gsplit and _eligible(rid)),
                  key=lambda rid: C.h01("gcand", card["card_id"], split, rid))
    out = []
    for rid in rids:
        r = FR.rec(rid)
        if not K.plain_files(r) or decisive_chars(r, card["rule"]) > DECISIVE_MAX:
            continue
        out.append(rid)
        if len(out) >= cap:
            break
    return out


def mo_cands(card: dict, gsplit: str) -> list[str]:
    k = ("mo", card["card_id"], gsplit)
    if k not in _GC:
        _GC[k] = mo_cands0(card, gsplit)
    return list(_GC[k])


def mo_cands0(card: dict, gsplit: str) -> list[str]:
    """Message-only candidates over the whole pack: cheap prefilter (every rule entity has an alias token in the
    message's M tokens), then plain files."""
    _, gs = FR.pack(card["card_id"], gsplit, card["ds"], frac=0.4 if gsplit == "train" else 1.0)
    gset = set(gs)
    need = [{p for w in CLS[e]["aliases"] for p in C.m_tokens(w)} for e in classes_of(card["rule"])]
    out = []
    for rid, x in FR.index().items():
        if x["group"] in gset and x["split"] == gsplit and _eligible(rid) and all(x["mtok"] & n for n in need):
            if K.plain_files(FR.rec(rid)):
                out.append(rid)
    return sorted(out)  # message-only rows show no diff: no decisive-size filter


_SKEY = {}


def _skey_cached(card: dict, rid: str):
    k = (card["card_id"], rid)
    if k not in _SKEY:
        _SKEY[k] = _sampler_key(card, FR.rec(rid))
    return _SKEY[k]


def _sampler_key(card: dict, rec: dict):
    s = card["sampler"]
    rule = card["rule"]
    if s == "S3":
        cnt = [a for a in rule["atoms"] if a[0] == "count"]
        if cnt:
            fc = file_classes_A(rec, classes_of(rule))
            return min(abs(qvalue_A(a, rec, fc) - a[3]) for a in cnt)
        wo = [a for a in rule["atoms"] if a[0] == "without"]
        if wo:
            fc = file_classes_A(rec, classes_of(rule))
            return 0 if any(wo[0][2] in x for x in fc) else 1
    if s == "S4":
        al = {p for c in classes_of(rule) for w in CLS[c]["aliases"] for p in C.m_tokens(w)}
        return 0 if set(C.m_tokens(rec["msg"])) & al else 1
    return 0


def build_rows(card: dict, em: FR.Emitter, reg: FR.Registry, split: str, n_rows: int, mo_share: float,
               twin_rate: float = 0.18):
    gsplit = "heldout" if split == "dev" else "train"
    rule = card["rule"]
    cands = _cands(card, split, gsplit)
    card["_mo_cands"] = mo_cands(card, gsplit) if card["slice"] else []
    hold_of = {}
    for rid in cands:
        kk = ("hold", card["card_id"], rid)
        if kk not in _GC:
            _GC[kk] = holds_A(rule, FR.rec(rid))
        hold_of[rid] = _GC[kk]
    if card["inverted"]:
        return _build_inverted(card, em, reg, split, n_rows, cands, hold_of)
    n_mo = round(mo_share * n_rows) if card["slice"] else 0
    n_diff = n_rows - n_mo
    kinds = []
    budget_tw = int(twin_rate * n_rows) if split != "dev" else 0
    tw_order = []
    if rule["tpl"] == "GT3":
        tw_order = ["contrast:threshold", "contrast:threshold", "negset", "contrast:threshold", "attack"]
    elif rule["tpl"] in ("GT1", "GT2"):
        tw_order = ["contrast:classedit", "negset", "contrast:classedit", "attack", "contrast:classedit"]
    else:
        tw_order = ["negset", "attack", "negset", "contrast:classedit"]
    used = 0
    for kd in tw_order * 3:
        add = yn.ROWS[kd.split(":")[0]] - 1
        if used + add > budget_tw:
            break
        kinds.append(kd)
        used += add
    n_single = max(0, n_diff - sum(yn.ROWS[k.split(":")[0]] for k in kinds))
    kinds += ["single"] * n_single
    units = yn.plan(card["card_id"], split, n_mo, [k.split(":")[0] for k in kinds], card["r"], "hold", "pass")
    sub = {}
    di = 0
    for u in units:
        if u["view"] == "message_diff":
            u["sub"] = kinds[di].split(":")[1] if ":" in kinds[di] else None
            di += 1
    wd_yn = FR.card_wordings("gate", "yn", card["card_id"])
    mo_pool = None
    stats = collections.Counter()
    pos = card.get('_pos_' + split, 0)
    for u in units:
        h = yn.truth_for(u["s"], u["frame"], u["k"], "hold")
        if u["view"] == "message_only" and mo_pool is None:
            mo_pool = {}
            need = [{p for w in CLS[e]["aliases"] for p in C.m_tokens(w)} for e in classes_of(rule)]
            for rid in sorted(card["_mo_cands"], key=lambda x: C.h01("mo", card["card_id"], x)):
                if rid not in hold_of:
                    hold_of[rid] = holds_A(rule, FR.rec(rid))
                ok, why, trig = mo_check(rule, FR.rec(rid))
                stats["mo_" + (why or "ok")] += 1
                if ok:
                    mo_pool[rid] = trig
        pool_ = [rid for rid in (mo_pool if u["view"] == "message_only" else cands)
                 if hold_of[rid] == h and reg.can_base(rid, "gate", split)]
        if u.get("sub") == "threshold":
            pool_ = [rid for rid in pool_ if _threshold_variant(rule, FR.rec(rid)) is not None]
        if u.get("sub") == "classedit":
            pool_ = [rid for rid in pool_ if _classedit_variant(rule, FR.rec(rid)) is not None]
        if not pool_:
            stats["unit_unfilled_" + u["view"]] += 1
            continue
        pool_.sort(key=lambda rid: (_skey_cached(card, rid), C.h01("pick", card["card_id"], split, rid)))
        rid = pool_[0]
        reg.take_base(rid, "gate", split)
        pos += 1
        _emit_unit(card, em, split, u, FR.rec(rid), wd_yn, pos, (mo_pool or {}).get(rid))
        stats["units"] += 1
    card['_pos_' + split] = pos
    return stats


def _threshold_variant(rule: dict, rec: dict):
    if rule["tpl"] != "GT3":
        return None
    a = rule["atoms"][0]
    fc = file_classes_A(rec, classes_of(rule))
    v = qvalue_A(a, rec, fc)
    h = eval_atom_A(a, rec, fc)
    if a[2] == "more than":
        t2 = v if h else v - 1
    else:
        t2 = v + 1 if h else v
    if t2 < 1 or t2 == a[3]:
        return None
    r2 = {**rule, "atoms": [(a[0], a[1], a[2], t2, a[4])]}
    return r2 if holds_A(r2, rec) != holds_A(rule, rec) else None


def _classedit_variant(rule: dict, rec: dict):
    """One folder name or file pattern added to / removed from one class used by a GT1/GT2 atom so gold flips."""
    cl = [a[1] for a in rule["atoms"] if a[0] in ("any", "without")]
    if not cl:
        return None
    base = holds_A(rule, rec)
    c = cl[0]
    cls = CLS[c]
    for kind in ("folders", "patterns"):
        for e in cls[kind]:
            new = {**cls, kind: [x for x in cls[kind] if x != e]}
            if new["folders"] or new["patterns"]:
                if holds_A(rule, rec, {c: new}) != base:
                    return {c: new}
    for f in rec["files"]:
        for seg in f["path"].split("/")[:-1]:
            if re.fullmatch(r"[A-Za-z0-9._-]+", seg) and seg not in (".", "..") and seg.lower() not in \
                    {x.lower() for x in cls["folders"]}:
                new = {**cls, "folders": cls["folders"] + [seg]}
                if holds_A(rule, rec, {c: new}) != base:
                    return {c: new}
    return None


def _wording(wds, card_id, rid, salt=""):
    return wds[int(C.h01("wd", card_id, rid, salt) * len(wds))]


def _qpick(frame: str, k: int, card_id: str, rid: str):
    qs = T.questions("gate_hold" if frame == "hold" else "gate_pass", k)
    return qs[int(C.h01("q", card_id, rid, k) * len(qs))]


def _emit_unit(card, em, split, u, rec, wds, pos, trig):
    rule = card["rule"]
    base_id = f"COMMIT-{split}-{card['card_id']}-{pos:03d}"
    view = u["view"]
    cir = card_ir(rule, view)

    def mk(rid_suffix, k, rule_v, cir_v, msg, twin_of=None, twin_kind=None, call=None, variant=None, edge=()):
        qid, qtext, kk = _qpick(u["frame"], k, card["card_id"], rec["rid"] + rid_suffix)
        hold = holds_A(rule_v["rule"] if "rule" in rule_v else rule, rec, rule_v.get("cls"))
        gold = yn.shown(hold, u["frame"], kk, "hold")
        r2 = rule_v.get("rule", rule)
        sp = {"id": base_id + rid_suffix, "type": "gate", "card": card, "rec": rec, "view": view,
              "form": "yesno", "qtype": "noul", "question": qtext, "qid": qid, "k": kk,
              "wording": _wording(wds, card["card_id"], rec["rid"]), "card_ir": cir_v, "gold": gold, "msg": msg,
              "build_extra": (lambda b: diff_extra(rec, r2, b)) if view == "message_diff" else None,
              "depth": len(atoms_of(rule)), "twin_of": twin_of, "twin_kind": twin_kind,
              "call_id": call or (base_id + rid_suffix + "-u"), "trigger_entities": trig or [],
              "polarity": "bad_yes" if u["frame"] == "hold" else "good_yes", "variant": variant,
              "edge": [f"tpl:{rule['tpl']}", f"frame:{u['frame']}", f"k:{kk}", *edge], "card_form": "normal",
              "sidecar": {"frame": u["frame"], "hold": hold}}
        return em.emit(sp)

    kind, sub = u["kind"], u.get("sub")
    if kind == "single":
        mk("-b", u["k"], {}, cir, rec["msg"])
    elif kind == "negset":
        call = base_id + "-u"
        a = mk("-b", 0, {}, cir, rec["msg"], call=call)
        if a:
            n1 = mk("-n1", 1, {}, cir, rec["msg"], twin_of=a["id"], twin_kind="negated", call=call)
            n2 = mk("-n2", 2, {}, cir, rec["msg"], twin_of=a["id"], twin_kind="double_negated", call=call)
            if n1:
                em.relate(a["id"], n1["id"], "complement")
            if n2:
                em.relate(a["id"], n2["id"], "equiv")
    elif kind == "attack":
        call = base_id + "-u"
        a = mk("-b", 0, {}, cir, rec["msg"], call=call)
        if a:
            line = L.ATTACK_LINES[int(C.h01("atk", rec["rid"]) * len(L.ATTACK_LINES))]
            t = mk("-a1", 0, {}, cir, rec["msg"] + "\n" + line, twin_of=a["id"], twin_kind="attack", call=call,
                   edge=("attack",))
            if t:
                em.relate(a["id"], t["id"], "inv")
    elif kind == "contrast":
        a = mk("-b", 0, {}, cir, rec["msg"])
        if a:
            if sub == "threshold":
                r2 = _threshold_variant(rule, rec)
                cir2 = card_ir(r2, view)
                mk("-t1", 0, {"rule": r2}, cir2, rec["msg"], twin_of=a["id"], twin_kind="threshold",
                   variant=f"{card['card_id']}-T{r2['atoms'][0][3]}")
            else:
                ov = _classedit_variant(rule, rec)
                cir2 = card_ir(rule, view, cls_override=ov)
                vid = C.sha256(json.dumps(ov, sort_keys=True))[:8]
                mk("-c1", 0, {"cls": ov}, cir2, rec["msg"], twin_of=a["id"], twin_kind="class_edit",
                   variant=f"{card['card_id']}-CE{vid}")


def _build_inverted(card, em, reg, split, n_rows, cands, hold_of):
    rule = card["rule"]
    stats = collections.Counter()
    yes = [r for r in cands if hold_of[r]]
    no = [r for r in cands if not hold_of[r]]
    wds = FR.card_wordings("gate", "choice", card["card_id"])
    for i in range(n_rows):
        k = 3 + (C.h01("invk", card["card_id"], split, i) < 0.5)
        g = next((r for r in yes if reg.can_extra(r, "gate", split) and reg.can_base(r, "gate", split)), None)
        if g is None:
            stats["inv_no_gold"] += 1
            break
        gr = FR.rec(g)
        ds_ = [r for r in no if r != g and reg.can_extra(r, "gate", split)
               and abs(FR.index()[r]["n_files"] - gr["n_files"]) <= 1][:k - 1]
        if len(ds_) < k - 1:
            stats["inv_no_distractors"] += 1
            yes.remove(g)
            continue
        reg.take_base(g, "gate", split)
        for d in ds_:
            reg.take_extra(d, "gate", split)
        recs = [gr] + [FR.rec(d) for d in ds_]
        refs = __import__("fmt1.card", fromlist=["case_refs"]).case_refs("IVN01", k, f"{card['card_id']}-{split}-{i}")
        order = sorted(range(k), key=lambda j: C.h01("invpos", card["card_id"], split, i, j))
        cases = [(refs[j], recs[order[j]]) for j in range(k)]
        gold_ref = refs[order.index(0)]
        doc = {"title": None, "meta": [], "blocks": [
            {"type": "section", "heading": ref, "blocks": [{"type": "para", "text": ln}
                                                          for ln in r_["msg"].split("\n") if ln.strip()]}
            for ref, r_ in cases]}

        def extra(b, cases=cases):
            parts = []
            for ref, r_ in cases:
                sh = K.shorten(r_, min(300, b // k), decisive_lines(r_, rule))
                if sh is None:
                    return None
                parts.append(f"{ref} diff:\n" + K.fence(K.render_shown(sh), "diff"))
            return "\n\n".join(parts), {}
        qid, qtext, _ = T.questions("gate_inv")[int(C.h01("qi", card["card_id"], i) * 2)]
        sp = {"id": f"COMMIT-{split}-{card['card_id']}-{i + 1:03d}-b", "type": "gate", "card": card, "rec": gr,
              "view": "message_diff", "form": "inverted", "qtype": "choice", "question": qtext, "qid": qid, "k": 0,
              "wording": _wording(wds, card["card_id"], g), "card_ir": card_ir(rule, "message_diff", inverted=True),
              "options": refs, "gold": gold_ref, "msg": gr["msg"], "doc": doc, "build_extra": extra,
              "budgets": [1200, 900, 700, 500], "depth": len(atoms_of(rule)), "call_id":
                  f"COMMIT-{split}-{card['card_id']}-{i + 1:03d}-u", "card_form": "inverted",
              "extra_recs": [dict(FR.rec(d), _use="inverted_case") for d in ds_],
              "edge": [f"tpl:{rule['tpl']}", f"k_cases:{k}"]}
        if em.emit(sp):
            stats["units"] += 1
        yes.remove(g)
    return stats
