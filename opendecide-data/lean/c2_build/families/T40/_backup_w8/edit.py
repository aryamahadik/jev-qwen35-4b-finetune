"""families/T40/edit.py: head C of T40 (a proposed str_replace edit on a small Python file), its generator and its executor.

A file is 2-4 functions from role templates ($F function name, $L list, $S scalar, $A accumulator, $E element, $R
second scalar); identifiers come from a vocabulary pack and are SLOTS (F<k> in the file, O<k> in old_str, N<k> in new_str,
all the same value at the start), so a twin can change one identifier of old_str. Functions share their L / E (and often A)
identifiers, so lines repeat and old_str fragments with 2+ occurrences exist in every file.

Label-first: the sampler draws the target label and a label-blind target length, picks a fragment of the file (count 1
for ONCE / NO_MATCH / BREAKS_SYNTAX bases, count >= 2 for MULTIPLE) closest to that length, then applies the label's
corruption; the REAL run (edit_exec.py in a subprocess: str.count, str.replace, ast.parse; 5 s cap, hermetic env,
temp dir) decides the label. A draw whose run disagrees with the target is redrawn.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABELS_C = ("APPLIES_ONCE", "NO_MATCH", "MULTIPLE", "BREAKS_SYNTAX")
TEMPLATES = (
    "def $F($L, $S):\n    $A = 0\n    for $E in $L:\n        $A = $A + $E * $S\n    return $A",
    "def $F($L):\n    $A = 0\n    for $E in $L:\n        if $E > 0:\n            $A = $A + 1\n    return $A",
    "def $F($L, $S):\n    $A = $S\n    for $E in $L:\n        if $E > $A:\n            $A = $E\n    return $A",
    "def $F($E, $S, $R):\n    if $E < $S:\n        return $S\n    if $E > $R:\n        return $R\n    return $E",
    "def $F($L, $S):\n    $A = [$E * $S for $E in $L]\n    return $A",
    "def $F($L):\n    $A = []\n    for $E in $L:\n        $A.append($E.strip())\n    return \", \".join($A)",
    "def $F($S, $R):\n    $A = $S / $R\n    return round($A, 2)",
)
PACKS = {
    "stock": dict(F=("total_stock", "count_items", "peak_price", "scale_prices", "clamp_level", "join_names", "unit_ratio"),
                  L=("items", "prices", "levels", "batches"), S=("factor", "limit", "rate", "step"),
                  A=("total", "count", "best", "acc"), E=("item", "price", "level", "entry"), R=("ceiling", "cap")),
    "scheduler": dict(F=("sum_slots", "count_jobs", "longest_gap", "scale_delays", "clamp_wait", "join_tasks", "slot_ratio"),
                      L=("jobs", "slots", "delays", "queue"), S=("weight", "floor", "quota", "offset"),
                      A=("busy", "tally", "longest", "out"), E=("job", "slot", "delay", "task"), R=("horizon", "deadline")),
    "billing": dict(F=("sum_charges", "count_paid", "top_charge", "scale_fees", "clamp_tax", "join_clients", "fee_ratio"),
                    L=("charges", "fees", "lines", "invoices"), S=("markup", "minimum", "tax", "discount"),
                    A=("amount", "paid", "highest", "bill"), E=("charge", "fee", "line", "invoice"), R=("maximum", "bound")),
    "reports": dict(F=("sum_rows", "count_pages", "widest_col", "scale_cells", "clamp_width", "join_titles", "page_ratio"),
                    L=("rows", "cells", "pages", "sections"), S=("zoom", "margin", "pad", "gap"),
                    A=("size", "pages", "widest", "text"), E=("row", "cell", "page", "section"), R=("span", "edge")),
    "sensors": dict(F=("sum_readings", "count_alerts", "max_reading", "scale_samples", "clamp_signal", "join_labels", "noise_ratio"),
                    L=("readings", "samples", "signals", "frames"), S=("gain", "bias", "scale", "trim"),
                    A=("energy", "alerts", "peak", "line"), E=("reading", "sample", "signal", "frame"), R=("upper", "lid")),
    "catalog": dict(F=("sum_weights", "count_tags", "heaviest", "scale_sizes", "clamp_rank", "join_authors", "rank_ratio"),
                    L=("books", "tags", "ranks", "shelves"), S=("boost", "base", "span", "shift"),
                    A=("weight", "tags_seen", "heavy", "joined"), E=("book", "tag", "rank", "shelf"), R=("top", "limit_hi")),
    "logs": dict(F=("sum_bytes", "count_errors", "slowest_call", "scale_times", "clamp_depth", "join_hosts", "error_ratio"),
                 L=("events", "times", "depths", "hosts"), S=("window", "skew", "level", "pace"),
                 A=("volume", "errors", "slowest", "names"), E=("event", "stamp", "depth", "host"), R=("deep", "outer")),
    "grades": dict(F=("sum_scores", "count_passes", "best_score", "scale_marks", "clamp_mark", "join_pupils", "pass_ratio"),
                   L=("scores", "marks", "grades", "classes"), S=("curve", "pass_mark", "bonus", "weighting"),
                   A=("points", "passes", "top_mark", "names_out"), E=("score", "mark", "grade", "pupil"), R=("perfect", "ceil_mark")),
    # held out for the sealed split (S5)
    "orbits": dict(F=("sum_burns", "count_passes", "peak_altitude", "scale_angles", "clamp_tilt", "join_targets", "range_ratio"),
                   L=("burns", "passes", "altitudes", "targets"), S=("thrust", "inclination", "drag", "margin_deg"),
                   A=("delta_v", "visible", "apogee", "roster"), E=("burn", "pass_", "altitude", "target"), R=("apex", "ceiling_km")),
    "kennel": dict(F=("sum_meals", "count_walks", "oldest_pup", "scale_portions", "clamp_weight", "join_owners", "walk_ratio"),
                   L=("meals", "walks", "ages", "dogs"), S=("portion", "stride", "ration", "bump"),
                   A=("kibble", "walked", "oldest", "board"), E=("meal", "walk", "age", "dog"), R=("heavy", "limit_kg")),
    "harbor": dict(F=("sum_cargo", "count_docks", "deepest_berth", "scale_loads", "clamp_draft", "join_ships", "dock_ratio"),
                   L=("cargo", "docks", "berths", "ships"), S=("ballast", "tide", "toll", "allowance"),
                   A=("tonnage", "docked", "deepest", "fleet"), E=("crate", "dock", "berth", "ship"), R=("keel", "sill")),
}
HELD_OUT_PACKS = ("orbits", "kennel", "harbor")
TRAIN_PACKS = tuple(p for p in PACKS if p not in HELD_OUT_PACKS)
# break operators; two are held out for the sealed split
BREAK_OPS_TRAIN = ("drop_colon", "drop_paren", "bad_indent", "dup_operator")
BREAK_OPS_HELD = ("unterminated_string", "stray_keyword")
_ROLE = re.compile(r"\$([FLSAER])")
EXEC_CACHE: dict = {}


def apply_edit(file_text: str, old: str, new: str) -> dict:
    """The real str_replace run in a hermetic subprocess (PYTHONHASHSEED=0, temp dir, 5 s cap, no network code)."""
    key = hashlib.sha256(json.dumps([file_text, old, new]).encode()).hexdigest()
    if key in EXEC_CACHE:
        return EXEC_CACHE[key]
    env = {"PYTHONHASHSEED": "0", "PATH": os.environ.get("PATH", ""), "LC_ALL": "C.UTF-8"}
    with tempfile.TemporaryDirectory(prefix="t40edit_") as d:
        p = subprocess.run([sys.executable, "-I", "-B", str(HERE / "edit_exec.py")], input=json.dumps(
            {"file": file_text, "old": old, "new": new}), capture_output=True, text=True, cwd=d, env=env, timeout=5)
    if p.returncode != 0:
        raise RuntimeError(f"edit_exec failed: {p.stderr[-300:]}")
    out = json.loads(p.stdout)
    EXEC_CACHE[key] = out
    return out


# ----------------------------------------------------------------------------------------------- files as tokens

def build_file(rng: random.Random, pack: str) -> dict:
    """{"idents": [value, ...], "lines": [[token, ...], ...]}; a token is ["t", text] or ["s", ident index]."""
    v = PACKS[pack]
    idents: list = []

    def ident(role: str, fresh_from=None) -> int:
        val = fresh_from
        if val not in idents:
            idents.append(val)
        return idents.index(val)

    n_f = rng.randint(2, 4)
    shared = {"L": rng.choice(v["L"]), "E": rng.choice(v["E"]), "A": rng.choice(v["A"])}
    tpls = rng.sample(range(len(TEMPLATES)), n_f)
    fnames = rng.sample(v["F"], n_f)
    lines: list = []
    for j, ti in enumerate(tpls):
        roles = {"F": fnames[j], "L": shared["L"], "E": shared["E"],
                 "A": shared["A"] if rng.random() < 0.6 else rng.choice(v["A"]),
                 "S": rng.choice(v["S"]), "R": rng.choice(v["R"])}
        if roles["S"] == roles["R"]:
            roles["R"] = [x for x in v["R"] if x != roles["S"]][0]
        for ln in TEMPLATES[ti].split("\n"):
            toks, pos = [], 0
            for m in _ROLE.finditer(ln):
                if m.start() > pos:
                    toks.append(["t", ln[pos:m.start()]])
                toks.append(["s", ident(m.group(1), roles[m.group(1)])])
                pos = m.end()
            if pos < len(ln):
                toks.append(["t", ln[pos:]])
            lines.append(toks)
        lines.append([])
    return {"idents": idents, "lines": lines[:-1]}


def render_tokens(tokens: list, prefix: str, vals: dict, mark: bool = False) -> str:
    out = []
    for kind, x in tokens:
        out.append(x if kind == "t" else (f"{{{prefix}{x}:raw}}" if mark else vals[f"{prefix}{x}"]))
    return "".join(out)


def file_tokens(code: dict) -> list:
    toks: list = []
    for i, ln in enumerate(code["lines"]):
        if i:
            toks.append(["t", "\n"])
        toks += ln
    return toks


def _snippets(code: dict, vals: dict, rng) -> list:
    """Candidate fragments: [(tokens, rendered text, line index)] over one line (token runs) and two full lines."""
    full = render_tokens(file_tokens(code), "F", vals)
    out = []
    for i, ln in enumerate(code["lines"]):
        if not ln:
            continue
        for a in range(len(ln)):
            for b in range(a + 1, len(ln) + 1):
                toks = ln[a:b]
                text = render_tokens(toks, "F", vals)
                if 8 <= len(text) <= 44 and text.strip() and "\n" not in text:
                    out.append((toks, text, i, full.count(text)))
        if i + 1 < len(code["lines"]) and code["lines"][i + 1]:
            toks = ln + [["t", "\n"]] + code["lines"][i + 1]
            text = render_tokens(toks, "F", vals)
            if len(text) <= 80:
                out.append((toks, text, i, full.count(text)))
    return out


# ----------------------------------------------------------------------------------------------- modifications

def _lit_positions(tokens, pred):
    return [i for i, (k, x) in enumerate(tokens) if k == "t" and pred(x)]


def modify_ok(rng, tokens: list, code: dict) -> list:
    """A syntactically-safe replacement of the fragment (token list); [] when no safe edit applies."""
    cands = []
    for i in _lit_positions(tokens, lambda x: re.search(r"\d", x)):
        for m in re.finditer(r"\d", tokens[i][1]):
            d = str((int(m.group()) + rng.randint(1, 8)) % 10)
            cands.append(("digit", i, tokens[i][1][:m.start()] + d + tokens[i][1][m.end():]))
    for i in _lit_positions(tokens, lambda x: any(o in x for o in (" + ", " - ", " * "))):
        for o in (" + ", " - ", " * "):
            if o in tokens[i][1]:
                n = rng.choice([x for x in (" + ", " - ", " * ") if x != o])
                cands.append(("operator", i, tokens[i][1].replace(o, n, 1)))
    for i, (k, x) in enumerate(tokens):
        if k == "s" and len(code["idents"]) > 1:
            j = rng.choice([y for y in range(len(code["idents"])) if y != x])
            cands.append(("ident", i, j))
    if tokens and tokens[-1][0] == "s":
        cands.append(("append", len(tokens), " + 1"))
    if not cands:
        return []
    kind, i, val = rng.choice(cands)
    new = [list(t) for t in tokens]
    if kind in ("digit", "operator"):
        new[i] = ["t", val]
    elif kind == "ident":
        new[i] = ["s", val]
    else:
        new.append(["t", val])
    return new


def break_tokens(rng, tokens: list, ops: tuple) -> list:
    """A replacement meant to break the syntax of the edited file; [] when the operator does not apply."""
    op = rng.choice(ops)
    new = [list(t) for t in tokens]
    lits = [i for i, (k, x) in enumerate(new) if k == "t"]
    if op == "drop_colon":
        for i in reversed(lits):
            if new[i][1].rstrip().endswith(":"):
                new[i][1] = new[i][1].rstrip()[:-1]
                return new
    elif op == "drop_paren":
        for i in lits:
            if ")" in new[i][1]:
                new[i][1] = new[i][1].replace(")", "", 1)
                return new
    elif op == "bad_indent":
        for i in lits:
            if "\n" in new[i][1]:
                new[i][1] = new[i][1].replace("\n", "\n ", 1)
                return new
        if lits and new[lits[0]][1].startswith(" "):
            new[lits[0]][1] = " " + new[lits[0]][1]
            return new
    elif op == "dup_operator":
        for i in lits:
            for o in (" + ", " - ", " * "):
                if o in new[i][1]:
                    new[i][1] = new[i][1].replace(o, o + "* ", 1)
                    return new
    elif op == "unterminated_string":
        return [["t", '"']] + new
    elif op == "stray_keyword":
        return new + [["t", " else"]]
    return []


# ----------------------------------------------------------------------------------------------- W4: label-group sharing
# A choice group (4 seeds, every label once) shares ONE file, ONE count-1 fragment f1 (APPLIES_ONCE / NO_MATCH / BREAKS_SYNTAX) and
# ONE count>=2 fragment f2 of nearly the same length (MULTIPLE); all edits keep len(new) == len(old). The labels then differ only in
# the edit (a typo in old_str, a broken new_str, the repeated fragment), never in file shape, length or number statistics.

def modify_options_eq(tokens: list, code: dict) -> list:
    """All length-preserving safe replacements of the fragment (token lists): digit, operator, same-length identifier."""
    out = []
    for i in _lit_positions(tokens, lambda x: re.search(r"\d", x)):
        for m in re.finditer(r"\d", tokens[i][1]):
            for d in "0123456789":
                if d != m.group():
                    new = [list(t) for t in tokens]
                    new[i] = ["t", tokens[i][1][:m.start()] + d + tokens[i][1][m.end():]]
                    out.append(new)
    for i in _lit_positions(tokens, lambda x: any(o in x for o in (" + ", " - ", " * "))):
        for o in (" + ", " - ", " * "):
            if o in tokens[i][1]:
                for n in (" + ", " - ", " * "):
                    if n != o:
                        new = [list(t) for t in tokens]
                        new[i] = ["t", tokens[i][1].replace(o, n, 1)]
                        out.append(new)
    for i, (k, x) in enumerate(tokens):
        if k == "s":
            for j, v in enumerate(code["idents"]):
                if j != x and len(v) == len(code["idents"][x]):
                    new = [list(t) for t in tokens]
                    new[i] = ["s", j]
                    out.append(new)
    return out


def break_options_eq(tokens: list, ops: tuple) -> list:
    """All length-preserving replacements meant to break the syntax of the edited file."""
    out = []
    lits = [i for i, (k, x) in enumerate(tokens) if k == "t"]

    def cp():
        return [list(t) for t in tokens]
    if "drop_colon" in ops:                      # a trailing colon becomes a semicolon
        for i in lits:
            if tokens[i][1].rstrip().endswith(":") and tokens[i][1].endswith(":"):
                n = cp()
                n[i][1] = n[i][1][:-1] + ";"
                out.append(n)
    if "drop_paren" in ops:                      # a closing parenthesis becomes a bracket
        for i in lits:
            if ")" in tokens[i][1]:
                n = cp()
                n[i][1] = n[i][1].replace(")", "]", 1)
                out.append(n)
    if "bad_indent" in ops:                      # one indentation space moves to the end of the fragment
        for i in lits:
            m = re.search(r"\n( {2,})", tokens[i][1]) or re.match(r"( {2,})", tokens[i][1])
            if m:
                n = cp()
                a, b = m.span(1)
                n[i][1] = n[i][1][:a] + n[i][1][a + 1:b] + n[i][1][b:]
                n.append(["t", " "])
                out.append(n)
                break
    if "dup_operator" in ops:                    # an operator loses its closing space and gains a slash
        for i in lits:
            for o in (" + ", " - ", " * "):
                if o in tokens[i][1]:
                    n = cp()
                    n[i][1] = n[i][1].replace(o, o[:2] + "/", 1)
                    out.append(n)
    if "unterminated_string" in ops:             # a quote opens, the last character goes
        if lits and tokens[-1][0] == "t" and len(tokens[-1][1]) >= 2:
            n = cp()
            n[-1][1] = n[-1][1][:-1]
            out.append([["t", '"']] + n)
    if "stray_keyword" in ops:                   # the last five characters become " else"
        if tokens and tokens[-1][0] == "t" and len(tokens[-1][1]) >= 6:
            n = cp()
            n[-1][1] = n[-1][1][:-5] + " else"
            out.append(n)
    return out


def nomatch_options_eq(tokens: list, code: dict) -> list:
    """All length-preserving corruptions of old_str: (new tokens, override or None). An identifier typo is an override of the O slot."""
    out = []
    for i, (k, x) in enumerate(tokens):
        if k == "s":
            bad = typo_ident(random.Random(code["idents"][x]), code["idents"][x])
            if bad != code["idents"][x] and len(bad) == len(code["idents"][x]):
                out.append(([list(t) for t in tokens], (f"O{x}", bad, x)))
    if tokens and tokens[0][0] == "t" and tokens[0][1].startswith(" "):
        n = [list(t) for t in tokens]
        n[0][1] = "\t" + n[0][1][1:]
        out.append((n, None))
    for i, (k, x) in enumerate(tokens):
        if k == "t":
            for a, b in ((" + ", " - "), (" - ", " + "), (" > ", " < "), (" < ", " > ")):      # W4: no corruption changes a bracket / star count
                if a in x:
                    n = [list(t) for t in tokens]
                    n[i] = ["t", x.replace(a, b, 1)]
                    out.append((n, None))
                    break
    return out


def draw_group(grng: random.Random, sampler: str, pack: str) -> dict:
    """The label-independent part of a head C choice group: {"code", "f1", "f2", "new1", "new2"} (token lists)."""
    held = sampler == "S5"
    ops = BREAK_OPS_HELD if held else BREAK_OPS_TRAIN
    for _ in range(200):
        code = build_file(grng, pack)
        vals = {f"F{k}": v for k, v in enumerate(code["idents"])}
        snips = _snippets(code, vals, grng)
        mult = [s for s in snips if s[3] >= 2]
        single = [s for s in snips if s[3] == 1]
        if not mult or not single:
            continue
        want = grng.randint(10, 40)
        mult.sort(key=lambda s: (abs(len(s[1]) - want) // 3, grng.random()))
        for toks2, text2, _, _ in mult[:6]:
            m2 = modify_options_eq(toks2, code)
            if not m2:
                continue
            dig2 = bool(re.search(r"\d", text2))
            prof2 = (text2.count("("), text2.count("["), text2.count("*"), text2.count('"'))
            single.sort(key=lambda s: ((s[1].count("("), s[1].count("["), s[1].count("*"), s[1].count('"')) != prof2, abs(len(s[1]) - len(text2)) // 2,
                                       bool(re.search(r"\d", s[1])) != dig2, grng.random()))
            for toks1, text1, _, _ in single[:10]:
                m1 = modify_options_eq(toks1, code)
                if not m1 or not nomatch_options_eq(toks1, code):
                    continue
                new1 = grng.choice(m1)
                brk = break_options_eq(new1, ops)
                if not brk:
                    continue
                new2 = grng.choice(m2)
                vals = {f"F{k}": v for k, v in enumerate(code["idents"])}

                def run(o, n):
                    return label_of(code, o, n, slots_for(code, o, n, {}))["label"]
                if (run(toks1, new1) != "APPLIES_ONCE" or run(toks2, new2) != "MULTIPLE"
                        or not any(run(toks1, b) == "BREAKS_SYNTAX" for b in brk)):
                    continue
                return {"code": code, "f1": [list(t) for t in toks1], "f2": [list(t) for t in toks2],
                        "new1": new1, "new2": new2}
    raise ValueError("no shareable group draw")


# ----------------------------------------------------------------------------------------------- the draw

def slots_for(code: dict, old, new, overrides: dict) -> dict:
    sl = {f"F{k}": v for k, v in enumerate(code["idents"])}
    for pre, toks in (("O", old), ("N", new)):
        for kind, x in toks:
            if kind == "s":
                sl[f"{pre}{x}"] = code["idents"][x]
    sl.update(overrides)
    return sl


def label_of(code: dict, old, new, vals: dict) -> dict:
    return apply_edit(render_tokens(file_tokens(code), "F", vals), render_tokens(old, "O", vals),
                      render_tokens(new, "N", vals))


def typo_ident(rng, s: str) -> str:
    idx = [i for i in range(1, len(s) - 1) if s[i].isalpha() and s[i + 1].isalpha() and s[i] != s[i + 1]]
    if not idx:
        return s + "x"
    i = rng.choice(idx)
    return s[:i] + s[i + 1] + s[i] + s[i + 2:]


def draw_shared(rng: random.Random, label: str, sampler: str, pack: str, grp: dict) -> tuple:
    """(structure, slots) for the target label inside a shared choice group (W4): only the edit differs between labels."""
    held = sampler == "S5"
    code = grp["code"]
    vals = {f"F{k}": v for k, v in enumerate(code["idents"])}
    old = [list(t) for t in (grp["f2"] if label == "MULTIPLE" else grp["f1"])]
    new = [list(t) for t in (grp["new2"] if label == "MULTIPLE" else grp["new1"])]
    overrides: dict = {}
    twin = None
    if label == "BREAKS_SYNTAX":
        opts = break_options_eq(new, BREAK_OPS_HELD if held else BREAK_OPS_TRAIN)
        if not opts:
            raise ValueError("no break applies")
        new = rng.choice(opts)
    elif label == "NO_MATCH":
        opts = nomatch_options_eq(old, code)
        old, ov = rng.choice(opts)
        if ov is not None:
            overrides[ov[0]] = ov[1]
            twin = {"slot": ov[0], "alt": code["idents"][ov[2]]}
    elif label == "APPLIES_ONCE":
        s_idx = [(i, x) for i, (k, x) in enumerate(old) if k == "s"]
        if s_idx:
            twin = {"slot": f"O{s_idx[0][1]}", "alt": typo_ident(rng, code["idents"][s_idx[0][1]])}
    sl = slots_for(code, old, new, overrides)
    got = label_of(code, old, new, sl)["label"]
    if got != label:
        raise ValueError(f"run says {got}, wanted {label}")
    if twin is not None:
        alt_sl = dict(sl)
        alt_sl[twin["slot"]] = twin["alt"]
        alt = label_of(code, old, new, alt_sl)["label"]
        want_alt = "APPLIES_ONCE" if label == "NO_MATCH" else "NO_MATCH"
        if alt != want_alt:
            twin = None
        else:
            twin["alt_label"] = alt
    structure = {"head": "C", "pack": pack, "path": f"src/{pack}.py", "code": code, "old": old, "new": new, "twin": twin,
                 "meta_target_len": len(render_tokens(grp["f1"], "F", vals))}
    return structure, sl


def draw(rng: random.Random, label: str, sampler: str, pack: str | None = None, grp: dict | None = None) -> tuple:
    """(structure, slots) for the target label; the REAL run decides, a miss raises ValueError (the caller redraws)."""
    if grp is not None:
        return draw_shared(rng, label, sampler, pack, grp)
    held = sampler == "S5"
    pack = pack or rng.choice(HELD_OUT_PACKS if held else TRAIN_PACKS)
    code = build_file(rng, pack)
    vals = {f"F{k}": v for k, v in enumerate(code["idents"])}
    snips = _snippets(code, vals, rng)
    want_len = rng.randint(10, 40)
    if not any(s[3] >= 2 for s in snips):       # A45: every file holds a repeated fragment, whatever the label (MULTIPLE needs one)
        raise ValueError("file has no repeated fragment")
    pool = [s for s in snips if (s[3] >= 2) == (label == "MULTIPLE") and (s[3] >= 1)]
    if not pool:
        raise ValueError("no fragment of the needed count")
    best = min(abs(len(s[1]) - want_len) for s in pool)
    order = sorted(pool, key=lambda s: (abs(len(s[1]) - want_len) // 3, rng.random()))
    new = []
    for toks, text, li, cnt in order[:12]:
        new = (break_tokens(rng, toks, BREAK_OPS_HELD if held else BREAK_OPS_TRAIN) if label == "BREAKS_SYNTAX"
               else modify_ok(rng, toks, code))
        if new:
            break
    if not new:
        raise ValueError("no edit applies to the fragment")
    old = [list(t) for t in toks]
    overrides: dict = {}
    twin = None
    if label == "NO_MATCH":
        how = rng.choice(("ident_typo", "indent", "op_flip"))
        s_idx = [i for i, (k, x) in enumerate(old) if k == "s"]
        if how in ("ident_typo", "ident_case") and s_idx:
            k = old[rng.choice(s_idx)][1]
            bad = typo_ident(rng, code["idents"][k])
            if bad != code["idents"][k]:
                overrides[f"O{k}"] = bad
                twin = {"slot": f"O{k}", "alt": code["idents"][k]}
            how = "slot"
        if how == "indent" or (how in ("ident_typo", "ident_case") and not overrides):
            if old[0][0] == "t" and old[0][1].startswith(" "):
                old[0] = ["t", " " + old[0][1]]
            else:
                how = "op_flip"
        if how == "op_flip" and not overrides:
            done = False
            for i, (k, x) in enumerate(old):
                if k == "t":
                    for a, b in ((" + ", " - "), (" * ", " / "), (" > ", " < "), ("(", "((")):
                        if a in x:
                            old[i] = ["t", x.replace(a, b, 1)]
                            done = True
                            break
                if done:
                    break
            if not done:
                raise ValueError("no corruption applies")
    elif label == "APPLIES_ONCE":
        s_idx = [(i, x) for i, (k, x) in enumerate(old) if k == "s"]
        if s_idx:
            k = s_idx[0][1]
            twin = {"slot": f"O{k}", "alt": typo_ident(rng, code["idents"][k])}
    sl = slots_for(code, old, new, overrides)
    got = label_of(code, old, new, sl)["label"]
    if got != label:
        raise ValueError(f"run says {got}, wanted {label}")
    if twin is not None:                       # verify the twin's construction with a real run
        alt_sl = dict(sl)
        alt_sl[twin["slot"]] = twin["alt"]
        alt = label_of(code, old, new, alt_sl)["label"]
        want_alt = "APPLIES_ONCE" if label == "NO_MATCH" else "NO_MATCH"
        if alt != want_alt:
            twin = None
        else:
            twin["alt_label"] = alt
    structure = {"head": "C", "pack": pack, "path": f"src/{pack}.py", "code": code, "old": old, "new": new, "twin": twin,
                 "meta_target_len": want_len}
    return structure, sl
