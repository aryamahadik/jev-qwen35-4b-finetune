"""A30 (B1b): the frozen clean maths set of the B1 rules = GSM8K TRAIN, a seeded 500 (A17-B1), plus the public
reference files of its counts-only overlap check. CPU only; no model reads anything here.

  python think/b1b_sets.py build      # all GSM8K main/train rows in our 4-option format (clean_sets.py k_gsm8k
                                      # recipe, unchanged) -> data/clean_b1b/gsm8k_train.candidates.jsonl
  python think/b1b_sets.py refs       # public full test / held-out sets -> data/public_refs/ (git-ignored); counts only
  python think/check_overlap_di.py --candidates think/data/clean_b1b --ref ...   (see refs output: the exact command)
  python think/b1b_sets.py finalize   # drop overlap hits, take the 500 smallest sha256(SEED:b1b_math500:id) ->
                                      # data/clean_b1b/{gsm8k_train500.jsonl, manifest.json}  (eval_think --clean)
                                      # + data/b1b_math500.jsonl (Modal input: NO gold) + data/b1b_math500_manifest.json

Selection (fixed in A30 before any model reads a row): rank every GSM8K train row that survives the overlap check by
sha256(f"{clean_sets.SEED}:b1b_math500:{id}") ascending; the first 500 are the set. think_type "math" for all.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import clean_sets as cs  # noqa: E402
from common import read_jsonl, sha256_file, write_jsonl  # noqa: E402

OUT = HERE / "data" / "clean_b1b"
REFS = HERE / "data" / "public_refs"
CAND = OUT / "gsm8k_train.candidates.jsonl"
SET = "gsm8k_train500"
N = 500
TAG = "b1b_math500"
MODAL_IN = HERE / "data" / "b1b_math500.jsonl"
MODAL_MAN = HERE / "data" / "b1b_math500_manifest.json"
# (name, repo, file, kind). Public full test / held-out splits only; csv is converted to jsonl (text never printed).
PUBLIC = [("gsm8k_test", "openai/gsm8k", "main/test-00000-of-00001.parquet", "copy"),
          ("mmlu_test", "cais/mmlu", "all/test-00000-of-00001.parquet", "copy"),
          ("cruxeval", "cruxeval-org/cruxeval", "test.jsonl", "copy"),
          ("arc_c_test", "allenai/ai2_arc", "ARC-Challenge/test-00000-of-00001.parquet", "copy"),
          ("arc_e_test", "allenai/ai2_arc", "ARC-Easy/test-00000-of-00001.parquet", "copy"),
          ("cladder", "causal-nlp/CLadder", "data/full_v1.5_default.csv", "csv"),
          ("gpqa_all", "Idavidrein/gpqa", "gpqa_extended.csv", "csv")]  # extended = superset of main and diamond
LOCAL_REFS = {"ohs1": HERE.parent / "data" / "ohs.jsonl", "ohs2": HERE.parent / "data" / "ohs2.jsonl"}  # never ohs3


def rank(rid: str) -> str:
    return hashlib.sha256(f"{cs.SEED}:{TAG}:{rid}".encode()).hexdigest()


def gsm8k_rows(recs) -> list:
    """Every GSM8K train record as our row, with clean_sets.py's k_gsm8k recipe (ids train:<index>)."""
    out = []
    for i, r in enumerate(recs):
        m = cs.re.search(r"####\s*(-?[\d,]*\.?\d+)", r["answer"])
        if not m:
            continue
        g = float(m.group(1).replace(",", ""))
        rid = f"train:{i}"
        opts, pos = cs.gsm8k_options(g, rid)
        row = cs.make_row("k_gsm8k", rid, r["question"], opts, pos, "openai/gsm8k", "math",
                          {"hf_split": "train (A17-B1 ruling: in, for the B1/B2 maths rule)"})
        if row is not None:
            out.append(row)
    return out


