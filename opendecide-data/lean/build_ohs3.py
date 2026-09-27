"""OHS-3: merge the held-out parts that passed verification (ohs3/build_*.py -> data/ohs3_parts/*.jsonl), validate,
decontaminate against everything we trained, tuned or selected on, add a small consistency layer (negated-question
twins for yes/no rows, option-order twins for choice rows), split groups into an open half (A, items may be inspected)
and a sealed half (S, aggregates only), then freeze: data/ohs3.jsonl, data/ohs3_relations.jsonl, data/ohs3_calls.jsonl,
data/ohs3_summary.json and data/ohs3.sha256. Commit these BEFORE any model is run on them (see PREREG_OHS3.md).
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python build_ohs3.py

Rules (mirrors build_ohs2.py; the consistency layer mirrors OHS-1 in spirit but uses its own new wordings):
  * parts: every data/ohs3_parts/<part>.jsonl whose part is in PASSED (verifier verdict PASS). A part that is not in
    PASSED is refused, not silently merged.
  * validate: the 14 row keys exactly, split == "ohs3", track in {F, U}, gold in options (choice) or gold in {0,1} with
    options null (yes/no), unique ids, one state per call_id and one call_id per state, 20-6,000 character states, no
    class above 40% of a choice task, every yes/no task exactly 50/50, no normalised state shared by two groups.
  * decontaminate: drop every group whose state equals (after normalisation) or shares a 13-word run with any string
    in our training/dev/eval files: every data/**/*.jsonl except the held-out files (data/ohs*.jsonl, data/ohs_parts/,
    data/ohs2_parts/, data/ohs3_parts/), plus ../data/**/*.jsonl. Every string field is scanned. A state shorter than
    13 words is checked as one run. The held-out OHS-1 / OHS-2 files are never opened here.
  * after decontamination: a yes/no task left unbalanced by drops loses its extra rows of the larger class (last in
    sha256("ohs3-bal:" + id) order); part groups that share any 13-word run inside OHS-3 (near-duplicates such as
    templated notices) are merged into one group (union-find; smallest group_id; meta.part_group_id keeps the original).
  * consistency layer (added AFTER decontamination, only to surviving base rows; no model calls, no LLM-written text):
      - _neg (relation "complement", gold = 1 - gold): 60 yes/no base rows per yes/no task (30 gold 1, 30 gold 0), picked
        by sha256("ohs3-var:" + id) order. The negated question is built from a PRE-WRITTEN proposition per question
        form (PROPS) and either the pre-written clause-negated question of that form (kind "clause_neg") or one of six
        pre-written negation frames over the proposition (NEG_FRAMES, kind "template_neg"), chosen 50/50 by a seeded
        rng per row. Every frame is checked to be new: it may not equal, or share a 6-word run with, any string literal
        of our builders/generators, the OHS-1 variant templates (ohs/variants.py), the wording banks
        (../assets/templates/**.jsonl) or any instruction string in our training/dev/eval files.
      - _perm (relation "equiv", same gold): 38 choice base rows per choice task, picked the same way; options reversed
        or rotated by k in 1..n-1 (seeded per row), so the gold always moves; instructions, state and card unchanged.
      - A twin keeps the base row's group_id (same half, same bootstrap cluster) and gets its own call_id
        "<base call_id>_v", so it is asked in a separate call, exactly as the base row is.
  * halves: group-level, A if int(sha256("ohs3:" + group_id)) is even, else S.
Deterministic, CPU only, no network, no model calls.
"""
import ast
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
D = HERE / "data"
PARTS = D / "ohs3_parts"
EXTRA_DIRS = [ROOT / "data"]  # the pre-lean pipeline's data (opendecide-data/data)
SPLIT = "ohs3"
GRAM = 13
MAX_OPTIONS = 255
MAX_SHARE = 0.40
LEN_RANGE = (20, 6000)
REQUIRED = ["id", "group_id", "call_id", "split", "track", "source", "state", "qtype", "instructions", "options", "gold",
            "role", "card", "meta"]
# verifier verdicts (26 Sep 2026): sec_8k_item FAILED (blocked, no rows), everything below PASSED
PASSED = ["bias_in_bios_profession", "causal_news_corpus", "ct_study_type", "few_nerd_fine", "fewrel_relation",
          "fr_agency", "medrxiv_category", "nvd_attack_vector", "openfda_recall_class", "rosetta_code_language",
          "se_site", "uk_wq_answering_body", "zenodo_resource_type"]
