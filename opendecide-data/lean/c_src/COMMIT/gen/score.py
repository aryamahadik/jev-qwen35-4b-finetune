"""SCORE generator (G0 section 4): ordinal choice over K = 3..7 levels "Level k - <name>" (masked: "Level k"),
rubric templates RT1 bands, RT2 bands + raise, RT3 max with class floors, RT4 decision list, RT5 points; samplers
S1-S4, S6 (card-level; all draw level-first for the per-rubric level floor); cut twins (1.6); meta.option_level.
Solver A: imperative evaluator over the record. Parser + solver B: rubric re-parsed from the rendered prompt, numstat
parsed from state, quantities and per-level membership predicates in sqlite; exactly one level must be true."""
from __future__ import annotations

import collections
import math
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

CLS = L.GATE_CLASSES
SCORE_CLS = ["test", "documentation", "CI", "build script", "manifest", "config", "migration", "security", "script",
             "container", "lockfile", "template"]
CC, PF = "CommitChronicle", "CommitPackFT"


def qphrase(q: tuple) -> str:
    if q[0] == "lines":
        return "changed lines"
    if q[0] == "files":
        return "files changed"
    if q[0] == "clines":
        return f"changed lines in {q[1]} files"
    return f"number of {q[1]} files"


def level_text(k: int, names: list[str] | None) -> str:
    return f"Level {k}" if names is None else f"Level {k} - {names[k - 1]}"


def band_text(lo: int, hi: int | None) -> str:
    return f"from {lo} up to {hi}" if hi is not None else f"{lo} or more"


# ---------------------------------------------------------------------------------------------------------------
# solver A

def qval_A(q: tuple, rec: dict) -> int:
    if q[0] == "lines":
        return rec["added"] + rec["removed"]
    if q[0] == "files":
        return len(rec["files"])
    fs = [f for f in rec["files"] if K.file_in_A(f, CLS[q[1]])]
    return sum(f["added"] + f["removed"] for f in fs) if q[0] == "clines" else len(fs)


def band(v: int, cuts: list[int]) -> int:
    """1-based band of v under cuts c1 < ... (band j: c_{j-1} <= v < c_j)."""
    return 1 + sum(1 for c in cuts if v >= c)


def touched_A(c: str, rec: dict) -> bool:
    return any(K.file_in_A(f, CLS[c]) for f in rec["files"])


def cond_A(cond, rec) -> bool:
    if cond[0] == "cmp":
        _, q, op, t = cond
        v = qval_A(q, rec)
        return v > t if op == "more than" else v >= t
    if cond[0] == "any":
        return touched_A(cond[1], rec)
    vals = [cond_A(x, rec) for x in cond[2]]
    return all(vals) if cond[1] == "all" else any(vals)


def level_A(rb: dict, rec: dict) -> int:
    t, Kk = rb["tpl"], rb["K"]
    if t == "RT1":
        return band(qval_A(rb["q"], rec), rb["cuts"])
    if t == "RT2":
        return min(Kk, band(qval_A(rb["q"], rec), rb["cuts"]) + sum(touched_A(c, rec) for c in rb["raise"]))
    if t == "RT3":
        lv = band(qval_A(rb["q"], rec), rb["cuts"])
        for c, j in rb["floors"]:
            if touched_A(c, rec):
                lv = max(lv, j)
        return lv
    if t == "RT4":
        for k, cond in rb["lines"]:
            if cond_A(cond, rec):
                return k
        return 1
    pts = sum(p for c, p in rb["points"] if touched_A(c, rec))
    pts += rb["size_pts"][band(qval_A(rb["q"], rec), rb["size_cuts"]) - 1]
    return band(pts, rb["cuts"])


# ---------------------------------------------------------------------------------------------------------------
# rubric text (instructions + option definition lines)

def cond_text(cond) -> str:
    if cond[0] == "cmp":
        _, q, op, t = cond
        return f"the number of {qphrase(q)} is {op} {t}"
    if cond[0] == "any":
        return f"any {cond[1]} file changes"
    items = "; ".join(f"[{i + 1}] {cond_text(x)}" for i, x in enumerate(cond[2]))
    return f"{cond[1]} of these are true: {items}"


