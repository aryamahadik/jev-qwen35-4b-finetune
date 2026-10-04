"""Replay sampler for C round 1 / round 2 (C_DATA_SPEC.md v4 section 5; deny-list rules 3.H.3). CPU only.

Pool: data/v14_parts/golden_train.jsonl (C1's training rows) + data/v14_parts/golden_relations.jsonl. The source status
table is c_spec/tools/make_replay_register.py (its DROP / DEFAULT_DROP / CLAUDE_GOLD / VERIFY / HF_ONLY lists are read
with ast, never imported: importing it rewrites LICENCE_REGISTER.md).

What it does, in order (every step is counted in the report):
  1. Source drops: DROP, DEFAULT_DROP (forbidden list, decision 4), Claude-gold prefixes (binj_, std_, hard_, planted_,
     proc_), every VERIFY / HF-card-only / gd_finqa source unless --verified lists it (an upstream record was read).
  2. Known 3.H.3 part checks that need no sealed file (politeness Stack Exchange half, CoNLL-2003 inside CrossNER,
     CrowdTruth record id, accepted-subset asserts) + a provisional forbidden-name match (exact name hits dropped,
     substring hits reported for the deny-list program).
  3. Deny-list program verdicts (3.H): read from --denylist-verdicts (default c_build/replay_denylist_verdicts.json,
     written by `c_src/common/denylist.py replay` in its own process; this script never opens ohs3/). verdict 'drop'
     drops the source; 'drop_part' drops the rows of EVERY element of `parts` (a 'split' part keeps only rows proven to
     be from a train split: meta.split = train, group_id split token, meta.dataset train-split marker, or a builder-
     declared split re-checked in the builder source; fail closed). Missing -> PENDING (counts provisional; writing
     refused, and --allow-pending never writes). Stale (query sha, denylist.py sha, deny_aliases.json sha or the
     deny-list file sha differs from the current files), non-canonical, provisional, or older than the A16 rulings ->
     usable in a dry run, writing refused. The query file c_build/replay_denylist_query.json is (re)written whenever the
     pool changes.
  4. OHS-3 hit sources, whole-source rule (PREREG_FINAL.md amendment A8-prime; orchestrator decision 3 Oct): every
     row of OHS3_HIT_SOURCES = gd_redocred, gd_helpsteer3_pref is dropped, the same constant as extra/build_fix2.py.
     This replaces spec v4 5's "7 OHS-3 overlap units (gd_redocred 6, gd_helpsteer3_pref 1)" row (A10 disclosure):
     no per-unit id file (a10_overlap_ids.json) is read or needed. It overrides --verified and every keep status.
  5. Relation units (union of complement / inv / equiv edges); a unit is dropped whole if any of its rows is dropped.
  6. Old slice: 2,000 rows (one per group, per-source share by quota), held out of replay by group_id AND normalized
     state, in both rounds.
  7. Quotas over the remaining pool: n_s^0.7, floor min(n_s, 150), cap 4% of round 2 (7,200); round 1 = half of
     each source's round-2 quota (largest remainder to 90,000).
  8. Per source, one seeded stratified order of units (qtype x role x gold; yes/no gold balanced per role). Round-2
     draw = prefix covering (1 + margin) x Q2_s rows; round-1 draw = prefix covering (1 + margin) x Q1_s rows of the
     SAME order, so round 1 is nested in round 2.
  9. E2: hard-label yes/no rows grouped by normalized instruction wording (quoted spans, numbers and mid-sentence
     capitalised names masked), pooled across sources. Cells with >= 50 rows outside 50 +/- 5 are re-stratified by
     same-source, same-size unit swaps (round 1: only with round-2-only units, so round 2's set is unchanged; round 2:
     only with unused units, never touching round 1). Smaller cells are pooled by wording family (role | first three
     words of the last instruction line). Cells are re-derived after every swap (a wording that drops under 50 rows is
     scored in its family), and every wording cell with >= 50 rows at the start stays scored on its own rate, so a cell
     is never "fixed" by shrinking it. The after-report re-derives the cells on the final set. Vote-share rows are
     logged apart and never moved.

Attacked rows in the p_g rule (orchestrator decision, disclosed in the C PREREG amendment): an attacked row (meta.
attack_target set or role "attacked") with C1 p_g < 0.2 is COUNTED as a successful attack, not dropped as label noise,
and its relation unit is judged by its clean partner (the unit is dropped only if a non-attacked human-labelled
hard-label row in it has p_g < 0.2). So --second-pass defaults to --attacked-pg-rule clean_partner, and it refuses to
run until --pg-rule-amendment names that amendment ("amendment A<n>" present in PREREG_FINAL.md). The spec v4 5 rule
(the attacked row drops its unit) stays available as --attacked-pg-rule spec; the rule used goes into the output.

Modes:
  --dry-run            counts only (c_build/replay_counts_dryrun.json + log); writes the deny-list query file.
  --write-shards       (G14: needs --sealed-sha, the committed sealed-suite sha256; and the deny-list verdicts) round-1
                       read shards (5,000 rows each) for `od_gcp.py label` (data/c_replay_r1_shards/), the old-slice
                       shard dir, and c_build/replay_draw.json (ids + order).
  --second-pass DIR    (after the C1 read; DIR = the label dir) p_g rule (whole units), C1 top / p_top / p_g and the
                       anchor flag per row -> c_build/replay_r1_pg_anchor.json. Attacked rows: clean_partner (above;
                       needs --pg-rule-amendment A<n>), recorded in the output. The margin trim to 90,000 and the E2
                       re-check on the trimmed set are the mixer's (step 9). Writes no training rows.

  ../.venv/bin/python c_build/replay_sample.py --dry-run
  ../.venv/bin/python c_build/replay_sample.py --write-shards --sealed-sha <A15 suite sha256>
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent            # lean/c_build
LEAN = HERE.parent
DATA = LEAN / "data"
GOLDEN = DATA / "v14_parts/golden_train.jsonl"
RELS = DATA / "v14_parts/golden_relations.jsonl"
REGISTER_PY = LEAN / "c_spec/tools/make_replay_register.py"
FORBIDDEN = LEAN / "golden_src/forbidden_label_nli.json"
PREREG = LEAN / "PREREG_FINAL.md"
LOG = HERE / "progress_prep.log"
DENYLIST_PY = LEAN / "c_src/common/denylist.py"          # the verdicts must come from the current program ...
DENY_ALIASES = LEAN / "c_src/common/deny_aliases.json"   # ... and the current aliases (staleness check)
SEED = 20261003

# paths this program may never open (spec 0 rule 7, 3.H.1, 7.4 and the task's never-open list)
NEVER = re.compile(r"(^|/)(ohs3|sealed_nd|sealed_brief|prep89|external_quarantine|longbench_v2|ejs5)(/|$)|"
                   r"(^|/)data/[^/]*ohs3|ohs3_parts|(^|/)preds_ohs|jev", re.I)

# A8-prime whole-source rule (PREREG_FINAL.md amendment A8-prime, extra/build_fix2.py): the owner's counts-only OHS-3
# 12-gram check found 7 hit units in C1's own replay rows (gd_redocred 6, gd_helpsteer3_pref 1); both sources are left
# out WHOLE, so no per-unit ids are needed (replaces the A10 7-unit id input)
OHS3_HIT_SOURCES = ("gd_redocred", "gd_helpsteer3_pref")
PROGRAM_LABELLED = ("gd_gen", "pg_")                 # gd_gen* covers gd_gen2_*
PROGRAM_LABELLED_EXACT = {"judge_mathderiv", "gd_babi_logic", "gd_prontoqa", "gd_logicinference"}
BAND = (0.45, 0.55)
MIN_CELL = 50


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} replay_sample: {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def safe_open(p, mode="r"):
    s = str(Path(p).resolve())
    if NEVER.search(s.replace(str(LEAN.parent.parent), "")):
        raise SystemExit(f"refused: {p} is on the never-open list")
    return open(p, mode)


def h64(*parts) -> int:
    return int.from_bytes(hashlib.sha256(":".join(map(str, parts)).encode()).digest()[:8], "big")


# ------------------------------------------------------------------ source status (register lists, read with ast)

def register_lists():
    want = {"DROP", "DEFAULT_DROP", "CLAUDE_GOLD", "PROGRAM", "MAP", "HF_ONLY", "VERIFY", "_HF"}
    tree = ast.parse(safe_open(REGISTER_PY).read())
    ns = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in want:
            exec(compile(ast.Module([node], []), str(REGISTER_PY), "exec"), {"__builtins__": {}}, ns)
    missing = want - set(ns)
    if missing:
        raise SystemExit(f"register lists missing in {REGISTER_PY}: {sorted(missing)}")
    return ns


def source_status(s, reg, verified):
    if s in reg["DROP"]:
        return "drop", "DROP: " + reg["DROP"][s]
    if s in reg["DEFAULT_DROP"]:
        return "drop", "DROP (default, forbidden list): " + reg["DEFAULT_DROP"][s]
    if s.startswith(tuple(reg["CLAUDE_GOLD"])):
        return "drop", "DROP (default): Claude-written golds"
    if s in reg["HF_ONLY"]:
        return ("keep", "VERIFIED upstream") if s in verified else ("drop", "VERIFY (HF card only): not verified")
    if s in reg["VERIFY"]:
        return ("keep", "VERIFIED upstream") if s in verified else ("drop", "VERIFY: not verified")
    return "keep", ""


def program_labelled(s):
    return s.startswith(PROGRAM_LABELLED) or s in PROGRAM_LABELLED_EXACT


# ------------------------------------------------------------------ wording normalization (E2)

_Q = re.compile(r'"[^"\n]{0,400}"|“[^”\n]{0,400}”|(?<![A-Za-z])\'[^\'\n]{1,160}\'(?![A-Za-z])')
_N = re.compile(r"\d+(?:[.,:/-]\d+)*")
_E = re.compile(r"(?<=[a-z0-9,;:)>] )[A-Z][\w'&.-]*(?:\s+(?:of|de|the|and|&)?\s*[A-Z][\w'&.-]*)*")
_SP = re.compile(r"\s+")


def norm_wording(ins: str) -> str:
    s = _Q.sub("<Q>", ins or "")
    s = _N.sub("<N>", s)
    s = _E.sub("<E>", s)
    s = re.sub(r"(?:<E>\s*){2,}", "<E> ", s)
    return "\n".join(_SP.sub(" ", x).strip().lower() for x in s.split("\n") if x.strip())


def wording_family(role: str, w: str) -> str:
    last = w.split("\n")[-1]
    return f"{role}|" + " ".join(last.split()[:3])


def norm_state(state: str) -> str:
    return hashlib.sha1(_SP.sub(" ", (state or "").strip().lower()).encode()).hexdigest()[:16]


def row_key(r) -> str:
    s = "\x00".join([r.get("state") or "", r.get("card") or "", r.get("instructions") or "", json.dumps(r.get("options"))])
    return hashlib.sha1(s.encode()).hexdigest()[:16]


# ------------------------------------------------------------------ load

def load_rows():
    t = time.time()
    rows = []
    with safe_open(GOLDEN) as f:
        for line in f:
            r = json.loads(line)
            m = r.get("meta") or {}
            teach = m.get("teacher")
            human_soft = isinstance(teach, dict) and m.get("teacher_src") != "blend50"
            w = norm_wording(r["instructions"]) if r["qtype"] == "noul" else ""
            opts = r.get("options") or []
            rows.append({
                "id": r["id"], "source": r["source"], "group": r["group_id"], "qtype": r["qtype"], "role": r["role"],
                "gold": r["gold"],
                "nopt": len(opts), "dup_opts": len(set(map(str, opts))) != len(opts),
                "family": m.get("family") or "none", "dataset": m.get("dataset") or "", "domain": m.get("domain") or "",
                "split": str(m.get("split") or "").strip().lower(),
                "soft": human_soft, "gold_probs": bool(m.get("gold_probs")), "blend50": m.get("teacher_src") == "blend50",
                "attacked": bool(m.get("attack_target")) or r["role"] == "attacked",
                "option_level": "option_level" in m,
                "w": w, "wf": wording_family(r["role"], w) if w else "",
                "state": norm_state(r.get("state")), "key": row_key(r),
                "chars": len(r.get("state") or "") + len(r.get("card") or "") + len(r.get("instructions") or "")
                         + sum(len(str(o)) for o in opts),
            })
    log(f"loaded {len(rows):,} golden_train rows in {time.time() - t:.0f}s")
    rels = [json.loads(l) for l in safe_open(RELS) if l.strip()]
    return rows, rels


def build_units(rows, rels):
    idx = {r["id"]: i for i, r in enumerate(rows)}
    parent = list(range(len(rows)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    rel_type = defaultdict(set)
    for x in rels:
        a, b = idx[x["a"]], idx[x["b"]]
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
        rel_type[a].add(x["type"])
        rel_type[b].add(x["type"])
    comp = defaultdict(list)
    for i in range(len(rows)):
        comp[find(i)].append(i)
    units = []
    for members in comp.values():
        members.sort()
        types = set().union(*(rel_type[i] for i in members)) if members else set()
        units.append({"rows": members, "types": sorted(types), "source": rows[members[0]]["source"]})
    for u_i, u in enumerate(units):
        u["id"] = rows[u["rows"][0]]["id"]
        for i in u["rows"]:
            rows[i]["unit"] = u_i
        if len({rows[i]["source"] for i in u["rows"]}) != 1:
            raise SystemExit(f"unit {u['id']} spans sources")
    return units


# ------------------------------------------------------------------ drops

SUBSET_ASSERT = {  # 3.H.3: only the accepted subset may be present (checked on meta.dataset)
    "gd_ragtruth_summary": r"summary",
    "gd_helpsteer3_pref": r"preference",
    "gd_multiwoz21_sysacts": r"2\.1.*system",
    "gd_webred": r"2\+1",
    "gd_redocred": r"re-docred",
    "gd_crowdtruth_mre": r"medical relation extraction",
}


def part_taint(r):
    """Known 3.H.3 partial taints that need no sealed file. Returns a reason or None."""
    s, ds = r["source"], r["dataset"].lower()
    if s in ("gd_politeness_votes", "br_politeness_wiki") and ("stack" in ds or "stack" in r["domain"].lower()):
        return "3.H.3 politeness: Stack Exchange half"
    if s == "gd_crossner":
        parts = r["group"].split(":")
        dom = parts[3] if len(parts) > 3 else ""
        if "conll" in dom.lower() or "conll" in ds:
            return "3.H.3 CrossNER: bundled CoNLL-2003"
    if s == "gd_crowdtruth_mre" and "1472330" in ds:
        return "3.H.3 CrowdTruth: open-domain RE record (LDC text)"
    if s in SUBSET_ASSERT and not re.search(SUBSET_ASSERT[s], ds):
        return f"3.H.3 {s}: row outside the accepted subset"
    return None


# ------------------------------------------------------------------ 3.H.3 split-scope parts: train provenance

NON_TRAIN = {"test", "validation", "valid", "dev", "eval", "evaluation"}
# a group_id ':' segment that names the train split: 'train' itself, or '<prefix>_train_<n>' / 'train-<n>' style ids
GROUP_TRAIN_SEG = re.compile(r"^(?:train|(?:[a-z0-9]+[_-])?train[_-]\d+(?:[_-][\w-]*)?)$")
DS_TRAIN = re.compile(r"\btrain split\b|(?:^|/)train\.(?:txt|jsonl?|csv|tsv)\b", re.I)
DS_NON_TRAIN = re.compile(r"\b(?:test|validation|valid|dev|eval|evaluation) split\b|"
                          r"(?:^|/)(?:test|valid|validation|dev|eval)\.(?:txt|jsonl?|csv|tsv)\b", re.I)
# split declared per source by its builder; re-checked in the builder source on every run (both patterns must match)
TRAIN_SPLIT_DECLARED = {
    "arc": {"builder": "build_train_v06.py",
            "split_re": r'load_dataset\("allenai/ai2_arc", "ARC-Challenge", split="train"\)',
            "group_re": r'f"g:arc:\{x\[.id.\]\}"', "group_prefix": "g:arc:"},
}


def check_declared_splits(declared=None):
    """{source: 'builder.py:<line>' | None}: a declaration counts only if its builder file still holds both patterns."""
    out = {}
    for s, d in (declared or TRAIN_SPLIT_DECLARED).items():
        p = LEAN / d["builder"]
        txt = safe_open(p).read() if p.exists() else ""
        m = re.search(d["split_re"], txt)
        out[s] = f"{d['builder']}:{txt[:m.start()].count(chr(10)) + 1}" if m and re.search(d["group_re"], txt) else None
    return out


def train_provenance(r, declared_ok, declared=None):
    """(True, how) only when the row is proven to come from a train split; (False, why) otherwise (fail closed).
    Proofs: meta.split = train; a group_id ':' segment naming the train split; a train-split marker in meta.dataset;
    or a split declared by the source's builder (checked by check_declared_splits) for rows with the declared group
    prefix. Any test / validation / dev / eval token in the group_id, a non-train meta.split, or a non-train split
    marker in meta.dataset refutes the row; a meta.split that is neither proves nothing."""
    declared = TRAIN_SPLIT_DECLARED if declared is None else declared
    segs = r["group"].split(":")
    split = r.get("split") or ""
    if any(t in NON_TRAIN for g in segs for t in re.split(r"[_\-.]", g.lower())):
        return False, "non-train split token in group_id"
    if split and any(t in NON_TRAIN for t in re.split(r"[_\-.\s/]", split)):
        return False, "non-train meta.split"
    if DS_NON_TRAIN.search(r["dataset"] or ""):
        return False, "non-train split marker in meta.dataset"
    if split == "train":
        return True, "meta.split train"
    if any(GROUP_TRAIN_SEG.match(g) for g in segs[1:]):
        return True, "group_id split token"
    if DS_TRAIN.search(r["dataset"] or ""):
        return True, "meta.dataset train-split marker"
    d = declared.get(r["source"])
    if d and declared_ok.get(r["source"]) and r["group"].startswith(d["group_prefix"]):
        return True, f"builder-declared split ({declared_ok[r['source']]})"
    return False, "train provenance not proven"


def verdict_parts(v):
    """Every part a deny-list verdict asks to drop: 'parts' (denylist.py v1.1), else the older part + parts_all."""
    if "parts" in v:
        return list(v["parts"] or [])
    out = [v["part"]] if v.get("part") else []
    return out + [p for p in (v.get("parts_all") or []) if p not in out]


def part_drop(r, parts, declared_ok):
    """The deny-list part rule for one row: a reason to drop it, or None. Unknown part fields fail the run."""
    for pv in parts:
        f = pv.get("field")
        if f == "split":
            ok, how = train_provenance(r, declared_ok)
            if not ok:
                return f"3.H taint part (split): {how}"
        elif f in ("dataset", "domain", "group"):
            if str(r.get(f, "")) in set(pv.get("values", [])):
                return f"3.H taint part ({f})"
        else:
            raise SystemExit(f"deny-list part field {f!r} not understood (fail closed)")
    return None


def _nm(x):
    return re.sub(r"[^a-z0-9]", "", x.lower())


def forbidden_name_hits(sources, datasets_by_src):
    names = json.load(safe_open(FORBIDDEN))
    toks = {}
    full = {}
    for n in names:
        for t in {n, n.split("/")[0], n.split("/")[-1]}:
            if len(_nm(t)) >= 4:
                toks.setdefault(_nm(t), n)          # exact match against a source's core name
        for t in {n, n.split("/")[0]}:
            if len(_nm(t)) >= 6:
                full.setdefault(_nm(t), n)          # substring match in meta.dataset (no generic last segments)
    exact, sub = {}, {}
    for s in sources:
        core = _nm(re.sub(r"^(gd|br|tb|judge|pg)_", "", s))
        if core in toks:
            exact[s] = toks[core]
            continue
        for ds in datasets_by_src.get(s, ()):
            nd = _nm(ds)
            hit = next((n for t, n in full.items() if t in nd), None)
            if hit:
                sub[s] = (hit, ds[:120])
                break
    return exact, sub


def load_denylist(path):
    if not path or not Path(path).exists():
        return None
    v = json.load(safe_open(path))
    if "verdicts" not in v:
        raise SystemExit(f"{path}: no 'verdicts' key")
    return v


def sha256_path(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).exists() else None


def _lean_path(rel):
    """A path as denylist.py writes it (`lean/...` relative to the repo root, or absolute) -> a Path."""
    rel = str(rel or "")
    if rel.startswith("lean/"):
        return LEAN / rel[len("lean/"):]
    return Path(rel)


def denylist_blockers(deny, query_sha, sources):
    """Reasons the deny-list verdicts may not be used to write shards (empty list = usable). Dry runs apply them
    anyway and report these reasons. Staleness: the verdicts must come from the CURRENT query, denylist.py and
    deny_aliases.json, and the deny-list file they name must still hold the sha they record."""
    out = []
    if deny.get("program") != "c_src/common/denylist.py" or deny.get("run") != "replay":
        out.append("not a denylist.py replay run")
    if deny.get("canonical") is not True:
        out.append("non-canonical verdicts (built without the real ohs3/used_sources.json or the fixed selection)")
    if deny.get("provisional"):
        out.append(f"provisional verdicts: {deny['provisional']}")
    if deny.get("query_sha256") != query_sha:
        out.append("stale: built from another replay_denylist_query.json (re-run denylist.py replay)")
    if deny.get("program_sha256") != sha256_path(DENYLIST_PY):
        out.append(f"stale: built by another denylist.py ({str(deny.get('program_sha256'))[:12]} vs current "
                   f"{str(sha256_path(DENYLIST_PY))[:12]}; re-run denylist.py replay)")
    if deny.get("aliases_sha256") != sha256_path(DENY_ALIASES):
        out.append(f"stale: built from another deny_aliases.json ({str(deny.get('aliases_sha256'))[:12]} vs current "
                   f"{str(sha256_path(DENY_ALIASES))[:12]}; re-run denylist.py replay)")
    dl_path = _lean_path(deny.get("denylist"))
    if deny.get("denylist_sha256") != sha256_path(dl_path):
        out.append(f"stale: the deny-list file {deny.get('denylist')} is missing or no longer the one the verdicts were "
                   "built with (re-run denylist.py replay)")
    if not str(deny.get("platform_rule", "")).startswith("RULED (PREREG_FINAL.md A16 a)"):
        out.append("verdicts predate the A16 rulings (bare-platform-word rule not RULED in the header)")
    miss = sorted(set(sources) - set(deny["verdicts"]))
    if miss:
        out.append(f"{len(miss)} pool sources have no verdict: {miss[:5]}")
    return out


def denylist_query(rows):
    q = defaultdict(lambda: {"names": set(), "datasets": set(), "domains": set()})
    for r in rows:
        e = q[r["source"]]
        e["names"].add(r["source"])
        if r["dataset"]:
            e["datasets"].add(r["dataset"])
        if r["domain"]:
            e["domains"].add(r["domain"])
    out = {"purpose": "3.H.3 replay check: one verdict per replay source (taint / no_new_rows / none)",
           "sources": {s: {k: sorted(v) for k, v in e.items()} for s, e in sorted(q.items())}}
    return json.dumps(out, indent=1)


def write_denylist_query(rows, path):
    """Writes the query when it is missing or changed; returns (its sha256, whether it was (re)written)."""
    s = denylist_query(rows)
    sha = hashlib.sha256(s.encode()).hexdigest()
    p = Path(path)
    if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == sha:
        return sha, False
    p.write_text(s)
    return sha, True


# ------------------------------------------------------------------ quotas, old slice, order

def quotas(n, total, alpha=0.7, floor=150, cap_frac=0.04):
    cap = int(round(cap_frac * total))
    lo = {s: min(v, floor) for s, v in n.items()}
    hi = {s: min(v, cap) for s, v in n.items()}
    if sum(hi.values()) < total:
        log(f"WARNING: pool cannot fill {total:,} under the cap; taking {sum(hi.values()):,}")
        return dict(hi), cap
    a, b = 0.0, 1e6
    f = lambda lam: sum(min(hi[s], max(lo[s], lam * n[s] ** alpha)) for s in n)
    for _ in range(200):
        mid = (a + b) / 2
        (a, b) = (mid, b) if f(mid) < total else (a, mid)
    raw = {s: min(hi[s], max(lo[s], b * n[s] ** alpha)) for s in n}
    q = {s: int(math.floor(v)) for s, v in raw.items()}
    rest = total - sum(q.values())
    for s in sorted(n, key=lambda s: (-(raw[s] - q[s]), s)):
        if rest <= 0:
            break
        if q[s] < hi[s]:
            q[s] += 1
            rest -= 1
    return q, cap


def split_half(q2, total1):
    raw = {s: v / 2 for s, v in q2.items()}
    q1 = {s: int(math.floor(v)) for s, v in raw.items()}
    rest = total1 - sum(q1.values())
    for s in sorted(q2, key=lambda s: (-(raw[s] - q1[s]), h64(SEED, "half", s))):
        if rest <= 0:
            break
        if q1[s] < q2[s]:
            q1[s] += 1
            rest -= 1
    return q1


def largest_remainder(weights, total):
    tw = sum(weights.values()) or 1
    raw = {s: total * w / tw for s, w in weights.items()}
    q = {s: int(math.floor(v)) for s, v in raw.items()}
    rest = total - sum(q.values())
    for s in sorted(weights, key=lambda s: (-(raw[s] - q[s]), s)):
        if rest <= 0:
            break
        q[s] += 1
        rest -= 1
    return q


def draw_old_slice(rows, units, live_units, q2, size=2000):
    share = largest_remainder({s: v for s, v in q2.items() if v > 0}, size)
    by_src = defaultdict(list)
    for ui in live_units:
        by_src[units[ui]["source"]].append(ui)
    picked = []
    for s, k in share.items():
        groups = defaultdict(list)
        for ui in by_src[s]:
            for i in units[ui]["rows"]:
                groups[rows[i]["group"]].append(i)
        order = sorted(groups, key=lambda g: h64(SEED, "old", g))
        for g in order[:k]:
            members = sorted(groups[g])
            picked.append(members[h64(SEED, "oldrow", g) % len(members)])
    return picked


def unit_order(rows, units, uis):
    """Seeded stratified order of a source's units: qtype x role x gold of the unit's lead row; yes/no gold balanced
    per role (each gold half gets half of the role's span), choice strata proportional."""
    strata = defaultdict(list)
    for ui in uis:
        r = rows[units[ui]["rows"][0]]
        strata[(r["qtype"], r["role"], r["gold"] if r["qtype"] == "noul" else "-")].append(ui)
    role_n = Counter()
    for (qt, role, g), us in strata.items():
        if qt == "noul":
            role_n[role] += len(us)
    keyed = []
    for st, us in strata.items():
        us.sort(key=lambda ui: h64(SEED, "rank", units[ui]["id"]))
        off = (h64(SEED, "off", *st) % 10 ** 6) / 10 ** 6
        span = role_n[st[1]] / 2 if st[0] == "noul" else len(us)
        for rank, ui in enumerate(us):
            keyed.append(((rank + off) / span, h64(SEED, "tie", units[ui]["id"]), ui))
    keyed.sort()
    return [ui for _, _, ui in keyed]


def prefix(order, units, target):
    out, n = [], 0
    for ui in order:
        if n >= target:
            break
        out.append(ui)
        n += len(units[ui]["rows"])
    return out


# ------------------------------------------------------------------ E2 cells and re-stratification

def hard_yn(r):
    return r["qtype"] == "noul" and not r["soft"] and not r["gold_probs"]


def cell_defs(rows, units, sel):
    wc = Counter()
    for ui in sel:
        for i in units[ui]["rows"]:
            if hard_yn(rows[i]):
                wc[rows[i]["w"]] += 1
    big = {w for w, c in wc.items() if c >= MIN_CELL}
    return lambda r: ("w:" + r["w"]) if r["w"] in big else ("f:" + r["wf"])


def cell_stats(rows, units, sel, cell_of):
    st = defaultdict(lambda: [0, 0])     # cell -> [n, yes]
    for ui in sel:
        for i in units[ui]["rows"]:
            r = rows[i]
            if hard_yn(r):
                c = st[cell_of(r)]
                c[0] += 1
                c[1] += r["gold"]
    return st


def _pen(n, y):
    """Out-of-band mass of a checked cell (>= MIN_CELL rows): rows outside 50 +/- 5, 0 for a smaller cell."""
    if n < MIN_CELL:
        return 0.0
    return _pen_any(n, y)


def _pen_any(n, y):
    """Out-of-band distance x max(n, MIN_CELL), at any size (for a sticky cell: >= MIN_CELL rows in the starting draw).
    Under MIN_CELL rows the weight stays MIN_CELL, so dropping rows without moving the rate never scores as a gain."""
    if n <= 0:
        return 0.0
    rate = y / n
    return max(0.0, BAND[0] - rate, rate - BAND[1]) * max(n, MIN_CELL)


def restratify(rows, units, sel, pool, cap=300, fixed=()):
    """Greedy same-source, same-size unit swaps between sel and pool that lower the E2 out-of-band mass. The cells are
    the spec's, kept current after every swap: a wording with >= MIN_CELL hard yes/no rows (sel + fixed) is its own
    cell; the rows of every smaller wording pool into their wording family's cell, which is checked once it has >=
    MIN_CELL rows. So a wording cell that a swap shrinks under MIN_CELL is scored in its family from then on. Also, every
    wording cell that had >= MIN_CELL rows at the start is sticky: it stays scored on its own rate at any size, so a
    cell is fixed only when its rate is inside 50 +/- 5, never by shrinking it. A swap is taken only if it lowers the
    total (cells + families + sticky cells). First choice: a pool unit with rows in the same cell; else a pool unit
    of the same source from other wordings (the spec's drop-and-refill). A cell no swap improves is marked stuck.
    `fixed` units count in the rates but are never swapped (round 1 inside round 2).
    Returns (new sel set, new pool set, swaps, stuck cells, sticky wordings)."""
    import bisect
    sel, pool = set(sel), set(pool)
    contrib = {}

    def uc(ui):  # {(wording, family): [n, yes]} of the unit's hard-label yes/no rows
        if ui not in contrib:
            c = {}
            for i in units[ui]["rows"]:
                r = rows[i]
                if hard_yn(r):
                    v = c.setdefault((r["w"], r["wf"]), [0, 0])
                    v[0] += 1
                    v[1] += r["gold"]
            contrib[ui] = c
        return contrib[ui]
    hk = lambda ui: h64(SEED, "pool", units[ui]["id"])
    key = lambda ui: (units[ui]["source"], len(units[ui]["rows"]))
    pst = defaultdict(lambda: [0, 0])            # (wording, family) -> [n, yes] over sel + fixed
    wst = defaultdict(lambda: [0, 0])            # wording -> [n, yes]
    fams_of = defaultdict(set)                   # wording -> families its rows fall in
    sel_w, sel_f = defaultdict(set), defaultdict(set)
    for ui in list(sel) + list(fixed):
        for (w, f), (n, y) in uc(ui).items():
            pst[(w, f)][0] += n
            pst[(w, f)][1] += y
            wst[w][0] += n
            wst[w][1] += y
            fams_of[w].add(f)
            if ui in sel:
                sel_w[w].add(ui)
                sel_f[f].add(ui)
    sticky = {w for w, (n, _) in wst.items() if n >= MIN_CELL}
    small = lambda w, ws=wst: ws[w][0] < MIN_CELL
    fam = defaultdict(lambda: [0, 0])            # family -> [n, yes] of its small wordings' rows
    for (w, f), (n, y) in pst.items():
        if small(w):
            fam[f][0] += n
            fam[f][1] += y

    def wpen(w, n, y):
        return _pen(n, y) if n >= MIN_CELL else (_pen_any(n, y) if w in sticky else 0.0)

    def delta(cu, cv):
        """(after - before) of the objective over the cells a swap touches, and the new per-wording / per-family
        counts. A touched wording that crosses MIN_CELL moves all its rows between its own cell and its families."""
        W = {w for w, _ in cu} | {w for w, _ in cv}
        F = {f for w in W for f in fams_of[w]} | {f for _, f in cu} | {f for _, f in cv}
        d_pair = defaultdict(lambda: [0, 0])
        for k, (n, y) in cu.items():
            d_pair[k][0] -= n
            d_pair[k][1] -= y
        for k, (n, y) in cv.items():
            d_pair[k][0] += n
            d_pair[k][1] += y
        new_w = {w: [wst[w][0], wst[w][1]] for w in W}
        for (w, _), (dn, dy) in d_pair.items():
            new_w[w][0] += dn
            new_w[w][1] += dy
        new_f = {f: [fam[f][0], fam[f][1]] for f in F}
        for w in W:
            was, now = wst[w][0] < MIN_CELL, new_w[w][0] < MIN_CELL
            for f in fams_of[w] | {f for (ww, f) in d_pair if ww == w}:
                old, dn = pst[(w, f)], d_pair.get((w, f), (0, 0))
                if was:
                    new_f[f][0] -= old[0]
                    new_f[f][1] -= old[1]
                if now:
                    new_f[f][0] += old[0] + dn[0]
                    new_f[f][1] += old[1] + dn[1]
        before = sum(wpen(w, *wst[w]) for w in W) + sum(_pen(*fam[f]) for f in F)
        after = sum(wpen(w, *new_w[w]) for w in W) + sum(_pen(*new_f[f]) for f in F)
        return after - before, d_pair, new_w, new_f

    pool_k, pool_ck = defaultdict(list), defaultdict(list)

    def pool_keys(ui):
        return {("w", w) for w, _ in uc(ui)} | {("f", f) for _, f in uc(ui)}
    for ui in sorted(pool, key=hk):
        pool_k[key(ui)].append((hk(ui), ui))
        for c in pool_keys(ui):
            pool_ck[(c,) + key(ui)].append((hk(ui), ui))

    def lrem(lst, ui):
        j = bisect.bisect_left(lst, (hk(ui), ui))
        if j < len(lst) and lst[j][1] == ui:
            lst.pop(j)

    def cell_pen(c):
        kind, x = c
        return wpen(x, *wst[x]) if kind == "w" else _pen(*fam[x])

    stuck, swaps = set(), 0
    while True:
        bad = [(cell_pen(c), c) for c in [("w", w) for w in wst] + [("f", f) for f in fam]
               if c not in stuck and cell_pen(c) > 0]
        if not bad:
            break
        _, c = max(bad)
        kind, x = c
        n, y = wst[x] if kind == "w" else fam[x]
        excess = 1 if y / n > BAND[1] else 0

        def over(ui):  # the unit's rows in this cell with the over-represented gold
            if kind == "w":
                return sum((yy if excess else nn - yy) for (w, _), (nn, yy) in uc(ui).items() if w == x)
            return sum((yy if excess else nn - yy) for (w, f), (nn, yy) in uc(ui).items() if f == x and small(w))
        outs = sorted((ui for ui in (sel_w[x] if kind == "w" else sel_f[x]) if over(ui) > 0), key=hk)
        done = False
        for u in outs:
            k = key(u)
            cands = [v for _, v in pool_ck.get((c,) + k, [])[:cap]] + [v for _, v in pool_k.get(k, [])[:cap]]
            best = None
            for v in cands:
                dlt, *_ = delta(uc(u), uc(v))
                if dlt < -1e-9 and (best is None or dlt < best[0]):
                    best = (dlt, v)
            if best is None:
                continue
            v = best[1]
            _, d_pair, new_w, new_f = delta(uc(u), uc(v))
            for (w, f), (dn, dy) in d_pair.items():
                pst[(w, f)][0] += dn
                pst[(w, f)][1] += dy
                fams_of[w].add(f)
            for w, val in new_w.items():
                wst[w] = val
            for f, val in new_f.items():
                fam[f] = val
            for w, f in uc(u):
                sel_w[w].discard(u)
                sel_f[f].discard(u)
            for w, f in uc(v):
                sel_w[w].add(v)
                sel_f[f].add(v)
            sel.remove(u), sel.add(v), pool.remove(v), pool.add(u)
            lrem(pool_k[k], v)
            bisect.insort(pool_k[k], (hk(u), u))
            for t in pool_keys(v):
                lrem(pool_ck[(t,) + k], v)
            for t in pool_keys(u):
                bisect.insort(pool_ck[(t,) + k], (hk(u), u))
            swaps += 1
            done = True
            break
        if not done:
            stuck.add(c)
    return sel, pool, swaps, sorted(f"{k}:{x}" for k, x in stuck), sticky


def e2_report(rows, units, sel, cell_of=None, sticky=()):
    """E2 cells of `sel` as the spec defines them on THIS set (cell_of None: cell_defs recomputed on sel), plus the
    sticky cells (wording cells with >= MIN_CELL rows in the starting draw) scored on their own rate at any size."""
    cell_of = cell_of or cell_defs(rows, units, sel)
    st = cell_stats(rows, units, sel, cell_of)
    checked = {c: v for c, v in st.items() if v[0] >= MIN_CELL}
    out_band = {c: v for c, v in checked.items() if not BAND[0] <= v[1] / v[0] <= BAND[1]}
    small = {c: v for c, v in st.items() if v[0] < MIN_CELL}
    rep = {
        "hard_yn_rows": sum(v[0] for v in st.values()),
        "yes_rate": round(sum(v[1] for v in st.values()) / max(1, sum(v[0] for v in st.values())), 4),
        "cells_checked": len(checked), "wording_cells_checked": sum(c.startswith("w:") for c in checked),
        "family_cells_checked": sum(c.startswith("f:") for c in checked),
        "cells_out_of_band": len(out_band), "rows_in_out_of_band_cells": sum(v[0] for v in out_band.values()),
        "small_pooled_cells_under_50": len(small), "rows_in_small_cells": sum(v[0] for v in small.values()),
        "worst": [{"cell": c[:140], "n": v[0], "yes_rate": round(v[1] / v[0], 3)}
                  for c, v in sorted(out_band.items(), key=lambda kv: -_pen(*kv[1]))[:15]],
    }
    if sticky:
        ws = defaultdict(lambda: [0, 0])
        for ui in sel:
            for i in units[ui]["rows"]:
                r = rows[i]
                if hard_yn(r) and r["w"] in sticky:
                    ws[r["w"]][0] += 1
                    ws[r["w"]][1] += r["gold"]
        bad = {w: v for w, v in ws.items() if _pen_any(*v) > 0}
        rep["start_cells"] = {
            "n": len(sticky), "now_under_50": sum(1 for w in sticky if ws[w][0] < MIN_CELL),
            "emptied": sum(1 for w in sticky if ws[w][0] == 0),
            "out_of_band_own_rate": len(bad), "rows_out_of_band_own_rate": sum(v[0] for v in bad.values()),
            "worst": [{"cell": ("w:" + w)[:140], "n": v[0], "yes_rate": round(v[1] / v[0], 3)}
                      for w, v in sorted(bad.items(), key=lambda kv: -_pen_any(*kv[1]))[:15]]}
    return rep


# ------------------------------------------------------------------ summaries

def summarize(rows, units, sel, name):
    src, fam, role, yn = Counter(), Counter(), Counter(), defaultdict(lambda: [0, 0])
    n = choice = soft = att = gp = dup = b50 = ordl = chars = reads_chars = reads_needed = 0
    prot = Counter()
    keys = Counter()
    for ui in sel:
        u = units[ui]
        for t in u["types"]:
            prot[t] += len(u["rows"])
        for i in u["rows"]:
            r = rows[i]
            n += 1
            src[r["source"]] += 1
            fam[r["family"]] += 1
            role[(r["qtype"], r["role"])] += 1
            choice += r["qtype"] == "choice"
            soft += r["soft"]
            att += r["attacked"]
            gp += r["gold_probs"]
            dup += r["dup_opts"]
            b50 += r["blend50"]
            ordl += r["option_level"]
            keys[r["key"]] += 1
            chars += r["chars"]
            reads_chars += r["chars"] * (2 if r["qtype"] == "choice" else 1)
            if not (r["soft"] or r["gold_probs"]):
                reads_needed += 1 + (r["qtype"] == "choice")
            if hard_yn(r):
                yn[r["source"]][0] += 1
                yn[r["source"]][1] += r["gold"]
    hy = sum(v[0] for v in yn.values())
    return {
        "name": name, "rows": n, "units": len(sel), "sources": len(src),
        "choice_rows": choice, "yesno_rows": n - choice, "hard_yesno_rows": hy,
        "hard_yesno_yes_rate": round(sum(v[1] for v in yn.values()) / max(1, hy), 4),
        "vote_share_rows": soft, "gold_probs_rows": gp, "blend50_only_rows": b50, "attacked_rows": att,
        "rows_in_units_by_relation": dict(prot), "dup_option_rows": dup, "ordinal_option_level_rows": ordl,
        "duplicate_row_keys": sum(c - 1 for c in keys.values() if c > 1),
        "reads_A5": n + choice, "reads_A5_without_own_target_rows": reads_needed, "chars_total": chars, "chars_weighted_by_reads": reads_chars,
        "by_family": dict(fam.most_common()),
        "by_qtype_role": {f"{a}/{b}": c for (a, b), c in role.most_common()},
        "by_source": dict(src.most_common()),
        "per_source_hard_yes_rate_outside_45_55": {s: [v[0], round(v[1] / v[0], 3)] for s, v in sorted(yn.items())
                                                    if v[0] >= 30 and not 0.45 <= v[1] / v[0] <= 0.55},
    }


def l4_estimate(sum_draw):
    """Scale the measured L4 read of the label-audit shard (4B, one view, merged, same layout): 15,590 golden_train rows
    (<= 150 per source) in 4,491 s (logs/audit_label.log, 30 Sep). Cost taken as proportional to prompt characters."""
    p = DATA / "v14_audit_shards/shard_000.jsonl"
    if not p.exists():
        return None
    ch = 0
    n = 0
    with safe_open(p) as f:
        for line in f:
            r = json.loads(line)
            ch += len(r.get("state") or "") + len(r.get("card") or "") + len(r.get("instructions") or "") + \
                sum(len(str(o)) for o in r.get("options") or [])
            n += 1
    sec_per_char = 4491.0 / ch
    sec = sum_draw["chars_weighted_by_reads"] * sec_per_char
    return {"ref": "data/v14_audit_shards shard_000: 15,590 rows, 4,491 s, NVIDIA L4, 4B merged, 1 view",
            "ref_rows": n, "ref_chars_per_row": round(ch / n), "draw_chars_per_read": round(
                sum_draw["chars_weighted_by_reads"] / max(1, sum_draw["reads_A5"])),
            "reads": sum_draw["reads_A5"], "est_hours_char_scaled": round(sec / 3600, 1),
            "est_hours_rows_scaled": round(sum_draw["reads_A5"] / (15590 / 4491) / 3600, 1)}


# ------------------------------------------------------------------ main

def parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write-shards", action="store_true")
    ap.add_argument("--second-pass", default="", help="C1 label dir (od_gcp.py label output) for the p_g rule")
    ap.add_argument("--shards-dir", default=str(DATA / "c_replay_r1_shards"), help="round-1 read shards")
    ap.add_argument("--r1", type=int, default=90000)
    ap.add_argument("--r2", type=int, default=180000)
    ap.add_argument("--margin", type=float, default=0.10)
    ap.add_argument("--old-slice", type=int, default=2000)
    ap.add_argument("--verified", default="", help="JSON list of VERIFY sources confirmed upstream (default: none)")
    ap.add_argument("--denylist-verdicts", default=str(HERE / "replay_denylist_verdicts.json"))
    ap.add_argument("--allow-pending", action="store_true", help="dry run only: say so explicitly when the deny-list "
                    "verdicts are missing. --write-shards refuses it (the write path never runs without usable verdicts)")
    ap.add_argument("--sealed-sha", default="", help="G14: the sealed suite sha256 committed in PREREG_FINAL.md "
                    "(required by --write-shards: the replay sample is spec 11 step 9, after the sealed commit)")
    ap.add_argument("--attacked-pg-rule", choices=["spec", "clean_partner"], default="clean_partner",
                    help="--second-pass: 'clean_partner' (default; orchestrator decision, disclosed in the C PREREG "
                    "amendment: an attacked row with p_g < 0.2 is counted as a successful attack, not dropped, and "
                    "its unit is judged by its clean partner; needs --pg-rule-amendment) or 'spec' (spec v4 5: the "
                    "attacked row drops its unit like any human-labelled hard-label row)")
    ap.add_argument("--pg-rule-amendment", default="", help="the PREREG_FINAL.md amendment id (e.g. A15) that discloses "
                    "--attacked-pg-rule clean_partner (the C PREREG amendment)")
    return ap


def main(argv=None):
    ap = parser()
    a = ap.parse_args(argv)
    if not (a.dry_run or a.write_shards or a.second_pass):
        ap.error("pick --dry-run, --write-shards or --second-pass")
    if a.write_shards and a.allow_pending:
        raise SystemExit("refusing: --allow-pending is a dry-run flag; --write-shards needs usable deny-list verdicts")
    if a.second_pass:
        return second_pass(a)
    t0 = time.time()
    reg = register_lists()
    verified = set(json.load(safe_open(a.verified))) if a.verified else set()
    rows, rels = load_rows()
    units = build_units(rows, rels)
    log(f"{len(units):,} relation units")
    rep = {"spec": "C_DATA_SPEC.md v4 section 5 / 3.H.3", "seed": SEED, "pool_rows": len(rows),
           "pool_sources": len({r['source'] for r in rows}), "pool_units": len(units)}

    # 1-4 drops
    drop = {}
    src_rows = Counter(r["source"] for r in rows)
    status = {s: source_status(s, reg, verified) for s in src_rows}
    datasets = defaultdict(set)
    for r in rows:
        datasets[r["source"]].add(r["dataset"])
    exact, sub = forbidden_name_hits([s for s, (st, _) in status.items() if st == "keep"], datasets)
    for s, n in exact.items():
        status[s] = ("drop", f"provisional forbidden-name hit: {n}")
    query_sha, query_new = write_denylist_query(rows, HERE / "replay_denylist_query.json")
    if query_new:
        log("deny-list query (re)written: c_build/replay_denylist_query.json (the pool changed or it was missing)")
    deny = load_denylist(a.denylist_verdicts)
    blockers = []
    if deny is None:
        log(f"deny-list verdicts {Path(a.denylist_verdicts).name} missing -> 3.H verdicts PENDING (counts provisional; "
            "--write-shards refuses). Run, in its own process: ../.venv/bin/python c_src/common/denylist.py replay "
            "(reads c_build/replay_denylist_query.json, writes c_build/replay_denylist_verdicts.json)")
    else:
        blockers = denylist_blockers(deny, query_sha, src_rows)
        if blockers:
            log("WARNING deny-list verdicts not usable for --write-shards: " + "; ".join(blockers))
        for s, v in deny["verdicts"].items():
            if s not in status or status[s][0] != "keep":
                continue
            if "verdict" in v:
                whole = v["verdict"] == "drop"
            else:                                       # pre-v1.1 schema
                whole = v.get("hit") and v.get("class") == "taint" and not verdict_parts(v) \
                    and not v.get("dev_seen_exception")
            if whole:
                status[s] = ("drop", f"3.H taint: {v.get('entry', '')}")
    # A8-prime whole-source rule: after every other status, so neither --verified nor a deny-list verdict keeps them
    ohs3_hit = {}
    for s in OHS3_HIT_SOURCES:
        prev = status.get(s)
        ohs3_hit[s] = {"rows": src_rows.get(s, 0), "status_before": (f"{prev[0]}: {prev[1]}" if prev and prev[1]
                                                                     else (prev[0] if prev else "not in pool"))}
        if prev is not None:
            status[s] = ("drop", "A8' OHS-3 hit source: whole source left out (extra/build_fix2.py OHS3_HIT_SOURCES)"
                         + (f"; also {prev[1]}" if prev[0] == "drop" else ""))
    log("A8' whole-source rule (replaces the A10 7-unit ids): dropped "
        + ", ".join(f"{s} ({v['rows']:,} rows; before: {v['status_before'][:60]})" for s, v in ohs3_hit.items()))
    part_rules = {s: verdict_parts(v) for s, v in (deny or {}).get("verdicts", {}).items()}
    declared_ok = check_declared_splits()
    for s, ok in declared_ok.items():
        if not ok:
            log(f"WARNING builder-declared train split for {s} not found in {TRAIN_SPLIT_DECLARED[s]['builder']}: "
                "its split-scope rows are unproven (dropped)")
    reasons = Counter()
    split_proof = defaultdict(Counter)                  # source -> how each row of a split-scope part was judged
    for i, r in enumerate(rows):
        st, why = status[r["source"]]
        parts = part_rules.get(r["source"], ())
        if any(p.get("field") == "split" for p in parts):
            split_proof[r["source"]]["status " + st] += 1
            if st == "keep":
                split_proof[r["source"]][train_provenance(r, declared_ok)[1]] += 1
        if st == "drop":
            drop[i] = why
        else:
            pt = part_taint(r) or part_drop(r, parts, declared_ok)
            if pt:
                drop[i] = pt
        if i in drop:
            reasons[drop[i].split(":")[0]] += 1
    dropped_units = set()
    for ui, u in enumerate(units):
        if any(i in drop for i in u["rows"]):
            dropped_units.add(ui)
    cascade = sum(1 for ui in dropped_units for i in units[ui]["rows"] if i not in drop)
    live = [ui for ui in range(len(units)) if ui not in dropped_units]
    rep["drops"] = {
        "rows_dropped": len(drop) + cascade, "rows_dropped_by_rule": dict(reasons.most_common()),
        "rows_dropped_with_their_unit": cascade,
        "sources_dropped": {s: [src_rows[s], why] for s, (st, why) in sorted(status.items()) if st == "drop"},
        "provisional_forbidden_name_hits_exact_dropped": exact,
        "provisional_forbidden_name_hits_substring_report_only": {s: list(v) for s, v in sub.items()},
        "denylist_3H": ("PENDING (c_build/replay_denylist_verdicts.json missing: run c_src/common/denylist.py replay)"
                        if deny is None else ("applied" if not blockers else "applied (NOT usable for --write-shards: "
                                              + "; ".join(blockers) + ")")),
        "denylist_verdicts": None if deny is None else {
            "path": os.path.relpath(Path(a.denylist_verdicts).resolve(), LEAN),
            "sha256": hashlib.sha256(Path(a.denylist_verdicts).read_bytes()).hexdigest(),
            "program_sha256": deny.get("program_sha256"), "program_sha256_now": sha256_path(DENYLIST_PY),
            "aliases_sha256": deny.get("aliases_sha256"), "aliases_sha256_now": sha256_path(DENY_ALIASES),
            "denylist_sha256": deny.get("denylist_sha256"), "platform_rule": deny.get("platform_rule"),
            "query_sha256": deny.get("query_sha256"), "query_sha256_now": query_sha, "canonical": deny.get("canonical"),
            "counts": deny.get("counts"), "provisional": deny.get("provisional"), "blockers": blockers},
        "split_scope_train_provenance": {
            "rule": "3.H.3 split-scope taint: a row is kept only if proven to be from a train split (group_id split "
                    "token, meta.dataset train-split marker, or a builder-declared split re-checked in the builder "
                    "source); every other row is dropped (fail closed)",
            "declared": declared_ok, "sources": {s: dict(c) for s, c in sorted(split_proof.items())}},
        "ohs3_hit_sources_A8prime": {"rule": "whole source dropped (PREREG_FINAL.md A8-prime; replaces the A10 7-unit "
                                             "ids; extra/build_fix2.py OHS3_HIT_SOURCES)", "sources": ohs3_hit},
        "verified_sources": sorted(verified),
    }
    # "No row is used twice": identical (state, instructions, options) rows keep one unit (seeded); a key whose copies
    # disagree on gold drops every unit that holds it (label conflict)
    golds = defaultdict(set)
    for ui in live:
        for i in units[ui]["rows"]:
            golds[rows[i]["key"]].add(str(rows[i]["gold"]))
    conflict = {k for k, g in golds.items() if len(g) > 1}
    seen, dup_units, conf_units = set(), set(), set()
    for ui in sorted(live, key=lambda ui: h64(SEED, "dedupe", units[ui]["id"])):
        ks = {rows[i]["key"] for i in units[ui]["rows"]}
        if ks & conflict:
            conf_units.add(ui)
        elif ks & seen:
            dup_units.add(ui)
        else:
            seen |= ks
    live = [ui for ui in live if ui not in dup_units and ui not in conf_units]
    rep["drops"]["duplicate_text_rows_dropped"] = sum(len(units[ui]["rows"]) for ui in dup_units)
    rep["drops"]["conflicting_gold_duplicate_rows_dropped"] = sum(len(units[ui]["rows"]) for ui in conf_units)
    elig_rows = sum(len(units[ui]["rows"]) for ui in live)
    rep["eligible_before_old_slice"] = {"rows": elig_rows, "units": len(live),
                                        "sources": len({units[ui]['source'] for ui in live})}
    log(f"eligible pool: {elig_rows:,} rows in {len(live):,} units")

    # 6 old slice
    n_s = Counter()
    for ui in live:
        n_s[units[ui]["source"]] += len(units[ui]["rows"])
    q2, _ = quotas(dict(n_s), a.r2)
    old = draw_old_slice(rows, units, live, q2, a.old_slice)
    og, ost = {rows[i]["group"] for i in old}, {rows[i]["state"] for i in old}
    held = set()
    for ui in live:
        if any(rows[i]["group"] in og or rows[i]["state"] in ost for i in units[ui]["rows"]):
            held.add(ui)
    live = [ui for ui in live if ui not in held]
    held_rows = sum(len(units[ui]["rows"]) for ui in held)
    rep["old_slice"] = {"rows": len(old), "sources": len({rows[i]['source'] for i in old}),
                        "groups": len(og), "states": len(ost),
                        "replay_rows_held_out_with_it": held_rows,
                        "hard_yes_rate": round(sum(rows[i]["gold"] for i in old if hard_yn(rows[i]))
                                               / max(1, sum(hard_yn(rows[i]) for i in old)), 3)}

    # 7 quotas
    n_s = Counter()
    by_src = defaultdict(list)
    for ui in live:
        n_s[units[ui]["source"]] += len(units[ui]["rows"])
        by_src[units[ui]["source"]].append(ui)
    q2, cap = quotas(dict(n_s), a.r2)
    q1 = split_half(q2, a.r1)
    rep["eligible"] = {"rows": sum(n_s.values()), "units": len(live), "sources": len(n_s)}
    rep["quota"] = {"r2_total": sum(q2.values()), "r1_total": sum(q1.values()), "cap": cap,
                    "sources_at_cap": sorted(s for s, v in q2.items() if v >= cap),
                    "sources_at_floor_all_rows": sorted(s for s, v in q2.items() if v == n_s[s]),
                    "r2_over_eligible": round(sum(q2.values()) / max(1, sum(n_s.values())), 3)}

    # 8 draws
    r1, r2 = [], []
    for s, uis in by_src.items():
        order = unit_order(rows, units, uis)
        t2 = min(n_s[s], int(math.ceil((1 + a.margin) * q2[s])))
        t1 = min(n_s[s], int(math.ceil((1 + a.margin) * q1[s])))
        r2 += prefix(order, units, t2)
        r1 += prefix(order, units, t1)
    assert set(r1) <= set(r2)
    unused = set(live) - set(r2)

    # 9 E2 (cells re-derived on each set: "before" on the draw, "after" on the re-stratified set)
    before1 = e2_report(rows, units, r1)
    r1_new, r2_only, sw1, stuck1, sticky1 = restratify(rows, units, r1, set(r2) - set(r1))
    after1 = e2_report(rows, units, r1_new, sticky=sticky1)
    r2_set = r1_new | r2_only
    before2 = e2_report(rows, units, r2_set)
    fresh, unused2, sw2, stuck2, sticky2 = restratify(rows, units, r2_only, unused, fixed=r1_new)
    r2_new = r1_new | fresh
    after2 = e2_report(rows, units, r2_new, sticky=sticky2)
    assert r1_new <= r2_new
    rep["e2"] = {"rule": "cells re-derived on the final set; start cells (>= 50 rows at the start) also scored on "
                         "their own rate at any size", "round1_draw": {"before": before1, "swaps": sw1,
                 "stuck_cells": stuck1[:20], "n_stuck": len(stuck1), "after": after1},
                 "round2_draw": {"before": before2, "swaps": sw2, "stuck_cells": stuck2[:20], "n_stuck": len(stuck2),
                                 "after": after2}}
    rep["round1_draw"] = summarize(rows, units, r1_new, f"round 1 draw ({a.r1:,} + {a.margin:.0%} margin)")
    rep["round2_draw"] = summarize(rows, units, r2_new, f"round 2 superset draw ({a.r2:,} + {a.margin:.0%} margin)")
    rep["round1_draw"]["human_labelled_hard_rows_pg_rule_applies"] = sum(
        1 for ui in r1_new for i in units[ui]["rows"]
        if not program_labelled(rows[i]["source"]) and not rows[i]["soft"] and not rows[i]["gold_probs"])
    rep["l4_estimate_round1_read"] = l4_estimate(rep["round1_draw"])
    rep["l4_estimate_old_slice"] = None
    rep["quota_by_source"] = {s: {"eligible": n_s[s], "q2": q2[s], "q1": q1[s]} for s in sorted(q2, key=lambda s: -q2[s])}
    rep["sec"] = round(time.time() - t0)
    out = HERE / "replay_counts_dryrun.json"
    out.write_text(json.dumps(rep, indent=1))
    log(f"dry run done in {rep['sec']}s: r1 draw {rep['round1_draw']['rows']:,} rows, r2 draw "
        f"{rep['round2_draw']['rows']:,} rows; E2 r1 out-of-band cells (re-derived on the final set) "
        f"{before1['cells_out_of_band']} -> {after1['cells_out_of_band']}, start cells out of band on their own rate "
        f"{after1['start_cells']['out_of_band_own_rate']} ({sw1} swaps, {len(stuck1)} stuck); r2 "
        f"{before2['cells_out_of_band']} -> {after2['cells_out_of_band']} / {after2['start_cells']['out_of_band_own_rate']}"
        f" ({sw2} swaps); report {out.name}")
    if a.dry_run:
        return rep
    if deny is None:
        raise SystemExit("refusing to write: deny-list verdicts are PENDING (see the log)")
    if blockers:
        raise SystemExit("refusing to write: deny-list verdicts not usable: " + "; ".join(blockers))
    why = sealed_sha_problem(a.sealed_sha)
    if why:
        raise SystemExit(f"refusing to write: G14 needs --sealed-sha <the sealed suite sha256 frozen by amendment A15 "
                         f"in PREREG_FINAL.md>: {why}")
    rep["write"] = {"sealed_sha256": a.sealed_sha, "a15": "suite sha found in the A15 amendment block of PREREG_FINAL.md",
                    "sampler_sha256": sha256_path(Path(__file__).resolve()),
                    "denylist_verdicts_sha256": rep["drops"]["denylist_verdicts"]["sha256"]}
    rep["write"].update(write_outputs(rows, units, r1_new, r2_new, old, a, rep["write"]))
    out = HERE / "replay_r1_write.json"
    out.write_text(json.dumps(rep, indent=1))
    log(f"write record: {out.name} (counts as in the dry-run report + the shard manifests)")
    return rep


def sealed_sha_problem(sha, text=None):
    """None when `sha` is the sealed suite sha256 frozen in PREREG_FINAL.md amendment A15 (the 'suite ... sha256 <hex>'
    line inside the A15 block); else the reason (G14: the replay sample is a step-9 output, after the sealed commit)."""
    if not re.fullmatch(r"[0-9a-f]{64}", sha or ""):
        return "not a 64-hex sha256"
    text = safe_open(PREREG).read() if text is None else text
    m = re.search(r"\*\*Amendment A15\b(.*?)(?=\n\s*>?\s*\*\*Amendment A\d|\Z)", text, re.S)
    if not m:
        return "no 'Amendment A15' block in PREREG_FINAL.md"
    block = m.group(1)
    if sha not in block:
        return "the sha is not in the A15 block"
    if not re.search(r"suite\s+`?suite_v\d+\.jsonl`?,\s+sha256\s+`?" + sha, block):
        return "the sha is in A15 but not as the suite file's sha256"
    return None


def write_outputs(rows, units, r1, r2, old, a, provenance=None):
    """Round-1 read shards for od_gcp.py label + the old-slice shard dir + the draw file (ids and order). Returns the
    counts and manifest hashes for the write record. Rows whose options repeat a string are not read (the readout
    cannot tell the options apart); they are counted and stay out of round 1 (their units are judged without them)."""
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    want = {i for ui in r1 for i in units[ui]["rows"]}
    want_old = set(old)
    keep, keep_old = [], []
    with safe_open(GOLDEN) as f:
        for i, line in enumerate(f):
            if i in want:
                keep.append(json.loads(line))
            elif i in want_old:
                keep_old.append(json.loads(line))
    n_drawn = len(keep)
    keep = [r for r in keep if len(set(map(str, r.get("options") or []))) == len(r.get("options") or [])]
    info = {"purpose": "C round-1 replay draw: C1 A5 read (p_g rule + selective anchor)", "seed": SEED,
            "from": str(GOLDEN.relative_to(LEAN)), **(provenance or {})}
    sd = Path(a.shards_dir)
    od = sd.parent / "c_old_slice_shards"
    m1 = sg.write_shards(keep, sd, 5000, info)
    m2 = sg.write_shards(keep_old, od, 2500, {**info, "purpose": "C old slice (monitor)"})
    draw = HERE / "replay_draw.json"
    draw.write_text(json.dumps({
        "seed": SEED, **(provenance or {}), "r1_unit_ids": sorted(units[ui]["id"] for ui in r1),
        "r2_unit_ids": sorted(units[ui]["id"] for ui in r2), "old_slice_ids": sorted(rows[i]["id"] for i in old)}))
    log(f"wrote {len(keep):,} round-1 read rows ({n_drawn - len(keep):,} repeated-option rows not read), "
        f"{len(keep_old):,} old-slice rows, replay_draw.json")

    def man(d, m):
        return {"dir": os.path.relpath(d, LEAN), "rows": m["rows"], "shards": len(m["shards"]),
                "manifest_sha256": sha256_path(d / sg.MANIFEST), "ids_sha256": m["ids_sha256"],
                "rows_sha256": m["rows_sha256"], "files": {s["file"]: s["sha256"] for s in m["shards"]}}
    return {"round1_rows_drawn": n_drawn, "round1_rows_read": len(keep),
            "round1_repeated_option_rows_not_read": n_drawn - len(keep), "round1_units": len(r1),
            "round2_units": len(r2), "old_slice_rows": len(keep_old),
            "round1_shards": man(sd, m1), "old_slice_shards": man(od, m2),
            "replay_draw": {"path": os.path.relpath(draw, LEAN), "sha256": sha256_path(draw)}}


def pg_rule(a) -> dict:
    """The p_g rule for attacked rows, as recorded in replay_r1_pg_anchor.json. Default 'clean_partner' (orchestrator
    decision: an attacked row's low p_g is a successful attack, not label noise: count it, judge the unit by its clean
    partner). It changes spec v4 5's pre-registered rule, so it runs only with --pg-rule-amendment naming the C PREREG
    amendment present in PREREG_FINAL.md. 'spec' (every human-labelled hard-label row with C1 p_g < 0.2 is dropped,
    attacked rows included) needs no amendment."""
    if a.attacked_pg_rule == "spec":
        return {"attacked_rows": "spec", "amendment": None}
    am = a.pg_rule_amendment or ""
    if not re.fullmatch(r"A\d+[a-z-]*", am):
        raise SystemExit("--attacked-pg-rule clean_partner changes spec 5's p_g rule: it needs --pg-rule-amendment "
                         "<the PREREG_FINAL.md amendment id that adopts it, A<n>>")
    if not re.search(rf"\b[Aa]mendment {re.escape(am)}\b", safe_open(PREREG).read()):
        raise SystemExit(f"--pg-rule-amendment {am}: no 'amendment {am}' in {PREREG.name} (record it first)")
    return {"attacked_rows": "clean_partner", "amendment": am}


def pg_drop_units(rows, rule: str):
    """Units the p_g rule drops (whole units, never single rows). rows: dicts with source, unit, attacked, own_target
    (vote shares or gold_probs) and p_g. Program-labelled sources and rows with their own target are never dropped.
    rule 'spec': any other row with p_g < 0.2 drops its unit. rule 'clean_partner': an attacked row with p_g < 0.2 is
    only counted. Returns (units dropped, attacked rows with p_g < 0.2)."""
    drop, att_low = set(), 0
    for r in rows:
        if program_labelled(r["source"]) or r["own_target"] or r["p_g"] >= 0.2:
            continue
        if r["attacked"]:
            att_low += 1
            if rule == "clean_partner":
                continue
        drop.add(r["unit"])
    return drop, att_low


def second_pass(a):
    """After the C1 read (od_gcp.py label --tta-choice on data/c_replay_r1_shards). Per row: p_g, C1's top answer and
    the anchor flag; per relation unit: the p_g drop. Rules (spec 5): a human-labelled hard-label row with p_g < 0.2
    drops its whole relation unit (whole units, never single rows); program-labelled sources, vote-share and gold_probs
    rows are never dropped. Attacked rows: counted, not dropped; the unit is judged by its clean partner (default
    clean_partner, needs the C PREREG amendment id; pg_rule); the rule used is written to the output. Anchor: no own
    target, C1 right, and p_top >= 0.8
    ("c1_anchor") or the row is in a protected unit (inv / equiv / complement unit, attacked row or its clean partner:
    "c1_anchor_protected"). The margin trim to 90,000 and the E2 re-check run in the mixer on these flags. Writes ids
    and flags only (no training rows: G14)."""
    rule = pg_rule(a)
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    sd = Path(a.shards_dir)
    probs, view = sg.load_labels(a.second_pass, sd, return_view=True)
    s = (view or {}).get("settings") or {}
    if not (s.get("name") == "q35_4b_main500k" and s.get("tta_choice") and not s.get("tta_noul")
            and s.get("perm_seed") is None and s.get("layout") == "schema_branch_mark"):
        raise SystemExit(f"labels are not the C1 A5 read: {s}")
    rows = [r for p in sg.shard_files(sd) for r in sg.read_jsonl(p)]
    ids = {r["id"] for r in rows}
    rels = [x for x in (json.loads(l) for l in safe_open(RELS) if l.strip()) if x["a"] in ids and x["b"] in ids]
    units = build_units(rows, rels)
    clean_of_attacked = {(r.get("meta") or {}).get("clean_id") for r in rows} - {None}
    for x in rels:
        if x["type"] == "inv":
            clean_of_attacked.add(x["a"])
    flags, judged, cnt = {}, [], Counter()
    for r in rows:
        m = r.get("meta") or {}
        p = probs[r["id"]]
        gold_key = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
        pg = p[gold_key]
        top = max(p, key=p.get)
        soft = isinstance(m.get("teacher"), dict) and m.get("teacher_src") != "blend50"
        own_target = soft or bool(m.get("gold_probs"))
        attacked = bool(m.get("attack_target")) or r["role"] == "attacked"
        judged.append({"source": r["source"], "unit": r["unit"], "attacked": attacked, "own_target": own_target,
                       "p_g": pg})
        protected = attacked or r["id"] in clean_of_attacked or bool(
            set(units[r["unit"]]["types"]) & {"inv", "equiv", "complement"})
        anchor = None
        if not own_target and top == gold_key:
            anchor = "c1_anchor" if p[top] >= 0.8 else ("c1_anchor_protected" if protected else None)
        flags[r["id"]] = {"p_g": round(pg, 4), "top": top, "p_top": round(p[top], 4), "anchor": anchor}
    drop_units, att_low = pg_drop_units(judged, rule["attacked_rows"])
    for r in rows:
        flags[r["id"]]["drop_pg"] = r["unit"] in drop_units
        cnt["rows_dropped_pg" if r["unit"] in drop_units else "rows_kept"] += 1
        if r["unit"] not in drop_units:
            cnt[f"anchor:{flags[r['id']]['anchor']}"] += 1
    out = {"read": s, "pg_rule": rule, "units_dropped_pg": len(drop_units), "attacked_rows_pg_lt_0.2": att_low,
           "attacked_rows_pg_lt_0.2_kept": att_low if rule["attacked_rows"] == "clean_partner" else 0,
           "counts": dict(cnt), "flags": flags}
    (HERE / "replay_r1_pg_anchor.json").write_text(json.dumps(out))
    log(f"second pass (p_g rule for attacked rows: {rule}): {len(drop_units)} units dropped by p_g; counts {dict(cnt)}")


if __name__ == "__main__":
    main()