NOT_PASSED = ["sec_8k_item"]

VAR_SEED = 20261003
N_NEG_PER_TASK = 60   # yes/no base rows per yes/no task that get a _neg twin (half gold 1, half gold 0)
N_PERM_PER_TASK = 38  # choice base rows per choice task that get a _perm twin
NOVELTY_K = 6

# ---------------------------------------------------------------------------------------------- consistency wordings
# Pre-written proposition per yes/no question form: (regex over the whole question, proposition p, negated question).
# {0} is the first regex group (the asked Zenodo resource type, kept verbatim with its quotes).
PROPS = [
    (r"Is this sentence causal\?", "this sentence is causal", "Is this sentence not causal?"),
    (r"Is this study interventional\?", "this study is interventional", "Is this study not interventional?"),
    (r"Does the CVSS v3\.1 Attack Vector value in the card apply to this vulnerability\?",
     "the CVSS v3.1 Attack Vector value in the card applies to this vulnerability",
     "Does the CVSS v3.1 Attack Vector value in the card not apply to this vulnerability?"),
    (r"Is this FDA recall classified as Class I\?", "this FDA recall is classified as Class I",
     "Is this FDA recall not classified as Class I?"),
    (r'Does the resource type "([^"]+)" apply to this Zenodo record\?', 'the resource type "{0}" applies to this Zenodo record',
     'Does the resource type "{0}" not apply to this Zenodo record?'),
]
# Negation frames: the answer is yes exactly when p is false. The proposition always closes the clause.
NEG_FRAMES = [
    ("T1", "Would it be an error to maintain that {p}?"),
    ("T2", "Is it incorrect to hold that {p}?"),
    ("T3", "Should one reject the suggestion that {p}?"),
    ("T4", "Is it wrong to assert that {p}?"),
    ("T5", "Would one be mistaken in believing that {p}?"),
    ("T6", "Answer no if {p}, and yes otherwise."),
]

# Unicode-aware (OHS-2 used [^a-z0-9], which erases non-Latin scripts: OHS-3 has Cyrillic, Arabic, ... Zenodo records)
words = lambda t: re.sub(r"[\W_]+", " ", t.casefold()).split()
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def grams(w, n=GRAM):
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def is_heldout(p: Path, root: Path) -> bool:
    parts = [x.lower() for x in p.relative_to(root).parts]
    return parts[0].startswith("ohs") or any(x in ("ohs", "ohs_parts", "ohs2_parts", "ohs3_parts", "bench")
                                             or x.startswith("ohs") for x in parts[:-1])


def touched_files():
    fs = [p for p in sorted(D.rglob("*.jsonl")) if not is_heldout(p, D)]
    for root in EXTRA_DIRS:
        if root.exists():
            fs += [p for p in sorted(root.rglob("*.jsonl")) if not is_heldout(p, root)]
    return fs


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def task_of(r):
    return r["meta"].get("task") or r["source"]