def rubric_classes(rb: dict) -> list[str]:
    out = []

    def add(c):
        if c and c not in out:
            out.append(c)
    if rb.get("q") and rb["q"][0] in ("clines", "cfiles"):
        add(rb["q"][1])
    for c in rb.get("raise", []):
        add(c)
    for c, _ in rb.get("floors", []):
        add(c)
    for c, _ in rb.get("points", []):
        add(c)

    def walk(cond):
        if cond[0] == "cmp":
            if cond[1][0] in ("clines", "cfiles"):
                add(cond[1][1])
        elif cond[0] == "any":
            add(cond[1])
        else:
            for x in cond[2]:
                walk(x)
    for _, cond in rb.get("lines", []):
        walk(cond)
    return out


def rubric_blocks(rb: dict, names) -> tuple[list[dict], list[dict]]:
    """(instruction blocks, defs entries). Defs only on RT1 / RT5 (ranges next to the levels, SEM-11)."""
    t, Kk = rb["tpl"], rb["K"]
    blocks, defs = [], []
    q = qphrase(rb["q"]) if rb.get("q") else None
    if t == "RT1":
        blocks.append({"type": "para", "text": f"Rubric: the level is set by the {q} of the change."})
        cuts = [0] + rb["cuts"]
        for k in range(1, Kk + 1):
            defs.append({"name": level_text(k, names), "text": f"{q} {band_text(cuts[k - 1], cuts[k] if k < Kk else None)}"})
    elif t in ("RT2", "RT3"):
        cuts = [0] + rb["cuts"]
        rows = "; ".join(f"size level {k}: {q} {band_text(cuts[k - 1], cuts[k] if k < len(cuts) else None)}"
                         for k in range(1, len(cuts) + 1))
        blocks.append({"type": "para", "text": f"Size table: {rows}."})
        if t == "RT2":
            blocks.append({"type": "para", "text": "Raise list: raise the level by one for each of these classes "
                                                   "the change touches: " + ", ".join(rb["raise"]) + "."})
        else:
            for c, j in rb["floors"]:
                blocks.append({"type": "para", "text": f"Class floor: if any {c} file changes, the level is at least "
                                                       f"Level {j}."})
    elif t == "RT4":
        items = [f"Level {k} if {cond_text(cond)}." for k, cond in rb["lines"]] + ["Level 1 otherwise."]
        blocks.append({"type": "para", "text": "Decision list (top to bottom): " + " ".join(items)})
    else:
        items = [f"any {c} file changes: {p} points" for c, p in rb["points"]]
        sc = [0] + rb["size_cuts"]
        items += [f"{q} {band_text(sc[j], sc[j + 1] if j + 1 < len(sc) else None)}: {rb['size_pts'][j]} points"
                  for j in range(len(sc))]
        blocks.append({"type": "para", "text": "Points table: " + "; ".join(items) + "."})
        cuts = [0] + rb["cuts"]
        for k in range(1, Kk + 1):
            defs.append({"name": level_text(k, names), "text": f"points {band_text(cuts[k - 1], cuts[k] if k < Kk else None)}"})
    if t in ("RT2", "RT3", "RT4"):
        blocks.append({"type": "para", "text": "Levels: " + ", ".join(level_text(k, names) for k in range(1, Kk + 1))
                                               + "."})
    for c in rubric_classes(rb):
        blocks.append({"type": "para", "text": T.class_line(c, CLS[c])})
    return blocks, defs


def clause_ids(rb: dict) -> list[str]:
    # SEM-05 / SEM-07 left out (inactive on every row: the builder keeps no renamed, binary or mode-only file)
    ids = ["SEM-01", "SEM-02", "SEM-06", "SEM-08", "SEM-09", "SEM-22", "SEM-23", "SEM-30",
           "SEM-31d", "SEM-32", "SEM-33", "SEM-36", "SEM-37", "SEM-41"]
    t = rb["tpl"]
    ids += {"RT1": ["SEM-11"], "RT2": ["SEM-11b", "SEM-20"], "RT3": ["SEM-11b", "SEM-19"],
            "RT4": ["SEM-18", "SEM-10", "SEM-12", "SEM-13", "SEM-39"], "RT5": ["SEM-11", "SEM-21"]}[t]
    if t == "RT4":
        ids.append("SEM-35")
    return ids


