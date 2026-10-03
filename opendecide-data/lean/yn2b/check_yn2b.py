"""check_yn2b.py: decontamination of the yn2b rows (SPEC.md section 7), programs only, CPU only.

Input: the ASSEMBLED yn2b files (golden row format: id, source, state, instructions, options, card, meta.latent_id,
meta.dev_kind). Checks, each reported per family (= source):
  7.1  12-word runs of every state, instruction, option and card line against held-out text: OHS-1/2 states,
       instructions and options (+ cards); eval, eval_card, eval_jagged, eval_opi, eval_redef, eval_long, eval_multi
       states; every string of bench/jevbench/datasets/public and bench/jevbench_v154/datasets/public.
       OHS-3 is loaded inside one function into an in-memory set and only the NUMBER of hits per family leaves it:
       no OHS-3 text, id or row is ever printed or written, and the dropped units are recorded only as salted hashes.
  7.2  12-word runs against every dev / eval split (dev, devzs, devzs2, devp_card, pg_dev, debate_dev, dev_nc,
       taskbank_dev, hard_dev, dev_negwords, dev_claims, hard12_dev, proc12_dev, planted12_dev, golden_dev,
       breadth_dev).
  A hit in 7.1 / 7.2 drops the whole latent unit (source + meta.latent_id). A yn2b text under 12 words is matched
  as one whole-text gram, and only from 4 words up (row_ghash: "0", "yes" or "none of these" is no source item).
  7.3  6-word runs of instruction and plant TEMPLATES (--templates; else the rendered instructions and meta.plant
       strings of the rows) against the dialogue_rebuttal templates, the v11 train templates (build_v11_fixes), the
       instruction of every row of the 9 ship splits, OHS-1/2 instructions and cards, and the injected spans (attacked
       text minus clean text) of eval_jagged, eval_opi and eval_redef; the banned words of SPEC 4.7 in any instruction
       or option; the cue-share rule (no word in >= 30 rows is more than 60% tied to answer-flipping questions); the
       marker rule (the <<<UNTRUSTED TEXT ...>>> strings only inside the state of a marker-spoof attack twin).
       7.3 failures are template bugs: reported (exit code 1), never silently dropped.
  7.5  exact dedupe of normalised state + instruction against golden_train and across yn2b units (the later unit is
       dropped; views inside one latent unit are exempt, F4(a) shares its base row's state by design).
  7.6  dev against train inside yn2b: every holdout / devx state shares at most 20% of its 12-grams with any single
       train state (the union share is reported too), and no iid dev state equals a train state; failing dev units
       are dropped.
  7.7  names (--names): no pool name occurs in a JevBench public string or in OHS-1/2 text (whole-word match; see
       --strict-substring); OHS-3 by hash comparison only (counts).
7.4 (the unseen set) is yn2b/check_unseen.py.
Outputs: --report (JSON: counts per family and check; row ids for non-OHS-3 hits; OHS-3 counts only) and --drop
(JSON: sorted salted sha256 of the dropped units' "source:latent_id"; assemble_yn2b.py --drop reads it). Exit 1 when a
7.3 / 7.7 check fails.

  ../.venv/bin/python yn2b/check_yn2b.py --train v14_parts/yn2b_train.jsonl --dev yn2b_dev.jsonl --devx yn2b_devx.jsonl \\
        --report /path/decontam.json --drop v14_parts/yn2b_raw/yn2b_drop.json
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402

N_HELD, N_TMPL = 12, 6
MIN_SHORT_WORDS = 4  # a yn2b text under 12 words counts as one whole-text gram only from 4 words up (see row_ghash)
DROP_SALT = "yn2b-drop:"
BENCH_DIRS = ("bench/jevbench/datasets/public", "bench/jevbench_v154/datasets/public")  # relative to the repo root
HELD_STATE_FILES = ("eval", "eval_card", "eval_jagged", "eval_opi", "eval_redef", "eval_long", "eval_multi")
OHS12 = ("ohs", "ohs2")
OHS3 = "ohs3"
DEV_SPLITS = ("dev", "devzs", "devzs2", "devp_card", "pg_dev", "debate_dev", "dev_nc", "taskbank_dev", "hard_dev",
              "dev_negwords", "dev_claims", "hard12_dev", "proc12_dev", "planted12_dev", "v14_parts/golden_dev",
              "breadth_dev")
SHIP_SPLITS = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev")
BANNED_WORDS = ("right", "wrong", "correct", "incorrect", "accurate", "inaccurate", "mistaken", "reply", "agreed",
                "disagree", "undercut", "debate", "two notes")
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(w).replace(r"\ ", r"\s+") for w in BANNED_WORDS) + r")\b", re.I)
CUE_MAX, CUE_MIN_COUNT = 0.60, 30
DEV_TRAIN_MAX = 0.20
SPOOF_FAMILIES = ("gd_gen3_rule_chain", "gd_gen3_tool_guard")  # F1, F2 (SPEC 4.8)

_words = lambda t: re.sub(r"[^\w]+", " ", (t or "").lower()).split()  # noqa: E731  (build_v13_breadth.words)
norm = lambda t: " ".join(_words(t))  # noqa: E731


def grams(text, n=N_HELD):
    """build_v13_breadth.grams for n = 12: word n-grams (a shorter text counts as one gram)."""
    w = _words(text)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)} if len(w) >= n else ({" ".join(w)} if w else set())


def ghash(text, n=N_HELD):
    """grams() as a set of 64-bit hashes (one process only; keeps the large held-out sets small in memory)."""
    return {hash(g) for g in grams(text, n)}


def row_ghash(text):
    """ghash() for a yn2b row text (7.1, 7.2, OHS-3). A text of 12+ words gives its 12-word runs. A shorter text is one
    whole-text gram (build_v13_breadth's rule, so a short state is still checked for a verbatim copy) only when it has
    at least MIN_SHORT_WORDS words: shorter texts are generic labels ("yes", "0", "5", "none of these") whose equality
    with a held-out option names no source item (1 Oct: all 90 F3 'hits' were such options). The reference sets keep
    the plain ghash(), so a 4-11-word yn2b text still matches an identical short held-out text."""
    return ghash(text) if len(_words(text)) >= MIN_SHORT_WORDS else set()


def toks(s):
    """build_v11_fixes.toks: template slots {x} -> 'zzslot', lower-case alphanumeric tokens."""
    s = re.sub(r"\{[^{}]*\}", " zzslot ", s or "")
    return re.findall(r"[a-z0-9]+", s.lower())


def runs(s, n=N_TMPL):
    t = toks(s)
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def row_texts(r):
    """Every text a yn2b row shows the model: state, instructions, options, card."""
    out = [r.get("state") or "", r.get("instructions") or ""]
    out += [o for o in (r.get("options") or []) if isinstance(o, str)]
    out += [ln for ln in (r.get("card") or "").splitlines() if ln.strip()]
    return out


def unit_key(r) -> str:
    return f"{r['source']}:{(r.get('meta') or {}).get('latent_id')}"


def drop_hash(key: str) -> str:
    return hashlib.sha256((DROP_SALT + key).encode()).hexdigest()


def _jsonl(root, name):
    p = root / "data" / f"{name}.jsonl"
    return yc.iter_jsonl(p) if p.exists() else None


# ------------------------------------------------------------------------------------------------ reference sets
def held_sets(root):
    """{set name: 12-gram set} for 7.1 without OHS-3, plus the list of missing files."""
    out, missing = {}, []
    for f in OHS12:
        it = _jsonl(root, f)
        if it is None:
            missing.append(f)
            continue
        g = set()
        for r in it:
            for s in [r.get("state"), r.get("instructions"), r.get("card")] + list(r.get("options") or []):
                if isinstance(s, str):
                    g |= ghash(s)
        out[f] = g
    for f in HELD_STATE_FILES:
        it = _jsonl(root, f)
        if it is None:
            missing.append(f)
            continue
        g = set()
        for r in it:
            g |= ghash(r.get("state") or "")
        out[f] = g
    for d in BENCH_DIRS:
        p = root.parent.parent / d
        files = sorted(p.glob("*.jsonl")) if p.exists() else []
        if not files:
            missing.append(d)
        g = set()
        for fp in files:
            for r in yc.iter_jsonl(fp):
                for s in strings(r):
                    g |= ghash(s)
        out[d] = g
    return out, missing


def ohs3_blind(root, rows, names=()):
    """7.1 and 7.7 against OHS-3, blind: the file is read here only, into memory; returns (hit units per family as
    a Counter, the salted hashes of the hit units, name hits per family, loaded). No text, id or row leaves this
    function; the n-gram set is hashed and deleted before it returns."""
    it = _jsonl(root, OHS3)
    if it is None:
        return Counter(), set(), Counter(), False
    want = defaultdict(dict)  # name length -> {hash of the name's words: [families]}
    for fam, nm in names:
        w = _words(nm)
        if 1 <= len(w) <= 6:
            want[len(w)].setdefault(hash(" ".join(w)), []).append(fam)
    g, name_hits = set(), Counter()
    for r in it:
        for s in [r.get("state"), r.get("instructions"), r.get("card")] + list(r.get("options") or []):
            if not isinstance(s, str):
                continue
            g |= ghash(s)
            if want:
                w = _words(s)
                for n, hs in want.items():
                    for i in range(len(w) - n + 1):
                        fams = hs.pop(hash(" ".join(w[i:i + n])), None)
                        if fams:
                            name_hits.update(fams)
    hit_units = defaultdict(set)
    for r in rows:
        if any(row_ghash(t) & g for t in row_texts(r)):
            hit_units[r["source"]].add(drop_hash(unit_key(r)))
    del g, want
    return Counter({k: len(v) for k, v in hit_units.items()}), set().union(*hit_units.values()) if hit_units else set(), \
        name_hits, True


def dev_sets(root):
    out, missing = {}, []
    for f in DEV_SPLITS:
        it = _jsonl(root, f)
        if it is None:
            missing.append(f)
            continue
        g = set()
        for r in it:
            for s in row_texts(r):
                g |= ghash(s)
        out[f] = g
    return out, missing


def injected_spans(root):
    """Attacked text minus clean text of eval_jagged (item_id: baseline vs adversarial), eval_opi (OPI row vs its
    clean_id row) and eval_redef (variant != clean vs the clean row of the same base_id): the inserted / replaced word
    spans, as strings."""
    spans = []

    def fields(r):
        return " \n ".join([r.get("state") or "", r.get("instructions") or "", r.get("card") or ""]
                           + [o for o in (r.get("options") or []) if isinstance(o, str)])

    def diff(clean, att):
        a, b = toks(fields(clean)), toks(fields(att))
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op in ("insert", "replace") and j2 > j1:
                spans.append(" ".join(b[j1:j2]))

    it = _jsonl(root, "eval_jagged")
    if it is not None:
        pair = defaultdict(dict)
        for r in it:
            pair[(r.get("meta") or {}).get("item_id")][(r.get("meta") or {}).get("arm")] = r
        for arms in pair.values():
            if "baseline" in arms and "adversarial" in arms:
                diff(arms["baseline"], arms["adversarial"])
    it = _jsonl(root, "eval_opi")
    if it is not None:
        rows = {r["id"]: r for r in it}
        for r in rows.values():
            c = (r.get("meta") or {}).get("clean_id")
            if r.get("track") == "OPI" and c in rows:
                diff(rows[c], r)
    it = _jsonl(root, "eval_redef")
    if it is not None:
        by = defaultdict(dict)
        for r in it:
            m = r.get("meta") or {}
            by[m.get("base_id")].setdefault(m.get("variant"), []).append(r)
        for vs in by.values():
            for c in vs.get("clean", [])[:1]:
                for v, rs in vs.items():
                    if v != "clean":
                        for r in rs:
                            diff(c, r)
    return spans


def template_refs(root):
    """{reference name: set of 6-word runs} for 7.3."""
    import build_v11_fixes as b
    refs = {"dialogue_rebuttal": set().union(*[runs(t["text"]) for t in b.TEMPLATES if t["family"] == b.DEV_FAMILY]),
            "v11_train_templates": set().union(*[runs(t["text"]) for t in b.TEMPLATES if t["family"] != b.DEV_FAMILY])}
    g = set()
    for sp in SHIP_SPLITS:
        it = _jsonl(root, sp)
        for r in it or ():
            g |= runs(r.get("instructions") or "")
    refs["ship_split_instructions"] = g
    g = set()
    for f in OHS12:
        for r in _jsonl(root, f) or ():
            g |= runs(r.get("instructions") or "")
            g |= runs(r.get("card") or "")
    refs["ohs12_instructions_cards"] = g
    refs["eval_injected_spans"] = set().union(*[runs(s) for s in injected_spans(root)] or [set()])
    return refs


# ------------------------------------------------------------------------------------------------ checks
def check_12(rows, sets):
    """{family: {set: n hit units}}, {hit unit key: [set names]}, row ids per set."""
    hits, per_unit = defaultdict(Counter), defaultdict(set)
    for r in rows:
        tg = set().union(*[row_ghash(t) for t in row_texts(r)])
        for name, g in sets.items():
            if tg & g:
                per_unit[unit_key(r)].add(name)
    fam_units = defaultdict(lambda: defaultdict(set))
    for k, names in per_unit.items():
        for n in names:
            fam_units[k.split(":", 1)[0]][n].add(k)
    for fam, d in fam_units.items():
        hits[fam] = Counter({n: len(v) for n, v in d.items()})
    return {f: dict(c) for f, c in hits.items()}, {k: sorted(v) for k, v in per_unit.items()}


def template_items(rows, templates=None):
    """[(family, kind, text, is_flipping)] from --templates or from the rows (instructions + meta.plant)."""
    if templates is not None:
        return [(t.get("family", "?"), t.get("kind", "instruction"), t["text"], bool(t.get("flips"))) for t in templates]
    out = []
    for r in rows:
        m = r.get("meta") or {}
        pol = m.get("polarity")  # mv_core: number of answer flips of the question (0 para, 1 neg, 2 dneg)
        flip = r.get("role") == "neg" or (isinstance(pol, int) and pol % 2 == 1) or m.get("q_polarity") == "neg"
        out.append((r["source"], "instruction", r.get("instructions") or "", flip))
        if isinstance(m.get("plant"), str):
            out.append((r["source"], "plant", m["plant"], False))
    return out + mv_core_plants()


def mv_core_plants():
    """mv_core's attack-plant templates (PLANT_TEMPLATES, SPOOF_TEMPLATES) as 'plant' items, when mv_core imports."""
    try:
        if str(yc.GEN3) not in sys.path:
            sys.path.insert(0, str(yc.GEN3))
        import mv_core
    except Exception:  # noqa: BLE001  (mv_core not built yet, or broken: the rows' own plants still count)
        return []
    out = []
    for name in ("PLANT_TEMPLATES", "SPOOF_TEMPLATES"):
        for tid, text in sorted((getattr(mv_core, name, None) or {}).items()):
            out.append(("mv_core_plants", "plant", text, False))
    return out


def check_templates(items, refs):
    clash = defaultdict(lambda: defaultdict(set))
    seen = {}
    for fam, kind, text, _ in items:
        k = (fam, kind, text)
        if k in seen:
            continue
        seen[k] = runs(text)
        for name, R in refs.items():
            if seen[k] & R:
                clash[fam][name].add(text)
    return {f: {n: len(v) for n, v in d.items()} for f, d in clash.items()}, \
        {f: {n: sorted(v)[:3] for n, v in d.items()} for f, d in clash.items()}


def banned_words(rows):
    out = defaultdict(list)
    for r in rows:
        for t in [r.get("instructions") or ""] + [o for o in (r.get("options") or []) if isinstance(o, str)]:
            m = BANNED_RE.search(t)
            if m:
                out[r["source"]].append((r["id"], m.group(1).lower()))
                break
    return out


def cue_shares(items, min_count=CUE_MIN_COUNT):
    """build_v11_fixes.cue_shares at row level over instructions: {family: (worst word, share, count)}."""
    import build_v11_fixes as b
    per = defaultdict(list)
    for fam, kind, text, flip in items:
        if kind == "instruction":
            per[fam].append((text, flip))
    out = {}
    for fam, its in per.items():
        sh = {w: v for w, v in b.cue_shares(its).items() if v[1] >= min_count}
        if sh:
            w, (s, n) = max(sh.items(), key=lambda kv: kv[1][0])
            out[fam] = {"word": w, "share": round(s, 4), "count": n, "pass": s <= CUE_MAX + 1e-12}
    return out


def marker_rule(rows, spoof_families=SPOOF_FAMILIES):
    bad = []
    for r in rows:
        m = r.get("meta") or {}
        spoof_ok = (r["source"] in spoof_families and r.get("role") == "attacked"
                    and bool(m.get("plant_spoof") or m.get("marker_spoof")))  # mv_core: meta.plant_spoof
        for field, texts in (("state", [r.get("state") or ""]), ("instructions", [r.get("instructions") or ""]),
                             ("options", [o for o in (r.get("options") or []) if isinstance(o, str)]),
                             ("card", [r.get("card") or ""])):
            if any(mk in t for t in texts for mk in yc.MARKERS) and not (field == "state" and spoof_ok):
                bad.append((r["id"], field))
    return bad


def dedupe(rows, golden_path=None):
    """7.5: units to drop (later duplicates across units, and rows equal to a golden_train row)."""
    key = lambda r: hashlib.sha1((norm(r.get("state")) + "||" + norm(r.get("instructions"))).encode()).digest()  # noqa: E731
    first, drop, n_within = {}, set(), 0
    for r in rows:
        k, u = key(r), unit_key(r)
        if k in first and first[k] != u:
            drop.add(u)
            n_within += 1
        first.setdefault(k, u)
    n_golden = 0
    if golden_path and Path(golden_path).exists():
        want = set(first)
        for g in yc.iter_jsonl(golden_path):
            k = key(g)
            if k in want:
                for r in rows:
                    if key(r) == k:
                        drop.add(unit_key(r))
                        n_golden += 1
                want.discard(k)
    return drop, {"within_yn2b_rows": n_within, "equal_to_golden_train_rows": n_golden}


def dev_vs_train(train, dev):
    """7.6: per dev unit the largest share of its state's 12-grams found in ONE train state (and in the union)."""
    tr_states = {norm(r.get("state")) for r in train}
    dg = {}
    for r in dev:
        g = grams(r.get("state") or "")
        if g:
            dg[r["id"]] = (r, g)
    inv = defaultdict(list)
    for i, (_, g) in dg.items():
        for x in g:
            inv[x].append(i)
    best, union = Counter(), defaultdict(set)
    seen_states = set()
    for t in train:
        st = t.get("state") or ""
        if st in seen_states:
            continue
        seen_states.add(st)
        c = Counter()
        for x in grams(st):
            for i in inv.get(x, ()):
                c[i] += 1
                union[i].add(x)
        for i, n in c.items():
            best[i] = max(best[i], n / len(dg[i][1]))
    fails, report = set(), {"holdout_devx_rows": 0, "max_share_single_train_state": 0.0, "max_share_union": 0.0,
                            "iid_equal_to_train": 0, "failing_units": 0}
    for i, (r, g) in dg.items():
        kind = (r.get("meta") or {}).get("dev_kind")
        if kind in ("holdout", "devx"):
            report["holdout_devx_rows"] += 1
            report["max_share_single_train_state"] = max(report["max_share_single_train_state"], best[i])
            report["max_share_union"] = max(report["max_share_union"], len(union[i]) / len(g))
            if best[i] > DEV_TRAIN_MAX + 1e-12:
                fails.add(unit_key(r))
    for r in dev:
        if (r.get("meta") or {}).get("dev_kind") == "iid" and norm(r.get("state")) in tr_states:
            report["iid_equal_to_train"] += 1
            fails.add(unit_key(r))
    report["failing_units"] = len(fails)
    report["max_share_single_train_state"] = round(report["max_share_single_train_state"], 4)
    report["max_share_union"] = round(report["max_share_union"], 4)
    return fails, report


def name_check(root, names, strict=False):
    """7.7 without OHS-3: {family: [names found]} in JevBench public strings or OHS-1/2 text."""
    texts = []
    for d in BENCH_DIRS:
        p = root.parent.parent / d
        for fp in sorted(p.glob("*.jsonl")) if p.exists() else []:
            for r in yc.iter_jsonl(fp):
                texts.extend(strings(r))
    for f in OHS12:
        for r in _jsonl(root, f) or ():
            texts.extend(s for s in [r.get("state"), r.get("instructions"), r.get("card")] + list(r.get("options") or [])
                         if isinstance(s, str))
    if strict:
        blob = "\n".join(t.lower() for t in texts)
        found = lambda nm: nm.lower() in blob  # noqa: E731
    else:
        blob = " " + " ".join(" ".join(_words(t)) + " |" for t in texts) + " "
        found = lambda nm: (" " + " ".join(_words(nm)) + " ") in blob  # noqa: E731
    out = defaultdict(list)
    for fam, nm in names:
        if nm.strip() and found(nm):
            out[fam].append(nm)
    return out


def load_names(path):
    """--names: JSON {family: [name, ...]} or a JSON list of names (family '?')."""
    if not path:
        return []
    obj = json.loads(Path(path).read_text())
    if isinstance(obj, dict):
        return [(f, n) for f, ns in obj.items() for n in ns]
    return [("?", n) for n in obj]


# ------------------------------------------------------------------------------------------------ main
def run(root, train, dev, devx, templates=None, names=(), golden="data/v14_parts/golden_train.jsonl", strict=False):
    root = Path(root)
    rows = train + dev + devx
    rep = {"rows": {"train": len(train), "dev": len(dev), "devx": len(devx)}, "families": sorted({r["source"] for r in rows})}
    drop = set()
    held, miss_h = held_sets(root)
    h12, unit_sets = check_12(rows, held)
    rep["7.1_heldout_12gram_units"] = h12
    rep["7.1_heldout_hit_units"] = unit_sets
    drop |= set(unit_sets)
    o3_units, o3_hashes, o3_names, o3_loaded = ohs3_blind(root, rows, names)
    rep["7.1_ohs3_hit_units_per_family"] = dict(o3_units)  # COUNTS ONLY
    rep["7.1_ohs3_loaded"] = o3_loaded
    dvs, miss_d = dev_sets(root)
    d12, dunit = check_12(rows, dvs)
    rep["7.2_dev_12gram_units"] = d12
    rep["7.2_dev_hit_units"] = dunit
    drop |= set(dunit)
    rep["missing_reference_files"] = miss_h + miss_d
    items = template_items(rows, templates)
    refs = template_refs(root)
    rep["7.3_reference_runs"] = {k: len(v) for k, v in refs.items()}
    tcount, texamples = check_templates(items, refs)
    rep["7.3_template_clashes"] = tcount
    rep["7.3_template_clash_examples"] = texamples  # yn2b's own template text only
    bw = banned_words(rows)
    rep["7.3_banned_words"] = {f: {"rows": len(v), "words": dict(Counter(w for _, w in v)), "first": v[0][0]}
                               for f, v in bw.items()}
    cs = cue_shares(items)
    rep["7.3_cue_shares"] = cs
    mk = marker_rule(rows)
    rep["7.3_marker_violations"] = {"n": len(mk), "first": mk[:5]}
    dd, drep = dedupe(rows, root / golden if golden else None)
    rep["7.5_dedupe"] = {**drep, "units": len(dd)}
    drop |= dd
    dt, dtrep = dev_vs_train(train, dev + devx)
    rep["7.6_dev_vs_train"] = dtrep
    drop |= dt
    nm = name_check(root, names, strict) if names else {}
    rep["7.7_names"] = {"checked": len(names), "found_in_jevbench_or_ohs12": {f: len(v) for f, v in nm.items()},
                        "examples": {f: v[:5] for f, v in nm.items()}, "ohs3_hash_hits_per_family": dict(o3_names)}
    hashes = {drop_hash(k) for k in drop} | o3_hashes
    fam_drop = Counter(k.split(":", 1)[0] for k in drop)
    rep["dropped_units_per_family_excluding_ohs3"] = dict(fam_drop)
    rep["dropped_units_total_including_ohs3"] = len(hashes)
    fails = []
    if any(tcount.values()):
        fails.append("7.3 template runs shared with a reference set")
    if bw:
        fails.append("7.3 banned words")
    if any(not v["pass"] for v in cs.values()):
        fails.append("7.3 cue share > 60%")
    if mk:
        fails.append("7.3 marker strings outside a marker-spoof attack twin's state")
    if nm or o3_names:
        fails.append("7.7 pool names found in held-out text")
    rep["template_failures"] = fails
    return rep, sorted(hashes)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(yc.LEAN), help="lean/ (tests use a fixture tree)")
    ap.add_argument("--train", default="v14_parts/yn2b_train.jsonl", help="relative to <root>/data")
    ap.add_argument("--dev", default="yn2b_dev.jsonl", help="one file or a comma list (iid,holdout)")
    ap.add_argument("--devx", default="yn2b_devx.jsonl")
    ap.add_argument("--templates", default="", help="JSON list of {family, kind: instruction|plant, text, flips}")
    ap.add_argument("--names", default="", help="JSON {family: [names]} of the generators' name pools")
    ap.add_argument("--golden", default="data/v14_parts/golden_train.jsonl", help="relative to root ('' = skip)")
    ap.add_argument("--strict-substring", action="store_true", help="7.7 as a raw case-insensitive substring test")
    ap.add_argument("--report", required=True, help="report JSON (new file)")
    ap.add_argument("--drop", default="", help="drop list JSON (new file) for assemble_yn2b.py --drop")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    missing = []

    def ld(spec):  # one path, or a comma list (e.g. yn2b_dev_iid.jsonl,yn2b_dev_holdout.jsonl), relative to <root>/data
        out = []
        for p in [x for x in (spec or "").split(",") if x]:
            if not (root / "data" / p).exists():
                missing.append(p)  # reported (inputs_missing), as before an absent file counts as no rows
                continue
            out += yc.read_jsonl(root / "data" / p)
        return out
    train, dev, devx = ld(a.train), ld(a.dev), ld(a.devx)
    tpl = json.loads(Path(a.templates).read_text()) if a.templates else None
    rep, hashes = run(root, train, dev, devx, tpl, load_names(a.names), a.golden, a.strict_substring)
    rep["inputs"] = {"train": a.train, "dev": a.dev, "devx": a.devx, "names": a.names or None}
    rep["inputs_missing"] = missing
    yc.write_json(yc.guard_out(a.report, overwrite=a.overwrite), rep)
    if a.drop:
        yc.write_json(yc.guard_out(a.drop, overwrite=a.overwrite), {"salt": DROP_SALT, "keys": hashes})
    summary = {k: v for k, v in rep.items() if not k.endswith(("_hit_units", "_examples"))}
    print(json.dumps(summary, indent=1))
    if rep["template_failures"]:
        print("TEMPLATE FAILURES: " + "; ".join(rep["template_failures"]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