# ---------------------------------------------------------------------------------------------- validation
def validate(rows, base_only=True):
    errs = []
    ids = Counter(r["id"] for r in rows)
    errs += [f"duplicate id {i}" for i, c in ids.items() if c > 1]
    by_call, by_state, by_norm = defaultdict(set), defaultdict(set), defaultdict(set)
    for r in rows:
        if sorted(r) != sorted(REQUIRED):
            errs.append(f"{r.get('id')}: keys {sorted(r)} != the 14 row keys")
            continue
        if r["split"] != SPLIT:
            errs.append(f"{r['id']}: split {r['split']!r}")
        if r["track"] not in ("F", "U"):
            errs.append(f"{r['id']}: track {r['track']!r}")
        if not isinstance(r["meta"], dict):
            errs.append(f"{r['id']}: meta is not a dict")
            continue
        variant = "variant_of" in r["meta"]
        if r["qtype"] == "choice":
            o = r["options"]
            if not (isinstance(o, list) and len(set(o)) == len(o) and 2 <= len(o) <= MAX_OPTIONS and r["gold"] in o):
                errs.append(f"{r['id']}: gold not in options / bad options")
            if r["role"] != "choice":
                errs.append(f"{r['id']}: choice row with role {r['role']!r}")
        elif r["qtype"] == "noul":
            if not (r["gold"] in (0, 1) and not isinstance(r["gold"], bool) and r["options"] is None):
                errs.append(f"{r['id']}: yes/no row needs gold 0/1 and options null")
            if r["role"] != "aff":
                errs.append(f"{r['id']}: yes/no row with role {r['role']!r}")
        else:
            errs.append(f"{r['id']}: qtype {r['qtype']!r}")
        if not (LEN_RANGE[0] <= len(r["state"]) <= LEN_RANGE[1]):
            errs.append(f"{r['id']}: state length {len(r['state'])}")
        if r["card"] is not None and not (isinstance(r["card"], str) and r["card"].strip()
                                          and all(l.startswith("- ") for l in r["card"].split("\n"))):
            errs.append(f"{r['id']}: card must be null or '- <option>: <definition>' lines")
        by_call[r["call_id"]].add(r["state"])
        if not variant:
            by_state[r["state"]].add(r["call_id"])
            by_norm[" ".join(words(r["state"]))].add(r["group_id"])
        elif not r["call_id"].endswith("_v"):
            errs.append(f"{r['id']}: variant call_id must end in _v")
    errs += [f"call_id {c} spans {len(s)} different states" for c, s in by_call.items() if len(s) > 1]
    errs += [f"one state has {len(c)} base call_ids: {sorted(c)}" for s, c in by_state.items() if len(c) > 1]
    errs += [f"normalised state shared by groups {sorted(g)}" for g in by_norm.values() if len(g) > 1]
    # balance (base rows): no class above 40% of a choice task; every yes/no task exactly 50/50
    by_task, qt = defaultdict(Counter), defaultdict(set)
    for r in rows:
        if "variant_of" in r["meta"]:
            continue
        by_task[task_of(r)][str(r["gold"])] += 1
        qt[task_of(r)].add(r["qtype"])
    for t, c in by_task.items():
        if len(qt[t]) != 1:
            errs.append(f"task {t}: mixes qtypes {qt[t]}")
        elif "noul" in qt[t]:
            if c["1"] != c["0"]:
                errs.append(f"task {t}: yes/no balance {dict(c)} is not 50/50")
        elif max(c.values()) > MAX_SHARE * sum(c.values()):
            errs.append(f"task {t}: class share {max(c.values()) / sum(c.values()):.2f} > {MAX_SHARE:.2f}")
    return errs


# ---------------------------------------------------------------------------------------------- decontamination
def decontaminate(rows):
    """Returns ({group_id: reason}, scan stats, instruction strings seen). Index the (small) OHS-3 side, stream ours."""
    full, gram_owner, short = defaultdict(set), defaultdict(set), defaultdict(set)
    short_len_by_first = defaultdict(set)
    for r in rows:
        w = words(r["state"])
        full[" ".join(w)].add(r["group_id"])
        for g in grams(w):
            gram_owner[g].add(r["group_id"])
        if 0 < len(w) < GRAM:  # too short for a 13-word run: the whole state is the run
            short[" ".join(w)].add(r["group_id"])
            short_len_by_first[w[0]].add(len(w))
    hit, seen, nfiles, examples, instr = {}, set(), 0, {}, set()
    for p in touched_files():
        nfiles += 1
        src = str(p.relative_to(ROOT))
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    x = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                if isinstance(x, dict) and isinstance(x.get("instructions"), str):
                    instr.add(x["instructions"])
                for t in strings(x):
                    if len(t) < 20:
                        continue
                    h = hash(t)
                    if h in seen:
                        continue
                    seen.add(h)
                    w = words(t)
                    for g in full.get(" ".join(w), ()):
                        hit.setdefault(g, "exact text"); examples.setdefault(g, src)
                    for i in range(len(w) - GRAM + 1):
                        for g in gram_owner.get(" ".join(w[i:i + GRAM]), ()):
                            hit.setdefault(g, f"shared {GRAM}-word run"); examples.setdefault(g, src)
                    if short:
                        for i, w0 in enumerate(w):
                            for L in short_len_by_first.get(w0, ()):
                                for g in short.get(" ".join(w[i:i + L]), ()):
                                    hit.setdefault(g, "short state contained"); examples.setdefault(g, src)
    return hit, {"files_scanned": nfiles, "unique_texts_scanned": len(seen), "hit_files": examples}, instr


