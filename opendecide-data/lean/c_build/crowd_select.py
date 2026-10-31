"""G9 crowd difficulty + spec 2.1 stratified selection for C round 1 (C_DATA_SPEC.md v4 2.1, 8 G9; PREREG A16, A17).

Crowd (A17): C1 = q35_4b_main500k, 4B-E = q35_4b_pxE, base Qwen3.5-4B (C1's adapter with every lora_B = 0, the A18.2
form, so the base runs through the exact same prompt and readout). Each scores every candidate row once (1 view per
read, given option order, no TTA) on a Modal H100 (A17 replaces decision 3's free L4 for round 1). Crowd p_g = mean of
the three models' probability on the gold answer. No model above 4B.

Bins: easy p_g > 0.97; medium 0.30 < p_g <= 0.97; hard p_g <= 0.30. Selection (representative, no LESS / influence /
IFD / targeting, addendum D1): keep all medium + hard units and a seeded 30% of all-easy units; bin budgets easy <= 25%,
hard <= 30%, medium the rest (>= 45%); inside each bin, label-balanced quotas per stratum (yes/no: wording x bin, gold
yes = no; choice: option-count bucket x bin, gold position class uniform), filled in a seeded random unit order (whole
relation units); a bin whose balanced pool falls short reflows the gap into bins with spare balanced rows (medium
first, caps kept; A27 c). Checks: label x bin chi-square p > 0.01; rows with crowd p_g < 0.05 go to a G5 re-read list (all ids
+ a seeded 300 of the selected rows outside that list, A27 c). Commits (spec 4.2): one selection per type x input_view with its own sub-target
(1,200 per type; 360 message-only of route, triage and gate). Relation files come from each family MANIFEST (any of
candidates_r1.relations.jsonl, candidates_r1.rel.jsonl, relations_candidates_r1.jsonl) and must match its declared
count and sha256, else the family is refused.

  ../.venv/bin/python c_build/crowd_select.py tasks [--write-shards]   task lists + Modal commands (no Modal call here)
  ../.venv/bin/python c_build/crowd_select.py select [--fam F1 ...]     after the reads: selection files per family
  ../.venv/bin/python c_build/crowd_select.py make-base0 --src ADAPTER --out DIR   zero-B adapter (A18.2 form)
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mixio import (A15_SUITE_SHA, DATA, HERE, LEAN, PY, InputLog, h64, log_line,  # noqa: E402
                   sha256_file, write_json)

SEED = 20261003
FAMS = [f"F{i}" for i in range(1, 14)]
TARGET_R1 = {"F1": 5400, "F2": 3150, "F3": 4500, "F4": 3600, "F5": 3600, "F6": 3600, "F7": 3150, "F8": 2250,
             "F9": 4050, "F10": 3600, "F11": 3600, "F12": 2700, "F13": 2050, "COMMIT": 6000}   # spec 0, 2.2, 4.2
CROWD = {   # key -> (adapter name on the Volume, note)
    "c1": ("q35_4b_main500k", "C1 (REF)"),
    "e4b": ("q35_4b_pxE", "4B-E"),
    "base": ("q35_4b_base0", "base Qwen3.5-4B: C1 adapter with every lora_B = 0 (A18.2 form)"),
}
BASE, REVISION, LAYOUT = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "schema_branch_mark"
EASY, HARD = 0.97, 0.30            # easy: p_g > 0.97; hard: p_g <= 0.30
EASY_KEEP = 0.30
CAP = {"easy": 0.25, "hard": 0.30}
MED_MIN = 0.45
G5_PG, G5_N = 0.05, 300
CHI_P = 0.01
REFLOW_ORDER, REFLOW_ROUNDS = ("medium", "hard", "easy"), 64   # A27 c: shortfall receivers, in order; round bound
CROWD_DIR = DATA / "c_crowd_r1_shards"
OUT = HERE / "crowd_r1"
LOG = HERE / "progress_mixer.log"


def log(msg):
    log_line(LOG, "crowd_select: " + msg)
    print(msg, flush=True)


# ------------------------------------------------------------------ family inputs

def fam_dir(fam):
    return LEAN / "c_src" / fam


REL_NAMES = ("candidates_r1.relations.jsonl", "candidates_r1.rel.jsonl", "relations_candidates_r1.jsonl")
_NOT_DECL = re.compile(r"sealed|check|gate|qc|report|previous|archive|history", re.I)   # records about a file, not of it


def rel_decl(man: dict) -> dict:
    """What a family MANIFEST declares about its candidates_r1 relation file, in any of the builders' layouts:
    {"names": {file names}, "n": {row counts}, "sha256": {shas}}. Forms read: a files/outputs entry keyed by the file
    name ({sha256, rows|lines|n}); a {path|file: <name>, sha256, rows|lines|n} record; a candidates_r1 record with
    'relations' (int) and 'relations_sha256' (F8)."""
    out = {"names": set(), "n": set(), "sha256": set()}

    def take(name, d):
        if name:
            out["names"].add(name)
        n = next((d[k] for k in ("rows", "lines", "n") if isinstance(d.get(k), int)), None)
        if n is not None:
            out["n"].add(n)
        if isinstance(d.get("sha256"), str):
            out["sha256"].add(d["sha256"])

    def visit(x, key=""):
        if isinstance(x, list):
            for v in x:
                visit(v, key)
            return
        if not isinstance(x, dict):
            return
        base = Path(str(key)).name
        if base in REL_NAMES:
            take(base, x)
        for k in ("path", "file"):
            if isinstance(x.get(k), str) and Path(x[k]).name in REL_NAMES:
                take(Path(x[k]).name, x)
        if base in ("candidates_r1", "candidates_r1.jsonl"):
            if isinstance(x.get("relations"), int):
                out["n"].add(x["relations"])
            if isinstance(x.get("relations_sha256"), str):
                out["sha256"].add(x["relations_sha256"])
        for k, v in x.items():
            if not _NOT_DECL.search(str(k)):
                visit(v, k)
    visit(man)
    return out


def fam_files(fam) -> dict:
    out = fam_dir(fam) / "out"
    man = out / "MANIFEST.json"
    names = []
    if man.exists():
        names = sorted(rel_decl(InputLog().json(man))["names"])
    rel = next((out / n for n in names + list(REL_NAMES) if (out / n).exists()), None)
    return {"cand": out / "candidates_r1.jsonl", "rel": rel, "manifest": man,
            "qc": fam_dir(fam) / "qc" / "QC_REPORT.json"}


def available(fams=None) -> list[str]:
    return [f for f in (fams or FAMS + ["COMMIT"]) if fam_files(f)["cand"].exists()]


def relation_problems(fam, man: dict, rel_path, rels) -> list[str]:
    """Refusals: the manifest declares relations (> 0 rows, or a sha256) and the loaded file is missing, or its row
    count or sha256 differs; the manifest's records disagree; or it names a file that is not on disk."""
    d = rel_decl(man)
    p = []
    if len(d["n"]) > 1 or len(d["sha256"]) > 1:
        p.append(f"{fam}: MANIFEST relation records disagree (n {sorted(d['n'])}, sha {len(d['sha256'])} values)")
    for nm in d["names"]:
        if not (fam_dir(fam) / "out" / nm).exists():
            p.append(f"{fam}: MANIFEST names relation file {nm}, not on disk")
    declared = any(n > 0 for n in d["n"]) or bool(d["sha256"])
    if declared and rel_path is None:
        p.append(f"{fam}: MANIFEST declares relations {sorted(d['n'])} but no relation file was found")
    if rel_path is not None:
        if d["n"] and len(rels) not in d["n"]:
            p.append(f"{fam}: {rel_path.name} has {len(rels)} relations, MANIFEST declares {sorted(d['n'])}")
        if d["sha256"] and sha256_file(rel_path) not in d["sha256"]:
            p.append(f"{fam}: {rel_path.name} sha256 differs from the MANIFEST's")
    return p