def card_ir(rb: dict, names, defs_style: str, fewshot=None) -> dict:
    blocks, defs = rubric_blocks(rb, names)
    blocks.append({"type": "section", "heading": "How to read the rubric",
                   "blocks": [{"type": "items", "items": [T.SEM[i] for i in clause_ids(rb)]}]})
    if defs:
        blocks.append({"type": "defs", "variant": "DV01", "heading": "Levels", "entries": defs})
    if fewshot:
        blocks.append({"type": "fewshot", "template": fewshot[0], "heading": None, "examples": fewshot[1]})
    return {"title": "Scoring rubric", "blocks": blocks}


# ---------------------------------------------------------------------------------------------------------------
# parser + solver B (rendered prompt only)

B_Q = re.compile(r"^(changed lines|files changed|changed lines in (.+?) files|number of (.+?) files)$")


def B_q(s: str):
    m = B_Q.match(s.strip())
    if not m:
        raise ValueError("quantity: " + s)
    if m.group(1) == "changed lines":
        return ("lines",)
    if m.group(1) == "files changed":
        return ("files",)
    if m.group(2):
        return ("clines", m.group(2))
    return ("cfiles", m.group(3))


def B_band(s: str):
    m = re.match(r"^(.*?) (?:from (\d+) up to (\d+)|(\d+) or more)$", s.strip())
    lo = int(m.group(2) or m.group(4))
    hi = int(m.group(3)) if m.group(3) else None
    return m.group(1), lo, hi


def B_cond(s: str):
    s = s.strip()
    m = re.match(r"^(all|any) of these are true: (.+)$", s)
    if m:
        return ("list", m.group(1), [B_cond(x) for x in re.split(r";? ?\[\d+\] ", " " + m.group(2)) if x.strip()])
    m = re.match(r"^any (.+?) file changes$", s)
    if m:
        return ("any", m.group(1))
    m = re.match(r"^the number of (.+) is (more than|at least) (\d+)$", s)
    if m:
        return ("cmp", B_q(m.group(1)), m.group(2), int(m.group(3)))
    raise ValueError("cond: " + s)


def B_parse(row: dict) -> dict:
    ins, card = row["instructions"], row["card"] or ""
    rb = {"levels": list(row["options"])}
    classes = {}
    for ln in ins.split("\n"):
        m = re.search(r"Rubric: the level is set by the (.+) of the change\.", ln)
        if m:
            rb["tpl"], rb["q"] = "RT1", B_q(m.group(1))
        m = re.search(r"Size table: (.+)\.$", ln)
        if m:
            rb.setdefault("tpl", "RT2/3")
            bands = [B_band(x.split(": ", 1)[1]) for x in m.group(1).split("; ")]
            rb["q"] = B_q(bands[0][0])
            rb["size_bands"] = [(lo, hi) for _, lo, hi in bands]
        m = re.search(r"Raise list: raise the level by one for each of these classes the change touches: (.+)\.$", ln)
        if m:
            rb["tpl"], rb["raise"] = "RT2", m.group(1).split(", ")
        m = re.search(r"Class floor: if any (.+?) file changes, the level is at least Level (\d+)\.$", ln)
        if m:
            rb["tpl"] = "RT3"
            rb.setdefault("floors", []).append((m.group(1), int(m.group(2))))
        m = re.search(r"Decision list \(top to bottom\): (.+)$", ln)
        if m:
            rb["tpl"] = "RT4"
            body = m.group(1)
            parts = re.findall(r"Level (\d+) if (.+?)\.(?= Level \d+ (?:if|otherwise))", body)
            rb["lines"] = [(int(k), B_cond(c)) for k, c in parts]
        m = re.search(r"Points table: (.+)\.$", ln)
        if m:
            rb["tpl"] = "RT5"
            pts, size = [], []
            for it in m.group(1).split("; "):
                mm = re.match(r"^any (.+?) file changes: (\d+) points$", it)
                if mm:
                    pts.append((mm.group(1), int(mm.group(2))))
                    continue
                left, p = it.rsplit(": ", 1)
                qn, lo, hi = B_band(left)
                rb["q"] = B_q(qn)
                size.append((lo, hi, int(p.split()[0])))
            rb["points"], rb["size"] = pts, size
        m = re.search(r"(?:^|\W)([A-Za-z][A-Za-z ]*?) files: (.+)\.$", ln)
        if m and "Rubric" not in ln and "table" not in ln:
            folders, pats = [], []
            for part in m.group(2).split("; or "):
                mm = re.match(r"any file in a folder named (.+)$", part)
                if mm:
                    folders = _split_or(mm.group(1))
                mm = re.match(r"any file whose file name matches (.+)$", part)
                if mm:
                    pats = _split_or(mm.group(1))
            classes[m.group(1).strip()] = {"folders": folders, "patterns": pats}
    defs = {}
    for ln in card.split("\n"):
        m = re.match(r"^- (Level \d+(?: - [^:]+)?): (.+)$", ln)
        if m:
            defs[m.group(1)] = m.group(2)
    rb["defs"] = defs
    rb["classes"] = classes
    return rb