def cmd_build(_a):
    repo, files, lic = cs.SOURCES["k_gsm8k"]
    p, rev = cs.fetch(repo, files[0])
    rows = gsm8k_rows(cs.records(p))
    OUT.mkdir(parents=True, exist_ok=True)
    write_jsonl(CAND, rows)
    man = {"set": "gsm8k_train (all rows, candidates)", "repo": repo, "file": files[0], "revision": rev, "licence": lic,
           "recipe": "clean_sets.gsm8k_options + make_row (k_gsm8k)", "rows": len(rows),
           "candidates_sha256": sha256_file(CAND)}
    (OUT / "build_manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    print(json.dumps({k: man[k] for k in ("rows", "revision", "candidates_sha256")}))


def cmd_refs(_a):
    from huggingface_hub import hf_hub_download
    REFS.mkdir(parents=True, exist_ok=True)
    got, args = {}, []
    for name, repo, fn, kind in PUBLIC:
        try:
            src = Path(hf_hub_download(repo, fn, repo_type="dataset"))
        except Exception as e:  # noqa: BLE001  (gated / missing: reported, the check runs without it)
            got[name] = f"UNAVAILABLE ({type(e).__name__})"
            continue
        d = REFS / name
        d.mkdir(exist_ok=True)
        if kind == "csv":
            with open(src, newline="", encoding="utf-8") as f:
                n = write_jsonl(d / (Path(fn).stem + ".jsonl"), list(csv.DictReader(f)))
        else:
            dst = d / Path(fn).name
            dst.write_bytes(src.read_bytes())
            n = "file"
        got[name] = {"repo": repo, "file": fn, "items": n}
        args.append(f"--ref {name}={d}")
    for name, p in LOCAL_REFS.items():
        if p.exists():
            args.append(f"--ref {name}={p}")
            got[name] = {"local": str(p)}
    (REFS / "refs_manifest.json").write_text(json.dumps(got, indent=1) + "\n")
    print(json.dumps({k: (v if isinstance(v, str) else "ok") for k, v in got.items()}))
    print("NEXT: ../.venv/bin/python think/check_overlap_di.py --candidates think/data/clean_b1b " + " ".join(args))


def select(rows: list, drop: set, n: int = N) -> list:
    keep = [r for r in rows if r["id"] not in drop]
    return sorted(keep, key=lambda r: rank(r["id"]))[:n]


def modal_items(rows: list, tp) -> list:
    """Gold-free Modal input in the squad2_parity100.jsonl format (id, row, info, letters, user, user_sha256)."""
    preps = {p["id"]: p for p in tp.prepare([{"id": r["id"], "row": r} for r in rows])}
    out = []
    for r in rows:
        p = preps[r["id"]]
        row = {k: r[k] for k in ("id", "state", "instructions", "qtype", "options", "card")}
        out.append({"id": r["id"], "row": row, "info": p["info"], "letters": p["letters"], "user": p["user"],
                    "user_sha256": hashlib.sha256(p["user"].encode()).hexdigest()})
    return out


def _think_path():
    import decoder_io as dio
    import think_engine as te
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(te_base()[0], revision=te_base()[1], local_files_only=True)
    return te.ThinkPath(te.FakeBackend(), tok, dio)


def te_base():
    return "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"


def cmd_finalize(a):
    ov_p = OUT / "overlap_drop_ids.json"
    if not ov_p.exists():
        raise SystemExit(f"{ov_p} missing: run check_overlap_di.py first (A17: overlap before any read)")
    ov = json.loads(ov_p.read_text())
    cname = CAND.name[: -len(".candidates.jsonl")]
    if ov.get("candidates", {}).get(cname) != sha256_file(CAND):
        raise SystemExit("the overlap check did not run on the current candidates (sha256 differs)")
    drop = set(ov["drop_ids"].get(cname, []))
    rows = select(list(read_jsonl(CAND)), drop)
    if len(rows) != N:
        raise SystemExit(f"only {len(rows)} rows after the overlap drops")
    for r in rows:
        r["set"] = SET
    f = OUT / f"{SET}.jsonl"
    write_jsonl(f, rows)
    ids = sorted(r["id"] for r in rows)
    man = {"rule": "A30: GSM8K TRAIN seeded 500 (A17-B1), after the counts-only overlap drops",
           "selection": f"sha256('{cs.SEED}:{TAG}:'+id) ascending, first {N}", "overlap_file": str(ov_p),
           "overlap_sha256": sha256_file(ov_p), "refs": [r.get("name") for r in ov.get("refs", [])],
           "sets": {SET: {"rows": len(rows), "dropped_overlap_in_pool": len(drop), "think_type": {"math": len(rows)},
                          "sha256": sha256_file(f), "ids_sha256": hashlib.sha256("\n".join(ids).encode()).hexdigest(),
                          "licence": "MIT"}}}
    (OUT / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    if not a.no_modal:
        items = modal_items(rows, _think_path())
        write_jsonl(MODAL_IN, items)
        MODAL_MAN.write_text(json.dumps({"built_by": "think/b1b_sets.py finalize", "n": len(items),
                                         "gold_free": True, "outputs": {MODAL_IN.name: sha256_file(MODAL_IN)},
                                         "clean_manifest_sha256": sha256_file(OUT / "manifest.json")}, indent=1) + "\n")
    print(json.dumps({"rows": len(rows), "dropped_overlap_in_pool": len(drop), "sha256": man["sets"][SET]["sha256"][:16],
                      "modal_input": None if a.no_modal else sha256_file(MODAL_IN)[:16]}))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build").set_defaults(func=cmd_build)
    sub.add_parser("refs").set_defaults(func=cmd_refs)
    p = sub.add_parser("finalize")
    p.add_argument("--no-modal", action="store_true", help="skip the Modal input file (tests)")
    p.set_defaults(func=cmd_finalize)
    a = ap.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
