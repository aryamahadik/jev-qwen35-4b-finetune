"""A17 clean practice sets for the think mode, from the public TRAIN / validation splits named in
reports/knowledge_gap/PLAN_knowledge_gap.md section 4 ("Clean validation sets"), in our row format. CPU, no model.

  set          source (split only)                                  licence       role (plan section 4)
  k_mmlu       cais/mmlu all: validation + dev (1,816)              MIT           paired no-harm guard; DI-adjacent
  k_arc        allenai/ai2_arc Challenge + Easy: train + validation CC-BY-SA-4.0  paired no-harm guard
  k_sci        m-a-p/SuperGPQA (its only split, train), Science,    ODC-BY        paired comparisons only
               middle + hard, 2,000 sampled, 4 options (gold + 3 distractors, fixed seed)
  k_sci2  (*)  TIGER-Lab/MMLU-Pro, non-MMLU parts only (src not ori_mmlu), 2,000 sampled, 10 options; MIT
               its big split is named "test" -> NOT a train/validation split: needs an owner ruling (--allow k_sci2)
  k_gsm8k (*)  openai/gsm8k main train, 2,000 sampled, 4 options (our distractor recipe, gold not centred); MIT;
               not listed in the clean-set table and DI-adjacent (C spec): needs an owner ruling (--allow k_gsm8k)
  (*) off by default. K-Math / K-Code / K-Causal (Claude- or program-written) and K-Skip are not public splits; a
  finished file in our row format can be added with --extra name=path.
Never: MMLU-Redux, MMMLU, GSM-Plus/Hard/Symbolic, MGSM, CRUXEval-X, SciQ, OpenBookQA, PIQA, TriviaQA, GPQA
extended, any test split of a DI benchmark (only the named split files are downloaded; test files are never fetched).

Row: {"id": "<set>:<native id>", "qtype": "choice", "state": question, "instructions": INSTR, "options": [...],
"gold": option text, "source", "set", "think_type" (math|code|science|knowledge, from the dataset's own subject
field; for reporting and the B1 maths rule, never a router input), "group_id", "split": dev_fit|dev_confirm
(60/40, common.split_of), "track": "THINK_CLEAN", "meta"}.
Steps (A17: overlap is checked counts-only BEFORE any model reads a row):
  python think/clean_sets.py build [--allow k_sci2,k_gsm8k] [--extra k_math=path]  -> data/clean/<set>.candidates.jsonl
  python think/check_overlap_di.py ... (orchestrator; counts only)                  -> data/clean/overlap_drop_ids.json
  python think/clean_sets.py finalize                                              -> data/clean/<set>.jsonl + manifest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import read_jsonl, sha256_file, split_of, write_jsonl  # noqa: E402

OUT = HERE / "data" / "clean"
INSTR = "Which option correctly answers the question in the text?"
N_SAMPLE = 2000
SEED = "think-clean-a17"
# (repo, [files], licence). Only these split files are ever downloaded.
SOURCES = {
    "k_mmlu": ("cais/mmlu", ["all/validation-00000-of-00001.parquet", "all/dev-00000-of-00001.parquet"], "MIT"),
    "k_arc": ("allenai/ai2_arc", [f"ARC-{c}/{s}-00000-of-00001.parquet" for c in ("Challenge", "Easy")
                                  for s in ("train", "validation")], "CC-BY-SA-4.0"),
    "k_sci": ("m-a-p/SuperGPQA", ["SuperGPQA-all.jsonl"], "ODC-BY"),
    "k_sci2": ("TIGER-Lab/MMLU-Pro", ["data/test-00000-of-00001.parquet", "data/validation-00000-of-00001.parquet"],
               "MIT"),
    "k_gsm8k": ("openai/gsm8k", ["main/train-00000-of-00001.parquet"], "MIT"),
}
DEFAULT = ("k_mmlu", "k_arc", "k_sci")
NEEDS_RULING = ("k_sci2", "k_gsm8k")
MMLU_MATH = {"abstract_algebra", "college_mathematics", "elementary_mathematics", "high_school_mathematics",
             "high_school_statistics"}
MMLU_CODE = {"college_computer_science", "high_school_computer_science"}
MMLU_SCI = {"anatomy", "astronomy", "college_biology", "college_chemistry", "college_physics", "conceptual_physics",
            "electrical_engineering", "high_school_biology", "high_school_chemistry", "high_school_physics",
            "medical_genetics", "virology", "nutrition", "clinical_knowledge", "college_medicine"}
FORBIDDEN_FILES = re.compile(r"(^|/)test-|/test/|auxiliary_train", re.I)


def _rng(*parts) -> random.Random:
    return random.Random(int(hashlib.sha256(":".join(map(str, (SEED,) + parts)).encode()).hexdigest()[:16], 16))


def fetch(repo, fname, allow_test=False):
    """Download ONE named split file (Hugging Face cache). A test-split file is refused unless the set is ruled in."""
    if FORBIDDEN_FILES.search(fname) and not allow_test:
        raise SystemExit(f"refused: {repo}/{fname} is a test split")
    from huggingface_hub import hf_hub_download
    p = hf_hub_download(repo, fname, repo_type="dataset")
    m = re.search(r"/snapshots/([0-9a-f]{40})/", p)
    return Path(p), (m.group(1) if m else None)


def records(path) -> list:
    path = Path(path)
    if path.suffix == ".parquet":
        import pyarrow.parquet as pq
        return pq.read_table(path).to_pylist()
    return list(read_jsonl(path))


def make_row(set_name, nid, question, options, gold_idx, source, think_type, meta):
    """Our row, or None when the item cannot be a clean single-answer choice (empty / duplicate options, > 26)."""
    opts = [re.sub(r"\s+", " ", str(o)).strip() for o in options]
    q = str(question or "").strip()
    if not q or len(opts) < 2 or len(opts) > 26 or any(not o for o in opts) or len(set(opts)) < len(opts):
        return None
    if not (0 <= gold_idx < len(opts)):
        return None
    rid = f"{set_name}:{nid}"
    return {"id": rid, "qtype": "choice", "state": q, "instructions": INSTR, "options": opts, "gold": opts[gold_idx],
            "source": source, "set": set_name, "think_type": think_type, "group_id": rid,
            "split": split_of(rid), "track": "THINK_CLEAN", "meta": meta, "card": None}


def sample_ids(items, key, n, tag):
    """Deterministic sample of n items: the n smallest sha256(seed, tag, id)."""
    if len(items) <= n:
        return items
    rank = lambda x: hashlib.sha256(f"{SEED}:{tag}:{key(x)}".encode()).hexdigest()
    return sorted(items, key=rank)[:n]


def conv_mmlu(recs, hf_split):
    out = []
    for i, r in enumerate(recs):
        s = r["subject"]
        tt = "math" if s in MMLU_MATH else "code" if s in MMLU_CODE else "science" if s in MMLU_SCI else "knowledge"
        out.append(make_row("k_mmlu", f"{hf_split}:{s}:{i}", r["question"], r["choices"], int(r["answer"]),
                            "cais/mmlu", tt, {"subject": s, "hf_split": hf_split}))
    return out


def conv_arc(recs, cfg, hf_split):
    out = []
    for r in recs:
        lab = list(r["choices"]["label"])
        if r["answerKey"] not in lab:
            continue
        out.append(make_row("k_arc", f"{cfg}:{r['id']}", r["question"], r["choices"]["text"], lab.index(r["answerKey"]),
                            f"allenai/ai2_arc/{cfg}", "science", {"config": cfg, "hf_split": hf_split}))
    return out


def conv_sci(recs):
    pool = [r for r in recs if r.get("discipline") == "Science" and r.get("difficulty") in ("middle", "hard")]
    out = []
    for r in sample_ids(pool, lambda x: x["uuid"], N_SAMPLE, "k_sci"):
        opts = list(r["options"])
        if r.get("answer") not in opts:
            continue
        g = opts.index(r["answer"])
        rng = _rng("k_sci", r["uuid"])
        four = [opts[g]] + rng.sample([o for i, o in enumerate(opts) if i != g], 3)
        rng.shuffle(four)
        tt = "math" if r.get("field") == "Mathematics" else "science"
        out.append(make_row("k_sci", r["uuid"], r["question"], four, four.index(opts[g]), "m-a-p/SuperGPQA", tt,
                            {"field": r.get("field"), "subfield": r.get("subfield"), "difficulty": r.get("difficulty"),
                             "hf_split": "train", "options_original": len(opts)}))
    return out


def conv_sci2(recs):
    pool = [r for r in recs if not str(r.get("src", "")).startswith("ori_mmlu")]
    out = []
    for r in sample_ids(pool, lambda x: x["question_id"], N_SAMPLE, "k_sci2"):
        opts = [o for o in r["options"] if str(o).strip() and str(o).strip() != "N/A"]
        gold = r["options"][int(r["answer_index"])]
        if gold not in opts:
            continue
        c = r.get("category", "")
        tt = ("math" if c == "math" else "code" if c == "computer science" else
              "science" if c in ("physics", "chemistry", "biology", "engineering", "health") else "knowledge")
        out.append(make_row("k_sci2", r["question_id"], r["question"], opts, opts.index(gold), "TIGER-Lab/MMLU-Pro", tt,
                            {"category": c, "src": r.get("src"), "hf_split": "test (ruling)"}))
    return out


def _fmt(x) -> str:
    return str(int(x)) if float(x).is_integer() else f"{x:.2f}".rstrip("0").rstrip(".")


def gsm8k_options(gold: float, rid: str):
    """4 options, our recipe (not DI's): 3 distinct positive distractors from fixed perturbations of the answer,
    then the gold placed at a uniform position (so it is not centred)."""
    rng = _rng("k_gsm8k", rid)
    cand = [gold + 1, gold - 1, gold * 2, gold + 10, gold - 10, round(gold * 1.5), gold * 10, gold + 2]
    if float(gold).is_integer() and gold % 2 == 0:
        cand.append(gold / 2)
    seen, pool = {gold}, []
    for c in cand:
        if c > 0 and c not in seen:
            seen.add(c)
            pool.append(c)
    rng.shuffle(pool)
    k = 3
    while len(pool) < 3:
        k += 1
        if gold + k not in seen:
            seen.add(gold + k)
            pool.append(gold + k)
    opts = [_fmt(c) for c in pool[:3]]
    pos = rng.randrange(4)
    opts.insert(pos, _fmt(gold))
    return opts, pos


def conv_gsm8k(recs):
    items = [dict(r, _i=i) for i, r in enumerate(recs)]
    out = []
    for r in sample_ids(items, lambda x: x["_i"], N_SAMPLE, "k_gsm8k"):
        m = re.search(r"####\s*(-?[\d,]*\.?\d+)", r["answer"])
        if not m:
            continue
        g = float(m.group(1).replace(",", ""))
        rid = f"train:{r['_i']}"
        opts, pos = gsm8k_options(g, rid)
        out.append(make_row("k_gsm8k", rid, r["question"], opts, pos, "openai/gsm8k", "math",
                            {"hf_split": "train (ruling, DI-adjacent)"}))
    return out


def convert(name, files: list) -> list:
    """files: [(file name, records)] of one set."""
    if name == "k_mmlu":
        return [x for f, rs in files for x in conv_mmlu(rs, f.split("/")[1].split("-")[0])]
    if name == "k_arc":
        return [x for f, rs in files for x in conv_arc(rs, f.split("/")[0], f.split("/")[1].split("-")[0])]
    allr = [r for _, rs in files for r in rs]
    return {"k_sci": conv_sci, "k_sci2": conv_sci2, "k_gsm8k": conv_gsm8k}[name](allr)


REQUIRED = ("id", "qtype", "state", "instructions", "options", "gold")


def cmd_build(a):
    allow = [s for s in (a.allow or "").split(",") if s]
    bad = [s for s in allow if s not in NEEDS_RULING]
    if bad:
        raise SystemExit(f"--allow takes only {NEEDS_RULING}, got {bad}")
    OUT.mkdir(parents=True, exist_ok=True)
    man = {"instructions": INSTR, "seed": SEED, "n_sample": N_SAMPLE, "sets": {}}
    for name in list(DEFAULT) + allow:
        repo, fnames, lic = SOURCES[name]
        files, revs = [], {}
        for fn in fnames:
            p, rev = fetch(repo, fn, allow_test=name in allow)
            files.append((fn, records(p)))
            revs[fn] = rev
        rows = convert(name, files)
        kept, ids = [], set()
        for r in rows:
            if r is not None and r["id"] not in ids:
                ids.add(r["id"])
                kept.append(r)
        _write_set(man, name, kept, {"repo": repo, "files": revs, "licence": lic,
                                     "raw_rows": sum(len(rs) for _, rs in files), "invalid_or_dup": len(rows) - len(kept),
                                     "ruling_needed": name in NEEDS_RULING})
    for spec in a.extra or []:
        name, path = spec.split("=", 1)
        rows = list(read_jsonl(path))
        miss = [k for k in REQUIRED if any(k not in r for r in rows)]
        if miss:
            raise SystemExit(f"--extra {name}: rows lack {miss}")
        for r in rows:
            r.setdefault("set", name)
            r.setdefault("split", split_of(r["id"]))
            r.setdefault("track", "THINK_CLEAN")
        _write_set(man, name, rows, {"repo": "extra", "files": {path: sha256_file(path)}, "licence": "ours"})
    (OUT / "build_manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    print(json.dumps({k: {x: v[x] for x in ("rows", "candidates_sha256")} for k, v in man["sets"].items()}, indent=1))
    print("NEXT (orchestrator, counts only): python think/check_overlap_di.py --candidates think/data/clean "
          "[--ref name=path ...]   then: python think/clean_sets.py finalize")


def _write_set(man, name, rows, info):
    f = OUT / f"{name}.candidates.jsonl"
    write_jsonl(f, rows)
    tt = {}
    for r in rows:
        tt[r.get("think_type", "other")] = tt.get(r.get("think_type", "other"), 0) + 1
    man["sets"][name] = {**info, "rows": len(rows), "think_type": tt, "candidates_sha256": sha256_file(f)}


def _ids_sha(ids) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()


def cmd_finalize(a):
    """Apply the counts-only overlap drops; freeze each set and its dev_fit / dev_confirm id lists (sha256)."""
    build = json.loads((OUT / "build_manifest.json").read_text())
    ov_p = Path(a.overlap or OUT / "overlap_drop_ids.json")
    if not ov_p.exists():
        raise SystemExit(f"{ov_p} is missing: run check_overlap_di.py first (A17: overlap before any read)")
    ov = json.loads(ov_p.read_text())
    man = {"overlap_file": str(ov_p), "overlap_sha256": sha256_file(ov_p), "refs": ov.get("refs"), "sets": {}}
    for name, info in build["sets"].items():
        cf = OUT / f"{name}.candidates.jsonl"
        if ov.get("candidates", {}).get(name) != sha256_file(cf):
            raise SystemExit(f"{name}: the overlap check did not run on the current candidates (sha256 differs)")
        drop = set(ov.get("drop_ids", {}).get(name, []))
        rows = [r for r in read_jsonl(cf) if r["id"] not in drop]
        f = OUT / f"{name}.jsonl"
        write_jsonl(f, rows)
        fit = [r["id"] for r in rows if r["split"] == "dev_fit"]
        con = [r["id"] for r in rows if r["split"] == "dev_confirm"]
        tt = {}
        for r in rows:
            tt[r.get("think_type", "other")] = tt.get(r.get("think_type", "other"), 0) + 1
        man["sets"][name] = {"rows": len(rows), "dropped_overlap": len(drop), "dev_fit": len(fit),
                             "dev_confirm": len(con), "think_type": tt, "sha256": sha256_file(f),
                             "dev_fit_ids_sha256": _ids_sha(fit), "dev_confirm_ids_sha256": _ids_sha(con),
                             "ruling_needed": info.get("ruling_needed", False), "licence": info.get("licence")}
    (OUT / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    print(json.dumps({k: {x: v[x] for x in ("rows", "dropped_overlap", "dev_fit", "dev_confirm")}
                      for k, v in man["sets"].items()}, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("--allow", default="", help=f"comma list from {NEEDS_RULING}; only with an owner ruling")
    p.add_argument("--extra", action="append", help="name=path of a finished row-format set (e.g. K-Math)")
    p.set_defaults(func=cmd_build)
    p = sub.add_parser("finalize")
    p.add_argument("--overlap", default=None)
    p.set_defaults(func=cmd_finalize)
    a = ap.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