def _split_or(s):
    if " or " in s:
        head, last = s.rsplit(" or ", 1)
        return [x.strip() for x in head.split(", ")] + [last.strip()]
    return [s.strip()]


def B_solve(row: dict) -> str:
    rb = B_parse(row)
    st = K.parse_state(row["state"])
    stats, tot = st["stats"], st["total"]
    if stats is None or tot is None or tot != (len(stats), sum(a + r for a, r, _ in stats)):
        raise ValueError("numstat/total")
    db = K.ClassDB(rb["classes"])
    fcls = db.classes_of([p for _, _, p in stats])
    con = sqlite3.connect(":memory:")
    con.execute("create table f(fid int, added int, removed int)")
    con.execute("create table fc(fid int, cls text)")
    for i, (a, r, p) in enumerate(stats):
        con.execute("insert into f values (?,?,?)", (i, a, r))
        for c in fcls[i]:
            con.execute("insert into fc values (?,?)", (i, c))

    def qv(q):
        if q[0] == "lines":
            return con.execute("select coalesce(sum(added+removed),0) from f").fetchone()[0]
        if q[0] == "files":
            return con.execute("select count(*) from f").fetchone()[0]
        if q[0] == "clines":
            return con.execute("select coalesce(sum(added+removed),0) from f where fid in (select fid from fc where "
                               "cls=?)", (q[1],)).fetchone()[0]
        return con.execute("select count(distinct fid) from fc where cls=?", (q[1],)).fetchone()[0]

    def has(c):
        return con.execute("select exists(select 1 from fc where cls=?)", (c,)).fetchone()[0] == 1

    def cond(cd):
        if cd[0] == "cmp":
            v = qv(cd[1])
            return v > cd[3] if cd[2] == "more than" else v >= cd[3]
        if cd[0] == "any":
            return has(cd[1])
        vs = [cond(x) for x in cd[2]]
        return all(vs) if cd[1] == "all" else any(vs)

    levels = rb["levels"]
    Kk = len(levels)
    num = {o: int(re.match(r"Level (\d+)", o).group(1)) for o in levels}

    def in_range(v, txt):
        _, lo, hi = B_band("x " + txt.split(" ", 1)[1] if txt.startswith("points") else txt)
        return lo <= v and (hi is None or v < hi)
    true = []
    for o in levels:
        k = num[o]
        if rb["tpl"] == "RT1":
            d = rb["defs"][o]
            qn, lo, hi = B_band(d)
            ok = lo <= qv(B_q(qn)) and (hi is None or qv(B_q(qn)) < hi)
        elif rb["tpl"] == "RT5":
            pts = sum(p for c, p in rb["points"] if has(c))
            v = qv(rb["q"])
            pts += sum(p for lo, hi, p in rb["size"] if lo <= v and (hi is None or v < hi))
            _, lo, hi = B_band("points " + rb["defs"][o].split(" ", 1)[1])
            ok = lo <= pts and (hi is None or pts < hi)
        elif rb["tpl"] == "RT4":
            higher = [c for kk, c in rb["lines"] if kk > k]
            mine = [c for kk, c in rb["lines"] if kk == k]
            ok = not any(cond(c) for c in higher) and (cond(mine[0]) if mine else k == 1)
        else:
            v = qv(rb["q"])
            size = next(j + 1 for j, (lo, hi) in enumerate(rb["size_bands"]) if lo <= v and (hi is None or v < hi))
            if rb["tpl"] == "RT2":
                fin = min(Kk, size + sum(1 for c in rb["raise"] if has(c)))
            else:
                fin = max([size] + [j for c, j in rb.get("floors", []) if has(c)])
            ok = fin == k
        if ok:
            true.append(o)
    if len(true) != 1:
        raise ValueError(f"{len(true)} levels true")
    return true[0]