def load_family(ilog: InputLog, fam):
    """Candidates + relations. Refuses (SystemExit, every mode) when the relation file does not match the MANIFEST."""
    f = fam_files(fam)
    rows = ilog.jsonl(f["cand"])
    rels = ilog.jsonl(f["rel"]) if f["rel"] else []
    man = ilog.json(f["manifest"]) if f["manifest"].exists() else {}
    bad = relation_problems(fam, man, f["rel"], rels)
    if bad:
        raise SystemExit("relation file refused: " + "; ".join(bad))
    return rows, rels


def fallback_rows(ilog: InputLog) -> dict:
    """Spec-stated fallbacks recorded by the public builders (3.2: a set that fails G1 / licence sends its rows to the
    named own family), e.g. public-1 counts.f13_fallback_rows_r1 (Qasper NC/ND papers -> F13). {family: rows}."""
    import re
    out = Counter()
    for m in sorted((LEAN / "c_src/public").glob("public-*/**/manifest*.json")):
        if "tmp" in m.parts:
            continue
        c = (ilog.json(m) or {}).get("counts") or {}
        for k, v in c.items():
            mm = re.fullmatch(r"(f\d+)_fallback_rows_r1", k)
            if mm and isinstance(v, int):
                out[mm.group(1).upper()] += v
    return dict(out)


def family_targets(ilog: InputLog) -> dict:
    fb = fallback_rows(ilog)
    return {f: t + fb.get(f, 0) for f, t in TARGET_R1.items()}


# ------------------------------------------------------------------ units, strata, crowd p_g