def cross_group_runs(rows):
    """Diagnostic: pairs of different groups inside OHS-3 that share a 13-word run."""
    owner = defaultdict(set)
    for r in rows:
        for g in grams(words(r["state"])):
            owner[g].add(r["group_id"])
    pairs = Counter()
    for gs in owner.values():
        if len(gs) > 1:
            for a in gs:
                for b in gs:
                    if a < b:
                        pairs[(a, b)] += 1
    return pairs


# ---------------------------------------------------------------------------------------------- novelty of wordings
_SLOT = re.compile(r"\{[^{}]*\}|%[sd]")


def _nwords(s):
    return re.sub(r"[^a-z0-9']+", " ", _SLOT.sub(" slot ", s.lower())).split()


def _ngrams(ws, k=NOVELTY_K):
    return {tuple(ws[i:i + k]) for i in range(len(ws) - k + 1)}


def _py_strings(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return []
    out, inner = [], set()
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            out.append("".join(v.value if isinstance(v, ast.Constant) and isinstance(v.value, str) else "{}"
                               for v in node.values))
            inner.update(id(v) for v in node.values)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in inner:
            out.append(node.value)
    return out


def existing_wordings():
    """String literals of every builder/generator (not this file, not the OHS-2/OHS-3 part builders, whose strings
    are held-out source text) + the OHS-1 variant templates + every string in the wording banks."""
    me = Path(__file__).resolve()
    files = sorted(set(HERE.glob("*.py")) | set(HERE.glob("pg/*.py")) | set(ROOT.glob("build/**/*.py"))
                   | set(ROOT.glob("assets/**/*.py")) | set(ROOT.glob("design/**/*.py")) | set(ROOT.glob("*.py"))
                   | {HERE / "ohs" / "variants.py"})
    out = []
    for f in files:
        if f.resolve() == me or ".venv" in f.parts or not f.exists():
            continue
        out += _py_strings(f)
    for f in sorted(ROOT.glob("assets/templates/**/*.jsonl")):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                out += list(strings(json.loads(line)))
    return sorted({s for s in out if _nwords(s)}), len(files)


def check_novelty(existing, instr):
    ex_norm = {tuple(_nwords(s)) for s in existing}
    ex_grams = set()
    for s in existing:
        ex_grams |= _ngrams(_nwords(s))
    in_grams = set()
    for s in instr:
        in_grams |= _ngrams(_nwords(s))
    bad = []
    for tid, t in NEG_FRAMES:
        w = _nwords(t)
        if tuple(w) in ex_norm:
            bad.append((tid, "equal"))
        h = _ngrams(w) & ex_grams
        if h:
            bad.append((tid, " ".join(sorted(h)[0])))
        for frag in _SLOT.split(t):  # fixed fragments vs every train/dev/eval instruction string
            h = _ngrams(_nwords(frag)) & in_grams
            if h:
                bad.append((tid, "instructions: " + " ".join(sorted(h)[0])))
    assert not bad, f"negation frames overlap existing wordings: {bad}"
    # the checker must catch a planted copy of a known train/dev wording
    assert _ngrams(_nwords("Would someone who says that {p} be mistaken?")) & ex_grams, "novelty checker failed a planted collision"
    return {"existing_strings": len(existing), "instruction_strings": len(instr), "k": NOVELTY_K, "overlaps": 0}


# ---------------------------------------------------------------------------------------------- variants
def _rng(*parts):
    return random.Random(int(sha(":".join([str(VAR_SEED), *map(str, parts)]))[:16], 16))


def _order(r):
    return sha("ohs3-var:" + r["id"])


def prop_of(question):
    for rx, p, nq in PROPS:
        m = re.fullmatch(rx, question.strip())
        if m:
            return p.format(*m.groups()), nq.format(*m.groups())
    raise SystemExit(f"no pre-written proposition for yes/no question {question!r}: add it to PROPS")


def _twin(base, suffix, meta_extra, **changes):
    row = {k: base[k] for k in REQUIRED}
    row.update(changes)
    row["id"] = f"{base['id']}_{suffix}"
    row["call_id"] = f"{base['call_id']}_v"
    row["meta"] = {**base["meta"], **meta_extra, "variant_of": base["id"]}
    return row


def make_variants(rows):
    by_task = defaultdict(list)
    for r in rows:
        by_task[task_of(r)].append(r)
    new, rels, picks = [], [], {}
    for t in sorted(by_task):
        rs = sorted(by_task[t], key=_order)
        if rs[0]["qtype"] == "noul":
            chosen = [r for r in rs if r["gold"] == 1][:N_NEG_PER_TASK // 2] + \
                     [r for r in rs if r["gold"] == 0][:N_NEG_PER_TASK // 2]
            for b in sorted(chosen, key=_order):
                p, nq = prop_of(b["instructions"])
                rr = _rng("neg", b["id"])
                if rr.random() < 0.5:
                    ins, kind, tid = nq, "clause_neg", "C0"
                else:
                    tid, tpl = rr.choice(NEG_FRAMES)
                    ins, kind = tpl.format(p=p), "template_neg"
                row = _twin(b, "neg", instructions=ins, gold=1 - b["gold"],
                            meta_extra={"variant_kind": kind, "template_id": tid, "prop": p})
                new.append(row)
                rels.append({"type": "complement", "a": b["id"], "b": row["id"]})
        else:
            chosen = rs[:N_PERM_PER_TASK]
            for b in sorted(chosen, key=_order):
                o = list(b["options"])
                rr = _rng("perm", b["id"])
                if rr.random() < 0.5:
                    o2, kind = o[::-1], "reverse"
                else:
                    k = rr.randrange(1, len(o))
                    o2, kind = o[k:] + o[:k], f"rotate:{k}"
                assert sorted(o2) == sorted(o) and o2.index(b["gold"]) != o.index(b["gold"]), b["id"]
                row = _twin(b, "perm", options=o2,
                            meta_extra={"variant_kind": "option_order", "perm": kind,
                                        "gold_pos_base": o.index(b["gold"]), "gold_pos_twin": o2.index(b["gold"])})
                new.append(row)
                rels.append({"type": "equiv", "a": b["id"], "b": row["id"]})
        picks[t] = len(chosen)
    return new, rels, picks


def label_source(ps):
    for k in ("label_definitions_source", "label_definition_source", "labels_source", "label_definitions"):
        if isinstance(ps.get(k), str):
            return ps[k]
    return "per-label sources: see the part summary" if ps.get("label_definitions") else None


# ---------------------------------------------------------------------------------------------- main
def main():
    found = sorted(f.stem for f in PARTS.glob("*.jsonl"))
    unknown = [p for p in found if p not in PASSED]
    if unknown:
        sys.exit(f"parts without a PASS verdict found in {PARTS}: {unknown}")
    missing = [p for p in PASSED if p not in found]
    if missing:
        sys.exit(f"passed parts missing: {missing}")
    rows, part_files, part_summ = [], {}, {}
    for name in PASSED:
        f = PARTS / f"{name}.jsonl"
        text = f.read_text(encoding="utf-8")
        part_files[f.name] = sha(text)
        for l in text.splitlines():
            if l.strip():
                r = json.loads(l)
                r["meta"].setdefault("part", name)
                rows.append(r)
        sp = PARTS / f"{name}_summary.json"
        if sp.exists():
            part_summ[name] = json.loads(sp.read_text())
    n_in = len(rows)
    errs = validate(rows)
    if errs:
        print("VALIDATION FAILED:\n  " + "\n  ".join(errs[:50]))
        sys.exit(1)
    if cross_group_runs(rows):
        print(f"info: {len(cross_group_runs(rows))} pairs of part groups share a {GRAM}-word run inside OHS-3 "
              "(merged into clusters after decontamination)")

    hit, scan, instr = decontaminate(rows)
    dropped = [{"group_id": g, "reason": hit[g], "first_file": scan["hit_files"][g],
                "rows": sorted(r["id"] for r in rows if r["group_id"] == g)} for g in sorted(hit)]
    rows = [r for r in rows if r["group_id"] not in hit]
    for d in dropped:
        print("dropped for overlap:", d)
    # dropping whole groups may unbalance a yes/no task: re-balance by dropping the extra rows of the larger class,
    # last in sha256("ohs3-bal:" + id) order (deterministic, label-blind within a class)
    rebalanced = []
    by_task = defaultdict(list)
    for r in rows:
        by_task[task_of(r)].append(r)
    for t, rs in by_task.items():
        if rs[0]["qtype"] != "noul":
            continue
        c = Counter(r["gold"] for r in rs)
        if c[1] != c[0]:
            big = 1 if c[1] > c[0] else 0
            extra = sorted([r for r in rs if r["gold"] == big], key=lambda r: sha("ohs3-bal:" + r["id"]))[-(abs(c[1] - c[0])):]
            rebalanced += [r["id"] for r in extra]
    rows = [r for r in rows if r["id"] not in set(rebalanced)]

    # near-duplicate clustering: groups that share any 13-word run (templated Federal Register notices, recall
    # batches, ...) are merged into one group (group_id = smallest member group_id; the part's own group_id is kept in
    # meta.part_group_id), so they fall in the same half and are resampled together by the group bootstrap
    pairs = cross_group_runs(rows)
    parent = {}

    def find(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x
    task_of_group = {r["group_id"]: task_of(r) for r in rows}
    for a, b in sorted(pairs):
        assert task_of_group[a] == task_of_group[b], f"cross-task shared run {a} {b}"
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    clusters = defaultdict(set)
    for r in rows:
        g = find(r["group_id"])
        clusters[g].add(r["group_id"])
        r["meta"]["part_group_id"] = r["group_id"]
        r["group_id"] = g
    merged = {g: sorted(m) for g, m in sorted(clusters.items()) if len(m) > 1}

    # consistency layer
    existing, n_src_files = existing_wordings()
    novelty = check_novelty(existing, instr)
    new, rels, picks = make_variants(rows)
    base_rows = rows
    rows = base_rows + new
    errs = validate(rows)
    if errs:
        print("VALIDATION FAILED after variants:\n  " + "\n  ".join(errs[:50]))
        sys.exit(1)
    ids = {r["id"] for r in rows}
    assert all(x["a"] in ids and x["b"] in ids for x in rels)

    # open / sealed halves by group hash (twins share their base row's group, so they share its half)
    for r in rows:
        r["meta"]["half"] = "A" if int(sha("ohs3:" + r["group_id"]), 16) % 2 == 0 else "S"
    calls = {}
    for r in rows:
        calls.setdefault(r["call_id"], {"call_id": r["call_id"], "state": r["state"], "row_ids": []})["row_ids"].append(r["id"])

    files = {"ohs3.jsonl": rows, "ohs3_relations.jsonl": rels, "ohs3_calls.jsonl": list(calls.values())}
    hashes = {}
    for name, items in files.items():
        text = "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in items)
        (D / name).write_text(text, encoding="utf-8")
        hashes[name] = sha(text)

    # summary
    tasks = {}
    bt = defaultdict(list)
    for r in base_rows:
        bt[task_of(r)].append(r)
    nvar = Counter(task_of(r) for r in new)
    for t in sorted(bt):
        rs = bt[t]
        bal = Counter(str(r["gold"]) for r in rs)
        r0 = rs[0]
        ps = part_summ.get(r0["meta"]["part"], {})
        aw = ps.get("author_written_definitions")
        tasks[t] = {
            "part": r0["meta"]["part"], "source": r0["source"], "qtype": r0["qtype"],
            "track": dict(sorted(Counter(r["track"] for r in rs).items())),
            "n": len(rs), "groups": len({r["group_id"] for r in rs}),
            "n_options": sorted({len(r["options"]) for r in rs if r["options"]}) or [2],
            "balance_n_classes": len(bal), "max_class_share": round(max(bal.values()) / len(rs), 3),
            "licence": (ps.get("licence") or ps.get("license") or ps.get("row_licence_counts") or r0["meta"].get("licence")
                        or r0["meta"].get("license")),
            "author_written_definitions": sorted(aw) if isinstance(aw, (dict, list)) and aw else [],
            "label_definitions_source": label_source(ps),
            "rows_with_card": sum(bool(r["card"]) for r in rs),
            "variant_rows": nvar.get(t, 0),
            "halves_rows": dict(sorted(Counter(r["meta"]["half"] for r in rs).items())),
        }
    groups = {r["group_id"]: r["meta"]["half"] for r in rows}
    summ = {
        "benchmark": "OHS-3", "split": SPLIT, "parts_passed": PASSED, "parts_not_passed": NOT_PASSED,
        "rows_in": n_in, "rows": len(rows), "base_rows": len(base_rows), "variant_rows": len(new),
        "relations": dict(Counter(x["type"] for x in rels)), "calls": len(calls), "base_calls": len({r["call_id"] for r in base_rows}),
        "groups": len(groups), "tasks": len(tasks), "dropped_for_overlap": dropped,
        "dropped_to_rebalance_yes_no": rebalanced,
        "by_part_base": dict(Counter(r["meta"]["part"] for r in base_rows)),
        "by_track_base": dict(sorted(Counter(r["track"] for r in base_rows).items())),
        "by_qtype_base": dict(sorted(Counter(r["qtype"] for r in base_rows).items())),
        "yes_no_base_rows": sum(r["qtype"] == "noul" for r in base_rows),
        "choice_base_rows_over_26_options": sum(r["qtype"] == "choice" and len(r["options"]) > 26 for r in base_rows),
        "halves": {"base_rows": dict(sorted(Counter(r["meta"]["half"] for r in base_rows).items())),
                   "all_rows": dict(sorted(Counter(r["meta"]["half"] for r in rows).items())),
                   "groups": dict(sorted(Counter(groups.values()).items()))},
        "max_options": max(len(r["options"] or [0, 1]) for r in rows),
        "state_chars": {"min": min(len(r["state"]) for r in rows), "max": max(len(r["state"]) for r in rows)},
        "consistency_layer": {
            "seed": VAR_SEED, "picked_per_task": picks,
            "neg_kinds": dict(sorted(Counter(r["meta"]["variant_kind"] for r in new if r["id"].endswith("_neg")).items())),
            "neg_templates": dict(sorted(Counter(r["meta"]["template_id"] for r in new if r["id"].endswith("_neg")).items())),
            "perm_kinds": dict(sorted(Counter(r["meta"]["perm"].split(":")[0] for r in new if r["id"].endswith("_perm")).items())),
            "neg_frames": dict(NEG_FRAMES), "props": [[rx, p, nq] for rx, p, nq in PROPS],
            "novelty_check": {**novelty, "source_files": n_src_files},
            "twin_call_rule": "each twin is its own call (<base call_id>_v); twins share their base row's group_id",
        },
        "decontamination": {"files_scanned": scan["files_scanned"], "unique_texts_scanned": scan["unique_texts_scanned"],
                            "rule": f"normalised exact state or shared {GRAM}-word run (whole state if under {GRAM} words) "
                                    "with any string in data/**/*.jsonl minus held-out files (data/ohs*, ohs_parts, "
                                    "ohs2_parts, ohs3_parts), and ../data/**/*.jsonl",
                            f"cross_group_{GRAM}gram_pairs_inside_ohs3": [[a, b, n] for (a, b), n in sorted(pairs.items())],
                            "merged_groups": merged,
                            "merge_rule": f"part groups sharing any {GRAM}-word run are merged into one group "
                                          "(union-find; group_id = smallest member; meta.part_group_id keeps the original)"},
        "per_task": tasks, "part_files_sha256": part_files, "sha256": hashes,
    }
    stext = json.dumps(summ, indent=1, ensure_ascii=False) + "\n"
    (D / "ohs3_summary.json").write_text(stext, encoding="utf-8")
    hashes["ohs3_summary.json"] = sha(stext)
    (D / "ohs3.sha256").write_text("".join(f"{h}  {n}\n" for n, h in hashes.items()))
    brief = {k: summ[k] for k in ("rows", "base_rows", "variant_rows", "relations", "calls", "groups", "tasks",
                                  "by_track_base", "by_qtype_base", "halves", "max_options")}
    brief["dropped_for_overlap"] = len(dropped)
    brief["dropped_to_rebalance_yes_no"] = len(rebalanced)
    brief["cross_group_pairs"] = len(pairs)
    brief["merged_clusters"] = len(merged)
    brief["rows_in_merged_clusters"] = sum(len(m) for m in merged.values())
    brief["decontamination"] = {k: v for k, v in summ["decontamination"].items() if not k.startswith("cross_group")}
    brief["consistency_layer"] = {k: summ["consistency_layer"][k] for k in ("neg_kinds", "neg_templates", "perm_kinds")}
    print(json.dumps(brief, indent=1))


if __name__ == "__main__":
    main()