# ---------------------------------------------------------------------------------------------------------------
# rubrics, cards, rows

TPLS = ["RT1", "RT2", "RT3", "RT4", "RT5"]
SAMPLERS = ["S1", "S2", "S3", "S4", "S6"]


def _nice(x: float) -> int:
    if x < 10:
        return max(1, int(round(x)))
    p = 10 ** (len(str(int(x))) - 2)
    return int(round(x / p) * p)


def _quant_cuts(vals: list[int], n_cuts: int, scale: float) -> list[int] | None:
    vs = sorted(vals)
    if not vs:
        return None
    cuts = []
    for j in range(1, n_cuts + 1):
        c = _nice(scale * vs[min(len(vs) - 1, int(j * len(vs) / (n_cuts + 1)))])
        cuts.append(c)
    cuts = [max(1, c) for c in cuts]
    if any(b <= a for a, b in zip(cuts, cuts[1:])):
        return None
    return cuts


def make_rubric(i: int, cands: list[dict], rng) -> dict | None:
    tpl = TPLS[i % 5]
    Kk = [3, 4, 5, 6, 7][(i // 5) % 5] if tpl != "RT5" else [3, 4, 5][(i // 5) % 3]
    names = L.LEVEL_NAMES[Kk][(i // 2) % len(L.LEVEL_NAMES[Kk])]
    qk = rng.choice(["lines", "lines", "lines", "files", "clines", "cfiles"])
    q = (qk,) if qk in ("lines", "files") else (qk, rng.choice(SCORE_CLS[:6]))
    rb = {"tpl": tpl, "K": Kk, "names": names, "q": q, "rubric_id": f"SR{i + 1:03d}"}
    scale = math.exp(rng.uniform(math.log(0.7), math.log(1.4)))
    vals = [qval_A(q, r) for r in cands]
    if qk in ("clines", "cfiles") and sum(1 for v in vals if v > 0) < 0.15 * len(vals):
        q = ("lines",)
        rb["q"] = q
        vals = [qval_A(q, r) for r in cands]
    if tpl == "RT1":
        rb["cuts"] = _quant_cuts(vals, Kk - 1, scale)
    elif tpl in ("RT2", "RT3"):
        rb["cuts"] = _quant_cuts(vals, Kk - 2, scale)
        cl = rng.sample(SCORE_CLS, 2)
        if tpl == "RT2":
            rb["raise"] = cl[:1 + (Kk >= 5)]
        else:
            rb["floors"] = [(cl[0], Kk), (cl[1], max(2, Kk - 1))] if Kk >= 4 else [(cl[0], Kk)]
    elif tpl == "RT4":
        lv = _quant_cuts(vals if q[0] == "lines" else [qval_A(("lines",), r) for r in cands], Kk - 1, scale)
        if lv is None:
            return None
        sec = rng.choice(["security", "migration", "CI"])
        lines = []
        for k in range(Kk, 1, -1):
            c = ("cmp", ("lines",), rng.choice(["more than", "at least"]), lv[k - 2])
            if k == Kk:
                c = ("list", "any", [c, ("any", sec)])
            lines.append((k, c))
        rb["lines"], rb["q"] = lines, None
        rb["cuts"] = lv
    else:
        cl = rng.sample(SCORE_CLS, 2)
        rb["points"] = [(cl[0], rng.choice([1, 2])), (cl[1], rng.choice([1, 2, 3]))]
        rb["size_cuts"] = _quant_cuts(vals, 2, scale)
        rb["size_pts"] = [0, 1, 2] if rng.random() < 0.5 else [0, 2, 3]
        if rb["size_cuts"] is None:
            return None
        pts = []
        for r in cands:
            p = sum(pp for c, pp in rb["points"] if touched_A(c, r))
            p += rb["size_pts"][band(qval_A(q, r), rb["size_cuts"]) - 1]
            pts.append(p)
        cuts = sorted(set(pts))[1:]
        if len(cuts) < Kk - 1:
            return None
        idx = [int(j * len(cuts) / (Kk - 1)) for j in range(Kk - 1)]
        rb["cuts"] = sorted(set(cuts[x] for x in idx))
        if len(rb["cuts"]) != Kk - 1:
            return None
    if rb.get("cuts") is None:
        return None
    return rb


def build_cards(split_kind: str = "train", n: int = 40) -> list[dict]:
    cards = []
    i = 0
    while len(cards) < n and i < 4 * n:
        cid = f"CMS{len(cards) + 1:03d}" if split_kind == "train" else f"CMSD{len(cards) + 1:02d}"
        ds = CC if (split_kind != "train" or C.h01("score-ds", cid) < 7 / 12) else PF
        card = {"card_id": cid, "type": "score", "sampler": SAMPLERS[len(cards) % 5] if split_kind == "train" else "S5",
                "ds": ds, "r": None, "fewshot": False, "inverted": False,
                "defs_style": ["one_line", "rubric_table", "decision_list"][len(cards) % 3]}
        gsplit = "train" if split_kind == "train" else "heldout"
        cands = _cands(card, gsplit)
        rng = FR.rng("score-rubric", cid, i)
        rb = make_rubric(i, [FR.rec(x) for x in cands[:800]], rng)
        i += 1
        if rb is None:
            continue
        lv = collections.Counter(level_A(rb, FR.rec(x)) for x in cands[:800])
        if any(lv[k] < 8 for k in range(1, rb["K"] + 1)):
            continue
        card.update(rubric=rb, rubric_id=rb["rubric_id"], _cands=cands)
        cards.append(card)
    return cards


def _cands(card, gsplit, cap=3000):
    pk, gs = FR.pack(card["card_id"], gsplit, card["ds"], frac=0.4 if gsplit == "train" else 1.0)
    card["pack_id"] = pk
    gset = set(gs)
    ix = FR.index()
    rids = sorted((rid for rid, x in ix.items() if x["group"] in gset and x["split"] == gsplit and x["n_files"] <= 20
                   and not x["bot"]), key=lambda r: C.h01("scand", card["card_id"], r))
    out = []
    for rid in rids:
        r = FR.rec(rid)
        if K.plain_files(r) and sum(len(t) + 2 for f in r["files"] if any(K.file_in_A(f, CLS[c]) for c in SCORE_CLS)
                                    for h in f["hunks"] for _, t in h["lines"]) <= 2400:
            out.append(rid)
        if len(out) >= cap:
            break
    return out


def decisive(rec, rb):
    cs = rubric_classes(rb)
    out = set()
    for fi, f in enumerate(rec["files"]):
        if any(K.file_in_A(f, CLS[c]) for c in cs):
            for hi, h in enumerate(f["hunks"]):
                out.update((fi, hi, li) for li in range(len(h["lines"])))
    return out


def extra(rec, rb, budget):
    sh = K.shorten(rec, budget, decisive(rec, rb))
    if sh is None:
        return None
    return K.fence(K.numstat_block(rec), "stats") + "\n\n" + K.fence(K.render_shown(sh), "diff"), {}


def _cut_variant(rb: dict, rec: dict, salt: str):
    if rb["tpl"] == "RT4":
        return None
    key = "cuts" if rb["tpl"] in ("RT1", "RT5") else "cuts"
    v = qval_A(rb["q"], rec) if rb["tpl"] != "RT5" else (
        sum(p for c, p in rb["points"] if touched_A(c, rec)) + rb["size_pts"][band(qval_A(rb["q"], rec),
                                                                                    rb["size_cuts"]) - 1])
    cuts = rb[key]
    j = band(v, cuts)  # 1-based
    lo = cuts[j - 2] if j >= 2 else 0
    hi = cuts[j - 1] if j - 1 < len(cuts) else None
    opts = []
    if hi is not None and v > lo and (j - 2 < 0 or v > cuts[j - 2]):
        new = list(cuts)
        new[j - 1] = v
        if all(b > a for a, b in zip(new, new[1:])) and new[0] >= 1:
            opts.append(new)
    if j >= 2 and v + 1 < (hi if hi is not None else 10 ** 9):
        new = list(cuts)
        new[j - 2] = v + 1
        if all(b > a for a, b in zip(new, new[1:])):
            opts.append(new)
    base = level_A(rb, rec)
    for new in sorted(opts, key=lambda x: C.h01("cutv", salt, str(x))):
        rb2 = {**rb, key: new}
        if abs(level_A(rb2, rec) - base) == 1:
            return rb2
    return None


def build_rows(card: dict, em: FR.Emitter, reg: FR.Registry, split: str, n_rows: int, twin_share: float = 0.22):
    rb = card["rubric"]
    stats = collections.Counter()
    cands = [r for r in card["_cands"] if reg.can_base(r, "score", split)]
    lvl = {r: level_A(rb, FR.rec(r)) for r in cands}
    by = collections.defaultdict(list)
    for r in cands:
        by[lvl[r]].append(r)
    wds = FR.card_wordings("score", "choice", card["card_id"])
    n_tw = int(twin_share * n_rows) if split != "dev" and rb["tpl"] != "RT4" else 0
    n_base = n_rows - n_tw
    Kk = rb["K"]
    pos = card.get('_pos_' + split, 0)
    tw_left = n_tw
    for i in range(n_base):
        k = 1 + (i % Kk)
        pool_ = [r for r in by[k] if reg.can_base(r, "score", split)]
        if not pool_:
            stats["level_short"] += 1
            continue
        def pref(r):
            rec = FR.rec(r)
            s = card["sampler"]
            if s == "S3" and rb.get("q") and rb["tpl"] != "RT4":
                v = qval_A(rb["q"], rec)
                return min(abs(v - c) for c in rb["cuts"])
            if s == "S4":
                cl = rubric_classes(rb)
                has = any(touched_A(c, rec) for c in cl)
                big = rec["added"] + rec["removed"] > 100
                return 0 if has != big else 1
            return 0
        pool_.sort(key=lambda r: (pref(r), C.h01("spick", card["card_id"], split, r)))
        rid = pool_[0]
        rec = FR.rec(rid)
        tw = None
        if tw_left > 0:
            tw = _cut_variant(rb, rec, rid)
        reg.take_base(rid, "score", split)
        pos += 1
        masked = (not card["fewshot"]) and C.h01("mask", card["card_id"], rid) < 0.12 and tw is None
        a = _emit(card, em, split, rec, rb, wds, pos, "-b", masked)
        if a and tw is not None:
            t = _emit(card, em, split, rec, tw, wds, pos, "-c1", False, twin_of=a["id"],
                      variant=f"{card['card_id']}-C{C.sha256(str(tw['cuts']))[:6]}")
            if t:
                tw_left -= 1
        stats["units"] += 1
    card['_pos_' + split] = pos
    return stats


def _emit(card, em, split, rec, rb, wds, pos, suf, masked, twin_of=None, variant=None):
    names = None if masked else rb["names"]
    Kk = rb["K"]
    opts = [level_text(k, names) for k in range(1, Kk + 1)]
    g = level_A(rb, rec)
    qid, qtext, _ = T.questions("score")[int(C.h01("sq", card["card_id"], rec["rid"]) * 3)]
    bid = f"COMMIT-{split}-{card['card_id']}-{pos:03d}"
    sp = {"id": bid + suf, "type": "score", "card": card, "rec": rec, "view": "message_diff", "form": "choice",
          "qtype": "choice", "question": qtext, "qid": qid, "k": 0,
          "wording": wds[int(C.h01("wd", card["card_id"], rec["rid"]) * len(wds))],
          "card_ir": card_ir(rb, names, card["defs_style"]), "options": opts, "gold": opts[g - 1], "msg": rec["msg"],
          "build_extra": lambda b: extra(rec, rb, b), "depth": len(rubric_classes(rb)) + 1,
          "option_level": {o: i for i, o in enumerate(opts)}, "twin_of": twin_of,
          "twin_kind": "cut" if twin_of else None, "call_id": bid + suf + "-u", "variant": variant,
          "edge": [f"tpl:{rb['tpl']}", f"K:{Kk}", "masked" if masked else "named"],
          "card_form": "normal", "sidecar": {"level": g}}
    return em.emit(sp)