def units_of(rows, rels) -> list[list[int]]:
    """Relation units: rows grouped by call_id, then joined by every relation edge (union-find), in first-row order."""
    idx = {r["id"]: i for i, r in enumerate(rows)}
    parent = list(range(len(rows)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    first = {}
    for i, r in enumerate(rows):
        c = r.get("call_id") or r["id"]
        if c in first:
            parent[find(i)] = find(first[c])
        else:
            first[c] = i
    for x in rels:
        if x.get("a") in idx and x.get("b") in idx:
            ra, rb = find(idx[x["a"]]), find(idx[x["b"]])
            if ra != rb:
                parent[ra] = rb
    comp = defaultdict(list)
    for i in range(len(rows)):
        comp[find(i)].append(i)
    return sorted(comp.values(), key=lambda u: u[0])


def opt_bucket(k: int) -> str:
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def label_class(r):
    """yes/no: gold 0/1. Ordinal rows (meta.option_level): the gold level. Other choice rows: gold position when
    k <= 4; one class for k >= 5 (positions are uniform from the builders and the order is random)."""
    if r["qtype"] == "noul":
        return int(r["gold"])
    ol = (r.get("meta") or {}).get("option_level")
    if isinstance(ol, dict) and r.get("gold") in ol:
        return int(ol[r["gold"]])
    o = r.get("options") or []
    return o.index(r["gold"]) if len(o) <= 4 and r.get("gold") in o else 0


_NEG: dict = {}


def neg_count(text: str) -> int:
    if text not in _NEG:
        sys.path.insert(0, str(LEAN / "c_src/common"))
        import negcount
        _NEG[text] = negcount.k_all(text)
    return _NEG[text]


COMMIT_TYPES = ("route", "triage", "score", "gate", "match")
COMMIT_MSG_ONLY = ("route", "triage", "gate")      # spec 4.2: 30% message-only of these three types
COMMIT_MSG_SHARE = 0.30


def commit_group(r) -> str:
    """Commit rows (top-level source 'commit_<type>'): '<type>|<input_view>'; '' for every other row."""
    s = str(r.get("source") or "")
    if not s.startswith("commit_"):
        return ""
    return f"{s[len('commit_'):]}|{(r.get('meta') or {}).get('input_view')}"


def commit_subtargets(target: int) -> dict:
    """Spec 4.2: equal type shares (r1 1,200 each of 6,000); message-only = 30% of route, triage and gate (360 each)."""
    per = target // len(COMMIT_TYPES)
    out = {}
    for t in COMMIT_TYPES:
        mo = round(COMMIT_MSG_SHARE * per) if t in COMMIT_MSG_ONLY else 0
        out[f"{t}|message_diff"] = per - mo
        if mo:
            out[f"{t}|message_only"] = mo
    return out


def stratum(r, b):
    """yes/no: wording x negation count x bin; ordinal: sampler x K x bin (level balance, G10 A2); choice: k (2-4) or
    bucket x bin. Commit rows: the same, prefixed by commit type x input_view (spec 4.2 counts)."""
    m = r.get("meta") or {}
    g = commit_group(r)
    pre = f"{g}|" if g else ""
    if r["qtype"] == "noul":    # G10 cell: family x wording x bin x negation count (negcount.k_all, A16.1 v1.1)
        return ("yn", f"{pre}{m.get('wording_id')}|k{neg_count(r.get('instructions') or '')}", b)
    ol = m.get("option_level")
    if isinstance(ol, dict) and ol:
        return ("ord", f"{pre}{m.get('sampler')}|{len(ol)}", b)
    k = len(r.get("options") or [])
    return ("ch", f"{pre}{k if k <= 4 else opt_bucket(k)}", b)


def n_classes(s) -> int:
    if s[0] == "yn":
        return 2
    if s[0] == "ord":
        return int(s[1].rsplit("|", 1)[1])
    last = s[1].rsplit("|", 1)[-1]           # commit strata carry a '<type>|<view>|' prefix
    return int(last) if last.isdigit() else 1


def p_gold(r, probs) -> float:
    if r["qtype"] == "noul":
        return float(probs.get("yes" if int(r["gold"]) == 1 else "no", 0.0))
    return float(probs.get(r["gold"], 0.0))


def bin_of(pg) -> str:
    if pg is None:
        return "na"
    return "easy" if pg > EASY else ("medium" if pg > HARD else "hard")


def load_crowd(ilog: InputLog, rows, label_dirs: dict, shards_dir=None) -> dict:
    """{row id: crowd p_g} = mean of the three models' p_g. label_dirs: {crowd key: labels dir or .jsonl}. Every row
    must be scored by every model (else SystemExit: the crowd read is incomplete)."""
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    per = {}
    for key in CROWD:
        p = Path(label_dirs[key])
        for f in ([p] if p.is_file() else sorted(p.glob("shard_*.jsonl")) + sorted(p.glob("shard_*.meta.json"))):
            ilog.record(f)
        per[key] = sg.load_labels(p, shards_dir) if not p.is_file() else sg.load_labels(p)
    out, missing = {}, Counter()
    for r in rows:
        vals = []
        for key in CROWD:
            pr = per[key].get(r["id"])
            if pr is None:
                missing[key] += 1
                continue
            vals.append(p_gold(r, pr))
        if len(vals) == len(CROWD):
            out[r["id"]] = sum(vals) / len(vals)
    if missing:
        raise SystemExit(f"crowd read incomplete: rows without labels per model {dict(missing)}")
    return out


def crowd_complete(fam) -> list[str]:
    """Problems with a family's crowd score files (every shard labelled by every crowd model); [] = complete."""
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    sd = CROWD_DIR / fam
    shards = sg.shard_files(sd) if (sd / sg.MANIFEST).exists() else []
    if not shards:
        return [f"{fam}: no crowd shards in {sd.relative_to(LEAN)}"]
    out = []
    for name, _ in CROWD.values():
        ld = sd / f"labels_{name}"
        if not all(sg.shard_done(sp, *sg.label_paths(ld, sp)) for sp in shards):
            out.append(f"{fam}: crowd labels of {name} incomplete")
    return out


# ------------------------------------------------------------------ selection (spec 2.1)

def _budgets(avail: Counter, target: int, crowd: bool) -> dict:
    if not crowd:
        return {"na": min(target, avail["na"])}
    b_e = min(avail["easy"], int(CAP["easy"] * target))
    b_h = min(avail["hard"], int(CAP["hard"] * target))
    return {"easy": b_e, "medium": min(avail["medium"], target - b_e - b_h), "hard": b_h}


def easy_thinned(rows, units, bins: dict, key: str, seed: int = SEED) -> set:
    """All-easy units outside the seeded 30% keep (spec 2.1): never selected, never used as a refill."""
    out = set()
    for u, x in enumerate(units):
        if all(bins.get(rows[i]["id"]) == "easy" for i in x) and \
                h64(seed, key, "easy", rows[x[0]]["id"]) % 10 ** 6 >= EASY_KEEP * 10 ** 6:
            out.add(u)
    return out


def select(rows, units, pg: dict | None, target: int, key: str = "", seed: int = SEED) -> dict:
    """Stratified, label-balanced, representative selection of whole units to `target` rows. pg None = provisional
    (no crowd yet: one bin 'na'; used by the mixer's --dry-run only). Returns sel (unit indices), bins, report."""
    crowd = pg is not None
    bins = {r["id"]: (bin_of(pg.get(r["id"])) if crowd else "na") for r in rows}
    uid = [rows[u[0]]["id"] for u in units]
    order = sorted(range(len(units)), key=lambda u: h64(seed, key, "order", uid[u]))
    easy_drop = easy_thinned(rows, units, bins, key, seed) if crowd else set()
    elig = [u for u in order if u not in easy_drop]
    info = {}
    for u in elig:
        for i in units[u]:
            r = rows[i]
            b = bins[r["id"]]
            info[i] = (b, stratum(r, b), label_class(r))
    avail = Counter(v[0] for v in info.values())
    budget = _budgets(avail, target, crowd)
    n = defaultdict(Counter)
    for b, s, c in info.values():
        n[s][c] += 1
    quota = {}
    for b, B in budget.items():
        ss = [s for s in n if s[2] == b]
        bal = {s: min(n[s][c] for c in range(n_classes(s))) for s in ss}
        tot = sum(bal[s] * n_classes(s) for s in ss)
        f = min(1.0, B / tot) if tot else 0.0
        for s in ss:
            quota[s] = math.floor(bal[s] * f)      # floor: the quotas never sum above the bin budget
    cnt, used, pool = defaultdict(Counter), Counter(), defaultdict(Counter)
    sel, taken, out = [], set(), set()
    cache = {}

    def add_of(u):
        if u not in cache:
            a, ab = defaultdict(Counter), Counter()
            for i in units[u]:
                b, s, c = info[i]
                a[s][c] += 1
                ab[b] += 1
            cache[u] = (a, ab)
        return cache[u]

    def pkey(s):
        return (s[0], s[1] if s[0] != "yn" else "", s[2])

    def imbalance(c: Counter, k: int) -> int:
        return max(c[j] for j in range(k)) - min(c[j] for j in range(k))

    def tol(s, c) -> float:
        return 1 if s[0] == "ord" else max(2, 0.02 * sum(c.values()))

    def move(u, sign):
        a, ab = add_of(u)
        for s, c in a.items():
            for cl, k in c.items():
                cnt[s][cl] += sign * k
                pool[pkey(s)][cl] += sign * k
        for b, k in ab.items():
            used[b] += sign * k
        if sign > 0:
            sel.append(u)
            taken.add(u)
        else:
            sel.remove(u)
            out.add(u)

    def fill(strict, slack=0):   # strict: per-stratum quotas (+ slack, and only units that feed a class below its
        for u in elig:           # quota when slack > 0); else fill without worsening pooled or ordinal balance
            if u in taken or u in out:
                continue
            a, ab = add_of(u)
            if any(used[b] + k > budget.get(b, 0) for b, k in ab.items()):
                continue
            if strict and any(cnt[s][c] + k > quota.get(s, 0) + slack for s, cc in a.items() for c, k in cc.items()):
                continue
            if strict and slack and not any(cnt[s][c] < quota.get(s, 0) for s, cc in a.items() for c in cc):
                continue
            if not strict:
                ok = True
                for s, cc in a.items():
                    for key, cur in ((pkey(s), pool[pkey(s)]), (s, cnt[s])) if s[0] == "ord" else ((pkey(s), pool[pkey(s)]),):
                        k = n_classes(s)
                        old, new = imbalance(cur, k), imbalance(cur + cc, k)
                        if new > old and new > tol(s, cur + cc):
                            ok = False
                if not ok:
                    continue
            move(u, +1)

    def rebalance():     # drop units that only feed over-filled classes of an unbalanced stratum
        n = 0
        for s in list(cnt):
            k = n_classes(s)
            if k < 2:
                continue
            for _ in range(10 ** 4):
                c = cnt[s]
                if imbalance(c, k) <= tol(s, c):
                    break
                lo = min(c[j] for j in range(k))
                hi = {j for j in range(k) if c[j] > lo + tol(s, c) - 1}
                u = next((u for u in reversed(sel) if s in add_of(u)[0] and set(add_of(u)[0][s]) <= hi), None)
                if u is None:
                    break
                move(u, -1)
                n += 1
        return n

    def run():
        fill(True)
        fill(True, slack=1)
        for _ in range(3):
            fill(False)
            if not rebalance():
                break
        fill(False)
        if crowd:                           # caps hold on the rows actually selected (a short total raises shares)
            for b in ("hard", "easy"):
                for u in reversed(list(sel)):
                    tot = sum(used.values())
                    if used[b] <= CAP[b] * tot + 1e-9:
                        break
                    bs = Counter(info[i][0] for i in units[u])
                    if bs[b] and not bs["medium"]:
                        move(u, -1)

    run()
    budget0, reflow = dict(budget), []
    if crowd and sum(used.values()) < target:
        # Reflow (PREREG A27 c): the bin budgets were fixed before the cell-balanced downsampling, so a bin whose
        # balanced pool is short left the total short. Freeze every bin at what it holds and grant the shortfall to
        # one receiver at a time (medium = "the rest" first, then hard and easy up to their caps), raise that bin's
        # per-stratum quotas with the same proportional floor rule (never lowered), and re-run the same seeded fill,
        # rebalance and cap passes. A round that gains no rows is undone (never fewer rows than before it) and its
        # receiver is exhausted. Runs only when short, so a selection that already meets its target is unchanged.
        def snapshot():
            return (list(sel), set(taken), set(out), {s: Counter(c) for s, c in cnt.items()}, Counter(used),
                    {s: Counter(c) for s, c in pool.items()}, dict(budget), dict(quota))

        def restore(st):
            for obj, val in zip((sel, taken, out, cnt, used, pool, budget, quota), st):
                obj.clear()
                obj.extend(val) if isinstance(obj, list) else obj.update(val)

        live = [b for b in REFLOW_ORDER if b in budget]
        for _ in range(REFLOW_ROUNDS):
            tot0 = sum(used.values())
            short = target - tot0
            if short <= 0 or not live:
                break
            b = live[0]
            room = (avail[b] if b == "medium" else min(avail[b], int(CAP[b] * target))) - used[b]
            if room <= 0:
                live.pop(0)
                continue
            grant = min(short, room)
            st = snapshot()
            for x in budget:
                budget[x] = used[x]
            budget[b] = used[b] + grant
            ss = [s for s in n if s[2] == b]
            bal = {s: min(n[s][c] for c in range(n_classes(s))) for s in ss}
            tot = sum(bal[s] * n_classes(s) for s in ss)
            f = min(1.0, budget[b] / tot) if tot else 0.0
            for s in ss:
                quota[s] = max(quota.get(s, 0), math.floor(bal[s] * f))
            run()
            gained = sum(used.values()) - tot0
            reflow.append({"bin": b, "grant": grant, "gained": gained, "kept": gained > 0})
            if gained <= 0:
                restore(st)
                live.pop(0)
    rep = selection_report(rows, units, sorted(sel), bins, target, crowd, pg)
    if crowd:
        rep["reflow"] = {"rounds": reflow, "budget_after": dict(budget)}
    return {"sel": sorted(sel), "bins": bins, "easy_dropped_units": len(easy_drop), "budget": budget0,
            "reflow": reflow, "report": rep}


def select_commit(rows, units, pg: dict | None, target: int, key: str = "COMMIT", seed: int = SEED) -> dict:
    """Commit selection (spec 4.2): one stratified selection per type x input_view with its own sub-target (1,200 per
    type; 360 message-only of route, triage and gate), so difficulty thinning cannot move the type or view counts.
    A unit whose rows span two groups is never selected (reported)."""
    subt = commit_subtargets(target)
    by = defaultdict(list)
    span = 0
    for u, x in enumerate(units):
        gs = {commit_group(rows[i]) for i in x}
        if len(gs) > 1:
            span += 1
            continue
        by[gs.pop()].append(u)
    sel, bins, budget, easy, sub = [], {}, {}, 0, {}
    for g in sorted(set(subt) | set(by)):
        us = by.get(g, [])
        sub_units = [units[u] for u in us]
        res = select(rows, sub_units, pg, subt.get(g, 0), key=f"{key}|{g}", seed=seed)
        sel += [us[j] for j in res["sel"]]
        bins |= res["bins"]
        budget[g] = res["budget"]
        easy += res["easy_dropped_units"]
        sub[g] = res["report"] | {"subtarget": subt.get(g, 0)}
    bins = {r["id"]: bins.get(r["id"], bin_of(pg.get(r["id"])) if pg is not None else "na") for r in rows}
    rep = selection_report(rows, units, sorted(sel), bins, target, pg is not None, pg)
    got = Counter(commit_group(rows[i]) for u in sel for i in units[u])
    rep["commit_groups"] = {g: [got.get(g, 0), subt.get(g, 0)] for g in sorted(set(subt) | set(got))}
    rep["units_spanning_groups"] = span
    rep["by_group"] = sub
    rep["checks"]["commit_4.2_counts"] = all(got.get(g, 0) == n for g, n in subt.items()) and set(got) <= set(subt)
    rep["checks"]["groups_pass"] = all(v["pass"] for v in sub.values())
    rep["pass"] = all(rep["checks"].values())
    return {"sel": sorted(sel), "bins": bins, "easy_dropped_units": easy, "budget": budget, "report": rep}


def select_any(rows, units, pg, target, key, seed: int = SEED) -> dict:
    return (select_commit if key == "COMMIT" else select)(rows, units, pg, target, key=key, seed=seed)


def chi2_p(table) -> float | None:
    """Contingency chi-square p (rows = bins, cols = label classes); None when fewer than 2 non-empty rows/cols."""
    from scipy.stats import chi2_contingency
    t = [r for r in table if sum(r) > 0]
    if len(t) < 2:
        return None
    cols = [j for j in range(len(t[0])) if sum(r[j] for r in t) > 0]
    if len(cols) < 2:
        return None
    return float(chi2_contingency([[r[j] for j in cols] for r in t])[1])


def selection_report(rows, units, sel, bins, target, crowd, pg) -> dict:
    ids = [i for u in sel for i in units[u]]
    nb = Counter(bins[rows[i]["id"]] for i in ids)
    tot = max(1, len(ids))
    share = {b: round(v / tot, 4) for b, v in nb.items()}
    yn, ch = defaultdict(Counter), defaultdict(lambda: defaultdict(Counter))
    for i in ids:
        r = rows[i]
        b = bins[r["id"]]
        if r["qtype"] == "noul":
            yn[b][int(r["gold"])] += 1
        else:
            s = stratum(r, b)
            ch[(s[0], s[1])][b][label_class(r)] += 1
    blist = sorted(nb)
    p_yn = chi2_p([[yn[b][0], yn[b][1]] for b in blist])
    p_ch = {"|".join(k): chi2_p([[d[b][j] for j in range(n_classes((*k, b)))] for b in blist]) for k, d in ch.items()}
    ps = [p for p in [p_yn, *p_ch.values()] if p is not None]
    rep = {"rows": len(ids), "target": target, "units": len(sel), "crowd": crowd, "bins": dict(nb), "shares": share,
           "yes_rate_by_bin": {b: round(v[1] / max(1, v[0] + v[1]), 4) for b, v in yn.items()},
           "chi2_label_x_bin": {"yes_no": p_yn, "choice_by_k": p_ch}, "short_by": max(0, target - len(ids))}
    checks = {"total_eq_target": len(ids) == target, "chi2_p_gt_0.01": all(p > CHI_P for p in ps)}
    if crowd:
        checks.update({"easy_le_25": share.get("easy", 0) <= CAP["easy"] + 1e-9,
                       "hard_le_30": share.get("hard", 0) <= CAP["hard"] + 1e-9,
                       "medium_ge_45": share.get("medium", 0) >= MED_MIN - 1e-9})
        low = [r["id"] for r in rows if pg.get(r["id"], 1.0) < G5_PG]
        rep["g5_reread_candidates"] = len(low)
    rep["checks"] = checks
    rep["pass"] = all(checks.values())
    return rep


def g5_reread(rows, units, sel, pg, fam) -> dict:
    """Every row with crowd p_g < 0.05 (all candidates) + a seeded sample of 300 (selected rows first)."""
    chosen = [rows[i]["id"] for u in sel for i in units[u]]
    low = sorted((r["id"] for r in rows if pg.get(r["id"], 1.0) < G5_PG), key=lambda x: h64(SEED, fam, "g5", x))
    lows = set(low)        # A27 c: all low rows PLUS a seeded 300 of the selected rows outside the low set
    sample = sorted((x for x in dict.fromkeys(chosen) if x not in lows), key=lambda x: h64(SEED, fam, "g5", x))[:G5_N]
    return {"family": fam, "rule": "crowd p_g < 0.05 (spec G9) + a seeded 300 of the selected rows (A27 c); "
            "flag-only G5 re-read; any confirmed error = generator bug",
            "n_low": len(low), "low_ids": low, "n_sample": len(sample), "sample_ids": sorted(sample),
            "reread_ids": sorted(lows | set(sample)), "n_reread": len(lows) + len(sample)}


# ------------------------------------------------------------------ CLI: select

def cmd_select(a):
    ilog = InputLog()
    targets = family_targets(ilog)
    drop_ids = set()
    for p in a.exclude_ids or []:
        drop_ids.update(ilog.json(LEAN / p).get("drop_ids") or [])
    for fam in available(a.fam):
        rows, rels = load_family(ilog, fam)
        units = units_of(rows, rels)
        excl = None
        if a.exclude_ids:    # A34 (b): units holding any G13-dropped id leave the pool before selection
            bad = {i for u in units if any(rows[i]["id"] in drop_ids for i in u) for i in u}
            n_u = sum(1 for u in units if bad.intersection(u))
            rows = [r for i, r in enumerate(rows) if i not in bad]
            units = units_of(rows, rels)
            excl = {"files": [str(p) for p in a.exclude_ids], "units_removed": n_u, "rows_removed": len(bad),
                    "pool_rows_after": len(rows)}
            log(f"select {fam}: --exclude-ids removed {n_u} units / {len(bad)} rows; pool now {len(rows)} rows")
        sd = CROWD_DIR / fam
        pg = load_crowd(ilog, rows, {k: sd / f"labels_{CROWD[k][0]}" for k in CROWD}, sd)
        res = select_any(rows, units, pg, targets[fam], key=fam)
        g5 = g5_reread(rows, units, res["sel"], pg, fam)
        ids = [rows[i]["id"] for u in res["sel"] for i in units[u]]
        sha = write_json(OUT / f"select_{fam}.json", {
            "family": fam, "target": targets[fam], "seed": SEED, "crowd": {k: v[0] for k, v in CROWD.items()},
            "candidates_sha256": sha256_file(fam_files(fam)["cand"]), "report": res["report"],
            "budget": res["budget"], "easy_dropped_units": res["easy_dropped_units"], "reflow": res.get("reflow", []),
            "selected_ids": ids, **({"exclude_ids": excl} if excl else {}),
            "crowd_pg": {r["id"]: round(pg[r["id"]], 4) for r in rows},
            "difficulty_bin": {r["id"]: res["bins"][r["id"]] for r in rows}})
        write_json(OUT / f"g5_reread_{fam}.json", g5)
        log(f"select {fam}: {res['report']['rows']} rows (target {targets[fam]}), bins {res['report']['bins']}, "
            f"pass {res['report']['pass']}, G5 low-p_g rows {g5['n_low']} + sample {g5['n_sample']}; sha {sha[:12]}")
    write_json(OUT / "select_inputs.json", {"inputs": ilog.entries})


# ------------------------------------------------------------------ CLI: tasks (shards + Modal commands; no Modal call)

L4_READS_PER_S, H100_SPEEDUP, H100_USD_PER_H = 3.47, 3.0, 3.95   # L4 audit rate (RUNBOOK 2); H100 factor assumed


def cmd_tasks(a):
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    ilog = InputLog()
    targets = family_targets(ilog)
    fams = available(a.fam)
    tasks = {"purpose": "C round-1 G9 crowd read (A17: Modal H100, 1 view per read: given order, no TTA)",
             "sealed_suite_sha256_A15": A15_SUITE_SHA, "base": BASE, "revision": REVISION, "layout": LAYOUT,
             "models": {k: {"adapter": v[0], "note": v[1]} for k, v in CROWD.items()}, "families": {}}
    reads = 0
    for fam in fams:
        f = fam_files(fam)
        rows, _ = load_family(ilog, fam)
        bad = [r["id"] for r in rows if (r.get("meta") or {}).get("sampler") == "S5"]
        if bad:
            raise SystemExit(f"{fam}: {len(bad)} S5 (held-out sampler) rows in candidates_r1: refused")
        dup = sum(1 for r in rows if r["qtype"] == "choice" and len(set(map(str, r["options"]))) != len(r["options"]))
        sd = CROWD_DIR / fam
        man = None
        if a.write_shards:
            man = sg.write_shards(rows, sd, 5000, {"purpose": f"C r1 crowd read {fam}", "seed": SEED,
                                                    "candidates_sha256": sha256_file(f["cand"])})
        n_sh = len(sg.split_even(len(rows), 5000))
        tasks["families"][fam] = {"candidates": str(f["cand"].relative_to(LEAN)), "candidates_sha256":
                                  sha256_file(f["cand"]), "rows": len(rows), "target_r1": targets.get(fam),
                                  "repeated_option_rows": dup, "shards_dir": str(sd.relative_to(LEAN)),
                                  "shards": n_sh, "shards_written": man is not None,
                                  "manifest_sha256": sha256_file(sd / sg.MANIFEST) if man else None}
        reads += len(rows) * len(CROWD)
    h = reads / L4_READS_PER_S / 3600 / H100_SPEEDUP
    tasks["estimate"] = {"reads": reads, "h100_hours": round(h, 2), "usd": round(h * H100_USD_PER_H, 1),
                         "basis": f"L4 {L4_READS_PER_S} reads/s x assumed H100 speed-up {H100_SPEEDUP}; "
                                  f"${H100_USD_PER_H}/h; one container per model (+ ~2 min load each)"}
    OUT.mkdir(parents=True, exist_ok=True)
    write_json(OUT / "crowd_tasks_r1.json", tasks)
    (OUT / "CROWD_READ_r1.sh").write_text(commands(fams))
    log(f"tasks: {len(fams)} families {fams}, {reads:,} reads, est {h:.1f} H100 h (~${h * H100_USD_PER_H:.0f}); "
        f"shards {'written' if a.write_shards else 'NOT written (pass --write-shards)'}")


def commands(fams) -> str:
    fl = ",".join(fams)
    lines = ["#!/bin/bash", "# C round-1 G9 crowd read (A17: Modal H100, owner GO ~$15). Written by crowd_select.py tasks;",
             "# NOT run by any agent. Paid step: run only after the owner's GO. From lean/:", "set -euo pipefail",
             "cd \"$(dirname \"$0\")/../..\"   # lean/", f"PY={PY}", "",
             "# 0. shards (CPU; refuses to overwrite a different set while a read runs)",
             f"$PY c_build/crowd_select.py tasks --write-shards --fam {' '.join(fams)}", "",
             "# 1. base adapter for the crowd's base-4B member (A18.2 form: C1 adapter, every lora_B = 0)",
             "$PY c_build/crowd_select.py make-base0 --src ../../backups/modal_models/q35_4b_main500k "
             "--out models/q35_4b_base0", "",
             "# 2. upload shards + adapters to the Modal Volume 'opendecide' (skip an adapter already there)",
             "for f in " + " ".join(fams) + "; do modal volume put -f opendecide data/c_crowd_r1_shards/$f "
             "crowd_r1_shards/$f; done",
             "modal volume put opendecide models/q35_4b_base0 models/q35_4b_base0 || true",
             "modal volume ls opendecide models | grep -E 'q35_4b_main500k|q35_4b_pxE|q35_4b_base0'", "",
             "# 3. reads: one H100 container per model, every family, 1 view per read (given order, no TTA)"]
    for k, (name, note) in CROWD.items():
        lines.append(f"modal run --detach c_build/modal_crowd.py::crowd --name {name} --fams {fl}   # {note}")
    lines += ["", "# 4. fetch labels, then select (CPU)",
              "for f in " + " ".join(fams) + "; do for m in " + " ".join(v[0] for v in CROWD.values()) +
              "; do modal volume get opendecide crowd_r1_shards/$f/labels_$m data/c_crowd_r1_shards/$f/; done; done",
              f"$PY c_build/crowd_select.py select --fam {' '.join(fams)}", ""]
    return "\n".join(lines)


# ------------------------------------------------------------------ CLI: make-base0 (A18.2 form)

def cmd_make_base0(a):
    """Copy an adapter folder and set every lora_B tensor to 0: the model is then exactly the base weights, read with
    C1's prompt, layout and style metadata (A18.2). Local CPU only."""
    import shutil
    import torch
    from safetensors.torch import load_file, save_file
    src, out = Path(a.src), Path(a.out)
    if out.exists():
        raise SystemExit(f"{out} exists")
    shutil.copytree(src, out)
    n = 0
    for f in out.glob("*.safetensors"):
        sd = load_file(str(f))
        for k in sd:
            if ".lora_B." in k:
                sd[k] = torch.zeros_like(sd[k])
                n += 1
        save_file(sd, str(f), metadata={"format": "pt"})
    if not n:
        raise SystemExit("no lora_B tensors found")
    write_json(out / "base0.json", {"from": str(src), "lora_B_zeroed": n, "rule": "PREREG A18.2 form (base = C1 adapter "
                                    "with every lora_B = 0)"})
    log(f"make-base0: {n} lora_B tensors zeroed -> {out}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tasks")
    t.add_argument("--fam", nargs="*", default=None)
    t.add_argument("--write-shards", dest="write_shards", action="store_true")
    s = sub.add_parser("select")
    s.add_argument("--fam", nargs="*", default=None)
    s.add_argument("--exclude-ids", dest="exclude_ids", nargs="+", default=None,
                   help="G13 decontam logs (key drop_ids); units holding a listed id are removed before selection")
    b = sub.add_parser("make-base0")
    b.add_argument("--src", required=True)
    b.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    {"tasks": cmd_tasks, "select": cmd_select, "make-base0": cmd_make_base0}[a.cmd](a)


if __name__ == "__main__":
    main()
